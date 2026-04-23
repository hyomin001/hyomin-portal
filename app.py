# app.py
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
from utils.core import hash_pw, format_korean_money, get_net_worth, sync_user_data, ADMIN_HASH, pull_user_data, get_online_users
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
        'last_estate_reset': u.get('last_estate_reset', 0),
        'login_fails':       0,
        '_last_seen_write':  0,
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

/* ── 공지 아코디언 ── */
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

/* Streamlit 텍스트/헤더 색상 보정 */
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }
p, span, div { color: var(--text); }
.stExpander { border-color: var(--border) !important; }
.stExpander summary { color: var(--text) !important; }
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
        _top_uid, _top_nw = "없음", 0
        _prices = {k: v['price'] for k, v in market.get('stock_data', {}).items()}
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
            if _w > _top_nw: _top_nw, _top_uid = _w, _u
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
        <div class="stat-label">1위: {_top_uid}</div>
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
          <div class='card-desc'>커맨드라인 방탈출 어드벤처<br>10 스테이지 · 가상 파일시스템</div>
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

    # ── 공지 & 아키텍처 ──
    with st.expander("📋 시스템 공지 & 전체 아키텍처", expanded=False):
        st.markdown("""
<div class='notice-card' style='border-color:rgba(0,255,136,0.3);'>
  <h4>🌟 시즌 1 공식 개막</h4>
  <p><b>기간:</b> 2026년 4월 15일 ~ 5월 15일 &nbsp;|&nbsp; 신규 가입 즉시 <b>초기 정착금 5억 원</b> 지급!</p>
</div>
<div class='notice-card' style='border-color:rgba(108,99,255,0.3);'>
  <h4>🔧 시스템 대공사 완료</h4>
  <p>MongoDB Atlas 클라우드 이전 완료. 38개 모듈화 설계 적용. 유저 자산 영구 안전 보존.</p>
  <div style='margin-top:10px;'>
    <span class='notice-badge'>MongoDB Atlas</span>
    <span class='notice-badge'>SHA-256</span>
    <span class='notice-badge'>38개 모듈</span>
    <span class='notice-badge'>실시간 백업</span>
  </div>
</div>
        """, unsafe_allow_html=True)

    with st.expander("📖 서비스 완전 가이드", expanded=False):
        g1, g2 = st.columns(2)
        with g1:
            st.markdown("""
<div class='notice-card'>
  <h4>🌌 효민 유니버스</h4>
  <p>가입 즉시 5억 지급. 주식·코인·부동산·은행·클랜·미니게임 8종·VIP 라운지.</p>
  <div style='margin-top:8px;'>
    <span class='notice-badge'>📈 주식</span><span class='notice-badge'>₿ 코인</span>
    <span class='notice-badge'>🏠 부동산</span><span class='notice-badge'>🎰 게임 8종</span>
  </div>
</div>
<div class='notice-card'>
  <h4>🧠 AI 무한 모의고사</h4>
  <p>Gemini 2.5 Flash가 PDF·텍스트를 분석해 무한 문제 생성. 오답 자동 재출제.</p>
</div>
<div class='notice-card'>
  <h4>🎲 인베스트 마블</h4>
  <p>모노폴리 기반 투자 보드게임. AI 봇 대전, 세계 랜드마크 독점.</p>
</div>
            """, unsafe_allow_html=True)
        with g2:
            st.markdown("""
<div class='notice-card'>
  <h4>🗳️ 월드 배틀</h4>
  <p>매일 새로운 주제로 A vs B 진영 투표. 실시간 비율 시각화, 댓글, 완전 익명.</p>
</div>
<div class='notice-card'>
  <h4>💻 THE TERMINAL</h4>
  <p>CLI 명령어로 가상 파일시스템을 탐색해 방탈출. 10 스테이지, 단계별 힌트.</p>
</div>
<div class='notice-card'>
  <h4>⚔️ 던전 런 REBORN</h4>
  <p>뱀서라이크 서바이벌. 전사·마법사·궁수·닌자 4클래스. 웨이브 보스 격파.</p>
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
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

            if st.button("🚀 로그인 및 계속하기", use_container_width=True):
                _fails      = st.session_state.get('login_fails', 0)
                _lock_until = st.session_state.get('login_lock_until', 0)
                if time.time() < _lock_until:
                    _remain = int(_lock_until - time.time())
                    st.error(f"🔒 로그인 시도 초과. {_remain}초 후 다시 시도하세요.")
                    st.stop()
                users = load_db(USERS_FILE, {})
                if l_id == "admin" and hash_pw(l_pw) == ADMIN_HASH:
                    if "admin" not in users:
                        users["admin"] = {"pw": ADMIN_HASH, "cash": 999_999_999_999,
                                          "inventory": [], "equipped_title": "👑 절대신 창조주"}
                        save_db(USERS_FILE, users)
                    _do_login("admin", users, device_mode)
                elif l_id != "admin" and l_id in users and users[l_id]['pw'] == hash_pw(l_pw):
                    _do_login(l_id, users, device_mode)
                else:
                    _fails += 1
                    st.session_state['login_fails'] = _fails
                    if _fails >= 5:
                        st.session_state['login_lock_until'] = time.time() + 30
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
                elif len(n_pw) < 6:
                    st.error("⚠️ 비밀번호는 6자 이상이어야 합니다.")
                else:
                    users[clean_id] = {
                        "pw": hash_pw(n_pw), "cash": 500_000_000, "inventory": [],
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
        st.session_state.equipped_title = "💸 신용불량자"
        sync_user_data()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"

    is_admin = st.session_state.logged_in_user == "admin"
    is_vip   = nw >= 100_000_000_000 or is_admin

    CATEGORY_MENUS = {
        "📈 경제":        ["🏠 홈 광장 (튜토리얼)", "📈 주식 트레이딩", "🪙 코인 거래소", "🏢 부동산 거래소", "🏦 은행 (대출/송금)", "📜 내 거래 기록"],
        "🎮 미니게임":    ["🎰 럭키 슬롯", "🃏 블랙잭 카지노", "⛏️ 광산 (노가다)", "🃏 텍사스 홀덤", "💻 정처기 CBT", "⚔️ 글로벌 로또", "🗡️ 전설의 명검 강화", "🎴 가챠 뽑기"],
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
        st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {market.get('admin_color','#FF4B4B')};border-radius:10px;padding:12px;color:{market.get('admin_color','#FF4B4B')}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {market['admin_msg']}</div>", unsafe_allow_html=True)

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
    elif menu == "💻 정처기 CBT":            from pages.games import quiz;        quiz.render(market, nw)
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
