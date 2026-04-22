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
# 🔥 quiz 검증 (study_note 추가)
# ==========================================
def validate_quiz(quiz):
    if not isinstance(quiz, list):
        return False
    for q in quiz:
        if not isinstance(q, dict):
            return False
        if not all(k in q for k in ["question", "options", "answer", "explanation", "study_note"]):
            return False
    return True

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

    return None

# ==========================================
# 🔥 fallback 문제 (study_note 추가)
# ==========================================
def fallback_quiz(count):
    dummy = []
    for i in range(max(count, 1)):
        ans = random.choice(["1", "2", "3", "4"])
        dummy.append({
            "question": f"기본 문제 {i+1} (시스템 오류로 자동 생성됨)",
            "options": ["1", "2", "3", "4"],
            "answer": ans,
            "explanation": "AI 응답 실패로 생성된 더미 문제입니다.",
            "study_note": "💡 현재 AI 서버 상태가 불안정합니다. 새로고침 후 다시 시도해주세요."
        })
    return dummy

# ==========================================
# 🔥 문제 생성 (프롬프트 강화)
# ==========================================
def generate_quiz(text, count, difficulty, q_type):
    prompt = f"""
JSON만 출력하세요. 마크다운은 제외하세요.
'study_note'에는 학생이 이 개념과 연관해서 추가로 알면 좋을 심화 내용이나 강사의 꿀팁을 친절하게 작성해주세요.

[
  {{
    "question": "문제 내용",
    "options": ["1번 보기","2번 보기","3번 보기","4번 보기"],
    "answer": "정답 텍스트 (반드시 옵션 중 하나와 정확히 일치)",
    "explanation": "정답인 이유와 오답인 이유 해설",
    "study_note": "💡 핵심 개념 정리 & 1타 강사의 꿀팁!"
  }}
]

문제 수: {count}
난이도: {difficulty}
스타일: {q_type}

[학습 내용]
{text[:2000]}
"""

    with st.spinner("👩‍🏫 AI가 지문을 분석하여 고품질 문제를 출제하고 있습니다..."):
        for _ in range(5):
            res = call_gemini(prompt)

            if not res:
                continue

            quiz = extract_json(res)
            if validate_quiz(quiz):
                return quiz

            quiz = repair_json(res)
            if validate_quiz(quiz):
                return quiz

            time.sleep(1)

    st.warning("⚠️ AI 응답 실패 → 기본 문제로 대체됩니다.")
    return fallback_quiz(count)

# ==========================================
# 🔥 텍스트 품질
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 200:
        return "❌ 짧음", 40, "error"
    elif l < 800:
        return "⚠️ 보통", 70, "warning"
    else:
        return "✅ 좋음", 90, "success"

# ==========================================
# 🎯 UI (인자 구조 유지!)
# ==========================================
def render(market=None, nw=None):
    # CSS 추가 (충돌 방지를 위해 심플하게)
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-list"] { gap: 10px; }
        .stTabs [data-baseweb="tab"] { height: 50px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("💡 AI 스마트 튜터 모의고사")
    st.caption("텍스트를 입력하면 AI가 맞춤형 문제와 핵심 요약 노트를 생성해줍니다.")

    # 상태 초기화
    ss = st.session_state

    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("last_quiz_text", "")
    ss.setdefault("is_graded", False)

    # ------------------------------------------
    # 탭 UI 분리
    # ------------------------------------------
    tab1, tab2, tab3 = st.tabs(["📚 1. 시험 설정", "📝 2. 모의고사 응시", "📖 3. 결과 및 오답 노트"])

    # ==========================================
    # 탭 1: 설정 및 입력
    # ==========================================
    with tab1:
        st.subheader("📄 학습 데이터 입력")
        text = st.text_area("학습할 내용을 자유롭게 붙여넣으세요.", height=200, key="input_text_area")
        
        if text:
            msg, score, m_type = analyze_text_quality(text)
            st.progress(score / 100, text=f"글자수: {len(text)}자 ({msg})")

        with st.container(border=True):
            col1, col2, col3 = st.columns(3)
            count = col1.slider("📌 문제 수", 3, 10, 5)
            difficulty = col2.selectbox("💪 난이도", ["쉬움","보통","어려움"])
            q_type = col3.selectbox("🎯 스타일", ["개념 확인","응용 문제","함정 주의"])

        if st.button("🚀 나만의 모의고사 생성하기", type="primary", use_container_width=True):
            if not text.strip():
                st.toast("❌ 내용을 먼저 입력해주세요!", icon="🚨")
            else:
                quiz = generate_quiz(text, count, difficulty, q_type)

                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.last_quiz_text = text
                ss.is_graded = False
                st.toast("🎉 생성 완료! [2. 모의고사 응시] 탭으로 이동하세요.", icon="✅")
                st.rerun()

    # ==========================================
    # 탭 2: 문제 응시
    # ==========================================
    with tab2:
        if not ss.quiz:
            st.info("👈 [1. 시험 설정] 탭에서 먼저 문제를 생성해주세요.")
        else:
            total = len(ss.quiz)
            answered = len([v for v in ss.answers.values() if v and v != "선택 안함"])

            st.progress(answered / total if total > 0 else 0, text=f"진행 상황: {answered} / {total} 완료")
            st.divider()

            for i, q in enumerate(ss.quiz):
                with st.container(border=True):
                    st.markdown(f"#### Q{i+1}. {q.get('question','문제 오류')}")

                    options = q.get("options", ["1","2","3","4"])

                    ans = st.radio(
                        "선택",
                        ["선택 안함"] + options,
                        key=f"q_{i}",
                        label_visibility="collapsed",
                        disabled=ss.is_graded
                    )

                    if ans != "선택 안함":
                        ss.answers[i] = ans

            st.markdown("<br>", unsafe_allow_html=True)

            if not ss.is_graded:
                if st.button("💯 답안 제출 및 채점", type="primary", use_container_width=True):
                    correct = 0
                    wrong = []

                    for i, q in enumerate(ss.quiz):
                        user = ss.answers.get(i)
                        answer = q.get("answer")

                        if user == answer:
                            correct += 1
                        else:
                            wrong.append(q)

                    if total > 0:
                        score = int(correct / total * 100)
                    else:
                        score = 0

                    ss.history.append(score)
                    ss.wrong = wrong
                    ss.is_graded = True
                    
                    if score == 100:
                        st.balloons()
                    
                    st.toast("채점이 완료되었습니다! [3. 결과] 탭을 확인하세요.", icon="🎓")
                    st.rerun()
            else:
                st.success("📝 채점이 완료되었습니다. 3번 탭에서 성적을 확인하세요.")

    # ==========================================
    # 탭 3: 채점 결과 및 공부 모드
    # ==========================================
    with tab3:
        if not ss.is_graded:
            st.info("📝 문제를 풀고 채점하면 결과와 오답 노트가 나타납니다.")
        else:
            total = len(ss.quiz) if ss.quiz else 0
            score = ss.history[-1] if ss.history else 0

            # 상단 요약
            c1, c2, c3 = st.columns(3)
            c1.metric("최종 점수", f"{score}점")
            c2.metric("맞힌 문항", f"{total - len(ss.wrong)}개")
            c3.metric("틀린 문항", f"{len(ss.wrong)}개")

            if ss.history:
                avg = int(sum(ss.history)/len(ss.history))
                st.caption(f"📊 나의 누적 평균 점수: {avg}점")

            st.divider()
            st.markdown("### 👨‍🏫 AI 튜터의 해설 & 핵심 노트")

            for i, q in enumerate(ss.quiz):
                user_ans = ss.answers.get(i, "선택 안함")
                real_ans = q.get("answer")
                is_correct = (user_ans == real_ans)

                with st.container(border=True):
                    if is_correct:
                        st.markdown(f"**🟢 Q{i+1}. 정답!** (나의 선택: {user_ans})")
                    else:
                        st.markdown(f"**🔴 Q{i+1}. 틀렸습니다.** (선택: {user_ans} / **정답: {real_ans}**)")

                    st.markdown(f"> {q.get('question')}")
                    
                    # 해설
                    st.write("**[해설]**")
                    st.write(q.get("explanation","없음"))

                    # 공부 모드 (꿀팁) - 틀린 문제만 기본적으로 펼쳐지도록
                    with st.expander("💡 관련 개념 심화 노트 보기", expanded=not is_correct):
                        st.info(q.get("study_note", "추가 내용이 없습니다."))

            st.divider()

            col_a, col_b = st.columns(2)
            with col_a:
                if ss.wrong:
                    if st.button("🔥 오답만 다시 풀기", type="primary", use_container_width=True):
                        txt = " ".join([q.get("question","") + " " + q.get("explanation","") for q in ss.wrong])
                        
                        with st.spinner("오답 기반 문제 생성 중..."):
                            ss.quiz = generate_quiz(txt, len(ss.wrong), "어려움", "함정 주의")
                            ss.answers = {}
                            ss.wrong = []
                            ss.is_graded = False
                            st.toast("오답 기반 재도전 세팅 완료!", icon="🔥")
                            st.rerun()
                else:
                    st.success("완벽합니다! 틀린 문제가 없습니다.")
            
            with col_b:
                if st.button("🔄 전체 초기화 및 새로 시작", use_container_width=True):
                    # history는 남겨두고 현재 시험만 리셋
                    ss.quiz = None
                    ss.answers = {}
                    ss.wrong = []
                    ss.is_graded = False
                    st.rerun()

# 테스트용 (모듈로 불릴 땐 실행되지 않음)
if __name__ == "__main__":
    render()
