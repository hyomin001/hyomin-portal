import streamlit as st
import google.generativeai as genai
import json
import re
import time

# ==========================================
# 🔑 [필독] 구글 API 키 설정 구역
# 보안을 위해 반드시 새로 발급받은 키를 넣어주세요!
# ==========================================
GOOGLE_API_KEY = "AIzaSyAfC4sXq5DXu9tkwbDDWKjlV_T8k6R83rg" 
# ==========================================

# AI 모델 설정 (404 에러 해결을 위해 -latest 추가)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def render(market, nw):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("비밀 프로젝트 A: 맞춤형 무한 모의고사")
    st.caption("복붙 한 번에 퀴즈가 와르르! AI가 출제위원에 빙의하여 실전 훈련을 돕습니다.")

    # 세션 상태 초기화
    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}

    # 1. 자료 입력 섹션
    with st.expander("📚 학습 자료 입력 (시험 범위 챕터를 통째로 복붙하세요!)", expanded=True):
        source_text = st.text_area("학습할 내용을 붙여넣으세요.", height=300, 
                                 placeholder="교과서 내용, 요약본, 자격증 기출 이론 등 무엇이든 좋습니다. (최대 5만 자 제한)")
        
        col1, col2 = st.columns(2)
        with col1:
            q_count = st.slider("생성할 문제 수", 3, 10, 5)
        with col2:
            difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움", "최악"])

    if st.button("🚀 AI 문제 출제 시작", use_container_width=True):
        if not source_text.strip():
            st.warning("⚠️ 학습할 내용을 먼저 입력해주세요!")
        else:
            # ⏳ 로딩창 시작
            st.toast("📡 제미나이 서버와 연결 중...", icon="⏳")
            with st.spinner("👨‍🏫 일타강사가 방대한 자료를 분석하여 함정 문제를 파는 중입니다... (약 10~20초 소요)"):
                try:
                    # AI에게 줄 프롬프트 (JSON 형식을 강제하여 파싱하기 쉽게 함)
                    prompt = f"""
                    다음 제공된 학습 자료를 바탕으로 {q_count}개의 객관식 문제를 만들어줘.
                    난이도는 '{difficulty}'로 설정해줘.
                    응답은 반드시 아래와 같은 JSON 형식으로만 보내줘. 다른 설명은 하지 마.

                    json_format:
                    [
                      {{
                        "question": "문제 내용",
                        "options": ["1번 선택지", "2번 선택지", "3번 선택지", "4번 선택지"],
                        "answer": "정답 번호 (예: 1번 선택지)",
                        "explanation": "해설 내용"
                      }}
                    ]

                    학습 자료:
                    {source_text[:50000]}  # 안전을 위해 5만자 단위로 끊음
                    """
                    
                    response = model.generate_content(prompt)
                    # JSON 부분만 추출
                    json_match = re.search(r'\[.*\]', response.text, re.DOTALL)
                    if json_match:
                        st.session_state.quiz_data = json.loads(json_match.group())
                        st.session_state.user_answers = {}
                        st.success(f"✅ 출제 완료! 총 {len(st.session_state.quiz_data)}문제가 준비되었습니다.")
                    else:
                        st.error("AI 응답 형식 오류. 다시 시도해주세요.")
                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

    # 2. 문제 풀이 섹션
    if st.session_state.quiz_data:
        st.write("---")
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"#### Q{i+1}. {q['question']}")
            # index=None을 추가하여 기본으로 1번이 선택되어 있는 현상 방지
            user_choice = st.radio(f"답안 선택 ({i+1}번)", q['options'], key=f"q_{i}", index=None)
            st.session_state.user_answers[i] = user_choice
            st.write("")

        if st.button("📝 채점 및 해설 보기", use_container_width=True):
            correct_count = 0
            for i, q in enumerate(st.session_state.quiz_data):
                is_correct = (st.session_state.user_answers.get(i) == q['answer'])
                if is_correct:
                    correct_count += 1
                    st.success(f"Q{i+1}: 정답입니다! 🎉")
                else:
                    user_ans = st.session_state.user_answers.get(i)
                    display_ans = user_ans if user_ans else "미선택"
                    st.error(f"Q{i+1}: 오답입니다. (제출한 답: {display_ans} / 정답: {q['answer']})")
                
                with st.expander("💡 해설 보기"):
                    st.write(q['explanation'])
            
            score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            if score == 100:
                st.balloons()
            st.metric("최종 점수", f"{score}점", f"{correct_count} / {len(st.session_state.quiz_data)}")
