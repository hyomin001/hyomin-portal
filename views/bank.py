import time
import streamlit as st

from config import USERS_FILE
from database import load_db, save_db, log_tx, sync_user_data


def render(nw):
    st.title("🏦 하이리스크 뱅크")

    st.markdown("""
<div class='card' style='margin-bottom:16px;'>
  <div style='color:#888;font-size:0.82rem;'>⚠️ 대출 조건: 10초마다 <b style='color:#FF4B4B;'>2% 복리 이자</b>가 붙습니다.</div>
</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 현금",    f"₩{st.session_state.global_cash:,}")
    c2.metric("💳 대출잔액", f"₩{st.session_state.loan:,}")
    c3.metric("📊 순자산",  f"₩{nw:,}")

    tab_send, tab_loan = st.tabs(["💸 송금", "💳 대출/상환"])

    with tab_send:
        target = st.text_input("받는 분 아이디", placeholder="상대방 아이디 입력")
        amt    = st.number_input("송금 금액 (원)", min_value=0, step=1_000_000, format="%d")
        st.caption(f"송금 예정: ₩{amt:,}")
        if st.button("📤 송금하기", use_container_width=True):
            us = load_db(USERS_FILE, {})
            if target not in us:
                st.error("존재하지 않는 사용자입니다.")
            elif st.session_state.global_cash < amt:
                st.error("잔액이 부족합니다.")
            elif amt <= 0:
                st.error("금액을 입력하세요.")
            else:
                st.session_state.global_cash -= amt
                us[target]['cash'] += amt
                save_db(USERS_FILE, us)
                log_tx(st.session_state.logged_in_user, "송금", f"{target}에게 송금", -amt)
                sync_user_data()
                st.success(f"✅ {target}님께 ₩{amt:,} 송금 완료!")

    with tab_loan:
        l_amt = st.number_input("대출 금액 (원)", min_value=0, step=100_000_000, format="%d", key="loan_in")
        if st.button("💳 대출 실행", use_container_width=True):
            if l_amt > 0:
                st.session_state.global_cash += l_amt
                st.session_state.loan += l_amt
                st.session_state.loan_time = time.time()
                log_tx(st.session_state.logged_in_user, "대출", f"대출 실행", l_amt)
                sync_user_data()
                st.success(f"✅ ₩{l_amt:,} 대출 완료. 빠른 상환을 권장합니다!")
                time.sleep(1); st.rerun()

        r_amt = st.number_input("상환 금액 (원)", min_value=0, step=100_000_000, format="%d", key="repay_in")
        if st.button("🏦 상환하기", use_container_width=True):
            actual = min(r_amt, st.session_state.loan)
            if st.session_state.global_cash >= actual and actual > 0:
                st.session_state.global_cash -= actual
                st.session_state.loan -= actual
                if st.session_state.loan <= 0:
                    st.session_state.loan = 0
                    if st.session_state.equipped_title == "💸 신용불량자":
                        st.session_state.equipped_title = "🌱 신규시민"
                        st.success("🎉 대출 전액 상환 완료! 신용이 회복되었습니다.")
                    else:
                        st.success("🎉 대출 전액 상환 완료!")
                else:
                    st.success(f"✅ ₩{actual:,} 상환 완료. 잔여 대출: ₩{st.session_state.loan:,}")
                log_tx(st.session_state.logged_in_user, "대출상환", f"대출 상환", -actual)
                sync_user_data(); time.sleep(1); st.rerun()
            else:
                st.error("잔액 부족 또는 상환 금액 오류")
