import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스나이퍼 엘리트</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--green:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--purple:#c04fff;--orange:#ff7700;--bg:#04080a;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.07);}
html,body{width:100%;height:728px;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100%;height:728px;overflow:hidden;}
canvas{position:absolute;top:0;left:0;}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;padding:10px 14px;background:linear-gradient(180deg,rgba(0,0,0,.88)0%,transparent 100%);display:flex;align-items:flex-start;gap:8px;pointer-events:none;}
.hb{background:rgba(0,0,0,.48);border:1px solid var(--border);border-radius:9px;padding:4px 10px;text-align:center;}
.hv{font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:900;color:#fff;letter-spacing:1px;line-height:1.1;}
.hl{font-size:7px;color:#445;letter-spacing:2px;text-transform:uppercase;}
#hud-right{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:5px;}

/* WIND BOX */
#wind-box{background:rgba(0,0,0,.48);border:1px solid rgba(0,212,255,.15);border-radius:9px;padding:5px 10px;display:flex;align-items:center;gap:6px;pointer-events:none;}
#wind-arrow{font-size:20px;transition:transform .6s;}
#wind-spd{font-family:'Rajdhani',sans-serif;font-size:14px;font-weight:900;color:var(--cyan);}
#wind-lbl{font-size:7px;color:#335;letter-spacing:2px;}

/* MISSION BOX */
#mission-box{position:absolute;top:65px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:7px 16px;text-align:center;min-width:200px;}
#ms-num{font-size:7px;color:#446;letter-spacing:3px;margin-bottom:2px;}
#ms-name{font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--gold);letter-spacing:1px;}
#ms-desc{font-size:8px;color:#556;margin-top:2px;}
#ms-prog{font-size:9px;color:var(--green);margin-top:3px;font-weight:700;letter-spacing:1px;}

/* AMMO + WEAPON */
#ammo-wrap{position:absolute;bottom:92px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:3px;}
#weapon-name{font-family:'Black Han Sans',sans-serif;font-size:10px;color:var(--gold);letter-spacing:1px;margin-bottom:2px;text-align:center;}
.ammo-col{display:flex;flex-direction:column;gap:2px;}
.adot{width:9px;height:20px;border-radius:3px;background:rgba(245,197,24,.1);border:1px solid rgba(245,197,24,.18);transition:all .1s;}
.adot.live{background:var(--gold);box-shadow:0 0 5px rgba(245,197,24,.6);}
#ammo-lbl{font-size:7px;color:#555;letter-spacing:2px;margin-top:3px;}

/* BREATH BAR */
#breath-wrap{position:absolute;bottom:92px;left:50%;transform:translateX(-50%);z-index:100;text-align:center;pointer-events:none;width:min(160px,40vw);}
#breath-lbl{font-size:7px;color:#446;letter-spacing:2px;margin-bottom:3px;}
#breath-track{height:7px;background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.18);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:linear-gradient(90deg,#004466,var(--cyan),#88ffff);border-radius:99px;transition:width .07s;}
#breath-state{font-size:7px;margin-top:3px;letter-spacing:2px;}

/* RELOAD RING */
#rl-ring{position:absolute;bottom:110px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;text-align:center;display:none;}
#rl-cv{display:block;margin:0 auto 2px;}
#rl-txt{font-size:7px;color:var(--gold);letter-spacing:2px;}

/* SCOPE */
#scope-wrap{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-bg{position:absolute;inset:0;background:rgba(0,0,0,.9);}
#scope-lens{position:absolute;border-radius:50%;overflow:hidden;left:50%;top:50%;transform:translate(-50%,-50%);border:3px solid rgba(0,200,0,.55);box-shadow:0 0 0 2000px rgba(0,0,0,.9);width:280px;height:280px;}
/* 경보 레벨 */
#alert-strip{position:absolute;top:0;left:0;right:0;height:5px;z-index:201;pointer-events:none;opacity:0;transition:opacity .3s,background .4s;}
#alert-lbl{position:absolute;top:5px;left:50%;transform:translateX(-50%);z-index:201;pointer-events:none;font-family:'Orbitron',sans-serif;font-size:8px;letter-spacing:3px;padding:2px 14px;border-radius:0 0 6px 6px;background:rgba(0,0,0,.75);opacity:0;transition:opacity .3s;white-space:nowrap;}
#scope-cv{display:block;}
#scope-ui{position:absolute;inset:0;pointer-events:none;}
/* Sway container */
#sway-container{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;}

/* SLOWMO */
#slowmo-frame{position:absolute;inset:0;z-index:80;pointer-events:none;opacity:0;box-shadow:inset 0 0 0 5px rgba(255,215,0,.45);background:rgba(255,215,0,.03);transition:opacity .15s;}
#slowmo-lbl{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:85;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-size:clamp(20px,4vw,30px);color:var(--gold);letter-spacing:4px;text-shadow:0 0 20px rgba(245,197,24,.8);opacity:0;transition:opacity .15s;}

/* KILL FEED */
#killfeed{position:absolute;top:70px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;max-width:210px;}
.kfe{background:rgba(0,0,0,.55);border-left:3px solid var(--red);padding:4px 8px;font-size:9px;color:#ccc;border-radius:0 6px 6px 0;animation:kfs .22s ease;white-space:nowrap;}
@keyframes kfs{from{opacity:0;transform:translateX(14px);}to{opacity:1;transform:none;}}

/* CROSSHAIR */
#crosshair{position:absolute;inset:0;z-index:55;pointer-events:none;}

/* MISSION CLEAR BANNER */
#mc-banner{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;text-align:center;opacity:0;transition:opacity .25s;}
#mc-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(26px,5.5vw,40px);letter-spacing:4px;text-shadow:0 0 28px currentColor;}
#mc-sub{font-size:11px;color:#bbb;letter-spacing:3px;margin-top:5px;}

/* TOUCH BUTTONS */
#touch-btns{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:9px;z-index:100;}
.tch{padding:11px 18px;border-radius:10px;border:1.5px solid;font-family:'Black Han Sans',sans-serif;font-size:13px;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;display:flex;flex-direction:column;align-items:center;gap:2px;}
.tch:active{transform:scale(.9);}
.tch-lbl{font-size:7px;letter-spacing:1px;}
#tch-scope{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.38);color:var(--cyan);}
#tch-hold{background:rgba(0,255,136,.07);border-color:rgba(0,255,136,.32);color:var(--green);}
#tch-fire{background:rgba(255,34,68,.18);border-color:rgba(255,34,68,.5);color:var(--red);}
#tch-reload{background:rgba(245,197,24,.08);border-color:rgba(245,197,24,.32);color:var(--gold);}
#tch-weapon{background:rgba(192,79,255,.1);border-color:rgba(192,79,255,.35);color:var(--purple);}

/* WEAPON SELECT */
#weapon-bar{position:absolute;bottom:0;left:0;right:0;z-index:100;background:linear-gradient(transparent,rgba(0,0,0,.75));padding:6px 12px 8px;display:flex;gap:6px;justify-content:center;pointer-events:auto;display:none;}
.wslot{padding:6px 12px;background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.08);border-radius:8px;cursor:pointer;transition:all .18s;text-align:center;min-width:70px;}
.wslot.active{border-color:var(--gold);box-shadow:0 0 12px rgba(245,197,24,.3);}
.ws-name{font-family:'Black Han Sans',sans-serif;font-size:9px;letter-spacing:1px;}
.ws-stats{font-size:7px;color:#446;margin-top:2px;}

/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:400;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:30px 22px;background:linear-gradient(160deg,#040809,#060d10);border:1px solid rgba(0,255,136,.18);border-radius:20px;min-width:320px;max-width:94vw;max-height:90vh;overflow-y:auto;}
.ov-eye{font-size:7px;letter-spacing:4px;color:var(--green);background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.2);border-radius:99px;padding:3px 12px;display:inline-block;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5.5vw,34px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#335;letter-spacing:4px;margin-bottom:14px;}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.sc{padding:6px 11px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.sv{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:#fff;}
.sl{font-size:7px;color:#446;letter-spacing:2px;}
.diff-row{display:flex;gap:6px;justify-content:center;margin-bottom:12px;flex-wrap:wrap;}
.dt{padding:8px 14px;border-radius:99px;background:var(--glass);border:1px solid var(--border);font-size:9px;color:#556;cursor:pointer;transition:all .18s;text-align:center;}
.dt.sel{border-color:var(--green);color:var(--green);background:rgba(0,255,136,.08);}
.ov-btn{display:inline-block;padding:12px 28px;background:linear-gradient(135deg,rgba(0,255,136,.16),rgba(0,212,255,.1));border:1px solid rgba(0,255,136,.42);border-radius:12px;font-family:'Black Han Sans',sans-serif;font-size:16px;color:var(--green);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(0,255,136,.3),rgba(0,212,255,.2));transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,255,136,.28);}
.ov-btn2{display:inline-block;padding:9px 20px;background:var(--glass);border:1px solid var(--border);border-radius:10px;font-family:'Black Han Sans',sans-serif;font-size:12px;color:#556;cursor:pointer;letter-spacing:1px;transition:all .18s;margin-top:8px;}
.mission-list{display:flex;flex-direction:column;gap:6px;margin-bottom:14px;text-align:left;}
.ml-item{padding:8px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;display:flex;align-items:center;gap:10px;}
.ml-ico{font-size:20px;}
.ml-info{flex:1;}
.ml-name{font-family:'Black Han Sans',sans-serif;font-size:11px;color:#ccc;letter-spacing:1px;}
.ml-desc{font-size:7px;color:#446;margin-top:2px;}
.ml-cleared{font-size:9px;color:var(--green);margin-left:auto;}
.tag-strip{overflow:hidden;margin-bottom:14px;}
.tag-inner{display:flex;gap:8px;animation:tgs 16s linear infinite;width:max-content;}
@keyframes tgs{0%{transform:translateX(0);}100%{transform:translateX(-50%)}}
.tpill{font-size:8px;border:1px solid var(--border);border-radius:99px;padding:3px 11px;white-space:nowrap;letter-spacing:1px;color:#445;}
.tpill.c{color:var(--cyan);border-color:rgba(0,212,255,.3);}
.tpill.g{color:var(--gold);border-color:rgba(245,197,24,.3);}
.tpill.r{color:var(--red);border-color:rgba(255,34,68,.3);}
.tpill.p{color:var(--purple);border-color:rgba(192,79,255,.3);}

#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,0.82);backdrop-filter:blur(4px);display:flex;justify-content:center;align-items:center;gap:16px;padding:5px 12px;font-size:10px;color:#778;letter-spacing:1px;flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,0.06);}
#ctrl-bar span{color:#aab;}
#ctrl-bar b{color:#22d3ee;font-weight:700;}
</style>
</head>
<body>
  <div id="ctrl-bar">
    <span><b>마우스</b> 조준  <b>클릭 / Space</b> 발사</span>
    <span>|</span>
    <span><b>Z / Esc</b> 스코프 토글</span>
    <span>|</span>
    <span><b>Shift</b> 숨참기(정확도↑)</span>
    <span>|</span>
    <span><b>R</b> 재장전  <b>1~4</b> 무기교체</span>
  </div>
<div id="root">
  <canvas id="bgc"></canvas>
  <canvas id="gc"></canvas>

  <!-- HUD -->
  <div id="hud">
    <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
    <div class="hb"><div class="hv" id="ms-kills-v">0/0</div><div class="hl">TARGETS</div></div>
    <div class="hb"><div class="hv" id="time-v">--</div><div class="hl">TIME</div></div>
    <div id="hud-right">
      <div id="wind-box">
        <div id="wind-arrow">→</div>
        <div><div id="wind-spd">0 m/s</div><div id="wind-lbl">WIND</div></div>
      </div>
    </div>
  </div>

  <div id="mission-box">
    <div id="ms-num">MISSION 1 / 6</div>
    <div id="ms-name">정지 표적 사격</div>
    <div id="ms-desc">표적을 저격하라</div>
    <div id="ms-prog"></div>
  </div>

  <!-- Scope -->
  <div id="scope-wrap">
    <div id="scope-bg"></div>
    <div id="sway-container">
      <div id="scope-lens">
        <canvas id="scope-cv" width="280" height="280"></canvas>
        <svg id="scope-ui" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="position:absolute;inset:0;width:100%;height:100%;">
          <!-- Cross hairs -->
          <line x1="50" y1="0" x2="50" y2="42" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
          <line x1="50" y1="58" x2="50" y2="100" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
          <line x1="0" y1="50" x2="42" y2="50" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
          <line x1="58" y1="50" x2="100" y2="50" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
          <!-- Center dot -->
          <circle cx="50" cy="50" r="1.8" fill="none" stroke="rgba(0,255,0,.85)" stroke-width=".9"/>
          <!-- Inner ring -->
          <circle cx="50" cy="50" r="13" fill="none" stroke="rgba(0,255,0,.28)" stroke-width=".4"/>
          <!-- Outer ring -->
          <circle cx="50" cy="50" r="26" fill="none" stroke="rgba(0,255,0,.18)" stroke-width=".3"/>
          <!-- Mil-dot scale marks -->
          <line x1="50" y1="33" x2="50" y2="36" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
          <line x1="50" y1="64" x2="50" y2="67" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
          <line x1="33" y1="50" x2="36" y2="50" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
          <line x1="64" y1="50" x2="67" y2="50" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
          <!-- Range labels -->
          <text x="52" y="32" fill="rgba(0,255,0,.4)" font-size="3" font-family="monospace">200</text>
          <text x="52" y="67" fill="rgba(0,255,0,.4)" font-size="3" font-family="monospace">500</text>
          <!-- Hold indicator -->
          <rect x="2" y="92" width="44" height="4" fill="rgba(0,255,0,.1)" rx="2"/>
          <rect id="hold-bar" x="2" y="92" width="44" height="4" fill="rgba(0,255,0,.6)" rx="2"/>
        </svg>
      </div>
    </div>
  </div>

  <!-- Crosshair (free-aim mode) -->
  <canvas id="crosshair-cv" style="position:absolute;inset:0;z-index:55;pointer-events:none;"></canvas>

  <div id="ammo-wrap">
    <div id="weapon-name">권총</div>
    <div class="ammo-col" id="ammo-col"></div>
    <div id="ammo-lbl">AMMO</div>
  </div>
  <div id="breath-wrap">
    <div id="breath-lbl">호흡 (HOLD)</div>
    <div id="breath-track"><div id="breath-fill" style="width:100%"></div></div>
    <div id="breath-state" style="color:#446">안정</div>
  </div>

  <div id="rl-ring"><canvas id="rl-cv" width="52" height="52"></canvas><div id="rl-txt">장전중...</div></div>

  <div id="killfeed"></div>
  <div id="alert-strip"></div>
  <div id="alert-lbl"></div>
  <div id="slowmo-frame"></div>
  <div id="slowmo-lbl">SLOW MOTION</div>

  <div id="mc-banner">
    <div id="mc-big" style="color:var(--gold)">✅ 클리어!</div>
    <div id="mc-sub"></div>
  </div>

  <div id="touch-btns">
    <div class="tch" id="tch-scope"><span>🔭</span><span class="tch-lbl">조준경</span></div>
    <div class="tch" id="tch-hold"><span>🫁</span><span class="tch-lbl">호흡</span></div>
    <div class="tch" id="tch-fire"><span>🔫</span><span class="tch-lbl">발사</span></div>
    <div class="tch" id="tch-reload"><span>🔄</span><span class="tch-lbl">장전</span></div>
    <div class="tch" id="tch-weapon"><span>🔀</span><span class="tch-lbl">무기</span></div>
  </div>

  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>

<script>
'use strict';
// ================================================================
//  스나이퍼 엘리트 v3.0
//  6 미션 스토리 · 4종 무기 (저격·반자동·산탄·권총)
//  4배율 조준경 · 실시간 바람 탄도 · 호흡 안정화
//  헤드샷/급소 판정 · 슬로우모션 · 킬체인 보너스
//  이동 표적 AI · 군집 표적 · 시간 제한 미션
//  파티클 이펙트 · 혈흔 · 장탄수 · 난이도 3단계
// ================================================================

const bgc   = document.getElementById('bgc');
const bgCtx = bgc.getContext('2d');
const canvas= document.getElementById('gc');
const ctx   = canvas.getContext('2d');
const scopeCV = document.getElementById('scope-cv');
const sCtx  = scopeCV.getContext('2d');
const crossCV = document.getElementById('crosshair-cv');
const crCtx = crossCV.getContext('2d');
const root  = document.getElementById('root');

function resize(){
  canvas.width = bgc.width = crossCV.width = root.clientWidth||window.innerWidth||730;
  canvas.height= bgc.height= crossCV.height= root.clientHeight||window.innerHeight||560;
}
resize(); window.addEventListener('resize', ()=>{ resize(); drawStaticBg(); });
setTimeout(()=>{resize();drawStaticBg();},100);setTimeout(()=>{resize();drawStaticBg();},500);

// ================================================================
//  WEAPON DEFS
// ================================================================
const WDEFS = [
  { id:0, name:'AWM 저격',   emoji:'🎯', mag:5,  relT:140, dmg:200, spread:.005, zoom:4,   col:'#c04fff', desc:'볼트액션·최강 위력',    movePen:true },
  { id:1, name:'SR-25 반자동',emoji:'⚙️', mag:10, relT:95,  dmg:120, spread:.015, zoom:3.5, col:'#00ff88', desc:'반자동·빠른 연사',      movePen:false},
  { id:2, name:'SPAS-12 샷건',emoji:'💥', mag:8,  relT:110, dmg:80,  spread:.18,  zoom:1.5, col:'#ff7700', desc:'근접 산탄·광역 피해',   movePen:false,pellets:7},
  { id:3, name:'M9 권총',    emoji:'🔫', mag:15, relT:50,  dmg:45,  spread:.04,  zoom:1.2, col:'#00d4ff', desc:'무한 탄약·빠른 재장전', unlimited:true},
];

// ================================================================
//  MISSION DEFS
// ================================================================
const MISSIONS = [
  { id:0, name:'정지 표적',   icon:'🎯', desc:'정지 표적 5개 제거',         n:5,  time:90,  moving:false, boss:false, group:false, escort:false },
  { id:1, name:'이동 표적',   icon:'🏃', desc:'이동 표적 4개 저격',         n:4,  time:75,  moving:true,  boss:false, group:false, escort:false },
  { id:2, name:'제한 시간',   icon:'⏱️', desc:'60초 안에 7명 처치',         n:7,  time:60,  moving:false, boss:false, group:false, escort:false },
  { id:3, name:'군집 섬멸',   icon:'👥', desc:'10명 무리 모두 제거',        n:10, time:100, moving:true,  boss:false, group:true,  escort:false },
  { id:4, name:'VIP 경호',    icon:'🚨', desc:'VIP를 지키며 적 6명 저격',   n:6,  time:80,  moving:true,  boss:false, group:false, escort:true  },
  { id:5, name:'보스 처치',   icon:'👹', desc:'고가치 표적(HVT) 제거!',     n:1,  time:60,  moving:true,  boss:true,  group:false, escort:false },
];

// TARGET TYPES
const TTYPES = [
  { emoji:'🎯', sz:22, pts:100, head:.35, body:.75, label:'일반 표적' },
  { emoji:'🪖', sz:20, pts:120, head:.33, body:.7,  label:'무장 병사' },
  { emoji:'💣', sz:24, pts:150, head:.3,  body:.72, label:'폭발물 운반' },
  { emoji:'📡', sz:26, pts:80,  head:.4,  body:.82, label:'통신 장비' },
];

// WEATHER affecting wind/sway
const WEATHERS = [
  { name:'맑음', wind:0,   sway:0,   fog:false },
  { name:'바람', wind:2.5, sway:.8,  fog:false },
  { name:'폭풍', wind:4.5, sway:1.8, fog:true  },
  { name:'야간', wind:1.5, sway:.4,  fog:false, night:true },
];

// ================================================================
//  STATE
// ================================================================
let G = { running: false, diffLv: 1 };
let PARTS = [], HITS = [];
let alertLevel = 0;        // 0=평온 1=경계 2=고경계 3=봉쇄
let alertDecayTimer = 0;
let _totalReinforced = 0;  // 증원된 표적 수

// ================================================================
//  INIT
// ================================================================
function initGame(){
  const W = WEATHERS[Math.floor(Math.random()*WEATHERS.length)];
  G = {
    running: true, diffLv: G.diffLv,
    mIdx: 0, score: 0, totalKills: 0, killChain: 0, chainTimer: 0,
    ammo: [5,10,8,15], wIdx: 0,
    reloading: false, relT: 0,
    scoped: false,
    breath: 100, breathHeld: false,
    swayX: 0, swayY: 0, swayVX:0, swayVY:0,
    wind: { dir: Math.random()<.5?1:-1, spd: 0 },
    weather: W,
    targets: [], bullets: [],
    missionComplete: false, missionFailed: false,
    mouse: { x: canvas.width/2, y: canvas.height/2 },
    scopeX: canvas.width/2, scopeY: canvas.height/2,
    frame: 0, timer: 0,
    cleared: [], // which missions cleared
    vip: null,
    sessionStats: { headshots:0, bodyshots:0, misses:0, longestShot:0 },
  };
  PARTS=[]; HITS=[];
  alertLevel=0; alertDecayTimer=0; _totalReinforced=0;
  drawStaticBg();
  buildAmmoDisplay();
  setWind();
  loadMission(0);
}

// ================================================================
//  BACKGROUND
// ================================================================
function drawStaticBg(){
  const W=canvas.width, H=canvas.height;
  const isNight = G.running && G.weather && G.weather.night;
  // Sky gradient
  const sky = bgCtx.createLinearGradient(0,0,0,H*.58);
  if(isNight){ sky.addColorStop(0,'#010206'); sky.addColorStop(1,'#040820'); }
  else        { sky.addColorStop(0,'#050908'); sky.addColorStop(1,'#0c1a10'); }
  bgCtx.fillStyle=sky; bgCtx.fillRect(0,0,W,H);

  // Stars (always a few, more at night)
  const starCount = isNight ? 180 : 55;
  for(let i=0;i<starCount;i++){
    const sx=((i*137.5+i*i*.003)%1)*W;
    const sy=((i*98.3+i*.5)%.52)*H;
    const sa=(isNight?.8:.28)+Math.random()*.4;
    bgCtx.fillStyle=`rgba(240,240,200,${sa})`;
    bgCtx.beginPath(); bgCtx.arc(sx,sy,i%9===0?1.3:.65,0,Math.PI*2); bgCtx.fill();
  }

  // Mountains — 4 layers
  const mcols = isNight
    ? ['#060d08','#091408','#0c1a0a','#10200c']
    : ['#080f06','#0c1808','#10200a','#14260d'];
  for(let l=0;l<4;l++){
    bgCtx.fillStyle = mcols[l];
    bgCtx.beginPath(); bgCtx.moveTo(0,H);
    const peaks = 6+l*2;
    for(let i=0;i<=peaks;i++){
      const mx=i*(W/peaks);
      const my=H*(.28+l*.08)+Math.sin(i*2.4+l)*H*(.14-l*.028);
      if(i===0) bgCtx.lineTo(mx,my);
      else { const cx=(mx+(i-1)*(W/peaks))/2; bgCtx.quadraticCurveTo(cx,my+20,mx,my); }
    }
    bgCtx.lineTo(W,H); bgCtx.closePath(); bgCtx.fill();
  }

  const fY = H*.62;

  // Trees along treeline
  bgCtx.fillStyle = isNight?'#040c04':'#050e05';
  for(let i=0;i<45;i++){
    const tx=Math.random()*W, ty=fY-2;
    const th=16+Math.random()*46, tw=8+Math.random()*14;
    bgCtx.beginPath();
    bgCtx.moveTo(tx,ty);
    bgCtx.lineTo(tx-tw/2,ty+th*.38); bgCtx.lineTo(tx-tw*.3,ty+th*.38);
    bgCtx.lineTo(tx-tw*.38,ty+th*.72); bgCtx.lineTo(tx,ty+th);
    bgCtx.lineTo(tx+tw*.38,ty+th*.72); bgCtx.lineTo(tx+tw*.3,ty+th*.38);
    bgCtx.lineTo(tx+tw/2,ty+th*.38);
    bgCtx.closePath(); bgCtx.fill();
  }

  // Ground
  const gr = bgCtx.createLinearGradient(0,fY,0,H);
  gr.addColorStop(0, isNight?'#101a10':'#182a12');
  gr.addColorStop(1, isNight?'#080e08':'#0a1408');
  bgCtx.fillStyle=gr; bgCtx.fillRect(0,fY,W,H-fY);
  bgCtx.strokeStyle='rgba(0,80,0,.07)'; bgCtx.lineWidth=1;
  for(let gy=fY;gy<H;gy+=20){ bgCtx.beginPath(); bgCtx.moveTo(0,gy); bgCtx.lineTo(W,gy); bgCtx.stroke(); }

  // Buildings silhouette
  for(let i=0;i<9;i++){
    const bx=i*(W/8.5)-20, bw=26+Math.random()*50, bh=35+Math.random()*75;
    bgCtx.fillStyle=isNight?'#050a05':'#060c04';
    bgCtx.fillRect(bx, fY-bh, bw, bh);
    for(let wx=bx+5;wx<bx+bw-5;wx+=11){
      for(let wy=fY-bh+5;wy<fY-5;wy+=13){
        if(Math.random()<(isNight?.5:.38)){
          const litc = isNight?`rgba(255,210,100,.38)`:`rgba(255,200,80,.22)`;
          bgCtx.fillStyle=litc; bgCtx.fillRect(wx,wy,4,7);
          bgCtx.fillStyle=isNight?'#050a05':'#060c04';
        }
      }
    }
  }

  // Fog overlay
  if(G.running && G.weather && G.weather.fog){
    const fg = bgCtx.createLinearGradient(0,0,0,H);
    fg.addColorStop(0,'rgba(150,180,160,.22)'); fg.addColorStop(1,'rgba(100,140,110,.08)');
    bgCtx.fillStyle=fg; bgCtx.fillRect(0,0,W,H);
  }
}

// ================================================================
//  WIND
// ================================================================
function setWind(){
  const ms = MISSIONS[G.mIdx];
  const diffWindMul = [0, .7, 1.4][G.diffLv];
  const baseWind = G.weather.wind * diffWindMul;
  G.wind.dir = Math.random()<.5 ? 1 : -1;
  G.wind.spd = G.wind.dir * (baseWind * (.6+Math.random()*.8));
  // Slowly change over time
  G._windTarget = G.wind.spd;
  updateWindHUD();
}
function updateWindHUD(){
  const arrows = ['←','↙','↓','↘','→','↗','↑','↖'];
  const abs = Math.abs(G.wind.spd);
  document.getElementById('wind-arrow').textContent = abs<.2 ? '○' : G.wind.spd>0 ? '→' : '←';
  document.getElementById('wind-spd').textContent = abs.toFixed(1)+' m/s';
}

// ================================================================
//  MISSION LOADER
// ================================================================
function loadMission(idx){
  const ms = MISSIONS[idx];
  G.mIdx = idx;
  G.missionComplete = false;
  G.missionFailed   = false;
  G.timer  = ms.time * 60;
  // Reset ammo for all weapons (keep pistol unlimited)
  G.ammo = [5,10,8,999];
  G.reloading = false; G.relT = 0;
  setWind(); drawStaticBg();
  spawnTargets(ms);
  buildAmmoDisplay();
  document.getElementById('ms-num').textContent  = `MISSION ${idx+1} / ${MISSIONS.length}`;
  document.getElementById('ms-name').textContent  = ms.name;
  document.getElementById('ms-desc').textContent  = ms.desc;
  document.getElementById('weapon-name').textContent = WDEFS[G.wIdx].name;
  updateMissionHUD();
  // VIP for escort mission
  if(ms.escort){
    G.vip = { x:canvas.width*.5, y:canvas.height*.52, hp:100, maxHp:100, alive:true };
  }else{ G.vip=null; }
}

function spawnTargets(ms){
  G.targets = [];
  const W=canvas.width, H=canvas.height;
  const zones=[.28,.35,.42,.5,.58];
  const isBoss=ms.boss;

  for(let i=0;i<ms.n;i++){
    let t;
    if(isBoss){
      t={emoji:'👹',sz:52,pts:600,head:.28,body:.65,label:'HVT 보스'};
    }else if(ms.escort && i===0){
      // First "target" is actually an enemy
      t = TTYPES[Math.floor(Math.random()*TTYPES.length)];
    }else{
      t = TTYPES[Math.floor(Math.random()*TTYPES.length)];
    }
    const y = H*zones[Math.floor(Math.random()*zones.length)];
    const x = W*.1+Math.random()*W*.8;
    const sz = t.sz + Math.random()*8;
    const spd = ms.moving ? (.6+Math.random()*1.4)*(isBoss?1.5:1) : 0;

    G.targets.push({
      x, y, baseX:x, baseY:y,
      sz, emoji:t.emoji, pts:t.pts, head:t.head, body:t.body, label:t.label,
      spd, phase:Math.random()*Math.PI*2, amp:W*(.06+Math.random()*.1),
      alive:true, flash:0,
      dist: (250+Math.random()*650)|0,
      isBoss,
      alertLevel:0, // 0=unaware 1=alert 2=fleeing
      vx:0, vy:0,
      // Patrol path
      patrolDir: Math.random()<.5 ? 1:-1,
    });
  }
}

// ================================================================
//  PARTICLES
// ================================================================
function spawnP(x,y,o={}){
  const n=o.n||8;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2, v=(o.vMin||1.5)+Math.random()*(o.vMax||5);
    const cols=Array.isArray(o.col)?o.col:[o.col||'#ff2244'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      dec:(o.dMin||.025)+Math.random()*(o.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(o.szMin||2)+Math.random()*(o.szMax||5),glow:o.glow||false});
  }
}
function spawnBlood(x,y,sz=1){
  spawnP(x,y,{n:14+sz*4|0,col:['#8b0000','#cc0000','#ee1122'],vMax:5+sz*2,szMin:3,szMax:6+sz*2,dMin:.02,dMax:.04});
  bgCtx.save(); bgCtx.globalAlpha=.42;
  bgCtx.fillStyle='rgba(80,0,0,.4)';
  bgCtx.beginPath(); bgCtx.ellipse(x,y,5+sz*5,3+sz*4,Math.random()*Math.PI,0,Math.PI*2); bgCtx.fill();
  bgCtx.restore();
}
function spawnHit(x,y,txt,col){ HITS.push({x,y:y-14,txt,col,life:1,vy:-.65}); }

// ================================================================
//  SHOOT
// ================================================================
function fire(){
  const w = WDEFS[G.wIdx];
  if(G.ammo[G.wIdx]<=0 || G.reloading || G.missionComplete) return;
  if(!w.unlimited) G.ammo[G.wIdx]--;
  buildAmmoDisplay();

  // Bullet position
  const originX = canvas.width/2, originY = canvas.height/2;

  // Wind drift (proportional to wind speed, difficulty, and whether scoped)
  const windDrift = G.wind.spd * (G.diffLv===0?0:G.diffLv===1?.6:1.2) * 18;
  // Sway at moment of shot
  const swayPen = G.breathHeld ? 0 : G.diffLv * (G.weather.sway+.5) * 3;

  const pellets = w.pellets||1;
  for(let pe=0;pe<pellets;pe++){
    const spr = (Math.random()-.5)*w.spread*2*(G.scoped?.5:1);
    const hitX = (G.scoped ? G.scopeX : G.mouse.x) + windDrift + (Math.random()-.5)*swayPen + spr*200;
    const hitY = (G.scoped ? G.scopeY : G.mouse.y) + (Math.random()-.5)*swayPen;

    let hitSomething = false;
    G.targets.forEach(t=>{
      if(!t.alive || hitSomething) return;
      const dx=hitX-t.x, dy=hitY-t.y;
      const dist=Math.sqrt(dx*dx+dy*dy);
      if(dist < t.sz*.95){
        hitSomething=true;
        const isHead = dist < t.sz*t.head;
        const isBody = dist < t.sz*t.body;
        // Damage
        let pts = isHead ? t.pts*3 : isBody ? t.pts : Math.round(t.pts*.6);
        // Distance bonus
        const distBonus = Math.max(1, Math.floor(t.dist/100));
        pts *= distBonus;
        // Kill chain
        G.killChain++; G.chainTimer=180;
        if(G.killChain>=2) pts = Math.round(pts*(1+G.killChain*.2));
        G.score += pts; G.totalKills++;
        if(isHead) G.sessionStats.headshots++;
        else G.sessionStats.bodyshots++;
        if(t.dist > G.sessionStats.longestShot) G.sessionStats.longestShot=t.dist;

        // Kill effects
        t.alive=false;
        spawnBlood(t.x, t.y, t.sz*.08);
        spawnP(t.x,t.y,{n:isHead?22:14,col:isHead?['#ff0000','#cc0000','#ffffff']:['#cc2200','#ff4400'],glow:isHead,vMax:isHead?9:6,szMax:isHead?12:8});

        // Headshot slow-mo
        if(isHead || t.isBoss){
          triggerSlowMo(isHead?'💀 HEADSHOT!':'👹 BOSS DOWN!');
        }

        addKillfeed(t, isHead, t.dist, pts);
        spawnHit(t.x,t.y-t.sz, isHead?'💀 HEADSHOT!': isBody?'BODY SHOT': 'HIT', isHead?'#f5c518':'#ff4444');
        spawnHit(t.x,t.y-t.sz-18,'+'+pts, isHead?'#f5c518':'#00d4ff');
      }
    });
    if(!hitSomething){
      G.sessionStats.misses++;
      G.killChain=0;
      spawnP(hitX,hitY,{n:4,col:'rgba(180,180,180,.4)',vMax:3,szMax:3,dMin:.08,dMax:.12});
    }

    // Bullet tracer
    G.bullets.push({x:originX, y:originY, tx:hitX, ty:hitY, life:1});
  }

  // 총성 → 경보 레벨 상승
  alertLevel = Math.min(3, alertLevel + 1);
  alertDecayTimer = 480; // ~8초
  updateAlertHUD();

  // Muzzle flash
  spawnP(originX,originY,{n:5,col:[w.col,'#fff'],vMin:2,vMax:5,dMin:.08,dMax:.12,glow:true});

  if(G.ammo[G.wIdx]<=0 && !w.unlimited) setTimeout(startReload,200);
  checkClear();
}

function startReload(){
  if(G.reloading) return;
  const w=WDEFS[G.wIdx];
  if(w.unlimited||G.ammo[G.wIdx]>=w.mag) return;
  G.reloading=true; G.relT=w.relT;
  document.getElementById('rl-ring').style.display='block';
}

function switchWeapon(idx){
  if(idx===G.wIdx||idx>=WDEFS.length) return;
  if(G.reloading){G.reloading=false;G.relT=0;document.getElementById('rl-ring').style.display='none';}
  G.wIdx=idx;
  document.getElementById('weapon-name').textContent=WDEFS[idx].name;
  buildAmmoDisplay();
}

// ================================================================
//  ALERT LEVEL HUD
// ================================================================
function updateAlertHUD(){
  const strip=document.getElementById('alert-strip');
  const lbl=document.getElementById('alert-lbl');
  const root=document.getElementById('root');
  const msgs=['','⚠️ 경계 — 적이 움직임을 감지했다','🔴 고경계 — 증원 요청 중','🚨 봉쇄 — 전군 응전!'];
  const cols=['','rgba(255,140,0,1)','rgba(255,50,0,1)','rgba(255,0,50,1)'];
  const shadows=['','inset 0 0 20px rgba(255,140,0,.25)','inset 0 0 32px rgba(255,50,0,.35)','inset 0 0 50px rgba(255,0,50,.5)'];
  if(strip){
    strip.style.opacity = alertLevel>0 ? '1':'0';
    strip.style.background = cols[alertLevel]||'transparent';
    // 점멸 효과 (고경계 이상)
    if(alertLevel>=2){ strip.style.animation='alertBlink .6s infinite'; }
    else strip.style.animation='none';
  }
  if(lbl){
    lbl.style.opacity = alertLevel>0 ? '1':'0';
    lbl.style.color = cols[alertLevel]||'transparent';
    lbl.textContent = msgs[alertLevel]||'';
  }
  if(root){ root.style.boxShadow = shadows[alertLevel]||'none'; }
}

// ================================================================
//  SLOW MOTION
// ================================================================
let slowMoTimer=0;
function triggerSlowMo(label){
  slowMoTimer=120;
  const sf=document.getElementById('slowmo-frame');
  const sl=document.getElementById('slowmo-lbl');
  sf.style.opacity='1'; sl.textContent=label; sl.style.opacity='1';
  setTimeout(()=>{sf.style.opacity='0';sl.style.opacity='0';},2000);
}

// KILL FEED
function addKillfeed(t, head, dist, pts){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div'); d.className='kfe';
  d.innerHTML=`${t.emoji} ${head?'💀 헤드샷':'격파'} <span style="color:var(--gold)">${dist}m</span> <b>+${pts}pt</b>`;
  if(head){ d.style.borderLeftColor='var(--gold)'; d.style.color='var(--gold)'; }
  if(t.isBoss){ d.style.borderLeftColor='var(--purple)'; d.style.fontSize='10px'; }
  kf.appendChild(d); setTimeout(()=>d.remove(),3200);
  while(kf.children.length>5) kf.removeChild(kf.firstChild);
}

// ================================================================
//  MISSION CHECK
// ================================================================
function checkClear(){
  const ms=MISSIONS[G.mIdx];
  const alive=G.targets.filter(t=>t.alive).length;
  if(alive===0 && !G.missionComplete){
    G.missionComplete=true;
    const bonus=(G.mIdx+1)*700;
    G.score+=bonus;
    G.cleared.push(G.mIdx);

    // ── 등급 산출 (마지막 미션 클리어 시) ──
    if(G.mIdx===MISSIONS.length-1){
      const headRatio = G.totalKills>0 ? G.sessionStats.headshots/G.totalKills : 0;
      const silent = alertLevel===0; // 무소음 여부
      const missRatio = (G.sessionStats.misses||0)/(Math.max(1,G.totalKills+G.sessionStats.misses));
      let grade='B';
      if(headRatio>=0.6 && silent && missRatio<0.3) grade='S';
      else if(headRatio>=0.4 && alertLevel<=1 && missRatio<0.5) grade='A';
      G._finalGrade=grade;
      const gradeReward={S:1000000,A:500000,B:200000};
      try{window.parent.postMessage({type:'sniper_result',grade,reward:gradeReward[grade],score:G.score},'*');}catch(e){}
    }
    const mc=document.getElementById('mc-banner');
    document.getElementById('mc-big').textContent=G.mIdx<MISSIONS.length-1?'✅ 미션 클리어!':'🏆 전 임무 완료!';
    document.getElementById('mc-sub').textContent=`+${bonus.toLocaleString()} 보너스 / 다음 미션 준비 중`;
    mc.style.opacity='1';
    setTimeout(()=>{
      mc.style.opacity='0';
      if(G.mIdx<MISSIONS.length-1){ G.mIdx++; setWind(); loadMission(G.mIdx); }
      else setTimeout(()=>showResult(true),400);
    },2800);
  }
}

function showResult(victory){
  G.running=false;
  alertLevel=0; updateAlertHUD();
  const best=Math.max(G.score,parseInt(localStorage.getItem('snipeBest')||'0'));
  localStorage.setItem('snipeBest',best);
  const grade=G._finalGrade||'B';
  const gradeColor={S:'var(--gold)',A:'var(--green)',B:'var(--cyan)'}[grade]||'var(--cyan)';
  const gradeReward={S:'100만원',A:'50만원',B:'20만원'}[grade];
  const gradeDesc={S:'무소음·헤드샷 달인 🏆',A:'숙련 저격수 ⭐',B:'임무 완료 ✅'}[grade]||'';
  const gradeHTML=victory?`<div style="margin:10px 0;padding:10px;background:rgba(255,255,255,.04);border:1px solid ${gradeColor}55;border-radius:10px;"><div style="font-family:'Black Han Sans',sans-serif;font-size:28px;color:${gradeColor};">${grade} 등급</div><div style="font-size:9px;color:#667;margin-top:2px;">${gradeDesc}</div><div style="font-size:10px;color:var(--gold);margin-top:4px;">💰 포털 보상: ${gradeReward}</div></div>`:'';
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-eye">${victory?'ALL MISSIONS CLEARED':'MISSION FAILED'}</div>
    <div class="ov-title" style="color:${victory?'var(--gold)':'var(--red)'}">${victory?'🏆 임무 완료!':'⏱️ 실패!'}</div>
    <div class="ov-sub">${victory?'MISSION COMPLETE':'TIME OVER'}</div>
    ${gradeHTML}
    <div class="stats-row">
      <div class="sc"><div class="sv" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="sl">점수</div></div>
      <div class="sc"><div class="sv">${G.totalKills}</div><div class="sl">처치</div></div>
      <div class="sc"><div class="sv" style="color:var(--red)">💀 ${G.sessionStats.headshots}</div><div class="sl">헤드샷</div></div>
      <div class="sc"><div class="sv" style="color:var(--cyan)">${G.sessionStats.longestShot}m</div><div class="sl">최장 저격</div></div>
    </div>
    <div style="font-size:9px;color:#446;margin-bottom:14px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>
    <button class="ov-btn" onclick="startGame()">재배치 🎯</button>
    <br><button class="ov-btn2" onclick="showTitle()">설정 변경</button>
  </div>`;
  ov.style.display='flex';
}

// ================================================================
//  UPDATE
// ================================================================
function update(){
  if(!G.running || G.missionComplete) return;
  G.frame++;

  // ── 경보 레벨 처리 ──
  if(alertDecayTimer>0){ alertDecayTimer--; }
  else if(alertLevel>0){ alertLevel=Math.max(0,alertLevel-1); updateAlertHUD(); }
  // 경보 2이상: 표적 이동속도 소폭 증가
  if(alertLevel>=2){
    G.targets.forEach(t=>{if(t.alive&&t.spd>0) t.spd=Math.min(t.spd*1.0008,3.5);});
  }
  // 경보 3: 10초마다 증원 표적 1명 추가 (최대 3명까지)
  if(alertLevel>=3 && G.frame%600===0 && _totalReinforced<3){
    const W=canvas.width,H=canvas.height;
    const t_extra=TTYPES[Math.floor(Math.random()*TTYPES.length)];
    const side=Math.floor(Math.random()*4);
    let rx,ry;
    if(side===0){rx=W*.1+Math.random()*W*.8;ry=-40;}
    else if(side===1){rx=W+40;ry=H*.2+Math.random()*H*.6;}
    else if(side===2){rx=W*.1+Math.random()*W*.8;ry=H+40;}
    else{rx=-40;ry=H*.2+Math.random()*H*.6;}
    G.targets.push({
      x:rx,y:ry,baseX:rx,baseY:ry,
      sz:t_extra.sz+4,emoji:'🪖',pts:t_extra.pts,head:t_extra.head,body:t_extra.body,label:'증원병',
      spd:1.4,phase:Math.random()*Math.PI*2,amp:W*.08,
      alive:true,flash:0,dist:150+Math.floor(Math.random()*200),
      isBoss:false,alertLevel:1,vx:0,vy:0,patrolDir:1,
    });
    _totalReinforced++;
    spawnHit(canvas.width/2,canvas.height/2,'🚨 증원 도착!','#ff2244');
  }

  // Kill chain decay
  if(G.chainTimer>0) G.chainTimer--;
  else if(G.killChain>0) G.killChain=0;

  // Timer
  if(!G.missionComplete){
    G.timer--;
    if(G.timer<=0 && !G.missionComplete){ setTimeout(()=>showResult(false),400); return; }
  }

  // Reload
  if(G.reloading){
    G.relT--;
    drawReloadRing();
    if(G.relT<=0){
      const w=WDEFS[G.wIdx]; G.ammo[G.wIdx]=w.mag;
      G.reloading=false; document.getElementById('rl-ring').style.display='none';
      buildAmmoDisplay();
    }
  }

  // Breath
  if(G.breathHeld){
    G.breath=Math.max(0,G.breath-.48);
    if(G.breath<=0){ G.breathHeld=false; }
  }else{
    G.breath=Math.min(100,G.breath+.22);
  }
  document.getElementById('breath-fill').style.width=G.breath+'%';
  const bs=document.getElementById('breath-state');
  if(G.breathHeld&&G.breath>30){ bs.textContent='✅ 안정'; bs.style.color='var(--green)'; }
  else if(G.breathHeld){ bs.textContent='⚠️ 한계'; bs.style.color='var(--orange)'; }
  else { bs.textContent='안정'; bs.style.color='#446'; }

  // Scope sway
  const diffSway = [0,.8,1.8][G.diffLv];
  const wSway = G.weather.sway;
  const baseSwayF = (diffSway + wSway) * (G.breathHeld ? .12 : 1.0);
  if(!G.breathHeld){
    G.swayVX += (Math.sin(G.frame*.031)*.15 + (Math.random()-.5)*.08)*baseSwayF;
    G.swayVY += (Math.cos(G.frame*.022)*.12 + (Math.random()-.5)*.06)*baseSwayF;
  }else{
    G.swayVX += (Math.sin(G.frame*.015)*.03 + (Math.random()-.5)*.01)*baseSwayF;
    G.swayVY += (Math.cos(G.frame*.011)*.025 + (Math.random()-.5)*.01)*baseSwayF;
  }
  G.swayVX *= .88; G.swayVY *= .88;
  G.swayX += G.swayVX; G.swayY += G.swayVY;
  G.swayX *= .92; G.swayY *= .92;

  // Wind slowly shifts
  if(G.frame%240===0){
    G._windTarget = G.wind.dir * (Math.abs(G.wind.spd)+((Math.random()-.5)*1.2));
    G._windTarget = Math.max(-G.weather.wind*1.5,Math.min(G.weather.wind*1.5,G._windTarget));
  }
  if(G._windTarget!==undefined){ G.wind.spd += (G._windTarget-G.wind.spd)*.005; updateWindHUD(); }

  // Target movement + AI
  G.targets.forEach(t=>{
    if(!t.alive) return;
    t.flash = Math.max(0,t.flash-1);
    if(t.spd>0){
      // Patrol movement
      t.phase += .008 * t.spd;
      const newX = t.baseX + Math.sin(t.phase)*t.amp;
      // Bounce off edges
      if(newX<canvas.width*.08 || newX>canvas.width*.92){
        t.baseX = Math.max(canvas.width*.1, Math.min(canvas.width*.9, newX));
        t.phase = -t.phase;
      }
      t.x = t.baseX + Math.sin(t.phase)*t.amp;
      // VIP escort: enemies slowly advance toward center
      if(MISSIONS[G.mIdx].escort){
        t.y = Math.min(canvas.height*.75, t.y + .3);
      }
    }
  });

  // VIP logic
  if(G.vip && G.vip.alive){
    // Enemies that reach VIP deal damage
    G.targets.forEach(t=>{
      if(!t.alive) return;
      const dx=G.vip.x-t.x, dy=G.vip.y-t.y;
      if(dx*dx+dy*dy < 2500){ G.vip.hp-=.2; if(G.vip.hp<=0){ G.missionFailed=true; showResult(false); } }
    });
  }

  // Bullet tracer fade
  for(let i=G.bullets.length-1;i>=0;i--){ G.bullets[i].life-=.15; if(G.bullets[i].life<=0)G.bullets.splice(i,1); }

  // Particles
  for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.dec;p.life<=0&&PARTS.splice(i,1);}
  for(let i=HITS.length-1;i>=0;i--){const h=HITS[i];h.y+=h.vy;h.life-=.022;h.life<=0&&HITS.splice(i,1);}

  // Slow-mo timer
  if(slowMoTimer>0) slowMoTimer--;

  updateMissionHUD();
}

function updateMissionHUD(){
  document.getElementById('score-v').textContent=G.score.toLocaleString();
  const ms=MISSIONS[G.mIdx];
  const alive=G.targets.filter(t=>t.alive).length;
  document.getElementById('ms-kills-v').textContent=`${ms.n-alive}/${ms.n}`;
  document.getElementById('time-v').textContent=Math.max(0,Math.ceil(G.timer/60));
  document.getElementById('ms-prog').textContent=alive===0?'✅ 완료!':G.killChain>=2?`🔥 킬체인 ×${G.killChain}`:'';
}

// ================================================================
//  RELOAD RING
// ================================================================
function drawReloadRing(){
  const w=WDEFS[G.wIdx], pct=1-(G.relT/w.relT);
  const rc=document.getElementById('rl-cv').getContext('2d');
  rc.clearRect(0,0,52,52);
  rc.strokeStyle='rgba(245,197,24,.12)'; rc.lineWidth=4;
  rc.beginPath(); rc.arc(26,26,22,0,Math.PI*2); rc.stroke();
  rc.strokeStyle='rgba(245,197,24,.85)'; rc.shadowColor='rgba(245,197,24,.5)'; rc.shadowBlur=8; rc.lineWidth=4;
  rc.beginPath(); rc.arc(26,26,22,-Math.PI*.5,-Math.PI*.5+Math.PI*2*pct); rc.stroke();
}

// ================================================================
//  SCOPE RENDER
// ================================================================
function drawScope(){
  const el=document.getElementById('scope-wrap');
  if(!G.scoped){ el.style.display='none'; return; }
  el.style.display='block';
  const W=canvas.width, H=canvas.height;
  const zoom = WDEFS[G.wIdx].zoom;
  const SW=280, SH=280;
  const srcW=W/zoom, srcH=H/zoom;
  // 좌표 클램핑 → 화면 끝에서도 까맣게 되지 않도록
  const rawX=G.scopeX-srcW/2, rawY=G.scopeY-srcH/2;
  const srcX=Math.max(0,Math.min(W-srcW, rawX));
  const srcY=Math.max(0,Math.min(H-srcH, rawY));
  // 1) 정적 배경 (bgc)
  try{ sCtx.drawImage(bgc, srcX, srcY, srcW, srcH, 0, 0, SW, SH); }catch(e){}
  // 2) 게임 캔버스(표적·파티클) 를 그 위에 합성
  try{ sCtx.drawImage(canvas, srcX, srcY, srcW, srcH, 0, 0, SW, SH); }catch(e){}
  // Draw targets in scope
  const scX=SW/srcW, scY=SH/srcH;
  G.targets.forEach(t=>{
    if(!t.alive) return;
    const tx=(t.x-srcX)*scX, ty=(t.y-srcY)*scY;
    if(tx<-30||tx>SW+30||ty<-30||ty>SH+30) return;
    sCtx.save();
    sCtx.font=`${t.sz*scX*1.5}px serif`; sCtx.textAlign='center'; sCtx.textBaseline='middle';
    sCtx.shadowBlur=10; sCtx.shadowColor='rgba(255,50,0,.5)';
    sCtx.fillText(t.emoji,tx,ty); sCtx.restore();
    // Head zone ring
    sCtx.strokeStyle='rgba(255,50,50,.25)'; sCtx.lineWidth=1;
    sCtx.beginPath(); sCtx.arc(tx,ty,t.sz*scX*t.head,0,Math.PI*2); sCtx.stroke();
    // Body zone ring
    sCtx.strokeStyle='rgba(255,150,50,.18)'; sCtx.lineWidth=1;
    sCtx.beginPath(); sCtx.arc(tx,ty,t.sz*scX*t.body,0,Math.PI*2); sCtx.stroke();
    // Range label
    sCtx.fillStyle='rgba(0,255,0,.5)'; sCtx.font='8px Orbitron,monospace';
    sCtx.textAlign='center'; sCtx.fillText(t.dist+'m',tx,ty+t.sz*scX+12);
  });
  // VIP
  if(G.vip&&G.vip.alive){
    const vx=(G.vip.x-srcX)*scX, vy=(G.vip.y-srcY)*scY;
    sCtx.save(); sCtx.font=`${28*scX}px serif`; sCtx.textAlign='center'; sCtx.textBaseline='middle';
    sCtx.shadowBlur=12; sCtx.shadowColor='rgba(0,255,136,.6)'; sCtx.fillText('🧑',vx,vy); sCtx.restore();
    // HP bar
    sCtx.fillStyle='rgba(0,0,0,.5)'; sCtx.fillRect(vx-20,vy-30,40,5);
    sCtx.fillStyle='#00ff88'; sCtx.fillRect(vx-20,vy-30,40*(G.vip.hp/G.vip.maxHp),5);
  }
  // Green tint + vignette
  sCtx.fillStyle='rgba(0,20,0,.1)'; sCtx.fillRect(0,0,SW,SH);
  const vg=sCtx.createRadialGradient(SW/2,SH/2,SW*.28,SW/2,SH/2,SW*.58);
  vg.addColorStop(0,'transparent'); vg.addColorStop(1,'rgba(0,0,0,.5)');
  sCtx.fillStyle=vg; sCtx.fillRect(0,0,SW,SH);
  // Hold bar in scope SVG
  const hb=document.getElementById('hold-bar');
  if(hb) hb.setAttribute('width',44*(G.breath/100));
  // Sway the lens
  const lens=document.getElementById('scope-lens');
  const sx=G.swayX*3, sy=G.swayY*3;
  lens.style.transform=`translate(calc(-50% + ${sx}px),calc(-50% + ${sy}px))`;
}

// CROSSHAIR
function drawCrosshair(){
  const W=canvas.width, H=canvas.height;
  crCtx.clearRect(0,0,W,H);
  if(G.scoped) return;
  const mx=G.mouse.x+G.swayX*2, my=G.mouse.y+G.swayY*2;
  const w=WDEFS[G.wIdx];
  const col=w.col;
  const sz=G.breathHeld?8:12+(1-G.breath/100)*10;
  crCtx.save();
  crCtx.strokeStyle=col; crCtx.lineWidth=1.2; crCtx.globalAlpha=.7;
  crCtx.shadowColor=col; crCtx.shadowBlur=4;
  crCtx.beginPath();
  crCtx.moveTo(mx-sz,my); crCtx.lineTo(mx+sz,my);
  crCtx.moveTo(mx,my-sz); crCtx.lineTo(mx,my+sz);
  crCtx.stroke();
  crCtx.beginPath(); crCtx.arc(mx,my,4,0,Math.PI*2); crCtx.stroke();
  // Wind indicator
  if(Math.abs(G.wind.spd)>.5){
    const wi=G.wind.spd*6;
    crCtx.strokeStyle='rgba(0,200,255,.4)'; crCtx.lineWidth=1;
    crCtx.beginPath(); crCtx.moveTo(mx,my); crCtx.lineTo(mx+wi,my); crCtx.stroke();
    crCtx.beginPath(); crCtx.arc(mx+wi,my,3,0,Math.PI*2); crCtx.stroke();
  }
  crCtx.restore();
}

// ================================================================
//  MAIN DRAW
// ================================================================
function drawTargets(){
  G.targets.forEach(t=>{
    if(!t.alive) return;
    ctx.save();
    if(t.flash>0&&t.flash%2===0) ctx.filter='brightness(4) saturate(0)';
    if(t.isBoss){ctx.shadowColor='rgba(255,0,50,.5)';ctx.shadowBlur=t.sz*.7;}
    ctx.font=`${t.sz*1.6}px serif`; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(t.emoji,t.x,t.y); ctx.restore();
    // Range tag
    ctx.save(); ctx.fillStyle='rgba(255,255,255,.28)';
    ctx.font=`${t.sz*.34}px Orbitron,monospace`; ctx.textAlign='center';
    ctx.fillText(t.dist+'m',t.x,t.y+t.sz*.95); ctx.restore();
    // HP bar for boss
    if(t.isBoss){
      const bw=t.sz*2.4,bh=6,bx=t.x-bw/2,by=t.y-t.sz-12;
      ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(bx,by,bw,bh);
      ctx.fillStyle='var(--red)'; ctx.fillRect(bx,by,bw*(t.hp/(t.maxHp||100)),bh);
    }
  });
  // VIP
  if(G.vip&&G.vip.alive){
    ctx.save(); ctx.font='36px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.shadowColor='rgba(0,255,136,.6)'; ctx.shadowBlur=14; ctx.fillText('🧑',G.vip.x,G.vip.y); ctx.restore();
    const bw=50,bh=5,bx=G.vip.x-bw/2,by=G.vip.y-28;
    ctx.fillStyle='rgba(0,0,0,.55)'; ctx.fillRect(bx,by,bw,bh);
    ctx.fillStyle='#00ff88'; ctx.fillRect(bx,by,bw*(G.vip.hp/G.vip.maxHp),bh);
    ctx.fillStyle='rgba(0,255,136,.4)'; ctx.font='7px Orbitron,monospace'; ctx.textAlign='center'; ctx.fillText('VIP',G.vip.x,by-4);
  }
}

function drawBulletTracers(){
  for(const b of G.bullets){
    ctx.save(); ctx.globalAlpha=b.life*.85;
    ctx.strokeStyle='rgba(255,220,100,.7)'; ctx.lineWidth=1.5;
    ctx.shadowColor='rgba(255,200,50,.5)'; ctx.shadowBlur=5;
    ctx.beginPath(); ctx.moveTo(b.x,b.y); ctx.lineTo(b.tx,b.ty); ctx.stroke();
    ctx.restore();
  }
}

function drawParts(){
  for(const p of PARTS){
    ctx.save(); ctx.globalAlpha=Math.max(0,p.life);
    if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}
    ctx.fillStyle=p.col; ctx.beginPath(); ctx.arc(p.x,p.y,p.sz*Math.max(.08,p.life),0,Math.PI*2); ctx.fill();
    if(p.glow)ctx.shadowBlur=0; ctx.restore();
  }
}
function drawHits(){
  for(const h of HITS){
    ctx.save(); ctx.globalAlpha=Math.max(0,h.life);
    ctx.shadowColor=h.col; ctx.shadowBlur=8; ctx.fillStyle=h.col;
    ctx.font="bold 12px 'Black Han Sans',sans-serif"; ctx.textAlign='center';
    ctx.fillText(h.txt,h.x,h.y); ctx.restore();
  }
}

// ================================================================
//  AMMO DISPLAY
// ================================================================
function buildAmmoDisplay(){
  const ac=document.getElementById('ammo-col'); ac.innerHTML='';
  const w=WDEFS[G.wIdx];
  const cur=G.ammo[G.wIdx];
  const max=w.mag;
  if(w.unlimited){ ac.innerHTML='<div style="font-family:Black Han Sans,sans-serif;font-size:12px;color:var(--cyan);letter-spacing:1px">∞</div>'; return; }
  for(let i=0;i<Math.min(max,30);i++){
    const d=document.createElement('div'); d.className='adot'+(i<cur?' live':''); ac.appendChild(d);
  }
}

// ================================================================
//  MAIN LOOP
// ================================================================
function loop(){
  if(!G.running) return;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  drawBulletTracers();
  drawTargets();
  drawParts(); drawHits();
  drawScope();
  drawCrosshair();
  update();
  requestAnimationFrame(loop);
}

// ================================================================
//  TITLE
// ================================================================
function showTitle(){
  const best=parseInt(localStorage.getItem('snipeBest')||'0');
  const tags=['🎯 4배율 조준경','💨 실시간 바람 탄도','🫁 호흡 안정화','💀 헤드샷 슬로우모션','🔫 4종 무기','📡 6개 미션','👹 VIP 경호·보스','🔥 킬체인 보너스','📏 최장 저격 기록','⛈️ 날씨 시스템','🔴 급소 판정','🩸 혈흔 시스템'];
  const tp=[...tags,...tags].map((t,i)=>`<span class="tpill ${['c','g','r','p'][i%4]}">${t}</span>`).join('');
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'],ddesc=['바람 없음·넓은 판정','바람+흔들림','강풍+작은 판정'];
  const msListHTML=MISSIONS.map((ms,i)=>`
    <div class="ml-item">
      <div class="ml-ico">${ms.icon}</div>
      <div class="ml-info"><div class="ml-name">${ms.name}</div><div class="ml-desc">${ms.desc}</div></div>
    </div>`).join('');
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">SNIPER ELITE v3.0</div>
    <div class="ov-title" style="color:var(--green)">🎯 스나이퍼<br>엘리트</div>
    <div class="ov-sub">6 MISSIONS · BALLISTICS · HEADSHOT</div>
    <div class="tag-strip"><div class="tag-inner">${tp}</div></div>
    <div style="font-size:8px;color:#336;margin-bottom:8px;letter-spacing:2px">미션 목록</div>
    <div class="mission-list">${msListHTML}</div>
    <div style="font-size:8px;color:#336;margin-bottom:8px;letter-spacing:2px">난이도</div>
    <div class="diff-row">${dnames.map((n,i)=>`<div class="dt${i===G.diffLv?' sel':''}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:2px">${ddesc[i]}</div></div>`).join('')}</div>
    <div style="font-size:8px;color:#334;line-height:2.3;margin-bottom:12px">
      우클릭(또는 🔭) — 조준경 전환 &nbsp;|&nbsp; HOLD/Shift — 호흡 유지<br>
      클릭/스페이스/🔫 — 발사 &nbsp;|&nbsp; R/🔄 — 재장전<br>
      1~4 키/🔀 — 무기 변경 &nbsp;|&nbsp; 바람 방향 보정 후 저격!
    </div>
    ${best>0?`<div style="font-size:9px;color:#446;margin-bottom:12px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>`:''}
    <button class="ov-btn" onclick="startGame()">임무 시작 🎯</button>`;
  document.getElementById('overlay').style.display='flex';
}

window.setDiff=d=>{G.diffLv=d;document.querySelectorAll('.dt').forEach((t,i)=>t.classList.toggle('sel',i===d));};
window.startGame=()=>{
  document.getElementById('overlay').style.display='none';
  initGame(); requestAnimationFrame(loop);
};
window.showTitle=showTitle;

// ================================================================
//  INPUT
// ================================================================
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  G.mouse.x=e.clientX-r.left; G.mouse.y=e.clientY-r.top;
  if(G.scoped){G.scopeX=G.mouse.x;G.scopeY=G.mouse.y;}
});
canvas.addEventListener('mousedown',e=>{if(G.running&&!G.missionComplete)fire();});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G.running)G.scoped=!G.scoped;});
canvas.addEventListener('touchmove',e=>{e.preventDefault();
  const t=e.touches[0]; const r=canvas.getBoundingClientRect();
  G.mouse.x=t.clientX-r.left; G.mouse.y=t.clientY-r.top;
  if(G.scoped){G.scopeX=G.mouse.x;G.scopeY=G.mouse.y;}
},{passive:false});
canvas.addEventListener('touchend',e=>{e.preventDefault();if(G.running&&G.scoped&&!G.missionComplete)fire();},{passive:false});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift')G.breathHeld=true;
  if((e.key==='r'||e.key==='R')&&G.running)startReload();
  if(e.key==='z'||e.key==='Z'||e.key==='Escape'){if(G.running)G.scoped=!G.scoped;}
  if(e.key===' '){e.preventDefault();if(G.running&&!G.missionComplete)fire();}
  if(e.key==='1')switchWeapon(0);if(e.key==='2')switchWeapon(1);
  if(e.key==='3')switchWeapon(2);if(e.key==='4')switchWeapon(3);
});
document.addEventListener('keyup',e=>{if(e.key==='Shift')G.breathHeld=false;});

// Touch buttons
function addT(id,dn,up){
  const el=document.getElementById(id);if(!el)return;
  const d=e=>{e.preventDefault();if(dn)dn();};
  const u=e=>{e.preventDefault();if(up)up();};
  el.addEventListener('touchstart',d,{passive:false});el.addEventListener('touchend',u,{passive:false});
  el.addEventListener('mousedown',d);el.addEventListener('mouseup',u);
}
addT('tch-scope',()=>{if(G.running)G.scoped=!G.scoped;},null);
addT('tch-fire',()=>{if(G.running&&!G.missionComplete)fire();},null);
addT('tch-reload',()=>{if(G.running)startReload();},null);
addT('tch-hold',()=>G.breathHeld=true,()=>G.breathHeld=false);
addT('tch-weapon',()=>{if(G.running)switchWeapon((G.wIdx+1)%WDEFS.length);},null);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
