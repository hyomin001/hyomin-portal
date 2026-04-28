# pages/oran_analyzer.py
# ============================================================
#  O-RAN Fronthaul IQ Analyzer — 독립 비밀 패널 (admin 전용)
#  project_a~e 와 동일한 구조의 standalone page_view
# ============================================================
import streamlit as st
import numpy as np
import math
import io
import time
import struct
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional


# ── 보안 가드 ────────────────────────────────────────────────
def render():
    if st.session_state.get('logged_in_user') != 'admin':
        st.error("⛔ 접근 권한이 없습니다.")
        st.stop()

    # ── CSS ──────────────────────────────────────────────────
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@700;900&family=Inter:wght@400;500;600&display=swap');
:root {
  --bg:    #07090f;
  --bg2:   #0b0f1a;
  --bg3:   #0f1628;
  --line:  rgba(0,212,255,0.12);
  --cyan:  #00d4ff;
  --green: #00ff88;
  --gold:  #ffd700;
  --red:   #ff3355;
  --purple:#9d8bff;
  --text:  #d0ddf5;
  --muted: #5a6e90;
}
.oran-title {
  font-family:'Orbitron',monospace; font-size:1.6rem; font-weight:900; letter-spacing:4px;
  background:linear-gradient(90deg,#00d4ff,#9d8bff,#00ff88); -webkit-background-clip:text;
  -webkit-text-fill-color:transparent; margin:0 0 4px;
}
.oran-sub { color:var(--muted); font-size:0.82rem; font-family:'Inter',sans-serif; letter-spacing:0.5px; }
.oran-header {
  background:linear-gradient(135deg,rgba(0,212,255,0.06),rgba(157,139,255,0.05));
  border:1px solid rgba(0,212,255,0.18); border-radius:14px;
  padding:20px 26px; margin-bottom:24px; display:flex; align-items:center; gap:18px;
}
.stat-pill {
  background:var(--bg2); border:1px solid var(--line);
  border-radius:10px; padding:14px 18px; text-align:center;
}
.stat-pill .val {
  font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700;
  color:var(--cyan);
}
.stat-pill .val.g { color:var(--green); }
.stat-pill .val.o { color:var(--gold); }
.stat-pill .val.p { color:var(--purple); }
.stat-pill .val.r { color:var(--red); }
.stat-pill .lbl { color:var(--muted); font-size:0.7rem; letter-spacing:1px; margin-top:4px; text-transform:uppercase; }
.pwr-card {
  background:var(--bg2); border:1px solid var(--line); border-radius:12px;
  padding:16px 20px; font-family:'JetBrains Mono',monospace;
}
.pwr-card .pwr-label { color:var(--muted); font-size:0.72rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px; }
.pwr-card .pwr-val { font-size:1.5rem; font-weight:700; }
.pwr-card .pwr-hint { color:var(--muted); font-size:0.73rem; margin-top:4px; }
.diag-row {
  background:var(--bg2); border:1px solid var(--line);
  border-radius:10px; padding:14px 18px; margin:8px 0;
  font-family:'JetBrains Mono',monospace; font-size:0.85rem;
}
.diag-row .diag-label { color:var(--muted); font-size:0.72rem; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px; }
.badge-ok  { display:inline-block; background:rgba(0,255,136,0.1); color:#00ff88 !important;
  border:1px solid rgba(0,255,136,0.35); border-radius:5px; padding:2px 10px; font-size:0.75rem; font-weight:700; }
.badge-ng  { display:inline-block; background:rgba(255,51,85,0.1); color:#ff3355 !important;
  border:1px solid rgba(255,51,85,0.35); border-radius:5px; padding:2px 10px; font-size:0.75rem; font-weight:700; }
.badge-info { display:inline-block; background:rgba(0,212,255,0.1); color:#00d4ff !important;
  border:1px solid rgba(0,212,255,0.3); border-radius:5px; padding:2px 10px; font-size:0.75rem; font-weight:700; }
.help-block {
  background:rgba(157,139,255,0.06); border-left:3px solid var(--purple);
  border-radius:0 10px 10px 0; padding:14px 18px; margin:10px 0;
  font-size:0.88rem; color:var(--text); line-height:1.7;
  font-family:'Inter',sans-serif;
}
.help-block code {
  background:rgba(0,212,255,0.12); color:var(--cyan); padding:1px 6px;
  border-radius:4px; font-family:'JetBrains Mono',monospace; font-size:0.82rem;
}
.seg-block {
  background:var(--bg2); border:1px solid var(--line); border-radius:10px;
  padding:14px 16px; font-family:'JetBrains Mono',monospace; font-size:0.83rem;
}
.seg-block .seg-title { color:var(--muted); font-size:0.7rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; }
.dl-card {
  background:var(--bg2); border:1px solid var(--line); border-radius:12px;
  padding:20px; margin:8px 0;
}
.dl-card h4 { color:var(--cyan) !important; margin:0 0 8px; font-size:0.95rem; font-family:'JetBrains Mono',monospace; }
.dl-card p { color:var(--muted); font-size:0.82rem; margin:0 0 12px; }
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class='oran-header'>
  <div style='font-size:2.2rem;'>📡</div>
  <div>
    <div class='oran-title'>O-RAN IQ ANALYZER</div>
    <div class='oran-sub'>5G Fronthaul PCAP 신호 분석 · Power / Timing / Spectrum / Constellation · Admin Only</div>
  </div>
</div>
""", unsafe_allow_html=True)

    # ── 탭 구성 ──────────────────────────────────────────────
    TAB_NAMES = ["⚙️ 설정 & 실행", "📊 분석 결과", "📈 시각화", "💾 데이터 출력", "🔍 PCAP 진단기", "❓ 도움말"]
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(TAB_NAMES)

    # ══════════════════════════════════════════════════════════
    # TAB 1 — 설정 & 실행
    # ══════════════════════════════════════════════════════════
    with tab1:
        st.markdown("##### 📁 PCAP 파일 업로드")
        uploaded = st.file_uploader(
            "`.pcap` 또는 `.pcapng` 파일",
            type=["pcap", "pcapng"],
            help="Wireshark 등으로 캡처한 O-RAN Fronthaul eCPRI 패킷 파일 (pcapng 블록 포맷)"
        )

        st.markdown("---")
        st.markdown("##### ⚙️ 신호 파라미터")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**📶 RF 설정**")
            BW       = st.selectbox("대역폭 (MHz)", [5,10,15,20,25,40,80,100], index=1,
                                    help="캡처 당시의 5G NR 시스템 대역폭")
            u        = st.selectbox("Numerology (μ)", [0,1,2],
                                    format_func=lambda x: f"μ={x}  SCS={[15,30,60][x]}kHz  Nslt={2**x}",
                                    help="5G NR Numerology: μ=0(15kHz), 1(30kHz), 2(60kHz)")
            Bitwidth = st.number_input("BFP Bitwidth", min_value=1, max_value=16, value=9, step=1,
                                       help="BFP 압축 시 I/Q 샘플 당 비트 수 (보통 9~12)")

        with col2:
            st.markdown("**🗜️ 압축 & 전송**")
            Comp      = st.selectbox("압축 방식 (Comp)", [1,0],
                                     format_func=lambda x: "1 = BFP (Block Floating Point)" if x==1 else "0 = 비압축 (Raw IQ)",
                                     help="O-RAN 7.2x C-Plane / U-Plane 압축 방식")
            udCompHdr = st.selectbox("udCompHdr 유무", [0,1],
                                     format_func=lambda x: f"{'있음 (벤더 헤더 포함)' if x else '없음 (표준)'}",
                                     help="U-Plane 데이터 내 udCompHdr 바이트 포함 여부 (벤더 구현마다 다름)")
            ONLY      = st.selectbox("방향 필터 (ONLY)", [0,1,2,3],
                                     format_func=lambda x: ["0 = 전체 (UL+DL)","1 = DL only","2 = UL only","3 = 카운팅만 (IQ 추출 없음)"][x],
                                     index=2,
                                     help="dat_dir 비트 기준 필터링: 0=UL, 1=DL")

        with col3:
            st.markdown("**🔍 필터 & 기타**")
            eAxCIds_str   = st.text_input("eAxC ID (hex)", value="0x0001",
                                          help="추출 대상 안테나 ID (hex). 예: 0x0001, 0x0301")
            Naxc          = st.number_input("안테나 수 (Naxc)", min_value=1, max_value=16, value=4,
                                            help="시스템 안테나 포트 수 (현재 파싱 로직에서 참조용)")
            allow_mac_str = st.text_input("MAC 필터", value="ffffffffffff",
                                          help="허용 MAC 주소 (src/dst). ffffffffffff = 전체 허용. 쉼표로 복수 입력")

        st.markdown("---")
        st.markdown("##### 🧮 추가 옵션")
        opt_c1, opt_c2 = st.columns(2)
        with opt_c1:
            cvt_time = st.checkbox("⏳ IFFT 시간도메인 변환 (cvt_time)",
                                   help="UL IQ 버퍼에 IFFT를 적용하여 시간축 신호로 변환 (계산 시간 증가)")
        with opt_c2:
            show_timing = st.checkbox("⏱️ 타이밍 분석 포함",
                                      value=True,
                                      help="패킷 간격 (μs) 평균/최대/최소/Jitter 및 CP-UP 딜레이 계산")

        st.markdown("---")
        run_btn = st.button("🚀 분석 실행", use_container_width=True, type="primary",
                            disabled=(uploaded is None))

        if uploaded is None:
            st.info("⬆️ 먼저 PCAP 파일을 업로드해주세요.")
        else:
            st.caption(f"📄 업로드됨: `{uploaded.name}`  ({uploaded.size:,} bytes)")

        if run_btn and uploaded is not None:
            try:
                eAxCIds = int(eAxCIds_str.strip(), 16)
            except Exception:
                st.error("eAxC ID 형식 오류. 예: 0x0001"); st.stop()
            allow_mac = [m.strip().lower() for m in allow_mac_str.split(",")]

            with st.spinner("🔄 PCAP 파싱 중..."):
                result = _run_analysis(
                    uploaded.read(), BW, u, Bitwidth, Comp, udCompHdr,
                    ONLY, eAxCIds, allow_mac, Naxc, cvt_time, show_timing
                )

            st.session_state['oran_result'] = result
            st.session_state['oran_params'] = dict(
                BW=BW, u=u, Bitwidth=Bitwidth, Comp=Comp, udCompHdr=udCompHdr,
                ONLY=ONLY, eAxCIds=eAxCIds, Naxc=Naxc, cvt_time=cvt_time
            )
            st.success(f"✅ 파싱 완료! ({result['elapsed']:.3f}초) — '분석 결과' 탭에서 확인하세요.")

    # ══════════════════════════════════════════════════════════
    # TAB 2 — 분석 결과
    # ══════════════════════════════════════════════════════════
    with tab2:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ **'설정 & 분석 실행'** 탭에서 파일을 업로드하고 분석을 실행하세요.")
            st.stop()

        r = st.session_state['oran_result']
        p = st.session_state['oran_params']
        ecpri_list = r['ecpri_list']
        ptp_list   = r['ptp_list']
        ULu_buf    = r['ULu_buf']
        DLu_buf    = r['DLu_buf']
        det_pwr_ul = r['det_pwr_ul']
        Bitwidth   = p['Bitwidth']

        # ── 패킷 요약 ─────────────────────────────────────────
        st.markdown("#### 📦 패킷 요약")
        uplane_n = sum(1 for x in ecpri_list if x.msg_type == 0)
        cplane_n = sum(1 for x in ecpri_list if x.msg_type == 2)
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1: st.markdown(f"<div class='stat-pill'><div class='val'>{r['PB_num']}</div><div class='lbl'>총 패킷</div></div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='stat-pill'><div class='val g'>{len(ecpri_list)}</div><div class='lbl'>eCPRI</div></div>", unsafe_allow_html=True)
        with m3: st.markdown(f"<div class='stat-pill'><div class='val'>{uplane_n}</div><div class='lbl'>U-Plane</div></div>", unsafe_allow_html=True)
        with m4: st.markdown(f"<div class='stat-pill'><div class='val o'>{cplane_n}</div><div class='lbl'>C-Plane</div></div>", unsafe_allow_html=True)
        with m5: st.markdown(f"<div class='stat-pill'><div class='val p'>{len(ptp_list)}</div><div class='lbl'>PTP</div></div>", unsafe_allow_html=True)
        with m6: st.markdown(f"<div class='stat-pill'><div class='val r'>{r.get('tcp_count',0)}</div><div class='lbl'>TCP/IP</div></div>", unsafe_allow_html=True)

        # ── eAxC / Frame 정보 ─────────────────────────────────
        st.markdown("#### 🔑 eAxC ID & Frame 정보")
        eaxc_ids    = sorted(set(x.eaxc_id for x in ecpri_list if x.eaxc_id is not None))
        frame_ids   = sorted(set(x.frame_id for x in ecpri_list if x.frame_id is not None))
        fc = r.get('frame_counter', {})
        ea1, ea2, ea3 = st.columns(3)
        with ea1:
            st.markdown(f"""<div class='seg-block'><div class='seg-title'>검출된 eAxC ID</div>
{', '.join(f'<span style="color:#00d4ff">{hex(x)}</span>' for x in eaxc_ids) or '없음'}</div>""", unsafe_allow_html=True)
        with ea2:
            st.markdown(f"""<div class='seg-block'><div class='seg-title'>Frame ID 범위</div>
<span style='color:#00ff88'>{frame_ids[0] if frame_ids else '-'}</span> ~
<span style='color:#00ff88'>{frame_ids[-1] if frame_ids else '-'}</span>
<span style='color:#5a6e90'> ({len(frame_ids)}개)</span></div>""", unsafe_allow_html=True)
        with ea3:
            top_frames = sorted(fc.items(), key=lambda x: -x[1])[:5]
            top_txt = " ".join(f"<span style='color:#ffd700'>F{k}:{v}</span>" for k, v in top_frames)
            st.markdown(f"<div class='seg-block'><div class='seg-title'>Frame ID별 패킷 수 (상위 5)</div>{top_txt or '없음'}</div>", unsafe_allow_html=True)

        # ── IQ 버퍼 ──────────────────────────────────────────
        st.markdown("#### 🧮 IQ 버퍼 채움 상태")
        bc1, bc2 = st.columns(2)
        with bc1:
            ul_nz = int(np.count_nonzero(ULu_buf))
            ul_rt = ul_nz / max(ULu_buf.size, 1) * 100
            st.markdown(f"""<div class='stat-pill' style='text-align:left;padding:18px;'>
<div class='lbl'>UL IQ 버퍼</div>
<div class='val g' style='font-size:1.8rem;'>{ul_rt:.1f}%</div>
<div style='color:#5a6e90;font-size:0.78rem;margin-top:4px;'>{ul_nz:,} / {ULu_buf.size:,} RE &nbsp;|&nbsp; shape {ULu_buf.shape}</div>
</div>""", unsafe_allow_html=True)
        with bc2:
            dl_nz = int(np.count_nonzero(DLu_buf))
            dl_rt = dl_nz / max(DLu_buf.size, 1) * 100
            st.markdown(f"""<div class='stat-pill' style='text-align:left;padding:18px;'>
<div class='lbl'>DL IQ 버퍼</div>
<div class='val' style='font-size:1.8rem;'>{dl_rt:.1f}%</div>
<div style='color:#5a6e90;font-size:0.78rem;margin-top:4px;'>{dl_nz:,} / {DLu_buf.size:,} RE &nbsp;|&nbsp; shape {DLu_buf.shape}</div>
</div>""", unsafe_allow_html=True)

        # ── 파워 분석 ─────────────────────────────────────────
        st.markdown("#### 📊 파워 분석 결과")
        with st.expander("ℹ️ Full Scale 기준 설명", expanded=False):
            st.markdown(f"""<div class='help-block'>
<b>• QAM 기준 (2^{int(round(math.log2((2**(Bitwidth-1)*2**15)**2)))})</b><br>
&nbsp;&nbsp;<code>full_scale = (2^(Bitwidth-1) × 2^15)²</code><br>
&nbsp;&nbsp;BFP 복원 후 I/Q 각 성분 최대 진폭의 제곱합. QAM 성상도 최대 반경 기준. <b>물리적으로 가장 정확한 기준</b>.<br><br>
<b>• Bit 기준 (2^{int(round(math.log2((2**(Bitwidth-1)*2**15)**2*2)))})</b><br>
&nbsp;&nbsp;<code>full_scale_bit = full_scale_qam × 2</code><br>
&nbsp;&nbsp;I와 Q 동시 최대치를 기준으로 한 power. QAM 대비 3 dB 낮게 나옴.<br><br>
<b>• 레거시 2^47 기준</b><br>
&nbsp;&nbsp;기존 스크립트에서 사용하던 고정 기준값. Bitwidth나 스케일과 무관한 절대 기준.
</div>""", unsafe_allow_html=True)

        valid_symbols = np.where(det_pwr_ul > 0)[0]
        empty_symbols = np.where(det_pwr_ul == 0)[0]

        if len(valid_symbols) > 0:
            full_scale_qam = float((2**(Bitwidth-1) * 2**15)**2)
            full_scale_bit = full_scale_qam * 2.0
            fse_qam = int(round(math.log2(full_scale_qam)))
            fse_bit = int(round(math.log2(full_scale_bit)))
            mean_pwr = float(np.mean(det_pwr_ul[valid_symbols]))
            pwr_qam  = 10 * math.log10(mean_pwr / full_scale_qam)
            pwr_bit  = 10 * math.log10(mean_pwr / full_scale_bit)
            pwr_47   = 10 * math.log10(mean_pwr / 2**47)
            pwr_per_prb_qam = pwr_qam  # mean_pwr is already per-RE average

            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                st.markdown(f"""<div class='pwr-card'>
<div class='pwr-label'>Power per RE — QAM 기준 2^{fse_qam}</div>
<div class='pwr-val' style='color:#00ff88;'>{pwr_qam:.4f} <span style='font-size:1rem;'>dBFS</span></div>
<div class='pwr-hint'>물리적 정답 · 성상도 최대 반경 기준</div>
</div>""", unsafe_allow_html=True)
            with pc2:
                st.markdown(f"""<div class='pwr-card'>
<div class='pwr-label'>Power per RE — Bit 기준 2^{fse_bit}</div>
<div class='pwr-val' style='color:#00d4ff;'>{pwr_bit:.4f} <span style='font-size:1rem;'>dBFS</span></div>
<div class='pwr-hint'>I/Q 합산 최대치 기준 (QAM -3dB)</div>
</div>""", unsafe_allow_html=True)
            with pc3:
                st.markdown(f"""<div class='pwr-card'>
<div class='pwr-label'>Power per RE — 레거시 2^47</div>
<div class='pwr-val' style='color:#ffd700;'>{pwr_47:.4f} <span style='font-size:1rem;'>dBFS</span></div>
<div class='pwr-hint'>기존 스크립트 고정 기준값</div>
</div>""", unsafe_allow_html=True)

            # ── 심볼 점유 ─────────────────────────────────────
            st.markdown("#### 🗓️ 심볼 점유 현황")
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"""<div class='seg-block'>
<div class='seg-title'>🟢 데이터 있는 심볼 ({len(valid_symbols)}개)</div>
<span style='color:#00ff88;'>{_group_consecutive(valid_symbols)}</span>
</div>""", unsafe_allow_html=True)
            with sc2:
                empty_txt = _group_consecutive(empty_symbols) if len(empty_symbols) > 0 else "없음 (전부 채워짐)"
                clr = "#ff3355" if len(empty_symbols) > 0 else "#00ff88"
                st.markdown(f"""<div class='seg-block'>
<div class='seg-title'>🔴 비어있는 심볼 ({len(empty_symbols)}개)</div>
<span style='color:{clr};'>{empty_txt}</span>
</div>""", unsafe_allow_html=True)

            # ── PRB 분포 ──────────────────────────────────────
            st.markdown("#### 📡 PRB별 파워 분포")
            Nprb = ULu_buf.shape[0] // 12
            if Nprb > 0 and ULu_buf.shape[0] % 12 == 0:
                prb_pwr_sc = np.mean(np.abs(ULu_buf)**2, axis=1)
                prb_avg    = prb_pwr_sc.reshape(Nprb, 12).mean(axis=1)
                valid_prbs = np.where(prb_avg > 0)[0]
                empty_prbs = np.where(prb_avg == 0)[0]

                pp1, pp2 = st.columns(2)
                with pp1:
                    st.markdown(f"""<div class='seg-block'>
<div class='seg-title'>🟢 데이터 있는 PRB ({len(valid_prbs)} / {Nprb}개)</div>
<span style='color:#00ff88;'>{_group_consecutive(valid_prbs)}</span>
</div>""", unsafe_allow_html=True)
                with pp2:
                    ep_txt = _group_consecutive(empty_prbs) if len(empty_prbs) > 0 else "없음"
                    st.markdown(f"""<div class='seg-block'>
<div class='seg-title'>🔴 비어있는 PRB ({len(empty_prbs)}개)</div>
<span style='color:#ff3355;'>{ep_txt}</span>
</div>""", unsafe_allow_html=True)

                if len(valid_prbs) > 0:
                    st.markdown("**구간별 평균 파워 (PRB 세그먼트):**")
                    seg_starts, seg_ends = _get_segments(valid_prbs)
                    for s, e in zip(seg_starts, seg_ends):
                        seg_pwr = float(np.mean(prb_avg[s:e+1]))
                        pq = 10*math.log10(seg_pwr/full_scale_qam) if seg_pwr > 0 else -999
                        pb = 10*math.log10(seg_pwr/full_scale_bit) if seg_pwr > 0 else -999
                        st.markdown(f"""<div class='diag-row'>
<span style='color:#00d4ff;'>PRB {s}~{e}</span> &nbsp;·&nbsp;
<span style='color:#00ff88;'>{pq:.2f} dBFS</span> (QAM 2^{fse_qam}) &nbsp;/&nbsp;
<span style='color:#ffd700;'>{pb:.2f} dBFS</span> (Bit 2^{fse_bit})
</div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ 데이터가 있는 심볼이 없습니다. 'PCAP 진단기' 탭을 확인하세요.")

        # ── 타이밍 분석 ──────────────────────────────────────
        intervals_us = r.get('intervals_us', np.array([]))
        if len(intervals_us) > 0:
            st.markdown("#### ⏱️ 타이밍 분석")
            all_pb_times = r.get('all_pb_times', [])
            total_time_ms = (all_pb_times[-1] - all_pb_times[0]) / 1000.0 if len(all_pb_times) > 1 else 0

            with st.expander("ℹ️ 타이밍 분석 설명", expanded=False):
                st.markdown("""<div class='help-block'>
pcapng EPB(Enhanced Packet Block) 타임스탬프 기반 분석입니다.<br>
기본 단위는 <b>μs (마이크로초)</b>이며, Jitter = 표준편차 σ로 정의합니다.<br>
CP-UP 딜레이 = C-Plane 수신 후 동일 (FrameID, eAxCID, SymID) U-Plane 수신까지의 시간입니다.
</div>""", unsafe_allow_html=True)

            t1, t2, t3, t4, t5 = st.columns(5)
            with t1: st.markdown(f"<div class='stat-pill'><div class='val'>{float(np.mean(intervals_us)):.1f}</div><div class='lbl'>평균 간격 μs</div></div>", unsafe_allow_html=True)
            with t2: st.markdown(f"<div class='stat-pill'><div class='val r'>{float(np.max(intervals_us)):.1f}</div><div class='lbl'>최대 간격 μs</div></div>", unsafe_allow_html=True)
            with t3: st.markdown(f"<div class='stat-pill'><div class='val g'>{float(np.min(intervals_us)):.1f}</div><div class='lbl'>최소 간격 μs</div></div>", unsafe_allow_html=True)
            with t4: st.markdown(f"<div class='stat-pill'><div class='val p'>{float(np.std(intervals_us)):.1f}</div><div class='lbl'>Jitter (σ) μs</div></div>", unsafe_allow_html=True)
            with t5: st.markdown(f"<div class='stat-pill'><div class='val o'>{total_time_ms:.2f}</div><div class='lbl'>캡처 총 시간 ms</div></div>", unsafe_allow_html=True)

            cp_up_delays = r.get('cp_up_delays', [])
            if cp_up_delays:
                delays_arr = np.array(cp_up_delays, dtype=np.float64)
                d1, d2, d3 = st.columns(3)
                with d1: st.markdown(f"<div class='stat-pill'><div class='val'>{float(np.mean(delays_arr)):.1f}</div><div class='lbl'>CP→UP 평균 딜레이 μs</div></div>", unsafe_allow_html=True)
                with d2: st.markdown(f"<div class='stat-pill'><div class='val r'>{float(np.max(delays_arr)):.1f}</div><div class='lbl'>CP→UP 최대 딜레이 μs</div></div>", unsafe_allow_html=True)
                with d3: st.markdown(f"<div class='stat-pill'><div class='val g'>{float(np.min(delays_arr)):.1f}</div><div class='lbl'>CP→UP 최소 딜레이 μs</div></div>", unsafe_allow_html=True)

        # ── PTP 상세 ─────────────────────────────────────────
        if ptp_list:
            st.markdown("#### 🕐 PTP 패킷 상세")
            ptp_with_ts = [p for p in ptp_list if p.timestamp_s > 0]
            if ptp_with_ts:
                ptp_tbl = ""
                for i, pp in enumerate(ptp_with_ts[:8]):
                    ts_str = f"{pp.timestamp_s}.{pp.timestamp_ns:09d}"
                    ptp_tbl += f"<div class='diag-row'><span style='color:#5a6e90;'>#{pp.packet_id}</span> &nbsp; Timestamp: <span style='color:#00d4ff;'>{ts_str} s</span></div>"
                if len(ptp_with_ts) > 8:
                    ptp_tbl += f"<div style='color:#5a6e90;font-size:0.78rem;padding:4px 8px;'>… 외 {len(ptp_with_ts)-8}개</div>"
                st.markdown(ptp_tbl, unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='diag-row'>PTP 패킷 {len(ptp_list)}개 발견 · Sync/Follow-Up 타임스탬프 없음</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 3 — 시각화
    # ══════════════════════════════════════════════════════════
    with tab3:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ 먼저 분석을 실행하세요."); st.stop()

        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        r = st.session_state['oran_result']
        p = st.session_state['oran_params']
        ULu_buf    = r['ULu_buf']
        det_pwr_ul = r['det_pwr_ul']
        Bitwidth   = p['Bitwidth']

        _PLOT_BG   = '#07090f'
        _PLOT_BG2  = '#0b0f1a'
        _TICK_CLR  = '#5a6e90'
        _GRID_CLR  = '#111a2e'
        _CYAN      = '#00d4ff'
        _GREEN     = '#00ff88'
        _GOLD      = '#ffd700'
        _RED       = '#ff3355'
        _PURPLE    = '#9d8bff'

        def _style_ax(ax, title='', xlabel='', ylabel=''):
            ax.set_facecolor(_PLOT_BG2)
            ax.tick_params(colors=_TICK_CLR, labelsize=8)
            ax.xaxis.label.set_color(_TICK_CLR); ax.yaxis.label.set_color(_TICK_CLR)
            ax.title.set_color(_CYAN); ax.set_title(title, fontsize=10, pad=8)
            if xlabel: ax.set_xlabel(xlabel, fontsize=8)
            if ylabel: ax.set_ylabel(ylabel, fontsize=8)
            ax.grid(True, color=_GRID_CLR, linewidth=0.5, linestyle='--')
            for spine in ax.spines.values():
                spine.set_edgecolor('#1a2440')

        full_scale_qam = float((2**(Bitwidth-1) * 2**15)**2)

        valid_symbols = np.where(det_pwr_ul > 0)[0]

        # ── 1. 심볼별 파워 추이 ───────────────────────────────
        st.markdown("##### 📉 심볼별 파워 추이 (UL)")
        if len(valid_symbols) > 0:
            fig, ax = plt.subplots(figsize=(12, 3.5), facecolor=_PLOT_BG)
            pwr_dBFS = np.where(det_pwr_ul > 0,
                                10*np.log10(np.where(det_pwr_ul > 0, det_pwr_ul, 1) / full_scale_qam),
                                np.nan)
            ax.plot(pwr_dBFS, color=_GREEN, linewidth=0.9, alpha=0.9)
            ax.fill_between(range(len(pwr_dBFS)), pwr_dBFS, np.nanmin(pwr_dBFS)-5,
                            color=_GREEN, alpha=0.08)
            _style_ax(ax, 'UL Power per Symbol (QAM Full Scale)', 'Symbol Index', 'Power (dBFS)')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("데이터 없음")

        # ── 2. IQ Heatmap ────────────────────────────────────
        st.markdown("##### 🌡️ UL IQ Heatmap (서브캐리어 × 심볼)")
        with st.expander("ℹ️ Heatmap 설명", expanded=False):
            st.markdown("""<div class='help-block'>
각 픽셀 = |I + jQ| 크기 (선형). X축 = 심볼 인덱스 (10ms 프레임 내),
Y축 = 서브캐리어 인덱스 (PRB×12). 밝을수록 강한 신호.
Heatmap에서 빈 줄 = Guard Band, 빈 열 = 비어있는 심볼.
</div>""", unsafe_allow_html=True)
        if np.count_nonzero(ULu_buf) > 0:
            mag = np.abs(ULu_buf).astype(np.float32)
            # 다운샘플링 (너무 크면)
            max_sc, max_sym = 512, 512
            step_sc  = max(1, mag.shape[0]//max_sc)
            step_sym = max(1, mag.shape[1]//max_sym)
            mag_ds   = mag[::step_sc, ::step_sym]
            fig, ax = plt.subplots(figsize=(12, 4), facecolor=_PLOT_BG)
            im = ax.imshow(mag_ds, aspect='auto', origin='lower',
                           cmap='viridis', interpolation='nearest')
            plt.colorbar(im, ax=ax, label='|IQ| magnitude', shrink=0.9,
                         format='%.0f').ax.yaxis.label.set_color(_TICK_CLR)
            _style_ax(ax, 'UL IQ Heatmap', 'Symbol Index', 'Subcarrier Index')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("UL 버퍼가 비어있습니다.")

        # ── 3. PRB 막대그래프 ────────────────────────────────
        st.markdown("##### 📊 PRB별 평균 파워 (dBFS)")
        Nprb = ULu_buf.shape[0] // 12
        if Nprb > 0 and np.count_nonzero(ULu_buf) > 0:
            prb_pwr_sc = np.mean(np.abs(ULu_buf)**2, axis=1)
            prb_avg    = prb_pwr_sc.reshape(Nprb, 12).mean(axis=1)
            prb_dBFS   = np.where(prb_avg > 0,
                                  10*np.log10(np.where(prb_avg > 0, prb_avg, 1) / full_scale_qam),
                                  np.nan)
            fig, ax = plt.subplots(figsize=(12, 3.5), facecolor=_PLOT_BG)
            colors = [_GREEN if not np.isnan(v) else _RED for v in prb_dBFS]
            ax.bar(range(Nprb), np.nan_to_num(prb_dBFS, nan=np.nanmin(prb_dBFS)-5),
                   color=colors, width=0.85, alpha=0.85)
            _style_ax(ax, 'PRB Average Power (QAM Full Scale)', 'PRB Index', 'Power (dBFS)')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)
        else:
            st.warning("PRB 데이터 없음")

        # ── 4. Constellation ─────────────────────────────────
        st.markdown("##### 🌐 Constellation Diagram")
        with st.expander("ℹ️ Constellation 설명", expanded=False):
            st.markdown("""<div class='help-block'>
선택된 심볼 인덱스의 전체 서브캐리어 I/Q 값을 산점도로 표시합니다.
이상적인 신호는 각 QAM 포인트에 타이트하게 모여야 합니다.
퍼져있으면 EVM(Error Vector Magnitude)이 높은 것입니다.
</div>""", unsafe_allow_html=True)

        if len(valid_symbols) > 0:
            sym_idx = st.slider("심볼 인덱스 선택", int(valid_symbols[0]), int(valid_symbols[-1]),
                                int(valid_symbols[0]), key="const_sym")
            if sym_idx < ULu_buf.shape[1]:
                iq_col = ULu_buf[:, sym_idx]
                if np.count_nonzero(iq_col) > 0:
                    fig, ax = plt.subplots(figsize=(5, 5), facecolor=_PLOT_BG)
                    ax.scatter(iq_col.real, iq_col.imag, s=2, c=_CYAN, alpha=0.5)
                    ax.axhline(0, color=_GRID_CLR, linewidth=0.8)
                    ax.axvline(0, color=_GRID_CLR, linewidth=0.8)
                    _style_ax(ax, f'Constellation  (sym={sym_idx})', 'I (Real)', 'Q (Imag)')
                    ax.set_aspect('equal', 'box')
                    plt.tight_layout()
                    st.pyplot(fig); plt.close(fig)
                else:
                    st.warning(f"심볼 {sym_idx}에 데이터 없음")
        else:
            st.warning("유효 심볼 없음")

        # ── 5. 스펙트럼 (PRB 파워 스펙트럼) ──────────────────
        st.markdown("##### 📻 PRB 파워 스펙트럼 (서브캐리어별)")
        if np.count_nonzero(ULu_buf) > 0:
            sc_pwr = np.mean(np.abs(ULu_buf)**2, axis=1)
            sc_dBFS = np.where(sc_pwr > 0,
                               10*np.log10(np.where(sc_pwr>0, sc_pwr, 1)/full_scale_qam),
                               np.nan)
            fig, ax = plt.subplots(figsize=(12, 3.5), facecolor=_PLOT_BG)
            ax.plot(sc_dBFS, color=_PURPLE, linewidth=0.7, alpha=0.9)
            ax.fill_between(range(len(sc_dBFS)), sc_dBFS, np.nanmin(sc_dBFS)-5,
                            color=_PURPLE, alpha=0.1)
            _style_ax(ax, 'Subcarrier Power Spectrum', 'Subcarrier Index', 'Power (dBFS)')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

        # ── 6. 타이밍 히스토그램 ─────────────────────────────
        intervals_us = r.get('intervals_us', np.array([]))
        if len(intervals_us) > 10:
            st.markdown("##### ⏱️ 패킷 간격 분포 (μs)")
            fig, ax = plt.subplots(figsize=(10, 3), facecolor=_PLOT_BG)
            clip_max = np.percentile(intervals_us, 99)
            clipped  = intervals_us[intervals_us <= clip_max]
            ax.hist(clipped, bins=80, color=_GOLD, alpha=0.75, edgecolor='none')
            _style_ax(ax, 'Packet Interval Distribution (99th percentile)', 'Interval (μs)', 'Count')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

        # ── 7. IFFT 시간도메인 ────────────────────────────────
        cvt_time_data = r.get('cvt_time_data')
        if cvt_time_data is not None:
            st.markdown("##### 🌊 IFFT 시간도메인 신호")
            with st.expander("ℹ️ IFFT 설명", expanded=False):
                st.markdown("""<div class='help-block'>
서브캐리어 축에 IFFT를 적용하여 시간도메인으로 변환한 UL 신호입니다.
X축 = 시간 샘플 인덱스, Y축 = 복소 포락선 크기 |s(t)|.
OFDM CP 구조, 시간도메인 누설, 지연 스프레드 등을 확인할 수 있습니다.
</div>""", unsafe_allow_html=True)
            td_mag = np.abs(cvt_time_data)
            td_mean = np.mean(td_mag, axis=1)
            fig, ax = plt.subplots(figsize=(12, 3.5), facecolor=_PLOT_BG)
            ax.plot(td_mean, color=_RED, linewidth=0.8, alpha=0.9)
            _style_ax(ax, 'IFFT Time Domain (avg across symbols)', 'Time Sample', '|s(t)|')
            plt.tight_layout()
            st.pyplot(fig); plt.close(fig)

    # ══════════════════════════════════════════════════════════
    # TAB 4 — 데이터 출력
    # ══════════════════════════════════════════════════════════
    with tab4:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ 먼저 분석을 실행하세요."); st.stop()

        r   = st.session_state['oran_result']
        ULu_buf    = r['ULu_buf']
        DLu_buf    = r['DLu_buf']
        det_pwr_ul = r['det_pwr_ul']

        st.markdown("##### 💾 분석 데이터 다운로드")
        st.markdown("분석 결과를 다양한 포맷으로 저장하세요. MATLAB 포맷은 scipy 설치 시 활성화됩니다.")

        dc1, dc2 = st.columns(2)

        with dc1:
            # NPY 파일들
            st.markdown("<div class='dl-card'><h4>📦 NumPy 배열 (.npy)</h4><p>numpy.load()로 바로 불러올 수 있는 바이너리 포맷</p>", unsafe_allow_html=True)
            for name, arr in [("ULu_buf", ULu_buf), ("DLu_buf", DLu_buf), ("det_pwr_ul", det_pwr_ul)]:
                buf = io.BytesIO()
                np.save(buf, arr)
                st.download_button(f"📥 {name}.npy  (shape={arr.shape})",
                                   buf.getvalue(), f"{name}.npy",
                                   "application/octet-stream", key=f"dl_npy_{name}")
            st.markdown("</div>", unsafe_allow_html=True)

            # IFFT NPY
            cvt_time_data = r.get('cvt_time_data')
            if cvt_time_data is not None:
                st.markdown("<div class='dl-card'><h4>🌊 IFFT 시간도메인 (.npy)</h4><p>IFFT 적용된 시간축 복소 배열</p>", unsafe_allow_html=True)
                buf = io.BytesIO()
                np.save(buf, cvt_time_data)
                st.download_button("📥 UL_time_domain.npy", buf.getvalue(),
                                   "UL_time_domain.npy", "application/octet-stream", key="dl_ifft")
                st.markdown("</div>", unsafe_allow_html=True)

        with dc2:
            # CSV
            st.markdown("<div class='dl-card'><h4>📄 CSV (I/Q 분리)</h4><p>Excel / pandas 에서 열 수 있는 텍스트 포맷</p>", unsafe_allow_html=True)
            for name, arr_part, color in [("UL_I", ULu_buf.real, "green"), ("UL_Q", ULu_buf.imag, "blue"),
                                          ("DL_I", DLu_buf.real, "gold"),  ("DL_Q", DLu_buf.imag, "orange")]:
                buf_s = io.StringIO()
                np.savetxt(buf_s, arr_part, delimiter=',', fmt='%.4f')
                st.download_button(f"📥 {name}.csv  (shape={arr_part.shape})",
                                   buf_s.getvalue().encode(), f"{name}.csv",
                                   "text/csv", key=f"dl_csv_{name}")
            st.markdown("</div>", unsafe_allow_html=True)

            # MATLAB
            st.markdown("<div class='dl-card'><h4>⚙️ MATLAB (.mat)</h4><p>scipy.io.savemat 포맷. MATLAB/Octave에서 load()로 사용</p>", unsafe_allow_html=True)
            try:
                import scipy.io
                mat_buf = io.BytesIO()
                # complex128로 변환 (MATLAB 호환)
                scipy.io.savemat(mat_buf, {
                    'ULu_buf':    ULu_buf.astype(np.complex128),
                    'DLu_buf':    DLu_buf.astype(np.complex128),
                    'det_pwr_ul': det_pwr_ul,
                })
                st.download_button("📥 oran_data.mat", mat_buf.getvalue(),
                                   "oran_data.mat", "application/octet-stream", key="dl_mat")
            except ImportError:
                st.caption("🔸 scipy 미설치 → MATLAB 출력 불가 (`pip install scipy`)")
            st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════
    # TAB 5 — PCAP 진단기
    # ══════════════════════════════════════════════════════════
    with tab5:
        if 'oran_result' not in st.session_state:
            st.info("⬅️ 먼저 분석을 실행하세요."); st.stop()

        r = st.session_state['oran_result']
        p = st.session_state['oran_params']
        ecpri_list = r['ecpri_list']
        ULu_buf    = r['ULu_buf']
        DLu_buf    = r['DLu_buf']
        eAxCIds    = p['eAxCIds']
        ONLY       = p['ONLY']

        st.markdown("#### 🔍 PCAP 진단기")
        st.caption("데이터가 비어있는 원인을 단계적으로 자동 분석합니다.")

        uplane_pkts = []; cplane_pkts = []; other_pkts = []
        actual_dirs = set(); actual_eaxc_ids = []; actual_frame_ids = []

        # ── STEP 1 ───────────────────────────────────────────
        st.markdown("---")
        st.markdown("**[1단계] eCPRI 포장지 존재 여부**")
        with st.expander("ℹ️ 이 단계 설명"):
            st.markdown("""<div class='help-block'>
O-RAN Fronthaul은 Ethernet 위에 eCPRI(enhanced Common Public Radio Interface) 프로토콜을 얹습니다.
EtherType <code>0xAEFE</code>가 없으면 이 파일은 Fronthaul 캡처가 아닙니다.
레시피 파일이나 IQ 샘플 파일은 이 단계에서 바로 실패합니다.
</div>""", unsafe_allow_html=True)

        if len(ecpri_list) == 0:
            st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;eCPRI 패킷이 없습니다. 레시피/웨이브폼 파일이거나 캡처가 안 된 파일입니다.", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='badge-ok'>✅ PASS</span> &nbsp;eCPRI 패킷 <b>{len(ecpri_list)}개</b> 발견.", unsafe_allow_html=True)

            # ── STEP 2 ─────────────────────────────────────────
            st.markdown("---")
            st.markdown("**[2단계] U-Plane / C-Plane 구성**")
            with st.expander("ℹ️ 이 단계 설명"):
                st.markdown("""<div class='help-block'>
<b>U-Plane (msg_type=0)</b>: IQ 데이터 실제 탑재. 없으면 신호가 흐르지 않은 것입니다.<br>
<b>C-Plane (msg_type=2)</b>: 제어 정보 (BW, 빔 등). C-Plane만 있고 U-Plane이 없으면
RRH와 BBU는 연결됐지만 I/Q 신호가 광케이블에 아직 흐르지 않은 상태입니다.
</div>""", unsafe_allow_html=True)

            uplane_pkts = [x for x in ecpri_list if x.msg_type == 0]
            cplane_pkts = [x for x in ecpri_list if x.msg_type == 2]
            other_pkts  = [x for x in ecpri_list if x.msg_type not in (0, 2)]

            s21, s22, s23 = st.columns(3)
            with s21: st.markdown(f"<div class='stat-pill'><div class='val g'>{len(uplane_pkts)}</div><div class='lbl'>U-Plane</div></div>", unsafe_allow_html=True)
            with s22: st.markdown(f"<div class='stat-pill'><div class='val o'>{len(cplane_pkts)}</div><div class='lbl'>C-Plane</div></div>", unsafe_allow_html=True)
            with s23: st.markdown(f"<div class='stat-pill'><div class='val'>{len(other_pkts)}</div><div class='lbl'>기타</div></div>", unsafe_allow_html=True)

            if len(uplane_pkts) == 0:
                st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;U-Plane 없음 — I/Q 데이터가 캡처되지 않았습니다.", unsafe_allow_html=True)
                if len(cplane_pkts) > 0:
                    st.warning("C-Plane(제어)만 존재합니다. I/Q 데이터는 실제 신호가 광케이블로 흐르는 순간에만 캡처됩니다.")
            else:
                st.markdown(f"<span class='badge-ok'>✅ PASS</span> &nbsp;U-Plane {len(uplane_pkts)}개 확인.", unsafe_allow_html=True)

                actual_eaxc_ids  = sorted(set(x.eaxc_id  for x in uplane_pkts if x.eaxc_id  is not None))
                actual_dirs      = set(x.dat_dir          for x in uplane_pkts if x.dat_dir  is not None)
                actual_frame_ids = sorted(set(x.frame_id  for x in uplane_pkts if x.frame_id is not None))

                # ── STEP 3 ───────────────────────────────────────
                st.markdown("---")
                st.markdown("**[3단계] 설정 오류 검사**")
                with st.expander("ℹ️ 이 단계 설명"):
                    st.markdown("""<div class='help-block'>
<b>3-A eAxC ID</b>: 특정 안테나/빔의 IQ만 추출. 잘못 설정하면 버퍼가 비게 됩니다.<br>
<b>3-B 방향 필터</b>: dat_dir 비트 (UL=0, DL=1). 업링크 파일에서 DL only 설정하면 아무것도 안 나옵니다.<br>
<b>3-C Frame ID</b>: 프레임 번호가 0~255 범위를 벗어나면 유효하지 않습니다.<br>
<b>3-D IQ 버퍼</b>: 위 설정이 모두 맞아야 버퍼가 채워집니다.
</div>""", unsafe_allow_html=True)

                # 3-A
                st.markdown(f"**3-A eAxC ID** &nbsp;— 설정값: `0x{eAxCIds:04X}` &nbsp;/ 파일 실제값: `{[hex(x) for x in actual_eaxc_ids]}`")
                if eAxCIds in actual_eaxc_ids:
                    st.markdown("<span class='badge-ok'>✅ PASS</span> &nbsp;eAxC ID 일치", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;eAxC ID 불일치! 파일 안의 ID로 변경 필요", unsafe_allow_html=True)
                    if actual_eaxc_ids:
                        st.code(f"eAxCIds = 0x{actual_eaxc_ids[0]:04X}  # ← 이 값으로 변경하세요")

                # 3-B
                only_names = {0:"전체(UL+DL)", 1:"DL only", 2:"UL only", 3:"카운팅만"}
                dir_names  = {0:"UL", 1:"DL"}
                st.markdown(f"**3-B 방향 필터** &nbsp;— 설정값: `ONLY={ONLY} ({only_names.get(ONLY)})` &nbsp;/ 파일: `{[dir_names.get(d,str(d)) for d in sorted(actual_dirs)]}`")
                if   ONLY==1 and 1 not in actual_dirs:
                    st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;DL only인데 DL 패킷 없음", unsafe_allow_html=True)
                elif ONLY==2 and 0 not in actual_dirs:
                    st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;UL only인데 UL 패킷 없음", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='badge-ok'>✅ PASS</span> &nbsp;방향 설정 일치", unsafe_allow_html=True)

                # 3-C
                frameIds_range = set(range(0, 256))
                overlap = [fid for fid in actual_frame_ids if fid in frameIds_range]
                st.markdown(f"**3-C Frame ID** &nbsp;— 파일 실제: `{actual_frame_ids}`")
                if len(overlap) == 0:
                    st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;frameIds 범위(0~255) 안에 실제 Frame 없음", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='badge-ok'>✅ PASS</span> &nbsp;{len(overlap)}개 Frame ID 범위 내 확인", unsafe_allow_html=True)

                # 3-D
                ul_nz = int(np.count_nonzero(ULu_buf))
                dl_nz = int(np.count_nonzero(DLu_buf))
                st.markdown(f"**3-D IQ 버퍼** &nbsp;— UL: `{ul_nz}/{ULu_buf.size}` &nbsp;/ DL: `{dl_nz}/{DLu_buf.size}`")
                if ul_nz == 0 and dl_nz == 0:
                    st.markdown("<span class='badge-ng'>❌ FAIL</span> &nbsp;버퍼가 비어있습니다. 위 설정 오류를 먼저 수정하세요.", unsafe_allow_html=True)
                else:
                    fill_rate = max(ul_nz, dl_nz) / max(ULu_buf.size, 1) * 100
                    st.markdown(f"<span class='badge-ok'>✅ PASS</span> &nbsp;채움률 {fill_rate:.1f}%", unsafe_allow_html=True)

        # ── 최종 요약 ─────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### 📋 진단 요약")
        if len(ecpri_list) == 0:
            st.error("→ 레시피/웨이브폼 파일입니다. 실제 광케이블 캡처 파일을 사용하세요.")
        elif len(uplane_pkts) == 0:
            st.error("→ eCPRI는 있지만 U-Plane이 없습니다. I/Q는 실제 신호가 흐르는 순간에만 캡처됩니다.")
        else:
            issues = []
            if eAxCIds not in actual_eaxc_ids:                           issues.append(f"eAxCIds 설정 오류 (현재: 0x{eAxCIds:04X})")
            if (ONLY==1 and 1 not in actual_dirs) or (ONLY==2 and 0 not in actual_dirs): issues.append("ONLY 방향 설정 오류")
            if actual_frame_ids and not any(fid in range(0,256) for fid in actual_frame_ids): issues.append("frameIds 범위 오류")
            if not issues:
                if np.count_nonzero(ULu_buf) + np.count_nonzero(DLu_buf) == 0:
                    st.warning("→ 설정은 정상입니다. Bitwidth, Comp, udCompHdr 값을 벤더 스펙과 재확인하세요.")
                else:
                    st.success("→ ✅ 설정 이상 없음. 정상적으로 데이터가 추출되었습니다.")
            else:
                for issue in issues:
                    st.error(f"⚠️ {issue}")

    # ══════════════════════════════════════════════════════════
    # TAB 6 — 도움말
    # ══════════════════════════════════════════════════════════
    with tab6:
        st.markdown("#### ❓ O-RAN IQ Analyzer 도움말")

        with st.expander("📐 Power 계산 공식 완전 해설", expanded=True):
            st.markdown("""<div class='help-block'>
<b>BFP 복원 후 I/Q 샘플 값 범위</b><br>
Bitwidth=9 기준:
<ul>
<li>BFP 복원 후 I (또는 Q) 최대값 = <code>2^(Bitwidth-1) - 1 ≈ 2^(Bitwidth-1)</code></li>
<li>15비트 left-shift (× 2^15) → 내부 int16 표현</li>
<li>I max = <code>2^(Bitwidth-1) × 2^15</code>, Q max = 동일</li>
</ul>

<b>Full Scale (QAM 기준)</b><br>
<code>full_scale_qam = (2^(Bitwidth-1) × 2^15)²</code><br>
→ QAM 성상도 반경 최대의 제곱. I²+Q² 이므로 최대 파워 = I_max² (I=Q이면 실제 Imax²+Qmax²이지만<br>
&nbsp;&nbsp;&nbsp;코드에서 mean_pwr는 I²+Q² 합산이므로 full_scale도 I²+Q²로 잡으면 Imax²+Qmax² = 2×Iqam이 맞음)<br><br>

<b>Full Scale (Bit 기준)</b><br>
<code>full_scale_bit = full_scale_qam × 2</code><br>
→ I와 Q 동시 최대를 기준으로 잡은 값. QAM 대비 3 dB 낮게 나옴.<br><br>

<b>레거시 2^47</b><br>
<code>full_scale_legacy = 2^47</code><br>
→ 원본 스크립트에서 사용하던 고정값. Bitwidth=9, 15bit shift 기준 고정.<br>
→ <code>2^(Bitwidth-1) × 2^15 = 2^(8+15) = 2^23</code>, 제곱하면 <code>2^46</code>... 미묘하게 다름.<br>
→ 레거시 비교용으로만 참고하세요.
</div>""", unsafe_allow_html=True)

        with st.expander("🗜️ BFP(Block Floating Point) 압축 해설"):
            st.markdown("""<div class='help-block'>
O-RAN 7.2x에서 IQ 데이터를 압축하는 표준 방식입니다.<br><br>

<b>압축 과정 (Tx side)</b>
<ol>
<li>1 PRB = 12 서브캐리어. 각 I/Q 샘플을 묶어 블록 구성</li>
<li>블록 내 최대 절대값 찾기 → <code>exponent (4비트)</code> 계산</li>
<li>모든 샘플을 exponent만큼 right-shift → Bitwidth 비트로 양자화</li>
<li>전송: [exponent(1byte)] [compressed IQ × 12 × 2]</li>
</ol>

<b>복원 과정 (이 코드)</b>
<ol>
<li>exponent 바이트 읽기: <code>RB_expo = blk[:,0] & 0x0F</code></li>
<li>I/Q 비트 언팩: <code>np.unpackbits</code>로 개별 비트 추출</li>
<li>부호 비트 처리 (2의 보수): <code>si, sq</code> XOR 연산으로 sign extension</li>
<li>left-shift × 2^15 후 exponent로 스케일 복원</li>
</ol>

<b>주의</b>: <code>udCompHdr=1</code>이면 각 PRB 앞에 1바이트 udCompHdr이 추가됩니다.<br>
벤더마다 구현이 다르므로 무조건 스펙 확인 필요.
</div>""", unsafe_allow_html=True)

        with st.expander("🔑 eAxC ID 비트 구조"):
            st.markdown("""<div class='help-block'>
eAxC ID (extended Antenna Carrier ID)는 16비트 식별자입니다.<br><br>
<code>[15:14] DU Port ID (2비트) | [13:8] BandSector (6비트) | [7:6] CC (2비트) | [5:0] RU Port (6비트)</code><br><br>
예시:
<ul>
<li><code>0x0001</code> → DU Port=0, BandSector=0, CC=0, RU Port=1</li>
<li><code>0x0301</code> → DU Port=0, BandSector=0, CC=3, RU Port=1</li>
</ul>
파일 내 실제 eAxC ID와 설정값이 다르면 IQ 버퍼가 비게 됩니다.<br>
→ PCAP 진단기 3-A 단계에서 자동 확인됩니다.
</div>""", unsafe_allow_html=True)

        with st.expander("📡 5G NR 프레임 구조 & 심볼 인덱스"):
            st.markdown("""<div class='help-block'>
<code>nsym = (SFN × Nslt × 14) + (SLN × 14) + SYN</code><br><br>
<ul>
<li><b>SFN</b> (Subframe Number): 0~9, 1 서브프레임 = 1ms</li>
<li><b>SLN</b> (Slot Number in subframe): μ=0이면 0, μ=1이면 0~1, μ=2이면 0~3</li>
<li><b>SYN</b> (Symbol Number in slot): 0~13 (14 OFDM symbols per slot)</li>
<li><b>Nslt</b> = 2^μ (슬롯/서브프레임 수)</li>
<li><b>Nsym_frm</b> = 10 × Nslt × 14 (1 라디오 프레임의 총 심볼 수)</li>
</ul>
ULu_buf shape = (Nsc, Nsym_frm) = (Nprb×12, Nsym_frm)<br>
예: μ=0, BW=10MHz → Nprb=52, Nsc=624, Nsym_frm=140
</div>""", unsafe_allow_html=True)

        with st.expander("📦 pcapng 블록 구조 파서 설명"):
            st.markdown("""<div class='help-block'>
이 코드는 pcapng 파일을 직접 파싱합니다 (외부 라이브러리 미사용).<br><br>
<b>블록 타입</b>
<ul>
<li><code>0x0a0d0d0a</code> → <b>SHB</b> (Section Header Block): 파일 시작, BOM/바이트순서 결정</li>
<li><code>0x00000001</code> → <b>IDB</b> (Interface Description Block): 타임스탬프 해상도(if_tsresol) 포함</li>
<li><code>0x00000006</code> → <b>EPB</b> (Enhanced Packet Block): 실제 패킷 데이터</li>
<li>기타 → <b>UKP</b>: 알 수 없는 블록, 건너뜀</li>
</ul>
<b>BOM (Byte Order Magic)</b><br>
SHB+8에서 4바이트 읽기: <code>0x1A2B3C4D</code> = Big-Endian, <code>0x4D3C2B1A</code> = Little-Endian<br>
코드에서 <code>SHB_BOM[0]==77</code>(= 0x4D) 이면 Little-Endian 처리.
</div>""", unsafe_allow_html=True)

        with st.expander("⌨️ 원본 스크립트 사용 가이드 (Console)"):
            st.markdown("""<div class='help-block'>
원본 Python 스크립트 실행 예시:
<pre style='background:#0b0f1a;padding:12px;border-radius:8px;font-size:0.82rem;color:#00ff88;border:1px solid #1a2440;'>
python oran_iq_parser.py \\
  --pcap capture.pcapng \\
  --BW 10 --u 0 --Bitwidth 9 \\
  --Comp 1 --udCompHdr 0 \\
  --ONLY 2 \\
  --eAxCIds 0x0001 \\
  --Naxc 4 \\
  --cvt_time 0
</pre>

주요 파라미터 요약:
<ul>
<li><code>--ONLY 0</code> = UL+DL 전체 &nbsp;|&nbsp; <code>1</code> = DL only &nbsp;|&nbsp; <code>2</code> = UL only &nbsp;|&nbsp; <code>3</code> = 카운팅만</li>
<li><code>--cvt_time 1</code> = IFFT 시간도메인 변환 활성화 (느림)</li>
<li><code>--allow_mac</code> = 특정 MAC 주소 필터 (미지정 시 전체 허용)</li>
</ul>

출력 파일:
<ul>
<li><code>ULu_buf.npy</code>: UL IQ 복소 배열</li>
<li><code>UL_I.csv / UL_Q.csv</code>: I/Q 분리 CSV</li>
<li><code>oran_data.mat</code>: MATLAB 포맷 (scipy 필요)</li>
</ul>
</div>""", unsafe_allow_html=True)

        with st.expander("🐛 자주 발생하는 문제"):
            st.markdown("""<div class='help-block'>
<b>Q. 버퍼가 비어있어요 (채움률 0%)</b><br>
A. PCAP 진단기 탭에서 3단계 순서대로 확인하세요.<br>
가장 흔한 원인: eAxC ID 불일치, ONLY 방향 설정 오류.<br><br>

<b>Q. eAxC ID를 hex로 어떻게 찾나요?</b><br>
A. PCAP 진단기 3-A 단계에서 파일 내 실제 eAxC ID 목록을 자동 출력합니다.<br>
Wireshark에서도 eCPRI 레이어를 필터하여 확인 가능합니다.<br><br>

<b>Q. U-Plane은 있는데 파워가 이상해요</b><br>
A. Bitwidth 또는 Comp 설정을 벤더 스펙과 비교하세요.<br>
BFP Bitwidth가 다르면 복원값이 완전히 틀립니다.<br><br>

<b>Q. Constellation이 한 점에 몰려있어요</b><br>
A. QPSK 또는 낮은 변조 차수를 사용 중이거나,<br>
채널 상태가 좋지 않아 EVM이 높은 상태일 수 있습니다.<br><br>

<b>Q. CSV로 저장 시 숫자가 이상해요</b><br>
A. 복소수 배열이므로 I(Real)과 Q(Imag)를 각각 다른 파일에 저장합니다.<br>
UL_I.csv = 실수부, UL_Q.csv = 허수부.
</div>""", unsafe_allow_html=True)


# ================================================================
#  내부 데이터 클래스
# ================================================================
@dataclass
class _EcpriPkt:
    packet_id: int
    time: int
    dat_dir:  Optional[int] = None
    msg_type: Optional[int] = None
    frame_id: Optional[int] = None
    eaxc_id:  Optional[int] = None
    sym_num:  Optional[int] = None
    sym_id:   Optional[int] = None

@dataclass
class _PtpPkt:
    packet_id:   int
    time:        int
    info:        int = 0
    timestamp_s: int = 0
    timestamp_ns: int = 0


# ================================================================
#  헬퍼 함수
# ================================================================
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
            ends.append(int(valid_arr[i-1]))
            starts.append(int(valid_arr[i]))
    ends.append(int(valid_arr[-1]))
    return starts, ends


# ================================================================
#  파싱 엔진 (전체 기능 포함)
# ================================================================
def _run_analysis(raw_bytes, BW, u, Bitwidth, Comp, udCompHdr,
                  ONLY, eAxCIds, allow_mac, Naxc, cvt_time=False, show_timing=True):

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

    ULu_buf    = np.zeros((Nsc, Nsym_frm), dtype=np.complex64)
    DLu_buf    = np.zeros((Nsc, Nsym_frm), dtype=np.complex64)
    det_pwr_ul = np.zeros(Nsym_frm, dtype=np.float64)

    ecpri_list: List[_EcpriPkt] = []
    ptp_list:   List[_PtpPkt]   = []

    PB_num = 0; flag0 = 0
    tcp_count = 0
    all_pb_times = []
    Up_lnk_frameIds = 1023
    Dn_lnk_frameIds = 1023

    # CP-UP 딜레이 추적용
    cp_map = {}   # (frame_id, eaxc_id, sym_id) -> time
    up_map = {}   # same -> time

    SHB_BOM = np.zeros(4)
    SHB_BL  = 0
    if_tsresol = 6
    IDB_BTL = 0

    fr = raw_bytes
    total_len = len(fr)

    # ── 내부 함수 ─────────────────────────────────────────────
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
        if opt_code == 9:
            if_tsresol = fr[ptr+20]
        return ptr + IDB_BTL

    def _UKP(ptr):
        if SHB_BOM[0] == 77:
            btl = (fr[ptr+7]<<24)|(fr[ptr+6]<<16)|(fr[ptr+5]<<8)|fr[ptr+4]
        else:
            btl = (fr[ptr+4]<<24)|(fr[ptr+5]<<16)|(fr[ptr+6]<<8)|fr[ptr+7]
        return ptr + max(btl, 12)

    def _IQ_extract(OD, nsym, dat_dir, clear_mat):
        nonlocal ULu_buf, DLu_buf, det_pwr_ul, flag0
        lComp, lBitwidth = Comp, Bitwidth
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

        bits = np.unpackbits(np_iq, axis=1).reshape(ORAN_PRBuN, 12, lBitwidth * 2)
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
        flat  = iq_c.reshape(-1) * (2.0**np.repeat(RB_expo, 12)).astype(np.float32)

        ss = ORAN_PRBuS * 12
        se = ss + ORAN_PRBuN * 12
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
        SLN  = ((OD[6]&0x0f)<<1)|(OD[7]>>7)
        SYN  = OD[7]&0x3f
        nsym = (SFN*Nslt*14)+(SLN*14)+SYN
        ecpri_list[-1].frame_id = FN
        ecpri_list[-1].eaxc_id  = eaxc
        ecpri_list[-1].dat_dir  = ddir
        ecpri_list[-1].sym_id   = nsym

        if msg_type == 2:
            ecpri_list[-1].sym_num = OD[17]&0x0f
            key = (FN, eaxc, nsym)
            cp_map[key] = ecpri_list[-1].time
            return

        if not (0 <= FN <= 255): return
        if ONLY == 3: return
        if eaxc != eAxCIds: return

        # UP 타임 기록 (CP-UP 딜레이용)
        key = (FN, eaxc, nsym)
        up_map[key] = ecpri_list[-1].time

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
            OD2  = _IQ_extract(OD2, nsym, ddir, clear_mat)
            if clear_mat == 1: clear_mat = 0
            consumed = prev - len(OD2)
            pl2 -= consumed
            if consumed == 0: break

    def _PB(ptr):
        nonlocal PB_num, tcp_count
        PB_num += 1
        PB_HDR = 28

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

        all_pb_times.append(PB_TIME)
        PD = fr[ptr+PB_HDR : ptr+PB_HDR+PB_CPL]
        if len(PD) < 14:
            return ptr + PB_TL

        des_mac = PD[0:6].hex()
        src_mac = PD[6:12].hex()
        if allow_mac[0] != "ffffffffffff":
            if not any(m==des_mac or m==src_mac for m in allow_mac):
                return ptr + PB_TL

        etype = (PD[12]<<8)|PD[13]

        # ── eCPRI (VLAN tagged) ─────────────────────────────
        if etype == 0x8100 and len(PD) >= 18:
            inner = (PD[16]<<8)|PD[17]
            if inner == 0xAEFE and len(PD) >= 22:
                mt = PD[19]
                pl = (PD[20]<<8)|PD[21]
                ecpri_list.append(_EcpriPkt(PB_num, PB_TIME))
                ecpri_list[-1].msg_type = mt
                _ORAN(PD, mt, pl)
            # VLAN IP/TCP
            elif inner == 0x0800 and len(PD) >= 32:
                ip_proto = PD[23]
                if ip_proto == 6:
                    tcp_count += 1

        # ── PTP ────────────────────────────────────────────
        elif etype == 0x88F7:
            ptp_list.append(_PtpPkt(PB_num, PB_TIME))
            if len(PD) >= 58:
                msg_type_ptp = PD[14] & 0x0f
                if msg_type_ptp in (0, 8):   # Sync or Follow-Up
                    ts_s  = int.from_bytes(PD[48:54], 'big')
                    ts_ns = (PD[54]<<24)|(PD[55]<<16)|(PD[56]<<8)|PD[57]
                    ptp_list[-1].timestamp_s  = ts_s
                    ptp_list[-1].timestamp_ns = ts_ns

        # ── 일반 IP/TCP ────────────────────────────────────
        elif etype == 0x0800 and len(PD) >= 24:
            ip_proto = PD[23]
            if ip_proto == 6:
                tcp_count += 1

        return ptr + PB_TL

    # ── 메인 파싱 루프 ────────────────────────────────────────
    t0 = time.time()
    ptr = 0
    while total_len > ptr + 4:
        bk = (fr[ptr]<<24)|(fr[ptr+1]<<16)|(fr[ptr+2]<<8)|fr[ptr+3]
        if   bk == 0x0a0d0d0a: ptr = _SHB(ptr)
        elif bk == 0x01000000:  ptr = _IDB(ptr)
        elif bk == 0x06000000:  ptr = _PB(ptr)
        else:                   ptr = _UKP(ptr)

    # ── 후처리 ───────────────────────────────────────────────
    # 타이밍 분석
    times_arr    = np.array(all_pb_times, dtype=np.float64)
    intervals_us = np.diff(times_arr) if len(times_arr) > 1 else np.array([])

    # Frame ID별 카운터
    frame_counter = Counter(x.frame_id for x in ecpri_list if x.frame_id is not None)

    # CP-UP 딜레이
    cp_up_delays = []
    for key in up_map:
        if key in cp_map:
            delay = float(up_map[key] - cp_map[key])
            if abs(delay) < 1e9:   # 비현실적 값 제외
                cp_up_delays.append(delay)

    # IFFT 시간도메인 변환
    cvt_time_data = None
    if cvt_time and np.count_nonzero(ULu_buf) > 0:
        cvt_time_data = np.fft.ifft(ULu_buf, axis=0).astype(np.complex64)

    return dict(
        elapsed       = time.time() - t0,
        PB_num        = PB_num,
        ecpri_list    = ecpri_list,
        ptp_list      = ptp_list,
        ULu_buf       = ULu_buf,
        DLu_buf       = DLu_buf,
        det_pwr_ul    = det_pwr_ul,
        tcp_count     = tcp_count,
        all_pb_times  = all_pb_times,
        intervals_us  = intervals_us,
        frame_counter = dict(frame_counter),
        cp_up_delays  = cp_up_delays,
        cvt_time_data = cvt_time_data,
    )
