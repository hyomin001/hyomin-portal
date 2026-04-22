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
# 🔥 Gemini 호출 (503 대응)
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

    raise Exception("모든 모델 실패")


# ==========================================
# 🔥 fallback 문제
# ==========================================
def fallback_quiz(count):
    dummy = []
    for i in range(count):
        ans = random.choice(["1", "2", "3", "4"])
        dummy.append({
            "question": f"기본 문제 {i+1}: 다음 중 올바른 것은?",
            "options": ["1", "2", "3", "4"],
            "answer": ans,
            "explanation": "AI 서버 불안정으로 기본 문제가 제공됩니다."
        })
    return dummy


# ==========================================
# 🔥 문제 생성
# ==========================================
def generate_quiz(text, count, difficulty, q_type):

    prompt = f"""
너는 시험 출제 AI다.

규칙:
- JSON 외 출력 금지
- 반드시 [ 로 시작, ] 로 끝

[
  {{
    "question": "문제",
    "options": ["1", "2", "3", "4"],
    "answer": "정답",
    "explanation": "해설"
  }}
]

문제 수: {count}
난이도: {difficulty}
스타일: {q_type}

{text[:2000]}
"""

    for _ in range(5):
        try:
            res = call_gemini(prompt)

            quiz = extract_json(res)
            if quiz:
                return quiz

            quiz = repair_json(res)
            if quiz:
                return quiz

        except:
            pass

        time.sleep(1)

    st.warning("⚠️ AI 생성 실패 → 기본 문제 제공")
    return fallback_quiz(count)


# ==========================================
# 🎯 UI (기존 구조 유지)
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 시스템 ")
    st.caption("2026/04/22업데이트 완료!")

    # 상태
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "wrong" not in st.session_state:
        st.session_state.wrong = []
    if "history" not in st.session_state:
        st.session_state.history = []

    # 초기화
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.rerun()

    # ==============================
    # 📘 사용자 가이드
    # ==============================
    with st.expander("📘 사용 가이드 (성공률 높이는 법)"):
        st.markdown("""
### ✅ 잘 되는 입력 방법
- 핵심 개념이 포함된 텍스트 (이론 설명)
- 너무 짧지 않게 (최소 300자 이상)
- 표, 기호, 깨진 PDF는 피하기

### ❌ 실패 잘 나는 경우
- 너무 긴 텍스트 (5000자 이상)
- 이미지 기반 PDF
- 의미 없는 데이터 로그

### 🎯 추천 세팅
- 문제 수: 5 ~ 7
- 난이도: 보통 → 점수 보고 조절
- 스타일: 개념 → 응용 순으로 학습

### 💡 성공 확률
- 일반 텍스트: 약 90% 이상
- PDF: 약 70~80%
- 긴 기술문서: 약 60%
        """)

    # 입력
    text = st.text_area("📚 학습 내용", height=200)

    col1, col2, col3 = st.columns(3)
    count = col1.slider("문제 수", 3, 10, 5)
    difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움"])
    q_type = col3.selectbox("스타일", ["개념", "응용", "함정"])

    # 생성
    if st.button("🚀 문제 생성", use_container_width=True):

        if not text.strip():
            st.warning("내용 입력하세요")
            return

        with st.spinner("문제 생성 중..."):
            quiz = generate_quiz(text, count, difficulty, q_type)

            st.session_state.quiz = quiz
            st.session_state.answers = {}
            st.session_state.wrong = []

            st.success("✅ 생성 완료")

    # 문제
    if st.session_state.quiz:
        st.write("---")

        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['question']}")

            ans = st.radio(
                "정답 선택",
                ["선택 안함"] + q['options'],
                key=f"q{i}"
            )

            if ans == "선택 안함":
                ans = None

            st.session_state.answers[i] = ans

        # 채점
        if st.button("💯 채점", use_container_width=True):

            correct = 0
            wrong_list = []

            for i, q in enumerate(st.session_state.quiz):
                user = st.session_state.answers.get(i)

                if user == q['answer']:
                    correct += 1
                    st.success(f"{i+1}번 정답")
                else:
                    st.error(f"{i+1}번 오답 (정답: {q['answer']})")
                    wrong_list.append(q)

                with st.expander("해설"):
                    st.write(q['explanation'])

            score = int(correct / len(st.session_state.quiz) * 100)
            st.metric("🎯 점수", f"{score}점")

            st.session_state.history.append(score)
            st.session_state.wrong = wrong_list

        # 평균
        if st.session_state.history:
            avg = sum(st.session_state.history) / len(st.session_state.history)
            st.metric("📊 평균 점수", f"{int(avg)}점")

        # 재출제
        if st.session_state.wrong:
            if st.button("🔥 틀린 문제 다시 풀기"):

                wrong_text = "\n".join([
                    f"{q['question']} {q['explanation']}"
                    for q in st.session_state.wrong
                ])

                with st.spinner("재출제 중..."):
                    quiz = generate_quiz(
                        wrong_text,
                        len(st.session_state.wrong),
                        "어려움",
                        "함정"
                    )

                    st.session_state.quiz = quiz
                    st.success("재출제 완료!")
