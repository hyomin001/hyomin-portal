# utils/database.py이 파일은 몽고DB 클라우드 연결과 로컬 데이터를 저장/불러오는 역할을 전담합니다.
import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from utils.config import *

@st.cache_resource
def get_mongo_client():
    uri = st.secrets.get("MONGO_URI", None)
    if uri: return MongoClient(uri)
    return None

def load_db(file, default):
    """MongoDB에서 데이터 불러오기"""
    client = get_mongo_client()
    if client:
        try:
            db = client["hyomin_universe"]
            col_name = file.replace(".json", "").replace("_db", "")
            doc = db[col_name].find_one({"_id": "main"})
            if doc:
                doc.pop("_id", None)
                return doc
        except Exception: pass
    return default

def save_db(file, data):
    """MongoDB에 데이터 저장하기"""
    if data is None: return
    client = get_mongo_client()
    if client:
        try:
            db = client["hyomin_universe"]
            col_name = file.replace(".json", "").replace("_db", "")
            db[col_name].replace_one(
                {"_id": "main"}, {"_id": "main", **data}, upsert=True
            )
        except Exception: pass

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