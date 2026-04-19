# pages/project_b.py
# 🗳️ 효민 월드 배틀 — 실시간 진영 투표
import streamlit as st
import time
import html
from datetime import datetime
from utils.config import KST, USERS_FILE
from utils.database import load_db, save_db

VOTE_FILE = "vote_db.json"

def load_vote_db():
    return load_db(VOTE_FILE, {
        "current": {
            "topic":   "아직 주제가 없습니다",
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

# ──────────────────────────────────────────────
# CSS (포털 밝은 테마 위에서 동작)
# ──────────────────────────────────────────────
VOTE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&display=swap');

.vote-wrap {
    font-family: 'Noto Sans KR', sans-serif;
    max-width: 860px;
    margin: 0 auto;
}

/* 상단 타이틀 */
.vote-hero {
    text-align: center;
    padding: 32px 0 20px;
}
.vote-hero-label {
    display: inline-block;
    background: #1E40AF;
    color: #fff;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 3px;
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 14px;
    text-transform: uppercase;
}
.vote-hero-title {
    font-family: 'Black Han Sans', sans-serif;
    font-size: clamp(1.8rem, 4vw, 3rem);
    color: #0F172A;
    line-height: 1.1;
    margin-bottom: 6px;
}
.vote-hero-sub {
    font-size: 0.9rem;
    color: #64748B;
}

/* 전쟁터 */
.battle-arena {
    display: flex;
    gap: 0;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.12);
    margin: 24px 0;
    min-height: 260px;
    position: relative;
}

.side-a, .side-b {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 32px 20px;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(.4,0,.2,1);
    position: relative;
    overflow: hidden;
}
.side-a {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
    color: #fff;
}
.side-b {
    background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);
    color: #fff;
}
.side-a:hover { filter: brightness(1.12); transform: scale(1.01); }
.side-b:hover { filter: brightness(1.12); transform: scale(1.01); }

.vs-badge {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 10;
    background: #fff;
    color: #0F172A;
    font-family: 'Black Han Sans', sans-serif;
    font-size: 1.4rem;
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25);
    border: 3px solid #f1f5f9;
}

.side-label {
    font-family: 'Black Han Sans', sans-serif;
    font-size: clamp(1.4rem, 3vw, 2.2rem);
    margin-bottom: 8px;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    text-align: center;
}
.side-count {
    font-size: 2.8rem;
    font-weight: 900;
    opacity: 0.95;
    line-height: 1;
}
.side-pct {
    font-size: 1rem;
    opacity: 0.75;
    margin-top: 4px;
}

/* 진행 바 */
.bar-wrap {
    background: #E2E8F0;
    border-radius: 999px;
    height: 14px;
    overflow: hidden;
    margin: 4px 0 16px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.08);
}
.bar-fill-a {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #1E3A8A, #3B82F6);
    transition: width 0.8s cubic-bezier(.4,0,.2,1);
    float: left;
}
.bar-fill-b {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #DC2626, #EF4444);
    transition: width 0.8s cubic-bezier(.4,0,.2,1);
    float: right;
}

/* 이미 투표했을 때 내 선택 배지 */
.my-choice-a {
    background: rgba(37,99,235,0.12);
    border: 2px solid #2563EB;
    color: #1E3A8A;
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.92rem;
    display: inline-block;
    margin-top: 8px;
}
.my-choice-b {
    background: rgba(220,38,38,0.10);
    border: 2px solid #DC2626;
    color: #991B1B;
    padding: 8px 20px;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.92rem;
    display: inline-block;
    margin-top: 8px;
}

/* 최근 투표 피드 */
.feed-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 14px;
    border-radius: 8px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    margin-bottom: 6px;
    font-size: 0.88rem;
    color: #475569;
    animation: fadeSlide 0.4s ease;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
}
.dot-a { width:10px; height:10px; border-radius:50%; background:#2563EB; flex-shrink:0; }
.dot-b { width:10px; height:10px; border-radius:50%; background:#DC2626; flex-shrink:0; }

/* 역대 전적 */
.hist-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    border-radius: 10px;
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    margin-bottom: 8px;
    font-size: 0.85rem;
}
.hist-winner { font-weight: 700; }
.win-a { color: #1E3A8A; }
.win-b { color: #991B1B; }
.win-tie { color: #64748B; }

/* 섹션 헤더 */
.sec-head {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #94A3B8;
    text-transform: uppercase;
    margin: 20px 0 10px;
}
</style>
"""

def render():
    st.markdown(VOTE_CSS, unsafe_allow_html=True)

    uid = st.session_state.get('logged_in_user', '')
    is_admin = uid == 'admin'
    vdb = load_vote_db()
    cur = vdb["current"]

    total = len(cur["votes_a"]) + len(cur["votes_b"])
    pct_a = round(len(cur["votes_a"]) / total * 100) if total else 50
    pct_b = 100 - pct_a

    user_voted = uid in cur["votes_a"] or uid in cur["votes_b"]
    user_side  = "A" if uid in cur["votes_a"] else ("B" if uid in cur["votes_b"] else None)

    # ── 히어로 헤더 ──────────────────────────
    st.markdown(f"""
    <div class='vote-wrap'>
      <div class='vote-hero'>
        <div class='vote-hero-label'>🔴 LIVE · 실시간 진영 투표</div>
        <div class='vote-hero-title'>{html.escape(cur['topic'])}</div>
        <div class='vote-hero-sub'>지금 당신의 선택은? 버튼 하나로 진영을 정하세요.</div>
      </div>
    """, unsafe_allow_html=True)

    # ── 전쟁터 (시각적 블록) ─────────────────
    st.markdown(f"""
      <div class='battle-arena'>
        <div class='side-a'>
          <div class='side-label'>{html.escape(cur['side_a'])}</div>
          <div class='side-count'>{len(cur['votes_a'])}<span style='font-size:1rem;opacity:.6;'>표</span></div>
          <div class='side-pct'>{pct_a}%</div>
        </div>
        <div class='vs-badge'>VS</div>
        <div class='side-b'>
          <div class='side-label'>{html.escape(cur['side_b'])}</div>
          <div class='side-count'>{len(cur['votes_b'])}<span style='font-size:1rem;opacity:.6;'>표</span></div>
          <div class='side-pct'>{pct_b}%</div>
        </div>
      </div>
      <div class='bar-wrap'>
        <div class='bar-fill-a' style='width:{pct_a}%'></div>
        <div class='bar-fill-b' style='width:{pct_b}%'></div>
      </div>
      <div style='display:flex;justify-content:space-between;font-size:0.8rem;color:#64748B;margin-bottom:20px;'>
        <span>🔵 {html.escape(cur['side_a'])}</span>
        <span style='color:#94A3B8;'>총 {total}표</span>
        <span>🔴 {html.escape(cur['side_b'])}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 투표 버튼 / 내 선택 표시 ─────────────
    if not uid:
        st.warning("⚠️ 투표하려면 로그인이 필요합니다.")
    elif user_voted:
        choice_label = cur['side_a'] if user_side == 'A' else cur['side_b']
        cls = "my-choice-a" if user_side == 'A' else "my-choice-b"
        st.markdown(f"<div style='text-align:center'><span class='{cls}'>✅ 나의 선택: {html.escape(choice_label)}</span></div>",
                    unsafe_allow_html=True)
        if st.button("🔄 선택 바꾸기", use_container_width=True):
            vdb2 = load_vote_db()
            if uid in vdb2["current"]["votes_a"]:
                vdb2["current"]["votes_a"].remove(uid)
            if uid in vdb2["current"]["votes_b"]:
                vdb2["current"]["votes_b"].remove(uid)
            save_vote_db(vdb2)
            st.rerun()
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"🔵 {cur['side_a']}", use_container_width=True, type="primary"):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_a"]:
                    vdb2["current"]["votes_a"].append(uid)
                save_vote_db(vdb2)
                st.rerun()
        with col_b:
            if st.button(f"🔴 {cur['side_b']}", use_container_width=True):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_b"]:
                    vdb2["current"]["votes_b"].append(uid)
                save_vote_db(vdb2)
                st.rerun()

    st.write("")

    # ── 최근 투표 피드 ───────────────────────
    st.markdown("<div class='sec-head'>최근 투표 현황</div>", unsafe_allow_html=True)

    # 최근 10명 (양쪽 합쳐서 시간순 — 실제로는 저장 순서로 근사)
    feed_a = [(u, 'A') for u in cur["votes_a"][-5:]]
    feed_b = [(u, 'B') for u in cur["votes_b"][-5:]]
    feed = (feed_a + feed_b)[-10:][::-1]

    if feed:
        feed_html = ""
        for voter_uid, side in feed:
            dot_cls = "dot-a" if side == 'A' else "dot-b"
            side_label = html.escape(cur['side_a'] if side == 'A' else cur['side_b'])
            safe_voter = html.escape(voter_uid)
            feed_html += f"<div class='feed-item'><div class='{dot_cls}'></div><b>{safe_voter}</b>님이 <b>{side_label}</b> 선택</div>"
        st.markdown(feed_html, unsafe_allow_html=True)
    else:
        st.markdown("<div class='feed-item'><div class='dot-a'></div>아직 투표가 없습니다. 첫 번째 투표자가 되어보세요!</div>", unsafe_allow_html=True)

    # ── 역대 전적 ────────────────────────────
    if vdb["history"]:
        st.markdown("<div class='sec-head'>역대 전적</div>", unsafe_allow_html=True)
        hist_html = ""
        for h in reversed(vdb["history"][-8:]):
            ta, tb = h['votes_a'], h['votes_b']
            tot_h = ta + tb
            if ta > tb:
                winner_cls = "win-a"
                winner_txt = f"🔵 {html.escape(h['side_a'])} 승"
            elif tb > ta:
                winner_cls = "win-b"
                winner_txt = f"🔴 {html.escape(h['side_b'])} 승"
            else:
                winner_cls = "win-tie"
                winner_txt = "🤝 무승부"
            hist_html += f"""
            <div class='hist-row'>
              <span>{html.escape(h['topic'])}</span>
              <span style='color:#94A3B8;font-size:0.78rem;'>{ta}:{tb} ({tot_h}표)</span>
              <span class='hist-winner {winner_cls}'>{winner_txt}</span>
            </div>"""
        st.markdown(hist_html, unsafe_allow_html=True)

    # ── 관리자 패널 ──────────────────────────
    if is_admin:
        st.write("---")
        st.markdown("#### 🛠️ 관리자 — 주제 변경")
        with st.expander("새 투표 시작하기", expanded=False):
            new_topic  = st.text_input("주제 (예: 짜장 vs 짬뽕)", max_chars=40)
            new_side_a = st.text_input("A 진영 이름", max_chars=20)
            new_side_b = st.text_input("B 진영 이름", max_chars=20)
            if st.button("🚀 새 투표 시작", use_container_width=True, type="primary"):
                if new_topic and new_side_a and new_side_b:
                    vdb2 = load_vote_db()
                    # 현재 투표 기록 보존
                    old = vdb2["current"]
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
                    st.error("주제와 진영 이름을 모두 입력하세요.")
