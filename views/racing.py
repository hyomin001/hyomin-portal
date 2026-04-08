import time
import random
import streamlit as st

from database import log_tx, sync_user_data


CARS = [
    {"name": "부가티 시론 SS",        "emoji": "🏎️", "odds": 20.0, "spd": (2, 7),   "color": "#FF0066"},
    {"name": "람보르기니 레부엘토",    "emoji": "🐂",  "odds": 12.0, "spd": (3, 10),  "color": "#FF6600"},
    {"name": "페라리 SF90 XX",         "emoji": "🐎",  "odds": 8.0,  "spd": (4, 12),  "color": "#FF2200"},
    {"name": "맥라렌 P1 GTR",          "emoji": "🚀",  "odds": 6.0,  "spd": (5, 13),  "color": "#FF9900"},
    {"name": "포르쉐 918 스파이더",    "emoji": "⚡",  "odds": 4.0,  "spd": (6, 15),  "color": "#FFCC00"},
    {"name": "테슬라 로드스터 2",      "emoji": "⚡",  "odds": 2.5,  "spd": (8, 17),  "color": "#00FF88"},
    {"name": "토요타 GR010 하이브리드","emoji": "🏁",  "odds": 1.8,  "spd": (10, 20), "color": "#00CCFF"},
]


def render():
    st.title("🏎️ 하이퍼카 레이싱")
    st.caption("배당률이 높을수록 우승 확률은 낮지만 당첨 시 고수익!")

    car_names = [f"{c['emoji']} {c['name']} ({c['odds']}배)" for c in CARS]
    sel_idx   = st.selectbox("차량 선택", range(len(CARS)), format_func=lambda i: car_names[i])
    my_car    = CARS[sel_idx]
    bet_amt   = st.number_input("베팅 금액 (원)", min_value=10_000, step=10_000, value=100_000)
    st.caption(f"우승 시 예상 수령액: ₩{int(bet_amt * my_car['odds']):,}")

    if st.button("🏁 레이스 시작!", use_container_width=True):
        if st.session_state.global_cash < bet_amt:
            st.error("잔액 부족!")
        else:
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
                    positions[c['name']] = min(100, positions[c['name']] + random.randint(c['spd'][0], c['spd'][1]))
                    rank     = sorted(positions.items(), key=lambda x: x[1], reverse=True)
                    pos_num  = next(i+1 for i, (n, _) in enumerate(rank) if n == c['name'])
                    bars[c['name']].progress(positions[c['name']]/100, text=f"{c['emoji']} {c['name']} {pos_num}위 | {positions[c['name']]:.0f}%")
                    if positions[c['name']] >= 100 and winner is None:
                        winner = c['name']

            st.write("---")
            winner_car = next(c for c in CARS if c['name'] == winner)
            st.markdown(f"<div style='text-align:center;font-family:Orbitron,monospace;font-size:1.8rem;color:{winner_car['color']};font-weight:900;padding:20px;'>🏆 {winner_car['emoji']} {winner} 우승!</div>", unsafe_allow_html=True)

            if winner == my_car['name']:
                prize = int(bet_amt * my_car['odds'])
                st.session_state.global_cash += prize
                log_tx(st.session_state.logged_in_user, "레이싱", f"{my_car['name']} 베팅 승리", prize - bet_amt)
                st.success(f"🎉 베팅 성공! +₩{prize:,}"); st.balloons()
            else:
                log_tx(st.session_state.logged_in_user, "레이싱", f"{my_car['name']} 베팅 패배", -bet_amt)
                st.error(f"😢 아쉽습니다. {winner}이(가) 우승했습니다.")

            sync_user_data(); time.sleep(3); st.rerun()
