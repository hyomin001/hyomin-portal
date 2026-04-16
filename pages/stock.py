# pages/stock.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.config import stock_config, KST
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.config import USERS_FILE
from utils.database import load_db, log_tx, save_market

def render(market, nw):
    st.title("📈 통합 거래소")

    TRADE_COOLDOWN   = 3.0  
    BULK_COOLDOWN    = 8.0  
    DAILY_BULK_LIMIT = 5    

    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    if st.session_state.get("bulk_trade_date") != today_str:
        st.session_state.bulk_trade_date  = today_str
        st.session_state.bulk_trade_count = 0

    tab_market, tab_port, tab_trade = st.tabs(["📊 전체 시황", "💼 내 포트폴리오", "⚡ 빠른 거래"])

    with tab_market:
        rows = ""
        for s in stock_config:
            d    = market['stock_data'][s['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲"   if diff > 0 else "▼"        if diff < 0 else "━"
            rows += f"<tr><td>{s['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#E2E8F0;'>₩{d['price']:,}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td><td style='text-align:right;color:#888;'>₩{d['history'][-2]:,}</td></tr>"
        st.markdown(f"<table class='stock-table'><thead><tr><th>종목</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th><th style='text-align:right;'>전일가</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

    with tab_port:
        p_rows = []; total_eval = 0; total_invested = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp  = market['stock_data'][sid]['price']
                ap  = info.get('avg_price', 0)
                inv = qty * ap; total_invested += inv
                ev  = qty * cp; total_eval += ev
                pnl = ev - inv
                roi = (cp - ap) / ap * 100 if ap > 0 else 0
                p_rows.append({
                    "종목": market['stock_data'][sid]['name'], 
                    "수량": f"{qty}주", "평균단가": f"₩{int(ap):,}", "현재가": f"₩{int(cp):,}",
                    "평가액": f"₩{int(ev):,}", "평가손익": f"₩{int(pnl):,}", "수익률": f"{roi:+.2f}%"
                })
        if p_rows:
            st.table(pd.DataFrame(p_rows))
            c1, c2, c3 = st.columns(3)
            c1.metric("💰 총 매수금액", format_korean_money(total_invested))
            c2.metric("📊 총 평가액", format_korean_money(total_eval))
            c3.metric("📈 총 평가손익", format_korean_money(total_eval - total_invested))
        else:
            st.info("보유 중인 주식이 없습니다.")

    with tab_trade:
        sel_n = st.selectbox("거래 종목 선택", [f"{s['icon']} {s['name']}" for s in stock_config])
        sid   = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        d     = market['stock_data'][sid]
        cp    = d['price']

        if len(d['history']) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=d['history'], mode='lines', line=dict(color='#00E5FF', width=2), fill='tozeroy', fillcolor='rgba(0,229,255,0.05)'))
            fig.update_layout(height=220, template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
            st.plotly_chart(fig, use_container_width=True)

        diff = cp - d['history'][-2] if len(d['history']) > 1 else 0
        pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        clr  = "#FF4B4B" if diff >= 0 else "#4B9EFF"
        arr  = "▲" if diff >= 0 else "▼"
        st.markdown(f"<div style='text-align:center;margin:10px 0;'><span style='font-size:1.8rem;font-weight:900;color:#E2E8F0;font-family:Orbitron;'>₩{cp:,}</span> <span style='color:{clr};font-weight:900;'>{arr} {abs(pct):.2f}%</span></div>", unsafe_allow_html=True)

        my_info = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
        my_qty, my_avg = my_info.get('qty', 0), my_info.get('avg_price', 0)
        
        if my_qty > 0:
            my_eval = my_qty * cp
            my_roi = (cp - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_col, roi_arr = ("#FF4B4B", "▲") if my_roi > 0 else ("#4B9EFF", "▼") if my_roi < 0 else ("#888", "")
            st.markdown(f"""
            <div style='background:linear-gradient(135deg, rgba(255,255,255,0.05), rgba(0,0,0,0.5)); border:1px solid rgba(255,255,255,0.1); padding:14px; border-radius:10px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;'>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>보유 수량</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{my_qty}주</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>평균 단가</span><br><b style='color:#E2E8F0;font-size:1.1rem;'>{format_korean_money(my_avg)}</b></div>
                <div style='flex:1;'><span style='color:#94A3B8;font-size:0.85rem;'>현재 평가액</span><br><b style='color:#FFD600;font-size:1.1rem;'>{format_korean_money(my_eval)}</b></div>
                <div style='flex:1; text-align:right;'><span style='color:#94A3B8;font-size:0.85rem;'>수익률</span><br><b style='color:{roi_col};font-size:1.2rem;'>{roi_arr} {my_roi:+.2f}%</b></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background:rgba(255,255,255,0.03); border:1px dashed rgba(255,255,255,0.1); padding:12px; border-radius:10px; margin-bottom:18px; color:#888; text-align:center;'>현재 보유 중인 주식이 없습니다.</div>", unsafe_allow_html=True)

        qty_input = st.number_input("거래 수량 (주)", min_value=1, step=1, value=1)
        cost = qty_input * cp
        st.caption(f"예상 거래금액: {format_korean_money(cost)}")

        bulk_rem  = cooldown_remaining("bulk_trade", BULK_COOLDOWN)
        trade_rem = cooldown_remaining(f"trade_{sid}", TRADE_COOLDOWN)
        bulk_left = DAILY_BULK_LIMIT - st.session_state.get("bulk_trade_count", 0)

        if bulk_rem > 0: st.markdown(f"<span class='cooldown-badge'>풀매수/풀매도 쿨다운 {bulk_rem:.1f}초</span>", unsafe_allow_html=True)
        if trade_rem > 0: st.markdown(f"<span class='cooldown-badge'>일반 거래 쿨다운 {trade_rem:.1f}초</span>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:#888;font-size:0.78rem;margin-bottom:8px;'>풀매수/풀매도 오늘 남은 횟수: <b style='color:#FFD600;'>{bulk_left}회</b></div>", unsafe_allow_html=True)

        def _safe_buy(qty, price, sid_):
            total = qty * price
            if st.session_state.global_cash < total: st.error("잔액 부족!"); return False
            u_db_check = load_db(USERS_FILE, {})
            if u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0) < total: st.error("잔액 부족! (DB 검증 실패)"); return False
            st.session_state.global_cash -= total
            old = st.session_state.portfolio.get(sid_, {'qty': 0, 'avg_price': 0})
            new_q = old['qty'] + qty
            new_a = ((old['qty'] * old['avg_price']) + total) / new_q
            st.session_state.portfolio[sid_] = {'qty': new_q, 'avg_price': new_a}
            log_tx(st.session_state.logged_in_user, "주식매수", f"{market['stock_data'][sid_]['name']} {qty}주 매수", -total)
            return True

        def _safe_sell(qty, price, sid_):
            own = st.session_state.portfolio.get(sid_, {'qty': 0})['qty']
            if own < qty:
                st.error("보유 수량 부족!")
                return False
            # DB에서 실제 보유 수량 재확인 (탭 2개 열어 동시 매도 방지)
            u_db_sell = load_db(USERS_FILE, {})
            db_own = u_db_sell.get(st.session_state.logged_in_user, {}).get('portfolio', {}).get(sid_, {}).get('qty', 0)
            if db_own < qty:
                st.error("보유 수량 부족! (DB 검증 실패) 잠시 후 다시 시도해주세요.")
                return False
            earn = qty * price
            st.session_state.global_cash += earn
            st.session_state.portfolio[sid_]['qty'] -= qty
            log_tx(st.session_state.logged_in_user, "주식매도", f"{market['stock_data'][sid_]['name']} {qty}주 매도", earn)
            return True

        c1, c2, c3, c4 = st.columns(4)
        bulk_ok = (bulk_rem <= 0) and (bulk_left > 0)

        with c1:
            if st.button("💥 풀매수", use_container_width=True, disabled=not bulk_ok):
                max_q = int(st.session_state.global_cash // cp) if cp > 0 else 0
                if max_q > 0:
                    set_cooldown("bulk_trade"); st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    if _safe_buy(max_q, cp, sid):
                        imp = min(((max_q * cp) / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = int(cp * (1 + imp))
                            market['news'] = f"🐋 [고래 매수] {st.session_state.logged_in_user}님이 {d['name']} 거액 매수! +{imp*100:.1f}% 영향"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else: st.error("잔액 부족!")

        with c2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True, disabled=trade_rem > 0):
                if trade_rem <= 0:
                    set_cooldown(f"trade_{sid}")
                    if _safe_buy(qty_input, cp, sid): sync_user_data(); st.success(f"✅ {qty_input}주 매수 완료!"); st.rerun()

        with c3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True, disabled=trade_rem > 0):
                if trade_rem <= 0:
                    set_cooldown(f"trade_{sid}")
                    if _safe_sell(qty_input, cp, sid): sync_user_data(); st.success(f"✅ {qty_input}주 매도!"); st.rerun()

        with c4:
            if st.button("💸 풀매도", use_container_width=True, disabled=not bulk_ok):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0:
                    set_cooldown("bulk_trade"); st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    if _safe_sell(own, cp, sid):
                        imp = min(((own * cp) / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                            market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {d['name']} 물량 투하! -{imp*100:.1f}% 영향"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else: st.error("보유 주식 없음")

        if bulk_left <= 0: st.warning("⚠️ 오늘 풀매수/풀매도 횟수를 모두 사용했습니다. 내일 자정에 초기화됩니다.")
