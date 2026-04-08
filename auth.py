import time
import streamlit as st

from config import USERS_FILE
from database import load_db, save_db


LOGIN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap');
.stApp { background: radial-gradient(ellipse at 20% 50%, #0d0221 0%, #050510 60%, #000 100%) !important; }
* { font-family:'Noto Sans KR',sans-serif !important; color:#FFF !important; }
.login-title {
  font-family:'Orbitron',monospace !important; font-size:clamp(2rem,6vw,4rem) !important;
  font-weight:900; text-align:center;
  background:linear-gradient(135deg,#00E5FF 0%,#FF00FF 50%,#FFD600 100%);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  padding:20px 0; letter-spacing:4px; animation:glow 3s ease-in-out infinite alternate;
}
@keyframes glow { from{filter:drop-shadow(0 0 10px #00E5FF)} to{filter:drop-shadow(0 0 30px #FF00FF)} }
.login-sub { text-align:center; color:#888 !important; font-size:1rem; margin-bottom:30px; letter-spacing:3px; }
.stTextInput>div>div>input {
  background:rgba(0,229,255,0.05) !important; border:1px solid rgba(0,229,255,0.3) !important;
  border-radius:8px !important; color:#000 !important; font-size:1rem !important; padding:12px !important;
}
.stButton>button {
  background:linear-gradient(135deg,#00E5FF,#0066FF) !important; border:none !important;
  border-radius:8px !important; color:#000 !important; font-weight:900 !important;
  font-size:1rem !important; padding:14px !important; width:100%;
}
</style>"""


def render_login():
    """로그인/회원가입 UI. 로그인 성공 시 st.rerun(), 미로그인 시 st.stop()."""
    if 'logged_in_user' in st.session_state:
        return

    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    st.markdown("<div class='login-title'>🌌 HYOMIN UNIVERSE</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-sub'>∙ 가상 자산 시뮬레이터 v17.0 ∙</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"], horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])

        with tabs[0]:
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            if st.button("🚀 유니버스 입장", use_container_width=True):
                users = load_db(USERS_FILE, {})

                def _do_login(uid):
                    u = users[uid]
                    st.session_state.update({
                        'logged_in_user': uid,
                        'global_cash':    u['cash'],
                        'inventory':      u.get('inventory', []),
                        'equipped_title': u.get('equipped_title', '🌱 신규시민'),
                        'portfolio':      u.get('portfolio', {}),
                        'real_estate':    u.get('real_estate', {}),
                        'rent_time':      u.get('rent_time', time.time()),
                        'loan':           u.get('loan', 0),
                        'loan_time':      u.get('loan_time', time.time()),
                        'device_mode':    device_mode,
                        'stats':          u.get('stats', {'wins': 0, 'losses': 0, 'races_won': 0, 'lotto_spent': 0}),
                    })
                    st.rerun()

                if l_id == "5891" and l_pw == "5891":
                    if "5891" not in users:
                        users["5891"] = {
                            "pw": "5891", "cash": 999_999_999_999, "inventory": [],
                            "equipped_title": "👑 절대신 창조주", "portfolio": {},
                            "real_estate": {}, "rent_time": time.time(),
                            "loan": 0, "loan_time": time.time(), "stats": {},
                        }
                        save_db(USERS_FILE, users)
                    _do_login("5891")
                elif l_id in users and users[l_id]['pw'] == l_pw:
                    _do_login(l_id)
                else:
                    st.error("❌ 아이디 또는 비밀번호가 올바르지 않습니다.")

        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 시민 등록하기", use_container_width=True):
                users = load_db(USERS_FILE, {})
                if n_id in users or n_id == "5891":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(n_id) < 2:
                    st.error("아이디는 2자 이상이어야 합니다.")
                else:
                    users[n_id] = {
                        "pw": n_pw, "cash": 100_000_000, "inventory": [],
                        "equipped_title": "🌱 신규시민", "portfolio": {},
                        "real_estate": {}, "rent_time": time.time(),
                        "loan": 0, "loan_time": time.time(), "stats": {},
                    }
                    save_db(USERS_FILE, users)
                    st.success("🎉 가입 성공! 초기 자금 1억원이 지급되었습니다!")
    st.stop()
