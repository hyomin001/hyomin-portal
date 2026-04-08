import time
import streamlit as st

from config import estate_config
from database import log_tx, sync_user_data


def render():
    st.title("🏢 부동산 제국")

    now      = time.time()
    pass_s   = int(now - st.session_state.rent_time)
    total_income_rate = sum(
        estate_config[eid]['income'] * cnt
        for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
    )
    pending = total_income_rate * pass_s

    st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,100,50,0.1));
     border:1px solid rgba(0,255,136,0.3);border-radius:14px;padding:22px;text-align:center;margin-bottom:18px;'>
  <div style='color:#888;font-size:0.85rem;letter-spacing:2px;margin-bottom:8px;'>누적 월세 수익</div>
  <div style='font-family:Orbitron,monospace;font-size:2rem;font-weight:900;color:#00FF88;'>₩{pending:,.0f}</div>
  <div style='color:#666;font-size:0.8rem;margin-top:8px;'>초당 ₩{total_income_rate:,} 수입 중</div>
</div>""", unsafe_allow_html=True)

    if st.button("💰 전액 수금하기", use_container_width=True):
        if pending > 0:
            st.session_state.global_cash += int(pending)
            st.session_state.rent_time = now
            log_tx(st.session_state.logged_in_user, "부동산수금", f"임대 수익 수금", int(pending))
            sync_user_data()
            st.success(f"✅ ₩{int(pending):,} 수금 완료!")
            time.sleep(1); st.rerun()
        else:
            st.info("수금할 금액이 없습니다.")

    st.write("---")
    st.markdown("### 🏘️ 부동산 매물 목록")

    for eid, info in estate_config.items():
        owned     = st.session_state.real_estate.get(eid, 0)
        inc_total = info['income'] * owned
        sell_val  = int(info['price'] * 0.8)

        c1, c2, c3 = st.columns([5, 2, 2])
        with c1:
            st.markdown(f"""
<div class='estate-card'>
  <div style='display:flex;align-items:center;gap:12px;'>
    <span style='font-size:2rem;'>{info['icon']}</span>
    <div>
      <div style='font-weight:900;font-size:1.05rem;color:#fff;'>{info['name']}</div>
      <div style='color:#888;font-size:0.82rem;'>{info['desc']}</div>
      <div style='margin-top:6px;'>
        <span style='color:#FFD600;font-weight:900;'>₩{info['price']:,}</span>
        <span style='color:#555;margin:0 8px;'>|</span>
        <span class='estate-income'>+₩{info['income']:,}/초</span>
        {f"<span style='margin-left:12px;color:#aaa;'>보유 {owned}채 → 초당 ₩{inc_total:,}</span>" if owned > 0 else ""}
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
        with c2:
            can_buy = st.session_state.global_cash >= info['price']
            if st.button("🏗️ 매입" if can_buy else "💸 잔액부족",
                         key=f"buy_{eid}", use_container_width=True, disabled=not can_buy):
                if st.session_state.global_cash >= info['price']:
                    st.session_state.global_cash -= info['price']
                    if st.session_state.global_cash < 0:
                        st.session_state.global_cash += info['price']
                        st.error("거래 취소 (잔액 보호)")
                    else:
                        st.session_state.real_estate[eid] = owned + 1
                        log_tx(st.session_state.logged_in_user, "부동산매입", f"{info['name']} 매입", -info['price'])
                        sync_user_data()
                        st.success(f"✅ {info['name']} 매입 완료!")
                        time.sleep(1); st.rerun()
                else:
                    st.error("잔액 부족!")
        with c3:
            if owned > 0:
                if st.button(f"🏷️ 매각 (80%)\n₩{sell_val:,}",
                             key=f"sell_{eid}", use_container_width=True):
                    st.session_state.global_cash += sell_val
                    st.session_state.real_estate[eid] = owned - 1
                    if st.session_state.real_estate[eid] == 0:
                        del st.session_state.real_estate[eid]
                    log_tx(st.session_state.logged_in_user, "부동산매각", f"{info['name']} 매각 (80%)", sell_val)
                    sync_user_data()
                    st.success(f"✅ {info['name']} 매각 완료! +₩{sell_val:,}")
                    time.sleep(1); st.rerun()
            else:
                st.markdown("<div style='height:52px;'></div>", unsafe_allow_html=True)
