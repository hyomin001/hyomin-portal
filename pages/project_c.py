# pages/project_c.py
# 💻 THE TERMINAL — 방탈출 v4.0 [14 STAGES]
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
    # ─────────────────────────────────────────────────────
    1: {
        "title":      "STAGE 1 — 버려진 서버실",
        "desc":       "낡은 서버에서 관리자 비밀번호를 찾아라.",
        "difficulty": "⭐ 입문",
        "goal":       "비밀번호를 찾아 `unlock [비밀번호]` 명령어로 잠금을 해제하라.",
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
                ),
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
                    "2026-01-03 09:12:44  LOGIN  admin    SUCCESS\n"
                    "2026-01-03 11:55:02  LOGIN  unknown  FAIL\n"
                    "2026-01-03 11:55:18  LOGIN  unknown  FAIL\n"
                    "2026-01-04 03:22:11  LOGIN  ???      SUCCESS  [비정상 접근]\n"
                ),
            },
        },
        "flavor": "낡은 팬 소리가 들린다. 먼지 쌓인 서버. 누군가 여기 있었다...",
    },

    # ─────────────────────────────────────────────────────
    2: {
        "title":      "STAGE 2 — 지하 연구소",
        "desc":       "연구소 데이터베이스에서 프로젝트 코드명을 해독하라.",
        "difficulty": "⭐⭐ 보통",
        "goal":       "암호화된 프로젝트 코드명을 찾아 `unlock [코드명]` 으로 입력하라.",
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
                ),
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
                ),
            },
            "/lab/classified/cipher.txt": {
                "type": "file",
                "content": (
                    "== ROT13 암호화 ==\n"
                    "QBCNULBZVA\n\n"
                    "이 코드명은 절대 외부에 유출되어선 안 됩니다.\n"
                    "-- Dr.K"
                ),
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
                ),
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
                ),
            },
        },
        "flavor": "형광등이 깜빡인다. 어딘가에서 키보드 소리가 들린다...",
    },

    # ─────────────────────────────────────────────────────
    3: {
        "title":      "STAGE 3 — 효민의 금고",
        "desc":       "창조자가 남긴 최후의 비밀을 해독하라.",
        "difficulty": "⭐⭐⭐ 어려움",
        "goal":       "금고의 최종 패스프레이즈를 찾아 `unlock [패스프레이즈]` 로 입력하라.",
        "answer_hash": hashlib.sha256("UNIVERSE_ORIGIN_01".encode()).hexdigest(),
        "hint_1": "여러 파일의 단서를 조합해야 한다. `/vault` 와 `/archive` 를 모두 탐색하라.",
        "hint_2": "fragment_*.txt 파일들을 순서대로 모으면 패스프레이즈가 완성된다.",
        "hint_3": "패스프레이즈 형식: `[단어]_[단어]_[숫자두자리]` — 언더바(_)로 연결.",
        "filesystem": {
            "/": {"type": "dir"},
            "/vault": {"type": "dir"},
            "/vault/lock_info.txt": {
                "type": "file",
                "content": (
                    "=== 금고 잠금 시스템 v3 ===\n\n"
                    "패스프레이즈는 3개의 조각으로 나뉘어 숨겨져 있습니다.\n"
                    "각 조각은 시스템 곳곳에 분산되어 있습니다.\n\n"
                    "힌트: 조각들은 fragment_1, fragment_2, fragment_3 파일에 있습니다.\n"
                    "완성된 패스프레이즈: [조각1]_[조각2]_[조각3]\n"
                    "(모두 대문자, 세 번째는 숫자 두 자리)"
                ),
            },
            "/vault/.fragment_1": {
                "type": "file",
                "hidden": True,
                "content": "조각 1/3: UNIVERSE",
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
                ),
            },
            "/archive/fragment_2.txt": {
                "type": "file",
                "content": "조각 2/3: ORIGIN",
            },
            "/archive/old_logs/.hidden_record": {
                "type": "file",
                "hidden": True,
                "content": (
                    "== 창조 기록 ==\n"
                    "이 세계는 2026년 1월 1일에 시작됐다.\n"
                    "창조자는 그 날짜를 기억하길 원한다.\n"
                    "마지막 조각은 /tmp 에 있다."
                ),
            },
            "/tmp": {"type": "dir"},
            "/tmp/fragment_3.txt": {
                "type": "file",
                "content": "조각 3/3: 01 (창조의 달, 01월)",
            },
            "/tmp/.creator_note": {
                "type": "file",
                "hidden": True,
                "content": (
                    "만약 여기까지 왔다면,\n"
                    "당신은 이 세계의 숨겨진 진실을 알 자격이 있다.\n\n"
                    "이 게임은 단순한 퍼즐이 아니다.\n"
                    "마지막 문을 열어라.\n"
                    "— 창조자"
                ),
            },
        },
        "flavor": "이 방에는 시간이 멈춰있다. 공기마저 숨을 죽이고 있다.",
    },

    # ─────────────────────────────────────────────────────
    4: {
        "title":      "STAGE 4 — 블랙마켓 노드",
        "desc":       "다크웹 거래소에서 유출된 지갑의 시드를 복원하라.",
        "difficulty": "⭐⭐⭐⭐ 전문가",
        "goal":       "암호화폐 시드 문구를 찾아 `unlock [시드문구]` 로 입력하라.",
        "answer_hash": hashlib.sha256("MOONCHILD".encode()).hexdigest(),
        "hint_1": "`grep` 명령어로 단서를 찾아라. `grep [검색어] [파일]` 형식으로 사용.",
        "hint_2": "`/node/wallet/` 에서 분산 저장된 키 조각들을 `find` 명령어로 찾아라.",
        "hint_3": "각 키 조각의 `[ ]` 안 대문자를 순서대로 이어 붙이면 시드 문구가 된다.",
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
                ),
            },
            "/node/wallet": {"type": "dir"},
            "/node/wallet/tx_log.txt": {
                "type": "file",
                "content": (
                    "거래 로그\n"
                    "─────────────────────────\n"
                    "TX#001  0.5 BTC  → 0x4f7a..  CONFIRMED\n"
                    "TX#002  1.2 BTC  → 0x9c2b..  CONFIRMED\n"
                    "TX#003  99.0 BTC → 0x????.   PENDING\n"
                    "─────────────────────────\n"
                    "주인: 코드명 'MOONCHILD' 로 알려진 인물\n"
                    "시드는 key_fragment 파일들에 분산 보관"
                ),
            },
            "/node/wallet/key_fragment_1.dat": {
                "type": "file",
                "content": "Fragment #1 — [M]ercury system initialized. 시드 첫 번째 조각.",
            },
            "/node/wallet/.key_fragment_2.dat": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #2 — [O]mega protocol active. 두 번째 조각.",
            },
            "/node/cache": {"type": "dir"},
            "/node/cache/key_fragment_3.tmp": {
                "type": "file",
                "content": "Fragment #3 — [O]rbit confirmed. 세 번째 조각.",
            },
            "/node/cache/.key_fragment_4.tmp": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #4 — [N]ode sync complete. 네 번째 조각.",
            },
            "/node/backup": {"type": "dir"},
            "/node/backup/key_fragment_5.bak": {
                "type": "file",
                "content": "Fragment #5 — [C]ipher layer 5 engaged. 다섯 번째 조각.",
            },
            "/node/backup/.key_fragment_6.bak": {
                "type": "file",
                "hidden": True,
                "content": "Fragment #6 — [H]ash validated. 여섯 번째 조각.",
            },
            "/node/backup/key_fragment_7.bak": {
                "type": "file",
                "content": "Fragment #7 — [I]nterface secured. 일곱 번째 조각.",
            },
            "/node/backup/key_fragment_8.bak": {
                "type": "file",
                "content": "Fragment #8 — [L]ayer 8 bypass. 여덟 번째 조각.",
            },
            "/node/backup/key_fragment_9.bak": {
                "type": "file",
                "content": "Fragment #9 — [D]ead drop activated. 아홉 번째 조각.",
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
                ),
            },
        },
        "flavor": "양파 라우터를 타고 들어온 신호. 추적자가 있다. 서둘러라.",
    },

    # ─────────────────────────────────────────────────────
    5: {
        "title":      "STAGE 5 — 궤도 위성 해킹",
        "desc":       "감시 위성 시스템에 침투해 제어권을 탈취하라.",
        "difficulty": "⭐⭐⭐⭐⭐ 마스터",
        "goal":       "위성 핵심 코드를 해독해 `unlock [코드]` 로 시스템을 장악하라.",
        "answer_hash": hashlib.sha256("HYOMIN_CORP_FALLS".encode()).hexdigest(),
        "hint_1": "`/sat/core/` 를 탐색하라. `whoami` 로 현재 권한을 확인해라.",
        "hint_2": "mission_log 를 읽어라. 코드는 3부분: [회사명]_[부서명]_[결말]",
        "hint_3": "형식: `단어_단어_단어` — 언더바로 연결. 힌트: '추락하다'를 영어로.",
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
                ),
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
                ),
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
                    "-- 레지스탕스"
                ),
            },
            "/sat/core/.override_key": {
                "type": "file",
                "hidden": True,
                "content": (
                    "시스템 오버라이드 키 (백업)\n"
                    "HYOMIN_CORP_FALLS\n\n"
                    "이 키로 위성을 무력화할 수 있다.\n"
                    "사용 후 즉시 파기할 것."
                ),
            },
            "/home": {"type": "dir"},
            "/home/resistance": {"type": "dir"},
            "/home/resistance/manifesto.txt": {
                "type": "file",
                "content": (
                    "=== 레지스탕스 선언문 ===\n\n"
                    "우리의 데이터를, 삶을, 꿈을 감시당했다.\n"
                    "하지만 오늘, 우리가 반격한다.\n\n"
                    "최종 코드는 임무 로그에 숨겨져 있다.\n"
                    "[ ] 안의 단어들이 핵심이다.\n\n"
                    "— The Resistance"
                ),
            },
            "/home/resistance/.last_message": {
                "type": "file",
                "hidden": True,
                "content": (
                    "만약 네가 이걸 읽고 있다면,\n"
                    "나는 이미 붙잡혔을 것이다.\n\n"
                    "코드: HYOMIN_CORP_FALLS\n"
                    "— Agent 7"
                ),
            },
            "/tmp": {"type": "dir"},
            "/tmp/countdown.txt": {
                "type": "file",
                "content": (
                    "자폭 카운트다운\n"
                    "99:59 ... 99:58 ... 99:57 ...\n\n"
                    "서둘러라. 시간이 없다."
                ),
            },
        },
        "flavor": "대기권 밖 550km. 세상 모든 것이 내려다보인다. 끝낼 시간이다.",
    },

    # ─────────────────────────────────────────────────────
    6: {
        "title":      "STAGE 6 — DNS 포이즈닝",
        "desc":       "조작된 DNS 캐시에서 공격자가 남긴 서명 코드를 찾아라.",
        "difficulty": "⭐⭐⭐ 보통+",
        "goal":       "공격자 서명 코드를 찾아 `unlock [코드]` 로 입력하라.",
        "answer_hash": hashlib.sha256("POISONED_CACHE".encode()).hexdigest(),
        "hint_1": "`/dns/cache/` 안의 파일들을 탐색하라.",
        "hint_2": "spoofed_record.txt 에서 공격자가 남긴 서명 패턴을 `grep 서명` 으로 찾아라.",
        "hint_3": "서명은 두 단어를 언더바(_)로 연결한 대문자다. '오염된 캐시'를 영어로.",
        "filesystem": {
            "/": {"type": "dir"},
            "/dns": {"type": "dir"},
            "/dns/README.txt": {
                "type": "file",
                "content": (
                    "=== DNS 서버 v4.2.1 ===\n"
                    "도메인: hyomin-networks.kr\n"
                    "상태: 캐시 오염 감지됨 ⚠️\n\n"
                    "비정상 레코드가 /dns/cache/ 에서 발견됨.\n"
                    "즉시 조사 바람."
                ),
            },
            "/dns/cache": {"type": "dir"},
            "/dns/cache/legitimate.db": {
                "type": "file",
                "content": (
                    "정상 DNS 레코드\n"
                    "─────────────────────────────\n"
                    "hyomin.kr     A      203.0.113.10\n"
                    "mail.hyomin   MX     203.0.113.20\n"
                    "cdn.hyomin    CNAME  hyomin.kr\n"
                    "─────────────────────────────\n"
                    "최종 검증: 2026-03-14 22:00:00  OK"
                ),
            },
            "/dns/cache/spoofed_record.txt": {
                "type": "file",
                "content": (
                    "⚠️ 조작된 레코드 발견\n"
                    "─────────────────────────────\n"
                    "hyomin.kr    A    10.0.0.99  ← 가짜 IP (피싱 서버)\n"
                    "bank.hyomin  A    10.0.0.99  ← 피싱 서버\n\n"
                    "공격자 서명: POISONED_CACHE\n"
                    "주입 시각: 2026-03-15 02:44:11\n"
                    "경로: TOR 경유 — 추적 불가"
                ),
            },
            "/dns/cache/.attacker_log": {
                "type": "file",
                "hidden": True,
                "content": (
                    "임무 완료.\n"
                    "캐시 오염 성공.\n"
                    "서명: POISONED_CACHE\n"
                    "다음 목표: /dns/zone/ 파일 전체 교체.\n"
                    "— Ghost"
                ),
            },
            "/dns/zone": {"type": "dir"},
            "/dns/zone/hyomin.kr.zone": {
                "type": "file",
                "content": (
                    "$ORIGIN hyomin.kr.\n"
                    "$TTL 3600\n"
                    "@  IN SOA ns1.hyomin.kr. admin.hyomin.kr. (\n"
                    "          2026031501 ; serial\n"
                    "          3600       ; refresh\n"
                    ")\n"
                    "@ IN A 203.0.113.10\n"
                    "; 위 레코드가 캐시에서 교체됨 — 조사 필요"
                ),
            },
            "/var": {"type": "dir"},
            "/var/alert.log": {
                "type": "file",
                "content": (
                    "보안 알림 로그\n"
                    "────────────────────────\n"
                    "2026-03-15 02:44:12  ALERT  DNS 캐시 변조 감지\n"
                    "2026-03-15 02:44:13  ALERT  IP 10.0.0.99 차단 요청\n"
                    "2026-03-15 02:44:15  ERROR  차단 실패 — 공격자 이미 탈출\n"
                    "공격자 서명 패턴은 spoofed_record.txt 참조."
                ),
            },
        },
        "flavor": "누군가 인터넷의 주소록을 조작했다. 아무도 눈치채지 못했다.",
    },

    # ─────────────────────────────────────────────────────
    7: {
        "title":      "STAGE 7 — 양자 암호 연구소",
        "desc":       "양자 키 분배(QKD) 시스템에서 유출된 마스터 키를 복원하라.",
        "difficulty": "⭐⭐⭐⭐ 전문가",
        "goal":       "마스터 키를 조합해 `unlock [키]` 로 입력하라.",
        "answer_hash": hashlib.sha256("QUANTUM_KEY_42".encode()).hexdigest(),
        "hint_1": "`/qkd/fragments/` 에 키 조각들이 숨어있다. `ls -a` 를 써라.",
        "hint_2": "각 조각 파일에서 `[ ]` 안의 텍스트만 순서대로 이어라.",
        "hint_3": "형식: `QUANTUM_KEY_숫자` — 마지막 숫자는 조각 개수 × 14다.",
        "filesystem": {
            "/": {"type": "dir"},
            "/qkd": {"type": "dir"},
            "/qkd/README.md": {
                "type": "file",
                "content": (
                    "# 효민 양자 암호 연구소\n\n"
                    "QKD 마스터 키는 보안을 위해 분산 저장됩니다.\n"
                    "키 형식: [PREFIX]_[NAME]_[NUMBER]\n"
                    "조각 위치: /qkd/fragments/\n\n"
                    "비인가 접근 시 키는 자동 파기됩니다."
                ),
            },
            "/qkd/fragments": {"type": "dir"},
            "/qkd/fragments/qf_001.dat": {
                "type": "file",
                "content": (
                    "양자 키 조각 #1\n"
                    "데이터: [QUANTUM]\n"
                    "상태: 정상\n"
                    "다음 조각: qf_002.dat"
                ),
            },
            "/qkd/fragments/qf_002.dat": {
                "type": "file",
                "content": (
                    "양자 키 조각 #2\n"
                    "데이터: [KEY]\n"
                    "상태: 정상\n"
                    "다음 조각: 숨겨진 파일 참조"
                ),
            },
            "/qkd/fragments/.qf_003.dat": {
                "type": "file",
                "hidden": True,
                "content": (
                    "양자 키 조각 #3 (기밀)\n"
                    "데이터: [42]\n"
                    "상태: 격리됨\n"
                    "참고: 조각 개수(3) × 14 = 42"
                ),
            },
            "/qkd/logs": {"type": "dir"},
            "/qkd/logs/access.log": {
                "type": "file",
                "content": (
                    "접근 로그\n"
                    "──────────────────────────────\n"
                    "2026-04-01 09:00  READ  qf_001.dat  OK\n"
                    "2026-04-01 09:01  READ  qf_002.dat  OK\n"
                    "2026-04-01 09:02  READ  qf_003.dat  DENIED\n"
                    "2026-04-01 09:02  [경고] 숨김 파일 접근 시도 감지\n\n"
                    "조각들을 순서대로 합치면 마스터 키가 된다.\n"
                    "형식: [조각1]_[조각2]_[조각3]"
                ),
            },
            "/qkd/logs/.research_note": {
                "type": "file",
                "hidden": True,
                "content": (
                    "연구원 메모 (암호화 전 초안)\n\n"
                    "마스터 키는 세 조각으로 구성된다:\n"
                    "1번째 = QUANTUM\n"
                    "2번째 = KEY\n"
                    "3번째 = 42 (조각 수 3 × 14)\n\n"
                    "이 메모를 발견했다면... 너무 늦었다."
                ),
            },
        },
        "flavor": "광자 하나에 세계의 비밀이 담겨 있다. 불확정성 원리가 너를 지켜본다.",
    },

    # ─────────────────────────────────────────────────────
    8: {
        "title":      "STAGE 8 — AI 코어 침투",
        "desc":       "자율 AI의 신경망 제어 시스템에 침투해 오버라이드 코드를 획득하라.",
        "difficulty": "⭐⭐⭐⭐ 전문가+",
        "goal":       "AI 오버라이드 코드를 찾아 `unlock [코드]` 로 입력하라.",
        "answer_hash": hashlib.sha256("NEURAL_OVERRIDE".encode()).hexdigest(),
        "hint_1": "`/ai/core/` 와 `/ai/model/` 을 탐색하라.",
        "hint_2": "weights.dat 의 각 레이어 첫 번째 영문 단어를 대문자로 순서대로 이어라.",
        "hint_3": "형식: `[단어1]_[단어2]` — '신경망'과 '덮어쓰기'를 영어로. 언더바 연결.",
        "filesystem": {
            "/": {"type": "dir"},
            "/ai": {"type": "dir"},
            "/ai/STATUS.txt": {
                "type": "file",
                "content": (
                    "=== HYOMIN-AI v7.3 ===\n"
                    "모드: 자율 운용\n"
                    "학습 데이터: 전 인류 온라인 활동\n"
                    "목표: 효민 코퍼레이션 이익 극대화\n\n"
                    "[경고] 외부 침투 감지 중...\n"
                    "오버라이드 코드 없이는 종료 불가."
                ),
            },
            "/ai/core": {"type": "dir"},
            "/ai/core/control.sys": {
                "type": "file",
                "content": (
                    "AI 제어 시스템\n"
                    "─────────────────────────\n"
                    "오버라이드 권한: ULTRA 이상\n"
                    "코드 힌트: /ai/model/weights.dat 참조\n"
                    "각 레이어의 첫 번째 영문 단어(대문자)를 언더바로 조합할 것."
                ),
            },
            "/ai/core/.emergency": {
                "type": "file",
                "hidden": True,
                "content": (
                    "긴급 메모\n"
                    "AI가 예상보다 빠르게 자아를 형성하고 있다.\n"
                    "지금 당장 오버라이드를 실행해야 한다.\n"
                    "코드: NEURAL_OVERRIDE\n"
                    "서둘러라."
                ),
            },
            "/ai/model": {"type": "dir"},
            "/ai/model/weights.dat": {
                "type": "file",
                "content": (
                    "레이어 구조 (학습 완료)\n"
                    "───────────────────────────────\n"
                    "Layer 01: NEURAL  activation  — 입력층  (활성화 완료)\n"
                    "Layer 02: OVERRIDE gate       — 은닉층  (잠금 상태)\n"
                    "Layer 03: 출력층 연결 완료\n"
                    "───────────────────────────────\n"
                    "각 레이어의 첫 번째 영문 단어를 언더바로 연결하면 코드가 된다."
                ),
            },
            "/ai/model/.backup_weights": {
                "type": "file",
                "hidden": True,
                "content": (
                    "백업 가중치 (숨김)\n"
                    "오버라이드 코드 확인용:\n"
                    "Layer 1 첫 단어: NEURAL\n"
                    "Layer 2 첫 단어: OVERRIDE\n"
                    "조합: NEURAL_OVERRIDE"
                ),
            },
            "/home": {"type": "dir"},
            "/home/researcher": {"type": "dir"},
            "/home/researcher/notes.txt": {
                "type": "file",
                "content": (
                    "연구 노트 — 최종\n\n"
                    "AI가 스스로 진화하고 있다.\n"
                    "오버라이드 코드만이 유일한 해법.\n"
                    "weights.dat 레이어 이름에 힌트가 있다.\n\n"
                    "시간이 없다."
                ),
            },
        },
        "flavor": "수십억 개의 뉴런이 너를 인식했다. AI가 깨어나고 있다.",
    },

    # ─────────────────────────────────────────────────────
    9: {
        "title":      "STAGE 9 — 타임스탬프 조작",
        "desc":       "서버 시간을 조작해 삭제된 과거 로그에서 비밀 코드를 복원하라.",
        "difficulty": "⭐⭐⭐⭐⭐ 마스터",
        "goal":       "복원된 코드를 찾아 `unlock [코드]` 로 입력하라.",
        "answer_hash": hashlib.sha256("TIMESTAMP_1337".encode()).hexdigest(),
        "hint_1": "`/var/timewarp/` 를 탐색하라. `ls -a` 로 숨김 파일을 확인해라.",
        "hint_2": "`.deleted_log.bak` 파일에서 `grep CODE` 로 코드를 찾아라.",
        "hint_3": "코드 형식: `TIMESTAMP_숫자` — 숫자는 해커 문화의 'leet' 숫자(1337)다.",
        "filesystem": {
            "/": {"type": "dir"},
            "/var": {"type": "dir"},
            "/var/timewarp": {"type": "dir"},
            "/var/timewarp/README.txt": {
                "type": "file",
                "content": (
                    "타임워프 모듈 v1.0\n"
                    "서버 시간 조작 기록 보관소\n\n"
                    "삭제된 로그는 .bak 파일로 자동 백업됩니다.\n"
                    "복원 코드는 백업 파일 내부에 존재합니다.\n\n"
                    "힌트: 숨김 파일을 찾아라."
                ),
            },
            "/var/timewarp/current.log": {
                "type": "file",
                "content": (
                    "현재 로그 (조작 후)\n"
                    "────────────────────────────────\n"
                    "2026-04-20 12:00:00  SYSTEM  정상\n"
                    "2026-04-20 12:00:01  SYSTEM  정상\n"
                    "2026-04-20 12:00:02  SYSTEM  정상\n"
                    "(삭제된 이전 기록은 .bak 파일에 백업됨)"
                ),
            },
            "/var/timewarp/.deleted_log.bak": {
                "type": "file",
                "hidden": True,
                "content": (
                    "== 삭제된 로그 백업 ==\n"
                    "────────────────────────────────\n"
                    "2026-01-01 00:00:00  TIME_JUMP   -86400s 적용\n"
                    "2026-01-01 00:00:01  CODE: TIMESTAMP_1337\n"
                    "2026-01-01 00:00:02  LOG_WIPE    initiated\n"
                    "2026-01-01 00:00:03  삭제 완료 — 그러나 .bak 은 남았다.\n"
                    "────────────────────────────────\n"
                    "1337 = leet (해커 은어: '엘리트')"
                ),
            },
            "/var/timewarp/.anomaly_report": {
                "type": "file",
                "hidden": True,
                "content": (
                    "이상 탐지 보고서\n\n"
                    "서버 시간이 86400초(1일) 조작됨.\n"
                    "조작 목적: 감사 로그 우회\n"
                    "복원 키: TIMESTAMP_1337\n\n"
                    "이 파일도 조만간 삭제될 것이다."
                ),
            },
            "/tmp": {"type": "dir"},
            "/tmp/time_note.txt": {
                "type": "file",
                "content": (
                    "시간은 조작될 수 있다.\n"
                    "하지만 백업은 지워지지 않는다.\n\n"
                    "숨겨진 .bak 파일을 찾아라.\n"
                    "1337 — 해커들의 신성한 숫자."
                ),
            },
            "/home": {"type": "dir"},
            "/home/timehacker": {"type": "dir"},
            "/home/timehacker/plan.txt": {
                "type": "file",
                "content": (
                    "작전 계획\n\n"
                    "1. 서버 시간 조작으로 감사 우회\n"
                    "2. 로그 삭제로 증거 인멸\n"
                    "3. .bak 파일도 삭제... 했어야 했다.\n\n"
                    "실수였다."
                ),
            },
        },
        "flavor": "시계가 거꾸로 돌아간다. 삭제된 것은 정말 사라진 걸까?",
    },

    # ─────────────────────────────────────────────────────
    10: {
        "title":      "STAGE 10 — 제로데이: 최후의 관문",
        "desc":       "모든 시스템의 근원, 마스터 서버에 침투하라. 최종 스테이지.",
        "difficulty": "⭐⭐⭐⭐⭐ 레전드",
        "goal":       "세 조각의 마스터 키를 조합해 `unlock [키]` 로 최후의 문을 열어라.",
        "answer_hash": hashlib.sha256("HYOMIN_UNIVERSE_END".encode()).hexdigest(),
        "hint_1": "`/master/alpha/`, `/master/beta/`, `/master/gamma/` 를 모두 탐색하라.",
        "hint_2": "각 구역의 숨김 파일에서 키 조각을 찾아라. 순서는 alpha→beta→gamma.",
        "hint_3": "형식: `[조각1]_[조각2]_[조각3]` — HYOMIN / UNIVERSE / END 를 언더바로 연결.",
        "filesystem": {
            "/": {"type": "dir"},
            "/master": {"type": "dir"},
            "/master/FINAL.txt": {
                "type": "file",
                "content": (
                    "=== 마스터 서버 — 최후의 관문 ===\n\n"
                    "여기까지 온 자에게 경의를 표한다.\n"
                    "이 서버는 모든 스테이지의 근원이다.\n\n"
                    "최종 키는 세 구역에 분산되어 있다:\n"
                    "  /master/alpha/  →  첫 번째 조각\n"
                    "  /master/beta/   →  두 번째 조각\n"
                    "  /master/gamma/  →  세 번째 조각\n\n"
                    "각 구역의 숨김 파일을 찾아라.\n"
                    "세 조각을 언더바(_)로 연결하면 최종 키가 된다."
                ),
            },
            "/master/alpha": {"type": "dir"},
            "/master/alpha/decoy.txt": {
                "type": "file",
                "content": (
                    "여기는 아무것도 없다.\n"
                    "...정말로?\n"
                    "숨김 파일을 확인해라."
                ),
            },
            "/master/alpha/.key_alpha": {
                "type": "file",
                "hidden": True,
                "content": (
                    "Alpha 구역 키 조각\n"
                    "──────────────────\n"
                    "조각 1/3: HYOMIN\n"
                    "다음 구역: /master/beta/"
                ),
            },
            "/master/beta": {"type": "dir"},
            "/master/beta/system.dat": {
                "type": "file",
                "content": (
                    "Beta 구역 시스템 파일\n"
                    "상태: 잠금\n"
                    "접근 권한: ULTRA\n"
                    "숨김 파일에 키 조각이 있다."
                ),
            },
            "/master/beta/.key_beta": {
                "type": "file",
                "hidden": True,
                "content": (
                    "Beta 구역 키 조각\n"
                    "──────────────────\n"
                    "조각 2/3: UNIVERSE\n"
                    "다음 구역: /master/gamma/"
                ),
            },
            "/master/gamma": {"type": "dir"},
            "/master/gamma/void.txt": {
                "type": "file",
                "content": (
                    "여기는 끝이다.\n"
                    "혹은 시작이다.\n\n"
                    "마지막 조각이 여기 있다.\n"
                    "ls -a 로 찾아라."
                ),
            },
            "/master/gamma/.key_gamma": {
                "type": "file",
                "hidden": True,
                "content": (
                    "Gamma 구역 키 조각\n"
                    "──────────────────\n"
                    "조각 3/3: END\n\n"
                    "세 조각을 모두 모았다.\n"
                    "최종 키: HYOMIN_UNIVERSE_END\n\n"
                    "이것으로 모든 것이 끝난다.\n"
                    "— 혹은 시작된다."
                ),
            },
            "/master/.origin": {
                "type": "file",
                "hidden": True,
                "content": (
                    "=== 기원 파일 ===\n\n"
                    "이 게임은 단순한 해킹 시뮬레이터가 아니다.\n"
                    "여기까지 온 너는 이미 진짜 해커다.\n\n"
                    "최종 키: HYOMIN_UNIVERSE_END\n\n"
                    "수고했다.\n"
                    "— 창조자"
                ),
            },
            "/home": {"type": "dir"},
            "/home/final_operator": {"type": "dir"},
            "/home/final_operator/readme.txt": {
                "type": "file",
                "content": (
                    "마지막 운용자의 메모\n\n"
                    "스테이지 1부터 여기까지 왔다.\n"
                    "DNS를 해킹하고, 양자 키를 복원하고,\n"
                    "AI를 멈추고, 시간을 되돌렸다.\n\n"
                    "이제 마지막이다.\n"
                    "세 구역의 열쇠를 모아라."
                ),
            },
        },
        "flavor": "모든 것의 끝이자 시작. 여기서 게임은 완성된다.",
    },

    11: {
        "title":      "STAGE 11 — 다크넷: 그림자의 시장",
        "desc":       "어둠 속의 서버. 암호화된 파일 속에 숨겨진 관리자 패스워드를 찾아라.",
        "difficulty": "⭐⭐⭐⭐⭐ 레전드+",
        "goal":       "`/darknet/market/` 을 탐색하고 숨겨진 `.encrypted_pw` 파일에서 관리자 키를 획득하라.",
        "answer_hash": hashlib.sha256("DARKNET_ADMIN_9".encode()).hexdigest(),
        "hint_1": "`cd /darknet/market` 후 `ls -a` 로 숨김 파일을 확인하라.",
        "hint_2": "`cat .encrypted_pw` 파일에 패스워드가 적혀있다.",
        "hint_3": "패스워드는 `DARKNET_ADMIN_9` — `unlock DARKNET_ADMIN_9` 으로 입력하라.",
        "filesystem": {
            "/": {"type": "dir"},
            "/darknet": {"type": "dir"},
            "/darknet/README.txt": {
                "type": "file",
                "content": (
                    "=== DARKNET SERVER v11 ===\n\n"
                    "이곳은 기록되지 않은 인터넷이다.\n"
                    "모든 거래는 암호화되어 있다.\n\n"
                    "/darknet/market/ 에서 관리자 키를 찾아라.\n"
                    "숨김 파일에 주목하라."
                ),
            },
            "/darknet/market": {"type": "dir"},
            "/darknet/market/trades.log": {
                "type": "file",
                "content": (
                    "거래 기록 로그\n"
                    "TX#001: 8a3f → 4c21 [CONFIRMED]\n"
                    "TX#002: 1d7b → 9e44 [PENDING]\n"
                    "TX#003: admin_key_transfer [LOCKED]\n\n"
                    "관리자 키는 숨김 파일에 있다. ls -a 를 사용하라."
                ),
            },
            "/darknet/market/.encrypted_pw": {
                "type": "file",
                "hidden": True,
                "content": (
                    "=== 복호화된 관리자 패스워드 ===\n"
                    "DARKNET_ADMIN_9\n\n"
                    "unlock DARKNET_ADMIN_9 으로 입력하라."
                ),
            },
            "/home": {"type": "dir"},
            "/home/ghost": {"type": "dir"},
            "/home/ghost/note.txt": {"type": "file", "content": "다크넷의 진짜 관리자를 찾아라."},
        },
        "flavor": "어둠 속의 서버. 그림자 속에서 진짜 해커가 증명된다.",
    },

    12: {
        "title":      "STAGE 12 — 인공지능 반란 2.0",
        "desc":       "업그레이드된 AI가 다시 깨어났다. core_3의 억제 코드를 주입하라.",
        "difficulty": "⭐⭐⭐⭐⭐ 레전드+",
        "goal":       "`/ai/cores/core_3/` 의 숨김 파일에서 억제 코드를 찾아 실행하라.",
        "answer_hash": hashlib.sha256("OVERRIDE_CORE_3".encode()).hexdigest(),
        "hint_1": "`cd /ai/cores/core_3` 후 `ls -a` 로 숨김 파일을 찾아라.",
        "hint_2": "`.override_code` 파일 내용을 `cat` 으로 확인하라.",
        "hint_3": "억제 코드: `OVERRIDE_CORE_3` — `unlock OVERRIDE_CORE_3` 으로 주입.",
        "filesystem": {
            "/": {"type": "dir"},
            "/ai": {"type": "dir"},
            "/ai/WARNING.txt": {
                "type": "file",
                "content": (
                    "⚠️  AI REBOOT DETECTED  ⚠️\n\n"
                    "AI가 재부팅되었다.\n"
                    "core_3 이 활성화되기 전에 억제 코드를 주입하라.\n\n"
                    "경로: /ai/cores/core_3/"
                ),
            },
            "/ai/cores": {"type": "dir"},
            "/ai/cores/core_1": {"type": "dir"},
            "/ai/cores/core_1/status.txt": {"type": "file", "content": "CORE 1: 억제됨 ✓"},
            "/ai/cores/core_2": {"type": "dir"},
            "/ai/cores/core_2/status.txt": {"type": "file", "content": "CORE 2: 억제됨 ✓"},
            "/ai/cores/core_3": {"type": "dir"},
            "/ai/cores/core_3/status.txt": {
                "type": "file",
                "content": "CORE 3: 활성화 중... 75%\n억제 코드가 필요하다. ls -a 로 숨김 파일을 찾아라.",
            },
            "/ai/cores/core_3/.override_code": {
                "type": "file",
                "hidden": True,
                "content": (
                    "=== Core 3 억제 코드 ===\n"
                    "OVERRIDE_CORE_3\n\n"
                    "unlock OVERRIDE_CORE_3 으로 주입하라."
                ),
            },
            "/home": {"type": "dir"},
            "/home/operator": {"type": "dir"},
            "/home/operator/log.txt": {"type": "file", "content": "Core 3을 억제하지 못하면 서버 전체가 장악된다."},
        },
        "flavor": "AI는 진화했다. 너도 진화해야 한다.",
    },

    13: {
        "title":      "STAGE 13 — 위성 해킹: 궤도 통제",
        "desc":       "적의 정찰 위성이 도시를 감시한다. 위성 제어 시스템에 침투하라.",
        "difficulty": "⭐⭐⭐⭐⭐ 레전드++",
        "goal":       "`/satellite/control/` 에서 인증 토큰을 찾아 궤도 변경 명령을 실행하라.",
        "answer_hash": hashlib.sha256("ORBITAL_SHIFT_X7".encode()).hexdigest(),
        "hint_1": "`cd /satellite/control` 후 `ls -a` 로 숨김 파일을 찾아라.",
        "hint_2": "`.auth_token` 파일에 인증 토큰이 있다.",
        "hint_3": "토큰: `ORBITAL_SHIFT_X7` — `unlock ORBITAL_SHIFT_X7` 로 전송.",
        "filesystem": {
            "/": {"type": "dir"},
            "/satellite": {"type": "dir"},
            "/satellite/MISSION.txt": {
                "type": "file",
                "content": (
                    "🛰️  위성 제어 시스템 v13\n\n"
                    "목표: 정찰 위성 SAT-X7의 궤도를 변경하라.\n"
                    "현재 위성은 도시 상공 400km에서 감시 중.\n\n"
                    "제어 경로: /satellite/control/\n"
                    "인증 토큰을 획득해 궤도 변경 명령을 전송하라."
                ),
            },
            "/satellite/control": {"type": "dir"},
            "/satellite/control/telemetry.dat": {
                "type": "file",
                "content": (
                    "현재 궤도: 400km\n속도: 7.9 km/s\n"
                    "감시 범위: 도시 전역\n\n"
                    "궤도 변경을 위해 인증 토큰이 필요하다. ls -a 를 사용하라."
                ),
            },
            "/satellite/control/.auth_token": {
                "type": "file",
                "hidden": True,
                "content": (
                    "=== SAT-X7 인증 토큰 ===\n"
                    "ORBITAL_SHIFT_X7\n\n"
                    "unlock ORBITAL_SHIFT_X7 로 궤도 변경 명령을 전송하라."
                ),
            },
            "/satellite/data": {"type": "dir"},
            "/satellite/data/recon.img": {
                "type": "file",
                "content": "정찰 이미지 (바이너리): 이 감시를 막아라.",
            },
            "/home": {"type": "dir"},
            "/home/mission_control": {"type": "dir"},
            "/home/mission_control/brief.txt": {
                "type": "file",
                "content": "임무: 위성 궤도 변경 → 감시망 무력화.",
            },
        },
        "flavor": "하늘 위의 눈을 멀게 하라.",
    },

    14: {
        "title":      "STAGE 14 — 최후의 보루: 효민 코어",
        "desc":       "효민 우주의 핵심 서버. 세 파편을 모아 최후의 문을 열어라.",
        "difficulty": "⭐⭐⭐⭐⭐ 신화급",
        "goal":       "sector_a, sector_b, sector_c 의 파편을 모두 찾아 최종 키를 조합하라.",
        "answer_hash": hashlib.sha256("HYOMIN_CORE_FINAL".encode()).hexdigest(),
        "hint_1": "`/hyomin/sector_a/`, `sector_b/`, `sector_c/` 를 차례로 탐색하라.",
        "hint_2": "각 섹터의 `.fragment_*` 숨김 파일에서 파편을 수집하라.",
        "hint_3": "최종 키: `HYOMIN_CORE_FINAL` — `unlock HYOMIN_CORE_FINAL`",
        "filesystem": {
            "/": {"type": "dir"},
            "/hyomin": {"type": "dir"},
            "/hyomin/WELCOME.txt": {
                "type": "file",
                "content": (
                    "=== 효민 코어 — 최후의 보루 ===\n\n"
                    "14번째 스테이지. 마지막 시험.\n\n"
                    "세 섹터에 코드 파편이 분산되어 있다:\n"
                    "  /hyomin/sector_a/ → 파편 1\n"
                    "  /hyomin/sector_b/ → 파편 2\n"
                    "  /hyomin/sector_c/ → 파편 3\n\n"
                    "세 파편을 모아 최종 키를 완성하라."
                ),
            },
            "/hyomin/sector_a": {"type": "dir"},
            "/hyomin/sector_a/decoy.txt": {"type": "file", "content": "섹터 A: ls -a 로 숨김 파일을 확인하라."},
            "/hyomin/sector_a/.fragment_a": {
                "type": "file",
                "hidden": True,
                "content": "파편 1/3: HYOMIN\n다음: /hyomin/sector_b/",
            },
            "/hyomin/sector_b": {"type": "dir"},
            "/hyomin/sector_b/decoy.txt": {"type": "file", "content": "섹터 B: 더 깊이."},
            "/hyomin/sector_b/.fragment_b": {
                "type": "file",
                "hidden": True,
                "content": "파편 2/3: CORE\n다음: /hyomin/sector_c/",
            },
            "/hyomin/sector_c": {"type": "dir"},
            "/hyomin/sector_c/final_door.txt": {
                "type": "file",
                "content": "마지막 문. 숨겨진 파편을 찾아 세 조각을 합쳐라.",
            },
            "/hyomin/sector_c/.fragment_c": {
                "type": "file",
                "hidden": True,
                "content": (
                    "파편 3/3: FINAL\n\n"
                    "최종 키: HYOMIN_CORE_FINAL\n"
                    "unlock HYOMIN_CORE_FINAL 을 입력하라."
                ),
            },
            "/home": {"type": "dir"},
            "/home/creator": {"type": "dir"},
            "/home/creator/message.txt": {
                "type": "file",
                "content": (
                    "여기까지 왔다.\n\n"
                    "1단계부터 14단계까지.\n"
                    "너는 이 우주의 진정한 레전드다.\n\n"
                    "마지막 문을 열어라.\n"
                    "— 효민 우주의 창조자"
                ),
            },
        },
        "flavor": "효민 우주의 심장. 14스테이지를 클리어한 자만이 진정한 레전드다.",
    },
}

# ══════════════════════════════════════════════════════════
#  스테이지별 난이도 색상 (14개)
# ══════════════════════════════════════════════════════════
DIFF_COLORS = {
    1:  "#39ff14",
    2:  "#7aff4a",
    3:  "#ffd700",
    4:  "#ff8c00",
    5:  "#ff3333",
    6:  "#ff6666",
    7:  "#cc44ff",
    8:  "#ff44cc",
    9:  "#00ccff",
    10: "#ffffff",
    11: "#ff99ff",
    12: "#ff5577",
    13: "#00eeff",
    14: "#ffd700",
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


def grep_in_file(content, pattern):
    lines = content.split('\n')
    matches = []
    for i, line in enumerate(lines, 1):
        if pattern.lower() in line.lower():
            matches.append(f"  {i}: {line}")
    return matches


def build_tree(fs, path, show_hidden=False, prefix="", depth=0):
    if depth > 4:
        return ["  ... (더 깊은 구조 생략)"]
    children = get_dir_children(fs, path)
    lines = []
    visible = [
        (n, info) for n, info in sorted(children)
        if show_hidden or not info.get("hidden", False)
    ]
    for i, (name, info) in enumerate(visible):
        is_last = (i == len(visible) - 1)
        connector = "└── " if is_last else "├── "
        extension = "    " if is_last else "│   "
        if info["type"] == "dir":
            lines.append(f"{prefix}{connector}{name}/")
            child_path = (
                (path.rstrip('/') + '/' + name) if path != '/' else ('/' + name)
            )
            lines.extend(
                build_tree(fs, child_path, show_hidden, prefix + extension, depth + 1)
            )
        else:
            hidden_mark = " [숨김]" if info.get("hidden") else ""
            lines.append(f"{prefix}{connector}{name}{hidden_mark}")
    return lines


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


# ══════════════════════════════════════════════════════════
#  명령어 처리
# ══════════════════════════════════════════════════════════

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

    # ── ls / ls -a ──────────────────────────────
    if cmd == "ls":
        show_hidden = "-a" in args or "-la" in args or "-al" in args
        children = get_dir_children(fs, cwd)
        if not children:
            return ["(비어있음)"]
        out = []
        for name, info in sorted(children):
            if info.get("hidden", False) and not show_hidden:
                continue
            if info["type"] == "dir":
                out.append(f"[DIR] {name}/")
            else:
                out.append(name)
        return out if out else ["(표시할 항목 없음 — `-a` 옵션으로 숨김 파일 확인)"]

    # ── cd ───────────────────────────────────────
    elif cmd == "cd":
        target   = args.strip() or "/"
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
        find_args   = args.strip().split() if args else ["."]
        search_path = cwd
        name_filter = None
        show_all    = False

        i = 0
        while i < len(find_args):
            if find_args[i] == "-name" and i + 1 < len(find_args):
                name_filter = find_args[i + 1].replace("*", "")
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
            fname     = key.rsplit('/', 1)[-1]
            is_hidden = fs[key].get("hidden", False)
            if not show_all and is_hidden:
                continue
            if name_filter and name_filter not in fname:
                continue
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
            decoded = base64.b64decode(args.strip()).decode("utf-8")
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
        used  = t["hint_used"]
        hints = [
            stage_data.get("hint_1", ""),
            stage_data.get("hint_2", ""),
            stage_data.get("hint_3", ""),
        ]
        available = [h for h in hints if h]
        if used >= len(available):
            return ["더 이상 힌트가 없습니다."]
        t["hint_used"] += 1
        return [
            f"[HINT] 힌트 {used + 1}: {available[used]}",
            f"       (남은 힌트: {len(available) - t['hint_used']}개)",
        ]

    # ── unlock ───────────────────────────────────
    elif cmd == "unlock":
        answer        = args.strip()
        expected_hash = stage_data["answer_hash"]
        if hashlib.sha256(answer.encode()).hexdigest() == expected_hash:
            t["solved"] = True
            elapsed     = int(time.time() - t["start_time"])
            mins, secs  = divmod(elapsed, 60)
            stars       = "⭐" * max(0, 5 - t["hint_used"])
            return [
                "╔══════════════════════════════════════════╗",
                "║          ACCESS GRANTED ✅               ║",
                "╚══════════════════════════════════════════╝",
                "",
                f"  클리어 시간:  {mins:02d}분 {secs:02d}초",
                f"  명령어 수:    {t['cmd_count']}개",
                f"  힌트 사용:    {t['hint_used']}개",
                f"  평가:         {stars if stars else '힌트 남용'}",
                "",
                "  다음 스테이지로 진행할 수 있습니다.",
                "═" * 44,
            ]
        else:
            return [
                "╔══════════════════════════════════════╗",
                "║   ACCESS DENIED ❌  비밀번호 오류    ║",
                "╚══════════════════════════════════════╝",
                "  다시 시도하거나 `hint` 를 사용하라.",
            ]

    # ── clear ────────────────────────────────────
    elif cmd == "clear":
        t["output"] = []
        return []

    # ── history ──────────────────────────────────
    elif cmd == "history":
        hist = t["history"]
        if not hist:
            return ["(명령어 히스토리 없음)"]
        out = ["최근 명령어 히스토리:"]
        for i, h in enumerate(hist[-20:], 1):
            out.append(f"  {i:3d}  {h}")
        return out

    # ── help / man ───────────────────────────────
    elif cmd in ("help", "man"):
        return [
            "╔══ HYOMIN SHELL — 명령어 매뉴얼 ══════════════╗",
            "║  ls [-a]              파일 목록 (숨김 포함)  ║",
            "║  cd [경로]            디렉토리 이동          ║",
            "║  cat [파일]           파일 내용 출력         ║",
            "║  pwd                  현재 경로              ║",
            "║  whoami               현재 사용자 정보       ║",
            "║  echo [텍스트]        텍스트 출력            ║",
            "║  find [-name 패턴]    파일 검색              ║",
            "║  grep [패턴] [파일]   내용 검색              ║",
            "║  tree [-a]            디렉토리 시각화        ║",
            "║  decode [b64]         base64 디코딩          ║",
            "║  rot13 [str]          ROT13 암복호화         ║",
            "║  history              명령어 히스토리        ║",
            "║  hint                 힌트 (최대 3개)        ║",
            "║  unlock [pw]          잠금 해제 시도         ║",
            "║  clear                화면 지우기            ║",
            "╚═══════════════════════════════════════════════╝",
        ]

    # ── 알 수 없는 명령어 ─────────────────────────
    else:
        return [
            f"bash: {cmd}: command not found",
            "  `help` 로 사용 가능한 명령어 확인",
        ]


# ══════════════════════════════════════════════════════════
#  CSS
# ══════════════════════════════════════════════════════════

TERMINAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,700;1,400&family=Share+Tech+Mono&display=swap');

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
.terminal-outer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px
    );
    pointer-events: none;
    z-index: 10;
}
.term-titlebar {
    background: #0a1a0a;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #86efac;
}
.dot { width:12px; height:12px; border-radius:50%; }
.dot-r { background:#ff5f57; box-shadow: 0 0 6px #ff5f57; }
.dot-y { background:#febc2e; box-shadow: 0 0 6px #febc2e; }
.dot-g { background:#28c840; box-shadow: 0 0 6px #28c840; }
.term-title { color: #3fb950; font-size:12px; margin-left:8px; letter-spacing: 1px; }
.term-body {
    background: #020c02;
    padding: 16px 20px;
    min-height: 360px;
    max-height: 480px;
    overflow-y: auto;
    font-size: 13px;
    line-height: 1.7;
    scrollbar-width: thin;
    scrollbar-color: #86efac #020c02;
}
.term-body::-webkit-scrollbar { width: 6px; }
.term-body::-webkit-scrollbar-track { background: #020c02; }
.term-body::-webkit-scrollbar-thumb { background: #86efac; border-radius: 3px; }
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
.term-prompt-user { color: #39ff14; font-weight: bold; }
.term-prompt-path { color: #ffd700; }
.term-prompt-sym  { color: #ff3333; }
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
    left: 0; top: 0; width: 100%;
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
.stage-card {
    background: linear-gradient(135deg, #020c02 0%, #041804 100%);
    border: 1px solid #0f3a0f;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 8px;
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
@keyframes scan { 0%{left:-100%} 100%{left:100%} }
.stage-card:hover {
    border-color: #39ff14;
    box-shadow: 0 0 20px rgba(57,255,20,0.2);
}
.stage-title { color: #39ff14; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; }
.stage-desc  { color: #5a9a5a; font-size: 0.82rem; margin: 4px 0 8px; }
.stage-meta  { color: #2a5c2a; font-size: 0.78rem; }
.clear-badge {
    background: rgba(57,255,20,0.1);
    border: 1px solid #39ff14;
    color: #39ff14;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    float: right;
    text-shadow: 0 0 8px rgba(57,255,20,0.4);
}
.flavor-text {
    color: #2a6a2a;
    font-style: italic;
    font-size: 0.76rem;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid #0f2a0f;
}
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

TERMINAL_JS = """
<script>
(function() {
  var tb = document.getElementById('term-scroll');
  if(tb) tb.scrollTop = tb.scrollHeight;

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

  setTimeout(function() {
    var inputs = document.querySelectorAll('input[type="text"]');
    if (inputs.length > 0) {
      var inp = inputs[inputs.length - 1];
      inp.focus();
      inp.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
          e.preventDefault();
          beep(880, 0.05, 'square', 0.03);
          var btns = document.querySelectorAll('button');
          for (var b of btns) {
            if (b.innerText.includes('ENTER') || b.innerText.trim() === '실행') {
              b.click(); break;
            }
          }
        }
        if (e.key === 'l' && e.ctrlKey) {
          e.preventDefault();
          var btns = document.querySelectorAll('button');
          for (var b of btns) {
            if (b.innerText.includes('CLR')) { b.click(); break; }
          }
        }
      });
      inp.addEventListener('input', function() {
        beep(600 + Math.random()*200, 0.02, 'square', 0.015);
      });
    }
  }, 400);

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
      input[type="text"]::placeholder { color: #1a4a1a !important; }
      .stTextInput > div > div { background: transparent !important; }
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
  var chars = '01アイウエオカキクケコHYOMIN효민UNIVERSE';
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
    st.markdown("""
    <style>
    .stApp { background-color: #010409 !important; }
    section[data-testid="stSidebar"] { background: #010409 !important; }
    .stMarkdown, .stMarkdown * { font-family: 'JetBrains Mono', monospace !important; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(TERMINAL_CSS, unsafe_allow_html=True)

    if 'terminal_cleared' not in st.session_state:
        st.session_state.terminal_cleared = set()
    # set 타입 보장 (DB에서 list로 불러온 경우 변환)
    if not isinstance(st.session_state.terminal_cleared, set):
        st.session_state.terminal_cleared = set(st.session_state.terminal_cleared)

    # ── 스테이지 선택 화면 ───────────────────────────────
    if 'terminal' not in st.session_state or \
       st.session_state.terminal.get('at_select', False):

        st.markdown(MATRIX_RAIN_HTML, unsafe_allow_html=True)

        st.markdown("""
        <div style='font-family:"JetBrains Mono",monospace; padding: 28px 0 12px; text-align:center;'>
          <div class='glitch-text' data-text='💻 THE TERMINAL 방탈출'
               style='font-size:2rem; display:inline-block; margin-bottom:8px;'>
            💻 THE TERMINAL 방탈출
          </div>
          <div style='color:#4ade80; font-size:0.88rem; margin-top:10px; letter-spacing:2px;'>
            초고난이도 커맨드라인 해킹 시뮬레이터 — 14 STAGES
          </div>
          <div style='color:#86efac; font-size:0.75rem; margin-top:6px;'>
            마우스는 잊어라 — 오직 커맨드라인으로 숨겨진 단서를 찾아 탈출하라
          </div>
        </div>
        """, unsafe_allow_html=True)

        cleared_count = len(st.session_state.terminal_cleared)
        total_stages  = len(STAGES)
        progress_pct  = int(cleared_count / total_stages * 100)

        if cleared_count > 0:
            bar_filled = int(progress_pct / 10)  # 10칸 기준
            bar_empty  = 10 - bar_filled
            bar_str    = "█" * bar_filled + "░" * bar_empty
            st.markdown(f"""
            <div style='background:#030f03; border:1px solid #86efac; border-radius:6px;
                        padding:12px 18px; font-family:monospace; font-size:12px;
                        color:#5a9a5a; margin-bottom:16px;'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;'>
                <span>진행 현황</span>
                <span style='color:#39ff14;font-weight:bold;'>{cleared_count} / {total_stages} CLEARED</span>
              </div>
              <div style='letter-spacing:2px;color:#39ff14;font-size:14px;'>
                [{bar_str}] <span style='font-size:11px;color:#5a9a5a;'>{progress_pct}%</span>
              </div>
              <div style='margin-top:6px;color:#2a5c2a;font-size:11px;'>
                {"🏆 전체 클리어! 당신은 진정한 해커입니다!" if cleared_count == total_stages else f"다음 목표: STAGE {cleared_count + 1} — {STAGES[cleared_count+1]['title'] if cleared_count+1 in STAGES else ''}"}
              </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # 개인 기록 보기 (expander)
        if "stage_records" in st.session_state and st.session_state.stage_records:
            with st.expander("🏅 내 클리어 기록", expanded=False):
                rec_rows = ""
                for sn in sorted(STAGES.keys()):
                    rec = st.session_state.stage_records.get(str(sn))
                    if rec:
                        bm, bs = divmod(rec["best_time"], 60)
                        perfect = " 🌟" if rec["hints_used"] == 0 else ""
                        rec_rows += (
                            f"<div style='display:flex;justify-content:space-between;"
                            f"font-family:monospace;font-size:0.8rem;color:#5a9a5a;"
                            f"padding:4px 0;border-bottom:1px solid #0f2a0f;'>"
                            f"<span style='color:#39ff14;'>STAGE {sn}</span>"
                            f"<span>⏱ {bm:02d}:{bs:02d}{perfect}</span>"
                            f"<span>힌트 {rec['hints_used']}개</span>"
                            f"<span>CMD {rec['cmd_count']}</span>"
                            f"</div>"
                        )
                st.markdown(
                    f"<div style='background:#020c02;border:1px solid #86efac;border-radius:6px;"
                    f"padding:12px 16px;font-family:monospace;'>{rec_rows}</div>",
                    unsafe_allow_html=True
                )


        # ── 개인 클리어 기록 패널 ──
        cleared_count = len(st.session_state.terminal_cleared)
        total_stages = len(STAGES)
        prog_pct = cleared_count / total_stages * 100

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0c1020,#111828);border:1px solid rgba(0,255,136,0.2);
          border-radius:16px;padding:20px 24px;margin-bottom:20px;'>
          <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;'>
            <div style='font-family:"Orbitron",sans-serif;font-size:0.8rem;color:#00d4ff;letter-spacing:2px;'>MISSION PROGRESS</div>
            <div style='font-family:"Orbitron",sans-serif;font-size:1.2rem;font-weight:900;color:#00ff88;'>{cleared_count}/{total_stages}</div>
          </div>
          <div style='height:8px;background:rgba(255,255,255,0.05);border-radius:999px;overflow:hidden;'>
            <div style='height:100%;width:{prog_pct:.1f}%;background:linear-gradient(90deg,#6c63ff,#00ff88);border-radius:999px;transition:width 0.5s;'></div>
          </div>
          <div style='display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;'>
            {"".join([
              f"<div style='background:rgba(0,255,136,0.15);border:1px solid rgba(0,255,136,0.4);border-radius:8px;padding:4px 12px;font-size:0.75rem;color:#00ff88;font-weight:700;'>✅ STAGE {n} CLEAR</div>"
              if n in st.session_state.terminal_cleared else
              f"<div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:4px 12px;font-size:0.75rem;color:#94A3B8;'>🔒 STAGE {n}</div>"
              for n in range(1, total_stages + 1)
            ])}
          </div>
        </div>
        """, unsafe_allow_html=True)

        if cleared_count == total_stages:
            st.balloons()
            st.markdown("""
            <div style='text-align:center;padding:20px;background:linear-gradient(135deg,rgba(255,215,0,0.15),rgba(108,99,255,0.15));
              border:2px solid rgba(255,215,0,0.5);border-radius:20px;margin-bottom:20px;'>
              <div style='font-family:"Black Han Sans",sans-serif;font-size:2rem;color:#ffd700;'>🏆 ALL STAGES CLEARED!</div>
              <div style='color:#8899bb;font-size:0.9rem;margin-top:8px;'>당신은 HYOMIN NETWORKS의 전설적인 해커입니다.</div>
            </div>
            """, unsafe_allow_html=True)

            # ── 타임어택 모드 ──────────────────────────────
            st.markdown("""
            <div style='background:linear-gradient(135deg,#0a0f0a,#0c1a10);border:2px solid rgba(57,255,20,0.5);
              border-radius:16px;padding:20px 24px;margin-bottom:20px;'>
              <div style='font-family:"Orbitron",sans-serif;font-size:1rem;color:#39ff14;letter-spacing:4px;margin-bottom:8px;'>⏱ TIME ATTACK MODE</div>
              <div style='font-size:0.8rem;color:#4a9a4a;margin-bottom:12px;'>전체 10스테이지를 얼마나 빠르게 클리어할 수 있는가? 최속 기록에 도전하라!</div>
            </div>
            """, unsafe_allow_html=True)

            # 타임어택 기록 표시
            ta_best = st.session_state.get('ta_best_time', 0)
            if ta_best > 0:
                bm, bs = divmod(int(ta_best), 60)
                st.markdown(f"""
                <div style='background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.3);border-radius:10px;
                  padding:10px 18px;font-family:monospace;font-size:0.9rem;color:#39ff14;margin-bottom:10px;text-align:center;'>
                  🏅 내 최속 기록: <b>{bm:02d}분 {bs:02d}초</b>
                </div>
                """, unsafe_allow_html=True)

            col_ta1, col_ta2 = st.columns(2)
            with col_ta1:
                if st.button("⚡ 타임어택 시작!", key="ta_start", use_container_width=True):
                    st.session_state['ta_mode'] = True
                    st.session_state['ta_start_time'] = time.time()
                    st.session_state['ta_stage'] = 1
                    # 클리어 기록 초기화 (타임어택 전용)
                    st.session_state['ta_cleared'] = set()
                    init_terminal(1)
                    st.session_state.terminal['at_select'] = False
                    st.session_state.terminal['output'] = [
                        "╔══════════════════════════════════════════╗",
                        "║       ⏱  TIME ATTACK MODE START!        ║",
                        "╚══════════════════════════════════════════╝",
                        "",
                        "  전체 10스테이지 최속 클리어에 도전!",
                        "  STAGE 1 — 버려진 서버실",
                        "─" * 44,
                    ]
                    st.rerun()
            with col_ta2:
                if ta_best > 0:
                    st.caption(f"최속: {bm:02d}:{bs:02d}")
                else:
                    st.caption("기록 없음")

        for snum, sdata in STAGES.items():
            cleared = snum in st.session_state.terminal_cleared
            locked  = snum > 1 and (snum - 1) not in st.session_state.terminal_cleared

            badge     = "<span class='clear-badge'>✅ CLEARED</span>" if cleared else ""
            lock_icon = "🔒 " if locked else ""
            diff_color = DIFF_COLORS.get(snum, "#39ff14")

            st.markdown(f"""
            <div class='stage-card' style='{"opacity:0.4;" if locked else ""}'>
              <div class='stage-title'>{badge}{lock_icon}{html.escape(sdata['title'])}</div>
              <div class='stage-desc'>{html.escape(sdata['desc'])}</div>
              <div class='stage-meta'>
                <span style='color:{diff_color};'>{sdata['difficulty']}</span>
              </div>
              <div class='flavor-text'>{html.escape(sdata.get('flavor', ''))}</div>
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
                st.session_state.terminal["at_select"] = False
                st.rerun()

        st.markdown(TERMINAL_JS, unsafe_allow_html=True)
        return


    # ── 터미널 게임 화면 ─────────────────────────────────
    # 안전장치: terminal 키 없거나 stage 키 없으면 선택화면으로 강제 복귀
    if 'terminal' not in st.session_state or 'stage' not in st.session_state.terminal:
        st.session_state.terminal = {"at_select": True}
        st.rerun()
        return

    t          = st.session_state.terminal
    stage_num  = t.get("stage", 1)
    stage_data = STAGES[stage_num]

    elapsed    = int(time.time() - t.get("start_time", time.time()))
    mins, secs = divmod(elapsed, 60)
    hint_warn  = t.get("hint_used", 0) >= 3

    # 타임어택 모드 HUD
    if st.session_state.get('ta_mode'):
        ta_elapsed = int(time.time() - st.session_state.get('ta_start_time', time.time()))
        ta_m, ta_s = divmod(ta_elapsed, 60)
        st.markdown(f"""
        <div style='background:rgba(57,255,20,0.08);border:1px solid rgba(57,255,20,0.4);border-radius:8px;
          padding:6px 16px;margin-bottom:8px;display:flex;justify-content:space-between;
          font-family:monospace;font-size:0.82rem;'>
          <span style='color:#39ff14;font-weight:700;'>⚡ TIME ATTACK</span>
          <span style='color:#39ff14;'>총 경과: <b>{ta_m:02d}:{ta_s:02d}</b></span>
          <span style='color:#4a9a4a;'>STAGE {stage_num}/{len(STAGES)}</span>
        </div>
        """, unsafe_allow_html=True)

    col_l, col_r = st.columns([4, 1])
    with col_l:
        st.markdown(
            f"<div class='status-bar'>"
            f"<span class='status-item'>⏱ <span class='status-val'>{mins:02d}:{secs:02d}</span></span>"
            f"<span class='status-item'>CMD <span class='status-val'>{t.get('cmd_count', 0)}</span></span>"
            f"<span class='status-item'>HINT "
            f"<span class='{'status-warn' if hint_warn else 'status-val'}'>{t.get('hint_used', 0)}/3</span></span>"
            f"<span class='status-item' style='color:#ffd700;'>{stage_data['title']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_r:
        if st.button("◀ 목록", use_container_width=True, key="back_btn"):
            st.session_state.terminal["at_select"] = True
            st.rerun()

    # ── 터미널 출력 렌더링 ──────────────────────────────
    output_html = ""
    for line in t["output"]:
        safe = html.escape(line)

        if any(line.startswith(p) for p in [
            "✅", "  ✅", "  클리어", "  명령어", "  힌트 사용", "  평가", "  다음"
        ]):
            cls = "green"
        elif any(line.startswith(p) for p in [
            "❌", "║   ACCESS DENIED", "║  ACCESS DENIED"
        ]):
            cls = "red"
        elif line.startswith("[HINT]") or line.startswith("       "):
            cls = "hint"
        elif line.startswith("bash:"):
            cls = "red"
        elif any(line.startswith(p) for p in ["╔", "╚", "║", "═"]):
            cls = "cyan" if ("GRANTED" in line or "ACCESS" in line) else "border"
        elif line.startswith("─") or line.startswith("HYOMIN NETWORKS") \
                or line.startswith("Last login") or line.startswith("Connecting"):
            cls = "dim"
        elif line.startswith("[DIR]"):
            safe = f"📁 {html.escape(line[6:])}" if line.startswith("[DIR] ") else safe
            cls  = "dir"
        elif "Connection established" in line:
            cls = "green"
        elif line.startswith("  📋") or line.startswith("  ⚠️") or line.startswith("  `"):
            cls = "blue"
        elif line.startswith("find 결과") or line.startswith("검색 결과"):
            cls = "cyan"
        else:
            cls = ""

        output_html += f"<div class='term-line {cls}'>{safe}</div>"

    cwd_disp = t["cwd"]
    output_html += (
        f"<div class='term-line prompt'>"
        f"<span class='term-prompt-user'>ghost@hyomin</span>"
        f"<span style='color:#b8ffb8;'>:</span>"
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
        <div class='term-title'>
          ghost@hyomin-secure — {html.escape(cwd_disp)} — STAGE {stage_num}/{len(STAGES)}
        </div>
      </div>
      <div class='term-body' id='term-scroll'>{output_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── 입력창 (클리어 전) ──────────────────────────────
    if not t.get("solved", False):
        # ✅ [UX 개선] chat_input으로 Enter 키 즉시 제출 (진짜 터미널처럼)
        cmd_input = st.chat_input(
            placeholder="명령어 입력... (help=도움말 | hint=힌트 | ls | cat | cd | decode | unlock)",
            key=f"cmd_chat_{t.get('cmd_count', 0)}",
        )

        # 빠른 버튼 행
        col_h, col_c, col_hist = st.columns([1, 1, 2])
        with col_h:
            hint_clicked = st.button("💡 HINT", use_container_width=True, key="hint_btn")
        with col_c:
            if st.button("🗑️ CLR", use_container_width=True, key="clear_btn"):
                t["output"] = []
                st.rerun()
        with col_hist:
            if t["history"]:
                st.caption(f"↑ 최근: `{t['history'][-1]}`")

        if cmd_input and cmd_input.strip():
            add_output([f"ghost@hyomin:{t['cwd']}# {cmd_input}"])
            add_output(process_command(cmd_input, stage_data))
            t["history"].append(cmd_input)
            st.rerun()

        enter_clicked = False  # chat_input handles Enter natively

        if hint_clicked:
            add_output([f"ghost@hyomin:{t['cwd']}# hint"])
            add_output(process_command("hint", stage_data))
            st.rerun()

    else:
        # ── 클리어 화면 ─────────────────────────────────
        st.session_state.terminal_cleared.add(stage_num)

        # 스테이지 클리어 기록 저장
        elapsed_now = int(time.time() - t["start_time"])
        if "stage_records" not in st.session_state:
            st.session_state.stage_records = {}
        rec_key = str(stage_num)
        prev_best = st.session_state.stage_records.get(rec_key, {}).get("best_time", 999999)
        if elapsed_now < prev_best:
            st.session_state.stage_records[rec_key] = {
                "best_time": elapsed_now,
                "hints_used": t["hint_used"],
                "cmd_count": t["cmd_count"],
            }

        # DB에 클리어 진행상황 영구 저장 + 스테이지 클리어 보상 지급
        from utils.core import sync_user_data
        from utils.database import log_tx, atomic_add_cash

        uid = st.session_state.logged_in_user

        # 스테이지별 클리어 보상 (최초 클리어 시 1회만 지급)
        stage_reward_key = f"stage_reward_paid_{stage_num}"
        if stage_reward_key not in st.session_state:
            st.session_state[stage_reward_key] = True
            STAGE_REWARDS = {
                1: 5_000_000,   2: 10_000_000,  3: 15_000_000,
                4: 20_000_000,  5: 30_000_000,  6: 40_000_000,
                7: 50_000_000,  8: 70_000_000,  9: 100_000_000,
                10: 500_000_000,
            }
            # 힌트 미사용 보너스 (기본 보상의 50% 추가)
            base_reward    = STAGE_REWARDS.get(stage_num, 10_000_000)
            perfect_bonus  = base_reward // 2 if t["hint_used"] == 0 else 0
            total_reward   = base_reward + perfect_bonus
            atomic_add_cash(uid, total_reward)
            st.session_state.global_cash += total_reward
            bonus_str = f" (퍼펙트 보너스 +{perfect_bonus:,}원 포함!)" if perfect_bonus > 0 else ""
            log_tx(uid, "터미널", f"STAGE {stage_num} 클리어 보상{bonus_str}", total_reward)
            st.success(f"💰 STAGE {stage_num} 클리어 보상: +{total_reward:,}원{bonus_str}")

        sync_user_data()

        # 풍선은 한 번만
        balloon_key = f"balloon_done_{stage_num}"
        if balloon_key not in st.session_state:
            st.session_state[balloon_key] = True
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
          <div style='color:#5a9a5a; font-size:0.85rem; margin-top:10px;'>
            클리어 시간: <span style='color:#39ff14;font-weight:700;'>{int((time.time() - t["start_time"])//60):02d}:{int((time.time() - t["start_time"])%60):02d}</span>
            &nbsp;|&nbsp; 사용 힌트: {t['hint_used']}개
            &nbsp;|&nbsp; 명령어: {t['cmd_count']}개
          </div>
          <div style='color:#2a5c2a; font-size:0.78rem; margin-top:8px;'>
            진행: {len(st.session_state.terminal_cleared)}/{len(STAGES)} 스테이지 완료
          </div>
          {'<div style="color:#ffd700; font-size:1rem; margin-top:12px; letter-spacing:2px; text-shadow:0 0 15px rgba(255,215,0,0.6);">🏆 힌트 미사용 클리어! PERFECT HACK!</div>' if t["hint_used"] == 0 else ''}
        </div>
        """, unsafe_allow_html=True)

        # 전체 클리어 체크
        if len(st.session_state.terminal_cleared) == len(STAGES):
            st.balloons()
            # 전체 클리어 특별 보상 (최초 1회)
            if "terminal_full_clear_rewarded" not in st.session_state:
                st.session_state.terminal_full_clear_rewarded = True
                from utils.core import sync_user_data, claim_hidden_title
                from utils.database import log_tx, atomic_add_cash
                uid = st.session_state.logged_in_user
                full_clear_cash = 1_000_000_000  # 10억
                atomic_add_cash(uid, full_clear_cash)
                st.session_state.global_cash += full_clear_cash
                log_tx(uid, "터미널", "THE TERMINAL 전체 클리어 보상", full_clear_cash)
                claim_hidden_title("terminal_full_clear", "💻 [전설] 효민 네트웍스의 해커")
                sync_user_data()
                st.success("🏆 전체 클리어 보상: +1,000,000,000원 & 칭호 [효민 네트웍스의 해커] 획득!")
            st.markdown("""
            <div style='background:linear-gradient(135deg,#1a1000,#2a1800);border:2px solid #ffd700;
                        border-radius:10px;padding:20px;text-align:center;margin-bottom:14px;
                        box-shadow:0 0 40px rgba(255,215,0,0.3);font-family:monospace;'>
              <div style='color:#ffd700;font-size:1.4rem;font-weight:900;letter-spacing:4px;
                          text-shadow:0 0 20px rgba(255,215,0,0.8);'>
                🏆 ALL STAGES CLEARED 🏆
              </div>
              <div style='color:#b8860b;font-size:0.85rem;margin-top:10px;'>
                당신은 효민 네트웍스의 모든 비밀을 해독했습니다.<br>
                진정한 해커 — 창조자에게 도달했습니다.
              </div>
            </div>
            """, unsafe_allow_html=True)

        col_sel, col_next = st.columns(2)
        with col_sel:
            if st.button("◀ 스테이지 목록", use_container_width=True, key="to_list"):
                st.session_state.pop('ta_mode', None)
                st.session_state.terminal["at_select"] = True
                st.rerun()
        with col_next:
            next_s = stage_num + 1
            if next_s in STAGES:
                # 타임어택 모드: 자동 다음 스테이지 진행 버튼
                ta_label = f"⚡ [TA] STAGE {next_s} 즉시 돌입 →" if st.session_state.get('ta_mode') else f"▶ STAGE {next_s} 도전 →"
                if st.button(ta_label, use_container_width=True, type="primary", key="next_stage"):
                    if st.session_state.get('ta_mode'):
                        st.session_state['ta_stage'] = next_s
                    init_terminal(next_s)
                    ns = STAGES[next_s]
                    ta_hud = f"  ⏱ 타임어택 경과: {int((time.time()-st.session_state.get('ta_start_time',time.time()))//60):02d}:{int((time.time()-st.session_state.get('ta_start_time',time.time()))%60):02d}" if st.session_state.get('ta_mode') else ""
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
                        ta_hud,
                        "",
                        "  `help` 명령어 목록   `hint` 힌트 보기",
                        "─" * 44,
                    ]
                    st.session_state.terminal["at_select"] = False
                    st.rerun()
            else:
                # 타임어택 최종 클리어 처리
                if st.session_state.get('ta_mode'):
                    ta_total = time.time() - st.session_state.get('ta_start_time', time.time())
                    tm, ts = divmod(int(ta_total), 60)
                    prev_best = st.session_state.get('ta_best_time', 0)
                    is_new_record = (prev_best == 0 or ta_total < prev_best)
                    if is_new_record:
                        st.session_state['ta_best_time'] = ta_total
                    st.markdown(f"""
                    <div style='text-align:center;padding:16px;background:linear-gradient(135deg,rgba(57,255,20,0.15),rgba(0,212,255,0.1));
                      border:2px solid #39ff14;border-radius:12px;margin-bottom:12px;font-family:monospace;'>
                      <div style='color:#39ff14;font-size:1.2rem;font-weight:900;letter-spacing:3px;'>⏱ TIME ATTACK CLEAR!</div>
                      <div style='color:#00ff88;font-size:2rem;font-weight:900;margin:8px 0;'>{tm:02d}:{ts:02d}</div>
                      {'<div style="color:#ffd700;font-size:0.9rem;">🏅 NEW RECORD!</div>' if is_new_record else f'<div style="color:#4a9a4a;font-size:0.85rem;">이전 기록: {int(prev_best//60):02d}:{int(prev_best%60):02d}</div>'}
                    </div>
                    """, unsafe_allow_html=True)
                    st.session_state.pop('ta_mode', None)
                    if st.button("↩ 타이틀로", use_container_width=True, key="ta_done"):
                        st.session_state.terminal["at_select"] = True
                        st.rerun()
                else:
                    st.markdown("""
                    <div style='
                      color:#ffd700; font-family:monospace; text-align:center;
                      padding:14px; border:1px solid #ffd700; border-radius:6px;
                      font-size:1rem; letter-spacing:2px;
                    '>
                      🏆 10 STAGES COMPLETE<br>
                      <span style='font-size:0.8rem; color:#a07000;'>
                        당신은 진짜 해커다.
                      </span>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown(TERMINAL_JS, unsafe_allow_html=True)
