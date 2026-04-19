import streamlit as st
import random
from itertools import combinations
from collections import Counter
from utils.core import format_korean_money, sync_user_data
from utils.database import log_tx

# ─────────────────────────────
# 카드 정의
# ─────────────────────────────
SUITS = ["♠","♥","♦","♣"]
RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
RANK_VAL = {r: i for i, r in enumerate(RANKS, 2)}

def make_deck():
    return [{"suit": s, "rank": r, "val": RANK_VAL[r]} 
            for s in SUITS for r in RANKS]

def card_str(card):
    color = "🔴" if card['suit'] in ["♥","♦"] else "⚫"
    return f"{color}{card['suit']}{card['rank']}"

# ─────────────────────────────
# 핸드 평가
# ─────────────────────────────
def evaluate_hand(seven_cards):
    best = (0, [])
    for five in combinations(seven_cards, 5):
        score = score_five(list(five))
        if score > best:
            best = score
    return best

def score_five(cards):
    vals = sorted([c['val'] for c in cards], reverse=True)
    suits = [c['suit'] for c in cards]

    is_flush = len(set(suits)) == 1
    is_straight = (
        vals == list(range(vals[0], vals[0]-5, -1)) or
        vals == [14,5,4,3,2]
    )

    cnt = Counter(vals)
    groups = sorted(cnt.values(), reverse=True)

    ordered = sorted(vals, key=lambda v: (cnt[v], v), reverse=True)

    if is_straight and is_flush:
        return (8, ordered)
    if groups[0] == 4:
        return (7, ordered)
    if groups[:2] == [3,2]:
        return (6, ordered)
    if is_flush:
        return (5, ordered)
    if is_straight:
        return (4, ordered)
    if groups[0] == 3:
        return (3, ordered)
    if groups[:2] == [2,2]:
        return (2, ordered)
    if groups[0] == 2:
        return (1, ordered)
    return (0, ordered)

HAND_NAMES = {
    8:"🔥 스트레이트 플러시",
    7:"💎 포카드",
    6:"🏠 풀하우스",
    5:"🌊 플러시",
    4:"➡️ 스트레이트",
    3:"3️⃣ 트리플",
    2:"2️⃣ 투페어",
    1:"1️⃣ 원페어",
    0:"🃏 하이카드"
}

# ─────────────────────────────
# 딜러 AI
# ─────────────────────────────
def dealer_action(state):
    score = evaluate_hand(state['dealer_hand'] + state['community'])[0]
    to_call = state['player_bet'] - state['dealer_bet']

    if score >= 3:
        return random.choices(['call','raise'], [3,7])[0]
    elif score >= 1:
        return random.choices(['fold','call','raise'], [2,6,2])[0]
    else:
        return random.choices(['fold','call'], [5,5])[0]

# ─────────────────────────────
# 스테이지 진행
# ─────────────────────────────
def advance_stage(state):
    deck = state['deck']

    if state['stage'] == 'preflop':
        state['community'] = [deck.pop(), deck.pop(), deck.pop()]
        state['stage'] = 'flop'

    elif state['stage'] == 'flop':
        state['community'].append(deck.pop())
        state['stage'] = 'turn'

    elif state['stage'] == 'turn':
        state['community'].append(deck.pop())
        state['stage'] = 'river'

    elif state['stage'] == 'river':
        state['stage'] = 'showdown'
        state['game_over'] = True

# ─────────────────────────────
# 메인 렌더
# ─────────────────────────────
def render(market, nw):
    st.title("🃏 텍사스 홀덤")

    BET_UNIT = 10_000_000
    MIN_BUY = 100_000_000

    # ── 초기화 ─────────────────
    if 'holdem' not in st.session_state or st.session_state.holdem.get('game_over'):
        buy = st.number_input("바이인", MIN_BUY, step=MIN_BUY)

        if st.button("게임 시작"):
            if st.session_state.global_cash < buy:
                st.error("잔액 부족")
                return

            deck = make_deck()
            random.shuffle(deck)

            st.session_state.holdem = {
                "deck": deck,
                "player_hand": [deck.pop(), deck.pop()],
                "dealer_hand": [deck.pop(), deck.pop()],
                "community": [],
                "pot": 0,
                "player_bet": 0,
                "dealer_bet": 0,
                "stage": "preflop",
                "game_over": False,
                "result": None,
                "buy_in": buy
            }

            st.session_state.global_cash -= buy
            sync_user_data()
            st.rerun()
        return

    state = st.session_state.holdem

    # ── 카드 표시 ─────────────────
    st.markdown("### 🤖 딜러")
    dealer_cards = []
    for i, c in enumerate(state['dealer_hand']):
        if state['stage'] != 'showdown' and i == 1:
            dealer_cards.append("🂠")
        else:
            dealer_cards.append(card_str(c))
    st.markdown("## " + " ".join(dealer_cards))

    st.write("---")

    st.markdown(f"💰 팟: {format_korean_money(state['pot'])}")
    st.markdown("## " + " ".join(card_str(c) for c in state['community']))

    st.write("---")

    st.markdown("### 😎 내 패")
    st.markdown("## " + " ".join(card_str(c) for c in state['player_hand']))

    # ── 액션 ─────────────────
    if not state['game_over']:

        if st.button("폴드"):
            state['result'] = 'lose'
            state['game_over'] = True
            st.rerun()

        if st.button("콜"):
            diff = state['dealer_bet'] - state['player_bet']
            state['player_bet'] += diff
            state['pot'] += diff
            advance_stage(state)
            st.rerun()

        if st.button("레이즈"):
            raise_amt = BET_UNIT
            state['player_bet'] += raise_amt
            state['pot'] += raise_amt

            action = dealer_action(state)

            if action == 'fold':
                state['result'] = 'win'
                state['game_over'] = True

            elif action == 'call':
                state['dealer_bet'] = state['player_bet']
                advance_stage(state)

            else:
                state['dealer_bet'] = state['player_bet'] + raise_amt
                state['pot'] += raise_amt

            st.rerun()

    # ── 결과 ─────────────────
    else:
        if state['result'] is None:
            p = evaluate_hand(state['player_hand'] + state['community'])
            d = evaluate_hand(state['dealer_hand'] + state['community'])

            if p > d:
                state['result'] = 'win'
            elif p < d:
                state['result'] = 'lose'
            else:
                state['result'] = 'draw'

        if state['result'] == 'win':
            prize = state['pot']
            st.success(f"승리 +{format_korean_money(prize)}")
            st.session_state.global_cash += prize

        elif state['result'] == 'draw':
            prize = state['pot']//2
            st.info(f"무승부 {format_korean_money(prize)}")
            st.session_state.global_cash += prize

        else:
            st.error("패배")

        sync_user_data()

        if st.button("다시"):
            del st.session_state.holdem
            st.rerun()
