# pages/pet.py
import streamlit as st
import time
import random
from datetime import datetime
from utils.config import KST, USERS_FILE
from utils.core import format_korean_money, sync_user_data
from utils.database import load_db, save_db, atomic_add_cash, atomic_deduct_cash, log_tx

# ══════════════════════════════════════════════════════════
# 🐾 펫 데이터 설정
# ══════════════════════════════════════════════════════════

PET_SPECIES = {
    "dragon":   {"name": "드래곤",     "egg": "🥚", "baby": "🐉", "adult": "🐲", "legend": "🌌",
                 "desc": "불을 내뿜는 전설의 드래곤. 성장하면 막대한 수익을!",
                 "price": 500_000_000, "rarity": "전설", "rarity_color": "#FF00FF"},
    "wolf":     {"name": "황금 늑대",  "egg": "🥚", "baby": "🐺", "adult": "🦊", "legend": "⭐",
                 "desc": "황금빛 모피를 가진 신비로운 늑대. 광산 보너스!",
                 "price": 100_000_000, "rarity": "희귀", "rarity_color": "#FFD600"},
    "penguin":  {"name": "황제 펭귄",  "egg": "🥚", "baby": "🐧", "adult": "🐧", "legend": "👑",
                 "desc": "남극의 황제. 주식 투자 시 행운을 가져다준다.",
                 "price": 50_000_000,  "rarity": "고급", "rarity_color": "#00E5FF"},
    "cat":      {"name": "럭키 고양이","egg": "🥚", "baby": "🐱", "adult": "🐈", "legend": "🍀",
                 "desc": "행운을 부르는 신비로운 고양이. 퀘스트 보너스!",
                 "price": 10_000_000,  "rarity": "일반", "rarity_color": "#00FF88"},
    "unicorn":  {"name": "유니콘",     "egg": "🥚", "baby": "🦄", "adult": "🦄", "legend": "🌈",
                 "desc": "무지개빛 유니콘. 코인 거래에 특별 보너스!",
                 "price": 200_000_000, "rarity": "영웅", "rarity_color": "#FF9500"},
    "phoenix":  {"name": "불사조",     "egg": "🔥", "baby": "🐦", "adult": "🦅", "legend": "🌟",
                 "desc": "죽어서도 다시 태어나는 불사의 새. 강화 보너스!",
                 "price": 300_000_000, "rarity": "영웅", "rarity_color": "#FF9500"},
    "slime":    {"name": "황금 슬라임","egg": "🟡", "baby": "🫧", "adult": "💛", "legend": "💰",
                 "desc": "돈을 먹고 자라는 슬라임. 패시브 수입 증가!",
                 "price": 30_000_000,  "rarity": "고급", "rarity_color": "#00E5FF"},
    "fox":      {"name": "구미호",     "egg": "🥚", "baby": "🦊", "adult": "🦊", "legend": "🌙",
                 "desc": "아홉 꼬리를 가진 신비로운 여우. 도박 보너스!",
                 "price": 150_000_000, "rarity": "희귀", "rarity_color": "#FFD600"},
}

PET_FOOD = {
    "kibble":   {"name": "일반 사료",    "icon": "🍖", "price": 500_000,    "exp": 10,  "happiness": 5},
    "gourmet":  {"name": "고급 사료",    "icon": "🥩", "price": 2_000_000,  "exp": 40,  "happiness": 15},
    "premium":  {"name": "프리미엄 사료","icon": "🍗", "price": 8_000_000,  "exp": 100, "happiness": 30},
    "stardust":  {"name": "별의 가루",   "icon": "✨", "price": 50_000_000, "exp": 500, "happiness": 50},
}

PET_ACCESSORIES = {
    "collar":  {"name": "황금 목걸이", "icon": "📿", "price": 20_000_000,  "desc": "행운 +5%",    "bonus_type": "luck",    "bonus": 5},
    "hat":     {"name": "왕관 모자",   "icon": "👑", "price": 50_000_000,  "desc": "EXP +10%",   "bonus_type": "exp",     "bonus": 10},
    "armor":   {"name": "미스릴 갑옷", "icon": "🛡️", "price": 100_000_000, "desc": "수입 +8%",   "bonus_type": "income",  "bonus": 8},
    "wings":   {"name": "불사의 날개", "icon": "🦋", "price": 200_000_000, "desc": "행복도 유지", "bonus_type": "happy",   "bonus": 20},
    "gem":     {"name": "드래곤 젬",   "icon": "💎", "price": 500_000_000, "desc": "모든 보너스+5%","bonus_type":"all",    "bonus": 5},
}

# 펫 스킬 (레벨별 해금)
PET_SKILLS = [
    {"level": 5,  "icon": "💤", "name": "낮잠",        "desc": "HP 자동 회복"},
    {"level": 10, "icon": "⚡", "name": "번개 질주",   "desc": "EXP 획득 +20%"},
    {"level": 15, "icon": "🔮", "name": "예지력",      "desc": "퀘스트 보상 +10%"},
    {"level": 20, "icon": "💰", "name": "황금 손",     "desc": "패시브 수입 발생"},
    {"level": 25, "icon": "🌟", "name": "별빛 오라",   "desc": "행운 대폭 상승"},
    {"level": 30, "icon": "🌌", "name": "우주 의지",   "desc": "모든 능력치 +30%"},
    {"level": 40, "icon": "👑", "name": "전설 각성",   "desc": "외형 전설 변환"},
    {"level": 50, "icon": "🌠", "name": "신의 은총",   "desc": "모든 보너스 2배"},
]

# 미니게임: 펫 훈련
TRAINING_GAMES = [
    {"id": "memory",    "icon": "🧠", "name": "기억력 훈련", "desc": "순서를 기억하라!", "exp_reward": 30,  "cost": 1_000_000},
    {"id": "speed",     "icon": "⚡", "name": "반응속도 훈련","desc": "빠르게 클릭!",     "exp_reward": 20,  "cost": 500_000},
    {"id": "strength",  "icon": "💪", "name": "체력 훈련",   "desc": "버튼을 연타하라!", "exp_reward": 25,  "cost": 800_000},
    {"id": "agility",   "icon": "🏃", "name": "민첩 훈련",   "desc": "미로를 빠져나가라!","exp_reward": 40,  "cost": 1_500_000},
]

EXP_PER_LEVEL = 200  # 레벨당 필요 EXP

def get_pet_sprite(species_id, level):
    sp = PET_SPECIES.get(species_id, PET_SPECIES['cat'])
    if level >= 40:   return sp['legend']
    elif level >= 20: return sp['adult']
    elif level >= 5:  return sp['baby']
    else:             return sp['egg']

def default_pet():
    return {
        "species": None,
        "name": "",
        "level": 0,
        "exp": 0,
        "happiness": 100,
        "hunger": 100,
        "hp": 100,
        "accessories": [],
        "skills": [],
        "last_fed": 0,
        "last_played": 0,
        "passive_collected": 0,
        "birth_date": "",
        "total_fed": 0,
    }

def load_pet(uid, users=None):
    if users is None:
        users = load_db(USERS_FILE, {})
    u = users.get(uid, {})
    return u.get('pet', default_pet())

def save_pet(uid, pet_data):
    users = load_db(USERS_FILE, {})
    if uid not in users:
        return
    users[uid]['pet'] = pet_data
    save_db(USERS_FILE, users)

def decay_stats(pet):
    """시간 경과에 따른 허기/행복도 감소"""
    now = time.time()
    last_fed   = pet.get('last_fed', now)
    last_played = pet.get('last_played', now)
    hours_since_fed   = (now - last_fed)   / 3600
    hours_since_played = (now - last_played) / 3600
    # 1시간마다 허기 5 감소, 행복도 3 감소
    hunger_decay  = int(hours_since_fed   * 5)
    happy_decay   = int(hours_since_played * 3)
    pet['hunger']    = max(0, pet.get('hunger', 100)    - hunger_decay)
    pet['happiness'] = max(0, pet.get('happiness', 100) - happy_decay)
    if pet['hunger'] < 20:
        pet['hp'] = max(0, pet.get('hp', 100) - int(hours_since_fed * 2))
    return pet

def add_exp(pet, exp_amount):
    acc_bonus = 0
    for acc_id in pet.get('accessories', []):
        acc = PET_ACCESSORIES.get(acc_id, {})
        if acc.get('bonus_type') in ('exp', 'all'):
            acc_bonus += acc.get('bonus', 0)
    exp_with_bonus = int(exp_amount * (1 + acc_bonus / 100))
    pet['exp'] = pet.get('exp', 0) + exp_with_bonus
    leveled_up = False
    while pet['exp'] >= EXP_PER_LEVEL:
        pet['exp'] -= EXP_PER_LEVEL
        pet['level'] = pet.get('level', 0) + 1
        pet['hp'] = min(100, pet.get('hp', 100) + 10)
        leveled_up = True
        new_skills = [s['name'] for s in PET_SKILLS if s['level'] == pet['level']]
        for s in new_skills:
            if s not in pet.get('skills', []):
                pet.setdefault('skills', []).append(s)
    return pet, leveled_up, exp_with_bonus

def get_passive_income(pet):
    lv = pet.get('level', 0)
    if lv < 20: return 0
    base = lv * 1_000_000
    for acc_id in pet.get('accessories', []):
        acc = PET_ACCESSORIES.get(acc_id, {})
        if acc.get('bonus_type') in ('income', 'all'):
            base = int(base * (1 + acc.get('bonus', 0) / 100))
    return base

# ══════════════════════════════════════════════════════════
# 메인 렌더
# ══════════════════════════════════════════════════════════
def render(market, nw):
    st.title("🐾 펫 키우기")
    uid = st.session_state.logged_in_user

    users = load_db(USERS_FILE, {})
    pet   = load_pet(uid, users)

    # ── 시간 경과 스탯 감소 처리
    if pet.get('species'):
        pet = decay_stats(pet)

    # ── 패시브 수입 수령
    passive = get_passive_income(pet)
    if passive > 0 and pet.get('species'):
        last_col = pet.get('passive_collected', time.time())
        elapsed  = time.time() - last_col
        earned   = int(passive * elapsed / 3600)  # 시간당 수입
        if earned > 0:
            pet['passive_collected'] = time.time()
            save_pet(uid, pet)
            atomic_add_cash(uid, earned)
            st.session_state.global_cash += earned
            st.toast(f"🐾 {pet.get('name','펫')}이(가) {format_korean_money(earned)} 벌어왔어요!", icon="💰")

    # ══════════════════════════════════════════════════════
    # 펫이 없으면 입양 화면
    # ══════════════════════════════════════════════════════
    if not pet.get('species'):
        st.markdown("""
        <div style='text-align:center;padding:40px;background:rgba(255,255,255,0.03);
                    border:1px solid rgba(0,229,255,0.2);border-radius:20px;margin-bottom:24px;'>
            <div style='font-size:5rem;margin-bottom:16px;'>🐾</div>
            <div style='font-size:1.5rem;font-weight:900;color:#E2E8F0;margin-bottom:8px;'>아직 펫이 없어요!</div>
            <div style='color:#64748B;'>아래에서 마음에 드는 펫을 입양해보세요.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏪 펫 입양소")
        sp_cols = st.columns(4)
        for i, (sp_id, sp) in enumerate(PET_SPECIES.items()):
            with sp_cols[i % 4]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                            border-radius:14px;padding:16px;text-align:center;margin-bottom:8px;'>
                    <div style='font-size:3rem;margin-bottom:8px;'>{sp['baby']}</div>
                    <div style='font-size:1rem;font-weight:900;color:#E2E8F0;'>{sp['name']}</div>
                    <div style='font-size:0.7rem;color:{sp["rarity_color"]};margin-top:2px;'>
                        ★ {sp['rarity']}
                    </div>
                    <div style='font-size:0.75rem;color:#64748B;margin:8px 0;'>{sp['desc']}</div>
                    <div style='color:#FFD600;font-weight:900;'>{format_korean_money(sp['price'])}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"입양하기", key=f"adopt_{sp_id}", use_container_width=True):
                    if st.session_state.global_cash < sp['price']:
                        st.error(f"현금 부족! {format_korean_money(sp['price'])} 필요")
                    else:
                        # 이름 입력을 위한 세션 세팅
                        st.session_state['adopting_pet'] = sp_id
                        st.rerun()

        # 이름 입력 다이얼로그
        if st.session_state.get('adopting_pet'):
            sp_id = st.session_state['adopting_pet']
            sp    = PET_SPECIES[sp_id]
            st.markdown(f"### 🎉 {sp['name']} 입양 중...")
            pet_name = st.text_input("펫 이름을 지어주세요!", max_chars=12, placeholder="최대 12자")
            c1, c2 = st.columns(2)
            if c1.button("✅ 입양 확정!", use_container_width=True):
                if not pet_name.strip():
                    st.error("이름을 입력해주세요!")
                else:
                    new_pet = default_pet()
                    new_pet['species']   = sp_id
                    new_pet['name']      = pet_name.strip()
                    new_pet['level']     = 1
                    new_pet['birth_date'] = datetime.now(KST).strftime("%Y-%m-%d")
                    new_pet['last_fed']  = time.time()
                    new_pet['last_played'] = time.time()
                    new_pet['passive_collected'] = time.time()
                    st.session_state.global_cash -= sp['price']
                    save_pet(uid, new_pet)
                    sync_user_data()
                    log_tx(uid, "펫", f"{pet_name} ({sp['name']}) 입양", -sp['price'])
                    del st.session_state['adopting_pet']
                    st.toast(f"🐾 {pet_name} 입양 완료!", icon="🎉")
                    st.balloons()
                    st.rerun()
            if c2.button("❌ 취소", use_container_width=True):
                del st.session_state['adopting_pet']
                st.rerun()
        return

    # ══════════════════════════════════════════════════════
    # 펫 메인 화면
    # ══════════════════════════════════════════════════════
    sp     = PET_SPECIES.get(pet['species'], PET_SPECIES['cat'])
    sprite = get_pet_sprite(pet['species'], pet['level'])
    lv     = pet.get('level', 1)
    exp    = pet.get('exp', 0)
    hunger = pet.get('hunger', 100)
    happy  = pet.get('happiness', 100)
    hp     = pet.get('hp', 100)
    exp_pct = int(exp / EXP_PER_LEVEL * 100)

    # 상태 컬러
    hunger_col = "#FF4B4B" if hunger < 30 else "#FFD600" if hunger < 60 else "#00FF88"
    happy_col  = "#FF4B4B" if happy < 30  else "#FFD600" if happy < 60  else "#00FF88"
    hp_col     = "#FF4B4B" if hp < 30     else "#FFD600" if hp < 60     else "#00FF88"

    # ── 메인 펫 카드
    passive_info = f"패시브 수입: {format_korean_money(passive)}/h" if passive > 0 else "Lv.20 달성 시 패시브 수입 시작"
    acc_icons = " ".join(PET_ACCESSORIES[a]['icon'] for a in pet.get('accessories', []) if a in PET_ACCESSORIES)

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0d1020,#111828);border:2px solid {sp["rarity_color"]};
                border-radius:20px;padding:28px;margin-bottom:24px;
                box-shadow:0 0 40px rgba(0,229,255,0.1);'>
        <div style='display:flex;align-items:center;gap:28px;flex-wrap:wrap;'>
            <div style='text-align:center;flex-shrink:0;'>
                <div style='font-size:6rem;'>{sprite}</div>
                <div style='color:{sp["rarity_color"]};font-size:0.75rem;font-weight:900;margin-top:4px;'>
                    ★ {sp['rarity']}
                </div>
                <div style='color:#475569;font-size:0.75rem;'>{acc_icons}</div>
            </div>
            <div style='flex:1;min-width:220px;'>
                <div style='font-size:1.8rem;font-weight:900;color:#fff;font-family:"Orbitron",monospace;'>{pet['name']}</div>
                <div style='color:#B0BAC8;font-size:0.9rem;margin-top:2px;'>{sp['name']} · 탄생일: {pet.get("birth_date","?")}</div>
                <div style='margin-top:16px;'>
                    <div style='display:flex;justify-content:space-between;margin-bottom:4px;'>
                        <span style='color:#B0BAC8;font-size:0.8rem;'>⚡ EXP</span>
                        <span style='color:#FFD600;font-size:0.8rem;font-weight:900;'>{exp}/{EXP_PER_LEVEL}</span>
                    </div>
                    <div style='background:#1E293B;border-radius:4px;height:8px;'>
                        <div style='background:linear-gradient(90deg,#FFD600,#FF9500);width:{exp_pct}%;height:100%;border-radius:4px;'></div>
                    </div>
                </div>
                <div style='color:#64748B;font-size:0.8rem;margin-top:8px;'>{passive_info}</div>
            </div>
            <div style='text-align:right;border-left:1px solid rgba(255,255,255,0.1);padding-left:24px;flex-shrink:0;'>
                <div style='font-size:2.5rem;font-weight:900;color:#FFD600;font-family:"Orbitron",monospace;'>Lv.{lv}</div>
                <div style='margin-top:12px;'>
                    <div style='color:#B0BAC8;font-size:0.75rem;'>❤️ HP</div>
                    <div style='color:{hp_col};font-weight:900;'>{hp}/100</div>
                </div>
                <div style='margin-top:6px;'>
                    <div style='color:#B0BAC8;font-size:0.75rem;'>🍖 배고픔</div>
                    <div style='color:{hunger_col};font-weight:900;'>{hunger}/100</div>
                </div>
                <div style='margin-top:6px;'>
                    <div style='color:#B0BAC8;font-size:0.75rem;'>😊 행복도</div>
                    <div style='color:{happy_col};font-weight:900;'>{happy}/100</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 경고 메시지
    if hunger < 20:
        st.warning(f"⚠️ {pet['name']}이(가) 너무 배가 고파요! 빨리 먹을 것을 주세요!")
    if happy < 20:
        st.warning(f"😢 {pet['name']}이(가) 너무 슬퍼해요! 같이 놀아주세요!")
    if hp < 30:
        st.error(f"💀 {pet['name']}의 HP가 위험해요! 먹이를 주고 쉬게 해주세요!")

    # ══════════════════════════════════════════════════════
    # 탭 메뉴
    # ══════════════════════════════════════════════════════
    tabs = st.tabs(["🍖 먹이주기", "🎮 훈련하기", "👗 아이템", "⚔️ 스킬", "🏪 분양/정보"])

    # ── 탭 1: 먹이주기
    with tabs[0]:
        st.markdown("#### 🍖 먹이 선택")
        st.markdown("<div style='color:#B0BAC8;font-size:0.85rem;margin-bottom:16px;'>먹이를 줄 수록 EXP와 행복도가 오릅니다. 배고픔이 0이 되면 HP가 감소합니다!</div>", unsafe_allow_html=True)
        food_cols = st.columns(4)
        for i, (f_id, food) in enumerate(PET_FOOD.items()):
            with food_cols[i]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                            border-radius:12px;padding:14px;text-align:center;margin-bottom:8px;'>
                    <div style='font-size:2.5rem;'>{food['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;'>{food['name']}</div>
                    <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>EXP +{food['exp']} · 행복 +{food['happiness']}</div>
                    <div style='color:#FFD600;font-weight:900;margin-top:6px;'>{format_korean_money(food['price'])}</div>
                </div>
                """, unsafe_allow_html=True)
                qty = st.number_input("수량", min_value=1, max_value=50, value=1, key=f"food_qty_{f_id}")
                if st.button(f"먹이기 ×{qty}", key=f"feed_{f_id}", use_container_width=True):
                    total_cost = food['price'] * qty
                    if st.session_state.global_cash < total_cost:
                        st.error("현금 부족!")
                    else:
                        st.session_state.global_cash -= total_cost
                        atomic_deduct_cash(uid, total_cost)
                        total_exp   = food['exp']       * qty
                        total_happy = food['happiness'] * qty
                        pet['hunger']    = min(100, pet.get('hunger', 100)    + 10 * qty)
                        pet['happiness'] = min(100, pet.get('happiness', 100) + total_happy)
                        pet['hp']        = min(100, pet.get('hp', 100)        + 5 * qty)
                        pet['last_fed']  = time.time()
                        pet['total_fed'] = pet.get('total_fed', 0) + qty
                        pet, leveled_up, gained_exp = add_exp(pet, total_exp)
                        save_pet(uid, pet)
                        sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} 먹이({food['name']}×{qty})", -total_cost)
                        st.toast(f"🍖 {food['icon']}×{qty} 먹임! EXP +{gained_exp}", icon="✅")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 {pet['name']} 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

    # ── 탭 2: 훈련
    with tabs[1]:
        st.markdown("#### 🎮 훈련 미니게임")
        st.markdown("<div style='color:#B0BAC8;font-size:0.85rem;margin-bottom:16px;'>훈련을 통해 EXP와 행복도를 올리세요! 각 훈련은 약간의 비용이 들어갑니다.</div>", unsafe_allow_html=True)

        train_cols = st.columns(2)
        for i, tg in enumerate(TRAINING_GAMES):
            with train_cols[i % 2]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
                            border-radius:12px;padding:16px;margin-bottom:12px;'>
                    <div style='display:flex;align-items:center;gap:12px;'>
                        <div style='font-size:2.5rem;'>{tg['icon']}</div>
                        <div>
                            <div style='font-weight:900;color:#E2E8F0;'>{tg['name']}</div>
                            <div style='color:#64748B;font-size:0.8rem;'>{tg['desc']}</div>
                            <div style='color:#FFD600;font-size:0.8rem;font-weight:700;'>EXP +{tg['exp_reward']} · 비용: {format_korean_money(tg['cost'])}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎮 {tg['name']} 시작!", key=f"train_{tg['id']}", use_container_width=True):
                    if st.session_state.global_cash < tg['cost']:
                        st.error("현금 부족!")
                    elif pet.get('happiness', 100) < 10:
                        st.error("행복도가 너무 낮아 훈련할 수 없어요!")
                    else:
                        st.session_state.global_cash -= tg['cost']
                        atomic_deduct_cash(uid, tg['cost'])
                        # 랜덤 성공률 (80~120%)
                        roll    = random.uniform(0.8, 1.2)
                        exp_got = int(tg['exp_reward'] * roll)
                        pet['happiness'] = max(0, pet.get('happiness', 100) - 5)
                        pet['last_played'] = time.time()
                        pet, leveled_up, gained_exp = add_exp(pet, exp_got)
                        save_pet(uid, pet)
                        sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} {tg['name']}", -tg['cost'])
                        if roll >= 1.1:
                            st.toast(f"🌟 대성공! EXP +{gained_exp}", icon="🎉")
                        else:
                            st.toast(f"✅ 훈련 완료! EXP +{gained_exp}", icon="💪")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 {pet['name']} 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

        st.write("---")
        st.markdown("#### 💝 같이 놀기 (무료)")
        st.markdown("<div style='color:#B0BAC8;font-size:0.85rem;margin-bottom:12px;'>행복도를 올려주세요! 쿨타임: 10분</div>", unsafe_allow_html=True)
        last_played = pet.get('last_played', 0)
        cooldown    = 600  # 10분
        elapsed     = time.time() - last_played
        remaining   = max(0, cooldown - elapsed)

        play_options = ["공 던지기 🎾", "숨바꼭질 🙈", "퍼즐 맞추기 🧩", "노래 부르기 🎵", "산책하기 🌿"]
        selected_play = st.selectbox("놀이 선택", play_options, key="play_select")

        if remaining > 0:
            st.info(f"⏳ 다음 놀기까지 {int(remaining//60)}분 {int(remaining%60)}초 남았어요!")
        else:
            if st.button("💝 같이 놀기!", use_container_width=True, key="play_btn"):
                play_exp   = random.randint(5, 15)
                play_happy = random.randint(15, 30)
                pet['happiness'] = min(100, pet.get('happiness', 100) + play_happy)
                pet['last_played'] = time.time()
                pet, leveled_up, gained_exp = add_exp(pet, play_exp)
                save_pet(uid, pet)
                st.toast(f"😊 {selected_play} 완료! 행복 +{play_happy}, EXP +{gained_exp}", icon="💝")
                if leveled_up:
                    st.balloons()
                    st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

    # ── 탭 3: 아이템/악세서리
    with tabs[2]:
        st.markdown("#### 👗 악세서리 상점")
        st.markdown("<div style='color:#B0BAC8;font-size:0.85rem;margin-bottom:16px;'>악세서리를 장착해 펫 능력을 강화하세요! 최대 2개 장착 가능.</div>", unsafe_allow_html=True)
        equipped = pet.get('accessories', [])

        acc_cols = st.columns(3)
        for i, (acc_id, acc) in enumerate(PET_ACCESSORIES.items()):
            is_equipped = acc_id in equipped
            with acc_cols[i % 3]:
                st.markdown(f"""
                <div style='background:{"rgba(0,229,255,0.08)" if is_equipped else "rgba(255,255,255,0.04)"};
                            border:1px solid {"#00E5FF" if is_equipped else "rgba(255,255,255,0.1)"};
                            border-radius:12px;padding:14px;text-align:center;margin-bottom:8px;'>
                    <div style='font-size:2.5rem;'>{acc['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;'>{acc['name']}</div>
                    <div style='color:#00FF88;font-size:0.8rem;margin-top:4px;'>{acc['desc']}</div>
                    <div style='color:#FFD600;font-weight:900;margin-top:8px;'>{format_korean_money(acc['price'])}</div>
                    {"<div style='color:#00E5FF;font-size:0.75rem;margin-top:4px;'>✅ 장착 중</div>" if is_equipped else ""}
                </div>
                """, unsafe_allow_html=True)
                if is_equipped:
                    if st.button("해제", key=f"unequip_{acc_id}", use_container_width=True):
                        equipped.remove(acc_id)
                        pet['accessories'] = equipped
                        save_pet(uid, pet)
                        st.toast(f"{acc['name']} 해제!", icon="✅")
                        st.rerun()
                else:
                    if st.button("구매·장착", key=f"buy_acc_{acc_id}", use_container_width=True):
                        if len(equipped) >= 2:
                            st.error("악세서리는 최대 2개까지 장착 가능합니다!")
                        elif st.session_state.global_cash < acc['price']:
                            st.error("현금 부족!")
                        else:
                            st.session_state.global_cash -= acc['price']
                            atomic_deduct_cash(uid, acc['price'])
                            equipped.append(acc_id)
                            pet['accessories'] = equipped
                            save_pet(uid, pet)
                            sync_user_data()
                            log_tx(uid, "펫", f"{pet['name']} 악세서리: {acc['name']}", -acc['price'])
                            st.toast(f"🎉 {acc['name']} 장착!", icon="✅")
                            st.rerun()

    # ── 탭 4: 스킬
    with tabs[3]:
        st.markdown("#### ⚔️ 펫 스킬")
        st.markdown("<div style='color:#B0BAC8;font-size:0.85rem;margin-bottom:16px;'>레벨을 올려 강력한 스킬을 해금하세요!</div>", unsafe_allow_html=True)
        sk_cols = st.columns(4)
        pet_skills = pet.get('skills', [])
        for i, skill in enumerate(PET_SKILLS):
            unlocked = lv >= skill['level']
            with sk_cols[i % 4]:
                st.markdown(f"""
                <div style='background:{"rgba(0,229,255,0.1)" if unlocked else "rgba(255,255,255,0.02)"};
                            border:1px solid {"#00E5FF" if unlocked else "#1E293B"};
                            border-radius:12px;padding:12px;text-align:center;margin-bottom:8px;
                            opacity:{"1" if unlocked else "0.4"}'>
                    <div style='font-size:2rem;'>{skill['icon']}</div>
                    <div style='color:#E2E8F0;font-size:0.85rem;font-weight:700;margin-top:6px;'>{skill['name']}</div>
                    <div style='color:#64748B;font-size:0.72rem;margin-top:4px;'>{skill['desc']}</div>
                    <div style='color:{"#FFD600" if unlocked else "#475569"};font-size:0.72rem;margin-top:6px;font-weight:700;'>
                        {"✅ 해금" if unlocked else f"🔒 Lv.{skill['level']} 필요"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── 탭 5: 분양/정보
    with tabs[4]:
        st.markdown("#### 📊 펫 상세 정보")
        total_fed = pet.get('total_fed', 0)
        info_rows = [
            ("🐾 종류",      sp['name']),
            ("📛 이름",      pet['name']),
            ("🎂 탄생일",    pet.get('birth_date', '?')),
            ("⚡ 레벨",      f"Lv.{lv}"),
            ("🍖 총 먹인 횟수", f"{total_fed:,}회"),
            ("💰 패시브 수입", format_korean_money(passive) + "/h" if passive > 0 else "미해금 (Lv.20~)"),
            ("👗 장착 악세서리", ", ".join(PET_ACCESSORIES[a]['name'] for a in equipped if a in PET_ACCESSORIES) or "없음"),
            ("⚔️ 보유 스킬",  ", ".join(pet_skills) or "없음"),
        ]
        for label, val in info_rows:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);'>
                <span style='color:#64748B;'>{label}</span>
                <span style='color:#E2E8F0;font-weight:700;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 🔴 펫 분양")
        st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;margin-bottom:12px;'>⚠️ 분양 시 펫이 영구히 사라집니다. 분양 보상은 입양 금액의 30%입니다.</div>", unsafe_allow_html=True)
        release_price = int(sp['price'] * 0.3)
        if st.button(f"💔 {pet['name']} 분양하기 (보상: {format_korean_money(release_price)})", key="release_pet"):
            st.session_state['confirm_release'] = True

        if st.session_state.get('confirm_release'):
            st.warning("정말 분양하시겠어요? 이 작업은 되돌릴 수 없습니다!")
            cc1, cc2 = st.columns(2)
            if cc1.button("✅ 최종 확인, 분양", use_container_width=True, key="confirm_yes"):
                st.session_state.global_cash += release_price
                atomic_add_cash(uid, release_price)
                save_pet(uid, default_pet())
                sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 분양", release_price)
                del st.session_state['confirm_release']
                st.toast(f"💔 {pet['name']}이(가) 새 주인을 찾아 떠났어요...", icon="🐾")
                st.rerun()
            if cc2.button("❌ 취소", use_container_width=True, key="confirm_no"):
                del st.session_state['confirm_release']
                st.rerun()
