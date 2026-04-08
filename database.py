import json
import os
import shutil
import time
import random
import streamlit as st
from datetime import datetime

from config import (
    USERS_FILE, COMMENTS_FILE, MARKET_FILE, TXLOG_FILE,
    stock_config, estate_config,
)


# ════════════════════════════════════
# DB 유틸 (데이터 소실 방지 버전)
# ════════════════════════════════════
def _atomic_save(filepath: str, data):
    """임시 파일에 쓴 뒤 교체 -> 쓰다 죽어도 원본 보존"""
    tmp = filepath + ".tmp"
    bak = filepath + ".bak"
    try:
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        if os.path.exists(filepath):
            shutil.copy2(filepath, bak)
        shutil.move(tmp, filepath)
    except Exception as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise e


def load_db(file, default):
    """파일 읽기 -- 손상되면 백업에서 복구 시도"""
    for target in [file, file + ".bak"]:
        if os.path.exists(target):
            try:
                with open(target, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if data:
                    return data
            except Exception:
                continue
    return default


def save_db(file, data):
    if data is None:
        return
    if isinstance(data, dict) and len(data) == 0 and file == USERS_FILE:
        return
    _atomic_save(file, data)


# ── 거래 기록 ──
def log_tx(uid: str, category: str, desc: str, amount: int):
    """거래 로그 1건 추가"""
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs:
        logs[uid] = []
    logs[uid].insert(0, {
        "time": datetime.now().strftime("%m/%d %H:%M:%S"),
        "category": category,
        "desc": desc,
        "amount": amount,
    })
    logs[uid] = logs[uid][:200]
    save_db(TXLOG_FILE, logs)


# ── 순자산 계산 ──
def get_net_worth(uid, market_data):
    users = load_db(USERS_FILE, {})
    if uid not in users:
        return 0
    u = users[uid]
    w = u.get('cash', 0) - u.get('loan', 0)
    prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
    for sid, p_data in u.get('portfolio', {}).items():
        if sid in prices:
            w += p_data.get('qty', 0) * prices[sid]
    for eid, count in u.get('real_estate', {}).items():
        if eid in estate_config:
            w += estate_config[eid]['price'] * count * 0.8
    return w


def sync_user_data():
    if 'logged_in_user' not in st.session_state:
        return
    users = load_db(USERS_FILE, {})
    uid = st.session_state.logged_in_user
    if uid not in users:
        return
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
        d = init_m()
        save_db(MARKET_FILE, d)
        return d
    d = load_db(MARKET_FILE, {})
    if d.get("version") != 6:
        d = init_m()
        save_db(MARKET_FILE, d)
        return d
    return d


def save_market(data):
    save_db(MARKET_FILE, data)
