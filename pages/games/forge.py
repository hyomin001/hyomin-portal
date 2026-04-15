# pages/games/forge.py
import streamlit as st
import random
import time
from utils.config import FORGE_DATA
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title
from utils.database import load_db, log_tx, USERS_FILE, save_market

def render(market, nw):
    st.title("🗡️ 전설의 명검 강화소")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>당신의 운과 욕망을 시험하세요. <b>+5~+9강은 실패 시 50% 확률로 파괴, +10강부터는 확정 파괴</b>됩니다.</div>", unsafe_allow_html=True)
    u_lv = st.session_state.get('weapon_level', 0)
    w_info = FORGE_DATA[u_lv]
    
    st.markdown(f"""
    <div style='text-align:center; padding:30px; background:linear-gradient(180deg, rgba(0,0,0,0.8), rgba(20,20,40,0.9)); border:2px solid {w_info['color']}; border-radius:15px; box-shadow:0 0 20px {w_info['color']}44;'>
        <div style='font-size:4rem; margin-bottom:10px;'>{w_info['name'].split(' ')[0]}</div>
        <div style='font-size:1.8rem; font-weight:900; color:{w_info['color']}; text-shadow:0 0 10px {w_info['color']}88;'>{w_info['name']}</div>
        <div style='color:#94A3B8; margin-top:15px; font-size:0.9rem;'>무기 가치 (판매가): <b style='color:#FFD600;'>{format_korean_money(w_info['sell'])}</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    if u_lv >= 15:
        st.success("🎉 만렙 달성! 더 이상 강화할 수 없습니다. 우주 최강의 무기입니다!")
    else:
        next_info = FORGE_DATA[u_lv + 1]
        cost = next_info['cost']
        rate = next_info['rate'] * 100
        ticket_count = st.session_state.inventory.count("파괴방지권")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"#### 🛠️ 강화 정보 (+{u_lv+1} 도전)")
            st.write(f"- **강화 비용:** {format_korean_money(cost)}")
            st.write(f"- **성공 확률:** {rate}%")
            
            if u_lv >= 9:
                st.markdown("<b style='color:#FF4B4B;'>⚠️ 경고: 실패 시 무기가 무조건 파괴됩니다!</b>", unsafe_allow_html=True)
            elif u_lv >= 4:
                st.markdown("<b style='color:#FF8800;'>⚠️ 경고: 실패 시 50% 확률로 무기가 파괴됩니다!</b>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color:#00FF88;'>안전 강화 구간입니다. 실패해도 레벨이 유지됩니다.</span>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown(f"**🎟️ 내 파괴 방지권:** {ticket_count}개")
            if st.button("🎟️ 파괴 방지권 구매 (500억원)", key="buy_ticket", use_container_width=True):
                if st.session_state.global_cash >= 50_000_000_000: 
                    st.session_state.global_cash -= 50_000_000_000 
                    st.session_state.inventory.append("파괴방지권")
                    sync_user_data()
                    st.success("✅ 파괴 방지권 구매 완료!")
                    st.rerun()
                else:
                    st.error("잔액이 부족합니다.")
            
        with c2:
            st.markdown("#### 🎯 선택")
            cd_forge = cooldown_remaining("forge_action", 1.0)
            
            if u_lv == 0:
                btn_label = f"🪵 목검 구매하기 ({format_korean_money(cost)})"
                use_ticket = False
            else:
                btn_label = f"🔨 강화하기! ({format_korean_money(cost)})"
                if u_lv >= 4:
                    use_ticket = st.checkbox("🛡️ 파괴 방지권 사용", disabled=(ticket_count == 0))
                else:
                    use_ticket = False
                
            if cd_forge > 0:
                st.warning(f"⏱️ 망치질 쿨다운... {cd_forge:.1f}초")
            else:
                if st.button(btn_label, use_container_width=True):
                    if st.session_state.global_cash < cost:
                        st.error("잔액이 부족합니다!")
                    elif use_ticket and "파괴방지권" not in st.session_state.inventory:
                        st.error("⚠️ 파괴 방지권이 없습니다! (중복 클릭 감지)")
                    else:
                        set_cooldown("forge_action")
                        st.session_state.global_cash -= cost
                        
                        if use_ticket:
                            st.session_state.inventory.remove("파괴방지권")
                        
                        uid = st.session_state.logged_in_user
                        us = load_db(USERS_FILE, {}) 
                        is_cursed = us.get(uid, {}).get('cursed_forge', False)
                        success = random.random() < next_info['rate'] 
                        
                        if is_cursed:
                            success = False
                            us[uid]['cursed_forge'] = False
                            us[uid]['cash'] = st.session_state.global_cash
                            save_db(USERS_FILE, us)
                            st.toast("💀 누군가의 불길한 기운이 개입했습니다...", icon="💀")
                            time.sleep(1)

                        if success:
                            st.session_state.weapon_level += 1
                            log_tx(uid, "강화", f"{next_info['name']} 강화 성공", -cost)
                            sync_user_data()
                            
                            if st.session_state.weapon_level >= 10:
                                st.balloons()
                                market['news'] = f"🎆 [전설 탄생] {uid}님이 {next_info['name']} 강화에 성공했습니다!!!"
                                save_market(market)
                                
                            st.success(f"✨ 강화 성공!! [{next_info['name']}]을(를) 획득했습니다!")
                            st.rerun()
                        else:
                            if use_ticket:
                                log_tx(uid, "강화", f"+{u_lv+1} 강화 실패 (방지권 사용)", -cost)
                                sync_user_data()
                                st.info("🛡️ 파괴 방지권이 빛을 발하며 무기를 보호했습니다! (수치 유지)")
                                st.rerun()
                            else:
                                is_destroyed = False
                                if u_lv >= 9:
                                    is_destroyed = True
                                elif u_lv >= 4:
                                    is_destroyed = random.random() < 0.5
                                
                                if is_destroyed:
                                    st.session_state.weapon_level = 0
                                    log_tx(uid, "강화", f"+{u_lv+1} 강화 파괴됨", -cost)
                                    sync_user_data()
                                    if u_lv >= 9:
                                        market['news'] = f"💥 [단독] {uid}님의 {w_info['name']}이(가) 산산조각 났습니다..."
                                        save_market(market)
                                    st.error("💥 쿠장창! 무기가 처참하게 파괴되었습니다...")
                                    st.snow()
                                    st.rerun()
                                else:
                                    if u_lv >= 4:
                                        log_tx(uid, "강화", f"+{u_lv+1} 강화 실패 (파괴 모면)", -cost)
                                        sync_user_data()
                                        st.warning("💦 휴... 강화에 실패했지만, 기적적으로 무기가 파괴되지 않았습니다!")
                                    else:
                                        log_tx(uid, "강화", f"+{u_lv+1} 강화 실패", -cost)
                                        sync_user_data()
                                        st.warning("💦 앗... 강화에 실패했습니다. (무기는 무사합니다)")
                                    st.rerun()

    if u_lv > 0:
        st.write("---")
        if st.button(f"💰 무기 판매 (익절): {format_korean_money(w_info['sell'])}", use_container_width=True, type="secondary"):
            sell_amt = w_info['sell']
            st.session_state.global_cash += sell_amt
            st.session_state.weapon_level = 0
            log_tx(st.session_state.logged_in_user, "무기판매", f"{w_info['name']} 판매", sell_amt)
            sync_user_data()
            st.success(f"✅ 무기를 팔아 {format_korean_money(sell_amt)}을 얻었습니다. 다시 목검부터 시작합니다!")
            if u_lv >= 13:
                claim_hidden_title("sell_high_weapon", "👑 [유일무이] 낭만 합격")
            st.rerun()