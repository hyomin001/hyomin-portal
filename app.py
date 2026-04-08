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
MARKET_FILE = "market_db.json" # 모든 유저가 100% 동일하게 공유하는 시장 DB

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

def load_db(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return default
    return default

def save_db(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def sync_user_data():
    if 'logged_in_user' in st.session_state:
        users = load_db(USERS_FILE, {})
        uid = st.session_state.logged_in_user
        if uid in users:
            users[uid].update({
                'cash': st.session_state.global_cash,
                'inventory': st.session_state.inventory,
                'equipped_title': st.session_state.equipped_title,
                'portfolio': st.session_state.portfolio
            })
            save_db(USERS_FILE, users)

def get_market():
    def init_market():
        data = {
            "version": 2, 
            "stock_data": {},
            "news": "시장이 안정적으로 운영 중입니다.",
            "news_time": time.time(),
            "last_tick": time.time()
        }
        for s in stock_config:
            p = random.randint(50000, 150000)
            data["stock_data"][s['id']] = {"name": s['name'], "price": p, "history": [p]}
        return data

    if not os.path.exists(MARKET_FILE):
        data = init_market()
        save_db(MARKET_FILE, data)
        return data
        
    data = load_db(MARKET_FILE, {})
    db_keys = set(data.get('stock_data', {}).keys())
    c_keys = set([s['id'] for s in stock_config])
    if data.get("version") != 2 or db_keys != c_keys:
        data = init_market()
        save_db(MARKET_FILE, data)
        return data
        
    return data

def save_market(data): save_db(MARKET_FILE, data)

def get_rankings(market_data):
    users = load_db(USERS_FILE, {})
    rankings = []
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for uid, data in users.items():
        wealth = data.get('cash', 0)
        for sid, p_data in data.get('portfolio', {}).items():
            if sid in prices: wealth += p_data.get('qty', 0) * prices[sid]
        rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

st.set_page_config(page_title="HYOMIN UNIVERSE v12.0", page_icon="🐋", layout="wide")

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("""
    <style>
        .stApp { background-color: #050505 !important; color: white !important; }
        h1 { text-align: center; color: #00E5FF !important; font-weight: 900 !important; font-size: 4rem !important; }
        p { text-align: center; font-size: 20px !important; color: #FFF !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<p>슈퍼개미의 움직임이 시장 전체를 뒤흔듭니다. 눈치싸움에 참전하세요!</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("💻 접속 환경 선택", ["🖥️ PC (데스크탑/태블릿)", "📱 모바일 (스마트폰)"], horizontal=True)
        st.write("---")
        
        choice = st.tabs(["🔑 로그인", "📝 시민등록"])
        with choice[0]:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'], 'inventory': users[l_id]['inventory'],
                        'equipped_title': users[l_id].get('equipped_title', '신규시민'), 'portfolio': users[l_id].get('portfolio', {}),
                        'device_mode': device_mode
                    }); st.rerun()
                else: st.error("정보 불일치")
        with choice[1]:
            n_id = st.text_input("새 아이디")
            n_pw = st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("중복된 이름입니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인하세요.")
    st.stop()

# ==============================
# 🎨 동적 CSS 적용 (PC vs Mobile)
# ==============================
if st.session_state.device_mode == "🖥️ PC (데스크탑/태블릿)":
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
        .stApp { background-color: #050505 !important; }
        html, body, [class*="css"], .stMarkdown, p, span, li, label { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; font-size: 24px !important; font-weight: 700 !important; }
        div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
        div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 24px !important; font-weight: 900 !important; }
        div[data-baseweb="popover"] * { background-color: #1A1C24 !important; color: #00FF88 !important; font-size: 22px !important; }
        .stNumberInput input { background-color: #222 !important; color: #00FF88 !important; font-size: 26px !important; }
        [data-testid="stSidebar"] { background-color: #001F3F !important; border-right: 4px solid #00E5FF; }
        div[data-testid="stSidebarNav"] span, .stRadio label p { color: #FFD600 !important; font-size: 26px !important; font-weight: 900 !important; }
        .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 3px solid #444; }
        .stock-table th { background-color: #333; color: #FFD600 !important; font-size: 28px !important; padding: 15px; text-align: center; }
        .stock-table td { font-size: 26px !important; padding: 15px; border-bottom: 2px solid #333; text-align: center; }
        .p-up { color: #FF4B4B !important; font-weight: 900; }
        .p-down { color: #1F77B4 !important; font-weight: 900; }
        h1 { font-size: 4.5rem !important; color: #00E5FF !important; font-weight: 900 !important; text-align: center; }
        h2 { font-size: 3rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }
        .stButton>button { height: 80px !important; border: 4px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; font-size: 28px !important; font-weight: 900 !important; border-radius: 15px; width: 100%; }
        .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
        .slot-text { text-align: center; font-weight: 900; font-size: 150px !important; margin: 0; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
        .stApp { background-color: #050505 !important; }
        html, body, [class*="css"], .stMarkdown, p, span, li, label { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; font-size: 16px !important; font-weight: 700 !important; }
        div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
        div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 16px !important; font-weight: 900 !important; }
        div[data-baseweb="popover"] * { background-color: #1A1C24 !important; color: #00FF88 !important; font-size: 16px !important; }
        .stNumberInput input { background-color: #222 !important; color: #00FF88 !important; font-size: 18px !important; }
        .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 2px solid #444; }
        .stock-table th { background-color: #333; color: #FFD600 !important; font-size: 14px !important; padding: 8px; text-align: center; }
        .stock-table td { font-size: 14px !important; padding: 8px; border-bottom: 1px solid #333; text-align: center; }
        .p-up { color: #FF4B4B !important; font-weight: 900; }
        .p-down { color: #1F77B4 !important; font-weight: 900; }
        h1 { font-size: 2.2rem !important; color: #00E5FF !important; font-weight: 900 !important; text-align: center; }
        h2 { font-size: 1.8rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }
        .stButton>button { height: 55px !important; border: 2px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; font-size: 18px !important; font-weight: 900 !important; border-radius: 12px; width: 100%; }
        .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
        .slot-text { text-align: center; font-weight: 900; font-size: 60px !important; margin: 0; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==============================
# 🌐 통합 글로벌 시장 동기화
# ==============================
market = get_market()
current_time = time.time()
market_updated = False

# 10초 주가 자동 변동
if current_time - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 30: curr['history'].pop(0)
    market['last_tick'] = current_time
    market_updated = True

# 30초 정규 뉴스
if current_time - market.get('news_time', 0) > 30:
    target = random.choice(stock_config)
    impact = random.uniform(-0.15, 0.15)
    market['stock_data'][target['id']]['price'] = int(market['stock_data'][target['id']]['price'] * (1 + impact))
    market['news'] = f"📰 [정규속보] {target['name']}, {'어닝 서프라이즈로 시장 기대감 상승!' if impact > 0 else '실적 부진으로 투자심리 위축'}"
    market['news_time'] = current_time
    market_updated = True

if market_updated: save_market(market)

# ==============================
# 🧭 메뉴 분기
# ==============================
menu_options = ["🏠 홈 광장", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 업무", "💻 CBT 모의고사", "🏎️ 레이싱", "🎰 슬롯머신", "⛏️ 채굴기", "👑 칭호 상점", "💬 랭커 게시판"]

if st.session_state.device_mode == "🖥️ PC (데스크탑/태블릿)":
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.logged_in_user}님")
        st.markdown(f"**칭호**: `{st.session_state.equipped_title}`")
        st.metric("💰 보유 자산", f"₩{st.session_state.global_cash:,}")
        if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        st.markdown("---")
        menu = st.radio("포털 이동", menu_options)
        st.markdown("---")
        st.markdown("### 🏆 서버 통합 랭킹")
        for i, r in enumerate(get_rankings(market)[:3]): st.write(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")
else:
    st.markdown(f"<div style='text-align:right; color:#FFD600;'>👤 <b>{st.session_state.logged_in_user}</b> <br> 🎖️ {st.session_state.equipped_title} <br> 💰 <b>₩{st.session_state.global_cash:,}</b></div>", unsafe_allow_html=True)
    menu = st.selectbox("📌 이동할 메뉴를 선택하세요", menu_options)
    with st.expander("🏆 통합 랭킹 보기"):
        for i, r in enumerate(get_rankings(market)[:5]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "🏅"
            st.write(f"{medal} **{r['uid']}**: ₩{r['total']:,.0f}")
        if st.button("🔴 로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")

# ==============================
# [1] 홈
# ==============================
if menu == "🏠 홈 광장":
    st.title(f"환영합니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("현재 **대주주(고래) 시장 개입 시스템**이 활성화되었습니다. 100억 이상의 대규모 자금이 움직이면 전 서버에 속보가 뜨며 시장이 요동칩니다!")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")
    


# ==============================
# [2] 주식 (고래 시스템 탑재)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 글로벌 통합 거래소")
    
    # 상단 뉴스 (가장 눈에 띄게)
    news_color = "#FF4B4B" if "폭등" in market['news'] else "#1F77B4" if "폭락" in market['news'] else "#FFD600"
    st.markdown(f"<div style='background-color:#222; padding:15px; border-left:10px solid {news_color}; margin-bottom:20px;'><h3 style='color:{news_color}; margin:0;'>{market['news']}</h3></div>", unsafe_allow_html=True)
    
    t_mkt, t_acc = st.tabs(["📊 시황", "💼 내 포트폴리오"])
    
    with t_mkt:
        rows = ""
        for s in stock_config:
            curr = market['stock_data'][s['id']]
            diff = curr['price'] - curr['history'][-2] if len(curr['history']) > 1 else 0
            pct = (diff / curr['history'][-2]) * 100 if len(curr['history']) > 1 else 0
            cls, sign = ("p-up", "▲") if diff >= 0 else ("p-down", "▼")
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{cls}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목</th><th>현재가</th><th>변동</th></tr>{rows}</table>", unsafe_allow_html=True)
        
    with t_acc:
        st.subheader("보유 계좌")
        p_list = []
        total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp = market['stock_data'][sid]['price']
                ap = info.get('avg_price', 0)
                eval_amt = qty * cp
                total_eval += eval_amt
                roi = ((cp - ap) / ap * 100) if ap > 0 else 0
                p_list.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("주식을 매수해보세요!")
        st.markdown(f"💰 주식자산: ₩{total_eval:,} | 💵 현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    sel_name = st.selectbox("매매할 종목을 고르세요", [s['name'] for s in stock_config])
    sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
    st.plotly_chart(px.line(y=market['stock_data'][sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    cp = market['stock_data'][sid]['price']
    st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{cp:,}</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💥 풀매수"):
            max_q = st.session_state.global_cash // cp
            buy_amt = max_q * cp
            if max_q > 0:
                st.session_state.global_cash -= buy_amt
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + max_q
                new_a = ((old['qty'] * old['avg_price']) + buy_amt) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data()
                
                # 🐋 대주주(고래) 매수 로직: 100억 이상 매수 시 주가 폭등
                if buy_amt >= 10000000000:
                    # 1000억당 10% 상승, 최대 50%까지 제한
                    impact = min((buy_amt / 100000000000) * 0.1, 0.5) 
                    market['stock_data'][sid]['price'] = int(cp * (1 + impact))
                    market['news'] = f"🚨 [슈퍼개미 출현] {st.session_state.equipped_title} {st.session_state.logged_in_user}님이 {sel_name}에 ₩{buy_amt//100000000:,}억 풀매수!! 주가 폭등!"
                    market['news_time'] = time.time()
                    save_market(market)
                st.rerun()
    with c2:
        if st.button("💸 풀매도"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            sell_amt = owned * cp
            if owned > 0:
                st.session_state.global_cash += sell_amt
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data()
                
                # 🐋 대주주(고래) 매도 로직: 50억 이상 매도 시 주가 폭락
                if sell_amt >= 5000000000:
                    impact = min((sell_amt / 100000000000) * 0.1, 0.5)
                    market['stock_data'][sid]['price'] = max(1000, int(cp * (1 - impact)))
                    market['news'] = f"📉 [패닉 셀] 대주주 {st.session_state.logged_in_user}님이 {sel_name} ₩{sell_amt//100000000:,}억 물량 투하!! 주가 폭락!"
                    market['news_time'] = time.time()
                    save_market(market)
                st.rerun()
    time.sleep(2); st.rerun()

# ==============================
# [3] 구단주
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    form = st.selectbox("포메이션 전술", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (중원)", "5-4-1 (수비)"])
    if st.button("🏟️ 경기 시작 (30초)"):
        b = st.empty(); p = st.progress(0); l = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            b.markdown(f"<div style='text-align:center; background:#000; border:2px solid #00FF88; padding:20px; border-radius:20px;'><div class='slot-text'>{h} : {a}</div></div>", unsafe_allow_html=True)
            p.progress((i+1)/30)
            l.info(f"🎙️ {random.choice(['측면 돌파!', '상대 역습!', '골키퍼 선방!', '중원 볼다툼!'])}")
            time.sleep(1)
        res = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += res; sync_user_data(); st.success(f"정산: +₩{res:,}")

# ==============================
# [4] 통신 업무
# ==============================
elif menu == "📡 통신 업무":
    st.title("📡 신호 동기화")
    if 'tf' not in st.session_state: st.session_state.tf = random.randint(2, 12); st.session_state.ta = random.randint(3, 10)
    st.markdown("### 💰 성공: +150만 | ❌ 실패: -50만")
    f = st.slider("주파수", 1, 15, 5); a = st.slider("진폭", 1, 15, 5)
    st.plotly_chart(px.line(y=a * np.sin(f * np.linspace(0, 10, 400)), template='plotly_dark', height=250), use_container_width=True)
    if st.button("📡 신호 승인"):
        if f == st.session_state.tf and a == st.session_state.ta: st.session_state.global_cash += 1500000; st.balloons()
        else: st.session_state.global_cash -= 500000
        del st.session_state.tf; sync_user_data(); st.rerun()

# ==============================
# [5] CBT 하드코어
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 실전 모의고사")
    if 'hard_q_pool' not in st.session_state:
        st.session_state.hard_q_pool = [
            {"q": "결합도(Coupling) 중 결합도가 가장 좋은 것은?", "a": "자료 결합도", "w": ["스탬프 결합도", "제어 결합도", "내용 결합도"]},
            {"q": "응집도(Cohesion) 중 응집도가 가장 좋은 것은?", "a": "기능적 응집도", "w": ["논리적 응집도", "시간적 응집도", "절차적 응집도"]},
            {"q": "GoF 패턴 중 '생성' 패턴이 아닌 것은?", "a": "Adapter", "w": ["Builder", "Singleton", "Prototype"]},
            {"q": "화이트박스 테스트 기법은?", "a": "기본 경로 검사", "w": ["경계값 분석", "동치 분할 검사", "원인-효과 그래프"]},
            {"q": "DB 제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행적 함수 종속 제거", "다치 종속 제거", "결정자가 후보키가 아닌 것 제거"]}
        ]
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(st.session_state.hard_q_pool)
        opts = st.session_state.current_q['w'] + [st.session_state.current_q['a']]
        random.shuffle(opts)
        st.session_state.current_opts = opts
    with st.form("exam"):
        st.markdown(f"<h2 style='color:#FFD600;'>Q. {st.session_state.current_q['q']}</h2>", unsafe_allow_html=True)
        ans = st.radio("정답 선택:", st.session_state.current_opts)
        if st.form_submit_button("제출"):
            if ans == st.session_state.current_q['a']: st.session_state.global_cash += 500000; st.success("정답! +50만")
            else: st.error(f"오답! (정답: {st.session_state.current_q['a']})")
            del st.session_state.current_q; sync_user_data(); st.rerun()

# ==============================
# [6] 레이싱
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 역배 챔피언십")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("배팅액", min_value=10000, step=10000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt; bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*3
            while max(pos) < 100:
                for i in range(3): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel: st.session_state.global_cash += int(amt * win['o']); st.success("승리!")
            else: st.error(f"우승: {win['n']}"); sync_user_data()

# ==============================
# [7] 슬롯머신
# ==============================
elif menu == "🎰 슬롯머신":
    st.title("🎰 럭키 슬롯 (수동정지)")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 당기기"): 
        if st.session_state.global_cash >= 100000: st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False; res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<div class='slot-text'>{' '.join(res)}</div>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]: st.session_state.global_cash += 10000000; st.balloons()
        sync_user_data()
    if st.session_state.spin:
        slot = st.empty()
        for _ in range(10): slot.markdown(f"<div class='slot-text'>{[random.choice(['💎','7️⃣','🍒']) for _ in range(3)]}</div>", unsafe_allow_html=True); time.sleep(0.1)

# ==============================
# [8] 채굴기
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 클릭! (+1,000)", use_container_width=True):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='color:gold;'>💰 +1,000</h1>", unsafe_allow_html=True)

# ==============================
# 👑 [9] 칭호 상점
# ==============================
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id = f"title_{i}"
            price = i * 10000000
            st.markdown(f"**{title_name}** | ₩{price:,}")
            if title_id in st.session_state.inventory:
                if st.session_state.equipped_title == title_name: st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"): st.session_state.equipped_title = title_name; sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        st.session_state.global_cash -= price; st.session_state.inventory.append(title_id)
                        st.session_state.equipped_title = title_name; sync_user_data(); st.rerun()
                    else: st.error("잔액 부족")

# ==============================
# 💬 [10] 게시판
# ==============================
elif menu == "💬 랭커 게시판":
    st.title("💬 랭커 게시판")
    msg = st.text_input("메시지 입력")
    if st.button("등록"):
        if msg:
            new_comment = {"name": st.session_state.logged_in_user, "title": st.session_state.equipped_title, "comment": msg, "time": datetime.now().strftime("%m-%d %H:%M")}
            save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [new_comment]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        st.markdown(f"""
        <div style='background-color: #111; border-left: 5px solid #00FF88; padding: 15px; margin-bottom: 15px; border-radius: 8px;'>
            <div style='margin-bottom: 8px;'>
                <span style='background-color: #222; color: #FFD600; border: 1px solid #FFD600; padding: 3px 8px; border-radius: 5px; font-size: 14px; margin-right: 10px;'>{c.get('title', '신규시민')}</span>
                <b style='color: #00E5FF; font-size: 20px;'>{c['name']}</b>
                <span style='color: #888; font-size: 12px; margin-left: 10px;'>{c.get('time', '')}</span>
            </div>
            <div style='color: #FFF; font-size: 18px; margin-left: 5px;'>{c['comment']}</div>
        </div>
        """, unsafe_allow_html=True)
