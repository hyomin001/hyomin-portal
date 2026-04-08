import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random
import json
import os
import time
from datetime import datetime

# ==============================
# 시스템 설정 및 데이터베이스
# ==============================
USERS_FILE = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE = "market_db.json" 

stock_config = [
    {"id": "NDX", "name": "나스닥100 ETF", "vol": 0.04},       
    {"id": "HDEC", "name": "현대건설", "vol": 0.03},            
    {"id": "MANU", "name": "맨체스터 유나이티드", "vol": 0.06}, 
    {"id": "CJENM", "name": "CJ ENM", "vol": 0.04},             
    {"id": "FOOD", "name": "삼양식품", "vol": 0.03},            
    {"id": "BIO", "name": "삼성바이오로직스", "vol": 0.05},     
    {"id": "AERO", "name": "한화에어로스페이스", "vol": 0.06},  
    {"id": "RETAIL", "name": "신세계", "vol": 0.02},            
    {"id": "CHEM", "name": "LG화학", "vol": 0.03},              
    {"id": "ENTER", "name": "하이브", "vol": 0.07}              
]

estate_config = {
    "E1": {"name": "역세권 원룸", "price": 10000000000, "income": 10000},       
    "E2": {"name": "초대형 PC방", "price": 50000000000, "income": 50000},       
    "E3": {"name": "강남 꼬마빌딩", "price": 500000000000, "income": 500000},    
    "E4": {"name": "시그니엘 펜트하우스", "price": 5000000000000, "income": 5000000} 
}

def load_db(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return default
    return default

def save_db(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return 0
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices: w += p_data.get('qty', 0) * prices[sid]
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config: w += estate_config[eid]['price'] * count * 0.8
    return w

def sync_user_data():
    if 'logged_in_user' in st.session_state:
        users = load_db(USERS_FILE, {})
        uid = st.session_state.logged_in_user
        if uid in users:
            users[uid].update({
                'cash': st.session_state.global_cash, 'inventory': st.session_state.inventory,
                'equipped_title': st.session_state.equipped_title, 'portfolio': st.session_state.portfolio,
                'real_estate': st.session_state.real_estate, 'rent_time': st.session_state.rent_time,
                'loan': st.session_state.loan, 'loan_time': st.session_state.loan_time
            }); save_db(USERS_FILE, users)

def get_market():
    def init_m():
        data = {
            "version": 5, "stock_data": {s['id']: {"name": s['name'], "price": random.randint(50000, 150000), "history": [80000]} for s in stock_config},
            "news": "시장이 개장되었습니다.", "news_time": time.time(), "last_tick": time.time(), "admin_msg": "",
            "lotto_pool": 5000000000, "lotto_tickets": {}, "lotto_last_draw": time.time(),
            "next_news_target": random.choice(stock_config)['id'], "next_news_impact": random.uniform(-0.2, 0.2)
        }
        return data
    if not os.path.exists(MARKET_FILE):
        d = init_m(); save_db(MARKET_FILE, d); return d
    d = load_db(MARKET_FILE, {})
    if d.get("version") != 5:
        d = init_m(); save_db(MARKET_FILE, d); return d
    return d

def save_market(data): save_db(MARKET_FILE, data)

st.set_page_config(page_title="HYOMIN UNIVERSE v15.0", page_icon="💎", layout="wide")

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align:center; color:#00E5FF;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tab_log = st.tabs(["🔑 로그인", "📝 시민등록"])
        with tab_log[0]:
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {"pw": "5891", "cash": 999999999999, "inventory": [], "equipped_title": "👑 절대신 창조주", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                        save_db(USERS_FILE, users)
                    st.session_state.update({'logged_in_user': "5891", 'global_cash': users["5891"]['cash'], 'inventory': users["5891"]['inventory'], 'equipped_title': "👑 절대신 창조주", 'portfolio': {}, 'real_estate': {}, 'rent_time': time.time(), 'loan': 0, 'loan_time': time.time(), 'device_mode': device_mode}); st.rerun()
                elif l_id in users and users[l_id]['pw'] == l_pw:
                    u = users[l_id]
                    st.session_state.update({'logged_in_user': l_id, 'global_cash': u['cash'], 'inventory': u['inventory'], 'equipped_title': u.get('equipped_title','신규시민'), 'portfolio': u.get('portfolio',{}), 'real_estate': u.get('real_estate',{}), 'rent_time': u.get('rent_time', time.time()), 'loan': u.get('loan', 0), 'loan_time': u.get('loan_time', time.time()), 'device_mode': device_mode}); st.rerun()
                else: st.error("정보 불일치")
        with tab_log[1]:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록"):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "5891": st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                    save_db(USERS_FILE, users); st.success("가입 성공!")
    st.stop()

# ==============================
# 🎨 CSS (모바일 레이아웃 파괴 버그 수정본)
# ==============================
css_base = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    /* 앱 배경 검정, 기본 텍스트 하양 */
    .stApp { background-color: #050505 !important; }
    html, body, p, span, label, h1, h2, h3, button, input, th, td { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; }
    
    /* 선택창 (입력 부분) */
    div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
    
    /* 선택창 (드롭다운 목록) - 모바일 버그 방지를 위해 role="listbox" 타겟팅 */
    div[role="listbox"] { background-color: #FFFFFF !important; border: 2px solid #00E5FF !important; border-radius: 8px; }
    div[role="listbox"] li, div[role="listbox"] span { color: #000000 !important; font-weight: 900 !important; }
    div[role="listbox"] li:hover, div[role="listbox"] li:hover span { background-color: #00E5FF !important; color: #000000 !important; }
    
    /* 주식 테이블 */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 2px solid #444; }
    .stock-table th { background-color: #333; color: #FFD600 !important; text-align: center; }
    .stock-table td { border-bottom: 1px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }
    
    /* 스코어보드 스타일 */
    .scoreboard { 
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 3px solid #00E5FF;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
    }
    .team-name { 
        font-size: 1.8em;
        font-weight: 900;
        color: #FFD600;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .score { 
        font-size: 4em;
        font-weight: 900;
        color: #00FF88;
        text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    }
    .commentary { 
        background-color: rgba(0, 229, 255, 0.1);
        border-left: 4px solid #00E5FF;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        font-size: 1.1em;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
"""
if st.session_state.device_mode == "🖥️ PC (데스크탑)":
    st.markdown(f"<style>{css_base} p, span, label, button, input, td, th {{ font-size: 20px !important; }} h1 {{ font-size: 3rem !important; color: #00E5FF !important; text-align:center; }} h2 {{ font-size: 2.2rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }} .stButton>button {{ height: 65px !important; font-size: 22px !important; font-weight: 900 !important; border-radius: 12px; border: 2px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; }} .stButton>button:hover {{ background-color: #00E5FF !important; color: #000 !important; }} [data-testid='stSidebar'] {{ background-color: #001F3F !important; border-right: 4px solid #00E5FF; }}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>{css_base} p, span, label, button, input, td, th {{ font-size: 15px !important; }} h1 {{ font-size: 1.8rem !important; color: #00E5FF !important; text-align:center; }} h2 {{ font-size: 1.4rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }} .stButton>button {{ height: 50px !important; font-size: 15px !important; font-weight: 900 !important; border-radius: 8px; border: 2px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; }} .stButton>button:hover {{ background-color: #00E5FF !important; color: #000 !important; }}</style>", unsafe_allow_html=True)

# ==============================
# 🌐 서버 통합 동기화 로직
# ==============================
market = get_market(); cur_t = time.time(); m_up = False

if cur_t - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]
        ch = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + ch)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 30: curr['history'].pop(0)
    market['last_tick'] = cur_t; m_up = True

if cur_t - market.get('news_time', 0) > 30:
    tid, imp = market['next_news_target'], market['next_news_impact']
    t_nm = [s['name'] for s in stock_config if s['id'] == tid][0]
    market['stock_data'][tid]['price'] = int(market['stock_data'][tid]['price'] * (1 + imp))
    market['news'] = f"📰 [속보] {t_nm}, {'급격한 성장세 기록!' if imp > 0 else '예기치 못한 리스크 발생!'}"
    market['news_time'] = cur_t; market['next_news_target'] = random.choice(stock_config)['id']; market['next_news_impact'] = random.uniform(-0.25, 0.25); m_up = True

if cur_t - market.get('lotto_last_draw', 0) > 3600:
    if market['lotto_tickets']:
        pool = []
        for u, c in market['lotto_tickets'].items(): pool.extend([u] * c)
        win = random.choice(pool); prize = market['lotto_pool']
        us = load_db(USERS_FILE, {})
        if win in us:
            us[win]['cash'] += prize; save_db(USERS_FILE, us)
            if win == st.session_state.logged_in_user: st.session_state.global_cash += prize
        market['news'] = f"🎊 [로또 당첨] {win}님이 1시간의 기다림 끝에 ₩{prize:,} 상금을 거머쥐었습니다!!"
    market['lotto_pool'] = 5000000000; market['lotto_tickets'] = {}; market['lotto_last_draw'] = cur_t; m_up = True

if m_up: save_market(market)

if st.session_state.loan > 0:
    cyc = int((cur_t - st.session_state.loan_time) / 10)
    if cyc > 0: st.session_state.loan = int(st.session_state.loan * (1.02 ** cyc)); st.session_state.loan_time += cyc * 10; sync_user_data()

nw = get_net_worth(st.session_state.logged_in_user, market)
if st.session_state.loan > 0 and nw < 0: st.session_state.equipped_title = "💸 신용불량자"; sync_user_data()

# ==============================
# 🧭 메뉴 분기
# ==============================
menu_ops = ["🏠 홈 광장", "📈 주식 트레이딩", "🏢 부동산 (수금)", "🏦 은행 (대출/송금)", "⚔️ 1시간 글로벌 로또", "⚽ 구단주", "💻 CBT", "🏎️ 레이싱", "🎰 슬롯", "👑 칭호 상점", "💬 랭커 게시판"]
if nw >= 100000000000 or st.session_state.logged_in_user == "5891": menu_ops.insert(2, "💎 VIP 라운지")
if st.session_state.logged_in_user == "5891": menu_ops.append("🛠️ 창조주 통제소")

if "🖥️" in st.session_state.device_mode:
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.logged_in_user}님\n**{st.session_state.equipped_title}**")
        st.metric("현금", f"₩{st.session_state.global_cash:,}"); st.metric("대출", f"₩{st.session_state.loan:,}")
        if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        menu = st.radio("이동", menu_ops)
else:
    st.markdown(f"<div style='text-align:right;'><b>{st.session_state.logged_in_user}</b> | 💰 {st.session_state.global_cash:,}</div>", unsafe_allow_html=True)
    menu = st.selectbox("메뉴 선택", menu_ops)
    if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()

# ==============================
# 💎 [VIP 라운지]
# ==============================
if menu == "💎 VIP 라운지":
    st.title("💎 VIP 시크릿 라운지")
    st.warning("내부자 정보 유출 시 창조주의 징벌이 따릅니다.")
    nxt_id = market['next_news_target']
    nxt_nm = [s['name'] for s in stock_config if s['id'] == nxt_id][0]
    status = "🔥 엄청난 호재" if market['next_news_impact'] > 0 else "❄️ 치명적인 악재"
    st.info(f"🕵️ **[내부자 첩보]** 다음 뉴스 종목: **'{nxt_nm}'** | 예상 흐름: **{status}**")
    st.caption("※ 정확한 변동 수치는 정보 보호를 위해 공개되지 않습니다.")
    
    st.write("---")
    if st.button("🎰 VIP 전용 1억 슬롯 (승률 50%)"):
        if st.session_state.global_cash >= 100000000:
            st.session_state.global_cash -= 100000000
            if random.random() < 0.5: st.session_state.global_cash += 200000000; st.success("당첨! +2억")
            else: st.error("꽝! 다음 기회에...")
            sync_user_data()
            time.sleep(2); st.rerun()
        else: st.error("잔액 부족")

# ==============================
# 🏠 [홈]
# ==============================
elif menu == "🏠 홈 광장":
    st.title(f"반갑습니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("부동산을 사서 월세를 받고, 1시간마다 열리는 글로벌 로또에 도전하세요!")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")
    if market.get('admin_msg'): st.error(f"👑 [창조주 공지] {market['admin_msg']}")

# ==============================
# 📈 [주식]
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소")
    st.warning(market['news'])
    t_m, t_a = st.tabs(["📊 시황", "💼 내 포트폴리오"])
    with t_m:
        rows = ""
        for s in stock_config:
            curr = market['stock_data'][s['id']]
            diff = curr['price'] - curr['history'][-2] if len(curr['history']) > 1 else 0
            pct = (diff / curr['history'][-2] * 100) if len(curr['history']) > 1 else 0
            cls, sign = ("p-up", "▲") if diff >= 0 else ("p-down", "▼")
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{cls}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목</th><th>현재가</th><th>변동</th></tr>{rows}</table>", unsafe_allow_html=True)
    with t_a:
        p_l, t_e = [], 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp, ap = market['stock_data'][sid]['price'], info.get('avg_price', 0)
                eval_a = qty * cp; t_e += eval_a; roi = ((cp-ap)/ap*100) if ap>0 else 0
                p_l.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주", "평가액": f"₩{int(eval_a):,}", "수익률": f"{roi:+.2f}%"})
        if p_l: st.table(pd.DataFrame(p_l))
        st.write(f"💰 주식자산: ₩{t_e:,} | 💵 현금: ₩{st.session_state.global_cash:,}")
    
    st.write("---")
    sel_n = st.selectbox("거래 종목", [s['name'] for s in stock_config])
    sid = [s['id'] for s in stock_config if s['name'] == sel_n][0]
    st.plotly_chart(px.line(y=market['stock_data'][sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    cp = market['stock_data'][sid]['price']
    st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{cp:,}</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💥 풀매수"):
            max_q = st.session_state.global_cash // cp
            if max_q > 0:
                buy_a = max_q * cp; st.session_state.global_cash -= buy_a
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + max_q; new_a = ((old['qty']*old['avg_price']) + buy_a) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                if buy_a >= 1000000000:
                    imp = min((buy_a / 1000000000000) * 0.1, 0.5); market['stock_data'][sid]['price'] = int(cp*(1+imp)); market['news'] = f"🚨 [고래 매수] {st.session_state.logged_in_user}님이 {sel_n} 거액 매수!"; save_market(market)
                sync_user_data(); st.rerun()
    with c2:
        if st.button("💸 풀매도"):
            own = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if own > 0:
                sell_a = own * cp; st.session_state.global_cash += sell_a; st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                if sell_a >= 1000000000:
                    imp = min((sell_a / 500000000000) * 0.1, 0.5); market['stock_data'][sid]['price'] = max(1000, int(cp*(1-imp))); market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {sel_n} 물량 투하!"; save_market(market)
                sync_user_data(); st.rerun()
    time.sleep(2); st.rerun()

# ==============================
# 🏢 [부동산]
# ==============================
elif menu == "🏢 부동산 (수금)":
    st.title("🏢 부동산 경매소")
    uc = 0; now = time.time(); pass_s = int(now - st.session_state.rent_time)
    for eid, count in st.session_state.real_estate.items():
        if eid in estate_config: uc += estate_config[eid]['income'] * count * pass_s
    st.markdown(f"<div style='background-color:#001F3F; padding:20px; text-align:center;'><h2>누적 월세: ₩{uc:,}</h2></div>", unsafe_allow_html=True)
    if st.button("💰 수금하기"):
        st.session_state.global_cash += uc; st.session_state.rent_time = now; sync_user_data(); st.rerun()
    for eid, info in estate_config.items():
        c1, c2 = st.columns([3, 1])
        owned = st.session_state.real_estate.get(eid, 0)
        c1.write(f"**{info['name']}** (₩{info['price']:,}) | 수량: {owned}채 (초당 +₩{info['income']*owned:,})")
        if c2.button("매입", key=eid):
            if st.session_state.global_cash >= info['price']:
                st.session_state.global_cash -= info['price']; st.session_state.real_estate[eid] = owned + 1; sync_user_data(); st.rerun()
            else: st.error("현금 부족")

# ==============================
# 🏦 [은행]
# ==============================
elif menu == "🏦 은행 (대출/송금)":
    st.title("🏦 하이리스크 은행")
    t1, t2 = st.tabs(["💸 송금", "💳 대출"])
    with t1:
        target = st.text_input("아이디"); amt = st.number_input("금액", min_value=0, step=1000000)
        if st.button("보내기"):
            us = load_db(USERS_FILE, {})
            if target in us and st.session_state.global_cash >= amt:
                st.session_state.global_cash -= amt; us[target]['cash'] += amt; save_db(USERS_FILE, us); sync_user_data(); st.success("완료")
    with t2:
        st.metric("내 빚", f"₩{st.session_state.loan:,}")
        l_amt = st.number_input("대출액", min_value=0, step=100000000)
        if st.button("대출"): st.session_state.global_cash += l_amt; st.session_state.loan += l_amt; st.session_state.loan_time = time.time(); sync_user_data(); st.rerun()
        r_amt = st.number_input("상환액", min_value=0, step=100000000)
        if st.button("상환"):
            actual = min(r_amt, st.session_state.loan)
            if st.session_state.global_cash >= actual:
                st.session_state.global_cash -= actual; st.session_state.loan -= actual
                if st.session_state.loan == 0 and st.session_state.equipped_title == "💸 신용불량자": st.session_state.equipped_title = "신규시민"
                sync_user_data(); st.rerun()

# ==============================
# ⚔️ [로또]
# ==============================
elif menu == "⚔️ 1시간 글로벌 로또":
    st.title("⚔️ 1시간 글로벌 로또")
    st.markdown(f"<h1 style='color:#FFD600;'>현재 누적 상금: ₩{market['lotto_pool']:,}</h1>", unsafe_allow_html=True)
    my_t = market['lotto_tickets'].get(st.session_state.logged_in_user, 0)
    st.write(f"내 티켓: {my_t}장"); b_cnt = st.number_input("구매 수량 (장당 1,000만)", min_value=1, step=1)
    if st.button("티켓 구매"):
        cost = b_cnt * 10000000
        if st.session_state.global_cash >= cost:
            st.session_state.global_cash -= cost; market['lotto_pool'] += cost; market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt; save_market(market); sync_user_data(); st.rerun()
    rem = int(3600 - (time.time() - market['lotto_last_draw']))
    st.info(f"⏳ 다음 추첨까지 약 {rem//60}분 {rem%60}초 남았습니다."); time.sleep(5); st.rerun()

# ==============================
# ⚽ [구단주] - 대폭 개선
# ==============================
elif menu == "⚽ 구단주":
    st.title("🏆 구단주 시뮬레이터")
    
    # 포메이션 및 팀 설정
    col1, col2 = st.columns(2)
    with col1:
        my_team = st.text_input("내 팀 이름", value="FC 효민")
        my_formation = st.selectbox("내 팀 포메이션", ["4-4-2 (균형)", "4-3-3 (공격)", "3-5-2 (중원)", "5-3-2 (수비)", "4-2-3-1 (현대)"])
    with col2:
        opp_team = st.text_input("상대 팀 이름", value="FC 라이벌")
        opp_formation = st.selectbox("상대 팀 포메이션", ["4-4-2 (균형)", "4-3-3 (공격)", "3-5-2 (중원)", "5-3-2 (수비)", "4-2-3-1 (현대)"])
    
    if st.button("⚽ 경기 시작", use_container_width=True):
        # 포메이션별 공격력/수비력 설정
        formation_stats = {
            "4-4-2 (균형)": {"attack": 0.30, "defense": 0.25},
            "4-3-3 (공격)": {"attack": 0.40, "defense": 0.15},
            "3-5-2 (중원)": {"attack": 0.28, "defense": 0.22},
            "5-3-2 (수비)": {"attack": 0.20, "defense": 0.35},
            "4-2-3-1 (현대)": {"attack": 0.32, "defense": 0.23}
        }
        
        my_stats = formation_stats[my_formation]
        opp_stats = formation_stats[opp_formation]
        
        # 실시간 해설 및 스코어
        h_score, a_score = 0, 0
        scoreboard = st.empty()
        commentary_box = st.empty()
        progress = st.progress(0)
        
        commentaries = []
        
        for minute in range(1, 11):  # 10분 경기
            time.sleep(0.6)
            
            # 내 팀 공격
            if random.random() < my_stats["attack"]:
                if random.random() > opp_stats["defense"]:
                    h_score += 1
                    events = [
                        f"⚽ {minute*9}분: 골!!! {my_team}의 환상적인 골이 터졌습니다!",
                        f"⚽ {minute*9}분: {my_team}, 완벽한 마무리! 골망을 흔듭니다!",
                        f"⚽ {minute*9}분: 믿을 수 없는 슈팅! {my_team}이 득점에 성공합니다!"
                    ]
                    commentaries.insert(0, random.choice(events))
                else:
                    events = [
                        f"🛡️ {minute*9}분: {opp_team} 수비수가 절묘하게 막아냅니다!",
                        f"🧤 {minute*9}분: 골키퍼의 슈퍼세이브! {opp_team}의 위기 대응!"
                    ]
                    commentaries.insert(0, random.choice(events))
            
            # 상대 팀 공격
            if random.random() < opp_stats["attack"]:
                if random.random() > my_stats["defense"]:
                    a_score += 1
                    events = [
                        f"⚽ {minute*9}분: {opp_team}이 골을 넣었습니다! 위협적인 공격이었습니다!",
                        f"⚽ {minute*9}분: {opp_team}의 역습! 골이 들어갑니다!",
                        f"⚽ {minute*9}분: {opp_team}, 정확한 슈팅으로 골 성공!"
                    ]
                    commentaries.insert(0, random.choice(events))
                else:
                    events = [
                        f"🛡️ {minute*9}분: {my_team} 수비진이 든든하게 막아냅니다!",
                        f"🧤 {minute*9}분: 우리 골키퍼의 환상적인 선방!"
                    ]
                    commentaries.insert(0, random.choice(events))
            
            # 일반 경기 상황
            if random.random() < 0.3:
                general_events = [
                    f"📊 {minute*9}분: 치열한 중원 싸움이 계속됩니다!",
                    f"🏃 {minute*9}분: 빠른 패스 플레이가 펼쳐집니다!",
                    f"⚡ {minute*9}분: 긴장감 넘치는 공방전!",
                    f"🎯 {minute*9}분: 정확한 패스로 기회를 만들어냅니다!"
                ]
                commentaries.insert(0, random.choice(general_events))
            
            # 스코어보드 업데이트
            scoreboard.markdown(f"""
                <div class='scoreboard'>
                    <div style='display: flex; justify-content: space-around; align-items: center;'>
                        <div style='text-align: center;'>
                            <div class='team-name'>{my_team}</div>
                            <div style='font-size: 0.9em; color: #888;'>{my_formation}</div>
                        </div>
                        <div class='score'>{h_score} : {a_score}</div>
                        <div style='text-align: center;'>
                            <div class='team-name'>{opp_team}</div>
                            <div style='font-size: 0.9em; color: #888;'>{opp_formation}</div>
                        </div>
                    </div>
                    <div style='text-align: center; margin-top: 15px; font-size: 1.2em; color: #00E5FF;'>
                        ⏱️ {minute*9}/90분
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 해설 업데이트
            commentary_html = ""
            for comm in commentaries[:5]:  # 최근 5개만 표시
                commentary_html += f"<div class='commentary'>{comm}</div>"
            commentary_box.markdown(commentary_html, unsafe_allow_html=True)
            
            progress.progress(minute / 10)
        
        # 경기 종료
        st.write("---")
        if h_score > a_score:
            result_msg = f"🎉 승리! {my_team}이 {h_score}:{a_score}로 승리했습니다!"
            reward = 5000000
            st.balloons()
        elif h_score == a_score:
            result_msg = f"🤝 무승부! {h_score}:{a_score} 팽팽한 경기였습니다!"
            reward = 1000000
        else:
            result_msg = f"😢 패배... {opp_team}에게 {h_score}:{a_score}로 패배했습니다."
            reward = 100000
        
        st.success(result_msg)
        st.session_state.global_cash += reward
        sync_user_data()
        st.info(f"💰 경기 보상: +₩{reward:,}")
        time.sleep(3)
        st.rerun()

# ==============================
# 💻 [CBT] - 정처기 실전 난이도
# ==============================
elif menu == "💻 CBT":
    st.title("💻 정보처리기사 실전 모의고사")
    st.warning("⚠️ 실제 정처기 수준의 고난도 문제입니다. 신중하게 풀이하세요!")
    
    if 'cbt_q' not in st.session_state:
        # 정처기 실전 문제 풀 (대폭 확장 및 난이도 상승)
        question_pool = [
            {
                "q": "데이터베이스의 정규화 과정 중 제2정규형(2NF)의 조건으로 옳은 것은?",
                "a": "부분 함수 종속을 제거한 형태",
                "w": ["이행 함수 종속을 제거한 형태", "다치 종속을 제거한 형태", "조인 종속을 제거한 형태"]
            },
            {
                "q": "OSI 7계층 중 세그먼트(Segment)를 데이터 단위로 사용하는 계층은?",
                "a": "전송 계층(Transport Layer)",
                "w": ["네트워크 계층", "세션 계층", "데이터링크 계층"]
            },
            {
                "q": "소프트웨어 개발 방법론 중 '스프린트(Sprint)'를 사용하는 애자일 방법론은?",
                "a": "스크럼(Scrum)",
                "w": ["폭포수 모델", "나선형 모델", "V 모델"]
            },
            {
                "q": "트랜잭션의 ACID 특성 중 '원자성(Atomicity)'의 의미는?",
                "a": "All or Nothing - 모두 실행되거나 모두 실행되지 않아야 함",
                "w": ["동시에 실행되는 트랜잭션이 서로 영향을 주지 않음", "트랜잭션 완료 후 결과가 영구적으로 반영됨", "트랜잭션 실행 전후 데이터 무결성 유지"]
            },
            {
                "q": "디자인 패턴 중 객체 생성을 캡슐화하는 패턴은?",
                "a": "팩토리 패턴(Factory Pattern)",
                "w": ["옵저버 패턴", "전략 패턴", "어댑터 패턴"]
            },
            {
                "q": "IP 주소 192.168.1.0/24에서 서브넷 마스크는?",
                "a": "255.255.255.0",
                "w": ["255.255.0.0", "255.0.0.0", "255.255.255.255"]
            },
            {
                "q": "SQL에서 LEFT OUTER JOIN의 결과로 올바른 설명은?",
                "a": "왼쪽 테이블의 모든 행을 포함하고, 오른쪽 테이블에 매칭되는 데이터가 없으면 NULL",
                "w": ["양쪽 테이블 모두 매칭되는 행만 출력", "오른쪽 테이블의 모든 행 포함", "매칭되지 않는 행은 모두 제외"]
            },
            {
                "q": "Quick Sort의 평균 시간 복잡도는?",
                "a": "O(n log n)",
                "w": ["O(n²)", "O(n)", "O(log n)"]
            },
            {
                "q": "Python에서 리스트 [1,2,3,4,5]를 역순으로 만드는 메서드는?",
                "a": "reverse()",
                "w": ["sort()", "pop()", "append()"]
            },
            {
                "q": "TCP와 UDP의 가장 큰 차이점은?",
                "a": "TCP는 연결 지향, UDP는 비연결 지향",
                "w": ["TCP는 비연결 지향, UDP는 연결 지향", "TCP는 느리고 UDP는 빠름만 차이", "TCP는 응용 계층, UDP는 전송 계층"]
            },
            {
                "q": "블록체인에서 작업 증명(Proof of Work)의 목적은?",
                "a": "분산 합의 달성 및 이중 지불 방지",
                "w": ["데이터 암호화", "네트워크 속도 향상", "저장 공간 절약"]
            },
            {
                "q": "REST API에서 리소스 삭제 시 사용하는 HTTP 메서드는?",
                "a": "DELETE",
                "w": ["GET", "POST", "PUT"]
            },
            {
                "q": "NoSQL 데이터베이스의 특징으로 올바른 것은?",
                "a": "스키마가 유연하고 수평적 확장(Scale-out)에 유리",
                "w": ["반드시 ACID를 보장해야 함", "관계형 모델만 사용", "수직적 확장만 가능"]
            },
            {
                "q": "메모리 관리 기법 중 '페이징(Paging)'의 주요 장점은?",
                "a": "외부 단편화 해결",
                "w": ["내부 단편화 해결", "메모리 접근 속도 향상", "메모리 용량 증가"]
            },
            {
                "q": "Git에서 원격 저장소의 변경사항을 로컬로 가져오는 명령어는?",
                "a": "git pull",
                "w": ["git push", "git commit", "git clone"]
            }
        ]
        
        selected_q = random.choice(question_pool)
        st.session_state.cbt_q = selected_q
        st.session_state.cbt_opts = selected_q['w'] + [selected_q['a']]
        random.shuffle(st.session_state.cbt_opts)
    
    # 문제 출제
    with st.form("exam_form"):
        st.markdown(f"<div style='background-color:#1A1C24; padding:25px; border-radius:10px; border:2px solid #00E5FF;'><h2 style='color:#FFD600;'>📝 문제</h2><p style='font-size:1.3em; line-height:1.6;'>{st.session_state.cbt_q['q']}</p></div>", unsafe_allow_html=True)
        
        st.write("")
        answer = st.radio("정답을 선택하세요:", st.session_state.cbt_opts, key="answer_radio")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("✅ 제출하기", use_container_width=True)
        
        if submit:
            if answer == st.session_state.cbt_q['a']:
                st.success("🎉 정답입니다! 훌륭한 실력이십니다!")
                reward = 500000
                st.session_state.global_cash += reward
                st.balloons()
                st.info(f"💰 보상: +₩{reward:,}")
            else:
                st.error(f"❌ 오답입니다. 정답은: {st.session_state.cbt_q['a']}")
                st.info("💡 다시 도전하여 실력을 키워보세요!")
            
            del st.session_state.cbt_q
            del st.session_state.cbt_opts
            sync_user_data()
            time.sleep(2.5)
            st.rerun()

# ==============================
# 🏎️ [레이싱] - 다양한 차량 추가
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 하이퍼카 레이싱")
    st.info("💡 배당률이 높을수록 우승 확률은 낮지만, 당첨 시 높은 수익!")
    
    # 다양한 차량 라인업
    cars = [
        {"name": "🏎️ 부가티 시론", "odds": 20.0, "speed_range": (3, 8)},
        {"name": "🚗 람보르기니", "odds": 12.0, "speed_range": (4, 10)},
        {"name": "🏁 페라리 SF90", "odds": 8.0, "speed_range": (5, 12)},
        {"name": "⚡ 맥라렌 P1", "odds": 6.0, "speed_range": (6, 13)},
        {"name": "🔥 포르쉐 911", "odds": 4.0, "speed_range": (7, 15)},
        {"name": "💨 테슬라 플레이드", "odds": 2.0, "speed_range": (10, 18)},
    ]
    
    # 차량 선택
    car_names = [f"{car['name']} ({car['odds']}배)" for car in cars]
    selected = st.selectbox("차량 선택", car_names)
    selected_car = cars[car_names.index(selected)]
    
    # 배팅
    bet_amount = st.number_input("배팅 금액", min_value=10000, step=10000, value=100000)
    
    if st.button("🏁 레이스 시작!", use_container_width=True):
        if st.session_state.global_cash >= bet_amount:
            st.session_state.global_cash -= bet_amount
            
            st.markdown("### 🏁 경주 진행 중...")
            
            # 진행바 생성 (각 차량별로 이름 라벨 포함)
            progress_bars = {}
            for car in cars:
                progress_bars[car['name']] = st.progress(0, text=f"{car['name']} - 0%")
            
            positions = {car['name']: 0 for car in cars}
            
            # 레이스 시작
            winner = None
            while winner is None:
                time.sleep(0.1)
                
                for car in cars:
                    move = random.randint(car['speed_range'][0], car['speed_range'][1])
                    positions[car['name']] = min(100, positions[car['name']] + move)
                    
                    # 진행바 업데이트 (이름 + 퍼센트 표시)
                    progress_bars[car['name']].progress(
                        positions[car['name']] / 100,
                        text=f"{car['name']} - {positions[car['name']]}%"
                    )
                    
                    if positions[car['name']] >= 100 and winner is None:
                        winner = car['name']
            
            st.write("---")
            st.markdown(f"<h2 style='text-align:center; color:#FFD600;'>🏆 우승: {winner}</h2>", unsafe_allow_html=True)
            
            # 결과 처리
            if winner == selected_car['name']:
                winnings = int(bet_amount * selected_car['odds'])
                st.session_state.global_cash += winnings
                st.success(f"🎉 축하합니다! {selected_car['name']} 우승!")
                st.balloons()
                st.info(f"💰 획득 상금: +₩{winnings:,}")
            else:
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")
                st.info("다음 레이스에서 재도전하세요!")
            
            sync_user_data()
            time.sleep(3)
            st.rerun()
        else:
            st.error("💸 잔액이 부족합니다!")

# ==============================
# 🎰 [슬롯]
# ==============================
elif menu == "🎰 슬롯":
    st.title("🎰 럭키 슬롯")
    if st.button("1,000만 당기기"):
        if st.session_state.global_cash >= 10000000:
            st.session_state.global_cash -= 10000000
            slot_box = st.empty()
            for _ in range(10):
                r = [random.choice(["💎","🍒","7️⃣"]) for _ in range(3)]
                slot_box.markdown(f"<h1 style='text-align:center; font-size:60px;'>{' '.join(r)}</h1>", unsafe_allow_html=True)
                time.sleep(0.1)
            
            if r[0]==r[1]==r[2]: st.session_state.global_cash += 500000000; st.success("🎉 잭팟! +5억"); st.balloons()
            else: st.error("꽝! 다음 기회에...")
            sync_user_data(); time.sleep(2); st.rerun()
        else: st.error("잔액 부족!")

# ==============================
# 👑 [칭호 상점]
# ==============================
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    if st.session_state.equipped_title == "💸 신용불량자": st.error("빚부터 갚으세요!")
    else:
        for i in range(1, 11):
            t_n = f"💎 VIP Lv.{i}"; t_p = i * 100000000
            c1, c2 = st.columns([3, 1])
            c1.write(f"**{t_n}** (₩{t_p:,})")
            if c2.button("구매/장착", key=t_n):
                if st.session_state.global_cash >= t_p: st.session_state.global_cash -= t_p; st.session_state.equipped_title = t_n; sync_user_data(); st.rerun()

# ==============================
# 💬 [게시판]
# ==============================
elif menu == "💬 랭커 게시판":
    st.title("💬 랭커 게시판")
    msg = st.text_input("메시지"); 
    if st.button("등록") and msg:
        new_c = {"name": st.session_state.logged_in_user, "title": st.session_state.equipped_title, "comment": msg}
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [new_c]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        st.markdown(f"**[{c.get('title','신규시민')}] {c['name']}**: {c['comment']}")

# ==============================
# 🛠️ [창조주 패널]
# ==============================
elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 창조주 패널")
    t1, t2 = st.tabs(["유저 조작", "시장 조작"])
    with t1:
        u_db = load_db(USERS_FILE, {}); sel_u = st.selectbox("유저", list(u_db.keys()))
        new_c = st.number_input("현금 변경", value=u_db[sel_u]['cash'])
        new_t = st.text_input("칭호 변경", value=u_db[sel_u]['equipped_title'])
        if st.button("조작 실행"): u_db[sel_u]['cash'] = new_c; u_db[sel_u]['equipped_title'] = new_t; save_db(USERS_FILE, u_db); st.success("완료")
    with t2:
        msg = st.text_input("공지사항"); 
        if st.button("공지발령"): market['admin_msg'] = msg; save_market(market)
        if st.button("🔥 전종목 폭등"):
            for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price']*1.5)
            save_market(market)
