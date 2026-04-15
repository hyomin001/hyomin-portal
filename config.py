# ============================================================
# config.py — HYOMIN UNIVERSE 전체 상수 및 게임 설정
# ============================================================

# ── 파일 경로 ──
USERS_FILE            = "users_db.json"
COMMENTS_FILE         = "comments_db.json"
MARKET_FILE           = "market_db.json"
TXLOG_FILE            = "txlog_db.json"
REALESTATE_MARKET_FILE= "realestate_market_db.json"
CLAN_FILE             = "clan_db.json"
MESSAGES_FILE         = "messages_db.json"
CLAN_CHATS_FILE       = "clan_chats_db.json"

# ── 보안 ──
import hashlib
ADMIN_HASH = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

# ── 주식 설정 ──
STOCK_CONFIG = [
    {"id": "NDX",    "name": "나스닥100 ETF",       "vol": 0.04, "icon": "🇺🇸"},
    {"id": "HDEC",   "name": "현대건설",             "vol": 0.03, "icon": "🏗️"},
    {"id": "MANU",   "name": "맨체스터 유나이티드",  "vol": 0.04, "icon": "⚽"},
    {"id": "CJENM",  "name": "CJ ENM",               "vol": 0.04, "icon": "🎬"},
    {"id": "FOOD",   "name": "삼양식품",             "vol": 0.03, "icon": "🍜"},
    {"id": "BIO",    "name": "삼성바이오로직스",      "vol": 0.05, "icon": "🧬"},
    {"id": "AERO",   "name": "한화에어로스페이스",    "vol": 0.06, "icon": "🚀"},
    {"id": "RETAIL", "name": "신세계",               "vol": 0.02, "icon": "🛍️"},
    {"id": "CHEM",   "name": "LG화학",               "vol": 0.03, "icon": "⚗️"},
    {"id": "ENTER",  "name": "하이브",               "vol": 0.07, "icon": "🎵"},
]

# ── 부동산 설정 ──
ESTATE_CONFIG = {
    "E1":  {"name": "역세권 원룸",          "icon": "🏠",  "base_price": 10_000_000_000,    "income": 8_000,     "desc": "지하철 2분 거리 황금 입지",          "total_supply": 20},
    "E2":  {"name": "초대형 PC방",           "icon": "🖥️",  "base_price": 50_000_000_000,    "income": 45_000,    "desc": "e스포츠 성지, 24시간 풀가동",        "total_supply": 10},
    "E3":  {"name": "강남 꼬마빌딩",         "icon": "🏢",  "base_price": 500_000_000_000,   "income": 450_000,   "desc": "강남 핵심 상권 4층 빌딩",             "total_supply": 6},
    "E4":  {"name": "시그니엘 펜트하우스",   "icon": "👑",  "base_price": 5_000_000_000_000, "income": 4_500_000, "desc": "롯데월드타워 최상층 전망",            "total_supply": 3},
    "E5":  {"name": "제주 풀빌라",           "icon": "🌴",  "base_price": 30_000_000_000,    "income": 25_000,    "desc": "성산일출봉 전망 프리미엄 풀빌라",    "total_supply": 8},
    "E6":  {"name": "홍대 상가건물",         "icon": "🎸",  "base_price": 200_000_000_000,   "income": 180_000,   "desc": "홍대 메인 스트리트 5층 상가",        "total_supply": 8},
    "E7":  {"name": "판교 오피스타워",       "icon": "💻",  "base_price": 800_000_000_000,   "income": 750_000,   "desc": "IT 기업 밀집 A급 오피스",             "total_supply": 8},
    "E8":  {"name": "해운대 호텔",           "icon": "🏖️",  "base_price": 2_000_000_000_000, "income": 2_000_000, "desc": "부산 해운대 특급 호텔 1동",          "total_supply": 20},
    "E9":  {"name": "용산 임대아파트 단지",  "icon": "🏘️",  "base_price": 1_000_000_000_000, "income": 900_000,   "desc": "용산 재개발 신축 100세대 단지",      "total_supply": 10},
    "E10": {"name": "인천공항 면세점",       "icon": "✈️",  "base_price": 3_000_000_000_000, "income": 3_500_000, "desc": "인천공항 1터미널 황금 면세점",       "total_supply": 5},
}

# ── 광산 아이템 ──
MINE_ITEMS = [
    {"name": "돌멩이",     "icon": "🪨", "value": 10_000,     "prob": 0.40},
    {"name": "구리광석",   "icon": "🟤", "value": 50_000,     "prob": 0.25},
    {"name": "은광석",     "icon": "⚪", "value": 200_000,    "prob": 0.15},
    {"name": "금광석",     "icon": "🟡", "value": 500_000,    "prob": 0.10},
    {"name": "루비",       "icon": "🔴", "value": 1_000_000,  "prob": 0.05},
    {"name": "사파이어",   "icon": "🔵", "value": 3_000_000,  "prob": 0.03},
    {"name": "다이아몬드", "icon": "💎", "value": 10_000_000, "prob": 0.015},
    {"name": "전설의 원석","icon": "🌟", "value": 100_000_000,"prob": 0.005},
]

# ── 코인 설정 ──
CRYPTO_CONFIG = [
    {"id": "BTC",  "name": "비트코인",  "vol": 0.12, "icon": "₿",  "base_price": 130_000_000},
    {"id": "ETH",  "name": "이더리움",  "vol": 0.10, "icon": "Ξ",  "base_price": 6_000_000},
    {"id": "SOL",  "name": "솔라나",    "vol": 0.15, "icon": "◎",  "base_price": 300_000},
    {"id": "DOGE", "name": "도지코인",  "vol": 0.22, "icon": "🐶", "base_price": 500},
    {"id": "PEPE", "name": "페페코인",  "vol": 0.35, "icon": "🐸", "base_price": 10},
    {"id": "HYO",  "name": "효민코인",  "vol": 0.28, "icon": "🌌", "base_price": 1_000_000},
]

# ── 가챠 풀 ──
GACHA_TICKET_PRICE = 50_000_000
GACHA_POOL = [
    {"grade": "💎 전설", "name": "👑 [시즌한정] 우주의 도박꾼",      "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 운영자를 노린다",      "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 갓생러",              "weight": 2,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 전설",                "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 돈복사 의혹자",       "weight": 1,  "type": "title"},
    {"grade": "💎 전설", "name": "👑 [시즌한정] 서버 경제 붕괴자",    "weight": 1,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 전장의 지배자",                 "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 억만장자의 품격",                "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 코인왕",                        "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 부동산 재벌",                   "weight": 4,  "type": "title"},
    {"grade": "🔴 영웅", "name": "⚔️ 주식의 신",                     "weight": 4,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 행운의 사나이",                 "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 억세게 운 좋은 놈",             "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 가챠 중독자",                   "weight": 10, "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 슬롯머신 애호가",               "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 광산의 제왕",                   "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 레이싱 황제",                   "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 블랙잭 고수",                   "weight": 8,  "type": "title"},
    {"grade": "🔵 희귀", "name": "🎖️ 로또 상습 구매자",              "weight": 8,  "type": "title"},
    {"grade": "🟢 일반", "name": "🍀 행운의 클로버",                  "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🌟 떠오르는 별",                    "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "💫 시민 모험가",                    "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🌈 평범한 시민",                    "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🐣 뉴비",                          "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🦆 그냥 오리",                      "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🍞 평범한 빵",                      "weight": 25, "type": "title"},
    {"grade": "🟢 일반", "name": "🐌 느릿느릿 투자자",               "weight": 25, "type": "title"},
    {"grade": "🟤 꽝",   "name": "파괴방지권",                        "weight": 30, "type": "item"},
    {"grade": "🟤 꽝",   "name": "빈 깡통",                           "weight": 30, "type": "item"},
]

# ── 명검 강화 데이터 ──
FORGE_DATA = {
    0:  {"rate": 1.0,     "cost": 10_000_000,        "sell": 0,                "name": "🪵 평범한 나무검",          "color": "#aaa"},
    1:  {"rate": 1.0,     "cost": 20_000_000,        "sell": 5_000_000,        "name": "🗡️ 강철 장검 +1",           "color": "#ddd"},
    2:  {"rate": 0.95,    "cost": 50_000_000,        "sell": 20_000_000,       "name": "🗡️ 강철 장검 +2",           "color": "#ddd"},
    3:  {"rate": 0.90,    "cost": 100_000_000,       "sell": 100_000_000,      "name": "🗡️ 강철 장검 +3",           "color": "#ddd"},
    4:  {"rate": 0.85,    "cost": 300_000_000,       "sell": 300_000_000,      "name": "🗡️ 정예 기사의 검 +4",      "color": "#00E5FF"},
    5:  {"rate": 0.70,    "cost": 1_000_000_000,     "sell": 1_500_000_000,    "name": "⚔️ 은빛 대검 +5",           "color": "#00FF88"},
    6:  {"rate": 0.65,    "cost": 3_000_000_000,     "sell": 5_000_000_000,    "name": "⚔️ 은빛 대검 +6",           "color": "#00FF88"},
    7:  {"rate": 0.55,    "cost": 8_000_000_000,     "sell": 15_000_000_000,   "name": "🔥 타오르는 흑염검 +7",     "color": "#FF8800"},
    8:  {"rate": 0.50,    "cost": 20_000_000_000,    "sell": 40_000_000_000,   "name": "🔥 타오르는 흑염검 +8",     "color": "#FF8800"},
    9:  {"rate": 0.45,    "cost": 50_000_000_000,    "sell": 150_000_000_000,  "name": "🩸 마왕의 재림 +9",         "color": "#FF4B4B"},
    10: {"rate": 0.20,    "cost": 100_000_000_000,   "sell": 500_000_000_000,  "name": "⚡ 영웅의 성검 +10",        "color": "#FFD600"},
    11: {"rate": 0.10,    "cost": 300_000_000_000,   "sell": 1_500_000_000_000,"name": "⚡ 영웅의 성검 +11",        "color": "#FFD600"},
    12: {"rate": 0.05,    "cost": 800_000_000_000,   "sell": 5_000_000_000_000,"name": "🌌 우주의 지배자 +12",      "color": "#FF00FF"},
    13: {"rate": 0.02,    "cost": 2_000_000_000_000, "sell": 20_000_000_000_000,"name": "🌌 우주의 지배자 +13",     "color": "#FF00FF"},
    14: {"rate": 0.005,   "cost": 5_000_000_000_000, "sell": 100_000_000_000_000,"name": "🌌 우주의 지배자 +14",    "color": "#FF00FF"},
    15: {"rate": 0.00001, "cost": 0,                 "sell": 500_000_000_000_000,"name": "👑 [신화] 엑스칼리버 +15","color": "#FFFFFF"},
}

# ── 일일 퀘스트 ──
DAILY_QUESTS_CONFIG = [
    {"id": "attendance", "icon": "📅", "name": "출석 체크",        "desc": "오늘 로그인 완료",                  "reward": 10_000_000},
    {"id": "rich5",      "icon": "💰", "name": "중산층 인증",       "desc": "순자산 5억 이상 달성",              "reward": 30_000_000},
    {"id": "landlord",   "icon": "🏠", "name": "건물주 인증",       "desc": "부동산 1채 이상 보유",              "reward": 20_000_000},
    {"id": "investor",   "icon": "📈", "name": "포트폴리오 투자자", "desc": "주식 평가액 1억 이상 보유",         "reward": 25_000_000},
    {"id": "coin100m",   "icon": "🪙", "name": "코인 홀더",         "desc": "코인 총 평가액 1억 이상 보유",      "reward": 20_000_000},
    {"id": "debtfree",   "icon": "🕊️", "name": "무대출 청렴인증",   "desc": "대출 잔액 0원 유지",                "reward": 15_000_000},
    {"id": "billionaire","icon": "👑", "name": "억만장자 인증",      "desc": "순자산 1000억 이상 달성",           "reward": 500_000_000},
]

# ── 차량 티어 ──
CAR_TIERS = [
    {"tier": "0", "name": "2021년형 컴팩트 박스카", "emoji": "🚙", "color": "#A0A0A0", "price": 10_000_000_000},
    {"tier": "1", "name": "터보차저 스포츠 세단",   "emoji": "🚗", "color": "#00E5FF", "price": 500_000_000_000},
    {"tier": "2", "name": "V12 럭셔리 하이퍼카",    "emoji": "🏎️", "color": "#FFD600", "price": 5_000_000_000_000},
    {"tier": "3", "name": "🌌 우주 뚫은 은하철도",  "emoji": "🚀", "color": "#FF00FF", "price": 50_000_000_000_000},
]

# ── 레이싱 차량 풀 ──
RACE_CARS = [
    {"name": "부가티 시론 SS",         "emoji": "🏎️", "odds": 20.0, "spd": (0, 15), "color": "#FF0066"},
    {"name": "람보르기니 레부엘토",     "emoji": "🐂",  "odds": 12.0, "spd": (1, 14), "color": "#FF6600"},
    {"name": "페라리 SF90 XX",          "emoji": "🐎",  "odds": 8.0,  "spd": (1, 13), "color": "#FF2200"},
    {"name": "맥라렌 P1 GTR",           "emoji": "🚀",  "odds": 6.0,  "spd": (2, 12), "color": "#FF9900"},
    {"name": "포르쉐 918 스파이더",     "emoji": "⚡",  "odds": 4.0,  "spd": (2, 11), "color": "#FFCC00"},
    {"name": "테슬라 로드스터 2",        "emoji": "⚡",  "odds": 2.5,  "spd": (3, 10), "color": "#00FF88"},
    {"name": "토요타 GR010 하이브리드", "emoji": "🏁",  "odds": 1.8,  "spd": (3,  9), "color": "#00CCFF"},
]

# ── 슬롯 설정 ──
SLOT_TIERS = [
    {"label": "🪙 일반 슬롯",  "cost": 1_000_000,   "jackpot": 30_000_000,    "jackpot_mult": 30, "prob": 0.10},
    {"label": "💰 골드 슬롯",  "cost": 10_000_000,  "jackpot": 500_000_000,   "jackpot_mult": 50, "prob": 0.08},
    {"label": "💎 다이아 슬롯","cost": 100_000_000, "jackpot": 5_000_000_000, "jackpot_mult": 50, "prob": 0.06},
]
SLOT_SYMBOLS = {"🍒": 0.35, "🍋": 0.25, "🔔": 0.18, "⭐": 0.12, "7️⃣": 0.07, "💎": 0.03}

# ── 메뉴 구조 ──
def build_menu(is_admin: bool, is_vip: bool) -> dict:
    menus = {
        "📈 경제": [
            "🏠 홈 광장 (튜토리얼)",
            "📈 주식 트레이딩",
            "🪙 코인 거래소",
            "🏢 부동산 거래소",
            "🏦 은행 (대출/송금)",
            "📜 내 거래 기록",
        ],
        "🎮 미니게임": [
            "🎰 럭키 슬롯",
            "🃏 블랙잭 카지노",
            "⛏️ 광산 (노가다)",
            "💻 정처기 CBT",
            "⚔️ 글로벌 로또",
            "🗡️ 전설의 명검 강화",
            "🎴 가챠 뽑기",
        ],
        "🌟 성장 & 혜택": [
            "📅 일일 퀘스트",
            "👑 칭호 상점",
        ],
        "⚽ 스포츠": [
            "⚽ 구단주 시뮬레이터",
            "⚽ 조기축구 승부차기",
            "🏎️ 하이퍼카 레이싱",
            "🛠️ 커스텀 튜닝 차고지",
        ],
        "👥 커뮤니티": [
            "🏰 길드/클랜",
            "🏅 [시즌2]랭킹 & 게시판",
            "✉️ 개인 쪽지함",
        ],
    }
    if is_vip:
        menus["📈 경제"].insert(1, "💎 VIP 라운지")
    if is_admin:
        menus["⚙️ 관리"] = ["🛠️ 창조주 통제소"]
    return menus
