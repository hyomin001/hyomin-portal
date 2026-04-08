import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import json
import os
from datetime import datetime

# ==============================
# 시스템 설정 및 상태 관리 (DB 대체)
# ==============================
st.set_page_config(page_title="김효민 게임 포털", page_icon="🎮", layout="wide")

# 댓글 저장을 위한 간단한 JSON 파일 시스템
COMMENTS_FILE = "comments_db.json"

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_comment(name, comment):
    comments = load_comments()
    comments.append({
        "name": name,
        "comment": comment,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f, indent=4, ensure_ascii=False)

# 세션 상태 초기화 (게임 간 돈 및 아이템 공유)
if 'global_cash' not in st.session_state:
    st.session_state.global_cash = 100000000  # 1억 시작
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'equipped_title' not in st.session_state:
    st.session_state.equipped_title = "무직"

# custom CSS for Neon Style (오타 수정: unsafe_allow_html=True)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Space Mono', monospace;
        color: #e0e0e0;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #16213e 100%);
    }
    h1, h2, h3 {
        color: #00ff88 !important;
        text-shadow: 0 0 10px rgba(0,255,136,0.5);
    }
    .stButton>button {
        background-color: transparent;
        border: 2px solid #00ff88;
        color: #00ff88;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ff88;
        color: #0f0f23;
        box-shadow: 0 0 20px #00ff88;
    }
    div[data-testid="stBlock"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# 메인 내비게이션
# ==============================
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/controller.png")
    st.title("효민 포털 메뉴")
    equipped_display = f"[{st.session_state.equipped_title}]"
    st.header(f"🧑 김효민 {equipped_display}")
    st.metric("보유 자산", f"₩{st.session_state.global_cash:,}")
    st.markdown("---")
    menu = st.radio("바로가기", ["🏠 홈", "⚽ 전술 슈팅", "📈 주식 마스터", "🛒 쇼핑몰", "💬 커뮤니티"])

# ==============================
# 페이지 1: 홈
# ==============================
if menu == "🏠 홈":
    st.title("KIM HYOMIN GAME PORTAL")
    st.subheader(f"{st.session_state.equipped_title} 효민님의 프라이빗 포털입니다.")
    st.markdown("""
    옵션 B(파이썬/Streamlit)로 새롭게 구축된 고퀄리티 게임 포털에 오신 것을 환영합니다!
    
    - **⚽ 전술 슈팅**: 직접 방향과 파워를 정하는 긴장감 넘치는 승부차기 게임입니다.
    - **📈 주식 마스터**: 삼지전자를 포함한 10개 종목의 실시간 트레이딩을 지원합니다.
    - **🛒 쇼핑몰**: 100가지 유니크 아이템으로 꾸미고 커뮤니티에서 뽐내보세요.
    - **💬 커뮤니티**: 친구들에게 이 페이지 주소를 공유하고 댓글 피드백을 받으세요!
    """)

# ==============================
# 페이지 2: 전술 슈팅 (Participative Soccer)
# ==============================
elif menu == "⚽ 전술 슈팅":
    st.title("⚽ 승부차기 전술 슈팅")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("슈팅 타겟 지역 (9분할)")
        
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)
        goal = patches.Rectangle((0, 0), 3, 3, linewidth=5, edgecolor='#00ff88', facecolor='#1a4d2e')
        ax.add_patch(goal)
        
        for v in range(1, 3):
            ax.axvline(v, color='white', linestyle='--', alpha=0.5)
            ax.axhline(v, color='white', linestyle='--', alpha=0.5)
        
        centers = []
        for r in range(3):
            for c in range(3):
                idx = (2-r)*3 + (c+1)
                ax.text(c+0.5, r+0.5, str(idx), color='white', fontsize=20, ha='center', va='center', fontweight='bold')

        ax.axis('off')
        st.pyplot(fig)

    with col2:
        st.subheader("조작 패널")
        target = st.selectbox("슈팅 방향 (그리드 번호)", range(1, 10))
        power = st.slider("슈팅 파워", 10, 100, 70, step=10)
        kick_btn = st.button("슈팅 KICK!")

        if kick_btn:
            keeper_direction = random.randint(1, 9)
            success_prob = 1.0
            
            if power > 80:
                success_prob -= 0.2
            
            shot_success = random.random() < success_prob
            
            with st.spinner("슈팅 중... ⚽💨"):
                import time
                time.sleep(1)
            
            st.markdown(f"**효민님의 조준:** 그리드 {target} 번")
            st.markdown(f"**AI 키퍼 다이빙:** 그리드 {keeper_direction} 번")

            if shot_success:
                if target != keeper_direction:
                    st.success(f"⚽ GOOOOOAL!! 득점 성공! (+₩5,000,000)")
                    st.balloons()
                    st.session_state.global_cash += 5000000
                else:
                    st.error("🧤 AI 키퍼의 슈퍼 세이브! 막혔습니다.")
            else:
                st.warning("💥 슈팅 미스! 공이 골대를 벗어났습니다.")

# ==============================
# 페이지 3: 주식 마스터
# ==============================
elif menu == "📈 주식 마스터":
    st.title("📈 주식 마스터 (실시간 트레이딩)")
    
    stock_config = [
        {"id": "SAMJI", "name": "삼지전자(우대)", "vol": 0.05, "color": "#00ff88", "trend": 1.01},
        {"id": "TECH", "name": "테크노밸리", "vol": 0.03, "color": "#00d4ff", "trend": 1.0},
        {"id": "AUTO", "name": "현대자동차", "vol": 0.025, "color": "#ffaa00", "trend": 1.0},
        {"id": "BIO", "name": "바이오젠", "vol": 0.04, "color": "#ff4444", "trend": 1.0},
        {"id": "FOOD", "name": "제일식품", "vol": 0.015, "color": "#ff88dd", "trend": 1.0},
        {"id": "AERO", "name": "나로스페이스", "vol": 0.06, "color": "#88aaff", "trend": 1.0},
        {"id": "COMM", "name": "국민은행", "vol": 0.02, "color": "#cccccc", "trend": 1.0},
        {"id": "ENT", "name": "빅히트엔터", "vol": 0.045, "color": "#dd88ff", "trend": 1.0},
        {"id": "CRYPTO", "name": "도지코인", "vol": 0.15, "color": "#ffcc00", "trend": 0.99},
        {"id": "ENERGY", "name": "에너지코리아", "vol": 0.035, "color": "#aa88ff", "trend": 1.0}
    ]

    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = {s['id']: {"name":s['name'], "price": random.randint(10000, 200000), "history": []} for s in stock_config}
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {}

    if st.button("🔄 주가 새로고침"):
        for cfg in stock_config:
            sid = cfg['id']
            curr_data = st.session_state.stock_data[sid]
            change_pct = (random.random() - 0.5) * 2 * cfg['vol'] * cfg['trend']
            new_price = max(500, curr_data['price'] * (1 + change_pct))
            curr_data['price'] = round(new_price)
            curr_data['history'].append(curr_data['price'])
            curr_data['history'] = curr_data['history'][-20:]
        st.rerun()

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("주식 시장 목록")
        stock_df_data = []
        for cfg in stock_config:
            sid = cfg['id']
            sd = st.session_state.stock_data[sid]
            owned = st.session_state.portfolio.get(sid, 0)
            stock_df_data.append({
                "티커": sid, "종목명": sd['name'], "현재가": f"₩{sd['price']:,}",
                "보유량": owned, "평가액": f"₩{(owned * sd['price']):,}"
            })
        st.dataframe(pd.DataFrame(stock_df_data), use_container_width=True)

    with col2:
        st.subheader("거래 및 차트")
        selected_sid = st.selectbox("거래할 종목 선택", [s['id'] for s in stock_config])
        
        chart_data = st.session_state.stock_data[selected_sid]['history']
        if chart_data:
            df_chart = pd.DataFrame(chart_data, columns=["가격"])
            st.plotly_chart(px.line(df_chart, y="가격", title=f"{st.session_state.stock_data[selected_sid]['name']} 주가 추이", 
                                    template="plotly_dark", color_discrete_sequence=['#00ff88']), use_container_width=True)
        else:
            st.info("새로고침을 눌러 차트 데이터를 생성하세요.")

        trade_amount = st.number_input("수량 입력", min_value=1, value=1, step=1)
        curr_price = st.session_state.stock_data[selected_sid]['price']
        total_cost = trade_amount * curr_price
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("📉 매수", help=f"총 ₩{total_cost:,} 필요"):
                if st.session_state.global_cash >= total_cost:
                    st.session_state.global_cash -= total_cost
                    st.session_state.portfolio[selected_sid] = st.session_state.portfolio.get(selected_sid, 0) + trade_amount
                    st.success(f"매수 완료! 현금: ₩{st.session_state.global_cash:,}")
                    st.rerun()
                else:
                    st.error("현금이 부족합니다.")
        with b2:
            if st.button("📈 매도", help=f"총 ₩{total_cost:,} 획득"):
                owned = st.session_state.portfolio.get(selected_sid, 0)
                if owned >= trade_amount:
                    st.session_state.global_cash += total_cost
                    st.session_state.portfolio[selected_sid] = owned - trade_amount
                    st.success(f"매도 완료! 현금: ₩{st.session_state.global_cash:,}")
                    st.rerun()
                else:
                    st.error("보유 수량이 부족합니다.")

# ============
# 페이지 4: 쇼핑몰
# ============
elif menu == "🛒 쇼핑몰":
    st.title("🛒 HYOMIN STORE (100 유니크 아이템)")

    categories = ['title', 'vehicle', 'tech', 'property']
    cat_icons = {'title': '🏷️', 'vehicle': '🏎️', 'tech': '📱', 'property': '🏢'}
    cat_prefix = {'title': '[칭호]', 'vehicle': '[이동수단]', 'tech': '[장비]', 'property': '🏠[부동산]'}
    
    custom_items = [
        {'id':'c1', 'type':'vehicle', 'name':'kia 레이 (2021)', 'price': 15000000},
        {'id':'c2', 'type':'property', 'name':'힐스테이트 푸르지오 수원 (98타입)', 'price': 800000000},
        {'id':'c3', 'type':'tech', 'name':'갤럭시 S26 울트라 (가상)', 'price': 1600000},
        {'id':'c4', 'type':'title', 'name':'삼지전자 수석엔지니어', 'price': 5000000},
        {'id':'c5', 'type':'tech', 'name':'PcapNG 파서 스크립트 Pro', 'price': 500000},
    ]

    items = custom_items.copy()
    item_prefixes = ['초호화', '한정판', '미래형', '레트로', '스마트', '사이버펑크', '황금', '미니멀']
    for i in range(1, 96):
        c_type = categories[i % 4]
        items.append({
            'id': f'auto_{i}',
            'type': c_type,
            'name': f"{random.choice(item_prefixes)} {cat_prefix[c_type].strip('[]')} Mk.{i}",
            'price': 100000 * (i**2)
        })

    filter_type = st.radio("카테고리 필터", ["전체"] + categories, horizontal=True)
    filtered_items = items if filter_type == "전체" else [i for i in items if i['type'] == filter_type]

    rows = len(filtered_items) // 4 + 1
    for r in range(rows):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            if idx < len(filtered_items):
                item = filtered_items[idx]
                with cols[c]:
                    st.markdown(f"### {cat_icons[item['type']]} {item['name']}")
                    st.markdown(f"**가격:** ₩{item['price']:,}")
                    
                    is_owned = item['id'] in st.session_state.inventory
                    is_equipped = st.session_state.equipped_title == item['name']
                    
                    if is_owned:
                        if item['type'] == 'title':
                            if is_equipped:
                                st.button("❌ 장착 해제", key=item['id'], disabled=True)
                            else:
                                if st.button("✅ 칭호 장착", key=item['id']):
                                    st.session_state.equipped_title = item['name']
                                    st.rerun()
                        else:
                            st.button("보유 중", key=item['id'], disabled=True)
                    else:
                        if st.button(f"🛒 구매", key=item['id']):
                            if st.session_state.global_cash >= item['price']:
                                st.session_state.global_cash -= item['price']
                                st.session_state.inventory.append(item['id'])
                                st.success(f"{item['name']} 구매 완료!")
                                st.rerun()
                            else:
                                st.error("현금이 부족합니다.")

# ============
# 페이지 5: 커뮤니티 (오타 수정: unsafe_allow_html=True)
# ============
elif menu == "💬 커뮤니티":
    st.title("💬 커뮤니티 (피드백 및 채팅)")
    
    st.markdown("---")
    st.subheader("📝 의견 남기기")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        c_name = st.text_input("이름 (또는 닉네임)", value="방문자", max_chars=10)
        c_text = st.text_area("내용", height=100, placeholder="게임에 대한 피드백이나 효민님께 메시지를 남겨주세요!")
        c_btn = st.button("댓글등록")
        
        if c_btn:
            if c_text.strip():
                save_comment(c_name, c_text)
                st.success("댓글이 성공적으로 등록되었습니다.")
                st.rerun()
            else:
                st.error("내용을 입력해 주세요.")

    with col2:
        comments = load_comments()
        st.subheader(f"전체 댓글 ({len(comments)}개)")
        
        if not comments:
            st.info("아직 등록된 댓글이 없습니다. 첫 댓글을 남겨보세요!")
        else:
            for c in reversed(comments):
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.05); border-left: 5px solid #00ff88; padding: 15px; margin-bottom: 10px; border-radius: 5px;">
                    <span style="color:#00ff88; font-weight:bold;">{c['name']}</span>
                    <span style="color:#aaa; font-size:0.8em; margin-left:10px;">({c['time']})</span>
                    <p style="margin-top:10px; color:#e0e0e0;">{c['comment']}</p>
                </div>
                """, unsafe_allow_html=True)