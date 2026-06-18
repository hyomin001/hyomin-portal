# pages/stock.py  — 토스증권 스타일 v2 (호가창 + 클릭 차트)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime
from utils.config import stock_config, KST, USERS_FILE
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import load_db, log_tx, save_market
from streamlit_autorefresh import st_autorefresh

# ────────────────────────────────────────────────────────────────────────────
# CSS
# ────────────────────────────────────────────────────────────────────────────
STOCK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Noto+Sans+KR:wght@400;500;700&display=swap');

.stock-wrap * { box-sizing: border-box; font-family: 'Noto Sans KR', sans-serif; }

/* ── 티커 ── */
.ticker-wrap {
    overflow: hidden; white-space: nowrap;
    background: #0D0D14; border: 1px solid #1E1E2E;
    border-radius: 10px; padding: 10px 0; margin-bottom: 18px;
}
.ticker-inner { display: inline-block; animation: ticker-scroll 30s linear infinite; }
.ticker-inner:hover { animation-play-state: paused; }
@keyframes ticker-scroll { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
.ticker-item {
    display: inline-flex; align-items: center; gap: 8px;
    margin-right: 40px; font-size: 0.82rem; color: #94A3B8; cursor: default;
}
.ticker-name  { color: #CBD5E1; font-weight: 500; }
.ticker-price { color: #E2E8F0; font-weight: 700; font-family: 'Orbitron', monospace; font-size: 0.75rem; }

/* ── 시황 카드 ── */
.mkt-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(185px, 1fr));
    gap: 10px; margin-bottom: 8px;
}
.mkt-card {
    background: #10101C; border: 1px solid #1E2035; border-radius: 14px;
    padding: 14px 16px; cursor: pointer;
    transition: border-color .18s, transform .12s, background .15s;
    position: relative; overflow: hidden; user-select: none;
}
.mkt-card:hover  { border-color: #3D4270; transform: translateY(-2px); }
.mkt-card.sel    { border-color: #5C6BC0 !important; background: #13132A !important; }
.mkt-card .c-icon  { font-size: 1.4rem; margin-bottom: 5px; display: block; }
.mkt-card .c-name  { font-size: 0.75rem; color: #64748B; font-weight: 500; margin-bottom: 3px; }
.mkt-card .c-price { font-size: 0.98rem; font-weight: 700; color: #E2E8F0;
                      font-family: 'Orbitron', monospace; letter-spacing: -0.5px; }
.mkt-card .c-chg   { font-size: 0.78rem; font-weight: 700; margin-top: 3px; }
.mkt-card .bar-bg  { position:absolute; bottom:0; left:0; right:0; height:3px; background:#1E2035; }
.mkt-card .bar-fill{ height:3px; border-radius:0 0 14px 14px; transition:width .4s; }

/* ── 종목 상세 헤더 ── */
.det-header {
    background: linear-gradient(135deg,#0D0D18,#111126);
    border: 1px solid #1E2035; border-radius: 16px;
    padding: 20px 22px; margin-bottom: 14px;
    display: flex; justify-content: space-between; align-items: flex-start; gap: 16px;
}
.det-left .d-icon-name { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.det-left .d-icon { font-size: 1.9rem; }
.det-left .d-name { font-size: 1.05rem; font-weight:700; color:#E2E8F0; }
.det-left .d-id   { font-size: 0.72rem; color:#475569; font-weight:500; letter-spacing:1px; }
.det-right { text-align:right; }
.det-right .d-price { font-size:1.9rem; font-weight:700; color:#E2E8F0;
                       font-family:'Orbitron',monospace; letter-spacing:-1px; }
.det-right .d-chg   { font-size:0.92rem; font-weight:700; margin-top:4px; }
.det-right .d-prev  { font-size:0.72rem; color:#475569; margin-top:2px; }

/* ── 호가창 ── */
.ob-wrap {
    background: #08080F; border: 1px solid #1A1A2E; border-radius: 14px;
    overflow: hidden; margin-bottom: 14px;
}
.ob-header {
    display: grid; grid-template-columns: 1fr auto 1fr;
    padding: 8px 12px; border-bottom: 1px solid #1A1A2E;
    font-size: 0.68rem; color: #374151; font-weight: 600; letter-spacing: 0.5px;
}
.ob-row {
    display: grid; grid-template-columns: 1fr auto 1fr;
    padding: 3px 0; position: relative; align-items: center;
}
.ob-sell-qty {
    text-align: right; padding: 4px 10px; font-size: 0.75rem; color: #64748B;
    font-weight: 500; z-index: 1; position: relative;
}
.ob-price {
    text-align: center; padding: 4px 14px; font-size: 0.82rem; font-weight: 700;
    z-index: 1; position: relative; white-space: nowrap; min-width: 90px;
}
.ob-price.ask { color: #4FC3F7; }
.ob-price.bid { color: #FF5252; }
.ob-price.cur { color: #FFD600; background: #1A1500; border-radius: 4px; }
.ob-buy-qty  {
    text-align: left; padding: 4px 10px; font-size: 0.75rem; color: #64748B;
    font-weight: 500; z-index: 1; position: relative;
}
.ob-bar-ask {
    position: absolute; right: 50%; top: 0; bottom: 0;
    background: rgba(79,195,247,0.07); z-index: 0;
}
.ob-bar-bid {
    position: absolute; left: 50%; top: 0; bottom: 0;
    background: rgba(255,82,82,0.07); z-index: 0;
}
.ob-divider { height: 2px; background: #1E2035; }
.ob-spread {
    text-align: center; padding: 5px; font-size: 0.7rem; color: #374151;
    background: #0C0C18; border-top: 1px solid #1A1A2E; border-bottom: 1px solid #1A1A2E;
}
.ob-total {
    display: flex; justify-content: space-between; padding: 7px 14px;
    font-size: 0.72rem; color: #374151; border-top: 1px solid #1A1A2E;
}
.ob-total .ask-t { color: #4FC3F7; font-weight: 700; }
.ob-total .bid-t { color: #FF5252; font-weight: 700; }

/* ── 포지션 바 ── */
.pos-bar {
    background:#0F1120; border:1px solid #1E2035; border-radius:12px;
    padding:12px 16px; display:flex; justify-content:space-between;
    align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;
}
.pos-item { text-align:center; }
.pos-label { font-size:0.7rem; color:#475569; margin-bottom:2px; }
.pos-value { font-size:0.9rem; font-weight:700; color:#E2E8F0; }

/* ── 주문박스 ── */
.order-box {
    background:#0D0D18; border:1px solid #1E2035; border-radius:14px;
    padding:16px 18px; margin-bottom:12px;
}
.ob2-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:7px; }
.ob2-label { font-size:0.75rem; color:#475569; }
.ob2-val   { font-size:0.85rem; font-weight:700; color:#CBD5E1; }
.ob2-total { font-size:0.98rem; font-weight:700; color:#FFD600; }

/* ── 포트폴리오 테이블 ── */
.port-table { width:100%; border-collapse:collapse; font-size:0.8rem; }
.port-table th {
    text-align:right; color:#475569; font-weight:500;
    padding:6px 8px; border-bottom:1px solid #1E2035; font-size:0.72rem;
}
.port-table th:first-child { text-align:left; }
.port-table td {
    text-align:right; color:#CBD5E1; padding:9px 8px;
    border-bottom:1px solid #0F1120;
}
.port-table td:first-child { text-align:left; color:#E2E8F0; font-weight:600; }
.port-table tr:last-child td { border-bottom:none; }
.port-table tr:hover td { background:#0F1120; }
.pnl-pos { color:#FF5252; font-weight:700; }
.pnl-neg { color:#4FC3F7; font-weight:700; }

/* ── 요약카드 ── */
.sum-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-top:12px; }
.sum-card { background:#0F1120; border:1px solid #1E2035; border-radius:12px; padding:12px 14px; }
.sum-card .s-label { font-size:0.7rem; color:#475569; margin-bottom:4px; }
.sum-card .s-val   { font-size:0.95rem; font-weight:700; color:#E2E8F0; }

/* ── 공통 색상 ── */
.up   { color:#FF5252; } .down { color:#4FC3F7; } .flat { color:#78909C; }
.cd-badge {
    display:inline-block; background:#1A1A2E; border:1px solid #2D2D4E;
    border-radius:8px; padding:3px 9px; font-size:0.7rem; color:#7E86A0; margin:3px 0;
}
.empty-port {
    text-align:center; padding:36px 20px; color:#374151;
    font-size:0.88rem; border:1px dashed #1E2035; border-radius:14px;
}
.news-bar {
    background:#0A0A14; border-left:3px solid #5C6BC0;
    border-radius:0 10px 10px 0; padding:8px 14px;
    font-size:0.8rem; color:#94A3B8; margin-bottom:14px;
    display:flex; align-items:center; gap:8px;
}
.nb-badge {
    background:#1E2440; color:#7986CB; font-size:0.66rem;
    font-weight:700; padding:2px 6px; border-radius:6px; white-space:nowrap;
}

/* ── 시황 탭 선택 차트 패널 ── */
.det-panel {
    background: #0D0D18; border: 1px solid #1E2035; border-radius: 14px;
    padding: 18px 20px; margin-top: 14px;
}
.det-panel .dp-title {
    font-size: 0.78rem; color: #475569; font-weight: 600;
    letter-spacing: 1px; margin-bottom: 10px;
}
</style>
"""

# ────────────────────────────────────────────────────────────────────────────
# 헬퍼
# ────────────────────────────────────────────────────────────────────────────

def _price_diff(d):
    if len(d['history']) > 1:
        delta = d['price'] - d['history'][-2]
        pct   = delta / d['history'][-2] * 100
        return delta, pct
    return 0, 0.0

def _cls(diff):
    if diff > 0: return "up",   "▲"
    if diff < 0: return "down", "▼"
    return "flat", "━"

def _spark_color(diff):
    return "#FF5252" if diff >= 0 else "#4FC3F7"

# ── 호가창 데이터 생성 (현재가 기준 시뮬)
def _make_orderbook(price, vol):
    """현재가 기준 ±10단계 호가 생성 (실제 체결은 현재가로)"""
    step = max(1, int(price * vol * 0.3))
    asks, bids = [], []
    for i in range(1, 11):
        ask_p = price + step * i
        bid_p = price - step * i
        # 잔량: 호가에서 멀수록 많아지는 경향 (+ 노이즈)
        ask_q = int((50 + i * 30) * random.uniform(0.6, 1.6))
        bid_q = int((60 + i * 25) * random.uniform(0.6, 1.6))
        asks.append((ask_p, ask_q))
        bids.append((bid_p, bid_q))
    return asks, bids   # asks: 낮은 가격부터, bids: 높은 가격부터

def _render_orderbook(price, vol):
    asks, bids = _make_orderbook(price, vol)
    asks_rev   = list(reversed(asks))   # 높은 매도호가 → 현재가 쪽으로 내려옴

    max_qty = max(max(q for _, q in asks), max(q for _, q in bids), 1)
    total_ask = sum(q for _, q in asks)
    total_bid = sum(q for _, q in bids)
    spread    = asks[0][0] - bids[0][0]

    rows = ""
    # 매도 10단계 (위 → 아래로 높은→낮은)
    for ap, aq in asks_rev:
        bar_w = int(aq / max_qty * 48)
        rows += f"""
        <div class='ob-row'>
            <div class='ob-bar-ask' style='width:{bar_w}%;'></div>
            <div class='ob-sell-qty'>{aq:,}</div>
            <div class='ob-price ask'>₩{ap:,}</div>
            <div class='ob-buy-qty'></div>
        </div>"""

    # 현재가 행
    diff, pct = _price_diff({'price': price, 'history': [price, price]})
    rows += f"""
    <div class='ob-spread'>스프레드 ₩{spread:,}</div>
    <div class='ob-row'>
        <div class='ob-sell-qty'></div>
        <div class='ob-price cur' style='font-size:0.9rem;'>₩{price:,}</div>
        <div class='ob-buy-qty'></div>
    </div>
    <div class='ob-divider'></div>"""

    # 매수 10단계 (높은→낮은)
    for bp, bq in bids:
        bar_w = int(bq / max_qty * 48)
        rows += f"""
        <div class='ob-row'>
            <div class='ob-bar-bid' style='width:{bar_w}%;'></div>
            <div class='ob-sell-qty'></div>
            <div class='ob-price bid'>₩{bp:,}</div>
            <div class='ob-buy-qty'>{bq:,}</div>
        </div>"""

    # ※ 수정: {rows} 자리에서 rows 가 줄바꿈(\n)으로 시작하기 때문에,
    #   앞쪽 들여쓰기 공백과 합쳐지면 "공백만 있는 줄"(=마크다운이 인식하는 빈 줄)이 생겨버림.
    #   그 빈 줄 때문에 위에서 열려있던 HTML 블록이 끊기고, 그 다음 줄(4칸 이상 들여쓰기)이
    #   마크다운의 "들여쓰기 코드블록"으로 오인식되어 raw HTML 텍스트로 출력되는 버그였음.
    #   rows.strip() 으로 선행 줄바꿈/공백을 제거해 빈 줄이 생기지 않게 하면 해결됨.
    return f"""
    <div class='ob-wrap'>
        <div class='ob-header'>
            <span style='text-align:right;'>잔량(매도)</span>
            <span style='text-align:center;'>호가</span>
            <span>잔량(매수)</span>
        </div>
        {rows.strip()}
        <div class='ob-total'>
            <span>총매도 <span class='ask-t'>{total_ask:,}</span></span>
            <span>총매수 <span class='bid-t'>{total_bid:,}</span></span>
        </div>
    </div>"""

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

    # 선택된 시황 카드 상태
    if "mkt_selected" not in st.session_state:
        st.session_state.mkt_selected = None

    # ── 뉴스 배너 ──
    news_txt = market.get("news", "")
    if news_txt:
        st.markdown(
            f"<div class='news-bar'><span class='nb-badge'>LIVE</span>{news_txt}</div>",
            unsafe_allow_html=True
        )

    # ── 티커 배너 ──
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
    doubled = items_html * 2
    st.markdown(
        f"<div class='ticker-wrap'><div class='ticker-inner'>{doubled}</div></div>",
        unsafe_allow_html=True
    )

    # ── 탭 ──
    tab_market, tab_trade, tab_port = st.tabs(["📊 시황", "⚡ 거래", "💼 포트폴리오"])

    # ════════════════════════════════════════════════════════════
    # TAB 1 — 시황: 카드 클릭 → 아래에 차트 펼치기
    # ════════════════════════════════════════════════════════════
    with tab_market:
        palette = ["#FF5252","#4FC3F7","#69F0AE","#FFD740","#EA80FC",
                   "#FF6D00","#40C4FF","#F48FB1","#B9F6CA","#FF9800"]

        # 카드 클릭 버튼 (Streamlit 버튼을 카드 모양으로)
        cols = st.columns(len(stock_config))
        for i, s in enumerate(stock_config):
            d = market['stock_data'].get(s['id'], {})
            if not d: continue
            diff, pct = _price_diff(d)
            cls, arr  = _cls(diff)
            bar_clr   = "#FF5252" if diff >= 0 else "#4FC3F7"
            bar_w     = min(abs(pct) / 10 * 100, 100)
            is_sel    = st.session_state.mkt_selected == s['id']
            sel_cls   = " sel" if is_sel else ""

            with cols[i]:
                # 카드 HTML (클릭은 아래 버튼으로)
                st.markdown(f"""
                <div class='mkt-card{sel_cls}'>
                    <span class='c-icon'>{s['icon']}</span>
                    <div class='c-name'>{d['name']}</div>
                    <div class='c-price'>₩{d['price']:,}</div>
                    <div class='c-chg {cls}'>{arr} {abs(pct):.2f}%</div>
                    <div class='bar-bg'><div class='bar-fill' style='width:{bar_w:.0f}%;background:{bar_clr};'></div></div>
                </div>
                """, unsafe_allow_html=True)
                btn_label = "✔ 선택됨" if is_sel else "차트보기"
                if st.button(btn_label, key=f"mkt_btn_{s['id']}", use_container_width=True):
                    if is_sel:
                        st.session_state.mkt_selected = None
                    else:
                        st.session_state.mkt_selected = s['id']
                    st.rerun()

        # ── 선택된 종목 차트 패널 ──
        sel_sid = st.session_state.mkt_selected
        if sel_sid and sel_sid in market['stock_data']:
            sd    = market['stock_data'][sel_sid]
            hist  = sd['history']
            diff_s, pct_s = _price_diff(sd)
            cls_s, arr_s  = _cls(diff_s)
            sc    = _spark_color(diff_s)
            s_cfg = next((x for x in stock_config if x['id'] == sel_sid), {})

            st.markdown(f"""
            <div class='det-panel'>
                <div class='dp-title'>{s_cfg.get('icon','')} {sd['name']} — 가격 추이 (최근 {len(hist)}틱)</div>
            </div>
            """, unsafe_allow_html=True)

            fig_s = go.Figure()
            fig_s.add_trace(go.Scatter(
                y=hist, mode='lines',
                line=dict(color=sc, width=2),
                fill='tozeroy',
                fillcolor=f"rgba({'255,82,82' if diff_s>=0 else '79,195,247'},0.07)",
                hovertemplate='₩%{y:,.0f}<extra></extra>'
            ))
            fig_s.add_hline(y=sd['price'], line_width=1, line_dash="dot",
                            line_color="rgba(255,255,255,0.13)")
            # 고가/저가 주석
            fig_s.add_annotation(x=hist.index(max(hist)), y=max(hist),
                text=f"고 ₩{max(hist):,}", showarrow=True, arrowhead=0,
                font=dict(size=9, color="#FF5252"), ay=-22, ax=0)
            fig_s.add_annotation(x=hist.index(min(hist)), y=min(hist),
                text=f"저 ₩{min(hist):,}", showarrow=True, arrowhead=0,
                font=dict(size=9, color="#4FC3F7"), ay=22, ax=0)
            fig_s.update_layout(
                height=220, template='plotly_dark',
                margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                           tickformat=',.0f', tickfont=dict(size=9)),
                showlegend=False,
            )
            st.plotly_chart(fig_s, use_container_width=True)

            # 미니 스탯 (선택 종목)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("현재가",  f"₩{sd['price']:,}")
            c2.metric("등락",    f"{arr_s} {abs(pct_s):.2f}%")
            c3.metric("고가(틱)", f"₩{max(hist):,}")
            c4.metric("저가(틱)", f"₩{min(hist):,}")
        else:
            # 전체 멀티라인 차트
            st.markdown("<div style='margin-top:16px;margin-bottom:5px;color:#374151;font-size:0.75rem;font-weight:600;letter-spacing:1px;'>▲ 종목 클릭 시 개별 차트 표시 &nbsp;|&nbsp; 전 종목 추이 (정규화)</div>", unsafe_allow_html=True)
            fig = go.Figure()
            for i, s in enumerate(stock_config):
                d = market['stock_data'].get(s['id'], {})
                if not d or not d.get('history'): continue
                hist = d['history']
                norm = [v / hist[0] * 100 for v in hist] if hist[0] else hist
                fig.add_trace(go.Scatter(
                    y=norm, mode='lines', name=d['name'],
                    line=dict(color=palette[i % len(palette)], width=1.5),
                    hovertemplate=f"{d['name']}<br>%{{y:.1f}}<extra></extra>"
                ))
            fig.update_layout(
                height=240, template='plotly_dark',
                margin=dict(l=0,r=0,t=8,b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", y=-0.3, font=dict(size=10)),
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                           title='(시작=100)', titlefont=dict(size=9), tickfont=dict(size=9)),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ════════════════════════════════════════════════════════════
    # TAB 2 — 거래 (호가창 포함)
    # ════════════════════════════════════════════════════════════
    with tab_trade:
        options = [f"{s['icon']} {s['name']}" for s in stock_config]
        sel_n   = st.selectbox("종목", options, label_visibility="collapsed")
        sid     = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == sel_n)
        s_cfg   = next(s for s in stock_config if s['id'] == sid)
        d       = market['stock_data'][sid]
        cp      = d['price']
        diff, pct  = _price_diff(d)
        cls, arr   = _cls(diff)
        spark_clr  = _spark_color(diff)

        # ── 종목 헤더 ──
        prev_price = d['history'][-2] if len(d['history']) > 1 else cp
        high_t = max(d['history']); low_t = min(d['history'])
        st.markdown(f"""
        <div class='det-header'>
            <div class='det-left'>
                <div class='d-icon-name'>
                    <span class='d-icon'>{s_cfg['icon']}</span>
                    <div>
                        <div class='d-name'>{d['name']}</div>
                        <div class='d-id'>{sid}</div>
                    </div>
                </div>
                <div style='display:flex;gap:18px;margin-top:7px;'>
                    <div><div style='font-size:0.65rem;color:#374151;'>고가</div><div style='font-size:0.8rem;color:#FF5252;font-weight:700;'>₩{high_t:,}</div></div>
                    <div><div style='font-size:0.65rem;color:#374151;'>저가</div><div style='font-size:0.8rem;color:#4FC3F7;font-weight:700;'>₩{low_t:,}</div></div>
                    <div><div style='font-size:0.65rem;color:#374151;'>전일</div><div style='font-size:0.8rem;color:#94A3B8;font-weight:600;'>₩{prev_price:,}</div></div>
                </div>
            </div>
            <div class='det-right'>
                <div class='d-price'>₩{cp:,}</div>
                <div class='d-chg {cls}'>{arr} {abs(pct):.2f}% ({'+' if diff>=0 else ''}{diff:,}원)</div>
                <div class='d-prev'>잔고 {format_korean_money(st.session_state.global_cash)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── 차트 + 호가창 2컬럼 ──
        col_chart, col_ob = st.columns([3, 2])

        with col_chart:
            if len(d['history']) > 1:
                hist = d['history']
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    y=hist, mode='lines',
                    line=dict(color=spark_clr, width=2),
                    fill='tozeroy',
                    fillcolor=f"rgba({'255,82,82' if diff>=0 else '79,195,247'},0.06)",
                    hovertemplate='₩%{y:,.0f}<extra></extra>'
                ))
                fig2.add_hline(y=cp, line_width=1, line_dash="dot",
                               line_color="rgba(255,255,255,0.13)")
                fig2.update_layout(
                    height=360, template='plotly_dark',
                    margin=dict(l=0,r=0,t=4,b=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                               tickformat=',.0f', tickfont=dict(size=9)),
                    showlegend=False,
                )
                st.plotly_chart(fig2, use_container_width=True)

        with col_ob:
            # 호가창
            vol = s_cfg.get('vol', 0.03)
            st.markdown(_render_orderbook(cp, vol), unsafe_allow_html=True)

        # ── 보유 포지션 ──
        my_info = st.session_state.portfolio.get(sid, {'qty': 0, 'avg_price': 0})
        my_qty  = my_info.get('qty', 0)
        my_avg  = my_info.get('avg_price', 0)

        if my_qty > 0:
            my_eval = my_qty * cp
            my_pnl  = my_eval - my_qty * my_avg
            my_roi  = (cp - my_avg) / my_avg * 100 if my_avg > 0 else 0
            roi_cls, roi_arr = _cls(my_roi)
            pnl_cls = "pnl-pos" if my_pnl >= 0 else "pnl-neg"
            st.markdown(f"""
            <div class='pos-bar'>
                <div class='pos-item'><div class='pos-label'>보유</div><div class='pos-value'>{my_qty:,}주</div></div>
                <div class='pos-item'><div class='pos-label'>평균단가</div><div class='pos-value'>₩{int(my_avg):,}</div></div>
                <div class='pos-item'><div class='pos-label'>평가액</div><div class='pos-value' style='color:#FFD600;'>₩{int(my_eval):,}</div></div>
                <div class='pos-item'><div class='pos-label'>평가손익</div><div class='pos-value {pnl_cls}'>{'+' if my_pnl>=0 else ''}{format_korean_money(int(my_pnl))}</div></div>
                <div class='pos-item'><div class='pos-label'>수익률</div><div class='pos-value {roi_cls}'>{roi_arr} {abs(my_roi):.2f}%</div></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                "<div style='background:#0A0A12;border:1px dashed #1A1A2A;border-radius:10px;"
                "padding:10px 16px;color:#374151;font-size:0.78rem;margin-bottom:10px;'>"
                "보유 포지션 없음</div>", unsafe_allow_html=True
            )

        # ── 수량 입력 ──
        max_buyable = int(st.session_state.global_cash // cp) if cp > 0 else 0
        col_qty, col_pct = st.columns([2, 1])
        with col_qty:
            qty_input = st.number_input(
                "수량(주)", min_value=1,
                max_value=max(1, max_buyable if max_buyable else 999_999),
                step=1, value=1, key="stock_qty"
            )
        with col_pct:
            pct_sel = st.selectbox("비율", ["직접입력","10%","25%","50%","100%"], key="stock_pct")
            if pct_sel != "직접입력":
                ratio     = int(pct_sel.replace("%","")) / 100
                qty_input = max(1, int(max_buyable * ratio))

        cost = qty_input * cp
        st.markdown(f"""
        <div class='order-box'>
            <div class='ob2-row'><span class='ob2-label'>거래 단가</span><span class='ob2-val'>₩{cp:,}</span></div>
            <div class='ob2-row'><span class='ob2-label'>수량</span><span class='ob2-val'>{qty_input:,}주</span></div>
            <div class='ob2-row' style='border-top:1px solid #1E2035;padding-top:9px;margin-top:4px;'>
                <span class='ob2-label'>예상 금액</span><span class='ob2-total'>{format_korean_money(cost)}</span>
            </div>
            <div class='ob2-row'><span class='ob2-label'>최대 매수 가능</span><span class='ob2-val' style='color:#475569;'>{max_buyable:,}주</span></div>
        </div>
        """, unsafe_allow_html=True)

        # ── 쿨다운 ──
        bulk_rem  = cooldown_remaining("bulk_trade", BULK_COOLDOWN)
        trade_rem = cooldown_remaining(f"trade_{sid}", TRADE_COOLDOWN)
        bulk_left = DAILY_BULK_LIMIT - st.session_state.get("bulk_trade_count", 0)
        cd_parts  = []
        if trade_rem > 0: cd_parts.append(f"일반 {trade_rem:.1f}초")
        if bulk_rem  > 0: cd_parts.append(f"풀매 {bulk_rem:.1f}초")
        if cd_parts:
            st.markdown(f"<span class='cd-badge'>⏱ {' · '.join(cd_parts)}</span>", unsafe_allow_html=True)
        st.markdown(
            f"<div style='font-size:0.7rem;color:#374151;margin-bottom:8px;'>"
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
            u_db   = load_db(USERS_FILE, {})
            db_own = u_db.get(st.session_state.logged_in_user, {}).get(
                'portfolio', {}).get(sid_, {}).get('qty', 0)
            if db_own < qty: st.error("보유 수량 부족! (DB 검증)"); return False
            earn = qty * price
            st.session_state.global_cash += earn
            st.session_state.portfolio[sid_]['qty'] -= qty
            log_tx(st.session_state.logged_in_user, "주식매도",
                   f"{market['stock_data'][sid_]['name']} {qty}주 매도", earn)
            return True

        # ── 거래 버튼 4개 ──
        bulk_ok = (bulk_rem <= 0) and (bulk_left > 0)
        bc1, bc2, bc3, bc4 = st.columns(4)

        with bc1:
            if st.button("💥 풀매수", use_container_width=True, disabled=not bulk_ok, key="btn_bulk_buy"):
                mq = max_buyable
                if mq > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count",0)+1
                    if _safe_buy(mq, cp, sid):
                        imp = min(((mq*cp)/500_000_000_000)*0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = int(cp*(1+imp))
                            market['news'] = f"🐋 [고래] {st.session_state.logged_in_user}님 {d['name']} 거액 매수! +{imp*100:.1f}%"
                            save_market(market)
                        sync_user_data(); st.rerun()
                else:
                    st.error("잔액 부족!")

        with bc2:
            if st.button(f"🟢 {qty_input}주 매수", use_container_width=True,
                         disabled=trade_rem>0, key="btn_buy"):
                set_cooldown(f"trade_{sid}")
                if _safe_buy(qty_input, cp, sid):
                    sync_user_data()
                    st.success(f"✅ {qty_input}주 매수!")
                    st.rerun()

        with bc3:
            if st.button(f"🔴 {qty_input}주 매도", use_container_width=True,
                         disabled=trade_rem>0, key="btn_sell"):
                set_cooldown(f"trade_{sid}")
                if _safe_sell(qty_input, cp, sid):
                    sync_user_data()
                    st.success(f"✅ {qty_input}주 매도!")
                    st.rerun()

        with bc4:
            if st.button("💸 풀매도", use_container_width=True,
                         disabled=not bulk_ok, key="btn_bulk_sell"):
                own = st.session_state.portfolio.get(sid, {'qty':0})['qty']
                if own > 0:
                    set_cooldown("bulk_trade")
                    st.session_state.bulk_trade_count = st.session_state.get("bulk_trade_count",0)+1
                    if _safe_sell(own, cp, sid):
                        imp = min(((own*cp)/500_000_000_000)*0.15, 0.08)
                        if imp > 0.005:
                            market['stock_data'][sid]['price'] = max(1_000, int(cp*(1-imp)))
                            market['news'] = f"📉 [고래] {st.session_state.logged_in_user}님 {d['name']} 물량 투하! -{imp*100:.1f}%"
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
        p_rows = []; total_eval=0; total_invested=0; total_pnl=0

        for sid_p, info in st.session_state.portfolio.items():
            qty = info.get('qty', 0)
            if qty <= 0 or sid_p not in market['stock_data']: continue
            cp_p = market['stock_data'][sid_p]['price']
            ap   = info.get('avg_price', 0)
            inv  = qty*ap;  total_invested += inv
            ev   = qty*cp_p; total_eval    += ev
            pnl  = ev-inv;   total_pnl     += pnl
            roi  = (cp_p-ap)/ap*100 if ap>0 else 0
            icon = next((s['icon'] for s in stock_config if s['id']==sid_p), '📊')
            nm   = market['stock_data'][sid_p]['name']
            diff_p, pct_p = _price_diff(market['stock_data'][sid_p])
            cls_p, arr_p  = _cls(diff_p)
            p_rows.append({
                "_nm":f"{icon} {nm}", "_qty":qty, "_ap":ap,
                "_cp":cp_p, "_ev":ev, "_pnl":pnl, "_roi":roi,
                "_cls":cls_p, "_arr":arr_p, "_pct":pct_p,
            })

        if p_rows:
            rows_html = ""
            for r in sorted(p_rows, key=lambda x:-x['_ev']):
                roi_cls = "pnl-pos" if r['_roi']>=0 else "pnl-neg"
                pnl_cls = "pnl-pos" if r['_pnl']>=0 else "pnl-neg"
                rows_html += f"""
                <tr>
                    <td>{r['_nm']}</td>
                    <td>{r['_qty']:,}주</td>
                    <td>₩{int(r['_ap']):,}</td>
                    <td>₩{int(r['_cp']):,} <span class='{r['_cls']}' style='font-size:0.7rem;'>{r['_arr']}{abs(r['_pct']):.1f}%</span></td>
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

            total_roi = (total_eval-total_invested)/total_invested*100 if total_invested else 0
            roi_cls_t = "pnl-pos" if total_pnl>=0 else "pnl-neg"
            st.markdown(f"""
            <div class='sum-grid'>
                <div class='sum-card'><div class='s-label'>총 매수금액</div><div class='s-val'>{format_korean_money(int(total_invested))}</div></div>
                <div class='sum-card'><div class='s-label'>총 평가액</div><div class='s-val' style='color:#FFD600;'>{format_korean_money(int(total_eval))}</div></div>
                <div class='sum-card'><div class='s-label'>총 손익 / 수익률</div>
                    <div class='s-val {roi_cls_t}'>{'+' if total_pnl>=0 else ''}{format_korean_money(int(total_pnl))} <span style='font-size:0.8rem;'>({'+' if total_roi>=0 else ''}{total_roi:.2f}%)</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 파이차트
            st.markdown("<div style='margin-top:18px;margin-bottom:4px;color:#374151;font-size:0.72rem;font-weight:600;letter-spacing:1px;'>보유 종목 비중</div>", unsafe_allow_html=True)
            pie = go.Figure(go.Pie(
                labels=[r['_nm'] for r in p_rows],
                values=[r['_ev'] for r in p_rows],
                hole=0.55,
                textinfo='label+percent', textfont=dict(size=11),
                marker=dict(
                    colors=["#FF5252","#4FC3F7","#69F0AE","#FFD740","#EA80FC",
                             "#FF6D00","#40C4FF","#F48FB1","#B9F6CA","#FF9800"],
                    line=dict(color='#0D0D18', width=2)
                ),
                hovertemplate='%{label}<br>₩%{value:,.0f}<br>%{percent}<extra></extra>'
            ))
            pie.add_annotation(text=f"<b>{format_korean_money(int(total_eval))}</b>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=13, color="#E2E8F0"))
            pie.update_layout(
                height=270, template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0,r=0,t=8,b=8),
                legend=dict(orientation="h", font=dict(size=10), y=-0.1),
            )
            st.plotly_chart(pie, use_container_width=True)

        else:
            st.markdown("""
            <div class='empty-port'>
                📭<br><br>보유 중인 주식이 없습니다.<br>
                <span style='font-size:0.75rem;color:#1E2035;'>거래 탭에서 종목을 선택하고 매수해보세요.</span>
            </div>
            """, unsafe_allow_html=True)
