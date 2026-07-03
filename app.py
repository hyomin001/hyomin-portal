#수정
import re
import streamlit as st
import time
import os
from datetime import datetime

# ==============================
# 1. 코어 모듈 임포트
# ==============================
from utils.config import MARKET_FILE, USERS_FILE, KST, MESSAGES_FILE, STATS_FILE, estate_config, FORGE_DATA, SEASON_DURATION_DAYS, NEXT_SEASON_DELAY
from utils.database import load_db, save_db, load_stats, save_stats, get_login_lock, set_login_lock, clear_login_lock, check_and_run_season_reset, get_game_meta
from utils.core import hash_pw, hash_pw_bcrypt, verify_pw, is_legacy_hash, format_korean_money, get_net_worth, sync_user_data, ADMIN_HASH, pull_user_data, get_online_users
from utils.market_sync import run_market_sync
from utils.css import GLOBAL_CSS
from components.promo_popup import render_promo_popup

# ==============================
# 2. 페이지 기본 설정
# ==============================
st.set_page_config(page_title="HYOMIN PORTAL", page_icon="🌐", layout="wide", initial_sidebar_state="auto")

# ── Google AdSense 소유권 확인 + 광고 코드 ──────────────────
st.markdown("""
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7480320301712613"
     crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

pull_user_data()

# ── 크론잡 핑 처리 (/health 역할) ──
if st.query_params.get("ping") == "1":
    try:
        check_and_run_season_reset(load_db(MARKET_FILE, {}))
    except Exception as _ping_se:
        import logging
        logging.error(f"[ping season check] 실패: {_ping_se}")
    st.write("ok")
    st.stop()


# last_seen — 60초에 한 번만 DB 쓰기
_now = time.time()
if 'logged_in_user' in st.session_state and st.session_state.logged_in_user:
    if _now - st.session_state.get('_last_seen_write', 0) >= 60:
        _ls_users = load_db(USERS_FILE, {})
        _ls_uid   = st.session_state.logged_in_user
        if _ls_uid in _ls_users:
            _ls_users[_ls_uid]['last_seen'] = _now
            save_db(USERS_FILE, _ls_users)
        st.session_state['_last_seen_write'] = _now

if "page_view" not in st.session_state:
    st.session_state.page_view = "portal"

# ══════════════════════════════════════════════════════════════
# 🎮 게임 결과 처리 — location.href 리로드 후 query_params 저장
# page_view와 무관하게 앱 진입 시 최우선으로 처리
# ══════════════════════════════════════════════════════════════
def _save_game_result():
    """게임 종료 후 URL query_params로 전달된 점수를 MongoDB $set으로 원자적 저장.
    기존 replace_one 방식 대신 $set을 사용해 Race Condition을 완전 차단.
    """
    qp = st.query_params
    _GAME_PARAMS = ['racing_score','zombie_wave','fighter_score','sniper_score','marble_score','dungeon_score']
    if not any(qp.get(p) for p in _GAME_PARAMS):
        return False

    try:
        import logging as _logging
        _logging.warning(f"[DEBUG_SAVE] 진입 params={dict(st.query_params)}")
        from utils.database import (
            get_mongo_client, _get_col, update_leaderboard, load_db
        )
        import logging

        # uid: session_state 우선, 없으면 URL 파라미터에서 복원
        uid = st.session_state.get('logged_in_user', '') or qp.get('_gr_uid', '')
        _logging.warning(f"[DEBUG_SAVE] uid='{uid}' session_uid='{st.session_state.get('logged_in_user','')}' qp_uid='{qp.get('_gr_uid','')}' ")
        if not uid:
            st.query_params.clear()
            return False

        # uid 존재 확인 (projection으로 빠르게)
        client = get_mongo_client()
        col = _get_col(USERS_FILE)
        doc = col.find_one({"_id": "main"}, {uid: 1})
        if not doc or uid not in doc:
            st.query_params.clear()
            return False

        udata = doc[uid]
        user_name = udata.get('nickname', uid)

        # ── 레이싱: 현재 기록보다 높을 때만 $set ──
        if qp.get('racing_score'):
            r_score = int(qp.get('racing_score', 0))
            r_dist  = float(qp.get('racing_dist', 0.0))
            if r_score > 0:
                cur = udata.get('game_records', {}).get('racing', {}).get('score', 0)
                if r_score > cur:
                    col.update_one(
                        {"_id": "main"},
                        {"$set": {
                            f"{uid}.game_records.racing.score": r_score,
                            f"{uid}.game_records.racing.dist":  r_dist,
                        }}
                    )
                    update_leaderboard('racing', user_name, r_score)
                    st.toast(f"🏎️ 레이싱 최고기록 {r_score:,}점 저장!", icon="🏆")
                    if st.session_state.get('logged_in_user') == uid:
                        st.session_state.setdefault('game_records', {}).setdefault('racing', {}).update({'score': r_score, 'dist': r_dist})

        # ── 좀비 ──
        if qp.get('zombie_wave'):
            z_wave  = int(qp.get('zombie_wave', 0))
            z_score = int(qp.get('zombie_score', 0))
            z_kills = int(qp.get('zombie_kills', 0))
            if z_wave > 0:
                cur = udata.get('game_records', {}).get('zombie', {}).get('wave', 0)
                if z_wave > cur:
                    col.update_one(
                        {"_id": "main"},
                        {"$set": {
                            f"{uid}.game_records.zombie.wave":  z_wave,
                            f"{uid}.game_records.zombie.score": z_score,
                            f"{uid}.game_records.zombie.kills": z_kills,
                        }}
                    )
                    update_leaderboard('zombie', user_name, z_wave)
                    st.toast(f"🧟 좀비 최고기록 Wave {z_wave} 저장!", icon="🏆")
                    if st.session_state.get('logged_in_user') == uid:
                        st.session_state.setdefault('game_records', {}).setdefault('zombie', {}).update({'wave': z_wave, 'score': z_score, 'kills': z_kills})

        # ── 격투 ──
        if qp.get('fighter_score'):
            f_score    = int(qp.get('fighter_score', 0))
            f_perfects = int(qp.get('fighter_perfects', 0))
            if f_score > 0:
                cur = udata.get('game_records', {}).get('fighter', {}).get('score', 0)
                if f_score > cur:
                    col.update_one(
                        {"_id": "main"},
                        {"$set": {
                            f"{uid}.game_records.fighter.score":    f_score,
                            f"{uid}.game_records.fighter.perfects": f_perfects,
                        }}
                    )
                    update_leaderboard('fighter', user_name, f_score)
                    st.toast(f"🥊 격투 최고기록 {f_score:,}점 저장!", icon="🏆")
                    if st.session_state.get('logged_in_user') == uid:
                        st.session_state.setdefault('game_records', {}).setdefault('fighter', {}).update({'score': f_score, 'perfects': f_perfects})

        # ── 저격전 ──
        if qp.get('sniper_score'):
            s_score = int(qp.get('sniper_score', 0))
            s_kills = int(qp.get('sniper_kills', 0))
            s_wave  = int(qp.get('sniper_wave', 1))
            if s_score > 0:
                cur = udata.get('game_records', {}).get('sniper', {}).get('score', 0)
                if s_score > cur:
                    col.update_one(
                        {"_id": "main"},
                        {"$set": {
                            f"{uid}.game_records.sniper.score": s_score,
                            f"{uid}.game_records.sniper.kills": s_kills,
                            f"{uid}.game_records.sniper.wave":  s_wave,
                        }}
                    )
                    update_leaderboard('sniper', user_name, s_score)
                    st.toast(f"🎯 저격전 최고기록 {s_score:,}점 저장!", icon="🏆")
                    if st.session_state.get('logged_in_user') == uid:
                        st.session_state.setdefault('game_records', {}).setdefault('sniper', {}).update({'score': s_score, 'kills': s_kills, 'wave': s_wave})

        # ── 인베스트 마블 ──
        if qp.get('marble_score'):
            m_score = int(qp.get('marble_score', 0))
            m_wins  = int(qp.get('marble_wins', 0))
            ms = udata.get('marble_stats', {'wins': 0, 'losses': 0, 'games_played': 0, 'best_net_worth': 0})
            new_played = ms.get('games_played', 0) + 1
            new_wins   = ms.get('wins', 0) + m_wins
            set_fields = {
                f"{uid}.marble_stats.games_played": new_played,
                f"{uid}.marble_stats.wins":         new_wins,
            }
            if m_score > ms.get('best_net_worth', 0):
                set_fields[f"{uid}.marble_stats.best_net_worth"]           = m_score
                set_fields[f"{uid}.game_records.invest_marble.score"]      = m_score
                set_fields[f"{uid}.game_records.invest_marble.wins"]       = new_wins
                update_leaderboard('invest_marble', user_name, m_score)
                st.toast(f"🌍 마블 최고 순자산 ₩{m_score:,} 저장!", icon="🏆")
            col.update_one({"_id": "main"}, {"$set": set_fields})

        # ── 던전 ──
        if qp.get('dungeon_score'):
            from utils.database import atomic_add_cash, log_tx
            from utils.config import KST
            from datetime import datetime, timedelta
            d_score = int(qp.get('dungeon_score', 0))
            d_kills = int(qp.get('dungeon_kills', 0))
            d_win   = qp.get('dungeon_win', 'false') == 'true'
            ds = udata.get('dungeon_stats', {'best_score': 0, 'best_kills': 0, 'clears': 0, 'games_played': 0})
            new_ds = {
                'games_played': ds.get('games_played', 0) + 1,
                'best_score':   max(ds.get('best_score', 0), d_score),
                'best_kills':   max(ds.get('best_kills', 0), d_kills),
                'clears':       ds.get('clears', 0) + (1 if d_win else 0),
            }
            # 주간 랭킹
            now_kst = datetime.now(KST)
            week_start = (now_kst - timedelta(days=now_kst.weekday())).replace(
                hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d')
            dw = udata.get('dungeon_weekly', {})
            if dw.get('week_start') != week_start:
                dw = {'week_start': week_start, 'score': 0, 'kills': 0}
            if d_score > dw.get('score', 0):
                dw['score'] = d_score
                dw['kills'] = d_kills
            set_fields = {
                f"{uid}.dungeon_stats":  new_ds,
                f"{uid}.dungeon_weekly": dw,
            }
            col.update_one({"_id": "main"}, {"$set": set_fields})
            # 보상 지급
            if d_win:
                atomic_add_cash(uid, 200_000_000)
                log_tx(uid, "던전", f"던전런 클리어 (점수:{d_score}, 킬:{d_kills})", 200_000_000)
                st.toast("🏆 던전 클리어! +2억원 보상!", icon="⚔️")
            elif d_score > 0:
                reward = d_score * 1000
                atomic_add_cash(uid, reward)
                log_tx(uid, "던전", f"던전런 점수 보상 (점수:{d_score}, 킬:{d_kills})", reward)
            update_leaderboard('dungeon', user_name, d_score)

    except Exception as _ge:
        import logging
        logging.error(f"[_save_game_result] {_ge}")
        logging.warning(f"[DEBUG_SAVE] 예외발생: {type(_ge).__name__}: {_ge}")

    st.query_params.clear()
    return True

_game_saved = _save_game_result()


# ==============================
# _merge_game_records — game_records 기본값 보장 (clears 필드 포함)
# ==============================
def _merge_game_records(stored: dict) -> dict:
    """DB에 저장된 game_records와 기본값을 병합해 누락 필드를 보완합니다."""
    default = {
        'racing':  {'score': 0, 'dist': 0.0},
        'zombie':  {'wave': 0, 'score': 0, 'kills': 0},
        'fighter': {'score': 0, 'perfects': 0},
        'sniper':  {'score': 0, 'grade': '', 'clears': []},  # clears: 클리어한 미션 인덱스 목록
    }
    result = {}
    for key, dval in default.items():
        db_val = stored.get(key, {})
        merged = {**dval, **db_val}
        # sniper.clears 누락 보완
        if key == 'sniper' and 'clears' not in merged:
            merged['clears'] = []
        result[key] = merged
    return result


# ==============================
# _do_login — 모듈 수준 함수
# ==============================
def _do_login(uid: str, users: dict, device_mode: str):
    u = users[uid]
    st.session_state.update({
        'logged_in_user':    uid,
        'global_cash':       u['cash'],
        'inventory':         u.get('inventory', []),
        'equipped_title':    u.get('equipped_title', '🌱 신규시민'),
        'portfolio':         u.get('portfolio', {}),
        'real_estate':       u.get('real_estate', {}),
        'rent_time':         u.get('rent_time', time.time()),
        'loan':              u.get('loan', 0),
        'loan_time':         u.get('loan_time', time.time()),
        'device_mode':       device_mode,
        'crypto_portfolio':  u.get('crypto_portfolio', {}),
        'daily_quests':      u.get('daily_quests', {}),
        'weapon_level':      u.get('weapon_level', 0),
        'bulk_trade_count':  u.get('bulk_trade_count', 0),
        'bulk_trade_date':   u.get('bulk_trade_date', ''),
        'last_estate_reset': u.get('last_estate_reset', 0),
        'login_fails':       0,
        '_last_seen_write':  0,
        # ✅ [BUG FIX] 로그인 시 누락된 세션 필드 보완
        'gacha_pity':        u.get('gacha_pity', 0),
        'terminal_cleared':  set(u.get('terminal_cleared', [])),
        'dungeon_stats':     u.get('dungeon_stats', {'best_score': 0, 'best_kills': 0, 'clears': 0, 'games_played': 0}),
        'marble_stats':      u.get('marble_stats', {'wins': 0, 'losses': 0, 'games_played': 0, 'best_net_worth': 0}),
        'game_records':      _merge_game_records(u.get('game_records', {})),
    })
    stats    = load_stats()
    today    = datetime.now(KST).strftime("%Y-%m-%d")
    visitors = stats.get("daily_visitors", {})
    if today not in visitors:      visitors[today] = []
    if uid not in visitors[today]: visitors[today].append(uid)
    # 24시간 경과한 날짜 데이터 자동 정리 (오늘 제외 모두 삭제)
    visitors = {k: v for k, v in visitors.items() if k >= today}
    stats["daily_visitors"] = visitors
    save_stats(stats)
    # 로그인 후 pending_page(게임 버튼에서 설정된 목적지)로 이동
    _pending = st.session_state.pop('_pending_page', None)
    _pending_cat  = st.session_state.pop('_pending_menu_cat', None)
    _pending_menu = st.session_state.pop('_pending_menu_page', None)
    st.session_state.page_view = _pending if _pending else "portal"
    if _pending_cat:  st.session_state.current_category = _pending_cat
    if _pending_menu: st.session_state.current_page = _pending_menu
    st.toast("✅ 로그인 성공!", icon="✅")
    st.rerun()


# ==============================
# 🎮 게임 사이트 스타일 포털 CSS
# ==============================
PORTAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Orbitron:wght@700;900&display=swap');

:root {
  --bg:    #060a14;
  --bg2:   #0a1020;
  --bg3:   #0f1830;
  --accent:#6c63ff;
  --cyan:  #00d4ff;
  --gold:  #ffd700;
  --green: #00ff88;
  --red:   #ff3366;
  --border:rgba(108,99,255,0.25);
  --text:  #e8f0ff;
  --text2: #8899bb;
}

/* ── 전체 배경 ── */
.stApp {
  background: var(--bg) !important;
  color: var(--text) !important;
}
.stApp > * { color: var(--text) !important; }

/* ── 파티클 배경 레이어 ── */
.portal-bg {
  position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 70% 50% at 20% 10%, rgba(108,99,255,0.15) 0%, transparent 60%),
    radial-gradient(ellipse 50% 60% at 80% 90%, rgba(0,212,255,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 40% 40% at 60% 40%, rgba(255,215,0,0.06) 0%, transparent 50%);
  animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
  0%   { filter: hue-rotate(0deg) brightness(1); }
  100% { filter: hue-rotate(20deg) brightness(1.05); }
}

/* ── 최상단 HUD 바 ── */
.top-hud {
  background: linear-gradient(90deg, rgba(108,99,255,0.15), rgba(0,212,255,0.10));
  border-bottom: 1px solid var(--border);
  padding: 8px 24px;
  display: flex; align-items: center; justify-content: space-between;
  font-size: 0.78rem; color: var(--text2);
  backdrop-filter: blur(10px);
}
.hud-brand {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem; font-weight: 900;
  background: linear-gradient(135deg, var(--accent), var(--cyan));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: 3px;
}
.hud-live {
  display: inline-flex; align-items: center; gap: 5px;
  color: var(--green); font-weight: 700;
}
.hud-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--green);
  animation: pulse 1.4s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { box-shadow: 0 0 0 0 rgba(0,255,136,0.6); }
  50%     { box-shadow: 0 0 0 6px rgba(0,255,136,0); }
}
.hud-season {
  background: linear-gradient(135deg, var(--gold), #ff8c00);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  font-weight: 900; font-size: 0.82rem;
}

/* ── 히어로 섹션 ── */
.hero {
  text-align: center;
  padding: 60px 20px 40px;
  position: relative;
}
.hero-eyebrow {
  font-size: 0.72rem; letter-spacing: 5px; text-transform: uppercase;
  color: var(--accent); font-weight: 700; margin-bottom: 12px;
}
.hero-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: clamp(3rem, 8vw, 6rem);
  line-height: 1;
  background: linear-gradient(135deg, #fff 0%, var(--cyan) 40%, var(--accent) 70%, var(--gold) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  animation: titleShine 4s ease-in-out infinite alternate;
  margin-bottom: 16px;
}
@keyframes titleShine {
  0%   { filter: drop-shadow(0 0 20px rgba(108,99,255,0.4)); }
  100% { filter: drop-shadow(0 0 40px rgba(0,212,255,0.6)); }
}
.hero-sub {
  color: var(--text2); font-size: 1.05rem; max-width: 580px; margin: 0 auto 24px;
  line-height: 1.7;
}
.hero-badge {
  display: inline-block;
  background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.15));
  border: 1px solid rgba(108,99,255,0.4);
  border-radius: 999px; padding: 6px 18px;
  font-size: 0.78rem; font-weight: 700;
  color: var(--cyan) !important;
  animation: badgeBounce 2s ease-in-out infinite;
}
@keyframes badgeBounce {
  0%,100% { transform: translateY(0); }
  50%     { transform: translateY(-3px); }
}

/* ── 통계 위젯 ── */
.stat-grid { display:flex; gap:14px; margin:24px 0; flex-wrap:wrap; }
.stat-card {
  flex:1; min-width:140px;
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 18px 14px; text-align: center;
  position: relative; overflow: hidden;
  transition: all 0.3s;
}
.stat-card::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, transparent, rgba(108,99,255,0.05));
  opacity: 0; transition: opacity 0.3s;
}
.stat-card:hover { transform: translateY(-4px); border-color: rgba(108,99,255,0.5); }
.stat-card:hover::before { opacity: 1; }
.stat-card.online { border-color: rgba(0,255,136,0.3); }
.stat-card.volume  { border-color: rgba(255,215,0,0.3); }
.stat-icon  { font-size: 1.6rem; margin-bottom: 6px; }
.stat-value { font-family: 'Orbitron', sans-serif; font-size: 1.5rem; font-weight: 900; color: var(--cyan) !important; }
.stat-card.online .stat-value { color: var(--green) !important; }
.stat-card.volume  .stat-value { color: var(--gold)  !important; font-size: 1.1rem; }
.stat-label { font-size: 0.7rem; font-weight: 700; color: var(--text2) !important; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 4px; }

/* ── 슬라이더/배너 ── */
.banner-scroll-wrap {
  overflow: hidden; margin: 30px 0; position: relative;
}
.banner-scroll-wrap::before,
.banner-scroll-wrap::after {
  content: ''; position: absolute; top: 0; bottom: 0; width: 80px; z-index: 2;
}
.banner-scroll-wrap::before { left: 0; background: linear-gradient(90deg, var(--bg), transparent); }
.banner-scroll-wrap::after  { right: 0; background: linear-gradient(-90deg, var(--bg), transparent); }
.banner-scroll-track {
  display: flex; gap: 16px;
  animation: scrollLeft 30s linear infinite;
  width: max-content;
}
.banner-scroll-track:hover { animation-play-state: paused; }
@keyframes scrollLeft {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.scroll-tag {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 999px; padding: 8px 20px;
  font-size: 0.82rem; font-weight: 700; color: var(--text2);
  white-space: nowrap; flex-shrink: 0;
  transition: all 0.3s;
}
.scroll-tag.hot  { border-color: rgba(255,51,102,0.4); color: var(--red)    !important; }
.scroll-tag.new  { border-color: rgba(0,255,136,0.4);  color: var(--green)  !important; }
.scroll-tag.live { border-color: rgba(0,212,255,0.4);  color: var(--cyan)   !important; }
.scroll-tag.gold { border-color: rgba(255,215,0,0.4);  color: var(--gold)   !important; }

/* ── 게임 카드 그리드 ── */
.game-section-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.3rem; color: var(--text);
  letter-spacing: 2px; margin: 30px 0 16px;
  display: flex; align-items: center; gap: 10px;
}
.game-section-title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--border), transparent);
}

.game-card {
  background: linear-gradient(160deg, var(--bg2) 0%, var(--bg3) 100%);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px 22px;
  text-align: center;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
  margin-bottom: 16px;
  min-height: 200px;
  display: flex; flex-direction: column; justify-content: center;
}
.game-card::before {
  content: '';
  position: absolute; top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: conic-gradient(from 0deg, transparent 70%, rgba(108,99,255,0.15) 80%, transparent 90%);
  animation: cardSpin 6s linear infinite;
  opacity: 0; transition: opacity 0.4s;
}
.game-card:hover { transform: translateY(-8px) scale(1.02); border-color: var(--accent); box-shadow: 0 20px 60px rgba(108,99,255,0.3); }
.game-card:hover::before { opacity: 1; }
.card-icon { font-size: 3rem; margin-bottom: 10px; position: relative; z-index: 1; }
.card-title { font-family: 'Black Han Sans', sans-serif; font-size: 1.2rem; color: var(--text) !important; margin-bottom: 6px; position: relative; z-index: 1; letter-spacing: 1px; }
.card-desc  { font-size: 0.82rem; color: var(--text2) !important; line-height: 1.6; position: relative; z-index: 1; }
.card-badge {
  position: absolute; top: 12px; right: 12px;
  font-size: 0.65rem; font-weight: 900; letter-spacing: 1px;
  padding: 3px 9px; border-radius: 999px;
}
.badge-hot  { background: rgba(255,51,102,0.2); color: var(--red)   !important; border: 1px solid rgba(255,51,102,0.4); }
.badge-new  { background: rgba(0,255,136,0.2); color: var(--green)  !important; border: 1px solid rgba(0,255,136,0.4); }
.badge-live { background: rgba(0,212,255,0.2); color: var(--cyan)   !important; border: 1px solid rgba(0,212,255,0.4); }
.badge-gold { background: rgba(255,215,0,0.2); color: var(--gold)   !important; border: 1px solid rgba(255,215,0,0.4); }

/* 카드별 테마 색상 */
.card-universe { border-color: rgba(108,99,255,0.4); }
.card-universe:hover { border-color: var(--accent); box-shadow: 0 20px 60px rgba(108,99,255,0.35); }
.card-academy  { border-color: rgba(0,212,255,0.4); }
.card-academy:hover  { border-color: var(--cyan);   box-shadow: 0 20px 60px rgba(0,212,255,0.35); }
.card-battle   { border-color: rgba(255,51,102,0.4); }
.card-battle:hover   { border-color: var(--red);    box-shadow: 0 20px 60px rgba(255,51,102,0.35); }
.card-terminal { border-color: rgba(0,255,136,0.4); }
.card-terminal:hover { border-color: var(--green);  box-shadow: 0 20px 60px rgba(0,255,136,0.35); }
.card-marble   { border-color: rgba(255,215,0,0.4); }
.card-marble:hover   { border-color: var(--gold);   box-shadow: 0 20px 60px rgba(255,215,0,0.35); }
.card-dungeon  { border-color: rgba(192,78,255,0.4); }
.card-dungeon:hover  { border-color: #c04fff; box-shadow: 0 20px 60px rgba(192,78,255,0.35); }
.card-rank-badge {
  position: absolute; top: 10px; left: 10px; z-index: 10;
  background: rgba(255,215,0,0.12); border: 1px solid rgba(255,215,0,0.35);
  border-radius: 7px; padding: 3px 8px; font-size: 0.68rem; font-weight: 700;
  color: #ffd700; line-height: 1.4; max-width: 120px; backdrop-filter: blur(4px);
}

@keyframes cardSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ── 공지/아키텍처 카드 (다크 테마) ── */
.notice-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 20px 24px; margin-bottom: 14px;
}
.notice-card h4 { color: var(--cyan) !important; margin: 0 0 8px; font-size: 1rem; }
.notice-card p  { color: var(--text2) !important; margin: 0; font-size: 0.88rem; line-height: 1.6; }
.notice-badge {
  display: inline-block; border-radius: 6px; font-size: 0.7rem; font-weight: 800;
  padding: 2px 8px; margin: 3px 3px 0 0;
  background: rgba(108,99,255,0.2); color: var(--accent) !important; border: 1px solid rgba(108,99,255,0.3);
}

/* ── 아키텍처 전용 카드 ── */
.arch-card {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border);
  border-radius: 16px; padding: 22px 24px; margin-bottom: 16px;
}
.arch-card h4 { color: var(--cyan) !important; margin: 0 0 8px 0; font-size: 1.05rem; }
.arch-card p  { color: var(--text2) !important; margin: 0; font-size: 0.92rem; line-height: 1.6; }
.arch-badge {
  display: inline-block;
  background: rgba(108,99,255,0.2); color: var(--accent) !important;
  border: 1px solid rgba(108,99,255,0.3); border-radius: 6px;
  font-size: 0.75rem; font-weight: 700; padding: 2px 9px; margin: 3px 3px 0 0;
}
.arch-highlight {
  background: linear-gradient(90deg, rgba(108,99,255,0.12), rgba(0,212,255,0.08));
  border-left: 4px solid var(--accent); border-radius: 0 10px 10px 0;
  padding: 14px 18px; margin-bottom: 18px;
}
.arch-highlight p { color: var(--text) !important; font-weight: 600; font-size: 0.95rem; margin: 0; }
.arch-highlight p.sub { font-weight: 400; color: var(--text2) !important; font-size: 0.88rem; margin-top: 6px; }
.module-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.module-item {
  background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px;
  padding: 10px 14px; flex: 1; min-width: 180px;
  font-size: 0.85rem; color: var(--text2) !important;
}
.module-item strong { color: var(--cyan) !important; display: block; margin-bottom: 2px; }

/* ── 서비스 가이드 카드 (다크 팁 박스) ── */
.guide-tip-box {
  border-radius: 8px; padding: 10px 12px; margin-top: 10px;
}

/* ── 유저 소통 창구 ── */
.feedback-section-title {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.3rem; color: var(--text);
  letter-spacing: 2px; margin: 36px 0 18px;
  display: flex; align-items: center; gap: 10px;
}
.feedback-section-title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, rgba(0,212,255,0.3), transparent);
}
.feedback-item {
  border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;
  transition: transform 0.2s;
}
.feedback-item:hover { transform: translateX(4px); }
.feedback-checked-badge {
  font-size: 0.72rem; font-weight: 800;
  padding: 2px 8px; border-radius: 999px;
  background: rgba(0,255,136,0.15); color: #00ff88;
  border: 1px solid rgba(0,255,136,0.35);
}
.feedback-unchecked-badge {
  font-size: 0.72rem; font-weight: 700;
  padding: 2px 8px; border-radius: 999px;
  background: rgba(136,153,187,0.1); color: var(--text2);
  border: 1px solid rgba(136,153,187,0.2);
}
.feedback-form-wrap {
  background: linear-gradient(135deg, var(--bg2), var(--bg3));
  border: 1px solid var(--border); border-radius: 16px;
  padding: 20px 22px;
}
.feedback-form-wrap h4 { color: var(--cyan) !important; margin: 0 0 14px; font-size: 1rem; }

/* ── 푸터 ── */
.portal-footer {
  text-align: center; padding: 40px 0;
  color: var(--text2); font-size: 0.78rem;
  border-top: 1px solid var(--border); margin-top: 40px;
}

/* ── Streamlit 버튼 오버라이드 ── */
div[data-testid="stButton"] > button {
  background: linear-gradient(135deg, rgba(108,99,255,0.2), rgba(0,212,255,0.15)) !important;
  border: 1px solid rgba(108,99,255,0.4) !important;
  color: var(--cyan) !important;
  font-weight: 700 !important;
  border-radius: 12px !important;
  transition: all 0.25s !important;
}
div[data-testid="stButton"] > button:hover {
  background: linear-gradient(135deg, rgba(108,99,255,0.4), rgba(0,212,255,0.3)) !important;
  border-color: var(--accent) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(108,99,255,0.35) !important;
}

/* =========================================
   Streamlit 네이티브 UI (셀렉트박스, 아코디언 등) 다크 테마 보정
   ========================================= */

/* 앱 전체 및 헤더 다크 배경 강제 적용 */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* 일반 마크다운 텍스트 및 제목 색상 보정 */
.stMarkdown p, .stMarkdown span { color: var(--text) !important; }
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; }

/* ── ▶ 아코디언 (Expander) 다크 테마 적용 ── */
[data-testid="stExpander"] {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 12px !important;
}
[data-testid="stExpander"] summary p {
  color: var(--cyan) !important;
  font-weight: 700;
  letter-spacing: 0.5px;
}
[data-testid="stExpander"] summary svg {
  fill: var(--cyan) !important;
}

/* ── 🔽 셀렉트 박스 (Selectbox) 다크 테마 적용 ── */
div[data-baseweb="select"] > div {
  background-color: var(--bg2) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
}
/* 드롭다운 클릭 시 펼쳐지는 선택 옵션 리스트 배경 및 글자색 */
div[data-baseweb="popover"] ul, ul[data-testid="stSelectboxVirtualDropdown"] {
  background-color: var(--bg3) !important;
  border: 1px solid var(--border) !important;
}
div[data-baseweb="popover"] li, li[role="option"] {
  color: var(--text) !important;
}
div[data-baseweb="popover"] li:hover, li[role="option"]:hover {
  background-color: rgba(108,99,255,0.2) !important;
  color: var(--cyan) !important;
}

/* ── ✍️ 텍스트 입력창 (Input Box) 다크 테마 적용 ── */
input[type="text"], input[type="password"] {
  background-color: var(--bg2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border) !important;
}
input[type="text"]::placeholder, input[type="password"]::placeholder {
  color: var(--text2) !important;
}

/* ── 알림창(Warning, Info 등) 텍스트 가독성 보호 ── */
div[data-testid="stAlert"] p, div[data-testid="stAlert"] span {
  color: #ffffff !important;
}
</style>
"""


# ==============================
# 3. [View 1] 포털 메인 화면
# ==============================
if st.session_state.page_view == "portal":
    st.markdown(PORTAL_CSS, unsafe_allow_html=True)
    render_promo_popup()  # 🎉 시즌 3 홍보 팝업 (닫기 / 일주일간 보지 않기)
    market = load_db(MARKET_FILE, {})

    # ── 시즌 자동 전환 체크 (market DB 기반, 중복 실행 방지 내장) ──
    try:
        _season_just_reset = check_and_run_season_reset(market)
        if _season_just_reset:
            market = load_db(MARKET_FILE, {})  # 초기화 후 최신 market 재로드
    except Exception as _season_check_e:
        import logging
        logging.error(f"[portal season check] 실패: {_season_check_e}")
        _season_just_reset = False

    # ── 최상단 HUD ──
    _users_db = {}  # 기본값 — 아래 try 블록 실패 시 NameError 방지
    try:
        _stats   = load_stats()
        _today   = datetime.now(KST).strftime("%Y-%m-%d")
        _online  = get_online_users()
        _today_v = len(_stats.get("daily_visitors", {}).get(_today, []))
        _users_db = load_db(USERS_FILE, {})   # ← 단 1회 로드, 아래 랭킹 계산에도 재사용
        _total_s = len([u for u in _users_db if u != "admin"])
    except:
        _online, _today_v, _total_s = 0, 0, 0

    # ── 게임별 1위 랭킹 수집 ──────────────────────────────────
    try:
        # 위에서 로드한 _users_db 재사용 (DB 이중 로드 없음)
        _users_db_for_rank = _users_db

        def _get_game_top(stat_key, val_key, val_fmt='score'):
            best_uid, best_val = '—', 0
            for _uid, _ud in _users_db_for_rank.items():
                if _uid == 'admin': continue
                v = _ud.get(stat_key, {}).get(val_key, 0)
                if isinstance(v, (int, float)) and v > best_val:
                    best_val, best_uid = v, _uid
            if best_val > 0:
                if val_fmt == 'money': disp = format_korean_money(int(best_val))
                elif val_fmt == 'wave': disp = f'{int(best_val)}웨이브'
                else: disp = f'{int(best_val):,}점'
                return best_uid, disp
            return '—', '기록 없음'

        def _get_gr_top(game_key, val_key, val_fmt='score'):
            best_uid, best_val = '—', 0
            for _uid, _ud in _users_db_for_rank.items():
                if _uid == 'admin': continue
                v = _ud.get('game_records', {}).get(game_key, {}).get(val_key, 0)
                if isinstance(v, (int, float)) and v > best_val:
                    best_val, best_uid = v, _uid
            if best_val > 0:
                if val_fmt == 'money': disp = format_korean_money(int(best_val))
                elif val_fmt == 'wave': disp = f'{int(best_val)}웨이브'
                else: disp = f'{int(best_val):,}점'
                return best_uid, disp
            return '—', '기록 없음'

        _r_marble_uid,  _r_marble_val  = _get_game_top('marble_stats', 'best_net_worth', 'money')
        _r_dungeon_uid, _r_dungeon_val = _get_game_top('dungeon_stats', 'best_score', 'score')
        _r_racing_uid,  _r_racing_val  = _get_gr_top('racing',  'score', 'score')
        _r_zombie_uid,  _r_zombie_val  = _get_gr_top('zombie',  'wave',  'wave')
        _r_fighter_uid, _r_fighter_val = _get_gr_top('fighter', 'score', 'score')
        _r_sniper_uid,  _r_sniper_val  = _get_gr_top('sniper',  'score', 'score')
        _r_soccer11_uid, _r_soccer11_val = _get_gr_top('soccer11', 'score', 'score')

        # 터미널: game_records에서 클리어 스테이지 수 기준
        def _get_terminal_top():
            best_uid, best_val = '—', 0
            for _uid, _ud in _users_db_for_rank.items():
                if _uid == 'admin': continue
                v = _ud.get('game_records', {}).get('terminal', {}).get('score', 0)
                # fallback: terminal_cleared 리스트 길이
                if v == 0:
                    v = len(_ud.get('terminal_cleared', []))
                if isinstance(v, (int, float)) and v > best_val:
                    best_val, best_uid = v, _uid
            if best_val > 0:
                return best_uid, f'STAGE {int(best_val)}/20'
            return '—', '기록 없음'
        _r_terminal_uid, _r_terminal_val = _get_terminal_top()

        def _rank_html(uid, val):
            if uid == '—':
                return "<div class='card-rank-badge' style='color:rgba(255,215,0,0.4);border-color:rgba(255,215,0,0.15);'>👑 기록 없음</div>"
            import html as _html
            return f"<div class='card-rank-badge'>👑 {_html.escape(str(uid))}<br><span style='color:#fff;font-weight:900;'>{_html.escape(str(val))}</span></div>"
    except Exception as _re:
        _rank_err = str(_re)
        def _rank_html(uid, val):
            return f"<div class='card-rank-badge' style='color:rgba(255,100,100,0.6);font-size:0.6rem;'>⚠️ err</div>"
        _r_marble_uid = _r_dungeon_uid = _r_racing_uid = '—'
        _r_zombie_uid = _r_fighter_uid = _r_sniper_uid = _r_terminal_uid = '—'
        _r_soccer11_uid = '—'
        _r_marble_val = _r_dungeon_val = _r_racing_val = '—'
        _r_zombie_val = _r_fighter_val = _r_sniper_val = '—'
        _r_terminal_val = '기록 없음'
        _r_soccer11_val = '기록 없음'


    hud_user_txt = f"👤 {st.session_state.logged_in_user}님 접속 중" if st.session_state.get('logged_in_user') else "🔒 비로그인"

    # ── 시즌 정보 (market DB 기반) ──
    _cur_sn       = market.get("season_num", 1)
    _season_end_ts= market.get("season_end", 0)
    _now_ts       = time.time()
    _remain_sec   = max(0, int(_season_end_ts - _now_ts))
    if _remain_sec > 0:
        _dd  = _remain_sec // 86400
        _hh  = (_remain_sec % 86400) // 3600
        _season_label = f"시즌 {_cur_sn} · 종료까지 {_dd}일 {_hh}시간"
    elif _season_end_ts > 0:
        _season_label = f"시즌 {_cur_sn} 종료 · 새 시즌 준비 중"
    else:
        _season_label = f"시즌 {_cur_sn} 진행 중"

    st.markdown(f"""
    <div class='portal-bg'></div>
    <div class='top-hud'>
      <div class='hud-brand'>HYOMIN PORTAL</div>
      <div class='hud-live'><div class='hud-dot'></div> LIVE · 접속자 {_online}명</div>
      <div class='hud-season'>🏆 {_season_label}</div>
      <div style='color:var(--text2);font-size:0.78rem;'>{hud_user_txt}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 새 시즌 시작 축하 배너 (방금 초기화된 경우) ──
    if _season_just_reset:
        st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(108,99,255,0.25),rgba(255,215,0,0.15));
     border:2px solid rgba(255,215,0,0.6);border-radius:16px;padding:20px 24px;margin:12px 0;text-align:center;'>
  <div style='font-size:1.6rem;font-weight:900;color:#ffd700;'>🎉 시즌 {_cur_sn} 시작!</div>
  <div style='color:#e8f0ff;margin-top:8px;font-size:0.95rem;'>
    시즌 {_cur_sn - 1}이 종료되었습니다. 모든 게임 기록이 초기화되었으며 새로운 경쟁이 시작됩니다!<br>
    이번 시즌도 최고 자리를 향해 달려보세요! 🚀
  </div>
</div>
        """, unsafe_allow_html=True)

    # ── 로그인/로그아웃 버튼 ──
    col_empty, col_btn = st.columns([8, 2])
    with col_btn:
        if st.session_state.get('logged_in_user'):
            if st.button("🚪 로그아웃", use_container_width=True):
                sync_user_data(); st.session_state.clear(); st.rerun()
        else:
            if st.button("🔑 로그인 / 회원가입", use_container_width=True):
                st.session_state.page_view = "login"; st.rerun()

    # ── 히어로 섹션 ──
    st.markdown(f"""
    <div class='hero'>
      <div class='hero-eyebrow'>POWERED BY AI · BUILT FOR YOU</div>
      <div class='hero-title'>HYOMIN PORTAL</div>
      <p class='hero-sub'>
        하나의 계정으로 효민 유니버스의 모든 경제, 엔터테인먼트,<br>
        AI 학습, 커뮤니티 서비스를 통합 이용하세요.
      </p>
      <div class='hero-badge'>🛡️ HYOMIN NETWORKS SECURE PLATFORM · 가입 시 5억 지급 · 시즌 {market.get('season_num', 1)} 진행 중</div>
    </div>
    """, unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════
    # 🖼️ 서비스 미리보기 섹션 (비로그인 유저용 소개)
    # ══════════════════════════════════════════════════════════════
    PORTAL_URL = "https://hyomin-app-2gv2xbsxqhrftspwcpgqqw.streamlit.app"  # ← 실제 URL로 변경하세요

    st.markdown("<div class='game-section-title'>🖼️ 서비스 미리보기</div>", unsafe_allow_html=True)

    # ── 서비스 미리보기 위 스크롤 태그 배너 ──
    _prev_tags_html = ""
    _cur_sn = market.get('season_num', 1)
    _prev_tags = [
        (f"🏅 시즌 {max(1, _cur_sn - 1)} 명예의 전당", "gold"), ("📈 주식·코인·부동산", "live"), ("🎰 카지노 & 게임", "hot"),
        ("🏎️ 하이퍼카 레이싱", "new"), ("🔥 HOT", "hot"), (f"🚀 시즌 {_cur_sn} 진행 중", "live"),
        ("🤖 AI 모의고사", "new"), ("🏆 랭킹 1위 쟁탈전", "gold"), ("⚔️ 던전 런 REBORN", "hot"),
        ("🎲 인베스트 마블", "gold"), ("💻 THE TERMINAL", "new"), ("🗳️ 월드 배틀", "live"),
    ]
    for _plabel, _pcls in _prev_tags * 2:
        _prev_tags_html += f"<span class='scroll-tag {_pcls}'>{_plabel}</span>"
    st.markdown(f"<div class='banner-scroll-wrap' style='margin-bottom:16px;'><div class='banner-scroll-track'>{_prev_tags_html}</div></div>", unsafe_allow_html=True)

    _preview_block = """
<style>
@keyframes carousel-slide {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes card-glow-pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(108,99,255,0.15); }
  50%       { box-shadow: 0 0 22px rgba(0,212,255,0.35); }
}
.preview-carousel-wrap {
  overflow: hidden;
  position: relative;
  margin-bottom: 14px;
  /* 양 끝 fade-out */
  mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
}
.preview-carousel-track {
  display: flex;
  gap: 16px;
  width: max-content;
  animation: carousel-slide 28s linear infinite;
}
.preview-carousel-wrap:hover .preview-carousel-track {
  animation-play-state: paused;
}
.preview-card {
  flex: 0 0 220px;
  background: rgba(10,16,32,0.85);
  border-radius: 14px;
  padding: 20px 16px 16px;
  text-align: center;
  position: relative;
  animation: card-glow-pulse 4s ease-in-out infinite;
  transition: transform 0.25s;
}
.preview-card:hover { transform: translateY(-4px); }
.preview-card-icon { font-size: 2.4rem; margin-bottom: 10px; line-height: 1; }
.preview-card-title { font-weight: 900; font-size: 0.88rem; margin-bottom: 6px; }
.preview-card-desc { color: #94A3B8; font-size: 0.75rem; line-height: 1.55; margin-bottom: 10px; }
.preview-tag {
  display: inline-block;
  border-radius: 999px;
  padding: 2px 9px;
  font-size: 0.68rem;
  font-weight: 700;
  margin: 2px 2px 0;
}
</style>

<div style='color:#00d4ff;font-weight:900;font-size:1rem;margin-bottom:4px;text-align:center;'>
  🎮 효민 포털에서 이런 걸 즐길 수 있어요
</div>
<div style='color:#94A3B8;font-size:0.82rem;margin-bottom:14px;text-align:center;'>
  가입 즉시 5억 원 지급 · 시즌 2 진행 중 · 마우스 올리면 멈춰요
</div>

<div class="preview-carousel-wrap">
<div class="preview-carousel-track">

  <!-- 카드 1벌 -->
  <div class="preview-card" style="border:1px solid rgba(0,212,255,0.3);">
    <div class="preview-card-icon">📈</div>
    <div class="preview-card-title" style="color:#00d4ff;">주식 트레이딩</div>
    <div class="preview-card-desc">실시간 변동 주가로<br>10개 종목에 투자</div>
    <span class="preview-tag" style="background:rgba(0,212,255,0.12);color:#00d4ff;">10종목</span>
    <span class="preview-tag" style="background:rgba(0,212,255,0.12);color:#00d4ff;">차트</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,214,0,0.3);">
    <div class="preview-card-icon">₿</div>
    <div class="preview-card-title" style="color:#ffd700;">코인 거래소</div>
    <div class="preview-card-desc">비트코인·이더리움 등<br>5종 코인 실시간 매매</div>
    <span class="preview-tag" style="background:rgba(255,214,0,0.1);color:#ffd700;">5종 코인</span>
    <span class="preview-tag" style="background:rgba(255,214,0,0.1);color:#ffd700;">레버리지</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,255,136,0.3);">
    <div class="preview-card-icon">🏢</div>
    <div class="preview-card-title" style="color:#00ff88;">부동산 임대</div>
    <div class="preview-card-desc">건물 매입 후<br>초당 임대료 수익 획득</div>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">패시브 수익</span>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">건물주</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,51,102,0.3);">
    <div class="preview-card-icon">🏎️</div>
    <div class="preview-card-title" style="color:#ff3366;">네온 도주 레이싱</div>
    <div class="preview-card-desc">5레인 무한 도로<br>니트로 · 경찰 추격</div>
    <span class="preview-tag" style="background:rgba(255,51,102,0.1);color:#ff3366;">×8 콤보</span>
    <span class="preview-tag" style="background:rgba(255,51,102,0.1);color:#ff3366;">랭킹</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,100,0,0.3);">
    <div class="preview-card-icon">🧟</div>
    <div class="preview-card-title" style="color:#ff6400;">좀비 아포칼립스</div>
    <div class="preview-card-desc">탑다운 슈터<br>웨이브 · 4종 무기</div>
    <span class="preview-tag" style="background:rgba(255,100,0,0.1);color:#ff6400;">생존</span>
    <span class="preview-tag" style="background:rgba(255,100,0,0.1);color:#ff6400;">업그레이드</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(192,79,255,0.3);">
    <div class="preview-card-icon">🥊</div>
    <div class="preview-card-title" style="color:#c04fff;">스트리트 파이터</div>
    <div class="preview-card-desc">1v1 격투 · 6캐릭터<br>필살기 · 슈퍼 게이지</div>
    <span class="preview-tag" style="background:rgba(192,79,255,0.1);color:#c04fff;">PVP</span>
    <span class="preview-tag" style="background:rgba(192,79,255,0.1);color:#c04fff;">3라운드</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,229,255,0.3);">
    <div class="preview-card-icon">🎯</div>
    <div class="preview-card-title" style="color:#00e5ff;">라인배틀 저격전</div>
    <div class="preview-card-desc">아군 소환 + 1인칭 저격<br>4가지 난이도</div>
    <span class="preview-tag" style="background:rgba(0,229,255,0.1);color:#00e5ff;">헤드샷</span>
    <span class="preview-tag" style="background:rgba(0,229,255,0.1);color:#00e5ff;">S등급</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,215,0,0.3);">
    <div class="preview-card-icon">⚔️</div>
    <div class="preview-card-title" style="color:#ffd700;">던전 런 REBORN</div>
    <div class="preview-card-desc">뱀서라이크 서바이벌<br>4클래스 · 보스 격파</div>
    <span class="preview-tag" style="background:rgba(255,215,0,0.1);color:#ffd700;">웨이브</span>
    <span class="preview-tag" style="background:rgba(255,215,0,0.1);color:#ffd700;">+2억 보상</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,255,136,0.3);">
    <div class="preview-card-icon">🎲</div>
    <div class="preview-card-title" style="color:#00ff88;">인베스트 마블</div>
    <div class="preview-card-desc">AI 봇과 보드게임 대결<br>30턴 · 6가지 승리조건</div>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">보드게임</span>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">AI 대전</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(108,99,255,0.3);">
    <div class="preview-card-icon">💻</div>
    <div class="preview-card-title" style="color:#6c63ff;">THE TERMINAL</div>
    <div class="preview-card-desc">커맨드라인 방탈출<br>20스테이지 해킹 미션</div>
    <span class="preview-tag" style="background:rgba(108,99,255,0.1);color:#6c63ff;">타임어택</span>
    <span class="preview-tag" style="background:rgba(108,99,255,0.1);color:#6c63ff;">기록 저장</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,140,66,0.3);">
    <div class="preview-card-icon">🗳️</div>
    <div class="preview-card-title" style="color:#ff8c42;">월드 배틀</div>
    <div class="preview-card-desc">매일 새 주제로<br>실시간 진영 투표</div>
    <span class="preview-tag" style="background:rgba(255,140,66,0.1);color:#ff8c42;">매일 갱신</span>
    <span class="preview-tag" style="background:rgba(255,140,66,0.1);color:#ff8c42;">실시간</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(100,200,255,0.3);">
    <div class="preview-card-icon">🧠</div>
    <div class="preview-card-title" style="color:#64c8ff;">AI 무한 모의고사</div>
    <div class="preview-card-desc">Gemini AI가 만드는<br>무한 문제 · PDF 업로드</div>
    <span class="preview-tag" style="background:rgba(100,200,255,0.1);color:#64c8ff;">AI 생성</span>
    <span class="preview-tag" style="background:rgba(100,200,255,0.1);color:#64c8ff;">성적 분석</span>
  </div>

  <!-- 2벌 반복 (무한루프용) -->
  <div class="preview-card" style="border:1px solid rgba(0,212,255,0.3);">
    <div class="preview-card-icon">📈</div>
    <div class="preview-card-title" style="color:#00d4ff;">주식 트레이딩</div>
    <div class="preview-card-desc">실시간 변동 주가로<br>10개 종목에 투자</div>
    <span class="preview-tag" style="background:rgba(0,212,255,0.12);color:#00d4ff;">10종목</span>
    <span class="preview-tag" style="background:rgba(0,212,255,0.12);color:#00d4ff;">차트</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,214,0,0.3);">
    <div class="preview-card-icon">₿</div>
    <div class="preview-card-title" style="color:#ffd700;">코인 거래소</div>
    <div class="preview-card-desc">비트코인·이더리움 등<br>5종 코인 실시간 매매</div>
    <span class="preview-tag" style="background:rgba(255,214,0,0.1);color:#ffd700;">5종 코인</span>
    <span class="preview-tag" style="background:rgba(255,214,0,0.1);color:#ffd700;">레버리지</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,255,136,0.3);">
    <div class="preview-card-icon">🏢</div>
    <div class="preview-card-title" style="color:#00ff88;">부동산 임대</div>
    <div class="preview-card-desc">건물 매입 후<br>초당 임대료 수익 획득</div>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">패시브 수익</span>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">건물주</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,51,102,0.3);">
    <div class="preview-card-icon">🏎️</div>
    <div class="preview-card-title" style="color:#ff3366;">네온 도주 레이싱</div>
    <div class="preview-card-desc">5레인 무한 도로<br>니트로 · 경찰 추격</div>
    <span class="preview-tag" style="background:rgba(255,51,102,0.1);color:#ff3366;">×8 콤보</span>
    <span class="preview-tag" style="background:rgba(255,51,102,0.1);color:#ff3366;">랭킹</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,100,0,0.3);">
    <div class="preview-card-icon">🧟</div>
    <div class="preview-card-title" style="color:#ff6400;">좀비 아포칼립스</div>
    <div class="preview-card-desc">탑다운 슈터<br>웨이브 · 4종 무기</div>
    <span class="preview-tag" style="background:rgba(255,100,0,0.1);color:#ff6400;">생존</span>
    <span class="preview-tag" style="background:rgba(255,100,0,0.1);color:#ff6400;">업그레이드</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(192,79,255,0.3);">
    <div class="preview-card-icon">🥊</div>
    <div class="preview-card-title" style="color:#c04fff;">스트리트 파이터</div>
    <div class="preview-card-desc">1v1 격투 · 6캐릭터<br>필살기 · 슈퍼 게이지</div>
    <span class="preview-tag" style="background:rgba(192,79,255,0.1);color:#c04fff;">PVP</span>
    <span class="preview-tag" style="background:rgba(192,79,255,0.1);color:#c04fff;">3라운드</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,229,255,0.3);">
    <div class="preview-card-icon">🎯</div>
    <div class="preview-card-title" style="color:#00e5ff;">라인배틀 저격전</div>
    <div class="preview-card-desc">아군 소환 + 1인칭 저격<br>4가지 난이도</div>
    <span class="preview-tag" style="background:rgba(0,229,255,0.1);color:#00e5ff;">헤드샷</span>
    <span class="preview-tag" style="background:rgba(0,229,255,0.1);color:#00e5ff;">S등급</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,215,0,0.3);">
    <div class="preview-card-icon">⚔️</div>
    <div class="preview-card-title" style="color:#ffd700;">던전 런 REBORN</div>
    <div class="preview-card-desc">뱀서라이크 서바이벌<br>4클래스 · 보스 격파</div>
    <span class="preview-tag" style="background:rgba(255,215,0,0.1);color:#ffd700;">웨이브</span>
    <span class="preview-tag" style="background:rgba(255,215,0,0.1);color:#ffd700;">+2억 보상</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(0,255,136,0.3);">
    <div class="preview-card-icon">🎲</div>
    <div class="preview-card-title" style="color:#00ff88;">인베스트 마블</div>
    <div class="preview-card-desc">AI 봇과 보드게임 대결<br>30턴 · 6가지 승리조건</div>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">보드게임</span>
    <span class="preview-tag" style="background:rgba(0,255,136,0.1);color:#00ff88;">AI 대전</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(108,99,255,0.3);">
    <div class="preview-card-icon">💻</div>
    <div class="preview-card-title" style="color:#6c63ff;">THE TERMINAL</div>
    <div class="preview-card-desc">커맨드라인 방탈출<br>20스테이지 해킹 미션</div>
    <span class="preview-tag" style="background:rgba(108,99,255,0.1);color:#6c63ff;">타임어택</span>
    <span class="preview-tag" style="background:rgba(108,99,255,0.1);color:#6c63ff;">기록 저장</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(255,140,66,0.3);">
    <div class="preview-card-icon">🗳️</div>
    <div class="preview-card-title" style="color:#ff8c42;">월드 배틀</div>
    <div class="preview-card-desc">매일 새 주제로<br>실시간 진영 투표</div>
    <span class="preview-tag" style="background:rgba(255,140,66,0.1);color:#ff8c42;">매일 갱신</span>
    <span class="preview-tag" style="background:rgba(255,140,66,0.1);color:#ff8c42;">실시간</span>
  </div>

  <div class="preview-card" style="border:1px solid rgba(100,200,255,0.3);">
    <div class="preview-card-icon">🧠</div>
    <div class="preview-card-title" style="color:#64c8ff;">AI 무한 모의고사</div>
    <div class="preview-card-desc">Gemini AI가 만드는<br>무한 문제 · PDF 업로드</div>
    <span class="preview-tag" style="background:rgba(100,200,255,0.1);color:#64c8ff;">AI 생성</span>
    <span class="preview-tag" style="background:rgba(100,200,255,0.1);color:#64c8ff;">성적 분석</span>
  </div>

</div>
</div>

<div style='text-align:center;margin-top:10px;margin-bottom:6px;'>
  <span style='color:#ffd700;font-weight:900;font-size:1rem;'>🎁 가입 즉시 5억 원 지급!</span>
  <span style='color:#94A3B8;font-size:0.82rem;margin-left:10px;'>지금 가입하고 시즌 2 랭킹 경쟁에 참여하세요</span>
</div>
    """
    _preview_block = _preview_block.replace("시즌 2", f"시즌 {market.get('season_num', 1)}")
    st.markdown(_preview_block, unsafe_allow_html=True)

    # ── 실시간 통계 위젯 ──
    try:
        _prices = {k: v['price'] for k, v in market.get('stock_data', {}).items()}
        _top_nw = 0
        _top_uid = "—"
        for _u, _udata in _users_db.items():
            if _u == "admin": continue
            _w = _udata.get('cash', 0) - _udata.get('loan', 0)
            for _sid, _pd in _udata.get('portfolio', {}).items():
                if _sid in _prices: _w += _pd.get('qty', 0) * _prices[_sid]
            for _cid, _ci in _udata.get('crypto_portfolio', {}).items():
                _w += _ci.get('qty', 0) * market.get('crypto_data', {}).get(_cid, {}).get('price', 0)
            for _eid, _cnt in _udata.get('real_estate', {}).items():
                if _eid in estate_config: _w += estate_config[_eid]['base_price'] * _cnt * 0.8
            _wlv = _udata.get('weapon_level', 0)
            if _wlv > 0 and _wlv in FORGE_DATA: _w += FORGE_DATA[_wlv]['sell']
            if _w > _top_nw:
                _top_nw = _w
                _top_uid = _u
        _nw_str = format_korean_money(_top_nw) if _top_nw > 0 else "0원"
    except:
        _top_uid, _nw_str = "집계 중", "—"

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card online">
        <div class="stat-icon">🟢</div>
        <div class="stat-value">{_online}</div>
        <div class="stat-label">지금 접속 중</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📅</div>
        <div class="stat-value">{_today_v}</div>
        <div class="stat-label">오늘 방문자</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-value">{_total_s}</div>
        <div class="stat-label">누적 가입자</div>
      </div>
      <div class="stat-card volume">
        <div class="stat-icon">👑</div>
        <div class="stat-value">{_nw_str}</div>
        <div class="stat-label">자산1위: {_top_uid}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='game-section-title'>🎮 서비스 입장</div>", unsafe_allow_html=True)

    # ── 게임 카드 그리드 ──
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class='game-card card-universe' style='position:relative;'>
          <div class='card-badge badge-live'>🔴 LIVE</div>
          <div class='card-icon'>🌌</div>
          <div class='card-title'>HYOMIN UNIVERSE</div>
          <div class='card-desc'>자본주의 생존 시뮬레이션 · 시즌 2 예고<br>주식·코인·부동산·게임 통합 경제</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("유니버스 입장 🚀", use_container_width=True, key="btn_uni"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "universe"
            else:
                st.session_state['_pending_page'] = "universe"
                st.session_state.page_view = "login"
            st.rerun()

        st.markdown("""
        <div class='game-card card-battle' style='margin-top:16px;position:relative;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          <div class='card-icon'>🗳️</div>
          <div class='card-title'>WORLD BATTLE</div>
          <div class='card-desc'>실시간 진영 투표 배틀<br>오늘의 질문에 참전하라!</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("지금 투표하기 ⚔️", use_container_width=True, key="btn_battle"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_b"
            else:
                st.session_state['_pending_page'] = "project_b"
                st.session_state.page_view = "login"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='game-card card-academy' style='position:relative;'>
          <div class='card-badge badge-new'>✨ NEW</div>
          <div class='card-icon'>🧠</div>
          <div class='card-title'>AI 아카데미</div>
          <div class='card-desc'>AI가 만드는 무한 모의고사<br>Gemini 2.5 Flash 탑재</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("AI 아카데미 입장 📚", use_container_width=True, key="btn_acad"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_a"
            else:
                st.session_state['_pending_page'] = "project_a"
                st.session_state.page_view = "login"
            st.rerun()

        st.markdown(f"""
        <div class='game-card card-marble' style='margin-top:16px;position:relative;'>
          <div class='card-badge badge-gold'>🏆 PICK</div>
          {_rank_html(_r_marble_uid, _r_marble_val)}
          <div class='card-icon'>🎲</div>
          <div class='card-title'>인베스트 마블 ULTRA</div>
          <div class='card-desc'>AI 봇과 보드게임 대결<br>이동 애니 · 미니게임 · 30턴 제한</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎲 마블 입장", use_container_width=True, key="btn_marble"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_d"
            else:
                st.session_state['_pending_page'] = "project_d"
                st.session_state.page_view = "login"
            st.rerun()

    with col3:
        st.markdown(f"""
        <div class='game-card card-terminal' style='position:relative;'>
          <div class='card-badge badge-new'>💡 도전</div>
          {_rank_html(_r_terminal_uid, _r_terminal_val)}
          <div class='card-icon'>💻</div>
          <div class='card-title'>THE TERMINAL</div>
          <div class='card-desc'>커맨드라인 방탈출 어드벤처<br>20 스테이지 · 타임어택 모드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("터미널 접속 >_", use_container_width=True, key="btn_term"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_c"
            else:
                st.session_state['_pending_page'] = "project_c"
                st.session_state.page_view = "login"
            st.rerun()

        st.markdown(f"""
        <div class='game-card card-dungeon' style='margin-top:16px;position:relative;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          {_rank_html(_r_dungeon_uid, _r_dungeon_val)}
          <div class='card-icon'>⚔️</div>
          <div class='card-title'>던전 런 REBORN</div>
          <div class='card-desc'>뱀서라이크 서바이벌 던전<br>4 클래스 · 웨이브 보스 격파</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("던전 입장 ⚔️", use_container_width=True, key="btn_dungeon"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_e"
            else:
                st.session_state['_pending_page'] = "project_e"
                st.session_state.page_view = "login"
            st.rerun()

    # ── 신규 게임 행 ──────────────────────────────────────────
    st.markdown("<div class='game-section-title'>🆕 신규 게임 추가</div>", unsafe_allow_html=True)
    nc1, nc2, nc3, nc4, nc5 = st.columns(5)

    with nc1:
        st.markdown(f"""
        <div class='game-card' style='border-color:rgba(0,212,255,0.4);min-height:180px;position:relative;'>
          <div class='card-badge badge-new'>🆕 NEW</div>
          {_rank_html(_r_racing_uid, _r_racing_val)}
          <div class='card-icon'>🏎️</div>
          <div class='card-title'>네온 도주 레이싱</div>
          <div class='card-desc'>5레인 무한 도로 · 니트로 부스터<br>경찰 추격 · ×8 콤보 시스템</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("레이싱 입장 🏎️", use_container_width=True, key="btn_f"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_f"
            else:
                st.session_state['_pending_page'] = "project_f"
                st.session_state.page_view = "login"
            st.rerun()

    with nc2:
        st.markdown(f"""
        <div class='game-card' style='border-color:rgba(255,34,68,0.4);min-height:180px;position:relative;'>
          <div class='card-badge badge-hot'>🔥 HOT</div>
          {_rank_html(_r_zombie_uid, _r_zombie_val)}
          <div class='card-icon'>🧟</div>
          <div class='card-title'>좀비 아포칼립스</div>
          <div class='card-desc'>탑다운 좀비 슈터 · 4종 무기<br>웨이브 + 상점 업그레이드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("생존 입장 🧟", use_container_width=True, key="btn_g"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_g"
            else:
                st.session_state['_pending_page'] = "project_g"
                st.session_state.page_view = "login"
            st.rerun()

    with nc3:
        st.markdown(f"""
        <div class='game-card' style='border-color:rgba(192,79,255,0.4);min-height:180px;position:relative;'>
          <div class='card-badge' style='background:rgba(192,79,255,0.2);color:#c04fff;border:1px solid rgba(192,79,255,0.4);'>⚡ PVP</div>
          {_rank_html(_r_fighter_uid, _r_fighter_val)}
          <div class='card-icon'>🥊</div>
          <div class='card-title'>스트리트 파이터 EX</div>
          <div class='card-desc'>1v1 격투 · 6 캐릭터 · AI CPU<br>필살기 · 슈퍼 게이지 · 3라운드</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("대전 입장 🥊", use_container_width=True, key="btn_h"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_h"
            else:
                st.session_state['_pending_page'] = "project_h"
                st.session_state.page_view = "login"
            st.rerun()

    with nc4:
        st.markdown(f"""
        <div class='game-card' style='border-color:rgba(255,140,66,0.4);min-height:180px;position:relative;'>
          <div class='card-badge' style='background:rgba(255,140,66,0.15);color:#ff8c42;border:1px solid rgba(255,140,66,0.35);'>⚔️ NEW</div>
          {_rank_html(_r_sniper_uid, _r_sniper_val)}
          <div class='card-icon'>🎯</div>
          <div class='card-title'>라인 배틀 저격전</div>
          <div class='card-desc'>Age of War · 4가지 난이도<br>유닛 소환 + 1인칭 저격 지원</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚔️ 저격전 입장", use_container_width=True, key="btn_i"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_i"
            else:
                st.session_state['_pending_page'] = "project_i"
                st.session_state.page_view = "login"
            st.rerun()

    with nc5:
        st.markdown(f"""
        <div class='game-card' style='border-color:rgba(46,168,255,.4);min-height:180px;position:relative;'>
          <div class='card-badge badge-new'>🆕 NEW</div>
          {_rank_html(_r_soccer11_uid, _r_soccer11_val)}
          <div class='card-icon'>⚽</div>
          <div class='card-title'>얼티밋 사커 11</div>
          <div class='card-desc'>11 vs 11 실시간 축구 매치<br>공수 전환 조작 · 3분 1경기</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚽ 매치 입장", use_container_width=True, key="btn_j"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "project_j"
            else:
                st.session_state['_pending_page'] = "project_j"
                st.session_state.page_view = "login"
            st.rerun()



    # ── 유저 성장 서비스 ──────────────────────────────────────
    st.markdown("<div class='game-section-title'>🌱 유저 성장 서비스</div>", unsafe_allow_html=True)
    pc1, pc2 = st.columns(2)

    with pc1:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(0,229,255,0.45);min-height:180px;position:relative;'>
          <div class='card-badge' style='background:rgba(0,229,255,0.15);color:#00E5FF;border:1px solid rgba(0,229,255,0.4);'>👤 프로필</div>
          <div class='card-icon'>🧑‍🚀</div>
          <div class='card-title'>내 프로필</div>
          <div class='card-desc'>아바타 · 배지 컬렉션 · 게임 기록<br>성장 타임라인 · 상태 메시지 설정</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("프로필 보기 👤", use_container_width=True, key="btn_profile"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "universe"
                st.session_state.current_category = "🌟 성장 & 혜택"
                st.session_state.current_page = "👤 내 프로필"
            else:
                st.session_state['_pending_page'] = "universe"
                st.session_state['_pending_menu_cat'] = "🌟 성장 & 혜택"
                st.session_state['_pending_menu_page'] = "👤 내 프로필"
                st.session_state.page_view = "login"
            st.rerun()

    with pc2:
        st.markdown("""
        <div class='game-card' style='border-color:rgba(0,255,136,0.45);min-height:180px;position:relative;'>
          <div class='card-badge' style='background:rgba(0,255,136,0.15);color:#00FF88;border:1px solid rgba(0,255,136,0.4);'>🐾 펫</div>
          <div class='card-icon'>🐾</div>
          <div class='card-title'>펫 키우기</div>
          <div class='card-desc'>8종 펫 입양 · 훈련 · 악세서리 장착<br>레벨업 · 스킬 해금 · 패시브 수입</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("펫 키우기 🐾", use_container_width=True, key="btn_pet"):
            if st.session_state.get('logged_in_user'):
                st.session_state.page_view = "universe"
                st.session_state.current_category = "🌟 성장 & 혜택"
                st.session_state.current_page = "🐾 펫 키우기"
            else:
                st.session_state['_pending_page'] = "universe"
                st.session_state['_pending_menu_cat'] = "🌟 성장 & 혜택"
                st.session_state['_pending_menu_page'] = "🐾 펫 키우기"
                st.session_state.page_view = "login"
            st.rerun()

    # ── 명예의 전당 ───────────────────────────────────────────
    st.markdown("<div class='game-section-title'>🏛️ 명예의 전당</div>", unsafe_allow_html=True)

    _season_records = market.get("season_records", {})
    if not _season_records:
        st.markdown("""
<div style='background:rgba(255,215,0,0.05);border:1px solid rgba(255,215,0,0.15);border-radius:14px;padding:28px;text-align:center;color:#94A3B8;'>
  🏛️ 아직 종료된 시즌이 없습니다. 첫 시즌이 끝나면 이곳에 기록이 새겨집니다.
</div>""", unsafe_allow_html=True)
    else:
        import html as _html
        _sorted_sns = sorted(_season_records.keys(), key=lambda x: int(x), reverse=True)
        _hof_tabs = st.tabs([f"시즌 {sn}" for sn in _sorted_sns[:8]])
        for _hof_tab, _sn_str in zip(_hof_tabs, _sorted_sns[:8]):
            _rec = _season_records[_sn_str]
            _sn_num = int(_sn_str)
            with _hof_tab:
                _hc1, _hc2 = st.columns(2)

                # 순자산 TOP 3
                with _hc1:
                    st.markdown(f"**🏆 시즌 {_sn_num} 순자산 순위**")
                    _nw_medals = ["🥇","🥈","🥉"]
                    _nw_colors = ["#FFD700","#C0C0C0","#CD7F32"]
                    for _ri in range(1, 4):
                        _entry = _rec.get(f"rank{_ri}")
                        if not _entry: break
                        _euid = _html.escape(str(_entry.get("uid","?") if isinstance(_entry,dict) else _entry))
                        _enw  = _entry.get("net_worth", 0) if isinstance(_entry, dict) else 0
                        _medal = _nw_medals[_ri-1] if _ri <= 3 else f"{_ri}위"
                        _col   = _nw_colors[_ri-1] if _ri <= 3 else "#00E5FF"
                        st.markdown(f"""
<div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:10px;
padding:9px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;'>
  <span style='font-weight:700;'><span style='font-size:1rem;'>{_medal}</span>
  <span style='color:#CBD5E1;margin-left:8px;'>{_euid}</span></span>
  <span style='font-weight:900;color:{_col};'>{format_korean_money(_enw)}</span>
</div>""", unsafe_allow_html=True)

                # 게임 챔피언
                with _hc2:
                    st.markdown(f"**🎮 시즌 {_sn_num} 게임 챔피언**")
                    _gchamps = _rec.get("game_champions", {})
                    if not _gchamps:
                        st.caption("다음 시즌부터 자동 기록됩니다.")
                    else:
                        _game_order = ["racing","zombie","fighter","sniper","invest_marble","terminal","dungeon","academy","zombie_war"]
                        _ordered_g  = [g for g in _game_order if g in _gchamps] + [g for g in _gchamps if g not in _game_order]
                        for _gid in _ordered_g:
                            _champ = _gchamps[_gid]
                            _gmeta = get_game_meta(_gid)
                            _gname = _gmeta.get("name", _gid)
                            _guser = _html.escape(str(_champ.get("top_user","?")))
                            try: _gdisp = _gmeta["fmt"](int(_champ.get("top_score",0)))
                            except: _gdisp = str(_champ.get("top_score","?"))
                            st.markdown(f"""
<div style='background:rgba(255,255,255,0.03);border:1px solid rgba(0,229,255,0.12);border-radius:10px;
padding:9px 14px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center;'>
  <div><div style='font-size:0.75rem;color:#94A3B8;'>{_gname}</div>
  <div style='font-weight:700;color:#CBD5E1;'>🥇 {_guser}</div></div>
  <div style='font-weight:900;color:#00E5FF;font-size:0.9rem;'>{_gdisp}</div>
</div>""", unsafe_allow_html=True)



    # ── 공유하기 섹션 ──────────────────────────────────────────
    st.markdown("<div class='game-section-title'>📢 친구에게 공유하기</div>", unsafe_allow_html=True)

    _share_msg_kakao   = f"🌌 효민 포털에서 같이 부자 되자!\n\n📈 주식·코인·부동산 투자\n🎮 레이싱·좀비·격투 게임 10종\n🏆 시즌 랭킹 경쟁\n\n가입하면 바로 5억 원 지급! 🎁\n👉 {PORTAL_URL}"
    _share_msg_discord = f"**🌌 효민 포털** 같이 하자!\n> 📈 주식·코인·부동산 | 🎮 게임 10종 | 🏆 시즌 랭킹\n> 가입하면 **5억 원 즉시 지급!** 🎁\n🔗 {PORTAL_URL}"

    import streamlit.components.v1 as _components
    import json as _json

    _share_html = f"""
<style>
body {{ margin:0; background:transparent; font-family:'Noto Sans KR',sans-serif; }}
.share-wrap {{
  background: linear-gradient(135deg,rgba(10,16,32,0.95),rgba(15,24,48,0.95));
  border: 1px solid rgba(108,99,255,0.3);
  border-radius: 16px;
  padding: 20px;
}}
.share-desc {{ color:#e8f0ff; font-size:0.88rem; margin-bottom:16px; }}
.share-desc span {{ color:#94A3B8; }}
.btn-row {{ display:flex; flex-wrap:wrap; gap:12px; margin-bottom:18px; }}
.share-btn {{
  border-radius:10px; padding:11px 20px; font-size:0.88rem; font-weight:800;
  cursor:pointer; font-family:inherit; transition:all 0.2s; border:1px solid;
  white-space:nowrap;
}}
.share-btn:hover {{ transform:translateY(-2px); filter:brightness(1.2); }}
.btn-kakao  {{ background:rgba(255,230,0,0.12);  border-color:rgba(255,230,0,0.4);  color:#ffe600; }}
.btn-discord{{ background:rgba(88,101,242,0.15); border-color:rgba(88,101,242,0.45);color:#7289da; }}
.btn-link   {{ background:rgba(0,212,255,0.10);  border-color:rgba(0,212,255,0.35); color:#00d4ff; }}
.preview-box {{
  background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
  border-radius:10px; padding:14px;
}}
.preview-label {{ color:#94A3B8; font-size:0.72rem; font-weight:700; margin-bottom:8px; }}
.preview-text  {{ color:#c8d8f0; font-size:0.82rem; line-height:1.8; white-space:pre-line; }}
</style>
<div class="share-wrap">
  <div class="share-desc">👇 아래 버튼으로 친구에게 바로 공유하세요! <span>(클릭하면 메시지가 복사됩니다)</span></div>
  <div class="btn-row">
    <button class="share-btn btn-kakao" onclick="copyMsg('kakao', this)">💬 카카오톡용 복사</button>
    <button class="share-btn btn-discord" onclick="copyMsg('discord', this)">🎮 디스코드용 복사</button>
    <button class="share-btn btn-link" onclick="copyMsg('link', this)">🔗 링크 복사</button>
  </div>
  <div class="preview-box">
    <div class="preview-label">💬 카카오톡 메시지 미리보기</div>
    <div class="preview-text" id="kakao-preview"></div>
  </div>
</div>
<script>
const msgs = {{
  kakao:   {_json.dumps(_share_msg_kakao)},
  discord: {_json.dumps(_share_msg_discord)},
  link:    {_json.dumps(PORTAL_URL)}
}};
const origLabels = {{
  kakao: '💬 카카오톡용 복사', discord: '🎮 디스코드용 복사', link: '🔗 링크 복사'
}};
document.getElementById('kakao-preview').textContent = msgs.kakao;
function copyMsg(type, btn) {{
  navigator.clipboard.writeText(msgs[type]).then(() => {{
    btn.textContent = '✅ 복사됨!';
    btn.style.background = 'rgba(0,255,136,0.2)';
    btn.style.borderColor = 'rgba(0,255,136,0.5)';
    btn.style.color = '#00ff88';
    setTimeout(() => {{
      btn.textContent = origLabels[type];
      btn.style.background = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }}, 2000);
  }});
}}
</script>
"""
    _components.html(_share_html, height=260, scrolling=False)
    # ── 시스템 공지 & 아키텍처 섹션 ───────────────────────
    with st.expander("📋 시스템 공지 & 전체 아키텍처 구조 보기", expanded=False):

        _sn_now = market.get('season_num', 1)
        _ss_ts = market.get('season_start', 0)
        _ss_str = datetime.fromtimestamp(_ss_ts, KST).strftime('%Y년 %m월 %d일 %H:%M') if _ss_ts else '날짜 정보 없음'
        st.markdown(f"""
<div class="arch-highlight">
    <p>🔧 시스템 대공사 및 재시작 안내</p>
    <p class="sub">
        데이터베이스를 외부 클라우드(MongoDB Atlas)로 완벽 분리하고,
        <b>40개 모듈화 설계</b>를 적용하여 서버 안정성을 극대화했습니다.
        유저 자산은 이제 영구히 안전합니다.
    </p>
</div>
<div class="arch-highlight" style="border-left-color:#00ff88; background: linear-gradient(90deg, rgba(0,255,136,0.08), rgba(0,212,255,0.06));">
    <p style="color:#00ff88 !important;">🚀 시즌 {_sn_now} 진행 중</p>
    <p class="sub">
        <b>[시즌 1 기간]</b> 2026년 4월 15일 ~ 5월 15일 15:35 (종료)<br>
        <b>[시즌 {_sn_now}]</b> {_ss_str} 이후 진행 중 — 기간·혜택은 추후 공지 예정입니다.<br>
        <b>신규 가입 시 초기 정착금 5억 원</b>이 즉시 지급됩니다!<br>
        궁금한 점이나 응원은 아래 <b>유저 소통 창구</b>를 통해 남겨주세요 — 모든 의견을 적극 반영합니다! 💬
    </p>
</div>
<div class="arch-highlight" style="border-left-color:#c04fff; background: linear-gradient(90deg, rgba(192,79,255,0.08), rgba(108,99,255,0.06));">
    <p style="color:#c04fff !important;">🎮 게임 패치노트 (2026.05.13)</p>
    <p class="sub">
        <b>🎯 라인 배틀 저격전</b><br>
        · <b>10라운드 미션 체제</b> - -> 난이도별 모드로 변경 <br>
        · <b>아군 소환 시스템</b> — 자원(💎)으로 보병/돌격대/중화기/의무병/아군저격수 소환 (1~5 단축키)<br>
        · <b>자원 재생 시스템</b> — 시간 경과 및 적 처치 시 자원 획득<br>
        · <b>화면 전체 채우기</b> — 브라우저 전체 크기에 맞춰 동적 렌더링<br>
        · <b>기록 영구 저장 수정</b> — 로그아웃 후 재로그인 시 클리어 기록 완벽 복원<br><br>
        <b>🎲 인베스트 마블 업그레이드</b><br>
        · <b>승리 조건 6가지 추가</b> — 라인독점+전체호텔 / 연속3칸건물 / 기존파산 유지 / 공항4개+호텔 / 단일국가지배 / 순자산₩50,000<br>
        · <b>이동 배너 실시간 표시</b> — 한 칸씩 이동 시 현재 위치와 프로그레스바 표시<br>
        · <b>게임 기록 DB 저장</b> — 승리/순자산 기록이 로그아웃 후에도 영구 보존<br><br>
        <b>🔧 기록 시스템 전면 개선</b><br>
        · 로그인 시 <code>game_records.sniper.clears</code> 필드 자동 복원<br>
        · 클리어한 미션 번호 MongoDB에 영구 저장<br>
        · 마블 승리 기록(순자산·승리횟수·게임수) DB 동기화
    </p>
</div>
        """, unsafe_allow_html=True)

        st.markdown("### 🏗️ SYSTEM ARCHITECTURE & MODULES")
        st.markdown("---")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("""
<div class="arch-card">
    <h4>🗄️ 데이터베이스 — MongoDB Atlas</h4>
    <p>
        모든 유저 자산 및 시장 데이터는 <b>MongoDB Atlas 클라우드</b>에 실시간 저장됩니다.
        로컬 JSON 파일 의존을 완전히 탈피하여, 서버 재시작과 무관하게 데이터가 영구 보존됩니다.
        비밀번호는 <b>bcrypt 단방향 해시</b>로 암호화되어 원문 복원이 불가능합니다. (레거시 SHA-256 → 로그인 시 자동 마이그레이션)
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">MongoDB Atlas</span>
        <span class="arch-badge">bcrypt 암호화</span>
        <span class="arch-badge">실시간 백업</span>
        <span class="arch-badge">utils/database.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🧩 44개 독립 모듈 구조</h4>
    <p>
        전체 시스템은 <b>1개의 진입점(app.py)</b>과 <b>43개의 기능 모듈</b>, 총 44개 파일로 구성됩니다.
        각 기능(주식, 코인, 부동산, 미니게임 등)이 완전히 분리되어 있어,
        한 모듈의 오류가 전체 서비스에 영향을 주지 않습니다.
        유지보수 및 신규 기능 추가가 용이한 구조입니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">app.py (진입점)</span>
        <span class="arch-badge">pages/ (36개 페이지)</span>
        <span class="arch-badge">utils/ (5개 유틸)</span>
        <span class="arch-badge">components/ (1개 컴포넌트)</span>
        <span class="arch-badge">독립 렌더링</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🔐 보안 & 접근 제어</h4>
    <p>
        로그인 5회 실패 시 30초 잠금이 적용되는 <b>Brute-force 방어</b> 시스템을 내장합니다.
        관리자 계정은 별도의 <b>하드코딩 해시</b>로 보호되며, DB에 평문이 저장되지 않습니다.
        VIP 라운지는 순자산 1,000억 이상 또는 관리자만 접근 가능한 권한 제어가 적용됩니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">Brute-force 방어</span>
        <span class="arch-badge">관리자 분리</span>
        <span class="arch-badge">VIP 권한 제어</span>
        <span class="arch-badge">utils/core.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_b:
            st.markdown("""
<div class="arch-card">
    <h4>⏱️ 자동 시장 동기화 — Market Sync</h4>
    <p>
        유저가 접속하지 않는 동안에도 <b>시간 슬롯 기반 자동 계산</b>이 작동합니다.
        주가 변동, 은행 이자, 부동산 임대료가 실시간으로 누적됩니다.
        접속 시 경과 시간만큼의 모든 변화가 한 번에 정확하게 반영됩니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">utils/market_sync.py</span>
        <span class="arch-badge">주가 자동변동</span>
        <span class="arch-badge">이자 자동계산</span>
        <span class="arch-badge">임대료 자동누적</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🌐 멀티 서비스 포털 구조</h4>
    <p>
        <b>HYOMIN PORTAL</b>은 단일 앱 안에서 여러 독립 서비스를 라우팅하는 구조입니다.
        효민 유니버스(경제 시뮬레이션), AI 아카데미(모의고사), 월드 배틀(투표),
        THE TERMINAL(방탈출) 등 각 서비스가 하나의 계정으로 통합 이용 가능합니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">단일 계정 통합</span>
        <span class="arch-badge">뷰 기반 라우팅</span>
        <span class="arch-badge">세션 상태 공유</span>
        <span class="arch-badge">app.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left-color:#ffd700;">
    <h4 style="color:#ffd700 !important;">⏰ 서버 상시 가동 — UptimeRobot Keepalive</h4>
    <p>
        Streamlit Cloud는 일정 시간 접속이 없으면 서버가 슬립 상태로 전환됩니다.
        이를 방지하기 위해 <b>UptimeRobot</b>을 이용해 5분마다 서버에 핑을 보내
        24시간 상시 깨어 있는 상태를 유지합니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge" style="color:#ffd700!important;background:rgba(255,215,0,0.12);border-color:rgba(255,215,0,0.35);">UptimeRobot</span>
        <span class="arch-badge" style="color:#ffd700!important;background:rgba(255,215,0,0.12);border-color:rgba(255,215,0,0.35);">5분 간격 모니터링</span>
        <span class="arch-badge" style="color:#ffd700!important;background:rgba(255,215,0,0.12);border-color:rgba(255,215,0,0.35);">슬립 방지 24/7</span>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>📊 실시간 통계 & 온라인 감지</h4>
    <p>
        접속자 수는 <b>last_seen 타임스탬프</b> 기반으로 5분 이내 활성 유저를 집계합니다.
        일별 방문자, 누적 가입자, 거래량 통계는 MongoDB stats 컬렉션에 별도 저장됩니다.
        포털 메인 화면에서 실시간으로 서버 현황을 확인할 수 있습니다.
    </p>
    <div style="margin-top:10px;">
        <span class="arch-badge">last_seen 감지</span>
        <span class="arch-badge">일별 방문자 집계</span>
        <span class="arch-badge">거래량 추적</span>
        <span class="arch-badge">utils/core.py</span>
    </div>
</div>
            """, unsafe_allow_html=True)

        st.markdown("#### 📦 전체 모듈 목록")
        st.markdown("""
<div class="module-grid">
    <div class="module-item"><strong>app.py</strong>진입점·라우터·로그인·뷰 전환</div>
    <div class="module-item"><strong>components/promo_popup.py</strong>🎉 시즌 홍보 팝업 (광고 모달)</div>
    <div class="module-item"><strong>utils/database.py</strong>MongoDB 연결·CRUD·stats 관리</div>
    <div class="module-item"><strong>utils/core.py</strong>해시·포맷·순자산·세션 동기화</div>
    <div class="module-item"><strong>utils/market_sync.py</strong>주가·코인·이자·임대료 자동동기화</div>
    <div class="module-item"><strong>utils/config.py</strong>종목·부동산·강화 설정 상수</div>
    <div class="module-item"><strong>utils/css.py</strong>유니버스 글로벌 다크 테마 CSS</div>
    <div class="module-item"><strong>pages/home.py</strong>홈 광장·튜토리얼·성장 목표</div>
    <div class="module-item"><strong>pages/stock.py</strong>주식 트레이딩·차트·매수매도</div>
    <div class="module-item"><strong>pages/crypto.py</strong>코인 거래소·실시간 시세</div>
    <div class="module-item"><strong>pages/real_estate.py</strong>부동산 매입·임대료 수익</div>
    <div class="module-item"><strong>pages/bank.py</strong>대출·상환·이자 계산</div>
    <div class="module-item"><strong>pages/txlog.py</strong>개인 거래 내역 조회</div>
    <div class="module-item"><strong>pages/ranking.py</strong>시즌 랭킹·게시판</div>
    <div class="module-item"><strong>pages/clan.py</strong>길드·클랜 시스템</div>
    <div class="module-item"><strong>pages/dm.py</strong>개인 쪽지·읽음 표시</div>
    <div class="module-item"><strong>pages/profile.py</strong>유저 프로필·배지·아바타·게임기록</div>
    <div class="module-item"><strong>pages/pet.py</strong>펫 입양·육성·훈련·악세서리·패시브수입</div>
    <div class="module-item"><strong>pages/quest.py</strong>일일 퀘스트·보상</div>
    <div class="module-item"><strong>pages/title_shop.py</strong>칭호 상점·장착</div>
    <div class="module-item"><strong>pages/vip.py</strong>VIP 전용 라운지</div>
    <div class="module-item"><strong>pages/games/slot.py</strong>럭키 슬롯머신</div>
    <div class="module-item"><strong>pages/games/blackjack.py</strong>블랙잭 카지노</div>
    <div class="module-item"><strong>pages/games/holdem.py</strong>텍사스 홀덤</div>
    <div class="module-item"><strong>pages/games/mine.py</strong>광산 노가다</div>
    <div class="module-item"><strong>pages/games/quiz.py</strong>사주팔자 운세</div>
    <div class="module-item"><strong>pages/games/lotto.py</strong>글로벌 로또</div>
    <div class="module-item"><strong>pages/games/forge.py</strong>전설의 명검 강화</div>
    <div class="module-item"><strong>pages/games/gacha.py</strong>가챠 뽑기</div>
    <div class="module-item"><strong>pages/sports/soccer_sim.py</strong>구단주 시뮬레이터</div>
    <div class="module-item"><strong>pages/sports/penalty.py</strong>조기축구 승부차기</div>
    <div class="module-item"><strong>pages/sports/racing.py</strong>하이퍼카 레이싱</div>
    <div class="module-item"><strong>pages/sports/garage.py</strong>커스텀 튜닝 차고지</div>
    <div class="module-item"><strong>pages/admin/panel.py</strong>창조주 통제소 (관리자 전용)</div>
    <div class="module-item"><strong>pages/project_a.py</strong>AI 무한 모의고사</div>
    <div class="module-item"><strong>pages/project_b.py</strong>월드 배틀</div>
    <div class="module-item"><strong>pages/project_c.py</strong>💻 THE TERMINAL 방탈출</div>
    <div class="module-item"><strong>pages/project_d.py</strong>🎲 인베스트 마블 보드게임</div>
    <div class="module-item"><strong>pages/project_e.py</strong>⚔️ 뱀서라이크 던전 게임</div>
    <div class="module-item"><strong>pages/project_f.py</strong>🏎️ 네온 도주 레이싱</div>
    <div class="module-item"><strong>pages/project_g.py</strong>🧟 좀비 아포칼립스 슈터</div>
    <div class="module-item"><strong>pages/project_h.py</strong>🥊 스트리트 파이터 EX</div>
    <div class="module-item"><strong>pages/project_i.py</strong>🎯 라인 배틀 저격전</div>
    <div class="module-item"><strong>pages/project_j.py</strong>⚽ 얼티밋 사커 11 (11v11 축구매치)</div>
    <div class="module-item"><strong>dep_graph_snippet.py</strong>🕸️ 파일 의존성 그래프 위젯</div>
</div>
        """, unsafe_allow_html=True)

        # ── 파일 의존성 인터랙티브 그래프 ─────────────────────
        st.markdown("#### 🕸️ 파일 의존성 인터랙티브 그래프")
        st.markdown(
            "<p style='color:#8899bb;font-size:0.88rem;margin-top:-6px;'>"
            "파일을 클릭하면 그 파일과 직접 연결된 다른 파일들이 강조됩니다. "
            "어떤 모듈을 고치면 어디까지 영향이 가는지 한눈에 확인할 수 있습니다."
            "</p>",
            unsafe_allow_html=True
        )
        import streamlit.components.v1 as _dg_components
        from dep_graph_snippet import DEP_GRAPH_HTML
        _dg_components.html(DEP_GRAPH_HTML, height=900, scrolling=True)

    # ── 전체 서비스 완전 가이드 ──────────────────────────────
    with st.expander("📖 전체 서비스 완전 가이드 보기", expanded=False):

        st.markdown("### 🗺️ HYOMIN PORTAL — 서비스 소개")
        st.markdown("---")

        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("""
<div class="arch-card">
    <h4>🌌 유니버스 — 자본주의 생존 시뮬레이션</h4>
    <p>
        효민 유니버스는 <b>현실과 동일한 자본주의 경제 시스템</b>을 체험하는 경제 시뮬레이션입니다.
        가입 즉시 <b>초기 정착금 5억 원</b>이 지급되며, 주식·코인·부동산·은행 등
        다양한 금융 수단으로 자산을 불려 나갈 수 있습니다.
        랭킹 시스템, 클랜, 일일 퀘스트, 미니게임, VIP 라운지, 유저 프로필, 펫 키우기까지 갖춘 풀 스케일 경제 세계입니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">📈 주식 트레이딩</span>
        <span class="arch-badge">₿ 코인 거래소</span>
        <span class="arch-badge">🏠 부동산 임대</span>
        <span class="arch-badge">🏦 대출·이자</span>
        <span class="arch-badge">🏆 시즌 랭킹</span>
        <span class="arch-badge">⚔️ 클랜 시스템</span>
        <span class="arch-badge">🎰 미니게임 8종</span>
        <span class="arch-badge">👤 유저 프로필</span>
        <span class="arch-badge">🐾 펫 키우기</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,212,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--cyan) !important;font-weight:700;">💡 입문 가이드</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① 로그인 후 유니버스 입장 → ② 홈 광장에서 튜토리얼 확인 → ③ 주식/코인 소액 매수로 시작
            → ④ 일일 퀘스트 완료로 보너스 획득 → ⑤ 부동산 매입으로 패시브 수익 확보
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🧠 AI 무한 모의고사 — AI 아카데미</h4>
    <p>
        공부한 내용을 붙여넣기하거나 PDF/TXT 파일을 업로드하면,
        <b>Gemini AI</b>가 실제 시험 스타일의 문제를 무한으로 생성해 드립니다.
        문제 수(5~20개), 난이도(쉬움/보통/어려움), 문제 유형(4지선다/단답형/O×)을 자유롭게 설정할 수 있으며,
        채점 후 <b>오답 자동 분석 및 재출제</b> 기능을 제공합니다.
        시험, 수능, 자격증 등 모든 분야에 활용 가능합니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🤖 Gemini 2.5 Flash</span>
        <span class="arch-badge">📄 PDF/TXT 업로드</span>
        <span class="arch-badge">🎚️ 난이도 3단계</span>
        <span class="arch-badge">✏️ 3가지 문제 유형</span>
        <span class="arch-badge">📊 오답 분석</span>
        <span class="arch-badge">🔁 오답 재출제</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 사용법</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① AI 아카데미 입장 → ② 학습 내용 직접 입력 또는 파일 업로드 → ③ 문제 수·난이도·유형 설정
            → ④ 문제 생성 → ⑤ 풀기 → ⑥ 채점 및 오답 확인 → ⑦ 오답만 재출제
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>🎲 인베스트 마블 — 보드게임</h4>
    <p>
        모노폴리에서 영감을 받은 <b>투자형 보드게임</b>입니다.
        AI 봇과 함께 주사위를 굴리며 전 세계 랜드마크 부지를 매입하고,
        <b>집→호텔</b>을 건설해 임대료 수익을 올립니다.
        저당 설정으로 급전을 마련하거나, 무인도에 갇혀 탈출을 시도하는 등
        다이나믹한 경제 전략이 필요한 게임입니다.
        화려한 3D 스타일 UI와 애니메이션이 적용된 풀 HTML 게임입니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🗺️ 세계 랜드마크 보드</span>
        <span class="arch-badge">🤖 AI 봇 대전</span>
        <span class="arch-badge">🏠 집·호텔 건설</span>
        <span class="arch-badge">⛓️ 저당·경매</span>
        <span class="arch-badge">🏝️ 무인도 탈출</span>
        <span class="arch-badge">🎴 이벤트 카드</span>
    </div>
    <div style="margin-top:10px;background:rgba(255,215,0,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--gold) !important;font-weight:700;">💡 전략 팁</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            같은 색 부지 독점 시 임대료 2배. 무인도 탈출은 주사위 더블 or 탈출 카드 사용.
            현금이 부족할 땐 호텔을 팔거나 저당을 설정해 버텨라.
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_g2:
            st.markdown("""
<div class="arch-card">
    <h4>🗳️ 월드 배틀 — 실시간 진영 투표</h4>
    <p>
        매일 새로운 <b>오늘의 질문</b>이 올라오면, A 진영 또는 B 진영 중 하나를 선택해 투표합니다.
        실시간으로 전체 투표 현황과 진영별 비율이 배틀 바를 통해 시각화되며,
        투표 후 다른 시민들의 댓글도 확인할 수 있습니다.
        관리자가 주제·기간·진영 이름을 자유롭게 설정하고, 종료된 투표는 히스토리로 보존됩니다.
        완전 익명으로 진행되며 계정당 1표만 허용됩니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🔵🔴 2진영 배틀</span>
        <span class="arch-badge">📊 실시간 비율 바</span>
        <span class="arch-badge">💬 투표 후 댓글</span>
        <span class="arch-badge">🕵️ 완전 익명</span>
        <span class="arch-badge">⏱️ 마감 카운트다운</span>
        <span class="arch-badge">📜 히스토리 보존</span>
    </div>
    <div style="margin-top:10px;background:rgba(108,99,255,0.1);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--accent) !important;font-weight:700;">💡 참여 방법</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① 로그인 후 월드 배틀 입장 → ② 오늘의 질문 확인 → ③ 원하는 진영 버튼 클릭
            → ④ 투표 완료 후 비율 확인 → ⑤ 댓글로 의견 남기기 (마감 후 결과 공개)
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card">
    <h4>💻 THE TERMINAL — 방탈출</h4>
    <p>
        오직 <b>커맨드라인 명령어</b>만으로 단서를 추적해 방을 탈출하는 해킹 어드벤처 게임입니다.
        총 <b>20개의 스테이지</b>로 구성되며, 각 스테이지마다 독립된 가상 파일시스템이 펼쳐집니다.
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cat</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cd</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">decode</code>,
        <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">rot13</code> 등
        실제 터미널 명령어와 유사한 커맨드를 입력해 숨겨진 비밀번호를 찾아야 합니다.
        단계별 3개의 힌트가 제공되며, 모든 스테이지를 클리어하면 <b>타임어택 모드</b>가 해금됩니다.
        스테이지 클리어 시 보상금이 지급되고 전체 클리어 시 특별 칭호가 부여됩니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge">🖥️ 20 STAGES</span>
        <span class="arch-badge">📁 가상 파일시스템</span>
        <span class="arch-badge">⌨️ 실제 CLI 명령어</span>
        <span class="arch-badge">🔐 SHA-256 정답 검증</span>
        <span class="arch-badge">💡 단계별 3힌트</span>
        <span class="arch-badge">⏱️ 타임어택 모드</span>
        <span class="arch-badge">💰 클리어 보상금</span>
        <span class="arch-badge">⭐~⭐⭐⭐⭐⭐ 난이도</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 기본 명령어</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls</code> 파일 목록 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">ls -a</code> 숨김파일 포함 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cat [파일]</code> 내용 보기 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">cd [경로]</code> 디렉토리 이동 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">decode [문자열]</code> base64 해독 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">unlock [정답]</code> 잠금 해제
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left: 3px solid #c04fff;">
    <h4 style="color:#c04fff !important;">⚔️ 던전 런 2.5D — SURVIVORS REBORN</h4>
    <p>
        사방에서 끝없이 몰려오는 몬스터들을 쓸어버리는 <b>본격 뱀서라이크(서바이벌)</b> 게임입니다.
        화려한 <b>2.5D 입체 그래픽</b>과 함께 적의 웨이브를 돌파하고 보스를 격파하세요.
        <b style="color:#ff3366;">레벨업 시 등장하는 무기와 패시브를 조합해 극한의 시너지를 완성하세요!</b><br>
        <b>전사·마법사·궁수·닌자</b> 4개의 고유 클래스, 몰입감 넘치는 타격감, 그리고 강력한 웨이브 보스들이 기다립니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🌪️ 뱀서라이크 서바이벌</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🧊 2.5D 입체 그래픽</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">⚔️ 자동 공격 & 핵앤슬래시</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">🃏 무기/스킬 조합</span>
        <span class="arch-badge" style="background:rgba(192,78,255,0.2);color:#c04fff !important;border-color:rgba(192,78,255,0.4);">👹 웨이브 보스전</span>
    </div>
    <div style="margin-top:10px;background:rgba(192,78,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#c04fff !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">W A S D</code> 또는
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">↑↓←→</code> 상하좌우 이동 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">자동</code> 기본 공격 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">Q E R</code> 액티브 스킬 사용 &nbsp;
            <code style="background:rgba(192,78,255,0.2);padding:1px 5px;border-radius:3px;">마우스</code> 캐릭터 및 능력 선택
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        # ── 신규 게임 4종 가이드 ────────────────────────────────
        st.markdown("### 🎮 신규 게임 4종 가이드")
        st.markdown("---")

        col_ng1, col_ng2 = st.columns(2)

        with col_ng1:
            st.markdown("""
<div class="arch-card" style="border-left-color:#00d4ff;">
    <h4 style="color:#00d4ff !important;">🏎️ 네온 도주 레이싱 &#8212; NEON RUNAWAY</h4>
    <p>
        5레인 무한 도로를 달리며 경찰 추격을 뿌리치는 하이스피드 레이싱 게임입니다.
        레인을 빠르게 전환하며 장애물을 피하고, 니트로 부스터로 화려한 스피드를 폭발시키세요.
        연속 회피로 콤보가 상승하며, 최대 ×8 콤보로 점수를 높여보세요.
        경찰 수는 파도비로 늘수록 더 터프해집니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">🛣️ 5레인 무한 도로</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">⚡ 니트로 부스터</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">🚨 경찰 추격 웨이브</span>
        <span class="arch-badge" style="color:#00d4ff !important;background:rgba(0,212,255,0.12);border-color:rgba(0,212,255,0.35);">×8 콤보 시스템</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,212,255,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--cyan) !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            PC: <code style="background:rgba(0,212,255,0.15);padding:1px 5px;border-radius:3px;">←→ 방향키</code> 레인 전환 &nbsp;
            <code style="background:rgba(0,212,255,0.15);padding:1px 5px;border-radius:3px;">Space</code> 니트로 &nbsp;|&nbsp;
            모바일: D-PAD + NITRO 버튼 지원
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left-color:#ff2244;">
    <h4 style="color:#ff2244 !important;">🧟 좀비 아포칼립스 &#8212; ZOMBIE APOCALYPSE</h4>
    <p>
        탑다운 시점의 시가지 맵에서 철연같이 몰려드는 좀비를 생존하는 싸일법 슈터입니다.
        새로운 웨이브마다 상점에서 코인으로 <b>무기 업그레이드</b>와 <b>탄약 보충</b>을 하며,
        권총·라이플·샷건·섬광백열 4종 무기를 스위칭할 수 있습니다.
        보스 좀비가 등장하는 매 5라운드를 버티세요.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🎯 탑다운 슈터</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🔫 4종 무기 시스템</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🛒 라운드간 상점</span>
        <span class="arch-badge" style="color:#ff2244 !important;background:rgba(255,34,68,0.12);border-color:rgba(255,34,68,0.35);">🧟‍♂️ 보스 좀비</span>
    </div>
    <div style="margin-top:10px;background:rgba(255,34,68,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#ff2244 !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            PC: <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">WASD</code> 이동 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">마우스</code> 조준·사격 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">R</code> 재장전 &nbsp;
            <code style="background:rgba(255,34,68,0.15);padding:1px 5px;border-radius:3px;">1-4</code> 무기 교체 &nbsp;|&nbsp; 모바일: 조이스틱 + 발사 버튼
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_ng2:
            st.markdown("""
<div class="arch-card" style="border-left-color:#c04fff;">
    <h4 style="color:#c04fff !important;">🥊 스트리트 파이터 EX &#8212; STREET FIGHTER EX</h4>
    <p>
        <b>6가지 고유 캐릭터</b>(전사/파이터/닌자/모헨/닉느/고스트) 중 하나를 선택해 AI CPU와 1v1 대결하는 게임입니다.
        각 캐릭터마다 고유한 필살기와 <b>슈퍼 게이지</b>가 있으며,
        3라운드 선승일경식으로 진행됩니다.
        콤보 파출로 슈퍼게이지를 치는 초리한 파이널 필살기를 시전하세요!
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🎮 6캐릭터 대전</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">⚡ 슈퍼 게이지</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🔥 필살기 파이니슬</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🏆 3라운드 선승</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">👥 2P 대전 모드</span>
        <span class="arch-badge" style="color:#c04fff !important;background:rgba(192,79,255,0.12);border-color:rgba(192,79,255,0.35);">🗺️ 8스테이지 아케이드</span>
    </div>
    <div style="margin-top:10px;background:rgba(192,79,255,0.08);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:#c04fff !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            🎮 <b>P1:</b> <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">A D</code> 이동 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">W</code> 점프 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">S</code> 가드 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">Z</code> 펀치 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">X</code> 킥 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">C</code> 강공격 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">V</code> 필살기 &nbsp;
            <code style="background:rgba(192,79,255,0.2);padding:1px 5px;border-radius:3px;">F</code> 슈퍼기술<br>
            🕹️ <b>P2:</b> <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">← →</code> 이동 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">↑</code> 점프 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">↓</code> 가드 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">1</code> 펀치 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">2</code> 킥 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">3</code> 강공격 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">4</code> 필살기 &nbsp;
            <code style="background:rgba(255,34,68,0.2);padding:1px 5px;border-radius:3px;">5</code> 슈퍼기술 &nbsp;|&nbsp; 모바일: D-PAD + 공격버튼
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

            st.markdown("""
<div class="arch-card" style="border-left-color:#00ff88;">
    <h4 style="color:#00ff88 !important;">🎯 라인 배틀 저격전 &#8212; FRONTLINE BREACH</h4>
    <p>
        전장의 저격수가 되어 <b>다양한 난이도 모드</b>를 돌파하는 본격 전선 돌파 시뮬레이션입니다.
        적을 처치하거나 시간이 지나면 <b>자원(💎)</b>이 쌓이고,
        이를 사용해 <b>보병·돌격대·중화기·의무병·아군저격수</b>를 소환해 전선을 밀어붙이세요.
        기관총병·장교·총사령관 같은 핵심 목표를 먼저 제거하면 전선이 크게 전진합니다.
        <b>클리어 기록은 MongoDB에 영구 저장</b>되어 로그아웃 후에도 진행상황이 유지됩니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🎮 난이도 모드</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🪖 아군 소환 시스템</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">💎 자원 관리</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🔭 스코프 저격</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">💀 헤드샷 시스템</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">💾 기록 영구 저장</span>
        <span class="arch-badge" style="color:#00ff88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">S~C 등급 평가</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 컨트롤</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">클릭/Space</code> 발사 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">우클릭/Z</code> 스코프 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">Shift</code> 숨참기 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">R</code> 재장전 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">C</code> 엄폐 &nbsp;
            <code style="background:rgba(0,255,136,0.15);padding:1px 5px;border-radius:3px;">1~5</code> 병력 소환
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)


        # ── 유저 성장 서비스 가이드 ────────────────────────────
        st.markdown("### 🌱 유저 성장 서비스 가이드")
        st.markdown("---")

        col_pg1, col_pg2 = st.columns(2)

        with col_pg1:
            st.markdown("""
<div class="arch-card" style="border-left-color:#00E5FF;">
    <h4 style="color:#00E5FF !important;">👤 내 프로필 &#8212; 나만의 캐릭터 카드</h4>
    <p>
        효민 유니버스에서의 모든 활동이 하나의 <b>게임 캐릭터 프로필</b>로 집약됩니다.
        순자산에 따라 <b>Lv.1 튜토리얼 중</b>부터 <b>Lv.100 우주신</b>까지 성장하며,
        달성한 목표에 따라 <b>배지 12종</b>이 자동으로 수여됩니다.
        아바타는 20종 중 선택 가능하며, 잠긴 아바타는 <b>30억</b>에 해금할 수 있습니다.
        상태 메시지를 설정해 다른 유저들에게 현재 상태를 알릴 수도 있습니다.
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">🧑‍🚀 아바타 20종</span>
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">🏅 배지 12종</span>
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">⚡ Lv.1~100 성장</span>
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">📊 자산 현황 요약</span>
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">🎮 게임 기록 6종</span>
        <span class="arch-badge" style="color:#00E5FF !important;background:rgba(0,229,255,0.1);border-color:rgba(0,229,255,0.3);">💬 상태 메시지</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,229,255,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--cyan) !important;font-weight:700;">💡 활용 팁</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            ① 유니버스 입장 → ② 🌟 성장 & 혜택 → 👤 내 프로필 → ③ 아바타 선택
            → ④ 상태 메시지 설정 → ⑤ 배지 달성 현황 확인 → ⑥ 게임 기록 조회
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

        with col_pg2:
            st.markdown("""
<div class="arch-card" style="border-left-color:#00FF88;">
    <h4 style="color:#00FF88 !important;">🐾 펫 키우기 &#8212; 나만의 동반자</h4>
    <p>
        <b>8종의 펫</b>을 입양해 함께 성장시키는 육성 시스템입니다.
        먹이주기·훈련·놀아주기로 EXP를 쌓아 레벨업하며,
        <b>레벨 20</b> 달성 시 시간당 <b>패시브 수입</b>이 발생합니다.
        악세서리 5종으로 능력치를 강화하고, 레벨별 <b>스킬 8종</b>을 해금하세요.
        레벨 40을 달성하면 외형이 <b>전설 폼</b>으로 각성합니다!
    </p>
    <div style="margin-top:12px;">
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🐉 8종 펫 (전설~일반)</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🍖 먹이 4종</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🎮 훈련 미니게임 4종</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">👗 악세서리 5종</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">⚔️ 스킬 8종</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">💰 패시브 수입 (Lv.20+)</span>
        <span class="arch-badge" style="color:#00FF88 !important;background:rgba(0,255,136,0.1);border-color:rgba(0,255,136,0.3);">🌟 전설 각성 (Lv.40)</span>
    </div>
    <div style="margin-top:10px;background:rgba(0,255,136,0.07);border-radius:8px;padding:10px 12px;">
        <p style="margin:0;font-size:0.85rem;color:var(--green) !important;font-weight:700;">💡 육성 팁</p>
        <p style="margin:4px 0 0 0;font-size:0.82rem;color:var(--text2) !important;">
            드래곤(500억) → 최고 패시브 수입 | 럭키 고양이(1000만) → 입문용 추천.
            방치하면 배고픔·행복도 하락 → HP 감소. 악세서리 "왕관 모자" 장착 시 EXP +10%.
            Lv.20 넘으면 접속할 때마다 자동으로 수입 수령!
        </p>
    </div>
</div>
            """, unsafe_allow_html=True)

    # ── 유저 소통 창구 ──────────────────────────────────────────
    _FEEDBACK_FILE = "portal_feedback"
    _TYPE_META = {
        "🐛 에러 신고":  ("#ff3366", "rgba(255,51,102,0.12)", "rgba(255,51,102,0.35)"),
        "💡 기능 요청":  ("#00d4ff", "rgba(0,212,255,0.10)",  "rgba(0,212,255,0.30)"),
        "📣 응원":       ("#ffd700", "rgba(255,215,0,0.10)",  "rgba(255,215,0,0.30)"),
        "⭐ 포털 리뷰":  ("#c04fff", "rgba(192,79,255,0.10)", "rgba(192,79,255,0.30)"),
    }
    _is_admin_portal = st.session_state.get('logged_in_user') == 'admin'

    st.markdown("<div class='feedback-section-title'>💬 유저 소통 창구</div>", unsafe_allow_html=True)
    _fb_col1, _fb_col2 = st.columns([1, 1], gap="large")

    # ── 왼쪽: 글 쓰기 폼 ──
    with _fb_col1:
        st.markdown("""
<div class='feedback-form-wrap'>
  <h4>📝 의견·에러·응원 남기기</h4>
</div>
""", unsafe_allow_html=True)
        _fb_type = st.selectbox(
            "유형",
            list(_TYPE_META.keys()),
            key="fb_type_sel",
            label_visibility="collapsed",
        )
        _fb_text = st.text_area(
            "내용",
            placeholder="버그, 건의사항, 응원 메시지를 자유롭게 남겨주세요 (최대 200자)",
            max_chars=200,
            height=110,
            key="fb_text_input",
            label_visibility="collapsed",
        )
        if st.button("📨 제출하기", use_container_width=True, key="fb_submit_btn"):
            _cur_uid = st.session_state.get('logged_in_user', '')
            if not _cur_uid:
                st.warning("⚠️ 로그인 후 이용 가능합니다.")
            elif not _fb_text.strip():
                st.error("내용을 입력해주세요.")
            else:
                import html as _html_fb
                _fb_list = load_db(_FEEDBACK_FILE, [])
                if not isinstance(_fb_list, list): _fb_list = []
                _today_str = datetime.now(KST).strftime("%Y-%m-%d")
                _today_cnt = sum(1 for _f in _fb_list
                                 if _f.get('uid') == _cur_uid
                                 and _f.get('date', '').startswith(_today_str))
                if _today_cnt >= 3:
                    st.error("하루 최대 3건까지 제출 가능합니다.")
                else:
                    _new_fb = {
                        "id":            f"{datetime.now(KST).strftime('%Y%m%d%H%M%S')}_{_cur_uid}",
                        "uid":           _cur_uid,
                        "type":          _fb_type,
                        "text":          _html_fb.escape(_fb_text.strip()),
                        "date":          datetime.now(KST).strftime("%Y-%m-%d %H:%M"),
                        "admin_checked": False,
                    }
                    _fb_list.insert(0, _new_fb)
                    _fb_list = _fb_list[:300]
                    save_db(_FEEDBACK_FILE, _fb_list)
                    st.success("✅ 의견이 등록되었습니다! 감사합니다 😊")
                    st.rerun()
        st.markdown("""
<div style='color:var(--text2);font-size:0.75rem;margin-top:10px;line-height:1.6;'>
  · 하루 최대 3건 제출 가능<br>
  · 관리자가 읽으면 <b style="color:#00ff88;">✅ 확인됨</b> 표시가 붙습니다<br>
  · 에러 신고 시 어떤 화면에서 발생했는지 함께 적어주시면 빠른 수정에 도움됩니다
</div>
""", unsafe_allow_html=True)

    # ── 오른쪽: 의견 목록 ──
    with _fb_col2:
        _fb_list_view = load_db(_FEEDBACK_FILE, [])
        if not isinstance(_fb_list_view, list): _fb_list_view = []
        _uncheck_cnt = sum(1 for _f in _fb_list_view if not _f.get('admin_checked', False))

        _header_extra = ""
        if _is_admin_portal and _uncheck_cnt > 0:
            _header_extra = f" <span style='background:rgba(255,51,102,0.2);color:#ff3366;border:1px solid rgba(255,51,102,0.4);border-radius:999px;font-size:0.7rem;padding:2px 8px;font-weight:800;'>{_uncheck_cnt} 미확인</span>"
        st.markdown(f"<div style='color:var(--cyan);font-weight:700;font-size:0.95rem;margin-bottom:12px;'>📋 최근 의견{_header_extra}</div>", unsafe_allow_html=True)

        if not _fb_list_view:
            st.markdown("<div style='color:var(--text2);font-size:0.85rem;text-align:center;padding:30px 0;'>아직 등록된 의견이 없습니다.<br>첫 번째 의견을 남겨보세요! 🙌</div>", unsafe_allow_html=True)
        else:
            import html as _html_fb2
            _display_limit = 15 if _is_admin_portal else 10
            for _fi, _fb in enumerate(_fb_list_view[:_display_limit]):
                _tc, _bc, _bdr = _TYPE_META.get(_fb.get('type', ''), ("#8899bb", "rgba(136,153,187,0.08)", "rgba(136,153,187,0.2)"))
                _checked = _fb.get('admin_checked', False)
                _badge_html = (
                    "<span class='feedback-checked-badge'>✅ 확인됨</span>"
                    if _checked else
                    "<span class='feedback-unchecked-badge'>⬜ 미확인</span>"
                )
                _safe_uid  = _html_fb2.escape(str(_fb.get('uid', '')))
                _safe_text = _html_fb2.escape(str(_fb.get('text', '')))
                _safe_type = _html_fb2.escape(str(_fb.get('type', '')))
                _safe_date = _html_fb2.escape(str(_fb.get('date', '')))

                st.markdown(f"""
<div class='feedback-item' style='background:{_bc};border:1px solid {_bdr};'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;'>
    <span style='color:{_tc};font-size:0.74rem;font-weight:800;'>{_safe_type}</span>
    {_badge_html}
  </div>
  <div style='color:var(--text);font-size:0.86rem;line-height:1.5;margin-bottom:6px;word-break:break-all;'>{_safe_text}</div>
  <div style='color:var(--text2);font-size:0.71rem;'>👤 {_safe_uid} · 🕐 {_safe_date}</div>
</div>
""", unsafe_allow_html=True)

                # 관리자 전용 확인 처리 버튼
                if _is_admin_portal:
                    _btn_lbl = "☑️ 확인 취소" if _checked else "✅ 확인 처리"
                    _btn_style = "color:#94A3B8;" if _checked else "color:#00ff88;"
                    if st.button(_btn_lbl, key=f"fb_ck_{_fb.get('id', _fi)}", use_container_width=True):
                        _fb_edit = load_db(_FEEDBACK_FILE, [])
                        if not isinstance(_fb_edit, list): _fb_edit = []
                        for _item in _fb_edit:
                            if _item.get('id') == _fb.get('id'):
                                _item['admin_checked'] = not _item.get('admin_checked', False)
                                break
                        save_db(_FEEDBACK_FILE, _fb_edit)
                        st.rerun()

            if len(_fb_list_view) > _display_limit:
                st.markdown(f"<div style='color:var(--text2);font-size:0.75rem;text-align:center;margin-top:4px;'>+ {len(_fb_list_view)-_display_limit}건 더 있음 (관리자 패널에서 전체 조회 가능)</div>", unsafe_allow_html=True)

    # ── 푸터 ──
    st.markdown("""
    <div class='portal-footer'>
      <p>ⓒ 2026 HYOMIN PORTAL INC. · Powered by AI & Vibe Coding</p>
      <p style='margin-top:6px;font-size:0.7rem;'>Built with Claude · MongoDB Atlas · Streamlit · Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ==============================
# 4. [View 2] 로그인 / 회원가입
# ==============================
elif st.session_state.page_view == "login":
    st.markdown(PORTAL_CSS, unsafe_allow_html=True)
    st.markdown("<div class='portal-bg'></div>", unsafe_allow_html=True)

    if st.button("🔙 포털 메인으로"):
        st.session_state.page_view = "portal"; st.rerun()

    _page_names = {
        "universe": "효민 유니버스", "project_a": "AI 아카데미", "project_b": "월드 배틀",
        "project_c": "더 터미널", "project_d": "인베스트 마블", "project_e": "던전 런",
        "project_f": "네온 도주 레이싱", "project_g": "좀비 아포칼립스",
        "project_h": "스트리트 파이터 EX", "project_i": "라인 배틀 저격전",
        "universe_profile": "내 프로필", "universe_pet": "펫 키우기",
    }
    _pending_name = _page_names.get(st.session_state.get('_pending_page', ''), '')
    _subtitle = f"로그인 후 <b>{_pending_name}</b>(으)로 이동합니다." if _pending_name else "안전한 서비스 이용을 위해 로그인해주세요."
    st.markdown(f"""
    <div style='text-align:center;padding:40px 0 20px;'>
      <div style='font-family:"Orbitron",sans-serif;font-size:1.8rem;font-weight:900;
        background:linear-gradient(135deg,#6c63ff,#00d4ff);-webkit-background-clip:text;
        -webkit-text-fill-color:transparent;letter-spacing:3px;'>HYOMIN ID</div>
      <p style='color:#94A3B8;margin-top:8px;'>{_subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        # JS 기반 자동 모바일/PC 감지
        if 'auto_device_detected' not in st.session_state:
            st.components.v1.html("""
<script>
function detectDevice() {
    var isMobile = window.innerWidth <= 768 || /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent);
    var msg = isMobile ? 'mobile' : 'pc';
    // Streamlit에 메시지 전달 (query param 방식)
    if (isMobile && !window.location.search.includes('_dev=mobile')) {
        var url = new URL(window.location.href);
        url.searchParams.set('_dev', 'mobile');
        window.location.replace(url.toString());
    }
}
detectDevice();
</script>
""", height=0)
        _qdev = st.query_params.get('_dev', '')
        if _qdev == 'mobile':
            _default_device = "📱 모바일 (스마트폰)"
        else:
            _default_device = "🖥️ PC (데스크탑)"
        device_mode = st.radio("접속 환경", ["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"],
                               index=["🖥️ PC (데스크탑)", "📱 모바일 (스마트폰)"].index(_default_device),
                               horizontal=True)
        tabs = st.tabs(["🔑 로그인", "📝 회원가입"])

        with tabs[0]:
            _login_sn = load_db(MARKET_FILE, {}).get('season_num', 1)
            st.markdown(f"""
<div style='background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.45);border-radius:10px;padding:14px;margin-bottom:16px;'>
  <div style='color:#00ff88;font-weight:900;font-size:1rem;'>🚀 시즌 {_login_sn} 진행 중!</div>
  <div style='color:#E2E8F0;font-size:0.9rem;margin-top:6px;'>
    시즌 {_login_sn}이 시작되었습니다! 새로운 경쟁에서 최고 자리를 차지하세요 🏆<br>
    <b>신규 가입 시 초기 정착금 5억 원</b>이 즉시 지급됩니다!<br>
    의견·응원은 포털 메인의 <b>유저 소통 창구</b>에 남겨주세요 💬
  </div>
</div>
""", unsafe_allow_html=True)
            l_id = st.text_input("아이디", placeholder="아이디를 입력하세요")
            l_pw = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")

            if st.button("🚀 로그인 및 계속하기", use_container_width=True):
                users = load_db(USERS_FILE, {})

                # ── DB 기반 로그인 잠금 확인 ──────────────────────────────
                if l_id and l_id in users:
                    _fails, _lock_until = get_login_lock(l_id)
                else:
                    # 없는 아이디는 세션으로만 임시 추적 (brute-force 방어)
                    _fails      = st.session_state.get('_anon_fails', 0)
                    _lock_until = st.session_state.get('_anon_lock', 0)

                if time.time() < _lock_until:
                    _remain = int(_lock_until - time.time())
                    st.error(f"🔒 로그인 시도 초과. {_remain}초 후 다시 시도하세요.")
                    st.stop()

                # ── 관리자 로그인 (SHA-256 유지) ─────────────────────────
                if l_id == "admin" and hash_pw(l_pw) == ADMIN_HASH:
                    if "admin" not in users:
                        users["admin"] = {"pw": ADMIN_HASH, "cash": 999_999_999_999,
                                          "inventory": [], "equipped_title": "👑 절대신 창조주"}
                        save_db(USERS_FILE, users)
                    _do_login("admin", users, device_mode)

                # ── 일반 유저 로그인 (bcrypt + 레거시 SHA-256 자동 마이그레이션) ──
                elif l_id != "admin" and l_id in users and verify_pw(l_pw, users[l_id]['pw']):
                    # 레거시 SHA-256 해시 감지 → 로그인 시점에 bcrypt로 자동 교체
                    if is_legacy_hash(users[l_id]['pw']):
                        users[l_id]['pw'] = hash_pw_bcrypt(l_pw)
                        save_db(USERS_FILE, users)
                    clear_login_lock(l_id)
                    _do_login(l_id, users, device_mode)

                # ── 로그인 실패 ───────────────────────────────────────────
                else:
                    _fails += 1
                    if l_id and l_id in users:
                        _lock_until_new = (time.time() + 30) if _fails >= 5 else 0.0
                        set_login_lock(l_id, _fails, _lock_until_new)
                    else:
                        st.session_state['_anon_fails'] = _fails
                        if _fails >= 5:
                            st.session_state['_anon_lock'] = time.time() + 30

                    if _fails >= 5:
                        st.error("🔒 로그인 5회 실패. 30초 후 다시 시도하세요.")
                    else:
                        st.error(f"❌ 아이디 또는 비밀번호가 올바르지 않습니다. (남은 시도: {5 - _fails}회)")
                        st.info("💡 혹시 비밀번호가 기억나지 않으시나요? 5월 1일 이후 서버 점검으로 비밀번호가 **1234**로 초기화된 적이 있습니다. 비밀번호가 1234인지 확인해보세요.")

        with tabs[1]:
            n_id = st.text_input("새 아이디", placeholder="사용할 아이디")
            n_pw = st.text_input("새 비밀번호", type="password", placeholder="비밀번호 설정")
            if st.button("✨ 계정 생성하기", use_container_width=True):
                users    = load_db(USERS_FILE, {})
                clean_id = n_id.strip()
                if not re.match(r'^[a-zA-Z0-9가-힣_]{2,20}$', clean_id):
                    st.error("⚠️ 아이디는 한글/영문/숫자/언더바(_)만 사용 가능하며 2~20자여야 합니다.")
                elif clean_id in users or clean_id == "admin":
                    st.error("⚠️ 이미 존재하는 아이디입니다.")
                elif len(n_pw) < 1:
                    st.error("⚠️ 비밀번호를 입력해주세요.")
                else:
                    users[clean_id] = {
                        "pw": hash_pw_bcrypt(n_pw), "cash": 500_000_000, "inventory": [],
                        "equipped_title": "🌱 신규시민", "portfolio": {}, "real_estate": {},
                        "rent_time": time.time(), "loan": 0, "loan_time": time.time(),
                        "last_estate_reset": 0, "bulk_trade_date": "", "bulk_trade_count": 0,
                        "crypto_portfolio": {}, "daily_quests": {}, "weapon_level": 0,
                        "garage": {'cars': {}, 'active_tier': None},
                    }
                    save_db(USERS_FILE, users)
                    stats = load_stats()
                    stats["total_signups"] = stats.get("total_signups", 0) + 1
                    save_stats(stats)
                    st.success("🎉 가입 성공! 로그인 탭에서 로그인해주세요.")
    st.stop()


# ==============================
# 5. [View 3] 효민 유니버스
# ==============================
elif st.session_state.page_view == "universe":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    market = run_market_sync()
    if market.get("maintenance_mode") and st.session_state.logged_in_user != "admin":
        st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
        st.warning(f"🔧 {market.get('maintenance_msg', '현재 서버 점검 중입니다.')}")
        if st.button("🏠 포털 메인으로"):
            st.session_state.page_view = "portal"; st.rerun()
        st.stop()
    st.markdown(f"<style>{GLOBAL_CSS}</style>", unsafe_allow_html=True)
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()

    def _calc_nw_from_session(market_data):
        w = st.session_state.global_cash - st.session_state.loan
        prices = {k: v['price'] for k, v in market_data.get('stock_data', {}).items()}
        for sid, p_data in st.session_state.portfolio.items():
            if sid in prices: w += p_data.get('qty', 0) * prices[sid]
        for cid, cinfo in st.session_state.get('crypto_portfolio', {}).items():
            w += cinfo.get('qty', 0) * market_data.get('crypto_data', {}).get(cid, {}).get('price', 0)
        for eid, count in st.session_state.get('real_estate', {}).items():
            if eid in estate_config: w += estate_config[eid]['base_price'] * count * 0.8
        w_lv = st.session_state.get('weapon_level', 0)
        if w_lv > 0 and w_lv in FORGE_DATA: w += FORGE_DATA[w_lv]['sell']
        return w

    nw = _calc_nw_from_session(market)
    if st.session_state.loan > 0 and nw < 0:
        # 이전 칭호 저장 (신용불량자가 아닐 때만 저장)
        cur_title = st.session_state.equipped_title
        if cur_title != "💸 신용불량자":
            st.session_state['_pre_debt_title'] = cur_title
        st.session_state.equipped_title = "💸 신용불량자"
        sync_user_data()

    if "current_page" not in st.session_state:
        st.session_state.current_page = "🏠 홈 광장 (튜토리얼)"

    is_admin = st.session_state.logged_in_user == "admin"
    is_vip   = nw >= 100_000_000_000 or is_admin

    CATEGORY_MENUS = {
        "📈 경제":        ["🏠 홈 광장 (튜토리얼)", "📈 주식 트레이딩", "🪙 코인 거래소", "🏢 부동산 거래소", "🏦 은행 (대출/상환)", "📜 내 거래 기록"],
        "🎮 미니게임":    ["🎰 럭키 슬롯", "🃏 블랙잭 카지노", "⛏️ 광산 (노가다)", "🃏 텍사스 홀덤", "💻 사주팔자", "⚔️ 글로벌 로또", "🗡️ 전설의 명검 강화", "🎴 가챠 뽑기"],
        "🌟 성장 & 혜택": ["👤 내 프로필", "🐾 펫 키우기", "📅 일일 퀘스트", "👑 칭호 상점"],
        "⚽ 스포츠":      ["⚽ 구단주 시뮬레이터", "⚽ 조기축구 승부차기", "🏎️ 하이퍼카 레이싱", "🛠️ 커스텀 튜닝 차고지"],
        "👥 커뮤니티":    ["🏰 길드/클랜", "🏅 랭킹 & 게시판", "✉️ 개인 쪽지함"],
    }
    if is_vip:   CATEGORY_MENUS["📈 경제"].insert(1, "💎 VIP 라운지")
    if is_admin: CATEGORY_MENUS["⚙️ 관리"] = ["🛠️ 창조주 통제소"]

    def get_current_category():
        for cat, pages in CATEGORY_MENUS.items():
            if st.session_state.current_page in pages: return cat
        return list(CATEGORY_MENUS.keys())[0]

    if "current_category" not in st.session_state:
        st.session_state.current_category = get_current_category()

    msg_db_check = load_db(MESSAGES_FILE, {})
    my_unread  = sum(1 for m in msg_db_check.get(st.session_state.logged_in_user, {}).get("inbox", []) if not m.get("read", False))
    unread_txt = f" 🔴{my_unread}" if my_unread > 0 else ""
    is_pc_mode = "PC" in st.session_state.get('device_mode', '🖥️ PC (데스크탑)')

    # PC모드일 때 첫 로그인 시 사이드바 자동 열기
    if is_pc_mode and not st.session_state.get('_sidebar_opened'):
        st.session_state['_sidebar_opened'] = True
        st.markdown("""<script>
        setTimeout(function(){
            var btn = window.parent.document.querySelector('[data-testid="collapsedControl"]');
            if(btn) btn.click();
        }, 300);
        </script>""", unsafe_allow_html=True)

    if is_pc_mode:
        with st.sidebar:
            st.markdown(f"<div style='padding:14px;background:rgba(255,255,255,0.05);border:1px solid #00E5FF;border-radius:10px;margin-bottom:14px;'><div style='color:#00E5FF;font-size:0.8rem;'>{st.session_state.equipped_title}</div><div style='font-size:1rem;font-weight:700;'>{st.session_state.logged_in_user}{unread_txt}</div></div>", unsafe_allow_html=True)
            st.metric("💵 현금",  format_korean_money(st.session_state.global_cash))
            st.metric("📊 순자산", format_korean_money(nw))
            st.write("---")
            for cat in CATEGORY_MENUS:
                if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                    st.session_state.current_category = cat
                    st.session_state.current_page = CATEGORY_MENUS[cat][0]; st.rerun()
            st.write("---")
            cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
            cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
            selected_menu = st.radio(f"{st.session_state.current_category} 메뉴", cur_cat_pages, index=cur_idx)
            if selected_menu != st.session_state.current_page:
                st.session_state.current_page = selected_menu; st.rerun()
            st.write("---")
            if st.button("로그아웃", use_container_width=True):
                sync_user_data(); st.session_state.clear(); st.rerun()
    else:
        c1, c2 = st.columns([3, 1])
        with c1: st.markdown(f"<div style='font-size:0.9rem;'>👤 <b>{st.session_state.logged_in_user}</b>{unread_txt} | <span style='color:#00E5FF;'>{st.session_state.equipped_title}</span><br>💵 {format_korean_money(st.session_state.global_cash)}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("로그아웃"): sync_user_data(); st.session_state.clear(); st.rerun()
        cat_sel = st.selectbox("카테고리", list(CATEGORY_MENUS.keys()), index=list(CATEGORY_MENUS.keys()).index(st.session_state.current_category))
        if cat_sel != st.session_state.current_category:
            st.session_state.current_category, st.session_state.current_page = cat_sel, CATEGORY_MENUS[cat_sel][0]; st.rerun()
        cur_cat_pages = CATEGORY_MENUS.get(st.session_state.current_category, [])
        cur_idx = cur_cat_pages.index(st.session_state.current_page) if st.session_state.current_page in cur_cat_pages else 0
        selected_menu = st.selectbox("메뉴 선택", cur_cat_pages, index=cur_idx)
        if selected_menu != st.session_state.current_page:
            st.session_state.current_page = selected_menu; st.rerun()

    st.markdown(f"<div class='news-banner'>📡 {market['news']}</div>", unsafe_allow_html=True)
    if market.get('admin_msg'):
        import html as _html_mod
        _safe_msg = _html_mod.escape(str(market['admin_msg']))
        _safe_color = _html_mod.escape(str(market.get('admin_color','#FF4B4B')))
        st.markdown(f"<div style='background:rgba(255,0,0,0.08);border:1px solid {_safe_color};border-radius:10px;padding:12px;color:{_safe_color}!important;font-weight:900;margin:8px 0;'>📢 [관리자 공지] {_safe_msg}</div>", unsafe_allow_html=True)

    menu = st.session_state.current_page
    if   menu == "🏠 홈 광장 (튜토리얼)":   from pages import home;              home.render(market, nw)
    elif menu == "💎 VIP 라운지":            from pages import vip;               vip.render(market, nw)
    elif menu == "📈 주식 트레이딩":         from pages import stock;             stock.render(market, nw)
    elif menu == "🪙 코인 거래소":           from pages import crypto;            crypto.render(market, nw)
    elif menu == "🏢 부동산 거래소":         from pages import real_estate;       real_estate.render(market, nw)
    elif menu == "🏦 은행 (대출/상환)":      from pages import bank;              bank.render(market, nw)
    elif menu == "📜 내 거래 기록":          from pages import txlog;             txlog.render(market, nw)
    elif menu == "👤 내 프로필":              from pages import profile;           profile.render(market, nw)
    elif menu == "🐾 펫 키우기":              from pages import pet;               pet.render(market, nw)
    elif menu == "📅 일일 퀘스트":           from pages import quest;             quest.render(market, nw)
    elif menu == "👑 칭호 상점":             from pages import title_shop;        title_shop.render(market, nw)
    elif menu == "🏅 랭킹 & 게시판": from pages import ranking;           ranking.render(market, nw)
    elif menu == "✉️ 개인 쪽지함":           from pages import dm;                dm.render(market, nw)
    elif menu == "🏰 길드/클랜":             from pages import clan;              clan.render(market, nw)
    elif menu == "🎰 럭키 슬롯":             from pages.games import slot;        slot.render(market, nw)
    elif menu == "🃏 블랙잭 카지노":         from pages.games import blackjack;   blackjack.render(market, nw)
    elif menu == "🃏 텍사스 홀덤":           from pages.games import holdem;      holdem.render(market, nw)
    elif menu == "⛏️ 광산 (노가다)":         from pages.games import mine;        mine.render(market, nw)
    elif menu == "💻 사주팔자":            from pages.games import quiz;        quiz.render(market, nw)
    elif menu == "⚔️ 글로벌 로또":           from pages.games import lotto;       lotto.render(market, nw)
    elif menu == "🗡️ 전설의 명검 강화":      from pages.games import forge;       forge.render(market, nw)
    elif menu == "🎴 가챠 뽑기":             from pages.games import gacha;       gacha.render(market, nw)
    elif menu == "⚽ 구단주 시뮬레이터":     from pages.sports import soccer_sim; soccer_sim.render(market, nw)
    elif menu == "⚽ 조기축구 승부차기":      from pages.sports import penalty;    penalty.render(market, nw)
    elif menu == "🏎️ 하이퍼카 레이싱":      from pages.sports import racing;     racing.render(market, nw)
    elif menu == "🛠️ 커스텀 튜닝 차고지":   from pages.sports import garage;     garage.render(market, nw)
    elif menu == "🛠️ 창조주 통제소":        from pages.admin import panel;       panel.render(market, nw)
    else: st.info(f"🚧 '{menu}' 페이지를 로드할 수 없습니다.")


# ==============================
# 6. [View 4] AI 아카데미
# ==============================
elif st.session_state.page_view == "project_a":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기"):
        st.session_state.page_view = "portal"; st.rerun()
    market = run_market_sync()
    from pages import project_a
    project_a.render(market, 0)


# ==============================
# 7. [View 5] 효민 월드 배틀
# ==============================
elif st.session_state.page_view == "project_b":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_b"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_b
    project_b.render()


# ==============================
# 8. [View 6] THE TERMINAL
# ==============================
elif st.session_state.page_view == "project_c":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_c"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_c
    project_c.render()


# ==============================
# 9. [View 7] 🎲 인베스트 마블
# ==============================
elif st.session_state.page_view == "project_d":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_d"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_d
    project_d.render()


# ==============================
# 10. [View 8] ⚔️ 뱀서라이크 던전
# ==============================
elif st.session_state.page_view == "project_e":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_e"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_e
    project_e.render()


# ==============================
# 11. [View 9] 🏎️ 네온 도주 레이싱
# ==============================
elif st.session_state.page_view == "project_f":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_f"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_f
    project_f.render()


# ==============================
# 12. [View 10] 🧟 좀비 아포칼립스
# ==============================
elif st.session_state.page_view == "project_g":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_g"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_g
    project_g.render()


# ==============================
# 13. [View 11] 🥊 스트리트 파이터 EX
# ==============================
elif st.session_state.page_view == "project_h":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_h"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_h
    project_h.render()


# ==============================
# 14. [View 12] 🎯 라인 배틀 저격전
# ==============================
elif st.session_state.page_view == "project_i":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_i"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_i
    project_i.render()


# ==============================
# 15. [View 13] ⚽ 얼티밋 사커 11
# ==============================
elif st.session_state.page_view == "project_j":
    if 'logged_in_user' not in st.session_state or not st.session_state.logged_in_user:
        st.session_state.page_view = "login"; st.rerun()
    if st.button("🏠 포털 메인으로 나가기", key="back_j"):
        st.session_state.page_view = "portal"; st.rerun()
    from pages import project_j
    project_j.render()
