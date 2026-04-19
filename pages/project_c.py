# pages/project_c.py
# 💻 THE TERMINAL — 효민 유니버스 ARG 방탈출 v2.0 [UPGRADED]
import streamlit as st
import time
import base64
import hashlib
import html
import random
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
        "flavor": "낡은 팬 소리가 들린다. 먼지 쌓인 서버. 누군가 여기 있었다...",
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
                    "암호는 labs 시스템 어딘가에 있다고 했다.\n"
                    "ROT13... 오래된 방식이지만 효과적이다."
                )
            },
        },
        "reward": 150_000_000,
        "reward_label": "1억 5천만원",
        "flavor": "형광등이 깜빡인다. 어딘가에서 키보드 소리가 들린다...",
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
        "flavor": "이 방에는 시간이 멈춰있다. 공기마저 숨을 죽이고 있다.",
    },
    4: {
        "title": "STAGE 4 — 블랙마켓 노드",
        "desc":  "다크웹 거래소에서 유출된 지갑 주소의 시드를 복원하라.",
        "difficulty": "⭐⭐⭐⭐ 전문가",
        "goal":  "암호화폐 시드 문구를 찾아 `unlock [시드문구]` 로 입력하라.",
        "answer_hash": hashlib.sha256("MOONCHILD".encode()).hexdigest(),
        "hint_1": "`grep` 명령어로 단서를 찾아라. `grep [검색어] [파일]` 형식으로 사용.",
        "hint_2": "`/node/wallet/` 에서 분산 저장된 키 조각들을 `find` 명령어로 찾아라.",
        "hint_3": "각 키 조각의 첫 글자를 순서대로 이어 붙이면 시드 문구가 된다. (대문자)",
        "filesystem": {
            "/": {"type": "dir"},
            "/node": {"type": "dir"},
            "/node/README": {
                "type": "file",
                "content": (
                    "=== BLACKMARKET NODE v0.9.3 ===\n"
                    "[TOR HIDDEN SERVICE]\n\n"
                    "이 노드는 익명 거래를 위한 중계 서버입니다.\n"
                    "모든 로그는 72시간 후 자동 파기됩니다.\n\n"
                    "wallet/ 디렉토리에 지갑 데이터 존재.\n"
                    "시드는 보안 강화를 위해 분산 저장됨.\n"
                    "find 명령어로 key_fragment 파일을 찾아보라."
                )
            },
            "/node/wallet": {"type": "dir"},
            "/node/wallet/tx_log.txt": {
                "type": "file",
                "content": (
                    "거래 로그\n"
                    "─────────────────────────\n"
                    "TX#001  0.5 BTC  → 0x4f7a..  CONFIRMED\n"
                    "TX#002  1.2 BTC  → 0x9c2b..  CONFIRMED\n"
                    "TX#003  99.0 BTC → 0x????.  PENDING\n"
                    "─────────────────────────\n"
                    "주인: 코드명 'MOONCHILD' 로 알려진 인물\n"
                    "시드는 key_fragment 파일들에 분산 보관"
                )
            },
            "/node/wallet/key_fragment_1.dat": {
                "type": "file",
                "content": "Fragment #1 — [M]ercury system initialized. 시드 첫 번째 조각."
            },
            "/node/wallet/.key_fragment_2.dat": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #2 — [O]mega protocol active. 두 번째 조각."
            },
            "/node/cache": {"type": "dir"},
            "/node/cache/key_fragment_3.tmp": {
                "type": "file",
                "content": "Fragment #3 — [O]rbit confirmed. 세 번째 조각."
            },
            "/node/cache/.key_fragment_4.tmp": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #4 — [N]ode sync complete. 네 번째 조각."
            },
            "/node/backup": {"type": "dir"},
            "/node/backup/key_fragment_5.bak": {
                "type": "file",
                "content": "Fragment #5 — [C]ipher layer 5 engaged. 다섯 번째 조각."
            },
            "/node/backup/.key_fragment_6.bak": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #6 — [H]ash validated. 여섯 번째 조각."
            },
            "/node/backup/key_fragment_7.bak": {
                "type": "file",
                "content": "Fragment #7 — [I]nterface secured. 일곱 번째 조각."
            },
            "/node/backup/key_fragment_8.bak": {
                "type": "file",
                "content": "Fragment #8 — [L]ayer 8 bypass. 여덟 번째 조각."
            },
            "/node/backup/key_fragment_9.bak": {
                "type": "file",
                "content": "Fragment #9 — [D]ead drop activated. 아홉 번째 조각."
            },
            "/home": {"type": "dir"},
            "/home/ghost": {"type": "dir"},
            "/home/ghost/.identity": {
                "type": "file",
                "hidden": True,
                "content": (
                    "나는 달의 아이(MOONCHILD).\n"
                    "어둠 속에서 태어난 자.\n"
                    "내 시드는 9개의 조각으로 나뉘어 있다.\n"
                    "각 파일명에서 [] 안의 대문자가 단서다.\n"
                    "M-O-O-N-C-H-I-L-D"
                )
            },
        },
        "reward": 1_000_000_000,
        "reward_label": "10억원",
        "flavor": "양파 라우터를 타고 들어온 신호. 추적자가 있다. 서둘러라.",
    },
    5: {
        "title": "STAGE 5 — 궤도 위성 해킹",
        "desc":  "효민 코퍼레이션의 감시 위성 시스템에 침투하라. 최종 보스 스테이지.",
        "difficulty": "⭐⭐⭐⭐⭐ 마스터",
        "goal":  "위성 핵심 코드를 해독해 `unlock [코드]` 로 시스템을 장악하라.",
        "answer_hash": hashlib.sha256("HYOMIN_CORP_FALLS".encode()).hexdigest(),
        "hint_1": "`/sat/core/` 를 탐색하라. `whoami` 로 현재 권한을 확인해라.",
        "hint_2": "mission_log 를 읽어라. 코드는 3부분으로 나뉜다: [회사명]_[부서명]_[결말]",
        "hint_3": "형식: `[영문대문자]_[영문대문자]_[영문대문자]` — 언더바로 연결. 힌트: '추락하다'를 영어로.",
        "filesystem": {
            "/": {"type": "dir"},
            "/sat": {"type": "dir"},
            "/sat/SYSTEM_STATUS.txt": {
                "type": "file",
                "content": (
                    "=== HYOMIN-SAT-7 궤도 위성 ===\n"
                    "고도: 550km LEO\n"
                    "상태: 정상 운용 중\n"
                    "운용사: HYOMIN CORP\n"
                    "임무: 전 세계 사용자 감시\n\n"
                    "[경고] 비인가 접근 감지됨\n"
                    "[경고] 자폭 시퀀스 대기 중..."
                )
            },
            "/sat/core": {"type": "dir"},
            "/sat/core/auth.sys": {
                "type": "file",
                "content": (
                    "인증 시스템 v9.1\n"
                    "현재 사용자: GHOST_OPERATOR\n"
                    "권한 레벨: ULTRA\n\n"
                    "최고 권한 획득 완료.\n"
                    "핵심 코드는 mission_log 에서 확인 가능."
                )
            },
            "/sat/core/mission_log.txt": {
                "type": "file",
                "content": (
                    "=== 최종 임무 기록 ===\n\n"
                    "이 위성은 [HYOMIN] 코퍼레이션이 운용 중이다.\n"
                    "감시 부서명: [CORP]\n"
                    "저항 세력의 목표: 이 기업을 [FALLS] — 추락시켜라.\n\n"
                    "세 단어를 언더바(_)로 연결하면 최종 코드가 완성된다.\n"
                    "예시: WORD1_WORD2_WORD3\n\n"
                    "경고: 이 메시지를 읽고 있다면,\n"
                    "당신이 이 싸움의 마지막 희망이다.\n"
                    "-- 레지스탕스"
                )
            },
            "/sat/core/.override_key": {
                "type": "file",
                "hidden": True,
                "content": (
                    "시스템 오버라이드 키 (백업)\n"
                    "HYOMIN_CORP_FALLS\n\n"
                    "이 키로 위성을 무력화할 수 있다.\n"
                    "사용 후 즉시 파기할 것."
                )
            },
            "/home": {"type": "dir"},
            "/home/resistance": {"type": "dir"},
            "/home/resistance/manifesto.txt": {
                "type": "file",
                "content": (
                    "=== 레지스탕스 선언문 ===\n\n"
                    "효민 코퍼레이션은 우리를 감시했다.\n"
                    "우리의 데이터를, 우리의 삶을, 우리의 꿈을.\n\n"
                    "하지만 오늘, 우리가 반격한다.\n"
                    "위성을 무너뜨리고, 자유를 되찾아라.\n\n"
                    "최종 코드는 임무 로그에 숨겨져 있다.\n"
                    "[ ] 안의 단어들이 핵심이다.\n\n"
                    "함께라면 우리는 이길 수 있다.\n"
                    "— The Resistance"
                )
            },
            "/home/resistance/.last_message": {
                "type": "file",
                "hidden": True,
                "content": (
                    "마지막 메시지\n\n"
                    "만약 네가 이걸 읽고 있다면,\n"
                    "나는 이미 붙잡혔을 것이다.\n\n"
                    "코드: HYOMIN_CORP_FALLS\n"
                    "이것으로 모든 것이 끝난다.\n\n"
                    "잊지 마라. 우리는 존재했다.\n"
                    "— Agent 7"
                )
            },
            "/tmp": {"type": "dir"},
            "/tmp/countdown.txt": {
                "type": "file",
                "content": (
                    "자폭 카운트다운\n"
                    "99:59 ... 99:58 ... 99:57 ...\n\n"
                    "서둘러라. 시간이 없다.\n"
                    "unlock 명령어로 위성을 무력화해라!"
                )
            },
        },
        "reward": 5_000_000_000,
        "reward_label": "50억원",
        "flavor": "대기권 밖 550km. 세상 모든 것이 내려다보인다. 끝낼 시간이다.",
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

def find_files(fs, start_path, show_hidden=True):
    """재귀적으로 파일 탐색"""
    results = []
    start = start_path.rstrip('/') or '/'
    for key in sorted(fs.keys()):
        if key == start:
            continue
        if key.startswith(start + '/') or start == '/':
            if start != '/' and not key.startswith(start + '/'):
                continue
            name = key.rsplit('/', 1)[-1]
            if not show_hidden and name.startswith('.'):
                continue
            results.append(key)
    return results

def grep_in_file(content, pattern):
    """파일에서 패턴 검색"""
    lines = content.split('\n')
    matches = []
    for i, line in enumerate(lines, 1):
        if pattern.lower() in line.lower():
            matches.append(f"  {i}: {line}")
    return matches

def build_tree(fs, path, show_hidden=False, prefix="", depth=0):
    """tree 명령어용 디렉토리 구조 생성"""
    if depth > 4:
        return ["  ... (더 깊은 구조 생략)"]
    children = get_dir_children(fs, path)
    lines = []
    visible = [(n, info) for n, info in sorted(children)
               if show_hidden or not info.get("hidden", False)]
    for i, (name, info) in enumerate(visible):
        is_last = (i == len(visible) - 1)
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        if info["type"] == "dir":
            lines.append(f"{prefix}{connector}{name}/")
            child_path = (path.rstrip('/') + '/' + name) if path != '/' else ('/' + name)
            lines.extend(build_tree(fs, child_path, show_hidden, prefix + extension, depth + 1))
        else:
            hidden_mark = " [숨김]" if info.get("hidden") else ""
            lines.append(f"{prefix}{connector}{name}{hidden_mark}")
    return lines

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
        "at_select":   False,
    }

def add_output(lines):
    t = st.session_state.terminal
    for line in lines:
        t["output"].append(line)
    if len(t["output"]) > 300:
        t["output"] = t["output"][-300:]

def process_command(cmd_raw, stage_data):
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
                out.append(f"[DIR] {name}/")
            else:
                out.append(name)
        return out if out else ["(표시할 항목 없음 — `-a` 옵션으로 숨김 파일 확인)"]

    # ── cd ───────────────────────────────────────
    elif cmd == "cd":
        target = args.strip() or "/"
        new_path = resolve_path(cwd, target)
        if new_path in fs and fs[new_path]["type"] == "dir":
            t["cwd"] = new_path
            return []
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

    # ── whoami ──────────────────────────────────
    elif cmd == "whoami":
        return [
            "ghost_operator",
            "uid=1337(ghost) gid=1337(shadow) groups=1337(shadow),0(root)",
            "권한: ULTRA — 모든 시스템 접근 가능",
        ]

    # ── echo ─────────────────────────────────────
    elif cmd == "echo":
        return [args if args else ""]

    # ── grep ─────────────────────────────────────
    elif cmd == "grep":
        # grep [패턴] [파일]
        grep_parts = args.strip().split(None, 1)
        if len(grep_parts) < 2:
            return ["사용법: grep [검색어] [파일]"]
        pattern, filename = grep_parts[0], grep_parts[1]
        target = resolve_path(cwd, filename.strip())
        if target not in fs:
            return [f"grep: {filename}: No such file or directory"]
        if fs[target]["type"] == "dir":
            return [f"grep: {filename}: Is a directory"]
        matches = grep_in_file(fs[target]["content"], pattern)
        if not matches:
            return [f"('{pattern}' 에 해당하는 내용 없음)"]
        return [f"검색 결과 '{pattern}' in {filename}:"] + matches

    # ── find ─────────────────────────────────────
    elif cmd == "find":
        # find [경로] [-name 패턴]
        find_args = args.strip().split() if args else ["."]
        search_path = cwd
        name_filter = None
        show_all = False

        i = 0
        while i < len(find_args):
            if find_args[i] == "-name" and i + 1 < len(find_args):
                name_filter = find_args[i+1].replace("*","")
                i += 2
            elif find_args[i] == "-a":
                show_all = True
                i += 1
            else:
                p = resolve_path(cwd, find_args[i])
                if p in fs:
                    search_path = p
                i += 1

        results = []
        for key in sorted(fs.keys()):
            fname = key.rsplit('/', 1)[-1]
            is_hidden = fs[key].get("hidden", False)
            if not show_all and is_hidden:
                continue
            if name_filter and name_filter not in fname:
                continue
            # 검색 경로 하위인지 확인
            if search_path == '/':
                results.append(key)
            elif key.startswith(search_path + '/') or key == search_path:
                results.append(key)

        if not results:
            return ["(검색 결과 없음)"]
        out = [f"find 결과 ({len(results)}개):"]
        out.extend(results)
        return out

    # ── tree ─────────────────────────────────────
    elif cmd == "tree":
        show_hidden = "-a" in args
        lines = [cwd]
        lines.extend(build_tree(fs, cwd, show_hidden))
        return lines

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
        return [f"[HINT] 힌트 {used+1}: {available[used]}",
                f"       (남은 힌트: {len(available) - t['hint_used']}개)"]

    # ── unlock ───────────────────────────────────
    elif cmd == "unlock":
        answer = args.strip()
        expected_hash = stage_data["answer_hash"]
        if hashlib.sha256(answer.encode()).hexdigest() == expected_hash:
            t["solved"] = True
            elapsed = int(time.time() - t["start_time"])
            mins, secs = divmod(elapsed, 60)
            stars = "⭐" * (5 - t["hint_used"])
            return [
                "╔══════════════════════════════════════════╗",
                "║          ACCESS GRANTED ✅               ║",
                "╚══════════════════════════════════════════╝",
                "",
                f"  클리어 시간:  {mins:02d}분 {secs:02d}초",
                f"  명령어 수:    {t['cmd_count']}개",
                f"  힌트 사용:    {t['hint_used']}개",
                f"  평가:         {stars if stars else '힌트 남용'}",
                f"  보상:         {stage_data['reward_label']}",
                "",
                "  다음 스테이지로 진행할 수 있습니다.",
                "═" * 44,
            ]
        else:
            return [
                "╔═══════════════════════════════════╗",
                "║   ACCESS DENIED ❌  비밀번호 오류  ║",
                "╚═══════════════════════════════════╝",
                "  다시 시도하거나 `hint` 를 사용하라.",
            ]

    # ── clear ────────────────────────────────────
    elif cmd == "clear":
        t["output"] = []
        return []

    # ── man / help ───────────────────────────────
    elif cmd in ("help", "man"):
        return [
            "╔══ HYOMIN SHELL — 명령어 매뉴얼 ══════════════╗",
            "║  ls [-a]        파일 목록 (숨김 파일 포함)   ║",
            "║  cd [경로]      디렉토리 이동               ║",
            "║  cat [파일]     파일 내용 출력              ║",
            "║  pwd            현재 경로                   ║",
            "║  whoami         현재 사용자 정보             ║",
            "║  echo [텍스트]  텍스트 출력                 ║",
            "║  find [-name]   파일 검색                   ║",
            "║  grep [패턴] [파일]  내용 검색              ║",
            "║  tree [-a]      디렉토리 구조 시각화         ║",
            "║  decode [b64]   base64 디코딩               ║",
            "║  rot13 [str]    ROT13 암복호화              ║",
            "║  hint           힌트 (최대 3개)              ║",
            "║  unlock [pw]    잠금 해제 시도              ║",
            "║  clear          화면 지우기                 ║",
            "╚═══════════════════════════════════════════════╝",
            "  ↑↓ 방향키: 명령어 히스토리 탐색",
        ]

    # ── 알 수 없는 명령어 ─────────────────────────
    else:
        return [
            f"bash: {cmd}: command not found",
            "  `help` 로 사용 가능한 명령어 확인",
        ]


# ══════════════════════════════════════════════════════════
#  CSS / JS 스타일
# ══════════════════════════════════════════════════════════

TERMINAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,700;1,400&family=Share+Tech+Mono&display=swap');

/* 전체 터미널 컨테이너 */
.terminal-outer {
    background: #020c02;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(0,255,65,0.15), 0 24px 80px rgba(0,0,0,0.8);
    font-family: 'JetBrains Mono', 'Share Tech Mono', monospace;
    margin: 0 0 16px 0;
    border: 1px solid #0f3a0f;
    position: relative;
}

/* 스캔라인 오버레이 */
.terminal-outer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.03) 2px,
        rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 10;
}

/* 상단 타이틀바 */
.term-titlebar {
    background: #0a1a0a;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #1a3a1a;
}
.dot { width:12px; height:12px; border-radius:50%; box-shadow: 0 0 6px; }
.dot-r { background:#ff5f57; box-shadow: 0 0 6px #ff5f57; }
.dot-y { background:#febc2e; box-shadow: 0 0 6px #febc2e; }
.dot-g { background:#28c840; box-shadow: 0 0 6px #28c840; }
.term-title { color: #3fb950; font-size:12px; margin-left:8px; letter-spacing: 1px; }

/* 출력 영역 */
.term-body {
    background: #020c02;
    padding: 16px 20px;
    min-height: 360px;
    max-height: 480px;
    overflow-y: auto;
    font-size: 13px;
    line-height: 1.7;
    scrollbar-width: thin;
    scrollbar-color: #1a3a1a #020c02;
}
.term-body::-webkit-scrollbar { width: 6px; }
.term-body::-webkit-scrollbar-track { background: #020c02; }
.term-body::-webkit-scrollbar-thumb { background: #1a3a1a; border-radius: 3px; }

/* 텍스트 색상 */
.term-line { color: #b8ffb8; white-space: pre-wrap; word-break: break-all; margin: 0; }
.term-line.green  { color: #39ff14; text-shadow: 0 0 8px rgba(57,255,20,0.4); }
.term-line.yellow { color: #ffd700; text-shadow: 0 0 8px rgba(255,215,0,0.3); }
.term-line.red    { color: #ff3333; text-shadow: 0 0 8px rgba(255,51,51,0.4); }
.term-line.blue   { color: #00bfff; }
.term-line.cyan   { color: #00ffff; text-shadow: 0 0 8px rgba(0,255,255,0.3); }
.term-line.dim    { color: #2a5c2a; }
.term-line.dir    { color: #00bfff; font-weight: bold; }
.term-line.hint   { color: #ffd700; background: rgba(255,215,0,0.05); padding: 2px 4px; border-left: 2px solid #ffd700; }
.term-line.prompt { color: #b8ffb8; }
.term-line.border { color: #39ff14; text-shadow: 0 0 4px rgba(57,255,20,0.2); }

/* 프롬프트 */
.term-prompt-user { color: #39ff14; font-weight: bold; }
.term-prompt-host { color: #00bfff; }
.term-prompt-sep  { color: #b8ffb8; }
.term-prompt-path { color: #ffd700; }
.term-prompt-sym  { color: #ff3333; }

/* 커서 깜빡임 */
.blink-cursor {
    display: inline-block;
    width: 9px; height: 16px;
    background: #39ff14;
    animation: blink 1s step-end infinite;
    vertical-align: middle;
    margin-left: 2px;
    box-shadow: 0 0 8px rgba(57,255,20,0.8);
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

/* 글리치 텍스트 */
@keyframes glitch1 {
    0%,100% { clip-path: inset(0 0 95% 0); transform: translate(-2px); }
    20% { clip-path: inset(30% 0 50% 0); transform: translate(2px); }
    40% { clip-path: inset(70% 0 10% 0); transform: translate(-1px); }
}
@keyframes glitch2 {
    0%,100% { clip-path: inset(80% 0 0 0); transform: translate(2px); }
    30% { clip-path: inset(10% 0 70% 0); transform: translate(-2px); }
    60% { clip-path: inset(50% 0 30% 0); transform: translate(1px); }
}
.glitch-text {
    position: relative;
    color: #39ff14;
    font-weight: 700;
    letter-spacing: 3px;
    text-shadow: 0 0 20px rgba(57,255,20,0.6);
}
.glitch-text::before,
.glitch-text::after {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    width: 100%;
}
.glitch-text::before {
    color: #ff003c;
    animation: glitch1 3s infinite linear alternate;
    opacity: 0.6;
}
.glitch-text::after {
    color: #00ffff;
    animation: glitch2 2s infinite linear alternate;
    opacity: 0.6;
}

/* 스테이지 카드 */
.stage-card {
    background: linear-gradient(135deg, #020c02 0%, #041804 100%);
    border: 1px solid #0f3a0f;
    border-radius: 8px;
    padding: 18px 22px;
    margin-bottom: 10px;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.stage-card::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #39ff14, transparent);
    animation: scan 4s linear infinite;
}
@keyframes scan {
    0% { left: -100%; }
    100% { left: 100%; }
}
.stage-card:hover {
    border-color: #39ff14;
    box-shadow: 0 0 20px rgba(57,255,20,0.2), inset 0 0 20px rgba(57,255,20,0.02);
}
.stage-title { color: #39ff14; font-size: 1rem; font-weight: 700; margin-bottom: 6px; }
.stage-desc  { color: #5a9a5a; font-size: 0.83rem; margin: 4px 0 10px; }
.stage-meta  { color: #2a5c2a; font-size: 0.8rem; }
.stage-reward { color: #ffd700; font-size: 0.85rem; }
.clear-badge {
    background: rgba(57,255,20,0.1);
    border: 1px solid #39ff14;
    color: #39ff14;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 0.72rem;
    font-weight: 700;
    float: right;
    text-shadow: 0 0 8px rgba(57,255,20,0.4);
}

/* 플레이버 텍스트 */
.flavor-text {
    color: #2a6a2a;
    font-style: italic;
    font-size: 0.78rem;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid #0f2a0f;
}

/* 상태바 */
.status-bar {
    background: #030f03;
    border: 1px solid #0f3a0f;
    border-radius: 6px;
    padding: 8px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    display: flex;
    gap: 16px;
    align-items: center;
    margin-bottom: 8px;
}
.status-item { color: #5a9a5a; }
.status-val  { color: #39ff14; font-weight: bold; }
.status-warn { color: #ff3333; animation: pulse 1s ease-in-out infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
</style>
"""

# ── 자바스크립트 (키보드 단축키 + 히스토리 + 자동스크롤 + 효과음) ──
TERMINAL_JS = """
<script>
(function() {
  // 자동 스크롤
  var tb = document.getElementById('term-scroll');
  if(tb) tb.scrollTop = tb.scrollHeight;

  // Web Audio 효과음
  var AudioCtx = window.AudioContext || window.webkitAudioContext;
  var ctx = AudioCtx ? new AudioCtx() : null;

  function beep(freq, dur, type, vol) {
    if (!ctx) return;
    try {
      var osc = ctx.createOscillator();
      var gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.frequency.value = freq;
      osc.type = type || 'square';
      gain.gain.setValueAtTime(vol || 0.04, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + dur);
    } catch(e) {}
  }

  // 입력창에 포커스 + 키 이벤트
  setTimeout(function() {
    var inputs = document.querySelectorAll('input[type="text"]');
    if (inputs.length > 0) {
      var inp = inputs[inputs.length - 1];
      inp.focus();
      inp.style.color = '#39ff14';
      inp.style.caretColor = '#39ff14';

      // Enter 키로 제출
      inp.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          beep(880, 0.05, 'square', 0.03);
          var btns = document.querySelectorAll('button');
          for (var b of btns) {
            if (b.innerText.includes('ENTER') || b.innerText.trim() === '실행') {
              b.click();
              break;
            }
          }
        }
        if (e.key === 'l' && e.ctrlKey) {
          e.preventDefault();
          var btns = document.querySelectorAll('button');
          for (var b of btns) {
            if (b.innerText.includes('CLEAR')) { b.click(); break; }
          }
        }
      });

      // 타이핑 효과음
      inp.addEventListener('input', function() {
        beep(600 + Math.random()*200, 0.02, 'square', 0.015);
      });
    }
  }, 400);

  // 입력창 스타일 강제 적용
  setTimeout(function() {
    var style = document.createElement('style');
    style.textContent = `
      input[type="text"] {
        background: #020c02 !important;
        color: #39ff14 !important;
        border: 1px solid #1a4a1a !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
        caret-color: #39ff14 !important;
      }
      input[type="text"]:focus {
        border-color: #39ff14 !important;
        box-shadow: 0 0 12px rgba(57,255,20,0.2) !important;
        outline: none !important;
      }
      input[type="text"]::placeholder {
        color: #1a4a1a !important;
      }
      .stTextInput > div > div {
        background: transparent !important;
      }
      .stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        background: #020c02 !important;
        color: #39ff14 !important;
        border: 1px solid #1a4a1a !important;
        border-radius: 4px !important;
        font-size: 12px !important;
        transition: all 0.15s !important;
      }
      .stButton > button:hover {
        background: #0a2a0a !important;
        border-color: #39ff14 !important;
        box-shadow: 0 0 10px rgba(57,255,20,0.2) !important;
        color: #ffffff !important;
      }
      .stButton > button[kind="primary"] {
        background: #0f3a0f !important;
        color: #39ff14 !important;
        border-color: #39ff14 !important;
      }
    `;
    document.head.appendChild(style);
  }, 200);
})();
</script>
"""


# ══════════════════════════════════════════════════════════
#  매트릭스 빗줄기 배경 (선택 화면용)
# ══════════════════════════════════════════════════════════
MATRIX_RAIN_HTML = """
<canvas id="matrix-canvas" style="
  position:fixed; top:0; left:0; width:100%; height:100%;
  z-index:-1; pointer-events:none; opacity:0.06;
"></canvas>
<script>
(function(){
  var c = document.getElementById('matrix-canvas');
  if(!c) return;
  var ctx = c.getContext('2d');
  c.width = window.innerWidth;
  c.height = window.innerHeight;
  var cols = Math.floor(c.width / 18);
  var drops = Array(cols).fill(1);
  var chars = '01アイウエオカキクケコサシスセソHYOMIN효민UNIVERSE';
  function draw() {
    ctx.fillStyle = 'rgba(0,0,0,0.05)';
    ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle = '#39ff14';
    ctx.font = '13px "JetBrains Mono", monospace';
    for(var i=0; i<drops.length; i++){
      var ch = chars[Math.floor(Math.random()*chars.length)];
      ctx.fillText(ch, i*18, drops[i]*18);
      if(drops[i]*18 > c.height && Math.random() > 0.975) drops[i] = 0;
      drops[i]++;
    }
  }
  setInterval(draw, 55);
})();
</script>
"""


# ══════════════════════════════════════════════════════════
#  메인 렌더 함수
# ══════════════════════════════════════════════════════════

def render():
    # 전체 배경 다크
    st.markdown("""
    <style>
    .stApp { background-color: #010409 !important; }
    section[data-testid="stSidebar"] { background: #010409 !important; }
    .stMarkdown, .stMarkdown * { font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(TERMINAL_CSS, unsafe_allow_html=True)

    uid = st.session_state.get('logged_in_user', '')

    if 'terminal_cleared' not in st.session_state:
        st.session_state.terminal_cleared = set()

    # ── 스테이지 선택 화면 ───────────────────────
    if 'terminal' not in st.session_state or \
       st.session_state.terminal.get('at_select', False):

        st.markdown(MATRIX_RAIN_HTML, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-family:"JetBrains Mono",monospace; padding: 28px 0 12px; text-align:center;'>
          <div class='glitch-text' data-text='&gt;_ THE TERMINAL 방탈출'
               style='font-size:2rem; display:inline-block; margin-bottom:8px;'>
            &gt;_ THE TERMINAL 방탈출
          </div>
          <div style='color:#3a6a3a; font-size:0.88rem; margin-top:10px; letter-spacing:2px;'>
            효민 유니버스 ARG · 방탈출 · 해킹 시뮬레이터
          </div>
          <div style='color:#1a3a1a; font-size:0.75rem; margin-top:6px;'>
            마우스는 잊어라 — 오직 커맨드라인으로만 진실에 접근할 수 있다
          </div>
        </div>
        """, unsafe_allow_html=True)

        # 전체 클리어 수
        cleared_count = len(st.session_state.terminal_cleared)
        total_stages  = len(STAGES)
        total_reward  = sum(STAGES[s]["reward"] for s in st.session_state.terminal_cleared)

        if cleared_count > 0:
            st.markdown(f"""
            <div style='background:#030f03; border:1px solid #1a3a1a; border-radius:6px;
                        padding:10px 18px; font-family:monospace; font-size:12px;
                        color:#5a9a5a; margin-bottom:16px; text-align:center;'>
              진행: {cleared_count}/{total_stages} 스테이지 클리어 &nbsp;|&nbsp;
              총 획득: <span style='color:#ffd700;'>₩{total_reward:,}</span>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        for snum, sdata in STAGES.items():
            cleared = snum in st.session_state.terminal_cleared
            locked  = snum > 1 and (snum - 1) not in st.session_state.terminal_cleared

            badge = "<span class='clear-badge'>✅ CLEARED</span>" if cleared else ""
            lock_icon = "🔒 " if locked else ""

            diff_color = ["", "#39ff14", "#7aff4a", "#ffd700", "#ff8c00", "#ff3333"][snum]

            st.markdown(f"""
            <div class='stage-card' style='{"opacity:0.45;" if locked else ""}'>
              <div class='stage-title'>{badge}{lock_icon}{html.escape(sdata['title'])}</div>
              <div class='stage-desc'>{html.escape(sdata['desc'])}</div>
              <div class='stage-meta'>
                <span style='color:{diff_color};'>{sdata['difficulty']}</span>
                &nbsp;&nbsp;
                <span class='stage-reward'>💰 {sdata['reward_label']}</span>
              </div>
              <div class='flavor-text'>{html.escape(sdata.get('flavor',''))}</div>
            </div>
            """, unsafe_allow_html=True)

            btn_label = (
                f"[REPLAY] STAGE {snum} 다시하기" if cleared else
                f"[LOCKED] STAGE {snum - 1} 클리어 후 해금" if locked else
                f"[ENTER]  STAGE {snum} 시작하기"
            )
            if st.button(btn_label, key=f"stage_btn_{snum}",
                         use_container_width=True, disabled=locked):
                init_terminal(snum)
                boot_msg = [
                    "HYOMIN NETWORKS — Secure Shell v2.26.0",
                    f"Last login: {datetime.now(KST).strftime('%a %b %d %H:%M:%S KST %Y')}",
                    "Connecting to hyomin-secure-node...",
                    "Connection established. ✓",
                    "",
                    "╔══════════════════════════════════════════╗",
                    f"║  {sdata['title']:<40}║",
                    "╚══════════════════════════════════════════╝",
                    "",
                    f"  📋 목표: {sdata['goal']}",
                    f"  ⚠️  {sdata.get('flavor', '')}",
                    "",
                    "  `help` — 명령어 목록   `hint` — 힌트 보기",
                    "─" * 44,
                ]
                st.session_state.terminal["output"] = boot_msg
                st.session_state.terminal['at_select'] = False
                st.rerun()

        st.markdown(TERMINAL_JS, unsafe_allow_html=True)
        return

    # ── 터미널 게임 화면 ─────────────────────────
    t = st.session_state.terminal
    stage_num  = t["stage"]
    stage_data = STAGES[stage_num]

    # 상단 상태바
    elapsed = int(time.time() - t["start_time"])
    mins, secs = divmod(elapsed, 60)
    hint_warn = t["hint_used"] >= 3

    col_l, col_r = st.columns([4, 1])
    with col_l:
        st.markdown(
            f"<div class='status-bar'>"
            f"<span class='status-item'>⏱ <span class='status-val'>{mins:02d}:{secs:02d}</span></span>"
            f"<span class='status-item'>CMD <span class='status-val'>{t['cmd_count']}</span></span>"
            f"<span class='status-item'>HINT <span class='{'status-warn' if hint_warn else 'status-val'}'>{t['hint_used']}/3</span></span>"
            f"<span class='status-item' style='color:#ffd700;'>{stage_data['title']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_r:
        if st.button("◀ 목록", use_container_width=True, key="back_btn"):
            st.session_state.terminal['at_select'] = True
            st.rerun()

    # ── 터미널 출력 렌더링 ─────────────────────────
    output_html = ""
    for line in t["output"]:
        safe = html.escape(line)

        # 색상 클래스 결정
        if any(line.startswith(p) for p in ["✅", "  ✅", "  클리어", "  명령어", "  힌트 사용", "  평가", "  보상", "  다음"]):
            cls = "green"
        elif any(line.startswith(p) for p in ["❌", "╔══", "╚══", "║  ACCESS DENIED", "║   ACCESS DENIED"]):
            cls = "red"
        elif line.startswith("[HINT]") or line.startswith("       "):
            cls = "hint"
        elif line.startswith("bash:"):
            cls = "red"
        elif any(line.startswith(p) for p in ["╔", "╚", "║", "═", "  ╔", "  ╚", "  ║"]):
            cls = "cyan" if "GRANTED" in line or "ACCESS" in line else "border"
        elif line.startswith("  보상") or line.startswith("  💰"):
            cls = "yellow"
        elif line.startswith("─") or line.startswith("HYOMIN NETWORKS") or line.startswith("Last login") or line.startswith("Connecting"):
            cls = "dim"
        elif line.startswith("[DIR]"):
            safe = html.escape(line[6:]) if line.startswith("[DIR] ") else safe
            cls = "dir"
            safe = f"📁 {html.escape(line[6:])}" if line.startswith("[DIR] ") else safe
        elif "Connection established" in line:
            cls = "green"
        elif line.startswith("  📋") or line.startswith("  ⚠️") or line.startswith("  `"):
            cls = "blue"
        elif line.startswith("find 결과") or line.startswith("검색 결과"):
            cls = "cyan"
        else:
            cls = ""

        output_html += f"<div class='term-line {cls}'>{safe}</div>"

    # 현재 프롬프트
    cwd_disp = t["cwd"]
    output_html += (
        f"<div class='term-line prompt'>"
        f"<span class='term-prompt-user'>ghost@hyomin</span>"
        f"<span class='term-prompt-sep'>:</span>"
        f"<span class='term-prompt-path'>{html.escape(cwd_disp)}</span>"
        f"<span class='term-prompt-sym'># </span>"
        f"<span class='blink-cursor'></span>"
        f"</div>"
    )

    st.markdown(f"""
    <div class='terminal-outer'>
      <div class='term-titlebar'>
        <div class='dot dot-r'></div>
        <div class='dot dot-y'></div>
        <div class='dot dot-g'></div>
        <div class='term-title'>ghost@hyomin-secure — {html.escape(cwd_disp)} — STAGE {stage_num}</div>
      </div>
      <div class='term-body' id='term-scroll'>{output_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 입력창 (클리어 전) ──────────────────────
    if not t["solved"]:
        cmd_input = st.text_input(
            label="cmd",
            key=f"cmd_input_{t['cmd_count']}",
            placeholder="$ 명령어 입력 후 Enter ↵  (도움말: help)",
            label_visibility="collapsed",
        )

        col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
        with col2:
            enter_clicked = st.button("ENTER ↵", use_container_width=True,
                                       type="primary", key="enter_btn")
        with col3:
            hint_clicked = st.button("💡 HINT", use_container_width=True,
                                      key="hint_btn")
        with col4:
            if st.button("CLR", use_container_width=True, key="clear_btn"):
                t["output"] = []
                st.rerun()

        if enter_clicked and cmd_input and cmd_input.strip():
            cwd_prompt = t["cwd"]
            prompt_line = f"ghost@hyomin:{cwd_prompt}# {cmd_input}"
            add_output([prompt_line])
            result = process_command(cmd_input, stage_data)
            add_output(result)
            t["history"].append(cmd_input)
            st.rerun()

        if hint_clicked:
            add_output([f"ghost@hyomin:{t['cwd']}# hint"])
            result = process_command("hint", stage_data)
            add_output(result)
            st.rerun()

    else:
        # ── 클리어 화면 ──────────────────────────
        st.session_state.terminal_cleared.add(stage_num)

        reward_key = f"terminal_reward_{stage_num}"
        if reward_key not in st.session_state:
            st.session_state[reward_key] = True
            reward = stage_data["reward"]
            st.session_state.global_cash = st.session_state.get('global_cash', 0) + reward
            try:
                from utils.core import sync_user_data
                from utils.database import log_tx
                sync_user_data()
                log_tx(uid, "터미널", f"THE TERMINAL Stage {stage_num} 클리어", reward)
            except Exception:
                pass
            st.balloons()

        st.markdown(f"""
        <div style='
          background: linear-gradient(135deg, #020c02, #041804);
          border: 1px solid #39ff14;
          border-radius: 8px;
          padding: 20px 24px;
          font-family: "JetBrains Mono", monospace;
          text-align: center;
          box-shadow: 0 0 30px rgba(57,255,20,0.2);
          margin-bottom: 12px;
        '>
          <div style='color:#39ff14; font-size:1.5rem; font-weight:700; letter-spacing:3px;
                      text-shadow: 0 0 20px rgba(57,255,20,0.6);'>
            ✅ STAGE {stage_num} CLEAR
          </div>
          <div style='color:#ffd700; font-size:1.1rem; margin-top:8px;'>
            보상 획득: {stage_data['reward_label']}
          </div>
          <div style='color:#5a9a5a; font-size:0.82rem; margin-top:6px;'>
            사용 힌트: {t['hint_used']}개 &nbsp;|&nbsp; 명령어: {t['cmd_count']}개
          </div>
        </div>
        """, unsafe_allow_html=True)

        col_sel, col_next = st.columns(2)
        with col_sel:
            if st.button("◀ 스테이지 목록", use_container_width=True, key="to_list"):
                st.session_state.terminal['at_select'] = True
                st.rerun()
        with col_next:
            next_s = stage_num + 1
            if next_s in STAGES:
                if st.button(f"▶ STAGE {next_s} 도전 →",
                              use_container_width=True, type="primary", key="next_stage"):
                    init_terminal(next_s)
                    ns = STAGES[next_s]
                    st.session_state.terminal["output"] = [
                        "HYOMIN NETWORKS — Secure Shell v2.26.0",
                        f"Last login: {datetime.now(KST).strftime('%a %b %d %H:%M:%S KST %Y')}",
                        "Connecting...",
                        "",
                        "╔══════════════════════════════════════════╗",
                        f"║  {ns['title']:<40}║",
                        "╚══════════════════════════════════════════╝",
                        "",
                        f"  📋 목표: {ns['goal']}",
                        f"  ⚠️  {ns.get('flavor', '')}",
                        "",
                        "  `help` 명령어 목록   `hint` 힌트 보기",
                        "─" * 44,
                    ]
                    st.session_state.terminal['at_select'] = False
                    st.rerun()
            else:
                st.markdown("""
                <div style='color:#ffd700; font-family:monospace; text-align:center;
                            padding:12px; border:1px solid #ffd700; border-radius:6px;'>
                  🏆 모든 스테이지 정복! 당신이 효민 유니버스의 흑막이다.
                </div>
                """, unsafe_allow_html=True)

    # JS는 항상 마지막에
    st.markdown(TERMINAL_JS, unsafe_allow_html=True)
