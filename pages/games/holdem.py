import streamlit as st
import random
import time
from itertools import combinations
from collections import Counter
from utils.core import format_korean_money, sync_user_data
from utils.config import USERS_FILE
from utils.database import load_db, save_db, log_tx

# ─────────────────────────────
# 🃏 1. 카드 및 덱 정의 (예쁜 UI - 한 줄로 압축!)
# ─────────────────────────────
SUITS = ["♠", "♥", "♦", "♣"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
RANK_VAL = {r: i for i, r in enumerate(RANKS, 2)}

def make_deck():
    return [{"suit": s, "rank": r, "val": RANK_VAL[r]} for s in SUITS for r in RANKS]

def card_html(card):
    color = "#FF4B4B" if card['suit'] in ["♥", "♦"] else "#E2E8F0"
    return f"<div style='display:inline-block; padding:15px 20px; margin:5px; background:linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02)); border:1px solid {color}66; border-radius:10px; color:{color}; font-weight:900; font-size:1.6rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3); text-align:center; min-width:60px;'><div style='font-size:1rem; margin-bottom:-5px;'>{card['suit']}</div><div>{card['rank']}</div></div>"

def hidden_card_html():
    return "<div style='display:inline-block; padding:15px 20px; margin:5px; background:linear-gradient(145deg, #1E293B, #0F172A); border:1px solid #334155; border-radius:10px; color:#64748B; font-weight:900; font-size:1.6rem; box-shadow: 0 4px 6px rgba(0,0,0,0.3); text-align:center; min-width:60px;'><div style='font-size:1rem; margin-bottom:-5px;'>🂠</div><div>?</div></div>"

# ─────────────────────────────
# 🔍 2. 실시간 족보 판독기
# ─────────────────────────────
HAND_NAMES = {
    8: "🔥 스트레이트 플러시",
    7: "💎 포카드 (Quads)",
    6: "🏠 풀하우스 (Full House)",
    5: "🌊 플러시 (Flush)",
    4: "➡️ 스트레이트 (Straight)",
    3: "3️⃣ 트리플 (Three of Kind)",
    2: "2️⃣ 투페어 (Two Pair)",
    1: "1️⃣ 원페어 (One Pair)",
    0: "🃏 하이카드 (탑)"
}

def get_best_hand(cards):
    if not cards: return (0, []), "알 수 없음"
    
    best_score = -1
    best_ordered = []
    eval_len = min(5, len(cards))
    
    for combo in combinations(cards, eval_len):
        vals = sorted([c['val'] for c in combo], reverse=True)
        suits = [c['suit'] for c in combo]
        
        is_flush = (len(combo) == 5) and (len(set(suits)) == 1)
        is_straight = False
        if len(combo) == 5:
            if vals == list(range(vals[0], vals[0]-5, -1)):
                is_straight = True
            elif vals == [14, 5, 4, 3, 2]:
                is_straight = True
                vals = [5, 4, 3, 2, 1] 
                
        cnt = Counter(vals)
        groups = sorted(cnt.values(), reverse=True)
        ordered = sorted(vals, key=lambda v: (cnt[v], v), reverse=True)
        
        score = 0
        if is_straight and is_flush: score = 8
        elif groups and groups[0] == 4: score = 7
        elif groups and len(groups) >= 2 and groups[:2] == [3, 2]: score = 6
        elif is_flush: score = 5
        elif is_straight: score = 4
        elif groups and groups[0] == 3: score = 3
        elif groups and len(groups) >= 2 and groups[:2] == [2, 2]: score = 2
        elif groups and groups[0] == 2: score = 1
        
        if score > best_score or (score == best_score and ordered > best_ordered):
            best_score = score
            best_ordered = ordered
            
    return (best_score, best_ordered)

# ─────────────────────────────
# 🤖 3. 딜러 AI 및 게임 스테이지 제어 (AI 개선)
# ─────────────────────────────
def dealer_action(state):
    score = get_best_hand(state['dealer_hand'] + state['community'])[0]
    
    # 🛠️ [수정] 1. 바닥에 카드가 없는 첫 턴(Pre-flop)에서는 딜러가 덜 쫄게 만듦!
    if len(state['community']) == 0:
        if score >= 1: # 시작부터 원페어면
            return 'call' # 무조건 콜
        else:
            return random.choices(['fold', 'call'], [2, 8])[0] # 80% 확률로 콜 받음 (20%만 폴드)
            
    # 🛠️ 2. 바닥에 카드가 깔린 이후 본격적인 심리전
    if score >= 2: # 투페어 이상
        return 'call'
    elif score >= 1: # 원페어
        return random.choices(['fold', 'call'], [3, 7])[0]
    else: # 뻥카 (하이카드)
        return random.choices(['fold', 'call'], [7, 3])[0] # 여긴 70% 확률로 도망감

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
# 🖥️ 4. 메인 렌더링 화면
# ─────────────────────────────
def render(market, nw):
    st.title("🃏 텍사스 홀덤 카지노")
    st.markdown("<div style='color:#888;margin-bottom:16px;'>딜러와 1:1 진검승부! 실시간으로 변하는 족보를 확인하며 베팅하세요.</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user

    # ── 초기화 및 바이인 (참가비) ─────────────────
    if 'holdem' not in st.session_state or st.session_state.holdem.get('rematch_ready'):
        st.markdown("### 🎫 참가비 (앤티) 설정")
        buy_opts = [10_000_000, 50_000_000, 100_000_000, 500_000_000, 1_000_000_000]
        buy = st.selectbox("기본 판돈을 선택하세요", buy_opts, format_func=lambda x: format_korean_money(x))

        if st.button("🚀 게임 시작", type="primary", use_container_width=True):
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
                "pot": buy * 2,
                "player_bet": 0,
                "dealer_bet": 0,
                "stage": "preflop",
                "game_over": False,
                "result": None,
                "reward_claimed": False,
                "base_bet": buy,
                "dealer_msg": "" # 👈 딜러의 반응을 화면에 고정시키기 위한 변수 추가!
            }
            sync_user_data()
            st.rerun()
        return

    state = st.session_state.holdem
    BET_UNIT = int(state['base_bet'] * 0.5)

    # ── 딜러의 반응 메시지 표시 ─────────────────
    if state.get('dealer_msg'):
        if "쫄아서" in state['dealer_msg']:
            st.success(state['dealer_msg'])
        else:
            st.warning(state['dealer_msg'])
        state['dealer_msg'] = "" # 화면에 한 번만 보여주고 초기화

    # ── 게임 화면 (카드 및 팟 표시) ─────────────────
    c_dlr, c_pot, c_me = st.columns([1, 1.2, 1])

    with c_dlr:
        st.markdown("<h4 style='color:#94A3B8; text-align:center;'>🤖 딜러의 패</h4>", unsafe_allow_html=True)
        dealer_html = "<div style='text-align:center;'>"
        for i, c in enumerate(state['dealer_hand']):
            if not state['game_over'] and i == 1:
                dealer_html += hidden_card_html()
            else:
                dealer_html += card_html(c)
        dealer_html += "</div>"
        st.markdown(dealer_html, unsafe_allow_html=True)
        
        if state['game_over']:
            dlr_score = get_best_hand(state['dealer_hand'] + state['community'])[0]
            st.markdown(f"<div style='text-align:center; color:#FF4B4B; font-weight:bold; margin-top:5px; font-size:1.1rem;'>딜러: {HAND_NAMES[dlr_score]}</div>", unsafe_allow_html=True)

    with c_pot:
        st.markdown(f"""
        <div style='text-align:center; background:rgba(255,214,0,0.1); border:2px solid #FFD600; border-radius:15px; padding:20px; box-shadow: 0 0 15px rgba(255,214,0,0.2);'>
            <div style='color:#FFD600; font-weight:900; font-size:1.1rem; margin-bottom:5px;'>💰 총 상금 (POT)</div>
            <div style='color:#FFFFFF; font-size:1.8rem; font-weight:900;'>{format_korean_money(state['pot'])}</div>
            <div style='color:#888; font-size:0.85rem; margin-top:10px;'>현재 스테이지: <b style='color:#00E5FF;'>{state['stage'].upper()}</b></div>
        </div>
        """, unsafe_allow_html=True)

    with c_me:
        st.markdown("<h4 style='color:#00E5FF; text-align:center;'>😎 나의 패</h4>", unsafe_allow_html=True)
        player_html = "<div style='text-align:center;'>" + "".join([card_html(c) for c in state['player_hand']]) + "</div>"
        st.markdown(player_html, unsafe_allow_html=True)
        
        my_score = get_best_hand(state['player_hand'] + state['community'])[0]
        st.markdown(f"""
        <div style='text-align:center; background:rgba(0,229,255,0.1); border:1px solid #00E5FF; padding:10px; margin-top:10px; border-radius:8px;'>
            <span style='color:#94A3B8; font-size:0.8rem;'>현재 내 예상 족보</span><br>
            <b style='color:#00E5FF; font-size:1.2rem;'>{HAND_NAMES[my_score]}</b>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    st.markdown("<h4 style='text-align:center; color:#E2E8F0;'>🌐 바닥 패 (Community)</h4>", unsafe_allow_html=True)
    if state['community']:
        comm_html = "<div style='text-align:center; margin-bottom:20px;'>" + "".join([card_html(c) for c in state['community']]) + "</div>"
        st.markdown(comm_html, unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center; color:#64748B; padding:30px; font-style:italic;'>아직 바닥에 카드가 깔리지 않았습니다.</div>", unsafe_allow_html=True)

    st.write("---")

    # ── 액션 버튼 (게임 진행 중) ─────────────────
    if not state['game_over']:
        st.markdown("### ⚡ 당신의 차례입니다!")
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("🏳️ 폴드 (기권)", use_container_width=True):
                state['result'] = 'lose'
                state['game_over'] = True
                st.rerun()

        with b2:
            diff_to_call = state['dealer_bet'] - state['player_bet']
            btn_txt = "체크 (패스)" if diff_to_call == 0 else f"콜 (+{format_korean_money(diff_to_call)})"
            
            if st.button(f"👌 {btn_txt}", use_container_width=True):
                if diff_to_call > 0:
                    u_fresh = load_db(USERS_FILE, {})
                    db_cash = u_fresh.get(uid, {}).get('cash', 0)
                    if db_cash < diff_to_call:
                        st.error("잔액이 부족하여 콜을 받을 수 없습니다!")
                        st.stop()
                    u_fresh[uid]['cash'] = db_cash - diff_to_call
                    save_db(USERS_FILE, u_fresh)
                    
                    st.session_state.global_cash -= diff_to_call
                    state['player_bet'] += diff_to_call
                    state['pot'] += diff_to_call
                    
                advance_stage(state)
                sync_user_data()
                st.rerun()

        with b3:
            raise_cost = (state['dealer_bet'] - state['player_bet']) + BET_UNIT
            if st.button(f"🔥 레이즈 (+{format_korean_money(raise_cost)})", use_container_width=True, type="primary"):
                u_fresh = load_db(USERS_FILE, {})
                db_cash = u_fresh.get(uid, {}).get('cash', 0)
                
                if db_cash < raise_cost:
                    st.error("잔액이 부족하여 베팅할 수 없습니다!")
                    st.stop()
                    
                u_fresh[uid]['cash'] = db_cash - raise_cost
                save_db(USERS_FILE, u_fresh)
                st.session_state.global_cash -= raise_cost
                state['player_bet'] += raise_cost
                state['pot'] += raise_cost
                sync_user_data()

                action = dealer_action(state)

                if action == 'fold':
                    # 🛠️ [수정] 딜러의 반응을 state 변수에 저장하여 증발 방지
                    state['dealer_msg'] = "🏃 딜러가 당신의 강력한 베팅에 쫄아서 기권(폴드)했습니다!"
                    state['result'] = 'win'
                    state['game_over'] = True
                elif action == 'call':
                    state['dealer_msg'] = "👌 딜러가 당신의 레이즈를 콜(수락)했습니다!"
                    state['dealer_bet'] += BET_UNIT
                    state['pot'] += BET_UNIT
                    advance_stage(state)
                    
                st.rerun()

    # ── 게임 결과 처리 (게임 종료) ─────────────────
    else:
        st.markdown("### 🏁 쇼다운! (결과)")
        
        if state['result'] is None:
            p_score_val, p_ordered = get_best_hand(state['player_hand'] + state['community'])
            d_score_val, d_ordered = get_best_hand(state['dealer_hand'] + state['community'])

            if p_score_val > d_score_val:
                state['result'] = 'win'
            elif p_score_val < d_score_val:
                state['result'] = 'lose'
            else:
                if p_ordered > d_ordered:
                    state['result'] = 'win'
                elif p_ordered < d_ordered:
                    state['result'] = 'lose'
                else:
                    state['result'] = 'draw'

        if not state['reward_claimed']:
            state['reward_claimed'] = True
            u_fresh = load_db(USERS_FILE, {})
            
            if state['result'] == 'win':
                prize = state['pot']
                u_fresh[uid]['cash'] += prize
                log_tx(uid, "홀덤", "승리 (팟 전체 획득)", prize)
            elif state['result'] == 'draw':
                prize = state['pot'] // 2
                u_fresh[uid]['cash'] += prize
                log_tx(uid, "홀덤", "무승부 (베팅금 반환)", prize)
            else:
                # ✅ [BUG FIX] 패배 시 손실액을 음수로 기록 (기존: 0으로 기록하여 txlog에서 확인 불가)
                log_tx(uid, "홀덤", "패배 (팟 잃음)", -state['base_bet'])
                
            save_db(USERS_FILE, u_fresh)
            st.session_state.global_cash = u_fresh[uid]['cash']
            sync_user_data()

        if state['result'] == 'win':
            st.success(f"🎉 승리! 딜러의 돈을 쓸어 담았습니다. (+{format_korean_money(state['pot'])})")
            st.balloons()
        elif state['result'] == 'draw':
            st.info(f"🤝 무승부! 배팅금을 정확히 나눠 갖습니다. (+{format_korean_money(state['pot'] // 2)})")
        else:
            st.error(f"💀 패배... 딜러가 상금을 모두 가져갑니다.")

        st.write("---")
        
        if st.button("🔄 다음 판 플레이", use_container_width=True, type="primary"):
            st.session_state.holdem['rematch_ready'] = True
            st.rerun()
