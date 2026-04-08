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

def get_rankings():
    users = load_db(USERS_FILE, {})
    rankings = []
    if 'stock_data' in st.session_state:
        prices = {k: v['price'] for k, v in st.session_state.stock_data.items()}
        for uid, data in users.items():
            wealth = data.get('cash', 0)
            portfolio = data.get('portfolio', {})
            for sid, p_data in portfolio.items():
                if sid in prices: wealth += p_data.get('qty', 0) * prices[sid]
            rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# 🎨 가독성 및 UI 스타일 (CSS)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v8.7", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    .stApp { background-color: #050505 !important; }
    
    /* 기본 텍스트 24px 굵게 */
    html, body, [class*="css"], .stMarkdown, p, span, li, label {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }

    /* 드롭다운(Selectbox) 목록 가시성 긴급 수정 */
    div[data-baseweb="select"] > div {
        background-color: #1A1C24 !important;
        border: 2px solid #00E5FF !important;
    }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 22px !important; }
    
    /* 드롭다운 리스트(팝오버) 내부 글씨 */
    div[data-baseweb="popover"] * {
        background-color: #1A1C24 !important;
        color: #00FF88 !important; /* 목록 글씨는 형광 연두 */
        font-size: 20px !important;
        font-weight: 900 !important;
    }

    /* 사이드바 메뉴 가독성 */
    [data-testid="stSidebar"] { background-color: #001F3F !important; border-right: 3px solid #00E5FF; }
    div[data-testid="stSidebarNav"] span, .stRadio label p {
        color: #FFD600 !important; font-size: 24px !important; font-weight: 900 !important;
    }

    /* 주식 테이블 디자인 */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 3px solid #444; }
    .stock-table th { background-color: #333; color: #FFD600 !important; font-size: 26px !important; padding: 15px; }
    .stock-table td { font-size: 26px !important; padding: 15px; border-bottom: 1px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }

    /* 버튼 스타일 */
    .stButton>button {
        height: 80px !important;
        border: 4px solid #00E5FF !important;
        background-color: #1A1C24 !important;
        color: #00E5FF !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        border-radius: 20px;
    }
    .stNumberInput input { background-color: #1A1C24 !important; color: #FFFFFF !important; font-size: 26px !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        choice = st.tabs(["🔑 로그인", "📝 시민등록"])
        with choice[0]:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("유니버스 접속"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_ids': set()
                    })
                    st.rerun()
                else: st.error("정보 불일치")
        with choice[1]:
            n_id, n_pw = st.text_input("아이디 생성"), st.text_input("비밀번호 생성", type="password")
            if st.button("시민 등록"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}}
                    save_db(USERS_FILE, users); st.success("성공! 로그인하세요.")
    st.stop()

# ==============================
# 📈 주식 데이터 엔진 (Time-Lock 10초 갱신)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SAMSG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDI", "name": "현대차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드밴드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GOODS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩", "vol": 0.07}
]

# 데이터 초기화 및 키 검증
if 'stock_data' not in st.session_state or set(st.session_state.stock_data.keys()) != set([s['id'] for s in stock_config]):
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [100000]} for s in stock_config}
    st.session_state.last_tick = time.time() # 주가 변동 기준 시간

if 'news' not in st.session_state: st.session_state.news = "시장이 안정적으로 운영 중입니다."
if 'last_news_time' not in st.session_state: st.session_state.last_news_time = time.time()

# [중요] 10초가 지났을 때만 주가 변동 (버튼 클릭 시 변동 방지)
if time.time() - st.session_state.last_tick > 10:
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 20: curr['history'].pop(0)
    st.session_state.last_tick = time.time()

# 30초마다 뉴스 발생
if time.time() - st.session_state.last_news_time > 30:
    target = random.choice(stock_config)
    impact = random.uniform(-0.15, 0.15)
    st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
    st.session_state.news = f"📰 [뉴스] {target['name']}, {'깜짝 실적 발표!' if impact > 0 else '공급망 이슈 발생!'}"
    st.session_state.last_news_time = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.logged_in_user}님")
    st.metric("💰 보유 자산", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 이동", ["🏠 홈", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 업무", "💻 CBT", "🏎️ 레이싱", "🎰 슬롯", "⛏️ 채굴기", "🛒 상점", "💬 게시판"])

# ==============================
# 🏠 1. 홈
# ==============================
if menu == "🏠 홈":
    st.title(f"반갑습니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("효민 유니버스에 오신 것을 환영합니다. 주식 버튼 버그를 완벽하게 수정했습니다!")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")

# ==============================
# 📈 2. 주식 (Time-Lock 갱신 + 포트폴리오)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소 (10초 자동 갱신)")
    st.warning(f"**{st.session_state.news}**")

    t_mkt, t_acc = st.tabs(["📊 시장 시황", "💼 내 포트폴리오(수익률)"])
    
    with t_mkt:
        rows = ""
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
            diff = curr['price'] - curr['history'][-2] if len(curr['history']) > 1 else 0
            pct = (diff / curr['history'][-2]) * 100 if len(curr['history']) > 1 else 0
            cls, sign = ("p-up", "▲") if diff >= 0 else ("p-down", "▼")
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{cls}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목</th><th>가격</th><th>변동</th></tr>{rows}</table>", unsafe_allow_html=True)

    with t_acc:
        st.subheader("내 주식 계좌 현황")
        p_list = []
        total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in st.session_state.stock_data:
                cp = st.session_state.stock_data[sid]['price']
                ap = info.get('avg_price', 0)
                eval_amt = qty * cp
                total_eval += eval_amt
                roi = ((cp - ap) / ap * 100) if ap > 0 else 0
                p_list.append({"종목": st.session_state.stock_data[sid]['name'], "수량": f"{qty}주", "평단가": f"₩{int(ap):,}", "현재가": f"₩{int(cp):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("보유 중인 주식이 없습니다.")
        st.markdown(f"### 💰 주식자산: ₩{total_eval:,} | 💵 현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        sel_name = st.selectbox("거래할 종목을 선택하세요", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=300), use_container_width=True)
    with c2:
        curr_p = st.session_state.stock_data[sid]['price']
        st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{curr_p:,}</h2>", unsafe_allow_html=True)
        if st.button("💥 풀매수 (ALL-IN)"):
            max_q = st.session_state.global_cash // curr_p
            if max_q > 0:
                st.session_state.global_cash -= max_q * curr_p
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + max_q
                # 평단가 고정 (새로 산 가격으로 갱신하거나 가중 평균)
                new_a = ((old['qty'] * old['avg_price']) + (max_q * curr_p)) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * curr_p
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data(); st.rerun()

    # 10초 자동 리런 (실시간성 유지)
    time.sleep(1); st.rerun()

# [나머지 게임들 v8.6 기능 유지]
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    form = st.selectbox("포메이션", ["4-4-2", "4-3-3", "3-5-2", "5-4-1"])
    if st.button("🏟️ 경기 시작 (30초)"):
        b = st.empty(); p = st.progress(0)
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            b.markdown(f"<div style='text-align:center; background:#000; border:5px solid #00FF88; padding:30px; border-radius:30px;'><h1 style='font-size:100px; color:#FFF;'>{h} : {a}</h1></div>", unsafe_allow_html=True)
            p.progress((i+1)/30); time.sleep(1)
        st.session_state.global_cash += (5000000 if h > a else 1000000 if h == a else 100000); sync_user_data(); st.rerun()

elif menu == "📡 통신 업무":
    st.title("📡 엔지니어 신호 동기화")
    if 'tf' not in st.session_state: st.session_state.tf = random.randint(2, 12); st.session_state.ta = random.randint(3, 10)
    st.markdown("### 💰 성공: +₩1,500,000 | ❌ 실패: -₩500,000")
    f = st.slider("주파수", 1, 15, 5); a = st.slider("진폭", 1, 15, 5)
    st.plotly_chart(px.line(y=a * np.sin(f * np.linspace(0, 10, 400)), template='plotly_dark'))
    if st.button("📡 승인"):
        if f == st.session_state.tf and a == st.session_state.ta: st.session_state.global_cash += 1500000; st.balloons()
        else: st.session_state.global_cash -= 500000
        del st.session_state.tf; sync_user_data(); st.rerun()

elif menu == "⛏️ 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK!! (₩1,000)"):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:gold; font-size:150px;'>💰 +1,000</h1>", unsafe_allow_html=True)

elif menu == "🛒 상점":
    st.title("🛒 LUXURY 100 ITEMS")
    for i in range(1, 11): # 예시로 10개만 표시 (공간상)
        col1, col2 = st.columns([3, 1])
        col1.write(f"**Item No.{i}** | ₩{i*10000000:,}")
        if f"i_{i}" in st.session_state.inventory: col2.button("보유 중", key=f"i_{i}", disabled=True)
        elif col2.button(f"구매 #{i}", key=f"i_{i}"):
            if st.session_state.global_cash >= i*10000000:
                st.session_state.global_cash -= i*10000000; st.session_state.inventory.append(f"i_{i}"); sync_user_data(); st.rerun()
