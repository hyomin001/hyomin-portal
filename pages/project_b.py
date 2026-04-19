# pages/project_b.py
# 🗳️ 효민 월드 배틀 — 실시간 진영 투표 (Modern UI & Blind Voting)
import streamlit as st
import time
import html
from datetime import datetime
from utils.config import KST
from utils.database import load_db, save_db

VOTE_FILE = "vote_db.json"

def load_vote_db():
    return load_db(VOTE_FILE, {
        "current": {
            "topic":   "오늘의 질문을 기다리는 중...",
            "side_a":  "A",
            "side_b":  "B",
            "votes_a": [],
            "votes_b": [],
            "created": 0,
        },
        "history": []
    })

def save_vote_db(data):
    save_db(VOTE_FILE, data)

# 모던 UI를 위한 커스텀 CSS (Pretendard 폰트 적용 및 글래스모피즘/소프트 섀도우)
VOTE_CSS = """
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.8/dist/web/static/pretendard.css");

.vw { font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif; max-width: 700px; margin: 0 auto; padding: 10px; }

/* 뱃지 & 헤더 */
.live-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(239, 68, 68, 0.1); color: #EF4444;
    border-radius: 20px; padding: 6px 16px; margin-bottom: 24px;
    font-size: 0.85rem; font-weight: 700; letter-spacing: 0.5px;
}
.live-dot { width: 6px; height: 6px; border-radius: 50%; background: #EF4444; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); } 70% { box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }

.topic-wrapper { text-align: center; margin-bottom: 40px; }
.topic-title { font-size: clamp(1.6rem, 4vw, 2.2rem); font-weight: 800; color: #111827; line-height: 1.3; word-break: keep-all; }
.topic-desc { font-size: 0.95rem; color: #6B7280; margin-top: 12px; font-weight: 500; }

/* 카드 섹션 */
.arena { display: flex; gap: 16px; margin-bottom: 30px; align-items: stretch; position: relative; }
.card { 
    flex: 1; border-radius: 24px; padding: 32px 20px; 
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    background: #FFFFFF; border: 1px solid #F3F4F6;
    box-shadow: 0 10px 30px rgba(0,0,0,0.03); position: relative; overflow: hidden;
}
.card-a { border-top: 6px solid #3B82F6; }
.card-b { border-top: 6px solid #EF4444; }

.card-name { font-size: 1.4rem; font-weight: 800; color: #1F2937; text-align: center; z-index: 1; word-break: keep-all; }
.card-result-wrap { margin-top: 16px; text-align: center; z-index: 1; animation: fadeIn 0.5s ease; }
.card-count { font-size: 2.5rem; font-weight: 800; color: #111827; line-height: 1; }
.card-unit { font-size: 1rem; font-weight: 600; color: #6B7280; margin-left: 4px; }
.card-pct { font-size: 1.1rem; font-weight: 700; margin-top: 8px; }
.pct-a { color: #3B82F6; }
.pct-b { color: #EF4444; }

.vs-badge { 
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    width: 40px; height: 40px; border-radius: 50%; background: #F9FAFB; color: #9CA3AF; 
    font-size: 0.9rem; font-weight: 800; display: flex; align-items: center; justify-content: center; 
    box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 2px solid #FFFFFF; z-index: 10;
}

/* 프로그레스 바 */
.ratio-wrap { margin: 10px 0 30px; animation: fadeIn 0.5s ease; }
.ratio-bar { height: 16px; background: #F3F4F6; border-radius: 12px; overflow: hidden; display: flex; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
.ratio-a { background: #3B82F6; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
.ratio-b { background: #EF4444; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
.ratio-footer { display: flex; justify-content: space-between; font-size: 0.85rem; color: #6B7280; margin-top: 10px; font-weight: 600; }

/* 알림 박스 */
.info-box { 
    background: #F8FAFC; border-radius: 16px; padding: 16px 20px; 
    display: flex; align-items: center; gap: 12px; margin-bottom: 24px;
}
.info-icon { font-size: 1.5rem; }
.info-text { font-size: 0.95rem; font-weight: 700; color: #1E293B; }
.info-sub { font-size: 0.8rem; color: #64748B; margin-top: 4px; }

/* 기록 섹션 */
.hist-section { margin-top: 40px; }
.hist-head { font-size: 1.1rem; font-weight: 800; color: #111827; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.hist-row { 
    display: flex; align-items: center; justify-content: space-between; padding: 16px; 
    border-radius: 16px; background: #FFFFFF; border: 1px solid #F3F4F6; 
    margin-bottom: 10px; font-size: 0.9rem; box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}
.hist-topic { flex: 1; color: #374151; font-weight: 600; padding-right: 16px; }
.hist-win-a { color: #3B82F6; font-weight: 700; background: rgba(59,130,246,0.1); padding: 6px 12px; border-radius: 8px; }
.hist-win-b { color: #EF4444; font-weight: 700; background: rgba(239,68,68,0.1); padding: 6px 12px; border-radius: 8px; }
.hist-win-tie { color: #6B7280; font-weight: 700; background: #F3F4F6; padding: 6px 12px; border-radius: 8px; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
</style>
"""

def render():
    st.markdown(VOTE_CSS, unsafe_allow_html=True)

    uid      = st.session_state.get('logged_in_user', '')
    is_admin = uid == 'admin'
    vdb      = load_vote_db()
    cur      = vdb["current"]

    total   = len(cur["votes_a"]) + len(cur["votes_b"])
    pct_a   = round(len(cur["votes_a"]) / total * 100) if total else 50
    pct_b   = 100 - pct_a
    voted_a = uid in cur["votes_a"]
    voted_b = uid in cur["votes_b"]
    user_voted = voted_a or voted_b
    user_side  = "A" if voted_a else ("B" if voted_b else None)

    s_topic  = html.escape(cur['topic'])
    s_side_a = html.escape(cur['side_a'])
    s_side_b = html.escape(cur['side_b'])

    st.markdown("<div class='vw'>", unsafe_allow_html=True)

    # 헤더 섹션
    st.markdown(f"""
    <div style="text-align: center;">
        <div class='live-badge'>
            <div class='live-dot'></div>
            LIVE 실시간 투표
        </div>
    </div>
    <div class='topic-wrapper'>
        <div class='topic-title'>Q. {s_topic}</div>
        <div class='topic-desc'>{"👇 아래에서 진영을 선택하면 결과가 공개됩니다." if not user_voted else "✨ 투표가 완료되었습니다! 현재 결과를 확인하세요."}</div>
    </div>
    """, unsafe_allow_html=True)

    # 투표 카드 & 결과 (블라인드 처리 로직 적용)
    if user_voted:
        # 투표 한 사람에게만 결과(숫자, 게이지) 공개
        st.markdown(f"""
        <div class='arena'>
            <div class='card card-a'>
                <div class='card-name'>🔵 {s_side_a}</div>
                <div class='card-result-wrap'>
                    <div class='card-count'>{len(cur['votes_a'])}<span class='card-unit'>표</span></div>
                    <div class='card-pct pct-a'>{pct_a}%</div>
                </div>
            </div>
            <div class='vs-badge'>VS</div>
            <div class='card card-b'>
                <div class='card-name'>🔴 {s_side_b}</div>
                <div class='card-result-wrap'>
                    <div class='card-count'>{len(cur['votes_b'])}<span class='card-unit'>표</span></div>
                    <div class='card-pct pct-b'>{pct_b}%</div>
                </div>
            </div>
        </div>
        
        <div class='ratio-wrap'>
            <div class='ratio-bar'>
                <div class='ratio-a' style='width:{pct_a}%'></div>
                <div class='ratio-b' style='width:{pct_b}%'></div>
            </div>
            <div class='ratio-footer'>
                <span>참여자 총 {total}명</span>
                <span>익명 투표</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # 투표 전에는 블라인드 뷰 제공
        st.markdown(f"""
        <div class='arena'>
            <div class='card card-a' style='min-height: 160px;'>
                <div class='card-name'>🔵 {s_side_a}</div>
            </div>
            <div class='vs-badge'>VS</div>
            <div class='card card-b' style='min-height: 160px;'>
                <div class='card-name'>🔴 {s_side_b}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 투표 액션 & 상태
    if not uid:
        st.info("💡 투표에 참여하려면 먼저 로그인해주세요.")

    elif user_voted:
        name = s_side_a if user_side == 'A' else s_side_b
        icon = "🔵" if user_side == 'A' else "🔴"
        st.markdown(f"""
        <div class='info-box'>
            <div class='info-icon'>{icon}</div>
            <div>
                <div class='info-text'>[{name}] 진영을 선택하셨습니다.</div>
                <div class='info-sub'>언제든지 아래 버튼을 눌러 선택을 바꿀 수 있습니다.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 마음이 바뀌었어요 (선택 취소)", use_container_width=True):
            vdb2 = load_vote_db()
            vdb2["current"]["votes_a"] = [v for v in vdb2["current"]["votes_a"] if v != uid]
            vdb2["current"]["votes_b"] = [v for v in vdb2["current"]["votes_b"] if v != uid]
            save_vote_db(vdb2)
            st.rerun()

    else:
        # 투표 버튼 영역
        st.markdown("<div style='text-align: center; margin-bottom: 10px; font-size: 0.9rem; font-weight: 600; color: #4B5563;'>어느 쪽을 선택하시겠습니까?</div>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"🔵 {cur['side_a']} 투표하기", use_container_width=True):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_a"]:
                    vdb2["current"]["votes_a"].append(uid)
                save_vote_db(vdb2)
                st.rerun()
        with col_b:
            if st.button(f"🔴 {cur['side_b']} 투표하기", use_container_width=True):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_b"]:
                    vdb2["current"]["votes_b"].append(uid)
                save_vote_db(vdb2)
                st.rerun()

    # 역대 전적 (수치 비공개, 승리 여부만 깔끔하게 노출하여 익명성/호기심 보호)
    if vdb["history"]:
        rows_html = ""
        for h in reversed(vdb["history"][-5:]): # 최근 5개만 노출
            ta, tb = h['votes_a'], h['votes_b']
            if ta > tb:
                win_cls, win_txt = "hist-win-a", f"🔵 {html.escape(h['side_a'])} 승리"
            elif tb > ta:
                win_cls, win_txt = "hist-win-b", f"🔴 {html.escape(h['side_b'])} 승리"
            else:
                win_cls, win_txt = "hist-win-tie", "🤝 무승부"
                
            rows_html += f"""
            <div class='hist-row'>
                <span class='hist-topic'>{html.escape(h['topic'])}</span>
                <span class='{win_cls}'>{win_txt}</span>
            </div>"""

        st.markdown(f"""
        <div class='hist-section'>
            <div class='hist-head'>🏆 최근 종료된 배틀 결과</div>
            {rows_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 관리자 패널
    if is_admin:
        st.write("---")
        st.markdown("#### 🛠️ [관리자] 새 투표 시작")
        with st.expander("주제 설정 패널 열기", expanded=False):
            new_topic = st.text_input("질문 (예: 평생 한 가지만 먹어야 한다면?)", max_chars=50)
            c1, c2 = st.columns(2)
            with c1:
                new_side_a = st.text_input("🔵 A 진영 이름", max_chars=20)
            with c2:
                new_side_b = st.text_input("🔴 B 진영 이름", max_chars=20)
                
            if st.button("🚀 위 주제로 새 투표 라이브 시작", use_container_width=True, type="primary"):
                if new_topic and new_side_a and new_side_b:
                    vdb2 = load_vote_db()
                    old  = vdb2["current"]
                    if old["votes_a"] or old["votes_b"]:
                        vdb2["history"].append({
                            "topic":   old["topic"],
                            "side_a":  old["side_a"],
                            "side_b":  old["side_b"],
                            "votes_a": len(old["votes_a"]),
                            "votes_b": len(old["votes_b"]),
                            "ended":   datetime.now(KST).strftime("%Y-%m-%d"),
                        })
                    vdb2["current"] = {
                        "topic":   new_topic.strip(),
                        "side_a":  new_side_a.strip(),
                        "side_b":  new_side_b.strip(),
                        "votes_a": [],
                        "votes_b": [],
                        "created": time.time(),
                    }
                    save_vote_db(vdb2)
                    st.success("✅ 새 투표가 시작되었습니다!")
                    st.rerun()
                else:
                    st.error("질문과 양쪽 진영 이름을 모두 입력해주세요.")
