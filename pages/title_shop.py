# pages/title_shop.py
import streamlit as st
from utils.core import format_korean_money, sync_user_data
from utils.config import USERS_FILE
from utils.database import load_db, log_tx, atomic_deduct_cash

def render(market, nw):
    st.title("👑 VIP 칭호 상점")
    st.markdown("칭호를 구매하고 장착하여 게시판에서 부를 과시하세요!")
    NON_TITLE_ITEMS = ["파괴방지권"]
    my_titles = [item for item in st.session_state.inventory if item not in NON_TITLE_ITEMS]

    st.markdown("### 🎖️ 내 칭호 보관함")
    if not my_titles:
        st.info("보유한 칭호가 없습니다. 칭호를 구매하거나 가챠를 뽑아보세요!")
    else:
        default_idx = my_titles.index(st.session_state.equipped_title) if st.session_state.equipped_title in my_titles else 0
        sel_title = st.selectbox("장착할 칭호 선택", my_titles, index=default_idx, format_func=lambda t: f"✅ {t}" if t == st.session_state.equipped_title else t)

        col_eq1, col_eq2 = st.columns([3, 1])
        with col_eq1:
            st.markdown(f"현재 장착 중: <b style='color:#FFD600;'>{st.session_state.equipped_title}</b>", unsafe_allow_html=True)
            if sel_title != st.session_state.equipped_title: st.caption(f"→ '{sel_title}' 으로 변경 예정")
        with col_eq2:
            if st.button("✅ 장착", use_container_width=True, disabled=(sel_title == st.session_state.equipped_title)):
                st.session_state.equipped_title = sel_title
                sync_user_data()
                st.toast(f"'{sel_title}' 장착 완료!", icon="👑")
                st.rerun()

        st.markdown("#### 📦 전체 보관함")
        cols_inv = st.columns(3)
        for i, title in enumerate(my_titles):
            with cols_inv[i % 3]:
                is_equipped = (title == st.session_state.equipped_title)
                border_col  = "#FFD600" if is_equipped else "rgba(0,229,255,0.2)"
                label       = "✅ 장착 중" if is_equipped else "🌟 장착"
                st.markdown(f"<div style='border:1px solid {border_col};border-radius:10px;padding:10px;margin:4px 0;text-align:center;background:rgba(255,255,255,0.03);'><div style='font-size:0.85rem;color:#94A3B8;word-break:break-all;'>{title}</div></div>", unsafe_allow_html=True)
                if not is_equipped:
                    if st.button(label, key=f"inv_eq_{i}", use_container_width=True):
                        st.session_state.equipped_title = title
                        sync_user_data()
                        st.toast(f"'{title}' 장착 완료!", icon="👑")
                        st.rerun()
                else:
                    st.button("✅ 장착 중", key=f"inv_eq_{i}", disabled=True, use_container_width=True)

    st.write("---")
    st.markdown("### 🛒 칭호 상점")

    # 페이지네이션 (한 페이지에 10개씩 표시, 성능 개선)
    PAGE_SIZE = 10
    total_titles = 100
    total_pages  = total_titles // PAGE_SIZE

    if "title_shop_page" not in st.session_state:
        st.session_state.title_shop_page = 0

    cur_page = st.session_state.title_shop_page
    start_i  = cur_page * PAGE_SIZE + 1
    end_i    = start_i + PAGE_SIZE

    # 페이지 네비게이션
    nav_c1, nav_c2, nav_c3 = st.columns([1, 3, 1])
    with nav_c1:
        if st.button("◀ 이전", disabled=(cur_page == 0), use_container_width=True):
            st.session_state.title_shop_page -= 1; st.rerun()
    with nav_c2:
        st.markdown(f"<div style='text-align:center;color:#888;padding-top:8px;'>페이지 {cur_page + 1} / {total_pages} (Lv.{start_i}~Lv.{end_i-1})</div>", unsafe_allow_html=True)
    with nav_c3:
        if st.button("다음 ▶", disabled=(cur_page >= total_pages - 1), use_container_width=True):
            st.session_state.title_shop_page += 1; st.rerun()

    cols = st.columns(2)
    for i in range(start_i, end_i):
        with cols[(i - start_i) % 2]:
            title_name = f"💫 초월자 Lv.{i}" if i >= 90 else f"💎 VIP 칭호 Lv.{i}"
            price      = i * 10_000_000

            st.markdown(f"**{title_name}** | {format_korean_money(price)}")

            if title_name in st.session_state.inventory:
                if st.session_state.equipped_title == title_name:
                    st.button("✅ 장착 중", key=f"eq_{i}", disabled=True)
                else:
                    if st.button("🌟 장착하기", key=f"eq_{i}"):
                        st.session_state.equipped_title = title_name
                        sync_user_data(); st.rerun()
            else:
                if st.button(f"구매하기", key=f"buy_{i}"):
                    if st.session_state.global_cash >= price:
                        # ✅ [BUG FIX] atomic_deduct_cash로 DB 원자적 차감 (기존: DB 확인 후 세션만 차감 → Race Condition)
                        if not atomic_deduct_cash(st.session_state.logged_in_user, price):
                            st.error("잔액 부족! (DB 검증 실패)")
                        else:
                            st.session_state.global_cash -= price
                            st.session_state.inventory.append(title_name)
                            st.session_state.equipped_title = title_name
                            log_tx(st.session_state.logged_in_user, "칭호구매", f"{title_name} 구매", -price)
                            sync_user_data(); st.rerun()
                    else:
                        st.error("잔액이 부족합니다.")
