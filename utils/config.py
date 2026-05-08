# utils/config.py
import os
from datetime import timedelta, timezone

# 🕒 서버 시간 강제 세팅 (KST)
os.environ['TZ'] = 'Asia/Seoul'
KST = timezone(timedelta(hours=9))

# 🌌 데이터베이스 파일명
USERS_FILE    = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE   = "market_db.json"
TXLOG_FILE    = "txlog_db.json"
REALESTATE_MARKET_FILE = "realestate_market_db.json"  
CLAN_FILE     = "clan_db.json"
MESSAGES_FILE = "messages_db.json"
STATS_FILE       = "stats_db.json"  # 👈 [통계 대시보드] 통계용 DB 파일 상수 추가!
LEADERBOARD_FILE = "leaderboard_db.json"  # 🏆 전역 명예의 전당 (A~I 전 게임 1위 기록)

# 📈 주식 설정
stock_config = [
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

# 🪙 코인 설정
CRYPTO_CONFIG = [
    {"id": "BTC",   "name": "비트코인",  "vol": 0.12, "icon": "₿",  "base_price": 130_000_000},
    {"id": "ETH",   "name": "이더리움",  "vol": 0.10, "icon": "Ξ",  "base_price": 6_000_000},
    {"id": "SOL",   "name": "솔라나",    "vol": 0.15, "icon": "◎",  "base_price": 300_000},
    {"id": "DOGE",  "name": "도지코인",  "vol": 0.22, "icon": "🐶", "base_price": 500},
    {"id": "PEPE",  "name": "페페코인",  "vol": 0.35, "icon": "🐸", "base_price": 10},
    {"id": "HYO",   "name": "효민코인",  "vol": 0.28, "icon": "🌌", "base_price": 1_000_000},
]

# 🏢 부동산 설정
estate_config = {
    "E1":  {"name": "역세권 원룸",          "icon": "🏠",  "base_price": 10_000_000_000,    "income": 8_000,     "desc": "지하철 2분 거리 황금 입지",          "total_supply": 20},
    "E2":  {"name": "초대형 PC방",            "icon": "🖥️",  "base_price": 50_000_000_000,    "income": 45_000,    "desc": "e스포츠 성지, 24시간 풀가동",        "total_supply": 10},
    "E3":  {"name": "강남 꼬마빌딩",          "icon": "🏢",  "base_price": 500_000_000_000,   "income": 450_000,   "desc": "강남 핵심 상권 4층 빌딩",              "total_supply": 6},
    "E4":  {"name": "시그니엘 펜트하우스",   "icon": "👑",  "base_price": 5_000_000_000_000, "income": 4_500_000, "desc": "롯데월드타워 최상층 전망",             "total_supply": 3},
    "E5":  {"name": "제주 풀빌라",            "icon": "🌴",  "base_price": 30_000_000_000,    "income": 25_000,    "desc": "성산일출봉 전망 프리미엄 풀빌라",    "total_supply": 8},
    "E6":  {"name": "홍대 상가건물",          "icon": "🎸",  "base_price": 200_000_000_000,   "income": 180_000,   "desc": "홍대 메인 스트리트 5층 상가",        "total_supply": 8},
    "E7":  {"name": "판교 오피스타워",        "icon": "💻",  "base_price": 800_000_000_000,   "income": 750_000,   "desc": "IT 기업 밀집 A급 오피스",              "total_supply": 8},
    "E8":  {"name": "해운대 호텔",            "icon": "🏖️",  "base_price": 2_000_000_000_000, "income": 2_000_000, "desc": "부산 해운대 특급 호텔 1동",          "total_supply": 20},
    "E9":  {"name": "용산 임대아파트 단지",  "icon": "🏘️",  "base_price": 1_000_000_000_000, "income": 900_000,   "desc": "용산 재개발 신축 100세대 단지",      "total_supply": 10},
    "E10": {"name": "인천공항 면세점",        "icon": "✈️",  "base_price": 3_000_000_000_000, "income": 3_500_000, "desc": "인천공항 1터미널 황금 면세점",       "total_supply": 5},
}

# ⛏️ 광산 아이템
MINE_ITEMS = [
    {"name": "돌멩이",      "icon": "🪨", "value": 10_000,      "prob": 0.40},
    {"name": "구리광석",    "icon": "🟤", "value": 50_000,      "prob": 0.25},
    {"name": "은광석",      "icon": "⚪", "value": 200_000,     "prob": 0.15},
    {"name": "금광석",      "icon": "🟡", "value": 500_000,     "prob": 0.10},
    {"name": "루비",        "icon": "🔴", "value": 1_000_000,  "prob": 0.05},
    {"name": "사파이어",    "icon": "🔵", "value": 3_000_000,  "prob": 0.03},
    {"name": "다이아몬드", "icon": "💎", "value": 10_000_000, "prob": 0.015},
    {"name": "전설의 원석","icon": "🌟", "value": 100_000_000,"prob": 0.005},
]

# 🗡️ 전설의 명검 강화 설정
FORGE_DATA = {
    0: {"rate": 1.0,  "cost": 10_000_000,    "sell": 0, "name": "🪵 평범한 나무검", "color": "#aaa"},
    1: {"rate": 1.0,  "cost": 20_000_000,    "sell": 5_000_000, "name": "🗡️ 강철 장검 +1", "color": "#ddd"},
    2: {"rate": 0.95, "cost": 50_000_000,    "sell": 20_000_000, "name": "🗡️ 강철 장검 +2", "color": "#ddd"},
    3: {"rate": 0.90, "cost": 100_000_000,   "sell": 100_000_000, "name": "🗡️ 강철 장검 +3", "color": "#ddd"},
    4: {"rate": 0.85, "cost": 300_000_000,   "sell": 300_000_000, "name": "🗡️ 정예 기사의 검 +4", "color": "#00E5FF"},
    5: {"rate": 0.70, "cost": 1_000_000_000,  "sell": 1_500_000_000, "name": "⚔️ 은빛 대검 +5", "color": "#00FF88"},
    6: {"rate": 0.65, "cost": 3_000_000_000,  "sell": 5_000_000_000, "name": "⚔️ 은빛 대검 +6", "color": "#00FF88"},
    7: {"rate": 0.55, "cost": 8_000_000_000,  "sell": 15_000_000_000, "name": "🔥 타오르는 흑염검 +7", "color": "#FF8800"},
    8: {"rate": 0.50, "cost": 20_000_000_000, "sell": 40_000_000_000, "name": "🔥 타오르는 흑염검 +8", "color": "#FF8800"},
    9: {"rate": 0.45, "cost": 50_000_000_000, "sell": 150_000_000_000, "name": "🩸 마왕의 재림 +9", "color": "#FF4B4B"},
    10: {"rate": 0.20, "cost": 100_000_000_000, "sell": 500_000_000_000, "name": "⚡ 영웅의 성검 +10", "color": "#FFD600"},
    11: {"rate": 0.1, "cost": 300_000_000_000, "sell": 1_500_000_000_000, "name": "⚡ 영웅의 성검 +11", "color": "#FFD600"},
    12: {"rate": 0.05, "cost": 800_000_000_000, "sell": 5_000_000_000_000, "name": "🌌 우주의 지배자 +12", "color": "#FF00FF"},
    13: {"rate": 0.02, "cost": 2_000_000_000_000, "sell": 20_000_000_000_000, "name": "🌌 우주의 지배자 +13", "color": "#FF00FF"},
    14: {"rate": 0.005, "cost": 5_000_000_000_000, "sell": 100_000_000_000_000, "name": "🌌 우주의 지배자 +14", "color": "#FF00FF"},
    15: {"rate": 0.00001, "cost": 0, "sell": 500_000_000_000_000, "name": "👑 [신화] 엑스칼리버 +15", "color": "#FFFFFF"}
}

# 📅 일일 퀘스트 설정
DAILY_QUESTS_CONFIG = [
    {"id": "attendance", "icon": "📅", "name": "출석 체크",        "desc": "오늘 로그인 완료",                    "reward": 10_000_000},
    {"id": "rich5",      "icon": "💰", "name": "중산층 인증",      "desc": "순자산 5억 이상 달성",                "reward": 30_000_000},
    {"id": "landlord",   "icon": "🏠", "name": "건물주 인증",      "desc": "부동산 1채 이상 보유",                "reward": 20_000_000},
    {"id": "investor",   "icon": "📈", "name": "포트폴리오 투자자", "desc": "주식 평가액 1억 이상 보유",          "reward": 25_000_000},
    {"id": "coin100m",   "icon": "🪙", "name": "코인 홀더",        "desc": "코인 총 평가액 1억 이상 보유",        "reward": 20_000_000},
    {"id": "debtfree",   "icon": "🕊️", "name": "무대출 청렴인증",  "desc": "대출 잔액 0원 유지",                  "reward": 15_000_000},
    {"id": "billionaire","icon": "👑", "name": "억만장자 인증",     "desc": "순자산 1000억 이상 달성",             "reward": 500_000_000},
]
