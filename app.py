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
# [중요] 시각적 고대비 및 가독성 설정 (CSS)
# ==============================
st.set_page_config(page_title="HYOMIN UNIVERSE v6.5", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    
    /* 전체 배경을 어둡게 고정하여 흰색/형광색 글씨가 잘 보이게 함 */
    .stApp { background-color: #0A0E17 !important; }
    
    /* 기본 텍스트 크기 및 가독성 (형광색/흰색 강조) */
    html, body, [class*="css"], .stMarkdown, p, label, span, li {
        font-family: 'Noto Sans KR', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        text-shadow: 1px 1px 2px #000;
    }
    
    /* 제목 및 강조 텍스트 색상 대비 조정 */
    h1 { font-size: 4.5rem !important; color: #00D4FF !important; font-weight: 900 !important; }
    h2 { font-size: 2.8rem !important; color: #00FF88 !important; }
    h3 { font-size: 2.2rem !important; color: #FFAA00 !important; }

    /* 주식 테이블 디자인 (고대비) */
    .stock-table { width: 100%; border-collapse: collapse; border: 2px solid #555; background-color: #161B22; }
    .stock-table th { background-color: #30363D; color: #00D4FF !important; font-size: 26px !important; padding: 15px; }
    .stock-table td { font-size: 26px !important; padding: 15px; border-bottom: 1px solid #444; text-align: center; }
    .price-up { color: #FF4B4B !important; font-weight: 900; } /* 빨간색 상승 */
    .price-down { color: #1F77B4 !important; font-weight: 900; } /* 파란색 하락 */

    /* 버튼 스타일 고도화 */
    .stButton>button {
        border: 4px solid #00D4FF !important;
        background-color: #1A1C24 !important;
        color: #00D4FF !important;
        font-size: 26px !important;
        font-weight: 900 !important;
        border-radius: 15px;
        padding: 15px 30px;
    }
    .stButton>button:hover { background-color: #00D4FF !important; color: #000000 !important; box-shadow: 0 0 20px #00D4FF; }

    /* 사이드바 메뉴 가독성 */
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #333; }
    [data-testid="stSidebar"] * { font-size: 20px !important; color: #E6EDF3 !important; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 / 세션 초기화
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 30px; color: #00FF88;'>효민 유니버스에 오신 것을 환영합니다!</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        tab_log = st.tabs(["🔒 로그인", "📝 시민 등록"])
        with tab_log[0]:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("입장하기"):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_ids': set(users[l_id].get('solved_ids', []))
                    })
                    st.rerun()
                else: st.error("정보가 일치하지 않습니다.")
        with tab_log[1]:
            n_id = st.text_input("아이디 생성")
            n_pw = st.text_input("비밀번호 생성", type="password")
            if st.button("등록 신청"):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 사용 중인 이름입니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인해 주세요.")
    st.stop()

# 주식 데이터 초기화 (KeyError 방지 로직)
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05}, {"id": "SMSUNG", "name": "삼성전자", "vol": 0.02},
    {"id": "HYNDAI", "name": "현대자동차", "vol": 0.025}, {"id": "NAVER", "name": "네이버", "vol": 0.03},
    {"id": "KAON", "name": "가온브로드", "vol": 0.06}, {"id": "HFR", "name": "HFR", "vol": 0.05},
    {"id": "GDS", "name": "굿어스데이터", "vol": 0.04}, {"id": "RAY", "name": "레이자동차", "vol": 0.03},
    {"id": "DOGE", "name": "도지코인", "vol": 0.15}, {"id": "VHDL", "name": "VHDL칩셋", "vol": 0.07}
]

if 'stock_data' not in st.session_state or len(st.session_state.stock_data) != len(stock_config):
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(30000, 150000), "history": [80000]} for s in stock_config}
if 'news' not in st.session_state: st.session_state.news = "시장이 개장되었습니다."
if 'last_news_time' not in st.session_state: st.session_state.last_news_time = time.time()

# ==============================
# 사이드바 (정보창)
# ==============================
with st.sidebar:
    st.markdown("### 👤 유저 정보")
    st.markdown(f"**이름:** {st.session_state.logged_in_user}")
    st.markdown(f"**칭호:** `{st.session_state.equipped_title}`")
    st.metric("💰 보유 자산", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): 
        sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 이동", ["🏠 메인 광장", "📈 주식 종합 시장", "⚽ 구단주 매니저", "📡 통신 신호 동기화", "💻 CBT 모의고사", "🏎️ 레이싱 배팅", "🎰 럭키 슬롯머신", "⛏️ 코인 채굴기", "🛒 슈퍼 상점", "💬 자유게시판"])
    
    st.markdown("---")
    st.markdown("### 🏆 부자 랭킹 (TOP 3)")
    for i, r in enumerate(get_user_rankings()[:3]):
        st.markdown(f"{['🥇','🥈','🥉'][i]} **{r['uid']}**: ₩{r['total']:,.0f}")

# ==============================
# 1. 홈 (안내데스크)
# ==============================
if menu == "🏠 메인 광장":
    st.title("🌠 효민 유니버스에 오신 것을 환영합니다!")
    st.markdown(f"안녕하세요, **{st.session_state.logged_in_user}님**! 이곳은 모든 시민이 평등하게 자산을 경쟁하는 공간입니다.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📢 게임 안내")
        st.markdown("""
        - **주식 시장**: 10개 종목을 분석하여 '풀매수'의 짜릿함을 느껴보세요.
        - **구단주**: 최고의 포메이션을 짜서 팀을 승리로 이끄세요. (30초 중계)
        - **통신 신호**: 엔지니어의 마음으로 파형을 맞추고 보너스를 획득하세요.
        - **CBT**: 공부도 하고 돈도 벌고! 정처기 문제를 풀고 장학금을 받으세요.
        """)
    with col2:
        st.subheader("💡 팁")
        st.markdown("""
        - 채굴기는 가장 확실한 자본 마련 수단입니다.
        - 랭킹은 10초마다 갱신되는 주식 가격을 포함하여 계산됩니다.
        - 상점의 '칭호' 아이템을 장착하여 명예를 드높이세요.
        """)
    st.info("친구들을 초대하여 누가 더 빨리 부자가 되는지 내기해보세요!")

# ==============================
# 2. 주식 (시장 + 포트폴리오)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 주식 종합 트레이딩 센터")
    
    # 30초마다 뉴스 발생 및 시장 반영
    if time.time() - st.session_state.last_news_time > 30:
        target = random.choice(stock_config)
        impact = random.uniform(-0.15, 0.15)
        st.session_state.stock_data[target['id']]['price'] *= (1 + impact)
        st.session_state.news = f"📰 [속보] {target['name']}, {'기록적인 영업이익 달성!' if impact > 0 else '공장 화재로 인한 생산 중단!'}"
        st.session_state.last_news_time = time.time()

    st.warning(st.session_state.news)

    # 1. 내 포트폴리오 (수익률 계산)
    st.subheader("💼 내 포트폴리오 (보유 주식 현황)")
    my_port_data = []
    total_eval = 0
    for sid, p_info in st.session_state.portfolio.items():
        qty = p_info.get('qty', 0)
        if qty > 0:
            curr_p = st.session_state.stock_data[sid]['price']
            avg_p = p_info.get('avg_price', 0)
            eval_amt = qty * curr_p
            total_eval += eval_amt
            profit_amt = eval_amt - (qty * avg_p)
            profit_rate = ((curr_p - avg_p) / avg_p * 100) if avg_p > 0 else 0
            
            my_port_data.append({
                "종목명": st.session_state.stock_data[sid]['name'],
                "보유량": f"{qty}주",
                "평단가": f"₩{int(avg_p):,}",
                "현재가": f"₩{int(curr_p):,}",
                "평가금액": f"₩{int(eval_amt):,}",
                "수익률": f"{profit_rate:+.2f}%"
            })
    
    if my_port_data:
        st.table(pd.DataFrame(my_port_data))
        st.markdown(f"**총 주식 평가액:** ₩{total_eval:,} | **보유 현금:** ₩{st.session_state.global_cash:,}")
    else:
        st.info("현재 보유 중인 주식이 없습니다.")

    st.markdown("---")

    # 2. 시장 현황 테이블
    rows_html = ""
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        color_class = "price-up" if change >= 0 else "price-down"
        sign = "▲" if change >= 0 else "▼"
        rows_html += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{color_class}'>{sign} {abs(change*100):.2f}%</td></tr>"

    c1, c2 = st.columns([1.4, 1])
    with c1:
        st.markdown(f"<table class='stock-table'><tr><th>종목명</th><th>현재가</th><th>전일비</th></tr>{rows_html}</table>", unsafe_allow_html=True)
    with c2:
        st.subheader("🕹️ 빠른 매매")
        sel_name = st.selectbox("종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'][-20:], template="plotly_dark", height=250), use_container_width=True)
        
        buy_qty = st.number_input("수량", min_value=1, value=1)
        if st.button("💥 풀매수 (ALL-IN)"):
            price = st.session_state.stock_data[sid]['price']
            can_buy = st.session_state.global_cash // price
            if can_buy > 0:
                st.session_state.global_cash -= can_buy * price
                old_info = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_qty = old_info['qty'] + can_buy
                # 평단가 계산: (기존총액 + 신규총액) / 신규수량
                new_avg = ((old_info['qty'] * old_info['avg_price']) + (can_buy * price)) / new_qty
                st.session_state.portfolio[sid] = {"qty": new_qty, "avg_price": new_avg}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도 (SELL-ALL)"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid] = {'qty':0, 'avg_price':0}
                sync_user_data(); st.rerun()

    time.sleep(10); st.rerun()

# ==============================
# 3. 구단주 매니저
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이션")
    col_f, col_s = st.columns([1, 2])
    with col_f:
        f_choice = st.selectbox("포메이션 설정", ["4-4-2 (표준)", "4-3-3 (공격)", "3-5-2 (중원)", "5-4-1 (수비)"])
        st.write(f"현재 선택: **{f_choice}**")
    
    if st.button("🏟️ 경기 시작 (30초 시뮬레이션)"):
        board = st.empty(); bar = st.progress(0); log = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            board.markdown(f"<div style='text-align:center; background:#111; padding:20px; border-radius:20px; border:5px solid #00FF88;'><h1 style='font-size:100px; color:#FFF;'>{h} : {a}</h1></div>", unsafe_allow_html=True)
            bar.progress((i+1)/30, text=f"전반전/후반전 진행 중... ({i*3}분)")
            time.sleep(1)
        win_money = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += win_money; sync_user_data()
        st.success(f"매치 종료! ₩{win_money:,} 정산 완료.")

# ==============================
# 4. 통신 신호 (금액 명시)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 처리 동기화 업무")
    if 't_f' not in st.session_state: st.session_state.t_f = random.randint(2, 12); st.session_state.t_a = random.randint(3, 10)
    
    st.markdown("<div style='background:#330000; padding:20px; border-radius:10px; border:2px solid #FF4B4B;'>"
                "<h3 style='color:#FF4B4B; margin:0;'>💰 성공 상금: +₩1,500,000 | ❌ 실패 벌금: -₩500,000</h3></div>", unsafe_allow_html=True)
    
    f = st.slider("주파수 조절", 1, 15, 5); a = st.slider("진폭 조절", 1, 15, 5)
    x = np.linspace(0, 10, 400); y_t = st.session_state.t_a * np.sin(st.session_state.t_f * x); y_u = a * np.sin(f * x)
    st.plotly_chart(px.line(pd.DataFrame({'x':x, 'Target':y_t, 'Input':y_u}), x='x', y=['Target', 'Input'], template='plotly_dark'), use_container_width=True)
    
    if st.button("📡 신호 동기화 승인"):
        if f == st.session_state.t_f and a == st.session_state.t_a:
            st.session_state.global_cash += 1500000; st.balloons(); st.success("✅ 성공! +₩1,500,000")
        else:
            st.session_state.global_cash -= 500000; st.error("❌ 실패! -₩500,000 및 파형 재스캔")
        del st.session_state.t_f; sync_user_data(); st.rerun()

# ==============================
# 5. CBT (글씨 대형화)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 모의고사 장학금")
    st.markdown("<h2 style='background:white; color:black; padding:10px;'>질문과 보기를 크게 출력합니다.</h2>", unsafe_allow_html=True)
    q_data = {"q":"OSI 7계층 중 3계층(IP 패킷 전송)에 해당하는 계층은?", "a":"네트워크 계층", "opts":["물리 계층", "데이터링크 계층", "네트워크 계층", "전송 계층"]}
    
    with st.form("cbt_huge"):
        st.markdown(f"<h1 style='color:yellow; text-align:left; font-size:40px !important;'>Q. {q_data['q']}</h1>", unsafe_allow_html=True)
        ans = st.radio("정답 선택", q_data['opts'])
        if st.form_submit_button("정답 제출"):
            if ans == q_data['a']:
                st.session_state.global_cash += 500000; st.success("🎉 정답! 장학금 ₩500,000 지급!")
            else: st.error("오답입니다.")
            sync_user_data()

# ==============================
# 6. 레이싱 (역배)
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 챔피언십 역배 배팅")
    cars = [{"n":"🚗 레이 (역배)", "o":15.0}, {"n":"🏎️ 페라리 (정배)", "o":1.5}, {"n":"🚙 람보르기니", "o":2.0}, {"n":"🚜 트랙터 (슈퍼역배)", "o":30.0}]
    st.table(pd.DataFrame(cars).rename(columns={"n":"차량", "o":"배당"}))
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("배팅 금액", min_value=10000, step=10000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt
            bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*4
            while max(pos) < 100:
                for i in range(4): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win_idx = pos.index(max(pos)); win_n = cars[win_idx]['n']
            if win_n == sel:
                money = int(amt * cars[win_idx]['o']); st.session_state.global_cash += money
                st.success(f"🎊 당첨! 우승차 {win_n} / 상금 ₩{money:,}"); st.balloons()
            else: st.error(f"실패.. 우승차는 {win_n}입니다.")
            sync_user_data()

# ==============================
# 7. 슬롯머신 (STOP 버튼)
# ==============================
elif menu == "🎰 럭키 슬롯머신":
    st.title("🎰 슬롯머신 (수동 정지)")
    if 'spin' not in st.session_state: st.session_state.spin = False
    c1, c2 = st.columns(2)
    if c1.button("🕹️ 레버 당기기 (₩100,000)"):
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000; st.session_state.spin = True; st.rerun()
    if c2.button("⏹️ STOP!"):
        st.session_state.spin = False
        res = [random.choice(["💎", "7️⃣", "🍒"]) for _ in range(3)]
        st.markdown(f"<div style='text-align:center; font-size:150px;'>{' '.join(res)}</div>", unsafe_allow_html=True)
        if res[0] == res[1] == res[2]:
            st.markdown("<h1 style='color:gold;'>🎊 CONGRATULATIONS! 🎊</h1>", unsafe_allow_html=True)
            st.session_state.global_cash += 10000000; st.balloons()
        else: st.write("꽝! 다음 기회에.."); sync_user_data()

# ==============================
# 8. 채굴기 (금액 강조)
# ==============================
elif menu == "⛏️ 코인 채굴기":
    st.title("⛏️ 채굴 센터")
    if st.button("💻 CLICK (₩1,000)"):
        st.session_state.global_cash += 1000; sync_user_data()
        st.markdown("<h1 style='text-align:center; color:#FFD700; font-size:120px;'>💰 +1,000</h1>", unsafe_allow_html=True)

# ==============================
# 9. 상점 (100개 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 100 ITEMS LUXURY SHOP")
    items = [{"id":f"i_{i}", "n":f"명품 아이템 #{i}", "p":i*10000000} for i in range(1, 101)]
    col_i = 0
    cols = st.columns(2)
    for it in items:
        with cols[col_i % 2]:
            st.write(f"**{it['n']}** | ₩{it['p']:,}")
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
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg}])
        st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        st.markdown(f"<div style='border-bottom:1px solid #333; padding:10px;'><b>{c['name']}</b>: {c['comment']}</div>", unsafe_allow_html=True)
