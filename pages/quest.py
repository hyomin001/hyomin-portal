# pages/quest.py
import streamlit as st
from datetime import datetime
from utils.config import DAILY_QUESTS_CONFIG, KST, stock_config
from utils.core import format_korean_money, sync_user_data
from utils.database import log_tx, atomic_add_cash

def check_quest(qid, nw, st_session, market):
    if qid == "attendance": return True
    elif qid == "rich5": return nw >= 500_000_000
    elif qid == "landlord": return any(v > 0 for v in (st_session.real_estate or {}).values())
    elif qid == "debtfree": return st_session.loan == 0
    elif qid == "investor":
        stock_data = market.get('stock_data', {})
        return sum(st_session.portfolio.get(s['id'], {}).get('qty', 0) * stock_data.get(s['id'], {}).get('price', 0) for s in stock_config) >= 100_000_000
    elif qid == "coin100m":
        if 'crypto_data' not in market: return False
        crypto_data = market['crypto_data']
        return sum(ci.get('qty', 0) * crypto_data.get(cid, {}).get('price', 0) for cid, ci in st_session.get('crypto_portfolio', {}).items()) >= 100_000_000
    elif qid == "billionaire": return nw >= 100_000_000_000
    return False

def get_progress_hint(qid, nw, st_session, market):
    if qid == "rich5":      return f"현재 순자산: {format_korean_money(nw)} / 5억"
    elif qid == "landlord": return f"보유 부동산: {sum(v for v in st_session.real_estate.values())}채 / 1채"
    elif qid == "investor":
        stock_data = market.get('stock_data', {})
        sv = sum(st_session.portfolio.get(s['id'], {}).get('qty', 0) * stock_data.get(s['id'], {}).get('price', 0) for s in stock_config)
        return f"주식 평가액: {format_korean_money(int(sv))} / 1억"
    elif qid == "coin100m":
        cv = sum(ci.get('qty',0) * market['crypto_data'].get(cid,{}).get('price',0) for cid, ci in st_session.get('crypto_portfolio',{}).items()) if 'crypto_data' in market else 0
        return f"코인 평가액: {format_korean_money(int(cv))} / 1억"
    elif qid == "debtfree": return f"현재 대출: {format_korean_money(st_session.loan)}"
    elif qid == "billionaire": return f"현재 순자산: {format_korean_money(nw)} / 1000억"
    return ""

def render(market, nw):
    st.title("📅 일일 퀘스트")
    st.markdown("<div style='color:#94A3B8;margin-bottom:20px;'>매일 자정에 초기화됩니다. 달성하고 보상을 수령하세요!</div>", unsafe_allow_html=True)
    
    today_str = datetime.now(KST).strftime("%Y-%m-%d")
    dq = st.session_state.get('daily_quests', {})
    today_dq = dq.get(today_str, {})
    
    for q in DAILY_QUESTS_CONFIG:
        is_claimed    = today_dq.get(q['id'], False)
        is_achievable = check_quest(q['id'], nw, st.session_state, market)
        hint = get_progress_hint(q['id'], nw, st.session_state, market)
        
        status_col = "#00FF88" if is_claimed else "#FFD600" if is_achievable else "#444"
        status_txt = "✅ 수령 완료" if is_claimed else "🟡 달성! 클릭하여 수령" if is_achievable else f"🔒 미달성 ({hint})" if hint else "🔒 미달성"
        
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.05); border-left:4px solid {status_col}; padding:15px; border-radius:8px; margin-bottom:10px;'>
            <div style='display:flex; justify-content:space-between; align-items:center;'>
                <div>
                    <span style='font-size:1.5rem;'>{q['icon']}</span> <b style='font-size:1.1rem; color:#E2E8F0;'>{q['name']}</b>
                    <div style='color:#94A3B8; font-size:0.85rem; margin-top:4px;'>{q['desc']}</div>
                </div>
                <div style='text-align:right;'>
                    <div style='color:#FFD600; font-weight:900;'>{format_korean_money(q['reward'])}</div>
                    <div style='color:{status_col}; font-size:0.8rem; margin-top:4px;'>{status_txt}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if is_achievable and not is_claimed:
            if st.button(f"[{q['name']}] 보상 수령", key=f"q_btn_{q['id']}"):
                # ✅ [BUG FIX] 퀘스트 완료 플래그를 먼저 세션에 기록한 후 atomic_add_cash 지급
                # 기존: 세션 cash만 올리고 sync_user_data() → 리로드 전 버튼 중복 클릭 시 이중 지급
                today_dq[q['id']] = True
                dq[today_str] = today_dq
                st.session_state.daily_quests = dq
                atomic_add_cash(st.session_state.logged_in_user, q['reward'])
                st.session_state.global_cash += q['reward']
                log_tx(st.session_state.logged_in_user, "퀘스트", f"{q['name']} 완료", q['reward'])
                sync_user_data()
                st.toast(f"🎉 {q['name']} 완료! +{format_korean_money(q['reward'])}", icon="🎁")
                st.balloons()
                st.rerun()
