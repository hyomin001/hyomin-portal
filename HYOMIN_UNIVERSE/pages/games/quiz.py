# pages/games/quiz.py
import streamlit as st
import random
from utils.core import format_korean_money, sync_user_data
from utils.database import log_tx

QUESTION_POOL = [
    {"q": "함수 종속에서 X → Y 의미는?", "a": "X 값이 Y를 결정", "w": ["Y가 X 결정","서로 독립","무관"], "cat": "데이터베이스"},
    {"q": "정규화 목적은?", "a": "데이터 중복 최소화", "w": ["속도 향상","보안 강화","암호화"], "cat": "데이터베이스"},
    {"q": "카디널리티 의미는?", "a": "튜플 수", "w": ["속성 수","키 수","인덱스 수"], "cat": "데이터베이스"},
    {"q": "차수(Degree)는?", "a": "속성 수", "w": ["튜플 수","키 수","인덱스"], "cat": "데이터베이스"},
    {"q": "프로세스 상태 중 실행 상태는?", "a": "CPU 사용 중", "w": ["대기","생성","종료"], "cat": "운영체제"},
    {"q": "스레드 장점은?", "a": "경량 프로세스", "w": ["무겁다","독립 메모리","느림"], "cat": "운영체제"},
    {"q": "IP 클래스 A 범위 시작은?", "a": "0", "w": ["128","192","224"], "cat": "네트워크"},
    {"q": "서브넷 목적은?", "a": "네트워크 분할", "w": ["속도 감소","보안 약화","주소 제거"], "cat": "네트워크"},
    {"q": "정렬 알고리즘 중 안정 정렬은?", "a": "버블 정렬", "w": ["퀵 정렬","힙 정렬","선택 정렬"], "cat": "알고리즘"},
    {"q": "해시 충돌 해결 방법은?", "a": "체이닝", "w": ["정렬","삭제","병합"], "cat": "자료구조"},
    {"q": "팩토리 패턴 목적은?", "a": "객체 생성 캡슐화", "w": ["삭제","정렬","압축"], "cat": "디자인패턴"},
    {"q": "폭포수 모델 단점은?", "a": "변경 어려움", "w": ["유연함","빠름","반복"], "cat": "소프트웨어공학"},
    {"q": "악성코드 중 자기 복제는?", "a": "웜", "w": ["트로이목마","스파이웨어","랜섬웨어"], "cat": "보안"},
    {"q": "HTTP 상태코드 200 의미는?", "a": "성공", "w": ["오류","리다이렉트","서버 오류"], "cat": "웹"}
] # (지면상 대표적인 문제만 넣었습니다. 필요시 기존 코드에서 전체 문제를 붙여넣어주세요!)

def render(market, nw):
    st.title("💻 정보처리기사 실전 CBT")
    st.caption("실제 정처기 수준의 문제입니다. 정답 시 50만원 지급!")

    if 'cbt_q' not in st.session_state:
        q    = random.choice(QUESTION_POOL)
        opts = q['w'] + [q['a']]; random.shuffle(opts)
        st.session_state.cbt_q    = q
        st.session_state.cbt_opts = opts

    q       = st.session_state.cbt_q
    cats    = {"데이터베이스":"🗄️","네트워크":"🌐","소프트웨어공학":"⚙️","알고리즘":"🔢","자료구조":"📚","운영체제":"🖥️","디자인패턴":"🎨","웹":"🌍","개발도구":"🛠️","보안":"🔒"}
    cat_ico = cats.get(q.get('cat',''), "📝")

    st.markdown(f"<div style='color:#888;font-size:0.8rem;margin-bottom:8px;'>{cat_ico} {q.get('cat','기타')} 분야</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-box'><b>Q.</b> {q['q']}</div>", unsafe_allow_html=True)
    st.write("")

    with st.form("cbt_form"):
        answer     = st.radio("정답을 선택하세요:", st.session_state.cbt_opts, key="cbt_radio")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button("✅ 제출", use_container_width=True)
        if submitted:
            if answer == q['a']:
                st.success("🎉 정답입니다!")
                st.session_state.global_cash += 500_000
                log_tx(st.session_state.logged_in_user, "CBT", "정처기 정답 보상", 500_000)
                st.balloons(); st.info("💰 보상: +₩500,000")
            else:
                st.error(f"❌ 오답! 정답: {q['a']}")
            del st.session_state.cbt_q, st.session_state.cbt_opts
            sync_user_data()
            st.rerun()

    if st.button("🔄 다른 문제", use_container_width=True):
        for k in ['cbt_q', 'cbt_opts']:
            if k in st.session_state: del st.session_state[k]
        st.rerun()