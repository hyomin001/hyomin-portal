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
# 시스템 및 DB 설정
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
    prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()} if 'stock_data' in st.session_state else {}
    for uid, data in users.items():
        wealth = data.get('cash', 0)
        for sid, p_data in data.get('portfolio', {}).items():
            if sid in prices: wealth += p_data.get('qty', 0) * prices[sid]
        rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# 🎨 가독성 끝판왕 CSS
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    .stApp { background-color: #050505 !important; }
    html, body, [class*="css"], .stMarkdown, p, span, li, label {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important; font-size: 22px !important; font-weight: 700 !important;
    }

    /* 선택창(Selectbox) 및 입력창 가독성 강제 고정 */
    div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 22px !important; font-weight: 900 !important; }
    div[data-baseweb="popover"] * { background-color: #1A1C24 !important; color: #00FF88 !important; font-size: 20px !important; }
    .stNumberInput input { background-color: #222 !important; color: #00FF88 !important; font-size: 24px !important; }

    /* 사이드바 */
    [data-testid="stSidebar"] { background-color: #001F3F !important; border-right: 3px solid #00E5FF; }
    div[data-testid="stSidebarNav"] span, .stRadio label p { color: #FFD600 !important; font-size: 24px !important; }

    /* 주식 테이블 */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 3px solid #444; }
    .stock-table th { background-color: #333; color: #FFD600 !important; font-size: 26px !important; padding: 15px; }
    .stock-table td { font-size: 24px !important; padding: 15px; border-bottom: 1px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }

    /* 제목 및 버튼 */
    h1 { font-size: 4rem !important; color: #00E5FF !important; font-weight: 900 !important; text-align: center; }
    h2 { font-size: 2.8rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }
    .stButton>button { height: 70px !important; border: 4px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; font-size: 26px !important; font-weight: 900 !important; border-radius: 15px; }
    .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
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
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'], 'inventory': users[l_id]['inventory'],
                        'equipped_title': users[l_id]['equipped_title'], 'portfolio': users[l_id].get('portfolio', {})
                    }); st.rerun()
                else: st.error("정보 불일치")
        with choice[1]:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인하세요.")
    st.stop()

# ==============================
# 📈 주식 데이터 엔진 (KeyError 방어)
# ==============================
stock_config = [
    {"id": "S1", "name": "삼지전자", "vol": 0.05}, {"id": "S2", "name": "삼성전자", "vol": 0.02},
    {"id": "S3", "name": "현대자동차", "vol": 0.025}, {"id": "S4", "name": "네이버", "vol": 0.03},
    {"id": "S5", "name": "가온브로드", "vol": 0.06}, {"id": "S6", "name": "HFR", "vol": 0.05},
    {"id": "S7", "name": "굿어스데이터", "vol": 0.04}, {"id": "S8", "name": "레이자동차", "vol": 0.03},
    {"id": "S9", "name": "도지코인", "vol": 0.15}, {"id": "S10", "name": "VHDL칩셋", "vol": 0.07}
]
c_keys = set([s['id'] for s in stock_config])
if 'stock_data' not in st.session_state or set(st.session_state.stock_data.keys()) != c_keys:
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [80000]} for s in stock_config}
if 'news' not in st.session_state: st.session_state.news = "시장이 개장되었습니다."
if 'news_time' not in st.session_state: st.session_state.news_time = time.time()
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.logged_in_user}님")
    st.metric("💰 보유 자산", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("이동", ["🏠 홈", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 업무", "💻 CBT", "🏎️ 레이싱", "🎰 슬롯", "⛏️ 채굴기", "🛒 상점", "💬 게시판"])
    st.markdown("### 🏆 부자 랭킹")
    for i, r in enumerate(get_rankings()[:3]): st.write(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")

# ==============================
# [1] 홈
# ==============================
if menu == "🏠 홈":
    st.title(f"환영합니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("효민 유니버스에 오신 것을 환영합니다. 모든 진행 상황은 자동으로 저장됩니다.")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")

# ==============================
# [2] 주식 (10초 자동 갱신 + 포트폴리오)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 실시간 통합 거래소")
    
    # 30초 뉴스
    if time.time() - st.session_state.news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.15, 0.15)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.news = f"📰 [속보] {target['name']}, 혁신 기술 발표!" if impact > 0 else f"📰 [속보] {target['name']}, 악재 발생!"
        st.session_state.news_time = time.time()
    st.warning(f"**{st.session_state.news}**")

    # 10초 주가 변동 (Time-Lock)
    if time.time() - st.session_state.last_tick > 10:
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
            change = (random.random()-0.5) * 2 * s['vol']
            curr['price'] = round(max(1000, curr['price'] * (1 + change)))
            curr['history'].append(curr['price'])
            if len(curr['history']) > 30: curr['history'].pop(0)
        st.session_state.last_tick = time.time()

    t_mkt, t_acc = st.tabs(["📊 실시간 시황", "💼 내 포트폴리오"])
    
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
                p_list.append({"종목": st.session_state.stock_data[sid]['name'], "수량": f"{qty}주", "평단가": f"₩{int(ap):,}", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("보유 주식이 없습니다.")
        st.markdown(f"### 💰 주식자산: ₩{total_eval:,} | 💵 가용현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    c1, c2 = st.columns([1.2, 1])
    with c1:
        sel_name = st.selectbox("거래할 종목 선택", [s['name'] for s in stock_config])
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
                new_a = ((old['qty'] * old['avg_price']) + (max_q * curr_p)) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * curr_p
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data(); st.rerun()
    time.sleep(5); st.rerun()

# ==============================
# [3] 구단주 (30초 시뮬레이션 + 해설 복구)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    form = st.selectbox("포메이션", ["4-4-2", "4-3-3", "3-5-2", "5-4-1"])
    if st.button("🏟️ 경기 시작 (30초)"):
        b = st.empty(); p = st.progress(0); l = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            b.markdown(f"<div style='text-align:center; background:#000; border:5px solid #00FF88; padding:30px; border-radius:30px;'><h1 style='font-size:100px; color:#FFF;'>{h} : {a}</h1></div>", unsafe_allow_html=True)
            p.progress((i+1)/30)
            # 해설 추가됨!
            l.info(f"🎙️ **중계:** {random.choice(['우리팀 공격수의 엄청난 돌파!', '상대 수비수의 태클!', '골키퍼의 슈퍼 세이브!', '치열한 중원 싸움!', '관중들의 함성이 쏟아집니다!'])}")
            time.sleep(1)
        res = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += res; sync_user_data(); st.success(f"정산: +₩{res:,}")

# ==============================
# [4] 통신 업무
# ==============================
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

# ==============================
# [5] CBT (글씨 시인성 강화)
# ==============================
elif menu == "💻 CBT":
    st.title("💻 정처기 장학금 모의고사")
    q_pool = [("OSI 7계층 중 3계층은?", "네트워크 계층"), ("LIFO 구조는?", "스택"), ("FIFO 구조는?", "큐")]
    q, ans_val = random.choice(q_pool)
    with st.form("exam"):
        st.markdown(f"<h1 style='color:#FFD600;'>Q. {q}</h1>", unsafe_allow_html=True)
        ans = st.radio("정답 선택", [ans_val, "물리 계층", "응용 계층", "세션 계층"])
        if st.form_submit_button("제출"):
            if ans == ans_val: st.session_state.global_cash += 500000; st.success("정답! +50만")
            else: st.error("오답!"); 
            sync_user_data()

# ==============================
# [6] 레이싱 (역배 시스템)
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 역배 챔피언십 배팅")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량", "o":"배당"}))
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("금액", min_value=10000, step=10000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt; bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*3
            while max(pos) < 100:
                for i in range(3): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel: st.session_state.global_cash += int(amt * win['o']); st.success("승리!"); st.balloons()
            else: st.error(f"우승차: {win['n']}"); sync_user_data()

# ==============================
# [7] 슬롯머신 (수동정지)
# ==============================
elif menu == "🎰 슬롯":
    st.title("🎰 슬롯머신 (수동정지)")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 레버 당기기"): 
        if st.session_state.global_cash >= 100000: st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False; res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<div style='text-align:center; font-size:150px;'>{' '.join(res)}</div>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]: st.session_state.global_cash += 10000000; st.balloons()
        sync_user_data()
    if st.session_state.spin:
        slot = st.empty()
        for _ in range(10): slot.markdown(f"<div style='text-align:center; font-size:150px;'>{[random.choice(['💎','7️⃣','🍒']) for _ in range(3)]}</div>", unsafe_allow_html=True); time.sleep(0.1)

# ==============================
# [8] 채굴기
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK!! (₩1,000)"):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:gold; font-size:150px;'>💰 +1,000</h1>", unsafe_allow_html=True)

# ==============================
# [9] 상점 (100개 루프)
# ==============================
elif menu == "🛒 상점":
    st.title("🛒 LUXURY 100 ITEMS")
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            st.write(f"**Item No.{i}** | ₩{i*10000000:,}")
            if f"item_{i}" in st.session_state.inventory: st.button("보유 중", key=f"item_{i}", disabled=True)
            elif st.button(f"구매 #{i}", key=f"item_{i}"):
                if st.session_state.global_cash >= i*10000000:
                    st.session_state.global_cash -= i*10000000; st.session_state.inventory.append(f"item_{i}"); sync_user_data(); st.rerun()

# ==============================
# [10] 게시판
# ==============================
elif menu == "💬 게시판":
    st.title("💬 자유 게시판")
    msg = st.text_input("메시지 입력")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        st.markdown(f"<div style='border-bottom:2px solid #444; padding:15px;'><b>{c['name']}</b>: {c['comment']}</div>", unsafe_allow_html=True)
