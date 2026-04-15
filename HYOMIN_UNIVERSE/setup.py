import os

# 생성할 폴더 목록
folders = [
    "utils", 
    "pages", "pages/games", "pages/sports", "pages/admin"
]

# 생성할 파일 목록
files = [
    "app.py",
    "utils/__init__.py", "utils/css.py", "utils/database.py", "utils/config.py",
    "pages/__init__.py", "pages/home.py", "pages/vip.py", "pages/stock.py", 
    "pages/crypto.py", "pages/real_estate.py", "pages/bank.py", "pages/txlog.py", 
    "pages/quest.py", "pages/title_shop.py", "pages/ranking.py", "pages/dm.py",
    "pages/games/__init__.py", "pages/games/slot.py", "pages/games/blackjack.py", 
    "pages/games/mine.py", "pages/games/quiz.py", "pages/games/lotto.py", 
    "pages/games/forge.py", "pages/games/gacha.py",
    "pages/sports/__init__.py", "pages/sports/soccer_sim.py", "pages/sports/penalty.py", 
    "pages/sports/racing.py", "pages/sports/garage.py",
    "pages/admin/__init__.py", "pages/admin/panel.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w', encoding='utf-8') as f:
        pass # 빈 파일 생성

print("✅ HYOMIN UNIVERSE 폴더 및 파일 구조 생성 완료!")