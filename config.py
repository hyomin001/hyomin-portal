# ==============================
# 시스템 설정 및 데이터베이스 경로
# ==============================
USERS_FILE    = "users_db.json"
COMMENTS_FILE = "comments_db.json"
MARKET_FILE   = "market_db.json"
TXLOG_FILE    = "txlog_db.json"

stock_config = [
    {"id": "NDX",    "name": "나스닥100 ETF",       "vol": 0.04, "icon": "🇺🇸"},
    {"id": "HDEC",   "name": "현대건설",             "vol": 0.03, "icon": "🏗️"},
    {"id": "MANU",   "name": "맨체스터 유나이티드",  "vol": 0.06, "icon": "⚽"},
    {"id": "CJENM",  "name": "CJ ENM",               "vol": 0.04, "icon": "🎬"},
    {"id": "FOOD",   "name": "삼양식품",              "vol": 0.03, "icon": "🍜"},
    {"id": "BIO",    "name": "삼성바이오로직스",      "vol": 0.05, "icon": "🧬"},
    {"id": "AERO",   "name": "한화에어로스페이스",    "vol": 0.06, "icon": "🚀"},
    {"id": "RETAIL", "name": "신세계",                "vol": 0.02, "icon": "🛍️"},
    {"id": "CHEM",   "name": "LG화학",                "vol": 0.03, "icon": "⚗️"},
    {"id": "ENTER",  "name": "하이브",                "vol": 0.07, "icon": "🎵"},
]

estate_config = {
    "E1": {"name": "역세권 원룸",       "icon": "🏠", "price": 10_000_000_000,    "income": 10_000,   "desc": "지하철 2분 거리 황금 입지"},
    "E2": {"name": "초대형 PC방",        "icon": "🖥️", "price": 50_000_000_000,   "income": 50_000,   "desc": "e스포츠 성지, 24시간 풀가동"},
    "E3": {"name": "강남 꼬마빌딩",      "icon": "🏢", "price": 500_000_000_000,  "income": 500_000,  "desc": "강남 핵심 상권 4층 빌딩"},
    "E4": {"name": "시그니엘 펜트하우스","icon": "👑", "price": 5_000_000_000_000,"income": 5_000_000,"desc": "롯데월드타워 최상층 전망"},
}

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
