# pages/txlog.py
import streamlit as st
from utils.core import format_korean_money
from utils.database import load_db, TXLOG_FILE

def render(market, nw):
    st.title("📜 내 거래 기록")
    st.caption("모든 자산 변동 내역을 확인할 수 있습니다. (최근 200건)")

    uid_log  = st.session_state.logged_in_user
    logs = load_db(TXLOG_FILE, {})
    my_logs = logs.get(uid_log, [])

    if not my_logs:
        st.info("아직 거래 기록이 없습니다.")
    else:
        cats_all = sorted(set(l['category'] for l in my_logs))
        sel_cat  = st.selectbox("카테고리 필터", ["전체"] + cats_all)

        filtered = my_logs if sel_cat == "전체" else [l for l in my_logs if l['category'] == sel_cat]

        total_in  = sum(l['amount'] for l in filtered if l['amount'] > 0)
        total_out = sum(l['amount'] for l in filtered if l['amount'] < 0)

        c1, c2, c3 = st.columns(3)
        c1.metric("📈 총 수입", format_korean_money(total_in))
        c2.metric("📉 총 지출", format_korean_money(abs(total_out)))
        c3.metric("💰 순손익",  format_korean_money(total_in + total_out))

        st.write("")

        for log in filtered[:100]:
            amt   = log['amount']
            color = "#FF4B4B" if amt > 0 else "#4B9EFF"
            arrow = "▲" if amt > 0 else "▼"
            sign  = "+" if amt > 0 else ""
            cat_icons = {
                "주식매수":"📉","주식매도":"📈","부동산매입":"🏗️","부동산구매":"🛒",
                "부동산판매":"🏷️","부동산수금":"💰","송금":"📤","대출":"💳","대출상환":"🏦",
                "로또":"🎫","축구베팅":"⚽","레이싱":"🏎️","슬롯":"🎰",
                "광산":"⛏️","CBT":"💻","칭호구매":"👑","VIP슬롯":"💎","승부차기":"🥅", 
            }
            cat_ico = cat_icons.get(log['category'], "📋")
            st.markdown(f"""
<div class='tx-row' style='display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.9rem;'>
  <span style='color:#777;min-width:110px;'>{log['time']}</span>
  <span style='color:#888;min-width:60px;'>{cat_ico} {log['category']}</span>
  <span style='color:#94A3B8;flex:1;margin:0 12px;'>{log['desc']}</span>
  <span style='color:{color};font-weight:900;'>{arrow} {sign}{format_korean_money(abs(amt))}</span>
</div>""", unsafe_allow_html=True)
