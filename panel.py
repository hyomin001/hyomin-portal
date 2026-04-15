# ============================================================
# pages/admin/panel.py — 창조주 통제소 (코인 통제 추가)
# ============================================================
import re
import time
import random
import streamlit as st
import pandas as pd
from datetime import datetime

from config import (
    STOCK_CONFIG, CRYPTO_CONFIG, ESTATE_CONFIG,
    FORGE_DATA, CAR_TIERS, DAILY_QUESTS_CONFIG,
)
from utils.database import (
    load_db, save_db, log_tx,
    get_market, save_market,
    load_estate_market, save_estate_market,
    load_clan_db, save_clan_db, get_user_clan,
    USERS_FILE, COMMENTS_FILE, TXLOG_FILE, MESSAGES_FILE,
)
from utils.helpers import format_korean_money, parse_korean_money
from utils.sync import get_net_worth, sync_user_data, claim_hidden_title
from datetime import timezone, timedelta

KST = timezone(timedelta(hours=9))


def render():
    st.title("🛠️ 창조주 통제소")
    st.markdown(
        "<div style='color:#FF4B4B;font-size:0.85rem;margin-bottom:10px;'>"
        "⚠️ 창조주 전용 패널. 모든 조작은 서버 전체에 즉시 반영됩니다.</div>",
        unsafe_allow_html=True,
    )

    market = get_market()
    u_db   = load_db(USERS_FILE, {})
    uid_list = [u for u in u_db if u != "admin"]

    tabs = st.tabs([
        "👤 유저 개조", "🏢 부동산 통제", "💬 게시판 관리",
        "🌍 글로벌 정책", "📈 주식 조작", "🪙 코인 조작",   # ← 코인 탭 신규
        "📊 전체 현황", "👁️ 활동 로그", "🏎️ 차고지 조작",
        "🏆 시즌 관리", "📩 쪽지 감시",
    ])

    # ════════════════════════════════════════
    # 탭 0: 유저 개조
    # ════════════════════════════════════════
    with tabs[0]:
        _tab_user(u_db, uid_list, market)

    # ════════════════════════════════════════
    # 탭 1: 부동산 통제
    # ════════════════════════════════════════
    with tabs[1]:
        _tab_real_estate(u_db, uid_list, market)

    # ════════════════════════════════════════
    # 탭 2: 게시판 관리
    # ════════════════════════════════════════
    with tabs[2]:
        _tab_board(market)

    # ════════════════════════════════════════
    # 탭 3: 글로벌 정책
    # ════════════════════════════════════════
    with tabs[3]:
        _tab_global(u_db, market)

    # ════════════════════════════════════════
    # 탭 4: 주식 조작
    # ════════════════════════════════════════
    with tabs[4]:
        _tab_stock(market)

    # ════════════════════════════════════════
    # 탭 5: 코인 조작 (신규)
    # ════════════════════════════════════════
    with tabs[5]:
        _tab_crypto(u_db, uid_list, market)

    # ════════════════════════════════════════
    # 탭 6: 전체 현황
    # ════════════════════════════════════════
    with tabs[6]:
        _tab_overview(u_db, market)

    # ════════════════════════════════════════
    # 탭 7: 활동 로그
    # ════════════════════════════════════════
    with tabs[7]:
        _tab_logs()

    # ════════════════════════════════════════
    # 탭 8: 차고지 조작
    # ════════════════════════════════════════
    with tabs[8]:
        _tab_garage(u_db, uid_list, market)

    # ════════════════════════════════════════
    # 탭 9: 시즌 관리
    # ════════════════════════════════════════
    with tabs[9]:
        _tab_season(market)

    # ════════════════════════════════════════
    # 탭 10: 쪽지 감시
    # ════════════════════════════════════════
    with tabs[10]:
        _tab_messages()


# ──────────────────────────────────────────────────────────────
# 내부 탭 함수들
# ──────────────────────────────────────────────────────────────

def _tab_user(u_db, uid_list, market):
    if not uid_list:
        st.info("유저 없음")
        return
    sel_u = st.selectbox("조작할 유저", uid_list, key="adm_u_sel")
    u_data = u_db[sel_u]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("##### 💰 자산 개조")
        raw_cash = st.text_input("현금 (예: 1000억)", placeholder="비워두면 유지", key="adm_cash")
        raw_loan = st.text_input("대출 (예: 5000만)", placeholder="비워두면 유지", key="adm_loan")
        final_cash = parse_korean_money(raw_cash) or int(u_data.get("cash", 0))
        final_loan = parse_korean_money(raw_loan) or int(u_data.get("loan", 0))
        st.markdown(
            f"<div style='background:rgba(0,229,255,0.1);padding:12px;border-radius:8px;border:1px solid #00E5FF;margin-top:8px;'>"
            f"<b>현금:</b> {format_korean_money(final_cash)}<br>"
            f"<b>대출:</b> {format_korean_money(final_loan)}</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown("##### 👑 신분 개조")
        new_title = st.text_input("칭호", value=u_data.get("equipped_title", ""), key="adm_title")
        st.metric("현재 현금", format_korean_money(u_data.get("cash", 0)))
        st.metric("현재 대출", format_korean_money(u_data.get("loan", 0)))

    b1, b2, b3 = st.columns(3)
    if b1.button("🔥 강제 개조", use_container_width=True):
        u_db[sel_u]["cash"]           = final_cash
        u_db[sel_u]["loan"]           = final_loan
        u_db[sel_u]["equipped_title"] = new_title
        save_db(USERS_FILE, u_db)
        st.success("완료!")
        st.rerun()
    if b2.button("🕊️ 빚 탕감", use_container_width=True):
        u_db[sel_u]["loan"] = 0
        if u_db[sel_u].get("equipped_title") == "💸 신용불량자":
            u_db[sel_u]["equipped_title"] = "🌱 신규시민"
        save_db(USERS_FILE, u_db)
        st.success("탕감 완료!")
        st.rerun()
    if b3.button("🗑️ 계정 삭제", use_container_width=True, type="secondary"):
        del u_db[sel_u]
        save_db(USERS_FILE, u_db)
        st.rerun()

    st.write("---")
    st.markdown("##### 🗡️ 명검 통제")
    w1, w2, w3 = st.columns(3)
    if w1.button("👑 +15강 부여", use_container_width=True):
        u_db[sel_u]["weapon_level"] = 15; save_db(USERS_FILE, u_db); st.rerun()
    if w2.button("💀 파괴의 저주", use_container_width=True):
        u_db[sel_u]["cursed_forge"] = True; save_db(USERS_FILE, u_db); st.success("저주 완료"); st.rerun()
    if w3.button("🔨 무기 압수(0강)", use_container_width=True):
        u_db[sel_u]["weapon_level"] = 0; save_db(USERS_FILE, u_db); st.rerun()

    st.write("---")
    st.markdown("##### 🎒 칭호 / 인벤토리")
    give_t = st.text_input("지급할 칭호명", key="adm_give_t")
    if st.button("🎁 칭호 지급", use_container_width=True):
        if give_t.strip():
            u_db[sel_u].setdefault("inventory", [])
            if give_t not in u_db[sel_u]["inventory"]:
                u_db[sel_u]["inventory"].append(give_t)
            u_db[sel_u]["equipped_title"] = give_t
            save_db(USERS_FILE, u_db); st.success("지급!"); st.rerun()

    inv = u_db[sel_u].get("inventory", [])
    if inv:
        seize_item = st.selectbox("압수할 아이템", inv, key=f"seize_{sel_u}")
        if st.button("🔥 개별 압수", use_container_width=True):
            u_db[sel_u]["inventory"].remove(seize_item)
            if u_db[sel_u].get("equipped_title") == seize_item:
                u_db[sel_u]["equipped_title"] = "🌱 신규시민"
            save_db(USERS_FILE, u_db); st.success("압수!"); st.rerun()
    if st.button("🗑️ 인벤토리 전체 초기화", use_container_width=True):
        u_db[sel_u]["inventory"] = []; u_db[sel_u]["equipped_title"] = "🌱 신규시민"
        save_db(USERS_FILE, u_db); st.rerun()

    st.write("---")
    p1, p2 = st.columns(2)
    if p1.button("📈 주식 리셋", use_container_width=True):
        u_db[sel_u]["portfolio"] = {}; save_db(USERS_FILE, u_db); st.rerun()
    if p2.button("🪙 코인 리셋", use_container_width=True):
        u_db[sel_u]["crypto_portfolio"] = {}; save_db(USERS_FILE, u_db); st.rerun()

    st.write("---")
    st.markdown("### 🧹 서버 전체 칭호 패턴 수거")
    pattern = st.text_input("수거할 칭호 앞글자 패턴", value="[시즌2]", key="revoke_pattern")
    if pattern.strip() and st.button(f"🚨 '{pattern}' 전체 수거", use_container_width=True, type="secondary"):
        all_u = load_db(USERS_FILE, {})
        revoked = 0
        for u_id, u_info in all_u.items():
            if "inventory" in u_info:
                old = len(u_info["inventory"])
                u_info["inventory"] = [i for i in u_info["inventory"] if not str(i).startswith(pattern)]
                revoked += old - len(u_info["inventory"])
                if str(u_info.get("equipped_title", "")).startswith(pattern):
                    u_info["equipped_title"] = "🌱 신규시민"
        save_db(USERS_FILE, all_u)
        st.success(f"총 {revoked}개 수거 완료!")
        st.rerun()


def _tab_crypto(u_db, uid_list, market):
    """코인 조작 탭 (신규 추가)"""
    st.markdown("### 🪙 코인 가격 강제 조작")
    st.caption("각 코인의 현재 가격을 직접 설정하거나 배율로 조정할 수 있습니다.")

    cdata = market.get("crypto_data", {})
    if not cdata:
        st.warning("코인 마켓 데이터가 없습니다.")
        return

    for c in CRYPTO_CONFIG:
        cid = c["id"]
        if cid not in cdata:
            continue
        cur_p = cdata[cid]["price"]
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        col1.write(f"{c['icon']} {c['name']}")
        col2.write(f"현재: ₩{cur_p:,.4f}")
        if col3.button(f"🚀 +50%", key=f"c_up_{cid}"):
            market["crypto_data"][cid]["price"] = round(cur_p * 1.5, 6)
            market["news"] = f"🚀 [코인 폭등] {c['name']} 급등!!"
            save_market(market); st.rerun()
        if col4.button(f"📉 -40%", key=f"c_dn_{cid}"):
            market["crypto_data"][cid]["price"] = max(0.01, round(cur_p * 0.6, 6))
            market["news"] = f"💣 [코인 폭락] {c['name']} 대폭락!!"
            save_market(market); st.rerun()

    st.write("---")
    st.markdown("#### 특정 코인 가격 직접 설정")
    sel_coin = st.selectbox("코인 선택", [c["id"] for c in CRYPTO_CONFIG],
                             format_func=lambda x: f"{cdata[x]['name']} (현재: {cdata[x]['price']:,.4f})",
                             key="adm_coin_sel")
    new_price_str = st.text_input("새 가격 (원 단위)", placeholder="예: 200000000", key="adm_coin_price")
    if st.button("💰 가격 강제 설정", use_container_width=True):
        try:
            new_p = float(new_price_str.replace(",", ""))
            if new_p > 0:
                market["crypto_data"][sel_coin]["price"] = new_p
                market["crypto_data"][sel_coin]["history"].append(new_p)
                market["news"] = f"⚡ [운영자 개입] {cdata[sel_coin]['name']} 가격 강제 조정!"
                save_market(market)
                st.success(f"✅ {cdata[sel_coin]['name']} 가격을 ₩{new_p:,.4f}으로 설정!")
                st.rerun()
        except ValueError:
            st.error("숫자 형식으로 입력하세요.")

    st.write("---")
    st.markdown("### 💼 유저 코인 포트폴리오 압수")
    if uid_list:
        coin_target = st.selectbox("대상 유저", uid_list, key="adm_coin_target")
        user_crypto = u_db[coin_target].get("crypto_portfolio", {})
        if not user_crypto:
            st.info(f"{coin_target}님은 코인이 없습니다.")
        else:
            seize_cid = st.selectbox(
                "압수할 코인",
                list(user_crypto.keys()),
                format_func=lambda x: f"{cdata.get(x, {}).get('name', x)} ({user_crypto[x].get('qty', 0):.6f})",
                key="adm_seize_coin"
            )
            c_seize1, c_seize2 = st.columns(2)
            if c_seize1.button("🔨 선택 코인 전량 압수", use_container_width=True):
                del u_db[coin_target]["crypto_portfolio"][seize_cid]
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {coin_target}의 {cdata.get(seize_cid, {}).get('name', seize_cid)} 전량 압수!")
                st.rerun()
            if c_seize2.button("💣 전체 코인 몰수", use_container_width=True, type="secondary"):
                u_db[coin_target]["crypto_portfolio"] = {}
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {coin_target}의 코인 전체 몰수 완료!")
                st.rerun()

    st.write("---")
    st.markdown("### 🌪️ 전체 코인 시장 리셋")
    if st.button("💣 코인 전 종목 초기가격 복원", use_container_width=True, type="secondary"):
        from config import CRYPTO_CONFIG as CC
        for c in CC:
            market["crypto_data"][c["id"]]["price"] = float(c["base_price"])
            market["crypto_data"][c["id"]]["history"] = [float(c["base_price"])]
        market["news"] = "🔄 [운영자] 코인 전 종목 가격이 초기화되었습니다."
        save_market(market)
        st.success("코인 시장 초기화 완료!")
        st.rerun()


def _tab_real_estate(u_db, uid_list, market):
    st.markdown("### 🏢 부동산 시장 통제")
    em = load_estate_market()

    # 공급량 조작
    st.markdown("#### 🏗️ 신규 공급량 조작")
    stock = em.get("initial_stock", {})
    sel_eid = st.selectbox("매물 선택", list(ESTATE_CONFIG.keys()),
                            format_func=lambda x: f"{ESTATE_CONFIG[x]['icon']} {ESTATE_CONFIG[x]['name']}",
                            key="adm_re_eid")
    info = ESTATE_CONFIG[sel_eid]
    owned = sum(v.get(sel_eid, 0) for v in em["owner_counts"].values())
    listed = sum(1 for l in em["listings"] if l["eid"] == sel_eid)
    cur_limit = stock.get(sel_eid, info["total_supply"])
    remaining = max(0, cur_limit - owned - listed)

    c1, c2, c3 = st.columns([2, 2, 2])
    c1.metric("현재 한도", f"{cur_limit}개")
    c2.metric("마켓 잔량", f"{remaining}개")
    mod = c3.number_input("조작 수량", 1, 100, 1, key="adm_re_mod")

    ba, bb = st.columns(2)
    if ba.button("➕ 공급 늘리기", use_container_width=True):
        em["initial_stock"][sel_eid] = cur_limit + mod
        save_estate_market(em)
        market["news"] = f"🏗️ {info['name']} {mod}개 추가 분양 승인!"
        save_market(market); st.success("완료!"); st.rerun()
    if bb.button("➖ 공급 줄이기", use_container_width=True):
        em["initial_stock"][sel_eid] = max(owned + listed, cur_limit - mod)
        save_estate_market(em); st.success("완료!"); st.rerun()

    st.write("---")
    # 유저 부동산 압수
    st.markdown("#### 🔨 유저 부동산 강제 압수")
    if uid_list:
        re_target = st.selectbox("대상 유저", uid_list, key="adm_re_target")
        u_re = u_db[re_target].get("real_estate", {})
        if not u_re:
            st.info(f"{re_target}님은 부동산이 없습니다.")
        else:
            r1, r2, r3 = st.columns([3, 2, 2])
            re_eid = r1.selectbox("압수 매물", list(u_re.keys()),
                                   format_func=lambda x: f"{ESTATE_CONFIG[x]['icon']} {ESTATE_CONFIG[x]['name']} ({u_re[x]}채)",
                                   key="adm_re_seize_eid")
            re_cnt = r2.number_input("수량", 1, u_re[re_eid], 1, key="adm_re_seize_cnt")
            r3.write("")
            r3.write("")
            if r3.button("🔨 압수", use_container_width=True):
                u_db[re_target]["real_estate"][re_eid] -= re_cnt
                if u_db[re_target]["real_estate"][re_eid] <= 0:
                    del u_db[re_target]["real_estate"][re_eid]
                save_db(USERS_FILE, u_db)
                if re_target in em["owner_counts"]:
                    em["owner_counts"][re_target][re_eid] = max(
                        0, em["owner_counts"][re_target].get(re_eid, 0) - re_cnt
                    )
                save_estate_market(em)
                st.success("압수 완료!"); st.rerun()

    st.write("---")
    # 중고 매물 관리
    st.markdown("#### 🔄 유저 중고 매물 관리")
    listings = em.get("listings", [])
    if not listings:
        st.info("등록된 매물 없음")
    else:
        for li in listings:
            info = ESTATE_CONFIG.get(li["eid"], {})
            ca, cb = st.columns([5, 1])
            ca.markdown(f"{info.get('icon','')} **{info.get('name','?')}** | `{li['seller']}` | {format_korean_money(li['price'])}")
            if cb.button("삭제", key=f"adm_del_re_{li['id']}", use_container_width=True):
                em["listings"] = [x for x in em["listings"] if x["id"] != li["id"]]
                save_estate_market(em); st.rerun()

    st.write("---")
    if st.button("💣 부동산 전체 초기화", type="secondary", use_container_width=True):
        now = time.time()
        save_estate_market({"listings": [], "owner_counts": {},
                             "initial_stock": {eid: info["total_supply"] for eid, info in ESTATE_CONFIG.items()}})
        all_u = load_db(USERS_FILE, {})
        for uid in all_u:
            all_u[uid]["real_estate"] = {}
            all_u[uid]["rent_time"]   = now
        save_db(USERS_FILE, all_u)
        market["force_estate_reset"] = now
        save_market(market)
        st.success("전체 초기화 완료!"); st.rerun()


def _tab_board(market):
    st.markdown("### 💬 게시판 관리")
    all_c = load_db(COMMENTS_FILE, [])
    c1, c2 = st.columns([4, 1])
    c1.write(f"총 {len(all_c)}개 게시물")
    if c2.button("💣 전체 초기화", use_container_width=True):
        save_db(COMMENTS_FILE, []); st.rerun()
    st.write("---")
    for idx, c in reversed(list(enumerate(all_c[-50:]))):
        col_txt, col_btn = st.columns([6, 1])
        col_txt.markdown(
            f"<div style='background:rgba(255,255,255,0.05);padding:8px;border-radius:6px;'>"
            f"<b style='color:#00E5FF;'>{c['name']}</b>: {c['comment']} "
            f"<span style='color:#888;font-size:0.8rem;'>({c.get('time','')})</span></div>",
            unsafe_allow_html=True,
        )
        if col_btn.button("🗑️", key=f"del_board_{idx}", use_container_width=True):
            all_c.pop(idx)
            save_db(COMMENTS_FILE, all_c); st.rerun()


def _tab_global(u_db, market):
    # 에어드랍
    st.markdown("### 🕊️ 에어드랍")
    airdrop = st.number_input("지급 금액", 0, step=10_000_000, value=100_000_000, format="%d")
    if st.button("💸 전 우주 현금 살포", use_container_width=True):
        for u in u_db:
            if u != "admin": u_db[u]["cash"] += airdrop
        save_db(USERS_FILE, u_db)
        market["news"] = f"🕊️ [은총] 모두에게 {format_korean_money(airdrop)} 지급!"
        save_market(market); st.rerun()

    st.write("---")
    # 부유세
    st.markdown("### 🌪️ 부유세 강제 징수")
    tax_rate = st.slider("징수율 (%)", 1, 99, 10)
    if st.button("🌪️ 전 우주 징수 실행", use_container_width=True):
        for u in u_db:
            if u != "admin":
                u_db[u]["cash"] -= int(u_db[u]["cash"] * tax_rate / 100)
        save_db(USERS_FILE, u_db)
        market["news"] = f"🌪️ [분노] {tax_rate}% 부유세 징수 완료!"
        save_market(market); st.rerun()

    st.write("---")
    # 게시판 이용 정지
    st.markdown("### 🔇 게시판 이용 정지")
    uid_list = [u for u in u_db if u != "admin"]
    ban_t = st.selectbox("정지 유저", uid_list, key="ban_target")
    b1, b2 = st.columns(2)
    if b1.button("🔇 정지 + 글 삭제", use_container_width=True):
        all_c = load_db(COMMENTS_FILE, [])
        all_c = [c for c in all_c if c["name"] != ban_t]
        save_db(COMMENTS_FILE, all_c)
        market.setdefault("board_banned", [])
        if ban_t not in market["board_banned"]:
            market["board_banned"].append(ban_t)
        save_market(market); st.success("완료!"); st.rerun()
    if b2.button("🔓 정지 해제", use_container_width=True):
        if ban_t in market.get("board_banned", []):
            market["board_banned"].remove(ban_t)
            save_market(market); st.success("해제!"); st.rerun()

    st.write("---")
    # 공지사항
    st.markdown("### 📢 서버 공지")
    msg_text  = st.text_area("공지 내용", value=market.get("admin_msg", ""), height=70)
    msg_color = st.color_picker("색상", value=market.get("admin_color", "#FF4B4B"))
    n1, n2 = st.columns(2)
    if n1.button("📣 공지 발령", use_container_width=True):
        market["admin_msg"] = msg_text; market["admin_color"] = msg_color
        save_market(market); st.success("완료!")
    if n2.button("🗑️ 공지 삭제", use_container_width=True):
        market["admin_msg"] = ""
        save_market(market); st.success("완료!")

    st.write("---")
    # 클랜 강제 해산
    st.markdown("### 🏰 클랜 강제 해산")
    clans = load_clan_db()
    if clans:
        clan_del = st.selectbox("해산 클랜", list(clans.keys()),
                                 format_func=lambda n: f"{clans[n]['icon']} {n} ({len(clans[n]['members'])}명)")
        cd1, cd2 = st.columns(2)
        if cd1.button("💣 강제 해산", use_container_width=True, type="secondary"):
            del clans[clan_del]; save_clan_db(clans)
            market["news"] = f"💣 [{clan_del}] 클랜 강제 해산!"
            save_market(market); st.success("완료!"); st.rerun()
        if cd2.button("🏦 은행 몰수", use_container_width=True):
            clans[clan_del]["bank"] = 0; save_clan_db(clans)
            st.success("몰수 완료!"); st.rerun()


def _tab_stock(market):
    st.markdown("### 📈 종목별 가격 조작")
    for s in STOCK_CONFIG:
        cur_p = market["stock_data"][s["id"]]["price"]
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        c1.write(f"{s['icon']} {s['name']}")
        c2.write(f"현재: ₩{cur_p:,}")
        if c3.button("🚀 +50%", key=f"up_{s['id']}"):
            market["stock_data"][s["id"]]["price"] = int(cur_p * 1.5)
            market["news"] = f"🚀 [조작] {s['name']} 급등!"
            save_market(market); st.rerun()
        if c4.button("📉 -30%", key=f"dn_{s['id']}"):
            market["stock_data"][s["id"]]["price"] = max(1000, int(cur_p * 0.7))
            market["news"] = f"💣 [조작] {s['name']} 폭락!"
            save_market(market); st.rerun()

    st.write("---")
    ca, cb = st.columns(2)
    if ca.button("🔥 전종목 +50%", use_container_width=True):
        for s in STOCK_CONFIG:
            market["stock_data"][s["id"]]["price"] = int(market["stock_data"][s["id"]]["price"] * 1.5)
        market["news"] = "🔥 전 종목 폭등!!"
        save_market(market); st.rerun()
    if cb.button("💣 전종목 -40%", use_container_width=True):
        for s in STOCK_CONFIG:
            market["stock_data"][s["id"]]["price"] = max(1000, int(market["stock_data"][s["id"]]["price"] * 0.6))
        market["news"] = "💣 전 종목 폭락!!"
        save_market(market); st.rerun()

    st.write("---")
    st.markdown("### 🎰 로또 강제 조작")
    st.metric("현재 로또 풀", format_korean_money(market.get("lotto_pool", 0)))
    lc1, lc2 = st.columns(2)
    with lc1:
        ladd = st.number_input("추가 금액", 0, step=1_000_000_000, value=1_000_000_000, format="%d")
        if st.button("💰 풀 금액 추가", use_container_width=True):
            market["lotto_pool"] += ladd; save_market(market); st.rerun()
    with lc2:
        if st.button("🎊 즉시 강제 추첨", use_container_width=True):
            market["lotto_last_draw"] = 0; save_market(market); st.success("다음 렌더에 추첨!"); st.rerun()
        if st.button("🗑️ 티켓 전체 초기화", use_container_width=True, type="secondary"):
            market["lotto_tickets"] = {}; market["lotto_pool"] = 5_000_000_000
            save_market(market); st.rerun()


def _tab_overview(u_db, market):
    total = len([u for u in u_db if u != "admin"])
    st.markdown(f"### 📈 총 유저: **{total}명**")
    rows = [
        {"ID": uid, "칭호": ud.get("equipped_title", ""),
         "현금": format_korean_money(ud.get("cash", 0)),
         "대출": format_korean_money(ud.get("loan", 0)),
         "무기": f"+{ud.get('weapon_level', 0)}강"}
        for uid, ud in u_db.items() if uid != "admin"
    ]
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.write("---")
    st.markdown("### 👑 히든 칭호 발급 현황")
    hidden = market.get("hidden_titles", {})
    if not hidden:
        st.info("발급된 히든 칭호 없음")
    else:
        for tid, owner in list(hidden.items()):
            hc1, hc2 = st.columns([4, 1])
            hc1.markdown(f"**{tid}** → `{owner}`")
            if hc2.button("🔄 초기화", key=f"reset_h_{tid}", use_container_width=True):
                del market["hidden_titles"][tid]; save_market(market); st.rerun()


def _tab_logs():
    if st.button("🔄 새로고침", use_container_width=True):
        st.rerun()
    all_logs = load_db(TXLOG_FILE, {})
    combined = []
    for uid, ulogs in all_logs.items():
        for log in ulogs:
            combined.append({**log, "uid": uid})
    combined.sort(key=lambda x: x["time"], reverse=True)
    for log in combined[:150]:
        amt   = log["amount"]
        color = "#FF4B4B" if amt > 0 else "#4B9EFF"
        sign  = "+" if amt > 0 else ""
        st.markdown(
            f"<div style='font-size:0.85rem;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.05);'>"
            f"<span style='color:#777;'>[{log['time']}]</span> "
            f"<b style='color:#00E5FF;'>{log['uid']}</b> "
            f"<span style='color:#94A3B8;'>{log['desc']}</span> "
            f"<b style='color:{color};'>({sign}{format_korean_money(amt)})</b></div>",
            unsafe_allow_html=True,
        )


def _tab_garage(u_db, uid_list, market):
    st.markdown("### 🏎️ 유저 차고지 통제")
    if not uid_list:
        st.info("유저 없음")
        return
    car_target = st.selectbox("대상 유저", uid_list, key="adm_car_target")
    garage = u_db[car_target].get("garage", {"cars": {}, "active_tier": None})
    cars = garage.get("cars", {})

    if not cars:
        st.info(f"{car_target}님은 차량이 없습니다.")
        if st.button("🚀 최고급 하이퍼카 하사 (풀강)", use_container_width=True):
            u_db[car_target]["garage"] = {
                "cars": {"3": {"engine_lv": 5, "suspension_lv": 5, "bumper_lv": 5, "needs_repair": False}},
                "active_tier": "3",
            }
            save_db(USERS_FILE, u_db); st.success("하사 완료!"); st.rerun()
        return

    tier_names = {c["tier"]: c["name"] for c in CAR_TIERS}
    sel_t = st.selectbox("조작할 차량", list(cars.keys()),
                          format_func=lambda t: f"Tier {t} — {tier_names.get(t, '?')}")
    parts = cars[sel_t]

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**튜닝:** 엔진{parts.get('engine_lv',0)} / 서스{parts.get('suspension_lv',0)} / 범퍼{parts.get('bumper_lv',0)}")
        st.markdown(f"**파손:** {'🚨 파손' if parts.get('needs_repair') else '✅ 정상'}")
    with c2:
        if st.button("💥 강제 후방 추돌", use_container_width=True):
            u_db[car_target]["garage"]["cars"][sel_t]["needs_repair"] = True
            save_db(USERS_FILE, u_db)
            market["news"] = f"🚨 {car_target}님 차량 대파!"
            save_market(market); st.rerun()
        if st.button("🔧 무상 수리", use_container_width=True):
            u_db[car_target]["garage"]["cars"][sel_t]["needs_repair"] = False
            save_db(USERS_FILE, u_db); st.success("수리 완료!"); st.rerun()
        if st.button("🗑️ 폐차", use_container_width=True, type="secondary"):
            del u_db[car_target]["garage"]["cars"][sel_t]
            remaining = list(u_db[car_target]["garage"]["cars"].keys())
            u_db[car_target]["garage"]["active_tier"] = remaining[0] if remaining else None
            save_db(USERS_FILE, u_db); st.rerun()


def _tab_season(market):
    st.markdown("### 🏆 시즌 수동 통제")
    cur_sn = market.get("season_num", 1)
    start_ts = market.get("season_start", time.time())
    end_ts   = market.get("season_end", time.time() + 30 * 86400)

    c1, c2, c3 = st.columns(3)
    new_sn = c1.number_input("시즌 번호", 1, value=int(cur_sn), key="adm_sn")
    s_date = c2.date_input("시작일", datetime.fromtimestamp(start_ts, KST))
    s_time = c2.time_input("시작시각", datetime.fromtimestamp(start_ts, KST))
    e_date = c3.date_input("종료일", datetime.fromtimestamp(end_ts, KST))
    e_time = c3.time_input("종료시각", datetime.fromtimestamp(end_ts, KST))

    new_start = datetime.combine(s_date, s_time, tzinfo=KST).timestamp()
    new_end   = datetime.combine(e_date, e_time, tzinfo=KST).timestamp()

    if st.button("💾 시즌 설정 저장", use_container_width=True):
        market.update({"season_num": new_sn, "season_start": new_start, "season_end": new_end})
        save_market(market); st.success("저장 완료!"); st.rerun()

    st.write("---")
    st.markdown("#### 💣 수동 경제 리셋")
    st.caption("⚠️ 전 유저 현금/주식/코인/부동산 몰수 후 5억 지급")
    confirm = st.checkbox("경제 리셋에 동의합니다.")
    if st.button("⚡ 즉시 경제 리셋", use_container_width=True, type="secondary", disabled=not confirm):
        from utils.sync import get_net_worth as gnw
        all_u = load_db(USERS_FILE, {})
        now = time.time()
        rank_list = [(uid, gnw(uid, market)) for uid in all_u if uid != "admin"]
        rank_list.sort(key=lambda x: x[1], reverse=True)
        sn = market.get("season_num", 1)
        titles = [f"🥇 [시즌{sn}] 우승자", f"🥈 [시즌{sn}] 준우승", f"🥉 [시즌{sn}] 3위"]
        record = {}
        for i, (uid, _) in enumerate(rank_list[:3]):
            record[f"rank{i+1}"] = uid
            if uid in all_u:
                all_u[uid].setdefault("inventory", [])
                if titles[i] not in all_u[uid]["inventory"]:
                    all_u[uid]["inventory"].append(titles[i])
                all_u[uid]["equipped_title"] = titles[i]
        for uid in all_u:
            if uid == "admin": continue
            all_u[uid].update({"cash": 500_000_000, "portfolio": {}, "crypto_portfolio": {},
                                "real_estate": {}, "loan": 0, "daily_quests": {},
                                "loan_time": now, "rent_time": now, "weapon_level": 0,
                                "bulk_trade_count": 0, "garage": {"cars": {}, "active_tier": None}})
        save_db(USERS_FILE, all_u)
        save_estate_market({"listings": [], "owner_counts": {},
                             "initial_stock": {eid: i["total_supply"] for eid, i in ESTATE_CONFIG.items()}})
        market.setdefault("season_records", {})[str(sn)] = record
        market.update({"season_num": sn + 1, "season_start": now, "season_end": now + 30 * 86400,
                       "season_ending": False, "lotto_pool": 5_000_000_000, "lotto_tickets": {},
                       "force_estate_reset": now,
                       "news": f"🏆 시즌{sn} 종료! {rank_list[0][0] if rank_list else '?'}님 우승!"})
        save_market(market)
        st.balloons(); st.success("리셋 완료!"); st.rerun()

    st.write("---")
    st.markdown("#### 📜 시즌 역사관")
    for sn_k, res in sorted(market.get("season_records", {}).items(), key=lambda x: int(x[0]), reverse=True):
        with st.expander(f"🌌 시즌 {sn_k} 기록"):
            for r, label in [("rank1","🥇"), ("rank2","🥈"), ("rank3","🥉")]:
                st.write(f"{label} {res.get(r, '-')}")


def _tab_messages():
    st.markdown("### 👁️ 전지적 쪽지 감시")
    all_msgs = load_db(MESSAGES_FILE, {})
    if not all_msgs:
        st.info("쪽지 데이터 없음")
        return

    sub = st.tabs(["🔍 유저별", "📜 전체 타임라인", "💣 초기화"])
    with sub[0]:
        target = st.selectbox("유저", list(all_msgs.keys()), key="adm_msg_u")
        u_data = all_msgs.get(target, {})
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**📥 {target} 받은 쪽지**")
            for m in reversed(u_data.get("inbox", [])[-20:]):
                st.markdown(f"<div style='font-size:0.82rem;padding:6px;background:rgba(255,255,255,0.03);border-radius:5px;margin:3px 0;'>"
                            f"<b style='color:#00E5FF;'>{m['sender']}</b>: {m['content']} "
                            f"<span style='color:#777;'>({m['time']})</span></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"**📤 {target} 보낸 쪽지**")
            for m in reversed(u_data.get("outbox", [])[-20:]):
                st.markdown(f"<div style='font-size:0.82rem;padding:6px;background:rgba(255,255,255,0.03);border-radius:5px;margin:3px 0;'>"
                            f"→ <b style='color:#FFD600;'>{m['receiver']}</b>: {m['content']} "
                            f"<span style='color:#777;'>({m['time']})</span></div>", unsafe_allow_html=True)
    with sub[1]:
        logs = []
        for uid, data in all_msgs.items():
            for m in data.get("outbox", []):
                logs.append({"time": m["time"], "from": uid, "to": m["receiver"], "content": m["content"]})
        logs.sort(key=lambda x: x["time"], reverse=True)
        for l in logs[:100]:
            st.markdown(f"<div style='font-size:0.85rem;border-bottom:1px solid rgba(255,255,255,0.05);padding:4px 0;'>"
                        f"<span style='color:#777;'>[{l['time']}]</span> "
                        f"<b style='color:#00E5FF;'>{l['from']}</b> → "
                        f"<b style='color:#FFD600;'>{l['to']}</b>: {l['content']}</div>", unsafe_allow_html=True)
    with sub[2]:
        if st.button("💣 전체 쪽지 DB 초기화", use_container_width=True, type="secondary"):
            save_db(MESSAGES_FILE, {})
            st.success("소멸 완료!"); st.rerun()
