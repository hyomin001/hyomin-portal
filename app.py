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
                'portfolio': st.session_state.portfolio,
                'solved_ids': list(st.session_state.get('solved_ids', []))
            })
            save_db(USERS_FILE, users)

# ==============================
# 초대형 고대비 스타일 (글씨 안보임 해결)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v7", page_icon="💰", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    .stApp { background-color: #0A0E17 !important; }
    
    /* 모든 텍스트 강제 흰색 & 굵게 */
    html, body, [class*="css"], .stMarkdown, p, label, span, li {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    
    h1 { font-size: 4.5rem !important; color: #00D4FF !important; }
    h2 { font-size: 3rem !important; color: #00FF88 !important; }

    /* 주식 테이블 (고대비) */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #161B22; border: 3px solid #444; }
    .stock-table th { background-color: #30363D; color: #00D4FF !important; font-size: 28px !important; padding: 15px; }
    .stock-table td { font-size: 28px !important; padding: 15px; border-bottom: 1px solid #444; text-align: center; }
    
    .price-up { color: #FF4B4B !important; font-weight: 900; }
    .price-down { color: #1F77B4 !important; font-weight: 900; }

    /* 버튼 스타일 */
    .stButton>button {
        height: 70px !important;
        border: 4px solid #00D4FF !important;
        background-color: #1A1C24 !important;
        color: #00D4FF !important;
        font-size: 28px !important;
        font-weight: 900 !important;
        border-radius: 15px;
    }
    input { color: black !important; font-size: 24px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 세션
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        choice = st.tabs(["🔒 로그인", "📝 시민등록"])
        with choice[0]:
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_ids': set(users[l_id].get('solved_ids', []))
                    })
                    st.rerun()
                else: st.error("정보 불일치")
        with choice[1]:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("성공! 로그인하세요.")
    st.stop()

# ==============================
# 주식 데이터 엔진 (10종목 고정)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SMSUNG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDAI", "name": "현대차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GDS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.12}, {"id": "VHDL", "name": "VHDL칩", "vol": 0.08}
]

# KeyError 방지를 위한 강력한 초기화
if 'stock_data' not in st.session_state or len(st.session_state.stock_data) != 10:
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [100000]} for s in stock_config}
if 'last_news' not in st.session_state: st.session_state.last_news = "주식 시장이 활발히 거래 중입니다."
if 'last_news_time' not in st.session_state: st.session_state.last_news_time = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.title("UNIVERSE")
    st.subheader(f"👤 {st.session_state.logged_in_user}")
    st.metric("자산", f"₩{st.session_state.global_cash:,}")
    if st.button("LOGOUT"):
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("메뉴 선택", ["🏠 홈", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 동기화", "💻 CBT 모의고사", "🏎️ 레이싱", "🎰 슬롯머신", "⛏️ 채굴기", "🛒 슈퍼 상점", "💬 게시판"])

# ==============================
# [1] 홈
# ==============================
if menu == "🏠 홈":
    st.title("반갑습니다! 효민 유니버스입니다. 🎉")
    st.write("---")
    st.markdown("""
    ### 🎮 플레이 가이드
    1. **주식 시장**: 10초마다 주가가 변합니다. 뉴스를 보고 풀매수하세요!
    2. **구단주**: 4-4-2 등 포메이션을 직접 짜고 30초 중계를 즐기세요.
    3. **통신**: 주파수를 맞춰 보너스를 받으세요. (틀리면 돈 깎임!)
    4. **상점**: 번 돈으로 100가지 명품 아이템을 수집하세요.
    """)
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")

# ==============================
# [2] 주식 (10초 자동 갱신 + 뉴스 + 포트폴리오)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 실시간 통합 거래소")
    
    # [뉴스 로직] 30초마다 랜덤 뉴스 발생
    if time.time() - st.session_state.last_news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.2, 0.2)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.last_news = f"📰 [뉴스] {target['name']}, {'역대급 실적 호재 발생!' if impact > 0 else '예상치 못한 위기 상황!'}"
        st.session_state.last_news_time = time.time()
    
    st.error(st.session_state.last_news)

    # [주가 변동 로직] 10초마다 자동 실행
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 30: curr['history'].pop(0)

    # UI 구성
    tab_market, tab_account = st.tabs(["📊 실시간 시장", "💼 내 포트폴리오"])
    
    with tab_market:
        rows = ""
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
            diff = curr['price'] - curr['history'][-2]
            pct = (diff / curr['history'][-2]) * 100
            color = "price-up" if diff >= 0 else "price-down"
            sign = "▲" if diff >= 0 else "▼"
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{color}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목</th><th>현재가</th><th>변동</th></tr>{rows}</table>", unsafe_allow_html=True)

    with tab_account:
        st.subheader("나의 주식 계좌 현황")
        my_port = []
        total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0:
                curr_p = st.session_state.stock_data[sid]['price']
                avg_p = info.get('avg_price', 0)
                eval_amt = qty * curr_p
                total_eval += eval_amt
                profit_pct = ((curr_p - avg_p) / avg_p * 100) if avg_p > 0 else 0
                my_port.append({"종목": st.session_state.stock_data[sid]['name'], "수량": qty, "평단가": f"₩{int(avg_p):,}", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{profit_pct:+.2f}%"})
        
        if my_port: st.table(pd.DataFrame(my_port))
        else: st.info("보유 주식이 없습니다.")
        st.markdown(f"### 💰 총 평가자산: ₩{total_eval:,} | 💵 현금: ₩{st.session_state.global_cash:,}")

    # 매매 컨트롤러
    st.write("---")
    c1, c2 = st.columns([1, 1])
    with c1:
        sel_name = st.selectbox("거래 종목", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    with c2:
        curr_p = st.session_state.stock_data[sid]['price']
        st.markdown(f"## {sel_name}: ₩{curr_p:,}")
        if st.button("💥 풀매수 (ALL-IN)"):
            buy_q = st.session_state.global_cash // curr_p
            if buy_q > 0:
                st.session_state.global_cash -= buy_q * curr_p
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_qty = old['qty'] + buy_q
                st.session_state.portfolio[sid] = {'qty': new_qty, 'avg_price': curr_p}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * curr_p
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data(); st.rerun()

    # 10초 대기 후 강제 갱신
    time.sleep(10); st.rerun()

# ==============================
# [3] 구단주 매니저 (포메이션 + 30초)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    form = st.selectbox("포메이션 지시", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (중원)", "5-4-1 (수비)"])
    if st.button(" Stadium 입장 (30초 경기 시작)"):
        board = st.empty(); bar = st.progress(0); log = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            board.markdown(f"<div style='text-align:center; background:#111; padding:20px; border:5px solid #00FF88;'><h1 style='font-size:100px;'>{h} : {a}</h1></div>", unsafe_allow_html=True)
            bar.progress((i+1)/30, text=f"경기 {i*3}분 진행 중...")
            log.warning(f"🎙️ {random.choice(['날카로운 공격!', '골키퍼 선방!', '치열한 몸싸움!', '관중의 함성!'])}")
            time.sleep(1)
        win_m = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += win_m; sync_user_data(); st.success(f"정산: +₩{win_m:,}")

# ==============================
# [4] 통신 신호 (패널티 강화)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 동기화 업무")
    if 'tf' not in st.session_state: st.session_state.tf = random.randint(2, 12); st.session_state.ta = random.randint(3, 10)
    st.markdown("### 💰 성공: +₩1,500,000 | ❌ 실패: -₩500,000")
    f = st.slider("주파수 조절", 1, 15, 5); a = st.slider("진폭 조절", 1, 15, 5)
    x = np.linspace(0, 10, 400); y_t = st.session_state.ta * np.sin(st.session_state.tf * x); y_u = a * np.sin(f * x)
    st.plotly_chart(px.line(pd.DataFrame({'x':x, 'Target':y_t, 'Input':y_u}), x='x', y=['Target', 'Input'], template='plotly_dark'))
    if st.button("동기화 승인"):
        if f == st.session_state.tf and a == st.session_state.ta:
            st.success("성공! +150만"); st.session_state.global_cash += 1500000; del st.session_state.tf
        else:
            st.error("실패! -50만"); st.session_state.global_cash -= 500000; del st.session_state.tf
        sync_user_data(); st.rerun()

# ==============================
# [5] CBT (무한 엔진)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 모의고사")
    q_pool = [("LIFO 구조?", "스택"), ("FIFO 구조?", "큐"), ("3계층?", "네트워크"), ("구조변경?", "ALTER"), ("테이블 삭제?", "DROP")]
    q, a = random.choice(q_pool)
    st.markdown(f"<h1 style='color:yellow;'>Q. {q}</h1>", unsafe_allow_html=True)
    ans = st.radio("정답 선택", [a, "응용", "물리", "UPDATE"])
    if st.button("제출"):
        if ans == a: st.success("정답! +₩500,000"); st.session_state.global_cash += 500000
        else: st.error("틀림")
        sync_user_data()

# ==============================
# [6] 레이싱 (역배 시스템)
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 역배 배팅")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    sel = st.selectbox("차량", [c['n'] for c in cars])
    amt = st.number_input("금액", min_value=10000, step=10000)
    if st.button("RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*3
            while max(pos) < 100:
                for i in range(3): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel:
                m = int(amt * win['o']); st.session_state.global_cash += m; st.balloons()
            else: st.error(f"우승: {win['n']}")
            sync_user_data()

# ==============================
# [7] 슬롯머신 (멈춤 기능)
# ==============================
elif menu == "🎰 슬롯머신":
    st.title("🎰 럭키 슬롯")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 레버 당기기 (10만)"): st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False
        res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<h1 style='font-size:150px; text-align:center;'>{' '.join(res)}</h1>", unsafe_allow_html=True)
        if res[0]==res[1]==res[2]: st.session_state.global_cash += 10000000; st.balloons()
        sync_user_data()
    if st.session_state.spin:
        area = st.empty()
        for _ in range(10):
            area.markdown(f"<h1 style='font-size:150px; text-align:center;'>{[random.choice(['💎','7️⃣','🍒']) for _ in range(3)]}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)

# ==============================
# [8] 채굴기 (금액 시각화)
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK!!", use_container_width=True):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:gold; font-size:150px;'>💰 +1,000</h1>", unsafe_allow_html=True)

# ==============================
# [9] 상점 (100개 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 LUXURY 100 ITEMS")
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            st.write(f"**명품 아이템 No.{i}** | ₩{i*10000000:,}")
            if f"i_{i}" in st.session_state.inventory: st.button("보유 중", key=f"i_{i}", disabled=True)
            elif st.button(f"구매하기 #{i}", key=f"i_{i}"):
                if st.session_state.global_cash >= i*10000000:
                    st.session_state.global_cash -= i*10000000; st.session_state.inventory.append(f"i_{i}"); sync_user_data(); st.rerun()

# ==============================
# [10] 게시판
# ==============================
elif menu == "💬 게시판":
    st.title("💬 자유 게시판")
    msg = st.text_input("메시지")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])): st.write(f"**{c['name']}**: {c['comment']}")
