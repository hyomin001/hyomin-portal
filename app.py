import time
import random
import streamlit as st

from config import stock_config, USERS_FILE
from database import (
    load_db, save_db, get_market, save_market,
    get_net_worth, sync_user_data,
)
from auth import render_login
from styles import apply_css
from views import (
    home, vip, trading, real_estate, bank,
    lotto, soccer, cbt, racing, slots,
    mining, title_shop, tx_history, rankings, admin,
)

# ── 페이지 설정 ──
st.set_page_config(page_title="HYOMIN UNIVERSE v17", page_icon="🌌", layout="wide")

# ── 로그인 (미로그인 시 st.stop()) ──
render_login()

# ── CSS 적용 ──
IS_PC = apply_css()

# ════════════════════════════════════
# 서버 마켓 동기화
# ════════════════════════════════════
market = get_market()
cur_t  = time.time()
m_up   = False

if cur_t - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]
        ch = (random.random() - 0.5) * 2 * s['vol']
        if market.get('event_active') and market.get('event_target') == s['id']:
            ch *= market.get('event_multiplier', 1.5)
        curr['price'] = round(max(1_000, curr['price'] * (1 + ch)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 60: curr['history'].pop(0)
    market['last_tick'] = cur_t
    m_up = True

if cur_t - market.get('news_time', 0) > 30:
    tid, imp = market['next_news_target'], market['next_news_impact']
    t_nm = next((s['name'] for s in stock_config if s['id'] == tid), tid)
    market['stock_data'][tid]['price'] = int(market['stock_data'][tid]['price'] * (1 + imp))
    direction = "급등" if imp > 0.1 else "강세" if imp > 0 else "급락" if imp < -0.1 else "약세"
    headlines = {
        "급등": [f"🚀 [속보] {t_nm}, 실적 서프라이즈로 장중 {direction}!", f"📈 [단독] {t_nm} 대규모 외국인 매수세 포착!"],
        "강세": [f"📊 [마감] {t_nm} 기관 꾸준한 매집 행보!", f"💡 [분석] {t_nm}, 업황 개선 기대감 반영"],
        "급락": [f"❄️ [속보] {t_nm}, 악재 공시로 투자자 충격!", f"📉 [단독] {t_nm} 대규모 기관 이탈!"],
        "약세": [f"⚠️ [마감] {t_nm}, 차익 실현 매물 출회", f"🔍 [분석] {t_nm} 단기 조정 국면"],
    }
    market['news'] = random.choice(headlines.get(direction, [f"📰 {t_nm} 시황 변동"]))
    market['news_time'] = cur_t
    market['next_news_target'] = random.choice(stock_config)['id']
    market['next_news_impact'] = random.uniform(-0.25, 0.25)
    m_up = True

if cur_t - market.get('lotto_last_draw', 0) > 3600:
    if market['lotto_tickets']:
        pool = []
        for u, c in market['lotto_tickets'].items(): pool.extend([u] * c)
        win = random.choice(pool)
        prize = market['lotto_pool']
        us = load_db(USERS_FILE, {})
        if win in us:
            us[win]['cash'] += prize
            save_db(USERS_FILE, us)
            if win == st.session_state.logged_in_user:
                st.session_state.global_cash += prize
        market['news'] = f"🎊 [당첨 확정] {win}님이 ₩{prize:,} 대박 상금을 수령하셨습니다!!"
        market['lotto_pool'] = 5_000_000_000
        market['lotto_tickets'] = {}
        market['lotto_last_draw'] = cur_t
        m_up = True

if m_up: save_market(market)

# ── 대출 이자 ──
if st.session_state.loan > 0:
    cyc = int((cur_t - st.session_state.loan_time) / 10)
    if cyc > 0:
        st.session_state.loan = int(st.session_state.loan * (1.02 ** cyc))
        st.session_state.loan_time += cyc * 10
        sync_user_data()

nw = get_net_worth(st.session_state.logged_in_user, market)
if st.session_state.loan > 0 and nw < 0:
    st.session_state.equipped_title = "💸 신용불량자"
    sync_user_data()

# ════════════════════════════════════
# 메뉴
# ════════════════════════════════════
is_admin = st.session_state.logged_in_user == "5891"
is_vip   = nw >= 100_000_000_000 or is_admin

menu_ops = [
    "🏠 홈 광장",
    "📈 주식 트레이딩",
    "🏢 부동산 수금소",
    "🏦 은행 (대출/송금)",
    "⚔️ 글로벌 로또",
    "⚽ 구단주 시뮬레이터",
    "💻 정처기 CBT",
    "🏎️ 하이퍼카 레이싱",
    "🎰 럭키 슬롯",
    "⛏️ 광산 (노가다)",
    "👑 칭호 상점",
    "📜 내 거래 기록",
    "🏅 랭킹 & 게시판",
]
if is_vip:   menu_ops.insert(2, "💎 VIP 라운지")
if is_admin: menu_ops.append("🛠️ 창조주 통제소")

if IS_PC:
    with st.sidebar:
        st.markdown(f"""
<div style='padding:16px;background:rgba(0,229,255,0.05);border-radius:12px;
     border:1px solid rgba(0,229,255,0.2);margin-bottom:16px;'>
  <div style='font-size:1.3rem;font-weight:900;color:#00E5FF;'>👤 {st.session_state.logged_in_user}</div>
  <div style='font-size:0.85rem;color:#FFD600;margin-top:4px;'>{st.session_state.equipped_title}</div>
</div>""", unsafe_allow_html=True)
        st.metric("💵 현금",   f"₩{st.session_state.global_cash:,.0f}")
        st.metric("📊 순자산", f"₩{nw:,.0f}")
        if st.session_state.loan > 0:
            st.metric("💳 대출잔액", f"₩{st.session_state.loan:,.0f}")
        st.write("---")
        menu = st.radio("메뉴", menu_ops, label_visibility="collapsed")
        st.write("---")
        if st.button("🔓 로그아웃", use_container_width=True):
            sync_user_data(); st.session_state.clear(); st.rerun()
else:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"<div style='font-size:0.82rem;color:#888;'>👤 <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b> | {st.session_state.equipped_title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.9rem;color:#FFD600;font-weight:900;'>💵 ₩{st.session_state.global_cash:,}</div>", unsafe_allow_html=True)
    with col_b:
        if st.button("로그아웃"):
            sync_user_data(); st.session_state.clear(); st.rerun()
    menu = st.selectbox("메뉴 선택", menu_ops, label_visibility="collapsed")

# ── 뉴스 배너 ──
st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
if market.get('admin_msg'):
    col = market.get('admin_color', '#FF4B4B')
    st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {col};border-radius:10px;padding:12px 16px;color:{col}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {market['admin_msg']}</div>", unsafe_allow_html=True)

# ════════════════════════════════════
# 페이지 라우팅
# ════════════════════════════════════
if   menu == "💎 VIP 라운지":       vip.render(market, nw)
elif menu == "🏠 홈 광장":          home.render(market, nw)
elif menu == "📈 주식 트레이딩":    trading.render(market)
elif menu == "🏢 부동산 수금소":    real_estate.render()
elif menu == "🏦 은행 (대출/송금)": bank.render(nw)
elif menu == "⚔️ 글로벌 로또":     lotto.render(market)
elif menu == "⚽ 구단주 시뮬레이터":soccer.render()
elif menu == "💻 정처기 CBT":       cbt.render()
elif menu == "🏎️ 하이퍼카 레이싱": racing.render()
elif menu == "🎰 럭키 슬롯":       slots.render(market)
elif menu == "⛏️ 광산 (노가다)":   mining.render(market)
elif menu == "👑 칭호 상점":        title_shop.render()
elif menu == "📜 내 거래 기록":     tx_history.render()
elif menu == "🏅 랭킹 & 게시판":   rankings.render(market)
elif menu == "🛠️ 창조주 통제소":   admin.render(market)
