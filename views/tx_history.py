import streamlit as st

from config import TXLOG_FILE
from database import load_db


def render():
    st.title("📜 내 거래 기록")
    st.caption("모든 자산 변동 내역을 확인할 수 있습니다. (최근 200건)")

    uid  = st.session_state.logged_in_user
    logs = load_db(TXLOG_FILE, {})
    my_logs = logs.get(uid, [])

    if not my_logs:
        st.info("아직 거래 기록이 없습니다. 주식, 부동산, 광산 등을 이용해보세요!")
    else:
        cats_all = sorted(set(l['category'] for l in my_logs))
        sel_cat  = st.selectbox("카테고리 필터", ["전체"] + cats_all)

        filtered = my_logs if sel_cat == "전체" else [l for l in my_logs if l['category'] == sel_cat]

        total_in  = sum(l['amount'] for l in filtered if l['amount'] > 0)
        total_out = sum(l['amount'] for l in filtered if l['amount'] < 0)

        c1, c2, c3 = st.columns(3)
        c1.metric("📈 총 수입", f"₩{total_in:,.0f}")
        c2.metric("📉 총 지출", f"₩{abs(total_out):,.0f}")
        c3.metric("💰 순손익",  f"₩{total_in + total_out:,.0f}")

        st.write("")

        cat_icons = {
            "주식매수":"📉","주식매도":"📈","부동산매입":"🏗️","부동산매각":"🏷️",
            "부동산수금":"💰","송금":"📤","대출":"💳","대출상환":"🏦",
            "로또":"🎫","축구베팅":"⚽","레이싱":"🏎️","슬롯":"🎰",
            "광산":"⛏️","CBT":"💻","칭호구매":"👑","VIP슬롯":"💎",
        }

        for log in filtered[:100]:
            amt   = log['amount']
            color = "#FF4B4B" if amt > 0 else "#4B9EFF"
            arrow = "▲" if amt > 0 else "▼"
            sign  = "+" if amt > 0 else ""
            cat_ico = cat_icons.get(log['category'], "📋")

            st.markdown(f"""
<div class='tx-row'>
  <span style='color:#555;min-width:110px;'>{log['time']}</span>
  <span style='color:#888;min-width:60px;'>{cat_ico} {log['category']}</span>
  <span style='color:#ddd;flex:1;margin:0 12px;'>{log['desc']}</span>
  <span style='color:{color};font-weight:900;'>{arrow} {sign}₩{abs(amt):,}</span>
</div>""", unsafe_allow_html=True)
