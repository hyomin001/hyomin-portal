import streamlit as st


def apply_css():
    IS_PC = "🖥️" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

    CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');
.stApp {
  background:#060610 !important;
  background-image:
    radial-gradient(ellipse at 0% 0%,rgba(0,229,255,0.06) 0%,transparent 50%),
    radial-gradient(ellipse at 100% 100%,rgba(255,0,200,0.06) 0%,transparent 50%) !important;
}
html,body,p,span,label,div { font-family:'Noto Sans KR',sans-serif !important; color:#E8E8F0 !important; }
h1,h2,h3 { font-family:'Orbitron',monospace !important; letter-spacing:2px; }
[data-testid='stSidebar'] {
  background:linear-gradient(180deg,#080818 0%,#0a0a20 100%) !important;
  border-right:1px solid rgba(0,229,255,0.2) !important;
}
.stTextInput>div>div>input,
.stNumberInput>div>div>input {
  background:#FFF !important; border:2px solid #00E5FF !important;
  border-radius:8px !important; color:#000 !important; font-weight:900 !important;
}
div[data-baseweb="select"]>div {
  background:rgba(255,255,255,0.04) !important;
  border:1px solid rgba(0,229,255,0.25) !important; border-radius:8px !important;
}
div[role="listbox"] { background:#111128 !important; border:1px solid #00E5FF !important; border-radius:10px !important; }
div[role="listbox"] li,div[role="listbox"] span { color:#fff !important; }
div[role="listbox"] li:hover { background:rgba(0,229,255,0.15) !important; }
.stButton>button {
  font-family:'Noto Sans KR',sans-serif !important; font-weight:900 !important;
  border-radius:10px !important; border:1px solid rgba(0,229,255,0.4) !important;
  background:rgba(0,229,255,0.07) !important; color:#00E5FF !important;
  transition:all 0.25s ease !important;
}
.stButton>button:hover {
  background:rgba(0,229,255,0.18) !important; border-color:#00E5FF !important;
  box-shadow:0 0 18px rgba(0,229,255,0.35) !important; transform:translateY(-1px) !important;
}
.stTabs [data-baseweb="tab-list"] { background:transparent !important; border-bottom:1px solid rgba(0,229,255,0.15) !important; }
.stTabs [data-baseweb="tab"] { color:#777 !important; font-weight:700 !important; font-size:0.95rem !important; padding:10px 20px !important; }
.stTabs [aria-selected="true"] { color:#00E5FF !important; border-bottom:2px solid #00E5FF !important; background:transparent !important; }
[data-testid="stMetric"] {
  background:rgba(255,255,255,0.03) !important; border:1px solid rgba(0,229,255,0.15) !important;
  border-radius:12px !important; padding:14px 18px !important;
}
[data-testid="stMetricLabel"] { color:#888 !important; font-size:0.8rem !important; }
[data-testid="stMetricValue"] { color:#FFD600 !important; font-family:'Orbitron',monospace !important; font-size:1.3rem !important; }
.stAlert { border-radius:10px !important; border:none !important; }
.stProgress>div>div { background:linear-gradient(90deg,#00E5FF,#FF00FF) !important; border-radius:4px !important; }
.stock-table { width:100%; border-collapse:collapse; }
.stock-table th {
  background:rgba(0,229,255,0.08); color:#00E5FF !important;
  font-family:'Orbitron',monospace !important; font-size:0.75rem !important;
  padding:10px 14px; text-align:left; border-bottom:1px solid rgba(0,229,255,0.2); letter-spacing:1px;
}
.stock-table td { padding:11px 14px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.95rem; vertical-align:middle; }
.stock-table tr:hover td { background:rgba(0,229,255,0.04); }
.p-up { color:#FF4B4B !important; font-weight:900; }
.p-down { color:#4B9EFF !important; font-weight:900; }
.p-flat { color:#888 !important; }
.card {
  background:rgba(255,255,255,0.03); border:1px solid rgba(0,229,255,0.15);
  border-radius:14px; padding:20px; margin:8px 0; transition:all 0.3s;
}
.card:hover { border-color:rgba(0,229,255,0.4); box-shadow:0 4px 20px rgba(0,229,255,0.1); }
.news-banner {
  background:linear-gradient(135deg,rgba(255,180,0,0.1),rgba(255,100,0,0.08));
  border:1px solid rgba(255,180,0,0.3); border-radius:10px; padding:12px 18px;
  font-weight:700; color:#FFD600 !important; margin:12px 0; font-size:0.95rem;
}
.scoreboard {
  background:linear-gradient(135deg,#0d1b2a,#1a1a3e);
  border:2px solid rgba(0,229,255,0.4); border-radius:16px; padding:28px; text-align:center;
  box-shadow:0 0 40px rgba(0,229,255,0.15),inset 0 0 40px rgba(0,0,50,0.5);
}
.score-number { font-family:'Orbitron',monospace !important; font-size:3.5rem !important; font-weight:900; color:#00FF88 !important; text-shadow:0 0 20px rgba(0,255,136,0.5); line-height:1; }
.team-label { font-size:1.2rem; font-weight:900; color:#FFD600 !important; margin-bottom:8px; }
.match-time { font-family:'Orbitron',monospace !important; color:#00E5FF !important; font-size:1rem; margin-top:14px; }
.commentary-item {
  background:rgba(255,255,255,0.04); border-left:3px solid #00E5FF;
  padding:10px 15px; margin:6px 0; border-radius:0 8px 8px 0; font-size:0.9rem; color:#ddd !important;
  animation:slideIn 0.4s ease;
}
@keyframes slideIn { from{opacity:0;transform:translateX(-10px)} to{opacity:1;transform:translateX(0)} }
.estate-card {
  background:linear-gradient(135deg,rgba(255,215,0,0.05),rgba(255,100,0,0.05));
  border:1px solid rgba(255,215,0,0.2); border-radius:14px; padding:18px 22px; margin:10px 0;
}
.estate-income { color:#00FF88 !important; font-weight:900; font-size:0.9rem; }
.profit { color:#FF4B4B !important; font-weight:900; }
.loss   { color:#4B9EFF !important; font-weight:900; }
.vip-banner {
  background:linear-gradient(135deg,#1a0a00,#2d1000);
  border:2px solid rgba(255,215,0,0.5); border-radius:16px; padding:22px; text-align:center;
  box-shadow:0 0 30px rgba(255,180,0,0.2);
}
.lotto-pool {
  background:linear-gradient(135deg,#1a003a,#2d0060);
  border:2px solid rgba(180,0,255,0.5); border-radius:16px; padding:24px; text-align:center;
  box-shadow:0 0 40px rgba(180,0,255,0.2);
}
.lotto-amount { font-family:'Orbitron',monospace !important; font-size:2.2rem !important; color:#FF00FF !important; text-shadow:0 0 20px rgba(255,0,255,0.5); font-weight:900; }
.slot-display {
  font-size:3.5rem; text-align:center; padding:20px;
  background:rgba(0,0,0,0.5); border:2px solid rgba(255,215,0,0.3); border-radius:14px;
  letter-spacing:20px; min-height:100px; display:flex; align-items:center; justify-content:center;
}
.question-box {
  background:linear-gradient(135deg,rgba(0,229,255,0.04),rgba(0,0,100,0.1));
  border:1px solid rgba(0,229,255,0.3); border-radius:14px; padding:28px;
  line-height:1.8; font-size:1.05rem; color:#f0f0ff !important;
}
.mine-card {
  background:linear-gradient(135deg,rgba(139,69,19,0.15),rgba(50,25,0,0.2));
  border:1px solid rgba(180,100,20,0.4); border-radius:14px; padding:20px; text-align:center;
}
.tx-row {
  display:flex; justify-content:space-between; align-items:center;
  padding:9px 14px; border-bottom:1px solid rgba(255,255,255,0.05); font-size:0.88rem;
}
"""

    if IS_PC:
        CSS += """
p,span,label,td,th,.stSelectbox label { font-size:1rem !important; }
h1 { font-size:2.2rem !important; color:#00E5FF !important; margin-bottom:4px; }
h2 { font-size:1.5rem !important; color:#00FF88 !important; }
h3 { font-size:1.2rem !important; color:#FFD600 !important; }
.stButton>button { height:52px !important; font-size:1rem !important; }
"""
    else:
        CSS += """
p,span,label,td,th { font-size:0.88rem !important; }
h1 { font-size:1.5rem !important; color:#00E5FF !important; }
h2 { font-size:1.15rem !important; color:#00FF88 !important; }
h3 { font-size:1rem !important; color:#FFD600 !important; }
.stButton>button { height:46px !important; font-size:0.88rem !important; }
.stock-table th,.stock-table td { padding:8px 8px; font-size:0.82rem !important; }
.score-number { font-size:2.5rem !important; }
.lotto-amount { font-size:1.6rem !important; }
"""

    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
    return IS_PC
