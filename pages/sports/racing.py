# pages/sports/racing.py
import streamlit as st
import random
import time
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx

def render(market, nw):
    st.title("🏎️ 하이퍼카 레이싱")
    st.caption("배당률이 높을수록 우승 확률은 낮지만 당첨 시 고수익! 내 차를 출전시키면 튜닝 스탯이 반영됩니다.")

    CARS = [
        {"name": "부가티 시론 SS",        "emoji": "🏎️", "odds": 20.0, "spd": (0, 15),  "color": "#FF0066"},
        {"name": "람보르기니 레부엘토",    "emoji": "🐂",  "odds": 12.0, "spd": (1, 14),  "color": "#FF6600"},
        {"name": "페라리 SF90 XX",         "emoji": "🐎",  "odds": 8.0,  "spd": (1, 13),  "color": "#FF2200"},
        {"name": "맥라렌 P1 GTR",          "emoji": "🚀",  "odds": 6.0,  "spd": (2, 12),  "color": "#FF9900"},
        {"name": "포르쉐 918 스파이더",    "emoji": "⚡",  "odds": 4.0,  "spd": (2, 11),  "color": "#FFCC00"},
        {"name": "테슬라 로드스터 2",       "emoji": "⚡",  "odds": 2.5,  "spd": (3, 10),  "color": "#00FF88"},
        {"name": "토요타 GR010 하이브리드","emoji": "🏁",  "odds": 1.8,  "spd": (3,  9),  "color": "#00CCFF"},
    ]

    uid = st.session_state.logged_in_user
    _tmp = load_db(USERS_FILE, {})
    my_garage = _tmp.get(uid, {}).get('garage', {})
    active_t = my_garage.get('active_tier')

    if active_t is not None and active_t in my_garage.get('cars', {}):
        parts = my_garage['cars'][active_t]
        if parts.get('needs_repair'):
            st.warning("🚨 현재 선택된 내 차량이 파손된 상태라 레이싱에 출전할 수 없습니다. 차고지에서 수리하세요!")
        else:
            CAR_TIERS_INFO = [
                {"name": "박스카", "emoji": "🚙", "color": "#A0A0A0", "base_spd": (1, 10), "base_odds": 15.0},
                {"name": "스포츠 세단", "emoji": "🚗", "color": "#00E5FF", "base_spd": (2, 12), "base_odds": 8.0},
                {"name": "럭셔리 하이퍼카", "emoji": "🏎️", "color": "#FFD600", "base_spd": (3, 13), "base_odds": 4.0},
                {"name": "은하철도", "emoji": "🚀", "color": "#FF00FF", "base_spd": (4, 15), "base_odds": 1.5}
            ]
            c_info = CAR_TIERS_INFO[int(active_t)]
            total_lv = parts['engine_lv'] + parts['suspension_lv'] + parts['bumper_lv']
            
            bonus_spd = total_lv // 2
            calc_odds = round(max(1.1, c_info['base_odds'] - (total_lv * 0.2)), 1)

            my_custom_car = {
                "name": f"[내 차] {c_info['name']} (+{total_lv}강)",
                "emoji": c_info['emoji'], "odds": calc_odds,
                "spd": (c_info['base_spd'][0], c_info['base_spd'][1] + bonus_spd),
                "color": c_info['color'], "is_mine": True
            }
            CARS.insert(0, my_custom_car)

    car_names = [f"{c['emoji']} {c['name']} ({c['odds']}배)" for c in CARS]
    sel_idx   = st.selectbox("베팅 및 출전 차량 선택", range(len(CARS)), format_func=lambda i: car_names[i])
    selected_car = CARS[sel_idx]
    
    bet_amt   = st.number_input("베팅 금액 (원)", min_value=10_000, step=10_000, value=100_000)
    st.caption(f"우승 시 예상 수령액: {format_korean_money(int(bet_amt * selected_car['odds']))}")

    cd_race = cooldown_remaining("race_start", 8.0)
    if cd_race > 0:
        st.warning(f"⏱️ 레이스 쿨다운 {cd_race:.1f}초")
    elif st.button("🏁 레이스 시작!", use_container_width=True):
        if st.session_state.global_cash < bet_amt:
            st.error("잔액 부족!")
        else:
            set_cooldown("race_start")
            st.session_state.global_cash -= bet_amt
            positions = {c['name']: 0.0 for c in CARS}
            winner    = None
            bars      = {}
            st.markdown("### 🏁 레이스 진행")
            for c in CARS:
                bars[c['name']] = st.progress(0, text=f"{c['emoji']} {c['name']}")

            while winner is None:
                time.sleep(0.12)
                for c in CARS:
                    base_move = random.randint(c['spd'][0], c['spd'][1])
                    if random.random() < 0.05: base_move += 15 # 부스터
                    positions[c['name']] = min(100, positions[c['name']] + base_move)
                    
                    rank     = sorted(positions.items(), key=lambda x: x[1], reverse=True)
                    pos_num  = next(i+1 for i, (n, _) in enumerate(rank) if n == c['name'])
                    bars[c['name']].progress(positions[c['name']]/100, text=f"{c['emoji']} {c['name']} {pos_num}위 | {positions[c['name']]:.0f}%")
                    if positions[c['name']] >= 100 and winner is None:
                        winner = c['name']

            st.write("---")
            winner_car = next(c for c in CARS if c['name'] == winner)
            st.markdown(f"<div style='text-align:center;font-family:Orbitron,monospace;font-size:1.8rem;color:{winner_car['color']};font-weight:900;padding:20px;'>🏆 {winner_car['emoji']} {winner} 우승!</div>", unsafe_allow_html=True)

            if winner == selected_car['name']:
                prize = int(bet_amt * selected_car['odds'])
                st.session_state.global_cash += prize
                log_tx(st.session_state.logged_in_user, "레이싱", f"{selected_car['name']} 승리", prize - bet_amt)
                st.success(f"🎉 베팅 성공! +{format_korean_money(prize)}"); st.balloons()
                if selected_car['odds'] >= 20.0: claim_hidden_title("first_bugatti", "👑 [유일무이] 레이싱 붉은 혜성")
            else:
                log_tx(st.session_state.logged_in_user, "레이싱", f"{selected_car['name']} 패배", -bet_amt)
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")
                
                if selected_car.get('is_mine') and random.random() < 0.1:
                    u_db = load_db(USERS_FILE, {})
                    u_db[uid]['garage']['cars'][active_t]['needs_repair'] = True
                    save_db(USERS_FILE, u_db)
                    st.error("🚨 쾅!! 무리한 주행으로 인해 내 차량이 대파되었습니다! 차고지에서 수리해야 합니다.")

            sync_user_data(); st.rerun()
