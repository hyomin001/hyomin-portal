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
# 데이터베이스 & 세션 시스템
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

def get_user_rankings():
    users = load_db(USERS_FILE, {})
    rankings = []
    for uid, data in users.items():
        total_wealth = data.get('cash', 0)
        portfolio_val = 0
        portfolio = data.get('portfolio', {})
        prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()}
        for sid, p_data in portfolio.items():
            qty = p_data.get('qty', 0)
            if qty > 0:
                portfolio_val += qty * prices.get(sid, p_data.get('avg_price', 0))
        rankings.append({"uid": uid, "total": total_wealth + portfolio_val})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# 커스텀 폰트 및 스타일 (가독성 극대화)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v6", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Noto Sans KR', sans-serif; 
        color: #ffffff; 
        font-size: 18px; 
    }
    .stApp { background-color: #050510; }
    
    /* 전체적인 글씨 크기 고도화 */
    h1 { font-size: 3.5rem !important; color: #00d4ff !important; font-weight: 800 !important; }
    h2 { font-size: 2.2rem !important; color: #00ff88 !important; }
    h3 { font-size: 1.8rem !important; }
    p, span, label, .stMarkdown { font-size: 20px !important; }

    /* 주식 시장 가독성 */
    .stock-table td, .stock-table th { font-size: 22px !important; padding: 20px !important; border-bottom: 1px solid #333; }
    .price-up { color: #00ff88; font-weight: bold; }
    .price-down { color: #ff4444; font-weight: bold; }

    /* 버튼 스타일 */
    .stButton>button { 
        border: 2px solid #00d4ff; 
        color: #00d4ff; 
        background: rgba(0,212,255,0.1); 
        font-size: 22px !important; 
        padding: 10px 25px !important;
        border-radius: 12px;
        font-weight: bold;
    }
    div[data-testid="stBlock"] { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 25px; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 화면
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 24px;'>성공적인 자산 관리를 위한 멀티 게이밍 포털</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tab1:
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("로그인", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({'logged_in_user': l_id, 'global_cash': users[l_id]['cash'], 'inventory': users[l_id]['inventory'], 
                                             'equipped_title': users[l_id]['equipped_title'], 'portfolio': users[l_id].get('portfolio', {}),
                                             'solved_ids': set(users[l_id].get('solved_ids', []))})
                    st.rerun()
                else: st.error("정보가 틀렸습니다.")
        with tab2:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("가입완료", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 있는 아이디")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인 하세요.")
    st.stop()

# ==============================
# 사이드바 & 랭킹
# ==============================
with st.sidebar:
    st.title("UNIVERSE")
    st.subheader(f"👤 {st.session_state.logged_in_user}")
    st.metric("My Cash", f"₩{st.session_state.global_cash:,}")
    if st.button("LOGOUT"):
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 메뉴", ["🏠 홈 (안내데스크)", "📈 주식 종합 시장", "⚽ 구단주 매니저", "📡 통신 신호 동기화", "💻 CBT 모의고사", "🏎️ 레이싱 배팅", "🎰 럭키 슬롯머신", "⛏️ 코인 채굴기", "🛒 슈퍼 상점", "💬 자유게시판"])
    
    st.markdown("---")
    st.markdown("### 🏆 실시간 부자 랭킹")
    for i, r in enumerate(get_user_rankings()[:3]):
        st.markdown(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")

# ==============================
# [1] 홈 - 안내데스크
# ==============================
if menu == "🏠 홈 (안내데스크)":
    st.title("방문해주셔서 감사합니다! 🎉")
    st.markdown(f"**{st.session_state.logged_in_user}님**, 효민 유니버스 포털에 오신 것을 환영합니다.")
    st.write("본 포털은 다양한 시뮬레이션과 미니게임을 통해 자산을 증식하고 경쟁하는 공간입니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎮 게임 가이드
        - **📈 주식 시장**: 10개 종목의 실시간 변동과 뉴스를 분석하여 투자하세요.
        - **⚽ 구단주**: 포메이션을 직접 짜고 30초간의 경기 중계를 시청하세요.
        - **📡 통신 신호**: 실제 파형을 동기화하여 업무 보너스를 받으세요. (실패 시 패널티!)
        - **💻 CBT**: 정처기 핵심 문제를 풀고 장학금을 받으세요.
        """)
    with col2:
        st.markdown("""
        ### 🚀 최근 업데이트
        - 주식 종목 10개로 확장 및 30초 뉴스 시스템 도입
        - 슬롯머신 수동 정지 기능 추가
        - 상점 아이템 100종 대규모 입고
        - 레이싱 배팅 역배 배당 시스템 적용
        """)
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200", caption="Hyper Connected Hyomin Universe")

# ==============================
# [2] 주식 종합 시장 (10개 종목 + 30초 뉴스)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 주식 종합 시장")
    
    stock_config = [
        {"id": "SAMJI", "name": "삼지전자", "vol": 0.05, "trend": 1.01},
        {"id": "SAMSUNG", "name": "삼성전자", "vol": 0.02, "trend": 1.0},
        {"id": "HYUNDAI", "name": "현대차", "vol": 0.025, "trend": 1.0},
        {"id": "NAVER", "name": "네이버", "vol": 0.03, "trend": 1.0},
        {"id": "KAON", "name": "가온브로드밴드", "vol": 0.06, "trend": 1.02},
        {"id": "HFR", "name": "HFR", "vol": 0.05, "trend": 1.0},
        {"id": "GOODUS", "name": "굿어스데이터", "vol": 0.04, "trend": 1.0},
        {"id": "RAY", "name": "레이자동차(Auto)", "vol": 0.03, "trend": 1.0},
        {"id": "CRYPTO", "name": "도지코인", "vol": 0.15, "trend": 0.99},
        {"id": "VHDL", "name": "VHDL 칩셋", "vol": 0.07, "trend": 1.05}
    ]

    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(30000, 150000), "history": [80000]} for s in stock_config}
    if 'news_impact' not in st.session_state: st.session_state.news_impact = {s['id']: 0 for s in stock_config}
    if 'last_news_time' not in st.session_state: st.session_state.last_news_time = time.time()
    if 'current_news' not in st.session_state: st.session_state.current_news = "시장 대기 중..."

    # 30초마다 뉴스 갱신
    if time.time() - st.session_state.last_news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.15, 0.15)
        st.session_state.news_impact[target['id']] = impact
        st.session_state.current_news = f"📰 [속보] {target['name']}, {'어닝 서프라이즈!' if impact > 0 else '예상치 못한 실적 부진!'}"
        st.session_state.last_news_time = time.time()

    # 가격 변동 (10초 강제 갱신)
    rows_html = ""
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        news_imp = st.session_state.news_impact[s['id']]
        change = (random.random()-0.5) * 2 * s['vol'] + (news_imp * 0.5)
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        st.session_state.news_impact[s['id']] *= 0.7 # 뉴스 영향 점차 감소
        
        color, sign = ("price-up", "▲") if change >= 0 else ("price-down", "▼")
        rows_html += f"<tr><td>{s['name']}</td><td style='text-align:right;'>₩{curr['price']:,}</td><td class='{color}' style='text-align:right;'>{sign} {abs(change*100):.2f}%</td></tr>"

    st.warning(st.session_state.current_news)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown(f"<table class='stock-table' style='width:100%'><tr><th>종목</th><th>가격</th><th>등락</th></tr>{rows_html}</table>", unsafe_allow_html=True)
    with col2:
        st.subheader("계좌 제어")
        sel = st.selectbox("종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=250), use_container_width=True)
        qty = st.number_input("수량", min_value=1, value=1)
        if st.button("💥 풀매수 (ALL IN)"):
            max_q = st.session_state.global_cash // st.session_state.stock_data[sid]['price']
            if max_q > 0:
                st.session_state.global_cash -= max_q * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid] = {"qty": st.session_state.portfolio.get(sid, {'qty':0})['qty'] + max_q, "avg_price": st.session_state.stock_data[sid]['price']}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid]['qty'] = 0; sync_user_data(); st.rerun()
    
    time.sleep(10); st.rerun()

# ==============================
# [3] 구단주 매니저 (포메이션 선택 추가)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이션")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("전술 지시")
        form = st.selectbox("포메이션 선택", ["4-4-2 (기본)", "4-3-3 (공격)", "3-5-2 (중원장악)", "5-3-2 (역습)"])
        strategy = st.radio("팀 전술", ["점유율 축구", "롱볼 축구", "게겐프레싱"])
        
        if st.button(" Stadium 입장 (30초 경기)", use_container_width=True):
            st.markdown("---")
            score_txt = st.empty(); live_bar = st.progress(0); log = st.empty()
            h, a = 0, 0
            for i in range(30):
                boost = 1.2 if "4-3-3" in form else 1.0
                if random.random() < 0.08 * boost: h += 1
                if random.random() < 0.05: a += 1
                score_txt.markdown(f"<h1 style='text-align:center; font-size:70px;'>HOME {h} : {a} AWAY</h1>", unsafe_allow_html=True)
                live_bar.progress((i+1)/30, text=f"매치 진행 중... ({i*3}분)")
                events = ["중원에서 공방전!", "골포스트를 맞춥니다!", "환상적인 티키타카!", "골키퍼 정면!"]
                log.info(f"🎙️ 중계: {random.choice(events)}")
                time.sleep(1)
            
            res = 5000000 if h > a else 1000000 if h == a else 100000
            st.session_state.global_cash += res; sync_user_data(); st.success(f"매치 종료! 상금 ₩{res:,} 정산 완료.")

# ==============================
# [4] 통신 신호 (패널티 강화)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 처리 업무 (보너스/패널티)")
    if 't_freq' not in st.session_state: 
        st.session_state.t_freq = random.randint(2, 12); st.session_state.t_amp = random.randint(3, 10)
    
    st.subheader("수신된 신호를 목표 파형과 일치시키세요. 실패 시 업무 지연 패널티가 부과됩니다.")
    f = st.slider("주파수(Frequency) 조정", 1, 15, 5); a = st.slider("진폭(Amplitude) 조정", 1, 15, 5)
    
    x = np.linspace(0, 10, 300)
    y_t = st.session_state.t_amp * np.sin(st.session_state.t_freq * x)
    y_u = a * np.sin(f * x)
    
    fig = px.line(pd.DataFrame({'x':x, 'Target':y_t, 'Input':y_u}), x='x', y=['Target', 'Input'], 
                  template='plotly_dark', color_discrete_map={'Target':'#00ff88', 'Input':'#00d4ff'})
    st.plotly_chart(fig, use_container_width=True)
    
    if st.button("신호 동기화 승인"):
        if f == st.session_state.t_freq and a == st.session_state.t_amp:
            st.balloons(); st.success("성공! 보너스 ₩1,500,000 획득!"); st.session_state.global_cash += 1500000
            del st.session_state.t_freq
        else:
            st.error("불일치! 업무 패널티 ₩500,000 차감 및 신호 재스캔."); st.session_state.global_cash -= 500000
            del st.session_state.t_freq # 새로운 파형 생성 유도
        sync_user_data(); st.rerun()

# ==============================
# [5] CBT 모의고사 (가독성 강화)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정보처리기사 모의고사 (공부하고 돈벌기)")
    st.markdown("<p style='font-size: 26px; color: #ffaa00;'>글씨를 크게 수정했습니다. 정답을 맞혀 장학금을 받으세요!</p>", unsafe_allow_html=True)
    
    # 문제 생성 엔진 (핵심 개념 기반)
    concepts = [("OSI 3계층", "네트워크 계층"), ("기본키 무결성", "개체 무결성"), ("LIFO", "스택"), ("FIFO", "큐"), ("삭제 SQL", "DROP")]
    if 'cbt_exam' not in st.session_state:
        selected = random.sample(concepts, 5)
        st.session_state.cbt_exam = [{"id":hash(q), "q":f"{q}에 해당하는 용어는?", "a":a, "opts":random.sample([a, "응용 계층", "세션 계층", "트리"], 4)} for q,a in selected]

    with st.form("exam_large"):
        ans = {}
        for i, q in enumerate(st.session_state.cbt_exam):
            st.markdown(f"<div style='font-size: 30px; font-weight: bold; margin-bottom: 10px;'>Q{i+1}. {q['q']}</div>", unsafe_allow_html=True)
            ans[i] = st.radio("선택지", q['opts'], key=f"ans_{i}", label_visibility="collapsed")
            st.write("---")
        if st.form_submit_button("채점 제출"):
            reward = sum(200000 for i, q in enumerate(st.session_state.cbt_exam) if ans[i] == q['a'])
            st.session_state.global_cash += reward; sync_user_data(); st.success(f"정산 완료: +₩{reward:,}")
    if st.button("🔄 새로운 문제 생성"): del st.session_state.cbt_exam; st.rerun()

# ==============================
# [6] 레이싱 배팅 (승률/역배 적용)
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 레이싱 챔피언십 (역배 시스템)")
    
    cars_data = [
        {"name": "🚗 기아 레이 (국민차)", "odds": 12.0, "win_rate": "8%"},
        {"name": "🏎️ 페라리 488", "odds": 1.5, "win_rate": "45%"},
        {"name": "🚙 람보르기니", "odds": 2.0, "win_rate": "35%"},
        {"name": "🚜 트랙터 (반전)", "odds": 25.0, "win_rate": "2%"}
    ]
    st.table(pd.DataFrame(cars_data).rename(columns={'name':'차량명', 'odds':'배당률', 'win_rate':'예상승률'}))
    
    bet_car = st.selectbox("배팅할 차량 선택", [c['name'] for c in cars_data])
    amt = st.number_input("배팅 금액", min_value=10000, step=10000)
    
    if st.button("🚥 RACE START!"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['name']) for c in cars_data]; pos = [0]*4
            while max(pos) < 100:
                for i in range(4):
                    spd = random.randint(1, 15) if "페라리" in cars_data[i]['name'] else random.randint(1, 10)
                    pos[i] += spd; bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win_idx = pos.index(max(pos)); win_name = cars_data[win_idx]['name']
            if win_name == bet_car:
                payout = int(amt * cars_data[win_idx]['odds'])
                st.success(f"🎊 예측 성공! {win_name} 우승! 당첨금 ₩{payout:,} 지급!"); st.session_state.global_cash += payout
            else: st.error(f"실패.. {win_name}이(가) 먼저 도착했습니다.")
            sync_user_data()
        else: st.error("잔액 부족")

# ==============================
# [7] 슬롯머신 (수동 정지 추가)
# ==============================
elif menu == "🎰 럭키 슬롯머신":
    st.title("🎰 럭키 슬롯머신")
    
    if 'slot_spinning' not in st.session_state: st.session_state.slot_spinning = False
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🕹️ 레버 당기기 (₩100,000)", disabled=st.session_state.slot_spinning):
            if st.session_state.global_cash >= 100000:
                st.session_state.global_cash -= 100000; st.session_state.slot_spinning = True; st.rerun()
    with col2:
        if st.button("⏹️ STOP!!", disabled=not st.session_state.slot_spinning):
            st.session_state.slot_spinning = False
            items = ["💎", "7️⃣", "🍒", "🍋", "🔔"]
            res = [random.choice(items) for _ in range(3)]
            st.markdown(f"<h1 style='text-align:center; font-size:100px;'>[ {' | '.join(res)} ]</h1>", unsafe_allow_html=True)
            if res[0] == res[1] == res[2]:
                st.balloons(); st.success("🎉 CONGRATULATIONS!!! 잭팟 ₩10,000,000!!"); st.session_state.global_cash += 10000000
            else: st.info("꽝! 다음 기회에..")
            sync_user_data()

    if st.session_state.slot_spinning:
        items = ["💎", "7️⃣", "🍒", "🍋", "🔔"]
        slot_area = st.empty()
        for _ in range(20):
            res = [random.choice(items) for _ in range(3)]
            slot_area.markdown(f"<h1 style='text-align:center; font-size:100px;'>[ {' | '.join(res)} ]</h1>", unsafe_allow_html=True)
            time.sleep(0.05)

# ==============================
# [8] 채굴기 (시각 효과 고도화)
# ==============================
elif menu == "⛏️ 코인 채굴기":
    st.title("⛏️ 가상화폐 채굴장")
    st.markdown("<p style='font-size:24px;'>클릭할 때마다 채굴 현황이 실시간으로 반영됩니다.</p>", unsafe_allow_html=True)
    if st.button("💻 CLICK TO MINE (₩1,000)", use_container_width=True):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h2 style='text-align:center; color:#00ff88;'>💰 +₩1,000 Mined!</h2>", unsafe_allow_html=True)
        st.toast("채굴 성공!")

# ==============================
# [9] 슈퍼 상점 (100가지 아이템 리스트)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 글로벌 하이엔드 상점 (100 ITEMS)")
    
    # 100개 아이템 생성 로직
    items = []
    prefixes = ["럭셔리", "한정판", "골든", "사이버", "빈티지", "다이아몬드", "최첨단"]
    goods = ["시계", "노트북", "요트", "슈트", "헤드셋", "반지", "와인", "카메라", "피규어", "드론"]
    for i in range(1, 91): # 자동 생성 90개
        p = random.choice(prefixes); g = random.choice(goods)
        items.append({"id": f"a{i}", "name": f"{p} {g} No.{i}", "price": i * 2000000, "type": "item"})
    
    # 고정 명품 10개
    lux = [
        {"id": "l1", "name": "🏢 시그니엘 레지던스", "price": 8000000000, "type": "property"},
        {"id": "l2", "name": "🏎️ 람보르기니 아벤타도르", "price": 700000000, "type": "item"},
        {"id": "l3", "name": "🚀 우주 여행 티켓", "price": 20000000000, "type": "item"},
        {"id": "l4", "name": "👑 유니버스 황제 칭호", "price": 1000000000, "type": "title"}
    ]
    items = lux + items
    
    col_i = 0
    cols = st.columns(3)
    for item in items:
        with cols[col_i % 3]:
            st.markdown(f"**{item['name']}**")
            st.write(f"가격: ₩{item['price']:,}")
            if item['id'] in st.session_state.inventory:
                st.button("보유 중", key=item['id'], disabled=True)
            elif st.button("구매하기", key=item['id']):
                if st.session_state.global_cash >= item['price']:
                    st.session_state.global_cash -= item['price']; st.session_state.inventory.append(item['id'])
                    if item['type'] == 'title': st.session_state.equipped_title = item['name']
                    sync_user_data(); st.rerun()
                else: st.error("돈 부족")
        col_i += 1

# ==============================
# [10] 자유게시판
# ==============================
elif menu == "💬 자유게시판":
    st.title("💬 유저 자유게시판")
    msg = st.text_input("메시지 입력 (최대 50자)", max_chars=50)
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg, "time":datetime.now().strftime("%H:%M")}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])): st.info(f"**{c['name']}**: {c['comment']} ({c['time']})")
