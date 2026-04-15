# app.py
# 로그인과 메뉴 네비게이션을 담당하며 선택한 메뉴에 따라 페이지의 폴더 안의 모듈호출
import streamlit as st
import time
import os
from datetime import datetime

# ==============================
# 1. 코어 모듈 임포트
# ==============================
from utils.config import MARKET_FILE, USERS_FILE, KST
from utils.database import load_db, save_db
from utils.core import hash_pw, format_korean_money, get_net_worth, sync_user_data, ADMIN_PW, ADMIN_HASH
from utils.market_sync import run_market_sync
from utils.css import GLOBAL_CSS

# ==============================
# 2. 페이지 기본 설정 및 CSS 주입
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v18.2", page_icon="🌌", layout="wide", initial_sidebar_state="collapsed")
st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)

# ==============================
# 3. 로그인 및 세션 관리
# ==============================
market = load_db(MARKET_FILE, {}) # 로그인 전 임시 로드
if 'logged_in_user' not in st.session_state:
    st.markdown("""
<style>
.stApp { background: radial-gradient(ellipse at 20% 50%, #0d0221 0%, #050510 60%, #000 100%) !important; }
.login-title { font-family:'Orbitron',monospace !important; font-size:clamp(2rem,6vw,4rem) !important; font-weight:900; text-align:center; background:linear-gradient(135deg,#00E5FF 0%,#FF00FF 50%,#FFD600 100%); -webkit-background-clip:text; -webkit-text-fill-color:transparent; padding:20px 0 5px 0; letter-spacing:4px; animation:glow 3s ease-in-out infinite alternate; }
@keyframes glow { from{filter:drop-shadow(0 0 10px #00E5FF)} to{filter:drop-shadow(0 0 30px #FF00FF)} }
.login-sub { text-align:center; color:#888 !important; font-size:1rem; margin-bottom:20px; letter-spacing:3px; }
</style>""", unsafe_allow_html=True)

    st.markdown("<div class='login-title'>🌌 HYOMIN UNIVERSE</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='login-sub'>∙ 자본주의 생존 시뮬레이션 시즌 {market.get('season_num', 1)} ∙</div>", unsafe_allow_html=True)

    # ==============================
    # 🌠 게임 소개 및 서버 점검 스플래시 패널
    # ==============================
    st.markdown("""
<div style='background: linear-gradient(135deg, rgba(15, 20, 35, 0.9), rgba(5, 10, 15, 0.95)); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 16px; padding: 30px; margin-bottom: 20px; max-width: 850px; margin-left: auto; margin-right: auto; box-shadow: 0 10px 30px rgba(0, 229, 255, 0.1);'>
<div style='text-align: center; margin-bottom: 25px;'>
<div style='font-size: 3.5rem; margin-bottom: 10px;'>🌌</div>
<h2 style='color: #00E5FF; margin: 0; font-family: "Orbitron", sans-serif; letter-spacing: 2px;'>WELCOME TO HYOMIN UNIVERSE</h2>
<p style='color: #94A3B8; font-size: 1rem; line-height: 1.6; margin-top: 10px;'>
주식, 코인, 부동산부터 짜릿한 카지노와 하이퍼카 레이싱까지.<br>
우주 최고의 억만장자가 되기 위한 <b>무한한 자본주의 생존 시뮬레이션</b>에 합류하세요!
</p>
</div>
<div style='display: flex; gap: 20px; flex-wrap: wrap;'>
<div style='flex: 1; min-width: 300px; background: linear-gradient(135deg, rgba(255, 75, 75, 0.1), rgba(0, 0, 0, 0.4)); border: 1px solid rgba(255, 75, 75, 0.4); border-radius: 12px; padding: 20px; position: relative; overflow: hidden;'>
<div style='position: absolute; top: -15px; right: -15px; font-size: 5rem; opacity: 0.1;'>🛠️</div>
<h4 style='color: #FF4B4B; margin-top: 0; display: flex; align-items: center; gap: 8px; font-size: 1.1rem;'>
<span>🚨</span> 시스템 대공사 및 재시작 안내
</h4>
<p style='color: #E2E8F0; font-size: 0.9rem; line-height: 1.7; margin-bottom: 0;'>
데이터베이스를 <b>외부 클라우드(MongoDB)로 완벽 분리</b>하고 <b>37개 모듈화 설계</b>를 적용하여 서버 안정성을 극대화했습니다. 유저 자산은 이제 영구히 안전합니다!
</p>
</div>
<div style='flex: 1; min-width: 300px; background: linear-gradient(135deg, rgba(255, 214, 0, 0.1), rgba(0, 0, 0, 0.4)); border: 1px solid rgba(255, 214, 0, 0.4); border-radius: 12px; padding: 20px; position: relative; overflow: hidden;'>
<div style='position: absolute; top: -15px; right: -15px; font-size: 5rem; opacity: 0.1;'>🏆</div>
<h4 style='color: #FFD600; margin-top: 0; display: flex; align-items: center; gap: 8px; font-size: 1.1rem;'>
<span>🏆</span> 정규 시즌 1 공식 개막
</h4>
<p style='color: #E2E8F0; font-size: 0.9rem; line-height: 1.7; margin-bottom: 0;'>
<b>[시즌 기간]</b> 2026년 4월 15일 ~ 5월 15일<br>
새로운 시즌의 시작을 기념하여 모든 시민분들께 <b>초기 정착금 5억 원</b>을 즉시 지급합니다! 💸
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # ==============================
    # 🔍 시스템 아키텍처 상세 안내 (HTML 전용 디자인)
    # ==============================
    st.markdown("""
<div style='background: rgba(0, 229, 255, 0.03); border: 1px dashed rgba(0, 229, 255, 0.3); border-radius: 12px; padding: 20px; max-width: 850px; margin: 0 auto 35px auto;'>
<div style='display: flex; align-items: center; gap: 10px; margin-bottom: 15px;'>
<span style='font-size: 1.5rem;'>🔍</span>
<h4 style='color: #00E5FF; margin: 0; font-family: "Orbitron", sans-serif; font-size: 1rem;'>SYSTEM ARCHITECTURE & MODULES</h4>
</div>
<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;'>
<div style='background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 8px;'>
<div style='color: #FFD600; font-weight: 800; font-size: 0.85rem; margin-bottom: 5px;'>🛡️ Data Integrity</div>
<div style='color: #94A3B8; font-size: 0.75rem; line-height: 1.5;'>
MongoDB Atlas 클라우드를 통한 자산 실시간 백업 및 SHA-256 암호화 보안 적용.
</div>
</div>
<div style='background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 8px;'>
<div style='color: #00FF88; font-weight: 800; font-size: 0.85rem; margin-bottom: 5px;'>⚙️ Modular Logic</div>
<div style='color: #94A3B8; font-size: 0.75rem; line-height: 1.5;'>
37개 독립 모듈 구조로 경제 시뮬레이션 및 미니게임 로직의 안정성 극대화.
</div>
</div>
<div style='background: rgba(255, 255, 255, 0.03); padding: 12px; border-radius: 8px;'>
<div style='color: #00E5FF; font-weight: 800; font-size: 0.85rem; margin-bottom: 5px;'>🔄 Market Sync</div>
<div style='color: #94A3B8; font-size: 0.75rem; line-height: 1.5;'>
사용자 부재 시에도 시간당 주가/이자/임대료를 자동 계산하는 타임 슬롯 시스템.
</div>
</div>
</div>
<div style='margin-top: 15px; padding: 10px; border-top: 1px solid rgba(255,255,255,0.05); text-align: center;'>
<p style='color: #64748B; font-size: 0.7rem; margin: 0;'>
Core Engine: Python 3.10+ | Framework: Streamlit v18.2 Modular Edition
</p>
</div>
</div>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            if st.button("🚀 유니버스 입장", use_container_width=True):
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
                    })
                    st.rerun()

                if l_id == "admin" and hash_pw(l_pw) == ADMIN_HASH:
                    if "admin" not in users:
                        users["admin"] = {"pw":"****","cash":999_999_999_999,"inventory":[], "equipped_title":"👑 절대신 창조주"}
                        save_db(USERS_FILE, users)
                    _do_login("admin")
                elif l_id != "admin" and l_id in users and users[l_id]['pw'] == hash_pw(l_pw):
                    _do_login(l_id)
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")
                    
        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 시민 등록하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                clean_id = n_id.strip()
                if clean_id in users or clean_id == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(clean_id) < 2:
                    st.error("⚠️ 아이디는 공백을 제외하고 2자 이상이어야 합니다.")
                else:
                    users[clean_id] = {
                        "pw":hash_pw(n_pw), "cash":500_000_000, "inventory":[], "equipped_title":"🌱 신규시민",
                        "portfolio":{}, "real_estate":{}, "rent_time":time.time(), "loan":0, "loan_time":time.time()
                    }
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 정착금 5억원이 지급되었습니다!")
    st.stop()

# ==============================
# 4. 로그인 후 데이터 동기화
# ==============================
market = run_market_sync()
nw = get_net_worth(st.session_state.logged_in_user, market)

if st.session_state.loan > 0 and nw < 0:
    st.session_state.equipped_title = "💸 신용불량자"
    sync_user_data()

# ==============================
# 5. 메뉴 및 라우팅 시스템
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
    "👥 커뮤니티": ["🏰 길드/클랜", "🏅 [시즌2]랭킹 & 게시판", "✉️ 개인 쪽지함"],
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
# 6. 페이지 라우팅 실행
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
elif menu == "🏅 [시즌2]랭킹 & 게시판":
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
