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
# 🔥 추가 기능
# ==========================================
def analyze_text_quality(text):
    length = len(text)
    if length < 200:
        return "❌ 너무 짧음", 40
    elif length < 800:
        return "⚠️ 보통", 70
    else:
        return "✅ 좋음", 90

# ==========================================
# 🎯 UI
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 시스템")
    st.caption("업데이트: 기능 확장 버전")

    # 상태
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "wrong" not in st.session_state:
        st.session_state.wrong = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "last_quiz_text" not in st.session_state:
        st.session_state.last_quiz_text = ""
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # 초기화
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.rerun()

    # 가이드
    with st.expander("📘 사용 가이드"):
        st.markdown("텍스트 300자 이상 권장 / 너무 길면 실패 확률 증가")

    # 입력
    text = st.text_area("📚 학습 내용", height=200)
    st.caption(f"✏️ 글자 수: {len(text)}자")

    quality, prob = analyze_text_quality(text)
    st.info(f"📊 입력 상태: {quality} | 성공확률: {prob}%")

    col1, col2, col3 = st.columns(3)
    count = col1.slider("문제 수", 3, 10, 5)
    difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움"])
    q_type = col3.selectbox("스타일", ["개념", "응용", "함정"])

    # 이전 문제
    if st.button("📥 이전 문제 불러오기"):
        if st.session_state.last_quiz_text:
            st.session_state.quiz = generate_quiz(
                st.session_state.last_quiz_text, count, difficulty, q_type
            )

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
            st.session_state.last_quiz_text = text

            st.success("✅ 생성 완료")

    # 시험 시작
    if st.button("⏱️ 시험 시작"):
        st.session_state.start_time = time.time()

    if st.session_state.start_time:
        elapsed = int(time.time() - st.session_state.start_time)
        st.metric("⏱️ 경과 시간", f"{elapsed}초")

    # 문제
    if st.session_state.quiz:

        total = len(st.session_state.quiz)
        answered = len([v for v in st.session_state.answers.values() if v])
        st.progress(answered / total)

        # 셔플
        if st.button("🔀 문제 섞기"):
            random.shuffle(st.session_state.quiz)

        # 다운로드
        st.download_button(
            "📥 문제 다운로드",
            json.dumps(st.session_state.quiz, ensure_ascii=False, indent=2),
            file_name="quiz.json"
        )

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

        # 정답 보기
        if st.button("👀 전체 정답 보기"):
            for i, q in enumerate(st.session_state.quiz):
                st.write(f"{i+1}번 → {q['answer']}")

        # 평균 + 최고
        if st.session_state.history:
            avg = sum(st.session_state.history) / len(st.session_state.history)
            st.metric("📊 평균 점수", f"{int(avg)}점")
            st.metric("🏆 최고 점수", f"{max(st.session_state.history)}점")

            st.line_chart(st.session_state.history)

            if avg < 50:
                st.warning("👉 난이도 낮추는 걸 추천")
            elif avg > 80:
                st.success("👉 난이도 올려도 됩니다")

        # 오답만 보기
        if st.session_state.wrong:
            if st.checkbox("❌ 오답만 보기"):
                for q in st.session_state.wrong:
                    st.write(q['question'])

            # 재출제
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
