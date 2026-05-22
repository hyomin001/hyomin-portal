# pages/pet.py — MEGA ULTIMATE EDITION v4.0 🐾
# 드래곤 알 부화 / 날개짓 / 쓰다듬기 / 탐험 / 배틀 / 업적 / 일지 완전판
import streamlit as st
import streamlit.components.v1 as components
import time, random, json
from datetime import datetime, timedelta
from utils.config import KST, USERS_FILE
from utils.core import format_korean_money, sync_user_data
from utils.database import load_db, save_db, atomic_add_cash, atomic_deduct_cash, log_tx

# ══════════════════════════════════════════════════════════════════════════════
# 📦 DATA DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

PET_SPECIES = {
    "dragon":  {"name":"드래곤",    "egg":"🥚","baby":"🐉","adult":"🐲","legend":"🌌",
                "desc":"전설의 화염룡. 성장할수록 막대한 수익과 불꽃 능력을 얻는다!",
                "price":500_000_000,"rarity":"전설","rarity_color":"#FF6B00",
                "ability":"화염 브레스 — 배틀 시 추가 화염 데미지"},
    "wolf":    {"name":"황금 늑대", "egg":"🥚","baby":"🐺","adult":"🦊","legend":"⭐",
                "desc":"황금빛 모피의 신비 늑대. 광산 보너스!",
                "price":100_000_000,"rarity":"희귀","rarity_color":"#FFD600",
                "ability":"황금 발톱 — 광산 수입 +15%"},
    "penguin": {"name":"황제 펭귄", "egg":"🥚","baby":"🐧","adult":"🐧","legend":"👑",
                "desc":"남극의 황제. 주식 투자 행운!",
                "price":50_000_000,"rarity":"고급","rarity_color":"#00E5FF",
                "ability":"빙하 방패 — 배틀 방어력 +20%"},
    "cat":     {"name":"럭키 고양이","egg":"🥚","baby":"🐱","adult":"🐈","legend":"🍀",
                "desc":"행운을 부르는 신비한 고양이.",
                "price":10_000_000,"rarity":"일반","rarity_color":"#00FF88",
                "ability":"럭키 포 — 퀘스트 보상 +10%"},
    "unicorn": {"name":"유니콘",    "egg":"🥚","baby":"🦄","adult":"🦄","legend":"🌈",
                "desc":"무지개빛 유니콘. 코인 거래 보너스!",
                "price":200_000_000,"rarity":"영웅","rarity_color":"#DD00FF",
                "ability":"무지개 마법 — 코인 수익 +12%"},
    "phoenix": {"name":"불사조",    "egg":"🔥","baby":"🐦","adult":"🦅","legend":"🌟",
                "desc":"불사의 새. 강화 보너스!",
                "price":300_000_000,"rarity":"영웅","rarity_color":"#FF9500",
                "ability":"불사 재생 — HP 자동 회복 2배"},
    "slime":   {"name":"황금 슬라임","egg":"🟡","baby":"🫧","adult":"💛","legend":"💰",
                "desc":"돈 먹고 자라는 슬라임. 패시브 수입 증가!",
                "price":30_000_000,"rarity":"고급","rarity_color":"#FFEE00",
                "ability":"황금 흡수 — 패시브 수입 +20%"},
    "fox":     {"name":"구미호",    "egg":"🥚","baby":"🦊","adult":"🦊","legend":"🌙",
                "desc":"아홉 꼬리 여우. 도박 보너스!",
                "price":150_000_000,"rarity":"희귀","rarity_color":"#FF6699",
                "ability":"미혹의 눈 — 도박 승률 +5%"},
}

PET_FOOD = {
    "kibble":   {"name":"일반 사료",    "icon":"🍖","price":500_000,    "exp":10, "happiness":5,  "hunger_restore":15},
    "gourmet":  {"name":"고급 사료",    "icon":"🥩","price":2_000_000,  "exp":40, "happiness":15, "hunger_restore":30},
    "premium":  {"name":"프리미엄 사료","icon":"🍗","price":8_000_000,  "exp":100,"happiness":30, "hunger_restore":50},
    "stardust": {"name":"별의 가루",    "icon":"✨","price":50_000_000, "exp":500,"happiness":50, "hunger_restore":100},
    "dragonmeat":{"name":"용의 심장",   "icon":"💎","price":200_000_000,"exp":2000,"happiness":80,"hunger_restore":100},
    "moonberry":{"name":"달빛 열매",    "icon":"🫐","price":20_000_000, "exp":200,"happiness":40, "hunger_restore":60},
}

PET_ACCESSORIES = {
    "collar": {"name":"황금 목걸이","icon":"📿","price":20_000_000,  "desc":"행운 +5%",    "bonus_type":"luck",   "bonus":5},
    "hat":    {"name":"왕관 모자",  "icon":"👑","price":50_000_000,  "desc":"EXP +10%",   "bonus_type":"exp",    "bonus":10},
    "armor":  {"name":"미스릴 갑옷","icon":"🛡️","price":100_000_000, "desc":"수입 +8%",   "bonus_type":"income", "bonus":8},
    "wings":  {"name":"불사의 날개","icon":"🦋","price":200_000_000, "desc":"행복도 유지", "bonus_type":"happy",  "bonus":20},
    "gem":    {"name":"드래곤 젬",  "icon":"💎","price":500_000_000, "desc":"모든 보너스+5%","bonus_type":"all", "bonus":5},
    "amulet": {"name":"별빛 부적",  "icon":"🔮","price":80_000_000,  "desc":"배틀 ATK+15%","bonus_type":"battle","bonus":15},
    "ribbon": {"name":"행운의 리본","icon":"🎀","price":15_000_000,  "desc":"탐험 보상+10%","bonus_type":"exp",  "bonus":10},
}

PET_SKILLS = [
    {"level":5,  "icon":"💤","name":"낮잠",      "desc":"HP 자동 회복 +5/h"},
    {"level":10, "icon":"⚡","name":"번개 질주", "desc":"EXP 획득 +20%"},
    {"level":15, "icon":"🔮","name":"예지력",    "desc":"퀘스트 보상 +10%"},
    {"level":20, "icon":"💰","name":"황금 손",   "desc":"패시브 수입 시작"},
    {"level":25, "icon":"🌟","name":"별빛 오라", "desc":"행운 대폭 상승"},
    {"level":30, "icon":"🌌","name":"우주 의지", "desc":"모든 능력치 +30%"},
    {"level":35, "icon":"🐉","name":"용맹 포효", "desc":"배틀 공격력 +25%"},
    {"level":40, "icon":"👑","name":"전설 각성", "desc":"외형 전설 변환"},
    {"level":45, "icon":"🌠","name":"유성 강타", "desc":"탐험 희귀도 +"},
    {"level":50, "icon":"🌠","name":"신의 은총", "desc":"모든 보너스 2배"},
]

EXPEDITION_ZONES = {
    "forest":  {"name":"신비의 숲",  "icon":"🌲","duration_h":1,  "min_lv":1,  "base_exp":80,  "base_cash":500_000,   "desc":"초보자도 도전 가능! 기본 탐험",     "rare_item":"🌿 희귀 약초"},
    "desert":  {"name":"황금 사막",  "icon":"🏜️","duration_h":3,  "min_lv":5,  "base_exp":300, "base_cash":3_000_000, "desc":"황금 모래 속 보물을 찾아라!",       "rare_item":"💰 황금 원석"},
    "dungeon": {"name":"고대 던전",  "icon":"🏰","duration_h":8,  "min_lv":10, "base_exp":900, "base_cash":12_000_000,"desc":"위험하지만 보상이 크다!",            "rare_item":"⚔️ 유물 파편"},
    "volcano": {"name":"용암 화산",  "icon":"🌋","duration_h":12, "min_lv":20, "base_exp":2000,"base_cash":40_000_000,"desc":"드래곤의 영역! 고위험 고보상",       "rare_item":"🔥 용암 결정"},
    "space":   {"name":"심우주",     "icon":"🚀","duration_h":24, "min_lv":35, "base_exp":6000,"base_cash":200_000_000,"desc":"우주의 끝에서 전설의 유물을!",      "rare_item":"🌌 별의 파편"},
    "heaven":  {"name":"신계 천공",  "icon":"☁️","duration_h":48, "min_lv":45, "base_exp":20000,"base_cash":1_000_000_000,"desc":"신이 사는 세계. 전설만 입장가능","rare_item":"🌟 신의 눈물"},
}

WILD_MONSTERS = [
    {"name":"고블린",      "icon":"👺","hp":30, "atk":8,  "def":3,  "reward_exp":15, "reward_cash":100_000,  "lv_req":1},
    {"name":"오크 전사",   "icon":"👹","hp":60, "atk":15, "def":8,  "reward_exp":35, "reward_cash":300_000,  "lv_req":5},
    {"name":"독 거미",     "icon":"🕷️","hp":50, "atk":20, "def":5,  "reward_exp":30, "reward_cash":250_000,  "lv_req":5},
    {"name":"불 도마뱀",   "icon":"🦎","hp":80, "atk":25, "def":12, "reward_exp":60, "reward_cash":800_000,  "lv_req":10},
    {"name":"어둠 늑대",   "icon":"🐺","hp":100,"atk":30, "def":15, "reward_exp":90, "reward_cash":1_500_000,"lv_req":15},
    {"name":"해골 기사",   "icon":"💀","hp":120,"atk":35, "def":20, "reward_exp":120,"reward_cash":2_000_000,"lv_req":20},
    {"name":"독룡",        "icon":"🐊","hp":160,"atk":45, "def":28, "reward_exp":200,"reward_cash":5_000_000,"lv_req":25},
    {"name":"어둠의 군주", "icon":"👿","hp":220,"atk":60, "def":35, "reward_exp":350,"reward_cash":15_000_000,"lv_req":35},
    {"name":"고대 드래곤", "icon":"🐲","hp":350,"atk":80, "def":50, "reward_exp":600,"reward_cash":50_000_000,"lv_req":40},
    {"name":"우주 신수",   "icon":"🌌","hp":500,"atk":100,"def":70, "reward_exp":1000,"reward_cash":200_000_000,"lv_req":45},
]

PET_ACHIEVEMENTS = [
    {"id":"first_feed",    "icon":"🍖","name":"첫 식사",     "desc":"처음으로 먹이를 줬다",           "condition":"total_fed >= 1"},
    {"id":"well_fed",      "icon":"🤤","name":"맛있겠다",    "desc":"총 50번 먹이기 완료",             "condition":"total_fed >= 50"},
    {"id":"feast",         "icon":"🏆","name":"미식가",      "desc":"총 500번 먹이기 완료",            "condition":"total_fed >= 500"},
    {"id":"lv10",          "icon":"⚡","name":"성장통",      "desc":"레벨 10 달성",                    "condition":"level >= 10"},
    {"id":"lv25",          "icon":"🌟","name":"영웅의 탄생", "desc":"레벨 25 달성",                    "condition":"level >= 25"},
    {"id":"lv50",          "icon":"🌌","name":"전설이 되다", "desc":"레벨 50 달성",                    "condition":"level >= 50"},
    {"id":"happy_max",     "icon":"😊","name":"행복 만점",   "desc":"행복도 100 달성",                 "condition":"happiness >= 100"},
    {"id":"explorer1",     "icon":"🗺️","name":"탐험가",      "desc":"첫 탐험 완료",                    "condition":"expeditions >= 1"},
    {"id":"explorer10",    "icon":"🌍","name":"세계 정복자", "desc":"탐험 10회 완료",                  "condition":"expeditions >= 10"},
    {"id":"battle_win1",   "icon":"⚔️","name":"첫 승리",     "desc":"배틀 첫 승리",                    "condition":"battles_won >= 1"},
    {"id":"battle_win10",  "icon":"🏅","name":"전투의 달인", "desc":"배틀 10승",                       "condition":"battles_won >= 10"},
    {"id":"hatched",       "icon":"🐣","name":"탄생의 기적", "desc":"알에서 부화",                     "condition":"level >= 5"},
    {"id":"bonded",        "icon":"💕","name":"절친",        "desc":"유대감 레벨 3 달성",             "condition":"bond >= 3"},
    {"id":"full_acc",      "icon":"👑","name":"풀 장착",     "desc":"악세서리 2개 장착",               "condition":"accessories >= 2"},
    {"id":"legend",        "icon":"🌌","name":"우주의 뜻",   "desc":"전설 단계 도달 (Lv.40)",          "condition":"level >= 40"},
]

MOOD_SYSTEM = {
    "신남":   {"emoji":"🤩","color":"#FFD600","desc":"최고로 행복한 상태!",    "condition":lambda h,hg,hp: h>=90 and hg>=80 and hp>=80},
    "행복":   {"emoji":"😊","color":"#00FF88","desc":"기분 좋은 상태",         "condition":lambda h,hg,hp: h>=60 and hg>=60},
    "배고픔": {"emoji":"😮","color":"#FF9500","desc":"배가 고파요!",            "condition":lambda h,hg,hp: hg<20},
    "아픔":   {"emoji":"🤒","color":"#FF4B4B","desc":"HP가 위험해요!",          "condition":lambda h,hg,hp: hp<20},
    "피곤":   {"emoji":"😴","color":"#8888FF","desc":"좀 쉬고 싶어요",         "condition":lambda h,hg,hp: h<30},
    "슬픔":   {"emoji":"😢","color":"#4488FF","desc":"같이 놀아주세요",         "condition":lambda h,hg,hp: h<50},
    "보통":   {"emoji":"😐","color":"#94A3B8","desc":"평범한 상태",            "condition":lambda h,hg,hp: True},
}

TRAINING_GAMES = [
    {"id":"memory",   "icon":"🧠","name":"기억력 훈련", "desc":"순서를 기억하라!", "exp_reward":30, "cost":1_000_000},
    {"id":"speed",    "icon":"⚡","name":"반응속도 훈련","desc":"빠르게 클릭!",    "exp_reward":20, "cost":500_000},
    {"id":"strength", "icon":"💪","name":"체력 훈련",   "desc":"버튼 연타!",       "exp_reward":25, "cost":800_000},
    {"id":"agility",  "icon":"🏃","name":"민첩 훈련",   "desc":"미로 탈출!",       "exp_reward":40, "cost":1_500_000},
    {"id":"magic",    "icon":"🔮","name":"마력 훈련",   "desc":"룬을 완성하라!",   "exp_reward":55, "cost":2_500_000},
    {"id":"battle",   "icon":"⚔️","name":"전투 훈련",   "desc":"콤보를 익혀라!",   "exp_reward":70, "cost":4_000_000},
]

EXP_PER_LEVEL = 200

BOND_TITLES = ["새내기🌱","친구🤝","단짝💛","절친❤️","운명💎","소울메이트🌌"]

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_pet_stage(lv):
    if lv < 5:   return 'egg'
    elif lv < 20: return 'baby'
    elif lv < 40: return 'adult'
    else:         return 'legend'

def get_pet_sprite(species_id, lv):
    sp = PET_SPECIES.get(species_id, PET_SPECIES['cat'])
    stage = get_pet_stage(lv)
    return sp.get(stage, sp['baby'])

def default_pet():
    return {
        "species":None,"name":"","level":0,"exp":0,
        "happiness":100,"hunger":100,"hp":100,
        "accessories":[],"skills":[],"last_fed":0,
        "last_played":0,"passive_collected":0,
        "birth_date":"","total_fed":0,
        "bond":0,"expeditions":0,"battles_won":0,
        "battles_total":0,"journal":[],"achievements":[],
        "expedition":None,"personality":"",
        "total_exp_gained":0,"highest_bond":0,
    }

def load_pet(uid, users=None):
    if users is None: users = load_db(USERS_FILE, {})
    p = users.get(uid, {}).get('pet', default_pet())
    # migrate old pets
    for k,v in default_pet().items():
        if k not in p: p[k] = v
    return p

def save_pet(uid, pet_data):
    users = load_db(USERS_FILE, {})
    if uid not in users: return
    users[uid]['pet'] = pet_data
    save_db(USERS_FILE, users)

def decay_stats(pet):
    now = time.time()
    hf  = (now - pet.get('last_fed',   now)) / 3600
    hp_ = (now - pet.get('last_played', now)) / 3600
    pet['hunger']    = max(0, pet.get('hunger',100)    - int(hf  * 5))
    pet['happiness'] = max(0, pet.get('happiness',100) - int(hp_ * 3))
    if pet['hunger'] < 20:
        pet['hp'] = max(0, pet.get('hp',100) - int(hf * 2))
    # Wings accessory keeps happiness higher
    if 'wings' in pet.get('accessories',[]):
        pet['happiness'] = min(100, pet['happiness'] + int(hp_ * 1))
    return pet

def add_exp(pet, exp_amount):
    acc_bonus = sum(
        PET_ACCESSORIES[a].get('bonus',0)
        for a in pet.get('accessories',[])
        if PET_ACCESSORIES.get(a,{}).get('bonus_type') in ('exp','all')
    )
    exp_gained = int(exp_amount * (1 + acc_bonus/100))
    pet['exp'] = pet.get('exp',0) + exp_gained
    pet['total_exp_gained'] = pet.get('total_exp_gained',0) + exp_gained
    leveled_up = False
    while pet['exp'] >= EXP_PER_LEVEL:
        pet['exp'] -= EXP_PER_LEVEL
        pet['level'] = pet.get('level',0) + 1
        pet['hp']    = min(100, pet.get('hp',100) + 10)
        leveled_up   = True
        for s in PET_SKILLS:
            if s['level'] == pet['level'] and s['name'] not in pet.get('skills',[]):
                pet.setdefault('skills',[]).append(s['name'])
        add_journal(pet, f"🎉 레벨업! Lv.{pet['level']} 달성!")
    return pet, leveled_up, exp_gained

def get_passive_income(pet):
    lv = pet.get('level',0)
    if lv < 20: return 0
    base = lv * 1_000_000
    # slime bonus
    if pet.get('species') == 'slime': base = int(base * 1.2)
    for a in pet.get('accessories',[]):
        acc = PET_ACCESSORIES.get(a,{})
        if acc.get('bonus_type') in ('income','all'):
            base = int(base * (1 + acc.get('bonus',0)/100))
    return base

def get_mood(pet):
    h  = pet.get('happiness',100)
    hg = pet.get('hunger',100)
    hp = pet.get('hp',100)
    for mood, data in MOOD_SYSTEM.items():
        if mood == '보통': continue
        if data['condition'](h, hg, hp):
            return mood, data
    return '보통', MOOD_SYSTEM['보통']

def get_pet_stats(pet):
    lv  = pet.get('level',1)
    atk = lv * 5
    df  = lv * 3
    spd = lv * 2
    # Species bonus
    sp = pet.get('species','cat')
    if sp == 'dragon':  atk = int(atk * 1.3)
    elif sp == 'wolf':  atk = int(atk * 1.15)
    elif sp == 'penguin': df = int(df * 1.2)
    elif sp == 'phoenix': spd= int(spd * 1.2)
    # Accessory
    for a in pet.get('accessories',[]):
        acc = PET_ACCESSORIES.get(a,{})
        if acc.get('bonus_type') == 'battle': atk = int(atk * (1 + acc.get('bonus',0)/100))
    return {"atk":atk,"def":df,"spd":spd}

def check_and_award_achievements(pet):
    earned = []
    lv  = pet.get('level',0)
    tf  = pet.get('total_fed',0)
    h   = pet.get('happiness',100)
    ex  = pet.get('expeditions',0)
    bw  = pet.get('battles_won',0)
    bd  = pet.get('bond',0)
    ac  = len(pet.get('accessories',[]))
    existing = pet.get('achievements',[])
    checks = {
        "first_feed":tf>=1,"well_fed":tf>=50,"feast":tf>=500,
        "lv10":lv>=10,"lv25":lv>=25,"lv50":lv>=50,
        "happy_max":h>=100,"explorer1":ex>=1,"explorer10":ex>=10,
        "battle_win1":bw>=1,"battle_win10":bw>=10,
        "hatched":lv>=5,"bonded":bd>=3,"full_acc":ac>=2,"legend":lv>=40,
    }
    for ach_id, cond in checks.items():
        if cond and ach_id not in existing:
            pet.setdefault('achievements',[]).append(ach_id)
            earned.append(ach_id)
    return earned

def add_journal(pet, entry):
    j = pet.setdefault('journal',[])
    ts = datetime.now(KST).strftime("%m/%d %H:%M")
    j.insert(0, f"[{ts}] {entry}")
    pet['journal'] = j[:50]  # 최근 50개만

def get_bond_title(bond_lv):
    return BOND_TITLES[min(bond_lv, len(BOND_TITLES)-1)]

def get_expedition_reward(zone_id, pet):
    z   = EXPEDITION_ZONES[zone_id]
    lv  = pet.get('level',1)
    mul = 1 + (lv - z['min_lv']) * 0.05
    mul = max(1.0, min(mul, 3.0))
    # Rare item chance
    rare_chance = 0.15 + lv * 0.003
    rare_chance = min(rare_chance, 0.5)
    got_rare = random.random() < rare_chance
    exp_  = int(z['base_exp']  * mul * random.uniform(0.85, 1.2))
    cash_ = int(z['base_cash'] * mul * random.uniform(0.85, 1.2))
    return exp_, cash_, got_rare, z.get('rare_item','✨ 희귀 아이템')

def get_available_monsters(lv):
    return [m for m in WILD_MONSTERS if m['lv_req'] <= lv]

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 HTML ANIMATION GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def generate_pet_animation_html(pet, sp, lv, exp, exp_pct, hunger, happy, hp):
    species      = pet.get('species','cat')
    name         = pet.get('name','펫')
    rarity_color = sp.get('rarity_color','#00E5FF')
    rarity       = sp.get('rarity','일반')
    stage        = get_pet_stage(lv)

    if stage == 'egg':    sprite = sp.get('egg','🥚')
    elif stage == 'baby': sprite = sp.get('baby','🐱')
    elif stage == 'adult': sprite = sp.get('adult','🐈')
    else:                  sprite = sp.get('legend','⭐')

    has_wings  = stage in ('adult','legend') and species in ('dragon','phoenix')
    wing_emoji = '🔥' if species == 'dragon' else '🌟' if species == 'phoenix' else '💫'

    ptcl_map = {
        'dragon':  ['🔥','⚡','✨','💛','🌋'],
        'phoenix': ['🔥','✨','🌟','💛','☀️'],
        'unicorn': ['🌈','✨','💜','💫','🦄'],
        'fox':     ['🌙','✨','🦊','💫','⭐'],
        'wolf':    ['⭐','✨','🌕','💛','❄️'],
        'cat':     ['✨','💫','🌟','🐾','💕'],
        'penguin': ['❄️','⛄','✨','💎','🌊'],
        'slime':   ['💛','✨','💰','🟡','⭐'],
    }
    particles = json.dumps(ptcl_map.get(species, ['✨','💫','⭐']))

    mood_name, mood_data = get_mood(pet)
    mood_color = mood_data['color']

    bg_map = {
        'dragon': ('#200800','#120300'),
        'phoenix':('#1f0900','#0f0500'),
        'unicorn':('#0c0018','#060010'),
        'fox':    ('#140010','#0a0010'),
        'wolf':   ('#080808','#050510'),
        'cat':    ('#060e08','#030a05'),
        'penguin':('#020e1e','#010c18'),
        'slime':  ('#0d0e00','#080900'),
    }
    bg1, bg2 = bg_map.get(species, ('#0a0f1e','#080d18'))
    if stage == 'legend': bg1, bg2 = '#0a000e','#000a0e'

    def bc(v): return '#ff4b4b' if v<30 else '#ffd600' if v<60 else '#00ff88'
    hp_col, hun_col, hap_col = bc(hp), bc(hunger), bc(happy)

    ptcl_interval = 600 if stage=='legend' else 1200 if stage=='adult' else 900

    # ── 기분에 따른 스프라이트 애니메이션 클래스 결정 (Python에서 처리)
    if happy >= 80 and hunger >= 70:
        sprite_anim = f"petFloat 3s ease-in-out infinite, petGlowHappy 2.2s ease-in-out infinite"
    elif stage == 'legend':
        sprite_anim = f"legendFloat 3.5s ease-in-out infinite, legendGlow 2s ease-in-out infinite"
    elif hp < 30 or hunger < 20:
        sprite_anim = f"petSleep 4s ease-in-out infinite"
    elif happy < 40:
        sprite_anim = f"petSad 2s ease-in-out infinite"
    else:
        sprite_anim = f"petFloat 3s ease-in-out infinite, petGlow 2.5s ease-in-out infinite"

    # ── 알 균열 가시성
    c1_op = "1" if exp_pct >= 20 else "0"
    c2_op = "1" if exp_pct >= 40 else "0"
    c3_op = "1" if exp_pct >= 60 else "0"
    c4_op = "1" if exp_pct >= 80 else "0"
    inner_op = "0.75" if exp_pct >= 80 else "0.45" if exp_pct >= 60 else "0.22" if exp_pct >= 40 else "0"
    egg_anim = "eggShake 0.18s ease-in-out infinite" if exp_pct >= 80 else "eggWobble 2.5s ease-in-out infinite"
    remaining_pct = 100 - exp_pct

    # ── HTML로 직접 렌더링할 센터 콘텐츠 생성
    if stage == 'egg':
        center_html = f"""
        <div id="egg-wrap" onclick="eggClick(event)" style="display:flex;flex-direction:column;align-items:center;cursor:pointer;user-select:none;position:relative;z-index:5;">
          <svg id="egg-svg" viewBox="0 0 120 148" width="165" height="202"
               xmlns="http://www.w3.org/2000/svg"
               style="animation:{egg_anim};filter:drop-shadow(0 0 24px {rarity_color});">
            <defs>
              <radialGradient id="eg" cx="38%" cy="30%" r="68%">
                <stop offset="0%" stop-color="#fffbf0"/>
                <stop offset="65%" stop-color="#f0d888"/>
                <stop offset="100%" stop-color="#d4a840"/>
              </radialGradient>
              <radialGradient id="ig" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="{rarity_color}" stop-opacity="0.7"/>
                <stop offset="100%" stop-color="{rarity_color}" stop-opacity="0"/>
              </radialGradient>
              <filter id="ds"><feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="{rarity_color}" flood-opacity="0.6"/></filter>
              <filter id="cs"><feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="{rarity_color}" flood-opacity="0.9"/></filter>
            </defs>
            <ellipse cx="60" cy="83" rx="50" ry="70" fill="url(#eg)" filter="url(#ds)"/>
            <ellipse cx="60" cy="83" rx="45" ry="64" fill="url(#ig)" opacity="{inner_op}" style="animation:innerGlowPulse 0.9s ease-in-out infinite"/>
            <ellipse cx="40" cy="48" rx="14" ry="20" fill="white" opacity="0.38" transform="rotate(-22,40,48)"/>
            <ellipse cx="72" cy="37" rx="5" ry="7" fill="white" opacity="0.22"/>
            <g opacity="{c1_op}"><polyline points="65,18 70,33 62,46 68,57" stroke="#7a3a05" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round" style="animation:crackGlow 1s ease-in-out infinite"/></g>
            <g opacity="{c2_op}"><polyline points="96,72 88,85 93,98 86,112" stroke="#7a3a05" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
            <g opacity="{c3_op}"><polyline points="24,68 32,81 26,95 33,108" stroke="#7a3a05" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
            <g opacity="{c4_op}">
              <polyline points="52,12 57,28 50,46 58,62 52,78 58,94 52,110 57,126" stroke="#4a1a00" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="52,12 57,28 50,46 58,62 52,78 58,94 52,110 57,126" stroke="{rarity_color}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.95" filter="url(#cs)" style="animation:crackGlow 0.5s ease-in-out infinite"/>
              <line x1="58" y1="62" x2="78" y2="55" stroke="#4a1a00" stroke-width="3" stroke-linecap="round"/>
              <line x1="58" y1="62" x2="78" y2="55" stroke="{rarity_color}" stroke-width="1.2" stroke-linecap="round" opacity="0.9"/>
              <line x1="52" y1="78" x2="32" y2="72" stroke="#4a1a00" stroke-width="2.5" stroke-linecap="round"/>
            </g>
            <ellipse cx="60" cy="83" rx="50" ry="70" fill="none" stroke="{rarity_color}" stroke-width="1.5" opacity="0.5"/>
          </svg>
          <div id="hatch-info" style="margin-top:14px;text-align:center;">
            <div id="hatch-lbl" style="color:{rarity_color};font-size:12px;font-weight:900;letter-spacing:1px;margin-bottom:7px;">
              {"💥 부화 임박!!!" if exp_pct >= 80 else f"🥚 부화까지 {remaining_pct}% 남음"}
            </div>
            <div style="width:170px;height:7px;background:rgba(255,255,255,0.1);border-radius:4px;margin:0 auto;overflow:hidden;">
              <div style="width:{exp_pct}%;height:100%;border-radius:4px;background:linear-gradient(90deg,{rarity_color},#fff8);"></div>
            </div>
          </div>
        </div>"""
    else:
        # 날개 HTML
        wings_html = ""
        if has_wings:
            wings_html = f"""
            <span class="wing wing-l" style="position:absolute;top:50%;font-size:42px;z-index:2;pointer-events:none;left:0;transform-origin:right center;animation:wingL 0.38s ease-in-out infinite;">{wing_emoji}</span>
            <span class="wing wing-r" style="position:absolute;top:50%;font-size:42px;z-index:2;pointer-events:none;right:0;transform-origin:left center;animation:wingR 0.38s ease-in-out infinite 0.19s;">{wing_emoji}</span>"""

        # 전설 링 HTML
        rings_html = ""
        if stage == 'legend':
            rings_html = """
            <div style="position:absolute;width:240px;height:240px;border-radius:50%;border:2px dashed rgba(255,255,255,0.12);pointer-events:none;z-index:1;animation:ringRot 6s linear infinite;"></div>
            <div style="position:absolute;width:180px;height:180px;border-radius:50%;border:1px solid rgba(255,255,255,0.08);pointer-events:none;z-index:1;animation:ringRot 4s linear infinite reverse;"></div>
            <div style="position:absolute;width:300px;height:300px;border-radius:50%;border:1px dashed rgba(255,255,255,0.05);pointer-events:none;z-index:1;animation:ringRot 10s linear infinite;"></div>"""

        center_html = f"""
        {rings_html}
        <div id="pet-area" style="position:relative;display:flex;align-items:center;justify-content:center;cursor:pointer;user-select:none;padding:20px 70px;z-index:5;">
          {wings_html}
          <span id="sprite" style="font-size:108px;line-height:1;position:relative;z-index:5;display:block;text-align:center;transition:transform 0.15s;animation:{sprite_anim};">{sprite}</span>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;overflow:hidden;font-family:'Courier New',monospace;}}
#app{{
  width:100%;height:440px;
  background:linear-gradient(160deg,{bg1} 0%,{bg2} 100%);
  border:2px solid {rarity_color};border-radius:22px;position:relative;
  overflow:hidden;display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 60px {rarity_color}44,inset 0 0 100px rgba(0,0,0,0.7);
}}
#bg-canvas{{position:absolute;inset:0;width:100%;height:100%;z-index:0;}}
#grid{{
  position:absolute;inset:0;pointer-events:none;z-index:1;
  background-image:
    linear-gradient(rgba(255,255,255,0.018) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.018) 1px,transparent 1px);
  background-size:40px 40px;
}}
.corner{{position:absolute;width:22px;height:22px;border-color:{rarity_color};border-style:solid;opacity:0.5;z-index:10;}}
.tl{{top:10px;left:10px;border-width:2px 0 0 2px;}}
.tr{{top:10px;right:10px;border-width:2px 2px 0 0;}}
.bl{{bottom:10px;left:10px;border-width:0 0 2px 2px;}}
.br{{bottom:10px;right:10px;border-width:0 2px 2px 0;}}
#rar-badge{{position:absolute;top:14px;left:16px;background:rgba(0,0,0,0.85);border:1px solid {rarity_color};border-radius:12px;padding:5px 13px;color:{rarity_color};font-size:11px;font-weight:900;letter-spacing:1px;z-index:20;}}
#lv-badge{{position:absolute;top:12px;right:16px;background:rgba(0,0,0,0.88);border:1px solid {rarity_color};border-radius:14px;padding:7px 15px;text-align:center;z-index:20;}}
#lv-num{{color:#FFD600;font-size:22px;font-weight:900;line-height:1;}}
#lv-lbl{{color:#64748b;font-size:9px;letter-spacing:2px;margin-top:1px;}}
#mood-badge{{position:absolute;top:14px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.85);border:1px solid {mood_color};border-radius:14px;padding:4px 14px;font-size:12px;color:{mood_color};font-weight:700;white-space:nowrap;z-index:20;}}
#name-tag{{position:absolute;bottom:90px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.75);border:1px solid {rarity_color};border-radius:20px;padding:4px 18px;color:#fff;font-size:13px;font-weight:900;letter-spacing:2px;white-space:nowrap;text-shadow:0 0 10px {rarity_color};z-index:20;}}
#status{{position:absolute;bottom:14px;left:18px;right:18px;z-index:20;}}
.bar-row{{display:flex;align-items:center;gap:8px;margin-bottom:5px;}}
.bar-lbl{{color:#94a3b8;font-size:10px;width:50px;flex-shrink:0;}}
.bar-bg{{flex:1;background:rgba(255,255,255,0.08);border-radius:3px;height:5px;overflow:hidden;}}
.bar-fill{{height:100%;border-radius:3px;}}
.bar-val{{color:#e2e8f0;font-size:10px;width:26px;text-align:right;flex-shrink:0;}}
#efx{{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:50;}}
.ptcl{{position:absolute;pointer-events:none;font-size:14px;animation:ptclRise linear forwards;opacity:0;}}
.heart{{position:absolute;pointer-events:none;font-size:20px;z-index:60;animation:heartUp 1.5s ease-out forwards;}}
.spark{{position:absolute;pointer-events:none;z-index:60;font-size:15px;animation:sparkPop 0.65s ease-out forwards;}}
.fire-shot{{position:absolute;pointer-events:none;font-size:22px;animation:fireShoot 0.7s ease-out forwards;}}
#pet-area.petting #sprite{{
  animation:petHappy 0.25s ease-in-out infinite!important;
  filter:drop-shadow(0 0 35px {rarity_color}) drop-shadow(0 0 18px #ffff0088)!important;
}}
@keyframes petFloat{{0%,100%{{transform:translateY(0) rotate(-2deg) scale(1);}}25%{{transform:translateY(-20px) rotate(0) scale(1.03);}}50%{{transform:translateY(-30px) rotate(2.5deg) scale(1.05);}}75%{{transform:translateY(-15px) rotate(0) scale(1.02);}}}}
@keyframes petSleep{{0%,100%{{transform:translateY(0) rotate(-5deg) scale(0.95);}}50%{{transform:translateY(-8px) rotate(-3deg) scale(0.97);}}}}
@keyframes petSad{{0%,100%{{transform:translateY(0) rotate(-1deg);}}50%{{transform:translateY(-10px) rotate(1deg);}}}}
@keyframes petGlow{{0%,100%{{filter:drop-shadow(0 0 12px {rarity_color});}}50%{{filter:drop-shadow(0 0 30px {rarity_color});}}}}
@keyframes petGlowHappy{{0%,100%{{filter:drop-shadow(0 0 18px {rarity_color});}}50%{{filter:drop-shadow(0 0 45px {rarity_color}) drop-shadow(0 0 20px #ffffffaa);}}}}
@keyframes legendFloat{{0%,100%{{transform:translateY(0) rotate(-2deg) scale(1);}}25%{{transform:translateY(-25px) rotate(0) scale(1.05);}}50%{{transform:translateY(-40px) rotate(3deg) scale(1.08);}}75%{{transform:translateY(-18px) rotate(0) scale(1.03);}}}}
@keyframes legendGlow{{0%,100%{{filter:drop-shadow(0 0 25px #ff00ff88) drop-shadow(0 0 40px #00ffff55);}}50%{{filter:drop-shadow(0 0 55px #ff00ffcc) drop-shadow(0 0 80px #00ffff99);}}}}
@keyframes petHappy{{0%,100%{{transform:translateY(-20px) rotate(-7deg) scale(1.13);}}50%{{transform:translateY(-30px) rotate(7deg) scale(1.18);}}}}
@keyframes wingL{{0%,100%{{transform:translateY(-50%) scaleX(-1) scaleY(1);}}50%{{transform:translateY(-42%) scaleX(-0.4) scaleY(0.8);}}}}
@keyframes wingR{{0%,100%{{transform:translateY(-50%) scaleX(1) scaleY(1);}}50%{{transform:translateY(-42%) scaleX(0.4) scaleY(0.8);}}}}
@keyframes ringRot{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
@keyframes eggWobble{{0%,100%{{transform:rotate(-5deg) translateY(0);}}25%{{transform:rotate(0) translateY(-12px);}}50%{{transform:rotate(5deg) translateY(0);}}75%{{transform:rotate(0) translateY(-6px);}}}}
@keyframes eggShake{{0%,100%{{transform:translateX(0) rotate(0);}}10%{{transform:translateX(-14px) rotate(-10deg);}}20%{{transform:translateX(14px) rotate(10deg);}}30%{{transform:translateX(-10px) rotate(-6deg);}}40%{{transform:translateX(10px) rotate(6deg);}}55%{{transform:translateX(-6px) rotate(-3deg);}}65%{{transform:translateX(6px) rotate(3deg);}}80%{{transform:translateX(-3px) rotate(-1deg);}}}}
@keyframes innerGlowPulse{{0%,100%{{opacity:0.3;}}50%{{opacity:0.85;}}}}
@keyframes crackGlow{{0%,100%{{stroke-opacity:0.7;}}50%{{stroke-opacity:1;}}}}
@keyframes ptclRise{{0%{{opacity:0;transform:translateY(0) scale(0.4);}}8%{{opacity:0.75;}}90%{{opacity:0.2;}}100%{{opacity:0;transform:translateY(-310px) translateX(var(--dx)) scale(1.1);}}}}
@keyframes heartUp{{0%{{opacity:1;transform:translateY(0) scale(0.4) rotate(var(--r));}}45%{{opacity:1;transform:translateY(-50px) scale(1.1) rotate(var(--r));}}100%{{opacity:0;transform:translateY(-110px) scale(0.7) rotate(var(--r));}}}}
@keyframes sparkPop{{0%{{opacity:1;transform:scale(0) rotate(0);}}50%{{opacity:1;transform:scale(1.7) rotate(180deg);}}100%{{opacity:0;transform:scale(0.2) rotate(360deg) translate(var(--sx),var(--sy));}}}}
@keyframes fireShoot{{0%{{opacity:1;transform:translate(0,0) scale(0.6);}}100%{{opacity:0;transform:translate(var(--fx),var(--fy)) scale(1.4);}}}}
</style>
</head>
<body>
<div id="app">
  <canvas id="bg-canvas"></canvas>
  <div id="grid"></div>
  <div class="corner tl"></div><div class="corner tr"></div>
  <div class="corner bl"></div><div class="corner br"></div>

  <div id="rar-badge">★ {rarity}</div>
  <div id="lv-badge"><div id="lv-num">Lv.{lv}</div><div id="lv-lbl">LEVEL</div></div>
  <div id="mood-badge">{mood_data['emoji']} {mood_name}</div>
  <div id="efx"></div>

  {center_html}

  <div id="name-tag">♦ {name} ♦</div>
  <div id="status">
    <div class="bar-row">
      <div class="bar-lbl">❤️ HP</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{hp}%;background:{hp_col};"></div></div>
      <div class="bar-val">{hp}</div>
    </div>
    <div class="bar-row">
      <div class="bar-lbl">🍖 허기</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{hunger}%;background:{hun_col};"></div></div>
      <div class="bar-val">{hunger}</div>
    </div>
    <div class="bar-row">
      <div class="bar-lbl">😊 행복</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{happy}%;background:{hap_col};"></div></div>
      <div class="bar-val">{happy}</div>
    </div>
  </div>
</div>

<script>
const RAR_COLOR="{rarity_color}";
const PARTICLES={particles};
const PET_SPECIES="{species}";
const IS_EGG={"true" if stage=="egg" else "false"};
const IS_LEGEND={"true" if stage=="legend" else "false"};
const PTCL_INTERVAL={ptcl_interval};
const APP = document.getElementById('app');
const EFX = document.getElementById('efx');

// ── Canvas starfield
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
canvas.width=700; canvas.height=440;
const stars = Array.from({{length:90}}, ()=>({{
  x:Math.random()*700, y:Math.random()*440,
  r:Math.random()*1.6+0.2, op:Math.random(), spd:Math.random()*0.018+0.006, dir:1
}}));
const orbs=[
  {{x:120,y:100,r:80, col:RAR_COLOR,op:0.06}},
  {{x:580,y:330,r:100,col:RAR_COLOR,op:0.05}},
  {{x:350,y:220,r:130,col:'#ffffff', op:0.02}},
];
function drawBg(){{
  ctx.clearRect(0,0,700,440);
  orbs.forEach(o=>{{
    const g=ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r);
    const rgb=o.col.replace(/^#/,'');
    const r=parseInt(rgb.slice(0,2),16),g2=parseInt(rgb.slice(2,4),16),b=parseInt(rgb.slice(4,6),16);
    g.addColorStop(0,`rgba(${{r}},${{g2}},${{b}},${{o.op}})`);
    g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
  }});
  stars.forEach(s=>{{
    s.op += s.spd * s.dir;
    if(s.op>1||s.op<0.08) s.dir*=-1;
    ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,'+s.op.toFixed(2)+')'; ctx.fill();
  }});
  requestAnimationFrame(drawBg);
}}
drawBg();

// ── 이미 HTML에 렌더된 요소에 이벤트 연결
if (IS_EGG) {{
  // 알 클릭
  window.eggClick = function(e) {{
    const rect = APP.getBoundingClientRect();
    const x = e.clientX - rect.left, y = e.clientY - rect.top;
    spawnSparks(x, y, 6);
    for(let i=0;i<5;i++) setTimeout(()=>spawnHeart(x+(Math.random()-0.5)*60, y+(Math.random()-0.5)*30), i*90);
  }};
}} else {{
  // 펫 쓰다듬기 & 클릭
  const petArea = document.getElementById('pet-area');
  if(petArea) {{
    let pettingTmo=null, lastHeart=0;
    petArea.addEventListener('mousemove', e => {{
      petArea.classList.add('petting');
      clearTimeout(pettingTmo);
      pettingTmo = setTimeout(()=>petArea.classList.remove('petting'), 380);
      const now=Date.now();
      if(now-lastHeart>160) {{
        const r=APP.getBoundingClientRect();
        spawnHeart(e.clientX-r.left, e.clientY-r.top-25);
        lastHeart=now;
      }}
    }});
    petArea.addEventListener('mouseleave', ()=>petArea.classList.remove('petting'));
    petArea.addEventListener('click', e => {{
      const r=APP.getBoundingClientRect();
      const x=e.clientX-r.left, y=e.clientY-r.top;
      spawnSparks(x, y, 8);
      for(let i=0;i<10;i++) setTimeout(()=>spawnHeart(x+(Math.random()-0.5)*80, y+(Math.random()-0.5)*45), i*70);
      if(PET_SPECIES==='dragon')  spawnFireBreath(x, y);
      if(PET_SPECIES==='phoenix') for(let i=0;i<8;i++) setTimeout(()=>spawnEmber(), i*80);
      if(PET_SPECIES==='unicorn') for(let i=0;i<10;i++) setTimeout(()=>spawnRainbow(), i*60);
    }});
  }}
}}

// ── PARTICLE SYSTEM
function spawnPtcl() {{
  const p=document.createElement('div');
  p.className='ptcl';
  p.textContent=PARTICLES[Math.floor(Math.random()*PARTICLES.length)];
  const dx=(Math.random()-0.5)*100;
  p.style.setProperty('--dx',dx+'px');
  p.style.left=Math.random()*100+'%';
  p.style.bottom='-20px';
  p.style.animationDuration=(4+Math.random()*6)+'s';
  APP.insertBefore(p,APP.firstChild);
  setTimeout(()=>p.remove(),11000);
}}
setInterval(spawnPtcl, PTCL_INTERVAL);

const HEARTS=['💕','💖','💗','💝','❤️','💓','💘','💞','🩷'];
function spawnHeart(x,y) {{
  const h=document.createElement('div');
  h.className='heart';
  h.textContent=HEARTS[Math.floor(Math.random()*HEARTS.length)];
  h.style.setProperty('--r',((Math.random()-0.5)*55)+'deg');
  h.style.left=x+'px'; h.style.top=y+'px';
  EFX.appendChild(h);
  setTimeout(()=>h.remove(),1700);
}}
const SPARKS=['✨','⭐','💫','🌟','⚡','💥','🌸'];
function spawnSparks(x,y,n) {{
  for(let i=0;i<n;i++) {{
    const s=document.createElement('div');
    s.className='spark';
    s.textContent=SPARKS[Math.floor(Math.random()*SPARKS.length)];
    const a=(i/n)*Math.PI*2+Math.random()*0.5;
    const d=30+Math.random()*38;
    s.style.setProperty('--sx',Math.cos(a)*d+'px');
    s.style.setProperty('--sy',Math.sin(a)*d+'px');
    s.style.left=x+'px'; s.style.top=y+'px';
    s.style.animationDelay=(i*0.04)+'s';
    EFX.appendChild(s);
    setTimeout(()=>s.remove(),900);
  }}
}}
function spawnFireBreath(x,y) {{
  const fireEmojis=['🔥','💥','🌋','⚡'];
  for(let i=0;i<12;i++) {{
    setTimeout(()=>{{
      const f=document.createElement('div');
      f.className='fire-shot';
      f.textContent=fireEmojis[Math.floor(Math.random()*fireEmojis.length)];
      const angle=(Math.random()-0.3)*1.2;
      const dist=80+Math.random()*120;
      f.style.setProperty('--fx',Math.cos(angle)*dist+'px');
      f.style.setProperty('--fy',(Math.sin(angle)*dist-30)+'px');
      f.style.left=x+'px'; f.style.top=y+'px';
      f.style.fontSize=(18+Math.random()*14)+'px';
      f.style.animationDuration=(0.4+Math.random()*0.4)+'s';
      EFX.appendChild(f);
      setTimeout(()=>f.remove(),900);
    }}, i*45);
  }}
}}
function spawnEmber() {{
  const f=document.createElement('div');
  f.className='fire-shot';
  f.textContent=['🔥','✨','💫','⭐'][Math.floor(Math.random()*4)];
  const angle=-Math.PI/2+(Math.random()-0.5)*1.5;
  const dist=40+Math.random()*80;
  f.style.setProperty('--fx',Math.cos(angle)*dist+'px');
  f.style.setProperty('--fy',Math.sin(angle)*dist+'px');
  f.style.left='50%'; f.style.top='45%';
  f.style.animationDuration=(0.5+Math.random()*0.5)+'s';
  EFX.appendChild(f);
  setTimeout(()=>f.remove(),1100);
}}
function spawnRainbow() {{
  const colors=['🌈','💜','💛','💖','🩵'];
  const f=document.createElement('div');
  f.className='spark';
  f.textContent=colors[Math.floor(Math.random()*colors.length)];
  const angle=Math.random()*Math.PI*2;
  const d=40+Math.random()*60;
  f.style.setProperty('--sx',Math.cos(angle)*d+'px');
  f.style.setProperty('--sy',Math.sin(angle)*d+'px');
  f.style.left='50%'; f.style.top='45%'; f.style.fontSize='20px';
  EFX.appendChild(f);
  setTimeout(()=>f.remove(),800);
}}

// Legend: continuous rainbow orb
if(IS_LEGEND) {{
  setInterval(()=>{{
    const f=document.createElement('div');
    f.className='spark';
    f.textContent=['🌌','⭐','💫','🌟','✨'][Math.floor(Math.random()*5)];
    const angle=Math.random()*Math.PI*2;
    const d=100+Math.random()*30;
    f.style.left=(350+Math.cos(angle)*d)+'px';
    f.style.top =(220+Math.sin(angle)*d)+'px';
    f.style.setProperty('--sx',(Math.random()-0.5)*40+'px');
    f.style.setProperty('--sy',(Math.random()-0.5)*40+'px');
    EFX.appendChild(f);
    setTimeout(()=>f.remove(),900);
  }}, 250);
}}
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 🏠 MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render(market, nw):
    st.markdown("""
    <style>
    .pet-tab-header{font-size:1.15rem;font-weight:900;color:#E2E8F0;margin-bottom:12px;}
    .pet-sub{color:#94A3B8;font-size:0.83rem;margin-bottom:16px;}
    .pet-card{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);
              border-radius:14px;padding:16px;margin-bottom:10px;}
    .pet-card:hover{border-color:rgba(0,229,255,0.3);background:rgba(0,229,255,0.04);}
    .stat-chip{display:inline-block;padding:3px 10px;border-radius:8px;font-size:0.75rem;
               font-weight:700;margin-right:5px;margin-bottom:4px;}
    </style>
    """, unsafe_allow_html=True)

    st.title("🐾 펫 키우기")
    uid   = st.session_state.logged_in_user
    users = load_db(USERS_FILE, {})
    pet   = load_pet(uid, users)

    # Time decay
    if pet.get('species'): pet = decay_stats(pet)

    # Passive income
    passive = get_passive_income(pet)
    if passive > 0 and pet.get('species'):
        elapsed = time.time() - pet.get('passive_collected', time.time())
        earned  = int(passive * elapsed / 3600)
        if earned > 0:
            pet['passive_collected'] = time.time()
            atomic_add_cash(uid, earned)
            st.session_state.global_cash += earned
            save_pet(uid, pet)
            st.toast(f"🐾 {pet.get('name','펫')}이(가) {format_korean_money(earned)} 벌어왔어요!", icon="💰")

    # Check expedition return
    exp_data = pet.get('expedition')
    if exp_data and time.time() >= exp_data.get('return_time', 0):
        st.session_state['expedition_returned'] = True

    # ══════════════════════════════════════════════════════════════════════════
    # NO PET → ADOPTION SCREEN
    # ══════════════════════════════════════════════════════════════════════════
    if not pet.get('species'):
        st.markdown("""
        <div style='text-align:center;padding:44px 20px;background:rgba(255,255,255,0.02);
                    border:1px solid rgba(0,229,255,0.18);border-radius:22px;margin-bottom:28px;'>
            <div style='font-size:5rem;margin-bottom:14px;animation:pulse 2s infinite;'>🐾</div>
            <div style='font-size:1.6rem;font-weight:900;color:#E2E8F0;margin-bottom:10px;'>아직 펫이 없어요!</div>
            <div style='color:#64748B;font-size:0.9rem;'>
                아래에서 파트너를 선택하고 함께 성장해보세요.<br>
                먹이주기, 훈련, 탐험, 배틀 등 다양한 콘텐츠가 기다립니다!
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏪 펫 입양소")
        rarity_order = ["전설","영웅","희귀","고급","일반"]
        sorted_species = sorted(PET_SPECIES.items(), key=lambda x: rarity_order.index(x[1]['rarity']) if x[1]['rarity'] in rarity_order else 99)

        sp_cols = st.columns(4)
        for i, (sp_id, sp) in enumerate(sorted_species):
            with sp_cols[i % 4]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;border-color:{sp["rarity_color"]}33;'>
                    <div style='font-size:3.2rem;margin-bottom:10px;'>{sp['baby']}</div>
                    <div style='font-size:1rem;font-weight:900;color:#E2E8F0;'>{sp['name']}</div>
                    <div style='font-size:0.7rem;color:{sp["rarity_color"]};margin:4px 0 8px;font-weight:900;'>
                        ★ {sp['rarity']}
                    </div>
                    <div style='font-size:0.75rem;color:#64748B;margin-bottom:10px;'>{sp['desc']}</div>
                    <div style='font-size:0.72rem;color:{sp["rarity_color"]};background:rgba(0,0,0,0.3);
                                padding:4px 8px;border-radius:6px;margin-bottom:10px;'>
                        🎯 {sp['ability']}
                    </div>
                    <div style='color:#FFD600;font-weight:900;'>{format_korean_money(sp['price'])}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("입양하기", key=f"adopt_{sp_id}", use_container_width=True):
                    if st.session_state.global_cash < sp['price']:
                        st.error(f"현금 부족! {format_korean_money(sp['price'])} 필요")
                    else:
                        st.session_state['adopting_pet'] = sp_id
                        st.rerun()

        if st.session_state.get('adopting_pet'):
            sp_id = st.session_state['adopting_pet']
            sp    = PET_SPECIES[sp_id]
            with st.container():
                st.markdown(f"---\n### 🎉 {sp['name']} 입양 중...")
                pet_name = st.text_input("펫 이름을 지어주세요!", max_chars=12, placeholder="최대 12자")
                personalities = ["용감한","조용한","장난꾸러기","우아한","힘찬","신비로운","따뜻한","재치있는"]
                personality = st.selectbox("성격 선택", personalities, key="personality_select")
                c1, c2 = st.columns(2)
                if c1.button("✅ 입양 확정!", use_container_width=True):
                    if not pet_name.strip():
                        st.error("이름을 입력해주세요!")
                    else:
                        new_pet = default_pet()
                        now = time.time()
                        new_pet.update({
                            'species': sp_id, 'name': pet_name.strip(),
                            'level': 1, 'birth_date': datetime.now(KST).strftime("%Y-%m-%d"),
                            'last_fed': now, 'last_played': now,
                            'passive_collected': now, 'personality': personality,
                        })
                        add_journal(new_pet, f"🐣 {pet_name}(이)가 태어났다!")
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

    # ══════════════════════════════════════════════════════════════════════════
    # PET MAIN SCREEN
    # ══════════════════════════════════════════════════════════════════════════
    sp      = PET_SPECIES.get(pet['species'], PET_SPECIES['cat'])
    lv      = pet.get('level', 1)
    exp     = pet.get('exp', 0)
    hunger  = pet.get('hunger', 100)
    happy   = pet.get('happiness', 100)
    hp      = pet.get('hp', 100)
    exp_pct = int(exp / EXP_PER_LEVEL * 100)
    stage   = get_pet_stage(lv)
    mood_name, mood_data = get_mood(pet)
    bond_lv = min(pet.get('bond',0)//20, 5)

    # Awards achievements
    new_ach = check_and_award_achievements(pet)
    if new_ach:
        save_pet(uid, pet)
        for ach_id in new_ach:
            ach_data = next((a for a in PET_ACHIEVEMENTS if a['id']==ach_id), None)
            if ach_data:
                st.toast(f"🏆 업적 달성: {ach_data['icon']} {ach_data['name']}!", icon="🎉")

    # Expedition return
    if st.session_state.get('expedition_returned') and pet.get('expedition'):
        exp_d = pet['expedition']
        zone  = EXPEDITION_ZONES.get(exp_d['zone'], {})
        st.success(f"🗺️ {zone.get('icon','')} **{zone.get('name','탐험')}** 탐험 완료! 보상을 수령하세요!")
        c1, c2 = st.columns([3,1])
        with c1:
            st.info(f"예상 보상 — EXP: ~{zone.get('base_exp',0):,} · 💰 ~{format_korean_money(zone.get('base_cash',0))}")
        with c2:
            if st.button("🎁 보상 수령", key="claim_expedition", use_container_width=True):
                exp_r, cash_r, got_rare, rare_name = get_expedition_reward(exp_d['zone'], pet)
                pet['expedition'] = None
                pet['expeditions'] = pet.get('expeditions',0) + 1
                pet, lvup, gained_exp = add_exp(pet, exp_r)
                atomic_add_cash(uid, cash_r)
                st.session_state.global_cash += cash_r
                add_journal(pet, f"🗺️ {zone.get('name','탐험')} 완료! EXP+{gained_exp} 💰+{format_korean_money(cash_r)}")
                if got_rare:
                    add_journal(pet, f"🎁 희귀 아이템 획득: {rare_name}!")
                save_pet(uid, pet)
                sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 탐험 보상 ({zone.get('name','')})", cash_r)
                del st.session_state['expedition_returned']
                st.toast(f"🗺️ EXP +{gained_exp} | 💰 +{format_korean_money(cash_r)}", icon="✅")
                if got_rare: st.toast(f"✨ 희귀 아이템: {rare_name}!", icon="🎁")
                if lvup: st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

    # ── Animated pet card
    components.html(
        generate_pet_animation_html(pet, sp, lv, exp, exp_pct, hunger, happy, hp),
        height=450
    )

    # Stat bar below the card
    stat_cols = st.columns(5)
    stat_data = [
        ("⚡ Lv.", str(lv),              "#FFD600"),
        ("🧬 EXP",f"{exp}/{EXP_PER_LEVEL}","#00E5FF"),
        ("💕 유대",get_bond_title(bond_lv), "#FF6699"),
        ("🌡️ 기분", f"{mood_data['emoji']} {mood_name}", mood_data['color']),
        ("💰 패시브", format_korean_money(passive)+"/h" if passive>0 else "Lv.20~", "#00FF88"),
    ]
    for i,(lbl,val,col) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                        border-radius:10px;padding:9px;text-align:center;'>
                <div style='color:#64748B;font-size:0.72rem;'>{lbl}</div>
                <div style='color:{col};font-weight:900;font-size:0.85rem;margin-top:2px;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    # Warnings
    if hunger < 20: st.warning(f"⚠️ {pet['name']}이(가) 너무 배가 고파요!")
    if happy  < 20: st.warning(f"😢 {pet['name']}이(가) 너무 슬퍼해요!")
    if hp     < 30: st.error(f"💀 {pet['name']}의 HP가 위험해요!")

    st.write("")

    # ── TABS ──────────────────────────────────────────────────────────────────
    tabs = st.tabs(["🍖 먹이주기","🎮 훈련","🗺️ 탐험","⚔️ 배틀","👗 아이템","📜 스킬","🏆 업적","📖 일지","📊 정보"])

    # ── TAB 1: 먹이주기
    with tabs[0]:
        st.markdown('<div class="pet-tab-header">🍖 먹이 선택</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">먹이를 줄수록 EXP와 행복도가 오릅니다.</div>', unsafe_allow_html=True)
        food_cols = st.columns(3)
        for i, (f_id, food) in enumerate(PET_FOOD.items()):
            with food_cols[i % 3]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2.8rem;'>{food['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:8px;'>{food['name']}</div>
                    <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>
                        EXP +{food['exp']} &nbsp;|&nbsp; 행복 +{food['happiness']} &nbsp;|&nbsp; 허기 +{food['hunger_restore']}
                    </div>
                    <div style='color:#FFD600;font-weight:900;margin-top:8px;font-size:1rem;'>{format_korean_money(food['price'])}</div>
                </div>
                """, unsafe_allow_html=True)
                qty = st.number_input("수량", min_value=1, max_value=50, value=1, key=f"food_qty_{f_id}")
                if st.button(f"{food['icon']} 먹이기 ×{qty}", key=f"feed_{f_id}", use_container_width=True):
                    total_cost = food['price'] * qty
                    if st.session_state.global_cash < total_cost:
                        st.error("현금 부족!")
                    else:
                        st.session_state.global_cash -= total_cost
                        atomic_deduct_cash(uid, total_cost)
                        pet['hunger']    = min(100, pet.get('hunger',100) + food['hunger_restore'] * qty)
                        pet['happiness'] = min(100, pet.get('happiness',100) + food['happiness'] * qty)
                        pet['hp']        = min(100, pet.get('hp',100) + 5 * qty)
                        pet['last_fed']  = time.time()
                        pet['total_fed'] = pet.get('total_fed',0) + qty
                        pet['bond']      = pet.get('bond',0) + qty
                        pet, leveled_up, gained_exp = add_exp(pet, food['exp'] * qty)
                        add_journal(pet, f"🍖 {food['name']}×{qty} 먹임! EXP+{gained_exp}")
                        save_pet(uid, pet)
                        sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} 먹이({food['name']}×{qty})", -total_cost)
                        st.toast(f"🍖 {food['icon']}×{qty}! EXP +{gained_exp}", icon="✅")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

    # ── TAB 2: 훈련
    with tabs[1]:
        st.markdown('<div class="pet-tab-header">🎮 훈련 미니게임</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">훈련으로 EXP를 올리세요. 대성공 시 보너스!</div>', unsafe_allow_html=True)
        train_cols = st.columns(3)
        for i, tg in enumerate(TRAINING_GAMES):
            with train_cols[i % 3]:
                st.markdown(f"""
                <div class='pet-card'>
                    <div style='display:flex;align-items:center;gap:12px;'>
                        <div style='font-size:2.5rem;'>{tg['icon']}</div>
                        <div>
                            <div style='font-weight:900;color:#E2E8F0;'>{tg['name']}</div>
                            <div style='color:#64748B;font-size:0.78rem;'>{tg['desc']}</div>
                            <div style='color:#FFD600;font-size:0.78rem;font-weight:700;margin-top:4px;'>
                                EXP +{tg['exp_reward']} &nbsp;|&nbsp; {format_korean_money(tg['cost'])}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🎮 {tg['name']}", key=f"train_{tg['id']}", use_container_width=True):
                    if st.session_state.global_cash < tg['cost']:
                        st.error("현금 부족!")
                    elif pet.get('happiness',100) < 10:
                        st.error("행복도가 너무 낮아요!")
                    else:
                        st.session_state.global_cash -= tg['cost']
                        atomic_deduct_cash(uid, tg['cost'])
                        roll    = random.uniform(0.75, 1.35)
                        exp_got = int(tg['exp_reward'] * roll)
                        pet['happiness']   = max(0, pet.get('happiness',100) - 5)
                        pet['last_played'] = time.time()
                        pet['bond']        = pet.get('bond',0) + 2
                        pet, leveled_up, gained_exp = add_exp(pet, exp_got)
                        result = "🌟 대성공!" if roll>=1.25 else "✅ 성공!" if roll>=0.95 else "😅 아쉬운 결과"
                        add_journal(pet, f"🎮 {tg['name']} {result} EXP+{gained_exp}")
                        save_pet(uid, pet)
                        sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} {tg['name']}", -tg['cost'])
                        st.toast(f"{result} EXP +{gained_exp}", icon="💪")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

        st.write("---")
        st.markdown("#### 💝 같이 놀기 (무료, 쿨타임 10분)")
        last_played = pet.get('last_played',0)
        remaining   = max(0, 600 - (time.time()-last_played))
        play_options = ["공 던지기 🎾","숨바꼭질 🙈","퍼즐 맞추기 🧩","노래 부르기 🎵","산책하기 🌿","수영 🏊","요리 먹기 🍳"]
        sel = st.selectbox("놀이 선택", play_options, key="play_select")
        if remaining > 0:
            st.info(f"⏳ {int(remaining//60)}분 {int(remaining%60)}초 후 다시 놀 수 있어요!")
        else:
            if st.button("💝 같이 놀기!", use_container_width=True, key="play_btn"):
                pe  = random.randint(5,15)
                ph  = random.randint(15,35)
                pet['happiness']   = min(100, pet.get('happiness',100) + ph)
                pet['last_played'] = time.time()
                pet['bond']        = pet.get('bond',0) + 5
                pet, lvup, ge = add_exp(pet, pe)
                add_journal(pet, f"💝 {sel} 함께 놀았다! 행복+{ph} EXP+{ge}")
                save_pet(uid, pet)
                st.toast(f"😊 {sel} 완료! 행복 +{ph}, EXP +{ge}", icon="💝")
                if lvup: st.balloons(); st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

    # ── TAB 3: 탐험
    with tabs[2]:
        st.markdown('<div class="pet-tab-header">🗺️ 탐험 보내기</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">펫을 탐험 보내면 시간이 지난 후 EXP와 재화를 가져옵니다!</div>', unsafe_allow_html=True)

        current_exp = pet.get('expedition')
        if current_exp and time.time() < current_exp.get('return_time',0):
            z = EXPEDITION_ZONES.get(current_exp['zone'],{})
            remain_s = current_exp['return_time'] - time.time()
            remain_h = int(remain_s // 3600)
            remain_m = int((remain_s % 3600) // 60)
            st.markdown(f"""
            <div style='background:rgba(0,229,255,0.06);border:1px solid #00E5FF44;
                        border-radius:14px;padding:20px;text-align:center;'>
                <div style='font-size:2.5rem;margin-bottom:8px;'>{z.get("icon","🗺️")}</div>
                <div style='color:#00E5FF;font-size:1.1rem;font-weight:900;'>{z.get("name","탐험")} 진행 중</div>
                <div style='color:#94A3B8;margin-top:8px;font-size:0.9rem;'>
                    ⏳ 귀환까지 <span style='color:#FFD600;font-weight:900;'>{remain_h}시간 {remain_m}분</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            exp_cols = st.columns(3)
            for i, (z_id, z) in enumerate(EXPEDITION_ZONES.items()):
                locked = lv < z['min_lv']
                with exp_cols[i % 3]:
                    st.markdown(f"""
                    <div class='pet-card' style='text-align:center;opacity:{"0.4" if locked else "1"};'>
                        <div style='font-size:2.5rem;'>{z['icon']}</div>
                        <div style='color:#E2E8F0;font-weight:900;margin-top:8px;'>{z['name']}</div>
                        <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>{z['desc']}</div>
                        <div style='margin-top:10px;'>
                            <span class='stat-chip' style='background:rgba(255,214,0,0.1);color:#FFD600;'>
                                ⏱️ {z['duration_h']}h
                            </span>
                            <span class='stat-chip' style='background:rgba(0,229,255,0.1);color:#00E5FF;'>
                                Lv.{z['min_lv']}+
                            </span>
                        </div>
                        <div style='color:#64748B;font-size:0.73rem;margin-top:8px;'>
                            💡 {z['rare_item']} 획득 가능
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if locked:
                        st.button(f"🔒 Lv.{z['min_lv']} 필요", key=f"exp_{z_id}", disabled=True, use_container_width=True)
                    else:
                        if st.button(f"🗺️ 탐험 출발!", key=f"exp_{z_id}", use_container_width=True):
                            pet['expedition'] = {
                                'zone': z_id,
                                'start_time': time.time(),
                                'return_time': time.time() + z['duration_h']*3600,
                            }
                            add_journal(pet, f"🗺️ {z['name']} 탐험 출발!")
                            save_pet(uid, pet)
                            st.toast(f"🗺️ {z['name']} 탐험 출발! {z['duration_h']}시간 후 귀환해요.", icon="🚀")
                            st.rerun()

    # ── TAB 4: 배틀
    with tabs[3]:
        st.markdown('<div class="pet-tab-header">⚔️ 배틀</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">야생 몬스터와 싸워 EXP와 재화를 획득하세요!</div>', unsafe_allow_html=True)

        pet_stats = get_pet_stats(pet)
        st.markdown(f"""
        <div class='pet-card'>
            <div style='color:#E2E8F0;font-weight:900;margin-bottom:10px;'>{pet['name']}의 능력치</div>
            <div style='display:flex;gap:16px;flex-wrap:wrap;'>
                <span class='stat-chip' style='background:rgba(255,75,75,0.15);color:#FF4B4B;'>⚔️ ATK {pet_stats["atk"]}</span>
                <span class='stat-chip' style='background:rgba(0,229,255,0.12);color:#00E5FF;'>🛡️ DEF {pet_stats["def"]}</span>
                <span class='stat-chip' style='background:rgba(0,255,136,0.12);color:#00FF88;'>💨 SPD {pet_stats["spd"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Battle state machine
        if 'battle_state' not in st.session_state:
            st.session_state.battle_state = None

        bs = st.session_state.battle_state

        if bs is None:
            st.markdown("#### 🦹 몬스터 선택")
            available = get_available_monsters(lv)
            mob_cols = st.columns(3)
            for i, mob in enumerate(available[:9]):
                with mob_cols[i % 3]:
                    st.markdown(f"""
                    <div class='pet-card' style='text-align:center;'>
                        <div style='font-size:2.5rem;'>{mob['icon']}</div>
                        <div style='color:#E2E8F0;font-weight:900;margin-top:6px;'>{mob['name']}</div>
                        <div style='margin-top:6px;'>
                            <span class='stat-chip' style='background:rgba(255,75,75,0.12);color:#FF4B4B;'>❤️{mob['hp']}</span>
                            <span class='stat-chip' style='background:rgba(255,0,0,0.1);color:#FF6B6B;'>⚔️{mob['atk']}</span>
                            <span class='stat-chip' style='background:rgba(0,229,255,0.1);color:#00E5FF;'>🛡️{mob['def']}</span>
                        </div>
                        <div style='color:#00FF88;font-size:0.75rem;margin-top:8px;'>
                            보상: EXP+{mob['reward_exp']} · {format_korean_money(mob['reward_cash'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"⚔️ 도전!", key=f"battle_{i}", use_container_width=True):
                        st.session_state.battle_state = {
                            'monster': mob.copy(),
                            'pet_hp': min(pet.get('hp',100), 100),
                            'monster_hp': mob['hp'],
                            'log': [f"⚔️ {pet['name']} VS {mob['name']} 배틀 시작!"],
                            'turn': 1,
                            'over': False, 'won': False
                        }
                        st.rerun()
        else:
            mob     = bs['monster']
            pet_hp  = bs['pet_hp']
            mob_hp  = bs['monster_hp']

            # Battle display
            b1, b2, b3 = st.columns([2,1,2])
            with b1:
                pct_p = max(0, int(pet_hp))
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2.5rem;'>{get_pet_sprite(pet['species'],lv)}</div>
                    <div style='color:#E2E8F0;font-weight:900;'>{pet['name']}</div>
                    <div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;'>
                        <div style='background:#00FF88;width:{pct_p}%;height:100%;border-radius:4px;transition:width 0.5s;'></div>
                    </div>
                    <div style='color:#00FF88;font-size:0.85rem;margin-top:4px;'>{pet_hp}/100 HP</div>
                </div>
                """, unsafe_allow_html=True)
            with b2:
                st.markdown(f"""
                <div style='text-align:center;padding:20px 0;'>
                    <div style='font-size:2rem;'>⚔️</div>
                    <div style='color:#FFD600;font-weight:900;margin-top:8px;'>TURN {bs['turn']}</div>
                    <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>VS</div>
                </div>
                """, unsafe_allow_html=True)
            with b3:
                pct_m = max(0, int(mob_hp/mob['hp']*100))
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2.5rem;'>{mob['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:900;'>{mob['name']}</div>
                    <div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;'>
                        <div style='background:#FF4B4B;width:{pct_m}%;height:100%;border-radius:4px;transition:width 0.5s;'></div>
                    </div>
                    <div style='color:#FF4B4B;font-size:0.85rem;margin-top:4px;'>{mob_hp}/{mob["hp"]} HP</div>
                </div>
                """, unsafe_allow_html=True)

            # Battle log
            for log_line in bs['log'][-6:]:
                st.markdown(f"<div style='color:#94A3B8;font-size:0.83rem;padding:2px 0;'>▸ {log_line}</div>", unsafe_allow_html=True)

            if bs['over']:
                if bs['won']:
                    st.success(f"🏆 승리! EXP +{mob['reward_exp']} · 💰 +{format_korean_money(mob['reward_cash'])}")
                else:
                    st.error(f"💀 패배... {pet['name']}이(가) 쓰러졌어요.")
                if st.button("🔄 배틀 종료", use_container_width=True, key="battle_end"):
                    if bs['won']:
                        pet, lvup, ge = add_exp(pet, mob['reward_exp'])
                        atomic_add_cash(uid, mob['reward_cash'])
                        st.session_state.global_cash += mob['reward_cash']
                        pet['battles_won']   = pet.get('battles_won',0) + 1
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        pet['bond'] = pet.get('bond',0) + 3
                        add_journal(pet, f"⚔️ {mob['name']} 격파! EXP+{ge} 💰+{format_korean_money(mob['reward_cash'])}")
                        log_tx(uid,"펫",f"{pet['name']} 배틀승 vs {mob['name']}",mob['reward_cash'])
                        save_pet(uid, pet)
                        sync_user_data()
                    else:
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        pet['hp'] = max(1, pet.get('hp',100) - 20)
                        add_journal(pet, f"⚔️ {mob['name']}에게 패배... HP -20")
                        save_pet(uid, pet)
                    st.session_state.battle_state = None
                    st.rerun()
            else:
                ca, cb, cc = st.columns(3)
                with ca:
                    if st.button("⚔️ 일반 공격", use_container_width=True, key="atk_normal"):
                        dmg_pet = max(0, pet_stats['atk'] - mob['def'] + random.randint(-5,8))
                        dmg_mob = max(0, mob['atk'] - pet_stats['def'] + random.randint(-3,6))
                        bs['monster_hp'] -= dmg_pet; bs['pet_hp'] -= dmg_mob
                        bs['log'].append(f"💥 {pet['name']} → {mob['name']}: -{dmg_pet}HP")
                        bs['log'].append(f"🩸 {mob['name']} → {pet['name']}: -{dmg_mob}HP")
                        bs['turn'] += 1
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cb:
                    if st.button("🔥 강공격 (HP-10)", use_container_width=True, key="atk_heavy"):
                        dmg_pet = max(0, int(pet_stats['atk']*1.8) - mob['def'] + random.randint(-4,12))
                        dmg_mob = max(0, mob['atk'] - pet_stats['def'] + random.randint(-2,5))
                        bs['pet_hp']     -= 10
                        bs['monster_hp'] -= dmg_pet; bs['pet_hp'] -= dmg_mob
                        bs['log'].append(f"💥💥 강공격! {mob['name']}: -{dmg_pet}HP (자상-10HP)")
                        bs['log'].append(f"🩸 {mob['name']}: -{dmg_mob}HP")
                        bs['turn'] += 1
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cc:
                    if st.button("🏃 도망가기", use_container_width=True, key="atk_flee"):
                        flee = random.random() < (0.4 + pet_stats['spd']/200)
                        if flee:
                            bs['log'].append("🏃 도망 성공!")
                            bs['over']=True; bs['won']=False
                        else:
                            dmg = max(0, mob['atk'] - pet_stats['def'] + random.randint(0,8))
                            bs['pet_hp'] -= dmg
                            bs['log'].append(f"❌ 도망 실패! 반격 -{dmg}HP")
                            if bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        bs['turn'] += 1
                        st.rerun()

    # ── TAB 5: 아이템
    with tabs[4]:
        st.markdown('<div class="pet-tab-header">👗 악세서리 상점</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">악세서리를 장착해 능력을 강화하세요! 최대 2개.</div>', unsafe_allow_html=True)
        equipped = pet.get('accessories',[])
        acc_cols = st.columns(3)
        for i,(acc_id, acc) in enumerate(PET_ACCESSORIES.items()):
            is_eq = acc_id in equipped
            with acc_cols[i%3]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;
                    {"border-color:#00E5FF;background:rgba(0,229,255,0.06);" if is_eq else ""}'>
                    <div style='font-size:2.5rem;'>{acc['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;'>{acc['name']}</div>
                    <div style='color:#00FF88;font-size:0.8rem;margin-top:4px;'>{acc['desc']}</div>
                    <div style='color:#FFD600;font-weight:900;margin-top:8px;'>{format_korean_money(acc['price'])}</div>
                    {"<div style='color:#00E5FF;font-size:0.75rem;margin-top:4px;'>✅ 장착 중</div>" if is_eq else ""}
                </div>
                """, unsafe_allow_html=True)
                if is_eq:
                    if st.button("해제", key=f"unequip_{acc_id}", use_container_width=True):
                        equipped.remove(acc_id); pet['accessories']=equipped
                        save_pet(uid,pet); st.rerun()
                else:
                    if st.button("구매·장착", key=f"buy_acc_{acc_id}", use_container_width=True):
                        if len(equipped)>=2: st.error("최대 2개!")
                        elif st.session_state.global_cash < acc['price']: st.error("현금 부족!")
                        else:
                            st.session_state.global_cash -= acc['price']
                            atomic_deduct_cash(uid, acc['price'])
                            equipped.append(acc_id); pet['accessories']=equipped
                            save_pet(uid,pet); sync_user_data()
                            log_tx(uid,"펫",f"{pet['name']} 악세서리: {acc['name']}",-acc['price'])
                            add_journal(pet, f"👗 {acc['name']} 장착!")
                            st.toast(f"🎉 {acc['name']} 장착!", icon="✅"); st.rerun()

    # ── TAB 6: 스킬
    with tabs[5]:
        st.markdown('<div class="pet-tab-header">📜 펫 스킬</div>', unsafe_allow_html=True)
        sk_cols = st.columns(5)
        for i,skill in enumerate(PET_SKILLS):
            unlocked = lv >= skill['level']
            with sk_cols[i%5]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;
                    {"border-color:#00E5FF;background:rgba(0,229,255,0.07);" if unlocked else "opacity:0.4;"}'>
                    <div style='font-size:1.8rem;'>{skill['icon']}</div>
                    <div style='color:#E2E8F0;font-size:0.82rem;font-weight:700;margin-top:6px;'>{skill['name']}</div>
                    <div style='color:#64748B;font-size:0.7rem;margin-top:3px;'>{skill['desc']}</div>
                    <div style='color:{"#FFD600" if unlocked else "#475569"};font-size:0.7rem;margin-top:6px;font-weight:700;'>
                        {"✅ 해금" if unlocked else f"🔒 Lv.{skill['level']}"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 7: 업적
    with tabs[6]:
        st.markdown('<div class="pet-tab-header">🏆 펫 업적</div>', unsafe_allow_html=True)
        earned_ids = pet.get('achievements',[])
        earned_count = len(earned_ids)
        total_count  = len(PET_ACHIEVEMENTS)
        st.markdown(f"""
        <div style='background:rgba(255,214,0,0.06);border:1px solid #FFD60033;
                    border-radius:12px;padding:14px;margin-bottom:16px;text-align:center;'>
            <div style='color:#FFD600;font-size:1.4rem;font-weight:900;'>{earned_count}/{total_count}</div>
            <div style='color:#94A3B8;font-size:0.85rem;margin-top:4px;'>업적 달성</div>
            <div style='background:rgba(255,255,255,0.08);border-radius:4px;height:6px;margin-top:10px;overflow:hidden;'>
                <div style='background:#FFD600;width:{int(earned_count/total_count*100)}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ach_cols = st.columns(3)
        for i, ach in enumerate(PET_ACHIEVEMENTS):
            has = ach['id'] in earned_ids
            with ach_cols[i%3]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;
                    {"border-color:#FFD600;background:rgba(255,214,0,0.06);" if has else "opacity:0.45;"}'>
                    <div style='font-size:2rem;'>{ach['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;font-size:0.9rem;'>{ach['name']}</div>
                    <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>{ach['desc']}</div>
                    <div style='color:{"#FFD600" if has else "#475569"};font-size:0.75rem;margin-top:6px;font-weight:700;'>
                        {"✅ 달성!" if has else "🔒 미달성"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 8: 일지
    with tabs[7]:
        st.markdown('<div class="pet-tab-header">📖 펫 일지</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">펫과의 활동 기록이 자동으로 남습니다.</div>', unsafe_allow_html=True)
        journal = pet.get('journal', [])
        if not journal:
            st.markdown("<div style='text-align:center;color:#475569;padding:30px;'>아직 기록이 없어요. 펫과 함께 활동해보세요!</div>", unsafe_allow_html=True)
        else:
            for entry in journal[:30]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03);border-left:2px solid {sp["rarity_color"]}44;
                            padding:8px 14px;margin-bottom:6px;border-radius:0 8px 8px 0;
                            color:#B0BAC8;font-size:0.84rem;'>
                    {entry}
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 9: 정보/분양
    with tabs[8]:
        st.markdown('<div class="pet-tab-header">📊 펫 상세 정보</div>', unsafe_allow_html=True)
        equipped = pet.get('accessories',[])
        pet_skills_list = pet.get('skills',[])
        info_rows = [
            ("🐾 종류",      sp['name']),
            ("📛 이름",      pet['name']),
            ("🌟 성격",      pet.get('personality','?')),
            ("🎂 탄생일",    pet.get('birth_date','?')),
            ("⚡ 레벨/단계", f"Lv.{lv} ({stage.upper()})"),
            ("🧬 총 EXP",    f"{pet.get('total_exp_gained',0):,}"),
            ("🍖 총 먹인 횟수", f"{pet.get('total_fed',0):,}회"),
            ("💕 유대감",    get_bond_title(bond_lv)),
            ("🗺️ 탐험 횟수", f"{pet.get('expeditions',0)}회"),
            ("⚔️ 배틀 전적", f"{pet.get('battles_won',0)}승 / {pet.get('battles_total',0)}전"),
            ("💰 패시브 수입", format_korean_money(passive)+"/h" if passive>0 else "미해금 (Lv.20~)"),
            ("👗 장착 악세서리", ", ".join(PET_ACCESSORIES[a]['name'] for a in equipped if a in PET_ACCESSORIES) or "없음"),
            ("📜 보유 스킬",  ", ".join(pet_skills_list) or "없음"),
            ("🏆 달성 업적",  f"{len(pet.get('achievements',[]))}/{len(PET_ACHIEVEMENTS)}"),
        ]
        for label, val in info_rows:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,0.05);'>
                <span style='color:#64748B;'>{label}</span>
                <span style='color:#E2E8F0;font-weight:700;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        # Species ability
        st.markdown(f"""
        <div style='margin-top:16px;background:rgba(255,255,255,0.04);border:1px solid {sp["rarity_color"]}33;
                    border-radius:12px;padding:14px;'>
            <div style='color:{sp["rarity_color"]};font-weight:900;margin-bottom:6px;'>🎯 종족 고유 능력</div>
            <div style='color:#E2E8F0;'>{sp["ability"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### 🔴 펫 분양")
        st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;margin-bottom:12px;'>⚠️ 분양 시 펫이 영구히 사라집니다. 보상: 입양 금액의 30%</div>", unsafe_allow_html=True)
        release_price = int(sp['price'] * 0.3)
        if st.button(f"💔 {pet['name']} 분양하기 (보상: {format_korean_money(release_price)})", key="release_pet"):
            st.session_state['confirm_release'] = True
        if st.session_state.get('confirm_release'):
            st.warning("정말 분양하시겠어요? 되돌릴 수 없습니다!")
            cc1, cc2 = st.columns(2)
            if cc1.button("✅ 최종 확인, 분양", use_container_width=True, key="confirm_yes"):
                st.session_state.global_cash += release_price
                atomic_add_cash(uid, release_price)
                save_pet(uid, default_pet())
                sync_user_data()
                log_tx(uid,"펫",f"{pet['name']} 분양",release_price)
                del st.session_state['confirm_release']
                st.toast(f"💔 {pet['name']}이(가) 떠났어요...", icon="🐾")
                st.rerun()
            if cc2.button("❌ 취소", use_container_width=True, key="confirm_no"):
                del st.session_state['confirm_release']
                st.rerun()
