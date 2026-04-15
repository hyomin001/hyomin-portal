# pages/games/slot.py
import streamlit as st
import time
import random
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title
from utils.database import load_db, log_tx, USERS_FILE, save_market

def render(market, nw):
    st.title("🎰 럭키 슬롯")

    SLOT_TIERS = [
        {"label": "🪙 일반 슬롯",  "cost": 1_000_000,   "jackpot": 30_000_000,    "jackpot_mult": 30, "prob": 0.10},
        {"label": "💰 골드 슬롯",  "cost": 10_000_000,  "jackpot": 500_000_000,   "jackpot_mult": 50, "prob": 0.08},
        {"label": "💎 다이아 슬롯","cost": 100_000_000, "jackpot": 5_000_000_000, "jackpot_mult": 50, "prob": 0.06},
    ]
    SYMBOLS = {"🍒": 0.35, "🍋": 0.25, "🔔": 0.18, "⭐": 0.12, "7️⃣": 0.07, "💎": 0.03}

    sel_tier = st.selectbox("슬롯 등급 선택", range(len(SLOT_TIERS)), format_func=lambda i: SLOT_TIERS[i]['label'])
    tier     = SLOT_TIERS[sel_tier]

    st.markdown(f"""
<div class='card' style='text-align:center;'>
  <div style='color:#888;font-size:0.82rem;'>비용: <b style='color:#FFD600;'>{format_korean_money(tier['cost'])}</b> &nbsp;|&nbsp; 잭팟: <b style='color:#FF00FF;'>{format_korean_money(tier['jackpot'])}</b></div>
  <div style='color:#888;font-size:0.78rem;margin-top:4px;'>💎=3개 잭팟, 같은 기호 3개=고배당, 2개=소배당</div>
</div>""", unsafe_allow_html=True)

    slot_display = st.empty()
    slot_display.markdown("<div style='font-size: 3.5rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.6); border: 1px inset rgba(255,214,0,0.2); border-radius: 14px; letter-spacing: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; text-shadow: 0 0 10px rgba(255,255,255,0.2);'>🎰 &nbsp; 🎰 &nbsp; 🎰</div>", unsafe_allow_html=True)

    cd_slot = cooldown_remaining(f"slot_{sel_tier}", 3.0)
    if cd_slot > 0:
        st.warning(f"⏱️ 슬롯 쿨다운 {cd_slot:.1f}초")
    elif st.button(f"🎰 {tier['label']} 당기기! ({format_korean_money(tier['cost'])})", use_container_width=True):
        if st.session_state.global_cash < tier['cost']:
            st.error("잔액 부족!")
        else:
            set_cooldown(f"slot_{sel_tier}")
            u_db_check = load_db(USERS_FILE, {})
            if u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0) < tier['cost']:
                st.error("잔액 부족! (DB 검증 실패)")
            else:
                st.session_state.global_cash -= tier['cost']
                syms = list(SYMBOLS.keys()); wts = list(SYMBOLS.values())
                for _ in range(14):
                    r = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                    slot_display.markdown(f"<div style='font-size: 3.5rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.6); border: 1px inset rgba(255,214,0,0.2); border-radius: 14px; letter-spacing: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; text-shadow: 0 0 10px rgba(255,255,255,0.2);'>{r[0]} &nbsp; {r[1]} &nbsp; {r[2]}</div>", unsafe_allow_html=True)
                    time.sleep(0.08)

                final = [random.choices(syms, weights=wts)[0] for _ in range(3)]
                slot_display.markdown(f"<div style='font-size: 3.5rem; text-align: center; padding: 20px; background: rgba(0,0,0,0.6); border: 1px inset rgba(255,214,0,0.2); border-radius: 14px; letter-spacing: 20px; min-height: 100px; display: flex; align-items: center; justify-content: center; text-shadow: 0 0 10px rgba(255,255,255,0.2);'>{final[0]} &nbsp; {final[1]} &nbsp; {final[2]}</div>", unsafe_allow_html=True)

                if final[0] == final[1] == final[2] == "💎":
                    prize = tier['jackpot']
                    st.session_state.global_cash += prize
                    if sel_tier == 0: claim_hidden_title("first_slot_jackpot", "👑 [유일무이] 기적을 부르는 유저")
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 잭팟!!!", prize)
                    st.success(f"💎💎💎 JACKPOT!!! +{format_korean_money(prize)}"); st.balloons()
                    market['news'] = f"🎊 [슬롯 잭팟] {st.session_state.logged_in_user}님이 {format_korean_money(prize)} 잭팟!!"
                    save_market(market)
                elif final[0] == final[1] == final[2]:
                    prize = int(tier['cost'] * tier['jackpot_mult'] * 0.2)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 트리플", prize)
                    st.success(f"🎉 트리플! +{format_korean_money(prize)}")
                elif final[0]==final[1] or final[1]==final[2] or final[0]==final[2]:
                    prize = int(tier['cost'] * 1.5)
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 더블", prize)
                    st.warning(f"✨ 더블 매치! +{format_korean_money(prize)}")
                else:
                    log_tx(st.session_state.logged_in_user, "슬롯", "슬롯 꽝", -tier['cost'])
                    st.error("꽝! 다음 기회를 노려보세요!")

                sync_user_data(); st.rerun()