# utils/core.py자산 계산, 돈 포맷팅, 쿨다운 타이머 등 모든 페이지에서 공통으로 쓰는 로직들이 들어갑니다.
import hashlib
import time
import random
import streamlit as st
from utils.config import (
    KST, USERS_FILE, MARKET_FILE, estate_config,
    stock_config, FORGE_DATA, MINE_ITEMS, CRYPTO_CONFIG, DAILY_QUESTS_CONFIG
)
from utils.database import load_db, save_db, load_clan_db

import os
ADMIN_HASH = os.environ.get("ADMIN_HASH", "b573ebf82028a56d9d724124bd51e072b175d160695e2735b0fa4ae5e4c79fd1")
if not ADMIN_HASH:
    raise ValueError("환경변수 ADMIN_HASH가 설정되지 않았습니다. 배포 전 반드시 설정하세요.")

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode('utf-8')).hexdigest()

def format_korean_money(num):
    try:
        if num is None or num != num or num == 0: return "0원"
    except TypeError: return "0원"
    is_neg = num < 0
    num = abs(int(num))
    jo, eok, man, won = num // 10**12, (num % 10**12) // 10**8, (num % 10**8) // 10**4, num % 10**4
    parts = []
    if jo > 0: parts.append(f"{jo:,}조")
    if eok > 0: parts.append(f"{eok:,}억")
    if man > 0: parts.append(f"{man:,}만")
    if won > 0 or not parts: parts.append(f"{won:,}")
    res = " ".join(parts) + "원"
    return f"-{res}" if is_neg else res

def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return 0
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices: w += p_data.get('qty', 0) * prices[sid]
    for cid, cinfo in u.get('crypto_portfolio', {}).items():
        price = market_data.get('crypto_data', {}).get(cid, {}).get('price', 0)
        w += cinfo.get('qty', 0) * price
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
    w_lv = u.get('weapon_level', 0)
    if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
    return w

def sync_user_data():
    if 'logged_in_user' not in st.session_state: return
    users = load_db(USERS_FILE, {})
    uid = st.session_state.logged_in_user
    if uid not in users: return
    users[uid].update({
        'cash': st.session_state.global_cash,
        'inventory': st.session_state.inventory,
        'equipped_title': st.session_state.equipped_title,
        'portfolio': st.session_state.portfolio,
        'real_estate': st.session_state.real_estate,
        'rent_time': st.session_state.rent_time,
        'loan': st.session_state.loan,
        'loan_time': st.session_state.loan_time,
        'crypto_portfolio': st.session_state.get('crypto_portfolio', {}),
        'daily_quests': st.session_state.get('daily_quests', {}),
        'weapon_level': st.session_state.get('weapon_level', 0), 
        'bulk_trade_date': st.session_state.get('bulk_trade_date', ''),
        'bulk_trade_count': st.session_state.get('bulk_trade_count', 0),
        'last_estate_reset': st.session_state.get('last_estate_reset', 0),
    })
    save_db(USERS_FILE, users)

def get_market():
    def init_m():
        return {
            "version": 6,
            "stock_data": {s['id']: {"name": s['name'], "icon": s['icon'], "price": random.randint(50_000, 150_000), "history": [80_000, 80_000]} for s in stock_config},
            "news": "🌌 HYOMIN UNIVERSE 시즌 2 시작!", "news_time": time.time(), "last_tick": time.time(),
            "admin_msg": "", "admin_color": "#FF4B4B", "lotto_pool": 5_000_000_000, "lotto_tickets": {}, "lotto_last_draw": time.time(),
            "next_news_target": random.choice(stock_config)['id'], "next_news_impact": random.uniform(-0.2, 0.2), "event_active": False,
        }
    d = load_db(MARKET_FILE, {})
    if not d or d.get("version") != 6:
        lp, lt, ll = d.get("lotto_pool", 5_000_000_000), d.get("lotto_tickets", {}), d.get("lotto_last_draw", time.time())
        d = init_m()
        d["lotto_pool"], d["lotto_tickets"], d["lotto_last_draw"] = lp, lt, ll
        save_db(MARKET_FILE, d); return d
    return d


def get_clan_total_nw(cname, market_data, users_db=None):
    clans = load_clan_db()
    if cname not in clans: return 0
    if users_db is None: users_db = load_db(USERS_FILE, {})
    total = clans[cname].get('bank', 0)
    for uid in clans[cname].get('members', []): total += get_net_worth(uid, market_data)
    return total

def claim_hidden_title(title_id, title_name):
    uid = st.session_state.logged_in_user
    market = get_market()
    if "hidden_titles" not in market: market["hidden_titles"] = {}
    if title_id not in market["hidden_titles"]:
        market["hidden_titles"][title_id] = uid
        us = load_db(USERS_FILE, {})
        if uid in us:
            if title_name not in us[uid].get('inventory', []):
                us[uid].setdefault('inventory', []).append(title_name)
            us[uid]['equipped_title'] = title_name
            save_db(USERS_FILE, us)
        st.session_state.equipped_title = title_name
        if title_name not in st.session_state.inventory: st.session_state.inventory.append(title_name)
        market['news'] = f"👑 [서버 최초 달성] {uid}님이 전설적인 칭호 '{title_name}'을(를) 거머쥐었습니다!!"
        from utils.database import save_market
        save_market(market)
        st.toast(f"🎉 서버 최초! [{title_name}] 칭호를 획득했습니다!", icon="👑")
        st.balloons(); return True
    return False

def set_cooldown(key: str): st.session_state[f"_cd_{key}"] = time.time()
def cooldown_remaining(key: str, cooldown_sec: float = 2.0) -> float:
    return max(0.0, cooldown_sec - (time.time() - st.session_state.get(f"_cd_{key}", 0)))
