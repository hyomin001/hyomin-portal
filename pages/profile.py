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

    # NW formatted
    nw_fmt = format_korean_money(nw)

    # Progress to next level
    cur_thresh = next((req for lv_m,_,_,req in MILESTONES if nw >= req), 0)
    next_thresh = next((req for lv_m,_,_,req in reversed(MILESTONES) if req > nw), cur_thresh*10 or 10_000_000)
    if next_thresh > cur_thresh:
        progress_pct = min(100, int((nw - cur_thresh) / (next_thresh - cur_thresh) * 100))
    else:
        progress_pct = 100

    # Pet snippet
    pet_emoji    = pet_info.get('emoji','🥚')
    pet_name     = pet_info.get('name','없음')
    pet_lv       = pet_info.get('level',0)
    has_pet      = pet_info.get('has_pet', False)

    # Asset donut data (simplified)
    asset_total  = sum(v for v in assets.values() if v > 0) or 1
    cash_pct     = int(assets.get('현금',0)/asset_total*100)
    stock_pct    = int(assets.get('주식',0)/asset_total*100)
    coin_pct     = int(assets.get('코인',0)/asset_total*100)
    estate_pct   = int(assets.get('부동산',0)/asset_total*100)

    # Frame glow
    frame_glow = {
        'none': 'none',
        'silver': '0 0 20px rgba(180,180,180,0.5)',
        'gold':   '0 0 25px rgba(255,214,0,0.6)',
        'diamond':'0 0 30px rgba(0,229,255,0.7)',
        'legend': '0 0 40px rgba(170,0,255,0.8)',
        'dragon': '0 0 50px rgba(255,80,0,0.9)',
    }.get(frame_id, 'none')

    frame_border = {
        'none':    p,
        'silver':  '#B8C0CC',
        'gold':    '#FFD600',
        'diamond': '#00E5FF',
        'legend':  '#AA00FF',
        'dragon':  '#FF6B00',
    }.get(frame_id, p)

    is_rainbow = theme_id == 'rainbow'

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;overflow:hidden;font-family:'Courier New',monospace;}}
#card{{
  width:100%;height:410px;
  background:linear-gradient(135deg,{bg} 0%,rgba(5,5,20,0.98) 100%);
  border:2px solid {frame_border};
  border-radius:22px;position:relative;overflow:hidden;
  box-shadow:{frame_glow},0 0 80px rgba(0,0,0,0.8);
}}
#bg-canvas{{position:absolute;inset:0;width:100%;height:100%;}}
#grid{{
  position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,0.015) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.015) 1px,transparent 1px);
  background-size:44px 44px;
}}
.corner{{position:absolute;width:22px;height:22px;border-color:{frame_border};border-style:solid;opacity:0.6;}}
.tl{{top:10px;left:10px;border-width:2px 0 0 2px;}}
.tr{{top:10px;right:10px;border-width:2px 2px 0 0;}}
.bl{{bottom:10px;left:10px;border-width:0 0 2px 2px;}}
.br{{bottom:10px;right:10px;border-width:0 2px 2px 0;}}

/* LAYOUT */
#layout{{position:absolute;inset:0;display:flex;flex-direction:row;align-items:stretch;z-index:5;}}
#left-panel{{
  width:200px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;
  justify-content:center;padding:20px 10px;border-right:1px solid rgba(255,255,255,0.06);
}}
#right-panel{{flex:1;display:flex;flex-direction:column;padding:18px 22px;overflow:visible;}}

/* AVATAR */
#avatar-ring{{
  width:108px;height:108px;border-radius:50%;
  border:3px solid {frame_border};
  background:rgba(0,0,0,0.5);
  display:flex;align-items:center;justify-content:center;
  position:relative;
  {"animation:rainbowBorder 3s linear infinite;" if is_rainbow else "animation:ringPulse 2.5s ease-in-out infinite;"}
  box-shadow:0 0 25px {frame_border}44;
}}
#avatar-emoji{{font-size:52px;line-height:1;animation:avatarFloat 4s ease-in-out infinite;}}
#lv-circle{{
  position:absolute;bottom:-8px;right:-8px;
  width:36px;height:36px;border-radius:50%;
  background:linear-gradient(135deg,{p},{s});
  border:2px solid rgba(0,0,0,0.6);
  display:flex;align-items:center;justify-content:center;
  color:#000;font-size:11px;font-weight:900;
}}
#username{{
  color:#fff;font-size:1.15rem;font-weight:900;text-align:center;margin-top:12px;
  letter-spacing:1px;text-shadow:0 0 12px {p};
}}
#player-title{{
  color:{p};font-size:0.68rem;font-weight:700;margin-top:4px;text-align:center;
  letter-spacing:1.5px;
}}
#frame-badge{{
  margin-top:8px;padding:3px 10px;border-radius:8px;
  background:rgba(0,0,0,0.5);border:1px solid {frame_border}66;
  color:{frame_border};font-size:0.68rem;font-weight:700;
}}

/* RIGHT PANEL TOP */
#top-row{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px;}}
#nw-block{{}}
#nw-lbl{{color:#64748b;font-size:0.72rem;letter-spacing:1px;}}
#nw-val{{
  {"background:linear-gradient(90deg,#ff00ff,#00ffff,#ff00ff);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:rainbowText 3s linear infinite;" if is_rainbow else "color:#FFD600;"}
  font-size:1.6rem;font-weight:900;margin-top:2px;line-height:1;
}}
#title-block{{text-align:right;}}
#lv-title-txt{{color:{p};font-size:0.78rem;font-weight:700;}}
#join-txt{{color:#475569;font-size:0.7rem;margin-top:3px;}}
#status-msg{{
  color:#94A3B8;font-size:0.78rem;margin-top:-4px;margin-bottom:12px;
  border-left:2px solid {p};padding-left:10px;font-style:italic;
}}

/* PROGRESS BAR */
#prog-section{{margin-bottom:12px;}}
#prog-lbl{{display:flex;justify-content:space-between;color:#64748b;font-size:0.7rem;margin-bottom:4px;}}
#prog-bg{{background:rgba(255,255,255,0.07);border-radius:4px;height:7px;overflow:hidden;}}
#prog-fill{{
  height:100%;border-radius:4px;
  background:linear-gradient(90deg,{p},{s});
  width:{progress_pct}%;transition:width 1s ease;
  {"animation:rainbowFill 3s linear infinite;" if is_rainbow else ""}
  box-shadow:0 0 8px {p}88;
}}

/* BOTTOM STATS */
#bottom-row{{display:flex;gap:12px;flex-wrap:wrap;margin-top:auto;}}
.stat-box{{
  background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
  border-radius:10px;padding:8px 12px;flex:1;min-width:80px;
}}
.stat-box-lbl{{color:#475569;font-size:0.65rem;letter-spacing:1px;margin-bottom:3px;}}
.stat-box-val{{color:#E2E8F0;font-size:0.88rem;font-weight:900;}}

/* MINI DONUT */
#donut-wrap{{
  position:absolute;right:18px;top:50%;transform:translateY(-50%);
  width:100px;height:100px;
}}
#donut-svg{{width:100%;height:100%;animation:donutSpin 20s linear infinite;}}
#donut-label{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  text-align:center;
}}
#donut-main{{color:#E2E8F0;font-size:0.65rem;font-weight:700;}}

/* PARTICLES */
.ptcl{{position:absolute;pointer-events:none;font-size:12px;animation:ptclRise linear forwards;opacity:0;z-index:4;}}
.glow-orb{{
  position:absolute;border-radius:50%;pointer-events:none;
  animation:orbPulse 4s ease-in-out infinite alternate;
  filter:blur(35px);z-index:0;
}}

/* ANIMATIONS */
@keyframes ringPulse{{
  0%,100%{{box-shadow:0 0 20px {p}44;}}
  50%{{box-shadow:0 0 40px {p}88,0 0 80px {p}22;}}
}}
@keyframes rainbowBorder{{
  0%{{box-shadow:0 0 30px #ff00ff88;border-color:#ff00ff;}}
  20%{{box-shadow:0 0 30px #ff990088;border-color:#ff9900;}}
  40%{{box-shadow:0 0 30px #ffff0088;border-color:#ffff00;}}
  60%{{box-shadow:0 0 30px #00ff8888;border-color:#00ff88;}}
  80%{{box-shadow:0 0 30px #00e5ff88;border-color:#00e5ff;}}
  100%{{box-shadow:0 0 30px #ff00ff88;border-color:#ff00ff;}}
}}
@keyframes rainbowText{{
  0%{{background-position:0%;}}
  100%{{background-position:200%;}}
}}
@keyframes rainbowFill{{
  0%{{background:linear-gradient(90deg,#ff00ff,#ff9900,#ffff00);}}
  33%{{background:linear-gradient(90deg,#00ff88,#00e5ff,#aa00ff);}}
  66%{{background:linear-gradient(90deg,#ff4b4b,#ff00ff,#00e5ff);}}
  100%{{background:linear-gradient(90deg,#ff00ff,#ff9900,#ffff00);}}
}}
@keyframes avatarFloat{{
  0%,100%{{transform:translateY(0) scale(1);}}
  50%{{transform:translateY(-10px) scale(1.04);}}
}}
@keyframes ptclRise{{
  0%{{opacity:0;transform:translateY(0) scale(0.5);}}
  10%{{opacity:0.6;}}
  90%{{opacity:0.1;}}
  100%{{opacity:0;transform:translateY(-280px) translateX(var(--dx)) scale(1);}}
}}
@keyframes orbPulse{{
  from{{opacity:0.06;transform:scale(0.9);}}
  to{{opacity:0.14;transform:scale(1.1);}}
}}
@keyframes donutSpin{{
  from{{transform:rotate(0);}} to{{transform:rotate(360deg);}}
}}
@keyframes scanLine{{
  0%{{top:-10%;}} 100%{{top:110%;}}
}}
</style>
</head>
<body>
<div id="card">
  <canvas id="bg-canvas"></canvas>
  <div id="grid"></div>
  <div class="corner tl"></div><div class="corner tr"></div>
  <div class="corner bl"></div><div class="corner br"></div>

  <!-- Glow orbs -->
  <div class="glow-orb" style="width:200px;height:200px;left:-60px;top:-60px;
    background:{p};animation-delay:0s;"></div>
  <div class="glow-orb" style="width:160px;height:160px;right:40px;bottom:-40px;
    background:{s};animation-delay:2s;"></div>

  <div id="layout">
    <!-- LEFT -->
    <div id="left-panel">
      <div id="avatar-ring">
        <div id="avatar-emoji">{avatar}</div>
        <div id="lv-circle">{lv}</div>
      </div>
      <div id="username">{uid}</div>
      <div id="player-title">✦ {custom_title} ✦</div>
      <div id="frame-badge">{frame['icon']} {frame['name']} 프레임</div>
    </div>

    <!-- RIGHT -->
    <div id="right-panel">
      <div id="top-row">
        <div id="nw-block">
          <div id="nw-lbl">💰 총 순자산</div>
          <div id="nw-val">{nw_fmt}</div>
        </div>
        <div id="title-block">
          <div id="lv-title-txt">{lv_title}</div>
          <div id="join-txt">📅 {join_date}</div>
        </div>
      </div>

      <div id="status-msg">{"💬 " + status_msg if status_msg else "상태 메시지를 설정해보세요..."}</div>

      <div id="prog-section">
        <div id="prog-lbl">
          <span>📈 다음 단계까지</span>
          <span>{progress_pct}%</span>
        </div>
        <div id="prog-bg"><div id="prog-fill"></div></div>
      </div>

      <div id="bottom-row">
        <div class="stat-box">
          <div class="stat-box-lbl">🏅 배지</div>
          <div class="stat-box-val">{badge_count}/{total_badges}</div>
        </div>
        <div class="stat-box">
          <div class="stat-box-lbl">🐾 펫</div>
          <div class="stat-box-val">{f"{pet_emoji} Lv.{pet_lv}" if has_pet else "없음"}</div>
        </div>
        <div class="stat-box">
          <div class="stat-box-lbl">💵 현금</div>
          <div class="stat-box-val">{format_korean_money(assets.get('현금',0))}</div>
        </div>
        <div class="stat-box">
          <div class="stat-box-lbl">📈 주식</div>
          <div class="stat-box-val">{format_korean_money(assets.get('주식',0))}</div>
        </div>
        <div class="stat-box">
          <div class="stat-box-lbl">🪙 코인</div>
          <div class="stat-box-val">{format_korean_money(assets.get('코인',0))}</div>
        </div>
      </div>
    </div>
  </div>

  <!-- EFX -->
  <div id="efx" style="position:absolute;inset:0;pointer-events:none;z-index:20;"></div>
</div>

<script>
const P="{p}", S="{s}", BG="{bg}";
const IS_RAINBOW={str(is_rainbow).lower()};
const APP = document.getElementById('card');
const EFX = document.getElementById('efx');

// ── Starfield canvas
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
canvas.width=700; canvas.height=410;
const stars = Array.from({{length:70}}, ()=>({{'x':Math.random()*700,'y':Math.random()*360,
  'r':Math.random()*1.4+0.2,'op':Math.random(),'spd':Math.random()*0.015+0.005,'dir':1}}));
// Rainbow stars
let hueOff = 0;
function drawBg(){{
  ctx.clearRect(0,0,700,360);
  stars.forEach(s=>{{
    s.op += s.spd*s.dir; if(s.op>1||s.op<0.05) s.dir*=-1;
    if(IS_RAINBOW){{
      hueOff += 0.002;
      ctx.fillStyle='hsla('+(s.x+hueOff*100)+',100%,80%,'+s.op.toFixed(2)+')';
    }} else {{
      ctx.fillStyle='rgba(255,255,255,'+s.op.toFixed(2)+')';
    }}
    ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2); ctx.fill();
  }});
  requestAnimationFrame(drawBg);
}}
drawBg();

// ── Particle emitter
const ptcls = IS_RAINBOW
  ? ['✨','🌈','💫','⭐','🔮','💜','💛','💖']
  : ['✨','💫','⭐','💎'];
function spawnPtcl(){{
  const p=document.createElement('div');
  p.className='ptcl';
  p.textContent=ptcls[Math.floor(Math.random()*ptcls.length)];
  const dx=(Math.random()-0.5)*80;
  p.style.setProperty('--dx',dx+'px');
  p.style.left=Math.random()*90+'%';
  p.style.bottom='-15px';
  p.style.animationDuration=(5+Math.random()*5)+'s';
  APP.insertBefore(p,APP.firstChild);
  setTimeout(()=>p.remove(),11000);
}}
setInterval(spawnPtcl,1600);

// ── Scan line effect
const scan=document.createElement('div');
scan.style.cssText='position:absolute;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,'+P+'44,transparent);pointer-events:none;z-index:15;animation:scanLine 5s linear infinite;';
APP.appendChild(scan);

// ── Click burst on avatar
const av=document.getElementById('avatar-ring');
const SPARKS=['✨','⭐','💫','🌟'];
av.addEventListener('click',e=>{{
  for(let i=0;i<8;i++){{
    const sp=document.createElement('div');
    sp.style.cssText='position:absolute;font-size:18px;pointer-events:none;z-index:60;';
    sp.textContent=SPARKS[Math.floor(Math.random()*SPARKS.length)];
    const a=(i/8)*Math.PI*2;
    const r=document.getElementById('card').getBoundingClientRect();
    sp.style.left=(e.clientX-r.left)+'px';
    sp.style.top =(e.clientY-r.top)+'px';
    EFX.appendChild(sp);
    const dx=Math.cos(a)*45,dy=Math.sin(a)*45;
    sp.animate([
      {{opacity:1,transform:'translate(0,0) scale(0.5)'}},
      {{opacity:0,transform:'translate('+dx+'px,'+dy+'px) scale(1.3)'}}
    ],{{duration:700,easing:'ease-out'}}).onfinish=()=>sp.remove();
  }}
}});
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
        height=420,
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
