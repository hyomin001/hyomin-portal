import time
import streamlit as st

from database import log_tx, sync_user_data, save_market


def render(market):
    st.title("⚔️ 1시간 글로벌 로또")

    rem          = max(0, int(3_600 - (time.time() - market['lotto_last_draw'])))
    my_t         = market['lotto_tickets'].get(st.session_state.logged_in_user, 0)
    total_tickets = sum(market['lotto_tickets'].values()) if market['lotto_tickets'] else 0
    my_pct       = (my_t / total_tickets * 100) if total_tickets > 0 else 0

    st.markdown(f"""
<div class='lotto-pool'>
  <div style='color:#888;font-size:0.8rem;letter-spacing:3px;margin-bottom:10px;'>JACKPOT POOL</div>
  <div class='lotto-amount'>₩{market['lotto_pool']:,}</div>
  <div style='color:#888;margin-top:14px;font-size:0.88rem;'>⏱ 추첨까지 <b style='color:#FF00FF;'>{rem//60}분 {rem%60}초</b></div>
  <div style='color:#888;font-size:0.82rem;margin-top:6px;'>내 당첨 확률: <b style='color:#FFD600;'>{my_pct:.1f}%</b> ({my_t}장 / 전체 {total_tickets}장)</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([2, 1])
    with c1:
        b_cnt = st.number_input("구매 수량 (장당 1,000만원)", min_value=1, step=1, value=1)
        cost  = b_cnt * 10_000_000
        st.caption(f"총 비용: ₩{cost:,}")
    with c2:
        st.metric("내 티켓", f"{my_t}장")

    if st.button("🎫 티켓 구매하기", use_container_width=True):
        if st.session_state.global_cash >= cost:
            st.session_state.global_cash -= cost
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += cost
                st.error("거래 취소 (잔액 보호)")
            else:
                market['lotto_pool']    += cost
                market['lotto_tickets'][st.session_state.logged_in_user] = my_t + b_cnt
                save_market(market)
                log_tx(st.session_state.logged_in_user, "로또", f"로또 {b_cnt}장 구매", -cost)
                sync_user_data()
                st.success(f"✅ {b_cnt}장 구매 완료!")
                time.sleep(1); st.rerun()
        else:
            st.error("잔액 부족!")

    if market['lotto_tickets']:
        st.write("---")
        st.markdown("### 👥 현재 참여자")
        sorted_t = sorted(market['lotto_tickets'].items(), key=lambda x: x[1], reverse=True)
        for uid, cnt in sorted_t[:10]:
            pct     = cnt / total_tickets * 100
            me_mark = " 👈" if uid == st.session_state.logged_in_user else ""
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05);'><span style='color:#ddd;'>{uid}{me_mark}</span><span style='color:#FF00FF;font-weight:900;'>{cnt}장 ({pct:.1f}%)</span></div>", unsafe_allow_html=True)

    time.sleep(5); st.rerun()
