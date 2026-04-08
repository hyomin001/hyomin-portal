import time
import random
import streamlit as st

from database import log_tx, sync_user_data


QUESTION_POOL = [
    {"q": "제2정규형(2NF)의 조건은?", "a": "부분 함수 종속 제거", "w": ["이행 함수 종속 제거","다치 종속 제거","조인 종속 제거"], "cat": "데이터베이스"},
    {"q": "OSI 7계층에서 세그먼트(Segment)를 데이터 단위로 사용하는 계층은?", "a": "전송 계층(Transport Layer)", "w": ["네트워크 계층","세션 계층","데이터링크 계층"], "cat": "네트워크"},
    {"q": "스크럼(Scrum)에서 반복 개발 주기를 의미하는 용어는?", "a": "스프린트(Sprint)", "w": ["이터레이션","릴리즈","에픽"], "cat": "소프트웨어공학"},
    {"q": "트랜잭션의 원자성(Atomicity)이란?", "a": "모두 실행되거나 모두 취소되어야 함", "w": ["동시 트랜잭션 간 독립성 보장","완료 후 영구 반영","실행 전후 무결성 유지"], "cat": "데이터베이스"},
    {"q": "객체 생성을 서브클래스에서 결정하도록 위임하는 패턴은?", "a": "팩토리 메서드(Factory Method)", "w": ["싱글톤","어댑터","옵저버"], "cat": "디자인패턴"},
    {"q": "IP 주소 192.168.1.0/24의 서브넷 마스크는?", "a": "255.255.255.0", "w": ["255.255.0.0","255.0.0.0","255.255.255.128"], "cat": "네트워크"},
    {"q": "SQL LEFT OUTER JOIN의 결과로 옳은 설명은?", "a": "왼쪽 테이블 전체 + 오른쪽 매칭값(없으면 NULL)", "w": ["양쪽 매칭 행만 출력","오른쪽 테이블 전체 포함","매칭 안 되는 행은 제외"], "cat": "데이터베이스"},
    {"q": "퀵 정렬(Quick Sort)의 평균 시간 복잡도는?", "a": "O(n log n)", "w": ["O(n²)","O(n)","O(log n)"], "cat": "알고리즘"},
    {"q": "TCP와 UDP의 핵심 차이점은?", "a": "TCP는 연결 지향, UDP는 비연결 지향", "w": ["TCP가 더 빠름","UDP가 신뢰성 보장","둘 다 응용 계층 프로토콜"], "cat": "네트워크"},
    {"q": "REST API에서 리소스 삭제 시 사용하는 HTTP 메서드는?", "a": "DELETE", "w": ["GET","POST","PUT"], "cat": "웹"},
    {"q": "NoSQL의 특징으로 올바른 것은?", "a": "유연한 스키마 + 수평 확장(Scale-out) 용이", "w": ["ACID 반드시 보장","관계형 모델 전용","수직 확장만 가능"], "cat": "데이터베이스"},
    {"q": "페이징(Paging) 기법의 주요 장점은?", "a": "외부 단편화 제거", "w": ["내부 단편화 제거","메모리 접근 속도 향상","TLB 불필요"], "cat": "운영체제"},
    {"q": "Git에서 원격 저장소 변경사항을 로컬에 병합하는 명령어는?", "a": "git pull", "w": ["git push","git fetch","git clone"], "cat": "개발도구"},
    {"q": "해시 테이블의 평균 검색 시간 복잡도는?", "a": "O(1)", "w": ["O(n)","O(log n)","O(n log n)"], "cat": "자료구조"},
    {"q": "프로세스와 스레드의 차이점으로 올바른 것은?", "a": "스레드는 같은 프로세스 내 메모리를 공유", "w": ["프로세스가 더 가벼움","스레드는 독립적인 메모리 공간 가짐","스레드 생성 비용이 더 큼"], "cat": "운영체제"},
    {"q": "대칭키 암호화 방식의 특징은?", "a": "암호화·복호화에 동일한 키 사용, 처리 속도 빠름", "w": ["공개키·개인키 쌍 사용","키 분배가 안전함","전자서명에 주로 사용"], "cat": "보안"},
]


def render():
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
        answer    = st.radio("정답을 선택하세요:", st.session_state.cbt_opts, key="cbt_radio")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button("✅ 제출", use_container_width=True)
        if submitted:
            if answer == q['a']:
                st.success("🎉 정답입니다!"); st.session_state.global_cash += 500_000
                log_tx(st.session_state.logged_in_user, "CBT", "정처기 정답 보상", 500_000)
                st.balloons(); st.info("💰 보상: +₩500,000")
            else:
                st.error(f"❌ 오답! 정답: {q['a']}")
            del st.session_state.cbt_q, st.session_state.cbt_opts
            sync_user_data(); time.sleep(2.5); st.rerun()

    if st.button("🔄 다른 문제", use_container_width=True):
        for k in ['cbt_q', 'cbt_opts']:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
