import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import random
import json
import os
import time
import tempfile
import shutil
from datetime import datetime

# 그 바로 아랫줄에 한국 시간(KST) 세팅을 추가해 줍니다.
KST = timezone(timedelta(hours=9))

# ==============================
# 🌌 시스템 설정 및 데이터베이스
# ==============================
USERS_FILE    = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE   = "market_db.json"
TXLOG_FILE    = "txlog_db.json"
REALESTATE_MARKET_FILE = "realestate_market_db.json"  # 부동산 거래 마켓

stock_config = [
    {"id": "NDX",    "name": "나스닥100 ETF",       "vol": 0.04, "icon": "🇺🇸"},
    {"id": "HDEC",   "name": "현대건설",             "vol": 0.03, "icon": "🏗️"},
    {"id": "MANU",   "name": "맨체스터 유나이티드",  "vol": 0.04, "icon": "⚽"},
    {"id": "CJENM",  "name": "CJ ENM",               "vol": 0.04, "icon": "🎬"},
    {"id": "FOOD",   "name": "삼양식품",             "vol": 0.03, "icon": "🍜"},
    {"id": "BIO",    "name": "삼성바이오로직스",      "vol": 0.05, "icon": "🧬"},
    {"id": "AERO",   "name": "한화에어로스페이스",    "vol": 0.06, "icon": "🚀"},
    {"id": "RETAIL", "name": "신세계",               "vol": 0.02, "icon": "🛍️"},
    {"id": "CHEM",   "name": "LG화학",               "vol": 0.03, "icon": "⚗️"},
    {"id": "ENTER",  "name": "하이브",               "vol": 0.07, "icon": "🎵"},

]

# ── 부동산 기본 매물 설정 (수량 제한 있음) ──
# 초기 공급량이 정해져 있고, 유저가 판매 등록해야 다른 유저가 살 수 있음
estate_config = {
    "E1":  {"name": "역세권 원룸",          "icon": "🏠",  "base_price": 10_000_000_000,    "income": 8_000,     "desc": "지하철 2분 거리 황금 입지",          "total_supply": 20},
    "E2":  {"name": "초대형 PC방",           "icon": "🖥️",  "base_price": 50_000_000_000,    "income": 45_000,    "desc": "e스포츠 성지, 24시간 풀가동",        "total_supply": 10},
    "E3":  {"name": "강남 꼬마빌딩",         "icon": "🏢",  "base_price": 500_000_000_000,   "income": 450_000,   "desc": "강남 핵심 상권 4층 빌딩",            "total_supply": 5},
    "E4":  {"name": "시그니엘 펜트하우스",   "icon": "👑",  "base_price": 5_000_000_000_000, "income": 4_500_000, "desc": "롯데월드타워 최상층 전망",           "total_supply": 2},
    "E5":  {"name": "제주 풀빌라",           "icon": "🌴",  "base_price": 30_000_000_000,    "income": 25_000,    "desc": "성산일출봉 전망 프리미엄 풀빌라",    "total_supply": 8},
    "E6":  {"name": "홍대 상가건물",         "icon": "🎸",  "base_price": 200_000_000_000,   "income": 180_000,   "desc": "홍대 메인 스트리트 5층 상가",        "total_supply": 6},
    "E7":  {"name": "판교 오피스타워",       "icon": "💻",  "base_price": 800_000_000_000,   "income": 750_000,   "desc": "IT 기업 밀집 A급 오피스",            "total_supply": 3},
    "E8":  {"name": "해운대 호텔",           "icon": "🏖️",  "base_price": 2_000_000_000_000, "income": 2_000_000, "desc": "부산 해운대 특급 호텔 1동",          "total_supply": 2},
    "E9":  {"name": "용산 임대아파트 단지",  "icon": "🏘️",  "base_price": 1_000_000_000_000, "income": 900_000,   "desc": "용산 재개발 신축 100세대 단지",      "total_supply": 3},
    "E10": {"name": "인천공항 면세점",       "icon": "✈️",  "base_price": 3_000_000_000_000, "income": 3_500_000, "desc": "인천공항 1터미널 황금 면세점",       "total_supply": 1},
}

# ── 광산 아이템 설정 ──
MINE_ITEMS = [
    {"name": "돌멩이",     "icon": "🪨", "value": 10_000,     "prob": 0.40},
    {"name": "구리광석",   "icon": "🟤", "value": 50_000,     "prob": 0.25},
    {"name": "은광석",     "icon": "⚪", "value": 200_000,    "prob": 0.15},
    {"name": "금광석",     "icon": "🟡", "value": 500_000,    "prob": 0.10},
    {"name": "루비",       "icon": "🔴", "value": 1_000_000,  "prob": 0.05},
    {"name": "사파이어",   "icon": "🔵", "value": 3_000_000,  "prob": 0.03},
    {"name": "다이아몬드", "icon": "💎", "value": 10_000_000, "prob": 0.015},
    {"name": "전설의 원석","icon": "🌟", "value": 100_000_000,"prob": 0.005},
]

# ── 숫자를 한글 단위로 변환 ──
def format_korean_money(num):
    if num is None or (isinstance(num, float) and np.isnan(num)) or num == 0: return "0원"
    is_neg = num < 0
    num = abs(int(num))
    jo = num // 10**12
    eok = (num % 10**12) // 10**8
    man = (num % 10**8) // 10**4
    won = num % 10**4
    parts = []
    if jo > 0: parts.append(f"{jo:,}조")
    if eok > 0: parts.append(f"{eok:,}억")
    if man > 0: parts.append(f"{man:,}만")
    if won > 0 or not parts: parts.append(f"{won:,}")
    res = " ".join(parts) + "원"
    return f"-{res}" if is_neg else res

# ════════════════════════════════════
# 🗄️ DB 유틸
# ════════════════════════════════════
def _atomic_save(filepath: str, data):
    tmp = filepath + ".tmp"
    bak = filepath + ".bak"
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if os.path.exists(filepath):
            shutil.copy2(filepath, bak)
        shutil.move(tmp, filepath)
    except Exception as e:
        if os.path.exists(tmp): os.remove(tmp)
        raise e

def load_db(file, default):
    for target in [file, file + ".bak"]:
        if os.path.exists(target):
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data is not None: return data
            except Exception:
                continue
    return default

def save_db(file, data):
    if data is None: return
    if isinstance(data, dict) and len(data) == 0 and file == USERS_FILE: return
    _atomic_save(file, data)

# ── 거래 기록 ──
def log_tx(uid: str, category: str, desc: str, amount: int):
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs: logs[uid] = []
    logs[uid].insert(0, {
        "time": datetime.now().strftime("%m/%d %H:%M:%S"),
        "category": category,
        "desc": desc,
        "amount": amount,
    })
    logs[uid] = logs[uid][:200]
    save_db(TXLOG_FILE, logs)

# ── 부동산 마켓 로드/저장 ──
def load_estate_market():
    """
    구조: {
      "listings": [
        {
          "id": str (uuid),
          "eid": str,
          "seller": str,
          "price": int,
          "listed_time": float
        }, ...
      ],
      "owner_counts": { uid: { eid: count } }  # 전체 소유 현황
    }
    """
    default = {"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}}
    d = load_db(REALESTATE_MARKET_FILE, default)
    # 초기 재고 동기화
    if "initial_stock" not in d:
        d["initial_stock"] = {eid: info["total_supply"] for eid, info in estate_config.items()}
    if "owner_counts" not in d:
        d["owner_counts"] = {}
    if "listings" not in d:
        d["listings"] = []
    return d

def save_estate_market(data):
    save_db(REALESTATE_MARKET_FILE, data)

def get_estate_initial_listings(em):
    """초기 공급 매물 (아직 아무도 안 산 것들) - 기본가로 판매"""
    result = []
    for eid, info in estate_config.items():
        # 현재 유저가 보유한 총 수량 계산
        owned_total = sum(
            v.get(eid, 0) for v in em["owner_counts"].values()
        )
        # 유저 간 거래 중인 수량
        listed_count = sum(1 for l in em["listings"] if l["eid"] == eid)
        # 초기 재고에서 소진된 수량
        initial_released = owned_total + listed_count
        remaining_initial = max(0, info["total_supply"] - initial_released)
        if remaining_initial > 0:
            result.append({
                "eid": eid,
                "remaining": remaining_initial,
                "price": info["base_price"],
                "is_initial": True
            })
    return result

# ── 순자산 계산 ──
def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return 0
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices: w += p_data.get('qty', 0) * prices[sid]
    em = load_estate_market()
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
    return w

def sync_user_data():
    if 'logged_in_user' not in st.session_state: return
    users = load_db(USERS_FILE, {})
    uid = st.session_state.logged_in_user
    if uid not in users: return
    users[uid].update({
        'cash':           st.session_state.global_cash,
        'inventory':      st.session_state.inventory,
        'equipped_title': st.session_state.equipped_title,
        'portfolio':      st.session_state.portfolio,
        'real_estate':    st.session_state.real_estate,
        'rent_time':      st.session_state.rent_time,
        'loan':           st.session_state.loan,
        'loan_time':      st.session_state.loan_time,
        'stats':          st.session_state.get('stats', {}),
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
            "news": "🌌 HYOMIN UNIVERSE v18 오픈! 부동산 실거래 시스템 도입!",
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

# ════════════════════════════════════
# ⏱️ 광클 방지 유틸
# ════════════════════════════════════
def can_action(key: str, cooldown_sec: float = 2.0) -> bool:
    """True면 실행 가능, False면 쿨다운 중"""
    last = st.session_state.get(f"_cd_{key}", 0)
    return (time.time() - last) >= cooldown_sec

def set_cooldown(key: str):
    st.session_state[f"_cd_{key}"] = time.time()

def cooldown_remaining(key: str, cooldown_sec: float = 2.0) -> float:
    last = st.session_state.get(f"_cd_{key}", 0)
    return max(0.0, cooldown_sec - (time.time() - last))

# ════════════════════════════════════
# 페이지 설정
# ════════════════════════════════════
st.set_page_config(page_title="HYOMIN UNIVERSE v18", page_icon="🌌", layout="wide")

# ==============================
# 🔐 로그인
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');
.stApp { background: radial-gradient(ellipse at 20% 50%, #0d0221 0%, #050510 60%, #000 100%) !important; }
* { font-family:'Noto Sans KR',sans-serif !important; color:#FFF !important; }
.login-title {
  font-family:'Orbitron',monospace !important; font-size:clamp(2rem,6vw,4rem) !important;
  font-weight:900; text-align:center;
  background:linear-gradient(135deg,#00E5FF 0%,#FF00FF 50%,#FFD600 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  padding:20px 0; letter-spacing:4px; animation:glow 3s ease-in-out infinite alternate;
}
@keyframes glow { from{filter:drop-shadow(0 0 10px #00E5FF)} to{filter:drop-shadow(0 0 30px #FF00FF)} }
.login-sub { text-align:center; color:#888 !important; font-size:1rem; margin-bottom:30px; letter-spacing:3px; }
.stTextInput>div>div>input {
  background:rgba(0,229,255,0.05) !important; border:1px solid rgba(0,229,255,0.3) !important;
  border-radius:8px !important; color:#000 !important; font-size:1rem !important; padding:12px !important;
}
.stButton>button {
  background:linear-gradient(135deg,#00E5FF,#0066FF) !important; border:none !important;
  border-radius:8px !important; color:#000 !important; font-weight:900 !important;
  font-size:1rem !important; padding:14px !important; width:100%;
}
</style>""", unsafe_allow_html=True)

    st.markdown("<div class='login-title'>🌌 HYOMIN UNIVERSE</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-sub'>∙ 가상 자산 시뮬레이터 v18 ∙</div>", unsafe_allow_html=True)

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
                        'global_cash':    u['cash'],
                        'inventory':      u.get('inventory', []),
                        'equipped_title': u.get('equipped_title', '🌱 신규시민'),
                        'portfolio':      u.get('portfolio', {}),
                        'real_estate':    u.get('real_estate', {}),
                        'rent_time':      u.get('rent_time', time.time()),
                        'loan':           u.get('loan', 0),
                        'loan_time':      u.get('loan_time', time.time()),
                        'device_mode':    device_mode,
                        'stats':          u.get('stats', {'wins':0,'losses':0,'races_won':0,'lotto_spent':0}),
                    })
                    st.rerun()
                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {"pw":"5891","cash":999_999_999_999,"inventory":[],
                                         "equipped_title":"👑 절대신 창조주","portfolio":{},
                                         "real_estate":{},"rent_time":time.time(),
                                         "loan":0,"loan_time":time.time(),"stats":{}}
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
                    users[n_id] = {"pw":n_pw,"cash":100_000_000,"inventory":[],
                                   "equipped_title":"🌱 신규시민","portfolio":{},
                                   "real_estate":{},"rent_time":time.time(),
                                   "loan":0,"loan_time":time.time(),"stats":{}}
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 초기 자금 1억원이 지급되었습니다!")
    st.stop()

# ==============================
# 🎨 CSS
# ==============================
IS_PC = "🖥️" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');
.stApp {
  background:#060610 !important;
  background-image:
    radial-gradient(ellipse at 0% 0%,rgba(0,229,255,0.06) 0%,transparent 50%),
    radial-gradient(ellipse at 100% 100%,rgba(255,0,200,0.06) 0%,transparent 50%) !important;
}
html,body,p,span,label,div { font-family:'Noto Sans KR',sans-serif !important; color:#E8E8F0 !important; }
h1,h2,h3 { font-family:'Orbitron',monospace !important; letter-spacing:2px; }
[data-testid='stSidebar'] {
  background:linear-gradient(180deg,#080818 0%,#0a0a20 100%) !important;
  border-right:1px solid rgba(0,229,255,0.2) !important;
}
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
  background:#FFF !important; border:2px solid #00E5FF !important;
  border-radius:8px !important; color:#000 !important; font-weight:900 !important;
}
div[data-baseweb="select"]>div {
  background:rgba(255,255,255,0.04) !important;
  border:1px solid rgba(0,229,255,0.25) !important; border-radius:8px !important;
}
div[role="listbox"] { background:#111128 !important; border:1px solid #00E5FF !important; border-radius:10px !important; }
div[role="listbox"] li,div[role="listbox"] span { color:#fff !important; }
div[role="listbox"] li:hover { background:rgba(0,229,255,0.15) !important; }
.stButton>button {
  font-family:'Noto Sans KR',sans-serif !important; font-weight:900 !important;
  border-radius:10px !important; border:1px solid rgba(0,229,255,0.4) !important;
  background:rgba(0,229,255,0.07) !important; color:#00E5FF !important;
  transition:all 0.25s ease !important;
}
.stButton>button:hover {
  background:rgba(0,229,255,0.18) !important; border-color:#00E5FF !important;
  box-shadow:0 0 18px rgba(0,229,255,0.35) !important; transform:translateY(-1px) !important;
}
.stButton>button:disabled {
  opacity:0.4 !important; cursor:not-allowed !important; transform:none !important;
}
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid rgba(0,229,255,0.15) !important; }
.stTabs [data-baseweb="tab"] { color:#777 !important; font-weight:700 !important; font-size:0.95rem !important; padding:10px 20px !important; }
.stTabs [aria-selected="true"] { color:#00E5FF !important; border-bottom:2px solid #00E5FF !important; background:transparent !important; }
[data-testid="stMetric"] {
  background:rgba(255,255,255,0.03) !important; border:1px solid rgba(0,229,255,0.15) !important;
  border-radius:12px !important; padding:14px 18px !important;
}
[data-testid="stMetricLabel"] { color:#888 !important; font-size:0.8rem !important; }
[data-testid="stMetricValue"] { color:#FFD600 !important; font-family:'Orbitron',monospace !important; font-size:1.3rem !important; }
.stAlert { border-radius:10px !important; border:none !important; }
.stProgress>div>div { background:linear-gradient(90deg,#00E5FF,#FF00FF) !important; border-radius:4px !important; }
.stock-table { width:100%; border-collapse:collapse; }
.stock-table th {
  background:rgba(0,229,255,0.08); color:#00E5FF !important;
  font-family:'Orbitron',monospace !important; font-size:0.75rem !important;
  padding:10px 14px; text-align:left; border-bottom:1px solid rgba(0,229,255,0.2); letter-spacing:1px;
}
.stock-table td { padding:11px 14px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.95rem; vertical-align:middle; }
.stock-table tr:hover td { background:rgba(0,229,255,0.04); }
.p-up { color:#FF4B4B !important; font-weight:900; }
.p-down { color:#4B9EFF !important; font-weight:900; }
.p-flat { color:#888 !important; }
.card {
  background:rgba(255,255,255,0.03); border:1px solid rgba(0,229,255,0.15);
  border-radius:14px; padding:20px; margin:8px 0; transition:all 0.3s;
}
.card:hover { border-color:rgba(0,229,255,0.4); box-shadow:0 4px 20px rgba(0,229,255,0.1); }
.news-banner {
  background:linear-gradient(135deg,rgba(255,180,0,0.1),rgba(255,100,0,0.08));
  border:1px solid rgba(255,180,0,0.3); border-radius:10px; padding:12px 18px;
  font-weight:700; color:#FFD600 !important; margin:12px 0; font-size:0.95rem;
}
.scoreboard {
  background:linear-gradient(135deg,#0d1b2a,#1a1a3e);
  border:2px solid rgba(0,229,255,0.4); border-radius:16px; padding:28px; text-align:center;
  box-shadow:0 0 40px rgba(0,229,255,0.15),inset 0 0 40px rgba(0,0,50,0.5);
}
.score-number { font-family:'Orbitron',monospace !important; font-size:3.5rem !important; font-weight:900; color:#00FF88 !important; text-shadow:0 0 20px rgba(0,255,136,0.5); line-height:1; }
.team-label { font-size:1.2rem; font-weight:900; color:#FFD600 !important; margin-bottom:8px; }
.match-time { font-family:'Orbitron',monospace !important; color:#00E5FF !important; font-size:1rem; margin-top:14px; }
.commentary-item {
  background:rgba(255,255,255,0.04); border-left:3px solid #00E5FF;
  padding:10px 15px; margin:6px 0; border-radius:0 8px 8px 0; font-size:0.9rem; color:#ddd !important;
}
.estate-card {
  background:linear-gradient(135deg,rgba(255,215,0,0.05),rgba(255,100,0,0.05));
  border:1px solid rgba(255,215,0,0.2); border-radius:14px; padding:18px 22px; margin:10px 0;
}
.estate-income { color:#00FF88 !important; font-weight:900; font-size:0.9rem; }
.market-listing {
  background:linear-gradient(135deg,rgba(0,229,255,0.04),rgba(0,100,200,0.06));
  border:1px solid rgba(0,229,255,0.25); border-radius:12px; padding:16px 20px; margin:8px 0;
}
.market-initial {
  background:linear-gradient(135deg,rgba(0,255,136,0.04),rgba(0,150,80,0.06));
  border:1px solid rgba(0,255,136,0.25); border-radius:12px; padding:16px 20px; margin:8px 0;
}
.my-listing {
  background:linear-gradient(135deg,rgba(255,180,0,0.06),rgba(200,100,0,0.06));
  border:1px solid rgba(255,180,0,0.35); border-radius:12px; padding:16px 20px; margin:8px 0;
}
.profit { color:#FF4B4B !important; font-weight:900; }
.loss   { color:#4B9EFF !important; font-weight:900; }
.vip-banner {
  background:linear-gradient(135deg,#1a0a00,#2d1000);
  border:2px solid rgba(255,215,0,0.5); border-radius:16px; padding:22px; text-align:center;
  box-shadow:0 0 30px rgba(255,180,0,0.2);
}
.lotto-pool {
  background:linear-gradient(135deg,#1a003a,#2d0060);
  border:2px solid rgba(180,0,255,0.5); border-radius:16px; padding:24px; text-align:center;
  box-shadow:0 0 40px rgba(180,0,255,0.2);
}
.lotto-amount { font-family:'Orbitron',monospace !important; font-size:2.2rem !important; color:#FF00FF !important; text-shadow:0 0 20px rgba(255,0,255,0.5); font-weight:900; }
.slot-display {
  font-size:3.5rem; text-align:center; padding:20px;
  background:rgba(0,0,0,0.5); border:2px solid rgba(255,215,0,0.3); border-radius:14px;
  letter-spacing:20px; min-height:100px; display:flex; align-items:center; justify-content:center;
}
.question-box {
  background:linear-gradient(135deg,rgba(0,229,255,0.04),rgba(0,0,100,0.1));
  border:1px solid rgba(0,229,255,0.3); border-radius:14px; padding:28px;
  line-height:1.8; font-size:1.05rem; color:#f0f0ff !important;
}
.mine-card {
  background:linear-gradient(135deg,rgba(139,69,19,0.15),rgba(50,25,0,0.2));
  border:1px solid rgba(180,100,20,0.4); border-radius:14px; padding:20px; text-align:center;
}
.tx-row {
  display:flex; justify-content:space-between; align-items:center;
  padding:9px 14px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.88rem;
}
.cooldown-badge {
  background:rgba(255,80,80,0.15); border:1px solid rgba(255,80,80,0.4);
  border-radius:6px; padding:4px 10px; font-size:0.78rem; color:#FF6060 !important;
  display:inline-block; margin-left:8px;
}
"""

if IS_PC:
    CSS += """
p,span,label,td,th,.stSelectbox label { font-size:1rem !important; }
h1 { font-size:2.2rem !important; color:#00E5FF !important; margin-bottom:4px; }
h2 { font-size:1.5rem !important; color:#00FF88 !important; }
h3 { font-size:1.2rem !important; color:#FFD600 !important; }
.stButton>button { height:52px !important; font-size:1rem !important; }
"""
else:
    CSS += """
p,span,label,td,th { font-size:0.88rem !important; }
h1 { font-size:1.5rem !important; color:#00E5FF !important; }
h2 { font-size:1.15rem !important; color:#00FF88 !important; }
h3 { font-size:1rem !important; color:#FFD600 !important; }
.stButton>button { height:46px !important; font-size:0.88rem !important; }
.stock-table th,.stock-table td { padding:8px 8px; font-size:0.82rem !important; }
.score-number { font-size:2.5rem !important; }
.lotto-amount { font-size:1.6rem !important; }
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ==============================
# 🌐 서버 마켓 동기화
# ==============================
market = get_market()
cur_t  = time.time()
m_up   = False

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
        market['news'] = f"🎊 [당첨 확정] {win}님이 {format_korean_money(prize)} 대박 상금을 수령하셨습니다!!"
        market['lotto_pool'] = 5_000_000_000
        market['lotto_tickets'] = {}
        market['lotto_last_draw'] = cur_t
        m_up = True

if m_up: save_market(market)

# 대출 이자
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
    "🏢 부동산 거래소",
    "🏦 은행 (대출/송금)",
    "⚔️ 글로벌 로또",
    "⚽ 구단주 시뮬레이터",
    "💻 정처기 CBT",
    "🏎️ 하이퍼카 레이싱",
    "🎰 럭키 슬롯",
    "⛏️ 광산 (노가다)",
    "👑 칭호 상점",
    "📜 내 거래 기록",
    "🏅 랭킹 & 게시판",
]
if is_vip:   menu_ops.insert(2, "💎 VIP 라운지")
if is_admin: menu_ops.append("🛠️ 창조주 통제소")

if IS_PC:
    with st.sidebar:
        st.markdown(f"""
<div style='padding:16px;background:rgba(0,229,255,0.05);border-radius:12px;
     border:1px solid rgba(0,229,255,0.2);margin-bottom:16px;'>
  <div style='font-size:1.3rem;font-weight:900;color:#00E5FF;'>👤 {st.session_state.logged_in_user}</div>
  <div style='font-size:0.85rem;color:#FFD600;margin-top:4px;'>{st.session_state.equipped_title}</div>
</div>""", unsafe_allow_html=True)
        st.metric("💵 현금",   format_korean_money(st.session_state.global_cash))
        st.metric("📊 순자산", format_korean_money(nw))
        if st.session_state.loan > 0:
            st.metric("💳 대출잔액", format_korean_money(st.session_state.loan))
        st.write("---")
        menu = st.radio("메뉴", menu_ops, label_visibility="collapsed")
        st.write("---")
        if st.button("🔓 로그아웃", use_container_width=True):
            sync_user_data(); st.session_state.clear(); st.rerun()
else:
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"<div style='font-size:0.82rem;color:#888;'>👤 <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b> | {st.session_state.equipped_title}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.9rem;color:#FFD600;font-weight:900;'>💵 {format_korean_money(st.session_state.global_cash)}</div>", unsafe_allow_html=True)
    with col_b:
        if st.button("로그아웃"):
            sync_user_data(); st.session_state.clear(); st.rerun()
    menu = st.selectbox("메뉴 선택", menu_ops, label_visibility="collapsed")

# 뉴스 배너
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
  <div style='color:#888;font-size:0.8rem;letter-spacing:2px;margin-bottom:12px;'>🕵️ INSIDER INTELLIGENCE</div>
  <div style='font-size:1.4rem;font-weight:900;color:#FFD600;'>{nxt_ico} {nxt_nm}</div>
  <div style='font-size:1.1rem;font-weight:900;color:{clr};margin-top:10px;'>{status}</div>
  <div style='color:#666;font-size:0.78rem;margin-top:14px;'>※ 정보 유출 시 창조주의 징벌이 따릅니다</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎰 VIP 전용 슬롯 (1억, 승률 50%)")
        cd_rem = cooldown_remaining("vip_slot", 5.0)
        if cd_rem > 0:
            st.warning(f"⏱️ 쿨다운 중... {cd_rem:.1f}초")
        elif st.button("💎 VIP 슬롯 당기기", use_container_width=True):
            if st.session_state.global_cash >= 100_000_000:
                set_cooldown("vip_slot")
                st.session_state.global_cash -= 100_000_000
                if random.random() < 0.5:
                    st.session_state.global_cash += 250_000_000
                    st.success("🎉 승리! +2.5억 획득!")
                    log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 승리", 150_000_000)
                else:
                    st.error("❌ 아쉽습니다. 다음 기회를!")
                    log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 패배", -100_000_000)
                sync_user_data(); time.sleep(1.5); st.rerun()
            else: st.error("잔액 부족!")
    with c2:
        st.markdown("### 📊 VIP 포트폴리오 요약")
        total_stock  = sum(st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price'] for s in stock_config)
        total_estate = sum(estate_config[eid]['base_price'] * cnt * 0.8 for eid, cnt in st.session_state.real_estate.items() if eid in estate_config)
        st.metric("주식 평가액",   format_korean_money(total_stock))
        st.metric("부동산 평가액", format_korean_money(total_estate))
        st.metric("총 순자산",     format_korean_money(nw))

# ════════════════════════════════════════════════
# 🏠 홈 광장
# ════════════════════════════════════════════════
elif menu == "🏠 홈 광장":
    st.title("🌌 HYOMIN UNIVERSE")
    st.markdown(f"<div style='color:#888;margin-bottom:24px;'>어서오세요, <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b>님! {st.session_state.equipped_title}</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("💵 현금",    format_korean_money(st.session_state.global_cash))
    with c2: st.metric("📊 순자산",  format_korean_money(nw))
    with c3: st.metric("💳 대출",    format_korean_money(st.session_state.loan))
    with c4:
        total_rent_pending = sum(
            estate_config[eid]['income'] * cnt * int(cur_t - st.session_state.rent_time)
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.metric("🏢 수금 대기", format_korean_money(total_rent_pending))

    st.write("---")
    st.markdown("### 📈 실시간 시장 현황")
    top_stocks = sorted(stock_config, key=lambda s: (
        (market['stock_data'][s['id']]['history'][-1] - market['stock_data'][s['id']]['history'][-2])
        / market['stock_data'][s['id']]['history'][-2]
        if len(market['stock_data'][s['id']]['history']) > 1 else 0
    ), reverse=True)[:5]

    cols = st.columns(5)
    for i, s in enumerate(top_stocks):
        d    = market['stock_data'][s['id']]
        diff = (d['history'][-1] - d['history'][-2]) / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        arrow, clr = ("▲", "#FF4B4B") if diff >= 0 else ("▼", "#4B9EFF")
        with cols[i]:
            st.markdown(f"""
<div class='card' style='text-align:center;padding:14px;'>
  <div style='font-size:1.4rem;'>{s['icon']}</div>
  <div style='font-size:0.78rem;color:#888;margin:4px 0;'>{d['name'][:6]}</div>
  <div style='font-size:1rem;font-weight:900;color:#fff;'>₩{d['price']:,}</div>
  <div style='font-size:0.85rem;color:{clr};font-weight:900;'>{arrow} {abs(diff):.2f}%</div>
</div>""", unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🏆 이번 시즌 랭킹 Top 5")
    users_all = load_db(USERS_FILE, {})
    rank_data = []
    for uid, udata in users_all.items():
        if uid == "5891": continue
        w = udata.get('cash', 0) - udata.get('loan', 0)
        for sid, p in udata.get('portfolio', {}).items():
            if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
        for eid, cnt in udata.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * cnt * 0.8
        rank_data.append({"uid": uid, "title": udata.get('equipped_title', '신규시민'), "nw": w})
    rank_data.sort(key=lambda x: x['nw'], reverse=True)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i, r in enumerate(rank_data[:5]):
        me = " ← 나" if r['uid'] == st.session_state.logged_in_user else ""
        st.markdown(f"""
<div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 20px;'>
  <span style='font-size:1.3rem;'>{medals[i]}</span>
  <span style='font-weight:900;color:#E8E8F0;'>{r['uid']}{me}</span>
  <span style='color:#888;font-size:0.85rem;'>{r['title']}</span>
  <span style='color:#FFD600;font-weight:900;'>{format_korean_money(r['nw'])}</span>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 📈 주식 트레이딩  (광클 방지 + 돈복사 방지 강화)
# ════════════════════════════════════════════════
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소")

    # ── 주식 거래 쿨다운 설정 ──
    TRADE_COOLDOWN   = 3.0   # 일반 매수/매도 쿨다운 (초)
    BULK_COOLDOWN    = 8.0   # 풀매수/풀매도 쿨다운 (초) — 조작 방지
    DAILY_BULK_LIMIT = 5     # 풀매수+풀매도 하루 합산 최대 횟수

    # 당일 거래 횟수 추적
    today_str = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.get("bulk_trade_date") != today_str:
        st.session_state.bulk_trade_date  = today_str
        st.session_state.bulk_trade_count = 0

    tab_market, tab_port, tab_trade = st.tabs(["📊 전체 시황", "💼 내 포트폴리오", "⚡ 빠른 거래"])

    with tab_market:
        rows = ""
        for s in stock_config:
            d    = market['stock_data'][s['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲"   if diff > 0 else "▼"        if diff < 0 else "━"
            rows += f"<tr><td>{s['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#fff;'>₩{d['price']:,}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td><td style='text-align:right;color:#888;'>₩{d['history'][-2]:,}</td></tr>"
        st.markdown(f"<table class='stock-table'><thead><tr><th>종목</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th><th style='text-align:right;'>전일가</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

    with tab_port:
        p_rows = []; total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp  = market['stock_data'][sid]['price']
                ap  = info.get('avg_price', 0)
                ev  = qty * cp; total_eval += ev
                roi = (cp - ap) / ap * 100 if ap > 0 else 0
                p_rows.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주",
                                "평균단가": f"₩{int(ap):,}", "평가액": f"₩{int(ev):,}",
                                "수익률": f"{roi:+.2f}%"})
        if p_rows:
            st.table(pd.DataFrame(p_rows))
            st.metric("📊 주식 총 평가액", format_korean_money(total_eval))
        else:
            st.info("보유 중인 주식이 없습니다.")

    with tab_trade:
        sel_n = st.selectbox("거래 종목 선택", [f"{s['icon']} {s['name']}" for s in stock_config])
        sid   = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        d     = market['stock_data'][sid]
        cp    = d['price']

        if len(d['history']) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=d['history'], mode='lines',
                                     line=dict(color='#00E5FF', width=2),
                                     fill='tozeroy', fillcolor='rgba(0,229,255,0.05)'))
            fig.update_layout(height=220, template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              xaxis=dict(showgrid=False, showticklabels=False),
                              yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
            st.plotly_chart(fig, use_container_width=True)

        diff = cp - d['history'][-2] if len(d['history']) > 1 else 0
        pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        clr  = "#FF4B4B" if diff >= 0 else "#4B9EFF"
        arr  = "▲" if diff >= 0 else "▼"
        st.markdown(f"<div style='text-align:center;margin:10px 0;'><span style='font-size:1.8rem;font-weight:900;color:#fff;font-family:Orbitron;'>₩{cp:,}</span> <span style='color:{clr};font-weight:900;'>{arr} {abs(pct):.2f}%</span></div>", unsafe_allow_html=True)

        qty_input = st.number_input("거래 수량 (주)", min_value=1, step=1, value=1)
        cost = qty_input * cp
        st.caption(f"예상 거래금액: {format_korean_money(cost)}")

        # 쿨다운 상태 표시
        bulk_rem  = cooldown_remaining("bulk_trade", BULK_COOLDOWN)
        trade_rem = cooldown_remaining(f"trade_{sid}", TRADE_COOLDOWN)
        bulk_left = DAILY_BULK_LIMIT - st.session_state.get("bulk_trade_count", 0)

        if bulk_rem > 0:
            st.markdown(f"<span class='cooldown-badge'>풀매수/풀매도 쿨다운 {bulk_rem:.1f}초</span>", unsafe_allow_html=True)
        if trade_rem > 0:
            st.markdown(f"<span class='cooldown-badge'>일반 거래 쿨다운 {trade_rem:.1f}초</span>", unsafe_allow_html=True)

        st.markdown(f"<div style='color:#666;font-size:0.78rem;margin-bottom:8px;'>풀매수/풀매도 오늘 남은 횟수: <b style='color:#FFD600;'>{bulk_left}회</b></div>", unsafe_allow_html=True)

        def _safe_buy(qty, price, sid_):
            total = qty * price
            if st.session_state.global_cash < total:
                st.error("잔액 부족!"); return False
            st.session_state.global_cash -= total
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += total
                st.error("거래 취소 (잔액 보호)"); return False
            old = st.session_state.portfolio.get(sid_, {'qty': 0, 'avg_price': 0})
            new_q = old['qty'] + qty
            new_a = ((old['qty'] * old['avg_price']) + total) / new_q
            st.session_state.portfolio[sid_] = {'qty': new_q, 'avg_price': new_a}
            log_tx(st.session_state.logged_in_user, "주식매수", f"{market['stock_data'][sid_]['name']} {qty}주 매수", -total)
            return True

        def _safe_sell(qty, price, sid_):
            own = st.session_state.portfolio.get(sid_, {'qty': 0})['qty']
            if own < qty:
                st.error(f"보유 수량 부족! (현재 {own}주)"); return False
            earn = qty * price
            st.session_state.global_cash += earn
            st.session_state.portfolio[sid_]['qty'] -= qty
            log_tx(st.session_state.logged_in_user, "주식매도", f"{market['stock_data'][sid_]['name']} {qty}주 매도", earn)
            return True

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            bulk_ok = (bulk_rem <= 0) and (bulk_left > 0)
            if st.button("💥 풀매수", use_container_width=True, disabled=not bulk_ok):
                max_q = st.session_state.global_cash // cp
                if max_q > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    buy_a = max_q * cp
                    if _safe_buy(max_q, cp, sid):
                        # 가격 영향: 최대 8%, 거래대금에 비례
                        imp = min((buy_a / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = int(cp * (1 + imp))
                            market['news'] = f"🐋 [고래 매수] {st.session_state.logged_in_user}님이 {d['name']} 거액 매수! +{imp*100:.1f}% 영향"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("잔액 부족!")

        with c2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True, disabled=trade_rem > 0):
                if trade_rem <= 0:
                    set_cooldown(f"trade_{sid}")
                    if _safe_buy(qty_input, cp, sid):
                        sync_user_data(); st.success(f"✅ {qty_input}주 매수 완료!"); time.sleep(1); st.rerun()

        with c3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True, disabled=trade_rem > 0):
                if trade_rem <= 0:
                    set_cooldown(f"trade_{sid}")
                    if _safe_sell(qty_input, cp, sid):
                        sync_user_data(); st.success(f"✅ {qty_input}주 매도!"); time.sleep(1); st.rerun()

        with c4:
            bulk_ok2 = (bulk_rem <= 0) and (bulk_left > 0)
            if st.button("💸 풀매도", use_container_width=True, disabled=not bulk_ok2):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    sell_a = own * cp
                    if _safe_sell(own, cp, sid):
                        # 가격 영향: 최대 8%
                        imp = min((sell_a / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                            market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {d['name']} 물량 투하! -{imp*100:.1f}% 영향"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("보유 주식 없음")

        # 풀매수/풀매도 횟수 소진 안내
        if bulk_left <= 0:
            st.warning("⚠️ 오늘 풀매수/풀매도 횟수를 모두 사용했습니다. 내일 자정에 초기화됩니다.")

    if menu == "📈 주식 트레이딩":
        time.sleep(3); st.rerun()

# ════════════════════════════════════════════════
# 🏢 부동산 거래소 (전면 재설계: 실거래 마켓 시스템)
# ════════════════════════════════════════════════
elif menu == "🏢 부동산 거래소":
    st.title("🏢 부동산 실거래 마켓")

    uid = st.session_state.logged_in_user
    now = time.time()

    # 임대 수익 수금 섹션
    pass_s = int(now - st.session_state.rent_time)
    total_income_rate = sum(
        estate_config[eid]['income'] * cnt
        for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
    )
    pending = total_income_rate * pass_s

    if total_income_rate > 0:
        st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,100,50,0.1));
     border:1px solid rgba(0,255,136,0.3);border-radius:14px;padding:18px;text-align:center;margin-bottom:16px;'>
  <div style='color:#888;font-size:0.82rem;letter-spacing:2px;margin-bottom:6px;'>누적 임대 수익</div>
  <div style='font-family:Orbitron,monospace;font-size:1.8rem;font-weight:900;color:#00FF88;'>{format_korean_money(pending)}</div>
  <div style='color:#666;font-size:0.78rem;margin-top:6px;'>초당 {format_korean_money(total_income_rate)} 수입 중</div>
</div>""", unsafe_allow_html=True)

        cd_rent = cooldown_remaining("rent_collect", 3.0)
        if cd_rent > 0:
            st.warning(f"⏱️ 수금 쿨다운 {cd_rent:.1f}초")
        elif st.button("💰 임대 수익 수금하기", use_container_width=True):
            set_cooldown("rent_collect")
            if pending > 0:
                st.session_state.global_cash += int(pending)
                st.session_state.rent_time = now
                log_tx(uid, "부동산수금", "임대 수익 수금", int(pending))
                sync_user_data()
                st.success(f"✅ {format_korean_money(pending)} 수금 완료!")
                time.sleep(0.8); st.rerun()

    st.write("---")

    em = load_estate_market()
    initial_listings = get_estate_initial_listings(em)

    tab_market_view, tab_my_estate, tab_sell = st.tabs(["🏪 마켓 (전체 매물)", "🏘️ 내 보유 부동산", "📋 판매 등록"])

    # ──────────────────────────────
    # 탭 1: 전체 마켓 (초기 매물 + 유저 매물)
    # ──────────────────────────────
    with tab_market_view:
        st.markdown("### 🏗️ 신규 공급 매물 (운영사 직판)")
        st.caption("수량 제한 있음 — 소진 시 유저 매물만 구매 가능")

        if not initial_listings:
            st.info("현재 신규 공급 매물이 없습니다. 유저 매물을 확인하세요!")
        else:
            for il in initial_listings:
                eid  = il["eid"]
                info = estate_config[eid]
                c1, c2 = st.columns([5, 2])
                with c1:
                    st.markdown(f"""
<div class='market-initial'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.8rem;'>{info['icon']}</span>
    <div>
      <div style='font-weight:900;font-size:1rem;color:#fff;'>{info['name']}</div>
      <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
      <div style='margin-top:4px;'>
        <span style='color:#FFD600;font-weight:900;'>{format_korean_money(info['base_price'])}</span>
        <span style='color:#555;margin:0 8px;'>|</span>
        <span class='estate-income'>+{format_korean_money(info['income'])}/초</span>
        <span style='color:#888;margin-left:10px;font-size:0.78rem;'>잔여 {il['remaining']}개</span>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                with c2:
                    can_buy = st.session_state.global_cash >= info['base_price']
                    cd_key  = f"estate_buy_{eid}_initial"
                    cd_rem  = cooldown_remaining(cd_key, 4.0)
                    if cd_rem > 0:
                        st.warning(f"⏱️ {cd_rem:.1f}초")
                    elif st.button("🏗️ 매입" if can_buy else "💸 잔액부족",
                                   key=f"init_buy_{eid}", use_container_width=True, disabled=not can_buy):
                        # 재고 재확인 (경쟁 방지)
                        em2 = load_estate_market()
                        il2 = next((x for x in get_estate_initial_listings(em2) if x["eid"] == eid), None)
                        if il2 is None or il2["remaining"] <= 0:
                            st.error("⚠️ 이미 매진되었습니다! 유저 매물을 확인하세요.")
                        elif st.session_state.global_cash >= info['base_price']:
                            set_cooldown(cd_key)
                            st.session_state.global_cash -= info['base_price']
                            st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                            # 소유 현황 업데이트
                            if uid not in em2["owner_counts"]:
                                em2["owner_counts"][uid] = {}
                            em2["owner_counts"][uid][eid] = em2["owner_counts"][uid].get(eid, 0) + 1
                            save_estate_market(em2)
                            log_tx(uid, "부동산매입", f"{info['name']} 신규 매입", -info['base_price'])
                            sync_user_data()
                            st.success(f"✅ {info['name']} 매입 완료!")
                            time.sleep(0.8); st.rerun()
                        else:
                            st.error("잔액 부족!")

        st.write("---")
        st.markdown("### 🔄 유저 매물 (2차 시장)")
        st.caption("다른 유저가 판매 등록한 매물입니다. 판매자에게 대금이 지급됩니다.")

        user_listings = [l for l in em["listings"] if l["seller"] != uid]
        if not user_listings:
            st.info("현재 등록된 유저 매물이 없습니다.")
        else:
            # 종목별로 그룹핑
            listings_by_eid = {}
            for l in user_listings:
                listings_by_eid.setdefault(l["eid"], []).append(l)

            for eid, llist in listings_by_eid.items():
                info = estate_config.get(eid)
                if not info: continue
                # 가장 저렴한 순으로 정렬
                llist_sorted = sorted(llist, key=lambda x: x["price"])
                st.markdown(f"#### {info['icon']} {info['name']} — {len(llist)}건 매물")
                for li in llist_sorted:
                    premium = (li['price'] - info['base_price']) / info['base_price'] * 100
                    prem_str = f"+{premium:.1f}%" if premium > 0 else f"{premium:.1f}%"
                    prem_col = "#FF4B4B" if premium > 0 else "#4B9EFF"
                    c1, c2 = st.columns([5, 2])
                    with c1:
                        st.markdown(f"""
<div class='market-listing'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div>
      <span style='color:#aaa;font-size:0.8rem;'>판매자: </span>
      <b style='color:#00E5FF;'>{li['seller']}</b>
      <span style='color:{prem_col};font-size:0.78rem;margin-left:10px;'>{prem_str} (기준가 대비)</span>
    </div>
    <div style='text-align:right;'>
      <div style='font-size:1.1rem;font-weight:900;color:#FFD600;'>{format_korean_money(li['price'])}</div>
      <div class='estate-income'>+{format_korean_money(info['income'])}/초</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                    with c2:
                        can_buy = st.session_state.global_cash >= li['price']
                        cd_key  = f"estate_buy_{li['id']}"
                        cd_rem  = cooldown_remaining(cd_key, 4.0)
                        if cd_rem > 0:
                            st.warning(f"⏱️ {cd_rem:.1f}초")
                        elif st.button("🛒 구매" if can_buy else "💸 잔액부족",
                                       key=f"buy_listing_{li['id']}", use_container_width=True, disabled=not can_buy):
                            # 매물 재확인 (중복 구매 방지)
                            em3 = load_estate_market()
                            target = next((x for x in em3["listings"] if x["id"] == li["id"]), None)
                            if target is None:
                                st.error("⚠️ 이미 판매된 매물입니다.")
                            elif st.session_state.global_cash >= target["price"]:
                                set_cooldown(cd_key)
                                # 구매자 처리
                                st.session_state.global_cash -= target["price"]
                                st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                                if uid not in em3["owner_counts"]:
                                    em3["owner_counts"][uid] = {}
                                em3["owner_counts"][uid][eid] = em3["owner_counts"][uid].get(eid, 0) + 1
                                # 판매자에게 대금 지급
                                seller = target["seller"]
                                us = load_db(USERS_FILE, {})
                                if seller in us:
                                    us[seller]['cash'] += target["price"]
                                    if seller not in em3["owner_counts"]:
                                        em3["owner_counts"][seller] = {}
                                    em3["owner_counts"][seller][eid] = max(0, em3["owner_counts"][seller].get(eid, 1) - 1)
                                    save_db(USERS_FILE, us)
                                    log_tx(seller, "부동산판매", f"{info['name']} 판매 완료", target["price"])
                                # 매물 제거
                                em3["listings"] = [x for x in em3["listings"] if x["id"] != li["id"]]
                                save_estate_market(em3)
                                log_tx(uid, "부동산구매", f"{info['name']} 유저 매물 구매", -target["price"])
                                sync_user_data()
                                market['news'] = f"🏢 [{uid}] {info['name']} 유저 매물 구매 완료!"
                                save_market(market)
                                st.success(f"✅ {info['name']} 구매 완료! {format_korean_money(target['price'])}")
                                time.sleep(0.8); st.rerun()
                            else:
                                st.error("잔액 부족!")

    # ──────────────────────────────
    # 탭 2: 내 보유 부동산
    # ──────────────────────────────
    with tab_my_estate:
        owned_any = any(v > 0 for v in st.session_state.real_estate.values())
        if not owned_any:
            st.info("보유 중인 부동산이 없습니다. 마켓에서 매입하세요!")
        else:
            for eid, cnt in st.session_state.real_estate.items():
                if cnt <= 0 or eid not in estate_config: continue
                info = estate_config[eid]
                # 내가 이미 판매 등록한 수량 확인
                my_listed = sum(1 for l in em["listings"] if l["eid"] == eid and l["seller"] == uid)
                available_to_sell = cnt - my_listed
                st.markdown(f"""
<div class='estate-card'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='display:flex;align-items:center;gap:12px;'>
      <span style='font-size:2rem;'>{info['icon']}</span>
      <div>
        <div style='font-weight:900;font-size:1.05rem;color:#fff;'>{info['name']}</div>
        <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
        <div style='margin-top:4px;'>
          <span style='color:#aaa;font-size:0.82rem;'>보유 {cnt}채 (판매 등록 {my_listed}채)</span>
          <span style='color:#555;margin:0 8px;'>|</span>
          <span class='estate-income'>+{format_korean_money(info['income'] * cnt)}/초</span>
        </div>
      </div>
    </div>
    <div style='text-align:right;'>
      <div style='color:#888;font-size:0.78rem;'>현재 평가액</div>
      <div style='color:#FFD600;font-weight:900;'>{format_korean_money(info['base_price'] * cnt * 0.8)}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                if available_to_sell > 0:
                    st.caption(f"👆 판매 등록 가능: {available_to_sell}채 → '판매 등록' 탭에서 진행하세요")
                elif my_listed > 0:
                    st.caption("⏳ 모든 물건이 판매 등록 중입니다.")

    # ──────────────────────────────
    # 탭 3: 판매 등록 / 내 매물 관리
    # ──────────────────────────────
    with tab_sell:
        st.markdown("### 📋 내 매물 판매 등록")
        st.caption("판매 등록 후 다른 유저가 구매하면 현금이 즉시 입금됩니다. 거래 수수료: 2%")

        # 판매 가능한 부동산 목록
        sellable = [(eid, cnt) for eid, cnt in st.session_state.real_estate.items()
                    if cnt > 0 and eid in estate_config]
        # 이미 등록한 수량 제외
        sellable_net = []
        for eid, cnt in sellable:
            my_listed = sum(1 for l in em["listings"] if l["eid"] == eid and l["seller"] == uid)
            if cnt - my_listed > 0:
                sellable_net.append((eid, cnt, my_listed))

        if not sellable_net:
            st.info("판매 등록 가능한 부동산이 없습니다. 모두 이미 등록되었거나 보유가 없습니다.")
        else:
            sel_eid = st.selectbox(
                "판매할 부동산 선택",
                [e for e, c, ml in sellable_net],
                format_func=lambda e: f"{estate_config[e]['icon']} {estate_config[e]['name']} (판매 가능 {dict({e:(c-ml) for e,c,ml in sellable_net}).get(e,0)}채)"
            )
            sel_info = estate_config[sel_eid]
            min_price = int(sel_info['base_price'] * 0.5)
            max_price = int(sel_info['base_price'] * 3.0)
            sell_price = st.number_input(
                f"판매 희망가 (기준가: {format_korean_money(sel_info['base_price'])})",
                min_value=min_price,
                max_value=max_price,
                value=sel_info['base_price'],
                step=int(sel_info['base_price'] * 0.01),
                format="%d"
            )
            fee = int(sell_price * 0.02)
            net_receive = sell_price - fee
            st.caption(f"📌 판매 시 수수료 2% ({format_korean_money(fee)}) 공제 → 실수령 {format_korean_money(net_receive)}")

            cd_list_rem = cooldown_remaining("estate_list", 5.0)
            if cd_list_rem > 0:
                st.warning(f"⏱️ 등록 쿨다운 {cd_list_rem:.1f}초")
            elif st.button("📋 판매 등록하기", use_container_width=True):
                set_cooldown("estate_list")
                import uuid as _uuid
                new_listing = {
                    "id": str(_uuid.uuid4())[:8],
                    "eid": sel_eid,
                    "seller": uid,
                    "price": sell_price,
                    "net_receive": net_receive,
                    "listed_time": time.time()
                }
                em_fresh = load_estate_market()
                em_fresh["listings"].append(new_listing)
                save_estate_market(em_fresh)
                market['news'] = f"🏢 [{uid}] {sel_info['name']} {format_korean_money(sell_price)}에 매물 등록!"
                save_market(market)
                st.success(f"✅ {sel_info['name']} 판매 등록 완료! 구매자 대기 중...")
                time.sleep(0.8); st.rerun()

        # 내 등록 매물 관리
        st.write("---")
        st.markdown("### 🗂️ 내 등록 매물 관리")
        my_listings = [l for l in em["listings"] if l["seller"] == uid]
        if not my_listings:
            st.info("현재 등록된 매물이 없습니다.")
        else:
            for li in my_listings:
                info = estate_config.get(li["eid"], {})
                listed_dt = datetime.fromtimestamp(li.get("listed_time", 0)).strftime("%m/%d %H:%M")
                c1, c2 = st.columns([5, 2])
                with c1:
                    st.markdown(f"""
<div class='my-listing'>
  <div style='display:flex;justify-content:space-between;'>
    <div>
      <span style='font-size:1.2rem;'>{info.get('icon','🏠')}</span>
      <b style='color:#fff;margin-left:8px;'>{info.get('name','?')}</b>
      <span style='color:#888;font-size:0.78rem;margin-left:8px;'>등록: {listed_dt}</span>
    </div>
    <div style='text-align:right;'>
      <div style='color:#FFD600;font-weight:900;'>{format_korean_money(li['price'])}</div>
      <div style='color:#888;font-size:0.78rem;'>실수령 {format_korean_money(li.get('net_receive', li['price']))}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌ 등록 취소", key=f"cancel_{li['id']}", use_container_width=True):
                        em_fresh = load_estate_market()
                        em_fresh["listings"] = [x for x in em_fresh["listings"] if x["id"] != li["id"]]
                        save_estate_market(em_fresh)
                        st.success("매물 등록 취소 완료!")
                        time.sleep(0.5); st.rerun()

# ════════════════════════════════════════════════
# 🏦 은행
# ════════════════════════════════════════════════
elif menu == "🏦 은행 (대출/송금)":
    st.title("🏦 하이리스크 뱅크")

    st.markdown("""
<div class='card' style='margin-bottom:16px;'>
  <div style='color:#888;font-size:0.82rem;'>⚠️ 대출 조건: 10초마다 <b style='color:#FF4B4B;'>2% 복리 이자</b>가 붙습니다.</div>
</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 현금",    format_korean_money(st.session_state.global_cash))
    c2.metric("💳 대출잔액", format_korean_money(st.session_state.loan))
    c3.metric("📊 순자산",  format_korean_money(nw))

    tab_send, tab_loan = st.tabs(["💸 송금", "💳 대출/상환"])

    with tab_send:
        target = st.text_input("받는 분 아이디", placeholder="상대방 아이디 입력")
        amt    = st.number_input("송금 금액 (원)", min_value=0, step=1_000_000, format="%d")
        st.caption(f"송금 예정: {format_korean_money(amt)}")
        cd_send = cooldown_remaining("send_money", 5.0)
        if cd_send > 0:
            st.warning(f"⏱️ 송금 쿨다운 {cd_send:.1f}초")
        elif st.button("📤 송금하기", use_container_width=True):
            us = load_db(USERS_FILE, {})
            if target not in us:
                st.error("존재하지 않는 사용자입니다.")
            elif st.session_state.global_cash < amt:
                st.error("잔액이 부족합니다.")
            elif amt <= 0:
                st.error("금액을 입력하세요.")
            else:
                set_cooldown("send_money")
                st.session_state.global_cash -= amt
                us[target]['cash'] += amt
                save_db(USERS_FILE, us)
                log_tx(st.session_state.logged_in_user, "송금", f"{target}에게 송금", -amt)
                sync_user_data()
                st.success(f"✅ {target}님께 {format_korean_money(amt)} 송금 완료!")

    with tab_loan:
        max_loan_limit = max(100_000_000, int(nw * 0.5))
        avail_loan = max(0, max_loan_limit - st.session_state.loan)

        st.info(f"💡 최대 대출 한도: {format_korean_money(max_loan_limit)} (순자산의 50%)\n💸 현재 대출 가능액: {format_korean_money(avail_loan)}\n⚠️ 대출 실행 시 1%의 선취 수수료가 공제됩니다.")

        if avail_loan > 0:
            l_amt = st.number_input("대출 금액 (원)", min_value=0, max_value=int(avail_loan), step=10_000_000, format="%d", key="loan_in")
            cd_loan = cooldown_remaining("loan_action", 5.0)
            if cd_loan > 0:
                st.warning(f"⏱️ 대출 쿨다운 {cd_loan:.1f}초")
            elif st.button("💳 대출 실행", use_container_width=True):
                if l_amt > 0 and l_amt <= avail_loan:
                    set_cooldown("loan_action")
                    fee = int(l_amt * 0.01)
                    actual_receive = l_amt - fee
                    st.session_state.global_cash += actual_receive
                    st.session_state.loan += l_amt
                    st.session_state.loan_time = time.time()
                    log_tx(st.session_state.logged_in_user, "대출", f"대출 실행 (수수료 {format_korean_money(fee)} 공제)", actual_receive)
                    sync_user_data()
                    st.success(f"✅ {format_korean_money(l_amt)} 대출 완료! (수수료 공제 후 {format_korean_money(actual_receive)} 입금)")
                    time.sleep(1.5); st.rerun()
                elif l_amt > avail_loan:
                    st.error("대출 한도를 초과했습니다!")
        else:
            st.error("🚨 현재 대출 한도를 모두 소진하셨습니다.")

        st.write("---")
        r_amt = st.number_input("상환 금액 (원)", min_value=0, step=100_000_000, format="%d", key="repay_in")
        cd_repay = cooldown_remaining("repay_action", 3.0)
        if cd_repay > 0:
            st.warning(f"⏱️ 상환 쿨다운 {cd_repay:.1f}초")
        elif st.button("🏦 상환하기", use_container_width=True):
            actual = min(r_amt, st.session_state.loan)
            if st.session_state.global_cash >= actual and actual > 0:
                set_cooldown("repay_action")
                st.session_state.global_cash -= actual
                st.session_state.loan -= actual
                if st.session_state.loan <= 0:
                    st.session_state.loan = 0
                    if st.session_state.equipped_title == "💸 신용불량자":
                        st.session_state.equipped_title = "🌱 신규시민"
                        st.success("🎉 대출 전액 상환 완료! 신용이 회복되었습니다.")
                    else:
                        st.success("🎉 대출 전액 상환 완료!")
                else:
                    st.success(f"✅ {format_korean_money(actual)} 상환 완료. 잔여 대출: {format_korean_money(st.session_state.loan)}")
                log_tx(st.session_state.logged_in_user, "대출상환", "대출 상환", -actual)
                sync_user_data(); time.sleep(1); st.rerun()
            else:
                st.error("잔액 부족 또는 상환 금액 오류")

# ════════════════════════════════════════════════
# ⚔️ 글로벌 로또
# ════════════════════════════════════════════════
elif menu == "⚔️ 글로벌 로또":
    st.title("⚔️ 1시간 글로벌 로또")

    rem          = max(0, int(3_600 - (time.time() - market['lotto_last_draw'])))
    my_t         = market['lotto_tickets'].get(st.session_state.logged_in_user, 0)
    total_tickets = sum(market['lotto_tickets'].values()) if market['lotto_tickets'] else 0
    my_pct       = (my_t / total_tickets * 100) if total_tickets > 0 else 0

    st.markdown(f"""
<div class='lotto-pool'>
  <div style='color:#888;font-size:0.8rem;letter-spacing:3px;margin-bottom:10px;'>JACKPOT POOL</div>
  <div class='lotto-amount'>₩{market['lotto_pool']:,}</div>
  <div style='color:#888;margin-top:14px;font-size:0.88rem;'>⏱ 추첨까지 <b style='color:#FF00FF;'>{rem//60}분 {rem%60}초</b></div>
  <div style='color:#888;font-size:0.82rem;margin-top:6px;'>내 당첨 확률: <b style='color:#FFD600;'>{my_pct:.1f}%</b> ({my_t}장 / 전체 {total_tickets}장)</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([2, 1])
    with c1:
        b_cnt = st.number_input("구매 수량 (장당 1,000만원)", min_value=1, step=1, value=1)
        cost  = b_cnt * 10_000_000
        st.caption(f"총 비용: {format_korean_money(cost)}")
    with c2:
        st.metric("내 티켓", f"{my_t}장")

    cd_lotto = cooldown_remaining("lotto_buy", 3.0)
    if cd_lotto > 0:
        st.warning(f"⏱️ 쿨다운 {cd_lotto:.1f}초")
    elif st.button("🎫 티켓 구매하기", use_container_width=True):
        if st.session_state.global_cash >= cost:
            set_cooldown("lotto_buy")
            st.session_state.global_cash -= cost
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += cost
                st.error("거래 취소 (잔액 보호)")
            else:
                market['lotto_pool']    += cost
                market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt
                save_market(market)
                log_tx(st.session_state.logged_in_user, "로또", f"로또 {b_cnt}장 구매", -cost)
                sync_user_data()
                st.success(f"✅ {b_cnt}장 구매 완료!")
                time.sleep(1); st.rerun()
        else:
            st.error("잔액 부족!")

    if market['lotto_tickets']:
        st.write("---")
        st.markdown("### 👥 현재 참여자")
        sorted_t = sorted(market['lotto_tickets'].items(), key=lambda x: x[1], reverse=True)
        for uid_l, cnt in sorted_t[:10]:
            pct     = cnt / total_tickets * 100
            me_mark = " 👈" if uid_l == st.session_state.logged_in_user else ""
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'><span style='color:#ddd;'>{uid_l}{me_mark}</span><span style='color:#FF00FF;font-weight:900;'>{cnt}장 ({pct:.1f}%)</span></div>", unsafe_allow_html=True)

    time.sleep(5); st.rerun()

# ════════════════════════════════════════════════
# ⚽ 구단주 시뮬레이터
# ════════════════════════════════════════════════
elif menu == "⚽ 구단주 시뮬레이터":
    st.title("🏆 구단주 시뮬레이터")

    FORMATION_STATS = {
        "4-4-2 (균형)":     {"atk": 0.30, "def": 0.27, "emoji": "⚖️"},
        "4-3-3 (공격)":     {"atk": 0.42, "def": 0.15, "emoji": "🔥"},
        "3-5-2 (중원장악)": {"atk": 0.27, "def": 0.22, "emoji": "🧠"},
        "5-3-2 (수비철벽)": {"atk": 0.18, "def": 0.38, "emoji": "🛡️"},
        "4-2-3-1 (현대)":   {"atk": 0.33, "def": 0.24, "emoji": "⚡"},
        "3-4-3 (총공격)":   {"atk": 0.48, "def": 0.10, "emoji": "💥"},
    }
    STADIUMS = ["🏟️ 효민 아레나", "⚽ 갤럭시 스타디움", "🌌 유니버스 파크", "🔥 인페르노 필드"]

    c1, c2 = st.columns(2)
    with c1:
        my_team  = st.text_input("내 팀 이름", value="FC 효민")
        my_form  = st.selectbox("포메이션", list(FORMATION_STATS.keys()), key="mf")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[my_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[my_form]['def']*10)}</div>", unsafe_allow_html=True)
    with c2:
        opp_team = st.text_input("상대 팀", value="FC 라이벌")
        opp_form = st.selectbox("상대 포메이션", list(FORMATION_STATS.keys()), key="of")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[opp_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[opp_form]['def']*10)}</div>", unsafe_allow_html=True)

    stadium = st.selectbox("경기장", STADIUMS)
    betting = st.number_input("경기 베팅금액 (내 팀 승리 시 2배)", min_value=0, step=1_000_000, value=0)

    cd_soccer = cooldown_remaining("soccer_game", 10.0)
    if cd_soccer > 0:
        st.warning(f"⏱️ 경기 쿨다운 {cd_soccer:.1f}초 (광클 방지)")
    elif st.button("⚽ 킥오프!", use_container_width=True):
        if betting > 0 and st.session_state.global_cash < betting:
            st.error("베팅 금액이 잔액을 초과합니다.")
        else:
            set_cooldown("soccer_game")
            if betting > 0: st.session_state.global_cash -= betting

            my_s  = FORMATION_STATS[my_form]
            opp_s = FORMATION_STATS[opp_form]
            h_score = a_score = 0
            scoreboard  = st.empty()
            comm_box    = st.empty()
            prog_bar    = st.progress(0, text="전반전 시작!")
            commentaries = []

            ALL_EVENTS = {
                "my_goal":  ["⚽ 골!!!! {my}의 환상적인 왼발 슈팅!", "⚽ {my} 코너킥 헤더로 득점!", "⚽ {my}의 원더골!"],
                "opp_goal": ["⚽ {opp}이 반격합니다!", "⚽ {opp}의 역습 득점!", "⚽ {opp}이 기습 골!"],
                "my_save":  ["🧤 우리 GK의 슈퍼세이브!", "🛡️ {my} 수비수의 살신성인 태클!"],
                "opp_save": ["🛡️ {opp} GK가 막아냅니다!", "⛔ {opp} 오프사이드!"],
                "neutral":  ["📊 팽팽한 중원 다툼...", "🌟 관중석의 열기!", "⚡ {my} 드리블 돌파!"],
            }
            def pick(key):
                return random.choice(ALL_EVENTS[key]).format(my=my_team[:6], opp=opp_team[:6])

            for minute in range(1, 19):
                time.sleep(0.45)
                real_min = minute * 5
                if real_min == 45:
                    commentaries.insert(0, f"🔔 전반 종료! 스코어: {h_score} : {a_score}")
                if random.random() < my_s['atk']:
                    if random.random() > opp_s['def']:
                        h_score += 1; commentaries.insert(0, f"🕐 {real_min}' | {pick('my_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_save')}")
                if random.random() < opp_s['atk']:
                    if random.random() > my_s['def']:
                        a_score += 1; commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('my_save')}")
                if random.random() < 0.35:
                    commentaries.insert(0, f"🕐 {real_min}' | {pick('neutral')}")

                scoreboard.markdown(f"""
<div class='scoreboard'>
  <div style='color:#555;font-size:0.78rem;letter-spacing:2px;margin-bottom:16px;'>{stadium}</div>
  <div style='display:flex;justify-content:space-around;align-items:center;'>
    <div><div class='team-label'>{my_team}</div><div style='color:#666;font-size:0.78rem;'>{my_form}</div></div>
    <div><div class='score-number'>{h_score} : {a_score}</div><div class='match-time'>⏱ {real_min}' / 90'</div></div>
    <div><div class='team-label'>{opp_team}</div><div style='color:#666;font-size:0.78rem;'>{opp_form}</div></div>
  </div>
</div>""", unsafe_allow_html=True)
                comm_box.markdown("".join(f"<div class='commentary-item'>{c}</div>" for c in commentaries[:6]), unsafe_allow_html=True)
                prog_bar.progress(minute/18, text=f"{'전반' if real_min<=45 else '후반'} {min(real_min,90)}분")

            prog_bar.progress(1.0, text="⚽ 경기 종료!")
            st.write("---")
            if h_score > a_score:
                st.success(f"🎉 승리! {my_team} {h_score}:{a_score} {opp_team}")
                reward = 10_000_000 + betting * 2 if betting > 0 else 5_000_000; st.balloons()
            elif h_score == a_score:
                st.warning(f"🤝 무승부! {h_score}:{a_score}")
                reward = 2_000_000 + (betting if betting > 0 else 0)
            else:
                st.error(f"😢 패배... {h_score}:{a_score}")
                reward = 500_000

            st.session_state.global_cash += reward
            log_tx(st.session_state.logged_in_user, "축구베팅", f"구단주 경기 보상", reward)
            sync_user_data()
            st.info(f"💰 경기 보상: +{format_korean_money(reward)}")
            time.sleep(3); st.rerun()

# ════════════════════════════════════════════════
# 💻 정처기 CBT
# ════════════════════════════════════════════════
elif menu == "💻 정처기 CBT":
    st.title("💻 정보처리기사 실전 CBT")
    st.caption("실제 정처기 수준의 문제입니다. 정답 시 50만원 지급!")

    QUESTION_POOL = [
        {"q": "제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행 함수 종속 제거","다치 종속 제거","조인 종속 제거"], "cat": "데이터베이스"},
        {"q": "OSI 7계층에서 세그먼트(Segment)를 데이터 단위로 사용하는 계층은?", "a": "전송 계층(Transport Layer)", "w": ["네트워크 계층","세션 계층","데이터링크 계층"], "cat": "네트워크"},
        {"q": "스크럼(Scrum)에서 반복 개발 주기를 의미하는 용어는?", "a": "스프린트(Sprint)", "w": ["이터레이션","릴리즈","에픽"], "cat": "소프트웨어공학"},
        {"q": "트랜잭션의 원자성(Atomicity)이란?", "a": "모두 실행되거나 모두 취소되어야 함", "w": ["동시 트랜잭션 간 독립성 보장","완료 후 영구 반영","실행 전후 무결성 유지"], "cat": "데이터베이스"},
        {"q": "객체 생성을 서브클래스에서 결정하도록 위임하는 패턴은?", "a": "팩토리 메서드(Factory Method)", "w": ["싱글톤","어댑터","옵저버"], "cat": "디자인패턴"},
        {"q": "IP 주소 192.168.1.0/24의 서브넷 마스크는?", "a": "255.255.255.0", "w": ["255.255.0.0","255.0.0.0","255.255.255.128"], "cat": "네트워크"},
        {"q": "SQL LEFT OUTER JOIN의 결과로 옳은 설명은?", "a": "왼쪽 테이블 전체 + 오른쪽 매칭값(없으면 NULL)", "w": ["양쪽 매칭 행만 출력","오른쪽 테이블 전체 포함","매칭 안 되는 행은 제외"], "cat": "데이터베이스"},
        {"q": "퀵 정렬(Quick Sort)의 평균 시간 복잡도는?", "a": "O(n log n)", "w": ["O(n²)","O(n)","O(log n)"], "cat": "알고리즘"},
        {"q": "TCP와 UDP의 핵심 차이점은?", "a": "TCP는 연결 지향, UDP는 비연결 지향", "w": ["TCP가 더 빠름","UDP가 신뢰성 보장","둘 다 응용 계층 프로토콜"], "cat": "네트워크"},
        {"q": "REST API에서 리소스 삭제 시 사용하는 HTTP 메서드는?", "a": "DELETE", "w": ["GET","POST","PUT"], "cat": "웹"},
        {"q": "NoSQL의 특징으로 올바른 것은?", "a": "유연한 스키마 + 수평 확장(Scale-out) 용이", "w": ["ACID 반드시 보장","관계형 모델 전용","수직 확장만 가능"], "cat": "데이터베이스"},
        {"q": "페이징(Paging) 기법의 주요 장점은?", "a": "외부 단편화 제거", "w": ["내부 단편화 제거","메모리 접근 속도 향상","TLB 불필요"], "cat": "운영체제"},
        {"q": "Git에서 원격 저장소 변경사항을 로컬에 병합하는 명령어는?", "a": "git pull", "w": ["git push","git fetch","git clone"], "cat": "개발도구"},
        {"q": "해시 테이블의 평균 검색 시간 복잡도는?", "a": "O(1)", "w": ["O(n)","O(log n)","O(n log n)"], "cat": "자료구조"},
        {"q": "프로세스와 스레드의 차이점으로 올바른 것은?", "a": "스레드는 같은 프로세스 내 메모리를 공유", "w": ["프로세스가 더 가벼움","스레드는 독립적인 메모리 공간 가짐","스레드 생성 비용이 더 큼"], "cat": "운영체제"},
        {"q": "대칭키 암호화 방식의 특징은?", "a": "암호화·복호화에 동일한 키 사용, 처리 속도 빠름", "w": ["공개키·개인키 쌍 사용","키 분배가 안전함","전자서명에 주로 사용"], "cat": "보안"},
    ]

    if 'cbt_q' not in st.session_state:
        q    = random.choice(QUESTION_POOL)
        opts = q['w'] + [q['a']]; random.shuffle(opts)
        st.session_state.cbt_q    = q
        st.session_state.cbt_opts = opts

    q       = st.session_state.cbt_q
    cats    = {"데이터베이스":"🗄️","네트워크":"🌐","소프트웨어공학":"⚙️","알고리즘":"🔢","자료구조":"📚","운영체제":"🖥️","디자인패턴":"🎨","웹":"🌍","개발도구":"🛠️","보안":"🔒"}
    cat_ico = cats.get(q.get('cat',''), "📝")

    st.markdown(f"<div style='color:#888;font-size:0.8rem;margin-bottom:8px;'>{cat_ico} {q.get('cat','기타')} 분야</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'><b>Q.</b> {q['q']}</div>", unsafe_allow_html=True)
    st.write("")

    with st.form("cbt_form"):
        answer    = st.radio("정답을 선택하세요:", st.session_state.cbt_opts, key="cbt_radio")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button("✅ 제출", use_container_width=True)
        if submitted:
            if answer == q['a']:
                st.success("🎉 정답입니다!"); st.session_state.global_cash += 500_000
                log_tx(st.session_state.logged_in_user, "CBT", "정처기 정답 보상", 500_000)
                st.balloons(); st.info("💰 보상: +₩500,000")
            else:
                st.error(f"❌ 오답! 정답: {q['a']}")
            del st.session_state.cbt_q, st.session_state.cbt_opts
            sync_user_data(); time.sleep(2.5); st.rerun()

    if st.button("🔄 다른 문제", use_container_width=True):
        for k in ['cbt_q', 'cbt_opts']:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

# ════════════════════════════════════════════════
# 🏎️ 하이퍼카 레이싱
# ════════════════════════════════════════════════
elif menu == "🏎️ 하이퍼카 레이싱":
    st.title("🏎️ 하이퍼카 레이싱")
    st.caption("배당률이 높을수록 우승 확률은 낮지만 당첨 시 고수익!")

    CARS = [
        {"name": "부가티 시론 SS",        "emoji": "🏎️", "odds": 20.0, "spd": (2, 7),   "color": "#FF0066"},
        {"name": "람보르기니 레부엘토",    "emoji": "🐂",  "odds": 12.0, "spd": (3, 10),  "color": "#FF6600"},
        {"name": "페라리 SF90 XX",         "emoji": "🐎",  "odds": 8.0,  "spd": (4, 12),  "color": "#FF2200"},
        {"name": "맥라렌 P1 GTR",          "emoji": "🚀",  "odds": 6.0,  "spd": (5, 13),  "color": "#FF9900"},
        {"name": "포르쉐 918 스파이더",    "emoji": "⚡",  "odds": 4.0,  "spd": (6, 15),  "color": "#FFCC00"},
        {"name": "테슬라 로드스터 2",      "emoji": "⚡",  "odds": 2.5,  "spd": (8, 17),  "color": "#00FF88"},
        {"name": "토요타 GR010 하이브리드","emoji": "🏁",  "odds": 1.8,  "spd": (10, 20), "color": "#00CCFF"},
    ]

    car_names = [f"{c['emoji']} {c['name']} ({c['odds']}배)" for c in CARS]
    sel_idx   = st.selectbox("차량 선택", range(len(CARS)), format_func=lambda i: car_names[i])
    my_car    = CARS[sel_idx]
    bet_amt   = st.number_input("베팅 금액 (원)", min_value=10_000, step=10_000, value=100_000)
    st.caption(f"우승 시 예상 수령액: {format_korean_money(int(bet_amt * my_car['odds']))}")

    cd_race = cooldown_remaining("race_start", 8.0)
    if cd_race > 0:
        st.warning(f"⏱️ 레이스 쿨다운 {cd_race:.1f}초")
    elif st.button("🏁 레이스 시작!", use_container_width=True):
        if st.session_state.global_cash < bet_amt:
            st.error("잔액 부족!")
        else:
            set_cooldown("race_start")
            st.session_state.global_cash -= bet_amt
            positions = {c['name']: 0.0 for c in CARS}
            winner    = None
            bars      = {}
            st.markdown("### 🏁 레이스 진행")
            for c in CARS:
                bars[c['name']] = st.progress(0, text=f"{c['emoji']} {c['name']}")

            while winner is None:
                time.sleep(0.12)
                for c in CARS:
                    positions[c['name']] = min(100, positions[c['name']] + random.randint(c['spd'][0], c['spd'][1]))
                    rank     = sorted(positions.items(), key=lambda x: x[1], reverse=True)
                    pos_num  = next(i+1 for i, (n, _) in enumerate(rank) if n == c['name'])
                    bars[c['name']].progress(positions[c['name']]/100, text=f"{c['emoji']} {c['name']} {pos_num}위 | {positions[c['name']]:.0f}%")
                    if positions[c['name']] >= 100 and winner is None:
                        winner = c['name']

            st.write("---")
            winner_car = next(c for c in CARS if c['name'] == winner)
            st.markdown(f"<div style='text-align:center;font-family:Orbitron,monospace;font-size:1.8rem;color:{winner_car['color']};font-weight:900;padding:20px;'>🏆 {winner_car['emoji']} {winner} 우승!</div>", unsafe_allow_html=True)

            if winner == my_car['name']:
                prize = int(bet_amt * my_car['odds'])
                st.session_state.global_cash += prize
                log_tx(st.session_state.logged_in_user, "레이싱", f"{my_car['name']} 베팅 승리", prize - bet_amt)
                st.success(f"🎉 베팅 성공! +{format_korean_money(prize)}"); st.balloons()
            else:
                log_tx(st.session_state.logged_in_user, "레이싱", f"{my_car['name']} 베팅 패배", -bet_amt)
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")

            sync_user_data(); time.sleep(3); st.rerun()

# ════════════════════════════════════════════════
# 🎰 럭키 슬롯
# ════════════════════════════════════════════════
elif menu == "🎰 럭키 슬롯":
    st.title("🎰 럭키 슬롯")

    SLOT_TIERS = [
        {"label": "🪙 일반 슬롯",  "cost": 1_000_000,   "jackpot": 30_000_000,    "jackpot_mult": 30, "prob": 0.10},
        {"label": "💰 골드 슬롯",  "cost": 10_000_000,  "jackpot": 500_000_000,   "jackpot_mult": 50, "prob": 0.08},
        {"label": "💎 다이아 슬롯","cost": 100_000_000, "jackpot": 5_000_000_000, "jackpot_mult": 50, "prob": 0.06},
    ]
    SYMBOLS = {"🍒": 0.35, "🍋": 0.25, "🔔": 0.18, "⭐": 0.12, "7️⃣": 0.07, "💎": 0.03}

    sel_tier = st.selectbox("슬롯 등급 선택", range(len(SLOT_TIERS)), format_func=lambda i: SLOT_TIERS[i]['label'])
    tier     = SLOT_TIERS[sel_tier]

    st.markdown(f"""
<div class='card' style='text-align:center;'>
  <div style='color:#888;font-size:0.82rem;'>비용: <b style='color:#FFD600;'>{format_korean_money(tier['cost'])}</b> &nbsp;|&nbsp; 잭팟: <b style='color:#FF00FF;'>{format_korean_money(tier['jackpot'])}</b></div>
  <div style='color:#666;font-size:0.78rem;margin-top:4px;'>💎=3개 잭팟, 같은 기호 3개=고배당, 2개=소배당</div>
</div>""", unsafe_allow_html=True)

    slot_display = st.empty()
    slot_display.markdown("<div class='slot-display'>🎰 &nbsp; 🎰 &nbsp; 🎰</div>", unsafe_allow_html=True)

    cd_slot = cooldown_remaining(f"slot_{sel_tier}", 3.0)
    if cd_slot > 0:
        st.warning(f"⏱️ 슬롯 쿨다운 {cd_slot:.1f}초")
    elif st.button(f"🎰 {tier['label']} 당기기! ({format_korean_money(tier['cost'])})", use_container_width=True):
        if st.session_state.global_cash < tier['cost']:
            st.error("잔액 부족!")
        else:
            set_cooldown(f"slot_{sel_tier}")
            st.session_state.global_cash -= tier['cost']
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += tier['cost']
                st.error("거래 취소 (잔액 보호)")
            else:
                syms = list(SYMBOLS.keys()); wts = list(SYMBOLS.values())
                for _ in range(14):
                    r = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                    slot_display.markdown(f"<div class='slot-display'>{r[0]} &nbsp; {r[1]} &nbsp; {r[2]}</div>", unsafe_allow_html=True)
                    time.sleep(0.08)

                final = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                slot_display.markdown(f"<div class='slot-display'>{final[0]} &nbsp; {final[1]} &nbsp; {final[2]}</div>", unsafe_allow_html=True)

                if final[0] == final[1] == final[2] == "💎":
                    prize = tier['jackpot']
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 잭팟!!!", prize)
                    st.success(f"💎💎💎 JACKPOT!!! +{format_korean_money(prize)}"); st.balloons()
                    market['news'] = f"🎊 [슬롯 잭팟] {st.session_state.logged_in_user}님이 {format_korean_money(prize)} 잭팟!!"
                    save_market(market)
                elif final[0] == final[1] == final[2]:
                    prize = int(tier['cost'] * tier['jackpot_mult'] * 0.2)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 트리플", prize)
                    st.success(f"🎉 트리플! +{format_korean_money(prize)}")
                elif final[0]==final[1] or final[1]==final[2] or final[0]==final[2]:
                    prize = int(tier['cost'] * 1.5)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 더블", prize)
                    st.warning(f"✨ 더블 매치! +{format_korean_money(prize)}")
                else:
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 꽝", -tier['cost'])
                    st.error("꽝! 다음 기회를 노려보세요!")

                sync_user_data(); time.sleep(2); st.rerun()

# ════════════════════════════════════════════════
# ⛏️ 광산
# ════════════════════════════════════════════════
elif menu == "⛏️ 광산 (노가다)":
    st.title("⛏️ 효민 광산")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>곡괭이를 들어 광물을 캐세요!</div>", unsafe_allow_html=True)

    cash = st.session_state.global_cash
    if cash < 10_000_000:
        mine_tier, mine_label, mine_color = 0, "🪨 초보 광산",  "#888"
    elif cash < 100_000_000:
        mine_tier, mine_label, mine_color = 1, "⛏️ 견습 광산",  "#CD7F32"
    elif cash < 1_000_000_000:
        mine_tier, mine_label, mine_color = 2, "🥈 숙련 광산",  "#C0C0C0"
    else:
        mine_tier, mine_label, mine_color = 3, "🥇 마스터 광산","#FFD600"

    tier_bonus = mine_tier * 0.005

    st.markdown(f"""
<div class='mine-card'>
  <div style='font-size:2rem;margin-bottom:8px;'>⛏️</div>
  <div style='font-size:1.2rem;font-weight:900;color:{mine_color};'>{mine_label}</div>
  <div style='color:#888;font-size:0.82rem;margin-top:6px;'>광산 티어가 높을수록 희귀 광물 확률 ↑</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📋 광물 목록")
    rows_html = "<table class='stock-table'><thead><tr><th>광물</th><th style='text-align:right;'>가치</th><th style='text-align:right;'>기본 확률</th></tr></thead><tbody>"
    for item in MINE_ITEMS:
        adj_prob = min(item['prob'] + tier_bonus, 0.99)
        rows_html += f"<tr><td>{item['icon']} {item['name']}</td><td style='text-align:right;color:#FFD600;font-weight:900;'>{format_korean_money(item['value'])}</td><td style='text-align:right;color:#888;'>{adj_prob*100:.1f}%</td></tr>"
    rows_html += "</tbody></table>"
    st.markdown(rows_html, unsafe_allow_html=True)
    st.write("")

    def do_mine(k):
        items_adj   = []
        weights_adj = []
        for item in MINE_ITEMS:
            items_adj.append(item)
            weights_adj.append(item['prob'] + tier_bonus)
        return random.choices(items_adj, weights=weights_adj, k=k)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        cd_mine1 = cooldown_remaining("mine_single", 1.5)
        if cd_mine1 > 0:
            st.warning(f"⏱️ 쿨다운 {cd_mine1:.1f}초")
        elif st.button("⛏️ 한 번 캐기!", use_container_width=True):
            set_cooldown("mine_single")
            result = do_mine(1)[0]
            st.session_state.global_cash += result['value']
            log_tx(st.session_state.logged_in_user, "광산", f"{result['name']} 채굴", result['value'])
            sync_user_data()
            if result['name'] in ["다이아몬드", "전설의 원석"]:
                st.balloons()
                st.success(f"✨ {result['icon']} **{result['name']}** 발견!! +{format_korean_money(result['value'])}")
                market['news'] = f"⛏️ [{st.session_state.logged_in_user}] 광산에서 {result['name']} 채굴 대박!"
                save_market(market)
            elif result['name'] in ["루비", "사파이어"]:
                st.success(f"🎉 {result['icon']} {result['name']} 발견! +{format_korean_money(result['value'])}")
            else:
                st.info(f"{result['icon']} {result['name']} 채굴. +{format_korean_money(result['value'])}")

    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        cd_mine10 = cooldown_remaining("mine_ten", 4.0)
        if cd_mine10 > 0:
            st.warning(f"⏱️ 10연속 쿨다운 {cd_mine10:.1f}초")
        elif st.button("⛏️⛏️ 10회 연속 채굴", use_container_width=True):
            set_cooldown("mine_ten")
            results = do_mine(10)
            total   = sum(r['value'] for r in results)
            st.session_state.global_cash += total
            log_tx(st.session_state.logged_in_user, "광산", "10회 연속 채굴", total)
            sync_user_data()
            summary = {}
            for r in results:
                summary[r['name']] = summary.get(r['name'], 0) + 1
            result_str = " | ".join(
                f"{next(m['icon'] for m in MINE_ITEMS if m['name']==n)} {n} x{cnt}"
                for n, cnt in summary.items()
            )
            st.success(f"⛏️ 10회 채굴 완료! +{format_korean_money(total)}\n{result_str}")

# ════════════════════════════════════════════════
# 👑 칭호 상점
# ════════════════════════════════════════════════
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    st.markdown("칭호를 구매하고 장착하여 게시판에서 부를 과시하세요!")

    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i % 2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id   = f"title_{i}"
            price      = i * 10_000_000

            st.markdown(f"**{title_name}** | {format_korean_money(price)}")

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
                        if st.session_state.global_cash < 0:
                            st.session_state.global_cash += price
                            st.error("거래 취소 (잔액 보호)")
                        else:
                            st.session_state.inventory.append(title_id)
                            st.session_state.equipped_title = title_name
                            log_tx(st.session_state.logged_in_user, "칭호구매", f"{title_name} 구매", -price)
                            sync_user_data(); st.rerun()
                    else:
                        st.error("잔액이 부족합니다.")

# ════════════════════════════════════════════════
# 📜 내 거래 기록
# ════════════════════════════════════════════════
elif menu == "📜 내 거래 기록":
    st.title("📜 내 거래 기록")
    st.caption("모든 자산 변동 내역을 확인할 수 있습니다. (최근 200건)")

    uid_log  = st.session_state.logged_in_user
    logs = load_db(TXLOG_FILE, {})
    my_logs = logs.get(uid_log, [])

    if not my_logs:
        st.info("아직 거래 기록이 없습니다.")
    else:
        cats_all = sorted(set(l['category'] for l in my_logs))
        sel_cat  = st.selectbox("카테고리 필터", ["전체"] + cats_all)

        filtered = my_logs if sel_cat == "전체" else [l for l in my_logs if l['category'] == sel_cat]

        total_in  = sum(l['amount'] for l in filtered if l['amount'] > 0)
        total_out = sum(l['amount'] for l in filtered if l['amount'] < 0)

        c1, c2, c3 = st.columns(3)
        c1.metric("📈 총 수입", format_korean_money(total_in))
        c2.metric("📉 총 지출", format_korean_money(abs(total_out)))
        c3.metric("💰 순손익",  format_korean_money(total_in + total_out))

        st.write("")

        for log in filtered[:100]:
            amt   = log['amount']
            color = "#FF4B4B" if amt > 0 else "#4B9EFF"
            arrow = "▲" if amt > 0 else "▼"
            sign  = "+" if amt > 0 else ""
            cat_icons = {
                "주식매수":"📉","주식매도":"📈","부동산매입":"🏗️","부동산구매":"🛒",
                "부동산판매":"🏷️","부동산수금":"💰","송금":"📤","대출":"💳","대출상환":"🏦",
                "로또":"🎫","축구베팅":"⚽","레이싱":"🏎️","슬롯":"🎰",
                "광산":"⛏️","CBT":"💻","칭호구매":"👑","VIP슬롯":"💎",
            }
            cat_ico = cat_icons.get(log['category'], "📋")
            st.markdown(f"""
<div class='tx-row'>
  <span style='color:#555;min-width:110px;'>{log['time']}</span>
  <span style='color:#888;min-width:60px;'>{cat_ico} {log['category']}</span>
  <span style='color:#ddd;flex:1;margin:0 12px;'>{log['desc']}</span>
  <span style='color:{color};font-weight:900;'>{arrow} {sign}{format_korean_money(abs(amt))}</span>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 🏅 랭킹 & 게시판
# ════════════════════════════════════════════════
elif menu == "🏅 랭킹 & 게시판":
    st.title("🏅 랭킹 & 게시판")

    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 게시판"])

    with tab_rank:
        users_all = load_db(USERS_FILE, {})
        rank_data = []
        for uid_r, udata in users_all.items():
            if uid_r == "5891": continue
            w = udata.get('cash', 0) - udata.get('loan', 0)
            for sid, p in udata.get('portfolio', {}).items():
                if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
            for eid, cnt in udata.get('real_estate', {}).items():
                if eid in estate_config: w += estate_config[eid]['base_price'] * cnt * 0.8
            rank_data.append({"uid": uid_r, "title": udata.get('equipped_title','🌱 신규시민'), "nw": w})
        rank_data.sort(key=lambda x: x['nw'], reverse=True)

        medals = ["🥇","🥈","🥉"] + [f"{i}위" for i in range(4, 101)]
        for i, r in enumerate(rank_data[:20]):
            me       = "🫵" if r['uid'] == st.session_state.logged_in_user else ""
            nw_color = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
            st.markdown(f"""
<div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 18px;margin:4px 0;'>
  <span style='font-size:1.1rem;min-width:36px;'>{medals[i]}</span>
  <span style='font-weight:900;color:#E8E8F0;flex:1;margin:0 10px;'>{r['uid']} {me}</span>
  <span style='color:#888;font-size:0.82rem;flex:1;'>{r['title']}</span>
  <span style='font-weight:900;color:{nw_color};'>{format_korean_money(r['nw'])}</span>
</div>""", unsafe_allow_html=True)

    with tab_board:
        msg = st.text_input("메시지 작성", placeholder="랭커 게시판에 글을 남겨보세요!")
        cd_post = cooldown_remaining("board_post", 5.0)
        if cd_post > 0:
            st.warning(f"⏱️ 도배 방지 쿨다운 {cd_post:.1f}초")
        elif st.button("📝 등록", use_container_width=True):
            if msg.strip():
                set_cooldown("board_post")
                comments = load_db(COMMENTS_FILE, [])
                comments.append({
                    "name":    st.session_state.logged_in_user,
                    "title":   st.session_state.equipped_title,
                    "comment": msg.strip(),
                    "time":    datetime.now().strftime("%m/%d %H:%M")
                })
                save_db(COMMENTS_FILE, comments)
                st.rerun()

        st.write("")
        all_c = load_db(COMMENTS_FILE, [])
        for c in reversed(all_c[-50:]):
            st.markdown(f"""
<div class='card' style='margin:6px 0;padding:12px 16px;'>
  <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
    <span><b style='color:#00E5FF;'>{c['name']}</b> <span style='color:#FFD600;font-size:0.82rem;'>{c.get('title','')}</span></span>
    <span style='color:#555;font-size:0.78rem;'>{c.get('time','')}</span>
  </div>
  <div style='color:#ddd;font-size:0.92rem;'>{c['comment']}</div>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# 🛠️ 창조주 통제소
# ════════════════════════════════════════════════
elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 창조주 통제소")
    st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;'>⚠️ 창조주 전용 패널</div>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.tabs(["👤 유저 조작", "📈 시장 조작", "📢 공지 & 이벤트", "📊 전체 현황", "🏢 부동산 관리"])

    with t1:
        def parse_creator_money(text):
            if not text: return None
            text = text.replace(',', '').replace(' ', '').strip()
            if text.isdigit(): return int(text)
            units = {"조": 10**12, "억": 10**8, "만": 10**4}
            total = 0
            import re
            matches = re.findall(r'([0-9.]+)([조억만]?)', text)
            if not matches:
                try:
                    clean_num = re.sub(r'[^0-9.]', '', text)
                    return int(float(clean_num)) if clean_num else None
                except: return None
            for val, unit in matches:
                total += float(val) * units.get(unit, 1)
            return int(total)

        u_db = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "5891"]

        if uid_list:
            sel_u  = st.selectbox("조작할 유저 선택", uid_list)
            u_data = u_db[sel_u]

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 💰 자산 개조")
                raw_cash = st.text_input("현금 설정 (예: 1000억, 1.5조)", placeholder="비워두면 유지", key="admin_cash_input")
                raw_loan = st.text_input("대출 설정 (예: 5000만)", placeholder="비워두면 유지", key="admin_loan_input")
                parsed_cash = parse_creator_money(raw_cash)
                parsed_loan = parse_creator_money(raw_loan)
                final_cash = parsed_cash if parsed_cash is not None else int(u_data.get('cash', 0))
                final_loan = parsed_loan if parsed_loan is not None else int(u_data.get('loan', 0))
                st.markdown(f"""
<div style='background:rgba(0,229,255,0.1);padding:15px;border-radius:10px;border:1px solid #00E5FF;margin-top:10px;'>
  <div style='color:#00E5FF;font-size:0.8rem;'>▼ 적용 예정 금액</div>
  <div style='font-size:1.1rem;margin-top:5px;'>
    <b>현금:</b> {format_korean_money(final_cash)}<br>
    <b>대출:</b> {format_korean_money(final_loan)}
  </div>
</div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("##### 👑 신분 개조")
                new_title = st.text_input("칭호 수정", value=u_data.get('equipped_title',''), key="admin_title_input")
                st.write("")
                st.metric("현재 현금", format_korean_money(u_data.get('cash', 0)))
                st.metric("현재 대출", format_korean_money(u_data.get('loan', 0)))

            if st.button("🔥 유저 데이터 강제 개조 실행", use_container_width=True):
                u_db[sel_u]['cash'] = final_cash
                u_db[sel_u]['loan'] = final_loan
                u_db[sel_u]['equipped_title'] = new_title
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 유저 자산 개조 완료!")
                time.sleep(1); st.rerun()

            st.write("---")
            if st.button("🗑️ 해당 유저 삭제", use_container_width=True, type="secondary"):
                if sel_u in u_db:
                    del u_db[sel_u]
                    save_db(USERS_FILE, u_db)
                    st.rerun()
        else:
            st.info("관리할 유저가 없습니다.")

    with t2:
        st.markdown("### 📈 종목별 가격 조작")
        for s in stock_config:
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"{s['icon']} {s['name']}")
            c2.write(f"현재: ₩{market['stock_data'][s['id']]['price']:,}")
            if c3.button("🚀 +50%", key=f"up_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = f"🚀 [시장조작] {s['name']} 급등!"; save_market(market); st.rerun()
            if c4.button("📉 -30%", key=f"dn_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 0.7)
                market['news'] = f"💣 [시장조작] {s['name']} 폭락!"; save_market(market); st.rerun()

        st.write("---")
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔥 전종목 +50% 폭등", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = "🔥 [창조주의 축복] 전 종목 폭등!!!"; save_market(market); st.rerun()
        with cb:
            if st.button("💣 전종목 -40% 폭락", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = max(1000, int(market['stock_data'][s['id']]['price'] * 0.6))
                market['news'] = "💣 [창조주의 심판] 전 종목 폭락!!!"; save_market(market); st.rerun()

    with t3:
        st.markdown("### 📢 공지사항")
        msg_text  = st.text_area("공지 내용", value=market.get('admin_msg', ''), height=100)
        msg_color = st.color_picker("텍스트 색상", value=market.get('admin_color', '#FF4B4B'))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📣 공지 발령", use_container_width=True):
                market['admin_msg'] = msg_text; market['admin_color'] = msg_color; save_market(market); st.success("공지 발령 완료!")
        with c2:
            if st.button("🗑️ 공지 삭제", use_container_width=True):
                market['admin_msg'] = ""; save_market(market); st.success("공지 삭제 완료!")

    with t4:
        st.markdown("### 📊 전체 유저 현황")
        u_db2 = load_db(USERS_FILE, {})
        rows = [{"ID": uid_r, "칭호": ud.get('equipped_title',''), "현금": format_korean_money(ud.get('cash',0)), "대출": format_korean_money(ud.get('loan',0))} for uid_r, ud in u_db2.items() if uid_r != "5891"]
        if rows: st.table(pd.DataFrame(rows))
        else: st.info("등록된 유저 없음")

        st.write("---")
        st.markdown("### 💾 데이터 백업 상태")
        for f in [USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE, REALESTATE_MARKET_FILE]:
            exists = "✅" if os.path.exists(f) else "❌"
            size = f"{os.path.getsize(f):,} bytes" if os.path.exists(f) else "—"
            st.markdown(f"<div style='color:#aaa;font-size:0.85rem;'>{exists} <b>{f}</b> ({size})</div>", unsafe_allow_html=True)

        if st.button("🗑️ 게시판 전체 삭제"):
            save_db(COMMENTS_FILE, []); st.success("게시판 초기화 완료!")

    with t5:
        st.markdown("### 🏢 부동산 마켓 관리")
        em_admin = load_estate_market()

        st.markdown("#### 현재 유저 매물 현황")
        if em_admin["listings"]:
            for li in em_admin["listings"]:
                info = estate_config.get(li["eid"], {})
                c1, c2 = st.columns([5, 1])
                with c1:
                    st.markdown(f"**{info.get('icon','')} {info.get('name','?')}** — 판매자: `{li['seller']}` — {format_korean_money(li['price'])}")
                with c2:
                    if st.button("강제삭제", key=f"admin_del_{li['id']}"):
                        em_admin["listings"] = [x for x in em_admin["listings"] if x["id"] != li["id"]]
                        save_estate_market(em_admin)
                        st.rerun()
        else:
            st.info("등록된 유저 매물 없음")

        st.write("---")
        st.markdown("#### 소유 현황 (owner_counts)")
        if em_admin["owner_counts"]:
            for uid_o, eids in em_admin["owner_counts"].items():
                owned_str = ", ".join(f"{estate_config.get(e,{}).get('name','?')} x{cnt}" for e, cnt in eids.items() if cnt > 0)
                if owned_str:
                    st.markdown(f"<div style='color:#aaa;font-size:0.85rem;'><b style='color:#00E5FF;'>{uid_o}</b>: {owned_str}</div>", unsafe_allow_html=True)

        if st.button("🔄 부동산 마켓 전체 초기화", type="secondary"):
            save_estate_market({"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}})
            st.success("부동산 마켓 초기화 완료!")
            st.rerun()
