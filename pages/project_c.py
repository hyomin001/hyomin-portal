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
#  WORLD DATA — 파일시스템 트리 & 로어(Lore)
# ══════════════════════════════════════════════════════════

# 각 스테이지마다 독립된 파일시스템을 정의
# 구조: {경로: {"type": "dir"|"file", "content": str, "hidden": bool}}
STAGES = {
    1: {
        "title": "STAGE 1 — 버려진 서버실",
        "desc":  "낡은 서버에서 관리자 비밀번호를 찾아라.",
        "difficulty": "⭐ 입문",
        "goal":  "비밀번호를 찾아 `unlock [비밀번호]` 명령어로 잠금을 해제하라.",
        "answer_hash": hashlib.sha256("hyomin2026".encode()).hexdigest(),
        "hint_1": "`ls -a` 로 숨김 파일도 볼 수 있다.",
        "hint_2": "`.secret` 파일을 열어보라. base64로 인코딩되어 있다.",
        "hint_3": "base64 디코딩: `decode [문자열]` 명령어를 써라.",
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
                "content": "aHlvbWluMjAyNg==",  # base64('hyomin2026')
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
        "goal":  "암호화된 프로젝트 코드명을 찾아 `unlock [코드명]` 으로 입력하라.",
        "answer_hash": hashlib.sha256("DOPAHYOMIN".encode()).hexdigest(),
        "hint_1": "`/lab/classified/` 디렉토리를 탐색해보라.",
        "hint_2": "cipher.txt 의 ROT13을 풀어야 한다. `rot13 [문자열]` 명령어를 사용해라.",
        "hint_3": "ROT13 결과에서 언더바(_)는 제거하고 대문자로만 입력해라.",
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
                    "QBCNULBZVA\n\n"   # ROT13('DOPAHYOMIN')
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
                    "암호는 labs 시스템 어딘가에 있다고 했다.\n"
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
        "goal":  "금고의 최종 패스프레이즈를 찾아 `unlock [패스프레이즈]` 로 입력하라.",
        "answer_hash": hashlib.sha256("UNIVERSE_ORIGIN_01".encode()).hexdigest(),
        "hint_1": "여러 파일의 단서를 조합해야 한다. `/vault` 와 `/archive` 를 모두 탐색하라.",
        "hint_2": "fragment_*.txt 파일들을 순서대로 모으면 패스프레이즈가 완성된다.",
        "hint_3": "패스프레이즈 형식: `[단어]_[단어]_[숫자두자리]` 조합이다. 언더바(_)로 연결.",
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
    """경로의 직접 자식 목록 반환"""
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
    """cd 명령어용 경로 해석"""
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
    """터미널 세션 상태 초기화"""
    st.session_state.terminal = {
        "stage":       stage_num,
        "cwd":         "/",
        "history":     [],
        "output":      [],
        "hint_used":   0,
        "solved":      False,
        "start_time":  time.time(),
        "cmd_count":   0,
    }

def add_output(lines):
    """출력 버퍼에 줄 추가"""
    t = st.session_state.terminal
    for line in lines:
        t["output"].append(line)
    # 최대 200줄 유지
    if len(t["output"]) > 200:
        t["output"] = t["output"][-200:]

def process_command(cmd_raw, stage_data):
    """명령어 처리 — 출력 리스트 반환"""
    fs = stage_data["filesystem"]
    t  = st.session_state.terminal
    cwd = t["cwd"]

    parts = cmd_raw.strip().split(None, 1)
    if not parts:
        return []
    cmd  = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    t["cmd_count"] += 1

    # ── ls / ls -a ──────────────────────────────
    if cmd == "ls":
        show_hidden = "-a" in args or "-la" in args or "-al" in args
        children = get_dir_children(fs, cwd)
        if not children:
            return ["(비어있음)"]
        out = []
        for name, info in sorted(children):
            is_hidden = info.get("hidden", False)
            if is_hidden and not show_hidden:
                continue
            if info["type"] == "dir":
                out.append(f"\033[34m{name}/\033[0m")  # 파란색 dir
            else:
                prefix = "." if is_hidden else ""
                out.append(prefix + name if not name.startswith(".") else name)
        return out if out else ["(표시할 항목 없음 — `-a` 옵션으로 숨김 파일 확인)"]

    # ── cd ───────────────────────────────────────
    elif cmd == "cd":
        target = args.strip() or "/"
        new_path = resolve_path(cwd, target)
        if new_path in fs and fs[new_path]["type"] == "dir":
            t["cwd"] = new_path
            return []
        # 존재하지 않는 경로
        return [f"bash: cd: {target}: No such file or directory"]

    # ── cat ─────────────────────────────────────
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

    # ── pwd ──────────────────────────────────────
    elif cmd == "pwd":
        return [cwd]

    # ── decode (base64) ──────────────────────────
    elif cmd == "decode":
        if not args:
            return ["사용법: decode [base64문자열]"]
        try:
            decoded = base64.b64decode(args.strip()).decode('utf-8')
            return [f"디코딩 결과: {decoded}"]
        except Exception:
            return ["오류: 유효한 base64 문자열이 아닙니다."]

    # ── rot13 ────────────────────────────────────
    elif cmd == "rot13":
        if not args:
            return ["사용법: rot13 [문자열]"]
        return [f"ROT13 결과: {rot13(args.strip())}"]

    # ── hint ─────────────────────────────────────
    elif cmd == "hint":
        used = t["hint_used"]
        hints = [
            stage_data.get("hint_1", ""),
            stage_data.get("hint_2", ""),
            stage_data.get("hint_3", ""),
        ]
        available = [h for h in hints if h]
        if used >= len(available):
            return ["더 이상 힌트가 없습니다."]
        t["hint_used"] += 1
        return [f"💡 힌트 {used+1}: {available[used]}",
                f"   (남은 힌트: {len(available) - t['hint_used']}개)"]

    # ── unlock ───────────────────────────────────
    elif cmd == "unlock":
        answer = args.strip()
        expected_hash = stage_data["answer_hash"]
        if hashlib.sha256(answer.encode()).hexdigest() == expected_hash:
            t["solved"] = True
            elapsed = int(time.time() - t["start_time"])
            mins, secs = divmod(elapsed, 60)
            reward = stage_data["reward"]
            return [
                "=" * 42,
                "  ✅  잠금 해제 성공!",
                "=" * 42,
                f"  클리어 시간: {mins}분 {secs}초",
                f"  사용한 명령어: {t['cmd_count']}개",
                f"  사용한 힌트: {t['hint_used']}개",
                f"  보상: {stage_data['reward_label']}",
                "",
                "  다음 스테이지로 진행할 수 있습니다.",
                "=" * 42,
            ]
        else:
            return ["❌ 잠금 해제 실패. 비밀번호가 틀렸습니다."]

    # ── clear ────────────────────────────────────
    elif cmd == "clear":
        t["output"] = []
        return []

    # ── help ─────────────────────────────────────
    elif cmd == "help":
        return [
            "사용 가능한 명령어:",
            "  ls          현재 디렉토리 목록",
            "  ls -a       숨김 파일 포함 목록",
            "  cd [경로]   디렉토리 이동",
            "  cat [파일]  파일 내용 보기",
            "  pwd         현재 경로 출력",
            "  decode [b64] base64 디코딩",
            "  rot13 [str]  ROT13 암복호화",
            "  hint        힌트 보기",
            "  unlock [pw] 잠금 해제 시도",
            "  clear       화면 지우기",
            "  help        이 도움말",
        ]

    # ── 알 수 없는 명령어 ─────────────────────────
    else:
        return [f"bash: {cmd}: command not found",
                "  사용 가능한 명령어 목록: help"]


# ══════════════════════════════════════════════════════════
#  메인 렌더 함수
# ══════════════════════════════════════════════════════════

TERMINAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

/* 터미널 전체 배경 */
.terminal-outer {
    background: #0d1117;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    margin: 0 0 16px 0;
}

/* 맥OS 스타일 상단 바 */
.term-titlebar {
    background: #1c2128;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #30363d;
}
.dot { width:12px;height:12px;border-radius:50%; }
.dot-r{background:#ff5f57;} .dot-y{background:#febc2e;} .dot-g{background:#28c840;}
.term-title { color:#8b949e; font-size:12px; margin-left:8px; }

/* 출력 영역 */
.term-body {
    background: #0d1117;
    padding: 16px 20px;
    min-height: 340px;
    max-height: 460px;
    overflow-y: auto;
    font-size: 13.5px;
    line-height: 1.65;
}
.term-line { color: #c9d1d9; white-space: pre-wrap; word-break: break-all; }
.term-line.green  { color: #3fb950; }
.term-line.yellow { color: #d29922; }
.term-line.red    { color: #f85149; }
.term-line.blue   { color: #58a6ff; }
.term-line.cyan   { color: #76e3ea; }
.term-line.dim    { color: #484f58; }
.term-prompt {
    color: #3fb950;
    display: inline;
}
.term-cwd { color: #58a6ff; display: inline; }
.blink-cursor {
    display: inline-block;
    width: 8px; height: 15px;
    background: #3fb950;
    animation: blink 1s step-end infinite;
    vertical-align: middle;
    margin-left: 2px;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* 스테이지 선택 카드 */
.stage-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: border-color 0.2s, box-shadow 0.2s;
    font-family: 'JetBrains Mono', monospace;
}
.stage-card:hover {
    border-color: #3fb950;
    box-shadow: 0 0 20px rgba(63,185,80,0.15);
}
.stage-title { color: #3fb950; font-size: 1rem; font-weight: 700; margin-bottom: 4px; }
.stage-meta  { color: #8b949e; font-size: 0.82rem; }
.stage-diff  { display: inline-block; margin-right: 12px; }

/* 클리어 배지 */
.clear-badge {
    background: rgba(63,185,80,0.15);
    border: 1px solid #3fb950;
    color: #3fb950;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    float: right;
}
</style>
"""

def render():
    # 전체 배경을 다크로
    st.markdown("""
    <style>
    .stApp { background-color: #010409 !important; }
    .stApp * { color: #c9d1d9 !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(TERMINAL_CSS, unsafe_allow_html=True)

    uid = st.session_state.get('logged_in_user', '')

    # 클리어 기록 (세션에 저장)
    if 'terminal_cleared' not in st.session_state:
        st.session_state.terminal_cleared = set()

    # ── 스테이지 선택 화면 ───────────────────────
    if 'terminal' not in st.session_state or \
       st.session_state.terminal.get('at_select', False):

        # 헤더
        st.markdown("""
        <div style='font-family:"JetBrains Mono",monospace; padding: 24px 0 8px;'>
          <div style='color:#3fb950;font-size:1.8rem;font-weight:700;letter-spacing:2px;'>
            &gt;_ THE TERMINAL
          </div>
          <div style='color:#8b949e;font-size:0.88rem;margin-top:6px;'>
            효민 유니버스의 숨겨진 흑막을 파헤치는 ARG 방탈출
          </div>
          <div style='color:#484f58;font-size:0.78rem;margin-top:4px;'>
            마우스는 잊어라. 오직 커맨드라인으로만 진실에 접근할 수 있다.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        for snum, sdata in STAGES.items():
            cleared = snum in st.session_state.terminal_cleared
            badge = "<span class='clear-badge'>✅ CLEARED</span>" if cleared else ""
            st.markdown(f"""
            <div class='stage-card'>
              <div class='stage-title'>{badge}{html.escape(sdata['title'])}</div>
              <div style='color:#8b949e;font-size:0.85rem;margin:4px 0 8px;'>
                {html.escape(sdata['desc'])}
              </div>
              <div class='stage-meta'>
                <span class='stage-diff'>{sdata['difficulty']}</span>
                <span style='color:#3fb950;'>보상: {sdata['reward_label']}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            btn_label = f"{'[REPLAY] ' if cleared else '[ENTER] '} STAGE {snum} 시작" 
            if st.button(btn_label, key=f"stage_btn_{snum}", use_container_width=True):
                init_terminal(snum)
                # 시작 메시지
                st.session_state.terminal["output"] = [
                    f"HYOMIN NETWORKS — Secure Shell v2.26",
                    f"Last login: {datetime.now(KST).strftime('%a %b %d %H:%M:%S %Y')}",
                    "",
                    f"== {sdata['title']} ==",
                    f"목표: {sdata['goal']}",
                    "",
                    "모르는 명령어는 `help` 를 입력하세요.",
                    "힌트가 필요하면 `hint` 를 입력하세요.",
                    "─" * 46,
                ]
                st.session_state.terminal['at_select'] = False
                st.rerun()

        return

    # ── 터미널 게임 화면 ─────────────────────────
    t = st.session_state.terminal
    stage_num  = t["stage"]
    stage_data = STAGES[stage_num]
    fs         = stage_data["filesystem"]

    # 상단 정보바
    elapsed = int(time.time() - t["start_time"])
    mins, secs = divmod(elapsed, 60)
    col_l, col_r = st.columns([3, 1])
    with col_l:
        st.markdown(
            f"<span style='font-family:monospace;color:#3fb950;font-size:0.85rem;'>"
            f"⏱ {mins:02d}:{secs:02d} &nbsp;|&nbsp; 🔢 CMD:{t['cmd_count']} &nbsp;|&nbsp; "
            f"💡 HINT:{t['hint_used']}/3 &nbsp;|&nbsp; "
            f"<span style='color:#58a6ff;'>{stage_data['title']}</span></span>",
            unsafe_allow_html=True
        )
    with col_r:
        if st.button("◀ 스테이지 선택", use_container_width=True):
            st.session_state.terminal['at_select'] = True
            st.rerun()

    # 터미널 출력 렌더링
    output_html = ""
    for line in t["output"]:
        # 특수 색상 처리
        safe_line = html.escape(line)
        if line.startswith("✅") or line.startswith("  ✅"):
            css_cls = "green"
        elif line.startswith("❌"):
            css_cls = "red"
        elif line.startswith("💡"):
            css_cls = "yellow"
        elif line.startswith("bash:"):
            css_cls = "red"
        elif line.startswith("="):
            css_cls = "cyan"
        elif line.startswith("  보상"):
            css_cls = "yellow"
        elif line.startswith("─"):
            css_cls = "dim"
        elif line.startswith("HYOMIN") or line.startswith("Last login"):
            css_cls = "dim"
        else:
            css_cls = ""
        output_html += f"<div class='term-line {css_cls}'>{safe_line}</div>"

    # 현재 프롬프트 줄
    cwd_disp = t["cwd"]
    output_html += (
        f"<div class='term-line'>"
        f"<span class='term-prompt'>user@hyomin</span>"
        f"<span style='color:#c9d1d9;'>:</span>"
        f"<span class='term-cwd'>{html.escape(cwd_disp)}</span>"
        f"<span style='color:#c9d1d9;'>$ </span>"
        f"<span class='blink-cursor'></span>"
        f"</div>"
    )

    st.markdown(f"""
    <div class='terminal-outer'>
      <div class='term-titlebar'>
        <div class='dot dot-r'></div>
        <div class='dot dot-y'></div>
        <div class='dot dot-g'></div>
        <div class='term-title'>hyomin@secure-shell — {html.escape(cwd_disp)}</div>
      </div>
      <div class='term-body' id='term-scroll'>{output_html}</div>
    </div>
    <script>
      var tb = document.getElementById('term-scroll');
      if(tb) tb.scrollTop = tb.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    # 명령어 입력창
    if not t["solved"]:
        cmd_input = st.text_input(
            label="명령어 입력",
            key=f"cmd_input_{t['cmd_count']}",
            placeholder="명령어를 입력하고 Enter ↵",
            label_visibility="collapsed",
        )

        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            pass
        with col2:
            if st.button("ENTER", use_container_width=True, type="primary"):
                if cmd_input and cmd_input.strip():
                    cwd_prompt = t["cwd"]
                    prompt_line = f"user@hyomin:{cwd_prompt}$ {cmd_input}"
                    add_output([prompt_line])
                    result = process_command(cmd_input, stage_data)
                    add_output(result)
                    t["history"].append(cmd_input)
                    st.rerun()
        with col3:
            if st.button("CLEAR", use_container_width=True):
                t["output"] = []
                st.rerun()

        # 빠른 힌트 버튼
        if st.button("💡 힌트 보기", use_container_width=True):
            add_output([f"user@hyomin:{t['cwd']}$ hint"])
            result = process_command("hint", stage_data)
            add_output(result)
            st.rerun() 

    else:
        # 클리어 상태
        st.session_state.terminal_cleared.add(stage_num)

        # 보상 지급
        reward_key = f"terminal_reward_{stage_num}"
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

        col_next, col_sel = st.columns(2)
        with col_sel:
            if st.button("◀ 스테이지 목록", use_container_width=True):
                st.session_state.terminal['at_select'] = True
                st.rerun()
        with col_next:
            next_stage = stage_num + 1
            if next_stage in STAGES:
                if st.button(f"▶ STAGE {next_stage} 도전", use_container_width=True, type="primary"):
                    init_terminal(next_stage)
                    st.session_state.terminal["output"] = [
                        f"HYOMIN NETWORKS — Secure Shell v2.26",
                        "",
                        f"== {STAGES[next_stage]['title']} ==",
                        f"목표: {STAGES[next_stage]['goal']}",
                        "",
                        "모르는 명령어는 `help` 를 입력하세요.",
                        "─" * 46,
                    ]
                    st.session_state.terminal['at_select'] = False
                    st.rerun()
            else:
                st.info("🏆 모든 스테이지를 클리어했습니다!")
