# pages/games/gacha.py
import streamlit as st
import random
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import log_tx, save_market

GACHA_TICKET_PRICE = 50_000_000
GACHA_POOL = [
    {"grade": "💎 전설", "name": "👑 [시즌한정] 우주의 도박꾼", "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 운영자를 노린다", "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 갓생러",         "weight": 2,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 전장의 지배자",            "weight": 4,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 행운의 사나이",            "weight": 8,  "type": "title"},
    {"grade": "🟢 일반", "name": "🍀 행운의 클로버",            "weight": 25, "type": "title"},
    {"grade": "🟤 꽝",   "name": "파괴방지권",                  "weight": 30, "type": "item"},
    {"grade": "🟤 꽝",   "name": "빈 깡통",                     "weight": 30, "type": "item"},
] # (기존 코드에서 일부만 발췌했습니다. 필요시 원본 풀을 채워주세요!)

def render(market, nw):
    st.title("🎴 가챠 뽑기")
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(180,0,255,0.1),rgba(0,0,180,0.1));
         border:2px solid rgba(180,0,255,0.4);border-radius:16px;padding:20px;text-align:center;margin-bottom:16px;'>
      <div style='font-size:2rem;'>🎴</div>
      <div style='font-size:1.3rem;font-weight:900;color:#FF00FF;margin-top:8px;'>시즌 {market.get('season_num',1)} 한정 가챠</div>
      <div style='color:#888;font-size:0.85rem;margin-top:6px;'>1회당 {format_korean_money(GACHA_TICKET_PRICE)} | 전설 칭호 획득 시 서버 전체 공지!</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 아이템 확률표")
    grade_summary = {}
    for item in GACHA_POOL:
        g = item['grade']
        grade_summary[g] = grade_summary.get(g, 0) + item['weight']
    total_weight = sum(grade_summary.values())

    rows_html = "<table class='stock-table'><thead><tr><th>등급</th><th style='text-align:right;'>확률</th></tr></thead><tbody>"
    for grade, w in grade_summary.items():
        pct = w / total_weight * 100
        rows_html += f"<tr><td>{grade}</td><td style='text-align:right;color:#FFD600;font-weight:900;'>{pct:.1f}%</td></tr>"
    rows_html += "</tbody></table>"
    st.markdown(rows_html, unsafe_allow_html=True)
    st.write("---")

    pull_count = st.selectbox("뽑기 횟수", [1, 5, 10], format_func=lambda x: f"{x}회 ({format_korean_money(GACHA_TICKET_PRICE * x)})")
    total_cost = GACHA_TICKET_PRICE * pull_count
    st.caption(f"총 비용: {format_korean_money(total_cost)}")

    cd_gacha = cooldown_remaining("gacha_pull", 3.0)
    if cd_gacha > 0:
        st.warning(f"⏱️ 쿨다운 {cd_gacha:.1f}초")
    elif st.button(f"🎴 {pull_count}회 뽑기!", use_container_width=True):
        if st.session_state.global_cash < total_cost:
            st.error("잔액 부족!")
        else:
            set_cooldown("gacha_pull")
            st.session_state.global_cash -= total_cost

            weights = [item['weight'] for item in GACHA_POOL]
            results = random.choices(range(len(GACHA_POOL)), weights=weights, k=pull_count)

            got_legendary = False
            result_html   = ""
            for idx in results:
                item = GACHA_POOL[idx]
                grade_col = "#FFD600" if "전설" in item['grade'] else "#00E5FF" if "희귀" in item['grade'] else "#00FF88" if "일반" in item['grade'] else "#888"
                if item['name'] not in st.session_state.inventory:
                    st.session_state.inventory.append(item['name'])

                result_html += f"<div style='background:rgba(255,255,255,0.04);border:1px solid {grade_col}44;border-radius:10px;padding:12px 16px;margin:6px 0;display:flex;justify-content:space-between;align-items:center;'><span style='color:{grade_col};font-weight:900;'>{item['grade']}</span><span style='color:#E2E8F0;font-weight:900;'>{item['name']}</span></div>"
                if "전설" in item['grade']:
                    got_legendary = True
                    market['news'] = f"🎴 [가챠 대박] {st.session_state.logged_in_user}님이 전설 [{item['name']}] 획득!!"
                    save_market(market)

            st.markdown(f"<div style='margin:16px 0;'>{result_html}</div>", unsafe_allow_html=True)
            log_tx(st.session_state.logged_in_user, "가챠", f"가챠 {pull_count}회 뽑기", -total_cost)
            sync_user_data()

            if got_legendary:
                st.balloons()
                st.success("🎉 전설 등급 획득! 칭호 상점에서 장착하세요!")
            else:
                st.success("✅ 뽑기 완료! 칭호 상점에서 장착할 수 있습니다.")