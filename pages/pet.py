# pages/pet.py — CUTE ULTIMATE EDITION v5.0 🐾
# 완전 새로운 귀여운 SVG 펫 캐릭터 + 풍부한 인터랙션 시스템
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
    "dragon":  {"name":"드래곤",    "rarity":"전설","rarity_color":"#FF6B35",
                "desc":"귀엽지만 강력한 아기 화염룡! 성장할수록 불꽃이 커져요.",
                "price":500_000_000,"ability":"화염 브레스 — 배틀 시 추가 화염 데미지",
                "bg_color":"#1a0800","accent":"#FF6B35","particle":["🔥","✨","💛","⚡"]},
    "wolf":    {"name":"황금 늑대", "rarity":"희귀","rarity_color":"#FFD600",
                "desc":"황금빛 모피를 가진 신비로운 아기 늑대. 귀가 쫑긋!",
                "price":100_000_000,"ability":"황금 발톱 — 광산 수입 +15%",
                "bg_color":"#0d0d00","accent":"#FFD600","particle":["⭐","✨","🌕","💛"]},
    "penguin": {"name":"황제 펭귄", "rarity":"고급","rarity_color":"#00E5FF",
                "desc":"뒤뚱뒤뚱 귀여운 황제 펭귄! 배가 통통해요.",
                "price":50_000_000,"ability":"빙하 방패 — 배틀 방어력 +20%",
                "bg_color":"#001520","accent":"#00E5FF","particle":["❄️","⛄","💎","🌊"]},
    "cat":     {"name":"럭키 고양이","rarity":"일반","rarity_color":"#FF9FC1",
                "desc":"행운을 부르는 복실복실한 고양이. 발바닥이 분홍!",
                "price":10_000_000,"ability":"럭키 포 — 퀘스트 보상 +10%",
                "bg_color":"#0f0008","accent":"#FF9FC1","particle":["✨","💕","🌸","🐾"]},
    "unicorn": {"name":"유니콘",    "rarity":"영웅","rarity_color":"#CC44FF",
                "desc":"무지개빛 갈기의 유니콘! 이마에서 빛이 나요.",
                "price":200_000_000,"ability":"무지개 마법 — 코인 수익 +12%",
                "bg_color":"#0d0020","accent":"#CC44FF","particle":["🌈","💜","✨","💫"]},
    "phoenix": {"name":"불사조",    "rarity":"영웅","rarity_color":"#FF9500",
                "desc":"아기 불사조! 머리의 불꽃이 활활 타오릅니다.",
                "price":300_000_000,"ability":"불사 재생 — HP 자동 회복 2배",
                "bg_color":"#150800","accent":"#FF9500","particle":["🔥","✨","🌟","☀️"]},
    "slime":   {"name":"황금 슬라임","rarity":"고급","rarity_color":"#FFE100",
                "desc":"젤리처럼 말랑말랑한 황금 슬라임! 눈이 초롱초롱.",
                "price":30_000_000,"ability":"황금 흡수 — 패시브 수입 +20%",
                "bg_color":"#0f0e00","accent":"#FFE100","particle":["💛","✨","💰","🟡"]},
    "fox":     {"name":"구미호",    "rarity":"희귀","rarity_color":"#FF6699",
                "desc":"꼬리 아홉 개인 아기 구미호. 눈이 초롱초롱해요!",
                "price":150_000_000,"ability":"미혹의 눈 — 도박 승률 +5%",
                "bg_color":"#150008","accent":"#FF6699","particle":["🌙","✨","🦊","💫"]},
}

# 펫 SVG 캐릭터 (각 펫마다 귀엽게 직접 그림)
def get_pet_svg(species, stage, mood, is_petting=False):
    """각 종 / 단계별 귀여운 SVG 캐릭터 반환"""

    # 눈 표정
    eyes = {
        "happy":   '<circle cx="37" cy="44" r="5" fill="#222"/><circle cx="63" cy="44" r="5" fill="#222"/><circle cx="39" cy="42" r="2" fill="white"/><circle cx="65" cy="42" r="2" fill="white"/>',
        "excited": '<ellipse cx="37" cy="44" rx="6" ry="7" fill="#222"/><ellipse cx="63" cy="44" rx="6" ry="7" fill="#222"/><circle cx="40" cy="41" r="2.5" fill="white"/>  <circle cx="66" cy="41" r="2.5" fill="white"/>',
        "shy":     '<path d="M32 46 Q37 40 42 46" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M58 46 Q63 40 68 46" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
        "tired":   '<path d="M32 44 Q37 48 42 44" stroke="#222" stroke-width="2.5" fill="none"/><path d="M58 44 Q63 48 68 44" stroke="#222" stroke-width="2.5" fill="none"/>',
        "sad":     '<path d="M33 46 Q37 43 41 46" stroke="#222" stroke-width="2" fill="none"/><path d="M59 46 Q63 43 67 46" stroke="#222" stroke-width="2" fill="none"/>',
        "normal":  '<circle cx="37" cy="44" r="4.5" fill="#222"/><circle cx="63" cy="44" r="4.5" fill="#222"/><circle cx="39" cy="42" r="1.5" fill="white"/><circle cx="65" cy="42" r="1.5" fill="white"/>',
    }
    blush = '<ellipse cx="26" cy="54" rx="9" ry="5" fill="#FF9FC1" opacity="0.5"/><ellipse cx="74" cy="54" rx="9" ry="5" fill="#FF9FC1" opacity="0.5"/>'
    blush_big = '<ellipse cx="24" cy="54" rx="12" ry="7" fill="#FF88BB" opacity="0.55"/><ellipse cx="76" cy="54" rx="12" ry="7" fill="#FF88BB" opacity="0.55"/>'

    eye_svg = eyes.get(mood, eyes["normal"])
    show_blush = mood in ("shy", "excited", "happy") or is_petting
    blush_svg = blush_big if is_petting else (blush if show_blush else "")

    # 입 표정
    mouths = {
        "happy":   '<path d="M38 60 Q50 70 62 60" stroke="#222" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
        "excited": '<ellipse cx="50" cy="63" rx="9" ry="7" fill="#FF6B9D"/><ellipse cx="50" cy="61" rx="9" ry="5" fill="#FF9FC1"/>',
        "shy":     '<path d="M42 62 Q50 58 58 62" stroke="#222" stroke-width="2" fill="none" stroke-linecap="round"/>',
        "tired":   '<path d="M43 63 Q50 67 57 63" stroke="#222" stroke-width="2" fill="none"/>',
        "sad":     '<path d="M40 65 Q50 60 60 65" stroke="#222" stroke-width="2" fill="none"/>',
        "normal":  '<path d="M40 62 Q50 68 60 62" stroke="#222" stroke-width="2" fill="none" stroke-linecap="round"/>',
    }
    mouth_svg = mouths.get(mood, mouths["normal"])

    if species == "dragon":
        col1, col2 = ("#FF6B35","#FF9060") if stage != "legend" else ("#FF2200","#FF6B35")
        horns = '<polygon points="30,18 26,2 34,14" fill="#FF4400"/><polygon points="70,18 74,2 66,14" fill="#FF4400"/>'
        wings = '' if stage == 'egg' else '<path d="M5,55 Q-5,35 15,30 Q5,55 20,60Z" fill="#FF5500" opacity="0.7"/><path d="M95,55 Q105,35 85,30 Q95,55 80,60Z" fill="#FF5500" opacity="0.7"/>'
        tail = '<path d="M75,85 Q95,100 85,115 Q75,120 80,105 Q90,95 75,90" fill="#FF6B35"/>' if stage != 'egg' else ''
        spikes = '<polygon points="50,5 46,20 54,20" fill="#FF4400"/><polygon points="40,10 37,22 44,20" fill="#FF5500"/><polygon points="60,10 63,22 56,20" fill="#FF5500"/>'
        nostrils = '<circle cx="45" cy="57" r="2.5" fill="#CC3300" opacity="0.7"/><circle cx="55" cy="57" r="2.5" fill="#CC3300" opacity="0.7"/>'
        body = f'''
        <g transform="scale(1.1) translate(-5,-5)">
        {wings}
        {horns}{spikes}
        <!-- body -->
        <ellipse cx="50" cy="70" rx="28" ry="32" fill="{col1}"/>
        <ellipse cx="50" cy="75" rx="20" ry="24" fill="{col2}" opacity="0.5"/>
        <!-- belly -->
        <ellipse cx="50" cy="72" rx="16" ry="18" fill="#FFD0A0" opacity="0.6"/>
        <!-- head -->
        <ellipse cx="50" cy="42" rx="26" ry="24" fill="{col1}"/>
        {eye_svg}{blush_svg}{mouth_svg}{nostrils}
        {tail}
        <!-- feet -->
        <ellipse cx="36" cy="97" rx="9" ry="6" fill="{col1}"/><ellipse cx="64" cy="97" rx="9" ry="6" fill="{col1}"/>
        <!-- claws -->
        <line x1="30" y1="100" x2="27" y2="105" stroke="#FF4400" stroke-width="2"/><line x1="36" y1="101" x2="36" y2="107" stroke="#FF4400" stroke-width="2"/><line x1="42" y1="100" x2="45" y2="105" stroke="#FF4400" stroke-width="2"/>
        </g>'''

    elif species == "slime":
        col1, col2 = ("#FFE100","#FFF176")
        body = f'''
        <!-- slime body -->
        <ellipse cx="50" cy="72" rx="36" ry="30" fill="{col1}"/>
        <!-- slime top bumps -->
        <ellipse cx="50" cy="44" rx="26" ry="22" fill="{col1}"/>
        <ellipse cx="30" cy="55" rx="14" ry="11" fill="{col1}"/>
        <ellipse cx="70" cy="55" rx="14" ry="11" fill="{col1}"/>
        <!-- shiny -->
        <ellipse cx="34" cy="36" rx="8" ry="11" fill="{col2}" opacity="0.55"/>
        <ellipse cx="27" cy="32" rx="3" ry="4" fill="white" opacity="0.4"/>
        <!-- eyes -->
        {eye_svg}{blush_svg}{mouth_svg}
        <!-- drip -->
        <ellipse cx="82" cy="85" rx="6" ry="9" fill="{col1}"/>
        <ellipse cx="20" cy="88" rx="5" ry="7" fill="{col1}"/>
        <!-- coins inside -->
        <circle cx="44" cy="78" r="6" fill="#FFD600" opacity="0.4"/>
        <circle cx="56" cy="73" r="5" fill="#FFD600" opacity="0.35"/>
        '''

    elif species == "cat":
        col1 = "#FFCCE0" if stage != "legend" else "#FF88C2"
        body = f'''
        <!-- ears -->
        <polygon points="22,22 14,2 36,18" fill="{col1}"/>
        <polygon points="78,22 86,2 64,18" fill="{col1}"/>
        <polygon points="25,20 19,7 34,17" fill="#FF9FC1"/>
        <polygon points="75,20 81,7 66,17" fill="#FF9FC1"/>
        <!-- body -->
        <ellipse cx="50" cy="73" rx="30" ry="28" fill="{col1}"/>
        <!-- tummy -->
        <ellipse cx="50" cy="75" rx="18" ry="18" fill="white" opacity="0.5"/>
        <!-- head -->
        <circle cx="50" cy="42" r="28" fill="{col1}"/>
        <!-- whiskers -->
        <line x1="20" y1="55" x2="40" y2="53" stroke="#aaa" stroke-width="1.2" opacity="0.6"/>
        <line x1="20" y1="58" x2="40" y2="58" stroke="#aaa" stroke-width="1.2" opacity="0.6"/>
        <line x1="80" y1="55" x2="60" y2="53" stroke="#aaa" stroke-width="1.2" opacity="0.6"/>
        <line x1="80" y1="58" x2="60" y2="58" stroke="#aaa" stroke-width="1.2" opacity="0.6"/>
        {eye_svg}{blush_svg}{mouth_svg}
        <!-- nose -->
        <polygon points="50,54 47,57 53,57" fill="#FF9FC1"/>
        <!-- paws -->
        <ellipse cx="30" cy="97" rx="11" ry="7" fill="{col1}"/>
        <ellipse cx="70" cy="97" rx="11" ry="7" fill="{col1}"/>
        <!-- paw pads -->
        <circle cx="28" cy="97" r="2.5" fill="#FF9FC1" opacity="0.6"/><circle cx="33" cy="95" r="2" fill="#FF9FC1" opacity="0.6"/><circle cx="33" cy="99" r="2" fill="#FF9FC1" opacity="0.6"/>
        <!-- tail -->
        <path d="M78,80 Q108,70 102,95 Q98,108 85,100" stroke="{col1}" stroke-width="11" fill="none" stroke-linecap="round"/>
        '''

    elif species == "wolf":
        col1, col2 = ("#E8C840","#FFF0A0")
        body = f'''
        <!-- ears -->
        <polygon points="25,20 18,0 38,16" fill="{col1}"/>
        <polygon points="75,20 82,0 62,16" fill="{col1}"/>
        <polygon points="27,18 22,5 36,15" fill="#FFF0A0"/>
        <polygon points="73,18 78,5 64,15" fill="#FFF0A0"/>
        <!-- body -->
        <ellipse cx="50" cy="73" rx="30" ry="27" fill="{col1}"/>
        <!-- chest fluff -->
        <ellipse cx="50" cy="70" rx="17" ry="20" fill="{col2}"/>
        <!-- head -->
        <ellipse cx="50" cy="43" rx="27" ry="25" fill="{col1}"/>
        <!-- snout -->
        <ellipse cx="50" cy="56" rx="13" ry="10" fill="{col2}"/>
        {eye_svg}{blush_svg}
        <!-- nose -->
        <ellipse cx="50" cy="52" rx="6" ry="4.5" fill="#333"/>
        <ellipse cx="48" cy="51" rx="2" ry="1.5" fill="white" opacity="0.5"/>
        {mouth_svg}
        <!-- paws -->
        <ellipse cx="32" cy="96" rx="10" ry="7" fill="{col1}"/><ellipse cx="68" cy="96" rx="10" ry="7" fill="{col1}"/>
        <!-- tail -->
        <path d="M77,82 Q110,65 105,92 Q100,108 82,100" stroke="{col1}" stroke-width="13" fill="none" stroke-linecap="round"/>
        <path d="M80,80 Q110,62 107,90 Q103,106 84,98" stroke="{col2}" stroke-width="6" fill="none" stroke-linecap="round"/>
        '''

    elif species == "penguin":
        body = f'''
        <!-- body -->
        <ellipse cx="50" cy="72" rx="28" ry="30" fill="#1a1a2e"/>
        <!-- belly -->
        <ellipse cx="50" cy="75" rx="18" ry="22" fill="white"/>
        <!-- head -->
        <ellipse cx="50" cy="40" rx="24" ry="23" fill="#1a1a2e"/>
        <!-- face white -->
        <ellipse cx="50" cy="44" rx="15" ry="14" fill="white"/>
        {eye_svg}{blush_svg}
        <!-- beak -->
        <polygon points="50,55 44,60 56,60" fill="#FFB300"/>
        {mouth_svg.replace('stroke="#222"','stroke="#FFB300"')}
        <!-- wings -->
        <ellipse cx="22" cy="68" rx="10" ry="20" fill="#1a1a2e" transform="rotate(-15,22,68)"/>
        <ellipse cx="78" cy="68" rx="10" ry="20" fill="#1a1a2e" transform="rotate(15,78,68)"/>
        <!-- feet -->
        <ellipse cx="38" cy="98" rx="12" ry="6" fill="#FFB300"/>
        <ellipse cx="62" cy="98" rx="12" ry="6" fill="#FFB300"/>
        <!-- crown (emperor) -->
        <rect x="38" y="14" width="24" height="8" rx="2" fill="#FFD600"/>
        <rect x="40" y="10" width="4" height="8" rx="1" fill="#FFD600"/>
        <rect x="48" y="8" width="4" height="10" rx="1" fill="#FFD600"/>
        <rect x="56" y="10" width="4" height="8" rx="1" fill="#FFD600"/>
        '''

    elif species == "unicorn":
        body = f'''
        <!-- body -->
        <ellipse cx="50" cy="73" rx="30" ry="28" fill="#F0CCFF"/>
        <!-- head -->
        <circle cx="50" cy="42" r="27" fill="#F0CCFF"/>
        <!-- horn -->
        <polygon points="50,4 44,26 56,26" fill="#CC44FF"/>
        <polygon points="50,4 44,26 50,20" fill="#EE88FF" opacity="0.6"/>
        <!-- mane -->
        <path d="M24,28 Q16,45 22,65" stroke="#FF88DD" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M22,30 Q14,47 20,67" stroke="#CC44FF" stroke-width="4" fill="none" stroke-linecap="round"/>
        {eye_svg}{blush_svg}{mouth_svg}
        <!-- nose -->
        <ellipse cx="50" cy="53" rx="6" ry="4" fill="#E0A0FF" opacity="0.5"/>
        <!-- legs -->
        <rect x="32" y="88" width="10" height="16" rx="5" fill="#F0CCFF"/>
        <rect x="58" y="88" width="10" height="16" rx="5" fill="#F0CCFF"/>
        <!-- hooves -->
        <ellipse cx="37" cy="104" rx="6" ry="4" fill="#CC44FF"/>
        <ellipse cx="63" cy="104" rx="6" ry="4" fill="#CC44FF"/>
        <!-- tail -->
        <path d="M78,75 Q100,60 95,90" stroke="#FF88DD" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M79,73 Q102,58 97,88" stroke="#CC44FF" stroke-width="4" fill="none" stroke-linecap="round"/>
        '''

    elif species == "phoenix":
        body = f'''
        <!-- tail feathers -->
        <path d="M50,90 Q20,115 15,140" stroke="#FF6600" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M50,90 Q50,120 45,145" stroke="#FF9500" stroke-width="8" fill="none" stroke-linecap="round"/>
        <path d="M50,90 Q80,115 85,140" stroke="#FFCC00" stroke-width="8" fill="none" stroke-linecap="round"/>
        <!-- wings -->
        <path d="M22,55 Q5,30 18,15 Q30,40 35,60Z" fill="#FF7700" opacity="0.85"/>
        <path d="M78,55 Q95,30 82,15 Q70,40 65,60Z" fill="#FF7700" opacity="0.85"/>
        <!-- body -->
        <ellipse cx="50" cy="70" rx="25" ry="26" fill="#FF9500"/>
        <!-- chest -->
        <ellipse cx="50" cy="72" rx="15" ry="16" fill="#FFCC44" opacity="0.7"/>
        <!-- head -->
        <circle cx="50" cy="42" r="25" fill="#FF9500"/>
        <!-- crest fire -->
        <path d="M35,22 Q40,5 50,15 Q55,0 60,15 Q70,5 65,22" fill="#FF4400"/>
        <path d="M40,22 Q44,10 50,18 Q56,10 60,22" fill="#FFCC00" opacity="0.8"/>
        {eye_svg}{blush_svg}{mouth_svg}
        <!-- beak -->
        <polygon points="50,53 44,58 56,58" fill="#FF6600"/>
        '''

    else:  # fallback cat
        col1 = "#FFCCE0"
        body = f'''<circle cx="50" cy="50" r="40" fill="{col1}"/>{eye_svg}{mouth_svg}'''

    # 알 단계는 별도
    if stage == "egg":
        sp = PET_SPECIES.get(species, PET_SPECIES["cat"])
        rc = sp["rarity_color"]
        return f'''<svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg" width="160" height="192">
          <defs>
            <radialGradient id="eg" cx="38%" cy="30%" r="68%">
              <stop offset="0%" stop-color="#fffbf0"/><stop offset="65%" stop-color="#f0d888"/><stop offset="100%" stop-color="#d4a840"/>
            </radialGradient>
            <radialGradient id="ig" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="{rc}" stop-opacity="0.7"/><stop offset="100%" stop-color="{rc}" stop-opacity="0"/>
            </radialGradient>
          </defs>
          <ellipse cx="50" cy="70" rx="42" ry="58" fill="url(#eg)" filter="drop-shadow(0 4px 16px {rc}88)"/>
          <ellipse cx="50" cy="70" rx="38" ry="52" fill="url(#ig)" opacity="0.4" style="animation:glowPulse 1.2s ease-in-out infinite"/>
          <ellipse cx="33" cy="42" rx="12" ry="16" fill="white" opacity="0.35" transform="rotate(-20,33,42)"/>
          <ellipse cx="50" cy="70" rx="42" ry="58" fill="none" stroke="{rc}" stroke-width="1.5" opacity="0.5"/>
          <text x="50" y="76" text-anchor="middle" font-size="28">❓</text>
        </svg>'''

    return f'''<svg viewBox="0 0 100 110" xmlns="http://www.w3.org/2000/svg" width="180" height="198">
      {body}
    </svg>'''


PET_FOOD = {
    "kibble":    {"name":"일반 사료",    "icon":"🍖","price":500_000,    "exp":10,"happiness":8,  "hunger_restore":15,"reaction":"먹었어요!"},
    "gourmet":   {"name":"고급 사료",    "icon":"🥩","price":2_000_000,  "exp":40,"happiness":20,"hunger_restore":30,"reaction":"맛있다!!"},
    "premium":   {"name":"프리미엄 사료","icon":"🍗","price":8_000_000,  "exp":100,"happiness":35,"hunger_restore":50,"reaction":"최고야~!"},
    "stardust":  {"name":"별의 가루",    "icon":"✨","price":50_000_000, "exp":500,"happiness":55,"hunger_restore":100,"reaction":"반짝반짝!"},
    "dragonmeat":{"name":"용의 심장",   "icon":"💎","price":200_000_000,"exp":2000,"happiness":80,"hunger_restore":100,"reaction":"최강이닷!"},
    "moonberry": {"name":"달빛 열매",   "icon":"🫐","price":20_000_000, "exp":200,"happiness":45,"hunger_restore":60,"reaction":"달달해~"},
}

PET_ACCESSORIES = {
    "collar": {"name":"황금 목걸이","icon":"📿","price":20_000_000,  "desc":"행운 +5%",     "bonus_type":"luck",   "bonus":5},
    "hat":    {"name":"왕관 모자",  "icon":"👑","price":50_000_000,  "desc":"EXP +10%",    "bonus_type":"exp",    "bonus":10},
    "armor":  {"name":"미스릴 갑옷","icon":"🛡️","price":100_000_000, "desc":"수입 +8%",    "bonus_type":"income", "bonus":8},
    "wings":  {"name":"불사의 날개","icon":"🦋","price":200_000_000, "desc":"행복도 유지",  "bonus_type":"happy",  "bonus":20},
    "gem":    {"name":"드래곤 젬",  "icon":"💎","price":500_000_000, "desc":"모든 보너스+5%","bonus_type":"all",   "bonus":5},
    "amulet": {"name":"별빛 부적",  "icon":"🔮","price":80_000_000,  "desc":"배틀 ATK+15%","bonus_type":"battle", "bonus":15},
    "ribbon": {"name":"행운의 리본","icon":"🎀","price":15_000_000,  "desc":"탐험 보상+10%","bonus_type":"exp",   "bonus":10},
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
    "forest":  {"name":"신비의 숲",  "icon":"🌲","duration_h":1,  "min_lv":1,  "base_exp":80,   "base_cash":500_000,    "desc":"초보자도 도전 가능!",      "rare_item":"🌿 희귀 약초"},
    "desert":  {"name":"황금 사막",  "icon":"🏜️","duration_h":3,  "min_lv":5,  "base_exp":300,  "base_cash":3_000_000,  "desc":"황금 모래 속 보물!",        "rare_item":"💰 황금 원석"},
    "dungeon": {"name":"고대 던전",  "icon":"🏰","duration_h":8,  "min_lv":10, "base_exp":900,  "base_cash":12_000_000, "desc":"위험하지만 보상이 크다!",    "rare_item":"⚔️ 유물 파편"},
    "volcano": {"name":"용암 화산",  "icon":"🌋","duration_h":12, "min_lv":20, "base_exp":2000, "base_cash":40_000_000, "desc":"드래곤의 영역!",             "rare_item":"🔥 용암 결정"},
    "space":   {"name":"심우주",     "icon":"🚀","duration_h":24, "min_lv":35, "base_exp":6000, "base_cash":200_000_000,"desc":"우주의 끝에서 전설의 유물!", "rare_item":"🌌 별의 파편"},
    "heaven":  {"name":"신계 천공",  "icon":"☁️","duration_h":48, "min_lv":45, "base_exp":20000,"base_cash":1_000_000_000,"desc":"신의 세계. 전설만 입장!", "rare_item":"🌟 신의 눈물"},
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
    {"id":"first_feed",   "icon":"🍖","name":"첫 식사",     "desc":"처음으로 먹이를 줬다"},
    {"id":"well_fed",     "icon":"🤤","name":"맛있겠다",    "desc":"총 50번 먹이기 완료"},
    {"id":"feast",        "icon":"🏆","name":"미식가",      "desc":"총 500번 먹이기 완료"},
    {"id":"lv10",         "icon":"⚡","name":"성장통",      "desc":"레벨 10 달성"},
    {"id":"lv25",         "icon":"🌟","name":"영웅의 탄생", "desc":"레벨 25 달성"},
    {"id":"lv50",         "icon":"🌌","name":"전설이 되다", "desc":"레벨 50 달성"},
    {"id":"happy_max",    "icon":"😊","name":"행복 만점",   "desc":"행복도 100 달성"},
    {"id":"explorer1",    "icon":"🗺️","name":"탐험가",      "desc":"첫 탐험 완료"},
    {"id":"explorer10",   "icon":"🌍","name":"세계 정복자", "desc":"탐험 10회 완료"},
    {"id":"battle_win1",  "icon":"⚔️","name":"첫 승리",     "desc":"배틀 첫 승리"},
    {"id":"battle_win10", "icon":"🏅","name":"전투의 달인", "desc":"배틀 10승"},
    {"id":"hatched",      "icon":"🐣","name":"탄생의 기적", "desc":"알에서 부화"},
    {"id":"bonded",       "icon":"💕","name":"절친",        "desc":"유대감 레벨 3 달성"},
    {"id":"full_acc",     "icon":"👑","name":"풀 장착",     "desc":"악세서리 2개 장착"},
    {"id":"legend",       "icon":"🌌","name":"우주의 뜻",   "desc":"전설 단계 도달 (Lv.40)"},
]

MOOD_SYSTEM = {
    "신남":   {"emoji":"🤩","color":"#FFD600","desc":"최고로 행복한 상태!",    "svg_mood":"excited", "condition":lambda h,hg,hp: h>=90 and hg>=80 and hp>=80},
    "행복":   {"emoji":"😊","color":"#00FF88","desc":"기분 좋은 상태",         "svg_mood":"happy",   "condition":lambda h,hg,hp: h>=60 and hg>=60},
    "배고픔": {"emoji":"😮","color":"#FF9500","desc":"배가 고파요!",            "svg_mood":"sad",     "condition":lambda h,hg,hp: hg<20},
    "아픔":   {"emoji":"🤒","color":"#FF4B4B","desc":"HP가 위험해요!",          "svg_mood":"tired",   "condition":lambda h,hg,hp: hp<20},
    "피곤":   {"emoji":"😴","color":"#8888FF","desc":"좀 쉬고 싶어요",         "svg_mood":"tired",   "condition":lambda h,hg,hp: h<30},
    "슬픔":   {"emoji":"😢","color":"#4488FF","desc":"같이 놀아주세요",         "svg_mood":"sad",     "condition":lambda h,hg,hp: h<50},
    "보통":   {"emoji":"😐","color":"#94A3B8","desc":"평범한 상태",            "svg_mood":"normal",  "condition":lambda h,hg,hp: True},
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
    if lv < 5:    return 'egg'
    elif lv < 20: return 'baby'
    elif lv < 40: return 'adult'
    else:         return 'legend'

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
        pet['hp'] = min(100, pet.get('hp',100) + 10)
        leveled_up = True
        for s in PET_SKILLS:
            if s['level'] == pet['level'] and s['name'] not in pet.get('skills',[]):
                pet.setdefault('skills',[]).append(s['name'])
        add_journal(pet, f"🎉 레벨업! Lv.{pet['level']} 달성!")
    return pet, leveled_up, exp_gained

def get_passive_income(pet):
    lv = pet.get('level',0)
    if lv < 20: return 0
    base = lv * 1_000_000
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
    atk = lv * 5; df = lv * 3; spd = lv * 2
    sp = pet.get('species','cat')
    if sp == 'dragon':   atk = int(atk * 1.3)
    elif sp == 'wolf':   atk = int(atk * 1.15)
    elif sp == 'penguin': df = int(df * 1.2)
    elif sp == 'phoenix': spd= int(spd * 1.2)
    for a in pet.get('accessories',[]):
        acc = PET_ACCESSORIES.get(a,{})
        if acc.get('bonus_type') == 'battle': atk = int(atk * (1 + acc.get('bonus',0)/100))
    return {"atk":atk,"def":df,"spd":spd}

def check_and_award_achievements(pet):
    earned = []
    lv=pet.get('level',0); tf=pet.get('total_fed',0); h=pet.get('happiness',100)
    ex=pet.get('expeditions',0); bw=pet.get('battles_won',0); bd=pet.get('bond',0); ac=len(pet.get('accessories',[]))
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
    pet['journal'] = j[:50]

def get_bond_title(bond_lv):
    return BOND_TITLES[min(bond_lv, len(BOND_TITLES)-1)]

def get_expedition_reward(zone_id, pet):
    z = EXPEDITION_ZONES[zone_id]; lv = pet.get('level',1)
    mul = max(1.0, min(1 + (lv - z['min_lv']) * 0.05, 3.0))
    rare_chance = min(0.15 + lv * 0.003, 0.5)
    got_rare = random.random() < rare_chance
    return (int(z['base_exp'] * mul * random.uniform(0.85,1.2)),
            int(z['base_cash'] * mul * random.uniform(0.85,1.2)),
            got_rare, z.get('rare_item','✨ 희귀 아이템'))

def get_available_monsters(lv):
    return [m for m in WILD_MONSTERS if m['lv_req'] <= lv]

# ══════════════════════════════════════════════════════════════════════════════
# 🎨 INTERACTIVE PET CARD HTML
# ══════════════════════════════════════════════════════════════════════════════

def generate_pet_card_html(pet, sp, lv, exp_pct, hunger, happy, hp):
    species   = pet.get('species','cat')
    name      = pet.get('name','펫')
    stage     = get_pet_stage(lv)
    mood_name, mood_data = get_mood(pet)
    svg_mood  = mood_data.get('svg_mood','normal')
    accent    = sp.get('accent','#00E5FF')
    bg_color  = sp.get('bg_color','#0a0f1e')
    particles = json.dumps(sp.get('particle',['✨','💫']))

    # SVG 캐릭터
    pet_svg = get_pet_svg(species, stage, svg_mood, False)
    pet_svg_happy = get_pet_svg(species, stage, 'excited', True)
    pet_svg_shy   = get_pet_svg(species, stage, 'shy', True)
    pet_svg_tired = get_pet_svg(species, stage, 'tired', False)

    # HP가 낮으면 tired 표정
    if hp < 30 or hunger < 20:
        default_svg = pet_svg_tired
    elif happy >= 80:
        default_svg = get_pet_svg(species, stage, 'happy', False)
    else:
        default_svg = pet_svg

    def bar_color(v):
        if v < 30: return '#ff4b4b'
        if v < 60: return '#ffd600'
        return '#00ff88'

    mood_reactions = {
        "신남":   ["최고야~!!! 🤩","우와아아!!! ✨","행복해 죽겠다!!"],
        "행복":   ["좋아좋아~ 😊","기분 최고!","오늘도 행복해~"],
        "피곤":   ["...피곤해 😴","조금만 쉬자...","졸려..."],
        "슬픔":   ["놀아줘... 😢","심심해...","혼자야?"],
        "배고픔": ["배고파!! 😮","밥 줘!!!","꼬르륵..."],
        "아픔":   ["아파... 🤒","치료해줘...","힘들어..."],
        "보통":   ["안녕! 😊","잘 있어~","오늘도 파이팅!"],
    }
    pet_says = json.dumps(mood_reactions.get(mood_name, mood_reactions["보통"]))
    feed_reactions = json.dumps(["맛있다! 😋","냠냠냠! 🍖","더 줘~! 💕","고마워! 😊","최고야! ✨"])
    pet_reactions = json.dumps(["좋아! 💕","히힛~ 부끄러워! 😳","기분좋다! 😊","또 쓰다듬어줘~ 🥰","간질간질! 😆"])
    tired_reactions = json.dumps(["지금 피곤해... 😴","나중에 놀자...","너무 힘들어 ㅠ"])

    rarity_color = sp.get('rarity_color', '#00E5FF')

    # 기분 카운트다운 애니메이션
    float_anim = "petFloat 3s ease-in-out infinite"
    if hp < 30 or hunger < 20:
        float_anim = "petSleep 4s ease-in-out infinite"
    elif happy < 40:
        float_anim = "petSad 2.5s ease-in-out infinite"
    elif happy >= 80 and hunger >= 60:
        float_anim = "petBounce 2s ease-in-out infinite"

    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{background:transparent;overflow:hidden;font-family:'Segoe UI',sans-serif;}}
#app{{
  width:100%;height:460px;
  background:radial-gradient(ellipse at 30% 30%, {bg_color}ee 0%, #050505 100%);
  border:2px solid {accent}55;border-radius:24px;position:relative;overflow:hidden;
  display:flex;align-items:center;justify-content:center;
  box-shadow:0 0 40px {accent}22,inset 0 0 80px rgba(0,0,0,0.5);
}}
/* starfield */
.star{{position:absolute;border-radius:50%;background:white;pointer-events:none;animation:twinkle var(--d) ease-in-out infinite var(--delay);}}
@keyframes twinkle{{0%,100%{{opacity:var(--min);transform:scale(1);}}50%{{opacity:var(--max);transform:scale(1.5);}}}}

/* pet container */
#pet-wrap{{
  display:flex;flex-direction:column;align-items:center;
  position:relative;z-index:10;cursor:pointer;user-select:none;
}}
#pet-svg-wrap{{
  position:relative;display:flex;align-items:center;justify-content:center;
  animation:{float_anim};
  transition:filter 0.3s;
  filter:drop-shadow(0 8px 30px {accent}66);
}}
#pet-svg-wrap:hover{{filter:drop-shadow(0 8px 45px {accent}cc) drop-shadow(0 0 20px #fff4);}}
#pet-svg-wrap.petting{{animation:petPetting 0.2s ease-in-out infinite!important;filter:drop-shadow(0 8px 50px {accent}ff) drop-shadow(0 0 30px #ffff0077)!important;}}
#pet-svg-wrap.fed{{animation:petJump 0.5s ease-out!important;}}

/* speech bubble */
#bubble{{
  position:absolute;top:-55px;left:50%;transform:translateX(-50%);
  background:white;color:#333;font-size:13px;font-weight:700;
  padding:8px 16px;border-radius:20px;white-space:nowrap;
  box-shadow:0 4px 20px rgba(0,0,0,0.3);
  opacity:0;transition:opacity 0.3s,transform 0.3s;
  pointer-events:none;z-index:30;
  border:2px solid {accent}44;
}}
#bubble::after{{
  content:'';position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);
  border:5px solid transparent;border-top:6px solid white;
}}
#bubble.show{{opacity:1;transform:translateX(-50%) translateY(-5px);}}

/* name & mood */
#name-area{{
  position:absolute;bottom:95px;left:50%;transform:translateX(-50%);
  text-align:center;z-index:20;
}}
#pet-name{{
  color:white;font-size:18px;font-weight:900;
  text-shadow:0 0 15px {accent};letter-spacing:2px;
}}
#mood-badge{{
  display:inline-block;margin-top:5px;
  background:rgba(0,0,0,0.7);border:1px solid {mood_data['color']};
  border-radius:20px;padding:3px 12px;
  color:{mood_data['color']};font-size:11px;font-weight:700;
}}

/* status bars */
#status{{position:absolute;bottom:10px;left:16px;right:16px;z-index:20;}}
.bar-row{{display:flex;align-items:center;gap:8px;margin-bottom:6px;}}
.bar-lbl{{color:#888;font-size:10px;width:48px;flex-shrink:0;}}
.bar-bg{{flex:1;background:rgba(255,255,255,0.08);border-radius:3px;height:6px;overflow:hidden;border:1px solid rgba(255,255,255,0.05);}}
.bar-fill{{height:100%;border-radius:3px;transition:width 0.8s ease;}}
.bar-val{{color:#ccc;font-size:10px;width:24px;text-align:right;flex-shrink:0;}}

/* badges */
#lv-badge{{
  position:absolute;top:14px;right:14px;
  background:rgba(0,0,0,0.85);border:2px solid {accent};border-radius:16px;
  padding:8px 14px;text-align:center;z-index:20;
}}
#lv-num{{color:#FFD600;font-size:24px;font-weight:900;line-height:1;}}
#lv-lbl{{color:#555;font-size:8px;letter-spacing:2px;margin-top:1px;}}
#rar-badge{{
  position:absolute;top:14px;left:14px;
  background:rgba(0,0,0,0.85);border:1px solid {rarity_color}88;
  border-radius:12px;padding:5px 12px;
  color:{rarity_color};font-size:11px;font-weight:900;letter-spacing:1px;z-index:20;
}}

/* effects layer */
#efx{{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:50;}}
.heart{{position:absolute;pointer-events:none;font-size:18px;animation:heartUp 1.4s ease-out forwards;}}
.spark{{position:absolute;pointer-events:none;font-size:14px;animation:sparkOut 0.7s ease-out forwards;}}
.food-effect{{position:absolute;pointer-events:none;font-size:26px;animation:foodBounce 1.2s ease-out forwards;}}
.ptcl{{position:absolute;pointer-events:none;font-size:13px;animation:ptclFloat linear forwards;opacity:0;}}
.lvup{{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-size:36px;font-weight:900;color:#FFD600;z-index:60;
  text-shadow:0 0 30px #FFD600;animation:lvUpPop 2s ease-out forwards;
  pointer-events:none;white-space:nowrap;
}}

/* pet animations */
@keyframes petFloat{{0%,100%{{transform:translateY(0) rotate(-1deg);}}50%{{transform:translateY(-20px) rotate(1.5deg);}}}}
@keyframes petBounce{{0%,100%{{transform:translateY(0) scale(1);}}30%{{transform:translateY(-28px) scale(1.05);}}60%{{transform:translateY(-12px) scale(1.02);}}}}
@keyframes petSleep{{0%,100%{{transform:translateY(0) rotate(-4deg) scale(0.96);}}50%{{transform:translateY(-8px) rotate(-2deg) scale(0.97);}}}}
@keyframes petSad{{0%,100%{{transform:translateY(0) rotate(0);}}50%{{transform:translateY(-10px) rotate(-2deg);}}}}
@keyframes petPetting{{0%,100%{{transform:rotate(-8deg) scale(1.08) translateY(-10px);}}50%{{transform:rotate(8deg) scale(1.12) translateY(-16px);}}}}
@keyframes petJump{{0%{{transform:scale(1) translateY(0);}}30%{{transform:scale(0.9) translateY(-40px);}}60%{{transform:scale(1.1) translateY(-10px);}}80%{{transform:scale(0.97) translateY(-5px);}}100%{{transform:scale(1) translateY(0);}}}}
@keyframes heartUp{{0%{{opacity:1;transform:translateY(0) scale(0.5) rotate(var(--r));}}50%{{opacity:1;transform:translateY(-45px) scale(1.1) rotate(var(--r));}}100%{{opacity:0;transform:translateY(-90px) scale(0.6) rotate(var(--r));}}}}
@keyframes sparkOut{{0%{{opacity:1;transform:scale(0) rotate(0);}}50%{{opacity:1;transform:scale(1.8) rotate(180deg) translate(var(--dx),var(--dy));}}100%{{opacity:0;transform:scale(0) rotate(360deg) translate(calc(var(--dx)*1.5),calc(var(--dy)*1.5));}}}}
@keyframes foodBounce{{0%{{opacity:1;transform:scale(0.3) translateY(20px);}}25%{{opacity:1;transform:scale(1.3) translateY(-30px);}}60%{{transform:scale(1) translateY(-15px);}}80%{{transform:scale(1.05) translateY(-18px);}}100%{{opacity:0;transform:scale(0.5) translateY(-60px);}}}}
@keyframes ptclFloat{{0%{{opacity:0;transform:translateY(0) scale(0.5);}}10%{{opacity:0.7;}}90%{{opacity:0.1;}}100%{{opacity:0;transform:translateY(-280px) translateX(var(--dx)) scale(1);}}}}
@keyframes lvUpPop{{0%{{opacity:0;transform:translate(-50%,-50%) scale(0.3);}}20%{{opacity:1;transform:translate(-50%,-50%) scale(1.3);}}50%{{opacity:1;transform:translate(-50%,-50%) scale(1);}}80%{{opacity:1;}}100%{{opacity:0;transform:translate(-50%,-80%) scale(0.8);}}}}
@keyframes glowPulse{{0%,100%{{opacity:0.3;}}50%{{opacity:0.8;}}}}
</style>
</head>
<body>
<div id="app">
  <!-- Stars background -->
  <div id="stars"></div>
  <div id="efx"></div>

  <!-- Badges -->
  <div id="rar-badge">★ {sp.get('rarity','일반')}</div>
  <div id="lv-badge"><div id="lv-num">Lv.{lv}</div><div id="lv-lbl">LEVEL</div></div>

  <!-- Pet -->
  <div id="pet-wrap">
    <div id="bubble" class="bubble"></div>
    <div id="pet-svg-wrap" onmouseenter="onHoverStart()" onmouseleave="onHoverEnd()" onmousemove="onMouseMove(event)" onclick="onPetClick(event)">
      <div id="pet-svg-inner">{default_svg}</div>
    </div>
  </div>

  <!-- Name & mood -->
  <div id="name-area">
    <div id="pet-name">♦ {name} ♦</div>
    <div id="mood-badge">{mood_data['emoji']} {mood_name} — {mood_data['desc']}</div>
  </div>

  <!-- Status -->
  <div id="status">
    <div class="bar-row">
      <div class="bar-lbl">❤️ HP</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{hp}%;background:{bar_color(hp)};"></div></div>
      <div class="bar-val">{hp}</div>
    </div>
    <div class="bar-row">
      <div class="bar-lbl">🍖 허기</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{hunger}%;background:{bar_color(hunger)};"></div></div>
      <div class="bar-val">{hunger}</div>
    </div>
    <div class="bar-row">
      <div class="bar-lbl">😊 행복</div>
      <div class="bar-bg"><div class="bar-fill" style="width:{happy}%;background:{bar_color(happy)};"></div></div>
      <div class="bar-val">{happy}</div>
    </div>
  </div>
</div>

<script>
const APP    = document.getElementById('app');
const EFX    = document.getElementById('efx');
const WRAP   = document.getElementById('pet-svg-wrap');
const INNER  = document.getElementById('pet-svg-inner');
const BUBBLE = document.getElementById('bubble');
const ACCENT = "{accent}";
const PARTICLES = {particles};
const PET_SAYS = {pet_says};
const FEED_REACTIONS = {feed_reactions};
const PET_REACTIONS = {pet_reactions};
const TIRED_REACTIONS = {tired_reactions};
const HUNGER = {hunger};
const HAPPY  = {happy};
const HP_VAL = {hp};
const STAGE  = "{stage}";

const SVG_NORMAL = `{default_svg.replace('`','&#96;')}`;
const SVG_HAPPY  = `{pet_svg_happy.replace('`','&#96;')}`;
const SVG_SHY    = `{pet_svg_shy.replace('`','&#96;')}`;
const SVG_TIRED  = `{pet_svg_tired.replace('`','&#96;')}`;

// ── Stars
const starsDiv = document.getElementById('stars');
for (let i = 0; i < 80; i++) {{
  const s = document.createElement('div');
  s.className = 'star';
  const size = Math.random() * 2 + 0.5;
  s.style.cssText = `width:${{size}}px;height:${{size}}px;left:${{Math.random()*100}}%;top:${{Math.random()*100}}%;--d:${{2+Math.random()*4}}s;--delay:${{-Math.random()*5}}s;--min:${{0.05+Math.random()*0.15}};--max:${{0.3+Math.random()*0.5}};`;
  starsDiv.appendChild(s);
}}

// ── Show bubble
let bubbleTimer = null;
function showBubble(text) {{
  BUBBLE.textContent = text;
  BUBBLE.classList.add('show');
  clearTimeout(bubbleTimer);
  bubbleTimer = setTimeout(() => BUBBLE.classList.remove('show'), 2200);
}}

// ── Mouse enter: 쓰다듬기 시작
let pettingInterval = null;
let lastHeartTime = 0;
let isTired = HP_VAL < 30 || HUNGER < 20;

function onHoverStart() {{
  if (STAGE === 'egg') return;
  if (isTired) {{
    // 피곤할 때 호버: 싫어함
    INNER.innerHTML = SVG_TIRED;
    showBubble(TIRED_REACTIONS[Math.floor(Math.random()*TIRED_REACTIONS.length)]);
    return;
  }}
  WRAP.classList.add('petting');
  INNER.innerHTML = SVG_SHY;
  showBubble(PET_REACTIONS[Math.floor(Math.random()*PET_REACTIONS.length)]);
}}

function onMouseMove(e) {{
  if (STAGE === 'egg' || isTired) return;
  const now = Date.now();
  if (now - lastHeartTime < 180) return;
  lastHeartTime = now;
  const r = APP.getBoundingClientRect();
  spawnHeart(e.clientX - r.left, e.clientY - r.top - 15);
}}

function onHoverEnd() {{
  if (STAGE === 'egg') return;
  WRAP.classList.remove('petting');
  if (!isTired) {{
    INNER.innerHTML = SVG_NORMAL;
  }}
}}

// ── Click: 신나게 점프
function onPetClick(e) {{
  if (STAGE === 'egg') {{
    eggTap(e); return;
  }}
  const r = APP.getBoundingClientRect();
  const x = e.clientX - r.left, y = e.clientY - r.top;
  spawnSparks(x, y, 8);
  WRAP.classList.add('fed');
  INNER.innerHTML = SVG_HAPPY;
  showBubble(PET_SAYS[Math.floor(Math.random()*PET_SAYS.length)]);
  setTimeout(() => {{
    WRAP.classList.remove('fed');
    INNER.innerHTML = isTired ? SVG_TIRED : SVG_NORMAL;
  }}, 800);
}}

// ── Egg tap
function eggTap(e) {{
  const r = APP.getBoundingClientRect();
  spawnSparks(e.clientX-r.left, e.clientY-r.top, 5);
  showBubble('??');
}}

// ── Particles
function spawnParticles() {{
  const p = document.createElement('div');
  p.className = 'ptcl';
  p.textContent = PARTICLES[Math.floor(Math.random()*PARTICLES.length)];
  const dx = (Math.random()-0.5)*120;
  p.style.setProperty('--dx', dx+'px');
  p.style.left = Math.random()*100+'%';
  p.style.bottom = '-10px';
  p.style.animationDuration = (5+Math.random()*6)+'s';
  APP.appendChild(p);
  setTimeout(() => p.remove(), 12000);
}}
setInterval(spawnParticles, 1000);

// ── Hearts
const HEARTS = ['💕','💖','💗','💝','❤️','🩷','💓'];
function spawnHeart(x, y) {{
  const h = document.createElement('div');
  h.className = 'heart';
  h.textContent = HEARTS[Math.floor(Math.random()*HEARTS.length)];
  h.style.setProperty('--r', (Math.random()-0.5)*50+'deg');
  h.style.left = x+'px'; h.style.top = y+'px';
  EFX.appendChild(h);
  setTimeout(() => h.remove(), 1500);
}}

// ── Sparks
const SPARKS = ['✨','⭐','💫','🌟','🌸','💥'];
function spawnSparks(x, y, n) {{
  for (let i = 0; i < n; i++) {{
    const s = document.createElement('div');
    s.className = 'spark';
    s.textContent = SPARKS[Math.floor(Math.random()*SPARKS.length)];
    const a = (i/n)*Math.PI*2;
    const d = 25+Math.random()*35;
    s.style.setProperty('--dx', Math.cos(a)*d+'px');
    s.style.setProperty('--dy', Math.sin(a)*d+'px');
    s.style.left = x+'px'; s.style.top = y+'px';
    s.style.animationDelay = (i*0.03)+'s';
    EFX.appendChild(s);
    setTimeout(() => s.remove(), 900);
  }}
}}

// ── Food effect (triggered externally via postMessage)
window.addEventListener('message', e => {{
  if (e.data && e.data.type === 'feed') {{
    const f = document.createElement('div');
    f.className = 'food-effect';
    f.textContent = e.data.icon || '🍖';
    f.style.left = '50%'; f.style.top = '45%';
    f.style.transform = 'translateX(-50%)';
    EFX.appendChild(f);
    setTimeout(() => f.remove(), 1500);

    WRAP.classList.add('fed');
    INNER.innerHTML = SVG_HAPPY;
    showBubble(FEED_REACTIONS[Math.floor(Math.random()*FEED_REACTIONS.length)]);
    setTimeout(() => {{
      WRAP.classList.remove('fed');
      INNER.innerHTML = SVG_NORMAL;
    }}, 1200);
  }}
  if (e.data && e.data.type === 'levelup') {{
    const lv = document.createElement('div');
    lv.className = 'lvup';
    lv.textContent = '🎉 LEVEL UP! 🎉';
    EFX.appendChild(lv);
    setTimeout(() => lv.remove(), 2200);
    for (let i = 0; i < 20; i++) {{
      setTimeout(() => spawnSparks(180+Math.random()*300, 100+Math.random()*200, 5), i*80);
    }}
  }}
}});

// ── Auto idle bubble (based on mood)
setInterval(() => {{
  if (BUBBLE.classList.contains('show')) return;
  if (Math.random() < 0.25) {{
    showBubble(PET_SAYS[Math.floor(Math.random()*PET_SAYS.length)]);
  }}
}}, 6000);
</script>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 🏠 MAIN RENDER
# ══════════════════════════════════════════════════════════════════════════════

def render(market, nw):
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');
    .pet-tab-header{font-size:1.1rem;font-weight:900;color:#E2E8F0;margin-bottom:10px;font-family:'Nunito',sans-serif;}
    .pet-sub{color:#64748B;font-size:0.82rem;margin-bottom:14px;}
    .pet-card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:16px;padding:14px;margin-bottom:10px;transition:all 0.2s;}
    .pet-card:hover{border-color:rgba(0,229,255,0.25);background:rgba(0,229,255,0.03);}
    .stat-chip{display:inline-block;padding:3px 10px;border-radius:8px;font-size:0.73rem;font-weight:700;margin-right:4px;margin-bottom:4px;}
    </style>
    """, unsafe_allow_html=True)

    st.title("🐾 펫 키우기")
    uid   = st.session_state.logged_in_user
    users = load_db(USERS_FILE, {})
    pet   = load_pet(uid, users)

    if pet.get('species'):
        pet = decay_stats(pet)

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

    # Expedition return
    exp_data = pet.get('expedition')
    if exp_data and time.time() >= exp_data.get('return_time', 0):
        st.session_state['expedition_returned'] = True

    # ══════════════════════════════════════════════════════════════
    # NO PET → ADOPTION
    # ══════════════════════════════════════════════════════════════
    if not pet.get('species'):
        st.markdown("""
        <div style='text-align:center;padding:40px 20px;background:rgba(255,255,255,0.02);
                    border:1px solid rgba(255,255,255,0.08);border-radius:22px;margin-bottom:28px;'>
            <div style='font-size:4.5rem;margin-bottom:12px;'>🐾</div>
            <div style='font-size:1.5rem;font-weight:900;color:#E2E8F0;margin-bottom:8px;'>아직 펫이 없어요!</div>
            <div style='color:#64748B;font-size:0.88rem;'>귀엽고 소중한 파트너를 입양해보세요!</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏪 펫 입양소")
        rarity_order = ["전설","영웅","희귀","고급","일반"]
        sorted_species = sorted(PET_SPECIES.items(), key=lambda x: rarity_order.index(x[1]['rarity']) if x[1]['rarity'] in rarity_order else 99)

        sp_cols = st.columns(4)
        for i, (sp_id, sp) in enumerate(sorted_species):
            with sp_cols[i % 4]:
                # 입양소에서는 알 상태의 귀여운 SVG 표시
                preview_svg = get_pet_svg(sp_id, 'baby', 'happy', False)
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;border-color:{sp["rarity_color"]}33;min-height:340px;'>
                    <div style='display:flex;justify-content:center;margin-bottom:8px;
                                filter:drop-shadow(0 4px 20px {sp["rarity_color"]}88);'>
                        {preview_svg}
                    </div>
                    <div style='font-size:1rem;font-weight:900;color:#E2E8F0;'>{sp['name']}</div>
                    <div style='font-size:0.72rem;color:{sp["rarity_color"]};margin:4px 0;font-weight:900;'>★ {sp['rarity']}</div>
                    <div style='font-size:0.73rem;color:#64748B;margin-bottom:8px;'>{sp['desc']}</div>
                    <div style='font-size:0.7rem;color:{sp["rarity_color"]};background:rgba(0,0,0,0.3);padding:4px 8px;border-radius:8px;margin-bottom:8px;'>🎯 {sp['ability']}</div>
                    <div style='color:#FFD600;font-weight:900;font-size:0.9rem;'>{format_korean_money(sp['price'])}</div>
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

    # ══════════════════════════════════════════════════════════════
    # PET MAIN SCREEN
    # ══════════════════════════════════════════════════════════════
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

    new_ach = check_and_award_achievements(pet)
    if new_ach:
        save_pet(uid, pet)
        for ach_id in new_ach:
            ach_data = next((a for a in PET_ACHIEVEMENTS if a['id']==ach_id), None)
            if ach_data:
                st.toast(f"🏆 업적 달성: {ach_data['icon']} {ach_data['name']}!", icon="🎉")

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
                if got_rare: add_journal(pet, f"🎁 희귀 아이템 획득: {rare_name}!")
                save_pet(uid, pet); sync_user_data()
                log_tx(uid, "펫", f"{pet['name']} 탐험 보상 ({zone.get('name','')})", cash_r)
                del st.session_state['expedition_returned']
                st.toast(f"🗺️ EXP +{gained_exp} | 💰 +{format_korean_money(cash_r)}", icon="✅")
                if got_rare: st.toast(f"✨ 희귀 아이템: {rare_name}!", icon="🎁")
                if lvup: st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                st.rerun()

    # ── 애니메이션 펫 카드
    components.html(
        generate_pet_card_html(pet, sp, lv, exp_pct, hunger, happy, hp),
        height=470
    )

    # 스탯 바
    stat_cols = st.columns(5)
    stat_data = [
        ("⚡ Lv.", str(lv),                "#FFD600"),
        ("🧬 EXP", f"{exp}/{EXP_PER_LEVEL}", "#00E5FF"),
        ("💕 유대", get_bond_title(bond_lv),  "#FF6699"),
        ("🌡️ 기분", f"{mood_data['emoji']} {mood_name}", mood_data['color']),
        ("💰 패시브", format_korean_money(passive)+"/h" if passive>0 else "Lv.20~", "#00FF88"),
    ]
    for i,(lbl,val,col) in enumerate(stat_data):
        with stat_cols[i]:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                        border-radius:12px;padding:10px;text-align:center;'>
                <div style='color:#64748B;font-size:0.7rem;'>{lbl}</div>
                <div style='color:{col};font-weight:900;font-size:0.83rem;margin-top:3px;'>{val}</div>
            </div>
            """, unsafe_allow_html=True)

    if hunger < 20: st.warning(f"⚠️ {pet['name']}이(가) 너무 배가 고파요! 밥을 줘야해요!")
    if happy  < 20: st.warning(f"😢 {pet['name']}이(가) 너무 슬퍼해요! 같이 놀아주세요!")
    if hp     < 30: st.error(f"💀 {pet['name']}의 HP가 위험해요! 먹이를 주세요!")
    st.write("")

    # ── TABS
    tabs = st.tabs(["🍖 먹이주기","🎮 훈련","🗺️ 탐험","⚔️ 배틀","👗 아이템","📜 스킬","🏆 업적","📖 일지","📊 정보"])

    # ── TAB 1: 먹이주기
    with tabs[0]:
        st.markdown('<div class="pet-tab-header">🍖 먹이 선택</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="pet-sub">{pet["name"]}에게 맛있는 먹이를 줘보세요! 밥을 주면 행복해서 애교를 부려요 💕</div>', unsafe_allow_html=True)
        food_cols = st.columns(3)
        for i, (f_id, food) in enumerate(PET_FOOD.items()):
            with food_cols[i % 3]:
                can_afford = st.session_state.global_cash >= food['price']
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;{"opacity:0.5;" if not can_afford else ""}'>
                    <div style='font-size:3rem;margin-bottom:6px;'>{food['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:800;font-size:0.92rem;'>{food['name']}</div>
                    <div style='color:#64748B;font-size:0.72rem;margin:6px 0;'>
                        ✨ EXP +{food['exp']} &nbsp; 💕 행복 +{food['happiness']} &nbsp; 🍖 허기 +{food['hunger_restore']}
                    </div>
                    <div style='color:#FFD600;font-weight:900;font-size:0.95rem;'>{format_korean_money(food['price'])}</div>
                    <div style='color:{sp["accent"]};font-size:0.72rem;margin-top:4px;font-style:italic;'>
                        먹이면: "{food['reaction']}"
                    </div>
                </div>
                """, unsafe_allow_html=True)
                qty = st.number_input("수량", min_value=1, max_value=50, value=1, key=f"food_qty_{f_id}")
                if st.button(f"{food['icon']} 먹이기 ×{qty}", key=f"feed_{f_id}", use_container_width=True, disabled=not can_afford):
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
                        add_journal(pet, f"🍖 {food['name']}×{qty} 먹임! {food['reaction']} EXP+{gained_exp}")
                        save_pet(uid, pet); sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} 먹이({food['name']}×{qty})", -total_cost)
                        st.toast(f"😋 {food['reaction']} EXP +{gained_exp}", icon="🍖")
                        if leveled_up:
                            st.balloons()
                            st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
                        st.rerun()

    # ── TAB 2: 훈련
    with tabs[1]:
        st.markdown('<div class="pet-tab-header">🎮 훈련 & 같이 놀기</div>', unsafe_allow_html=True)
        st.markdown('<div class="pet-sub">훈련으로 EXP를 올리고, 같이 놀아주면 행복해요!</div>', unsafe_allow_html=True)
        train_cols = st.columns(3)
        for i, tg in enumerate(TRAINING_GAMES):
            with train_cols[i % 3]:
                st.markdown(f"""
                <div class='pet-card'>
                    <div style='display:flex;align-items:center;gap:10px;'>
                        <div style='font-size:2.2rem;'>{tg['icon']}</div>
                        <div>
                            <div style='font-weight:900;color:#E2E8F0;font-size:0.9rem;'>{tg['name']}</div>
                            <div style='color:#64748B;font-size:0.75rem;'>{tg['desc']}</div>
                            <div style='color:#FFD600;font-size:0.75rem;font-weight:700;margin-top:3px;'>
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
                        st.error("행복도가 너무 낮아요! 먼저 밥을 주세요 🍖")
                    else:
                        st.session_state.global_cash -= tg['cost']
                        atomic_deduct_cash(uid, tg['cost'])
                        roll = random.uniform(0.75, 1.35)
                        exp_got = int(tg['exp_reward'] * roll)
                        pet['happiness']   = max(0, pet.get('happiness',100) - 5)
                        pet['last_played'] = time.time()
                        pet['bond']        = pet.get('bond',0) + 2
                        pet, leveled_up, gained_exp = add_exp(pet, exp_got)
                        result = "🌟 대성공!" if roll>=1.25 else "✅ 성공!" if roll>=0.95 else "😅 아쉬운 결과"
                        add_journal(pet, f"🎮 {tg['name']} {result} EXP+{gained_exp}")
                        save_pet(uid, pet); sync_user_data()
                        log_tx(uid, "펫", f"{pet['name']} {tg['name']}", -tg['cost'])
                        st.toast(f"{result} EXP +{gained_exp}", icon="💪")
                        if leveled_up: st.balloons(); st.toast(f"🎉 레벨업! Lv.{pet['level']}!", icon="⬆️")
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
                pe = random.randint(5,15); ph = random.randint(15,35)
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
            remain_h = int(remain_s // 3600); remain_m = int((remain_s % 3600) // 60)
            st.markdown(f"""
            <div style='background:rgba(0,229,255,0.05);border:1px solid #00E5FF33;border-radius:16px;padding:24px;text-align:center;'>
                <div style='font-size:3rem;margin-bottom:8px;'>{z.get("icon","🗺️")}</div>
                <div style='color:#00E5FF;font-size:1.1rem;font-weight:900;'>{z.get("name","탐험")} 진행 중</div>
                <div style='color:#94A3B8;margin-top:10px;'>
                    ⏳ 귀환까지 <span style='color:#FFD600;font-weight:900;'>{remain_h}시간 {remain_m}분</span> 남음
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            exp_cols = st.columns(3)
            for i, (z_id, z) in enumerate(EXPEDITION_ZONES.items()):
                locked = lv < z['min_lv']
                with exp_cols[i % 3]:
                    st.markdown(f"""
                    <div class='pet-card' style='text-align:center;{"opacity:0.4;" if locked else ""}'>
                        <div style='font-size:2.2rem;'>{z['icon']}</div>
                        <div style='color:#E2E8F0;font-weight:900;margin-top:6px;'>{z['name']}</div>
                        <div style='color:#64748B;font-size:0.73rem;margin-top:4px;'>{z['desc']}</div>
                        <div style='margin-top:8px;'>
                            <span class='stat-chip' style='background:rgba(255,214,0,0.1);color:#FFD600;'>⏱️ {z['duration_h']}h</span>
                            <span class='stat-chip' style='background:rgba(0,229,255,0.1);color:#00E5FF;'>Lv.{z['min_lv']}+</span>
                        </div>
                        <div style='color:#64748B;font-size:0.7rem;margin-top:6px;'>💡 {z['rare_item']} 획득 가능</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if locked:
                        st.button(f"🔒 Lv.{z['min_lv']} 필요", key=f"exp_{z_id}", disabled=True, use_container_width=True)
                    else:
                        if st.button("🗺️ 탐험 출발!", key=f"exp_{z_id}", use_container_width=True):
                            pet['expedition'] = {'zone': z_id,'start_time': time.time(),'return_time': time.time() + z['duration_h']*3600}
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
            <div style='color:#E2E8F0;font-weight:900;margin-bottom:8px;'>{pet['name']}의 능력치</div>
            <div>
                <span class='stat-chip' style='background:rgba(255,75,75,0.15);color:#FF4B4B;'>⚔️ ATK {pet_stats["atk"]}</span>
                <span class='stat-chip' style='background:rgba(0,229,255,0.12);color:#00E5FF;'>🛡️ DEF {pet_stats["def"]}</span>
                <span class='stat-chip' style='background:rgba(0,255,136,0.12);color:#00FF88;'>💨 SPD {pet_stats["spd"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
                        <div style='font-size:2.2rem;'>{mob['icon']}</div>
                        <div style='color:#E2E8F0;font-weight:900;margin-top:4px;'>{mob['name']}</div>
                        <div style='margin-top:6px;'>
                            <span class='stat-chip' style='background:rgba(255,75,75,0.12);color:#FF4B4B;'>❤️{mob['hp']}</span>
                            <span class='stat-chip' style='background:rgba(255,0,0,0.1);color:#FF6B6B;'>⚔️{mob['atk']}</span>
                            <span class='stat-chip' style='background:rgba(0,229,255,0.1);color:#00E5FF;'>🛡️{mob['def']}</span>
                        </div>
                        <div style='color:#00FF88;font-size:0.73rem;margin-top:6px;'>
                            보상: EXP+{mob['reward_exp']} · {format_korean_money(mob['reward_cash'])}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("⚔️ 도전!", key=f"battle_{i}", use_container_width=True):
                        st.session_state.battle_state = {
                            'monster': mob.copy(),'pet_hp': min(pet.get('hp',100),100),
                            'monster_hp': mob['hp'],'log': [f"⚔️ {pet['name']} VS {mob['name']} 배틀 시작!"],
                            'turn': 1,'over': False,'won': False
                        }
                        st.rerun()
        else:
            mob = bs['monster']; pet_hp = bs['pet_hp']; mob_hp = bs['monster_hp']
            b1, b2, b3 = st.columns([2,1,2])
            with b1:
                pct_p = max(0, int(pet_hp))
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2rem;'>{sp.get("accent","✨")}</div>
                    <div style='color:#E2E8F0;font-weight:900;'>{pet['name']}</div>
                    <div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;'>
                        <div style='background:#00FF88;width:{pct_p}%;height:100%;border-radius:4px;'></div>
                    </div>
                    <div style='color:#00FF88;font-size:0.85rem;margin-top:4px;'>{pet_hp}/100 HP</div>
                </div>
                """, unsafe_allow_html=True)
            with b2:
                st.markdown(f"""
                <div style='text-align:center;padding:20px 0;'>
                    <div style='font-size:2rem;'>⚔️</div>
                    <div style='color:#FFD600;font-weight:900;margin-top:8px;'>TURN {bs['turn']}</div>
                </div>
                """, unsafe_allow_html=True)
            with b3:
                pct_m = max(0, int(mob_hp/mob['hp']*100))
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;'>
                    <div style='font-size:2rem;'>{mob['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:900;'>{mob['name']}</div>
                    <div style='margin-top:8px;background:rgba(255,255,255,0.08);border-radius:4px;height:8px;'>
                        <div style='background:#FF4B4B;width:{pct_m}%;height:100%;border-radius:4px;'></div>
                    </div>
                    <div style='color:#FF4B4B;font-size:0.85rem;margin-top:4px;'>{mob_hp}/{mob["hp"]} HP</div>
                </div>
                """, unsafe_allow_html=True)

            for log_line in bs['log'][-6:]:
                st.markdown(f"<div style='color:#94A3B8;font-size:0.82rem;padding:2px 0;'>▸ {log_line}</div>", unsafe_allow_html=True)

            if bs['over']:
                if bs['won']: st.success(f"🏆 승리! EXP +{mob['reward_exp']} · 💰 +{format_korean_money(mob['reward_cash'])}")
                else: st.error(f"💀 패배... {pet['name']}이(가) 쓰러졌어요.")
                if st.button("🔄 배틀 종료", use_container_width=True, key="battle_end"):
                    if bs['won']:
                        pet, lvup, ge = add_exp(pet, mob['reward_exp'])
                        atomic_add_cash(uid, mob['reward_cash'])
                        st.session_state.global_cash += mob['reward_cash']
                        pet['battles_won'] = pet.get('battles_won',0) + 1
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        pet['bond'] = pet.get('bond',0) + 3
                        add_journal(pet, f"⚔️ {mob['name']} 격파! EXP+{ge} 💰+{format_korean_money(mob['reward_cash'])}")
                        log_tx(uid,"펫",f"{pet['name']} 배틀승 vs {mob['name']}",mob['reward_cash'])
                        save_pet(uid, pet); sync_user_data()
                    else:
                        pet['battles_total'] = pet.get('battles_total',0) + 1
                        pet['hp'] = max(1, pet.get('hp',100) - 20)
                        add_journal(pet, f"⚔️ {mob['name']}에게 패배... HP -20")
                        save_pet(uid, pet)
                    st.session_state.battle_state = None; st.rerun()
            else:
                ca, cb, cc = st.columns(3)
                with ca:
                    if st.button("⚔️ 일반 공격", use_container_width=True, key="atk_normal"):
                        dmg_p = max(0, pet_stats['atk'] - mob['def'] + random.randint(-5,8))
                        dmg_m = max(0, mob['atk'] - pet_stats['def'] + random.randint(-3,6))
                        bs['monster_hp'] -= dmg_p; bs['pet_hp'] -= dmg_m
                        bs['log'].append(f"💥 {pet['name']} → {mob['name']}: -{dmg_p}HP")
                        bs['log'].append(f"🩸 {mob['name']} → {pet['name']}: -{dmg_m}HP")
                        bs['turn'] += 1
                        if bs['monster_hp'] <= 0: bs['over']=True; bs['won']=True
                        elif bs['pet_hp'] <= 0: bs['over']=True; bs['won']=False
                        st.rerun()
                with cb:
                    if st.button("🔥 강공격 (HP-10)", use_container_width=True, key="atk_heavy"):
                        dmg_p = max(0, int(pet_stats['atk']*1.8) - mob['def'] + random.randint(-4,12))
                        dmg_m = max(0, mob['atk'] - pet_stats['def'] + random.randint(-2,5))
                        bs['pet_hp'] -= 10; bs['monster_hp'] -= dmg_p; bs['pet_hp'] -= dmg_m
                        bs['log'].append(f"💥💥 강공격! {mob['name']}: -{dmg_p}HP (자상-10HP)")
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
                        bs['turn'] += 1; st.rerun()

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
                <div class='pet-card' style='text-align:center;{"border-color:#00E5FF;background:rgba(0,229,255,0.05);" if is_eq else ""}'>
                    <div style='font-size:2.5rem;'>{acc['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:6px;'>{acc['name']}</div>
                    <div style='color:#00FF88;font-size:0.78rem;margin-top:4px;'>{acc['desc']}</div>
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
                <div class='pet-card' style='text-align:center;{"border-color:#00E5FF;background:rgba(0,229,255,0.06);" if unlocked else "opacity:0.4;"}'>
                    <div style='font-size:1.8rem;'>{skill['icon']}</div>
                    <div style='color:#E2E8F0;font-size:0.8rem;font-weight:700;margin-top:5px;'>{skill['name']}</div>
                    <div style='color:#64748B;font-size:0.68rem;margin-top:3px;'>{skill['desc']}</div>
                    <div style='color:{"#FFD600" if unlocked else "#475569"};font-size:0.7rem;margin-top:5px;font-weight:700;'>
                        {"✅ 해금" if unlocked else f"🔒 Lv.{skill['level']}"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 7: 업적
    with tabs[6]:
        st.markdown('<div class="pet-tab-header">🏆 펫 업적</div>', unsafe_allow_html=True)
        earned_ids = pet.get('achievements',[])
        earned_count = len(earned_ids); total_count = len(PET_ACHIEVEMENTS)
        st.markdown(f"""
        <div style='background:rgba(255,214,0,0.05);border:1px solid #FFD60022;border-radius:12px;padding:14px;margin-bottom:16px;text-align:center;'>
            <div style='color:#FFD600;font-size:1.4rem;font-weight:900;'>{earned_count}/{total_count}</div>
            <div style='color:#94A3B8;font-size:0.83rem;margin-top:3px;'>업적 달성</div>
            <div style='background:rgba(255,255,255,0.07);border-radius:4px;height:6px;margin-top:10px;overflow:hidden;'>
                <div style='background:#FFD600;width:{int(earned_count/max(total_count,1)*100)}%;height:100%;border-radius:4px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        ach_cols = st.columns(3)
        for i, ach in enumerate(PET_ACHIEVEMENTS):
            has = ach['id'] in earned_ids
            with ach_cols[i%3]:
                st.markdown(f"""
                <div class='pet-card' style='text-align:center;{"border-color:#FFD600;background:rgba(255,214,0,0.05);" if has else "opacity:0.45;"}'>
                    <div style='font-size:2rem;'>{ach['icon']}</div>
                    <div style='color:#E2E8F0;font-weight:700;margin-top:5px;font-size:0.88rem;'>{ach['name']}</div>
                    <div style='color:#64748B;font-size:0.73rem;margin-top:3px;'>{ach['desc']}</div>
                    <div style='color:{"#FFD600" if has else "#475569"};font-size:0.73rem;margin-top:5px;font-weight:700;'>
                        {"✅ 달성!" if has else "🔒 미달성"}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 8: 일지
    with tabs[7]:
        st.markdown('<div class="pet-tab-header">📖 펫 일지</div>', unsafe_allow_html=True)
        journal = pet.get('journal', [])
        if not journal:
            st.markdown("<div style='text-align:center;color:#475569;padding:30px;'>아직 기록이 없어요!</div>", unsafe_allow_html=True)
        else:
            for entry in journal[:30]:
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.02);border-left:2px solid {sp["accent"]}44;
                            padding:8px 14px;margin-bottom:5px;border-radius:0 8px 8px 0;
                            color:#94A3B8;font-size:0.82rem;'>
                    {entry}
                </div>
                """, unsafe_allow_html=True)

    # ── TAB 9: 정보
    with tabs[8]:
        st.markdown('<div class="pet-tab-header">📊 펫 상세 정보</div>', unsafe_allow_html=True)
        equipped_list = pet.get('accessories',[])
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
            ("👗 장착 악세서리", ", ".join(PET_ACCESSORIES[a]['name'] for a in equipped_list if a in PET_ACCESSORIES) or "없음"),
            ("📜 보유 스킬",  ", ".join(pet.get('skills',[])) or "없음"),
            ("🏆 달성 업적",  f"{len(pet.get('achievements',[]))}/{len(PET_ACHIEVEMENTS)}"),
        ]
        for label, val in info_rows:
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;padding:10px 0;
                        border-bottom:1px solid rgba(255,255,255,0.04);'>
                <span style='color:#64748B;'>{label}</span>
                <span style='color:#E2E8F0;font-weight:700;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style='margin-top:16px;background:rgba(255,255,255,0.03);border:1px solid {sp["accent"]}33;
                    border-radius:12px;padding:14px;'>
            <div style='color:{sp["accent"]};font-weight:900;margin-bottom:6px;'>🎯 종족 고유 능력</div>
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
                save_pet(uid, default_pet()); sync_user_data()
                log_tx(uid,"펫",f"{pet['name']} 분양",release_price)
                del st.session_state['confirm_release']
                st.toast(f"💔 {pet['name']}이(가) 떠났어요...", icon="🐾")
                st.rerun()
            if cc2.button("❌ 취소", use_container_width=True, key="confirm_no"):
                del st.session_state['confirm_release']
                st.rerun()
