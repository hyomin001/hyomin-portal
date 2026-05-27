# pages/bank.py
import streamlit as st
import time
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx, atomic_deduct_cash, atomic_add_cash

from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data, claim_hidden_title

def render(market, nw):
    st.title("🏦 하이리스크 뱅크")
    st.markdown("<div class='card' style='margin-bottom:16px;'><div style='color:#B0BAC8;font-size:0.82rem;'>⚠️ 대출 조건: 10초마다 <b style='color:#FF4B4B;'>2% 복리 이자</b>가 붙습니다.</div></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("💵 현금",    format_korean_money(st.session_state.global_cash))
    c2.metric("💳 대출잔액", format_korean_money(st.session_state.loan))
    c3.metric("📊 순자산",  format_korean_money(nw))

    tab_loan = st.container()

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
                    # ✅ [BUG FIX] atomic_add_cash로 지급 (기존: 세션만 수정 후 sync → 연결 끊기면 미지급)
                    atomic_add_cash(st.session_state.logged_in_user, actual_receive)
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
                        # 이전 칭호를 복원 (없으면 기본값으로)
                        prev_title = st.session_state.get('_pre_debt_title', '🌱 신규시민')
                        # 복원 대상 칭호가 인벤토리에 있는지 확인
                        if prev_title in st.session_state.inventory:
                            st.session_state.equipped_title = prev_title
                        elif st.session_state.inventory:
                            st.session_state.equipped_title = st.session_state.inventory[-1]
                        else:
                            st.session_state.equipped_title = '🌱 신규시민'
                        st.success("🎉 대출 전액 상환 완료! 신용이 회복되었습니다.")
                    else: st.success("🎉 대출 전액 상환 완료!")
                else: st.success(f"✅ {format_korean_money(actual)} 상환 완료.")
                log_tx(st.session_state.logged_in_user, "대출상환", "대출 상환", -actual)
                sync_user_data()  
                if st.session_state.global_cash == 0 and actual > 0: claim_hidden_title("perfect_zero_cash", "👑 [유일무이] 완벽한 무소유")
                st.rerun()
            else: st.error("잔액 부족 또는 상환 금액 오류")
