# app.py
import re
import streamlit as st
import time
import os
from datetime import datetime

# ==============================
# 1. 코어 모듈 임포트
# ==============================
# 💡 [추가] 랭킹 1위 자산 계산을 위해 estate_config, FORGE_DATA 임포트 추가
from utils.config import MARKET_FILE, USERS_FILE, KST, MESSAGES_FILE, STATS_FILE, estate_config, FORGE_DATA
from utils.database import load_db, save_db, load_stats, save_stats
from utils.core import hash_pw, format_korean_money, get_net_worth, sync_user_data, ADMIN_HASH, pull_user_data, get_online_users
from utils.market_sync import run_market_sync
from utils.css import GLOBAL_CSS

# ==============================
# 2. 페이지 기본 설정
# ==============================
st.set_page_config(page_title="HYOMIN PORTAL", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

pull_user_data()

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: last_seen — 60초에 한 번만 전체 DB 쓰기
#   기존: 매 리렌더마다 전체 users_db 읽기+쓰기 → MongoDB 과부하
# ─────────────────────────────────────────────────────────────────────────────
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

# FIX 2: market 최상단 로드 제거 — universe/project_a 뷰 진입 시점에만 각각 로드

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: _do_login 모듈 수준 함수로 이동 (버튼 핸들러 내부 중첩 정의 제거)
# ─────────────────────────────────────────────────────────────────────────────
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
    if today not in visitors:        visitors[today] = []
    if uid not in visitors[today]:   visitors[today].append(uid)
    stats["daily_visitors"] = visitors
    save_stats(stats)
    st.success("로그인 성공!")
    time.sleep(0.5)
    st.session_state.page_view = "portal"
    st.rerun()


# 🌟 포털·로그인 전용 밝은 테마 CSS
PORTAL_LIGHT_CSS = """
<style>
.stApp { background-color: #F8FAFC !important; color: #0F172A !important; }
h1, h2, h3, h4, p, span, div { color: #0F172A; }
.portal-header { text-align: center; padding: 50px 0 20px 0; }
.portal-title {
    font-family: 'Inter', sans-serif; font-size: 3.5rem; font-weight: 900;
    letter-spacing: 2px; color: #2563EB !important; margin-bottom: 10px;
}
.trust-badge {
    display: inline-block; background: rgba(37,99,235,0.1);
    border: 1px solid rgba(37,99,235,0.3); color: #2563EB !important;
    padding: 5px 12px; border-radius: 20px; font-size: 0.8rem;
    font-weight: bold; margin-bottom: 20px;
}
.banner-card {
    background: #FFFFFF !important; border-radius: 12px; padding: 30px;
    text-align: center; border: 1px solid #E2E8F0 !important;
    transition: all 0.3s ease; margin-bottom: 20px; min-height: 200px;
    display: flex; flex-direction: column; justify-content: center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.banner-card:hover {
    border-color: #3B82F6 !important; transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(59,130,246,0.15);
}
.banner-card h2 { color: #1E293B !important; margin-bottom: 8px; }
.banner-card p  { color: #64748B !important; font-weight: 500; }
.stat-grid { display:flex; gap:16px; margin:24px 0 8px 0; flex-wrap:wrap; }
.stat-card {
    flex:1; min-width:160px; background:#FFFFFF; border:1px solid #E2E8F0;
    border-radius:14px; padding:20px 18px 16px 18px; text-align:center;
    box-shadow:0 2px 8px rgba(37,99,235,0.06); transition:box-shadow 0.2s,transform 0.2s;
}
.stat-card:hover { box-shadow:0 6px 20px rgba(37,99,235,0.13); transform:translateY(-3px); }
.stat-icon  { font-size:1.8rem; margin-bottom:6px; line-height:1; }
.stat-value { font-size:1.6rem; font-weight:900; color:#1E40AF !important; line-height:1.1; margin-bottom:4px; }
.stat-label { font-size:0.75rem; font-weight:600; color:#64748B !important; letter-spacing:0.04em; text-transform:uppercase; }
.stat-card.online .stat-value { color:#16A34A !important; }
.stat-card.volume  .stat-value { color:#7C3AED !important; }
.stat-section-title { font-size:0.72rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:#94A3B8 !important; margin-bottom:4px; }
</style>
"""


# ==============================
# 3. [View 1] 포털 메인 화면
# ==============================
if st.session_state.page_view == "portal":
    st.markdown(PORTAL_LIGHT_CSS, unsafe_allow_html=True)
    market = load_db(MARKET_FILE, {}) # 포털용 임시 로드

    col_empty, col_btn = st.columns([8, 2])
    with col_btn:
        if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
            st.markdown(f"<div style='text-align:right;color:#475569;font-weight:bold;margin-bottom:5px;'>👤 {st.session_state.logged_in_user}님</div>", unsafe_allow_html=True)
            if st.button("🚪 로그아웃", use_container_width=True):
                sync_user_data(); st.session_state.clear(); st.rerun()
        else:
            if st.button("🔑 로그인 / 회원가입", use_container_width=True):
                st.session_state.page_view = "login"; st.rerun()

    st.markdown("""
        <div class='portal-header'>
            <div class='trust-badge'>🛡️ HYOMIN NETWORKS SECURE PLATFORM</div>
            <div class='portal-title'>HYOMIN PORTAL</div>
            <p style='color:#475569;font-size:1.1rem;max-width:600px;margin:0 auto;'>
                하나의 계정으로 효민 유니버스의 모든 경제, 엔터테인먼트, 커뮤니티 서비스를 통합 이용하세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")

    try:
        _stats     = load_stats()
        _today     = datetime.now(KST).strftime("%Y-%m-%d")
        _online    = get_online_users()
        _today_v   = len(_stats.get("daily_visitors", {}).get(_today, []))
        
        _users_db_for_stats = load_db(USERS_FILE, {})
        _total_s   = len([u for u in _users_db_for_stats.keys() if u != "admin"])
        
        # 👑 [랭킹 1위 계산] 순자산 1위 유저 찾기
        _top_uid = "없음"
        _top_nw = 0
        _prices = {k: v['price'] for k, v in market.get('stock_data', {}).items()}
        
        for _u, _udata in _users_db_for_stats.items():
            if _u == "admin": continue
            _w = _udata.get('cash', 0) - _udata.get('loan', 0)
            for _sid, _p_data in _udata.get('portfolio', {}).items():
                if _sid in _prices: _w += _p_data.get('qty', 0) * _prices[_sid]
            for _cid, _cinfo in _udata.get('crypto_portfolio', {}).items():
                _cprice = market.get('crypto_data', {}).get(_cid, {}).get('price', 0)
                _w += _cinfo.get('qty', 0) * _cprice
            for _eid, _count in _udata.get('real_estate', {}).items():
                if _eid in estate_config: _w += estate_config[_eid]['base_price'] * _count * 0.8
            _w_lv = _udata.get('weapon_level', 0)
            if _w_lv > 0: _w += FORGE_DATA[_w_lv]['sell']
            
            if _w > _top_nw:
                _top_nw = _w
                _top_uid = _u

        _nw_str = format_korean_money(_top_nw) if _top_nw > 0 else "0원"
        
        st.markdown("<div class='stat-section-title'>📡 실시간 서비스 현황</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-card online"><div class="stat-icon">🟢</div><div class="stat-value">{_online}명</div><div class="stat-label">지금 접속 중</div></div>
            <div class="stat-card"><div class="stat-icon">📅</div><div class="stat-value">{_today_v}명</div><div class="stat-label">오늘 방문자</div></div>
            <div class="stat-card"><div class="stat-icon">👥</div><div class="stat-value">{_total_s}명</div><div class="stat-label">누적 가입자</div></div>
            <div class="stat-card volume"><div class="stat-icon">👑</div><div class="stat-value" style="font-size:1.4rem;">{_nw_str}</div><div class="stat-label">1위: {_top_uid}</div></div>
        </div>""", unsafe_allow_html=True)
    except Exception as e:
        pass

    st.write("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='banner-card'><h2>🌌 효민 유니버스</h2><p>자본주의 생존 시뮬레이션 시즌 1</p></div>", unsafe_allow_html=True)
        if st.button("유니버스 입장하기 🚀", use_container_width=True):
            if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
                st.session_state.page_view = "universe"
            else:
                st.warning("⚠️ 해당 서비스를 이용하시려면 먼저 로그인해주세요.")
                time.sleep(1); st.session_state.page_view = "login"
            st.rerun()
        st.markdown("<div class='banner-card'><h2>🛠️ 비밀 프로젝트 B</h2><p>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b2", disabled=True, use_container_width=True)
        st.markdown("<div class='banner-card'><h2>🛠️ 비밀 프로젝트 D</h2><p>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b4", disabled=True, use_container_width=True)

    with col2:
        st.markdown("<div class='banner-card'><h2>🧠 AI 무한 모의고사</h2><p>공부한 내용 복붙하면, AI가 끝없이 문제를 만들어 드립니다.</p></div>", unsafe_allow_html=True)
        if st.button("AI 아카데미 입장 📚", key="b1", use_container_width=True):
            if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
                st.session_state.page_view = "project_a"
            else:
                st.warning("⚠️ 해당 서비스를 이용하시려면 먼저 로그인해주세요.")
                time.sleep(1); st.session_state.page_view = "login"
            st.rerun()
        st.markdown("<div class='banner-card'><h2>🛠️ 비밀 프로젝트 C</h2><p>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b3", disabled=True, use_container_width=True)
        st.markdown("<div class='banner-card'><h2>🛠️ 비밀 프로젝트 E</h2><p>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b5", disabled=True, use_container_width=True)

    st.markdown("<div style='text-align:center;padding:40px 0;color:#94A3B8;font-size:0.8rem;'><p>ⓒ 2026 HYOMIN PORTAL INC. All rights reserved.</p></div>", unsafe_allow_html=True)
    st.stop()


# ==============================
# 4. [View 2] 로그인 / 회원가입
# ==============================
elif st.session_state.page_view == "login":
    st.markdown(PORTAL_LIGHT_CSS, unsafe_allow_html=True)

    if st.button("🔙 포털 메인으로 돌아가기"):
        st.session_state.page_view = "portal"; st.rerun()

    st.markdown("<div style='text-align:center;padding:30px 0 10px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#2563EB !important;'>HYOMIN ID 로그인</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B !important;'>안전한 서비스 이용을 위해 로그인해주세요.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])

        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

            if st.button("🚀 로그인 및 계속하기", use_container_width=True):
                # ──────────────────────────────────────────────────────────
                # FIX 4: 브루트포스 방어 — 5회 실패 시 30초 잠금
                # ──────────────────────────────────────────────────────────
                _fails     = st.session_state.get('login_fails', 0)
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
                # ──────────────────────────────────────────────────────────
                # FIX 5: 아이디 특수문자 필터링 — 한글·영문·숫자·언더바만 허용
                # ──────────────────────────────────────────────────────────
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
                        "crypto_portfolio": {},
                        "daily_quests": {},
                        "weapon_level": 0,
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

    # FIX 2 이어서 + 점검모드 체크 (FIX 3)
    market = run_market_sync()

    if market.get("maintenance_mode") and st.session_state.logged_in_user != "admin":
        st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
        st.warning(f"🔧 {market.get('maintenance_msg', '현재 서버 점검 중입니다. 이용에 불편을 드려 죄송합니다.')}")
        st.info("점검이 끝나면 자동으로 이용 가능합니다.")
        if st.button("🏠 포털 메인으로 돌아가기"):
            st.session_state.page_view = "portal"; st.rerun()
        st.stop()

    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:15px;'>", unsafe_allow_html=True)
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    def _calc_nw_from_session(market_data):
        from utils.config import estate_config, FORGE_DATA
        w = st.session_state.global_cash - st.session_state.loan
        prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
        for sid, p_data in st.session_state.portfolio.items():
            if sid in prices: w += p_data.get('qty', 0) * prices[sid]
        for cid, cinfo in st.session_state.get('crypto_portfolio', {}).items():
            w += cinfo.get('qty', 0) * market_data.get('crypto_data', {}).get(cid, {}).get('price', 0)
        for eid, count in st.session_state.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
        w_lv = st.session_state.get('weapon_level', 0)
        if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
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
    if   menu == "🏠 홈 광장 (튜토리얼)":   from pages import home;          home.render(market, nw)
    elif menu == "💎 VIP 라운지":            from pages import vip;           vip.render(market, nw)
    elif menu == "📈 주식 트레이딩":         from pages import stock;         stock.render(market, nw)
    elif menu == "🪙 코인 거래소":           from pages import crypto;        crypto.render(market, nw)
    elif menu == "🏢 부동산 거래소":         from pages import real_estate;   real_estate.render(market, nw)
    elif menu == "🏦 은행 (대출/송금)":      from pages import bank;          bank.render(market, nw)
    elif menu == "📜 내 거래 기록":          from pages import txlog;         txlog.render(market, nw)
    elif menu == "📅 일일 퀘스트":           from pages import quest;         quest.render(market, nw)
    elif menu == "👑 칭호 상점":             from pages import title_shop;    title_shop.render(market, nw)
    elif menu == "🏅 [시즌1]랭킹 & 게시판": from pages import ranking;       ranking.render(market, nw)
    elif menu == "✉️ 개인 쪽지함":           from pages import dm;            dm.render(market, nw)
    elif menu == "🏰 길드/클랜":             from pages import clan;          clan.render(market, nw)
    elif menu == "🎰 럭키 슬롯":             from pages.games import slot;    slot.render(market, nw)
    elif menu == "🃏 블랙잭 카지노":         from pages.games import blackjack; blackjack.render(market, nw)
    elif menu == "🃏 텍사스 홀덤":           from pages.games import holdem;  holdem.render(market, nw)
    elif menu == "⛏️ 광산 (노가다)":         from pages.games import mine;    mine.render(market, nw)
    elif menu == "💻 정처기 CBT":            from pages.games import quiz;    quiz.render(market, nw)
    elif menu == "⚔️ 글로벌 로또":           from pages.games import lotto;   lotto.render(market, nw)
    elif menu == "🗡️ 전설의 명검 강화":      from pages.games import forge;   forge.render(market, nw)
    elif menu == "🎴 가챠 뽑기":             from pages.games import gacha;   gacha.render(market, nw)
    elif menu == "⚽ 구단주 시뮬레이터":     from pages.sports import soccer_sim;  soccer_sim.render(market, nw)
    elif menu == "⚽ 조기축구 승부차기":      from pages.sports import penalty;    penalty.render(market, nw)
    elif menu == "🏎️ 하이퍼카 레이싱":      from pages.sports import racing;     racing.render(market, nw)
    elif menu == "🛠️ 커스텀 튜닝 차고지":   from pages.sports import garage;     garage.render(market, nw)
    elif menu == "🛠️ 창조주 통제소":        from pages.admin import panel;       panel.render(market, nw)
    else: st.info(f"🚧 '{menu}' 페이지는 존재하지 않거나 로드할 수 없습니다.")


# ==============================
# 6. [View 4] 비밀 프로젝트 A
# ==============================
elif st.session_state.page_view == "project_a":

    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()

    st.markdown("<div style='margin-bottom:15px;'>", unsafe_allow_html=True)
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # project_a도 market 사용 → 여기서 로드 (포털 화면엔 영향 없음)
    market = run_market_sync()
    from pages import project_a
    project_a.render(market, 0)
