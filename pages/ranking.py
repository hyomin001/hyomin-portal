# pages/ranking.py
import streamlit as st
import time  # time 모듈 추가
import html  # 👈 XSS 방어(HTML 이스케이프)를 위한 모듈 추가
from datetime import datetime
from utils.config import KST, estate_config, FORGE_DATA
from utils.core import format_korean_money, cooldown_remaining, set_cooldown
from utils.config import USERS_FILE, COMMENTS_FILE
from utils.database import load_db, save_db

def render(market, nw):
    st.title("🏅 랭킹 & 게시판")

    # 탭 이름이 '자유 게시판'으로 바뀌어야 정상 적용된 것입니다!
    tab_rank, tab_board = st.tabs(["🏆 순위표", "💬 자유 게시판"])

    # ==========================================
    # 🏆 탭 1: 순위표 로직
    # ==========================================
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
            
            # 🛡️ XSS 방어: 랭킹에 표시되는 모든 유저 데이터를 이스케이프 처리
            s_uid    = html.escape(r['uid'])
            s_title  = html.escape(r['title'])
            s_weapon = html.escape(r['weapon'])
            s_car    = html.escape(r['car'])
            s_estate = html.escape(r['estate'])
            
            st.markdown(f"""
<div class='card' style='display:flex; flex-direction:column; padding:16px 20px; margin:8px 0;'>
  <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;'>
    <div style='display:flex; align-items:center;'>
      <span style='font-size:1.3rem; min-width:40px;'>{medals[i]}</span>
      <span style='font-weight:900; color:#CBD5E1; font-size:1.1rem; margin-right:10px;'>{s_uid} {me}</span>
      <span style='color:#888; font-size:0.85rem;'>{s_title}</span>
    </div>
    <span style='font-weight:900; color:{nw_color}; font-size:1.1rem;'>{format_korean_money(r['nw'])}</span>
  </div>
  <div style='background:rgba(255,255,255,0.03); border-radius:8px; padding:10px 14px; font-size:0.88rem; color:#94A3B8; line-height:1.7;'>
    <div><b>🗡️ 명검:</b> <span style='color:#00FF88;'>{s_weapon}</span></div>
    <div><b>🏎️ 차량:</b> <span style='color:#00E5FF;'>{s_car}</span></div>
    <div><b>🏢 부동산:</b> <span style='color:#FFD600;'>{s_estate}</span></div>
  </div>
</div>""", unsafe_allow_html=True)


    # ==========================================
    # 💬 탭 2: 게시판 로직 (완벽 개편)
    # ==========================================
    with tab_board:
        st.markdown("### 📝 자유 게시판")
        st.caption("우주 시민들과 자유롭게 대화를 나눠보세요!")

        # 1. 폼(Form) 적용: 엔터키를 쳐도 글이 날아가지 않고 안전하게 저장됨
        with st.form("board_form", clear_on_submit=True):
            # 🛡️ 주의 #2 수정: max_chars 제한으로 DB 폭탄 방지
            msg = st.text_input("메시지 작성", placeholder="내용을 입력하세요 (최대 200자)", max_chars=200)
            submit_btn = st.form_submit_button("🚀 글 등록하기", use_container_width=True)

            if submit_btn:
                cd_post = cooldown_remaining("board_post", 5.0)
                if cd_post > 0:
                    st.error(f"⏱️ 도배 방지! {cd_post:.1f}초 후에 다시 작성해주세요.")
                elif not msg.strip():
                    st.warning("⚠️ 내용을 입력해주세요.")
                elif len(msg.strip()) > 200:
                    st.error("⚠️ 댓글은 200자 이내로 작성해주세요.")
                elif st.session_state.logged_in_user in market.get('board_banned', []):
                    st.error("🔇 창조주에 의해 게시판 이용이 정지된 계정입니다.")
                else:
                    set_cooldown("board_post")
                    comments = load_db(COMMENTS_FILE, [])
                    comments.append({
                        "name":    st.session_state.logged_in_user,
                        "title":   st.session_state.equipped_title,
                        "comment": msg.strip()[:200],  # 🛡️ 서버사이드에서도 잘라내기
                        "time":    datetime.now(KST).strftime("%m/%d %H:%M")
                    })
                    # 🛡️ DB 무한 증식 방지 — 최근 500개만 유지
                    if len(comments) > 500:
                        comments = comments[-500:]
                    save_db(COMMENTS_FILE, comments)
                    st.success("✅ 게시글이 등록되었습니다!")
                    time.sleep(0.5)
                    st.rerun()

        st.write("---")
        
        col1, col2 = st.columns([8, 2])
        with col1: st.markdown("#### 💬 실시간 소통 현황")
        with col2:
            if st.button("🔄 새로고침", use_container_width=True): st.rerun()

        # 2. 게시판 출력 로직 (스크롤 컨테이너 + 예외 처리 추가)
        all_c = load_db(COMMENTS_FILE, [])
        
        if not all_c:
            st.info("텅~ 비었습니다. 영광스러운 첫 번째 글의 주인공이 되어보세요!")
        else:
            # 글이 많아도 화면이 길어지지 않게 고정 높이의 스크롤 박스 생성
            with st.container(height=600):
                for c in reversed(all_c[-100:]): # 최근 100개까지만 표시
                    is_me = (c['name'] == st.session_state.logged_in_user)
                    border = "border-left: 4px solid #00E5FF;" if is_me else "border-left: 4px solid #334155;"
                    me_badge = " <span style='background:#00E5FF;color:#000;font-size:0.7rem;padding:2px 6px;border-radius:4px;font-weight:900;'>나</span>" if is_me else ""
                    
                    # 🛡️ XSS 방어: 이름, 칭호, 내용 모두 안전하게 변환
                    s_name    = html.escape(c['name'])
                    s_ctitle  = html.escape(c.get('title', ''))
                    s_comment = html.escape(c.get('comment', ''))
                    
                    st.markdown(f"""
                    <div class='card' style='margin:8px 0; padding:15px; {border} background: rgba(30, 41, 59, 0.4);'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                            <span>
                                <b style='color:#FFFFFF; font-size:1.05rem;'>{s_name}</b>{me_badge}
                                <span style='color:#94A3B8; font-size:0.85rem; margin-left:8px;'>{s_ctitle}</span>
                            </span>
                            <span style='color:#64748B; font-size:0.8rem;'>{c.get('time','')}</span>
                        </div>
                        <div style='color:#E2E8F0; font-size:0.95rem; line-height: 1.5;'>{s_comment}</div>
                    </div>
                    """, unsafe_allow_html=True)
