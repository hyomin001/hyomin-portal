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

# ==========================================
# 🔥 JSON 복구
# ==========================================
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
# 🔥 quiz 검증
# ==========================================
def validate_quiz(quiz):
    if not isinstance(quiz, list):
        return False
    for q in quiz:
        if not isinstance(q, dict):
            return False
        if not all(k in q for k in ["question", "options", "answer", "explanation"]):
            return False
    return True

# ==========================================
# 🔥 Gemini 호출
# ==========================================
def call_gemini(prompt):

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
            "maxOutputTokens": 2048
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"

        for attempt in range(5):
            try:
                res = requests.post(url, json=payload, timeout=10)

                if res.status_code == 200:
                    data = res.json()
                    try:
                        return data['candidates'][0]['content']['parts'][0]['text']
                    except:
                        return str(data)

                elif res.status_code in [429, 503]:
                    time.sleep((2 ** attempt) + 1)

            except:
                time.sleep(1)

    return None

# ==========================================
# 🔥 fallback 문제
# ==========================================
def fallback_quiz(count):
    dummy = []
    for i in range(max(count, 1)):
        ans = random.choice(["1", "2", "3", "4"])
        dummy.append({
            "question": f"기본 문제 {i+1}",
            "options": ["1", "2", "3", "4"],
            "answer": ans,
            "explanation": "AI 실패로 생성된 문제"
        })
    return dummy

# ==========================================
# 🔥 문제 생성 (방탄 로직 & 1타 강사 프롬프트 추가)
# ==========================================
def generate_quiz(text, count, difficulty, q_type):

    prompt = f"""
무조건 JSON 배열 형식으로만 출력하세요. 마크다운(` ```json ` 등)이나 일반 텍스트는 절대 포함하지 마세요.
🚨 절대 규칙: 정답(answer)은 반드시 options 배열에 제공된 4개의 보기 중 하나와 100% 일치해야 합니다.

[
  {{
    "question": "문제",
    "options": ["1","2","3","4"],
    "answer": "정답",
    "explanation": "해설",
    "study_note": "👩‍🏫 1타 강사의 꿀팁, 함정 피하는 법 또는 암기법"
  }}
]

문제 수: {count}
난이도: {difficulty}
스타일: {q_type}

학습 내용:
{text[:2000]}
"""

    for _ in range(5):
        res = call_gemini(prompt)

        if not res:
            continue

        quiz = extract_json(res)
        if validate_quiz(quiz):
            return quiz

        quiz = repair_json(res)
        if validate_quiz(quiz):
            return quiz

        time.sleep(1)

    st.warning("⚠️ AI 실패 → 기본 문제")
    return fallback_quiz(count)

# ==========================================
# 🔥 텍스트 품질
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 200:
        return "❌ 짧음", 40
    elif l < 800:
        return "⚠️ 보통", 70
    else:
        return "✅ 좋음", 90

# ==========================================
# 🎨 UI CSS 주입 함수 (웹 서비스급 스타일링)
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* 기본 문제 카드 둥글고 예쁘게 */
    .quiz-card {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        transition: transform 0.2s ease-in-out;
    }
    .quiz-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }
    /* 정답/오답 카드 강조 */
    .quiz-card-correct {
        border-left: 6px solid #4CAF50 !important;
        background-color: #f2fdf4;
    }
    .quiz-card-wrong {
        border-left: 6px solid #F44336 !important;
        background-color: #fff5f5;
    }
    /* 1타 강사 노트 (노란색 포스트잇 느낌) */
    .study-note {
        background-color: #fff8e1;
        border-left: 5px solid #ffc107;
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
        color: #856404;
        font-size: 0.95em;
        line-height: 1.5;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎯 UI (렌더링)
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 (완전 안정화)")

    # 상태 초기화
    ss = st.session_state

    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("last_quiz_text", "")
    ss.setdefault("start_time", None)

    # 초기화
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.rerun()

    # 예쁜 CSS 적용
    inject_custom_css() 

    # 탭 구조 분할
    tab1, tab2, tab3 = st.tabs(["📝 출제 설정", "🎯 응시 화면", "📊 성적표 및 복습"])

    with tab1:
        # 입력
        text = st.text_area("📚 학습 내용", height=200)
        st.caption(f"글자수: {len(text)}")

        q, p = analyze_text_quality(text)
        st.info(f"{q} / 성공확률 {p}%")

        col1, col2, col3 = st.columns(3)
        count = col1.slider("문제 수", 3, 10, 5)
        difficulty = col2.selectbox("난이도", ["쉬움","보통","어려움"])
        q_type = col3.selectbox("스타일", ["개념","응용","함정"])

        # 생성
        if st.button("🚀 문제 생성"):

            if not text.strip():
                st.warning("입력 필요")
            else:
                quiz = generate_quiz(text, count, difficulty, q_type)

                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.last_quiz_text = text
                
                st.toast("🚀 출제 완료! [응시 화면] 탭으로 이동하세요.", icon="✅")

    # 문제 로직
    if ss.quiz:

        total = len(ss.quiz) if ss.quiz else 0
        answered = len([v for v in ss.answers.values() if v])

        # 안전 progress
        if total > 0:
            prog = answered / total
            prog = max(0.0, min(1.0, prog))
        else:
            prog = 0.0

        with tab2:
            st.progress(prog)

            for i, q in enumerate(ss.quiz):

                st.markdown('<div class="quiz-card">', unsafe_allow_html=True) # 카드 시작
                st.markdown(f"### Q{i+1}. {q.get('question','문제 오류')}")

                options = q.get("options", ["1","2","3","4"])

                ans = st.radio(
                    "선택",
                    ["선택 안함"] + options,
                    key=f"q_{i}"
                )

                if ans != "선택 안함":
                    if ss.answers.get(i) != ans: # 새로 마킹했을 때만 알림
                        st.toast(f"{i+1}번 마킹 완료!", icon="✏️")
                    ss.answers[i] = ans
                
                st.markdown('</div>', unsafe_allow_html=True) # 카드 끝

        with tab3:
            # 채점
            if st.button("💯 채점"):

                correct = 0
                wrong = []

                for i, q in enumerate(ss.quiz):

                    user = ss.answers.get(i)
                    answer = q.get("answer")
                    is_wrong = (user != answer)

                    # 맞힌 문제/틀린 문제 시각적 분리
                    card_class = "quiz-card-wrong" if is_wrong else "quiz-card-correct"
                    st.markdown(f'<div class="quiz-card {card_class}">', unsafe_allow_html=True)
                    
                    if is_wrong:
                        wrong.append(q)
                        st.error(f"🔴 Q{i+1}. 오답입니다. (내 답: {user} / 정답: {answer})")
                    else:
                        correct += 1
                        st.success(f"🟢 Q{i+1}. 정답입니다!")
                        
                    st.markdown(f"**문제:** {q.get('question','')}")
                    
                    # 1타 강사 오답 밀착 마크: 틀린 문제는 자동으로 expander가 열림
                    with st.expander(f"📖 {i+1}번 해설 및 강사의 꿀팁 보기", expanded=is_wrong):
                        st.write(f"**해설:** {q.get('explanation','없음')}")
                        if "study_note" in q and q["study_note"]:
                            st.markdown(f'<div class="study-note">👨‍🏫 <b>1타 강사 Note:</b><br>{q.get("study_note")}</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)

                # 안전 점수 계산 및 애니메이션 피드백
                if total > 0:
                    score = int(correct / total * 100)
                else:
                    score = 0

                st.metric("최종 점수", f"{score} 점")
                
                if score == 100:
                    st.balloons()
                    st.toast("완벽합니다! 100점 만점! 🎉", icon="🏆")
                elif score >= 70:
                    st.toast("수고하셨습니다! 좋은 점수네요. 👍", icon="🌟")
                else:
                    st.toast("조금만 더 복습해볼까요? 오답 노트를 확인하세요! 💪", icon="🔥")

                ss.history.append(score)
                ss.wrong = wrong

            # 평균
            if ss.history:
                avg = int(sum(ss.history)/len(ss.history))
                st.metric("나의 평균", avg)

            # 재출제 (하드코어 오답 복수전)
            if ss.wrong:
                st.markdown("---")
                st.subheader("🔥 하드코어 오답 복수전")
                if st.button("🚨 틀린 문제로만 최상 난이도 재도전"):

                    txt = " ".join([q.get("question","") + " " + q.get("study_note", "") for q in ss.wrong])
                    st.toast("오답 분석 및 하드코어 모의고사 출제 중...", icon="⏳")

                    ss.quiz = generate_quiz(
                        txt,
                        len(ss.wrong),
                        "어려움",
                        "함정"
                    )
                    ss.answers = {}
                    ss.wrong = []
                    st.rerun()
