# pages/project_b.py
# 🗳️ 효민 월드 배틀 v2.0 — 실시간 진영 투표 (완전 익명 · 배틀 아레나 UI)
import streamlit as st
import time
import html
import random
from datetime import datetime
from utils.config import KST
from utils.database import load_db, save_db

VOTE_FILE = "vote_db.json"

def load_vote_db():
    return load_db(VOTE_FILE, {
        "current": {
            "topic":    "오늘의 질문을 기다리는 중...",
            "side_a":   "A",
            "side_b":   "B",
            "desc_a":   "",
            "desc_b":   "",
            "emoji_a":  "🔵",
            "emoji_b":  "🔴",
            "votes_a":  [],
            "votes_b":  [],
            "created":  0,
            "deadline": 0,
        },
        "history": [],
        "total_participants": 0,
    })

def save_vote_db(data):
    save_db(VOTE_FILE, data)

def safe_md(text: str) -> str:
    """HTML escape + Markdown 특수문자 무력화 (언더바, 별표, 백틱, 물결 등)"""
    escaped = html.escape(str(text))
    # Streamlit은 unsafe_allow_html=True 여도 내부 텍스트를 MD로 파싱함
    # 언더바(_), 별표(*), 백틱(`), 물결(~)을 HTML 엔티티로 치환
    escaped = escaped.replace('_', '&#95;')
    escaped = escaped.replace('*', '&#42;')
    escaped = escaped.replace('`', '&#96;')
    escaped = escaped.replace('~', '&#126;')
    return escaped

# ══════════════════════════════════════════════════════════════
#  CSS — 배틀 아레나 다크 테마
# ══════════════════════════════════════════════════════════════

VOTE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

:root {
  --blue:      #3D8EF0;
  --blue-glow: rgba(61,142,240,0.35);
  --blue-dim:  rgba(61,142,240,0.12);
  --red:       #F04F3D;
  --red-glow:  rgba(240,79,61,0.35);
  --red-dim:   rgba(240,79,61,0.12);
  --bg:        #0D0F14;
  --bg2:       #13161E;
  --bg3:       #1A1E2A;
  --border:    rgba(255,255,255,0.07);
  --text:      #E8EAF0;
  --text-dim:  #6B7280;
  --gold:      #F5C842;
}

/* ── 전체 래퍼 ─────────────────────────── */
.vw {
  font-family: 'Noto Sans KR', -apple-system, sans-serif;
  max-width: 680px;
  margin: 0 auto;
  padding: 8px 4px 40px;
  color: var(--text);
}

/* ── LIVE 뱃지 ─────────────────────────── */
.live-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(239,68,68,0.12); color: #EF4444;
  border: 1px solid rgba(239,68,68,0.25);
  border-radius: 999px; padding: 5px 14px;
  font-size: 0.78rem; font-weight: 700; letter-spacing: 1.5px;
}
.live-dot {
  width: 7px; height: 7px; border-radius: 50%; background: #EF4444;
  animation: livepulse 1.4s ease-in-out infinite;
}
@keyframes livepulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.6); }
  50%     { box-shadow: 0 0 0 7px rgba(239,68,68,0); }
}

/* ── 헤더 ──────────────────────────────── */
.battle-header { text-align: center; margin: 20px 0 36px; }
.battle-eyebrow {
  font-size: 0.75rem; letter-spacing: 3px; color: var(--text-dim);
  text-transform: uppercase; margin-bottom: 14px;
}
.battle-topic {
  font-family: 'Black Han Sans', 'Noto Sans KR', sans-serif;
  font-size: clamp(1.6rem, 5vw, 2.4rem);
  line-height: 1.25;
  color: #fff;
  word-break: keep-all;
  text-shadow: 0 2px 30px rgba(0,0,0,0.5);
}
.battle-sub {
  font-size: 0.88rem; color: var(--text-dim); margin-top: 14px;
  display: flex; align-items: center; justify-content: center; gap: 6px;
}

/* ── 배틀 아레나 ────────────────────────── */
.arena-wrap {
  display: grid; grid-template-columns: 1fr auto 1fr;
  gap: 12px; margin-bottom: 28px; align-items: stretch;
}

/* 팀 카드 */
.team-card {
  border-radius: 20px; padding: 28px 16px 24px;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 10px; cursor: pointer;
  position: relative; overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  min-height: 180px;
  border: 1px solid var(--border);
}
.team-card::before {
  content: ''; position: absolute;
  inset: 0; opacity: 0; transition: opacity 0.2s;
}
.team-card:hover { transform: translateY(-4px); }

.team-card-a {
  background: linear-gradient(160deg, var(--bg2) 60%, rgba(61,142,240,0.08));
  border-top: 3px solid var(--blue);
}
.team-card-a::before { background: radial-gradient(ellipse at top, var(--blue-dim), transparent 70%); }
.team-card-a:hover {
  box-shadow: 0 12px 40px var(--blue-glow), inset 0 0 30px rgba(61,142,240,0.05);
}
.team-card-a:hover::before { opacity: 1; }

.team-card-b {
  background: linear-gradient(160deg, var(--bg2) 60%, rgba(240,79,61,0.08));
  border-top: 3px solid var(--red);
}
.team-card-b::before { background: radial-gradient(ellipse at top, var(--red-dim), transparent 70%); }
.team-card-b:hover {
  box-shadow: 0 12px 40px var(--red-glow), inset 0 0 30px rgba(240,79,61,0.05);
}
.team-card-b:hover::before { opacity: 1; }

/* 선택됨 강조 */
.team-card-a.picked {
  background: linear-gradient(160deg, #0f1e35 60%, rgba(61,142,240,0.15));
  border: 1.5px solid var(--blue);
  box-shadow: 0 0 30px var(--blue-glow), inset 0 0 20px rgba(61,142,240,0.06);
}
.team-card-b.picked {
  background: linear-gradient(160deg, #2a0f0d 60%, rgba(240,79,61,0.15));
  border: 1.5px solid var(--red);
  box-shadow: 0 0 30px var(--red-glow), inset 0 0 20px rgba(240,79,61,0.06);
}

.team-emoji {
  font-size: 2.6rem; line-height: 1;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.4));
  animation: floaty 3s ease-in-out infinite;
}
@keyframes floaty {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-5px); }
}

.team-name {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.2rem; color: #fff;
  text-align: center; line-height: 1.3;
  word-break: keep-all;
}
.team-desc { font-size: 0.78rem; color: var(--text-dim); text-align: center; }

/* 결과 숫자 */
.team-result {
  text-align: center; animation: popIn 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes popIn { from { opacity:0; transform: scale(0.7); } to { opacity:1; transform: scale(1); } }
.result-num { font-family: 'Black Han Sans', sans-serif; font-size: 2.4rem; color: #fff; line-height: 1; }
.result-unit { font-size: 0.8rem; color: var(--text-dim); margin-left: 2px; }
.result-pct-a { font-size: 1rem; font-weight: 700; color: var(--blue); margin-top: 4px; }
.result-pct-b { font-size: 1rem; font-weight: 700; color: var(--red); margin-top: 4px; }

/* 내 선택 체크 */
.my-pick {
  position: absolute; top: 10px; right: 12px;
  font-size: 1rem; background: rgba(255,255,255,0.1);
  border-radius: 50%; width: 26px; height: 26px;
  display: flex; align-items: center; justify-content: center;
}

/* VS 배지 */
.vs-center {
  display: flex; align-items: center; justify-content: center;
  flex-direction: column; gap: 8px;
}
.vs-badge {
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--bg3); border: 2px solid var(--border);
  color: var(--text-dim); font-size: 0.85rem; font-weight: 900;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 20px rgba(0,0,0,0.4);
  letter-spacing: 0.5px;
}
.vs-total { font-size: 0.72rem; color: var(--text-dim); text-align: center; }

/* ── 비율 바 ─────────────────────────── */
.ratio-section { margin-bottom: 24px; }
.ratio-labels {
  display: flex; justify-content: space-between;
  font-size: 0.82rem; font-weight: 700; margin-bottom: 8px;
}
.ratio-label-a { color: var(--blue); }
.ratio-label-b { color: var(--red); }
.ratio-track {
  height: 14px; border-radius: 99px;
  background: rgba(255,255,255,0.05);
  overflow: hidden; display: flex; position: relative;
}
.ratio-fill-a {
  background: linear-gradient(90deg, #2563EB, #60A5FA);
  transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
  border-radius: 99px 0 0 99px;
}
.ratio-fill-b {
  background: linear-gradient(90deg, #F87171, #EF4444);
  transition: width 1.2s cubic-bezier(0.4,0,0.2,1);
  border-radius: 0 99px 99px 0;
}
.ratio-footer {
  display: flex; justify-content: space-between;
  font-size: 0.78rem; color: var(--text-dim); margin-top: 8px;
}

/* ── 기세 인디케이터 ──────────────────── */
.momentum-bar {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 12px; padding: 12px 16px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 0.82rem; margin-bottom: 20px;
}
.momentum-fire { color: #F97316; animation: shake 0.5s ease-in-out infinite alternate; }
@keyframes shake { from { transform: rotate(-5deg); } to { transform: rotate(5deg); } }

/* ── 알림/상태 박스 ──────────────────── */
.status-box {
  border-radius: 16px; padding: 16px 20px;
  display: flex; align-items: center; gap: 14px;
  margin-bottom: 20px; border: 1px solid var(--border);
  background: var(--bg2);
  animation: slideUp 0.4s ease;
}
@keyframes slideUp { from { opacity:0; transform: translateY(12px); } to { opacity:1; transform: translateY(0); } }
.status-icon { font-size: 1.8rem; flex-shrink: 0; }
.status-title { font-size: 0.95rem; font-weight: 700; color: #fff; }
.status-sub { font-size: 0.8rem; color: var(--text-dim); margin-top: 3px; }

/* ── 히스토리 ────────────────────────── */
.hist-section { margin-top: 44px; }
.hist-head {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.05rem; color: var(--text-dim);
  letter-spacing: 2px; text-transform: uppercase;
  margin-bottom: 16px; display: flex; align-items: center; gap: 8px;
}
.hist-head::before {
  content: ''; display: block; width: 3px; height: 18px;
  background: var(--gold); border-radius: 2px;
}
.hist-card {
  background: var(--bg2); border: 1px solid var(--border);
  border-radius: 14px; padding: 14px 18px;
  margin-bottom: 10px; transition: border-color 0.15s;
}
.hist-card:hover { border-color: rgba(255,255,255,0.15); }
.hist-top {
  display: flex; justify-content: space-between;
  align-items: flex-start; gap: 12px; margin-bottom: 10px;
}
.hist-topic { font-size: 0.9rem; font-weight: 700; color: var(--text); flex: 1; word-break: keep-all; }
.hist-badge {
  font-size: 0.75rem; font-weight: 700; padding: 4px 10px;
  border-radius: 6px; flex-shrink: 0; white-space: nowrap;
}
.hist-badge-a { background: var(--blue-dim); color: var(--blue); }
.hist-badge-b { background: var(--red-dim); color: var(--red); }
.hist-badge-tie { background: rgba(255,255,255,0.07); color: var(--text-dim); }
.hist-mini-bar {
  height: 6px; border-radius: 99px; overflow: hidden;
  display: flex; background: rgba(255,255,255,0.05);
}
.hist-fill-a { background: var(--blue); }
.hist-fill-b { background: var(--red); }
.hist-meta {
  display: flex; justify-content: space-between;
  font-size: 0.73rem; color: var(--text-dim); margin-top: 7px;
}

/* ── 파티클 캔버스 ────────────────────── */
#vote-confetti {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  pointer-events: none; z-index: 9999;
}

/* ── Streamlit 오버라이드 ──────────────── */
.stApp { background-color: #0D0F14 !important; }
div[data-testid="stVerticalBlock"] { gap: 0 !important; }

.stButton > button {
  font-family: 'Black Han Sans', 'Noto Sans KR', sans-serif !important;
  font-size: 1rem !important; letter-spacing: 1px !important;
  border-radius: 12px !important; border: 1px solid var(--border) !important;
  background: var(--bg3) !important; color: var(--text) !important;
  transition: all 0.18s ease !important;
  padding: 12px 0 !important;
}
.stButton > button:hover {
  background: rgba(255,255,255,0.08) !important;
  border-color: rgba(255,255,255,0.2) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #1D4ED8, #3B82F6) !important;
  color: #fff !important; border-color: transparent !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, #2563EB, #60A5FA) !important;
  box-shadow: 0 8px 24px rgba(59,130,246,0.4) !important;
}

.stTextInput input, .stTextArea textarea {
  background: var(--bg3) !important; color: var(--text) !important;
  border: 1px solid var(--border) !important; border-radius: 10px !important;
  font-family: 'Noto Sans KR', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(61,142,240,0.15) !important;
}
label[data-testid="stWidgetLabel"] { color: var(--text-dim) !important; font-size: 0.82rem !important; }

/* ── 관리자 패널 텍스트 가시성 ──────────── */
div[data-testid="stExpander"] {
  background: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
div[data-testid="stExpander"] summary {
  color: var(--text) !important;
}
div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span {
  color: var(--text) !important;
}
div[data-testid="stExpander"] p,
div[data-testid="stExpander"] span,
div[data-testid="stExpander"] label,
div[data-testid="stExpander"] div {
  color: var(--text) !important;
}
div[data-testid="stExpander"] .stMarkdown p {
  color: var(--text) !important;
}
div[data-testid="stExpander"] [data-testid="stText"],
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
  color: var(--text) !important;
}
.stApp h4 { color: var(--text) !important; }
hr { border-color: var(--border) !important; }
div[data-testid="stExpander"] [data-testid="stSlider"] p { color: var(--text-dim) !important; }
</style>
"""

# ══════════════════════════════════════════════════════════════
#  JS — 파티클 컨페티 + 자동 새로고침
# ══════════════════════════════════════════════════════════════

def confetti_js(color_a="#3D8EF0", color_b="#F04F3D"):
    return f"""
<canvas id="vote-confetti"></canvas>
<script>
(function() {{
  var c = document.getElementById('vote-confetti');
  if (!c) return;
  var ctx = c.getContext('2d');
  c.width = window.innerWidth; c.height = window.innerHeight;
  var particles = [];
  var colors = ['{color_a}', '{color_b}', '#F5C842', '#fff', '#a78bfa'];
  for (var i = 0; i < 120; i++) {{
    particles.push({{
      x: Math.random() * c.width,
      y: -10 - Math.random() * 200,
      r: 4 + Math.random() * 6,
      d: 2 + Math.random() * 4,
      color: colors[Math.floor(Math.random() * colors.length)],
      tilt: Math.random() * 10 - 5,
      tiltAngle: 0,
      tiltSpeed: 0.1 + Math.random() * 0.1,
      shape: Math.random() > 0.5 ? 'rect' : 'circle',
    }});
  }}
  var angle = 0, ttl = 180, frame;
  function draw() {{
    ctx.clearRect(0, 0, c.width, c.height);
    angle += 0.01;
    particles.forEach(function(p) {{
      p.y += p.d; p.x += Math.sin(angle) * 1.2;
      p.tiltAngle += p.tiltSpeed; p.tilt = Math.sin(p.tiltAngle) * 12;
      ctx.beginPath();
      ctx.fillStyle = p.color;
      if (p.shape === 'rect') {{
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.tilt * Math.PI/180);
        ctx.fillRect(-p.r/2, -p.r/2, p.r, p.r * 1.6); ctx.restore();
      }} else {{
        ctx.arc(p.x, p.y, p.r/2, 0, Math.PI*2); ctx.fill();
      }}
      if (p.y > c.height) {{ p.y = -10; p.x = Math.random() * c.width; }}
    }});
    ttl--;
    if (ttl > 0) {{ frame = requestAnimationFrame(draw); }}
    else {{ ctx.clearRect(0,0,c.width,c.height); }}
  }}
  draw();
}})();
</script>
"""

AUTO_REFRESH_JS = """
<script>
// 30초마다 자동 새로고침 (투표 수 실시간 반영)
if (!window._voteRefreshTimer) {
  window._voteRefreshTimer = setInterval(function() {
    // Streamlit rerun trigger — 버튼 클릭 시뮬레이션 없이 조용히
    var ev = new Event('streamlit:formsSubmitted', {bubbles: true});
    window.dispatchEvent(ev);
  }, 30000);
}
</script>
"""


# ══════════════════════════════════════════════════════════════
#  메인 렌더
# ══════════════════════════════════════════════════════════════

def render():
    st.markdown(VOTE_CSS, unsafe_allow_html=True)

    uid      = st.session_state.get('logged_in_user', '')
    is_admin = uid == 'admin'
    vdb      = load_vote_db()
    cur      = vdb["current"]

    # ── 통계 계산 (누가 투표했는지는 절대 노출 안 함) ──
    cnt_a = len(cur["votes_a"])
    cnt_b = len(cur["votes_b"])
    total = cnt_a + cnt_b
    pct_a = round(cnt_a / total * 100) if total else 50
    pct_b = 100 - pct_a

    voted_a    = uid in cur["votes_a"]
    voted_b    = uid in cur["votes_b"]
    user_voted = voted_a or voted_b
    user_side  = "A" if voted_a else ("B" if voted_b else None)

    # safe escape — 언더바 등 마크다운 특수문자도 엔티티 변환
    s_topic  = safe_md(cur['topic'])
    s_side_a = safe_md(cur['side_a'])
    s_side_b = safe_md(cur['side_b'])
    s_desc_a = safe_md(cur.get('desc_a', ''))
    s_desc_b = safe_md(cur.get('desc_b', ''))
    emoji_a  = cur.get('emoji_a', '🔵')
    emoji_b  = cur.get('emoji_b', '🔴')

    # 마감 계산
    deadline = cur.get('deadline', 0)
    is_closed = deadline > 0 and time.time() > deadline
    time_left = ""
    if deadline > 0 and not is_closed:
        rem = int(deadline - time.time())
        h, m = divmod(rem // 60, 60)
        s_rem = rem % 60
        time_left = f"{h}시간 {m}분 {s_rem}초 남음" if h > 0 else f"{m}분 {s_rem}초 남음"

    # ── 기세 텍스트 (순수 시각 장식, 실제 속도 측정 아님) ──
    momentum_txt = ""
    if total >= 5:
        if pct_a > pct_b + 15:
            momentum_txt = f"🔥 {s_side_a} 압도적 우세!"
        elif pct_b > pct_a + 15:
            momentum_txt = f"🔥 {s_side_b} 압도적 우세!"
        elif pct_a > pct_b + 5:
            momentum_txt = f"📈 {s_side_a} 기세 상승 중"
        elif pct_b > pct_a + 5:
            momentum_txt = f"📈 {s_side_b} 기세 상승 중"
        else:
            momentum_txt = "⚡ 초접전! 팽팽한 박빙 승부"

    st.markdown("<div class='vw'>", unsafe_allow_html=True)

    # ── 헤더 ────────────────────────────────────────
    live_or_closed = (
        "<span class='live-badge'><span class='live-dot'></span> LIVE 실시간</span>"
        if not is_closed else
        "<span class='live-badge' style='background:rgba(107,114,128,0.12);color:#6B7280;border-color:rgba(107,114,128,0.2);'>⏹ 투표 종료</span>"
    )
    time_note = ""
    if time_left:
        time_note = f"<span style='color:#F97316;font-size:0.78rem;'>⏰ {time_left}</span>"
    elif is_closed:
        time_note = "<span style='color:#6B7280;font-size:0.78rem;'>투표가 종료되었습니다</span>"

    st.html(f"""
    <div class='battle-header'>
      <div style='display:flex;justify-content:center;gap:10px;align-items:center;margin-bottom:16px;flex-wrap:wrap;'>
        {live_or_closed}
        {time_note}
      </div>
      <div class='battle-eyebrow'>효민 월드 배틀 · 익명 투표</div>
      <div class='battle-topic'>Q. {s_topic}</div>
      <div class='battle-sub'>
        {"🔒 투표 전에는 결과가 숨겨집니다 · 완전 익명" if not user_voted else "✅ 투표 완료 · 익명으로 처리됩니다"}
      </div>
    </div>
    """)

    # ── 배틀 카드 ─────────────────────────────────────
    pick_a_cls = "picked" if voted_a else ""
    pick_b_cls = "picked" if voted_b else ""
    my_pick_a  = "<div class='my-pick'>&#10003;</div>" if voted_a else ""
    my_pick_b  = "<div class='my-pick'>&#10003;</div>" if voted_b else ""

    # 결과 블록: 투표 후에만 숫자 공개, 투표 전엔 빈 문자열
    if user_voted:
        result_a = (
            "<div class='team-result'>"
            f"<div class='result-num'>{cnt_a}"
            "<span class='result-unit'>&#54364;</span></div>"
            f"<div class='result-pct-a'>{pct_a}%</div>"
            "</div>"
        )
        result_b = (
            "<div class='team-result'>"
            f"<div class='result-num'>{cnt_b}"
            "<span class='result-unit'>&#54364;</span></div>"
            f"<div class='result-pct-b'>{pct_b}%</div>"
            "</div>"
        )
    else:
        result_a = result_b = ""

    desc_a_html = f"<div class='team-desc'>{s_desc_a}</div>" if s_desc_a else ""
    desc_b_html = f"<div class='team-desc'>{s_desc_b}</div>" if s_desc_b else ""

    # 카드 HTML을 문자열 연결로 구성 (f-string 중첩 방지)
    card_a_html = (
        "<div class='team-card team-card-a " + pick_a_cls + "'>"
        + my_pick_a
        + "<div class='team-emoji' style='animation-delay:0s;'>" + emoji_a + "</div>"
        + "<div class='team-name'>" + s_side_a + "</div>"
        + desc_a_html
        + result_a
        + "</div>"
    )
    card_b_html = (
        "<div class='team-card team-card-b " + pick_b_cls + "'>"
        + my_pick_b
        + "<div class='team-emoji' style='animation-delay:1.5s;'>" + emoji_b + "</div>"
        + "<div class='team-name'>" + s_side_b + "</div>"
        + desc_b_html
        + result_b
        + "</div>"
    )

    vs_html = (
        "<div class='vs-center'>"
        "<div class='vs-badge'>VS</div>"
        f"<div class='vs-total'>{total}&#47;&#47;<br>&#52632;&#44396;</div>"
        "</div>"
    )
    # vs 가운데 텍스트: "N명\n참여"
    vs_html = (
        "<div class='vs-center'>"
        "<div class='vs-badge'>VS</div>"
        f"<div class='vs-total'>{total}&#47;&#47;</div>"
        "</div>"
    )
    vs_html = (
        "<div class='vs-center'>"
        + "<div class='vs-badge'>VS</div>"
        + f"<div class='vs-total'>{total}명<br>참여</div>"
        + "</div>"
    )

    arena_html = (
        "<div class='arena-wrap'>"
        + card_a_html
        + vs_html
        + card_b_html
        + "</div>"
    )

    st.html(arena_html)

    # ── 비율 바 (투표 후 공개) ──────────────────────
    if user_voted and total > 0:
        lead_name = s_side_a if pct_a > pct_b else (s_side_b if pct_b > pct_a else "")
        st.html(f"""
        <div class='ratio-section'>
          <div class='ratio-labels'>
            <span class='ratio-label-a'>{emoji_a} {pct_a}%</span>
            <span class='ratio-label-b'>{pct_b}% {emoji_b}</span>
          </div>
          <div class='ratio-track'>
            <div class='ratio-fill-a' style='width:{pct_a}%'></div>
            <div class='ratio-fill-b' style='width:{pct_b}%'></div>
          </div>
          <div class='ratio-footer'>
            <span>총 {total}명 참여 (익명)</span>
            <span>{"무승부" if pct_a == pct_b else f"{lead_name} 우세"}</span>
          </div>
        </div>
        """)

        if momentum_txt:
            st.html(f"""
            <div class='momentum-bar'>
              <span style='color:var(--text-dim);font-size:0.8rem;'>현재 흐름</span>
              <span style='font-weight:700;font-size:0.88rem;color:var(--text);'>{momentum_txt}</span>
            </div>
            """)

    # ── 투표 액션 ──────────────────────────────────
    st.write("")

    if not uid:
        st.html("""
        <div class='status-box'>
          <div class='status-icon'>🔐</div>
          <div>
            <div class='status-title'>로그인이 필요합니다</div>
            <div class='status-sub'>투표에 참여하려면 먼저 로그인해주세요.</div>
          </div>
        </div>
        """)

    elif is_closed:
        st.html("""
        <div class='status-box' style='border-color:rgba(107,114,128,0.2);'>
          <div class='status-icon'>⏹</div>
          <div>
            <div class='status-title'>투표가 종료되었습니다</div>
            <div class='status-sub'>다음 배틀을 기대해주세요!</div>
          </div>
        </div>
        """)

    elif user_voted:
        name_picked = s_side_a if user_side == 'A' else s_side_b  # already safe_md
        icon_picked = emoji_a if user_side == 'A' else emoji_b
        color_picked = "#3D8EF0" if user_side == 'A' else "#F04F3D"

        status_html = (
            "<div class='status-box' style='border-color:rgba(255,255,255,0.12);'>"
            f"<div class='status-icon'>{icon_picked}</div>"
            "<div>"
            f"<div class='status-title' style='color:{color_picked};'>"
            f"[{name_picked}] 진영 선택 완료"
            "</div>"
            "<div class='status-sub'>완전 익명으로 처리됩니다 &middot; 마음이 바뀌면 취소할 수 있어요</div>"
            "</div>"
            "</div>"
        )
        st.html(status_html)

        if st.button("🔄  선택 취소하기", use_container_width=True, key="cancel_vote"):
            vdb2 = load_vote_db()
            vdb2["current"]["votes_a"] = [v for v in vdb2["current"]["votes_a"] if v != uid]
            vdb2["current"]["votes_b"] = [v for v in vdb2["current"]["votes_b"] if v != uid]
            save_vote_db(vdb2)
            st.rerun()

    else:
        # 투표 버튼
        st.html("<div style='text-align:center;font-size:0.82rem;color:var(--text-dim);margin-bottom:14px;'>⬇ 진영을 선택하면 실시간 결과가 공개됩니다</div>")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"{emoji_a}  {cur['side_a']} 선택", use_container_width=True, type="primary", key="vote_a"):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_a"]:
                    vdb2["current"]["votes_a"].append(uid)
                    vdb2["total_participants"] = vdb2.get("total_participants", 0) + 1
                save_vote_db(vdb2)
                st.markdown(confetti_js("#3D8EF0", "#60A5FA"), unsafe_allow_html=True)
                st.rerun()
        with col_b:
            if st.button(f"{emoji_b}  {cur['side_b']} 선택", use_container_width=True, key="vote_b"):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_b"]:
                    vdb2["current"]["votes_b"].append(uid)
                    vdb2["total_participants"] = vdb2.get("total_participants", 0) + 1
                save_vote_db(vdb2)
                st.markdown(confetti_js("#F04F3D", "#F87171"), unsafe_allow_html=True)
                st.rerun()

    # ── 히스토리 ──────────────────────────────────
    if vdb.get("history"):
        recent = list(reversed(vdb["history"][-6:]))
        rows_html = ""
        for h in recent:
            ta, tb = h.get('votes_a', 0), h.get('votes_b', 0)
            total_h = ta + tb or 1
            pa = round(ta / total_h * 100)
            pb = 100 - pa
            h_sa = safe_md(h.get('side_a', ''))
            h_sb = safe_md(h.get('side_b', ''))
            h_tp = safe_md(h.get('topic', ''))
            if ta > tb:
                badge_cls, badge_txt = "hist-badge-a", h_sa + " 승 🎉"
            elif tb > ta:
                badge_cls, badge_txt = "hist-badge-b", h_sb + " 승 🎉"
            else:
                badge_cls, badge_txt = "hist-badge-tie", "🤝 무승부"

            date_str = h.get('ended', '')
            rows_html += (
                "<div class='hist-card'>"
                "<div class='hist-top'>"
                f"<div class='hist-topic'>{h_tp}</div>"
                f"<div class='hist-badge {badge_cls}'>{badge_txt}</div>"
                "</div>"
                "<div class='hist-mini-bar'>"
                f"<div class='hist-fill-a' style='width:{pa}%'></div>"
                f"<div class='hist-fill-b' style='width:{pb}%'></div>"
                "</div>"
                "<div class='hist-meta'>"
                f"<span>{h_sa} {pa}% · {h_sb} {pb}%</span>"
                f"<span>{total_h}명 참여 · {date_str}</span>"
                "</div>"
                + "</div>"
            )

        hist_section_html = (
            "<div class='hist-section'>"
            "<div class='hist-head'>지난 배틀 결과</div>"
            + rows_html
            + "</div>"
        )
        st.html(hist_section_html)

    st.html("</div>")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(AUTO_REFRESH_JS, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    #  관리자 패널
    # ══════════════════════════════════════════════
    if is_admin:
        st.write("")
        st.divider()
        st.markdown("#### ⚙️ 관리자 패널")

        with st.expander("📝 새 배틀 설정", expanded=False):
            st.markdown("**새 투표 주제**")
            new_topic = st.text_input("질문", max_chars=60, placeholder="예: 치킨 vs 피자, 뭘 선택할래?")

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**🔵 A 진영**")
                new_side_a  = st.text_input("진영 이름 A", max_chars=20, key="adm_na")
                new_desc_a  = st.text_input("설명 A (선택)", max_chars=40, key="adm_da", placeholder="짧은 설명")
                new_emoji_a = st.text_input("이모지 A", max_chars=4, key="adm_ea", value="🔵")
            with c2:
                st.markdown("**🔴 B 진영**")
                new_side_b  = st.text_input("진영 이름 B", max_chars=20, key="adm_nb")
                new_desc_b  = st.text_input("설명 B (선택)", max_chars=40, key="adm_db", placeholder="짧은 설명")
                new_emoji_b = st.text_input("이모지 B", max_chars=4, key="adm_eb", value="🔴")

            hours = st.slider("투표 마감 시간 (0 = 무기한)", 0, 72, 0, key="adm_hours")

            if st.button("🚀 새 배틀 시작!", use_container_width=True, type="primary", key="adm_start"):
                if new_topic and new_side_a and new_side_b:
                    vdb2 = load_vote_db()
                    old = vdb2["current"]
                    if old.get("votes_a") or old.get("votes_b"):
                        vdb2["history"].append({
                            "topic":   old["topic"],
                            "side_a":  old["side_a"],
                            "side_b":  old["side_b"],
                            "votes_a": len(old["votes_a"]),
                            "votes_b": len(old["votes_b"]),
                            "ended":   datetime.now(KST).strftime("%Y-%m-%d"),
                        })
                    vdb2["current"] = {
                        "topic":    new_topic.strip(),
                        "side_a":   new_side_a.strip(),
                        "side_b":   new_side_b.strip(),
                        "desc_a":   new_desc_a.strip(),
                        "desc_b":   new_desc_b.strip(),
                        "emoji_a":  new_emoji_a.strip() or "🔵",
                        "emoji_b":  new_emoji_b.strip() or "🔴",
                        "votes_a":  [],
                        "votes_b":  [],
                        "created":  time.time(),
                        "deadline": time.time() + hours * 3600 if hours > 0 else 0,
                    }
                    save_vote_db(vdb2)
                    st.success("✅ 새 배틀이 시작되었습니다!")
                    st.rerun()
                else:
                    st.error("질문과 양쪽 진영 이름을 모두 입력해주세요.")

        with st.expander("📊 현재 통계 (관리자 전용)", expanded=False):
            # st.write는 마크다운을 안전하게 처리
            st.write(f"**주제:** {cur['topic']}")
            st.write(f"**A 진영 ({cur['side_a']}):** {cnt_a}표 ({pct_a}%)")
            st.write(f"**B 진영 ({cur['side_b']}):** {cnt_b}표 ({pct_b}%)")
            st.write(f"**총 참여:** {total}명 (개인 정보 미노출 · 완전 익명)")
            if st.button("🗑️ 현재 투표 초기화", key="adm_reset"):
                vdb2 = load_vote_db()
                vdb2["current"]["votes_a"] = []
                vdb2["current"]["votes_b"] = []
                save_vote_db(vdb2)
                st.success("초기화 완료!")
                st.rerun()
