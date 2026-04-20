# pages/project_d.py
# 🎲 부루마블 — 고퀄 보드게임 (봇 AI / 집·호텔 / 저당 / 무인도 보석금)
import streamlit as st
import random
import time
import json
import hashlib

# ══════════════════════════════════════════════════════════
#  BOARD DEFINITION  (40칸)
# ══════════════════════════════════════════════════════════

CELLS = [
    # 0~9 (하단, 오른→왼)
    {"name": "출발",     "type": "go",     "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "서울",     "type": "prop",   "price": 600,  "rent": 60,  "group": 0,  "color": "#c0392b"},
    {"name": "찬스",     "type": "chance", "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "부산",     "type": "prop",   "price": 600,  "rent": 60,  "group": 0,  "color": "#c0392b"},
    {"name": "소득세",   "type": "tax",    "price": 200,  "rent": 0,   "group": -1, "color": ""},
    {"name": "철도 A",   "type": "rail",   "price": 400,  "rent": 100, "group": -1, "color": ""},
    {"name": "인천",     "type": "prop",   "price": 800,  "rent": 80,  "group": 1,  "color": "#8e44ad"},
    {"name": "운명",     "type": "fate",   "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "대전",     "type": "prop",   "price": 800,  "rent": 80,  "group": 1,  "color": "#8e44ad"},
    {"name": "제주",     "type": "prop",   "price": 900,  "rent": 90,  "group": 1,  "color": "#8e44ad"},
    # 10~19 (좌측, 아→위)
    {"name": "여행",     "type": "visit",  "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "광주",     "type": "prop",   "price": 1000, "rent": 100, "group": 2,  "color": "#d35400"},
    {"name": "전기",     "type": "util",   "price": 300,  "rent": 0,   "group": -1, "color": ""},
    {"name": "울산",     "type": "prop",   "price": 1000, "rent": 100, "group": 2,  "color": "#d35400"},
    {"name": "대구",     "type": "prop",   "price": 1100, "rent": 110, "group": 2,  "color": "#d35400"},
    {"name": "철도 B",   "type": "rail",   "price": 400,  "rent": 100, "group": -1, "color": ""},
    {"name": "수원",     "type": "prop",   "price": 1200, "rent": 120, "group": 3,  "color": "#c0392b"},
    {"name": "찬스",     "type": "chance", "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "고양",     "type": "prop",   "price": 1300, "rent": 130, "group": 3,  "color": "#c0392b"},
    {"name": "성남",     "type": "prop",   "price": 1400, "rent": 140, "group": 3,  "color": "#c0392b"},
    # 20~29 (상단, 왼→오)
    {"name": "무인도",   "type": "jail",   "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "청주",     "type": "prop",   "price": 1400, "rent": 140, "group": 4,  "color": "#27ae60"},
    {"name": "운명",     "type": "fate",   "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "전주",     "type": "prop",   "price": 1500, "rent": 150, "group": 4,  "color": "#27ae60"},
    {"name": "춘천",     "type": "prop",   "price": 1600, "rent": 160, "group": 4,  "color": "#27ae60"},
    {"name": "철도 C",   "type": "rail",   "price": 400,  "rent": 100, "group": -1, "color": ""},
    {"name": "강릉",     "type": "prop",   "price": 1600, "rent": 160, "group": 5,  "color": "#2980b9"},
    {"name": "찬스",     "type": "chance", "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "원주",     "type": "prop",   "price": 1700, "rent": 170, "group": 5,  "color": "#2980b9"},
    {"name": "속초",     "type": "prop",   "price": 1800, "rent": 180, "group": 5,  "color": "#2980b9"},
    # 30~39 (우측, 위→아)
    {"name": "무료주차", "type": "free",   "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "평택",     "type": "prop",   "price": 1800, "rent": 180, "group": 6,  "color": "#e74c3c"},
    {"name": "운명",     "type": "fate",   "price": 0,    "rent": 0,   "group": -1, "color": ""},
    {"name": "천안",     "type": "prop",   "price": 1900, "rent": 190, "group": 6,  "color": "#e74c3c"},
    {"name": "아산",     "type": "prop",   "price": 2000, "rent": 200, "group": 6,  "color": "#e74c3c"},
    {"name": "철도 D",   "type": "rail",   "price": 400,  "rent": 100, "group": -1, "color": ""},
    {"name": "파주",     "type": "prop",   "price": 2200, "rent": 220, "group": 7,  "color": "#f39c12"},
    {"name": "가스",     "type": "util",   "price": 300,  "rent": 0,   "group": -1, "color": ""},
    {"name": "김포",     "type": "prop",   "price": 2200, "rent": 220, "group": 7,  "color": "#f39c12"},
    {"name": "사치세",   "type": "tax",    "price": 300,  "rent": 0,   "group": -1, "color": ""},
]

# 그룹별 총 칸 수
GROUP_SIZE = {0: 2, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 2}

# 집/호텔 건설비
BUILD_COST = {0: 200, 1: 250, 2: 300, 3: 350, 4: 350, 5: 400, 6: 400, 7: 500}
HOTEL_COST = {k: v * 5 for k, v in BUILD_COST.items()}

# 통행료 배수 (집 수에 따라)  0집=기본, 1집=*5, 2집=*15, 3집=*45, 4집(호텔)=*80
RENT_MULT = [1, 5, 15, 45, 80]

# 찬스/운명 카드
CHANCE_CARDS = [
    {"text": "은행 배당금 +100", "type": "money", "amount": 100},
    {"text": "세금 환급 +150", "type": "money", "amount": 150},
    {"text": "생일 선물! 각 플레이어에게 50씩 받기", "type": "birthday", "amount": 50},
    {"text": "수리비 청구 -100", "type": "money", "amount": -100},
    {"text": "의료비 청구 -150", "type": "money", "amount": -150},
    {"text": "학교 수업료 -200", "type": "money", "amount": -200},
    {"text": "투자 수익 +200", "type": "money", "amount": 200},
    {"text": "출발점으로 이동! +200 통과 보너스", "type": "goto", "target": 0},
    {"text": "무인도로 이동!", "type": "goto_jail"},
    {"text": "뒤로 3칸 이동", "type": "move", "amount": -3},
    {"text": "앞으로 6칸 이동", "type": "move", "amount": 6},
    {"text": "가장 가까운 철도로 이동", "type": "nearest_rail"},
    {"text": "각 집마다 40, 호텔마다 115 납부", "type": "repair"},
    {"text": "은행 오류! +500 지급", "type": "money", "amount": 500},
]

FATE_CARDS = [
    {"text": "복권 당첨! +300", "type": "money", "amount": 300},
    {"text": "과태료 -50", "type": "money", "amount": -50},
    {"text": "보험금 수령 +100", "type": "money", "amount": 100},
    {"text": "자동차 수리비 -100", "type": "money", "amount": -100},
    {"text": "콘서트 수익 +150", "type": "money", "amount": 150},
    {"text": "여행 경비 -100", "type": "money", "amount": -100},
    {"text": "출발점으로 이동! +200", "type": "goto", "target": 0},
    {"text": "무인도로 이동!", "type": "goto_jail"},
    {"text": "앞으로 3칸 이동", "type": "move", "amount": 3},
    {"text": "각 플레이어에게 50씩 받기", "type": "birthday", "amount": 50},
    {"text": "탈세 적발 -200", "type": "money", "amount": -200},
    {"text": "은행 이자 +200", "type": "money", "amount": 200},
]

PLAYER_COLORS = ["#e74c3c", "#3498db", "#2ecc71", "#f39c12"]
PLAYER_TOKENS = ["▲", "●", "◆", "★"]
BOT_NAMES = ["봇 알파", "봇 베타", "봇 감마"]

JAIL_BAIL = 500
START_MONEY = 8000
PASS_GO_BONUS = 200
MORTGAGE_RATE = 0.5   # 저당 시 매입가의 50% 환급
UNMORTGAGE_RATE = 0.6  # 저당 해제 시 매입가의 60% 지불

# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════

GAME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

.bm-root { font-family:'Noto Sans KR',sans-serif; padding:0; }

/* ─── 보드 ─────────────────────────────────────────── */
.bm-board {
    display: grid;
    grid-template-columns: 80px repeat(9,1fr) 80px;
    grid-template-rows: 80px repeat(9,1fr) 80px;
    width: 100%; aspect-ratio: 1;
    border: 2px solid #2c3e50;
    border-radius: 8px;
    overflow: hidden;
    background: #ecf0f1;
    font-size: 10px;
}

.bm-cell {
    border: 1px solid #bdc3c7;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 2px; text-align: center;
    background: #fefefe; position: relative;
    overflow: hidden; cursor: default;
}
.bm-cell:hover { background: #f8f9fa; }
.bm-cell.corner { font-weight: 700; font-size: 9px; }
.bm-cell.mortgaged { opacity: 0.45; background: #dfe6e9 !important; }

.bm-color-bar {
    width: 100%; height: 10px; flex-shrink: 0;
}
.bm-cell-name {
    font-size: 8.5px; line-height: 1.2; color: #2c3e50;
    font-weight: 500; padding: 1px 0;
}
.bm-cell-price { font-size: 7.5px; color: #7f8c8d; }
.bm-cell-owner {
    position: absolute; bottom: 2px; right: 2px;
    width: 8px; height: 8px; border-radius: 50%;
    border: 1px solid #fff;
}
.bm-houses {
    display: flex; gap: 1px; flex-wrap: wrap;
    justify-content: center; margin-top: 1px;
}
.bm-house { width: 6px; height: 6px; background: #27ae60; border-radius: 1px; }
.bm-hotel { width: 10px; height: 7px; background: #e74c3c; border-radius: 1px; font-size: 6px; }

.bm-center {
    grid-column: 2/11; grid-row: 2/11;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: linear-gradient(135deg,#ecf0f1,#dfe6e9);
    font-size: 22px; font-weight: 900; color: #2c3e50;
    letter-spacing: 2px;
}

.bm-token {
    display: inline-flex; align-items: center; justify-content: center;
    width: 18px; height: 18px; border-radius: 50%;
    font-size: 9px; font-weight: 700; color: #fff;
    border: 1.5px solid rgba(255,255,255,0.6);
    margin: 1px; box-shadow: 0 1px 3px rgba(0,0,0,0.3);
}
.bm-tokens-row {
    position: absolute; bottom: 0; left: 0; right: 0;
    display: flex; flex-wrap: wrap; justify-content: center;
    padding: 1px;
}

/* ─── 사이드 패널 ─────────────────────────────────── */
.bm-panel {
    background: #fefefe; border: 1px solid #dfe6e9;
    border-radius: 12px; padding: 14px; margin-bottom: 12px;
}
.bm-panel h3 {
    font-size: 13px; font-weight: 700; margin: 0 0 10px 0;
    color: #2c3e50; border-bottom: 1px solid #ecf0f1; padding-bottom: 6px;
}
.bm-player-row {
    display: flex; align-items: center; gap: 8px;
    padding: 6px 0; border-bottom: 1px solid #ecf0f1; font-size: 12px;
}
.bm-player-row:last-child { border-bottom: none; }
.bm-player-row.active-p {
    background: #eaf4fe; margin: 0 -8px; padding: 6px 8px;
    border-radius: 6px; border-bottom: none;
}
.bm-player-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.bm-player-name { flex: 1; font-weight: 600; color: #2c3e50; }
.bm-player-money { color: #16a085; font-weight: 700; font-size: 11px; }
.bm-player-jail { font-size: 10px; color: #e74c3c; }
.bm-player-bankrupt { font-size: 11px; color: #e74c3c; text-decoration: line-through; }

.bm-dice-area { text-align: center; margin: 8px 0; }
.bm-dice { font-size: 34px; letter-spacing: 6px; min-height: 44px; line-height: 1; }
.bm-turn-label { font-size: 12px; color: #7f8c8d; margin-bottom: 6px; }

.bm-log {
    max-height: 160px; overflow-y: auto;
    font-size: 11px; color: #555; line-height: 1.7;
}
.bm-log-entry { padding: 2px 0; border-bottom: 1px solid #ecf0f1; }
.bm-log-entry:last-child { border-bottom: none; }
.bm-log-entry.important { color: #e74c3c; font-weight: 700; }
.bm-log-entry.gain { color: #27ae60; }
.bm-log-entry.lose { color: #c0392b; }

.bm-card-popup {
    background: #fffef2; border: 2px solid #f39c12;
    border-radius: 10px; padding: 12px; margin: 8px 0;
    text-align: center; font-size: 13px; color: #2c3e50; font-weight: 600;
}

.bm-prop-panel { margin: 4px 0; }
.bm-prop-item {
    display: flex; align-items: center; gap: 6px;
    padding: 4px 0; font-size: 11px; color: #2c3e50;
    border-bottom: 1px solid #ecf0f1;
}
.bm-prop-item:last-child { border-bottom: none; }
.bm-prop-dot { width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0; }
.bm-prop-name { flex: 1; }
.bm-prop-status { font-size: 10px; color: #7f8c8d; }
.bm-prop-status.mortgaged { color: #e74c3c; }
.bm-prop-status.hotel { color: #e74c3c; font-weight: 700; }
.bm-prop-status.houses { color: #27ae60; font-weight: 700; }

/* ─── 버튼 ──────────────────────────────────────────── */
.stButton>button {
    font-family: 'Noto Sans KR', sans-serif !important;
    border-radius: 8px !important; font-size: 13px !important;
    font-weight: 600 !important;
}

/* ─── 모달 오버레이 ─────────────────────────────────── */
.bm-modal-bg {
    background: rgba(44,62,80,0.7); border-radius: 12px;
    padding: 20px; margin: 8px 0;
}
.bm-modal {
    background: #fff; border-radius: 10px; padding: 20px;
    max-width: 400px; margin: 0 auto; text-align: center;
}
.bm-modal h3 { font-size: 16px; font-weight: 700; color: #2c3e50; margin-bottom: 8px; }
.bm-modal p  { font-size: 13px; color: #555; margin-bottom: 14px; line-height: 1.6; }

/* ─── 승자 화면 ─────────────────────────────────────── */
.bm-winner {
    text-align: center; padding: 40px 20px;
}
.bm-winner h1 { font-size: 2rem; font-weight: 900; margin-bottom: 12px; }
.bm-winner p  { font-size: 14px; color: #555; margin-bottom: 8px; }
</style>
"""

# ══════════════════════════════════════════════════════════
#  GAME STATE HELPERS
# ══════════════════════════════════════════════════════════

def fresh_cells():
    import copy
    cells = copy.deepcopy(CELLS)
    for c in cells:
        c["owner"] = None
        c["houses"] = 0        # 0~3 = 집, 4 = 호텔
        c["mortgaged"] = False
    return cells

def init_game(my_name, bot_count, difficulty):
    players = []
    players.append({
        "name": my_name, "money": START_MONEY, "pos": 0,
        "color": PLAYER_COLORS[0], "token": PLAYER_TOKENS[0],
        "is_bot": False, "bankrupt": False, "jail_turns": 0,
        "jail_free": 0,   # 무인도 탈출 카드 수
    })
    for i in range(bot_count):
        players.append({
            "name": BOT_NAMES[i], "money": START_MONEY, "pos": 0,
            "color": PLAYER_COLORS[i+1], "token": PLAYER_TOKENS[i+1],
            "is_bot": True, "bankrupt": False, "jail_turns": 0,
            "jail_free": 0,
        })
    return {
        "players": players,
        "cells": fresh_cells(),
        "turn": 0,
        "doubles": 0,
        "phase": "roll",        # roll | buy | card | build | mortgage | bail | gameover
        "log": [],
        "difficulty": difficulty,
        "pending_card": None,
        "winner": None,
        "card_shown": False,
    }

def add_log(g, msg, style=""):
    g["log"].insert(0, {"msg": msg, "style": style})
    if len(g["log"]) > 60:
        g["log"] = g["log"][:60]

def active_players(g):
    return [p for p in g["players"] if not p["bankrupt"]]

def check_winner(g):
    alive = active_players(g)
    if len(alive) == 1:
        g["winner"] = alive[0]["name"]
        g["phase"] = "gameover"
        return True
    return False

# 그룹 독점 여부
def owns_group(g, player_idx, group):
    if group < 0:
        return False
    total = GROUP_SIZE.get(group, 0)
    owned = sum(1 for c in g["cells"] if c.get("group") == group and c.get("owner") == player_idx)
    return owned == total

# 통행료 계산
def calc_rent(g, cell_idx, roll_total=0):
    cell = g["cells"][cell_idx]
    owner = cell.get("owner")
    if owner is None or cell.get("mortgaged"):
        return 0
    t = cell["type"]
    if t == "prop":
        base = cell["rent"]
        h = cell["houses"]
        mult = RENT_MULT[min(h, 4)]
        # 독점 + 집 없으면 2배
        if h == 0 and owns_group(g, owner, cell["group"]):
            return base * 2
        return base * mult
    elif t == "rail":
        owned_rails = sum(1 for c in g["cells"] if c["type"] == "rail" and c.get("owner") == owner)
        return 100 * owned_rails
    elif t == "util":
        owned_utils = sum(1 for c in g["cells"] if c["type"] == "util" and c.get("owner") == owner)
        if roll_total == 0:
            roll_total = random.randint(2, 12)
        return roll_total * (4 if owned_utils == 1 else 10)
    return 0

# 가장 가까운 철도 인덱스
def nearest_rail(pos):
    rails = [i for i, c in enumerate(CELLS) if c["type"] == "rail"]
    best = min(rails, key=lambda r: (r - pos) % 40)
    return best

# ══════════════════════════════════════════════════════════
#  MOVE & LAND
# ══════════════════════════════════════════════════════════

def move_player(g, pidx, steps):
    p = g["players"][pidx]
    old = p["pos"]
    new = (old + steps) % 40
    if steps > 0 and new <= old and new != 0:
        p["money"] += PASS_GO_BONUS
        add_log(g, f"🚩 {p['name']} 출발점 통과! +{PASS_GO_BONUS}", "gain")
    p["pos"] = new

def send_to_jail(g, pidx):
    p = g["players"][pidx]
    p["pos"] = 20
    p["jail_turns"] = 3
    add_log(g, f"🔒 {p['name']} 무인도로!", "lose")

def land_cell(g, pidx, roll_total):
    """셀에 착지 후 처리. phase를 변경하거나 즉시 처리."""
    p = g["players"][pidx]
    ci = p["pos"]
    cell = g["cells"][ci]
    ct = cell["type"]
    add_log(g, f"📍 {p['name']} → {cell['name']}")

    if ct == "go":
        p["money"] += PASS_GO_BONUS
        add_log(g, f"🎉 출발! +{PASS_GO_BONUS}", "gain")

    elif ct in ("prop", "rail", "util"):
        owner = cell.get("owner")
        if owner is None:
            # 살 수 있으면 구매 단계
            g["phase"] = "buy"
            return
        elif owner == pidx:
            add_log(g, "🏠 자기 소유지 — 무료")
        else:
            if cell.get("mortgaged"):
                add_log(g, f"📋 {cell['name']} 저당 중 — 통행료 없음")
            else:
                rent = calc_rent(g, ci, roll_total)
                pay_rent(g, pidx, owner, rent, cell["name"])
        check_winner(g)

    elif ct in ("chance", "fate"):
        pool = CHANCE_CARDS if ct == "chance" else FATE_CARDS
        card = random.choice(pool)
        g["pending_card"] = card
        g["card_shown"] = False
        g["phase"] = "card"
        return

    elif ct == "tax":
        p["money"] -= cell["price"]
        add_log(g, f"💸 {p['name']} 세금 -{cell['price']}", "lose")
        maybe_bankrupt(g, pidx)

    elif ct == "jail":
        send_to_jail(g, pidx)

    elif ct in ("visit", "free"):
        add_log(g, f"✅ {cell['name']} — 안전")

    if g["phase"] not in ("gameover",):
        g["phase"] = "roll"

def pay_rent(g, from_idx, to_idx, amount, name):
    payer = g["players"][from_idx]
    receiver = g["players"][to_idx]
    actual = min(amount, payer["money"])
    payer["money"] -= actual
    receiver["money"] += actual
    add_log(g, f"💸 {payer['name']} → {receiver['name']} 통행료 {actual} ({name})", "lose")
    maybe_bankrupt(g, from_idx)

def maybe_bankrupt(g, pidx):
    p = g["players"][pidx]
    if p["money"] < 0:
        # 저당으로 자산 청산 시도
        for ci, cell in enumerate(g["cells"]):
            if cell.get("owner") == pidx and not cell.get("mortgaged"):
                if p["money"] >= 0:
                    break
                mortgage_property(g, pidx, ci)
        if p["money"] < 0:
            p["bankrupt"] = True
            p["money"] = 0
            # 소유지 반환
            for cell in g["cells"]:
                if cell.get("owner") == pidx:
                    cell["owner"] = None
                    cell["houses"] = 0
                    cell["mortgaged"] = False
            add_log(g, f"💀 {p['name']} 파산!", "important")
            check_winner(g)

def mortgage_property(g, pidx, ci):
    cell = g["cells"][ci]
    if cell.get("owner") != pidx or cell.get("mortgaged"):
        return False
    if cell["houses"] > 0:
        return False  # 집 있으면 먼저 집 매각
    val = int(cell["price"] * MORTGAGE_RATE)
    cell["mortgaged"] = True
    g["players"][pidx]["money"] += val
    add_log(g, f"📋 {g['players'][pidx]['name']} {cell['name']} 저당 +{val}", "lose")
    return True

def unmortgage_property(g, pidx, ci):
    cell = g["cells"][ci]
    if cell.get("owner") != pidx or not cell.get("mortgaged"):
        return False
    cost = int(cell["price"] * UNMORTGAGE_RATE)
    if g["players"][pidx]["money"] < cost:
        return False
    cell["mortgaged"] = False
    g["players"][pidx]["money"] -= cost
    add_log(g, f"✅ {g['players'][pidx]['name']} {cell['name']} 저당 해제 -{cost}")
    return True

def apply_card(g, pidx, card):
    p = g["players"][pidx]
    ct = card["type"]
    if ct == "money":
        p["money"] += card["amount"]
        style = "gain" if card["amount"] > 0 else "lose"
        add_log(g, f"🃏 {p['name']} {card['text']} ({card['amount']:+})", style)
        if card["amount"] < 0:
            maybe_bankrupt(g, pidx)
    elif ct == "birthday":
        for i, other in enumerate(g["players"]):
            if i != pidx and not other["bankrupt"]:
                actual = min(card["amount"], other["money"])
                other["money"] -= actual
                p["money"] += actual
        add_log(g, f"🎂 {p['name']} 생일! 각자 {card['amount']} 받음", "gain")
    elif ct == "goto":
        target = card["target"]
        if target == 0:
            p["money"] += PASS_GO_BONUS
        p["pos"] = target
        add_log(g, f"🚀 {p['name']} {CELLS[target]['name']}으로 이동!")
        land_cell(g, pidx, 0)
        return
    elif ct == "goto_jail":
        send_to_jail(g, pidx)
    elif ct == "move":
        amt = card["amount"]
        move_player(g, pidx, amt)
        add_log(g, f"👣 {p['name']} {amt:+}칸 이동")
        land_cell(g, pidx, 0)
        return
    elif ct == "nearest_rail":
        nr = nearest_rail(p["pos"])
        steps = (nr - p["pos"]) % 40
        move_player(g, pidx, steps)
        add_log(g, f"🚂 {p['name']} 가장 가까운 철도로!")
        land_cell(g, pidx, 0)
        return
    elif ct == "repair":
        houses = sum(1 for c in g["cells"] if c.get("owner") == pidx and 0 < c["houses"] < 4)
        hotels = sum(1 for c in g["cells"] if c.get("owner") == pidx and c["houses"] == 4)
        cost = houses * 40 + hotels * 115
        p["money"] -= cost
        add_log(g, f"🔧 {p['name']} 수리비 -{cost} (집{houses}/호텔{hotels})", "lose")
        maybe_bankrupt(g, pidx)

    if g["phase"] not in ("gameover",):
        g["phase"] = "roll"

# ══════════════════════════════════════════════════════════
#  BOT AI
# ══════════════════════════════════════════════════════════

def bot_think(g, pidx):
    """봇 구매·건설·저당 결정. True 반환 시 추가 행동 있음."""
    p = g["players"][pidx]
    diff = g["difficulty"]

    # ── 구매 결정 ──────────────────────────────────────
    if g["phase"] == "buy":
        ci = p["pos"]
        cell = g["cells"][ci]
        price = cell["price"]

        buy = False
        if diff == "easy":
            buy = random.random() > 0.35 and p["money"] >= price
        elif diff == "normal":
            buy = p["money"] >= price * 1.5
        elif diff == "hard":
            # 독점 완성 가능하면 무조건 구매
            group = cell.get("group", -1)
            if group >= 0:
                need = GROUP_SIZE.get(group, 0)
                have = sum(1 for c in g["cells"] if c.get("group") == group and c.get("owner") == pidx)
                if have == need - 1 and p["money"] >= price:
                    buy = True
                else:
                    buy = p["money"] >= price * 1.2
            else:
                buy = p["money"] >= price

        if buy:
            cell["owner"] = pidx
            p["money"] -= price
            add_log(g, f"🏠 {p['name']} {cell['name']} 매입! -{price}", "lose")
        else:
            add_log(g, f"↩️ {p['name']} {cell['name']} 패스")
        g["phase"] = "roll"
        return False

    # ── 찬스/운명 카드 ─────────────────────────────────
    if g["phase"] == "card":
        card = g["pending_card"]
        if card:
            apply_card(g, pidx, card)
            g["pending_card"] = None
        return False

    # ── 무인도 보석금 ───────────────────────────────────
    if g["phase"] == "bail":
        if diff == "hard" and p["money"] >= JAIL_BAIL * 1.5:
            p["money"] -= JAIL_BAIL
            p["jail_turns"] = 0
            add_log(g, f"💰 {p['name']} 보석금 납부!", "lose")
        g["phase"] = "roll"
        return False

    # ── 건설 (hard 봇만) ───────────────────────────────
    if diff == "hard":
        built = False
        for ci, cell in enumerate(g["cells"]):
            if cell.get("owner") != pidx or cell["type"] != "prop":
                continue
            if not owns_group(g, pidx, cell["group"]):
                continue
            if cell["houses"] >= 4 or cell.get("mortgaged"):
                continue
            cost = BUILD_COST.get(cell["group"], 300)
            if p["money"] >= cost * 1.3:
                cell["houses"] += 1
                p["money"] -= cost
                label = "호텔 🏨" if cell["houses"] == 4 else f"집 {cell['houses']}채 🏠"
                add_log(g, f"🔨 {p['name']} {cell['name']} {label} 건설 -{cost}")
                built = True
        return built

    return False

# ══════════════════════════════════════════════════════════
#  BOARD RENDERING (HTML)
# ══════════════════════════════════════════════════════════

def render_board_html(g):
    players = g["players"]
    cells = g["cells"]

    # 각 칸에 플레이어 위치 매핑
    cell_players = {}
    for pi, p in enumerate(players):
        if not p["bankrupt"]:
            cell_players.setdefault(p["pos"], []).append(pi)

    def cell_html(ci):
        cell = cells[ci]
        ct = cell["type"]
        owner = cell.get("owner")
        mortgaged = cell.get("mortgaged", False)
        houses = cell.get("houses", 0)

        extra_cls = "mortgaged" if mortgaged else ""

        # 색상 바
        color_bar = ""
        if ct == "prop" and cell.get("color"):
            color_bar = f"<div class='bm-color-bar' style='background:{cell['color']};'></div>"
        elif ct == "rail":
            color_bar = "<div class='bm-color-bar' style='background:#2c3e50;'></div>"
        elif ct == "util":
            color_bar = "<div class='bm-color-bar' style='background:#7f8c8d;'></div>"

        # 집/호텔
        house_html = ""
        if houses > 0 and ct == "prop":
            if houses == 4:
                house_html = "<div class='bm-houses'><div class='bm-hotel'>H</div></div>"
            else:
                house_html = "<div class='bm-houses'>" + "".join(["<div class='bm-house'></div>"]*houses) + "</div>"

        # 소유자 점
        owner_dot = ""
        if owner is not None:
            oc = players[owner]["color"]
            owner_dot = f"<div class='bm-cell-owner' style='background:{oc};'></div>"

        # 셀 이름
        name = cell["name"]
        price_txt = f"<div class='bm-cell-price'>{cell['price']:,}</div>" if cell["price"] > 0 else ""

        # 특수 아이콘
        special = ""
        if ct == "go":      special = "🚩"
        elif ct == "jail":  special = "🔒"
        elif ct == "visit": special = "✈️"
        elif ct == "free":  special = "🅿️"
        elif ct == "tax":   special = "💸"
        elif ct == "chance":special = "?"
        elif ct == "fate":  special = "★"

        # 토큰
        tokens_html = ""
        if ci in cell_players:
            tokens = ""
            for pi in cell_players[ci]:
                pc = players[pi]["color"]
                pt = players[pi]["token"]
                tokens += f"<div class='bm-token' style='background:{pc};'>{pt}</div>"
            tokens_html = f"<div class='bm-tokens-row'>{tokens}</div>"

        corner_cls = "corner" if ct in ("go","jail","visit","free") else ""

        return (
            f"<div class='bm-cell {corner_cls} {extra_cls}'>"
            f"{color_bar}"
            f"<div style='font-size:11px;'>{special}</div>"
            f"<div class='bm-cell-name'>{name}</div>"
            f"{price_txt}"
            f"{house_html}"
            f"{owner_dot}"
            f"{tokens_html}"
            f"</div>"
        )

    # 40칸 배치: 11×11 그리드
    # 하단행(0~10): col 11→1, row 11
    # 좌측열(11~20): col 1, row 10→1
    # 상단행(21~30): col 2→11, row 1  (단 30은 col11,row1)
    # 우측열(31~39): col 11, row 2→10

    grid = {}
    # 하단 (row=11)
    for i, ci in enumerate(range(10, -1, -1)):
        grid[(11, 11-i)] = cell_html(ci)
    # 좌측 (col=1)
    for i, ci in enumerate(range(11, 21)):
        grid[(10-i, 1)] = cell_html(ci)
    # 상단 (row=1)
    for i, ci in enumerate(range(20, 31)):
        grid[(1, 1+i)] = cell_html(ci)
    # 우측 (col=11)
    for i, ci in enumerate(range(31, 40)):
        grid[(2+i, 11)] = cell_html(ci)

    # 중앙
    center_html = "<div class='bm-center'>🎲<br>부루마블<br><span style='font-size:13px;font-weight:400;color:#7f8c8d;'>효민 월드</span></div>"

    html = "<div class='bm-board'>"
    for row in range(1, 12):
        for col in range(1, 12):
            if row in range(2, 11) and col in range(2, 11):
                if row == 2 and col == 2:
                    html += center_html
            else:
                key = (row, col)
                html += grid.get(key, "<div class='bm-cell'></div>")
    html += "</div>"
    return html

# ══════════════════════════════════════════════════════════
#  MAIN RENDER
# ══════════════════════════════════════════════════════════

def render():
    st.markdown(GAME_CSS, unsafe_allow_html=True)

    # ── 게임 없음 → 설정 화면 ───────────────────────────
    if "bm_game" not in st.session_state:
        _render_setup()
        return

    g = st.session_state.bm_game

    if g["phase"] == "gameover":
        _render_winner(g)
        return

    _render_game(g)

# ──────────────────────────────────────────────────────────
def _render_setup():
    st.markdown("<div class='bm-root'>", unsafe_allow_html=True)
    st.title("🎲 부루마블")
    st.caption("봇과 함께하는 고퀄 부루마블 — 집·호텔·저당·무인도 보석금 완비")

    c1, c2 = st.columns(2)
    with c1:
        my_name = st.text_input("내 이름", value="플레이어", max_chars=8)
        bot_count = st.selectbox("봇 수", [1, 2, 3], index=1, format_func=lambda x: f"봇 {x}명 ({x+1}인 게임)")
    with c2:
        difficulty = st.selectbox("봇 난이도", ["easy", "normal", "hard"],
                                  index=1, format_func=lambda x: {"easy":"쉬움 — 무작위","normal":"보통 — 상황 판단","hard":"어려움 — 공격적 전략"}[x])

    st.markdown("---")
    st.markdown("""
    **게임 규칙 요약**
    - 시작 자금: **8,000**  |  출발점 통과: **+200**
    - 그룹 독점 시 통행료 2배, 집/호텔 건설로 최대 80배
    - 무인도 탈출: 더블 주사위 또는 보석금 **500**
    - 저당: 매입가 50% 환급, 해제 시 60% 지불
    - 철도 보유 수에 따라 통행료 ×1~4배
    """)

    if st.button("🎲 게임 시작!", use_container_width=True):
        st.session_state.bm_game = init_game(my_name, bot_count, difficulty)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────
def _render_winner(g):
    st.markdown("<div class='bm-winner'>", unsafe_allow_html=True)
    winner_name = g["winner"] or "알 수 없음"
    winner = next((p for p in g["players"] if p["name"] == winner_name), None)
    color = winner["color"] if winner else "#2c3e50"

    st.markdown(f"""
    <div class='bm-winner'>
      <h1 style='color:{color};'>🏆 {winner_name} 우승!</h1>
      <p>최후의 1인이 살아남았습니다.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**최종 자산 순위**")
    ranked = sorted(g["players"], key=lambda p: p["money"], reverse=True)
    for i, p in enumerate(ranked):
        medal = ["🥇","🥈","🥉","4️⃣"][i] if i < 4 else ""
        status = "💀 파산" if p["bankrupt"] else f"💵 {p['money']:,}"
        st.markdown(f"{medal} **{p['name']}** — {status}")

    if st.button("🔄 다시 하기", use_container_width=True):
        del st.session_state.bm_game
        st.rerun()

# ──────────────────────────────────────────────────────────
def _render_game(g):
    st.markdown("<div class='bm-root'>", unsafe_allow_html=True)

    col_board, col_side = st.columns([5, 2])

    with col_board:
        board_html = render_board_html(g)
        st.markdown(board_html, unsafe_allow_html=True)

    with col_side:
        _render_players_panel(g)
        _render_action_panel(g)
        _render_log_panel(g)

    st.markdown("</div>", unsafe_allow_html=True)

    # 봇 자동 진행
    _maybe_bot_turn(g)

def _render_players_panel(g):
    st.markdown("<div class='bm-panel'>", unsafe_allow_html=True)
    st.markdown("<h3>플레이어</h3>", unsafe_allow_html=True)
    html = ""
    for i, p in enumerate(g["players"]):
        active_cls = "active-p" if i == g["turn"] and not p["bankrupt"] else ""
        if p["bankrupt"]:
            html += f"<div class='bm-player-row'><div class='bm-player-dot' style='background:{p['color']};opacity:0.3'></div><span class='bm-player-bankrupt'>{p['name']}</span></div>"
        else:
            jail_txt = f"<span class='bm-player-jail'>🔒{p['jail_turns']}턴</span>" if p["jail_turns"] > 0 else ""
            bot_txt = " 🤖" if p["is_bot"] else ""
            html += (
                f"<div class='bm-player-row {active_cls}'>"
                f"<div class='bm-player-dot' style='background:{p['color']};'></div>"
                f"<span class='bm-player-name'>{p['token']} {p['name']}{bot_txt}</span>"
                f"<span class='bm-player-money'>{p['money']:,}</span>"
                f"{jail_txt}</div>"
            )
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def _render_action_panel(g):
    turn = g["turn"]
    p = g["players"][turn]
    phase = g["phase"]

    st.markdown("<div class='bm-panel'>", unsafe_allow_html=True)
    st.markdown(f"<div class='bm-turn-label'><span style='color:{p['color']};font-weight:700;'>{p['token']} {p['name']}</span> 차례</div>", unsafe_allow_html=True)

    if p["is_bot"]:
        st.markdown("<div class='bm-dice-area'><div class='bm-dice'>⚙️</div></div>", unsafe_allow_html=True)
        st.caption("봇이 생각 중...")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # 주사위 표시
    d1 = st.session_state.get("bm_d1", 1)
    d2 = st.session_state.get("bm_d2", 1)
    faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
    st.markdown(f"<div class='bm-dice-area'><div class='bm-dice'>{faces[d1-1]} {faces[d2-1]}</div></div>", unsafe_allow_html=True)

    # ── 무인도 ──────────────────────────────────────────
    if p["jail_turns"] > 0 and phase == "roll":
        st.info(f"🔒 무인도 {p['jail_turns']}턴 남음")
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"💰 보석금 ({JAIL_BAIL})", use_container_width=True,
                         disabled=p["money"] < JAIL_BAIL):
                p["money"] -= JAIL_BAIL
                p["jail_turns"] = 0
                add_log(g, f"💰 {p['name']} 보석금 납부!", "lose")
                st.session_state.bm_game = g
                st.rerun()
        with c2:
            if st.button("🎲 더블 도전", use_container_width=True):
                d1 = random.randint(1, 6)
                d2 = random.randint(1, 6)
                st.session_state.bm_d1 = d1
                st.session_state.bm_d2 = d2
                if d1 == d2:
                    p["jail_turns"] = 0
                    add_log(g, f"🎉 {p['name']} 더블! 탈출!")
                    move_player(g, turn, d1+d2)
                    land_cell(g, turn, d1+d2)
                else:
                    p["jail_turns"] -= 1
                    add_log(g, f"😔 {p['name']} 더블 실패. ({p['jail_turns']}턴 남음)")
                    if p["jail_turns"] <= 0:
                        p["jail_turns"] = 0
                        add_log(g, f"{p['name']} 강제 석방")
                        move_player(g, turn, d1+d2)
                        land_cell(g, turn, d1+d2)
                    else:
                        g["phase"] = "roll"
                _advance_turn(g)
                st.session_state.bm_game = g
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return

    # ── 주사위 굴리기 ────────────────────────────────────
    if phase == "roll":
        if st.button("🎲 주사위 굴리기", use_container_width=True, type="primary"):
            d1 = random.randint(1, 6)
            d2 = random.randint(1, 6)
            st.session_state.bm_d1 = d1
            st.session_state.bm_d2 = d2
            total = d1 + d2
            isDouble = d1 == d2

            if isDouble:
                g["doubles"] += 1
                if g["doubles"] >= 3:
                    send_to_jail(g, turn)
                    add_log(g, f"3연속 더블! {p['name']} 무인도!")
                    _advance_turn(g)
                    st.session_state.bm_game = g
                    st.rerun()
                    return
                add_log(g, f"🎲 {p['name']} 더블! ({d1}+{d2}={total})")
            else:
                g["doubles"] = 0
                add_log(g, f"🎲 {p['name']} {d1}+{d2}={total}")

            move_player(g, turn, total)
            land_cell(g, turn, total)

            if not isDouble and g["phase"] not in ("buy","card","gameover"):
                _advance_turn(g)

            st.session_state.bm_game = g
            st.rerun()

    # ── 구매 ─────────────────────────────────────────────
    elif phase == "buy":
        ci = p["pos"]
        cell = g["cells"][ci]
        st.markdown(f"<div class='bm-card-popup'>🏠 {cell['name']}<br>매입가 <b>{cell['price']:,}</b><br>기본 통행료 {cell['rent']:,}</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button(f"✅ 매입", use_container_width=True, disabled=p["money"] < cell["price"]):
                cell["owner"] = turn
                p["money"] -= cell["price"]
                add_log(g, f"🏠 {p['name']} {cell['name']} 매입! -{cell['price']}", "lose")
                g["phase"] = "roll"
                _advance_turn(g)
                st.session_state.bm_game = g
                st.rerun()
        with c2:
            if st.button("↩️ 패스", use_container_width=True):
                g["phase"] = "roll"
                _advance_turn(g)
                st.session_state.bm_game = g
                st.rerun()

    # ── 카드 ─────────────────────────────────────────────
    elif phase == "card":
        card = g.get("pending_card")
        if card:
            st.markdown(f"<div class='bm-card-popup'>🃏 {card['text']}</div>", unsafe_allow_html=True)
            if st.button("확인", use_container_width=True):
                apply_card(g, turn, card)
                g["pending_card"] = None
                if g["phase"] not in ("gameover",):
                    _advance_turn(g)
                st.session_state.bm_game = g
                st.rerun()

    # ── 건설/저당 탭 ─────────────────────────────────────
    if phase == "roll" and not p["is_bot"] and not p["bankrupt"]:
        with st.expander("🏗️ 건설 / 저당 관리"):
            _render_build_mortgage(g, turn)

    st.markdown("</div>", unsafe_allow_html=True)

def _render_build_mortgage(g, pidx):
    p = g["players"][pidx]
    my_cells = [(ci, cell) for ci, cell in enumerate(g["cells"]) if cell.get("owner") == pidx]

    if not my_cells:
        st.caption("소유한 땅이 없습니다.")
        return

    for ci, cell in my_cells:
        if cell["type"] != "prop":
            continue
        group = cell.get("group", -1)
        can_build = owns_group(g, pidx, group) and not cell.get("mortgaged") and cell["houses"] < 4
        build_cost = BUILD_COST.get(group, 300)
        color = cell.get("color", "#ccc")

        h = cell["houses"]
        h_label = "호텔" if h == 4 else f"집 {h}채"
        mort_label = "저당 중" if cell.get("mortgaged") else "정상"

        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            st.markdown(f"<div style='display:flex;align-items:center;gap:6px;font-size:12px;'>"
                        f"<div style='width:10px;height:10px;background:{color};border-radius:2px;'></div>"
                        f"<b>{cell['name']}</b> — {h_label} / {mort_label}</div>", unsafe_allow_html=True)
        with c2:
            if can_build and p["money"] >= build_cost:
                label = "🏨 호텔" if h == 3 else "🏠 건설"
                if st.button(label, key=f"build_{ci}", use_container_width=True):
                    cell["houses"] += 1
                    p["money"] -= build_cost
                    lbl = "호텔 건설 🏨" if cell["houses"] == 4 else f"집 {cell['houses']}채 🏠"
                    add_log(g, f"🔨 {p['name']} {cell['name']} {lbl} -{build_cost}")
                    st.session_state.bm_game = g
                    st.rerun()
        with c3:
            if not cell.get("mortgaged") and cell["houses"] == 0:
                val = int(cell["price"] * MORTGAGE_RATE)
                if st.button(f"📋 저당+{val}", key=f"mort_{ci}", use_container_width=True):
                    mortgage_property(g, pidx, ci)
                    st.session_state.bm_game = g
                    st.rerun()
            elif cell.get("mortgaged"):
                cost = int(cell["price"] * UNMORTGAGE_RATE)
                if st.button(f"✅해제-{cost}", key=f"unmort_{ci}",
                             use_container_width=True, disabled=p["money"] < cost):
                    unmortgage_property(g, pidx, ci)
                    st.session_state.bm_game = g
                    st.rerun()

def _render_log_panel(g):
    st.markdown("<div class='bm-panel'>", unsafe_allow_html=True)
    st.markdown("<h3>게임 로그</h3>", unsafe_allow_html=True)
    html = "<div class='bm-log'>"
    for entry in g["log"][:25]:
        cls = entry.get("style", "")
        html += f"<div class='bm-log-entry {cls}'>{entry['msg']}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def _advance_turn(g):
    """다음 살아있는 플레이어로 턴 넘김."""
    if g["phase"] == "gameover":
        return
    n = len(g["players"])
    nxt = (g["turn"] + 1) % n
    attempts = 0
    while g["players"][nxt]["bankrupt"] and attempts < n:
        nxt = (nxt + 1) % n
        attempts += 1
    g["turn"] = nxt
    g["phase"] = "roll"

def _maybe_bot_turn(g):
    """봇 턴이면 자동으로 처리 후 rerun."""
    if g["phase"] == "gameover":
        return
    p = g["players"][g["turn"]]
    if not p["is_bot"] or p["bankrupt"]:
        return

    time.sleep(0.4)

    phase = g["phase"]

    # 무인도
    if p["jail_turns"] > 0 and phase == "roll":
        diff = g["difficulty"]
        if diff == "hard" and p["money"] >= JAIL_BAIL:
            p["money"] -= JAIL_BAIL
            p["jail_turns"] = 0
            add_log(g, f"💰 {p['name']} 보석금 납부!")
        else:
            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            st.session_state.bm_d1 = d1
            st.session_state.bm_d2 = d2
            if d1 == d2:
                p["jail_turns"] = 0
                add_log(g, f"🎉 {p['name']} 더블 탈출!")
                move_player(g, g["turn"], d1+d2)
                land_cell(g, g["turn"], d1+d2)
            else:
                p["jail_turns"] -= 1
                add_log(g, f"😔 {p['name']} 더블 실패")
                if p["jail_turns"] <= 0:
                    p["jail_turns"] = 0
                    move_player(g, g["turn"], d1+d2)
                    land_cell(g, g["turn"], d1+d2)
        _advance_turn(g)
        st.session_state.bm_game = g
        st.rerun()
        return

    # 구매/카드
    if phase in ("buy", "card", "bail"):
        bot_think(g, g["turn"])
        if g["phase"] not in ("gameover",):
            _advance_turn(g)
        st.session_state.bm_game = g
        st.rerun()
        return

    # 주사위
    if phase == "roll":
        # 건설 먼저
        bot_think(g, g["turn"])

        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        total = d1+d2
        isDouble = d1==d2
        st.session_state.bm_d1 = d1
        st.session_state.bm_d2 = d2

        if isDouble:
            g["doubles"] += 1
            if g["doubles"] >= 3:
                send_to_jail(g, g["turn"])
                _advance_turn(g)
                st.session_state.bm_game = g
                st.rerun()
                return
            add_log(g, f"🎲 {p['name']} 더블! ({d1}+{d2})")
        else:
            g["doubles"] = 0
            add_log(g, f"🎲 {p['name']} {d1}+{d2}={total}")

        move_player(g, g["turn"], total)
        land_cell(g, g["turn"], total)

        # buy/card는 bot_think에서 처리
        if g["phase"] in ("buy","card"):
            bot_think(g, g["turn"])

        if not isDouble and g["phase"] not in ("gameover",):
            _advance_turn(g)

        st.session_state.bm_game = g
        st.rerun()
