# pages/sports/soccer_sim.py
import streamlit as st
import random
import time
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import log_tx, atomic_deduct_cash, atomic_add_cash

def render(market, nw):
    st.title("🏆 구단주 시뮬레이터")
    st.markdown("<div style='color:#B0BAC8;margin-bottom:16px;'>베팅 금액을 0원으로 설정하면 <b>'친선 경기(소액 기본 보상)'</b>로 진행됩니다.</div>", unsafe_allow_html=True)

    FORMATION_STATS = {
        "4-4-2 (균형)":     {"atk": 0.30, "def": 0.27, "emoji": "⚖️"},
        "4-3-3 (공격)":     {"atk": 0.42, "def": 0.15, "emoji": "🔥"},
        "3-5-2 (중원장악)": {"atk": 0.27, "def": 0.22, "emoji": "🧠"},
        "5-3-2 (수비철벽)": {"atk": 0.18, "def": 0.38, "emoji": "🛡️"},
        "4-2-3-1 (현대)":   {"atk": 0.33, "def": 0.24, "emoji": "⚡"},
        "3-4-3 (총공격)":   {"atk": 0.48, "def": 0.10, "emoji": "💥"},
    }
    STADIUMS = ["🏟️ 효민 아레나", "⚽ 갤럭시 스타디움", "🌌 유니버스 파크", "🔥 인페르노 필드"]

    c1, c2 = st.columns(2)
    with c1:
        my_team  = st.text_input("내 팀 이름", value="FC 효민")
        my_form  = st.selectbox("포메이션", list(FORMATION_STATS.keys()), key="mf")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[my_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[my_form]['def']*10)}</div>", unsafe_allow_html=True)
    with c2:
        opp_team = st.text_input("상대 팀", value="FC 라이벌")
        opp_form = st.selectbox("상대 포메이션", list(FORMATION_STATS.keys()), key="of")
        st.markdown(f"<div class='card' style='margin-top:8px;padding:12px;text-align:center;'>공격력 {'⚡'*int(FORMATION_STATS[opp_form]['atk']*10)} &nbsp; 수비력 {'🛡️'*int(FORMATION_STATS[opp_form]['def']*10)}</div>", unsafe_allow_html=True)

    stadium = st.selectbox("경기장", STADIUMS)
    
    # 💡 베팅 관련 UI 강화
    betting = st.number_input("경기 베팅금액 (0원 = 친선경기)", min_value=0, step=1_000_000, value=0)
    if betting > 0:
        st.caption(f"💰 승리 시 예상 수령액: {format_korean_money(betting * 2 + 10_000_000)} (원금 포함)")
    else:
        st.caption("🤝 친선 경기 승리 시 기본 보상: 5,000,000원")

    cd_soccer = cooldown_remaining("soccer_game", 10.0)
    if cd_soccer > 0:
        st.warning(f"⏱️ 경기 쿨다운 {cd_soccer:.1f}초 (광클 방지)")
    elif st.button("⚽ 킥오프!", use_container_width=True):
        if betting > 0 and st.session_state.global_cash < betting:
            st.error("베팅 금액이 현재 잔액을 초과합니다!")
        else:
            set_cooldown("soccer_game")

            # ✅ [BUG FIX] 베팅금을 게임 시작 전 atomic_deduct_cash로 선차감
            # 기존: net_profit으로 나중에 한 번에 정산 → 게임 도중 세션이 끊기면 베팅금 미차감
            if betting > 0:
                uid = st.session_state.logged_in_user
                if not atomic_deduct_cash(uid, betting):
                    st.error("잔액 부족! (DB 검증 실패)")
                    st.stop()
                st.session_state.global_cash -= betting
            my_s  = FORMATION_STATS[my_form]
            opp_s = FORMATION_STATS[opp_form]
            h_score = a_score = 0
            scoreboard  = st.empty()
            comm_box    = st.empty()
            prog_bar    = st.progress(0, text="전반전 시작!")
            commentaries = []

            ALL_EVENTS = {
                "my_goal":  ["⚽ 골!!!! {my}의 환상적인 왼발 슈팅!", "⚽ {my} 코너킥 헤더로 득점!", "⚽ {my}의 원더골!"],
                "opp_goal": ["⚽ {opp}이 반격합니다!", "⚽ {opp}의 역습 득점!", "⚽ {opp}이 기습 골!"],
                "my_save":  ["🧤 우리 GK의 슈퍼세이브!", "🛡️ {my} 수비수의 살신성인 태클!"],
                "opp_save": ["🛡️ {opp} GK가 막아냅니다!", "⛔ {opp} 오프사이드!"],
                "neutral":  ["📊 팽팽한 중원 다툼...", "🌟 관중석의 열기!", "⚡ {my} 드리블 돌파!"],
            }
            def pick(key):
                return random.choice(ALL_EVENTS[key]).format(my=my_team[:6], opp=opp_team[:6])

            for minute in range(1, 19):
                time.sleep(0.45)
                real_min = minute * 5
                if real_min == 45:
                    commentaries.insert(0, f"🔔 전반 종료! 스코어: {h_score} : {a_score}")
                if random.random() < my_s['atk']:
                    if random.random() > opp_s['def']:
                        h_score += 1; commentaries.insert(0, f"🕐 {real_min}' | {pick('my_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_save')}")
                if random.random() < opp_s['atk']:
                    if random.random() > my_s['def']:
                        a_score += 1; commentaries.insert(0, f"🕐 {real_min}' | {pick('opp_goal')}")
                    else:
                        commentaries.insert(0, f"🕐 {real_min}' | {pick('my_save')}")
                if random.random() < 0.35:
                    commentaries.insert(0, f"🕐 {real_min}' | {pick('neutral')}")

                scoreboard.markdown(f"""
<div class='scoreboard'>
  <div style='color:#B0BAC8;font-size:0.78rem;letter-spacing:2px;margin-bottom:16px;'>{stadium}</div>
  <div style='display:flex;justify-content:space-around;align-items:center;'>
    <div><div class='team-label'>{my_team}</div><div style='color:#B0BAC8;font-size:0.78rem;'>{my_form}</div></div>
    <div><div class='score-number'>{h_score} : {a_score}</div><div class='match-time'>⏱ {real_min}' / 90'</div></div>
    <div><div class='team-label'>{opp_team}</div><div style='color:#B0BAC8;font-size:0.78rem;'>{opp_form}</div></div>
  </div>
</div>""", unsafe_allow_html=True)
                comm_box.markdown("".join(f"<div class='commentary-item'>{c}</div>" for c in commentaries[:6]), unsafe_allow_html=True)
                prog_bar.progress(minute/18, text=f"{'전반' if real_min<=45 else '후반'} {min(real_min,90)}분")

            prog_bar.progress(1.0, text="⚽ 경기 종료!")
            st.write("---")
            
            # 💡 결과 및 순수익(net_profit) 정산 로직
            # ✅ [BUG FIX] betting은 이미 선차감됨 → 상금(prize)만 지급
            if h_score > a_score:
                st.success(f"🎉 승리! {my_team} {h_score}:{a_score} {opp_team}")
                prize = (10_000_000 + betting * 2) if betting > 0 else 5_000_000
                st.balloons()
            elif h_score == a_score:
                st.warning(f"🤝 무승부! {h_score}:{a_score}")
                prize = (2_000_000 + betting) if betting > 0 else 2_000_000
            else:
                st.error(f"😢 패배... {h_score}:{a_score}")
                prize = 500_000 if betting == 0 else 0

            net_profit = prize - betting  # 표시용 순손익 계산 (betting=0이면 prize=net_profit)
            # ✅ [BUG FIX] atomic_add_cash로 지급 (기존: 세션만 수정 → sync 실패시 미지급)
            if prize > 0:
                atomic_add_cash(st.session_state.logged_in_user, prize)
            st.session_state.global_cash += prize
            
            if net_profit > 0:
                log_tx(st.session_state.logged_in_user, "축구베팅", f"경기 승리 보상", net_profit)
            elif net_profit < 0:
                log_tx(st.session_state.logged_in_user, "축구베팅", f"경기 패배 (베팅금 손실)", net_profit)
            else:
                log_tx(st.session_state.logged_in_user, "축구베팅", f"무승부 (원금 반환)", 0)
                
            sync_user_data()
            
            # 사용자 화면에 최종 정산액 표시
            profit_text = "수익" if net_profit > 0 else "손실" if net_profit < 0 else "변동 없음"
            st.info(f"💰 최종 정산: {format_korean_money(net_profit)} ({profit_text})")
            st.rerun()
