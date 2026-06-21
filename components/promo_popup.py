# -*- coding: utf-8 -*-
"""
시즌 홍보 팝업 (메인 포털 진입 시 1회성 광고 모달)
- assets/season3_promo.jpg 이미지를 풀스크린 오버레이로 표시
- "닫기" / "일주일간 보지 않기" 버튼 제공
- localStorage 기반으로 7일간 재노출 방지 (새로고침/재방문에도 유지)
"""

import base64
import os
import streamlit as st


def _get_promo_image_b64(image_path: str) -> str:
    """이미지를 base64로 인코딩 (세션 내 캐싱)"""
    cache_key = f"_promo_b64_cache::{image_path}"
    if cache_key not in st.session_state:
        with open(image_path, "rb") as f:
            st.session_state[cache_key] = base64.b64encode(f.read()).decode("utf-8")
    return st.session_state[cache_key]


def render_promo_popup(
    image_path: str = "assets/season3_promo.jpg",
    storage_key: str = "hyomin_promo_season3_hide_until",
    hide_days: int = 7,
):
    """
    메인 포털 화면 최상단에서 호출하면 풀스크린 홍보 팝업을 띄운다.
    app.py 의 `if st.session_state.page_view == "portal":` 블록 맨 위,
    PORTAL_CSS 마크다운 호출 직후에 넣는 것을 권장.
    """

    if not os.path.exists(image_path):
        return  # 이미지가 없으면 조용히 스킵 (배포 환경 안전장치)

    img_b64 = _get_promo_image_b64(image_path)

    html = f"""
<style>
#hyomin-promo-overlay {{
    position: fixed;
    inset: 0;
    z-index: 99999;
    background: rgba(5, 8, 20, 0.88);
    backdrop-filter: blur(6px);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: hyomin-promo-fadein 0.35s ease;
    padding: 24px 16px;
}}
@keyframes hyomin-promo-fadein {{
    from {{ opacity: 0; }}
    to   {{ opacity: 1; }}
}}
#hyomin-promo-card {{
    position: relative;
    max-width: 480px;
    width: 100%;
    max-height: 90vh;
    border-radius: 20px;
    overflow: hidden;
    box-shadow:
        0 0 0 1px rgba(108,99,255,0.5),
        0 0 60px rgba(108,99,255,0.45),
        0 20px 60px rgba(0,0,0,0.6);
    background: #05060f;
    display: flex;
    flex-direction: column;
    animation: hyomin-promo-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}}
@keyframes hyomin-promo-pop {{
    from {{ transform: scale(0.92); opacity: 0; }}
    to   {{ transform: scale(1); opacity: 1; }}
}}
#hyomin-promo-scroll {{
    overflow-y: auto;
    max-height: 90vh;
}}
#hyomin-promo-scroll img {{
    display: block;
    width: 100%;
    height: auto;
}}
#hyomin-promo-close-x {{
    position: absolute;
    top: 10px;
    right: 10px;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,255,255,0.25);
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 2;
    transition: background 0.15s, transform 0.15s;
}}
#hyomin-promo-close-x:hover {{
    background: rgba(255,60,60,0.85);
    transform: scale(1.08);
}}
#hyomin-promo-actions {{
    display: flex;
    gap: 0;
    border-top: 1px solid rgba(255,255,255,0.08);
}}
.hyomin-promo-btn {{
    flex: 1;
    padding: 14px 10px;
    text-align: center;
    font-size: 0.85rem;
    font-weight: 700;
    cursor: pointer;
    border: none;
    background: rgba(255,255,255,0.04);
    color: #cbd5e1;
    transition: background 0.15s, color 0.15s;
    font-family: inherit;
}}
.hyomin-promo-btn:hover {{
    background: rgba(255,255,255,0.09);
    color: #fff;
}}
#hyomin-promo-btn-cta {{
    background: linear-gradient(135deg, #6c63ff, #00d4ff);
    color: #fff;
}}
#hyomin-promo-btn-cta:hover {{
    background: linear-gradient(135deg, #7d75ff, #1ae0ff);
    color: #fff;
}}
</style>

<div id="hyomin-promo-overlay">
  <div id="hyomin-promo-card">
    <div id="hyomin-promo-close-x" onclick="window.__hyominPromoClose()">✕</div>
    <div id="hyomin-promo-scroll">
      <img src="data:image/jpeg;base64,{img_b64}" alt="HYOMIN PORTAL 시즌 3 시작" />
    </div>
    <div id="hyomin-promo-actions">
      <button class="hyomin-promo-btn" onclick="window.__hyominPromoHideWeek()">🙈 일주일간 보지 않기</button>
      <button class="hyomin-promo-btn" id="hyomin-promo-btn-cta" onclick="window.__hyominPromoClose()">확인하고 닫기</button>
    </div>
  </div>
</div>

<script>
(function() {{
    var STORAGE_KEY = "{storage_key}";
    var HIDE_DAYS = {hide_days};

    function removeOverlay() {{
        var el = document.getElementById('hyomin-promo-overlay');
        if (el) {{
            el.style.transition = 'opacity 0.2s ease';
            el.style.opacity = '0';
            setTimeout(function() {{ if (el.parentNode) el.parentNode.removeChild(el); }}, 200);
        }}
    }}

    window.__hyominPromoClose = function() {{
        removeOverlay();
    }};

    window.__hyominPromoHideWeek = function() {{
        var until = Date.now() + HIDE_DAYS * 24 * 60 * 60 * 1000;
        try {{
            window.localStorage.setItem(STORAGE_KEY, String(until));
        }} catch (e) {{}}
        removeOverlay();
    }};

    // ESC 키로도 닫기
    document.addEventListener('keydown', function(e) {{
        if (e.key === 'Escape') removeOverlay();
    }}, {{ once: true }});
}})();
</script>
"""

    # localStorage 체크는 JS 실행 시점이 React 컴포넌트(iframe) 내부라 Streamlit과
    # 직접 통신이 어려우므로, "항상 HTML을 그리되 즉시 JS로 노출 여부 판단" 방식 사용.
    # → 차단 기간 내라면 JS가 0ms 안에 오버레이를 숨겨 깜빡임 없이 처리.
    guard_script = f"""
<script>
(function() {{
    var STORAGE_KEY = "{storage_key}";
    var until = 0;
    try {{ until = parseInt(window.localStorage.getItem(STORAGE_KEY) || "0", 10); }} catch (e) {{}}
    if (Date.now() < until) {{
        var style = document.createElement('style');
        style.innerHTML = "#hyomin-promo-overlay{{display:none !important;}}";
        document.head.appendChild(style);
    }}
}})();
</script>
"""

    st.markdown(guard_script + html, unsafe_allow_html=True)
