# pages/vip.py
import streamlit as st
import random
from utils.config import stock_config, estate_config
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import load_db, log_tx, USERS_FILE

def render(market, nw):
    st.title("💎 VIP 시크릿 라운지")
    nxt_id  = market['next_news_target']
    nxt_nm  = next((s['name'] for s in stock_config if s['id'] == nxt_id), nxt_id)
    nxt_ico = next((s['icon'] for s in stock_config if s['id'] == nxt_id), "")
    imp_raw = market['next_news_impact']
    
    if imp_raw > 0.1:   status, clr = "🚀 강력한 호재 예정!", "#FF4B4B"
    elif imp_raw > 0:   status, clr = "📈 소폭 상승 예상",   "#FF8800"
    elif imp_raw > -0.1:status, clr = "📉 소폭 조정 예상",   "#4B9EFF"
    else:               status, clr = "💣 큰 악재 임박!",    "#8800FF"

    st.markdown(f"""
<div class='vip-banner'>
  <div style='color:#888;font-size:0.8rem;letter-spacing:2px;margin-bottom:12px;'>🕵️ INSIDER INTELLIGENCE</div>
  <div style='font-size:1.4rem;font-weight:900;color:#FFD600;'>{nxt_ico} {nxt_nm}</div>
  <div style='font-size:1.1rem;font-weight:900;color:{clr};margin-top:10px;'>{status}</div>
  <div style='color:#888;font-size:0.78rem;margin-top:14px;'>※ 정보 유출 시 창조주의 징벌이 따릅니다</div>
</div>""", unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🎰 VIP 전용 슬롯 (1억, 승률 50%)")
        cd_rem = cooldown_remaining("vip_slot", 5.0)
        if cd_rem > 0:
            st.warning(f"⏱️ 쿨다운 중... {cd_rem:.1f}초")
        elif st.button("💎 VIP 슬롯 당기기", use_container_width=True):
            if st.session_state.global_cash >= 100_000_000:
                u_db_check = load_db(USERS_FILE, {})
                db_cash = u_db_check.get(st.session_state.logged_in_user, {}).get('cash', 0)
                if db_cash < 100_000_000:
                    st.error("잔액 부족! (DB 검증 실패)")
                else:
                    set_cooldown("vip_slot")
                    st.session_state.global_cash -= 100_000_000
                    if random.random() < 0.5:
                        st.session_state.global_cash += 250_000_000
                        st.success("🎉 승리! +2.5억 획득!")
                        log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 승리", 150_000_000)
                    else:
                        st.error("❌ 아쉽습니다. 다음 기회를!")
                        log_tx(st.session_state.logged_in_user, "VIP슬롯", "VIP 슬롯 패배", -100_000_000)
                    sync_user_data(); st.rerun()
            else:
                st.error("잔액 부족!")
    with c2:
        st.markdown("### 📊 VIP 포트폴리오 요약")
        total_stock  = sum(st.session_state.portfolio.get(s['id'], {}).get('qty', 0) * market['stock_data'][s['id']]['price'] for s in stock_config)
        total_estate = sum(estate_config[eid]['base_price'] * cnt * 0.8 for eid, cnt in st.session_state.real_estate.items() if eid in estate_config)
        st.metric("주식 평가액",   format_korean_money(total_stock))
        st.metric("부동산 평가액", format_korean_money(total_estate))
        st.metric("총 순자산",     format_korean_money(nw))