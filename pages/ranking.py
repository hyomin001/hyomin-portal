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


        # ── 던전런 이번 주 TOP 5 ──
        st.markdown("---")
        st.markdown("### 🗡️ 이번 주 던전런 최고 점수 TOP 5")
        from datetime import timedelta
        now_kst = datetime.now(KST)
        week_start = (now_kst - timedelta(days=now_kst.weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
        dungeon_scores = []
        for uid_r, udata in users_all.items():
            if uid_r == "admin": continue
            ds = udata.get('dungeon_stats', {})
            weekly = udata.get('dungeon_weekly', {})
            # 주간 기록이 있으면 주간 점수, 없으면 최고점수로 fallback
            ws = weekly.get('score', 0)
            ww = weekly.get('week_start', '')
            score = ws if ww == week_start.strftime('%Y-%m-%d') else ds.get('best_score', 0)
            if score > 0:
                dungeon_scores.append({
                    'uid': uid_r,
                    'title': udata.get('equipped_title', '🌱 신규시민'),
                    'score': score,
                    'kills': weekly.get('kills', ds.get('best_kills', 0)) if ww == week_start.strftime('%Y-%m-%d') else ds.get('best_kills', 0),
                    'clears': ds.get('clears', 0),
                })
        dungeon_scores.sort(key=lambda x: x['score'], reverse=True)
        d_medals = ["🥇","🥈","🥉","4위","5위"]
        if dungeon_scores:
            for i, d in enumerate(dungeon_scores[:5]):
                me = "🫵" if d['uid'] == st.session_state.logged_in_user else ""
                col = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
                s_du = html.escape(d['uid'])
                s_dt = html.escape(d['title'])
                st.markdown(f"""
<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,215,0,0.15);border-radius:12px;padding:12px 16px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.3rem;'>{d_medals[i]}</span>
    <div>
      <span style='font-weight:900;color:#CBD5E1;margin-right:6px;'>{s_du} {me}</span>
      <span style='color:#888;font-size:0.82rem;'>{s_dt}</span>
    </div>
  </div>
  <div style='text-align:right;'>
    <div style='font-weight:900;color:{col};font-size:1rem;'>🗡️ {d["score"]:,}점</div>
    <div style='font-size:0.8rem;color:#666;'>킬 {d["kills"]} · 클리어 {d["clears"]}회</div>
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.info("이번 주 던전런 기록이 없습니다. 지금 바로 도전해보세요! ⚔️")

        # ── 게임별 1위 기록 ──
        st.markdown("---")
        st.markdown("### 🎮 게임별 역대 1위 기록")

        GAME_DEFS = [
            {
                "key": "sniper",   "icon": "🎯", "name": "라인 배틀 저격전",
                "score_label": "점수", "score_key": "score",
                "sub_fn": lambda d: f"킬 {d.get('kills',0)} · Wave {d.get('wave',1)}"
            },
            {
                "key": "zombie",   "icon": "🧟", "name": "좀비 서바이벌",
                "score_label": "최고 웨이브", "score_key": "wave",
                "sub_fn": lambda d: f"점수 {d.get('score',0):,} · 킬 {d.get('kills',0)}"
            },
            {
                "key": "racing",   "icon": "🏎️", "name": "익스트림 레이싱",
                "score_label": "점수", "score_key": "score",
                "sub_fn": lambda d: f"거리 {d.get('dist',0):.1f}km"
            },
            {
                "key": "fighter",  "icon": "🥊", "name": "격투 토너먼트",
                "score_label": "점수", "score_key": "score",
                "sub_fn": lambda d: f"퍼펙트 {d.get('perfects',0)}회"
            },
        ]

        cols = st.columns(2)
        for gi, gdef in enumerate(GAME_DEFS):
            scores = []
            for uid_r, udata in users_all.items():
                if uid_r == "admin": continue
                rec = udata.get('game_records', {}).get(gdef['key'], {})
                sv = rec.get(gdef['score_key'], 0)
                if sv > 0:
                    scores.append({
                        'uid': uid_r,
                        'title': udata.get('equipped_title', '🌱 신규시민'),
                        'score': sv,
                        'data': rec,
                    })
            scores.sort(key=lambda x: x['score'], reverse=True)

            with cols[gi % 2]:
                st.markdown(f"#### {gdef['icon']} {gdef['name']}")
                if not scores:
                    st.info(f"아직 기록 없음")
                else:
                    gmedals = ["🥇","🥈","🥉","4위","5위"]
                    for i, s in enumerate(scores[:5]):
                        me = "🫵" if s['uid'] == st.session_state.logged_in_user else ""
                        col_str = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
                        s_uid   = html.escape(s['uid'])
                        s_ttl   = html.escape(s['title'])
                        sub_txt = html.escape(gdef['sub_fn'](s['data']))
                        score_disp = f"{s['score']:,}" if gdef['score_key'] == 'score' else f"Wave {s['score']}"
                        st.markdown(f"""
<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;'>
  <div style='display:flex;align-items:center;gap:8px;'>
    <span style='font-size:1.1rem;'>{gmedals[i]}</span>
    <div>
      <span style='font-weight:900;color:#CBD5E1;margin-right:4px;'>{s_uid} {me}</span>
      <span style='color:#888;font-size:0.78rem;'>{s_ttl}</span>
    </div>
  </div>
  <div style='text-align:right;'>
    <div style='font-weight:900;color:{col_str};font-size:0.95rem;'>{gdef["icon"]} {score_disp}점</div>
    <div style='font-size:0.75rem;color:#666;'>{sub_txt}</div>
  </div>
</div>""", unsafe_allow_html=True)

        # ── 인베스트 마블 TOP 5 ──
        st.markdown("---")
        st.markdown("#### 🌍 인베스트 마블 최고 순자산 TOP 5")
        marble_scores = []
        for uid_r, udata in users_all.items():
            if uid_r == "admin": continue
            ms = udata.get('marble_stats', {})
            bw = ms.get('best_net_worth', 0)
            if bw > 0:
                marble_scores.append({
                    'uid': uid_r,
                    'title': udata.get('equipped_title', '🌱 신규시민'),
                    'nw': bw,
                    'wins': ms.get('wins', 0),
                })
        marble_scores.sort(key=lambda x: x['nw'], reverse=True)
        if not marble_scores:
            st.info("아직 마블 기록이 없습니다. 지금 도전해보세요! 🌍")
        else:
            m_medals = ["🥇","🥈","🥉","4위","5위"]
            m_cols = st.columns(min(len(marble_scores[:5]), 5))
            for i, m in enumerate(marble_scores[:5]):
                me = "🫵" if m['uid'] == st.session_state.logged_in_user else ""
                col_str = "#FFD600" if i==0 else "#C0C0C0" if i==1 else "#CD7F32" if i==2 else "#00E5FF"
                s_uid = html.escape(m['uid'])
                s_ttl = html.escape(m['title'])
                st.markdown(f"""
<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,215,0,0.12);border-radius:10px;padding:10px 14px;margin-bottom:6px;display:flex;justify-content:space-between;align-items:center;'>
  <div style='display:flex;align-items:center;gap:8px;'>
    <span style='font-size:1.1rem;'>{m_medals[i]}</span>
    <div>
      <span style='font-weight:900;color:#CBD5E1;margin-right:4px;'>{s_uid} {me}</span>
      <span style='color:#888;font-size:0.78rem;'>{s_ttl}</span>
    </div>
  </div>
  <div style='text-align:right;'>
    <div style='font-weight:900;color:{col_str};font-size:0.95rem;'>🌍 ₩{m["nw"]:,}</div>
    <div style='font-size:0.75rem;color:#666;'>승리 {m["wins"]}회</div>
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
