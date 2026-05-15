# utils/database.py
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta
import logging
import time as _time
from utils.config import (
    KST, USERS_FILE, COMMENTS_FILE, MARKET_FILE, TXLOG_FILE,
    REALESTATE_MARKET_FILE, CLAN_FILE, STATS_FILE, LEADERBOARD_FILE, estate_config
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
    """거래량 통계만 별도로 빠르게 갱신 — 오늘 이전 날짜 데이터 자동 정리"""
    try:
        stats = load_stats()
        today = datetime.now(KST).strftime("%Y-%m-%d")
        vol   = stats.get("daily_volume", {})
        vol[today] = vol.get(today, 0) + abs(amount)
        # 오늘 이전 날짜 데이터 자동 삭제 (무한 누적 방지)
        stats["daily_volume"] = {k: v for k, v in vol.items() if k >= today}
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


# ══════════════════════════════════════════════════════════════
# 🏆 전역 명예의 전당 (Global Leaderboard)  A~I 전 게임 공통
# 구조: { "game_id": { "top_user": str, "top_score": int, "date": str } }
# ══════════════════════════════════════════════════════════════

_GAME_META = {
    "academy":       {"name": "AI 아카데미",        "fmt": lambda s: f"{s:,}점"},
    "zombie_war":    {"name": "좀비 전쟁",           "fmt": lambda s: f"{s:,}점"},
    "terminal":      {"name": "THE TERMINAL",        "fmt": lambda s: f"{s:,}점"},
    "invest_marble": {"name": "인베스트마블",         "fmt": lambda s: f"₩{s:,}"},
    "dungeon":       {"name": "던전 런 REBORN",       "fmt": lambda s: f"{s:,}점"},
    "racing":        {"name": "네온 도주 레이싱",     "fmt": lambda s: f"{s:,}점"},
    "zombie":        {"name": "좀비 아포칼립스",      "fmt": lambda s: f"{s:,}킬"},
    "fighter":       {"name": "스트리트 파이터 EX",   "fmt": lambda s: f"{s:,}점"},
    "sniper":        {"name": "라인 배틀 저격전",     "fmt": lambda s: f"{s:,}킬"},
}

def get_game_meta(game_id: str) -> dict:
    return _GAME_META.get(game_id, {"name": game_id, "fmt": lambda s: f"{s:,}점"})

def load_leaderboard() -> dict:
    """전역 리더보드 로드"""
    return load_db(LEADERBOARD_FILE, {})

def save_leaderboard(data: dict):
    """전역 리더보드 저장"""
    save_db(LEADERBOARD_FILE, data)

def update_leaderboard(game_id: str, user_name: str, score) -> bool:
    """
    게임 종료 시 호출 — 현재 유저 점수가 기존 1위보다 높으면 갱신.
    반환값: True = 신규 1위 달성, False = 기록 미달성
    """
    try:
        lb = load_leaderboard()
        prev = lb.get(game_id, {})
        if score > prev.get("top_score", -1):
            lb[game_id] = {
                "top_user":  user_name,
                "top_score": score,
                "date":      datetime.now(KST).strftime("%Y-%m-%d"),
            }
            save_leaderboard(lb)
            return True
        return False
    except Exception as e:
        logging.error(f"[update_leaderboard] {game_id} 업데이트 실패: {e}")
        return False

def format_leaderboard_score(game_id: str, score) -> str:
    """게임별 단위에 맞게 점수를 포맷팅"""
    meta = get_game_meta(game_id)
    try:
        return meta["fmt"](int(score))
    except Exception:
        return str(score)


# ══════════════════════════════════════════════════════════════
# 🎮 게임 기록 원자적 업데이트 — Race Condition 완전 방어
# replace_one 대신 $set으로 특정 필드만 업데이트
# ══════════════════════════════════════════════════════════════

def atomic_set_game_record(uid: str, game_key: str, record: dict) -> bool:
    """
    game_records.{game_key}를 MongoDB $set으로 원자적 업데이트.
    전체 document replace 없이 해당 필드만 교체 → Race Condition 없음.
    """
    client = get_mongo_client()
    if client is None: return False
    try:
        col = _get_col(USERS_FILE)
        col.update_one(
            {"_id": "main"},
            {"$set": {f"{uid}.game_records.{game_key}": record}},
        )
        return True
    except Exception as e:
        logging.error(f"[atomic_set_game_record] {uid}/{game_key} 실패: {e}")
        return False


def atomic_set_user_field(uid: str, field: str, value) -> bool:
    """
    users.{uid}.{field}를 MongoDB $set으로 원자적 업데이트.
    dungeon_stats, marble_stats 등 중첩 필드에 사용.
    """
    client = get_mongo_client()
    if client is None: return False
    try:
        col = _get_col(USERS_FILE)
        col.update_one(
            {"_id": "main"},
            {"$set": {f"{uid}.{field}": value}},
        )
        return True
    except Exception as e:
        logging.error(f"[atomic_set_user_field] {uid}/{field} 실패: {e}")
        return False


def get_user_game_record(uid: str, game_key: str) -> dict:
    """DB에서 특정 유저의 특정 게임 기록만 빠르게 읽어옴."""
    client = get_mongo_client()
    if client is None: return {}
    try:
        col = _get_col(USERS_FILE)
        proj = {f"{uid}.game_records.{game_key}": 1}
        doc = col.find_one({"_id": "main"}, proj)
        if not doc: return {}
        return doc.get(uid, {}).get("game_records", {}).get(game_key, {})
    except Exception as e:
        logging.error(f"[get_user_game_record] {uid}/{game_key} 실패: {e}")
        return {}


def get_user_field(uid: str, field: str):
    """DB에서 특정 유저의 특정 필드만 빠르게 읽어옴."""
    client = get_mongo_client()
    if client is None: return None
    try:
        col = _get_col(USERS_FILE)
        doc = col.find_one({"_id": "main"}, {f"{uid}.{field}": 1})
        if not doc: return None
        return doc.get(uid, {}).get(field)
    except Exception as e:
        logging.error(f"[get_user_field] {uid}/{field} 실패: {e}")
        return None



# ══════════════════════════════════════════════════════════════
# 🏆 시즌 종료 처리 — market DB 기반 완전 자동화
# ══════════════════════════════════════════════════════════════

def _save_season_snapshot(market: dict) -> None:
    """
    시즌 초기화 직전 1~10위 순자산 스냅샷을 market['season_records']에 영구 저장.
    관리자 패널 '역대 시즌 기록'에서 확인 가능.
    """
    try:
        from utils.config import estate_config, FORGE_DATA
        col      = _get_col(USERS_FILE)
        doc      = col.find_one({"_id": "main"}) or {}
        prices   = {k: v.get("price", 0) for k, v in market.get("stock_data", {}).items()}
        crypto   = market.get("crypto_data", {})
        rankings = []

        for uid, ud in doc.items():
            if uid in ("_id", "admin"):
                continue
            w = ud.get("cash", 0) - ud.get("loan", 0)
            for sid, pd in ud.get("portfolio", {}).items():
                w += pd.get("qty", 0) * prices.get(sid, 0)
            for cid, ci in ud.get("crypto_portfolio", {}).items():
                w += ci.get("qty", 0) * crypto.get(cid, {}).get("price", 0)
            for eid, cnt in ud.get("real_estate", {}).items():
                if eid in estate_config:
                    w += estate_config[eid]["base_price"] * cnt * 0.8
            wlv = ud.get("weapon_level", 0)
            if wlv > 0 and wlv in FORGE_DATA:
                w += FORGE_DATA[wlv]["sell"]
            rankings.append((uid, int(w)))

        rankings.sort(key=lambda x: x[1], reverse=True)
        sn = market.get("season_num", 1)
        record = {}
        for i, (uid, w) in enumerate(rankings[:10]):
            record[f"rank{i+1}"] = {"uid": uid, "net_worth": w}

        # ── 게임별 1위 기록도 함께 스냅샷 ──
        try:
            lb = load_leaderboard()
            record["game_champions"] = {
                game_id: {
                    "top_user":  entry.get("top_user", "?"),
                    "top_score": entry.get("top_score", 0),
                    "date":      entry.get("date", ""),
                }
                for game_id, entry in lb.items()
            }
        except Exception as _ge:
            logging.warning(f"[_save_season_snapshot] 게임 챔피언 스냅샷 실패: {_ge}")
            record["game_champions"] = {}

        market.setdefault("season_records", {})[str(sn)] = record
        logging.info(f"[_save_season_snapshot] 시즌 {sn} 스냅샷 저장 완료 ({len(rankings)}명)")
    except Exception as e:
        logging.error(f"[_save_season_snapshot] 실패: {e}")


def reset_season_records(market: dict) -> bool:
    """
    시즌 종료 시 호출.
    1) 현재 순위 스냅샷 저장 (명예의 전당)
    2) 상위 3인에게 시즌 우승 칭호 지급
    3) 전역 리더보드 초기화
    4) 모든 유저 게임 기록 초기화
    5) market DB에 새 시즌 번호·종료일 기록
    반환값: True = 성공, False = 실패
    """
    import time as _t
    from utils.config import SEASON_DURATION_DAYS, NEXT_SEASON_DELAY, estate_config
    try:
        sn = market.get("season_num", 1)

        # 1) 순위 스냅샷 + 우승 칭호
        _save_season_snapshot(market)
        records = market.get("season_records", {}).get(str(sn), {})
        season_titles = [
            f"🥇 [시즌{sn}] 전설의 우승자",
            f"🥈 [시즌{sn}] 준우승의 영광",
            f"🥉 [시즌{sn}] 시즌 3위",
        ]
        col = _get_col(USERS_FILE)
        doc = col.find_one({"_id": "main"}) or {}
        title_set = {}
        for i, key in enumerate([f"rank{j+1}" for j in range(3)]):
            entry = records.get(key, {})
            uid   = entry.get("uid") if isinstance(entry, dict) else entry
            if uid and uid in doc:
                title = season_titles[i]
                ud    = doc[uid]
                inv   = ud.get("inventory", [])
                if title not in inv:
                    inv.append(title)
                title_set[f"{uid}.inventory"]      = inv
                title_set[f"{uid}.equipped_title"] = title
        if title_set:
            col.update_one({"_id": "main"}, {"$set": title_set})

        # 2) 리더보드 초기화
        save_leaderboard({})

        # 3) 유저 게임 기록 초기화
        empty_game_records = {
            "racing":        {"score": 0, "dist": 0.0},
            "zombie":        {"wave": 0, "score": 0, "kills": 0},
            "fighter":       {"score": 0, "perfects": 0},
            "sniper":        {"score": 0, "grade": "", "clears": []},
            "invest_marble": {"score": 0, "wins": 0},
            "dungeon":       {"score": 0},
            "terminal":      {"score": 0},
        }
        empty_dungeon = {"best_score": 0, "best_kills": 0, "clears": 0, "games_played": 0}
        empty_marble  = {"wins": 0, "losses": 0, "games_played": 0, "best_net_worth": 0}
        set_fields = {}
        for uid, udata in doc.items():
            if uid in ("_id", "admin"):
                continue
            set_fields[f"{uid}.game_records"]    = empty_game_records
            set_fields[f"{uid}.dungeon_stats"]   = empty_dungeon
            set_fields[f"{uid}.marble_stats"]    = empty_marble
            set_fields[f"{uid}.dungeon_weekly"]  = {}
            set_fields[f"{uid}.terminal_cleared"]= []
        if set_fields:
            col.update_one({"_id": "main"}, {"$set": set_fields})

        # 4) market DB — 새 시즌 번호·기간 기록
        new_sn    = sn + 1
        now_ts    = _t.time()
        market["season_num"]      = new_sn
        market["season_start"]    = now_ts
        market["season_end"]      = now_ts + SEASON_DURATION_DAYS * 86400
        market["season_ending"]   = False
        market["news"] = (
            f"🏆 [시즌{sn} 종료] "
            + (f"{records.get('rank1', {}).get('uid','?')}님 우승! " if isinstance(records.get('rank1'), dict) else "")
            + f"🌌 시즌 {new_sn} 시작!"
        )
        save_market(market)

        # 5) stats 기록
        stats = load_stats()
        stats["season_reset_at"] = datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S")
        stats["last_season_num"] = sn
        save_stats(stats)

        logging.info(f"[reset_season_records] 시즌 {sn}→{new_sn} 초기화 완료")
        return True
    except Exception as e:
        logging.error(f"[reset_season_records] 실패: {e}")
        return False


def check_and_run_season_reset(market: dict) -> bool:
    """
    포털 메인 로드 시마다 호출.
    market['season_end'] 기준으로 시즌 종료 여부를 판단하고,
    NEXT_SEASON_DELAY(1시간) 경과 후 아직 초기화 안 됐으면 자동 실행.

    중복 실행 방지: stats['season_reset_at'] 타임스탬프로 이미 처리된 시즌은 건너뜀.
    반환값: True = 이번 호출에서 초기화 실행됨
    """
    import time as _t
    from utils.config import NEXT_SEASON_DELAY
    try:
        season_end_ts = market.get("season_end", 0)
        if season_end_ts <= 0:
            return False  # 시즌 종료일이 DB에 없음 — 관리자가 아직 설정 전

        now = _t.time()
        trigger_ts = season_end_ts + NEXT_SEASON_DELAY
        if now < trigger_ts:
            return False  # 아직 시즌 진행 중 또는 유예 기간

        # 중복 방지: 이미 이 시즌 종료 이후에 초기화한 기록이 있으면 스킵
        stats      = load_stats()
        reset_at   = stats.get("season_reset_at", "")
        last_sn    = stats.get("last_season_num", -1)
        cur_sn     = market.get("season_num", 1)
        if last_sn >= cur_sn and reset_at:
            # 이미 처리된 시즌
            return False

        logging.info("[check_and_run_season_reset] 시즌 자동 초기화 실행!")
        return reset_season_records(market)
    except Exception as e:
        logging.error(f"[check_and_run_season_reset] {e}")
        return False
