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
# 데이터베이스 및 시스템 설정
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
    # 주식 데이터가 아직 생성 전일 경우를 대비해 기본값 설정
    prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()}
    for uid, data in users.items():
        wealth = data.get('cash', 0)
        portfolio = data.get('portfolio', {})
        for sid, p_data in portfolio.items():
            # 현재 가격이 있으면 합산
            wealth += p_data.get('qty', 0) * prices.get(sid, p_data.get('avg_price', 0))
        rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# 🎨 UI 디자인 (사이드바 메뉴 및 글씨 강조)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v8.2", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    /* 전체 배경: 검정색 */
    .stApp { background-color: #050505 !important; }
    
    /* 기본 텍스트: 흰색 & 굵게 */
    html, body, [class*="css"], .stMarkdown, p, label, span, li {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    /* 사이드바 글씨 및 배경 (핵심 수정) */
    [data-testid="stSidebar"] {
        background-color: #001F3F !important; /* 진한 네이비 */
        border-right: 3px solid #00E5FF;
    }
    
    /* 사이드바 메뉴 라디오 버튼 글씨를 노란색으로 */
    div[data-testid="stSidebarNav"] span, .stRadio label p {
        color: #FFD600 !important; 
        font-size: 24px !important;
        font-weight: 900 !important;
    }

    /* 헤더 스타일 */
    h1 { font-size: 4.5rem !important; color: #00E5FF !important; font-weight: 900 !important; text-align: center; }
    h2 { font-size: 2.8rem !important; color: #00FF88 !important; }

    /* 주식 테이블 디자인 */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 3px solid #444; }
    .stock-table th { background-color: #222; color: #00E5FF !important; font-size: 28px !important; padding: 15px; }
    .stock-table td { font-size: 26px !important; padding: 15px; border-bottom: 2px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }

    /* 버튼 스타일 */
    .stButton>button {
        height: 75px !important;
        border: 4px solid #00E5FF !important;
        background-color: #1A1C24 !important;
        color: #00E5FF !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 15px;
    }
    .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
    
    /* 입력창 */
    input { color: black !important; font-size: 24px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size: 28px;'>글씨와 메뉴 가시성을 대폭 개선했습니다. 지금 입장하세요!</p>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        tab_log = st.tabs(["🔑 로그인", "📝 시민등록"])
        with tab_log[0]:
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
                else: st.error("아이디 또는 비밀번호가 틀립니다.")
        with tab_log[1]:
            n_id = st.text_input("새 아이디")
            n_pw = st.text_input("새 비밀번호", type="password")
            if st.button("등록 완료"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 존재하는 이름입니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인해 주세요.")
    st.stop()

# ==============================
# 📈 주식 엔진 (KeyError 방지 및 종목 설정)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SAMSG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDI", "name": "현대자동차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GOODS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이자동차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩셋", "vol": 0.07}
]

# 종목 리스트가 바뀌었거나 데이터가 없으면 강제 재설정 (KeyError 해결)
if 'stock_data' not in st.session_state or set(st.session_state.stock_data.keys()) != set([s['id'] for s in stock_config]):
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [80000]} for s in stock_config}
if 'news' not in st.session_state: st.session_state.news = "주식 시장이 개장되었습니다."
if 'news_time' not in st.session_state: st.session_state.news_time = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.logged_in_user}님")
    st.markdown(f"**칭호:** `{st.session_state.equipped_title}`")
    st.metric("💰 보유 현금", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): 
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 메뉴", ["🏠 홈 광장", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 업무", "💻 CBT 모의고사", "🏎️ 레이싱", "🎰 슬롯머신", "⛏️ 채굴기", "🛒 슈퍼 상점", "💬 게시판"])
    
    st.markdown("---")
    st.markdown("### 🏆 부자 랭킹")
    for i, r in enumerate(get_rankings()[:3]):
        st.write(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")

# ==============================
# [1] 홈 (인사말 자동화)
# ==============================
if menu == "🏠 홈 광장":
    st.title(f"반갑습니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("효민 유니버스에 방문해주셔서 감사합니다. 이곳은 자산을 모으고 경쟁하는 가상 포털입니다.")
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🎮 게임 콘텐츠")
        st.markdown("- **주식**: 10초마다 자동 갱신! 뉴스 분석 필수.\n- **구단주**: 전술을 짜고 30초 중계 시청.\n- **통신**: 파형 맞추기 보너스 도전.")
    with col2:
        st.subheader("🛒 상점 & 랭킹")
        st.markdown("- **상점**: 100종의 럭셔리 아이템 입고.\n- **랭킹**: 실시간으로 반영되는 부의 상징.")
    st.info("💡 사이드바 메뉴가 이제 아주 잘 보입니다. 원하는 게임을 선택하세요!")

# ==============================
# [2] 주식 (10초 자동 갱신 + 뉴스 + 포트폴리오)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 실시간 통합 거래소")
    
    # 30초 뉴스 엔진
    if time.time() - st.session_state.news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.15, 0.15)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.news = f"📰 [속보] {target['name']}, 혁신 기술 개발로 시장을 뒤흔들다!" if impact > 0 else f"📰 [속보] {target['name']}, 예상치 못한 악재 발생!"
        st.session_state.news_time = time.time()

    st.warning(f"**{st.session_state.news}**")

    # 10초 주가 변동 로직
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 20: curr['history'].pop(0)

    t_market, t_mine = st.tabs(["📊 시장 시황", "💼 내 포트폴리오(계좌)"])
    
    with t_market:
        rows_html = ""
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
            diff = curr['price'] - curr['history'][-2]
            pct = (diff / curr['history'][-2]) * 100
            cls, sign = ("p-up", "▲") if diff >= 0 else ("p-down", "▼")
            rows_html += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{cls}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목명</th><th>현재가</th><th>전일비</th></tr>{rows_html}</table>", unsafe_allow_html=True)

    with t_mine:
        st.subheader("보유 주식 상세 현황")
        p_list = []
        total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0:
                curr_p = st.session_state.stock_data[sid]['price']
                avg_p = info.get('avg_price', 0)
                eval_amt = qty * curr_p
                total_eval += eval_amt
                roi = ((curr_p - avg_p) / avg_p * 100) if avg_p > 0 else 0
                p_list.append({"종목": st.session_state.stock_data[sid]['name'], "수량": f"{qty}주", "평단가": f"₩{int(avg_p):,}", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("보유 중인 주식이 없습니다.")
        st.markdown(f"### 💰 주식 총액: ₩{total_eval:,} | 💵 가용 현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    c_chart, c_trade = st.columns([1, 1])
    with c_chart:
        sel_name = st.selectbox("거래 종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=300), use_container_width=True)
    with c_trade:
        cp = st.session_state.stock_data[sid]['price']
        st.markdown(f"## {sel_name}: ₩{cp:,}")
        if st.button("💥 풀매수 (ALL-IN)"):
            buyable = st.session_state.global_cash // cp
            if buyable > 0:
                st.session_state.global_cash -= buyable * cp
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + buyable
                new_a = ((old['qty'] * old['avg_price']) + (buyable * cp)) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * cp
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data(); st.rerun()
    time.sleep(10); st.rerun()

# ==============================
# [3] 구단주 매니저 (포메이션 + 30초)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 라이브 시뮬레이터")
    f_choice = st.selectbox("경기 전술 선택", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (점유율)", "5-4-1 (수비)"])
    if st.button("🏟️ Stadium 입장 (30초 경기 시작)"):
        b = st.empty(); p = st.progress(0); l = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            b.markdown(f"<div style='text-align:center; background:#000; border:5px solid #00FF88; padding:30px; border-radius:30px;'><h1 style='font-size:120px; color:#FFF;'>{h} : {a}</h1></div>", unsafe_allow_html=True)
            p.progress((i+1)/30, text=f"경기 {i*3}분 경과...")
            l.info(f"🎙️ 중계: {random.choice(['측면 파고듭니다!', '아! 상대의 위협적인 중거리!', '골키퍼 선방!', '치열한 볼다툼!'])}")
            time.sleep(1)
        win = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += win; sync_user_data(); st.success(f"정산 완료: +₩{win:,}")

# ==============================
# [4] 통신 업무 (벌금/보너스 명시)
# ==============================
elif menu == "📡 통신 업무":
    st.title("📡 엔지니어 신호 동기화")
    if 'tf' not in st.session_state: st.session_state.tf = random.randint(2, 12); st.session_state.ta = random.randint(3, 10)
    st.markdown("<div style='background:#222; border-left:10px solid #00E5FF; padding:20px;'>### 💰 성공: <span style='color:#00FF88;'>+₩1,500,000</span> | ❌ 실패: <span style='color:#FF3D00;'>-₩500,000</span></div>", unsafe_allow_html=True)
    f = st.slider("주파수", 1, 15, 5); a = st.slider("진폭", 1, 15, 5)
    x = np.linspace(0, 10, 400); y_t = st.session_state.ta * np.sin(st.session_state.tf * x); y_u = a * np.sin(f * x)
    st.plotly_chart(px.line(pd.DataFrame({'x':x, 'Target':y_t, 'Input':y_u}), x='x', y=['Target', 'Input'], template='plotly_dark'))
    if st.button("📡 신호 승인"):
        if f == st.session_state.tf and a == st.session_state.ta:
            st.session_state.global_cash += 1500000; st.balloons()
        else:
            st.session_state.global_cash -= 500000; st.error("불일치! 벌금 부과 및 재스캔")
        del st.session_state.tf; sync_user_data(); st.rerun()

# ==============================
# [5] CBT (무한 생성 엔진)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 모의고사 장학금")
    q_pool = [("OSI 7계층 중 3계층은?", "네트워크 계층"), ("LIFO 구조의 자료구조는?", "스택(Stack)"), ("FIFO 구조의 자료구조는?", "큐(Queue)")]
    q, a = random.choice(q_pool)
    with st.form("exam"):
        st.markdown(f"<h1 style='color:#FFD600; font-size:40px !important;'>Q. {q}</h1>", unsafe_allow_html=True)
        ans = st.radio("보기", [a, "물리 계층", "응용 계층", "세션 계층"])
        if st.form_submit_button("장학금 신청"):
            if ans == a: st.session_state.global_cash += 500000; st.success("정답! +50만")
            else: st.error("오답!")
            sync_user_data()

# ==============================
# [6] 레이싱 (역배)
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 챔피언십 역배 배팅")
    cars = [{"n":"🚗 기아 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량", "o":"배당"}))
    sel = st.selectbox("배팅 선택", [c['n'] for c in cars])
    amt = st.number_input("배팅액", min_value=10000, step=10000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*3
            while max(pos) < 100:
                for i in range(3): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel:
                m = int(amt * win['o']); st.session_state.global_cash += m; st.balloons()
            else: st.error(f"실패.. 우승: {win['n']}")
            sync_user_data()

# ==============================
# [7] 슬롯머신 (STOP 버튼)
# ==============================
elif menu == "🎰 슬롯머신":
    st.title("🎰 럭키 슬롯머신 (수동정지)")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 레버 당기기"): 
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False
        res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<div style='text-align:center; font-size:150px;'>{' '.join(res)}</div>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]:
            st.markdown("<h1 style='color:gold;'>🎊 잭팟!!! +₩10,000,000 🎊</h1>", unsafe_allow_html=True); st.session_state.global_cash += 10000000; st.balloons()
        else: st.write("꽝!"); sync_user_data()
    if st.session_state.spin:
        slot = st.empty()
        for _ in range(10):
            slot.markdown(f"<div style='text-align:center; font-size:150px;'>{[random.choice(['💎','7️⃣','🍒']) for _ in range(3)]}</div>", unsafe_allow_html=True); time.sleep(0.1)

# ==============================
# [8] 채굴기 (시각화)
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK!! (₩1,000)"):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:#FFD700; font-size:150px;'>💰 +1,000</h1>", unsafe_allow_html=True)

# ==============================
# [9] 상점 (100개 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 LUXURY 100 ITEMS SHOP")
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            st.write(f"**Luxury Item No.{i}** | ₩{i*10000000:,}")
            if f"item_{i}" in st.session_state.inventory: st.button("보유 중", key=f"i_{i}", disabled=True)
            elif st.button(f"구매하기 #{i}", key=f"i_{i}"):
                if st.session_state.global_cash >= i*10000000:
                    st.session_state.global_cash -= i*10000000; st.session_state.inventory.append(f"item_{i}"); sync_user_data(); st.rerun()

# ==============================
# [10] 게시판
# ==============================
elif menu == "💬 게시판":
    st.title("💬 자유 게시판")
    msg = st.text_input("메시지")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg}])
        st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        st.markdown(f"<div style='border-bottom:2px solid #444; padding:15px;'><b>{c['name']}</b>: {c['comment']}</div>", unsafe_allow_html=True)
