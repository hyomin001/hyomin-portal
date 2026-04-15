# ============================================================
# utils/market_engine.py — 마켓 자동 틱 처리 (주식/코인/뉴스/로또/시즌)
# ============================================================
import time
import random
import streamlit as st

from config import STOCK_CONFIG, CRYPTO_CONFIG, ESTATE_CONFIG, FORGE_DATA
from utils.database import (
    load_db, save_db, log_tx,
    get_market, save_market,
    load_estate_market, save_estate_market,
    load_clan_db, save_clan_db,
    USERS_FILE,
)
from utils.helpers import format_korean_money
from datetime import timezone, timedelta

KST = timezone(timedelta(hours=9))


def run_market_tick(market: dict) -> tuple[dict, bool]:
    """마켓 전체 틱 처리. 변경된 market dict와 변경 여부(bool) 반환."""
    cur_t = time.time()
    changed = False

    # ── 주식 틱 (10초마다) ────────────────────────────────────
    stock_passed = cur_t - market.get("last_tick", cur_t)
    s_ticks = min(int(stock_passed / 10), 60)
    if s_ticks > 0:
        for _ in range(s_ticks):
            for s in STOCK_CONFIG:
                curr = market["stock_data"][s["id"]]
                ch = (random.random() - 0.5) * 2 * s["vol"]
                curr["price"] = round(max(1_000, curr["price"] * (1 + ch)))
                curr["history"].append(curr["price"])
                if len(curr["history"]) > 60:
                    curr["history"].pop(0)
        market["last_tick"] = cur_t
        changed = True

    # ── 코인 틱 (5초마다) ─────────────────────────────────────
    crypto_passed = cur_t - market.get("crypto_tick", cur_t)
    c_ticks = min(int(crypto_passed / 5), 60)
    if c_ticks > 0:
        for _ in range(c_ticks):
            for c in CRYPTO_CONFIG:
                curr = market["crypto_data"][c["id"]]
                ch = (random.random() - 0.5) * 2 * c["vol"]
                curr["price"] = max(0.01, round(curr["price"] * (1 + ch), 6))
                curr["history"].append(curr["price"])
                if len(curr["history"]) > 60:
                    curr["history"].pop(0)
        market["crypto_tick"] = cur_t
        changed = True

    # ── 뉴스 (30초마다) ───────────────────────────────────────
    if cur_t - market.get("news_time", 0) > 30:
        tid = market.get("next_news_target", STOCK_CONFIG[0]["id"])
        imp = market.get("next_news_impact", 0.0)
        t_nm = next((s["name"] for s in STOCK_CONFIG if s["id"] == tid), tid)
        market["stock_data"][tid]["price"] = int(
            market["stock_data"][tid]["price"] * (1 + imp)
        )
        direction = (
            "급등" if imp > 0.1 else "강세" if imp > 0
            else "급락" if imp < -0.1 else "약세"
        )
        headlines = {
            "급등": [f"🚀 [속보] {t_nm} 실적 서프라이즈! 장중 {direction}!"],
            "강세": [f"📊 [마감] {t_nm} 기관 꾸준한 매집 행보!"],
            "급락": [f"❄️ [속보] {t_nm} 악재 공시로 투자자 충격!"],
            "약세": [f"⚠️ [마감] {t_nm} 단기 조정 국면"],
        }
        market["news"] = random.choice(headlines.get(direction, [f"📰 {t_nm} 시황 변동"]))
        market["news_time"] = cur_t
        market["next_news_target"] = random.choice(STOCK_CONFIG)["id"]
        market["next_news_impact"] = random.uniform(-0.25, 0.25)
        changed = True

    # ── 로또 추첨 (1시간마다) ─────────────────────────────────
    if cur_t - market.get("lotto_last_draw", 0) > 3600 and market.get("lotto_tickets"):
        pool_tickets = []
        for u, c in market["lotto_tickets"].items():
            pool_tickets.extend([u] * c)
        winner = random.choice(pool_tickets)
        prize = market["lotto_pool"]
        us = load_db(USERS_FILE, {})
        if winner in us:
            us[winner]["cash"] += prize
            save_db(USERS_FILE, us)
            log_tx(winner, "로또당첨", "글로벌 로또 1등 잭팟!!", prize)
        market["news"] = f"🎊 [당첨] {winner}님이 {format_korean_money(prize)} 대박!"
        market["lotto_pool"] = 5_000_000_000
        market["lotto_tickets"] = {}
        market["lotto_last_draw"] = cur_t
        changed = True

    # ── 시즌 종료 체크 ────────────────────────────────────────
    if cur_t > market.get("season_end", cur_t + 9999) and not market.get("season_ending", False):
        market, changed = _run_season_end(market, cur_t)

    return market, changed


def _run_season_end(market: dict, cur_t: float) -> tuple[dict, bool]:
    """시즌 종료 처리 (자산 리셋, 칭호 지급, 다음 시즌 개막)"""
    from utils.sync import get_net_worth

    market["season_ending"] = True
    us_all = load_db(USERS_FILE, {})

    # 순위 산정
    rank_list = []
    for uid, udata in us_all.items():
        if uid == "admin":
            continue
        w = get_net_worth(uid, market)
        rank_list.append((uid, w))
    rank_list.sort(key=lambda x: x[1], reverse=True)

    sn = market.get("season_num", 1)
    season_titles = [
        f"🥇 [시즌{sn}] 전설의 우승자",
        f"🥈 [시즌{sn}] 준우승의 영광",
        f"🥉 [시즌{sn}] 시즌 3위",
    ]
    record = {}
    for i, (uid, _) in enumerate(rank_list[:3]):
        title = season_titles[i]
        record[f"rank{i+1}"] = uid
        if uid in us_all:
            us_all[uid].setdefault("inventory", [])
            if title not in us_all[uid]["inventory"]:
                us_all[uid]["inventory"].append(title)
            us_all[uid]["equipped_title"] = title

    # 전체 리셋
    for uid in us_all:
        if uid == "admin":
            continue
        us_all[uid].update({
            "cash": 500_000_000,
            "portfolio": {}, "crypto_portfolio": {},
            "real_estate": {}, "loan": 0,
            "loan_time": cur_t, "rent_time": cur_t,
            "weapon_level": 0, "daily_quests": {},
            "bulk_trade_count": 0, "garage": {"cars": {}, "active_tier": None},
        })
    save_db(USERS_FILE, us_all)

    # 클랜 은행 초기화
    clans = load_clan_db()
    for cn in clans:
        clans[cn]["bank"] = 0
    save_clan_db(clans)

    # 부동산 마켓 초기화
    save_estate_market({
        "listings": [], "owner_counts": {},
        "initial_stock": {eid: info["total_supply"] for eid, info in ESTATE_CONFIG.items()},
    })

    # 다음 시즌 세팅
    market.setdefault("season_records", {})[str(sn)] = record
    market["season_num"] = sn + 1
    market["season_start"] = cur_t
    market["season_end"] = cur_t + 30 * 86400
    market["season_ending"] = False
    market["lotto_pool"] = 5_000_000_000
    market["lotto_tickets"] = {}
    market["force_estate_reset"] = cur_t
    winner_name = rank_list[0][0] if rank_list else "?"
    market["news"] = f"🏆 [시즌{sn} 종료] {winner_name}님 우승! 시즌{sn+1} 개막!"

    return market, True
