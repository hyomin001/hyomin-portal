# pages/project_c.py
# 💻 THE TERMINAL — 효민 유니버스 ARG 방탈출
import streamlit as st
import time
import base64
import hashlib
import html
from datetime import datetime
from utils.config import KST

# ══════════════════════════════════════════════════════════
#  WORLD DATA
# ══════════════════════════════════════════════════════════
STAGES = {
    1: {
        "title": "STAGE 1 — 버려진 서버실",
        "desc":  "낡은 서버에서 관리자 비밀번호를 찾아라.",
        "difficulty": "⭐ 입문",
        "goal":  "비밀번호를 찾아 unlock [비밀번호] 명령어로 잠금을 해제하라.",
        "answer_hash": hashlib.sha256("hyomin2026".encode()).hexdigest(),
        "hint_1": "ls -a 로 숨김 파일도 볼 수 있다.",
        "hint_2": ".secret 파일을 열어보라. base64로 인코딩되어 있다.",
        "hint_3": "decode [문자열] 명령어로 base64를 디코딩할 수 있다.",
        "filesystem": {
            "/": {"type": "dir"},
            "/home": {"type": "dir"},
            "/home/admin": {"type": "dir"},
            "/home/admin/notes.txt": {
                "type": "file",
                "content": (
                    "== 관리자 메모 ==\n"
                    "서버 점검 완료. 비밀번호는 안전한 곳에 숨겨 두었다.\n"
                    "혹시나 싶어서 .secret 파일에 백업해 놓음.\n"
                    "-- admin"
                )
            },
            "/home/admin/.secret": {
                "type": "file",
                "hidden": True,
                "content": "aHlvbWluMjAyNg==",
            },
            "/var": {"type": "dir"},
            "/var/log": {"type": "dir"},
            "/var/log/access.log": {
                "type": "file",
                "content": (
                    "2026-01-03 09:12:44  LOGIN  admin  SUCCESS\n"
                    "2026-01-03 11:55:02  LOGIN  unknown  FAIL\n"
                    "2026-01-03 11:55:18  LOGIN  unknown  FAIL\n"
                    "2026-01-04 03:22:11  LOGIN  ???  SUCCESS  [비정상 접근]\n"
                ),
            },
        },
        "reward": 50_000_000,
        "reward_label": "5천만원",
    },
    2: {
        "title": "STAGE 2 — 지하 연구소",
        "desc":  "연구소 데이터베이스에서 프로젝트 코드명을 해독하라.",
        "difficulty": "⭐⭐ 보통",
        "goal":  "암호화된 프로젝트 코드명을 찾아 unlock [코드명] 으로 입력하라.",
        "answer_hash": hashlib.sha256("DOPAHYOMIN".encode()).hexdigest(),
        "hint_1": "/lab/classified/ 디렉토리를 탐색해보라.",
        "hint_2": "cipher.txt 의 ROT13을 풀어야 한다. rot13 [문자열] 명령어를 사용해라.",
        "hint_3": "ROT13 결과를 그대로 대문자로 입력하면 된다.",
        "filesystem": {
            "/": {"type": "dir"},
            "/lab": {"type": "dir"},
            "/lab/README.txt": {
                "type": "file",
                "content": (
                    "=== 효민 네트웍스 지하 연구소 ===\n"
                    "이 시스템은 외부 접근이 차단되어 있습니다.\n"
                    "모든 기밀 파일은 /lab/classified/ 에 있습니다.\n"
                    "비인가 접근 시 즉시 보안팀에 통보됩니다."
                )
            },
            "/lab/classified": {"type": "dir"},
            "/lab/classified/project_list.txt": {
                "type": "file",
                "content": (
                    "프로젝트 목록 (코드명 암호화됨)\n"
                    "-------------------------------\n"
                    "PRJ-001: [REDACTED]\n"
                    "PRJ-002: [REDACTED]\n"
                    "PRJ-003: cipher.txt 참조\n"
                    "-------------------------------\n"
                    "암호화 키는 연구소장 Dr.K 만 알고 있음."
                )
            },
            "/lab/classified/cipher.txt": {
                "type": "file",
                "content": (
                    "== ROT13 암호화 ==\n"
                    "QBCNULBZVA\n\n"
                    "이 코드명은 절대 외부에 유출되어선 안 됩니다.\n"
                    "-- Dr.K"
                )
            },
            "/lab/classified/.drk_memo": {
                "type": "file",
                "hidden": True,
                "content": (
                    "개인 메모 — Dr.K\n"
                    "오늘 효민이 직접 연락해왔다.\n"
                    "프로젝트 DOPAHYOMIN... 그가 알고 있는 걸까?\n"
                    "만약 이 파일을 누군가 읽고 있다면,\n"
                    "당신은 이미 너무 깊이 들어온 것이다."
                )
            },
            "/home": {"type": "dir"},
            "/home/drk": {"type": "dir"},
            "/home/drk/diary.txt": {
                "type": "file",
                "content": (
                    "일기 — 2026.02.14\n\n"
                    "그가 다시 나타났다. 포털 뒤에 숨어서\n"
                    "모든 것을 지켜보고 있었다는 걸 이제야 알았다.\n"
                    "암호는 lab 시스템 어딘가에 있다고 했다.\n"
                    "ROT13... 오래된 방식이지만 효과적이다."
                )
            },
        },
        "reward": 150_000_000,
        "reward_label": "1억 5천만원",
    },
    3: {
        "title": "STAGE 3 — 효민의 금고",
        "desc":  "효민 유니버스의 창조자가 남긴 최후의 비밀을 해독하라.",
        "difficulty": "⭐⭐⭐ 어려움",
        "goal":  "금고의 최종 패스프레이즈를 찾아 unlock [패스프레이즈] 로 입력하라.",
        "answer_hash": hashlib.sha256("UNIVERSE_ORIGIN_01".encode()).hexdigest(),
        "hint_1": "여러 파일의 단서를 조합해야 한다. /vault 와 /archive 를 모두 탐색하라.",
        "hint_2": "fragment_1, fragment_2, fragment_3 파일들을 순서대로 모아라.",
        "hint_3": "패스프레이즈 형식: [단어]_[단어]_[숫자두자리] — 언더바(_)로 연결, 모두 대문자.",
        "filesystem": {
            "/": {"type": "dir"},
            "/vault": {"type": "dir"},
            "/vault/lock_info.txt": {
                "type": "file",
                "content": (
                    "=== 효민 금고 잠금 시스템 v3 ===\n\n"
                    "패스프레이즈는 3개의 조각으로 나뉘어 숨겨져 있습니다.\n"
                    "각 조각은 시스템 곳곳에 분산되어 있습니다.\n\n"
                    "힌트: 조각들은 fragment_1, fragment_2, fragment_3 파일에 있습니다.\n"
                    "완성된 패스프레이즈: [조각1]_[조각2]_[조각3]\n"
                    "(모두 대문자, 세 번째는 숫자 두 자리)"
                )
            },
            "/vault/.fragment_1": {
                "type": "file",
                "hidden": True,
                "content": "조각 1/3: UNIVERSE"
            },
            "/archive": {"type": "dir"},
            "/archive/old_logs": {"type": "dir"},
            "/archive/old_logs/system_2025.log": {
                "type": "file",
                "content": (
                    "2025-12-31 23:59:59  SYSTEM_BOOT  HYOMIN_UNIVERSE_v1\n"
                    "2025-12-31 23:59:59  INIT  Creating world...\n"
                    "2026-01-01 00:00:00  WORLD_BORN  Season 1 start\n"
                    "2026-01-01 00:00:01  NOTE: 기원(ORIGIN)을 잊지 마라.\n"
                    "2026-01-01 00:00:02  fragment_2 archived.\n"
                )
            },
            "/archive/fragment_2.txt": {
                "type": "file",
                "content": "조각 2/3: ORIGIN"
            },
            "/archive/old_logs/.hidden_record": {
                "type": "file",
                "hidden": True,
                "content": (
                    "== 창조 기록 ==\n"
                    "이 세계는 2026년 1월 1일에 시작됐다.\n"
                    "창조자는 그 날짜를 기억하길 원한다.\n"
                    "마지막 조각은 /tmp 에 있다."
                )
            },
            "/tmp": {"type": "dir"},
            "/tmp/fragment_3.txt": {
                "type": "file",
                "content": "조각 3/3: 01 (창조의 달, 01월)"
            },
            "/tmp/.creator_note": {
                "type": "file",
                "hidden": True,
                "content": (
                    "만약 여기까지 왔다면,\n"
                    "당신은 이 세계의 숨겨진 진실을 알 자격이 있다.\n\n"
                    "효민 유니버스는 단순한 게임이 아니다.\n"
                    "모든 유저의 선택이 이 세계를 만들고 있다.\n\n"
                    "마지막 문을 열어라.\n"
                    "— 창조자"
                )
            },
        },
        "reward": 500_000_000,
        "reward_label": "5억원",
    },
}

# ══════════════════════════════════════════════════════════
#  헬퍼 함수
# ══════════════════════════════════════════════════════════

def rot13(text):
    result = []
    for c in text:
        if 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        elif 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        else:
            result.append(c)
    return ''.join(result)

def get_dir_children(fs, path):
    if path != '/':
        path = path.rstrip('/')
    children = []
    for key in fs:
        if key == path:
            continue
        parent = key.rsplit('/', 1)[0] or '/'
        if parent == path:
            name = key.rsplit('/', 1)[-1]
            children.append((name, fs[key]))
    return children

def resolve_path(current, target):
    if target == '/':
        return '/'
    if target.startswith('/'):
        return target.rstrip('/') or '/'
    if target == '..':
        if current == '/':
            return '/'
        return current.rsplit('/', 1)[0] or '/'
    if target == '.':
        return current
    if current == '/':
        return '/' + target
    return current + '/' + target

def init_terminal(stage_num):
    st.session_state.terminal = {
        "stage":      stage_num,
        "cwd":        "/",
        "history":    [],
        "output":     [],
        "hint_used":  0,
        "solved":     False,
        "start_time": time.time(),
        "cmd_count":  0,
        "at_select":  False,
    }

def add_output(lines):
    t = st.session_state.terminal
    for line in lines:
        t["output"].append(line)
    if len(t["output"]) > 300:
        t["output"] = t["output"][-300:]

def process_command(cmd_raw, stage_data):
    fs  = stage_data["filesystem"]
    t   = st.session_state.terminal
    cwd = t["cwd"]

    parts = cmd_raw.strip().split(None, 1)
    if not parts:
        return []
    cmd  = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""
    t["cmd_count"] += 1

    if cmd == "ls":
        show_hidden = "-a" in args or "-la" in args or "-al" in args
        children = get_dir_children(fs, cwd)
        if not children:
            return ["(비어있음)"]
        out = []
        for name, info in sorted(children):
            if info.get("hidden", False) and not show_hidden:
                continue
            suffix = "/" if info["type"] == "dir" else ""
            out.append(name + suffix)
        return out if out else ["(표시할 항목 없음 — ls -a 로 숨김 파일 확인)"]

    elif cmd == "cd":
        target = args.strip() or "/"
        new_path = resolve_path(cwd, target)
        if new_path in fs and fs[new_path]["type"] == "dir":
            t["cwd"] = new_path
            return []
        return [f"cd: {target}: No such file or directory"]

    elif cmd == "cat":
        if not args:
            return ["사용법: cat [파일명]"]
        target = resolve_path(cwd, args.strip())
        if target in fs:
            info = fs[target]
            if info["type"] == "dir":
                return [f"cat: {args}: Is a directory"]
            return info["content"].split("\n")
        return [f"cat: {args}: No such file or directory"]

    elif cmd == "pwd":
        return [cwd]

    elif cmd == "decode":
        if not args:
            return ["사용법: decode [base64문자열]"]
        try:
            decoded = base64.b64decode(args.strip()).decode('utf-8')
            return [f"디코딩 결과: {decoded}"]
        except Exception:
            return ["오류: 유효한 base64 문자열이 아닙니다."]

    elif cmd == "rot13":
        if not args:
            return ["사용법: rot13 [문자열]"]
        return [f"ROT13 결과: {rot13(args.strip())}"]

    elif cmd == "hint":
        used   = t["hint_used"]
        hints  = [stage_data.get(f"hint_{i}", "") for i in range(1, 4)]
        avail  = [h for h in hints if h]
        if used >= len(avail):
            return ["더 이상 힌트가 없습니다."]
        t["hint_used"] += 1
        return [
            f"[힌트 {used+1}] {avail[used]}",
            f"       남은 힌트: {len(avail) - t['hint_used']}개",
        ]

    elif cmd == "unlock":
        answer = args.strip()
        if hashlib.sha256(answer.encode()).hexdigest() == stage_data["answer_hash"]:
            t["solved"] = True
            elapsed = int(time.time() - t["start_time"])
            mins, secs = divmod(elapsed, 60)
            return [
                "=" * 46,
                "  >> 잠금 해제 성공!",
                "=" * 46,
                f"  클리어 시간  : {mins}분 {secs}초",
                f"  사용 명령어  : {t['cmd_count']}개",
                f"  사용 힌트    : {t['hint_used']}개",
                f"  보상         : {stage_data['reward_label']}",
                "=" * 46,
            ]
        return [">> 잠금 해제 실패. 비밀번호가 틀렸습니다."]

    elif cmd == "clear":
        t["output"] = []
        return []

    elif cmd == "help":
        return [
            "── 사용 가능한 명령어 ────────────────────",
            "  ls            현재 디렉토리 목록",
            "  ls -a         숨김 파일 포함 목록",
            "  cd [경로]     디렉토리 이동  (cd .. 으로 상위 이동)",
            "  cat [파일]    파일 내용 보기",
            "  pwd           현재 경로 출력",
            "  decode [b64]  base64 디코딩",
            "  rot13 [str]   ROT13 암복호화",
            "  hint          힌트 보기 (최대 3개)",
            "  unlock [pw]   잠금 해제 시도",
            "  clear         화면 지우기",
            "  help          이 도움말",
            "─────────────────────────────────────────",
        ]

    else:
        return [
            f"bash: {cmd}: command not found",
            "  도움말: help",
        ]


# ══════════════════════════════════════════════════════════
#  CSS — 흰 배경 위에 진한 텍스트, 터미널 박스만 검정
# ══════════════════════════════════════════════════════════
TERMINAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Noto+Sans+KR:wght@400;600;700;900&display=swap');

/* 스테이지 선택 화면 */
.tc-wrap { font-family: 'Noto Sans KR', sans-serif; max-width: 720px; margin: 0 auto; }

.tc-hero { padding: 28px 0 20px; }
.tc-hero-tag {
    display: inline-block; background: #0F172A; color: #4ADE80;
    font-family: 'JetBrains Mono', monospace; font-size: .72rem;
    padding: 4px 14px; border-radius: 4px; margin-bottom: 14px;
    letter-spacing: 2px;
}
.tc-hero-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(1.6rem, 4vw, 2.6rem); font-weight: 700;
    color: #0F172A; line-height: 1.1; margin-bottom: 6px;
}
.tc-hero-sub { font-size: .88rem; color: #475569; }

/* 스테이지 카드 */
.sc {
    border: 1.5px solid #E2E8F0; border-radius: 14px;
    padding: 20px 22px; margin-bottom: 12px;
    background: #FAFAFA;
    transition: border-color .18s, box-shadow .18s, transform .18s;
    position: relative; overflow: hidden;
}
.sc:hover { border-color: #0F172A; box-shadow: 0 8px 32px rgba(15,23,42,.1); transform: translateY(-2px); }
.sc::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; border-radius:4px 0 0 4px; }
.sc-1::before { background: #22C55E; }
.sc-2::before { background: #F59E0B; }
.sc-3::before { background: #EF4444; }

.sc-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.sc-title { font-family: 'JetBrains Mono', monospace; font-size: .98rem; font-weight: 700; color: #0F172A; }
.sc-cleared { background: #DCFCE7; color: #166534; font-size: .68rem; font-weight: 700; padding: 2px 10px; border-radius: 20px; border: 1px solid #86EFAC; }
.sc-desc   { font-size: .85rem; color: #475569; margin-bottom: 10px; }
.sc-footer { display: flex; gap: 16px; align-items: center; font-size: .8rem; }
.sc-diff   { color: #64748B; }
.sc-reward { color: #0F172A; font-weight: 700; }

/* ── 터미널 박스 ── */
.term-outer {
    background: #0D1117; border-radius: 12px;
    overflow: hidden; margin-bottom: 12px;
    box-shadow: 0 8px 32px rgba(0,0,0,.18), 0 0 0 1px rgba(255,255,255,.06);
}
.term-bar {
    background: #161B22; padding: 10px 16px;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid #21262D;
}
.td { width:12px; height:12px; border-radius:50%; }
.td-r{background:#FF5F56;} .td-y{background:#FFBD2E;} .td-g{background:#27C93F;}
.term-bar-title { color: #8B949E; font-family:'JetBrains Mono',monospace; font-size:.78rem; margin-left:6px; }

.term-body {
    padding: 16px 20px; min-height: 320px; max-height: 440px;
    overflow-y: auto; font-family: 'JetBrains Mono', monospace;
    font-size: 13px; line-height: 1.75; background: #0D1117;
}

/* 출력 줄 색상 — 터미널 안은 어두운 배경이므로 밝은 색 */
.tl      { color: #C9D1D9; white-space: pre-wrap; word-break: break-all; }
.tl-grn  { color: #3FB950; }
.tl-red  { color: #F85149; }
.tl-yel  { color: #D29922; }
.tl-cyn  { color: #76E3EA; }
.tl-dim  { color: #484F58; }
.tl-dir  { color: #58A6FF; }   /* 디렉토리 */

.term-prompt { color: #3FB950; }
.term-cwd    { color: #58A6FF; }
.term-dollar { color: #C9D1D9; }
.blink-cur   { display:inline-block; width:8px; height:14px; background:#3FB950; animation: cur-blink 1s step-end infinite; vertical-align:middle; margin-left:1px; }
@keyframes cur-blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* 정보 바 (터미널 위) */
.info-bar {
    display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
    padding: 8px 14px; background: #F1F5F9; border: 1px solid #E2E8F0;
    border-radius: 10px; margin-bottom: 8px; font-size: .8rem; color: #334155;
    font-family: 'JetBrains Mono', monospace;
}
.ib-stage { color: #0F172A; font-weight: 700; }
.ib-time  { color: #475569; }
.ib-hint  { color: #D97706; }
.ib-cmd   { color: #0284C7; }
</style>
"""

def render():
    st.markdown(TERMINAL_CSS, unsafe_allow_html=True)

    uid = st.session_state.get('logged_in_user', '')
    if 'terminal_cleared' not in st.session_state:
        st.session_state.terminal_cleared = set()

    # ── 스테이지 선택 ─────────────────────────
    if 'terminal' not in st.session_state or \
       st.session_state.terminal.get('at_select', False):

        st.markdown("""
        <div class='tc-wrap'>
          <div class='tc-hero'>
            <div class='tc-hero-tag'>&gt;_ THE TERMINAL</div>
            <div class='tc-hero-title'>효민 유니버스의<br>흑막을 파헤쳐라</div>
            <div class='tc-hero-sub'>
              ARG 방탈출 · 오직 커맨드라인으로만 진실에 접근할 수 있다
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        for snum, sdata in STAGES.items():
            cleared = snum in st.session_state.terminal_cleared
            badge   = "<span class='sc-cleared'>✅ CLEARED</span>" if cleared else ""
            sc_cls  = f"sc sc-{snum}"
            st.markdown(f"""
            <div class='{sc_cls}'>
              <div class='sc-header'>
                <span class='sc-title'>{html.escape(sdata['title'])}</span>
                {badge}
              </div>
              <div class='sc-desc'>{html.escape(sdata['desc'])}</div>
              <div class='sc-footer'>
                <span class='sc-diff'>{sdata['difficulty']}</span>
                <span class='sc-reward'>보상 {sdata['reward_label']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            btn_txt = f"{'[REPLAY]' if cleared else '[ENTER]'} STAGE {snum} 시작"
            if st.button(btn_txt, key=f"sb_{snum}", use_container_width=True):
                init_terminal(snum)
                st.session_state.terminal["output"] = [
                    "HYOMIN NETWORKS — Secure Shell v2.26",
                    f"Last login: {datetime.now(KST).strftime('%a %b %d %H:%M:%S %Y')}",
                    "",
                    f"=== {sdata['title']} ===",
                    f"목표: {sdata['goal']}",
                    "",
                    "모르는 명령어는 help 를 입력하세요.",
                    "힌트가 필요하면 hint 를 입력하세요.",
                    "─" * 46,
                ]
                st.rerun()
        return

    # ── 터미널 게임 ───────────────────────────
    t          = st.session_state.terminal
    stage_num  = t["stage"]
    stage_data = STAGES[stage_num]

    elapsed    = int(time.time() - t["start_time"])
    mins, secs = divmod(elapsed, 60)

    # 정보 바
    col_info, col_back = st.columns([4, 1])
    with col_info:
        st.markdown(f"""
        <div class='info-bar'>
          <span class='ib-stage'>{html.escape(stage_data['title'])}</span>
          <span class='ib-time'>⏱ {mins:02d}:{secs:02d}</span>
          <span class='ib-cmd'>CMD {t['cmd_count']}</span>
          <span class='ib-hint'>💡 힌트 {t['hint_used']}/3</span>
        </div>
        """, unsafe_allow_html=True)
    with col_back:
        if st.button("◀ 목록", use_container_width=True):
            st.session_state.terminal['at_select'] = True
            st.rerun()

    # 터미널 출력 HTML 빌드
    out_html = ""
    for line in t["output"]:
        safe = html.escape(line)
        if line.startswith("=") or line.startswith("─") or line.startswith("──"):
            cls = "tl-cyn"
        elif line.startswith(">> 잠금 해제 성공") or line.startswith("  >> 잠금"):
            cls = "tl-grn"
        elif "실패" in line or line.startswith("bash:") or line.startswith("cd:") or line.startswith("cat:"):
            cls = "tl-red"
        elif line.startswith("[힌트"):
            cls = "tl-yel"
        elif line.startswith("  보상") or line.startswith("  클리어") or line.startswith("  사용"):
            cls = "tl-grn"
        elif line.startswith("HYOMIN") or line.startswith("Last login") or line.startswith("──"):
            cls = "tl-dim"
        elif line.endswith("/"):
            cls = "tl-dir"
        else:
            cls = ""
        out_html += f"<div class='tl {cls}'>{safe}</div>"

    cwd_disp = t["cwd"]
    out_html += (
        f"<div class='tl'>"
        f"<span class='term-prompt'>user@hyomin</span>"
        f"<span class='term-dollar'>:</span>"
        f"<span class='term-cwd'>{html.escape(cwd_disp)}</span>"
        f"<span class='term-dollar'>$ </span>"
        f"<span class='blink-cur'></span>"
        f"</div>"
    )

    st.markdown(f"""
    <div class='term-outer'>
      <div class='term-bar'>
        <div class='td td-r'></div>
        <div class='td td-y'></div>
        <div class='td td-g'></div>
        <span class='term-bar-title'>hyomin@secure-shell: {html.escape(cwd_disp)}</span>
      </div>
      <div class='term-body' id='tscroll'>{out_html}</div>
    </div>
    <script>
      var el = document.getElementById('tscroll');
      if(el) el.scrollTop = el.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    # 입력창
    if not t["solved"]:
        cmd_in = st.text_input(
            "cmd",
            key=f"ci_{t['cmd_count']}",
            placeholder="명령어 입력 후 Enter ↵  (모르면 help)",
            label_visibility="collapsed",
        )
        c1, c2, c3, c4 = st.columns([4, 1, 1, 1])
        with c2:
            if st.button("실행", use_container_width=True, type="primary"):
                if cmd_in and cmd_in.strip():
                    add_output([f"user@hyomin:{t['cwd']}$ {cmd_in}"])
                    add_output(process_command(cmd_in, stage_data))
                    t["history"].append(cmd_in)
                    st.rerun()
        with c3:
            if st.button("힌트", use_container_width=True):
                add_output([f"user@hyomin:{t['cwd']}$ hint"])
                add_output(process_command("hint", stage_data))
                st.rerun()
        with c4:
            if st.button("지우기", use_container_width=True):
                t["output"] = []
                st.rerun()

    else:
        # 클리어
        st.session_state.terminal_cleared.add(stage_num)
        reward_key = f"tr_{stage_num}"
        if reward_key not in st.session_state:
            st.session_state[reward_key] = True
            reward = stage_data["reward"]
            st.session_state.global_cash = st.session_state.get('global_cash', 0) + reward
            from utils.core import sync_user_data
            from utils.database import log_tx
            sync_user_data()
            log_tx(uid, "터미널", f"THE TERMINAL Stage {stage_num} 클리어", reward)
            st.balloons()

        st.success(f"🎉 STAGE {stage_num} 클리어! {stage_data['reward_label']} 보상 지급 완료!")

        c_sel, c_next = st.columns(2)
        with c_sel:
            if st.button("◀ 스테이지 목록", use_container_width=True):
                st.session_state.terminal['at_select'] = True
                st.rerun()
        with c_next:
            nxt = stage_num + 1
            if nxt in STAGES:
                if st.button(f"▶ STAGE {nxt} 도전", use_container_width=True, type="primary"):
                    init_terminal(nxt)
                    st.session_state.terminal["output"] = [
                        "HYOMIN NETWORKS — Secure Shell v2.26",
                        "",
                        f"=== {STAGES[nxt]['title']} ===",
                        f"목표: {STAGES[nxt]['goal']}",
                        "",
                        "모르는 명령어는 help 를 입력하세요.",
                        "─" * 46,
                    ]
                    st.rerun()
            else:
                st.info("🏆 모든 스테이지를 클리어했습니다!")
