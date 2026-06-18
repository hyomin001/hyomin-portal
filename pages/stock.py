# pages/stock.py  — 토스증권 스타일 통합 거래소 (풀 리빌드)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from utils.config import stock_config, KST, USERS_FILE
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import load_db, log_tx, save_market
from streamlit_autorefresh import st_autorefresh

# ────────────────────────────────────────────────────────────────────────────
# CSS — 토스증권 느낌 다크 테마
# ────────────────────────────────────────────────────────────────────────────
STOCK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Noto+Sans+KR:wght@400;500;700&display=swap');

/* ── 공통 리셋 ── */
.stock-wrap * { box-sizing: border-box; font-family: 'Noto Sans KR', sans-serif; }

/* ── 티커 배너 ── */
.ticker-wrap {
    overflow: hidden; white-space: nowrap;
    background: #0D0D14; border: 1px solid #1E1E2E;
    border-radius: 10px; padding: 10px 0; margin-bottom: 18px;
}
.ticker-inner {
    display: inline-block;
    animation: ticker-scroll 30s linear infinite;
}
.ticker-inner:hover { animation-play-state: paused; }
@keyframes ticker-scroll { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
.ticker-item {
    display: inline-flex; align-items: center; gap: 8px;
    margin-right: 40px; font-size: 0.82rem; color: #94A3B8;
    cursor: default;
}
.ticker-name { color: #CBD5E1; font-weight: 500; }
.ticker-price { color: #E2E8F0; font-weight: 700; font-family: 'Orbitron', monospace; font-size: 0.75rem; }
.t-up   { color: #FF5252 !important; }
.t-down { color: #4FC3F7 !important; }
.t-flat { color: #78909C !important; }

/* ── 시황 카드 그리드 ── */
.mkt-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(195px, 1fr));
    gap: 12px; margin-bottom: 8px;
}
.mkt-card {
    background: #10101C;
    border: 1px solid #1E2035;
    border-radius: 14px;
    padding: 16px 18px;
    cursor: pointer;
    transition: border-color .18s, transform .12s;
    position: relative; overflow: hidden;
}
.mkt-card:hover { border-color: #3D4270; transform: translateY(-2px); }
.mkt-card.selected { border-color: #5C6BC0; background: #13132A; }
.mkt-card .c-icon  { font-size: 1.5rem; margin-bottom: 6px; display: block; }
.mkt-card .c-name  { font-size: 0.78rem; color: #64748B; font-weight: 500; margin-bottom: 4px; }
.mkt-card .c-price { font-size: 1.05rem; font-weight: 700; color: #E2E8F0;
                      font-family: 'Orbitron', monospace; letter-spacing: -0.5px; }
.mkt-card .c-chg   { font-size: 0.8rem; font-weight: 700; margin-top: 4px; }
.mkt-card .bar-bg  { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: #1E2035; }
.mkt-card .bar-fill { height: 3px; border-radius: 0 0 14px 14px; transition: width .4s; }

/* ── 종목 상세 헤더 ── */
.det-header {
    background: linear-gradient(135deg, #0D0D18 0%, #111126 100%);
    border: 1px solid #1E2035; border-radius: 16px;
    padding: 22px 26px; margin-bottom: 16px;
    display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;
}
.det-left .d-icon-name { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.det-left .d-icon { font-size: 2rem; }
.det-left .d-name { font-size: 1.1rem; font-weight: 700; color: #E2E8F0; }
.det-left .d-id   { font-size: 0.75rem; color: #475569; font-weight: 500; letter-spacing: 1px; }
.det-right { text-align: right; }
.det-right .d-price {
    font-size: 2rem; font-weight: 700; color: #E2E8F0;
    font-family: 'Orbitron', monospace; letter-spacing: -1px;
}
.det-right .d-chg  { font-size: 0.95rem; font-weight: 700; margin-top: 4px; }
.det-right .d-prev { font-size: 0.75rem; color: #475569; margin-top: 2px; }
.up   { color: #FF5252; }
.down { color: #4FC3F7; }
.flat { color: #78909C; }

/* ── 보유 포지션 배지 ── */
.pos-bar {
    background: #0F1120; border: 1px solid #1E2035;
    border-radius: 12px; padding: 14px 20px;
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 14px; flex-wrap: wrap; gap: 10px;
}
.pos-item { text-align: center; }
.pos-label { font-size: 0.72rem; color: #475569; margin-bottom: 3px; }
.pos-value { font-size: 0.95rem; font-weight: 700; color: #E2E8F0; }

/* ── 수량 입력 + 금액 표시 ── */
.order-box {
    background: #0D0D18; border: 1px solid #1E2035;
    border-radius: 14px; padding: 18px 20px; margin-bottom: 14px;
}
.order-box .ob-row {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 8px;
}
.order-box .ob-label { font-size: 0.78rem; color: #475569; }
.order-box .ob-val   { font-size: 0.88rem; font-weight: 700; color: #CBD5E1; }
.order-box .ob-total { font-size: 1rem; font-weight: 700; color: #FFD600; }

/* ── 거래 버튼 ── */
.btn-buy  { background: #B71C1C !important; color: #fff !important;
            border: none !important; border-radius: 10px !important;
            font-weight: 700 !important; font-size: 0.88rem !important; }
.btn-sell { background: #0D47A1 !important; color: #fff !important;
            border: none !important; border-radius: 10px !important;
            font-weight: 700 !important; font-size: 0.88rem !important; }
.btn-bulk { background: #37474F !important; color: #CFD8DC !important;
            border: 1px solid #546E7A !important; border-radius: 10px !important;
            font-weight: 700 !important; font-size: 0.82rem !important; }

/* ── 뉴스 배너 ── */
.news-bar {
    background: #0A0A14; border-left: 3px solid #5C6BC0;
    border-radius: 0 10px 10px 0; padding: 9px 16px;
    font-size: 0.82rem; color: #94A3B8; margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}
.news-bar .nb-badge {
    background: #1E2440; color: #7986CB;
    font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 6px;
    white-space: nowrap; letter-spacing: 0.5px;
}

/* ── 포트폴리오 테이블 ── */
.port-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.port-table th {
    text-align: right; color: #475569; font-weight: 500;
    padding: 7px 10px; border-bottom: 1px solid #1E2035; font-size: 0.75rem;
}
.port-table th:first-child { text-align: left; }
.port-table td {
    text-align: right; color: #CBD5E1; padding: 10px 10px;
    border-bottom: 1px solid #0F1120;
}
.port-table td:first-child { text-align: left; color: #E2E8F0; font-weight: 600; }
.port-table tr:last-child td { border-bottom: none; }
.port-table tr:hover td { background: #0F1120; }
.pnl-pos { color: #FF5252; font-weight: 700; }
.pnl-neg { color: #4FC3F7; font-weight: 700; }

/* ── 요약 메트릭 ── */
.sum-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 14px; }
.sum-card {
    background: #0F1120; border: 1px solid #1E2035; border-radius: 12px; padding: 14px 16px;
}
.sum-card .s-label { font-size: 0.72rem; color: #475569; margin-bottom: 5px; }
.sum-card .s-val   { font-size: 1rem; font-weight: 700; color: #E2E8F0; }

/* ── 쿨다운 배지 ── */
.cd-badge {
    display: inline-block; background: #1A1A2E;
    border: 1px solid #2D2D4E; border-radius: 8px;
    padding: 4px 10px; font-size: 0.72rem; color: #7E86A0; margin: 4px 0;
}

/* ── 빈 포트폴리오 ── */
.empty-port {
    text-align: center; padding: 40px 20px; color: #374151;
    font-size: 0.9rem; border: 1px dashed #1E2035; border-radius: 14px;
}
.empty-port .ep-icon { font-size: 2.5rem; margin-bottom: 10px; display: block; }

/* ── 탭 스타일 오버라이드 ── */
button[data-baseweb="tab"] { font-size: 0.85rem !important; font-weight: 600 !important; }
</style>
"""

# ────────────────────────────────────────────────────────────────────────────
# 헬퍼
# ────────────────────────────────────────────────────────────────────────────

def _price_diff(d):
    if len(d['history']) > 1:
        return d['price'] - d['history'][-2], (d['price'] - d['history'][-2]) / d['history'][-2] * 100
    return 0, 0.0

def _cls(diff):
    if diff > 0: return "up", "▲"
    if diff < 0: return "down", "▼"
    return "flat", "━"

def _spark_color(diff):
    return "#FF5252" if diff >= 0 else "#4FC3F7"

# ────────────────────────────────────────────────────────────────────────────
# 메인 렌더
# ────────────────────────────────────────────────────────────────────────────

def render(market, nw):
    st_autorefresh(interval=10_000, limit=None, key="stock_auto_refresh")
    st.markdown(STOCK_CSS, unsafe_allow_html=True)

    TRADE_COOLDOWN   = 3.0
    BULK_COOLDOWN    = 8.0
    DAILY_BULK_LIMIT = 5

    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    if st.session_state.get("bulk_trade_date") != today_str:
        st.session_state.bulk_trade_date  = today_str
        st.session_state.bulk_trade_count = 0

    # ── 뉴스 배너 ──
    news_txt = market.get("news", "")
    if news_txt:
        st.markdown(
            f"<div class='news-bar'><span class='nb-badge'>LIVE</span>{news_txt}</div>",
            unsafe_allow_html=True
        )

    # ── 티커 배너 (전 종목 흐르는 띠) ──
    items_html = ""
    for s in stock_config:
        d = market['stock_data'].get(s['id'], {})
        if not d: continue
        diff, pct = _price_diff(d)
        cls, arr  = _cls(diff)
        items_html += (
            f"<span class='ticker-item'>"
            f"<span>{s['icon']}</span>"
            f"<span class='ticker-name'>{d['name']}</span>"
            f"<span class='ticker-price'>₩{d['price']:,}</span>"
            f"<span class='{cls}'>{arr} {abs(pct):.2f}%</span>"
            f"</span>"
        )
    doubled = items_html * 2   # 끊김 없이 무한 스크롤
    st.markdown(
        f"<div class='ticker-wrap'><div class='ticker-inner'>{doubled}</div></div>",
        unsafe_allow_html=True
    )

    # ── 탭 ──
    tab_market, tab_trade, tab_port = st.tabs(["📊 시황", "⚡ 거래", "💼 포트폴리오"])

    # ════════════════════════════════════════════════════════════
    # TAB 1 — 시황 (카드 그리드)
    # ════════════════════════════════════════════════════════════
    with tab_market:
        cards_html = "<div class='mkt-grid'>"
        for s in stock_config:
            d = market['stock_data'].get(s['id'], {})
            if not d: continue
            diff, pct = _price_diff(d)
            cls, arr  = _cls(diff)
            bar_clr   = "#FF5252" if diff >= 0 else "#4FC3F7"
            # 미니 바 (변동률 0~10% → 0~100%)
            bar_w = min(abs(pct) / 10 * 100, 100)
            cards_html += f"""
            <div class='mkt-card'>
                <span class='c-icon'>{s['icon']}</span>
                <div class='c-name'>{d['name']} <span style='color:#2D3A4A;font-size:0.68rem;'>{s['id']}</span></div>
                <div class='c-price'>₩{d['price']:,}</div>
                <div class='c-chg {cls}'>{arr} {abs(pct):.2f}%
                    <span style='color:#374151;font-weight:400;font-size:0.72rem;margin-left:6px;'>
                        전일 ₩{d['history'][-2]:,}
                    </span>
                </div>
                <div class='bar-bg'><div class='bar-fill' style='width:{bar_w:.0f}%;background:{bar_clr};'></div></div>
            </div>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)

        # 최근 60틱 전체 차트 (멀티라인)
        st.markdown("<div style='margin-top:20px;margin-bottom:6px;color:#475569;font-size:0.78rem;font-weight:600;letter-spacing:1px;'>전 종목 60틱 가격 추이</div>", unsafe_allow_html=True)
        fig = go.Figure()
        palette = ["#FF5252","#4FC3F7","#69F0AE","#FFD740","#EA80FC",
                   "#FF6D00","#40C4FF","#F48FB1","#B9F6CA","#FF9800"]
        for i, s in enumerate(stock_config):
            d = market['stock_data'].get(s['id'], {})
            if not d or not d.get('history'): continue
            hist = d['history']
            norm = [v / hist[0] * 100 for v in hist] if hist[0] else hist
            fig.add_trace(go.Scatter(
                y=norm, mode='lines', name=d['name'],
                line=dict(color=palette[i % len(palette)], width=1.5),
                hovertemplate=f"{d['name']}<br>%{{y:.1f}} (기준 100)<extra></extra>"
            ))
        fig.update_layout(
            height=260, template='plotly_dark',
            margin=dict(l=0,r=0,t=10,b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", y=-0.25, font=dict(size=10)),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                       ticksuffix='', title='(시작=100)',
                       titlefont=dict(size=9), tickfont=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    # TAB 2 — 거래
    # ════════════════════════════════════════════════════════════
    with tab_trade:
        # 종목 선택
        options    = [f"{s['icon']} {s['name']}" for s in stock_config]
        sel_n      = st.selectbox("종목", options, label_visibility="collapsed")
        sid        = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        d          = market['stock_data'][sid]
        cp         = d['price']
        diff, pct  = _price_diff(d)
        cls, arr   = _cls(diff)
        spark_clr  = _spark_color(diff)

        # ── 종목 헤더 ──
        prev_price = d['history'][-2] if len(d['history']) > 1 else cp
        high_52 = max(d['history']); low_52 = min(d['history'])
        st.markdown(f"""
        <div class='det-header'>
            <div class='det-left'>
                <div class='d-icon-name'>
                    <span class='d-icon'>{d.get('icon', s['icon'])}</span>
                    <div>
                        <div class='d-name'>{d['name']}</div>
                        <div class='d-id'>{sid}</div>
                    </div>
                </div>
                <div style='display:flex;gap:20px;margin-top:8px;'>
                    <div><div style='font-size:0.68rem;color:#374151;'>고가</div><div style='font-size:0.82rem;color:#FF5252;font-weight:700;'>₩{high_52:,}</div></div>
                    <div><div style='font-size:0.68rem;color:#374151;'>저가</div><div style='font-size:0.82rem;color:#4FC3F7;font-weight:700;'>₩{low_52:,}</div></div>
                    <div><div style='font-size:0.68rem;color:#374151;'>전일</div><div style='font-size:0.82rem;color:#94A3B8;font-weight:600;'>₩{prev_price:,}</div></div>
                </div>
            </div>
            <div class='det-right'>
                <div class='d-price'>₩{cp:,}</div>
                <div class='d-chg {cls}'>{arr} {abs(pct):.2f}% ({'+' if diff>=0 else ''}{diff:,}원)</div>
                <div class='d-prev'>잔고 {format_korean_money(st.session_state.global_cash)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 캔들 / 라인 차트 ──
        if len(d['history']) > 1:
            hist = d['history']
            fig2 = go.Figure()
            # 면적 채우기
            fig2.add_trace(go.Scatter(
                y=hist, mode='lines',
                line=dict(color=spark_clr, width=2),
                fill='tozeroy',
                fillcolor=f"rgba({'255,82,82' if diff>=0 else '79,195,247'},0.06)",
                hovertemplate='₩%{y:,.0f}<extra></extra>'
            ))
            # 현재가 수평선
            fig2.add_hline(y=cp, line_width=1, line_dash="dot",
                           line_color="rgba(255,255,255,0.15)")
            fig2.update_layout(
                height=180, template='plotly_dark',
                margin=dict(l=0,r=0,t=4,b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                           tickformat=',.0f', tickfont=dict(size=9)),
                showlegend=False,
            )
            st.plotly_chart(fig2, use_container_width=True)

        # ── 보유 포지션 바 ──
        my_info = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
        my_qty  = my_info.get('qty', 0)
        my_avg  = my_info.get('avg_price', 0)

        if my_qty > 0:
            my_eval = my_qty * cp
            my_pnl  = my_eval - my_qty * my_avg
            my_roi  = (cp - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_cls, roi_arr = _cls(my_roi)
            st.markdown(f"""
            <div class='pos-bar'>
                <div class='pos-item'>
                    <div class='pos-label'>보유 수량</div>
                    <div class='pos-value'>{my_qty:,}주</div>
                </div>
                <div class='pos-item'>
                    <div class='pos-label'>평균 단가</div>
                    <div class='pos-value'>₩{int(my_avg):,}</div>
                </div>
                <div class='pos-item'>
                    <div class='pos-label'>평가액</div>
                    <div class='pos-value' style='color:#FFD600;'>₩{int(my_eval):,}</div>
                </div>
                <div class='pos-item'>
                    <div class='pos-label'>평가손익</div>
                    <div class='pos-value {"pnl-pos" if my_pnl>=0 else "pnl-neg"}'>
                        {'+' if my_pnl>=0 else ''}{format_korean_money(int(my_pnl))}
                    </div>
                </div>
                <div class='pos-item'>
                    <div class='pos-label'>수익률</div>
                    <div class='pos-value {roi_cls}'>{roi_arr} {abs(my_roi):.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background:#0A0A12;border:1px dashed #1E2035;border-radius:12px;"
                "padding:12px 18px;color:#374151;font-size:0.82rem;margin-bottom:14px;'>"
                "보유 포지션 없음</div>",
                unsafe_allow_html=True
            )

        # ── 주문 입력 ──
        max_buyable = int(st.session_state.global_cash // cp) if cp > 0 else 0

        col_qty, col_pct = st.columns([2, 1])
        with col_qty:
            qty_input = st.number_input(
                "수량 (주)", min_value=1, max_value=max(1, max_buyable if max_buyable else 999_999),
                step=1, value=1, key="stock_qty"
            )
        with col_pct:
            pct_sel = st.selectbox("비율", ["직접입력","10%","25%","50%","100%"], key="stock_pct")
            if pct_sel != "직접입력":
                ratio = int(pct_sel.replace("%","")) / 100
                qty_input = max(1, int(max_buyable * ratio))

        cost = qty_input * cp
        avail_sell_qty = my_qty
        sell_cost = qty_input * cp

        order_html = f"""
        <div class='order-box'>
            <div class='ob-row'>
                <span class='ob-label'>거래 단가</span>
                <span class='ob-val'>₩{cp:,}</span>
            </div>
            <div class='ob-row'>
                <span class='ob-label'>수량</span>
                <span class='ob-val'>{qty_input:,}주</span>
            </div>
            <div class='ob-row' style='border-top:1px solid #1E2035;padding-top:10px;margin-top:4px;'>
                <span class='ob-label'>예상 거래금액</span>
                <span class='ob-total'>{format_korean_money(cost)}</span>
            </div>
            <div class='ob-row'>
                <span class='ob-label'>최대 매수 가능</span>
                <span class='ob-val' style='color:#64748B;'>{max_buyable:,}주</span>
            </div>
        </div>
        """
        st.markdown(order_html, unsafe_allow_html=True)

        # ── 쿨다운 표시 ──
        bulk_rem  = cooldown_remaining("bulk_trade", BULK_COOLDOWN)
        trade_rem = cooldown_remaining(f"trade_{sid}", TRADE_COOLDOWN)
        bulk_left = DAILY_BULK_LIMIT - st.session_state.get("bulk_trade_count", 0)

        cd_parts = []
        if trade_rem > 0: cd_parts.append(f"일반 거래 {trade_rem:.1f}초")
        if bulk_rem  > 0: cd_parts.append(f"풀매수/도 {bulk_rem:.1f}초")
        if cd_parts:
            st.markdown(f"<span class='cd-badge'>⏱ 쿨다운: {' · '.join(cd_parts)}</span>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.72rem;color:#374151;margin-bottom:10px;'>"
            f"풀매수/매도 오늘 잔여 <b style='color:#FFD600;'>{max(0,bulk_left)}회</b></div>",
            unsafe_allow_html=True
        )

        # ── 매수/매도 함수 ──
        def _safe_buy(qty, price, sid_):
            total = qty * price
            if st.session_state.global_cash < total:
                st.error("잔액 부족!"); return False
            u_db = load_db(USERS_FILE, {})
            if u_db.get(st.session_state.logged_in_user, {}).get('cash', 0) < total:
                st.error("잔액 부족! (DB 검증 실패)"); return False
            st.session_state.global_cash -= total
            old   = st.session_state.portfolio.get(sid_, {'qty': 0, 'avg_price': 0})
            new_q = old['qty'] + qty
            new_a = ((old['qty'] * old['avg_price']) + total) / new_q
            st.session_state.portfolio[sid_] = {'qty': new_q, 'avg_price': new_a}
            log_tx(st.session_state.logged_in_user, "주식매수",
                   f"{market['stock_data'][sid_]['name']} {qty}주 매수", -total)
            return True

        def _safe_sell(qty, price, sid_):
            own = st.session_state.portfolio.get(sid_, {'qty': 0})['qty']
            if own < qty: st.error("보유 수량 부족!"); return False
            u_db = load_db(USERS_FILE, {})
            db_own = u_db.get(st.session_state.logged_in_user, {}).get(
                'portfolio', {}).get(sid_, {}).get('qty', 0)
            if db_own < qty: st.error("보유 수량 부족! (DB 검증)"); return False
            earn = qty * price
            st.session_state.global_cash += earn
            st.session_state.portfolio[sid_]['qty'] -= qty
            log_tx(st.session_state.logged_in_user, "주식매도",
                   f"{market['stock_data'][sid_]['name']} {qty}주 매도", earn)
            return True

        # ── 거래 버튼 ──
        bulk_ok = (bulk_rem <= 0) and (bulk_left > 0)

        bc1, bc2, bc3, bc4 = st.columns(4)

        with bc1:
            if st.button("💥 풀매수", use_container_width=True, disabled=not bulk_ok, key="btn_bulk_buy"):
                mq = max_buyable
                if mq > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    if _safe_buy(mq, cp, sid):
                        imp = min(((mq * cp) / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = int(cp * (1 + imp))
                            market['news'] = f"🐋 [고래 매수] {st.session_state.logged_in_user}님 {d['name']} 거액 매수! +{imp*100:.1f}%"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("잔액 부족!")

        with bc2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True,
                         disabled=trade_rem > 0, key="btn_buy"):
                set_cooldown(f"trade_{sid}")
                if _safe_buy(qty_input, cp, sid):
                    sync_user_data()
                    st.success(f"✅ {qty_input}주 매수 완료!")
                    st.rerun()

        with bc3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True,
                         disabled=trade_rem > 0, key="btn_sell"):
                set_cooldown(f"trade_{sid}")
                if _safe_sell(qty_input, cp, sid):
                    sync_user_data()
                    st.success(f"✅ {qty_input}주 매도!")
                    st.rerun()

        with bc4:
            if st.button("💸 풀매도", use_container_width=True,
                         disabled=not bulk_ok, key="btn_bulk_sell"):
                own = st.session_state.portfolio.get(sid, {'qty': 0})['qty']
                if own > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count", 0) + 1
                    if _safe_sell(own, cp, sid):
                        imp = min(((own * cp) / 500_000_000_000) * 0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = max(1_000, int(cp * (1 - imp)))
                            market['news'] = f"📉 [고래 매도] {st.session_state.logged_in_user}님 {d['name']} 물량 투하! -{imp*100:.1f}%"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("보유 주식 없음")

        if bulk_left <= 0:
            st.warning("⚠️ 오늘 풀매수/풀매도 횟수를 모두 사용했습니다. 자정에 초기화됩니다.")

    # ════════════════════════════════════════════════════════════
    # TAB 3 — 포트폴리오
    # ════════════════════════════════════════════════════════════
    with tab_port:
        p_rows = []; total_eval = 0; total_invested = 0; total_pnl = 0

        for sid_p, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty <= 0 or sid_p not in market['stock_data']:
                continue
            cp_p  = market['stock_data'][sid_p]['price']
            ap    = info.get('avg_price', 0)
            inv   = qty * ap; total_invested += inv
            ev    = qty * cp_p; total_eval += ev
            pnl   = ev - inv; total_pnl += pnl
            roi   = (cp_p - ap) / ap * 100 if ap > 0 else 0
            # 종목명 + 아이콘
            icon = next((s['icon'] for s in stock_config if s['id'] == sid_p), '📊')
            nm   = market['stock_data'][sid_p]['name']
            diff_p, pct_p = _price_diff(market['stock_data'][sid_p])
            cls_p, arr_p  = _cls(diff_p)
            p_rows.append({
                "_nm": f"{icon} {nm}", "_qty": qty, "_ap": ap,
                "_cp": cp_p, "_ev": ev, "_pnl": pnl, "_roi": roi,
                "_cls": cls_p, "_arr": arr_p, "_pct": pct_p,
            })

        if p_rows:
            # 테이블 HTML
            rows_html = ""
            for r in sorted(p_rows, key=lambda x: -x['_ev']):
                roi_cls = "pnl-pos" if r['_roi'] >= 0 else "pnl-neg"
                pnl_cls = "pnl-pos" if r['_pnl'] >= 0 else "pnl-neg"
                rows_html += f"""
                <tr>
                    <td>{r['_nm']}</td>
                    <td>{r['_qty']:,}주</td>
                    <td>₩{int(r['_ap']):,}</td>
                    <td>₩{int(r['_cp']):,}
                        <span class='{r['_cls']}' style='font-size:0.7rem;'>{r['_arr']}{abs(r['_pct']):.1f}%</span>
                    </td>
                    <td>₩{int(r['_ev']):,}</td>
                    <td class='{pnl_cls}'>{'+' if r['_pnl']>=0 else ''}{format_korean_money(int(r['_pnl']))}</td>
                    <td class='{roi_cls}'>{'+' if r['_roi']>=0 else ''}{r['_roi']:.2f}%</td>
                </tr>"""

            st.markdown(f"""
            <table class='port-table'>
              <thead><tr>
                <th>종목</th><th style='text-align:right'>수량</th>
                <th style='text-align:right'>평균단가</th><th style='text-align:right'>현재가</th>
                <th style='text-align:right'>평가액</th><th style='text-align:right'>평가손익</th>
                <th style='text-align:right'>수익률</th>
              </tr></thead>
              <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

            # 요약 카드
            total_roi = (total_eval - total_invested) / total_invested * 100 if total_invested else 0
            roi_cls_t = "pnl-pos" if total_pnl >= 0 else "pnl-neg"
            st.markdown(f"""
            <div class='sum-grid' style='margin-top:16px;'>
                <div class='sum-card'>
                    <div class='s-label'>총 매수금액</div>
                    <div class='s-val'>{format_korean_money(int(total_invested))}</div>
                </div>
                <div class='sum-card'>
                    <div class='s-label'>총 평가액</div>
                    <div class='s-val' style='color:#FFD600;'>{format_korean_money(int(total_eval))}</div>
                </div>
                <div class='sum-card'>
                    <div class='s-label'>총 평가손익 / 수익률</div>
                    <div class='s-val {roi_cls_t}'>
                        {'+' if total_pnl>=0 else ''}{format_korean_money(int(total_pnl))}
                        <span style='font-size:0.82rem;'>({'+' if total_roi>=0 else ''}{total_roi:.2f}%)</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 종목별 비중 파이차트
            st.markdown("<div style='margin-top:20px;margin-bottom:6px;color:#475569;font-size:0.78rem;font-weight:600;letter-spacing:1px;'>보유 종목 비중</div>", unsafe_allow_html=True)
            labels = [f"{r['_nm']}" for r in p_rows]
            values = [r['_ev'] for r in p_rows]
            pie = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.55,
                textinfo='label+percent', textfont=dict(size=11),
                marker=dict(colors=["#FF5252","#4FC3F7","#69F0AE","#FFD740","#EA80FC",
                                     "#FF6D00","#40C4FF","#F48FB1","#B9F6CA","#FF9800"],
                             line=dict(color='#0D0D18', width=2)),
                hovertemplate='%{label}<br>₩%{value:,.0f}<br>%{percent}<extra></extra>'
            ))
            pie.update_layout(
                height=280, template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0,r=0,t=10,b=10),
                legend=dict(orientation="h", font=dict(size=10), y=-0.1),
                showlegend=True,
            )
            # 가운데 총 평가액 주석
            pie.add_annotation(
                text=f"<b style='font-size:13px;'>{format_korean_money(int(total_eval))}</b>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=13, color="#E2E8F0"),
            )
            st.plotly_chart(pie, use_container_width=True)

        else:
            st.markdown("""
            <div class='empty-port'>
                <span class='ep-icon'>📭</span>
                보유 중인 주식이 없습니다.<br>
                <span style='font-size:0.78rem;color:#1E2035;'>거래 탭에서 종목을 선택하고 매수해보세요.</span>
            </div>
            """, unsafe_allow_html=True)
