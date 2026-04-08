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
# 가독성 폭발 스타일 (초대형 폰트 & 고대비)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v7", page_icon="💰", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@500;900&display=swap');
    
    /* 전체 배경을 밝게, 글씨는 검게 (가독성 1순위) */
    .stApp { background-color: #FFFFFF !important; }
    
    html, body, [class*="css"], .stMarkdown, p, label, span, li {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #000000 !important;
        font-size: 24px !important; /* 기본 폰트 대폭 상향 */
        font-weight: 600 !important;
        line-height: 1.6 !important;
    }
    
    /* 제목 스타일 */
    h1 { font-family: 'Black Han Sans', sans-serif !important; font-size: 80px !important; color: #E91E63 !important; text-align: center; }
    h2 { font-size: 50px !important; color: #1A237E !important; border-bottom: 5px solid #1A237E; padding-bottom: 10px; }
    h3 { font-size: 35px !important; color: #2E7D32 !important; }

    /* 주식/포트폴리오 테이블 가독성 */
    table { width: 100% !important; border: 3px solid #000 !important; }
    th { background-color: #F5F5F5 !important; color: #000 !important; font-size: 26px !important; padding: 15px !important; border: 2px solid #000 !important; }
    td { font-size: 26px !important; padding: 15px !important; border: 1px solid #AAA !important; font-weight: 900 !important; text-align: center !important; }
    
    .up { color: #D32F2F !important; } /* 상승: 빨강 */
    .down { color: #1976D2 !important; } /* 하락: 파랑 */

    /* 버튼 스타일 (크고 명확하게) */
    .stButton>button {
        height: 80px !important;
        font-size: 30px !important;
        font-weight: 900 !important;
        background-color: #1A237E !important;
        color: white !important;
        border-radius: 20px !important;
        border: 4px solid #000 !important;
        margin-top: 10px;
    }
    
    /* 사이드바 글씨 조정 */
    section[data-testid="stSidebar"] * { color: white !important; font-size: 20px !important; }
    section[data-testid="stSidebar"] { background-color: #1A237E !important; }

    /* 입력칸 */
    input { font-size: 25px !important; font-weight: bold !important; border: 3px solid #000 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 초기화 및 로그인
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1>🌌 효민 유니버스</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>글씨가 안 보이신다기에 폰트를 3배 키웠습니다. 자산을 관리하세요!</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        t1, t2 = st.tabs(["로그인", "회원가입"])
        with t1:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("유니버스 접속"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_ids': set(users[l_id].get('solved_ids', []))
                    })
                    st.rerun()
                else: st.error("정보 불일치")
        with t2:
            n_id = st.text_input("아이디 생성")
            n_pw = st.text_input("비밀번호 생성", type="password")
            if st.button("가입 신청"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 있음")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "뉴비", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인 하세요.")
    st.stop()

# 랭킹 계산 함수
def get_rankings():
    users = load_db(USERS_FILE, {})
    ranks = []
    prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()}
    for uid, data in users.items():
        total = data.get('cash', 0)
        port = data.get('portfolio', {})
        for sid, p_data in port.items():
            total += p_data.get('qty', 0) * prices.get(sid, p_data.get('avg_price', 0))
        ranks.append({"id": uid, "total": total})
    ranks.sort(key=lambda x: x['total'], reverse=True)
    return ranks

# ==============================
# 주식 데이터 초기화 (KeyError 완벽 차단)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SAMSUNG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYUNDAI", "name": "현대차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GOODUS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩", "vol": 0.07}
]

if 'stock_data' not in st.session_state or len(st.session_state.stock_data) != len(stock_config):
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [100000]} for s in stock_config}
if 'last_news' not in st.session_state: st.session_state.last_news = "현재 시장은 평온합니다."
if 'news_time' not in st.session_state: st.session_state.news_time = time.time()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.header(f"👤 {st.session_state.logged_in_user}")
    st.subheader(f"[{st.session_state.equipped_title}]")
    st.metric("💰 내 현금", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): 
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("이동할 메뉴", ["🏠 홈", "📈 주식 종합 시장", "⚽ 구단주 매니저", "📡 통신 신호 동기화", "💻 CBT 모의고사", "🏎️ 레이싱 배팅", "🎰 럭키 슬롯머신", "⛏️ 코인 채굴기", "🛒 슈퍼 상점", "💬 자유게시판"])
    st.markdown("---")
    st.markdown("### 🏆 부자 랭킹")
    for i, r in enumerate(get_rankings()[:3]):
        st.write(f"{['🥇','🥈','🥉'][i]} {r['id']}: ₩{r['total']:,.0f}")

# ==============================
# 1. 홈
# ==============================
if menu == "🏠 홈":
    st.title("방문해주셔서 감사합니다! 🎉")
    st.markdown(f"**{st.session_state.logged_in_user}님**, 환영합니다. 모든 글씨를 읽기 쉽게 크게 키웠습니다.")
    st.write("왼쪽 메뉴에서 주식 투자, 축구 팀 운영, 기사 문제 풀이 등 10가지 게임을 즐기고 부자가 되어보세요.")
    st.image("https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200", caption="Hyper Asset Management")

# ==============================
# 2. 주식 시장 (내 포트폴리오 상세 추가)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 주식 종합 시장 & 내 계좌")
    
    # 30초마다 뉴스
    if time.time() - st.session_state.news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.15, 0.15)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.last_news = f"📰 [속보] {target['name']}, 혁신 기술 발표로 시장 주도!" if impact > 0 else f"📰 [속보] {target['name']}, 실적 부진으로 주가 급락!"
        st.session_state.news_time = time.time()

    st.error(f"📡 {st.session_state.last_news}")

    # 가격 변동 (10초 강제)
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])

    tab_market, tab_my = st.tabs(["📊 시장 전체 현황", "💼 내 포트폴리오 (계좌)"])
    
    with tab_market:
        rows = ""
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
            change_val = (curr['price'] - curr['history'][-2]) / curr['history'][-2] * 100
            color = "up" if change_val >= 0 else "down"
            sign = "▲" if change_val >= 0 else "▼"
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{color}'>{sign} {abs(change_val):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목명</th><th>현재가</th><th>등락</th></tr>{rows}</table>", unsafe_allow_html=True)
        
    with tab_my:
        st.subheader("내 보유 주식 상세 현황")
        my_data = []
        total_eval = 0
        for sid, p_data in st.session_state.portfolio.items():
            qty = p_data['qty']
            if qty <= 0: continue
            curr_p = st.session_state.stock_data[sid]['price']
            avg_p = p_data['avg_price']
            eval_amt = qty * curr_p
            profit_amt = eval_amt - (qty * avg_p)
            profit_pct = (curr_p - avg_p) / avg_p * 100
            total_eval += eval_amt
            my_data.append({"종목": st.session_state.stock_data[sid]['name'], "수량": qty, "평단가": f"₩{int(avg_p):,}", "현재가": f"₩{curr_p:,}", "평가금액": f"₩{eval_amt:,}", "수익률": profit_pct})

        if my_data:
            df_my = pd.DataFrame(my_data)
            def color_profit(val):
                color = 'red' if val > 0 else 'blue'
                return f'color: {color}; font-weight: bold;'
            st.table(df_my.style.applymap(color_profit, subset=['수익률']).format({"수익률": "{:.2f}%"}))
            st.markdown(f"### 💰 내 총 주식 가치: ₩{total_eval:,}")
        else: st.info("보유 중인 주식이 없습니다.")

    st.write("---")
    st.subheader("주식 매매 컨트롤러")
    col1, col2 = st.columns([1, 1])
    with col1:
        sel_name = st.selectbox("거래 종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], title=f"{sel_name} 주가 추이", template="plotly_white"), use_container_width=True)
    with col2:
        curr_price = st.session_state.stock_data[sid]['price']
        st.markdown(f"## ₩{curr_price:,}")
        amount = st.number_input("거래 수량 입력", min_value=1, value=1)
        if st.button("💥 풀매수 (ALL-IN)"):
            max_q = st.session_state.global_cash // curr_price
            if max_q > 0:
                cost = max_q * curr_price
                st.session_state.global_cash -= cost
                old = st.session_state.portfolio.get(sid, {"qty": 0, "avg_price": 0})
                new_qty = old['qty'] + max_q
                st.session_state.portfolio[sid] = {"qty": new_qty, "avg_price": curr_price}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {"qty": 0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * curr_price
                st.session_state.portfolio[sid]['qty'] = 0; sync_user_data(); st.rerun()

    time.sleep(10); st.rerun()

# ==============================
# 3. 축구 구단주 (포메이션 + 30초)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 라이브 시뮬레이션")
    f_choice = st.selectbox("포메이션을 선택하세요", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (점유율)", "5-4-1 (수비)"])
    if st.button(" Stadium 입장 (30초 경기 시작)"):
        st.markdown("---")
        board = st.empty(); bar = st.progress(0); log = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            board.markdown(f"<h1 style='font-size:120px; color:black;'>{h} : {a}</h1>", unsafe_allow_html=True)
            bar.progress((i+1)/30, text=f"매치 {i*3}분 진행 중...")
            log.warning(f"🎙️ 중계멘트: {random.choice(['우리팀 공격수가 골문을 두드리고 있습니다!', '상대팀의 역습이 날카롭습니다!', '골키퍼 정면! 위기를 넘깁니다!'])}")
            time.sleep(1)
        win_money = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += win_money; sync_user_data(); st.success(f"매치 종료! ₩{win_money:,} 수익 발생.")

# ==============================
# 4. 통신 신호 (패널티 명시)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 처리 동기화 업무")
    if 'tf' not in st.session_state: st.session_state.tf = random.randint(2, 12); st.session_state.ta = random.randint(3, 10)
    
    st.markdown("### 💰 성공 보너스: +₩1,500,000 | ❌ 실패 패널티: -₩500,000")
    f = st.slider("주파수(Frequency) 조절", 1, 15, 5); a = st.slider("진폭(Amplitude) 조절", 1, 15, 5)
    
    x = np.linspace(0, 10, 400)
    y_t = st.session_state.ta * np.sin(st.session_state.tf * x)
    y_u = a * np.sin(f * x)
    fig = px.line(pd.DataFrame({'x':x, '목표파형':y_t, '입력파형':y_u}), x='x', y=['목표파형', '입력파형'], template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("신호 동기화 승인"):
        if f == st.session_state.tf and a == st.session_state.ta:
            st.success("✅ 정확합니다! 보너스 ₩1,500,000"); st.session_state.global_cash += 1500000; del st.session_state.tf
        else:
            st.error("❌ 신호 불일치! 패널티 ₩500,000"); st.session_state.global_cash -= 500000; del st.session_state.tf
        sync_user_data(); st.rerun()

# ==============================
# 5. CBT 모의고사 (글씨 킹사이즈)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 모의고사 장학금")
    if 'exam' not in st.session_state:
        st.session_state.exam = [{"q":"LIFO(Last In First Out) 구조의 자료구조는 무엇인가?", "a":"스택(Stack)", "opts":["스택(Stack)", "큐(Queue)", "트리(Tree)", "그래프(Graph)"]}]

    with st.form("exam_huge"):
        for i, q in enumerate(st.session_state.exam):
            st.markdown(f"<h1 style='color:blue; font-size:40px !important;'>Q. {q['q']}</h1>", unsafe_allow_html=True)
            ans = st.radio("정답을 선택하세요", q['opts'], key=f"ans_{i}")
        if st.form_submit_button("장학금 받기"):
            if ans == q['a']:
                st.success("🎉 정답! ₩1,000,000 획득!"); st.session_state.global_cash += 1000000
            else: st.error("❌ 틀렸습니다!")
            sync_user_data()

# ==============================
# 6. 레이싱 배팅 (역배)
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 챔피언십 배팅 (역배의 기회)")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚙 람보 (2배)", "o":2.0}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량명(배당률)", "o":"배당수치"}))
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("배팅 금액 입력", min_value=10000, step=10000)
    if st.button("🚥 RACE START!"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*4
            while max(pos) < 100:
                for i in range(4): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel:
                money = int(amt * win['o']); st.success(f"🎊 예측 적중! ₩{money:,} 획득!"); st.session_state.global_cash += money
            else: st.error(f"실패.. 우승차: {win['n']}")
            sync_user_data()

# ==============================
# 7. 슬롯머신 (멈춤 버튼)
# ==============================
elif menu == "🎰 럭키 슬롯머신":
    st.title("🎰 럭키 슬롯")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 레버 당기기 (₩100,000)"):
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False
        res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<h1 style='font-size:150px; text-align:center;'>{res}</h1>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]:
            st.balloons(); st.success("🎊 잭팟!!! +₩10,000,000"); st.session_state.global_cash += 10000000
        else: st.write("꽝!"); sync_user_data()
    if st.session_state.spin:
        area = st.empty()
        for _ in range(15):
            area.markdown(f"<h1 style='font-size:150px; text-align:center;'>{[random.choice(['💎','7️⃣','🍒']) for _ in range(3)]}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)

# ==============================
# 8. 채굴기 (시각화)
# ==============================
elif menu == "⛏️ 코인 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 클릭하여 ₩1,000 채굴!"):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:orange;'>💰 ₩1,000</h1>", unsafe_allow_html=True)

# ==============================
# 9. 상점 (100개 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 100 ITEMS LUXURY SHOP")
    items = []
    for i in range(1, 101): items.append({"id":f"item_{i}", "n":f"Luxury Goods No.{i}", "p":i*10000000})
    
    col_i = 0
    cols = st.columns(2) # 폰트가 크므로 2열로 배치
    for it in items:
        with cols[col_i % 2]:
            st.markdown(f"### {it['n']}")
            st.write(f"가격: ₩{it['p']:,}")
            if it['id'] in st.session_state.inventory: st.button("보유 중", key=it['id'], disabled=True)
            elif st.button(f"구매하기", key=it['id']):
                if st.session_state.global_cash >= it['p']:
                    st.session_state.global_cash -= it['p']; st.session_state.inventory.append(it['id'])
                    sync_user_data(); st.rerun()
        col_i += 1

# ==============================
# 10. 자유게시판
# ==============================
elif menu == "💬 자유게시판":
    st.title("💬 유저 게시판")
    msg = st.text_input("메시지 입력")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])): st.markdown(f"**{c['name']}**: {c['comment']}")
