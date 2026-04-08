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
    prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()} if 'stock_data' in st.session_state else {}
    for uid, data in users.items():
        wealth = data.get('cash', 0)
        for sid, p_data in data.get('portfolio', {}).items():
            if sid in prices: wealth += p_data.get('qty', 0) * prices[sid]
        rankings.append({"uid": uid, "total": wealth})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

st.set_page_config(page_title="HYOMIN UNIVERSE v10.0", page_icon="🌌", layout="wide")

# ==============================
# 🔐 로그인 시스템 (기기 환경 선택 추가)
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
    st.markdown("<p>최적의 해상도를 위해 접속하시는 기기 환경을 선택해 주세요.</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        # 기기 선택 라디오 버튼
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
                        'equipped_title': users[l_id]['equipped_title'], 'portfolio': users[l_id].get('portfolio', {}),
                        'device_mode': device_mode # 선택한 기기 환경 저장
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
    # PC 전용 CSS (크고 굵고 시원하게)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
        .stApp { background-color: #050505 !important; }
        html, body, [class*="css"], .stMarkdown, p, span, li, label { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; font-size: 24px !important; font-weight: 700 !important; }
        div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
        div[data-baseweb="select"] * { color: #FFFFFF !important; font-size: 24px !important; font-weight: 900 !important; }
        div[data-baseweb="popover"] * { background-color: #1A1C24 !important; color: #00FF88 !important; font-size: 22px !important; }
        .stNumberInput input { background-color: #222 !important; color: #00FF88 !important; font-size: 26px !important; }
        
        /* PC 사이드바 강조 */
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
    # 모바일 전용 CSS (컴팩트하게)
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
# 📈 주식 데이터 엔진
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SAMSG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDI", "name": "현대차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GOODS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩", "vol": 0.07}
]

c_keys = set([s['id'] for s in stock_config])
if 'stock_data' not in st.session_state or set(st.session_state.stock_data.keys()) != c_keys:
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 150000), "history": [80000]} for s in stock_config}
if 'news' not in st.session_state: st.session_state.news = "시장이 안정적으로 운영 중입니다."
if 'news_time' not in st.session_state: st.session_state.news_time = time.time()
if 'last_tick' not in st.session_state: st.session_state.last_tick = time.time()

# ==============================
# 🧭 메뉴 분기 (PC vs Mobile)
# ==============================
menu_options = ["🏠 홈 광장", "📈 주식 트레이딩", "⚽ 구단주 매니저", "📡 통신 업무", "💻 CBT 모의고사", "🏎️ 레이싱", "🎰 슬롯머신", "⛏️ 채굴기", "🛒 슈퍼 상점", "💬 게시판"]

if st.session_state.device_mode == "🖥️ PC (데스크탑/태블릿)":
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.logged_in_user}님")
        st.markdown(f"**칭호**: `{st.session_state.equipped_title}`")
        st.metric("💰 보유 자산", f"₩{st.session_state.global_cash:,}")
        if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        st.markdown("---")
        menu = st.radio("포털 이동", menu_options)
        st.markdown("---")
        st.markdown("### 🏆 부자 랭킹")
        for i, r in enumerate(get_rankings()[:3]): st.write(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")
else:
    st.markdown(f"<div style='text-align:right; color:#FFD600;'>👤 <b>{st.session_state.logged_in_user}</b>님 | 💰 <b>₩{st.session_state.global_cash:,}</b></div>", unsafe_allow_html=True)
    menu = st.selectbox("📌 이동할 메뉴를 선택하세요", menu_options)
    with st.expander("🏆 실시간 부자 랭킹 보기"):
        for i, r in enumerate(get_rankings()[:5]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "🏅"
            st.write(f"{medal} **{r['uid']}**: ₩{r['total']:,.0f}")
        if st.button("🔴 로그아웃"):
            sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")

# ==============================
# [1] 홈
# ==============================
if menu == "🏠 홈 광장":
    st.title(f"환영합니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown(f"현재 **{st.session_state.device_mode}** 모드로 접속 중입니다.")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")
    
    st.write("---")
    st.markdown("### 👑 창조주 전용 치트키")
    if st.button("비밀 금고에서 10억 인출하기"):
        st.session_state.global_cash += 1000000000
        sync_user_data(); st.success("통장에 10억이 입금되었습니다!"); st.rerun()

# ==============================
# [2] 주식 (10초 강제 갱신 + 포트폴리오)
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 실시간 거래소")
    
    # 뉴스 엔진
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

    t_mkt, t_acc = st.tabs(["📊 시황", "💼 내 포트폴리오"])
    
    with t_mkt:
        rows = ""
        for s in stock_config:
            curr = st.session_state.stock_data[s['id']]
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
            if qty > 0 and sid in st.session_state.stock_data:
                cp = st.session_state.stock_data[sid]['price']
                ap = info.get('avg_price', 0)
                eval_amt = qty * cp
                total_eval += eval_amt
                roi = ((cp - ap) / ap * 100) if ap > 0 else 0
                p_list.append({"종목": st.session_state.stock_data[sid]['name'], "수량": f"{qty}주", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("보유 주식이 없습니다.")
        st.markdown(f"💰 주식자산: ₩{total_eval:,} | 💵 현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    sel_name = st.selectbox("매매할 종목을 고르세요", [s['name'] for s in stock_config])
    sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
    st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    
    cp = st.session_state.stock_data[sid]['price']
    st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{cp:,}</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💥 풀매수"):
            max_q = st.session_state.global_cash // cp
            if max_q > 0:
                st.session_state.global_cash -= max_q * cp
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + max_q
                new_a = ((old['qty'] * old['avg_price']) + (max_q * cp)) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data(); st.rerun()
    with c2:
        if st.button("💸 풀매도"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * cp
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data(); st.rerun()

    time.sleep(2); st.rerun()

# ==============================
# [3] 구단주 시뮬레이터
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
# [5] CBT 하드코어 모의고사
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 실전 모의고사")
    st.markdown("정보처리기사 핵심 기출문제 50제가 무작위로 출제됩니다.")
    
    if 'hard_q_pool' not in st.session_state:
        st.session_state.hard_q_pool = [
            {"q": "결합도(Coupling) 중 결합도가 가장 좋은 것은?", "a": "자료 결합도", "w": ["스탬프 결합도", "제어 결합도", "내용 결합도"]},
            {"q": "응집도(Cohesion) 중 응집도가 가장 좋은 것은?", "a": "기능적 응집도", "w": ["논리적 응집도", "시간적 응집도", "절차적 응집도"]},
            {"q": "GoF 디자인 패턴 중 '생성' 패턴에 속하지 않는 것은?", "a": "Adapter", "w": ["Builder", "Singleton", "Prototype"]},
            {"q": "화이트박스 테스트 기법에 해당하는 것은?", "a": "기본 경로 검사", "w": ["경계값 분석", "동치 분할 검사", "원인-효과 그래프"]},
            {"q": "데이터베이스 제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행적 함수 종속 제거", "다치 종속 제거", "결정자가 후보키가 아닌 것 제거"]},
            {"q": "OSI 7계층 중 종단 간 신뢰성을 담당하는 계층은?", "a": "전송 계층", "w": ["네트워크 계층", "데이터링크 계층", "세션 계층"]},
            {"q": "교착상태(Deadlock)의 발생 조건이 아닌 것은?", "a": "선점(Preemption)", "w": ["상호배제", "점유와 대기", "환형 대기"]},
            {"q": "공개키 암호화 알고리즘에 해당하는 것은?", "a": "RSA", "w": ["DES", "AES", "SEED"]},
            {"q": "UML 다이어그램 중 동적 모델링에 사용되는 것은?", "a": "시퀀스 다이어그램", "w": ["클래스 다이어그램", "객체 다이어그램", "컴포넌트 다이어그램"]},
            {"q": "운영체제의 스케줄링 기법 중 비선점형 방식은?", "a": "SJF", "w": ["Round Robin", "SRT", "다단계 큐"]}
        ]
        
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(st.session_state.hard_q_pool)
        opts = st.session_state.current_q['w'] + [st.session_state.current_q['a']]
        random.shuffle(opts)
        st.session_state.current_opts = opts

    with st.form("exam"):
        curr_q = st.session_state.current_q
        st.markdown(f"<h2 style='color:#FFD600;'>Q. {curr_q['q']}</h2>", unsafe_allow_html=True)
        ans = st.radio("정답 선택:", st.session_state.current_opts)
        if st.form_submit_button("제출"):
            if ans == curr_q['a']: 
                st.session_state.global_cash += 500000; st.success("🎉 정답입니다! ₩500,000 지급.")
            else: st.error(f"❌ 오답입니다! (정답: {curr_q['a']})")
            del st.session_state.current_q; sync_user_data(); st.rerun()

# ==============================
# [6] 레이싱
# ==============================
elif menu == "🏎️ 레이싱":
    st.title("🏎️ 역배 챔피언십 배팅")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량", "o":"배당"}))
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("배팅액", min_value=10000, step=10000)
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
# [9] 상점
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 LUXURY SHOP")
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
        st.markdown(f"<div style='border-bottom:1px solid #444; padding:10px;'><b>{c['name']}</b>: {c['comment']}</div>", unsafe_allow_html=True)
