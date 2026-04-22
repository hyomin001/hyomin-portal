import streamlit as st
import requests
import json
import re
import time

# ==========================================
# 🔐 API KEY
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

if not GOOGLE_API_KEY:
    st.error("❌ API KEY 없음")
    st.stop()


# ==========================================
# 🔥 JSON 복구 엔진
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


def force_json_repair(text):
    """깨진 JSON 강제 복구"""
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
# 🔥 Gemini 안정 호출
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
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"

        for attempt in range(5):
            try:
                res = requests.post(url, json=payload, timeout=20)

                if res.status_code == 200:
                    data = res.json()

                    try:
                        return data['candidates'][0]['content']['parts'][0]['text']
                    except:
                        return str(data)

                elif res.status_code in [429, 503]:
                    wait = (2 ** attempt) + 1
                    st.warning(f"{model} 과부하 → {wait}s")
                    time.sleep(wait)

            except Exception as e:
                st.warning(f"{model} 오류: {e}")
                time.sleep(1)

    raise Exception("모든 모델 실패")


# ==========================================
# 🔥 문제 생성 (초강화)
# ==========================================
def generate_quiz(text, count, difficulty, q_type):

    prompt = f"""
너는 시험 출제 AI다.

절대 규칙:
- JSON 외 출력 금지
- 반드시 [ 로 시작, ] 로 끝
- 설명 금지

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

자료:
{text[:4000]}
"""

    for i in range(5):
        res = call_gemini(prompt)

        quiz = extract_json(res)
        if quiz:
            return quiz

        # 🔥 복구 시도
        quiz = force_json_repair(res)
        if quiz:
            return quiz

        st.warning(f"재시도 {i+1}/5")

    return None


# ==========================================
# 🎯 UI
# ==========================================
def render():

    st.title("🔥 AI 모의고사 ")
    st.caption("시험모드 + 자동난이도 + 안정화 완료")

    # 상태
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "wrong" not in st.session_state:
        st.session_state.wrong = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "보통"
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # 초기화
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.rerun()

    # 입력
    text = st.text_area("📚 학습 내용", height=200)

    col1, col2 = st.columns(2)
    count = col1.slider("문제 수", 3, 10, 5)
    q_type = col2.selectbox("스타일", ["개념", "응용", "함정"])

    # 시험 모드
    exam_mode = st.checkbox("⏱️ 시험 모드 (60초)")

    # 생성
    if st.button("🚀 문제 생성"):

        if not text.strip():
            st.warning("내용 입력")
            return

        with st.spinner("AI 생성 중..."):
            quiz = generate_quiz(
                text,
                count,
                st.session_state.difficulty,
                q_type
            )

            if not quiz:
                st.error("❌ 생성 실패")
                return

            st.session_state.quiz = quiz
            st.session_state.answers = {}
            st.session_state.wrong = []

            if exam_mode:
                st.session_state.start_time = time.time()

            st.success("✅ 완료")

    # 문제
    if st.session_state.quiz:

        # 타이머
        if st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            remain = max(0, 60 - int(elapsed))
            st.metric("⏱️ 남은 시간", f"{remain}s")

            if remain == 0:
                st.warning("시간 종료!")
                st.session_state.start_time = None

        st.progress(len(st.session_state.answers) / len(st.session_state.quiz))

        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['question']}")

            ans = st.radio(
                "선택",
                ["선택 안함"] + q['options'],
                key=f"q{i}"
            )

            if ans != "선택 안함":
                st.session_state.answers[i] = ans

        # 채점
        if st.button("💯 채점"):

            correct = 0
            wrong = []

            for i, q in enumerate(st.session_state.quiz):
                user = st.session_state.answers.get(i)

                if user == q['answer']:
                    correct += 1
                else:
                    wrong.append(q)

            score = int(correct / len(st.session_state.quiz) * 100)
            st.metric("점수", f"{score}점")

            st.session_state.history.append(score)
            st.session_state.wrong = wrong

            # 🔥 난이도 자동 조절
            if score < 40:
                st.session_state.difficulty = "쉬움"
            elif score > 80:
                st.session_state.difficulty = "어려움"

        # 통계
        if st.session_state.history:
            avg = sum(st.session_state.history) / len(st.session_state.history)
            st.metric("📊 평균 점수", f"{int(avg)}점")

        # 재출제
        if st.session_state.wrong:
            if st.button("🔥 오답 다시"):

                wrong_text = "\n".join([
                    f"{q['question']} {q['explanation']}"
                    for q in st.session_state.wrong
                ])

                quiz = generate_quiz(
                    wrong_text,
                    len(st.session_state.wrong),
                    "어려움",
                    "함정"
                )

                if quiz:
                    st.session_state.quiz = quiz
                    st.success("재출제 완료")
