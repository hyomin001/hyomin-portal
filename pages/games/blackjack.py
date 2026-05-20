# pages/games/blackjack.py
import streamlit as st
import random
from utils.core import format_korean_money, cooldown_remaining, set_cooldown, sync_user_data
from utils.database import log_tx, atomic_deduct_cash, atomic_add_cash

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
            'bj_split_hand': [], 'bj_split_active': False, 'bj_split_bet': 0,
            'bj_current_hand': 'main',  # 'main' or 'split'
        })

    state = st.session_state.bj_state
    uid   = st.session_state.logged_in_user

    # ── 베팅 화면 ──
    if state == 'betting':
        st.markdown(f"""
        <div style='text-align:center;padding:30px;background:linear-gradient(135deg,rgba(180,0,0,0.15),rgba(0,100,0,0.15));
             border:2px solid rgba(255,215,0,0.3);border-radius:18px;margin-bottom:24px;'>
          <div style='font-size:4rem;'>🃏</div>
          <div style='font-family:Orbitron,monospace;font-size:1.3rem;color:#FFD600;margin-top:8px;font-weight:900;'>BLACKJACK</div>
          <div style='color:#94A3B8;margin-top:10px;font-size:0.88rem;'>블랙잭(A+10) = 베팅의 1.5배 추가 지급 &nbsp;|&nbsp; 더블다운 = 카드 1장 추가 + 베팅 2배 &nbsp;|&nbsp; 스플릿 = 페어 분리</div>
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
                # 원자적 차감
                if not atomic_deduct_cash(uid, bet):
                    st.error("잔액 부족! (DB 검증 실패)")
                    st.stop()
                st.session_state.global_cash -= bet
                st.session_state.bj_bet = bet
                deck   = st.session_state.bj_deck if len(st.session_state.bj_deck) > 30 else bj_make_deck()
                player = [deck.pop(), deck.pop()]
                dealer = [deck.pop(), deck.pop()]
                st.session_state.bj_player     = player
                st.session_state.bj_dealer     = dealer
                st.session_state.bj_deck       = deck
                st.session_state.bj_split_hand = []
                st.session_state.bj_split_active = False
                st.session_state.bj_split_bet  = 0
                st.session_state.bj_current_hand = 'main'

                if bj_value(player) == 21:
                    dl, dk = bj_dealer_play(dealer, deck)
                    st.session_state.bj_dealer = dl
                    st.session_state.bj_deck   = dk
                    st.session_state.bj_state  = 'done'
                else:
                    st.session_state.bj_state = 'playing'
                sync_user_data()
                st.rerun()

    # ── 플레이 화면 ──
    elif state == 'playing':
        player   = st.session_state.bj_player
        dealer   = st.session_state.bj_dealer
        bet      = st.session_state.bj_bet
        pval     = bj_value(player)
        split_on = st.session_state.bj_split_active
        cur_hand = st.session_state.bj_current_hand

        # 딜러 패
        st.markdown("### 🎩 딜러의 패")
        st.markdown(f"{bj_render(dealer, hide_second=True)}", unsafe_allow_html=True)
        st.caption(f"딜러 공개 패: {bj_value([dealer[0]])}점 + ?")
        st.write("")

        # 현재 플레이 손 표시
        def show_hand(hand, label, hand_bet):
            hval = bj_value(hand)
            col = "#FF4B4B" if hval > 21 else "#00FF88" if hval == 21 else "#fff"
            bust_str = "  💥BUST" if hval > 21 else ("  🃏BJ!" if hval == 21 and len(hand) == 2 else "")
            st.markdown(f"### 🎴 {label} (베팅: {format_korean_money(hand_bet)})")
            st.markdown(f"{bj_render(hand)} <span style='color:{col};font-size:1.2rem;font-weight:900;margin-left:12px;'>{hval}점{bust_str}</span>", unsafe_allow_html=True)
            return hval

        if split_on:
            if cur_hand == 'main':
                pval = show_hand(player, "메인 손 (진행 중)", bet)
                show_hand(st.session_state.bj_split_hand, "스플릿 손 (대기)", st.session_state.bj_split_bet)
            else:
                show_hand(player, "메인 손 (완료)", bet)
                pval = show_hand(st.session_state.bj_split_hand, "스플릿 손 (진행 중)", st.session_state.bj_split_bet)
        else:
            pval = show_hand(player, "내 패", bet)

        st.write("")

        # 스플릿 가능 여부
        can_split = (
            not split_on
            and len(player) == 2
            and player[0][0] == player[1][0]
            and st.session_state.global_cash >= bet
        )
        # 더블다운 가능 여부 (처음 2장일 때만)
        active_hand = player if (not split_on or cur_hand == 'main') else st.session_state.bj_split_hand
        can_double  = len(active_hand) == 2 and st.session_state.global_cash >= bet

        def finish_current_hand():
            """현재 손을 스탠드 처리하고, 스플릿이 있으면 다음 손으로 전환."""
            if split_on and cur_hand == 'main':
                st.session_state.bj_current_hand = 'split'
            else:
                # 모든 손 완료 → 딜러 플레이 → done
                dl, dk = bj_dealer_play(st.session_state.bj_dealer, st.session_state.bj_deck)
                st.session_state.bj_dealer = dl
                st.session_state.bj_deck   = dk
                st.session_state.bj_state  = 'done'

        # 액션 버튼
        cols = st.columns(4 if (can_split or can_double) else 2)
        col_idx = 0

        with cols[col_idx]:
            if st.button("👊 히트", use_container_width=True):
                deck = st.session_state.bj_deck
                if not split_on or cur_hand == 'main':
                    st.session_state.bj_player.append(deck.pop())
                    new_val = bj_value(st.session_state.bj_player)
                else:
                    st.session_state.bj_split_hand.append(deck.pop())
                    new_val = bj_value(st.session_state.bj_split_hand)
                st.session_state.bj_deck = deck
                if new_val >= 21:
                    finish_current_hand()
                st.rerun()
        col_idx += 1

        with cols[col_idx]:
            if st.button("🛑 스탠드", use_container_width=True):
                finish_current_hand()
                st.rerun()
        col_idx += 1

        if can_double:
            with cols[col_idx]:
                if st.button("✌️ 더블다운", use_container_width=True):
                    # 추가 베팅 (원자적)
                    if atomic_deduct_cash(uid, bet):
                        st.session_state.global_cash -= bet
                        deck = st.session_state.bj_deck
                        if not split_on or cur_hand == 'main':
                            st.session_state.bj_player.append(deck.pop())
                            st.session_state.bj_bet *= 2
                        else:
                            st.session_state.bj_split_hand.append(deck.pop())
                            st.session_state.bj_split_bet *= 2
                        st.session_state.bj_deck = deck
                        finish_current_hand()
                        sync_user_data()
                        st.rerun()
                    else:
                        st.error("잔액 부족! (더블다운 실패)")
            col_idx += 1

        if can_split:
            with cols[col_idx]:
                if st.button("🔀 스플릿", use_container_width=True):
                    # 추가 베팅 (원자적)
                    if atomic_deduct_cash(uid, bet):
                        st.session_state.global_cash -= bet
                        deck = st.session_state.bj_deck
                        # 두 번째 카드를 스플릿 손으로 분리
                        split_card = st.session_state.bj_player.pop()
                        st.session_state.bj_split_hand  = [split_card, deck.pop()]
                        st.session_state.bj_player.append(deck.pop())
                        st.session_state.bj_deck        = deck
                        st.session_state.bj_split_active = True
                        st.session_state.bj_split_bet   = bet
                        st.session_state.bj_current_hand = 'main'
                        sync_user_data()
                        st.rerun()
                    else:
                        st.error("잔액 부족! (스플릿 실패)")

    # ── 결과 화면 ──
    else:  # done
        player = st.session_state.bj_player
        dealer = st.session_state.bj_dealer
        bet    = st.session_state.bj_bet
        split_hand = st.session_state.bj_split_hand
        split_bet  = st.session_state.bj_split_bet
        split_on   = st.session_state.bj_split_active

        # 딜러 패 공개
        st.markdown("### 🎩 딜러의 패")
        dval = bj_value(dealer)
        dcol = "#FF4B4B" if dval > 21 else "#fff"
        st.markdown(f"{bj_render(dealer)} <span style='color:{dcol};font-size:1.1rem;font-weight:900;margin-left:12px;'>{dval}점{'  💥BUST' if dval>21 else ''}</span>", unsafe_allow_html=True)
        st.write("")

        def calc_result(hand, hand_bet):
            pval_f = bj_value(hand)
            is_bj  = (pval_f == 21 and len(hand) == 2 and not split_on)
            if pval_f > 21:
                return "💥 버스트! 패배", "#4B9EFF", 0
            elif dval > 21:
                return "🎉 딜러 버스트! 승리!", "#FF4B4B", hand_bet * 2
            elif is_bj and dval != 21:
                return "🃏 블랙잭!! 1.5배!", "#FFD600", int(hand_bet * 2.5)
            elif pval_f > dval:
                return "🎉 승리!", "#00FF88", hand_bet * 2
            elif pval_f == dval:
                return "🤝 푸시 (타이)", "#888888", hand_bet
            else:
                return "😢 패배...", "#4B9EFF", 0

        def show_result_card(hand, hand_bet, label):
            result, res_col, prize = calc_result(hand, hand_bet)
            net     = prize - hand_bet
            net_str = f"+{format_korean_money(net)}" if net > 0 else f"-{format_korean_money(abs(net))}" if net < 0 else "베팅금 반환"
            net_col = "#FF4B4B" if net > 0 else "#4B9EFF" if net < 0 else "#888"
            st.markdown(f"### 🎴 {label}")
            st.markdown(f"{bj_render(hand)} <span style='font-size:1rem;color:#aaa;margin-left:12px;'>{bj_value(hand)}점</span>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='text-align:center;background:rgba(0,0,0,0.4);border:2px solid {res_col};
                 border-radius:18px;padding:20px;margin:14px 0;box-shadow:0 0 30px {res_col}44;'>
              <div style='font-size:1.5rem;font-weight:900;color:{res_col};'>{result}</div>
              <div style='font-size:1.2rem;font-weight:900;color:{net_col};margin-top:8px;'>{net_str}</div>
              <div style='color:#94A3B8;font-size:0.8rem;margin-top:6px;'>지급액: {format_korean_money(prize)}</div>
            </div>
            """, unsafe_allow_html=True)
            return prize

        if 'bj_paid' not in st.session_state:
            st.session_state.bj_paid = True
            total_prize = 0
            total_prize += show_result_card(player, bet, "메인 손" if split_on else "내 패")
            if split_on:
                total_prize += show_result_card(split_hand, split_bet, "스플릿 손")

            total_bet = bet + (split_bet if split_on else 0)
            total_net = total_prize - total_bet
            if total_prize > 0:
                atomic_add_cash(uid, total_prize)
                st.session_state.global_cash += total_prize
            # ✅ [BUG FIX] total_prize=0(패배)일 때 log_tx가 없어서 손실 기록 누락되던 것 수정
            log_tx(uid, "블랙잭", f"블랙잭 결과 (지급 {format_korean_money(total_prize)})", total_net)
            sync_user_data()
        else:
            # 이미 지급된 경우 결과만 재표시
            show_result_card(player, bet, "메인 손" if split_on else "내 패")
            if split_on:
                show_result_card(split_hand, split_bet, "스플릿 손")

        if st.button("🔄 다시 하기!", use_container_width=True):
            for k in ['bj_state','bj_player','bj_dealer','bj_bet','bj_paid',
                      'bj_split_hand','bj_split_active','bj_split_bet','bj_current_hand']:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
