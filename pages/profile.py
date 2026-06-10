# pages/profile.py — MEGA ULTIMATE EDITION v4.0 👤
# 프로필 카드 애니메이션 / 자산 시각화 / 배지 / 타임라인 / 커스터마이징 완전판
import streamlit as st
import streamlit.components.v1 as components
import time
from datetime import datetime
from utils.config import (
    KST, USERS_FILE, FORGE_DATA, estate_config,
    stock_config, CRYPTO_CONFIG
)
from utils.core import format_korean_money, sync_user_data
from utils.database import load_db, save_db, log_tx, atomic_add_cash

# ══════════════════════════════════════════════════════════════════════════════
# 📦 DATA
# ══════════════════════════════════════════════════════════════════════════════

AVATARS = [
    ("🧑‍🚀","우주인"),  ("🥷","닌자"),    ("🧙","마법사"),  ("🦸","슈퍼히어로"),
    ("🧛","뱀파이어"), ("🤖","로봇"),    ("👑","왕"),      ("🐉","드래곤"),
    ("🦊","여우"),     ("🐺","늑대"),    ("🦁","사자"),    ("🐯","호랑이"),
    ("🐼","판다"),     ("🐸","개구리"),  ("🦋","나비"),    ("🌟","별의신"),
    ("🔥","불꽃왕"),   ("❄️","얼음마왕"), ("⚡","번개신"),   ("🌙","달의여신"),
    ("🌌","우주신"),   ("🎭","가면무사"), ("🦅","독수리"),  ("🐲","현무"),
    ("🌊","파도왕"),   ("🍀","행운아"),   ("💀","사신"),    ("🌈","무지개"),
    ("🎪","마술사"),   ("🦄","유니콘"),
]

AVATAR_UNLOCK_PRICE = 3_000_000_000

PROFILE_THEMES = {
    "cyan":    {"name":"사이버 시안",   "primary":"#00E5FF","secondary":"#0066FF","bg":"#020b18"},
    "gold":    {"name":"황금 왕조",     "primary":"#FFD600","secondary":"#FF9500","bg":"#0d0900"},
    "purple":  {"name":"신비 보라",     "primary":"#AA00FF","secondary":"#7700DD","bg":"#0a0010"},
    "green":   {"name":"에메랄드 숲",   "primary":"#00FF88","secondary":"#00CC55","bg":"#001208"},
    "red":     {"name":"레드 불꽃",     "primary":"#FF4B4B","secondary":"#FF0000","bg":"#120000"},
    "rainbow": {"name":"무지개 전설",   "primary":"#FF00FF","secondary":"#00FFFF","bg":"#050010"},
}

PROFILE_FRAMES = {
    "none":    {"name":"기본","icon":"⬜","price":0},
    "silver":  {"name":"실버","icon":"🥈","price":50_000_000},
    "gold":    {"name":"골드","icon":"🥇","price":200_000_000},
    "diamond": {"name":"다이아","icon":"💎","price":1_000_000_000},
    "legend":  {"name":"전설","icon":"🌌","price":10_000_000_000},
    "dragon":  {"name":"드래곤","icon":"🐉","price":50_000_000_000},
}

PROFILE_BADGES = [
    {"id":"first_login",   "icon":"🎖️","name":"첫 발걸음",   "desc":"처음 로그인"},
    {"id":"rich_5",        "icon":"💰","name":"초보 부자",    "desc":"순자산 5억 달성"},
    {"id":"landlord",      "icon":"🏢","name":"건물주",       "desc":"부동산 1채 보유"},
    {"id":"billionaire",   "icon":"💎","name":"억만장자",     "desc":"순자산 1000억 달성"},
    {"id":"weapon_master", "icon":"⚔️","name":"무기 장인",    "desc":"+10 이상 명검 보유"},
    {"id":"gambler",       "icon":"🎰","name":"도박사",       "desc":"카지노 100회 이상"},
    {"id":"miner",         "icon":"⛏️","name":"광부왕",       "desc":"광산 1000회 이상"},
    {"id":"clan_member",   "icon":"🏰","name":"클랜원",       "desc":"클랜 가입"},
    {"id":"cryptowhale",   "icon":"🐋","name":"코인 고래",    "desc":"코인 평가액 10억 이상"},
    {"id":"stock_guru",    "icon":"📈","name":"주식의 신",    "desc":"주식 평가액 10억 이상"},
    {"id":"pet_owner",     "icon":"🐾","name":"펫 주인",      "desc":"펫 레벨 10 달성"},
    {"id":"dungeon_clear", "icon":"🗡️","name":"던전 클리어",  "desc":"던전 1회 클리어"},
    {"id":"trillionaire",  "icon":"🌌","name":"조만장자",     "desc":"순자산 1조 달성"},
    {"id":"pet_legend",    "icon":"🐲","name":"전설 조련사",  "desc":"펫 레벨 40 달성"},
    {"id":"explorer",      "icon":"🗺️","name":"모험가",       "desc":"탐험 10회 완료"},
    {"id":"battle_master", "icon":"🏅","name":"배틀 마스터",  "desc":"배틀 50승"},
    {"id":"stock_king",    "icon":"📊","name":"주식왕",       "desc":"주식 100거래 달성"},
    {"id":"coin_master",   "icon":"🪙","name":"코인 장인",    "desc":"코인 총 거래 50회"},
    {"id":"fullhouse",     "icon":"🏠","name":"풀하우스",     "desc":"모든 종류 부동산 보유"},
    {"id":"speedrun",      "icon":"⚡","name":"스피드런",     "desc":"가입 1주일 내 100억"},
]

STATUS_MESSAGES = [
    "지금 막 대박났음 🎰","주식이 날아가고 있다... ✈️","코인 HODLing 중 🚀",
    "광산에서 노가다 중 ⛏️","자본주의의 꼭대기를 향해 📈","건물주의 삶은 달콤해 🏢",
    "강화 실패로 멘탈 나감 💀","오늘은 무조건 대박 🔥","효민 우주에서 살아남기 🌌",
    "부동산은 역시 최고 💎","퀘스트 완료 도전 중 📅","랭킹 1위를 향해 👑",
    "펫과 함께라면 무섭지 않아 🐾","지금 이 순간이 역사가 된다 ⚡","돈이 돈을 번다 💰",
    "리스크 없으면 리워드 없다 🎯","내 포트폴리오 지금 전설급 🌟","매일매일 성장 중 📊",
]

MILESTONES = [
    (1,  "🌱","튜토리얼",      0),
    (10, "📊","초보 투자자",   10_000_000),
    (20, "🥉","브론즈",        50_000_000),
    (25, "🥈","실버",          100_000_000),
    (30, "🥇","골드",          500_000_000),
    (35, "🏆","마스터",        1_000_000_000),
    (40, "💫","위성 자본가",   5_000_000_000),
    (50, "⭐","별의 상인",     10_000_000_000),
    (55, "🚀","우주 탐험가",   50_000_000_000),
    (60, "🌙","달 지배자",     100_000_000_000),
    (70, "🪐","행성 영주",     500_000_000_000),
    (80, "☄️","소행성 군주",   1_000_000_000_000),
    (90, "🌠","은하계 지배자", 100_000_000_000_000),
    (100,"🌌","우주신",        1_000_000_000_000_000),
]

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def get_level_from_nw(nw):
    thresholds = [
        (1_000_000_000_000_000,100,"🌌 우주신"),
        (100_000_000_000_000,  90, "🌠 은하계 지배자"),
        (10_000_000_000_000,   80, "☄️ 소행성 대군주"),
        (1_000_000_000_000,    70, "🪐 행성 영주"),
        (500_000_000_000,      60, "🌙 달 지배자"),
        (100_000_000_000,      55, "🚀 우주 탐험가"),
        (50_000_000_000,       50, "⭐ 별의 상인"),
        (10_000_000_000,       40, "💫 위성 자본가"),
        (5_000_000_000,        35, "🏆 마스터 투자자"),
        (1_000_000_000,        30, "💎 다이아 투자자"),
        (500_000_000,          25, "🥇 골드 투자자"),
        (100_000_000,          20, "🥈 실버 투자자"),
        (50_000_000,           15, "🥉 브론즈 투자자"),
        (10_000_000,           10, "📊 초보 투자자"),
        (0,                    1,  "🌱 튜토리얼 중"),
    ]
    for thresh, lv, title in thresholds:
        if nw >= thresh:
            return lv, title
    return 1, "🌱 튜토리얼 중"

def get_next_milestone(nw):
    for lv_m, icon, name, req in MILESTONES:
        if req > nw:
            return lv_m, icon, name, req
    return None, "🌌", "우주신", 1_000_000_000_000_000

def compute_badges(uid, users, market, nw):
    u = users.get(uid, {})
    badges = ["first_login"]
    if nw >= 500_000_000:         badges.append("rich_5")
    if nw >= 100_000_000_000:     badges.append("billionaire")
    if nw >= 1_000_000_000_000:   badges.append("trillionaire")
    if any(v > 0 for v in u.get('real_estate', {}).values()):
        badges.append("landlord")
    if u.get('weapon_level', 0) >= 10: badges.append("weapon_master")
    if u.get('dungeon_stats', {}).get('clears', 0) >= 1: badges.append("dungeon_clear")

    crypto_data = market.get('crypto_data', {})
    coin_val = sum(
        ci.get('qty',0) * crypto_data.get(cid,{}).get('price',0)
        for cid, ci in u.get('crypto_portfolio',{}).items()
    )
    if coin_val >= 1_000_000_000: badges.append("cryptowhale")

    stock_data = market.get('stock_data', {})
    stock_val = sum(
        u.get('portfolio',{}).get(s['id'],{}).get('qty',0) * stock_data.get(s['id'],{}).get('price',0)
        for s in stock_config
    )
    if stock_val >= 1_000_000_000: badges.append("stock_guru")

    pet_data = u.get('pet', {})
    pet_lv   = pet_data.get('level', 0)
    if pet_lv >= 10: badges.append("pet_owner")
    if pet_lv >= 40: badges.append("pet_legend")
    if pet_data.get('expeditions', 0) >= 10: badges.append("explorer")
    if pet_data.get('battles_won', 0) >= 50: badges.append("battle_master")

    return set(badges)

def get_asset_breakdown(u, market, nw):
    cash = u.get('cash', 0)
    loan = u.get('loan', 0)

    real_estate_val = sum(
        estate_config[eid]['base_price'] * cnt * 0.8
        for eid, cnt in u.get('real_estate', {}).items()
        if eid in estate_config
    )
    stock_data = market.get('stock_data', {})
    stock_val = sum(
        u.get('portfolio',{}).get(s['id'],{}).get('qty',0) * stock_data.get(s['id'],{}).get('price',0)
        for s in stock_config
    )
    crypto_data = market.get('crypto_data', {})
    coin_val = sum(
        ci.get('qty',0) * crypto_data.get(cid,{}).get('price',0)
        for cid, ci in u.get('crypto_portfolio',{}).items()
    )
    w_lv = u.get('weapon_level', 0)
    weapon_val = FORGE_DATA[w_lv]['sell'] if w_lv > 0 and w_lv in FORGE_DATA else 0

    return {
        "현금":   cash,
        "주식":   int(stock_val),
        "코인":   int(coin_val),
        "부동산": int(real_estate_val),
        "명검":   weapon_val,
        "대출":   -loan,
    }

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 ANIMATED PROFILE CARD HTML
# ══════════════════════════════════════════════════════════════════════════════

def generate_profile_card_html(uid, avatar, lv, lv_title, nw, custom_title,
                                status_msg, join_date, theme_id, frame_id,
                                badge_count, total_badges, pet_info, assets):
    theme = PROFILE_THEMES.get(theme_id, PROFILE_THEMES['cyan'])
    frame = PROFILE_FRAMES.get(frame_id, PROFILE_FRAMES['none'])
    p  = theme['primary']
    s  = theme['secondary']
    bg = theme['bg']

    nw_fmt = format_korean_money(nw)

    cur_thresh = next((req for lv_m,_,_,req in MILESTONES if nw >= req), 0)
    next_thresh = next((req for lv_m,_,_,req in reversed(MILESTONES) if req > nw), cur_thresh*10 or 10_000_000)
    if next_thresh > cur_thresh:
        progress_pct = min(100, int((nw - cur_thresh) / (next_thresh - cur_thresh) * 100))
    else:
        progress_pct = 100

    pet_emoji = pet_info.get('emoji','🥚')
    pet_lv    = pet_info.get('level',0)
    has_pet   = pet_info.get('has_pet', False)
    pet_name  = pet_info.get('name','없음')

    asset_total = sum(v for v in assets.values() if v > 0) or 1
    cash_pct    = int(assets.get('현금',0)/asset_total*100)
    stock_pct   = int(assets.get('주식',0)/asset_total*100)
    coin_pct    = int(assets.get('코인',0)/asset_total*100)
    estate_pct  = int(assets.get('부동산',0)/asset_total*100)
    weapon_pct  = int(assets.get('명검',0)/asset_total*100)

    frame_border = {
        'none':    p,
        'silver':  '#B8C0CC',
        'gold':    '#FFD600',
        'diamond': '#00E5FF',
        'legend':  '#AA00FF',
        'dragon':  '#FF6B00',
    }.get(frame_id, p)

    is_rainbow = theme_id == 'rainbow'
    nw_raw = int(nw)

    # Build conic gradient for asset donut
    segs = []
    acc = 0
    colors_seg = [('#FFD600',cash_pct),('#00FF88',stock_pct),('#FF9500',coin_pct),('#00E5FF',estate_pct),('#FF00FF',weapon_pct)]
    for col, pct in colors_seg:
        if pct > 0:
            segs.append(f"{col} {acc}% {acc+pct}%")
            acc += pct
    if acc < 100:
        segs.append(f"rgba(255,255,255,0.06) {acc}% 100%")
    donut_css = "conic-gradient(" + ",".join(segs) + ")" if segs else "rgba(255,255,255,0.05)"

    # Build badge JSON for JS
    import json
    badges_json = json.dumps([
        {"icon": b["icon"], "name": b["name"], "earned": b["id"] in earned_badges}
        for b in PROFILE_BADGES[:16]
    ])

    status_escaped = (status_msg or '').replace('"', "'").replace('\\', '')

    rainbow_ring_css  = "animation:rainbowRing 3s linear infinite;" if is_rainbow else f"box-shadow:0 0 24px {frame_border}44;"
    rainbow_nw_css    = "background:linear-gradient(90deg,#ff00ff,#00ffff,#ff00ff);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rainbowTxt 3s linear infinite;" if is_rainbow else f"color:{p};"
    rainbow_fill_css  = "animation:rainbowFill 3s linear infinite;" if is_rainbow else ""
    is_rainbow_js     = "true" if is_rainbow else "false"

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;font-family:'Segoe UI',system-ui,sans-serif;overflow:hidden;}}
#card{{width:100%;height:520px;position:relative;overflow:hidden;background:{bg};border:2px solid {frame_border};border-radius:24px;}}
#wave-canvas{{position:absolute;inset:0;width:100%;height:100%;z-index:0;}}
#shimmer{{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(105deg,transparent 40%,{p}18 50%,transparent 60%);background-size:200% 100%;animation:shimmerMove 4s ease-in-out infinite;}}
#grid-overlay{{position:absolute;inset:0;z-index:1;pointer-events:none;background-image:linear-gradient({p}12 1px,transparent 1px),linear-gradient(90deg,{p}12 1px,transparent 1px);background-size:40px 40px;}}
.cm{{position:absolute;width:18px;height:18px;border-color:{frame_border};border-style:solid;opacity:0.7;z-index:10;}}
.cm-tl{{top:10px;left:10px;border-width:2px 0 0 2px;}}.cm-tr{{top:10px;right:10px;border-width:2px 2px 0 0;}}
.cm-bl{{bottom:10px;left:10px;border-width:0 0 2px 2px;}}.cm-br{{bottom:10px;right:10px;border-width:0 2px 2px 0;}}
#content{{position:absolute;inset:0;z-index:5;display:flex;flex-direction:column;padding:18px 22px 14px;}}
#topbar{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;}}
#online-dot{{width:8px;height:8px;border-radius:50%;background:#00FF88;box-shadow:0 0 8px #00FF88;animation:blink 2s ease-in-out infinite;margin-right:6px;flex-shrink:0;}}
#topbar-left{{display:flex;align-items:center;gap:6px;}}
#uid-tag{{color:{p};font-size:0.7rem;font-weight:700;letter-spacing:2px;opacity:0.8;}}
#topbar-right{{display:flex;gap:8px;align-items:center;}}
.top-chip{{padding:3px 10px;border-radius:20px;font-size:0.62rem;font-weight:700;background:rgba(255,255,255,0.05);border:1px solid {frame_border}55;color:{frame_border};letter-spacing:0.5px;}}
#hero{{display:flex;gap:16px;align-items:flex-start;margin-bottom:12px;}}
#av-zone{{flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:5px;}}
#av-ring{{width:90px;height:90px;border-radius:50%;cursor:pointer;border:3px solid {frame_border};background:rgba(0,0,0,0.45);display:flex;align-items:center;justify-content:center;position:relative;{rainbow_ring_css}transition:transform 0.15s;}}
#av-ring:hover{{transform:scale(1.06);}}
#av-emoji{{font-size:44px;line-height:1;animation:float 4s ease-in-out infinite;}}
#av-lv{{position:absolute;bottom:-8px;right:-8px;width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,{p},{s});border:2px solid rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;color:#000;font-size:10px;font-weight:900;}}
#av-name{{color:#fff;font-size:0.95rem;font-weight:900;text-align:center;letter-spacing:0.5px;text-shadow:0 0 14px {p};}}
#av-title{{color:{p};font-size:0.6rem;font-weight:700;letter-spacing:1.5px;text-align:center;}}
#info-zone{{flex:1;min-width:0;}}
#nw-label{{color:#64748B;font-size:0.65rem;letter-spacing:1.5px;margin-bottom:2px;}}
#nw-counter{{{rainbow_nw_css}font-size:1.75rem;font-weight:900;line-height:1;cursor:pointer;transition:transform 0.1s;font-variant-numeric:tabular-nums;}}
#nw-counter:hover{{transform:scale(1.03);}}
#nw-sub{{color:#475569;font-size:0.65rem;margin-top:2px;margin-bottom:8px;}}
#status-wrap{{background:rgba(255,255,255,0.03);border-left:2px solid {p};padding:5px 10px;border-radius:0 8px 8px 0;margin-bottom:8px;}}
#status-txt{{color:#94A3B8;font-size:0.75rem;font-style:italic;}}
#cursor{{display:inline-block;width:2px;height:11px;background:{p};margin-left:2px;animation:cursorBlink 0.8s steps(1) infinite;vertical-align:middle;}}
#prog-row{{display:flex;align-items:center;gap:8px;}}
#prog-right{{flex:1;}}
#prog-labels{{display:flex;justify-content:space-between;color:#475569;font-size:0.62rem;margin-bottom:3px;}}
#prog-track{{height:6px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;}}
#prog-fill{{height:100%;border-radius:3px;width:0%;background:linear-gradient(90deg,{p},{s});{rainbow_fill_css}box-shadow:0 0 8px {p}66;transition:width 1.2s cubic-bezier(0.34,1.56,0.64,1);}}
#stats-row{{display:flex;gap:7px;margin-bottom:0;}}
.scard{{flex:1;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:7px 9px;transition:border-color 0.2s,background 0.2s;cursor:default;}}
.scard:hover{{border-color:{p}44;background:rgba(255,255,255,0.06);}}
.scard-icon{{font-size:1.1rem;margin-bottom:2px;}}
.scard-val{{color:#E2E8F0;font-size:0.75rem;font-weight:900;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.scard-lbl{{color:#475569;font-size:0.57rem;letter-spacing:0.5px;margin-top:1px;}}
.hdiv{{height:1px;background:linear-gradient(90deg,transparent,{p}33,transparent);margin:10px 0;}}
#bottom{{display:flex;gap:12px;align-items:flex-start;}}
#donut-zone{{flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:5px;}}
#donut-ring{{width:76px;height:76px;border-radius:50%;background:{donut_css};display:flex;align-items:center;justify-content:center;cursor:pointer;transition:transform 0.2s;}}
#donut-ring:hover{{transform:scale(1.06) rotate(5deg);}}
#donut-inner{{width:52px;height:52px;border-radius:50%;background:{bg};display:flex;flex-direction:column;align-items:center;justify-content:center;}}
#donut-pct{{color:{p};font-size:0.68rem;font-weight:900;transition:color 0.3s;}}
#donut-lbl{{color:#475569;font-size:0.52rem;}}
#asset-legend{{display:flex;flex-direction:column;gap:2px;}}
.aleg{{display:flex;align-items:center;gap:4px;font-size:0.56rem;color:#64748B;}}
.aleg-dot{{width:6px;height:6px;border-radius:50%;flex-shrink:0;}}
#pet-zone{{flex-shrink:0;display:flex;flex-direction:column;align-items:center;gap:3px;}}
#pet-bubble{{background:rgba(255,255,255,0.04);border:1px solid {p}33;border-radius:14px;padding:6px 10px;text-align:center;cursor:pointer;transition:all 0.2s;min-width:60px;}}
#pet-bubble:hover{{background:rgba(255,255,255,0.08);transform:translateY(-2px);}}
#pet-sprite{{font-size:1.7rem;animation:petBob 2.5s ease-in-out infinite;}}
#pet-info-txt{{color:#94A3B8;font-size:0.58rem;margin-top:2px;}}
#badge-zone{{flex:1;}}
#badge-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;}}
#badge-title{{color:#94A3B8;font-size:0.62rem;letter-spacing:1px;}}
#badge-count-txt{{color:{p};font-size:0.62rem;font-weight:700;}}
#badge-strip{{display:flex;flex-wrap:wrap;gap:3px;}}
.bdot{{width:22px;height:22px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:0.8rem;cursor:default;transition:transform 0.15s;}}
.bdot:hover{{transform:scale(1.28);}}
.bdot.earned{{background:rgba(255,214,0,0.12);border:1px solid #FFD60044;}}
.bdot.locked{{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);filter:grayscale(1);opacity:0.28;}}
#efx{{position:absolute;inset:0;pointer-events:none;z-index:20;}}
.ptcl{{position:absolute;pointer-events:none;font-size:12px;animation:ptclRise linear forwards;opacity:0;}}
#scanline{{position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,{p}55,transparent);pointer-events:none;z-index:15;animation:scan 6s linear infinite;}}
@keyframes shimmerMove{{0%{{background-position:-100% 0;}}50%{{background-position:200% 0;}}100%{{background-position:200% 0;}}}}
@keyframes float{{0%,100%{{transform:translateY(0);}}50%{{transform:translateY(-8px);}}}}
@keyframes petBob{{0%,100%{{transform:translateY(0) rotate(-3deg);}}50%{{transform:translateY(-5px) rotate(3deg);}}}}
@keyframes blink{{0%,100%{{opacity:1;}}50%{{opacity:0.3;}}}}
@keyframes cursorBlink{{0%,49%{{opacity:1;}}50%,100%{{opacity:0;}}}}
@keyframes rainbowRing{{0%{{border-color:#ff00ff;box-shadow:0 0 24px #ff00ff44;}}25%{{border-color:#ffff00;box-shadow:0 0 24px #ffff0044;}}50%{{border-color:#00ffff;box-shadow:0 0 24px #00ffff44;}}75%{{border-color:#00ff88;box-shadow:0 0 24px #00ff8844;}}100%{{border-color:#ff00ff;box-shadow:0 0 24px #ff00ff44;}}}}
@keyframes rainbowTxt{{0%{{background-position:0%;}}100%{{background-position:200%;}}}}
@keyframes rainbowFill{{0%{{background:linear-gradient(90deg,#ff00ff,#ff9900);}}50%{{background:linear-gradient(90deg,#00e5ff,#aa00ff);}}100%{{background:linear-gradient(90deg,#ff00ff,#ff9900);}}}}
@keyframes ptclRise{{0%{{opacity:0;transform:translateY(0) scale(0.5);}}10%{{opacity:0.7;}}90%{{opacity:0.1;}}100%{{opacity:0;transform:translateY(-220px) translateX(var(--dx)) scale(1.2);}}}}
@keyframes scan{{0%{{top:-2px;}}100%{{top:102%;}}}}
@keyframes popIn{{0%{{transform:scale(0) rotate(-15deg);opacity:0;}}70%{{transform:scale(1.15) rotate(5deg);}}100%{{transform:scale(1) rotate(0deg);opacity:1;}}}}
</style>
</head><body>
<div id="card">
<canvas id="wave-canvas"></canvas>
<div id="grid-overlay"></div>
<div id="shimmer"></div>
<div id="scanline"></div>
<div class="cm cm-tl"></div><div class="cm cm-tr"></div>
<div class="cm cm-bl"></div><div class="cm cm-br"></div>
<div id="efx"></div>
<div id="content">
  <div id="topbar">
    <div id="topbar-left"><div id="online-dot"></div><span id="uid-tag">@{uid}</span></div>
    <div id="topbar-right">
      <span class="top-chip">{frame['icon']} {frame['name']}</span>
      <span class="top-chip" id="time-chip">--:--</span>
    </div>
  </div>
  <div id="hero">
    <div id="av-zone">
      <div id="av-ring" onclick="avatarClick(event)">
        <div id="av-emoji">{avatar}</div>
        <div id="av-lv">{lv}</div>
      </div>
      <div id="av-name">{uid}</div>
      <div id="av-title">✦ {custom_title} ✦</div>
    </div>
    <div id="info-zone">
      <div id="nw-label">💰 TOTAL NET WORTH</div>
      <div id="nw-counter" onclick="nwClick(event)">₩0</div>
      <div id="nw-sub">{lv_title} &nbsp;·&nbsp; 📅 {join_date}</div>
      <div id="status-wrap"><span id="status-txt"></span><span id="cursor"></span></div>
      <div id="prog-row">
        <span style="font-size:1rem;flex-shrink:0;">📈</span>
        <div id="prog-right">
          <div id="prog-labels"><span>다음 레벨까지</span><span id="prog-pct-txt">0%</span></div>
          <div id="prog-track"><div id="prog-fill"></div></div>
        </div>
      </div>
    </div>
  </div>
  <div id="stats-row">
    <div class="scard"><div class="scard-icon">🏅</div><div class="scard-val">{badge_count}<span style="color:#475569;font-size:0.6rem;">/{total_badges}</span></div><div class="scard-lbl">배지</div></div>
    <div class="scard"><div class="scard-icon">💵</div><div class="scard-val">{format_korean_money(assets.get('현금',0))}</div><div class="scard-lbl">현금</div></div>
    <div class="scard"><div class="scard-icon">📈</div><div class="scard-val">{format_korean_money(assets.get('주식',0))}</div><div class="scard-lbl">주식</div></div>
    <div class="scard"><div class="scard-icon">🪙</div><div class="scard-val">{format_korean_money(assets.get('코인',0))}</div><div class="scard-lbl">코인</div></div>
    <div class="scard"><div class="scard-icon">🏢</div><div class="scard-val">{format_korean_money(assets.get('부동산',0))}</div><div class="scard-lbl">부동산</div></div>
  </div>
  <div class="hdiv"></div>
  <div id="bottom">
    <div id="donut-zone">
      <div id="donut-ring" onclick="donutClick()" title="자산 구성">
        <div id="donut-inner">
          <div id="donut-pct" style="color:#FFD600;">{cash_pct}%</div>
          <div id="donut-lbl">현금</div>
        </div>
      </div>
      <div id="asset-legend">
        <div class="aleg"><div class="aleg-dot" style="background:#FFD600;"></div>현금 {cash_pct}%</div>
        <div class="aleg"><div class="aleg-dot" style="background:#00FF88;"></div>주식 {stock_pct}%</div>
        <div class="aleg"><div class="aleg-dot" style="background:#FF9500;"></div>코인 {coin_pct}%</div>
      </div>
    </div>
    <div id="pet-zone">
      <div id="pet-bubble" onclick="petClick()">
        <div id="pet-sprite">{"🥚" if not has_pet else pet_emoji}</div>
        <div id="pet-info-txt">{"없음" if not has_pet else f"{pet_name} Lv.{pet_lv}"}</div>
      </div>
      <div style="color:#475569;font-size:0.58rem;text-align:center;">🐾 파트너</div>
    </div>
    <div id="badge-zone">
      <div id="badge-header">
        <span id="badge-title">🏅 BADGES</span>
        <span id="badge-count-txt">{badge_count}/{total_badges} 달성</span>
      </div>
      <div id="badge-strip"></div>
    </div>
  </div>
</div>
</div>
<script>
const P="{p}",S="{s}",BG="{bg}";
const IS_RAINBOW={is_rainbow_js};
const NW_RAW={nw_raw};
const PROGRESS={progress_pct};
const STATUS_MSG="{status_escaped}";
const BADGES_DATA={badges_json};
const DONUT_SEGS=[
  {{pct:{cash_pct},label:"현금",color:"#FFD600"}},
  {{pct:{stock_pct},label:"주식",color:"#00FF88"}},
  {{pct:{coin_pct},label:"코인",color:"#FF9500"}},
  {{pct:{estate_pct},label:"부동산",color:"#00E5FF"}},
  {{pct:{weapon_pct},label:"명검",color:"#FF00FF"}}
].filter(d=>d.pct>0);

// Time chip
function updClock(){{const n=new Date(),h=String(n.getHours()).padStart(2,'0'),m=String(n.getMinutes()).padStart(2,'0');document.getElementById('time-chip').textContent=h+':'+m;}}
updClock();setInterval(updClock,10000);

// Wave BG
const cv=document.getElementById('wave-canvas');
const cx=cv.getContext('2d');
cv.width=800;cv.height=520;
let wt=0;
function drawWave(){{
  cx.clearRect(0,0,800,520);
  [[120,80,180,P+'22'],[700,410,160,S+'1A'],[400,260,130,P+'0E']].forEach(([ox,oy,or,oc])=>{{
    const g=cx.createRadialGradient(ox,oy,0,ox,oy,or);
    g.addColorStop(0,oc);g.addColorStop(1,'transparent');
    cx.fillStyle=g;cx.beginPath();cx.arc(ox,oy,or,0,Math.PI*2);cx.fill();
  }});
  [0,1,2].forEach(i=>{{
    cx.beginPath();cx.strokeStyle=P+(i===1?'30':'18');cx.lineWidth=1;
    for(let x=0;x<=800;x+=3){{const y=260+(Math.sin((x/120)+wt+i*1.2)*28)+(Math.sin((x/60)+wt*1.5)*10);x===0?cx.moveTo(x,y):cx.lineTo(x,y);}}
    cx.stroke();
  }});
  wt+=0.018;requestAnimationFrame(drawWave);
}}
drawWave();

// Count-up NW
const NWE=document.getElementById('nw-counter');
const FU=[[1e15,'경'],[1e12,'조'],[1e8,'억'],[1e4,'만']];
function fmtKr(n){{if(n<=0)return '₩0';let r='';for(const[u,l]of FU){{if(n>=u){{r+=Math.floor(n/u).toLocaleString()+l;n%=u;}}}}return '₩'+r;}}
(function(){{const dur=1800,t0=performance.now();function step(now){{const t=Math.min((now-t0)/dur,1),e=1-Math.pow(1-t,4);NWE.textContent=fmtKr(Math.floor(NW_RAW*e));if(t<1)requestAnimationFrame(step);else NWE.textContent=fmtKr(NW_RAW);}}requestAnimationFrame(step);}})();

// Typewriter status
(function(){{const el=document.getElementById('status-txt'),msg=STATUS_MSG||'상태 메시지를 설정해보세요...';let i=0;function type(){{if(i<=msg.length){{el.textContent=msg.slice(0,i++);setTimeout(type,i===1?700:55);}}}}setTimeout(type,1000);}})();

// Progress
setTimeout(()=>{{document.getElementById('prog-fill').style.width=PROGRESS+'%';document.getElementById('prog-pct-txt').textContent=PROGRESS+'%';}},400);

// Badges
(function(){{const s=document.getElementById('badge-strip');BADGES_DATA.forEach((b,idx)=>{{const d=document.createElement('div');d.className='bdot '+(b.earned?'earned':'locked');d.textContent=b.icon;d.title=b.name;if(b.earned){{d.style.opacity='0';d.style.animation='popIn 0.35s ease forwards';d.style.animationDelay=(idx*0.04)+'s';}}s.appendChild(d);}});}})();

// Particles
const EFX=document.getElementById('efx'),CARD=document.getElementById('card');
const PTCLS=IS_RAINBOW?['✨','🌈','💫','⭐','💖']:['✨','💫','⭐','💎'];
function spawnP(){{const p=document.createElement('div');p.className='ptcl';p.textContent=PTCLS[Math.floor(Math.random()*PTCLS.length)];p.style.setProperty('--dx',(Math.random()-0.5)*70+'px');p.style.left=Math.random()*88+'%';p.style.bottom='-10px';p.style.animationDuration=(4+Math.random()*4)+'s';CARD.appendChild(p);setTimeout(()=>p.remove(),9000);}}
setInterval(spawnP,2200);

function burst(ex,ey,arr,n){{for(let i=0;i<n;i++){{const sp=document.createElement('div');sp.style.cssText='position:absolute;font-size:16px;pointer-events:none;z-index:60;';sp.textContent=arr[Math.floor(Math.random()*arr.length)];const r=CARD.getBoundingClientRect();sp.style.left=(ex-r.left)+'px';sp.style.top=(ey-r.top)+'px';EFX.appendChild(sp);const a=(i/n)*Math.PI*2,d=40+Math.random()*40;sp.animate([{{opacity:1,transform:'translate(0,0) scale(0.4)'}},{{opacity:0,transform:`translate(${{Math.cos(a)*d}}px,${{Math.sin(a)*d}}px) scale(1.3)`}}],{{duration:600+Math.random()*300,easing:'ease-out'}}).onfinish=()=>sp.remove();}}}}

function confetti(ex,ey){{const cols=[P,S,'#FFD600','#FF4B4B','#00FF88'];for(let i=0;i<22;i++){{const d=document.createElement('div');const sz=6+Math.random()*7;d.style.cssText=`position:absolute;width:${{sz}}px;height:${{sz}}px;border-radius:${{Math.random()>.5?'50%':'2px'}};background:${{cols[i%cols.length]}};pointer-events:none;z-index:60;left:${{ex-CARD.getBoundingClientRect().left}}px;top:${{ey-CARD.getBoundingClientRect().top}}px;`;EFX.appendChild(d);const dx=(Math.random()-.5)*150,dy=-60-Math.random()*100,rt=Math.random()*720;d.animate([{{opacity:1,transform:'translate(0,0) rotate(0deg)'}},{{opacity:0,transform:`translate(${{dx}}px,${{dy}}px) rotate(${{rt}}deg)`}}],{{duration:900+Math.random()*400,easing:'cubic-bezier(0.1,0.8,0.3,1)'}}).onfinish=()=>d.remove();}}}}

function avatarClick(e){{const av=document.getElementById('av-ring');av.style.transform='scale(0.88)';setTimeout(()=>av.style.transform='',180);burst(e.clientX,e.clientY,['✨','⭐','💫','💎','🌟'],10);}}
function nwClick(e){{confetti(e.clientX,e.clientY);NWE.style.transform='scale(1.12)';setTimeout(()=>NWE.style.transform='',180);}}

let donutIdx=0;
function donutClick(){{if(!DONUT_SEGS.length)return;donutIdx=(donutIdx+1)%DONUT_SEGS.length;const seg=DONUT_SEGS[donutIdx];const pe=document.getElementById('donut-pct');pe.style.color=seg.color;pe.textContent=seg.pct+'%';document.getElementById('donut-lbl').textContent=seg.label;}}

function petClick(){{const pb=document.getElementById('pet-bubble');pb.style.transform='translateY(-6px) scale(1.1)';setTimeout(()=>pb.style.transform='',280);burst(pb.getBoundingClientRect().x+35,pb.getBoundingClientRect().y+30,['🐾','💖','✨'],6);}}
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 🏠 MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render(market, nw):
    st.markdown("""
    <style>
    .prof-section-header{
      font-size:1.2rem;font-weight:900;color:#E2E8F0;
      margin:20px 0 12px;padding-bottom:8px;
      border-bottom:1px solid rgba(255,255,255,0.07);
    }
    .prof-card{
      background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
      border-radius:14px;padding:16px;margin-bottom:10px;
      transition:border-color 0.2s;
    }
    .prof-card:hover{border-color:rgba(0,229,255,0.25);}
    .chip{
      display:inline-block;padding:3px 10px;border-radius:8px;
      font-size:0.73rem;font-weight:700;margin:2px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("👤 내 프로필")

    uid   = st.session_state.logged_in_user
    users = load_db(USERS_FILE, {})
    u     = users.get(uid, {})

    lv, lv_title  = get_level_from_nw(nw)
    avatar        = u.get('avatar', '🧑‍🚀')
    custom_title  = st.session_state.get('equipped_title', '투자자')
    status_msg    = u.get('status_msg', '')
    join_date     = u.get('join_date', '알 수 없음')
    unlocked_av   = set(u.get('unlocked_avatars', ['🧑‍🚀']))
    theme_id      = u.get('profile_theme', 'cyan')
    frame_id      = u.get('profile_frame', 'none')

    # Asset data
    assets     = get_asset_breakdown(u, market, nw)
    earned_badges = compute_badges(uid, users, market, nw)
    badge_count   = len(earned_badges)

    # Pet info
    pet_data = u.get('pet', {})
    has_pet  = bool(pet_data.get('species'))
    pet_lv   = pet_data.get('level', 0)
    if has_pet:
        from pages.pet import PET_SPECIES, get_pet_sprite
        sp_id  = pet_data.get('species','cat')
        sp_inf = PET_SPECIES.get(sp_id, {})
        pet_info = {
            'has_pet': True,
            'emoji':   get_pet_sprite(sp_id, pet_lv),
            'name':    pet_data.get('name','?'),
            'level':   pet_lv,
        }
    else:
        pet_info = {'has_pet':False,'emoji':'🥚','name':'없음','level':0}

    # ── Animated Profile Card
    components.html(
        generate_profile_card_html(
            uid, avatar, lv, lv_title, nw, custom_title,
            status_msg, join_date, theme_id, frame_id,
            badge_count, len(PROFILE_BADGES), pet_info, assets
        ),
        height=540,
        scrolling=False
    )

    st.write("")

    # ══════════════════════════════════════════════════════════════════════════
    # MAIN TABS
    # ══════════════════════════════════════════════════════════════════════════
    main_tabs = st.tabs(["📊 자산 현황","🏅 배지","🎮 게임 기록","📈 성장 로드맵","🎨 꾸미기","🔧 설정"])

    # ── TAB 1: 자산 현황
    with main_tabs[0]:
        st.markdown('<div class="prof-section-header">📊 자산 포트폴리오</div>', unsafe_allow_html=True)

        cash = st.session_state.global_cash
        loan = st.session_state.loan
        real_estate_val = sum(
            estate_config[eid]['base_price'] * cnt * 0.8
            for eid, cnt in st.session_state.get('real_estate', {}).items()
            if eid in estate_config
        )
        stock_data = market.get('stock_data', {})
        stock_val  = sum(
            u.get('portfolio',{}).get(s['id'],{}).get('qty',0) * stock_data.get(s['id'],{}).get('price',0)
            for s in stock_config
        )
        crypto_data = market.get('crypto_data', {})
        coin_val    = sum(
            ci.get('qty',0) * crypto_data.get(cid,{}).get('price',0)
            for cid, ci in u.get('crypto_portfolio',{}).items()
        )
        w_lv = u.get('weapon_level', 0)
        weapon_val = FORGE_DATA[w_lv]['sell'] if w_lv > 0 and w_lv in FORGE_DATA else 0

        asset_items = [
            ("💵","보유 현금",     cash,            "#FFD600",  "유동성 자산"),
            ("📈","주식 평가액",   int(stock_val),  "#00FF88",  "포트폴리오"),
            ("🪙","코인 평가액",   int(coin_val),   "#FF9500",  "디지털 자산"),
            ("🏢","부동산 평가",   int(real_estate_val),"#00E5FF","고정 자산"),
            ("⚔️","명검 가치",     weapon_val,      "#FF00FF",  "희귀 아이템"),
            ("💳","대출금",        loan,            "#FF4B4B",  "부채"),
            ("📊","총 순자산",     nw,              "#FFFFFF",  "Net Worth"),
        ]

        asset_cols = st.columns(4)
        for i, (icon, label, val, color, sub) in enumerate(asset_items):
            with asset_cols[i % 4]:
                is_debt = label == "대출금"
                st.markdown(f"""
                <div class='prof-card' style='text-align:center;border-color:{color}22;'>
                    <div style='font-size:1.8rem;margin-bottom:6px;'>{icon}</div>
                    <div style='color:#64748B;font-size:0.72rem;letter-spacing:1px;'>{label}</div>
                    <div style='color:{color};font-weight:900;font-size:0.95rem;margin-top:4px;'>
                        {"▼ " if is_debt else ""}{format_korean_money(val)}
                    </div>
                    <div style='color:#475569;font-size:0.68rem;margin-top:4px;'>{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="prof-section-header">🏠 부동산 보유 현황</div>', unsafe_allow_html=True)
        re_data = st.session_state.get('real_estate', {})
        re_cols = st.columns(4)
        has_any_estate = False
        for i, (eid, ec) in enumerate(estate_config.items()):
            cnt = re_data.get(eid, 0)
            if cnt > 0:
                has_any_estate = True
                val_ = int(ec['base_price'] * cnt * 0.8)
                with re_cols[i % 4]:
                    st.markdown(f"""
                    <div class='prof-card' style='text-align:center;'>
                        <div style='font-size:2rem;'>{ec.get("icon","🏢")}</div>
                        <div style='color:#E2E8F0;font-weight:700;margin-top:6px;font-size:0.88rem;'>{ec.get("name",eid)}</div>
                        <div style='color:#FFD600;font-weight:900;margin-top:4px;'>{cnt}채</div>
                        <div style='color:#64748B;font-size:0.75rem;margin-top:2px;'>{format_korean_money(val_)}</div>
                    </div>
                    """, unsafe_allow_html=True)
        if not has_any_estate:
            st.markdown("<div style='color:#475569;font-size:0.9rem;padding:20px;text-align:center;'>보유 부동산이 없습니다.</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown('<div class="prof-section-header">📈 주식 포트폴리오 상세</div>', unsafe_allow_html=True)
        portfolio = u.get('portfolio', {})
        has_stocks = any(v.get('qty',0) > 0 for v in portfolio.values())
        if has_stocks:
            st.markdown("""
            <div style='display:flex;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:10px;padding:10px 14px;margin-bottom:8px;'>
                <div style='flex:2;color:#64748B;font-size:0.78rem;'>종목</div>
                <div style='flex:1;color:#64748B;font-size:0.78rem;text-align:right;'>보유수량</div>
                <div style='flex:1;color:#64748B;font-size:0.78rem;text-align:right;'>평가금액</div>
                <div style='flex:1;color:#64748B;font-size:0.78rem;text-align:right;'>평균매입가</div>
                <div style='flex:1;color:#64748B;font-size:0.78rem;text-align:right;'>손익</div>
            </div>
            """, unsafe_allow_html=True)
            for s in stock_config:
                pos = portfolio.get(s['id'],{})
                qty = pos.get('qty',0)
                if qty <= 0: continue
                cur_price = stock_data.get(s['id'],{}).get('price',0)
                avg_price = pos.get('avg_price',cur_price)
                total_val = qty * cur_price
                pnl       = (cur_price - avg_price) * qty
                pnl_pct   = ((cur_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
                pnl_color = "#00FF88" if pnl >= 0 else "#FF4B4B"
                pnl_sign  = "+" if pnl >= 0 else ""
                st.markdown(f"""
                <div style='display:flex;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.04);align-items:center;'>
                    <div style='flex:2;'>
                        <span style='color:#E2E8F0;font-weight:700;'>{s.get("name",s["id"])}</span>
                    </div>
                    <div style='flex:1;text-align:right;color:#94A3B8;'>{qty:,}주</div>
                    <div style='flex:1;text-align:right;color:#FFD600;font-weight:700;'>{format_korean_money(total_val)}</div>
                    <div style='flex:1;text-align:right;color:#64748B;'>{format_korean_money(avg_price)}</div>
                    <div style='flex:1;text-align:right;color:{pnl_color};font-weight:700;'>
                        {pnl_sign}{format_korean_money(int(pnl))} ({pnl_sign}{pnl_pct:.1f}%)
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#475569;font-size:0.9rem;padding:20px;text-align:center;'>보유 주식이 없습니다.</div>", unsafe_allow_html=True)

    # ── TAB 2: 배지
    with main_tabs[1]:
        st.markdown('<div class="prof-section-header">🏅 배지 컬렉션</div>', unsafe_allow_html=True)
        earned_count = len(earned_badges)
        total_count  = len(PROFILE_BADGES)
        pct = int(earned_count/total_count*100)
        st.markdown(f"""
        <div style='background:rgba(255,214,0,0.05);border:1px solid #FFD60033;
                    border-radius:14px;padding:16px;margin-bottom:18px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                <div style='color:#FFD600;font-size:1.4rem;font-weight:900;'>{earned_count}/{total_count} 배지 달성</div>
                <div style='color:#94A3B8;font-size:0.85rem;'>{pct}% 완료</div>
            </div>
            <div style='background:rgba(255,255,255,0.07);border-radius:4px;height:7px;overflow:hidden;'>
                <div style='background:linear-gradient(90deg,#FFD600,#FF9500);width:{pct}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        badge_cols = st.columns(5)
        for i, b in enumerate(PROFILE_BADGES):
            has = b['id'] in earned_badges
            with badge_cols[i%5]:
                st.markdown(f"""
                <div class='prof-card' style='text-align:center;
                    {"border-color:#FFD600;background:rgba(255,214,0,0.06);" if has else "opacity:0.38;"}'>
                    <div style='font-size:2rem;'>{b['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;font-size:0.8rem;margin-top:6px;'>{b['name']}</div>
                    <div style='color:#64748B;font-size:0.68rem;margin-top:3px;'>{b['desc']}</div>
                    <div style='color:{"#FFD600" if has else "#475569"};font-size:0.68rem;margin-top:5px;font-weight:700;'>
                        {"✅ 달성" if has else "🔒 미달성"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 3: 게임 기록
    with main_tabs[2]:
        st.markdown('<div class="prof-section-header">🎮 게임 기록</div>', unsafe_allow_html=True)
        gr = u.get('game_records', {})
        dungeon = u.get('dungeon_stats', {})
        marble  = u.get('marble_stats', {})
        pet_d   = u.get('pet', {})

        game_records = [
            ("🏎️","네온 레이싱",   f"{gr.get('racing',{}).get('score',0):,}점",      f"거리: {gr.get('racing',{}).get('dist',0):.1f}km"),
            ("🧟","좀비 서바이벌", f"Wave {gr.get('zombie',{}).get('wave',0)}",       f"킬: {gr.get('zombie',{}).get('kills',0):,}"),
            ("🥊","격투 챔피언",   f"{gr.get('fighter',{}).get('score',0):,}점",      f"퍼펙트: {gr.get('fighter',{}).get('perfects',0)}"),
            ("🎯","저격 마스터",   f"{gr.get('sniper',{}).get('score',0):,}점",       f"킬: {gr.get('sniper',{}).get('kills',0):,}"),
            ("🌍","인베스트 마블", format_korean_money(marble.get('best_net_worth',0)),f"승: {marble.get('wins',0)} / {marble.get('games_played',0)}판"),
            ("⚔️","던전 클리어",   f"{dungeon.get('clears',0)}회",                    f"킬: {dungeon.get('best_kills',0):,}"),
            ("🐾","펫 배틀 전적",  f"{pet_d.get('battles_won',0)}승",                 f"총 {pet_d.get('battles_total',0)}전"),
            ("🗺️","펫 탐험",       f"{pet_d.get('expeditions',0)}회",                 f"Lv.{pet_d.get('level',0)} 도달"),
        ]

        gr_cols = st.columns(4)
        for i, (icon, title, main, sub) in enumerate(game_records):
            with gr_cols[i%4]:
                st.markdown(f"""
                <div class='prof-card'>
                    <div style='display:flex;align-items:center;gap:10px;margin-bottom:8px;'>
                        <div style='font-size:1.6rem;'>{icon}</div>
                        <div style='color:#94A3B8;font-size:0.78rem;'>{title}</div>
                    </div>
                    <div style='color:#FFD600;font-size:1.05rem;font-weight:900;'>{main}</div>
                    <div style='color:#475569;font-size:0.75rem;margin-top:3px;'>{sub}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 4: 성장 로드맵
    with main_tabs[3]:
        st.markdown('<div class="prof-section-header">📈 성장 로드맵</div>', unsafe_allow_html=True)
        next_lv_m, next_icon, next_name, next_req = get_next_milestone(nw)
        if next_req and nw < next_req:
            remain = next_req - nw
            cur_thresh = next((req for lv_m,_,_,req in MILESTONES if nw >= req), 0)
            if next_req > cur_thresh:
                pct_ = min(100, int((nw-cur_thresh)/(next_req-cur_thresh)*100))
            else: pct_ = 100
            st.markdown(f"""
            <div style='background:rgba(0,229,255,0.05);border:1px solid #00E5FF33;
                        border-radius:14px;padding:18px;margin-bottom:18px;'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                    <div>
                        <div style='color:#00E5FF;font-weight:900;font-size:1rem;'>
                            {next_icon} 다음 목표: {next_name}
                        </div>
                        <div style='color:#64748B;font-size:0.82rem;margin-top:4px;'>
                            남은 금액: <span style='color:#FFD600;font-weight:700;'>{format_korean_money(remain)}</span>
                        </div>
                    </div>
                    <div style='color:#FFD600;font-size:1.4rem;font-weight:900;'>{pct_}%</div>
                </div>
                <div style='background:rgba(255,255,255,0.07);border-radius:4px;height:8px;overflow:hidden;'>
                    <div style='background:linear-gradient(90deg,#00E5FF,#00FF88);width:{pct_}%;height:100%;border-radius:4px;
                                box-shadow:0 0 10px #00E5FF66;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        ml_cols = st.columns(7)
        for i, (lv_m, icon, name, req) in enumerate(MILESTONES):
            achieved = nw >= req
            is_current = (lv == lv_m)
            with ml_cols[i%7]:
                st.markdown(f"""
                <div style='text-align:center;padding:10px 4px;border-radius:12px;
                    background:{"rgba(0,229,255,0.12)" if achieved else "rgba(255,255,255,0.02)"};
                    border:1px solid {"#FFD600" if is_current else "#00E5FF" if achieved else "#1E293B"};
                    opacity:{"1" if achieved else "0.4"};margin-bottom:6px;'>
                    <div style='font-size:1.6rem;'>{icon}</div>
                    <div style='color:#FFD600;font-size:0.78rem;font-weight:900;margin-top:4px;'>Lv.{lv_m}</div>
                    <div style='color:#94A3B8;font-size:0.62rem;margin-top:2px;'>{name}</div>
                    <div style='color:#64748B;font-size:0.6rem;margin-top:4px;'>{format_korean_money(req)}</div>
                    {"<div style='color:#FFD600;font-size:0.65rem;margin-top:3px;font-weight:700;'>★ 현재</div>" if is_current else ""}
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 5: 꾸미기
    with main_tabs[4]:
        cust_tabs = st.tabs(["🖼️ 아바타","🎨 테마","🔲 프레임","💬 상태 메시지"])

        # ── Avatar
        with cust_tabs[0]:
            st.markdown('<div class="prof-section-header">🖼️ 아바타 선택</div>', unsafe_allow_html=True)
            st.markdown("<div style='color:#94A3B8;font-size:0.85rem;margin-bottom:16px;'>기본 제공 외 아바타는 30억원에 해금 가능합니다.</div>", unsafe_allow_html=True)
            av_cols = st.columns(6)
            for i, (em, name) in enumerate(AVATARS):
                unlocked = em in unlocked_av or i == 0
                is_cur   = (em == avatar)
                with av_cols[i%6]:
                    bc = "#FFD600" if is_cur else "#00E5FF" if unlocked else "#1E293B"
                    st.markdown(f"""
                    <div style='background:{"rgba(255,214,0,0.1)" if is_cur else "rgba(255,255,255,0.03)"};
                                border:2px solid {bc};border-radius:12px;
                                padding:12px 6px;text-align:center;margin-bottom:6px;'>
                        <div style='font-size:2.2rem;'>{em}</div>
                        <div style='font-size:0.65rem;color:#94A3B8;margin-top:4px;'>
                            {name}{"" if unlocked else " 🔒"}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if not is_cur:
                        if unlocked:
                            if st.button("선택", key=f"av_{i}", use_container_width=True):
                                users[uid]['avatar'] = em
                                save_db(USERS_FILE, users)
                                st.toast(f"{em} 아바타 변경!", icon="✅")
                                st.rerun()
                        else:
                            if st.button("해금 30억", key=f"av_ul_{i}", use_container_width=True):
                                if st.session_state.global_cash < AVATAR_UNLOCK_PRICE:
                                    st.error("현금 부족!")
                                else:
                                    st.session_state.global_cash -= AVATAR_UNLOCK_PRICE
                                    unlocked_av.add(em)
                                    users[uid]['unlocked_avatars'] = list(unlocked_av)
                                    users[uid]['avatar'] = em
                                    save_db(USERS_FILE, users)
                                    sync_user_data()
                                    st.toast(f"🎉 {em} 해금!", icon="✅")
                                    st.rerun()
                    else:
                        st.markdown("<div style='text-align:center;color:#FFD600;font-size:0.7rem;'>✓ 착용 중</div>", unsafe_allow_html=True)

        # ── Theme
        with cust_tabs[1]:
            st.markdown('<div class="prof-section-header">🎨 프로필 테마</div>', unsafe_allow_html=True)
            th_cols = st.columns(3)
            for i, (th_id, th) in enumerate(PROFILE_THEMES.items()):
                is_cur = (theme_id == th_id)
                with th_cols[i%3]:
                    st.markdown(f"""
                    <div style='background:linear-gradient(135deg,rgba(5,5,20,0.9),rgba(10,10,30,0.9));
                                border:2px solid {"#FFD600" if is_cur else th["primary"]+"44"};
                                border-radius:14px;padding:16px;text-align:center;margin-bottom:8px;'>
                        <div style='width:50px;height:50px;border-radius:50%;margin:0 auto 12px;
                                    background:linear-gradient(135deg,{th["primary"]},{th["secondary"]});
                                    box-shadow:0 0 20px {th["primary"]}88;'></div>
                        <div style='color:#E2E8F0;font-weight:900;'>{th["name"]}</div>
                        <div style='color:{th["primary"]};font-size:0.75rem;margin-top:4px;'>{th["primary"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if is_cur:
                        st.markdown("<div style='text-align:center;color:#FFD600;font-size:0.75rem;margin-bottom:4px;'>✓ 적용 중</div>", unsafe_allow_html=True)
                    else:
                        if st.button(f"적용", key=f"theme_{th_id}", use_container_width=True):
                            users[uid]['profile_theme'] = th_id
                            save_db(USERS_FILE, users)
                            st.toast(f"🎨 {th['name']} 테마 적용!", icon="✅")
                            st.rerun()

        # ── Frame
        with cust_tabs[2]:
            st.markdown('<div class="prof-section-header">🔲 프로필 프레임</div>', unsafe_allow_html=True)
            unlocked_frames = set(u.get('unlocked_frames', ['none']))
            fr_cols = st.columns(3)
            for i, (fr_id, fr) in enumerate(PROFILE_FRAMES.items()):
                is_cur  = (frame_id == fr_id)
                is_unlo = fr_id in unlocked_frames
                with fr_cols[i%3]:
                    st.markdown(f"""
                    <div class='prof-card' style='text-align:center;
                        {"border-color:#FFD600;" if is_cur else ""}'>
                        <div style='font-size:2.5rem;'>{fr["icon"]}</div>
                        <div style='color:#E2E8F0;font-weight:700;margin-top:8px;'>{fr["name"]} 프레임</div>
                        {"<div style='color:#00FF88;font-size:0.75rem;margin-top:4px;'>✅ 적용 중</div>" if is_cur else ""}
                        {"<div style='color:#00E5FF;font-size:0.75rem;margin-top:4px;'>🔓 해금됨</div>" if is_unlo and not is_cur else ""}
                        {f"<div style='color:#FFD600;font-weight:700;margin-top:6px;'>{format_korean_money(fr['price'])}</div>" if fr['price']>0 and not is_unlo else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    if not is_cur:
                        if is_unlo:
                            if st.button("적용", key=f"fr_apply_{fr_id}", use_container_width=True):
                                users[uid]['profile_frame'] = fr_id
                                save_db(USERS_FILE, users)
                                st.toast(f"🔲 {fr['name']} 프레임 적용!", icon="✅")
                                st.rerun()
                        else:
                            if st.button(f"구매 {format_korean_money(fr['price'])}", key=f"fr_buy_{fr_id}", use_container_width=True):
                                if st.session_state.global_cash < fr['price']:
                                    st.error("현금 부족!")
                                else:
                                    st.session_state.global_cash -= fr['price']
                                    atomic_add_cash(uid, -fr['price'])
                                    unlocked_frames.add(fr_id)
                                    users[uid]['unlocked_frames'] = list(unlocked_frames)
                                    users[uid]['profile_frame']   = fr_id
                                    save_db(USERS_FILE, users)
                                    sync_user_data()
                                    log_tx(uid,"프로필",f"{fr['name']} 프레임 구매",-fr['price'])
                                    st.toast(f"🔲 {fr['name']} 프레임 구매 완료!", icon="✅")
                                    st.rerun()

        # ── Status message
        with cust_tabs[3]:
            st.markdown('<div class="prof-section-header">💬 상태 메시지</div>', unsafe_allow_html=True)
            st.markdown("<div style='color:#94A3B8;font-size:0.85rem;margin-bottom:12px;'>다른 유저들이 볼 수 있는 상태 메시지를 설정하세요.</div>", unsafe_allow_html=True)
            st.markdown("**⚡ 빠른 선택**")
            msg_cols = st.columns(3)
            for i, msg in enumerate(STATUS_MESSAGES):
                with msg_cols[i%3]:
                    if st.button(msg, key=f"qmsg_{i}", use_container_width=True):
                        users[uid]['status_msg'] = msg
                        save_db(USERS_FILE, users)
                        st.toast("상태 메시지 변경!", icon="✅")
                        st.rerun()
            st.write("")
            st.markdown("**✏️ 직접 입력**")
            new_msg = st.text_input("상태 메시지 (최대 40자)", value=status_msg, max_chars=40)
            if st.button("✅ 저장", use_container_width=True, key="save_msg"):
                users[uid]['status_msg'] = new_msg
                save_db(USERS_FILE, users)
                st.toast("저장 완료!", icon="✅")
                st.rerun()

    # ── TAB 6: 설정
    with main_tabs[5]:
        set_tabs = st.tabs(["🔑 비밀번호 변경","🗑️ 거래내역","ℹ️ 계정 정보"])

        with set_tabs[0]:
            st.markdown('<div class="prof-section-header">🔑 비밀번호 변경</div>', unsafe_allow_html=True)
            cur_pw  = st.text_input("현재 비밀번호", type="password", key="chpw_cur")
            new_pw1 = st.text_input("새 비밀번호",   type="password", key="chpw_new1")
            new_pw2 = st.text_input("새 비밀번호 확인", type="password", key="chpw_new2")
            if st.button("✅ 비밀번호 변경", use_container_width=True, key="chpw_btn"):
                from utils.core import verify_pw, hash_pw_bcrypt
                if not verify_pw(cur_pw, users[uid].get('pw','')):
                    st.error("❌ 현재 비밀번호가 틀렸습니다.")
                elif len(new_pw1) < 1:
                    st.error("❌ 새 비밀번호를 입력해주세요.")
                elif new_pw1 != new_pw2:
                    st.error("❌ 새 비밀번호가 일치하지 않습니다.")
                else:
                    users[uid]['pw'] = hash_pw_bcrypt(new_pw1)
                    save_db(USERS_FILE, users)
                    st.success("✅ 비밀번호가 변경되었습니다!")

        with set_tabs[1]:
            st.markdown('<div class="prof-section-header">🗑️ 최근 거래내역</div>', unsafe_allow_html=True)
            tx_list = u.get('tx_log', [])
            if not tx_list:
                st.markdown("<div style='color:#475569;text-align:center;padding:20px;'>거래 내역이 없습니다.</div>", unsafe_allow_html=True)
            else:
                for tx in tx_list[-30:]:
                    amt   = tx.get('amount', 0)
                    col   = "#00FF88" if amt > 0 else "#FF4B4B"
                    sign  = "+" if amt > 0 else ""
                    st.markdown(f"""
                    <div style='display:flex;justify-content:space-between;padding:9px 0;
                                border-bottom:1px solid rgba(255,255,255,0.04);'>
                        <div>
                            <span style='color:#E2E8F0;font-size:0.85rem;'>{tx.get("desc","?")}</span>
                            <span style='color:#64748B;font-size:0.75rem;margin-left:10px;'>{tx.get("ts","")}</span>
                        </div>
                        <span style='color:{col};font-weight:700;font-size:0.88rem;'>
                            {sign}{format_korean_money(abs(amt))}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

        with set_tabs[2]:
            st.markdown('<div class="prof-section-header">ℹ️ 계정 정보</div>', unsafe_allow_html=True)
            info_rows = [
                ("👤 아이디",       uid),
                ("📅 가입일",       join_date),
                ("⚡ 투자 레벨",     f"Lv.{lv} — {lv_title}"),
                ("🏅 달성 배지",     f"{badge_count}/{len(PROFILE_BADGES)}"),
                ("🎨 현재 테마",     PROFILE_THEMES.get(theme_id,{}).get('name','기본')),
                ("🔲 현재 프레임",   PROFILE_FRAMES.get(frame_id,{}).get('name','기본')),
                ("🐾 펫",           f"{pet_info['emoji']} Lv.{pet_lv}" if has_pet else "없음"),
            ]
            for label, val in info_rows:
                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;padding:10px 0;
                            border-bottom:1px solid rgba(255,255,255,0.05);'>
                    <span style='color:#64748B;'>{label}</span>
                    <span style='color:#E2E8F0;font-weight:700;'>{val}</span>
                </div>
                """, unsafe_allow_html=True)
