import time
import random
import streamlit as st

from database import log_tx, sync_user_data, save_market


SLOT_TIERS = [
    {"label": "🪙 일반 슬롯",  "cost": 1_000_000,   "jackpot": 30_000_000,    "jackpot_mult": 30, "prob": 0.10},
    {"label": "💰 골드 슬롯",  "cost": 10_000_000,  "jackpot": 500_000_000,   "jackpot_mult": 50, "prob": 0.08},
    {"label": "💎 다이아 슬롯","cost": 100_000_000, "jackpot": 5_000_000_000, "jackpot_mult": 50, "prob": 0.06},
]
SYMBOLS = {"🍒": 0.35, "🍋": 0.25, "🔔": 0.18, "⭐": 0.12, "7️⃣": 0.07, "💎": 0.03}


def render(market):
    st.title("🎰 럭키 슬롯")

    sel_tier = st.selectbox("슬롯 등급 선택", range(len(SLOT_TIERS)), format_func=lambda i: SLOT_TIERS[i]['label'])
    tier     = SLOT_TIERS[sel_tier]

    st.markdown(f"""
<div class='card' style='text-align:center;'>
  <div style='color:#888;font-size:0.82rem;'>비용: <b style='color:#FFD600;'>₩{tier['cost']:,}</b> &nbsp;|&nbsp; 잭팟: <b style='color:#FF00FF;'>₩{tier['jackpot']:,}</b></div>
  <div style='color:#666;font-size:0.78rem;margin-top:4px;'>💎=3개 잭팟, 같은 기호 3개=고배당, 2개=소배당</div>
</div>""", unsafe_allow_html=True)

    slot_display = st.empty()
    slot_display.markdown("<div class='slot-display'>🎰 &nbsp; 🎰 &nbsp; 🎰</div>", unsafe_allow_html=True)

    if st.button(f"🎰 {tier['label']} 당기기! (₩{tier['cost']:,})", use_container_width=True):
        if st.session_state.global_cash < tier['cost']:
            st.error("잔액 부족!")
        else:
            st.session_state.global_cash -= tier['cost']
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += tier['cost']
                st.error("거래 취소 (잔액 보호)")
            else:
                syms = list(SYMBOLS.keys()); wts = list(SYMBOLS.values())
                for _ in range(14):
                    r = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                    slot_display.markdown(f"<div class='slot-display'>{r[0]} &nbsp; {r[1]} &nbsp; {r[2]}</div>", unsafe_allow_html=True)
                    time.sleep(0.08)

                final = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                slot_display.markdown(f"<div class='slot-display'>{final[0]} &nbsp; {final[1]} &nbsp; {final[2]}</div>", unsafe_allow_html=True)

                if final[0] == final[1] == final[2] == "💎":
                    prize = tier['jackpot']
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 잭팟!!!",  prize)
                    st.success(f"💎💎💎 JACKPOT!!! +₩{prize:,}"); st.balloons()
                    market['news'] = f"🎊 [슬롯 잭팟] {st.session_state.logged_in_user}님이 ₩{prize:,} 잭팟!!"
                    save_market(market)
                elif final[0] == final[1] == final[2]:
                    prize = int(tier['cost'] * tier['jackpot_mult'] * 0.2)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 트리플",    prize)
                    st.success(f"🎉 트리플! +₩{prize:,}")
                elif final[0]==final[1] or final[1]==final[2] or final[0]==final[2]:
                    prize = int(tier['cost'] * 1.5)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 더블",      prize)
                    st.warning(f"✨ 더블 매치! +₩{prize:,}")
                else:
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 꽝",       -tier['cost'])
                    st.error("꽝! 다음 기회를 노려보세요!")

                sync_user_data(); time.sleep(2); st.rerun()
