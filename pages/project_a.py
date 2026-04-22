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
# 🔥 문제 생성
# ==========================================
def generate_quiz(text, count, difficulty, q_type):

    prompt = f"""
JSON만 출력

[
  {{
    "question": "문제",
    "options": ["1","2","3","4"],
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
# 🎯 UI
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
            return

        quiz = generate_quiz(text, count, difficulty, q_type)

        ss.quiz = quiz
        ss.answers = {}
        ss.wrong = []
        ss.last_quiz_text = text

    # 문제
    if ss.quiz:

        total = len(ss.quiz) if ss.quiz else 0
        answered = len([v for v in ss.answers.values() if v])

        # 안전 progress
        if total > 0:
            prog = answered / total
            prog = max(0.0, min(1.0, prog))
        else:
            prog = 0.0

        st.progress(prog)

        for i, q in enumerate(ss.quiz):

            st.markdown(f"### Q{i+1}. {q.get('question','문제 오류')}")

            options = q.get("options", ["1","2","3","4"])

            ans = st.radio(
                "선택",
                ["선택 안함"] + options,
                key=f"q_{i}"
            )

            if ans != "선택 안함":
                ss.answers[i] = ans

        # 채점
        if st.button("💯 채점"):

            correct = 0
            wrong = []

            for i, q in enumerate(ss.quiz):

                user = ss.answers.get(i)
                answer = q.get("answer")

                if user == answer:
                    correct += 1
                else:
                    wrong.append(q)

                with st.expander(f"{i+1} 해설"):
                    st.write(q.get("explanation","없음"))

            # 안전 점수 계산
            if total > 0:
                score = int(correct / total * 100)
            else:
                score = 0

            st.metric("점수", f"{score}")

            ss.history.append(score)
            ss.wrong = wrong

        # 평균
        if ss.history:
            avg = int(sum(ss.history)/len(ss.history))
            st.metric("평균", avg)

        # 재출제
        if ss.wrong:
            if st.button("🔥 오답 재도전"):

                txt = " ".join([q.get("question","") for q in ss.wrong])

                ss.quiz = generate_quiz(
                    txt,
                    len(ss.wrong),
                    "어려움",
                    "함정"
                )
