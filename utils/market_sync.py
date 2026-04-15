# utils/market_sync.py
import time
import random
import streamlit as st
from utils.config import *
from utils.database import load_db, save_db, log_tx
from utils.core import get_net_worth, sync_user_data, get_market, save_market

def run_market_sync():
    market = get_market()
    cur_t  = time.time()
    m_up   = False

    # 부동산 초기화 감지
    if 'logged_in_user' in st.session_state:
        if st.session_state.get('last_estate_reset', 0) < market.get('force_estate_reset', 0):
            st.session_state.real_estate = {}
            st.session_state.rent_time = cur_t
            st.session_state.last_estate_reset = market.get('force_estate_reset', 0)
            sync_user_data()

    # 주식 시뮬레이션 (최대 60틱 보정)
    if 'last_tick' not in market:
        market['last_tick'] = cur_t - 10
        m_up = True
        
    stock_passed = cur_t - market['last_tick']
    s_ticks = min(int(stock_passed / 10), 60)
    if s_ticks > 0:
        for _ in range(s_ticks):
            for s in stock_config:
                curr = market['stock_data'][s['id']]
                ch = (random.random() - 0.5) * 2 * s['vol']
                curr['price'] = round(max(1_000, curr['price'] * (1 + ch)))
                curr['history'].append(curr['price'])
                if len(curr['history']) > 60: curr['history'].pop(0)
        market['last_tick'] = cur_t
        m_up = True

    # 🪙 코인 시장 시뮬레이션 (수정된 부분: 얼어붙은 타이머 강제 가동)
    if 'crypto_data' not in market:
        # 최초 생성 시 history에 값이 2개 있어야 0.00% 오류가 안 남
        market['crypto_data'] = {c['id']: {"name": c['name'], "icon": c['icon'], "price": float(c['base_price']), "history": [float(c['base_price']), float(c['base_price'])]} for c in CRYPTO_CONFIG}
        m_up = True
        
    if 'crypto_tick' not in market:
        market['crypto_tick'] = cur_t - 6 # 강제로 1틱(5초) 이상 지나게 만듦
        m_up = True

    crypto_passed = cur_t - market['crypto_tick']
    c_ticks = min(int(crypto_passed / 5), 60)
    
    if c_ticks > 0:
        for _ in range(c_ticks):
            for c in CRYPTO_CONFIG:
                curr = market['crypto_data'][c['id']]
                ch = (random.random() - 0.5) * 2 * c['vol']
                curr['price'] = max(0.01, round(curr['price'] * (1 + ch), 6))
                curr['history'].append(curr['price'])
                if len(curr['history']) > 60: curr['history'].pop(0)
        market['crypto_tick'] = cur_t
        m_up = True

    # 뉴스 발생 로직
    if cur_t - market.get('news_time', 0) > 30:
        tid, imp = market['next_news_target'], market['next_news_impact']
        t_nm = next((s['name'] for s in stock_config if s['id'] == tid), tid)
        market['stock_data'][tid]['price'] = int(market['stock_data'][tid]['price'] * (1 + imp))
        direction = "급등" if imp > 0.1 else "강세" if imp > 0 else "급락" if imp < -0.1 else "약세"
        market['news'] = f"📰 {t_nm} 장중 {direction}!"
        market['news_time'] = cur_t
        market['next_news_target'] = random.choice(stock_config)['id']
        market['next_news_impact'] = random.uniform(-0.25, 0.25)
        m_up = True

    # 로또 당첨 로직
    if cur_t - market.get('lotto_last_draw', 0) > 3600:
        if market.get('lotto_tickets'):
            pool = []
            for u, c in market['lotto_tickets'].items(): pool.extend([u] * c)
            win, prize = random.choice(pool), market['lotto_pool']
            us = load_db(USERS_FILE, {})
            if win in us:
                us[win]['cash'] += prize
                save_db(USERS_FILE, us)
                log_tx(win, "로또당첨", f"글로벌 로또 1등 잭팟!!", prize)
            market['news'] = f"🎊 [당첨 확정] {win}님이 대박 상금을 수령하셨습니다!!"
            market['lotto_pool'] = 5_000_000_000
            market['lotto_tickets'] = {}
        market['lotto_last_draw'] = cur_t
        m_up = True

    # 대출 이자 폭탄 (오프라인 보정)
    if 'logged_in_user' in st.session_state and st.session_state.loan > 0:
        elapsed = cur_t - st.session_state.loan_time
        cyc = min(int(elapsed / 10), 30)
        if cyc > 0:
            st.session_state.loan = min(int(st.session_state.loan * (1.02 ** cyc)), 999_999_999_999_999)
            st.session_state.loan_time += cyc * 10
            sync_user_data()

    if m_up: save_market(market)
    return market
