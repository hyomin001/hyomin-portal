import streamlit as st
import requests
import json
import re
import os
import time

# ==========================================
# 🔐 API KEY
# ==========================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"].strip()

# ==========================================
# 🔥 JSON 추출 (강화)
# ==========================================
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1:
            return json.loads(text[start:end+1])

        return None
    except:
        return None


# ==========================================
# 🔥 Gemini 호출 (완전 안정화)
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

        for attempt in range(3):
            try:
                res = requests.post(url, json=payload, timeout=15)

                if res.status_code == 200:
                    st.info(f"🤖 사용 모델: {model}")
                    return res.json()['candidates'][0]['content']['parts'][0]['text']

                else:
                    st.warning(f"{model} 실패 ({res.status_code})")
                    st.text(res.text)

                if res.status_code in [429, 503]:
                    time.sleep(2 + attempt)

            except Exception as e:
                st.warning(f"{model} 오류: {e}")
                time.sleep(1)

    raise Exception("❌ 모든 모델 호출 실패")


# ==========================================
# 🔥 문제 생성 (JSON 강제)
# ==========================================
def generate_quiz(text, count, difficulty, q_type):

    prompt = f"""
너는 시험 출제 전문가다.

조건:
- 문제 수: {count}
- 난이도: {difficulty}
- 스타일: {q_type}

규칙:
- 실제 시험처럼 출제
- 헷갈리는 오답 포함
- 핵심 개념 기반
- 반드시 JSON 배열만 출력
- 다른 말 절대 금지

[
  {{
    "question": "문제",
    "options": ["1번", "2번", "3번", "4번"],
    "answer": "정답 텍스트",
    "explanation": "핵심 해설"
  }}
]

자료:
{text[:5000]}
"""

    for _ in range(3):
        res = call_gemini(prompt)
        quiz = extract_json(res)

        if quiz:
            return quiz

    return None


# ==========================================
# 메인 UI
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 시스템 (안정화 버전)")
    st.caption("문제 생성 + 채점 + 오답 분석 + 재출제")

    # 상태
    if "quiz" not in st.session_state:
        st.session_state.quiz = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "wrong" not in st.session_state:
        st.session_state.wrong = []

    # 초기화
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.rerun()

    # ==============================
    # 파일 업로드
    # ==============================
    uploaded_file = st.file_uploader(
        "📄 파일 업로드 (txt, pdf)",
        type=["txt", "pdf"]
    )

    file_text = ""

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".txt"):
                file_text = uploaded_file.read().decode("utf-8")

            elif uploaded_file.name.endswith(".pdf"):
                import PyPDF2
                reader = PyPDF2.PdfReader(uploaded_file)

                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        file_text += txt

            st.success(f"파일 업로드 완료: {uploaded_file.name}")

        except Exception as e:
            st.error(f"파일 처리 실패: {e}")

    # ==============================
    # 입력
    # ==============================
    text = st.text_area("📚 학습 내용", value=file_text, height=200)

    col1, col2, col3 = st.columns(3)
    count = col1.slider("문제 수", 3, 10, 5)
    difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움"])
    q_type = col3.selectbox("스타일", ["개념", "응용", "함정"])

    # ==============================
    # 문제 생성
    # ==============================
    if st.button("🚀 문제 생성", use_container_width=True):

        if not text.strip():
            st.warning("내용 입력하세요")
            return

        with st.spinner("문제 생성 중..."):
            try:
                quiz = generate_quiz(text, count, difficulty, q_type)

                if not quiz:
                    st.error("🔥 JSON 생성 실패 (AI 응답 문제)")
                    return

                st.session_state.quiz = quiz
                st.session_state.answers = {}
                st.session_state.wrong = []

                st.success("✅ 생성 완료")

            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")

    # ==============================
    # 문제 풀이
    # ==============================
    if st.session_state.quiz:
        st.write("---")

        for i, q in enumerate(st.session_state.quiz):
            st.markdown(f"### Q{i+1}. {q['question']}")

            ans = st.radio(
                "정답 선택",
                q['options'],
                key=f"q{i}",
                index=None
            )

            st.session_state.answers[i] = ans

        # ==============================
        # 채점
        # ==============================
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

            st.session_state.wrong = wrong_list

            if score < 50:
                st.warning("👉 난이도 낮춰서 다시 추천")
            elif score > 80:
                st.success("👉 더 어려운 문제 도전 가능")

        # ==============================
        # 틀린 문제 재출제
        # ==============================
        if st.session_state.wrong:
            if st.button("🔥 틀린 문제 다시 풀기"):

                wrong_text = " ".join([q["question"] for q in st.session_state.wrong])

                with st.spinner("재출제 중..."):
                    try:
                        new_quiz = generate_quiz(
                            wrong_text,
                            len(st.session_state.wrong),
                            "어려움",
                            "함정"
                        )

                        if new_quiz:
                            st.session_state.quiz = new_quiz
                            st.success("재출제 완료!")

                    except Exception as e:
                        st.error(f"재출제 실패: {e}")
