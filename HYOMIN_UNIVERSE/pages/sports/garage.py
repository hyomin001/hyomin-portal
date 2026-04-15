# pages/sports/garage.py
import streamlit as st
import random
from utils.core import format_korean_money, sync_user_data, claim_hidden_title
from utils.database import load_db, save_db, log_tx, USERS_FILE, save_market

def render(market, nw):
    st.title("🛠️ 커스텀 튜닝 차고지")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>차량을 구매하고 우주 최고의 하이퍼카로 개조하세요!</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user
    us = load_db(USERS_FILE, {})
    my_data = us.get(uid, {})

    if 'garage' not in my_data:
        my_data['garage'] = {'cars': {}, 'active_tier': None}
    else:
        g = my_data['garage']
        if 'cars' not in g:
            g['cars'] = {}
            if g.get('owned', False):
                t = str(g.get('tier', 0))
                g['cars'][t] = {"engine_lv": g.get('engine_lv', 0), "suspension_lv": g.get('suspension_lv', 0), "bumper_lv": g.get('bumper_lv', 0), "needs_repair": g.get('needs_repair', False)}
                g['active_tier'] = t
            else:
                g['active_tier'] = None

    garage = my_data['garage']
    CAR_TIERS = [
        {"tier": "0", "name": "2021년형 컴팩트 박스카", "emoji": "🚙", "color": "#A0A0A0", "price": 10_000_000_000},
        {"tier": "1", "name": "터보차저 스포츠 세단", "emoji": "🚗", "color": "#00E5FF", "price": 500_000_000_000},
        {"tier": "2", "name": "V12 럭셔리 하이퍼카", "emoji": "🏎️", "color": "#FFD600", "price": 5_000_000_000_000},
        {"tier": "3", "name": "🌌 우주 뚫은 은하철도", "emoji": "🚀", "color": "#FF00FF", "price": 50_000_000_000_000}
    ]

    tab_my_garage, tab_shop = st.tabs(["🚘 내 차고지", "🏢 차량 대리점 (신차 구매)"])

    with tab_my_garage:
        if not garage['cars']:
            st.info("🚗 소유한 차량이 없습니다. '차량 대리점'에서 첫 차를 구매하세요!")
        else:
            owned_tiers = list(garage['cars'].keys())
            if garage['active_tier'] not in owned_tiers: garage['active_tier'] = owned_tiers[0]
            
            sel_active = st.selectbox(
                "🏁 메인(출전) 차량 선택", owned_tiers, index=owned_tiers.index(garage['active_tier']),
                format_func=lambda t: f"{next(c['emoji'] for c in CAR_TIERS if c['tier']==t)} {next(c['name'] for c in CAR_TIERS if c['tier']==t)}"
            )

            if sel_active != garage['active_tier']:
                garage['active_tier'] = sel_active
                my_data['garage'] = garage; us[uid] = my_data; save_db(USERS_FILE, us); st.rerun()

            active_t = garage['active_tier']
            cur_car_data = garage['cars'][active_t]
            cur_tier_info = next(c for c in CAR_TIERS if c['tier'] == active_t)
            total_lv = cur_car_data['engine_lv'] + cur_car_data['suspension_lv'] + cur_car_data['bumper_lv']

            st.markdown(f"""
            <div style='text-align:center; padding:30px; background:linear-gradient(135deg, rgba(20,20,20,0.8), rgba(40,40,60,0.9)); border:2px solid {cur_tier_info['color']}; border-radius:15px; box-shadow:0 0 20px {cur_tier_info['color']}44;'>
                <div style='font-size:5rem; margin-bottom:10px;'>{cur_tier_info['emoji']}</div>
                <div style='font-size:1.8rem; font-weight:900; color:{cur_tier_info['color']};'>{cur_tier_info['name']}</div>
                <div style='color:#94A3B8; margin-top:15px; font-size:1rem;'>현재 총합 튜닝 레벨: <b style='color:#FFD600;'>Lv.{total_lv}</b> / 15</div>
            </div>
            """, unsafe_allow_html=True)
            st.write("---")

            if cur_car_data['needs_repair']:
                st.error("🚨 앗! 심각한 차량 파손이 감지되었습니다!")
                st.markdown("### 💥 뒷범퍼 및 백판넬 대파")
                st.caption("차량이 파손된 상태에서는 튜닝 및 레이싱 출전이 불가능합니다.")
                
                repair_cost = 8_700_000_000 * (10 ** int(active_t)) 
                if st.button(f"🛠️ 눈물을 머금고 수리하기 ({format_korean_money(repair_cost)})", use_container_width=True):
                    if st.session_state.global_cash >= repair_cost:
                        st.session_state.global_cash -= repair_cost
                        garage['cars'][active_t]['needs_repair'] = False
                        my_data['garage'] = garage; us[uid] = my_data; save_db(USERS_FILE, us)
                        sync_user_data(); log_tx(uid, "차량수리", f"{cur_tier_info['name']} 파손 수리", -repair_cost)
                        st.toast("✨ 수리가 완료되었습니다!", icon="✅"); st.rerun()
                    else: st.error("수리비가 부족합니다!")
            else:
                st.markdown("### 🔧 파츠 튜닝샵")
                st.caption("각 파츠가 5레벨에 도달하면 다음 등급의 차량으로 무상 승급(풀체인지) 할 수 있습니다.")

                def tune_part(part_key, part_name):
                    current_lv = cur_car_data[part_key]
                    if current_lv >= 5:
                        st.success(f"✅ {part_name} 파츠는 이미 최고 레벨(MAX)입니다!")
                        return

                    tier_mult = 10 ** int(active_t)
                    cost = (current_lv + 1) * 10_000_000_000 * tier_mult 
                    prob = max(0.15, 0.8 - (current_lv * 0.15) - (int(active_t) * 0.1))

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{part_name}** (Lv.{current_lv}/5) <br> <span style='color:#888;font-size:0.8rem;'>비용: {format_korean_money(cost)} | 성공률: {prob*100:.0f}%</span>", unsafe_allow_html=True)
                    with col2:
                        if st.button("🔨 강화", key=f"tune_{active_t}_{part_key}", use_container_width=True):
                            if st.session_state.global_cash < cost: st.error("잔액 부족!")
                            else:
                                st.session_state.global_cash -= cost
                                if random.random() < prob:
                                    garage['cars'][active_t][part_key] += 1
                                    log_tx(uid, "튜닝", f"{part_name} 성공 (+{current_lv+1})", -cost)
                                    st.success(f"✨ {part_name} 튜닝 성공!!")
                                    if active_t == "0" and garage['cars'][active_t]['engine_lv'] == 5 and garage['cars'][active_t]['suspension_lv'] == 5 and garage['cars'][active_t]['bumper_lv'] == 5:
                                        claim_hidden_title("first_tier0_max", "👑 [유일무이] 똥차계의 람보르기니")
                                else:
                                    if random.random() < 0.20:
                                        garage['cars'][active_t]['needs_repair'] = True
                                        st.error("💥 쾅!! 튜닝 중 차량이 미끄러져 벽을 들이받았습니다!")
                                        log_tx(uid, "튜닝", f"{part_name} 대실패 (사고발생)", -cost)
                                    else:
                                        log_tx(uid, "튜닝", f"{part_name} 실패", -cost)
                                        st.warning("💦 부품이 맞지 않아 튜닝에 실패했습니다. (파손은 없습니다)")

                                my_data['garage'] = garage; us[uid] = my_data; save_db(USERS_FILE, us)
                                sync_user_data(); st.rerun()

                tune_part("engine_lv", "🔥 하이퍼 V엔진 스왑")
                tune_part("suspension_lv", "🧲 에어 서스펜션 조정")
                tune_part("bumper_lv", "🛡️ 카본 에어로 다이내믹 뒷범퍼")

                st.write("---")
                if cur_car_data['engine_lv'] >= 5 and cur_car_data['suspension_lv'] >= 5 and cur_car_data['bumper_lv'] >= 5:
                    next_tier_int = int(active_t) + 1
                    if next_tier_int < len(CAR_TIERS):
                        next_tier_str = str(next_tier_int)
                        st.info("모든 파츠가 최대 레벨에 도달했습니다! 상위 등급으로 무상 풀체인지가 가능합니다.")
                        if st.button("🚀 차량 풀체인지 승급하기! (무료)", use_container_width=True):
                            del garage['cars'][active_t]
                            garage['cars'][next_tier_str] = {"engine_lv": 0, "suspension_lv": 0, "bumper_lv": 0, "needs_repair": False}
                            garage['active_tier'] = next_tier_str
                            my_data['garage'] = garage; us[uid] = my_data; save_db(USERS_FILE, us)
                            sync_user_data()
                            log_tx(uid, "차량승급", f"{CAR_TIERS[next_tier_int]['name']} 승급", 0)
                            market['news'] = f"🏎️ [차고지 핫이슈] {uid}님이 풀튜닝의 결실로 {CAR_TIERS[next_tier_int]['name']} 오너가 되셨습니다!!"
                            save_market(market)
                            st.balloons(); st.success(f"🎉 승급 완료!"); st.rerun()
                    else:
                        st.success("🌟 튜닝의 끝판왕! 우주 최고의 스펙을 달성했습니다!")

    with tab_shop:
        st.markdown("### 🏢 HYOMIN 모터스 공식 대리점")
        st.caption("돈만 있다면 승급을 위한 튜닝 노가다 없이 바로 하이퍼카를 현찰 박치기로 구매할 수 있습니다.")

        for c_info in CAR_TIERS:
            t_str = c_info['tier']
            c1, c2 = st.columns([4, 2])
            with c1:
                st.markdown(f"**{c_info['emoji']} {c_info['name']}**")
                st.markdown(f"<span style='color:#FFD600;font-weight:900;'>{format_korean_money(c_info['price'])}</span>", unsafe_allow_html=True)
            with c2:
                if t_str in garage['cars']:
                    st.button("✅ 보유 중", key=f"shop_own_{t_str}", disabled=True, use_container_width=True)
                else:
                    if st.button("🛒 구매하기", key=f"shop_buy_{t_str}", use_container_width=True):
                        if st.session_state.global_cash >= c_info['price']:
                            st.session_state.global_cash -= c_info['price']
                            garage['cars'][t_str] = {"engine_lv": 0, "suspension_lv": 0, "bumper_lv": 0, "needs_repair": False}
                            garage['active_tier'] = t_str
                            my_data['garage'] = garage; us[uid] = my_data; save_db(USERS_FILE, us)
                            sync_user_data()
                            log_tx(uid, "차량구매", f"{c_info['name']} 즉시 구매", -c_info['price'])
                            st.toast(f"🎉 {c_info['name']} 출고 완료!", icon="🚗"); st.rerun()
                        else: st.error("잔액이 부족합니다.")
            st.write("---")