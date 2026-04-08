import streamlit as st
import pandas as pd
import plotly.express as px
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
                'solved_count': st.session_state.get('solved_count', 0)
            })
            save_db(USERS_FILE, users)

st.set_page_config(page_title="HYOMIN UNIVERSE v4", page_icon="🚀", layout="wide")

# ==============================
# [핵심] 정보처리기사 무한 문제 생성 엔진
# ==============================
def generate_questions(count=5):
    # 실제 정처기 핵심 개념 뱅크 (이 내용을 기반으로 수천개의 조합 생성)
    concept_bank = [
        {"q": "OSI 7계층 중 전송 경로를 설정하고 패킷을 전달하는 계층은?", "a": "네트워크 계층", "w": ["물리 계층", "전송 계층", "응용 계층"]},
        {"q": "데이터베이스의 무결성 중 기본키 값은 Null이 될 수 없다는 규칙은?", "a": "개체 무결성", "w": ["참조 무결성", "도메인 무결성", "사용자 무결성"]},
        {"q": "소프트웨어 테스트 중 모듈 간의 인터페이스를 확인하는 테스트는?", "a": "통합 테스트", "w": ["단위 테스트", "시스템 테스트", "인수 테스트"]},
        {"q": "응집도(Cohesion) 중 가장 높은 응집도를 가진 단계는?", "a": "기능적 응집도", "w": ["순차적 응집도", "교환적 응집도", "논리적 응집도"]},
        {"q": "결합도(Coupling) 중 가장 낮은 결합도를 가진 단계는?", "a": "자료 결합도", "w": ["스탬프 결합도", "제어 결합도", "내용 결합도"]},
        {"q": "SQL에서 테이블의 구조를 변경할 때 사용하는 명령어는?", "a": "ALTER", "w": ["UPDATE", "INSERT", "MODIFY"]},
        {"q": "TCP/IP 4계층 중 응용 계층의 프로토콜이 아닌 것은?", "a": "UDP", "w": ["HTTP", "FTP", "SMTP"]},
        {"q": "디자인 패턴 중 객체 생성을 캡슐화하여 서브클래스에서 결정하게 하는 패턴은?", "a": "Factory Method", "w": ["Singleton", "Observer", "Strategy"]},
        {"q": "UML 다이어그램 중 정적인 구조를 표현하는 대표적인 다이어그램은?", "a": "클래스 다이어그램", "w": ["시퀀스 다이어그램", "상태 다이어그램", "활동 다이어그램"]},
        {"q": "프로세스 스케줄링 중 선점형 방식인 것은?", "a": "Round Robin", "w": ["FIFO", "SJF", "HRN"]},
        {"q": "소프트웨어 개발 보안의 3요소가 아닌 것은?", "a": "가용성", "w": ["무결성", "기밀성", "효율성"]},
        {"q": "정적 테스트 기법 중 하나로, 개발자가 작성한 코드를 읽으며 오류를 찾는 것은?", "a": "인스펙션", "w": ["블랙박스 테스트", "회귀 테스트", "스트레스 테스트"]},
        {"q": "데이터베이스 로그(Log)를 이용하여 복구하는 기법은?", "a": "회복(Recovery)", "w": ["병행제어", "정규화", "교착상태"]},
        {"q": "애플리케이션 성능 지표가 아닌 것은?", "a": "유지보수성", "w": ["처리량", "응답시간", "자원사용률"]},
        {"q": "암호화 알고리즘 중 공개키 암호 방식의 대표적인 예는?", "a": "RSA", "w": ["DES", "AES", "SEED"]}
    ]
    
    selected = random.sample(concept_bank, min(count, len(concept_bank)))
    final_qs = []
    for i, item in enumerate(selected):
        opts = item['w'] + [item['a']]
        random.shuffle(opts)
        final_qs.append({"id": f"gen_{random.randint(1,999999)}", "q": item['q'], "opts": opts, "a": item['a']})
    return final_qs

# ==============================
# CSS 스타일링 (가독성 최우선)
# ==============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; color: #f0f0f0; }
    .stApp { background: linear-gradient(135deg, #050510 0%, #101025 50%, #0d1221 100%); }
    
    .market-header { font-size: 28px !important; font-weight: 700; color: #00d4ff; border-bottom: 2px solid #00d4ff; padding-bottom: 10px; margin-bottom: 20px; }
    .stock-table { width: 100%; border-collapse: collapse; font-size: 22px; background: rgba(255,255,255,0.02); border-radius: 10px; }
    .stock-table td, .stock-table th { padding: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
    .price-up { color: #00ff88; font-weight: bold; }
    .price-down { color: #ff4444; font-weight: bold; }

    .stButton>button { border: 1px solid #00d4ff; color: #00d4ff; background: rgba(0,212,255,0.05); font-size: 18px; padding: 10px 20px; border-radius: 8px; }
    .stButton>button:hover { background-color: #00d4ff; color: #0a0a1a; box-shadow: 0 0 15px #00d4ff; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 로직
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 50px;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tab1:
            l_id = st.text_input("아이디")
            l_pw = st.text_input("비밀번호", type="password")
            if st.button("접속하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'],
                        'inventory': users[l_id]['inventory'], 'equipped_title': users[l_id]['equipped_title'],
                        'portfolio': users[l_id].get('portfolio', {}), 'solved_count': users[l_id].get('solved_count', 0)
                    })
                    st.rerun()
                else: st.error("정보 불일치")
        with tab2:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("가입", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users: st.error("이미 있음")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "solved_count": 0}
                    save_db(USERS_FILE, users); st.success("성공!")
    st.stop()

# ==============================
# 사이드바
# ==============================
with st.sidebar:
    st.title("UNIVERSE MENU")
    st.subheader(f"👤 {st.session_state.logged_in_user}")
    st.markdown(f"**현재 칭호:** `{st.session_state.equipped_title}`")
    st.metric("자산 현황", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃", use_container_width=True):
        sync_user_data()
        st.session_state.clear(); st.rerun()
    st.markdown("---")
    menu = st.radio("포털 이동", ["🏦 통합 금융", "⚽ 구단주 매니저", "💻 무한 CBT 모의고사", "⛏️ 채굴기", "🛒 프리미엄 상점", "💬 자유게시판"])

# ==============================
# 🏦 통합 금융 (주식 시장) - 10초 자동 갱신형
# ==============================
if menu == "🏦 통합 금융":
    st.markdown("<div class='market-header'>📈 글로벌 실시간 주식 종합 시장 (10초 자동 갱신)</div>", unsafe_allow_html=True)
    
    stock_config = [
        {"id": "SAMJI", "name": "삼지전자", "vol": 0.05, "trend": 1.01},
        {"id": "SAMSUNG", "name": "삼성전자", "vol": 0.02, "trend": 1.0},
        {"id": "HYUNDAI", "name": "현대차", "vol": 0.025, "trend": 1.0},
        {"id": "NAVER", "name": "네이버", "vol": 0.03, "trend": 1.0},
        {"id": "KAON", "name": "가온브로드밴드", "vol": 0.06, "trend": 1.02},
        {"id": "CRYPTO", "name": "도지코인", "vol": 0.15, "trend": 0.99}
    ]

    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(10000, 100000), "history": [random.randint(10000, 100000)]} for s in stock_config}

    # 주가 변동 엔진
    rows_html = ""
    for cfg in stock_config:
        sid = cfg['id']
        curr = st.session_state.stock_data[sid]
        change_pct = (random.random() - 0.5) * 2 * cfg['vol'] * cfg['trend']
        curr['price'] = round(max(500, curr['price'] * (1 + change_pct)))
        curr['history'].append(curr['price'])
        curr['history'] = curr['history'][-20:]
        
        color_class = "price-up" if change_pct >= 0 else "price-down"
        sign = "▲" if change_pct >= 0 else "▼"
        rows_html += f"<tr><td>{curr['name']}</td><td style='text-align:right;'>₩{curr['price']:,}</td><td class='{color_class}' style='text-align:right;'>{sign} {abs(change_pct*100):.2f}%</td></tr>"

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"<table class='stock-table'><tr><th>종목명</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th></tr>{rows_html}</table>", unsafe_allow_html=True)
    with col2:
        st.subheader("계좌 관리")
        sel = st.selectbox("종목 선택", [s['name'] for s in stock_config])
        sid = [s['id'] for s in stock_config if s['name'] == sel][0]
        
        # 차트 가독성 보강
        fig = px.line(y=st.session_state.stock_data[sid]['history'], template="plotly_dark", height=250)
        fig.update_traces(line_color="#00d4ff", line_width=3)
        st.plotly_chart(fig, use_container_width=True)
        
        curr_price = st.session_state.stock_data[sid]['price']
        st.markdown(f"### 현재가: ₩{curr_price:,}")
        
        qty_input = st.number_input("거래 수량", min_value=1, value=1)
        c1, c2 = st.columns(2)
        if c1.button("📈 매수", use_container_width=True):
            if st.session_state.global_cash >= qty_input * curr_price:
                st.session_state.global_cash -= qty_input * curr_price
                old = st.session_state.portfolio.get(sid, {"qty": 0, "avg_price": 0})
                new_qty = old['qty'] + qty_input
                new_avg = ((old['qty'] * old['avg_price']) + (qty_input * curr_price)) / new_qty
                st.session_state.portfolio[sid] = {"qty": new_qty, "avg_price": new_avg}
                sync_user_data(); st.rerun()
            else: st.error("잔액 부족")
        if c2.button("📉 매도", use_container_width=True):
            owned = st.session_state.portfolio.get(sid, {"qty": 0})['qty']
            if owned >= qty_input:
                st.session_state.global_cash += qty_input * curr_price
                st.session_state.portfolio[sid]['qty'] -= qty_input
                sync_user_data(); st.rerun()
            else: st.error("보유량 부족")

    time.sleep(10); st.rerun()

# ==============================
# ⚽ 구단주 매니저 (30초 시뮬레이션)
# ==============================
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 라이브 시뮬레이션")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("경기 설정")
        formation = st.selectbox("전술 선택", ["4-4-2 (밸런스)", "4-3-3 (공격형)", "3-5-2 (중원장악)"])
        if st.button("🏟️ 경기 시작 (30초)", use_container_width=True):
            st.markdown("---")
            score_area = st.empty()
            live_bar = st.progress(0)
            comm_area = st.empty()
            h, a = 0, 0
            for i in range(30):
                if random.random() < 0.06: h += 1
                if random.random() < 0.04: a += 1
                score_area.markdown(f"<h1 style='text-align:center; font-size:60px;'>HOME {h} : {a} AWAY</h1>", unsafe_allow_html=True)
                live_bar.progress((i+1)/30, text=f"매치 진행 중... ({i*3}분)")
                events = ["중원에서의 치열한 몸싸움!", "역습 기회!", "골키퍼 슈퍼 세이브!", "날카로운 킬패스!", "관중석의 함성!"]
                comm_area.info(f"🎙️ 중계멘트: {random.choice(events)}")
                time.sleep(1)
            
            if h > a: 
                reward = 5000000; st.success(f"승리! 보상 ₩{reward:,} 지급"); st.balloons()
            elif h == a:
                reward = 1000000; st.warning(f"무승부! 보상 ₩{reward:,} 지급")
            else:
                reward = 100000; st.error(f"패배.. 위로금 ₩{reward:,} 지급")
            st.session_state.global_cash += reward
            sync_user_data()

# ==============================
# 💻 무한 CBT 모의고사 (무한 생성 엔진)
# ==============================
elif menu == "💻 무한 CBT 모의고사":
    st.title("💻 무한 정처기 모의고사 엔진")
    st.info("💡 엔진이 이론 데이터를 기반으로 문제를 무작위 조합하여 무한 생성합니다.")
    
    if 'current_exam' not in st.session_state:
        st.session_state.current_exam = generate_questions(5)

    with st.form("exam_form"):
        user_ans = {}
        for i, q in enumerate(st.session_state.current_exam):
            st.markdown(f"**Q{i+1}. {q['q']}**")
            user_ans[i] = st.radio(f"정답 선택 (문제ID: {q['id']})", q['opts'], key=f"q_{i}")
        
        if st.form_submit_button("채점 및 상금 수령"):
            correct = 0
            for i, q in enumerate(st.session_state.current_exam):
                if user_ans[i] == q['a']: correct += 1
            
            earned = correct * 200000
            st.session_state.global_cash += earned
            st.session_state.solved_count += correct
            sync_user_data()
            st.success(f"채점 완료! {correct}문제 정답. 총 ₩{earned:,} 장학금 지급!")

    if st.button("🔄 새로운 5문제 생성 (다음 세트)"):
        st.session_state.current_exam = generate_questions(5)
        st.rerun()

# ==============================
# ⛏️ 채굴기 (1000원)
# ==============================
elif menu == "⛏️ 채굴기":
    st.title("⛏️ 가상화폐 채굴장")
    st.markdown("클릭 한 번당 ₩1,000의 수익이 발생합니다.")
    if st.button("💻 클릭하여 채굴!", use_container_width=True):
        st.session_state.global_cash += 1000
        st.toast("₩1,000 채굴 완료!", icon="💰")
        sync_user_data()

# ==============================
# 🛒 프리미엄 상점 (리뉴얼)
# ==============================
elif menu == "🛒 프리미엄 상점":
    st.title("🛒 하이엔드 럭셔리 상점")
    items = [
        {"id": "t1", "name": "🥉 유망주 칭호", "price": 1000000, "type": "title"},
        {"id": "t2", "name": "🥈 프로 게이머 칭호", "price": 10000000, "type": "title"},
        {"id": "t3", "name": "🥇 억만장자 칭호", "price": 100000000, "type": "title"},
        {"id": "t4", "name": "💎 유니버스 지배자 칭호", "price": 1000000000, "type": "title"},
        {"id": "i1", "name": "🍎 최신형 스마트폰 Pro Max", "price": 2000000, "type": "item"},
        {"id": "i2", "name": "☕ 평생 무료 스타벅스 이용권", "price": 5000000, "type": "item"},
        {"id": "i3", "name": "🚗 테슬라 모델 S", "price": 120000000, "type": "item"},
        {"id": "i4", "name": "🚁 자가용 헬리콥터", "price": 500000000, "type": "item"},
        {"id": "i5", "name": "🏰 강남 펜트하우스", "price": 5000000000, "type": "item"},
        {"id": "i6", "name": "🚀 화성 탐사 티켓", "price": 10000000000, "type": "item"}
    ]
    
    for item in items:
        col1, col2 = st.columns([3, 1])
        owned = item['id'] in st.session_state.inventory
        col1.markdown(f"### {item['name']}")
        col1.write(f"가격: ₩{item['price']:,}")
        if owned:
            if item['type'] == 'title' and st.session_state.equipped_title != item['name']:
                if col2.button("장착", key=item['id']):
                    st.session_state.equipped_title = item['name']; sync_user_data(); st.rerun()
            else: col2.button("보유 중", disabled=True, key=item['id'])
        else:
            if col2.button(f"구매", key=item['id']):
                if st.session_state.global_cash >= item['price']:
                    st.session_state.global_cash -= item['price']
                    st.session_state.inventory.append(item['id'])
                    sync_user_data(); st.success("구매 성공!"); st.rerun()
                else: st.error("잔액 부족")
