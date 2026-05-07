#수정
import re
import streamlit as st
import time
import os
from datetime import datetime

# ==============================
# 1. 코어 모듈 임포트
# ==============================
from utils.config import MARKET_FILE, USERS_FILE, KST, MESSAGES_FILE, STATS_FILE, estate_config, FORGE_DATA
from utils.database import load_db, save_db, load_stats, save_stats
from utils.core import hash_pw, hash_pw_bcrypt, verify_pw, is_legacy_hash, format_korean_money, get_net_worth, sync_user_data, ADMIN_HASH, pull_user_data, get_online_users
from utils.database import get_login_lock, set_login_lock, clear_login_lock, save_db
from utils.market_sync import run_market_sync
from utils.css import GLOBAL_CSS

# ==============================
# 2. 페이지 기본 설정
# ==============================
st.set_page_config(page_title="HYOMIN PORTAL", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

# ── Google AdSense 소유권 확인 + 광고 코드 ──────────────────
st.markdown("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7480320301712613"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

pull_user_data()

# last_seen — 60초에 한 번만 DB 쓰기
_now = time.time()
if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
    if _now - st.session_state.get('_last_seen_write', 0) >= 60:
        _ls_users = load_db(USERS_FILE, {})
        _ls_uid   = st.session_state.logged_in_user
        if _ls_uid in _ls_users:
            _ls_users[_ls_uid]['last_seen'] = _now
            save_db(USERS_FILE, _ls_users)
        st.session_state['_last_seen_write'] = _now

if "page_view" not in st.session_state:
    st.session_state.page_view = "portal"


# ==============================
# _do_login — 모듈 수준 함수
# ==============================
def _do_login(uid: str, users: dict, device_mode: str):
    u = users[uid]
    st.session_state.update({
        'logged_in_user':    uid,
        'global_cash':       u['cash'],
        'inventory':         u.get('inventory', []),
        'equipped_title':    u.get('equipped_title', '🌱 신규시민'),
        'portfolio':         u.get('portfolio', {}),
        'real_estate':       u.get('real_estate', {}),
        'rent_time':         u.get('rent_time', time.time()),
        'loan':              u.get('loan', 0),
        'loan_time':         u.get('loan_time', time.time()),
        'device_mode':       device_mode,
        'crypto_portfolio':  u.get('crypto_portfolio', {}),
        'daily_quests':      u.get('daily_quests', {}),
        'weapon_level':      u.get('weapon_level', 0),
        'bulk_trade_count':  u.get('bulk_trade_count', 0),
        'bulk_trade_date':   u.get('bulk_trade_date', ''),
        'last_estate_reset': u.get('last_estate_reset', 0),
        'login_fails':       0,
        '_last_seen_write':  0,
        # ✅ [BUG FIX] 로그인 시 누락된 세션 필드 보완
        'gacha_pity':        u.get('gacha_pity', 0),
        'terminal_cleared':  set(u.get('terminal_cleared', [])),
        'dungeon_stats':     u.get('dungeon_stats', {'best_score': 0, 'best_kills': 0, 'clears': 0, 'games_played': 0}),
        'marble_stats':      u.get('marble_stats', {'wins': 0, 'losses': 0, 'games_played': 0, 'best_net_worth': 0}),
        'game_records':      u.get('game_records', {'racing': {'score': 0, 'dist': 0.0}, 'zombie': {'wave': 0, 'score': 0, 'kills': 0}, 'fighter': {'score': 0, 'perfects': 0}, 'sniper': {'score': 0, 'grade': ''}}),
    })
    stats    = load_stats()
    today    = datetime.now(KST).strftime("%Y-%m-%d")
    visitors = stats.get("daily_visitors", {})
    if today not in visitors:      visitors[today] = []
    if uid not in visitors[today]: visitors[today].append(uid)
    stats["daily_visitors"] = visitors
    save_stats(stats)
    st.success("로그인 성공!")
    time.sleep(0.5)
    st.session_state.page_view = "portal"
    st.rerun()


# ==============================
# 🎮 게임 사이트 스타일 포털 CSS
# ==============================
PORTAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Orbitron:wght@700;900&display=swap');

:root {
  --bg:    #060a14;
  --bg2:   #0a1020;
  --bg3:   #0f1830;
  --accent:#6c63ff;
  --cyan:  #00d4ff;
  --gold:  #ffd700;
  --green: #00ff88;
  --red:   #ff3366;
  --border:rgba(108,99,255,0.25);
  --text:  #e8f0ff;
  --text2: #8899bb;
}

/* ── 전체 배경 ── */
.stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
}
.stApp > * { color: var(--text) !important; }

/* ── 파티클 배경 레이어 ── */
.portal-bg {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 70% 50% at 20% 10%, rgba(108,99,255,0.15) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 80% 90%, rgba(0,212,255,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 40% 40% at 60% 40%, rgba(255,215,0,0.06) 0%, transparent 50%);
  animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
  0%   { filter: hue-rotate(0deg) brightness(1); }
  100% { filter: hue-rotate(20deg) brightness(1.05); }
}

/* ── 최상단 HUD 바 ── */
.top-hud {
  background: linear-gradient(90deg, rgba(108,99,255,0.15), rgba(0,212,255,0.10));
  border-bottom: 1px solid var(--border);
  padding: 8px 24px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 0.78rem; color: var(--text2);
  backdrop-filter: blur(10px);
}
.hud-brand {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem; font-weight: 900;
  background: linear-gradient(135deg, var(--accent), var(--cyan));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: 3px;
}
.hud-live {
  display: inline-flex; align-items: center; gap: 5px;
  color: var(--green); font-weight: 700;
}
.hud-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--green);
  animation: pulse 1.4s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(0,255,136,0.6); }
  50%     { box-shadow: 0 0 0 6px rgba(0,255,136,0); }
}
.hud-season {
  background: linear-gradient(135deg, var(--gold), #ff8c00);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  font-weight: 900; font-size: 0.82rem;
}

/* ── 히어로 섹션 ── */
.hero {
  text-align: center;
  padding: 60px 20px 40px;
  position: relative;
}
.hero-eyebrow {
  font-size: 0.72rem; letter-spacing: 5px; text-transform: uppercase;
  color: var(--accent); font-weight: 700; margin-bottom: 12px;
}
.hero-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: clamp(3rem, 8vw, 6rem);
  line-height: 1;
  background: linear-gradient(135deg, #fff 0%, var(--cyan) 40%, var(--accent) 70%, var(--gold) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  animation: titleShine 4s ease-in-out infinite alternate;
  margin-bottom: 16px;
}
@keyframes titleShine {
  0%   { filter: drop-shadow(0 0 20px rgba(108,99,255,0.4)); }
  100% { filter: drop-shadow(0 0 40px rgba(0,212,255,0.6)); }
}
.hero-sub {
  color: var(--text2); font-size: 1.05rem; max-width: 580px; margin: 0 auto 24px;
  line-height: 1.7;
}
.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.15));
  border: 1px solid rgba(108,99,255,0.4);
  border-radius: 999px; padding: 6px 18px;
  font-size: 0.78rem; font-weight: 700;
  color: var(--cyan) !important;
  animation: badgeBounce 2s ease-in-out infinite;
}
@keyframes badgeBounce {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-3px); }
}

/* ── 통계 위젯 ── */
.stat-grid { display:flex; gap:14px; margin:24px 0; flex-wrap:wrap; }
.stat-card {
  flex:1; min-width:140px;
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 18px 14px; text-align: center;
  position: relative; overflow: hidden;
  transition: all 0.3s;
}
.stat-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, transparent, rgba(108,99,255,0.05));
  opacity: 0; transition: opacity 0.3s;
}
.stat-card:hover { transform: translateY(-4px); border-color: rgba(108,99,255,0.5); }
.stat-card:hover::before { opacity: 1; }
.stat-card.online { border-color: rgba(0,255,136,0.3); }
.stat-card.volume  { border-color: rgba(255,215,0,0.3); }
.stat-icon  { font-size: 1.6rem; margin-bottom: 6px; }
.stat-value { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 900; color: var(--cyan) !important; }
.stat-card.online .stat-value { color: var(--green) !important; }
.stat-card.volume  .stat-value { color: var(--gold)  !important; font-size: 1.1rem; }
.stat-label { font-size: 0.7rem; font-weight: 700; color: var(--text2) !important; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }

/* ── 슬라이더/배너 ── */
.banner-scroll-wrap {
  overflow: hidden; margin: 30px 0; position: relative;
}
.banner-scroll-wrap::before,
.banner-scroll-wrap::after {
  content: ''; position: absolute; top: 0; bottom: 0; width: 80px; z-index: 2;
}
.banner-scroll-wrap::before { left: 0; background: linear-gradient(90deg, var(--bg), transparent); }
.banner-scroll-wrap::after  { right: 0; background: linear-gradient(-90deg, var(--bg), transparent); }
.banner-scroll-track {
  display: flex; gap: 16px;
  animation: scrollLeft 30s linear infinite;
  width: max-content;
}
.banner-scroll-track:hover { animation-play-state: paused; }
@keyframes scrollLeft {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.scroll-tag {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 999px; padding: 8px 20px;
  font-size: 0.82rem; font-weight: 700; color: var(--text2);
  white-space: nowrap; flex-shrink: 0;
  transition: all 0.3s;
}
.scroll-tag.hot  { border-color: rgba(255,51,102,0.4); color: var(--red)    !important; }
.scroll-tag.new  { border-color: rgba(0,255,136,0.4);  color: var(--green)  !important; }
.scroll-tag.live { border-color: rgba(0,212,255,0.4);  color: var(--cyan)   !important; }
.scroll-tag.gold { border-color: rgba(255,215,0,0.4);  color: var(--gold)   !important; }

/* ── 게임 카드 그리드 ── */
.game-section-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.3rem; color: var(--text);
  letter-spacing: 2px; margin: 30px 0 16px;
  display: flex; align-items: center; gap: 10px;
}
.game-section-title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}

.game-card {
  background: linear-gradient(160deg, var(--bg2) 0%, var(--bg3) 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px 22px;
  text-align: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-bottom: 16px;
  min-height: 200px;
  display: flex; flex-direction: column; justify-content: center;
}
.game-card::before {
  content: '';
  position: absolute; top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: conic-gradient(from 0deg, transparent 70%, rgba(108,99,255,0.15) 80%, transparent 90%);
  animation: cardSpin 6s linear infinite;
  opacity: 0; transition: opacity 0.4s;
}
.game-card:hover { transform: translateY(-8px) scale(1.02); border-color: var(--accent); box-shadow: 0 20px 60px rgba(108,99,255,0.3); }
.game-card:hover::before { opacity: 1; }
.card-icon { font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 1; }
.card-title { font-family: 'Black Han Sans', sans-serif; font-size: 1.2rem; color: var(--text) !important; margin-bottom: 6px; position: relative; z-index: 1; letter-spacing: 1px; }
.card-desc  { font-size: 0.82rem; color: var(--text2) !important; line-height: 1.6; position: relative; z-index: 1; }
.card-badge {
  position: absolute; top: 12px; right: 12px;
  font-size: 0.65rem; font-weight: 900; letter-spacing: 1px;
  padding: 3px 9px; border-radius: 999px;
}
.badge-hot  { background: rgba(255,51,102,0.2); color: var(--red)   !important; border: 1px solid rgba(255,51,102,0.4); }
.badge-new  { background: rgba(0,255,136,0.2); color: var(--green)  !important; border: 1px solid rgba(0,255,136,0.4); }
.badge-live { background: rgba(0,212,255,0.2); color: var(--cyan)   !important; border: 1px solid rgba(0,212,255,0.4); }
.badge-gold { background: rgba(255,215,0,0.2); color: var(--gold)   !important; border: 1px solid rgba(255,215,0,0.4); }

/* 카드별 테마 색상 */
.card-universe { border-color: rgba(108,99,255,0.4); }
.card-universe:hover { border-color: var(--accent); box-shadow: 0 20px 60px rgba(108,99,255,0.35); }
.card-academy  { border-color: rgba(0,212,255,0.4); }
.card-academy:hover  { border-color: var(--cyan);   box-shadow: 0 20px 60px rgba(0,212,255,0.35); }
.card-battle   { border-color: rgba(255,51,102,0.4); }
.card-battle:hover   { border-color: var(--red);    box-shadow: 0 20px 60px rgba(255,51,102,0.35); }
.card-terminal { border-color: rgba(0,255,136,0.4); }
.card-terminal:hover { border-color: var(--green);  box-shadow: 0 20px 60px rgba(0,255,136,0.35); }
.card-marble   { border-color: rgba(255,215,0,0.4); }
.card-marble:hover   { border-color: var(--gold);   box-shadow: 0 20px 60px rgba(255,215,0,0.35); }
.card-dungeon  { border-color: rgba(192,78,255,0.4); }
.card-dungeon:hover  { border-color: #c04fff; box-shadow: 0 20px 60px rgba(192,78,255,0.35); }

@keyframes cardSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ── 공지/아키텍처 카드 (다크 테마) ── */
.notice-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 20px 24px; margin-bottom: 14px;
}
.notice-card h4 { color: var(--cyan) !important; margin: 0 0 8px; font-size: 1rem; }
.notice-card p  { color: var(--text2) !important; margin: 0; font-size: 0.88rem; line-height: 1.6; }
.notice-badge {
  display: inline-block; border-radius: 6px; font-size: 0.7rem; font-weight: 800;
  padding: 2px 8px; margin: 3px 3px 0 0;
  background: rgba(108,99,255,0.2); color: var(--accent) !important; border: 1px solid rgba(108,99,255,0.3);
}

/* ── 아키텍처 전용 카드 ── */
.arch-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 22px 24px; margin-bottom: 16px;
}
.arch-card h4 { color: var(--cyan) !important; margin: 0 0 8px 0; font-size: 1.05rem; }
.arch-card p  { color: var(--text2) !important; margin: 0; font-size: 0.92rem; line-height: 1.6; }
.arch-badge {
  display: inline-block;
  background: rgba(108,99,255,0.2); color: var(--accent) !important;
  border: 1px solid rgba(108,99,255,0.3); border-radius: 6px;
  font-size: 0.75rem; font-weight: 700; padding: 2px 9px; margin: 3px 3px 0 0;
}
.arch-highlight {
  background: linear-gradient(90deg, rgba(108,99,255,0.12), rgba(0,212,255,0.08));
  border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0;
  padding: 14px 18px; margin-bottom: 18px;
}
.arch-highlight p { color: var(--text) !important; font-weight: 600; font-size: 0.95rem; margin: 0; }
.arch-highlight p.sub { font-weight: 400; color: var(--text2) !important; font-size: 0.88rem; margin-top: 6px; }
.module-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.module-item {
  background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 14px; flex: 1; min-width: 180px;
  font-size: 0.85rem; color: var(--text2) !important;
}
.module-item strong { color: var(--cyan) !important; display: block; margin-bottom: 2px; }

/* ── 서비스 가이드 카드 (다크 팁 박스) ── */
.guide-tip-box {
  border-radius: 8px; padding: 10px 12px; margin-top: 10px;
}

/* ── 푸터 ── */
.portal-footer {
  text-align: center; padding: 40px 0;
  color: var(--text2); font-size: 0.78rem;
  border-top: 1px solid var(--border); margin-top: 40px;
}

/* ── Streamlit 버튼 오버라이드 ── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.15)) !important;
  border: 1px solid rgba(108,99,255,0.4) !important;
  color: var(--cyan) !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  transition: all 0.25s !important;
}
div[data-testid="stButton"] > button:hover {
  background: linear-gradient(135deg, rgba(108,99,255,0.4), rgba(0,212,255,0.3)) !important;
  border-color: var(--accent) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(108,99,255,0.35) !important;
}

/* =========================================
   Streamlit 네이티브 UI (셀렉트박스, 아코디언 등) 다크 테마 보정
   ========================================= */

/* 앱 전체 및 헤더 다크 배경 강제 적용 */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* 일반 마크다운 텍스트 및 제목 색상 보정 */
.stMarkdown p, .stMarkdown span { color: var(--text) !important; }
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }

/* ── ▶ 아코디언 (Expander) 다크 테마 적용 ── */
[data-testid="stExpander"] {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary p {
  color: var(--cyan) !important;
  font-weight: 700;
  letter-spacing: 0.5px;
}
[data-testid="stExpander"] summary svg {
  fill: var(--cyan) !important;
}

/* ── 🔽 셀렉트 박스 (Selectbox) 다크 테마 적용 ── */
div[data-baseweb="select"] > div {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}
/* 드롭다운 클릭 시 펼쳐지는 선택 옵션 리스트 배경 및 글자색 */
div[data-baseweb="popover"] ul, ul[data-testid="stSelectboxVirtualDropdown"] {
  background-color: var(--bg3) !important;
  border: 1px solid var(--border) !important;
}
div[data-baseweb="popover"] li, li[role="option"] {
  color: var(--text) !important;
}
div[data-baseweb="popover"] li:hover, li[role="option"]:hover {
  background-color: rgba(108,99,255,0.2) !important;
  color: var(--cyan) !important;
}

/* ── ✍️ 텍스트 입력창 (Input Box) 다크 테마 적용 ── */
input[type="text"], input[type="password"] {
  background-color: var(--bg2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
}
input[type="text"]::placeholder, input[type="password"]::placeholder {
  color: var(--text2) !important;
}

/* ── 알림창(Warning, Info 등) 텍스트 가독성 보호 ── */
div[data-testid="stAlert"] p, div[data-testid="stAlert"] span {
  color: #111111 !important;
}
</style>
"""


# ==============================
# 3. [View 1] 포털 메인 화면
# ==============================
if st.session_state.page_view == "portal":
    st.markdown(PORTAL_CSS, unsafe_allow_html=True)
    market = load_db(MARKET_FILE, {})

    # ── 최상단 HUD ──
    try:
        _stats   = load_stats()
        _today   = datetime.now(KST).strftime("%Y-%m-%d")
        _online  = get_online_users()
        _today_v = len(_stats.get("daily_visitors", {}).get(_today, []))
        _users_db_for_stats = load_db(USERS_FILE, {})
        _total_s = len([u for u in _users_db_for_stats if u != "admin"])
    except:
        _online, _today_v, _total_s = 0, 0, 0

    hud_user_txt = f"👤 {st.session_state.logged_in_user}님 접속 중" if st.session_state.get('logged_in_user') else "🔒 비로그인"
    st.markdown(f"""
    <div class='portal-bg'></div>
    <div class='top-hud'>
      <div class='hud-brand'>HYOMIN PORTAL</div>
      <div class='hud-live'><div class='hud-dot'></div> LIVE · 접속자 {_online}명</div>
      <div class='hud-season'>🏆 시즌 1 진행 중</div>
      <div style='color:var(--text2);font-size:0.78rem;'>{hud_user_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 로그인/로그아웃 버튼 ──
    col_empty, col_btn = st.columns([8, 2])
    with col_btn:
        if st.session_state.get('logged_in_user'):
            if st.button("🚪 로그아웃", use_container_width=True):
                sync_user_data(); st.session_state.clear(); st.rerun()
        else:
            if st.button("🔑 로그인 / 회원가입", use_container_width=True):
                st.session_state.page_view = "login"; st.rerun()

    # ── 히어로 섹션 ──
    st.markdown("""
    <div class='hero'>
      <div class='hero-eyebrow'>POWERED BY AI · BUILT FOR YOU</div>
      <div class='hero-title'>HYOMIN PORTAL</div>
      <p class='hero-sub'>
        하나의 계정으로 효민 유니버스의 모든 경제, 엔터테인먼트,<br>
        AI 학습, 커뮤니티 서비스를 통합 이용하세요.
      </p>
      <div class='hero-badge'>🛡️ HYOMIN NETWORKS SECURE PLATFORM · 시즌 1 신규 가입 시 5억 지급</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 실시간 스크롤 태그 배너 ──
    tags_html = ""
    tags = [
        ("🔥 HOT", "hot"),  ("🌌 유니버스 시즌1 개막", "live"), ("🤖 AI 모의고사", "new"),
        ("🏆 랭킹 1위 쟁탈전", "gold"), ("⚔️ 던전 런 REBORN", "hot"), ("🎲 인베스트 마블", "gold"),
        ("💻 THE TERMINAL", "new"), ("🗳️ 월드 배틀", "live"), ("💰 초기 정착금 5억", "gold"),
        ("📈 주식·코인·부동산", "live"), ("🎰 카지노 & 게임", "hot"), ("🏎️ 하이퍼카 레이싱", "new"),
    ]
    for label, cls in tags * 2:
        tags_html += f"<span class='scroll-tag {cls}'>{label}</span>"
    st.markdown(f"<div class='banner-scroll-wrap'><div class='banner-scroll-track'>{tags_html}</div></div>", unsafe_allow_html=True)

    # ── 실시간 통계 위젯 ──
    try:
        _prices = {k: v['price'] for k, v in market.get('stock_data', {}).items()}
        _top_nw = 0
        _top_uid = "—"
        for _u, _udata in _users_db_for_stats.items():
            if _u == "admin": continue
            _w = _udata.get('cash', 0) - _udata.get('loan', 0)
            for _sid, _pd in _udata.get('portfolio', {}).items():
                if _sid in _prices: _w += _pd.get('qty', 0) * _prices[_sid]
            for _cid, _ci in _udata.get('crypto_portfolio', {}).items():
                _w += _ci.get('qty', 0) * market.get('crypto_data', {}).get(_cid, {}).get('price', 0)
            for _eid, _cnt in _udata.get('real_estate', {}).items():
                if _eid in estate_config: _w += estate_config[_eid]['base_price'] * _cnt * 0.8
            _wlv = _udata.get('weapon_level', 0)
            if _wlv > 0 and _wlv in FORGE_DATA: _w += FORGE_DATA[_wlv]['sell']
            if _w > _top_nw:
                _top_nw = _w
                _top_uid = _u
        _nw_str = format_korean_money(_top_nw) if _top_nw > 0 else "0원"
    except:
        _top_uid, _nw_str = "집계 중", "—"

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card online">
        <div class="stat-icon">🟢</div>
        <div class="stat-value">{_online}</div>
        <div class="stat-label">지금 접속 중</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-value">{_today_v}</div>
        <div class="stat-label">오늘 방문자</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-value">{_total_s}</div>
        <div class="stat-label">누적 가입자</div>
      </div>
      <div class="stat-card volume">
        <div class="stat-icon">👑</div>
        <div class="stat-value">{_nw_str}</div>
        <div class="stat-label">자산1위: {_top_uid}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='game-section-title'>🎮 서비스 입장</div>", unsafe_allow_html=True)

    # ── 게임 카드 그리드 ──
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class='game-card card-universe'>
          <div class='card-badge badge-live'>🔴 LIVE</div>
          <div class='card-icon'>🌌</div>
          <div class='card-title'>HYOMIN UNIVERSE</div>
          <div class='card-desc'>자본주의 생존 시뮬레이션 시즌 1<br>주식·코인·부동산·게임 통합 경제</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("유니버스 입장 🚀", use_container_width=True, key="btn_uni"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "universe"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

        st.markdown("""
        <div class='game-card card-battle' style='margin-top:16px;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          <div class='card-icon'>🗳️</div>
          <div class='card-title'>WORLD BATTLE</div>
          <div class='card-desc'>실시간 진영 투표 배틀<br>오늘의 질문에 참전하라!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("지금 투표하기 ⚔️", use_container_width=True, key="btn_battle"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_b"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='game-card card-academy'>
          <div class='card-badge badge-new'>✨ NEW</div>
          <div class='card-icon'>🧠</div>
          <div class='card-title'>AI 아카데미</div>
          <div class='card-desc'>AI가 만드는 무한 모의고사<br>Gemini 2.5 Flash 탑재</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("AI 아카데미 입장 📚", use_container_width=True, key="btn_acad"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_a"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

        st.markdown("""
        <div class='game-card card-marble' style='margin-top:16px;'>
          <div class='card-badge badge-gold'>🏆 PICK</div>
          <div class='card-icon'>🎲</div>
          <div class='card-title'>인베스트 마블</div>
          <div class='card-desc'>AI 봇과 보드게임 대결<br>집·호텔·저당·무인도 전략</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎲 마블 입장", use_container_width=True, key="btn_marble"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_d"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    with col3:
        st.markdown("""
        <div class='game-card card-terminal'>
          <div class='card-badge badge-new'>💡 도전</div>
          <div class='card-icon'>💻</div>
          <div class='card-title'>THE TERMINAL</div>
          <div class='card-desc'>커맨드라인 방탈출 어드벤처<br>20 스테이지 · 타임어택 모드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("터미널 접속 >_", use_container_width=True, key="btn_term"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_c"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

        st.markdown("""
        <div class='game-card card-dungeon' style='margin-top:16px;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          <div class='card-icon'>⚔️</div>
          <div class='card-title'>던전 런 REBORN</div>
          <div class='card-desc'>뱀서라이크 서바이벌 던전<br>4 클래스 · 웨이브 보스 격파</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("던전 입장 ⚔️", use_container_width=True, key="btn_dungeon"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_e"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    # ── 신규 게임 행 ──────────────────────────────────────────
    st.markdown("<div class='game-section-title'>🆕 신규 게임 추가</div>", unsafe_allow_html=True)
    nc1, nc2, nc3, nc4 = st.columns(4)

    with nc1:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(0,212,255,0.4);min-height:180px;'>
          <div class='card-badge badge-new'>🆕 NEW</div>
          <div class='card-icon'>🏎️</div>
          <div class='card-title'>네온 도주 레이싱</div>
          <div class='card-desc'>5레인 무한 도로 · 니트로 부스터<br>경찰 추격 · ×8 콤보 시스템</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("레이싱 입장 🏎️", use_container_width=True, key="btn_f"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_f"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    with nc2:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(255,34,68,0.4);min-height:180px;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          <div class='card-icon'>🧟</div>
          <div class='card-title'>좀비 아포칼립스</div>
          <div class='card-desc'>탑다운 좀비 슈터 · 4종 무기<br>웨이브 + 상점 업그레이드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("생존 입장 🧟", use_container_width=True, key="btn_g"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_g"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    with nc3:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(192,79,255,0.4);min-height:180px;'>
          <div class='card-badge' style='background:rgba(192,79,255,0.2);color:#c04fff;border:1px solid rgba(192,79,255,0.4);'>⚡ PVP</div>
          <div class='card-icon'>🥊</div>
          <div class='card-title'>스트리트 파이터 EX</div>
          <div class='card-desc'>1v1 격투 · 6 캐릭터 · AI CPU<br>필살기 · 슈퍼 게이지 · 3라운드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("대전 입장 🥊", use_container_width=True, key="btn_h"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_h"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    with nc4:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(0,255,136,0.4);min-height:180px;'>
          <div class='card-badge' style='background:rgba(0,255,136,0.15);color:#00ff88;border:1px solid rgba(0,255,136,0.35);'>🎯 ELITE</div>
          <div class='card-icon'>🎯</div>
          <div class='card-title'>스나이퍼 엘리트 ULTRA</div>
          <div class='card-desc'>6 미션 · 야간작전 포함<br>콤보·헤드샷·바람탄도·미니맵</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("임무 입장 🎯", use_container_width=True, key="btn_i"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_i"
            else:
                st.warning("⚠️ 로그인이 필요합니다.")
                time.sleep(0.8); st.session_state.page_view = "login"
            st.rerun()

    # ── 시스템 공지 & 아키텍처 섹션 ───────────────────────
    with st.expander("📋 시스템 공지 & 전체 아키텍처 구조 보기", expanded=False):

        st.markdown("""
<div class="arch-highlight">
    <p>🔧 시스템 대공사 및 재시작 안내</p>
    <p class="sub">
        데이터베이스를 외부 클라우드(MongoDB Atlas)로 완벽 분리하고,
        <b>38개 모듈화 설계</b>를 적용하여 서버 안정성을 극대화했습니다.
        유저 자산은 이제 영구히 안전합니다.
    </p>
</div>
<div class="arch-highlight" style="border-left-color:#00ff88; background: linear-gradient(90deg, rgba(0,255,136,0.08), rgba(0,212,255,0.06));">
    <p style="color:#00ff88 !important;">🌟 정규 시즌 1 공식 개막</p>
    <p class="sub">
        <b>[시즌 기간]</b> 2026년 4월 15일 ~ 5월 15일<br>
        새로운 시즌의 시작을 기념하여 모든 시민께 <b>초기 정착금 5억 원</b>을 즉시 지급합니다!
    </p>
</div>
<div class="arch-highlight" style="border-left-color:#c04fff; background: linear-gradient(90deg, rgba(192,79,255,0.08), rgba(108,99,255,0.06));">
    <p style="color:#c04fff !important;">🎮 게임 패치노트 (2026.05.07)</p>
    <p class="sub">
        <b>🎯 스나이퍼 엘리트 ULTRA 대업그레이드</b><br>
        · <b>6미션 체제</b> — 야간 특수작전(6스테이지) 신규 추가<br>
        · <b>콤보 시스템</b> — 연속 킬 시 최대 ×10 점수 배율 적용<br>
        · <b>헤드샷 시스템</b> — 헤드샷 판정 시 2배 데미지 + 💀 연출<br>
        · <b>파티클 엔진</b> — 혈흔·폭발·총구화염·탄환궤적 전면 적용<br>
        · <b>미니맵</b> — 우하단 실시간 아군/적/탄환 위치 표시<br>
        · <b>탄창 시각화</b> — 개별 황동 탄환 핍 UI로 교체<br>
        · <b>Web Audio API</b> — 총성·재장전·보스킬 사운드 레이어드 추가<br>
        · <b>스코프 업그레이드</b> — 밀도트 + 노이즈 그레인 + 야시경 필터<br><br>
        <b>💻 THE TERMINAL</b><br>
        · <b>20 스테이지 완성</b> — stage 15~20 SyntaxError 버그 수정 및 정식 해금<br>
        · <b>타임어택 모드</b> — 전체 20스테이지 최속 클리어 도전 모드 추가<br>
        · Enter키 즉시 제출(chat_input) 방식으로 UX 개선<br><br>
        <b>🎮 전체 공통</b><br>
        · 포털 카드 최신 게임 정보 반영 업데이트
    </p>
</div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏗️ SYSTEM ARCHITECTURE & MODULES")
        st.markdown("---")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
<div class="arch-card">
    <h4>🗄️ 데이터베이스 — MongoDB Atlas</h4>
    <p>
        모든 유저 자산 및 시장 데이터는 <b>MongoDB Atlas 클라우드</b>에 실시간 저장됩니다.
        로컬 JSON 파일 의존을 완전히 탈피하여, 서버 재시작과 무관하게 데이터가 영구 보존됩니다.
        비밀번호는 <b>bcrypt 단방향 해시</b>로 암호화되어 원문 복원이 불가능합니다. (레거시 SHA-256 → 로그인 시 자동 마이그레이션)
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">MongoDB Atlas</span>
        <span class="arch-badge">bcrypt 암호화</span>
        <span class="arch-badge">실시간 백업</span>
        <span class="arch-badge">utils/database.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🧩 38개 독립 모듈 구조</h4>
    <p>
        전체 시스템은 <b>1개의 진입점(app.py)</b>과 <b>38개의 독립 모듈</b>로 구성됩니다.
        각 기능(주식, 코인, 부동산, 미니게임 등)이 완전히 분리되어 있어,
        한 모듈의 오류가 전체 서비스에 영향을 주지 않습니다.
        유지보수 및 신규 기능 추가가 용이한 구조입니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">app.py (진입점)</span>
        <span class="arch-badge">pages/ (27개 페이지)</span>
        <span class="arch-badge">utils/ (5개 유틸)</span>
        <span class="arch-badge">독립 렌더링</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🔐 보안 & 접근 제어</h4>
    <p>
        로그인 5회 실패 시 30초 잠금이 적용되는 <b>Brute-force 방어</b> 시스템을 내장합니다.
        관리자 계정은 별도의 <b>하드코딩 해시</b>로 보호되며, DB에 평문이 저장되지 않습니다.
        VIP 라운지는 순자산 1,000억 이상 또는 관리자만 접근 가능한 권한 제어가 적용됩니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">Brute-force 방어</span>
        <span class="arch-badge">관리자 분리</span>
        <span class="arch-badge">VIP 권한 제어</span>
        <span class="arch-badge">utils/core.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown("""
<div class="arch-card">
    <h4>⏱️ 자동 시장 동기화 — Market Sync</h4>
    <p>
        유저가 접속하지 않는 동안에도 <b>시간 슬롯 기반 자동 계산</b>이 작동합니다.
        주가 변동, 은행 이자, 부동산 임대료가 실시간으로 누적됩니다.
        접속 시 경과 시간만큼의 모든 변화가 한 번에 정확하게 반영됩니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">utils/market_sync.py</span>
        <span class="arch-badge">주가 자동변동</span>
        <span class="arch-badge">이자 자동계산</span>
        <span class="arch-badge">임대료 자동누적</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🌐 멀티 서비스 포털 구조</h4>
    <p>
        <b>HYOMIN PORTAL</b>은 단일 앱 안에서 여러 독립 서비스를 라우팅하는 구조입니다.
        효민 유니버스(경제 시뮬레이션), AI 아카데미(모의고사), 월드 배틀(투표),
        THE TERMINAL(방탈출) 등 각 서비스가 하나의 계정으로 통합 이용 가능합니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">단일 계정 통합</span>
        <span class="arch-badge">뷰 기반 라우팅</span>
        <span class="arch-badge">세션 상태 공유</span>
        <span class="arch-badge">app.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>📊 실시간 통계 & 온라인 감지</h4>
    <p>
        접속자 수는 <b>last_seen 타임스탬프</b> 기반으로 5분 이내 활성 유저를 집계합니다.
        일별 방문자, 누적 가입자, 거래량 통계는 MongoDB stats 컬렉션에 별도 저장됩니다.
        포털 메인 화면에서 실시간으로 서버 현황을 확인할 수 있습니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">last_seen 감지</span>
        <span class="arch-badge">일별 방문자 집계</span>
        <span class="arch-badge">거래량 추적</span>
        <span class="arch-badge">utils/core.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

        st.markdown("#### 📦 전체 모듈 목록")
        st.markdown("""
<div class="module-grid">
    <div class="module-item"><strong>app.py</strong>진입점·라우터·로그인·뷰 전환</div>
    <div class="module-item"><strong>utils/database.py</strong>MongoDB 연결·CRUD·stats 관리</div>
    <div class="module-item"><strong>utils/core.py</strong>해시·포맷·순자산·세션 동기화</div>
    <div class="module-item"><strong>utils/market_sync.py</strong>주가·코인·이자·임대료 자동동기화</div>
    <div class="module-item"><strong>utils/config.py</strong>종목·부동산·강화 설정 상수</div>
    <div class="module-item"><strong>utils/css.py</strong>유니버스 글로벌 다크 테마 CSS</div>
    <div class="module-item"><strong>pages/home.py</strong>홈 광장·튜토리얼·성장 목표</div>
    <div class="module-item"><strong>pages/stock.py</strong>주식 트레이딩·차트·매수매도</div>
    <div class="module-item"><strong>pages/crypto.py</strong>코인 거래소·실시간 시세</div>
    <div class="module-item"><strong>pages/real_estate.py</strong>부동산 매입·임대료 수익</div>
    <div class="module-item"><strong>pages/bank.py</strong>대출·송금·이자 계산</div>
    <div class="module-item"><strong>pages/txlog.py</strong>개인 거래 내역 조회</div>
    <div class="module-item"><strong>pages/ranking.py</strong>시즌1 랭킹·게시판</div>
    <div class="module-item"><strong>pages/clan.py</strong>길드·클랜 시스템</div>
    <div class="module-item"><strong>pages/dm.py</strong>개인 쪽지·읽음 표시</div>
    <div class="module-item"><strong>pages/quest.py</strong>일일 퀘스트·보상</div>
    <div class="module-item"><strong>pages/title_shop.py</strong>칭호 상점·장착</div>
    <div class="module-item"><strong>pages/vip.py</strong>VIP 전용 라운지</div>
    <div class="module-item"><strong>pages/games/slot.py</strong>럭키 슬롯머신</div>
    <div class="module-item"><strong>pages/games/blackjack.py</strong>블랙잭 카지노</div>
    <div class="module-item"><strong>pages/games/holdem.py</strong>텍사스 홀덤</div>
    <div class="module-item"><strong>pages/games/mine.py</strong>광산 노가다</div>
    <div class="module-item"><strong>pages/games/quiz.py</strong>사주팔</div>
    <div class="module-item"><strong>pages/games/lotto.py</strong>글로벌 로또</div>
    <div class="module-item"><strong>pages/games/forge.py</strong>전설의 명검 강화</div>
    <div class="module-item"><strong>pages/games/gacha.py</strong>가챠 뽑기</div>
    <div class="module-item"><strong>pages/sports/soccer_sim.py</strong>구단주 시뮬레이터</div>
    <div class="module-item"><strong>pages/sports/penalty.py</strong>조기축구 승부차기</div>
    <div class="module-item"><strong>pages/sports/racing.py</strong>하이퍼카 레이싱</div>
    <div class="module-item"><strong>pages/sports/garage.py</strong>커스텀 튜닝 차고지</div>
    <div class="module-item"><strong>pages/admin/panel.py</strong>창조주 통제소 (관리자 전용)</div>
    <div class="module-item"><strong>pages/project_a.py</strong>AI 무한 모의고사</div>
    <div class="module-item"><strong>pages/project_b.py</strong>월드 배틀</div>
    <div class="module-item"><strong>pages/project_d.py</strong>🎲 인베스트 마블 보드게임</div>
    <div class="module-item"><strong>pages/project_e.py</strong>⚔️ 뱀서라이크 던전 게임</div>
    <div class="module-item"><strong>pages/project_f.py</strong>🏎️ 네온 도주 레이싱</div>
    <div class="module-item"><strong>pages/project_g.py</strong>🧟 좀비 아포칼립스 슈터</div>
    <div class="module-item"><strong>pages/project_h.py</strong>🥊 스트리트 파이터 EX</div>
    <div class="module-item"><strong>pages/project_i.py</strong>🎯 스나이퍼 엘리트 ULTRA</div>
</div>
        """, unsafe_allow_html=True)

    # ── 전체 서비스 완전 가이드 ──────────────────────────────
    with st.expander("📖 전체 서비스 완전 가이드 보기", expanded=False):

        st.markdown("### 🗺️ HYOMIN PORTAL — 서비스 소개")
        st.markdown("---")

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("""
<div class="arch-card">
    <h4>🌌 유니버스 — 자본주의 생존 시뮬레이션</h4>
    <p>
        효민 유니버스는 <b>현실과 동일한 자본주의 경제 시스템</b>을 체험하는 경제 시뮬레이션입니다.
        가입 즉시 <b>초기 정착금 5억 원</b>이 지급되며, 주식·코인·부동산·은행 등
        다양한 금융 수단으로 자산을 불려 나갈 수 있습니다.
        랭킹 시스템, 클랜, 일일 퀘스트, 미니게임, VIP 라운지까지 갖춘 풀 스케일 경제 세계입니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">📈 주식 트레이딩</span>
        <span class="arch-badge">₿ 코인 거래소</span>
        <span class="arch-badge">🏠 부동산 임대</span>
        <span class="arch-badge">🏦 대출·이자</span>
        <span class="arch-badge">🏆 시즌 랭킹</span>
        <span class="arch-badge">⚔️ 클랜 시스템</span>
        <span class="arch-badge">🎰 미니게임 8종</span>
        <span class="arch-badge">🚀 시즌 1 진행 중</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,212,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--cyan) !important;font-weight:700;">💡 입문 가이드</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① 로그인 후 유니버스 입장 → ② 홈 광장에서 튜토리얼 확인 → ③ 주식/코인 소액 매수로 시작
            → ④ 일일 퀘스트 완료로 보너스 획득 → ⑤ 부동산 매입으로 패시브 수익 확보
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🧠 AI 무한 모의고사 — AI 아카데미</h4>
    <p>
        공부한 내용을 붙여넣기하거나 PDF/TXT 파일을 업로드하면,
        <b>Gemini AI</b>가 실제 시험 스타일의 문제를 무한으로 생성해 드립니다.
        문제 수(5~20개), 난이도(쉬움/보통/어려움), 문제 유형(4지선다/단답형/O×)을 자유롭게 설정할 수 있으며,
        채점 후 <b>오답 자동 분석 및 재출제</b> 기능을 제공합니다.
        시험, 수능, 자격증 등 모든 분야에 활용 가능합니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🤖 Gemini 2.5 Flash</span>
        <span class="arch-badge">📄 PDF/TXT 업로드</span>
        <span class="arch-badge">🎚️ 난이도 3단계</span>
        <span class="arch-badge">✏️ 3가지 문제 유형</span>
        <span class="arch-badge">📊 오답 분석</span>
        <span class="arch-badge">🔁 오답 재출제</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 사용법</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① AI 아카데미 입장 → ② 학습 내용 직접 입력 또는 파일 업로드 → ③ 문제 수·난이도·유형 설정
            → ④ 문제 생성 → ⑤ 풀기 → ⑥ 채점 및 오답 확인 → ⑦ 오답만 재출제
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🎲 인베스트 마블 — 보드게임</h4>
    <p>
        모노폴리에서 영감을 받은 <b>투자형 보드게임</b>입니다.
        AI 봇과 함께 주사위를 굴리며 전 세계 랜드마크 부지를 매입하고,
        <b>집→호텔</b>을 건설해 임대료 수익을 올립니다.
        저당 설정으로 급전을 마련하거나, 무인도에 갇혀 탈출을 시도하는 등
        다이나믹한 경제 전략이 필요한 게임입니다.
        화려한 3D 스타일 UI와 애니메이션이 적용된 풀 HTML 게임입니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🗺️ 세계 랜드마크 보드</span>
        <span class="arch-badge">🤖 AI 봇 대전</span>
        <span class="arch-badge">🏠 집·호텔 건설</span>
        <span class="arch-badge">⛓️ 저당·경매</span>
        <span class="arch-badge">🏝️ 무인도 탈출</span>
        <span class="arch-badge">🎴 이벤트 카드</span>
    </div>
    <div style="margin-top:10px;background:rgba(255,215,0,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--gold) !important;font-weight:700;">💡 전략 팁</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            같은 색 부지 독점 시 임대료 2배. 무인도 탈출은 주사위 더블 or 탈출 카드 사용.
            현금이 부족할 땐 호텔을 팔거나 저당을 설정해 버텨라.
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_g2:
            st.markdown("""
<div class="arch-card">
    <h4>🗳️ 월드 배틀 — 실시간 진영 투표</h4>
    <p>
        매일 새로운 <b>오늘의 질문</b>이 올라오면, A 진영 또는 B 진영 중 하나를 선택해 투표합니다.
        실시간으로 전체 투표 현황과 진영별 비율이 배틀 바를 통해 시각화되며,
        투표 후 다른 시민들의 댓글도 확인할 수 있습니다.
        관리자가 주제·기간·진영 이름을 자유롭게 설정하고, 종료된 투표는 히스토리로 보존됩니다.
        완전 익명으로 진행되며 계정당 1표만 허용됩니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🔵🔴 2진영 배틀</span>
        <span class="arch-badge">📊 실시간 비율 바</span>
        <span class="arch-badge">💬 투표 후 댓글</span>
        <span class="arch-badge">🕵️ 완전 익명</span>
        <span class="arch-badge">⏱️ 마감 카운트다운</span>
        <span class="arch-badge">📜 히스토리 보존</span>
    </div>
    <div style="margin-top:10px;background:rgba(108,99,255,0.1);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--accent) !important;font-weight:700;">💡 참여 방법</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① 로그인 후 월드 배틀 입장 → ② 오늘의 질문 확인 → ③ 원하는 진영 버튼 클릭
            → ④ 투표 완료 후 비율 확인 → ⑤ 댓글로 의견 남기기 (마감 후 결과 공개)
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>💻 THE TERMINAL — 방탈출</h4>
    <p>
        오직 <b>커맨드라인 명령어</b>만으로 단서를 추적해 방을 탈출하는 해킹 어드벤처 게임입니다.
        총 <b>20개의 스테이지</b>로 구성되며, 각 스테이지마다 독립된 가상 파일시스템이 펼쳐집니다.
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cat</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cd</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">decode</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">rot13</code> 등
        실제 터미널 명령어와 유사한 커맨드를 입력해 숨겨진 비밀번호를 찾아야 합니다.
        단계별 3개의 힌트가 제공되며, 모든 스테이지를 클리어하면 <b>타임어택 모드</b>가 해금됩니다.
        스테이지 클리어 시 보상금이 지급되고 전체 클리어 시 특별 칭호가 부여됩니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🖥️ 20 STAGES</span>
        <span class="arch-badge">📁 가상 파일시스템</span>
        <span class="arch-badge">⌨️ 실제 CLI 명령어</span>
        <span class="arch-badge">🔐 SHA-256 정답 검증</span>
        <span class="arch-badge">💡 단계별 3힌트</span>
        <span class="arch-badge">⏱️ 타임어택 모드</span>
        <span class="arch-badge">💰 클리어 보상금</span>
        <span class="arch-badge">⭐~⭐⭐⭐⭐⭐ 난이도</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 기본 명령어</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls</code> 파일 목록 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls -a</code> 숨김파일 포함 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cat [파일]</code> 내용 보기 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cd [경로]</code> 디렉토리 이동 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">decode [문자열]</code> base64 해독 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">unlock [정답]</code> 잠금 해제
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left: 3px solid #c04fff;">
    <h4 style="color:#c04fff !important;">⚔️ 던전 런 2.5D — SURVIVORS REBORN</h4>
    <p>
        사방에서 끝없이 몰려오는 몬스터들을 쓸어버리는 <b>본격 뱀서라이크(서바이벌)</b> 게임입니다.
        화려한 <b>2.5D 입체 그래픽</b>과 함께 적의 웨이브를 돌파하고 보스를 격파하세요.
        <b style="color:#ff3366;">레벨업 시 등장하는 무기와 패시브를 조합해 극한의 시너지를 완성하세요!</b><br>
        <b>전사·마법사·궁수·닌자</b> 4개의 고유 클래스, 몰입감 넘치는 타격감, 그리고 강력한 웨이브 보스들이 기다립니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🌪️ 뱀서라이크 서바이벌</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🧊 2.5D 입체 그래픽</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">⚔️ 자동 공격 & 핵앤슬래시</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🃏 무기/스킬 조합</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">👹 웨이브 보스전</span>
    </div>
    <div style="margin-top:10px;background:rgba(192,78,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#c04fff !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">W A S D</code> 또는
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">↑↓←→</code> 상하좌우 이동 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">자동</code> 기본 공격 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">Q E R</code> 액티브 스킬 사용 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">마우스</code> 캐릭터 및 능력 선택
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        # ── 신규 게임 4종 가이드 ────────────────────────────────
        st.markdown("### 🎮 신규 게임 4종 가이드")
        st.markdown("---")

        col_ng1, col_ng2 = st.columns(2)

        with col_ng1:
            st.markdown("""
<div class="arch-card" style="border-left-color:#00d4ff;">
    <h4 style="color:#00d4ff !important;">🏎️ 네온 도주 레이싱 &#8212; NEON RUNAWAY</h4>
    <p>
        5레인 무한 도로를 달리며 경찰 추격을 뿌리치는 하이스피드 레이싱 게임입니다.
        레인을 빠르게 전환하며 장애물을 피하고, 니트로 부스터로 화려한 스피드를 폭발시키세요.
        연속 회피로 콤보가 상승하며, 최대 ×8 콤보로 점수를 높여보세요.
        경찰 수는 파도비로 늘수록 더 터프해집니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">🛣️ 5레인 무한 도로</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">⚡ 니트로 부스터</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">🚨 경찰 추격 웨이브</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">×8 콤보 시스템</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,212,255,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--cyan) !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            PC: <code style="background:rgba(0,212,255,0.15);padding:1px 5px;border-radius:3px;">←→ 방향키</code> 레인 전환 &nbsp;
            <code style="background:rgba(0,212,255,0.15);padding:1px 5px;border-radius:3px;">Space</code> 니트로 &nbsp;|&nbsp;
            모바일: D-PAD + NITRO 버튼 지원
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left-color:#ff2244;">
    <h4 style="color:#ff2244 !important;">🧟 좀비 아포칼립스 &#8212; ZOMBIE APOCALYPSE</h4>
    <p>
        탑다운 시점의 시가지 맵에서 철연같이 몰려드는 좀비를 생존하는 싸일법 슈터입니다.
        새로운 웨이브마다 상점에서 코인으로 <b>무기 업그레이드</b>와 <b>탄약 보충</b>을 하며,
        권총·라이플·샷건·섬광백열 4종 무기를 스위칭할 수 있습니다.
        보스 좀비가 등장하는 매 5라운드를 버티세요.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🎯 탑다운 슈터</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🔫 4종 무기 시스템</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🛒 라운드간 상점</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🧟‍♂️ 보스 좀비</span>
    </div>
    <div style="margin-top:10px;background:rgba(255,34,68,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#ff2244 !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            PC: <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">WASD</code> 이동 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">마우스</code> 조준·사격 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">R</code> 재장전 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">1-4</code> 무기 교체 &nbsp;|&nbsp; 모바일: 조이스틱 + 발사 버튼
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_ng2:
            st.markdown("""
<div class="arch-card" style="border-left-color:#c04fff;">
    <h4 style="color:#c04fff !important;">🥊 스트리트 파이터 EX &#8212; STREET FIGHTER EX</h4>
    <p>
        <b>6가지 고유 캐릭터</b>(전사/파이터/닌자/모헨/닉느/고스트) 중 하나를 선택해 AI CPU와 1v1 대결하는 게임입니다.
        각 캐릭터마다 고유한 필살기와 <b>슈퍼 게이지</b>가 있으며,
        3라운드 선승일경식으로 진행됩니다.
        콤보 파출로 슈퍼게이지를 치는 초리한 파이널 필살기를 시전하세요!
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🎮 6캐릭터 대전</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">⚡ 슈퍼 게이지</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🔥 필살기 파이니슬</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🏆 3라운드 선승</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">👥 2P 대전 모드</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🗺️ 8스테이지 아케이드</span>
    </div>
    <div style="margin-top:10px;background:rgba(192,79,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#c04fff !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            🎮 <b>P1:</b> <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">A D</code> 이동 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">W</code> 점프 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">S</code> 가드 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">Z</code> 펀치 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">X</code> 킥 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">C</code> 강공격 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">V</code> 필살기 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">F</code> 슈퍼기술<br>
            🕹️ <b>P2:</b> <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">← →</code> 이동 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">↑</code> 점프 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">↓</code> 가드 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">1</code> 펀치 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">2</code> 킥 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">3</code> 강공격 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">4</code> 필살기 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">5</code> 슈퍼기술 &nbsp;|&nbsp; 모바일: D-PAD + 공격버튼
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left-color:#00ff88;">
    <h4 style="color:#00ff88 !important;">🎯 스나이퍼 엘리트 ULTRA &#8212; WAR SNIPER</h4>
    <p>
        전장의 저격수가 되어 6개의 미션을 완수하는 본격 스나이퍼 시뮬레이션입니다.
        실제 바람 탄도 물리가 적용되어 풍향·풍속에 따라 탄환이 휘며,
        <b>헤드샷</b> 판정 시 2배 데미지와 함께 💀 연출이 등장합니다.
        <b>콤보 시스템</b>(×10까지)으로 연속 킬 시 점수 배율이 상승하고,
        6스테이지는 <b>야간 특수작전</b>으로 야시경 스코프를 사용합니다.
        파티클 엔진, 미니맵, Web Audio 사운드, 탄창 시각화 UI까지 완비된 게임입니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🔭 3.5x~5x 배율 스코프</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🌬️ 바람 탄도 물리</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">💀 헤드샷 시스템</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🔥 ×10 콤보</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🌙 야간 6스테이지</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🗺️ 실시간 미니맵</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">S~D 등급 평가</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">클릭/Space</code> 발사 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">우클릭/Z</code> 스코프 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">Shift</code> 숨참기 안정 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">R</code> 재장전 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ESC</code> 타이틀
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class='portal-footer'>
      <p>ⓒ 2026 HYOMIN PORTAL INC. · Powered by AI & Vibe Coding</p>
      <p style='margin-top:6px;font-size:0.7rem;'>Built with Claude · MongoDB Atlas · Streamlit · Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ==============================
# 4. [View 2] 로그인 / 회원가입
# ==============================
elif st.session_state.page_view == "login":
    st.markdown(PORTAL_CSS, unsafe_allow_html=True)
    st.markdown("<div class='portal-bg'></div>", unsafe_allow_html=True)

    if st.button("🔙 포털 메인으로"):
        st.session_state.page_view = "portal"; st.rerun()

    st.markdown("""
    <div style='text-align:center;padding:40px 0 20px;'>
      <div style='font-family:"Orbitron",sans-serif;font-size:1.8rem;font-weight:900;
        background:linear-gradient(135deg,#6c63ff,#00d4ff);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;letter-spacing:3px;'>HYOMIN ID</div>
      <p style='color:#8899bb;margin-top:8px;'>안전한 서비스 이용을 위해 로그인해주세요.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])

        with tabs[0]:
            st.markdown("""
<div style='background:rgba(255,200,0,0.1);border:1px solid #FFD600;border-radius:10px;padding:14px;margin-bottom:16px;'>
  <div style='color:#FFD600;font-weight:900;font-size:1rem;'>📢 공지사항</div>
  <div style='color:#E2E8F0;font-size:0.9rem;margin-top:6px;'>
    서버 점검으로 인해 <b>모든 계정의 비밀번호가 1234로 초기화</b>되었습니다.<br>
    로그인 후 <b>🏠 홈 광장</b>에서 비밀번호를 변경해주세요.
  </div>
</div>
""", unsafe_allow_html=True)
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

            if st.button("🚀 로그인 및 계속하기", use_container_width=True):
                users = load_db(USERS_FILE, {})

                # ── DB 기반 로그인 잠금 확인 ──────────────────────────────
                if l_id and l_id in users:
                    _fails, _lock_until = get_login_lock(l_id)
                else:
                    # 없는 아이디는 세션으로만 임시 추적 (brute-force 방어)
                    _fails      = st.session_state.get('_anon_fails', 0)
                    _lock_until = st.session_state.get('_anon_lock', 0)

                if time.time() < _lock_until:
                    _remain = int(_lock_until - time.time())
                    st.error(f"🔒 로그인 시도 초과. {_remain}초 후 다시 시도하세요.")
                    st.stop()

                # ── 관리자 로그인 (SHA-256 유지) ─────────────────────────
                if l_id == "admin" and hash_pw(l_pw) == ADMIN_HASH:
                    if "admin" not in users:
                        users["admin"] = {"pw": ADMIN_HASH, "cash": 999_999_999_999,
                                          "inventory": [], "equipped_title": "👑 절대신 창조주"}
                        save_db(USERS_FILE, users)
                    _do_login("admin", users, device_mode)

                # ── 일반 유저 로그인 (bcrypt + 레거시 SHA-256 자동 마이그레이션) ──
                elif l_id != "admin" and l_id in users and verify_pw(l_pw, users[l_id]['pw']):
                    # 레거시 SHA-256 해시 감지 → 로그인 시점에 bcrypt로 자동 교체
                    if is_legacy_hash(users[l_id]['pw']):
                        users[l_id]['pw'] = hash_pw_bcrypt(l_pw)
                        save_db(USERS_FILE, users)
                    clear_login_lock(l_id)
                    _do_login(l_id, users, device_mode)

                # ── 로그인 실패 ───────────────────────────────────────────
                else:
                    _fails += 1
                    if l_id and l_id in users:
                        _lock_until_new = (time.time() + 30) if _fails >= 5 else 0.0
                        set_login_lock(l_id, _fails, _lock_until_new)
                    else:
                        st.session_state['_anon_fails'] = _fails
                        if _fails >= 5:
                            st.session_state['_anon_lock'] = time.time() + 30

                    if _fails >= 5:
                        st.error("🔒 로그인 5회 실패. 30초 후 다시 시도하세요.")
                    else:
                        st.error(f"❌ 아이디 또는 비밀번호가 올바르지 않습니다. (남은 시도: {5 - _fails}회)")

        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 계정 생성하기", use_container_width=True):
                users    = load_db(USERS_FILE, {})
                clean_id = n_id.strip()
                if not re.match(r'^[a-zA-Z0-9가-힣_]{2,20}$', clean_id):
                    st.error("⚠️ 아이디는 한글/영문/숫자/언더바(_)만 사용 가능하며 2~20자여야 합니다.")
                elif clean_id in users or clean_id == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(n_pw) < 1:
                    st.error("⚠️ 비밀번호를 입력해주세요.")
                else:
                    users[clean_id] = {
                        "pw": hash_pw_bcrypt(n_pw), "cash": 500_000_000, "inventory": [],
                        "equipped_title": "🌱 신규시민", "portfolio": {}, "real_estate": {},
                        "rent_time": time.time(), "loan": 0, "loan_time": time.time(),
                        "last_estate_reset": 0, "bulk_trade_date": "", "bulk_trade_count": 0,
                        "crypto_portfolio": {}, "daily_quests": {}, "weapon_level": 0,
                        "garage": {'cars': {}, 'active_tier': None},
                    }
                    save_db(USERS_FILE, users)
                    stats = load_stats()
                    stats["total_signups"] = stats.get("total_signups", 0) + 1
                    save_stats(stats)
                    st.success("🎉 가입 성공! 로그인 탭에서 로그인해주세요.")
    st.stop()


# ==============================
# 5. [View 3] 효민 유니버스
# ==============================
elif st.session_state.page_view == "universe":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    market = run_market_sync()
    if market.get("maintenance_mode") and st.session_state.logged_in_user != "admin":
        st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
        st.warning(f"🔧 {market.get('maintenance_msg', '현재 서버 점검 중입니다.')}")
        if st.button("🏠 포털 메인으로"):
            st.session_state.page_view = "portal"; st.rerun()
        st.stop()
    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()

    def _calc_nw_from_session(market_data):
        w = st.session_state.global_cash - st.session_state.loan
        prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
        for sid, p_data in st.session_state.portfolio.items():
            if sid in prices: w += p_data.get('qty', 0) * prices[sid]
        for cid, cinfo in st.session_state.get('crypto_portfolio', {}).items():
            w += cinfo.get('qty', 0) * market_data.get('crypto_data', {}).get(cid, {}).get('price', 0)
        for eid, count in st.session_state.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
        w_lv = st.session_state.get('weapon_level', 0)
        if w_lv > 0 and w_lv in FORGE_DATA: w += FORGE_DATA[w_lv]['sell']
        return w

    nw = _calc_nw_from_session(market)
    if st.session_state.loan > 0 and nw < 0:
        # 이전 칭호 저장 (신용불량자가 아닐 때만 저장)
        cur_title = st.session_state.equipped_title
        if cur_title != "💸 신용불량자":
            st.session_state['_pre_debt_title'] = cur_title
        st.session_state.equipped_title = "💸 신용불량자"
        sync_user_data()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"

    is_admin = st.session_state.logged_in_user == "admin"
    is_vip   = nw >= 100_000_000_000 or is_admin

    CATEGORY_MENUS = {
        "📈 경제":        ["🏠 홈 광장 (튜토리얼)", "📈 주식 트레이딩", "🪙 코인 거래소", "🏢 부동산 거래소", "🏦 은행 (대출/송금)", "📜 내 거래 기록"],
        "🎮 미니게임":    ["🎰 럭키 슬롯", "🃏 블랙잭 카지노", "⛏️ 광산 (노가다)", "🃏 텍사스 홀덤", "💻 사주팔자", "⚔️ 글로벌 로또", "🗡️ 전설의 명검 강화", "🎴 가챠 뽑기"],
        "🌟 성장 & 혜택": ["📅 일일 퀘스트", "👑 칭호 상점"],
        "⚽ 스포츠":      ["⚽ 구단주 시뮬레이터", "⚽ 조기축구 승부차기", "🏎️ 하이퍼카 레이싱", "🛠️ 커스텀 튜닝 차고지"],
        "👥 커뮤니티":    ["🏰 길드/클랜", "🏅 [시즌1]랭킹 & 게시판", "✉️ 개인 쪽지함"],
    }
    if is_vip:   CATEGORY_MENUS["📈 경제"].insert(1, "💎 VIP 라운지")
    if is_admin: CATEGORY_MENUS["⚙️ 관리"] = ["🛠️ 창조주 통제소"]

    def get_current_category():
        for cat, pages in CATEGORY_MENUS.items():
            if st.session_state.current_page in pages: return cat
        return list(CATEGORY_MENUS.keys())[0]

    if "current_category" not in st.session_state:
        st.session_state.current_category = get_current_category()

    msg_db_check = load_db(MESSAGES_FILE, {})
    my_unread  = sum(1 for m in msg_db_check.get(st.session_state.logged_in_user, {}).get("inbox", []) if not m.get("read", False))
    unread_txt = f" 🔴{my_unread}" if my_unread > 0 else ""
    is_pc_mode = "PC" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

    if is_pc_mode:
        with st.sidebar:
            st.markdown(f"<div style='padding:14px;background:rgba(255,255,255,0.05);border:1px solid #00E5FF;border-radius:10px;margin-bottom:14px;'><div style='color:#00E5FF;font-size:0.8rem;'>{st.session_state.equipped_title}</div><div style='font-size:1rem;font-weight:700;'>{st.session_state.logged_in_user}{unread_txt}</div></div>", unsafe_allow_html=True)
            st.metric("💵 현금",  format_korean_money(st.session_state.global_cash))
            st.metric("📊 순자산", format_korean_money(nw))
            st.write("---")
            for cat in CATEGORY_MENUS:
                if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                    st.session_state.current_category = cat
                    st.session_state.current_page = CATEGORY_MENUS[cat][0]; st.rerun()
            st.write("---")
            cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
            cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
            selected_menu = st.radio(f"{st.session_state.current_category} 메뉴", cur_cat_pages, index=cur_idx)
            if selected_menu != st.session_state.current_page:
                st.session_state.current_page = selected_menu; st.rerun()
            st.write("---")
            if st.button("로그아웃", use_container_width=True):
                sync_user_data(); st.session_state.clear(); st.rerun()
    else:
        c1, c2 = st.columns([3, 1])
        with c1: st.markdown(f"<div style='font-size:0.9rem;'>👤 <b>{st.session_state.logged_in_user}</b>{unread_txt} | <span style='color:#00E5FF;'>{st.session_state.equipped_title}</span><br>💵 {format_korean_money(st.session_state.global_cash)}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        cat_sel = st.selectbox("카테고리", list(CATEGORY_MENUS.keys()), index=list(CATEGORY_MENUS.keys()).index(st.session_state.current_category))
        if cat_sel != st.session_state.current_category:
            st.session_state.current_category, st.session_state.current_page = cat_sel, CATEGORY_MENUS[cat_sel][0]; st.rerun()
        cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
        cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
        selected_menu = st.selectbox("메뉴 선택", cur_cat_pages, index=cur_idx)
        if selected_menu != st.session_state.current_page:
            st.session_state.current_page = selected_menu; st.rerun()

    st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
    if market.get('admin_msg'):
        import html as _html_mod
        _safe_msg = _html_mod.escape(str(market['admin_msg']))
        _safe_color = _html_mod.escape(str(market.get('admin_color','#FF4B4B')))
        st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {_safe_color};border-radius:10px;padding:12px;color:{_safe_color}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {_safe_msg}</div>", unsafe_allow_html=True)

    menu = st.session_state.current_page
    if   menu == "🏠 홈 광장 (튜토리얼)":   from pages import home;              home.render(market, nw)
    elif menu == "💎 VIP 라운지":            from pages import vip;               vip.render(market, nw)
    elif menu == "📈 주식 트레이딩":         from pages import stock;             stock.render(market, nw)
    elif menu == "🪙 코인 거래소":           from pages import crypto;            crypto.render(market, nw)
    elif menu == "🏢 부동산 거래소":         from pages import real_estate;       real_estate.render(market, nw)
    elif menu == "🏦 은행 (대출/송금)":      from pages import bank;              bank.render(market, nw)
    elif menu == "📜 내 거래 기록":          from pages import txlog;             txlog.render(market, nw)
    elif menu == "📅 일일 퀘스트":           from pages import quest;             quest.render(market, nw)
    elif menu == "👑 칭호 상점":             from pages import title_shop;        title_shop.render(market, nw)
    elif menu == "🏅 [시즌1]랭킹 & 게시판": from pages import ranking;           ranking.render(market, nw)
    elif menu == "✉️ 개인 쪽지함":           from pages import dm;                dm.render(market, nw)
    elif menu == "🏰 길드/클랜":             from pages import clan;              clan.render(market, nw)
    elif menu == "🎰 럭키 슬롯":             from pages.games import slot;        slot.render(market, nw)
    elif menu == "🃏 블랙잭 카지노":         from pages.games import blackjack;   blackjack.render(market, nw)
    elif menu == "🃏 텍사스 홀덤":           from pages.games import holdem;      holdem.render(market, nw)
    elif menu == "⛏️ 광산 (노가다)":         from pages.games import mine;        mine.render(market, nw)
    elif menu == "💻 사주팔자":            from pages.games import quiz;        quiz.render(market, nw)
    elif menu == "⚔️ 글로벌 로또":           from pages.games import lotto;       lotto.render(market, nw)
    elif menu == "🗡️ 전설의 명검 강화":      from pages.games import forge;       forge.render(market, nw)
    elif menu == "🎴 가챠 뽑기":             from pages.games import gacha;       gacha.render(market, nw)
    elif menu == "⚽ 구단주 시뮬레이터":     from pages.sports import soccer_sim; soccer_sim.render(market, nw)
    elif menu == "⚽ 조기축구 승부차기":      from pages.sports import penalty;    penalty.render(market, nw)
    elif menu == "🏎️ 하이퍼카 레이싱":      from pages.sports import racing;     racing.render(market, nw)
    elif menu == "🛠️ 커스텀 튜닝 차고지":   from pages.sports import garage;     garage.render(market, nw)
    elif menu == "🛠️ 창조주 통제소":        from pages.admin import panel;       panel.render(market, nw)
    else: st.info(f"🚧 '{menu}' 페이지를 로드할 수 없습니다.")


# ==============================
# 6. [View 4] AI 아카데미
# ==============================
elif st.session_state.page_view == "project_a":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()
    market = run_market_sync()
    from pages import project_a
    project_a.render(market, 0)


# ==============================
# 7. [View 5] 효민 월드 배틀
# ==============================
elif st.session_state.page_view == "project_b":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_b"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_b
    project_b.render()


# ==============================
# 8. [View 6] THE TERMINAL
# ==============================
elif st.session_state.page_view == "project_c":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_c"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_c
    project_c.render()


# ==============================
# 9. [View 7] 🎲 인베스트 마블
# ==============================
elif st.session_state.page_view == "project_d":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_d"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_d
    project_d.render()


# ==============================
# 10. [View 8] ⚔️ 뱀서라이크 던전
# ==============================
elif st.session_state.page_view == "project_e":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_e"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_e
    project_e.render()


# ==============================
# 11. [View 9] 🏎️ 네온 도주 레이싱
# ==============================
elif st.session_state.page_view == "project_f":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_f"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_f
    project_f.render()


# ==============================
# 12. [View 10] 🧟 좀비 아포칼립스
# ==============================
elif st.session_state.page_view == "project_g":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_g"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_g
    project_g.render()


# ==============================
# 13. [View 11] 🥊 스트리트 파이터 EX
# ==============================
elif st.session_state.page_view == "project_h":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_h"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_h
    project_h.render()


# ==============================
# 14. [View 12] 🎯 스나이퍼 엘리트
# ==============================
elif st.session_state.page_view == "project_i":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_i"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_i
    project_i.render()
