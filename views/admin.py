import re
import os
import streamlit as st
import pandas as pd

from config import (
    USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE,
    stock_config,
)
from database import load_db, save_db, save_market


def korean_to_int(text):
    if not text:
        return 0
    if isinstance(text, int) or text.isdigit():
        return int(text)
    text = text.replace(',', '').replace(' ', '')
    units = {"조": 10**12, "억": 10**8, "만": 10**4}
    parts = re.findall(r'[0-9.]+[조억만]?', text)
    if not parts:
        try:
            return int(float(text))
        except Exception:
            return 0
    total = 0
    for part in parts:
        match = re.match(r'([0-9.]+)([조억만]?)', part)
        if match:
            val, unit = match.groups()
            total += float(val) * units.get(unit, 1)
    return int(total)


def render(market):
    st.title("🛠️ 창조주 통제소")
    st.markdown("<div style='color:#FF4B4B;font-size:0.85rem;'>⚠️ 창조주 전용 패널</div>", unsafe_allow_html=True)

    t1, t2, t3, t4 = st.tabs(["👤 유저 조작", "📈 시장 조작", "📢 공지 & 이벤트", "📊 전체 현황"])

    with t1:
        u_db     = load_db(USERS_FILE, {})
        uid_list = [u for u in u_db.keys() if u != "5891"]
        if uid_list:
            sel_u  = st.selectbox("유저 선택", uid_list)
            u_data = u_db[sel_u]
            c1, c2 = st.columns(2)

            with c1:
                st.markdown("##### ✍️ 자산 수정 (한글 단위 가능)")
                raw_cash = st.text_input("현금 설정", value=str(u_data['cash']), help="예: 10억, 1.5조, 5500만")
                raw_loan = st.text_input("대출 설정", value=str(u_data.get('loan', 0)))

                new_cash = korean_to_int(raw_cash)
                new_loan = korean_to_int(raw_loan)

                st.caption(f"💡 변환 결과: 현금 {new_cash:,}원 / 대출 {new_loan:,}원")

            with c2:
                new_title = st.text_input("칭호 설정", value=u_data.get('equipped_title',''))
                st.metric("현재 현금", f"₩{u_data['cash']:,}")
                st.metric("현재 대출", f"₩{u_data.get('loan',0):,}")

            if st.button("⚡ 데이터 즉시 개조", use_container_width=True):
                u_db[sel_u]['cash']           = new_cash
                u_db[sel_u]['loan']           = new_loan
                u_db[sel_u]['equipped_title'] = new_title
                save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 유저의 운명이 바뀌었습니다.")
                st.rerun()

            st.write("---")
            if st.button("🗑️ 유저 데이터 소멸", use_container_width=True, type="secondary"):
                del u_db[sel_u]; save_db(USERS_FILE, u_db)
                st.success(f"✅ {sel_u} 삭제 완료!"); st.rerun()
        else:
            st.info("등록된 유저가 없습니다.")

    with t2:
        st.markdown("### 📈 종목별 가격 조작")
        for s in stock_config:
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            c1.write(f"{s['icon']} {s['name']}")
            c2.write(f"현재: ₩{market['stock_data'][s['id']]['price']:,}")
            if c3.button("🚀 +50%", key=f"up_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = f"🚀 [시장조작] {s['name']} 급등!"; save_market(market); st.rerun()
            if c4.button("📉 -30%", key=f"dn_{s['id']}"):
                market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 0.7)
                market['news'] = f"💣 [시장조작] {s['name']} 폭락!"; save_market(market); st.rerun()

        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔥 전종목 +50% 폭등", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = int(market['stock_data'][s['id']]['price'] * 1.5)
                market['news'] = "🔥 [창조주의 축복] 전 종목 폭등!!!"; save_market(market); st.rerun()
        with c2:
            if st.button("💣 전종목 -40% 폭락", use_container_width=True):
                for s in stock_config: market['stock_data'][s['id']]['price'] = max(1000, int(market['stock_data'][s['id']]['price'] * 0.6))
                market['news'] = "💣 [창조주의 심판] 전 종목 폭락!!!"; save_market(market); st.rerun()

        st.write("---")
        new_lotto = st.number_input("로또 잭팟 설정", value=market['lotto_pool'], step=1_000_000_000)
        if st.button("💰 로또 잭팟 변경"):
            market['lotto_pool'] = new_lotto; save_market(market); st.success("완료!")

    with t3:
        st.markdown("### 📢 공지사항")
        msg_text  = st.text_area("공지 내용", value=market.get('admin_msg', ''), height=100)
        msg_color = st.color_picker("텍스트 색상", value=market.get('admin_color', '#FF4B4B'))
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📣 공지 발령", use_container_width=True):
                market['admin_msg'] = msg_text; market['admin_color'] = msg_color; save_market(market); st.success("공지 발령 완료!")
        with c2:
            if st.button("🗑️ 공지 삭제", use_container_width=True):
                market['admin_msg'] = ""; save_market(market); st.success("공지 삭제 완료!")

        st.write("---")
        st.markdown("### 🎭 특별 이벤트")
        ev_name   = st.text_input("이벤트 이름", placeholder="예: 황금의 시간 🌟")
        ev_target = st.selectbox("대상 종목", [f"{s['icon']} {s['name']}" for s in stock_config])
        ev_mult   = st.slider("변동 배율", min_value=0.5, max_value=5.0, value=2.0, step=0.5)
        if st.button("🎭 이벤트 발동", use_container_width=True):
            ev_sid = next(s['id'] for s in stock_config if f"{s['icon']} {s['name']}" == ev_target)
            market.update({'event_active': True, 'event_name': ev_name, 'event_target': ev_sid, 'event_multiplier': ev_mult})
            market['news'] = f"🎭 [이벤트] {ev_name} 시작! {ev_target} 변동성 {ev_mult}배!"; save_market(market); st.success("이벤트 발동!")
        if st.button("⏹️ 이벤트 종료"):
            market['event_active'] = False; save_market(market); st.success("이벤트 종료!")

    with t4:
        st.markdown("### 📊 전체 유저 현황")
        u_db2 = load_db(USERS_FILE, {})
        rows  = [{"ID": uid, "칭호": ud.get('equipped_title',''), "현금": f"₩{ud.get('cash',0):,}", "대출": f"₩{ud.get('loan',0):,}"} for uid, ud in u_db2.items() if uid != "5891"]
        if rows: st.table(pd.DataFrame(rows))
        else:    st.info("등록된 유저 없음")

        st.write("---")
        st.markdown("### 💾 데이터 백업 상태")
        for f in [USERS_FILE, MARKET_FILE, COMMENTS_FILE, TXLOG_FILE]:
            exists  = "✅" if os.path.exists(f) else "❌"
            bak_ok  = "✅ 백업 있음" if os.path.exists(f + ".bak") else "⚠️ 백업 없음"
            size    = f"{os.path.getsize(f):,} bytes" if os.path.exists(f) else "—"
            st.markdown(f"<div style='color:#aaa;font-size:0.85rem;padding:4px 0;'>{exists} <b style='color:#00E5FF;'>{f}</b> &nbsp; {size} &nbsp; {bak_ok}</div>", unsafe_allow_html=True)

        st.write("---")
        st.markdown("### 💬 게시판 관리")
        if st.button("🗑️ 게시판 전체 삭제"):
            save_db(COMMENTS_FILE, []); st.success("게시판 초기화 완료!")
