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

def hex_to_rgba(clr, alpha=0.3):
    try:
        if not clr or not isinstance(clr, str):
            return f"rgba(255,255,255,{alpha})"

        clr = clr.lstrip('#')

        if len(clr) == 3:
            clr = ''.join([c*2 for c in clr])

        if len(clr) != 6:
            return f"rgba(255,255,255,{alpha})"

        r = int(clr[0:2], 16)
        g = int(clr[2:4], 16)
        b = int(clr[4:6], 16)

        return f"rgba({r},{g},{b},{alpha})"
    except:
        return f"rgba(255,255,255,{alpha})"

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
# 💻 정처기 CBT
# ════════════════════════════════════════════════
elif menu == "💻 정처기 CBT":
    st.title("💻 정보처리기사 실전 CBT")
    st.caption("실제 정처기 수준의 문제입니다. 정답 시 50만원 지급!")

    QUESTION_POOL = [
        {"q": "제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행 함수 종속 제거", "다치 종속 제거", "조인 종속 제거"], "cat": "데이터베이스"},
        {"q": "OSI 7계층에서 세그먼트(Segment)를 데이터 단위로 사용하는 계층은?", "a": "전송 계층(Transport Layer)", "w": ["네트워크 계층", "세션 계층", "데이터링크 계층"], "cat": "네트워크"},
        {"q": "스크럼(Scrum)에서 반복 개발 주기를 의미하는 용어는?", "a": "스프린트(Sprint)", "w": ["이터레이션", "릴리즈", "에픽"], "cat": "소프트웨어공학"},
        {"q": "트랜잭션의 원자성(Atomicity)이란?", "a": "모두 실행되거나 모두 취소되어야 함", "w": ["동시 트랜잭션 간 독립성 보장", "완료 후 영구 반영", "실행 전후 무결성 유지"], "cat": "데이터베이스"},
        {"q": "객체 생성을 서브클래스에서 결정하도록 위임하는 패턴은?", "a": "팩토리 메서드(Factory Method)", "w": ["싱글톤", "어댑터", "옵저버"], "cat": "디자인패턴"},
        {"q": "IP 주소 192.168.1.0/24의 서브넷 마스크는?", "a": "255.255.255.0", "w": ["255.255.0.0", "255.0.0.0", "255.255.255.128"], "cat": "네트워크"},
        {"q": "SQL LEFT OUTER JOIN의 결과로 옳은 설명은?", "a": "왼쪽 테이블 전체 + 오른쪽 매칭값(없으면 NULL)", "w": ["양쪽 매칭 행만 출력", "오른쪽 테이블 전체 포함", "매칭 안 되는 행은 제외"], "cat": "데이터베이스"},
        {"q": "퀵 정렬(Quick Sort)의 평균 시간 복잡도는?", "a": "O(n log n)", "w": ["O(n²)", "O(n)", "O(log n)"], "cat": "알고리즘"},
        {"q": "TCP와 UDP의 핵심 차이점은?", "a": "TCP는 연결 지향, UDP는 비연결 지향", "w": ["TCP가 더 빠름", "UDP가 신뢰성 보장", "둘 다 응용 계층 프로토콜"], "cat": "네트워크"},
        {"q": "REST API에서 리소스 삭제 시 사용하는 HTTP 메서드는?", "a": "DELETE", "w": ["GET", "POST", "PUT"], "cat": "웹"},
        {"q": "NoSQL의 특징으로 올바른 것은?", "a": "유연한 스키마 + 수평 확장(Scale-out) 용이", "w": ["ACID 반드시 보장", "관계형 모델 전용", "수직 확장만 가능"], "cat": "데이터베이스"},
        {"q": "페이징(Paging) 기법의 주요 장점은?", "a": "외부 단편화 제거", "w": ["내부 단편화 제거", "메모리 접근 속도 향상", "TLB 불필요"], "cat": "운영체제"},
        {"q": "Git에서 원격 저장소 변경사항을 로컬에 병합하는 명령어는?", "a": "git pull", "w": ["git push", "git fetch", "git clone"], "cat": "개발도구"},
        {"q": "해시 테이블의 평균 검색 시간 복잡도는?", "a": "O(1)", "w": ["O(n)", "O(log n)", "O(n log n)"], "cat": "자료구조"},
        {"q": "프로세스와 스레드의 차이점으로 올바른 것은?", "a": "스레드는 같은 프로세스 내 메모리를 공유", "w": ["프로세스가 더 가벼움", "스레드는 독립적인 메모리 공간 가짐", "스레드 생성 비용이 더 큼"], "cat": "운영체제"},
        {"q": "UML 다이어그램 중 시스템 동적 행위를 표현하지 않는 것은?", "a": "클래스 다이어그램", "w": ["시퀀스 다이어그램", "상태 다이어그램", "활동 다이어그램"], "cat": "소프트웨어공학"},
        {"q": "대칭키 암호화 방식의 특징은?", "a": "암호화·복호화에 동일한 키 사용, 처리 속도 빠름", "w": ["공개키·개인키 쌍 사용", "키 분배가 안전함", "전자서명에 주로 사용"], "cat": "보안"},
        {"q": "Python에서 GIL(Global Interpreter Lock)의 영향은?", "a": "멀티스레드 환경에서 CPU 병렬 실행이 제한됨", "w": ["메모리 누수 방지", "비동기 I/O 불가", "멀티프로세스 제한"], "cat": "프로그래밍"},
    ]

    if 'cbt_q' not in st.session_state:
        q = random.choice(QUESTION_POOL)
        opts = q['w'] + [q['a']]
        random.shuffle(opts)
        st.session_state.cbt_q    = q
        st.session_state.cbt_opts = opts
        st.session_state.cbt_answered = False

    q = st.session_state.cbt_q
    cats = {"데이터베이스": "🗄️", "네트워크": "🌐", "소프트웨어공학": "⚙️",
            "알고리즘": "🔢", "자료구조": "📚", "운영체제": "🖥️",
            "디자인패턴": "🎨", "웹": "🌍", "개발도구": "🛠️", "보안": "🔒", "프로그래밍": "💻"}
    cat_icon = cats.get(q.get('cat', ''), "📝")

    st.markdown(f"<div style='color:#888;font-size:0.8rem;margin-bottom:8px;'>{cat_icon} {q.get('cat','기타')} 분야</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'><b>Q.</b> {q['q']}</div>", unsafe_allow_html=True)
    st.write("")

    with st.form("cbt_form"):
        answer = st.radio("정답을 선택하세요:", st.session_state.cbt_opts, key="cbt_radio")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button("✅ 제출", use_container_width=True)
        if submitted:
            if answer == q['a']:
                st.success("🎉 정답입니다! 훌륭합니다!")
                st.session_state.global_cash += 500_000
                st.balloons()
                st.info("💰 보상: +₩500,000")
            else:
                st.error(f"❌ 오답! 정답: {q['a']}")
            del st.session_state.cbt_q, st.session_state.cbt_opts
            sync_user_data()
            time.sleep(2.5); st.rerun()

    if st.button("🔄 다른 문제", use_container_width=True):
        if 'cbt_q' in st.session_state: del st.session_state.cbt_q
        if 'cbt_opts' in st.session_state: del st.session_state.cbt_opts
        st.rerun()

# ════════════════════════════════════════════════
# 🏎️ 하이퍼카 레이싱
# ════════════════════════════════════════════════
elif menu == "🏎️ 하이퍼카 레이싱":
    st.title("🏎️ 하이퍼카 레이싱")
    st.caption("배당률이 높을수록 우승 확률은 낮지만 당첨 시 고수익!")

    CARS = [
        {"name": "부가티 시론 SS",    "emoji": "🏎️", "odds": 20.0, "spd": (2, 7),  "color": "#FF0066"},
        {"name": "람보르기니 레부엘토","emoji": "🐂", "odds": 12.0, "spd": (3, 10), "color": "#FF6600"},
        {"name": "페라리 SF90 XX",    "emoji": "🐎", "odds": 8.0,  "spd": (4, 12), "color": "#FF2200"},
        {"name": "맥라렌 P1 GTR",     "emoji": "🚀", "odds": 6.0,  "spd": (5, 13), "color": "#FF9900"},
        {"name": "포르쉐 918 스파이더","emoji": "⚡", "odds": 4.0,  "spd": (6, 15), "color": "#FFCC00"},
        {"name": "테슬라 로드스터 2",  "emoji": "⚡", "odds": 2.5,  "spd": (8, 17), "color": "#00FF88"},
        {"name": "토요타 GR010 하이브","emoji": "🏁", "odds": 1.8,  "spd": (10, 20),"color": "#00CCFF"},
    ]

    car_names = [f"{c['emoji']} {c['name']} ({c['odds']}배)" for c in CARS]
    sel_idx   = st.selectbox("차량 선택", range(len(CARS)), format_func=lambda i: car_names[i])
    my_car    = CARS[sel_idx]
    bet_amt   = st.number_input("베팅 금액 (원)", min_value=10_000, step=10_000, value=100_000)
    st.caption(f"우승 시 예상 수령액: ₩{int(bet_amt * my_car['odds']):,}")

    if st.button("🏁 레이스 시작!", use_container_width=True):
        if st.session_state.global_cash < bet_amt:
            st.error("잔액 부족!")
        else:
            st.session_state.global_cash -= bet_amt

            positions = {c['name']: 0.0 for c in CARS}
            winner    = None
            bars      = {}
            st.markdown("### 🏁 레이스 진행")
            for c in CARS:
                bars[c['name']] = st.progress(0, text=f"{c['emoji']} {c['name']}")

            lap = 0
            while winner is None:
                time.sleep(0.12)
                lap += 1
                for c in CARS:
                    move = random.randint(c['spd'][0], c['spd'][1])
                    positions[c['name']] = min(100, positions[c['name']] + move)
                    pct  = positions[c['name']] / 100
                    rank = sorted(positions.items(), key=lambda x: x[1], reverse=True)
                    pos_num = next(i+1 for i, (n, _) in enumerate(rank) if n == c['name'])
                    bars[c['name']].progress(pct, text=f"{c['emoji']} {c['name']}  {pos_num}위 | {positions[c['name']]:.0f}%")
                    if positions[c['name']] >= 100 and winner is None:
                        winner = c['name']

            st.write("---")
            winner_car = next(c for c in CARS if c['name'] == winner)
            st.markdown(f"<div style='text-align:center;font-family:Orbitron,monospace;font-size:1.8rem;color:{winner_car['color']};font-weight:900;padding:20px;'>🏆 {winner_car['emoji']} {winner} 우승!</div>", unsafe_allow_html=True)

            if winner == my_car['name']:
                prize = int(bet_amt * my_car['odds'])
                st.session_state.global_cash += prize
                st.success(f"🎉 베팅 성공! +₩{prize:,}")
                st.balloons()
            else:
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")

            sync_user_data(); time.sleep(3); st.rerun()

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
    st.title("👑 칭호 상점")

    if st.session_state.equipped_title == "💸 신용불량자":
        st.error("💸 신용불량 상태에서는 칭호 구매가 불가합니다. 대출을 먼저 상환하세요!")
    else:
        st.markdown(f"<div class='card' style='text-align:center;'>현재 장착 칭호: <b style='color:#FFD600;font-size:1.2rem;'>{st.session_state.equipped_title}</b></div>", unsafe_allow_html=True)
        st.write("")

        grade_colors = {1:"#888",2:"#4CAF50",3:"#2196F3",4:"#9C27B0",5:"#FF9800",6:"#FF5722",7:"#E91E63",8:"#00BCD4",9:"#FFEB3B",10:"#FF1744",99:"#FFD600"}

        for t in TITLE_SHOP:
            can_buy = st.session_state.global_cash >= t['price']
            is_equipped = st.session_state.equipped_title == t['name']
            clr = grade_colors.get(t['grade'], "#888")
            c1, c2 = st.columns([5, 2])
            with c1:
                badge = "✅ 장착중" if is_equipped else ""
                st.markdown(f"""
                <div class='card' style='padding:14px 18px;border-color:rgba({int(clr[1:3],16)},{int(clr[3:5],16)},{int(clr[5:7],16)},0.3);'>
                    <span style='font-size:1.05rem;font-weight:900;color:{clr};'>{t['name']}</span>
                    <span style='color:#FFD600;margin-left:12px;font-size:0.9rem;'>₩{t['price']:,}</span>
                    {f"<span style='color:#00FF88;margin-left:8px;font-size:0.82rem;'>{badge}</span>" if badge else ""}
                </div>
                """, unsafe_allow_html=True)
            with c2:
                btn_label = "✅ 장착중" if is_equipped else "🛒 구매/장착" if can_buy else "💸 부족"
                if not is_equipped:
                    if st.button(btn_label, key=f"title_{t['name']}", use_container_width=True, disabled=not can_buy):
                        st.session_state.global_cash -= t['price']
                        st.session_state.equipped_title = t['name']
                        sync_user_data()
                        st.success(f"✅ [{t['name']}] 장착 완료!")
                        time.sleep(1); st.rerun()

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
