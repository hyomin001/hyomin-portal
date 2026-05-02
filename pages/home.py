# pages/home.py
import streamlit as st
import time
from utils.config import estate_config, stock_config
from utils.core import format_korean_money

def render(market, nw):

    st.title("🌌 HYOMIN UNIVERSE")

    # 1. 게임 캐릭터 프로필 느낌의 UI
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #111128, #0a0a20); border: 2px solid #00E5FF; border-radius: 15px; padding: 20px; display: flex; align-items: center; gap: 20px; margin-bottom: 25px; box-shadow: 0 0 20px rgba(0, 229, 255, 0.2);'>
        <div style='font-size: 4rem; background: rgba(255,255,255,0.05); padding: 10px; border-radius: 50%;'>🧑‍🚀</div>
        <div style='flex: 1;'>
            <div style='color:#00FF88; font-weight:900; font-size:1.1rem; margin-bottom:5px;'>{st.session_state.equipped_title}</div>
            <div style='font-size: 2rem; font-family: "Orbitron", monospace; font-weight: 900; color: #fff; line-height: 1.2;'>{st.session_state.logged_in_user}</div>
            <div style='color:#888; font-size:0.9rem; margin-top:5px;'>환영합니다! 우주에서의 새로운 하루가 시작되었습니다.</div>
        </div>
        <div style='text-align: right; border-left: 1px solid rgba(0,229,255,0.3); padding-left: 20px;'>
            <div style='color:#94A3B8; font-size:0.9rem;'>보유 현금</div>
            <div style='font-size:1.8rem; font-weight:900; color:#FFD600;'>{format_korean_money(st.session_state.global_cash)}</div>
            <div style='color:#94A3B8; font-size:0.9rem; margin-top:10px;'>총 순자산</div>
            <div style='font-size:1.3rem; font-weight:900; color:#E2E8F0;'>{format_korean_money(nw)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 🗺️ 성장 단계별 맞춤형 퀘스트 보드
    st.markdown("### 🗺️ 현재 성장 목표")
    
    if nw < 500_000_000:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(0, 229, 255, 0.1), rgba(0, 102, 255, 0.1)); border: 1px solid #00E5FF; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#00E5FF; margin-top:0;'>🌱 튜토리얼 1단계: 흙수저 탈출 작전</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>초기 시드머니를 모아야 합니다. 광산에서 노가다를 하거나 일일 퀘스트를 완료하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>다음 목표: 순자산 5억 달성</div>
        </div>
        """, unsafe_allow_html=True)
        col_q1, col_q2 = st.columns(2)
        if col_q1.button("⛏️ 광산으로 돈 벌러 가기", use_container_width=True):
            st.session_state.current_category = "🎮 미니게임"
            st.session_state.current_page = "⛏️ 광산 (노가다)"
            st.rerun()
        if col_q2.button("📅 일일 퀘스트 보상받기", use_container_width=True):
            st.session_state.current_category = "🌟 성장 & 혜택"
            st.session_state.current_page = "📅 일일 퀘스트"
            st.rerun()
            
    elif nw < 10_000_000_000:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 214, 0, 0.1), rgba(255, 100, 0, 0.1)); border: 1px solid #FFD600; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#FFD600; margin-top:0;'>🏢 튜토리얼 2단계: 자본가의 길</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>이제 돈이 돈을 벌게 해야 합니다. 주식과 코인에 투자하고 첫 부동산을 매입하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>다음 목표: 순자산 100억 달성 (건물주)</div>
        </div>
        """, unsafe_allow_html=True)
        col_q1, col_q2, col_q3 = st.columns(3)
        if col_q1.button("📈 주식 시장 보기", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "📈 주식 트레이딩"
            st.rerun()
        if col_q2.button("🪙 코인 거래소 이동", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "🪙 코인 거래소"
            st.rerun()
        if col_q3.button("🏢 첫 부동산 매입", use_container_width=True):
            st.session_state.current_category = "📈 경제"
            st.session_state.current_page = "🏢 부동산 거래소"
            st.rerun()
            
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, rgba(255, 0, 255, 0.1), rgba(100, 0, 255, 0.1)); border: 1px solid #FF00FF; border-radius: 12px; padding: 20px; margin-bottom: 20px;'>
            <h4 style='color:#FF00FF; margin-top:0;'>👑 튜토리얼 완료: 우주 억만장자</h4>
            <p style='color:#A0AEC0; font-size:0.9rem;'>당신은 이미 훌륭한 자본가입니다. 이제 서버 랭킹 1위를 향해 명검을 벼리고 하이퍼카를 수집하세요!</p>
            <div style='margin-top: 10px; font-weight: 700; color: #FFF;'>최종 목표: 서버 랭킹 1위 달성</div>
        </div>
        """, unsafe_allow_html=True)
        col_q1, col_q2 = st.columns(2)
        if col_q1.button("🗡️ 명검 강화하러 가기", use_container_width=True):
            st.session_state.current_category = "🎮 미니게임"
            st.session_state.current_page = "🗡️ 전설의 명검 강화"
            st.rerun()
        if col_q2.button("🏎️ 하이퍼카 차고지 가기", use_container_width=True):
            st.session_state.current_category = "⚽ 스포츠"
            st.session_state.current_page = "🛠️ 커스텀 튜닝 차고지"
            st.rerun()

    st.write("---")

    # 3. 자산 상태 요약
    c3, c4 = st.columns(2)
    with c3:
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='color:#888; font-size:0.9rem;'>💳 갚아야 할 대출금</div>
            <div style='color:#FF4B4B; font-size:1.5rem; font-weight:900;'>{format_korean_money(st.session_state.loan)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        cur_t = time.time()
        _capped_pass = min(int(cur_t - st.session_state.rent_time), 86400)
        total_rent_pending = sum(
            estate_config[eid]['income'] * cnt * _capped_pass
            for eid, cnt in st.session_state.real_estate.items() if eid in estate_config
        )
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='color:#888; font-size:0.9rem;'>🏢 수금 대기 중인 임대료</div>
            <div style='color:#00FF88; font-size:1.5rem; font-weight:900;'>{format_korean_money(total_rent_pending)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # 🔑 비밀번호 변경
    st.markdown("### 🔑 비밀번호 변경")
    with st.expander("비밀번호 변경하기"):
        cur_pw  = st.text_input("현재 비밀번호", type="password", key="chpw_cur")
        new_pw1 = st.text_input("새 비밀번호",   type="password", key="chpw_new1")
        new_pw2 = st.text_input("새 비밀번호 확인", type="password", key="chpw_new2")
        if st.button("✅ 변경하기", key="chpw_btn"):
            from utils.core import verify_pw, hash_pw_bcrypt
            from utils.database import load_db, save_db
            from utils.config import USERS_FILE
            uid   = st.session_state.logged_in_user
            users = load_db(USERS_FILE, {})
            if not verify_pw(cur_pw, users[uid]['pw']):
                st.error("❌ 현재 비밀번호가 틀렸습니다.")
            elif len(new_pw1) < 1:
                st.error("❌ 새 비밀번호를 입력해주세요.")
            elif new_pw1 != new_pw2:
                st.error("❌ 새 비밀번호가 일치하지 않습니다.")
            else:
                users[uid]['pw'] = hash_pw_bcrypt(new_pw1)
                save_db(USERS_FILE, users)
                st.success("✅ 비밀번호가 변경되었습니다!")

    st.write("---")

    # 4. 주식 핫 종목
    st.markdown("### 📈 실시간 시장 현황")
    top_stocks = sorted(stock_config, key=lambda s: (
        (market['stock_data'][s['id']]['history'][-1] - market['stock_data'][s['id']]['history'][-2])
        / market['stock_data'][s['id']]['history'][-2]
        if len(market['stock_data'][s['id']]['history']) > 1 else 0
    ), reverse=True)[:5]

    cols = st.columns(5)
    for i, s in enumerate(top_stocks):
        d    = market['stock_data'][s['id']]
        diff = (d['history'][-1] - d['history'][-2]) / d['history'][-2] * 100 if len(d['history']) > 1 else 0
        arrow, clr = ("▲", "#FF4B4B") if diff >= 0 else ("▼", "#4B9EFF")
        with cols[i]:
            st.markdown(f"""
<div class='card' style='text-align:center;padding:14px;'>
  <div style='font-size:1.4rem;'>{s['icon']}</div>
  <div style='font-size:0.78rem;color:#888;margin:4px 0;'>{d['name'][:6]}</div>
  <div style='font-size:1rem;font-weight:900;color:#E2E8F0;'>₩{d['price']:,}</div>
  <div style='font-size:0.85rem;color:{clr};font-weight:900;'>{arrow} {abs(diff):.2f}%</div>
</div>""", unsafe_allow_html=True)
