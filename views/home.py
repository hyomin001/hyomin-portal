import time
import streamlit as st

from config import stock_config, estate_config, USERS_FILE
from database import load_db


def render(market, nw):
    st.title("🌌 HYOMIN UNIVERSE")
    st.markdown(f"<div style='color:#888;margin-bottom:24px;'>어서오세요, <b style='color:#00E5FF;'>{st.session_state.logged_in_user}</b>님! {st.session_state.equipped_title}</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("💵 현금",    f"₩{st.session_state.global_cash:,.0f}")
    with c2: st.metric("📊 순자산",  f"₩{nw:,.0f}")
    with c3: st.metric("💳 대출",    f"₩{st.session_state.loan:,.0f}")
    with c4:
        cur_t = time.time()
        total_rent_pending = sum(
            estate_config[eid]['income'] * cnt * int(cur_t - st.session_state.rent_time)
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.metric("🏢 수금 대기", f"₩{total_rent_pending:,.0f}")

    st.write("---")
    st.markdown("### 📈 실시간 시장 현황")
    top_stocks = sorted(stock_config, key=lambda s: (
        (market['stock_data'][s['id']]['history'][-1] - market['stock_data'][s['id']]['history'][-2])
        / market['stock_data'][s['id']]['history'][-2]
        if len(market['stock_data'][s['id']]['history']) > 1 else 0
    ), reverse=True)[:5]

    cols = st.columns(5)
    for i, s in enumerate(top_stocks):
        d    = market['stock_data'][s['id']]
        diff = (d['history'][-1] - d['history'][-2]) / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        arrow, clr = ("▲", "#FF4B4B") if diff >= 0 else ("▼", "#4B9EFF")
        with cols[i]:
            st.markdown(f"""
<div class='card' style='text-align:center;padding:14px;'>
  <div style='font-size:1.4rem;'>{s['icon']}</div>
  <div style='font-size:0.78rem;color:#888;margin:4px 0;'>{d['name'][:6]}</div>
  <div style='font-size:1rem;font-weight:900;color:#fff;'>₩{d['price']:,}</div>
  <div style='font-size:0.85rem;color:{clr};font-weight:900;'>{arrow} {abs(diff):.2f}%</div>
</div>""", unsafe_allow_html=True)

    st.write("---")
    st.markdown("### 🏆 이번 시즌 랭킹 Top 5")
    users_all = load_db(USERS_FILE, {})
    rank_data = []
    for uid, udata in users_all.items():
        if uid == "5891": continue
        w = udata.get('cash', 0) - udata.get('loan', 0)
        for sid, p in udata.get('portfolio', {}).items():
            if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
        for eid, cnt in udata.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['price'] * cnt * 0.8
        rank_data.append({"uid": uid, "title": udata.get('equipped_title', '신규시민'), "nw": w})
    rank_data.sort(key=lambda x: x['nw'], reverse=True)
    medals = ["🥇","🥈","🥉","4️⃣","5️⃣"]
    for i, r in enumerate(rank_data[:5]):
        me = " ← 나" if r['uid'] == st.session_state.logged_in_user else ""
        st.markdown(f"""
<div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 20px;'>
  <span style='font-size:1.3rem;'>{medals[i]}</span>
  <span style='font-weight:900;color:#E8E8F0;'>{r['uid']}{me}</span>
  <span style='color:#888;font-size:0.85rem;'>{r['title']}</span>
  <span style='color:#FFD600;font-weight:900;'>₩{r['nw']:,.0f}</span>
</div>""", unsafe_allow_html=True)
