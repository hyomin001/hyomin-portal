pages/project_a.py
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
# 🔥 Gemini 호출 (대기 시간 90초 및 5만 자 대응)
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
            "maxOutputTokens": 4096
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"

        for attempt in range(3):
            try:
                # 🚨 5만 자 읽을 시간을 주기 위해 타임아웃 90초로 연장
                res = requests.post(url, json=payload, timeout=90)

                if res.status_code == 200:
                    data = res.json()
                    try:
                        return data['candidates'][0]['content']['parts'][0]['text']
                    except:
                        return str(data)

                elif res.status_code in [429, 503]:
                    time.sleep((2 ** attempt) + 1)

            except requests.exceptions.Timeout:
                time.sleep(2)
            except Exception:
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
            "explanation": "AI 실패로 생성된 문제 (시스템 오류)"
        })
    return dummy

# ==========================================
# 🔥 문제 생성 (입력 글자수 최대 5만 자 지원)
# ==========================================
def generate_quiz(text, count, difficulty, q_type, status):

    prompt = f"""
무조건 JSON 배열 형식으로만 출력하세요. 마크다운(` ```json ` 등)이나 일반 텍스트는 절대 포함하지 마세요.
🚨 절대 규칙: 정답(answer)은 반드시 options 배열에 제공된 4개의 보기 중 하나와 100% 일치해야 합니다.

[
  {{
    "question": "문제",
    "options": ["1","2","3","4"],
    "answer": "정답",
    "explanation": "해설",
    "study_note": "👩‍🏫 1타 강사의 꿀팁, 함정 피하는 법 또는 암기법"
  }}
]

문제 수: {count}
난이도: {difficulty}
스타일: {q_type}

학습 내용:
{text[:50000]}  
"""
    # 🚨 50,000자까지 슬라이싱 확장 완료

    for attempt in range(5):
        status.update(label=f"⏳ AI 모의고사 출제 중... (시도 {attempt + 1}/5)", state="running")
        status.write(f"🤖 방대한 문서를 정독하고 있습니다... (글이 길면 최대 1분 이상 소요될 수 있습니다. 커피 한 모금 드세요!)")
        
        res = call_gemini(prompt)

        if not res:
            status.write(f"⚠️ {attempt + 1}차 시도 시간 초과. AI를 다시 재촉합니다.")
            continue

        status.write("🔍 AI 응답 완료! 데이터 형식(JSON) 검증 중...")
        quiz = extract_json(res)
        
        if validate_quiz(quiz):
            status.write("✅ 완벽한 JSON 데이터 확인 완료!")
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz

        status.write("🔧 형식이 조금 어긋났습니다. 자동 복구를 시도합니다...")
        quiz = repair_json(res)
        
        if validate_quiz(quiz):
            status.write("🛠️ 데이터 복구 성공!")
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz

        status.write(f"❌ {attempt + 1}차 시도 실패. 멱살 잡고 다시 출제시킵니다...")
        time.sleep(1)

    status.update(label="🚨 AI 출제 최종 실패 (기본 문제로 대체됩니다)", state="error")
    return fallback_quiz(count)

# ==========================================
# 🔥 텍스트 품질
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 200:
        return "❌ 너무 짧음 (문맥 파악 어려움)", 40
    elif l < 800:
        return "⚠️ 보통 (내용을 더 넣으면 좋습니다)", 70
    elif l < 50000:
        return "✅ 훌륭함 (완벽한 출제 가능)", 95
    else:
        return "🔥 방대함 (5만 자까지만 인식됩니다)", 90

# ==========================================
# 🎨 UI CSS 주입 함수
# ==========================================
def inject_custom_css():
    st.markdown("""
    <style>
    @import url('[https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap](https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap)');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif !important; }
    
    .quiz-card {
        background: linear-gradient(145deg, #ffffff, #f5f7fa);
        border-radius: 20px; padding: 30px; margin-bottom: 25px;
        box-shadow: 10px 10px 30px #e6e6e6, -10px -10px 30px #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.3s ease;
    }
    .quiz-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.08); }
    
    .quiz-card-correct {
        background: linear-gradient(135deg, #f0fff4 0%, #e6ffe6 100%);
        border: 2px solid #48bb78; box-shadow: 0 0 15px rgba(72, 187, 120, 0.3);
    }
    .quiz-card-wrong {
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
        border: 2px solid #f56565; box-shadow: 0 0 15px rgba(245, 101, 101, 0.3);
    }
    
    .study-note {
        background: linear-gradient(135deg, #fffcf0 0%, #fff3cd 100%);
        border-left: 6px solid #f59e0b; padding: 20px; margin-top: 20px;
        border-radius: 12px; color: #92400e; font-size: 1.05em; font-weight: 500;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.1); line-height: 1.6;
    }
    
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important; border: none !important; border-radius: 50px !important;
        padding: 12px 28px !important; font-weight: 700 !important; font-size: 1.1em !important;
        transition: all 0.3s ease !important; box-shadow: 0 8px 20px rgba(118, 75, 162, 0.4) !important;
    }
    div.stButton > button:first-child:hover {
        transform: scale(1.05) translateY(-2px) !important;
        box-shadow: 0 12px 25px rgba(118, 75, 162, 0.6) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 15px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa; border-radius: 10px 10px 0 0; padding: 10px 20px;
        border: 1px solid #e9ecef; border-bottom: none; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important; border-top: 3px solid #667eea !important;
        font-weight: 700 !important; color: #764ba2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 🎯 UI (렌더링)
# ==========================================
def render(market=None, nw=None):

    st.title("🔥 AI 모의고사 (Premium Edition)")

    # ==========================================
    # 📖 팀원들을 위한 사용 가이드 (Expander)
    # ==========================================
    with st.expander("💡 [필독] AI 모의고사 200% 활용 가이드 및 주의사항", expanded=False):
        st.markdown("""
        **환영합니다! 이 앱은 입력하신 문서/노트를 기반으로 똑똑하게 모의고사를 출제해주는 AI 도구입니다.**
        
        ✅ **최대 5만 자 지원 (책 한 챕터 분량):**
        단순한 키워드뿐만 아니라, 회의록, 프로젝트 정리 노트, 전공 서적 내용 등 긴 문서를 통째로 넣어도 모두 읽고 문제를 냅니다. 문맥이 구체적일수록 고퀄리티 문제가 탄생합니다.
        
        ⏳ **조금만 기다려주세요 (최대 1~2분 소요):**
        내용이 길고 난이도가 높을수록 AI가 정독하고 해설을 작성하는 데 시간이 걸립니다. 화면에 뜨는 상태창(Status)을 보며 AI가 작업을 마칠 때까지 인내심을 갖고 기다려주세요!
        
        🚨 **주의사항 및 에러 발생 시:**
        - 가끔 AI가 헷갈려서 형식(JSON)을 틀릴 때가 있습니다. (스스로 최대 5번까지 재도전합니다.)
        - 최종적으로 실패하면 '기본 문제(오류)'가 뜹니다. 이럴 땐 내용을 조금 줄이거나 정리해서 다시 시도해주세요.
        
        🔥 **오답은 복수전으로 완벽 마스터:**
        채점 후 [성적표] 탭 하단에서 **'하드코어 오답 복수전'** 버튼을 눌러보세요. 틀린 개념만 모아 AI 1타 강사가 지옥 난이도로 다시 훈련시켜 줍니다!
        """)

    # 상태 초기화
    ss = st.session_state

    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("last_quiz_text", "")

    # 초기화 버튼
    if st.button("🧹 전체 초기화"):
        st.session_state.clear()
        st.rerun()

    # 예쁜 CSS 적용
    inject_custom_css() 

    # 탭 구조 분할
    tab1, tab2, tab3 = st.tabs(["📝 출제 설정", "🎯 응시 화면", "📊 성적표 및 복습"])

    with tab1:
        # 입력
        text = st.text_area("📚 학습 내용 입력 (최대 5만 자까지 권장)", height=250, placeholder="여기에 공부한 노트, 회의록, 텍스트를 복사해서 붙여넣으세요!")
        st.caption(f"현재 글자 수: {len(text):,} 자 / 최대 인식 한도: 50,000 자")

        q, p = analyze_text_quality(text)
        st.info(f"텍스트 분석: {q} / 생성 성공 확률: {p}%")

        col1, col2, col3 = st.columns(3)
        count = col1.slider("출제 문항 수", 3, 20, 5) # 문항수도 약간 넉넉하게
        difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움", "최상(지옥)"])
        q_type = col3.selectbox("문제 스타일", ["개념 확인", "실무 응용", "함정 유발"])

        # 생성
        if st.button("🚀 AI 모의고사 출제 시작"):
            if not text.strip():
                st.warning("⚠️ 출제할 학습 내용을 먼저 입력해주세요.")
            else:
                with st.status("🚀 AI 엔진 가동 중...", expanded=True) as status:
                    quiz = generate_quiz(text, count, difficulty, q_type, status)

                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.last_quiz_text = text
                
                st.toast("🚀 출제 완료! [응시 화면] 탭으로 이동해서 문제를 풀어보세요.", icon="✅")

    # 문제 로직 (Tab 2)
    if ss.quiz:
        total = len(ss.quiz) if ss.quiz else 0
        answered = len([v for v in ss.answers.values() if v])
        prog = max(0.0, min(1.0, answered / total)) if total > 0 else 0.0

        with tab2:
            st.progress(prog, text=f"진행률: {answered} / {total} 문항")

            for i, q in enumerate(ss.quiz):
                st.markdown('<div class="quiz-card">', unsafe_allow_html=True) 
                st.markdown(f"### Q{i+1}. {q.get('question','문제 오류')}")

                options = q.get("options", ["1","2","3","4"])
                ans = st.radio("선택", ["선택 안함"] + options, key=f"q_{i}")

                if ans != "선택 안함":
                    if ss.answers.get(i) != ans: 
                        st.toast(f"{i+1}번 마킹 완료!", icon="✏️")
                    ss.answers[i] = ans
                
                st.markdown('</div>', unsafe_allow_html=True) 

        # 성적표 로직 (Tab 3)
        with tab3:
            if st.button("💯 OMR 제출 및 채점하기"):
                correct = 0
                wrong = []

                with st.spinner("📊 제출하신 답안을 채점하고 있습니다..."):
                    time.sleep(1) 

                    for i, q in enumerate(ss.quiz):
                        user = ss.answers.get(i)
                        answer = q.get("answer")
                        is_wrong = (user != answer)

                        card_class = "quiz-card-wrong" if is_wrong else "quiz-card-correct"
                        st.markdown(f'<div class="quiz-card {card_class}">', unsafe_allow_html=True)
                        
                        if is_wrong:
                            wrong.append(q)
                            st.error(f"🔴 Q{i+1}. 오답입니다. (내 답: {user} / 정답: {answer})")
                        else:
                            correct += 1
                            st.success(f"🟢 Q{i+1}. 정답입니다!")
                            
                        st.markdown(f"**문제:** {q.get('question','')}")
                        
                        with st.expander(f"📖 {i+1}번 해설 및 1타 강사의 꿀팁 보기", expanded=is_wrong):
                            st.write(f"**해설:** {q.get('explanation','없음')}")
                            if "study_note" in q and q["study_note"]:
                                st.markdown(f'<div class="study-note">👨‍🏫 <b>1타 강사 Note:</b><br>{q.get("study_note")}</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)

                    score = int(correct / total * 100) if total > 0 else 0
                    st.metric("최종 점수", f"{score} 점")
                    
                    if score == 100:
                        st.balloons()
                        st.toast("완벽합니다! 100점 만점! 🎉", icon="🏆")
                    elif score >= 70:
                        st.toast("수고하셨습니다! 훌륭한 점수네요. 👍", icon="🌟")
                    else:
                        st.toast("조금만 더 복습해볼까요? 오답 노트를 꼭 확인하세요! 💪", icon="🔥")

                    ss.history.append(score)
                    ss.wrong = wrong

            if ss.history:
                avg = int(sum(ss.history)/len(ss.history))
                st.metric("나의 누적 평균 점수", f"{avg} 점")

            if ss.wrong:
                st.markdown("---")
                st.subheader("🔥 1타 강사 오답 밀착 마크 (하드코어 복수전)")
                st.caption("틀린 문제의 개념과 해설을 모아 가장 어려운 난이도로 재출제합니다.")
                
                if st.button("🚨 틀린 내용으로만 지옥 난이도 재도전"):
                    with st.status("🔥 오답의 뼈대를 분석하여 지옥 난이도로 재출제 중...", expanded=True) as status:
                        txt = " ".join([q.get("question","") + " " + q.get("study_note", "") + " " + q.get("explanation", "") for q in ss.wrong])

                        ss.quiz = generate_quiz(
                            txt,
                            len(ss.wrong),
                            "최상(지옥)",
                            "함정 유발",
                            status 
                        )
                        ss.answers = {}
                        ss.wrong = []
                    
                    st.rerun()
