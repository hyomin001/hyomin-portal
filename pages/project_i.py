import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<title>Age of War — 전선 돌파 저격전</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Rajdhani:wght@500;700;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--grn:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--bg:#06080a;--blue:#4488ff;}
html,body{width:100%;height:100vh;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:100vh;overflow:hidden;}
canvas{display:block;}

/* ── CUSTOM CURSOR (숨기고 캔버스에서 그림) ── */
.in-game, .in-game * { cursor: none !important; }

/* ── CTRL BAR ── */
#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,.92);border-bottom:1px solid rgba(255,255,255,.06);display:flex;justify-content:center;align-items:center;gap:10px;padding:3px 10px;font-size:9px;color:#556;flex-wrap:wrap;}
#ctrl-bar b{color:#f5c518;}

/* ── HUD TOP ── */
#hud{position:absolute;top:24px;left:0;right:0;z-index:100;pointer-events:none;display:flex;gap:4px;padding:4px 8px;align-items:stretch;}
.hb{background:rgba(0,0,0,.82);border:1px solid rgba(255,255,255,.08);border-radius:6px;padding:3px 8px;text-align:center;min-width:48px;}
.hv{font-family:'Rajdhani',sans-serif;font-size:14px;font-weight:900;color:var(--gold);}
.hl{font-size:7px;color:#334;letter-spacing:.8px;text-transform:uppercase;}
#frontline-wrap{flex:1;margin:0 6px;display:flex;flex-direction:column;justify-content:center;}
#fl-label{display:flex;justify-content:space-between;font-size:7px;color:#334;margin-bottom:3px;}
#fl-track{height:10px;background:rgba(255,255,255,.04);border-radius:99px;overflow:hidden;position:relative;border:1px solid rgba(255,255,255,.06);}
#fl-ally{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,#0033cc,#2266ff,#44aaff);transition:width .35s;}
#fl-enemy{position:absolute;top:0;right:0;height:100%;background:linear-gradient(270deg,#880000,#cc2200,#ff4400);transition:width .35s;}
#fl-mid{position:absolute;top:-1px;bottom:-1px;width:3px;background:#fff;border-radius:2px;transition:left .35s;transform:translateX(-50%);box-shadow:0 0 6px #fff;}

/* ── AMMO STRIP ── */
#ammo-strip{position:absolute;top:72px;right:10px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;align-items:flex-end;}
.ammo-pip{width:6px;height:18px;border-radius:2px;background:#f5c518;border:1px solid rgba(255,255,255,.2);box-shadow:0 0 4px rgba(245,197,24,.4);transition:all .15s;}
.ammo-pip.empty{background:#1a1a1a;border-color:#333;box-shadow:none;}

/* ── PLAYER HP BAR ── */
#php-wrap{position:absolute;left:8px;bottom:14px;z-index:100;pointer-events:none;width:150px;}
#php-label{font-size:7px;color:#445;letter-spacing:1px;margin-bottom:3px;display:flex;justify-content:space-between;}
#php-track{height:8px;background:rgba(0,0,0,.5);border-radius:99px;overflow:hidden;border:1px solid rgba(0,255,100,.1);}
#php-fill{height:100%;background:linear-gradient(90deg,#00aa44,#00ff88);border-radius:99px;transition:width .3s;}

/* ── AGGRO ── */
#aggro-wrap{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;width:320px;}
#aggro-row{display:flex;justify-content:space-between;font-size:8px;color:#445;margin-bottom:3px;}
.at{color:#ff8844;}
#aggro-track{height:11px;background:rgba(0,0,0,.5);border-radius:99px;overflow:hidden;border:1px solid rgba(255,100,50,.15);}
#aggro-fill{height:100%;border-radius:99px;transition:width .08s;}
#aggro-txt{font-size:8px;text-align:center;margin-top:3px;color:#445;letter-spacing:.8px;}

/* ── ALLY SUMMON PANEL ── */
#summon-panel{position:absolute;left:0;top:64px;bottom:50px;width:120px;z-index:100;display:flex;flex-direction:column;gap:4px;padding:6px 6px;background:rgba(0,0,0,.7);border-right:1px solid rgba(0,255,136,.12);}
#summon-title{font-size:7px;color:#0f9;letter-spacing:1px;text-align:center;margin-bottom:4px;border-bottom:1px solid rgba(0,255,136,.15);padding-bottom:4px;}
#resource-row{display:flex;align-items:center;justify-content:center;gap:4px;font-family:'Rajdhani',sans-serif;font-size:13px;font-weight:900;color:#f5c518;margin-bottom:5px;}
#resource-ico{font-size:10px;}
.summon-btn{background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.25);border-radius:5px;padding:4px 5px;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;gap:2px;user-select:none;}
.summon-btn:hover{background:rgba(0,255,136,.18);border-color:#00ff88;box-shadow:0 0 8px rgba(0,255,136,.25);}
.summon-btn:active{transform:scale(0.95);}
.summon-btn.disabled{opacity:.3;cursor:not-allowed;}
.sb-ico{font-size:14px;}
.sb-name{font-size:7px;color:#aaa;letter-spacing:.5px;}
.sb-cost{font-size:7px;color:#f5c518;font-family:'Rajdhani',sans-serif;font-weight:700;}
.sb-effect{font-size:6px;color:#446;margin-top:1px;}
#summon-cd{font-size:7px;color:#334;text-align:center;margin-top:3px;}

/* ── COVER BTN ── */
#cover-btn{position:absolute;bottom:14px;right:10px;z-index:100;background:rgba(0,0,0,.8);border:1px solid rgba(0,255,136,.25);border-radius:7px;padding:5px 13px;font-family:'Rajdhani',sans-serif;font-size:11px;color:#00ff88;cursor:pointer;letter-spacing:1px;user-select:none;transition:all .12s;}
#cover-btn.active{background:rgba(0,255,136,.12);border-color:#00ff88;box-shadow:0 0 12px rgba(0,255,136,.35);}

/* ── SCOPE MODE — 전체화면 오버레이 방식 ── */
/* 스코프는 캔버스 위에 직접 그려지므로 별도 DOM 없음 */
#scope-info-hud{position:absolute;bottom:60px;right:10px;z-index:110;pointer-events:none;display:none;flex-direction:column;align-items:flex-end;gap:3px;}
#scope-info-hud .si{font-family:'Rajdhani',sans-serif;font-size:10px;color:rgba(0,255,100,.8);letter-spacing:2px;text-align:right;}
#breath-wrap{position:absolute;bottom:46px;right:10px;z-index:110;pointer-events:none;display:none;width:140px;}
#breath-lbl{font-size:7px;color:#334;text-align:center;margin-bottom:2px;letter-spacing:1px;}
#breath-track{height:4px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:#00ff88;transition:width .05s;}

/* ── OVERLAYS ── */
#warning-flash{position:absolute;inset:0;z-index:190;pointer-events:none;opacity:0;background:rgba(255,0,40,.4);transition:opacity .08s;}
#cover-vignette{position:absolute;inset:0;z-index:40;pointer-events:none;background:radial-gradient(ellipse 55% 45% at 50% 50%,transparent 35%,rgba(0,0,0,.75) 100%);opacity:0;transition:opacity .3s;}
#cover-vignette.on{opacity:1;}
#muzzle-flash{position:absolute;inset:0;z-index:35;pointer-events:none;opacity:0;background:radial-gradient(ellipse at 8% 90%,rgba(255,220,100,.2),transparent 38%);transition:opacity .05s;}

/* ── TOAST ── */
#toast-wrap{position:absolute;top:58px;left:50%;transform:translateX(-50%);z-index:280;display:flex;flex-direction:column;gap:5px;align-items:center;pointer-events:none;}
.toast-item{background:rgba(4,12,4,.97);border:1px solid rgba(245,197,24,.35);border-radius:4px;padding:5px 14px;font-size:10px;color:var(--gold);letter-spacing:1px;white-space:nowrap;animation:toastSlide .2s ease,toastFade .4s ease 1.6s forwards;}
@keyframes toastSlide{from{transform:translateY(-14px);opacity:0}to{transform:none;opacity:1}}
@keyframes toastFade{to{opacity:0}}
.toast-item.red{border-color:rgba(255,50,50,.4);color:#ff6666;}
.toast-item.grn{border-color:rgba(0,255,100,.4);color:#00ff88;}
.toast-item.blue{border-color:rgba(0,200,255,.4);color:#00d4ff;}

/* ── KILL FEED ── */
#killfeed{position:absolute;top:68px;right:8px;z-index:200;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kf{background:rgba(0,0,0,.85);border-left:3px solid #ff4444;border-radius:3px;padding:3px 8px;font-size:9px;color:#bbb;animation:kfIn .2s ease;}
@keyframes kfIn{from{transform:translateX(20px);opacity:0}to{transform:none;opacity:1}}

/* ── DAMAGE NUMBERS ── */
.dnum{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dUp .85s ease forwards;z-index:300;text-shadow:1px 2px 5px rgba(0,0,0,.95);}
@keyframes dUp{0%{opacity:1;transform:translateY(0) scale(1)}40%{opacity:1;transform:translateY(-22px) scale(1.15)}100%{opacity:0;transform:translateY(-52px) scale(.7)}}

/* ── DETECTED BANNER ── */
#det-banner{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%) scale(.6);opacity:0;z-index:250;pointer-events:none;background:rgba(180,0,0,.94);border:2px solid #ff3333;border-radius:8px;padding:10px 28px;font-family:'Black Han Sans',sans-serif;font-size:1.3rem;color:#fff;letter-spacing:4px;transition:all .18s;box-shadow:0 0 40px rgba(255,0,0,.4);}
#det-banner.show{transform:translate(-50%,-50%) scale(1);opacity:1;}

/* ── WAR CRY ── */
#war-cry{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);z-index:240;font-family:'Black Han Sans',sans-serif;font-size:1.5rem;color:#00ff88;text-shadow:0 0 18px rgba(0,255,136,.9),0 0 40px rgba(0,255,136,.4);pointer-events:none;opacity:0;transition:opacity .25s;letter-spacing:4px;white-space:nowrap;text-align:center;}
#war-cry.show{opacity:1;}

/* ── AGE BANNER ── */
#age-banner{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.7);opacity:0;z-index:260;pointer-events:none;text-align:center;transition:all .3s;}
#age-banner.show{transform:translate(-50%,-50%) scale(1);opacity:1;}
.ab-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;letter-spacing:6px;text-shadow:0 0 40px currentColor;}
.ab-sub{font-size:.8rem;letter-spacing:3px;margin-top:5px;opacity:.8;}

/* ── MISSION SCREEN ── */
#mission-ov{position:absolute;inset:0;z-index:300;background:radial-gradient(ellipse at 50% 30%,#0a1a0a,#050a05 70%);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;}
.mo-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;color:var(--gold);letter-spacing:8px;text-shadow:0 0 30px rgba(245,197,24,.5);margin-bottom:3px;}
.mo-sub{font-size:.65rem;color:#223;letter-spacing:3px;margin-bottom:16px;}
.mission-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:7px;max-width:760px;width:100%;margin-bottom:14px;padding:0 8px;}
.mis-card{background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:9px 5px;cursor:pointer;transition:all .16s;text-align:center;position:relative;overflow:hidden;}
.mis-card:hover,.mis-card.sel{border-color:rgba(245,197,24,.45);background:rgba(245,197,24,.04);box-shadow:0 0 16px rgba(245,197,24,.08);}
.mis-card.locked{opacity:.2;cursor:default;}
.mc-num{font-family:'Rajdhani',sans-serif;font-size:17px;font-weight:900;color:var(--gold);}
.mc-name{font-family:'Black Han Sans',sans-serif;font-size:8px;color:#99a;margin:2px 0 1px;letter-spacing:1px;}
.mc-diff{font-size:6px;color:#334;}
.mc-desc{font-size:6px;color:#223;margin-top:2px;line-height:1.4;}
.mc-clr{font-size:7px;color:#0f9;margin-top:2px;}
.mo-start{padding:10px 42px;background:linear-gradient(135deg,#132800,#1e4400);border:1px solid #2a6600;border-radius:5px;color:#77ee33;font-family:'Black Han Sans',sans-serif;font-size:12px;letter-spacing:4px;cursor:pointer;transition:all .18s;}
.mo-start:hover:not(:disabled){transform:scale(1.04);filter:brightness(1.25);}
.mo-start:disabled{opacity:.25;cursor:default;}

/* ── RESULT ── */
#result-ov{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.94);backdrop-filter:blur(4px);display:none;flex-direction:column;align-items:center;justify-content:center;gap:10px;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:1.8rem;letter-spacing:5px;}
.res-grade{font-family:'Rajdhani',sans-serif;font-size:4rem;font-weight:900;line-height:1;text-shadow:0 0 40px currentColor;}
.res-stats{display:grid;grid-template-columns:1fr 1fr;gap:6px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.06);border-radius:8px;padding:12px 18px;min-width:280px;}
.rs{font-size:10px;color:#445;display:flex;justify-content:space-between;gap:12px;}
.rs b{color:var(--gold);}
.res-btns{display:flex;gap:8px;}
.rbtn{padding:7px 22px;border:none;border-radius:5px;cursor:pointer;font-family:'Black Han Sans',sans-serif;font-size:11px;letter-spacing:2px;transition:all .14s;}
.rbtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.rbtn.retry{background:linear-gradient(135deg,#132800,#1e4400);color:#77ee33;border:1px solid #2a6600;}
.rbtn.back{background:rgba(255,255,255,.04);color:#445;border:1px solid rgba(255,255,255,.08);}

/* ── SUMMON BURST EFFECT ── */
.summon-burst{position:fixed;pointer-events:none;border-radius:50%;border:2px solid #00ff88;animation:sburst .5s ease-out forwards;z-index:500;}
@keyframes sburst{from{transform:scale(0.2);opacity:1}to{transform:scale(2.5);opacity:0}}

/* ── AGE INDICATOR ── */
#age-indicator{position:absolute;top:68px;left:130px;z-index:110;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-size:10px;letter-spacing:2px;padding:3px 10px;border-radius:4px;border:1px solid currentColor;opacity:.85;}
</style>
</head>
<body>
<div id="root">
<canvas id="gc"></canvas>

<!-- SCOPE INFO HUD (DOM, 스코프 켤 때만 표시) -->
<div id="scope-info-hud">
  <div class="si" id="si-dist">---m</div>
  <div class="si" id="si-ammo">--/--</div>
</div>
<div id="breath-wrap">
  <div id="breath-lbl">BREATH HOLD</div>
  <div id="breath-track"><div id="breath-fill" style="width:100%"></div></div>
</div>

<div id="ctrl-bar">
  <span><b>클릭/SPACE</b> 발사</span><span>|</span>
  <span><b>우클릭/Z</b> 스코프(마우스=조준점)</span><span>|</span>
  <span><b>C</b> 엄폐</span><span>|</span>
  <span><b>R</b> 재장전</span><span>|</span>
  <span><b>SHIFT</b> 숨참기</span><span>|</span>
  <span><b>1~5</b> 병력 소환</span>
</div>

<div id="hud">
  <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
  <div class="hb"><div class="hv" id="kill-v">0</div><div class="hl">킬</div></div>
  <div class="hb"><div class="hv" id="timer-v">--:--</div><div class="hl">TIME</div></div>
  <div class="hb"><div class="hv" id="ally-hp-v">100%</div><div class="hl">아군HP</div></div>
  <div class="hb"><div class="hv" id="res-v" style="color:#00d4ff">100</div><div class="hl">자원</div></div>
  <div id="frontline-wrap">
    <div id="fl-label"><span>🔵 아군</span><span id="fl-pct-txt">50%</span><span>적군 🔴</span></div>
    <div id="fl-track">
      <div id="fl-ally"></div>
      <div id="fl-enemy"></div>
      <div id="fl-mid"></div>
    </div>
  </div>
</div>

<!-- AGE INDICATOR -->
<div id="age-indicator"></div>

<!-- AMMO STRIP -->
<div id="ammo-strip"></div>

<!-- ALLY SUMMON PANEL -->
<div id="summon-panel">
  <div id="summon-title">🪖 병력 소환</div>
  <div id="resource-row"><span id="resource-ico">💎</span><span id="resource-val">100</span></div>
  <div id="summon-btns"></div>
  <div id="summon-cd"></div>
</div>

<!-- PLAYER HP -->
<div id="php-wrap">
  <div id="php-label"><span>저격수 HP</span><span id="php-pct">100%</span></div>
  <div id="php-track"><div id="php-fill"></div></div>
</div>

<!-- AGGRO -->
<div id="aggro-wrap">
  <div id="aggro-row"><span class="at">⚠ 발각 위험도</span><span id="aggro-pct">0%</span></div>
  <div id="aggro-track"><div id="aggro-fill" style="width:0%"></div></div>
  <div id="aggro-txt">은폐 유지 중 — 안전</div>
</div>

<div id="cover-btn" onmousedown="setCover(true)" onmouseup="setCover(false)" ontouchstart="setCover(true)" ontouchend="setCover(false)">[ C ] 엄폐</div>

<div id="cover-vignette"></div>
<div id="muzzle-flash"></div>
<div id="warning-flash"></div>
<div id="det-banner">💥 발각됨!</div>
<div id="war-cry"></div>
<div id="age-banner"><div class="ab-title" id="ab-title"></div><div class="ab-sub" id="ab-sub"></div></div>
<div id="toast-wrap"></div>
<div id="killfeed"></div>

<!-- MISSION -->
<div id="mission-ov">
  <div class="mo-title">⚔️ AGE of WAR — 저격 지원</div>
  <div class="mo-sub">전쟁의 시대 · 라인 배틀 + 스나이퍼 지원</div>
  <div class="mission-grid" id="mission-grid"></div>
  <button class="mo-start" id="mo-start-btn" disabled onclick="startMission()">작전 개시 ▶</button>
</div>

<!-- RESULT -->
<div id="result-ov">
  <div class="res-title" id="res-title"></div>
  <div class="res-grade" id="res-grade"></div>
  <div class="res-stats" id="res-stats"></div>
  <div class="res-btns">
    <button class="rbtn retry" onclick="retryMission()">재시도 ↺</button>
    <button class="rbtn back" onclick="gotoTitle()">타이틀</button>
  </div>
</div>
</div>

<script>
'use strict';
// ══════════════════════════════════════════════════════
//  AGE of WAR — 전선 라인배틀 + 스나이퍼 지원
//  스코프: 마우스 커서 = 조준점 정중앙 (캔버스 직접 렌더링)
// ══════════════════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
let GW = window.innerWidth, GH = window.innerHeight;
canvas.width = GW; canvas.height = GH;

// ── 시대(AGE) 정의 — Age of War 스타일 ────────────────
const AGES = [
  { id:0, name:'석기 시대',    color:'#aa8844', bgSky:['#1a1208','#2a1e10'], bgGnd:['#1a1008','#0e0a04'], unitStyle:'primitive'  },
  { id:1, name:'고대 시대',    color:'#cc9922', bgSky:['#0a1220','#1a2030'], bgGnd:['#181408','#0e0c04'], unitStyle:'ancient'    },
  { id:2, name:'중세 시대',    color:'#8899aa', bgSky:['#060e1a','#0e182a'], bgGnd:['#0e1208','#080e04'], unitStyle:'medieval'   },
  { id:3, name:'르네상스',     color:'#aa6622', bgSky:['#081420','#102030'], bgGnd:['#0a1004','#080c04'], unitStyle:'renaissance'},
  { id:4, name:'산업 혁명',    color:'#888888', bgSky:['#060808','#0e1010'], bgGnd:['#080808','#040404'], unitStyle:'industrial' },
  { id:5, name:'근현대전',     color:'#445566', bgSky:['#04080a','#080f12'], bgGnd:['#060a04','#040804'], unitStyle:'modern'     },
  { id:6, name:'SF 미래전',    color:'#0088ff', bgSky:['#020408','#040810'], bgGnd:['#020408','#020406'], unitStyle:'future'     },
];

// ── 병력 유닛 정의 (시대별 외관 변화) ─────────────────
const ALLY_UNITS = [
  { id:'warrior',  name:'전사',    cost:15, key:'1', ico:'⚔️', hp:90,  fireRate:1.4, dmg:16, speed:0.28, effect:'기본 근접 전사',   color:'#2255aa' },
  { id:'archer',   name:'궁수',    cost:20, key:'2', ico:'🏹', hp:55,  fireRate:1.0, dmg:12, speed:0.20, effect:'원거리 공격수',    color:'#44aa22' },
  { id:'knight',   name:'기사',    cost:40, key:'3', ico:'🛡️', hp:220, fireRate:1.8, dmg:28, speed:0.12, effect:'고체력 방패전사', color:'#8844ff' },
  { id:'medic',    name:'의무병',  cost:25, key:'4', ico:'🏥', hp:70,  fireRate:3.0, dmg:5,  speed:0.18, effect:'아군 HP 회복',     color:'#00ffaa', isHeal:true },
  { id:'sniper_a', name:'아군저격', cost:45, key:'5', ico:'🎯', hp:55,  fireRate:3.8, dmg:90, speed:0.10, effect:'고데미지 저격병',  color:'#aaff44' },
];

// ── 미션 정의 (시대 진행 포함) ────────────────────────
const MISSIONS = [
  { id:1,  name:'부족 전쟁',      diff:'⭐',      timeLimit:100, startLine:500, allyN:6,  enemyN:8,  reward:3_000_000,   resource:60,  ageId:0, keyTargets:[{type:'mg',n:1}],                            desc:'석기 부족의 침략을 막아라.' },
  { id:2,  name:'성벽 공방',      diff:'⭐⭐',     timeLimit:120, startLine:515, allyN:8,  enemyN:12, reward:8_000_000,   resource:70,  ageId:1, keyTargets:[{type:'mg',n:2},{type:'officer',n:1}],       desc:'고대 성곽 전투. 장교를 노려라.' },
  { id:3,  name:'십자군 원정',    diff:'⭐⭐⭐',    timeLimit:150, startLine:530, allyN:10, enemyN:18, reward:18_000_000,  resource:80,  ageId:2, keyTargets:[{type:'mg',n:2},{type:'officer',n:2},{type:'sniper_e',n:1}], desc:'중세 전장. 적 궁병을 제거하라.' },
  { id:4,  name:'화약 전쟁',      diff:'⭐⭐⭐⭐',   timeLimit:180, startLine:545, allyN:7,  enemyN:25, reward:40_000_000,  resource:90,  ageId:3, keyTargets:[{type:'mg',n:3},{type:'officer',n:2},{type:'sniper_e',n:2}], desc:'머스킷 소총 시대. 정밀 사격 필요.' },
  { id:5,  name:'산업 대전',      diff:'⭐⭐⭐⭐⭐',  timeLimit:200, startLine:560, allyN:12, enemyN:30, reward:80_000_000,  resource:100, ageId:4, keyTargets:[{type:'mg',n:3},{type:'officer',n:3},{type:'sniper_e',n:2},{type:'general',n:1}], desc:'증기기관 시대. 기관총 진지를 격파.' },
  { id:6,  name:'참호전',         diff:'⭐⭐⭐⭐⭐',  timeLimit:220, startLine:575, allyN:9,  enemyN:35, reward:130_000_000, resource:110, ageId:5, keyTargets:[{type:'mg',n:4},{type:'officer',n:3},{type:'sniper_e',n:3},{type:'general',n:1}], desc:'세계대전 참호. 기관총수를 처리하라.' },
  { id:7,  name:'도심 침공',      diff:'💀 극한',  timeLimit:240, startLine:590, allyN:8,  enemyN:40, reward:200_000_000, resource:120, ageId:5, keyTargets:[{type:'mg',n:4},{type:'officer',n:4},{type:'sniper_e',n:3},{type:'general',n:2}], desc:'현대 도시 전투. 특수부대를 저지.' },
  { id:8,  name:'해안 상륙작전',  diff:'💀 극한',  timeLimit:260, startLine:605, allyN:14, enemyN:45, reward:350_000_000, resource:130, ageId:5, keyTargets:[{type:'mg',n:5},{type:'officer',n:4},{type:'sniper_e',n:4},{type:'general',n:2}], desc:'해안 교두보 확보. 대규모 전투.' },
  { id:9,  name:'미래 전쟁',      diff:'🔥 전설',  timeLimit:280, startLine:620, allyN:10, enemyN:55, reward:600_000_000, resource:140, ageId:6, keyTargets:[{type:'mg',n:5},{type:'officer',n:5},{type:'sniper_e',n:5},{type:'general',n:3}], desc:'SF 로봇 전쟁. 에너지 무기 주의.' },
  { id:10, name:'최후의 전쟁',    diff:'⚡ 신화',  timeLimit:300, startLine:640, allyN:12, enemyN:65, reward:1_000_000_000,resource:150, ageId:6, keyTargets:[{type:'mg',n:6},{type:'officer',n:5},{type:'sniper_e',n:5},{type:'general',n:4}], desc:'세계의 운명이 걸린 최후의 전쟁.' },
];

const ECFG = {
  infantry: { name:'보병',     hp:80,  xp:80,   sz:10, key:false, mgSupp:0,  moraleBoost:0,  speed:0.3  },
  mg:       { name:'기관총병', hp:140, xp:400,  sz:12, key:true,  mgSupp:10, moraleBoost:0,  speed:0    },
  officer:  { name:'장교',     hp:180, xp:500,  sz:11, key:true,  mgSupp:0,  moraleBoost:18, speed:0.25 },
  sniper_e: { name:'적저격수', hp:90,  xp:600,  sz:9,  key:true,  mgSupp:0,  moraleBoost:0,  speed:0.18 },
  general:  { name:'총사령관', hp:350, xp:2000, sz:14, key:true,  mgSupp:0,  moraleBoost:32, speed:0.18 },
};

let G=null, selMis=null, RAF, lastTs=0, gTimer=0;

// ── SCOPE 상태 ─────────────────────────────────────────
// 스코프는 별도 DOM 없이 캔버스에 직접 그린다.
// mouseX, mouseY가 항상 조준점 중앙.
const SCOPE_RADIUS = Math.min(GW, GH) * 0.28; // 화면 비율로 동적 설정
let scopeR = SCOPE_RADIUS;

// ── INIT ──────────────────────────────────────────────
function initGame(midx) {
  const mis = MISSIONS[midx];
  scopeR = Math.min(GW, GH) * 0.28;
  G = {
    midx, mis, phase:'play',
    time: mis.timeLimit,
    score:0, kills:0, keyKills:0, headshots:0,
    playerHP:100, allyHP:100,
    frontlineX: mis.startLine,
    allies:[], enemies:[], particles:[], tracers:[],
    aggro:0, coverActive:false,
    isDetected:false, detectedTimer:0,
    suppressionLevel:0, enemyMorale:50,
    warCryTimer:0,
    shakeX:0, shakeY:0,
    scoped:false, breathHeld:false, breathTimer:3,
    swayX:0, swayY:0, swayT:0,
    shootCd:0, ammo:5, maxAmmo:5,
    reloading:false, reloadTimer:0, reloadDur:2.2,
    mouse:{x:GW/2, y:GH/2},
    frame:0, done:false, failReason:'',
    muzzleFlash:0,
    resource: mis.resource,
    resourceMax: mis.resource,
    resourceRegen: 4.5,
    summonCd:0,
    ageId: mis.ageId,
    ageBannerTimer: 2.5,
    ageBannerShown: true,
  };
  for(let i=0;i<mis.allyN;i++) spawnAlly('warrior');
  for(const kt of mis.keyTargets) for(let j=0;j<kt.n;j++) spawnEnemy(kt.type);
  for(let i=0;i<mis.enemyN;i++) spawnEnemy('infantry');
  buildAmmoStrip();
  buildSummonPanel();
  updateHUD();
  // 시대 배너 표시
  showAgeBanner(AGES[mis.ageId]);
  updateAgeIndicator();
}

function showAgeBanner(age) {
  const el = document.getElementById('age-banner');
  document.getElementById('ab-title').textContent = '⚔ ' + age.name;
  document.getElementById('ab-title').style.color = age.color;
  document.getElementById('ab-sub').textContent = '새로운 전쟁 시대가 열렸다';
  el.classList.add('show');
  setTimeout(()=>el.classList.remove('show'), 2200);
}

function updateAgeIndicator() {
  if(!G) return;
  const age = AGES[G.ageId];
  const el = document.getElementById('age-indicator');
  el.textContent = '⚔ ' + age.name;
  el.style.color = age.color;
  el.style.borderColor = age.color;
  el.style.textShadow = `0 0 12px ${age.color}88`;
}

// ── SPAWN ──────────────────────────────────────────────
function spawnAlly(type, targetX, targetY) {
  const unit = ALLY_UNITS.find(u=>u.id===type)||ALLY_UNITS[0];
  const y = targetY||(115 + Math.random()*(GH-220));
  const x = targetX||(G.frontlineX - 20 - Math.random()*50);
  G.allies.push({
    unitType:type, x, y, targetY:y,
    hp:unit.hp, maxHp:unit.hp,
    fireTimer:unit.fireRate*(0.8+Math.random()*0.4),
    fireRate:unit.fireRate, dmg:unit.dmg, speed:unit.speed,
    isHeal:unit.isHeal||false, color:unit.color,
    phase:Math.random()*Math.PI*2,
    alive:true, dying:false, deathT:0,
    walkOff:Math.random()*0.4,
    spawnAnim:0.5,
  });
}

function spawnEnemy(type) {
  const c = ECFG[type];
  const y = 115 + Math.random()*(GH-220);
  const ahead = type==='general'?70:type==='mg'?22:type==='sniper_e'?50:20;
  const ex = G.frontlineX + ahead + Math.random()*60;
  const hp = c.hp + Math.round(c.hp*0.2*G.midx);
  G.enemies.push({
    type, x:ex, y, targetY:y,
    hp, maxHp:hp, sz:c.sz,
    xp:Math.round(c.xp*(1+G.midx*0.22)),
    key:c.key, mgSupp:c.mgSupp, moraleBoost:c.moraleBoost, speed:c.speed,
    name:c.name,
    alive:true, dying:false, deathT:0,
    phase:Math.random()*Math.PI*2,
    fireTimer:type==='mg'?0.15:0.7+Math.random()*1.8,
    snipeTimer:type==='sniper_e'?(5+Math.random()*8):0,
    moveTimer:1+Math.random()*3,
  });
}

// ── TICK ──────────────────────────────────────────────
function tick(dt) {
  if(!G||G.phase!=='play'||G.done) return;
  G.frame++; gTimer+=dt;
  G.time-=dt;
  G.swayT+=dt;
  G.shootCd=Math.max(0,G.shootCd-dt);
  G.muzzleFlash=Math.max(0,G.muzzleFlash-dt*8);
  G.summonCd=Math.max(0,G.summonCd-dt);
  G.resource=Math.min(G.resourceMax, G.resource+G.resourceRegen*dt);

  // Sway (스코프 시 마우스가 조준점이므로 sway는 경미하게)
  const sm=G.breathHeld?0.04:G.scoped?0.3:G.coverActive?1.2:1;
  G.swayX=(Math.sin(G.swayT*0.9)*4.5+Math.sin(G.swayT*2.3)*1.8)*sm;
  G.swayY=(Math.cos(G.swayT*0.74)*3.5+Math.cos(G.swayT*1.9)*1.5)*sm;

  // Breath
  if(G.breathHeld){G.breathTimer-=dt*0.35;if(G.breathTimer<=0){G.breathHeld=false;G.breathTimer=0;}}
  else G.breathTimer=Math.min(3,G.breathTimer+dt*0.48);

  // Reload
  if(G.reloading){
    G.reloadTimer-=dt;
    if(G.reloadTimer<=0){G.reloading=false;G.ammo=G.maxAmmo;showToast('탄창 장전 완료!','grn');buildAmmoStrip();updateHUD();}
    buildAmmoStrip();
  }

  // Aggro decay
  const decayRate=G.coverActive?44:G.scoped?2:5;
  G.aggro=Math.max(0,G.aggro-dt*decayRate);
  if(G.aggro>=100&&!G.isDetected) triggerDetection();
  if(G.isDetected){
    G.detectedTimer-=dt;
    G.shakeX=(Math.random()-.5)*14;G.shakeY=(Math.random()-.5)*14;
    if(G.detectedTimer<=0){
      G.isDetected=false;G.aggro=18;G.shakeX=G.shakeY=0;
      document.getElementById('det-banner').classList.remove('show');
      document.getElementById('warning-flash').style.opacity='0';
    }
  } else {G.shakeX*=0.82;G.shakeY*=0.82;}

  // Suppression
  let supp=0,morale=38;
  for(const e of G.enemies) if(e.alive){supp+=e.mgSupp;morale+=e.moraleBoost;}
  G.suppressionLevel=Math.min(100,supp);
  G.enemyMorale=Math.min(100,morale);

  tickFrontline(dt);
  tickAllies(dt);
  tickEnemies(dt);
  tickTracers(dt);
  tickParticles(dt);

  if(G.suppressionLevel>35) G.allyHP-=dt*(G.suppressionLevel-35)*0.055;
  G.allyHP=Math.max(0,Math.min(100,G.allyHP));
  if(G.warCryTimer>0){G.warCryTimer-=dt;if(G.warCryTimer<=0)document.getElementById('war-cry').classList.remove('show');}
  document.getElementById('muzzle-flash').style.opacity=G.muzzleFlash>0?G.muzzleFlash*0.7:0;

  updateHUD();
  checkEnd();
}

function triggerDetection() {
  G.isDetected=true;G.detectedTimer=2.5;
  const dmg=20+G.midx*4;
  G.playerHP=Math.max(0,G.playerHP-dmg);
  document.getElementById('det-banner').classList.add('show');
  document.getElementById('warning-flash').style.opacity='1';
  setTimeout(()=>document.getElementById('warning-flash').style.opacity='0',600);
  showKF('💥 발각! 적 포격 개시!','#ff3333');
  showToast('발각됨! 엄폐하라!','red');
  for(let i=0;i<14;i++) addParticle(60+Math.random()*160,130+Math.random()*(GH-220),'#ff6600','exp');
  sfx_detected();
}

function tickFrontline(dt) {
  const mgAlive=G.enemies.filter(e=>e.alive&&e.type==='mg').length;
  const allyAlive=G.allies.filter(a=>a.alive).length;
  let push=0;
  if(mgAlive===0) push=5+(G.enemyMorale<55?7:0);
  else push=-2.2*mgAlive;
  const enemyPush=(G.enemyMorale/100)*2.2;
  const aStr=Math.max(0.25,allyAlive/G.mis.allyN);
  const net=(push*aStr)-enemyPush;
  G.frontlineX=Math.max(130,Math.min(GW-80,G.frontlineX+net*dt));
  for(const a of G.allies){if(!a.alive)continue;a.x+=(G.frontlineX-22-Math.random()*30-a.x)*dt*1.6;}
  for(const e of G.enemies){
    if(!e.alive||e.dying||e.type==='mg')continue;
    const tx=G.frontlineX+20+Math.random()*35;
    e.x+=(tx-e.x)*dt*1.3;
  }
}

function tickAllies(dt) {
  if(G.frame%350===0&&G.allies.filter(a=>a.alive).length<Math.max(2,Math.floor(G.mis.allyN*0.4))&&G.allyHP>15) {
    spawnAlly('warrior');
  }
  for(const a of G.allies) {
    if(a.dying){a.deathT+=dt;if(a.deathT>0.7)a.alive=false;continue;}
    if(!a.alive)continue;
    if(a.spawnAnim>0) a.spawnAnim-=dt;
    a.phase+=dt*2.6;
    a.fireTimer-=dt;
    a.y+=(a.targetY-a.y)*dt*0.8;
    if(a.isHeal) {
      if(a.fireTimer<=0) {
        a.fireTimer=a.fireRate;
        for(const b of G.allies) {
          if(!b.alive||b===a) continue;
          if(Math.hypot(b.x-a.x,b.y-a.y)<120) {
            b.hp=Math.min(b.maxHp,b.hp+8);
            G.allyHP=Math.min(100,G.allyHP+0.5);
            addParticle(b.x,b.y,'#00ffaa','muzzle');
          }
        }
      }
    } else {
      if(a.fireTimer<=0) {
        a.fireTimer=a.fireRate*(0.9+Math.random()*0.2);
        const ne=nearestEnemy(a.x,a.y);
        if(ne&&ne.x-a.x<350) {
          addTracer(a.x+9,a.y,ne.x,ne.y,'#88aaff',false);
          addParticle(a.x+10,a.y,'#ffff99','muzzle');
          const dmg=a.dmg+Math.random()*a.dmg*0.3;
          ne.hp-=dmg;
          if(ne.hp<=0) killEnemy(ne,false);
        }
      }
    }
    a.y=Math.max(115,Math.min(GH-55,a.y+Math.sin(a.phase)*0.09));
  }
}

function tickEnemies(dt) {
  for(const e of G.enemies) {
    if(e.dying){e.deathT+=dt;if(e.deathT>0.7){e.dying=false;e.alive=false;}continue;}
    if(!e.alive)continue;
    e.phase+=dt*2.4;
    e.fireTimer-=dt;
    e.moveTimer-=dt;
    if(e.moveTimer<=0&&e.type!=='mg'){e.moveTimer=1.5+Math.random()*3;e.targetY=115+Math.random()*(GH-220);}
    e.y+=(e.targetY-e.y)*dt*0.9;
    if(e.fireTimer<=0) {
      e.fireTimer=e.type==='mg'?0.13:0.65+Math.random()*1.7;
      const na=nearestAlly(e.x,e.y);
      if(na&&e.x-na.x<360) {
        addTracer(e.x-9,e.y,na.x,na.y,'#ff8844',false);
        addParticle(e.x-10,e.y,'#ffaa44','muzzle');
        const dmg=(e.type==='mg'?4:8)+Math.random()*5;
        na.hp-=dmg;
        if(na.hp<=0){na.dying=true;na.deathT=0;G.allyHP-=9;addParticle(na.x,na.y,'#4488ff','blood');}
      }
    }
    if(e.type==='sniper_e'&&G.scoped&&!G.coverActive) {
      e.snipeTimer-=dt;
      if(e.snipeTimer<=0) {
        e.snipeTimer=4+Math.random()*7;
        G.aggro=Math.min(100,G.aggro+40);
        showKF('⚠ 적 저격수 역조준!','#ff5500');
        if(G.aggro>=80){G.playerHP-=10;showToast('적 저격수의 반격!','red');}
      }
    }
  }
}

function nearestEnemy(x,y){let b=null,d=Infinity;for(const e of G.enemies){if(!e.alive||e.dying)continue;const dd=Math.hypot(e.x-x,e.y-y);if(dd<d){d=dd;b=e;}}return b;}
function nearestAlly(x,y){let b=null,d=Infinity;for(const a of G.allies){if(!a.alive||a.dying)continue;const dd=Math.hypot(a.x-x,a.y-y);if(dd<d){d=dd;b=a;}}return b;}
function addTracer(x1,y1,x2,y2,col,isPlayer){G.tracers.push({x1,y1,x2,y2,col,isPlayer,life:isPlayer?0.22:0.1,maxLife:isPlayer?0.22:0.1});}
function tickTracers(dt){for(let i=G.tracers.length-1;i>=0;i--){G.tracers[i].life-=dt;if(G.tracers[i].life<=0)G.tracers.splice(i,1);}}
function tickParticles(dt){
  for(let i=G.particles.length-1;i>=0;i--){
    const p=G.particles[i];
    p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=100*dt;p.life-=dt;
    if(p.life<=0)G.particles.splice(i,1);
  }
}
function addParticle(x,y,col,type){
  const cnt=type==='exp'?14:type==='blood'?7:type==='muzzle'?4:3;
  for(let i=0;i<cnt;i++){
    const spd=type==='exp'?160:type==='blood'?80:type==='muzzle'?60:40;
    const angle=Math.random()*Math.PI*2;
    G.particles.push({x,y,vx:Math.cos(angle)*spd*(0.3+Math.random()*0.7),vy:Math.sin(angle)*spd*(0.3+Math.random()*0.7)-30,life:type==='muzzle'?0.08+Math.random()*0.08:0.22+Math.random()*0.3,col:type==='muzzle'?'#ffe066':col,r:type==='exp'?1.5+Math.random()*2.5:1});
  }
}

// ── KILL ──────────────────────────────────────────────
function killEnemy(e,byPlayer) {
  if(!e.alive||e.dying)return;
  e.dying=true;e.deathT=0;
  addParticle(e.x,e.y,'#cc1100','blood');
  for(let i=0;i<3;i++) addParticle(e.x+Math.random()*12-6,e.y+Math.random()*12-6,'#442200','blood');
  if(!byPlayer)return;
  G.kills++;G.score+=e.xp;
  const resGain=e.key?20:5;
  G.resource=Math.min(G.resourceMax,G.resource+resGain);
  if(e.key){
    G.keyKills++;
    let push=0,cry='',kfmsg='',kfcol='#f5c518';
    switch(e.type){
      case 'mg':    push=55;cry='아군 전진!';       kfmsg='💥 기관총 제압! 전선 전진!'; kfcol='#00ff88';showToast('기관총 처치! 아군 전진!','grn');break;
      case 'officer':push=32;cry='지휘관 처치!';    kfmsg='🎖 장교 제거! 적 사기 하락!';kfcol='#f5c518';showToast('장교 처치! 전선 약화!');break;
      case 'general':push=95;cry='총사령관 처치!\n전면 돌파!';kfmsg='🏅 총사령관 처치!';kfcol='#ff4400';showToast('총사령관 처치!','grn');break;
      case 'sniper_e':push=24;cry='적 저격수 제거!';kfmsg='🎯 적 저격수 처치!';kfcol='#00aaff';showToast('적 저격수 처치!');break;
    }
    if(push>0)G.frontlineX=Math.min(GW-80,G.frontlineX+push);
    if(cry){const el=document.getElementById('war-cry');el.innerHTML=cry.replace('\n','<br>');el.classList.add('show');G.warCryTimer=2.2;}
    showKF(kfmsg,kfcol);
  } else {
    showKF(`처치 +${e.xp}pt`,'#666');
  }
}

// ── SUMMON ALLY ────────────────────────────────────────
function summonUnit(unitId) {
  if(!G||G.phase!=='play'||G.done) return;
  const unit=ALLY_UNITS.find(u=>u.id===unitId);
  if(!unit) return;
  if(G.resource<unit.cost){showToast('자원 부족!','red');return;}
  if(G.summonCd>0){showToast(`쿨다운 ${G.summonCd.toFixed(1)}초`,'red');return;}
  G.resource-=unit.cost;
  G.summonCd=1.5;
  const y=115+Math.random()*(GH-220);
  const x=G.frontlineX-10-Math.random()*30;
  spawnAlly(unitId, x, y);
  showToast(`${unit.ico} ${unit.name} 소환!`,'blue');
  showKF(`🪖 ${unit.name} 소환 (-${unit.cost}자원)`,'#4488ff');
  const burst=document.createElement('div');
  burst.className='summon-burst';
  const r=canvas.getBoundingClientRect();
  burst.style.cssText=`left:${r.left+x-20}px;top:${r.top+y-20}px;width:40px;height:40px;`;
  document.body.appendChild(burst);
  setTimeout(()=>burst.remove(),550);
  ensureAudio();sfx_summon();
  updateHUD();buildAmmoStrip();
}

// ── FIRE ──────────────────────────────────────────────
function fire() {
  if(!G||G.phase!=='play'||G.done)return;
  if(G.coverActive){showToast('엄폐 중엔 발사 불가!','red');return;}
  if(G.reloading||G.shootCd>0)return;
  if(G.ammo<=0){startReload();return;}
  G.ammo--;G.shootCd=0.85;G.muzzleFlash=1;
  ensureAudio();sfx_shoot();
  updateHUD();buildAmmoStrip();
  G.aggro=Math.min(100,G.aggro+22+(G.scoped?8:15));

  const crit=G.breathHeld&&Math.random()<0.25;
  const hs=crit&&Math.random()<0.45;

  // ── 핵심: 스코프 켤 때 마우스 위치 = 완전한 조준점 ──
  // 스코프 시에는 마우스 위치가 그대로 조준점 (오프셋 없음)
  // 일반 모드에서도 마우스 위치가 조준점
  let aimX = G.mouse.x;
  let aimY = G.mouse.y;

  // 흔들림만 적용 (조준점 자체는 이동 없음)
  const sw=G.breathHeld?0.08:G.scoped?0.5:2.8;
  aimX+=(Math.random()-.5)*sw*2+G.swayX*(G.scoped?0.08:0.4);
  aimY+=(Math.random()-.5)*sw*2+G.swayY*(G.scoped?0.08:0.4);

  let hit=false;
  // 스코프 시 탐지 반경 확대 (확대됨)
  const hitBonus = G.scoped ? 8 : 0;
  const sorted=[...G.enemies].sort((a,b)=>Math.hypot(a.x-aimX,a.y-aimY)-Math.hypot(b.x-aimX,b.y-aimY));
  for(const e of sorted){
    if(!e.alive||e.dying)continue;
    const hitR=hs?e.sz+14:e.sz+5+hitBonus;
    if(Math.hypot(aimX-e.x,aimY-e.y)<hitR){
      const dmg=hs?999:crit?e.sz*14+50:80+Math.random()*25;
      e.hp-=dmg;
      spawnDmgNum(e.x,e.y,hs?'💀 HEADSHOT':Math.round(dmg),crit||hs);
      addParticle(e.x,e.y,'#ff2200','blood');
      addParticle(e.x,e.y,'#cc0000','exp');
      if(e.hp<=0)killEnemy(e,true);
      hit=true;
      if(hs)G.headshots++;
      G.shakeX=(Math.random()-.5)*6;G.shakeY=(Math.random()-.5)*6;
      break;
    }
  }
  if(!hit){
    for(const e of G.enemies){if(!e.alive)continue;if(Math.hypot(aimX-e.x,aimY-e.y)<50){G.aggro=Math.min(100,G.aggro+8);break;}}
    addParticle(aimX,aimY,'#aa8844','blood');
  }
  // 총구 불꽃 위치: 저격수 거점 (왼쪽 하단)
  addTracer(80,GH-38,aimX,aimY,'#ffffa0',true);
  if(G.ammo===0)setTimeout(startReload,250);
}

function startReload(){if(!G||G.reloading||G.ammo===G.maxAmmo)return;G.reloading=true;G.reloadTimer=G.reloadDur;showToast('재장전 중...');sfx_reload();}
function setCover(on){
  if(!G||G.phase!=='play'||G.done)return;
  G.coverActive=on;
  const btn=document.getElementById('cover-btn');
  if(on)btn.classList.add('active');else btn.classList.remove('active');
  const vig=document.getElementById('cover-vignette');
  if(on)vig.classList.add('on');else vig.classList.remove('on');
  if(on&&G.scoped)toggleScope();
}
function toggleScope(){
  if(!G||G.phase!=='play'||G.done)return;
  if(G.coverActive&&!G.scoped){showToast('엄폐 중 스코프 불가!','red');return;}
  G.scoped=!G.scoped;
  // 스코프 HUD 토글
  const siHud=document.getElementById('scope-info-hud');
  const bwrap=document.getElementById('breath-wrap');
  siHud.style.display=G.scoped?'flex':'none';
  bwrap.style.display=G.scoped?'block':'none';
  sfx_scope(G.scoped);
}

// ── END ────────────────────────────────────────────────
function checkEnd(){
  if(G.done)return;
  if(G.frontlineX>=GW-80){G.done=true;showResult(true);return;}
  if(G.playerHP<=0||G.frontlineX<=130||G.time<=0||G.allyHP<=0){
    G.done=true;
    G.failReason=G.playerHP<=0?'저격수 전사':G.frontlineX<=130?'전선 붕괴':G.time<=0?'시간 초과':'아군 전멸';
    showResult(false);
  }
}
function grade(){const s=G.score;return s>=7000?'S':s>=3500?'A':s>=1400?'B':'C';}
function gradeColor(){return{S:'#f5c518',A:'#00ff88',B:'#00aaff',C:'#888'}[grade()];}
function showResult(win){
  G.phase='result';
  if(G.scoped)toggleScope();
  const el=document.getElementById('result-ov');
  const t=document.getElementById('res-title');
  t.textContent=win?'🏆 작전 성공!':'💀 '+G.failReason;
  t.style.color=win?'#f5c518':'#ff2244';
  const g=grade();
  const gEl=document.getElementById('res-grade');
  gEl.textContent=g;gEl.style.color=gradeColor();
  const elapsed=G.mis.timeLimit-G.time;
  const fl=Math.max(0,Math.round((G.frontlineX-G.mis.startLine)/(GW-80-G.mis.startLine)*100));
  document.getElementById('res-stats').innerHTML=`
    <div class="rs">처치<b>${G.kills}</b></div>
    <div class="rs">점수<b>${Math.round(G.score).toLocaleString()}</b></div>
    <div class="rs">헤드샷<b>${G.headshots}</b></div>
    <div class="rs">경과<b>${Math.floor(elapsed/60)}m${Math.floor(elapsed%60)}s</b></div>
    <div class="rs">저격수HP<b>${Math.round(G.playerHP)}%</b></div>
    <div class="rs">전선전진<b>${fl}%</b></div>`;
  el.style.display='flex';
  if(win){
    sfx_win();
    if(!window._sc)window._sc=[];
    if(!window._sc.includes(G.midx))window._sc.push(G.midx);
    try{window.parent.postMessage({type:'sniper_result',score:Math.round(G.score),grade:g,midx:G.midx},'*');}catch(e){}
  } else sfx_fail();
}
function retryMission(){document.getElementById('result-ov').style.display='none';initGame(G.midx);}
function gotoTitle(){document.getElementById('result-ov').style.display='none';G=null;buildTitle();document.getElementById('mission-ov').style.display='flex';}

// ══════════════════════════════════════════════════════
//  DRAW — 전체 렌더링
// ══════════════════════════════════════════════════════
function drawScene(c, W, H, zoom, panX, panY) {
  // zoom, panX, panY: 스코프 확대 시 사용. 기본값은 1, 0, 0
  const z = zoom||1;
  const age = G ? AGES[G.ageId] : AGES[0];

  // 배경
  const sky=c.createLinearGradient(0,0,0,H*0.36);
  sky.addColorStop(0, age.bgSky[0]); sky.addColorStop(1, age.bgSky[1]);
  c.fillStyle=sky; c.fillRect(0,0,W,H);
  const gnd=c.createLinearGradient(0,H*0.34,0,H);
  gnd.addColorStop(0, age.bgGnd[0]); gnd.addColorStop(1, age.bgGnd[1]);
  c.fillStyle=gnd; c.fillRect(0,H*0.34,W,H);

  drawTreeLine(c,W,H,age);
  drawTerrain(c,W,H,age);
  if(G) {
    drawFrontlineIndicator(c,W,H);
    for(const p of G.particles){c.save();c.globalAlpha=Math.max(0,Math.min(1,p.life*3));c.fillStyle=p.col;c.beginPath();c.arc(p.x,p.y,p.r,0,Math.PI*2);c.fill();c.restore();}
    for(const t of G.tracers){const a=t.life/t.maxLife;c.save();c.globalAlpha=a*0.85;c.strokeStyle=t.col;c.lineWidth=t.isPlayer?2.2:1.2;c.shadowColor=t.col;c.shadowBlur=t.isPlayer?10:4;c.beginPath();c.moveTo(t.x1,t.y1);c.lineTo(t.x2,t.y2);c.stroke();c.shadowBlur=0;c.restore();}
    for(const a of G.allies) drawAlly(c,a,age);
    for(const e of G.enemies) drawEnemy(c,e,age);
    drawSniperHide(c,W,H,age);
  }
}

function drawTreeLine(c,W,H,age){
  const col = age.id<=1?'#1a1008':age.id<=3?'#0a1508':age.id<=5?'#0a1408':'#050810';
  c.fillStyle=col;
  for(let tx=0;tx<W;tx+=55){
    const th=28+Math.sin(tx*0.065+1)*22+Math.sin(tx*0.03)*14;
    c.beginPath();c.moveTo(tx,H*0.38);c.lineTo(tx+8,H*0.38-th);
    c.lineTo(tx+26,H*0.38-th-8);c.lineTo(tx+44,H*0.38-th);c.lineTo(tx+55,H*0.38);c.fill();
  }
}

function drawFrontlineIndicator(c,W,H){
  const fx=G.frontlineX;
  c.save();
  c.strokeStyle='rgba(255,255,255,0.08)';c.lineWidth=2;c.setLineDash([5,9]);
  c.beginPath();c.moveTo(fx,88);c.lineTo(fx,H-46);c.stroke();
  c.setLineDash([]);
  c.fillStyle='rgba(255,255,255,0.18)';c.font='bold 8px Orbitron';c.textAlign='center';
  c.fillText('FRONT',fx,84);
  c.restore();
}

function drawTerrain(c,W,H,age){
  c.save();
  // 아군 엄폐물 (시대별)
  if(age.id<=1){
    // 석기/고대: 바위 방어선
    [[140,290],[140,190],[140,400],[195,250],[195,360]].forEach(([x,y])=>drawRock(c,x,y,'#302010'));
  } else if(age.id<=3){
    // 중세/르네상스: 목책+모래주머니
    [[140,290],[140,190],[140,400],[195,250],[195,360],[250,310]].forEach(([x,y])=>drawSandbag(c,x,y));
  } else {
    // 근현대+SF: 모래주머니+참호
    [[140,290],[140,190],[140,400],[195,250],[195,360],[250,310]].forEach(([x,y])=>drawSandbag(c,x,y));
    // 참호선
    c.fillStyle='rgba(0,0,0,.35)';c.fillRect(120,H*0.38+20,8,H*0.55);
  }
  // 적 진영 엄폐물
  const rkCol = age.id>=5?'#1a2828':'#282828';
  [[W-80,270],[W-80,390],[W-120,200],[W-120,440],[W-50,330]].forEach(([x,y])=>drawRock(c,x,y,rkCol));
  // 분화구
  [[320,300],[490,265],[640,380],[410,175],[550,435]].forEach(([cx,cy])=>{
    c.fillStyle='#0a1008';c.beginPath();c.ellipse(cx,cy,24,14,0.1,0,Math.PI*2);c.fill();
    c.strokeStyle='#182015';c.lineWidth=1.5;c.beginPath();c.ellipse(cx,cy,24,14,0.1,0,Math.PI*2);c.stroke();
  });
  // 나무 그루터기
  [[255,375],[435,195],[695,295],[340,155]].forEach(([tx,ty])=>{
    c.fillStyle='#1a1208';c.fillRect(tx-4,ty-24,8,24);c.fillRect(tx-7,ty-2,14,6);
  });
  // SF 시대: 에너지 장벽
  if(age.id>=6){
    c.save();
    c.globalAlpha=0.15;
    c.strokeStyle='#0088ff';c.lineWidth=2;c.setLineDash([8,4]);
    c.beginPath();c.moveTo(180,H*0.12);c.lineTo(180,H*0.9);c.stroke();
    c.setLineDash([]);c.restore();
  }
  c.restore();
}

function drawSandbag(c,x,y){
  c.save();c.fillStyle='#3a2a10';
  c.beginPath();c.ellipse(x,y,20,9,0,0,Math.PI*2);c.fill();
  c.fillStyle='#4a3818';
  c.beginPath();c.ellipse(x-6,y-2,12,6,0,0,Math.PI*2);c.fill();
  c.beginPath();c.ellipse(x+6,y-2,12,6,0,0,Math.PI*2);c.fill();
  c.restore();
}
function drawRock(c,x,y,col){
  c.save();c.fillStyle=col||'#282828';
  c.beginPath();c.ellipse(x,y,17,11,0.25,0,Math.PI*2);c.fill();
  c.fillStyle='rgba(255,255,255,0.04)';c.beginPath();c.ellipse(x-5,y-3,10,7,0.1,0,Math.PI*2);c.fill();
  c.restore();
}

function drawSniperHide(c,W,H,age){
  c.save();
  c.translate(80,H-38);
  // 시대별 무기 모양
  if(age.id<=1){
    // 석기/고대: 활
    c.strokeStyle='#8a6020';c.lineWidth=2.5;
    c.beginPath();c.arc(0,0,22,Math.PI*0.8,Math.PI*2.2);c.stroke();
    c.strokeStyle='#c8a060';c.lineWidth=1;
    c.beginPath();c.moveTo(-16,-8);c.lineTo(16,8);c.stroke();
  } else if(age.id<=3){
    // 중세/르네상스: 석궁/머스킷
    c.fillStyle='#1a1a1a';c.fillRect(8,-2,38,5);c.fillRect(44,-3,12,7);
    c.fillStyle='#8a6020';c.fillRect(5,-8,12,14);
    c.fillStyle='#604010';c.fillRect(-12,2,20,12);
  } else if(age.id<=5){
    // 근현대: 저격 소총
    c.fillStyle='#1a1a1a';c.fillRect(8,-2,38,5);c.fillRect(44,-3,12,7);
    c.fillStyle='#111a11';c.fillRect(16,-7,18,5);
    c.strokeStyle='#1a1a1a';c.lineWidth=2;
    c.beginPath();c.moveTo(38,3);c.lineTo(34,16);c.stroke();
    c.beginPath();c.moveTo(38,3);c.lineTo(42,16);c.stroke();
  } else {
    // SF: 에너지 라이플
    c.fillStyle='#0a1a2a';c.fillRect(4,-4,48,8);c.fillRect(48,-5,14,10);
    c.fillStyle='#0044aa';c.fillRect(16,-2,18,4);
    c.strokeStyle='#0088ff';c.lineWidth=1.5;
    c.shadowColor='#0088ff';c.shadowBlur=8;
    c.beginPath();c.moveTo(58,0);c.lineTo(72,0);c.stroke();
    c.shadowBlur=0;
  }
  // 플레이어 몸 (시대별 색상)
  const bodyCol = age.id<=1?'#3a2810':age.id<=3?'#2a2010':age.id<=5?'#1a3010':'#0a1a2a';
  const helmetCol = age.id<=1?'#402a10':age.id<=3?'#281e0e':age.id<=5?'#182818':'#0a1428';
  c.fillStyle=bodyCol;c.beginPath();c.ellipse(-12,2,22,9,0.15,0,Math.PI*2);c.fill();
  c.fillStyle='#223318';c.beginPath();c.ellipse(-20,1,12,7,-0.1,0,Math.PI*2);c.fill();
  c.fillStyle=helmetCol;c.beginPath();c.arc(-8,-5,7,Math.PI,0);c.closePath();c.fill();
  if(age.id>=6){
    // SF 바이저
    c.fillStyle='rgba(0,136,255,0.6)';c.fillRect(-14,-9,12,5);
    c.shadowColor='#0088ff';c.shadowBlur=4;c.fillRect(-14,-9,12,5);c.shadowBlur=0;
  }
  c.restore();
}

// ── DRAW ALLY (시대별 외관) ────────────────────────────
function drawAlly(c,a,age){
  if(!a.alive&&!a.dying)return;
  const alpha=a.dying?Math.max(0,1-a.deathT/0.7):1;
  const spawnScale=a.spawnAnim>0?Math.max(0.2,1-a.spawnAnim*1.5):1;
  const bob=Math.sin(a.phase)*1.4;
  c.save();
  c.globalAlpha=alpha;
  c.translate(Math.round(a.x),Math.round(a.y+bob));
  c.scale(spawnScale,spawnScale);
  if(a.spawnAnim>0){c.shadowColor=a.color;c.shadowBlur=20;}
  c.save();c.globalAlpha=0.22*alpha;c.fillStyle='#000';c.beginPath();c.ellipse(0,14,10,4,0,0,Math.PI*2);c.fill();c.restore();
  // 다리
  c.fillStyle='#1a2a1a';c.fillRect(-4,4,4,9);c.fillRect(1,4,4,9);
  c.fillStyle='#111';c.fillRect(-4,12,4,4);c.fillRect(1,12,4,4);
  // 몸
  c.fillStyle='#253525';c.fillRect(-5,-5,10,10);
  c.fillStyle='#304030';c.fillRect(-4,-4,8,8);
  c.fillStyle='#253525';c.fillRect(-8,-4,4,7);c.fillRect(5,-4,4,7);
  // 얼굴
  c.fillStyle='#c09870';c.beginPath();c.arc(0,-10,4.5,0,Math.PI*2);c.fill();
  // 헬멧 (시대별)
  const hCol = age.id<=1?'#4a3818':age.id<=3?'#2a3a5a':age.id<=5?'#1e3a6e':'#0a1e40';
  c.fillStyle=hCol;c.beginPath();c.arc(0,-14,5.5,Math.PI,0);c.fill();c.fillRect(-6.5,-14,13,3);
  c.fillStyle=age.id>=6?'rgba(0,136,255,0.4)':'#162e58';c.fillRect(-7,-13,14,2);
  if(age.id>=6){
    c.fillStyle='rgba(0,136,255,0.5)';c.fillRect(-5,-12,10,3);
  }
  // 무기
  if(age.id<=1){
    c.strokeStyle='#8a6020';c.lineWidth=1.5;
    c.beginPath();c.moveTo(6,0);c.lineTo(22,-6);c.stroke();
  } else if(age.id<=3){
    c.fillStyle='#604010';c.fillRect(6,-2,14,4);c.fillRect(18,-5,4,9);
  } else if(age.id<=5){
    c.fillStyle='#1a1a1a';c.fillRect(6,-2,18,4);c.fillRect(12,2,4,6);c.fillRect(8,2,3,5);
  } else {
    c.fillStyle='#0a1a2a';c.fillRect(6,-3,22,5);
    c.fillStyle='#0044aa';c.fillRect(16,-1,8,3);
    c.strokeStyle='#00aaff';c.lineWidth=1;c.shadowColor='#00aaff';c.shadowBlur=4;
    c.beginPath();c.moveTo(28,0);c.lineTo(34,0);c.stroke();c.shadowBlur=0;
  }
  // 유닛 타입 아이콘
  if(a.unitType!=='warrior'){
    c.globalAlpha=0.9;c.fillStyle=a.color||'#00ff88';
    c.font='bold 7px Orbitron';c.textAlign='center';
    const labels={archer:'🏹',knight:'🛡',medic:'🏥',sniper_a:'🎯'};
    c.fillText(labels[a.unitType]||'',0,-22);
  }
  c.restore();
}

// ── DRAW ENEMY (시대별 외관) ───────────────────────────
function drawEnemy(c,e,age){
  if(!e.alive&&!e.dying)return;
  const alpha=e.dying?Math.max(0,1-e.deathT/0.7):1;
  const bob=Math.sin(e.phase)*1.2;
  c.save();
  c.globalAlpha=alpha;
  c.translate(Math.round(e.x),Math.round(e.y+bob));
  const sz=e.type==='general'?1.28:e.type==='mg'?1.12:1;
  c.scale(sz,sz);
  c.save();c.globalAlpha=0.22*alpha;c.fillStyle='#000';c.beginPath();c.ellipse(0,14,9,4,0,0,Math.PI*2);c.fill();c.restore();
  const helmetC=e.type==='general'?'#553300':e.type==='officer'?'#4a3000':e.type==='sniper_e'?'#162216':'#503828';
  const bodyC=e.type==='general'?'#3a1200':e.type==='officer'?'#2a1200':e.type==='sniper_e'?'#182018':'#2e1a0e';
  const pantC=e.type==='general'?'#280e00':e.type==='officer'?'#1e0e00':'#241408';
  // SF 시대는 약간 다른 색상
  const actualBodyC = age.id>=6 ? (e.type==='general'?'#001a3a':e.type==='officer'?'#001030':bodyC) : bodyC;
  const actualHelmetC = age.id>=6 ? (e.type==='general'?'#002255':e.type==='officer'?'#001844':helmetC) : helmetC;
  c.fillStyle=pantC;c.fillRect(-4,4,4,9);c.fillRect(1,4,4,9);
  c.fillStyle='#111';c.fillRect(-4,12,4,4);c.fillRect(1,12,4,4);
  c.fillStyle=actualBodyC;c.fillRect(-5,-5,10,10);
  c.fillStyle='#3a2a18';c.fillRect(-4,-4,8,8);
  c.fillStyle='#2a1e0e';c.fillRect(-3,-2,3,3);c.fillRect(1,-2,3,3);
  c.fillStyle=actualBodyC;c.fillRect(-8,-4,4,7);c.fillRect(5,-4,4,7);
  c.fillStyle='#b88858';c.beginPath();c.arc(0,-10,4.5,0,Math.PI*2);c.fill();
  c.fillStyle=actualHelmetC;
  if(e.type==='officer'||e.type==='general'){
    c.fillRect(-6,-17,12,4);c.beginPath();c.arc(0,-15,5,Math.PI,0);c.fill();
    c.fillStyle='#f5c518';c.beginPath();c.arc(0,-16,2,0,Math.PI*2);c.fill();
    if(e.type==='general'){c.fillStyle='#f5c518';c.fillRect(-10,-4,4,3);c.fillRect(7,-4,4,3);}
  } else {
    c.beginPath();c.arc(0,-14,5.5,Math.PI,0);c.fill();c.fillRect(-6.5,-14,13,3);
    c.fillStyle=e.type==='sniper_e'?'#0e1a0e':'#3a2818';c.fillRect(-7,-13,14,2);
  }
  // SF 바이저
  if(age.id>=6){
    c.fillStyle='rgba(255,50,0,0.5)';c.fillRect(-5,-12,10,3);
    c.shadowColor='#ff3300';c.shadowBlur=4;c.fillRect(-5,-12,10,3);c.shadowBlur=0;
  }
  if(e.type==='sniper_e'){c.fillStyle='rgba(0,35,0,0.55)';c.fillRect(-4,-13,8,7);}
  c.fillStyle='#1a1a1a';
  if(e.type==='mg'){
    if(age.id>=6){
      c.fillStyle='#0a1a2a';c.fillRect(-24,-2,22,4);c.fillRect(-22,2,2,10);c.fillRect(-18,2,2,10);
      c.fillStyle='#0044aa';c.beginPath();c.arc(-14,2,4,0,Math.PI*2);c.fill();
      c.strokeStyle='#ff3300';c.lineWidth=1;c.shadowColor='#ff3300';c.shadowBlur=6;
      c.beginPath();c.moveTo(-26,0);c.lineTo(-34,0);c.stroke();c.shadowBlur=0;
    } else {
      c.fillRect(-24,-2,22,4);c.fillRect(-22,2,2,10);c.fillRect(-18,2,2,10);
      c.fillStyle='#2a2a2a';c.beginPath();c.arc(-14,2,4,0,Math.PI*2);c.fill();
    }
  } else if(e.type==='sniper_e'){
    c.fillRect(-28,0,26,3);c.fillStyle='#111a11';c.fillRect(-22,-4,10,4);
    c.fillStyle='#2a2a2a';c.fillRect(-30,-1,4,5);
  } else {
    c.fillRect(-20,-1,18,4);c.fillRect(-16,3,4,6);c.fillRect(-14,3,3,5);
  }
  c.restore();
  // Key target markers
  if(e.key&&e.alive){
    const lbl=e.type==='general'?'★사령관':e.type==='officer'?'★장교':e.type==='mg'?'★기관총':'★저격수';
    c.save();
    const pulse=0.6+Math.sin(gTimer*4)*0.4;
    c.globalAlpha=pulse*0.55;
    c.strokeStyle=e.type==='general'?'#ff4400':e.type==='mg'?'#ff0000':e.type==='officer'?'#f5c518':'#00aaff';
    c.lineWidth=2;c.setLineDash([4,4]);
    c.beginPath();c.arc(e.x,e.y,e.sz*sz+10,0,Math.PI*2);c.stroke();
    c.setLineDash([]);c.globalAlpha=1;
    c.fillStyle='rgba(0,0,0,.7)';c.fillRect(e.x-28,e.y-e.sz*sz-28,56,13);
    c.fillStyle=c.strokeStyle||'#f5c518';c.font='8px Black Han Sans';c.textAlign='center';
    c.fillText(lbl,e.x,e.y-e.sz*sz-18);
    const bw=e.sz*sz*3.8,pct=Math.max(0,e.hp/e.maxHp);
    c.fillStyle='rgba(0,0,0,.7)';c.fillRect(e.x-bw/2,e.y-e.sz*sz-13,bw,6);
    c.fillStyle=pct>0.5?'#22cc44':pct>0.25?'#ccaa00':'#cc1100';
    c.fillRect(e.x-bw/2,e.y-e.sz*sz-13,bw*pct,6);
    c.restore();
  }
}

// ══════════════════════════════════════════════════════
//  스코프 렌더링 — 마우스가 항상 조준점 정중앙
//  방식: 캔버스 전체에 직접 그림 (DOM 분리 X)
// ══════════════════════════════════════════════════════
function drawScopeOverlay(mainCtx, W, H) {
  if(!G||!G.scoped) return;

  const mx = G.mouse.x;
  const my = G.mouse.y;
  const R  = scopeR;
  const ZOOM = 3.8;

  // ── 1. 화면 전체를 반투명 검정으로 덮기 ──
  mainCtx.save();
  mainCtx.fillStyle = 'rgba(0,0,0,0.93)';
  mainCtx.fillRect(0,0,W,H);

  // ── 2. 스코프 원 안쪽만 클리핑 (마우스 위치 중심) ──
  mainCtx.save();
  mainCtx.beginPath();
  mainCtx.arc(mx, my, R, 0, Math.PI*2);
  mainCtx.clip();

  // ── 3. 스코프 원 안에 확대된 씬 그리기 ──
  // 확대 변환: 마우스 위치(mx, my)를 중심으로 ZOOM배 확대
  mainCtx.save();
  // 약간의 흔들림
  const swayOffX = G.swayX * 0.15;
  const swayOffY = G.swayY * 0.15;
  mainCtx.translate(mx + swayOffX, my + swayOffY);
  mainCtx.scale(ZOOM, ZOOM);
  mainCtx.translate(-mx, -my);
  // 확대된 씬 그리기
  drawScene(mainCtx, W, H);
  mainCtx.restore();

  // ── 4. 스코프 내부 비네트 (원 안쪽 가장자리 어두움) ──
  const vgr = mainCtx.createRadialGradient(mx, my, R*0.55, mx, my, R);
  vgr.addColorStop(0, 'transparent');
  vgr.addColorStop(1, 'rgba(0,0,0,0.75)');
  mainCtx.fillStyle = vgr;
  mainCtx.beginPath();
  mainCtx.arc(mx, my, R, 0, Math.PI*2);
  mainCtx.fill();

  // ── 5. 십자선(크로스헤어) — 마우스 위치 정중앙 ──
  const chCol = 'rgba(0,255,100,0.9)';
  const chFade = 'rgba(0,255,100,0.3)';
  mainCtx.strokeStyle = chCol;
  mainCtx.lineWidth = 1.0;

  // 수평선 (좌)
  mainCtx.beginPath();
  mainCtx.moveTo(mx - R + 4, my);
  mainCtx.lineTo(mx - 28, my);
  mainCtx.stroke();
  // 수평선 (우)
  mainCtx.beginPath();
  mainCtx.moveTo(mx + 28, my);
  mainCtx.lineTo(mx + R - 4, my);
  mainCtx.stroke();
  // 수직선 (상)
  mainCtx.beginPath();
  mainCtx.moveTo(mx, my - R + 4);
  mainCtx.lineTo(mx, my - 28);
  mainCtx.stroke();
  // 수직선 (하)
  mainCtx.beginPath();
  mainCtx.moveTo(mx, my + 28);
  mainCtx.lineTo(mx, my + R - 4);
  mainCtx.stroke();

  // 밀-닷 (mil-dot reticle)
  mainCtx.strokeStyle = chFade;
  mainCtx.lineWidth = 0.7;
  // 수평 보조선
  mainCtx.beginPath(); mainCtx.moveTo(mx-26, my+20); mainCtx.lineTo(mx+26, my+20); mainCtx.stroke();
  mainCtx.beginPath(); mainCtx.moveTo(mx-26, my-20); mainCtx.lineTo(mx+26, my-20); mainCtx.stroke();
  // 밀-닷 점들
  mainCtx.fillStyle = chCol;
  [-40,-20,20,40].forEach(d=>{
    mainCtx.beginPath(); mainCtx.arc(mx+d, my, 1.5, 0, Math.PI*2); mainCtx.fill();
    mainCtx.beginPath(); mainCtx.arc(mx, my+d, 1.5, 0, Math.PI*2); mainCtx.fill();
  });

  // 중앙 작은 원
  mainCtx.strokeStyle = chCol;
  mainCtx.lineWidth = 0.8;
  mainCtx.beginPath();
  mainCtx.arc(mx, my, 3.5, 0, Math.PI*2);
  mainCtx.stroke();

  mainCtx.restore(); // clip 해제

  // ── 6. 스코프 테두리 원 ──
  mainCtx.save();
  mainCtx.strokeStyle = 'rgba(0,255,100,0.35)';
  mainCtx.lineWidth = 3;
  mainCtx.shadowColor = 'rgba(0,255,100,0.2)';
  mainCtx.shadowBlur = 15;
  mainCtx.beginPath();
  mainCtx.arc(mx, my, R, 0, Math.PI*2);
  mainCtx.stroke();
  // 바깥 더블링
  mainCtx.strokeStyle = 'rgba(0,255,100,0.1)';
  mainCtx.lineWidth = 1;
  mainCtx.beginPath();
  mainCtx.arc(mx, my, R+4, 0, Math.PI*2);
  mainCtx.stroke();
  mainCtx.restore();

  // ── 7. 스코프 정보 텍스트 ──
  const dist = Math.round(Math.hypot(mx-80, my-(GH-38)));
  const info = `${dist}m  ·  ${G.breathHeld?'숨참기 ✓':'흔들림 中'}  ·  ${G.ammo}/${G.maxAmmo}탄`;
  mainCtx.save();
  mainCtx.font = '10px Rajdhani,sans-serif';
  mainCtx.textAlign = 'center';
  mainCtx.fillStyle = 'rgba(0,255,100,0.75)';
  mainCtx.letterSpacing = '2px';
  mainCtx.fillText(info, mx, my + R * 0.78);
  mainCtx.restore();

  // ── 8. 숨참기 바 ──
  mainCtx.save();
  const bw = 140, bh = 4;
  const bx = mx - bw/2, by = my + R * 0.86;
  mainCtx.fillStyle='rgba(255,255,255,.06)';mainCtx.fillRect(bx,by,bw,bh);
  const bf = G.breathTimer/3;
  mainCtx.fillStyle = bf > 0.5 ? '#00ff88' : bf > 0.2 ? '#ffcc00' : '#ff4444';
  mainCtx.fillRect(bx,by,bw*bf,bh);
  mainCtx.restore();

  mainCtx.restore(); // 맨 처음 save
}

// ── 일반 모드 크로스헤어 (스코프 OFF일 때) ─────────────
function drawCrosshair(c, mx, my) {
  if(!G||G.scoped||G.coverActive) return;
  const col = 'rgba(255,255,255,0.85)';
  const size = 10;
  const gap  = 5;
  c.save();
  c.strokeStyle = col;
  c.lineWidth = 1.5;
  c.shadowColor = 'rgba(0,0,0,0.9)';
  c.shadowBlur = 3;
  // 수평
  c.beginPath();c.moveTo(mx-size-gap,my);c.lineTo(mx-gap,my);c.stroke();
  c.beginPath();c.moveTo(mx+gap,my);c.lineTo(mx+size+gap,my);c.stroke();
  // 수직
  c.beginPath();c.moveTo(mx,my-size-gap);c.lineTo(mx,my-gap);c.stroke();
  c.beginPath();c.moveTo(mx,my+gap);c.lineTo(mx,my+size+gap);c.stroke();
  // 중앙 점
  c.fillStyle = col;
  c.beginPath();c.arc(mx,my,1.5,0,Math.PI*2);c.fill();
  c.restore();
}

// ── HUD ────────────────────────────────────────────────
function buildAmmoStrip(){
  if(!G)return;
  const strip=document.getElementById('ammo-strip');
  let html='';
  for(let i=0;i<G.maxAmmo;i++){
    const loaded=i<G.ammo;
    const isReloading=G.reloading&&!loaded;
    const pct=isReloading?Math.round((1-G.reloadTimer/G.reloadDur)*100):0;
    html+=`<div class="ammo-pip${loaded?'':' empty'}" style="${isReloading?`background:linear-gradient(to top,#f5c518 ${pct}%,#1a1a1a ${pct}%);`:''}"></div>`;
  }
  strip.innerHTML=html;
}

function buildSummonPanel(){
  const btn_container=document.getElementById('summon-btns');
  btn_container.innerHTML=ALLY_UNITS.map(u=>`
    <div class="summon-btn" id="sbtn-${u.id}" onclick="summonUnit('${u.id}')" title="${u.effect}">
      <span class="sb-ico">${u.ico}</span>
      <span class="sb-name">[${u.key}]${u.name}</span>
      <span class="sb-cost">💎${u.cost}</span>
      <span class="sb-effect">${u.effect}</span>
    </div>
  `).join('');
}

function updateHUD(){
  if(!G)return;
  document.getElementById('score-v').textContent=Math.round(G.score).toLocaleString();
  document.getElementById('kill-v').textContent=G.kills;
  const t=Math.max(0,G.time);
  const ts=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  const tv=document.getElementById('timer-v');tv.textContent=ts;
  tv.style.color=t<30?'#ff4444':t<60?'#ffcc00':'#f5c518';
  const ahp=Math.round(G.allyHP);
  const av=document.getElementById('ally-hp-v');av.textContent=ahp+'%';
  av.style.color=ahp>60?'#00ff88':ahp>30?'#ffcc00':'#ff4444';
  const rv=Math.floor(G.resource);
  document.getElementById('res-v').textContent=rv;
  document.getElementById('resource-val').textContent=rv;
  ALLY_UNITS.forEach(u=>{
    const btn=document.getElementById('sbtn-'+u.id);
    if(btn){const canAfford=G.resource>=u.cost&&G.summonCd<=0;btn.classList.toggle('disabled',!canAfford);}
  });
  const cdEl=document.getElementById('summon-cd');
  if(cdEl) cdEl.textContent=G.summonCd>0?`쿨다운 ${G.summonCd.toFixed(1)}s`:'소환 준비됨';
  const total=(GW-80)-130,pos=G.frontlineX-130;
  const pct=(pos/total*100);
  document.getElementById('fl-ally').style.width=pct+'%';
  document.getElementById('fl-enemy').style.width=(100-pct)+'%';
  document.getElementById('fl-mid').style.left=pct+'%';
  document.getElementById('fl-pct-txt').textContent=Math.round(pct)+'%';
  const ap=Math.round(G.aggro);
  const af=document.getElementById('aggro-fill');
  af.style.width=ap+'%';
  af.style.background=ap>70?'linear-gradient(90deg,#ff3300,#ff0000)':ap>40?'linear-gradient(90deg,#ffcc00,#ff6600)':'linear-gradient(90deg,#aacc00,#ffaa00)';
  document.getElementById('aggro-pct').textContent=ap+'%';
  const at=ap<28?'은폐 유지 중 — 안전':ap<55?'주의 — 노출 위험':ap<82?'⚠ 위험! 즉시 엄폐!':'🔴 발각 직전!';
  const atEl=document.getElementById('aggro-txt');atEl.textContent=at;atEl.style.color=ap>55?'#ff5500':'#445';
  const php=Math.round(G.playerHP);
  document.getElementById('php-pct').textContent=php+'%';
  document.getElementById('php-fill').style.width=php+'%';
  document.getElementById('php-fill').style.background=php>60?'linear-gradient(90deg,#00aa44,#00ff88)':php>30?'linear-gradient(90deg,#cc8800,#ffcc00)':'linear-gradient(90deg,#aa0000,#ff4444)';
  // 스코프 HUD
  if(G.scoped){
    const dist=Math.round(Math.hypot(G.mouse.x-80,G.mouse.y-(GH-38)));
    document.getElementById('si-dist').textContent=`${dist}m`;
    document.getElementById('si-ammo').textContent=`${G.ammo}/${G.maxAmmo}탄`;
    document.getElementById('breath-fill').style.width=(G.breathTimer/3*100)+'%';
  }
}

// ── UI HELPERS ─────────────────────────────────────────
function showToast(msg,cls=''){
  const w=document.getElementById('toast-wrap');
  const el=document.createElement('div');
  el.className='toast-item'+(cls?' '+cls:'');
  el.textContent=msg;w.appendChild(el);
  setTimeout(()=>el.remove(),2100);
}
function showKF(msg,col){
  const kf=document.getElementById('killfeed');
  const it=document.createElement('div');it.className='kf';
  it.style.borderLeftColor=col||'#ff4444';
  it.style.color=col||'#ccc';it.textContent=msg;
  kf.appendChild(it);
  setTimeout(()=>{it.style.transition='opacity .4s';it.style.opacity='0';setTimeout(()=>it.remove(),450);},2400);
  while(kf.children.length>6)kf.removeChild(kf.firstChild);
}
function spawnDmgNum(x,y,v,crit){
  const el=document.createElement('div');el.className='dnum';
  const r=canvas.getBoundingClientRect();
  const isText=typeof v==='string';
  el.style.cssText=`left:${r.left+x+(isText?-55:-18)}px;top:${r.top+y-12}px;font-size:${isText?11:crit?20:13}px;color:${isText?'#ff4444':crit?'#ffe033':'#ffffff'};`;
  el.textContent=v;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),900);
}

// ── AUDIO ──────────────────────────────────────────────
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function beep(f,t,d,v=.18,delay=0,shape='sine'){if(!ACtx)return;try{
  const o=ACtx.createOscillator(),g=ACtx.createGain();
  o.connect(g);g.connect(ACtx.destination);o.type=shape;o.frequency.value=f;
  const ts=ACtx.currentTime+delay;
  g.gain.setValueAtTime(0,ts);g.gain.linearRampToValueAtTime(v,ts+.004);
  g.gain.exponentialRampToValueAtTime(.001,ts+d);o.start(ts);o.stop(ts+d+.05);
}catch(e){}}
function sfx_shoot(){ensureAudio();beep(120,'sawtooth',.06,.45,0,'sawtooth');beep(68,'sine',.12,.3,.04);beep(2200,'square',.02,.07,0,'square');beep(90,'sine',.22,.12,.08);}
function sfx_reload(){ensureAudio();beep(800,'square',.03,.1,0,'square');beep(400,'sine',.08,.1,.07);beep(1200,'square',.02,.08,.35,'square');beep(600,'sine',.06,.1,.38);}
function sfx_scope(on){ensureAudio();if(on){beep(1800,'sine',.04,.05);beep(2200,'sine',.06,.04,.05);}else{beep(1200,'sine',.04,.04);beep(800,'sine',.05,.03,.04);}}
function sfx_detected(){ensureAudio();[900,650,400,200].forEach((f,i)=>beep(f,'sawtooth',.18,.38,i*.07,'sawtooth'));}
function sfx_win(){ensureAudio();[523,659,784,1047,1319].forEach((f,i)=>beep(f,'sine',.3,.28,i*.11));}
function sfx_fail(){ensureAudio();[280,200,140].forEach((f,i)=>beep(f,'sawtooth',.32,.28,i*.15,'sawtooth'));}
function sfx_summon(){ensureAudio();beep(440,'sine',.06,.12);beep(660,'sine',.08,.1,.06);beep(880,'sine',.06,.08,.12);}

// ── TITLE ──────────────────────────────────────────────
function buildTitle(){
  const cleared=window._sc||[];
  const grid=document.getElementById('mission-grid');
  grid.innerHTML='';
  MISSIONS.forEach((m,i)=>{
    const locked=i>0&&!cleared.includes(i-1);
    const age=AGES[m.ageId];
    const div=document.createElement('div');
    div.className='mis-card'+(locked?' locked':'');
    div.style.borderColor=locked?'rgba(255,255,255,.06)':`${age.color}44`;
    div.innerHTML=`<div class="mc-num" style="color:${age.color}">${i+1}</div><div class="mc-name">${m.name}</div><div class="mc-diff">${m.diff}</div><div style="font-size:7px;color:${age.color}88;margin-top:2px;">${age.name}</div><div class="mc-desc">${m.desc}</div>${cleared.includes(i)?'<div class="mc-clr">✅ 완료</div>':''}`;
    if(!locked){div.onclick=()=>{selMis=i;document.querySelectorAll('.mis-card').forEach(x=>x.classList.remove('sel'));div.classList.add('sel');document.getElementById('mo-start-btn').disabled=false;ensureAudio();};}
    grid.appendChild(div);
  });
}

function startMission(){
  if(selMis===null)return;
  document.getElementById('mission-ov').style.display='none';
  initGame(selMis);
}

// ── INPUT ──────────────────────────────────────────────
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  const rx=e.clientX-r.left, ry=e.clientY-r.top;
  if(G){G.mouse.x=rx;G.mouse.y=ry;}
});
canvas.addEventListener('click',e=>{if(G&&G.phase==='play'){ensureAudio();fire();}});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G&&G.phase==='play')toggleScope();});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift'&&G)G.breathHeld=true;
  if(e.key===' '){e.preventDefault();if(G&&G.phase==='play'){ensureAudio();fire();}}
  if((e.key==='r'||e.key==='R')&&G&&G.phase==='play')startReload();
  if((e.key==='z'||e.key==='Z'||e.key==='Escape')&&G&&G.phase==='play')toggleScope();
  if((e.key==='c'||e.key==='C')&&G&&G.phase==='play')setCover(true);
  const numMap={'1':'warrior','2':'archer','3':'knight','4':'medic','5':'sniper_a'};
  if(numMap[e.key]&&G&&G.phase==='play'){ensureAudio();summonUnit(numMap[e.key]);}
});
document.addEventListener('keyup',e=>{
  if(e.key==='Shift'&&G)G.breathHeld=false;
  if((e.key==='c'||e.key==='C')&&G)setCover(false);
});
window.addEventListener('resize',()=>{
  GW=window.innerWidth;GH=window.innerHeight;
  canvas.width=GW;canvas.height=GH;
  scopeR=Math.min(GW,GH)*0.28;
});

// ── MAIN LOOP ──────────────────────────────────────────
function loop(ts){
  const dt=Math.min((ts-lastTs)/1000,.05);lastTs=ts;
  ctx.save();
  if(G&&(G.shakeX||G.shakeY))ctx.translate(Math.round(G.shakeX),Math.round(G.shakeY));
  ctx.clearRect(-12,-12,GW+24,GH+24);

  if(G&&G.phase==='play'){
    tick(dt);
    // 일반 씬 렌더링
    drawScene(ctx,GW,GH);
    // 스코프 오버레이 (캔버스 직접)
    if(G.scoped) {
      drawScopeOverlay(ctx, GW, GH);
    } else {
      // 일반 크로스헤어
      drawCrosshair(ctx, G.mouse.x, G.mouse.y);
    }
  } else {
    ctx.fillStyle='#06080a';ctx.fillRect(0,0,GW,GH);
    // 대기 화면 크로스헤어
    if(G&&G.scoped) drawScopeOverlay(ctx,GW,GH);
  }
  ctx.restore();
  RAF=requestAnimationFrame(loop);
}

buildTitle();
RAF=requestAnimationFrame(loop);
</script>
</body>
</html>"""

def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import load_db, save_db
    from utils.config import USERS_FILE
    import json

    qp = st.query_params

    if qp.get('sniper_score'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            s_score = int(qp.get('sniper_score', 0))
            s_grade = qp.get('sniper_grade', '')
            s_midx  = int(qp.get('sniper_midx', -1))
            if uid and s_score > 0:
                _users = load_db(USERS_FILE, {})
                cur_rec = _users.get(uid, {}).get('game_records', st.session_state.get('game_records', {}))
                changed = False
                if s_score > cur_rec.get('sniper', {}).get('score', 0):
                    cur_rec.setdefault('sniper', {}).update({'score': s_score, 'grade': s_grade})
                    changed = True
                    st.toast(f"🏆 스나이퍼 최고기록 갱신! {s_score:,}점 ({s_grade}등급)", icon="🎯")
                if s_midx >= 0:
                    clears = cur_rec.get('sniper', {}).get('clears', [])
                    if s_midx not in clears:
                        clears.append(s_midx)
                        cur_rec.setdefault('sniper', {})['clears'] = clears
                        changed = True
                if changed:
                    st.session_state.game_records = cur_rec
                    if uid in _users:
                        _users[uid]['game_records'] = cur_rec
                        save_db(USERS_FILE, _users)
                    sync_user_data()
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    cleared_list = []
    try:
        gr = st.session_state.get('game_records', {})
        cleared_list = gr.get('sniper', {}).get('clears', [])
    except Exception:
        cleared_list = []

    final_html = GAME_HTML.replace(
        "buildTitle();\nRAF=requestAnimationFrame(loop);",
        f"window._sc={json.dumps(cleared_list)};\nbuildTitle();\nRAF=requestAnimationFrame(loop);"
    )

    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
    .block-container{padding:0!important;max-width:100%!important;}
    iframe{border:none!important;}
    </style>
    """, unsafe_allow_html=True)

    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'sniper_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('sniper_score', e.data.score);
        url.searchParams.set('sniper_grade', e.data.grade);
        url.searchParams.set('sniper_midx',  e.data.midx ?? -1);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(final_html, height=900, scrolling=False)
