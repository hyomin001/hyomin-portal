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

# 👑 [고퀄리티 칭호 생성기]
def get_title_name(lv):
    if lv == 0: return "🌱 이름없는 시민"
    if lv <= 10: return f"💰 자산가 Lv.{lv}"
    if lv <= 30: return f"🏢 건물주 Lv.{lv}"
    if lv <= 50: return f"💎 다이아몬드 수저 Lv.{lv}"
    if lv <= 70: return f"🚀 경제의 지배자 Lv.{lv}"
    if lv <= 85: return f"🌌 은하계 자본가 Lv.{lv}"
    if lv <= 99: return f"💫 신화적 초월자 Lv.{lv}"
    return "👑 절대신 창조주"

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
            "version": 6, "stock_data": {s['id']: {"name": s['name'], "price": random.randint(50000, 150000), "history": [80000]} for s in stock_config},
            "news": "시장이 개장되었습니다.", "news_time": time.time(), "last_tick": time.time(), "admin_msg": "",
            "lotto_pool": 5000000000, "lotto_tickets": {}, "lotto_last_draw": time.time(),
            "next_news_target": random.choice(stock_config)['id'], "next_news_impact": random.uniform(-0.2, 0.2)
        }
        return data
    if not os.path.exists(MARKET_FILE):
        d = init_m(); save_db(MARKET_FILE, d); return d
    d = load_db(MARKET_FILE, {})
    if d.get("version") != 6:
        d = init_m(); save_db(MARKET_FILE, d); return d
    return d

def save_market(data): save_db(MARKET_FILE, data)

st.set_page_config(page_title="HYOMIN UNIVERSE v14.6", page_icon="💎", layout="wide")

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align:center; color:#00E5FF;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("환경 설정", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tab_log = st.tabs(["🔑 로그인", "📝 시민등록"])
        with tab_log[0]:
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                # 👑 창조주 계정 (5891)
                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {"pw": "5891", "cash": 999999999999, "inventory": ["title_100"], "equipped_title": "👑 절대신 창조주", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                        save_db(USERS_FILE, users)
                    st.session_state.update({'logged_in_user': "5891", 'global_cash': users["5891"]['cash'], 'inventory': users["5891"]['inventory'], 'equipped_title': "👑 절대신 창조주", 'portfolio': {}, 'real_estate': {}, 'rent_time': time.time(), 'loan': 0, 'loan_time': time.time(), 'device_mode': device_mode}); st.rerun()
                elif l_id in users and users[l_id]['pw'] == l_pw:
                    u = users[l_id]
                    st.session_state.update({'logged_in_user': l_id, 'global_cash': u['cash'], 'inventory': u['inventory'], 'equipped_title': u.get('equipped_title','🌱 이름없는 시민'), 'portfolio': u.get('portfolio',{}), 'real_estate': u.get('real_estate',{}), 'rent_time': u.get('rent_time', time.time()), 'loan': u.get('loan', 0), 'loan_time': u.get('loan_time', time.time()), 'device_mode': device_mode}); st.rerun()
                else: st.error("정보 불일치")
        with tab_log[1]:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록"):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "5891": st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "🌱 이름없는 시민", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                    save_db(USERS_FILE, users); st.success("가입 성공!")
    st.stop()

# ==============================
# 🎨 CSS (고퀄리티 통합)
# ==============================
css_base = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    .stApp { background-color: #050505 !important; }
    html, body, p, span, label, h1, h2, h3, button, input, th, td { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; }
    div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
    div[role="listbox"] { background-color: #FFFFFF !important; border: 2px solid #00E5FF !important; border-radius: 8px; }
    div[role="listbox"] li, div[role="listbox"] span { color: #000000 !important; font-weight: 900 !important; }
    div[role="listbox"] li:hover, div[role="listbox"] li:hover span { background-color: #00E5FF !important; color: #000000 !important; }
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 2px solid #444; }
    .stock-table th { background-color: #333; color: #FFD600 !important; text-align: center; }
    .stock-table td { border-bottom: 1px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }
    .stButton>button { height: 65px !important; font-weight: 900 !important; border-radius: 12px; border: 2px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; }
    .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
"""
if st.session_state.device_mode == "🖥️ PC (데스크탑)":
    st.markdown(f"<style>{css_base} p, span, label, button, input, td, th {{ font-size: 20px !important; }} h1 {{ font-size: 3rem !important; color: #00E5FF !important; text-align:center; }} h2 {{ font-size: 2.2rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }} [data-testid='stSidebar'] {{ background-color: #001F3F !important; border-right: 4px solid #00E5FF; }}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>{css_base} p, span, label, button, input, td, th {{ font-size: 15px !important; }} h1 {{ font-size: 1.8rem !important; color: #00E5FF !important; text-align:center; }} h2 {{ font-size: 1.4rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }}</style>", unsafe_allow_html=True)

# ==============================
# 🌐 동기화 로직
# ==============================
market = get_market(); cur_t = time.time(); m_up = False

if cur_t - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]; ch = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + ch))); curr['history'].append(curr['price'])
        if len(curr['history']) > 30: curr['history'].pop(0)
    market['last_tick'] = cur_t; m_up = True

if cur_t - market.get('news_time', 0) > 30:
    tid, imp = market['next_news_target'], market['next_news_impact']; t_nm = [s['name'] for s in stock_config if s['id'] == tid][0]
    market['stock_data'][tid]['price'] = int(market['stock_data'][tid]['price'] * (1 + imp))
    market['news'] = f"📰 [속보] {t_nm}, {'급격한 성장세 기록!' if imp > 0 else '예기치 못한 리스크 발생!'}"
    market['news_time'] = cur_t; market['next_news_target'] = random.choice(stock_config)['id']; market['next_news_impact'] = random.uniform(-0.25, 0.25); m_up = True

if cur_t - market.get('lotto_last_draw', 0) > 3600:
    if market['lotto_tickets']:
        pool = []; [pool.extend([u] * c) for u, c in market['lotto_tickets'].items()]
        win = random.choice(pool); prize = market['lotto_pool']; us = load_db(USERS_FILE, {})
        if win in us:
            us[win]['cash'] += prize; save_db(USERS_FILE, us)
            if win == st.session_state.logged_in_user: st.session_state.global_cash += prize
        market['news'] = f"🎊 [로또 당첨] {win}님이 ₩{prize:,} 상금을 독식했습니다!"
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
menu_ops = ["🏠 홈 광장", "📈 주식 트레이딩", "🏢 부동산 (수금)", "🏦 은행 (대출/송금)", "⚔️ 1시간 글로벌 로또", "⚽ 구단주 매니저", "💻 CBT 모의고사", "🏎️ 역배 레이싱", "🎰 슬롯", "👑 칭호 상점", "💬 랭커 게시판"]
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
# 💎 VIP 라운지
# ==============================
if menu == "💎 VIP 라운지":
    st.title("💎 VIP 시크릿 라운지")
    status = "🔥 엄청난 호재" if market['next_news_impact'] > 0 else "❄️ 치명적인 악재"
    st.info(f"🕵️ 다음 뉴스 종목: **'{[s['name'] for s in stock_config if s['id'] == market['next_news_target']][0]}'** | 예상 흐름: **{status}**")
    if st.button("🎰 VIP 전용 1억 슬롯 (승률 50%)"):
        if st.session_state.global_cash >= 100000000:
            st.session_state.global_cash -= 100000000
            if random.random() < 0.5: st.session_state.global_cash += 200000000; st.success("당첨!")
            else: st.error("꽝!")
            sync_user_data(); time.sleep(1.5); st.rerun()
        else: st.error("잔액 부족")

# ==============================
# 🏠 홈
# ==============================
elif menu == "🏠 홈 광장":
    st.title(f"반갑습니다 {st.session_state.logged_in_user}님! 🎉")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")
    if market.get('admin_msg'): st.error(f"👑 [창조주 공지] {market['admin_msg']}")

# ==============================
# 📈 주식
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소")
    st.warning(market['news'])
    t_m, t_a = st.tabs(["📊 시황", "💼 포트폴리오"])
    with t_m:
        rows = ""
        for s in stock_config:
            curr = market['stock_data'][s['id']]; diff = curr['price'] - curr['history'][-2] if len(curr['history']) > 1 else 0
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
    
    sel_n = st.selectbox("거래 종목", [s['name'] for s in stock_config])
    sid = [s['id'] for s in stock_config if s['name'] == sel_n][0]; cp = market['stock_data'][sid]['price']
    st.plotly_chart(px.line(y=market['stock_data'][sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{cp:,}</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💥 풀매수"):
            max_q = st.session_state.global_cash // cp
            if max_q > 0:
                buy_a = max_q * cp; st.session_state.global_cash -= buy_a; old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
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
# 🏢 부동산
# ==============================
elif menu == "🏢 부동산 (수금)":
    st.title("🏢 부동산 경매소")
    uc = 0; now = time.time(); pass_s = int(now - st.session_state.rent_time)
    for eid, count in st.session_state.real_estate.items():
        if eid in estate_config: uc += estate_config[eid]['income'] * count * pass_s
    st.markdown(f"<div style='background-color:#001F3F; padding:20px; text-align:center; border-radius:15px;'><h2>누적 월세: ₩{uc:,}</h2></div>", unsafe_allow_html=True)
    if st.button("💰 수금하기"): st.session_state.global_cash += uc; st.session_state.rent_time = now; sync_user_data(); st.rerun()
    for eid, info in estate_config.items():
        c1, c2 = st.columns([3, 1]); owned = st.session_state.real_estate.get(eid, 0)
        c1.write(f"**{info['name']}** (₩{info['price']:,}) | 수량: {owned}채 (초당 +₩{info['income']*owned:,})")
        if c2.button("매입", key=eid):
            if st.session_state.global_cash >= info['price']: st.session_state.global_cash -= info['price']; st.session_state.real_estate[eid] = owned + 1; sync_user_data(); st.rerun()
            else: st.error("현금 부족")

# ==============================
# ⚽ [고퀄리티] 구단주 시뮬
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터 Pro")
    form = st.selectbox("전술 포메이션", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (중원)", "5-4-1 (수비)"])
    if st.button("🏟️ 경기 시작 (생중계)"):
        h, a = 0, 0; b = st.empty(); c = st.empty(); p = st.progress(0)
        mentary = ["중원에서 치열한 공방전!", "수비수 몸을 날리는 태클!", "측면 돌파 성공! 크로스!!", "골키퍼 정면 슈팅!", "환상적인 티키타카!", "VAR 판독 중...", "역습 찬스!"]
        for i in range(15):
            if random.random() < 0.2: h += 1
            if random.random() < 0.15: a += 1
            b.markdown(f"<div style='background:#111; border:4px solid #00E5FF; padding:30px; border-radius:20px; text-align:center;'><h1 style='font-size:60px;'>내 팀 {h} : {a} 상대</h1></div>", unsafe_allow_html=True)
            c.info(f"🎙️ [해설] {random.choice(mentary)}")
            p.progress((i+1)/15); time.sleep(0.8)
        res = 10000000 if h > a else 2000000 if h == a else 200000
        st.session_state.global_cash += res; sync_user_data(); st.success(f"최종 결과: {h}:{a} | 수익: +₩{res:,}")
        time.sleep(3); st.rerun()

# ==============================
# 💻 [고퀄리티] CBT 모의고사
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 실전 1급 모의고사")
    if 'cbt_q' not in st.session_state:
        q_pool = [
            {"q": "데이터베이스의 '이행적 함수 종속'을 제거하는 단계는?", "a": "제3정규형(3NF)", "w": ["제1정규형", "제2정규형", "BCNF"]},
            {"q": "객체지향 설계 원칙(SOLID) 중 '상위 클래스는 하위 클래스로 대체 가능해야 함'을 뜻하는 것은?", "a": "LSP (리스코프 치환)", "w": ["SRP", "DIP", "OCP"]},
            {"q": "OSI 7계층 중 물리적 주소(MAC)를 사용하여 데이터를 전송하는 계층은?", "a": "데이터 링크 계층", "w": ["물리 계층", "네트워크 계층", "전송 계층"]},
            {"q": "응집도(Cohesion) 중 가장 응집도가 낮은(안좋은) 것은?", "a": "우연적(Coincidental)", "w": ["논리적", "시간적", "절차적"]},
            {"q": "결합도(Coupling) 중 가장 결합도가 높은(안좋은) 것은?", "a": "내용(Content)", "w": ["공통", "외부", "제어"]}
        ]
        st.session_state.cbt_q = random.choice(q_pool); opts = st.session_state.cbt_q['w'] + [st.session_state.cbt_q['a']]; random.shuffle(opts); st.session_state.cbt_opts = opts
    with st.form("cbt"):
        st.markdown(f"### Q. {st.session_state.cbt_q['q']}")
        ans = st.radio("정답 선택", st.session_state.cbt_opts)
        if st.form_submit_button("답안 제출"):
            if ans == st.session_state.cbt_q['a']: st.session_state.global_cash += 1000000; st.success("🎉 정답! ₩1,000,000 지급")
            else: st.error(f"❌ 오답! 정답은 [{st.session_state.cbt_q['a']}]"); sync_user_data()
            del st.session_state.cbt_q; time.sleep(2); st.rerun()

# ==============================
# 🏎️ [고퀄리티] 역배 레이싱
# ==============================
elif menu == "🏎️ 역배 레이싱":
    st.title("🏎️ 역배 챔피언십 (High Risk)")
    cars = [{"n":"🚲 자전거 (50배)", "o":50.0}, {"n":"🚜 경운기 (20배)", "o":20.0}, {"n":"🚗 레이 (10배)", "o":10.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차종","o":"배당"}))
    sel = st.selectbox("베팅 차량", [c['n'] for c in cars]); amt = st.number_input("베팅액", min_value=100000, step=100000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt; pos = [0]*4; bars = [st.progress(0, text=f"{c['n']}") for c in cars]
            while max(pos) < 100:
                for i in range(4): 
                    speed = 10 if cars[i]['o']<2 else 5 if cars[i]['o']<15 else 3
                    pos[i] += random.randint(1, speed); bars[i].progress(min(pos[i], 100), text=f"{cars[i]['n']} [{min(pos[i],100)}%]")
                time.sleep(0.15)
            win = cars[pos.index(max(pos))]; 
            if win['n'] == sel: win_m = int(amt * win['o']); st.session_state.global_cash += win_m; st.success(f"🎉 승리! +₩{win_m:,}"); st.balloons()
            else: st.error(f"💀 패배! 우승은 {win['n']}"); sync_user_data(); time.sleep(3); st.rerun()

# ==============================
# 👑 [고퀄리티] 칭호 상점
# ==============================
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점 (Lv.1 ~ 100)")
    if st.session_state.equipped_title == "💸 신용불량자": st.error("빚부터 갚으세요!")
    else:
        cols = st.columns(2)
        for i in range(1, 101):
            with cols[i%2]:
                t_n = get_title_name(i); t_p = i * 500000000 # 부동산 비싼만큼 칭호도 비싸게 상향
                st.markdown(f"**{t_n}** | ₩{t_p:,}")
                t_id = f"title_{i}"
                if t_id in st.session_state.inventory:
                    if st.session_state.equipped_title == t_n: st.button("✅ 장착 중", key=t_id, disabled=True)
                    else:
                        if st.button("🌟 장착", key=t_id): st.session_state.equipped_title = t_n; sync_user_data(); st.rerun()
                else:
                    if st.button(f"구매", key=t_id):
                        if st.session_state.global_cash >= t_p: st.session_state.global_cash -= t_p; st.session_state.inventory.append(t_id); st.session_state.equipped_title = t_n; sync_user_data(); st.rerun()
                        else: st.error("현금 부족")

# ==============================
# 💬 [고퀄리티] 랭커 게시판
# ==============================
elif menu == "💬 랭커 게시판":
    st.title("💬 랭커 전용 게시판")
    msg = st.text_input("메시지 입력 (품격있게)"); 
    if st.button("등록") and msg:
        new_c = {"name": st.session_state.logged_in_user, "title": st.session_state.equipped_title, "comment": msg, "time": datetime.now().strftime("%H:%M")}
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [new_c]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        # 칭호 등급에 따른 배경색 설정
        t = c.get('title','🌱 이름없는 시민'); b_color = "#333"
        if "👑" in t: b_color = "#500000"
        elif "💫" in t: b_color = "#330066"
        elif "💎" in t: b_color = "#003366"
        st.markdown(f"""
        <div style='background-color: {b_color}; border-left: 5px solid #00FF88; padding: 15px; margin-bottom: 10px; border-radius: 10px;'>
            <span style='background:#FFD600; color:#000; padding:2px 6px; border-radius:4px; font-size:12px; font-weight:900;'>{t}</span>
            <b style='color:#00E5FF;'> {c['name']}</b> <small style='color:#888;'>{c.get('time','')}</small><br>
            <div style='margin-top:5px; font-size:18px;'>{c['comment']}</div>
        </div>
        """, unsafe_allow_html=True)

# [은행, 로또, 창조주 통제소는 기존 고퀄리티 기능 유지]
elif menu == "🏦 은행 (대출/송금)":
    st.title("🏦 글로벌 뱅크"); t1, t2 = st.tabs(["💸 송금", "💳 대출"])
    with t1:
        target = st.text_input("상대방 ID"); amt = st.number_input("송금액", min_value=0, step=10000000)
        if st.button("송금 실행"):
            u_db = load_db(USERS_FILE, {})
            if target in u_db and st.session_state.global_cash >= amt:
                st.session_state.global_cash -= amt; u_db[target]['cash'] += amt; save_db(USERS_FILE, u_db); sync_user_data(); st.success("송금 완료")
    with t2:
        st.metric("현재 빚", f"₩{st.session_state.loan:,}"); l_amt = st.number_input("대출 신청", min_value=0, step=1000000000)
        if st.button("대출 받기"): st.session_state.global_cash += l_amt; st.session_state.loan += l_amt; st.session_state.loan_time = time.time(); sync_user_data(); st.rerun()

elif menu == "⚔️ 1시간 글로벌 로또":
    st.title("⚔️ 글로벌 로또 잭팟")
    st.markdown(f"## 누적 상금: ₩{market['lotto_pool']:,}")
    my_t = market['lotto_tickets'].get(st.session_state.logged_in_user, 0); st.write(f"내 티켓: {my_t}장")
    b_cnt = st.number_input("구매 수량 (장당 1,000만)", min_value=1, step=1)
    if st.button("티켓 구매"):
        cost = b_cnt * 10000000
        if st.session_state.global_cash >= cost:
            st.session_state.global_cash -= cost; market['lotto_pool'] += cost; market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt; save_market(market); sync_user_data(); st.rerun()

elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 절대신 통제소")
    u_db = load_db(USERS_FILE, {}); sel_u = st.selectbox("유저 선택", list(u_db.keys()))
    c1, c2 = st.columns(2)
    new_c = c1.number_input("현금 변경", value=u_db[sel_u]['cash'])
    new_t = c2.text_input("칭호 강제 변경", value=u_db[sel_u]['equipped_title'])
    if st.button("⚠️ 신의 권능 행사 (데이터 변조)"): u_db[sel_u]['cash'] = new_c; u_db[sel_u]['equipped_title'] = new_t; save_db(USERS_FILE, u_db); st.success("조작 완료")
