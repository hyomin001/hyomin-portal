import streamlit as st
import requests
import json
import re
import time
import random
import pandas as pd
from datetime import datetime

# ==========================================
# 🎨 1. 앱 기본 설정 & 커스텀 CSS (최상단)
# ==========================================
st.set_page_config(page_title="AI 스마트 튜터 PRO", page_icon="🎓", layout="wide")

st.markdown("""
<style>
    /* 전체적인 UI 고급화 */
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px; }
    div[data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; }
    div[data-testid="stMetricDelta"] { font-size: 1.2rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #F3F4F6; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; border-radius: 5px; padding: 0 20px; font-weight: 700; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    /* 버튼 스타일링 */
    .stButton>button { border-radius: 8px; font-weight: bold; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 🔐 2. 환경 변수 및 상태 초기화
# ==========================================
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY", "").strip()
if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY가 설정되지 않았습니다. secrets.toml을 확인하세요.")
    st.stop()

def init_session_state():
    """모든 세션 상태를 안전하게 초기화합니다."""
    defaults = {
        "quiz_data": None,
        "user_answers": {},
        "wrong_questions": [],
        "score_history": [],
        "time_history": [],
        "is_graded": False,
        "start_time": None,
        "end_time": None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==========================================
# 🧠 3. 핵심 비즈니스 로직 (API 및 데이터 처리 클래스)
# ==========================================
class AIQuizGenerator:
    """AI API 통신 및 문제 생성, 예외 처리를 전담하는 클래스"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.models = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite",
            "gemini-2.0-flash"
        ]

    def _extract_and_repair_json(self, text):
        """AI가 반환한 텍스트에서 안전하게 JSON을 추출하고 망가진 부분을 복구합니다."""
        # 1차 시도: 정규식으로 배열 형태 추출
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if not match:
            return None
            
        raw_json = match.group()
        
        # 2차 시도: 정상 파싱
        try:
            return json.loads(raw_json)
        except json.JSONDecodeError:
            pass
            
        # 3차 시도: 작은 문법 오류 자동 복구 (작은따옴표, 후행 쉼표 등)
        try:
            repaired = raw_json.replace("'", '"')
            repaired = re.sub(r",\s*}", "}", repaired)
            repaired = re.sub(r",\s*]", "]", repaired)
            return json.loads(repaired)
        except Exception as e:
            print(f"JSON Parsing Error: {e}")
            return None

    def _validate_format(self, quiz_list):
        """생성된 퀴즈가 시스템 포맷에 완벽히 맞는지 검증합니다."""
        if not isinstance(quiz_list, list) or len(quiz_list) == 0:
            return False
            
        required_keys = {"question", "options", "answer", "explanation", "study_note"}
        for q in quiz_list:
            if not isinstance(q, dict): return False
            if not required_keys.issubset(q.keys()): return False
            if not isinstance(q["options"], list) or len(q["options"]) < 2: return False
        return True

    def generate(self, text, count, difficulty, q_type, keywords):
        """실제 API를 호출하여 모의고사를 생성합니다 (재시도 로직 포함)."""
        keyword_prompt = f"\n특별히 다음 키워드/개념을 중심으로 출제해주세요: {keywords}" if keywords else ""
        
        prompt = f"""
당신은 최고의 1타 강사입니다. 입력된 텍스트를 분석하여 완벽한 객관식 모의고사를 출제하세요.
반드시 아래의 JSON 배열 형식만을 반환해야 합니다. 마크다운 블록(```json)을 쓰지 말고 순수 배열만 출력하세요.

[
  {{
    "question": "명확하고 헷갈리지 않는 문제 내용",
    "options": ["1번 보기", "2번 보기", "3번 보기", "4번 보기"],
    "answer": "정답 텍스트 (반드시 options 배열 안의 텍스트와 100% 일치해야 함)",
    "explanation": "정답인 이유와 오답인 이유에 대한 논리적 해설",
    "study_note": "💡 [1타 강사의 핵심 요약] 학생이 외워야 할 암기 팁이나 관련 심화 개념"
  }}
]

- 출제 문항 수: {count}개
- 난이도: {difficulty}
- 출제 스타일: {q_type}{keyword_prompt}

[학습 텍스트 데이터]
{text[:3000]}
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4, "maxOutputTokens": 4096}
        }

        # 여러 모델을 순회하며 다중 재시도 로직 수행
        for model in self.models:
            url = f"[https://generativelanguage.googleapis.com/v1/models/](https://generativelanguage.googleapis.com/v1/models/){model}:generateContent?key={self.api_key}"
            
            for attempt in range(4): # 최대 4번 재시도
                try:
                    res = requests.post(url, json=payload, timeout=15)
                    if res.status_code == 200:
                        raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                        quiz_data = self._extract_and_repair_json(raw_text)
                        
                        if quiz_data and self._validate_format(quiz_data):
                            return quiz_data
                            
                    elif res.status_code in [429, 503]: # Rate limit or Server Error
                        time.sleep((2 ** attempt) + 1) # 지수 백오프
                except Exception as e:
                    time.sleep(1)
                    continue

        return None # 모든 시도 실패 시

# 인스턴스 생성
generator = AIQuizGenerator(GOOGLE_API_KEY)

# ==========================================
# 📊 4. UI 렌더링 헬퍼 함수들
# ==========================================
def analyze_text_length(text):
    """입력된 텍스트의 품질을 평가합니다."""
    length = len(text)
    if length < 100:
        return "❌ 너무 짧습니다. 최소 100자 이상 입력해주세요.", 0, "error"
    elif length < 500:
        return "⚠️ 내용이 다소 짧아 문제의 다양성이 떨어질 수 있습니다.", 50, "warning"
    elif length < 2000:
        return "✅ 딱 좋은 길이입니다! 고품질 모의고사가 생성됩니다.", 90, "success"
    else:
        return "🔥 아주 풍부한 데이터입니다! 완벽한 시험지가 기대됩니다.", 100, "success"

def export_study_note_as_txt():
    """오답 노트를 다운로드 가능한 텍스트 포맷으로 변환합니다."""
    ss = st.session_state
    if not ss.wrong_questions:
        return "틀린 문제가 없습니다. 완벽합니다!"
        
    content = "🔥 AI 스마트 튜터 - 나의 오답 노트 🔥\n"
    content += f"생성 일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    content += "=" * 50 + "\n\n"
    
    for i, q in enumerate(ss.wrong_questions):
        content += f"Q{i+1}. {q.get('question')}\n"
        content += f"❌ 정답: {q.get('answer')}\n"
        content += f"📝 해설: {q.get('explanation')}\n"
        content += f"👨‍🏫 강사 꿀팁: {q.get('study_note')}\n\n"
        content += "-" * 50 + "\n\n"
        
    return content

# ==========================================
# 🖥️ 5. 메인 앱 화면 구조화
# ==========================================
def render_sidebar():
    """사이드바 대시보드 렌더링"""
    ss = st.session_state
    with st.sidebar:
        st.image("[https://cdn-icons-png.flaticon.com/512/3176/3176378.png](https://cdn-icons-png.flaticon.com/512/3176/3176378.png)", width=80)
        st.title("학습 대시보드")
        st.divider()
        
        if ss.score_history:
            avg_score = sum(ss.score_history) / len(ss.score_history)
            st.metric("누적 평균 점수", f"{avg_score:.1f}점", f"총 {len(ss.score_history)}회 응시")
            
            # Pandas를 이용한 성적 추이 그래프
            st.markdown("#### 📈 성적 추이 그래프")
            df = pd.DataFrame({
                "회차": [f"{i+1}회" for i in range(len(ss.score_history))],
                "점수": ss.score_history
            })
            st.line_chart(df.set_index("회차"), height=200, use_container_width=True)
            
            # 풀이 시간 평균
            if ss.time_history:
                avg_time = sum(ss.time_history) / len(ss.time_history)
                st.caption(f"⏱️ 평균 문제 풀이 시간: {avg_time:.1f}초")
        else:
            st.info("👋 아직 시험 기록이 없습니다.\n\n오른쪽 화면에서 학습할 내용을 넣고 모의고사를 시작해보세요!")
            
        st.divider()
        if st.button("🔄 학습 데이터 전체 초기화", use_container_width=True):
            st.session_state.clear()
            init_session_state()
            st.rerun()

def render_main():
    """메인 화면 (탭) 렌더링"""
    ss = st.session_state
    
    st.title("🔥 AI 스마트 튜터 PRO")
    st.markdown("단순한 모의고사가 아닙니다. **출제, 타이머 측정, 채점, 약점 분석, 오답노트 생성**까지 완벽하게 지원합니다.")
    
    tab_setup, tab_exam, tab_result = st.tabs(["📚 1. 출제 센터", "📝 2. 시험 응시장", "📖 3. 성적 및 오답노트"])

    # ------------------------------------------
    # [TAB 1] 출제 센터
    # ------------------------------------------
    with tab_setup:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📄 학습 데이터 입력")
            text = st.text_area("여기에 공부할 내용(교재, 위키, 기사)을 복사해서 붙여넣으세요.", height=250)
            if text:
                msg, progress, m_type = analyze_text_length(text)
                st.progress(progress / 100)
                if m_type == "error": st.error(msg)
                elif m_type == "warning": st.warning(msg)
                else: st.success(msg)

        with col2:
            st.subheader("⚙️ 출제 알고리즘 설정")
            with st.container(border=True):
                count = st.number_input("📌 문항 수", 3, 20, 5)
                difficulty = st.select_slider("💪 난이도 조정", options=["기초 입문", "보통", "실력 점검", "하드코어"], value="보통")
                q_type = st.selectbox("🎯 문제 스타일", ["핵심 개념 확인", "수능형 응용/추론", "헷갈리는 함정 문제"])
                keywords = st.text_input("🔑 집중 공략 키워드 (선택사항)", placeholder="예: 조건문, 반복문")

        if st.button("🚀 즉시 출제 시작하기", type="primary", use_container_width=True):
            if len(text) < 50:
                st.toast("❌ 텍스트 길이가 너무 짧습니다. 더 길게 입력해주세요!", icon="🚨")
            else:
                with st.spinner("🧠 1타 강사 AI가 지문을 분석하고 고품질 문제를 출제 중입니다... (최대 15초)"):
                    quiz = generator.generate(text, count, difficulty, q_type, keywords)
                    
                    if quiz:
                        # 상태 리셋 및 세팅
                        ss.quiz_data = quiz
                        ss.user_answers = {}
                        ss.wrong_questions = []
                        ss.is_graded = False
                        ss.start_time = time.time() # ⏳ 시험 시작 시간 기록
                        st.toast("🎉 문제 출제 완료! [2. 시험 응시장] 탭으로 이동하세요.", icon="✅")
                    else:
                        st.error("⚠️ 서버가 혼잡하거나 지문이 너무 복잡하여 문제 생성에 실패했습니다. 내용을 조금 수정 후 다시 시도해주세요.")

    # ------------------------------------------
    # [TAB 2] 시험 응시장
    # ------------------------------------------
    with tab_exam:
        if not ss.quiz_data:
            st.info("👈 [1. 출제 센터]에서 먼저 시험지를 만들어주세요.")
        else:
            total_q = len(ss.quiz_data)
            answered_q = len([v for v in ss.user_answers.values() if v != "선택 안함"])
            
            # 상단 진행률 바
            st.progress(answered_q / total_q if total_q > 0 else 0)
            st.markdown(f"**진행 상황:** {answered_q} / {total_q} 문제 완료")
            st.divider()

            # 문제 출력 루프
            for i, q in enumerate(ss.quiz_data):
                with st.container(border=True):
                    st.markdown(f"#### **Q{i+1}.** {q.get('question')}")
                    
                    # 옵션이 없는 에러 방지
                    options = q.get("options", ["보기 1", "보기 2", "보기 3", "보기 4"])
                    
                    ans = st.radio(
                        "정답 선택", ["선택 안함"] + options,
                        key=f"exam_q_{i}", 
                        label_visibility="collapsed", 
                        disabled=ss.is_graded
                    )
                    if ans != "선택 안함":
                        ss.user_answers[i] = ans

            st.markdown("<br>", unsafe_allow_html=True)
            
            # 제출 버튼
            if not ss.is_graded:
                if st.button("💯 OMR 답안지 제출 및 채점", type="primary", use_container_width=True):
                    if answered_q < total_q:
                        st.warning("⚠️ 아직 마킹하지 않은 문제가 있습니다. 꼼꼼히 확인하세요!")
                    else:
                        ss.end_time = time.time() # ⏳ 시험 종료 시간 기록
                        
                        # 채점 로직
                        correct = 0
                        wrong_list = []
                        for i, q in enumerate(ss.quiz_data):
                            if ss.user_answers.get(i) == q.get("answer"):
                                correct += 1
                            else:
                                wrong_list.append(q)
                                
                        score = int((correct / total_q) * 100)
                        time_taken = round(ss.end_time - ss.start_time, 1)
                        
                        ss.score_history.append(score)
                        ss.time_history.append(time_taken)
                        ss.wrong_questions = wrong_list
                        ss.is_graded = True
                        
                        if score == 100: st.balloons()
                        st.toast("✅ 채점 완료! [3. 성적 및 오답노트] 탭을 확인하세요.", icon="🎓")
                        st.rerun()
            else:
                st.success("📝 이미 제출된 답안지입니다. 3번 탭에서 성적표를 확인하세요.")

    # ------------------------------------------
    # [TAB 3] 성적 및 오답노트 (공부 모드)
    # ------------------------------------------
    with tab_result:
        if not ss.is_graded:
            st.info("📝 시험 응시를 완료하고 채점 버튼을 누르면 성적표가 발급됩니다.")
        else:
            total_q = len(ss.quiz_data)
            score = ss.score_history[-1]
            time_taken = ss.time_history[-1]
            
            # 성적표 요약 대시보드
            st.markdown("### 🏆 이번 회차 성적표")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("최종 점수", f"{score}점")
            c2.metric("맞힌 문항", f"{total_q - len(ss.wrong_questions)}개")
            c3.metric("틀린 문항", f"{len(ss.wrong_questions)}개")
            c4.metric("소요 시간", f"{time_taken}초")
            
            st.divider()

            # 1타 강사 해설 모드
            st.markdown("### 👨‍🏫 1타 강사 AI의 밀착 해설 & 오답 노트")
            
            # 다운로드 버튼
            if ss.wrong_questions:
                txt_content = export_study_note_as_txt()
                st.download_button(
                    label="💾 내 오답 노트 다운로드 (.txt)",
                    data=txt_content,
                    file_name=f"오답노트_{datetime.now().strftime('%y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=False
                )
            
            for i, q in enumerate(ss.quiz_data):
                user_ans = ss.user_answers.get(i, "선택 안함")
                real_ans = q.get("answer")
                is_correct = (user_ans == real_ans)

                # 맞춤형 카드 렌더링
                bg_color = "#F0FDF4" if is_correct else "#FEF2F2"
                border_color = "green" if is_correct else "red"
                
                with st.container(border=True):
                    if is_correct:
                        st.markdown(f"**🟢 Q{i+1}. 정답!** (나의 선택: {user_ans})")
                    else:
                        st.markdown(f"**🔴 Q{i+1}. 오답** (나의 선택: {user_ans} / **실제 정답: {real_ans}**)")
                    
                    st.markdown(f"> {q.get('question')}")
                    
                    # 상세 해설
                    st.info(f"**[논리적 해설]**\n{q.get('explanation')}")
                    
                    # 틀린 문제에 대해서만 심화 노트 확장
                    with st.expander("💡 1타 강사의 핵심 요약 노트 (클릭)", expanded=not is_correct):
                        st.write(q.get('study_note', '추가 팁이 없습니다.'))

            st.divider()
            
            # 하단 리트라이 구역
            col_a, col_b = st.columns(2)
            with col_a:
                if ss.wrong_questions:
                    if st.button("🔥 오답만 다시 모아서 복수전 시작", type="primary", use_container_width=True):
                        # 오답 내용을 기반으로 텍스트 재구성
                        retry_text = " ".join([q.get('question') + " " + q.get('explanation') for q in ss.wrong_questions])
                        
                        with st.spinner("오답 기반으로 하드코어 문제를 준비 중입니다..."):
                            new_quiz = generator.generate(retry_text, len(ss.wrong_questions), "하드코어", "헷갈리는 함정 문제", "")
                            
                            if new_quiz:
                                ss.quiz_data = new_quiz
                                ss.user_answers = {}
                                ss.wrong_questions = []
                                ss.is_graded = False
                                ss.start_time = time.time()
                                st.toast("🔥 복수전 세팅 완료! [2. 시험 응시장]으로 이동하세요.", icon="🥊")
                                st.rerun()
                            else:
                                st.error("문제 재생성에 실패했습니다.")
                else:
                    st.success("🎉 완벽합니다! 오답이 없어 복수전이 필요 없습니다.")
            
            with col_b:
                if st.button("🔄 새로운 지문으로 처음부터 다시 시작", use_container_width=True):
                    ss.quiz_data = None
                    ss.is_graded = False
                    st.rerun()

# ==========================================
# 🚀 앱 실행
# ==========================================
if __name__ == "__main__":
    render_sidebar()
    render_main()
