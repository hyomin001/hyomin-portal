import streamlit as st

from database import log_tx, sync_user_data


def render():
    st.title("👑 VIP 칭호 상점")
    st.markdown("칭호를 구매하고 장착하여 게시판에서 부를 과시하세요!")

    cols = st.columns(2)
    for i in range(1, 101):
        with cols[i % 2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            title_id   = f"title_{i}"
            price      = i * 10_000_000

            st.markdown(f"**{title_name}** | ₩{price:,}")

            if title_id in st.session_state.inventory:
                if st.session_state.equipped_title == title_name:
                    st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"):
                        st.session_state.equipped_title = title_name
                        sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        st.session_state.global_cash -= price
                        if st.session_state.global_cash < 0:
                            st.session_state.global_cash += price
                            st.error("거래 취소 (잔액 보호)")
                        else:
                            st.session_state.inventory.append(title_id)
                            st.session_state.equipped_title = title_name
                            log_tx(st.session_state.logged_in_user, "칭호구매", f"{title_name} 구매", -price)
                            sync_user_data(); st.rerun()
                    else:
                        st.error("잔액이 부족합니다.")
