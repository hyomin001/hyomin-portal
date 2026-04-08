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
        current_prices = {k: v['price'] for k, v in st.session_state.get('stock_data', {}).items()}
        for sid, p_data in portfolio.items():
            qty = p_data.get('qty', 0)
            if qty > 0:
                portfolio_val += qty * current_prices.get(sid, p_data.get('avg_price', 0))
        rankings.append({"uid": uid, "title": data.get('equipped_title', '시민'), "total": total_wealth + portfolio_val})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

# ==============================
# [무한 문제 생성] 정처기 엔진
# ==============================
def get_random_exam():
    concepts = [
        ("OSI 7계층 중 3계층", "네트워크 계층"), ("LIFO 구조의 자료구조", "스택(Stack)"),
        ("FIFO 구조의 자료구조", "큐(Queue)"), ("기본키는 Null 불가", "개체 무결성"),
        ("외래키 관련 무결성", "참조 무결성"), ("응집도 가장 높은 단계", "기능적 응집도"),
        ("결합도 가장 낮은 단계", "자료 결합도"), ("SQL 테이블 삭제", "DROP"),
        ("SQL 구조 변경", "ALTER"), ("UML 정적 다이어그램", "클래스 다이어그램"),
        ("선점형 스케줄링", "Round Robin"), ("비공개키 암호화 방식", "AES / DES"),
        ("공개키 암호화 방식", "RSA"), ("정적 테스트의 대표", "인스펙션"),
        ("화이트박스 테스트", "경로 검사"), ("블랙박스 테스트", "경계값 분석")
    ]
    selected = random.sample(concepts, 5)
    exam_batch = []
    for q_text, a_text in selected:
        wrong_pool = list(set([item[1] for item in concepts if item[1] != a_text]))
        opts = random.sample(wrong_pool, 3) + [a_text]
        random.shuffle(opts)
        exam_batch.append({"id": f"q_{hash(q_text)}_{datetime.now().day}", "q": f"'{q_text}'에 해당하는 것은?", "opts": opts, "a": a_text})
    return exam_batch

st.set_page_config(page_title="HYOMIN UNIVERSE v5", page_icon="🌠", layout="wide")

# ==============================
# CSS (가독성 & 디자인)
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #e0e0e0; }
    .stApp { background: linear-gradient(135deg, #050510 0%, #101025 50%, #0d1221 100%); }
    .stock-table td, .stock-table th { font-size: 20px !important; padding: 15px !important; }
    .price-up { color: #00ff88; font-weight: bold; font-size: 22px; }
    .price-down { color: #ff4444; font-weight: bold; font-size: 22px; }
    .stButton>button { border: 1px solid #00d4ff; color: #00d4ff; background: rgba(0,212,255,0.05); font-weight: bold; border-radius: 8px; }
    div[data-testid="stBlock"] { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; }
    .rank-card { background: rgba(0, 0, 0, 0.4); border-left: 4px solid #ffaa00; padding: 10px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 로직
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 50px;'>🌠 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
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
                else: st.error("정보 불일치")
        with tab2:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("가입", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("중복")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_ids": []}
                    save_db(USERS_FILE, users); st.success("성공!")
    st.stop()

# ==============================
# 글로벌 데이터 초기화
# ==============================
stock_config = [{"id": "SAMJI", "name": "삼지전자", "vol": 0.05, "trend": 1.01}, {"id": "SAMSUNG", "name": "삼성전자", "vol": 0.02, "trend": 1.0},
                {"id": "HYUNDAI", "name": "현대차", "vol": 0.025, "trend": 1.0}, {"id": "KAON", "name": "가온브로드밴드", "vol": 0.06, "trend": 1.02}]
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(50000, 100000), "history": [75000]} for s in stock_config}

# ==============================
# 사이드바 & 랭킹
# ==============================
with st.sidebar:
    st.title("UNIVERSE MENU")
    st.subheader(f"👤 {st.session_state.logged_in_user} [{st.session_state.equipped_title}]")
    st.metric("현금", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 이동", ["🏠 홈", "📈 주식 종합 시장", "⚽ 구단주 매니저", "📡 통신 신호 동기화", "💻 CBT 모의고사", "🏎️ 레이싱 배팅", "🎰 슬롯머신", "⛏️ 채굴기", "🛒 슈퍼 상점", "💬 자유게시판"])
    
    st.markdown("---")
    st.markdown("### 🏆 실시간 랭킹")
    for i, r in enumerate(get_user_rankings()[:3]):
        st.markdown(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")

# ==============================
# 1. 홈
# ==============================
if menu == "🏠 홈":
    st.title("🌠 효민 게임 포털 v5")
    st.markdown("모든 게임의 보상은 자산으로 축적됩니다. 친구들과 경쟁해보세요!")
    st.image("https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?auto=format&fit=crop&w=1200&q=80")

# ==============================
# 2. 주식 (10초 자동 갱신)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 주식 종합 시장")
    rows_html = ""
    for s in stock_config:
        curr = st.session_state.stock_data[s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(curr['price'] * (1 + change))
        curr['history'].append(curr['price'])
        color, sign = ("price-up", "▲") if change >= 0 else ("price-down", "▼")
        rows_html += f"<tr><td>{s['name']}</td><td style='text-align:right;'>₩{curr['price']:,}</td><td class='{color}' style='text-align:right;'>{sign} {abs(change*100):.2f}%</td></tr>"

    col1, col2 = st.columns([1.5, 1])
    with col1: st.markdown(f"<table class='stock-table' style='width:100%'><tr><th>종목</th><th>가격</th><th>등락</th></tr>{rows_html}</table>", unsafe_allow_html=True)
    with col2:
        sel = st.selectbox("종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel][0]
        st.plotly_chart(px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=200), use_container_width=True)
        if st.button("📉 풀매수"):
            max_q = st.session_state.global_cash // st.session_state.stock_data[sid]['price']
            if max_q > 0:
                st.session_state.global_cash -= max_q * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid] = {"qty": st.session_state.portfolio.get(sid, {'qty':0})['qty'] + max_q, "avg_price": st.session_state.stock_data[sid]['price']}
                sync_user_data(); st.rerun()
        if st.button("💸 풀매도"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            if owned > 0:
                st.session_state.global_cash += owned * st.session_state.stock_data[sid]['price']
                st.session_state.portfolio[sid]['qty'] = 0; sync_user_data(); st.rerun()
    time.sleep(10); st.rerun()

# ==============================
# 3. 축구 구단주 (30초 시뮬레이션)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 라이브 시뮬레이터")
    if st.button("🏟️ 경기 시작 (30초 시뮬레이션)", use_container_width=True):
        score_area = st.empty(); live_bar = st.progress(0); comm_area = st.empty()
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.07: h += 1
            if random.random() < 0.04: a += 1
            score_area.markdown(f"<h1 style='text-align:center; font-size:60px;'>HOME {h} : {a} AWAY</h1>", unsafe_allow_html=True)
            live_bar.progress((i+1)/30, text=f"경기 진행 중... ({i*3}분)")
            comm_area.info(f"🎙️ 중계: {random.choice(['우리팀의 환상적인 돌파!', '상대 수비수의 태클!', '골키퍼의 슈퍼 세이브!', '미드필더의 킬패스!'])}")
            time.sleep(1)
        res = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += res; sync_user_data(); st.success(f"정산 완료: +₩{res:,}")

# ==============================
# 4. 통신 신호 (복구)
# ==============================
elif menu == "📡 통신 신호 동기화":
    st.title("📡 신호 처리 미니게임")
    if 't_freq' not in st.session_state: st.session_state.t_freq = random.randint(2, 10); st.session_state.t_amp = random.randint(2, 10)
    f = st.slider("주파수 조절", 1, 15, 5); a = st.slider("진폭 조절", 1, 15, 5)
    x = np.linspace(0, 10, 200)
    y_t = st.session_state.t_amp * np.sin(st.session_state.t_freq * x)
    y_u = a * np.sin(f * x)
    st.plotly_chart(px.line(pd.DataFrame({'x':x, 'Target':y_t, 'You':y_u}), x='x', y=['Target', 'You'], template='plotly_dark'))
    if st.button("신호 일치 확인"):
        if f == st.session_state.t_freq and a == st.session_state.t_amp:
            st.success("보너스 ₩1,000,000!"); st.session_state.global_cash += 1000000; sync_user_data(); del st.session_state.t_freq
        else: st.error("일치하지 않습니다.")

# ==============================
# 5. CBT 모의고사 (무한 문제 엔진)
# ==============================
elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 무한 장학금 모의고사")
    if 'cur_exam' not in st.session_state: st.session_state.cur_exam = get_random_exam()
    with st.form("exam"):
        ans = {}
        for i, q in enumerate(st.session_state.cur_exam):
            st.write(f"**Q{i+1}. {q['q']}**")
            ans[i] = st.radio("보기", q['opts'], key=f"q_{i}")
        if st.form_submit_button("채점"):
            corr = sum(1 for i, q in enumerate(st.session_state.cur_exam) if ans[i] == q['a'] and q['id'] not in st.session_state.solved_ids)
            for i, q in enumerate(st.session_state.cur_exam):
                if ans[i] == q['a']: st.session_state.solved_ids.add(q['id'])
            st.session_state.global_cash += corr * 200000; sync_user_data(); st.success(f"{corr}문제 정답! +₩{corr*200000:,}")
    if st.button("🔄 새로운 문제 가져오기"): st.session_state.cur_exam = get_random_exam(); st.rerun()

# ==============================
# 6. 레이싱 (복구)
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 레이싱 챔피언 배팅")
    cars = ["🚗 페라리", "🚙 람보르기니", "🏎️ 맥라렌", "🚜 트랙터(대박용)"]
    bet_car = st.selectbox("우승차 선택", cars); bet_amt = st.number_input("배팅금액", min_value=10000, step=10000)
    if st.button("🏁 경기 시작!"):
        if st.session_state.global_cash >= bet_amt:
            st.session_state.global_cash -= bet_amt; bars = [st.progress(0, text=c) for c in cars]; pos = [0]*4
            while max(pos) < 100:
                for i in range(4): pos[i] += random.randint(1, 10); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win == bet_car:
                mult = 10 if "트랙터" in win else 3
                st.success(f"{win} 우승! 보상 ₩{bet_amt * mult:,}"); st.session_state.global_cash += bet_amt * mult
            else: st.error(f"{win} 우승.. 배팅금을 잃었습니다.")
            sync_user_data()
        else: st.error("잔액 부족")

# ==============================
# 7. 슬롯머신 (복구)
# ==============================
elif menu == "🎰 슬롯머신":
    st.title("🎰 럭키 슬롯")
    if st.button("🕹️ 레버 당기기 (₩100,000)"):
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000
            slot = st.empty()
            for _ in range(10):
                res = [random.choice(["💎","7️⃣","🍒","🍋"]) for _ in range(3)]
                slot.markdown(f"<h1 style='text-align:center;'>[ {' | '.join(res)} ]</h1>", unsafe_allow_html=True); time.sleep(0.1)
            if res[0] == res[1] == res[2]:
                st.success("잭팟!!! ₩10,000,000!"); st.session_state.global_cash += 10000000; st.balloons()
            sync_user_data()
        else: st.error("잔액 부족")

# ==============================
# 8. 채굴기 (1000원 상향)
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 코인 채굴장")
    if st.button("💻 클릭하여 ₩1,000 채굴!", use_container_width=True):
        st.session_state.global_cash += 1000; st.toast("💰 1,000원 획득!"); sync_user_data()

# ==============================
# 9. 상점 (다양한 럭셔리 아이템)
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 글로벌 프리미엄 상점")
    items = [
        {"id":"t1", "name":"🥉 유망주 칭호", "price":1000000, "type":"title"},
        {"id":"t2", "name":"🥈 프로 게이머 칭호", "price":10000000, "type":"title"},
        {"id":"t3", "name":"🥇 억만장자 칭호", "price":100000000, "type":"title"},
        {"id":"i1", "name":"🍎 스마트폰 Pro Max", "price":2000000, "type":"item"},
        {"id":"i2", "name":"🏎️ 테슬라 모델 S", "price":150000000, "type":"item"},
        {"id":"i3", "name":"🏰 강남 펜트하우스", "price":5000000000, "type":"item"},
        {"id":"i4", "name":"🚀 우주 여행 티켓", "price":10000000000, "type":"item"}
    ]
    for item in items:
        c1, c2 = st.columns([3, 1])
        c1.write(f"### {item['name']} (₩{item['price']:,})")
        if item['id'] in st.session_state.inventory: 
            if item['type'] == 'title' and st.session_state.equipped_title != item['name']:
                if c2.button("장착", key=item['id']): st.session_state.equipped_title = item['name']; sync_user_data(); st.rerun()
            else: c2.button("보유 중", disabled=True, key=item['id'])
        elif c2.button("구매", key=item['id']):
            if st.session_state.global_cash >= item['price']:
                st.session_state.global_cash -= item['price']; st.session_state.inventory.append(item['id'])
                if "칭호" in item['name']: st.session_state.equipped_title = item['name']
                sync_user_data(); st.rerun()

# ==============================
# 10. 커뮤니티
# ==============================
elif menu == "💬 자유게시판":
    st.title("💬 유저 광장")
    msg = st.text_input("메시지 입력")
    if st.button("등록"):
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [{"name":st.session_state.logged_in_user, "comment":msg, "time":datetime.now().strftime("%H:%M")}]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])): st.info(f"**{c['name']}**: {c['comment']} ({c['time']})")
