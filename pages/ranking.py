# pages/ranking.py
import streamlit as st
from datetime import datetime
from utils.config import KST, estate_config, FORGE_DATA
from utils.core import format_korean_money, cooldown_remaining, set_cooldown
from utils.database import load_db, save_db, USERS_FILE, COMMENTS_FILE

def render(market, nw):
    st.title("🏅 랭킹 & 게시판")

    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 게시판"])

    with tab_rank:
        users_all = load_db(USERS_FILE, {})
        rank_data = []
        car_tier_map = {"0": "🚙 컴팩트 박스카", "1": "🚗 스포츠 세단", "2": "🏎️ V12 하이퍼카", "3": "🚀 은하철도"}
        
        for uid_r, udata in users_all.items():
            if uid_r == "admin": continue
            w = udata.get('cash', 0) - udata.get('loan', 0)
            
            for sid, p in udata.get('portfolio', {}).items():
                if sid in market['stock_data']: w += p.get('qty', 0) * market['stock_data'][sid]['price']

            for cid, cinfo in udata.get('crypto_portfolio', {}).items():
                price = market.get('crypto_data', {}).get(cid, {}).get('price', 0)
                w += cinfo.get('qty', 0) * price
            
            re_list = []
            for eid, cnt in udata.get('real_estate', {}).items():
                if eid in estate_config: 
                    w += estate_config[eid]['base_price'] * cnt * 0.8
                    if cnt > 0: re_list.append(f"{estate_config[eid]['icon']} {estate_config[eid]['name']} {cnt}채")
            re_str = ", ".join(re_list) if re_list else "보유 부동산 없음"
            
            w_lv = udata.get('weapon_level', 0)
            w_name = FORGE_DATA[w_lv]['name'] if w_lv in FORGE_DATA else "없음"
            if w_lv > 0: w += FORGE_DATA[w_lv]['sell']
            
            garage = udata.get('garage', {})
            car_str = "뚜벅이 (차량 없음)"
            if 'active_tier' in garage and garage['active_tier'] is not None:
                active_t = str(garage['active_tier'])
                car_info = garage.get('cars', {}).get(active_t, {})
                if active_t in car_tier_map:
                    tot_lv = car_info.get('engine_lv', 0) + car_info.get('suspension_lv', 0) + car_info.get('bumper_lv', 0)
                    car_str = f"{car_tier_map[active_t]} (+{tot_lv}강)"
            elif garage.get('owned', False):
                active_t = str(garage.get('tier', '0'))
                if active_t in car_tier_map:
                    tot_lv = garage.get('engine_lv', 0) + garage.get('suspension_lv', 0) + garage.get('bumper_lv', 0)
                    car_str = f"{car_tier_map[active_t]} (+{tot_lv}강)"

            rank_data.append({
                "uid": uid_r, "title": udata.get('equipped_title','🌱 신규시민'), 
                "nw": w, "weapon": w_name, "car": car_str, "estate": re_str
            })
            
        rank_data.sort(key=lambda x: x['nw'], reverse=True)
        medals = ["🥇","🥈","🥉"] + [f"{i}위" for i in range(4, 101)]
        
        for i, r in enumerate(rank_data[:20]):
            me       = "🫵" if r['uid'] == st.session_state.logged_in_user else ""
            nw_color = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
            
            st.markdown(f"""
<div class='card' style='display:flex; flex-direction:column; padding:16px 20px; margin:8px 0;'>
  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;'>
    <div style='display:flex; align-items:center;'>
      <span style='font-size:1.3rem; min-width:40px;'>{medals[i]}</span>
      <span style='font-weight:900; color:#CBD5E1; font-size:1.1rem; margin-right:10px;'>{r['uid']} {me}</span>
      <span style='color:#888; font-size:0.85rem;'>{r['title']}</span>
    </div>
    <span style='font-weight:900; color:{nw_color}; font-size:1.1rem;'>{format_korean_money(r['nw'])}</span>
  </div>
  <div style='background:rgba(255,255,255,0.03); border-radius:8px; padding:10px 14px; font-size:0.88rem; color:#94A3B8; line-height:1.7;'>
    <div><b>🗡️ 명검:</b> <span style='color:#00FF88;'>{r['weapon']}</span></div>
    <div><b>🏎️ 차량:</b> <span style='color:#00E5FF;'>{r['car']}</span></div>
    <div><b>🏢 부동산:</b> <span style='color:#FFD600;'>{r['estate']}</span></div>
  </div>
</div>""", unsafe_allow_html=True)

    with tab_board:
        msg = st.text_input("메시지 작성", placeholder="랭커 게시판에 글을 남겨보세요!")
        cd_post = cooldown_remaining("board_post", 5.0)
        if cd_post > 0:
            st.warning(f"⏱️ 도배 방지 쿨다운 {cd_post:.1f}초")
        elif st.button("📝 등록", use_container_width=True):
            if msg.strip():
                if st.session_state.logged_in_user in market.get('board_banned', []):
                    st.error("🔇 게시판 이용이 정지된 계정입니다.")
                else:
                    set_cooldown("board_post")
                    comments = load_db(COMMENTS_FILE, [])
                    comments.append({
                        "name":    st.session_state.logged_in_user,
                        "title":   st.session_state.equipped_title,
                        "comment": msg.strip(),
                        "time":    datetime.now(KST).strftime("%m/%d %H:%M")
                    })
                    save_db(COMMENTS_FILE, comments)
                    st.rerun()

        st.write("")
        all_c = load_db(COMMENTS_FILE, [])
        for c in reversed(all_c[-50:]):
            is_me = (c['name'] == st.session_state.logged_in_user)
            border = "border-left:3px solid #FFD600;" if is_me else ""
            me_badge = " <span style='background:#FFD600;color:#000;font-size:0.7rem;padding:1px 6px;border-radius:4px;font-weight:900;'>나</span>" if is_me else ""
            st.markdown(f"""
<div class='card' style='margin:6px 0;padding:12px 16px;{border}'>
  <div style='display:flex;justify-content:space-between;margin-bottom:6px;'>
    <span><b style='color:#00E5FF;'>{c['name']}</b>{me_badge} <span style='color:#FFD600;font-size:0.82rem;'>{c.get('title','')}</span></span>
    <span style='color:#777;font-size:0.78rem;'>{c.get('time','')}</span>
  </div>
  <div style='color:#94A3B8;font-size:0.92rem;'>{c['comment']}</div>
</div>""", unsafe_allow_html=True)
