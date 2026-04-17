import streamlit as st
import requests
import json
import re
import os
import time
from datetime import datetime

# ==========================================
# 🔐 API KEY 불러오기 (스트림릿 Secrets 자동 연동)
# ==========================================
GOOGLE_API_KEY = None

if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
elif os.getenv("GOOGLE_API_KEY"):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ API 키가 설정되지 않았습니다. Streamlit Secrets를 확인해주세요!")
    st.stop()

GOOGLE_API_KEY = GOOGLE_API_KEY.strip()

# ==========================================
# 🔥 JSON 추출 (강력한 정규식 & 파싱 로직)
# ==========================================
def extract_json(text):
    try:
        # 1. 쓸데없는 마크다운 찌꺼기 완벽 제거
        text = text.replace("```json", "").replace("```", "").strip()
        
        # 2. 처음 시작하는 '[' 와 마지막에 끝나는 ']' 사이만 추출
        start_idx = text.find('[')
        end_idx = text.rfind(']')
        
        if start_idx != -1 and end_idx != -1:
            clean_json = text[start_idx:end_idx+1]
            return json.loads(clean_json)
            
        # 3. 최후의 보루
        return json.loads(text)
    except:
        return None

# ==========================================
# 🔥 Gemini 호출 (JSON 강제 모드 & 토큰 용량 2배 상향)
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
            "maxOutputTokens": 8192, # 👈 토큰 제한을 8192로 대폭 상향하여 글자 짤림 방지!
            "responseMimeType": "application/json" # 무조건 JSON 형태로만 대답하도록 강제
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    return result['candidates'][0]['content']['parts'][0]['text']
                elif response.status_code == 503:
                    time.sleep(2)
                else:
                    break
            except:
                time.sleep(1)
    raise Exception("❌ 모든 모델 호출 실패")

# ==========================================
# 메인 UI
# ==========================================
def render(market=None, nw=None):
    st.title("👨‍🏫 일타강사 제미나이")
    st.subheader("비밀 프로젝트 A: AI 무한 모의고사 + 오답노트")

    if "quiz_data" not in st.session_state:
        st.session_state.quiz_data = None
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = {}
    if "ai_feedback" not in st.session_state:
        st.session_state.ai_feedback = None

    # 🔥 세션 초기화 버튼
    c_title1, c_title2 = st.columns([8, 2])
    with c_title2:
        if st.button("🧹 화면 초기화", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    # ==============================
    # 1. 자료 입력 (파일 업로드)
    # ==============================
    with st.expander("📚 학습 자료 입력 (파일 업로드 지원_최대 5만자)", expanded=True):
        uploaded_file = st.file_uploader("📄 문서 파일 업로드 (선택사항)", type=['txt', 'pdf'])
        file_text = ""
        
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.txt'):
                file_text = uploaded_file.read().decode('utf-8')
            elif uploaded_file.name.endswith('.pdf'):
                try:
                    import PyPDF2
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    for page in pdf_reader.pages:
                        extracted = page.extract_text()
                        if extracted: file_text += extracted + "\n"
                except ImportError:
                    st.error("⚠️ PDF 기능을 쓰려면 requirements.txt에 PyPDF2 를 추가해주세요!")
        
        source_text = st.text_area("시험 범위 직접 입력 (파일을 올리면 자동 채워짐)", value=file_text, height=200)

        st.write("---")
        c1, c2, c3 = st.columns(3)
        with c1: q_count = st.slider("문제 수", 3, 10, 5)
        with c2: difficulty = st.selectbox("난이도", ["쉬움", "보통", "어려움", "최악 (함정 다수)"])
        with c3: q_type = st.selectbox("출제 스타일", ["핵심 개념 위주", "실전 응용 위주", "기출 변형 스타일"])

    # ==============================
    # 2. 문제 생성
    # ==============================
    if st.button("🚀 나만의 모의고사 출제하기", type="primary", use_container_width=True):
        if not source_text.strip():
            st.warning("⚠️ 내용을 먼저 입력하거나 파일을 업로드하세요!")
        else:
            with st.spinner("AI가 방대한 자료를 분석하여 영혼을 갈아 문제를 출제 중입니다... (약 10~20초 소요)"):
                try:
                    # 👈 프롬프트에 간결함 요구 조건 추가
                    prompt = f"""
                    다음 자료 기반으로 {q_count}개 객관식 문제 생성

                    난이도: {difficulty}
                    스타일: {q_type}

                    ⚠️ 매우 중요:
                    - JSON 배열만 출력
                    - 설명 절대 금지
                    - JSON 외 텍스트 포함 금지
                    - 선택지와 해설은 너무 길지 않게 핵심만 간결하게 작성할 것

                    [
                      {{
                        "question": "문제",
                        "options": ["1번", "2번", "3번", "4번"],
                        "answer": "정답 텍스트 그대로",
                        "explanation": "해설"
                      }}
                    ]

                    자료:
                    {source_text[:20000]}
                    """
                    quiz_json = None
                    response_text = None
                    
                    for _ in range(3):
                        response_text = call_gemini(prompt)
                        quiz_json = extract_json(response_text)
                        if quiz_json: break

                    if not quiz_json:
                        st.error("🔥 AI 응답 오류 - 잠시 후 다시 시도해주세요.")
                        with st.expander("에러 난 원본 응답 보기"):
                            st.write(response_text)
                        st.stop()

                    st.session_state.quiz_data = quiz_json
                    st.session_state.user_answers = {}
                    st.session_state.ai_feedback = None
                    st.success("✅ 출제 완료! 아래에서 문제를 풀어보세요.")
                except Exception as e:
                    st.error(f"❌ 오류 발생: {e}")

    # ==============================
    # 3. 문제 풀이 및 다운로드
    # ==============================
    if st.session_state.quiz_data:
        st.write("---")
        
        quiz_txt = f"🎓 효민 AI 아카데미 - 모의고사 ({datetime.now().strftime('%Y-%m-%d')})\n"
        quiz_txt += f"난이도: {difficulty} | 스타일: {q_type}\n{'='*40}\n\n"
        for i, q in enumerate(st.session_state.quiz_data):
            quiz_txt += f"Q{i+1}. {q['question']}\n"
            for idx, opt in enumerate(q['options']):
                quiz_txt += f"  {idx+1}) {opt}\n"
            quiz_txt += "\n"
            
        st.download_button("📥 빈 시험지 다운로드 (오프라인 인쇄용)", quiz_txt, file_name="hyomin_mock_exam.txt", use_container_width=True)
        st.write("")

        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"### Q{i+1}. {q['question']}")
            user_choice = st.radio("정답 선택", q['options'], key=f"q_{i}", index=None)
            st.session_state.user_answers[i] = user_choice

        st.write("---")
        
        # ==============================
        # 4. 채점 및 오답노트
        # ==============================
        if st.button("💯 답안지 제출 및 채점하기", type="primary", use_container_width=True):
            correct = 0
            analysis = []
            wrong_notes = []

            for i, q in enumerate(st.session_state.quiz_data):
                user_ans = st.session_state.user_answers.get(i)
                is_correct = user_ans == q['answer']

                if is_correct:
                    correct += 1
                    st.success(f"**Q{i+1}. 정답입니다!**")
                else:
                    user_ans_text = user_ans if user_ans else "선택 안 함"
                    st.error(f"**Q{i+1}. 오답입니다.** (내 답: {user_ans_text} ➔ 정답: {q['answer']})")
                    wrong_notes.append({
                        "q_num": i+1, "question": q['question'], 
                        "my_ans": user_ans_text, "real_ans": q['answer'], "exp": q['explanation']
                    })

                analysis.append({"q": q['question'], "is_correct": is_correct})
                with st.expander("💡 해설 보기"):
                    st.write(q['explanation'])

            score = int((correct / len(st.session_state.quiz_data)) * 100)
            st.metric("🎯 최종 점수", f"{score}점")
            
            if score == 100: st.balloons()

            if wrong_notes:
                st.write("---")
                st.markdown("### 📓 나만의 오답 노트")
                for w in wrong_notes:
                    st.markdown(f"""
                    <div style='background:rgba(255, 75, 75, 0.1); border-left: 4px solid #FF4B4B; padding:15px; margin-bottom:10px; border-radius:8px;'>
                        <b>Q{w['q_num']}. {w['question']}</b><br>
                        <span style='color:#FF4B4B;'>❌ 내 답: {w['my_ans']}</span> | <span style='color:#00E5FF;'>✅ 정답: {w['real_ans']}</span><br>
                        <hr style='margin: 8px 0; border-color: rgba(255,255,255,0.1);'>
                        <span style='color:#E2E8F0; font-size: 0.9rem;'>{w['exp']}</span>
                    </div>
                    """, unsafe_allow_html=True)

            try:
                summary = "\n".join([f"- {d['q']}: {'맞음' if d['is_correct'] else '틀림'}" for d in analysis])
                feedback_prompt = f"점수: {score}\n결과:\n{summary}\n\n3줄 피드백:\n1. 종합 평가\n2. 취약점 분석\n3. 추천 공부법"
                st.session_state.ai_feedback = call_gemini(feedback_prompt)
            except:
                st.session_state.ai_feedback = "피드백 생성에 실패했습니다."

            if st.session_state.ai_feedback:
                st.info(st.session_state.ai_feedback)
