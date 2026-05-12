# utils/config.py
import os
from datetime import timedelta, timezone, datetime

# 🕒 서버 시간 강제 세팅 (KST)
os.environ['TZ'] = 'Asia/Seoul'
KST = timezone(timedelta(hours=9))

# ══════════════════════════════════════════════════════════════
# 🏆 시즌 설정 — 시즌 번호·종료일은 market DB에서 읽어옴
#   config에는 "신규 시즌 기본 기간"만 보관
#   market['season_num']  : 현재 시즌 번호 (int)
#   market['season_end']  : 시즌 종료 unix timestamp (float)
#   market['season_start']: 시즌 시작 unix timestamp (float)
# ══════════════════════════════════════════════════════════════
SEASON_DURATION_DAYS = 30        # 시즌 기본 기간 (관리자가 패널에서 바꿀 수 있음)
NEXT_SEASON_DELAY    = 3600      # 시즌 종료 후 새 시즌 자동 시작까지 대기 (초, 1시간)
SEASON_RESET_GRACE   = 60        # 종료 판정 유예 (초) — 정확히 종료 시각에 동시 요청 충돌 방지

# ══════════════════════════════════════════════════════════════
# 🌌 데이터베이스 파일명
# ══════════════════════════════════════════════════════════════
USERS_FILE    = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE   = "market_db.json"
TXLOG_FILE    = "txlog_db.json"
REALESTATE_MARKET_FILE = "realestate_market_db.json"
CLAN_FILE     = "clan_db.json"
MESSAGES_FILE = "messages_db.json"
STATS_FILE       = "stats_db.json"
LEADERBOARD_FILE = "leaderboard_db.json"

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
}

# ⚔️ 강화 설정
FORGE_DATA = {
    1:  {"cost": 50_000_000,        "success": 90, "destroy": 0,  "sell": 100_000_000,       "name": "+1 수련생의 단검"},
    2:  {"cost": 150_000_000,       "success": 80, "destroy": 0,  "sell": 350_000_000,       "name": "+2 견습 기사의 검"},
    3:  {"cost": 400_000_000,       "success": 70, "destroy": 0,  "sell": 900_000_000,       "name": "+3 정예 기사의 장검"},
    4:  {"cost": 1_000_000_000,     "success": 60, "destroy": 5,  "sell": 2_500_000_000,     "name": "+4 엘리트 기사단장의 검"},
    5:  {"cost": 2_500_000_000,     "success": 50, "destroy": 8,  "sell": 7_000_000_000,     "name": "+5 왕국 근위대의 성검"},
    6:  {"cost": 6_000_000_000,     "success": 40, "destroy": 12, "sell": 18_000_000_000,    "name": "+6 드래곤슬레이어"},
    7:  {"cost": 15_000_000_000,    "success": 30, "destroy": 15, "sell": 45_000_000_000,    "name": "+7 고대 룬 마검"},
    8:  {"cost": 40_000_000_000,    "success": 22, "destroy": 18, "sell": 120_000_000_000,   "name": "+8 신화급 세계수 대검"},
    9:  {"cost": 100_000_000_000,   "success": 15, "destroy": 20, "sell": 300_000_000_000,   "name": "+9 천계의 심판자"},
    10: {"cost": 250_000_000_000,   "success": 10, "destroy": 25, "sell": 800_000_000_000,   "name": "+10 천공의 패왕검"},
    11: {"cost": 600_000_000_000,   "success": 7,  "destroy": 30, "sell": 2_000_000_000_000, "name": "+11 차원을 가르는 검"},
    12: {"cost": 1_500_000_000_000, "success": 5,  "destroy": 35, "sell": 5_000_000_000_000, "name": "+12 시공간 붕괴의 마검"},
    13: {"cost": 4_000_000_000_000, "success": 3,  "destroy": 40, "sell": 15_000_000_000_000,"name": "+13 우주를 삼킨 검"},
    14: {"cost": 10_000_000_000_000,"success": 2,  "destroy": 45, "sell": 40_000_000_000_000,"name": "+14 신도 두려워하는 검"},
    15: {"cost": 30_000_000_000_000,"success": 1,  "destroy": 50, "sell": 100_000_000_000_000,"name": "+15 엑스칼리버 진"},
}
