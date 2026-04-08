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

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_users(users_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=4, ensure_ascii=False)

def sync_user_data():
    if 'logged_in_user' in st.session_state:
        users = load_users()
        uid = st.session_state.logged_in_user
        users[uid]['cash'] = st.session_state.global_cash
        users[uid]['inventory'] = st.session_state.inventory
        users[uid]['equipped_title'] = st.session_state.equipped_title
        users[uid]['portfolio'] = st.session_state.portfolio
        save_users(users)

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def save_comment(name, comment):
    comments = load_comments()
    comments.append({"name": name, "comment": comment, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

# --- 랭킹 시스템 추가 ---
def get_user_rankings():
    users = load_users()
    rankings = []
    for uid, data in users.items():
        total_wealth = data.get('cash', 0)
        # 포트폴리오 가치 계산 (현재가 기준, 현재가가 없으면 매입 단가 사용)
        portfolio_val = 0
        portfolio = data.get('portfolio', {})
        
        # 현재 주식 가격 가져오기 (세션에 있으면 사용, 없으면 0)
        current_prices = {}
        if 'stock_data' in st.session_state:
             current_prices = {k: v['price'] for k, v in st.session_state.stock_data.items()}
             
        for sid, p_data in portfolio.items():
            qty = p_data.get('qty', 0)
            if qty > 0:
                price = current_prices.get(sid, p_data.get('avg_price', 0))
                portfolio_val += qty * price
                
        rankings.append({
            "uid": uid,
            "title": data.get('equipped_title', '뉴비'),
            "total": total_wealth + portfolio_val
        })
    
    # 총 자산 기준으로 내림차순 정렬
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings


st.set_page_config(page_title="HYOMIN UNIVERSE", page_icon="🌌", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Noto Sans KR', sans-serif; color: #e0e0e0; }
    .stApp { background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 50%, #16213e 100%); }
    h1, h2, h3 { color: #00d4ff !important; }
    .stButton>button { border: 1px solid #00d4ff; color: #00d4ff; background: rgba(0,212,255,0.05); border-radius: 8px; }
    .stButton>button:hover { background-color: #00d4ff; color: #0a0a1a; }
    div[data-testid="stBlock"] { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; }
    /* 랭킹 스타일 */
    .rank-card { background: rgba(0, 0, 0, 0.4); border-left: 4px solid #ffaa00; padding: 10px; margin-bottom: 8px; border-radius: 0 8px 8px 0; }
    .rank-1 { border-color: #ffd700; } /* 금 */
    .rank-2 { border-color: #c0c0c0; } /* 은 */
    .rank-3 { border-color: #cd7f32; } /* 동 */
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 화면
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 50px; margin-top: 50px;'>🌌 HYOMIN UNIVERSE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>10가지 다채로운 콘텐츠가 있는 종합 포털입니다.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tab1:
            login_id = st.text_input("아이디")
            login_pw = st.text_input("비밀번호", type="password")
            if st.button("로그인", use_container_width=True):
                users = load_users()
                if login_id in users and users[login_id]['pw'] == login_pw:
                    st.session_state.logged_in_user = login_id
                    st.session_state.global_cash = users[login_id]['cash']
                    st.session_state.inventory = users[login_id]['inventory']
                    st.session_state.equipped_title = users[login_id]['equipped_title']
                    st.session_state.portfolio = users[login_id].get('portfolio', {})
                    st.rerun()
                else: st.error("정보가 일치하지 않습니다.")
        with tab2:
            new_id = st.text_input("새 아이디", key="r_id")
            new_pw = st.text_input("새 비밀번호", type="password", key="r_pw")
            if st.button("가입하기", use_container_width=True):
                users = load_users()
                if new_id in users: st.error("이미 존재하는 아이디입니다.")
                elif len(new_id) < 2 or len(new_pw) < 2: st.warning("2글자 이상 입력하세요.")
                else:
                    users[new_id] = {"pw": new_pw, "cash": 100000000, "inventory": [], "equipped_title": "뉴비", "portfolio": {}}
                    save_users(users)
                    st.success("가입 완료! 로그인해주세요.")
    st.stop()

# ==============================
# 글로벌 주식 데이터 초기화 (다른 탭에서도 랭킹 계산에 필요)
# ==============================
stock_config = [
    {"id": "SAMJI", "name": "삼지전자", "vol": 0.05, "trend": 1.01},
    {"id": "SAMSUNG", "name": "삼성전자", "vol": 0.02, "trend": 1.0},
    {"id": "HYUNDAI", "name": "현대차", "vol": 0.025, "trend": 1.0},
    {"id": "NAVER", "name": "네이버", "vol": 0.03, "trend": 1.0},
    {"id": "KAKAO", "name": "카카오", "vol": 0.035, "trend": 0.99},
    {"id": "KAON", "name": "가온브로드밴드", "vol": 0.06, "trend": 1.02},
    {"id": "HFR", "name": "에이치에프알", "vol": 0.055, "trend": 1.0},
    {"id": "GOODUS", "name": "굿어스데이터", "vol": 0.04, "trend": 1.0}
]

if 'stock_data' not in st.session_state:
    st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(10000, 100000), "history": []} for s in stock_config}
if 'news_feed' not in st.session_state: 
    st.session_state.news_feed = []

# ==============================
# 사이드바 메뉴 & 실시간 랭킹
# ==============================
with st.sidebar:
    st.title("메인 메뉴")
    st.subheader(f"[{st.session_state.equipped_title}] {st.session_state.logged_in_user}")
    st.metric("내 현금 자산", f"₩{st.session_state.global_cash:,}")
    if st.button("로그아웃", use_container_width=True):
        sync_user_data()
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
    st.markdown("---")
    
    menus = [
        "🏠 대시보드", "📈 주식 종합 시장", "⚽ 축구 구단주 매니저", 
        "📡 통신 신호 맞추기", "💻 정보처리기사 모의고사", "🏎️ 레이싱 배팅", 
        "🎰 럭키 슬롯머신", "⛏️ 코인 채굴장", "🛒 슈퍼 상점", "💬 커뮤니티"
    ]
    menu = st.radio("콘텐츠 선택", menus)
    
    st.markdown("---")
    st.markdown("### 🏆 명예의 전당 (실시간 총자산)")
    sync_user_data() # 랭킹 표시 전 내 정보 동기화
    rankings = get_user_rankings()
    
    medals = ["🥇", "🥈", "🥉"]
    for i, rank in enumerate(rankings[:5]): # Top 5까지만 표시
        medal = medals[i] if i < 3 else "🏅"
        rank_class = f"rank-{i+1}" if i < 3 else ""
        is_me = " (나)" if rank['uid'] == st.session_state.logged_in_user else ""
        
        st.markdown(f"""
        <div class='rank-card {rank_class}'>
            <div style='font-size: 14px; font-weight: bold; color: #fff;'>{medal} {rank['uid']}{is_me}</div>
            <div style='font-size: 11px; color: #aaa;'>[{rank['title']}]</div>
            <div style='font-size: 15px; color: #00ff88; text-align: right;'>₩{rank['total']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# 콘텐츠 1: 홈 대시보드
# ==============================
if menu == "🏠 대시보드":
    st.title("대시보드")
    st.markdown("좌측 메뉴에서 10가지 다양한 미니게임과 기능을 즐겨보세요! 모든 자산(Cash)은 연동되어 저장됩니다.")
    st.image("https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80", caption="Cyberpunk City")

# ==============================
# 콘텐츠 2: 주식 종합 시장 (오류 완벽 수정본)
# ==============================
elif menu == "📈 주식 종합 시장":
    st.title("📈 대한민국 주식 종합 시장")
    
    auto_refresh = st.checkbox("🔄 실시간 차트/뉴스 갱신 (3초)")
    if auto_refresh: st.markdown('<meta http-equiv="refresh" content="3">', unsafe_allow_html=True)

    # 주가 변동 엔진
    market_data = []
    for cfg in stock_config:
        sid = cfg['id']
        curr_data = st.session_state.stock_data[sid]
        change_pct = (random.random() - 0.5) * 2 * cfg['vol'] * cfg['trend']
        new_price = max(500, curr_data['price'] * (1 + change_pct))
        curr_data['price'] = round(new_price)
        curr_data['history'].append(curr_data['price'])
        curr_data['history'] = curr_data['history'][-20:]
        
        market_data.append({
            "종목명": curr_data['name'], 
            "현재가": curr_data['price'], 
            "등락률": change_pct * 100
        })
        
        if random.random() < 0.05:
            msg = "어닝 서프라이즈! 기관 대량 매수" if change_pct > 0 else "악재 돌출! 외인 매도세 전환"
            st.session_state.news_feed.insert(0, f"[{curr_data['name']}] {msg}")
            st.session_state.news_feed = st.session_state.news_feed[:5]

    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("📊 시장 전체 현황")
        df_market = pd.DataFrame(market_data)
        
        # Pandas 버전 호환성 완벽 해결 (styler 대신 직접 HTML 렌더링)
        def highlight_row(row):
            color = '#ff4444' if row['등락률'] < 0 else '#00ff88'
            sign = '▲' if row['등락률'] >= 0 else '▼'
            return f"<tr><td style='padding:8px;'>{row['종목명']}</td><td style='padding:8px; text-align:right;'>₩{row['현재가']:,}</td><td style='padding:8px; text-align:right; color:{color}; font-weight:bold;'>{sign} {abs(row['등락률']):.2f}%</td></tr>"

        html_table = "<table style='width:100%; border-collapse: collapse; background:rgba(0,0,0,0.3); border-radius:8px;'>"
        html_table += "<tr style='border-bottom: 1px solid #555;'><th style='padding:8px; text-align:left;'>종목명</th><th style='padding:8px; text-align:right;'>현재가</th><th style='padding:8px; text-align:right;'>등락률</th></tr>"
        for _, row in df_market.iterrows():
            html_table += highlight_row(row)
        html_table += "</table>"
        
        st.markdown(html_table, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📰 실시간 시장 속보")
        for n in st.session_state.news_feed: 
            st.info(n)

    with col2:
        st.subheader("💼 내 계좌 및 거래")
        selected_stock_name = st.selectbox("거래 종목 선택", [s['name'] for s in stock_config])
        sid = next(s['id'] for s in stock_config if s['name'] == selected_stock_name)
        
        # 미니 차트
        df_chart = pd.DataFrame(st.session_state.stock_data[sid]['history'], columns=["가격"])
        fig = px.line(df_chart, y="가격", template="plotly_dark", height=250)
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), xaxis_title="", yaxis_title="")
        fig.update_traces(line_color="#00d4ff")
        st.plotly_chart(fig, use_container_width=True)
        
        curr_price = st.session_state.stock_data[sid]['price']
        owned = st.session_state.portfolio.get(sid, {"qty": 0, "avg_price": 0})
        
        # 평가액 및 수익률 계산
        qty = owned['qty']
        avg_price = owned['avg_price']
        eval_amt = qty * curr_price
        profit = eval_amt - (qty * avg_price)
        profit_pct = ((curr_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
        
        st.markdown(f"**현재가:** <span style='font-size: 24px; color: #00d4ff;'>₩{curr_price:,}</span>", unsafe_allow_html=True)
        st.markdown(f"**보유량:** {qty}주 (평단가: ₩{int(avg_price):,})")
        if qty > 0:
            p_color = "#00ff88" if profit >= 0 else "#ff4444"
            p_sign = "+" if profit >= 0 else ""
            st.markdown(f"**평가액:** ₩{eval_amt:,} / **손익:** <span style='color: {p_color};'>{p_sign}₩{int(profit):,} ({p_sign}{profit_pct:.2f}%)</span>", unsafe_allow_html=True)
        
        trade_qty = st.number_input("수량", min_value=1, value=1)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📈 매수", use_container_width=True):
                cost = trade_qty * curr_price
                if st.session_state.global_cash >= cost:
                    st.session_state.global_cash -= cost
                    new_qty = qty + trade_qty
                    new_avg = ((qty * avg_price) + cost) / new_qty
                    st.session_state.portfolio[sid] = {"qty": new_qty, "avg_price": new_avg}
                    sync_user_data()
                    st.rerun()
                else: st.error("현금이 부족합니다.")
            if st.button("🔥 풀매수", use_container_width=True):
                max_qty = st.session_state.global_cash // curr_price
                if max_qty > 0:
                    cost = max_qty * curr_price
                    st.session_state.global_cash -= cost
                    new_qty = qty + max_qty
                    new_avg = ((qty * avg_price) + cost) / new_qty
                    st.session_state.portfolio[sid] = {"qty": new_qty, "avg_price": new_avg}
                    sync_user_data()
                    st.rerun()
                else: st.error("매수할 현금이 없습니다.")
        with c2:
            if st.button("📉 매도", use_container_width=True):
                if qty >= trade_qty:
                    st.session_state.global_cash += trade_qty * curr_price
                    st.session_state.portfolio[sid]["qty"] -= trade_qty
                    if st.session_state.portfolio[sid]["qty"] == 0:
                         st.session_state.portfolio[sid]["avg_price"] = 0
                    sync_user_data()
                    st.rerun()
                else: st.error("보유량이 부족합니다.")
            if st.button("💸 풀매도", use_container_width=True):
                if qty > 0:
                    st.session_state.global_cash += qty * curr_price
                    st.session_state.portfolio[sid]["qty"] = 0
                    st.session_state.portfolio[sid]["avg_price"] = 0
                    sync_user_data()
                    st.rerun()
                else: st.error("매도할 주식이 없습니다.")

# ==============================
# 콘텐츠 3: 축구 구단주 매니저
# ==============================
elif menu == "⚽ 축구 구단주 매니저":
    st.title("⚽ 축구 구단주 시뮬레이터")
    st.markdown("액션 대신 지략으로 승부합니다! 감독이 되어 전술을 지시하고 시뮬레이션 결과를 확인하세요.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("전술 보드")
        formation = st.selectbox("포메이션", ["4-4-2 (밸런스)", "4-3-3 (공격형)", "5-3-2 (수비형)"])
        playstyle = st.radio("플레이 스타일", ["티키타카 (점유율)", "게겐프레싱 (전방압박)", "선수비 후역습"])
        
        if st.button("경기 시작 (시뮬레이션 돌리기)", use_container_width=True):
            with st.spinner("90분 경기 시뮬레이션 중..."):
                time.sleep(2)
            
            # 승패 확률 계산
            win_prob = 50
            if "4-3-3" in formation and "게겐프레싱" in playstyle: win_prob += 15
            elif "5-3-2" in formation and "선수비" in playstyle: win_prob += 10
            
            result_num = random.randint(1, 100)
            if result_num <= win_prob:
                st.success("🎉 경기 종료: 2 - 1 승리! 관중 수입 ₩3,000,000 획득!")
                st.session_state.global_cash += 3000000
                st.balloons()
            elif result_num <= win_prob + 20:
                st.warning("🤝 경기 종료: 1 - 1 무승부. 관중 수입 ₩1,000,000 획득.")
                st.session_state.global_cash += 1000000
            else:
                st.error("💥 경기 종료: 0 - 2 패배. 수입이 없습니다.")
            sync_user_data()
            
    with col2:
        st.subheader("현재 내 스쿼드 상태")
        st.info("팀 사기: 85%\n\n체력: 90%\n\n팬 만족도: 72%")
        st.markdown("*(향후 상점에서 A급 선수를 영입하여 스쿼드를 강화할 수 있습니다.)*")

# ==============================
# 콘텐츠 4: 통신 신호 맞추기
# ==============================
elif menu == "📡 통신 신호 맞추기":
    st.title("📡 신호 처리 동기화 미니게임")
    st.markdown("수신된 잡음 섞인 신호의 주파수와 진폭을 조정하여 타겟 신호와 완벽하게 동기화하세요!")
    
    if 'target_freq' not in st.session_state:
        st.session_state.target_freq = random.randint(2, 10)
        st.session_state.target_amp = random.randint(2, 10)
        
    col1, col2 = st.columns([1, 2])
    with col1:
        freq = st.slider("주파수 (Frequency)", 1, 15, 5)
        amp = st.slider("진폭 (Amplitude)", 1, 15, 5)
        
        if st.button("신호 검증하기"):
            if freq == st.session_state.target_freq and amp == st.session_state.target_amp:
                st.success("✅ 동기화 완료! 업무 보너스 ₩500,000 획득!")
                st.session_state.global_cash += 500000
                sync_user_data()
                st.session_state.target_freq = random.randint(2, 10)
                st.session_state.target_amp = random.randint(2, 10)
            else:
                st.error("❌ 파형이 일치하지 않습니다. 다시 조율하세요.")
                
    with col2:
        import numpy as np
        x = np.linspace(0, 10, 200)
        y_target = st.session_state.target_amp * np.sin(st.session_state.target_freq * x)
        y_user = amp * np.sin(freq * x)
        
        df_sig = pd.DataFrame({'시간': x, '타겟 신호': y_target, '내 신호': y_user})
        st.plotly_chart(px.line(df_sig, x='시간', y=['타겟 신호', '내 신호'], template='plotly_dark'), use_container_width=True)

# ==============================
# 콘텐츠 5: 정보처리기사 모의고사
# ==============================
elif menu == "💻 정보처리기사 모의고사":
    st.title("💻 정보처리기사 CBT 모의고사")
    st.markdown("자격증 시험 대비! 정답을 맞히면 1문제당 ₩200,000의 장학금이 지급됩니다.")
    
    questions = [
        {"q": "OSI 7계층 중 물리적 매체를 통해 비트 스트림을 전송하는 계층은?", "opts": ["데이터 링크 계층", "물리 계층", "네트워크 계층", "전송 계층"], "a": "물리 계층"},
        {"q": "객체지향 프로그래밍에서 하위 클래스가 상위 클래스의 속성과 메서드를 물려받는 것은?", "opts": ["다형성", "캡슐화", "상속", "추상화"], "a": "상속"},
        {"q": "데이터베이스 이상(Anomaly) 현상의 종류가 아닌 것은?", "opts": ["삽입 이상", "삭제 이상", "갱신 이상", "검색 이상"], "a": "검색 이상"}
    ]
    
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}. {q['q']}**")
        ans = st.radio(f"보기 {i+1}", q['opts'], key=f"q_{i}")
        if st.button(f"{i+1}번 정답 제출", key=f"btn_{i}"):
            if ans == q['a']:
                st.success("정답입니다! ₩200,000 지급 완료.")
                st.session_state.global_cash += 200000
                sync_user_data()
            else:
                st.error("오답입니다. 다시 복습해보세요!")

# ==============================
# 콘텐츠 6: 레이싱 배팅
# ==============================
elif menu == "🏎️ 레이싱 배팅":
    st.title("🏎️ 레이싱 우승자 맞추기")
    
    cars = ["🚗 2021년식 레이", "🏎️ 페라리", "🚙 포르쉐", "🚜 트랙터"]
    bet_car = st.selectbox("어떤 차가 우승할까요?", cars)
    bet_amount = st.number_input("배팅 금액", min_value=10000, max_value=max(10000, st.session_state.global_cash), step=10000)
    
    if st.button("레이스 시작!"):
        if st.session_state.global_cash >= bet_amount:
            st.session_state.global_cash -= bet_amount
            progress_bars = [st.progress(0, text=car) for car in cars]
            positions = [0, 0, 0, 0]
            
            winner = -1
            while winner == -1:
                for i in range(4):
                    positions[i] += random.randint(1, 15)
                    if positions[i] >= 100:
                        positions[i] = 100
                        winner = i
                    progress_bars[i].progress(positions[i], text=cars[i])
                time.sleep(0.1)
                
            winning_car = cars[winner]
            st.markdown(f"### 🏁 우승: {winning_car}!")
            
            if bet_car == winning_car:
                st.success(f"예측 성공! 배팅 금액의 3배인 ₩{bet_amount * 3:,} 획득!")
                st.session_state.global_cash += bet_amount * 3
            else:
                st.error("예측 실패. 배팅 금액을 잃었습니다.")
            sync_user_data()
        else:
            st.error("배팅 금액이 보유 자산을 초과합니다.")

# ==============================
# 콘텐츠 7: 럭키 슬롯머신
# ==============================
elif menu == "🎰 럭키 슬롯머신":
    st.title("🎰 럭키 슬롯머신")
    st.markdown("1회전 당 ₩100,000. 3개가 일치하면 ₩5,000,000 잭팟!")
    
    if st.button("🕹️ 레버 당기기 (₩100,000)"):
        if st.session_state.global_cash >= 100000:
            st.session_state.global_cash -= 100000
            emojis = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
            with st.empty():
                for _ in range(10):
                    r1, r2, r3 = random.choice(emojis), random.choice(emojis), random.choice(emojis)
                    st.markdown(f"<h1 style='text-align:center; font-size:80px;'>[ {r1} | {r2} | {r3} ]</h1>", unsafe_allow_html=True)
                    time.sleep(0.1)
            
            if r1 == r2 == r3:
                st.success("🎉 JACKPOT!!! ₩5,000,000 획득!")
                st.session_state.global_cash += 5000000
                st.balloons()
            else:
                st.error("아쉽습니다. 다음 기회에!")
            sync_user_data()
        else:
            st.error("현금이 부족합니다.")

# ==============================
# 콘텐츠 8: 코인 채굴장
# ==============================
elif menu == "⛏️ 코인 채굴장":
    st.title("⛏️ 가상화폐 수동 채굴장")
    st.markdown("클릭할 때마다 돈이 벌립니다. 단순하지만 확실한 노동의 대가!")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("💻 열심히 타자 치기 (클릭)", use_container_width=True):
            st.session_state.global_cash += 15000
            st.success("+₩15,000 획득")
            sync_user_data()
            
    with col2:
        st.info("광클릭으로 자본금을 모아 주식 시장이나 상점, 슬롯머신을 이용해 보세요.")

# ==============================
# 콘텐츠 9: 슈퍼 상점
# ==============================
elif menu == "🛒 슈퍼 상점":
    st.title("🛒 하이엔드 슈퍼 상점")
    st.markdown("자산을 모아 부와 명예를 보여주는 칭호와 물건을 구매하세요.")
    
    items = [
        {"id": "i1", "name": "VHDL 마스터 칭호", "price": 2000000, "type": "title"},
        {"id": "i2", "name": "시스템 개발팀장 칭호", "price": 10000000, "type": "title"},
        {"id": "i3", "name": "힐스테이트 푸르지오 아파트", "price": 800000000, "type": "property"},
        {"id": "i4", "name": "초고성능 PXI 계측 장비", "price": 50000000, "type": "tech"}
    ]
    
    for item in items:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{item['name']}** - ₩{item['price']:,}")
        with col2:
            if item['id'] in st.session_state.inventory:
                if item['type'] == 'title':
                    if st.session_state.equipped_title == item['name']:
                        st.button("장착 중", key=item['id'], disabled=True)
                    else:
                        if st.button("칭호 장착", key=item['id']):
                            st.session_state.equipped_title = item['name']
                            sync_user_data()
                            st.rerun()
                else:
                    st.button("보유 중", key=item['id'], disabled=True)
            else:
                if st.button("구매", key=item['id']):
                    if st.session_state.global_cash >= item['price']:
                        st.session_state.global_cash -= item['price']
                        st.session_state.inventory.append(item['id'])
                        sync_user_data()
                        st.success("구매 완료!")
                        st.rerun()
                    else: st.error("현금 부족")
        st.markdown("---")

# ==============================
# 콘텐츠 10: 커뮤니티
# ==============================
elif menu == "💬 커뮤니티":
    st.title("💬 유저 커뮤니티")
    
    c_text = st.text_area("방명록 / 피드백 남기기")
    if st.button("등록하기"):
        save_comment(st.session_state.logged_in_user, c_text)
        st.success("등록 완료")
        st.rerun()
        
    for c in reversed(load_comments()):
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; margin-bottom:10px;'>
            <span style='color:#00d4ff; font-weight:bold;'>{c['name']}</span> <span style='font-size:12px; color:#aaa;'>({c['time']})</span><br>
            {c['comment']}
        </div>
        """, unsafe_allow_html=True)
