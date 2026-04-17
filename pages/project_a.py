import streamlit as st
import requests
import json
import re

# ==========================================
# 🔐 Streamlit Secrets에서 API KEY 불러오기
# ==========================================
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("❌ API 키가 설정되지 않았습니다. secrets.toml 확인하세요.")
    st.stop()
# ==========================================


def call_gemini_direct(prompt):
    # 🔥 최신 안정 모델
    model = "gemini-2.5-flash"

    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"API 오류 ({response.status_code}): {response.text}")

        result = response.json()

        return result['candidates'][0]['content']['parts'][0]['text']

    except Exception as e:
        raise Exception(f"Gemini 호출 실패: {e}")


def render(market=None, nw=None):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("자격증 & 시험 합격 정밀 케어")
    st.caption("AI가 문제 출제 + 채점 + 약점 분석까지 해드립니다.")

    # ==============================
    # 세션 초기화
    # ==============================
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

    # ==============================
    # 입력 UI
    # ==============================
    with st.expander("📚 학습 자료 입력", expanded=True):
        source_text = st.text_area(
            "시험 범위를 복붙하세요",
            height=250,
            placeholder="교과서, 요약본 등 입력"
        )

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
            st.warning("⚠️ 학습 내용을 입력하세요.")
        else:
            with st.spinner("문제 생성 중..."):
                try:
                    prompt = f"""
다음 자료 기반으로 {q_count}개 객관식 문제 생성

난이도: {difficulty}
스타일: {q_type}

반드시 JSON만 출력:

[
  {{
    "question": "문제",
    "options": ["1번", "2번", "3번", "4번"],
    "answer": "정답 텍스트 그대로",
    "explanation": "해설"
  }}
]

자료:
{source_text[:30000]}
"""

                    response_text = call_gemini_direct(prompt)

                    # 🔥 JSON 추출 안정화
                    json_match = re.search(r'\[\s*{.*}\s*\]', response_text, re.DOTALL)

                    if not json_match:
                        raise Exception("JSON 형식 추출 실패")

                    quiz_json = json.loads(json_match.group())

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
                is_correct = (user_ans == q['answer'])

                if is_correct:
                    correct += 1
                    st.success(f"{i+1}번 정답 ✅")
                else:
                    st.error(f"{i+1}번 오답 ❌ (정답: {q['answer']})")

                analysis.append({
                    "q": q['question'],
                    "is_correct": is_correct
                })

                with st.expander("📖 해설 보기"):
                    st.write(q['explanation'])

            score = int(correct / len(st.session_state.quiz_data) * 100)
            st.metric("🎯 점수", f"{score}점", f"{correct}/{len(st.session_state.quiz_data)}")

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
1. 전체 평가
2. 취약 개념
3. 공부 전략
"""

                st.session_state.ai_feedback = call_gemini_direct(feedback_prompt)

            except:
                st.session_state.ai_feedback = "피드백 생성 실패"

        # ==============================
        # 피드백 출력
        # ==============================
        if st.session_state.ai_feedback:
            st.info("👨‍🏫 합격 전략 가이드")
            st.write(st.session_state.ai_feedback)
