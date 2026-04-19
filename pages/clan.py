# pages/clan.py
import streamlit as st
import time
import html
import re
from utils.config import USERS_FILE
from utils.core import format_korean_money, sync_user_data, get_clan_total_nw
from utils.database import load_clan_db, save_clan_db, get_user_clan, load_db, save_db, log_tx, save_market

def render(market, nw):
    st.title("🏰 클랜 관리 사무소")
    uid = st.session_state.logged_in_user
    clans = load_clan_db()
    my_clan = get_user_clan(uid)

    def has_perm(user_id, clan_data, perm_name):
        if clan_data['leader'] == user_id: return True
        u_rank = clan_data.get('member_ranks', {}).get(user_id, "일반멤버")
        rank_perms = {
            "클랜장":   {"출금": True, "추방": True, "가입승인": True, "계급관리": True, "위임": True},
            "부클랜장": {"출금": True, "추방": True, "가입승인": True, "계급관리": False, "위임": False},
            "운영진":   {"출금": False, "추방": False, "가입승인": True, "계급관리": False, "위임": False},
            "일반멤버": {"출금": False, "추방": False, "가입승인": False, "계급관리": False, "위임": False}
        }
        return rank_perms.get(u_rank, rank_perms["일반멤버"]).get(perm_name, False)

    tab_my, tab_list, tab_rank = st.tabs(["🏠 내 클랜", "🔍 클랜 목록", "🏆 클랜 랭킹"])

    with tab_my:
        if my_clan is None:
            st.info("소속된 클랜이 없습니다. 새로운 세력을 구축하거나 기존 클랜에 가입하세요!")
            st.write("---")
            st.markdown("### ⚔️ 새 클랜 창설")
            st.caption("창설 비용: 10억원 | 당신은 자동으로 '클랜장'이 됩니다.")
            new_clan_name = st.text_input("클랜 이름", max_chars=10)
            new_clan_desc = st.text_input("클랜 한줄 소개", max_chars=30)
            new_clan_icon = st.selectbox("아이콘", ["🏰","⚔️","🐉","🔥","💀","🌙","🌊","⚡","🦁","🐺"])
            
            if st.button("🏰 클랜 창설 (10억)", use_container_width=True):
                clean_clan_name = new_clan_name.strip()
                # 🛡️ 주의 #5: 클랜명 특수문자 필터링 — 한글·영문·숫자·공백·이모지 허용, HTML 특수문자 차단
                if not clean_clan_name:
                    st.error("이름을 입력하세요.")
                elif not re.match(r'^[a-zA-Z0-9가-힣 _\-!?.★☆♥♦♣♠🏰⚔️🐉🔥💀🌙🌊⚡🦁🐺]{1,10}$', clean_clan_name):
                    st.error("⚠️ 클랜명에 사용할 수 없는 특수문자가 포함되어 있습니다.")
                elif clean_clan_name in clans:
                    st.error("이미 있는 이름입니다.")
                elif st.session_state.global_cash < 1_000_000_000:
                    st.error("돈이 부족합니다.")
                else:
                    # 🛡️ 버그 #1: DB 잔액 재검증 후 차감
                    us_fresh = load_db(USERS_FILE, {})
                    db_cash = us_fresh.get(uid, {}).get('cash', 0)
                    if db_cash < 1_000_000_000:
                        st.error("잔액이 부족합니다. (DB 재검증 실패)")
                    else:
                        us_fresh[uid]['cash'] = db_cash - 1_000_000_000
                        save_db(USERS_FILE, us_fresh)
                        st.session_state.global_cash = us_fresh[uid]['cash']
                        clans[clean_clan_name] = {
                            "leader": uid, "members": [uid], "member_ranks": {uid: "클랜장"},
                            "bank": 0, "desc": new_clan_desc, "icon": new_clan_icon,
                            "created": time.time(), "join_requests": [],
                        }
                        save_clan_db(clans)
                        log_tx(uid, "클랜", f"[{clean_clan_name}] 창설", -1_000_000_000)
                        st.rerun()

            st.write("---")
            st.markdown("### 🚪 가입 신청")
            if clans:
                join_target = st.selectbox("가입할 클랜", list(clans.keys()), format_func=lambda n: f"{clans[n]['icon']} {n}")
                if st.button("📨 신청서 보내기", use_container_width=True):
                    if uid in clans[join_target].get('join_requests', []): st.warning("이미 신청했습니다.")
                    else:
                        clans[join_target].setdefault('join_requests', []).append(uid)
                        save_clan_db(clans); st.success("신청 완료!")

        else:
            cdata = clans[my_clan]
            if 'member_ranks' not in cdata:
                cdata['member_ranks'] = {m: ("클랜장" if m == cdata['leader'] else "일반멤버") for m in cdata['members']}
            
            rank_map = {"Leader": "클랜장", "Vice": "부클랜장", "Manager": "운영진", "Member": "일반멤버"}
            for m, r in cdata['member_ranks'].items():
                if r in rank_map: cdata['member_ranks'][m] = rank_map[r]

            my_rank = cdata['member_ranks'].get(uid, "일반멤버")

            # 🛡️ XSS 방어: 내 클랜 카드 렌더링 전 모든 문자열 이스케이프
            s_my_clan = html.escape(my_clan)
            s_my_rank = html.escape(my_rank)
            s_uid     = html.escape(uid)
            s_desc    = html.escape(cdata.get('desc', ''))

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(0,229,255,0.1),rgba(0,100,255,0.05));
                 border:2px solid #00E5FF;border-radius:16px;padding:24px;text-align:center;'>
              <div style='font-size:3rem;'>{cdata['icon']}</div>
              <div style='font-size:1.8rem;font-weight:900;color:#FFF;'>{s_my_clan}</div>
              <div style='color:#00E5FF;font-weight:700;'>{s_my_rank} {s_uid}</div>
              <div style='color:#888;margin-top:8px;'>"{s_desc}"</div>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            col_a, col_b = st.columns(2)
            col_a.metric("🏦 클랜 자금", format_korean_money(cdata.get('bank', 0)))
            col_b.metric("💪 클랜 전투력(순자산)", format_korean_money(get_clan_total_nw(my_clan, market)))

            with st.expander("🏦 클랜 금고 (입/출금)"):
                c_dep, c_wit = st.columns(2)
                with c_dep:
                    d_amt = st.number_input("입금액", min_value=0, step=10_000_000, format="%d", key="d_in")
                    if st.button("💰 금고 채우기", use_container_width=True):
                        if d_amt <= 0:
                            st.error("금액을 입력하세요.")
                        else:
                            # 🛡️ 버그 #1 수정: DB 잔액 재검증 후 차감 (다중탭 이중입금 방지)
                            us_fresh = load_db(USERS_FILE, {})
                            db_cash = us_fresh.get(uid, {}).get('cash', 0)
                            if db_cash < d_amt:
                                st.error("잔액이 부족합니다. (DB 재검증 실패)")
                            else:
                                us_fresh[uid]['cash'] = db_cash - d_amt
                                save_db(USERS_FILE, us_fresh)
                                st.session_state.global_cash = us_fresh[uid]['cash']
                                # clan DB는 users DB 저장 완료 후 반영
                                clans_fresh = load_clan_db()
                                if my_clan in clans_fresh:
                                    clans_fresh[my_clan]['bank'] = clans_fresh[my_clan].get('bank', 0) + d_amt
                                    save_clan_db(clans_fresh)
                                log_tx(uid, "클랜", f"[{my_clan}] 금고 입금", -d_amt)
                                st.success(f"✅ {format_korean_money(d_amt)} 입금 완료!")
                                st.rerun()
                with c_wit:
                    w_amt = st.number_input("출금액", min_value=0, step=10_000_000, format="%d", key="w_in")
                    can_w = has_perm(uid, cdata, "출금")
                    if st.button("🏧 금고에서 꺼내기", use_container_width=True, disabled=not can_w):
                        if w_amt <= 0:
                            st.error("금액을 입력하세요.")
                        else:
                            # 🛡️ 버그 #1 수정: 클랜 DB 재조회로 최신 금고 잔액 검증
                            clans_fresh = load_clan_db()
                            bank_now = clans_fresh.get(my_clan, {}).get('bank', 0)
                            if w_amt > bank_now:
                                st.error("금고 잔액이 부족합니다. (DB 재검증 실패)")
                            else:
                                clans_fresh[my_clan]['bank'] = bank_now - w_amt
                                save_clan_db(clans_fresh)
                                st.session_state.global_cash += w_amt
                                sync_user_data()
                                log_tx(uid, "클랜", f"[{my_clan}] 금고 출금", w_amt)
                                st.success(f"✅ {format_korean_money(w_amt)} 출금 완료!")
                                st.rerun()
                    if not can_w: st.caption("🔒 부클랜장 이상만 출금 가능")

            with st.expander("👥 멤버 목록 및 계급 관리"):
                can_rank = has_perm(uid, cdata, "계급관리")
                can_kick = has_perm(uid, cdata, "추방")
                can_lead = has_perm(uid, cdata, "위임")

                for m in cdata['members']:
                    m_rank = cdata['member_ranks'].get(m, "일반멤버")
                    col_m1, col_m2, col_m3 = st.columns([2, 1, 1])
                    with col_m1:
                        st.write(f"**{m}** [{m_rank}]")
                    with col_m2:
                        if can_rank and m != uid:
                            new_r = st.selectbox("계급 변경", ["일반멤버", "운영진", "부클랜장"], 
                                                 index=["일반멤버", "운영진", "부클랜장"].index(m_rank) if m_rank in ["일반멤버", "운영진", "부클랜장"] else 0,
                                                 key=f"r_sel_{m}", label_visibility="collapsed")
                            if new_r != m_rank:
                                cdata['member_ranks'][m] = new_r
                                save_clan_db(clans); st.rerun()
                    with col_m3:
                        if can_kick and m != uid and m != cdata['leader']:
                            if st.button("🦶 추방", key=f"k_{m}", use_container_width=True):
                                cdata['members'].remove(m)
                                if m in cdata['member_ranks']: del cdata['member_ranks'][m]
                                save_clan_db(clans); st.rerun()

                if can_lead:
                    st.write("---")
                    st.markdown("#### 👑 클랜장 직위 위임")
                    successors = [m for m in cdata['members'] if m != uid]
                    if successors:
                        target_lead = st.selectbox("직위를 넘겨줄 멤버", successors)
                        if st.button(f"🤝 {target_lead}에게 클랜장 위임", use_container_width=True):
                            cdata['leader'] = target_lead
                            cdata['member_ranks'][target_lead] = "클랜장"
                            cdata['member_ranks'][uid] = "부클랜장"
                            save_clan_db(clans)
                            market['news'] = f"🏰 [{my_clan}] 클랜의 수장이 {uid}님에서 {target_lead}님으로 교체되었습니다!"
                            save_market(market); st.success("위임 완료!"); st.rerun()

            if has_perm(uid, cdata, "가입승인"):
                with st.expander(f"📥 가입 신청 현황 ({len(cdata.get('join_requests', []))})"):
                    reqs = cdata.get('join_requests', [])
                    if not reqs: st.info("신청자가 없습니다.")
                    for r_uid in reqs:
                        rc1, rc2, rc3 = st.columns([2, 1, 1])
                        rc1.write(f"👤 {r_uid}")
                        if rc2.button("승인", key=f"a_{r_uid}"):
                            cdata['members'].append(r_uid)
                            cdata['member_ranks'][r_uid] = "일반멤버"
                            cdata['join_requests'].remove(r_uid)
                            save_clan_db(clans); st.rerun()
                        if rc3.button("거절", key=f"j_{r_uid}"):
                            cdata['join_requests'].remove(r_uid)
                            save_clan_db(clans); st.rerun()

            st.write("---")
            if st.button("🚪 클랜 탈퇴 / 해산", use_container_width=True):
                if uid == cdata['leader'] and len(cdata['members']) > 1:
                    st.error("멤버가 남아있을 때는 해산할 수 없습니다. 위임을 먼저 하거나 멤버를 전부 추방하세요.")
                elif uid == cdata['leader']:
                    del clans[my_clan]; save_clan_db(clans); st.rerun()
                else:
                    cdata['members'].remove(uid)
                    if uid in cdata['member_ranks']: del cdata['member_ranks'][uid]
                    save_clan_db(clans); st.rerun()

    with tab_list:
        st.markdown("### 🔍 전체 클랜 목록")
        for cn, cd in clans.items():
            # 🛡️ XSS 방어: 클랜 목록 렌더링 전 이름과 리더 닉네임 이스케이프 처리
            s_cn     = html.escape(cn)
            s_leader = html.escape(cd['leader'])
            st.markdown(f"<div class='card'>{cd['icon']} <b>{s_cn}</b> | 클랜장: {s_leader} | 멤버: {len(cd['members'])}명</div>", unsafe_allow_html=True)
            
    with tab_rank:
        st.markdown("### 🏆 클랜 자산 순위")
        # st.write()는 기본적으로 자동 이스케이프가 되므로 안전합니다!
        ranked = sorted([(cn, get_clan_total_nw(cn, market), cd) for cn, cd in clans.items()], key=lambda x: x[1], reverse=True)
        for i, (cn, tot, cd) in enumerate(ranked[:10]):
            st.write(f"{i+1}위. {cd['icon']} {cn} - {format_korean_money(tot)}")
