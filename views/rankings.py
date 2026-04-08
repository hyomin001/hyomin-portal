import streamlit as st
from datetime import datetime

from config import USERS_FILE, COMMENTS_FILE, stock_config, estate_config
from database import load_db, save_db


def render(market):
    st.title("🏅 랭킹 & 게시판")

    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 게시판"])

    with tab_rank:
        users_all = load_db(USERS_FILE, {})
        rank_data = []
        for uid, udata in users_all.items():
            if uid == "5891": continue
            w = udata.get('cash', 0) - udata.get('loan', 0)
            for sid, p in udata.get('portfolio', {}).items():
                if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']
            for eid, cnt in udata.get('real_estate', {}).items():
                if eid in estate_config: w += estate_config[eid]['price'] * cnt * 0.8
            rank_data.append({"uid": uid, "title": udata.get('equipped_title','🌱 신규시민'), "nw": w})
        rank_data.sort(key=lambda x: x['nw'], reverse=True)

        medals = ["🥇","🥈","🥉"] + [f"{i}위" for i in range(4, 101)]
        for i, r in enumerate(rank_data[:20]):
            me       = "🫵" if r['uid'] == st.session_state.logged_in_user else ""
            nw_color = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
            st.markdown(f"""
<div class='card' style='display:flex;justify-content:space-between;align-items:center;padding:12px 18px;margin:4px 0;'>
  <span style='font-size:1.1rem;min-width:36px;'>{medals[i]}</span>
  <span style='font-weight:900;color:#E8E8F0;flex:1;margin:0 10px;'>{r['uid']} {me}</span>
  <span style='color:#888;font-size:0.82rem;flex:1;'>{r['title']}</span>
  <span style='font-weight:900;color:{nw_color};'>₩{r['nw']:,.0f}</span>
</div>""", unsafe_allow_html=True)

    with tab_board:
        msg = st.text_input("메시지 작성", placeholder="랭커 게시판에 글을 남겨보세요!")
        if st.button("📝 등록", use_container_width=True):
            if msg.strip():
                comments = load_db(COMMENTS_FILE, [])
                comments.append({
                    "name":    st.session_state.logged_in_user,
                    "title":   st.session_state.equipped_title,
                    "comment": msg.strip(),
                    "time":    datetime.now().strftime("%m/%d %H:%M")
                })
                save_db(COMMENTS_FILE, comments)
                st.rerun()

        st.write("")
        all_c = load_db(COMMENTS_FILE, [])
        for c in reversed(all_c[-50:]):
            st.markdown(f"""
<div class='card' style='margin:6px 0;padding:12px 16px;'>
  <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
    <span><b style='color:#00E5FF;'>{c['name']}</b> <span style='color:#FFD600;font-size:0.82rem;'>{c.get('title','')}</span></span>
    <span style='color:#555;font-size:0.78rem;'>{c.get('time','')}</span>
  </div>
  <div style='color:#ddd;font-size:0.92rem;'>{c['comment']}</div>
</div>""", unsafe_allow_html=True)
