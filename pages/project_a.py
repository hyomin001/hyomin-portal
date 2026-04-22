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
# 🔥 문제 생성 (실시간 상태 중계 및 방탄 로직)
# ==========================================
def generate_quiz(text, count, difficulty, q_type, status):

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

    for attempt in range(5):
        # UI에 현재 진행 상태 실시간 업데이트
        status.update(label=f"⏳ AI 모의고사 출제 중... (시도 {attempt + 1}/5)", state="running")
        status.write(f"🤖 딥러닝 모델 호출 중... (데이터가 길면 최대 30초 이상 소요될 수 있습니다.)")
        
        res = call_gemini(prompt)

        if not res:
            status.write(f"⚠️ {attempt + 1}차 시도 응답 없음. 다시 시도합니다.")
            continue

        status.write("🔍 AI 응답 완료! 데이터 형식(JSON) 검증 중...")
        quiz = extract_json(res)
        
        if validate_quiz(quiz):
            status.write("✅ 완벽한 JSON 데이터 확인 완료!")
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz

        status.write("🔧 형식이 조금 어긋났습니다. 자동 복구를 시도합니다...")
        quiz = repair_json(res)
        
        if validate_quiz(quiz):
            status.write("🛠️ 데이터 복구 성공!")
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz

        status.write(f"❌ {attempt + 1}차 시도 실패. AI를 다시 호출합니다...")
        time.sleep(1)

    status.update(label="🚨 AI 출제 최종 실패 (기본 문제로 대체됩니다)", state="error")
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
# 🎨 UI CSS 주입 함수 (프리미엄, 화려한 디자인)
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    /* Google Font 적용 (Noto Sans KR) */
    @import url('[https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap](https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap)');
    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif !important;
    }

    /* 기본 문제 카드 (Neumorphism & Glassmorphism 혼합 럭셔리 스타일) */
    .quiz-card {
        background: linear-gradient(145deg, #ffffff, #f5f7fa);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 10px 10px 30px #e6e6e6, -10px -10px 30px #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease;
    }
    .quiz-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
    }

    /* 정답/오답 카드 (화려한 빛 반사 및 네온 스타일 테두리) */
    .quiz-card-correct {
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffe6 100%);
        border: 2px solid #48bb78;
        box-shadow: 0 0 15px rgba(72, 187, 120, 0.3);
    }
    .quiz-card-wrong {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
        border: 2px solid #f56565;
        box-shadow: 0 0 15px rgba(245, 101, 101, 0.3);
    }

    /* 1타 강사 노트 (프리미엄 골드 포인트) */
    .study-note {
        background: linear-gradient(135deg, #fffcf0 0%, #fff3cd 100%);
        border-left: 6px solid #f59e0b;
        padding: 20px;
        margin-top: 20px;
        border-radius: 12px;
        color: #92400e;
        font-size: 1.05em;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.1);
        line-height: 1.6;
    }

    /* Streamlit 기본 버튼 오버라이딩 (그라데이션 버튼) */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 28px !important;
        font-weight: 700 !important;
        font-size: 1.1em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4) !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05) translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(118, 75, 162, 0.6) !important;
    }
    
    /* 탭 메뉴 스타일링 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        border: 1px solid #e9ecef;
        border-bottom: none;
        transition: 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        border-top: 3px solid #667eea !important;
        font-weight: 700 !important;
        color: #764ba2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎯 UI (렌더링)
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 (Premium Edition)")

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
                # 🚀 스피너 대신 확장형 상태창(status) 사용
                with st.status("🚀 AI 엔진 가동 중...", expanded=True) as status:
                    quiz = generate_quiz(text, count, difficulty, q_type, status)

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
            if st.button("💯 채점 및 결과 확인"):

                correct = 0
                wrong = []

                # 채점 중 연출을 위한 짧은 스피너
                with st.spinner("📊 OMR 카드를 채점하고 있습니다..."):
                    time.sleep(1) # 극적인 효과를 위해 1초 대기

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
                        with st.expander(f"📖 {i+1}번 해설 및 1타 강사의 꿀팁 보기", expanded=is_wrong):
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
                if st.button("🚨 틀린 문제로만 지옥 난이도 재도전"):
                    
                    # 🚀 재도전 시에도 상태창 적용
                    with st.status("🔥 오답 분석 및 지옥 난이도 재출제 중...", expanded=True) as status:
                        txt = " ".join([q.get("question","") + " " + q.get("study_note", "") for q in ss.wrong])

                        ss.quiz = generate_quiz(
                            txt,
                            len(ss.wrong),
                            "어려움",
                            "함정",
                            status # status 객체 전달
                        )
                        ss.answers = {}
                        ss.wrong = []
                    
                    st.rerun()
