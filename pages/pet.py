# pages/pet.py — MEGA ULTIMATE EDITION v7.0 🐾
# v7 업그레이드:
#   · 신규 펫 3종 (불꽃 여우🔥, 우주 고래🐋, 강철 골렘🤖)
#   · 스탯 영구 강화 시스템 (ATK/DEF/HP/SPD/LUCK)
#   · 일일 & 주간 미션 시스템 (매일/매주 리셋, 현금 보상)
#   · 탐험 랜덤 이벤트 (보물/함정/회복/몬스터/행운)
#   · 배틀 버그 수정 (HP 저장 정확화, 독 시스템 추가)
#   · 강화 탭 추가 (스탯 업그레이드)
#   · 우주 고래 패시브 수입 최강 보너스 +35%
#   · 골렘 강철 심장 DEF+40% HP보너스
#   · 포토카드에 ATK/DEF 스탯 표시
#   · 미션 액션 카운터 (_add_action 시스템)
import streamlit as st
import requests as _req
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
                "ability":"화염 브레스 — 배틀 시 추가 화염 데미지",
                "special_skill":{"name":"🔥 화염 폭풍","desc":"전체 화염 데미지 ×3.0 + 크리티컬 확정","dmg_mult":3.0,"crit":True,"cooldown":5},
                "season_comment":{"봄":"봄비에 날개가 젖어 짜증나...","여름":"더위? 내가 더 뜨거운데?","가을":"낙엽이 불타는 것 같아서 기분 좋아!","겨울":"눈을 불로 녹여줄게!"},
                "weather_comment":{"맑음":"화창한 날엔 하늘 높이 날고 싶어!","비":"비는... 별로야.","눈":"눈밭에서 뒹굴고 싶어!","흐림":"흐린 날엔 그냥 자고 싶어..."}},
    "wolf":    {"name":"황금 늑대", "egg":"🥚","baby":"🐺","adult":"🦊","legend":"⭐",
                "desc":"황금빛 모피의 신비 늑대. 광산 보너스!",
                "price":100_000_000,"rarity":"희귀","rarity_color":"#FFD600",
                "ability":"황금 발톱 — 광산 수입 +15%",
                "special_skill":{"name":"⚡ 황금 질주","desc":"초고속 2연타 ×1.6 + 회피율 상승","dmg_mult":1.6,"crit":False,"cooldown":3},
                "season_comment":{"봄":"봄 바람에 털이 날려~ 아름다워!","여름":"더운 여름엔 개울가가 최고야!","가을":"추수철엔 먹을 게 많아서 좋아!","겨울":"눈밭 질주가 제일 신나!"},
                "weather_comment":{"맑음":"황금빛 햇살이 내 털에 반짝여!","비":"비 냄새... 뭔가 사냥하고 싶어진다!","눈":"눈밭 달리기 최고!","흐림":"흐린 날엔 멀리서 뭔가 냄새가 나..."}},
    "penguin": {"name":"황제 펭귄", "egg":"🥚","baby":"🐧","adult":"🐧","legend":"👑",
                "desc":"남극의 황제. 주식 투자 행운!",
                "price":50_000_000,"rarity":"고급","rarity_color":"#00E5FF",
                "ability":"빙하 방패 — 배틀 방어력 +20%",
                "special_skill":{"name":"❄️ 빙결 포격","desc":"빙하 폭발! ×2.2 + 상대 다음 공격력 -50%","dmg_mult":2.2,"crit":False,"cooldown":4},
                "season_comment":{"봄":"따뜻해지면 빙하가 녹아서 슬퍼...","여름":"더위 너무 싫어!! 에어컨 틀어줘!","가을":"이 정도 온도가 딱 좋아!","겨울":"겨울이 최고야! 나의 계절이야!"},
                "weather_comment":{"맑음":"햇빛이 빙하에 반짝여서 예뻐!","비":"비보다 눈이 좋은데...","눈":"눈이다!! 신나!!","흐림":"흐린 날엔 바다 보며 멍 때리기~"}},
    "cat":     {"name":"럭키 고양이","egg":"🥚","baby":"🐱","adult":"🐈","legend":"🍀",
                "desc":"행운을 부르는 신비한 고양이.",
                "price":10_000_000,"rarity":"일반","rarity_color":"#00FF88",
                "ability":"럭키 포 — 퀘스트 보상 +10%",
                "special_skill":{"name":"🍀 행운의 발톱","desc":"랜덤 배율 ×0.5~4.0! 운에 맡겨라","dmg_mult":2.0,"crit":False,"cooldown":3},
                "season_comment":{"봄":"봄 햇살 아래 낮잠이 최고야~ 냐옹","여름":"여름엔 시원한 데 누워있을 거야.","가을":"가을 바람이 시원해서 산책하기 좋아!","겨울":"이불 속이 최고야! 나올 생각 없어."},
                "weather_comment":{"맑음":"햇살 가득한 창가가 최애 자리야~","비":"비는 싫어! 창문이나 보고 있을게.","눈":"눈은 신기해... 잡으려다가 녹더라.","흐림":"흐린 날엔 그냥 하루 종일 잘 거야."}},
    "unicorn": {"name":"유니콘",    "egg":"🥚","baby":"🦄","adult":"🦄","legend":"🌈",
                "desc":"무지개빛 유니콘. 코인 거래 보너스!",
                "price":200_000_000,"rarity":"영웅","rarity_color":"#DD00FF",
                "ability":"무지개 마법 — 코인 수익 +12%",
                "special_skill":{"name":"🌈 오로라 폭발","desc":"무지개 폭발 ×2.5 + HP 10 회복","dmg_mult":2.5,"crit":True,"cooldown":5},
                "season_comment":{"봄":"봄꽃밭에서 뛰어놀고 싶어!","여름":"무지개가 자주 떠서 여름이 좋아!","가을":"단풍빛이 내 갈기랑 비슷해!","겨울":"흰 눈밭에 무지개 발자국 남기기!"},
                "weather_comment":{"맑음":"무지개가 잘 보이는 날이야!","비":"비 뒤에 무지개가 뜰 거야, 기다려!","눈":"눈 위를 달리면 무지개 먼지가 나!","흐림":"흐린 날엔 내가 빛이 되어줄게!"}},
    "phoenix": {"name":"불사조",    "egg":"🔥","baby":"🐦","adult":"🦅","legend":"🌟",
                "desc":"불사의 새. 강화 보너스!",
                "price":300_000_000,"rarity":"영웅","rarity_color":"#FF9500",
                "ability":"불사 재생 — HP 자동 회복 2배",
                "special_skill":{"name":"☀️ 피닉스 버스트","desc":"재생의 불꽃 ×2.8 + HP 15 회복","dmg_mult":2.8,"crit":True,"cooldown":5},
                "season_comment":{"봄":"봄에 다시 태어나는 기분이야!","여름":"뜨거운 여름이 내 본령이야!","가을":"타오르는 단풍처럼 아름다워!","겨울":"내 불꽃이 가장 빛나는 계절!"},
                "weather_comment":{"맑음":"맑은 하늘을 날고 싶어!","비":"빗물이 내 불꽃을 끄려 하지만... 절대 못 꺼!","눈":"눈을 녹이며 나는 게 최고야!","흐림":"흐린 날에도 내 불꽃은 꺼지지 않아!"}},
    "slime":   {"name":"황금 슬라임","egg":"🟡","baby":"🫧","adult":"💛","legend":"💰",
                "desc":"돈 먹고 자라는 슬라임. 패시브 수입 증가!",
                "price":30_000_000,"rarity":"고급","rarity_color":"#FFEE00",
                "ability":"황금 흡수 — 패시브 수입 +20%",
                "special_skill":{"name":"💰 황금 용해","desc":"황금 도포 ×2.0 + 이번 배틀 현금 보너스","dmg_mult":2.0,"crit":False,"cooldown":3},
                "season_comment":{"봄":"봄비에 몸이 퉁퉁 불어서 좋아~","여름":"뜨거우면 녹을 것 같아... 그늘 줘!","가을":"낙엽이 나한테 달라붙어 귀찮아.","겨울":"눈이 오면 얼어붙을 것 같아 무서워!"},
                "weather_comment":{"맑음":"햇살에 반짝반짝 빛나는 게 좋아!","비":"빗물이 맛있어! (핥아봄)","눈":"차가워... 빨리 녹아줘!","흐림":"흐린 날엔 코인이나 먹을게."}},
    "fox":     {"name":"구미호",    "egg":"🥚","baby":"🦊","adult":"🦊","legend":"🌙",
                "desc":"아홉 꼬리 여우. 도박 보너스!",
                "price":150_000_000,"rarity":"희귀","rarity_color":"#FF6699",
                "ability":"미혹의 눈 — 도박 승률 +5%",
                "special_skill":{"name":"🌙 구미 환상","desc":"환상 기만 ×2.6 + 크리티컬 확정","dmg_mult":2.6,"crit":True,"cooldown":4},
                "season_comment":{"봄":"봄밤에 달빛이 아름다워...","여름":"여름 축제에서 미혹시키기 딱 좋아!","가을":"보름달 아래서 춤추는 가을이 최고야!","겨울":"눈 덮인 달밤에 꼬리가 아홉 개 빛나~"},
                "weather_comment":{"맑음":"맑은 날엔 꼬리가 더 예뻐 보여!","비":"비 오는 날 밤엔 신비로운 기운이 넘쳐!","눈":"눈 위에 발자국 남기는 걸 좋아해.","흐림":"흐린 날 안개 속이 내 무대야!"}},
    # ── v6 신규 종족 ──
    "rabbit":  {"name":"럭키 래빗", "egg":"🥚","baby":"🐰","adult":"🐇","legend":"🌠",
                "desc":"달나라 행운 토끼! 가챠·이벤트 보너스 + 초고속 연타기.",
                "price":80_000_000,"rarity":"희귀","rarity_color":"#A8EDEA",
                "ability":"달빛 도약 — 탐험 희귀 아이템 확률 +8%",
                "special_skill":{"name":"🌕 달빛 연타","desc":"초고속 5연타! 총 데미지 ×3.5","dmg_mult":3.5,"crit":False,"cooldown":5},
                "season_comment":{"봄":"봄 달밤에 방아 찧는 게 너무 신나!","여름":"여름엔 수박이 최고야~ 냠냠!","가을":"추석 보름달이 제일 커서 좋아!","겨울":"눈밭에서 깡충깡충 뛰는 게 재밌어!"},
                "weather_comment":{"맑음":"달이 잘 보여서 기분 최고야!","비":"비 맞으면 귀가 축 처져...","눈":"눈 위 발자국 귀엽지 않아?","흐림":"달이 안 보여서 슬퍼."}},
    "seahorse":{"name":"레인보우 해마","egg":"🥚","baby":"🌊","adult":"🦭","legend":"🌈",
                "desc":"무지개빛 해마. 색이 바뀌는 신비한 존재!",
                "price":120_000_000,"rarity":"희귀","rarity_color":"#7B61FF",
                "ability":"색채 마력 — 패시브 수입 +10% & 방어력 보너스",
                "special_skill":{"name":"🌊 프리즘 웨이브","desc":"무지개 파도 ×2.1 + 3턴 독 (매 턴 20HP)","dmg_mult":2.1,"crit":False,"cooldown":4},
                "season_comment":{"봄":"봄 바닷물이 따뜻해서 좋아!","여름":"여름 바다가 내 무대야!","가을":"파도 소리 들으면서 쉬는 게 최고!","겨울":"찬 바다에서도 난 괜찮아!"},
                "weather_comment":{"맑음":"맑은 날엔 몸 색이 더 예뻐!","비":"빗방울이 바다랑 섞이는 게 신기해!","눈":"눈꽃이 바다에 녹는 걸 보고 있어.","흐림":"흐린 날엔 몸 색이 어둡게 변해."}},
    # ── v7 신규 종족 ──
    "firebird":{"name":"불꽃 여우",  "egg":"🔥","baby":"🦊","adult":"🦊","legend":"🌋",
                "desc":"화염을 다루는 신비한 여우. 배틀+도박 동시 보너스!",
                "price":180_000_000,"rarity":"영웅","rarity_color":"#FF3D00",
                "ability":"업화 — 배틀 ATK +20% & 도박 승률 +3%",
                "special_skill":{"name":"🌋 업화 폭발","desc":"화염 연타 ×3.2 + 상대 2턴 화상(매 턴 15HP)","dmg_mult":3.2,"crit":True,"cooldown":5},
                "season_comment":{"봄":"봄꽃보다 내 불꽃이 더 예뻐!","여름":"뜨거운 여름... 나도 뜨겁지만!","가을":"단풍도 나처럼 불타는 거야.","겨울":"내 불꽃으로 겨울을 녹여줄게!"},
                "weather_comment":{"맑음":"맑은 날엔 불꽃이 더 선명해!","비":"비에도 내 불꽃은 안 꺼져!","눈":"눈 위에서 불꽃 피우기~","흐림":"흐려도 내가 빛이 되어줄게!"}},
    "whale":   {"name":"우주 고래",  "egg":"🥚","baby":"🐋","adult":"🐋","legend":"🌌",
                "desc":"은하를 헤엄치는 거대한 고래. 최강 패시브 수입!",
                "price":800_000_000,"rarity":"전설","rarity_color":"#00CFFF",
                "ability":"은하 조류 — 패시브 수입 +35% (최고 보너스!)",
                "special_skill":{"name":"🌊 은하 파도","desc":"우주 에너지 ×4.0! 전설급 데미지","dmg_mult":4.0,"crit":True,"cooldown":7},
                "season_comment":{"봄":"봄 은하수가 따뜻해서 좋아~","여름":"우주에선 항상 여름이야!","가을":"별빛이 쏟아지는 가을 밤이 최고!","겨울":"우주 얼음 속에서도 따뜻해."},
                "weather_comment":{"맑음":"맑은 날엔 지구 하늘이 예뻐!","비":"빗소리가 파도 소리 같아서 좋아.","눈":"눈결정이 우주 먼지 같아~","흐림":"구름 위로 날아가면 맑아!"}},
    "golem":   {"name":"강철 골렘",  "egg":"⚙️","baby":"🤖","adult":"🤖","legend":"🛡️",
                "desc":"철과 마법으로 만들어진 수호자. 최강 방어력!",
                "price":250_000_000,"rarity":"영웅","rarity_color":"#8899AA",
                "ability":"강철 심장 — 배틀 DEF +40% & HP 최대치 +30",
                "special_skill":{"name":"⚙️ 핵폭권","desc":"강철 주먹 ×2.9 + 자신 HP 30 회복","dmg_mult":2.9,"crit":False,"cooldown":4},
                "season_comment":{"봄":"봄 비에 녹 슬면 안 되는데...","여름":"열 받으면 오히려 강해지지!","가을":"낙엽이 나에게 쌓여도 안 움직여.","겨울":"추워도 끄떡없어. 나 강철이잖아."},
                "weather_comment":{"맑음":"맑은 날엔 철갑이 빛나!","비":"녹슬지 않게 조심해야지...","눈":"무거워서 안 움직이는 게 낫겠어.","흐림":"흐려도 나는 튼튼해!"}},
    # ── v7 신규 종족 ──
    "firebird":{"name":"불꽃 여우",  "egg":"🔥","baby":"🦊","adult":"🦊","legend":"🌋",
                "desc":"화염을 다루는 신비한 여우. 도박+배틀 동시 보너스!",
                "price":180_000_000,"rarity":"영웅","rarity_color":"#FF3D00",
                "ability":"업화 — 배틀 ATK +20% & 도박 승률 +3%",
                "special_skill":{"name":"🌋 업화 폭발","desc":"화염 연타 ×3.2 + 상대 2턴 화상(매 턴 15HP)","dmg_mult":3.2,"crit":True,"cooldown":5},
                "season_comment":{"봄":"봄꽃보다 내 불꽃이 더 예뻐!","여름":"뜨거운 여름... 나도 뜨겁지만!","가을":"단풍도 나처럼 불타는 거야.","겨울":"내 불꽃으로 겨울을 녹여줄게!"},
                "weather_comment":{"맑음":"맑은 날엔 불꽃이 더 선명해!","비":"비에도 내 불꽃은 안 꺼져!","눈":"눈 위에서 춤추듯 불꽃 피우기~","흐림":"흐려도 내가 빛이 되어줄게!"}},
    "whale":   {"name":"우주 고래",  "egg":"🥚","baby":"🐋","adult":"🐋","legend":"🌌",
                "desc":"은하를 헤엄치는 거대한 고래. 최강 패시브 수입 +35%!",
                "price":800_000_000,"rarity":"전설","rarity_color":"#00CFFF",
                "ability":"은하 조류 — 패시브 수입 +35% (역대 최고 보너스!)",
                "special_skill":{"name":"🌊 은하 파도","desc":"우주 에너지 ×4.0! 전설급 데미지","dmg_mult":4.0,"crit":True,"cooldown":7},
                "season_comment":{"봄":"봄 은하수가 따뜻해서 좋아~","여름":"우주에선 항상 여름이야!","가을":"별빛이 쏟아지는 가을 밤이 최고!","겨울":"우주 얼음 속에서도 따뜻해."},
                "weather_comment":{"맑음":"맑은 날엔 지구 하늘이 예뻐!","비":"빗소리가 파도 소리 같아서 좋아.","눈":"눈결정이 우주 먼지 같아~","흐림":"구름 위로 날아가면 맑아!"}},
    "golem":   {"name":"강철 골렘",  "egg":"⚙️","baby":"🤖","adult":"🤖","legend":"🛡️",
                "desc":"철과 마법으로 만들어진 수호자. 역대 최강 방어력!",
                "price":250_000_000,"rarity":"영웅","rarity_color":"#8899AA",
                "ability":"강철 심장 — 배틀 DEF +40% & HP 최대치 +30",
                "special_skill":{"name":"⚙️ 핵폭권","desc":"강철 주먹 ×2.9 + 자신 HP 30 회복","dmg_mult":2.9,"crit":False,"cooldown":4},
                "season_comment":{"봄":"봄 비에 녹 슬면 안 되는데...","여름":"열 받으면 오히려 강해지지!","가을":"낙엽이 나에게 쌓여도 안 움직여.","겨울":"추워도 끄떡없어. 나 강철이잖아."},
                "weather_comment":{"맑음":"맑은 날엔 철갑이 빛나!","비":"녹슬지 않게 조심해야지...","눈":"무거워서 안 움직이는 게 낫겠어.","흐림":"흐려도 나는 튼튼해!"}},

}

PET_FOOD = {
    "kibble":    {"name":"일반 사료",    "icon":"🍖","price":500_000,     "exp":10,  "happiness":5,  "hunger_restore":15, "hp_restore":0},
    "gourmet":   {"name":"고급 사료",    "icon":"🥩","price":2_000_000,   "exp":40,  "happiness":15, "hunger_restore":30, "hp_restore":0},
    "premium":   {"name":"프리미엄 사료","icon":"🍗","price":8_000_000,   "exp":100, "happiness":30, "hunger_restore":50, "hp_restore":0},
    "stardust":  {"name":"별의 가루",    "icon":"✨","price":50_000_000,  "exp":500, "happiness":50, "hunger_restore":100,"hp_restore":0},
    "dragonmeat":{"name":"용의 심장",   "icon":"💎","price":200_000_000, "exp":2000,"happiness":80, "hunger_restore":100,"hp_restore":0},
    "moonberry": {"name":"달빛 열매",    "icon":"🫐","price":20_000_000,  "exp":200, "happiness":40, "hunger_restore":60, "hp_restore":0},
    # v6 신규 — 포션/회복 아이템
    "potion_s":  {"name":"소형 포션",   "icon":"🧪","price":3_000_000,   "exp":0,   "happiness":5,  "hunger_restore":0,  "hp_restore":25},
    "potion_l":  {"name":"대형 포션",   "icon":"💊","price":15_000_000,  "exp":0,   "happiness":10, "hunger_restore":0,  "hp_restore":60},
    "elixir":    {"name":"전설의 영약", "icon":"⚗️","price":100_000_000, "exp":300, "happiness":50, "hunger_restore":30, "hp_restore":100},
    "galaxy_feed":{"name":"은하수 사료","icon":"🌌","price":500_000_000, "exp":8000,"happiness":100,"hunger_restore":100,"hp_restore":100},
    "candy":     {"name":"행복 캔디",   "icon":"🍬","price":1_000_000,   "exp":5,   "happiness":25, "hunger_restore":5,  "hp_restore":0},
    # v7 신규
    "galaxy_feed":{"name":"은하수 사료","icon":"🌌","price":500_000_000, "exp":8000,"happiness":100,"hunger_restore":100,"hp_restore":100},
    "candy":      {"name":"행복 캔디",  "icon":"🍬","price":1_000_000,   "exp":5,   "happiness":25, "hunger_restore":5,  "hp_restore":0},
}

PET_ACCESSORIES = {
    "collar": {"name":"황금 목걸이","icon":"📿","price":20_000_000,  "desc":"행운 +5%",      "bonus_type":"luck",   "bonus":5},
    "hat":    {"name":"왕관 모자",  "icon":"👑","price":50_000_000,  "desc":"EXP +10%",     "bonus_type":"exp",    "bonus":10},
    "armor":  {"name":"미스릴 갑옷","icon":"🛡️","price":100_000_000, "desc":"수입 +8%",     "bonus_type":"income", "bonus":8},
    "wings":  {"name":"불사의 날개","icon":"🦋","price":200_000_000, "desc":"행복도 유지", "bonus_type":"happy",  "bonus":20},
    "gem":    {"name":"드래곤 젬",  "icon":"💎","price":500_000_000, "desc":"모든 보너스+5%","bonus_type":"all", "bonus":5},
    "amulet": {"name":"별빛 부적",  "icon":"🔮","price":80_000_000,  "desc":"배틀 ATK+15%","bonus_type":"battle","bonus":15},
    "ribbon":  {"name":"행운의 리본","icon":"🎀","price":15_000_000,  "desc":"탐험 보상+10%", "bonus_type":"exp",    "bonus":10},
    "crystal": {"name":"달빛 크리스탈","icon":"🔷","price":60_000_000, "desc":"HP 감소 완화",  "bonus_type":"hp",     "bonus":30},
    "galaxy_stone":{"name":"은하 원석","icon":"🌠","price":300_000_000,"desc":"배틀 ALL+10%","bonus_type":"all","bonus":10},
    "iron_core":{"name":"강철 심핵","icon":"⚙️","price":150_000_000,"desc":"DEF +20%","bonus_type":"def","bonus":20},
    # v7 신규
    "galaxy_stone":{"name":"은하 원석","icon":"🌠","price":300_000_000,"desc":"배틀 ALL+10%","bonus_type":"all","bonus":10},
    "iron_core":{"name":"강철 심핵",  "icon":"⚙️","price":150_000_000,"desc":"DEF +20%",    "bonus_type":"def","bonus":20},
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
    # v7 신규 보스
    {"name":"강철 거인",   "icon":"🤖","hp":280,"atk":70, "def":60, "reward_exp":500, "reward_cash":30_000_000, "lv_req":30},
    {"name":"은하 수호자", "icon":"🌊","hp":700,"atk":120,"def":90, "reward_exp":2000,"reward_cash":500_000_000,"lv_req":50},
    # v9 신규: 만렙(5000) 체계 대응 고레벨 보스 (고레벨일수록 보상 폭증)
    {"name":"심연의 군주",   "icon":"🦑","hp":1500,  "atk":260,  "def":160,  "reward_exp":6000,    "reward_cash":2_000_000_000,    "lv_req":200},
    {"name":"화염 타이탄",   "icon":"🌋","hp":3000,  "atk":450,  "def":280,  "reward_exp":15000,   "reward_cash":8_000_000_000,    "lv_req":500},
    {"name":"서리 드레이크", "icon":"🐉","hp":6000,  "atk":800,  "def":500,  "reward_exp":40000,   "reward_cash":30_000_000_000,   "lv_req":1000},
    {"name":"공허 포식자",   "icon":"🕳️","hp":13000, "atk":1500, "def":900,  "reward_exp":110000,  "reward_cash":100_000_000_000,  "lv_req":2000},
    {"name":"시공의 지배자", "icon":"⏳","hp":28000, "atk":2800, "def":1700, "reward_exp":300000,  "reward_cash":400_000_000_000,  "lv_req":3000},
    {"name":"창세의 용",     "icon":"🌠","hp":60000, "atk":5000, "def":3200, "reward_exp":800000,  "reward_cash":1_500_000_000_000,"lv_req":4000},
    {"name":"종말의 신",     "icon":"👁️","hp":150000,"atk":9999, "def":6000, "reward_exp":2500000, "reward_cash":5_000_000_000_000,"lv_req":5000},
]

PET_ACHIEVEMENTS = [
    {"id":"first_feed",    "icon":"🍖","name":"첫 식사",      "desc":"처음으로 먹이를 줬다",       "reward":500_000},
    {"id":"well_fed",      "icon":"🤤","name":"맛있겠다",     "desc":"총 50번 먹이기 완료",         "reward":2_000_000},
    {"id":"feast",         "icon":"🏆","name":"미식가",       "desc":"총 500번 먹이기 완료",        "reward":10_000_000},
    {"id":"lv10",          "icon":"⚡","name":"성장통",       "desc":"레벨 10 달성",                "reward":5_000_000},
    {"id":"lv25",          "icon":"🌟","name":"영웅의 탄생",  "desc":"레벨 25 달성",                "reward":20_000_000},
    {"id":"lv50",          "icon":"🌌","name":"전설이 되다",  "desc":"레벨 50 달성",                "reward":100_000_000},
    {"id":"happy_max",     "icon":"😊","name":"행복 만점",    "desc":"행복도 100 달성",              "reward":1_000_000},
    {"id":"explorer1",     "icon":"🗺️","name":"탐험가",       "desc":"첫 탐험 완료",                "reward":1_000_000},
    {"id":"explorer10",    "icon":"🌍","name":"세계 정복자",  "desc":"탐험 10회 완료",               "reward":15_000_000},
    {"id":"battle_win1",   "icon":"⚔️","name":"첫 승리",      "desc":"배틀 첫 승리",                 "reward":500_000},
    {"id":"battle_win10",  "icon":"🏅","name":"전투의 달인",  "desc":"배틀 10승",                    "reward":8_000_000},
    {"id":"hatched",       "icon":"🐣","name":"탄생의 기적",  "desc":"알에서 부화 (Lv.5)",           "reward":500_000},
    {"id":"bonded",        "icon":"💕","name":"절친",         "desc":"유대감 레벨 3 달성",           "reward":3_000_000},
    {"id":"full_acc",      "icon":"👑","name":"풀 장착",      "desc":"악세서리 2개 장착",             "reward":5_000_000},
    {"id":"legend",        "icon":"🌌","name":"우주의 뜻",    "desc":"전설 단계 도달 (Lv.40)",        "reward":50_000_000},
    {"id":"petting30",     "icon":"🤗","name":"스킨십 왕",    "desc":"쓰다듬기 30회",                "reward":3_000_000},
    {"id":"skill_use5",    "icon":"⚡","name":"필살기 마스터","desc":"종족 필살기 5회 사용",          "reward":7_000_000},
    {"id":"chef",          "icon":"🧑‍🍳","name":"셰프",         "desc":"레시피 1회 제조",              "reward":2_000_000},
    {"id":"battler100",    "icon":"💪","name":"백전노장",      "desc":"배틀 100전",                   "reward":30_000_000},
    {"id":"battle_win50",  "icon":"🏆","name":"불패 전사",    "desc":"배틀 50승",                      "reward":30_000_000},
    {"id":"mission10",     "icon":"📋","name":"미션 헌터",    "desc":"일일/주간 미션 10회 완료",        "reward":15_000_000},
    {"id":"stat_max",      "icon":"💯","name":"완벽한 펫",    "desc":"스탯 강화 10회 달성",             "reward":25_000_000},
    {"id":"lv_100",        "icon":"👑","name":"신의 경지",    "desc":"레벨 100 달성",                   "reward":1_000_000_000},
    # v9 신규 업적 (만렙/진화/환생/룬)
    {"id":"lv_1000",       "icon":"🌟","name":"천 단위 돌파",  "desc":"레벨 1000 달성 (성체 진화)",       "reward":5_000_000_000},
    {"id":"lv_3000",       "icon":"💫","name":"초월의 시작",  "desc":"레벨 3000 달성 (초월체)",          "reward":30_000_000_000},
    {"id":"lv_max",        "icon":"👑","name":"창세신",       "desc":"만렙 5000 달성!",                  "reward":100_000_000_000},
    {"id":"evo_t3",        "icon":"🌟","name":"전설의 증명",  "desc":"전설체(Tier 3) 진화",              "reward":3_000_000_000},
    {"id":"rebirth1",      "icon":"♻️","name":"다시 태어나다","desc":"첫 환생 달성",                      "reward":50_000_000_000},
    {"id":"rebirth5",      "icon":"🌌","name":"윤회의 화신",  "desc":"환생 5회 달성",                     "reward":500_000_000_000},
    {"id":"rune_master",   "icon":"🔮","name":"룬 마스터",    "desc":"룬 하나를 MAX(Lv.50)까지 강화",     "reward":80_000_000_000},
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

# v8 신규: 타이밍 명중 미니게임 (연타 게임 대체)
TIMING_GAME = {"cost": 2_000_000, "base_exp": 60}

# v7 신규: 영구 스탯 강화
PET_STAT_UPGRADES = {
    "atk_up":  {"name":"ATK 강화",  "icon":"⚔️","desc":"기본 공격력 영구 +5","stat":"atk_bonus","cost":10_000_000, "max_lv":20},
    "def_up":  {"name":"DEF 강화",  "icon":"🛡️","desc":"기본 방어력 영구 +5","stat":"def_bonus","cost":8_000_000,  "max_lv":20},
    "hp_up":   {"name":"HP 강화",   "icon":"❤️","desc":"최대 HP +10",         "stat":"hp_bonus", "cost":5_000_000,  "max_lv":10},
    "spd_up":  {"name":"SPD 강화",  "icon":"💨","desc":"속도 영구 +3",        "stat":"spd_bonus","cost":6_000_000,  "max_lv":20},
    "luck_up": {"name":"행운 강화", "icon":"🍀","desc":"행운 +2%",            "stat":"luck_bonus","cost":12_000_000,"max_lv":10},
}

# ══════════════════════════════════════════════════════════════════════════════
# 🔮 v9: 룬 시스템 (룬 조각으로 강화, 배틀 스탯 직접 상승)
# ══════════════════════════════════════════════════════════════════════════════
PET_RUNES = {
    "rune_atk":  {"name":"분노의 룬",   "icon":"🔴","stat":"atk", "per_lv":30,  "max_lv":50, "shard_cost":5,  "desc":"레벨당 ATK +30"},
    "rune_def":  {"name":"수호의 룬",   "icon":"🔵","stat":"def", "per_lv":25,  "max_lv":50, "shard_cost":5,  "desc":"레벨당 DEF +25"},
    "rune_spd":  {"name":"질풍의 룬",   "icon":"🟢","stat":"spd", "per_lv":18,  "max_lv":50, "shard_cost":4,  "desc":"레벨당 SPD +18"},
    "rune_omni": {"name":"태초의 룬",   "icon":"🟣","stat":"all", "per_lv":20,  "max_lv":30, "shard_cost":12, "desc":"레벨당 전 스탯 +20"},
}

# 룬 조각 획득처 안내 (배틀/탐험/잭팟에서 드랍)
RUNE_SHARD_DROP = {"battle_win": (1, 3), "expedition": (2, 5), "jackpot": (3, 8)}

# ══════════════════════════════════════════════════════════════════════════════
# ♻️ v9: 환생(전직) 시스템
# ══════════════════════════════════════════════════════════════════════════════
#   만렙(5000) 도달 시 환생 가능. 레벨 1로 리셋되지만:
#   · 영구 EXP 배수 +10%/환생 · 영구 전 스탯 +15%/환생
#   · 환생 칭호 부여 · prestige_points 지급(특수 상점용)
#   ※ REBIRTH_REQ_LEVEL은 MAX_LEVEL 정의 이후(363줄 부근)에서 할당됩니다.
REBIRTH_TITLES = [
    "필멸자",       # 0
    "🥉 각성자",    # 1
    "🥈 초월자",    # 2
    "🥇 반신",      # 3
    "💠 신격",      # 4
    "🌟 천상신",    # 5
    "🌌 우주신",    # 6
    "♾️ 무한신",    # 7+
]
def get_rebirth_title(rb):
    return REBIRTH_TITLES[min(rb, len(REBIRTH_TITLES)-1)]

# ══════════════════════════════════════════════════════════════════════════════
# 🏅 v9: 프레스티지 상점 (환생 포인트로만 구매하는 영구 강화)
# ══════════════════════════════════════════════════════════════════════════════
PRESTIGE_SHOP = {
    "p_exp":   {"name":"영원한 지혜",   "icon":"📖","desc":"영구 EXP 획득 +25%",        "cost":1,  "stat":"p_exp",   "max":10},
    "p_income":{"name":"황금의 축복",   "icon":"💰","desc":"영구 패시브 수입 +30%",     "cost":1,  "stat":"p_income","max":10},
    "p_atk":   {"name":"파괴의 인장",   "icon":"⚔️","desc":"영구 ATK +50%",              "cost":2,  "stat":"p_atk",   "max":5},
    "p_luck":  {"name":"운명의 주사위", "icon":"🎲","desc":"영구 잭팟·희귀 확률 2배",    "cost":3,  "stat":"p_luck",  "max":3},
}

# v7 신규: 일일/주간 미션
DAILY_MISSIONS = [
    {"id":"dm_feed3",   "name":"오늘의 식사",   "desc":"오늘 3번 먹이기",    "target":3,  "type":"feed",    "reward":1_000_000},
    {"id":"dm_pet2",    "name":"스킨십 타임",   "desc":"오늘 2번 쓰다듬기",  "target":2,  "type":"petting", "reward":500_000},
    {"id":"dm_battle1", "name":"오늘의 도전",   "desc":"배틀 1회 승리",      "target":1,  "type":"battle",  "reward":2_000_000},
    {"id":"dm_train1",  "name":"열심히 훈련",   "desc":"훈련 1회 완료",      "target":1,  "type":"train",   "reward":800_000},
    {"id":"dm_chat3",   "name":"대화 나누기",   "desc":"펫과 3번 대화",      "target":3,  "type":"chat",    "reward":600_000},
]
WEEKLY_MISSIONS = [
    {"id":"wm_battle10","name":"격투가",        "desc":"이번 주 배틀 10승",  "target":10, "type":"battle",  "reward":15_000_000},
    {"id":"wm_feed30",  "name":"헌신적인 집사", "desc":"이번 주 먹이 30회",  "target":30, "type":"feed",    "reward":10_000_000},
    {"id":"wm_exp1",    "name":"탐험가 왕",     "desc":"탐험 1회 완료",      "target":1,  "type":"expedition","reward":8_000_000},
    {"id":"wm_lv_up",   "name":"빠른 성장",     "desc":"레벨업 2회",         "target":2,  "type":"levelup", "reward":20_000_000},
]

# v7 신규: 탐험 랜덤 이벤트
EXPEDITION_EVENTS = [
    {"name":"보물 발견!", "icon":"💎","desc":"숨겨진 보물!","cash_mult":2.5,"exp_mult":1.0,"hp_effect":0},
    {"name":"함정 발동!", "icon":"⚠️","desc":"함정! HP 감소","cash_mult":0.8,"exp_mult":1.0,"hp_effect":-20},
    {"name":"신비한 샘",  "icon":"💧","desc":"회복!","cash_mult":1.0,"exp_mult":1.2,"hp_effect":30},
    {"name":"몬스터 습격","icon":"👺","desc":"강한 몬스터!","cash_mult":1.5,"exp_mult":2.0,"hp_effect":-10},
    {"name":"행운의 별",  "icon":"⭐","desc":"행운의 별!","cash_mult":3.0,"exp_mult":1.5,"hp_effect":0},
    {"name":"평화로운 여행","icon":"🌸","desc":"평화로운 귀환","cash_mult":1.0,"exp_mult":1.0,"hp_effect":5},
]

EXP_PER_LEVEL = 200          # (레거시 호환용 — 실제 곡선은 exp_to_next 사용)

# ══════════════════════════════════════════════════════════════════════════════
# 🌟 v9: 만렙 / 진화 / 환생 시스템
# ══════════════════════════════════════════════════════════════════════════════
MAX_LEVEL = 5000                 # 만렙
REBIRTH_REQ_LEVEL = MAX_LEVEL    # 환생 가능 레벨 (MAX_LEVEL 정의 이후 할당)
EVO_INTERVAL = 1000              # 1000렙마다 진화

# 진화 단계 정의 (스테이지 수 = 6: egg, baby, adult, legend + 초월 2단계)
#   레벨대별 진화명/칭호/오라색. SVG 스프라이트 stage 키와 매핑.
EVOLUTION_STAGES = [
    {"min":0,    "stage":"egg",     "tier":0, "name":"알",       "title":"🥚 미부화",   "aura":"#94A3B8", "scale":1.00},
    {"min":5,    "stage":"baby",    "tier":1, "name":"새끼",     "title":"🐣 유년기",   "aura":"#00E5FF", "scale":1.00},
    {"min":1000, "stage":"adult",   "tier":2, "name":"성체",     "title":"⚔️ 성장기",   "aura":"#00FF88", "scale":1.05},
    {"min":2000, "stage":"legend",  "tier":3, "name":"전설",     "title":"🌟 전설체",   "aura":"#FFD600", "scale":1.10},
    {"min":3000, "stage":"legend",  "tier":4, "name":"초월",     "title":"💫 초월체",   "aura":"#DD00FF", "scale":1.16},
    {"min":4000, "stage":"legend",  "tier":5, "name":"신화",     "title":"🌌 신화체",   "aura":"#FF2D95", "scale":1.24},
    {"min":5000, "stage":"legend",  "tier":6, "name":"창세",     "title":"👑 창세신",   "aura":"#FF0044", "scale":1.34},
]

def get_evo(lv):
    """레벨에 해당하는 진화 단계 dict 반환."""
    cur = EVOLUTION_STAGES[0]
    for e in EVOLUTION_STAGES:
        if lv >= e["min"]:
            cur = e
        else:
            break
    return cur

def get_evo_tier(lv):
    return get_evo(lv)["tier"]

def exp_to_next(lv):
    """레벨업에 필요한 EXP — 레벨이 오를수록 완만히 증가.
    저레벨(1~40)은 기존(200 안팎)과 거의 같고, 고레벨로 갈수록 가파르게."""
    if lv < 1:
        return 100
    # 기본 200 + 레벨 비례 증가 + 약한 2차항. 만렙 근처에서 충분히 무겁게.
    return int(200 + lv * 35 + (lv ** 2) * 0.45)

def total_exp_for_level(target_lv):
    """1레벨부터 target_lv까지 도달에 필요한 누적 EXP (보정용)."""
    tot = 0
    for l in range(1, target_lv):
        tot += exp_to_next(l)
    return tot

# ── 계절 / 날씨
WEATHER_ICONS = {"맑음":"☀️","비":"🌧️","흐림":"☁️","눈":"❄️"}
SEASON_BG = {
    "봄":  {"particles":["🌸","🌺","🌷","💐","🦋"]},
    "여름":{"particles":["☀️","🌊","🌴","🍉","⭐"]},
    "가을":{"particles":["🍂","🍁","🌾","🎃","🍄"]},
    "겨울":{"particles":["❄️","⛄","🌨️","🔵","✨"]},
}

def get_season():
    m = datetime.now(KST).month
    if m in [3,4,5]:    return "봄",  "🌸"
    elif m in [6,7,8]:  return "여름","☀️"
    elif m in [9,10,11]:return "가을","🍂"
    else:               return "겨울","❄️"

def get_weather():
    """날짜 시드 기반 결정론적 날씨 (API 없이)"""
    today = datetime.now(KST)
    seed  = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    w = random.choice(["맑음","맑음","맑음","비","흐림","눈"])
    random.seed()
    return w

# ── 일일 펫 대화
DAILY_QUOTES = {
    "신남":   ["오늘 뭔가 좋은 일이 생길 것 같아!","나 요즘 너무 행복해!! 같이 뛰어놀자!","오늘은 탐험 가고 싶어! 어서 가자!","최고의 하루가 될 것 같은 느낌이야!"],
    "행복":   ["오늘 날씨가 딱 좋다~ 기분 굿!","맛있는 거 더 주면 안 돼? 히힝~","오늘 하루도 잘 부탁해!","같이 있으면 항상 기분이 좋아!"],
    "배고픔": ["배고파... 밥 줘... 제발...","먹이를 안 주면... 삐질 거야.","꼬르륵... 들려? 내 배 소리..."],
    "아픔":   ["몸이 안 좋아... 쉬고 싶어...","HP가 부족해... 회복 좀 해줘...","오늘은 배틀 하기 싫어. 아파..."],
    "피곤":   ["너무 피곤해... 좀 쉬자...","오늘은 그냥 같이 쉬면 안 돼?","훈련은 내일 하면 안 될까..."],
    "슬픔":   ["같이 놀아줘... 심심해...","왜 이렇게 혼자인 것 같지...","오늘 조금 슬퍼. 안아줘."],
    "보통":   ["오늘 뭐 할까?","탐험이나 갈까? 아니면 훈련?","그냥저냥 괜찮은 하루야.","뭔가 먹고 싶긴 한데..."],
}

def get_daily_quote(pet):
    """기분+종족+계절+날씨 조합 일일 한마디 (날짜 고정)"""
    mood_name, _ = get_mood(pet)
    quotes    = DAILY_QUOTES.get(mood_name, DAILY_QUOTES['보통'])
    sp_data   = PET_SPECIES.get(pet.get('species','cat'), {})
    season, _ = get_season()
    weather   = get_weather()
    seed = int(datetime.now(KST).strftime("%Y%m%d"))
    random.seed(seed)
    q = random.choice(quotes)
    extras = [sp_data.get('season_comment',{}).get(season,""),
              sp_data.get('weather_comment',{}).get(weather,"")]
    extras = [x for x in extras if x]
    extra  = f" ({random.choice(extras)})" if extras else ""
    random.seed()
    return q + extra

# ── 특수 먹이 레시피
SPECIAL_RECIPES = {
    "golden_meal": {
        "name":"황금 만찬","icon":"🌟",
        "desc":"일반 사료 + 고급 사료 + 달빛 열매 조합",
        "ingredients":{"kibble":1,"gourmet":1,"moonberry":1},
        "exp":800,"happiness":60,"hunger_restore":100,
        "special":"EXP 대폭 + 유대감 +10","bond_bonus":10,
    },
    "dragon_feast": {
        "name":"드래곤 향연","icon":"🔥",
        "desc":"용의 심장 + 별의 가루 + 프리미엄 사료 조합",
        "ingredients":{"dragonmeat":1,"stardust":1,"premium":1},
        "exp":5000,"happiness":100,"hunger_restore":100,
        "special":"EXP 대폭 + HP 완전 회복","bond_bonus":20,
    },
    "lucky_blend": {
        "name":"행운의 블렌드","icon":"🍀",
        "desc":"일반 사료 + 별의 가루 + 고급 사료 조합",
        "ingredients":{"kibble":1,"stardust":1,"gourmet":1},
        "exp":600,"happiness":80,"hunger_restore":80,
        "special":"행복도 대폭 상승 + 유대감 +15","bond_bonus":15,
    },
    # v7 신규
    "galaxy_potion": {
        "name":"은하수 포션","icon":"🌌",
        "desc":"은하수 사료 + 전설의 영약 조합 (초고급!)",
        "ingredients":{"galaxy_feed":1,"elixir":1},
        "exp":20000,"happiness":100,"hunger_restore":100,
        "special":"전설급 EXP + 완전 회복 + 유대감 +50","bond_bonus":50,
    },
}

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 SVG PET SPRITES — 치비 캐릭터 (알→새끼→성체→전설)
# ══════════════════════════════════════════════════════════════════════════════

def build_svg_sprites():
    """각 종별 단계별 SVG 문자열 반환"""

    DRAGON_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="dbg" cx="45%" cy="40%" r="60%"><stop offset="0%" stop-color="#ff9944"/><stop offset="100%" stop-color="#cc2200"/></radialGradient><radialGradient id="dbelly" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#ffcc88"/><stop offset="100%" stop-color="#ff8844"/></radialGradient></defs><path d="M62,85 Q80,95 78,105 Q72,100 68,92" fill="#cc2200"/><ellipse cx="50" cy="72" rx="28" ry="26" fill="url(#dbg)"/><ellipse cx="50" cy="76" rx="16" ry="14" fill="url(#dbelly)" opacity="0.85"/><ellipse cx="26" cy="78" rx="9" ry="7" fill="#cc2200" transform="rotate(-30,26,78)"/><circle cx="20" cy="83" r="5" fill="#bb1100"/><ellipse cx="74" cy="78" rx="9" ry="7" fill="#cc2200" transform="rotate(30,74,78)"/><circle cx="80" cy="83" r="5" fill="#bb1100"/><ellipse cx="37" cy="96" rx="10" ry="7" fill="#bb2200" transform="rotate(10,37,96)"/><ellipse cx="63" cy="96" rx="10" ry="7" fill="#bb2200" transform="rotate(-10,63,96)"/><circle cx="30" cy="101" r="3" fill="#991100"/><circle cx="36" cy="103" r="3" fill="#991100"/><circle cx="58" cy="103" r="3" fill="#991100"/><circle cx="64" cy="101" r="3" fill="#991100"/><ellipse cx="50" cy="50" rx="16" ry="14" fill="url(#dbg)"/><ellipse cx="50" cy="32" rx="24" ry="22" fill="url(#dbg)"/><path d="M38,14 L34,2 L42,12" fill="#ff6600"/><path d="M62,14 L66,2 L58,12" fill="#ff6600"/><ellipse cx="50" cy="38" rx="12" ry="8" fill="#ff8844"/><circle cx="46" cy="39" r="2" fill="#cc2200"/><circle cx="54" cy="39" r="2" fill="#cc2200"/><circle cx="40" cy="27" r="6" fill="#fff"/><circle cx="60" cy="27" r="6" fill="#fff"/><circle cx="41" cy="27" r="4" fill="#ff6600"/><circle cx="61" cy="27" r="4" fill="#ff6600"/><circle cx="42" cy="26" r="2" fill="#111"/><circle cx="62" cy="26" r="2" fill="#111"/><circle cx="43" cy="25" r="1" fill="#fff"/><circle cx="63" cy="25" r="1" fill="#fff"/><path d="M40,52 L36,42 L44,50" fill="#ff5500"/><path d="M50,48 L50,36 L54,47" fill="#ff5500"/><path d="M60,52 L64,42 L56,50" fill="#ff5500"/><ellipse cx="35" cy="34" rx="5" ry="3" fill="#ff6644" opacity="0.5"/><ellipse cx="65" cy="34" rx="5" ry="3" fill="#ff6644" opacity="0.5"/><path d="M22,60 Q10,48 18,42 Q26,50 28,62" fill="#ff4400" opacity="0.8"/><path d="M78,60 Q90,48 82,42 Q74,50 72,62" fill="#ff4400" opacity="0.8"/></svg>"""

    DRAGON_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="dag" cx="40%" cy="35%" r="65%"><stop offset="0%" stop-color="#ff7722"/><stop offset="100%" stop-color="#990000"/></radialGradient><filter id="dglow"><feGaussianBlur stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M18,55 Q-5,25 10,10 Q28,30 30,55" fill="#cc3300" opacity="0.9"/><path d="M20,55 Q2,28 14,14 Q30,34 32,55" fill="#ff5500" opacity="0.5"/><path d="M82,55 Q105,25 90,10 Q72,30 70,55" fill="#cc3300" opacity="0.9"/><path d="M80,55 Q98,28 86,14 Q70,34 68,55" fill="#ff5500" opacity="0.5"/><path d="M68,95 Q88,108 85,118 Q76,110 70,100" fill="#990000"/><path d="M85,118 L90,115 L83,112" fill="#ff4400"/><ellipse cx="50" cy="76" rx="30" ry="27" fill="url(#dag)"/><path d="M35,66 Q38,62 41,66" fill="none" stroke="#ff5500" stroke-width="1.5" opacity="0.6"/><path d="M45,62 Q48,58 51,62" fill="none" stroke="#ff5500" stroke-width="1.5" opacity="0.6"/><path d="M55,66 Q58,62 61,66" fill="none" stroke="#ff5500" stroke-width="1.5" opacity="0.6"/><ellipse cx="50" cy="80" rx="17" ry="15" fill="#ffaa66" opacity="0.7"/><path d="M22,72 Q10,78 12,90 Q18,86 24,80" fill="#cc2200"/><path d="M22,72 Q14,65 10,72 Q16,76 22,78" fill="#bb2200"/><path d="M12,90 L8,96 M12,90 L11,97 M12,90 L15,96" stroke="#ff6600" stroke-width="2" stroke-linecap="round"/><path d="M78,72 Q90,78 88,90 Q82,86 76,80" fill="#cc2200"/><path d="M78,72 Q86,65 90,72 Q84,76 78,78" fill="#bb2200"/><path d="M88,90 L92,96 M88,90 L89,97 M88,90 L85,96" stroke="#ff6600" stroke-width="2" stroke-linecap="round"/><path d="M34,98 Q28,108 32,116 Q38,110 40,100" fill="#bb1100"/><path d="M66,98 Q72,108 68,116 Q62,110 60,100" fill="#bb1100"/><path d="M32,116 L28,120 M32,116 L33,121 M32,116 L37,119" stroke="#ff4400" stroke-width="1.5" stroke-linecap="round"/><path d="M68,116 L72,120 M68,116 L67,121 M68,116 L63,119" stroke="#ff4400" stroke-width="1.5" stroke-linecap="round"/><ellipse cx="50" cy="53" rx="17" ry="14" fill="url(#dag)"/><path d="M42,45 L38,34 L46,44" fill="#ff4400"/><path d="M50,42 L50,30 L54,41" fill="#ff4400"/><path d="M58,45 L62,34 L54,44" fill="#ff4400"/><ellipse cx="50" cy="30" rx="26" ry="24" fill="url(#dag)"/><path d="M36,14 L28,-2 L40,12" fill="#ff5500"/><path d="M64,14 L72,-2 L60,12" fill="#ff5500"/><path d="M38,34 Q50,46 62,34 Q62,28 50,26 Q38,28 38,34" fill="#ff7744"/><circle cx="45" cy="35" r="2.5" fill="#990000"/><circle cx="55" cy="35" r="2.5" fill="#990000"/><path d="M43,32 Q44,28 46,30" fill="#ff6600" opacity="0.7" filter="url(#dglow)"/><path d="M53,32 Q54,28 56,30" fill="#ff6600" opacity="0.7" filter="url(#dglow)"/><ellipse cx="39" cy="23" rx="7" ry="6" fill="#fff"/><ellipse cx="61" cy="23" rx="7" ry="6" fill="#fff"/><ellipse cx="40" cy="23" rx="5" ry="4" fill="#ff6600"/><ellipse cx="62" cy="23" rx="5" ry="4" fill="#ff6600"/><ellipse cx="40" cy="23" rx="2" ry="4" fill="#111"/><ellipse cx="62" cy="23" rx="2" ry="4" fill="#111"/><circle cx="38" cy="21" r="1.2" fill="#fff"/><circle cx="60" cy="21" r="1.2" fill="#fff"/><path d="M33,19 Q39,16 45,19" fill="none" stroke="#cc2200" stroke-width="2" stroke-linecap="round"/><path d="M55,19 Q61,16 67,19" fill="none" stroke="#cc2200" stroke-width="2" stroke-linecap="round"/></svg>"""

    DRAGON_LEGEND = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="dlg" cx="40%" cy="30%" r="70%"><stop offset="0%" stop-color="#ffdd00"/><stop offset="50%" stop-color="#ff4400"/><stop offset="100%" stop-color="#660000"/></radialGradient><radialGradient id="dlfire" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fff" stop-opacity="0.9"/><stop offset="60%" stop-color="#ff9900" stop-opacity="0.6"/><stop offset="100%" stop-color="#ff4400" stop-opacity="0"/></radialGradient><filter id="dlglow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><circle cx="50" cy="60" r="46" fill="none" stroke="#ff6600" stroke-width="1" opacity="0.3" stroke-dasharray="4,3"/><ellipse cx="50" cy="60" rx="40" ry="45" fill="url(#dlfire)" opacity="0.25"/><path d="M15,52 Q-10,20 8,2 Q26,28 28,55" fill="#cc3300"/><path d="M18,52 Q0,22 12,6 Q28,30 30,54" fill="#ff6600" opacity="0.55"/><path d="M85,52 Q110,20 92,2 Q74,28 72,55" fill="#cc3300"/><path d="M82,52 Q100,22 88,6 Q72,30 70,54" fill="#ff6600" opacity="0.55"/><path d="M66,94 Q90,110 88,120 Q78,112 72,102" fill="#880000"/><polygon points="88,120 84,114 92,113 91,121" fill="#ffdd00"/><ellipse cx="50" cy="74" rx="30" ry="27" fill="url(#dlg)"/><path d="M34,64 Q37,60 40,64" fill="none" stroke="#ffdd00" stroke-width="1.5" opacity="0.7"/><path d="M44,60 Q47,56 50,60" fill="none" stroke="#ffdd00" stroke-width="1.5" opacity="0.7"/><path d="M54,60 Q57,56 60,60" fill="none" stroke="#ffdd00" stroke-width="1.5" opacity="0.7"/><polygon points="50,72 46,78 50,84 54,78" fill="#ff2200" filter="url(#dlglow)"/><path d="M22,70 Q8,78 10,92 Q18,86 24,78" fill="#cc2200"/><path d="M78,70 Q92,78 90,92 Q82,86 76,78" fill="#cc2200"/><path d="M10,92 L6,99 M10,92 L10,100 M10,92 L14,98" stroke="#ffdd00" stroke-width="2" stroke-linecap="round" filter="url(#dlglow)"/><path d="M90,92 L94,99 M90,92 L90,100 M90,92 L86,98" stroke="#ffdd00" stroke-width="2" stroke-linecap="round" filter="url(#dlglow)"/><path d="M34,96 Q28,108 32,118 Q38,110 40,100" fill="#aa1100"/><path d="M66,96 Q72,108 68,118 Q62,110 60,100" fill="#aa1100"/><path d="M32,118 L27,122 M32,118 L33,123 M32,118 L37,121" stroke="#ffdd00" stroke-width="1.5" stroke-linecap="round" filter="url(#dlglow)"/><path d="M68,118 L73,122 M68,118 L67,123 M68,118 L63,121" stroke="#ffdd00" stroke-width="1.5" stroke-linecap="round" filter="url(#dlglow)"/><ellipse cx="50" cy="50" rx="17" ry="14" fill="url(#dlg)"/><path d="M41,42 L36,28 L45,41" fill="#ffdd00" filter="url(#dlglow)"/><path d="M50,38 L50,24 L54,38" fill="#ffdd00" filter="url(#dlglow)"/><path d="M59,42 L64,28 L55,41" fill="#ffdd00" filter="url(#dlglow)"/><ellipse cx="50" cy="28" rx="27" ry="25" fill="url(#dlg)"/><path d="M34,12 L24,-6 L38,10" fill="#ffdd00" filter="url(#dlglow)"/><path d="M66,12 L76,-6 L62,10" fill="#ffdd00" filter="url(#dlglow)"/><path d="M50,8 L50,-4 L54,8" fill="#ff8800" filter="url(#dlglow)"/><circle cx="24" cy="-4" r="3" fill="#ff2200" filter="url(#dlglow)"/><circle cx="76" cy="-4" r="3" fill="#ff2200" filter="url(#dlglow)"/><path d="M37,33 Q50,48 63,33 Q63,26 50,24 Q37,26 37,33" fill="#ff8844"/><circle cx="44" cy="34" r="3" fill="#880000"/><circle cx="56" cy="34" r="3" fill="#880000"/><ellipse cx="44" cy="30" rx="2" ry="4" fill="#ff6600" opacity="0.9" filter="url(#dlglow)"/><ellipse cx="56" cy="30" rx="2" ry="4" fill="#ff6600" opacity="0.9" filter="url(#dlglow)"/><ellipse cx="38" cy="21" rx="8" ry="7" fill="#ffdd00" filter="url(#dlglow)"/><ellipse cx="62" cy="21" rx="8" ry="7" fill="#ffdd00" filter="url(#dlglow)"/><ellipse cx="38" cy="21" rx="6" ry="5" fill="#ff6600"/><ellipse cx="62" cy="21" rx="6" ry="5" fill="#ff6600"/><ellipse cx="38" cy="21" rx="2" ry="5" fill="#111"/><ellipse cx="62" cy="21" rx="2" ry="5" fill="#111"/><circle cx="36" cy="19" r="1.5" fill="#fff"/><circle cx="60" cy="19" r="1.5" fill="#fff"/><path d="M30,10 L34,4 L38,10 L42,2 L46,10 L50,4 L54,10 L58,2 L62,10 L66,4 L70,10" fill="none" stroke="#ffdd00" stroke-width="2" stroke-linejoin="round" filter="url(#dlglow)"/></svg>"""

    PHOENIX_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="pbg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffcc44"/><stop offset="100%" stop-color="#cc3300"/></radialGradient></defs><path d="M50,90 Q38,105 32,108" stroke="#ff6600" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M50,90 Q50,108 46,112" stroke="#ff8800" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M50,90 Q62,105 68,108" stroke="#ff4400" stroke-width="4" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="74" rx="24" ry="22" fill="url(#pbg)"/><path d="M28,66 Q16,58 18,46 Q24,54 30,62" fill="#cc3300"/><path d="M28,66 Q20,56 22,48 Q26,56 30,63" fill="#ff8800" opacity="0.7"/><path d="M72,66 Q84,58 82,46 Q76,54 70,62" fill="#cc3300"/><path d="M72,66 Q80,56 78,48 Q74,56 70,63" fill="#ff8800" opacity="0.7"/><ellipse cx="50" cy="78" rx="13" ry="11" fill="#ffeeaa" opacity="0.8"/><rect x="40" y="93" width="8" height="10" rx="3" fill="#cc4400"/><rect x="52" y="93" width="8" height="10" rx="3" fill="#cc4400"/><path d="M40,103 L36,108 M40,103 L40,109 M40,103 L44,108" stroke="#ff6600" stroke-width="2" stroke-linecap="round"/><path d="M60,103 L56,108 M60,103 L60,109 M60,103 L64,108" stroke="#ff6600" stroke-width="2" stroke-linecap="round"/><ellipse cx="50" cy="54" rx="13" ry="11" fill="url(#pbg)"/><circle cx="50" cy="36" r="22" fill="url(#pbg)"/><path d="M44,16 Q46,8 50,12 Q52,6 54,12 Q58,8 58,16" fill="#ff4400"/><path d="M44,40 L50,46 L56,40" fill="#ffcc00"/><circle cx="40" cy="32" r="7" fill="#fff"/><circle cx="60" cy="32" r="7" fill="#fff"/><circle cx="41" cy="32" r="5" fill="#ff6600"/><circle cx="61" cy="32" r="5" fill="#ff6600"/><circle cx="42" cy="31" r="2.5" fill="#111"/><circle cx="62" cy="31" r="2.5" fill="#111"/><circle cx="43" cy="30" r="1.2" fill="#fff"/><circle cx="63" cy="30" r="1.2" fill="#fff"/><ellipse cx="33" cy="38" rx="5" ry="3" fill="#ff8844" opacity="0.5"/><ellipse cx="67" cy="38" rx="5" ry="3" fill="#ff8844" opacity="0.5"/></svg>"""

    PHOENIX_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="pag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffcc22"/><stop offset="60%" stop-color="#ff4400"/><stop offset="100%" stop-color="#880000"/></radialGradient><filter id="pglow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M50,92 Q30,112 24,122" stroke="#ff4400" stroke-width="5" fill="none" stroke-linecap="round" filter="url(#pglow)"/><path d="M50,92 Q44,116 40,122" stroke="#ff8800" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M50,92 Q50,116 50,122" stroke="#ffcc00" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M50,92 Q56,116 60,122" stroke="#ff8800" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M50,92 Q70,112 76,122" stroke="#ff4400" stroke-width="5" fill="none" stroke-linecap="round" filter="url(#pglow)"/><ellipse cx="50" cy="72" rx="26" ry="24" fill="url(#pag)"/><path d="M24,62 Q0,40 6,18 Q18,40 28,60" fill="#cc3300"/><path d="M24,62 Q4,42 8,22 Q18,42 26,60" fill="#ff6600" opacity="0.6"/><path d="M24,62 Q8,44 12,26 Q20,44 26,60" fill="#ffcc00" opacity="0.3"/><path d="M76,62 Q100,40 94,18 Q82,40 72,60" fill="#cc3300"/><path d="M76,62 Q96,42 92,22 Q82,42 74,60" fill="#ff6600" opacity="0.6"/><path d="M76,62 Q92,44 88,26 Q80,44 74,60" fill="#ffcc00" opacity="0.3"/><path d="M38,70 Q42,64 46,70 Q42,68 38,70" fill="#ffcc66" opacity="0.7"/><path d="M46,68 Q50,62 54,68 Q50,66 46,68" fill="#ffcc66" opacity="0.7"/><path d="M54,70 Q58,64 62,70 Q58,68 54,70" fill="#ffcc66" opacity="0.7"/><path d="M40,92 L36,108 Q40,112 42,108 L42,94" fill="#cc4400"/><path d="M60,92 L64,108 Q60,112 58,108 L58,94" fill="#cc4400"/><path d="M36,108 L32,114 M36,108 L37,115 M36,108 L40,113" stroke="#ffcc00" stroke-width="1.5" stroke-linecap="round"/><path d="M64,108 L68,114 M64,108 L63,115 M64,108 L60,113" stroke="#ffcc00" stroke-width="1.5" stroke-linecap="round"/><ellipse cx="50" cy="50" rx="14" ry="13" fill="url(#pag)"/><ellipse cx="50" cy="30" rx="22" ry="20" fill="url(#pag)"/><path d="M40,14 L36,2 L44,12" fill="#ff4400" filter="url(#pglow)"/><path d="M50,10 L50,-2 L54,10" fill="#ffcc00" filter="url(#pglow)"/><path d="M60,14 L64,2 L56,12" fill="#ff4400" filter="url(#pglow)"/><path d="M42,34 Q50,42 58,34 Q56,28 50,26 Q44,28 42,34" fill="#ffcc00"/><path d="M46,38 Q50,44 54,38" fill="#cc8800"/><ellipse cx="39" cy="25" rx="7" ry="6" fill="#ffdd00" filter="url(#pglow)"/><ellipse cx="61" cy="25" rx="7" ry="6" fill="#ffdd00" filter="url(#pglow)"/><ellipse cx="39" cy="25" rx="5" ry="4" fill="#ff6600"/><ellipse cx="61" cy="25" rx="5" ry="4" fill="#ff6600"/><circle cx="39" cy="25" r="2" fill="#111"/><circle cx="61" cy="25" r="2" fill="#111"/><circle cx="38" cy="23" r="1" fill="#fff"/><circle cx="60" cy="23" r="1" fill="#fff"/></svg>"""

    UNICORN_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="ubg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#ddaaff"/></radialGradient><linearGradient id="umane" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff88dd"/><stop offset="50%" stop-color="#aa44ff"/><stop offset="100%" stop-color="#44aaff"/></linearGradient></defs><ellipse cx="50" cy="76" rx="26" ry="22" fill="url(#ubg)"/><rect x="34" y="92" width="9" height="14" rx="4" fill="#eeddff"/><rect x="57" y="92" width="9" height="14" rx="4" fill="#eeddff"/><rect x="34" y="102" width="9" height="5" rx="2" fill="#cc88ff"/><rect x="57" y="102" width="9" height="5" rx="2" fill="#cc88ff"/><path d="M74,82 Q88,82 88,92 Q80,88 76,84" fill="none" stroke="#ff88dd" stroke-width="4" stroke-linecap="round"/><path d="M74,84 Q90,86 88,96" stroke="#aa44ff" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M74,86 Q86,92 82,100" stroke="#44aaff" stroke-width="2" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="56" rx="14" ry="12" fill="url(#ubg)"/><circle cx="50" cy="36" r="22" fill="url(#ubg)"/><path d="M36,26 Q28,32 30,44 Q34,36 36,30" fill="url(#umane)" opacity="0.9"/><path d="M36,24 Q26,28 28,38 Q32,32 34,26" fill="url(#umane)" opacity="0.7"/><path d="M50,16 L46,2 L52,14" fill="url(#umane)"/><path d="M50,16 L54,2 L48,14" fill="#ffddff" opacity="0.6"/><path d="M34,20 L30,10 L40,18" fill="#eeddff"/><path d="M35,20 L32,12 L39,18" fill="url(#umane)" opacity="0.6"/><path d="M66,20 L70,10 L60,18" fill="#eeddff"/><path d="M65,20 L68,12 L61,18" fill="url(#umane)" opacity="0.6"/><circle cx="39" cy="36" r="7.5" fill="#fff"/><circle cx="61" cy="36" r="7.5" fill="#fff"/><circle cx="40" cy="36" r="5.5" fill="#aa44ff"/><circle cx="62" cy="36" r="5.5" fill="#aa44ff"/><circle cx="41" cy="35" r="2.8" fill="#111"/><circle cx="63" cy="35" r="2.8" fill="#111"/><circle cx="43" cy="33" r="1.5" fill="#fff"/><circle cx="65" cy="33" r="1.5" fill="#fff"/><ellipse cx="32" cy="41" rx="5" ry="3" fill="#ff88dd" opacity="0.5"/><ellipse cx="68" cy="41" rx="5" ry="3" fill="#ff88dd" opacity="0.5"/><ellipse cx="50" cy="44" rx="8" ry="5" fill="#ffddff" opacity="0.8"/></svg>"""

    UNICORN_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="uag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffffff"/><stop offset="80%" stop-color="#ccaaff"/><stop offset="100%" stop-color="#9944dd"/></radialGradient><linearGradient id="umane2" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#ff44cc"/><stop offset="33%" stop-color="#aa00ff"/><stop offset="66%" stop-color="#4488ff"/><stop offset="100%" stop-color="#00ffdd"/></linearGradient><filter id="uglow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M74,84 Q92,80 94,96 Q84,90 78,86" fill="none" stroke="#ff44cc" stroke-width="5" stroke-linecap="round"/><path d="M74,86 Q94,84 94,100" stroke="#aa00ff" stroke-width="3.5" fill="none" stroke-linecap="round"/><path d="M74,88 Q92,88 90,104" stroke="#4488ff" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M74,90 Q88,94 84,108" stroke="#00ffdd" stroke-width="2" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="76" rx="27" ry="23" fill="url(#uag)"/><ellipse cx="44" cy="68" rx="8" ry="5" fill="#fff" opacity="0.3" transform="rotate(-20,44,68)"/><path d="M36,94 L32,116 Q38,118 40,116 L40,96" fill="#ddaaff"/><path d="M60,94 L64,116 Q58,118 56,116 L56,96" fill="#ddaaff"/><ellipse cx="36" cy="116" rx="6" ry="3" fill="#aa44ff"/><ellipse cx="62" cy="116" rx="6" ry="3" fill="#aa44ff"/><path d="M38,54 Q24,60 26,76 Q32,66 38,58" fill="url(#umane2)" opacity="0.9"/><path d="M36,52 Q20,58 22,74 Q28,64 36,56" fill="url(#umane2)" opacity="0.7"/><path d="M34,50 Q18,56 20,72 Q26,62 34,54" fill="url(#umane2)" opacity="0.5"/><ellipse cx="50" cy="54" rx="15" ry="14" fill="url(#uag)"/><ellipse cx="50" cy="30" rx="24" ry="22" fill="url(#uag)"/><path d="M34,22 Q20,26 22,40 Q28,32 34,26" fill="url(#umane2)" opacity="0.85"/><path d="M32,20 Q16,24 18,36 Q24,28 32,22" fill="url(#umane2)" opacity="0.65"/><path d="M50,10 L44,-8 L54,8" fill="url(#umane2)" filter="url(#uglow)"/><path d="M50,10 L56,-8 L46,8" fill="#ffffff" opacity="0.5"/><path d="M32,18 L26,6 L38,16" fill="#eeddff"/><path d="M33,18 L28,8 L38,16" fill="url(#umane2)" opacity="0.6"/><path d="M68,18 L74,6 L62,16" fill="#eeddff"/><path d="M67,18 L72,8 L62,16" fill="url(#umane2)" opacity="0.6"/><ellipse cx="38" cy="28" rx="8" ry="7" fill="#fff" filter="url(#uglow)"/><ellipse cx="62" cy="28" rx="8" ry="7" fill="#fff" filter="url(#uglow)"/><ellipse cx="38" cy="28" rx="6" ry="5" fill="#aa00ff"/><ellipse cx="62" cy="28" rx="6" ry="5" fill="#aa00ff"/><circle cx="38" cy="28" r="2.5" fill="#111"/><circle cx="62" cy="28" r="2.5" fill="#111"/><circle cx="36" cy="26" r="1.5" fill="#fff"/><circle cx="60" cy="26" r="1.5" fill="#fff"/><ellipse cx="50" cy="38" rx="10" ry="6" fill="#fff" opacity="0.8"/></svg>"""

    WOLF_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="wbg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffeebb"/><stop offset="100%" stop-color="#cc8800"/></radialGradient></defs><path d="M68,86 Q84,80 86,90 Q78,90 72,88" fill="#cc8800"/><path d="M70,84 Q88,76 88,86" stroke="#ffdd88" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="74" rx="26" ry="22" fill="url(#wbg)"/><ellipse cx="50" cy="78" rx="14" ry="12" fill="#fff8dd" opacity="0.9"/><ellipse cx="36" cy="92" rx="9" ry="7" fill="#cc8800" transform="rotate(10,36,92)"/><ellipse cx="64" cy="92" rx="9" ry="7" fill="#cc8800" transform="rotate(-10,64,92)"/><ellipse cx="32" cy="98" rx="7" ry="5" fill="#bb7700"/><ellipse cx="68" cy="98" rx="7" ry="5" fill="#bb7700"/><ellipse cx="30" cy="102" rx="5" ry="3" fill="#ffcc66"/><ellipse cx="70" cy="102" rx="5" ry="3" fill="#ffcc66"/><ellipse cx="50" cy="54" rx="15" ry="13" fill="url(#wbg)"/><ellipse cx="50" cy="33" rx="24" ry="22" fill="url(#wbg)"/><path d="M34,18 L28,4 L42,16" fill="#cc8800"/><path d="M35,18 L30,6 L41,16" fill="#ffcc88" opacity="0.6"/><path d="M66,18 L72,4 L58,16" fill="#cc8800"/><path d="M65,18 L70,6 L59,16" fill="#ffcc88" opacity="0.6"/><ellipse cx="50" cy="40" rx="12" ry="9" fill="#ffdd99"/><ellipse cx="50" cy="36" rx="4" ry="3" fill="#222"/><ellipse cx="49" cy="35" rx="1.5" ry="1" fill="#555"/><path d="M44,42 Q50,46 56,42" fill="none" stroke="#cc8800" stroke-width="1.5" stroke-linecap="round"/><path d="M50,42 L50,46" stroke="#cc8800" stroke-width="1.5" stroke-linecap="round"/><circle cx="39" cy="28" r="7" fill="#fff"/><circle cx="61" cy="28" r="7" fill="#fff"/><circle cx="40" cy="28" r="5" fill="#ffaa00"/><circle cx="62" cy="28" r="5" fill="#ffaa00"/><circle cx="41" cy="27" r="2.5" fill="#111"/><circle cx="63" cy="27" r="2.5" fill="#111"/><circle cx="42" cy="26" r="1.2" fill="#fff"/><circle cx="64" cy="26" r="1.2" fill="#fff"/><ellipse cx="32" cy="36" rx="5" ry="3" fill="#ffaa44" opacity="0.4"/><ellipse cx="68" cy="36" rx="5" ry="3" fill="#ffaa44" opacity="0.4"/></svg>"""

    WOLF_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="wag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffeeaa"/><stop offset="60%" stop-color="#cc8800"/><stop offset="100%" stop-color="#774400"/></radialGradient><filter id="wglow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M70,88 Q90,76 92,62 Q82,72 74,82" fill="#cc8800"/><path d="M70,86 Q92,72 94,58" stroke="#ffdd88" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M70,90 Q86,80 86,68" stroke="#fff8cc" stroke-width="2" fill="none" stroke-linecap="round"/><ellipse cx="92" cy="60" rx="8" ry="6" fill="#fff8cc" transform="rotate(-30,92,60)"/><ellipse cx="50" cy="74" rx="28" ry="24" fill="url(#wag)"/><ellipse cx="50" cy="80" rx="15" ry="13" fill="#fff8dd" opacity="0.75"/><path d="M34,92 L28,114 Q34,116 36,114 L38,94" fill="#bb7700"/><path d="M66,92 L72,114 Q66,116 64,114 L62,94" fill="#bb7700"/><ellipse cx="32" cy="114" rx="7" ry="4" fill="#ffcc66"/><ellipse cx="68" cy="114" rx="7" ry="4" fill="#ffcc66"/><path d="M27,114 L25,120 M30,115 L29,121 M33,115 L32,121" stroke="#cc8800" stroke-width="1.2" stroke-linecap="round"/><path d="M65,115 L63,121 M68,115 L67,121 M71,114 L72,120" stroke="#cc8800" stroke-width="1.2" stroke-linecap="round"/><ellipse cx="50" cy="52" rx="18" ry="16" fill="url(#wag)"/><path d="M34,44 Q28,50 30,62 Q34,54 36,46" fill="#ffdd88" opacity="0.8"/><path d="M66,44 Q72,50 70,62 Q66,54 64,46" fill="#ffdd88" opacity="0.8"/><ellipse cx="50" cy="28" rx="25" ry="23" fill="url(#wag)"/><path d="M32,14 L24,-2 L40,12" fill="#bb7700"/><path d="M33,14 L27,0 L40,12" fill="#ffcc88" opacity="0.7"/><path d="M68,14 L76,-2 L60,12" fill="#bb7700"/><path d="M67,14 L73,0 L60,12" fill="#ffcc88" opacity="0.7"/><path d="M38,34 Q50,46 62,34 Q60,26 50,24 Q40,26 38,34" fill="#ffdd99"/><ellipse cx="50" cy="32" rx="5" ry="4" fill="#111"/><ellipse cx="48" cy="31" rx="2" ry="1.2" fill="#444"/><path d="M44,38 Q50,44 56,38" fill="none" stroke="#aa6600" stroke-width="1.5"/><path d="M50,38 L50,44" stroke="#aa6600" stroke-width="1.5"/><ellipse cx="38" cy="24" rx="7.5" ry="6.5" fill="#fff"/><ellipse cx="62" cy="24" rx="7.5" ry="6.5" fill="#fff"/><ellipse cx="38" cy="24" rx="5.5" ry="4.5" fill="#ffaa00" filter="url(#wglow)"/><ellipse cx="62" cy="24" rx="5.5" ry="4.5" fill="#ffaa00" filter="url(#wglow)"/><ellipse cx="38" cy="24" rx="2" ry="4" fill="#111"/><ellipse cx="62" cy="24" rx="2" ry="4" fill="#111"/><circle cx="36" cy="22" r="1.2" fill="#fff"/><circle cx="60" cy="22" r="1.2" fill="#fff"/><path d="M30,20 Q38,17 44,20" fill="none" stroke="#774400" stroke-width="2" stroke-linecap="round"/><path d="M56,20 Q62,17 70,20" fill="none" stroke="#774400" stroke-width="2" stroke-linecap="round"/></svg>"""

    CAT_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cbg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffeecc"/><stop offset="100%" stop-color="#ffaa44"/></radialGradient></defs><path d="M68,86 Q88,82 88,96 Q80,92 74,88" fill="#ff9933"/><path d="M70,84 Q92,78 90,96" stroke="#ffcc88" stroke-width="2" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="74" rx="24" ry="22" fill="url(#cbg)"/><ellipse cx="50" cy="78" rx="12" ry="10" fill="#fff8ee" opacity="0.95"/><ellipse cx="36" cy="93" rx="8" ry="6" fill="#ffaa44" transform="rotate(5,36,93)"/><ellipse cx="64" cy="93" rx="8" ry="6" fill="#ffaa44" transform="rotate(-5,64,93)"/><ellipse cx="34" cy="98" rx="6" ry="4" fill="#ffcc88"/><ellipse cx="66" cy="98" rx="6" ry="4" fill="#ffcc88"/><circle cx="31" cy="100" r="2" fill="#ffaa88"/><circle cx="34" cy="101" r="2" fill="#ffaa88"/><circle cx="37" cy="100" r="2" fill="#ffaa88"/><circle cx="63" cy="100" r="2" fill="#ffaa88"/><circle cx="66" cy="101" r="2" fill="#ffaa88"/><circle cx="69" cy="100" r="2" fill="#ffaa88"/><ellipse cx="50" cy="54" rx="14" ry="12" fill="url(#cbg)"/><circle cx="50" cy="34" r="23" fill="url(#cbg)"/><path d="M32,18 L26,4 L40,16" fill="#ffaa44"/><path d="M33,18 L28,6 L39,16" fill="#ff88aa" opacity="0.7"/><path d="M68,18 L74,4 L60,16" fill="#ffaa44"/><path d="M67,18 L72,6 L61,16" fill="#ff88aa" opacity="0.7"/><ellipse cx="50" cy="42" rx="10" ry="7" fill="#fff0dd"/><path d="M46,39 L50,42 L54,39" fill="#ff88aa"/><path d="M44,44 Q50,48 56,44" fill="none" stroke="#cc6633" stroke-width="1.2"/><path d="M50,44 L50,48" stroke="#cc6633" stroke-width="1.2"/><circle cx="39" cy="30" r="7.5" fill="#fff"/><circle cx="61" cy="30" r="7.5" fill="#fff"/><circle cx="40" cy="30" r="5.5" fill="#44cc44"/><circle cx="62" cy="30" r="5.5" fill="#44cc44"/><circle cx="41" cy="29" r="2.8" fill="#111"/><circle cx="63" cy="29" r="2.8" fill="#111"/><circle cx="42" cy="28" r="1.5" fill="#fff"/><circle cx="64" cy="28" r="1.5" fill="#fff"/><ellipse cx="31" cy="38" rx="5" ry="3" fill="#ff88aa" opacity="0.4"/><ellipse cx="69" cy="38" rx="5" ry="3" fill="#ff88aa" opacity="0.4"/><line x1="24" y1="40" x2="42" y2="43" stroke="#cc8844" stroke-width="0.8" opacity="0.7"/><line x1="24" y1="43" x2="42" y2="44" stroke="#cc8844" stroke-width="0.8" opacity="0.7"/><line x1="76" y1="40" x2="58" y2="43" stroke="#cc8844" stroke-width="0.8" opacity="0.7"/><line x1="76" y1="43" x2="58" y2="44" stroke="#cc8844" stroke-width="0.8" opacity="0.7"/><circle cx="50" cy="62" r="6" fill="#ffdd00" opacity="0.85"/><text x="47" y="66" font-size="7" fill="#cc8800">&#165;</text></svg>"""

    CAT_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="cag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffeebb"/><stop offset="70%" stop-color="#ff9922"/><stop offset="100%" stop-color="#cc5500"/></radialGradient><filter id="cglow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M70,90 Q94,80 96,62 Q86,72 76,84" fill="#ff8822"/><path d="M72,88 Q96,76 96,58" stroke="#ffcc88" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="96" cy="58" rx="8" ry="6" fill="#ffcc88" transform="rotate(-20,96,58)"/><ellipse cx="50" cy="76" rx="26" ry="23" fill="url(#cag)"/><path d="M35,68 Q40,64 45,68" fill="none" stroke="#cc6600" stroke-width="1.5" opacity="0.4"/><path d="M55,68 Q60,64 65,68" fill="none" stroke="#cc6600" stroke-width="1.5" opacity="0.4"/><ellipse cx="50" cy="80" rx="14" ry="12" fill="#fff8ee" opacity="0.8"/><path d="M34,94 L28,116 Q34,118 36,116 L38,96" fill="#ff9922"/><path d="M66,94 L72,116 Q66,118 64,116 L62,96" fill="#ff9922"/><ellipse cx="32" cy="116" rx="8" ry="5" fill="#ffcc88"/><ellipse cx="68" cy="116" rx="8" ry="5" fill="#ffcc88"/><circle cx="28" cy="118" r="2.2" fill="#ffaa88"/><circle cx="32" cy="119" r="2.2" fill="#ffaa88"/><circle cx="36" cy="118" r="2.2" fill="#ffaa88"/><circle cx="64" cy="118" r="2.2" fill="#ffaa88"/><circle cx="68" cy="119" r="2.2" fill="#ffaa88"/><circle cx="72" cy="118" r="2.2" fill="#ffaa88"/><ellipse cx="50" cy="54" rx="16" ry="14" fill="url(#cag)"/><rect x="32" y="62" width="36" height="5" rx="2.5" fill="#ff2244"/><circle cx="50" cy="68" r="5" fill="#ffdd00" filter="url(#cglow)"/><text x="47" y="71" font-size="6" fill="#cc8800">&#9733;</text><ellipse cx="50" cy="30" rx="26" ry="24" fill="url(#cag)"/><path d="M30,16 L22,0 L40,14" fill="#cc5500"/><path d="M31,16 L24,2 L39,14" fill="#ff88aa" opacity="0.7"/><path d="M70,16 L78,0 L60,14" fill="#cc5500"/><path d="M69,16 L76,2 L61,14" fill="#ff88aa" opacity="0.7"/><ellipse cx="50" cy="38" rx="11" ry="8" fill="#fff0dd"/><path d="M46,35 L50,38 L54,35" fill="#ff88aa"/><path d="M44,40 Q50,45 56,40" fill="none" stroke="#cc6633" stroke-width="1.5"/><path d="M50,40 L50,45" stroke="#cc6633" stroke-width="1.5"/><ellipse cx="38" cy="24" rx="8.5" ry="7.5" fill="#fff"/><ellipse cx="62" cy="24" rx="8.5" ry="7.5" fill="#fff"/><ellipse cx="38" cy="24" rx="6.5" ry="5.5" fill="#22cc44" filter="url(#cglow)"/><ellipse cx="62" cy="24" rx="6.5" ry="5.5" fill="#22cc44" filter="url(#cglow)"/><ellipse cx="38" cy="24" rx="3" ry="5" fill="#111"/><ellipse cx="62" cy="24" rx="3" ry="5" fill="#111"/><circle cx="36" cy="22" r="1.5" fill="#fff"/><circle cx="60" cy="22" r="1.5" fill="#fff"/><line x1="20" y1="36" x2="40" y2="38" stroke="#cc8844" stroke-width="1" opacity="0.6"/><line x1="20" y1="39" x2="40" y2="40" stroke="#cc8844" stroke-width="1" opacity="0.6"/><line x1="80" y1="36" x2="60" y2="38" stroke="#cc8844" stroke-width="1" opacity="0.6"/><line x1="80" y1="39" x2="60" y2="40" stroke="#cc8844" stroke-width="1" opacity="0.6"/></svg>"""

    PENGUIN_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="penbg" cx="50%" cy="40%" r="55%"><stop offset="0%" stop-color="#334466"/><stop offset="100%" stop-color="#111133"/></radialGradient></defs><ellipse cx="50" cy="72" rx="26" ry="28" fill="url(#penbg)"/><ellipse cx="50" cy="76" rx="16" ry="20" fill="#eef2ff"/><ellipse cx="26" cy="74" rx="8" ry="14" fill="#223355" transform="rotate(-10,26,74)"/><ellipse cx="74" cy="74" rx="8" ry="14" fill="#223355" transform="rotate(10,74,74)"/><ellipse cx="20" cy="84" rx="5" ry="4" fill="#112244"/><ellipse cx="80" cy="84" rx="5" ry="4" fill="#112244"/><ellipse cx="40" cy="98" rx="10" ry="5" fill="#ff8800"/><ellipse cx="60" cy="98" rx="10" ry="5" fill="#ff8800"/><line x1="34" y1="100" x2="32" y2="105" stroke="#cc6600" stroke-width="1.5"/><line x1="38" y1="101" x2="37" y2="106" stroke="#cc6600" stroke-width="1.5"/><line x1="42" y1="101" x2="42" y2="106" stroke="#cc6600" stroke-width="1.5"/><line x1="46" y1="100" x2="48" y2="105" stroke="#cc6600" stroke-width="1.5"/><line x1="54" y1="100" x2="52" y2="105" stroke="#cc6600" stroke-width="1.5"/><line x1="58" y1="101" x2="58" y2="106" stroke="#cc6600" stroke-width="1.5"/><line x1="62" y1="101" x2="63" y2="106" stroke="#cc6600" stroke-width="1.5"/><line x1="66" y1="100" x2="68" y2="105" stroke="#cc6600" stroke-width="1.5"/><circle cx="50" cy="36" r="24" fill="url(#penbg)"/><ellipse cx="50" cy="40" rx="14" ry="16" fill="#eef2ff"/><path d="M44,44 L50,50 L56,44" fill="#ff9900"/><circle cx="38" cy="30" r="7" fill="#fff"/><circle cx="62" cy="30" r="7" fill="#fff"/><circle cx="39" cy="30" r="5" fill="#111"/><circle cx="63" cy="30" r="5" fill="#111"/><circle cx="40" cy="28" r="2" fill="#fff"/><circle cx="64" cy="28" r="2" fill="#fff"/><ellipse cx="30" cy="38" rx="5" ry="3" fill="#aabbff" opacity="0.4"/><ellipse cx="70" cy="38" rx="5" ry="3" fill="#aabbff" opacity="0.4"/><path d="M42,14 L44,8 L48,13 L50,6 L52,13 L56,8 L58,14" fill="none" stroke="#ffdd00" stroke-width="1.5" stroke-linejoin="round"/></svg>"""

    PENGUIN_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="penag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#334466"/><stop offset="100%" stop-color="#0a0a22"/></radialGradient><filter id="penglow"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><ellipse cx="50" cy="76" rx="28" ry="32" fill="url(#penag)"/><ellipse cx="50" cy="80" rx="18" ry="24" fill="#f0f4ff"/><rect x="46" y="56" width="8" height="16" rx="4" fill="#fff" opacity="0.85"/><path d="M22,62 Q8,72 10,90 Q18,80 24,68" fill="#223355"/><path d="M78,62 Q92,72 90,90 Q82,80 76,68" fill="#223355"/><ellipse cx="38" cy="106" rx="14" ry="7" fill="#ff8800"/><ellipse cx="62" cy="106" rx="14" ry="7" fill="#ff8800"/><path d="M28,104 L24,112 M33,105 L31,112 M38,106 L38,113 M43,105 L46,112" stroke="#cc6600" stroke-width="1.5" stroke-linecap="round"/><path d="M52,106 L49,112 M57,105 L56,112 M62,106 L62,113 M67,105 L70,112" stroke="#cc6600" stroke-width="1.5" stroke-linecap="round"/><ellipse cx="50" cy="48" rx="18" ry="14" fill="url(#penag)"/><ellipse cx="50" cy="26" rx="24" ry="22" fill="url(#penag)"/><ellipse cx="50" cy="32" rx="14" ry="14" fill="#f0f4ff"/><path d="M32,12 L36,4 L42,10 L50,2 L58,10 L64,4 L68,12" fill="#ffdd00" filter="url(#penglow)"/><circle cx="50" cy="2" r="3" fill="#fff" filter="url(#penglow)"/><circle cx="36" cy="4" r="2" fill="#00eeff" filter="url(#penglow)"/><circle cx="64" cy="4" r="2" fill="#00eeff" filter="url(#penglow)"/><path d="M43,34 L50,42 L57,34" fill="#ff8800"/><path d="M43,34 L50,38 L57,34" fill="#ffcc00" opacity="0.5"/><ellipse cx="38" cy="24" rx="7" ry="6.5" fill="#fff"/><ellipse cx="62" cy="24" rx="7" ry="6.5" fill="#fff"/><ellipse cx="38" cy="24" rx="5" ry="4.5" fill="#111"/><ellipse cx="62" cy="24" rx="5" ry="4.5" fill="#111"/><circle cx="36" cy="22" r="2" fill="#fff"/><circle cx="60" cy="22" r="2" fill="#fff"/><path d="M50,56 L48,60 L44,60 L46,63 L44,67 L48,65 L50,68 L52,65 L56,67 L54,63 L56,60 L52,60 Z" fill="#00eeff" opacity="0.8" filter="url(#penglow)"/></svg>"""

    FOX_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="fbg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffcc88"/><stop offset="100%" stop-color="#dd4488"/></radialGradient></defs><path d="M68,84 Q88,78 90,92 Q80,90 74,86" fill="#ee6699"/><path d="M68,82 Q90,74 90,90" stroke="#ffaacc" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="90" cy="90" rx="8" ry="6" fill="#fff8ff" transform="rotate(-20,90,90)"/><ellipse cx="50" cy="74" rx="25" ry="22" fill="url(#fbg)"/><ellipse cx="50" cy="78" rx="13" ry="11" fill="#fff0ee" opacity="0.9"/><ellipse cx="36" cy="92" rx="9" ry="6" fill="#dd4488" transform="rotate(8,36,92)"/><ellipse cx="64" cy="92" rx="9" ry="6" fill="#dd4488" transform="rotate(-8,64,92)"/><ellipse cx="32" cy="97" rx="6" ry="4" fill="#ee7799"/><ellipse cx="68" cy="97" rx="6" ry="4" fill="#ee7799"/><ellipse cx="50" cy="54" rx="14" ry="12" fill="url(#fbg)"/><ellipse cx="50" cy="33" rx="23" ry="21" fill="url(#fbg)"/><path d="M33,17 L26,2 L42,15" fill="#ee5588"/><path d="M34,17 L28,4 L41,15" fill="#ffaacc" opacity="0.7"/><path d="M67,17 L74,2 L58,15" fill="#ee5588"/><path d="M66,17 L72,4 L59,15" fill="#ffaacc" opacity="0.7"/><path d="M38,38 Q50,50 62,38 Q60,30 50,28 Q40,30 38,38" fill="#ffddcc"/><ellipse cx="50" cy="34" rx="3.5" ry="2.5" fill="#222"/><ellipse cx="39" cy="28" rx="7" ry="6" fill="#fff"/><ellipse cx="61" cy="28" rx="7" ry="6" fill="#fff"/><ellipse cx="39" cy="28" rx="5" ry="4" fill="#aa22cc"/><ellipse cx="61" cy="28" rx="5" ry="4" fill="#aa22cc"/><ellipse cx="39" cy="28" rx="2" ry="3.5" fill="#111"/><ellipse cx="61" cy="28" rx="2" ry="3.5" fill="#111"/><circle cx="37" cy="26" r="1.2" fill="#fff"/><circle cx="59" cy="26" r="1.2" fill="#fff"/><ellipse cx="31" cy="36" rx="5" ry="3" fill="#ff88aa" opacity="0.5"/><ellipse cx="69" cy="36" rx="5" ry="3" fill="#ff88aa" opacity="0.5"/></svg>"""

    FOX_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="fag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffbb77"/><stop offset="60%" stop-color="#cc3377"/><stop offset="100%" stop-color="#660033"/></radialGradient><filter id="fglow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><path d="M62,90 Q80,84 84,72 Q76,78 70,86" fill="#cc3377" opacity="0.9"/><path d="M62,90 Q82,80 88,66" stroke="#ff88cc" stroke-width="2.5" fill="none" stroke-linecap="round" opacity="0.8"/><path d="M62,90 Q84,78 86,64" stroke="#ddaaff" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.6"/><path d="M64,88 Q86,82 90,70" stroke="#ff88cc" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.7"/><path d="M64,90 Q82,88 84,80 Q78,84 72,88" fill="#dd5599" opacity="0.7"/><path d="M64,92 Q80,92 80,84" stroke="#ffaacc" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.6"/><path d="M64,94 Q78,96 76,88" stroke="#ddaaff" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.5"/><path d="M63,94 Q76,100 72,94" stroke="#ffbbee" stroke-width="1.5" fill="none" stroke-linecap="round" opacity="0.5"/><path d="M62,92 Q72,100 68,98" stroke="#aa44cc" stroke-width="2" fill="none" stroke-linecap="round" opacity="0.6"/><ellipse cx="85" cy="64" rx="7" ry="5" fill="#fff0ff" transform="rotate(-40,85,64)" opacity="0.9" filter="url(#fglow)"/><ellipse cx="88" cy="70" rx="6" ry="4" fill="#fff0ff" transform="rotate(-30,88,70)" opacity="0.7"/><ellipse cx="48" cy="76" rx="26" ry="24" fill="url(#fag)"/><ellipse cx="48" cy="80" rx="14" ry="16" fill="#fff0ee" opacity="0.8"/><path d="M34,96 L28,116 Q34,118 36,116 L38,98" fill="#cc3377"/><path d="M62,96 L68,116 Q62,118 60,116 L58,98" fill="#cc3377"/><ellipse cx="32" cy="116" rx="8" ry="4" fill="#ee8899"/><ellipse cx="64" cy="116" rx="8" ry="4" fill="#ee8899"/><circle cx="24" cy="108" r="4" fill="#aa22cc" opacity="0.5" filter="url(#fglow)"/><circle cx="72" cy="108" r="4" fill="#aa22cc" opacity="0.5" filter="url(#fglow)"/><ellipse cx="48" cy="54" rx="16" ry="14" fill="url(#fag)"/><path d="M34,48 Q36,40 42,44 Q38,42 34,48" fill="#ffaacc" opacity="0.6"/><path d="M62,48 Q60,40 54,44 Q58,42 62,48" fill="#ffaacc" opacity="0.6"/><ellipse cx="48" cy="28" rx="26" ry="24" fill="url(#fag)"/><path d="M30,14 L22,-4 L40,12" fill="#cc2266"/><path d="M31,14 L24,-2 L40,12" fill="#ffaacc" opacity="0.7"/><path d="M66,14 L74,-4 L60,12" fill="#cc2266"/><path d="M65,14 L72,-2 L60,12" fill="#ffaacc" opacity="0.7"/><circle cx="48" cy="14" r="5" fill="#aa22cc" opacity="0.7" filter="url(#fglow)"/><text x="45" y="17" font-size="5" fill="#fff">&#20061;</text><path d="M36,32 Q48,46 60,32 Q58,24 48,22 Q38,24 36,32" fill="#ffddcc"/><ellipse cx="48" cy="28" rx="4" ry="3" fill="#111"/><ellipse cx="36" cy="22" rx="8" ry="7" fill="#fff"/><ellipse cx="60" cy="22" rx="8" ry="7" fill="#fff"/><ellipse cx="36" cy="22" rx="6" ry="5" fill="#aa00dd" filter="url(#fglow)"/><ellipse cx="60" cy="22" rx="6" ry="5" fill="#aa00dd" filter="url(#fglow)"/><ellipse cx="36" cy="22" rx="2" ry="4.5" fill="#111"/><ellipse cx="60" cy="22" rx="2" ry="4.5" fill="#111"/><circle cx="34" cy="20" r="1.5" fill="#fff"/><circle cx="58" cy="20" r="1.5" fill="#fff"/><circle cx="10" cy="52" r="5" fill="#aa22cc" opacity="0.3" filter="url(#fglow)"/><circle cx="86" cy="44" r="4" fill="#ff66cc" opacity="0.25" filter="url(#fglow)"/></svg>"""

    SLIME_BABY = """<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="slbg" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffee88"/><stop offset="100%" stop-color="#cc8800"/></radialGradient><radialGradient id="slsheen" cx="35%" cy="25%" r="45%"><stop offset="0%" stop-color="#fffacc" stop-opacity="0.9"/><stop offset="100%" stop-color="#ffee88" stop-opacity="0"/></radialGradient></defs><ellipse cx="26" cy="85" rx="5" ry="7" fill="#cc8800" opacity="0.7"/><ellipse cx="74" cy="83" rx="4" ry="6" fill="#cc8800" opacity="0.6"/><ellipse cx="50" cy="90" rx="6" ry="8" fill="#cc8800" opacity="0.8"/><path d="M50,15 Q80,12 90,35 Q96,55 82,72 Q68,88 50,90 Q32,88 18,72 Q4,55 10,35 Q20,12 50,15Z" fill="url(#slbg)"/><ellipse cx="38" cy="35" rx="20" ry="14" fill="url(#slsheen)"/><circle cx="50" cy="55" r="14" fill="#ffcc00" opacity="0.4"/><circle cx="50" cy="55" r="10" fill="#ffdd44" opacity="0.3"/><text x="45" y="59" font-size="10" fill="#cc8800" opacity="0.6">&#165;</text><circle cx="38" cy="44" r="8" fill="#fff"/><circle cx="62" cy="44" r="8" fill="#fff"/><circle cx="39" cy="44" r="5.5" fill="#111"/><circle cx="63" cy="44" r="5.5" fill="#111"/><circle cx="41" cy="42" r="2.5" fill="#fff"/><circle cx="65" cy="42" r="2.5" fill="#fff"/><path d="M40,58 Q50,66 60,58" fill="none" stroke="#aa6600" stroke-width="2" stroke-linecap="round"/><circle cx="22" cy="30" r="6" fill="#ffee88" opacity="0.5"/><circle cx="20" cy="28" r="2" fill="#fff" opacity="0.6"/><text x="72" y="28" font-size="8" fill="#ffcc00" opacity="0.7">&#10022;</text></svg>"""

    SLIME_ADULT = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="slag" cx="38%" cy="28%" r="68%"><stop offset="0%" stop-color="#ffee44"/><stop offset="50%" stop-color="#ddaa00"/><stop offset="100%" stop-color="#886600"/></radialGradient><radialGradient id="slsheen2" cx="32%" cy="22%" r="48%"><stop offset="0%" stop-color="#fffacc" stop-opacity="0.95"/><stop offset="100%" stop-color="#ffee44" stop-opacity="0"/></radialGradient><filter id="slglow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><ellipse cx="20" cy="92" rx="7" ry="10" fill="#aa7700" opacity="0.8"/><ellipse cx="50" cy="98" rx="9" ry="12" fill="#aa7700" opacity="0.9"/><ellipse cx="80" cy="90" rx="6" ry="9" fill="#aa7700" opacity="0.7"/><ellipse cx="34" cy="94" rx="5" ry="7" fill="#cc9900" opacity="0.6"/><ellipse cx="66" cy="96" rx="5" ry="8" fill="#cc9900" opacity="0.7"/><path d="M50,10 Q84,8 95,34 Q100,58 86,78 Q70,96 50,98 Q30,96 14,78 Q0,58 5,34 Q16,8 50,10Z" fill="url(#slag)"/><ellipse cx="36" cy="32" rx="24" ry="16" fill="url(#slsheen2)"/><circle cx="50" cy="56" r="22" fill="#ffcc00" opacity="0.25" filter="url(#slglow)"/><circle cx="40" cy="52" r="8" fill="#ffdd44" opacity="0.4"/><text x="37" y="56" font-size="8" fill="#886600" opacity="0.7">&#165;</text><circle cx="60" cy="58" r="7" fill="#ffdd44" opacity="0.4"/><text x="57" y="62" font-size="8" fill="#886600" opacity="0.7">&#165;</text><ellipse cx="36" cy="40" rx="10" ry="9" fill="#fff"/><ellipse cx="64" cy="40" rx="10" ry="9" fill="#fff"/><ellipse cx="36" cy="40" rx="7" ry="6" fill="#ffcc00" filter="url(#slglow)"/><ellipse cx="64" cy="40" rx="7" ry="6" fill="#ffcc00" filter="url(#slglow)"/><circle cx="36" cy="40" r="3.5" fill="#111"/><circle cx="64" cy="40" r="3.5" fill="#111"/><circle cx="34" cy="37" r="2" fill="#fff"/><circle cx="62" cy="37" r="2" fill="#fff"/><path d="M36,56 Q50,68 64,56" fill="none" stroke="#886600" stroke-width="2.5" stroke-linecap="round"/><circle cx="50" cy="16" r="10" fill="#ffdd00" opacity="0.7" filter="url(#slglow)"/><text x="46" y="20" font-size="9" fill="#886600">$</text><circle cx="12" cy="42" r="5" fill="#ffcc00" opacity="0.4" filter="url(#slglow)"/><circle cx="88" cy="38" r="4" fill="#ffcc00" opacity="0.35" filter="url(#slglow)"/></svg>"""

    GENERIC_EGG = """<svg viewBox="0 0 80 100" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="egg_g" cx="38%" cy="30%" r="68%"><stop offset="0%" stop-color="#fffbf0"/><stop offset="65%" stop-color="#f0d888"/><stop offset="100%" stop-color="#d4a840"/></radialGradient></defs><ellipse cx="40" cy="58" rx="34" ry="48" fill="url(#egg_g)"/><ellipse cx="26" cy="32" rx="10" ry="14" fill="white" opacity="0.35" transform="rotate(-22,26,32)"/></svg>"""

    RABBIT_BABY = """<svg viewBox="0 0 100 115" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="rbbg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#a8edea"/></radialGradient></defs><rect x="33" y="0" width="9" height="26" rx="5" fill="#a8edea"/><rect x="58" y="0" width="9" height="26" rx="5" fill="#a8edea"/><rect x="34" y="1" width="7" height="22" rx="3.5" fill="#ffb3d1" opacity="0.8"/><rect x="59" y="1" width="7" height="22" rx="3.5" fill="#ffb3d1" opacity="0.8"/><ellipse cx="50" cy="72" rx="26" ry="22" fill="url(#rbbg)"/><ellipse cx="50" cy="76" rx="14" ry="12" fill="#e0faf8" opacity="0.9"/><ellipse cx="36" cy="90" rx="9" ry="6" fill="#a8edea" transform="rotate(8,36,90)"/><ellipse cx="64" cy="90" rx="9" ry="6" fill="#a8edea" transform="rotate(-8,64,90)"/><ellipse cx="32" cy="96" rx="7" ry="4" fill="#7ed8d4"/><ellipse cx="68" cy="96" rx="7" ry="4" fill="#7ed8d4"/><ellipse cx="50" cy="44" rx="14" ry="12" fill="url(#rbbg)"/><ellipse cx="50" cy="28" rx="22" ry="20" fill="url(#rbbg)"/><ellipse cx="38" cy="28" rx="7" ry="6" fill="#fff"/><ellipse cx="62" cy="28" rx="7" ry="6" fill="#fff"/><ellipse cx="38" cy="28" rx="5" ry="4" fill="#a8edea"/><ellipse cx="62" cy="28" rx="5" ry="4" fill="#a8edea"/><ellipse cx="38" cy="28" rx="2" ry="3.5" fill="#111"/><ellipse cx="62" cy="28" rx="2" ry="3.5" fill="#111"/><circle cx="36" cy="26" r="1.5" fill="#fff"/><circle cx="60" cy="26" r="1.5" fill="#fff"/><ellipse cx="50" cy="37" rx="5" ry="3" fill="#ffb3d1"/><circle cx="50" cy="93" r="6" fill="#fff" opacity="0.95"/><ellipse cx="30" cy="36" rx="5" ry="3" fill="#ffb3d1" opacity="0.5"/><ellipse cx="70" cy="36" rx="5" ry="3" fill="#ffb3d1" opacity="0.5"/></svg>"""

    RABBIT_ADULT = """<svg viewBox="0 0 100 125" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="rbag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffffff"/><stop offset="60%" stop-color="#a8edea"/><stop offset="100%" stop-color="#48c9c0"/></radialGradient><filter id="rbglow"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><rect x="30" y="0" width="11" height="30" rx="6" fill="#a8edea" filter="url(#rbglow)"/><rect x="59" y="0" width="11" height="30" rx="6" fill="#a8edea" filter="url(#rbglow)"/><rect x="31" y="1" width="9" height="26" rx="4.5" fill="#ffb3d1" opacity="0.85"/><rect x="60" y="1" width="9" height="26" rx="4.5" fill="#ffb3d1" opacity="0.85"/><path d="M76,60 Q96,52 94,68 Q86,66 80,62" fill="#7ed8d4"/><path d="M78,58 Q98,48 96,66" stroke="#a8edea" stroke-width="2.5" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="74" rx="28" ry="24" fill="url(#rbag)"/><ellipse cx="50" cy="78" rx="16" ry="14" fill="#e0faf8" opacity="0.8"/><path d="M34,95 Q26,115 30,122 Q38,114 40,100" fill="#7ed8d4"/><path d="M66,95 Q74,115 70,122 Q62,114 60,100" fill="#7ed8d4"/><ellipse cx="32" cy="122" rx="8" ry="4" fill="#a8edea"/><ellipse cx="68" cy="122" rx="8" ry="4" fill="#a8edea"/><ellipse cx="50" cy="32" rx="26" ry="24" fill="url(#rbag)"/><ellipse cx="38" cy="24" rx="8" ry="7" fill="#fff"/><ellipse cx="62" cy="24" rx="8" ry="7" fill="#fff"/><ellipse cx="38" cy="24" rx="6" ry="5" fill="#a8edea" filter="url(#rbglow)"/><ellipse cx="62" cy="24" rx="6" ry="5" fill="#a8edea" filter="url(#rbglow)"/><ellipse cx="38" cy="24" rx="2" ry="4" fill="#111"/><ellipse cx="62" cy="24" rx="2" ry="4" fill="#111"/><circle cx="36" cy="22" r="1.8" fill="#fff"/><circle cx="60" cy="22" r="1.8" fill="#fff"/><ellipse cx="50" cy="37" rx="6" ry="4" fill="#ffb3d1"/><circle cx="50" cy="97" r="8" fill="#fff" opacity="0.92"/><text x="46" y="8" font-size="8" fill="#48c9c0" filter="url(#rbglow)">🌕</text></svg>"""

    SEAHORSE_BABY = """<svg viewBox="0 0 80 115" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="shbg" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#a78bfa"/><stop offset="50%" stop-color="#7b61ff"/><stop offset="100%" stop-color="#4c1d95"/></linearGradient><radialGradient id="shbelly" cx="40%" cy="40%" r="60%"><stop offset="0%" stop-color="#c4b5fd" stop-opacity="0.7"/><stop offset="100%" stop-color="#7b61ff" stop-opacity="0"/></radialGradient></defs><!-- crown --><path d="M36,6 L32,0 L36,5 L40,1 L44,5 L48,0 L44,6" fill="#e879f9" stroke="#c026d3" stroke-width="0.5"/><path d="M34,18 Q28,20 26,30 Q28,26 30,22 Q32,28 34,24" fill="#a78bfa" opacity="0.7"/><path d="M46,18 Q52,20 54,30 Q52,26 50,22 Q48,28 46,24" fill="#a78bfa" opacity="0.5"/><!-- body curve --><path d="M40,22 Q60,22 62,42 Q62,62 48,78 Q40,88 36,100 Q34,108 40,112" fill="none" stroke="url(#shbg)" stroke-width="16" stroke-linecap="round"/><path d="M40,22 Q60,22 62,42 Q62,62 48,78 Q40,88 36,100 Q34,108 40,112" fill="none" stroke="url(#shbelly)" stroke-width="8" stroke-linecap="round"/><!-- head --><ellipse cx="40" cy="18" rx="15" ry="13" fill="url(#shbg)"/><!-- eyes --><circle cx="34" cy="14" r="5" fill="#fff"/><circle cx="46" cy="14" r="5" fill="#fff"/><circle cx="34" cy="14" r="3" fill="#7b61ff"/><circle cx="46" cy="14" r="3" fill="#7b61ff"/><circle cx="33" cy="13" r="1.5" fill="#fff"/><circle cx="45" cy="13" r="1.5" fill="#fff"/><!-- snout --><path d="M37,22 L40,28 L43,22" fill="none" stroke="#c4b5fd" stroke-width="1.5"/><!-- fins --><path d="M60,36 Q74,32 70,44 Q64,44 62,38" fill="#a78bfa" opacity="0.75"/><path d="M60,56 Q74,52 70,64 Q64,64 62,58" fill="#7b61ff" opacity="0.65"/><!-- shine dots --><circle cx="24" cy="36" r="2" fill="#e879f9" opacity="0.6"/><circle cx="62" cy="76" r="2" fill="#06b6d4" opacity="0.6"/></svg>"""

    SEAHORSE_ADULT = """<svg viewBox="0 0 90 130" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="shag" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#e879f9"/><stop offset="25%" stop-color="#7b61ff"/><stop offset="60%" stop-color="#06b6d4"/><stop offset="100%" stop-color="#10b981"/></linearGradient><radialGradient id="shabelly" cx="38%" cy="38%" r="58%"><stop offset="0%" stop-color="#e0d7ff" stop-opacity="0.6"/><stop offset="100%" stop-color="#7b61ff" stop-opacity="0"/></radialGradient><filter id="shglow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><!-- crown --><path d="M40,8 L34,0 L39,7 L43,2 L47,7 L50,1 L46,8" fill="#e879f9" stroke="#c026d3" stroke-width="0.8" filter="url(#shglow)"/><circle cx="34" cy="0" r="2.5" fill="#f0abfc" filter="url(#shglow)"/><circle cx="50" cy="1" r="2" fill="#67e8f9" filter="url(#shglow)"/><!-- neck fins --><path d="M34,22 Q24,24 22,36 Q26,30 30,26 Q30,34 34,30" fill="#a78bfa" opacity="0.85"/><path d="M50,22 Q60,24 62,36 Q58,30 54,26 Q54,34 50,30" fill="#e879f9" opacity="0.7"/><!-- body curve --><path d="M42,26 Q66,26 68,52 Q68,76 52,96 Q42,108 38,118 Q36,126 44,128" fill="none" stroke="url(#shag)" stroke-width="20" stroke-linecap="round" filter="url(#shglow)"/><path d="M42,26 Q66,26 68,52 Q68,76 52,96 Q42,108 38,118 Q36,126 44,128" fill="none" stroke="url(#shabelly)" stroke-width="10" stroke-linecap="round"/><!-- head --><ellipse cx="42" cy="20" rx="18" ry="16" fill="url(#shag)" filter="url(#shglow)"/><!-- eyes --><circle cx="34" cy="15" r="7" fill="#fff"/><circle cx="50" cy="15" r="7" fill="#fff"/><circle cx="34" cy="15" r="5" fill="#7b61ff" filter="url(#shglow)"/><circle cx="50" cy="15" r="5" fill="#7b61ff" filter="url(#shglow)"/><circle cx="32" cy="13" r="2.5" fill="#fff"/><circle cx="48" cy="13" r="2.5" fill="#fff"/><!-- snout --><path d="M38,26 L42,34 L46,26" fill="none" stroke="#c4b5fd" stroke-width="2"/><!-- big fins --><path d="M64,44 Q82,38 78,54 Q70,54 66,48" fill="#a78bfa" opacity="0.9" filter="url(#shglow)"/><path d="M64,68 Q82,62 78,78 Q70,78 66,72" fill="#06b6d4" opacity="0.85" filter="url(#shglow)"/><!-- sparkle dots --><circle cx="20" cy="50" r="3" fill="#e879f9" opacity="0.5" filter="url(#shglow)"/><circle cx="68" cy="94" r="3" fill="#10b981" opacity="0.55" filter="url(#shglow)"/><text x="26" y="12" font-size="10" fill="#e879f9" filter="url(#shglow)">✦</text></svg>"""

    # v7 신규 종족 SVG
    FIREBIRD_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="fibg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ffaa33"/><stop offset="100%" stop-color="#cc1100"/></radialGradient></defs><ellipse cx="50" cy="72" rx="24" ry="22" fill="url(#fibg)"/><ellipse cx="50" cy="76" rx="12" ry="10" fill="#ffdd88" opacity="0.9"/><path d="M28,66 Q14,56 16,44 Q22,52 28,62" fill="#cc2200"/><path d="M72,66 Q86,56 84,44 Q78,52 72,62" fill="#cc2200"/><ellipse cx="50" cy="52" rx="14" ry="12" fill="url(#fibg)"/><circle cx="50" cy="34" r="22" fill="url(#fibg)"/><path d="M36,16 Q40,4 44,12 Q46,6 50,10 Q54,6 56,12 Q60,4 64,16" fill="#ff4400"/><circle cx="40" cy="30" r="7" fill="#fff"/><circle cx="60" cy="30" r="7" fill="#fff"/><circle cx="41" cy="30" r="5" fill="#ff6600"/><circle cx="61" cy="30" r="5" fill="#ff6600"/><circle cx="42" cy="29" r="2.5" fill="#111"/><circle cx="62" cy="29" r="2.5" fill="#111"/><circle cx="43" cy="28" r="1.2" fill="#fff"/><circle cx="63" cy="28" r="1.2" fill="#fff"/></svg>"""
    FIREBIRD_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="fiag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ffcc22"/><stop offset="50%" stop-color="#ff4400"/><stop offset="100%" stop-color="#880000"/></radialGradient></defs><path d="M22,58 Q4,38 10,16 Q22,38 26,60" fill="#cc3300"/><path d="M78,58 Q96,38 90,16 Q78,38 74,60" fill="#cc3300"/><ellipse cx="50" cy="74" rx="26" ry="23" fill="url(#fiag)"/><path d="M50,92 Q32,114 26,122" stroke="#ff4400" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M50,92 Q68,114 74,122" stroke="#ff4400" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M50,92 Q50,116 50,122" stroke="#ffcc00" stroke-width="3" fill="none" stroke-linecap="round"/><ellipse cx="50" cy="52" rx="16" ry="14" fill="url(#fiag)"/><ellipse cx="50" cy="28" rx="25" ry="23" fill="url(#fiag)"/><path d="M34,14 Q38,2 42,10 Q46,4 50,8 Q54,4 58,10 Q62,2 66,14" fill="#ffdd00"/><ellipse cx="38" cy="23" rx="8" ry="7" fill="#fff"/><ellipse cx="62" cy="23" rx="8" ry="7" fill="#fff"/><ellipse cx="38" cy="23" rx="6" ry="5" fill="#ff6600"/><ellipse cx="62" cy="23" rx="6" ry="5" fill="#ff6600"/><ellipse cx="38" cy="23" rx="2" ry="4" fill="#111"/><ellipse cx="62" cy="23" rx="2" ry="4" fill="#111"/><circle cx="36" cy="21" r="1.5" fill="#fff"/><circle cx="60" cy="21" r="1.5" fill="#fff"/></svg>"""
    WHALE_BABY = """<svg viewBox="0 0 110 90" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="whabg" cx="40%" cy="35%" r="60%"><stop offset="0%" stop-color="#66ddff"/><stop offset="100%" stop-color="#0066cc"/></radialGradient></defs><path d="M85,40 Q100,28 100,40 Q100,52 85,50" fill="#0066cc"/><ellipse cx="50" cy="50" rx="40" ry="30" fill="url(#whabg)"/><ellipse cx="50" cy="54" rx="28" ry="18" fill="#aaeeff" opacity="0.6"/><path d="M30,70 Q22,84 28,80 Q34,84 36,72" fill="#0066cc"/><path d="M50,70 Q50,86 46,82 Q54,86 50,70" fill="#0055bb"/><path d="M70,70 Q78,84 72,80 Q66,84 64,72" fill="#0066cc"/><circle cx="34" cy="36" r="8" fill="#fff"/><circle cx="66" cy="36" r="8" fill="#fff"/><circle cx="35" cy="36" r="5" fill="#0066cc"/><circle cx="67" cy="36" r="5" fill="#0066cc"/><circle cx="36" cy="35" r="2.5" fill="#111"/><circle cx="68" cy="35" r="2.5" fill="#111"/><circle cx="37" cy="33" r="1.2" fill="#fff"/><circle cx="69" cy="33" r="1.2" fill="#fff"/><path d="M44,54 Q50,60 56,54" fill="none" stroke="#0055bb" stroke-width="2" stroke-linecap="round"/><path d="M50,28 Q46,22 50,18 Q54,22 50,28" fill="#0099ff" opacity="0.8"/></svg>"""
    WHALE_ADULT = """<svg viewBox="0 0 120 100" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="whaag" cx="40%" cy="35%" r="65%"><stop offset="0%" stop-color="#00cfff"/><stop offset="50%" stop-color="#0066cc"/><stop offset="100%" stop-color="#003388"/></radialGradient></defs><path d="M96,44 Q115,28 114,46 Q114,62 96,56" fill="#0055bb"/><ellipse cx="54" cy="54" rx="46" ry="34" fill="url(#whaag)"/><ellipse cx="54" cy="58" rx="32" ry="20" fill="#aaeeff" opacity="0.5"/><path d="M54,75 Q18,18 8,72" fill="#0055bb"/><circle cx="36" cy="40" r="10" fill="#fff"/><circle cx="72" cy="40" r="10" fill="#fff"/><circle cx="37" cy="40" r="7" fill="#0066cc"/><circle cx="73" cy="40" r="7" fill="#0066cc"/><circle cx="38" cy="39" r="3" fill="#111"/><circle cx="74" cy="39" r="3" fill="#111"/><circle cx="40" cy="37" r="1.5" fill="#fff"/><circle cx="76" cy="37" r="1.5" fill="#fff"/><path d="M46,58 Q54,66 62,58" fill="none" stroke="#0044aa" stroke-width="2.5" stroke-linecap="round"/></svg>"""
    GOLEM_BABY = """<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="gobg" cx="45%" cy="35%" r="60%"><stop offset="0%" stop-color="#ccddee"/><stop offset="100%" stop-color="#556677"/></radialGradient></defs><ellipse cx="50" cy="74" rx="26" ry="24" fill="url(#gobg)"/><rect x="28" y="88" width="16" height="18" rx="4" fill="#4a5566"/><rect x="56" y="88" width="16" height="18" rx="4" fill="#4a5566"/><rect x="18" y="66" width="12" height="20" rx="4" fill="#4a5566"/><rect x="70" y="66" width="12" height="20" rx="4" fill="#4a5566"/><rect x="28" y="22" width="44" height="38" rx="10" fill="url(#gobg)"/><rect x="34" y="32" width="14" height="10" rx="3" fill="#aabbcc"/><rect x="52" y="32" width="14" height="10" rx="3" fill="#aabbcc"/><rect x="36" y="34" width="10" height="6" rx="2" fill="#2299ff"/><rect x="54" y="34" width="10" height="6" rx="2" fill="#2299ff"/><circle cx="41" cy="37" r="2" fill="#fff" opacity="0.7"/><circle cx="59" cy="37" r="2" fill="#fff" opacity="0.7"/><rect x="38" y="46" width="24" height="6" rx="3" fill="#556677"/><circle cx="50" cy="49" r="2" fill="#2299ff" opacity="0.8"/></svg>"""
    GOLEM_ADULT = """<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg"><defs><radialGradient id="goag" cx="40%" cy="30%" r="65%"><stop offset="0%" stop-color="#ddeeff"/><stop offset="60%" stop-color="#667788"/><stop offset="100%" stop-color="#334455"/></radialGradient></defs><rect x="10" y="58" width="18" height="28" rx="5" fill="#4a5566"/><rect x="72" y="58" width="18" height="28" rx="5" fill="#4a5566"/><rect x="10" y="80" width="18" height="10" rx="3" fill="#2299ff" opacity="0.6"/><rect x="72" y="80" width="18" height="10" rx="3" fill="#2299ff" opacity="0.6"/><rect x="20" y="90" width="20" height="26" rx="5" fill="#4a5566"/><rect x="60" y="90" width="20" height="26" rx="5" fill="#4a5566"/><rect x="22" y="50" width="56" height="48" rx="10" fill="url(#goag)"/><rect x="30" y="60" width="18" height="12" rx="4" fill="#99aacc"/><rect x="52" y="60" width="18" height="12" rx="4" fill="#99aacc"/><rect x="32" y="62" width="14" height="8" rx="3" fill="#2299ff"/><rect x="54" y="62" width="14" height="8" rx="3" fill="#2299ff"/><circle cx="39" cy="66" r="3" fill="#fff" opacity="0.8"/><circle cx="61" cy="66" r="3" fill="#fff" opacity="0.8"/><rect x="34" y="76" width="32" height="8" rx="4" fill="#445566"/><circle cx="50" cy="80" r="3" fill="#00eeff"/><rect x="26" y="16" width="48" height="38" rx="10" fill="url(#goag)"/><circle cx="38" cy="35" r="6" fill="#aabbcc"/><circle cx="62" cy="35" r="6" fill="#aabbcc"/><circle cx="38" cy="35" r="4" fill="#2299ff"/><circle cx="62" cy="35" r="4" fill="#2299ff"/><circle cx="38" cy="35" r="2" fill="#111"/><circle cx="62" cy="35" r="2" fill="#111"/><circle cx="37" cy="33" r="1" fill="#fff"/><circle cx="61" cy="33" r="1" fill="#fff"/></svg>"""

    return {
        'dragon':   {'egg': GENERIC_EGG, 'baby': DRAGON_BABY,    'adult': DRAGON_ADULT,    'legend': DRAGON_LEGEND},
        'phoenix':  {'egg': GENERIC_EGG, 'baby': PHOENIX_BABY,   'adult': PHOENIX_ADULT,   'legend': PHOENIX_ADULT},
        'unicorn':  {'egg': GENERIC_EGG, 'baby': UNICORN_BABY,   'adult': UNICORN_ADULT,   'legend': UNICORN_ADULT},
        'wolf':     {'egg': GENERIC_EGG, 'baby': WOLF_BABY,      'adult': WOLF_ADULT,      'legend': WOLF_ADULT},
        'cat':      {'egg': GENERIC_EGG, 'baby': CAT_BABY,       'adult': CAT_ADULT,       'legend': CAT_ADULT},
        'penguin':  {'egg': GENERIC_EGG, 'baby': PENGUIN_BABY,   'adult': PENGUIN_ADULT,   'legend': PENGUIN_ADULT},
        'fox':      {'egg': GENERIC_EGG, 'baby': FOX_BABY,       'adult': FOX_ADULT,       'legend': FOX_ADULT},
        'slime':    {'egg': GENERIC_EGG, 'baby': SLIME_BABY,     'adult': SLIME_ADULT,     'legend': SLIME_ADULT},
        'rabbit':   {'egg': GENERIC_EGG, 'baby': RABBIT_BABY,    'adult': RABBIT_ADULT,    'legend': RABBIT_ADULT},
        'seahorse': {'egg': GENERIC_EGG, 'baby': SEAHORSE_BABY,  'adult': SEAHORSE_ADULT,  'legend': SEAHORSE_ADULT},
        'firebird': {'egg': GENERIC_EGG, 'baby': FIREBIRD_BABY,  'adult': FIREBIRD_ADULT,  'legend': FIREBIRD_ADULT},
        'whale':    {'egg': GENERIC_EGG, 'baby': WHALE_BABY,     'adult': WHALE_ADULT,     'legend': WHALE_ADULT},
        'golem':    {'egg': GENERIC_EGG, 'baby': GOLEM_BABY,     'adult': GOLEM_ADULT,     'legend': GOLEM_ADULT},
    }

_SVG_SPRITES = None

def get_svg_sprite(species_id, stage):
    """캐시된 SVG 스프라이트 반환"""
    global _SVG_SPRITES
    if _SVG_SPRITES is None:
        _SVG_SPRITES = build_svg_sprites()
    sp = _SVG_SPRITES.get(species_id, _SVG_SPRITES.get('cat', {}))
    return sp.get(stage, sp.get('baby', '🐱'))



BOND_TITLES = ["새내기🌱","친구🤝","단짝💛","절친❤️","운명💎","소울메이트🌌"]

# ══════════════════════════════════════════════════════════════════════════════
# 🔧 CORE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def get_pet_stage(lv):
    # v9: 진화 시스템과 연동 (SVG 스프라이트 stage 키 반환)
    return get_evo(lv)["stage"]

def get_pet_sprite(species_id, lv):
    stage = get_pet_stage(lv)
    return get_svg_sprite(species_id, stage)

def default_pet():
    return {
        "species":None,"name":"","level":0,"exp":0,
        "happiness":100,"hunger":100,"hp":100,
        "accessories":[],"skills":[],"last_fed":0,
        "last_played":0,"last_petted":0,"passive_collected":0,
        "birth_date":"","total_fed":0,
        "bond":0,"expeditions":0,"battles_won":0,
        "battles_total":0,"journal":[],"achievements":[],
        "expedition":None,"personality":"",
        "total_exp_gained":0,"highest_bond":0,
        "recipes_made":0,"pet_count":0,"skill_used":0,
        "skill_cooldown":0,"chat_history":[],
        # v7 신규 필드
        "atk_bonus":0,"def_bonus":0,"hp_bonus":0,"spd_bonus":0,"luck_bonus":0,
        "stat_upgrades":{},"missions_completed":0,
        "daily_actions":{},"weekly_actions":{},
        # v9 신규 필드 (만렙/진화/환생/도감/룬)
        "rebirth":0,"evo_tier":0,"prestige_points":0,
        "collection":[],"runes":{},"rune_shards":0,
        "max_level_reached":0,"evolutions_seen":[],
        "total_rebirths":0,"ascension":0,
    }

def load_pet(uid, users=None):
    if users is None: users = load_db(USERS_FILE, {})
    p = users.get(uid, {}).get('pet', default_pet())
    # migrate old pets
    for k,v in default_pet().items():
        if k not in p: p[k] = v
    # v9: 만렙 초과 유저 자동 보정
    if p.get('level', 0) > MAX_LEVEL:
        p['level'] = MAX_LEVEL
        p['exp'] = 0
    # evo_tier 동기화 (레벨에 맞게 재계산)
    p['evo_tier'] = get_evo_tier(p.get('level', 0))
    # 최고 레벨 기록
    if p.get('level', 0) > p.get('max_level_reached', 0):
        p['max_level_reached'] = p.get('level', 0)
    # 진화 도감 자동 기록
    cur_tier = get_evo_tier(p.get('level', 0))
    seen = p.setdefault('evolutions_seen', [])
    for t in range(cur_tier + 1):
        if t not in seen:
            seen.append(t)
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
    # v8: 배가 고프지 않을 때 시간당 HP 소폭 자동 회복
    if pet.get('hunger',100) >= 30:
        regen = int(hp_ * 3)
        if 'wings' in pet.get('accessories',[]) or pet.get('species') == 'phoenix':
            regen *= 2
        _mhp = 100 + pet.get('hp_bonus',0)
        pet['hp'] = min(_mhp, pet.get('hp',100) + regen)
    return pet

def add_exp(pet, exp_amount):
    acc_bonus = sum(
        PET_ACCESSORIES[a].get('bonus',0)
        for a in pet.get('accessories',[])
        if PET_ACCESSORIES.get(a,{}).get('bonus_type') in ('exp','all')
    )
    # v9: 환생 보너스 EXP (+10%/환생, 최대 +200%)
    rb = pet.get('rebirth', 0)
    rebirth_mult = 1 + min(rb * 0.10, 2.0)
    exp_gained = int(exp_amount * (1 + acc_bonus/100) * rebirth_mult)
    pet['exp'] = pet.get('exp',0) + exp_gained
    pet['total_exp_gained'] = pet.get('total_exp_gained',0) + exp_gained
    leveled_up = False
    evolved = None
    while pet.get('level',0) < MAX_LEVEL and pet['exp'] >= exp_to_next(pet.get('level',0)):
        need = exp_to_next(pet.get('level',0))
        pet['exp'] -= need
        prev_tier = get_evo_tier(pet.get('level',0))
        pet['level'] = pet.get('level',0) + 1
        pet['hp']    = min(100 + pet.get('hp_bonus',0), pet.get('hp',100) + 10)
        leveled_up   = True
        for s in PET_SKILLS:
            if s['level'] == pet['level'] and s['name'] not in pet.get('skills',[]):
                pet.setdefault('skills',[]).append(s['name'])
        new_tier = get_evo_tier(pet['level'])
        if new_tier > prev_tier:
            evo = get_evo(pet['level'])
            evolved = evo
            pet['evo_tier'] = new_tier
            add_journal(pet, f"✨🌟 진화! {evo['title']} ({evo['name']}) 단계 도달! Lv.{pet['level']}")
        else:
            add_journal(pet, f"🎉 레벨업! Lv.{pet['level']} 달성!")
    if pet.get('level',0) >= MAX_LEVEL:
        pet['level'] = MAX_LEVEL
        pet['exp'] = 0
    if evolved is not None:
        pet['_evo_pending'] = {'tier': evolved['tier'], 'name': evolved['name'],
                               'title': evolved['title'], 'aura': evolved['aura'],
                               'level': pet['level']}
    return pet, leveled_up, exp_gained

def get_passive_income(pet):
    lv = pet.get('level',0)
    if lv < 15: return 0          # v8: 20 → 15 완화
    base = lv * 1_500_000         # v8: 100만 → 150만 상향
    # slime bonus
    if pet.get('species') == 'slime':    base = int(base * 1.2)
    if pet.get('species') == 'seahorse': base = int(base * 1.1)
    if pet.get('species') == 'whale':    base = int(base * 1.35)
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
    atk = lv * 5  + pet.get('atk_bonus',0)
    df  = lv * 3  + pet.get('def_bonus',0)
    spd = lv * 2  + pet.get('spd_bonus',0)
    # Species bonus
    sp = pet.get('species','cat')
    if sp == 'dragon':    atk = int(atk * 1.3)
    elif sp == 'wolf':    atk = int(atk * 1.15)
    elif sp == 'penguin': df  = int(df  * 1.2)
    elif sp == 'phoenix': spd = int(spd * 1.2)
    elif sp == 'firebird': atk = int(atk * 1.2)
    elif sp == 'golem':   df  = int(df  * 1.4); atk = int(atk * 0.9)
    elif sp == 'whale':   atk = int(atk * 1.5)
    # Accessory
    for a in pet.get('accessories',[]):
        acc = PET_ACCESSORIES.get(a,{})
        bt = acc.get('bonus_type','')
        if bt in ('battle','all'): atk = int(atk * (1 + acc.get('bonus',0)/100))
        if bt in ('def','all'):    df  = int(df  * (1 + acc.get('bonus',0)/100))
    # v9: 진화 tier 배수 (단계마다 강해짐)
    evo_mult = 1 + get_evo_tier(lv) * 0.25
    atk = int(atk * evo_mult); df = int(df * evo_mult); spd = int(spd * evo_mult)
    # v9: 환생 배수 (+15%/환생)
    rb_mult = 1 + pet.get('rebirth', 0) * 0.15
    atk = int(atk * rb_mult); df = int(df * rb_mult); spd = int(spd * rb_mult)
    # v9: 룬 보너스
    runes = pet.get('runes', {})
    for r_id, r_lv in runes.items():
        rdata = PET_RUNES.get(r_id)
        if not rdata or r_lv <= 0: continue
        val = rdata['per_lv'] * r_lv
        if rdata['stat'] == 'atk': atk += val
        elif rdata['stat'] == 'def': df += val
        elif rdata['stat'] == 'spd': spd += val
        elif rdata['stat'] == 'all': atk += val; df += val; spd += val
    return {"atk":atk,"def":df,"spd":spd}

def check_and_award_achievements(pet):
    earned = []
    lv  = pet.get('level',0)
    tf  = pet.get('total_fed',0)
    h   = pet.get('happiness',100)
    ex  = pet.get('expeditions',0)
    bw  = pet.get('battles_won',0)
    bt  = pet.get('battles_total',0)
    bd  = pet.get('bond',0)
    ac  = len(pet.get('accessories',[]))
    rm  = pet.get('recipes_made',0)
    pc  = pet.get('pet_count',0)
    su  = pet.get('skill_used',0)
    existing = pet.get('achievements',[])
    checks = {
        "first_feed":tf>=1,"well_fed":tf>=50,"feast":tf>=500,
        "lv10":lv>=10,"lv25":lv>=25,"lv50":lv>=50,
        "happy_max":h>=100,"explorer1":ex>=1,"explorer10":ex>=10,
        "battle_win1":bw>=1,"battle_win10":bw>=10,
        "hatched":lv>=5,"bonded":bd>=3,"full_acc":ac>=2,"legend":lv>=40,
        "chef":rm>=1,"battler100":bt>=100,
        "petting30":pc>=30,"skill_use5":su>=5,
        "battle_win50":bw>=50,"lv_100":lv>=100,
        "mission10":pet.get('missions_completed',0)>=10,
        "stat_max":sum(pet.get('stat_upgrades',{}).values())>=10,
        # v9
        "lv_1000":lv>=1000,"lv_3000":lv>=3000,"lv_max":lv>=MAX_LEVEL,
        "evo_t3":get_evo_tier(lv)>=3,
        "rebirth1":pet.get('rebirth',0)>=1,"rebirth5":pet.get('rebirth',0)>=5,
        "rune_master":any(v>=50 for v in pet.get('runes',{}).values()),
    }
    for ach_id, cond in checks.items():
        if cond and ach_id not in existing:
            pet.setdefault('achievements',[]).append(ach_id)
            earned.append(ach_id)
    return earned

def _today_key():
    return datetime.now(KST).strftime("%Y%m%d")

def _week_key():
    d = datetime.now(KST)
    week = d.isocalendar()[1]
    return f"{d.year}W{week}"

def _add_action(pet, action_type, count=1):
    """일일/주간 미션 액션 카운트"""
    today = _today_key(); week = _week_key()
    da = pet.setdefault('daily_actions', {})
    wa = pet.setdefault('weekly_actions', {})
    if da.get('date') != today: da.clear(); da['date'] = today
    if wa.get('week') != week:  wa.clear(); wa['week'] = week
    da[action_type] = da.get(action_type, 0) + count
    wa[action_type] = wa.get(action_type, 0) + count

def get_mission_progress(pet):
    today = _today_key(); week = _week_key()
    da = pet.get('daily_actions', {}); wa = pet.get('weekly_actions', {})
    if da.get('date') != today: da = {'date': today}
    if wa.get('week') != week:  wa = {'week': week}
    daily_todo = []
    for m in DAILY_MISSIONS:
        prog = da.get(m['type'], 0); done = prog >= m['target']
        claimed_key = f"dclaimed_{today}_{m['id']}"
        daily_todo.append((m, prog, done, claimed_key))
    weekly_todo = []
    for m in WEEKLY_MISSIONS:
        prog = wa.get(m['type'], 0); done = prog >= m['target']
        claimed_key = f"wclaimed_{week}_{m['id']}"
        weekly_todo.append((m, prog, done, claimed_key))
    return daily_todo, weekly_todo


def add_journal(pet, entry):
    j = pet.setdefault('journal',[])
    ts = datetime.now(KST).strftime("%m/%d %H:%M")
    j.insert(0, f"[{ts}] {entry}")
    pet['journal'] = j[:50]  # 최근 50개만

def get_bond_title(bond_lv):
    return BOND_TITLES[min(bond_lv, len(BOND_TITLES)-1)]

# v7: 탐험 랜덤 이벤트
EXPEDITION_EVENTS = [
    {"name":"보물 발견!", "icon":"💎","desc":"숨겨진 보물을 발견했다!","cash_mult":2.5,"exp_mult":1.0,"hp_effect":0},
    {"name":"함정 발동!", "icon":"⚠️","desc":"함정에 빠졌다! HP 감소","cash_mult":0.8,"exp_mult":1.0,"hp_effect":-20},
    {"name":"신비한 샘",  "icon":"💧","desc":"신비한 샘에서 회복했다!","cash_mult":1.0,"exp_mult":1.2,"hp_effect":30},
    {"name":"몬스터 습격","icon":"👺","desc":"강한 몬스터가 나타났다!","cash_mult":1.5,"exp_mult":2.0,"hp_effect":-10},
    {"name":"행운의 별",  "icon":"⭐","desc":"행운의 별이 쏟아졌다!","cash_mult":3.0,"exp_mult":1.5,"hp_effect":0},
    {"name":"평화로운 여행","icon":"🌸","desc":"특별한 일 없이 귀환","cash_mult":1.0,"exp_mult":1.0,"hp_effect":5},
]

def get_expedition_reward(zone_id, pet):
    z   = EXPEDITION_ZONES[zone_id]
    lv  = pet.get('level',1)
    mul = max(1.0, min(1 + (lv - z['min_lv']) * 0.05, 3.0))
    event = random.choice(EXPEDITION_EVENTS)
    rare_chance = min(0.15 + lv * 0.003 + pet.get('luck_bonus',0)*0.01, 0.6)
    if pet.get('species') == 'rabbit': rare_chance += 0.08
    got_rare = random.random() < rare_chance
    exp_  = int(z['base_exp']  * mul * random.uniform(0.85, 1.2) * event['exp_mult'])
    cash_ = int(z['base_cash'] * mul * random.uniform(0.85, 1.2) * event['cash_mult'])
    return exp_, cash_, got_rare, z.get('rare_item','✨ 희귀 아이템'), event

def get_available_monsters(lv):
    # 해금된 몹들 중, 현재 레벨에 비해 너무 약한 잡몹은 일부만 노출.
    avail = [m for m in WILD_MONSTERS if m['lv_req'] <= lv]
    if not avail:
        return [WILD_MONSTERS[0]]
    # lv_req 기준 내림차순 정렬 → 강한(=보상 큰) 몹을 위로
    avail = sorted(avail, key=lambda m: m['lv_req'], reverse=True)
    # 상위 12종만 (강한 순)
    return avail[:12]

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 HTML ANIMATION GENERATOR
# ══════════════════════════════════════════════════════════════════════════════

def _evolution_cutscene_html(pet, sp, lv, evo):
    """v9: 진화 풀스크린 연출 — 펫이 빛에 휩싸였다가 새 모습으로 등장."""
    aura = evo.get('aura', '#FFD600')
    title = evo.get('title', '진화!')
    name = evo.get('name', '')
    species = pet.get('species', 'cat')
    # 진화 전/후 스프라이트 (직전 tier vs 현재)
    prev_lv = max(0, lv - 1)
    before_svg = get_pet_sprite(species, prev_lv)
    after_svg  = get_pet_sprite(species, lv)
    pet_name = pet.get('name', '펫')
    return """
    <div id="evo" style="position:relative;height:360px;border-radius:20px;overflow:hidden;
         background:radial-gradient(circle at 50% 50%,#1a1030,#05030a 75%);
         border:2px solid AURA;display:flex;align-items:center;justify-content:center;
         box-shadow:0 0 50px AURA66 inset;font-family:'Pretendard',sans-serif;">
      <div id="rays" style="position:absolute;width:600px;height:600px;
           background:conic-gradient(from 0deg,transparent,AURA44,transparent,AURA44,transparent,AURA44,transparent);
           border-radius:50%;animation:evoRays 4s linear infinite;opacity:0;"></div>
      <div id="ring1" style="position:absolute;width:160px;height:160px;border:2px solid AURA;border-radius:50%;opacity:0;"></div>
      <div id="ring2" style="position:absolute;width:160px;height:160px;border:1px dashed AURA88;border-radius:50%;opacity:0;"></div>
      <div id="sprite" style="width:150px;height:150px;display:flex;align-items:center;justify-content:center;
           filter:drop-shadow(0 0 20px AURA);z-index:3;">BEFORE_SVG</div>
      <div id="flashwhite" style="position:absolute;inset:0;background:#fff;opacity:0;z-index:5;pointer-events:none;"></div>
      <div id="evotext" style="position:absolute;top:24px;left:0;right:0;text-align:center;z-index:6;opacity:0;">
        <div style="font-size:0.9rem;color:#fff;letter-spacing:3px;font-weight:700;">✨ E V O L U T I O N ✨</div>
      </div>
      <div id="evoresult" style="position:absolute;bottom:26px;left:0;right:0;text-align:center;z-index:6;opacity:0;">
        <div style="font-size:1.5rem;font-weight:900;color:AURA;text-shadow:0 0 16px AURA;">TITLE</div>
        <div style="font-size:0.85rem;color:#E2E8F0;margin-top:4px;">PETNAME (이)가 NAME (으)로 진화했다! · Lv.LVNUM</div>
      </div>
      <div id="parts" style="position:absolute;inset:0;pointer-events:none;z-index:4;"></div>
    </div>
    <style>
    @keyframes evoRays{from{transform:rotate(0)}to{transform:rotate(360deg)}}
    @keyframes evoRingExpand{0%{transform:scale(0.4);opacity:0.9}100%{transform:scale(2.6);opacity:0}}
    @keyframes evoShake{0%,100%{transform:translate(0,0)}25%{transform:translate(-6px,3px)}50%{transform:translate(5px,-4px)}75%{transform:translate(-4px,-2px)}}
    @keyframes evoFloat{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-12px) scale(1.05)}}
    .evop{position:absolute;animation:evoPRise ease-out forwards;pointer-events:none;}
    @keyframes evoPRise{0%{opacity:0;transform:translateY(0) scale(0.3)}15%{opacity:1}100%{opacity:0;transform:translateY(-220px) translateX(var(--dx)) scale(1.1)}}
    </style>
    <script>
    (function(){
      var AURA="AURA";
      var rays=document.getElementById('rays'),r1=document.getElementById('ring1'),r2=document.getElementById('ring2'),
          sprite=document.getElementById('sprite'),fw=document.getElementById('flashwhite'),
          et=document.getElementById('evotext'),er=document.getElementById('evoresult'),parts=document.getElementById('parts');
      var AFTER=`AFTER_SVG`;
      // 1) 광선 + 텍스트 등장, 펫 떨림
      setTimeout(function(){rays.style.transition='opacity 0.6s';rays.style.opacity='1';et.style.transition='opacity 0.6s';et.style.opacity='1';sprite.style.animation='evoShake 0.25s infinite';},100);
      // 2) 파티클 분출
      var pi=['✨','⭐','💫','🌟','💥'];
      var spawner=setInterval(function(){var p=document.createElement('div');p.className='evop';p.textContent=pi[Math.floor(Math.random()*pi.length)];p.style.left=(40+Math.random()*20)+'%';p.style.bottom='40%';p.style.color=AURA;p.style.fontSize=(14+Math.random()*14)+'px';p.style.setProperty('--dx',((Math.random()-0.5)*160)+'px');p.style.animationDuration=(1.2+Math.random()*1.2)+'s';parts.appendChild(p);setTimeout(function(){p.remove();},2400);},90);
      // 3) 링 폭발 (1.4초 지점)
      setTimeout(function(){r1.style.animation='evoRingExpand 0.9s ease-out';r2.style.animation='evoRingExpand 1.1s ease-out 0.1s';},1400);
      // 4) 화이트 플래시 + 모습 교체 (2.0초)
      setTimeout(function(){
        fw.style.transition='opacity 0.18s';fw.style.opacity='0.95';
        setTimeout(function(){
          sprite.innerHTML=AFTER;sprite.style.animation='evoFloat 2.5s ease-in-out infinite';
          sprite.style.transform='scale(1.12)';
          fw.style.opacity='0';
        },180);
      },2000);
      // 5) 결과 텍스트 (2.5초)
      setTimeout(function(){er.style.transition='opacity 0.7s';er.style.opacity='1';clearInterval(spawner);},2500);
    })();
    </script>
    """.replace("AURA", aura).replace("BEFORE_SVG", before_svg).replace("AFTER_SVG", after_svg).replace("TITLE", title).replace("PETNAME", pet_name).replace("NAME", name).replace("LVNUM", str(lv))


def generate_pet_animation_html(pet, sp, lv, exp, exp_pct, hunger, happy, hp, feed_anim=False):
    species      = pet.get('species','cat')
    name         = pet.get('name','펫')
    # v9: 진화 tier가 높을수록 오라색을 진화 색으로 (Tier2+부터 진화색 우선)
    _evo = get_evo(lv)
    rarity_color = _evo['aura'] if _evo['tier'] >= 2 else sp.get('rarity_color','#00E5FF')
    rarity       = (_evo['name'] + " · " + sp.get('rarity','일반')) if _evo['tier'] >= 2 else sp.get('rarity','일반')
    stage        = get_pet_stage(lv)

    if stage == 'egg':    sprite = sp.get('egg','🥚')
    elif stage == 'baby': sprite = sp.get('baby','🐱')
    elif stage == 'adult': sprite = sp.get('adult','🐈')
    else:                  sprite = sp.get('legend','⭐')

    has_wings  = stage in ('adult','legend') and species in ('dragon','phoenix')
    wing_emoji = '🔥' if species == 'dragon' else '🌟' if species == 'phoenix' else '💫'

    ptcl_map = {
        'dragon':   ['🔥','⚡','✨','💛','🌋'],
        'phoenix':  ['🔥','✨','🌟','💛','☀️'],
        'unicorn':  ['🌈','✨','💜','💫','🦄'],
        'fox':      ['🌙','✨','🦊','💫','⭐'],
        'wolf':     ['⭐','✨','🌕','💛','❄️'],
        'cat':      ['✨','💫','🌟','🐾','💕'],
        'penguin':  ['❄️','⛄','✨','💎','🌊'],
        'slime':    ['💛','✨','💰','🟡','⭐'],
        'rabbit':   ['🌕','✨','🐰','🌟','💫'],
        'seahorse': ['🌊','✨','🌈','💜','🫧'],
    }
    particles = json.dumps(ptcl_map.get(species, ['✨','💫','⭐']))

    # 계절 파티클
    season_name, season_icon = get_season()
    weather_now = get_weather()
    weather_icon_now = WEATHER_ICONS.get(weather_now, "☀️")
    season_particles = json.dumps(SEASON_BG[season_name]['particles'])

    # 먹이 반응 애니메이션 플래그
    feed_anim_js = "true" if feed_anim else "false"

    mood_name, mood_data = get_mood(pet)
    mood_color = mood_data['color']

    bg_map = {
        'dragon':   ('#200800','#120300'),
        'phoenix':  ('#1f0900','#0f0500'),
        'unicorn':  ('#0c0018','#060010'),
        'fox':      ('#140010','#0a0010'),
        'wolf':     ('#080808','#050510'),
        'cat':      ('#060e08','#030a05'),
        'penguin':  ('#020e1e','#010c18'),
        'slime':    ('#0d0e00','#080900'),
        'rabbit':   ('#071a18','#040f0e'),
        'seahorse': ('#0a0020','#060018'),
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
        # SVG 캐릭터 렌더링
        svg_sprite = get_svg_sprite(species, stage)

        # 날개/이펙트 오버레이 (SVG 위에)
        overlay_html = ""
        if stage == 'legend':
            overlay_html = """
            <div style="position:absolute;width:240px;height:240px;border-radius:50%;border:2px dashed rgba(255,255,255,0.12);pointer-events:none;z-index:1;animation:ringRot 6s linear infinite;"></div>
            <div style="position:absolute;width:180px;height:180px;border-radius:50%;border:1px solid rgba(255,255,255,0.08);pointer-events:none;z-index:1;animation:ringRot 4s linear infinite reverse;"></div>"""

        center_html = f"""
        {overlay_html}
        <div id="pet-area" onclick="onPetClick(event)" onmousemove="onPetHover(event)" onmouseleave="onPetLeave()" style="position:relative;display:flex;align-items:center;justify-content:center;cursor:pointer;user-select:none;padding:10px 30px;z-index:5;">
          <div id="sprite" style="width:140px;height:140px;display:flex;align-items:center;justify-content:center;transition:transform 0.15s;animation:{sprite_anim};">
            {svg_sprite}
          </div>
        </div>"""

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;overflow:hidden;font-family:'Courier New',monospace;}}
#app{{
  width:100%;min-height:380px;height:clamp(360px,50vw,440px);
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
#season-badge{{position:absolute;top:50px;left:50%;transform:translateX(-50%);background:rgba(0,0,0,0.7);border-radius:10px;padding:2px 10px;font-size:10px;color:#94A3B8;white-space:nowrap;z-index:20;}}
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
.dmg-num{{position:absolute;pointer-events:none;font-weight:900;z-index:70;animation:dmgFloat 1.2s ease-out forwards;}}
.eat-anim{{position:absolute;pointer-events:none;font-size:28px;z-index:70;animation:eatBounce 0.9s ease-out forwards;}}
#pet-area.petting #sprite{{
  animation:petHappy 0.25s ease-in-out infinite!important;
  filter:drop-shadow(0 0 35px {rarity_color}) drop-shadow(0 0 18px #ffff0088)!important;
}}
#sprite svg{{width:100%;height:100%;}}
#sprite{{filter:drop-shadow(0 0 10px {rarity_color}44);}}
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
@keyframes dmgFloat{{0%{{opacity:1;transform:translateY(0) scale(1.2);}}40%{{opacity:1;transform:translateY(-40px) scale(1.4);}}100%{{opacity:0;transform:translateY(-90px) scale(0.8);}}}}
@keyframes eatBounce{{0%{{opacity:1;transform:scale(0.5) rotate(-20deg);}}40%{{opacity:1;transform:scale(1.4) rotate(10deg);}}100%{{opacity:0;transform:scale(0.8) translateY(-50px);}}}}
@keyframes screenShake{{0%,100%{{transform:translate(0,0);}}10%{{transform:translate(-8px,-4px);}}20%{{transform:translate(8px,4px);}}30%{{transform:translate(-6px,2px);}}40%{{transform:translate(6px,-2px);}}55%{{transform:translate(-4px,4px);}}65%{{transform:translate(4px,-4px);}}80%{{transform:translate(-2px,2px);}}}}
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
  <div id="season-badge">{season_icon} {season_name} · {weather_icon_now} {weather_now}</div>
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
const SEASON_P={season_particles};
const PET_SPECIES="{species}";
const IS_EGG={"true" if stage=="egg" else "false"};
const IS_LEGEND={"true" if stage=="legend" else "false"};
const PTCL_INTERVAL={ptcl_interval};
const FEED_ANIM={feed_anim_js};
const APP = document.getElementById('app');
const EFX = document.getElementById('efx');

// ── Canvas starfield
const canvas = document.getElementById('bg-canvas');
const ctx    = canvas.getContext('2d');
function resizeCanvas() {{
  canvas.width = APP.clientWidth || window.innerWidth;
  canvas.height = APP.clientHeight || 440;
}}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);
const CW = () => canvas.width;
const CH = () => canvas.height;
const stars = Array.from({{length:90}}, ()=>({{
  x:Math.random()*CW(), y:Math.random()*CH(),
  r:Math.random()*1.6+0.2, op:Math.random(), spd:Math.random()*0.018+0.006, dir:1
}}));
const orbs=[
  {{x:120,y:100,r:80, col:RAR_COLOR,op:0.06}},
  {{x:580,y:330,r:100,col:RAR_COLOR,op:0.05}},
  {{x:350,y:220,r:130,col:'#ffffff', op:0.02}},
];
function drawBg(){{
  ctx.clearRect(0,0,CW(),CH());
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
  // SVG 기반 펫 — HTML 어트리뷰트로 이벤트 처리
}}

let _pettingTmo=null, _lastHeart=0;
window.onPetHover = function(e) {{
  const petArea = document.getElementById('pet-area');
  if(petArea) petArea.classList.add('petting');
  clearTimeout(_pettingTmo);
  _pettingTmo = setTimeout(()=>{{if(petArea)petArea.classList.remove('petting');}}, 380);
  const now=Date.now();
  if(now-_lastHeart>150) {{
    const r=APP.getBoundingClientRect();
    spawnHeart(e.clientX-r.left, e.clientY-r.top-25);
    _lastHeart=now;
  }}
}};
window.onPetLeave = function() {{
  const petArea = document.getElementById('pet-area');
  if(petArea) petArea.classList.remove('petting');
}};
window.onPetClick = function(e) {{
  const r=APP.getBoundingClientRect();
  const x=e.clientX-r.left, y=e.clientY-r.top;
  spawnSparks(x, y, 8);
  for(let i=0;i<10;i++) setTimeout(()=>spawnHeart(x+(Math.random()-0.5)*80, y+(Math.random()-0.5)*45), i*70);
  if(PET_SPECIES==='dragon')  spawnFireBreath(x, y);
  if(PET_SPECIES==='phoenix') for(let i=0;i<8;i++) setTimeout(()=>spawnEmber(), i*80);
  if(PET_SPECIES==='unicorn') for(let i=0;i<10;i++) setTimeout(()=>spawnRainbow(), i*60);
  // SVG 스프라이트 쿵 애니메이션
  const sprite=document.getElementById('sprite');
  if(sprite) {{
    sprite.style.transform='scale(1.18) rotate(-5deg)';
    setTimeout(()=>{{sprite.style.transform='';}}, 200);
  }}
}};

// ── PARTICLE SYSTEM
function spawnPtcl() {{
  const p=document.createElement('div');
  p.className='ptcl';
  // 20% 확률로 계절 파티클
  const pool = Math.random() < 0.2 ? SEASON_P : PARTICLES;
  p.textContent=pool[Math.floor(Math.random()*pool.length)];
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

// ── 먹이 반응 애니메이션 (먹이 버튼 클릭 시 자동 실행)
function triggerFeedAnimation() {{
  const sprite = document.getElementById('sprite');
  if(sprite) {{
    sprite.style.transition = 'transform 0.12s';
    sprite.style.transform  = 'scale(1.35) translateY(-22px) rotate(6deg)';
    setTimeout(()=>{{ sprite.style.transform='scale(1.1) translateY(-10px) rotate(-4deg)'; }},180);
    setTimeout(()=>{{ sprite.style.transform='scale(1.2) translateY(-15px) rotate(3deg)'; }},360);
    setTimeout(()=>{{ sprite.style.transform='scale(1.05) translateY(-5px) rotate(-1deg)'; }},540);
    setTimeout(()=>{{ sprite.style.transform=''; sprite.style.transition=''; }},700);
  }}
  const cx=APP.clientWidth/2, cy=APP.clientHeight/2;
  // 하트 폭발
  for(let i=0;i<16;i++) {{
    setTimeout(()=>spawnHeart(cx+(Math.random()-0.5)*140,cy+(Math.random()-0.5)*100),i*50);
  }}
  // 먹이 이모지 이펙트
  const foodEmojis=['🍖','✨','💕','😋','🌟','💗'];
  foodEmojis.forEach((e,i)=>{{
    setTimeout(()=>{{
      const el=document.createElement('div');
      el.className='eat-anim';
      el.textContent=e;
      el.style.left=(cx+(Math.random()-0.5)*110)+'px';
      el.style.top =(cy+(Math.random()-0.5)*80)+'px';
      EFX.appendChild(el);
      setTimeout(()=>el.remove(),1000);
    }},i*75);
  }});
  // 만족 텍스트 팝업
  setTimeout(()=>{{
    const t=document.createElement('div');
    t.className='dmg-num';
    t.textContent='냠냠~ 😋';
    t.style.cssText='color:#FFD600;font-size:22px;left:50%;top:36%;transform:translateX(-50%);text-shadow:0 0 12px #FFD600;';
    EFX.appendChild(t);
    setTimeout(()=>t.remove(),1500);
  }},300);
}}
if(FEED_ANIM) setTimeout(triggerFeedAnimation, 150);

// ── 배틀 타격 이펙트 (Python에서 st.rerun 후 컴포넌트가 다시 로드될 때 호출)
window.triggerBattleHit = function(damage, isCrit) {{
  // 화면 흔들림
  APP.style.animation = 'screenShake 0.45s ease-out';
  setTimeout(()=>{{ APP.style.animation=''; }}, 500);
  // 피격 플래시
  const flash = document.createElement('div');
  flash.style.cssText = 'position:absolute;inset:0;background:rgba(255,50,50,0.18);z-index:40;pointer-events:none;border-radius:22px;';
  APP.appendChild(flash);
  setTimeout(()=>flash.remove(), 200);
  // 데미지 숫자
  const cx=APP.clientWidth/2, cy=APP.clientHeight*0.40;
  const d=document.createElement('div');
  d.className='dmg-num';
  d.textContent=(isCrit?'💥 CRIT! ':'')+'-'+damage+'HP';
  d.style.cssText='color:'+(isCrit?'#FF3333':'#FF8800')+';font-size:'+(isCrit?28:22)+'px;left:'+(cx+(Math.random()-0.5)*60)+'px;top:'+cy+'px;text-shadow:0 0 14px '+(isCrit?'#FF0000':'#FF8800')+';';
  EFX.appendChild(d);
  setTimeout(()=>d.remove(),1400);
  // 스파크 이펙트
  const hits=['💥','⚡','✨','💫'];
  for(let i=0;i<8;i++) {{
    setTimeout(()=>{{
      const s=document.createElement('div'); s.className='spark';
      s.textContent=hits[Math.floor(Math.random()*hits.length)];
      const a=(i/8)*Math.PI*2; const dist=30+Math.random()*50;
      s.style.setProperty('--sx',Math.cos(a)*dist+'px');
      s.style.setProperty('--sy',Math.sin(a)*dist+'px');
      s.style.left=(cx+(Math.random()-0.5)*70)+'px';
      s.style.top =(cy+(Math.random()-0.5)*50)+'px';
      s.style.fontSize='20px';
      EFX.appendChild(s); setTimeout(()=>s.remove(),850);
    }},i*28);
  }}
}};
window.triggerPetAttack = function(damage) {{
  const cx=APP.clientWidth*0.28, cy=APP.clientHeight*0.42;
  const d=document.createElement('div'); d.className='dmg-num';
  d.textContent='⚔️ -'+damage+'HP';
  d.style.cssText='color:#00FF88;font-size:22px;left:'+cx+'px;top:'+cy+'px;text-shadow:0 0 10px #00FF88;';
  EFX.appendChild(d); setTimeout(()=>d.remove(),1300);
  spawnSparks(cx,cy,6);
}};
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

    st.title("🐾 펫 키우기 v9.0 — MAX EVOLUTION")
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
                baby_svg = get_svg_sprite(sp_id, 'baby')
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;border-color:{sp["rarity_color"]}33;'>
                    <div style='width:90px;height:90px;margin:0 auto 10px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 8px {sp["rarity_color"]}88);'>{baby_svg}</div>
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
    _need = exp_to_next(lv) if lv < MAX_LEVEL else 1
    exp_pct = int(exp / _need * 100) if lv < MAX_LEVEL else 100
    stage   = get_pet_stage(lv)
    evo_cur = get_evo(lv)
    mood_name, mood_data = get_mood(pet)
    bond_lv = min(pet.get('bond',0)//20, 5)

    # Awards achievements + cash rewards
    new_ach = check_and_award_achievements(pet)
    if new_ach:
        save_pet(uid, pet)
        for ach_id in new_ach:
            ach_data = next((a for a in PET_ACHIEVEMENTS if a['id']==ach_id), None)
            if ach_data:
                reward = ach_data.get('reward', 0)
                if reward > 0:
                    atomic_add_cash(uid, reward)
                    st.session_state.global_cash += reward
                    st.toast(f"🏆 업적: {ach_data['icon']} {ach_data['name']} +{format_korean_money(reward)}!", icon="🎉")
                else:
                    st.toast(f"🏆 업적 달성: {ach_data['icon']} {ach_data['name']}!", icon="🎉")

    # ── 쓰다듬기 버튼 (독립 쿨타임 5분)
    last_petted  = pet.get('last_petted', 0)
    pet_cooldown = max(0, 300 - (time.time() - last_petted))
    pc1, pc2, pc3 = st.columns([1,2,1])
    with pc2:
        if pet_cooldown > 0:
            m, s = int(pet_cooldown//60), int(pet_cooldown%60)
            st.markdown(f"<div style='text-align:center;color:#64748B;font-size:0.82rem;padding:6px;'>🤗 쓰다듬기 쿨타임: {m}분 {s}초</div>", unsafe_allow_html=True)
        else:
            if st.button("🤗 쓰다듬기! (유대감↑ 행복↑)", use_container_width=True, key="pet_btn"):
                pet['happiness']   = min(100, pet.get('happiness',100) + 15)
                pet['bond']        = pet.get('bond',0) + 3
                pet['last_petted'] = time.time()
                pet['pet_count']   = pet.get('pet_count',0) + 1
                ge_p = random.randint(2,8)
                pet, lvup_p, ge_p = add_exp(pet, ge_p)
                add_journal(pet, f"🤗 쓰다듬어줬다! 행복+15 유대감+3")
                _add_action(pet,'petting')
                save_pet(uid, pet)
                st.session_state['feed_animation'] = True
                st.toast(f"🤗 {pet['name']}이(가) 좋아해요! 행복 +15", icon="💕")
                if lvup_p: st.balloons(); st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

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
                exp_r, cash_r, got_rare, rare_name, event = get_expedition_reward(exp_d['zone'], pet)
                pet['expedition'] = None
                pet['expeditions'] = pet.get('expeditions',0) + 1
                _rs = random.randint(*RUNE_SHARD_DROP['expedition'])
                pet['rune_shards'] = pet.get('rune_shards',0) + _rs
                _add_action(pet,'expedition')
                pet, lvup, gained_exp = add_exp(pet, exp_r)
                atomic_add_cash(uid, cash_r)
                st.session_state.global_cash += cash_r
                # v7: 이벤트 HP 효과
                if event['hp_effect'] != 0:
                    max_hp = 100 + pet.get('hp_bonus', 0)
                    pet['hp'] = max(1, min(max_hp, pet.get('hp',100) + event['hp_effect']))
                add_journal(pet, f"🗺️ {zone.get('name','탐험')} 완료! {event['icon']} {event['name']} EXP+{gained_exp} 💰+{format_korean_money(cash_r)}")
                if got_rare:
                    add_journal(pet, f"🎁 희귀 아이템 획득: {rare_name}!")
                save_pet(uid, pet)
                sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 탐험 보상 ({zone.get('name','')})", cash_r)
                del st.session_state['expedition_returned']
                st.toast(f"{event['icon']} {event['name']}! EXP +{gained_exp} | 💰 +{format_korean_money(cash_r)}", icon="✅")
                if got_rare: st.toast(f"✨ 희귀 아이템: {rare_name}!", icon="🎁")
                if lvup: st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

    # ── 일일 펫 한마디 (기분+계절+날씨 조합)
    season_name, season_icon = get_season()
    weather_now     = get_weather()
    weather_icon_now = WEATHER_ICONS.get(weather_now, "☀️")
    daily_quote = get_daily_quote(pet)
    st.markdown(f"""
    <div style='background:rgba(255,214,0,0.06);border:1px solid rgba(255,214,0,0.25);
                border-radius:14px;padding:14px 18px;margin-bottom:14px;
                font-style:italic;color:#FFD600;font-size:0.95rem;'>
        <span style='font-size:1.1rem;'>{mood_data['emoji']}</span>
        &nbsp;<b>{pet.get('name','펫')}</b>: "{daily_quote}"
        <span style='float:right;color:#64748B;font-size:0.8rem;'>{season_icon}{season_name} · {weather_icon_now}{weather_now}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── v9: 진화 연출 (레벨업으로 새 단계 도달 시 풀스크린 모션)
    _evo_pending = pet.pop('_evo_pending', None)
    if _evo_pending:
        save_pet(uid, pet)  # _evo_pending 제거된 상태 저장
        st.balloons()
        components.html(_evolution_cutscene_html(pet, sp, lv, _evo_pending), height=380)
        st.toast(f"✨ 진화! {_evo_pending['title']} 단계 도달!", icon="🌟")

    # ── Animated pet card
    feed_anim_flag = st.session_state.pop('feed_animation', False)
    components.html(
        generate_pet_animation_html(pet, sp, lv, exp, exp_pct, hunger, happy, hp, feed_anim=feed_anim_flag),
        height=460
    )

    # Stat bar below the card (v9: 6칸 — 진화/환생 추가)
    _need_disp = exp_to_next(lv) if lv < MAX_LEVEL else 0
    _exp_disp = f"{exp:,}/{_need_disp:,}" if lv < MAX_LEVEL else "MAX"
    _rb = pet.get('rebirth', 0)
    stat_cols = st.columns(6)
    stat_data = [
        ("⚡ Lv.", f"{lv:,}" + ("/5000" if lv < MAX_LEVEL else " MAX👑"), "#FFD600"),
        ("🧬 EXP", _exp_disp, "#00E5FF"),
        (f"{evo_cur['title'][:2]} 진화", f"{evo_cur['name']} (T{evo_cur['tier']})", evo_cur['aura']),
        ("♻️ 환생", get_rebirth_title(_rb) if _rb>0 else "없음", "#DD00FF" if _rb>0 else "#64748B"),
        ("🌡️ 기분", f"{mood_data['emoji']} {mood_name}", mood_data['color']),
        ("💰 패시브", format_korean_money(passive)+"/h" if passive>0 else "Lv.15~", "#00FF88"),
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
    tabs = st.tabs(["🍖 먹이","🎮 훈련","🗺️ 탐험","⚔️ 배틀","👗 아이템","🧪 레시피","💪 강화","📋 미션","📜 스킬","🏆 업적","📸 포토","📖 일지","📊 정보","💬 채팅","🧬 진화","♻️ 환생","🔮 룬"])

    # ── TAB 1: 먹이주기
    with tabs[0]:
        st.markdown('<div class="pet-tab-header">🍖 먹이 & 회복 아이템</div>', unsafe_allow_html=True)

        # ── 빠른 먹이기
        st.markdown("#### ⚡ 빠른 먹이기")
        qf1, qf2, qf3, qf4 = st.columns(4)
        quick_items = [
            ("kibble",   3, qf1),
            ("gourmet",  1, qf2),
            ("potion_s", 1, qf3),
            ("potion_l", 1, qf4),
        ]
        for f_id, qty, col in quick_items:
            food = PET_FOOD[f_id]
            cost = food['price'] * qty
            with col:
                label = f"{food['icon']} {food['name']}" + (f" ×{qty}" if qty>1 else "")
                if st.button(f"{label}\n{format_korean_money(cost)}", key=f"quick_{f_id}", use_container_width=True):
                    if st.session_state.global_cash < cost:
                        st.error("현금 부족!")
                    else:
                        st.session_state.global_cash -= cost
                        atomic_deduct_cash(uid, cost)
                        pet['hunger']    = min(100, pet.get('hunger',100) + food['hunger_restore']*qty)
                        pet['happiness'] = min(100, pet.get('happiness',100) + food['happiness']*qty)
                        pet['hp']        = min(100, pet.get('hp',100) + (food.get('hp_restore',0) or 5)*qty)
                        pet['last_fed']  = time.time()
                        pet['total_fed'] = pet.get('total_fed',0) + qty
                        pet['bond']      = pet.get('bond',0) + qty
                        pet, lv_up, ge = add_exp(pet, food['exp']*qty)
                        tag = "💊" if food.get('hp_restore',0) else "🍖"
                        add_journal(pet, f"{tag} {food['name']}×{qty}!")
                        _add_action(pet,'feed',qty)
                        save_pet(uid, pet); sync_user_data()
                        log_tx(uid,"펫",f"{pet['name']} {food['name']}×{qty}",-cost)
                        st.session_state['feed_animation'] = True
                        st.toast(f"{food['icon']}×{qty}! EXP+{ge}", icon="✅")
                        if lv_up: st.balloons(); st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

        st.write("---")
        st.markdown("#### 🍽️ 전체 목록")
        st.markdown('<div class="pet-sub">먹이줄수록 EXP·행복도↑ | 포션은 HP 직접 회복</div>', unsafe_allow_html=True)
        food_cols = st.columns(3)
        for i, (f_id, food) in enumerate(PET_FOOD.items()):
            with food_cols[i % 3]:
                hp_r = food.get('hp_restore', 0)
                is_potion = hp_r > 0
                border = "border-color:#FF4B4B44;" if is_potion else ""
                info_color = "#FF4B4B" if is_potion else "#00E5FF"
                # v8 수정: 안내문을 f-string 밖에서 미리 조립 (중첩 조건식이 가격을 깨뜨리던 버그 해결)
                _parts = []
                if is_potion:
                    _parts.append(f"❤️ HP +{hp_r}")
                else:
                    _parts.append(f"EXP +{food['exp']}")
                    if food['happiness']:
                        _parts.append(f"행복 +{food['happiness']}")
                if food['hunger_restore']:
                    _parts.append(f"허기 +{food['hunger_restore']}")
                info_line = " | ".join(_parts)
                price_str = format_korean_money(food['price'])
                st.markdown(
                    "<div class='pet-card' style='text-align:center;" + border + "'>"
                    "<div style='font-size:2.8rem;'>" + food['icon'] + "</div>"
                    "<div style='color:#E2E8F0;font-weight:700;margin-top:8px;'>" + food['name'] + "</div>"
                    "<div style='color:" + info_color + ";font-size:0.75rem;margin-top:4px;'>" + info_line + "</div>"
                    "<div style='color:#FFD600;font-weight:900;margin-top:8px;font-size:1rem;'>" + price_str + "</div>"
                    "</div>",
                    unsafe_allow_html=True)
                qty = st.number_input("수량", min_value=1, max_value=50, value=1, key=f"food_qty_{f_id}")
                if st.button(f"{food['icon']} {'포션 사용' if is_potion else '먹이기'} ×{qty}", key=f"feed_{f_id}", use_container_width=True):
                    total_cost = food['price'] * qty
                    if st.session_state.global_cash < total_cost:
                        st.error("현금 부족!")
                    else:
                        st.session_state.global_cash -= total_cost
                        atomic_deduct_cash(uid, total_cost)
                        pet['hunger']    = min(100, pet.get('hunger',100) + food['hunger_restore']*qty)
                        pet['happiness'] = min(100, pet.get('happiness',100) + food['happiness']*qty)
                        if is_potion:
                            pet['hp'] = min(100, pet.get('hp',100) + hp_r*qty)
                        else:
                            pet['hp'] = min(100, pet.get('hp',100) + 5*qty)
                        pet['last_fed']  = time.time()
                        pet['total_fed'] = pet.get('total_fed',0) + qty
                        pet['bond']      = pet.get('bond',0) + qty
                        pet, leveled_up, gained_exp = add_exp(pet, food['exp']*qty)
                        tag = "💊" if is_potion else "🍖"
                        add_journal(pet, f"{tag} {food['name']}×{qty}! {f'HP+{hp_r*qty}' if is_potion else f'EXP+{gained_exp}'}")
                        save_pet(uid, pet); sync_user_data()
                        log_tx(uid,"펫",f"{pet['name']} 먹이({food['name']}×{qty})",-total_cost)
                        st.session_state['feed_animation'] = True
                        st.toast(f"{food['icon']}×{qty}! {'HP +' + str(hp_r*qty) if is_potion else 'EXP +' + str(gained_exp)}", icon="✅")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

    # ── TAB 2: 훈련
    with tabs[1]:
        st.markdown('<div class="pet-tab-header">🎮 훈련 미니게임</div>', unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # v8 신규: 타이밍 명중 게임 (포털 임베드에서도 100% 작동 — 순수 JS)
        # ──────────────────────────────────────────
        st.markdown("#### 🎯 타이밍 명중 게임 (실제 플레이!)")
        st.markdown('<div class="pet-sub">움직이는 게이지를 멈춰 가운데 PERFECT 존을 맞춰라! 정확할수록 EXP 폭발 💥 (rerun 없이 즉시 판정 · 모바일 터치 지원)</div>', unsafe_allow_html=True)

        TM_COST = TIMING_GAME['cost']
        st.markdown(
            "<div class='pet-card' style='padding:10px 14px;margin-bottom:10px;'>"
            "<span class='stat-chip' style='background:rgba(255,214,0,0.12);color:#FFD600;'>💰 비용 " + format_korean_money(TM_COST) + "</span>"
            "<span class='stat-chip' style='background:rgba(0,255,136,0.12);color:#00FF88;'>⭐ PERFECT 시 ×3.5 EXP</span>"
            "<span class='stat-chip' style='background:rgba(0,229,255,0.12);color:#00E5FF;'>🎮 STOP 타이밍 게임</span>"
            "</div>", unsafe_allow_html=True)

        timing_html = """
        <div style="font-family:'Pretendard',-apple-system,'Segoe UI',sans-serif;text-align:center;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #00E5FF;border-radius:18px;padding:22px 18px;color:#fff;box-shadow:0 0 30px rgba(0,229,255,0.15) inset;">
          <div style="font-size:1.05rem;font-weight:900;color:#00E5FF;margin-bottom:14px;letter-spacing:1px;">🎯 타이밍 명중!</div>
          <div id="track" style="position:relative;height:44px;border-radius:10px;overflow:hidden;background:linear-gradient(90deg,#475569 0%,#475569 12%,#0088aa 12%,#0088aa 30%,#00aa55 30%,#00aa55 42%,#FFD600 42%,#FFD600 58%,#00aa55 58%,#00aa55 70%,#0088aa 70%,#0088aa 88%,#475569 88%);border:1px solid rgba(255,255,255,0.18);box-shadow:0 2px 10px rgba(0,0,0,0.4) inset;">
            <div style="position:absolute;left:42%;top:0;width:16%;height:100%;background:rgba(255,214,0,0.25);border-left:1px dashed rgba(255,255,255,0.4);border-right:1px dashed rgba(255,255,255,0.4);"></div>
            <div id="needle" style="position:absolute;top:-5px;left:0%;width:5px;height:54px;background:#fff;box-shadow:0 0 10px #fff,0 0 20px #00E5FF;border-radius:3px;"></div>
          </div>
          <div style="display:flex;justify-content:space-between;margin-top:6px;font-size:0.6rem;color:#64748B;padding:0 2px;">
            <span>빗나감</span><span style="color:#00E5FF;">GOOD</span><span style="color:#00FF88;">GREAT</span><span style="color:#FFD600;font-weight:900;">PERFECT</span><span style="color:#00FF88;">GREAT</span><span style="color:#00E5FF;">GOOD</span><span>빗나감</span>
          </div>
          <div id="tmresult" style="font-size:1.35rem;font-weight:900;margin:16px 0;min-height:32px;color:#64748B;">START를 눌러 시작!</div>
          <button id="tmbtn" style="width:100%;padding:20px;font-size:1.3rem;font-weight:900;background:linear-gradient(135deg,#00E5FF,#0088cc);color:#001;border:none;border-radius:14px;cursor:pointer;touch-action:manipulation;user-select:none;-webkit-tap-highlight-color:transparent;box-shadow:0 4px 0 #006699;transition:transform 0.05s;">▶ START</button>
          <div style="color:#64748B;font-size:0.72rem;margin-top:10px;">멈춘 뒤 아래 <b style="color:#00E5FF;">보상받기</b> 버튼을 누르세요</div>
        </div>
        <script>
        (function(){
          var needle=document.getElementById('needle'),btn=document.getElementById('tmbtn'),resEl=document.getElementById('tmresult');
          var pos=0,dir=1,speed=1.65,running=false,raf,locked=false;
          function move(){pos+=dir*speed;if(pos>=100){pos=100;dir=-1;}if(pos<=0){pos=0;dir=1;}needle.style.left=pos+'%';raf=requestAnimationFrame(move);}
          function zoneOf(p){var z=[[0,12,0.5,'빗나감 😢','#94A3B8'],[12,30,1.0,'GOOD','#00E5FF'],[30,42,2.0,'GREAT!','#00FF88'],[42,58,3.5,'⭐ PERFECT! ⭐','#FFD600'],[58,70,2.0,'GREAT!','#00FF88'],[70,88,1.0,'GOOD','#00E5FF'],[88,100,0.5,'빗나감 😢','#94A3B8']];for(var i=0;i<z.length;i++){if(p>=z[i][0]&&p<=z[i][1])return z[i];}return z[0];}
          function start(){running=true;locked=false;btn.textContent='🛑 STOP!';btn.style.background='linear-gradient(135deg,#FF4B4B,#cc0000)';btn.style.boxShadow='0 4px 0 #990000';resEl.textContent='지금 멈춰!';resEl.style.color='#fff';raf=requestAnimationFrame(move);}
          function stop(){running=false;locked=true;cancelAnimationFrame(raf);var z=zoneOf(pos);needle.style.boxShadow='0 0 16px '+z[4]+',0 0 30px '+z[4];resEl.innerHTML='<span style="color:'+z[4]+';">'+z[3]+'</span> <span style="color:#FFD600;font-size:0.95rem;">(×'+z[2]+')</span>';btn.textContent='✅ 결과 전송 완료';btn.style.opacity='0.55';btn.style.background='linear-gradient(135deg,#334155,#1e293b)';btn.style.boxShadow='0 4px 0 #0f172a';btn.disabled=true;var score=Math.round(z[2]*10);try{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){if(inp.getAttribute('aria-label')==='__tm_score__'){var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(score));inp.dispatchEvent(new Event('input',{bubbles:true}));inp.dispatchEvent(new Event('change',{bubbles:true}));}});}catch(e){}}
          function click(e){if(e){e.preventDefault();}if(locked)return;if(!running){start();}else{stop();}}
          btn.addEventListener('click',click);btn.addEventListener('touchstart',click,{passive:false});
        })();
        </script>
        """
        components.html(timing_html, height=300)

        tmc1, tmc2 = st.columns([2,1])
        with tmc1:
            tm_score = st.text_input("__tm_score__", value="", key="tm_score_input",
                                     label_visibility="collapsed", placeholder="명중 결과가 자동 입력됩니다")
        with tmc2:
            claim_tm = st.button("🎁 보상받기", key="tm_claim", use_container_width=True, type="primary")

        if claim_tm:
            try:
                mult10 = int(str(tm_score).strip() or "0")
            except ValueError:
                mult10 = 0
            if mult10 <= 0:
                st.warning("먼저 게임에서 STOP을 눌러 결과를 만든 뒤 보상받기를 눌러주세요!")
            elif st.session_state.global_cash < TM_COST:
                st.error(f"현금 부족! {format_korean_money(TM_COST)} 필요")
            elif pet.get('happiness', 100) < 10:
                st.error("행복도가 너무 낮아요! 먼저 쓰다듬거나 같이 놀아주세요 🥺")
            elif st.session_state.get('_tm_last') == mult10 and st.session_state.get('_tm_claimed'):
                st.info("이미 이 결과로 보상받았어요. 다시 플레이한 뒤 받아주세요!")
            else:
                mult = mult10 / 10.0
                exp_reward = int(TIMING_GAME['base_exp'] * mult)
                st.session_state.global_cash -= TM_COST
                atomic_deduct_cash(uid, TM_COST)
                pet['happiness']   = max(0, pet.get('happiness', 100) - 5)
                pet['last_played'] = time.time()
                pet['bond']        = pet.get('bond', 0) + 4
                pet, lvup, ge = add_exp(pet, exp_reward)
                grade = "⭐PERFECT⭐" if mult >= 3.5 else "GREAT" if mult >= 2.0 else "GOOD" if mult >= 1.0 else "빗나감"
                add_journal(pet, f"🎯 타이밍 명중 [{grade}] EXP+{ge}")
                _add_action(pet, 'train')
                save_pet(uid, pet); sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 타이밍게임({grade})", -TM_COST)
                st.session_state['_tm_last'] = mult10
                st.session_state['_tm_claimed'] = True
                st.toast(f"🎯 {grade}! EXP +{ge}", icon="🎮")
                if mult >= 3.5: st.balloons()
                if lvup: st.balloons(); st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()
        else:
            if st.session_state.get('_tm_last') != (tm_score or ''):
                st.session_state['_tm_claimed'] = False

        st.write("---")
        st.markdown("#### 🎮 훈련 미니게임 — 펫과 함께!")
        st.markdown('<div class="pet-sub">펫이 직접 참여하는 훈련이에요! 게임을 플레이하고 결과에 따라 EXP를 획득합니다. 5% 확률 잭팟도 있어요 🎰</div>', unsafe_allow_html=True)

        # ── 훈련 미니게임 선택
        pet_sprite = get_pet_sprite(pet.get('species','cat'), pet.get('level',1))
        pet_name_disp = pet.get('name', '펫')

        mini_game_choice = st.radio(
            "훈련 종목 선택",
            ["🧠 기억력 훈련", "⚡ 반응속도 훈련", "💪 체력(연타) 훈련", "🏃 민첩 훈련", "🔮 마력 훈련", "⚔️ 전투 훈련"],
            horizontal=True, key="mini_game_choice"
        )

        game_map = {
            "🧠 기억력 훈련":  ("memory",  30, 1_000_000),
            "⚡ 반응속도 훈련": ("speed",   20,   500_000),
            "💪 체력(연타) 훈련":("strength",25,   800_000),
            "🏃 민첩 훈련":    ("agility", 40, 1_500_000),
            "🔮 마력 훈련":    ("magic",   55, 2_500_000),
            "⚔️ 전투 훈련":    ("battle",  70, 4_000_000),
        }
        sel_id, sel_exp, sel_cost = game_map[mini_game_choice]

        st.markdown(
            f"<div class='pet-card' style='padding:10px 14px;margin-bottom:10px;'>"
            f"<span style='font-size:1.5rem;margin-right:10px;'>{pet_sprite}</span>"
            f"<span style='color:#E2E8F0;font-weight:700;'>{pet_name_disp}</span>이(가) 훈련에 참여합니다! &nbsp;"
            f"<span class='stat-chip' style='background:rgba(255,214,0,0.12);color:#FFD600;'>💰 {format_korean_money(sel_cost)}</span>"
            f"<span class='stat-chip' style='background:rgba(0,255,136,0.12);color:#00FF88;'>⭐ 기본 EXP +{sel_exp}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # ──────────────────────────────────────────
        # 기억력 훈련 — 시퀀스 기억 게임
        # ──────────────────────────────────────────
        if sel_id == "memory":
            mem_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #AA00FF;border-radius:18px;padding:20px;color:#fff;box-shadow:0 0 30px rgba(170,0,255,0.15) inset;">
              <div style="text-align:center;font-size:1rem;font-weight:900;color:#AA00FF;margin-bottom:12px;letter-spacing:1px;">🧠 {pet_name_disp}과 기억력 훈련! 순서를 기억해서 따라 클릭하세요</div>
              <div id="mem-pet" style="text-align:center;font-size:3rem;margin-bottom:8px;transition:transform 0.15s;">{pet_sprite}</div>
              <div id="mem-msg" style="text-align:center;color:#94A3B8;font-size:0.85rem;margin-bottom:14px;min-height:22px;">START를 눌러 시작!</div>
              <div id="mem-btns" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;max-width:280px;margin:0 auto 16px;">
                <button id="mb0" data-i="0" onclick="memClick(0)" style="padding:22px;font-size:1.5rem;background:rgba(255,75,75,0.15);border:2px solid #FF4B4B;border-radius:12px;cursor:pointer;color:#fff;transition:all 0.1s;">🔴</button>
                <button id="mb1" data-i="1" onclick="memClick(1)" style="padding:22px;font-size:1.5rem;background:rgba(0,229,255,0.15);border:2px solid #00E5FF;border-radius:12px;cursor:pointer;color:#fff;transition:all 0.1s;">🔵</button>
                <button id="mb2" data-i="2" onclick="memClick(2)" style="padding:22px;font-size:1.5rem;background:rgba(0,255,136,0.15);border:2px solid #00FF88;border-radius:12px;cursor:pointer;color:#fff;transition:all 0.1s;">🟢</button>
                <button id="mb3" data-i="3" onclick="memClick(3)" style="padding:22px;font-size:1.5rem;background:rgba(255,214,0,0.15);border:2px solid #FFD600;border-radius:12px;cursor:pointer;color:#fff;transition:all 0.1s;">🟡</button>
              </div>
              <button id="mem-start" onclick="memStart()" style="width:100%;padding:14px;font-size:1.1rem;font-weight:900;background:linear-gradient(135deg,#AA00FF,#7700DD);color:#fff;border:none;border-radius:12px;cursor:pointer;">▶ START</button>
            </div>
            <script>
            (function(){{
              var seq=[],userSeq=[],step=0,showing=false,score=0,maxRound=5;
              var colors=['#FF4B4B','#00E5FF','#00FF88','#FFD600'];
              var pet=document.getElementById('mem-pet');
              function msg(t){{document.getElementById('mem-msg').textContent=t;}}
              function flash(i,cb){{
                var b=document.getElementById('mb'+i);
                b.style.background=colors[i]+'88';b.style.transform='scale(1.1)';
                setTimeout(function(){{b.style.background='rgba('+hexRgb(colors[i])+',0.15)';b.style.transform='scale(1)';if(cb)cb();}},400);
              }}
              function hexRgb(h){{var r=parseInt(h.slice(1,3),16),g=parseInt(h.slice(3,5),16),b=parseInt(h.slice(5,7),16);return r+','+g+','+b;}}
              function showSeq(idx){{
                if(idx>=seq.length){{showing=false;step=0;msg('따라 클릭하세요! ('+seq.length+'번)');return;}}
                pet.style.transform='scale(1.2)';setTimeout(function(){{pet.style.transform='scale(1)';}},200);
                flash(seq[idx],function(){{setTimeout(function(){{showSeq(idx+1);}},300);}});
              }}
              function memStart(){{
                seq=[];userSeq=[];step=0;score=0;showing=true;
                document.getElementById('mem-start').style.display='none';
                for(var r=0;r<maxRound;r++)seq.push(Math.floor(Math.random()*4));
                msg('잘 봐! 순서를 기억해!');
                setTimeout(function(){{showSeq(0);}},600);
              }}
              window.memClick=function(i){{
                if(showing)return;
                flash(i);
                if(i===seq[step]){{
                  step++;
                  if(step>=seq.length){{
                    score=seq.length;
                    pet.textContent='🎉';
                    msg('완벽해! 전부 맞췄어! ×'+score+' EXP');
                    sendScore(score*2);
                  }} else {{ msg((seq.length-step)+'개 남았어!'); }}
                }} else {{
                  score=step;
                  pet.textContent='😢';
                  msg('틀렸어... '+step+'/'+seq.length+' 맞춤');
                  sendScore(score);
                }}
              }};
              function sendScore(s){{
                try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}
              }}
            }})();
            </script>
            """
            components.html(mem_html, height=340)

        # ──────────────────────────────────────────
        # 반응속도 훈련 — 빛나면 클릭!
        # ──────────────────────────────────────────
        elif sel_id == "speed":
            speed_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #00E5FF;border-radius:18px;padding:20px;color:#fff;text-align:center;">
              <div style="font-size:1rem;font-weight:900;color:#00E5FF;margin-bottom:12px;">⚡ {pet_name_disp}과 반응속도 훈련! 빛나면 즉시 클릭!</div>
              <div id="sp-pet" style="font-size:3rem;margin-bottom:8px;transition:all 0.15s;">{pet_sprite}</div>
              <div id="sp-msg" style="color:#94A3B8;font-size:0.9rem;margin-bottom:16px;min-height:22px;">START를 눌러 시작!</div>
              <div id="sp-target" onclick="spClick()" style="width:120px;height:120px;border-radius:50%;margin:0 auto 18px;background:rgba(255,255,255,0.05);border:3px solid #334155;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:3rem;transition:all 0.1s;user-select:none;">⚫</div>
              <div id="sp-score" style="color:#FFD600;font-weight:900;font-size:1rem;margin-bottom:12px;"></div>
              <button id="sp-start" onclick="spStart()" style="width:100%;padding:14px;font-size:1.1rem;font-weight:900;background:linear-gradient(135deg,#00E5FF,#0088cc);color:#001;border:none;border-radius:12px;cursor:pointer;">▶ START</button>
            </div>
            <script>
            (function(){{
              var rounds=5,hit=0,round=0,waiting=false,timeout,startTime;
              var pet=document.getElementById('sp-pet'),tgt=document.getElementById('sp-target'),msgEl=document.getElementById('sp-msg'),scEl=document.getElementById('sp-score');
              function msg(t){{msgEl.textContent=t;}}
              function spStart(){{
                hit=0;round=0;document.getElementById('sp-start').style.display='none';
                nextRound();
              }}
              function nextRound(){{
                if(round>=rounds){{
                  var sc=Math.round((hit/rounds)*10);
                  pet.textContent=hit>=4?'🎉':'😤';
                  msg(hit+'/'+rounds+' 성공! '+(hit>=4?'빠르다!':'아쉽다'));
                  scEl.textContent='결과: '+hit+'/'+rounds;
                  sendScore(sc); return;
                }}
                tgt.style.background='rgba(255,255,255,0.05)';tgt.style.borderColor='#334155';tgt.textContent='⚫';
                waiting=false; msg('준비...');
                var delay=1200+Math.random()*2000;
                timeout=setTimeout(function(){{waiting=true;tgt.style.background='rgba(0,229,255,0.3)';tgt.style.borderColor='#00E5FF';tgt.textContent='⚡';tgt.style.boxShadow='0 0 30px #00E5FF';msg('지금!!');startTime=Date.now();}},delay);
              }}
              window.spClick=function(){{
                if(!waiting){{clearTimeout(timeout);msg('너무 빨라! 기다려!');tgt.style.borderColor='#FF4B4B';setTimeout(function(){{nextRound();}},800);return;}}
                waiting=false;hit++;round++;
                var rt=Date.now()-startTime;
                pet.style.transform='scale(1.2)';setTimeout(function(){{pet.style.transform='scale(1)';}},200);
                tgt.style.background='rgba(0,255,136,0.3)';tgt.style.borderColor='#00FF88';tgt.textContent='✅';
                msg(rt+'ms! '+(rt<350?'초고속!':rt<600?'빠름!':'조금 느림'));
                setTimeout(function(){{nextRound();}},900);
              }};
              function sendScore(s){{try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}}}
            }})();
            </script>
            """
            components.html(speed_html, height=330)

        # ──────────────────────────────────────────
        # 체력(연타) 훈련 — 빠르게 연타!
        # ──────────────────────────────────────────
        elif sel_id == "strength":
            strength_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #FF4B4B;border-radius:18px;padding:20px;color:#fff;text-align:center;">
              <div style="font-size:1rem;font-weight:900;color:#FF4B4B;margin-bottom:10px;">💪 {pet_name_disp}의 체력 훈련! 5초 안에 최대한 연타!</div>
              <div id="st-pet" style="font-size:3.5rem;margin-bottom:6px;">{pet_sprite}</div>
              <div id="st-timer" style="font-size:2rem;font-weight:900;color:#FFD600;margin-bottom:6px;">5.0</div>
              <div id="st-count" style="font-size:2.5rem;font-weight:900;color:#FF4B4B;margin-bottom:8px;">0</div>
              <div id="st-msg" style="color:#94A3B8;font-size:0.85rem;margin-bottom:14px;min-height:20px;">START 후 펀치 버튼 연타!</div>
              <button id="st-punch" onclick="stPunch()" style="width:140px;height:140px;border-radius:50%;font-size:2.5rem;background:rgba(255,75,75,0.15);border:3px solid #FF4B4B;cursor:pointer;color:#fff;display:none;transition:all 0.05s;user-select:none;-webkit-tap-highlight-color:transparent;">👊</button>
              <button id="st-start" onclick="stStart()" style="width:100%;padding:14px;font-size:1.1rem;font-weight:900;background:linear-gradient(135deg,#FF4B4B,#cc0000);color:#fff;border:none;border-radius:12px;cursor:pointer;margin-top:10px;">▶ START</button>
            </div>
            <script>
            (function(){{
              var cnt=0,running=false,interval,timeLeft=5.0;
              var pet=document.getElementById('st-pet'),timerEl=document.getElementById('st-timer'),cntEl=document.getElementById('st-count'),msgEl=document.getElementById('st-msg');
              function stStart(){{
                cnt=0;timeLeft=5.0;running=true;
                document.getElementById('st-start').style.display='none';
                document.getElementById('st-punch').style.display='inline-block';
                msgEl.textContent='연타! 연타! 연타!';
                interval=setInterval(function(){{
                  timeLeft=Math.max(0,timeLeft-0.1);
                  timerEl.textContent=timeLeft.toFixed(1);
                  if(timeLeft<=0){{
                    clearInterval(interval);running=false;
                    document.getElementById('st-punch').style.display='none';
                    var sc=cnt>=60?10:cnt>=40?7:cnt>=25?5:cnt>=15?3:1;
                    pet.textContent=cnt>=40?'🎉':'💪';
                    msgEl.textContent=cnt+'번 연타! '+(cnt>=60?'전설!':cnt>=40?'엄청나!':cnt>=25?'잘했어!':'더 연습!');
                    sendScore(sc);
                  }}
                }},100);
              }}
              window.stPunch=function(){{
                if(!running)return;
                cnt++;cntEl.textContent=cnt;
                pet.style.transform='scale(1.3) rotate(-10deg)';
                setTimeout(function(){{pet.style.transform='scale(1)';pet.style.color='';}} ,80);
                var b=document.getElementById('st-punch');
                b.style.transform='scale(0.9)';setTimeout(function(){{b.style.transform='scale(1)';}},60);
              }};
              function sendScore(s){{try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}}}
            }})();
            </script>
            """
            components.html(strength_html, height=350)

        # ──────────────────────────────────────────
        # 민첩 훈련 — 나타나는 목표물 클릭!
        # ──────────────────────────────────────────
        elif sel_id == "agility":
            agility_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #00FF88;border-radius:18px;padding:16px;color:#fff;text-align:center;">
              <div style="font-size:1rem;font-weight:900;color:#00FF88;margin-bottom:8px;">🏃 {pet_name_disp}의 민첩 훈련! 나타나는 순간 잡아라!</div>
              <div id="ag-pet" style="font-size:2.5rem;margin-bottom:4px;">{pet_sprite}</div>
              <div id="ag-info" style="color:#94A3B8;font-size:0.82rem;margin-bottom:10px;">TARGET: <span id="ag-score" style="color:#FFD600;font-weight:900;">0</span>/8 &nbsp; 시간: <span id="ag-time" style="color:#00E5FF;font-weight:900;">30</span>s</div>
              <div id="ag-arena" style="position:relative;width:100%;height:180px;background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:12px;overflow:hidden;margin-bottom:10px;cursor:pointer;" onclick="agClick(event)"></div>
              <div id="ag-msg" style="color:#94A3B8;font-size:0.85rem;margin-bottom:10px;min-height:20px;">START 후 아레나에서 목표물을 클릭!</div>
              <button id="ag-start" onclick="agStart()" style="width:100%;padding:12px;font-size:1.05rem;font-weight:900;background:linear-gradient(135deg,#00FF88,#00CC55);color:#001;border:none;border-radius:12px;cursor:pointer;">▶ START</button>
            </div>
            <script>
            (function(){{
              var score=0,timeLeft=30,running=false,interval,targets=[];
              var arena=document.getElementById('ag-arena'),scEl=document.getElementById('ag-score'),tmEl=document.getElementById('ag-time'),msgEl=document.getElementById('ag-msg'),pet=document.getElementById('ag-pet');
              var emojis=['🎯','⭐','💎','🔥','⚡','🌟'];
              function spawnTarget(){{
                if(!running)return;
                var t=document.createElement('div');
                var x=Math.random()*80,y=Math.random()*75;
                var em=emojis[Math.floor(Math.random()*emojis.length)];
                t.style.cssText='position:absolute;font-size:2rem;cursor:pointer;left:'+x+'%;top:'+y+'%;transform:scale(0);transition:transform 0.15s;user-select:none;';
                t.textContent=em;t.dataset.alive='1';
                arena.appendChild(t);targets.push(t);
                setTimeout(function(){{t.style.transform='scale(1)';}},50);
                setTimeout(function(){{if(t.dataset.alive==='1'){{t.style.opacity='0';setTimeout(function(){{t.remove();}},300);}}}},1800);
                setTimeout(function(){{spawnTarget();}},600+Math.random()*800);
              }}
              function agStart(){{
                score=0;timeLeft=30;running=true;
                document.getElementById('ag-start').style.display='none';
                scEl.textContent='0';msgEl.textContent='잡아라!';
                spawnTarget();
                interval=setInterval(function(){{
                  timeLeft--;tmEl.textContent=timeLeft;
                  if(timeLeft<=0){{
                    clearInterval(interval);running=false;
                    targets.forEach(function(t){{t.remove();}});targets=[];
                    var sc=score>=8?10:score>=6?8:score>=4?5:score>=2?3:1;
                    pet.textContent=score>=6?'🎉':'😤';
                    msgEl.textContent=score+'개 잡음! '+(score>=8?'신의 손!':score>=5?'날쌘!':'더 연습!');
                    sendScore(sc);
                  }}
                }},1000);
              }}
              window.agClick=function(e){{
                if(!running)return;
                var el=e.target;
                if(el.dataset&&el.dataset.alive==='1'){{
                  el.dataset.alive='0';el.style.transform='scale(1.5)';el.style.opacity='0';
                  score++;scEl.textContent=score;
                  pet.style.transform='scale(1.2)';setTimeout(function(){{pet.style.transform='scale(1)';}},150);
                  setTimeout(function(){{el.remove();}},300);
                }}
              }};
              function sendScore(s){{try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}}}
            }})();
            </script>
            """
            components.html(agility_html, height=360)

        # ──────────────────────────────────────────
        # 마력 훈련 — 룬 순서 맞추기
        # ──────────────────────────────────────────
        elif sel_id == "magic":
            magic_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #7700DD;border-radius:18px;padding:20px;color:#fff;text-align:center;">
              <div style="font-size:1rem;font-weight:900;color:#AA00FF;margin-bottom:10px;">🔮 {pet_name_disp}의 마력 훈련! 룬을 올바른 순서로!</div>
              <div id="mg-pet" style="font-size:3rem;margin-bottom:6px;">{pet_sprite}</div>
              <div id="mg-display" style="font-size:2.5rem;letter-spacing:12px;margin-bottom:10px;min-height:44px;background:rgba(170,0,255,0.1);border:1px solid #7700DD;border-radius:10px;padding:8px;"></div>
              <div id="mg-msg" style="color:#94A3B8;font-size:0.85rem;margin-bottom:12px;min-height:20px;">START를 눌러 룬을 확인하고 순서대로 클릭!</div>
              <div id="mg-runes" style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;"></div>
              <div id="mg-input" style="font-size:2rem;letter-spacing:8px;min-height:40px;margin-bottom:10px;color:#AA00FF;font-weight:900;"></div>
              <button id="mg-start" onclick="mgStart()" style="width:100%;padding:12px;font-size:1.05rem;font-weight:900;background:linear-gradient(135deg,#AA00FF,#7700DD);color:#fff;border:none;border-radius:12px;cursor:pointer;">▶ START</button>
            </div>
            <script>
            (function(){{
              var runes=['🔴','🔵','🟢','🟡','🟣','🟠'],seq=[],input=[],round=0,maxRound=4,totalScore=0;
              var dispEl=document.getElementById('mg-display'),msgEl=document.getElementById('mg-msg'),runeDiv=document.getElementById('mg-runes'),inputEl=document.getElementById('mg-input'),pet=document.getElementById('mg-pet');
              function buildButtons(){{
                runeDiv.innerHTML='';
                runes.forEach(function(r,i){{
                  var b=document.createElement('button');
                  b.textContent=r;b.style.cssText='font-size:1.8rem;padding:10px 14px;background:rgba(255,255,255,0.05);border:2px solid rgba(255,255,255,0.15);border-radius:10px;cursor:pointer;color:#fff;';
                  b.onclick=function(){{mgInput(r);}};runeDiv.appendChild(b);
                }});
              }}
              function mgStart(){{
                round=0;totalScore=0;input=[];inputEl.textContent='';
                document.getElementById('mg-start').style.display='none';
                buildButtons();nextRound();
              }}
              function nextRound(){{
                if(round>=maxRound){{
                  var sc=Math.round((totalScore/maxRound)*10);
                  pet.textContent=totalScore>=3?'🎉':'😤';
                  msgEl.textContent=totalScore+'/'+maxRound+' 라운드 성공! '+(totalScore>=3?'마법사!':'더 연습!');
                  runeDiv.innerHTML='';sendScore(sc);return;
                }}
                var len=round+2;seq=[];
                for(var i=0;i<len;i++)seq.push(runes[Math.floor(Math.random()*runes.length)]);
                input=[];inputEl.textContent='';dispEl.textContent=seq.join(' ');
                msgEl.textContent='기억해! 3초 후 사라져요...';
                setTimeout(function(){{dispEl.textContent='❓'.repeat(seq.length);msgEl.textContent='순서대로 클릭! ('+seq.length+'개)';}},2500);
              }}
              window.mgInput=function(r){{
                if(!seq.length)return;
                input.push(r);inputEl.textContent=input.join(' ');
                var idx=input.length-1;
                if(input[idx]!==seq[idx]){{
                  pet.textContent='😢';msgEl.textContent='틀렸어! 다음 라운드...';
                  input=[];setTimeout(function(){{round++;nextRound();}},1000);return;
                }}
                if(input.length===seq.length){{
                  totalScore++;round++;pet.style.transform='scale(1.3)';
                  msgEl.textContent='완벽! 다음 라운드!';
                  setTimeout(function(){{pet.style.transform='scale(1)';nextRound();}},700);
                }}
              }};
              function sendScore(s){{try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}}}
            }})();
            </script>
            """
            components.html(magic_html, height=370)

        # ──────────────────────────────────────────
        # 전투 훈련 — 콤보 입력 게임
        # ──────────────────────────────────────────
        elif sel_id == "battle":
            battle_html = f"""
            <div style="font-family:-apple-system,sans-serif;background:linear-gradient(160deg,#0a0f1e,#06101a);border:2px solid #FF9500;border-radius:18px;padding:18px;color:#fff;text-align:center;">
              <div style="font-size:1rem;font-weight:900;color:#FF9500;margin-bottom:10px;">⚔️ {pet_name_disp}의 전투 훈련! 화면에 뜨는 콤보를 따라 입력!</div>
              <div id="bt-pet" style="font-size:3rem;margin-bottom:6px;">{pet_sprite}</div>
              <div id="bt-combo-show" style="font-size:2rem;letter-spacing:8px;min-height:48px;background:rgba(255,149,0,0.1);border:1px solid #FF9500;border-radius:10px;padding:8px;margin-bottom:8px;"></div>
              <div id="bt-input-show" style="font-size:2rem;letter-spacing:8px;min-height:40px;color:#FFD600;font-weight:900;margin-bottom:6px;"></div>
              <div id="bt-msg" style="color:#94A3B8;font-size:0.85rem;margin-bottom:12px;min-height:20px;">START 후 표시되는 콤보를 버튼으로 따라 입력!</div>
              <div id="bt-btns" style="display:flex;gap:10px;justify-content:center;margin-bottom:14px;">
                <button onclick="btInput('👊')" style="font-size:1.6rem;padding:12px 16px;background:rgba(255,75,75,0.15);border:2px solid #FF4B4B;border-radius:10px;cursor:pointer;color:#fff;">👊</button>
                <button onclick="btInput('🦵')" style="font-size:1.6rem;padding:12px 16px;background:rgba(0,229,255,0.15);border:2px solid #00E5FF;border-radius:10px;cursor:pointer;color:#fff;">🦵</button>
                <button onclick="btInput('🛡️')" style="font-size:1.6rem;padding:12px 16px;background:rgba(0,255,136,0.15);border:2px solid #00FF88;border-radius:10px;cursor:pointer;color:#fff;">🛡️</button>
                <button onclick="btInput('✨')" style="font-size:1.6rem;padding:12px 16px;background:rgba(255,214,0,0.15);border:2px solid #FFD600;border-radius:10px;cursor:pointer;color:#fff;">✨</button>
              </div>
              <button id="bt-start" onclick="btStart()" style="width:100%;padding:12px;font-size:1.05rem;font-weight:900;background:linear-gradient(135deg,#FF9500,#FF6B00);color:#fff;border:none;border-radius:12px;cursor:pointer;">▶ START</button>
            </div>
            <script>
            (function(){{
              var moves=['👊','🦵','🛡️','✨'],combo=[],input=[],round=0,maxRound=5,score=0;
              var comboEl=document.getElementById('bt-combo-show'),inputEl=document.getElementById('bt-input-show'),msgEl=document.getElementById('bt-msg'),pet=document.getElementById('bt-pet');
              function btStart(){{
                round=0;score=0;
                document.getElementById('bt-start').style.display='none';
                nextCombo();
              }}
              function nextCombo(){{
                if(round>=maxRound){{
                  var sc=Math.round((score/maxRound)*10);
                  pet.textContent=score>=4?'🎉':'😤';
                  msgEl.textContent=score+'/'+maxRound+' 콤보 성공! '+(score>=4?'전투왕!':'더 연습!');
                  comboEl.textContent='';inputEl.textContent='';sendScore(sc);return;
                }}
                var len=round+2;combo=[];
                for(var i=0;i<len;i++)combo.push(moves[Math.floor(Math.random()*moves.length)]);
                input=[];inputEl.textContent='';comboEl.textContent=combo.join(' ');
                msgEl.textContent='콤보를 따라 입력! ('+len+'번)';
              }}
              window.btInput=function(m){{
                if(!combo.length)return;
                input.push(m);inputEl.textContent=input.join(' ');
                var idx=input.length-1;
                if(input[idx]!==combo[idx]){{
                  pet.textContent='😢';comboEl.style.borderColor='#FF4B4B';
                  msgEl.textContent='틀렸어! 다음 콤보...';
                  input=[];round++;setTimeout(function(){{comboEl.style.borderColor='#FF9500';nextCombo();}},800);return;
                }}
                if(input.length===combo.length){{
                  score++;round++;pet.style.transform='scale(1.3)';
                  comboEl.style.borderColor='#00FF88';
                  msgEl.textContent='콤보 성공! 🔥';
                  setTimeout(function(){{pet.style.transform='scale(1)';comboEl.style.borderColor='#FF9500';nextCombo();}},700);
                }}
              }};
              function sendScore(s){{try{{var inputs=window.parent.document.querySelectorAll('input[type=text]');inputs.forEach(function(inp){{if(inp.getAttribute('aria-label')==='__mg_score__'){{var setter=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;setter.call(inp,String(s));inp.dispatchEvent(new Event('input',{{bubbles:true}}));inp.dispatchEvent(new Event('change',{{bubbles:true}}));}}}})}};catch(e){{}}}}
            }})();
            </script>
            """
            components.html(battle_html, height=370)

        # ── 미니게임 공통 보상 처리
        mg_c1, mg_c2 = st.columns([2, 1])
        with mg_c1:
            mg_score_raw = st.text_input(
                "__mg_score__", value="", key=f"mg_score_{sel_id}",
                label_visibility="collapsed", placeholder="게임 결과가 자동 입력됩니다"
            )
        with mg_c2:
            mg_claim = st.button("🎁 훈련 보상받기", key=f"mg_claim_{sel_id}", use_container_width=True, type="primary")

        if mg_claim:
            try:
                mg_score_val = int(str(mg_score_raw).strip() or "0")
            except ValueError:
                mg_score_val = 0
            if mg_score_val <= 0:
                st.warning("게임을 끝까지 플레이한 뒤 보상받기를 눌러주세요!")
            elif st.session_state.global_cash < sel_cost:
                st.error(f"현금 부족! {format_korean_money(sel_cost)} 필요")
            elif pet.get('happiness', 100) < 10:
                st.error("행복도가 너무 낮아요! 먼저 쓰다듬거나 같이 놀아주세요 🥺")
            elif st.session_state.get(f'_mg_last_{sel_id}') == mg_score_val and st.session_state.get(f'_mg_claimed_{sel_id}'):
                st.info("이미 이 결과로 보상받았어요. 다시 플레이한 뒤 받아주세요!")
            else:
                mult      = mg_score_val / 10.0
                exp_got   = int(sel_exp * max(0.5, mult))
                jackpot   = random.random() < 0.05
                if jackpot:
                    exp_got *= 5
                    _rs = random.randint(*RUNE_SHARD_DROP['jackpot'])
                    pet['rune_shards'] = pet.get('rune_shards', 0) + _rs
                st.session_state.global_cash -= sel_cost
                atomic_deduct_cash(uid, sel_cost)
                pet['happiness']   = max(0, pet.get('happiness', 100) - 5)
                pet['last_played'] = time.time()
                pet['bond']        = pet.get('bond', 0) + 3
                pet, leveled_up, gained_exp = add_exp(pet, exp_got)
                grade = "🌟 대성공" if mult >= 0.8 else "✅ 성공" if mult >= 0.5 else "😅 아쉬운 결과"
                if jackpot: grade = "🎰 잭팟!!"
                add_journal(pet, f"🎮 {mini_game_choice} {grade} EXP+{gained_exp}")
                _add_action(pet, 'train')
                save_pet(uid, pet)
                sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} {mini_game_choice[2:]}", -sel_cost)
                st.session_state[f'_mg_last_{sel_id}']    = mg_score_val
                st.session_state[f'_mg_claimed_{sel_id}'] = True
                st.toast(f"{grade}! {pet_name_disp}이(가) EXP +{gained_exp} 획득!", icon="🎮")
                if jackpot or leveled_up:
                    st.balloons()
                if leveled_up:
                    st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()
        else:
            if st.session_state.get(f'_mg_last_{sel_id}') != (mg_score_raw or ''):
                st.session_state[f'_mg_claimed_{sel_id}'] = False

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
            remain_s  = current_exp['return_time'] - time.time()
            total_s   = z.get('duration_h',1) * 3600
            elapsed_s = total_s - remain_s
            progress  = min(100, int(elapsed_s / total_s * 100)) if total_s>0 else 0
            remain_h  = int(remain_s // 3600)
            remain_m  = int((remain_s % 3600) // 60)
            st.markdown(f"""
            <div style='background:rgba(0,229,255,0.06);border:1px solid #00E5FF44;
                        border-radius:14px;padding:20px;text-align:center;'>
                <div style='font-size:2.5rem;margin-bottom:8px;'>{z.get("icon","🗺️")}</div>
                <div style='color:#00E5FF;font-size:1.1rem;font-weight:900;'>{z.get("name","탐험")} 탐험 중!</div>
                <div style='color:#94A3B8;margin-top:8px;font-size:0.9rem;'>
                    ⏳ 귀환까지 <span style='color:#FFD600;font-weight:900;'>{remain_h}시간 {remain_m}분</span>
                </div>
                <div style='margin-top:14px;'>
                    <div style='color:#64748B;font-size:0.75rem;margin-bottom:6px;'>탐험 진행도 {progress}%</div>
                    <div style='background:rgba(255,255,255,0.08);border-radius:8px;height:10px;overflow:hidden;'>
                        <div style='background:linear-gradient(90deg,#00E5FF,#00FF88);width:{progress}%;height:100%;border-radius:8px;transition:width 0.5s;'></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            if st.button("🚫 탐험 강제 귀환 (보상 없음)", key="cancel_expedition", use_container_width=False):
                pet['expedition'] = None
                add_journal(pet, f"🚫 {z.get('name','탐험')} 탐험 강제 귀환")
                save_pet(uid, pet)
                st.toast("탐험을 취소했어요.", icon="🚫")
                st.rerun()
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
                            'pet_hp': pet.get('hp',100),
                            'monster_hp': mob['hp'],
                            'log': [f"⚔️ {pet['name']} VS {mob['name']} 배틀 시작!"],
                            'turn': 1,
                            'over': False, 'won': False,
                            'skill_cd': 0, 'poison': 0,
                        }
                        st.rerun()
        else:
            mob     = bs['monster']
            pet_hp  = bs['pet_hp']
            mob_hp  = bs['monster_hp']
            max_hp_view = 100 + pet.get('hp_bonus', 0)

            # ── v8: 자체 배틀 모션 스테이지 (직전 공격을 즉시 재생 — iframe 격리 문제 해결)
            _efx   = st.session_state.pop('battle_efx', None)
            _pd    = _efx.get('pet_dmg', 0) if _efx else 0
            _md    = _efx.get('mob_dmg', 0) if _efx else 0
            _crit  = "true" if (_efx and _efx.get('crit')) else "false"
            _skill = "true" if (_efx and _efx.get('skill')) else "false"
            _heal  = _efx.get('heal', 0) if _efx else 0
            _mob_icon = mob.get('icon', '👾')
            _pet_svg  = get_pet_sprite(pet['species'], lv)
            _nonce    = bs.get('turn', 0)
            efx_html = """
            <div id="bstage" data-n="__NONCE__" style="position:relative;height:160px;border-radius:16px;overflow:hidden;background:radial-gradient(circle at 50% 42%,#241018,#0c0610 70%);border:1px solid #FF4B4B44;display:flex;align-items:center;justify-content:space-around;box-shadow:0 0 30px rgba(255,75,75,0.12) inset;">
              <div style="position:absolute;bottom:0;left:0;right:0;height:34px;background:linear-gradient(180deg,transparent,rgba(0,0,0,0.45));"></div>
              <div id="pchar" style="width:88px;height:88px;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 12px rgba(0,255,136,0.55));z-index:2;">__PET_SVG__</div>
              <div style="font-size:1.4rem;opacity:0.35;z-index:1;">⚔️</div>
              <div id="mchar" style="font-size:3.6rem;filter:drop-shadow(0 0 12px rgba(255,75,75,0.55));z-index:2;">__MOB_ICON__</div>
              <div id="efx" style="position:absolute;inset:0;pointer-events:none;z-index:5;"></div>
            </div>
            <style>
            @keyframes bShake{0%,100%{transform:translateX(0)}15%{transform:translateX(-10px)}30%{transform:translateX(10px)}45%{transform:translateX(-7px)}60%{transform:translateX(7px)}80%{transform:translateX(-3px)}}
            @keyframes bLungeR{0%{transform:translateX(0) scale(1)}45%{transform:translateX(40px) scale(1.15) rotate(-4deg)}100%{transform:translateX(0) scale(1)}}
            @keyframes bLungeL{0%{transform:translateX(0) scale(1)}45%{transform:translateX(-40px) scale(1.15) rotate(4deg)}100%{transform:translateX(0) scale(1)}}
            @keyframes bHurt{0%,100%{transform:translateX(0) rotate(0)}20%{transform:translateX(-13px) rotate(-7deg)}50%{transform:translateX(10px) rotate(6deg)}75%{transform:translateX(-5px) rotate(-3deg)}}
            .bdn{position:absolute;font-weight:900;animation:bdF 1.15s ease-out forwards;pointer-events:none;white-space:nowrap;}
            @keyframes bdF{0%{opacity:0;transform:translateY(6px) scale(0.6)}18%{opacity:1;transform:translateY(0) scale(1.15)}100%{opacity:0;transform:translateY(-52px) scale(0.85)}}
            .bsp{position:absolute;animation:bsP 0.65s ease-out forwards;pointer-events:none;}
            @keyframes bsP{0%{opacity:1;transform:scale(0)}45%{opacity:1;transform:scale(1.6)}100%{opacity:0;transform:scale(0.3) translate(var(--sx),var(--sy))}}
            @keyframes bFlash{0%{opacity:0}30%{opacity:0.7}100%{opacity:0}}
            </style>
            <script>
            (function(){
              var PD=__PD__,MD=__MD__,CRIT=__CRIT__,SKILL=__SKILL__,HEAL=__HEAL__;
              var stage=document.getElementById('bstage'),pchar=document.getElementById('pchar'),mchar=document.getElementById('mchar'),efx=document.getElementById('efx');
              if(!stage)return;
              var W=stage.clientWidth||320;
              function dnum(x,y,txt,col,big){var d=document.createElement('div');d.className='bdn';d.textContent=txt;d.style.left=x+'px';d.style.top=y+'px';d.style.color=col;d.style.fontSize=(big?27:19)+'px';d.style.textShadow='0 0 10px '+col;efx.appendChild(d);setTimeout(function(){d.remove();},1150);}
              function sparks(x,y,n,col){var ic=['💥','⚡','✨','💫','🔥'];for(var i=0;i<n;i++){(function(k){setTimeout(function(){var s=document.createElement('div');s.className='bsp';s.textContent=ic[Math.floor(Math.random()*ic.length)];var a=(k/n)*Math.PI*2,dist=26+Math.random()*34;s.style.setProperty('--sx',Math.cos(a)*dist+'px');s.style.setProperty('--sy',Math.sin(a)*dist+'px');s.style.left=x+'px';s.style.top=y+'px';s.style.fontSize=(15+Math.random()*8)+'px';efx.appendChild(s);setTimeout(function(){s.remove();},700);},k*22);})(i);}}
              function flash(col){var f=document.createElement('div');f.style.cssText='position:absolute;inset:0;background:'+col+';animation:bFlash 0.4s ease-out forwards;pointer-events:none;';efx.appendChild(f);setTimeout(function(){f.remove();},420);}
              if(PD>0){
                pchar.style.animation='bLungeR 0.42s ease-out';
                setTimeout(function(){
                  mchar.style.animation='bHurt 0.42s ease-out';
                  sparks(W*0.74,72,SKILL?15:8,CRIT?'#FF3333':'#FFD600');
                  dnum(W*0.62,40,(SKILL?'⚡ SKILL ':(CRIT?'💥 CRIT ':''))+'-'+PD,CRIT?'#FF3333':'#FF8800',CRIT||SKILL);
                  if(SKILL||CRIT){stage.style.animation='bShake 0.5s';flash(SKILL?'rgba(255,214,0,0.3)':'rgba(255,75,75,0.25)');setTimeout(function(){stage.style.animation='';},520);}
                  if(HEAL>0)dnum(W*0.10,62,'+'+HEAL+' ❤️','#00FF88',false);
                },210);
              }
              if(MD>0){
                setTimeout(function(){
                  mchar.style.animation='bLungeL 0.42s ease-out';
                  setTimeout(function(){pchar.style.animation='bHurt 0.42s ease-out';sparks(W*0.16,72,6,'#FF4B4B');dnum(W*0.06,40,'-'+MD,'#FF6B6B',false);},150);
                },PD>0?680:0);
              }
            })();
            </script>
            """
            efx_html = (efx_html
                        .replace("__NONCE__", str(_nonce))
                        .replace("__PET_SVG__", _pet_svg)
                        .replace("__MOB_ICON__", _mob_icon)
                        .replace("__PD__", str(_pd)).replace("__MD__", str(_md))
                        .replace("__CRIT__", _crit).replace("__SKILL__", _skill)
                        .replace("__HEAL__", str(_heal)))
            components.html(efx_html, height=178)

            # ── HP 바 디스플레이
            b1, b2, b3 = st.columns([2,1,2])
            with b1:
                pct_p = max(0, int(pet_hp / max_hp_view * 100))
                st.markdown(
                    "<div class='pet-card' style='text-align:center;'>"
                    "<div style='color:#E2E8F0;font-weight:900;'>" + pet['name'] + "</div>"
                    "<div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:10px;'>"
                    "<div style='background:#00FF88;width:" + str(pct_p) + "%;height:100%;border-radius:4px;transition:width 0.4s;'></div></div>"
                    "<div style='color:#00FF88;font-size:0.85rem;margin-top:4px;'>" + str(max(0, pet_hp)) + "/" + str(max_hp_view) + " HP</div></div>",
                    unsafe_allow_html=True)
            with b2:
                st.markdown(
                    "<div style='text-align:center;padding:16px 0;'><div style='font-size:1.6rem;'>⚔️</div>"
                    "<div style='color:#FFD600;font-weight:900;margin-top:6px;'>TURN " + str(bs['turn']) + "</div></div>",
                    unsafe_allow_html=True)
            with b3:
                pct_m = max(0, int(mob_hp / mob['hp'] * 100))
                st.markdown(
                    "<div class='pet-card' style='text-align:center;'>"
                    "<div style='color:#E2E8F0;font-weight:900;'>" + mob['name'] + "</div>"
                    "<div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:10px;'>"
                    "<div style='background:#FF4B4B;width:" + str(pct_m) + "%;height:100%;border-radius:4px;transition:width 0.4s;'></div></div>"
                    "<div style='color:#FF4B4B;font-size:0.85rem;margin-top:4px;'>" + str(max(0, mob_hp)) + "/" + str(mob["hp"]) + " HP</div></div>",
                    unsafe_allow_html=True)

            # Battle log
            for log_line in bs['log'][-6:]:
                if "💥" in log_line or "크리티컬" in log_line:
                    line_color = "#FF4B4B"
                elif "⚡✨" in log_line or "필살기" in log_line:
                    line_color = "#FFD600"
                elif "🩸" in log_line:
                    line_color = "#FF8844"
                elif "🏃" in log_line or "도망" in log_line:
                    line_color = "#00E5FF"
                else:
                    line_color = "#94A3B8"
                st.markdown(f"<div style='color:{line_color};font-size:0.83rem;padding:2px 0;'>▸ {log_line}</div>", unsafe_allow_html=True)

            if bs['over']:
                if bs['won']:
                    st.success(f"🏆 승리! EXP +{mob['reward_exp']} · 💰 +{format_korean_money(mob['reward_cash'])}")
                else:
                    st.error(f"💀 패배... {pet['name']}이(가) 쓰러졌어요.")
                if st.button("🔄 배틀 종료", use_container_width=True, key="battle_end"):
                    if bs['won']:
                        max_hp_b = 100 + pet.get('hp_bonus',0)
                        pet['hp'] = max(1, min(max_hp_b, bs['pet_hp']))
                        pet, lvup, ge = add_exp(pet, mob['reward_exp'])
                        atomic_add_cash(uid, mob['reward_cash'])
                        st.session_state.global_cash += mob['reward_cash']
                        pet['battles_won']   = pet.get('battles_won',0) + 1
                        _rs = random.randint(*RUNE_SHARD_DROP['battle_win'])
                        pet['rune_shards'] = pet.get('rune_shards',0) + _rs
                        st.toast(f"🔹 룬 조각 +{_rs}", icon="🔮")
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        pet['bond'] = pet.get('bond',0) + 3
                        _add_action(pet,'battle')
                        add_journal(pet, f"⚔️ {mob['name']} 격파! EXP+{ge} 💰+{format_korean_money(mob['reward_cash'])}")
                        log_tx(uid,"펫",f"{pet['name']} 배틀승 vs {mob['name']}",mob['reward_cash'])
                        save_pet(uid, pet)
                        sync_user_data()
                    else:
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        max_hp_b = 100 + pet.get('hp_bonus',0)
                        pet['hp'] = max(1, min(max_hp_b, bs['pet_hp']))
                        add_journal(pet, f"⚔️ {mob['name']}에게 패배. HP:{pet['hp']}")
                        save_pet(uid, pet)
                    st.session_state.battle_state = None
                    st.rerun()
            else:
                sp_skill = sp.get('special_skill', {})
                b_skill_cd = bs.get('skill_cd', pet.get('skill_cooldown', 0))
                ca, cb, cc, cd = st.columns(4)
                with ca:
                    if st.button("⚔️ 일반 공격", use_container_width=True, key="atk_normal"):
                        crit    = random.random() < 0.15
                        dmg_pet = max(1, pet_stats['atk'] - mob['def'] + random.randint(-5,8))
                        if crit: dmg_pet = int(dmg_pet * 1.8)
                        dmg_mob = max(0, mob['atk'] - pet_stats['def'] + random.randint(-3,6))
                        bs['monster_hp'] -= dmg_pet; bs['pet_hp'] -= dmg_mob
                        bs['log'].append(f"{'💥 크리티컬! ' if crit else '💥 '}{pet['name']} → {mob['name']}: -{dmg_pet}HP")
                        bs['log'].append(f"🩸 {mob['name']} → {pet['name']}: -{dmg_mob}HP")
                        bs['turn'] += 1
                        if b_skill_cd > 0: bs['skill_cd'] = b_skill_cd - 1
                        st.session_state['battle_efx'] = {'pet_dmg': dmg_pet, 'mob_dmg': dmg_mob, 'crit': crit}
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cb:
                    if st.button("🔥 강공격 (-10HP)", use_container_width=True, key="atk_heavy"):
                        dmg_pet = max(1, int(pet_stats['atk']*1.8) - mob['def'] + random.randint(-4,12))
                        dmg_mob = max(0, mob['atk'] - pet_stats['def'] + random.randint(-2,5))
                        bs['pet_hp']     -= 10
                        bs['monster_hp'] -= dmg_pet; bs['pet_hp'] -= dmg_mob
                        bs['log'].append(f"💥💥 강공격! {mob['name']}: -{dmg_pet}HP (자상-10HP)")
                        bs['log'].append(f"🩸 {mob['name']}: -{dmg_mob}HP")
                        bs['turn'] += 1
                        if b_skill_cd > 0: bs['skill_cd'] = b_skill_cd - 1
                        st.session_state['battle_efx'] = {'pet_dmg': dmg_pet, 'mob_dmg': dmg_mob, 'crit': True}
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cc:
                    skill_ready = b_skill_cd <= 0
                    skill_label = f"⚡ {sp_skill.get('name','필살기')}" if skill_ready else f"⏳ CD {b_skill_cd}턴"
                    if st.button(skill_label, use_container_width=True, key="atk_skill",
                                 disabled=not skill_ready, type="primary" if skill_ready else "secondary"):
                        mult   = sp_skill.get('dmg_mult', 2.0)
                        # 고양이 필살기: 랜덤 배율
                        if pet.get('species') == 'cat':
                            mult = random.uniform(0.5, 4.0)
                        force_crit = sp_skill.get('crit', False) or (mult > 3.0)
                        dmg_pet = max(1, int(pet_stats['atk'] * mult) - mob['def'] + random.randint(0,10))
                        dmg_mob = max(0, mob['atk'] - pet_stats['def'] + random.randint(-5,3))
                        bs['monster_hp'] -= dmg_pet; bs['pet_hp'] -= dmg_mob
                        # 회복형 종족 HP 회복 (유니콘/피닉스/골렘)
                        heal = 0
                        _mhp = 100 + pet.get('hp_bonus', 0)
                        if pet.get('species') == 'unicorn': heal = 10
                        if pet.get('species') == 'phoenix': heal = 15
                        if pet.get('species') == 'golem':   heal = 30
                        if heal: bs['pet_hp'] = min(_mhp, bs['pet_hp']+heal)
                        bs['skill_cd'] = sp_skill.get('cooldown', 4)
                        pet['skill_used'] = pet.get('skill_used',0) + 1
                        heal_str = f" HP+{heal}" if heal else ""
                        bs['log'].append(f"⚡✨ {sp_skill.get('name','필살기')}!! -{dmg_pet}HP{heal_str}")
                        bs['log'].append(f"🩸 {mob['name']} → {pet['name']}: -{dmg_mob}HP")
                        bs['turn'] += 1
                        st.session_state['battle_efx'] = {'pet_dmg': dmg_pet, 'mob_dmg': dmg_mob, 'crit': True, 'skill': True, 'heal': heal}
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cd:
                    if st.button("🏃 도망가기", use_container_width=True, key="atk_flee"):
                        flee = random.random() < (0.4 + pet_stats['spd']/200)
                        if flee:
                            bs['log'].append("🏃 도망 성공!")
                            bs['over']=True; bs['won']=False
                        else:
                            dmg = max(0, mob['atk'] - pet_stats['def'] + random.randint(0,8))
                            bs['pet_hp'] -= dmg
                            bs['log'].append(f"❌ 도망 실패! 반격 -{dmg}HP")
                            st.session_state['battle_efx'] = {'pet_dmg': 0, 'mob_dmg': dmg, 'crit': False}
                            if bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        bs['turn'] += 1
                        st.rerun()

    # ── TAB 5: 아이템
    with tabs[4]:
        st.markdown('<div class="pet-tab-header">👗 악세서리 상점</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">악세서리를 장착해 능력을 강화하세요! 최대 3개.</div>', unsafe_allow_html=True)
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
                        if len(equipped)>=3: st.error("최대 3개까지 장착 가능!")
                        elif st.session_state.global_cash < acc['price']: st.error("현금 부족!")
                        else:
                            st.session_state.global_cash -= acc['price']
                            atomic_deduct_cash(uid, acc['price'])
                            equipped.append(acc_id); pet['accessories']=equipped
                            save_pet(uid,pet); sync_user_data()
                            log_tx(uid,"펫",f"{pet['name']} 악세서리: {acc['name']}",-acc['price'])
                            add_journal(pet, f"👗 {acc['name']} 장착!")
                            st.toast(f"🎉 {acc['name']} 장착!", icon="✅"); st.rerun()

    # ── TAB 6: 스탯 강화 (v7 신규)
    with tabs[6]:
        st.markdown('<div class="pet-tab-header">💪 스탯 영구 강화</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">골드로 펫의 기본 스탯을 영구적으로 강화하세요! 강화 레벨에 따라 비용 증가.</div>', unsafe_allow_html=True)
        stat_upgrades = pet.get('stat_upgrades',{})
        ug_cols = st.columns(3)
        for i_ug,(ug_id,ug) in enumerate(PET_STAT_UPGRADES.items()):
            cur_lv = stat_upgrades.get(ug_id,0)
            is_max = cur_lv >= ug['max_lv']
            cost   = ug['cost'] * (cur_lv+1)
            with ug_cols[i_ug%3]:
                st.markdown(f"""<div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2.5rem;'>{ug['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;'>{ug['name']}</div>
                    <div style='color:#00FF88;font-size:0.8rem;margin-top:4px;'>{ug['desc']}</div>
                    <div style='color:#00E5FF;font-size:0.85rem;margin-top:6px;font-weight:700;'>Lv.{cur_lv}/{ug['max_lv']}</div>
                    <div style='margin-top:6px;background:rgba(255,255,255,0.08);border-radius:4px;height:6px;overflow:hidden;'>
                        <div style='background:#00E5FF;width:{int(cur_lv/ug["max_lv"]*100)}%;height:100%;border-radius:4px;'></div>
                    </div>
                    <div style='color:{"#888" if is_max else "#FFD600"};font-weight:900;margin-top:8px;'>
                        {"✨ MAX" if is_max else format_korean_money(cost)}
                    </div>
                </div>""", unsafe_allow_html=True)
                if not is_max:
                    if st.button(f"⬆️ 강화 (Lv.{cur_lv}→{cur_lv+1})", key=f"ug_{ug_id}", use_container_width=True):
                        if st.session_state.global_cash < cost:
                            st.error("현금 부족!")
                        else:
                            st.session_state.global_cash -= cost
                            atomic_deduct_cash(uid, cost)
                            stat_upgrades[ug_id] = cur_lv+1
                            pet['stat_upgrades'] = stat_upgrades
                            # 실제 스탯 보너스 증가
                            inc = 10 if 'hp' in ug_id else 2 if 'luck' in ug_id else 5
                            pet[ug['stat']] = pet.get(ug['stat'],0) + inc
                            pet['missions_completed'] = pet.get('missions_completed',0)+1
                            add_journal(pet, f"💪 {ug['name']} Lv.{cur_lv+1} 강화!")
                            save_pet(uid, pet); sync_user_data()
                            log_tx(uid,"펫",f"{pet['name']} 스탯강화:{ug['name']}",-cost)
                            st.toast(f"💪 {ug['name']} Lv.{cur_lv+1} 강화!", icon="⬆️"); st.rerun()
                else:
                    st.button("✨ MAX 달성!", key=f"ug_{ug_id}", disabled=True, use_container_width=True)

    # ── TAB 7: 미션 (v7 신규)
    with tabs[7]:
        st.markdown('<div class="pet-tab-header">📋 일일 & 주간 미션</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">매일/매주 초기화! 미션 완료 시 현금 보상을 받으세요.</div>', unsafe_allow_html=True)
        daily_todo, weekly_todo = get_mission_progress(pet)
        today_key_m = _today_key(); week_key_m = _week_key()

        st.markdown("#### 📅 일일 미션")
        for m_d, prog, done, claimed_key in daily_todo:
            already = claimed_key in pet.get('achievements',[])
            pct = min(100, int(prog/m_d['target']*100))
            bar_c = "#00FF88" if done else "#00E5FF"
            st.markdown(f"""<div class='pet-card'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                    <div><span style='color:#E2E8F0;font-weight:700;'>{m_d['name']}</span>
                    <span style='color:#64748B;font-size:0.8rem;margin-left:8px;'>{m_d['desc']}</span></div>
                    <span style='color:#FFD600;font-weight:700;'>{format_korean_money(m_d["reward"])}</span>
                </div>
                <div style='display:flex;align-items:center;gap:10px;'>
                    <div style='flex:1;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;overflow:hidden;'>
                        <div style='background:{bar_c};width:{pct}%;height:100%;border-radius:4px;'></div>
                    </div>
                    <span style='color:{bar_c};font-size:0.8rem;font-weight:700;min-width:55px;text-align:right;'>{prog}/{m_d["target"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            if done and not already:
                if st.button(f"🎁 수령 ({format_korean_money(m_d['reward'])})", key=f"claim_dm_{m_d['id']}", use_container_width=True):
                    pet.setdefault('achievements',[]).append(claimed_key)
                    atomic_add_cash(uid, m_d['reward']); st.session_state.global_cash += m_d['reward']
                    pet['missions_completed'] = pet.get('missions_completed',0)+1
                    add_journal(pet, f"📋 일일미션 완료: {m_d['name']} +{format_korean_money(m_d['reward'])}")
                    save_pet(uid, pet); sync_user_data()
                    log_tx(uid,"펫",f"일일미션:{m_d['name']}",m_d['reward'])
                    st.toast(f"📋 {m_d['name']} 완료! +{format_korean_money(m_d['reward'])}", icon="✅"); st.rerun()
            elif already:
                st.markdown("<div style='color:#475569;font-size:0.8rem;padding:4px 0;'>✅ 오늘 수령 완료</div>", unsafe_allow_html=True)

        st.write("---")
        st.markdown("#### 📆 주간 미션")
        for m_w, prog, done, claimed_key in weekly_todo:
            already = claimed_key in pet.get('achievements',[])
            pct = min(100, int(prog/m_w['target']*100))
            bar_c = "#FFD600" if done else "#FF6699"
            st.markdown(f"""<div class='pet-card' style='border-color:rgba(255,214,0,0.2);'>
                <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                    <div><span style='color:#E2E8F0;font-weight:700;'>{m_w['name']}</span>
                    <span style='color:#64748B;font-size:0.8rem;margin-left:8px;'>{m_w['desc']}</span></div>
                    <span style='color:#FFD600;font-weight:700;'>{format_korean_money(m_w["reward"])}</span>
                </div>
                <div style='display:flex;align-items:center;gap:10px;'>
                    <div style='flex:1;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;overflow:hidden;'>
                        <div style='background:{bar_c};width:{pct}%;height:100%;border-radius:4px;'></div>
                    </div>
                    <span style='color:{bar_c};font-size:0.8rem;font-weight:700;min-width:55px;text-align:right;'>{prog}/{m_w["target"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            if done and not already:
                if st.button(f"🎁 주간 수령 ({format_korean_money(m_w['reward'])})", key=f"claim_wm_{m_w['id']}", use_container_width=True):
                    pet.setdefault('achievements',[]).append(claimed_key)
                    atomic_add_cash(uid, m_w['reward']); st.session_state.global_cash += m_w['reward']
                    pet['missions_completed'] = pet.get('missions_completed',0)+1
                    add_journal(pet, f"📋 주간미션 완료: {m_w['name']} +{format_korean_money(m_w['reward'])}")
                    save_pet(uid, pet); sync_user_data()
                    log_tx(uid,"펫",f"주간미션:{m_w['name']}",m_w['reward'])
                    st.toast(f"📋 {m_w['name']} 완료! +{format_korean_money(m_w['reward'])}", icon="✅"); st.rerun()
            elif already:
                st.markdown("<div style='color:#475569;font-size:0.8rem;padding:4px 0;'>✅ 이번 주 수령 완료</div>", unsafe_allow_html=True)

    # ── TAB 6: 특수 먹이 레시피 (NEW)
    with tabs[5]:
        st.markdown('<div class="pet-tab-header">🧪 특수 먹이 레시피</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">재료 3가지를 조합해 강력한 특수 먹이를 만드세요! 일반 먹이보다 훨씬 강력합니다.</div>', unsafe_allow_html=True)

        for r_id, recipe in SPECIAL_RECIPES.items():
            with st.expander(f"{recipe['icon']} {recipe['name']} — {recipe['desc']}", expanded=False):
                ingredient_names = []
                total_cost = 0
                for food_id, qty_needed in recipe['ingredients'].items():
                    fd = PET_FOOD.get(food_id, {})
                    ingredient_names.append(f"{fd.get('icon','?')} {fd.get('name','?')} ×{qty_needed}")
                    total_cost += fd.get('price', 0) * qty_needed

                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.04);border-radius:10px;padding:14px;margin-bottom:12px;'>
                    <div style='color:#94A3B8;font-size:0.8rem;margin-bottom:8px;'>📦 필요 재료:</div>
                    <div style='display:flex;gap:10px;flex-wrap:wrap;'>
                        {"".join(f"<span class='stat-chip' style='background:rgba(255,214,0,0.1);color:#FFD600;'>{ing}</span>" for ing in ingredient_names)}
                    </div>
                    <div style='margin-top:12px;color:#94A3B8;font-size:0.8rem;'>
                        💰 총 비용: <span style='color:#FFD600;font-weight:900;'>{format_korean_money(total_cost)}</span>
                    </div>
                    <div style='margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;'>
                        <span class='stat-chip' style='background:rgba(0,229,255,0.1);color:#00E5FF;'>⚡ EXP +{recipe["exp"]}</span>
                        <span class='stat-chip' style='background:rgba(255,100,150,0.1);color:#FF6699;'>😊 행복 +{recipe["happiness"]}</span>
                        <span class='stat-chip' style='background:rgba(0,255,136,0.1);color:#00FF88;'>🍖 허기 +{recipe["hunger_restore"]}</span>
                    </div>
                    <div style='margin-top:8px;color:#DD00FF;font-size:0.85rem;font-weight:700;'>✨ 특수 효과: {recipe["special"]}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🧪 {recipe['name']} 제조!", key=f"recipe_{r_id}", use_container_width=True):
                    if st.session_state.global_cash < total_cost:
                        st.error(f"재료 비용 부족! {format_korean_money(total_cost)} 필요")
                    else:
                        st.session_state.global_cash -= total_cost
                        atomic_deduct_cash(uid, total_cost)
                        pet['hunger']    = min(100, pet.get('hunger', 100)    + recipe['hunger_restore'])
                        pet['happiness'] = min(100, pet.get('happiness', 100) + recipe['happiness'])
                        pet['hp']        = min(100, pet.get('hp', 100)        + 20)
                        pet['last_fed']  = time.time()
                        pet['total_fed'] = pet.get('total_fed', 0) + 1
                        pet['bond']      = pet.get('bond', 0) + recipe.get('bond_bonus', 10)
                        pet['recipes_made'] = pet.get('recipes_made', 0) + 1
                        pet, leveled_up, gained_exp = add_exp(pet, recipe['exp'])
                        add_journal(pet, f"🧪 {recipe['name']} 제조! EXP+{gained_exp}")
                        save_pet(uid, pet)
                        sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} 레시피: {recipe['name']}", -total_cost)
                        st.session_state['feed_animation'] = True
                        st.toast(f"✨ {recipe['name']} 제조 성공! EXP +{gained_exp}", icon="🧪")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

    # ── TAB 7: 스킬
    with tabs[8]:
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

    # ── TAB 8: 업적
    with tabs[9]:
        st.markdown('<div class="pet-tab-header">🏆 펫 업적</div>', unsafe_allow_html=True)
        earned_ids = pet.get('achievements',[])
        earned_count = len(earned_ids)
        total_count  = len(PET_ACHIEVEMENTS)
        total_reward = sum(a.get('reward',0) for a in PET_ACHIEVEMENTS if a['id'] in earned_ids)
        st.markdown(f"""
        <div style='background:rgba(255,214,0,0.06);border:1px solid #FFD60033;
                    border-radius:12px;padding:14px;margin-bottom:16px;text-align:center;'>
            <div style='color:#FFD600;font-size:1.4rem;font-weight:900;'>{earned_count}/{total_count}</div>
            <div style='color:#94A3B8;font-size:0.85rem;margin-top:4px;'>업적 달성 · 총 보상 {format_korean_money(total_reward)} 수령</div>
            <div style='background:rgba(255,255,255,0.08);border-radius:4px;height:6px;margin-top:10px;overflow:hidden;'>
                <div style='background:#FFD600;width:{int(earned_count/max(total_count,1)*100)}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ach_cols = st.columns(3)
        for i, ach in enumerate(PET_ACHIEVEMENTS):
            has = ach['id'] in earned_ids
            reward = ach.get('reward', 0)
            with ach_cols[i%3]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;
                    {"border-color:#FFD600;background:rgba(255,214,0,0.06);" if has else "opacity:0.45;"}'>
                    <div style='font-size:2rem;'>{ach['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;font-size:0.9rem;'>{ach['name']}</div>
                    <div style='color:#64748B;font-size:0.75rem;margin-top:4px;'>{ach['desc']}</div>
                    <div style='color:#FFD600;font-size:0.72rem;margin-top:4px;font-weight:700;'>💰 보상 {format_korean_money(reward)}</div>
                    <div style='color:{"#FFD600" if has else "#475569"};font-size:0.75rem;margin-top:4px;font-weight:700;'>
                        {"✅ 달성!" if has else "🔒 미달성"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 9: 포토카드 (NEW)
    with tabs[10]:
        st.markdown('<div class="pet-tab-header">📸 펫 포토카드</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">내 펫의 현황을 예쁜 프로필 카드로 확인하세요! 스크린샷으로 공유하세요 📷</div>', unsafe_allow_html=True)

        _stage_nm = {"egg":"알","baby":"새끼","adult":"성체","legend":"전설"}.get(stage,"성체")
        _svg_big  = get_svg_sprite(pet['species'], stage)
        _ach_cnt  = len(pet.get('achievements', []))
        _bday     = pet.get('birth_date','?')
        _days     = 0
        if _bday and _bday != '?':
            try:
                from datetime import datetime as _dt
                _days = (_dt.now() - _dt.strptime(_bday, "%Y-%m-%d")).days
            except: pass
        _sn, _si = get_season()
        _wn      = get_weather()
        _wi      = WEATHER_ICONS.get(_wn,"☀️")

        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{sp['rarity_color']}22 0%,#0a0f1e 50%,{sp['rarity_color']}11 100%);
            border:2px solid {sp['rarity_color']};border-radius:24px;padding:28px 24px;
            max-width:440px;margin:0 auto;box-shadow:0 0 40px {sp['rarity_color']}44;
            font-family:'Courier New',monospace;position:relative;overflow:hidden;">
            <div style="position:absolute;top:-10px;right:-10px;font-size:110px;opacity:0.04;user-select:none;">{sp.get('legend','⭐')}</div>
            <div style="text-align:center;margin-bottom:20px;">
                <div style="color:{sp['rarity_color']};font-size:0.8rem;font-weight:900;letter-spacing:3px;margin-bottom:6px;">★ {sp['rarity'].upper()} ★</div>
                <div style="font-size:1.7rem;font-weight:900;color:#E2E8F0;letter-spacing:2px;">{pet.get('name','펫')}</div>
                <div style="color:#64748B;font-size:0.8rem;margin-top:4px;">{sp['name']} · {_stage_nm} 단계 · {pet.get('personality','?')}</div>
            </div>
            <div style="width:140px;height:140px;margin:0 auto 20px;display:flex;align-items:center;justify-content:center;
                background:radial-gradient(circle,{sp['rarity_color']}22 0%,transparent 70%);border-radius:50%;
                filter:drop-shadow(0 0 18px {sp['rarity_color']}88);">{_svg_big}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;">
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">⚡ 레벨</div><div style="color:#FFD600;font-weight:900;font-size:1.2rem;">Lv.{lv}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">💕 유대감</div><div style="color:#FF6699;font-weight:900;font-size:1rem;">{get_bond_title(bond_lv)}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">⚔️ ATK</div><div style="color:#FF4B4B;font-weight:900;font-size:1.2rem;">{get_pet_stats(pet)["atk"]}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">🛡️ DEF</div><div style="color:#00E5FF;font-weight:900;font-size:1.2rem;">{get_pet_stats(pet)["def"]}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">🏆 업적</div><div style="color:#FFD600;font-weight:900;font-size:1.2rem;">{_ach_cnt}/{len(PET_ACHIEVEMENTS)}</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">⚔️ 배틀</div><div style="color:#FF4B4B;font-weight:900;font-size:1.1rem;">{pet.get('battles_won',0)}승/{pet.get('battles_total',0)}전</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">🗺️ 탐험</div><div style="color:#00E5FF;font-weight:900;font-size:1.2rem;">{pet.get('expeditions',0)}회</div>
                </div>
                <div style="background:rgba(255,255,255,0.05);border-radius:10px;padding:10px;text-align:center;">
                    <div style="color:#64748B;font-size:0.7rem;">🌟 함께한 날</div><div style="color:#00FF88;font-weight:900;font-size:1.2rem;">{_days}일</div>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.03);border-radius:10px;padding:12px;text-align:center;margin-bottom:14px;">
                <span style="color:{mood_data['color']};font-size:1.2rem;">{mood_data['emoji']}</span>
                <span style="color:{mood_data['color']};font-weight:700;"> {mood_name}</span>
                <span style="color:#475569;margin:0 10px;">·</span>
                <span style="color:#94A3B8;">{_si}{_sn} {_wi}{_wn}</span>
            </div>
            <div style="background:{sp['rarity_color']}18;border:1px solid {sp['rarity_color']}44;border-radius:10px;padding:10px;text-align:center;margin-bottom:12px;">
                <div style="color:{sp['rarity_color']};font-size:0.75rem;font-weight:900;margin-bottom:4px;">🎯 종족 고유 능력</div>
                <div style="color:#E2E8F0;font-size:0.82rem;">{sp['ability']}</div>
            </div>
            <div style="text-align:center;color:#475569;font-size:0.72rem;">🎂 탄생일: {_bday} · {_si}{_sn}에 태어난 {sp['name']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.info("💡 카드를 스크린샷 찍어 친구들에게 공유해보세요!")

    # ── TAB 10: 일지
    with tabs[11]:
        st.markdown('<div class="pet-tab-header">📖 펫 일지</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">펫과의 활동 기록이 자동으로 남습니다.</div>', unsafe_allow_html=True)
        journal = pet.get('journal', [])

        # 카테고리 필터
        filter_opt = st.selectbox("🔍 필터", ["전체","🎉 레벨업","🍖 먹이","⚔️ 배틀","🗺️ 탐험","🧪 레시피","💪 훈련","🤗 쓰다듬기"], key="journal_filter")
        filter_kw  = {"전체":None,"🎉 레벨업":"레벨업","🍖 먹이":"먹","⚔️ 배틀":"배틀","🗺️ 탐험":"탐험","🧪 레시피":"레시피","💪 훈련":"훈련","🤗 쓰다듬기":"쓰다듬"}.get(filter_opt)
        filtered = [e for e in journal if filter_kw is None or filter_kw in e]

        if not filtered:
            st.markdown("<div style='text-align:center;color:#475569;padding:30px;'>해당 카테고리 기록이 없어요!</div>", unsafe_allow_html=True)
        else:
            for entry in filtered[:30]:
                ic = "#FFD600" if "레벨업" in entry else "#FF4B4B" if "배틀" in entry else "#00E5FF" if "탐험" in entry else "#DD00FF" if "레시피" in entry else "#FF6699" if "쓰다듬" in entry else "#00FF88"
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.03);border-left:2px solid {ic}55;
                            padding:8px 14px;margin-bottom:6px;border-radius:0 8px 8px 0;
                            color:#B0BAC8;font-size:0.84rem;'>
                    {entry}
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 11: 정보/분양
    with tabs[12]:
        st.markdown('<div class="pet-tab-header">📊 펫 상세 정보</div>', unsafe_allow_html=True)
        equipped = pet.get('accessories',[])
        pet_skills_list = pet.get('skills',[])
        info_rows = [
            ("🐾 종류",      sp['name']),
            ("📛 이름",      pet['name']),
            ("🌟 성격",      pet.get('personality','?')),
            ("🎂 탄생일",    pet.get('birth_date','?')),
            ("⚡ 레벨/단계", f"Lv.{lv:,}/{MAX_LEVEL:,} ({get_evo(lv)['name']})"),
            ("🧬 진화 단계", f"{get_evo(lv)['title']} (Tier {get_evo_tier(lv)})"),
            ("♻️ 환생", f"{get_rebirth_title(pet.get('rebirth',0))} ({pet.get('rebirth',0)}회)"),
            ("💠 환생포인트", f"{pet.get('prestige_points',0)}"),
            ("🔮 룬 조각", f"{pet.get('rune_shards',0):,}개"),
            ("🏔️ 최고 레벨", f"Lv.{pet.get('max_level_reached',lv):,}"),
            ("🧬 총 EXP",    f"{pet.get('total_exp_gained',0):,}"),
            ("🍖 총 먹인 횟수", f"{pet.get('total_fed',0):,}회"),
            ("🧪 레시피 제조", f"{pet.get('recipes_made',0):,}회"),
            ("💕 유대감",    get_bond_title(bond_lv)),
            ("🗺️ 탐험 횟수", f"{pet.get('expeditions',0)}회"),
            ("⚔️ 배틀 전적", f"{pet.get('battles_won',0)}승 / {pet.get('battles_total',0)}전"),
            ("💰 패시브 수입", format_korean_money(passive)+"/h" if passive>0 else "미해금 (Lv.15~)"),
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

    # ── TAB 12: 💬 펫과 대화 (Claude AI)
    with tabs[13]:
        st.markdown('<div class="pet-tab-header">💬 펫과 대화하기</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pet-sub">{pet["name"]}이(가) 직접 대답해요! AI가 종족·기분·레벨에 맞게 응답합니다 🤖</div>', unsafe_allow_html=True)

        # 채팅 이력 초기화
        if 'pet_chat_history' not in st.session_state:
            st.session_state.pet_chat_history = []

        mood_name_c, mood_data_c = get_mood(pet)
        season_c, _ = get_season()
        weather_c = get_weather()

        # 시스템 프롬프트 생성
        sp_data = PET_SPECIES.get(pet.get('species','cat'), {})
        system_prompt = f"""너는 '{pet.get('name','펫')}'이라는 {sp_data.get('name','펫')}야. 
성격: {pet.get('personality','장난꾸러기')}. 레벨: {lv}. 기분: {mood_name_c}({mood_data_c['desc']}).
HP: {hp}/100, 허기: {pet.get('hunger',100)}/100, 행복: {happy}/100.
지금 계절은 {season_c}, 날씨는 {weather_c}야.
유대감 단계: {get_bond_title(bond_lv)}. 탄생일: {pet.get('birth_date','?')}.

반드시 지켜야 할 규칙:
- 펫의 입장에서 1인칭으로 짧고 귀엽게 대답해
- 종족 특성({sp_data.get('ability','')})과 성격을 반영해
- 기분이 나쁘면(배고픔/아픔) 그 상태를 티내
- 한국어로만 대답하고, 1~3문장 이내로
- 이모티콘을 적절히 사용해 (너무 많이는 ❌)
- 절대 AI라고 밝히지 말고, 진짜 펫처럼 행동해"""

        # 채팅 UI
        chat_container = st.container()
        with chat_container:
            if not st.session_state.pet_chat_history:
                greeting_map = {
                    "신남": f"안녕! 나 오늘 기분 최고야! 같이 뭐 할까? 🤩",
                    "행복": f"어, 왔어? 잘됐다~ 심심하던 참이야 😊",
                    "배고픔": f"...배고파. 밥 좀... 😮",
                    "아픔": f"몸이 좀 안 좋아... 포션 줘... 🤒",
                    "피곤": f"...졸려. 잠깐 쉬고 싶어 😴",
                    "슬픔": f"왜 이제 왔어... 보고싶었는데 😢",
                    "보통": f"응, 왔어? 뭐 물어보려고? 😐",
                }
                greeting = greeting_map.get(mood_name_c, f"안녕! 나야, {pet['name']}!")
                st.markdown(f"""
                <div style='display:flex;gap:12px;margin-bottom:16px;align-items:flex-start;'>
                    <div style='width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.08);
                                display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1.2rem;
                                border:1px solid {sp["rarity_color"]}44;'>
                        {sp.get("baby","🐾")}
                    </div>
                    <div style='background:rgba(255,255,255,0.05);border:1px solid {sp["rarity_color"]}33;
                                border-radius:0 14px 14px 14px;padding:10px 14px;max-width:80%;'>
                        <div style='color:#E2E8F0;font-size:0.9rem;'>{greeting}</div>
                        <div style='color:#475569;font-size:0.7rem;margin-top:4px;'>{pet["name"]} · {mood_data_c["emoji"]} {mood_name_c}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            for msg in st.session_state.pet_chat_history[-20:]:
                if msg['role'] == 'user':
                    st.markdown(f"""
                    <div style='display:flex;justify-content:flex-end;margin-bottom:12px;'>
                        <div style='background:rgba(0,229,255,0.1);border:1px solid rgba(0,229,255,0.3);
                                    border-radius:14px 0 14px 14px;padding:10px 14px;max-width:80%;'>
                            <div style='color:#E2E8F0;font-size:0.9rem;'>{msg["content"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='display:flex;gap:12px;margin-bottom:12px;align-items:flex-start;'>
                        <div style='width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.08);
                                    display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1.2rem;
                                    border:1px solid {sp["rarity_color"]}44;'>
                            {sp.get("baby","🐾")}
                        </div>
                        <div style='background:rgba(255,255,255,0.05);border:1px solid {sp["rarity_color"]}33;
                                    border-radius:0 14px 14px 14px;padding:10px 14px;max-width:80%;'>
                            <div style='color:#E2E8F0;font-size:0.9rem;'>{msg["content"]}</div>
                            <div style='color:#475569;font-size:0.7rem;margin-top:4px;'>{pet["name"]} · {mood_data_c["emoji"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # 입력
        with st.form("pet_chat_form", clear_on_submit=True):
            col_inp, col_btn = st.columns([5,1])
            with col_inp:
                user_msg = st.text_input("메시지 입력...", placeholder=f"{pet['name']}에게 말 걸기!", label_visibility="collapsed")
            with col_btn:
                sent = st.form_submit_button("전송", use_container_width=True, type="primary")

        if sent and user_msg.strip():
            # ── Gemini API 호출 (project_a.py와 동일 방식)
            import requests as _req
            GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
            st.session_state.pet_chat_history.append({"role":"user","content":user_msg.strip()})

            pet_reply = None
            if GOOGLE_API_KEY:
                # 대화 이력 → Gemini 형식으로 변환
                gemini_contents = []
                for m in st.session_state.pet_chat_history[-10:]:
                    role = "user" if m["role"] == "user" else "model"
                    gemini_contents.append({"role": role, "parts": [{"text": m["content"]}]})

                # 시스템 프롬프트를 첫 user 메시지 앞에 삽입
                full_contents = [
                    {"role": "user",  "parts": [{"text": system_prompt + "\n\n이 설정을 이해했으면 '네!'라고만 답해줘."}]},
                    {"role": "model", "parts": [{"text": "네!"}]},
                ] + gemini_contents

                payload = {
                    "contents": full_contents,
                    "generationConfig": {"temperature": 0.85, "maxOutputTokens": 300},
                }
                models = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-2.0-flash-lite"]
                for model in models:
                    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={GOOGLE_API_KEY}"
                    try:
                        res = _req.post(url, json=payload, timeout=15)
                        if res.status_code == 200:
                            data = res.json()
                            pet_reply = data['candidates'][0]['content']['parts'][0]['text']
                            break
                        elif res.status_code in [429, 503]:
                            continue
                    except Exception:
                        continue

            if not pet_reply:
                # API 키 없거나 실패 시 fallback
                fallbacks = {
                    "신남":   [f"그거 진짜 좋은 말이야! 나도 그렇게 생각해 🤩", f"맞아맞아! 완전 공감~ 더 신나는 것 하자!"],
                    "행복":   [f"응, 기분 좋아서 뭐든 다 좋아 보여 😊", f"좋은 얘기 해줘서 고마워~"],
                    "배고픔": [f"...밥 줘. 배고파서 집중이 안 돼 😮", f"밥 먼저... 그다음에 얘기하자..."],
                    "아픔":   [f"몸이 안 좋아서 말하기 힘들어... 포션 좀... 🤒"],
                    "피곤":   [f"...졸려. 나중에 얘기해... 😴"],
                    "슬픔":   [f"그래... 고마워. 같이 있어줘서 😢"],
                    "보통":   [f"흠, 그렇구나~", f"나도 그런 생각 해봤어.", f"재밌는 얘기네!"],
                }
                import random as _r
                pet_reply = _r.choice(fallbacks.get(mood_name_c, fallbacks["보통"]))

            st.session_state.pet_chat_history.append({"role":"assistant","content":pet_reply})
            # 대화하면 행복도 살짝 오름
            pet['happiness'] = min(100, pet.get('happiness',100) + 3)
            pet['bond']      = pet.get('bond',0) + 1
            _add_action(pet,'chat')
            add_journal(pet, f"💬 '{user_msg[:20]}...' 대화!")
            save_pet(uid, pet)
            st.rerun()

        # 대화 초기화 버튼
        if st.session_state.pet_chat_history:
            if st.button("🗑️ 대화 초기화", key="clear_chat"):
                st.session_state.pet_chat_history = []
                st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # 🧬 TAB 15: 진화 (진화 트리 + 도감)
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[14]:
        st.markdown('<div class="pet-tab-header">🧬 진화 트리</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">1000레벨마다 진화하여 외형과 능력이 강해집니다! 만렙은 5000 (창세신 👑)</div>', unsafe_allow_html=True)

        cur_tier = get_evo_tier(lv)
        next_evo = None
        for e in EVOLUTION_STAGES:
            if e['tier'] == cur_tier + 1:
                next_evo = e; break

        # 현재 진화 상태 카드
        _evo = get_evo(lv)
        st.markdown(
            "<div class='pet-card' style='text-align:center;border-color:" + _evo['aura'] + "55;'>"
            "<div style='width:120px;height:120px;margin:0 auto;display:flex;align-items:center;justify-content:center;filter:drop-shadow(0 0 18px " + _evo['aura'] + ");'>" + get_pet_sprite(pet['species'], lv) + "</div>"
            "<div style='color:" + _evo['aura'] + ";font-weight:900;font-size:1.3rem;margin-top:10px;'>" + _evo['title'] + "</div>"
            "<div style='color:#E2E8F0;font-size:0.9rem;margin-top:4px;'>" + pet['name'] + " · " + _evo['name'] + " 단계 (Tier " + str(cur_tier) + ")</div>"
            "<div style='color:#64748B;font-size:0.78rem;margin-top:6px;'>진화 배수: 전 스탯 ×" + f"{1 + cur_tier*0.25:.2f}" + "</div>"
            "</div>", unsafe_allow_html=True)

        # 다음 진화까지
        if lv >= MAX_LEVEL:
            st.success("👑 최종 진화 완료! 창세신 단계에 도달했습니다. 이제 환생(♻️)으로 더 강해지세요!")
        elif next_evo:
            need_lv = next_evo['min']
            remain = need_lv - lv
            prog = max(0, min(100, int((lv - _evo['min']) / (need_lv - _evo['min']) * 100))) if need_lv > _evo['min'] else 0
            st.markdown(
                "<div class='pet-card'><div style='display:flex;justify-content:space-between;margin-bottom:6px;'>"
                "<span style='color:#E2E8F0;font-weight:700;'>다음 진화: " + next_evo['title'] + " (" + next_evo['name'] + ")</span>"
                "<span style='color:" + next_evo['aura'] + ";font-weight:900;'>Lv." + f"{need_lv:,}" + "</span></div>"
                "<div style='color:#64748B;font-size:0.8rem;margin-bottom:6px;'>앞으로 " + f"{remain:,}" + "레벨 남음</div>"
                "<div style='background:rgba(255,255,255,0.08);border-radius:5px;height:9px;overflow:hidden;'>"
                "<div style='background:linear-gradient(90deg," + _evo['aura'] + "," + next_evo['aura'] + ");width:" + str(prog) + "%;height:100%;border-radius:5px;'></div></div>"
                "<div style='text-align:right;color:#94A3B8;font-size:0.72rem;margin-top:3px;'>" + str(prog) + "%</div></div>",
                unsafe_allow_html=True)

        # 진화 도감 (전 단계 미리보기)
        st.markdown("#### 📖 진화 도감")
        st.markdown('<div class="pet-sub">우리 펫이 거쳐갈 / 거쳐온 모든 단계</div>', unsafe_allow_html=True)
        seen = pet.get('evolutions_seen', [])
        evo_cols = st.columns(len(EVOLUTION_STAGES))
        for i, e in enumerate(EVOLUTION_STAGES):
            with evo_cols[i]:
                reached = lv >= e['min']
                unlocked = e['tier'] in seen or reached
                op = "1" if reached else ("0.65" if unlocked else "0.3")
                bdr = "border:2px solid " + e['aura'] + ";" if e['tier'] == cur_tier else "border:1px solid rgba(255,255,255,0.1);"
                preview = get_svg_sprite(pet['species'], e['min'] if reached else (e['min'] if unlocked else e['min']))
                badge = "✅" if reached else ("🔓" if unlocked else "🔒")
                st.markdown(
                    "<div style='text-align:center;padding:10px 4px;border-radius:12px;" + bdr + "opacity:" + op + ";'>"
                    "<div style='width:54px;height:54px;margin:0 auto;display:flex;align-items:center;justify-content:center;'>" + (preview if unlocked else "<div style='font-size:2rem;'>❔</div>") + "</div>"
                    "<div style='color:" + e['aura'] + ";font-size:0.7rem;font-weight:900;margin-top:5px;'>" + e['name'] + "</div>"
                    "<div style='color:#64748B;font-size:0.62rem;'>Lv." + (f"{e['min']:,}" if e['min'] > 0 else "0") + "</div>"
                    "<div style='font-size:0.7rem;margin-top:2px;'>" + badge + "</div></div>",
                    unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # ♻️ TAB 16: 환생 (만렙 후 리셋 + 영구 보너스)
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[15]:
        st.markdown('<div class="pet-tab-header">♻️ 환생 (Rebirth)</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">만렙(5000) 도달 시 환생 가능! 레벨은 1로 리셋되지만 영구 보너스를 얻습니다.</div>', unsafe_allow_html=True)

        rb = pet.get('rebirth', 0)
        pp = pet.get('prestige_points', 0)
        st.markdown(
            "<div class='pet-card' style='text-align:center;border-color:#DD00FF44;'>"
            "<div style='font-size:2.5rem;'>♻️</div>"
            "<div style='color:#DD00FF;font-weight:900;font-size:1.2rem;margin-top:6px;'>" + get_rebirth_title(rb) + "</div>"
            "<div style='color:#E2E8F0;font-size:0.85rem;margin-top:6px;'>환생 횟수: " + str(rb) + "회 · 보유 환생포인트: 💠 " + str(pp) + "</div>"
            "<div style='margin-top:10px;'>"
            "<span class='stat-chip' style='background:rgba(0,229,255,0.12);color:#00E5FF;'>EXP +" + str(min(rb*10,200)) + "%</span>"
            "<span class='stat-chip' style='background:rgba(255,75,75,0.12);color:#FF4B4B;'>전 스탯 +" + str(rb*15) + "%</span>"
            "</div></div>", unsafe_allow_html=True)

        if lv >= REBIRTH_REQ_LEVEL:
            st.success("🌟 환생 조건 충족! 환생하면 레벨이 1로 돌아가지만 영구 보너스 + 환생포인트 💠를 받습니다.")
            gain_pp = 1 + rb  # 환생할수록 더 많은 포인트
            st.warning(f"환생 시 받는 환생포인트: 💠 {gain_pp}  ·  새 칭호: {get_rebirth_title(rb+1)}")
            confirm_rb = st.checkbox("환생합니다 (레벨 1로 리셋, 영구 보너스 획득)", key="rebirth_confirm")
            if st.button("♻️ 환생하기!", use_container_width=True, disabled=not confirm_rb, type="primary"):
                pet['rebirth'] = rb + 1
                pet['total_rebirths'] = pet.get('total_rebirths', 0) + 1
                pet['prestige_points'] = pp + gain_pp
                pet['level'] = 1
                pet['exp'] = 0
                pet['evo_tier'] = 0
                pet['hp'] = 100 + pet.get('hp_bonus', 0)
                add_journal(pet, f"♻️✨ 환생! {get_rebirth_title(rb+1)} 각성! (환생 {rb+1}회)")
                save_pet(uid, pet); sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 환생 {rb+1}회", 0)
                st.balloons()
                st.toast(f"♻️ 환생 완료! {get_rebirth_title(rb+1)} · 💠+{gain_pp}", icon="🌟")
                st.rerun()
        else:
            remain = REBIRTH_REQ_LEVEL - lv
            st.info(f"⏳ 환생까지 {remain:,}레벨 남았어요. (현재 Lv.{lv:,} / {REBIRTH_REQ_LEVEL:,})")

        # 프레스티지 상점
        st.write("---")
        st.markdown("#### 🏅 프레스티지 상점")
        st.markdown('<div class="pet-sub">환생포인트(💠)로만 구매하는 영구 강화입니다.</div>', unsafe_allow_html=True)
        upg = pet.setdefault('stat_upgrades', {})
        psh_cols = st.columns(2)
        for i, (p_id, p) in enumerate(PRESTIGE_SHOP.items()):
            with psh_cols[i % 2]:
                cur = pet.get('prestige_owned', {}).get(p_id, 0)
                maxed = cur >= p['max']
                st.markdown(
                    "<div class='pet-card'><div style='display:flex;align-items:center;gap:12px;'>"
                    "<div style='font-size:2rem;'>" + p['icon'] + "</div><div style='flex:1;'>"
                    "<div style='color:#E2E8F0;font-weight:900;'>" + p['name'] + " <span style='color:#64748B;font-size:0.72rem;'>(" + str(cur) + "/" + str(p['max']) + ")</span></div>"
                    "<div style='color:#94A3B8;font-size:0.76rem;'>" + p['desc'] + "</div>"
                    "<div style='color:#DD00FF;font-size:0.76rem;font-weight:700;margin-top:3px;'>💠 " + str(p['cost']) + "</div>"
                    "</div></div></div>", unsafe_allow_html=True)
                if maxed:
                    st.button("⭐ MAX", key=f"psh_{p_id}", use_container_width=True, disabled=True)
                else:
                    if st.button(f"구매 (💠{p['cost']})", key=f"psh_{p_id}", use_container_width=True):
                        if pet.get('prestige_points', 0) < p['cost']:
                            st.toast("환생포인트 부족!", icon="💠")
                        else:
                            pet['prestige_points'] -= p['cost']
                            po = pet.setdefault('prestige_owned', {})
                            po[p_id] = po.get(p_id, 0) + 1
                            add_journal(pet, f"🏅 프레스티지: {p['name']} 구매!")
                            save_pet(uid, pet); sync_user_data()
                            st.toast(f"🏅 {p['name']} 구매! (Lv.{po[p_id]})", icon="💠")
                            st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # 🔮 TAB 17: 룬 (룬 조각으로 배틀 스탯 강화)
    # ══════════════════════════════════════════════════════════════════════════
    with tabs[16]:
        st.markdown('<div class="pet-tab-header">🔮 룬 강화</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">룬 조각(🔹)으로 룬을 강화해 배틀 능력치를 직접 올리세요! 조각은 배틀 승리·탐험·잭팟에서 획득합니다.</div>', unsafe_allow_html=True)

        shards = pet.get('rune_shards', 0)
        st.markdown(
            "<div class='pet-card' style='text-align:center;'>"
            "<span style='font-size:1.4rem;'>🔹</span> <span style='color:#00E5FF;font-weight:900;font-size:1.2rem;'>" + f"{shards:,}" + "</span>"
            "<span style='color:#64748B;font-size:0.85rem;'> 개의 룬 조각 보유</span></div>",
            unsafe_allow_html=True)

        runes = pet.setdefault('runes', {})
        rune_cols = st.columns(2)
        for i, (r_id, r) in enumerate(PET_RUNES.items()):
            with rune_cols[i % 2]:
                cur = runes.get(r_id, 0)
                maxed = cur >= r['max_lv']
                cost = r['shard_cost'] * (cur + 1)  # 강화할수록 비용 증가
                cur_bonus = r['per_lv'] * cur
                st.markdown(
                    "<div class='pet-card'><div style='display:flex;align-items:center;gap:12px;'>"
                    "<div style='font-size:2.2rem;'>" + r['icon'] + "</div><div style='flex:1;'>"
                    "<div style='color:#E2E8F0;font-weight:900;'>" + r['name'] + " <span style='color:#64748B;font-size:0.72rem;'>(Lv." + str(cur) + "/" + str(r['max_lv']) + ")</span></div>"
                    "<div style='color:#94A3B8;font-size:0.76rem;'>" + r['desc'] + "</div>"
                    "<div style='color:#00FF88;font-size:0.74rem;margin-top:3px;'>현재 보너스: +" + str(cur_bonus) + " " + r['stat'].upper() + "</div>"
                    + ("" if maxed else "<div style='color:#00E5FF;font-size:0.74rem;'>강화 비용: 🔹 " + str(cost) + "</div>")
                    + "</div></div></div>", unsafe_allow_html=True)
                if maxed:
                    st.button("⭐ MAX", key=f"rune_{r_id}", use_container_width=True, disabled=True)
                else:
                    if st.button(f"🔮 강화 (🔹{cost})", key=f"rune_{r_id}", use_container_width=True):
                        if pet.get('rune_shards', 0) < cost:
                            st.toast("룬 조각 부족! 배틀·탐험으로 모으세요 🔹", icon="🔹")
                        else:
                            pet['rune_shards'] -= cost
                            runes[r_id] = cur + 1
                            add_journal(pet, f"🔮 {r['name']} 강화! (Lv.{cur+1})")
                            save_pet(uid, pet); sync_user_data()
                            st.toast(f"🔮 {r['name']} Lv.{cur+1}!", icon="✨")
                            if (cur+1) % 10 == 0: st.balloons()
                            st.rerun()

        st.write("---")
        st.caption("💡 룬 조각은 배틀 승리(1~3개), 탐험 완료(2~5개), 훈련 잭팟(3~8개)에서 획득합니다.")
