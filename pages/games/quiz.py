# pages/games/quiz.py
import streamlit as st
import random
from datetime import date
from utils.core import format_korean_money, sync_user_data
from utils.database import log_tx, atomic_add_cash

# ──────────────────────────────────────────────────────────────
# 🔮 사주팔자 데이터
# ──────────────────────────────────────────────────────────────

# 12지신
ZODIAC = {
    0:  ("🐀 자(子)", "쥐"),
    1:  ("🐂 축(丑)", "소"),
    2:  ("🐅 인(寅)", "호랑이"),
    3:  ("🐇 묘(卯)", "토끼"),
    4:  ("🐉 진(辰)", "용"),
    5:  ("🐍 사(巳)", "뱀"),
    6:  ("🐎 오(午)", "말"),
    7:  ("🐑 미(未)", "양"),
    8:  ("🐒 신(申)", "원숭이"),
    9:  ("🐓 유(酉)", "닭"),
    10: ("🐕 술(戌)", "개"),
    11: ("🐖 해(亥)", "돼지"),
}

# 오행
ELEMENTS = ["🌲 목(木)", "🔥 화(火)", "🌍 토(土)", "🪙 금(金)", "💧 수(水)"]

# 천간
HEAVENLY_STEMS = ["갑(甲)", "을(乙)", "병(丙)", "정(丁)", "무(戊)",
                  "기(己)", "경(庚)", "신(辛)", "임(壬)", "계(癸)"]

# 오늘의 운세 텍스트 풀
FORTUNE_POOL = {
    "재물운": [
        "오늘은 작은 투자가 큰 수익으로 이어질 수 있는 날입니다. 단, 욕심은 금물.",
        "재물이 들어오는 기운이 있으나 지출도 많을 수 있습니다. 충동구매를 조심하세요.",
        "금전적 기회가 찾아오지만 성급히 결정하지 마세요. 신중함이 답입니다.",
        "재물운이 약한 날입니다. 오늘은 보수적으로 자산을 지키는 것이 현명합니다.",
        "예상치 못한 곳에서 수익이 발생할 수 있는 길일입니다.",
        "투자보다는 저축에 집중하는 게 좋은 날. 묵혀둔 돈이 빛을 발합니다.",
        "광산과 슬롯에서의 운이 특히 강합니다. 한 번 도전해보세요!",
        "주식 시장에서 기회를 포착할 수 있는 날. 차트를 주목하세요.",
    ],
    "애정운": [
        "소통이 원활한 날입니다. 마음속 이야기를 솔직하게 털어놓아 보세요.",
        "인연이 가까이 있습니다. 평소에 관심 있던 사람에게 먼저 다가가 보세요.",
        "오해가 생기기 쉬운 날입니다. 말 한마디에 신중을 기하세요.",
        "혼자만의 시간이 필요한 날. 관계보다는 자기 자신에게 집중하세요.",
        "오랜 인연이 다시 연결되는 기운이 있습니다.",
        "새로운 만남이 기다리고 있습니다. 적극적으로 나서보세요.",
    ],
    "건강운": [
        "과로를 피하고 충분한 수면을 취하세요. 몸이 먼저입니다.",
        "가벼운 스트레칭이나 산책으로 활력을 되찾을 수 있는 날입니다.",
        "소화기가 예민한 날. 자극적인 음식은 피하는 것이 좋습니다.",
        "컨디션이 최상인 날입니다. 오늘 하고 싶었던 활동을 즐겨보세요.",
        "정신적 피로가 쌓일 수 있습니다. 명상이나 휴식을 추천합니다.",
        "기력이 넘치는 날. 도전적인 활동에 좋은 에너지를 쓰세요.",
    ],
    "총운": [
        "오늘은 무엇이든 시작하기 좋은 날입니다. 계획을 실행에 옮겨보세요.",
        "막혔던 일들이 풀리는 기운이 있습니다. 포기하지 마세요.",
        "신중함이 필요한 날. 중요한 결정은 내일로 미루는 것도 방법입니다.",
        "주변의 도움을 받을 수 있는 날. 혼자 끌어안지 말고 협력하세요.",
        "작은 노력이 큰 결실을 맺는 날입니다. 꾸준함이 최고의 무기.",
        "뜻밖의 행운이 찾아올 수 있습니다. 열린 마음을 유지하세요.",
        "오늘은 쉬어가도 괜찮은 날. 재충전이 내일의 도약을 만듭니다.",
        "하이퍼카나 명검 강화에 도전하기 좋은 기운입니다!",
    ],
}

# 음식별 오행 매핑
FOOD_ELEMENTS = {
    "🍚 밥/국": "🌍 토(土)",
    "🍖 고기": "🔥 화(火)",
    "🥗 채소/샐러드": "🌲 목(木)",
    "🍜 라면/국수": "💧 수(水)",
    "🍣 해산물/생선": "💧 수(水)",
    "🍕 피자/빵": "🌍 토(土)",
    "🍗 치킨/튀김": "🔥 화(火)",
    "☕ 커피/음료": "🌲 목(木)",
    "🍰 디저트/과자": "🪙 금(金)",
    "🥩 스테이크": "🪙 금(金)",
    "🍱 도시락/편의점": "🌍 토(土)",
    "🍔 버거/패스트푸드": "🔥 화(火)",
}

# 오늘의 행운 아이템
LUCKY_ITEMS = [
    "🔴 빨간 물건", "💙 파란 물건", "🌿 식물", "📚 책", "💰 동전",
    "⌚ 시계", "🎵 음악", "🌊 물", "🪨 돌", "🕯️ 초", "🎋 대나무",
]

# 행운의 숫자
LUCKY_NUMBERS_POOL = list(range(1, 100))

# 별자리 (생년월일 기반)
def get_star_sign(birth_month, birth_day):
    signs = [
        (1, 20, "🏹 염소자리"), (2, 19, "🌊 물병자리"), (3, 20, "🐟 물고기자리"),
        (4, 20, "🐏 양자리"), (5, 21, "🐂 황소자리"), (6, 21, "👯 쌍둥이자리"),
        (7, 22, "🦀 게자리"), (8, 23, "🦁 사자자리"), (9, 23, "👧 처녀자리"),
        (10, 23, "⚖️ 천칭자리"), (11, 22, "🦂 전갈자리"), (12, 22, "🏹 사수자리"),
        (12, 31, "🏹 염소자리"),
    ]
    for month, day, sign in signs:
        if (birth_month, birth_day) <= (month, day):
            return sign
    return "🏹 염소자리"

def get_zodiac(birth_year):
    return ZODIAC[(birth_year - 4) % 12]

def get_element(birth_year):
    return ELEMENTS[(birth_year % 10) // 2]

def get_heavenly_stem(birth_year):
    return HEAVENLY_STEMS[birth_year % 10]

def generate_saju(name, birth_year, birth_month, birth_day, last_food):
    """입력값 기반으로 오늘의 사주 운세 생성"""
    # 시드를 오늘 날짜 + 유저 정보로 고정 (하루에 한 번 같은 결과)
    today = date.today()
    seed  = hash(f"{name}{birth_year}{birth_month}{birth_day}{today.isoformat()}")
    rng   = random.Random(seed)

    zodiac_label, zodiac_animal = get_zodiac(birth_year)
    element     = get_element(birth_year)
    stem        = get_heavenly_stem(birth_year)
    star_sign   = get_star_sign(birth_month, birth_day)
    food_element = FOOD_ELEMENTS.get(last_food, rng.choice(ELEMENTS))

    # 운세 점수 (1~5)
    scores = {cat: rng.randint(1, 5) for cat in ["재물운", "애정운", "건강운", "총운"]}
    # 음식의 오행이 태어난 해의 오행과 맞으면 재물운 +1 보너스
    if food_element == element and scores["재물운"] < 5:
        scores["재물운"] += 1

    # 운세 텍스트
    fortunes   = {cat: rng.choice(FORTUNE_POOL[cat]) for cat in FORTUNE_POOL}
    lucky_item = rng.choice(LUCKY_ITEMS)
    lucky_num  = rng.choice(LUCKY_NUMBERS_POOL)

    return {
        "zodiac": zodiac_label,
        "zodiac_animal": zodiac_animal,
        "element": element,
        "stem": stem,
        "star_sign": star_sign,
        "food_element": food_element,
        "scores": scores,
        "fortunes": fortunes,
        "lucky_item": lucky_item,
        "lucky_num": lucky_num,
    }

def star_bar(score):
    filled = "⭐" * score
    empty  = "☆" * (5 - score)
    return f"{filled}{empty}"


# ──────────────────────────────────────────────────────────────
# 🔮 메인 렌더
# ──────────────────────────────────────────────────────────────
def render(market, nw):
    st.title("🔮 오늘의 사주팔자")
    st.caption("생년월일 + 가장 최근에 먹은 음식으로 오늘 하루 운세를 봐드립니다!")

    uid = st.session_state.logged_in_user

    # ── 입력 폼 ──
    if 'saju_result' not in st.session_state:
        st.markdown("""
        <div style='background:linear-gradient(135deg,rgba(100,0,200,0.1),rgba(0,0,100,0.15));
             border:1px solid rgba(180,0,255,0.3);border-radius:14px;padding:20px;margin-bottom:20px;'>
          <div style='font-size:1.1rem;font-weight:900;color:#CC88FF;margin-bottom:8px;'>🔮 사주 정보 입력</div>
          <div style='color:#888;font-size:0.85rem;'>오늘 날짜 기준으로 사주를 분석합니다. 매일 새로운 결과가 나옵니다!</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("saju_form"):
            name       = st.text_input("이름 (닉네임 가능)", placeholder="홍길동")
            col1, col2, col3 = st.columns(3)
            with col1:
                birth_year  = st.number_input("출생 연도", min_value=1900, max_value=2010, value=2000, step=1)
            with col2:
                birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=1, step=1)
            with col3:
                birth_day   = st.number_input("출생 일", min_value=1, max_value=31, value=1, step=1)

            last_food = st.selectbox("가장 최근에 먹은 음식", list(FOOD_ELEMENTS.keys()))

            submitted = st.form_submit_button("🔮 사주 보기!", use_container_width=True)
            if submitted:
                if not name.strip():
                    st.warning("이름을 입력해주세요!")
                else:
                    result = generate_saju(name.strip(), int(birth_year), int(birth_month), int(birth_day), last_food)
                    st.session_state.saju_result = result
                    st.session_state.saju_name   = name.strip()
                    st.session_state.saju_rewarded = False
                    st.rerun()
        return

    # ── 결과 화면 ──
    result = st.session_state.saju_result
    name   = st.session_state.saju_name
    today  = date.today()

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(100,0,200,0.15),rgba(0,0,150,0.2));
         border:2px solid rgba(180,0,255,0.5);border-radius:18px;padding:24px;text-align:center;margin-bottom:24px;'>
      <div style='font-size:3rem;margin-bottom:8px;'>{result['zodiac'].split()[0]}</div>
      <div style='font-size:1.4rem;font-weight:900;color:#CC88FF;'>{name}님의 오늘의 사주</div>
      <div style='color:#888;font-size:0.82rem;margin-top:6px;'>{today.strftime("%Y년 %m월 %d일")} 기준</div>
      <div style='display:flex;justify-content:center;gap:16px;margin-top:14px;flex-wrap:wrap;'>
        <span style='background:rgba(255,215,0,0.1);border:1px solid rgba(255,215,0,0.3);border-radius:8px;padding:4px 12px;color:#FFD600;font-size:0.82rem;'>{result['zodiac']}</span>
        <span style='background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);border-radius:8px;padding:4px 12px;color:#00E5FF;font-size:0.82rem;'>{result['star_sign']}</span>
        <span style='background:rgba(0,255,136,0.1);border:1px solid rgba(0,255,136,0.3);border-radius:8px;padding:4px 12px;color:#00FF88;font-size:0.82rem;'>{result['element']}</span>
        <span style='background:rgba(255,100,100,0.1);border:1px solid rgba(255,100,100,0.3);border-radius:8px;padding:4px 12px;color:#FF8888;font-size:0.82rem;'>천간 {result['stem']}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 음식 오행 분석
    food_match = result['food_element'] == result['element']
    st.markdown(f"""
    <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 18px;margin-bottom:16px;'>
      <div style='color:#888;font-size:0.78rem;margin-bottom:6px;'>🍽️ 최근 식사의 오행 분석</div>
      <div style='color:#E2E8F0;font-size:0.9rem;'>마지막 식사의 오행: <b style='color:#FFD600;'>{result['food_element']}</b>
      {"&nbsp; ✨ <b style='color:#FFD600;'>나의 오행과 일치! 재물운 +1 보너스</b>" if food_match else ""}</div>
    </div>
    """, unsafe_allow_html=True)

    # 운세 점수표
    st.markdown("### 📊 오늘의 운세")
    for cat, score in result['scores'].items():
        score_color = "#00FF88" if score >= 4 else "#FFD600" if score == 3 else "#FF4B4B"
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
             padding:10px 14px;background:rgba(255,255,255,0.03);border-radius:8px;margin:6px 0;'>
          <span style='color:#E2E8F0;font-size:0.9rem;'>{cat}</span>
          <span style='color:{score_color};font-size:1rem;font-weight:900;'>{star_bar(score)} ({score}/5)</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 운세 상세
    st.markdown("### 🔮 상세 운세")
    for cat, text in result['fortunes'].items():
        score = result['scores'][cat]
        icon  = "🟢" if score >= 4 else "🟡" if score == 3 else "🔴"
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.03);border-left:3px solid rgba(180,0,255,0.5);
             border-radius:8px;padding:12px 16px;margin:8px 0;'>
          <div style='color:#CC88FF;font-size:0.8rem;font-weight:900;margin-bottom:4px;'>{icon} {cat}</div>
          <div style='color:#A0AEC0;font-size:0.88rem;line-height:1.6;'>{text}</div>
        </div>
        """, unsafe_allow_html=True)

    # 행운의 정보
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div style='background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.3);border-radius:10px;padding:14px;text-align:center;'>
          <div style='color:#888;font-size:0.78rem;'>오늘의 행운 아이템</div>
          <div style='color:#FFD600;font-size:1.2rem;font-weight:900;margin-top:6px;'>{result['lucky_item']}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div style='background:rgba(0,229,255,0.08);border:1px solid rgba(0,229,255,0.3);border-radius:10px;padding:14px;text-align:center;'>
          <div style='color:#888;font-size:0.78rem;'>오늘의 행운 숫자</div>
          <div style='color:#00E5FF;font-size:1.2rem;font-weight:900;margin-top:6px;'>{result['lucky_num']}</div>
        </div>
        """, unsafe_allow_html=True)

    # 총운 기반 보상 (1회 지급)
    st.write("")
    total_score = result['scores']['총운']
    if not st.session_state.get('saju_rewarded', False):
        reward_map = {5: 2_000_000, 4: 1_000_000, 3: 500_000, 2: 200_000, 1: 100_000}
        reward = reward_map[total_score]
        atomic_add_cash(uid, reward)
        st.session_state.global_cash += reward
        st.session_state.saju_rewarded = True
        log_tx(uid, "사주", f"사주 총운 {total_score}성 보상", reward)
        sync_user_data()
        st.success(f"🎁 오늘의 사주 보상: +{format_korean_money(reward)} (총운 {star_bar(total_score)})")

    st.write("")
    if st.button("🔄 다시 보기 (정보 초기화)", use_container_width=True):
        for k in ['saju_result', 'saju_name', 'saju_rewarded']:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()
