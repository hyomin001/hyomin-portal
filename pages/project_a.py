import streamlit as st
import requests
import json
import re
import os
import time

# ==========================================
# 🔐 API KEY 불러오기
# ==========================================
GOOGLE_API_KEY = None

if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
elif os.getenv("GOOGLE_API_KEY"):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ API 키 없음")
    st.stop()

GOOGLE_API_KEY = GOOGLE_API_KEY.strip()

st.write("🔑 KEY CHECK:", GOOGLE_API_KEY[:10])
# ==========================================


# ==========================================
# 🔥 JSON 추출
# ==========================================
def extract_json(text):
    try:
        text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

        matches = re.findall(r'\[\s*{.*?}\s*\]', text, re.DOTALL)

        for match in matches:
            try:
                return json.loads(match)
            except:
                continue

        return None
    except:
        return None


# ==========================================
# 🔥 Gemini 호출 (Fallback + 재시도)
# ==========================================
def call_gemini(prompt):

    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash"
    ]

    headers = {"Content-Type": "application/json"}

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"

        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    st.info(f"🤖 사용 모델: {model}")
                    result = response.json()
                    return result['candidates'][0]['content']['parts'][0]['text']

                elif response.status_code == 503:
                    time.sleep(2)

                else:
                    break

            except:
                time.sleep(1)

    raise Exception("❌ 모든 모델 실패")


# ==========================================
# 메인 UI
# ==========================================
def render(market=None, nw=None):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("AI 문제 출제 + 채점 + 약점 분석")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

    # 🔥 세션 초기화 버튼
    if st.button("🧹 초기화"):
        st.session_state.clear()
        st.success("초기화 완료")
        st.stop()

    # ==============================
    # 입력
    # ==============================
    with st.expander("📚 학습 자료 입력", expanded=True):
        source_text = st.text_area("시험 범위 입력", height=250)

        c1, c2, c3 = st.columns(3)

        with c1:
            q_count = st.slider("문제 수", 3, 10, 5)
        with c2:
            difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움", "최악"])
        with c3:
            q_type = st.selectbox("출제 스타일", ["핵심 개념", "실전 응용", "함정 문제"])

    # ==============================
    # 문제 생성
    # ==============================
    if st.button("🚀 모의고사 시작", use_container_width=True):
        if not source_text.strip():
            st.warning("내용 입력하세요")
        else:
            with st.spinner("문제 생성 중..."):
                try:
                    prompt = f"""
다음 자료 기반으로 {q_count}개 객관식 문제 생성

난이도: {difficulty}
스타일: {q_type}

⚠️ 매우 중요:
- JSON 배열만 출력
- 설명 절대 금지
- ``` 사용 금지
- JSON 외 텍스트 포함 금지

[
  {{
    "question": "문제",
    "options": ["1번", "2번", "3번", "4번"],
    "answer": "정답 텍스트 그대로",
    "explanation": "해설"
  }}
]

자료:
{source_text[:10000]}
"""

                    quiz_json = None
                    response_text = None

                    # 🔥 JSON 실패 시 재요청
                    for _ in range(3):
                        response_text = call_gemini(prompt)
                        quiz_json = extract_json(response_text)

                        if quiz_json:
                            break

                    # ❌ 최종 실패
                    if not quiz_json:
                        st.error("🔥 JSON 깨짐 - 다시 시도하세요")
                        st.text_area("응답 확인", response_text, height=300)
                        st.stop()

                    st.session_state.quiz_data = quiz_json
                    st.session_state.user_answers = {}
                    st.session_state.ai_feedback = None

                    st.success("✅ 출제 완료!")

                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

    # ==============================
    # 문제 풀이
    # ==============================
    if st.session_state.quiz_data:
        st.write("---")

        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"### Q{i+1}. {q['question']}")

            user_choice = st.radio(
                "정답 선택",
                q['options'],
                key=f"q_{i}",
                index=None
            )

            st.session_state.user_answers[i] = user_choice

        # ==============================
        # 채점
        # ==============================
        if st.button("💯 채점하기", use_container_width=True):
            correct = 0
            analysis = []

            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = user_ans == q['answer']

                if is_correct:
                    correct += 1
                    st.success(f"{i+1}번 정답")
                else:
                    st.error(f"{i+1}번 오답 (정답: {q['answer']})")

                analysis.append({
                    "q": q['question'],
                    "is_correct": is_correct
                })

                with st.expander("해설"):
                    st.write(q['explanation'])

            score = int(correct / len(st.session_state.quiz_data) * 100)
            st.metric("점수", f"{score}점")

            # ==============================
            # AI 피드백
            # ==============================
            try:
                summary = "\n".join([
                    f"- {d['q']}: {'맞음' if d['is_correct'] else '틀림'}"
                    for d in analysis
                ])

                feedback_prompt = f"""
점수: {score}

결과:
{summary}

3줄 피드백:
1. 평가
2. 약점
3. 공부법
"""

                st.session_state.ai_feedback = call_gemini(feedback_prompt)

            except:
                st.session_state.ai_feedback = "피드백 생성 실패"

        if st.session_state.ai_feedback:
            st.info(st.session_state.ai_feedback)



