# utils/database.py
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import logging
from utils.config import (
    KST, USERS_FILE, COMMENTS_FILE, MARKET_FILE, TXLOG_FILE,
    REALESTATE_MARKET_FILE, CLAN_FILE, STATS_FILE, estate_config
)

@st.cache_resource
def get_mongo_client():
    uri = st.secrets.get("MONGO_URI", None)
    if uri: return MongoClient(uri)
    return None

def load_db(file, default):
    """MongoDB에서 데이터 불러오기"""
    client = get_mongo_client()
    if client is None:
        st.error("❌ DB 연결 실패: MongoDB에 연결할 수 없습니다. 관리자에게 문의하세요.")
        st.stop()
    try:
        db      = client["hyomin_universe"]
        col_name = file.replace(".json", "").replace("_db", "")
        doc     = db[col_name].find_one({"_id": "main"})
        if doc:
            doc.pop("_id", None)
            if "_list" in doc and len(doc) == 1:
                return doc["_list"]
            return doc
        return default
    except Exception as e:
        logging.error(f"[load_db] {file} 로드 실패: {e}")
        st.error(f"❌ DB 읽기 오류: {e}")
        st.stop()

def save_db(file, data):
    """MongoDB에 데이터 저장하기"""
    if data is None:
        return
    client = get_mongo_client()
    if client is None:
        logging.error(f"[save_db] MongoDB 연결 없음 - {file} 저장 취소")
        return
    try:
        db       = client["hyomin_universe"]
        col_name = file.replace(".json", "").replace("_db", "")
        if isinstance(data, list):
            doc_to_save = {"_id": "main", "_list": data}
        else:
            doc_to_save = {"_id": "main", **data}
        db[col_name].replace_one({"_id": "main"}, doc_to_save, upsert=True)
    except Exception as e:
        logging.error(f"[save_db] {file} 저장 실패: {e}")

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

# ─────────────────────────────────────────────────────────────────────────────
# FIX: log_tx 내부 거래량 통계 RMW 개선
#   기존: log_tx 안에서 load_stats() → 수정 → save_stats() 패턴이
#         tx 로그 저장과 같은 함수에 묶여 있어 두 번의 DB 왕복이 직렬로 실행됨.
#         동시 요청 시 두 번째 load가 첫 번째 save 이전 값을 읽어 거래량 누락.
#   변경: 통계 집계를 log_tx와 분리하고, 조회 후 저장까지의 코드를
#         최대한 짧게 유지하여 경쟁 창(race window)을 최소화.
#         (완전한 원자성은 MongoDB $inc 마이그레이션으로 추후 해결)
# ─────────────────────────────────────────────────────────────────────────────
def _update_daily_volume(amount: int):
    """거래량 통계만 별도로 빠르게 갱신 (RMW 창 최소화)"""
    try:
        stats = load_stats()
        today = datetime.now(KST).strftime("%Y-%m-%d")
        vol   = stats.get("daily_volume", {})
        vol[today] = vol.get(today, 0) + abs(amount)
        stats["daily_volume"] = vol
        save_stats(stats)
    except Exception as e:
        logging.error(f"[_update_daily_volume] 통계 갱신 실패 (거래는 이미 완료됨): {e}")


def log_tx(uid: str, category: str, desc: str, amount: int):
    """거래 로그 기록 + 거래량 통계 갱신"""
    # 1단계: 거래 로그 저장 (핵심 — 실패해선 안 됨)
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

    # 2단계: 거래량 통계 갱신 (분리 실행 — 실패해도 거래 자체에 영향 없음)
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
