import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import json
import os
import time
from datetime import datetime

# ==============================
# 🌌 시스템 설정 및 데이터베이스
# ==============================
USERS_FILE = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE = "market_db.json"

stock_config = [
    {"id": "NDX",    "name": "나스닥100 ETF",      "vol": 0.04, "icon": "🇺🇸"},
    {"id": "HDEC",   "name": "현대건설",            "vol": 0.03, "icon": "🏗️"},
    {"id": "MANU",   "name": "맨체스터 유나이티드", "vol": 0.06, "icon": "⚽"},
    {"id": "CJENM",  "name": "CJ ENM",              "vol": 0.04, "icon": "🎬"},
    {"id": "FOOD",   "name": "삼양식품",            "vol": 0.03, "icon": "🍜"},
    {"id": "BIO",    "name": "삼성바이오로직스",    "vol": 0.05, "icon": "🧬"},
    {"id": "AERO",   "name": "한화에어로스페이스",  "vol": 0.06, "icon": "🚀"},
    {"id": "RETAIL", "name": "신세계",              "vol": 0.02, "icon": "🛍️"},
    {"id": "CHEM",   "name": "LG화학",              "vol": 0.03, "icon": "⚗️"},
    {"id": "ENTER",  "name": "하이브",              "vol": 0.07, "icon": "🎵"},
]

estate_config = {
    "E1": {"name": "역세권 원룸",        "icon": "🏠", "price": 10_000_000_000,    "income": 10_000,    "desc": "지하철 2분 거리 황금 입지"},
    "E2": {"name": "초대형 PC방",        "icon": "🖥️", "price": 50_000_000_000,    "income": 50_000,    "desc": "e스포츠 성지, 24시간 풀가동"},
    "E3": {"name": "강남 꼬마빌딩",      "icon": "🏢", "price": 500_000_000_000,   "income": 500_000,   "desc": "강남 핵심 상권 4층 빌딩"},
    "E4": {"name": "시그니엘 펜트하우스","icon": "👑", "price": 5_000_000_000_000, "income": 5_000_000, "desc": "롯데월드타워 최상층 전망"},
}

TITLE_SHOP = [
    {"name": "🌟 신진 투자자",   "price": 50_000_000,     "grade": 1},
    {"name": "💰 재테크 고수",   "price": 200_000_000,    "grade": 2},
    {"name": "🦈 시장의 상어",   "price": 1_000_000_000,  "grade": 3},
    {"name": "🏆 주식왕",        "price": 5_000_000_000,  "grade": 4},
    {"name": "🌍 글로벌 거부",   "price": 20_000_000_000, "grade": 5},
    {"name": "💎 VIP Lv.1",      "price": 100_000_000,    "grade": 1},
    {"name": "💎 VIP Lv.2",      "price": 200_000_000,    "grade": 2},
    {"name": "💎 VIP Lv.3",      "price": 300_000_000,    "grade": 3},
    {"name": "💎 VIP Lv.4",      "price": 400_000_000,    "grade": 4},
    {"name": "💎 VIP Lv.5",      "price": 500_000_000,    "grade": 5},
    {"name": "💎 VIP Lv.6",      "price": 600_000_000,    "grade": 6},
    {"name": "💎 VIP Lv.7",      "price": 700_000_000,    "grade": 7},
    {"name": "💎 VIP Lv.8",      "price": 800_000_000,    "grade": 8},
    {"name": "💎 VIP Lv.9",      "price": 900_000_000,    "grade": 9},
    {"name": "💎 VIP Lv.10",     "price": 1_000_000_000,  "grade": 10},
    {"name": "🔱 유니버스 지배자","price": 50_000_000_000, "grade": 99},
]
def hex_to_rgba(hex_color, alpha=0.3):
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3: 
            hex_color = ''.join(c*2 for c in hex_color)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r},{g},{b},{alpha})"
    except:
        return f"rgba(255,255,255,{alpha})"
# ────────────────── DB 유틸 ──────────────────
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
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices: w += p_data.get('qty', 0) * prices[sid]
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config: w += estate_config[eid]['price'] * count * 0.8
    return w

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
                'loan_time': st.session_state.loan_time,
                'stats': st.session_state.get('stats', {}),
            })
            save_db(USERS_FILE, users)

def get_market():
    def init_m():
        return {
            "version": 6,
            "stock_data": {
                s['id']: {"name": s['name'], "icon": s['icon'],
                           "price": random.randint(50_000, 150_000), "history": [80_000]}
                for s in stock_config
            },
            "news": "🌌 HYOMIN UNIVERSE 개장을 환영합니다!",
            "news_time": time.time(),
            "last_tick": time.time(),
            "admin_msg": "",
            "admin_color": "#FF4B4B",
            "lotto_pool": 5_000_000_000,
            "lotto_tickets": {},
            "lotto_last_draw": time.time(),
            "next_news_target": random.choice(stock_config)['id'],
            "next_news_impact": random.uniform(-0.2, 0.2),
            "event_active": False,
            "event_name": "",
            "event_multiplier": 1.0,
        }
    if not os.path.exists(MARKET_FILE):
        d = init_m(); save_db(MARKET_FILE, d); return d
    d = load_db(MARKET_FILE, {})
    if d.get("version") != 6:
        d = init_m(); save_db(MARKET_FILE, d); return d
    return d

def save_market(data): save_db(MARKET_FILE, data)

# ────────────────── 페이지 설정 ──────────────────
st.set_page_config(page_title="HYOMIN UNIVERSE v16", page_icon="🌌", layout="wide")

# ==============================
# 🔐 로그인 시스템
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');
    .stApp { background: radial-gradient(ellipse at 20% 50%, #0d0221 0%, #050510 60%, #000000 100%) !important; }
    * { font-family: 'Noto Sans KR', sans-serif !important; color: #FFFFFF !important; }
    .login-title {
        font-family: 'Orbitron', monospace !important;
        font-size: clamp(2rem, 6vw, 4rem) !important;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #00E5FF 0%, #FF00FF 50%, #FFD600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
        padding: 20px 0;
        animation: glow 3s ease-in-out infinite alternate;
        letter-spacing: 4px;
    }
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px #00E5FF); }
        to   { filter: drop-shadow(0 0 30px #FF00FF); }
    }
    .login-sub {
        text-align: center;
        color: #888 !important;
        font-size: 1rem;
        margin-bottom: 30px;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .stTextInput > div > div > input {
        background: rgba(0,229,255,0.05) !important;
        border: 1px solid rgba(0,229,255,0.3) !important;
        border-radius: 8px !important;
        color: #000000 !important;
        font-size: 1rem !important;
        padding: 12px !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00E5FF !important;
        box-shadow: 0 0 15px rgba(0,229,255,0.3) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00E5FF, #0066FF) !important;
        border: none !important;
        border-radius: 8px !important;
        color: #000 !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        padding: 14px !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,229,255,0.4) !important;
    }
    .stRadio > div { justify-content: center; }
    .stTabs [data-baseweb="tab"] { color: #888 !important; font-weight: 700 !important; }
    .stTabs [aria-selected="true"] { color: #00E5FF !important; border-bottom: 2px solid #00E5FF !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='login-title'>🌌 HYOMIN UNIVERSE</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-sub'>∙ 가상 자산 시뮬레이터 v16.0 ∙</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])
        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            if st.button("🚀 유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})
                def _do_login(uid):
                    u = users[uid]
                    st.session_state.update({
                        'logged_in_user': uid,
                        'global_cash': u['cash'],
                        'inventory': u.get('inventory', []),
                        'equipped_title': u.get('equipped_title', '신규시민'),
                        'portfolio': u.get('portfolio', {}),
                        'real_estate': u.get('real_estate', {}),
                        'rent_time': u.get('rent_time', time.time()),
                        'loan': u.get('loan', 0),
                        'loan_time': u.get('loan_time', time.time()),
                        'device_mode': device_mode,
                        'stats': u.get('stats', {'wins': 0, 'losses': 0, 'races_won': 0, 'lotto_spent': 0}),
                    })
                    st.rerun()
                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {"pw": "5891", "cash": 999_999_999_999, "inventory": [],
                                         "equipped_title": "👑 절대신 창조주", "portfolio": {},
                                         "real_estate": {}, "rent_time": time.time(),
                                         "loan": 0, "loan_time": time.time(), "stats": {}}
                        save_db(USERS_FILE, users)
                    _do_login("5891")
                elif l_id in users and users[l_id]['pw'] == l_pw:
                    _do_login(l_id)
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")
        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 시민 등록하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "5891":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(n_id) < 2:
                    st.error("아이디는 2자 이상이어야 합니다.")
                else:
                    users[n_id] = {"pw": n_pw, "cash": 100_000_000, "inventory": [],
                                   "equipped_title": "🌱 신규시민", "portfolio": {},
                                   "real_estate": {}, "rent_time": time.time(),
                                   "loan": 0, "loan_time": time.time(), "stats": {}}
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 초기 자금 1억원이 지급되었습니다!")
    st.stop()

# ==============================
# 🎨 CSS (PC/모바일 대응)
# ==============================
IS_PC = "🖥️" in st.session_state.device_mode

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');

/* ── 전체 배경 ── */
.stApp {
    background: #060610 !important;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(0,229,255,0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(255,0,200,0.06) 0%, transparent 50%) !important;
}

/* ── 기본 텍스트 ── */
html, body, p, span, label, div { font-family: 'Noto Sans KR', sans-serif !important; color: #E8E8F0 !important; }
h1, h2, h3 { font-family: 'Orbitron', monospace !important; letter-spacing: 2px; }

/* ── 사이드바 ── */
[data-testid='stSidebar'] {
    background: linear-gradient(180deg, #080818 0%, #0a0a20 100%) !important;
    border-right: 1px solid rgba(0,229,255,0.2) !important;
}

/* ── 입력창 ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: #FFFFFF !important; /* 배경을 완전 하양으로 */
    border: 2px solid #00E5FF !important;
    border-radius: 8px !important;
    color: #000000 !important; /* 글씨를 완전 검정으로 */
    font-weight: 900 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #00E5FF !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.25) !important;
}

/* ── 선택창 ── */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(0,229,255,0.25) !important;
    border-radius: 8px !important;
}
div[role="listbox"] {
    background: #111128 !important;
    border: 1px solid #00E5FF !important;
    border-radius: 10px !important;
}
div[role="listbox"] li, div[role="listbox"] span { color: #ffffff !important; }
div[role="listbox"] li:hover { background: rgba(0,229,255,0.15) !important; }

/* ── 버튼 ── */
.stButton > button {
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 900 !important;
    border-radius: 10px !important;
    border: 1px solid rgba(0,229,255,0.4) !important;
    background: rgba(0,229,255,0.07) !important;
    color: #00E5FF !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: rgba(0,229,255,0.18) !important;
    border-color: #00E5FF !important;
    box-shadow: 0 0 18px rgba(0,229,255,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid rgba(0,229,255,0.15) !important; }
.stTabs [data-baseweb="tab"] { color: #777 !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 10px 20px !important; }
.stTabs [aria-selected="true"] { color: #00E5FF !important; border-bottom: 2px solid #00E5FF !important; background: transparent !important; }

/* ── 메트릭 ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,229,255,0.15) !important;
    border-radius: 12px !important;
    padding: 14px 18px !important;
}
[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.8rem !important; }
[data-testid="stMetricValue"] { color: #FFD600 !important; font-family: 'Orbitron', monospace !important; font-size: 1.3rem !important; }

/* ── 알림창 ── */
.stAlert { border-radius: 10px !important; border: none !important; }

/* ── 진행바 ── */
.stProgress > div > div { background: linear-gradient(90deg, #00E5FF, #FF00FF) !important; border-radius: 4px !important; }

/* ── 주식 테이블 ── */
.stock-table { width:100%; border-collapse:collapse; }
.stock-table th {
    background: rgba(0,229,255,0.08);
    color: #00E5FF !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.75rem !important;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid rgba(0,229,255,0.2);
    letter-spacing: 1px;
}
.stock-table td {
    padding: 11px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.95rem;
    vertical-align: middle;
}
.stock-table tr:hover td { background: rgba(0,229,255,0.04); }
.p-up   { color: #FF4B4B !important; font-weight: 900; }
.p-down { color: #4B9EFF !important; font-weight: 900; }
.p-flat { color: #888 !important; }

/* ── 카드 컴포넌트 ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 14px;
    padding: 20px;
    margin: 8px 0;
    transition: all 0.3s;
}
.card:hover { border-color: rgba(0,229,255,0.4); box-shadow: 0 4px 20px rgba(0,229,255,0.1); }

/* ── 뉴스 배너 ── */
.news-banner {
    background: linear-gradient(135deg, rgba(255,180,0,0.1), rgba(255,100,0,0.08));
    border: 1px solid rgba(255,180,0,0.3);
    border-radius: 10px;
    padding: 12px 18px;
    font-weight: 700;
    color: #FFD600 !important;
    margin: 12px 0;
    font-size: 0.95rem;
}

/* ── 스코어보드 ── */
.scoreboard {
    background: linear-gradient(135deg, #0d1b2a, #1a1a3e);
    border: 2px solid rgba(0,229,255,0.4);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 0 40px rgba(0,229,255,0.15), inset 0 0 40px rgba(0,0,50,0.5);
}
.score-number {
    font-family: 'Orbitron', monospace !important;
    font-size: 3.5rem !important;
    font-weight: 900;
    color: #00FF88 !important;
    text-shadow: 0 0 20px rgba(0,255,136,0.5);
    line-height: 1;
}
.team-label {
    font-size: 1.2rem;
    font-weight: 900;
    color: #FFD600 !important;
    margin-bottom: 8px;
}
.match-time {
    font-family: 'Orbitron', monospace !important;
    color: #00E5FF !important;
    font-size: 1rem;
    margin-top: 14px;
}
.commentary-item {
    background: rgba(255,255,255,0.04);
    border-left: 3px solid #00E5FF;
    padding: 10px 15px;
    margin: 6px 0;
    border-radius: 0 8px 8px 0;
    font-size: 0.9rem;
    color: #ddd !important;
    animation: slideIn 0.4s ease;
}
@keyframes slideIn { from { opacity:0; transform: translateX(-10px); } to { opacity:1; transform: translateX(0); } }

/* ── 부동산 카드 ── */
.estate-card {
    background: linear-gradient(135deg, rgba(255,215,0,0.05), rgba(255,100,0,0.05));
    border: 1px solid rgba(255,215,0,0.2);
    border-radius: 14px;
    padding: 18px 22px;
    margin: 10px 0;
}
.estate-income { color: #00FF88 !important; font-weight: 900; font-size: 0.9rem; }

/* ── 수익 표시 ── */
.profit { color: #FF4B4B !important; font-weight: 900; }
.loss   { color: #4B9EFF !important; font-weight: 900; }

/* ── VIP 배너 ── */
.vip-banner {
    background: linear-gradient(135deg, #1a0a00, #2d1000);
    border: 2px solid rgba(255,215,0,0.5);
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 0 30px rgba(255,180,0,0.2);
}

/* ── 로또 풀 ── */
.lotto-pool {
    background: linear-gradient(135deg, #1a003a, #2d0060);
    border: 2px solid rgba(180,0,255,0.5);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 0 40px rgba(180,0,255,0.2);
}
.lotto-amount {
    font-family: 'Orbitron', monospace !important;
    font-size: 2.2rem !important;
    color: #FF00FF !important;
    text-shadow: 0 0 20px rgba(255,0,255,0.5);
    font-weight: 900;
}

/* ── 슬롯 기호 ── */
.slot-display {
    font-size: 3.5rem;
    text-align: center;
    padding: 20px;
    background: rgba(0,0,0,0.5);
    border: 2px solid rgba(255,215,0,0.3);
    border-radius: 14px;
    letter-spacing: 20px;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ── 순위 배지 ── */
.rank-1 { color: #FFD600 !important; font-size: 1.3rem; }
.rank-2 { color: #C0C0C0 !important; font-size: 1.2rem; }
.rank-3 { color: #CD7F32 !important; font-size: 1.1rem; }

/* ── CBT 문제 박스 ── */
.question-box {
    background: linear-gradient(135deg, rgba(0,229,255,0.04), rgba(0,0,100,0.1));
    border: 1px solid rgba(0,229,255,0.3);
    border-radius: 14px;
    padding: 28px;
    line-height: 1.8;
    font-size: 1.05rem;
    color: #f0f0ff !important;
}

/* ── 레이스 진행바 커스텀 ── */
.race-bar-wrap {
    margin: 6px 0;
    padding: 10px 14px;
    background: rgba(255,255,255,0.03);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.07);
}
"""

# PC/모바일 폰트 크기
if IS_PC:
    CSS += """
    p, span, label, td, th, .stSelectbox label { font-size: 1rem !important; }
    h1 { font-size: 2.2rem !important; color: #00E5FF !important; margin-bottom: 4px; }
    h2 { font-size: 1.5rem !important; color: #00FF88 !important; }
    h3 { font-size: 1.2rem !important; color: #FFD600 !important; }
    .stButton > button { height: 52px !important; font-size: 1rem !important; }
    """
else:
    CSS += """
    p, span, label, td, th { font-size: 0.88rem !important; }
    h1 { font-size: 1.5rem !important; color: #00E5FF !important; }
    h2 { font-size: 1.15rem !important; color: #00FF88 !important; }
    h3 { font-size: 1rem !important; color: #FFD600 !important; }
    .stButton > button { height: 46px !important; font-size: 0.88rem !important; }
    .stock-table th, .stock-table td { padding: 8px 8px; font-size: 0.82rem !important; }
    .score-number { font-size: 2.5rem !important; }
    .lotto-amount { font-size: 1.6rem !important; }
    """

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ==============================
# 🌐 서버 마켓 동기화
# ==============================
market = get_market()
cur_t = time.time()
m_up = False

if cur_t - market.get('last_tick', 0) > 10:
    for s in stock_config:
        curr = market['stock_data'][s['id']]
        ch = (random.random() - 0.5) * 2 * s['vol']
        if market.get('event_active') and market.get('event_target') == s['id']:
            ch *= market.get('event_multiplier', 1.5)
        curr['price'] = round(max(1_000, curr['price'] * (1 + ch)))
        curr['history'].append(curr['price'])
        if len(curr['history']) > 60: curr['history'].pop(0)
    market['last_tick'] = cur_t
    m_up = True

if cur_t - market.get('news_time', 0) > 30:
    tid, imp = market['next_news_target'], market['next_news_impact']
    t_nm = next((s['name'] for s in stock_config if s['id'] == tid), tid)
    market['stock_data'][tid]['price'] = int(market['stock_data'][tid]['price'] * (1 + imp))
    direction = "급등" if imp > 0.1 else "강세" if imp > 0 else "급락" if imp < -0.1 else "약세"
    headlines = {
        "급등": [f"🚀 [속보] {t_nm}, 실적 서프라이즈로 장중 {direction}!", f"📈 [단독] {t_nm} 대규모 외국인 매수세 포착!"],
        "강세": [f"📊 [마감] {t_nm} 기관 꾸준한 매집 행보!", f"💡 [분석] {t_nm}, 업황 개선 기대감 반영"],
        "급락": [f"❄️ [속보] {t_nm}, 악재 공시로 투자자 충격!", f"📉 [단독] {t_nm} 대규모 기관 이탈!"],
        "약세": [f"⚠️ [마감] {t_nm}, 차익 실현 매물 출회", f"🔍 [분석] {t_nm} 단기 조정 국면"],
    }
    market['news'] = random.choice(headlines.get(direction, [f"📰 {t_nm} 시황 변동"]))
    market['news_time'] = cur_t
    market['next_news_target'] = random.choice(stock_config)['id']
    market['next_news_impact'] = random.uniform(-0.25, 0.25)
    m_up = True

if cur_t - market.get('lotto_last_draw', 0) > 3600:
    if market['lotto_tickets']:
        pool = []
        for u, c in market['lotto_tickets'].items(): pool.extend([u] * c)
        win = random.choice(pool)
        prize = market['lotto_pool']
        us = load_db(USERS_FILE, {})
        if win in us:
            us[win]['cash'] += prize
            save_db(USERS_FILE, us)
            if win == st.session_state.logged_in_user:
                st.session_state.global_cash += prize
        market['news'] = f"🎊 [당첨 확정] {win}님이 ₩{prize:,} 대박 상금을 수령하셨습니다!!"
    market['lotto_pool'] = 5_000_000_000
    market['lotto_tickets'] = {}
    market['lotto_last_draw'] = cur_t
    m_up = True

if m_up: save_market(market)

# 대출 이자 처리
if st.session_state.loan > 0:
    cyc = int((cur_t - st.session_state.loan_time) / 10)
    if cyc > 0:
        st.session_state.loan = int(st.session_state.loan * (1.02 ** cyc))
        st.session_state.loan_time += cyc * 10
        sync_user_data()

nw = get_net_worth(st.session_state.logged_in_user, market)
if st.session_state.loan > 0 and nw < 0:
    st.session_state.equipped_title = "💸 신용불량자"
    sync_user_data()

# ==============================
# 🧭 메뉴
# ==============================
is_admin = st.session_state.logged_in_user == "5891"
is_vip   = nw >= 100_000_000_000 or is_admin

menu_ops = [
    "🏠 홈 광장",
    "📈 주식 트레이딩",
    "🏢 부동산 수금소",
    "🏦 은행 (대출/송금)",
    "⚔️ 글로벌 로또",
    "⚽ 구단주 시뮬레이터",
    "💻 정처기 CBT",
    "🏎️ 하이퍼카 레이싱",
    "🎰 럭키 슬롯",
    "👑 칭호 상점",
    "🏅 랭킹 & 게시판",
]
if is_vip:   menu_ops.insert(2, "💎 VIP 라운지")
if is_admin: menu_ops.append("🛠️ 창조주 통제소")

# ── 사이드바 (PC) / 상단 선택 (모바일) ──
if IS_PC:
    with st.sidebar:
        st.markdown(f"""
        <div style='padding:16px; background:rgba(0,229,255,0.05); border-radius:12px; border:1px solid rgba(0,229,255,0.2); margin-bottom:16px;'>
            <div style='font-size:1.3rem; font-weight:900; color:#00E5FF;'>👤 {st.session_state.logged_in_user}</div>
            <div style='font-size:0.85rem; color:#FFD600; margin-top:4px;'>{st.session_state.equipped_title}</div>
        </div>
        """, unsafe_allow_html=True)
        st.metric("💵 현금", f"₩{st.session_state.global_cash:,.0f}")
        st.metric("📊 순자산", f"₩{nw:,.0f}")
        if st.session_state.loan > 0:
            st.metric("💳 대출잔액", f"₩{st.session_state.loan:,.0f}")
        st.write("---")
        menu = st.radio("메뉴", menu_ops, label_visibility="collapsed")
        st.write("---")
        if st.button("🔓 로그아웃", use_container_width=True):
            sync_user_data(); st.session_state.clear(); st.rerun()
else:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"<div style='font-size:0.82rem; color:#888;'>👤 <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b> | {st.session_state.equipped_title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.9rem; color:#FFD600; font-weight:900;'>💵 ₩{st.session_state.global_cash:,}</div>", unsafe_allow_html=True)
    with col_b:
        if st.button("로그아웃"):
            sync_user_data(); st.session_state.clear(); st.rerun()
    menu = st.selectbox("메뉴 선택", menu_ops, label_visibility="collapsed")

# ── 뉴스 배너 (전 페이지 공통) ──
st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
if market.get('admin_msg'):
    col = market.get('admin_color', '#FF4B4B')
    st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {col};border-radius:10px;padding:12px 16px;color:{col}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {market['admin_msg']}</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 💎 VIP 라운지
# ════════════════════════════════════════════════
if menu == "💎 VIP 라운지":
    st.title("💎 VIP 시크릿 라운지")
    nxt_id  = market['next_news_target']
    nxt_nm  = next((s['name'] for s in stock_config if s['id'] == nxt_id), nxt_id)
    nxt_ico = next((s['icon'] for s in stock_config if s['id'] == nxt_id), "")
    imp_raw = market['next_news_impact']
    if imp_raw > 0.1:   status, clr = "🚀 강력한 호재 예정!", "#FF4B4B"
    elif imp_raw > 0:   status, clr = "📈 소폭 상승 예상",   "#FF8800"
    elif imp_raw > -0.1:status, clr = "📉 소폭 조정 예상",   "#4B9EFF"
    else:               status, clr = "💣 큰 악재 임박!",    "#8800FF"

    st.markdown(f"""
    <div class='vip-banner'>
        <div style='color:#888; font-size:0.8rem; letter-spacing:2px; margin-bottom:12px;'>🕵️ INSIDER INTELLIGENCE</div>
        <div style='font-size:1.4rem; font-weight:900; color:#FFD600;'>{nxt_ico} {nxt_nm}</div>
        <div style='font-size:1.1rem; font-weight:900; color:{clr}; margin-top:10px;'>{status}</div>
        <div style='color:#666; font-size:0.78rem; margin-top:14px;'>※ 정보 유출 시 창조주의 징벌이 따릅니다</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎰 VIP 전용 슬롯 (1억, 승률 50%)")
        if st.button("💎 VIP 슬롯 당기기", use_container_width=True):
            if st.session_state.global_cash >= 100_000_000:
                st.session_state.global_cash -= 100_000_000
                if random.random() < 0.5:
                    st.session_state.global_cash += 250_000_000
                    st.success("🎉 승리! +2.5억 획득!")
                else:
                    st.error("❌ 아쉽습니다. 다음 기회를!")
                sync_user_data(); time.sleep(1.5); st.rerun()
            else: st.error("잔액 부족!")
    with c2:
        st.markdown("### 📊 VIP 포트폴리오 요약")
        total_stock = sum(
            st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price']
            for s in stock_config
        )
        total_estate = sum(
            estate_config[eid]['price'] * cnt * 0.8
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.metric("주식 평가액", f"₩{total_stock:,.0f}")
        st.metric("부동산 평가액", f"₩{total_estate:,.0f}")
        st.metric("총 순자산", f"₩{nw:,.0f}")

# ════════════════════════════════════════════════
# 🏠 홈 광장
# ════════════════════════════════════════════════
elif menu == "🏠 홈 광장":
    st.title(f"🌌 HYOMIN UNIVERSE")
    st.markdown(f"<div style='color:#888; margin-bottom:24px;'>어서오세요, <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b>님! {st.session_state.equipped_title}</div>", unsafe_allow_html=True)

    # 자산 현황 카드
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("💵 현금", f"₩{st.session_state.global_cash:,.0f}")
    with c2: st.metric("📊 순자산", f"₩{nw:,.0f}")
    with c3: st.metric("💳 대출", f"₩{st.session_state.loan:,.0f}")
    with c4:
        total_rent_pending = sum(
            estate_config[eid]['income'] * cnt * int(cur_t - st.session_state.rent_time)
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.metric("🏢 수금 대기", f"₩{total_rent_pending:,.0f}")

    st.write("---")

    # 실시간 시장 미니 차트
    st.markdown("### 📈 실시간 시장 현황")
    top_stocks = sorted(stock_config, key=lambda s: (
        (market['stock_data'][s['id']]['history'][-1] - market['stock_data'][s['id']]['history'][-2])
        / market['stock_data'][s['id']]['history'][-2] if len(market['stock_data'][s['id']]['history']) > 1 else 0
    ), reverse=True)[:5]

    cols = st.columns(5)
    for i, s in enumerate(top_stocks):
        d = market['stock_data'][s['id']]
        diff = (d['history'][-1] - d['history'][-2]) / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        arrow = "▲" if diff >= 0 else "▼"
        clr   = "#FF4B4B" if diff >= 0 else "#4B9EFF"
        with cols[i]:
            st.markdown(f"""
            <div class='card' style='text-align:center; padding:14px;'>
                <div style='font-size:1.4rem;'>{s['icon']}</div>
                <div style='font-size:0.78rem; color:#888; margin:4px 0;'>{d['name'][:6]}</div>
                <div style='font-size:1rem; font-weight:900; color:#fff;'>₩{d['price']:,}</div>
                <div style='font-size:0.85rem; color:{clr}; font-weight:900;'>{arrow} {abs(diff):.2f}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🏆 이번 시즌 랭킹 Top 5")
    users_all = load_db(USERS_FILE, {})
    rank_data = []
    for uid, udata in users_all.items():
        if uid == "5891": continue
        w = udata.get('cash', 0) - udata.get('loan', 0)
        for sid, p in udata.get('portfolio', {}).items():
            if sid in market['stock_data']:
                w += p.get('qty', 0) * market['stock_data'][sid]['price']
        for eid, cnt in udata.get('real_estate', {}).items():
            if eid in estate_config:
                w += estate_config[eid]['price'] * cnt * 0.8
        rank_data.append({"uid": uid, "title": udata.get('equipped_title', '신규시민'), "nw": w})
    rank_data.sort(key=lambda x: x['nw'], reverse=True)
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    for i, r in enumerate(rank_data[:5]):
        me = " ← 나" if r['uid'] == st.session_state.logged_in_user else ""
        st.markdown(f"""
        <div class='card' style='display:flex; justify-content:space-between; align-items:center; padding:12px 20px;'>
            <span style='font-size:1.3rem;'>{medals[i]}</span>
            <span style='font-weight:900; color:#E8E8F0;'>{r['uid']}{me}</span>
            <span style='color:#888; font-size:0.85rem;'>{r['title']}</span>
            <span style='color:#FFD600; font-weight:900;'>₩{r['nw']:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 📈 주식 트레이딩
# ════════════════════════════════════════════════
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소")

    tab_market, tab_port, tab_trade = st.tabs(["📊 전체 시황", "💼 내 포트폴리오", "⚡ 빠른 거래"])

    with tab_market:
        rows = ""
        for s in stock_config:
            d = market['stock_data'][s['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲" if diff > 0 else "▼" if diff < 0 else "━"
            rows += f"<tr><td>{s['icon']} {d['name']}</td><td style='text-align:right; font-weight:900; color:#fff;'>₩{d['price']:,}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td><td style='text-align:right; color:#888;'>₩{d['history'][-2]:,}</td></tr>"
        st.markdown(f"<table class='stock-table'><thead><tr><th>종목</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th><th style='text-align:right;'>전일가</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

    with tab_port:
        p_rows = []
        total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp = market['stock_data'][sid]['price']
                ap = info.get('avg_price', 0)
                ev = qty * cp; total_eval += ev
                roi = (cp - ap) / ap * 100 if ap > 0 else 0
                p_rows.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주",
                                "평균단가": f"₩{int(ap):,}", "평가액": f"₩{int(ev):,}",
                                "수익률": f"{roi:+.2f}%"})
        if p_rows:
            st.table(pd.DataFrame(p_rows))
            st.metric("📊 주식 총 평가액", f"₩{total_eval:,.0f}")
        else:
            st.info("보유 중인 주식이 없습니다. 거래 탭에서 매수해보세요!")

    with tab_trade:
        sel_n = st.selectbox("거래 종목 선택", [f"{s['icon']} {s['name']}" for s in stock_config])
        sid   = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        d     = market['stock_data'][sid]
        cp    = d['price']

        # 미니 차트
        if len(d['history']) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=d['history'], mode='lines',
                line=dict(color='#00E5FF', width=2),
                fill='tozeroy', fillcolor='rgba(0,229,255,0.05)'
            ))
            fig.update_layout(
                height=220, template='plotly_dark', margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
            )
            st.plotly_chart(fig, use_container_width=True)

        diff = cp - d['history'][-2] if len(d['history']) > 1 else 0
        pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        clr  = "#FF4B4B" if diff >= 0 else "#4B9EFF"
        arr  = "▲" if diff >= 0 else "▼"
        st.markdown(f"<div style='text-align:center; margin:10px 0;'><span style='font-size:1.8rem; font-weight:900; color:#fff; font-family:Orbitron;'>₩{cp:,}</span> <span style='color:{clr}; font-weight:900;'>{arr} {abs(pct):.2f}%</span></div>", unsafe_allow_html=True)

        qty_input = st.number_input("거래 수량 (주)", min_value=1, step=1, value=1)
        cost = qty_input * cp
        st.caption(f"예상 거래금액: ₩{cost:,}")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("💥 풀매수", use_container_width=True):
                max_q = st.session_state.global_cash // cp
                if max_q > 0:
                    buy_a = max_q * cp; st.session_state.global_cash -= buy_a
                    old   = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
                    new_q = old['qty'] + max_q
                    new_a = ((old['qty'] * old['avg_price']) + buy_a) / new_q
                    st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                    if buy_a >= 1_000_000_000:
                        imp = min((buy_a / 1_000_000_000_000) * 0.1, 0.5)
                        market['stock_data'][sid]['price'] = int(cp * (1 + imp))
                        market['news'] = f"🐋 [고래 매수] {st.session_state.logged_in_user}님이 {d['name']} 거액 매수!"
                        save_market(market)
                    sync_user_data(); st.rerun()
                else: st.error("잔액 부족!")
        with c2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True):
                if st.session_state.global_cash >= cost:
                    st.session_state.global_cash -= cost
                    old   = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
                    new_q = old['qty'] + qty_input
                    new_a = ((old['qty'] * old['avg_price']) + cost) / new_q
                    st.session_state.portfolio[sid] = {'qty': new_q, 'avg_price': new_a}
                    sync_user_data(); st.success(f"✅ {qty_input}주 매수 완료!"); time.sleep(1); st.rerun()
                else: st.error("잔액 부족!")
        with c3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own >= qty_input:
                    earn = qty_input * cp
                    st.session_state.global_cash += earn
                    st.session_state.portfolio[sid]['qty'] -= qty_input
                    sync_user_data(); st.success(f"✅ {qty_input}주 매도! +₩{earn:,}"); time.sleep(1); st.rerun()
                else: st.error(f"보유 수량 부족! (현재 {own}주)")
        with c4:
            if st.button("💸 풀매도", use_container_width=True):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0:
                    sell_a = own * cp; st.session_state.global_cash += sell_a
                    st.session_state.portfolio[sid] = {'qty': 0, 'avg_price': 0}
                    if sell_a >= 1_000_000_000:
                        imp = min((sell_a / 500_000_000_000) * 0.1, 0.5)
                        market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                        market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {d['name']} 물량 투하!"
                        save_market(market)
                    sync_user_data(); st.rerun()
                else: st.error("보유 주식 없음")

if menu == "📈 주식 트레이딩":
        time.sleep(3)
        st.rerun()

# ════════════════════════════════════════════════
# 🏢 부동산 수금소
# ════════════════════════════════════════════════
elif menu == "🏢 부동산 수금소":
    st.title("🏢 부동산 제국")

    now = time.time()
    pass_s = int(now - st.session_state.rent_time)
    total_income_rate = sum(
        estate_config[eid]['income'] * cnt
        for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
    )
    pending = total_income_rate * pass_s

    # 수금 대기 배너
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,100,50,0.1));
                border:1px solid rgba(0,255,136,0.3);border-radius:14px;
                padding:22px;text-align:center;margin-bottom:18px;'>
        <div style='color:#888;font-size:0.85rem;letter-spacing:2px;margin-bottom:8px;'>누적 월세 수익</div>
        <div style='font-family:Orbitron,monospace;font-size:2rem;font-weight:900;color:#00FF88;'>₩{pending:,.0f}</div>
        <div style='color:#666;font-size:0.8rem;margin-top:8px;'>초당 ₩{total_income_rate:,} 수입 중</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("💰 전액 수금하기", use_container_width=True):
        if pending > 0:
            st.session_state.global_cash += int(pending)
            st.session_state.rent_time = now
            sync_user_data()
            st.success(f"✅ ₩{int(pending):,} 수금 완료!")
            time.sleep(1); st.rerun()
        else:
            st.info("수금할 금액이 없습니다.")

    st.write("---")
    st.markdown("### 🏘️ 부동산 매물 목록")

    for eid, info in estate_config.items():
        owned = st.session_state.real_estate.get(eid, 0)
        inc_total = info['income'] * owned
        c1, c2 = st.columns([5, 2])
        with c1:
            st.markdown(f"""
            <div class='estate-card'>
                <div style='display:flex;align-items:center;gap:12px;'>
                    <span style='font-size:2rem;'>{info['icon']}</span>
                    <div>
                        <div style='font-weight:900;font-size:1.05rem;color:#fff;'>{info['name']}</div>
                        <div style='color:#888;font-size:0.82rem;'>{info['desc']}</div>
                        <div style='margin-top:6px;'>
                            <span style='color:#FFD600;font-weight:900;'>₩{info['price']:,}</span>
                            <span style='color:#555;margin:0 8px;'>|</span>
                            <span class='estate-income'>+₩{info['income']:,}/초</span>
                            {f"<span style='margin-left:12px;color:#aaa;'>보유 {owned}채 → 초당 ₩{inc_total:,}</span>" if owned > 0 else ""}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            can_buy = st.session_state.global_cash >= info['price']
            if st.button(f"🏗️ 매입" if can_buy else "💸 잔액부족", key=f"buy_{eid}", use_container_width=True, disabled=not can_buy):
                st.session_state.global_cash -= info['price']
                st.session_state.real_estate[eid] = owned + 1
                sync_user_data()
                st.success(f"✅ {info['name']} 매입 완료!")
                time.sleep(1); st.rerun()

# ════════════════════════════════════════════════
# 🏦 은행
# ════════════════════════════════════════════════
elif menu == "🏦 은행 (대출/송금)":
    st.title("🏦 하이리스크 뱅크")

    LOAN_INTEREST_RATE = 2  # 10초당 2% 복리
    st.markdown(f"""
    <div class='card' style='margin-bottom:16px;'>
        <div style='color:#888;font-size:0.82rem;margin-bottom:8px;'>⚠️ 대출 조건: 10초마다 <b style='color:#FF4B4B;'>2% 복리 이자</b>가 붙습니다. 빠른 상환을 권장합니다!</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 현금", f"₩{st.session_state.global_cash:,}")
    c2.metric("💳 대출잔액", f"₩{st.session_state.loan:,}")
    c3.metric("📊 순자산", f"₩{nw:,}")

    tab_send, tab_loan = st.tabs(["💸 송금", "💳 대출/상환"])

    with tab_send:
        target = st.text_input("받는 분 아이디", placeholder="상대방 아이디 입력")
        amt    = st.number_input("송금 금액 (원)", min_value=0, step=1_000_000, format="%d")
        st.caption(f"송금 예정: ₩{amt:,}")
        if st.button("📤 송금하기", use_container_width=True):
            us = load_db(USERS_FILE, {})
            if target not in us:
                st.error("존재하지 않는 사용자입니다.")
            elif st.session_state.global_cash < amt:
                st.error("잔액이 부족합니다.")
            elif amt <= 0:
                st.error("금액을 입력하세요.")
            else:
                st.session_state.global_cash -= amt
                us[target]['cash'] += amt
                save_db(USERS_FILE, us)
                sync_user_data()
                st.success(f"✅ {target}님께 ₩{amt:,} 송금 완료!")

    with tab_loan:
        l_amt = st.number_input("대출 금액 (원)", min_value=0, step=100_000_000, format="%d", key="loan_in")
        if st.button("💳 대출 실행", use_container_width=True):
            if l_amt > 0:
                st.session_state.global_cash += l_amt
                st.session_state.loan += l_amt
                st.session_state.loan_time = time.time()
                sync_user_data()
                st.success(f"✅ ₩{l_amt:,} 대출 완료. 빠른 상환을 권장합니다!")
                time.sleep(1); st.rerun()

        r_amt = st.number_input("상환 금액 (원)", min_value=0, step=100_000_000, format="%d", key="repay_in")
        if st.button("🏦 상환하기", use_container_width=True):
            actual = min(r_amt, st.session_state.loan)
            if st.session_state.global_cash >= actual and actual > 0:
                st.session_state.global_cash -= actual
                st.session_state.loan -= actual
                if st.session_state.loan <= 0:
                    st.session_state.loan = 0
                    if st.session_state.equipped_title == "💸 신용불량자":
                        st.session_state.equipped_title = "🌱 신규시민"
                    st.success("🎉 대출 전액 상환 완료! 신용이 회복되었습니다.")
                else:
                    st.success(f"✅ ₩{actual:,} 상환 완료. 잔여 대출: ₩{st.session_state.loan:,}")
                sync_user_data(); time.sleep(1); st.rerun()
            else:
                st.error("잔액 부족 또는 상환 금액 오류")

# ════════════════════════════════════════════════
# ⚔️ 글로벌 로또
# ════════════════════════════════════════════════
elif menu == "⚔️ 글로벌 로또":
    st.title("⚔️ 1시간 글로벌 로또")

    rem = int(3_600 - (time.time() - market['lotto_last_draw']))
    rem = max(0, rem)
    my_t = market['lotto_tickets'].get(st.session_state.logged_in_user, 0)
    total_tickets = sum(market['lotto_tickets'].values()) if market['lotto_tickets'] else 0
    my_pct = (my_t / total_tickets * 100) if total_tickets > 0 else 0

    st.markdown(f"""
    <div class='lotto-pool'>
        <div style='color:#888;font-size:0.8rem;letter-spacing:3px;margin-bottom:10px;'>JACKPOT POOL</div>
        <div class='lotto-amount'>₩{market['lotto_pool']:,}</div>
        <div style='color:#888;margin-top:14px;font-size:0.88rem;'>
            ⏱ 추첨까지 <b style='color:#FF00FF;'>{rem//60}분 {rem%60}초</b>
        </div>
        <div style='color:#888;font-size:0.82rem;margin-top:6px;'>
            내 당첨 확률: <b style='color:#FFD600;'>{my_pct:.1f}%</b> ({my_t}장 / 전체 {total_tickets}장)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([2, 1])
    with c1:
        b_cnt = st.number_input("구매 수량 (장당 1,000만원)", min_value=1, step=1, value=1)
        cost  = b_cnt * 10_000_000
        st.caption(f"총 비용: ₩{cost:,}")
    with c2:
        st.metric("내 티켓", f"{my_t}장")

    if st.button("🎫 티켓 구매하기", use_container_width=True):
        if st.session_state.global_cash >= cost:
            st.session_state.global_cash -= cost
            market['lotto_pool'] += cost
            market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt
            save_market(market)
            sync_user_data()
            st.success(f"✅ {b_cnt}장 구매 완료! 당첨 확률 {(my_t+b_cnt)/(total_tickets+b_cnt)*100:.1f}%")
            time.sleep(1); st.rerun()
        else:
            st.error("잔액 부족!")

    # 참여자 현황
    if market['lotto_tickets']:
        st.write("---")
        st.markdown("### 👥 현재 참여자")
        sorted_t = sorted(market['lotto_tickets'].items(), key=lambda x: x[1], reverse=True)
        for uid, cnt in sorted_t[:10]:
            pct = cnt / total_tickets * 100
            me_mark = " 👈" if uid == st.session_state.logged_in_user else ""
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'><span style='color:#ddd;'>{uid}{me_mark}</span><span style='color:#FF00FF;font-weight:900;'>{cnt}장 ({pct:.1f}%)</span></div>", unsafe_allow_html=True)

    time.sleep(5); st.rerun()

# ════════════════════════════════════════════════
# ⚽ 구단주 시뮬레이터
# ════════════════════════════════════════════════
elif menu == "⚽ 구단주 시뮬레이터":
    st.title("🏆 구단주 시뮬레이터")

    FORMATION_STATS = {
        "4-4-2 (균형)":    {"atk": 0.30, "def": 0.27, "emoji": "⚖️"},
        "4-3-3 (공격)":    {"atk": 0.42, "def": 0.15, "emoji": "🔥"},
        "3-5-2 (중원장악)":{"atk": 0.27, "def": 0.22, "emoji": "🧠"},
        "5-3-2 (수비철벽)":{"atk": 0.18, "def": 0.38, "emoji": "🛡️"},
        "4-2-3-1 (현대)":  {"atk": 0.33, "def": 0.24, "emoji": "⚡"},
        "3-4-3 (총공격)":  {"atk": 0.48, "def": 0.10, "emoji": "💥"},
    }
    STADIUMS = ["🏟️ 효민 아레나", "⚽ 갤럭시 스타디움", "🌌 유니버스 파크", "🔥 인페르노 필드"]

    c1, c2 = st.columns(2)
    with c1:
        my_team   = st.text_input("내 팀 이름", value="FC 효민")
        my_form   = st.selectbox("포메이션", list(FORMATION_STATS.keys()), key="mf")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[my_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[my_form]['def']*10)}</div>", unsafe_allow_html=True)
    with c2:
        opp_team  = st.text_input("상대 팀", value="FC 라이벌")
        opp_form  = st.selectbox("상대 포메이션", list(FORMATION_STATS.keys()), key="of")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[opp_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[opp_form]['def']*10)}</div>", unsafe_allow_html=True)

    stadium = st.selectbox("경기장", STADIUMS)
    betting = st.number_input("경기 베팅금액 (내 팀 승리 시 2배)", min_value=0, step=1_000_000, value=0)

    if st.button("⚽ 킥오프!", use_container_width=True):
        if betting > 0 and st.session_state.global_cash < betting:
            st.error("베팅 금액이 잔액을 초과합니다.")
        else:
            if betting > 0: st.session_state.global_cash -= betting

            my_s  = FORMATION_STATS[my_form]
            opp_s = FORMATION_STATS[opp_form]
            h_score = a_score = 0
            scoreboard   = st.empty()
            comm_box     = st.empty()
            prog_bar     = st.progress(0, text="전반전 시작!")
            commentaries = []

            ALL_EVENTS = {
                "my_goal":  ["⚽ 골!!!! {my}의 환상적인 왼발 슈팅!", "⚽ 골!!!! {my} 코너킥 헤더로 득점!", "⚽ 골!!!! {my}의 원더골! 관중석이 술렁입니다!",
                             "⚽ {my} 선수의 멀티골! 완벽한 경기!", "⚽ 프리킥 직접 연결! {my}이 득점합니다!"],
                "opp_goal": ["⚽ {opp}이 반격합니다! 동점!","⚽ {opp}의 역습 득점! 위기!","⚽ {opp}이 기습 골을 터트립니다!",
                             "⚽ {opp}의 헤더골! 수비가 뚫렸습니다!"],
                "my_save":  ["🧤 우리 GK의 슈퍼세이브! 기적 같은 선방!", "🛡️ {my} 수비수의 살신성인 태클!", "🏃 {my}의 역습 저지!"],
                "opp_save": ["🛡️ {opp} GK가 막아냅니다!", "🧤 {opp}의 철벽 수비!", "⛔ {opp} 오프사이드! 기회 무산"],
                "neutral":  ["📊 팽팽한 중원 다툼...", "🌟 관중석의 열기가 뜨겁습니다!", "⚡ {my} 드리블 돌파 시도!", "🎯 {opp} 롱패스 연결 실패", "🔥 양팀 모두 숨막히는 접전!"],
            }

            def pick(key, **kw):
                t = random.choice(ALL_EVENTS[key])
                return t.format(my=my_team[:6], opp=opp_team[:6])

            for minute in range(1, 19):  # 18분 = 90분 시뮬
                time.sleep(0.45)
                real_min = minute * 5

                if real_min == 45:
                    commentaries.insert(0, f"🔔 전반 종료! 스코어: {h_score} : {a_score}")

                # 내 팀 공격
                if random.random() < my_s['atk']:
                    if random.random() > opp_s['def']:
                        h_score += 1
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('my_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_save')}")

                # 상대 팀 공격
                if random.random() < opp_s['atk']:
                    if random.random() > my_s['def']:
                        a_score += 1
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('my_save')}")

                if random.random() < 0.35:
                    commentaries.insert(0, f"🕐 {real_min}' | {pick('neutral')}")

                # 스코어보드
                form_label_m = f"{my_form} {FORMATION_STATS[my_form]['emoji']}"
                form_label_o = f"{opp_form} {FORMATION_STATS[opp_form]['emoji']}"
                scoreboard.markdown(f"""
                <div class='scoreboard'>
                    <div style='color:#555;font-size:0.78rem;letter-spacing:2px;margin-bottom:16px;'>{stadium}</div>
                    <div style='display:flex;justify-content:space-around;align-items:center;'>
                        <div>
                            <div class='team-label'>{my_team}</div>
                            <div style='color:#666;font-size:0.78rem;'>{form_label_m}</div>
                        </div>
                        <div>
                            <div class='score-number'>{h_score} : {a_score}</div>
                            <div class='match-time'>⏱ {real_min}' / 90'</div>
                        </div>
                        <div>
                            <div class='team-label'>{opp_team}</div>
                            <div style='color:#666;font-size:0.78rem;'>{form_label_o}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                comm_html = "".join(f"<div class='commentary-item'>{c}</div>" for c in commentaries[:6])
                comm_box.markdown(comm_html, unsafe_allow_html=True)
                prog_bar.progress(minute / 18, text=f"{'전반' if real_min<=45 else '후반'} {min(real_min,90)}분")

            prog_bar.progress(1.0, text="⚽ 경기 종료!")
            st.write("---")

            if h_score > a_score:
                st.success(f"🎉 승리! {my_team} {h_score}:{a_score} {opp_team}")
                reward = 10_000_000 + betting * 2 if betting > 0 else 5_000_000
                st.balloons()
            elif h_score == a_score:
                st.warning(f"🤝 무승부! {h_score}:{a_score}")
                reward = 2_000_000 + (betting if betting > 0 else 0)
            else:
                st.error(f"😢 패배... {h_score}:{a_score}")
                reward = 500_000

            st.session_state.global_cash += reward
            sync_user_data()
            st.info(f"💰 경기 보상: +₩{reward:,}")
            time.sleep(3); st.rerun()
# ════════════════════════════════════════════════
# 💻 정처기 CBT (HTML 고퀄리티 버전 삽입)
# ════════════════════════════════════════════════
elif menu == "💻 정처기 CBT":
    import streamlit.components.v1 as components
    
    st.title("💻 정보처리기사 실기 완벽정복")
    st.markdown("스마트폰 앱 환경처럼 구현된 최고급 실전 모의고사입니다.")
    
    # 효민님이 주신 HTML 코드를 통째로 문자열로 넣습니다.
    cbt_html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>정처기 실기 완벽정복 🥔</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
    <style>
    *{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
    :root{
      --ac:#3B5BDB;--ac-l:#EEF2FF;
      --bg:#F0F2F8;--card:#fff;--text:#1A1D2E;--sub:#6B7280;
      --border:#E2E6F0;
      --green:#059669;--green-l:#ECFDF5;--green-b:#A7F3D0;
      --red:#DC2626;--red-l:#FEF2F2;--red-b:#FECACA;
      --orange:#D97706;--orange-l:#FFFBEB;
      --nav-h:62px;
    }
    html,body{height:100%;overflow-x:hidden}
    body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);padding-bottom:calc(var(--nav-h) + env(safe-area-inset-bottom) + 12px)}
    .hd{background:#fff;border-bottom:1.5px solid var(--border);padding:10px 14px 0;position:sticky;top:0;z-index:200;box-shadow:0 2px 10px rgba(0,0,0,.06)}
    .hd-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:9px}
    .hd-title{font-size:16px;font-weight:900;letter-spacing:-.3px;display:flex;align-items:center;gap:6px}
    .hd-badge{padding:2px 9px;border-radius:20px;font-size:10px;font-weight:800;color:#fff;background:var(--ac)}
    .hd-streak{font-size:11px;font-weight:700;color:var(--orange);background:var(--orange-l);padding:3px 9px;border-radius:20px}
    .mode-tabs{display:flex;background:var(--bg);border-radius:10px;padding:3px;gap:2px;margin-bottom:10px}
    .mtab{flex:1;padding:7px 2px;border:none;border-radius:7px;font-family:inherit;font-size:11.5px;font-weight:700;cursor:pointer;color:var(--sub);background:transparent;transition:all .2s;display:flex;align-items:center;justify-content:center;gap:3px}
    .mtab.on{background:#fff;color:var(--text);box-shadow:0 1px 5px rgba(0,0,0,.1)}
    .nav{position:fixed;bottom:0;left:0;right:0;background:#fff;border-top:1.5px solid var(--border);display:flex;z-index:300;padding-bottom:env(safe-area-inset-bottom);height:calc(var(--nav-h) + env(safe-area-inset-bottom))}
    .nbtn{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;border:none;background:transparent;cursor:pointer;color:var(--sub);font-family:inherit;font-size:9px;font-weight:700;padding:8px 2px 4px;transition:all .2s;position:relative}
    .nbtn .ico{font-size:20px;line-height:1;transition:transform .2s}
    .nbtn.on{color:var(--ac)}.nbtn.on .ico{transform:scale(1.1)}
    .nbtn .dot{position:absolute;top:7px;right:calc(50% - 16px);width:7px;height:7px;border-radius:50%;background:var(--red);border:2px solid #fff;display:none}
    .nbtn .dot.show{display:block}
    .main{padding:12px}
    .view{display:none}.view.on{display:block}
    .fview{display:none;flex-direction:column}.fview.on{display:flex}
    .qview{display:none;flex-direction:column;gap:10px}.qview.on{display:flex}
    .rcard{background:#fff;border-radius:14px;margin-bottom:10px;box-shadow:0 1px 5px rgba(0,0,0,.06);border:1.5px solid var(--border);overflow:hidden;transition:border-color .2s}
    .rcard.open{border-color:var(--ac)}
    .rcard-hd{display:flex;align-items:center;padding:13px 14px;cursor:pointer;gap:8px;user-select:none;-webkit-user-select:none}
    .rcard-num{width:30px;height:30px;border-radius:8px;flex-shrink:0;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;background:var(--ac-l);color:var(--ac)}
    .rcard-name{font-size:13.5px;font-weight:700;line-height:1.3;flex:1}
    .prob{font-size:14px;flex-shrink:0}
    .arr{font-size:11px;color:#ccc;transition:transform .25s;flex-shrink:0}
    .rcard.open .arr{transform:rotate(180deg)}
    .rcard-body{display:none;border-top:1.5px solid var(--border);padding:13px 14px}
    .rcard.open .rcard-body{display:block}
    .rt{width:100%;border-collapse:collapse;font-size:12.5px;margin:6px 0}
    .rt th{background:var(--ac-l);padding:7px 10px;text-align:left;font-weight:800;color:var(--ac);border-bottom:1.5px solid var(--border);font-size:11px}
    .rt td{padding:7px 10px;border-bottom:1px solid var(--border);color:#333;vertical-align:top;line-height:1.55;font-size:12.5px}
    .rt tr:last-child td{border-bottom:none}
    .rt td b,.rt td strong{color:#111;font-weight:800}
    .tip{background:var(--ac-l);border-left:3px solid var(--ac);border-radius:0 8px 8px 0;padding:10px 12px;margin-top:8px;font-size:12.5px;line-height:1.75;color:#333}
    .tip b{color:var(--ac)}
    .mnemo{background:var(--text);color:#fff;border-radius:7px;padding:5px 11px;font-size:12px;font-weight:700;margin-bottom:8px;display:inline-block}
    .flow{display:flex;flex-wrap:wrap;align-items:center;gap:5px;margin:8px 0}
    .flow .s{background:var(--ac-l);border:1.5px solid #c5d0f8;border-radius:7px;padding:4px 9px;font-size:12px;font-weight:700;color:var(--ac)}
    .flow .a{color:#bbb;font-size:11px}
    .fc-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
    .fc-prog-txt{font-size:12px;font-weight:700;color:var(--sub)}
    .fc-score-wrap{display:flex;gap:10px;font-size:12px;font-weight:800}
    .fc-score-k{color:var(--green)}.fc-score-u{color:var(--red)}
    .fc-pbar{height:5px;background:var(--border);border-radius:99px;overflow:hidden;margin-bottom:14px}
    .fc-pbar-fill{height:100%;background:var(--ac);border-radius:99px;transition:width .4s}
    .fc-area{perspective:1200px;height:230px;cursor:pointer;margin-bottom:10px}
    .fc-inner{width:100%;height:100%;position:relative;transition:transform .55s cubic-bezier(.4,0,.2,1);transform-style:preserve-3d;-webkit-transform-style:preserve-3d}
    .fc-inner.flip{transform:rotateY(180deg)}
    .fc-face{position:absolute;width:100%;height:100%;backface-visibility:hidden;-webkit-backface-visibility:hidden;border-radius:18px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:22px 20px;border:2px solid var(--border);box-shadow:0 5px 24px rgba(0,0,0,.09)}
    .fc-front{background:#fff}
    .fc-back{background:var(--ac);transform:rotateY(180deg);border-color:var(--ac)}
    .fc-tag{font-size:10px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:10px;opacity:.55}
    .fc-front .fc-tag{color:var(--ac)}
    .fc-back .fc-tag{color:rgba(255,255,255,.75)}
    .fc-word{font-size:17px;font-weight:900;text-align:center;line-height:1.55}
    .fc-front .fc-word{color:var(--text)}
    .fc-back .fc-word{color:#fff}
    .fc-sub{font-size:12.5px;text-align:center;line-height:1.65;margin-top:8px;font-weight:500}
    .fc-front .fc-sub{color:var(--sub)}
    .fc-back .fc-sub{color:rgba(255,255,255,.85)}
    .fc-hint-txt{text-align:center;font-size:11px;color:#c5c8d4;font-weight:600;margin-top:10px}
    .fc-actions{display:none;gap:10px;margin-bottom:12px}
    .fc-actions.show{display:grid;grid-template-columns:1fr 1fr}
    .fc-no{padding:14px;border-radius:12px;border:2px solid var(--red-b);background:var(--red-l);font-family:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--red);transition:all .15s}
    .fc-yes{padding:14px;border-radius:12px;border:2px solid var(--green-b);background:var(--green-l);font-family:inherit;font-size:13.5px;font-weight:800;cursor:pointer;color:var(--green);transition:all .15s}
    .fc-no:active,.fc-yes:active{opacity:.78;transform:scale(.97)}
    .fc-result{background:#fff;border-radius:16px;border:1.5px solid var(--border);padding:28px 18px;text-align:center;display:none}
    .fc-result.show{display:block}
    .fc-result .re{font-size:50px;margin-bottom:6px}
    .fc-result .rt2{font-size:19px;font-weight:900;margin-bottom:4px}
    .fc-result .rs{font-size:13px;color:var(--sub);margin-bottom:14px;line-height:1.6}
    .fc-result .rstats{display:flex;justify-content:center;gap:24px;padding:12px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border);margin-bottom:14px}
    .fc-result .rstat .n{font-size:22px;font-weight:900}
    .fc-result .rstat .l{font-size:10px;color:var(--sub);font-weight:600;margin-top:2px}
    .fc-btn{width:100%;padding:13px;border-radius:11px;border:none;font-family:inherit;font-size:14px;font-weight:800;cursor:pointer;background:var(--ac);color:#fff;margin-bottom:8px}
    .fc-btn2{width:100%;padding:11px;border-radius:11px;border:2px solid var(--red-b);font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;background:#fff;color:var(--red);display:none}
    .fc-btn2.show{display:block}
    .qprog{background:#fff;border-radius:12px;padding:11px 14px;border:1.5px solid var(--border);box-shadow:0 1px 4px rgba(0,0,0,.05)}
    .qprog-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:7px}
    .qpl{font-size:11.5px;font-weight:700;color:var(--sub)}
    .qpr{display:flex;gap:12px;font-size:12px;font-weight:800}
    .qpr-c{color:var(--green)}.qpr-w{color:var(--red)}
    .qpbar{height:5px;background:var(--border);border-radius:99px;overflow:hidden}
    .qpbar-f{height:100%;background:linear-gradient(90deg,var(--ac),#6B8AFF);border-radius:99px;transition:width .5s cubic-bezier(.4,0,.2,1)}
    .qcard{background:#fff;border-radius:16px;border:1.5px solid var(--border);box-shadow:0 3px 14px rgba(0,0,0,.07);overflow:hidden;animation:fadeUp .3s ease both}
    @keyframes fadeUp{from{opacity:0;transform:translateY(9px)}to{opacity:1;transform:translateY(0)}}
    .qcard-top{padding:9px 16px;display:flex;justify-content:space-between;align-items:center}
    .qcat-l{font-size:11px;font-weight:800;color:var(--ac);background:var(--ac-l);padding:3px 8px;border-radius:5px}
    .qnum-l{font-size:11px;font-weight:700;color:var(--sub)}
    .qbody{padding:16px}
    .qtype{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:800;padding:3px 8px;border-radius:5px;margin-bottom:12px;border:1px solid}
    .qtype-sa{background:#FEF3C7;color:#92400E;border-color:#FDE68A}
    .qbox{background:#F8F9FC;border:1.5px solid var(--border);border-radius:10px;padding:14px 15px;margin-bottom:14px;font-size:14px;line-height:1.85;color:#111;font-weight:500;white-space:pre-wrap}
    .ans-section{margin-top:0}
    .ans-label{font-size:11px;font-weight:800;color:var(--sub);margin-bottom:7px;letter-spacing:.05em}
    .ans-wrap{display:flex;gap:8px}
    .ans-input{flex:1;padding:12px 14px;border:2px solid var(--border);border-radius:10px;font-family:inherit;font-size:15px;font-weight:700;color:var(--text);background:#fff;outline:none;transition:border-color .2s;-webkit-appearance:none}
    .ans-input:focus{border-color:var(--ac)}
    .ans-input.ok{border-color:var(--green);background:var(--green-l)}
    .ans-input.ng{border-color:var(--red);background:var(--red-l)}
    .ans-input:disabled{cursor:default}
    .submit-btn{padding:12px 16px;border-radius:10px;border:none;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;background:var(--ac);color:#fff;white-space:nowrap;transition:opacity .2s;flex-shrink:0}
    .submit-btn:active{opacity:.85}
    .res-box{display:none;margin-top:12px;border-radius:10px;padding:12px 14px;font-size:13.5px;line-height:1.75;border-left:4px solid}
    .res-box.show{display:block}
    .res-box.ok{background:var(--green-l);border-color:var(--green);color:#065f46}
    .res-box.ng{background:var(--red-l);border-color:var(--red);color:#991b1b}
    .res-head{font-size:13px;font-weight:900;margin-bottom:5px;display:flex;align-items:center;gap:5px}
    .res-correct{font-size:14px;font-weight:800;margin:6px 0;padding:8px 12px;background:rgba(255,255,255,.65);border-radius:7px}
    .res-exp{font-size:12.5px;margin-top:5px;line-height:1.75;opacity:.9}
    .next-btn{width:100%;padding:14px;border-radius:12px;border:none;font-family:inherit;font-size:14px;font-weight:800;cursor:pointer;background:var(--ac);color:#fff;display:none;margin-top:12px}
    .next-btn.show{display:block}
    .qresult{background:#fff;border-radius:16px;border:1.5px solid var(--border);padding:28px 18px;text-align:center;display:none;box-shadow:0 3px 14px rgba(0,0,0,.07)}
    .qresult.show{display:block;animation:fadeUp .35s ease both}
    .qr-e{font-size:52px;margin-bottom:6px}
    .qr-t{font-size:20px;font-weight:900;margin-bottom:4px}
    .qr-s{font-size:13px;color:var(--sub);margin-bottom:12px;line-height:1.6}
    .qr-pct{font-size:50px;font-weight:900;color:var(--ac);line-height:1;margin-bottom:10px}
    .qr-stats{display:flex;justify-content:center;gap:28px;margin-bottom:18px;padding:14px 0;border-top:1px solid var(--border);border-bottom:1px solid var(--border)}
    .qr-stat .n{font-size:22px;font-weight:900}.qr-stat .l{font-size:10px;color:var(--sub);font-weight:600;margin-top:3px}
    .qr-btn{width:100%;padding:13px;border-radius:11px;border:none;font-family:inherit;font-size:14px;font-weight:800;cursor:pointer;background:var(--ac);color:#fff;margin-bottom:8px}
    .qr-btn2{width:100%;padding:11px;border-radius:11px;border:2px solid var(--red-b);font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;background:#fff;color:var(--red);margin-bottom:8px;display:none}
    .qr-btn2.show{display:block}
    .qr-btn3{width:100%;padding:11px;border-radius:11px;border:1.5px solid var(--border);font-family:inherit;font-size:12px;font-weight:700;cursor:pointer;background:#fff;color:var(--text)}
    .wrongs{display:none;flex-direction:column;gap:8px}.wrongs.on{display:flex}
    .wcard{background:#fff;border-radius:12px;border:1.5px solid var(--red-b);padding:13px}
    .wcard-q{font-size:12.5px;font-weight:700;color:#111;margin-bottom:8px;line-height:1.7;background:#F8F9FC;padding:10px;border-radius:8px;white-space:pre-wrap}
    .wcard-your{font-size:11.5px;color:var(--red);font-weight:700;margin-bottom:4px}
    .wcard-ans-l{font-size:10px;color:var(--green);font-weight:800;margin-bottom:3px}
    .wcard-ans{font-size:13.5px;color:var(--green);font-weight:800;background:var(--green-l);padding:8px 12px;border-radius:8px}
    .wcard-exp{font-size:12px;color:#555;margin-top:6px;line-height:1.65}
    .back-btn{width:100%;padding:12px;border-radius:11px;border:none;font-family:inherit;font-size:13px;font-weight:700;cursor:pointer;background:var(--ac);color:#fff;margin-bottom:10px}
    .sechd{font-size:11px;font-weight:800;color:var(--sub);letter-spacing:.08em;padding:2px 0 8px}
    .empty-state{text-align:center;padding:48px 16px;color:var(--sub);font-size:14px;font-weight:700;line-height:1.8}
    </style>
    </head>
    <body>
    <div class="hd">
      <div class="hd-top">
        <div class="hd-title">🥔 정처기 실기<span class="hd-badge" id="hd-badge">DB</span></div>
        <span class="hd-streak" id="hd-streak">🔥 0일</span>
      </div>
      <div class="mode-tabs">
        <button class="mtab on" onclick="setMode('review')">📖 복습</button>
        <button class="mtab" onclick="setMode('flash')">🃏 암기</button>
        <button class="mtab" onclick="setMode('quiz')">✏️ 기출형</button>
        <button class="mtab" onclick="setMode('wrong')">❌ 오답</button>
      </div>
    </div>
    <div class="main">
      <div class="view on" id="view-review"></div>
      <div class="fview" id="view-flash">
        <div class="fc-hd">
          <span class="fc-prog-txt" id="fc-prog">0 / 0</span>
          <div class="fc-score-wrap">
            <span class="fc-score-k" id="fc-k">✅ 0</span>
            <span class="fc-score-u" id="fc-u">❌ 0</span>
          </div>
        </div>
        <div class="fc-pbar"><div class="fc-pbar-fill" id="fc-pbar" style="width:0%"></div></div>
        <div class="fc-area" id="fc-area" onclick="flipCard()">
          <div class="fc-inner" id="fc-inner">
            <div class="fc-face fc-front">
              <div class="fc-tag" id="fc-tag-f">카테고리</div>
              <div class="fc-word" id="fc-word">—</div>
              <div class="fc-sub" id="fc-hint-sub"></div>
            </div>
            <div class="fc-face fc-back">
              <div class="fc-tag">정답 ✅</div>
              <div class="fc-word" id="fc-ans"></div>
              <div class="fc-sub" id="fc-exp"></div>
            </div>
          </div>
        </div>
        <div class="fc-hint-txt" id="fc-hint-txt">👆 카드를 탭해서 뒤집기</div>
        <div class="fc-actions" id="fc-actions">
          <button class="fc-no" onclick="fcMark(false)">❌ 모르겠어</button>
          <button class="fc-yes" onclick="fcMark(true)">✅ 알아!</button>
        </div>
        <div class="fc-result" id="fc-result">
          <div class="re" id="fc-r-e"></div>
          <div class="rt2" id="fc-r-t"></div>
          <div class="rs" id="fc-r-s"></div>
          <div class="rstats">
            <div class="rstat"><div class="n" style="color:var(--green)" id="fc-r-k">0</div><div class="l">알아!</div></div>
            <div class="rstat"><div class="n" style="color:var(--red)" id="fc-r-u">0</div><div class="l">모르겠어</div></div>
            <div class="rstat"><div class="n" id="fc-r-tot">0</div><div class="l">전체</div></div>
          </div>
          <button class="fc-btn" onclick="startFlash()">🔁 다시 외우기</button>
          <button class="fc-btn2" id="fc-r-unkn-btn" onclick="startFlashUnknown()">❌ 모르는 것만 다시</button>
        </div>
      </div>
      <div class="qview" id="view-quiz">
        <div class="qprog">
          <div class="qprog-top">
            <span class="qpl" id="qpl">0 / 0</span>
            <div class="qpr"><span class="qpr-c" id="qpr-c">✓ 0</span><span class="qpr-w" id="qpr-w">✗ 0</span></div>
          </div>
          <div class="qpbar"><div class="qpbar-f" id="qpbar-f" style="width:0%"></div></div>
        </div>
        <div class="qcard" id="qcard">
          <div class="qcard-top">
            <span class="qcat-l" id="qcat-l">—</span>
            <span class="qnum-l" id="qnum-l">1 / 20</span>
          </div>
          <div class="qbody">
            <span class="qtype" id="qt-badge"></span>
            <div class="qbox" id="qtxt"></div>
            <div class="ans-section">
              <div class="ans-label">▶ 답안 입력</div>
              <div class="ans-wrap">
                <input class="ans-input" id="ans-input" type="text" placeholder="답을 입력하세요" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
                <button class="submit-btn" id="submit-btn" onclick="submitAns()">확인</button>
              </div>
            </div>
            <div class="res-box" id="res-box"></div>
            <button class="next-btn" id="next-btn" onclick="nextQ()">다음 문제 →</button>
          </div>
        </div>
        <div class="qresult" id="qresult">
          <div class="qr-e" id="qr-e"></div>
          <div class="qr-t" id="qr-t"></div>
          <div class="qr-s" id="qr-s"></div>
          <div class="qr-pct" id="qr-pct"></div>
          <div class="qr-stats">
            <div class="qr-stat"><div class="n" style="color:var(--green)" id="qr-c">0</div><div class="l">맞음</div></div>
            <div class="qr-stat"><div class="n" style="color:var(--red)" id="qr-w">0</div><div class="l">틀림</div></div>
            <div class="qr-stat"><div class="n" id="qr-t2">0</div><div class="l">전체</div></div>
          </div>
          <button class="qr-btn" onclick="startQuiz()">🔁 다시 풀기</button>
          <button class="qr-btn2" id="qr-btn2" onclick="viewWrong()">❌ 오답 보기</button>
          <button class="qr-btn3" onclick="setMode('review')">📖 복습으로</button>
        </div>
      </div>
      <div class="view" id="view-wrong">
        <div class="sechd" id="wrong-hd"></div>
        <div id="wrong-body"></div>
      </div>
    </div>
    <nav class="nav">
      <button class="nbtn on" data-cat="db" onclick="setCat('db')"><span class="ico">🗄️</span>DB<span class="dot" id="dot-db"></span></button>
      <button class="nbtn" data-cat="net" onclick="setCat('net')"><span class="ico">🌐</span>네트워크<span class="dot" id="dot-net"></span></button>
      <button class="nbtn" data-cat="sw" onclick="setCat('sw')"><span class="ico">🧪</span>SW개발<span class="dot" id="dot-sw"></span></button>
      <button class="nbtn" data-cat="des" onclick="setCat('des')"><span class="ico">🏗️</span>SW설계<span class="dot" id="dot-des"></span></button>
      <button class="nbtn" data-cat="sec" onclick="setCat('sec')"><span class="ico">🔐</span>보안<span class="dot" id="dot-sec"></span></button>
    </nav>
    <script>
    const CATS = {
      db:  {name:'DB·SQL',      color:'#3B5BDB',light:'#EEF2FF'},
      net: {name:'네트워크·OS', color:'#7C3AED',light:'#F3EEFF'},
      sw:  {name:'SW 개발',     color:'#059669',light:'#ECFDF5'},
      des: {name:'SW 설계',     color:'#D97706',light:'#FFFBEB'},
      sec: {name:'보안·신기술', color:'#DC2626',light:'#FFF5F5'},
    };
    const RV = {
    db:[
    {num:'1',name:'SQL 핵심 명령어',p:'💯',b:`<div class="mnemo">DDL·DML·DCL 구분 먼저!</div><table class="rt"><tr><th>분류</th><th>명령어</th><th>역할</th></tr><tr><td>DML</td><td><b>SELECT</b></td><td>조회</td></tr><tr><td>DML</td><td><b>INSERT INTO</b></td><td>삽입</td></tr><tr><td>DML</td><td><b>UPDATE SET</b></td><td>수정</td></tr><tr><td>DML</td><td><b>DELETE FROM</b></td><td>삭제</td></tr><tr><td>DDL</td><td><b>CREATE</b></td><td>생성</td></tr><tr><td>DDL</td><td><b>ALTER ADD/MODIFY/DROP</b></td><td>구조 변경</td></tr><tr><td>DDL</td><td><b>DROP TABLE</b></td><td>삭제 (CASCADE/RESTRICT)</td></tr><tr><td>DCL</td><td><b>GRANT … TO</b></td><td>권한 부여</td></tr><tr><td>DCL</td><td><b>REVOKE … FROM</b></td><td>권한 회수</td></tr></table><div class="tip"><b>WHERE vs HAVING:</b> WHERE = 그룹화 전 / HAVING = GROUP BY 후 집계에 조건<br><b>LIKE:</b> '%문자%'=포함 · '문자%'=시작 · '_문'=앞 1글자<br><b>AND는 OR보다 우선!</b></div>`},
    {num:'2',name:'JOIN·집합연산자·서브쿼리',p:'💯',b:`<table class="rt"><tr><th>JOIN</th><th>설명</th></tr><tr><td><b>INNER JOIN</b></td><td>두 테이블 모두 매칭되는 행만</td></tr><tr><td><b>LEFT OUTER</b></td><td>왼쪽 전부 + 오른쪽 NULL</td></tr><tr><td><b>NATURAL JOIN</b></td><td>ON 없음, 공통 컬럼 자동 매칭</td></tr><tr><td><b>CROSS JOIN</b></td><td>모든 조합 (카르테시안)</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>집합연산자</th><th>핵심</th></tr><tr><td><b>UNION</b></td><td>중복 제거 합집합</td></tr><tr><td><b>UNION ALL</b></td><td>중복 허용 합집합</td></tr><tr><td><b>INTERSECT</b></td><td>교집합</td></tr><tr><td><b>EXCEPT / MINUS</b></td><td>차집합 (Oracle = MINUS)</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>서브쿼리 연산자</th><th>의미</th></tr><tr><td><b>IN</b></td><td>하나라도 일치</td></tr><tr><td><b>&gt; ALL</b></td><td>모든 값보다 큼</td></tr><tr><td><b>&gt; ANY</b></td><td>하나보다 큼</td></tr><tr><td><b>EXISTS</b></td><td>결과 존재하면 반환</td></tr></table>`},
    {num:'3',name:'트랜잭션 ACID + Lock + 회복',p:'⭐',b:`<table class="rt"><tr><th>ACID</th><th>영어</th><th>의미</th></tr><tr><td><b>원자성</b></td><td>Atomicity</td><td><b>All or Nothing</b></td></tr><tr><td><b>일관성</b></td><td>Consistency</td><td>전후 무결성 보장</td></tr><tr><td><b>고립성</b></td><td>Isolation</td><td>다른 트랜잭션 끼어들기 불가</td></tr><tr><td><b>지속성</b></td><td>Durability</td><td>완료 결과 영구 저장</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>Lock</th><th>설명</th></tr><tr><td><b>S-Lock(공유락)</b></td><td>읽기 시, 동시 읽기 가능, 쓰기 불가</td></tr><tr><td><b>X-Lock(배타락)</b></td><td>쓰기 시, 읽기·쓰기 모두 불가</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>회복</th><th>조건</th><th>동작</th></tr><tr><td><b>Redo(재실행)</b></td><td>Start O + Commit O</td><td>복구 재실행</td></tr><tr><td><b>Undo(취소)</b></td><td>Start O + Commit X</td><td>작업 전부 취소</td></tr></table>`},
    {num:'4',name:'정규화 (1NF~BCNF)',p:'🔥',b:`<div class="mnemo">1NF→2NF→3NF→BCNF</div><table class="rt"><tr><th>정규형</th><th>제거 대상</th><th>조건</th></tr><tr><td><b>1NF</b></td><td>반복 그룹</td><td>모든 속성 = 원자값</td></tr><tr><td><b>2NF</b></td><td><b>부분 함수 종속</b></td><td>완전 함수 종속</td></tr><tr><td><b>3NF</b></td><td><b>이행 함수 종속</b></td><td>A→B→C 제거</td></tr><tr><td><b>BCNF</b></td><td>후보키 아닌 결정자</td><td>모든 결정자 = 후보키</td></tr></table><div class="tip"><b>이행 함수 종속:</b> A→B, B→C → A→C 성립 (3NF에서 제거)</div>`},
    {num:'5',name:'키(Key) · 무결성 · RAID',p:'⭐',b:`<div class="mnemo">슈퍼키→후보키→기본키+대체키</div><table class="rt"><tr><th>키</th><th>유일성</th><th>최소성</th></tr><tr><td><b>슈퍼키</b></td><td>✅</td><td>❌</td></tr><tr><td><b>후보키</b></td><td>✅</td><td>✅</td></tr><tr><td><b>기본키(PK)</b></td><td>✅ NOT NULL</td><td>✅</td></tr><tr><td><b>대체키</b></td><td>✅</td><td>✅</td></tr><tr><td><b>외래키(FK)</b></td><td>NULL 가능</td><td>—</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>RAID</th><th>방식</th><th>최소 디스크</th></tr><tr><td><b>RAID 0</b></td><td>스트라이핑, 패리티 없음</td><td>2개</td></tr><tr><td><b>RAID 1</b></td><td>미러링</td><td>2개</td></tr><tr><td><b>RAID 5</b></td><td>스트라이핑+분산패리티</td><td>3개</td></tr><tr><td><b>RAID 6</b></td><td>이중분산패리티</td><td>4개</td></tr></table>`},
    ],
    net:[
    {num:'1',name:'메모리 교체 + 스케줄링',p:'⭐',b:`<table class="rt"><tr><th>교체 알고리즘</th><th>기준</th><th>특이사항</th></tr><tr><td><b>FIFO</b></td><td>먼저 들어온 것</td><td>Belady 이상 발생</td></tr><tr><td><b>LRU</b></td><td>가장 오래 미참조</td><td>가장 많이 사용</td></tr><tr><td><b>LFU</b></td><td>참조 횟수 최소</td><td>동률 시 FIFO</td></tr><tr><td><b>OPT</b></td><td>앞으로 가장 안쓸 것</td><td>이론상 최적, 구현 불가</td></tr></table><div class="tip"><b>Belady's Anomaly:</b> FIFO에서 프레임 수↑ → Page Fault가 오히려 ↑</div><table class="rt" style="margin-top:8px"><tr><th>스케줄링</th><th>선점</th><th>핵심</th></tr><tr><td><b>FIFO</b></td><td>비선점</td><td>도착 순서</td></tr><tr><td><b>SJF</b></td><td>비선점</td><td>짧은 것 먼저</td></tr><tr><td><b>Round Robin</b></td><td>선점</td><td>FIFO+시간할당량</td></tr><tr><td><b>SRT</b></td><td>선점</td><td>선점형 SJF</td></tr><tr><td><b>HRN</b></td><td>비선점</td><td>SJF+대기시간 고려</td></tr></table>`},
    {num:'2',name:'라우팅 프로토콜 + 네트워크 계층',p:'⭐',b:`<table class="rt"><tr><th>프로토콜</th><th>알고리즘</th><th>분류</th><th>특징</th></tr><tr><td><b>RIP</b></td><td>거리 벡터(벨만-포드)</td><td>IGP</td><td>홉 수 기준, 최대 15홉</td></tr><tr><td><b>OSPF</b></td><td>링크 상태(다익스트라)</td><td>IGP</td><td>비용 기준, 대규모</td></tr><tr><td><b>BGP</b></td><td>경로 벡터</td><td>EGP</td><td>AS 간 라우팅</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>프로토콜</th><th>역할</th></tr><tr><td><b>ARP</b></td><td>IP→MAC 주소 변환</td></tr><tr><td><b>RARP</b></td><td>MAC→IP 주소 변환</td></tr><tr><td><b>ICMP</b></td><td>오류 전송 (Ping)</td></tr><tr><td><b>NAT</b></td><td>사설IP→공인IP 변환</td></tr></table>`},
    {num:'3',name:'응용 계층 포트번호 (암기 필수)',p:'🔥',b:`<div class="mnemo">22 23 25 53 80 110 143 443 — 순서대로 외워!</div><table class="rt"><tr><th>포트</th><th>프로토콜</th><th>역할</th></tr><tr><td><b>22</b></td><td>SSH</td><td>암호화 원격접속</td></tr><tr><td><b>23</b></td><td>Telnet</td><td>평문 원격접속</td></tr><tr><td><b>25</b></td><td>SMTP</td><td>메일 발송</td></tr><tr><td><b>53</b></td><td>DNS</td><td>도메인→IP 변환</td></tr><tr><td><b>80</b></td><td>HTTP</td><td>웹</td></tr><tr><td><b>110</b></td><td>POP3</td><td>메일 수신(다운로드)</td></tr><tr><td><b>143</b></td><td>IMAP</td><td>메일 수신(동기화)</td></tr><tr><td><b>443</b></td><td>HTTPS</td><td>HTTP+SSL/TLS</td></tr></table>`},
    {num:'4',name:'HDLC·Shell Script·오류제어·IPv6',p:'🔥',b:`<table class="rt"><tr><th>HDLC 프레임</th><th>비트</th><th>역할</th></tr><tr><td><b>I 프레임</b></td><td>0</td><td>데이터 전달</td></tr><tr><td><b>S 프레임</b></td><td>10</td><td>오류/흐름 제어</td></tr><tr><td><b>U 프레임</b></td><td>11</td><td>링크 동작 모드 설정</td></tr></table><div class="tip"><b>chmod 754:</b> 사용자(7=rwx), 그룹(5=r-x), 기타(4=r--)<br>r=4, w=2, x=1<br><b>FEC:</b> 스스로 수정 (해밍코드) / <b>BEC/ARQ:</b> 재전송 요청 (CRC, 패리티)<br><b>IPv6:</b> 128비트, 16진수 8그룹, :(콜론)으로 구분</div>`},
    ],
    sw:[
    {num:'1',name:'테스트 커버리지 · 블랙박스 기법',p:'⭐',b:`<div class="mnemo">커버리지 강도: 구문 &lt; 결정 &lt; 조건 &lt; 조건/결정 &lt; MC/DC</div><table class="rt"><tr><th>커버리지</th><th>핵심</th></tr><tr><td><b>구문(Statement)</b></td><td>모든 명령문 1회 이상 실행</td></tr><tr><td><b>결정(Branch)</b></td><td>결정문 T/F 모두</td></tr><tr><td><b>조건</b></td><td>각 개별 조건식 T/F</td></tr><tr><td><b>MC/DC</b></td><td>개별 조건 독립적 영향</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>블랙박스</th><th>핵심</th></tr><tr><td><b>동등 분할</b></td><td>유효값/무효값 그룹핑 후 대표값</td></tr><tr><td><b>경곗값 분석</b></td><td>경계값 집중 테스트</td></tr><tr><td><b>결정 테이블</b></td><td>조건·행동 표로 정리</td></tr><tr><td><b>상태 전이</b></td><td>상태 변화 기반</td></tr><tr><td><b>오류 예측</b></td><td>경험/직관으로 예측</td></tr></table>`},
    {num:'2',name:'테스트 자동화 · 레벨 · VPN',p:'🔥',b:`<table class="rt"><tr><th>구성요소</th><th>역할</th></tr><tr><td><b>테스트 드라이버</b></td><td><b>상향식</b> — 상위 모듈 역할 임시 대체</td></tr><tr><td><b>테스트 스텁</b></td><td><b>하향식</b> — 하위 모듈 역할 임시 대체</td></tr><tr><td><b>테스트 하네스</b></td><td>테스트 환경 구축 도구</td></tr><tr><td><b>테스트 슈트</b></td><td>테스트 케이스 집합</td></tr></table><div class="flow" style="margin-top:8px"><span class="s">단위</span><span class="a">→</span><span class="s">통합</span><span class="a">→</span><span class="s">시스템</span><span class="a">→</span><span class="s">인수</span></div><div class="tip"><b>알파:</b> 개발자 환경 / <b>베타:</b> 개발자 없이 사용자 수행</div><table class="rt" style="margin-top:8px"><tr><th>VPN 프로토콜</th><th>계층</th></tr><tr><td><b>PPTP</b></td><td>데이터링크</td></tr><tr><td><b>L2TP</b></td><td>데이터링크 (L2F+PPTP)</td></tr><tr><td><b>IPSec</b></td><td>네트워크 (가장 강력)</td></tr><tr><td><b>SSL/TLS</b></td><td>전송 (HTTPS 기반)</td></tr></table>`},
    {num:'3',name:'데이터 형식 · 웹 서비스',p:'🤔',b:`<table class="rt"><tr><th>형식</th><th>주석</th><th>특징</th></tr><tr><td><b>JSON</b></td><td>❌</td><td>key-value, 경량, 현대 표준</td></tr><tr><td><b>XML</b></td><td>✅</td><td>태그(&lt;&gt;), 확장성</td></tr><tr><td><b>YAML</b></td><td>✅(#)</td><td>들여쓰기, 사람 친화적</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>웹서비스</th><th>특징</th></tr><tr><td><b>SOAP</b></td><td>XML 메시지</td></tr><tr><td><b>REST</b></td><td>HTTP+JSON, 현대 표준</td></tr><tr><td><b>UDDI</b></td><td>웹서비스 검색 레지스트리</td></tr><tr><td><b>WSDL</b></td><td>XML로 인터페이스 기술</td></tr></table>`},
    ],
    des:[
    {num:'1',name:'생성 패턴 5가지 (싱팩빌프앱)',p:'💯',b:`<div class="mnemo">싱팩빌프앱 → 자주 출제!</div><table class="rt"><tr><th>패턴</th><th>핵심 설명</th></tr><tr><td><b>싱글톤</b></td><td>인스턴스 <b>하나만</b> 생성, 전역 접근</td></tr><tr><td><b>팩토리 메서드</b></td><td>상위=인터페이스, 서브클래스=실제 생성</td></tr><tr><td><b>빌더</b></td><td>단계별 복잡한 객체 생성</td></tr><tr><td><b>프로토타입</b></td><td>인스턴스 <b>복제(clone)</b></td></tr><tr><td><b>앱스트랙트 팩토리</b></td><td>관련 객체 조합 인터페이스 (Kit)</td></tr></table>`},
    {num:'2',name:'구조 패턴 7가지 (어데퍼프브플컴)',p:'💯',b:`<div class="mnemo">어데퍼프브플컴</div><table class="rt"><tr><th>패턴</th><th>핵심 설명</th></tr><tr><td><b>어댑터</b></td><td>다른 인터페이스 <b>연결</b> (변환기)</td></tr><tr><td><b>데코레이터</b></td><td>객체 감싸서 기능 <b>동적 추가</b></td></tr><tr><td><b>퍼사드</b></td><td>복잡한 내부를 단순 인터페이스로</td></tr><tr><td><b>프록시</b></td><td><b>대리 객체</b>가 실제 객체 대신 처리</td></tr><tr><td><b>브리지</b></td><td>기능/구현 클래스 분리</td></tr><tr><td><b>플라이웨이트</b></td><td>공유로 <b>메모리 절약</b></td></tr><tr><td><b>컴포지트</b></td><td><b>트리 구조</b>, 복합/단일 동일 처리</td></tr></table>`},
    {num:'3',name:'행위 패턴 9가지 (전옵중방이상인매커책템)',p:'💯',b:`<table class="rt"><tr><th>패턴</th><th>핵심 설명</th></tr><tr><td><b>전략(Strategy)</b></td><td>알고리즘 캡슐화, 동적 교체</td></tr><tr><td><b>옵저버(Observer)</b></td><td>상태변화 → 의존 객체 <b>자동 알림</b></td></tr><tr><td><b>커맨드</b></td><td>요청을 객체로 캡슐화 (Undo)</td></tr><tr><td><b>이터레이터</b></td><td>컬렉션 <b>순차 탐색</b> (Cursor)</td></tr><tr><td><b>템플릿 메서드</b></td><td>상위=골격, 하위=세부 구체화</td></tr><tr><td><b>상태(State)</b></td><td>상태에 따라 행동 변경</td></tr><tr><td><b>방문자(Visitor)</b></td><td>메서드가 각 클래스 순회</td></tr><tr><td><b>책임연쇄</b></td><td>요청 처리 체인 연결</td></tr><tr><td><b>중재자</b></td><td>객체 간 통신 <b>중앙 관리</b></td></tr></table>`},
    {num:'4',name:'응집도·결합도·SOLID',p:'🔥',b:`<div class="mnemo">응집도 강→약: 기순통절시논우 (기능적=최선)</div><div class="mnemo" style="margin-top:6px">결합도 약→강: 자스제외공내 (자료=최선)</div><table class="rt"><tr><th>SOLID</th><th>원칙</th><th>핵심</th></tr><tr><td><b>SRP</b></td><td>단일 책임</td><td>클래스 = 하나의 책임</td></tr><tr><td><b>OCP</b></td><td>개방-폐쇄</td><td>확장O 변경X</td></tr><tr><td><b>LSP</b></td><td>리스코프 치환</td><td>자식이 부모 대체 가능</td></tr><tr><td><b>ISP</b></td><td>인터페이스 분리</td><td>안쓰는 메서드 의존X</td></tr><tr><td><b>DIP</b></td><td>의존성 역전</td><td>고수준이 저수준 의존X</td></tr></table>`},
    {num:'5',name:'UML 다이어그램·클래스 관계',p:'🤔',b:`<div class="mnemo">정적 6: 클·객·컴·배·복·패 / 동적 7: 유·시·커·상·활·타·협</div><table class="rt"><tr><th>관계</th><th>표기</th><th>의미</th></tr><tr><td><b>복합(Composition)</b></td><td>◆ 채운 마름모</td><td>강한 소유, 생명주기 공유</td></tr><tr><td><b>집합(Aggregation)</b></td><td>◇ 빈 마름모</td><td>약한 소유</td></tr><tr><td><b>연관(Association)</b></td><td>─→</td><td>서로 연결</td></tr><tr><td><b>의존(Dependency)</b></td><td>⇢ 점선</td><td>짧은 시간 연관</td></tr><tr><td><b>일반화(상속)</b></td><td>─▷ 실선 빈삼각</td><td>상속</td></tr><tr><td><b>실체화(구현)</b></td><td>--▷ 점선 빈삼각</td><td>인터페이스 구현</td></tr></table>`},
    ],
    sec:[
    {num:'1',name:'DoS 공격 종류',p:'🔥',b:`<table class="rt"><tr><th>공격</th><th>핵심 키워드</th></tr><tr><td><b>랜드 어택</b></td><td>출발지IP = 목적지IP 동일하게 위조</td></tr><tr><td><b>스머프(Smurf)</b></td><td>ICMP Echo + 브로드캐스팅 → 증폭</td></tr><tr><td><b>티어드롭</b></td><td>IP Fragment 조립 과정에서 오류 유발</td></tr><tr><td><b>죽음의 핑</b></td><td>과도하게 큰 ICMP 패킷 전송</td></tr><tr><td><b>SYN 플러딩</b></td><td>3-way handshake 미완료, SYN만 전송</td></tr></table><div class="tip"><b>DoS:</b> 단일 시스템<br><b>DDoS:</b> 다수 분산 시스템<br><b>DRDoS:</b> IP 스푸핑 + 정상 제3 서버(반사체) 이용, 증폭</div>`},
    {num:'2',name:'네트워크 공격 · 악성코드',p:'🔥',b:`<table class="rt"><tr><th>공격</th><th>핵심</th></tr><tr><td><b>ARP 스푸핑</b></td><td>MAC 주소 위조, 트래픽 가로채기</td></tr><tr><td><b>세션 하이재킹</b></td><td>handshake 완료 후 세션 탈취</td></tr><tr><td><b>레인보우 테이블</b></td><td>미리 계산된 해시값으로 패스워드 역추적</td></tr><tr><td><b>무차별 공격</b></td><td>모든 문자 조합 대입 (Brute-force)</td></tr><tr><td><b>사전 공격</b></td><td>사전 단어 대입 (Dictionary)</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>악성코드</th><th>특징</th></tr><tr><td><b>웜(Worm)</b></td><td>자가 복제 + 자율 전파, 숙주 불필요</td></tr><tr><td><b>바이러스</b></td><td>실행파일 기생, 자율 전파 없음</td></tr><tr><td><b>트로이 목마</b></td><td>정상 프로그램 위장, 자기복제 없음</td></tr></table>`},
    {num:'3',name:'암호화 알고리즘',p:'⭐',b:`<div class="tip"><b>대칭키:</b> 암복호화 키 동일, 빠름<br><b>비대칭키:</b> 공개키+개인키, 느림<br><b>해시:</b> 단방향, 복호화 불가</div><table class="rt"><tr><th>대칭키(블록)</th><th>특징</th></tr><tr><td><b>DES</b></td><td>IBM, 블록 64비트 (취약, 구식)</td></tr><tr><td><b>AES</b></td><td>DES 대체, 블록 128비트, 현재 표준</td></tr><tr><td><b>SEED</b></td><td>KISA 개발, 한국 최초 표준</td></tr><tr><td><b>Skipjack</b></td><td>음성 암호화에 주로 사용</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>비대칭키</th><th>기반</th></tr><tr><td><b>디피-헬만</b></td><td>최초 공개키, 이산 로그</td></tr><tr><td><b>RSA</b></td><td>소인수분해</td></tr><tr><td><b>ECC</b></td><td>타원곡선, 짧은 키</td></tr></table><table class="rt" style="margin-top:8px"><tr><th>해시</th><th>비트 수</th></tr><tr><td><b>MD5</b></td><td>128비트</td></tr><tr><td><b>SHA-1</b></td><td>160비트</td></tr><tr><td><b>SHA-256</b></td><td>256비트 (현재 표준)</td></tr></table>`},
    {num:'4',name:'접근통제 · 3A · 인증 · 클라우드',p:'🤔',b:`<table class="rt"><tr><th>접근 통제</th><th>기반</th><th>특징</th></tr><tr><td><b>DAC(임의적)</b></td><td>신분/식별자</td><td>소유자가 직접 허용</td></tr><tr><td><b>MAC(강제적)</b></td><td>규칙/등급</td><td>강력한 중앙 통제</td></tr><tr><td><b>RBAC(역할기반)</b></td><td>역할(Role)</td><td>중앙 관리자</td></tr></table><div class="tip"><b>3A:</b> Authentication(인증) · Authorization(권한부여) · Accounting(계정)<br><b>SSO:</b> 커버로스 사용, 한번 인증→여러 자원<br><b>OTP:</b> 일회용 비밀번호, 단방향 해시<br><b>IaaS/PaaS/SaaS:</b> 인프라/플랫폼/소프트웨어</div>`},
    ],
    };
    const FC = {
    db:[
    {front:'다음이 설명하는 SQL 명령어\n\n기존 테이블의 데이터를 변경할 때 사용하며\n"SET 컬럼=값 WHERE 조건" 형식으로 사용',back:'UPDATE',hint:'DML'},
    {front:'UNION vs UNION ALL\n\n중복을 제거하는 것 / 중복을 허용하는 것',back:'UNION = 중복 제거\nUNION ALL = 중복 허용',hint:'집합연산자'},
    {front:'권한을 부여하는 SQL 명령어\n권한을 회수하는 SQL 명령어',back:'부여: GRANT … ON … TO\n회수: REVOKE … ON … FROM',hint:'DCL'},
    {front:'트랜잭션 ACID\nAll or Nothing을 의미하는 특성',back:'원자성 (Atomicity)',hint:'ACID'},
    {front:'트랜잭션 회복\nStart O + Commit O 일 때',back:'Redo (재실행)\n— 완료된 트랜잭션 복구',hint:'회복 기법'},
    {front:'트랜잭션 회복\nStart O + Commit X 일 때',back:'Undo (취소)\n— 작업 전부 취소',hint:'회복 기법'},
    {front:'읽기 시 사용, 동시 읽기 가능\n쓰기는 불가능한 Lock',back:'S-Lock (공유 락, Shared Lock)',hint:'동시성 제어'},
    {front:'2NF가 제거하는 종속\n기본키 일부에만 종속된 속성',back:'부분 함수 종속',hint:'정규화'},
    {front:'A→B이고 B→C일 때 A→C가 성립\n3NF에서 제거하는 대상',back:'이행 함수 종속 (Transitive)',hint:'정규화'},
    {front:'유일성 O + 최소성 O\nPK가 될 수 있는 키',back:'후보키 (Candidate Key)',hint:'키 종류'},
    {front:'스트라이핑 + 분산 패리티\n최소 3개 디스크 필요',back:'RAID 5',hint:'RAID'},
    {front:'오라클에서 차집합 연산자\n표준 SQL의 EXCEPT에 해당',back:'MINUS',hint:'집합연산자'},
    {front:'GROUP BY 후 집계 결과에 조건\nWHERE와의 차이점',back:'HAVING\n(WHERE는 그룹화 전 조건)',hint:'SQL'},
    {front:'외부 스키마 / 개념 스키마 / 내부 스키마\n각각 어떤 관점?',back:'외부=사용자·개발자\n개념=DBA 전체구조\n내부=물리적 저장',hint:'DB 스키마'},
    ],
    net:[
    {front:'가장 오랫동안 참조되지 않은 페이지를 교체\n가장 널리 쓰이는 교체 알고리즘',back:'LRU\n(Least Recently Used)',hint:'메모리 교체'},
    {front:'프레임 수를 늘렸는데 Page Fault가 오히려 증가\nFIFO에서 발생하는 이상 현상',back:"Belady's Anomaly\n(벨라디 이상 현상)",hint:'메모리 교체'},
    {front:'선점형 SJF\n더 짧은 프로세스 도착 시 즉시 선점',back:'SRT\n(Shortest Remaining Time)',hint:'스케줄링'},
    {front:'IP 주소 → MAC 주소 변환\nMAC 주소 → IP 주소 변환',back:'ARP (IP→MAC)\nRARP (MAC→IP)',hint:'네트워크 계층'},
    {front:'메일 발송 포트번호\n메일 수신(동기화) 포트번호\n암호화 원격접속 포트번호',back:'SMTP: 25\nIMAP: 143\nSSH: 22',hint:'포트번호'},
    {front:'HTTP 포트번호\nHTTPS 포트번호\nDNS 포트번호',back:'HTTP: 80\nHTTPS: 443\nDNS: 53',hint:'포트번호'},
    {front:'거리 벡터(벨만-포드) 알고리즘 사용\n홉 수 기준, 최대 15홉, IGP',back:'RIP',hint:'라우팅'},
    {front:'링크 상태(다익스트라) 알고리즘\n비용 기준, 대규모 네트워크, IGP',back:'OSPF',hint:'라우팅'},
    {front:'AS 간 라우팅\n경로 벡터 알고리즘, EGP',back:'BGP',hint:'라우팅'},
    {front:'HDLC 프레임 비트 0\n데이터 전달 담당',back:'I 프레임 (정보 프레임)',hint:'HDLC'},
    {front:'chmod 754\n사용자 / 그룹 / 기타 권한',back:'사용자: rwx (7)\n그룹: r-x (5)\n기타: r-- (4)',hint:'Shell Script'},
    {front:'스스로 오류 검출·수정\n대표적 기법: 해밍 코드',back:'FEC (전진 오류 수정)\nForward Error Correction',hint:'오류 제어'},
    ],
    sw:[
    {front:'테스트 커버리지 강도 순서',back:'구문 < 결정 < 조건 < 조건/결정 < MC/DC',hint:'커버리지'},
    {front:'상향식 테스트에서\n아직 구현되지 않은 상위 모듈 역할 임시 대체',back:'테스트 드라이버 (Driver)',hint:'테스트 자동화'},
    {front:'하향식 테스트에서\n아직 구현되지 않은 하위 모듈 역할 임시 대체',back:'테스트 스텁 (Stub)',hint:'테스트 자동화'},
    {front:'테스트 레벨 순서',back:'단위 → 통합 → 시스템 → 인수',hint:'테스트 레벨'},
    {front:'개발자 환경, 통제된 상태에서 수행\nvs\n개발자 없이 사용자 직접 수행',back:'알파(Alpha) vs 베타(Beta) 테스트',hint:'인수 테스트'},
    {front:'IP 패킷 단위로 암호화\n네트워크 계층, 가장 강력한 VPN',back:'IPSec',hint:'VPN'},
    {front:'L2F와 PPTP를 결합한 VPN\n데이터링크 계층',back:'L2TP',hint:'VPN'},
    {front:'JSON은 주석 가능? 불가?\nYAML은 주석 가능? 불가?',back:'JSON: 주석 불가 ❌\nYAML: 주석 가능 ✅ (# 사용)',hint:'데이터 형식'},
    ],
    des:[
    {front:'다음이 설명하는 디자인 패턴\n\n클래스 인스턴스를 오직 하나만 생성하고\n어디서든 이 인스턴스에 접근할 수 있게 함',back:'싱글톤 (Singleton)\n생성 패턴',hint:'디자인 패턴'},
    {front:'다음이 설명하는 디자인 패턴\n\n한 객체의 상태가 바뀌면 그 객체에 의존하는\n다른 객체들에게 자동으로 알림을 보내는 패턴',back:'옵저버 (Observer)\n행위 패턴 / 발행-수신 모델',hint:'디자인 패턴'},
    {front:'다음이 설명하는 디자인 패턴\n\n대리 객체(Surrogate)가 실제 객체 대신\n요청을 처리하고 흐름을 제어하는 패턴',back:'프록시 (Proxy)\n구조 패턴',hint:'디자인 패턴'},
    {front:'다음이 설명하는 디자인 패턴\n\n서로 다른 인터페이스를 가진 클래스들을\n함께 사용할 수 있도록 변환하는 패턴',back:'어댑터 (Adapter)\n구조 패턴',hint:'디자인 패턴'},
    {front:'다음이 설명하는 디자인 패턴\n\n객체를 복제(clone)하여 새로운 인스턴스를\n생성하는 패턴',back:'프로토타입 (Prototype)\n생성 패턴',hint:'디자인 패턴'},
    {front:'다음이 설명하는 디자인 패턴\n\n컬렉션의 내부를 노출하지 않고\n모든 요소를 순차적으로 접근하는 패턴\nCursor라고도 불림',back:'이터레이터 (Iterator)\n행위 패턴',hint:'디자인 패턴'},
    {front:'응집도 강도 순서 (강→약)',back:'기능적 > 순차적 > 통신적 > 절차적\n> 시간적 > 논리적 > 우연적',hint:'응집도'},
    {front:'결합도 강도 순서 (약→강)',back:'자료 < 스탬프 < 제어 < 외부\n< 공통 < 내용',hint:'결합도'},
    {front:'OCP 원칙\n개방-폐쇄 원칙',back:'확장에는 열려 있고\n변경에는 닫혀 있어야 함',hint:'SOLID'},
    {front:'클래스다이어그램\n◆ 채운 마름모 vs ◇ 빈 마름모',back:'◆ 복합(Composition): 강한 소유, 생명주기 공유\n◇ 집합(Aggregation): 약한 소유',hint:'UML'},
    {front:'럼바우 3가지 모델링\n각각의 산출물',back:'객체모델링 → ER 다이어그램\n동적모델링 → 상태 다이어그램\n기능모델링 → 자료흐름도(DFD)',hint:'럼바우'},
    ],
    sec:[
    {front:'다음이 설명하는 공격\n\n패킷의 출발지 IP와 목적지 IP를 동일하게 설정하여\n서버가 자기 자신에게 응답하게 만드는 공격',back:'랜드 어택 (LAND Attack)',hint:'DoS 공격'},
    {front:'다음이 설명하는 공격\n\nICMP Echo 패킷을 브로드캐스트로 전송하여\n네트워크 전체가 피해자에게 응답하도록 유도',back:'스머프 (Smurf) 공격',hint:'DoS 공격'},
    {front:'다음이 설명하는 공격\n\nTCP 3-way handshake를 완료하지 않고\nSYN 패킷만 대량 전송하여 서버 자원 고갈',back:'SYN 플러딩 (SYN Flooding)',hint:'DoS 공격'},
    {front:'다음이 설명하는 악성코드\n\n숙주 프로그램 없이 자가 복제하고\n네트워크를 통해 자율적으로 전파',back:'웜 (Worm)',hint:'악성코드'},
    {front:'DES의 단점을 보완한 현재 대칭키 표준\n블록 크기 128비트',back:'AES (Advanced Encryption Standard)',hint:'암호화 알고리즘'},
    {front:'한국인터넷진흥원(KISA)이 개발한\n한국 최초 블록 암호화 표준',back:'SEED',hint:'암호화 알고리즘'},
    {front:'소인수분해를 기반으로 하는\n공개키 비대칭 암호화 알고리즘',back:'RSA',hint:'비대칭키'},
    {front:'역할(Role)에 기초하여\n중앙 관리자가 접근 권한을 관리하는 방식',back:'RBAC (역할기반 접근통제)\nRole Based Access Control',hint:'접근 통제'},
    {front:'커버로스(Kerberos)를 사용\n한번 로그인으로 여러 시스템/서비스 이용',back:'SSO (Single Sign-On)',hint:'인증'},
    {front:'IP 스푸핑 + 정상적인 제3 서버를 반사체로 이용\n증폭 효과로 피해 극대화',back:'DRDoS\n(Distributed Reflection DoS)',hint:'분산 공격'},
    ],
    };
    const QZ = {
    db:[
    {type:'단답형',s:'SQL',q:`다음이 설명하는 SQL 명령어를 쓰시오.\n\n기존 테이블에 새로운 데이터를 추가할 때 사용하며, 다음과 같은 형식으로 사용한다.\n\n  ___ INTO 테이블명(컬럼1, 컬럼2) VALUES(값1, 값2);`,ans:['INSERT','insert'],disp:'INSERT',exp:'INSERT INTO 테이블명(컬럼) VALUES(값); — DML 중 삽입 명령어'},
    {type:'단답형',s:'SQL',q:`다음이 설명하는 SQL 명령어를 쓰시오.\n\n특정 사용자에게 테이블에 대한 SELECT, INSERT 등의 권한을 부여하는 DCL 명령어이다. 반대로 권한을 회수하는 명령어는 REVOKE이다.`,ans:['GRANT','grant'],disp:'GRANT',exp:'GRANT 권한 ON 테이블 TO 사용자;\\nREVOKE 권한 ON 테이블 FROM 사용자;'},
    {type:'단답형',s:'SQL',q:`다음 두 집합 연산자의 차이를 빈칸에 쓰시오.\n\nUNION     : 두 SELECT 결과를 합치며 (   ①   )을 제거한다.\nUNION ALL : 두 SELECT 결과를 합치며 (   ①   )을 제거하지 않는다.\n\n①에 들어갈 말을 쓰시오.`,ans:['중복','duplicate','중복행','중복 행'],disp:'중복',exp:'UNION: 중복 제거 / UNION ALL: 중복 유지'},
    {type:'단답형',s:'SQL',q:`다음이 설명하는 SQL 절(Clause)을 쓰시오.\n\nGROUP BY 절로 그룹화한 이후, 집계 함수 결과에 조건을 적용할 때 사용한다. WHERE 절은 그룹화 전에 조건을 적용하지만 이 절은 그룹화 후에 적용한다.`,ans:['HAVING','having'],disp:'HAVING',exp:'WHERE: 그룹화 전 조건 / HAVING: GROUP BY 후 집계에 조건'},
    {type:'단답형',s:'트랜잭션',q:`트랜잭션의 특성 중 다음이 설명하는 것을 쓰시오.\n\n트랜잭션의 연산은 데이터베이스에 모두 반영되든지 아니면 전혀 반영되지 않아야 한다. 즉, 트랜잭션 내의 모든 명령은 반드시 완벽히 수행되어야 하며, 모두 실행되지 못한 경우엔 되돌려야 한다.\n(All or Nothing)`,ans:['원자성','atomicity','Atomicity'],disp:'원자성 (Atomicity)',exp:'ACID 중 원자성: All or Nothing. 전부 실행되거나 하나도 실행 안 됨'},
    {type:'단답형',s:'트랜잭션',q:`다음 괄호 안에 알맞은 것을 쓰시오.\n\n트랜잭션 회복 기법에서 로그 파일을 분석한 결과, Start 기록은 있지만 Commit 기록이 없는 트랜잭션은 (    ) 연산을 수행하여 작업 이전 상태로 되돌린다.`,ans:['Undo','undo','취소'],disp:'Undo',exp:'Start O + Commit X → Undo (취소)\\nStart O + Commit O → Redo (재실행)'},
    {type:'단답형',s:'트랜잭션',q:`다음이 설명하는 Lock의 종류를 쓰시오.\n\n트랜잭션이 데이터를 읽을 때 설정하는 잠금으로, 여러 트랜잭션이 동시에 이 잠금을 설정하고 읽기를 수행할 수 있지만, 쓰기는 불가능하다.`,ans:['S-Lock','s-lock','공유락','공유 락','Shared Lock','shared lock'],disp:'S-Lock (공유 락)',exp:'S-Lock: 읽기 시, 동시 읽기 가능, 쓰기 불가\\nX-Lock(배타락): 읽기·쓰기 모두 불가'},
    {type:'단답형',s:'정규화',q:`다음이 설명하는 정규화 단계를 쓰시오.\n\n릴레이션에서 부분 함수 종속을 제거하여 완전 함수 종속으로 만드는 과정이다. 기본키의 일부 속성에만 종속된 속성들을 별도의 릴레이션으로 분리한다.`,ans:['2NF','제2정규형','2차 정규형','제 2 정규형'],disp:'제2정규형 (2NF)',exp:'2NF: 부분 함수 종속 제거 / 3NF: 이행 함수 종속 제거'},
    {type:'단답형',s:'정규화',q:`다음 빈칸에 들어갈 알맞은 용어를 쓰시오.\n\nA→B이고 B→C일 때 A→C가 성립하는 경우를 (    )(이)라고 한다. 제3정규형(3NF)은 이것을 제거하는 것을 목표로 한다.`,ans:['이행함수종속','이행 함수 종속','이행적 함수 종속','Transitive Functional Dependency'],disp:'이행 함수 종속',exp:'이행 함수 종속: A→B, B→C → A→C 성립. 3NF에서 제거'},
    {type:'단답형',s:'키(Key)',q:`다음이 설명하는 키의 종류를 쓰시오.\n\n릴레이션에서 튜플을 유일하게 식별할 수 있는 속성들의 집합 중, 최소성을 만족하는 키이다. 기본키(Primary Key)가 될 수 있는 모든 키를 의미한다.`,ans:['후보키','Candidate Key','candidate key'],disp:'후보키 (Candidate Key)',exp:'후보키 = 유일성O + 최소성O / 슈퍼키 = 유일성O + 최소성X'},
    {type:'단답형',s:'SQL',q:`다음이 설명하는 SQL 연산자를 쓰시오.\n\n두 테이블에서 서로 관련된 컬럼명이 같을 때 ON 조건 없이 자동으로 매칭하여 조인하며, 결과에서 중복 컬럼을 제거하는 조인 방식이다.`,ans:['NATURAL JOIN','natural join','자연조인','자연 조인'],disp:'NATURAL JOIN',exp:'NATURAL JOIN: 공통 컬럼 자동 매칭, ON 없음, 중복 컬럼 제거'},
    {type:'단답형',s:'RAID',q:`다음이 설명하는 RAID 레벨을 쓰시오.\n\n스트라이핑과 분산 패리티를 결합한 방식으로, 최소 3개의 디스크가 필요하다. 하나의 디스크에 장애가 발생해도 데이터를 복구할 수 있으며, 성능과 안정성의 균형이 좋다.`,ans:['RAID 5','RAID5','raid 5','raid5'],disp:'RAID 5',exp:'RAID 5: 스트라이핑+분산패리티, 최소 3개, 1개 장애 허용'},
    {type:'단답형',s:'무결성',q:`다음이 설명하는 무결성 제약 조건을 쓰시오.\n\n기본키(Primary Key)로 설정된 속성은 NULL 값을 가질 수 없고, 각 튜플을 유일하게 식별할 수 있어야 한다는 조건이다.`,ans:['개체무결성','개체 무결성','Entity Integrity'],disp:'개체 무결성',exp:'개체 무결성: PK = NOT NULL + 유일\\n참조 무결성: FK = 참조 PK값 or NULL'},
    {type:'단답형',s:'관계대수',q:`관계대수 연산자 중 다음이 설명하는 것의 기호를 쓰시오.\n\n수평적 연산으로, 릴레이션에서 조건을 만족하는 튜플(행)만을 선택하는 연산이다. SQL의 WHERE 절에 해당한다.`,ans:['σ','시그마','Sigma'],disp:'σ (시그마, Select 연산)',exp:'σ = 셀렉트(수평, 행 선택) / π = 프로젝트(수직, 열 선택)'},
    ],
    net:[
    {type:'단답형',s:'메모리 교체',q:`다음이 설명하는 페이지 교체 알고리즘을 쓰시오.\n\n메모리에서 가장 오랫동안 사용하지 않은 페이지를 교체한다. 참조된 페이지를 목록의 최상위로 이동시키는 방식으로 구현되며, 성능이 우수하여 실제로 가장 많이 사용되는 알고리즘이다.`,ans:['LRU','lru','LRU 알고리즘','Least Recently Used'],disp:'LRU (Least Recently Used)',exp:'LRU: 가장 오래 미참조 교체 / LFU: 참조횟수 최소 / FIFO: 먼저 들어온 것'},
    {type:'단답형',s:'메모리 교체',q:`다음이 설명하는 현상을 무엇이라 하는가?\n\nFIFO 페이지 교체 알고리즘에서 프레임의 수를 늘렸음에도 불구하고 페이지 폴트(Page Fault)의 수가 오히려 증가하는 현상이다.`,ans:["Belady's Anomaly","belady's anomaly","벨라디","벨라디의 이상","Belady Anomaly","belady anomaly"],disp:"Belady's Anomaly (벨라디 이상 현상)",exp:'FIFO 알고리즘에서만 발생, 프레임↑ → Page Fault↑'},
    {type:'단답형',s:'스케줄링',q:`다음이 설명하는 CPU 스케줄링 알고리즘을 쓰시오.\n\nSJF(Shortest Job First) 알고리즘의 선점형 버전으로, 현재 실행 중인 프로세스보다 남은 실행시간이 더 짧은 프로세스가 도착하면 즉시 CPU를 빼앗는다.`,ans:['SRT','srt','SRT 알고리즘','Shortest Remaining Time'],disp:'SRT (Shortest Remaining Time)',exp:'SRT = 선점형 SJF / SJF = 비선점형'},
    {type:'단답형',s:'라우팅',q:`다음이 설명하는 라우팅 프로토콜을 쓰시오.\n\n링크 상태(Link State) 알고리즘인 다익스트라(Dijkstra) 알고리즘을 사용하며, 경로 비용을 기준으로 최단 경로를 계산한다. IGP 계열로 대규모 네트워크에 적합하다.`,ans:['OSPF','ospf','Open Shortest Path First'],disp:'OSPF',exp:'OSPF: 링크상태·다익스트라·비용기준·IGP\\nRIP: 거리벡터·벨만포드·홉수·IGP·최대15홉'},
    {type:'단답형',s:'네트워크 계층',q:`다음이 설명하는 프로토콜을 쓰시오.\n\nIP 주소(논리 주소)를 이용하여 해당 호스트의 MAC 주소(물리 주소)를 알아내는 프로토콜이다. 반대로 MAC 주소로 IP 주소를 알아내는 것은 RARP이다.`,ans:['ARP','arp','Address Resolution Protocol'],disp:'ARP (Address Resolution Protocol)',exp:'ARP: IP→MAC / RARP: MAC→IP'},
    {type:'단답형',s:'응용 계층',q:`다음 각 프로토콜의 포트 번호를 쓰시오.\n\nSMTP:  (   ①   )\nPOP3:  (   ②   )\n\n①을 쓰시오.`,ans:['25'],disp:'25',exp:'SMTP(25): 메일 발송 / POP3(110): 메일 수신 다운로드 / IMAP(143): 메일 수신 동기화'},
    {type:'단답형',s:'응용 계층',q:`SSH 프로토콜의 포트 번호를 쓰시오.\n\nSSH는 원격 접속 시 데이터를 암호화하여 전송하는 프로토콜로, 평문으로 전송하는 Telnet(포트 23)의 보안 문제를 해결하였다.`,ans:['22'],disp:'22',exp:'SSH: 22 (암호화) / Telnet: 23 (평문) — SSH가 보안상 우수'},
    {type:'단답형',s:'HDLC',q:`다음이 설명하는 HDLC 프레임의 종류를 쓰시오.\n\n첫 번째 비트가 '10'으로 시작하는 프레임으로, 오류 제어 및 흐름 제어에 사용된다.`,ans:['S프레임','S 프레임','감시 프레임','감독 프레임','Supervisory Frame'],disp:'S 프레임 (감시 프레임)',exp:'I프레임(0): 데이터 / S프레임(10): 오류·흐름 제어 / U프레임(11): 링크 설정'},
    {type:'단답형',s:'오류 제어',q:`다음이 설명하는 오류 제어 방식을 쓰시오.\n\n수신측에서 오류를 스스로 검출하고 수정할 수 있는 방식으로, 별도의 재전송을 요구하지 않는다. 대표적인 기법으로 해밍 코드(Hamming Code)가 있다.`,ans:['FEC','fec','전진오류수정','Forward Error Correction'],disp:'FEC (전진 오류 수정)',exp:'FEC: 스스로 수정 (해밍코드)\\nBEC/ARQ: 재전송 요청 (CRC, 패리티)'},
    {type:'단답형',s:'IPv6',q:`IPv4와 비교하여 IPv6의 주소 비트 수를 쓰시오.\n\nIPv4는 32비트를 사용하지만, IPv6는 주소 공간 부족 문제를 해결하기 위해 더 많은 비트를 사용한다.`,ans:['128','128비트','128 비트'],disp:'128비트',exp:'IPv4: 32비트, 10진수, .으로 구분\\nIPv6: 128비트, 16진수, :으로 구분'},
    {type:'단답형',s:'스케줄링',q:`반환 시간을 구하는 공식을 쓰시오. 빈칸을 채우시오.\n\n반환 시간 = (    ) + 실행 시간`,ans:['대기시간','대기 시간','Waiting Time'],disp:'대기 시간',exp:'반환 시간 = 대기 시간 + 실행 시간'},
    ],
    sw:[
    {type:'단답형',s:'테스트 자동화',q:`다음이 설명하는 테스트 구성 요소를 쓰시오.\n\n상향식 통합 테스트에서 아직 개발이 완료되지 않은 상위 모듈을 대신하여 임시로 제공되는 테스트 도구이다. 하위 모듈을 테스트하기 위해 상위 모듈의 역할을 임시로 수행한다.`,ans:['테스트 드라이버','테스트드라이버','드라이버','Driver','Test Driver'],disp:'테스트 드라이버 (Driver)',exp:'드라이버: 상향식, 상위모듈 대체\\n스텁: 하향식, 하위모듈 대체'},
    {type:'단답형',s:'테스트 자동화',q:`다음이 설명하는 테스트 구성 요소를 쓰시오.\n\n하향식 통합 테스트에서 아직 개발이 완료되지 않은 하위 모듈을 대신하여 임시로 제공되는 테스트 도구이다. 상위 모듈이 호출할 때 미리 정해진 결과를 반환한다.`,ans:['테스트 스텁','테스트스텁','스텁','Stub','Test Stub'],disp:'테스트 스텁 (Stub)',exp:'스텁: 하향식, 하위모듈 대체\\n드라이버: 상향식, 상위모듈 대체'},
    {type:'단답형',s:'커버리지',q:`다음이 설명하는 테스트 커버리지를 쓰시오.\n\n각 개별 조건식이 다른 조건에 독립적으로 전체 결정의 결과에 영향을 미치는지 확인하는 커버리지로, 화이트박스 테스트 커버리지 기준 중 가장 강도가 강하다.`,ans:['MC/DC','mc/dc','MCDC','mcdc','변형조건결정 커버리지','수정 조건/결정 커버리지'],disp:'MC/DC 커버리지',exp:'커버리지 강도: 구문 < 결정 < 조건 < 조건/결정 < MC/DC (가장 강함)'},
    {type:'단답형',s:'블랙박스 테스트',q:`다음이 설명하는 블랙박스 테스트 기법을 쓰시오.\n\n입력 데이터를 유효한 값과 유효하지 않은 값으로 분류하여 각 그룹의 대표값으로 테스트하는 기법이다. 동일한 결과를 나타내는 입력 데이터들을 하나의 그룹으로 묶어 처리한다.`,ans:['동등 분할','동등분할','동치 분할','Equivalence Partitioning','동등 분할 기법'],disp:'동등 분할 (Equivalence Partitioning)',exp:'동등분할: 유효값/무효값 그룹핑 후 대표값 테스트'},
    {type:'단답형',s:'테스트 레벨',q:`다음 빈칸에 알맞은 테스트 레벨을 순서대로 쓰시오.\n\n(   ① 테스트   ) → 통합 테스트 → 시스템 테스트 → (   ② 테스트   )\n\n①을 쓰시오.`,ans:['단위','단위 테스트','유닛'],disp:'단위',exp:'단위 → 통합 → 시스템 → 인수 테스트'},
    {type:'단답형',s:'인터페이스 보안',q:`다음이 설명하는 VPN 프로토콜을 쓰시오.\n\n네트워크 계층에서 IP 패킷 단위로 암호화를 수행하는 가장 강력한 VPN 프로토콜이다. AH(Authentication Header)와 ESP(Encapsulating Security Payload) 두 가지 헤더를 사용한다.`,ans:['IPSec','ipsec','IPsec'],disp:'IPSec',exp:'IPSec: 네트워크 계층, 가장 강력\\nL2TP: 데이터링크(L2F+PPTP)\\nSSL/TLS: 전송 계층'},
    {type:'단답형',s:'데이터 형식',q:`다음이 설명하는 데이터 표현 형식을 쓰시오.\n\n들여쓰기를 이용하여 데이터 구조를 표현하는 사람 친화적인 데이터 직렬화 형식이다. 주석을 지원하며(#), 설정 파일 작성에 자주 사용된다.`,ans:['YAML','yaml'],disp:'YAML',exp:'YAML: 들여쓰기, 주석(#) 가능, 사람 친화적\\nJSON: 주석 불가 / XML: 태그(<>) 사용'},
    {type:'단답형',s:'인수 테스트',q:`다음이 설명하는 인수 테스트 종류를 쓰시오.\n\n개발자의 통제 하에서 개발자 환경에서 실시되는 테스트로, 테스터가 사용자를 대표하여 실시한다. 반대로 베타 테스트는 개발자 없이 사용자가 직접 수행한다.`,ans:['알파 테스트','알파테스트','Alpha Test','알파'],disp:'알파(Alpha) 테스트',exp:'알파: 개발자 환경, 통제된 상태\\n베타: 개발자 없이, 사용자 직접'},
    ],
    des:[
    {type:'단답형',s:'생성 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n클래스의 인스턴스가 오직 하나임을 보장하고, 이 인스턴스에 대한 전역적인 접근을 제공하는 패턴이다. 예를 들어 프린터 스풀러, 로그 기록기 등에 사용된다.`,ans:['싱글톤','Singleton','singleton'],disp:'싱글톤 (Singleton)',exp:'생성 패턴 | 인스턴스 하나만 생성, 전역 접근'},
    {type:'단답형',s:'생성 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n객체 생성을 위한 인터페이스는 상위 클래스에서 정의하고, 실제로 어떤 클래스의 인스턴스를 만들지는 하위 클래스에서 결정하도록 하는 패턴이다.`,ans:['팩토리 메서드','Factory Method','factory method','팩토리메서드'],disp:'팩토리 메서드 (Factory Method)',exp:'생성 패턴 | 상위=인터페이스 정의, 서브클래스=실제 생성'},
    {type:'단답형',s:'구조 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n클라이언트가 요청한 인터페이스와 실제 제공되는 인터페이스가 달라 함께 동작할 수 없을 때, 이를 변환하여 연결해주는 패턴이다. 전원 콘센트 변환기에 비유된다.`,ans:['어댑터','Adapter','adapter'],disp:'어댑터 (Adapter)',exp:'구조 패턴 | 서로 다른 인터페이스 연결 (변환기 역할)'},
    {type:'단답형',s:'구조 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n실제 객체에 대한 접근을 제어하기 위해 대리 객체(Surrogate)를 제공하는 패턴이다. 보안, 원격 접근, 지연 초기화, 캐싱 등에 활용된다.`,ans:['프록시','Proxy','proxy'],disp:'프록시 (Proxy)',exp:'구조 패턴 | 대리 객체가 실제 객체 대신 처리'},
    {type:'단답형',s:'행위 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n한 객체의 상태가 바뀌면 그 객체에 의존하는 다른 객체들에게 연락이 가고 자동으로 내용이 갱신되는 방식의 일대다(1:N) 의존성을 정의한 패턴이다.\n(발행-구독 모델, Publish-Subscribe)`,ans:['옵저버','Observer','observer'],disp:'옵저버 (Observer)',exp:'행위 패턴 | 상태 변화 자동 알림, 발행-수신 모델'},
    {type:'단답형',s:'행위 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n내부 컬렉션의 구현 방법을 외부로 노출시키지 않으면서도 모든 항목에 순서대로 접근할 수 있는 방법을 제공하는 패턴이다. "Cursor"라고도 불린다.`,ans:['이터레이터','Iterator','iterator'],disp:'이터레이터 (Iterator)',exp:'행위 패턴 | 컬렉션 순차 탐색, Cursor'},
    {type:'단답형',s:'구조 패턴',q:`다음이 설명하는 디자인 패턴의 이름을 쓰시오.\n\n복잡한 서브 시스템들에 대한 단순화된 인터페이스를 제공하는 패턴이다. 클라이언트와 서브 시스템 사이의 의존관계를 줄여 결합도를 낮추는 효과가 있다.`,ans:['퍼사드','파사드','Facade','facade'],disp:'퍼사드 (Facade)',exp:'구조 패턴 | 단순한 인터페이스 제공, 결합도 낮춤'},
    {type:'단답형',s:'응집도',q:`다음이 설명하는 응집도의 종류를 쓰시오.\n\n모듈 내의 모든 기능 요소들이 단 하나의 목적을 위해 수행되는 응집도이다. 가장 강한 응집도로, 모듈이 단 하나의 기능만을 수행하도록 설계되어 이상적인 형태로 평가된다.`,ans:['기능적응집도','기능적 응집도','기능 응집도','Functional Cohesion'],disp:'기능적 응집도',exp:'응집도 강→약: 기능적 > 순차적 > 통신적 > 절차적 > 시간적 > 논리적 > 우연적'},
    {type:'단답형',s:'SOLID',q:`다음이 설명하는 객체지향 설계 원칙(SOLID)을 약어로 쓰시오.\n\n소프트웨어 구성요소(클래스, 모듈, 함수 등)는 확장에는 열려 있어야 하고, 수정에 대해서는 닫혀 있어야 한다는 원칙이다.`,ans:['OCP','ocp','개방폐쇄원칙','개방-폐쇄 원칙'],disp:'OCP (개방-폐쇄 원칙)',exp:'SOLID: SRP(단일책임) OCP(개방폐쇄) LSP(리스코프) ISP(인터페이스분리) DIP(의존성역전)'},
    {type:'단답형',s:'UML',q:`UML 클래스 다이어그램에서 다음이 설명하는 관계를 쓰시오.\n\n전체-부분 관계에서 부분 객체가 전체 객체에 강하게 속하여 생명주기를 함께하는 관계이다. 채워진 마름모(◆)로 표현한다.`,ans:['복합','Composition','composition','복합관계','복합(Composition)'],disp:'복합 관계 (Composition)',exp:'◆ 복합: 강한 소유, 생명주기 공유 / ◇ 집합: 약한 소유, 독립 존재 가능'},
    {type:'단답형',s:'럼바우',q:`럼바우 방법론에서 기능 모델링(Functional Modeling)의 산출물을 쓰시오.`,ans:['자료흐름도','자료 흐름도','DFD','dfd','Data Flow Diagram'],disp:'자료 흐름도 (DFD)',exp:'럼바우: 객체→ER다이어그램 / 동적→상태다이어그램 / 기능→DFD'},
    ],
    sec:[
    {type:'단답형',s:'DoS 공격',q:`다음이 설명하는 공격 기법을 쓰시오.\n\n공격자가 패킷의 출발지 IP 주소를 피해자의 IP 주소와 동일하게 위조하여 전송하는 공격이다. 피해 시스템이 자기 자신에게 계속 응답을 전송하게 되어 과부하가 발생한다.`,ans:['랜드어택','랜드 어택','LAND Attack','LAND','land attack'],disp:'랜드 어택 (LAND Attack)',exp:'출발지IP = 목적지IP 동일 설정'},
    {type:'단답형',s:'DoS 공격',q:`다음이 설명하는 공격 기법을 쓰시오.\n\n출발지 IP를 피해자 IP로 위조한 ICMP Echo Request 패킷을 브로드캐스트 주소로 전송한다. 네트워크상의 모든 호스트가 피해자에게 응답을 보내 트래픽이 폭증한다.`,ans:['스머프','스머프공격','Smurf','smurf','Smurf Attack'],disp:'스머프 (Smurf) 공격',exp:'ICMP Echo + 브로드캐스팅 → 증폭 효과'},
    {type:'단답형',s:'DoS 공격',q:`다음이 설명하는 공격 기법을 쓰시오.\n\nTCP 3-way handshake 과정에서 SYN 패킷만 대량으로 전송하고 ACK를 보내지 않아, 서버의 연결 대기 큐(백로그)를 가득 채워 정상 서비스를 불가능하게 하는 공격이다.`,ans:['SYN 플러딩','SYN플러딩','SYN Flooding','SYN flooding','SYN flood'],disp:'SYN 플러딩 (SYN Flooding)',exp:'TCP 3-way handshake 악용 / 3-way handshake: SYN→SYN+ACK→ACK'},
    {type:'단답형',s:'분산 공격',q:`다음이 설명하는 공격 기법을 쓰시오.\n\nIP 주소를 피해자의 IP로 위조한 요청 패킷을 정상적인 제3의 서버(반사체)에 보내고, 반사 서버가 피해자에게 대용량 응답을 보내게 만드는 DoS 공격이다. IP 스푸핑과 서버의 응답 증폭 효과를 이용한다.`,ans:['DRDoS','drDos','DR DoS','Distributed Reflection DoS'],disp:'DRDoS',exp:'IP스푸핑 + 정상서버(반사체) + 증폭 효과\\nDoS: 단일 / DDoS: 다수 분산 / DRDoS: 반사'},
    {type:'단답형',s:'악성코드',q:`다음이 설명하는 악성코드를 쓰시오.\n\n독립적인 프로그램으로, 숙주 프로그램 없이 스스로 복제하며 네트워크를 통해 다른 시스템으로 자율적으로 전파된다. 이메일이나 네트워크 공유를 통해 주로 확산된다.`,ans:['웜','Worm','worm'],disp:'웜 (Worm)',exp:'웜: 자가복제+자율전파, 숙주불필요\\n바이러스: 실행파일기생, 자율전파없음'},
    {type:'단답형',s:'암호화 알고리즘',q:`다음이 설명하는 암호화 알고리즘을 쓰시오.\n\n미국 국가표준기술연구소(NIST)가 DES의 취약점을 보완하기 위해 선정한 현재의 대칭키 블록 암호화 표준이다. 블록 크기는 128비트이며, 키 길이는 128/192/256비트를 지원한다.`,ans:['AES','aes','Advanced Encryption Standard'],disp:'AES (Advanced Encryption Standard)',exp:'AES: DES 대체, 블록 128비트, 현재 대칭키 표준\\nDES: IBM, 64비트 (취약)'},
    {type:'단답형',s:'암호화 알고리즘',q:`다음이 설명하는 암호화 알고리즘을 쓰시오.\n\n한국인터넷진흥원(KISA)에서 개발한 대칭키 블록 암호화 알고리즘으로, 한국의 최초 국내 표준 암호 알고리즘이다.`,ans:['SEED','seed'],disp:'SEED',exp:'SEED: KISA 개발, 한국 최초 블록 암호 표준'},
    {type:'단답형',s:'암호화 알고리즘',q:`다음이 설명하는 암호화 알고리즘을 쓰시오.\n\n큰 합성수의 소인수분해가 매우 어렵다는 수학적 원리를 기반으로 하는 공개키 암호화 알고리즘이다. 공개키와 개인키 한 쌍을 사용한다.`,ans:['RSA','rsa'],disp:'RSA',exp:'RSA: 소인수분해 기반, 비대칭키\\n디피-헬만: 이산로그 / ECC: 타원곡선'},
    {type:'단답형',s:'접근 통제',q:`다음이 설명하는 접근 통제 방식을 약어로 쓰시오.\n\n사용자의 역할(Role)에 기반하여 접근 권한을 부여하는 방식이다. 중앙 관리자가 역할을 정의하고, 사용자에게 역할을 할당하여 권한을 관리한다.`,ans:['RBAC','rbac','역할기반접근통제','역할 기반 접근 통제','Role Based Access Control'],disp:'RBAC (역할기반 접근통제)',exp:'DAC: 신분기반, 소유자 직접\\nMAC: 규칙/등급, 강제 통제\\nRBAC: 역할 기반, 중앙 관리자'},
    {type:'단답형',s:'인증',q:`다음이 설명하는 인증 기술을 쓰시오.\n\n사용자가 한 번만 로그인하면 별도의 인증 과정 없이 여러 시스템이나 서비스를 이용할 수 있는 기술이다. 커버로스(Kerberos) 프로토콜을 주로 사용한다.`,ans:['SSO','sso','Single Sign-On','Single Sign On'],disp:'SSO (Single Sign-On)',exp:'SSO: 커버로스 사용, 1회 인증으로 여러 자원 접근'},
    ],
    };
    let curCat='db', curMode='review';
    let fcList=[],fcIdx=0,fcKnow=0,fcUnknow=0,fcFlipped=false,fcUnknowList=[];
    let qList=[],qIdx=0,qSc=0,qSw=0,qWrongList=[],qAnswered=false;
    const wrongMap={};
    window.onload=()=>{loadStreak();setCat('db')};
    function loadStreak(){
      try{
        const d=localStorage.getItem('streak_date'),n=localStorage.getItem('streak_days')||'0';
        const today=new Date().toDateString();
        if(d!==today){
          const yesterday=new Date(Date.now()-86400000).toDateString();
          const days=d===yesterday?parseInt(n)+1:1;
          localStorage.setItem('streak_date',today);localStorage.setItem('streak_days',days);
          document.getElementById('hd-streak').textContent=`🔥 ${days}일`;
        }else document.getElementById('hd-streak').textContent=`🔥 ${n}일`;
      }catch(e){}
    }
    function setCat(cat){
      curCat=cat;const c=CATS[cat];
      document.documentElement.style.setProperty('--ac',c.color);
      document.documentElement.style.setProperty('--ac-l',c.light);
      document.querySelectorAll('.nbtn').forEach(b=>b.classList.toggle('on',b.dataset.cat===cat));
      document.getElementById('hd-badge').textContent=c.name;
      updateDots();
      if(curMode==='review')renderReview();
      else if(curMode==='flash')startFlash();
      else if(curMode==='quiz')startQuiz();
      else renderWrong();
    }
    function setMode(m){
      curMode=m;
      document.querySelectorAll('.mtab').forEach((b,i)=>b.classList.toggle('on',['review','flash','quiz','wrong'][i]===m));
      document.getElementById('view-review').classList.toggle('on',m==='review');
      document.getElementById('view-flash').classList.toggle('on',m==='flash');
      document.getElementById('view-quiz').classList.toggle('on',m==='quiz');
      document.getElementById('view-wrong').classList.toggle('on',m==='wrong');
      if(m==='review')renderReview();
      else if(m==='flash')startFlash();
      else if(m==='quiz')startQuiz();
      else renderWrong();
    }
    function updateDots(){
      ['db','net','sw','des','sec'].forEach(cat=>{
        const el=document.getElementById('dot-'+cat);
        if(el)el.classList.toggle('show',!!(wrongMap[cat]&&wrongMap[cat].length>0));
      });
    }
    function renderReview(){
      const wrap=document.getElementById('view-review');
      wrap.innerHTML=(RV[curCat]||[]).map((s,i)=>`
        <div class="rcard" id="rc${i}">
          <div class="rcard-hd" onclick="tog('rc${i}')">
            <div class="rcard-num">${s.num}</div>
            <div class="rcard-name">${s.name}</div>
            <span class="prob">${s.p}</span>
            <span class="arr">▾</span>
          </div>
          <div class="rcard-body">${s.b}</div>
        </div>`).join('');
      tog('rc0');
    }
    function tog(id){document.getElementById(id).classList.toggle('open')}
    function startFlash(useUnknown){
      const all=FC[curCat]||[];
      fcList=shuffle(useUnknown?(fcUnknowList.length?[...fcUnknowList]:[...all]):[...all]);
      fcIdx=0;fcKnow=0;fcUnknow=0;fcFlipped=false;fcUnknowList=[];
      document.getElementById('fc-result').classList.remove('show');
      document.getElementById('fc-area').style.display='';
      document.getElementById('fc-hint-txt').style.display='';
      document.getElementById('fc-actions').classList.remove('show');
      showFC();
    }
    function startFlashUnknown(){startFlash(true)}
    function showFC(){
      if(fcIdx>=fcList.length){showFCResult();return}
      const c=fcList[fcIdx];
      fcFlipped=false;
      document.getElementById('fc-inner').classList.remove('flip');
      document.getElementById('fc-tag-f').textContent=c.hint||curCat.toUpperCase();
      document.getElementById('fc-word').textContent=c.front;
      document.getElementById('fc-hint-sub').textContent='';
      document.getElementById('fc-ans').textContent=c.back;
      document.getElementById('fc-exp').textContent='';
      document.getElementById('fc-hint-txt').style.display='';
      document.getElementById('fc-actions').classList.remove('show');
      const total=fcList.length;
      document.getElementById('fc-prog').textContent=`${fcIdx+1} / ${total}`;
      document.getElementById('fc-pbar').style.width=(fcIdx/total*100)+'%';
      document.getElementById('fc-k').textContent=`✅ ${fcKnow}`;
      document.getElementById('fc-u').textContent=`❌ ${fcUnknow}`;
    }
    function flipCard(){
      if(fcIdx>=fcList.length)return;
      if(!fcFlipped){
        fcFlipped=true;
        document.getElementById('fc-inner').classList.add('flip');
        document.getElementById('fc-hint-txt').style.display='none';
        document.getElementById('fc-actions').classList.add('show');
      }
    }
    function fcMark(know){
      if(!fcFlipped)return;
      if(know)fcKnow++;else{fcUnknow++;fcUnknowList.push(fcList[fcIdx]);}
      fcIdx++;showFC();
    }
    function showFCResult(){
      document.getElementById('fc-area').style.display='none';
      document.getElementById('fc-hint-txt').style.display='none';
      document.getElementById('fc-actions').classList.remove('show');
      const total=fcList.length,pct=Math.round(fcKnow/total*100);
      const e=pct>=90?'🎉':pct>=70?'😊':pct>=50?'💪':'📚';
      const t=pct>=90?'완벽해요!':pct>=70?'잘하고 있어요!':pct>=50?'반은 외웠어요!':'더 반복이 필요해요!';
      document.getElementById('fc-r-e').textContent=e;
      document.getElementById('fc-r-t').textContent=t;
      document.getElementById('fc-r-s').textContent=`정답률 ${pct}%`;
      document.getElementById('fc-r-k').textContent=fcKnow;
      document.getElementById('fc-r-u').textContent=fcUnknow;
      document.getElementById('fc-r-tot').textContent=total;
      const btn=document.getElementById('fc-r-unkn-btn');
      btn.className='fc-btn2'+(fcUnknow>0?' show':'');
      btn.textContent=`❌ 모르는 것만 다시 (${fcUnknow}개)`;
      document.getElementById('fc-result').classList.add('show');
    }
    function startQuiz(){
      const qs=QZ[curCat]||[];
      qList=shuffle([...qs]);
      qIdx=0;qSc=0;qSw=0;qWrongList=[];qAnswered=false;
      document.getElementById('qresult').classList.remove('show');
      document.getElementById('qcard').style.display='';
      if(qList.length)showQ();
    }
    function showQ(){
      if(qIdx>=qList.length){showQResult();return}
      const q=qList[qIdx];
      qAnswered=false;
      document.getElementById('qcat-l').textContent=q.s;
      document.getElementById('qnum-l').textContent=`${qIdx+1} / ${qList.length}`;
      const tb=document.getElementById('qt-badge');
      tb.className='qtype qtype-sa';
      tb.textContent='✏️ 단답형';
      document.getElementById('qtxt').textContent=q.q;
      const inp=document.getElementById('ans-input');
      inp.value='';inp.className='ans-input';inp.disabled=false;
      inp.onkeydown=e=>{if(e.key==='Enter'&&!qAnswered)submitAns()};
      document.getElementById('submit-btn').disabled=false;
      document.getElementById('res-box').className='res-box';
      document.getElementById('res-box').innerHTML='';
      document.getElementById('next-btn').className='next-btn';
      const card=document.getElementById('qcard');
      card.style.animation='none';card.offsetHeight;card.style.animation='';
      setTimeout(()=>inp.focus(),300);
      updateQProg();
    }
    function submitAns(){
      if(qAnswered)return;
      const q=qList[qIdx];
      const input=document.getElementById('ans-input').value;
      if(!input.trim())return;
      qAnswered=true;
      document.getElementById('submit-btn').disabled=true;
      document.getElementById('ans-input').disabled=true;
      const correct=checkAns(input,q.ans);
      const inp=document.getElementById('ans-input');
      inp.className='ans-input '+(correct?'ok':'ng');
      const box=document.getElementById('res-box');
      if(correct){
        qSc++;
        box.className='res-box show ok';
        box.innerHTML=`<div class="res-head">🎉 정답!</div><div class="res-exp">${q.exp}</div>`;
      }else{
        qSw++;
        qWrongList.push({...q,userAns:input});
        box.className='res-box show ng';
        box.innerHTML=`<div class="res-head">❌ 오답</div><div class="res-correct">✅ 정답: ${q.disp}</div><div class="res-exp">${q.exp}</div>`;
      }
      document.getElementById('next-btn').className='next-btn show';
      updateQProg();
    }
    function nextQ(){qIdx++;showQ()}
    function updateQProg(){
      const total=qList.length;
      document.getElementById('qpl').textContent=`${qIdx} / ${total}`;
      document.getElementById('qpbar-f').style.width=(qIdx/total*100)+'%';
      document.getElementById('qpr-c').textContent=`✓ ${qSc}`;
      document.getElementById('qpr-w').textContent=`✗ ${qSw}`;
    }
    function showQResult(){
      document.getElementById('qcard').style.display='none';
      const total=qList.length,pct=Math.round(qSc/total*100);
      document.getElementById('qr-e').textContent=pct>=90?'🎉':pct>=70?'👍':pct>=50?'💪':'📚';
      document.getElementById('qr-t').textContent=pct>=90?'완벽해요!':pct>=70?'잘했어요!':pct>=50?'절반 정도!':'다시 복습하세요!';
      document.getElementById('qr-s').textContent=pct>=90?'이 파트 자신 있습니다!':pct>=70?'틀린 것만 복습하면 완벽!':'복습 탭으로 개념 다시 확인하세요.';
      document.getElementById('qr-pct').textContent=pct+'%';
      document.getElementById('qr-c').textContent=qSc;
      document.getElementById('qr-w').textContent=qSw;
      document.getElementById('qr-t2').textContent=total;
      const btn2=document.getElementById('qr-btn2');
      if(qWrongList.length>0){
        wrongMap[curCat]=[...qWrongList];
        btn2.className='qr-btn2 show';
        btn2.textContent=`❌ 오답 보기 (${qWrongList.length}개)`;
        updateDots();
      }else btn2.className='qr-btn2';
      document.getElementById('qresult').classList.add('show');
      updateQProg();
    }
    function checkAns(input,answers){
      const norm=s=>s.trim().toLowerCase().replace(/[\s\-\_\(\)]/g,'');
      const ni=norm(input);
      return answers.some(a=>{
        const na=norm(a);
        return ni===na||ni.includes(na)||na.includes(ni);
      });
    }
    function viewWrong(){setMode('wrong')}
    function renderWrong(){
      const wrongs=wrongMap[curCat]||[];
      const hd=document.getElementById('wrong-hd');
      const body=document.getElementById('wrong-body');
      if(wrongs.length===0){
        hd.textContent='오답 노트';
        body.innerHTML='<div class="empty-state">아직 오답이 없어요 🎉<br>기출형 퀴즈를 먼저 풀어보세요!</div>';
        return;
      }
      hd.textContent=`${CATS[curCat].name} 오답 ${wrongs.length}개`;
      body.innerHTML=`<button class="back-btn" onclick="setMode('quiz')">↩ 기출형 다시 풀기</button>`+
        wrongs.map((q,i)=>`<div class="wcard">
          <div class="wcard-q">${i+1}. ${q.q}</div>
          ${q.userAns?`<div class="wcard-your">내 답: "${q.userAns}"</div>`:''}
          <div class="wcard-ans-l">✅ 정답</div>
          <div class="wcard-ans">${q.disp}</div>
          <div class="wcard-exp">${q.exp}</div>
        </div>`).join('');
    }
    function shuffle(a){
      for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
      return a;
    }
    </script>
    </body>
    </html>
    """
    
    # Streamlit 화면에 HTML/JS 앱 전체를 내장 (높이 800px 지정)
    components.html(cbt_html, height=800, scrolling=True)

# ════════════════════════════════════════════════
# 🎰 럭키 슬롯
# ════════════════════════════════════════════════
elif menu == "🎰 럭키 슬롯":
    st.title("🎰 럭키 슬롯")

    SLOT_TIERS = [
        {"label": "🪙 일반 슬롯",   "cost": 1_000_000,   "jackpot": 30_000_000,   "jackpot_mult": 30, "prob": 0.10},
        {"label": "💰 골드 슬롯",   "cost": 10_000_000,  "jackpot": 500_000_000,  "jackpot_mult": 50, "prob": 0.08},
        {"label": "💎 다이아 슬롯", "cost": 100_000_000, "jackpot": 5_000_000_000,"jackpot_mult": 50, "prob": 0.06},
    ]
    SYMBOLS = {
        "🍒": 0.35, "🍋": 0.25, "🔔": 0.18, "⭐": 0.12, "7️⃣": 0.07, "💎": 0.03
    }

    sel_tier = st.selectbox("슬롯 등급 선택", range(len(SLOT_TIERS)), format_func=lambda i: SLOT_TIERS[i]['label'])
    tier = SLOT_TIERS[sel_tier]

    st.markdown(f"""
    <div class='card' style='text-align:center;'>
        <div style='color:#888;font-size:0.82rem;'>비용: <b style='color:#FFD600;'>₩{tier['cost']:,}</b> &nbsp;|&nbsp; 잭팟: <b style='color:#FF00FF;'>₩{tier['jackpot']:,}</b></div>
        <div style='color:#666;font-size:0.78rem;margin-top:4px;'>💎=3개 잭팟, 같은 기호 3개=고배당, 2개=소배당</div>
    </div>
    """, unsafe_allow_html=True)

    slot_display = st.empty()
    slot_display.markdown("<div class='slot-display'>🎰 &nbsp; 🎰 &nbsp; 🎰</div>", unsafe_allow_html=True)

    if st.button(f"🎰 {tier['label']} 당기기! (₩{tier['cost']:,})", use_container_width=True):
        if st.session_state.global_cash < tier['cost']:
            st.error("잔액 부족!")
        else:
            st.session_state.global_cash -= tier['cost']
            syms = list(SYMBOLS.keys())
            wts  = list(SYMBOLS.values())

            # 릴 스핀 애니메이션
            for _ in range(14):
                r = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                slot_display.markdown(f"<div class='slot-display'>{r[0]} &nbsp; {r[1]} &nbsp; {r[2]}</div>", unsafe_allow_html=True)
                time.sleep(0.08)

            final = [random.choices(syms, weights=wts)[0] for _ in range(3)]
            slot_display.markdown(f"<div class='slot-display'>{final[0]} &nbsp; {final[1]} &nbsp; {final[2]}</div>", unsafe_allow_html=True)

            if final[0] == final[1] == final[2] == "💎":
                prize = tier['jackpot']
                st.session_state.global_cash += prize
                st.success(f"💎💎💎 JACKPOT!!! +₩{prize:,}")
                st.balloons()
                market['news'] = f"🎊 [슬롯 잭팟] {st.session_state.logged_in_user}님이 {tier['label']}에서 ₩{prize:,} 잭팟 달성!!!"
                save_market(market)
            elif final[0] == final[1] == final[2]:
                prize = int(tier['cost'] * tier['jackpot_mult'] * 0.2)
                st.session_state.global_cash += prize
                st.success(f"🎉 트리플! +₩{prize:,}")
            elif final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
                prize = int(tier['cost'] * 1.5)
                st.session_state.global_cash += prize
                st.warning(f"✨ 더블 매치! +₩{prize:,}")
            else:
                st.error("꽝! 다음 기회를 노려보세요!")

            sync_user_data(); time.sleep(2); st.rerun()

# ════════════════════════════════════════════════
# 👑 칭호 상점
# ════════════════════════════════════════════════
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    st.markdown("칭호를 구매하고 장착하여 게시판에서 부를 과시하세요!")
    
    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i%2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id = f"title_{i}"
            price = i * 10000000
            
            st.markdown(f"**{title_name}** | ₩{price:,}")
            
            if title_id in st.session_state.inventory:
                if st.session_state.equipped_title == title_name:
                    st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"):
                        st.session_state.equipped_title = title_name
                        sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        st.session_state.global_cash -= price
                        st.session_state.inventory.append(title_id)
                        st.session_state.equipped_title = title_name # 사면 바로 장착
                        sync_user_data(); st.rerun()
                    else:
                        st.error("잔액이 부족합니다.")


# ════════════════════════════════════════════════
# 🏅 랭킹 & 게시판
# ════════════════════════════════════════════════
elif menu == "🏅 랭킹 & 게시판":
    st.title("🏅 랭킹 & 게시판")

    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 게시판"])

    with tab_rank:
        users_all = load_db(USERS_FILE, {})
        rank_data = []
        for uid, udata in users_all.items():
            if uid == "5891": continue
            w = udata.get('cash', 0) - udata.get('loan', 0)
            for sid, p in udata.get('portfolio', {}).items():
                if sid in market['stock_data']:
                    w += p.get('qty', 0) * market['stock_data'][sid]['price']
            for eid, cnt in udata.get('real_estate', {}).items():
                if eid in estate_config:
                    w += estate_config[eid]['price'] * cnt * 0.8
            rank_data.append({"uid": uid, "title": udata.get('equipped_title','🌱 신규시민'), "nw": w, "cash": udata.get('cash',0)})
        rank_data.sort(key=lambda x: x['nw'], reverse=True)

        medals = ["🥇", "🥈", "🥉"] + [f"{i}위" for i in range(4, 101)]
        for i, r in enumerate(rank_data[:20]):
            me = "🫵" if r['uid'] == st.session_state.logged_in_user else ""
            nw_color = "#FFD600" if i == 0 else "#C0C0C0" if i == 1 else "#CD7F32" if i == 2 else "#00E5FF"
            st.markdown(f"""
            <div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 18px;margin:4px 0;'>
                <span style='font-size:1.1rem;min-width:36px;'>{medals[i]}</span>
                <span style='font-weight:900;color:#E8E8F0;flex:1;margin:0 10px;'>{r['uid']} {me}</span>
                <span style='color:#888;font-size:0.82rem;flex:1;'>{r['title']}</span>
                <span style='font-weight:900;color:{nw_color};'>₩{r['nw']:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab_board:
        msg = st.text_input("메시지 작성", placeholder="랭커 게시판에 글을 남겨보세요!")
        if st.button("📝 등록", use_container_width=True):
            if msg.strip():
                comments = load_db(COMMENTS_FILE, [])
                comments.append({
                    "name": st.session_state.logged_in_user,
                    "title": st.session_state.equipped_title,
                    "comment": msg.strip(),
                    "time": datetime.now().strftime("%m/%d %H:%M")
                })
                save_db(COMMENTS_FILE, comments)
                st.rerun()

        st.write("")
        all_c = load_db(COMMENTS_FILE, [])
        for c in reversed(all_c[-50:]):
            t_color = "#FFD600"
            st.markdown(f"""
            <div class='card' style='margin:6px 0;padding:12px 16px;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
                    <span><b style='color:#00E5FF;'>{c['name']}</b> <span style='color:{t_color};font-size:0.82rem;'>{c.get('title','')}</span></span>
                    <span style='color:#555;font-size:0.78rem;'>{c.get('time','')}</span>
                </div>
                <div style='color:#ddd;font-size:0.92rem;'>{c['comment']}</div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 🛠️ 창조주 통제소
# ════════════════════════════════════════════════
elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 창조주 통제소")
    st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;'>⚠️ 창조주 전용 패널입니다. 신중하게 사용하세요.</div>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["👤 유저 조작", "📈 시장 조작", "📢 공지 & 이벤트", "📊 전체 현황"])

    with t1:
        u_db = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "5891"]
        if uid_list:
            sel_u = st.selectbox("유저 선택", uid_list)
            u_data = u_db[sel_u]
            c1, c2 = st.columns(2)
            with c1:
                new_cash = st.number_input("현금 설정", value=int(u_data['cash']), step=1_000_000)
                new_loan = st.number_input("대출 설정", value=int(u_data.get('loan', 0)), step=1_000_000)
            with c2:
                new_title = st.text_input("칭호 설정", value=u_data.get('equipped_title',''))
                st.metric("현재 현금", f"₩{u_data['cash']:,}")
                st.metric("현재 대출", f"₩{u_data.get('loan',0):,}")

            if st.button("⚡ 조작 실행", use_container_width=True):
                u_db[sel_u]['cash'] = new_cash
                u_db[sel_u]['loan'] = new_loan
                u_db[sel_u]['equipped_title'] = new_title
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 데이터 수정 완료!")

            st.write("---")
            if st.button("🗑️ 유저 삭제 (주의!)", use_container_width=True, type="secondary"):
                del u_db[sel_u]
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 삭제 완료!")
                st.rerun()
        else:
            st.info("등록된 유저가 없습니다.")

    with t2:
        st.markdown("### 📈 종목별 가격 조작")
        for s in stock_config:
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"{s['icon']} {s['name']}")
            c2.write(f"현재: ₩{market['stock_data'][s['id']]['price']:,}")
            if c3.button("🚀 +50%", key=f"up_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = f"🚀 [시장조작] {s['name']} 급등!"
                save_market(market); st.rerun()
            if c4.button("📉 -30%", key=f"dn_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 0.7)
                market['news'] = f"💣 [시장조작] {s['name']} 폭락!"
                save_market(market); st.rerun()

        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 전종목 +50% 폭등", use_container_width=True):
                for s in stock_config:
                    market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = "🔥 [창조주의 축복] 전 종목 폭등!!!"
                save_market(market); st.rerun()
        with c2:
            if st.button("💣 전종목 -40% 폭락", use_container_width=True):
                for s in stock_config:
                    market['stock_data'][s['id']]['price'] = max(1000, int(market['stock_data'][s['id']]['price'] * 0.6))
                market['news'] = "💣 [창조주의 심판] 전 종목 폭락!!!"
                save_market(market); st.rerun()

        st.write("---")
        new_lotto = st.number_input("로또 잭팟 설정", value=market['lotto_pool'], step=1_000_000_000)
        if st.button("💰 로또 잭팟 변경"):
            market['lotto_pool'] = new_lotto; save_market(market); st.success("완료!")

    with t3:
        st.markdown("### 📢 공지사항")
        msg_text = st.text_area("공지 내용", value=market.get('admin_msg', ''), height=100)
        msg_color = st.color_picker("텍스트 색상", value=market.get('admin_color', '#FF4B4B'))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📣 공지 발령", use_container_width=True):
                market['admin_msg'] = msg_text; market['admin_color'] = msg_color; save_market(market); st.success("공지 발령 완료!")
        with c2:
            if st.button("🗑️ 공지 삭제", use_container_width=True):
                market['admin_msg'] = ""; save_market(market); st.success("공지 삭제 완료!")

        st.write("---")
        st.markdown("### 🎭 특별 이벤트")
        ev_name = st.text_input("이벤트 이름", placeholder="예: 황금의 시간 🌟")
        ev_target = st.selectbox("대상 종목", [f"{s['icon']} {s['name']}" for s in stock_config])
        ev_mult = st.slider("변동 배율 (1.0 = 정상)", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
        if st.button("🎭 이벤트 발동", use_container_width=True):
            ev_sid = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == ev_target)
            market['event_active'] = True
            market['event_name'] = ev_name
            market['event_target'] = ev_sid
            market['event_multiplier'] = ev_mult
            market['news'] = f"🎭 [이벤트] {ev_name} 시작! {ev_target} 변동성 {ev_mult}배 증가!"
            save_market(market); st.success("이벤트 발동!")

        if st.button("⏹️ 이벤트 종료"):
            market['event_active'] = False; save_market(market); st.success("이벤트 종료!")

    with t4:
        st.markdown("### 📊 전체 유저 현황")
        u_db = load_db(USERS_FILE, {})
        rows = []
        for uid, ud in u_db.items():
            if uid == "5891": continue
            rows.append({"ID": uid, "칭호": ud.get('equipped_title',''), "현금": f"₩{ud.get('cash',0):,}", "대출": f"₩{ud.get('loan',0):,}"})
        if rows:
            st.table(pd.DataFrame(rows))
        else:
            st.info("등록된 유저 없음")

        st.write("---")
        st.markdown("### 💬 게시판 관리")
        if st.button("🗑️ 게시판 전체 삭제"):
            save_db(COMMENTS_FILE, []); st.success("게시판 초기화 완료!")
