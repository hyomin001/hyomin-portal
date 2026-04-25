import streamlit as st
import requests
import json
import re
import time
import random
from datetime import datetime

# ==========================================
# 🔐 API KEY
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY 없음")
    st.stop()

# ==========================================
# 🔥 JSON 추출 / 복구 / 검증
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
    if not isinstance(quiz, list): return False
    for q in quiz:
        if not isinstance(q, dict): return False
        if not all(k in q for k in ["question", "options", "answer", "explanation"]): return False
    return True

# ==========================================
# 🔥 Gemini 호출
# ==========================================
def call_gemini(prompt):
    models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-2.0-flash-lite"]
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 8192}
    }
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
        for attempt in range(3):
            try:
                res = requests.post(url, json=payload, timeout=90)
                if res.status_code == 200:
                    data = res.json()
                    try: return data['candidates'][0]['content']['parts'][0]['text']
                    except: return str(data)
                elif res.status_code in [429, 503]:
                    time.sleep((2 ** attempt) + 1)
            except requests.exceptions.Timeout:
                time.sleep(2)
            except Exception:
                time.sleep(1)
    return None

def fallback_quiz(count):
    dummy = []
    for i in range(max(count, 1)):
        ans = random.choice(["1", "2", "3", "4"])
        dummy.append({"question": f"기본 문제 {i+1}", "options": ["1","2","3","4"], "answer": ans, "explanation": "AI 실패로 생성된 문제"})
    return dummy

def generate_quiz(text, count, difficulty, q_type, status):
    prompt = f"""
무조건 JSON 배열 형식으로만 출력하세요. 마크다운이나 일반 텍스트는 절대 포함하지 마세요.
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
    for attempt in range(5):
        status.update(label=f"⏳ AI 모의고사 출제 중... (시도 {attempt + 1}/5)", state="running")
        status.write(f"🤖 방대한 문서를 정독하고 있습니다...")
        res = call_gemini(prompt)
        if not res:
            status.write(f"⚠️ {attempt + 1}차 시도 시간 초과. 재시도 중...")
            continue
        status.write("🔍 AI 응답 완료! JSON 검증 중...")
        quiz = extract_json(res)
        if validate_quiz(quiz):
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz
        quiz = repair_json(res)
        if validate_quiz(quiz):
            status.update(label="✨ 출제 완료! (복구)", state="complete")
            return quiz
        status.write(f"❌ {attempt + 1}차 시도 실패. 재출제 중...")
        time.sleep(1)
    status.update(label="🚨 AI 출제 최종 실패 (기본 문제로 대체)", state="error")
    return fallback_quiz(count)

def analyze_text_quality(text):
    l = len(text)
    if l < 200:    return "❌ 너무 짧음", 40, "🔴"
    elif l < 800:  return "⚠️ 보통", 70, "🟡"
    elif l < 50000: return "✅ 훌륭함", 95, "🟢"
    else:          return "🔥 방대함 (5만 자까지 인식)", 90, "🟢"

# ==========================================
# 🎨 다크 게임 스타일 CSS
# ==========================================
ACADEMY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Orbitron:wght@700;900&display=swap');

:root {
  --bg: #07090f; --bg2: #0c1020; --bg3: #111828;
  --accent: #6c63ff; --cyan: #00d4ff; --gold: #ffd700;
  --green: #00ff88; --red: #ff3366; --orange: #ff8c00;
  --border: rgba(108,99,255,0.2); --text: #e8f0ff; --text2: #8899bb;
}

.stApp { background: var(--bg) !important; color: var(--text) !important; }
/* 제목·단락 텍스트만 색상 지정 (span/div 제외 — 팝오버 색 충돌 방지) */
h1,h2,h3,h4,p,label { color: var(--text) !important; }

/* ── 드롭다운 트리거 + 팝오버 완전 커버 ── */
div[data-baseweb="select"] > div {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}
div[data-baseweb="select"] span,
div[data-baseweb="select"] div { color: var(--text) !important; background-color: transparent !important; }
[data-baseweb="popover"],
[role="listbox"],
[data-baseweb="menu"],
ul[data-testid="stSelectboxVirtualDropdown"] {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
}
[data-baseweb="popover"] *,
[role="listbox"] *,
[data-baseweb="menu"] *,
ul[data-testid="stSelectboxVirtualDropdown"] * {
  color: var(--text) !important;
  background-color: transparent !important;
}
[role="option"]:hover, [data-baseweb="menu"] li:hover {
  background-color: rgba(108,99,255,0.2) !important;
}
[role="option"]:hover *, [data-baseweb="menu"] li:hover * { color: var(--cyan) !important; }
[role="option"][aria-selected="true"] { background-color: rgba(0,212,255,0.15) !important; }
[role="option"][aria-selected="true"] * { color: var(--cyan) !important; }

/* ── 히어로 헤더 ── */
.academy-hero {
  text-align: center; padding: 30px 0 20px;
  background: linear-gradient(160deg, var(--bg2), var(--bg));
  border-bottom: 1px solid var(--border); margin-bottom: 24px;
}
.academy-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: clamp(2rem, 5vw, 3.5rem);
  background: linear-gradient(135deg, #fff 0%, var(--cyan) 50%, var(--accent) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: 3px; margin-bottom: 8px;
}
.academy-sub { color: var(--text2) !important; font-size: 0.95rem; }

/* ── 통계 배지 ── */
.stat-badge-row { display: flex; gap: 12px; margin: 16px 0; flex-wrap: wrap; }
.stat-badge {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border); border-radius: 12px;
  padding: 14px 18px; flex: 1; min-width: 120px; text-align: center;
  transition: all 0.3s;
}
.stat-badge:hover { border-color: var(--accent); transform: translateY(-2px); }
.sb-val { font-family: 'Orbitron', sans-serif; font-size: 1.4rem; font-weight: 900; color: var(--cyan) !important; }
.sb-lbl { font-size: 0.7rem; color: var(--text2) !important; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px; }

/* ── 퀴즈 카드 ── */
.quiz-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 20px; padding: 28px; margin-bottom: 20px;
  transition: all 0.3s; position: relative; overflow: hidden;
}
.quiz-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--cyan));
}
.quiz-card:hover { border-color: rgba(108,99,255,0.4); transform: translateY(-2px); }
.quiz-card-correct {
  border-color: rgba(0,255,136,0.4) !important;
  background: linear-gradient(135deg, rgba(0,255,136,0.05), var(--bg3)) !important;
}
.quiz-card-correct::before { background: linear-gradient(90deg, var(--green), #00cc6a) !important; }
.quiz-card-wrong {
  border-color: rgba(255,51,102,0.4) !important;
  background: linear-gradient(135deg, rgba(255,51,102,0.05), var(--bg3)) !important;
}
.quiz-card-wrong::before { background: linear-gradient(90deg, var(--red), #cc0044) !important; }

.q-num {
  font-family: 'Orbitron', sans-serif; font-size: 0.75rem; font-weight: 900;
  color: var(--accent) !important; letter-spacing: 2px; margin-bottom: 8px;
}
.q-text { font-size: 1.05rem; font-weight: 700; color: var(--text) !important; line-height: 1.6; }

/* ── 강사 노트 ── */
.study-note {
  background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(255,140,0,0.05));
  border-left: 4px solid var(--gold); border-radius: 0 12px 12px 0;
  padding: 16px 20px; margin-top: 16px; color: var(--gold) !important;
  font-size: 0.92rem; line-height: 1.7;
}

/* ── 점수 카드 ── */
.score-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 2px solid var(--accent); border-radius: 20px;
  padding: 30px; text-align: center; margin: 20px 0;
}
.score-big {
  font-family: 'Orbitron', sans-serif; font-size: 4rem; font-weight: 900;
  background: linear-gradient(135deg, var(--gold), var(--orange));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  line-height: 1;
}
.score-grade { font-size: 1.2rem; font-weight: 900; margin-top: 8px; }

/* ── 진행 바 ── */
.prog-wrap { background: rgba(255,255,255,0.05); border-radius: 999px; height: 8px; margin: 12px 0; overflow: hidden; }
.prog-fill { height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--accent), var(--cyan)); transition: width 0.5s; }

/* ── 버튼 ── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, rgba(108,99,255,0.25), rgba(0,212,255,0.15)) !important;
  border: 1px solid rgba(108,99,255,0.4) !important; color: var(--cyan) !important;
  font-weight: 700 !important; border-radius: 12px !important; transition: all 0.25s !important;
}
div[data-testid="stButton"] > button:hover {
  background: linear-gradient(135deg, rgba(108,99,255,0.5), rgba(0,212,255,0.3)) !important;
  transform: translateY(-2px) !important; box-shadow: 0 8px 25px rgba(108,99,255,0.4) !important;
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent !important; }
.stTabs [data-baseweb="tab"] {
  background: var(--bg2) !important; border: 1px solid var(--border) !important;
  border-radius: 10px 10px 0 0 !important; color: var(--text2) !important; font-weight: 700 !important;
}
.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.15)) !important;
  border-color: var(--accent) !important; color: var(--cyan) !important;
}

/* ── 입력 ── */
textarea, .stTextArea textarea { 
  background: var(--bg2) !important; border-color: var(--border) !important;
  color: var(--text) !important; border-radius: 12px !important;
}
.stSlider > div > div > div { background: var(--accent) !important; }
</style>
"""

# ==========================================
# 🎯 메인 렌더링
# ==========================================
def render(market=None, nw=None):
    st.markdown(ACADEMY_CSS, unsafe_allow_html=True)

    # 히어로 헤더
    st.markdown("""
    <div class='academy-hero'>
      <div class='academy-title'>🧠 AI 아카데미</div>
      <p class='academy-sub'>Gemini AI가 당신의 학습 자료를 분석하여 무한 문제를 생성합니다</p>
    </div>
    """, unsafe_allow_html=True)

    ss = st.session_state
    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("last_quiz_text", "")
    ss.setdefault("quiz_start_time", None)
    ss.setdefault("quiz_submitted", False)
    ss.setdefault("last_score", None)
    ss.setdefault("last_elapsed", 0)
    ss.setdefault("bookmarks", set())
    ss.setdefault("score_log", [])
    ss.setdefault("streak", 0)
    ss.setdefault("best_score", 0)

    # 통계 배지
    avg_score = int(sum(ss.history) / len(ss.history)) if ss.history else 0
    st.markdown(f"""
    <div class='stat-badge-row'>
      <div class='stat-badge'>
        <div class='sb-val'>{len(ss.history)}</div>
        <div class='sb-lbl'>응시 횟수</div>
      </div>
      <div class='stat-badge'>
        <div class='sb-val'>{avg_score}점</div>
        <div class='sb-lbl'>누적 평균</div>
      </div>
      <div class='stat-badge'>
        <div class='sb-val'>{ss.best_score}점</div>
        <div class='sb-lbl'>최고 점수</div>
      </div>
      <div class='stat-badge'>
        <div class='sb-val'>{ss.streak}🔥</div>
        <div class='sb-lbl'>연속 정답</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_reset, _ = st.columns([1, 5])
    with col_reset:
        if st.button("🧹 초기화"):
            for k in ["quiz","answers","wrong","history","last_quiz_text","quiz_start_time",
                      "quiz_submitted","last_score","last_elapsed","bookmarks","score_log","streak","best_score"]:
                ss.pop(k, None)
            st.rerun()

    with st.expander("💡 사용 가이드", expanded=False):
        st.markdown("""
**📌 사용법:**
1. 학습 내용을 아래 텍스트 박스에 붙여넣거나 직접 입력
2. 문항 수, 난이도, 스타일 설정
3. **[AI 모의고사 출제 시작]** 클릭
4. [응시 화면] 탭에서 문제 풀기
5. [성적표] 탭에서 채점 및 오답 복습

**💡 팁:** 최대 5만 자까지 지원. 길수록 좋은 문제가 나옵니다!
        """)

    tab1, tab2, tab3 = st.tabs(["📝 출제 설정", "🎯 응시 화면", "📊 성적표 & 복습"])

    with tab1:
        text = st.text_area("📚 학습 내용 입력 (최대 5만 자)", height=250,
                            placeholder="공부한 노트, 교재 내용, 회의록 등을 붙여넣으세요!")
        
        char_count = len(text)
        quality_txt, quality_pct, quality_color = analyze_text_quality(text)
        st.caption(f"{quality_color} {quality_txt} | {char_count:,} / 50,000 자 | 출제 성공률 {quality_pct}%")
        
        # 진행 바
        prog_pct = min(char_count / 50000 * 100, 100)
        st.markdown(f"<div class='prog-wrap'><div class='prog-fill' style='width:{prog_pct}%'></div></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        count = col1.slider("문항 수", 3, 30, 5)
        difficulty = col2.selectbox("난이도", ["쉬움", "보통", "어려움", "최상(지옥)"])
        q_type = col3.selectbox("문제 스타일", ["개념 확인", "실무 응용", "함정 유발", "혼합"])

        if st.button("🚀 AI 모의고사 출제 시작", use_container_width=True):
            if not text.strip():
                st.warning("⚠️ 학습 내용을 먼저 입력해주세요.")
            else:
                with st.status("🚀 AI 엔진 가동 중...", expanded=True) as status:
                    quiz = generate_quiz(text, count, difficulty, q_type, status)
                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.last_quiz_text = text
                ss.quiz_start_time = time.time()
                ss.quiz_submitted = False
                ss.last_score = None
                st.toast("🚀 출제 완료! [응시 화면] 탭으로 이동하세요.", icon="✅")

    if ss.quiz:
        total = len(ss.quiz)
        answered = len([v for v in ss.answers.values() if v])

        with tab2:
            if ss.quiz_start_time and not ss.quiz_submitted:
                elapsed = int(time.time() - ss.quiz_start_time)
                mins, secs = divmod(elapsed, 60)
                st.markdown(f"<div style='text-align:right;font-family:\"Orbitron\",sans-serif;font-size:0.9rem;color:#00d4ff;font-weight:900;margin-bottom:8px;'>⏱️ {mins:02d}:{secs:02d}</div>", unsafe_allow_html=True)

            prog = answered / total if total > 0 else 0
            st.markdown(f"<div class='prog-wrap'><div class='prog-fill' style='width:{prog*100:.1f}%'></div></div>", unsafe_allow_html=True)
            st.caption(f"진행률: {answered} / {total} 문항 완료")

            for i, q in enumerate(ss.quiz):
                is_bm = i in ss.bookmarks
                st.markdown(f"""
                <div class='quiz-card'>
                  <div class='q-num'>{'🔖 ' if is_bm else ''}QUESTION {i+1:02d} / {total:02d}</div>
                  <div class='q-text'>{q.get('question','문제 오류')}</div>
                </div>
                """, unsafe_allow_html=True)

                options = q.get("options", ["1","2","3","4"])
                col_q, col_bm = st.columns([10, 1])
                with col_q:
                    ans = st.radio("선택", ["선택 안함"] + options, key=f"q_{i}", label_visibility="collapsed")
                with col_bm:
                    if st.button("🔖" if is_bm else "☆", key=f"bm_{i}"):
                        ss.bookmarks.discard(i) if is_bm else ss.bookmarks.add(i)
                        st.rerun()

                if ans != "선택 안함":
                    ss.answers[i] = ans

        with tab3:
            if st.button("💯 OMR 제출 및 채점하기", use_container_width=True):
                correct = 0
                wrong = []
                elapsed_time = int(time.time() - ss.quiz_start_time) if ss.quiz_start_time else 0

                with st.spinner("📊 채점 중..."):
                    time.sleep(0.8)
                    for i, q in enumerate(ss.quiz):
                        user = ss.answers.get(i)
                        answer = q.get("answer")
                        is_wrong = (user != answer)

                        card_class = "quiz-card-wrong" if is_wrong else "quiz-card-correct"
                        status_icon = "❌" if is_wrong else "✅"
                        st.markdown(f'<div class="quiz-card {card_class}">', unsafe_allow_html=True)
                        st.markdown(f"**{status_icon} Q{i+1}.** {q.get('question','')}")

                        if is_wrong:
                            wrong.append(q)
                            st.error(f"내 답: **{user}** → 정답: **{answer}**")
                        else:
                            correct += 1
                            st.success("정답!")

                        with st.expander(f"📖 해설 보기", expanded=is_wrong):
                            st.write(f"**해설:** {q.get('explanation','없음')}")
                            if q.get("study_note"):
                                st.markdown(f'<div class="study-note">👨‍🏫 <b>1타 강사 Note:</b><br>{q["study_note"]}</div>', unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)

                score = int(correct / total * 100) if total > 0 else 0
                mins_e, secs_e = divmod(elapsed_time, 60)

                # 등급 산정
                if score == 100: grade, grade_color = "S+ 만점", "#ffd700"
                elif score >= 90: grade, grade_color = "A+ 우수", "#00ff88"
                elif score >= 80: grade, grade_color = "A 양호", "#00d4ff"
                elif score >= 70: grade, grade_color = "B 보통", "#6c63ff"
                elif score >= 60: grade, grade_color = "C 미흡", "#ff8c00"
                else: grade, grade_color = "D 재도전", "#ff3366"

                st.markdown(f"""
                <div class='score-card'>
                  <div class='score-big'>{score}</div>
                  <div class='score-grade' style='color:{grade_color} !important;'>{grade}</div>
                  <div style='color:var(--text2);font-size:0.85rem;margin-top:8px;'>
                    {correct}✅ / {len(wrong)}❌ | ⏱️ {mins_e:02d}:{secs_e:02d}
                  </div>
                </div>
                """, unsafe_allow_html=True)

                if score == 100: st.balloons(); st.toast("완벽합니다! 100점 만점! 🎉", icon="🏆")
                elif score >= 70: st.toast("훌륭합니다! 👍", icon="🌟")
                else: st.toast("오답 복습을 통해 실력을 키워봐요! 💪", icon="🔥")

                # 연속 정답 스트릭
                if not wrong:
                    ss.streak = ss.get("streak", 0) + 1
                    if ss.streak >= 3:
                        st.success(f"🔥 {ss.streak}회 연속 만점! 놀라운 실력입니다!")
                else:
                    ss.streak = 0

                ss.best_score = max(ss.get("best_score", 0), score)
                ss.history.append(score)
                ss.score_log.append({"score": score, "count": total, "date": datetime.now().strftime("%m/%d %H:%M")})
                if len(ss.score_log) > 20: ss.score_log = ss.score_log[-20:]
                ss.wrong = wrong
                ss.quiz_submitted = True
                ss.last_elapsed = elapsed_time

                # 결과 다운로드
                now_str = datetime.now().strftime("%Y%m%d_%H%M")
                result_lines = [f"[AI 모의고사 결과 — {now_str}]", f"점수: {score}점 ({correct}/{total})", f"등급: {grade}", ""]
                for i, q in enumerate(ss.quiz):
                    user = ss.answers.get(i, "미응답")
                    answer = q.get("answer")
                    mark = "✅" if user == answer else "❌"
                    result_lines += [f"Q{i+1}. {mark} {q.get('question','')}", f"   내 답: {user}  정답: {answer}", f"   해설: {q.get('explanation','')}", ""]
                st.download_button("📥 결과 저장", data="\n".join(result_lines),
                                   file_name=f"quiz_{now_str}.txt", mime="text/plain", use_container_width=True)

            # 누적 점수 차트
            if len(ss.history) >= 2:
                import pandas as pd
                chart_data = pd.DataFrame({"점수": ss.history[-10:], "회차": [f"{i+1}회" for i in range(len(ss.history[-10:]))]})
                st.line_chart(chart_data.set_index("회차"), use_container_width=True)

            # 오답 복습
            if ss.wrong:
                st.markdown("---")
                if ss.bookmarks:
                    with st.expander(f"🔖 북마크 ({len(ss.bookmarks)}개)", expanded=False):
                        for bi in sorted(ss.bookmarks):
                            if bi < len(ss.quiz):
                                bq = ss.quiz[bi]
                                st.markdown(f"**Q{bi+1}.** {bq.get('question','')}")
                                st.caption(f"정답: {bq.get('answer','')} | {bq.get('explanation','')[:80]}...")
                st.subheader("🔥 오답 밀착 재출제 (지옥 난이도)")
                st.caption(f"틀린 {len(ss.wrong)}문제를 다시 지옥 난이도로 재출제합니다.")
                if st.button("🚨 오답 지옥 재도전!", use_container_width=True):
                    with st.status("🔥 오답 분석 및 재출제 중...", expanded=True) as status:
                        txt = " ".join([q.get("question","") + " " + q.get("study_note","") + " " + q.get("explanation","") for q in ss.wrong])
                        ss.quiz = generate_quiz(txt, len(ss.wrong), "최상(지옥)", "함정 유발", status)
                        ss.answers = {}; ss.wrong = []
                    st.rerun()
