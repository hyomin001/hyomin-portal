# pages/sports/penalty.py
import streamlit as st
import random
from utils.core import format_korean_money, sync_user_data, claim_hidden_title
from utils.database import log_tx

def render(market, nw):
    st.title("⚽ 조기축구 승부차기")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>키커와 골키퍼의 피 말리는 심리전! 5판 3선승제로 승부합니다.</div>", unsafe_allow_html=True)

    if 'ps_state' not in st.session_state:
        st.session_state.update({
            'ps_state': 'betting', 'ps_bet': 0, 'ps_round': 1,
            'ps_turn': 'kicker', 'ps_my_score': 0, 'ps_ai_score': 0, 'ps_logs': []
        })

    state = st.session_state.ps_state

    # ── 베팅 화면 ──
    if state == 'betting':
        st.markdown(f"""
        <div style='text-align:center;padding:30px;background:linear-gradient(135deg,rgba(0,255,136,0.1),rgba(0,100,50,0.15));
             border:2px solid rgba(0,255,136,0.3);border-radius:18px;margin-bottom:24px;'>
          <div style='font-size:4rem;'>🥅</div>
          <div style='font-family:Orbitron,monospace;font-size:1.3rem;color:#00FF88;margin-top:8px;font-weight:900;'>PENALTY SHOOTOUT</div>
          <div style='color:#888;margin-top:10px;font-size:0.88rem;'>승리 시 베팅금의 2배 획득! (무승부 시 원금 반환)</div>
        </div>
        """, unsafe_allow_html=True)
        
        bet = st.number_input("베팅 금액 (원)", min_value=1_000_000, step=1_000_000, value=1_000_000, format="%d", key="ps_bet_input")
        st.caption(f"💵 베팅 예정: {format_korean_money(bet)} | 잔액: {format_korean_money(st.session_state.global_cash)}")
        
        if st.button("⚽ 승부차기 시작!", use_container_width=True):
            if st.session_state.global_cash < bet:
                st.error("잔액이 부족합니다!")
            else:
                st.session_state.global_cash -= bet
                st.session_state.ps_bet = bet
                st.session_state.ps_state = 'playing'
                st.session_state.ps_round = 1
                st.session_state.ps_turn = 'kicker'
                st.session_state.ps_my_score = 0
                st.session_state.ps_ai_score = 0
                st.session_state.ps_logs = []
                sync_user_data()
                st.rerun()

    # ── 플레이 및 결과 화면 ──
    elif state in ['playing', 'done']:
        my_score, ai_score = st.session_state.ps_my_score, st.session_state.ps_ai_score
        current_round = st.session_state.ps_round
        turn, logs = st.session_state.ps_turn, st.session_state.ps_logs

        st.markdown(f"""
        <div class='scoreboard'>
          <div style='color:#777;font-size:0.9rem;letter-spacing:2px;margin-bottom:12px;'>🏆 조기축구 결승전 승부차기</div>
          <div style='display:flex;justify-content:space-around;align-items:center;'>
            <div><div class='team-label'>{st.session_state.logged_in_user} (나)</div></div>
            <div>
              <div class='score-number' style='color:#FFD600;'>{my_score} : {ai_score}</div>
              <div class='match-time'>Round {min(current_round, 5)} / 5</div>
            </div>
            <div><div class='team-label'>동네 라이벌 (AI)</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")

        if state == 'playing':
            if turn == 'kicker':
                st.markdown("<h3 style='text-align:center; color:#FF4B4B;'>🔥 당신은 키커입니다! 슛 방향을 선택하세요!</h3>", unsafe_allow_html=True)
                btn_labels = ["◀️ 좌측으로 슛", "⏺️ 중앙 꽂기", "▶️ 우측으로 슛"]
            else:
                st.markdown("<h3 style='text-align:center; color:#4B9EFF;'>🧤 당신은 골키퍼입니다! 다이빙 방향을 예측하세요!</h3>", unsafe_allow_html=True)
                btn_labels = ["◀️ 좌측 다이빙", "⏺️ 중앙 대기", "▶️ 우측 다이빙"]

            dirs = ["Left", "Center", "Right"]
            c1, c2, c3 = st.columns(3)
            
            def process_turn(my_choice):
                ai_choice = random.choice(dirs)
                if turn == 'kicker':
                    if my_choice != ai_choice:
                        st.session_state.ps_my_score += 1
                        logs.insert(0, f"✅ [Round {current_round}] <b>나(공격)</b>: {my_choice} 슛! / AI(수비): {ai_choice} 다이빙 ➔ <span style='color:#00FF88;'>GOAL!! ⚽</span>")
                    else:
                        logs.insert(0, f"❌ [Round {current_round}] <b>나(공격)</b>: {my_choice} 슛! / AI(수비): {ai_choice} 다이빙 ➔ <span style='color:#FF4B4B;'>막혔습니다!! 🧤</span>")
                    st.session_state.ps_turn = 'keeper'
                else:
                    if my_choice == ai_choice:
                        logs.insert(0, f"✅ [Round {current_round}] AI(공격): {ai_choice} 슛! / <b>나(수비)</b>: {my_choice} 다이빙 ➔ <span style='color:#00FF88;'>슈퍼 세이브!! 🧤</span>")
                    else:
                        st.session_state.ps_ai_score += 1
                        logs.insert(0, f"❌ [Round {current_round}] AI(공격): {ai_choice} 슛! / <b>나(수비)</b>: {my_choice} 다이빙 ➔ <span style='color:#FF4B4B;'>실점했습니다... ⚽</span>")
                    st.session_state.ps_turn = 'kicker'
                    st.session_state.ps_round += 1

                if st.session_state.ps_round > 5:
                    st.session_state.ps_state = 'done'

            if c1.button(btn_labels[0], use_container_width=True): process_turn("Left"); st.rerun()
            if c2.button(btn_labels[1], use_container_width=True): process_turn("Center"); st.rerun()
            if c3.button(btn_labels[2], use_container_width=True): process_turn("Right"); st.rerun()

        else:
            bet = st.session_state.ps_bet
            if my_score > ai_score:
                result_txt, result_col, prize = "🎉 승리! 상금을 획득합니다!", "#00FF88", bet * 2
            elif my_score == ai_score:
                result_txt, result_col, prize = "🤝 치열한 접전 끝 무승부! 원금 반환", "#888888", bet
            else:
                result_txt, result_col, prize = "😢 패배... 베팅금을 잃었습니다.", "#FF4B4B", 0

            net = prize - bet
            net_str = f"+{format_korean_money(net)}" if net > 0 else f"-{format_korean_money(abs(net))}" if net < 0 else "베팅금 반환"
            
            st.markdown(f"""
            <div style='text-align:center;background:rgba(0,0,0,0.4);border:2px solid {result_col};
                 border-radius:18px;padding:28px;margin:20px 0;box-shadow:0 0 30px {result_col}44;'>
              <div style='font-size:1.8rem;font-weight:900;color:{result_col};'>{result_txt}</div>
              <div style='font-size:1.3rem;font-weight:900;margin-top:10px;'>{net_str}</div>
              <div style='color:#888;font-size:0.8rem;margin-top:8px;'>지급액: {format_korean_money(prize)}</div>
            </div>
            """, unsafe_allow_html=True)

            if 'ps_paid' not in st.session_state:
                st.session_state.ps_paid = True
                if prize > 0:
                    st.session_state.global_cash += prize
                    if bet >= 10_000_000_000: claim_hidden_title("penalty_master", "👑 [유일무이] 거미손")
                if net > 0: log_tx(st.session_state.logged_in_user, "승부차기", "승부차기 승리", net)
                elif net < 0: log_tx(st.session_state.logged_in_user, "승부차기", "승부차기 패배", net)
                sync_user_data()

            if st.button("🔄 다시 하기", use_container_width=True):
                for k in ['ps_state','ps_bet','ps_round','ps_turn','ps_my_score','ps_ai_score','ps_logs','ps_paid']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()

        if logs:
            st.write("---")
            st.markdown("#### 📡 실시간 중계 기록")
            for log in logs: st.markdown(f"<div class='commentary-item'>{log}</div>", unsafe_allow_html=True)