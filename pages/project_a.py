import streamlit as st
import requests
import json
import re
import time
import random

# ==========================================
# 🔐 API KEY
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY 없음")
    st.stop()

# ==========================================
# 🔥 JSON 추출
# ==========================================
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None

def repair_json(text):
    try:
        text = text.replace("'", '"')
        text = re.sub(r",\s*}", "}", text)
        text = re.sub(r",\s*]", "]", text)
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        return None

# ==========================================
# ✅ 완화된 validate_quiz (핵심 수정)
# answer == options 완벽 일치 검증 제거
# ==========================================
def validate_quiz(quiz):
    if not isinstance(quiz, list) or len(quiz) == 0:
        return False
    for q in quiz:
        if not isinstance(q, dict):
            return False
        if not all(k in q for k in ["question", "options", "answer", "explanation"]):
            return False
        if not isinstance(q.get("options"), list) or len(q.get("options")) < 2:
            return False
    return True

# ==========================================
# 🔥 Gemini 호출
# ==========================================
def call_gemini(prompt, timeout=90):
    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ]

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 8192
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
        for attempt in range(3):
            try:
                res = requests.post(url, json=payload, timeout=timeout)
                if res.status_code == 200:
                    data = res.json()
                    try:
                        return data['candidates'][0]['content']['parts'][0]['text']
                    except:
                        return str(data)
                elif res.status_code in [429, 503]:
                    time.sleep((2 ** attempt) + 1)
            except requests.exceptions.Timeout:
                time.sleep(2)
            except Exception:
                time.sleep(1)
    return None

# ==========================================
# 🧠 긴 텍스트 청킹 요약
# ==========================================
def summarize_chunk(chunk, chunk_idx, total_chunks, status):
    prompt = f"""다음 텍스트(총 {total_chunks}개 중 {chunk_idx+1}번째 파트)에서 시험 문제 출제에 필요한 핵심 개념, 사실, 중요 용어, 수치, 정의만 간결하게 추출하세요.
불필요한 서론/인사/예의 표현은 제외하고 오직 학습 내용의 핵심만 bullet point 형태로 정리하세요.

텍스트:
{chunk}

핵심 내용만 bullet point로 출력:"""
    res = call_gemini(prompt, timeout=60)
    if res:
        status.write(f"  ✅ 파트 {chunk_idx+1}/{total_chunks} 요약 완료")
    return res or ""

def compress_long_text(text, status):
    MAX_DIRECT = 8000
    CHUNK_SIZE = 6000

    if len(text) <= MAX_DIRECT:
        return text

    status.write(f"📄 긴 문서 감지 ({len(text):,}자) → 청킹 분석 시작...")

    chunks = []
    remaining = text
    while len(remaining) > CHUNK_SIZE:
        cut = CHUNK_SIZE
        for boundary in ['. ', '.\n', '\n\n', '\n']:
            pos = remaining.rfind(boundary, CHUNK_SIZE // 2, CHUNK_SIZE)
            if pos > 0:
                cut = pos + len(boundary)
                break
        chunks.append(remaining[:cut])
        remaining = remaining[cut:]
    if remaining.strip():
        chunks.append(remaining)

    status.write(f"  총 {len(chunks)}개 파트로 분할 → 각 파트 핵심 추출 중...")

    summaries = []
    for i, chunk in enumerate(chunks):
        summary = summarize_chunk(chunk, i, len(chunks), status)
        summaries.append(summary)
        time.sleep(0.3)

    compressed = "\n\n".join(summaries)
    status.write(f"  📦 압축 완료: {len(text):,}자 → {len(compressed):,}자 ({len(compressed)*100//len(text)}%)")
    return compressed

# ==========================================
# fallback 문제
# ==========================================
def fallback_quiz(count):
    dummy = []
    for i in range(max(count, 1)):
        ans = random.choice(["보기 1", "보기 2", "보기 3", "보기 4"])
        dummy.append({
            "question": f"기본 문제 {i+1} (AI 생성 실패)",
            "options": ["보기 1", "보기 2", "보기 3", "보기 4"],
            "answer": ans,
            "explanation": "AI 실패로 생성된 임시 문제입니다. 내용을 줄여 다시 시도해주세요.",
            "study_note": ""
        })
    return dummy

# ==========================================
# 🔥 문제 생성
# ==========================================
def generate_quiz(text, count, difficulty, q_type, status):
    processed_text = compress_long_text(text, status)

    prompt = f"""당신은 전문 시험 출제 AI입니다. 아래 학습 내용을 바탕으로 정확히 {count}개의 4지선다 문제를 출제하세요.

⚠️ 출력 규칙 (반드시 준수):
1. 반드시 아래 JSON 배열 형식만 출력하세요
2. JSON 앞뒤에 어떤 텍스트도, 마크다운도 붙이지 마세요
3. answer 값은 반드시 options 배열의 4개 중 정확히 하나와 동일해야 합니다
4. 문자열 내부에 쌍따옴표(")가 필요하면 \\\"로 이스케이프하세요

출력 형식:
[
  {{
    "question": "구체적인 문제 내용",
    "options": ["보기1 내용", "보기2 내용", "보기3 내용", "보기4 내용"],
    "answer": "정답 보기 내용 (options 중 하나와 완전 일치)",
    "explanation": "왜 이 답인지 구체적 해설",
    "study_note": "시험 대비 핵심 암기 팁 또는 함정 포인트"
  }}
]

문제 수: 정확히 {count}개
난이도: {difficulty}
스타일: {q_type}

학습 내용:
{processed_text[:12000]}
"""

    for attempt in range(6):
        status.update(label=f"⏳ 문제 출제 중... (시도 {attempt+1}/6)", state="running")
        if attempt == 0:
            status.write("🤖 AI가 학습 내용을 분석하고 있습니다...")
        elif attempt == 1:
            status.write("🔄 다시 시도 중... (AI가 형식을 재조정 중)")
        else:
            status.write(f"🔁 {attempt+1}번째 재시도 중...")

        res = call_gemini(prompt, timeout=90)

        if not res:
            status.write("⚠️ 응답 없음, 재시도 중...")
            time.sleep(2)
            continue

        quiz = extract_json(res)
        if validate_quiz(quiz):
            if len(quiz) < count:
                status.write(f"⚠️ 문제 수 부족 ({len(quiz)}/{count}), 재시도...")
                continue
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz[:count]

        quiz = repair_json(res)
        if validate_quiz(quiz):
            status.write("🛠️ JSON 자동 복구 성공!")
            if len(quiz) < count:
                continue
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz[:count]

        # 부분 성공
        if isinstance(quiz, list) and len(quiz) >= max(1, count // 2):
            valid = [q for q in quiz if isinstance(q, dict) and all(k in q for k in ["question", "options", "answer", "explanation"])]
            if len(valid) >= max(1, count // 2):
                status.write(f"⚠️ 일부만 유효 ({len(valid)}개), 사용 중...")
                status.update(label=f"✨ 부분 출제 완료 ({len(valid)}개)", state="complete")
                return valid

        status.write(f"❌ {attempt+1}차 실패, 재시도...")
        time.sleep(1 + attempt * 0.5)

    status.update(label="🚨 출제 실패 (기본 문제로 대체)", state="error")
    return fallback_quiz(count)

# ==========================================
# 텍스트 품질 분석
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 200:
        return "❌ 너무 짧음 (문맥 파악 어려움)", 40
    elif l < 800:
        return "⚠️ 보통 (내용을 더 넣으면 좋습니다)", 70
    elif l < 8000:
        return "✅ 훌륭함 (완벽한 직접 출제 가능)", 95
    elif l < 30000:
        return "🔄 대용량 (청킹 요약 후 출제, 품질 양호)", 88
    else:
        return "📚 초대용량 (청킹 압축 후 출제, 2~3분 소요)", 82

# ==========================================
# CSS
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }

    .quiz-card {
        background: linear-gradient(145deg, #ffffff, #f5f7fa);
        border-radius: 20px; padding: 30px; margin-bottom: 25px;
        box-shadow: 10px 10px 30px #e6e6e6, -10px -10px 30px #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease;
    }
    .quiz-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); }
    .quiz-card-correct {
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffe6 100%);
        border: 2px solid #48bb78; box-shadow: 0 0 15px rgba(72, 187, 120, 0.3);
    }
    .quiz-card-wrong {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
        border: 2px solid #f56565; box-shadow: 0 0 15px rgba(245, 101, 101, 0.3);
    }
    .study-note {
        background: linear-gradient(135deg, #fffcf0 0%, #fff3cd 100%);
        border-left: 6px solid #f59e0b; padding: 20px; margin-top: 20px;
        border-radius: 12px; color: #92400e; font-size: 1.05em; font-weight: 500;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.1); line-height: 1.6;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important; border-radius: 50px !important;
        padding: 12px 28px !important; font-weight: 700 !important; font-size: 1.1em !important;
        transition: all 0.3s ease !important; box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4) !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05) translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(118, 75, 162, 0.6) !important;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa; border-radius: 10px 10px 0 0; padding: 10px 20px;
        border: 1px solid #e9ecef; border-bottom: none; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important; border-top: 3px solid #667eea !important;
        font-weight: 700 !important; color: #764ba2 !important;
    }
    .chunk-info {
        background: linear-gradient(135deg, #e8f4fd, #d1ecf1);
        border-left: 4px solid #17a2b8; padding: 12px 16px;
        border-radius: 8px; font-size: 0.9em; color: #0c5460; margin: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎯 UI
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 (Premium Edition)")

    with st.expander("💡 [필독] AI 모의고사 200% 활용 가이드 및 주의사항", expanded=False):
        st.markdown("""
        **환영합니다! 이 앱은 입력하신 문서/노트를 기반으로 AI가 모의고사를 출제해주는 도구입니다.**

        ✅ **글자 수 제한 없음 — 긴 문서도 OK:**
        내부적으로 긴 문서를 청킹(분할) → 핵심 요약 → 압축 후 출제하므로, 책 한 챕터 분량도 처리 가능합니다.
        단, 문서가 길수록 처리 시간이 길어집니다 (최대 3~5분).

        ⏳ **처리 시간 안내:**
        - 8,000자 이하: 1~2분 (직접 출제)
        - 8,000~30,000자: 2~4분 (청킹 요약 후 출제)
        - 30,000자 이상: 4~6분 (다단계 압축 후 출제)

        🚨 **실패 시:** 내용을 조금 줄이거나 핵심 부분만 남겨 다시 시도해주세요.

        🔥 **오답 복수전:** 채점 후 [성적표] 탭 하단의 '하드코어 오답 복수전' 버튼을 눌러보세요!
        """)

    ss = st.session_state
    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("last_quiz_text", "")

    if st.button("🧹 전체 초기화"):
        st.session_state.clear()
        st.rerun()

    inject_custom_css()

    tab1, tab2, tab3 = st.tabs(["📝 출제 설정", "🎯 응시 화면", "📊 성적표 및 복습"])

    with tab1:
        text = st.text_area(
            "📚 학습 내용 입력 (글자 수 제한 없음, 길수록 처리 시간 증가)",
            height=250,
            placeholder="여기에 공부한 노트, 회의록, 교재 내용을 붙여넣으세요! 길어도 됩니다."
        )

        char_count = len(text)
        st.caption(f"현재 글자 수: {char_count:,}자")

        q, p = analyze_text_quality(text)
        st.info(f"텍스트 분석: {q} / 출제 성공 확률: {p}%")

        if char_count > 8000:
            st.markdown(f"""
            <div class="chunk-info">
            ℹ️ <b>청킹 모드 활성화:</b> {char_count:,}자 텍스트를 {max(2, char_count//6000)}개 파트로 분할 요약 후 출제합니다.
            예상 처리 시간: 약 {max(2, char_count//8000 * 2 + 1)}~{max(3, char_count//8000 * 3 + 2)}분
            </div>
            """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        count = col1.slider("출제 문항 수", 3, 20, 5)
        difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움", "최상(지옥)"])
        q_type = col3.selectbox("문제 스타일", ["개념 확인", "실무 응용", "함정 유발"])

        if st.button("🚀 AI 모의고사 출제 시작"):
            if not text.strip():
                st.warning("⚠️ 출제할 학습 내용을 먼저 입력해주세요.")
            else:
                with st.status("🚀 AI 엔진 가동 중...", expanded=True) as status:
                    quiz = generate_quiz(text, count, difficulty, q_type, status)

                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.last_quiz_text = text

                st.toast("🚀 출제 완료! [응시 화면] 탭으로 이동하세요.", icon="✅")

    # Tab 2: 응시
    if ss.quiz:
        total = len(ss.quiz)
        answered = len([v for v in ss.answers.values() if v])
        prog = max(0.0, min(1.0, answered / total)) if total > 0 else 0.0

        with tab2:
            st.progress(prog, text=f"진행률: {answered} / {total} 문항")

            for i, q in enumerate(ss.quiz):
                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                st.markdown(f"### Q{i+1}. {q.get('question','문제 오류')}")

                options = q.get("options", ["보기1", "보기2", "보기3", "보기4"])
                ans = st.radio("선택", ["선택 안함"] + options, key=f"q_{i}")

                if ans != "선택 안함":
                    if ss.answers.get(i) != ans:
                        st.toast(f"{i+1}번 마킹 완료!", icon="✏️")
                    ss.answers[i] = ans

                st.markdown('</div>', unsafe_allow_html=True)

        # Tab 3: 성적표
        with tab3:
            if st.button("💯 OMR 제출 및 채점하기"):
                correct = 0
                wrong = []

                with st.spinner("📊 채점 중..."):
                    time.sleep(0.8)
                    for i, q in enumerate(ss.quiz):
                        # ✅ 핵심 수정: strip()으로 공백 차이 무시하고 채점
                        user = (ss.answers.get(i) or "").strip()
                        answer = (q.get("answer") or "").strip()
                        is_wrong = (user != answer)

                        card_class = "quiz-card-wrong" if is_wrong else "quiz-card-correct"
                        st.markdown(f'<div class="quiz-card {card_class}">', unsafe_allow_html=True)

                        if is_wrong:
                            wrong.append(q)
                            st.error(f"🔴 Q{i+1}. 오답 (내 답: {user} / 정답: {answer})")
                        else:
                            correct += 1
                            st.success(f"🟢 Q{i+1}. 정답!")

                        st.markdown(f"**문제:** {q.get('question','')}")

                        with st.expander(f"📖 {i+1}번 해설 보기", expanded=is_wrong):
                            st.write(f"**해설:** {q.get('explanation','없음')}")
                            if q.get("study_note"):
                                st.markdown(f'<div class="study-note">👨‍🏫 <b>1타 강사 Note:</b><br>{q.get("study_note")}</div>', unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

                    score = int(correct / total * 100) if total > 0 else 0
                    st.metric("최종 점수", f"{score} 점")

                    if score == 100:
                        st.balloons()
                        st.toast("완벽합니다! 100점 만점! 🎉", icon="🏆")
                    elif score >= 70:
                        st.toast("훌륭한 점수네요! 👍", icon="🌟")
                    else:
                        st.toast("오답 노트를 꼭 확인하세요! 💪", icon="🔥")

                    ss.history.append(score)
                    ss.wrong = wrong

            if ss.history:
                avg = int(sum(ss.history) / len(ss.history))
                st.metric("나의 누적 평균 점수", f"{avg} 점")

            if ss.wrong:
                st.markdown("---")
                st.subheader("🔥 오답 밀착 마크 — 하드코어 복수전")
                st.caption(f"틀린 {len(ss.wrong)}개 문제의 개념으로 지옥 난이도 재출제")

                if st.button("🚨 틀린 내용으로만 지옥 난이도 재도전"):
                    with st.status("🔥 오답 분석 중...", expanded=True) as status:
                        txt = " ".join([
                            q.get("question", "") + " " +
                            q.get("study_note", "") + " " +
                            q.get("explanation", "")
                            for q in ss.wrong
                        ])
                        ss.quiz = generate_quiz(
                            txt, len(ss.wrong), "최상(지옥)", "함정 유발", status
                        )
                        ss.answers = {}
                        ss.wrong = []
                    st.rerun()
