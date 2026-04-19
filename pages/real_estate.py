# pages/real_estate.py
import streamlit as st
import time
import uuid
from datetime import datetime
from utils.config import estate_config, KST, USERS_FILE
from utils.database import load_db, save_db, log_tx, load_estate_market, save_estate_market, get_estate_initial_listings, save_market
from utils.core import format_korean_money, sync_user_data, cooldown_remaining, set_cooldown, claim_hidden_title

def render(market, nw):
    st.title("🏢 부동산 실거래 마켓")

    uid = st.session_state.logged_in_user
    now = time.time()

    pass_s = int(now - st.session_state.rent_time)
    pass_s = max(0, pass_s)
    if pass_s >= 86400:
        st.session_state.rent_time = now - 86400
        pass_s = 86400
        sync_user_data()
        
    total_income_rate = sum(
        estate_config[eid]['income'] * cnt
        for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
    )
    pending = total_income_rate * pass_s

    if total_income_rate > 0:
        st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,100,50,0.1));
     border:1px solid rgba(0,255,136,0.3);border-radius:14px;padding:18px;text-align:center;margin-bottom:16px;'>
  <div style='color:#888;font-size:0.82rem;letter-spacing:2px;margin-bottom:6px;'>누적 임대 수익</div>
  <div style='font-family:Orbitron,monospace;font-size:1.8rem;font-weight:900;color:#00FF88;'>{format_korean_money(pending)}</div>
  <div style='color:#888;font-size:0.78rem;margin-top:6px;'>초당 {format_korean_money(total_income_rate)} 수입 중</div>
</div>""", unsafe_allow_html=True)

        cd_rent = cooldown_remaining("rent_collect", 3.0)
        if cd_rent > 0:
            st.warning(f"⏱️ 수금 쿨다운 {cd_rent:.1f}초")
        elif st.button("💰 임대 수익 수금하기", use_container_width=True):
            set_cooldown("rent_collect")
            if pending > 0:
                st.session_state.global_cash += int(pending)
                st.session_state.rent_time = now
                sync_user_data()
                log_tx(uid, "부동산수금", "임대 수익 수금", int(pending))
                st.success(f"✅ {format_korean_money(pending)} 수금 완료!")
                st.rerun()

    st.write("---")

    em = load_estate_market()
    initial_listings = get_estate_initial_listings(em)

    tab_market_view, tab_my_estate, tab_sell = st.tabs(["🏪 마켓 (전체 매물)", "🏘️ 내 보유 부동산", "📋 판매 등록"])

    with tab_market_view:
        st.markdown("### 🏗️ 신규 공급 매물 (운영사 직판)")
        st.caption("수량 제한 있음 — 소진 시 유저 매물만 구매 가능")

        if not initial_listings:
            st.info("현재 신규 공급 매물이 없습니다. 유저 매물을 확인하세요!")
        else:
            for il in initial_listings:
                eid  = il["eid"]
                info = estate_config[eid]
                c1, c2 = st.columns([5, 2])
                with c1:
                    st.markdown(f"""
<div class='market-initial' style='background: rgba(0, 255, 136, 0.05); border: 1px solid rgba(0, 255, 136, 0.2); border-radius: 12px; padding: 16px 20px; margin: 8px 0;'>
  <div style='display:flex;align-items:center;gap:10px;'>
    <span style='font-size:1.8rem;'>{info['icon']}</span>
    <div>
      <div style='font-weight:900;font-size:1rem;color:#E2E8F0;'>{info['name']}</div>
      <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
      <div style='margin-top:4px;'>
        <span style='color:#FFD600;font-weight:900;'>{format_korean_money(info['base_price'])}</span>
        <span style='color:#777;margin:0 8px;'>|</span>
        <span style='color:#00FF88;font-weight:900;font-size:0.9rem;'>+{format_korean_money(info['income'])}/초</span>
        <span style='color:#888;margin-left:10px;font-size:0.78rem;'>잔여 {il['remaining']}개</span>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                with c2:
                    can_buy = st.session_state.global_cash >= info['base_price']
                    cd_key  = f"estate_buy_{eid}_initial"
                    cd_rem  = cooldown_remaining(cd_key, 4.0)
                    if cd_rem > 0:
                        st.warning(f"⏱️ {cd_rem:.1f}초")
                    elif st.button("🏗️ 매입" if can_buy else "💸 잔액부족", key=f"init_buy_{eid}", use_container_width=True, disabled=not can_buy):
                        em2 = load_estate_market()
                        il2 = next((x for x in get_estate_initial_listings(em2) if x["eid"] == eid), None)
                        if il2 is None or il2["remaining"] <= 0:
                            st.error("⚠️ 이미 매진되었습니다! 유저 매물을 확인하세요.")
                        elif st.session_state.global_cash >= info['base_price']:
                            set_cooldown(cd_key)
                            
                            # 🛡️ [보안] DB 기준 잔액 재확인 (다중 탭 이중 매입 방지)
                            u_fresh = load_db(USERS_FILE, {})
                            db_cash = u_fresh.get(uid, {}).get('cash', 0)
                            
                            if db_cash < info['base_price']:
                                st.error("❌ 잔액 부족! (DB 재검증 실패)")
                            else:
                                # DB 잔액 원자적 차감
                                u_fresh[uid]['cash'] = db_cash - info['base_price']
                                save_db(USERS_FILE, u_fresh)
                                
                                # 세션 동기화
                                st.session_state.global_cash = u_fresh[uid]['cash']
                                if 'real_estate' not in st.session_state:
                                    st.session_state.real_estate = {}
                                st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                                sync_user_data()

                                if uid not in em2["owner_counts"]: em2["owner_counts"][uid] = {}
                                em2["owner_counts"][uid][eid] = em2["owner_counts"][uid].get(eid, 0) + 1
                                save_estate_market(em2)
                                
                                log_tx(uid, "부동산매입", f"{info['name']} 신규 매입", -info['base_price'])
                                
                                owned_types = sum(1 for e, c in st.session_state.real_estate.items() if c > 0)
                                if owned_types == len(estate_config): claim_hidden_title("real_estate_monopoly", "👑 [유일무이] 진짜 부루마불 우승자")
                                st.success(f"✅ {info['name']} 매입 완료!"); st.rerun()

        st.write("---")
        st.markdown("### 🔄 유저 매물 (2차 시장)")
        st.caption("다른 유저가 판매 등록한 매물입니다. 판매자에게 대금이 지급됩니다.")

        user_listings = [l for l in em["listings"] if l["seller"] != uid]
        if not user_listings:
            st.info("현재 등록된 유저 매물이 없습니다.")
        else:
            listings_by_eid = {}
            for l in user_listings: listings_by_eid.setdefault(l["eid"], []).append(l)

            for eid, llist in listings_by_eid.items():
                info = estate_config.get(eid)
                if not info: continue
                llist_sorted = sorted(llist, key=lambda x: x["price"])
                st.markdown(f"#### {info['icon']} {info['name']} — {len(llist)}건 매물")
                for li in llist_sorted:
                    premium = (li['price'] - info['base_price']) / info['base_price'] * 100
                    prem_str = f"+{premium:.1f}%" if premium > 0 else f"{premium:.1f}%"
                    prem_col = "#FF4B4B" if premium > 0 else "#4B9EFF"
                    c1, c2 = st.columns([5, 2])
                    with c1:
                        st.markdown(f"""
<div style='background:rgba(0, 229, 255, 0.05); border:1px solid rgba(0, 229, 255, 0.2); border-radius:12px; padding:16px 20px; margin:8px 0;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div>
      <span style='color:#94A3B8;font-size:0.8rem;'>판매자: </span>
      <b style='color:#00E5FF;'>{li['seller']}</b>
      <span style='color:{prem_col};font-size:0.78rem;margin-left:10px;'>{prem_str} (기준가 대비)</span>
    </div>
    <div style='text-align:right;'>
      <div style='font-size:1.1rem;font-weight:900;color:#FFD600;'>{format_korean_money(li['price'])}</div>
      <div style='color:#00FF88;font-weight:900;font-size:0.9rem;'>+{format_korean_money(info['income'])}/초</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                    with c2:
                        can_buy = st.session_state.global_cash >= li['price']
                        cd_key  = f"estate_buy_{li['id']}"
                        cd_rem  = cooldown_remaining(cd_key, 4.0)
                        if cd_rem > 0:
                            st.warning(f"⏱️ {cd_rem:.1f}초")
                        elif st.button("🛒 구매" if can_buy else "💸 잔액부족", key=f"buy_listing_{li['id']}", use_container_width=True, disabled=not can_buy):
                            em3 = load_estate_market()
                            target = next((x for x in em3["listings"] if x["id"] == li["id"]), None)
                            
                            if target is None:
                                st.error("⚠️ 이미 판매된 매물입니다.")
                            elif st.session_state.global_cash >= target["price"]:
                                set_cooldown(cd_key)
                                
                                # 🛡️ [보안] DB 기준 잔액 재확인 (유저 매물 구매 시 다중 탭 방지)
                                u_fresh = load_db(USERS_FILE, {})
                                db_cash = u_fresh.get(uid, {}).get('cash', 0)
                                
                                if db_cash < target["price"]:
                                    st.error("❌ 잔액 부족! (DB 재검증 실패)")
                                else:
                                    # 구매자의 DB 잔액 원자적 차감
                                    u_fresh[uid]['cash'] = db_cash - target["price"]
                                    save_db(USERS_FILE, u_fresh)
                                    
                                    # 구매자의 세션 동기화
                                    st.session_state.global_cash = u_fresh[uid]['cash']
                                    if 'real_estate' not in st.session_state:
                                        st.session_state.real_estate = {}
                                    st.session_state.real_estate[eid] = st.session_state.real_estate.get(eid, 0) + 1
                                    sync_user_data()

                                    if uid not in em3["owner_counts"]: em3["owner_counts"][uid] = {}
                                    em3["owner_counts"][uid][eid] = em3["owner_counts"][uid].get(eid, 0) + 1
                                    
                                    # 판매자에게 대금 지급 (이미 위에서 load_db 했으므로 u_fresh 재사용)
                                    seller = target["seller"]
                                    if seller in u_fresh:
                                        u_fresh[seller]['cash'] += target["price"]
                                        if seller not in em3["owner_counts"]: em3["owner_counts"][seller] = {}
                                        em3["owner_counts"][seller][eid] = max(0, em3["owner_counts"][seller].get(eid, 0) - 1)
                                        if 'real_estate' in u_fresh[seller] and eid in u_fresh[seller]['real_estate']:
                                            u_fresh[seller]['real_estate'][eid] = max(0, u_fresh[seller]['real_estate'][eid] - 1)
                                            if u_fresh[seller]['real_estate'][eid] <= 0: del u_fresh[seller]['real_estate'][eid]
                                        save_db(USERS_FILE, u_fresh) # 판매자 잔액 업데이트 저장
                                        log_tx(seller, "부동산판매", f"{info['name']} 판매 완료", target["price"])
                                    
                                    em3["listings"] = [x for x in em3["listings"] if x["id"] != li["id"]]
                                    save_estate_market(em3)
                                    log_tx(uid, "부동산구매", f"{info['name']} 유저 매물 구매", -target["price"])
                                    
                                    market['news'] = f"🏢 [{uid}] {info['name']} 유저 매물 구매 완료!"
                                    save_market(market)
                                    
                                    owned_types = sum(1 for e, c in st.session_state.real_estate.items() if c > 0)
                                    if owned_types == len(estate_config): claim_hidden_title("real_estate_monopoly", "👑 [유일무이] 진짜 부루마불 우승자")
                                    st.success(f"✅ {info['name']} 구매 완료! {format_korean_money(target['price'])}")
                                    st.rerun()

    with tab_my_estate:
        owned_any = any(v > 0 for v in st.session_state.real_estate.values())
        if not owned_any:
            st.info("보유 중인 부동산이 없습니다. 마켓에서 매입하세요!")
        else:
            for eid, cnt in st.session_state.real_estate.items():
                if cnt <= 0 or eid not in estate_config: continue
                info = estate_config[eid]
                my_listed = sum(1 for l in em["listings"] if l["eid"] == eid and l["seller"] == uid)
                available_to_sell = cnt - my_listed
                st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(255,255,255,0.03),rgba(0,0,0,0.2));border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:18px 22px;margin:10px 0;'>
  <div style='display:flex;justify-content:space-between;align-items:center;'>
    <div style='display:flex;align-items:center;gap:12px;'>
      <span style='font-size:2rem;'>{info['icon']}</span>
      <div>
        <div style='font-weight:900;font-size:1.05rem;color:#E2E8F0;'>{info['name']}</div>
        <div style='color:#888;font-size:0.8rem;'>{info['desc']}</div>
        <div style='margin-top:4px;'>
          <span style='color:#94A3B8;font-size:0.82rem;'>보유 {cnt}채 (판매 등록 {my_listed}채)</span>
          <span style='color:#777;margin:0 8px;'>|</span>
          <span style='color:#00FF88;font-weight:900;font-size:0.9rem;'>+{format_korean_money(info['income'] * cnt)}/초</span>
        </div>
      </div>
    </div>
    <div style='text-align:right;'>
      <div style='color:#888;font-size:0.78rem;'>현재 평가액</div>
      <div style='color:#FFD600;font-weight:900;'>{format_korean_money(info['base_price'] * cnt * 0.8)}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                if available_to_sell > 0:
                    st.caption(f"👆 판매 등록 가능: {available_to_sell}채 → '판매 등록' 탭에서 진행하세요")
                elif my_listed > 0:
                    st.caption("⏳ 모든 물건이 판매 등록 중입니다.")

    with tab_sell:
        st.markdown("### 📋 내 매물 판매 등록")
        st.caption("판매 등록 후 다른 유저가 구매하면 현금이 즉시 입금됩니다. 거래 수수료: **2%**")

        sellable = [(eid, cnt) for eid, cnt in st.session_state.real_estate.items() if cnt > 0 and eid in estate_config]
        sellable_net = []
        for eid, cnt in sellable:
            my_listed = sum(1 for l in em["listings"] if l["eid"] == eid and l["seller"] == uid)
            if cnt - my_listed > 0:
                sellable_net.append((eid, cnt, my_listed))

        if not sellable_net:
            st.info("판매 등록 가능한 부동산이 없습니다. 모두 이미 등록되었거나 보유가 없습니다.")
        else:
            sel_eid = st.selectbox("판매할 부동산 선택", [e for e, c, ml in sellable_net], format_func=lambda e: f"{estate_config[e]['icon']} {estate_config[e]['name']} (판매 가능 {dict({e:(c-ml) for e,c,ml in sellable_net}).get(e,0)}채)")
            sel_info = estate_config[sel_eid]
            min_price = int(sel_info['base_price'] * 0.5)
            max_price = int(sel_info['base_price'] * 3.0)
            sell_price = st.number_input(f"판매 희망가 (기준가: {format_korean_money(sel_info['base_price'])})", min_value=min_price, max_value=max_price, value=sel_info['base_price'], step=int(sel_info['base_price'] * 0.01), format="%d")
            fee = int(sell_price * 0.02)
            net_receive = sell_price - fee
            st.caption(f"📌 판매 시 수수료 **2%** ({format_korean_money(fee)}) 공제 → 실수령 {format_korean_money(net_receive)}")

            cd_list_rem = cooldown_remaining("estate_list", 5.0)
            if cd_list_rem > 0:
                st.warning(f"⏱️ 등록 쿨다운 {cd_list_rem:.1f}초")
            elif st.button("📋 판매 등록하기", use_container_width=True):
                set_cooldown("estate_list")
                new_listing = {
                    "id": str(uuid.uuid4())[:8], "eid": sel_eid, "seller": uid, "price": sell_price,
                    "net_receive": net_receive, "listed_time": time.time()
                }
                em_fresh = load_estate_market()
                em_fresh["listings"].append(new_listing)
                save_estate_market(em_fresh)
                market['news'] = f"🏢 [{uid}] {sel_info['name']} {format_korean_money(sell_price)}에 매물 등록!"
                save_market(market)
                st.success(f"✅ {sel_info['name']} 판매 등록 완료! 구매자 대기 중...")
                st.rerun()

        st.write("---")
        st.markdown("### 🗂️ 내 등록 매물 관리")
        my_listings = [l for l in em["listings"] if l["seller"] == uid]
        if not my_listings:
            st.info("현재 등록된 매물이 없습니다.")
        else:
            for li in my_listings:
                info = estate_config.get(li["eid"], {})
                listed_dt = datetime.fromtimestamp(li.get("listed_time", 0), KST).strftime("%m/%d %H:%M")
                c1, c2 = st.columns([5, 2])
                with c1:
                    st.markdown(f"""
<div style='background:rgba(255,214,0,0.05); border:1px solid rgba(255,214,0,0.2); border-radius:12px; padding:16px 20px; margin:8px 0;'>
  <div style='display:flex;justify-content:space-between;'>
    <div>
      <span style='font-size:1.2rem;'>{info.get('icon','🏠')}</span>
      <b style='color:#E2E8F0;margin-left:8px;'>{info.get('name','?')}</b>
      <span style='color:#888;font-size:0.78rem;margin-left:8px;'>등록: {listed_dt}</span>
    </div>
    <div style='text-align:right;'>
      <div style='color:#FFD600;font-weight:900;'>{format_korean_money(li['price'])}</div>
      <div style='color:#888;font-size:0.78rem;'>실수령 {format_korean_money(li.get('net_receive', li['price']))}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)
                with c2:
                    if st.button("❌ 등록 취소", key=f"cancel_{li['id']}", use_container_width=True):
                        em_fresh = load_estate_market()
                        em_fresh["listings"] = [x for x in em_fresh["listings"] if x["id"] != li["id"]]
                        save_estate_market(em_fresh)
                        st.success("매물 등록 취소 완료!")
                        st.rerun()
