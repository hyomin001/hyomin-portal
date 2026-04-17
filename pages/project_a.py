import streamlit as st
import requests
import json
import re

# ==========================================
# 🔑 [필독] 새로 발급받으신 API 키를 유지해주세요!
# ==========================================
GOOGLE_API_KEY = "AIzaSyAfC4sXq5DXu9tkwbDDWKjlV_T8k6R83rg"
# ==========================================

def call_gemini_direct(prompt):
    """google-generativeai 패키지 없이 직접 API와 통신하는 다이렉트 함수"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7}
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API 통신 오류 ({response.status_code}): {response.text}")
        
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def render(market, nw):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("자격증 & 시험 맞춤형 무한 모의고사")
    st.caption("복붙 한 번에 퀴즈가 와르르! 출제부터 성적 분석, 약점 보완 피드백까지 완벽하게 케어합니다.")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

    with st.expander("📚 학습 자료 및 출제 설정 (시험 범위 챕터를 통째로 복붙하세요!)", expanded=True):
        source_text = st.text_area("학습할 내용을 붙여넣으세요.", height=250, 
                                 placeholder="교과서 내용, 요약본, 자격증 기출 이론 등 무엇이든 좋습니다. (최대 5만 자 제한)")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            q_count = st.slider("생성할 문제 수", 3, 10, 5)
        with c2:
            difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움", "최악"])
        with c3:
            q_type = st.selectbox("출제 스타일", ["단순 개념 암기", "실전 상황 응용", "헷갈리는 함정 위주"])

    if st.button("🚀 AI 모의고사 출제 시작", use_container_width=True):
        if not source_text.strip():
            st.warning("⚠️ 학습할 내용을 먼저 입력해주세요!")
        elif GOOGLE_API_KEY == "여기에_새로_발급받은_키를_넣으세요" or not GOOGLE_API_KEY.startswith("AIza"):
            st.error("⚠️ API 키가 올바르게 입력되지 않았습니다. 코드를 다시 확인해주세요.")
        else:
            st.toast("📡 일타강사 모드 가동 중...", icon="⏳")
            with st.spinner("👨‍🏫 방대한 자료를 분석하여 맞춤형 문제를 출제하고 있습니다... (약 10~20초 소요)"):
                try:
                    prompt = f"""
                    다음 제공된 학습 자료를 바탕으로 {q_count}개의 객관식 문제를 만들어줘.
                    난이도는 '{difficulty}'로, 출제 스타일은 '{q_type}'에 맞춰서 내줘.
                    응답은 반드시 아래와 같은 JSON 형식으로만 보내줘. 다른 설명은 절대 하지 마.

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
                    {source_text[:50000]}
                    """
                    
                    response_text = call_gemini_direct(prompt)
                    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                    
                    if json_match:
                        st.session_state.quiz_data = json.loads(json_match.group())
                        st.session_state.user_answers = {}
                        st.session_state.ai_feedback = None # 새 퀴즈 시 피드백 초기화
                        st.success(f"✅ 출제 완료! 총 {len(st.session_state.quiz_data)}문제가 준비되었습니다.")
                    else:
                        st.error("AI 응답 형식 오류. 다시 시도해주세요.")
                        
                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

    # ==========================================
    # 📝 문제 풀이 및 멘토링 피드백 섹션
    # ==========================================
    if st.session_state.quiz_data:
        st.write("---")
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"#### Q{i+1}. {q['question']}")
            user_choice = st.radio(f"답안 선택 ({i+1}번)", q['options'], key=f"q_{i}", index=None)
            st.session_state.user_answers[i] = user_choice
            st.write("")

        if st.button("💯 채점 및 일타강사 분석 받기", use_container_width=True):
            correct_count = 0
            result_summary_for_ai = "" # AI 피드백을 위한 결과 요약 텍스트
            
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = (user_ans == q['answer'])
                
                if is_correct:
                    correct_count += 1
                    st.success(f"Q{i+1}: 정답입니다! 🎉")
                    result_summary_for_ai += f"Q{i+1}: 맞춤 (주제: {q['question']})\n"
                else:
                    display_ans = user_ans if user_ans else "미선택"
                    st.error(f"Q{i+1}: 오답입니다. (제출한 답: {display_ans} / 정답: {q['answer']})")
                    result_summary_for_ai += f"Q{i+1}: 틀림 (주제: {q['question']})\n"
                
                with st.expander("💡 해설 보기"):
                    st.write(q['explanation'])
            
            score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            if score == 100:
                st.balloons()
            st.metric("최종 점수", f"{score}점", f"{correct_count} / {len(st.session_state.quiz_data)}")

            # 🧠 AI 학습 코멘트 생성
            with st.spinner("📊 제출하신 답안을 바탕으로 일타강사가 취약점을 분석하고 있습니다..."):
                try:
                    feedback_prompt = f"""
                    사용자가 방금 시험을 치렀고, 총 {len(st.session_state.quiz_data)}문제 중 {correct_count}문제를 맞혔어. 점수는 {score}점이야.
                    아래는 각 문제의 주제와 사용자의 정답 여부야:
                    {result_summary_for_ai}
                    
                    너는 친절하고 명쾌한 일타강사야. 이 결과를 바탕으로 사용자에게 학습 조언(피드백)을 3~4문장으로 해줘.
                    사용자가 틀린 문제들의 주제를 파악해서, 어떤 개념을 더 복습해야 할지 구체적으로 짚어줘.
                    마크다운을 활용해서 가독성 좋고 동기부여가 되는 따뜻하면서도 예리한 멘트를 작성해.
                    """
                    st.session_state.ai_feedback = call_gemini_direct(feedback_prompt)
                except Exception as e:
                    st.session_state.ai_feedback = "피드백 생성 중 통신 지연이 발생했습니다. 오답 노트 위주로 복습해주세요!"

        # AI 피드백 결과 화면에 예쁘게 출력
        if st.session_state.ai_feedback:
            st.markdown("""
            <div style="background: rgba(37, 99, 235, 0.05); border-left: 5px solid #2563EB; padding: 20px; border-radius: 8px; margin-top: 20px;">
                <h3 style="color: #2563EB; margin-top: 0;">👨‍🏫 일타강사 제미나이의 성적 분석 리포트</h3>
                <div style="color: #333; line-height: 1.6;">
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.ai_feedback)
            st.markdown("</div></div>", unsafe_allow_html=True)
