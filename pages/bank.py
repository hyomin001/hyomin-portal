# pages/bank.py
import streamlit as st
import time
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx

from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title

def render(market, nw):
    st.title("🏦 하이리스크 뱅크")
    st.markdown("<div class='card' style='margin-bottom:16px;'><div style='color:#888;font-size:0.82rem;'>⚠️ 대출 조건: 10초마다 <b style='color:#FF4B4B;'>2% 복리 이자</b>가 붙습니다.</div></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 현금",    format_korean_money(st.session_state.global_cash))
    c2.metric("💳 대출잔액", format_korean_money(st.session_state.loan))
    c3.metric("📊 순자산",  format_korean_money(nw))

    tab_send, tab_loan = st.tabs(["💸 송금", "💳 대출/상환"])

    with tab_send:
        _all_users = [u for u in load_db(USERS_FILE, {}).keys() if u != st.session_state.logged_in_user and u != "admin"]
        target = st.selectbox("받는 분 선택", _all_users) if _all_users else None
        if not _all_users: st.info("송금 가능한 다른 유저가 없습니다.")
        amt = st.number_input("송금 금액 (원)", min_value=0, step=1_000_000, format="%d")
        st.caption(f"송금 예정: {format_korean_money(amt)}")
        
        cd_send = cooldown_remaining("send_money", 5.0)
        if cd_send > 0: st.warning(f"⏱️ 송금 쿨다운 {cd_send:.1f}초")
        elif st.button("📤 송금하기", use_container_width=True):
            us = load_db(USERS_FILE, {})
            if target not in us: st.error("존재하지 않는 사용자입니다.")
            elif st.session_state.global_cash < amt: st.error("잔액이 부족합니다.")
            elif amt <= 0: st.error("금액을 입력하세요.")
            else:
                set_cooldown("send_money")
                us_fresh = load_db(USERS_FILE, {})
                if st.session_state.global_cash < amt:
                    st.error("잔액이 부족합니다. (재검증 실패)")
                else:
                    st.session_state.global_cash -= amt
                    us_fresh[target]['cash'] += amt
                    us_fresh[st.session_state.logged_in_user]['cash'] = st.session_state.global_cash
                    save_db(USERS_FILE, us_fresh)
                    log_tx(st.session_state.logged_in_user, "송금", f"{target}에게 송금", -amt)
                    log_tx(target, "송금수신", f"{st.session_state.logged_in_user}에게서 수신", amt)
                    sync_user_data(); st.success(f"✅ {target}님께 {format_korean_money(amt)} 송금 완료!")
                    if amt >= 10_000_000_000: claim_hidden_title("first_donate_10b", "👑 [유일무이] 자선사업가")
                    st.rerun()

    with tab_loan:
        if st.session_state.equipped_title == "💸 신용불량자":
            st.error("🚨 신용불량자 상태에서는 추가 대출이 불가능합니다. 먼저 기존 대출을 상환하세요.")
            avail_loan, max_loan_limit = 0, 0
        else:
            max_loan_limit = max(100_000_000, int(nw * 0.5))
            avail_loan = max(0, max_loan_limit - st.session_state.loan)

        st.info(f"💡 최대 대출 한도: {format_korean_money(max_loan_limit)} (순자산의 50%)\n💸 현재 대출 가능액: {format_korean_money(avail_loan)}\n⚠️ 대출 실행 시 1%의 선취 수수료가 공제됩니다.")
        
        if avail_loan > 0:
            l_amt = st.number_input("대출 금액 (원)", min_value=0, max_value=min(int(avail_loan), 9007199254740991), step=10_000_000, format="%d", key="loan_in_safe")
            cd_loan = cooldown_remaining("loan_action", 5.0)
            if cd_loan > 0: st.warning(f"⏱️ 대출 쿨다운 {cd_loan:.1f}초")
            elif st.button("💳 대출 실행", use_container_width=True):
                if l_amt > 0 and l_amt <= avail_loan:
                    set_cooldown("loan_action")
                    fee = int(l_amt * 0.01)
                    actual_receive = l_amt - fee
                    st.session_state.global_cash += actual_receive
                    st.session_state.loan += l_amt
                    st.session_state.loan_time = time.time()
                    log_tx(st.session_state.logged_in_user, "대출", f"대출 실행 (수수료 공제)", actual_receive)
                    sync_user_data(); st.success(f"✅ {format_korean_money(l_amt)} 대출 완료!")
                    if st.session_state.loan >= 100_000_000_000_000: claim_hidden_title("first_loan_100b", "👑 [유일무이] 갚아도 갚아도 끝이 없는 인생")
                    st.rerun()
                elif l_amt > avail_loan: st.error("대출 한도를 초과했습니다!")
        else: st.error("🚨 현재 대출 한도를 모두 소진하셨습니다.")

        st.write("---")
        r_amt = st.number_input("상환 금액 (원)", min_value=0, step=100_000_000, format="%d", key="repay_in")
        cd_repay = cooldown_remaining("repay_action", 3.0)
        if cd_repay > 0: st.warning(f"⏱️ 상환 쿨다운 {cd_repay:.1f}초")
        elif st.button("🏦 상환하기", use_container_width=True):
            actual = min(r_amt, st.session_state.loan)
            if st.session_state.global_cash >= actual and actual > 0:
                set_cooldown("repay_action")
                st.session_state.global_cash -= actual
                st.session_state.loan -= actual
                if st.session_state.loan <= 0:
                    st.session_state.loan = 0
                    if st.session_state.equipped_title == "💸 신용불량자":
                        st.session_state.equipped_title = "🌱 신규시민"
                        st.success("🎉 대출 전액 상환 완료! 신용이 회복되었습니다.")
                    else: st.success("🎉 대출 전액 상환 완료!")
                else: st.success(f"✅ {format_korean_money(actual)} 상환 완료.")
                log_tx(st.session_state.logged_in_user, "대출상환", "대출 상환", -actual)
                sync_user_data()  
                if st.session_state.global_cash == 0 and actual > 0: claim_hidden_title("perfect_zero_cash", "👑 [유일무이] 완벽한 무소유")
                st.rerun()
            else: st.error("잔액 부족 또는 상환 금액 오류")
