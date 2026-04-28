# pages/oran_analyzer.py
# ============================================================
#  O-RAN Fronthaul IQ Analyzer — HYOMIN PORTAL 전용 패널
#  admin 계정 전용 비밀 패널
# ============================================================
import streamlit as st
import numpy as np
import math
import io
import time
from dataclasses import dataclass
from typing import List

# ── 보안 가드 ────────────────────────────────────────────────
def render():
    if st.session_state.get('logged_in_user') != 'admin':
        st.error("⛔ 접근 권한이 없습니다.")
        st.stop()

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
<style>
.oran-header {
    background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,212,255,0.08));
    border: 1px solid rgba(0,255,136,0.3);
    border-radius: 16px; padding: 20px 28px; margin-bottom: 20px;
}
.oran-header h2 { color: #00ff88 !important; margin: 0 0 6px; font-family: 'Orbitron', monospace; }
.oran-header p  { color: #8899bb !important; margin: 0; font-size: 0.88rem; }
.result-box {
    background: rgba(10, 16, 32, 0.9);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 12px; padding: 18px 20px; margin: 10px 0;
    font-family: 'Courier New', monospace; font-size: 0.85rem;
}
.result-box .label { color: #8899bb; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; }
.result-box .value { color: #00d4ff !important; font-size: 1.4rem; font-weight: 900; }
.result-box .value.green { color: #00ff88 !important; }
.result-box .value.gold  { color: #ffd700 !important; }
.pass-badge { display:inline-block; background:rgba(0,255,136,0.15); color:#00ff88 !important;
    border:1px solid rgba(0,255,136,0.4); border-radius:6px; padding:2px 10px; font-size:0.78rem; font-weight:700; margin:2px; }
.fail-badge { display:inline-block; background:rgba(255,51,102,0.15); color:#ff3366 !important;
    border:1px solid rgba(255,51,102,0.4); border-radius:6px; padding:2px 10px; font-size:0.78rem; font-weight:700; margin:2px; }
.info-badge { display:inline-block; background:rgba(0,212,255,0.12); color:#00d4ff !important;
    border:1px solid rgba(0,212,255,0.3); border-radius:6px; padding:2px 10px; font-size:0.78rem; font-weight:700; margin:2px; }
.prb-row { padding: 8px 12px; border-radius: 8px; margin: 4px 0; font-size: 0.85rem;
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); }
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='oran-header'>
  <h2>📡 O-RAN IQ ANALYZER</h2>
  <p>PCAP 파일에서 IQ 데이터를 추출하고 파워를 분석하는 관리자 전용 신호 분석 패널입니다.</p>
</div>
""", unsafe_allow_html=True)

    # ── 탭 구성 ──────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["⚙️ 설정 & 분석 실행", "📊 분석 결과", "🔍 PCAP 진단기"])

    # ══════════════════════════════════════════════════════════
    # TAB 1 — 설정 & 실행
    # ══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("#### 📁 PCAP 파일 업로드")
        uploaded = st.file_uploader(
            "`.pcap` 또는 `.pcapng` 파일을 업로드하세요",
            type=["pcap", "pcapng"],
            help="Wireshark 등으로 캡처한 O-RAN Fronthaul 패킷 파일"
        )

        st.markdown("#### ⚙️ 신호 파라미터 설정")
        col1, col2, col3 = st.columns(3)
        with col1:
            BW       = st.selectbox("대역폭 (MHz)", [5, 10, 15, 20, 40, 80, 100], index=1)
            u        = st.selectbox("Numerology", [0, 1, 2],
                                    format_func=lambda x: f"{x} ({[15,30,60][x]}kHz)", index=0)
            Bitwidth = st.number_input("BFP Bitwidth", min_value=1, max_value=16, value=9, step=1)
        with col2:
            Comp     = st.selectbox("압축 방식", [1, 0], format_func=lambda x: "1=BFP" if x==1 else "0=비압축")
            udCompHdr= st.selectbox("udCompHdr", [0, 1], format_func=lambda x: f"{x}={'있음' if x else '없음'}")
            ONLY     = st.selectbox("방향 필터", [0, 1, 2, 3],
                                    format_func=lambda x: ["전체(UL+DL)","DL only","UL only","카운팅만"][x],
                                    index=2)
        with col3:
            eAxCIds_str = st.text_input("eAxC ID (hex)", value="0x0001",
                                        help="예: 0x0001, 0x0301")
            Naxc = st.number_input("안테나 수 (Naxc)", min_value=1, max_value=16, value=4)
            allow_mac_str = st.text_input("MAC 필터", value="ffffffffffff",
                                          help="ffffffffffff = 전체 허용")

        st.markdown("---")
        run_btn = st.button("🚀 분석 실행", use_container_width=True, type="primary",
                            disabled=(uploaded is None))

        if uploaded is None:
            st.info("⬆️ 먼저 PCAP 파일을 업로드해주세요.")

        # ── 분석 실행 ────────────────────────────────────────
        if run_btn and uploaded is not None:
            try:
                eAxCIds = int(eAxCIds_str, 16)
            except:
                st.error("eAxC ID 형식 오류. 예: 0x0001")
                st.stop()

            allow_mac = [m.strip().lower() for m in allow_mac_str.split(",")]

            with st.spinner("🔄 파싱 중..."):
                result = _run_analysis(
                    uploaded.read(), BW, u, Bitwidth, Comp, udCompHdr,
                    ONLY, eAxCIds, allow_mac, Naxc
                )

            st.session_state['oran_result'] = result
            st.session_state['oran_params'] = dict(
                BW=BW, u=u, Bitwidth=Bitwidth, Comp=Comp,
                ONLY=ONLY, eAxCIds=eAxCIds, Naxc=Naxc
            )
            st.success(f"✅ 파싱 완료! ({result['elapsed']:.3f}초)")
            st.info("👆 **'분석 결과'** 탭과 **'PCAP 진단기'** 탭에서 결과를 확인하세요.")

    # ══════════════════════════════════════════════════════════
    # TAB 2 — 분석 결과
    # ══════════════════════════════════════════════════════════
    with tab2:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ 먼저 **'설정 & 분석 실행'** 탭에서 파일을 업로드하고 분석을 실행하세요.")
            st.stop()

        r = st.session_state['oran_result']
        p = st.session_state['oran_params']

        # ── 기본 통계 ─────────────────────────────────────────
        st.markdown("#### 📦 파싱 결과 요약")
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown(f"<div class='result-box'><div class='label'>총 패킷</div><div class='value'>{r['PB_num']}</div></div>", unsafe_allow_html=True)
        with mc2:
            st.markdown(f"<div class='result-box'><div class='label'>eCPRI 패킷</div><div class='value green'>{len(r['ecpri_list'])}</div></div>", unsafe_allow_html=True)
        with mc3:
            st.markdown(f"<div class='result-box'><div class='label'>U-Plane</div><div class='value'>{sum(1 for x in r['ecpri_list'] if x.msg_type==0)}</div></div>", unsafe_allow_html=True)
        with mc4:
            st.markdown(f"<div class='result-box'><div class='label'>C-Plane</div><div class='value gold'>{sum(1 for x in r['ecpri_list'] if x.msg_type==2)}</div></div>", unsafe_allow_html=True)

        mc5, mc6, mc7 = st.columns(3)
        with mc5:
            st.markdown(f"<div class='result-box'><div class='label'>PTP 패킷</div><div class='value'>{len(r['ptp_list'])}</div></div>", unsafe_allow_html=True)
        with mc6:
            eaxc_ids = sorted(set(x.eaxc_id for x in r['ecpri_list'] if x.eaxc_id is not None))
            st.markdown(f"<div class='result-box'><div class='label'>검출 eAxC ID</div><div class='value' style='font-size:1rem;'>{[hex(x) for x in eaxc_ids]}</div></div>", unsafe_allow_html=True)
        with mc7:
            frame_ids = sorted(set(x.frame_id for x in r['ecpri_list'] if x.frame_id is not None))
            st.markdown(f"<div class='result-box'><div class='label'>Frame ID 범위</div><div class='value' style='font-size:1rem;'>{frame_ids[:5]}{'...' if len(frame_ids)>5 else ''}</div></div>", unsafe_allow_html=True)

        # ── IQ 버퍼 상태 ──────────────────────────────────────
        st.markdown("#### 🧮 IQ 버퍼 채움 상태")
        ULu_buf = r['ULu_buf']
        DLu_buf = r['DLu_buf']
        ul_filled = int(np.count_nonzero(ULu_buf))
        dl_filled = int(np.count_nonzero(DLu_buf))
        bc1, bc2 = st.columns(2)
        with bc1:
            ul_rate = ul_filled / max(ULu_buf.size, 1) * 100
            st.markdown(f"""<div class='result-box'>
<div class='label'>UL IQ 버퍼 채움률</div>
<div class='value green'>{ul_rate:.1f}%</div>
<div style='color:#8899bb;font-size:0.78rem;'>{ul_filled:,} / {ULu_buf.size:,} RE &nbsp;|&nbsp; shape {ULu_buf.shape}</div>
</div>""", unsafe_allow_html=True)
        with bc2:
            dl_rate = dl_filled / max(DLu_buf.size, 1) * 100
            st.markdown(f"""<div class='result-box'>
<div class='label'>DL IQ 버퍼 채움률</div>
<div class='value'>{dl_rate:.1f}%</div>
<div style='color:#8899bb;font-size:0.78rem;'>{dl_filled:,} / {DLu_buf.size:,} RE &nbsp;|&nbsp; shape {DLu_buf.shape}</div>
</div>""", unsafe_allow_html=True)

        # ── 파워 분석 ─────────────────────────────────────────
        det_pwr_ul = r['det_pwr_ul']
        Bitwidth   = p['Bitwidth']
        full_scale_qam = float((2**(Bitwidth-1) * 2**15)**2)
        full_scale_bit = full_scale_qam * 2.0
        fse_qam = int(round(math.log2(full_scale_qam)))
        fse_bit = int(round(math.log2(full_scale_bit)))

        valid_symbols = np.where(det_pwr_ul > 0)[0]
        empty_symbols = np.where(det_pwr_ul == 0)[0]

        st.markdown("#### 📊 파워 분석 결과")

        if len(valid_symbols) > 0:
            mean_pwr = float(np.mean(det_pwr_ul[valid_symbols]))
            pwr_qam  = 10 * math.log10(mean_pwr / full_scale_qam)
            pwr_bit  = 10 * math.log10(mean_pwr / full_scale_bit)
            pwr_47   = 10 * math.log10(mean_pwr / 2**47)

            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                st.markdown(f"""<div class='result-box'>
<div class='label'>Power per RE (QAM 기준 2^{fse_qam})</div>
<div class='value green'>{pwr_qam:.4f} dBFS</div>
<div style='color:#8899bb;font-size:0.75rem;'>물리적 정답 — 원 반경 최대치</div>
</div>""", unsafe_allow_html=True)
            with pc2:
                st.markdown(f"""<div class='result-box'>
<div class='label'>Power per RE (Bit 기준 2^{fse_bit})</div>
<div class='value'>{pwr_bit:.4f} dBFS</div>
<div style='color:#8899bb;font-size:0.75rem;'>I/Q 동시 최대치 기준</div>
</div>""", unsafe_allow_html=True)
            with pc3:
                st.markdown(f"""<div class='result-box'>
<div class='label'>Power per RE (원본 2^47 기준)</div>
<div class='value gold'>{pwr_47:.4f} dBFS</div>
<div style='color:#8899bb;font-size:0.75rem;'>기존 레거시 기준값</div>
</div>""", unsafe_allow_html=True)

            # ── 심볼 점유 현황 ─────────────────────────────────
            st.markdown("#### 🗓️ 심볼 점유 현황")
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"""<div class='result-box'>
<div class='label'>🟢 데이터 있는 심볼 (총 {len(valid_symbols)}개)</div>
<div style='color:#00ff88;font-size:0.9rem;margin-top:6px;'>{_group_consecutive(valid_symbols)}</div>
</div>""", unsafe_allow_html=True)
            with sc2:
                empty_txt = _group_consecutive(empty_symbols) if len(empty_symbols) > 0 else "없음 (전부 채워짐)"
                st.markdown(f"""<div class='result-box'>
<div class='label'>🔴 비어있는 심볼 (총 {len(empty_symbols)}개)</div>
<div style='color:#ff3366;font-size:0.9rem;margin-top:6px;'>{empty_txt}</div>
</div>""", unsafe_allow_html=True)

            # ── PRB 분포 ───────────────────────────────────────
            st.markdown("#### 📡 PRB별 파워 분포")
            Nprb = ULu_buf.shape[0] // 12
            if Nprb > 0 and ULu_buf.shape[0] % 12 == 0:
                prb_pwr_sc = np.mean(np.abs(ULu_buf)**2, axis=1)
                prb_avg    = prb_pwr_sc.reshape(Nprb, 12).mean(axis=1)
                valid_prbs = np.where(prb_avg > 0)[0]
                empty_prbs = np.where(prb_avg == 0)[0]

                pc1, pc2 = st.columns(2)
                with pc1:
                    st.markdown(f"""<div class='result-box'>
<div class='label'>🟢 데이터 있는 PRB (총 {len(valid_prbs)}개 / 전체 {Nprb}개)</div>
<div style='color:#00ff88;font-size:0.9rem;margin-top:6px;'>{_group_consecutive(valid_prbs)}</div>
</div>""", unsafe_allow_html=True)
                with pc2:
                    empty_prb_txt = _group_consecutive(empty_prbs) if len(empty_prbs) > 0 else "없음"
                    st.markdown(f"""<div class='result-box'>
<div class='label'>🔴 비어있는 PRB (총 {len(empty_prbs)}개)</div>
<div style='color:#ff3366;font-size:0.9rem;margin-top:6px;'>{empty_prb_txt}</div>
</div>""", unsafe_allow_html=True)

                # PRB 구간별 파워
                if len(valid_prbs) > 0:
                    seg_starts, seg_ends = _get_segments(valid_prbs)
                    st.markdown("**구간별 평균 파워:**")
                    for s, e in zip(seg_starts, seg_ends):
                        seg_pwr = float(np.mean(prb_avg[s:e+1]))
                        pq = 10*math.log10(seg_pwr/full_scale_qam) if seg_pwr > 0 else -999
                        pb = 10*math.log10(seg_pwr/full_scale_bit) if seg_pwr > 0 else -999
                        st.markdown(f"""<div class='prb-row'>
<span style='color:#00d4ff;'>PRB {s}~{e}</span>
&nbsp;&nbsp;→&nbsp;&nbsp;
<span style='color:#00ff88;'>{pq:.2f} dBFS</span> (QAM 2^{fse_qam})
&nbsp;/&nbsp;
<span style='color:#ffd700;'>{pb:.2f} dBFS</span> (Bit 2^{fse_bit})
</div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ 데이터가 있는 심볼이 없습니다. PCAP 진단기 탭을 확인하세요.")

    # ══════════════════════════════════════════════════════════
    # TAB 3 — PCAP 진단기
    # ══════════════════════════════════════════════════════════
    with tab3:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ 먼저 **'설정 & 분석 실행'** 탭에서 파일을 업로드하고 분석을 실행하세요.")
            st.stop()

        r = st.session_state['oran_result']
        p = st.session_state['oran_params']

        st.markdown("#### 🔍 PCAP 진단기 — 데이터가 비어있는 원인 분석")

        ecpri_list = r['ecpri_list']
        ULu_buf    = r['ULu_buf']
        DLu_buf    = r['DLu_buf']
        eAxCIds    = p['eAxCIds']
        ONLY       = p['ONLY']

        uplane_pkts = []; cplane_pkts = []; other_pkts = []
        actual_dirs = set(); actual_eaxc_ids = []; actual_frame_ids = []

        # ── 1단계 ─────────────────────────────────────────────
        st.markdown("---")
        st.markdown("**[1단계] eCPRI 포장지 존재 여부**")
        if len(ecpri_list) == 0:
            st.markdown("<span class='fail-badge'>❌ FAIL</span> eCPRI 패킷이 없습니다. 레시피/웨이브폼 파일이거나 캡처가 안 된 파일입니다.", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='pass-badge'>✅ PASS</span> eCPRI 패킷 <b>{len(ecpri_list)}개</b> 발견. 통신용 패킷 확인.", unsafe_allow_html=True)

            # ── 2단계 ──────────────────────────────────────────
            st.markdown("---")
            st.markdown("**[2단계] U-Plane / C-Plane 구성**")
            uplane_pkts = [p_ for p_ in ecpri_list if p_.msg_type == 0]
            cplane_pkts = [p_ for p_ in ecpri_list if p_.msg_type == 2]
            other_pkts  = [p_ for p_ in ecpri_list if p_.msg_type not in (0, 2)]

            d2c1, d2c2, d2c3 = st.columns(3)
            with d2c1:
                st.markdown(f"<div class='result-box'><div class='label'>U-Plane (IQ 데이터)</div><div class='value {'green' if len(uplane_pkts)>0 else ''}'>{len(uplane_pkts)}</div></div>", unsafe_allow_html=True)
            with d2c2:
                st.markdown(f"<div class='result-box'><div class='label'>C-Plane (제어)</div><div class='value gold'>{len(cplane_pkts)}</div></div>", unsafe_allow_html=True)
            with d2c3:
                st.markdown(f"<div class='result-box'><div class='label'>기타</div><div class='value'>{len(other_pkts)}</div></div>", unsafe_allow_html=True)

            if len(uplane_pkts) == 0:
                st.markdown("<span class='fail-badge'>❌ FAIL</span> U-Plane이 없습니다.", unsafe_allow_html=True)
                if len(cplane_pkts) > 0:
                    st.warning("C-Plane(제어)만 있습니다. I/Q 데이터는 실제 신호가 광케이블로 흐르는 순간에만 캡처됩니다.")
                else:
                    st.warning("알려진 msg_type이 없습니다. 특수 포맷을 의심하세요.")
            else:
                st.markdown(f"<span class='pass-badge'>✅ PASS</span> U-Plane {len(uplane_pkts)}개 확인.", unsafe_allow_html=True)

                actual_eaxc_ids  = sorted(set(p_.eaxc_id   for p_ in uplane_pkts if p_.eaxc_id   is not None))
                actual_dirs      = set(p_.dat_dir           for p_ in uplane_pkts if p_.dat_dir   is not None)
                actual_frame_ids = sorted(set(p_.frame_id   for p_ in uplane_pkts if p_.frame_id  is not None))
                frameIds         = np.arange(0, 256)

                # ── 3단계 ──────────────────────────────────────
                st.markdown("---")
                st.markdown("**[3단계] 설정 오류 검사**")

                # 3-A: eAxC ID
                st.markdown(f"**3-A eAxC ID** — 설정값: `0x{eAxCIds:04X}` / 파일 실제값: `{[hex(x) for x in actual_eaxc_ids]}`")
                if eAxCIds in actual_eaxc_ids:
                    st.markdown("<span class='pass-badge'>✅ PASS</span> eAxC ID 일치", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='fail-badge'>❌ FAIL</span> eAxC ID 불일치! 파일 안의 ID로 변경 필요", unsafe_allow_html=True)
                    if actual_eaxc_ids:
                        st.code(f"eAxCIds = 0x{actual_eaxc_ids[0]:04X}  # ← 이 값으로 변경")

                # 3-B: 방향 필터
                only_names = {0:"전체(UL+DL)", 1:"DL only", 2:"UL only", 3:"카운팅만"}
                dir_names  = {0:"UL", 1:"DL"}
                st.markdown(f"**3-B 방향 필터** — 설정값: `ONLY={ONLY}({only_names.get(ONLY)})` / 파일: `{[dir_names.get(d,str(d)) for d in sorted(actual_dirs)]}`")
                if ONLY == 1 and 1 not in actual_dirs:
                    st.markdown("<span class='fail-badge'>❌ FAIL</span> DL only인데 DL 패킷 없음", unsafe_allow_html=True)
                elif ONLY == 2 and 0 not in actual_dirs:
                    st.markdown("<span class='fail-badge'>❌ FAIL</span> UL only인데 UL 패킷 없음", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='pass-badge'>✅ PASS</span> 방향 설정 일치", unsafe_allow_html=True)

                # 3-C: Frame ID
                overlap = [fid for fid in actual_frame_ids if fid in frameIds]
                st.markdown(f"**3-C Frame ID** — 파일 실제: `{actual_frame_ids}`")
                if len(overlap) == 0:
                    st.markdown("<span class='fail-badge'>❌ FAIL</span> frameIds 범위 안에 실제 Frame 없음", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='pass-badge'>✅ PASS</span> {len(overlap)}개 Frame ID 범위 내 확인", unsafe_allow_html=True)

                # 3-D: 버퍼 채움
                ul_nz = int(np.count_nonzero(ULu_buf))
                dl_nz = int(np.count_nonzero(DLu_buf))
                st.markdown(f"**3-D IQ 버퍼** — UL: `{ul_nz}/{ULu_buf.size}` / DL: `{dl_nz}/{DLu_buf.size}`")
                if ul_nz == 0 and dl_nz == 0:
                    st.markdown("<span class='fail-badge'>❌ FAIL</span> 버퍼가 비어있습니다. 위 설정 오류를 먼저 수정하세요.", unsafe_allow_html=True)
                else:
                    fill_rate = max(ul_nz, dl_nz) / max(ULu_buf.size, 1) * 100
                    st.markdown(f"<span class='pass-badge'>✅ PASS</span> 채움률 {fill_rate:.1f}%", unsafe_allow_html=True)

        # ── 최종 요약 ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📋 진단 요약")
        if len(ecpri_list) == 0:
            st.error("→ 레시피/웨이브폼 파일입니다. 실제 광케이블 캡처 파일을 사용하세요.")
        elif len(uplane_pkts) == 0:
            st.error("→ eCPRI는 있지만 U-Plane이 없습니다. I/Q는 실제 신호가 흐르는 순간에만 캡처됩니다.")
        else:
            issues = []
            if eAxCIds not in actual_eaxc_ids:
                issues.append(f"eAxCIds 설정 오류 (현재: 0x{eAxCIds:04X})")
            if (ONLY==1 and 1 not in actual_dirs) or (ONLY==2 and 0 not in actual_dirs):
                issues.append("ONLY 방향 설정 오류")
            if len(uplane_pkts) > 0 and not any(fid in np.arange(0,256) for fid in actual_frame_ids):
                issues.append("frameIds 범위 오류")

            if not issues:
                if np.count_nonzero(ULu_buf) + np.count_nonzero(DLu_buf) == 0:
                    st.warning("→ 설정은 정상입니다. Bitwidth, Comp, udCompHdr 값을 벤더 스펙과 재확인하세요.")
                else:
                    st.success("→ ✅ 설정 이상 없음. 정상적으로 데이터가 추출되었습니다.")
            else:
                for issue in issues:
                    st.error(f"⚠️ {issue}")


# ================================================================
#  내부 파싱 엔진 (기존 코드 그대로 이식)
# ================================================================
@dataclass
class _EcpriPkt:
    packet_id: int; time: int
    dat_dir: int = None; msg_type: int = None
    frame_id: int = None; eaxc_id: int = None
    sym_num: int = None; sym_id: int = None

@dataclass
class _PtpPkt:
    packet_id: int; time: int
    info: int = 0; timestamp_s: int = 0; timestamp_ns: int = 0


def _group_consecutive(nums):
    if len(nums) == 0: return "(없음)"
    ranges, start, end = [], int(nums[0]), int(nums[0])
    for i in range(1, len(nums)):
        if int(nums[i]) == end + 1:
            end = int(nums[i])
        else:
            ranges.append(f"{start}~{end}" if start != end else str(start))
            start = end = int(nums[i])
    ranges.append(f"{start}~{end}" if start != end else str(start))
    return ", ".join(ranges)


def _get_segments(valid_arr):
    if len(valid_arr) == 0: return [], []
    starts, ends = [int(valid_arr[0])], []
    for i in range(1, len(valid_arr)):
        if int(valid_arr[i]) != int(valid_arr[i-1]) + 1:
            ends.append(int(valid_arr[i-1])); starts.append(int(valid_arr[i]))
    ends.append(int(valid_arr[-1]))
    return starts, ends


def _run_analysis(raw_bytes, BW, u, Bitwidth, Comp, udCompHdr, ONLY, eAxCIds, allow_mac, Naxc):
    import struct

    _prb_table = {
        (0,5):25,(0,10):52,(0,15):79,(0,20):106,(0,25):133,
        (1,10):24,(1,20):51,(1,40):106,(1,80):217,(1,100):273,
        (2,40):51,(2,80):107,(2,100):135,
    }
    if (u, BW) not in _prb_table:
        raise ValueError(f"지원하지 않는 BW/numerology: u={u}, BW={BW}MHz")

    Nprb     = _prb_table[(u, BW)]
    Nslt     = 2**u
    Nsc      = 12 * Nprb
    Nsym_frm = 10 * Nslt * 14

    ULu_buf = np.zeros((Nsc, Nsym_frm), dtype=np.complex64)
    DLu_buf = np.zeros((Nsc, Nsym_frm), dtype=np.complex64)
    det_pwr_ul = np.zeros(Nsym_frm, dtype=np.float64)

    ecpri_list: List[_EcpriPkt] = []
    ptp_list:   List[_PtpPkt]   = []
    PB_num = 0; flag0 = 0
    Up_lnk_frameIds = 1023; Dn_lnk_frameIds = 1023

    SHB_BOM = np.zeros(4); SHB_BL = 0
    if_tsresol = 6; IDB_BTL = 0

    fr = raw_bytes
    total_len = len(fr)

    # ── 파서 내부 함수 ────────────────────────────────────────
    def _SHB(ptr):
        nonlocal SHB_BOM, SHB_BL
        SHB_BOM = np.array([fr[ptr+8],fr[ptr+9],fr[ptr+10],fr[ptr+11]])
        if SHB_BOM[0] == 77:
            SHB_BL = (fr[ptr+7]<<24)|(fr[ptr+6]<<16)|(fr[ptr+5]<<8)|fr[ptr+4]
        else:
            SHB_BL = (fr[ptr+4]<<24)|(fr[ptr+5]<<16)|(fr[ptr+6]<<8)|fr[ptr+7]
        return ptr + SHB_BL

    def _IDB(ptr):
        nonlocal IDB_BTL, if_tsresol
        if SHB_BOM[0] == 77:
            IDB_BTL  = (fr[ptr+7]<<24)|(fr[ptr+6]<<16)|(fr[ptr+5]<<8)|fr[ptr+4]
            opt_code = (fr[ptr+17]<<8)|fr[ptr+16]
        else:
            IDB_BTL  = (fr[ptr+4]<<24)|(fr[ptr+5]<<16)|(fr[ptr+6]<<8)|fr[ptr+7]
            opt_code = (fr[ptr+16]<<8)|fr[ptr+17]
        if opt_code == 9: if_tsresol = fr[ptr+20]
        return ptr + IDB_BTL

    def _UKP(ptr):
        if SHB_BOM[0] == 77:
            btl = (fr[ptr+7]<<24)|(fr[ptr+6]<<16)|(fr[ptr+5]<<8)|fr[ptr+4]
        else:
            btl = (fr[ptr+4]<<24)|(fr[ptr+5]<<16)|(fr[ptr+6]<<8)|fr[ptr+7]
        return ptr + max(btl, 12)

    def _IQ_extract(OD, nsym, dat_dir, clear_mat):
        nonlocal ULu_buf, DLu_buf, det_pwr_ul, flag0
        lBW, lComp, lBitwidth = Bitwidth, Comp, Bitwidth
        if clear_mat == 1:
            if dat_dir == 0:
                tmp = np.mean(np.abs(ULu_buf)**2, axis=0)
                if flag0 == 1: det_pwr_ul = np.append(det_pwr_ul, tmp)
                else:           det_pwr_ul = tmp; flag0 = 1
                ULu_buf[:] = 0
            else:
                DLu_buf[:] = 0
        ORAN_PRBuS = ((OD[1] & 0x03) << 8) + OD[2]
        ORAN_PRBuN = OD[3] if OD[3] != 0 else 273
        local_udCompHdr = udCompHdr
        if local_udCompHdr == 1:
            lBitwidth = (OD[4] >> 4) or 9
            lComp     = OD[4] & 0x0f
            OD = OD[6:]
        else:
            OD = OD[4:]
        bpiq = int(12 * lBitwidth * 2 / 8)
        RB_expo = np.zeros(ORAN_PRBuN, dtype=np.uint16)
        if lComp == 1:
            stride = bpiq + 1
            total  = ORAN_PRBuN * stride
            blk    = np.frombuffer(OD[:total], dtype=np.uint8).reshape(ORAN_PRBuN, stride)
            RB_expo = (blk[:, 0] & 0x0f).astype(np.uint16)
            np_iq   = blk[:, 1:]
        else:
            total  = ORAN_PRBuN * bpiq
            np_iq  = np.frombuffer(OD[:total], dtype=np.uint8).reshape(ORAN_PRBuN, bpiq)
        bits  = np.unpackbits(np_iq, axis=1).reshape(ORAN_PRBuN, 12, lBitwidth*2)
        bi = bits[:,:,:lBitwidth]; bq = bits[:,:,lBitwidth:]
        si = bi[:,:,:1]; sq = bq[:,:,:1]
        ii = np.bitwise_xor(bi, np.broadcast_to(si, bi.shape))
        qi = np.bitwise_xor(bq, np.broadcast_to(sq, bq.shape))
        if lBitwidth > 8:
            sh = lBitwidth - 8
            di = (np.packbits(ii[:,:,:8],axis=-1).astype(np.int16)<<sh) + \
                 np.right_shift(np.packbits(ii[:,:,8:],axis=-1).astype(np.int16), 16-lBitwidth)
            dq = (np.packbits(qi[:,:,:8],axis=-1).astype(np.int16)<<sh) + \
                 np.right_shift(np.packbits(qi[:,:,8:],axis=-1).astype(np.int16), 16-lBitwidth)
            dec_i = di[:,:,0]; dec_q = dq[:,:,0]
        else:
            sh = lBitwidth - 8
            dec_i = (np.packbits(ii[:,:,:lBitwidth],axis=-1).astype(np.int16)<<sh)[:,:,0]
            dec_q = (np.packbits(qi[:,:,:lBitwidth],axis=-1).astype(np.int16)<<sh)[:,:,0]
        si2 = si[:,:,0]; sq2 = sq[:,:,0]
        dec_i = (dec_i + si2) * (-2*si2.astype(np.int16) + 1)
        dec_q = (dec_q + sq2) * (-2*sq2.astype(np.int16) + 1)
        iq_c  = (dec_i + 1j*dec_q).astype(np.complex64)
        flat  = iq_c.reshape(-1) * (2.0**np.repeat(RB_expo,12)).astype(np.float32)
        ss = ORAN_PRBuS*12; se = ss + ORAN_PRBuN*12
        if dat_dir == 1: DLu_buf[ss:se, nsym] = flat
        else:            ULu_buf[ss:se, nsym] = flat
        return OD[total:]

    def _ORAN(PD, msg_type, pl_size):
        nonlocal Up_lnk_frameIds, Dn_lnk_frameIds
        OD = PD[22:]
        eaxc  = (OD[0]<<8)|OD[1]
        ddir  = OD[4]>>7
        if ddir==1 and ONLY==2: return
        if ddir==0 and ONLY==1: return
        FN   = OD[5]; SFN  = OD[6]>>4
        SLN  = ((OD[6]&0x0f)<<1)|(OD[7]>>7); SYN = OD[7]&0x3f
        nsym = (SFN*Nslt*14)+(SLN*14)+SYN
        ecpri_list[-1].frame_id = FN
        ecpri_list[-1].eaxc_id  = eaxc
        ecpri_list[-1].dat_dir  = ddir
        ecpri_list[-1].sym_id   = nsym
        if msg_type == 2:
            ecpri_list[-1].sym_num = OD[17]&0x0f; return
        if not np.isin(FN, np.arange(0,256)): return
        if ONLY == 3: return
        if eaxc != eAxCIds: return
        clear_mat = 0
        if ddir == 0:
            if Up_lnk_frameIds == 1023: Up_lnk_frameIds = FN
            elif Up_lnk_frameIds != FN: clear_mat = 1
            Up_lnk_frameIds = FN
        else:
            if Dn_lnk_frameIds == 1023: Dn_lnk_frameIds = FN
            elif Dn_lnk_frameIds != FN: clear_mat = 1
            Dn_lnk_frameIds = FN
        OD2 = OD[8:]; pl2 = pl_size - 8
        while pl2 > 4:
            prev = len(OD2)
            OD2 = _IQ_extract(OD2, nsym, ddir, clear_mat)
            if clear_mat == 1: clear_mat = 0
            consumed = prev - len(OD2)
            pl2 -= consumed
            if consumed == 0: break

    def _PB(ptr):
        nonlocal PB_num
        PB_num += 1; PB_HDR = 28
        if SHB_BOM[0] == 77:
            PB_TL   = (fr[ptr+7]<<24)|(fr[ptr+6]<<16)|(fr[ptr+5]<<8)|fr[ptr+4]
            PB_CPL  = (fr[ptr+23]<<24)|(fr[ptr+22]<<16)|(fr[ptr+21]<<8)|fr[ptr+20]
            PB_TIME = ((fr[ptr+15]<<56)|(fr[ptr+14]<<48)|(fr[ptr+13]<<40)|(fr[ptr+12]<<32)|
                       (fr[ptr+19]<<24)|(fr[ptr+18]<<16)|(fr[ptr+17]<<8)|fr[ptr+16])
        else:
            PB_TL   = (fr[ptr+4]<<24)|(fr[ptr+5]<<16)|(fr[ptr+6]<<8)|fr[ptr+7]
            PB_CPL  = (fr[ptr+20]<<24)|(fr[ptr+21]<<16)|(fr[ptr+22]<<8)|fr[ptr+23]
            PB_TIME = ((fr[ptr+12]<<56)|(fr[ptr+13]<<48)|(fr[ptr+14]<<40)|(fr[ptr+15]<<32)|
                       (fr[ptr+16]<<24)|(fr[ptr+17]<<16)|(fr[ptr+18]<<8)|fr[ptr+19])
        PD = fr[ptr+PB_HDR : ptr+PB_HDR+PB_CPL]
        if len(PD) < 14: return ptr + PB_TL
        des_mac = PD[0:6].hex(); src_mac = PD[6:12].hex()
        if allow_mac[0] != "ffffffffffff":
            if not any(m==des_mac or m==src_mac for m in allow_mac):
                return ptr + PB_TL
        etype = (PD[12]<<8)|PD[13]
        if etype == 0x8100 and len(PD) >= 18:
            inner = (PD[16]<<8)|PD[17]
            if inner == 0xAEFE:
                mt = PD[19]; pl = (PD[20]<<8)|PD[21]
                ecpri_list.append(_EcpriPkt(PB_num, PB_TIME))
                ecpri_list[-1].msg_type = mt
                _ORAN(PD, mt, pl)
        elif etype == 0x88F7:
            ptp_list.append(_PtpPkt(PB_num, PB_TIME))
        return ptr + PB_TL

    # ── 메인 루프 ─────────────────────────────────────────────
    t0 = time.time()
    ptr = 0
    while total_len > ptr + 4:
        bk = (fr[ptr]<<24)|(fr[ptr+1]<<16)|(fr[ptr+2]<<8)|fr[ptr+3]
        if   bk == 0x0a0d0d0a: ptr = _SHB(ptr)
        elif bk == 0x01000000:  ptr = _IDB(ptr)
        elif bk == 0x06000000:  ptr = _PB(ptr)
        else:                   ptr = _UKP(ptr)

    return dict(
        elapsed=time.time()-t0,
        PB_num=PB_num,
        ecpri_list=ecpri_list,
        ptp_list=ptp_list,
        ULu_buf=ULu_buf,
        DLu_buf=DLu_buf,
        det_pwr_ul=det_pwr_ul,
    )
