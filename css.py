# ============================================================
# utils/css.py — 전체 CSS (누락 클래스 모두 정의)
# ============================================================

def get_css(theme_color: str = "#00E5FF") -> str:
    return f"""
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

* {{ box-sizing: border-box; }}

html, body, p, span, div, td, th {{
  font-family: 'Noto Sans KR', -apple-system, sans-serif !important;
  color: #FFFFFF !important;
}}

/* ── 앱 배경 ── */
.stApp {{
  background-color: #080A12 !important;
  background-image:
    radial-gradient(circle at 15% 30%, {theme_color}0D, transparent 30%),
    radial-gradient(circle at 85% 70%, rgba(255, 0, 200, 0.05), transparent 30%) !important;
  background-attachment: fixed;
}}

[data-testid='stSidebar'] {{
  background: rgba(10, 12, 20, 0.95) !important;
  border-right: 1px solid {theme_color}26 !important;
}}

/* ── 헤딩 ── */
h1 {{ font-family:'Orbitron',sans-serif !important; font-size:1.8rem !important; font-weight:900 !important; color:#FFF !important; text-shadow:0 0 10px {theme_color}4D; }}
h2 {{ font-size:1.3rem !important; font-weight:800 !important; color:#00FF88 !important; }}
h3 {{ font-size:1.1rem !important; font-weight:800 !important; color:#FFD600 !important; }}

/* ── 라벨 ── */
label, label p, label div, .stRadio label,
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] div {{
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}}

/* ── 입력 ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {{
  background: rgba(0,0,0,0.5) !important;
  border: 1px solid {theme_color}4D !important;
  border-radius: 8px !important;
  color: #FFF !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
}}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {{
  border-color: {theme_color} !important;
  box-shadow: 0 0 10px {theme_color}4D !important;
}}

/* ── 드롭다운 ── */
div[data-baseweb="select"] > div {{ background-color: #FFFFFF !important; }}
div[data-baseweb="select"] * {{ color: #000000 !important; font-weight: 600 !important; }}

/* ── 버튼 ── */
.stButton > button {{
  font-family: 'Noto Sans KR', sans-serif !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  border: 1px solid {theme_color}66 !important;
  background: linear-gradient(135deg, {theme_color}0D, rgba(0,102,255,0.1)) !important;
  color: {theme_color} !important;
  transition: all 0.2s ease !important;
  font-size: 0.95rem !important;
  height: 46px !important;
}}
.stButton > button:hover {{
  background: linear-gradient(135deg, {theme_color}, #0066FF) !important;
  border-color: {theme_color} !important;
  color: #000 !important;
  box-shadow: 0 4px 15px {theme_color}66 !important;
  transform: translateY(-2px);
}}

/* ── 탭 ── */
.stTabs [data-baseweb="tab-list"] {{ background: transparent !important; border-bottom: 1px solid rgba(255,255,255,0.1) !important; }}
.stTabs [aria-selected="true"] {{ color: {theme_color} !important; border-bottom: 2px solid {theme_color} !important; text-shadow: 0 0 10px {theme_color}4D; }}

/* ── 일반 카드 ── */
.card {{
  background: rgba(20,24,35,0.6) !important;
  backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px;
  padding: 20px;
  margin: 8px 0;
  transition: all 0.3s ease;
}}
.card:hover {{ border-color: {theme_color}4D !important; box-shadow: 0 6px 20px {theme_color}1A; }}

/* ── 뉴스 배너 ── */
.news-banner {{
  background: linear-gradient(90deg, rgba(0,229,255,0.08), rgba(0,0,0,0));
  border-left: 3px solid {theme_color};
  padding: 10px 16px;
  border-radius: 0 8px 8px 0;
  margin: 8px 0 16px 0;
  font-size: 0.92rem;
  color: #E2E8F0 !important;
  font-weight: 600;
}}

/* ── VIP 배너 ── */
.vip-banner {{
  background: linear-gradient(135deg, rgba(255,215,0,0.08), rgba(180,0,255,0.08));
  border: 2px solid rgba(255,215,0,0.4);
  border-radius: 16px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 0 30px rgba(255,215,0,0.15);
  margin-bottom: 20px;
}}

/* ── 주식 테이블 ── */
.stock-table {{ width:100%; border-collapse:collapse; font-size:0.92rem; }}
.stock-table th {{
  color:#888; font-weight:600; padding:8px 12px;
  border-bottom:1px solid rgba(255,255,255,0.08); text-align:left;
}}
.stock-table td {{ padding:8px 12px; border-bottom:1px solid rgba(255,255,255,0.04); }}
.stock-table tr:hover td {{ background:rgba(255,255,255,0.02); }}
.p-up   {{ color:#FF4B4B; font-weight:900; }}
.p-down {{ color:#4B9EFF; font-weight:900; }}
.p-flat {{ color:#888; }}

/* ── 거래 기록 행 ── */
.tx-row {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.88rem;
}}

/* ── 슬롯 디스플레이 ── */
.slot-display {{
  text-align: center;
  font-size: 3.5rem;
  background: rgba(0,0,0,0.5);
  border: 2px solid {theme_color}44;
  border-radius: 16px;
  padding: 20px;
  margin: 16px 0;
  letter-spacing: 10px;
}}

/* ── 광산 카드 ── */
.mine-card {{
  background: linear-gradient(135deg, rgba(50,30,0,0.6), rgba(20,10,0,0.8));
  border: 2px solid rgba(200,150,50,0.4);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
}}

/* ── 로또 ── */
.lotto-pool {{
  background: linear-gradient(135deg, rgba(180,0,255,0.15), rgba(0,0,100,0.2));
  border: 2px solid rgba(180,0,255,0.5);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 0 40px rgba(180,0,255,0.2);
  margin-bottom: 20px;
}}
.lotto-amount {{
  font-family: 'Orbitron', monospace;
  font-size: clamp(1.5rem, 4vw, 2.8rem);
  font-weight: 900;
  color: #FF00FF;
  text-shadow: 0 0 20px rgba(255,0,255,0.6);
}}

/* ── 질문 박스 (CBT) ── */
.question-box {{
  background: rgba(0,229,255,0.06);
  border: 1px solid {theme_color}44;
  border-radius: 12px;
  padding: 20px 24px;
  font-size: 1.05rem;
  font-weight: 700;
  color: #E2E8F0 !important;
  line-height: 1.6;
  margin-bottom: 16px;
}}

/* ── 스코어보드 (축구/승부차기) ── */
.scoreboard {{
  background: linear-gradient(135deg, rgba(20,20,40,0.9), rgba(10,10,30,0.95));
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  margin-bottom: 20px;
  box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}}
.team-label {{
  font-size: 1.1rem;
  font-weight: 900;
  color: #E2E8F0;
  margin-bottom: 4px;
}}
.score-number {{
  font-family: 'Orbitron', monospace;
  font-size: 2.8rem;
  font-weight: 900;
  color: #FFD600;
  text-shadow: 0 0 20px rgba(255,214,0,0.4);
}}
.match-time {{
  color: #888;
  font-size: 0.85rem;
  margin-top: 4px;
}}
.commentary-item {{
  background: rgba(255,255,255,0.03);
  border-radius: 6px;
  padding: 8px 12px;
  margin: 4px 0;
  font-size: 0.88rem;
  color: #94A3B8 !important;
  border-left: 2px solid {theme_color}44;
}}

/* ── 부동산 ── */
.estate-card {{
  background: rgba(20,24,35,0.7);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 18px 20px;
  margin: 10px 0;
  transition: all 0.3s;
}}
.estate-card:hover {{ border-color: #00FF8844; box-shadow: 0 4px 16px rgba(0,255,136,0.1); }}
.estate-income {{ color: #00FF88 !important; font-weight: 900; font-size: 0.85rem; }}
.market-initial {{
  background: rgba(0,229,255,0.04);
  border: 1px solid {theme_color}22;
  border-radius: 12px;
  padding: 14px 16px;
  margin: 6px 0;
}}
.market-listing {{
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 10px;
  padding: 12px 14px;
  margin: 4px 0;
}}
.my-listing {{
  background: rgba(255,214,0,0.04);
  border: 1px solid rgba(255,214,0,0.2);
  border-radius: 10px;
  padding: 12px 14px;
  margin: 4px 0;
}}

/* ── 쿨다운 배지 ── */
.cooldown-badge {{
  background: rgba(255,75,75,0.15);
  border: 1px solid #FF4B4B44;
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 0.82rem;
  color: #FF4B4B !important;
  display: inline-block;
  margin: 4px 0;
}}

/* ── 사이드바 긴급 버튼 ── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {{
    background-color: #FF4B4B !important;
    border: 2px solid #FF0000 !important;
    border-radius: 8px !important;
    width: 40px !important;
    height: 40px !important;
    box-shadow: 0 4px 10px rgba(255,75,75,0.5) !important;
    z-index: 999999 !important;
}}

/* ── 익스팬더 아이콘 정리 ── */
[data-testid="stExpanderToggleIcon"],
.streamlit-expanderHeader svg {{ display: none !important; }}

/* ── 모바일 최적화 ── */
@media (max-width: 768px) {{
    .block-container {{ zoom: 0.92; padding-top: 2rem !important; }}
    .stButton>button {{ height:40px !important; font-size:0.85rem !important; }}
    .score-number {{ font-size: 2rem; }}
}}
"""
