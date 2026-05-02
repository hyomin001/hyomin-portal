# pages/admin/panel.py
import streamlit as st
import time
import os
import pandas as pd
import html  # 👈 XSS 방어(HTML 이스케이프) 모듈 추가
from datetime import datetime
from utils.config import KST, stock_config, estate_config, USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE, REALESTATE_MARKET_FILE, FORGE_DATA, MESSAGES_FILE # 👈 MESSAGES_FILE 상수 추가
from utils.core import hash_pw, format_korean_money, sync_user_data, get_net_worth
from utils.database import load_db, save_db, save_market, load_estate_market, save_estate_market, load_clan_db, save_clan_db, get_user_clan

def render(market, nw):
    # 🛡️ [보안] 함수 자체에도 admin 검증 — 라우팅 우회 방어
    if st.session_state.get('logged_in_user') != 'admin':
        st.error("⛔ 접근 권한이 없습니다.")
        st.stop()

    st.title("🛠️ 창조주 통제소")
    st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;margin-bottom:10px;'>⚠️ 창조주 전용 패널입니다. 이곳의 모든 조작은 우주(서버) 전체에 즉시 반영됩니다.</div>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = st.tabs([
        "👤 유저 개조", "🏢 부동산 통제", "💬 게시판 관리", "🌍 글로벌 정책",
        "📈 시장 조작", "📊 전체 현황", "👁️ 전지적 모니터링", "🏎️ 차고지 조작",
        "🏆 시즌 관리", "📩 쪽지 감시"
    ])

    with t1:
        def parse_creator_money(text):
            if not text: return None
            text = text.replace(',', '').replace(' ', '').strip()
            if text.isdigit(): return int(text)
            units = {"조": 10**12, "억": 10**8, "만": 10**4}
            total = 0
            import re
            matches = re.findall(r'([0-9.]+)([조억만]?)', text)
            if not matches:
                try:
                    clean_num = re.sub(r'[^0-9.]', '', text)
                    return int(float(clean_num)) if clean_num else None
                except: return None
            for val, unit in matches:
                total += float(val) * units.get(unit, 1)
            return int(total)

        u_db = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "admin"]



        if uid_list:
            sel_u  = st.selectbox("조작할 유저 선택", uid_list, key="admin_sel_u")
            u_data = u_db[sel_u]

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("##### 💰 자산 개조")
                raw_cash = st.text_input("현금 설정 (예: 1000억, 1.5조)", placeholder="비워두면 유지", key="admin_cash_input")
                raw_loan = st.text_input("대출 설정 (예: 5000만)", placeholder="비워두면 유지", key="admin_loan_input")
                parsed_cash = parse_creator_money(raw_cash)
                parsed_loan = parse_creator_money(raw_loan)
                final_cash = parsed_cash if parsed_cash is not None else int(u_data.get('cash', 0))
                final_loan = parsed_loan if parsed_loan is not None else int(u_data.get('loan', 0))
                st.markdown(f"""
                <div style='background:rgba(0,229,255,0.1);padding:15px;border-radius:10px;border:1px solid #00E5FF;margin-top:10px;'>
                  <div style='color:#00E5FF;font-size:0.8rem;'>▼ 적용 예정 금액</div>
                  <div style='font-size:1.1rem;margin-top:5px;'>
                    <b>현금:</b> {format_korean_money(final_cash)}<br>
                    <b>대출:</b> {format_korean_money(final_loan)}
                  </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown("##### 👑 신분 개조")
                new_title = st.text_input("칭호 수정", value=u_data.get('equipped_title',''), key="admin_title_input")
                st.write("")
                st.metric("현재 현금", format_korean_money(u_data.get('cash', 0)))
                st.metric("현재 대출", format_korean_money(u_data.get('loan', 0)))
                st.write("")
                st.markdown("##### 🔑 비밀번호 초기화")
                new_pw_admin = st.text_input("새 비밀번호", type="password", placeholder="새 비밀번호 입력", key="admin_pw_reset")
                if st.button("🔑 비밀번호 강제 변경", use_container_width=True, key="admin_pw_btn"):
                    if not new_pw_admin:
                        st.error("비밀번호를 입력하세요.")
                    else:
                        from utils.core import hash_pw_bcrypt
                        u_db[sel_u]['pw'] = hash_pw_bcrypt(new_pw_admin)
                        save_db(USERS_FILE, u_db)
                        st.success(f"✅ {sel_u} 비밀번호 변경 완료!")
                        st.rerun()

            c_btn1, c_btn2, c_btn3 = st.columns(3)
            if c_btn1.button("🔥 유저 데이터 강제 개조", use_container_width=True):
                u_db[sel_u]['cash'] = final_cash
                u_db[sel_u]['loan'] = final_loan
                u_db[sel_u]['equipped_title'] = new_title
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 유저 조작 완료!"); st.rerun()
            
            if c_btn2.button("🕊️ 신용 대사면 (빚 전액 탕감)", use_container_width=True):
                u_db[sel_u]['loan'] = 0
                if u_db[sel_u]['equipped_title'] == "💸 신용불량자": u_db[sel_u]['equipped_title'] = "🌱 신규시민"
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 유저의 빚을 모두 탕감했습니다!"); st.rerun()

            if c_btn3.button("🗑️ 해당 유저 계정 삭제", use_container_width=True, type="secondary"):
                del u_db[sel_u]; save_db(USERS_FILE, u_db); st.rerun()
                
            st.write("---")
            st.markdown("##### 🗡️ 전설의 명검 강제 통제소")
            c_w1, c_w2, c_w3 = st.columns(3)
            
            if c_w1.button("👑 신의 망치 (+15강 투척)", use_container_width=True):
                u_db[sel_u]['weapon_level'] = 15
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}에게 엑스칼리버를 하사했습니다!"); st.rerun()
                
            if c_w2.button("💀 파괴의 저주 (다음 강화 무조건 파괴)", use_container_width=True):
                u_db[sel_u]['cursed_forge'] = True
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}의 무기에 저주를 내렸습니다!"); st.rerun()
                
            if c_w3.button("🔨 무기 강제 압수 (0강으로)", use_container_width=True):
                u_db[sel_u]['weapon_level'] = 0
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u}의 무기를 분쇄했습니다!"); st.rerun()

            st.write("---")
            st.markdown("##### 🎒 인벤토리 강제 조작")
            give_title = st.text_input("지급할 칭호명 입력", placeholder="예: 👑 [유일무이] 테스트", key="give_title_input")
            gc1, gc2 = st.columns(2)
            if gc1.button("🎁 칭호 강제 지급 + 장착", use_container_width=True):
                if give_title.strip():
                    u_db[sel_u].setdefault('inventory', [])
                    if give_title not in u_db[sel_u]['inventory']:
                        u_db[sel_u]['inventory'].append(give_title)
                    u_db[sel_u]['equipped_title'] = give_title
                    save_db(USERS_FILE, u_db)
                    st.success(f"✅ {sel_u}에게 [{give_title}] 지급 + 장착 완료!")
                    st.rerun()
            if gc2.button("🗑️ 인벤토리 전체 초기화", use_container_width=True, type="secondary"):
                u_db[sel_u]['inventory'] = []
                u_db[sel_u]['equipped_title'] = "🌱 신규시민"
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 인벤토리 초기화 완료!")
                st.rerun()

            st.write("---")
            st.markdown("##### 🪙 코인/주식 포트폴리오 강제 초기화")
            pa1, pa2, pa3 = st.columns(3)
            if pa1.button("📈 주식 포트폴리오 초기화", use_container_width=True):
                u_db[sel_u]['portfolio'] = {}
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 주식 포트폴리오 초기화!"); st.rerun()
            if pa2.button("🪙 코인 포트폴리오 초기화", use_container_width=True):
                u_db[sel_u]['crypto_portfolio'] = {}
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 코인 포트폴리오 초기화!"); st.rerun()
            if pa3.button("📅 일퀘 강제 초기화", use_container_width=True):
                u_db[sel_u]['daily_quests'] = {}
                save_db(USERS_FILE, u_db); st.success(f"✅ {sel_u} 일퀘 초기화!"); st.rerun()
        else:
            st.info("관리할 유저가 없습니다.")

    with t2:
        u_db   = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "admin"]
        
        st.markdown("### 🏗️ 부동산 신규 공급량(초기 재고) 조작")
        st.caption("운영사 직판 물량(initial_stock)을 늘리거나 줄여서 시장에 개입합니다.")
        
        em_admin = load_estate_market()
        initial_stock_data = em_admin.get("initial_stock", {eid: info["total_supply"] for eid, info in estate_config.items()})
        
        c_sup1, c_sup2, c_sup3, c_sup4 = st.columns([3, 2, 2, 2])
        
        with c_sup1:
            sup_eid = st.selectbox("조작할 매물 선택", list(estate_config.keys()), format_func=lambda x: f"{estate_config[x]['icon']} {estate_config[x]['name']} (기본공급: {estate_config[x]['total_supply']}개)")
        
        owned_total = sum(v.get(sup_eid, 0) for v in em_admin["owner_counts"].values())
        listed_count = sum(1 for l in em_admin["listings"] if l["eid"] == sup_eid)
        initial_released = owned_total + listed_count
        
        current_limit = initial_stock_data.get(sup_eid, estate_config[sup_eid]["total_supply"])
        remaining_sup = max(0, current_limit - initial_released)
        
        with c_sup2:
            st.write("")
            st.markdown(f"**현재 설정 한도:** {current_limit}개")
            st.markdown(f"**마켓 잔여 물량:** <b style='color:#00FF88;'>{remaining_sup}개</b>", unsafe_allow_html=True)
            
        with c_sup3:
            sup_mod = st.number_input("조작 수량 (개)", min_value=1, step=1, value=1)
            
        with c_sup4:
            st.write(""); st.write("")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("➕ 늘리기", use_container_width=True):
                    initial_stock_data[sup_eid] = current_limit + sup_mod
                    em_admin["initial_stock"] = initial_stock_data
                    save_estate_market(em_admin)
                    market['news'] = f"🏗️ [운영사 공지] {estate_config[sup_eid]['name']} 신규 분양 물량이 {sup_mod}개 추가되었습니다!"
                    save_market(market); st.success("물량 추가 완료!"); st.rerun()
            with col_b:
                if st.button("➖ 줄이기", use_container_width=True):
                    new_limit = max(initial_released, current_limit - sup_mod)
                    initial_stock_data[sup_eid] = new_limit
                    em_admin["initial_stock"] = initial_stock_data
                    save_estate_market(em_admin)
                    st.success("물량 축소 완료!"); st.rerun()

        st.write("---")

        st.markdown("### 🏢 특정 유저 부동산 강제 압수 (몰수)")
        if uid_list:
            re_target = st.selectbox("압수할 대상 유저", uid_list, key="re_target_u")
            u_re = u_db[re_target].get('real_estate', {})
            
            if not u_re:
                st.info(f"{re_target} 유저는 보유 중인 부동산이 없습니다.")
            else:
                c1, c2, c3 = st.columns([3, 2, 2])
                with c1:
                    re_eid = st.selectbox("압수할 매물 선택", list(u_re.keys()), format_func=lambda x: f"{estate_config[x]['icon']} {estate_config[x]['name']} (보유: {u_re[x]}채)")
                with c2:
                    re_cnt = st.number_input("압수할 수량", min_value=1, max_value=u_re[re_eid], step=1)
                with c3:
                    st.write(""); st.write("")
                    if st.button("🔨 강제 압수 실행", use_container_width=True):
                        u_db[re_target]['real_estate'][re_eid] -= re_cnt
                        if u_db[re_target]['real_estate'][re_eid] <= 0:
                            del u_db[re_target]['real_estate'][re_eid]
                        save_db(USERS_FILE, u_db)

                        if re_target in em_admin["owner_counts"] and re_eid in em_admin["owner_counts"][re_target]:
                            em_admin["owner_counts"][re_target][re_eid] -= re_cnt
                            if em_admin["owner_counts"][re_target][re_eid] <= 0:
                                del em_admin["owner_counts"][re_target][re_eid]
                        save_estate_market(em_admin)
                        st.toast(f"✅ {re_target} 유저의 부동산 환수 완료!", icon="🏢"); st.rerun()
        else:
             st.info("관리할 유저가 없습니다.")

        st.write("---")
        
        st.markdown("### 🔄 유저 등록 중고 매물 강제 삭제")
        if em_admin["listings"]:
            for li in em_admin["listings"]:
                info = estate_config.get(li["eid"], {})
                ca, cb = st.columns([5, 1])
                ca.markdown(f"**{info.get('icon','')} {info.get('name','?')}** — 판매자: `{li['seller']}` — {format_korean_money(li['price'])}")
                if cb.button("강제삭제", key=f"admin_del_re_{li['id']}"):
                    em_admin["listings"] = [x for x in em_admin["listings"] if x["id"] != li["id"]]
                    save_estate_market(em_admin); st.rerun()
        else:
            st.info("현재 유저가 등록한 중고 매물이 없습니다.")
            
        st.write("---")
        
        st.markdown("### 💣 부동산 마켓 전체 초기화")
        if st.button("🔄 부동산 마켓 전체 초기화 (경매장 싹쓸이 & 전 유저 몰수 & 공급량 리셋)", type="secondary"):
            save_estate_market({"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}})
            
            u_db_reset = load_db(USERS_FILE, {})
            now_time = time.time()
            for uid_k in u_db_reset:
                u_db_reset[uid_k]['real_estate'] = {} 
                u_db_reset[uid_k]['rent_time'] = now_time 
            save_db(USERS_FILE, u_db_reset)
            
            st.session_state.real_estate = {}
            st.session_state.rent_time = now_time
            
            market['force_estate_reset'] = now_time
            save_market(market)
            
            st.toast("💣 부동산 마켓 초기화 완료!", icon="💣"); st.rerun()

    with t3:
        st.markdown("### 💬 게시판 개별/전체 관리")
        all_c = load_db(COMMENTS_FILE, [])
        
        c1, c2 = st.columns([4, 1])
        c1.write(f"총 {len(all_c)}개의 게시물이 있습니다.")
        if c2.button("💣 게시판 전체 초기화", use_container_width=True):
            save_db(COMMENTS_FILE, []); st.success("초기화 완료!"); st.rerun()
            
        st.write("---")
        if not all_c:
            st.info("등록된 게시물이 없습니다.")
        else:
            for idx, c in reversed(list(enumerate(all_c))):
                col_txt, col_btn = st.columns([6, 1])
                with col_txt:
                    # 🛡️ XSS 방어: 작성자 닉네임과 게시판 글 내용 모두 HTML 이스케이프 적용
                    safe_name = html.escape(c.get('name', ''))
                    safe_comment = html.escape(c.get('comment', ''))
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;'><b style='color:#00E5FF;'>{safe_name}</b>: {safe_comment} <span style='color:#888; font-size:0.8rem;'>({c.get('time','')})</span></div>", unsafe_allow_html=True)
                with col_btn:
                    if st.button("🗑️ 삭제", key=f"del_board_{idx}", use_container_width=True):
                        all_c.pop(idx) 
                        save_db(COMMENTS_FILE, all_c); st.rerun()

    with t4:
        st.markdown("### 🚧 서버 점검 관리 (Maintenance Mode)")
        st.caption("점검 모드를 켜면 일반 유저의 유니버스 접속이 차단되며 포털 첫 화면에 점검 배너가 뜹니다.")

        current_m_mode = market.get("maintenance_mode", False)
        current_m_msg = market.get("maintenance_msg", "현재 서버 점검 및 업데이트 중입니다. 이용에 불편을 드려 죄송합니다.")

        c_m1, c_m2 = st.columns([1, 2])
        with c_m1:
            new_m_mode = st.toggle("🚨 점검 모드 켜기 (유저 접속 차단)", value=current_m_mode)
        with c_m2:
            new_m_msg = st.text_input("점검 배너 메시지 입력", value=current_m_msg)

        if st.button("⚙️ 점검 설정 적용 (서버 즉시 반영)", use_container_width=True):
            market["maintenance_mode"] = new_m_mode
            market["maintenance_msg"] = new_m_msg
            save_market(market)
            if new_m_mode:
                st.error("🚨 점검 모드가 활성화되었습니다. 이제 일반 유저들은 접속할 수 없습니다.")
            else:
                st.success("✅ 점검이 끝났습니다. 우주의 문이 다시 열렸습니다!")
            st.rerun()

        st.write("---")
        st.markdown("### 🕊️ 창조주의 은총 (에어드랍)")
        st.caption("모든 유저(관리자 제외)에게 동일한 현금을 일괄 지급합니다.")
        airdrop_amt = st.number_input("지급할 금액", min_value=0, step=10_000_000, value=100_000_000)
        if st.button("💸 전 우주에 현금 살포하기", use_container_width=True):
            # FIX: 에어드랍 시 항상 최신 DB 로드 (t1에서 로드한 stale u_db 사용 금지)
            fresh_db = load_db(USERS_FILE, {})
            for u in fresh_db:
                if u != "admin": fresh_db[u]['cash'] += airdrop_amt
            save_db(USERS_FILE, fresh_db)
            # 현재 로그인된 어드민 세션 현금은 변경 안 함 (admin은 에어드랍 제외)
            market['news'] = f"🕊️ [창조주의 은총] 모든 시민에게 {format_korean_money(airdrop_amt)}이 지급되었습니다!"
            save_market(market); st.toast("에어드랍 완료!", icon="🕊️"); st.rerun()

        st.write("---")
        st.markdown("### 🔇 특정 유저 게시판 이용 정지")
        st.caption("해당 유저의 게시판 글을 전부 삭제하고 블랙리스트에 등록합니다.")
        ban_target = st.selectbox("정지할 유저", [u for u in load_db(USERS_FILE, {}).keys() if u != "admin"], key="ban_target")
        if st.button("🔇 게시판 이용 정지 (글 전삭)", use_container_width=True):
            all_c = load_db(COMMENTS_FILE, [])
            before = len(all_c)
            all_c = [c for c in all_c if c['name'] != ban_target]
            save_db(COMMENTS_FILE, all_c)
            market_ban = market
            market_ban.setdefault('board_banned', [])
            if ban_target not in market_ban['board_banned']: market_ban['board_banned'].append(ban_target)
            save_market(market_ban)
            st.success(f"✅ {ban_target} 글 {before - len(all_c)}개 삭제 + 이용 정지!"); st.rerun()

        if st.button("🔓 게시판 이용 정지 해제", use_container_width=True):
            market_ban = market
            if ban_target in market_ban.get('board_banned', []):
                market_ban['board_banned'].remove(ban_target)
                save_market(market_ban)
                st.success(f"✅ {ban_target} 이용 정지 해제!"); st.rerun()

        st.write("---")
        st.markdown("### 🌪️ 창조주의 분노 (부유세 강제 징수)")
        st.caption("모든 유저(관리자 제외)의 현재 '현금'에서 설정한 퍼센트(%)만큼을 강제로 징수합니다.")
        tax_rate = st.slider("징수율 (%)", min_value=1, max_value=99, value=10)
        if st.button("🌪️ 전 우주 부유세 징수 실행", use_container_width=True):
            for u in u_db:
                if u != "admin":
                    tax_amount = int(u_db[u]['cash'] * (tax_rate / 100.0))
                    u_db[u]['cash'] -= tax_amount
            save_db(USERS_FILE, u_db)
            market['news'] = f"🌪️ [창조주의 분노] 전 우주를 대상으로 {tax_rate}%의 부유세가 강제 징수되었습니다!"
            save_market(market); st.toast("세금 징수 완료!", icon="🌪️"); st.rerun()

        st.write("---")
        st.markdown("### 🏰 클랜 강제 해산")
        clans_admin = load_clan_db()
        if clans_admin:
            clan_del_target = st.selectbox("해산할 클랜 선택", list(clans_admin.keys()), format_func=lambda n: f"{clans_admin[n]['icon']} {n} ({len(clans_admin[n]['members'])}명)", key="clan_del_select")
            cd1, cd2 = st.columns(2)
            if cd1.button("💣 클랜 강제 해산", use_container_width=True, type="secondary"):
                del clans_admin[clan_del_target]
                save_clan_db(clans_admin)
                market['news'] = f"💣 [창조주의 심판] [{clan_del_target}] 클랜이 강제 해산되었습니다!"
                save_market(market); st.success(f"✅ {clan_del_target} 클랜 해산 완료!"); st.rerun()
            if cd2.button("🏦 클랜 은행 전액 몰수", use_container_width=True):
                seized = clans_admin[clan_del_target].get('bank', 0)
                clans_admin[clan_del_target]['bank'] = 0
                save_clan_db(clans_admin)
                st.success(f"✅ {format_korean_money(seized)} 몰수 완료!"); st.rerun()
        else:
            st.info("현재 존재하는 클랜이 없습니다.")

        st.write("---")
        st.markdown("### 🏹 유저 클랜 강제 조정")
        st.caption("특정 유저를 다른 클랜으로 강제 이동시키거나 무소속으로 만듭니다.")

        all_users_list = [u for u in u_db.keys() if u != "admin"]
        all_clans_data = load_clan_db()

        if all_users_list:
            c_move1, c_move2 = st.columns(2)
            with c_move1:
                target_u = st.selectbox("조정할 유저 선택", all_users_list, key="admin_move_user")
                current_c = get_user_clan(target_u)
                st.markdown(f"현재 상태: <b style='color:#00E5FF;'>{current_c if current_c else '무소속'}</b>", unsafe_allow_html=True)

            with c_move2:
                dest_c = st.selectbox("이동시킬 대상 클랜", ["🚫 무소속으로 방출"] + list(all_clans_data.keys()), key="admin_move_dest")

            if st.button("⚡ 클랜 소속 강제 변경 실행", use_container_width=True):
                if current_c:
                    all_clans_data[current_c]['members'] = [m for m in all_clans_data[current_c]['members'] if m != target_u]
                    if all_clans_data[current_c]['leader'] == target_u:
                        if all_clans_data[current_c]['members']:
                            all_clans_data[current_c]['leader'] = all_clans_data[current_c]['members'][0]
                        else:
                            del all_clans_data[current_c]

                if dest_c == "🚫 무소속으로 방출":
                    msg = f"🍃 [창조주의 명령] {target_u}님이 클랜에서 방출되어 무소속이 되었습니다."
                else:
                    if target_u not in all_clans_data[dest_c]['members']:
                        all_clans_data[dest_c]['members'].append(target_u)
                    msg = f"🏹 [창조주의 명령] {target_u}님이 [{dest_c}] 클랜으로 강제 전입되었습니다."

                save_clan_db(all_clans_data)
                market['news'] = msg; save_market(market); st.success("✅ 유저 소속 변경 완료!"); st.rerun()

    with t5:
        st.markdown("### 📈 종목별 가격 조작")
        for s in stock_config:
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"{s['icon']} {s['name']}")
            c2.write(f"현재: ₩{market['stock_data'][s['id']]['price']:,}")
            if c3.button("🚀 +50%", key=f"up_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = f"🚀 [시장조작] {s['name']} 급등!"; save_market(market); st.rerun()
            if c4.button("📉 -30%", key=f"dn_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 0.7)
                market['news'] = f"💣 [시장조작] {s['name']} 폭락!"; save_market(market); st.rerun()

        st.write("---")
        ca, cb = st.columns(2)
        with ca:
            if st.button("🔥 전종목 +50% 폭등", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = "🔥 [창조주의 축복] 전 종목 폭등!!!"; save_market(market); st.rerun()
        with cb:
            if st.button("💣 전종목 -40% 폭락", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = max(1000, int(market['stock_data'][s['id']]['price'] * 0.6))
                market['news'] = "💣 [창조주의 심판] 전 종목 폭락!!!"; save_market(market); st.rerun()

        st.write("---")
        st.markdown("### 📢 공지사항 & 이벤트")
        msg_text  = st.text_area("공지 내용", value=market.get('admin_msg', ''), height=70)
        msg_color = st.color_picker("텍스트 색상", value=market.get('admin_color', '#FF4B4B'))
        cc1, cc2 = st.columns(2)
        if cc1.button("📣 공지 발령", use_container_width=True):
            market['admin_msg'] = msg_text; market['admin_color'] = msg_color; save_market(market); st.success("완료!")
        if cc2.button("🗑️ 공지 삭제", use_container_width=True):
            market['admin_msg'] = ""; save_market(market); st.success("완료!")

        st.write("---")
        st.markdown("### 🎰 로또 강제 조작")
        st.metric("현재 로또 풀", format_korean_money(market.get('lotto_pool', 0)))
        lc1, lc2 = st.columns(2)
        with lc1:
            lotto_add = st.number_input("로또 풀 추가 금액", min_value=0, step=1_000_000_000, value=1_000_000_000, format="%d")
            if st.button("💰 로또 풀 금액 추가", use_container_width=True):
                market['lotto_pool'] += lotto_add; save_market(market)
                st.success(f"✅ {format_korean_money(lotto_add)} 추가! 현재: {format_korean_money(market['lotto_pool'])}"); st.rerun()
        with lc2:
            if st.button("🎊 로또 즉시 강제 추첨", use_container_width=True):
                market['lotto_last_draw'] = 0; save_market(market)
                st.success("✅ 다음 렌더링에서 즉시 추첨됩니다!"); st.rerun()
            if st.button("🗑️ 로또 티켓 전체 초기화", use_container_width=True, type="secondary"):
                market['lotto_tickets'] = {}
                market['lotto_pool'] = 5_000_000_000
                save_market(market); st.success("✅ 로또 초기화 완료!"); st.rerun()

    with t6:
        u_db2 = load_db(USERS_FILE, {})
        total_users = len([u for u in u_db2.keys() if u != "admin"])
        
        st.markdown(f"### 📈 누적 가입(접속) 유저 수: <b style='color:#00E5FF; font-size:1.8rem;'>{total_users}명</b>", unsafe_allow_html=True)
        st.write("---")
        
        st.markdown("### 📊 전체 유저 현황")
        rows = [{"ID": uid_r, "칭호": ud.get('equipped_title',''), "현금": format_korean_money(ud.get('cash',0)), "무기": f"+{ud.get('weapon_level',0)}강", "대출": format_korean_money(ud.get('loan',0))} for uid_r, ud in u_db2.items() if uid_r != "admin"]
        if rows: st.table(pd.DataFrame(rows))
        else: st.info("등록된 유저가 없습니다.")

        st.write("---")
        st.markdown("### 💾 데이터베이스 연결 상태")
        # FIX: MongoDB 기반이므로 os.path.exists 대신 실제 컬렉션 존재 여부 확인
        from utils.database import get_mongo_client
        _mongo_ok = get_mongo_client() is not None
        _status   = "✅ MongoDB 연결됨" if _mongo_ok else "❌ MongoDB 연결 실패"
        st.markdown(f"<div style='color:#ccc;font-size:0.9rem;'>{_status}</div>", unsafe_allow_html=True)
        if _mongo_ok:
            for _col in [USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE, REALESTATE_MARKET_FILE]:
                _col_name = _col.replace(".json", "").replace("_db", "")
                st.markdown(f"<div style='color:#888;font-size:0.85rem;margin-left:12px;'>📂 컬렉션: <b>{_col_name}</b></div>", unsafe_allow_html=True)
            
        st.write("---")
        st.markdown("### 🚨 긴급 데이터 백업 (다운로드)")
        import json
        users_data = load_db(USERS_FILE, {})
        market_data_backup = load_db(MARKET_FILE, {})
        re_data = load_db(REALESTATE_MARKET_FILE, {})
        st.download_button("📥 유저 데이터 백업", json.dumps(users_data, ensure_ascii=False, indent=2), file_name=f"backup_{USERS_FILE}", mime="application/json")
        st.download_button("📥 시장 데이터 백업", json.dumps(market_data_backup, ensure_ascii=False, indent=2), file_name=f"backup_{MARKET_FILE}", mime="application/json")
        st.download_button("📥 부동산 데이터 백업", json.dumps(re_data, ensure_ascii=False, indent=2), file_name=f"backup_{REALESTATE_MARKET_FILE}", mime="application/json")

        st.write("---")
        st.markdown("### 👑 히든 칭호 발급 현황")
        hidden_titles = market.get('hidden_titles', {})
        if not hidden_titles:
            st.info("아직 발급된 히든 칭호가 없습니다.")
        else:
            for tid, owner in list(hidden_titles.items()):
                hc1, hc2 = st.columns([4, 1])
                hc1.markdown(f"**{tid}** → <b style='color:#00E5FF;'>{owner}</b>", unsafe_allow_html=True)
                if hc2.button("🔄 초기화", key=f"reset_hidden_{tid}", use_container_width=True):
                    del market['hidden_titles'][tid]
                    save_market(market); st.success(f"✅ {tid} 칭호 발급 기록 초기화!"); st.rerun()

    with t7:
        c_title, c_btn = st.columns([5, 1])
        with c_title: st.markdown("### 👁️ 실시간 유저 활동 로그")
        with c_btn: 
            if st.button("🔄 새로고침", use_container_width=True): st.rerun()

        all_logs = load_db(TXLOG_FILE, {})
        combined_logs = []
        for user_id, user_logs in all_logs.items():
            for log in user_logs:
                log['uid'] = user_id  
                combined_logs.append(log)
                
        combined_logs.sort(key=lambda x: x['time'], reverse=True)
        
        if not combined_logs:
            st.info("아직 기록된 활동이 없습니다.")
        else:
            for log in combined_logs[:100]:
                amt   = log['amount']
                color = "#FF4B4B" if amt > 0 else "#4B9EFF"
                sign  = "+" if amt > 0 else ""
                
                # 🛡️ XSS 방어: 활동 로그 내용 HTML 이스케이프 적용
                safe_uid = html.escape(log.get('uid', ''))
                safe_desc = html.escape(log.get('desc', ''))
                
                st.markdown(f"""
                <div style='font-size:0.85rem; padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.05);'>
                    <span style='color:#777;'>[{log['time']}]</span> 
                    <b style='color:#00E5FF;'>{safe_uid}</b>님이 
                    <span style='color:#94A3B8;'>{safe_desc}</span> 
                    <b style='color:{color};'>({sign}{format_korean_money(amt)})</b>
                </div>
                """, unsafe_allow_html=True)

    with t8:
        st.markdown("### 🏎️ 유저 차량 강제 개조 및 통제")
        u_db_car = load_db(USERS_FILE, {})
        uid_list_car = [u for u in u_db_car.keys() if u != "admin"]

        CAR_TIERS_ADMIN = [
            {"tier": "0", "name": "2021년형 컴팩트 박스카"}, {"tier": "1", "name": "터보차저 스포츠 세단"},
            {"tier": "2", "name": "V12 럭셔리 하이퍼카"}, {"tier": "3", "name": "🌌 우주 뚫은 은하철도"}
        ]

        if uid_list_car:
            car_target = st.selectbox("조작할 대상 유저", uid_list_car, key="car_target_u")
            raw_garage = u_db_car[car_target].get('garage', {})

            if 'cars' in raw_garage and isinstance(raw_garage['cars'], dict):
                garage_cars = raw_garage.get('cars', {})
                active_t    = raw_garage.get('active_tier', None)
            else:
                if raw_garage.get('owned', False):
                    t = str(raw_garage.get('tier', 0))
                    garage_cars = {t: {"engine_lv": raw_garage.get('engine_lv', 0), "suspension_lv": raw_garage.get('suspension_lv', 0), "bumper_lv": raw_garage.get('bumper_lv', 0), "needs_repair": raw_garage.get('needs_repair', False)}}
                    active_t = t
                else:
                    garage_cars = {}
                    active_t    = None

            if not garage_cars:
                st.info(f"{car_target} 유저는 아직 차량을 소유하고 있지 않습니다.")
                if st.button("🚀 우주 끝판왕 하이퍼카 꽂아주기", use_container_width=True):
                    u_db_car[car_target]['garage'] = {'cars': {'3': {"engine_lv": 5, "suspension_lv": 5, "bumper_lv": 5, "needs_repair": False}}, 'active_tier': '3'}
                    save_db(USERS_FILE, u_db_car); st.success(f"✅ {car_target}님에게 풀튜닝 우주선을 하사했습니다!"); st.rerun()
            else:
                owned_tiers = list(garage_cars.keys())
                sel_view_t  = st.selectbox("조작할 차량 선택", owned_tiers, format_func=lambda t: f"Tier {t} — {next((c['name'] for c in CAR_TIERS_ADMIN if c['tier']==t), '알 수 없음')}")
                parts       = garage_cars[sel_view_t]
                repair_cost = 8_700_000_000 * (10 ** int(sel_view_t))

                c_car1, c_car2 = st.columns(2)
                with c_car1:
                    st.markdown(f"**현재 등급:** Tier {sel_view_t} — {next((c['name'] for c in CAR_TIERS_ADMIN if c['tier']==sel_view_t), '?')}")
                    st.markdown(f"**튜닝 레벨:** 엔진({parts.get('engine_lv',0)}) / 서스({parts.get('suspension_lv',0)}) / 범퍼({parts.get('bumper_lv',0)})")
                    st.markdown(f"**사고상태:** {'🚨 파손' if parts.get('needs_repair') else '✅ 정상'}")
                    st.markdown(f"**메인여부:** {'⭐ 메인' if active_t == sel_view_t else '서브'}")

                with c_car2:
                    if st.button(f"💥 강제 사고 발생 (수리비 {format_korean_money(repair_cost)})", use_container_width=True):
                        u_db_car[car_target]['garage']['cars'][sel_view_t]['needs_repair'] = True
                        save_db(USERS_FILE, u_db_car); market['news'] = f"🚨 {car_target}님 차량 대파!"; save_market(market); st.rerun()
                    if st.button("🔧 무상 수리", use_container_width=True):
                        u_db_car[car_target]['garage']['cars'][sel_view_t]['needs_repair'] = False
                        save_db(USERS_FILE, u_db_car); st.rerun()
                    if st.button("🗑️ 강제 폐차", use_container_width=True, type="secondary"):
                        del u_db_car[car_target]['garage']['cars'][sel_view_t]
                        remaining = list(u_db_car[car_target]['garage']['cars'].keys())
                        u_db_car[car_target]['garage']['active_tier'] = remaining[0] if remaining else None
                        save_db(USERS_FILE, u_db_car); st.rerun()
        else: st.info("관리할 유저가 없습니다.")
        
    with t9:
        st.markdown("### 🏆 시즌 관리")
        cur_season    = market.get('season_num', 1)
        season_end_ts = market.get('season_end', 0)
        season_end_dt = datetime.fromtimestamp(season_end_ts, KST).strftime("%Y-%m-%d %H:%M")
        remain_sec    = max(0, int(season_end_ts - time.time()))
        
        st.markdown(f"""
        <div style='background:rgba(0,229,255,0.08);border:1px solid #00E5FF; border-radius:12px;padding:20px;margin-bottom:16px;'>
          <div style='color:#888;font-size:0.82rem;'>현재 운영 중인 시즌</div>
          <div style='font-size:2rem;font-weight:900;color:#FFD600;'>시즌 {cur_season}</div>
          <div style='color:#94A3B8;margin-top:8px;'>종료 예정: <b style='color:#FF00FF;'>{season_end_dt}</b></div>
          <div style='color:#94A3B8;'>잔여: <b style='color:#00FF88;'>{remain_sec // 86400}일 {(remain_sec % 86400) // 3600}시간</b></div>
        </div>""", unsafe_allow_html=True)

        st.markdown("#### 🛠️ 시즌 번호 강제 조정")
        c_sn1, c_sn2 = st.columns([3, 1])
        with c_sn1: new_sn = st.number_input("변경할 시즌 번호", min_value=1, value=int(cur_season), key="admin_manual_sn")
        with c_sn2:
            st.write(""); st.write("")
            if st.button("🪄 즉시 변경", use_container_width=True):
                market['season_num'] = new_sn; save_market(market); st.rerun()

        st.write("---")
        st.markdown("### 📅 시즌 종료일 수동 조정")
        new_days = st.number_input("지금부터 몇 일 후에 시즌 종료?", min_value=1, max_value=90, value=30)
        if st.button("📅 시즌 종료일 변경", use_container_width=True):
            market['season_end'] = time.time() + new_days * 86400; save_market(market); st.rerun()

        st.write("---")
        st.markdown("### ⚡ 시즌 즉시 강제 종료")
        if st.button("💣 시즌 즉시 종료 & 경제 리셋 실행", use_container_width=True, type="secondary"):
            market['season_end'] = time.time() - 1
            us_instant = load_db(USERS_FILE, {})
            rd_instant = []
            
            for uid_i, udata_i in us_instant.items():
                if uid_i == 'admin': continue
                w_i = udata_i.get('cash', 0) - udata_i.get('loan', 0)
                for sid_i, p_i in udata_i.get('portfolio', {}).items():
                    if sid_i in market['stock_data']: w_i += p_i.get('qty', 0) * market['stock_data'][sid_i]['price']
                for eid_i, cnt_i in udata_i.get('real_estate', {}).items():
                    if eid_i in estate_config: w_i += estate_config[eid_i]['base_price'] * cnt_i * 0.8
                w_lv_i = udata_i.get('weapon_level', 0)
                if w_lv_i > 0: w_i += FORGE_DATA[w_lv_i]['sell']
                rd_instant.append((uid_i, w_i))

            rd_instant.sort(key=lambda x: x[1], reverse=True)
            sn_i = market.get('season_num', 1)
            season_titles_i = [f"🥇 [시즌{sn_i}] 전설의 우승자", f"🥈 [시즌{sn_i}] 준우승의 영광", f"🥉 [시즌{sn_i}] 시즌 3위"]
            
            record_i = {}
            for idx_i, (uid_i, w_i) in enumerate(rd_instant[:3]):
                title_i = season_titles_i[idx_i]
                record_i[f"rank{idx_i+1}"] = uid_i
                if uid_i in us_instant:
                    if title_i not in us_instant[uid_i].get('inventory', []):
                        us_instant[uid_i].setdefault('inventory', []).append(title_i)
                    us_instant[uid_i]['equipped_title'] = title_i

            for uid_i in us_instant:
                if uid_i == 'admin': continue
                us_instant[uid_i]['cash']             = 500_000_000 
                us_instant[uid_i]['portfolio']        = {}
                us_instant[uid_i]['crypto_portfolio'] = {}
                us_instant[uid_i]['real_estate']      = {}
                us_instant[uid_i]['loan']             = 0
                us_instant[uid_i]['daily_quests']     = {}
                us_instant[uid_i]['bulk_trade_count'] = 0
                us_instant[uid_i]['loan_time']        = time.time()
                us_instant[uid_i]['rent_time']        = time.time()
                us_instant[uid_i]['weapon_level']     = 0

            save_db(USERS_FILE, us_instant)
            save_estate_market({"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}})

            market['season_records'] = market.get('season_records', {})
            market['season_records'][str(sn_i)] = record_i
            market['season_num']     = sn_i + 1
            market['season_start']   = time.time()
            market['season_end']     = time.time() + 30 * 86400
            market['season_ending']  = False
            market['lotto_pool']     = 5_000_000_000
            market['lotto_tickets']  = {}
            market['force_estate_reset'] = time.time()
            market['news'] = f"🏆 [시즌{sn_i} 종료] {rd_instant[0][0] if rd_instant else '?'}님 우승! 🌌 시즌 {sn_i+1} 시작!"
            save_market(market)

            st.session_state.real_estate = {}
            st.session_state.portfolio = {}
            if hasattr(st.session_state, 'crypto_portfolio'): st.session_state.crypto_portfolio = {}
            st.session_state.loan = 0
            st.rerun()

        st.write("---")
        st.markdown("### 📜 역대 시즌 기록")
        records = market.get('season_records', {})
        if not records: st.info("아직 완료된 시즌이 없습니다.")
        else:
            for sn, rec in sorted(records.items(), key=lambda x: int(x[0]), reverse=True):
                st.markdown(f"**시즌 {sn}**\n- 🥇 1위: {rec.get('rank1','?')}\n- 🥈 2위: {rec.get('rank2','?')}\n- 🥉 3위: {rec.get('rank3','?')}")
        st.write("---")
        st.markdown("### 🔑 전체 비밀번호 초기화")
        st.caption("⚠️ admin 제외 모든 유저 비밀번호를 **1234** 로 초기화합니다.")
        if st.button("🔑 전체 비밀번호 1234로 초기화", type="primary", use_container_width=True):
            from utils.core import hash_pw_bcrypt
            pw_db = load_db(USERS_FILE, {})
            new_hash = hash_pw_bcrypt("1234")
            for u in pw_db:
                if u == "admin": continue
                pw_db[u]['pw'] = new_hash
            save_db(USERS_FILE, pw_db)
            st.success("✅ 전체 유저 비밀번호가 1234로 초기화됐습니다!")
            st.rerun()

        st.write("---")
        st.markdown("### 💥 우주 대폭발 (시즌 1 완벽 초기화)")
        st.caption("⚠️ **경고:** 모든 유저의 칭호, 차량, 명검, 클랜, 게시판, 쪽지, 거래 기록이 싹 다 날아가고 시즌 1 1일차로 완벽하게 돌아갑니다. (아이디/비밀번호만 유지)")
        
        delete_confirm = st.text_input("초기화하려면 '우주 대폭발' 이라고 정확히 입력하세요.", key="bigbang_confirm")
        if st.button("💥 빅뱅 실행 (모든 데이터 영구 삭제 및 리셋)", type="primary", use_container_width=True):
            if delete_confirm == "우주 대폭발":
                # 1. 유저 데이터 초기화 (비밀번호 빼고 싹 리셋)
                us_db = load_db(USERS_FILE, {})
                for u in list(us_db.keys()):
                    if u == "admin": continue
                    us_db[u] = {
                        "pw": us_db[u]["pw"], # 비밀번호 유지
                        "cash": 500_000_000,  # 초기 정착금
                        "inventory": [],
                        "equipped_title": "🌱 신규시민",
                        "portfolio": {}, "crypto_portfolio": {}, "real_estate": {},
                        "loan": 0, "loan_time": time.time(), "rent_time": time.time(),
                        "daily_quests": {}, "weapon_level": 0, "bulk_trade_count": 0,
                        "garage": {'cars': {}, 'active_tier': None}
                    }
                save_db(USERS_FILE, us_db)
                
                # 2. 마켓 데이터 초기화 (시즌 1로 롤백)
                market['season_num'] = 1
                market['season_records'] = {}
                market['hidden_titles'] = {}
                market['season_start'] = time.time()
                market['season_end'] = time.time() + 30 * 86400
                market['lotto_pool'] = 5_000_000_000
                market['lotto_tickets'] = {}
                market['news'] = "🌌 [우주 대폭발] 새로운 우주가 탄생했습니다. 역사적인 시즌 1 시작!"
                save_market(market)
                
                # 3. 부동산, 클랜, 게시판, 쪽지, 거래로그 전부 날리기
                save_estate_market({"listings": [], "owner_counts": {}, "initial_stock": {eid: info["total_supply"] for eid, info in estate_config.items()}})
                save_clan_db({})
                save_db(COMMENTS_FILE, [])
                save_db(TXLOG_FILE, {})
                save_db(MESSAGES_FILE, {})  # 👈 MESSAGES_FILE 적용
                
                # 4. 현재 접속 중인 관리자 세션 임시 리셋
                st.session_state.inventory = []
                st.session_state.equipped_title = "👑 절대신 창조주"
                st.session_state.weapon_level = 0
                st.session_state.real_estate = {}
                st.session_state.portfolio = {}
                if hasattr(st.session_state, 'crypto_portfolio'): st.session_state.crypto_portfolio = {}
                st.session_state.loan = 0
                
                st.success("💥 우주 대폭발 완료! 모든 것이 백지상태가 되었습니다.")
                st.balloons()
                time.sleep(2)
                st.rerun()
            else:
                st.error("입력한 문구가 일치하지 않습니다. 오타를 확인해주세요.")
    
    with t10:
        st.markdown("### 👁️ 전지적 쪽지 모니터링")
        all_msg_db = load_db(MESSAGES_FILE, {}) # 👈 MESSAGES_FILE 적용
        
        if not all_msg_db:
            st.info("현재 우주에 생성된 쪽지 데이터가 없습니다.")
        else:
            admin_sub_tabs = st.tabs(["🔍 유저별 조회", "📜 전체 로그", "💣 데이터 관리"])
            with admin_sub_tabs[0]:
                target_u = st.selectbox("조회할 유저 선택", list(all_msg_db.keys()), key="admin_msg_u")
                u_msgs = all_msg_db.get(target_u, {})
                col_in, col_out = st.columns(2)
                with col_in:
                    st.markdown(f"**📥 {target_u}의 받은 쪽지**")
                    for m in reversed(u_msgs.get("inbox", [])):
                        # 🛡️ XSS 방어 적용
                        safe_sender = html.escape(m.get('sender', '알 수 없음'))
                        safe_content = html.escape(m.get('content', ''))
                        st.markdown(f"<div style='font-size:0.8rem; padding:8px; background:rgba(255,255,255,0.03); border-radius:5px; margin-bottom:5px;'><b style='color:#00E5FF;'>{safe_sender}</b> → {safe_content} <br><span style='color:#777;'>{m['time']}</span></div>", unsafe_allow_html=True)
                with col_out:
                    st.markdown(f"**📤 {target_u}의 보낸 쪽지**")
                    for m in reversed(u_msgs.get("outbox", [])):
                        # 🛡️ XSS 방어 적용
                        safe_receiver = html.escape(m.get('receiver', '알 수 없음'))
                        safe_content = html.escape(m.get('content', ''))
                        st.markdown(f"<div style='font-size:0.8rem; padding:8px; background:rgba(255,255,255,0.03); border-radius:5px; margin-bottom:5px;'>→ <b style='color:#FFD600;'>{safe_receiver}</b>: {safe_content} <br><span style='color:#777;'>{m['time']}</span></div>", unsafe_allow_html=True)

            with admin_sub_tabs[1]:
                st.markdown("**🌐 우주 전체 쪽지 타임라인**")
                global_logs = []
                for sender_id, data in all_msg_db.items():
                    for m in data.get("outbox", []):
                        global_logs.append({"time": m['time'], "from": sender_id, "to": m['receiver'], "content": m['content']})
                global_logs.sort(key=lambda x: x['time'], reverse=True)
                for log in global_logs[:100]:
                    # 🛡️ XSS 방어 적용
                    safe_from = html.escape(log.get('from', '알 수 없음'))
                    safe_to = html.escape(log.get('to', '알 수 없음'))
                    safe_content = html.escape(log.get('content', ''))
                    st.markdown(f"<div style='font-size:0.85rem; border-bottom:1px solid rgba(255,255,255,0.05); padding:5px 0;'><span style='color:#777;'>[{log['time']}]</span> <b style='color:#00E5FF;'>{safe_from}</b> ➔ <b style='color:#FFD600;'>{safe_to}</b> : {safe_content}</div>", unsafe_allow_html=True)

            with admin_sub_tabs[2]:
                if st.button("💣 우주 전체 쪽지 DB 초기화", use_container_width=True, type="secondary"):
                    save_db(MESSAGES_FILE, {})  # 👈 MESSAGES_FILE 적용
                    st.success("전체 쪽지 데이터가 소멸되었습니다.")
                    st.rerun()
