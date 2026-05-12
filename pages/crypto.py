# pages/crypto.py
import streamlit as st
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh  # 🚀 자동 새로고침 부품 가져오기
from utils.config import CRYPTO_CONFIG
from utils.core import format_korean_money, sync_user_data, claim_hidden_title
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx  # 👈 save_db 임포트 추가!

def render(market, nw):
    st.title("🪙 가상화폐 거래소")
    
    # 🚀 핵심: 5초(5000ms)마다 이 페이지를 자동으로 새로고침 하라!
    # (유저가 아무것도 안 해도 코인 가격이 실시간으로 춤을 춥니다)
    st_autorefresh(interval=5000, limit=None, key="crypto_auto_refresh")
    
    if 'crypto_data' not in market:
        st.warning("코인 시장 개장 중... 잠시 후 새로고침 해주세요.")
        st.stop()
        
    cdata = market['crypto_data']

    # --- 유저 선택 코인 ID 고정 (비트코인 리셋 방지) ---
    if "selected_crypto_id" not in st.session_state:
        st.session_state.selected_crypto_id = CRYPTO_CONFIG[0]['id']

    def fmt_crypto_price(price):
        if price >= 1_000_000:   return f"₩{price:,.0f}"
        elif price >= 1:         return f"₩{price:,.2f}"
        elif price >= 0.01:      return f"₩{price:,.4f}"
        else:                    return f"₩{price:.8f}"
    
    def fmt_crypto_qty(qty, cid):
        if cid in ['BTC','ETH']:  return f"{qty:.6f}"
        elif cid in ['SOL','HYO']:return f"{qty:.4f}"
        else:                     return f"{qty:,.2f}"

    tab_market, tab_port, tab_trade = st.tabs(["📊 코인 시황", "💼 내 코인 지갑", "⚡ 거래"])
    
    with tab_market:
        st.markdown("### 🔥 실시간 코인 시황")
        st.caption("⚡ 5초마다 자동 업데이트 | 주식보다 최대 3배 높은 변동성")
        rows_html = "<table class='stock-table'><thead><tr><th>코인</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th></tr></thead><tbody>"
        for c in CRYPTO_CONFIG:
            d    = cdata[c['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 and d['history'][-2] > 0 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲" if diff > 0 else "▼" if diff < 0 else "━"
            rows_html += f"<tr><td>{c['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#E2E8F0;'>{fmt_crypto_price(d['price'])}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td></tr>"
        rows_html += "</tbody></table>"
        st.markdown(rows_html, unsafe_allow_html=True)
        
    with tab_port:
        cp_dict = st.session_state.get('crypto_portfolio', {})
        total_eval = 0; total_invested = 0
        if not cp_dict:
            st.info("보유 중인 코인이 없습니다.")
        else:
            rows = []
            for cid, info in cp_dict.items():
                qty = info.get('qty', 0)
                if qty <= 0 or cid not in cdata: continue
                cur_p  = cdata[cid]['price']
                avg_p  = info.get('avg_price', 0)
                inv = qty * avg_p; total_invested += inv
                ev     = qty * cur_p; total_eval += ev
                pnl = ev - inv
                roi    = (cur_p - avg_p) / avg_p * 100 if avg_p > 0 else 0
                rows.append({
                    "코인": f"{cdata[cid]['name']}", 
                    "보유량": fmt_crypto_qty(qty, cid), 
                    "평균단가": fmt_crypto_price(avg_p), 
                    "현재가": fmt_crypto_price(cur_p),
                    "평가액": format_korean_money(int(ev)), 
                    "평가손익": format_korean_money(int(pnl)),
                    "수익률": f"{roi:+.2f}%"
                })
            if rows:
                st.table(pd.DataFrame(rows))
                c1, c2, c3 = st.columns(3)
                c1.metric("💰 총 매수금액", format_korean_money(int(total_invested)))
                c2.metric("🪙 총 평가액", format_korean_money(int(total_eval)))
                c3.metric("📈 총 평가손익", format_korean_money(int(total_eval - total_invested)))

    with tab_trade:
        crypto_ids = [c['id'] for c in CRYPTO_CONFIG]
        
        try:
            default_idx = crypto_ids.index(st.session_state.selected_crypto_id)
        except ValueError:
            default_idx = 0
            
        sel_c = st.selectbox(
            "거래할 코인 선택", 
            crypto_ids, 
            index=default_idx,
            format_func=lambda cid: f"{next(c['icon'] for c in CRYPTO_CONFIG if c['id']==cid)} {cdata[cid]['name']} — {fmt_crypto_price(cdata[cid]['price'])}",
            key="crypto_trade_selectbox"
        )
        
        st.session_state.selected_crypto_id = sel_c
        
        cd    = cdata[sel_c]
        cur_p = cd['price']
 
        my_info = st.session_state.get('crypto_portfolio', {}).get(sel_c, {'qty': 0, 'avg_price': 0})
        my_qty, my_avg = my_info.get('qty', 0), my_info.get('avg_price', 0)
        
        if my_qty > 0:
            my_eval = my_qty * cur_p
            my_roi = (cur_p - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_col, roi_arr = ("#FF4B4B", "▲") if my_roi > 0 else ("#4B9EFF", "▼") if my_roi < 0 else ("#888", "")
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,0,0,0.5)); border:1px solid rgba(255,255,255,0.1); padding:14px; border-radius:10px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>보유량</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{fmt_crypto_qty(my_qty, sel_c)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>평균 단가</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{fmt_crypto_price(my_avg)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>현재 평가액</span><br><b style='color:#FFD600;font-size:1.1rem;'>{format_korean_money(int(my_eval))}</b></div>
                <div style='flex:1; text-align:right;'><span style='color:#94A3B8;font-size:0.85rem;'>수익률</span><br><b style='color:{roi_col};font-size:1.2rem;'>{roi_arr} {my_roi:+.2f}%</b></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:rgba(255,255,255,0.03); border:1px dashed rgba(255,255,255,0.1); padding:12px; border-radius:10px; margin-bottom:18px; color:#888; text-align:center;'>현재 보유 중인 코인이 없습니다.</div>", unsafe_allow_html=True)
        
        tab_buy, tab_sell = st.tabs(["🟢 매수", "🔴 매도"])
        
        with tab_buy:
            current_cash = max(0, int(st.session_state.global_cash))
            buy_won = st.number_input("투자 금액 (원)", min_value=0, step=10_000, max_value=min(current_cash, 9007199254740991), value=0, format="%d", key="coin_buy_input_safe")
            if st.button("🟢 매수하기", use_container_width=True):
                if buy_won <= 0: st.error("금액 입력 오류")
                elif st.session_state.global_cash < buy_won: st.error("잔액 부족!")
                else:
                    qty_to_buy = buy_won / cur_p
                    
                    # 🛡️ [보안] DB 기준 잔액 재확인 (다중 탭 이중 매입 방지)
                    u_fresh = load_db(USERS_FILE, {})
                    uid = st.session_state.logged_in_user
                    db_cash = u_fresh.get(uid, {}).get('cash', 0)
                    
                    if db_cash < buy_won:
                        st.error("❌ 잔액 부족! (DB 재검증 실패)")
                    else:
                        # ✅ [BUG FIX] DB 포트폴리오를 기준으로 업데이트 (세션 상태 불일치 방지)
                        # DB에서 최신 포트폴리오 가져오기 (u_fresh는 방금 로드됨)
                        cp_port = u_fresh[uid].get('crypto_portfolio', {})
                        old = cp_port.get(sel_c, {'qty': 0, 'avg_price': 0})
                        new_q = old['qty'] + qty_to_buy
                        new_a = ((old['qty'] * old['avg_price']) + buy_won) / new_q if new_q > 0 else cur_p
                        cp_port[sel_c] = {'qty': new_q, 'avg_price': new_a}
                        
                        # ✅ [BUG FIX] 현금 차감 + 포트폴리오 업데이트를 단일 저장으로 처리 (원자적)
                        u_fresh[uid]['cash'] = db_cash - buy_won
                        u_fresh[uid]['crypto_portfolio'] = cp_port
                        save_db(USERS_FILE, u_fresh)
                        
                        # 세션 동기화 (DB 기준으로 덮어씀)
                        st.session_state.global_cash = db_cash - buy_won
                        st.session_state.crypto_portfolio = cp_port
                        
                        log_tx(uid, "코인매수", f"{cd['name']} 매수", -int(buy_won))
                        sync_user_data()
                        st.success("✅ 매수 완료!")
                        if sel_c == "HYO" and buy_won >= 1_000_000_000_000_000: 
                            claim_hidden_title("pepe_all_in", "👑 [유일무이] 상남자특_김효민_믿음")
                        st.rerun()
                    
        with tab_sell:
            actual_holding = st.session_state.get('crypto_portfolio', {}).get(sel_c, {}).get('qty', 0)
            if actual_holding <= 1e-10:
                st.info("보유 중인 코인이 없습니다.")
            else:
                sell_pct = st.slider("매도 비율", min_value=1, max_value=100, value=100, step=1, format="%d%%")
                sell_qty = actual_holding * sell_pct / 100
                sell_won = sell_qty * cur_p
                st.caption(f"예상 수령액: {format_korean_money(int(sell_won))}")
                if st.button(f"🔴 매도하기", use_container_width=True):
                    # ✅ [BUG FIX] 매도도 DB 재검증 후 원자적 저장
                    u_sell = load_db(USERS_FILE, {})
                    uid_sell = st.session_state.logged_in_user
                    db_port = u_sell.get(uid_sell, {}).get('crypto_portfolio', {})
                    actual_qty = db_port.get(sel_c, {}).get('qty', 0)
                    if actual_qty <= 1e-10:
                        st.error(f"⚠️ 보유량이 없습니다! (DB 재검증 실패)")
                    else:
                        real_sell_qty = min(sell_qty, actual_qty)
                        real_sell_won = real_sell_qty * cur_p
                        db_port[sel_c]['qty'] -= real_sell_qty
                        if db_port[sel_c]['qty'] < 1e-10: del db_port[sel_c]
                        db_cash_sell = u_sell[uid_sell].get('cash', 0)
                        # ✅ 현금 추가 + 포트폴리오 차감을 단일 저장으로 처리 (원자적)
                        u_sell[uid_sell]['cash'] = db_cash_sell + int(real_sell_won)
                        u_sell[uid_sell]['crypto_portfolio'] = db_port
                        save_db(USERS_FILE, u_sell)
                        # 세션 동기화 (DB 기준)
                        st.session_state.crypto_portfolio = db_port
                        st.session_state.global_cash = db_cash_sell + int(real_sell_won)
                        log_tx(uid_sell, "코인매도", f"{cd['name']} 매도", int(real_sell_won))
                        sync_user_data(); st.success("✅ 매도 완료!"); st.rerun()
