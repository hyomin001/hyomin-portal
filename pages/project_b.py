# pages/project_b.py
# 🗳️ 효민 월드 배틀 — 실시간 진영 투표
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

VOTE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;600;700;900&display=swap');

.vw { font-family: 'Noto Sans KR', sans-serif; max-width: 780px; margin: 0 auto; padding: 0 4px; }

.live-banner {
    display: flex; align-items: center; justify-content: center; gap: 10px;
    background: #0F172A; color: #fff;
    border-radius: 12px; padding: 10px 24px; margin-bottom: 28px;
    font-size: 0.8rem; font-weight: 600; letter-spacing: 1px;
}
.live-dot {
    width: 8px; height: 8px; border-radius: 50%; background: #EF4444;
    animation: vpulse 1.4s ease-in-out infinite;
}
@keyframes vpulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(1.5)} }

.topic-block { text-align: center; margin-bottom: 32px; }
.topic-eyebrow { font-size: 0.72rem; font-weight: 700; letter-spacing: 3px; color: #94A3B8; text-transform: uppercase; margin-bottom: 10px; }
.topic-title { font-family: 'Black Han Sans', sans-serif; font-size: clamp(1.6rem, 5vw, 2.8rem); color: #0F172A; line-height: 1.15; }
.topic-sub { font-size: 0.88rem; color: #64748B; margin-top: 8px; }

.arena { display: flex; gap: 12px; margin-bottom: 16px; align-items: stretch; }

.card-a, .card-b {
    flex: 1; border-radius: 20px; padding: 36px 20px 28px;
    display: flex; flex-direction: column; align-items: center;
    position: relative; overflow: hidden; min-height: 230px;
    transition: transform .2s cubic-bezier(.4,0,.2,1), box-shadow .2s;
}
.card-a { background: linear-gradient(160deg, #1E3A8A 0%, #1D4ED8 55%, #3B82F6 100%); box-shadow: 0 12px 40px rgba(29,78,216,.3); }
.card-b { background: linear-gradient(160deg, #7F1D1D 0%, #B91C1C 55%, #EF4444 100%); box-shadow: 0 12px 40px rgba(185,28,28,.3); }
.card-a::before, .card-b::before { content:''; position:absolute; width:200px; height:200px; border-radius:50%; opacity:.1; top:-60px; right:-60px; background:#fff; }

.card-name { font-family: 'Black Han Sans', sans-serif; font-size: clamp(1.2rem, 3.5vw, 1.8rem); color: #fff; text-shadow: 0 2px 12px rgba(0,0,0,.3); text-align: center; margin-bottom: 18px; position: relative; z-index:1; }
.card-count { font-size: 3.2rem; font-weight: 900; color: #fff; line-height: 1; position: relative; z-index:1; }
.card-unit { font-size: 1rem; font-weight: 600; opacity: .7; margin-left: 2px; }
.card-pct  { font-size: 1rem; color: rgba(255,255,255,.75); margin-top: 6px; font-weight: 600; position: relative; z-index:1; }

.my-ribbon { position: absolute; top: 14px; right: -28px; background: #FFD600; color: #000; font-size: .62rem; font-weight: 900; padding: 3px 36px; transform: rotate(35deg); letter-spacing: 1px; box-shadow: 0 2px 8px rgba(0,0,0,.2); }

.vs-wrap { display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.vs-circle { width: 46px; height: 46px; border-radius: 50%; background: #fff; color: #0F172A; font-family: 'Black Han Sans', sans-serif; font-size: 1rem; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(0,0,0,.15); border: 3px solid #E2E8F0; }

.ratio-wrap { margin: 0 0 8px; }
.ratio-labels { display: flex; justify-content: space-between; font-size: .8rem; font-weight: 700; margin-bottom: 6px; color: #334155; }
.ratio-bar { height: 18px; background: #E2E8F0; border-radius: 999px; overflow: hidden; display: flex; }
.ratio-a { background: linear-gradient(90deg, #1E3A8A, #3B82F6); transition: width .9s cubic-bezier(.4,0,.2,1); }
.ratio-b { background: linear-gradient(90deg, #EF4444, #B91C1C); transition: width .9s cubic-bezier(.4,0,.2,1); margin-left: auto; }
.ratio-total { text-align:center; font-size:.78rem; color:#94A3B8; margin-top:7px; }

.voted-box { border-radius: 14px; padding: 14px 18px; margin: 10px 0 14px; display: flex; align-items: center; gap: 12px; }
.voted-a { background: rgba(29,78,216,.07); border: 1.5px solid #3B82F6; }
.voted-b { background: rgba(185,28,28,.07); border: 1.5px solid #EF4444; }
.voted-icon { font-size: 1.4rem; }
.voted-text { font-size: .92rem; font-weight: 700; color: #0F172A; }
.voted-sub  { font-size: .76rem; color: #64748B; margin-top: 2px; }

.hist-section { margin-top: 28px; padding-top: 4px; }
.hist-head { font-size: .72rem; font-weight: 700; letter-spacing: 2.5px; color: #94A3B8; text-transform: uppercase; margin-bottom: 10px; }
.hist-row { display: flex; align-items: center; gap: 10px; padding: 11px 16px; border-radius: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; margin-bottom: 7px; font-size: .84rem; }
.hist-topic { flex: 1; color: #334155; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.hist-score { color: #94A3B8; font-size: .78rem; white-space: nowrap; }
.hist-win-a   { color: #1D4ED8; font-weight: 700; white-space: nowrap; }
.hist-win-b   { color: #B91C1C; font-weight: 700; white-space: nowrap; }
.hist-win-tie { color: #64748B; font-weight: 700; white-space: nowrap; }
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

    # LIVE 배너
    st.markdown("""
    <div class='live-banner'>
      <div class='live-dot'></div>
      LIVE &nbsp;·&nbsp; 실시간 진영 투표 &nbsp;·&nbsp; 효민 월드 배틀
    </div>
    """, unsafe_allow_html=True)

    # 주제
    st.markdown(f"""
    <div class='topic-block'>
      <div class='topic-eyebrow'>오늘의 질문</div>
      <div class='topic-title'>{s_topic}</div>
      <div class='topic-sub'>당신의 선택은? 아래에서 진영을 정하세요.</div>
    </div>
    """, unsafe_allow_html=True)

    # 대결 카드
    ribbon_a = "<div class='my-ribbon'>MY PICK</div>" if voted_a else ""
    ribbon_b = "<div class='my-ribbon'>MY PICK</div>" if voted_b else ""

    st.markdown(f"""
    <div class='arena'>
      <div class='card-a'>
        {ribbon_a}
        <div class='card-name'>{s_side_a}</div>
        <div class='card-count'>{len(cur['votes_a'])}<span class='card-unit'>표</span></div>
        <div class='card-pct'>{pct_a}%</div>
      </div>
      <div class='vs-wrap'><div class='vs-circle'>VS</div></div>
      <div class='card-b'>
        {ribbon_b}
        <div class='card-name'>{s_side_b}</div>
        <div class='card-count'>{len(cur['votes_b'])}<span class='card-unit'>표</span></div>
        <div class='card-pct'>{pct_b}%</div>
      </div>
    </div>
    <div class='ratio-wrap'>
      <div class='ratio-labels'>
        <span style='color:#1D4ED8'>🔵 {s_side_a} {pct_a}%</span>
        <span style='color:#B91C1C'>{pct_b}% {s_side_b} 🔴</span>
      </div>
      <div class='ratio-bar'>
        <div class='ratio-a' style='width:{pct_a}%'></div>
        <div class='ratio-b' style='width:{pct_b}%'></div>
      </div>
      <div class='ratio-total'>총 {total}명 참여 · 투표는 익명으로 집계됩니다</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # 투표 버튼 / 상태
    if not uid:
        st.warning("⚠️ 투표하려면 로그인이 필요합니다.")

    elif user_voted:
        cls  = "voted-a" if user_side == 'A' else "voted-b"
        name = s_side_a   if user_side == 'A' else s_side_b
        icon = "🔵"        if user_side == 'A' else "🔴"
        st.markdown(f"""
        <div class='voted-box {cls}'>
          <div class='voted-icon'>{icon}</div>
          <div>
            <div class='voted-text'>나의 선택: {name}</div>
            <div class='voted-sub'>투표는 익명으로 처리됩니다. 선택을 바꿀 수 있습니다.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 선택 바꾸기", use_container_width=True):
            vdb2 = load_vote_db()
            vdb2["current"]["votes_a"] = [v for v in vdb2["current"]["votes_a"] if v != uid]
            vdb2["current"]["votes_b"] = [v for v in vdb2["current"]["votes_b"] if v != uid]
            save_vote_db(vdb2)
            st.rerun()

    else:
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(f"🔵  {cur['side_a']}", use_container_width=True, type="primary"):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_a"]:
                    vdb2["current"]["votes_a"].append(uid)
                save_vote_db(vdb2)
                st.rerun()
        with col_b:
            if st.button(f"🔴  {cur['side_b']}", use_container_width=True):
                vdb2 = load_vote_db()
                if uid not in vdb2["current"]["votes_b"]:
                    vdb2["current"]["votes_b"].append(uid)
                save_vote_db(vdb2)
                st.rerun()

    # 역대 전적
    if vdb["history"]:
        rows_html = ""
        for h in reversed(vdb["history"][-10:]):
            ta, tb = h['votes_a'], h['votes_b']
            if ta > tb:
                win_cls = "hist-win-a"
                win_txt = f"🔵 {html.escape(h['side_a'])} 승"
            elif tb > ta:
                win_cls = "hist-win-b"
                win_txt = f"🔴 {html.escape(h['side_b'])} 승"
            else:
                win_cls = "hist-win-tie"
                win_txt = "🤝 무승부"
            rows_html += f"""
            <div class='hist-row'>
              <span class='hist-topic'>{html.escape(h['topic'])}</span>
              <span class='hist-score'>{ta} : {tb}</span>
              <span class='{win_cls}'>{win_txt}</span>
            </div>"""

        st.markdown(f"""
        <div class='hist-section'>
          <div class='hist-head'>역대 전적</div>
          {rows_html}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 관리자 패널
    if is_admin:
        st.write("---")
        st.markdown("#### 🛠️ 관리자 — 새 투표 시작")
        with st.expander("주제 설정", expanded=False):
            new_topic = st.text_input("질문 (예: 짜장면 vs 짬뽕)", max_chars=40)
            c1, c2 = st.columns(2)
            with c1:
                new_side_a = st.text_input("🔵 A 진영 이름", max_chars=20)
            with c2:
                new_side_b = st.text_input("🔴 B 진영 이름", max_chars=20)
            if st.button("🚀 새 투표 시작", use_container_width=True, type="primary"):
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
                    st.error("질문과 진영 이름을 모두 입력하세요.")
