# pages/profile.py
import streamlit as st
import time
from datetime import datetime
from utils.config import (
    KST, USERS_FILE, FORGE_DATA, estate_config,
    stock_config, CRYPTO_CONFIG
)
from utils.core import format_korean_money, sync_user_data
from utils.database import load_db, save_db, log_tx, atomic_add_cash

# ── 아바타 목록 ─────────────────────────────────────────────
AVATARS = [
    ("🧑‍🚀", "우주인"),  ("🥷", "닌자"),    ("🧙", "마법사"),  ("🦸", "슈퍼히어로"),
    ("🧛", "뱀파이어"), ("🤖", "로봇"),    ("👑", "왕"),      ("🐉", "드래곤"),
    ("🦊", "여우"),     ("🐺", "늑대"),    ("🦁", "사자"),    ("🐯", "호랑이"),
    ("🐼", "판다"),     ("🐸", "개구리"),  ("🦋", "나비"),    ("🌟", "별"),
    ("🔥", "불꽃"),     ("❄️", "얼음"),    ("⚡", "번개"),    ("🌙", "달"),
]

AVATAR_UNLOCK_PRICE = 3_000_000_000  # 아바타 잠금 해제: 30억

PROFILE_BADGES = [
    {"id": "first_login",    "icon": "🎖️",  "name": "첫 발걸음",    "desc": "처음 로그인"},
    {"id": "rich_5",         "icon": "💰",  "name": "초보 부자",     "desc": "순자산 5억 달성"},
    {"id": "landlord",       "icon": "🏢",  "name": "건물주",        "desc": "부동산 1채 보유"},
    {"id": "billionaire",    "icon": "💎",  "name": "억만장자",      "desc": "순자산 1000억 달성"},
    {"id": "weapon_master",  "icon": "⚔️",  "name": "무기 장인",     "desc": "+10 이상 명검 보유"},
    {"id": "gambler",        "icon": "🎰",  "name": "도박사",        "desc": "카지노 100회 이상"},
    {"id": "miner",          "icon": "⛏️",  "name": "광부왕",        "desc": "광산 1000회 이상"},
    {"id": "clan_member",    "icon": "🏰",  "name": "클랜원",        "desc": "클랜 가입"},
    {"id": "cryptowhale",    "icon": "🐋",  "name": "코인 고래",     "desc": "코인 평가액 10억 이상"},
    {"id": "stock_guru",     "icon": "📈",  "name": "주식의 신",     "desc": "주식 평가액 10억 이상"},
    {"id": "pet_owner",      "icon": "🐾",  "name": "펫 주인",       "desc": "펫 레벨 10 달성"},
    {"id": "dungeon_clear",  "icon": "🗡️",  "name": "던전 클리어",   "desc": "던전 1회 클리어"},
]

STATUS_MESSAGES = [
    "지금 막 대박났음 🎰",
    "주식이 날아가고 있다... ✈️",
    "코인 HODLing 중 🚀",
    "광산에서 노가다 중 ⛏️",
    "자본주의의 꼭대기를 향해 📈",
    "건물주의 삶은 달콤해 🏢",
    "강화 실패로 멘탈 나감 💀",
    "오늘은 무조건 대박 🔥",
    "효민 우주에서 살아남기 🌌",
    "부동산은 역시 최고 💎",
    "퀘스트 완료 도전 중 📅",
    "랭킹 1위를 향해 👑",
]

def compute_badges(uid, users, market, nw):
    u = users.get(uid, {})
    badges = []
    badges.append("first_login")
    if nw >= 500_000_000:       badges.append("rich_5")
    if any(v > 0 for v in u.get('real_estate', {}).values()):
        badges.append("landlord")
    if nw >= 100_000_000_000:   badges.append("billionaire")
    if u.get('weapon_level', 0) >= 10: badges.append("weapon_master")
    if u.get('dungeon_stats', {}).get('clears', 0) >= 1: badges.append("dungeon_clear")
    # 코인/주식 평가
    crypto_data = market.get('crypto_data', {})
    coin_val = sum(ci.get('qty', 0) * crypto_data.get(cid, {}).get('price', 0)
                   for cid, ci in u.get('crypto_portfolio', {}).items())
    if coin_val >= 1_000_000_000: badges.append("cryptowhale")
    stock_data = market.get('stock_data', {})
    stock_val = sum(u.get('portfolio', {}).get(s['id'], {}).get('qty', 0) * stock_data.get(s['id'], {}).get('price', 0)
                    for s in stock_config)
    if stock_val >= 1_000_000_000: badges.append("stock_guru")
    if u.get('game_records', {}).get('dungeon_stats', {}).get('clears', 0) >= 1: badges.append("dungeon_clear")
    pet_data = u.get('pet', {})
    if pet_data.get('level', 0) >= 10: badges.append("pet_owner")
    return badges

def get_level_from_nw(nw):
    thresholds = [
        (1_000_000_000_000_000, 100, "🌌 우주신"),
        (100_000_000_000_000,   90,  "🌠 은하계 지배자"),
        (10_000_000_000_000,    80,  "☄️ 소행성 대군주"),
        (1_000_000_000_000,     70,  "🪐 행성 영주"),
        (500_000_000_000,       60,  "🌙 달 지배자"),
        (100_000_000_000,       55,  "🚀 우주 탐험가"),
        (50_000_000_000,        50,  "⭐ 별의 상인"),
        (10_000_000_000,        40,  "💫 위성 자본가"),
        (5_000_000_000,         35,  "🏆 마스터 투자자"),
        (1_000_000_000,         30,  "💎 다이아 투자자"),
        (500_000_000,           25,  "🥇 골드 투자자"),
        (100_000_000,           20,  "🥈 실버 투자자"),
        (50_000_000,            15,  "🥉 브론즈 투자자"),
        (10_000_000,            10,  "📊 초보 투자자"),
        (0,                     1,   "🌱 튜토리얼 중"),
    ]
    for thresh, lv, title in thresholds:
        if nw >= thresh:
            return lv, title
    return 1, "🌱 튜토리얼 중"

def render(market, nw):
    st.title("👤 내 프로필")

    uid   = st.session_state.logged_in_user
    users = load_db(USERS_FILE, {})
    u     = users.get(uid, {})

    # ── 레벨/칭호 계산
    lv, lv_title = get_level_from_nw(nw)
    avatar        = u.get('avatar', '🧑‍🚀')
    custom_title  = st.session_state.equipped_title
    status_msg    = u.get('status_msg', '')
    join_date     = u.get('join_date', '알 수 없음')
    unlocked_av   = set(u.get('unlocked_avatars', ['🧑‍🚀']))

    # ══════════════════════════════════════════════════════
    # 🏠 메인 프로필 카드
    # ══════════════════════════════════════════════════════
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0d1020,#111828);border:2px solid #00E5FF;
                border-radius:20px;padding:28px;margin-bottom:24px;
                box-shadow:0 0 40px rgba(0,229,255,0.15);'>
        <div style='display:flex;align-items:center;gap:24px;flex-wrap:wrap;'>
            <div style='font-size:5rem;background:rgba(0,229,255,0.08);border:2px solid rgba(0,229,255,0.3);
                        border-radius:50%;width:110px;height:110px;display:flex;align-items:center;
                        justify-content:center;flex-shrink:0;'>
                {avatar}
            </div>
            <div style='flex:1;min-width:200px;'>
                <div style='color:#00FF88;font-size:0.85rem;font-weight:700;letter-spacing:2px;
                            text-transform:uppercase;margin-bottom:4px;'>
                    {custom_title}
                </div>
                <div style='font-size:2.2rem;font-weight:900;color:#fff;
                            font-family:"Orbitron",monospace;line-height:1.1;'>
                    {uid}
                </div>
                <div style='color:#64748B;font-size:0.85rem;margin-top:6px;'>
                    {"💬 " + status_msg if status_msg else "상태 메시지를 설정해보세요..."}
                </div>
            </div>
            <div style='text-align:right;border-left:1px solid rgba(0,229,255,0.2);
                        padding-left:24px;flex-shrink:0;'>
                <div style='font-size:2.5rem;font-weight:900;color:#FFD600;
                            font-family:"Orbitron",monospace;'>Lv.{lv}</div>
                <div style='color:#B0BAC8;font-size:0.9rem;margin-top:4px;'>{lv_title}</div>
                <div style='color:#475569;font-size:0.8rem;margin-top:8px;'>가입일: {join_date}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # 📊 자산 요약 카드
    # ══════════════════════════════════════════════════════
    st.markdown("### 📊 자산 현황")

    cash = st.session_state.global_cash
    loan = st.session_state.loan
    real_estate_val = sum(
        estate_config[eid]['base_price'] * cnt * 0.8
        for eid, cnt in st.session_state.get('real_estate', {}).items()
        if eid in estate_config
    )
    stock_data = market.get('stock_data', {})
    stock_val = sum(
        u.get('portfolio', {}).get(s['id'], {}).get('qty', 0) * stock_data.get(s['id'], {}).get('price', 0)
        for s in stock_config
    )
    crypto_data = market.get('crypto_data', {})
    coin_val = sum(
        ci.get('qty', 0) * crypto_data.get(cid, {}).get('price', 0)
        for cid, ci in u.get('crypto_portfolio', {}).items()
    )
    w_lv = u.get('weapon_level', 0)
    weapon_val = FORGE_DATA[w_lv]['sell'] if w_lv > 0 and w_lv in FORGE_DATA else 0

    asset_rows = [
        ("💵 보유 현금",     cash,          "#FFD600"),
        ("📈 주식 평가액",   int(stock_val), "#00FF88"),
        ("🪙 코인 평가액",   int(coin_val),  "#FF9500"),
        ("🏢 부동산 평가",   int(real_estate_val), "#00E5FF"),
        ("⚔️ 명검 가치",     weapon_val,    "#FF00FF"),
        ("💳 대출금",        -loan,         "#FF4B4B"),
        ("📊 총 순자산",     nw,            "#FFFFFF"),
    ]

    cols = st.columns(4)
    for i, (label, val, color) in enumerate(asset_rows):
        with cols[i % 4]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                        border-radius:12px;padding:14px;margin-bottom:12px;text-align:center;'>
                <div style='color:#64748B;font-size:0.8rem;margin-bottom:4px;'>{label}</div>
                <div style='color:{color};font-weight:900;font-size:1rem;'>{format_korean_money(abs(val))}{"" if val >= 0 else " (부채)"}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ══════════════════════════════════════════════════════
    # 🏅 배지 컬렉션
    # ══════════════════════════════════════════════════════
    st.markdown("### 🏅 획득 배지")
    earned = set(compute_badges(uid, users, market, nw))

    badge_cols = st.columns(6)
    for i, b in enumerate(PROFILE_BADGES):
        has = b['id'] in earned
        with badge_cols[i % 6]:
            st.markdown(f"""
            <div style='background:{"rgba(0,229,255,0.1)" if has else "rgba(255,255,255,0.03)"};
                        border:1px solid {"#00E5FF" if has else "#1E293B"};
                        border-radius:12px;padding:12px;text-align:center;margin-bottom:8px;
                        opacity:{"1" if has else "0.35"};'>
                <div style='font-size:1.8rem;'>{b['icon']}</div>
                <div style='font-size:0.72rem;color:#E2E8F0;font-weight:700;margin-top:4px;'>{b['name']}</div>
                <div style='font-size:0.65rem;color:#64748B;margin-top:2px;'>{b['desc']}</div>
                {"<div style='color:#00FF88;font-size:0.65rem;margin-top:4px;'>✅ 달성</div>" if has else "<div style='color:#475569;font-size:0.65rem;margin-top:4px;'>🔒 미달성</div>"}
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ══════════════════════════════════════════════════════
    # 🎮 게임 기록
    # ══════════════════════════════════════════════════════
    st.markdown("### 🎮 게임 기록")
    gr = u.get('game_records', {})
    dungeon = u.get('dungeon_stats', {})
    marble  = u.get('marble_stats', {})

    game_records = [
        ("🏎️ 네온 레이싱", f"{gr.get('racing',{}).get('score',0):,}점", f"거리: {gr.get('racing',{}).get('dist',0):.1f}km"),
        ("🧟 좀비 서바이벌", f"Wave {gr.get('zombie',{}).get('wave',0)}", f"킬: {gr.get('zombie',{}).get('kills',0):,}"),
        ("🥊 격투 챔피언", f"{gr.get('fighter',{}).get('score',0):,}점", f"퍼펙트: {gr.get('fighter',{}).get('perfects',0)}"),
        ("🎯 저격 마스터", f"{gr.get('sniper',{}).get('score',0):,}점", f"킬: {gr.get('sniper',{}).get('kills',0):,}"),
        ("🌍 인베스트 마블", format_korean_money(marble.get('best_net_worth',0)), f"승: {marble.get('wins',0)} / 판: {marble.get('games_played',0)}"),
        ("⚔️ 던전 클리어", f"{dungeon.get('clears',0)}회", f"킬: {dungeon.get('best_kills',0):,}"),
    ]

    gr_cols = st.columns(3)
    for i, (title, main, sub) in enumerate(game_records):
        with gr_cols[i % 3]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:12px;padding:14px;margin-bottom:12px;'>
                <div style='color:#B0BAC8;font-size:0.8rem;'>{title}</div>
                <div style='color:#FFD600;font-size:1.1rem;font-weight:900;margin-top:4px;'>{main}</div>
                <div style='color:#475569;font-size:0.78rem;margin-top:2px;'>{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ══════════════════════════════════════════════════════
    # 🎨 프로필 꾸미기 탭
    # ══════════════════════════════════════════════════════
    st.markdown("### 🎨 프로필 커스터마이징")
    tab1, tab2, tab3 = st.tabs(["🖼️ 아바타 변경", "💬 상태 메시지", "🔑 비밀번호 변경"])

    with tab1:
        st.markdown("<div style='color:#B0BAC8;font-size:0.9rem;margin-bottom:16px;'>아바타를 선택하세요. 기본 제공 외 아바타는 30억원에 해금 가능합니다.</div>", unsafe_allow_html=True)
        av_cols = st.columns(5)
        for i, (em, name) in enumerate(AVATARS):
            unlocked = em in unlocked_av or em == '🧑‍🚀'
            is_cur   = (em == avatar)
            with av_cols[i % 5]:
                border_color = "#FFD600" if is_cur else ("#00E5FF" if unlocked else "#333")
                lock_badge   = "" if unlocked else "🔒"
                st.markdown(f"""
                <div style='background:{"rgba(255,214,0,0.1)" if is_cur else "rgba(255,255,255,0.04)"};
                            border:2px solid {border_color};border-radius:12px;
                            padding:12px;text-align:center;margin-bottom:8px;'>
                    <div style='font-size:2rem;'>{em}</div>
                    <div style='font-size:0.7rem;color:#B0BAC8;margin-top:4px;'>{name} {lock_badge}</div>
                </div>
                """, unsafe_allow_html=True)
                if not is_cur:
                    if unlocked:
                        if st.button(f"선택", key=f"av_{i}"):
                            users[uid]['avatar'] = em
                            save_db(USERS_FILE, users)
                            st.toast(f"{em} 아바타로 변경!", icon="✅")
                            st.rerun()
                    else:
                        if st.button(f"해금 30억", key=f"av_unlock_{i}"):
                            if st.session_state.global_cash < AVATAR_UNLOCK_PRICE:
                                st.error("현금이 부족합니다!")
                            else:
                                st.session_state.global_cash -= AVATAR_UNLOCK_PRICE
                                unlocked_av.add(em)
                                users[uid]['unlocked_avatars'] = list(unlocked_av)
                                users[uid]['avatar'] = em
                                save_db(USERS_FILE, users)
                                sync_user_data()
                                st.toast(f"🎉 {em} 아바타 해금!", icon="✅")
                                st.rerun()
                else:
                    st.markdown("<div style='text-align:center;color:#FFD600;font-size:0.75rem;'>현재 착용 중</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div style='color:#B0BAC8;font-size:0.9rem;margin-bottom:12px;'>다른 유저들이 볼 수 있는 상태 메시지를 설정하세요.</div>", unsafe_allow_html=True)
        st.markdown("**빠른 선택:**")
        msg_cols = st.columns(3)
        for i, msg in enumerate(STATUS_MESSAGES):
            with msg_cols[i % 3]:
                if st.button(msg, key=f"quick_msg_{i}", use_container_width=True):
                    users[uid]['status_msg'] = msg
                    save_db(USERS_FILE, users)
                    st.toast("상태 메시지 변경!", icon="✅")
                    st.rerun()
        st.markdown("**직접 입력:**")
        new_msg = st.text_input("상태 메시지", value=status_msg, max_chars=40, placeholder="최대 40자...")
        if st.button("✅ 상태 메시지 저장", use_container_width=True):
            users[uid]['status_msg'] = new_msg
            save_db(USERS_FILE, users)
            st.toast("상태 메시지 저장!", icon="✅")
            st.rerun()

    with tab3:
        cur_pw  = st.text_input("현재 비밀번호", type="password", key="prof_chpw_cur")
        new_pw1 = st.text_input("새 비밀번호",   type="password", key="prof_chpw_new1")
        new_pw2 = st.text_input("새 비밀번호 확인", type="password", key="prof_chpw_new2")
        if st.button("✅ 비밀번호 변경", use_container_width=True, key="prof_chpw_btn"):
            from utils.core import verify_pw, hash_pw_bcrypt
            if not verify_pw(cur_pw, users[uid].get('pw', '')):
                st.error("❌ 현재 비밀번호가 틀렸습니다.")
            elif len(new_pw1) < 1:
                st.error("❌ 새 비밀번호를 입력해주세요.")
            elif new_pw1 != new_pw2:
                st.error("❌ 새 비밀번호가 일치하지 않습니다.")
            else:
                users[uid]['pw'] = hash_pw_bcrypt(new_pw1)
                save_db(USERS_FILE, users)
                st.success("✅ 비밀번호가 변경되었습니다!")

    st.write("---")

    # ══════════════════════════════════════════════════════
    # 📈 성장 타임라인
    # ══════════════════════════════════════════════════════
    st.markdown("### 📈 성장 단계")
    milestones = [
        (1,   "🌱",  "튜토리얼 시작",       0),
        (10,  "📊",  "초보 투자자",         10_000_000),
        (20,  "🥉",  "브론즈 투자자",       50_000_000),
        (25,  "🥈",  "실버 투자자",         100_000_000),
        (30,  "🥇",  "골드 투자자",         500_000_000),
        (35,  "🏆",  "마스터 투자자",       1_000_000_000),
        (40,  "💫",  "위성 자본가",         5_000_000_000),
        (50,  "⭐",  "별의 상인",           10_000_000_000),
        (55,  "🚀",  "우주 탐험가",         50_000_000_000),
        (60,  "🌙",  "달 지배자",           100_000_000_000),
        (70,  "🪐",  "행성 영주",           500_000_000_000),
        (80,  "☄️",  "소행성 대군주",       1_000_000_000_000),
        (90,  "🌠",  "은하계 지배자",       100_000_000_000_000),
        (100, "🌌",  "우주신",              1_000_000_000_000_000),
    ]

    ml_cols = st.columns(7)
    for i, (lv_m, icon, name, req) in enumerate(milestones):
        achieved = nw >= req
        with ml_cols[i % 7]:
            st.markdown(f"""
            <div style='text-align:center;padding:8px;border-radius:10px;
                        background:{"rgba(0,229,255,0.1)" if achieved else "rgba(255,255,255,0.02)"};
                        border:1px solid {"#00E5FF" if achieved else "#1E293B"};
                        margin-bottom:8px;opacity:{"1" if achieved else "0.4"}'>
                <div style='font-size:1.5rem;'>{icon}</div>
                <div style='color:#FFD600;font-size:0.8rem;font-weight:900;'>Lv.{lv_m}</div>
                <div style='color:#94A3B8;font-size:0.65rem;'>{name}</div>
            </div>
            """, unsafe_allow_html=True)
