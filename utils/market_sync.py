# utils/market_sync.py  — 고도화 시장 시뮬레이터
# 변경 요약:
#   · 섹터 모멘텀 (연속 상승/하락 편향)
#   · 뉴스 이벤트 → 2~4 연속 틱 동안 가격 영향 지속
#   · 급등락 이벤트 (서킷브레이커 연출용 큰 임팩트)
#   · 코인 변동성 개선 (고변동 코인 별도 알고리즘)
#   · 기존 대출이자 / 로또 / 부동산 리셋 로직 완전 보존
import time
import random
import math
import streamlit as st
from utils.config import stock_config, CRYPTO_CONFIG, USERS_FILE, MARKET_FILE
from utils.database import load_db, save_db, log_tx, save_market, atomic_add_cash
from utils.core import get_net_worth, sync_user_data, get_market, format_korean_money

# ────────────────────────────────────────────────────────────────────────────
# 뉴스 풀 (랜덤 선택)
# ────────────────────────────────────────────────────────────────────────────
_NEWS_UP = [
    "{nm} 호재! 기관 대규모 순매수 포착",
    "{nm} 깜짝 실적 발표… 어닝 서프라이즈",
    "{nm} 신사업 진출 소식에 매수세 급증",
    "{nm} 외국인 연속 순매수 {day}일째",
    "{nm} 대규모 자사주 매입 공시",
    "🚀 {nm} 상한가 근접! 시장 과열 경고",
    "{nm} 글로벌 파트너십 체결 발표",
]
_NEWS_DOWN = [
    "{nm} 악재 공시… 투자심리 급랭",
    "{nm} 외국인 연속 순매도 {day}일째",
    "{nm} 실적 쇼크… 어닝 미스",
    "⚠️ {nm} 하한가 경고! 공매도 급증",
    "{nm} 주요 임원 지분 매각 공시",
    "{nm} 경쟁사 신제품 발표로 매물 폭탄",
    "{nm} 시장 신뢰도 하락… 하락세 지속",
]
_NEWS_NEUTRAL = [
    "📊 시장 개요: 대형주 혼조세 속 거래량 증가",
    "🏦 한국은행 기준금리 동결… 시장 안도",
    "📈 코스피 박스권 탈출 시도… 투자자 주목",
    "🌏 글로벌 경기 불확실성 속 방어주 강세",
    "💹 외환시장 안정… 수출주 반등 기대",
]


def _pick_news(name, impact):
    day = random.randint(2, 9)
    if impact > 0.08:
        pool = _NEWS_UP
    elif impact < -0.08:
        pool = _NEWS_DOWN
    elif abs(impact) < 0.03:
        return random.choice(_NEWS_NEUTRAL)
    else:
        pool = _NEWS_UP if impact > 0 else _NEWS_DOWN
    return random.choice(pool).format(nm=name, day=day)


# ────────────────────────────────────────────────────────────────────────────
# 주가 1틱 업데이트 — 섹터 모멘텀 + 이벤트 편향 포함
# ────────────────────────────────────────────────────────────────────────────
def _tick_stock(market, s):
    """단일 종목 1틱 처리. market dict를 직접 수정."""
    curr  = market['stock_data'][s['id']]
    base  = s.get('base_price', 80_000)
    floor = base * 0.05

    # ── 기본 랜덤 변동 ──
    vol     = s['vol']
    # 정규분포 기반 변동 (가우시안이 더 자연스러움)
    raw_ch  = random.gauss(0, vol * 0.6)
    raw_ch  = max(-vol * 1.8, min(vol * 1.8, raw_ch))   # 극단값 클램프

    # ── 섹터 모멘텀 (연속 상승/하락 편향) ──
    hist    = curr['history']
    if len(hist) >= 3:
        recent = [hist[-1] - hist[-2], hist[-2] - hist[-3]]
        mom    = sum(1 if v > 0 else -1 for v in recent) / 2   # -1 ~ +1
        raw_ch += mom * vol * 0.25   # 모멘텀 편향 추가

    # ── 이벤트 영향 (뉴스 발생 후 지속 틱) ──
    event_impact = market.get('event_impact', {}).get(s['id'], 0)
    if abs(event_impact) > 0.001:
        raw_ch += event_impact
        # 매 틱 마다 감쇠 (절반씩)
        market.setdefault('event_impact', {})[s['id']] = event_impact * 0.5
        if abs(market['event_impact'][s['id']]) < 0.002:
            market['event_impact'][s['id']] = 0

    # ── 평균 회귀 (가격이 기준가의 3배 이상이면 하락 편향) ──
    ratio = curr['price'] / base
    if ratio > 3.0:
        raw_ch -= vol * 0.3
    elif ratio < 0.2:
        raw_ch += vol * 0.3

    new_price = round(max(floor, curr['price'] * (1 + raw_ch)))
    curr['price'] = new_price
    curr['history'].append(new_price)
    if len(curr['history']) > 60:
        curr['history'].pop(0)


# ────────────────────────────────────────────────────────────────────────────
# 코인 1틱 업데이트
# ────────────────────────────────────────────────────────────────────────────
def _tick_coin(market, c):
    curr  = market['crypto_data'][c['id']]
    vol   = c['vol']
    base  = c.get('base_price', 1)
    floor = base * 0.001

    # 고변동 코인 (vol > 0.2)은 점프 확률 추가
    raw_ch = random.gauss(0, vol * 0.55)
    if vol > 0.2 and random.random() < 0.05:
        raw_ch += random.choice([-1, 1]) * random.uniform(vol, vol * 2.5)
    raw_ch = max(-vol * 2.2, min(vol * 2.2, raw_ch))

    new_price = max(floor, round(curr['price'] * (1 + raw_ch), 6))
    curr['price'] = new_price
    curr['history'].append(new_price)
    if len(curr['history']) > 60:
        curr['history'].pop(0)


# ────────────────────────────────────────────────────────────────────────────
# 메인 시장 동기화 함수
# ────────────────────────────────────────────────────────────────────────────
def run_market_sync():
    market = get_market()
    cur_t  = time.time()
    m_up   = False

    # ── 부동산 강제 리셋 감지 ──
    if 'logged_in_user' in st.session_state:
        if st.session_state.get('last_estate_reset', 0) < market.get('force_estate_reset', 0):
            st.session_state.real_estate = {}
            st.session_state.rent_time   = cur_t
            st.session_state.last_estate_reset = market.get('force_estate_reset', 0)
            sync_user_data()

    # ── 주식 시뮬레이션 ──
    if 'last_tick' not in market:
        market['last_tick'] = cur_t - 10
        m_up = True

    stock_passed = cur_t - market['last_tick']
    s_ticks      = min(int(stock_passed / 10), 60)

    if s_ticks > 0:
        for _ in range(s_ticks):
            for s in stock_config:
                _tick_stock(market, s)
        market['last_tick'] = cur_t
        m_up = True

    # ── 코인 시뮬레이션 ──
    if 'crypto_data' not in market:
        market['crypto_data'] = {
            c['id']: {
                "name": c['name'], "icon": c['icon'],
                "price": float(c['base_price']),
                "history": [float(c['base_price']), float(c['base_price'])]
            } for c in CRYPTO_CONFIG
        }
        m_up = True

    if 'crypto_tick' not in market:
        market['crypto_tick'] = cur_t - 6
        m_up = True

    crypto_passed = cur_t - market['crypto_tick']
    c_ticks       = min(int(crypto_passed / 5), 60)

    if c_ticks > 0:
        for _ in range(c_ticks):
            for c in CRYPTO_CONFIG:
                _tick_coin(market, c)
        market['crypto_tick'] = cur_t
        m_up = True

    # ── 이벤트 뉴스 발생 로직 (개선) ──
    if cur_t - market.get('news_time', 0) > 30:
        tid        = market.get('next_news_target', stock_config[0]['id'])
        imp        = market.get('next_news_impact', 0.0)
        t_cfg      = next((s for s in stock_config if s['id'] == tid), stock_config[0])
        t_nm       = market['stock_data'][tid]['name']

        # 즉시 가격 반영
        old_p  = market['stock_data'][tid]['price']
        new_p  = round(max(old_p * 0.05, old_p * (1 + imp)))
        market['stock_data'][tid]['price'] = new_p
        market['stock_data'][tid]['history'].append(new_p)
        if len(market['stock_data'][tid]['history']) > 60:
            market['stock_data'][tid]['history'].pop(0)

        # 이벤트 잔향 (다음 2~4 틱 동안 편향)
        residual = imp * 0.3
        market.setdefault('event_impact', {})[tid] = residual

        # 뉴스 텍스트
        market['news']      = _pick_news(t_nm, imp)
        market['news_time'] = cur_t

        # 다음 이벤트 스케줄
        # 급등락 이벤트: 5% 확률로 큰 임팩트 (-25% ~ +25%)
        if random.random() < 0.05:
            market['next_news_impact'] = random.choice([-1, 1]) * random.uniform(0.15, 0.25)
        else:
            market['next_news_impact'] = random.uniform(-0.12, 0.12)
        market['next_news_target'] = random.choice(stock_config)['id']
        m_up = True

    # ── 로또 당첨 ──
    if cur_t - market.get('lotto_last_draw', 0) > 3600:
        if market.get('lotto_tickets'):
            users_list   = list(market['lotto_tickets'].keys())
            weights_list = list(market['lotto_tickets'].values())
            win   = random.choices(users_list, weights=weights_list, k=1)[0]
            prize = market['lotto_pool']
            us_check = load_db(USERS_FILE, {})
            if win in us_check:
                atomic_add_cash(win, prize)
                log_tx(win, "로또당첨", "글로벌 로또 1등 잭팟!!", prize)
                if 'logged_in_user' in st.session_state and st.session_state.logged_in_user == win:
                    st.session_state.global_cash += prize
            market['news']         = f"🎊 [당첨 확정] {win}님이 대박 상금을 수령하셨습니다!!"
            market['lotto_pool']   = 5_000_000_000
            market['lotto_tickets'] = {}
        market['lotto_last_draw'] = cur_t
        m_up = True

    # ── 대출 이자 ──
    if 'logged_in_user' in st.session_state and st.session_state.loan > 0:
        try:
            _u_fresh   = load_db(USERS_FILE, {})
            _uid_      = st.session_state.logged_in_user
            _u_data    = _u_fresh.get(_uid_, {})
            db_loan    = _u_data.get('loan', 0)
            db_loan_t  = _u_data.get('loan_time', cur_t)
            ref_loan_t = max(st.session_state.loan_time, db_loan_t)
            ref_loan   = max(st.session_state.loan, db_loan)
            elapsed    = cur_t - ref_loan_t
            cyc        = min(int(elapsed / 10), 30)
            if cyc > 0:
                old_loan = ref_loan
                new_loan = min(int(ref_loan * (1.02 ** cyc)), 999_999_999_999_999)
                st.session_state.loan      = new_loan
                st.session_state.loan_time = ref_loan_t + cyc * 10
                added = new_loan - old_loan
                if added > 0:
                    st.warning(f"⚠️ 오프라인 동안 대출 이자 {format_korean_money(added)}이 붙었습니다!")
                sync_user_data()
        except Exception:
            pass

    if m_up:
        save_market(market)
    return market
