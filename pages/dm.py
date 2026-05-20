# pages/dm.py
import streamlit as st
import time
import html  # 👈 XSS 방어(HTML 이스케이프)를 위한 모듈
from datetime import datetime
from utils.config import KST
from utils.core import cooldown_remaining, set_cooldown
from utils.config import USERS_FILE, MESSAGES_FILE  # 👈 MESSAGES_FILE 상수 임포트 추가!
from utils.database import load_db, save_db

def render(market, nw):
    st.title("✉️ 1:1 비밀 쪽지함")
    st.markdown("<div style='color:#94A3B8;margin-bottom:16px;'>다른 시민들과 은밀하게 작전을 모의하거나 흥정하세요. 시스템은 여러분의 대화를 엿듣지 않습니다. (아마도요)</div>", unsafe_allow_html=True)

    uid = st.session_state.logged_in_user
    msg_db = load_db(MESSAGES_FILE, {})  # 👈 상수로 교체
    
    if uid not in msg_db:
        msg_db[uid] = {"inbox": [], "outbox": []}

    tab_in, tab_out, tab_send = st.tabs(["📥 받은 편지함", "📤 보낸 편지함", "✍️ 쪽지 쓰기"])

    with tab_in:
        inbox = msg_db[uid].get("inbox", [])
        unread_exist = False
        for m in inbox:
            if not m.get("read", False):
                m["read"] = True
                unread_exist = True
        if unread_exist:
            save_db(MESSAGES_FILE, msg_db)  # 👈 상수로 교체
            
        if not inbox:
            st.info("받은 쪽지가 없습니다.")
        else:
            if st.button("🗑️ 받은 쪽지 모두 비우기", use_container_width=True, type="secondary"):
                msg_db[uid]["inbox"] = []
                save_db(MESSAGES_FILE, msg_db)  # 👈 상수로 교체
                st.success("받은 쪽지함이 비워졌습니다.")
                st.rerun()
                
            st.write("---")
            needs_save = False
            for m in reversed(inbox[-50:]): 
                read_badge = "" if m.get("read_before", False) else "<span style='color:#FF4B4B;font-size:0.75rem;font-weight:900;'>[NEW]</span> "
                if not m.get("read_before", False):
                    m["read_before"] = True 
                    needs_save = True
                
                # 🛡️ XSS 방어: 보낸 사람과 내용을 모두 안전하게 변환
                safe_sender  = html.escape(m.get('sender', '알 수 없음'))
                safe_content = html.escape(m.get('content', ''))
                
                st.markdown(f"""
                <div class='card' style='padding:14px 18px; margin:8px 0; border-left:4px solid #00E5FF;'>
                  <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                    <span style='font-size:0.9rem;'>{read_badge}보낸 사람: <b style='color:#00E5FF;'>{safe_sender}</b></span>
                    <span style='color:#94A3B8;font-size:0.75rem;'>{m.get('time', '')}</span>
                  </div>
                  <div style='color:#CBD5E1;font-size:0.95rem;line-height:1.5;word-break:break-all;'>
                    {safe_content}
                  </div>
                </div>
                """, unsafe_allow_html=True)
                
            if needs_save:
                save_db(MESSAGES_FILE, msg_db)  # 👈 상수로 교체

    with tab_out:
        outbox = msg_db[uid].get("outbox", [])
        if not outbox:
            st.info("보낸 쪽지가 없습니다.")
        else:
            if st.button("🗑️ 보낸 쪽지 모두 비우기", key="clear_outbox", use_container_width=True, type="secondary"):
                msg_db[uid]["outbox"] = []
                save_db(MESSAGES_FILE, msg_db)  # 👈 상수로 교체
                st.success("보낸 쪽지함이 비워졌습니다.")
                st.rerun()
                
            st.write("---")
            for m in reversed(outbox[-50:]):
                
                # 🛡️ XSS 방어: 받는 사람과 내용을 모두 안전하게 변환
                safe_receiver = html.escape(m.get('receiver', '알 수 없음'))
                safe_content  = html.escape(m.get('content', ''))
                
                st.markdown(f"""
                <div class='card' style='padding:14px 18px; margin:8px 0; border-left:4px solid #FFD600; background:rgba(255,215,0,0.02);'>
                  <div style='display:flex;justify-content:space-between;margin-bottom:8px;'>
                    <span style='font-size:0.9rem;color:#94A3B8;'>받는 사람: <b style='color:#FFD600;'>{safe_receiver}</b></span>
                    <span style='color:#94A3B8;font-size:0.75rem;'>{m.get('time', '')}</span>
                  </div>
                  <div style='color:#94A3B8;font-size:0.95rem;line-height:1.5;word-break:break-all;'>
                    {safe_content}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    with tab_send:
        users_db = load_db(USERS_FILE, {})
        user_list = [u for u in users_db.keys() if u != "admin" and u != uid]
        
        if not user_list:
            st.warning("현재 우주에 쪽지를 보낼 다른 시민이 존재하지 않습니다.")
        else:
            target_user = st.selectbox("수신자 선택", user_list)
            msg_content = st.text_area("쪽지 내용", placeholder="여기에 은밀한 메시지를 작성하세요. (최대 500자)", max_chars=500, height=150)
            
            cd_msg = cooldown_remaining("send_dm", 3.0)
            if cd_msg > 0:
                st.warning(f"⏱️ 도배 방지: {cd_msg:.1f}초 후 전송 가능")
            elif st.button("📨 쪽지 전송", use_container_width=True):
                if not msg_content.strip():
                    st.error("내용을 입력해주세요.")
                else:
                    set_cooldown("send_dm")
                    now_str = datetime.now(KST).strftime("%m/%d %H:%M:%S")
                    
                    new_msg_in = {"sender": uid, "content": msg_content.strip(), "time": now_str, "read": False}
                    new_msg_out = {"receiver": target_user, "content": msg_content.strip(), "time": now_str}
                    
                    if target_user not in msg_db:
                        msg_db[target_user] = {"inbox": [], "outbox": []}
                    msg_db[target_user]["inbox"].append(new_msg_in)
                    msg_db[uid]["outbox"].append(new_msg_out)
                    
                    save_db(MESSAGES_FILE, msg_db)  # 👈 상수로 교체
                    st.success(f"✅ {target_user}님에게 쪽지를 성공적으로 전송했습니다!")
                    time.sleep(1)
                    st.rerun()
