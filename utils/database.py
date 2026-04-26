# utils/database.py
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import logging
import time as _time
from utils.config import (
    KST, USERS_FILE, COMMENTS_FILE, MARKET_FILE, TXLOG_FILE,
    REALESTATE_MARKET_FILE, CLAN_FILE, STATS_FILE, estate_config
)

@st.cache_resource
def get_mongo_client():
    uri = st.secrets.get("MONGO_URI", None)
    if uri: return MongoClient(uri)
    return None

def _get_col(file: str):
    client = get_mongo_client()
    if client is None: return None
    db = client["hyomin_universe"]
    return db[file.replace(".json", "").replace("_db", "")]

def load_db(file, default):
    """MongoDB에서 데이터 불러오기 (재시도 1회 포함)"""
    client = get_mongo_client()
    if client is None:
        st.error("❌ DB 연결 실패: MongoDB에 연결할 수 없습니다. 관리자에게 문의하세요.")
        st.stop()
    for attempt in range(2):
        try:
            col = _get_col(file)
            doc = col.find_one({"_id": "main"})
            if doc:
                doc.pop("_id", None)
                if "_list" in doc and len(doc) == 1:
                    return doc["_list"]
                return doc
            return default
        except Exception as e:
            logging.error(f"[load_db] {file} 로드 실패 (시도 {attempt+1}/2): {e}")
            if attempt == 0:
                _time.sleep(0.5)
                continue
            st.warning(f"⚠️ DB 일시 오류 발생. 일부 데이터가 최신이 아닐 수 있습니다. ({file})")
            return default

def save_db(file, data):
    """MongoDB에 데이터 저장하기"""
    if data is None: return
    client = get_mongo_client()
    if client is None:
        logging.error(f"[save_db] MongoDB 연결 없음 - {file} 저장 취소")
        return
    try:
        col = _get_col(file)
        if isinstance(data, list):
            doc_to_save = {"_id": "main", "_list": data}
        else:
            doc_to_save = {"_id": "main", **data}
        col.replace_one({"_id": "main"}, doc_to_save, upsert=True)
    except Exception as e:
        logging.error(f"[save_db] {file} 저장 실패: {e}")


def atomic_deduct_cash(uid: str, amount: int) -> bool:
    """
    MongoDB 원자적 현금 차감 — Race Condition 방어의 핵심.
    users 도큐먼트에서 uid.cash >= amount 인 경우에만 $inc로 차감.
    성공 시 True, 잔액 부족 또는 오류 시 False 반환.
    """
    client = get_mongo_client()
    if client is None: return False
    try:
        col = _get_col(USERS_FILE)
        result = col.find_one_and_update(
            {"_id": "main", f"{uid}.cash": {"$gte": amount}},
            {"$inc": {f"{uid}.cash": -amount}},
        )
        return result is not None
    except Exception as e:
        logging.error(f"[atomic_deduct_cash] {uid} 차감 실패: {e}")
        return False


def atomic_add_cash(uid: str, amount: int) -> bool:
    """MongoDB 원자적 현금 지급."""
    client = get_mongo_client()
    if client is None: return False
    try:
        col = _get_col(USERS_FILE)
        col.update_one(
            {"_id": "main"},
            {"$inc": {f"{uid}.cash": amount}},
        )
        return True
    except Exception as e:
        logging.error(f"[atomic_add_cash] {uid} 지급 실패: {e}")
        return False


# ── 로그인 잠금 — DB 기반 ──────────────────────────────────────────────────

def get_login_lock(uid: str) -> tuple[int, float]:
    """(실패 횟수, 잠금 해제 타임스탬프) 반환. uid가 없으면 (0, 0) 반환."""
    try:
        col = _get_col(USERS_FILE)
        doc = col.find_one({"_id": "main"}, {f"{uid}.login_fails": 1, f"{uid}.lock_until": 1})
        if not doc or uid not in doc: return 0, 0.0
        u = doc[uid]
        return u.get("login_fails", 0), float(u.get("lock_until", 0))
    except Exception as e:
        logging.error(f"[get_login_lock] {e}")
        return 0, 0.0

def set_login_lock(uid: str, fails: int, lock_until: float):
    """로그인 실패 횟수·잠금 타임스탬프를 DB에 원자적으로 저장."""
    try:
        col = _get_col(USERS_FILE)
        col.update_one(
            {"_id": "main"},
            {"$set": {f"{uid}.login_fails": fails, f"{uid}.lock_until": lock_until}},
        )
    except Exception as e:
        logging.error(f"[set_login_lock] {e}")

def clear_login_lock(uid: str):
    """로그인 성공 시 잠금 초기화."""
    try:
        col = _get_col(USERS_FILE)
        col.update_one(
            {"_id": "main"},
            {"$set": {f"{uid}.login_fails": 0, f"{uid}.lock_until": 0.0}},
        )
    except Exception as e:
        logging.error(f"[clear_login_lock] {e}")


# 📊 통계 전용 로드/저장
def load_stats():
    return load_db(STATS_FILE, {
        "daily_visitors": {},
        "total_signups":  0,
        "game_counts":    {},
        "daily_volume":   {}
    })

def save_stats(data):
    save_db(STATS_FILE, data)

def _update_daily_volume(amount: int):
    """거래량 통계만 별도로 빠르게 갱신"""
    try:
        stats = load_stats()
        today = datetime.now(KST).strftime("%Y-%m-%d")
        vol   = stats.get("daily_volume", {})
        vol[today] = vol.get(today, 0) + abs(amount)
        stats["daily_volume"] = vol
        save_stats(stats)
    except Exception as e:
        logging.error(f"[_update_daily_volume] 통계 갱신 실패: {e}")

def log_tx(uid: str, category: str, desc: str, amount: int):
    """거래 로그 기록 + 거래량 통계 갱신"""
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs: logs[uid] = []
    logs[uid].insert(0, {
        "time":     datetime.now(KST).strftime("%m/%d %H:%M:%S"),
        "category": category,
        "desc":     desc,
        "amount":   amount,
    })
    logs[uid] = logs[uid][:200]
    save_db(TXLOG_FILE, logs)

    if category in ["주식매수", "주식매도", "코인매수", "코인매도"]:
        _update_daily_volume(amount)


def load_estate_market():
    default = {
        "listings":     [],
        "owner_counts": {},
        "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}
    }
    d = load_db(REALESTATE_MARKET_FILE, default)
    if "initial_stock"  not in d: d["initial_stock"]  = {eid: info["total_supply"] for eid, info in estate_config.items()}
    if "owner_counts"   not in d: d["owner_counts"]   = {}
    if "listings"       not in d: d["listings"]       = []
    return d

def save_estate_market(data):
    save_db(REALESTATE_MARKET_FILE, data)

def get_estate_initial_listings(em):
    result = []
    for eid, info in estate_config.items():
        owned_total      = sum(v.get(eid, 0) for v in em["owner_counts"].values())
        listed_count     = sum(1 for l in em["listings"] if l["eid"] == eid)
        initial_released = owned_total + listed_count
        current_limit    = em.get("initial_stock", {}).get(eid, info["total_supply"])
        remaining_initial = max(0, current_limit - initial_released)
        if remaining_initial > 0:
            result.append({"eid": eid, "remaining": remaining_initial, "price": info["base_price"], "is_initial": True})
    return result

def load_clan_db():  return load_db(CLAN_FILE, {})
def save_clan_db(data): save_db(CLAN_FILE, data)

def get_user_clan(uid):
    clans = load_clan_db()
    for cname, cdata in clans.items():
        if uid in cdata.get('members', []): return cname
    return None

def save_market(data):
    """시장 전체 데이터 저장"""
    save_db(MARKET_FILE, data)
