# app.py
import streamlit as st
import time
import os
from datetime import datetime

# ==============================
# 1. 코어 모듈 임포트
# ==============================
from utils.config import MARKET_FILE, USERS_FILE, KST
from utils.database import load_db, save_db
from utils.core import hash_pw, format_korean_money, get_net_worth, sync_user_data, ADMIN_HASH, pull_user_data
from utils.market_sync import run_market_sync
from utils.css import GLOBAL_CSS

# ==============================
# 2. 페이지 기본 설정 및 CSS 주입
# ==============================
st.set_page_config(page_title="HYOMIN PORTAL", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")
st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

# [핵심 방어막] 사용자의 행동 전 최신 정보 강제 동기화 (로그인 된 경우에만 작동함)
pull_user_data()

# 라우팅(화면 이동)을 위한 세션 상태 초기화
if "page_view" not in st.session_state:
    st.session_state.page_view = "portal"  # 항상 첫 화면은 포털 메인

market = load_db(MARKET_FILE, {}) # 임시 로드

# ==============================
# 3. [View 1] 포털 메인 화면 (로그인 불필요, 신뢰감 주는 디자인)
# ==============================
if st.session_state.page_view == "portal":
    # 신뢰감을 주는 딥 네이비 & 깔끔한 블루 UI 스타일
    st.markdown("""
        <style>
        .portal-header {
            text-align: center;
            padding: 40px 0 20px 0;
            color: #E2E8F0;
        }
        .portal-title {
            font-family: 'Inter', sans-serif;
            font-size: 3rem;
            font-weight: 900;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #4B9EFF, #00E5FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .trust-badge {
            display: inline-block;
            background: rgba(75, 158, 255, 0.1);
            border: 1px solid rgba(75, 158, 255, 0.3);
            color: #4B9EFF;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .banner-card {
            background: #111827; /* 다크 네이비 */
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            border: 1px solid #1F2937;
            transition: all 0.3s ease;
            margin-bottom: 20px;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .banner-card:hover {
            border-color: #4B9EFF;
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(75, 158, 255, 0.15);
        }
        </style>
    """, unsafe_allow_html=True)

    # 상단 로그인/내정보 바
    col_empty, col_btn = st.columns([8, 2])
    with col_btn:
        if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
            st.markdown(f"<div style='text-align:right; color:#94A3B8; margin-bottom:5px;'>👤 {st.session_state.logged_in_user}님</div>", unsafe_allow_html=True)
            if st.button("로그아웃", use_container_width=True):
                sync_user_data()
                st.session_state.clear()
                st.rerun()
        else:
            if st.button("🔑 로그인 / 회원가입", use_container_width=True):
                st.session_state.page_view = "login"
                st.rerun()

    # 포털 헤더
    st.markdown("""
        <div class='portal-header'>
            <div class='trust-badge'>🛡️ HYOMIN NETWORKS SECURE PLATFORM</div>
            <div class='portal-title'>HYOMIN PORTAL</div>
            <p style='color: #94A3B8; font-size: 1.1rem; max-width: 600px; margin: 0 auto;'>
                하나의 계정으로 효민 유니버스의 모든 경제, 엔터테인먼트, 커뮤니티 서비스를 안전하게 이용하세요.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    
    # 배너 섹션 (클릭 시 로그인 체크 로직 추가)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='banner-card'><h2>🌌 효민 유니버스</h2><p style='color:#94A3B8;'>자본주의 생존 시뮬레이션 시즌 1</p></div>", unsafe_allow_html=True)
        if st.button("유니버스 입장하기 🚀", use_container_width=True):
            if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
                st.session_state.page_view = "universe"
            else:
                st.warning("⚠️ 해당 서비스를 이용하시려면 먼저 로그인해주세요.")
                time.sleep(1)
                st.session_state.page_view = "login"
            st.rerun()

        st.markdown("<div class='banner-card'><h2>📊 하이엔드 퀀트 투자</h2><p style='color:#94A3B8;'>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b2", disabled=True, use_container_width=True)

        st.markdown("<div class='banner-card'><h2>🤝 클랜 연합 커뮤니티</h2><p style='color:#94A3B8;'>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b4", disabled=True, use_container_width=True)

    with col2:
        st.markdown("<div class='banner-card'><h2>🎮 HYOMIN 아케이드</h2><p style='color:#94A3B8;'>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b1", disabled=True, use_container_width=True)

        st.markdown("<div class='banner-card'><h2>🏢 글로벌 부동산 플랫폼</h2><p style='color:#94A3B8;'>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b3", disabled=True, use_container_width=True)

        st.markdown("<div class='banner-card'><h2>🤖 AI 비서 서비스</h2><p style='color:#94A3B8;'>Coming Soon...</p></div>", unsafe_allow_html=True)
        st.button("준비 중...", key="b5", disabled=True, use_container_width=True)

    # 포털 푸터
    st.markdown("""
        <div style='text-align: center; padding: 40px 0; color: #64748B; font-size: 0.8rem;'>
            <p>ⓒ 2026 HYOMIN PORTAL INC. All rights reserved.</p>
            <p>Powered by MongoDB Atlas & Streamlit Cloud</p>
        </div>
    """, unsafe_allow_html=True)
    st.stop()


# ==============================
# 4. [View 2] 로그인 / 회원가입 화면
# ==============================
elif st.session_state.page_view == "login":
    
    if st.button("🔙 포털 메인으로 돌아가기"):
        st.session_state.page_view = "portal"
        st.rerun()

    st.markdown("<div style='text-align:center; padding: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#4B9EFF;'>HYOMIN ID 로그인</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8;'>안전한 서비스 이용을 위해 로그인해주세요.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])
        
        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            if st.button("🚀 로그인 및 계속하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                def _do_login(uid):
                    u = users[uid]
                    st.session_state.update({
                        'logged_in_user': uid,
                        'global_cash':    u['cash'],
                        'inventory':      u.get('inventory', []),
                        'equipped_title': u.get('equipped_title', '🌱 신규시민'),
                        'portfolio':      u.get('portfolio', {}),
                        'real_estate':    u.get('real_estate', {}),
                        'rent_time':      u.get('rent_time', time.time()),
                        'loan':           u.get('loan', 0),
                        'loan_time':      u.get('loan_time', time.time()),
                        'device_mode':    device_mode,
                        'crypto_portfolio': u.get('crypto_portfolio', {}),
                        'daily_quests':     u.get('daily_quests', {}),
                        'weapon_level':   u.get('weapon_level', 0), 
                        'bulk_trade_count': u.get('bulk_trade_count', 0),
                        'last_estate_reset': u.get('last_estate_reset', 0),
                    })
                    # 로그인 성공 시 포털로 돌아감
                    st.success("로그인 성공!")
                    time.sleep(0.5)
                    st.session_state.page_view = "portal"
                    st.rerun()

                if l_id == "admin" and hash_pw(l_pw) == ADMIN_HASH:
                    if "admin" not in users:
                        users["admin"] = {"pw": ADMIN_HASH, "cash": 999_999_999_999, "inventory": [], "equipped_title": "👑 절대신 창조주"}
                        save_db(USERS_FILE, users)
                    _do_login("admin")
                elif l_id != "admin" and l_id in users and users[l_id]['pw'] == hash_pw(l_pw):
                    _do_login(l_id)
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")
                    
        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 계정 생성하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                clean_id = n_id.strip()
                if clean_id in users or clean_id == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(clean_id) < 2:
                    st.error("⚠️ 아이디는 공백을 제외하고 2자 이상이어야 합니다.")
                elif len(n_pw) < 4:
                    st.error("⚠️ 비밀번호는 4자 이상이어야 합니다.")
                else:
                    users[clean_id] = {
                        "pw":hash_pw(n_pw), "cash":500_000_000, "inventory":[], "equipped_title":"🌱 신규시민",
                        "portfolio":{}, "real_estate":{}, "rent_time":time.time(), "loan":0, "loan_time":time.time(),
                        "last_estate_reset": 0, "bulk_trade_date": "", "bulk_trade_count": 0,
                    }
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 로그인 탭에서 로그인해주세요.")
    st.stop()


# ==============================
# 5. [View 3] 효민 유니버스 (인게임 로직)
# ==============================
elif st.session_state.page_view == "universe":
    
    # 비정상 접근(로그인 안하고 직접 URL 등) 차단
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"
        st.rerun()

    # 상단에 포털로 돌아가는 버튼 추가
    st.markdown("<div style='margin-bottom: 15px;'>", unsafe_allow_html=True)
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    market = run_market_sync()

    # 순자산 계산
    def _calc_nw_from_session(market_data):
        from utils.config import estate_config, FORGE_DATA
        w = st.session_state.global_cash - st.session_state.loan
        prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
        for sid, p_data in st.session_state.portfolio.items():
            if sid in prices: w += p_data.get('qty', 0) * prices[sid]
        for cid, cinfo in st.session_state.get('crypto_portfolio', {}).items():
            price = market_data.get('crypto_data', {}).get(cid, {}).get('price', 0)
            w += cinfo.get('qty', 0) * price
        for eid, count in st.session_state.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
        w_lv = st.session_state.get('weapon_level', 0)
        if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
        return w

    nw = _calc_nw_from_session(market)

    if st.session_state.loan > 0 and nw < 0:
        st.session_state.equipped_title = "💸 신용불량자"
        sync_user_data()

    # ==============================
    # 6. 메뉴 및 라우팅 시스템
    # ==============================
    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"

    is_admin = st.session_state.logged_in_user == "admin"
    is_vip   = nw >= 100_000_000_000 or is_admin

    CATEGORY_MENUS = {
        "📈 경제": ["🏠 홈 광장 (튜토리얼)", "📈 주식 트레이딩", "🪙 코인 거래소", "🏢 부동산 거래소", "🏦 은행 (대출/송금)", "📜 내 거래 기록"],
        "🎮 미니게임": ["🎰 럭키 슬롯", "🃏 블랙잭 카지노", "⛏️ 광산 (노가다)", "💻 정처기 CBT", "⚔️ 글로벌 로또", "🗡️ 전설의 명검 강화", "🎴 가챠 뽑기"],
        "🌟 성장 & 혜택": ["📅 일일 퀘스트", "👑 칭호 상점"],
        "⚽ 스포츠": ["⚽ 구단주 시뮬레이터", "⚽ 조기축구 승부차기", "🏎️ 하이퍼카 레이싱", "🛠️ 커스텀 튜닝 차고지"],
        "👥 커뮤니티": ["🏰 길드/클랜", "🏅 [시즌1]랭킹 & 게시판", "✉️ 개인 쪽지함"],
    }
    if is_vip: CATEGORY_MENUS["📈 경제"].insert(1, "💎 VIP 라운지")
    if is_admin: CATEGORY_MENUS["⚙️ 관리"] = ["🛠️ 창조주 통제소"]

    def get_current_category():
        for cat, pages in CATEGORY_MENUS.items():
            if st.session_state.current_page in pages: return cat
        return list(CATEGORY_MENUS.keys())[0]

    if "current_category" not in st.session_state:
        st.session_state.current_category = get_current_category()

    # UI 분기 (PC / 모바일)
    msg_db_check = load_db("messages_db.json", {})
    my_unread = sum(1 for m in msg_db_check.get(st.session_state.logged_in_user, {}).get("inbox", []) if not m.get("read", False))
    unread_txt = f" 🔴{my_unread}" if my_unread > 0 else ""

    is_pc_mode = "PC" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

    if is_pc_mode:
        with st.sidebar:
            st.markdown(f"<div style='padding:14px; background:rgba(255,255,255,0.05); border:1px solid #00E5FF; border-radius:10px; margin-bottom:14px;'><div style='color:#00E5FF;font-size:0.8rem;'>{st.session_state.equipped_title}</div><div style='font-size:1rem;font-weight:700;'>{st.session_state.logged_in_user}{unread_txt}</div></div>", unsafe_allow_html=True)
            st.metric("💵 현금", format_korean_money(st.session_state.global_cash))
            st.metric("📊 순자산", format_korean_money(nw))
            st.write("---")
            
            for cat in CATEGORY_MENUS:
                if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                    st.session_state.current_category = cat
                    st.session_state.current_page = CATEGORY_MENUS[cat][0]
                    st.rerun()
                    
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
            st.session_state.current_category, st.session_state.current_page = cat_sel, CATEGORY_MENUS[cat_sel][0]
            st.rerun()

        cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
        cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
        selected_menu = st.selectbox("메뉴 선택", cur_cat_pages, index=cur_idx)
        if selected_menu != st.session_state.current_page:
            st.session_state.current_page = selected_menu; st.rerun()

    # 공통 뉴스 배너
    st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
    if market.get('admin_msg'):
        st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {market.get('admin_color','#FF4B4B')};border-radius:10px;padding:12px;color:{market.get('admin_color','#FF4B4B')}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {market['admin_msg']}</div>", unsafe_allow_html=True)

    # ==============================
    # 7. 페이지 라우팅 실행
    # ==============================
    menu = st.session_state.current_page

    if menu == "🏠 홈 광장 (튜토리얼)":
        from pages import home; home.render(market, nw)
    elif menu == "💎 VIP 라운지":
        from pages import vip; vip.render(market, nw)
    elif menu == "📈 주식 트레이딩":
        from pages import stock; stock.render(market, nw)
    elif menu == "🪙 코인 거래소":
        from pages import crypto; crypto.render(market, nw)
    elif menu == "🏢 부동산 거래소":
        from pages import real_estate; real_estate.render(market, nw)
    elif menu == "🏦 은행 (대출/송금)":
        from pages import bank; bank.render(market, nw)
    elif menu == "📜 내 거래 기록":
        from pages import txlog; txlog.render(market, nw)
    elif menu == "📅 일일 퀘스트":
        from pages import quest; quest.render(market, nw)
    elif menu == "👑 칭호 상점":
        from pages import title_shop; title_shop.render(market, nw)
    elif menu == "🏅 [시즌1]랭킹 & 게시판":
        from pages import ranking; ranking.render(market, nw)
    elif menu == "✉️ 개인 쪽지함":
        from pages import dm; dm.render(market, nw)
    elif menu == "🏰 길드/클랜":
        from pages import clan; clan.render(market, nw)
    elif menu == "🎰 럭키 슬롯":
        from pages import games
        from pages.games import slot; slot.render(market, nw)
    elif menu == "🃏 블랙잭 카지노":
        from pages.games import blackjack; blackjack.render(market, nw)
    elif menu == "⛏️ 광산 (노가다)":
        from pages.games import mine; mine.render(market, nw)
    elif menu == "💻 정처기 CBT":
        from pages.games import quiz; quiz.render(market, nw)
    elif menu == "⚔️ 글로벌 로또":
        from pages.games import lotto; lotto.render(market, nw)
    elif menu == "🗡️ 전설의 명검 강화":
        from pages.games import forge; forge.render(market, nw)
    elif menu == "🎴 가챠 뽑기":
        from pages.games import gacha; gacha.render(market, nw)
    elif menu == "⚽ 구단주 시뮬레이터":
        from pages.sports import soccer_sim; soccer_sim.render(market, nw)
    elif menu == "⚽ 조기축구 승부차기":
        from pages.sports import penalty; penalty.render(market, nw)
    elif menu == "🏎️ 하이퍼카 레이싱":
        from pages.sports import racing; racing.render(market, nw)
    elif menu == "🛠️ 커스텀 튜닝 차고지":
        from pages.sports import garage; garage.render(market, nw)
    elif menu == "🛠️ 창조주 통제소":
        from pages.admin import panel; panel.render(market, nw)
    else:
        st.info(f"🚧 '{menu}' 페이지는 존재하지 않거나 로드할 수 없습니다.")
