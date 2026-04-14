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
import uuid
from datetime import datetime, timedelta, timezone
from filelock import FileLock

def _get_lock(filepath: str) -> FileLock:
    return FileLock(filepath + ".lock", timeout=5)
import hashlib

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

ADMIN_PW = "***"



# ==============================
# 🕒 서버 시간 강제 세팅 (KST)
# ==============================
os.environ['TZ'] = 'Asia/Seoul'
try: time.tzset()
except AttributeError: pass
KST = timezone(timedelta(hours=9))

# ==============================
# 🌌 시스템 설정 및 데이터베이스
# ==============================
USERS_FILE    = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE   = "market_db.json"
TXLOG_FILE    = "txlog_db.json"
REALESTATE_MARKET_FILE = "realestate_market_db.json"  
CLAN_FILE = "clan_db.json"

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

estate_config = {
    "E1":  {"name": "역세권 원룸",          "icon": "🏠",  "base_price": 10_000_000_000,    "income": 8_000,     "desc": "지하철 2분 거리 황금 입지",          "total_supply": 20},
    "E2":  {"name": "초대형 PC방",           "icon": "🖥️",  "base_price": 50_000_000_000,    "income": 45_000,    "desc": "e스포츠 성지, 24시간 풀가동",        "total_supply": 10},
    "E3":  {"name": "강남 꼬마빌딩",         "icon": "🏢",  "base_price": 500_000_000_000,   "income": 450_000,   "desc": "강남 핵심 상권 4층 빌딩",             "total_supply": 6},
    "E4":  {"name": "시그니엘 펜트하우스",   "icon": "👑",  "base_price": 5_000_000_000_000, "income": 4_500_000, "desc": "롯데월드타워 최상층 전망",            "total_supply": 3},
    "E5":  {"name": "제주 풀빌라",           "icon": "🌴",  "base_price": 30_000_000_000,    "income": 25_000,    "desc": "성산일출봉 전망 프리미엄 풀빌라",    "total_supply": 8},
    "E6":  {"name": "홍대 상가건물",         "icon": "🎸",  "base_price": 200_000_000_000,   "income": 180_000,   "desc": "홍대 메인 스트리트 5층 상가",        "total_supply": 8},
    "E7":  {"name": "판교 오피스타워",       "icon": "💻",  "base_price": 800_000_000_000,   "income": 750_000,   "desc": "IT 기업 밀집 A급 오피스",             "total_supply": 8},
    "E8":  {"name": "해운대 호텔",           "icon": "🏖️",  "base_price": 2_000_000_000_000, "income": 2_000_000, "desc": "부산 해운대 특급 호텔 1동",          "total_supply": 20},
    "E9":  {"name": "용산 임대아파트 단지",  "icon": "🏘️",  "base_price": 1_000_000_000_000, "income": 900_000,   "desc": "용산 재개발 신축 100세대 단지",      "total_supply": 10},
    "E10": {"name": "인천공항 면세점",       "icon": "✈️",  "base_price": 3_000_000_000_000, "income": 3_500_000, "desc": "인천공항 1터미널 황금 면세점",       "total_supply": 5},
}

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

CRYPTO_CONFIG = [
    {"id": "BTC",   "name": "비트코인",  "vol": 0.12, "icon": "₿",  "base_price": 130_000_000},
    {"id": "ETH",   "name": "이더리움",  "vol": 0.10, "icon": "Ξ",  "base_price": 6_000_000},
    {"id": "SOL",   "name": "솔라나",    "vol": 0.15, "icon": "◎",  "base_price": 300_000},
    {"id": "DOGE",  "name": "도지코인",  "vol": 0.22, "icon": "🐶", "base_price": 500},
    {"id": "PEPE",  "name": "페페코인",  "vol": 0.35, "icon": "🐸", "base_price": 10},
    {"id": "HYO",   "name": "효민코인",  "vol": 0.28, "icon": "🌌", "base_price": 1_000_000},
]
# ── 🎴 가챠 설정 ──
GACHA_POOL = [
    # ── 💎 전설 ──
    {"grade": "💎 전설", "name": "👑 [시즌한정] 우주의 도박꾼",        "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 운영자를 노린다",        "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 갓생러",                "weight": 2,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 전설",    "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 돈복사 의혹자",         "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 서버 경제 붕괴자",       "weight": 1,  "type": "title"},
    # ── 🔴 영웅 ──
    {"grade": "🔴 영웅", "name": "⚔️ 전장의 지배자",                   "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 억만장자의 품격",                  "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 코인왕",                          "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 부동산 재벌",                     "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 주식의 신",                       "weight": 4,  "type": "title"},
    # ── 🔵 희귀 ──
    {"grade": "🔵 희귀", "name": "🎖️ 행운의 사나이",                   "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 억세게 운 좋은 놈",               "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 가챠 중독자",                     "weight": 10, "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 슬롯머신 애호가",                 "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 광산의 제왕",                     "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 레이싱 황제",                     "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 블랙잭 고수",                     "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 로또 상습 구매자",                "weight": 8,  "type": "title"},
    # ── 🟢 일반 ──
    {"grade": "🟢 일반", "name": "🍀 행운의 클로버",                   "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🌟 떠오르는 별",                     "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "💫 시민 모험가",                     "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🌈 평범한 시민",                     "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🐣 뉴비",                           "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🦆 그냥 오리",                       "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🍞 평범한 빵",                       "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🐌 느릿느릿 투자자",                  "weight": 25, "type": "title"},
    # ── 🟤 꽝 ──
    {"grade": "🟤 꽝",   "name": "파괴방지권",                          "weight": 30, "type": "item"},
    {"grade": "🟤 꽝",   "name": "빈 깡통",                             "weight": 30, "type": "item"},
]

GACHA_TICKET_PRICE = 50_000_000

DAILY_QUESTS_CONFIG = [
    {"id": "attendance", "icon": "📅", "name": "출석 체크",       "desc": "오늘 로그인 완료",                   "reward": 10_000_000},
    {"id": "rich5",      "icon": "💰", "name": "중산층 인증",      "desc": "순자산 5억 이상 달성",               "reward": 30_000_000},
    {"id": "landlord",   "icon": "🏠", "name": "건물주 인증",      "desc": "부동산 1채 이상 보유",               "reward": 20_000_000},
    {"id": "investor",   "icon": "📈", "name": "포트폴리오 투자자", "desc": "주식 평가액 1억 이상 보유",          "reward": 25_000_000},
    {"id": "coin100m",   "icon": "🪙", "name": "코인 홀더",        "desc": "코인 총 평가액 1억 이상 보유",       "reward": 20_000_000},
    {"id": "debtfree",   "icon": "🕊️", "name": "무대출 청렴인증",  "desc": "대출 잔액 0원 유지",                 "reward": 15_000_000},
    {"id": "billionaire","icon": "👑", "name": "억만장자 인증",     "desc": "순자산 1000억 이상 달성",            "reward": 500_000_000},
]

# ── 🗡️ 전설의 명검 강화 확률 및 설정 ──
FORGE_DATA = {
    0: {"rate": 1.0,  "cost": 10_000_000,    "sell": 0, "name": "🪵 평범한 나무검", "color": "#aaa"},
    1: {"rate": 1.0,  "cost": 20_000_000,    "sell": 5_000_000, "name": "🗡️ 강철 장검 +1", "color": "#ddd"},
    2: {"rate": 0.95, "cost": 50_000_000,    "sell": 20_000_000, "name": "🗡️ 강철 장검 +2", "color": "#ddd"},
    3: {"rate": 0.90, "cost": 100_000_000,   "sell": 100_000_000, "name": "🗡️ 강철 장검 +3", "color": "#ddd"},
    4: {"rate": 0.85, "cost": 300_000_000,   "sell": 300_000_000, "name": "🗡️ 정예 기사의 검 +4", "color": "#00E5FF"},
    5: {"rate": 0.70, "cost": 1_000_000_000,  "sell": 1_500_000_000, "name": "⚔️ 은빛 대검 +5", "color": "#00FF88"},
    6: {"rate": 0.65, "cost": 3_000_000_000,  "sell": 5_000_000_000, "name": "⚔️ 은빛 대검 +6", "color": "#00FF88"},
    7: {"rate": 0.55, "cost": 8_000_000_000,  "sell": 15_000_000_000, "name": "🔥 타오르는 흑염검 +7", "color": "#FF8800"},
    8: {"rate": 0.50, "cost": 20_000_000_000, "sell": 40_000_000_000, "name": "🔥 타오르는 흑염검 +8", "color": "#FF8800"},
    9: {"rate": 0.45, "cost": 50_000_000_000, "sell": 150_000_000_000, "name": "🩸 마왕의 재림 +9", "color": "#FF4B4B"},
    10: {"rate": 0.20, "cost": 100_000_000_000, "sell": 500_000_000_000, "name": "⚡ 영웅의 성검 +10", "color": "#FFD600"},
    11: {"rate": 0.1, "cost": 300_000_000_000, "sell": 1_500_000_000_000, "name": "⚡ 영웅의 성검 +11", "color": "#FFD600"},
    12: {"rate": 0.05, "cost": 800_000_000_000, "sell": 5_000_000_000_000, "name": "🌌 우주의 지배자 +12", "color": "#FF00FF"},
    13: {"rate": 0.02, "cost": 2_000_000_000_000, "sell": 20_000_000_000_000, "name": "🌌 우주의 지배자 +13", "color": "#FF00FF"},
    14: {"rate": 0.005, "cost": 5_000_000_000_000, "sell": 100_000_000_000_000, "name": "🌌 우주의 지배자 +14", "color": "#FF00FF"},
    15: {"rate": 0.00001, "cost": 0, "sell": 500_000_000_000_000, "name": "👑 [신화] 엑스칼리버 +15", "color": "#FFFFFF"}
}

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
# 🗄️ DB 유틸 (동시성 에러 완벽 방어)
# ════════════════════════════════════
def _atomic_save(filepath: str, data):
    unique_id = str(uuid.uuid4())[:8]
    tmp = f"{filepath}.{unique_id}.tmp"
    bak = f"{filepath}.bak"
    
    lock = _get_lock(filepath)
    try:
        with lock:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            if os.path.exists(filepath):
                shutil.copy2(filepath, bak)
            os.replace(tmp, filepath)
    except Exception as e:
        if os.path.exists(tmp):
            try: os.remove(tmp)
            except: pass
        raise e
        
def load_db(file, default):
    lock = _get_lock(file)
    with lock:
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

def log_tx(uid: str, category: str, desc: str, amount: int):
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs: logs[uid] = []
    logs[uid].insert(0, {
        "time": datetime.now(KST).strftime("%m/%d %H:%M:%S"),
        "category": category,
        "desc": desc,
        "amount": amount,
    })
    logs[uid] = logs[uid][:200]
    save_db(TXLOG_FILE, logs)

def load_estate_market():
    default = {"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}}
    d = load_db(REALESTATE_MARKET_FILE, default)
    if "initial_stock" not in d: d["initial_stock"] = {eid: info["total_supply"] for eid, info in estate_config.items()}
    if "owner_counts" not in d: d["owner_counts"] = {}
    if "listings" not in d: d["listings"] = []
    return d

def save_estate_market(data):
    save_db(REALESTATE_MARKET_FILE, data)

def get_estate_initial_listings(em):
    result = []
    for eid, info in estate_config.items():
        owned_total = sum(v.get(eid, 0) for v in em["owner_counts"].values())
        listed_count = sum(1 for l in em["listings"] if l["eid"] == eid)
        initial_released = owned_total + listed_count
        
        
        current_limit = em.get("initial_stock", {}).get(eid, info["total_supply"])
        remaining_initial = max(0, current_limit - initial_released)
        
        if remaining_initial > 0:
            result.append({"eid": eid, "remaining": remaining_initial, "price": info["base_price"], "is_initial": True})
    return result

def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return 0
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices: w += p_data.get('qty', 0) * prices[sid]
    if 'crypto_data' in market_data:
        for cid, cinfo in u.get('crypto_portfolio', {}).items():
            if cid in market_data['crypto_data']:
                w += cinfo.get('qty', 0) * market_data['crypto_data'][cid]['price']
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
    w_lv = u.get('weapon_level', 0)
    if w_lv > 0:
        w += FORGE_DATA[w_lv]['sell']
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
        'crypto_portfolio': st.session_state.get('crypto_portfolio', {}),
        'daily_quests':     st.session_state.get('daily_quests', {}),
        'weapon_level':   st.session_state.get('weapon_level', 0), 
        'bulk_trade_date':  st.session_state.get('bulk_trade_date', ''),
        'bulk_trade_count': st.session_state.get('bulk_trade_count', 0),
        'last_estate_reset': st.session_state.get('last_estate_reset', 0),
    })
    save_db(USERS_FILE, users)

def get_market():
    def init_m():
        return {
            "version": 6,
            "stock_data": {
                s['id']: {"name": s['name'], "icon": s['icon'],
                          "price": random.randint(50_000, 150_000), "history": [80_000, 80_000]}
                for s in stock_config
            },
            "news": "🌌 HYOMIN UNIVERSE v18.2 오픈!",
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
        # ✅ 수정: 로또 관련 값만 백업 후 복원
        lp = d.get("lotto_pool",      5_000_000_000)
        lt = d.get("lotto_tickets",   {})
        ll = d.get("lotto_last_draw", time.time())
        d  = init_m()
        d["lotto_pool"]      = lp
        d["lotto_tickets"]   = lt
        d["lotto_last_draw"] = ll
        save_db(MARKET_FILE, d); return d
    return d

def save_market(data): save_db(MARKET_FILE, data)
# ════════════════════════════════════
# 🏰 클랜 유틸
# ════════════════════════════════════
def load_clan_db():
    return load_db(CLAN_FILE, {})

def save_clan_db(data):
    save_db(CLAN_FILE, data)

def get_user_clan(uid):
    clans = load_clan_db()
    for cname, cdata in clans.items():
        if uid in cdata.get('members', []):
            return cname
    return None

def get_clan_total_nw(cname, market_data):
    clans = load_clan_db()
    if cname not in clans:
        return 0
    total = clans[cname].get('bank', 0)
    for uid in clans[cname].get('members', []):
        total += get_net_worth(uid, market_data)
    return total
def claim_hidden_title(title_id, title_name):
    uid = st.session_state.logged_in_user
    market = get_market()
    
    # 히든 칭호 발급 기록 DB 초기화
    if "hidden_titles" not in market:
        market["hidden_titles"] = {}
        
    # 아직 아무도 이 칭호를 먹지 않았다면?
    if title_id not in market["hidden_titles"]:
        market["hidden_titles"][title_id] = uid
        
        # 1. 유저 인벤토리에 추가하고 즉시 장착
        us = load_db(USERS_FILE, {})
        if uid in us:
            if title_name not in us[uid].get('inventory', []):
                us[uid].setdefault('inventory', []).append(title_name)
            us[uid]['equipped_title'] = title_name
            save_db(USERS_FILE, us)
        
        # 2. 현재 세션 즉시 업데이트
        st.session_state.equipped_title = title_name
        if title_name not in st.session_state.inventory:
            st.session_state.inventory.append(title_name)
            
        # 3. 글로벌 뉴스 전파 (모두가 보게 만듦)
        market['news'] = f"👑 [서버 최초 달성] {uid}님이 전설적인 칭호 '{title_name}'을(를) 거머쥐었습니다!!"
        save_market(market)
        
        st.toast(f"🎉 서버 최초! [{title_name}] 칭호를 획득했습니다!", icon="👑")
        st.balloons()
        return True
    return False

def set_cooldown(key: str):
    st.session_state[f"_cd_{key}"] = time.time()

def cooldown_remaining(key: str, cooldown_sec: float = 2.0) -> float:
    last = st.session_state.get(f"_cd_{key}", 0)
    return max(0.0, cooldown_sec - (time.time() - last))

st.set_page_config(
    page_title="HYOMIN UNIVERSE v18.2", 
    page_icon="🌌", 
    layout="wide",
    initial_sidebar_state="collapsed"  # 처음 접속 시 사이드바 접어두기
)

# ==============================
# 🎨 전역 CSS 적용 (위치 최상단으로 이동!)
# ==============================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

* { box-sizing: border-box; }

/* 기본 텍스트 색상 강제 흰색 */
html, body, p, span, div, td, th {
  font-family: 'Noto Sans KR', -apple-system, sans-serif !important;
  color: #FFFFFF !important; 
}

/* 🚨 로그인 화면 텍스트(접속환경, 아이디, 비밀번호 등) 강제 흰색 처리 */
label,
label p,
label div,
.stRadio label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] div {
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}

/* 프리미엄 다크 스페이스 배경 */
.stApp {
  background-color: #080A12 !important;
  background-image: 
    radial-gradient(circle at 15% 30%, rgba(0, 229, 255, 0.05), transparent 30%),
    radial-gradient(circle at 85% 70%, rgba(255, 0, 200, 0.05), transparent 30%) !important;
  background-attachment: fixed;
}

[data-testid='stSidebar'] {
  background: rgba(10, 12, 20, 0.95) !important;
  border-right: 1px solid rgba(0, 229, 255, 0.15) !important;
}

h1 { font-family:'Orbitron', sans-serif !important; font-size: 1.8rem !important; font-weight: 900 !important; color: #FFF !important; text-shadow: 0 0 10px rgba(0,229,255,0.3); }
h2 { font-size: 1.3rem !important; font-weight: 800 !important; color: #00FF88 !important; }
h3 { font-size: 1.1rem !important; font-weight: 800 !important; color: #FFD600 !important; }

/* 입력창 네온 스타일 */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: rgba(0, 0, 0, 0.5) !important;
  border: 1px solid rgba(0, 229, 255, 0.3) !important;
  border-radius: 8px !important;
  color: #FFF !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: #00E5FF !important;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3) !important;
}

/* 드롭다운 및 팝업 스타일 */
div[data-baseweb="select"] > div { background-color: #FFFFFF !important; }
div[data-baseweb="select"] * { color: #000000 !important; font-weight: 600 !important; }
[data-baseweb="popover"] { background-color: #FFFFFF !important; }
[data-baseweb="popover"] *, [role="listbox"] *, [data-baseweb="menu"] * { color: #000000 !important; background-color: #FFFFFF !important; }
[role="option"]:hover, [data-baseweb="menu"] li:hover { background-color: #EEEEEE !important; }
div[data-baseweb="select"] div[aria-hidden="true"] { color: #666666 !important; }

/* 사이버펑크 버튼 스타일 */
.stButton > button {
  font-family: 'Noto Sans KR', sans-serif !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  border: 1px solid rgba(0, 229, 255, 0.4) !important;
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.05), rgba(0, 102, 255, 0.1)) !important;
  color: #00E5FF !important;
  transition: all 0.2s ease !important;
  font-size: 0.95rem !important;
  height: 46px !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #00E5FF, #0066FF) !important;
  border-color: #00E5FF !important;
  color: #000 !important;
  box-shadow: 0 4px 15px rgba(0, 229, 255, 0.4) !important;
  transform: translateY(-2px);
}
.stButton > button:disabled { opacity: 0.3 !important; cursor: not-allowed !important; transform: none !important; box-shadow: none !important; border-color: rgba(255,255,255,0.1) !important; color: #888 !important; }

/* 탭 스타일 */
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid rgba(255,255,255,0.1) !important; }
.stTabs [data-baseweb="tab"] { color: #A0AEC0 !important; font-weight: 700 !important; font-size: 0.95rem !important; }
.stTabs [aria-selected="true"] { color: #00E5FF !important; border-bottom: 2px solid #00E5FF !important; text-shadow: 0 0 10px rgba(0,229,255,0.3); }

/* 매트릭 (자산 요약 등) */
[data-testid="stMetric"] {
  background: rgba(255, 255, 255, 0.03) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 12px !important;
  padding: 16px 20px !important;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
}
[data-testid="stMetricLabel"] { color: #888 !important; font-size: 0.85rem !important; font-weight: 700; }
[data-testid="stMetricValue"] { color: #FFF !important; font-family: 'Orbitron', sans-serif !important; font-size: 1.4rem !important; font-weight: 900 !important; }

/* 공통 카드 (글래스모피즘) */
.card {
  background: rgba(20, 24, 35, 0.6) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px;
  padding: 20px;
  margin: 8px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.card:hover { border-color: rgba(0, 229, 255, 0.3) !important; box-shadow: 0 6px 20px rgba(0, 229, 255, 0.1); }

/* 알림 및 프로그레스바 */
.stAlert { border-radius: 10px !important; border: none !important; background: rgba(255,255,255,0.05) !important; }
.stProgress > div > div { background: linear-gradient(90deg, #00E5FF, #FF00FF) !important; border-radius: 6px !important; }

/* 테이블 (주식, 코인) */
.stock-table { width: 100%; border-collapse: collapse; }
.stock-table th { background: rgba(0, 229, 255, 0.1); color: #00E5FF !important; font-family: 'Orbitron', sans-serif !important; font-size: 0.8rem !important; padding: 12px; text-align: left; border-bottom: 1px solid rgba(0, 229, 255, 0.2); letter-spacing: 1px; }
.stock-table td { padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.95rem; }
.stock-table tr:hover td { background: rgba(255, 255, 255, 0.02); }
.p-up   { color: #FF4B4B !important; font-weight: 900; }
.p-down { color: #4B9EFF !important; font-weight: 900; }
.p-flat { color: #888 !important; }

/* 스코어보드 및 기타 요소들 */
.scoreboard { background: linear-gradient(135deg, #0A0F1C, #1A1C2E); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 16px; padding: 28px; text-align: center; box-shadow: inset 0 0 30px rgba(0,0,0,0.8); }
.score-number { font-size: 3.5rem !important; font-weight: 900; color: #00FF88 !important; text-shadow: 0 0 15px rgba(0,255,136,0.4); line-height: 1; }
.team-label   { font-size: 1.2rem; font-weight: 900; color: #FFF !important; margin-bottom: 6px; }
.match-time   { font-family: 'Orbitron'; color: #00E5FF !important; font-size: 1rem; margin-top: 14px; }
.commentary-item { background: rgba(255,255,255,0.03); border-left: 3px solid #00E5FF; padding: 10px 14px; margin: 6px 0; border-radius: 0 6px 6px 0; font-size: 0.9rem; color: #CCC !important; }
.news-banner { background: linear-gradient(135deg, rgba(255,214,0,0.1), rgba(255,100,0,0.05)); border: 1px solid rgba(255,214,0,0.3); border-radius: 10px; padding: 12px 18px; font-weight: 700; color: #FFD600 !important; margin: 12px 0; font-size: 0.95rem; }
.estate-card { background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(0,0,0,0.2)); border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 18px 22px; margin: 10px 0; }
.estate-income { color: #00FF88 !important; font-weight: 900; font-size: 0.9rem; }
.market-listing { background: rgba(0, 229, 255, 0.05); border: 1px solid rgba(0, 229, 255, 0.2); border-radius: 12px; padding: 16px 20px; margin: 8px 0; }
.market-initial { background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0, 255, 136, 0.2); border-radius: 12px; padding: 16px 20px; margin: 8px 0; }
.my-listing { background: rgba(255, 214, 0, 0.05); border: 1px solid rgba(255, 214, 0, 0.2); border-radius: 12px; padding: 16px 20px; margin: 8px 0; }
.lotto-pool { background: linear-gradient(135deg, #11052C, #2A0845); border: 1px solid rgba(255, 0, 255, 0.3); border-radius: 16px; padding: 28px; text-align: center; box-shadow: inset 0 0 30px rgba(0,0,0,0.6); }
.lotto-amount { font-size: 2.5rem !important; color: #FF00FF !important; text-shadow: 0 0 15px rgba(255,0,255,0.5); font-weight: 900; }
.vip-banner { background: linear-gradient(135deg, #2A1A00, #4A2500); border: 1px solid rgba(255, 214, 0, 0.4); border-radius: 16px; padding: 24px; text-align: center; box-shadow: 0 0 20px rgba(255,214,0,0.1); }
.slot-display { font-size: 3.5rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.6); border: 1px inset rgba(255,214,0,0.2); border-radius: 14px; letter-spacing: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
.question-box { background: rgba(0, 102, 255, 0.1); border: 1px solid rgba(0, 102, 255, 0.3); border-radius: 12px; padding: 28px; line-height: 1.8; font-size: 1.1rem; color: #FFF !important; }
.mine-card { background: linear-gradient(135deg, rgba(139,69,19,0.15), rgba(0,0,0,0.3)); border: 1px solid rgba(205,127,50,0.3); border-radius: 14px; padding: 20px; text-align: center; }

/* 거래 기록 */
.tx-row { display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.9rem; }
.cooldown-badge { background: rgba(255, 75, 75, 0.1); border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 6px; padding: 4px 10px; font-size: 0.78rem; color: #FF4B4B !important; display: inline-block; margin-left: 8px; font-weight: 700; }

/* ===================================================
   🚨 사이드바 열기/닫기 텍스트 버튼으로 변경 (초록/빨강 네온)
   =================================================== */
/* 기존 화살표/X 아이콘 숨기기 */
[data-testid="collapsedControl"] svg,
[data-testid="stSidebarCollapseButton"] svg {
    display: none !important;
}

/* 1. 메뉴 열기 버튼 (접혀있을 때) */
[data-testid="collapsedControl"] {
    background-color: rgba(0, 255, 136, 0.1) !important;
    border: 2px solid #00FF88 !important;
    border-radius: 20px !important;
    width: 70px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-top: 15px !important;
    margin-left: 15px !important;
    box-shadow: 0 0 15px rgba(0, 255, 136, 0.5), inset 0 0 10px rgba(0, 255, 136, 0.3) !important;
    transition: all 0.3s ease !important;
    z-index: 999999 !important;
}

/* '열기' 텍스트 강제 삽입 */
[data-testid="collapsedControl"]::after {
    content: "열기" !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    font-size: 0.95rem !important;
}

[data-testid="collapsedControl"]:hover {
    background-color: rgba(0, 255, 136, 0.3) !important;
    box-shadow: 0 0 25px rgba(0, 255, 136, 0.8) !important;
    transform: scale(1.05) !important;
}

/* 2. 메뉴 닫기 버튼 (열려있을 때) */
[data-testid="stSidebarCollapseButton"] {
    background-color: rgba(255, 75, 75, 0.1) !important;
    border: 1px solid #FF4B4B !important;
    border-radius: 20px !important;
    width: 60px !important;
    height: 35px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 0 10px rgba(255, 75, 75, 0.4) !important;
    transition: all 0.2s ease !important;
}

/* '닫기' 텍스트 강제 삽입 */
[data-testid="stSidebarCollapseButton"]::after {
    content: "닫기" !important;
    color: #FFFFFF !important;
    font-weight: 900 !important;
    font-size: 0.9rem !important;
}

[data-testid="stSidebarCollapseButton"]:hover {
    background-color: rgba(255, 75, 75, 0.4) !important;
    box-shadow: 0 0 15px rgba(255, 75, 75, 0.8) !important;
}

/* 📱 모바일 화면용 설정 (화면이 768px 이하일 때 자동 적용) */
@media (max-width: 768px) {
    .block-container { 
        zoom: 0.92; 
        padding-top: 2rem !important; 
        padding-left: 0.5rem !important; 
        padding-right: 0.5rem !important; 
        padding-bottom: 2rem !important; 
    }
    div[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.5rem !important; }
    p,span,label,td,th { font-size:0.85rem !important; }
    h1 { font-size:1.4rem !important; }
    h2 { font-size:1.1rem !important; }
    h3 { font-size:0.95rem !important; }
    .stButton>button { height:40px !important; font-size:0.85rem !important; }
    .score-number { font-size:2.2rem !important; }
    .lotto-amount { font-size:1.4rem !important; }
    .card { padding: 10px !important; margin: 4px 0 !important; }
    .estate-card, .market-listing, .market-initial { padding: 10px !important; margin: 6px 0 !important; }
    [data-testid="stMetric"] { padding: 8px 12px !important; }
    html, body, .stApp {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    * {
        word-break: keep-all !important;
        overflow-wrap: break-word !important;
    }
    div[style*="display: flex"], div[style*="display:flex"] {
        flex-wrap: wrap !important;
    }
    .stock-table {
        display: block !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
    }
    .stock-table th, .stock-table td { 
        padding: 6px 8px !important; 
        font-size: 0.78rem !important; 
    }
}

/* 💻 PC 화면용 설정 (화면이 769px 이상일 때 자동 적용) */
@media (min-width: 769px) {
    p,span,label,td,th,.stSelectbox label { font-size:1rem !important; }
    .stButton>button { height:52px !important; font-size:1rem !important; }
}
"""

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

if 'logged_in_user' in st.session_state:
    us_check = load_db(USERS_FILE, {})
    my_uid = st.session_state.logged_in_user
    if my_uid in us_check:
        db_user = us_check[my_uid]
        st.session_state.global_cash = db_user.get('cash', 0)
        st.session_state.real_estate = db_user.get('real_estate', {})
        st.session_state.loan = db_user.get('loan', 0)
        st.session_state.inventory = db_user.get('inventory', [])

# ==============================
# 🔐 로그인
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("""
<style>
.stApp { background: radial-gradient(ellipse at 20% 50%, #0d0221 0%, #050510 60%, #000 100%) !important; }
* { font-family:'Noto Sans KR',sans-serif !important; color:#FFF !important; }
.login-title {
  font-family:'Orbitron',monospace !important; font-size:clamp(2rem,6vw,4rem) !important;
  font-weight:900; text-align:center;
  background:linear-gradient(135deg,#00E5FF 0%,#FF00FF 50%,#FFD600 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  padding:20px 0 5px 0; letter-spacing:4px; animation:glow 3s ease-in-out infinite alternate;
}
@keyframes glow { from{filter:drop-shadow(0 0 10px #00E5FF)} to{filter:drop-shadow(0 0 30px #FF00FF)} }
.login-sub { text-align:center; color:#888 !important; font-size:1rem; margin-bottom:20px; letter-spacing:3px; }
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
    st.markdown("<div class='login-sub'>∙ 자본주의 생존 시뮬레이션 게임 v18.2 ∙</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ✨ 신규: 로그인 화면 게임 소개(스플래시) 패널
    # ---------------------------------------------------------
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(0, 229, 255, 0.05), rgba(255, 0, 200, 0.05)); border: 1px solid rgba(0, 229, 255, 0.3); border-radius: 15px; padding: 25px; margin-bottom: 30px; max-width: 800px; margin-left: auto; margin-right: auto; text-align: center; box-shadow: 0 0 20px rgba(0, 229, 255, 0.1);'>
        <h3 style='color: #FFD600 !important; margin-top: 0; margin-bottom: 20px; font-family: "Orbitron", monospace; letter-spacing: 1px;'>🚀 무엇을 하는 게임인가요?</h3>
        <div style='display: flex; justify-content: center; gap: 15px; flex-wrap: wrap; margin-bottom: 20px;'>
            <div style='flex: 1; min-width: 180px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);'>
                <div style='font-size: 2.2rem; margin-bottom: 5px;'>📈</div>
                <b style='color:#00E5FF; font-size: 1.1rem;'>투자 & 자산 증식</b><br>
                <span style='font-size:0.85rem; color:#aaa; line-height: 1.4; display: inline-block; margin-top: 5px;'>주식, 코인, 부동산<br>안전하고 확실한 부의 축적</span>
            </div>
            <div style='flex: 1; min-width: 180px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);'>
                <div style='font-size: 2.2rem; margin-bottom: 5px;'>🎰</div>
                <b style='color:#FF4B4B; font-size: 1.1rem;'>도박 & 미니게임</b><br>
                <span style='font-size:0.85rem; color:#aaa; line-height: 1.4; display: inline-block; margin-top: 5px;'>슬롯, 카지노, 하이퍼카 레이싱<br>하이리스크 하이리턴 일확천금</span>
            </div>
            <div style='flex: 1; min-width: 180px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);'>
                <div style='font-size: 2.2rem; margin-bottom: 5px;'>⚔️</div>
                <b style='color:#00FF88; font-size: 1.1rem;'>경쟁 & RPG 요소</b><br>
                <span style='font-size:0.85rem; color:#aaa; line-height: 1.4; display: inline-block; margin-top: 5px;'>전설의 명검 강화, 클랜전<br>서버 1위 달성 및 칭호 획득</span>
            </div>
        </div>
        <p style='color: #ddd; font-size: 0.95rem; margin: 0; line-height: 1.6;'>
            가입 즉시 초기 정착금 <b style='color:#00E5FF; font-size:1.1rem;'>1억 원</b>이 지급됩니다.<br>지금 바로 시민으로 등록하고 우주 최고의 억만장자가 되어보세요!
        </p>
    </div>
    """, unsafe_allow_html=True)
    # ---------------------------------------------------------

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
                        'crypto_portfolio': u.get('crypto_portfolio', {}),
                        'daily_quests':     u.get('daily_quests', {}),
                        'weapon_level':   u.get('weapon_level', 0), 
                        'bulk_trade_date':  u.get('bulk_trade_date', ''),
                        'bulk_trade_count': u.get('bulk_trade_count', 0),
                        'last_estate_reset': u.get('last_estate_reset', 0),
                    })
                    st.rerun()
                if l_id == "admin" and l_pw == ADMIN_PW:
                    if "admin" not in users:
                        users["admin"] = {"pw":"****","cash":999_999_999_999,"inventory":[],
                                         "equipped_title":"👑 절대신 창조주","portfolio":{},
                                         "real_estate":{},"rent_time":time.time(),
                                         "loan":0,"loan_time":time.time(),}
                        save_db(USERS_FILE, users)
                    _do_login("admin")
                elif l_id != "admin" and l_id in users and users[l_id]['pw'] == hash_pw(l_pw):
                    _do_login(l_id)
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")
        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 시민 등록하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(n_id) < 2:
                    st.error("아이디는 2자 이상이어야 합니다.")
                else:
                    users[n_id] = {"pw":hash_pw(n_pw),"cash":100_000_000,"inventory":[],
                                   "equipped_title":"🌱 신규시민","portfolio":{},
                                   "real_estate":{},"rent_time":time.time(),
                                   "loan":0,"loan_time":time.time(),}
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 초기 자금 1억원이 지급되었습니다!")
    st.stop()

# ==============================
# 🌐 서버 마켓 동기화
# ==============================
market = get_market()
cur_t  = time.time()
m_up   = False

if 'logged_in_user' in st.session_state:
    if st.session_state.get('last_estate_reset', 0) < market.get('force_estate_reset', 0):
        st.session_state.real_estate = {}
        st.session_state.rent_time = cur_t
        st.session_state.last_estate_reset = market.get('force_estate_reset', 0)
        sync_user_data()

stock_passed = cur_t - market.get('last_tick', cur_t)
s_ticks = int(stock_passed / 10)
if s_ticks > 0:
    s_ticks = min(s_ticks, 60)  # 🚨 오프라인 시간 보정 (최대 60틱까지만 시뮬레이션)
    for _ in range(s_ticks):
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

if 'crypto_data' not in market:
    market['crypto_data'] = {
        c['id']: {"name": c['name'], "icon": c['icon'],
                  "price": float(c['base_price']), "history": [float(c['base_price'])]}
        for c in CRYPTO_CONFIG
    }
    m_up = True

crypto_passed = cur_t - market.get('crypto_tick', cur_t)
c_ticks = int(crypto_passed / 5)
if c_ticks > 0:
    c_ticks = min(c_ticks, 60)  # 🚨 코인 시장 오프라인 시간 보정
    for _ in range(c_ticks):
        for c in CRYPTO_CONFIG:
            curr = market['crypto_data'][c['id']]
            ch = (random.random() - 0.5) * 2 * c['vol']
            curr['price'] = max(0.01, round(curr['price'] * (1 + ch), 6))
            curr['history'].append(curr['price'])
            if len(curr['history']) > 60: curr['history'].pop(0)
    market['crypto_tick'] = cur_t
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
            log_tx(win, "로또당첨", f"글로벌 로또 1등 잭팟!!", prize) # 로그 추가
            # 세션 조작은 제거함. 동기화 로직에서 알아서 처리하도록 함.
            
        market['news'] = f"🎊 [당첨 확정] {win}님이 {format_korean_money(prize)} 대박 상금을 수령하셨습니다!!"
        market['lotto_pool'] = 5_000_000_000
        market['lotto_tickets'] = {}
        market['lotto_last_draw'] = cur_t
        m_up = True

# ── 시즌 자동 종료 체크 ──
if 'season_num' not in market:
    market['season_num']      = 1
    market['season_start']    = cur_t
    market['season_end']      = cur_t + 30 * 86400
    market['season_records']  = {}
    m_up = True

if cur_t > market.get('season_end', cur_t + 9999) and not market.get('season_ending', False):
    market['season_ending'] = True
    us_all = load_db(USERS_FILE, {})
    rd = []
    for uid_s, udata_s in us_all.items():
        if uid_s == 'admin': continue
        w = udata_s.get('cash', 0) - udata_s.get('loan', 0)
        for sid_s, p_s in udata_s.get('portfolio', {}).items():
            if sid_s in market['stock_data']:
                w += p_s.get('qty', 0) * market['stock_data'][sid_s]['price']
        for eid_s, cnt_s in udata_s.get('real_estate', {}).items():
            if eid_s in estate_config:
                w += estate_config[eid_s]['base_price'] * cnt_s * 0.8
        rd.append((uid_s, w))
    rd.sort(key=lambda x: x[1], reverse=True)

    season_titles = [
        f"🥇 [시즌{market['season_num']}] 전설의 우승자",
        f"🥈 [시즌{market['season_num']}] 준우승의 영광",
        f"🥉 [시즌{market['season_num']}] 시즌 3위",
    ]
    record = {}
    for i, (uid_s, w_s) in enumerate(rd[:3]):
        title = season_titles[i]
        record[f"rank{i+1}"] = uid_s
        if uid_s in us_all:
            if title not in us_all[uid_s].get('inventory', []):
                us_all[uid_s].setdefault('inventory', []).append(title)
            us_all[uid_s]['equipped_title'] = title

    for uid_s in us_all:
        if uid_s == 'admin': continue
        us_all[uid_s]['cash']             = 100_000_000
        us_all[uid_s]['portfolio']        = {}
        us_all[uid_s]['crypto_portfolio'] = {}
        us_all[uid_s]['real_estate']      = {}
        us_all[uid_s]['loan']             = 0
        us_all[uid_s]['loan_time']        = cur_t
        us_all[uid_s]['rent_time']        = cur_t
        us_all[uid_s]['weapon_level']     = 0
        us_all[uid_s]['daily_quests']     = {}
        us_all[uid_s]['bulk_trade_count'] = 0

    save_db(USERS_FILE, us_all)

    clan_db_reset = load_clan_db()
    for cn in clan_db_reset:
        clan_db_reset[cn]['bank'] = 0
    save_clan_db(clan_db_reset)

    save_estate_market({
        "listings": [], "owner_counts": {},
        "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}
    })

    sn = market['season_num']
    market['season_records'][str(sn)] = record
    market['season_num']     = sn + 1
    market['season_start']   = cur_t
    market['season_end']     = cur_t + 30 * 86400
    market['season_ending']  = False
    market['lotto_pool']     = 5_000_000_000
    market['lotto_tickets']  = {}
    market['force_estate_reset'] = cur_t
    market['news'] = f"🏆 [시즌{sn} 종료] {rd[0][0] if rd else '?'}님이 시즌 우승! 새 시즌 시작!"
    m_up = True

if m_up: save_market(market)

if st.session_state.loan > 0:
    MAX_CYC = 30  # 🚨 이자 폭탄 방지: 장기 오프라인이어도 최대 30번(5분 분량)까지만 이자 적용
    MAX_LOAN = 999_999_999_999_999
    elapsed = cur_t - st.session_state.loan_time
    cyc = min(int(elapsed / 10), MAX_CYC)
    if cyc > 0:
        new_loan = st.session_state.loan * (1.02 ** cyc)
        st.session_state.loan = min(int(new_loan), MAX_LOAN)
        st.session_state.loan_time += cyc * 10  # 🚨 처리한 틱만큼만 전진, 나머지 시간 보존
        sync_user_data()
        
nw = get_net_worth(st.session_state.logged_in_user, market)
if st.session_state.loan > 0 and nw < 0:
    st.session_state.equipped_title = "💸 신용불량자"
    sync_user_data()

# ==============================
# 🧭 메뉴
# ==============================
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"

is_admin = st.session_state.logged_in_user == "admin"
is_vip   = nw >= 100_000_000_000 or is_admin


CATEGORY_MENUS = {
    "📈 경제": [
        "🏠 홈 광장 (튜토리얼)",
        "📈 주식 트레이딩",
        "🪙 코인 거래소",
        "🏢 부동산 거래소",
        "🏦 은행 (대출/송금)",
        "📜 내 거래 기록",
    ],
    "🎮 미니게임": [
        "🎰 럭키 슬롯",
        "🃏 블랙잭 카지노",
        "⛏️ 광산 (노가다)",
        "💻 정처기 CBT",
        "⚔️ 글로벌 로또",       # 경제에서 이동
        "🗡️ 전설의 명검 강화",  # 경제에서 이동
        "🎴 가챠 뽑기",         # 경제에서 이동
    ],
    "🌟 성장 & 혜택": [         # 신규 카테고리 생성
        "📅 일일 퀘스트",       # 경제에서 이동
        "👑 칭호 상점",         # 경제에서 이동
    ],
    "⚽ 스포츠": [
        "⚽ 구단주 시뮬레이터",
        "⚽ 조기축구 승부차기",
        "🏎️ 하이퍼카 레이싱",
        "🛠️ 커스텀 튜닝 차고지",
    ],
    "👥 커뮤니티": [
        "🏰 길드/클랜",
        "🏅 랭킹 & 게시판",
        "✉️ 개인 쪽지함",
    ],
}

if is_vip:
    CATEGORY_MENUS["📈 경제"].insert(1, "💎 VIP 라운지")
if is_admin:
    CATEGORY_MENUS["⚙️ 관리"] = ["🛠️ 창조주 통제소"]

# 현재 페이지가 어느 카테고리인지 찾기
def get_current_category():
    for cat, pages in CATEGORY_MENUS.items():
        if st.session_state.current_page in pages:
            return cat
    return list(CATEGORY_MENUS.keys())[0]

if "current_category" not in st.session_state:
    st.session_state.current_category = get_current_category()

# 쪽지 뱃지
msg_db_check = load_db("messages_db.json", {})
my_unread = sum(1 for m in msg_db_check.get(st.session_state.logged_in_user, {}).get("inbox", []) if not m.get("read", False))

# --- [수정 후] 사용자의 기기 선택에 따라 UI 분기 ---
# session_state에 저장된 device_mode 문자열에 'PC'가 포함되어 있는지 확인합니다.
is_pc_mode = "PC" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

if is_pc_mode:
    # 💻 PC 모드 선택 시: 왼쪽 사이드바에 메뉴 배치
    with st.sidebar:
        # 유저 프로필
        st.markdown(f"""
<div style='padding:14px 16px; background:rgba(255,255,255,0.05); border:1px solid rgba(0,229,255,0.2);
     border-radius:10px; margin-bottom:14px;'>
  <div style='font-size:0.8rem; color:#00E5FF; margin-top:3px;'>{st.session_state.equipped_title}</div>
  <div style='font-size:1rem; font-weight:700; color:#E2E8F0;'>
    {st.session_state.logged_in_user}
    {"  🔴" if my_unread > 0 else ""}
  </div>
</div>""", unsafe_allow_html=True)

        # 자산 요약
        col_a, col_b = st.columns(2)
        col_a.metric("💵 현금", format_korean_money(st.session_state.global_cash))
        col_b.metric("📊 순자산", format_korean_money(nw))
        if st.session_state.loan > 0:
            st.metric("💳 대출", format_korean_money(st.session_state.loan))

        st.write("---")

        # 카테고리 탭 (버튼식)
        st.markdown("<div style='font-size:0.75rem; color:#999; margin-bottom:8px;'>카테고리</div>", unsafe_allow_html=True)
        for cat in CATEGORY_MENUS:
            is_active_cat = (st.session_state.current_category == cat)
            if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                st.session_state.current_category = cat
                st.session_state.current_page = CATEGORY_MENUS[cat][0]
                st.rerun()

        st.write("---")

        # 세부 메뉴 선택 (라디오 버튼)
        cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
        st.markdown(f"<div style='font-size:0.75rem; color:#999; margin-bottom:8px;'>{st.session_state.current_category} 메뉴</div>", unsafe_allow_html=True)
        
        cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
        selected_menu = st.radio("메뉴", cur_cat_pages, index=cur_idx, label_visibility="collapsed")
        if selected_menu != st.session_state.current_page:
            st.session_state.current_page = selected_menu
            st.rerun()

        st.write("---")
        if st.button("로그아웃", use_container_width=True):
            sync_user_data(); st.session_state.clear(); st.rerun()

else:
    # 📱 모바일 모드 선택 시: 사이드바 없이 상단 드롭다운 배치
    col_a, col_b = st.columns([3, 1])
    with col_a:
        unread_txt = f" 🔴{my_unread}" if my_unread > 0 else ""
        st.markdown(f"""
<div style='font-size:0.82rem; color:#999;'>
  👤 <b style='color:#E2E8F0;'>{st.session_state.logged_in_user}</b>{unread_txt}
  &nbsp;|&nbsp; <span style='color:#00E5FF;'>{st.session_state.equipped_title}</span>
</div>
<div style='font-size:0.9rem; font-weight:700; color:#E2E8F0; margin-top:2px;'>
  💵 {format_korean_money(st.session_state.global_cash)}
</div>""", unsafe_allow_html=True)
    with col_b:
        if st.button("로그아웃"):
            sync_user_data(); st.session_state.clear(); st.rerun()

    # 카테고리 및 메뉴 선택을 드롭다운으로 변경 (좁은 화면 최적화)
    cat_sel = st.selectbox("카테고리", list(CATEGORY_MENUS.keys()), 
                            index=list(CATEGORY_MENUS.keys()).index(st.session_state.current_category))
    if cat_sel != st.session_state.current_category:
        st.session_state.current_category = cat_sel
        st.session_state.current_page = CATEGORY_MENUS[cat_sel][0]
        st.rerun()

    cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
    cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
    selected_menu = st.selectbox("메뉴 선택", cur_cat_pages, index=cur_idx)
    if selected_menu != st.session_state.current_page:
        st.session_state.current_page = selected_menu
        st.rerun()


# --- 공통 뉴스 배너 및 공지 출력 ---
menu = st.session_state.current_page
st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
if market.get('admin_msg'):
    col = market.get('admin_color', '#FF4B4B')
    st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {col};border-radius:10px;padding:12px 16px;color:{col}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {market['admin_msg']}</div>", unsafe_allow_html=True)

# =====================================================================
# 💎 VIP 라운지
# =====================================================================
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
  <div style='color:#888;font-size:0.78rem;margin-top:14px;'>※ 정보 유출 시 창조주의 징벌이 따릅니다</div>
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
                u_db_check = load_db(USERS_FILE, {})
                db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
                if db_cash < 100_000_000:
                    st.error("잔액 부족! (DB 검증 실패)")
                else:
                    set_cooldown("vip_slot")
                    st.session_state.global_cash -= 100_000_000
                    if random.random() < 0.5:
                        st.session_state.global_cash += 250_000_000
                        st.success("🎉 승리! +2.5억 획득!")
                        log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 승리", 150_000_000)
                    else:
                        st.error("❌ 아쉽습니다. 다음 기회를!")
                        log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 패배", -100_000_000)
                    sync_user_data()
                    if st.session_state.current_page == menu: st.rerun()
            else:
                st.error("잔액 부족!")
    with c2:
        st.markdown("### 📊 VIP 포트폴리오 요약")
        total_stock  = sum(st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price'] for s in stock_config)
        total_estate = sum(estate_config[eid]['base_price'] * cnt * 0.8 for eid, cnt in st.session_state.real_estate.items() if eid in estate_config)
        st.metric("주식 평가액",   format_korean_money(total_stock))
        st.metric("부동산 평가액", format_korean_money(total_estate))
        st.metric("총 순자산",     format_korean_money(nw))

# =====================================================================
# 🏠 홈 광장
# =====================================================================
elif menu == "🏠 홈 광장 (튜토리얼)":
    st.title("🌌 HYOMIN UNIVERSE")
    
    # 1. 게임 캐릭터 프로필 느낌의 UI
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #111128, #0a0a20); border: 2px solid #00E5FF; border-radius: 15px; padding: 20px; display: flex; align-items: center; gap: 20px; margin-bottom: 25px; box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);'>
        <div style='font-size: 4rem; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 50%;'>🧑‍🚀</div>
        <div style='flex: 1;'>
            <div style='color:#00FF88; font-weight:900; font-size:1.1rem; margin-bottom:5px;'>{st.session_state.equipped_title}</div>
            <div style='font-size: 2rem; font-family: "Orbitron", monospace; font-weight: 900; color: #fff; line-height: 1.2;'>{st.session_state.logged_in_user}</div>
            <div style='color:#888; font-size:0.9rem; margin-top:5px;'>환영합니다! 우주에서의 새로운 하루가 시작되었습니다.</div>
        </div>
        <div style='text-align: right; border-left: 1px solid rgba(0,229,255,0.3); padding-left: 20px;'>
            <div style='color:#94A3B8; font-size:0.9rem;'>보유 현금</div>
            <div style='font-size:1.8rem; font-weight:900; color:#FFD600;'>{format_korean_money(st.session_state.global_cash)}</div>
            <div style='color:#94A3B8; font-size:0.9rem; margin-top:10px;'>총 순자산</div>
            <div style='font-size:1.3rem; font-weight:900; color:#E2E8F0;'>{format_korean_money(nw)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 🗺️ 성장 단계별 맞춤형 퀘스트 보드
    st.markdown("### 🗺️ 현재 성장 목표")
    
    if nw < 500_000_000:
        # [초보자 코스] 5억 미만
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 229, 255, 0.1), rgba(0, 102, 255, 0.1)); border: 1px solid #00E5FF; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#00E5FF; margin-top:0;'>🌱 튜토리얼 1단계: 흙수저 탈출 작전</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>초기 시드머니를 모아야 합니다. 광산에서 노가다를 하거나 일일 퀘스트를 완료하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>다음 목표: 순자산 5억 달성</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_q1, col_q2 = st.columns(2)
        if col_q1.button("⛏️ 광산으로 돈 벌러 가기", use_container_width=True):
            st.session_state.current_category = "🎮 미니게임" # 카테고리 변경 추가!
            st.session_state.current_page = "⛏️ 광산 (노가다)"
            st.rerun()
        if col_q2.button("📅 일일 퀘스트 보상받기", use_container_width=True):
            st.session_state.current_category = "🌟 성장 & 혜택" # 카테고리 변경 추가!
            st.session_state.current_page = "📅 일일 퀘스트"
            st.rerun()
            
    elif nw < 10_000_000_000:
        # [중급자 코스] 5억 ~ 100억 미만
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 214, 0, 0.1), rgba(255, 100, 0, 0.1)); border: 1px solid #FFD600; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#FFD600; margin-top:0;'>🏢 튜토리얼 2단계: 자본가의 길</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>이제 돈이 돈을 벌게 해야 합니다. 주식과 코인에 투자하고 첫 부동산을 매입하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>다음 목표: 순자산 100억 달성 (건물주)</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_q1, col_q2, col_q3 = st.columns(3)
        if col_q1.button("📈 주식 시장 보기", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "📈 주식 트레이딩"
            st.rerun()
        if col_q2.button("🪙 코인 떡상 노리기", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "🪙 코인 거래소"
            st.rerun()
        if col_q3.button("🏢 첫 부동산 사기", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "🏢 부동산 거래소"
            st.rerun()
            
    else:
        # [고급자 코스] 100억 이상
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(100, 0, 255, 0.1)); border: 1px solid #FF00FF; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#FF00FF; margin-top:0;'>👑 튜토리얼 완료: 우주 억만장자</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>당신은 이미 훌륭한 자본가입니다. 이제 서버 랭킹 1위를 향해 명검을 벼리고 하이퍼카를 수집하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>최종 목표: 서버 랭킹 1위 및 모든 칭호 수집</div>
        </div>
        """, unsafe_allow_html=True)
        
        col_q1, col_q2 = st.columns(2)
        if col_q1.button("🗡️ 명검 강화하러 가기", use_container_width=True):
            st.session_state.current_category = "🎮 미니게임" # 카테고리 변경 추가!
            st.session_state.current_page = "🗡️ 전설의 명검 강화"
            st.rerun()
        if col_q2.button("🏎️ 하이퍼카 차고지 가기", use_container_width=True):
            st.session_state.current_category = "⚽ 스포츠" # 카테고리 변경 추가!
            st.session_state.current_page = "🛠️ 커스텀 튜닝 차고지"
            st.rerun()

    st.write("---")

    # 3. 기존 대시보드 (대출 및 부동산 수금 요약)
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='color:#888; font-size:0.9rem;'>💳 갚아야 할 대출금</div>
            <div style='color:#FF4B4B; font-size:1.5rem; font-weight:900;'>{format_korean_money(st.session_state.loan)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        _capped_pass = min(int(cur_t - st.session_state.rent_time), 86400)
        total_rent_pending = sum(
            estate_config[eid]['income'] * cnt * _capped_pass
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='color:#888; font-size:0.9rem;'>🏢 수금 대기 중인 임대료</div>
            <div style='color:#00FF88; font-size:1.5rem; font-weight:900;'>{format_korean_money(total_rent_pending)}</div>
        </div>
        """, unsafe_allow_html=True)

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
  <div style='font-size:1rem;font-weight:900;color:#E2E8F0;'>₩{d['price']:,}</div>
  <div style='font-size:0.85rem;color:{clr};font-weight:900;'>{arrow} {abs(diff):.2f}%</div>
</div>""", unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🏆 이번 시즌 랭킹 Top 5")
    users_all = load_db(USERS_FILE, {})  
    rank_data = []
    for uid, udata in users_all.items(): 
        if uid == "admin": continue
        w = udata.get('cash', 0) - udata.get('loan', 0)
        for sid, p in udata.get('portfolio', {}).items():
            if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
        for eid, cnt in udata.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * cnt * 0.8
        w_lv = udata.get('weapon_level', 0)
        if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
        rank_data.append({"uid": uid, "title": udata.get('equipped_title', '신규시민'), "nw": w})
    rank_data.sort(key=lambda x: x['nw'], reverse=True)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i, r in enumerate(rank_data[:5]):
        me = " ← 나" if r['uid'] == st.session_state.logged_in_user else ""
        st.markdown(f"""
<div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 20px;'>
  <span style='font-size:1.3rem;'>{medals[i]}</span>
  <span style='font-weight:900;color:#CBD5E1;'>{r['uid']}{me}</span>
  <span style='color:#888;font-size:0.85rem;'>{r['title']}</span>
  <span style='color:#FFD600;font-weight:900;'>{format_korean_money(r['nw'])}</span>
</div>""", unsafe_allow_html=True)

# =====================================================================
# 📈 주식 트레이딩
# =====================================================================
elif menu == "📈 주식 트레이딩":
    st.title("📈 통합 거래소")

    TRADE_COOLDOWN   = 3.0  
    BULK_COOLDOWN    = 8.0  
    DAILY_BULK_LIMIT = 5    

    today_str = datetime.now(KST).strftime("%Y-%m-%d")
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
            rows += f"<tr><td>{s['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#E2E8F0;'>₩{d['price']:,}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td><td style='text-align:right;color:#888;'>₩{d['history'][-2]:,}</td></tr>"
        st.markdown(f"<table class='stock-table'><thead><tr><th>종목</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th><th style='text-align:right;'>전일가</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

    with tab_port:
        p_rows = []; total_eval = 0; total_invested = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp  = market['stock_data'][sid]['price']
                ap  = info.get('avg_price', 0)
                inv = qty * ap; total_invested += inv
                ev  = qty * cp; total_eval += ev
                pnl = ev - inv
                roi = (cp - ap) / ap * 100 if ap > 0 else 0
                p_rows.append({
                    "종목": market['stock_data'][sid]['name'], 
                    "수량": f"{qty}주",
                    "평균단가": f"₩{int(ap):,}", 
                    "현재가": f"₩{int(cp):,}",
                    "평가액": f"₩{int(ev):,}",
                    "평가손익": f"₩{int(pnl):,}",
                    "수익률": f"{roi:+.2f}%"
                })
        if p_rows:
            st.table(pd.DataFrame(p_rows))
            c1, c2, c3 = st.columns(3)
            c1.metric("💰 총 매수금액", format_korean_money(total_invested))
            c2.metric("📊 총 평가액", format_korean_money(total_eval))
            c3.metric("📈 총 평가손익", format_korean_money(total_eval - total_invested))
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
        st.markdown(f"<div style='text-align:center;margin:10px 0;'><span style='font-size:1.8rem;font-weight:900;color:#E2E8F0;font-family:Orbitron;'>₩{cp:,}</span> <span style='color:{clr};font-weight:900;'>{arr} {abs(pct):.2f}%</span></div>", unsafe_allow_html=True)

       
        # ====== 수익률 현황판 시작 ======
        my_info = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
        my_qty = my_info.get('qty', 0)
        my_avg = my_info.get('avg_price', 0)
        
        if my_qty > 0:
            my_eval = my_qty * cp  # 💡 평가액 계산
            my_roi = (cp - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_col = "#FF4B4B" if my_roi > 0 else "#4B9EFF" if my_roi < 0 else "#888"
            roi_arr = "▲" if my_roi > 0 else "▼" if my_roi < 0 else ""
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,0,0,0.5)); border:1px solid rgba(255,255,255,0.1); padding:14px; border-radius:10px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>보유 수량</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{my_qty}주</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>평균 단가</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{format_korean_money(my_avg)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>현재 평가액</span><br><b style='color:#FFD600;font-size:1.1rem;'>{format_korean_money(my_eval)}</b></div>
                <div style='flex:1; text-align:right;'><span style='color:#94A3B8;font-size:0.85rem;'>수익률</span><br><b style='color:{roi_col};font-size:1.2rem;'>{roi_arr} {my_roi:+.2f}%</b></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:rgba(255,255,255,0.03); border:1px dashed rgba(255,255,255,0.1); padding:12px; border-radius:10px; margin-bottom:18px; color:#888; text-align:center;'>현재 보유 중인 주식이 없습니다.</div>", unsafe_allow_html=True)
        # ====== 수익률 현황판 끝 ======
        
        
        qty_input = st.number_input("거래 수량 (주)", min_value=1, step=1, value=1)
        cost = qty_input * cp
        st.caption(f"예상 거래금액: {format_korean_money(cost)}")

        bulk_rem  = cooldown_remaining("bulk_trade", BULK_COOLDOWN)
        trade_rem = cooldown_remaining(f"trade_{sid}", TRADE_COOLDOWN)
        bulk_left = DAILY_BULK_LIMIT - st.session_state.get("bulk_trade_count", 0)

        if bulk_rem > 0:
            st.markdown(f"<span class='cooldown-badge'>풀매수/풀매도 쿨다운 {bulk_rem:.1f}초</span>", unsafe_allow_html=True)
        if trade_rem > 0:
            st.markdown(f"<span class='cooldown-badge'>일반 거래 쿨다운 {trade_rem:.1f}초</span>", unsafe_allow_html=True)

        st.markdown(f"<div style='color:#888;font-size:0.78rem;margin-bottom:8px;'>풀매수/풀매도 오늘 남은 횟수: <b style='color:#FFD600;'>{bulk_left}회</b></div>", unsafe_allow_html=True)

        def _safe_buy(qty, price, sid_):
            total = qty * price
            if st.session_state.global_cash < total:
                st.error("잔액 부족!"); return False
            u_db_check = load_db(USERS_FILE, {})
            uid_check = st.session_state.logged_in_user
            db_cash = u_db_check.get(uid_check, {}).get('cash', 0)
            if db_cash < total:
                st.error("잔액 부족! (DB 검증 실패)"); return False
            st.session_state.global_cash -= total
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
                max_q = int(st.session_state.global_cash // cp) if cp > 0 else 0
                if max_q > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    buy_a = max_q * cp
                    if _safe_buy(max_q, cp, sid):
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
                        sync_user_data(); st.success(f"✅ {qty_input}주 매수 완료!"); st.rerun()

        with c3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True, disabled=trade_rem > 0):
                if trade_rem <= 0:
                    set_cooldown(f"trade_{sid}")
                    if _safe_sell(qty_input, cp, sid):
                        sync_user_data(); st.success(f"✅ {qty_input}주 매도!"); st.rerun()

        with c4:
            bulk_ok2 = (bulk_rem <= 0) and (bulk_left > 0)
            if st.button("💸 풀매도", use_container_width=True, disabled=not bulk_ok2):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    sell_a = own * cp
                    if _safe_sell(own, cp, sid):
                        imp = min((sell_a / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                            market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {d['name']} 물량 투하! -{imp*100:.1f}% 영향"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("보유 주식 없음")

        if bulk_left <= 0:
            st.warning("⚠️ 오늘 풀매수/풀매도 횟수를 모두 사용했습니다. 내일 자정에 초기화됩니다.")

    
        

# =====================================================================
# 🪙 코인 거래소
# =====================================================================
elif menu == "🪙 코인 거래소":
    st.title("🪙 가상화폐 거래소")
    if 'crypto_data' not in market:
        st.warning("코인 시장 개장 중... 잠시 후 새로고침 해주세요.")
        st.stop()
    cdata = market['crypto_data']

    def fmt_crypto_price(price):
        if price >= 1_000_000:   return f"₩{price:,.0f}"
        elif price >= 1:         return f"₩{price:,.2f}"
        elif price >= 0.01:      return f"₩{price:,.4f}"
        else:                    return f"₩{price:.8f}"
    
    def fmt_crypto_qty(qty, cid):
        if cid in ['BTC','ETH']:  return f"{qty:.6f}"
        elif cid in ['SOL','HYO']:return f"{qty:.4f}"
        else:                     return f"{qty:,.2f}"

    tab_market, tab_port, tab_trade = st.tabs(["📊 코인 시황", "💼 내 코인 지갑", "⚡ 거래"])
    
    with tab_market:
        st.markdown("### 🔥 실시간 코인 시황")
        st.caption("⚡ 5초마다 자동 업데이트 | 주식보다 최대 3배 높은 변동성")
        rows_html = "<table class='stock-table'><thead><tr><th>코인</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th></tr></thead><tbody>"
        for c in CRYPTO_CONFIG:
            d    = cdata[c['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 and d['history'][-2] > 0 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲" if diff > 0 else "▼" if diff < 0 else "━"
            rows_html += f"<tr><td>{c['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#E2E8F0;'>{fmt_crypto_price(d['price'])}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td></tr>"
        rows_html += "</tbody></table>"
        st.markdown(rows_html, unsafe_allow_html=True)
        
    with tab_port:
        cp_dict = st.session_state.get('crypto_portfolio', {})
        total_eval = 0; total_invested = 0
        if not cp_dict:
            st.info("보유 중인 코인이 없습니다.")
        else:
            rows = []
            for cid, info in cp_dict.items():
                qty = info.get('qty', 0)
                if qty <= 0 or cid not in cdata: continue
                cur_p  = cdata[cid]['price']
                avg_p  = info.get('avg_price', 0)
                inv = qty * avg_p; total_invested += inv
                ev     = qty * cur_p; total_eval += ev
                pnl = ev - inv
                roi    = (cur_p - avg_p) / avg_p * 100 if avg_p > 0 else 0
                rows.append({
                    "코인": f"{cdata[cid]['name']}", 
                    "보유량": fmt_crypto_qty(qty, cid), 
                    "평균단가": fmt_crypto_price(avg_p), 
                    "현재가": fmt_crypto_price(cur_p),
                    "평가액": format_korean_money(int(ev)), 
                    "평가손익": format_korean_money(int(pnl)),
                    "수익률": f"{roi:+.2f}%"
                })
            if rows:
                st.table(pd.DataFrame(rows))
                c1, c2, c3 = st.columns(3)
                c1.metric("💰 총 매수금액", format_korean_money(int(total_invested)))
                c2.metric("🪙 총 평가액", format_korean_money(int(total_eval)))
                c3.metric("📈 총 평가손익", format_korean_money(int(total_eval - total_invested)))
                
    # 고쳐야 할 모습
    with tab_trade:
        coin_ids = [c['id'] for c in CRYPTO_CONFIG]
        sel_c = st.selectbox(
            "거래할 코인 선택",
            coin_ids,
            format_func=lambda cid: f"{next(c['icon'] for c in CRYPTO_CONFIG if c['id']==cid)} {cdata[cid]['name']} — {fmt_crypto_price(cdata[cid]['price'])}"
        )

        cd    = cdata[sel_c]
        cur_p = cd['price']
 
        # ====== 수익률 현황판 시작 ======
        my_info = st.session_state.get('crypto_portfolio', {}).get(sel_c, {'qty': 0, 'avg_price': 0})
        my_qty = my_info.get('qty', 0)
        my_avg = my_info.get('avg_price', 0)
        
        if my_qty > 0:
            my_eval = my_qty * cur_p  # 💡 평가액 계산
            my_roi = (cur_p - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_col = "#FF4B4B" if my_roi > 0 else "#4B9EFF" if my_roi < 0 else "#888"
            roi_arr = "▲" if my_roi > 0 else "▼" if my_roi < 0 else ""
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,0,0,0.5)); border:1px solid rgba(255,255,255,0.1); padding:14px; border-radius:10px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>보유량</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{fmt_crypto_qty(my_qty, sel_c)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>평균 단가</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{fmt_crypto_price(my_avg)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>현재 평가액</span><br><b style='color:#FFD600;font-size:1.1rem;'>{format_korean_money(int(my_eval))}</b></div>
                <div style='flex:1; text-align:right;'><span style='color:#94A3B8;font-size:0.85rem;'>수익률</span><br><b style='color:{roi_col};font-size:1.2rem;'>{roi_arr} {my_roi:+.2f}%</b></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:rgba(255,255,255,0.03); border:1px dashed rgba(255,255,255,0.1); padding:12px; border-radius:10px; margin-bottom:18px; color:#888; text-align:center;'>현재 보유 중인 코인이 없습니다.</div>", unsafe_allow_html=True)
        # ====== 수익률 현황판 끝 ======
        
        
        tab_buy, tab_sell = st.tabs(["🟢 매수", "🔴 매도"])
        
        with tab_buy:
            current_cash = max(0, int(st.session_state.global_cash))
            JS_MAX_INT = 9007199254740991
            safe_max = min(current_cash, JS_MAX_INT)

            buy_won = st.number_input(
                "투자 금액 (원)", 
                min_value=0, 
                step=10_000,
                max_value=safe_max, 
                value=0, 
                format="%d",
                key="coin_buy_input_safe" 
            )
            if st.button("🟢 매수하기", use_container_width=True):
                if buy_won <= 0: 
                    st.error("금액 입력 오류")
                elif st.session_state.global_cash < buy_won: 
                    st.error("잔액 부족!")
                else:
                    qty_to_buy = buy_won / cur_p
                    u_db_check = load_db(USERS_FILE, {})
                    db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
                    if db_cash < buy_won:
                        st.error("잔액 부족! (DB 검증 실패)")
                    else:
                        st.session_state.global_cash -= buy_won
                        cp_port = st.session_state.get('crypto_portfolio', {})
                        old = cp_port.get(sel_c, {'qty': 0, 'avg_price': 0})
                        new_q = old['qty'] + qty_to_buy
                        new_a = ((old['qty'] * old['avg_price']) + buy_won) / new_q if new_q > 0 else cur_p
                        cp_port[sel_c] = {'qty': new_q, 'avg_price': new_a}
                        st.session_state.crypto_portfolio = cp_port
                        log_tx(st.session_state.logged_in_user, "코인매수", f"{cd['name']} 매수", -int(buy_won))
                        sync_user_data()
                        st.success("✅ 매수 완료!")
                        if sel_c == "HYO" and buy_won >= 1_000_000_000_000_000:
                            claim_hidden_title("pepe_all_in", "👑 [유일무이] 상남자특_김효민_믿음")
                        st.rerun()
                    
        with tab_sell:
            if my_qty <= 0: 
                st.info("보유 중인 코인이 없습니다.")
            else:
                sell_pct = st.slider("매도 비율", min_value=1, max_value=100, value=100, step=1, format="%d%%")
                sell_qty = my_qty * sell_pct / 100
                sell_won = sell_qty * cur_p
                st.caption(f"예상 수령액: {format_korean_money(int(sell_won))}")
                if st.button(f"🔴 매도하기", use_container_width=True):
                    cp = st.session_state.get('crypto_portfolio', {})
                    actual_qty = cp.get(sel_c, {}).get('qty', 0)
                    if actual_qty <= 1e-10:
                        st.error(f"⚠️ 보유량이 없습니다!")
                    else:
                        sell_qty = min(sell_qty, actual_qty)
                        sell_won = sell_qty * cur_p
                        cp[sel_c]['qty'] -= sell_qty
                        if cp[sel_c]['qty'] < 1e-10:
                            del cp[sel_c]

                        st.session_state.crypto_portfolio = cp
                        st.session_state.global_cash += int(sell_won)
                        log_tx(st.session_state.logged_in_user, "코인매도", f"{cd['name']} 매도", int(sell_won))
                        sync_user_data()
                        st.success("✅ 매도 완료!")
                        st.rerun()
                       

# =====================================================================
# 🏢 부동산 거래소
# =====================================================================
elif menu == "🏢 부동산 거래소":
    st.title("🏢 부동산 실거래 마켓")

    uid = st.session_state.logged_in_user
    now = time.time()

    pass_s = int(now - st.session_state.rent_time)

    if pass_s >= 86400:
        st.session_state.rent_time = now - 86400
        pass_s = 86400
        sync_user_data()

    pass_s = max(0, min(pass_s, 86400))
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
  <div style='color:#888;font-size:0.78rem;margin-top:6px;'>초당 {format_korean_money(total_income_rate)} 수입 중</div>
</div>""", unsafe_allow_html=True)

        cd_rent = cooldown_remaining("rent_collect", 3.0)
        if cd_rent > 0:
            st.warning(f"⏱️ 수금 쿨다운 {cd_rent:.1f}초")
        elif st.button("💰 임대 수익 수금하기", use_container_width=True):
            set_cooldown("rent_collect")
            if pending > 0:
                st.session_state.global_cash += int(pending)
                st.session_state.rent_time = now
                sync_user_data()
                log_tx(uid, "부동산수금", "임대 수익 수금", int(pending))
                st.success(f"✅ {format_korean_money(pending)} 수금 완료!")
                st.rerun()

    st.write("---")

    em = load_estate_market()
    initial_listings = get_estate_initial_listings(em)

    tab_market_view, tab_my_estate, tab_sell = st.tabs(["🏪 마켓 (전체 매물)", "🏘️ 내 보유 부동산", "📋 판매 등록"])

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
      <div style='font-weight:900;font-size:1rem;color:#E2E8F0;'>{info['name']}</div>
      <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
      <div style='margin-top:4px;'>
        <span style='color:#FFD600;font-weight:900;'>{format_korean_money(info['base_price'])}</span>
        <span style='color:#777;margin:0 8px;'>|</span>
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
                        em2 = load_estate_market()
                        il2 = next((x for x in get_estate_initial_listings(em2) if x["eid"] == eid), None)
                        if il2 is None or il2["remaining"] <= 0:
                            st.error("⚠️ 이미 매진되었습니다! 유저 매물을 확인하세요.")
                        elif st.session_state.global_cash >= info['base_price']:
                            set_cooldown(cd_key)
                            st.session_state.global_cash -= info['base_price']
                            st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                            if uid not in em2["owner_counts"]:
                                em2["owner_counts"][uid] = {}
                            em2["owner_counts"][uid][eid] = em2["owner_counts"][uid].get(eid, 0) + 1
                            save_estate_market(em2)
                            log_tx(uid, "부동산매입", f"{info['name']} 신규 매입", -info['base_price'])
                            sync_user_data()
                            owned_types = sum(1 for e, c in st.session_state.real_estate.items() if c > 0)
                            if owned_types == len(estate_config):
                                claim_hidden_title("real_estate_monopoly", "👑 [유일무이] 진짜 부루마불 우승자")
                            st.success(f"✅ {info['name']} 매입 완료!")
                            st.rerun()
                        else:
                            st.error("잔액 부족!")

        st.write("---")
        st.markdown("### 🔄 유저 매물 (2차 시장)")
        st.caption("다른 유저가 판매 등록한 매물입니다. 판매자에게 대금이 지급됩니다.")

        user_listings = [l for l in em["listings"] if l["seller"] != uid]
        if not user_listings:
            st.info("현재 등록된 유저 매물이 없습니다.")
        else:
            listings_by_eid = {}
            for l in user_listings:
                listings_by_eid.setdefault(l["eid"], []).append(l)

            for eid, llist in listings_by_eid.items():
                info = estate_config.get(eid)
                if not info: continue
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
      <span style='color:#94A3B8;font-size:0.8rem;'>판매자: </span>
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
                            em3 = load_estate_market()
                            target = next((x for x in em3["listings"] if x["id"] == li["id"]), None)
                            if target is None:
                                st.error("⚠️ 이미 판매된 매물입니다.")
                            elif st.session_state.global_cash >= target["price"]:
                                set_cooldown(cd_key)
                                st.session_state.global_cash -= target["price"]
                                st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                                if uid not in em3["owner_counts"]:
                                    em3["owner_counts"][uid] = {}
                                em3["owner_counts"][uid][eid] = em3["owner_counts"][uid].get(eid, 0) + 1
                                seller = target["seller"]
                                us = load_db(USERS_FILE, {})
                                if seller in us:
                                    us[seller]['cash'] += target["price"]
                                    if seller not in em3["owner_counts"]:
                                        em3["owner_counts"][seller] = {}
                                    em3["owner_counts"][seller][eid] = max(0, em3["owner_counts"][seller].get(eid, 0) - 1)
                                    
                                    # 판매자 개인 보유 부동산 목록에서도 빼주기 (복사 버그 방지)
                                    if 'real_estate' in us[seller] and eid in us[seller]['real_estate']:
                                        us[seller]['real_estate'][eid] = max(0, us[seller]['real_estate'][eid] - 1)
                                        if us[seller]['real_estate'][eid] <= 0:
                                            del us[seller]['real_estate'][eid]
                                            
                                    save_db(USERS_FILE, us)
                                    log_tx(seller, "부동산판매", f"{info['name']} 판매 완료", target["price"])
                                em3["listings"] = [x for x in em3["listings"] if x["id"] != li["id"]]
                                save_estate_market(em3)
                                log_tx(uid, "부동산구매", f"{info['name']} 유저 매물 구매", -target["price"])
                                sync_user_data()
                                market['news'] = f"🏢 [{uid}] {info['name']} 유저 매물 구매 완료!"
                                save_market(market)
                                owned_types = sum(1 for e, c in st.session_state.real_estate.items() if c > 0)
                                if owned_types == len(estate_config):
                                    claim_hidden_title("real_estate_monopoly", "👑 [유일무이] 진짜 부루마불 우승자")
                                st.success(f"✅ {info['name']} 구매 완료! {format_korean_money(target['price'])}")
                                st.rerun()
                            else:
                                st.error("잔액 부족!")

    with tab_my_estate:
        owned_any = any(v > 0 for v in st.session_state.real_estate.values())
        if not owned_any:
            st.info("보유 중인 부동산이 없습니다. 마켓에서 매입하세요!")
        else:
            for eid, cnt in st.session_state.real_estate.items():
                if cnt <= 0 or eid not in estate_config: continue
                info = estate_config[eid]
                my_listed = sum(1 for l in em["listings"] if l["eid"] == eid and l["seller"] == uid)
                available_to_sell = cnt - my_listed
                st.markdown(f"""
<div class='estate-card'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='display:flex;align-items:center;gap:12px;'>
      <span style='font-size:2rem;'>{info['icon']}</span>
      <div>
        <div style='font-weight:900;font-size:1.05rem;color:#E2E8F0;'>{info['name']}</div>
        <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
        <div style='margin-top:4px;'>
          <span style='color:#94A3B8;font-size:0.82rem;'>보유 {cnt}채 (판매 등록 {my_listed}채)</span>
          <span style='color:#777;margin:0 8px;'>|</span>
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

    with tab_sell:
        st.markdown("### 📋 내 매물 판매 등록")
        st.caption("판매 등록 후 다른 유저가 구매하면 현금이 즉시 입금됩니다. 거래 수수료: 2%")

        sellable = [(eid, cnt) for eid, cnt in st.session_state.real_estate.items() if cnt > 0 and eid in estate_config]
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
                min_value=min_price, max_value=max_price, value=sel_info['base_price'], step=int(sel_info['base_price'] * 0.01), format="%d"
            )
            fee = int(sell_price * 0.02)
            net_receive = sell_price - fee
            st.caption(f"📌 판매 시 수수료 2% ({format_korean_money(fee)}) 공제 → 실수령 {format_korean_money(net_receive)}")

            cd_list_rem = cooldown_remaining("estate_list", 5.0)
            if cd_list_rem > 0:
                st.warning(f"⏱️ 등록 쿨다운 {cd_list_rem:.1f}초")
            elif st.button("📋 판매 등록하기", use_container_width=True):
                set_cooldown("estate_list")
                new_listing = {
                    "id": str(uuid.uuid4())[:8],
                    "eid": sel_eid, "seller": uid, "price": sell_price,
                    "net_receive": net_receive, "listed_time": time.time()
                }
                em_fresh = load_estate_market()
                em_fresh["listings"].append(new_listing)
                save_estate_market(em_fresh)
                market['news'] = f"🏢 [{uid}] {sel_info['name']} {format_korean_money(sell_price)}에 매물 등록!"
                save_market(market)
                st.success(f"✅ {sel_info['name']} 판매 등록 완료! 구매자 대기 중...")
                st.rerun()

        st.write("---")
        st.markdown("### 🗂️ 내 등록 매물 관리")
        my_listings = [l for l in em["listings"] if l["seller"] == uid]
        if not my_listings:
            st.info("현재 등록된 매물이 없습니다.")
        else:
            for li in my_listings:
                info = estate_config.get(li["eid"], {})
                listed_dt = datetime.fromtimestamp(li.get("listed_time", 0), KST).strftime("%m/%d %H:%M")
                c1, c2 = st.columns([5, 2])
                with c1:
                    st.markdown(f"""
<div class='my-listing'>
  <div style='display:flex;justify-content:space-between;'>
    <div>
      <span style='font-size:1.2rem;'>{info.get('icon','🏠')}</span>
      <b style='color:#E2E8F0;margin-left:8px;'>{info.get('name','?')}</b>
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
                        st.rerun()

# =====================================================================
# 🏦 은행 (대출/송금)
# =====================================================================
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
        _all_users = [u for u in load_db(USERS_FILE, {}).keys() if u != st.session_state.logged_in_user and u != "admin"]
        target = st.selectbox("받는 분 선택", _all_users) if _all_users else None
        if not _all_users:
            st.info("송금 가능한 다른 유저가 없습니다.")
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
                
                us_fresh = load_db(USERS_FILE, {})
                if st.session_state.global_cash < amt:
                    st.error("잔액이 부족합니다. (재검증 실패)")
                else:
                    st.session_state.global_cash -= amt
                    us_fresh[target]['cash'] += amt
                    us_fresh[st.session_state.logged_in_user]['cash'] = st.session_state.global_cash
                    save_db(USERS_FILE, us_fresh)
                    log_tx(st.session_state.logged_in_user, "송금", f"{target}에게 송금", -amt)
                    log_tx(target, "송금수신", f"{st.session_state.logged_in_user}에게서 수신", amt)
                    sync_user_data()
                    st.success(f"✅ {target}님께 {format_korean_money(amt)} 송금 완료!")
                    if amt >= 10_000_000_000:
                        claim_hidden_title("first_donate_10b", "👑 [유일무이] 자선사업가")
                    st.rerun()
            

    with tab_loan:
        if st.session_state.equipped_title == "💸 신용불량자":
            st.error("🚨 신용불량자 상태에서는 추가 대출이 불가능합니다. 먼저 기존 대출을 상환하세요.")
            avail_loan = 0
            max_loan_limit = 0
        else:
            max_loan_limit = max(100_000_000, int(nw * 0.5))
            avail_loan = max(0, max_loan_limit - st.session_state.loan)

        st.info(f"💡 최대 대출 한도: {format_korean_money(max_loan_limit)} (순자산의 50%)\n💸 현재 대출 가능액: {format_korean_money(avail_loan)}\n⚠️ 대출 실행 시 1%의 선취 수수료가 공제됩니다.")
        
        if avail_loan > 0:
            JS_MAX_INT = 9007199254740991
            safe_max_loan = min(int(avail_loan), JS_MAX_INT)

            l_amt = st.number_input("대출 금액 (원)", min_value=0, max_value=safe_max_loan, step=10_000_000, format="%d", key="loan_in_safe")
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
                    if st.session_state.loan >= 100_000_000_000_000:
                        claim_hidden_title("first_loan_100b", "👑 [유일무이] 갚아도 갚아도 끝이 없는 인생")
                    st.rerun()
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
                sync_user_data();  
                if st.session_state.global_cash == 0 and actual > 0:
                    claim_hidden_title("perfect_zero_cash", "👑 [유일무이] 완벽한 무소유")
                st.rerun()
            else:
                st.error("잔액 부족 또는 상환 금액 오류")

# =====================================================================
# ⚔️ 글로벌 로또
# =====================================================================
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
            u_db_check = load_db(USERS_FILE, {})
            db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
            if db_cash < cost:
                st.error("잔액 부족! (DB 검증 실패)")
            else:
                st.session_state.global_cash -= cost
                market['lotto_pool']    += cost
                market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt
                save_market(market)
                log_tx(st.session_state.logged_in_user, "로또", f"로또 {b_cnt}장 구매", -cost)
                sync_user_data()
                st.success(f"✅ {b_cnt}장 구매 완료!")
                st.rerun()
        else:
            st.error("잔액 부족!")

    if market['lotto_tickets']:
        st.write("---")
        st.markdown("### 👥 현재 참여자")
        sorted_t = sorted(market['lotto_tickets'].items(), key=lambda x: x[1], reverse=True)
        for uid_l, cnt in sorted_t[:10]:
            pct     = cnt / total_tickets * 100
            me_mark = " 👈" if uid_l == st.session_state.logged_in_user else ""
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'><span style='color:#94A3B8;'>{uid_l}{me_mark}</span><span style='color:#FF00FF;font-weight:900;'>{cnt}장 ({pct:.1f}%)</span></div>", unsafe_allow_html=True)

    

# =====================================================================
# ⚽ 구단주 시뮬레이터
# =====================================================================
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
  <div style='color:#777;font-size:0.78rem;letter-spacing:2px;margin-bottom:16px;'>{stadium}</div>
  <div style='display:flex;justify-content:space-around;align-items:center;'>
    <div><div class='team-label'>{my_team}</div><div style='color:#888;font-size:0.78rem;'>{my_form}</div></div>
    <div><div class='score-number'>{h_score} : {a_score}</div><div class='match-time'>⏱ {real_min}' / 90'</div></div>
    <div><div class='team-label'>{opp_team}</div><div style='color:#888;font-size:0.78rem;'>{opp_form}</div></div>
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
            st.rerun()

# =====================================================================
# ⚽ 조기축구 승부차기 (심리전)
# =====================================================================
elif menu == "⚽ 조기축구 승부차기":
    st.title("⚽ 조기축구 승부차기")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>키커와 골키퍼의 피 말리는 심리전! 5판 3선승제로 승부합니다.</div>", unsafe_allow_html=True)

    # --- 초기 상태 세팅 ---
    if 'ps_state' not in st.session_state:
        st.session_state.update({
            'ps_state': 'betting',     # betting, playing, done
            'ps_bet': 0,
            'ps_round': 1,             # 1 ~ 5 라운드
            'ps_turn': 'kicker',       # 유저 기준 'kicker'(공격) or 'keeper'(수비)
            'ps_my_score': 0,
            'ps_ai_score': 0,
            'ps_logs': []              # 경기 중계 로그
        })

    state = st.session_state.ps_state

    # ── 베팅 화면 ──
    if state == 'betting':
        st.markdown(f"""
        <div style='text-align:center;padding:30px;background:linear-gradient(135deg,rgba(0,255,136,0.1),rgba(0,100,50,0.15));
             border:2px solid rgba(0,255,136,0.3);border-radius:18px;margin-bottom:24px;'>
          <div style='font-size:4rem;'>🥅</div>
          <div style='font-family:Orbitron,monospace;font-size:1.3rem;color:#00FF88;margin-top:8px;font-weight:900;'>PENALTY SHOOTOUT</div>
          <div style='color:#888;margin-top:10px;font-size:0.88rem;'>승리 시 베팅금의 2배 획득! (무승부 시 원금 반환)</div>
        </div>
        """, unsafe_allow_html=True)
        
        bet = st.number_input("베팅 금액 (원)", min_value=1_000_000, step=1_000_000, value=1_000_000, format="%d", key="ps_bet_input")
        st.caption(f"💵 베팅 예정: {format_korean_money(bet)} | 잔액: {format_korean_money(st.session_state.global_cash)}")
        
        if st.button("⚽ 승부차기 시작!", use_container_width=True):
            if st.session_state.global_cash < bet:
                st.error("잔액이 부족합니다!")
            else:
                # 베팅금 차감 및 상태 변경
                st.session_state.global_cash -= bet
                st.session_state.ps_bet = bet
                st.session_state.ps_state = 'playing'
                st.session_state.ps_round = 1
                st.session_state.ps_turn = 'kicker'
                st.session_state.ps_my_score = 0
                st.session_state.ps_ai_score = 0
                st.session_state.ps_logs = []
                sync_user_data()
                st.rerun()

    # ── 플레이 및 결과 화면 ──
    elif state in ['playing', 'done']:
        my_score = st.session_state.ps_my_score
        ai_score = st.session_state.ps_ai_score
        current_round = st.session_state.ps_round
        turn = st.session_state.ps_turn
        logs = st.session_state.ps_logs

        # 스코어 보드
        st.markdown(f"""
        <div class='scoreboard'>
          <div style='color:#777;font-size:0.9rem;letter-spacing:2px;margin-bottom:12px;'>🏆 조기축구 결승전 승부차기</div>
          <div style='display:flex;justify-content:space-around;align-items:center;'>
            <div><div class='team-label'>{st.session_state.logged_in_user} (나)</div></div>
            <div>
              <div class='score-number' style='color:#FFD600;'>{my_score} : {ai_score}</div>
              <div class='match-time'>Round {min(current_round, 5)} / 5</div>
            </div>
            <div><div class='team-label'>동네 라이벌 (AI)</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        if state == 'playing':
            # 플레이어 입력 UI
            if turn == 'kicker':
                st.markdown("<h3 style='text-align:center; color:#FF4B4B;'>🔥 당신은 키커입니다! 슛 방향을 선택하세요!</h3>", unsafe_allow_html=True)
                btn_labels = ["◀️ 좌측으로 슛", "⏺️ 중앙 꽂기", "▶️ 우측으로 슛"]
            else:
                st.markdown("<h3 style='text-align:center; color:#4B9EFF;'>🧤 당신은 골키퍼입니다! 다이빙 방향을 예측하세요!</h3>", unsafe_allow_html=True)
                btn_labels = ["◀️ 좌측 다이빙", "⏺️ 중앙 대기", "▶️ 우측 다이빙"]

            dirs = ["Left", "Center", "Right"]
            c1, c2, c3 = st.columns(3)
            
            # 사용자 선택 처리 함수
            def process_turn(my_choice):
                ai_choice = random.choice(dirs)
                
                if turn == 'kicker':
                    # 내가 키커일 때: 내 슛 방향 != AI 다이빙 방향 이면 골!
                    if my_choice != ai_choice:
                        st.session_state.ps_my_score += 1
                        logs.insert(0, f"✅ [Round {current_round}] <b>나(공격)</b>: {my_choice} 슛! / AI(수비): {ai_choice} 다이빙 ➔ <span style='color:#00FF88;'>GOAL!! ⚽</span>")
                    else:
                        logs.insert(0, f"❌ [Round {current_round}] <b>나(공격)</b>: {my_choice} 슛! / AI(수비): {ai_choice} 다이빙 ➔ <span style='color:#FF4B4B;'>막혔습니다!! 🧤</span>")
                    # 다음은 수비 턴
                    st.session_state.ps_turn = 'keeper'
                    
                else:
                    # 내가 수비일 때: 내 다이빙 방향 == AI 슛 방향 이면 선방!
                    if my_choice == ai_choice:
                        logs.insert(0, f"✅ [Round {current_round}] AI(공격): {ai_choice} 슛! / <b>나(수비)</b>: {my_choice} 다이빙 ➔ <span style='color:#00FF88;'>슈퍼 세이브!! 🧤</span>")
                    else:
                        st.session_state.ps_ai_score += 1
                        logs.insert(0, f"❌ [Round {current_round}] AI(공격): {ai_choice} 슛! / <b>나(수비)</b>: {my_choice} 다이빙 ➔ <span style='color:#FF4B4B;'>실점했습니다... ⚽</span>")
                    
                    # 수비 턴이 끝나면 라운드 증가 및 공격 턴으로
                    st.session_state.ps_turn = 'kicker'
                    st.session_state.ps_round += 1

                # 5라운드 턴까지 다 돌았거나 남은 기회로 역전 불가능할 때 게임 종료 처리 가능
                # (여기서는 심플하게 무조건 5라운드 끝까지 차는 것으로 구현)
                if st.session_state.ps_round > 5:
                    st.session_state.ps_state = 'done'

            # 버튼 UI
            if c1.button(btn_labels[0], use_container_width=True):
                process_turn("Left"); st.rerun()
            if c2.button(btn_labels[1], use_container_width=True):
                process_turn("Center"); st.rerun()
            if c3.button(btn_labels[2], use_container_width=True):
                process_turn("Right"); st.rerun()

        else: # state == 'done'
            bet = st.session_state.ps_bet
            if my_score > ai_score:
                result_txt, result_col, prize = "🎉 승리! 상금을 획득합니다!", "#00FF88", bet * 2
            elif my_score == ai_score:
                result_txt, result_col, prize = "🤝 치열한 접전 끝 무승부! 원금 반환", "#888888", bet
            else:
                result_txt, result_col, prize = "😢 패배... 베팅금을 잃었습니다.", "#FF4B4B", 0

            net = prize - bet
            net_str = f"+{format_korean_money(net)}" if net > 0 else f"-{format_korean_money(abs(net))}" if net < 0 else "베팅금 반환"
            
            st.markdown(f"""
            <div style='text-align:center;background:rgba(0,0,0,0.4);border:2px solid {result_col};
                 border-radius:18px;padding:28px;margin:20px 0;box-shadow:0 0 30px {result_col}44;'>
              <div style='font-size:1.8rem;font-weight:900;color:{result_col};'>{result_txt}</div>
              <div style='font-size:1.3rem;font-weight:900;margin-top:10px;'>{net_str}</div>
              <div style='color:#888;font-size:0.8rem;margin-top:8px;'>지급액: {format_korean_money(prize)}</div>
            </div>
            """, unsafe_allow_html=True)

            # 정산은 최초 한 번만
            if 'ps_paid' not in st.session_state:
                st.session_state.ps_paid = True
                if prize > 0:
                    st.session_state.global_cash += prize
                    if bet >= 10_000_000_000:
                        claim_hidden_title("penalty_master", "👑 [유일무이] 거미손")
                    
                # 거래 기록 로그 남기기
                if net > 0:
                    log_tx(st.session_state.logged_in_user, "승부차기", "승부차기 승리", net)
                elif net < 0:
                    log_tx(st.session_state.logged_in_user, "승부차기", "승부차기 패배", net)
                    
                sync_user_data()

            if st.button("🔄 다시 하기", use_container_width=True):
                for k in ['ps_state','ps_bet','ps_round','ps_turn','ps_my_score','ps_ai_score','ps_logs','ps_paid']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

        # 중계 로그 출력
        if logs:
            st.write("---")
            st.markdown("#### 📡 실시간 중계 기록")
            for log in logs:
                st.markdown(f"<div class='commentary-item'>{log}</div>", unsafe_allow_html=True)

# =====================================================================
# 💻 정처기 CBT
# =====================================================================
elif menu == "💻 정처기 CBT":
    st.title("💻 정보처리기사 실전 CBT")
    st.caption("실제 정처기 수준의 문제입니다. 정답 시 50만원 지급!")

    # 👇 이 아래부터 덮어쓰기 시작 👇
    QUESTION_POOL = [
        {"q": "함수 종속에서 X → Y 의미는?", "a": "X 값이 Y를 결정", "w": ["Y가 X 결정","서로 독립","무관"], "cat": "데이터베이스"},
        {"q": "정규화 목적은?", "a": "데이터 중복 최소화", "w": ["속도 향상","보안 강화","암호화"], "cat": "데이터베이스"},
        {"q": "카디널리티 의미는?", "a": "튜플 수", "w": ["속성 수","키 수","인덱스 수"], "cat": "데이터베이스"},
        {"q": "차수(Degree)는?", "a": "속성 수", "w": ["튜플 수","키 수","인덱스"], "cat": "데이터베이스"},
        {"q": "후보키 특징은?", "a": "유일성+최소성", "w": ["유일성만","최소성만","중복 허용"], "cat": "데이터베이스"},
        {"q": "기본키 특징은?", "a": "NULL 불가", "w": ["중복 허용","여러 개 필수","변경 불가"], "cat": "데이터베이스"},
        {"q": "외래키 역할은?", "a": "참조 무결성 유지", "w": ["속도 향상","정렬","암호화"], "cat": "데이터베이스"},
        {"q": "트랜잭션 COMMIT 의미는?", "a": "영구 반영", "w": ["취소","대기","삭제"], "cat": "데이터베이스"},
        {"q": "ROLLBACK 의미는?", "a": "작업 취소", "w": ["반영","저장","병합"], "cat": "데이터베이스"},
        {"q": "뷰(View) 장점은?", "a": "보안성 향상", "w": ["속도 증가","저장 공간 증가","정렬"], "cat": "데이터베이스"},

        {"q": "프로세스 상태 중 실행 상태는?", "a": "CPU 사용 중", "w": ["대기","생성","종료"], "cat": "운영체제"},
        {"q": "스레드 장점은?", "a": "경량 프로세스", "w": ["무겁다","독립 메모리","느림"], "cat": "운영체제"},
        {"q": "문맥교환 의미는?", "a": "CPU 상태 전환", "w": ["메모리 삭제","파일 저장","네트워크 연결"], "cat": "운영체제"},
        {"q": "데드락 해결 중 회피는?", "a": "안전 상태 유지", "w": ["무시","강제 종료","롤백"], "cat": "운영체제"},
        {"q": "페이징 단위는?", "a": "페이지", "w": ["세그먼트","블록","파일"], "cat": "운영체제"},

        {"q": "IP 클래스 A 범위 시작은?", "a": "0", "w": ["128","192","224"], "cat": "네트워크"},
        {"q": "서브넷 목적은?", "a": "네트워크 분할", "w": ["속도 감소","보안 약화","주소 제거"], "cat": "네트워크"},
        {"q": "FTP 포트는?", "a": "21", "w": ["80","443","25"], "cat": "네트워크"},
        {"q": "SMTP 역할은?", "a": "메일 송신", "w": ["수신","라우팅","DNS"], "cat": "네트워크"},
        {"q": "POP3 역할은?", "a": "메일 수신", "w": ["송신","DNS","라우팅"], "cat": "네트워크"},

        {"q": "정렬 알고리즘 중 안정 정렬은?", "a": "버블 정렬", "w": ["퀵 정렬","힙 정렬","선택 정렬"], "cat": "알고리즘"},
        {"q": "힙 특징은?", "a": "완전 이진 트리", "w": ["그래프","리스트","배열"], "cat": "자료구조"},
        {"q": "해시 충돌 해결 방법은?", "a": "체이닝", "w": ["정렬","삭제","병합"], "cat": "자료구조"},
        {"q": "그래프 간선 수 의미는?", "a": "연결 수", "w": ["노드 수","트리 수","경로"], "cat": "자료구조"},
        {"q": "큐 활용 예는?", "a": "프린터 대기열", "w": ["재귀","정렬","검색"], "cat": "자료구조"},

        {"q": "팩토리 패턴 목적은?", "a": "객체 생성 캡슐화", "w": ["삭제","정렬","압축"], "cat": "디자인패턴"},
        {"q": "전략 패턴 특징은?", "a": "알고리즘 교체", "w": ["고정","삭제","압축"], "cat": "디자인패턴"},
        {"q": "어댑터 패턴은?", "a": "인터페이스 변환", "w": ["생성","삭제","정렬"], "cat": "디자인패턴"},

        {"q": "폭포수 모델 단점은?", "a": "변경 어려움", "w": ["유연함","빠름","반복"], "cat": "소프트웨어공학"},
        {"q": "스크럼 역할 중 제품 책임자는?", "a": "PO", "w": ["SM","개발자","QA"], "cat": "소프트웨어공학"},
        {"q": "유스케이스 다이어그램 목적은?", "a": "사용자 요구 표현", "w": ["코드 작성","DB 설계","테스트"], "cat": "소프트웨어공학"},

        {"q": "악성코드 중 자기 복제는?", "a": "웜", "w": ["트로이목마","스파이웨어","랜섬웨어"], "cat": "보안"},
        {"q": "랜섬웨어 특징은?", "a": "금전 요구", "w": ["삭제만","속도 증가","백업"], "cat": "보안"},
        {"q": "SSL 역할은?", "a": "암호화 통신", "w": ["라우팅","DNS","파일 전송"], "cat": "보안"},

        {"q": "HTTP 상태코드 200 의미는?", "a": "성공", "w": ["오류","리다이렉트","서버 오류"], "cat": "웹"},
        {"q": "404 의미는?", "a": "페이지 없음", "w": ["성공","서버 오류","리다이렉트"], "cat": "웹"},
        {"q": "REST 특징은?", "a": "자원 기반", "w": ["상태 유지","고정","비표준"], "cat": "웹"},
        {"q": "ERD에서 관계(Relationship)의 의미는?", "a": "엔터티 간 연관", "w": ["속성","키","도메인"], "cat": "데이터베이스"},
        {"q": "도메인(Domain)의 의미는?", "a": "속성 값 범위", "w": ["테이블","키","레코드"], "cat": "데이터베이스"},
        {"q": "무결성 제약 조건의 목적은?", "a": "데이터 정확성 유지", "w": ["속도 증가","압축","삭제"], "cat": "데이터베이스"},
        {"q": "CHECK 제약 조건은?", "a": "조건 만족 데이터만 허용", "w": ["NULL 허용","중복 허용","삭제"], "cat": "데이터베이스"},
        {"q": "UNIQUE 제약 조건은?", "a": "중복 방지", "w": ["NULL 금지","삭제","정렬"], "cat": "데이터베이스"},

        {"q": "프로세스 생성 함수는?", "a": "fork()", "w": ["exec()","exit()","wait()"], "cat": "운영체제"},
        {"q": "exec() 역할은?", "a": "프로그램 교체 실행", "w": ["생성","종료","대기"], "cat": "운영체제"},
        {"q": "임계구역 문제 해결 조건은?", "a": "상호배제", "w": ["중복 허용","비동기","랜덤"], "cat": "운영체제"},
        {"q": "뮤텍스 특징은?", "a": "상호배제 락", "w": ["동시 실행","비동기","큐"], "cat": "운영체제"},
        {"q": "스케줄링 중 RR 특징은?", "a": "순환 할당", "w": ["우선순위 고정","비선점","단일"], "cat": "운영체제"},

        {"q": "라우팅 프로토콜 예는?", "a": "RIP", "w": ["HTTP","FTP","SMTP"], "cat": "네트워크"},
        {"q": "게이트웨이 역할은?", "a": "네트워크 간 연결", "w": ["증폭","저장","삭제"], "cat": "네트워크"},
        {"q": "허브 특징은?", "a": "브로드캐스트", "w": ["필터링","라우팅","암호화"], "cat": "네트워크"},
        {"q": "스위치 특징은?", "a": "MAC 기반 전달", "w": ["IP 기반","암호화","라우팅"], "cat": "네트워크"},
        {"q": "ICMP 역할은?", "a": "오류 메시지", "w": ["파일 전송","메일","DNS"], "cat": "네트워크"},

        {"q": "삽입 정렬 특징은?", "a": "부분 정렬 활용", "w": ["완전 랜덤","트리","그래프"], "cat": "알고리즘"},
        {"q": "선택 정렬 특징은?", "a": "최솟값 선택", "w": ["재귀","트리","그래프"], "cat": "알고리즘"},
        {"q": "병합 정렬 특징은?", "a": "분할 정복", "w": ["그리디","완전탐색","랜덤"], "cat": "알고리즘"},
        {"q": "힙 정렬 특징은?", "a": "힙 구조 사용", "w": ["리스트","그래프","큐"], "cat": "알고리즘"},
        {"q": "이진 트리 특징은?", "a": "최대 2개 자식", "w": ["3개","무한","0개"], "cat": "자료구조"},

        {"q": "브리지 패턴은?", "a": "추상과 구현 분리", "w": ["생성","삭제","정렬"], "cat": "디자인패턴"},
        {"q": "커맨드 패턴은?", "a": "요청 캡슐화", "w": ["삭제","정렬","압축"], "cat": "디자인패턴"},
        {"q": "템플릿 메서드 패턴은?", "a": "알고리즘 구조 정의", "w": ["삭제","압축","정렬"], "cat": "디자인패턴"},

        {"q": "형상관리 목적은?", "a": "변경 추적", "w": ["삭제","압축","정렬"], "cat": "소프트웨어공학"},
        {"q": "테스트 종류 중 단위 테스트는?", "a": "모듈 단위", "w": ["시스템","통합","인수"], "cat": "소프트웨어공학"},
        {"q": "통합 테스트 목적은?", "a": "모듈 간 인터페이스 검증", "w": ["단일","사용자","배포"], "cat": "소프트웨어공학"},

        {"q": "방화벽 역할은?", "a": "접근 제어", "w": ["암호화","저장","삭제"], "cat": "보안"},
        {"q": "IDS 역할은?", "a": "침입 탐지", "w": ["차단","삭제","압축"], "cat": "보안"},
        {"q": "IPS 역할은?", "a": "침입 차단", "w": ["탐지","저장","압축"], "cat": "보안"},

        {"q": "쿠키 특징은?", "a": "클라이언트 저장", "w": ["서버 저장","암호화","삭제"], "cat": "웹"},
        {"q": "세션 특징은?", "a": "서버 저장", "w": ["클라이언트","파일","삭제"], "cat": "웹"},
        {"q": "AJAX 특징은?", "a": "비동기 통신", "w": ["동기","정적","삭제"], "cat": "웹"}
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
            sync_user_data(); st.rerun()

    if st.button("🔄 다른 문제", use_container_width=True):
        for k in ['cbt_q', 'cbt_opts']:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

# =====================================================================
# 🏎️ 하이퍼카 레이싱 (역배당/부스터 패치 + 내 차량 연동)
# =====================================================================
elif menu == "🏎️ 하이퍼카 레이싱":
    st.title("🏎️ 하이퍼카 레이싱")
    st.caption("배당률이 높을수록 우승 확률은 낮지만 당첨 시 고수익! 내 차를 출전시키면 튜닝 스탯이 반영됩니다.")

    CARS = [
        {"name": "부가티 시론 SS",        "emoji": "🏎️", "odds": 20.0, "spd": (0, 15),  "color": "#FF0066"},
        {"name": "람보르기니 레부엘토",    "emoji": "🐂",  "odds": 12.0, "spd": (1, 14),  "color": "#FF6600"},
        {"name": "페라리 SF90 XX",         "emoji": "🐎",  "odds": 8.0,  "spd": (1, 13),  "color": "#FF2200"},
        {"name": "맥라렌 P1 GTR",          "emoji": "🚀",  "odds": 6.0,  "spd": (2, 12),  "color": "#FF9900"},
        {"name": "포르쉐 918 스파이더",    "emoji": "⚡",  "odds": 4.0,  "spd": (2, 11),  "color": "#FFCC00"},
        {"name": "테슬라 로드스터 2",       "emoji": "⚡",  "odds": 2.5,  "spd": (3, 10),  "color": "#00FF88"},
        {"name": "토요타 GR010 하이브리드","emoji": "🏁",  "odds": 1.8,  "spd": (3,  9),  "color": "#00CCFF"},
    ]

    # 유저의 차고지 데이터 불러오기
    uid = st.session_state.logged_in_user
    _tmp = load_db(USERS_FILE, {})
    my_garage = _tmp.get(uid, {}).get('garage', {})
    active_t = my_garage.get('active_tier')

    my_custom_car = None
    if active_t is not None and active_t in my_garage.get('cars', {}):
        parts = my_garage['cars'][active_t]
        
        if parts.get('needs_repair'):
            st.warning("🚨 현재 선택된 내 차량이 파손된 상태라 레이싱에 출전할 수 없습니다. 차고지에서 수리하세요!")
        else:
            # 티어별 기본 스탯 정의
            CAR_TIERS_INFO = [
                {"name": "박스카", "emoji": "🚙", "color": "#A0A0A0", "base_spd": (1, 10), "base_odds": 15.0},
                {"name": "스포츠 세단", "emoji": "🚗", "color": "#00E5FF", "base_spd": (2, 12), "base_odds": 8.0},
                {"name": "럭셔리 하이퍼카", "emoji": "🏎️", "color": "#FFD600", "base_spd": (3, 13), "base_odds": 4.0},
                {"name": "은하철도", "emoji": "🚀", "color": "#FF00FF", "base_spd": (4, 15), "base_odds": 1.5}
            ]
            
            c_info = CAR_TIERS_INFO[int(active_t)]
            total_lv = parts['engine_lv'] + parts['suspension_lv'] + parts['bumper_lv']
            
            # 튜닝 레벨이 높을수록 최고 속도가 올라가고, 배당률은 살짝 낮아짐 (안정적인 우승)
            bonus_spd = total_lv // 2
            calc_odds = round(max(1.1, c_info['base_odds'] - (total_lv * 0.2)), 1)

            my_custom_car = {
                "name": f"[내 차] {c_info['name']} (+{total_lv}강)",
                "emoji": c_info['emoji'],
                "odds": calc_odds,
                "spd": (c_info['base_spd'][0], c_info['base_spd'][1] + bonus_spd),
                "color": c_info['color'],
                "is_mine": True
            }
            CARS.insert(0, my_custom_car) # 리스트 맨 앞에 내 차 추가

    car_names = [f"{c['emoji']} {c['name']} ({c['odds']}배)" for c in CARS]
    sel_idx   = st.selectbox("베팅 및 출전 차량 선택", range(len(CARS)), format_func=lambda i: car_names[i])
    selected_car = CARS[sel_idx]
    
    bet_amt   = st.number_input("베팅 금액 (원)", min_value=10_000, step=10_000, value=100_000)
    st.caption(f"우승 시 예상 수령액: {format_korean_money(int(bet_amt * selected_car['odds']))}")

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
                    base_move = random.randint(c['spd'][0], c['spd'][1])
                    if random.random() < 0.05:
                        base_move += 15 # 부스터 터짐!
                        
                    positions[c['name']] = min(100, positions[c['name']] + base_move)
                    
                    rank     = sorted(positions.items(), key=lambda x: x[1], reverse=True)
                    pos_num  = next(i+1 for i, (n, _) in enumerate(rank) if n == c['name'])
                    bars[c['name']].progress(positions[c['name']]/100, text=f"{c['emoji']} {c['name']} {pos_num}위 | {positions[c['name']]:.0f}%")
                    if positions[c['name']] >= 100 and winner is None:
                        winner = c['name']

            st.write("---")
            winner_car = next(c for c in CARS if c['name'] == winner)
            st.markdown(f"<div style='text-align:center;font-family:Orbitron,monospace;font-size:1.8rem;color:{winner_car['color']};font-weight:900;padding:20px;'>🏆 {winner_car['emoji']} {winner} 우승!</div>", unsafe_allow_html=True)

            if winner == selected_car['name']:
                prize = int(bet_amt * selected_car['odds'])
                st.session_state.global_cash += prize
                log_tx(st.session_state.logged_in_user, "레이싱", f"{selected_car['name']} 승리", prize - bet_amt)
                st.success(f"🎉 베팅 성공! +{format_korean_money(prize)}"); st.balloons()
                if selected_car['odds'] >= 20.0:
                    claim_hidden_title("first_bugatti", "👑 [유일무이] 레이싱 붉은 혜성")
            else:
                log_tx(st.session_state.logged_in_user, "레이싱", f"{selected_car['name']} 패배", -bet_amt)
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")
                
                # 내 차를 직접 출전시켰는데 졌을 경우, 10% 확률로 차량 파손 페널티!
                if selected_car.get('is_mine') and random.random() < 0.1:
                    u_db = load_db(USERS_FILE, {})
                    u_db[uid]['garage']['cars'][active_t]['needs_repair'] = True
                    save_db(USERS_FILE, u_db)
                    st.error("🚨 쾅!! 무리한 주행으로 인해 내 차량이 대파되었습니다! 차고지에서 수리해야 합니다.")

            sync_user_data(); st.rerun()

# =====================================================================
# 🎰 럭키 슬롯
# =====================================================================
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
  <div style='color:#888;font-size:0.78rem;margin-top:4px;'>💎=3개 잭팟, 같은 기호 3개=고배당, 2개=소배당</div>
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
            u_db_check = load_db(USERS_FILE, {})
            db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
            if db_cash < tier['cost']:
                st.error("잔액 부족! (DB 검증 실패)")
            else:
                st.session_state.global_cash -= tier['cost']
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
                    if sel_tier == 0: 
                        claim_hidden_title("first_slot_jackpot", "👑 [유일무이] 기적을 부르는 유저")
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

                sync_user_data(); st.rerun()

# =====================================================================
# 🃏 블랙잭 카지노
# =====================================================================
elif menu == "🃏 블랙잭 카지노":
    st.title("🃏 블랙잭 카지노")

    CARD_VALS = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
    SUITS = ['♠','♥','♦','♣']

    def bj_make_deck():
        deck = [(rank, suit) for rank in CARD_VALS for suit in SUITS] * 6
        random.shuffle(deck); return deck

    def bj_value(hand):
        val  = sum(CARD_VALS[r] for r, s in hand)
        aces = sum(1 for r, s in hand if r == 'A')
        while val > 21 and aces:
            val -= 10; aces -= 1
        return val

    def bj_render(hand, hide_second=False):
        parts = []
        for i, (r, s) in enumerate(hand):
            if i == 1 and hide_second:
                parts.append("<span style='font-size:2.2rem;background:#222;border:2px solid #555;padding:6px 10px;border-radius:8px;margin:3px;display:inline-block;'>🂠</span>")
            else:
                col = "color:#FF4B4B;" if s in ['♥','♦'] else "color:#1a1a1a;"
                parts.append(f"<span style='font-size:1.5rem;font-weight:900;background:#fff;{col}padding:6px 12px;border-radius:8px;margin:3px;display:inline-block;box-shadow:0 2px 8px rgba(0,0,0,0.4);'>{r}{s}</span>")
        return " ".join(parts)

    def bj_dealer_play(dealer, deck):
        while bj_value(dealer) < 17:
            dealer.append(deck.pop())
        return dealer, deck

    # 초기화
    if 'bj_state' not in st.session_state:
        st.session_state.update({
            'bj_state': 'betting', 'bj_deck': bj_make_deck(),
            'bj_player': [], 'bj_dealer': [], 'bj_bet': 0, 
        })

    state = st.session_state.bj_state

    # ── 베팅 화면 ──
    if state == 'betting':
        st.markdown(f"""
        <div style='text-align:center;padding:30px;background:linear-gradient(135deg,rgba(180,0,0,0.15),rgba(0,100,0,0.15));
             border:2px solid rgba(255,215,0,0.3);border-radius:18px;margin-bottom:24px;'>
          <div style='font-size:4rem;'>🃏</div>
          <div style='font-family:Orbitron,monospace;font-size:1.3rem;color:#FFD600;margin-top:8px;font-weight:900;'>BLACKJACK</div>
          <div style='color:#888;margin-top:10px;font-size:0.88rem;'>블랙잭(A+10) = 베팅의 1.5배 추가 지급 &nbsp;|&nbsp; 딜러 16 이하 히트</div>
        </div>
        """, unsafe_allow_html=True)
        
        bet = st.number_input("베팅 금액 (원)", min_value=1_000_000, step=1_000_000, value=1_000_000, format="%d", key="bj_bet_input")
        st.caption(f"💵 베팅 예정: {format_korean_money(bet)} | 잔액: {format_korean_money(st.session_state.global_cash)}")
        
        cd_deal = cooldown_remaining("bj_deal", 1.0)
        if cd_deal > 0:
            st.warning(f"⏱️ {cd_deal:.1f}초 후 딜 가능")
        elif st.button("🃏 카드 딜!", use_container_width=True):
            if st.session_state.global_cash < bet:
                st.error("잔액 부족!")
            else:
                set_cooldown("bj_deal")
                st.session_state.global_cash -= bet
                st.session_state.bj_bet = bet
                deck = st.session_state.bj_deck if len(st.session_state.bj_deck) > 30 else bj_make_deck()
                player = [deck.pop(), deck.pop()]
                dealer = [deck.pop(), deck.pop()]
                st.session_state.bj_player = player
                st.session_state.bj_dealer = dealer
                st.session_state.bj_deck   = deck
                
                
                if bj_value(player) == 21:
                    dl, dk = bj_dealer_play(dealer, deck)
                    st.session_state.bj_dealer = dl
                    st.session_state.bj_deck   = dk
                    st.session_state.bj_state  = 'done'
                else:
                    st.session_state.bj_state  = 'playing'
                sync_user_data()
                st.rerun()

    # ── 플레이 화면 ──
    elif state in ['playing', 'done']:
        player = st.session_state.bj_player
        dealer = st.session_state.bj_dealer
        bet    = st.session_state.bj_bet
        pval   = bj_value(player)

        st.markdown("### 🎩 딜러의 패")
        if state == 'playing':
            dv_shown = bj_value([dealer[0]])
            st.markdown(f"{bj_render(dealer, hide_second=True)}", unsafe_allow_html=True)
            st.caption(f"딜러 공개 패: {dv_shown}점 + ?")
        else:
            dval = bj_value(dealer)
            dcol = "#FF4B4B" if dval > 21 else "#fff"
            st.markdown(f"{bj_render(dealer)} <span style='color:{dcol};font-size:1.1rem;font-weight:900;margin-left:12px;'>{dval}점{'  💥BUST' if dval>21 else ''}</span>", unsafe_allow_html=True)
        st.write("")

        st.markdown("### 🎴 내 패")
        pcol = "#FF4B4B" if pval > 21 else "#00FF88" if pval == 21 else "#fff"
        st.markdown(f"{bj_render(player)} <span style='color:{pcol};font-size:1.2rem;font-weight:900;margin-left:12px;'>{pval}점{'  💥BUST' if pval>21 else '  🃏BJ!' if pval==21 and len(player)==2 else ''}</span>", unsafe_allow_html=True)
        st.write("")

        c_bet, c_pot = st.columns(2)
        c_bet.metric("💰 베팅", format_korean_money(bet))
        c_pot.metric("🏆 승리 시 지급", format_korean_money(bet * 2))

        if state == 'playing':
            st.write("")
            c1, c2 = st.columns(2)
            
            with c1:
                if st.button("👊 히트 (Hit)", use_container_width=True):
                    deck = st.session_state.bj_deck
                    st.session_state.bj_player.append(deck.pop())
                    st.session_state.bj_deck = deck
                    new_val = bj_value(st.session_state.bj_player)
                    if new_val >= 21:
                        if new_val == 21:
                            dl, dk = bj_dealer_play(st.session_state.bj_dealer, st.session_state.bj_deck)
                            st.session_state.bj_dealer = dl
                            st.session_state.bj_deck   = dk
                        st.session_state.bj_state = 'done'
                    st.rerun()
            with c2:
                if st.button("🛑 스탠드 (Stand)", use_container_width=True):
                    dl, dk = bj_dealer_play(st.session_state.bj_dealer, st.session_state.bj_deck)
                    st.session_state.bj_dealer = dl
                    st.session_state.bj_deck   = dk
                    st.session_state.bj_state  = 'done'
                    st.rerun()

        # ── 결과 화면 ──
        else:
            pval_f = bj_value(player)
            dval_f = bj_value(dealer)
            bet_f  = st.session_state.bj_bet
            is_bj  = (pval_f == 21 and len(player) == 2)
            
            if pval_f > 21:
                result, res_col, prize = "💥 버스트! 패배", "#4B9EFF", 0
            elif dval_f > 21:
                result, res_col, prize = "🎉 딜러 버스트! 승리!", "#FF4B4B", bet_f * 2
            elif is_bj and dval_f != 21:
                result, res_col, prize = "🃏 블랙잭!! 1.5배!", "#FFD600", int(bet_f * 2.5)
            elif pval_f > dval_f:
                result, res_col, prize = "🎉 승리!", "#00FF88", bet_f * 2
            elif pval_f == dval_f:
                result, res_col, prize = "🤝 푸시 (타이)", "#888888", bet_f
            else:
                result, res_col, prize = "😢 패배...", "#4B9EFF", 0

            net = prize - bet_f
            net_str = f"+{format_korean_money(net)}" if net > 0 else f"-{format_korean_money(abs(net))}" if net < 0 else "베팅금 반환"
            net_col = "#FF4B4B" if net > 0 else "#4B9EFF" if net < 0 else "#888"

            st.markdown(f"""
            <div style='text-align:center;background:rgba(0,0,0,0.4);border:2px solid {res_col};
                 border-radius:18px;padding:28px;margin:20px 0;box-shadow:0 0 30px {res_col}44;'>
              <div style='font-size:1.8rem;font-weight:900;color:{res_col};'>{result}</div>
              <div style='font-size:1.3rem;font-weight:900;color:{net_col};margin-top:10px;'>{net_str}</div>
              <div style='color:#888;font-size:0.8rem;margin-top:8px;'>지급액: {format_korean_money(prize)}</div>
            </div>
            """, unsafe_allow_html=True)

            if 'bj_paid' not in st.session_state:
                st.session_state.bj_paid = True
                if prize > 0:
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "블랙잭", result, net)
                sync_user_data()              

            if st.button("🔄 다시 하기!", use_container_width=True):
                for k in ['bj_state','bj_player','bj_dealer','bj_bet','bj_paid']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()


# =====================================================================
# ⛏️ 광산 (노가다)
# =====================================================================
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
            rarity_mult = 1.0 + (tier_bonus / item['prob']) * 0.5
            weights_adj.append(item['prob'] * rarity_mult)
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
                if result['name'] == "전설의 원석":
                    claim_hidden_title("first_legendary_ore", "👑 [유일무이] 럭키가이")
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

# =====================================================================
# 👑 칭호 상점
# =====================================================================
elif menu == "👑 칭호 상점":
    st.title("👑 VIP 칭호 상점")
    st.markdown("칭호를 구매하고 장착하여 게시판에서 부를 과시하세요!")
    NON_TITLE_ITEMS = ["파괴방지권"]
    my_titles = [item for item in st.session_state.inventory if item not in NON_TITLE_ITEMS]

    st.markdown("### 🎖️ 내 칭호 보관함")
    if not my_titles:
        st.info("보유한 칭호가 없습니다. 칭호를 구매하거나 가챠를 뽑아보세요!")
    else:
        # 현재 장착 칭호가 보관함에 없으면 첫 번째 칭호를 기본값으로
        default_idx = my_titles.index(st.session_state.equipped_title) if st.session_state.equipped_title in my_titles else 0

        sel_title = st.selectbox(
            "장착할 칭호 선택",
            my_titles,
            index=default_idx,
            format_func=lambda t: f"✅ {t}" if t == st.session_state.equipped_title else t
        )

        col_eq1, col_eq2 = st.columns([3, 1])
        with col_eq1:
            st.markdown(f"현재 장착 중: <b style='color:#FFD600;'>{st.session_state.equipped_title}</b>", unsafe_allow_html=True)
            if sel_title != st.session_state.equipped_title:
                st.caption(f"→ '{sel_title}' 으로 변경 예정")
        with col_eq2:
            if st.button("✅ 장착", use_container_width=True, disabled=(sel_title == st.session_state.equipped_title)):
                st.session_state.equipped_title = sel_title
                sync_user_data()
                st.toast(f"'{sel_title}' 장착 완료!", icon="👑")
                st.rerun()

        # 보관함 전체 목록 표시
        st.markdown("#### 📦 전체 보관함")
        cols_inv = st.columns(3)
        for i, title in enumerate(my_titles):
            with cols_inv[i % 3]:
                is_equipped = (title == st.session_state.equipped_title)
                border_col  = "#FFD600" if is_equipped else "rgba(0,229,255,0.2)"
                label       = "✅ 장착 중" if is_equipped else "🌟 장착"
                st.markdown(f"""
<div style='border:1px solid {border_col};border-radius:10px;padding:10px;
     margin:4px 0;text-align:center;background:rgba(255,255,255,0.03);'>
  <div style='font-size:0.85rem;color:#94A3B8;word-break:break-all;'>{title}</div>
</div>""", unsafe_allow_html=True)
                if not is_equipped:
                    if st.button(label, key=f"inv_eq_{i}", use_container_width=True):
                        st.session_state.equipped_title = title
                        sync_user_data()
                        st.toast(f"'{title}' 장착 완료!", icon="👑")
                        st.rerun()
                else:
                    st.button("✅ 장착 중", key=f"inv_eq_{i}", disabled=True, use_container_width=True)

    st.write("---")

    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i % 2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id   = f"title_{i}"
            price      = i * 10_000_000

            st.markdown(f"**{title_name}** | {format_korean_money(price)}")

            if title_name in st.session_state.inventory:
                if st.session_state.equipped_title == title_name:
                    st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"):
                        st.session_state.equipped_title = title_name
                        sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        u_db_check = load_db(USERS_FILE, {})
                        db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
                        if db_cash < price:
                            st.error("잔액 부족! (DB 검증 실패)")
                        else:
                            st.session_state.global_cash -= price
                            st.session_state.inventory.append(title_name)
                            st.session_state.equipped_title = title_name
                            log_tx(st.session_state.logged_in_user, "칭호구매", f"{title_name} 구매", -price)
                            sync_user_data(); st.rerun()
                    else:
                        st.error("잔액이 부족합니다.")

# =====================================================================
# 📜 내 거래 기록
# =====================================================================
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
                "승부차기":"🥅", # 
            }
            cat_ico = cat_icons.get(log['category'], "📋")
            st.markdown(f"""
<div class='tx-row'>
  <span style='color:#777;min-width:110px;'>{log['time']}</span>
  <span style='color:#888;min-width:60px;'>{cat_ico} {log['category']}</span>
  <span style='color:#94A3B8;flex:1;margin:0 12px;'>{log['desc']}</span>
  <span style='color:{color};font-weight:900;'>{arrow} {sign}{format_korean_money(abs(amt))}</span>
</div>""", unsafe_allow_html=True)

# =====================================================================
# 🏅 랭킹 & 게시판
# =====================================================================
elif menu == "🏅 랭킹 & 게시판":
    st.title("🏅 랭킹 & 게시판")

    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 게시판"])

    with tab_rank:
        users_all = load_db(USERS_FILE, {})
        rank_data = []
        
        # 🚗 차량 티어 매핑용 딕셔너리
        car_tier_map = {"0": "🚙 컴팩트 박스카", "1": "🚗 스포츠 세단", "2": "🏎️ V12 하이퍼카", "3": "🚀 은하철도"}
        
        for uid_r, udata in users_all.items():
            if uid_r == "admin": continue
            w = udata.get('cash', 0) - udata.get('loan', 0)
            
            # 1. 주식 자산 합산
            for sid, p in udata.get('portfolio', {}).items():
                if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
            
            # 2. 부동산 계산 및 보유 목록 텍스트 생성
            re_list = []
            for eid, cnt in udata.get('real_estate', {}).items():
                if eid in estate_config: 
                    w += estate_config[eid]['base_price'] * cnt * 0.8
                    if cnt > 0:
                        re_list.append(f"{estate_config[eid]['icon']} {estate_config[eid]['name']} {cnt}채")
            re_str = ", ".join(re_list) if re_list else "보유 부동산 없음"
            
            # 3. 전설의 명검 계산 및 이름 추출
            w_lv = udata.get('weapon_level', 0)
            w_name = FORGE_DATA[w_lv]['name'] if w_lv in FORGE_DATA else "없음"
            if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
            
            # 4. 차량 정보 추출 (✨ 구버전 & 신버전 DB 완벽 호환)
            garage = udata.get('garage', {})
            car_str = "뚜벅이 (차량 없음)"
            
            # [신버전] 멀티 차고지 시스템 데이터
            if 'active_tier' in garage and garage['active_tier'] is not None:
                active_t = str(garage['active_tier'])
                car_info = garage.get('cars', {}).get(active_t, {})
                if active_t in car_tier_map:
                    tot_lv = car_info.get('engine_lv', 0) + car_info.get('suspension_lv', 0) + car_info.get('bumper_lv', 0)
                    car_str = f"{car_tier_map[active_t]} (+{tot_lv}강)"
            
            # [구버전] 단일 차량 시스템 데이터 (아직 차고지 업데이트 안 한 유저용)
            elif garage.get('owned', False):
                active_t = str(garage.get('tier', '0'))
                if active_t in car_tier_map:
                    tot_lv = garage.get('engine_lv', 0) + garage.get('suspension_lv', 0) + garage.get('bumper_lv', 0)
                    car_str = f"{car_tier_map[active_t]} (+{tot_lv}강)"

            # 유저 데이터 저장
            rank_data.append({
                "uid": uid_r, 
                "title": udata.get('equipped_title','🌱 신규시민'), 
                "nw": w,
                "weapon": w_name,
                "car": car_str,
                "estate": re_str
            })
            
        # 순자산(nw) 기준으로 정렬
        rank_data.sort(key=lambda x: x['nw'], reverse=True)

        medals = ["🥇","🥈","🥉"] + [f"{i}위" for i in range(4, 101)]
        
        # 랭킹 UI 출력 (카드 안에 상세 정보 추가)
        for i, r in enumerate(rank_data[:20]):
            me       = "🫵" if r['uid'] == st.session_state.logged_in_user else ""
            nw_color = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
            
            st.markdown(f"""
<div class='card' style='display:flex; flex-direction:column; padding:16px 20px; margin:8px 0;'>
  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;'>
    <div style='display:flex; align-items:center;'>
      <span style='font-size:1.3rem; min-width:40px;'>{medals[i]}</span>
      <span style='font-weight:900; color:#CBD5E1; font-size:1.1rem; margin-right:10px;'>{r['uid']} {me}</span>
      <span style='color:#888; font-size:0.85rem;'>{r['title']}</span>
    </div>
    <span style='font-weight:900; color:{nw_color}; font-size:1.1rem;'>{format_korean_money(r['nw'])}</span>
  </div>
  <div style='background:rgba(255,255,255,0.03); border-radius:8px; padding:10px 14px; font-size:0.88rem; color:#94A3B8; line-height:1.7;'>
    <div><b>🗡️ 명검:</b> <span style='color:#00FF88;'>{r['weapon']}</span></div>
    <div><b>🏎️ 차량:</b> <span style='color:#00E5FF;'>{r['car']}</span></div>
    <div><b>🏢 부동산:</b> <span style='color:#FFD600;'>{r['estate']}</span></div>
  </div>
</div>""", unsafe_allow_html=True)

    with tab_board:
        msg = st.text_input("메시지 작성", placeholder="랭커 게시판에 글을 남겨보세요!")
        cd_post = cooldown_remaining("board_post", 5.0)
        if cd_post > 0:
            st.warning(f"⏱️ 도배 방지 쿨다운 {cd_post:.1f}초")
        elif st.button("📝 등록", use_container_width=True):
            if msg.strip():
                if st.session_state.logged_in_user in market.get('board_banned', []):
                    st.error("🔇 게시판 이용이 정지된 계정입니다.")
                else:
                    set_cooldown("board_post")
                    comments = load_db(COMMENTS_FILE, [])
                    comments.append({
                        "name":    st.session_state.logged_in_user,
                        "title":   st.session_state.equipped_title,
                        "comment": msg.strip(),
                        "time":    datetime.now(KST).strftime("%m/%d %H:%M")
                    })
                    save_db(COMMENTS_FILE, comments)
                    st.rerun()

        st.write("")
        all_c = load_db(COMMENTS_FILE, [])
        for c in reversed(all_c[-50:]):
            is_me = (c['name'] == st.session_state.logged_in_user)
            border = "border-left:3px solid #FFD600;" if is_me else ""
            me_badge = " <span style='background:#FFD600;color:#000;font-size:0.7rem;padding:1px 6px;border-radius:4px;font-weight:900;'>나</span>" if is_me else ""
            st.markdown(f"""
<div class='card' style='margin:6px 0;padding:12px 16px;{border}'>
  <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
    <span><b style='color:#00E5FF;'>{c['name']}</b>{me_badge} <span style='color:#FFD600;font-size:0.82rem;'>{c.get('title','')}</span></span>
    <span style='color:#777;font-size:0.78rem;'>{c.get('time','')}</span>
  </div>
  <div style='color:#94A3B8;font-size:0.92rem;'>{c['comment']}</div>
</div>""", unsafe_allow_html=True)

# =====================================================================
# ✉️ 개인 쪽지함 (1:1 DM)
# =====================================================================
elif menu == "✉️ 개인 쪽지함":
    st.title("✉️ 1:1 비밀 쪽지함")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>다른 시민들과 은밀하게 작전을 모의하거나 흥정하세요. 시스템은 여러분의 대화를 엿듣지 않습니다. (아마도요)</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user
    msg_db = load_db("messages_db.json", {})
    
    # 내 DB 구조 초기화
    if uid not in msg_db:
        msg_db[uid] = {"inbox": [], "outbox": []}

    tab_in, tab_out, tab_send = st.tabs(["📥 받은 편지함", "📤 보낸 편지함", "✍️ 쪽지 쓰기"])

    # ── [1] 받은 편지함 ──
    with tab_in:
        inbox = msg_db[uid].get("inbox", [])
        
        # '읽음' 처리 로직 (탭에 들어오면 미확인 쪽지를 모두 읽음으로 처리)
        unread_exist = False
        for m in inbox:
            if not m.get("read", False):
                m["read"] = True
                unread_exist = True
        if unread_exist:
            save_db("messages_db.json", msg_db)
            
        if not inbox:
            st.info("받은 쪽지가 없습니다.")
        else:
            if st.button("🗑️ 받은 쪽지 모두 비우기", use_container_width=True, type="secondary"):
                msg_db[uid]["inbox"] = []
                save_db("messages_db.json", msg_db)
                st.success("받은 쪽지함이 비워졌습니다.")
                st.rerun()
                
            st.write("---")
            # 최신순으로 정렬해서 보여줌
            for m in reversed(inbox[-50:]):  # 최근 50개만 표시
                read_badge = "" if m.get("read_before", False) else "<span style='color:#FF4B4B;font-size:0.75rem;font-weight:900;'>[NEW]</span> "
                m["read_before"] = True # 화면에 그릴 때 예전 상태 방지용 (DB저장 안함)
                
                st.markdown(f"""
                <div class='card' style='padding:14px 18px; margin:8px 0; border-left:4px solid #00E5FF;'>
                  <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                    <span style='font-size:0.9rem;'>{read_badge}보낸 사람: <b style='color:#00E5FF;'>{m['sender']}</b></span>
                    <span style='color:#777;font-size:0.75rem;'>{m['time']}</span>
                  </div>
                  <div style='color:#CBD5E1;font-size:0.95rem;line-height:1.5;word-break:break-all;'>
                    {m['content']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── [2] 보낸 편지함 ──
    with tab_out:
        outbox = msg_db[uid].get("outbox", [])
        if not outbox:
            st.info("보낸 쪽지가 없습니다.")
        else:
            if st.button("🗑️ 보낸 쪽지 모두 비우기", key="clear_outbox", use_container_width=True, type="secondary"):
                msg_db[uid]["outbox"] = []
                save_db("messages_db.json", msg_db)
                st.success("보낸 쪽지함이 비워졌습니다.")
                st.rerun()
                
            st.write("---")
            for m in reversed(outbox[-50:]):
                st.markdown(f"""
                <div class='card' style='padding:14px 18px; margin:8px 0; border-left:4px solid #FFD600; background:rgba(255,215,0,0.02);'>
                  <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                    <span style='font-size:0.9rem;color:#94A3B8;'>받는 사람: <b style='color:#FFD600;'>{m['receiver']}</b></span>
                    <span style='color:#777;font-size:0.75rem;'>{m['time']}</span>
                  </div>
                  <div style='color:#94A3B8;font-size:0.95rem;line-height:1.5;word-break:break-all;'>
                    {m['content']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── [3] 쪽지 쓰기 ──
    with tab_send:
        users_db = load_db(USERS_FILE, {})
        # 관리자와 본인을 제외한 수신 가능 유저 목록
        user_list = [u for u in users_db.keys() if u != "admin" and u != uid]
        
        if not user_list:
            st.warning("현재 우주에 쪽지를 보낼 다른 시민이 존재하지 않습니다.")
        else:
            target_user = st.selectbox("수신자 선택", user_list)
            msg_content = st.text_area("쪽지 내용", placeholder="여기에 은밀한 메시지를 작성하세요. (최대 500자)", max_chars=500, height=150)
            
            cd_msg = cooldown_remaining("send_dm", 3.0)
            if cd_msg > 0:
                st.warning(f"⏱️ 도배 방지: {cd_msg:.1f}초 후 전송 가능")
            elif st.button("📨 쪽지 전송", use_container_width=True):
                if not msg_content.strip():
                    st.error("내용을 입력해주세요.")
                else:
                    set_cooldown("send_dm")
                    now_str = datetime.now(KST).strftime("%m/%d %H:%M:%S")
                    
                    # 새로운 쪽지 객체
                    new_msg_in = {"sender": uid, "content": msg_content.strip(), "time": now_str, "read": False}
                    new_msg_out = {"receiver": target_user, "content": msg_content.strip(), "time": now_str}
                    
                    # 수신자 DB에 추가
                    if target_user not in msg_db:
                        msg_db[target_user] = {"inbox": [], "outbox": []}
                    msg_db[target_user]["inbox"].append(new_msg_in)
                    
                    # 내 발신 DB에 추가
                    msg_db[uid]["outbox"].append(new_msg_out)
                    
                    # 저장
                    save_db("messages_db.json", msg_db)
                    
                    st.success(f"✅ {target_user}님에게 쪽지를 성공적으로 전송했습니다!")
                    time.sleep(1)
                    st.rerun()

# =====================================================================
# 📅 일일 퀘스트
# =====================================================================
elif menu == "📅 일일 퀘스트":
    st.title("📅 일일 퀘스트")
    st.markdown("<div style='color:#888;margin-bottom:20px;'>매일 자정에 초기화됩니다. 달성하고 보상을 수령하세요!</div>", unsafe_allow_html=True)
    
    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    dq = st.session_state.get('daily_quests', {})
    today_dq = dq.get(today_str, {})

    def check_quest(qid):
        if qid == "attendance": return True
        elif qid == "rich5": return nw >= 500_000_000
        elif qid == "landlord": return any(v > 0 for v in st.session_state.real_estate.values())
        elif qid == "debtfree": return st.session_state.loan == 0
        elif qid == "investor":
            return sum(
                st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price']
                for s in stock_config
            ) >= 100_000_000
        elif qid == "coin100m":
            if 'crypto_data' not in market: return False
            return sum(
                ci.get('qty', 0) * market['crypto_data'].get(cid, {}).get('price', 0)
                for cid, ci in st.session_state.get('crypto_portfolio', {}).items()
            ) >= 100_000_000
        elif qid == "billionaire": return nw >= 100_000_000_000
        return False
    
    for q in DAILY_QUESTS_CONFIG:
        is_claimed    = today_dq.get(q['id'], False)
        is_achievable = check_quest(q['id'])
        
        status_col = "#00FF88" if is_claimed else "#FFD600" if is_achievable else "#444"
        def get_progress_hint(qid):
            if qid == "rich5":      return f"현재 순자산: {format_korean_money(nw)} / 5억"
            elif qid == "landlord": return f"보유 부동산: {sum(v for v in st.session_state.real_estate.values())}채 / 1채"
            elif qid == "investor":
                sv = sum(st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price'] for s in stock_config)
                return f"주식 평가액: {format_korean_money(int(sv))} / 1억"
            elif qid == "coin100m":
                cv = sum(ci.get('qty',0) * market['crypto_data'].get(cid,{}).get('price',0) for cid, ci in st.session_state.get('crypto_portfolio',{}).items()) if 'crypto_data' in market else 0
                return f"코인 평가액: {format_korean_money(int(cv))} / 1억"
            elif qid == "debtfree": return f"현재 대출: {format_korean_money(st.session_state.loan)}"
            elif qid == "billionaire": return f"현재 순자산: {format_korean_money(nw)} / 1000억"
            return ""

        hint = get_progress_hint(q['id'])
        status_txt = "✅ 수령 완료" if is_claimed else "🟡 달성! 클릭하여 수령" if is_achievable else f"🔒 미달성 ({hint})" if hint else "🔒 미달성"
        
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); border-left:4px solid {status_col}; padding:15px; border-radius:8px; margin-bottom:10px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='font-size:1.5rem;'>{q['icon']}</span> <b style='font-size:1.1rem; color:#E2E8F0;'>{q['name']}</b>
                    <div style='color:#888; font-size:0.85rem; margin-top:4px;'>{q['desc']}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:#FFD600; font-weight:900;'>{format_korean_money(q['reward'])}</div>
                    <div style='color:{status_col}; font-size:0.8rem; margin-top:4px;'>{status_txt}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if is_achievable and not is_claimed:
            if st.button(f"[{q['name']}] 보상 수령", key=f"q_btn_{q['id']}"):
                today_dq[q['id']] = True
                dq[today_str] = today_dq
                st.session_state.daily_quests = dq
                st.session_state.global_cash += q['reward']
                log_tx(st.session_state.logged_in_user, "퀘스트", f"{q['name']} 완료", q['reward'])
                sync_user_data(); st.rerun()

# =====================================================================
# 🗡️ 전설의 명검 강화 (신규 매운맛)
# =====================================================================
elif menu == "🗡️ 전설의 명검 강화":
    st.title("🗡️ 전설의 명검 강화소")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>당신의 운과 욕망을 시험하세요. <b>+5~+9강은 실패 시 50% 확률로 파괴, +10강부터는 확정 파괴</b>됩니다.</div>", unsafe_allow_html=True)
    u_lv = st.session_state.get('weapon_level', 0)
    w_info = FORGE_DATA[u_lv]
    
    st.markdown(f"""
    <div style='text-align:center; padding:30px; background:linear-gradient(180deg, rgba(0,0,0,0.8), rgba(20,20,40,0.9)); border:2px solid {w_info['color']}; border-radius:15px; box-shadow:0 0 20px {w_info['color']}44;'>
        <div style='font-size:4rem; margin-bottom:10px;'>{w_info['name'].split(' ')[0]}</div>
        <div style='font-size:1.8rem; font-weight:900; color:{w_info['color']}; text-shadow:0 0 10px {w_info['color']}88;'>{w_info['name']}</div>
        <div style='color:#94A3B8; margin-top:15px; font-size:0.9rem;'>무기 가치 (판매가): <b style='color:#FFD600;'>{format_korean_money(w_info['sell'])}</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if u_lv >= 15:
        st.success("🎉 만렙 달성! 더 이상 강화할 수 없습니다. 우주 최강의 무기입니다!")
    else:
        next_info = FORGE_DATA[u_lv + 1]
        cost = next_info['cost']
        rate = next_info['rate'] * 100
        
        ticket_count = st.session_state.inventory.count("파괴방지권")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🛠️ 강화 정보 (+{u_lv+1} 도전)")
            st.write(f"- **강화 비용:** {format_korean_money(cost)}")
            st.write(f"- **성공 확률:** {rate}%")
            
            if u_lv >= 9:
                st.markdown("<b style='color:#FF4B4B;'>⚠️ 경고: 실패 시 무기가 무조건 파괴됩니다!</b>", unsafe_allow_html=True)
            elif u_lv >= 4:
                st.markdown("<b style='color:#FF8800;'>⚠️ 경고: 실패 시 50% 확률로 무기가 파괴됩니다!</b>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#00FF88;'>안전 강화 구간입니다. 실패해도 레벨이 유지됩니다.</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(f"**🎟️ 내 파괴 방지권:** {ticket_count}개")
            if st.button("🎟️ 파괴 방지권 구매 (500억원)", key="buy_ticket", use_container_width=True):
                if st.session_state.global_cash >= 50_000_000_000: 
                    st.session_state.global_cash -= 50_000_000_000 
                    st.session_state.inventory.append("파괴방지권")
                    sync_user_data()
                    st.success("✅ 파괴 방지권 구매 완료!")
                    st.rerun()
                else:
                    st.error("잔액이 부족합니다.")
            
        with c2:
            st.markdown("#### 🎯 선택")
            cd_forge = cooldown_remaining("forge_action", 1.0)
            
            if u_lv == 0:
                btn_label = f"🪵 목검 구매하기 ({format_korean_money(cost)})"
                use_ticket = False
            else:
                btn_label = f"🔨 강화하기! ({format_korean_money(cost)})"
                if u_lv >= 4:
                    use_ticket = st.checkbox("🛡️ 파괴 방지권 사용", disabled=(ticket_count == 0))
                else:
                    use_ticket = False
                
            if cd_forge > 0:
                st.warning(f"⏱️ 망치질 쿨다운... {cd_forge:.1f}초")
            else:
                if st.button(btn_label, use_container_width=True):
                    if st.session_state.global_cash < cost:
                        st.error("잔액이 부족합니다!")
                    elif use_ticket and "파괴방지권" not in st.session_state.inventory:
                        st.error("⚠️ 파괴 방지권이 없습니다! (중복 클릭 감지)")
                    else:
                        set_cooldown("forge_action")
                        st.session_state.global_cash -= cost
                        
                        if use_ticket:
                            st.session_state.inventory.remove("파괴방지권")
                        
                        uid = st.session_state.logged_in_user
                        us = load_db(USERS_FILE, {}) 
                        is_cursed = us.get(uid, {}).get('cursed_forge', False)
                        
                        success = random.random() < next_info['rate'] 
                        
                        if is_cursed:
                            success = False
                            us[uid]['cursed_forge'] = False          # ← 이미 읽은 us 재활용
                            us[uid]['cash'] = st.session_state.global_cash
                            save_db(USERS_FILE, us)
                            st.toast("💀 누군가의 불길한 기운이 개입했습니다...", icon="💀")
                            time.sleep(1)

                        if success:
                            st.session_state.weapon_level += 1
                            log_tx(uid, "강화", f"{next_info['name']} 강화 성공", -cost)
                            sync_user_data()
                            
                            if st.session_state.weapon_level >= 10:
                                st.balloons()
                                market['news'] = f"🎆 [전설 탄생] {uid}님이 {next_info['name']} 강화에 성공했습니다!!!"
                                save_market(market)
                                
                            st.success(f"✨ 강화 성공!! [{next_info['name']}]을(를) 획득했습니다!")
                            st.rerun()
                        else:
                            if use_ticket:
                                log_tx(uid, "강화", f"+{u_lv+1} 강화 실패 (방지권 사용)", -cost)
                                sync_user_data()
                                st.info("🛡️ 파괴 방지권이 빛을 발하며 무기를 보호했습니다! (수치 유지)")
                                st.rerun()
                            else:
                                is_destroyed = False
                                if u_lv >= 9:
                                    is_destroyed = True
                                elif u_lv >= 4:
                                    is_destroyed = random.random() < 0.5
                                
                                if is_destroyed:
                                    st.session_state.weapon_level = 0
                                    log_tx(uid, "강화", f"+{u_lv+1} 강화 파괴됨", -cost)
                                    sync_user_data()
                                    if u_lv >= 9:
                                        market['news'] = f"💥 [단독] {uid}님의 {w_info['name']}이(가) 산산조각 났습니다..."
                                        save_market(market)
                                    st.error("💥 쿠장창! 무기가 처참하게 파괴되었습니다...")
                                    st.snow()
                                    st.rerun()
                                else:
                                    if u_lv >= 4:
                                        log_tx(uid, "강화", f"+{u_lv+1} 강화 실패 (파괴 모면)", -cost)
                                        sync_user_data()
                                        st.warning("💦 휴... 강화에 실패했지만, 기적적으로 무기가 파괴되지 않았습니다!")
                                    else:
                                        log_tx(uid, "강화", f"+{u_lv+1} 강화 실패", -cost)
                                        sync_user_data()
                                        st.warning("💦 앗... 강화에 실패했습니다. (무기는 무사합니다)")
                                    st.rerun()

    # 👇 [수정됨] 15강이어도 버튼이 나오도록 들여쓰기를 바깥으로 뺐습니다!
    if u_lv > 0:
        st.write("---")
        if st.button(f"💰 무기 판매 (익절): {format_korean_money(w_info['sell'])}", use_container_width=True, type="secondary"):
            sell_amt = w_info['sell']
            st.session_state.global_cash += sell_amt
            st.session_state.weapon_level = 0
            log_tx(st.session_state.logged_in_user, "무기판매", f"{w_info['name']} 판매", sell_amt)
            sync_user_data()
            st.success(f"✅ 무기를 팔아 {format_korean_money(sell_amt)}을 얻었습니다. 다시 목검부터 시작합니다!")
            
            if u_lv >= 13:
                claim_hidden_title("sell_high_weapon", "👑 [유일무이] 낭만 합격")
                
            st.rerun()

# =====================================================================
# 🛠️ 커스텀 튜닝 차고지 (대리점 및 멀티 차고지 시스템)
# =====================================================================
elif menu == "🛠️ 커스텀 튜닝 차고지":
    st.title("🛠️ 커스텀 튜닝 차고지")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>차량을 구매하고 우주 최고의 하이퍼카로 개조하세요!</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user
    us = load_db(USERS_FILE, {})
    my_data = us.get(uid, {})

    # [데이터 마이그레이션] 기존 단일 차량 시스템을 멀티 차량 시스템으로 변환
    if 'garage' not in my_data:
        my_data['garage'] = {'cars': {}, 'active_tier': None}
    else:
        g = my_data['garage']
        if 'cars' not in g:
            g['cars'] = {}
            if g.get('owned', False):
                t = str(g.get('tier', 0))
                g['cars'][t] = {
                    "engine_lv": g.get('engine_lv', 0),
                    "suspension_lv": g.get('suspension_lv', 0),
                    "bumper_lv": g.get('bumper_lv', 0),
                    "needs_repair": g.get('needs_repair', False)
                }
                g['active_tier'] = t
            else:
                g['active_tier'] = None

    garage = my_data['garage']

    CAR_TIERS = [
        {"tier": "0", "name": "2021년형 컴팩트 박스카", "emoji": "🚙", "color": "#A0A0A0", "price": 10_000_000_000},
        {"tier": "1", "name": "터보차저 스포츠 세단", "emoji": "🚗", "color": "#00E5FF", "price": 500_000_000_000},
        {"tier": "2", "name": "V12 럭셔리 하이퍼카", "emoji": "🏎️", "color": "#FFD600", "price": 5_000_000_000_000},
        {"tier": "3", "name": "🌌 우주 뚫은 은하철도", "emoji": "🚀", "color": "#FF00FF", "price": 50_000_000_000_000}
    ]

    tab_my_garage, tab_shop = st.tabs(["🚘 내 차고지", "🏢 차량 대리점 (신차 구매)"])

    # ------------------ [내 차고지 탭] ------------------
    with tab_my_garage:
        if not garage['cars']:
            st.info("🚗 소유한 차량이 없습니다. '차량 대리점'에서 첫 차를 구매하세요!")
        else:
            # 탑승할 차량 선택
            owned_tiers = list(garage['cars'].keys())
            if garage['active_tier'] not in owned_tiers:
                garage['active_tier'] = owned_tiers[0]
            
            sel_active = st.selectbox(
                "🏁 메인(출전) 차량 선택", 
                owned_tiers, 
                index=owned_tiers.index(garage['active_tier']),
                format_func=lambda t: f"{next(c['emoji'] for c in CAR_TIERS if c['tier']==t)} {next(c['name'] for c in CAR_TIERS if c['tier']==t)}"
            )

            if sel_active != garage['active_tier']:
                garage['active_tier'] = sel_active
                my_data['garage'] = garage
                us[uid] = my_data
                save_db(USERS_FILE, us)
                st.rerun()

            active_t = garage['active_tier']
            cur_car_data = garage['cars'][active_t]
            cur_tier_info = next(c for c in CAR_TIERS if c['tier'] == active_t)
            total_lv = cur_car_data['engine_lv'] + cur_car_data['suspension_lv'] + cur_car_data['bumper_lv']

            st.markdown(f"""
            <div style='text-align:center; padding:30px; background:linear-gradient(135deg, rgba(20,20,20,0.8), rgba(40,40,60,0.9)); border:2px solid {cur_tier_info['color']}; border-radius:15px; box-shadow:0 0 20px {cur_tier_info['color']}44;'>
                <div style='font-size:5rem; margin-bottom:10px;'>{cur_tier_info['emoji']}</div>
                <div style='font-size:1.8rem; font-weight:900; color:{cur_tier_info['color']};'>{cur_tier_info['name']}</div>
                <div style='color:#94A3B8; margin-top:15px; font-size:1rem;'>현재 총합 튜닝 레벨: <b style='color:#FFD600;'>Lv.{total_lv}</b> / 15</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("---")

            if cur_car_data['needs_repair']:
                st.error("🚨 앗! 심각한 차량 파손이 감지되었습니다!")
                st.markdown("### 💥 뒷범퍼 및 백판넬 대파")
                st.caption("차량이 파손된 상태에서는 튜닝 및 레이싱 출전이 불가능합니다.")
                
                repair_cost = 8_700_000_000 * (10 ** int(active_t)) 

                if st.button(f"🛠️ 눈물을 머금고 수리하기 ({format_korean_money(repair_cost)})", use_container_width=True):
                    if st.session_state.global_cash >= repair_cost:
                        st.session_state.global_cash -= repair_cost
                        garage['cars'][active_t]['needs_repair'] = False
                        my_data['garage'] = garage
                        us[uid] = my_data
                        save_db(USERS_FILE, us)
                        sync_user_data()
                        log_tx(uid, "차량수리", f"{cur_tier_info['name']} 파손 수리", -repair_cost)
                        st.toast("✨ 수리가 완료되었습니다!", icon="✅")
                        st.rerun()
                    else:
                        st.error("수리비가 부족합니다!")
            else:
                st.markdown("### 🔧 파츠 튜닝샵")
                st.caption("각 파츠가 5레벨에 도달하면 다음 등급의 차량으로 무상 승급(풀체인지) 할 수 있습니다.")

                def tune_part(part_key, part_name):
                    current_lv = cur_car_data[part_key]
                    if current_lv >= 5:
                        st.success(f"✅ {part_name} 파츠는 이미 최고 레벨(MAX)입니다!")
                        return

                    tier_mult = 10 ** int(active_t)
                    cost = (current_lv + 1) * 10_000_000_000 * tier_mult 
                    prob = max(0.15, 0.8 - (current_lv * 0.15) - (int(active_t) * 0.1))

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{part_name}** (Lv.{current_lv}/5) <br> <span style='color:#888;font-size:0.8rem;'>비용: {format_korean_money(cost)} | 성공률: {prob*100:.0f}%</span>", unsafe_allow_html=True)
                    with col2:
                        if st.button("🔨 강화", key=f"tune_{active_t}_{part_key}", use_container_width=True):
                            if st.session_state.global_cash < cost:
                                st.error("잔액 부족!")
                            else:
                                st.session_state.global_cash -= cost
                                
                                if random.random() < prob:
                                    garage['cars'][active_t][part_key] += 1
                                    log_tx(uid, "튜닝", f"{part_name} 성공 (+{current_lv+1})", -cost)
                                    st.success(f"✨ {part_name} 튜닝 성공!!")
                                    if active_t == "0" and garage['cars'][active_t]['engine_lv'] == 5 and garage['cars'][active_t]['suspension_lv'] == 5 and garage['cars'][active_t]['bumper_lv'] == 5:
                                        claim_hidden_title("first_tier0_max", "👑 [유일무이] 똥차계의 람보르기니")
                                else:
                                    if random.random() < 0.20:
                                        garage['cars'][active_t]['needs_repair'] = True
                                        st.error("💥 쾅!! 튜닝 중 차량이 미끄러져 벽을 들이받았습니다!")
                                        log_tx(uid, "튜닝", f"{part_name} 대실패 (사고발생)", -cost)
                                    else:
                                        log_tx(uid, "튜닝", f"{part_name} 실패", -cost)
                                        st.warning("💦 부품이 맞지 않아 튜닝에 실패했습니다. (파손은 없습니다)")

                                my_data['garage'] = garage
                                us[uid] = my_data
                                save_db(USERS_FILE, us)
                                sync_user_data()
                                st.rerun()

                tune_part("engine_lv", "🔥 하이퍼 V엔진 스왑")
                tune_part("suspension_lv", "🧲 에어 서스펜션 조정")
                tune_part("bumper_lv", "🛡️ 카본 에어로 다이내믹 뒷범퍼")

                st.write("---")
                if cur_car_data['engine_lv'] >= 5 and cur_car_data['suspension_lv'] >= 5 and cur_car_data['bumper_lv'] >= 5:
                    next_tier_int = int(active_t) + 1
                    if next_tier_int < len(CAR_TIERS):
                        next_tier_str = str(next_tier_int)
                        st.info("모든 파츠가 최대 레벨에 도달했습니다! 상위 등급으로 무상 풀체인지가 가능합니다.")
                        if st.button("🚀 차량 풀체인지 승급하기! (무료)", use_container_width=True):
                            del garage['cars'][active_t] # 기존 차 버림
                            garage['cars'][next_tier_str] = {"engine_lv": 0, "suspension_lv": 0, "bumper_lv": 0, "needs_repair": False}
                            garage['active_tier'] = next_tier_str
                            my_data['garage'] = garage
                            us[uid] = my_data
                            save_db(USERS_FILE, us)
                            sync_user_data()
                            log_tx(uid, "차량승급", f"{CAR_TIERS[next_tier_int]['name']} 승급", 0)
                            market['news'] = f"🏎️ [차고지 핫이슈] {uid}님이 풀튜닝의 결실로 {CAR_TIERS[next_tier_int]['name']} 오너가 되셨습니다!!"
                            save_market(market)
                            st.balloons(); st.success(f"🎉 승급 완료!"); st.rerun()
                    else:
                        st.success("🌟 튜닝의 끝판왕! 우주 최고의 스펙을 달성했습니다!")

    # ------------------ [차량 대리점 탭] ------------------
    with tab_shop:
        st.markdown("### 🏢 HYOMIN 모터스 공식 대리점")
        st.caption("돈만 있다면 승급을 위한 튜닝 노가다 없이 바로 하이퍼카를 현찰 박치기로 구매할 수 있습니다.")

        for c_info in CAR_TIERS:
            t_str = c_info['tier']
            c1, c2 = st.columns([4, 2])
            with c1:
                st.markdown(f"**{c_info['emoji']} {c_info['name']}**")
                st.markdown(f"<span style='color:#FFD600;font-weight:900;'>{format_korean_money(c_info['price'])}</span>", unsafe_allow_html=True)
            with c2:
                if t_str in garage['cars']:
                    st.button("✅ 보유 중", key=f"shop_own_{t_str}", disabled=True, use_container_width=True)
                else:
                    if st.button("🛒 구매하기", key=f"shop_buy_{t_str}", use_container_width=True):
                        if st.session_state.global_cash >= c_info['price']:
                            st.session_state.global_cash -= c_info['price']
                            garage['cars'][t_str] = {"engine_lv": 0, "suspension_lv": 0, "bumper_lv": 0, "needs_repair": False}
                            garage['active_tier'] = t_str # 구매 즉시 메인카로 변경
                            my_data['garage'] = garage
                            us[uid] = my_data
                            save_db(USERS_FILE, us)
                            sync_user_data()
                            log_tx(uid, "차량구매", f"{c_info['name']} 즉시 구매", -c_info['price'])
                            st.toast(f"🎉 {c_info['name']} 출고 완료!", icon="🚗")
                            st.rerun()
                        else:
                            st.error("잔액이 부족합니다.")
            st.write("---")

# =====================================================================
# 🏰 길드/클랜
# =====================================================================
elif menu == "🏰 길드/클랜":
    st.title("🏰 길드/클랜 시스템")
    uid = st.session_state.logged_in_user
    clans = load_clan_db()
    my_clan = get_user_clan(uid)

    tab_my, tab_list, tab_rank = st.tabs(["🏠 내 클랜", "🔍 클랜 목록", "🏆 클랜 랭킹"])

    with tab_my:
        if my_clan is None:
            st.info("소속된 클랜이 없습니다.")
            st.write("---")
            st.markdown("### ⚔️ 새 클랜 창설")
            st.caption("클랜 창설 비용: 10억원")
            new_clan_name = st.text_input("클랜 이름 (최대 10자)", max_chars=10)
            new_clan_desc = st.text_input("클랜 소개글 (최대 30자)", max_chars=30)
            new_clan_icon = st.selectbox("클랜 아이콘", ["🏰","⚔️","🐉","🔥","💀","🌙","🌊","⚡","🦁","🐺"])
            if st.button("🏰 클랜 창설하기 (10억)", use_container_width=True):
                if not new_clan_name.strip():
                    st.error("클랜 이름을 입력하세요.")
                elif new_clan_name in clans:
                    st.error("이미 존재하는 클랜 이름입니다.")
                elif st.session_state.global_cash < 1_000_000_000:
                    st.error("잔액 부족! (10억 필요)")
                else:
                    st.session_state.global_cash -= 1_000_000_000
                    clans[new_clan_name] = {
                        "leader":        uid,
                        "members":       [uid],
                        "bank":          0,
                        "desc":          new_clan_desc,
                        "icon":          new_clan_icon,
                        "created":       time.time(),
                        "join_requests": [],
                    }
                    save_clan_db(clans)
                    log_tx(uid, "클랜", f"{new_clan_name} 클랜 창설", -1_000_000_000)
                    sync_user_data()
                    market['news'] = f"🏰 [{uid}]님이 [{new_clan_name}] 클랜을 창설했습니다!"
                    save_market(market)
                    st.success(f"✅ [{new_clan_name}] 클랜 창설 완료!")
                    st.rerun()

            st.write("---")
            st.markdown("### 🚪 클랜 가입 신청")
            if clans:
                join_target = st.selectbox(
                    "가입할 클랜 선택",
                    list(clans.keys()),
                    format_func=lambda n: f"{clans[n]['icon']} {n} ({len(clans[n]['members'])}명)"
                )
                if st.button("📨 가입 신청하기", use_container_width=True):
                    if uid in clans[join_target].get('join_requests', []):
                        st.warning("이미 신청한 클랜입니다.")
                    else:
                        clans[join_target].setdefault('join_requests', []).append(uid)
                        save_clan_db(clans)
                        st.success(f"✅ [{join_target}] 클랜에 가입 신청 완료! 클랜장의 승인을 기다리세요.")
            else:
                st.info("아직 클랜이 없습니다. 첫 클랜을 창설하세요!")

        else:
            cdata = clans[my_clan]
            is_leader = (cdata['leader'] == uid)

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(255,180,0,0.08),rgba(255,100,0,0.06));
                 border:2px solid rgba(255,180,0,0.4);border-radius:16px;padding:24px;text-align:center;'>
              <div style='font-size:3rem;'>{cdata['icon']}</div>
              <div style='font-size:1.8rem;font-weight:900;color:#FFD600;margin-top:8px;'>{my_clan}</div>
              <div style='color:#888;font-size:0.88rem;margin-top:6px;'>{cdata.get('desc','')}</div>
              <div style='margin-top:10px;color:#94A3B8;'>클랜장: <b style='color:#00E5FF;'>{cdata['leader']}</b> &nbsp;|&nbsp; 멤버: {len(cdata['members'])}명</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            c1, c2 = st.columns(2)
            c1.metric("🏦 클랜 은행", format_korean_money(cdata.get('bank', 0)))
            c2.metric("💪 클랜 총 순자산", format_korean_money(get_clan_total_nw(my_clan, market)))

            st.write("---")
            st.markdown("### 🏦 클랜 은행")
            col_dep, col_wit = st.columns(2)
            with col_dep:
                dep_amt = st.number_input("입금액", min_value=0, step=10_000_000, format="%d", key="clan_dep")
                if st.button("💰 클랜 은행 입금", use_container_width=True):
                    if st.session_state.global_cash >= dep_amt > 0:
                        st.session_state.global_cash -= dep_amt
                        clans[my_clan]['bank'] = clans[my_clan].get('bank', 0) + dep_amt
                        save_clan_db(clans)
                        log_tx(uid, "클랜", f"{my_clan} 클랜 은행 입금", -dep_amt)
                        sync_user_data()
                        st.success(f"✅ {format_korean_money(dep_amt)} 입금 완료!")
                        st.rerun()
                    else:
                        st.error("잔액 부족!")
            with col_wit:
                wit_amt = st.number_input("출금액", min_value=0, step=10_000_000, format="%d", key="clan_wit")
                if st.button("🏧 클랜 은행 출금", use_container_width=True, disabled=not is_leader):
                    bank = clans[my_clan].get('bank', 0)
                    if not is_leader:
                        st.error("클랜장만 출금 가능합니다.")
                    elif wit_amt > bank:
                        st.error("클랜 은행 잔액 부족!")
                    elif wit_amt > 0:
                        clans[my_clan]['bank'] = bank - wit_amt
                        st.session_state.global_cash += wit_amt
                        save_clan_db(clans)
                        log_tx(uid, "클랜", f"{my_clan} 클랜 은행 출금", wit_amt)
                        sync_user_data()
                        st.success(f"✅ {format_korean_money(wit_amt)} 출금 완료!")
                        st.rerun()
            if not is_leader:
                st.caption("⚠️ 출금은 클랜장만 가능합니다.")

            st.write("---")
            st.markdown("### 👥 멤버 목록")
            for m in cdata['members']:
                crown   = "👑 " if m == cdata['leader'] else ""
                me_mark = " ← 나" if m == uid else ""
                m_nw    = get_net_worth(m, market)
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;padding:8px 12px;
                     background:rgba(255,255,255,0.03);border-radius:8px;margin:4px 0;'>
                  <span>{crown}<b style='color:#00E5FF;'>{m}</b>{me_mark}</span>
                  <span style='color:#FFD600;'>{format_korean_money(m_nw)}</span>
                </div>
                """, unsafe_allow_html=True)

            if is_leader:
                st.write("---")
                st.markdown("### 📨 가입 신청 관리")
                requests = cdata.get('join_requests', [])
                if not requests:
                    st.info("신청자가 없습니다.")
                else:
                    for req_uid in requests:
                        r1, r2, r3 = st.columns([3, 1, 1])
                        r1.write(f"👤 {req_uid}")
                        if r2.button("✅ 승인", key=f"approve_{req_uid}"):
                            clans[my_clan]['members'].append(req_uid)
                            clans[my_clan]['join_requests'].remove(req_uid)
                            save_clan_db(clans)
                            market['news'] = f"🏰 [{req_uid}]님이 [{my_clan}] 클랜에 합류했습니다!"
                            save_market(market)
                            st.rerun()
                        if r3.button("❌ 거절", key=f"reject_{req_uid}"):
                            clans[my_clan]['join_requests'].remove(req_uid)
                            save_clan_db(clans)
                            st.rerun()

                st.write("---")
                kick_candidates = [m for m in cdata['members'] if m != uid]
                if kick_candidates:
                    kick_target = st.selectbox("강퇴할 멤버", kick_candidates)
                    if st.button(f"🦵 {kick_target} 강퇴", use_container_width=True):
                        clans[my_clan]['members'].remove(kick_target)
                        save_clan_db(clans)
                        st.success(f"✅ {kick_target} 강퇴 완료!")
                        st.rerun()

            st.write("---")
            if st.button("🚪 클랜 탈퇴 / 해산", use_container_width=True, type="secondary"):
                if is_leader and len(cdata['members']) > 1:
                    st.error("클랜장은 멤버가 있으면 탈퇴 불가. 먼저 멤버를 전부 강퇴하세요.")
                elif is_leader:
                    del clans[my_clan]
                    save_clan_db(clans)
                    st.success("클랜 해산 완료!")
                    st.rerun()
                else:
                    clans[my_clan]['members'].remove(uid)
                    save_clan_db(clans)
                    st.success("클랜 탈퇴 완료!")
                    st.rerun()

    with tab_list:
        st.markdown("### 🔍 전체 클랜 목록")
        if not clans:
            st.info("아직 클랜이 없습니다.")
        else:
            for cname, cdata in clans.items():
                total_nw = get_clan_total_nw(cname, market)
                st.markdown(f"""
                <div class='card' style='padding:16px 20px;'>
                  <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <div>
                      <span style='font-size:1.5rem;'>{cdata['icon']}</span>
                      <b style='color:#FFD600;font-size:1.1rem;margin-left:8px;'>{cname}</b>
                      <span style='color:#888;font-size:0.82rem;margin-left:10px;'>{cdata.get('desc','')}</span>
                    </div>
                    <div style='text-align:right;'>
                      <div style='color:#00E5FF;font-weight:900;'>{format_korean_money(total_nw)}</div>
                      <div style='color:#888;font-size:0.78rem;'>멤버 {len(cdata['members'])}명 | 클랜장: {cdata['leader']}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_rank:
        st.markdown("### 🏆 클랜 순자산 랭킹")
        if not clans:
            st.info("아직 클랜이 없습니다.")
        else:
            ranked = sorted(
                [(cn, get_clan_total_nw(cn, market), clans[cn]) for cn in clans],
                key=lambda x: x[1], reverse=True
            )
            medals = ["🥇","🥈","🥉"] + [f"{i}위" for i in range(4, 20)]
            for i, (cname, total, cdata) in enumerate(ranked):
                nw_col  = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
                my_mark = " ← 내 클랜" if cname == my_clan else ""
                st.markdown(f"""
                <div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:14px 20px;'>
                  <div>
                    <span style='font-size:1.2rem;margin-right:10px;'>{medals[i]}</span>
                    <span style='font-size:1.2rem;'>{cdata['icon']}</span>
                    <b style='color:#E2E8F0;margin-left:8px;'>{cname}</b>
                    <span style='color:#888;font-size:0.8rem;margin-left:6px;'>({len(cdata['members'])}명){my_mark}</span>
                  </div>
                  <span style='color:{nw_col};font-weight:900;font-size:1.1rem;'>{format_korean_money(total)}</span>
                </div>
                """, unsafe_allow_html=True)

# =====================================================================
# 🎴 가챠 뽑기
# =====================================================================
elif menu == "🎴 가챠 뽑기":
    st.title("🎴 가챠 뽑기")
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(180,0,255,0.1),rgba(0,0,180,0.1));
         border:2px solid rgba(180,0,255,0.4);border-radius:16px;padding:20px;text-align:center;margin-bottom:16px;'>
      <div style='font-size:2rem;'>🎴</div>
      <div style='font-size:1.3rem;font-weight:900;color:#FF00FF;margin-top:8px;'>시즌 {market.get('season_num',1)} 한정 가챠</div>
      <div style='color:#888;font-size:0.85rem;margin-top:6px;'>1회당 {format_korean_money(GACHA_TICKET_PRICE)} | 전설 칭호 획득 시 서버 전체 공지!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 아이템 확률표")
    grade_summary = {}
    for item in GACHA_POOL:
        g = item['grade']
        grade_summary[g] = grade_summary.get(g, 0) + item['weight']
    total_weight = sum(grade_summary.values())

    rows_html = "<table class='stock-table'><thead><tr><th>등급</th><th style='text-align:right;'>확률</th></tr></thead><tbody>"
    for grade, w in grade_summary.items():
        pct = w / total_weight * 100
        rows_html += f"<tr><td>{grade}</td><td style='text-align:right;color:#FFD600;font-weight:900;'>{pct:.1f}%</td></tr>"
    rows_html += "</tbody></table>"
    st.markdown(rows_html, unsafe_allow_html=True)

    st.write("---")

    pull_count = st.selectbox(
        "뽑기 횟수",
        [1, 5, 10],
        format_func=lambda x: f"{x}회 ({format_korean_money(GACHA_TICKET_PRICE * x)})"
    )
    total_cost = GACHA_TICKET_PRICE * pull_count
    st.caption(f"총 비용: {format_korean_money(total_cost)}")

    cd_gacha = cooldown_remaining("gacha_pull", 3.0)
    if cd_gacha > 0:
        st.warning(f"⏱️ 쿨다운 {cd_gacha:.1f}초")
    elif st.button(f"🎴 {pull_count}회 뽑기!", use_container_width=True):
        if st.session_state.global_cash < total_cost:
            st.error("잔액 부족!")
        else:
            set_cooldown("gacha_pull")
            st.session_state.global_cash -= total_cost

            weights = [item['weight'] for item in GACHA_POOL]
            results = random.choices(range(len(GACHA_POOL)), weights=weights, k=pull_count)

            got_legendary = False
            result_html   = ""
            for idx in results:
                item = GACHA_POOL[idx]
                grade_col = (
                    "#FFD600" if "전설" in item['grade'] else
                    "#00E5FF" if "희귀" in item['grade'] else
                    "#00FF88" if "일반" in item['grade'] else "#888"
                )
                if item['name'] not in st.session_state.inventory:
                    st.session_state.inventory.append(item['name'])

                # ▼ 들여쓰기 문제를 없애기 위해 한 줄로 깔끔하게 합쳤습니다.
                result_html += f"<div style='background:rgba(255,255,255,0.04);border:1px solid {grade_col}44;border-radius:10px;padding:12px 16px;margin:6px 0;display:flex;justify-content:space-between;align-items:center;'><span style='color:{grade_col};font-weight:900;'>{item['grade']}</span><span style='color:#E2E8F0;font-weight:900;'>{item['name']}</span></div>"
                if "전설" in item['grade']:
                    got_legendary = True
                    market['news'] = f"🎴 [가챠 대박] {st.session_state.logged_in_user}님이 전설 [{item['name']}] 획득!!"
                    save_market(market)

            st.markdown(f"<div style='margin:16px 0;'>{result_html}</div>", unsafe_allow_html=True)
            log_tx(st.session_state.logged_in_user, "가챠", f"가챠 {pull_count}회 뽑기", -total_cost)
            sync_user_data()

            if got_legendary:
                st.balloons()
                st.success("🎉 전설 등급 획득! 칭호 상점에서 장착하세요!")
            else:
                st.success("✅ 뽑기 완료! 칭호 상점에서 장착할 수 있습니다.")

# =====================================================================
# 🛠️ 창조주 통제소
# =====================================================================
elif menu == "🛠️ 창조주 통제소":
    st.title("🛠️ 창조주 통제소")
    st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;margin-bottom:10px;'>⚠️ 창조주 전용 패널입니다. 이곳의 모든 조작은 우주(서버) 전체에 즉시 반영됩니다.</div>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs([
        "👤 유저 개조", "🏢 부동산 통제", "💬 게시판 관리", "🌍 글로벌 정책",
        "📈 시장 조작", "📊 전체 현황", "👁️ 전지적 모니터링", "🏎️ 차고지 조작",
        "🏆 시즌 관리", "📩 쪽지 감시"
    ])

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
        uid_list = [u for u in u_db.keys() if u != "admin"]

        # 기존 평문 비밀번호 → 해시 자동 마이그레이션
        u_db_migrate = load_db(USERS_FILE, {})
        migrated = False
        for _uid, _udata in u_db_migrate.items():
            if _uid == "admin": continue
            pw_val = _udata.get('pw', '')
            if len(pw_val) != 64:  # sha256 hexdigest는 항상 64자
                u_db_migrate[_uid]['pw'] = hash_pw(pw_val)
                migrated = True
        if migrated:
            save_db(USERS_FILE, u_db_migrate)
            

        if uid_list:
            sel_u  = st.selectbox("조작할 유저 선택", uid_list, key="admin_sel_u")
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

            c_btn1, c_btn2, c_btn3 = st.columns(3)
            if c_btn1.button("🔥 유저 데이터 강제 개조", use_container_width=True):
                u_db[sel_u]['cash'] = final_cash
                u_db[sel_u]['loan'] = final_loan
                u_db[sel_u]['equipped_title'] = new_title
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 유저 조작 완료!"); st.rerun()
            
            if c_btn2.button("🕊️ 신용 대사면 (빚 전액 탕감)", use_container_width=True):
                u_db[sel_u]['loan'] = 0
                if u_db[sel_u]['equipped_title'] == "💸 신용불량자": u_db[sel_u]['equipped_title'] = "🌱 신규시민"
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 유저의 빚을 모두 탕감했습니다!"); st.rerun()

            if c_btn3.button("🗑️ 해당 유저 계정 삭제", use_container_width=True, type="secondary"):
                del u_db[sel_u]; save_db(USERS_FILE, u_db); st.rerun()
                
            st.write("---")
            st.markdown("##### 🗡️ 전설의 명검 강제 통제소")
            c_w1, c_w2, c_w3 = st.columns(3)
            
            if c_w1.button("👑 신의 망치 (+15강 투척)", use_container_width=True):
                u_db[sel_u]['weapon_level'] = 15
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}에게 엑스칼리버를 하사했습니다!"); st.rerun()
                
            if c_w2.button("💀 파괴의 저주 (다음 강화 무조건 파괴)", use_container_width=True):
                u_db[sel_u]['cursed_forge'] = True
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}의 무기에 저주를 내렸습니다!"); st.rerun()
                
            if c_w3.button("🔨 무기 강제 압수 (0강으로)", use_container_width=True):
                u_db[sel_u]['weapon_level'] = 0
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}의 무기를 분쇄했습니다!"); st.rerun()

            st.write("---")
            st.markdown("##### 🎒 인벤토리 강제 조작")
            give_title = st.text_input("지급할 칭호명 입력", placeholder="예: 👑 [유일무이] 테스트", key="give_title_input")
            gc1, gc2 = st.columns(2)
            if gc1.button("🎁 칭호 강제 지급 + 장착", use_container_width=True):
                if give_title.strip():
                    u_db[sel_u].setdefault('inventory', [])
                    if give_title not in u_db[sel_u]['inventory']:
                        u_db[sel_u]['inventory'].append(give_title)
                    u_db[sel_u]['equipped_title'] = give_title
                    save_db(USERS_FILE, u_db)
                    st.success(f"✅ {sel_u}에게 [{give_title}] 지급 + 장착 완료!")
                    st.rerun()
            if gc2.button("🗑️ 인벤토리 전체 초기화", use_container_width=True, type="secondary"):
                u_db[sel_u]['inventory'] = []
                u_db[sel_u]['equipped_title'] = "🌱 신규시민"
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 인벤토리 초기화 완료!")
                st.rerun()

            st.write("---")
            st.markdown("##### 🪙 코인/주식 포트폴리오 강제 초기화")
            pa1, pa2, pa3 = st.columns(3)
            if pa1.button("📈 주식 포트폴리오 초기화", use_container_width=True):
                u_db[sel_u]['portfolio'] = {}
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 주식 포트폴리오 초기화!"); st.rerun()
            if pa2.button("🪙 코인 포트폴리오 초기화", use_container_width=True):
                u_db[sel_u]['crypto_portfolio'] = {}
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 코인 포트폴리오 초기화!"); st.rerun()
            if pa3.button("📅 일퀘 강제 초기화", use_container_width=True):
                u_db[sel_u]['daily_quests'] = {}
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 일퀘 초기화!"); st.rerun()

        else:
            st.info("관리할 유저가 없습니다.")

    with t2:
        u_db   = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "admin"]
        # 1. 부동산 신규 공급 물량 조작 (새로 추가된 기능!)
        st.markdown("### 🏗️ 부동산 신규 공급량(초기 재고) 조작")
        st.caption("운영사 직판 물량(initial_stock)을 늘리거나 줄여서 시장에 개입합니다.")
        
        em_admin = load_estate_market()
        initial_stock_data = em_admin.get("initial_stock", {eid: info["total_supply"] for eid, info in estate_config.items()})
        
        c_sup1, c_sup2, c_sup3, c_sup4 = st.columns([3, 2, 2, 2])
        
        with c_sup1:
            sup_eid = st.selectbox(
                "조작할 매물 선택", 
                list(estate_config.keys()), 
                format_func=lambda x: f"{estate_config[x]['icon']} {estate_config[x]['name']} (기본공급: {estate_config[x]['total_supply']}개)"
            )
        
        owned_total = sum(v.get(sup_eid, 0) for v in em_admin["owner_counts"].values())
        listed_count = sum(1 for l in em_admin["listings"] if l["eid"] == sup_eid)
        initial_released = owned_total + listed_count
        
        current_limit = initial_stock_data.get(sup_eid, estate_config[sup_eid]["total_supply"])
        remaining_sup = max(0, current_limit - initial_released)
        
        with c_sup2:
            st.write("")
            st.markdown(f"**현재 설정 한도:** {current_limit}개")
            st.markdown(f"**마켓 잔여 물량:** <b style='color:#00FF88;'>{remaining_sup}개</b>", unsafe_allow_html=True)
            
        with c_sup3:
            sup_mod = st.number_input("조작 수량 (개)", min_value=1, step=1, value=1)
            
        with c_sup4:
            st.write("")
            st.write("")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("➕ 늘리기", use_container_width=True):
                    initial_stock_data[sup_eid] = current_limit + sup_mod
                    em_admin["initial_stock"] = initial_stock_data
                    save_estate_market(em_admin)
                    market['news'] = f"🏗️ [운영사 공지] {estate_config[sup_eid]['name']} 신규 분양 물량이 {sup_mod}개 추가되었습니다!"
                    save_market(market)
                    st.success("물량 추가 완료!")
                    st.rerun()
            with col_b:
                if st.button("➖ 줄이기", use_container_width=True):
                    new_limit = max(initial_released, current_limit - sup_mod)
                    initial_stock_data[sup_eid] = new_limit
                    em_admin["initial_stock"] = initial_stock_data
                    save_estate_market(em_admin)
                    st.success("물량 축소 완료!")
                    st.rerun()

        st.write("---")

        # 2. 기존 특정 유저 부동산 압수 (몰수)
        st.markdown("### 🏢 특정 유저 부동산 강제 압수 (몰수)")
        if uid_list:
            re_target = st.selectbox("압수할 대상 유저", uid_list, key="re_target_u")
            u_re = u_db[re_target].get('real_estate', {})
            
            if not u_re:
                st.info(f"{re_target} 유저는 보유 중인 부동산이 없습니다.")
            else:
                c1, c2, c3 = st.columns([3, 2, 2])
                with c1:
                    re_eid = st.selectbox("압수할 매물 선택", list(u_re.keys()), format_func=lambda x: f"{estate_config[x]['icon']} {estate_config[x]['name']} (보유: {u_re[x]}채)")
                with c2:
                    re_cnt = st.number_input("압수할 수량", min_value=1, max_value=u_re[re_eid], step=1)
                with c3:
                    st.write("") 
                    st.write("")
                    if st.button("🔨 강제 압수 실행", use_container_width=True):
                        u_db[re_target]['real_estate'][re_eid] -= re_cnt
                        if u_db[re_target]['real_estate'][re_eid] <= 0:
                            del u_db[re_target]['real_estate'][re_eid]
                        save_db(USERS_FILE, u_db)

                        if re_target in em_admin["owner_counts"] and re_eid in em_admin["owner_counts"][re_target]:
                            em_admin["owner_counts"][re_target][re_eid] -= re_cnt
                            if em_admin["owner_counts"][re_target][re_eid] <= 0:
                                del em_admin["owner_counts"][re_target][re_eid]
                        save_estate_market(em_admin)

                        st.toast(f"✅ {re_target} 유저의 부동산 환수 완료!", icon="🏢")
                        st.rerun()
        else:
             st.info("관리할 유저가 없습니다.")

        st.write("---")
        
        # 3. 유저 등록 중고 매물 강제 삭제
        st.markdown("### 🔄 유저 등록 중고 매물 강제 삭제")
        if em_admin["listings"]:
            for li in em_admin["listings"]:
                info = estate_config.get(li["eid"], {})
                ca, cb = st.columns([5, 1])
                ca.markdown(f"**{info.get('icon','')} {info.get('name','?')}** — 판매자: `{li['seller']}` — {format_korean_money(li['price'])}")
                if cb.button("강제삭제", key=f"admin_del_re_{li['id']}"):
                    em_admin["listings"] = [x for x in em_admin["listings"] if x["id"] != li["id"]]
                    save_estate_market(em_admin); st.rerun()
        else:
            st.info("현재 유저가 등록한 중고 매물이 없습니다.")
            
        st.write("---")
        
        # 4. 부동산 마켓 전체 초기화
        st.markdown("### 💣 부동산 마켓 전체 초기화")
        if st.button("🔄 부동산 마켓 전체 초기화 (경매장 싹쓸이 & 전 유저 몰수 & 공급량 리셋)", type="secondary"):
            # 1. 마켓 DB 초기화
            save_estate_market({"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}})
            
            # 2. 모든 유저의 개인 부동산 보유 내역 싹쓸이
            u_db_reset = load_db(USERS_FILE, {})
            now_time = time.time()
            for uid_k in u_db_reset:
                u_db_reset[uid_k]['real_estate'] = {} 
                u_db_reset[uid_k]['rent_time'] = now_time 
            save_db(USERS_FILE, u_db_reset)
            
            # 3. 현재 접속 중인 창조주(어드민) 세션 동기화
            st.session_state.real_estate = {}
            st.session_state.rent_time = now_time
            
            # 👇 [핵심] 접속 중인 다른 유저들의 브라우저도 털어버리도록 마켓에 '리셋 신호'를 발송!
            market['force_estate_reset'] = now_time
            save_market(market)
            
            st.toast("💣 부동산 마켓 초기화 완료!", icon="💣")
            st.rerun()

    with t3:
        st.markdown("### 💬 게시판 개별/전체 관리")
        all_c = load_db(COMMENTS_FILE, [])
        
        c1, c2 = st.columns([4, 1])
        c1.write(f"총 {len(all_c)}개의 게시물이 있습니다.")
        if c2.button("💣 게시판 전체 초기화", use_container_width=True):
            save_db(COMMENTS_FILE, []); st.success("초기화 완료!"); st.rerun()
            
        st.write("---")
        if not all_c:
            st.info("등록된 게시물이 없습니다.")
        else:
            for idx, c in reversed(list(enumerate(all_c))):
                col_txt, col_btn = st.columns([6, 1])
                with col_txt:
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;'><b style='color:#00E5FF;'>{c['name']}</b>: {c['comment']} <span style='color:#888; font-size:0.8rem;'>({c.get('time','')})</span></div>", unsafe_allow_html=True)
                with col_btn:
                    if st.button("🗑️ 삭제", key=f"del_board_{idx}", use_container_width=True):
                        all_c.pop(idx) 
                        save_db(COMMENTS_FILE, all_c)
                        st.rerun()

    with t4:
        st.markdown("### 🕊️ 창조주의 은총 (에어드랍)")
        st.caption("모든 유저(관리자 제외)에게 동일한 현금을 일괄 지급합니다.")
        airdrop_amt = st.number_input("지급할 금액", min_value=0, step=10_000_000, value=100_000_000)
        if st.button("💸 전 우주에 현금 살포하기", use_container_width=True):
            for u in u_db:
                if u != "admin": u_db[u]['cash'] += airdrop_amt
            save_db(USERS_FILE, u_db)
            market['news'] = f"🕊️ [창조주의 은총] 모든 시민에게 {format_korean_money(airdrop_amt)}이 지급되었습니다!"
            save_market(market); st.toast("에어드랍 완료!", icon="🕊️"); st.rerun()

        st.write("---")
        st.markdown("### 🔇 특정 유저 게시판 이용 정지")
        st.caption("해당 유저의 게시판 글을 전부 삭제하고 블랙리스트에 등록합니다.")
        ban_target = st.selectbox("정지할 유저", [u for u in load_db(USERS_FILE, {}).keys() if u != "admin"], key="ban_target")
        if st.button("🔇 게시판 이용 정지 (글 전삭)", use_container_width=True):
            all_c = load_db(COMMENTS_FILE, [])
            before = len(all_c)
            all_c = [c for c in all_c if c['name'] != ban_target]
            save_db(COMMENTS_FILE, all_c)
            market_ban = get_market()
            market_ban.setdefault('board_banned', [])
            if ban_target not in market_ban['board_banned']:
                market_ban['board_banned'].append(ban_target)
            save_market(market_ban)
            st.success(f"✅ {ban_target} 글 {before - len(all_c)}개 삭제 + 이용 정지!")
            st.rerun()

        if st.button("🔓 게시판 이용 정지 해제", use_container_width=True):
            market_ban = get_market()
            if ban_target in market_ban.get('board_banned', []):
                market_ban['board_banned'].remove(ban_target)
                save_market(market_ban)
                st.success(f"✅ {ban_target} 이용 정지 해제!")
                st.rerun()

        st.write("---")
        st.markdown("### 📢 긴급 서버 점검 공지")
        if st.button("🚨 서버 점검 공지 발령 (모든 유저 화면에 표시)", use_container_width=True):
            market['admin_msg'] = "🚨 현재 서버 점검 중입니다. 잠시 후 다시 접속해주세요."
            market['admin_color'] = "#FF0000"
            save_market(market)
            st.success("점검 공지 발령 완료!")
            st.rerun()

        st.write("---")
        st.markdown("### 🌪️ 창조주의 분노 (부유세 강제 징수)")
        st.caption("모든 유저(관리자 제외)의 현재 '현금'에서 설정한 퍼센트(%)만큼을 강제로 징수합니다.")
        tax_rate = st.slider("징수율 (%)", min_value=1, max_value=99, value=10)
        if st.button("🌪️ 전 우주 부유세 징수 실행", use_container_width=True):
            for u in u_db:
                if u != "admin":
                    tax_amount = int(u_db[u]['cash'] * (tax_rate / 100.0))
                    u_db[u]['cash'] -= tax_amount
            save_db(USERS_FILE, u_db)
            market['news'] = f"🌪️ [창조주의 분노] 전 우주를 대상으로 {tax_rate}%의 부유세가 강제 징수되었습니다!"
            save_market(market); st.toast("세금 징수 완료!", icon="🌪️"); st.rerun()

        st.write("---")
        st.markdown("### 🏰 클랜 강제 해산")
        clans_admin = load_clan_db()
        if clans_admin:
            clan_del_target = st.selectbox(
                "해산할 클랜 선택",
                list(clans_admin.keys()),
                format_func=lambda n: f"{clans_admin[n]['icon']} {n} ({len(clans_admin[n]['members'])}명)",
                key="clan_del_select"
            )
            cd1, cd2 = st.columns(2)
            if cd1.button("💣 클랜 강제 해산", use_container_width=True, type="secondary"):
                del clans_admin[clan_del_target]
                save_clan_db(clans_admin)
                market['news'] = f"💣 [창조주의 심판] [{clan_del_target}] 클랜이 강제 해산되었습니다!"
                save_market(market)
                st.success(f"✅ {clan_del_target} 클랜 해산 완료!"); st.rerun()
            if cd2.button("🏦 클랜 은행 전액 몰수", use_container_width=True):
                seized = clans_admin[clan_del_target].get('bank', 0)
                clans_admin[clan_del_target]['bank'] = 0
                save_clan_db(clans_admin)
                st.success(f"✅ {format_korean_money(seized)} 몰수 완료!"); st.rerun()
        else:
            st.info("현재 존재하는 클랜이 없습니다.")

        # ---------------------------------------------------------
        # 🏹 유저 클랜 강제 조정 (추가된 부분)
        # ---------------------------------------------------------
        st.write("---")
        st.markdown("### 🏹 유저 클랜 강제 조정")
        st.caption("특정 유저를 다른 클랜으로 강제 이동시키거나 무소속으로 만듭니다.")

        all_users_list = [u for u in u_db.keys() if u != "admin"]
        all_clans_data = load_clan_db()

        if all_users_list:
            c_move1, c_move2 = st.columns(2)
            with c_move1:
                target_u = st.selectbox("조정할 유저 선택", all_users_list, key="admin_move_user")
                current_c = get_user_clan(target_u)
                st.markdown(f"현재 상태: <b style='color:#00E5FF;'>{current_c if current_c else '무소속'}</b>", unsafe_allow_html=True)

            with c_move2:
                dest_c = st.selectbox("이동시킬 대상 클랜", ["🚫 무소속으로 방출"] + list(all_clans_data.keys()), key="admin_move_dest")

            if st.button("⚡ 클랜 소속 강제 변경 실행", use_container_width=True):
                # 1. 기존 클랜에서 제거 로직
                if current_c:
                    all_clans_data[current_c]['members'] = [m for m in all_clans_data[current_c]['members'] if m != target_u]
                    if all_clans_data[current_c]['leader'] == target_u:
                        if all_clans_data[current_c]['members']:
                            all_clans_data[current_c]['leader'] = all_clans_data[current_c]['members'][0]
                        else:
                            del all_clans_data[current_c]

                # 2. 새 클랜으로 전입 혹은 방출
                if dest_c == "🚫 무소속으로 방출":
                    msg = f"🍃 [창조주의 명령] {target_u}님이 클랜에서 방출되어 무소속이 되었습니다."
                else:
                    if target_u not in all_clans_data[dest_c]['members']:
                        all_clans_data[dest_c]['members'].append(target_u)
                    msg = f"🏹 [창조주의 명령] {target_u}님이 [{dest_c}] 클랜으로 강제 전입되었습니다."

                save_clan_db(all_clans_data)
                market['news'] = msg
                save_market(market)
                st.success("✅ 유저 소속 변경 완료!")
                st.rerun()

    

    with t5:
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

        st.write("---")
        st.markdown("### 📢 공지사항 & 이벤트")
        msg_text  = st.text_area("공지 내용", value=market.get('admin_msg', ''), height=70)
        msg_color = st.color_picker("텍스트 색상", value=market.get('admin_color', '#FF4B4B'))
        cc1, cc2 = st.columns(2)
        if cc1.button("📣 공지 발령", use_container_width=True):
            market['admin_msg'] = msg_text; market['admin_color'] = msg_color; save_market(market); st.success("완료!")
        if cc2.button("🗑️ 공지 삭제", use_container_width=True):
            market['admin_msg'] = ""; save_market(market); st.success("완료!")

        st.write("---")
        st.markdown("### 🎰 로또 강제 조작")
        st.metric("현재 로또 풀", format_korean_money(market.get('lotto_pool', 0)))
        lc1, lc2 = st.columns(2)
        with lc1:
            lotto_add = st.number_input("로또 풀 추가 금액", min_value=0, step=1_000_000_000, value=1_000_000_000, format="%d")
            if st.button("💰 로또 풀 금액 추가", use_container_width=True):
                market['lotto_pool'] += lotto_add
                save_market(market)
                st.success(f"✅ {format_korean_money(lotto_add)} 추가! 현재: {format_korean_money(market['lotto_pool'])}"); st.rerun()
        with lc2:
            if st.button("🎊 로또 즉시 강제 추첨", use_container_width=True):
                market['lotto_last_draw'] = 0
                save_market(market)
                st.success("✅ 다음 렌더링에서 즉시 추첨됩니다!"); st.rerun()
            if st.button("🗑️ 로또 티켓 전체 초기화", use_container_width=True, type="secondary"):
                market['lotto_tickets'] = {}
                market['lotto_pool'] = 5_000_000_000
                save_market(market)
                st.success("✅ 로또 초기화 완료!"); st.rerun()

    with t6:
        u_db2 = load_db(USERS_FILE, {})
        total_users = len([u for u in u_db2.keys() if u != "admin"])
        
        st.markdown(f"### 📈 누적 가입(접속) 유저 수: <b style='color:#00E5FF; font-size:1.8rem;'>{total_users}명</b>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### 📊 전체 유저 현황")
        rows = [{"ID": uid_r, "칭호": ud.get('equipped_title',''), "현금": format_korean_money(ud.get('cash',0)), "무기": f"+{ud.get('weapon_level',0)}강", "대출": format_korean_money(ud.get('loan',0))} for uid_r, ud in u_db2.items() if uid_r != "admin"]
        if rows: st.table(pd.DataFrame(rows))
        else: st.info("등록된 유저가 없습니다.")

        st.write("---")
        st.markdown("### 💾 데이터베이스 파일 상태")
        for f in [USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE, REALESTATE_MARKET_FILE]:
            exists = "✅ 정상" if os.path.exists(f) else "❌ 없음"
            size = f"{os.path.getsize(f):,} bytes" if os.path.exists(f) else "—"
            st.markdown(f"<div style='color:#ccc;font-size:0.9rem;'>{exists} | <b>{f}</b> ({size})</div>", unsafe_allow_html=True)
            
        st.write("---")
        st.markdown("### 🚨 긴급 데이터 백업 (다운로드)")
        
        # 파일이 존재하면 다운로드 버튼 생성
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "rb") as f:
                st.download_button("📥 유저 데이터 (users_db) 백업", f, file_name=f"backup_{USERS_FILE}", mime="application/json")
                
        if os.path.exists(MARKET_FILE):
            with open(MARKET_FILE, "rb") as f:
                st.download_button("📥 시장 데이터 (market_db) 백업", f, file_name=f"backup_{MARKET_FILE}", mime="application/json")
                
        if os.path.exists(REALESTATE_MARKET_FILE):
            with open(REALESTATE_MARKET_FILE, "rb") as f:
                st.download_button("📥 부동산 데이터 백업", f, file_name=f"backup_{REALESTATE_MARKET_FILE}", mime="application/json")

        st.write("---")
        st.markdown("### 👑 히든 칭호 발급 현황")
        st.caption("초기화하면 해당 칭호를 다음 달성자가 다시 받을 수 있습니다.")
        hidden_titles = market.get('hidden_titles', {})
        if not hidden_titles:
            st.info("아직 발급된 히든 칭호가 없습니다.")
        else:
            for tid, owner in list(hidden_titles.items()):
                hc1, hc2 = st.columns([4, 1])
                hc1.markdown(f"**{tid}** → <b style='color:#00E5FF;'>{owner}</b>", unsafe_allow_html=True)
                if hc2.button("🔄 초기화", key=f"reset_hidden_{tid}", use_container_width=True):
                    del market['hidden_titles'][tid]
                    save_market(market)
                    st.success(f"✅ {tid} 칭호 발급 기록 초기화!")
                    st.rerun()

    with t7:
        c_title, c_btn = st.columns([5, 1])
        with c_title:
            st.markdown("### 👁️ 실시간 유저 활동 로그")
            st.caption("우주에서 일어나는 모든 거래의 은밀한 기록입니다.")
        with c_btn:
            if st.button("🔄 새로고침", use_container_width=True):
                st.rerun()

        all_logs = load_db(TXLOG_FILE, {})
        
        combined_logs = []
        for user_id, user_logs in all_logs.items():
            for log in user_logs:
                log['uid'] = user_id  
                combined_logs.append(log)
                
        combined_logs.sort(key=lambda x: x['time'], reverse=True)
        
        if not combined_logs:
            st.info("아직 기록된 활동이 없습니다.")
        else:
            for log in combined_logs[:100]:
                amt   = log['amount']
                color = "#FF4B4B" if amt > 0 else "#4B9EFF"
                sign  = "+" if amt > 0 else ""
                st.markdown(f"""
                <div style='font-size:0.85rem; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.05);'>
                    <span style='color:#777;'>[{log['time']}]</span> 
                    <b style='color:#00E5FF;'>{log['uid']}</b>님이 
                    <span style='color:#94A3B8;'>{log['desc']}</span> 
                    <b style='color:{color};'>({sign}{format_korean_money(amt)})</b>
                </div>
                """, unsafe_allow_html=True)
    with t8:
        st.markdown("### 🏎️ 유저 차량 강제 개조 및 통제")
        st.caption("특정 유저의 차량을 압수하거나, 강제로 사고를 내서 수리비를 물게 할 수 있습니다.")

        u_db_car = load_db(USERS_FILE, {})
        uid_list_car = [u for u in u_db_car.keys() if u != "admin"]

        CAR_TIERS_ADMIN = [
            {"tier": "0", "name": "2021년형 컴팩트 박스카"},
            {"tier": "1", "name": "터보차저 스포츠 세단"},
            {"tier": "2", "name": "V12 럭셔리 하이퍼카"},
            {"tier": "3", "name": "🌌 우주 뚫은 은하철도"}
        ]

        if uid_list_car:
            car_target = st.selectbox("조작할 대상 유저", uid_list_car, key="car_target_u")
            raw_garage = u_db_car[car_target].get('garage', {})

            is_new_structure = 'cars' in raw_garage and isinstance(raw_garage['cars'], dict)

            if is_new_structure:
                garage_cars = raw_garage.get('cars', {})
                active_t    = raw_garage.get('active_tier', None)
            else:
                if raw_garage.get('owned', False):
                    t = str(raw_garage.get('tier', 0))
                    garage_cars = {
                        t: {
                            "engine_lv":     raw_garage.get('engine_lv', 0),
                            "suspension_lv": raw_garage.get('suspension_lv', 0),
                            "bumper_lv":     raw_garage.get('bumper_lv', 0),
                            "needs_repair":  raw_garage.get('needs_repair', False),
                        }
                    }
                    active_t = t
                else:
                    garage_cars = {}
                    active_t    = None

            if not garage_cars:
                st.info(f"{car_target} 유저는 아직 차량을 소유하고 있지 않습니다.")
                if st.button("🚀 우주 끝판왕 하이퍼카 꽂아주기", use_container_width=True):
                    u_db_car[car_target]['garage'] = {
                        'cars': {
                            '3': {"engine_lv": 5, "suspension_lv": 5, "bumper_lv": 5, "needs_repair": False}
                        },
                        'active_tier': '3'
                    }
                    save_db(USERS_FILE, u_db_car)
                    st.success(f"✅ {car_target}님에게 풀튜닝 우주선을 하사했습니다!")
                    st.rerun()
            else:
                owned_tiers = list(garage_cars.keys())
                sel_view_t  = st.selectbox(
                    "조작할 차량 선택",
                    owned_tiers,
                    format_func=lambda t: f"Tier {t} — {next((c['name'] for c in CAR_TIERS_ADMIN if c['tier']==t), '알 수 없음')}"
                )
                parts       = garage_cars[sel_view_t]
                repair_cost = 8_700_000_000 * (10 ** int(sel_view_t))

                c_car1, c_car2 = st.columns(2)
                with c_car1:
                    st.markdown(f"**현재 등급:** Tier {sel_view_t} — {next((c['name'] for c in CAR_TIERS_ADMIN if c['tier']==sel_view_t), '?')}")
                    st.markdown(f"**튜닝 레벨:** 엔진({parts.get('engine_lv',0)}) / 서스({parts.get('suspension_lv',0)}) / 범퍼({parts.get('bumper_lv',0)})")
                    st.markdown(f"**사고(파손) 상태:** {'🚨 파손됨 (수리필요)' if parts.get('needs_repair') else '✅ 정상'}")
                    st.markdown(f"**메인 차량 여부:** {'⭐ 메인' if active_t == sel_view_t else '서브'}")

                with c_car2:
                    if st.button(f"💥 강제 후방 추돌 사고 발생 (수리비 {format_korean_money(repair_cost)} 청구)", use_container_width=True):
                        u_db_car[car_target]['garage']['cars'][sel_view_t]['needs_repair'] = True
                        save_db(USERS_FILE, u_db_car)
                        market['news'] = f"🚨 [교통사고] {car_target}님의 차량이 누군가의 테러로 대파되었습니다!"
                        save_market(market)
                        st.toast(f"✅ {car_target}님의 차량 대파 완료!", icon="💥")
                        st.rerun()

                    if st.button("🔧 파손 상태 무상 수리 (창조주의 은혜)", use_container_width=True):
                        u_db_car[car_target]['garage']['cars'][sel_view_t]['needs_repair'] = False
                        save_db(USERS_FILE, u_db_car)
                        st.success(f"✅ {car_target}님의 차량을 무상으로 고쳐주었습니다!")
                        st.rerun()

                    if st.button("🗑️ 선택 차량 강제 폐차 (고철로 만들기)", use_container_width=True, type="secondary"):
                        del u_db_car[car_target]['garage']['cars'][sel_view_t]
                        remaining = list(u_db_car[car_target]['garage']['cars'].keys())
                        u_db_car[car_target]['garage']['active_tier'] = remaining[0] if remaining else None
                        save_db(USERS_FILE, u_db_car)
                        st.toast(f"✅ Tier {sel_view_t} 차량 폐차 완료!", icon="🗑️")
                        st.rerun()
        else:
            st.info("관리할 유저가 없습니다.")   # ← 여기로 이동 (uid_list_car가 비었을 때만 표시)
    with t9:
        st.markdown("### 🏆 시즌 관리")
        cur_season    = market.get('season_num', 1)
        season_end_ts = market.get('season_end', 0)
        season_end_dt = datetime.fromtimestamp(season_end_ts, KST).strftime("%Y-%m-%d %H:%M")
        remain_sec    = max(0, int(season_end_ts - time.time()))
        remain_day    = remain_sec // 86400
        remain_hr     = (remain_sec % 86400) // 3600

        st.markdown(f"""
        <div style='background:rgba(0,229,255,0.08);border:1px solid #00E5FF;
             border-radius:12px;padding:20px;margin-bottom:16px;'>
          <div style='color:#888;font-size:0.82rem;'>현재 시즌</div>
          <div style='font-size:2rem;font-weight:900;color:#FFD600;'>시즌 {cur_season}</div>
          <div style='color:#94A3B8;margin-top:8px;'>종료 예정: <b style='color:#FF00FF;'>{season_end_dt}</b></div>
          <div style='color:#94A3B8;'>잔여: <b style='color:#00FF88;'>{remain_day}일 {remain_hr}시간</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📅 시즌 종료일 수동 조정")
        new_days = st.number_input("지금부터 몇 일 후에 시즌 종료?", min_value=1, max_value=90, value=30)
        if st.button("📅 시즌 종료일 변경", use_container_width=True):
            market['season_end'] = time.time() + new_days * 86400
            save_market(market)
            st.success(f"✅ {new_days}일 후로 시즌 종료일 설정 완료!")
            st.rerun()

        st.write("---")
        st.markdown("### ⚡ 시즌 즉시 강제 종료")
        st.caption("⚠️ 지금 즉시 시즌 종료 + 랭킹 보상 지급 + 전체 리셋 실행")
        if st.button("💣 시즌 즉시 종료 & 리셋 실행", use_container_width=True, type="secondary"):
            market['season_end'] = time.time() - 1
            save_market(market)
            st.success("✅ 다음 렌더링에서 시즌이 종료됩니다. 잠시 후 새로고침하세요!")

        st.write("---")
        st.markdown("### 📜 역대 시즌 기록")
        records = market.get('season_records', {})
        if not records:
            st.info("아직 완료된 시즌이 없습니다.")
        else:
            for sn, rec in sorted(records.items(), key=lambda x: int(x[0]), reverse=True):
                st.markdown(f"""
                **시즌 {sn}**
                - 🥇 1위: {rec.get('rank1','?')}
                - 🥈 2위: {rec.get('rank2','?')}
                - 🥉 3위: {rec.get('rank3','?')}
                """)


# ── [t10] 쪽지 감시 (창조주 전용) ──
    with t10:
        st.markdown("### 👁️ 전지적 쪽지 모니터링")
        st.caption("우주 내에서 오가는 모든 비밀 쪽지를 감시합니다. 삭제 및 초기화 권한이 있습니다.")

        all_msg_db = load_db("messages_db.json", {})
        
        if not all_msg_db:
            st.info("현재 우주에 생성된 쪽지 데이터가 없습니다.")
        else:
            admin_sub_tabs = st.tabs(["🔍 유저별 조회", "📜 전체 로그", "💣 데이터 관리"])

            # 1. 유저별 조회
            with admin_sub_tabs[0]:
                target_u = st.selectbox("조회할 유저 선택", list(all_msg_db.keys()), key="admin_msg_u")
                u_msgs = all_msg_db.get(target_u, {})
                
                col_in, col_out = st.columns(2)
                with col_in:
                    st.markdown(f"**📥 {target_u}의 받은 쪽지**")
                    for m in reversed(u_msgs.get("inbox", [])):
                        st.markdown(f"""
                        <div style='font-size:0.8rem; padding:8px; background:rgba(255,255,255,0.03); border-radius:5px; margin-bottom:5px;'>
                          <b style='color:#00E5FF;'>{m['sender']}</b> → {m['content']} <br>
                          <span style='color:#777;'>{m['time']}</span>
                        </div>""", unsafe_allow_html=True)
                
                with col_out:
                    st.markdown(f"**📤 {target_u}의 보낸 쪽지**")
                    for m in reversed(u_msgs.get("outbox", [])):
                        st.markdown(f"""
                        <div style='font-size:0.8rem; padding:8px; background:rgba(255,255,255,0.03); border-radius:5px; margin-bottom:5px;'>
                          → <b style='color:#FFD600;'>{m['receiver']}</b>: {m['content']} <br>
                          <span style='color:#777;'>{m['time']}</span>
                        </div>""", unsafe_allow_html=True)

            # 2. 전체 로그 (시간순)
            with admin_sub_tabs[1]:
                st.markdown("**🌐 우주 전체 쪽지 타임라인**")
                global_logs = []
                for sender_id, data in all_msg_db.items():
                    for m in data.get("outbox", []):
                        global_logs.append({
                            "time": m['time'],
                            "from": sender_id,
                            "to": m['receiver'],
                            "content": m['content']
                        })
                
                # 시간 역순 정렬
                global_logs.sort(key=lambda x: x['time'], reverse=True)
                
                for log in global_logs[:100]:
                    st.markdown(f"""
                    <div style='font-size:0.85rem; border-bottom:1px solid rgba(255,255,255,0.05); padding:5px 0;'>
                      <span style='color:#777;'>[{log['time']}]</span> 
                      <b style='color:#00E5FF;'>{log['from']}</b> ➔ <b style='color:#FFD600;'>{log['to']}</b> : {log['content']}
                    </div>""", unsafe_allow_html=True)

            # 3. 데이터 관리
            with admin_sub_tabs[2]:
                st.warning("⚠️ 주의: 쪽지 데이터를 삭제하면 복구할 수 없습니다.")
                if st.button("💣 우주 전체 쪽지 DB 초기화", use_container_width=True, type="secondary"):
                    save_db("messages_db.json", {})
                    st.success("전체 쪽지 데이터가 소멸되었습니다.")
                    st.rerun()
