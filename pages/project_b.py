# pages/project_b.py
# 🗳️ 효민 월드 배틀 — 실시간 블라인드 진영 투표
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
            "topic":   "오늘의 블라인드 매치를 기다리는 중...",
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

# 🌟 고퀄리티 프리미엄 UI CSS (Toss / Apple 감성)
VOTE_CSS = """
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

.vw-container { 
    font-family: 'Pretendard', sans-serif; 
    max-width: 800px; 
    margin: 0 auto; 
    padding: 20px 10px;
    color: #1E293B;
}

/* 상단 라이브 뱃지 */
.premium-badge {
    display: inline-flex; align-items: center; justify-content: center; gap: 8px;
    background: rgba(15, 23, 42, 0.04); border: 1px solid rgba(15, 23, 42, 0.08);
    border-radius: 30px; padding: 8px 18px; margin-bottom: 30px;
    font-size: 0.85rem; font-weight: 700; color: #475569;
}
.live-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #3B82F6;
    animation: vpulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
@keyframes vpulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

/* 타이틀 섹션 */
.topic-header { text-align: center; margin-bottom: 40px; }
.topic-eyebrow { font-size: 0.85rem; font-weight: 800; color: #3B82F6; letter-spacing: 1px; margin-bottom: 12px; }
.topic-title { font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 900; color: #0F172A; line-height: 1.3; word-break: keep-all; }
.topic-desc { font-size: 1rem; color: #64748B; margin-top: 12px; font-weight: 500; }

/* 블라인드 매치 카드 (투표 전) */
.blind-card {
    background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 24px;
    padding: 50px 20px; text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.03);
    margin-bottom: 20px;
}
.blind-icon { font-size: 3rem; margin-bottom: 15px; opacity: 0.8; }
.blind-text { font-size: 1.2rem; font-weight: 800; color: #0F172A; margin-bottom: 5px; }
.blind-sub { font-size: 0.9rem; color: #94A3B8; font-weight: 500; }

/* 결과 공개 카드 (투표 후) */
.result-arena { display: flex; flex-direction: column; gap: 20px; margin-bottom: 30px; }
.result-row { 
    display: flex; align-items: center; justify-content: space-between;
    background: #F8FAFC; border-radius: 20px; padding: 24px 30px;
    position: relative; overflow: hidden; border: 1px solid #F1F5F9;
}
.result-row.winner { background: #FFFFFF; border: 1px solid #E2E8F0; box-shadow: 0 8px 30px rgba(0,0,0,0.04); }
.result-row.winner::before {
    content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 6px;
    background: #3B82F6; border-radius: 6px 0 0 6px;
}
.result-info { display: flex; flex-direction: column; z-index: 1; }
.result-name { font-size: 1.3rem; font-weight: 800; color: #0F172A; margin-bottom: 4px; }
.result-pct { font-size: 2.2rem; font-weight: 900; color: #3B82F6; line-height: 1; }
.result-row:not(.winner) .result-pct { color: #94A3B8; }
.result-bar-bg { width: 100%; height: 8px; background: #F1F5F9; border-radius: 10px; margin-top: 15px; overflow: hidden; position: relative; z-index: 1; }
.result-bar-fill { height: 100%; background: #3B82F6; border-radius: 10px; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
.result-row:not(.winner) .result-bar-fill { background: #CBD5E1; }

/* 내가 투표한 항목 뱃지 */
.my-pick-badge {
    background: #0F172A; color: #FFFFFF; font-size: 0.75rem; font-weight: 700;
    padding: 4px 10px; border-radius: 12px; margin-left: 10px; vertical-align: middle;
}

/* 역대 전적 (깔끔한 리스트형) */
.history-title { font-size: 1.1rem; font-weight: 800; color: #0F172A; margin: 40px 0 15px 0; padding-bottom: 10px; border-bottom: 2px solid #F1F5F9; }
.history-item { 
    display: flex; justify-content: space-between; align-items: center; 
    padding: 16px 0; border-bottom: 1px solid #F1F5F9;
}
.history-topic { font-size: 0.95rem; font-weight: 600; color: #334155; flex: 1; padding-right: 20px; word-break: keep-all; }
.history-winner { font-size: 0.9rem; font-weight: 800; color: #3B82F6; background: rgba(59, 130, 246, 0.1); padding: 6px 14px; border-radius: 20px; white-space: nowrap; }
.history-tie { color: #64748B; background: rgba(100, 116, 139, 0.1); }
</style>
"""

def render():
    st.markdown(VOTE_CSS, unsafe_allow_html=True)

    uid      = st.session_state.get('logged_in_user', '')
    is_admin = uid == 'admin'
    vdb      = load_vote_db()
    cur      = vdb["current"]

    total   = len(cur["votes_a"]) + len(cur["votes_b"])
    pct_a   = round(len(cur["votes_a"]) / total * 100) if total else 0
    pct_b   = 100 - pct_a if total else 0
    
    voted_a = uid in cur["votes_a"]
    voted_b = uid in cur["votes_b"]
    user_voted = voted_a or voted_b

    s_topic  = html.escape(cur['topic'])
    s_side_a = html.escape(cur['side_a'])
    s_side_b = html.escape(cur['side_b'])

    st.markdown("<div class='vw-container'>", unsafe_allow_html=True)

    # 1. 라이브 뱃지 & 주제
    st.markdown(f"""
    <div style='text-align: center;'>
        <div class='premium-badge'>
            <div class='live-dot'></div> 
            실시간 익명 투표 진행 중
        </div>
    </div>
    <div class='topic-header'>
        <div class='topic-eyebrow'>Q. 오늘의 논제</div>
        <div class='topic-title'>{s_topic}</div>
        <div class='topic-desc'>투표 결과는 철저히 익명으로 보호되며, 참여 후 현황을 확인할 수 있습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 메인 투표 / 결과 UI
    if not uid:
        st.info("💡 투표에 참여하고 사람들의 생각을 확인하려면 먼저 로그인해주세요.")
        
    elif not user_voted:
        # [투표 전] 블라인드 카드 & 선택 버튼
        st.markdown(f"""
        <div class='blind-card'>
            <div class='blind-icon'>🔒</div>
            <div class='blind-text'>결과 블라인드 처리됨</div>
            <div class='blind-sub'>현재 {total}명이 참여했습니다. 나의 선택을 내려 결과를 확인하세요.</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"👈 {cur['side_a']}", use_container_width=True):
                vdb2 = load_vote_db()
                vdb2["current"]["votes_a"].append(uid)
                save_vote_db(vdb2)
                st.rerun()
        with col2:
            if st.button(f"{cur['side_b']} 👉", use_container_width=True):
                vdb2 = load_vote_db()
                vdb2["current"]["votes_b"].append(uid)
                save_vote_db(vdb2)
                st.rerun()

    else:
        # [투표 후] 결과 공개 (우세한 쪽을 강조)
        st.success("✅ 소중한 의견이 익명으로 반영되었습니다!")
        
        is_a_winner = pct_a >= pct_b
        is_b_winner = pct_b >= pct_a
        
        badge_a = "<span class='my-pick-badge'>나의 선택</span>" if voted_a else ""
        badge_b = "<span class='my-pick-badge'>나의 선택</span>" if voted_b else ""
        
        cls_a = "winner" if is_a_winner else ""
        cls_b = "winner" if is_b_winner else ""

        st.markdown(f"""
        <div class='result-arena'>
            <div class='result-row {cls_a}'>
                <div class='result-info'>
                    <div class='result-name'>{s_side_a} {badge_a}</div>
                </div>
                <div style='text-align: right; width: 60%;'>
                    <div class='result-pct'>{pct_a}%</div>
                    <div class='result-bar-bg'><div class='result-bar-fill' style='width: {pct_a}%;'></div></div>
                </div>
            </div>
            
            <div class='result-row {cls_b}'>
                <div class='result-info'>
                    <div class='result-name'>{s_side_b} {badge_b}</div>
                </div>
                <div style='text-align: right; width: 60%;'>
                    <div class='result-pct'>{pct_b}%</div>
                    <div class='result-bar-bg'><div class='result-bar-fill' style='width: {pct_b}%;'></div></div>
                </div>
            </div>
        </div>
        <div style='text-align: center; color: #94A3B8; font-size: 0.85rem; margin-bottom: 20px;'>총 {total}명 참여완료</div>
        """, unsafe_allow_html=True)
        
        # 선택 변경 기능 (선택적)
        if st.button("🔄 마음이 바뀌었습니다 (다시 투표하기)", use_container_width=True):
            vdb2 = load_vote_db()
            vdb2["current"]["votes_a"] = [v for v in vdb2["current"]["votes_a"] if v != uid]
            vdb2["current"]["votes_b"] = [v for v in vdb2["current"]["votes_b"] if v != uid]
            save_vote_db(vdb2)
            st.rerun()

    # 3. 역대 전적 (결과만 심플하게)
    if vdb["history"]:
        st.markdown("<div class='history-title'>📖 명예의 전당 (과거 투표 결과)</div>", unsafe_allow_html=True)
        hist_html = ""
        for h in reversed(vdb["history"][-7:]): # 최근 7개만 노출
            ta, tb = h['votes_a'], h['votes_b']
            if ta > tb:
                win_text = f"👑 {html.escape(h['side_a'])} 승리"
                win_cls = "history-winner"
            elif tb > ta:
                win_text = f"👑 {html.escape(h['side_b'])} 승리"
                win_cls = "history-winner"
            else:
                win_text = "🤝 무승부"
                win_cls = "history-winner history-tie"
                
            hist_html += f"""
            <div class='history-item'>
                <div class='history-topic'>Q. {html.escape(h['topic'])}</div>
                <div class='{win_cls}'>{win_text}</div>
            </div>
            """
        st.markdown(hist_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 4. 관리자 패널 (기존 로직 유지, 디자인 정돈)
    if is_admin:
        st.write("---")
        with st.expander("⚙️ 관리자 전용 — 새 투표 개설", expanded=False):
            st.caption("새 투표를 시작하면 현재 투표는 '명예의 전당'으로 넘어갑니다.")
            new_topic = st.text_input("새로운 논제 (예: 평생 탕수육 부먹 vs 평생 찍먹)", max_chars=50)
            c1, c2 = st.columns(2)
            with c1: new_side_a = st.text_input("👈 A 진영", max_chars=20)
            with c2: new_side_b = st.text_input("👉 B 진영", max_chars=20)
            
            if st.button("🚀 새 투표 시작하기", use_container_width=True, type="primary"):
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
                    st.success("✅ 새 투표가 시작됐습니다!")
                    st.rerun()
                else:
                    st.error("⚠️ 질문과 양쪽 진영 이름을 모두 입력해주세요.")
