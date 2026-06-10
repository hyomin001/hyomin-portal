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


/* 탭 버튼 가시성 */
[data-testid="stTabs"] [data-baseweb="tab"] {
  color: #94A3B8 !important;
  font-weight: 600 !important;
  font-size: 0.95rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
  color: #00E5FF !important;
  font-weight: 700 !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background-color: #00E5FF !important;
}
[data-testid="stTabs"] [data-baseweb="tab-border"] {
  background-color: rgba(255,255,255,0.1) !important;
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
.stock-table td { padding: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); font-size: 0.95rem; color: #E2E8F0 !important; }
.stock-table tr { background: transparent !important; }
.stock-table tr:hover { background: rgba(0, 229, 255, 0.04) !important; }
.stock-table { background: transparent !important; }
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

/* 메인 컨텐츠 영역만 전역 흰 글씨 - 사이드바 제외 */
[data-testid="stMain"] div,
[data-testid="stMain"] span,
[data-testid="stMain"] p,
[data-testid="stMain"] li,
[data-testid="stMain"] td,
[data-testid="stMain"] th,
[data-testid="stMain"] small,
[data-testid="stMain"] strong,
[data-testid="stMain"] b,
[data-testid="stMain"] em {
  color: #E2E8F0;
}

/* 드롭다운/팝업은 흰 배경이라 검은 글씨 유지 */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div,
[data-baseweb="popover"] span,
[data-baseweb="popover"] div,
[role="listbox"] span,
[role="listbox"] div,
[role="listbox"] li,
[data-baseweb="menu"] span,
[data-baseweb="menu"] div,
[data-baseweb="menu"] li {
  color: #000000 !important;
}

/* 버튼 색상 유지 - 내부 span/div 포함 */
.stButton > button,
.stButton > button span,
.stButton > button div,
.stButton > button p {
  color: #00E5FF !important;
}
.stButton > button:hover,
.stButton > button:hover span,
.stButton > button:hover div,
.stButton > button:hover p {
  color: #000000 !important;
}

/* 스포츠 스코어보드 */
.scoreboard { background:rgba(10,14,26,0.85); border:1px solid rgba(0,229,255,0.25); border-radius:16px; padding:24px 32px; text-align:center; margin:12px 0; }
.team-label { font-family:'Orbitron',sans-serif !important; font-size:1.1rem !important; font-weight:900 !important; color:#E2E8F0 !important; }
.score-number { font-family:'Orbitron',sans-serif !important; font-size:2.8rem !important; font-weight:900 !important; color:#FFD600 !important; }
.match-time { font-size:0.85rem !important; color:#94A3B8 !important; }
.commentary-item { border-left:3px solid rgba(0,229,255,0.4); border-radius:0 8px 8px 0; padding:8px 14px; margin:4px 0; color:#CBD5E1 !important; }
.card { color: #E2E8F0 !important; }

/* =======================================================
   📱 모바일 반응형 (768px 이하)
   PC는 기존 레이아웃 그대로, 모바일만 적용됨
======================================================== */
@media (max-width: 768px) {

  /* ── 1. 가로 삐져나옴 완전 차단 ── */
  html, body {
    overflow-x: hidden !important;
    width: 100% !important;
  }
  [data-testid="stAppViewContainer"],
  [data-testid="stMain"],
  [data-testid="stVerticalBlock"] {
    overflow-x: hidden !important;
    max-width: 100vw !important;
  }

  /* ── 2. 전체 여백 축소 ── */
  .block-container {
    padding-left: 10px !important;
    padding-right: 10px !important;
    padding-top: 10px !important;
    max-width: 100% !important;
  }

  /* ── 3. 컬럼 gap 축소 ── */
  [data-testid="stHorizontalBlock"] {
    flex-wrap: wrap !important;
    gap: 6px !important;
  }

  /* ── 4. 기본: 모든 컬럼 100% 너비로 세로 쌓기 ── */
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    min-width: 100% !important;
    width: 100% !important;
    flex: 1 1 100% !important;
  }

  /* ── 5. 예외: 2칸짜리만 나란히 (버튼 쌍, 간단한 입력폼 등) ── */
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(2):last-child) > [data-testid="stColumn"] {
    min-width: calc(50% - 4px) !important;
    flex: 1 1 calc(50% - 4px) !important;
  }

  /* ── 6. iframe (components.html 게임/프로필 카드) 너비 맞춤 ── */
  iframe {
    max-width: 100% !important;
    width: 100% !important;
  }

  /* ── 7. 인라인 flex 컨테이너 줄바꿈 허용 ── */
  [data-testid="stMain"] div[style*="display:flex"],
  [data-testid="stMain"] div[style*="display: flex"] {
    flex-wrap: wrap !important;
  }

  /* ── 8. 홈 상단 프로필 카드 세로 정렬 ── */
  [data-testid="stMain"] div[style*="display: flex"][style*="gap: 20px"] {
    flex-direction: column !important;
    align-items: center !important;
  }
  [data-testid="stMain"] div[style*="border-left: 1px solid"] {
    border-left: none !important;
    border-top: 1px solid rgba(0,229,255,0.3) !important;
    padding-left: 0 !important;
    padding-top: 12px !important;
    text-align: center !important;
    width: 100% !important;
  }

  /* ── 9. 테이블 가로 스크롤 허용 ── */
  .stock-table {
    display: block !important;
    overflow-x: auto !important;
    -webkit-overflow-scrolling: touch !important;
    font-size: 0.8rem !important;
  }
  .stock-table th, .stock-table td {
    padding: 8px 6px !important;
    white-space: nowrap !important;
  }

  /* ── 10. 폰트 크기 조정 ── */
  h1 { font-size: 1.3rem !important; }
  h2 { font-size: 1.1rem !important; }
  h3 { font-size: 1rem !important; }
  .score-number { font-size: 2rem !important; }

  /* ── 11. 버튼 ── */
  .stButton > button {
    height: 46px !important;
    font-size: 0.88rem !important;
    padding: 0 8px !important;
  }

  /* ── 12. 카드 패딩 축소 ── */
  .card { padding: 12px !important; }

  /* ── 13. 사이드바 너비 ── */
  [data-testid="stSidebar"] {
    width: 82vw !important;
    min-width: unset !important;
  }

  /* ── 14. 탭 글씨 ── */
  [data-testid="stTabs"] [data-baseweb="tab"] {
    font-size: 0.78rem !important;
    padding: 8px 8px !important;
  }

  /* ── 15. 숫자 입력 등 입력창 전체 너비 ── */
  .stTextInput, .stNumberInput, .stSelectbox {
    width: 100% !important;
  }
}

/* ── 초소형 화면 (360px 이하, 갤럭시 폴드 등) ── */
@media (max-width: 380px) {
  .block-container {
    padding-left: 6px !important;
    padding-right: 6px !important;
  }
  [data-testid="stHorizontalBlock"]:has(> [data-testid="stColumn"]:nth-child(2):last-child) > [data-testid="stColumn"] {
    min-width: 100% !important;
    flex: 1 1 100% !important;
  }
  h1 { font-size: 1.1rem !important; }
}
"""
