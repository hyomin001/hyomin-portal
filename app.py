# ============================================================
# app.py — HYOMIN UNIVERSE 메인 진입점
# ============================================================
import time
import random
import streamlit as st

st.set_page_config(
    page_title="HYOMIN UNIVERSE v19",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── 내부 모듈 임포트 ─────────────────────────────────────────
from config import (
    USERS_FILE, STOCK_CONFIG, ESTATE_CONFIG,
    DAILY_QUESTS_CONFIG, FORGE_DATA, build_menu, hash_pw, ADMIN_HASH,
)
from utils.database import (
    load_db, save_db, get_market, save_market,
    load_estate_market,
)
from utils.helpers import format_korean_money, set_cooldown, cooldown_remaining
from utils.sync import (
    get_net_worth, sync_user_data,
    load_session_from_db, claim_hidden_title,
)
from utils.css import get_css
from utils.market_engine import run_market_tick
from datetime import timezone, timedelta

KST = timezone(timedelta(hours=9))

# ════════════════════════════════════════════════════════════
# 1. 마켓 로드 & 틱 실행
# ════════════════════════════════════════════════════════════
market = get_market()
market, market_changed = run_market_tick(market)
if market_changed:
    save_market(market)

# ── 테마 컬러 결정 ────────────────────────────────────────
ndx_h    = market["stock_data"].get("NDX", {}).get("history", [0, 0])
ndx_diff = (ndx_h[-1] - ndx_h[-2]) / ndx_h[-2] if len(ndx_h) > 1 and ndx_h[-2] > 0 else 0
theme_color = "#00E5FF"
if ndx_diff >= 0.02:    theme_color = "#FF4B4B"
elif ndx_diff <= -0.02: theme_color = "#4B9EFF"

# ── CSS 적용 ─────────────────────────────────────────────
st.markdown(f"<style>{get_css(theme_color)}</style>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# 2. 세션 → DB 동기화 (로그인 상태일 때)
# ════════════════════════════════════════════════════════════
if "logged_in_user" in st.session_state:
    # 부동산 리셋 신호 처리
    if st.session_state.get("last_estate_reset", 0) < market.get("force_estate_reset", 0):
        st.session_state.real_estate    = {}
        st.session_state.rent_time      = time.time()
        st.session_state.last_estate_reset = market["force_estate_reset"]
        sync_user_data()

    # DB에서 최신 데이터 로드 (현금/자산이 다른 세션에서 변경될 수 있으므로)
    us_db = load_db(USERS_FILE, {})
    my_uid = st.session_state.logged_in_user
    if my_uid in us_db:
        u = us_db[my_uid]
        st.session_state.global_cash      = u.get("cash", 0)
        st.session_state.real_estate      = u.get("real_estate", {})
        st.session_state.loan             = u.get("loan", 0)
        st.session_state.inventory        = u.get("inventory", [])
        st.session_state.equipped_title   = u.get("equipped_title", "🌱 신규시민")
        st.session_state.portfolio        = u.get("portfolio", {})
        st.session_state.crypto_portfolio = u.get("crypto_portfolio", {})
        st.session_state.weapon_level     = u.get("weapon_level", 0)
        st.session_state.daily_quests     = u.get("daily_quests", {})
        st.session_state.garage           = u.get("garage", {"cars": {}, "active_tier": None})

    # 대출 이자 처리
    cur_t = time.time()
    if st.session_state.get("loan", 0) > 0:
        MAX_CYC  = 30
        MAX_LOAN = 999_999_999_999_999
        elapsed  = cur_t - st.session_state.get("loan_time", cur_t)
        cyc      = min(int(elapsed / 10), MAX_CYC)
        if cyc > 0:
            st.session_state.loan = min(int(st.session_state.loan * (1.02 ** cyc)), MAX_LOAN)
            st.session_state.loan_time = st.session_state.get("loan_time", cur_t) + cyc * 10
            sync_user_data()

    # 신용불량자 체크
    nw = get_net_worth(my_uid, market)
    if st.session_state.loan > 0 and nw < 0:
        st.session_state.equipped_title = "💸 신용불량자"
        sync_user_data()

    # ── 출석 퀘스트 자동 지급 ────────────────────────────
    from datetime import datetime
    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    dq = st.session_state.get("daily_quests", {})
    today_dq = dq.get(today_str, {})
    if not today_dq.get("attendance", False):
        today_dq["attendance"] = True
        dq[today_str]          = today_dq
        st.session_state.daily_quests = dq
        attendance_reward = next(
            q["reward"] for q in DAILY_QUESTS_CONFIG if q["id"] == "attendance"
        )
        st.session_state.global_cash += attendance_reward
        sync_user_data()
        st.toast(f"📅 출석 체크 완료! +{format_korean_money(attendance_reward)}", icon="🎁")

# ════════════════════════════════════════════════════════════
# 3. 로그인 화면
# ════════════════════════════════════════════════════════════
if "logged_in_user" not in st.session_state:
    _render_login(market, theme_color)
    st.stop()

# ════════════════════════════════════════════════════════════
# 4. 메뉴 & 네비게이션
# ════════════════════════════════════════════════════════════
nw       = get_net_worth(st.session_state.logged_in_user, market)
is_admin = st.session_state.logged_in_user == "admin"
is_vip   = nw >= 100_000_000_000 or is_admin
MENUS    = build_menu(is_admin, is_vip)

# 쪽지 미확인 배지
msg_db_check = load_db("messages_db.json", {})
my_unread = sum(
    1 for m in msg_db_check.get(st.session_state.logged_in_user, {}).get("inbox", [])
    if not m.get("read", False)
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"
if "current_category" not in st.session_state:
    st.session_state.current_category = "📈 경제"

is_pc = "PC" in st.session_state.get("device_mode", "🖥️ PC (데스크탑)")

if is_pc:
    _render_sidebar(MENUS, nw, my_unread)
else:
    _render_mobile_nav(MENUS, my_unread)

# ── 공통 시즌 배너 (경제 카테고리) ──────────────────────────
if st.session_state.current_category == "📈 경제":
    _render_season_banner(market, theme_color)

# ── 뉴스 & 공지 배너 ────────────────────────────────────────
st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
if market.get("admin_msg"):
    col = market.get("admin_color", "#FF4B4B")
    st.markdown(
        f"<div style='background:rgba(255,0,0,0.08);border:1px solid {col};"
        f"border-radius:10px;padding:12px 16px;color:{col}!important;font-weight:900;margin:8px 0;'>"
        f"📢 [관리자 공지] {market['admin_msg']}</div>",
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════
# 5. 페이지 라우팅
# ════════════════════════════════════════════════════════════
menu = st.session_state.current_page

if   menu == "🏠 홈 광장 (튜토리얼)":
    from pages.home          import render; render(market, nw, theme_color)
elif menu == "💎 VIP 라운지":
    from pages.vip           import render; render(market, nw)
elif menu == "📈 주식 트레이딩":
    from pages.stock         import render; render(market)
elif menu == "🪙 코인 거래소":
    from pages.crypto        import render; render(market)
elif menu == "🏢 부동산 거래소":
    from pages.real_estate   import render; render(market)
elif menu == "🏦 은행 (대출/송금)":
    from pages.bank          import render; render(market, nw)
elif menu == "📜 내 거래 기록":
    from pages.tx_history    import render; render()
elif menu == "🎰 럭키 슬롯":
    from pages.games.slot    import render; render(market)
elif menu == "🃏 블랙잭 카지노":
    from pages.games.blackjack import render; render()
elif menu == "⛏️ 광산 (노가다)":
    from pages.games.mine    import render; render(market)
elif menu == "💻 정처기 CBT":
    from pages.games.cbt     import render; render()
elif menu == "⚔️ 글로벌 로또":
    from pages.games.lotto   import render; render(market)
elif menu == "🗡️ 전설의 명검 강화":
    from pages.games.forge   import render; render(market)
elif menu == "🎴 가챠 뽑기":
    from pages.games.gacha   import render; render(market)
elif menu == "📅 일일 퀘스트":
    from pages.quest         import render; render(market, nw)
elif menu == "👑 칭호 상점":
    from pages.title_shop    import render; render()
elif menu == "⚽ 구단주 시뮬레이터":
    from pages.sports.soccer_sim import render; render(market)
elif menu == "⚽ 조기축구 승부차기":
    from pages.sports.penalty    import render; render()
elif menu == "🏎️ 하이퍼카 레이싱":
    from pages.sports.racing     import render; render(market)
elif menu == "🛠️ 커스텀 튜닝 차고지":
    from pages.sports.garage     import render; render(market)
elif menu == "🏰 길드/클랜":
    from pages.clan          import render; render(market)
elif menu == "🏅 [시즌2]랭킹 & 게시판":
    from pages.ranking       import render; render(market)
elif menu == "✉️ 개인 쪽지함":
    from pages.dm            import render; render()
elif menu == "🛠️ 창조주 통제소" and is_admin:
    from pages.admin.panel   import render; render()


# ════════════════════════════════════════════════════════════
# 내부 헬퍼 함수들 (app.py 하단)
# ════════════════════════════════════════════════════════════

def _render_login(market, theme_color):
    st.markdown(f"""
<style>
.stApp {{ background: radial-gradient(ellipse at 20% 50%, #0d0221, #050510 60%, #000) !important; }}
.login-title {{
  font-family:'Orbitron',monospace !important; font-size:clamp(2rem,6vw,4rem) !important;
  font-weight:900; text-align:center;
  background:linear-gradient(135deg,#00E5FF,#FF00FF,#FFD600);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  padding:20px 0 5px; letter-spacing:4px;
}}
.login-sub {{ text-align:center; color:#888 !important; font-size:1rem; letter-spacing:3px; margin-bottom:20px; }}
</style>""", unsafe_allow_html=True)

    sn = market.get("season_num", 1)
    st.markdown("<div class='login-title'>🌌 HYOMIN UNIVERSE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='login-sub'>∙ 자본주의 생존 시뮬레이션 시즌 {sn} ∙</div>", unsafe_allow_html=True)

    _, c2, _ = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호")
            if st.button("🚀 유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id == "admin":
                    if hash_pw(l_pw) == ADMIN_HASH:
                        if "admin" not in users:
                            users["admin"] = {"pw": ADMIN_HASH, "cash": 999_999_999_999,
                                              "inventory": [], "equipped_title": "👑 절대신 창조주",
                                              "portfolio": {}, "real_estate": {}, "rent_time": time.time(),
                                              "loan": 0, "loan_time": time.time()}
                            save_db(USERS_FILE, users)
                        load_session_from_db("admin", device_mode)
                        st.rerun()
                    else:
                        st.error("❌ 비밀번호 오류")
                elif l_id in users and users[l_id]["pw"] == hash_pw(l_pw):
                    load_session_from_db(l_id, device_mode)
                    st.rerun()
                else:
                    st.error("❌ 아이디 또는 비밀번호 오류")

        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호")
            if st.button("✨ 시민 등록", use_container_width=True):
                users = load_db(USERS_FILE, {})
                clean = n_id.strip()
                if not clean or len(clean) < 2:
                    st.error("⚠️ 아이디는 2자 이상이어야 합니다.")
                elif clean in users or clean == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif "<" in clean or ">" in clean:
                    st.error("⚠️ 특수문자(<, >)는 사용 불가합니다.")
                else:
                    users[clean] = {
                        "pw": hash_pw(n_pw), "cash": 500_000_000,
                        "inventory": [], "equipped_title": "🌱 신규시민",
                        "portfolio": {}, "real_estate": {}, "rent_time": time.time(),
                        "loan": 0, "loan_time": time.time(),
                    }
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 시즌 2 정착금 5억원이 지급되었습니다!")


def _render_sidebar(menus, nw, my_unread):
    uid = st.session_state.logged_in_user
    with st.sidebar:
        unread_dot = "  🔴" if my_unread > 0 else ""
        st.markdown(
            f"<div style='padding:14px 16px;background:rgba(255,255,255,0.05);"
            f"border:1px solid rgba(0,229,255,0.2);border-radius:10px;margin-bottom:14px;'>"
            f"<div style='font-size:0.8rem;color:#00E5FF;'>{st.session_state.equipped_title}</div>"
            f"<div style='font-size:1rem;font-weight:700;color:#E2E8F0;'>{uid}{unread_dot}</div></div>",
            unsafe_allow_html=True,
        )
        ca, cb = st.columns(2)
        ca.metric("💵 현금", format_korean_money(st.session_state.global_cash))
        cb.metric("📊 순자산", format_korean_money(nw))
        if st.session_state.loan > 0:
            st.metric("💳 대출", format_korean_money(st.session_state.loan))
        st.write("---")
        for cat in menus:
            if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                st.session_state.current_category = cat
                st.session_state.current_page = menus[cat][0]
                st.rerun()
        st.write("---")
        cur_pages = menus.get(st.session_state.current_category, [])
        cur_idx = cur_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_pages else 0
        sel = st.radio("메뉴", cur_pages, index=cur_idx, label_visibility="collapsed")
        if sel != st.session_state.current_page:
            st.session_state.current_page = sel
            st.rerun()
        st.write("---")
        if st.button("로그아웃", use_container_width=True):
            sync_user_data(); st.session_state.clear(); st.rerun()


def _render_mobile_nav(menus, my_unread):
    uid = st.session_state.logged_in_user
    unread_txt = f" 🔴{my_unread}" if my_unread > 0 else ""
    ca, cb = st.columns([3, 1])
    ca.markdown(
        f"<div style='font-size:0.82rem;color:#999;'>👤 <b style='color:#E2E8F0;'>{uid}</b>{unread_txt}"
        f"&nbsp;|&nbsp;<span style='color:#00E5FF;'>{st.session_state.equipped_title}</span></div>"
        f"<div style='font-size:0.9rem;font-weight:700;color:#E2E8F0;margin-top:2px;'>"
        f"💵 {format_korean_money(st.session_state.global_cash)}</div>",
        unsafe_allow_html=True,
    )
    if cb.button("로그아웃"):
        sync_user_data(); st.session_state.clear(); st.rerun()

    cat_sel = st.selectbox("카테고리", list(menus.keys()),
                            index=list(menus.keys()).index(st.session_state.current_category))
    if cat_sel != st.session_state.current_category:
        st.session_state.current_category = cat_sel
        st.session_state.current_page = menus[cat_sel][0]
        st.rerun()
    cur_pages = menus.get(st.session_state.current_category, [])
    cur_idx = cur_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_pages else 0
    sel = st.selectbox("메뉴", cur_pages, index=cur_idx)
    if sel != st.session_state.current_page:
        st.session_state.current_page = sel
        st.rerun()


def _render_season_banner(market, theme_color):
    from datetime import datetime
    sn  = market.get("season_num", 1)
    end = market.get("season_end", time.time() + 30 * 86400)
    rem = max(0, int(end - time.time()))
    days, hours = rem // 86400, (rem % 86400) // 3600
    end_str = datetime.fromtimestamp(end, KST).strftime("%Y-%m-%d %H:%M")
    st.markdown(
        f"<div style='background:linear-gradient(90deg,rgba(0,229,255,0.1),rgba(0,0,0,0));"
        f"border-left:4px solid {theme_color};padding:10px 15px;margin-bottom:20px;border-radius:0 10px 10px 0;'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;'>"
        f"<span style='color:{theme_color};font-weight:900;font-size:1.1rem;'>제 {sn}기 유니버스</span>"
        f"<div style='text-align:right;'>"
        f"<div style='color:#FF4B4B;font-weight:700;font-size:0.9rem;'>🏁 시즌 종료 임박</div>"
        f"<div style='color:#DDD;font-size:0.8rem;'>{end_str} ({days}일 {hours}시간 남음)</div>"
        f"</div></div></div>",
        unsafe_allow_html=True,
    )
