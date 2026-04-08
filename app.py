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

# 랭킹 계산
def get_user_rankings():
    users = load_db(USERS_FILE, {})
    rankings = []
    prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()}
    for uid, data in users.items():
        wealth = data.get('cash', 0)
        portfolio = data.get('portfolio', {})
        for sid, p_data in portfolio.items():
            wealth += p_data.get('qty', 0) * prices.get(sid, p_data.get('avg_price', 0))
        rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# 폰트 가독성 및 디자인 (강제 고대비 설정)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v6", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    
    /* 배경 및 기본 텍스트 설정 */
    .stApp { background-color: #0E1117 !important; }
    html, body, [class*="css"], .stMarkdown, p, label, span {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 22px !important;
        font-weight: 500 !important;
    }
    
    /* 헤더 */
    h1 { font-size: 4rem !important; color: #00D4FF !important; font-weight: 900 !important; }
    h2 { font-size: 2.5rem !important; color: #00FF88 !important; }
    h3 { font-size: 1.8rem !important; color: #FFAA00 !important; }

    /* 주식 테이블 가독성 극대화 */
    .stock-table { width: 100%; border-collapse: collapse; background-color: #1A1C24; border: 2px solid #444; }
    .stock-table th, .stock-table td { padding: 25px !important; font-size: 26px !important; border: 1px solid #444; text-align: center; }
    .price-up { color: #FF4B4B !important; font-weight: bold; }
    .price-down { color: #1F77B4 !important; font-weight: bold; }

    /* 버튼 가시성 */
    .stButton>button {
        border: 3px solid #00D4FF !important;
        background-color: #1A1C24 !important;
        color: #00D4FF !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 12px;
        padding: 10px 20px;
    }
    .stButton>button:hover { background-color: #00D4FF !important; color: #000000 !important; }

    /* 입력창 글씨 색상 고정 */
    input { color: black !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 화면
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; font-size: 28px;'>방문해주셔서 감사합니다. 자산을 증식하여 경쟁하세요!</div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        tab_log = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tab_log[0]:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_ids': set(users[l_id].get('solved_ids', []))
                    })
                    st.rerun()
                else: st.error("로그인 정보가 틀렸습니다.")
        with tab_log[1]:
            n_id = st.text_input("새 아이디")
            n_pw = st.text_input("새 비밀번호", type="password")
            if st.button("가입 신청"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 사용 중인 아이디입니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인해 주세요.")
    st.stop()

# ==============================
# 데이터 초기화 (KeyError 방지)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SMSUNG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDAI", "name": "현대차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GDS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩", "vol": 0.07}
]

if 'stock_data' not in st.session_state or len(st.session_state.stock_data) != len(stock_config):
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(30000, 150000), "history": [80000]} for s in stock_config}
if 'news' not in st.session_state: st.session_state.news = "시장 상황 안정적입니다."
if 'last_news_time' not in st.session_state: st.session_state.last_news_time = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.title("MENU")
    st.subheader(f"👤 {st.session_state.logged_in_user}")
    st.metric("자산", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): 
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 이동", ["🏠 홈", "📈 주식 종합 시장", "⚽ 구단주 매니저", "📡 통신 신호 동기화", "💻 CBT 모의고사", "🏎️ 레이싱 배팅", "🎰 럭키 슬롯머신", "⛏️ 코인 채굴기", "🛒 슈퍼 상점", "💬 자유게시판"])
    
    st.markdown("---")
    st.markdown("### 🏆 부자 랭킹 (TOP 3)")
    for i, r in enumerate(get_user_rankings()[:3]):
        st.markdown(f"{['🥇','🥈','🥉'][i]} **{r['uid']}**: ₩{r['total']:,.0f}")

# ==============================
# 1. 홈
# ==============================
if menu == "🏠 홈":
    st.title("🌠 효민 유니버스 포털")
    st.markdown("방문해주셔서 감사합니다. 이곳은 다양한 게임을 즐기고 자산을 불리는 가상 세계입니다.")
    st.write("---")
    st.markdown("""
    ### 🎮 게임 안내
    1. **📈 주식 시장**: 실시간 뉴스 분석을 통해 10개 종목에 투자하세요. (10초 자동 갱신)
    2. **⚽ 구단주**: 포메이션을 전략적으로 짜고 30초간의 라이브 경기를 시청하세요.
    3. **📡 통신 업무**: 파형을 동기화하여 보너스를 받으세요. (실패 시 차감 주의!)
    4. **💻 CBT**: 기사 문제를 풀고 장학금을 획득하세요.
    """)

# ==============================
# 2. 주식 (10초 자동 갱신 + 뉴스)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 주식 종합 시장")
    
    # 30초마다 뉴스 발생
    if time.time() - st.session_state.last_news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.2, 0.2)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.news = f"📰 [속보] {target['name']}, {'기대 이상의 실적 발표!' if impact > 0 else '공급망 차질로 인한 위기!'}"
        st.session_state.last_news_time = time.time()

    st.warning(st.session_state.news)

    rows_html = ""
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        color, sign = ("price-up", "▲") if change >= 0 else ("price-down", "▼")
        rows_html += f"<tr><td>{s['name']}</td><td style='text-align:right;'>₩{curr['price']:,}</td><td class='{color}' style='text-align:right;'>{sign} {abs(change*100):.2f}%</td></tr>"

    c1, c2 = st.columns([1.5, 1])
    with c1:
        st.markdown(f"<table class='stock-table'>{rows_html}</table>", unsafe_allow_html=True)
    with c2:
        sel_name = st.selectbox("거래할 종목", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=300), use_container_width=True)
        q = st.number_input("수량", min_value=1, value=1)
        if st.button("💥 풀매수 (ALL-IN)"):
            price = st.session_state.stock_data[sid]['price']
            max_q = st.session_state.global_cash // price
            if max_q > 0:
                st.session_state.global_cash -= max_q * price
                st.session_state.portfolio[sid] = {"qty": st.session_state.portfolio.get(sid, {'qty':0})['qty'] + max_q, "avg_price": price}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid]['qty'] = 0; sync_user_data(); st.rerun()
    time.sleep(10); st.rerun()

# ==============================
# 3. 구단주 매니저 (포메이션 + 30초)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    f_choice = st.selectbox("경기 전 포메이션 선택", ["4-4-2 (기본)", "4-3-3 (공공격)", "3-5-2 (점유율)", "5-4-1 (수비)"])
    if st.button("Stadium 입장 (30초 경기 시작)"):
        st.markdown("---")
        board = st.empty(); bar = st.progress(0); log = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            board.markdown(f"<h1 style='text-align:center; font-size:80px;'>HOME {h} : {a} AWAY</h1>", unsafe_allow_html=True)
            bar.progress((i+1)/30, text=f"매치 진행 중... ({i*3}분)")
            log.info(f"🎙️ 중계: {random.choice(['우리팀 공격수의 환상적인 드리블!', '아! 상대팀의 거친 태클!', '골키퍼 정면입니다!'])}")
            time.sleep(1)
        win_money = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += win_money; sync_user_data(); st.success(f"매치 종료! ₩{win_money:,} 정산 완료.")

# ==============================
# 4. 통신 신호 (금액 명시)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 처리 동기화 업무")
    if 't_f' not in st.session_state: st.session_state.t_f = random.randint(2, 12); st.session_state.t_a = random.randint(3, 10)
    
    st.markdown("### 💰 성공 시: +₩1,500,000 | ❌ 실패 시: -₩500,000")
    f = st.slider("주파수 조절", 1, 15, 5); a = st.slider("진폭 조절", 1, 15, 5)
    
    x = np.linspace(0, 10, 300)
    y_t = st.session_state.t_a * np.sin(st.session_state.t_f * x)
    y_u = a * np.sin(f * x)
    fig = px.line(pd.DataFrame({'x':x, 'Target':y_t, 'Input':y_u}), x='x', y=['Target', 'Input'], template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("신호 동기화 승인"):
        if f == st.session_state.t_f and a == st.session_state.t_a:
            st.success("✅ 완벽하게 일치합니다! +₩1,500,000")
            st.session_state.global_cash += 1500000; del st.session_state.t_f
        else:
            st.error("❌ 신호 불일치! 업무 패널티 발생: -₩500,000")
            st.session_state.global_cash -= 500000; del st.session_state.t_f
        sync_user_data(); st.rerun()

# ==============================
# 5. CBT (글씨 크게)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 모의고사 장학금")
    if 'cbt_q' not in st.session_state:
        st.session_state.cbt_q = [{"q":"LIFO 구조의 자료구조는?", "a":"스택", "opts":["스택", "큐", "트리", "그래프"]}]

    with st.form("big_cbt"):
        for i, q in enumerate(st.session_state.cbt_q):
            st.markdown(f"<h2 style='color:yellow;'>Q. {q['q']}</h2>", unsafe_allow_html=True)
            ans = st.radio("정답 선택", q['opts'], key=f"ans_{i}")
        if st.form_submit_button("장학금 신청"):
            if ans == q['a']:
                st.balloons(); st.success("정답! +₩500,000"); st.session_state.global_cash += 500000
            else: st.error("오답입니다.")
            sync_user_data()

# ==============================
# 6. 레이싱 (역배 시스템)
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 챔피언십 배팅")
    cars = [{"n":"🚗 레이", "o":15.0, "p":"5%"}, {"n":"🏎️ 페라리", "o":1.5, "p":"45%"}, {"n":"🚙 람보", "o":2.2, "p":"30%"}, {"n":"🚜 트랙터", "o":30.0, "p":"2%"}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량", "o":"배당", "p":"우승확률"}))
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("금액", min_value=10000, step=10000)
    if st.button("RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*4
            while max(pos) < 100:
                for i in range(4): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel:
                st.success(f"축하합니다! ₩{int(amt * win['o']):,} 획득!"); st.session_state.global_cash += int(amt * win['o'])
            else: st.error(f"실패.. 우승차는 {win['n']}입니다.")
            sync_user_data()

# ==============================
# 7. 슬롯머신 (수동 정지)
# ==============================
elif menu == "🎰 럭키 슬롯머신":
    st.title("🎰 슬롯머신")
    if 'spin' not in st.session_state: st.session_state.spin = False
    col1, col2 = st.columns(2)
    if col1.button("🕹️ 당기기 (₩100,000)"):
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if col2.button("⏹️ STOP!"):
        st.session_state.spin = False
        res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<h1 style='text-align:center; font-size:100px;'>{res}</h1>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]:
            st.balloons(); st.success("🎊 CONGRATS! +₩10,000,000"); st.session_state.global_cash += 10000000
        else: st.info("꽝!")
        sync_user_data()
    if st.session_state.spin:
        area = st.empty()
        for _ in range(15):
            area.markdown(f"<h1 style='text-align:center; font-size:100px;'>{[random.choice(['💎', '7️⃣', '🍒']) for _ in range(3)]}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)

# ==============================
# 8. 채굴기 (시각화)
# ==============================
elif menu == "⛏️ 코인 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK (₩1,000)", use_container_width=True):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown(f"<h1 style='text-align:center; color:yellow;'>💰 +₩1,000</h1>", unsafe_allow_html=True)

# ==============================
# 9. 상점 (100개 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 100 ITEMS LUXURY SHOP")
    items = []
    # Programmatic Generation of 100 items
    for i in range(1, 101):
        items.append({"id":f"item_{i}", "n":f"Luxury Item #{i}", "p":i*5000000})
    
    col_i = 0
    cols = st.columns(3)
    for it in items:
        with cols[col_i % 3]:
            st.write(f"**{it['n']}**")
            st.write(f"가격: ₩{it['p']:,}")
            if it['id'] in st.session_state.inventory: st.button("보유 중", key=it['id'], disabled=True)
            elif st.button(f"구매 #{it['id']}", key=it['id']):
                if st.session_state.global_cash >= it['p']:
                    st.session_state.global_cash -= it['p']; st.session_state.inventory.append(it['id'])
                    sync_user_data(); st.rerun()
        col_i += 1

# ==============================
# 10. 자유게시판
# ==============================
elif menu == "💬 자유게시판":
    st.title("💬 유저 게시판")
    msg = st.text_input("한 줄 입력")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg, "time":datetime.now().strftime("%H:%M")}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])): st.info(f"**{c['name']}**: {c['comment']}")
