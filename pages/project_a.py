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
# 🔥 JSON 파싱 (더 독하게)
# ==========================================
def extract_json(text):
    try:
        # JSON 강제 모드를 써도 가끔 마크다운을 붙이는 경우 제거
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return json.loads(text) # 정규식 실패시 통짜 파싱 시도
    except:
        return None

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

def validate_quiz(quiz):
    if not isinstance(quiz, list) or len(quiz) == 0:
        return False
    for q in quiz:
        if not isinstance(q, dict):
            return False
        # 필수 키워드가 하나라도 없으면 실패 처리
        if not all(k in q for k in ["question", "options", "answer", "explanation", "study_note"]):
            return False
        if len(q.get("options", [])) < 2:
            return False
    return True

# ==========================================
# 🔥 좀비 Gemini 호출 (JSON 강제화 적용)
# ==========================================
def call_gemini(prompt):
    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-2.5-flash-lite"
    ]

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2, # 온도를 낮춰서 창의성보단 정확성(JSON 양식) 강제
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json" # 🔥 핵심: 구글 API단에서 JSON만 뱉도록 강제
        }
    }

    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
        
        # 모델당 3번씩 끈질기게 요청
        for attempt in range(3):
            try:
                res = requests.post(url, json=payload, timeout=15)
                if res.status_code == 200:
                    data = res.json()
                    try:
                        return data['candidates'][0]['content']['parts'][0]['text']
                    except:
                        pass
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
            "question": f"시스템 점검 중입니다. 기본 문제 {i+1}",
            "options": ["1", "2", "3", "4"],
            "answer": ans,
            "explanation": "현재 AI 서버가 일시적으로 혼잡하여 자동 생성된 임시 문제입니다.",
            "study_note": "💡 우측 하단의 [초기화] 또는 새로고침 후 다시 시도해주세요."
        })
    return dummy

# ==========================================
# 🔥 문제 생성 (독한 Retry 늪 + 방탄 프롬프트)
# ==========================================
def generate_quiz(text, count, difficulty, q_type):
    prompt = f"""너는 대한민국 최고 수준의 시험 출제 위원이자 1타 강사다.
사용자가 제공한 자료를 바탕으로 고품질 객관식 문제를 출제하라.

# 🚨 절대 규칙 (위반 시 시스템 치명적 오류 발생)
1. 오직 JSON 배열만 출력한다.
2. 마크다운 코드블럭(```json 등), 인사말, 부연 설명은 절대 금지한다. 반드시 '['로 시작해서 ']'로 끝나야 한다.

# 📦 출력 형식 (고정)
[
  {{
    "question": "명확하고 논란의 여지가 없는 문제 내용",
    "options": ["매력적인 오답 1", "정답 텍스트", "매력적인 오답 2", "매력적인 오답 3"],
    "answer": "정답 (반드시 options 배열에 있는 텍스트 중 하나와 100% 일치해야 함)",
    "explanation": "왜 정답이고, 다른 보기는 왜 오답인지 논리적이고 명확한 해설",
    "study_note": "💡 [1타 강사 요약] 해당 개념의 핵심 암기법, 주의할 함정, 또는 심화 출제 포인트"
  }}
]

# 🎯 출제 조건
- 출제 문항 수: {count}
- 체감 난이도: {difficulty}
- 출제 스타일: {q_type}

# 🧠 출제 품질 및 검수 기준
- [매력적인 오답] 단순 텍스트 찾기로 풀 수 있는 문제는 배제하고, 지문을 정확히 이해해야만 풀 수 있도록 헷갈리게 구성한다.
- [정답 랜덤화] 정답이 항상 같은 번호에 위치하지 않도록, options 배열 내 정답의 위치를 완벽하게 섞는다.
- [학습 노트] 'study_note'는 학생이 오답을 복습할 때 뇌리에 박힐 수 있도록 친절하고 임팩트 있게 작성한다.

# 📚 학습 자료
{text[:3000]}
"""

    progress_text = "🧠 1타 강사 AI가 지문을 분석하여 문제를 출제 중입니다..."
    my_bar = st.progress(0, text=progress_text)
    
    # 5번의 큰 사이클 (실패시 계속 재도전)
    for i in range(5):
        my_bar.progress((i + 1) * 20, text=f"고품질 문제 생성 중... (시도 {i+1}/5)")
        
        res = call_gemini(prompt)
        if not res:
            continue

        quiz = extract_json(res)
        if validate_quiz(quiz):
            my_bar.empty()
            return quiz

        quiz = repair_json(res)
        if validate_quiz(quiz):
            my_bar.empty()
            return quiz
            
        time.sleep(1)

    my_bar.empty()
    st.error("⚠️ AI 서버가 극도로 혼잡하여 임시 문제로 대체됩니다.")
    return fallback_quiz(count)

# ==========================================
# 🔥 텍스트 품질
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 150: return "❌ 텍스트가 너무 짧습니다.", 30
    elif l < 500: return "⚠️ 무난한 품질의 문제가 나옵니다.", 60
    else: return "✅ 고품질의 모의고사가 기대됩니다!", 100

# ==========================================
# 🎯 UI (고퀄리티 CSS 주입 + 기존 인자 유지)
# ==========================================
def render(market=None, nw=None):

    # 🎨 환골탈태 커스텀 CSS 주입
    st.markdown("""
        <style>
        /* 탭 디자인 고급화 */
        .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #f7f9fc; padding: 10px; border-radius: 12px; }
        .stTabs [data-baseweb="tab"] { height: 45px; border-radius: 8px; padding: 0 20px; font-weight: 600; color: #4b5563; }
        .stTabs [aria-selected="true"] { background-color: #ffffff !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05); color: #2563eb !important; }
        
        /* 카드형 컨테이너 */
        .quiz-card { background-color: #ffffff; padding: 25px; border-radius: 16px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 20px; }
        
        /* 정답/오답 박스 스타일 */
        .correct-box { background-color: #f0fdf4; border-left: 6px solid #22c55e; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .wrong-box { background-color: #fef2f2; border-left: 6px solid #ef4444; padding: 15px; border-radius: 8px; margin-top: 15px; }
        .study-note { background-color: #eff6ff; border: 1px solid #bfdbfe; padding: 15px; border-radius: 8px; margin-top: 10px; }
        
        /* 제목 스타일 */
        .main-title { font-size: 2.2rem; font-weight: 800; color: #1e3a8a; margin-bottom: 0px; }
        .sub-title { font-size: 1.1rem; color: #6b7280; margin-bottom: 30px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-title">🔥 AI 스마트 튜터 모의고사</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">텍스트를 입력하면 대한민국 1타 출제 위원 AI가 맞춤형 문제와 요약 노트를 생성합니다.</p>', unsafe_allow_html=True)

    ss = st.session_state
    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("is_graded", False)

    tab1, tab2, tab3 = st.tabs(["📚 1. 출제 설정", "📝 2. 응시 화면", "📖 3. 성적표 & 1타 노트"])

    # ------------------------------------------
    # [TAB 1] 출제 설정
    # ------------------------------------------
    with tab1:
        st.markdown("#### 📄 학습 데이터 입력")
        text = st.text_area("교재 내용, 위키백과, 기사 등을 붙여넣으세요.", height=200, label_visibility="collapsed", placeholder="이곳에 공부할 텍스트를 입력하세요...")
        
        if text:
            msg, prog = analyze_text_quality(text)
            st.progress(prog / 100, text=f"입력 분량: {len(text)}자 ({msg})")

        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown("#### ⚙️ 출제 옵션")
            c1, c2, c3 = st.columns(3)
            count = c1.slider("📌 문제 수", 3, 15, 5)
            difficulty = c2.selectbox("💪 난이도", ["쉬움", "보통", "어려움", "최상"])
            q_type = c3.selectbox("🎯 스타일", ["개념 확인", "수능형 응용", "함정 주의"])

        if st.button("🚀 나만의 모의고사 출제하기", type="primary", use_container_width=True):
            if len(text.strip()) < 50:
                st.error("❌ 텍스트가 너무 짧습니다. 최소 50자 이상 입력해주세요.")
            else:
                ss.quiz = generate_quiz(text, count, difficulty, q_type)
                ss.answers = {}
                ss.wrong = []
                ss.is_graded = False
                st.toast("🎉 생성 완료! [2. 응시 화면]으로 넘어갑니다.", icon="✅")
                st.rerun()

    # ------------------------------------------
    # [TAB 2] 응시 화면
    # ------------------------------------------
    with tab2:
        if not ss.quiz:
            st.info("👈 [1. 출제 설정] 탭에서 텍스트를 넣고 문제를 만들어주세요.")
        else:
            total = len(ss.quiz)
            answered = len([v for v in ss.answers.values() if v and v != "선택 안함"])

            st.progress(answered / total if total > 0 else 0, text=f"🎯 마킹 진행률: {answered} / {total} 문제 완료")
            st.divider()

            for i, q in enumerate(ss.quiz):
                st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
                st.markdown(f"### **Q{i+1}.** {q.get('question')}")
                
                options = q.get("options", ["1", "2", "3", "4"])
                ans = st.radio(
                    "선택", ["선택 안함"] + options,
                    key=f"q_{i}", label_visibility="collapsed", disabled=ss.is_graded
                )
                if ans != "선택 안함": ss.answers[i] = ans
                st.markdown('</div>', unsafe_allow_html=True)

            if not ss.is_graded:
                if st.button("💯 OMR 답안지 제출 및 채점", type="primary", use_container_width=True):
                    if answered < total:
                        st.warning("⚠️ 아직 풀지 않은 문제가 있습니다!")
                    else:
                        correct = 0
                        wrong = []
                        for i, q in enumerate(ss.quiz):
                            if ss.answers.get(i) == q.get("answer"): correct += 1
                            else: wrong.append(q)

                        score = int((correct / total) * 100) if total > 0 else 0
                        ss.history.append(score)
                        ss.wrong = wrong
                        ss.is_graded = True
                        if score == 100: st.balloons()
                        st.toast("채점이 완료되었습니다! [3. 성적표] 탭을 확인하세요.", icon="🎓")
                        st.rerun()
            else:
                st.success("✅ 이미 채점된 시험지입니다. 3번 탭을 확인하세요.")

    # ------------------------------------------
    # [TAB 3] 성적표 & 1타 강사 노트
    # ------------------------------------------
    with tab3:
        if not ss.is_graded:
            st.info("📝 문제를 풀고 채점을 완료해야 성적표가 발급됩니다.")
        else:
            total = len(ss.quiz)
            score = ss.history[-1]

            st.markdown(f"## 🏆 이번 시험 점수: **{score}점**")
            c1, c2 = st.columns(2)
            c1.metric("🟢 맞힌 문항", f"{total - len(ss.wrong)}개")
            c2.metric("🔴 틀린 문항", f"{len(ss.wrong)}개")
            st.divider()

            st.markdown("### 👩‍🏫 AI 튜터의 밀착 해설 & 오답 노트")
            
            for i, q in enumerate(ss.quiz):
                user_ans = ss.answers.get(i, "선택 안함")
                real_ans = q.get("answer")
                is_correct = (user_ans == real_ans)

                st.markdown(f'<div class="quiz-card">', unsafe_allow_html=True)
                st.markdown(f"**Q{i+1}.** {q.get('question')}")
                
                # 정답/오답 여부에 따른 커스텀 박스 출력
                if is_correct:
                    st.markdown(f'<div class="correct-box"><b>🎉 정답입니다!</b> (나의 선택: {user_ans})<br><br><b>[해설]</b> {q.get("explanation")}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="wrong-box"><b>❌ 틀렸습니다.</b> (나의 선택: {user_ans} / <b>정답: {real_ans}</b>)<br><br><b>[해설]</b> {q.get("explanation")}</div>', unsafe_allow_html=True)

                # 선생님 꿀팁 (틀린 문제는 기본적으로 열려있게)
                with st.expander("💡 1타 강사의 심화 학습 노트", expanded=not is_correct):
                    st.markdown(f'<div class="study-note">👩‍🏫 <b>선생님의 꿀팁:</b><br>{q.get("study_note")}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            c1, c2 = st.columns(2)
            with c1:
                if ss.wrong:
                    if st.button("🔥 오답만 모아서 재도전", type="primary", use_container_width=True):
                        txt = " ".join([q.get("question","") + " " + q.get("explanation","") for q in ss.wrong])
                        ss.quiz = generate_quiz(txt, len(ss.wrong), "최상", "함정 주의")
                        ss.answers = {}
                        ss.wrong = []
                        ss.is_graded = False
                        st.rerun()
                else:
                    st.success("🎉 완벽합니다! 다시 풀 오답이 없습니다.")
            with c2:
                if st.button("🔄 지문 비우고 새로 시작하기", use_container_width=True):
                    ss.quiz = None
                    ss.answers = {}
                    ss.wrong = []
                    ss.is_graded = False
                    st.rerun()
