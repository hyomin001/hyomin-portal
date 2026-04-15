# ============================================================
# utils/sync.py — 세션 ↔ DB 동기화 및 순자산 계산
# ============================================================
import time
import streamlit as st

from config import ESTATE_CONFIG, FORGE_DATA, STOCK_CONFIG
from utils.database import load_db, save_db, log_tx, get_market, save_market, USERS_FILE


def get_net_worth(uid: str, market: dict) -> int:
    users = load_db(USERS_FILE, {})
    if uid not in users:
        return 0
    u = users[uid]
    w = u.get("cash", 0) - u.get("loan", 0)

    # 주식
    for sid, p in u.get("portfolio", {}).items():
        price = market.get("stock_data", {}).get(sid, {}).get("price", 0)
        w += p.get("qty", 0) * price

    # 코인
    for cid, ci in u.get("crypto_portfolio", {}).items():
        price = market.get("crypto_data", {}).get(cid, {}).get("price", 0)
        w += ci.get("qty", 0) * price

    # 부동산 (평가액 80%)
    for eid, cnt in u.get("real_estate", {}).items():
        if eid in ESTATE_CONFIG:
            w += ESTATE_CONFIG[eid]["base_price"] * cnt * 0.8

    # 명검
    lv = u.get("weapon_level", 0)
    if lv > 0 and lv in FORGE_DATA:
        w += FORGE_DATA[lv]["sell"]

    return int(w)


def sync_user_data():
    """세션 상태 → DB 동기화 (로그인된 유저에게만 적용)"""
    if "logged_in_user" not in st.session_state:
        return
    users = load_db(USERS_FILE, {})
    uid = st.session_state.logged_in_user
    if uid not in users:
        return

    users[uid].update({
        "cash":              st.session_state.get("global_cash", 0),
        "inventory":         st.session_state.get("inventory", []),
        "equipped_title":    st.session_state.get("equipped_title", "🌱 신규시민"),
        "portfolio":         st.session_state.get("portfolio", {}),
        "real_estate":       st.session_state.get("real_estate", {}),
        "rent_time":         st.session_state.get("rent_time", time.time()),
        "loan":              st.session_state.get("loan", 0),
        "loan_time":         st.session_state.get("loan_time", time.time()),
        "crypto_portfolio":  st.session_state.get("crypto_portfolio", {}),
        "daily_quests":      st.session_state.get("daily_quests", {}),
        "weapon_level":      st.session_state.get("weapon_level", 0),
        "bulk_trade_date":   st.session_state.get("bulk_trade_date", ""),
        "bulk_trade_count":  st.session_state.get("bulk_trade_count", 0),
        "last_estate_reset": st.session_state.get("last_estate_reset", 0),
        # ✅ 기존 코드에서 누락됐던 garage 필드 추가
        "garage":            st.session_state.get("garage", {"cars": {}, "active_tier": None}),
    })
    save_db(USERS_FILE, users)


def load_session_from_db(uid: str, device_mode: str = "🖥️ PC (데스크탑)"):
    """DB → 세션 상태 로드 (로그인 시 호출)"""
    users = load_db(USERS_FILE, {})
    if uid not in users:
        return
    u = users[uid]
    st.session_state.update({
        "logged_in_user":    uid,
        "global_cash":       u.get("cash", 0),
        "inventory":         u.get("inventory", []),
        "equipped_title":    u.get("equipped_title", "🌱 신규시민"),
        "portfolio":         u.get("portfolio", {}),
        "real_estate":       u.get("real_estate", {}),
        "rent_time":         u.get("rent_time", time.time()),
        "loan":              u.get("loan", 0),
        "loan_time":         u.get("loan_time", time.time()),
        "crypto_portfolio":  u.get("crypto_portfolio", {}),
        "daily_quests":      u.get("daily_quests", {}),
        "weapon_level":      u.get("weapon_level", 0),
        "bulk_trade_date":   u.get("bulk_trade_date", ""),
        "bulk_trade_count":  u.get("bulk_trade_count", 0),
        "last_estate_reset": u.get("last_estate_reset", 0),
        "garage":            u.get("garage", {"cars": {}, "active_tier": None}),
        "device_mode":       device_mode,
    })


def claim_hidden_title(title_id: str, title_name: str) -> bool:
    """히든 칭호 최초 달성자에게만 지급"""
    uid = st.session_state.get("logged_in_user")
    if not uid:
        return False
    market = get_market()
    market.setdefault("hidden_titles", {})
    if title_id in market["hidden_titles"]:
        return False  # 이미 누군가 보유

    market["hidden_titles"][title_id] = uid
    us = load_db(USERS_FILE, {})
    if uid in us:
        if title_name not in us[uid].get("inventory", []):
            us[uid].setdefault("inventory", []).append(title_name)
        us[uid]["equipped_title"] = title_name
        save_db(USERS_FILE, us)

    st.session_state.equipped_title = title_name
    if title_name not in st.session_state.get("inventory", []):
        st.session_state.setdefault("inventory", []).append(title_name)

    market["news"] = f"👑 [서버 최초] {uid}님이 '{title_name}' 칭호를 거머쥐었습니다!!"
    save_market(market)
    st.toast(f"🎉 서버 최초! [{title_name}] 칭호 획득!", icon="👑")
    st.balloons()
    return True
