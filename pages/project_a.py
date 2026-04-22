import streamlit as st
import requests
import json
import re
import time
import random
import unicodedata
from datetime import datetime

# ==========================================
# 🔐 API KEY
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY 없음")
    st.stop()

# ==========================================
# 🔥 JSON 파싱
# ==========================================
def extract_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return None
    except:
        return None

def repair_json(text):
    try:
        text = text.replace("'", '"')
        text = re.sub(r",\s*\}", "}", text)
        text = re.sub(r",\s*\]", "]", text)
        text = re.sub(r'[\x00-\x1f\x7f]', ' ', text)
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
        if not all(k in q for k in ["question", "options", "answer", "explanation"]):
            return False
        if not isinstance(q.get("options"), list) or len(q.get("options")) < 2:
            return False
    return True

# ==========================================
# 🧠 퍼지 정답 매칭
# ==========================================
def normalize_str(s):
    s = str(s).strip()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r'[\s\u200b\u00a0]+', '', s)
    return s.lower()

def is_answer_correct(user_ans, correct_ans, options=None):
    if not user_ans or not correct_ans:
        return False
    if normalize_str(user_ans) == normalize_str(correct_ans):
        return True
    if options:
        try:
            idx = int(re.search(r'\d+', str(user_ans)).group()) - 1
            if 0 <= idx < len(options):
                return normalize_str(options[idx]) == normalize_str(correct_ans)
        except:
            pass
    return False

# ==========================================
# 🔥 Gemini 호출
# ==========================================
def call_gemini(prompt, timeout=90, max_tokens=8192):
    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite"
    ]
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": max_tokens}
    }
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
        for attempt in range(3):
            try:
                res = requests.post(url, json=payload, timeout=timeout)
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
# 🧠 주제 자동 감지
# ==========================================
def detect_subject(text):
    prompt = f"""다음 텍스트의 주제/분야를 한 단어로만 답하세요.
예: 역사, 과학, 수학, 법학, 경영, 의학, IT/프로그래밍, 언어, 문학, 기타

코드(Python, JavaScript 등)가 포함되어 있으면 반드시 "IT/프로그래밍"으로 답하세요.

텍스트:
{text[:500]}

주제(한 단어):"""
    res = call_gemini(prompt, timeout=30, max_tokens=20)
    return res.strip()[:15] if res else "일반"

# ==========================================
# 🧠 2단계 압축
# ==========================================
def summarize_chunk(chunk, chunk_idx, total_chunks, status):
    prompt = f"""[파트 {chunk_idx+1}/{total_chunks}] 아래 텍스트에서 시험 출제용 핵심만 추출하세요.
- 중요 개념, 정의, 수치, 인과관계, 예외사항만 포함
- bullet point로 간결하게
- 서론/인사/불필요한 설명 제외

텍스트:
{chunk}

핵심 추출:"""
    res = call_gemini(prompt, timeout=60)
    if res:
        status.write(f"  ✅ 파트 {chunk_idx+1}/{total_chunks} 완료")
    return res or f"[파트 {chunk_idx+1} 실패]"

def final_compress(summaries, subject, status):
    combined = "\n\n".join(summaries)
    if len(combined) <= 15000:
        return combined
    status.write("  🔁 최종 재압축 중...")
    prompt = f"""아래는 {subject} 관련 문서의 파트별 핵심 요약입니다.
시험 출제에 중요한 내용만 남겨 전체를 재정리하세요.
중복 제거, 중요도 낮은 내용 삭제, 핵심 개념 중심으로 압축.

{combined[:20000]}

최종 핵심 정리:"""
    res = call_gemini(prompt, timeout=90)
    if res:
        status.write("  ✅ 최종 압축 완료")
        return res
    return combined[:15000]

def compress_long_text(text, status, subject="일반"):
    MAX_DIRECT = 8000
    CHUNK_SIZE = 5000
    if len(text) <= MAX_DIRECT:
        return text

    status.write(f"📄 긴 문서 감지 ({len(text):,}자) → 2단계 압축 시작...")

    chunks = []
    remaining = text
    while len(remaining) > CHUNK_SIZE:
        cut = CHUNK_SIZE
        for boundary in ['.\n\n', '\n\n', '.\n', '. ', '\n']:
            pos = remaining.rfind(boundary, CHUNK_SIZE // 2, CHUNK_SIZE)
            if pos > 0:
                cut = pos + len(boundary)
                break
        chunks.append(remaining[:cut])
        remaining = remaining[cut:]
    if remaining.strip():
        chunks.append(remaining)

    status.write(f"  총 {len(chunks)}개 파트 분할 → 핵심 추출 중...")
    summaries = []
    for i, chunk in enumerate(chunks):
        summaries.append(summarize_chunk(chunk, i, len(chunks), status))
        time.sleep(0.2)

    compressed = final_compress(summaries, subject, status)
    ratio = len(compressed) * 100 // len(text) if len(text) > 0 else 0
    status.write(f"  📦 압축 완료: {len(text):,}자 → {len(compressed):,}자 ({ratio}%)")
    return compressed

# ==========================================
# fallback 문제
# ==========================================
def fallback_quiz(count):
    return [{
        "question": f"임시 문제 {i+1} (AI 생성 실패 — 내용 줄여 재시도)",
        "options": ["보기 1", "보기 2", "보기 3", "보기 4"],
        "answer": random.choice(["보기 1", "보기 2", "보기 3", "보기 4"]),
        "explanation": "AI 실패로 생성된 임시 문제입니다.",
        "study_note": "",
        "type": "4지선다"
    } for i in range(max(count, 1))]

# ==========================================
# 🔥 유형별 프롬프트
# ==========================================
def get_type_prompt(q_type, count, subject):
    base = f"""당신은 {subject} 분야 전문 시험 출제 AI입니다.
아래 학습 내용으로 정확히 {count}개의 문제를 출제하세요.

⚠️ 출력 규칙:
1. JSON 배열만 출력 (앞뒤 텍스트/마크다운 없음)
2. answer는 options 중 하나와 완전 일치
3. 각 문제에 "type" 필드 포함
"""
    if q_type == "4지선다":
        return base + """
형식:
[{"type":"4지선다","question":"문제","options":["보기1","보기2","보기3","보기4"],"answer":"정답(options 중 하나)","explanation":"상세 해설","study_note":"핵심 암기 팁"}]"""
    elif q_type == "OX퀴즈":
        return base + """
형식:
[{"type":"OX","question":"참/거짓을 판단하는 서술 문장","options":["O (참)","X (거짓)"],"answer":"O (참) 또는 X (거짓)","explanation":"상세 해설","study_note":"관련 핵심 개념"}]"""
    elif q_type == "빈칸채우기":
        return base + """
형식:
[{"type":"빈칸","question":"핵심 용어를 ___로 표시한 문장 (예: ___은 세포의 에너지 공장이다)","options":["정답 단어","오답1","오답2","오답3"],"answer":"정답 단어","explanation":"해설","study_note":"암기법"}]"""
    else:
        return base + """
4지선다/OX/빈칸채우기를 골고루 섞어 출제하세요.
형식:
[{"type":"4지선다 또는 OX 또는 빈칸","question":"문제","options":["보기1","보기2",...],"answer":"정답","explanation":"해설","study_note":"암기 팁"}]"""

# ==========================================
# 🔥 문제 생성
# ==========================================
def generate_quiz(text, count, difficulty, q_type, status, subject="일반"):
    processed_text = compress_long_text(text, status, subject)
    type_prompt = get_type_prompt(q_type, count, subject)

    diff_guide = {
        "쉬움": "정의/사실 중심, 직접적인 표현",
        "보통": "개념 이해 + 기본 적용",
        "어려움": "심화 분석, 예외, 비교, 추론 필요",
        "최상(지옥)": "함정 포함, 유사개념 혼동 유발, 복합 추론, 부정 문제 활용"
    }.get(difficulty, "보통")

    prompt = f"""{type_prompt}

문제 수: 정확히 {count}개
난이도: {difficulty} — {diff_guide}
분야: {subject}

학습 내용:
{processed_text[:18000]}
"""

    for attempt in range(6):
        status.update(label=f"⏳ 출제 중... ({attempt+1}/6)", state="running")
        msgs = ["🤖 학습 내용 분석 중...","🔄 형식 재조정 중...",
                f"🔁 {attempt+1}번째 재시도...","💡 다른 접근법 시도...",
                "🛠️ 복구 모드...","⚡ 마지막 시도..."]
        status.write(msgs[min(attempt, 5)])

        res = call_gemini(prompt, timeout=90)
        if not res:
            status.write("⚠️ 응답 없음, 재시도...")
            time.sleep(2)
            continue

        quiz = extract_json(res)
        if validate_quiz(quiz):
            if len(quiz) < count:
                if len(quiz) >= max(1, count // 2):
                    status.update(label=f"✨ 부분 출제 ({len(quiz)}개)", state="complete")
                    return quiz
                status.write(f"⚠️ 부족 ({len(quiz)}/{count}), 재시도...")
                continue
            status.update(label="✨ 출제 완료!", state="complete")
            return quiz[:count]

        quiz = repair_json(res)
        if validate_quiz(quiz):
            status.write("🛠️ JSON 복구 성공!")
            status.update(label="✨ 출제 완료 (복구)", state="complete")
            return quiz[:count] if len(quiz) >= count else quiz

        if isinstance(quiz, list):
            valid = [q for q in quiz if isinstance(q, dict)
                     and all(k in q for k in ["question","options","answer","explanation"])]
            if len(valid) >= max(1, count // 2):
                status.update(label=f"✨ 부분 완료 ({len(valid)}개)", state="complete")
                return valid

        time.sleep(1 + attempt * 0.5)

    status.update(label="🚨 출제 실패 (기본 문제 대체)", state="error")
    return fallback_quiz(count)

# ==========================================
# 🤖 AI 학습 분석 리포트
# ==========================================
def generate_study_report(quiz, answers, score, subject):
    wrong_qs = []
    for i, q in enumerate(quiz):
        user = (answers.get(i) or "").strip()
        correct = (q.get("answer") or "").strip()
        if not is_answer_correct(user, correct, q.get("options")):
            wrong_qs.append({
                "question": q.get("question",""),
                "correct": correct,
                "user_answer": user,
                "explanation": q.get("explanation","")
            })
    if not wrong_qs:
        return "🎉 **완벽합니다!** 모든 문제를 맞혔습니다. 다음 단계로 나아가세요!"

    prompt = f"""학생이 {subject} 시험에서 {score}점을 받았습니다.
틀린 문제 목록:
{json.dumps(wrong_qs, ensure_ascii=False, indent=2)}

아래 항목을 포함한 학습 분석 리포트를 한국어로 작성하세요 (3~5문단):
1. 취약 개념/영역 파악
2. 오답 패턴 분석 (왜 틀렸는지)
3. 우선 복습해야 할 내용
4. 구체적 학습 전략 추천

친절하고 동기부여가 되는 톤으로 작성."""

    res = call_gemini(prompt, timeout=60)
    return res or "분석 리포트 생성 실패. 오답 해설을 직접 확인해주세요."

# ==========================================
# 📊 텍스트 품질
# ==========================================
def analyze_text_quality(text):
    l = len(text)
    if l < 200:    return "❌ 너무 짧음", 40
    elif l < 800:  return "⚠️ 보통", 70
    elif l < 8000: return "✅ 훌륭함 (직접 출제)", 95
    elif l < 50000:  return "🔄 대용량 (2단계 압축 후 출제)", 88
    elif l < 150000: return "📚 초대용량 (다단계 압축, 3~6분)", 80
    else:            return "🌊 극대용량 (5~10분 소요)", 70

# ==========================================
# 🎨 CSS
# ==========================================
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');
*,html,body{font-family:'Noto Sans KR',sans-serif!important;}
.quiz-card{background:linear-gradient(145deg,#fff,#f5f7fa);border-radius:20px;padding:28px;
  margin-bottom:22px;box-shadow:8px 8px 24px #e0e3e8,-4px -4px 12px #fff;
  border:1px solid rgba(255,255,255,.9);transition:transform .25s ease,box-shadow .25s ease;}
.quiz-card:hover{transform:translateY(-3px);box-shadow:0 16px 36px rgba(0,0,0,.09);}
.quiz-card-correct{background:linear-gradient(135deg,#f0fff4,#e6ffe6)!important;border:2px solid #48bb78!important;}
.quiz-card-wrong{background:linear-gradient(135deg,#fff5f5,#ffe6e6)!important;border:2px solid #f56565!important;}
.study-note{background:linear-gradient(135deg,#fffcf0,#fff3cd);border-left:5px solid #f59e0b;
  padding:16px 20px;margin-top:16px;border-radius:12px;color:#92400e;font-weight:500;line-height:1.7;}
.report-box{background:linear-gradient(135deg,#f0f4ff,#e8f0fe);border-left:5px solid #4361ee;
  padding:20px 24px;margin-top:16px;border-radius:12px;color:#1a237e;line-height:1.8;}
.streak-badge{display:inline-block;background:linear-gradient(135deg,#f72585,#b5179e);
  color:white;padding:4px 14px;border-radius:50px;font-weight:700;font-size:.9em;
  margin-left:10px;box-shadow:0 3px 10px rgba(247,37,133,.4);}
.chunk-info{background:linear-gradient(135deg,#e8f4fd,#d1ecf1);border-left:4px solid #17a2b8;
  padding:12px 16px;border-radius:8px;font-size:.9em;color:#0c5460;margin:8px 0;}
.subject-badge{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);
  color:white;padding:3px 14px;border-radius:50px;font-size:.85em;font-weight:700;margin-left:8px;}
div.stButton>button:first-child{background:linear-gradient(135deg,#667eea,#764ba2)!important;
  color:white!important;border:none!important;border-radius:50px!important;padding:12px 28px!important;
  font-weight:700!important;font-size:1.05em!important;transition:all .3s ease!important;
  box-shadow:0 6px 18px rgba(118,75,162,.4)!important;}
div.stButton>button:first-child:hover{transform:scale(1.04) translateY(-2px)!important;
  box-shadow:0 10px 24px rgba(118,75,162,.6)!important;}
.stTabs [data-baseweb="tab-list"]{gap:12px;background:transparent;}
.stTabs [data-baseweb="tab"]{background:#f8f9fa;border-radius:10px 10px 0 0;padding:10px 18px;
  border:1px solid #e9ecef;border-bottom:none;transition:.3s;}
.stTabs [aria-selected="true"]{background:white!important;border-top:3px solid #667eea!important;
  font-weight:700!important;color:#764ba2!important;}

/* 🔥 st.expander 우측 화살표 완전 제거 (글자 겹침 해결) */
[data-testid="stExpanderToggleIcon"] { display: none !important; }
details summary svg { display: none !important; }
</style>""", unsafe_allow_html=True)

# ==========================================
# 🎯 MAIN UI
# ==========================================
def render(market=None, nw=None):
    st.title("🔥 AI 모의고사 Pro")
    inject_css()

    ss = st.session_state
    ss.setdefault("quiz", None)
    ss.setdefault("answers", {})
    ss.setdefault("wrong", [])
    ss.setdefault("history", [])
    ss.setdefault("subject", "일반")
    ss.setdefault("streak", 0)
    ss.setdefault("best_streak", 0)
    ss.setdefault("report", None)
    ss.setdefault("timer_start", None)
    ss.setdefault("timer_enabled", False)
    ss.setdefault("timer_limit", 60)
    ss.setdefault("scored", False)

    _, col_reset = st.columns([6, 1])
    with col_reset:
        if st.button("🧹 초기화"):
            for k in ["quiz","answers","wrong","report","timer_start","scored"]:
                ss[k] = None if k in ["quiz","report","timer_start"] else ([] if k in ["answers","wrong"] else False)
            st.rerun()

    tab1, tab2, tab3 = st.tabs(["📝 출제 설정", "🎯 응시 화면", "📊 성적표 & 분석"])

    # ──────────────────────────────
    # TAB 1
    # ──────────────────────────────
    with tab1:
        with st.expander("💡 사용 가이드", expanded=False):
            st.markdown("""
**📌 글자 수 제한 없음** — 내부 2단계 압축으로 책 1챕터도 처리 가능  
**⏱ 예상 시간:** 8천자↓ 약 1분 / ~5만자 2~4분 / ~15만자 4~8분 / 그 이상 8~15분  
**🔥 문제 유형:** 4지선다 / OX퀴즈 / 빈칸채우기 / 혼합  
**🤖 채점 후:** AI가 취약점 분석 리포트 자동 생성  
**📥 결과 다운로드:** 채점 후 txt 파일로 저장 가능  
            """)

        text = st.text_area(
            "📚 학습 내용 (길이 무제한)",
            height=260,
            placeholder="교재, 노트, 회의록, 논문 등 무엇이든 붙여넣으세요!"
        )

        char_count = len(text)
        q_label, prob = analyze_text_quality(text)
        st.caption(f"현재 글자 수: **{char_count:,}자**  |  분석: {q_label}  |  성공 확률: **{prob}%**")

        if char_count > 8000:
            est_parts = max(2, char_count // 5000)
            est_sec_lo = est_parts * 5 + 30
            est_sec_hi = est_parts * 10 + 60
            lo_m = max(1, est_sec_lo // 60)
            hi_m = max(2, est_sec_hi // 60)
            time_str = f"약 {lo_m}~{hi_m}분" if hi_m >= 2 else "약 1~2분"
            st.markdown(f"""<div class="chunk-info">
ℹ️ <b>2단계 압축 모드:</b> {char_count:,}자 → {est_parts}개 파트 핵심 추출 → 최종 재압축 → 출제<br>
예상 처리 시간: {time_str}
</div>""", unsafe_allow_html=True)

        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        count      = col1.slider("문항 수", 3, 20, 5)
        difficulty = col2.selectbox("난이도", ["쉬움","보통","어려움","최상(지옥)"])
        q_type     = col3.selectbox("문제 유형", ["4지선다","OX퀴즈","빈칸채우기","혼합"])
        timer_on   = col4.checkbox("⏱ 타이머 모드")
        timer_limit = col4.number_input("제한(초/전체)", 30, 3600, 300) if timer_on else 300

        auto_subject = st.checkbox("🧠 주제 자동 감지 (권장)", value=True)
        manual_subject = None
        if not auto_subject:
            manual_subject = st.text_input("분야 직접 입력", placeholder="예: 의학, 법학, 경영...")

        if st.button("🚀 AI 모의고사 출제 시작"):
            if not text.strip():
                st.warning("⚠️ 학습 내용을 먼저 입력해주세요.")
            else:
                with st.status("🚀 AI 엔진 가동 중...", expanded=True) as status:
                    if auto_subject:
                        status.write("🔍 주제 자동 감지 중...")
                        subject = detect_subject(text)
                        status.write(f"  ✅ 감지된 주제: **{subject}**")
                    else:
                        subject = manual_subject or "일반"
                    ss.subject = subject
                    quiz = generate_quiz(text, count, difficulty, q_type, status, subject)

                ss.quiz = quiz
                ss.answers = {}
                ss.wrong = []
                ss.report = None
                ss.scored = False
                ss.timer_enabled = timer_on
                ss.timer_limit = timer_limit
                ss.timer_start = time.time()
                st.toast(f"🚀 [{subject}] 출제 완료! [응시 화면] 탭으로 이동하세요.", icon="✅")

    # ──────────────────────────────
    # TAB 2
    # ──────────────────────────────
    if ss.quiz:
        total = len(ss.quiz)
        answered = len([v for v in ss.answers.values() if v])
        prog = max(0.0, min(1.0, answered / total)) if total > 0 else 0.0

        with tab2:
            h1, h2, h3 = st.columns([4, 2, 2])
            h1.progress(prog, text=f"진행: {answered}/{total} 문항")
            h2.markdown(f"분야: <span class='subject-badge'>{ss.subject}</span>", unsafe_allow_html=True)
            if ss.streak >= 3:
                h3.markdown(f"🔥 <span class='streak-badge'>{ss.streak}연속 정답!</span>", unsafe_allow_html=True)

            if ss.timer_enabled and ss.timer_start:
                elapsed = time.time() - ss.timer_start
                remaining = max(0, ss.timer_limit - elapsed)
                mins, secs = divmod(int(remaining), 60)
                color = "#f72585" if remaining < 60 else "#667eea"
                st.markdown(f"""<div style="background:linear-gradient(135deg,{color},{color}cc);
color:white;border-radius:16px;padding:10px 20px;text-align:center;
font-size:1.5em;font-weight:900;margin-bottom:16px;">⏱ {mins:02d}:{secs:02d}</div>""",
                    unsafe_allow_html=True)
                if remaining == 0:
                    st.warning("⏰ 시간 초과! [성적표] 탭에서 채점하세요.")

            st.markdown("---")

            for i, q in enumerate(ss.quiz):
                type_icon = {"4지선다":"📋","OX":"⭕","빈칸":"📝"}.get(
                    str(q.get("type",""))[:2], "📋")
                st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                st.markdown(f"#### {type_icon} Q{i+1}. {q.get('question','문제 오류')}")

                options = q.get("options", ["보기1","보기2","보기3","보기4"])
                prev = ss.answers.get(i)
                choices = ["선택 안함"] + options
                default_idx = choices.index(prev) if prev in choices else 0

                ans = st.radio(
                    f"Q{i+1}",
                    choices,
                    index=default_idx,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                if ans != "선택 안함":
                    if ss.answers.get(i) != ans:
                        st.toast(f"Q{i+1} 마킹!", icon="✏️")
                    ss.answers[i] = ans

                st.markdown('</div>', unsafe_allow_html=True)

            st.info("✅ 모두 풀었으면 [성적표 & 분석] 탭에서 채점하세요!")

    # ──────────────────────────────
    # TAB 3
    # ──────────────────────────────
    if ss.quiz:
        total = len(ss.quiz)
        with tab3:
            if not ss.scored:
                if st.button("💯 OMR 제출 및 채점"):
                    correct = 0
                    wrong = []
                    streak = 0
                    best_streak = ss.best_streak

                    with st.spinner("📊 채점 및 AI 분석 중..."):
                        time.sleep(0.5)
                        for i, q in enumerate(ss.quiz):
                            user = (ss.answers.get(i) or "").strip()
                            answer = (q.get("answer") or "").strip()
                            options = q.get("options", [])
                            ok = is_answer_correct(user, answer, options)

                            card_cls = "quiz-card-correct" if ok else "quiz-card-wrong"
                            st.markdown(f'<div class="quiz-card {card_cls}">', unsafe_allow_html=True)

                            if ok:
                                correct += 1
                                streak += 1
                                best_streak = max(best_streak, streak)
                                st.success(f"🟢 Q{i+1}. 정답!")
                            else:
                                streak = 0
                                wrong.append(q)
                                st.error(f"🔴 Q{i+1}. 오답  (내 답: **{user or '미응답'}** / 정답: **{answer}**)")

                            st.markdown(f"**{q.get('question','')}**")
                            with st.expander(f"📖 Q{i+1} 해설", expanded=not ok):
                                st.write(q.get("explanation","해설 없음"))
                                if q.get("study_note"):
                                    st.markdown(f'<div class="study-note">👨‍🏫 <b>핵심 Note:</b><br>{q["study_note"]}</div>',
                                        unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)

                        score = int(correct / total * 100) if total > 0 else 0
                        m1, m2, m3, m4 = st.columns(4)
                        m1.metric("최종 점수", f"{score}점")
                        m2.metric("정답/전체", f"{correct}/{total}")
                        m3.metric("최대 연속정답", f"{best_streak}연속")
                        if ss.timer_start:
                            m4.metric("소요 시간", f"{int(time.time()-ss.timer_start)}초")

                        if score == 100:
                            st.balloons()
                            st.toast("🏆 완벽! 100점 만점!", icon="🎊")
                        elif score >= 80:
                            st.toast("🌟 우수한 점수입니다!", icon="👍")
                        elif score >= 60:
                            st.toast("💪 조금만 더!", icon="📚")
                        else:
                            st.toast("🔥 오답 분석으로 취약점 공략!", icon="💡")

                        if wrong:
                            st.markdown("---")
                            with st.spinner("🤖 AI 학습 분석 리포트 생성 중..."):
                                ss.report = generate_study_report(ss.quiz, ss.answers, score, ss.subject)

                        ss.history.append((score, datetime.now().strftime("%m/%d %H:%M"), ss.subject))
                        ss.wrong = wrong
                        ss.streak = streak
                        ss.best_streak = best_streak
                        ss.scored = True

            if ss.scored:
                if ss.report:
                    st.markdown("---")
                    st.subheader("🤖 AI 맞춤 학습 분석 리포트")
                    st.markdown(f'<div class="report-box">{ss.report}</div>', unsafe_allow_html=True)

                # 결과 다운로드
                if ss.quiz:
                    result_text = f"=== AI 모의고사 결과 ({ss.subject}) ===\n날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                    for i, q in enumerate(ss.quiz):
                        user = ss.answers.get(i, "미응답")
                        correct = q.get("answer","")
                        ok = is_answer_correct(str(user), correct, q.get("options",[]))
                        result_text += f"Q{i+1}. [{'O' if ok else 'X'}] {q.get('question','')}\n"
                        result_text += f"  내 답: {user}  /  정답: {correct}\n"
                        result_text += f"  해설: {q.get('explanation','')}\n\n"
                    if ss.report:
                        result_text += f"\n=== AI 분석 리포트 ===\n{ss.report}\n"

                    st.download_button(
                        "📥 결과 다운로드 (.txt)",
                        data=result_text.encode("utf-8"),
                        file_name=f"quiz_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )

            if ss.history:
                st.markdown("---")
                st.subheader("📈 누적 성적")
                scores_only = [h[0] for h in ss.history]
                c1, c2, c3 = st.columns(3)
                c1.metric("누적 평균", f"{int(sum(scores_only)/len(scores_only))}점")
                c2.metric("최고점", f"{max(scores_only)}점")
                c3.metric("시도 횟수", f"{len(scores_only)}회")
                for score, date, subj in reversed(ss.history[-5:]):
                    bar = "🟩" * (score // 10) + "⬜" * (10 - score // 10)
                    st.caption(f"{date}  [{subj}]  {bar}  {score}점")

            if ss.wrong and ss.scored:
                st.markdown("---")
                st.subheader("🔥 오답 밀착 마크 — 하드코어 복수전")
                st.caption(f"틀린 {len(ss.wrong)}개 문제 기반 지옥 난이도 재출제")
                if st.button("🚨 틀린 내용으로만 지옥 난이도 재도전"):
                    with st.status("🔥 오답 분석 중...", expanded=True) as status:
                        txt = " ".join([
                            q.get("question","") + " " + q.get("study_note","") + " " + q.get("explanation","")
                            for q in ss.wrong
                        ])
                        ss.quiz = generate_quiz(txt, len(ss.wrong), "최상(지옥)", "혼합", status, ss.subject)
                        ss.answers = {}
                        ss.wrong = []
                        ss.report = None
                        ss.scored = False
                    st.rerun()
