# pages/games/gacha.py
import streamlit as st
import random
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import log_tx, save_market, atomic_deduct_cash

GACHA_TICKET_PRICE = 50_000_000
PITY_THRESHOLD     = 80   # 80회 내 전설 1개 보장

# 가챠 풀 (전체 가중치 합: 1000)
GACHA_POOL = [
    # --- 💎 전설 (총합 10 = 1.0%) ---
    {"grade": "💎 전설", "name": "👑 [시즌한정] 우주의 도박꾼", "weight": 2, "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 운영자를 노린다", "weight": 2, "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 갓생러",         "weight": 2, "type": "title"},
    {"grade": "💎 전설", "name": "👑 건물주 위의 조물주",       "weight": 2, "type": "title"},
    {"grade": "💎 전설", "name": "👑 인간 도파민",             "weight": 2, "type": "title"},

    # --- 🔴 영웅 (총합 50 = 5.0%) ---
    {"grade": "🔴 영웅", "name": "⚔️ 전장의 지배자",           "weight": 10, "type": "title"},
    {"grade": "🔴 영웅", "name": "🚀 화성 갈끄니까",           "weight": 10, "type": "title"},
    {"grade": "🔴 영웅", "name": "📈 떡상의 화신",             "weight": 10, "type": "title"},
    {"grade": "🔴 영웅", "name": "💎 다이아몬드 손",           "weight": 10, "type": "title"},
    {"grade": "🔴 영웅", "name": "🏎️ 최고급 슈퍼카 열쇠",       "weight": 10, "type": "item"},

    # --- 🔵 희귀 (총합 140 = 14.0%) ---
    {"grade": "🔵 희귀", "name": "🎖️ 행운의 사나이",           "weight": 28, "type": "title"},
    {"grade": "🔵 희귀", "name": "💼 여의도 펀드매니저",       "weight": 28, "type": "title"},
    {"grade": "🔵 희귀", "name": "🏦 은행 VIP 고객",           "weight": 28, "type": "title"},
    {"grade": "🔵 희귀", "name": "🐷 황금 돼지 저금통",         "weight": 28, "type": "item"},
    {"grade": "🔵 희귀", "name": "🪙 비트코인 기념주화",       "weight": 28, "type": "item"},

    # --- 🟢 일반 (총합 300 = 30.0%) ---
    {"grade": "🟢 일반", "name": "🍀 행운의 클로버",           "weight": 60, "type": "title"},
    {"grade": "🟢 일반", "name": "🐜 영차영차 개미",           "weight": 60, "type": "title"},
    {"grade": "🟢 일반", "name": "🍜 뜨끈한 든든 국밥",         "weight": 60, "type": "item"},
    {"grade": "🟢 일반", "name": "🎟️ 로또 5등 당첨금",         "weight": 60, "type": "item"},
    {"grade": "🟢 일반", "name": "☕ 브랜드 커피 쿠폰",         "weight": 60, "type": "item"},

    # --- 🟤 꽝 (총합 500 = 50.0%) ---
    {"grade": "🟤 꽝",   "name": "🛡️ 파괴방지권",             "weight": 100, "type": "item"},
    {"grade": "🟤 꽝",   "name": "🥫 빈 깡통",                "weight": 100, "type": "item"},
    {"grade": "🟤 꽝",   "name": "🧾 찢어진 영수증",          "weight": 100, "type": "item"},
    {"grade": "🟤 꽝",   "name": "📉 상장폐지된 주식",        "weight": 100, "type": "item"},
    {"grade": "🟤 꽝",   "name": "🌡️ 한강물 온도계",          "weight": 100, "type": "item"},
]

# 전설 아이템 인덱스 목록 (pity 보장 뽑기용)
LEGENDARY_ITEMS = [i for i, item in enumerate(GACHA_POOL) if "전설" in item['grade']]


def _pull_one(pity: int) -> tuple[dict, int]:
    """
    단일 뽑기. pity는 전설 미획득 연속 횟수.
    pity+1 >= PITY_THRESHOLD 이면 전설 강제 지급.
    반환: (item, new_pity)
    """
    pity += 1

    if pity >= PITY_THRESHOLD:
        # 천장 도달 — 랜덤 전설 강제 지급
        idx = random.choice(LEGENDARY_ITEMS)
        return GACHA_POOL[idx], 0  # pity 리셋

    weights = [item['weight'] for item in GACHA_POOL]
    idx     = random.choices(range(len(GACHA_POOL)), weights=weights, k=1)[0]
    item    = GACHA_POOL[idx]

    new_pity = 0 if "전설" in item['grade'] else pity
    return item, new_pity


def render(market, nw):
    st.title("🎴 가챠 뽑기")

    uid   = st.session_state.logged_in_user
    pity  = st.session_state.get('gacha_pity', 0)
    pulls_to_pity = PITY_THRESHOLD - pity

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(180,0,255,0.1),rgba(0,0,180,0.1));
         border:2px solid rgba(180,0,255,0.4);border-radius:16px;padding:20px;text-align:center;margin-bottom:16px;'>
      <div style='font-size:2rem;'>🎴</div>
      <div style='font-size:1.3rem;font-weight:900;color:#FF00FF;margin-top:8px;'>시즌 {market.get('season_num',1)} 한정 가챠</div>
      <div style='color:#888;font-size:0.85rem;margin-top:6px;'>1회당 {format_korean_money(GACHA_TICKET_PRICE)} | 전설 칭호 획득 시 서버 전체 공지!</div>
      <div style='margin-top:10px;background:rgba(255,215,0,0.12);border:1px solid rgba(255,215,0,0.4);border-radius:8px;padding:8px 14px;display:inline-block;'>
        <span style='color:#FFD600;font-weight:900;'>⭐ 천장 보정: {pulls_to_pity}회 이내 전설 100% 보장</span>
        <div style='background:rgba(255,215,0,0.2);border-radius:4px;height:6px;margin-top:6px;'>
          <div style='background:#FFD600;border-radius:4px;height:6px;width:{min(100, pity/PITY_THRESHOLD*100):.0f}%;'></div>
        </div>
        <div style='color:#aaa;font-size:0.75rem;margin-top:4px;'>{pity} / {PITY_THRESHOLD} 누적</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📋 아이템 확률표")
    grade_summary = {}
    for item in GACHA_POOL:
        g = item['grade']
        grade_summary[g] = grade_summary.get(g, 0) + item['weight']
    total_weight = sum(grade_summary.values())

    rows_html = "<table class='stock-table'><thead><tr><th>등급</th><th style='text-align:right;'>기본 확률</th></tr></thead><tbody>"
    for grade, w in grade_summary.items():
        pct = w / total_weight * 100
        rows_html += f"<tr><td>{grade}</td><td style='text-align:right;color:#FFD600;font-weight:900;'>{pct:.1f}%</td></tr>"
    rows_html += f"<tr><td colspan='2' style='color:#FFD600;font-size:0.8rem;'>⭐ {PITY_THRESHOLD}회 내 전설 1개 100% 보장 (천장)</td></tr>"
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
            # 원자적 차감
            if not atomic_deduct_cash(uid, total_cost):
                st.error("잔액 부족! (DB 검증 실패)")
                st.stop()
            st.session_state.global_cash -= total_cost

            got_legendary = False
            result_html   = ""
            current_pity  = pity

            for _ in range(pull_count):
                item, current_pity = _pull_one(current_pity)

                grade_col = ("#FFD600" if "전설" in item['grade']
                             else "#00E5FF" if "영웅" in item['grade']
                             else "#AA88FF" if "희귀" in item['grade']
                             else "#00FF88" if "일반" in item['grade']
                             else "#888")

                pity_badge = " ✨<b style='color:#FFD600;'>천장 보정!</b>" if current_pity == 0 and "전설" in item['grade'] else ""

                if item['name'] not in st.session_state.inventory:
                    st.session_state.inventory.append(item['name'])

                result_html += (f"<div style='background:rgba(255,255,255,0.04);border:1px solid {grade_col}44;"
                                f"border-radius:10px;padding:12px 16px;margin:6px 0;display:flex;"
                                f"justify-content:space-between;align-items:center;'>"
                                f"<span style='color:{grade_col};font-weight:900;'>{item['grade']}{pity_badge}</span>"
                                f"<span style='color:#E2E8F0;font-weight:900;'>{item['name']}</span></div>")

                if "전설" in item['grade']:
                    got_legendary = True
                    market['news'] = f"🎴 [가챠 대박] {uid}님이 전설 [{item['name']}] 획득!!"
                    save_market(market)

            # pity 저장
            st.session_state.gacha_pity = current_pity

            st.markdown(f"<div style='margin:16px 0;'>{result_html}</div>", unsafe_allow_html=True)
            log_tx(uid, "가챠", f"가챠 {pull_count}회 뽑기", -total_cost)
            sync_user_data()

            if got_legendary:
                st.balloons()
                st.success("🎉 전설 등급 획득! 칭호 상점에서 장착하세요!")
            else:
                st.success(f"✅ 뽑기 완료! 칭호 상점에서 장착할 수 있습니다. (천장까지 {PITY_THRESHOLD - current_pity}회)")
