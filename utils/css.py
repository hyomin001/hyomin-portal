GLOBAL_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

* { box-sizing: border-box; }
/* 스트림릿 기본 파일 메뉴 숨기기 */
[data-testid="stSidebarNav"] { display: none !important; }

/* =======================================================
   [수정됨] 아이콘 깨짐 방지! 
   위험한 div, span 강제 덮어쓰기를 제거하고 안전한 태그에만 적용
======================================================== */
html, body, p, td, th, li, a {
  font-family: 'Noto Sans KR', -apple-system, sans-serif !important;
  color: #FFFFFF !important; 
}

/* 클랜(Expander) 제목 등 특정 영역 글자만 안전하게 흰색 처리 */
.streamlit-expanderHeader {
  color: #FFFFFF !important;
  font-family: 'Noto Sans KR', -apple-system, sans-serif !important;
}

/* 로그인 화면 텍스트 강제 흰색 처리 */
label, label p, label div, .stRadio label, [data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] div {
    color: #FFFFFF !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
}

/* 프리미엄 다크 스페이스 배경 */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {
  background-color: #080A12 !important;
  background-image:
    radial-gradient(circle at 15% 30%, rgba(0, 229, 255, 0.05), transparent 30%),
    radial-gradient(circle at 85% 70%, rgba(255, 0, 200, 0.05), transparent 30%) !important;
  background-attachment: fixed;
}

/* block-container 투명 처리 (배경 덮어씌워지는 현상 방지) */
[data-testid="stVerticalBlock"],
.block-container {
  background: transparent !important;
}

[data-testid='stSidebar'] {
  background: rgba(10, 12, 20, 0.95) !important;
  border-right: 1px solid rgba(0, 229, 255, 0.15) !important;
}

h1 { font-family:'Orbitron', sans-serif !important; font-size: 1.8rem !important; font-weight: 900 !important; color: #FFF !important; text-shadow: 0 0 10px rgba(0,229,255,0.3); }
h2 { font-size: 1.3rem !important; font-weight: 800 !important; color: #00FF88 !important; }
h3 { font-size: 1.1rem !important; font-weight: 800 !important; color: #FFD600 !important; }

/* 입력창 네온 스타일 */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
  background: rgba(0, 0, 0, 0.5) !important;
  border: 1px solid rgba(0, 229, 255, 0.3) !important;
  border-radius: 8px !important;
  color: #FFF !important;
  font-size: 1rem !important;
  font-weight: 700 !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
  border-color: #00E5FF !important;
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.3) !important;
}

/* 드롭다운 및 팝업 스타일 (글씨 안 보이는 현상 완벽 수정) */
div[data-baseweb="select"] > div { background-color: #FFFFFF !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] div { color: #000000 !important; font-weight: 600 !important; }

[data-baseweb="popover"] { background-color: #FFFFFF !important; }
[data-baseweb="popover"] span, [data-baseweb="popover"] div, 
[role="listbox"] span, [role="listbox"] div, [role="listbox"] li,
[data-baseweb="menu"] span, [data-baseweb="menu"] div, [data-baseweb="menu"] li { 
    color: #000000 !important; 
}
[role="listbox"], [data-baseweb="menu"] { background-color: #FFFFFF !important; }
[role="option"]:hover, [data-baseweb="menu"] li:hover, [role="option"]:hover span, [role="option"]:hover div { 
    background-color: #EEEEEE !important; 
}

/* 사이버펑크 버튼 스타일 */
.stButton > button {
  font-family: 'Noto Sans KR', sans-serif !important;
  font-weight: 700 !important;
  border-radius: 8px !important;
  border: 1px solid rgba(0, 229, 255, 0.4) !important;
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.05), rgba(0, 102, 255, 0.1)) !important;
  color: #00E5FF !important;
  transition: all 0.2s ease !important;
  font-size: 0.95rem !important;
  height: 46px !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, #00E5FF, #0066FF) !important;
  border-color: #00E5FF !important;
  color: #000 !important;
  box-shadow: 0 4px 15px rgba(0, 229, 255, 0.4) !important;
  transform: translateY(-2px);
}

/* 공통 카드 (글래스모피즘) */
.card {
  background: rgba(20, 24, 35, 0.6) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 14px;
  padding: 20px;
  margin: 8px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.card:hover { border-color: rgba(0, 229, 255, 0.3) !important; box-shadow: 0 6px 20px rgba(0, 229, 255, 0.1); }

/* 테이블 (주식, 코인) */
.stock-table { width: 100%; border-collapse: collapse; }
.stock-table th { background: rgba(0, 229, 255, 0.1); color: #00E5FF !important; font-family: 'Orbitron', sans-serif !important; font-size: 0.8rem !important; padding: 12px; text-align: left; border-bottom: 1px solid rgba(0, 229, 255, 0.2); letter-spacing: 1px; }
.stock-table td { padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.95rem; }
.p-up   { color: #FF4B4B !important; font-weight: 900; }
.p-down { color: #4B9EFF !important; font-weight: 900; }
.p-flat { color: #888 !important; }

/* 열기/닫기 버튼 공통 빨간 박스 디자인 */
[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] {
    background-color: #FF4B4B !important; 
    border: 2px solid #FF0000 !important;
    border-radius: 8px !important;
    width: 40px !important; height: 40px !important;
    box-shadow: 0 4px 10px rgba(255, 75, 75, 0.5) !important;
    z-index: 999999 !important;
}
[data-testid="collapsedControl"] *, [data-testid="stSidebarCollapseButton"] * { opacity: 0 !important; font-size: 0 !important; }
"""
