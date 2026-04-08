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
MARKET_FILE = "market_db.json" 

stock_config = [
    {"id": "NDX", "name": "나스닥100 ETF", "vol": 0.04},       
    {"id": "HDEC", "name": "현대건설", "vol": 0.03},            
    {"id": "MANU", "name": "맨체스터 유나이티드", "vol": 0.06}, 
    {"id": "CJENM", "name": "CJ ENM", "vol": 0.04},             
    {"id": "FOOD", "name": "삼양식품", "vol": 0.03},            
    {"id": "BIO", "name": "삼성바이오로직스", "vol": 0.05},     
    {"id": "AERO", "name": "한화에어로스페이스", "vol": 0.06},  
    {"id": "RETAIL", "name": "신세계", "vol": 0.02},            
    {"id": "CHEM", "name": "LG화학", "vol": 0.03},              
    {"id": "ENTER", "name": "하이브", "vol": 0.07}              
]

# 부동산 매물 설정 (초당 수익)
estate_config = {
    "E1": {"name": "역세권 원룸", "price": 10000000000, "income": 10000},       # 100억, 초당 1만
    "E2": {"name": "초대형 PC방", "price": 50000000000, "income": 50000},       # 500억, 초당 5만
    "E3": {"name": "강남 꼬마빌딩", "price": 500000000000, "income": 500000},    # 5천억, 초당 50만
    "E4": {"name": "시그니엘 펜트하우스", "price": 5000000000000, "income": 5000000} # 5조, 초당 500만
}

def load_db(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return default
    return default

def save_db(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return 0
    u_data = users[uid]
    wealth = u_data.get('cash', 0) - u_data.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u_data.get('portfolio', {}).items():
        if sid in prices: wealth += p_data.get('qty', 0) * prices[sid]
    for eid, count in u_data.get('real_estate', {}).items():
        if eid in estate_config: wealth += estate_config[eid]['price'] * count * 0.8 # 부동산은 자산 가치 80% 인정
    return wealth

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
                'real_estate': st.session_state.real_estate,
                'rent_time': st.session_state.rent_time,
                'loan': st.session_state.loan,
                'loan_time': st.session_state.loan_time
            })
            save_db(USERS_FILE, users)

def get_market():
    def init_market():
        data = {
            "version": 4, 
            "stock_data": {},
            "news": "시장이 안정적으로 운영 중입니다.",
            "news_time": time.time(),
            "last_tick": time.time(),
            "admin_msg": "",
            "lotto_pool": 5000000000, # 로또 기본 상금 50억
            "lotto_tickets": {}, 
            "lotto_last_draw": time.time(),
            "next_news_target": random.choice(stock_config)['id'],
            "next_news_impact": random.uniform(-0.2, 0.2)
        }
        for s in stock_config:
            p = random.randint(50000, 150000)
            data["stock_data"][s['id']] = {"name": s['name'], "price": p, "history": [p]}
        return data

    if not os.path.exists(MARKET_FILE):
        data = init_market()
        save_db(MARKET_FILE, data)
        return data
        
    data = load_db(MARKET_FILE, {})
    db_keys = set(data.get('stock_data', {}).keys())
    c_keys = set([s['id'] for s in stock_config])
    if data.get("version") != 4 or db_keys != c_keys:
        data = init_market()
        save_db(MARKET_FILE, data)
        return data
    return data

def save_market(data): save_db(MARKET_FILE, data)

def get_rankings(market_data):
    users = load_db(USERS_FILE, {})
    rankings = []
    for uid in users: rankings.append({"uid": uid, "total": get_net_worth(uid, market_data)})
    rankings.sort(key=lambda x: x['total'], reverse=True)
    return rankings

st.set_page_config(page_title="HYOMIN UNIVERSE v14.0", page_icon="👑", layout="wide")

# ==============================
# 🔐 로그인 시스템
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
    st.markdown("<p>자본주의 끝판왕: 부동산, 대출, 로또 시스템 대규모 업데이트!</p>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("💻 접속 환경 선택", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        st.write("---")
        
        choice = st.tabs(["🔑 로그인", "📝 시민등록"])
        with choice[0]:
            l_id, l_pw = st.text_input("아이디"), st.text_input("비밀번호", type="password")
            if st.button("유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {"pw": "5891", "cash": 999999999999, "inventory": [], "equipped_title": "👑 절대신 창조주", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                        save_db(USERS_FILE, users)
                    st.session_state.update({
                        'logged_in_user': "5891", 'global_cash': users["5891"]['cash'], 'inventory': users["5891"]['inventory'],
                        'equipped_title': users["5891"].get('equipped_title', '👑 절대신 창조주'), 'portfolio': users["5891"].get('portfolio', {}),
                        'real_estate': users["5891"].get('real_estate', {}), 'rent_time': users["5891"].get('rent_time', time.time()),
                        'loan': users["5891"].get('loan', 0), 'loan_time': users["5891"].get('loan_time', time.time()),
                        'device_mode': device_mode
                    }); st.rerun()
                elif l_id in users and users[l_id]['pw'] == l_pw:
                    st.session_state.update({
                        'logged_in_user': l_id, 'global_cash': users[l_id]['cash'], 'inventory': users[l_id]['inventory'],
                        'equipped_title': users[l_id].get('equipped_title', '신규시민'), 'portfolio': users[l_id].get('portfolio', {}),
                        'real_estate': users[l_id].get('real_estate', {}), 'rent_time': users[l_id].get('rent_time', time.time()),
                        'loan': users[l_id].get('loan', 0), 'loan_time': users[l_id].get('loan_time', time.time()),
                        'device_mode': device_mode
                    }); st.rerun()
                else: st.error("정보가 일치하지 않습니다.")
                
        with choice[1]:
            n_id, n_pw = st.text_input("새 아이디"), st.text_input("새 비밀번호", type="password")
            if st.button("시민 등록", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "5891": st.error("사용할 수 없는 이름입니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100000000, "inventory": [], "equipped_title": "신규시민", "portfolio": {}, "real_estate": {}, "rent_time": time.time(), "loan": 0, "loan_time": time.time()}
                    save_db(USERS_FILE, users); st.success("가입 성공! 로그인하세요.")
    st.stop()

# ==============================
# 🎨 동적 CSS 적용 (PC vs Mobile)
# ==============================
css_common = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@700;900&display=swap');
    .stApp { background-color: #050505 !important; }
    html, body, [class*="css"], .stMarkdown, p, span, li, label { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; font-weight: 700 !important; }
    div[data-baseweb="select"] > div { background-color: #1A1C24 !important; border: 2px solid #00E5FF !important; }
    div[data-baseweb="select"] * { color: #FFFFFF !important; font-weight: 900 !important; }
    div[data-baseweb="popover"] * { background-color: #1A1C24 !important; color: #00FF88 !important; }
    .stNumberInput input { background-color: #222 !important; color: #00FF88 !important; }
    .stock-table { width: 100%; border-collapse: collapse; background-color: #111; border: 2px solid #444; }
    .stock-table th { background-color: #333; color: #FFD600 !important; text-align: center; }
    .stock-table td { border-bottom: 1px solid #333; text-align: center; }
    .p-up { color: #FF4B4B !important; font-weight: 900; }
    .p-down { color: #1F77B4 !important; font-weight: 900; }
    .stButton>button:hover { background-color: #00E5FF !important; color: #000 !important; }
"""
if st.session_state.device_mode == "🖥️ PC (데스크탑)":
    st.markdown(f"<style>{css_common} html, body, * {{ font-size: 20px !important; }} h1 {{ font-size: 3.5rem !important; color: #00E5FF !important; text-align: center; }} h2 {{ font-size: 2.5rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }} .stButton>button {{ height: 70px !important; border: 3px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; font-size: 24px !important; font-weight: 900 !important; border-radius: 12px; width: 100%; }} .slot-text {{ text-align: center; font-weight: 900; font-size: 100px !important; margin: 0; padding: 10px; }} [data-testid='stSidebar'] {{ background-color: #001F3F !important; border-right: 4px solid #00E5FF; }}</style>", unsafe_allow_html=True)
else:
    st.markdown(f"<style>{css_common} html, body, * {{ font-size: 14px !important; }} h1 {{ font-size: 2rem !important; color: #00E5FF !important; text-align: center; }} h2 {{ font-size: 1.5rem !important; color: #00FF88 !important; border-bottom: 2px solid #00FF88; }} .stButton>button {{ height: 50px !important; border: 2px solid #00E5FF !important; background-color: #1A1C24 !important; color: #00E5FF !important; font-size: 16px !important; font-weight: 900 !important; border-radius: 8px; width: 100%; }} .slot-text {{ text-align: center; font-weight: 900; font-size: 50px !important; margin: 0; padding: 10px; }}</style>", unsafe_allow_html=True)

# ==============================
# 🌐 통합 글로벌 시장 동기화 & 백그라운드 연산
# ==============================
market = get_market()
current_time = time.time()
market_updated = False

# 1. 10초 주가 자동 변동
if current_time - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]
        change = (random.random()-0.5) * 2 * s['vol']
        curr['price'] = round(max(1000, curr['price'] * (1 + change)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 30: curr['history'].pop(0)
    market['last_tick'] = current_time
    market_updated = True

# 2. 30초 정규 뉴스 (내부자 정보 적용)
if current_time - market.get('news_time', 0) > 30:
    target_id = market['next_news_target']
    impact = market['next_news_impact']
    t_name = [s['name'] for s in stock_config if s['id'] == target_id][0]
    
    market['stock_data'][target_id]['price'] = int(market['stock_data'][target_id]['price'] * (1 + impact))
    market['news'] = f"📰 [정규속보] {t_name}, {'어닝 서프라이즈로 시장 기대감 상승!' if impact > 0 else '실적 부진으로 투자심리 위축'}"
    market['news_time'] = current_time
    
    # VIP를 위한 '다음 뉴스' 세팅
    market['next_news_target'] = random.choice(stock_config)['id']
    market['next_news_impact'] = random.uniform(-0.25, 0.25)
    market_updated = True

# 3. 로또 5분 추첨 로직
if current_time - market.get('lotto_last_draw', 0) > 3600: # 3600초 = 1시
    if market['lotto_tickets']:
        tickets = []
        for uid, count in market['lotto_tickets'].items(): tickets.extend([uid] * count)
        winner = random.choice(tickets)
        prize = market['lotto_pool']
        
        users = load_db(USERS_FILE, {})
        if winner in users:
            users[winner]['cash'] += prize
            save_db(USERS_FILE, users)
            if winner == st.session_state.logged_in_user: st.session_state.global_cash += prize
        market['news'] = f"🎉 [잭팟] {winner}님이 글로벌 로또에 당첨되어 ₩{prize//100000000:,}억을 독식했습니다!!"
    market['lotto_pool'] = 50000000000 # 리셋 (기본금 500억)
    market['lotto_tickets'] = {}
    market['lotto_last_draw'] = current_time
    market_updated = True

if market_updated: save_market(market)

# 4. 내 대출 이자 및 신용불량자 체크 로직 (접속 시마다 연산)
if st.session_state.loan > 0:
    loan_cycles = int((current_time - st.session_state.loan_time) / 10)
    if loan_cycles > 0:
        st.session_state.loan = int(st.session_state.loan * (1.02 ** loan_cycles)) # 10초당 2% 이자
        st.session_state.loan_time += loan_cycles * 10
        sync_user_data()

net_worth = get_net_worth(st.session_state.logged_in_user, market)
if st.session_state.loan > 0 and net_worth < 0:
    st.session_state.equipped_title = "💸 신용불량자"
    sync_user_data()

# ==============================
# 🧭 메뉴 구성
# ==============================
menu_options = ["🏠 홈 광장", "📈 주식 트레이딩", "🏢 부동산 경매 (수금)", "🏦 대출 & 송금 은행", "⚔️ 5분 글로벌 로또", "⚽ 구단주 매니저", "💻 CBT 모의고사", "🏎️ 레이싱", "🎰 슬롯머신", "👑 칭호 상점", "💬 랭커 게시판"]

# VIP 전용 메뉴 추가 (순자산 1000억 이상)
if net_worth >= 100000000000 or st.session_state.logged_in_user == "5891":
    menu_options.insert(2, "💎 VIP 시크릿 라운지")

if st.session_state.logged_in_user == "5891":
    menu_options.append("🛠️ 창조주 통제소")

if "🖥️" in st.session_state.device_mode:
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.logged_in_user}")
        st.markdown(f"**칭호**: `{st.session_state.equipped_title}`")
        st.metric("💰 보유 현금", f"₩{st.session_state.global_cash:,}")
        st.metric("💳 대출 (빚)", f"₩{st.session_state.loan:,}", delta="-2%/10초" if st.session_state.loan>0 else "")
        if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        st.markdown("---")
        menu = st.radio("포털 이동", menu_options)
        st.markdown("---")
        st.markdown("### 🏆 서버 통합 랭킹 (순자산)")
        for i, r in enumerate(get_rankings(market)[:3]): st.write(f"{['🥇','🥈','🥉'][i]} {r['uid']}: ₩{r['total']:,.0f}")
else:
    st.markdown(f"<div style='text-align:right; color:#FFD600;'>👤 <b>{st.session_state.logged_in_user}</b> <br> 🎖️ {st.session_state.equipped_title} <br> 💰 <b>₩{st.session_state.global_cash:,}</b> | 빚: ₩{st.session_state.loan:,}</div>", unsafe_allow_html=True)
    menu = st.selectbox("📌 이동할 메뉴를 선택하세요", menu_options)
    with st.expander("🏆 통합 랭킹 보기"):
        for i, r in enumerate(get_rankings(market)[:5]):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else "🏅"
            st.write(f"{medal} **{r['uid']}**: ₩{r['total']:,.0f}")
        if st.button("🔴 로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()

# 공통 UI: 긴급 공지
if market.get('admin_msg') and menu in ["🏠 홈 광장", "📈 주식 트레이딩"]:
    st.markdown(f"<div style='background-color:#500000; border:3px solid #FF0000; padding:15px; border-radius:10px; margin-bottom:20px; text-align:center;'><h2 style='color:#FFFFFF; margin:0;'>👑 [창조주 긴급 공지] {market['admin_msg']}</h2></div>", unsafe_allow_html=True)

# ==============================
# [1] 홈
# ==============================
if menu == "🏠 홈 광장":
    st.title(f"환영합니다 {st.session_state.logged_in_user}님! 🎉")
    st.markdown("부동산으로 월세를 받고, 빚을 내어 주식에 투자하세요. 파산하면 신용불량자가 됩니다!")
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200")
    if st.session_state.logged_in_user == "5891":
        if st.button("비상금 10억 인출하기"): st.session_state.global_cash += 1000000000; sync_user_data(); st.rerun()

# ==============================
# 💎 [VIP 시크릿 라운지]
# ==============================
elif menu == "💎 VIP 시크릿 라운지":
    st.title("💎 VIP 시크릿 라운지")
    st.markdown("자산 1000억 이상 최상위 랭커만 들어올 수 있는 비밀 라운지입니다.")
    st.warning("⚠️ 내부자 정보는 절대 외부 게시판에 유출하지 마세요.")
    
    t_name = [s['name'] for s in stock_config if s['id'] == market['next_news_target']][0]
    imp = market['next_news_impact'] * 100
    st.info(f"🕵️ **[내부자 정보]** 다음 뉴스(최대 30초 뒤) 타겟은 **'{t_name}'** 이며, 주가는 **약 {imp:+.1f}%** 변동할 예정입니다.")
    
    st.markdown("---")
    st.subheader("🎰 VIP 전용 하이리스크 슬롯머신 (승률 50%)")
    st.markdown("1억을 넣고 당첨되면 2억을 받습니다.")
    if st.button("🎰 1억 베팅 (VIP 슬롯)"):
        if st.session_state.global_cash >= 100000000:
            st.session_state.global_cash -= 100000000
            if random.random() < 0.50:
                st.session_state.global_cash += 200000000
                st.success("🎉 당첨!! 2억 회수 완료!")
            else: st.error("❌ 꽝... 1억 증발.")
            sync_user_data()
        else: st.error("현금이 부족합니다.")

# ==============================
# [2] 주식
# ==============================
elif menu == "📈 주식 트레이딩":
    st.title("📈 글로벌 통합 거래소")
    news_color = "#FF4B4B" if "폭등" in market['news'] or "창조주" in market['news'] else "#1F77B4" if "폭락" in market['news'] else "#FFD600"
    st.markdown(f"<div style='background-color:#222; padding:15px; border-left:10px solid {news_color}; margin-bottom:20px;'><h3 style='color:{news_color}; margin:0;'>{market['news']}</h3></div>", unsafe_allow_html=True)
    
    t_mkt, t_acc = st.tabs(["📊 시황", "💼 내 포트폴리오"])
    with t_mkt:
        rows = ""
        for s in stock_config:
            curr = market['stock_data'][s['id']]
            diff = curr['price'] - curr['history'][-2] if len(curr['history']) > 1 else 0
            pct = (diff / curr['history'][-2]) * 100 if len(curr['history']) > 1 else 0
            cls, sign = ("p-up", "▲") if diff >= 0 else ("p-down", "▼")
            rows += f"<tr><td>{curr['name']}</td><td>₩{curr['price']:,}</td><td class='{cls}'>{sign} {abs(pct):.2f}%</td></tr>"
        st.markdown(f"<table class='stock-table'><tr><th>종목</th><th>현재가</th><th>변동</th></tr>{rows}</table>", unsafe_allow_html=True)
        
    with t_acc:
        st.subheader("보유 계좌")
        p_list, total_eval = [], 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp, ap = market['stock_data'][sid]['price'], info.get('avg_price', 0)
                eval_amt = qty * cp; total_eval += eval_amt
                roi = ((cp - ap) / ap * 100) if ap > 0 else 0
                p_list.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주", "평가액": f"₩{int(eval_amt):,}", "수익률": f"{roi:+.2f}%"})
        if p_list: st.table(pd.DataFrame(p_list))
        else: st.info("주식을 매수해보세요!")
        st.markdown(f"💰 주식자산: ₩{total_eval:,} | 💵 현금: ₩{st.session_state.global_cash:,}")

    st.write("---")
    sel_name = st.selectbox("매매할 종목을 고르세요", [s['name'] for s in stock_config])
    sid = [s['id'] for s in stock_config if s['name'] == sel_name][0]
    st.plotly_chart(px.line(y=market['stock_data'][sid]['history'], template="plotly_dark", height=250), use_container_width=True)
    cp = market['stock_data'][sid]['price']
    st.markdown(f"<h2 style='text-align:center;'>현재가: ₩{cp:,}</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💥 풀매수"):
            max_q = st.session_state.global_cash // cp
            buy_amt = max_q * cp
            if max_q > 0:
                st.session_state.global_cash -= buy_amt
                old = st.session_state.portfolio.get(sid, {'qty':0, 'avg_price':0})
                new_q = old['qty'] + max_q
                new_a = ((old['qty'] * old['avg_price']) + buy_amt) / new_q
                st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                sync_user_data()
                if buy_amt >= 1000000000:
                    impact = min((buy_amt / 100000000000) * 0.1, 0.5) 
                    market['stock_data'][sid]['price'] = int(cp * (1 + impact))
                    market['news'] = f"🚨 [고래 출현] {st.session_state.equipped_title} {st.session_state.logged_in_user}님이 {sel_name} ₩{buy_amt//100000000:,}억 풀매수!! 주가 폭등!"
                    market['news_time'] = time.time(); save_market(market)
                st.rerun()
    with c2:
        if st.button("💸 풀매도"):
            owned = st.session_state.portfolio.get(sid, {'qty':0})['qty']
            sell_amt = owned * cp
            if owned > 0:
                st.session_state.global_cash += sell_amt
                st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                sync_user_data()
                if sell_amt >= 1000000000:
                    impact = min((sell_amt / 100000000000) * 0.1, 0.5)
                    market['stock_data'][sid]['price'] = max(1000, int(cp * (1 - impact)))
                    market['news'] = f"📉 [패닉 셀] 대주주 {st.session_state.logged_in_user}님이 {sel_name} ₩{sell_amt//100000000:,}억 물량 투하!! 주가 폭락!"
                    market['news_time'] = time.time(); save_market(market)
                st.rerun()
    time.sleep(2); st.rerun()

# ==============================
# 🏢 [3] 부동산 (건물주 시스템)
# ==============================
elif menu == "🏢 부동산 경매 (수금)":
    st.title("🏢 부동산 경매소")
    st.markdown("건물을 사두면 접속하지 않아도 1초마다 월세가 누적됩니다.")
    
    # 1. 수금 로직
    uncollected = 0
    now = time.time()
    passed_sec = int(now - st.session_state.rent_time)
    for eid, count in st.session_state.real_estate.items():
        if eid in estate_config:
            uncollected += estate_config[eid]['income'] * count * passed_sec
            
    st.markdown(f"<div style='background-color:#001F3F; padding:20px; border-radius:10px; text-align:center;'><h2>누적된 월세 수익: ₩{uncollected:,}</h2></div>", unsafe_allow_html=True)
    if st.button("💰 수금하기 (일괄 회수)"):
        st.session_state.global_cash += uncollected
        st.session_state.rent_time = now
        sync_user_data(); st.success(f"₩{uncollected:,}을 수금했습니다!"); st.rerun()
        
    st.write("---")
    st.subheader("매물 목록 및 구매")
    for eid, info in estate_config.items():
        c1, c2 = st.columns([3, 1])
        c1.write(f"**{info['name']}** | 가격: ₩{info['price']:,} | 수익: 초당 +₩{info['income']:,}")
        owned_cnt = st.session_state.real_estate.get(eid, 0)
        c1.caption(f"보유 수량: {owned_cnt}채 (초당 +₩{info['income'] * owned_cnt:,})")
        if c2.button(f"매입하기", key=f"buy_est_{eid}"):
            if st.session_state.global_cash >= info['price']:
                # 구매 전 이전까지의 수익 강제 수금 및 정산
                st.session_state.global_cash += uncollected
                st.session_state.global_cash -= info['price']
                st.session_state.real_estate[eid] = owned_cnt + 1
                st.session_state.rent_time = time.time()
                sync_user_data(); st.rerun()
            else: st.error("현금이 부족합니다.")

# ==============================
# 🏦 [4] 은행 (송금 & 대출)
# ==============================
elif menu == "🏦 대출 & 송금 은행":
    st.title("🏦 하이리스크 은행")
    
    t_trans, t_loan = st.tabs(["💸 친구에게 송금", "💳 신용 대출"])
    
    with t_trans:
        st.subheader("계좌 이체")
        target_uid = st.text_input("받는 사람 아이디 입력")
        send_amt = st.number_input("송금할 금액", min_value=10000, step=10000)
        if st.button("💸 송금하기"):
            users = load_db(USERS_FILE, {})
            if target_uid not in users: st.error("존재하지 않는 유저입니다.")
            elif target_uid == st.session_state.logged_in_user: st.error("자신에게 보낼 수 없습니다.")
            elif st.session_state.global_cash < send_amt: st.error("잔액이 부족합니다.")
            else:
                st.session_state.global_cash -= send_amt
                users[target_uid]['cash'] += send_amt
                users[st.session_state.logged_in_user]['cash'] = st.session_state.global_cash
                save_db(USERS_FILE, users); st.success(f"{target_uid}님에게 ₩{send_amt:,} 송금 완료!"); st.rerun()
                
    with t_loan:
        st.subheader("신용 대출 (이자: 10초당 2% 복리)")
        st.warning("⚠️ 파산 시 '신용불량자' 칭호가 박제됩니다.")
        st.metric("현재 나의 대출금", f"₩{st.session_state.loan:,}")
        
        c1, c2 = st.columns(2)
        with c1:
            loan_amt = st.number_input("대출받을 금액", min_value=0, step=100000000)
            if st.button("💳 대출 실행"):
                if loan_amt > 0:
                    st.session_state.global_cash += loan_amt
                    if st.session_state.loan == 0: st.session_state.loan_time = time.time()
                    st.session_state.loan += loan_amt
                    sync_user_data(); st.success(f"₩{loan_amt:,} 대출 승인!"); st.rerun()
        with c2:
            repay_amt = st.number_input("상환할 금액", min_value=0, step=100000000)
            if st.button("💵 빚 갚기"):
                if repay_amt > 0 and st.session_state.global_cash >= repay_amt:
                    actual_repay = min(repay_amt, st.session_state.loan)
                    st.session_state.global_cash -= actual_repay
                    st.session_state.loan -= actual_repay
                    if st.session_state.loan == 0 and st.session_state.equipped_title == "💸 신용불량자":
                        st.session_state.equipped_title = "신규시민" # 빚 청산 시 칭호 해제
                    sync_user_data(); st.success(f"₩{actual_repay:,} 상환 완료!"); st.rerun()
                else: st.error("현금이 부족합니다.")

# ==============================
# ⚔️ [5] 글로벌 로또
# ==============================
elif menu == "⚔️ 5분 글로벌 로또":
    st.title("⚔️ 글로벌 잭팟 복권")
    st.markdown("모든 유저의 구매금이 누적되며 **5분마다 단 1명**이 독식합니다!")
    st.markdown(f"<h1 style='color:#FFD600;'>현재 누적 상금: ₩{market['lotto_pool']:,}</h1>", unsafe_allow_html=True)
    
    my_tix = market['lotto_tickets'].get(st.session_state.logged_in_user, 0)
    total_tix = sum(market['lotto_tickets'].values())
    win_rate = (my_tix / total_tix * 100) if total_tix > 0 else 0
    st.write(f"내 티켓: **{my_tix}장** (당첨 확률: **{win_rate:.2f}%**)")
    
    buy_cnt = st.number_input("구매할 티켓 수량 (장당 1,000만 원)", min_value=1, step=1)
    if st.button("🎟️ 티켓 구매하기"):
        cost = buy_cnt * 10000000
        if st.session_state.global_cash >= cost:
            st.session_state.global_cash -= cost
            market['lotto_pool'] += cost
            market['lotto_tickets'][st.session_state.logged_in_user] = my_tix + buy_cnt
            save_market(market); sync_user_data(); st.success(f"{buy_cnt}장 구매 완료!"); st.rerun()
        else: st.error("현금이 부족합니다.")
    
    remain_sec = int(300 - (current_time - market.get('lotto_last_draw', 0)))
    st.info(f"⏳ 다음 추첨까지 약 {remain_sec}초 남았습니다.")
    time.sleep(2); st.rerun() # 실시간 갱신

# [기타 메뉴들은 기존 V13과 동일. 구단주, 통신업무 생략 없이 포함]
elif menu == "⚽ 구단주 매니저":
    st.title("🏆 구단주 시뮬레이터")
    form = st.selectbox("포메이션", ["4-4-2", "4-3-3", "3-5-2", "5-4-1"])
    if st.button("🏟️ 경기 시작 (30초)"):
        b = st.empty(); p = st.progress(0)
        h, a = 0, 0
        for i in range(30):
            if random.random() < 0.08: h += 1
            if random.random() < 0.05: a += 1
            b.markdown(f"<div class='slot-text' style='background:#000; border:2px solid #00FF88;'>{h} : {a}</div>", unsafe_allow_html=True)
            p.progress((i+1)/30); time.sleep(1)
        res = 5000000 if h > a else 1000000 if h == a else 100000
        st.session_state.global_cash += res; sync_user_data(); st.success(f"정산: +₩{res:,}")

elif menu == "💻 CBT 모의고사":
    st.title("💻 정처기 실전 모의고사")
    if 'hard_q_pool' not in st.session_state:
        st.session_state.hard_q_pool = [
            {"q": "결합도(Coupling) 중 가장 좋은 것은?", "a": "자료 결합도", "w": ["스탬프 결합도", "제어 결합도", "내용 결합도"]},
            {"q": "DB 제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행적 함수 종속 제거", "다치 종속 제거", "결정자 문제"]}
        ]
    if 'current_q' not in st.session_state:
        st.session_state.current_q = random.choice(st.session_state.hard_q_pool)
        opts = st.session_state.current_q['w'] + [st.session_state.current_q['a']]
        random.shuffle(opts)
        st.session_state.current_opts = opts
    with st.form("exam"):
        st.markdown(f"<h2 style='color:#FFD600;'>Q. {st.session_state.current_q['q']}</h2>", unsafe_allow_html=True)
        ans = st.radio("정답 선택:", st.session_state.current_opts)
        if st.form_submit_button("제출"):
            if ans == st.session_state.current_q['a']: st.session_state.global_cash += 500000; st.success("정답! +50만")
            else: st.error("오답!")
            del st.session_state.current_q; sync_user_data(); st.rerun()

elif menu == "🏎️ 레이싱":
    st.title("🏎️ 역배 챔피언십")
    cars = [{"n":"🚗 레이 (15배)", "o":15.0}, {"n":"🏎️ 페라리 (1.5배)", "o":1.5}, {"n":"🚜 트랙터 (30배)", "o":30.0}]
    sel = st.selectbox("배팅 차량", [c['n'] for c in cars])
    amt = st.number_input("배팅액", min_value=10000, step=10000)
    if st.button("🏁 RACE START"):
        if st.session_state.global_cash >= amt:
            st.session_state.global_cash -= amt; bars = [st.progress(0, text=c['n']) for c in cars]; pos = [0]*3
            while max(pos) < 100:
                for i in range(3): pos[i] += random.randint(1, 12); bars[i].progress(min(pos[i], 100))
                time.sleep(0.1)
            win = cars[pos.index(max(pos))]
            if win['n'] == sel: st.session_state.global_cash += int(amt * win['o']); st.success("승리!")
            else: st.error("패배"); sync_user_data()

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

elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    if st.session_state.equipped_title == "💸 신용불량자":
        st.error("신용불량자는 칭호를 변경하거나 장착할 수 없습니다. 빚부터 갚으세요!")
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id = f"title_{i}"
            price = i * 10000000
            st.markdown(f"**{title_name}** | ₩{price:,}")
            if title_id in st.session_state.inventory:
                if st.session_state.equipped_title == title_name: st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"):
                        if st.session_state.equipped_title != "💸 신용불량자":
                            st.session_state.equipped_title = title_name; sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        st.session_state.global_cash -= price; st.session_state.inventory.append(title_id)
                        if st.session_state.equipped_title != "💸 신용불량자": st.session_state.equipped_title = title_name
                        sync_user_data(); st.rerun()

elif menu == "💬 랭커 게시판":
    st.title("💬 랭커 게시판")
    msg = st.text_input("메시지 입력")
    if st.button("등록") and msg:
        new_comment = {"name": st.session_state.logged_in_user, "title": st.session_state.equipped_title, "comment": msg, "time": datetime.now().strftime("%m-%d %H:%M")}
        save_db(COMMENTS_FILE, load_db(COMMENTS_FILE, []) + [new_comment]); st.rerun()
    for c in reversed(load_db(COMMENTS_FILE, [])):
        title_color = "#FF4B4B" if c.get('title') == "💸 신용불량자" else "#FFD600"
        st.markdown(f"""
        <div style='background-color: #111; border-left: 5px solid #00FF88; padding: 15px; margin-bottom: 15px; border-radius: 8px;'>
            <div style='margin-bottom: 8px;'>
                <span style='background-color: #222; color: {title_color}; border: 1px solid {title_color}; padding: 3px 8px; border-radius: 5px; font-size: 14px; margin-right: 10px;'>{c.get('title', '신규시민')}</span>
                <b style='color: #00E5FF; font-size: 20px;'>{c['name']}</b>
            </div>
            <div style='color: #FFF; font-size: 18px; margin-left: 5px;'>{c['comment']}</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================
# [0] 🛠️ 창조주 통제소 (관리자)
# ==============================
elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 절대신 창조주 통제 패널")
    
    a_tab1, a_tab2, a_tab3 = st.tabs(["👥 유저 조롱 & 통제", "📈 주식 시장 강제 개입", "💬 데스노트 (게시판)"])
    with a_tab1:
        st.subheader("모든 유저 자산 & 칭호 강제 조작")
        all_users = load_db(USERS_FILE, {})
        user_list = list(all_users.keys())
        if user_list:
            sel_u = st.selectbox("조작할 유저 선택", user_list, key="admin_u")
            c1, c2 = st.columns(2)
            with c1:
                curr_c = all_users[sel_u].get('cash', 0)
                new_c = st.number_input("변경할 현금 자산", value=curr_c, step=100000000, key="admin_cash")
            with c2:
                curr_t = all_users[sel_u].get('equipped_title', '신규시민')
                new_t = st.text_input("강제 부여할 칭호", value=curr_t, key="admin_title")
            if st.button("⚔️ 해당 유저 통제 실행"):
                all_users[sel_u]['cash'] = new_c
                all_users[sel_u]['equipped_title'] = new_t
                save_db(USERS_FILE, all_users)
                st.success(f"[{sel_u}]님 정보 조작 완료!")
    with a_tab2:
        st.subheader("신의 손 (시장 조작)")
        admin_notice = st.text_input("전체 서버 고정 공지사항")
        if st.button("🚨 공지 업데이트"): market['admin_msg'] = admin_notice; save_market(market); st.success("업데이트됨")
        col_bull, col_bear = st.columns(2)
        with col_bull:
            if st.button("🔥 전 종목 50% 폭등"):
                for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = "🔥 [창조주 강림] 전 종목 50% 떡상! 글로벌 대세 상승장 도래!!"
                save_market(market); st.success("펌핑 완료")
        with col_bear:
            if st.button("🧊 전 종목 50% 폭락"):
                for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 0.5)
                market['news'] = "🧊 [창조주 분노] 전 종목 50% 폭락! 대공황 시작!!"
                save_market(market); st.error("폭락 완료")
    with a_tab3:
        st.subheader("데스노트 (게시판 삭제)")
        if st.button("💥 게시판 싹쓸이 (전체 삭제)"): save_db(COMMENTS_FILE, []); st.success("모든 흔적 삭제됨.")
