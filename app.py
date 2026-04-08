import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import random
import json
import os
import math
from datetime import datetime

# ==============================
# 데이터베이스 시스템 (JSON)
# ==============================
USERS_FILE = "users_db.json"
COMMENTS_FILE = "comments_db.json"

# 1. 유저 DB 로드 및 저장
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_users(users_data):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users_data, f, indent=4, ensure_ascii=False)

# 2. 현재 세션의 유저 데이터를 DB에 동기화 (돈 변동 시 호출)
def sync_user_data():
    if 'logged_in_user' in st.session_state:
        users = load_users()
        uid = st.session_state.logged_in_user
        users[uid]['cash'] = st.session_state.global_cash
        users[uid]['inventory'] = st.session_state.inventory
        users[uid]['equipped_title'] = st.session_state.equipped_title
        users[uid]['portfolio'] = st.session_state.portfolio
        save_users(users)

# 3. 댓글 DB
def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []

def save_comment(name, comment):
    comments = load_comments()
    comments.append({"name": name, "comment": comment, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

# ==============================
# 시스템 초기화 및 CSS
# ==============================
st.set_page_config(page_title="김효민 슈퍼 포털", page_icon="🌐", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Space Mono', monospace; color: #e0e0e0; }
    .stApp { background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%); }
    h1, h2, h3 { color: #00ff88 !important; }
    .stButton>button { border: 2px solid #00ff88; color: #00ff88; background: transparent; font-weight: bold; border-radius: 8px;}
    .stButton>button:hover { background-color: #00ff88; color: #0f0f23; }
    div[data-testid="stBlock"] { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; }
</style>
""", unsafe_allow_html=True)

# ==============================
# 로그인 / 회원가입 페이지
# ==============================
if 'logged_in_user' not in st.session_state:
    st.markdown("<h1 style='text-align: center; font-size: 60px; margin-top: 50px;'>⚡ HYOMIN PORTAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #aaa;'>계정을 만들고 자산을 영구적으로 저장하세요.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        tab1, tab2 = st.tabs(["🔑 로그인", "📝 회원가입"])
        
        with tab1:
            login_id = st.text_input("아이디", key="l_id")
            login_pw = st.text_input("비밀번호", type="password", key="l_pw")
            if st.button("로그인", use_container_width=True):
                users = load_users()
                if login_id in users and users[login_id]['pw'] == login_pw:
                    # 세션에 정보 로드
                    st.session_state.logged_in_user = login_id
                    st.session_state.global_cash = users[login_id]['cash']
                    st.session_state.inventory = users[login_id]['inventory']
                    st.session_state.equipped_title = users[login_id]['equipped_title']
                    st.session_state.portfolio = users[login_id].get('portfolio', {})
                    st.success("로그인 성공! 포털로 이동합니다...")
                    st.rerun()
                else:
                    st.error("아이디나 비밀번호가 틀렸습니다.")
                    
        with tab2:
            new_id = st.text_input("새 아이디", key="r_id")
            new_pw = st.text_input("새 비밀번호", type="password", key="r_pw")
            if st.button("가입하기", use_container_width=True):
                users = load_users()
                if new_id in users:
                    st.error("이미 존재하는 아이디입니다.")
                elif len(new_id) < 2 or len(new_pw) < 2:
                    st.warning("아이디와 비밀번호는 2글자 이상 입력해주세요.")
                else:
                    users[new_id] = {
                        "pw": new_pw,
                        "cash": 100000000, # 초기 자본 1억
                        "inventory": [],
                        "equipped_title": "신규 유저",
                        "portfolio": {}
                    }
                    save_users(users)
                    st.success("가입 완료! 이제 로그인 탭에서 로그인해주세요.")
                    
    st.stop() # 로그인 전에는 아래 코드를 실행하지 않음

# ==============================
# 로그인 후: 메인 포털 UI
# ==============================
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/controller.png")
    st.title("메뉴")
    st.header(f"🧑 [{st.session_state.equipped_title}] {st.session_state.logged_in_user}")
    st.metric("보유 자산", f"₩{st.session_state.global_cash:,}")
    
    if st.button("🚪 로그아웃"):
        sync_user_data() # 나가기 전에 강제 저장
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
        
    st.markdown("---")
    menu = st.radio("바로가기", ["🏠 홈", "⚽ 11vs11 실시간 사커", "📈 실시간 주식 마스터", "🛒 쇼핑몰", "💬 커뮤니티"])

# ==============================
# ⚽ 11vs11 실시간 사커 (패스/슛 개선 & 버그 수정)
# ==============================
if menu == "⚽ 11vs11 실시간 사커":
    st.title("⚽ 11vs11 실시간 액션 사커")
    st.markdown("조작법: **WASD** 이동 / 공을 가진 상태에서 **[S] 자동 패스**, **[D] 강슛**")
    
    if 'soccer_game_active' not in st.session_state:
        st.session_state.soccer_game_active = False

    col1, col2 = st.columns([1, 3])
    with col1:
        st.info("🎟️ **참가비:** ₩500,000\n\n🏆 **우승 상금:** ₩2,000,000")
        position = st.selectbox("출전 포지션", ["공격수 (FW)", "미드필더 (MF)", "수비수 (DF)"])
        start_x = 600 if position == "공격수 (FW)" else 400 if position == "미드필더 (MF)" else 200
        
        if not st.session_state.soccer_game_active:
            if st.button("경기 시작 (참가비 결제)", use_container_width=True):
                if st.session_state.global_cash >= 500000:
                    st.session_state.global_cash -= 500000
                    st.session_state.soccer_game_active = True
                    sync_user_data()
                    st.rerun()
                else:
                    st.error("참가비가 부족합니다.")
        else:
            if st.button("🏆 상금 정산 및 종료", use_container_width=True):
                st.session_state.global_cash += 2000000
                st.session_state.soccer_game_active = False
                sync_user_data()
                st.success("상금 2,000,000원 획득 완료!")
                st.rerun()

    with col2:
        if st.session_state.soccer_game_active:
            # 개선된 JS 물리엔진 및 조작
            html_code = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ margin: 0; overflow: hidden; background: #1a4d2e; display: flex; justify-content: center; align-items: center; color: white; font-family: monospace; }}
                    canvas {{ border: 2px solid #00ff88; box-shadow: 0 0 20px rgba(0,255,136,0.3); background: #1a4d2e; }}
                    #ui {{ position: absolute; top: 10px; width: 760px; display: flex; justify-content: space-between; font-size: 24px; font-weight: bold; text-shadow: 1px 1px 2px black; pointer-events: none; }}
                </style>
            </head>
            <body>
                <div id="ui">
                    <div style="color: #00d4ff;">HOME <span id="homeScore">0</span></div>
                    <div style="color: #ffaa00;">[S]패스 [D]슛</div>
                    <div style="color: #ff4444;"><span id="awayScore">0</span> AWAY</div>
                </div>
                <canvas id="gameCanvas" width="800" height="500"></canvas>
                <script>
                    const canvas = document.getElementById("gameCanvas");
                    const ctx = canvas.getContext("2d");
                    
                    let score = {{ home: 0, away: 0 }};
                    const keys = {{}};
                    window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
                    window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

                    const ball = {{ x: 400, y: 250, vx: 0, vy: 0, radius: 6, heldBy: null }};
                    const players = [];
                    
                    const userPlayer = {{ x: {start_x}, y: 250, vx: 0, vy: 0, color: '#ffaa00', team: 'home', isUser: true }};
                    players.push(userPlayer);
                    
                    // Teammates & Enemies
                    for(let i=0; i<10; i++) players.push({{ x: Math.random()*300 + 50, y: Math.random()*400 + 50, vx: 0, vy: 0, color: '#00d4ff', team: 'home', isUser: false }});
                    for(let i=0; i<11; i++) players.push({{ x: Math.random()*300 + 450, y: Math.random()*400 + 50, vx: 0, vy: 0, color: '#ff4444', team: 'away', isUser: false }});

                    function update() {{
                        let speed = 0.8;
                        players.forEach(p => {{
                            if(p.isUser) {{
                                if(keys['arrowup'] || keys['w']) p.vy -= speed;
                                if(keys['arrowdown'] || keys['s']) p.vy += speed;
                                if(keys['arrowleft'] || keys['a']) p.vx -= speed;
                                if(keys['arrowright'] || keys['d']) p.vx += speed;
                            }} else {{
                                // AI
                                if(Math.hypot(ball.x - p.x, ball.y - p.y) < 150 && ball.heldBy !== p) {{
                                    p.vx += (ball.x - p.x) * 0.003;
                                    p.vy += (ball.y - p.y) * 0.003;
                                }}
                            }}
                            
                            p.x += p.vx; p.y += p.vy;
                            p.vx *= 0.85; p.vy *= 0.85; // Friction
                            p.x = Math.max(10, Math.min(790, p.x));
                            p.y = Math.max(10, Math.min(490, p.y));
                        }});

                        // Ball Grab Logic
                        if(ball.heldBy === null) {{
                            players.forEach(p => {{
                                if(Math.hypot(ball.x - p.x, ball.y - p.y) < 15) ball.heldBy = p;
                            }});
                        }}

                        if(ball.heldBy !== null) {{
                            let p = ball.heldBy;
                            // Keep ball at player's feet
                            ball.x = p.x + (p.team === 'home' ? 10 : -10);
                            ball.y = p.y;
                            ball.vx = 0; ball.vy = 0;
                            
                            if(p.isUser) {{
                                // User Pass (S)
                                if(keys['s']) {{
                                    // Find nearest teammate
                                    let bestDist = Infinity; let target = null;
                                    players.forEach(tm => {{
                                        if(tm.team === 'home' && !tm.isUser && tm.x > p.x) {{
                                            let d = Math.hypot(tm.x - p.x, tm.y - p.y);
                                            if(d < bestDist) {{ bestDist = d; target = tm; }}
                                        }}
                                    }});
                                    if(target) {{
                                        let angle = Math.atan2(target.y - ball.y, target.x - ball.x);
                                        ball.vx = Math.cos(angle) * 18;
                                        ball.vy = Math.sin(angle) * 18;
                                    }} else {{ ball.vx = 15; ball.vy = 0; }}
                                    ball.heldBy = null;
                                    keys['s'] = false; // Prevent spam
                                }}
                                // User Shoot (D)
                                else if(keys['d']) {{
                                    let angle = Math.atan2(250 - ball.y, 800 - ball.x);
                                    ball.vx = Math.cos(angle) * 25; // Super fast shot
                                    ball.vy = Math.sin(angle) * 25;
                                    ball.heldBy = null;
                                    keys['d'] = false;
                                }}
                            }} else {{
                                // AI Pass/Shoot
                                if(Math.random() < 0.02) {{
                                    ball.vx = (p.team === 'home' ? 1 : -1) * (10 + Math.random()*10);
                                    ball.vy = (Math.random()-0.5)*10;
                                    ball.heldBy = null;
                                }}
                            }}
                        }} else {{
                            ball.x += ball.vx; ball.y += ball.vy;
                            ball.vx *= 0.96; ball.vy *= 0.96;
                        }}

                        // Wall Bounces & Goals
                        if(ball.y < 0 || ball.y > 500) ball.vy *= -1;
                        if(ball.x < 0) {{ score.away++; resetBall(); }} 
                        if(ball.x > 800) {{ score.home++; resetBall(); }} 
                        
                        document.getElementById('homeScore').innerText = score.home;
                        document.getElementById('awayScore').innerText = score.away;
                    }}

                    function resetBall() {{ ball.x = 400; ball.y = 250; ball.vx = 0; ball.vy = 0; ball.heldBy = null; }}

                    function draw() {{
                        ctx.clearRect(0, 0, canvas.width, canvas.height);
                        ctx.strokeStyle = "rgba(255,255,255,0.3)"; ctx.lineWidth = 2;
                        ctx.beginPath(); ctx.moveTo(400, 0); ctx.lineTo(400, 500); ctx.stroke();
                        ctx.beginPath(); ctx.arc(400, 250, 60, 0, Math.PI*2); ctx.stroke();
                        ctx.fillStyle = "rgba(255,255,255,0.5)"; ctx.fillRect(0, 150, 10, 200); ctx.fillRect(790, 150, 10, 200);

                        players.forEach(p => {{
                            ctx.fillStyle = p.color;
                            ctx.beginPath(); ctx.arc(p.x, p.y, p.isUser ? 12 : 9, 0, Math.PI*2); ctx.fill();
                            if(p.isUser) {{ ctx.strokeStyle = '#fff'; ctx.stroke(); ctx.fillStyle='white'; ctx.fillText('ME', p.x-6, p.y-15);}}
                        }});

                        ctx.fillStyle = "white";
                        ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI*2); ctx.fill();
                        if(ball.heldBy) {{ ctx.strokeStyle = 'yellow'; ctx.beginPath(); ctx.arc(ball.x, ball.y, 8, 0, Math.PI*2); ctx.stroke(); }}
                    }}

                    function loop() {{ update(); draw(); requestAnimationFrame(loop); }}
                    loop();
                </script>
            </body>
            </html>
            """
            components.html(html_code, height=520)
        else:
            st.info("좌측에서 참가비를 결제하고 경기를 시작해주세요.")

# ==============================
# 📈 주식 마스터 및 기타 메뉴 
# (데이터 동기화: sync_user_data() 적용)
# ==============================
elif menu == "📈 실시간 주식 마스터":
    st.title("📈 실시간 주식 마스터")
    
    auto_refresh = st.checkbox("🔄 실시간 차트 자동 반영 켜기 (3초 단위)", value=False)
    if auto_refresh: st.markdown('<meta http-equiv="refresh" content="3">', unsafe_allow_html=True)

    stock_config = [
        {"id": "SAMJI", "name": "삼지전자(우대)", "vol": 0.05, "trend": 1.01},
        {"id": "TECH", "name": "테크노밸리", "vol": 0.03, "trend": 1.0},
        {"id": "AUTO", "name": "현대자동차", "vol": 0.025, "trend": 1.0},
        {"id": "CRYPTO", "name": "도지코인", "vol": 0.15, "trend": 0.99}
    ]

    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(10000, 200000), "history": []} for s in stock_config}
    if 'news_feed' not in st.session_state: st.session_state.news_feed = []

    # 주가 변동 엔진
    for cfg in stock_config:
        sid = cfg['id']
        curr_data = st.session_state.stock_data[sid]
        change_pct = (random.random() - 0.5) * 2 * cfg['vol'] * cfg['trend']
        new_price = max(500, curr_data['price'] * (1 + change_pct))
        curr_data['price'] = round(new_price)
        curr_data['history'].append(curr_data['price'])
        curr_data['history'] = curr_data['history'][-30:]
        
        if random.random() < 0.05:
            st.session_state.news_feed.insert(0, f"[{curr_data['name']}] {'급등 조짐!' if change_pct>0 else '급락 우려!'}")
            st.session_state.news_feed = st.session_state.news_feed[:4]

    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.subheader("내 포트폴리오 및 수익률")
        port_data = []
        total_eval = 0
        for sid, p_data in st.session_state.portfolio.items():
            qty = p_data.get("qty", 0)
            if qty == 0: continue
            avg = p_data["avg_price"]
            curr = st.session_state.stock_data[sid]["price"]
            eval_amt = qty * curr
            profit = eval_amt - (qty * avg)
            profit_pct = (curr - avg) / avg * 100
            total_eval += eval_amt
            
            port_data.append({
                "종목명": st.session_state.stock_data[sid]["name"],
                "보유량": qty,
                "평단가": f"₩{int(avg):,}",
                "현재가": f"₩{curr:,}",
                "평가액": f"₩{eval_amt:,}",
                "손익금(수익률)": f"{'🔴+' if profit>0 else '🔵'}₩{int(profit):,} ({profit_pct:.2f}%)"
            })
        if port_data:
            st.dataframe(pd.DataFrame(port_data), use_container_width=True)
            st.markdown(f"**💰 현금:** ₩{st.session_state.global_cash:,} | **📊 총 평가액:** ₩{total_eval:,}")
        else:
            st.info("보유 주식이 없습니다.")
            
        selected_sid = st.selectbox("차트 종목", [s['id'] for s in stock_config])
        df_chart = pd.DataFrame(st.session_state.stock_data[selected_sid]['history'], columns=["가격"])
        st.plotly_chart(px.line(df_chart, y="가격", title=st.session_state.stock_data[selected_sid]['name'], template="plotly_dark"), use_container_width=True)

    with col2:
        st.subheader("속보")
        for n in st.session_state.news_feed: st.warning(n)
            
        curr_price = st.session_state.stock_data[selected_sid]['price']
        st.markdown(f"**현재가:** <span style='color:#00ff88; font-size:24px;'>₩{curr_price:,}</span>", unsafe_allow_html=True)
        trade_amount = st.number_input("수량 입력", min_value=1, value=1)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📉 매수"):
                cost = trade_amount * curr_price
                if st.session_state.global_cash >= cost:
                    st.session_state.global_cash -= cost
                    old = st.session_state.portfolio.get(selected_sid, {"qty": 0, "avg_price": 0})
                    new_qty = old["qty"] + trade_amount
                    new_avg = ((old["qty"] * old["avg_price"]) + cost) / new_qty
                    st.session_state.portfolio[selected_sid] = {"qty": new_qty, "avg_price": new_avg}
                    sync_user_data()
                    st.rerun()
            if st.button("💥 풀매수"):
                max_qty = st.session_state.global_cash // curr_price
                if max_qty > 0:
                    cost = max_qty * curr_price
                    st.session_state.global_cash -= cost
                    old = st.session_state.portfolio.get(selected_sid, {"qty": 0, "avg_price": 0})
                    new_qty = old["qty"] + max_qty
                    new_avg = ((old["qty"] * old["avg_price"]) + cost) / new_qty
                    st.session_state.portfolio[selected_sid] = {"qty": new_qty, "avg_price": new_avg}
                    sync_user_data()
                    st.rerun()

        with c2:
            if st.button("📈 매도"):
                owned = st.session_state.portfolio.get(selected_sid, {"qty": 0})["qty"]
                if owned >= trade_amount:
                    st.session_state.global_cash += trade_amount * curr_price
                    st.session_state.portfolio[selected_sid]["qty"] -= trade_amount
                    sync_user_data()
                    st.rerun()
            if st.button("💸 풀매도"):
                owned = st.session_state.portfolio.get(selected_sid, {"qty": 0})["qty"]
                if owned > 0:
                    st.session_state.global_cash += owned * curr_price
                    st.session_state.portfolio[selected_sid]["qty"] = 0
                    sync_user_data()
                    st.rerun()

elif menu == "🛒 쇼핑몰":
    # (상점 뷰는 이전 구조 유지, 구매/장착 시 sync_user_data()만 추가)
    st.title("🛒 HYOMIN STORE")
    items = [
        {'id':'c1', 'type':'vehicle', 'name':'kia 레이 (2021)', 'price': 15000000},
        {'id':'c2', 'type':'property', 'name':'힐스테이트 푸르지오 수원', 'price': 800000000},
        {'id':'c3', 'type':'title', 'name':'삼지전자 수석엔지니어', 'price': 5000000},
    ]
    cols = st.columns(3)
    for i, item in enumerate(items):
        with cols[i%3]:
            st.markdown(f"### {item['name']}")
            st.markdown(f"**₩{item['price']:,}**")
            if item['id'] in st.session_state.inventory:
                if item['type'] == 'title':
                    if st.session_state.equipped_title == item['name']: st.button("장착중", key=item['id'], disabled=True)
                    else:
                        if st.button("장착하기", key=item['id']):
                            st.session_state.equipped_title = item['name']
                            sync_user_data()
                            st.rerun()
                else:
                    st.button("보유중", key=item['id'], disabled=True)
            else:
                if st.button("구매", key=item['id']):
                    if st.session_state.global_cash >= item['price']:
                        st.session_state.global_cash -= item['price']
                        st.session_state.inventory.append(item['id'])
                        sync_user_data()
                        st.rerun()

elif menu == "💬 커뮤니티":
    st.title("💬 포털 커뮤니티")
    c_text = st.text_area("메시지 남기기")
    if st.button("댓글등록"):
        save_comment(st.session_state.logged_in_user, c_text)
        st.success("등록 완료")
        st.rerun()
    for c in reversed(load_comments()):
        st.info(f"**{c['name']}** ({c['time']}): {c['comment']}")
