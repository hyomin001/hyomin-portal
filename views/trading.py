import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from config import stock_config
from database import log_tx, sync_user_data, save_market


def render(market):
    st.title("📈 통합 거래소")

    tab_market, tab_port, tab_trade = st.tabs(["📊 전체 시황", "💼 내 포트폴리오", "⚡ 빠른 거래"])

    with tab_market:
        rows = ""
        for s in stock_config:
            d    = market['stock_data'][s['id']]
            diff = d['price'] - d['history'][-2] if len(d['history']) > 1 else 0
            pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
            cls  = "p-up" if diff > 0 else "p-down" if diff < 0 else "p-flat"
            arr  = "▲"   if diff > 0 else "▼"       if diff < 0 else "━"
            rows += f"<tr><td>{s['icon']} {d['name']}</td><td style='text-align:right;font-weight:900;color:#fff;'>₩{d['price']:,}</td><td class='{cls}' style='text-align:right;'>{arr} {abs(pct):.2f}%</td><td style='text-align:right;color:#888;'>₩{d['history'][-2]:,}</td></tr>"
        st.markdown(f"<table class='stock-table'><thead><tr><th>종목</th><th style='text-align:right;'>현재가</th><th style='text-align:right;'>변동률</th><th style='text-align:right;'>전일가</th></tr></thead><tbody>{rows}</tbody></table>", unsafe_allow_html=True)

    with tab_port:
        p_rows = []; total_eval = 0
        for sid, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty > 0 and sid in market['stock_data']:
                cp  = market['stock_data'][sid]['price']
                ap  = info.get('avg_price', 0)
                ev  = qty * cp; total_eval += ev
                roi = (cp - ap) / ap * 100 if ap > 0 else 0
                p_rows.append({"종목": market['stock_data'][sid]['name'], "수량": f"{qty}주",
                                "평균단가": f"₩{int(ap):,}", "평가액": f"₩{int(ev):,}",
                                "수익률": f"{roi:+.2f}%"})
        if p_rows:
            st.table(pd.DataFrame(p_rows))
            st.metric("📊 주식 총 평가액", f"₩{total_eval:,.0f}")
        else:
            st.info("보유 중인 주식이 없습니다.")

    with tab_trade:
        sel_n = st.selectbox("거래 종목 선택", [f"{s['icon']} {s['name']}" for s in stock_config])
        sid   = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        d     = market['stock_data'][sid]
        cp    = d['price']

        if len(d['history']) > 1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=d['history'], mode='lines',
                                     line=dict(color='#00E5FF', width=2),
                                     fill='tozeroy', fillcolor='rgba(0,229,255,0.05)'))
            fig.update_layout(height=220, template='plotly_dark', margin=dict(l=0,r=0,t=0,b=0),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              xaxis=dict(showgrid=False, showticklabels=False),
                              yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
            st.plotly_chart(fig, use_container_width=True)

        diff = cp - d['history'][-2] if len(d['history']) > 1 else 0
        pct  = diff / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        clr  = "#FF4B4B" if diff >= 0 else "#4B9EFF"
        arr  = "▲" if diff >= 0 else "▼"
        st.markdown(f"<div style='text-align:center;margin:10px 0;'><span style='font-size:1.8rem;font-weight:900;color:#fff;font-family:Orbitron;'>₩{cp:,}</span> <span style='color:{clr};font-weight:900;'>{arr} {abs(pct):.2f}%</span></div>", unsafe_allow_html=True)

        qty_input = st.number_input("거래 수량 (주)", min_value=1, step=1, value=1)
        cost = qty_input * cp
        st.caption(f"예상 거래금액: ₩{cost:,}")

        c1, c2, c3, c4 = st.columns(4)

        def _safe_buy(qty, price, sid_):
            total = qty * price
            if st.session_state.global_cash < total:
                st.error("잔액 부족!"); return False
            st.session_state.global_cash -= total
            if st.session_state.global_cash < 0:
                st.session_state.global_cash += total
                st.error("거래 취소 (잔액 보호)"); return False
            old = st.session_state.portfolio.get(sid_, {'qty': 0, 'avg_price': 0})
            new_q = old['qty'] + qty
            new_a = ((old['qty'] * old['avg_price']) + total) / new_q
            st.session_state.portfolio[sid_] = {'qty': new_q, 'avg_price': new_a}
            log_tx(st.session_state.logged_in_user, "주식매수", f"{market['stock_data'][sid_]['name']} {qty}주 매수", -total)
            return True

        def _safe_sell(qty, price, sid_):
            own = st.session_state.portfolio.get(sid_, {'qty': 0})['qty']
            if own < qty:
                st.error(f"보유 수량 부족! (현재 {own}주)"); return False
            earn = qty * price
            st.session_state.global_cash += earn
            st.session_state.portfolio[sid_]['qty'] -= qty
            log_tx(st.session_state.logged_in_user, "주식매도", f"{market['stock_data'][sid_]['name']} {qty}주 매도", earn)
            return True

        with c1:
            if st.button("💥 풀매수", use_container_width=True):
                max_q = st.session_state.global_cash // cp
                if max_q > 0 and _safe_buy(max_q, cp, sid):
                    buy_a = max_q * cp
                    if buy_a >= 1_000_000_000:
                        imp = min((buy_a / 1_000_000_000_000) * 0.1, 0.5)
                        market['stock_data'][sid]['price'] = int(cp * (1 + imp))
                        market['news'] = f"🐋 [고래 매수] {st.session_state.logged_in_user}님이 {d['name']} 거액 매수!"
                        save_market(market)
                    sync_user_data(); st.rerun()
                else:
                    if max_q == 0: st.error("잔액 부족!")
        with c2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True):
                if _safe_buy(qty_input, cp, sid):
                    sync_user_data(); st.success(f"✅ {qty_input}주 매수 완료!"); time.sleep(1); st.rerun()
        with c3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True):
                if _safe_sell(qty_input, cp, sid):
                    sync_user_data(); st.success(f"✅ {qty_input}주 매도!"); time.sleep(1); st.rerun()
        with c4:
            if st.button("💸 풀매도", use_container_width=True):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0 and _safe_sell(own, cp, sid):
                    sell_a = own * cp
                    if sell_a >= 1_000_000_000:
                        imp = min((sell_a / 500_000_000_000) * 0.1, 0.5)
                        market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                        market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님이 {d['name']} 물량 투하!"
                        save_market(market)
                    sync_user_data(); st.rerun()
                else:
                    if own == 0: st.error("보유 주식 없음")

    time.sleep(3); st.rerun()
