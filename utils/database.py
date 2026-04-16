# utils/database.py
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import logging
from utils.config import (
    KST, USERS_FILE, COMMENTS_FILE, MARKET_FILE, TXLOG_FILE,
    REALESTATE_MARKET_FILE, CLAN_FILE, estate_config
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
        # MongoDB가 없으면 앱을 멈춤 (빈 데이터로 덮어쓰는 사고 방지)
        import streamlit as st
        st.error("❌ DB 연결 실패: MongoDB에 연결할 수 없습니다. 관리자에게 문의하세요.")
        st.stop()
    try:
        db = client["hyomin_universe"]
        col_name = file.replace(".json", "").replace("_db", "")
        doc = db[col_name].find_one({"_id": "main"})
        if doc:
            doc.pop("_id", None)
            # 리스트로 저장된 데이터 복원
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
        # 연결이 없으면 저장 자체를 막음 (빈 데이터 덮어쓰기 방지)
        logging.error(f"[save_db] MongoDB 연결 없음 - {file} 저장 취소")
        return
    try:
        db = client["hyomin_universe"]
        col_name = file.replace(".json", "").replace("_db", "")
        
        # 리스트 타입이면 래핑해서 저장하고 _id 유지
        if isinstance(data, list):
            doc_to_save = {"_id": "main", "_list": data}
        else:
            doc_to_save = {"_id": "main", **data}
            
        db[col_name].replace_one(
            {"_id": "main"}, doc_to_save, upsert=True
        )
    except Exception as e:
        logging.error(f"[save_db] {file} 저장 실패: {e}")

def log_tx(uid: str, category: str, desc: str, amount: int):
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs: logs[uid] = []
    logs[uid].insert(0, {
        "time": datetime.now(KST).strftime("%m/%d %H:%M:%S"),
        "category": category, "desc": desc, "amount": amount,
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

def load_clan_db(): return load_db(CLAN_FILE, {})
def save_clan_db(data): save_db(CLAN_FILE, data)

def get_user_clan(uid):
    clans = load_clan_db()
    for cname, cdata in clans.items():
        if uid in cdata.get('members', []): return cname
    return None

def save_market(data):
    """시장 전체 데이터를 저장"""
    save_db(MARKET_FILE, data)
