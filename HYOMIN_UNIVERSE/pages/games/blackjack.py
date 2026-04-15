# pages/games/blackjack.py
import streamlit as st
import random
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import log_tx

def render(market, nw):
    st.title("🃏 블랙잭 카지노")

    CARD_VALS = {'A':11,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10,'Q':10,'K':10}
    SUITS = ['♠','♥','♦','♣']

    def bj_make_deck():
        deck = [(rank, suit) for rank in CARD_VALS for suit in SUITS] * 6
        random.shuffle(deck)
        return deck

    def bj_value(hand):
        val  = sum(CARD_VALS[r] for r, s in hand)
        aces = sum(1 for r, s in hand if r == 'A')
        while val > 21 and aces:
            val -= 10; aces -= 1
        return val

    def bj_render(hand, hide_second=False):
        parts = []
        for i, (r, s) in enumerate(hand):
            if i == 1 and hide_second:
                parts.append("<span style='font-size:2.2rem;background:#222;border:2px solid #555;padding:6px 10px;border-radius:8px;margin:3px;display:inline-block;'>🂠</span>")
            else:
                col = "color:#FF4B4B;" if s in ['♥','♦'] else "color:#1a1a1a;"
                parts.append(f"<span style='font-size:1.5rem;font-weight:900;background:#fff;{col}padding:6px 12px;border-radius:8px;margin:3px;display:inline-block;box-shadow:0 2px 8px rgba(0,0,0,0.4);'>{r}{s}</span>")
        return " ".join(parts)

    def bj_dealer_play(dealer, deck):
        while bj_value(dealer) < 17:
            dealer.append(deck.pop())
        return dealer, deck

    if 'bj_state' not in st.session_state:
        st.session_state.update({
            'bj_state': 'betting', 'bj_deck': bj_make_deck(),
            'bj_player': [], 'bj_dealer': [], 'bj_bet': 0, 
        })

    state = st.session_state.bj_state

    # ── 베팅 화면 ──
    if state == 'betting':
        st.markdown(f"""
        <div style='text-align:center;padding:30px;background:linear-gradient(135deg,rgba(180,0,0,0.15),rgba(0,100,0,0.15));
             border:2px solid rgba(255,215,0,0.3);border-radius:18px;margin-bottom:24px;'>
          <div style='font-size:4rem;'>🃏</div>
          <div style='font-family:Orbitron,monospace;font-size:1.3rem;color:#FFD600;margin-top:8px;font-weight:900;'>BLACKJACK</div>
          <div style='color:#888;margin-top:10px;font-size:0.88rem;'>블랙잭(A+10) = 베팅의 1.5배 추가 지급 &nbsp;|&nbsp; 딜러 16 이하 히트</div>
        </div>
        """, unsafe_allow_html=True)
        
        bet = st.number_input("베팅 금액 (원)", min_value=1_000_000, step=1_000_000, value=1_000_000, format="%d", key="bj_bet_input")
        st.caption(f"💵 베팅 예정: {format_korean_money(bet)} | 잔액: {format_korean_money(st.session_state.global_cash)}")
        
        cd_deal = cooldown_remaining("bj_deal", 1.0)
        if cd_deal > 0:
            st.warning(f"⏱️ {cd_deal:.1f}초 후 딜 가능")
        elif st.button("🃏 카드 딜!", use_container_width=True):
            if st.session_state.global_cash < bet:
                st.error("잔액 부족!")
            else:
                set_cooldown("bj_deal")
                st.session_state.global_cash -= bet
                st.session_state.bj_bet = bet
                deck = st.session_state.bj_deck if len(st.session_state.bj_deck) > 30 else bj_make_deck()
                player = [deck.pop(), deck.pop()]
                dealer = [deck.pop(), deck.pop()]
                st.session_state.bj_player = player
                st.session_state.bj_dealer = dealer
                st.session_state.bj_deck   = deck
                
                if bj_value(player) == 21:
                    dl, dk = bj_dealer_play(dealer, deck)
                    st.session_state.bj_dealer = dl
                    st.session_state.bj_deck   = dk
                    st.session_state.bj_state  = 'done'
                else:
                    st.session_state.bj_state  = 'playing'
                sync_user_data()
                st.rerun()

    # ── 플레이 및 결과 화면 ──
    elif state in ['playing', 'done']:
        player = st.session_state.bj_player
        dealer = st.session_state.bj_dealer
        bet    = st.session_state.bj_bet
        pval   = bj_value(player)

        st.markdown("### 🎩 딜러의 패")
        if state == 'playing':
            dv_shown = bj_value([dealer[0]])
            st.markdown(f"{bj_render(dealer, hide_second=True)}", unsafe_allow_html=True)
            st.caption(f"딜러 공개 패: {dv_shown}점 + ?")
        else:
            dval = bj_value(dealer)
            dcol = "#FF4B4B" if dval > 21 else "#fff"
            st.markdown(f"{bj_render(dealer)} <span style='color:{dcol};font-size:1.1rem;font-weight:900;margin-left:12px;'>{dval}점{'  💥BUST' if dval>21 else ''}</span>", unsafe_allow_html=True)
        st.write("")

        st.markdown("### 🎴 내 패")
        pcol = "#FF4B4B" if pval > 21 else "#00FF88" if pval == 21 else "#fff"
        st.markdown(f"{bj_render(player)} <span style='color:{pcol};font-size:1.2rem;font-weight:900;margin-left:12px;'>{pval}점{'  💥BUST' if pval>21 else '  🃏BJ!' if pval==21 and len(player)==2 else ''}</span>", unsafe_allow_html=True)
        st.write("")

        c_bet, c_pot = st.columns(2)
        c_bet.metric("💰 베팅", format_korean_money(bet))
        c_pot.metric("🏆 승리 시 지급", format_korean_money(bet * 2))

        if state == 'playing':
            st.write("")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("👊 히트 (Hit)", use_container_width=True):
                    deck = st.session_state.bj_deck
                    st.session_state.bj_player.append(deck.pop())
                    st.session_state.bj_deck = deck
                    new_val = bj_value(st.session_state.bj_player)
                    if new_val >= 21:
                        dl, dk = bj_dealer_play(st.session_state.bj_dealer, st.session_state.bj_deck)
                        st.session_state.bj_dealer = dl
                        st.session_state.bj_deck   = dk
                        st.session_state.bj_state  = 'done'
                    st.rerun()
            with c2:
                if st.button("🛑 스탠드 (Stand)", use_container_width=True):
                    dl, dk = bj_dealer_play(st.session_state.bj_dealer, st.session_state.bj_deck)
                    st.session_state.bj_dealer = dl
                    st.session_state.bj_deck   = dk
                    st.session_state.bj_state  = 'done'
                    st.rerun()

        else:
            pval_f = bj_value(player)
            dval_f = bj_value(dealer)
            bet_f  = st.session_state.bj_bet
            is_bj  = (pval_f == 21 and len(player) == 2)
            
            if pval_f > 21:
                result, res_col, prize = "💥 버스트! 패배", "#4B9EFF", 0
            elif dval_f > 21:
                result, res_col, prize = "🎉 딜러 버스트! 승리!", "#FF4B4B", bet_f * 2
            elif is_bj and dval_f != 21:
                result, res_col, prize = "🃏 블랙잭!! 1.5배!", "#FFD600", int(bet_f * 2.5)
            elif pval_f > dval_f:
                result, res_col, prize = "🎉 승리!", "#00FF88", bet_f * 2
            elif pval_f == dval_f:
                result, res_col, prize = "🤝 푸시 (타이)", "#888888", bet_f
            else:
                result, res_col, prize = "😢 패배...", "#4B9EFF", 0

            net = prize - bet_f
            net_str = f"+{format_korean_money(net)}" if net > 0 else f"-{format_korean_money(abs(net))}" if net < 0 else "베팅금 반환"
            net_col = "#FF4B4B" if net > 0 else "#4B9EFF" if net < 0 else "#888"

            st.markdown(f"""
            <div style='text-align:center;background:rgba(0,0,0,0.4);border:2px solid {res_col};
                 border-radius:18px;padding:28px;margin:20px 0;box-shadow:0 0 30px {res_col}44;'>
              <div style='font-size:1.8rem;font-weight:900;color:{res_col};'>{result}</div>
              <div style='font-size:1.3rem;font-weight:900;color:{net_col};margin-top:10px;'>{net_str}</div>
              <div style='color:#888;font-size:0.8rem;margin-top:8px;'>지급액: {format_korean_money(prize)}</div>
            </div>
            """, unsafe_allow_html=True)

            if 'bj_paid' not in st.session_state:
                st.session_state.bj_paid = True
                if prize > 0:
                    st.session_state.global_cash += prize
                    log_tx(st.session_state.logged_in_user, "블랙잭", result, net)
                sync_user_data()              

            if st.button("🔄 다시 하기!", use_container_width=True):
                for k in ['bj_state','bj_player','bj_dealer','bj_bet','bj_paid']:
                    if k in st.session_state: del st.session_state[k]
                st.rerun()