import streamlit as st
import requests
import json
import re

# ==========================================
# 🔑 [필독] 새로 발급받으신 API 키를 여기에 넣으세요!
# 보안을 위해 이전에 노출된 키는 구글 AI 스튜디오에서 삭제 후 새 키를 권장합니다.
# ==========================================
GOOGLE_API_KEY = "AIzaSyAfC4sXq5DXu9tkwbDDWKjlV_T8k6R83rg
"
# ==========================================

def call_gemini_direct(prompt):
    # 모델명을 gemini-1.5-flash로 수정하고 v1 엔드포인트를 사용합니다.
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"API 통신 오류 ({response.status_code}): {response.text}")
        
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']

def render(market, nw):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("자격증 & 시험 합격 정밀 케어")
    st.caption("복붙 한 번에 퀴즈 출제부터 약점 분석까지! 당신의 암기 메이트가 되어드립니다.")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

    with st.expander("📚 학습 자료 및 시험 설정", expanded=True):
        source_text = st.text_area("시험 범위를 복붙하세요 (교과서, 요약본 등)", height=250, 
                                 placeholder="여기에 입력된 내용을 바탕으로 AI가 문제를 창조합니다.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            q_count = st.slider("생성할 문제 수", 3, 10, 5)
        with c2:
            difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움", "최악"])
        with c3:
            q_type = st.selectbox("출제 스타일", ["핵심 개념 위주", "실전 응용 문제", "함정/지엽적 문제"])

    if st.button("🚀 AI 출제위원 소환 (모의고사 시작)", use_container_width=True):
        if not source_text.strip():
            st.warning("⚠️ 학습할 내용을 먼저 입력해주세요!")
        else:
            st.toast("📡 출제위원이 자료를 분석 중입니다...", icon="⏳")
            with st.spinner("👨‍🏫 일타강사가 시험 적중 예상 문제를 뽑아내고 있습니다..."):
                try:
                    prompt = f"""
                    다음 학습 자료를 바탕으로 {q_count}개의 객관식 문제를 만들어줘.
                    난이도는 '{difficulty}', 스타일은 '{q_type}'으로 설정해.
                    반드시 아래 JSON 형식으로만 응답해.

                    json_format:
                    [
                      {{
                        "question": "문제 내용",
                        "options": ["1번 선택지", "2번 선택지", "3번 선택지", "4번 선택지"],
                        "answer": "정답 번호 (예: 1번 선택지)",
                        "explanation": "이 문제가 왜 정답인지, 그리고 어떤 핵심 개념을 담고 있는지 상세히 설명"
                      }}
                    ]

                    자료:
                    {source_text[:50000]}
                    """
                    
                    response_text = call_gemini_direct(prompt)
                    json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                    
                    if json_match:
                        st.session_state.quiz_data = json.loads(json_match.group())
                        st.session_state.user_answers = {}
                        st.session_state.ai_feedback = None 
                        st.success("✅ 출제가 완료되었습니다! 문제를 풀어보세요.")
                    else:
                        st.error("AI가 형식을 지키지 않았습니다. 다시 시도해주세요.")
                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

    # 문제 풀이 및 정밀 분석
    if st.session_state.quiz_data:
        st.write("---")
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"#### Q{i+1}. {q['question']}")
            user_choice = st.radio(f"정답 선택 ({i+1}번)", q['options'], key=f"q_{i}", index=None)
            st.session_state.user_answers[i] = user_choice
            st.write("")

        if st.button("💯 채점 및 AI 약점 분석 리포트 보기", use_container_width=True):
            correct_count = 0
            analysis_data = []
            
            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = (user_ans == q['answer'])
                
                if is_correct:
                    correct_count += 1
                    st.success(f"Q{i+1}: 정답! ✨")
                else:
                    st.error(f"Q{i+1}: 오답 (선택: {user_ans if user_ans else '미선택'} / 정답: {q['answer']})")
                
                analysis_data.append({"q": q['question'], "is_correct": is_correct})
                with st.expander("📖 해설 및 핵심 포인트"):
                    st.write(q['explanation'])
            
            score = int((correct_count / len(st.session_state.quiz_data)) * 100)
            st.metric("최종 합격 점수", f"{score}점", f"{correct_count} / {len(st.session_state.quiz_data)}")

            # 🧠 AI 맞춤형 멘토링 생성
            with st.spinner("📊 일타강사가 당신의 취약 단원을 분석 중입니다..."):
                try:
                    summary = "\n".join([f"- {d['q']}: {'맞음' if d['is_correct'] else '틀림'}" for d in analysis_data])
                    feedback_prompt = f"""
                    사용자가 {score}점을 받았어. 아래는 문제별 결과야:
                    {summary}
                    
                    일타강사로서 다음 내용을 포함해 3~4문장으로 피드백해줘:
                    1. 전체적인 학습 상태 평가
                    2. 틀린 문제를 통해 본 '취약 개념' 지목
                    3. 앞으로의 암기 전략 조언 (마크다운 활용)
                    """
                    st.session_state.ai_feedback = call_gemini_direct(feedback_prompt)
                except:
                    st.session_state.ai_feedback = "분석 중 통신 지연이 발생했습니다. 오답 해설을 다시 읽어보세요!"

        if st.session_state.ai_feedback:
            st.info(f"👨‍🏫 **일타강사의 합격 전략 가이드**\n\n{st.session_state.ai_feedback}")
