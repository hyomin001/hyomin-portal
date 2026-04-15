# ============================================================
# utils/database.py — DB 연산 (MongoDB 우선, JSON 폴백)
# ============================================================
import os
import json
import time
import random
import streamlit as st

from config import (
    USERS_FILE, MARKET_FILE, TXLOG_FILE,
    REALESTATE_MARKET_FILE, CLAN_FILE,
    MESSAGES_FILE, CLAN_CHATS_FILE,
    STOCK_CONFIG, CRYPTO_CONFIG, ESTATE_CONFIG,
)
from datetime import timezone, timedelta

KST = timezone(timedelta(hours=9))

# ── MongoDB 연결 ──────────────────────────────────────────────
@st.cache_resource
def get_mongo_client():
    try:
        from pymongo import MongoClient
        uri = st.secrets.get("MONGO_URI", None)
        if uri:
            return MongoClient(uri, serverSelectionTimeoutMS=3000)
    except Exception:
        pass
    return None

# ── 범용 로드/저장 ────────────────────────────────────────────
def load_db(file: str, default):
    client = get_mongo_client()
    if client:
        try:
            col_name = file.replace(".json", "").replace("_db", "")
            doc = client["hyomin_universe"][col_name].find_one({"_id": "main"})
            if doc:
                doc.pop("_id", None)
                return doc
        except Exception:
            pass
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default


def save_db(file: str, data):
    if data is None:
        return
    client = get_mongo_client()
    saved_mongo = False
    if client:
        try:
            col_name = file.replace(".json", "").replace("_db", "")
            client["hyomin_universe"][col_name].replace_one(
                {"_id": "main"}, {"_id": "main", **data}, upsert=True
            )
            saved_mongo = True
        except Exception:
            pass
    if not saved_mongo:
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass


# ── 거래 로그 ─────────────────────────────────────────────────
def log_tx(uid: str, category: str, desc: str, amount: int):
    from datetime import datetime
    logs = load_db(TXLOG_FILE, {})
    if uid not in logs:
        logs[uid] = []
    logs[uid].insert(0, {
        "time": datetime.now(KST).strftime("%m/%d %H:%M:%S"),
        "category": category,
        "desc": desc,
        "amount": amount,
    })
    logs[uid] = logs[uid][:200]
    save_db(TXLOG_FILE, logs)


# ── 마켓 ──────────────────────────────────────────────────────
MARKET_VERSION = 7  # 버전 올려서 클린 초기화

def _init_market() -> dict:
    return {
        "version": MARKET_VERSION,
        "season_num": 2,
        "stock_data": {
            s["id"]: {
                "name": s["name"], "icon": s["icon"],
                "price": random.randint(50_000, 150_000),
                "history": [80_000, 80_000],
            }
            for s in STOCK_CONFIG
        },
        "crypto_data": {
            c["id"]: {
                "name": c["name"], "icon": c["icon"],
                "price": float(c["base_price"]),
                "history": [float(c["base_price"])],
            }
            for c in CRYPTO_CONFIG
        },
        "news": "🌌 HYOMIN UNIVERSE 시즌 2 시작!",
        "news_time": time.time(),
        "last_tick": time.time(),
        "crypto_tick": time.time(),
        "admin_msg": "",
        "admin_color": "#FF4B4B",
        "lotto_pool": 5_000_000_000,
        "lotto_tickets": {},
        "lotto_last_draw": time.time(),
        "next_news_target": random.choice(STOCK_CONFIG)["id"],
        "next_news_impact": random.uniform(-0.2, 0.2),
        "board_banned": [],
        "hidden_titles": {},
        "season_start": time.time(),
        "season_end": time.time() + 30 * 86400,
        "season_records": {},
        "season_ending": False,
        "force_estate_reset": 0,
    }


def get_market() -> dict:
    d = load_db(MARKET_FILE, {})
    if not d or d.get("version") != MARKET_VERSION:
        # 기존 데이터 최대한 보존
        preserved = {
            "season_num":     d.get("season_num", 2),
            "lotto_pool":     d.get("lotto_pool", 5_000_000_000),
            "lotto_tickets":  d.get("lotto_tickets", {}),
            "lotto_last_draw":d.get("lotto_last_draw", time.time()),
            "season_records": d.get("season_records", {}),
            "board_banned":   d.get("board_banned", []),
            "hidden_titles":  d.get("hidden_titles", {}),
            "admin_msg":      d.get("admin_msg", ""),
            "admin_color":    d.get("admin_color", "#FF4B4B"),
        }
        fresh = _init_market()
        fresh.update(preserved)
        save_db(MARKET_FILE, fresh)
        return fresh
    return d


def save_market(data: dict):
    save_db(MARKET_FILE, data)


# ── 부동산 마켓 ───────────────────────────────────────────────
def load_estate_market() -> dict:
    default = {
        "listings": [],
        "owner_counts": {},
        "initial_stock": {eid: info["total_supply"] for eid, info in ESTATE_CONFIG.items()},
    }
    d = load_db(REALESTATE_MARKET_FILE, default)
    for k in default:
        if k not in d:
            d[k] = default[k]
    return d


def save_estate_market(data: dict):
    save_db(REALESTATE_MARKET_FILE, data)


def get_estate_initial_listings(em: dict) -> list:
    result = []
    for eid, info in ESTATE_CONFIG.items():
        owned_total = sum(v.get(eid, 0) for v in em["owner_counts"].values())
        listed_count = sum(1 for l in em["listings"] if l["eid"] == eid)
        released = owned_total + listed_count
        limit = em.get("initial_stock", {}).get(eid, info["total_supply"])
        remaining = max(0, limit - released)
        if remaining > 0:
            result.append({
                "eid": eid, "remaining": remaining,
                "price": info["base_price"], "is_initial": True,
            })
    return result


# ── 클랜 ──────────────────────────────────────────────────────
def load_clan_db() -> dict:
    return load_db(CLAN_FILE, {})


def save_clan_db(data: dict):
    save_db(CLAN_FILE, data)


def get_user_clan(uid: str):
    for cname, cdata in load_clan_db().items():
        if uid in cdata.get("members", []):
            return cname
    return None


def load_clan_chat(clan_name: str) -> list:
    chat_db = load_db(CLAN_CHATS_FILE, {})
    return chat_db.get(clan_name, [])


def save_clan_chat(clan_name: str, messages: list):
    chat_db = load_db(CLAN_CHATS_FILE, {})
    chat_db[clan_name] = messages[-50:]
    save_db(CLAN_CHATS_FILE, chat_db)
