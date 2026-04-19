import streamlit as st
import random
from itertools import combinations
from collections import Counter
from utils.core import format_korean_money, sync_user_data
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx

# ─────────────────────────────
# 🃏 카드 및 덱 정의
# ─────────────────────────────
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VAL = {r: i for i, r in enumerate(RANKS, 2)}

def make_deck():
    return [{"suit": s, "rank": r, "val": RANK_VAL[r]} for s in SUITS for r in RANKS]

def card_html(card):
    # ♥, ♦는 빨간색 / ♠, ♣는 흰색(테마에 맞게)으로 예쁘게 렌더링
    color = "#FF4B4B" if card['suit'] in ["♥", "♦"] else "#E2E8F0"
    return f"<div style='display:inline-block; padding:10px 15px; margin:4px; background:rgba(255,255,255,0.05); border:1px solid {color}55; border-radius:8px; color:{color}; font-weight:900; font-size:1.5rem; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);'>{card['suit']} {card['rank']}</div>"

def hidden_card_html():
    return f"<div style='display:inline-block; padding:10px 15px; margin:4px; background:linear-gradient(135deg, #1E293B, #0F172A); border:1px solid #334155; border-radius:8px; color:#64748B; font-weight:900; font-size:1.5rem; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);'>🂠 ?</div>"

# ─────────────────────────────
# 🔍 실시간 핸드 평가 (족보 판독기)
# ─────────────────────────────
def score_cards(cards):
    if not cards: return (0, [])
    vals = sorted([c['val'] for c in cards], reverse=True)
    suits = [c['suit'] for c in cards]

    is_flush = len(cards) >= 5 and len(set(suits)) == 1
    is_straight = False
    if len(cards) >= 5:
        if vals == list(range(vals[0], vals[0]-5, -1)) or vals == [14, 5, 4, 3, 2]:
            is_straight = True

    cnt = Counter(vals)
    groups = sorted(cnt.values(), reverse=True)
    ordered = sorted(vals, key=lambda v: (cnt[v], v), reverse=True)

    if is_straight and is_flush: return (8, ordered)
    if groups and groups[0] == 4: return (7, ordered)
    if groups and len(groups) >= 2 and groups[:2] == [3, 2]: return (6, ordered)
    if is_flush: return (5, ordered)
    if is_straight: return (4, ordered)
    if groups and groups[0] == 3: return (3, ordered)
    if groups and len(groups) >= 2 and groups[:2] == [2, 2]: return (2, ordered)
    if groups and groups[0] == 2: return (1, ordered)
    return (0, ordered)

def evaluate_hand(cards):
    # 카드가 5장 미만일 땐 현재 카드만으로 족보 판별
    if len(cards) < 5:
        return score_cards(cards)
    
    best = (0, [])
    for five in combinations(cards, 5):
        score = score_cards(list(five))
        if score > best:
            best = score
    return best

HAND_NAMES = {
    8: "🔥 스트레이트 플러시",
    7: "💎 포카드",
    6: "🏠 풀하우스",
    5: "🌊 플러시",
    4: "➡️ 스트레이트",
    3: "3️⃣ 트리플",
    2: "2️⃣ 투페어",
    1: "1️⃣ 원페어",
    0: "🃏 하이카드 (탑)"
}

# ─────────────────────────────
# 🤖 딜러 AI 및 게임 진행
# ─────────────────────────────
def dealer_action(state):
    score = evaluate_hand(state['dealer_hand'] + state['community'])[0]
    
    if score >= 2: # 투페어 이상: 무조건 콜 또는 역레이즈 성향
        return random.choices(['call'], [10])[0] 
    elif score >= 1: # 원페어: 대부분 콜, 가끔 쫄아서 폴드
        return random.choices(['fold', 'call'], [2, 8])[0]
    else: # 뻥카: 대부분 폴드, 가끔 블러핑 콜
        return random.choices(['fold', 'call'], [7, 3])[0]

def advance_stage(state):
    deck = state['deck']
    state['player_bet'] = 0
    state['dealer_bet'] = 0

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
# 🖥️ 메인 렌더링 화면
# ─────────────────────────────
def render(market, nw):
    st.title("🃏 텍사스 홀덤 카지노")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>딜러와 1:1 진검승부! 실시간으로 변하는 족보를 확인하며 베팅하세요.</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user

    # ── 초기화 및 바이인 ─────────────────
    if 'holdem' not in st.session_state or st.session_state.holdem.get('game_over'):
        st.markdown("### 🎫 참가비 (앤티) 설정")
        buy = st.selectbox("베팅 규모를 선택하세요", [10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_000_000_000], format_func=lambda x: format_korean_money(x))

        if st.button("🚀 게임 시작", type="primary", use_container_width=True):
            # 🛡️ DB 원자적 차감 (경쟁 조건 방지)
            u_fresh = load_db(USERS_FILE, {})
            db_cash = u_fresh.get(uid, {}).get('cash', 0)
            
            if db_cash < buy:
                st.error("❌ 잔액이 부족합니다!")
                st.stop()
                
            u_fresh[uid]['cash'] = db_cash - buy
            save_db(USERS_FILE, u_fresh)
            st.session_state.global_cash = u_fresh[uid]['cash']
            
            deck = make_deck()
            random.shuffle(deck)

            st.session_state.holdem = {
                "deck": deck,
                "player_hand": [deck.pop(), deck.pop()],
                "dealer_hand": [deck.pop(), deck.pop()],
                "community": [],
                "pot": buy * 2, # 내가 낸 참가비 + 딜러가 낸 참가비
                "player_bet": 0,
                "dealer_bet": 0,
                "stage": "preflop",
                "game_over": False,
                "result": None,
                "base_bet": buy
            }
            sync_user_data()
            st.rerun()
        return

    state = st.session_state.holdem
    BET_UNIT = int(state['base_bet'] * 0.5) # 레이즈 한 번에 기본 판돈의 50%씩 추가 베팅

    # ── 게임 화면 (카드 및 팟 표시) ─────────────────
    c_dlr, c_pot, c_me = st.columns([1, 1.2, 1])

    with c_dlr:
        st.markdown("<h4 style='color:#94A3B8;'>🤖 딜러의 패</h4>", unsafe_allow_html=True)
        dealer_html = ""
        for i, c in enumerate(state['dealer_hand']):
            if state['stage'] != 'showdown' and i == 1:
                dealer_html += hidden_card_html()
            else:
                dealer_html += card_html(c)
        st.markdown(dealer_html, unsafe_allow_html=True)
        
        if state['stage'] == 'showdown':
            dlr_score = evaluate_hand(state['dealer_hand'] + state['community'])[0]
            st.markdown(f"<div style='color:#FF4B4B; font-weight:bold; margin-top:5px;'>딜러 족보: {HAND_NAMES[dlr_score]}</div>", unsafe_allow_html=True)

    with c_pot:
        st.markdown(f"""
        <div style='text-align:center; background:rgba(255,214,0,0.1); border:2px solid #FFD600; border-radius:15px; padding:20px; box-shadow: 0 0 15px rgba(255,214,0,0.2);'>
            <div style='color:#FFD600; font-weight:900; font-size:1.1rem; margin-bottom:5px;'>💰 총 상금 (POT)</div>
            <div style='color:#FFFFFF; font-size:1.8rem; font-weight:900;'>{format_korean_money(state['pot'])}</div>
            <div style='color:#888; font-size:0.85rem; margin-top:10px;'>현재 스테이지: <b style='color:#00E5FF;'>{state['stage'].upper()}</b></div>
        </div>
        """, unsafe_allow_html=True)

    with c_me:
        st.markdown("<h4 style='color:#00E5FF;'>😎 나의 패</h4>", unsafe_allow_html=True)
        player_html = "".join([card_html(c) for c in state['player_hand']])
        st.markdown(player_html, unsafe_allow_html=True)
        
        my_score = evaluate_hand(state['player_hand'] + state['community'])[0]
        st.markdown(f"""
        <div style='background:rgba(0,229,255,0.1); border-left:4px solid #00E5FF; padding:10px; margin-top:10px; border-radius:4px;'>
            <span style='color:#94A3B8; font-size:0.8rem;'>현재 예상 족보</span><br>
            <b style='color:#00E5FF; font-size:1.1rem;'>{HAND_NAMES[my_score]}</b>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("<h4 style='text-align:center; color:#E2E8F0;'>🌐 공유 카드 (Community)</h4>", unsafe_allow_html=True)
    if state['community']:
        comm_html = "<div style='text-align:center; margin-bottom:20px;'>" + "".join([card_html(c) for c in state['community']]) + "</div>"
        st.markdown(comm_html, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; color:#64748B; padding:20px; font-style:italic;'>아직 바닥에 카드가 깔리지 않았습니다.</div>", unsafe_allow_html=True)

    st.write("---")

    # ── 액션 버튼 ─────────────────
    if not state['game_over']:
        st.markdown("### ⚡ 당신의 차례입니다!")
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("🏳️ 폴드 (기권)", use_container_width=True):
                state['result'] = 'lose'
                state['game_over'] = True
                st.rerun()

        with b2:
            btn_txt = "콜 (체크)" if state['dealer_bet'] == state['player_bet'] else f"콜 ({format_korean_money(state['dealer_bet'] - state['player_bet'])} 추가)"
            if st.button(f"👌 {btn_txt}", use_container_width=True):
                diff = state['dealer_bet'] - state['player_bet']
                if diff > 0:
                    u_fresh = load_db(USERS_FILE, {})
                    if u_fresh.get(uid, {}).get('cash', 0) < diff:
                        st.error("잔액이 부족하여 콜을 받을 수 없습니다!")
                        st.stop()
                    u_fresh[uid]['cash'] -= diff
                    save_db(USERS_FILE, u_fresh)
                    st.session_state.global_cash -= diff
                    state['player_bet'] += diff
                    state['pot'] += diff
                    
                advance_stage(state)
                sync_user_data()
                st.rerun()

        with b3:
            if st.button(f"🔥 베팅 / 레이즈 (+{format_korean_money(BET_UNIT)})", use_container_width=True, type="primary"):
                u_fresh = load_db(USERS_FILE, {})
                db_cash = u_fresh.get(uid, {}).get('cash', 0)
                
                # 내가 레이즈하기 위해 내야 할 돈 (콜 비용 + 추가 레이즈 비용)
                diff_to_call = state['dealer_bet'] - state['player_bet']
                total_cost = diff_to_call + BET_UNIT
                
                if db_cash < total_cost:
                    st.error("잔액이 부족하여 베팅할 수 없습니다!")
                    st.stop()
                    
                # 1. 내 돈 차감 및 팟에 추가
                u_fresh[uid]['cash'] -= total_cost
                save_db(USERS_FILE, u_fresh)
                st.session_state.global_cash -= total_cost
                state['player_bet'] += total_cost
                state['pot'] += total_cost
                sync_user_data()

                # 2. 딜러의 응답 확인
                action = dealer_action(state)

                if action == 'fold':
                    st.toast("딜러가 당신의 레이즈에 쫄아서 폴드했습니다!", icon="🏃")
                    state['result'] = 'win'
                    state['game_over'] = True
                elif action == 'call':
                    st.toast("딜러가 콜을 받았습니다!", icon="👌")
                    # 딜러가 콜을 받았으므로 팟에 돈 추가
                    state['dealer_bet'] += BET_UNIT
                    state['pot'] += BET_UNIT
                    advance_stage(state)
                    
                st.rerun()

    # ── 게임 결과 처리 ─────────────────
    else:
        st.markdown("---")
        st.markdown("### 🏁 게임 종료!")
        
        if state['result'] is None:
            p_score = evaluate_hand(state['player_hand'] + state['community'])
            d_score = evaluate_hand(state['dealer_hand'] + state['community'])

            if p_score > d_score:
                state['result'] = 'win'
            elif p_score < d_score:
                state['result'] = 'lose'
            else:
                state['result'] = 'draw'

        if state['result'] == 'win':
            prize = state['pot']
            st.success(f"🎉 승리! 딜러의 돈을 쓸어 담았습니다. (+{format_korean_money(prize)})")
            u_fresh = load_db(USERS_FILE, {})
            u_fresh[uid]['cash'] += prize
            save_db(USERS_FILE, u_fresh)
            st.session_state.global_cash += prize
            log_tx(uid, "홀덤", "승리 (팟 획득)", prize)

        elif state['result'] == 'draw':
            prize = state['pot'] // 2
            st.info(f"🤝 무승부! 배팅금을 나눠 갖습니다. (+{format_korean_money(prize)})")
            u_fresh = load_db(USERS_FILE, {})
            u_fresh[uid]['cash'] += prize
            save_db(USERS_FILE, u_fresh)
            st.session_state.global_cash += prize
            log_tx(uid, "홀덤", "무승부 (베팅금 반환)", prize)

        else:
            st.error(f"💀 패배... 딜러가 상금을 모두 가져갑니다.")
            log_tx(uid, "홀덤", "패배 (팟 잃음)", 0)

        sync_user_data()

        if st.button("🔄 다음 판 플레이", use_container_width=True, type="primary"):
            del st.session_state.holdem
            st.rerun()
