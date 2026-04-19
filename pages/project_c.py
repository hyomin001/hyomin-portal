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
    if target == '/': return '/'
    if target.startswith('/'): return target.rstrip('/') or '/'
    if target == '..':
        if current == '/': return '/'
        return current.rsplit('/', 1)[0] or '/'
    if target == '.': return current
    if current == '/': return '/' + target
    return current + '/' + target

def init_terminal(stage_num):
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
    t = st.session_state.terminal
    for line in lines:
        t["output"].append(line)
    if len(t["output"]) > 200:
        t["output"] = t["output"][-200:]

def process_command(cmd_raw, stage_data):
    fs = stage_data["filesystem"]
    t  = st.session_state.terminal
    cwd = t["cwd"]

    parts = cmd_raw.strip().split(None, 1)
    if not parts: return []
    cmd  = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    t["cmd_count"] += 1

    if cmd == "ls":
        show_hidden = "-a" in args or "-la" in args or "-al" in args
        children = get_dir_children(fs, cwd)
        if not children: return ["(비어있음)"]
        out = []
        for name, info in sorted(children):
            is_hidden = info.get("hidden", False)
            if is_hidden and not show_hidden: continue
            if info["type"] == "dir":
                out.append(f"\033[34m{name}/\033[0m") 
            else:
                prefix = "." if is_hidden else ""
                out.append(prefix + name if not name.startswith(".") else name)
        return out if out else ["(표시할 항목 없음 — `-a` 옵션으로 숨김 파일 확인)"]

    elif cmd == "cd":
        target = args.strip() or "/"
        new_path = resolve_path(cwd, target)
        if new_path in fs and fs[new_path]["type"] == "dir":
            t["cwd"] = new_path
            return []
        return [f"bash: cd: {target}: No such file or directory"]

    elif cmd == "cat":
        if not args: return ["사용법: cat [파일명]"]
        target = resolve_path(cwd, args.strip())
        if target in fs:
            info = fs[target]
            if info["type"] == "dir": return [f"cat: {args}: Is a directory"]
            return info["content"].split("\n")
        return [f"cat: {args}: No such file or directory"]

    elif cmd == "pwd":
        return [cwd]

    elif cmd == "decode":
        if not args: return ["사용법: decode [base64문자열]"]
        try:
            decoded = base64.b64decode(args.strip()).decode('utf-8')
            return [f"디코딩 결과: {decoded}"]
        except Exception:
            return ["오류: 유효한 base64 문자열이 아닙니다."]

    elif cmd == "rot13":
        if not args: return ["사용법: rot13 [문자열]"]
        return [f"ROT13 결과: {rot13(args.strip())}"]

    elif cmd == "hint":
        used = t["hint_used"]
        hints = [stage_data.get("hint_1", ""), stage_data.get("hint_2", ""), stage_data.get("hint_3", "")]
        available = [h for h in hints if h]
        if used >= len(available): return ["더 이상 힌트가 없습니다."]
        t["hint_used"] += 1
        return [f"💡 힌트 {used+1}: {available[used]}", f"   (남은 힌트: {len(available) - t['hint_used']}개)"]

    elif cmd == "unlock":
        answer = args.strip()
        expected_hash = stage_data["answer_hash"]
        if hashlib.sha256(answer.encode()).hexdigest() == expected_hash:
            t["solved"] = True
            elapsed = int(time.time() - t["start_time"])
            mins, secs = divmod(elapsed, 60)
            return [
                "=" * 42,
                "  ✅  잠금 해제 성공! 시스템 권한 획득",
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
            return ["❌ 접근 거부. 비밀번호가 일치하지 않습니다."]

    elif cmd == "clear":
        t["output"] = []
        return []

    elif cmd == "help":
        return [
            "사용 가능한 명령어:",
            "  ls          현재 디렉토리 목록",
            "  ls -a       숨김 파일 포함 목록",
            "  cd [경로]   디렉토리 이동",
            "  cat [파일]  파일 내용 보기",
            "  pwd         현재 경로 출력",
            "  decode      base64 디코딩 (예: decode aGVsbG8=)",
            "  rot13       ROT13 암복호화 (예: rot13 Uryyb)",
            "  hint        힌트 보기",
            "  unlock [pw] 잠금 해제 시도",
            "  clear       화면 지우기",
            "  help        이 도움말",
        ]

    else:
        return [f"bash: {cmd}: command not found", "  사용 가능한 명령어 목록을 보려면 help를 입력하세요."]


# ══════════════════════════════════════════════════════════
#  프리미엄 UI CSS 및 렌더링
# ══════════════════════════════════════════════════════════

PREMIUM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Pretendard:wght@400;600;800&display=swap');

/* 기존 화면 전체 어둡게 하는 코드 제거 -> 포털 본연의 밝은 테마 유지 */
/* 입력창 글씨가 안 보이는 문제는 이것으로 해결됨 */

/* --- 스테이지 선택 화면 (요원 브리핑 스타일) --- */
.mission-header { text-align: center; margin: 30px 0 40px; font-family: 'Pretendard', sans-serif; }
.mission-title { font-size: 2.5rem; font-weight: 800; color: #0F172A; letter-spacing: 2px; font-family: 'JetBrains Mono', monospace; }
.mission-subtitle { font-size: 1.05rem; color: #64748B; margin-top: 10px; font-weight: 600; }

.stage-card {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    border-left: 6px solid #3B82F6;
    font-family: 'Pretendard', sans-serif;
    transition: all 0.2s ease;
}
.stage-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 25px rgba(59,130,246,0.15);
    border-color: #3B82F6;
}
.stage-card.cleared { border-left-color: #10B981; background: #F8FAFC; }

.s-title { font-size: 1.25rem; font-weight: 800; color: #1E293B; font-family: 'JetBrains Mono', monospace; }
.s-desc { color: #64748B; font-size: 0.95rem; margin: 8px 0 16px; line-height: 1.5; }
.s-meta { display: flex; gap: 15px; font-size: 0.85rem; font-weight: 600; }
.s-diff { background: #F1F5F9; color: #475569; padding: 4px 12px; border-radius: 20px; }
.s-reward { background: rgba(59,130,246,0.1); color: #2563EB; padding: 4px 12px; border-radius: 20px; }
.s-cleared-badge { float: right; background: rgba(16,185,129,0.1); color: #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; }

/* --- 고퀄리티 터미널 UI --- */
.terminal-window {
    background: #0A0F1A;
    border-radius: 14px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.4);
    overflow: hidden;
    border: 1px solid #1E293B;
    margin-bottom: 20px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
}
.mac-titlebar {
    background: #111827;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #1F2937;
}
.mac-dot { width: 12px; height: 12px; border-radius: 50%; margin-right: 8px; }
.mac-dot.red { background: #EF4444; }
.mac-dot.yellow { background: #F59E0B; }
.mac-dot.green { background: #10B981; }
.mac-title { color: #94A3B8; font-size: 0.8rem; margin-left: 10px; font-weight: 600; }

.term-body {
    padding: 20px 24px;
    min-height: 400px;
    max-height: 500px;
    overflow-y: auto;
    font-size: 0.95rem;
    line-height: 1.6;
}
.t-line { color: #E2E8F0; white-space: pre-wrap; word-break: break-all; margin-bottom: 2px; }
.t-line.green  { color: #10B981; font-weight: 700; }
.t-line.yellow { color: #F59E0B; }
.t-line.red    { color: #EF4444; font-weight: 700; }
.t-line.blue   { color: #3B82F6; }
.t-line.cyan   { color: #06B6D4; font-weight: 700; }
.t-line.dim    { color: #64748B; }

.t-prompt { color: #10B981; font-weight: 700; }
.t-cwd { color: #3B82F6; font-weight: 700; }
.t-cursor {
    display: inline-block; width: 9px; height: 16px; background: #10B981;
    animation: blink 1s step-end infinite; vertical-align: middle; margin-left: 4px;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

/* 터미널 입력창 강제 스타일링 (입력창 내부 글씨 검정색 보장) */
div[data-testid="stTextInput"] input {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #0F172A !important;  /* 글씨 무조건 검정/진한회색 */
    background-color: #FFFFFF !important; /* 하얀 바탕 보장 */
}
</style>
"""

def render():
    st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

    uid = st.session_state.get('logged_in_user', '')

    if 'terminal_cleared' not in st.session_state:
        st.session_state.terminal_cleared = set()

    # ── [화면 1] 스테이지 선택 화면 (미션 브리핑) ──
    if 'terminal' not in st.session_state or st.session_state.terminal.get('at_select', False):
        st.markdown("""
        <div class='mission-header'>
            <div class='mission-title'>_THE TERMINAL</div>
            <div class='mission-subtitle'>효민 유니버스의 숨겨진 진실을 파헤치는 코드 해독 미션</div>
        </div>
        """, unsafe_allow_html=True)

        for snum, sdata in STAGES.items():
            cleared = snum in st.session_state.terminal_cleared
            cls_name = "stage-card cleared" if cleared else "stage-card"
            badge = "<span class='s-cleared-badge'>SYSTEM UNLOCKED</span>" if cleared else ""
            
            st.markdown(f"""
            <div class='{cls_name}'>
                <div class='s-title'>STAGE {snum} {badge}</div>
                <div class='s-desc'>{html.escape(sdata['desc'])}</div>
                <div class='s-meta'>
                    <div class='s-diff'>난이도: {sdata['difficulty']}</div>
                    <div class='s-reward'>해독 보상: {sdata['reward_label']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            btn_label = f"{'🔄 다시 플레이하기' if cleared else '🚀 시스템 접속하기'} (STAGE {snum})" 
            if st.button(btn_label, key=f"stage_btn_{snum}", use_container_width=True):
                init_terminal(snum)
                st.session_state.terminal["output"] = [
                    f"HYOMIN OS v1.0.4 — Secure Shell [Encrypted]",
                    f"Session started: {datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')}",
                    "",
                    f"=== {sdata['title']} ===",
                    f"임무: {sdata['goal']}",
                    "",
                    "도움말이 필요하면 `help` 명령어를 입력하십시오.",
                    "─" * 50,
                ]
                st.session_state.terminal['at_select'] = False
                st.rerun()
        return

    # ── [화면 2] 터미널 게임 화면 ──
    t = st.session_state.terminal
    stage_num  = t["stage"]
    stage_data = STAGES[stage_num]
    fs         = stage_data["filesystem"]

    elapsed = int(time.time() - t["start_time"])
    mins, secs = divmod(elapsed, 60)
    
    # 상단 상태바 (스트림릿 네이티브 활용)
    col_l, col_r = st.columns([4, 1])
    with col_l:
        st.markdown(f"**진행 중인 미션:** STAGE {stage_num} — {stage_data['title']} | ⏱ **{mins:02d}:{secs:02d}**")
    with col_r:
        if st.button("🚪 종료(나가기)", use_container_width=True):
            st.session_state.terminal['at_select'] = True
            st.rerun()

    # 터미널 창 렌더링
    output_html = ""
    for line in t["output"]:
        safe_line = html.escape(line)
        if line.startswith("✅") or line.startswith("  ✅"): css_cls = "green"
        elif line.startswith("❌"): css_cls = "red"
        elif line.startswith("💡"): css_cls = "yellow"
        elif line.startswith("bash:"): css_cls = "red"
        elif line.startswith("="): css_cls = "cyan"
        elif line.startswith("  보상"): css_cls = "yellow"
        elif line.startswith("─") or line.startswith("HYOMIN") or line.startswith("Session"): css_cls = "dim"
        else: css_cls = ""
        
        # ls 명령어의 디렉토리 파란색 살리기
        if "\033[34m" in line:
            safe_line = safe_line.replace("\033[34m", "<span style='color:#3B82F6; font-weight:bold;'>")
            safe_line = safe_line.replace("\033[0m", "</span>")
            
        output_html += f"<div class='t-line {css_cls}'>{safe_line}</div>"

    cwd_disp = html.escape(t["cwd"])
    output_html += (
        f"<div class='t-line'>"
        f"<span class='t-prompt'>guest@hyomin</span><span style='color:#E2E8F0;'>:</span>"
        f"<span class='t-cwd'>{cwd_disp}</span><span style='color:#E2E8F0;'>$ </span>"
        f"<span class='t-cursor'></span>"
        f"</div>"
    )

    st.markdown(f"""
    <div class='terminal-window'>
        <div class='mac-titlebar'>
            <div class='mac-dot red'></div>
            <div class='mac-dot yellow'></div>
            <div class='mac-dot green'></div>
            <div class='mac-title'>Terminal — guest@hyomin — bash — 80x24</div>
        </div>
        <div class='term-body' id='term-scroll'>{output_html}</div>
    </div>
    <script>
        var tb = document.getElementById('term-scroll');
        if(tb) tb.scrollTop = tb.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    # 하단 컨트롤 (입력창 & 버튼)
    if not t["solved"]:
        st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#334155; margin-bottom:5px;'>명령어 입력:</div>", unsafe_allow_html=True)
        cmd_input = st.text_input(
            label="명령어 입력",
            key=f"cmd_input_{t['cmd_count']}",
            placeholder="여기에 명령어를 치고 엔터를 누르세요 (예: ls, cd, cat)",
            label_visibility="collapsed"
        )

        c1, c2, c3 = st.columns([6, 2, 2])
        with c2:
            if st.button("↵ 실행(ENTER)", use_container_width=True, type="primary"):
                if cmd_input and cmd_input.strip():
                    prompt_line = f"guest@hyomin:{t['cwd']}$ {cmd_input}"
                    add_output([prompt_line])
                    result = process_command(cmd_input, stage_data)
                    add_output(result)
                    t["history"].append(cmd_input)
                    st.rerun()
        with c3:
            if st.button("💡 힌트 보기", use_container_width=True):
                add_output([f"guest@hyomin:{t['cwd']}$ hint"])
                result = process_command("hint", stage_data)
                add_output(result)
                st.rerun() 

    else:
        # 클리어 상태 처리
        st.session_state.terminal_cleared.add(stage_num)
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

        st.success(f"🎉 STAGE {stage_num} 클리어! {stage_data['reward_label']} 보상이 지갑으로 입금되었습니다.")

        col_next, col_sel = st.columns(2)
        with col_sel:
            if st.button("목록으로 돌아가기", use_container_width=True):
                st.session_state.terminal['at_select'] = True
                st.rerun()
        with col_next:
            next_stage = stage_num + 1
            if next_stage in STAGES:
                if st.button(f"▶ 다음 스테이지(STAGE {next_stage}) 도전", use_container_width=True, type="primary"):
                    init_terminal(next_stage)
                    st.session_state.terminal["output"] = [
                        f"HYOMIN OS v1.0.4 — Secure Shell [Encrypted]",
                        "",
                        f"=== {STAGES[next_stage]['title']} ===",
                        f"임무: {STAGES[next_stage]['goal']}",
                        "",
                        "─" * 50,
                    ]
                    st.session_state.terminal['at_select'] = False
                    st.rerun()
            else:
                st.info("🏆 축하합니다! 준비된 모든 암호를 해독했습니다.")
