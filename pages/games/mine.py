# pages/games/mine.py
import streamlit as st
import random
from utils.config import MINE_ITEMS
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title
from utils.database import log_tx, save_market

def render(market, nw):
    st.title("⛏️ 효민 광산")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>곡괭이를 들어 광물을 캐세요!</div>", unsafe_allow_html=True)

    cash = st.session_state.global_cash
    if cash < 10_000_000:
        mine_tier, mine_label, mine_color = 0, "🪨 초보 광산",  "#888"
    elif cash < 100_000_000:
        mine_tier, mine_label, mine_color = 1, "⛏️ 견습 광산",  "#CD7F32"
    elif cash < 1_000_000_000:
        mine_tier, mine_label, mine_color = 2, "🥈 숙련 광산",  "#C0C0C0"
    else:
        mine_tier, mine_label, mine_color = 3, "🥇 마스터 광산","#FFD600"

    tier_bonus = mine_tier * 0.005

    st.markdown(f"""
<div style='background: linear-gradient(135deg, rgba(139,69,19,0.15), rgba(0,0,0,0.3)); border: 1px solid rgba(205,127,50,0.3); border-radius: 14px; padding: 20px; text-align: center;'>
  <div style='font-size:2rem;margin-bottom:8px;'>⛏️</div>
  <div style='font-size:1.2rem;font-weight:900;color:{mine_color};'>{mine_label}</div>
  <div style='color:#888;font-size:0.82rem;margin-top:6px;'>광산 티어가 높을수록 희귀 광물 확률 ↑</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### 📋 광물 목록")
    rows_html = "<table class='stock-table'><thead><tr><th>광물</th><th style='text-align:right;'>가치</th><th style='text-align:right;'>기본 확률</th></tr></thead><tbody>"
    for item in MINE_ITEMS:
        adj_prob = min(item['prob'] + tier_bonus, 0.99)
        rows_html += f"<tr><td>{item['icon']} {item['name']}</td><td style='text-align:right;color:#FFD600;font-weight:900;'>{format_korean_money(item['value'])}</td><td style='text-align:right;color:#888;'>{adj_prob*100:.1f}%</td></tr>"
    rows_html += "</tbody></table>"
    st.markdown(rows_html, unsafe_allow_html=True)
    st.write("")

    def do_mine(k):
        items_adj   = []
        weights_adj = []
        for item in MINE_ITEMS:
            items_adj.append(item)
            rarity_mult = 1.0 + (tier_bonus / item['prob']) * 0.5
            weights_adj.append(item['prob'] * rarity_mult)
        return random.choices(items_adj, weights=weights_adj, k=k)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        cd_mine1 = cooldown_remaining("mine_single", 1.5)
        if cd_mine1 > 0:
            st.warning(f"⏱️ 쿨다운 {cd_mine1:.1f}초")
        elif st.button("⛏️ 한 번 캐기!", use_container_width=True):
            set_cooldown("mine_single")
            result = do_mine(1)[0]
            st.session_state.global_cash += result['value']
            log_tx(st.session_state.logged_in_user, "광산", f"{result['name']} 채굴", result['value'])
            sync_user_data()
            if result['name'] in ["다이아몬드", "전설의 원석"]:
                if result['name'] == "전설의 원석": claim_hidden_title("first_legendary_ore", "👑 [유일무이] 럭키가이")
                st.balloons()
                st.success(f"✨ {result['icon']} **{result['name']}** 발견!! +{format_korean_money(result['value'])}")
                market['news'] = f"⛏️ [{st.session_state.logged_in_user}] 광산에서 {result['name']} 채굴 대박!"
                save_market(market)
            elif result['name'] in ["루비", "사파이어"]:
                st.success(f"🎉 {result['icon']} {result['name']} 발견! +{format_korean_money(result['value'])}")
            else:
                st.info(f"{result['icon']} {result['name']} 채굴. +{format_korean_money(result['value'])}")

    st.write("")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        cd_mine10 = cooldown_remaining("mine_ten", 4.0)
        if cd_mine10 > 0:
            st.warning(f"⏱️ 10연속 쿨다운 {cd_mine10:.1f}초")
        elif st.button("⛏️⛏️ 10회 연속 채굴", use_container_width=True):
            set_cooldown("mine_ten")
            results = do_mine(10)
            total   = sum(r['value'] for r in results)
            st.session_state.global_cash += total
            log_tx(st.session_state.logged_in_user, "광산", "10회 연속 채굴", total)
            sync_user_data()
            summary = {}
            for r in results:
                summary[r['name']] = summary.get(r['name'], 0) + 1
            result_str = " | ".join(f"{next(m['icon'] for m in MINE_ITEMS if m['name']==n)} {n} x{cnt}" for n, cnt in summary.items())
            st.success(f"⛏️ 10회 채굴 완료! +{format_korean_money(total)}\n{result_str}")