import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<title>스나이퍼 엘리트 — 전선 돌파</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Rajdhani:wght@500;700;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--grn:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--bg:#06080a;}
html,body{width:100%;height:780px;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100%;height:780px;overflow:hidden;}
canvas{display:block;image-rendering:pixelated;}

/* ── CTRL BAR ── */
#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,.85);border-bottom:1px solid rgba(255,255,255,.07);display:flex;justify-content:center;align-items:center;gap:14px;padding:4px 12px;font-size:10px;color:#667;flex-wrap:wrap;}
#ctrl-bar b{color:#f5c518;}
#ctrl-bar span{color:#99a;}

/* ── HUD ── */
#hud{position:absolute;top:34px;left:0;right:0;z-index:100;pointer-events:none;display:flex;gap:5px;padding:5px 10px;align-items:center;}
.hb{background:rgba(0,0,0,.7);border:1px solid rgba(255,255,255,.1);border-radius:7px;padding:3px 9px;text-align:center;min-width:52px;}
.hv{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:var(--gold);}
.hl{font-size:8px;color:#445;letter-spacing:.5px;}
#frontline-wrap{flex:1;margin:0 8px;}
#fl-label{display:flex;justify-content:space-between;font-size:8px;color:#445;margin-bottom:2px;}
#fl-bg{height:8px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;position:relative;}
#fl-fill{position:absolute;top:0;left:0;height:100%;background:linear-gradient(90deg,#1155ff,#3399ff);transition:width .4s;}
#fl-enemy-fill{position:absolute;top:0;right:0;height:100%;background:linear-gradient(270deg,#ff2244,#ff5500);transition:width .4s;}
#fl-marker{position:absolute;top:-2px;width:3px;height:12px;background:#fff;border-radius:1px;transition:left .4s;transform:translateX(-50%);}

/* ── AGGRO GAUGE ── */
#aggro-wrap{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;width:340px;}
#aggro-label{display:flex;justify-content:space-between;font-size:9px;color:#556;margin-bottom:3px;}
#aggro-label .al-title{color:#ff8844;}
#aggro-bg{height:12px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;border:1px solid rgba(255,100,50,.2);}
#aggro-fill{height:100%;background:linear-gradient(90deg,#ffcc00,#ff4400);border-radius:99px;transition:width .1s;}
#aggro-status{font-size:9px;text-align:center;margin-top:3px;color:#556;letter-spacing:1px;}

/* ── PLAYER HP ── */
#player-hp-wrap{position:absolute;bottom:10px;left:10px;z-index:100;pointer-events:none;width:160px;}
#php-label{font-size:8px;color:#556;margin-bottom:2px;}
#php-bg{height:10px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;border:1px solid rgba(0,255,100,.15);}
#php-fill{height:100%;background:linear-gradient(90deg,#00aa44,#00ff88);transition:width .3s;}

/* ── COVER BUTTON ── */
#cover-btn{position:absolute;bottom:10px;right:10px;z-index:100;background:rgba(0,0,0,.75);border:1px solid rgba(0,255,136,.3);border-radius:8px;padding:6px 16px;font-family:'Rajdhani',sans-serif;font-size:12px;color:#00ff88;cursor:pointer;letter-spacing:2px;user-select:none;transition:all .15s;}
#cover-btn.active{background:rgba(0,255,136,.15);border-color:#00ff88;box-shadow:0 0 10px rgba(0,255,136,.3);}

/* ── SCOPE ── */
#scope-wrap{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-bg{position:absolute;inset:0;background:rgba(0,0,0,.95);}
#scope-lens{position:absolute;border-radius:50%;overflow:hidden;left:50%;top:50%;transform:translate(-50%,-50%);border:3px solid rgba(0,255,100,.45);box-shadow:0 0 0 2000px rgba(0,0,0,.95),0 0 30px rgba(0,255,100,.3);width:300px;height:300px;}
#scope-cv{display:block;width:300px;height:300px;}
#scope-cross{position:absolute;pointer-events:none;left:50%;top:50%;transform:translate(-50%,-50%);width:300px;height:300px;}
#scope-info{position:absolute;bottom:20%;left:50%;transform:translateX(-50%);font-family:'Rajdhani',sans-serif;font-size:11px;color:#0f9;letter-spacing:2px;text-align:center;}
#breath-bar{position:absolute;bottom:15%;left:50%;transform:translateX(-50%);width:160px;}
#breath-bg{height:5px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:#00ff88;transition:width .05s;}

/* ── OVERLAYS ── */
#warning-flash{position:absolute;inset:0;z-index:190;pointer-events:none;background:rgba(255,0,50,.0);transition:background .1s;}
#warning-flash.show{background:rgba(255,0,50,.35);}
#toast{position:absolute;top:52px;left:50%;transform:translateX(-50%) translateY(-70px);background:rgba(5,15,5,.97);border:1px solid rgba(245,197,24,.4);border-radius:5px;padding:6px 16px;z-index:280;pointer-events:none;transition:transform .22s;white-space:nowrap;font-size:11px;color:var(--gold);letter-spacing:1px;}
#toast.show{transform:translateX(-50%) translateY(0);}
#killfeed{position:absolute;top:60px;right:10px;z-index:200;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kf{background:rgba(0,0,0,.8);border-left:3px solid #ff4444;border-radius:3px;padding:3px 8px;font-size:10px;color:#ccc;animation:kfIn .25s ease;}
@keyframes kfIn{from{transform:translateX(25px);opacity:0}to{transform:none;opacity:1}}
.dnum{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dUp .9s ease forwards;z-index:300;text-shadow:1px 1px 4px rgba(0,0,0,.9);}
@keyframes dUp{0%{opacity:1;transform:translateY(0)}60%{opacity:1;transform:translateY(-28px)}100%{opacity:0;transform:translateY(-55px)}}

/* ── DETECTED BANNER ── */
#detected-banner{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(.7);opacity:0;z-index:250;pointer-events:none;background:rgba(200,0,0,.9);border:2px solid #ff4444;border-radius:8px;padding:12px 32px;font-family:'Black Han Sans',sans-serif;font-size:1.4rem;color:#fff;letter-spacing:4px;text-align:center;transition:all .2s;}
#detected-banner.show{transform:translate(-50%,-50%) scale(1);opacity:1;}

/* ── COVER VIGNETTE ── */
#cover-vignette{position:absolute;inset:0;z-index:40;pointer-events:none;background:radial-gradient(ellipse 60% 50% at 50% 50%, transparent 40%, rgba(0,0,0,.7) 100%);opacity:0;transition:opacity .3s;}
#cover-vignette.show{opacity:1;}

/* ── MISSION SCREEN ── */
#mission-ov{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.95);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;}
.mo-title{font-family:'Black Han Sans',sans-serif;font-size:2.2rem;color:var(--gold);letter-spacing:8px;text-shadow:0 0 30px rgba(245,197,24,.5);margin-bottom:4px;}
.mo-sub{font-size:.72rem;color:#334;letter-spacing:3px;margin-bottom:20px;}
.mission-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:560px;margin-bottom:18px;}
.mis-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:9px;padding:12px 8px;cursor:pointer;transition:all .18s;text-align:center;}
.mis-card:hover,.mis-card.sel{border-color:rgba(245,197,24,.5);background:rgba(245,197,24,.05);}
.mis-card.locked{opacity:.25;cursor:default;}
.mc-num{font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:900;color:var(--gold);}
.mc-name{font-family:'Black Han Sans',sans-serif;font-size:10px;color:#aab;margin:3px 0 2px;}
.mc-diff{font-size:8px;color:#445;}
.mc-clr{font-size:8px;color:#0f9;margin-top:2px;}
.mo-start{padding:11px 46px;background:linear-gradient(135deg,#1a3a00,#2a6600);border:1px solid #4a9a00;border-radius:6px;color:#88ff44;font-family:'Black Han Sans',sans-serif;font-size:13px;letter-spacing:4px;cursor:pointer;transition:all .2s;}
.mo-start:hover{transform:scale(1.05);filter:brightness(1.2);}
.mo-start:disabled{opacity:.3;cursor:default;transform:none;}

/* ── RESULT ── */
#result-ov{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.92);display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:1.9rem;letter-spacing:5px;}
.res-stats{display:grid;grid-template-columns:1fr 1fr;gap:7px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);border-radius:9px;padding:14px 20px;min-width:300px;}
.rs{font-size:11px;color:#556;display:flex;justify-content:space-between;gap:14px;}
.rs b{color:var(--gold);}
.res-btns{display:flex;gap:10px;}
.rbtn{padding:8px 26px;border:none;border-radius:5px;cursor:pointer;font-family:'Black Han Sans',sans-serif;font-size:12px;letter-spacing:2px;transition:all .15s;}
.rbtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.rbtn.retry{background:linear-gradient(135deg,#1a3a00,#2a6600);color:#88ff44;border:1px solid #4a9a00;}
.rbtn.back{background:rgba(255,255,255,.05);color:#555;border:1px solid rgba(255,255,255,.1);}

/* ── WAR CRY ── */
#war-cry{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:240;font-family:'Black Han Sans',sans-serif;font-size:1.6rem;color:#00ff88;text-shadow:0 0 20px rgba(0,255,136,.8),0 0 40px rgba(0,255,136,.4);pointer-events:none;opacity:0;transition:opacity .3s;letter-spacing:4px;white-space:nowrap;}
#war-cry.show{opacity:1;}
</style>
</head>
<body>
<div id="root">
<canvas id="gc"></canvas>

<div id="ctrl-bar">
  <span><b>클릭/SPACE</b> 발사</span><span>|</span>
  <span><b>우클릭/Z</b> 스코프</span><span>|</span>
  <span><b>C/버튼</b> 엄폐</span><span>|</span>
  <span><b>R</b> 재장전</span><span>|</span>
  <span><b>SHIFT</b> 숨참기</span>
</div>

<div id="hud">
  <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
  <div class="hb"><div class="hv" id="kill-v">0</div><div class="hl">킬</div></div>
  <div class="hb"><div class="hv" id="timer-v">--:--</div><div class="hl">TIME</div></div>
  <div class="hb"><div class="hv" id="ammo-v">5/5</div><div class="hl">탄약</div></div>
  <div id="frontline-wrap">
    <div id="fl-label"><span>🔵 아군 본진</span><span>적 본진 🔴</span></div>
    <div id="fl-bg">
      <div id="fl-fill"></div>
      <div id="fl-enemy-fill"></div>
      <div id="fl-marker"></div>
    </div>
  </div>
</div>

<div id="aggro-wrap">
  <div id="aggro-label"><span class="al-title">⚠️ 발각 위험도</span><span id="aggro-pct">0%</span></div>
  <div id="aggro-bg"><div id="aggro-fill" style="width:0%"></div></div>
  <div id="aggro-status">은폐 유지 중 — 안전</div>
</div>

<div id="player-hp-wrap">
  <div id="php-label">저격수 HP</div>
  <div id="php-bg"><div id="php-fill" style="width:100%"></div></div>
</div>

<div id="cover-btn" id="cover-btn" onmousedown="setCover(true)" onmouseup="setCover(false)" ontouchstart="setCover(true)" ontouchend="setCover(false)">[ C ] 엄폐</div>

<div id="scope-wrap">
  <div id="scope-bg"></div>
  <div id="scope-lens"><canvas id="scope-cv"></canvas></div>
  <svg id="scope-cross" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
    <circle cx="150" cy="150" r="148" stroke="rgba(0,255,100,.35)" stroke-width="1.5" fill="none"/>
    <line x1="0" y1="150" x2="120" y2="150" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="180" y1="150" x2="300" y2="150" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="150" y1="0" x2="150" y2="120" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="150" y1="180" x2="150" y2="300" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <circle cx="150" cy="150" r="2.5" stroke="rgba(0,255,100,.9)" stroke-width="1" fill="none"/>
    <line x1="120" y1="165" x2="180" y2="165" stroke="rgba(0,255,100,.3)" stroke-width=".8"/>
    <line x1="120" y1="135" x2="180" y2="135" stroke="rgba(0,255,100,.3)" stroke-width=".8"/>
  </svg>
  <div id="scope-info"></div>
  <div id="breath-bar"><div style="font-size:8px;color:#334;margin-bottom:2px;text-align:center;">BREATH</div><div id="breath-bg"><div id="breath-fill" style="width:100%"></div></div></div>
</div>

<div id="cover-vignette"></div>
<div id="warning-flash"></div>
<div id="detected-banner">💥 발각됨!</div>
<div id="war-cry"></div>
<div id="toast"></div>
<div id="killfeed"></div>

<div id="mission-ov">
  <div class="mo-title">🎯 스나이퍼 엘리트</div>
  <div class="mo-sub">전선 돌파 작전 — FRONTLINE BREACH</div>
  <div class="mission-grid" id="mission-grid"></div>
  <button class="mo-start" id="mo-start-btn" disabled onclick="startMission()">작전 개시 ▶</button>
</div>

<div id="result-ov">
  <div class="res-title" id="res-title"></div>
  <div class="res-stats" id="res-stats"></div>
  <div class="res-btns">
    <button class="rbtn retry" onclick="retryMission()">재시도 ↺</button>
    <button class="rbtn back" onclick="gotoTitle()">타이틀</button>
  </div>
</div>
</div>

<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  스나이퍼 엘리트 — 전선 돌파 v3.0
//  전술적 은폐·발각 시스템 + 전선 밀기 + 병사 비주얼
// ══════════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
const scvs   = document.getElementById('scope-cv');
const sCtx   = scvs.getContext('2d');
const GW = 900, GH = 640;
canvas.width = GW; canvas.height = GH;

let G = null, selMis = null, RAF, lastTs = 0, gTimer = 0;

// ── MISSIONS ──────────────────────────────────────────────────
const MISSIONS = [
  { id:1, name:'도강 엄호', diff:'⭐ 초급', timeLimit:120, startLine:430,
    allyN:8, enemyN:10, reward:5_000_000,
    keyTargets:[{type:'mg',n:1}],
    desc:'아군의 도강 작전. 기관총 사수 1명을 제거해 전진로를 열어라.' },
  { id:2, name:'고지 탈환', diff:'⭐⭐ 보통', timeLimit:150, startLine:460,
    allyN:10, enemyN:15, reward:15_000_000,
    keyTargets:[{type:'mg',n:2},{type:'officer',n:1}],
    desc:'중요 고지 탈환 작전. 기관총 2정과 장교 1명을 제거하라.' },
  { id:3, name:'시가전', diff:'⭐⭐⭐ 어려움', timeLimit:180, startLine:480,
    allyN:12, enemyN:22, reward:30_000_000,
    keyTargets:[{type:'mg',n:2},{type:'officer',n:2},{type:'sniper_e',n:1}],
    desc:'도심 시가전. 적 저격수와 지휘관을 우선 제압하라.' },
  { id:4, name:'포위망 탈출', diff:'⭐⭐⭐⭐ 전문가', timeLimit:210, startLine:500,
    allyN:7, enemyN:30, reward:60_000_000,
    keyTargets:[{type:'mg',n:3},{type:'officer',n:2},{type:'sniper_e',n:2}],
    desc:'포위된 아군 구출. 수적 열세를 정밀 저격으로 극복하라.' },
  { id:5, name:'사령부 공략', diff:'⭐⭐⭐⭐⭐ 전설', timeLimit:240, startLine:520,
    allyN:14, enemyN:35, reward:150_000_000,
    keyTargets:[{type:'mg',n:3},{type:'officer',n:3},{type:'sniper_e',n:2},{type:'general',n:1}],
    desc:'적 사령부 총공격. 총사령관 처치 시 적군 전체가 패주한다.' },
  { id:6, name:'결전의 날', diff:'⭐⭐⭐⭐⭐ 신화', timeLimit:300, startLine:540,
    allyN:10, enemyN:45, reward:500_000_000,
    keyTargets:[{type:'mg',n:4},{type:'officer',n:4},{type:'sniper_e',n:3},{type:'general',n:2}],
    desc:'최후의 대결전. 모든 지휘부를 무력화하고 전선을 돌파하라.' },
];

// ── ENTITY CONFIG ────────────────────────────────────────────
const ECFG = {
  infantry: { name:'보병',    hp:80,  xp:80,  sz:10, key:false, mgSupp:0,   moraleBoost:0,  color:'#aa2800', hcolor:'#885500', speed:0.3 },
  mg:       { name:'기관총병',hp:140, xp:400, sz:12, key:true,  mgSupp:18,  moraleBoost:0,  color:'#881500', hcolor:'#664400', speed:0   },
  officer:  { name:'장교',    hp:180, xp:500, sz:11, key:true,  mgSupp:0,   moraleBoost:20, color:'#6a0000', hcolor:'#551100', speed:0.3 },
  sniper_e: { name:'적저격수',hp:90,  xp:600, sz:9,  key:true,  mgSupp:0,   moraleBoost:0,  color:'#334422', hcolor:'#223311', speed:0.2 },
  general:  { name:'총사령관',hp:350, xp:2000,sz:14, key:true,  mgSupp:0,   moraleBoost:35, color:'#440000', hcolor:'#330000', speed:0.2 },
};

// ── INIT GAME ─────────────────────────────────────────────────
function initGame(midx) {
  const mis = MISSIONS[midx];
  G = {
    midx, mis, phase:'play',
    time: mis.timeLimit,
    score:0, kills:0, keyKills:0,
    playerHP:100, allyHP:100,
    frontlineX: mis.startLine,
    allies:[], enemies:[], bullets:[], particles:[],
    aggro:0,
    coverActive:false,
    isDetected:false, detectedTimer:0,
    suppressionLevel:0, enemyMorale:50,
    warCry:'', warCryTimer:0,
    shakeX:0, shakeY:0,
    scoped:false, breathHeld:false, breathTimer:3,
    swayX:0, swayY:0, swayT:0,
    shootCd:0, ammo:5, maxAmmo:5,
    reloading:false, reloadTimer:0,
    mouse:{x:GW/2,y:GH/2},
    frame:0, done:false,
    spawnTimer:0,
    failReason:'',
  };

  // Spawn allies along left of frontline
  for (let i = 0; i < mis.allyN; i++) spawnAlly();

  // Spawn key targets
  for (const kt of mis.keyTargets) {
    for (let j = 0; j < kt.n; j++) spawnEnemy(kt.type);
  }
  // Fill with infantry
  for (let i = 0; i < mis.enemyN; i++) spawnEnemy('infantry');

  updateHUD();
}

function spawnAlly() {
  const y = 115 + Math.random() * (GH - 210);
  const beh = 18 + Math.random() * 45;
  G.allies.push({
    x: G.frontlineX - beh, targetX: G.frontlineX - beh,
    y, vx:0, vy:0,
    hp: 60 + Math.random()*30, maxHp:80,
    phase: Math.random()*Math.PI*2,
    fireTimer: 0.4 + Math.random()*1.8,
    state:'crouching', alive:true,
    animT:0, idx: Math.floor(Math.random()*3),
  });
}

function spawnEnemy(type) {
  const c = ECFG[type];
  const y = 115 + Math.random() * (GH - 210);
  const aheadBase = type === 'general' ? 60 : type === 'mg' ? 20 : type === 'sniper_e' ? 40 : 18;
  const ex = G.frontlineX + aheadBase + Math.random() * 45;
  G.enemies.push({
    type, x:ex, y, targetX:ex,
    hp: c.hp + Math.round(c.hp*0.18*G.midx),
    maxHp: c.hp + Math.round(c.hp*0.18*G.midx),
    sz: c.sz, xp: Math.round(c.xp*(1+G.midx*0.2)),
    key:c.key, mgSupp:c.mgSupp, moraleBoost:c.moraleBoost,
    color:c.color, hcolor:c.hcolor, speed:c.speed,
    name:c.name,
    alive:true, dying:false, deathT:0,
    phase: Math.random()*Math.PI*2,
    fireTimer: type==='mg' ? 0.12 : 0.6 + Math.random()*1.5,
    snipeTimer: type==='sniper_e' ? (4+Math.random()*7) : 0,
    animT:0, idx: Math.floor(Math.random()*3),
  });
}

// ── TICK ─────────────────────────────────────────────────────
function tick(dt) {
  if (!G || G.phase !== 'play' || G.done) return;
  G.frame++;
  gTimer += dt;
  G.time -= dt;
  G.swayT += dt;
  G.shootCd = Math.max(0, G.shootCd - dt);

  // Sway
  const sm = G.breathHeld ? 0.06 : G.coverActive ? 1.3 : 1;
  G.swayX = (Math.sin(G.swayT*0.85)*5 + Math.sin(G.swayT*2.1)*2) * sm;
  G.swayY = (Math.cos(G.swayT*0.72)*4 + Math.cos(G.swayT*1.7)*2) * sm;

  // Breath
  if (G.breathHeld) { G.breathTimer -= dt*0.38; if (G.breathTimer<=0){G.breathHeld=false;G.breathTimer=0;} }
  else G.breathTimer = Math.min(3, G.breathTimer + dt*0.5);

  // Reload
  if (G.reloading) {
    G.reloadTimer -= dt;
    if (G.reloadTimer <= 0) { G.reloading=false; G.ammo=G.maxAmmo; showToast('탄창 장전!'); updateHUD(); }
  }

  // Aggro decay
  if (G.coverActive) G.aggro = Math.max(0, G.aggro - dt*38);
  else G.aggro = Math.max(0, G.aggro - dt*4);

  // Detection event
  if (G.aggro >= 100 && !G.isDetected) triggerDetection();
  if (G.isDetected) {
    G.detectedTimer -= dt;
    G.shakeX = (Math.random()-0.5)*10;
    G.shakeY = (Math.random()-0.5)*10;
    if (G.detectedTimer <= 0) {
      G.isDetected = false;
      G.shakeX = G.shakeY = 0;
      G.aggro = 20;
      document.getElementById('detected-banner').classList.remove('show');
      document.getElementById('warning-flash').classList.remove('show');
    }
  } else { G.shakeX *= 0.8; G.shakeY *= 0.8; }

  // Suppression & morale
  let totalSupp = 0, totalMorale = 40;
  for (const e of G.enemies) {
    if (e.alive) { totalSupp += e.mgSupp; totalMorale += e.moraleBoost; }
  }
  G.suppressionLevel = Math.min(100, totalSupp);
  G.enemyMorale = Math.min(100, totalMorale);

  // Frontline movement
  tickFrontline(dt);

  tickAllies(dt);
  tickEnemies(dt);
  tickBullets(dt);
  tickParticles(dt);

  if (G.suppressionLevel > 40) G.allyHP -= dt*(G.suppressionLevel-40)*0.12;
  G.allyHP = Math.max(0, Math.min(100, G.allyHP));

  if (G.warCryTimer > 0) {
    G.warCryTimer -= dt;
    const el = document.getElementById('war-cry');
    if (G.warCryTimer <= 0) el.classList.remove('show');
  }

  updateHUD();
  checkEnd();
}

function triggerDetection() {
  G.isDetected = true;
  G.detectedTimer = 2.2;
  const dmg = 22 + G.midx * 4;
  G.playerHP = Math.max(0, G.playerHP - dmg);
  document.getElementById('detected-banner').classList.add('show');
  document.getElementById('warning-flash').classList.add('show');
  showKF('💥 발각! 적 포격 개시!', '#ff0000');
  showToast('⚠️ 발각됨! 즉시 엄폐!');
  for (let i=0;i<10;i++) addParticle(50+Math.random()*180, 120+Math.random()*(GH-200), '#ff6600', 'exp');
  sfx_detected();
}

function tickFrontline(dt) {
  const mgAlive = G.enemies.filter(e=>e.alive&&e.type==='mg').length;
  const allyAlive = G.allies.filter(a=>a.alive).length;

  // Ally advance rate
  let pushRate = 0;
  if (mgAlive === 0) {
    pushRate = 5 + (G.enemyMorale < 60 ? 6 : 0);
  } else {
    pushRate = -2.5 * mgAlive;
  }

  // Enemy push back
  const enemyPush = (G.enemyMorale / 100) * 2.5;
  const allyStrength = Math.max(0.3, allyAlive / G.mis.allyN);
  const net = (pushRate * allyStrength) - enemyPush;

  G.frontlineX = Math.max(80, Math.min(820, G.frontlineX + net * dt));

  // Keep soldiers near their frontline
  for (const a of G.allies) {
    if (!a.alive) continue;
    a.targetX = G.frontlineX - 18 - Math.random()*40;
    a.x += (a.targetX - a.x) * dt * 1.8;
  }
  for (const e of G.enemies) {
    if (!e.alive || e.dying || e.type==='mg') continue;
    e.targetX = G.frontlineX + 18 + Math.random()*40;
    e.x += (e.targetX - e.x) * dt * 1.5;
  }
}

function tickAllies(dt) {
  if (G.frame % 280 === 0 && G.allies.filter(a=>a.alive).length < Math.max(3, G.mis.allyN - G.kills) && G.allyHP > 15) {
    spawnAlly();
  }
  for (const a of G.allies) {
    if (!a.alive) continue;
    a.phase += dt * 2.8;
    a.animT += dt;
    a.fireTimer -= dt;
    if (a.fireTimer <= 0) {
      a.fireTimer = 0.5 + Math.random()*1.8;
      const ne = nearestEnemy(a.x, a.y);
      if (ne && ne.x - a.x < 320) {
        fireBullet(a.x+8, a.y, ne.x, ne.y, 12+Math.random()*8, false, 'ally');
        addParticle(a.x+10, a.y, '#ffffaa', 'muzzle');
        ne.hp -= 12 + Math.random()*8;
        if (ne.hp <= 0) killEnemy(ne, false);
      }
    }
    a.y = Math.max(115, Math.min(GH-55, a.y + Math.sin(a.phase)*0.1));
  }
}

function tickEnemies(dt) {
  for (const e of G.enemies) {
    if (e.dying) { e.deathT += dt; if (e.deathT > 0.65) { e.dying=false; e.alive=false; } continue; }
    if (!e.alive) continue;
    e.phase += dt * 2.5;
    e.animT += dt;

    // Fire at allies
    e.fireTimer -= dt;
    if (e.fireTimer <= 0) {
      e.fireTimer = e.type==='mg' ? 0.14 : 0.6+Math.random()*1.6;
      const na = nearestAlly(e.x, e.y);
      if (na && e.x - na.x < 320) {
        fireBullet(e.x-8, e.y, na.x, na.y, e.type==='mg'?8:14, false, 'enemy');
        addParticle(e.x-10, e.y, '#ffaa44', 'muzzle');
        na.hp -= (e.type==='mg'?5:9)+Math.random()*5;
        if (na.hp <= 0) { na.alive=false; G.allyHP-=9; addParticle(na.x,na.y,'#4488ff','blood'); }
      }
    }

    // Enemy sniper counter-snipe
    if (e.type==='sniper_e' && G.scoped && !G.coverActive) {
      e.snipeTimer -= dt;
      if (e.snipeTimer <= 0) {
        e.snipeTimer = 3.5 + Math.random()*6;
        G.aggro = Math.min(100, G.aggro + 45);
        showKF('⚠️ 적 저격수 역조준!', '#ff4400');
        if (G.aggro >= 80) { G.playerHP -= 12; showToast('적 저격수 공격!'); }
      }
    }
  }
}

function nearestEnemy(x, y) {
  let best=null, bd=Infinity;
  for (const e of G.enemies) { if(!e.alive||e.dying) continue; const d=Math.hypot(e.x-x,e.y-y); if(d<bd){bd=d;best=e;} }
  return best;
}
function nearestAlly(x, y) {
  let best=null, bd=Infinity;
  for (const a of G.allies) { if(!a.alive) continue; const d=Math.hypot(a.x-x,a.y-y); if(d<bd){bd=d;best=a;} }
  return best;
}

function fireBullet(x1,y1,x2,y2,dmg,isPlayer,faction) {
  const dx=x2-x1, dy=y2-y1, d=Math.hypot(dx,dy)+0.001;
  const spd=580;
  G.bullets.push({x:x1,y:y1,vx:(dx/d)*spd,vy:(dy/d)*spd,dmg,isPlayer,faction,life:d/spd+0.6});
}

function tickBullets(dt) {
  for (let i=G.bullets.length-1;i>=0;i--) {
    const b=G.bullets[i];
    b.x+=b.vx*dt; b.y+=b.vy*dt; b.life-=dt;
    if (b.life<=0||b.x<0||b.x>GW||b.y<0||b.y>GH) { G.bullets.splice(i,1); continue; }
    if (b.isPlayer) {
      for (const e of G.enemies) {
        if(!e.alive||e.dying) continue;
        if(Math.hypot(e.x-b.x,e.y-b.y) < e.sz+4) {
          e.hp-=b.dmg;
          spawnDmgNum(e.x,e.y,Math.round(b.dmg),b.crit);
          addParticle(e.x,e.y,'#ff4444','blood');
          if(e.hp<=0) killEnemy(e,true);
          G.bullets.splice(i,1); break;
        }
      }
    }
  }
}

function tickParticles(dt) {
  for (let i=G.particles.length-1;i>=0;i--) {
    const p=G.particles[i];
    p.x+=p.vx*dt; p.y+=p.vy*dt;
    p.vy+=90*dt;
    p.life-=dt;
    if(p.life<=0) G.particles.splice(i,1);
  }
}

function addParticle(x,y,col,type) {
  const cnt=type==='exp'?10:type==='blood'?6:3;
  for(let i=0;i<cnt;i++) {
    G.particles.push({
      x,y,
      vx:(Math.random()-0.5)*(type==='exp'?140:70),
      vy:-Math.random()*(type==='exp'?110:55),
      life:0.25+Math.random()*0.35,
      col: type==='muzzle'?'#ffff88':col,
      r: type==='exp'?2+Math.random()*3:1.5,
    });
  }
}

function killEnemy(e, byPlayer) {
  if(!e.alive||e.dying) return;
  e.dying=true; e.deathT=0;
  addParticle(e.x,e.y,'#cc2200','blood');
  if(!byPlayer) return;

  G.kills++; G.score+=e.xp;

  if(e.key) {
    G.keyKills++;
    let push=0, cry='', kfmsg='', kfcol='#f5c518';
    switch(e.type) {
      case 'mg':
        push=52; cry='아군 전진!'; kfmsg='💥 기관총 제압! 전선 전진!'; kfcol='#00ff88';
        showToast('기관총 처치! 아군 전진!');
        break;
      case 'officer':
        push=30; cry='장교 처치!'; kfmsg='🎖️ 장교 제거! 적 사기 하락!'; kfcol='#f5c518';
        showToast('장교 처치! 적 전선 약화!');
        break;
      case 'general':
        push=90; cry='총사령관 처치!\n전면 돌파!'; kfmsg='🏅 총사령관 처치! 적군 패주!'; kfcol='#ff4400';
        showToast('총사령관 처치! 전면 돌파 개시!');
        break;
      case 'sniper_e':
        push=22; cry='적 저격수 제거!'; kfmsg='🎯 적 저격수 처치!'; kfcol='#00aaff';
        showToast('적 저격수 처치!');
        break;
    }
    if(push>0) G.frontlineX = Math.min(820, G.frontlineX+push);
    if(cry) showWarCry(cry);
    showKF(kfmsg, kfcol);
  } else {
    showKF(`보병 처치 +${e.xp}`, '#888');
  }
}

// ── FIRE ─────────────────────────────────────────────────────
function fire() {
  if(!G||G.phase!=='play'||G.done) return;
  if(G.coverActive){ showToast('엄폐 중엔 발사 불가!'); return; }
  if(G.reloading||G.shootCd>0) return;
  if(G.ammo<=0){ startReload(); return; }
  G.ammo--; G.shootCd=0.9; updateHUD();
  ensureAudio();

  // Aggro spike
  G.aggro = Math.min(100, G.aggro+24);

  const crit = G.breathHeld && Math.random()<0.22;
  let aimX=G.mouse.x, aimY=G.mouse.y;
  if(G.scoped) {
    const z=3.5;
    aimX = G.mouse.x + (G._scopeAimX-150)/z;
    aimY = G.mouse.y + (G._scopeAimY-150)/z;
  }
  const sw = G.breathHeld?0.18:2.8;
  aimX += (Math.random()-0.5)*sw*2 + G.swayX*(G.scoped?0.18:0.45);
  aimY += (Math.random()-0.5)*sw*2 + G.swayY*(G.scoped?0.18:0.45);

  // Hit detection
  let hit=false;
  for(const e of G.enemies) {
    if(!e.alive||e.dying) continue;
    if(Math.hypot(aimX-e.x,aimY-e.y) < e.sz+5) {
      const dmg = crit ? e.sz*15 : 85+Math.random()*20;
      e.hp -= dmg;
      spawnDmgNum(e.x,e.y,Math.round(dmg),crit);
      addParticle(e.x,e.y,'#ff3333','blood');
      if(e.hp<=0) killEnemy(e,true);
      hit=true; break;
    }
  }
  if(!hit) {
    // Near miss → small aggro boost
    for(const e of G.enemies) {
      if(!e.alive) continue;
      if(Math.hypot(aimX-e.x,aimY-e.y)<40) { G.aggro=Math.min(100,G.aggro+9); break; }
    }
    addParticle(aimX,aimY,'#cc8844','blood');
  }

  addParticle(65, GH-40, '#ffffcc', 'muzzle');
  sfx_shoot();
  if(G.ammo===0) setTimeout(startReload,300);
}

G && (G._scopeAimX=150);
G && (G._scopeAimY=150);

function startReload() {
  if(!G||G.reloading||G.ammo===G.maxAmmo) return;
  G.reloading=true; G.reloadTimer=2.2;
  showToast('재장전 중...');
}

function setCover(on) {
  if(!G||G.phase!=='play'||G.done) return;
  G.coverActive=on;
  document.getElementById('cover-btn').className = on ? 'active' : '';
  document.getElementById('cover-vignette').className = on ? 'show' : '';
  if(on && G.scoped) toggleScope();
}

function toggleScope() {
  if(!G||G.phase!=='play'||G.done) return;
  if(G.coverActive && !G.scoped) { showToast('엄폐 중엔 스코프 사용 불가!'); return; }
  G.scoped=!G.scoped;
  document.getElementById('scope-wrap').style.display=G.scoped?'block':'none';
}

// ── WIN/LOSE ─────────────────────────────────────────────────
function checkEnd() {
  if(G.done) return;
  if(G.frontlineX>=820){ G.done=true; showResult(true); return; }
  if(G.playerHP<=0||G.frontlineX<=80||G.time<=0||G.allyHP<=0) {
    G.done=true;
    G.failReason = G.playerHP<=0?'저격수 전사':G.frontlineX<=80?'전선 붕괴':G.time<=0?'시간 초과':'아군 전멸';
    showResult(false);
  }
}

function showResult(win) {
  G.phase='result';
  if(G.scoped) toggleScope();
  const el=document.getElementById('result-ov');
  const t=document.getElementById('res-title');
  t.textContent=win?'🏆 작전 성공!':'💀 '+G.failReason;
  t.style.color=win?'#f5c518':'#ff2244';
  const elapsed=G.mis.timeLimit-G.time;
  const fl=Math.round((G.frontlineX-G.mis.startLine)/(820-G.mis.startLine)*100);
  document.getElementById('res-stats').innerHTML=`
    <div class="rs">처치<b>${G.kills}</b></div>
    <div class="rs">점수<b>${Math.round(G.score).toLocaleString()}</b></div>
    <div class="rs">경과시간<b>${Math.floor(elapsed/60)}m${Math.floor(elapsed%60)}s</b></div>
    <div class="rs">저격수HP<b>${Math.round(G.playerHP)}%</b></div>
    <div class="rs">전선전진<b>${Math.max(0,fl)}%</b></div>
    <div class="rs">등급<b>${grade()}</b></div>`;
  el.style.display='flex';
  if(win){ sfx_win(); try{window.parent.postMessage({type:'sniper_result',score:Math.round(G.score),grade:grade()},'*');}catch(e){} }
  else sfx_fail();
}

function grade(){const s=G.score;return s>=60000?'S':s>=35000?'A':s>=15000?'B':'C';}
function retryMission(){document.getElementById('result-ov').style.display='none';initGame(G.midx);}
function gotoTitle(){document.getElementById('result-ov').style.display='none';G=null;buildTitle();document.getElementById('mission-ov').style.display='flex';}

// ── DRAW SOLDIERS ────────────────────────────────────────────
function drawSoldier(c, x, y, side, type, alive, dying, deathT, phase, animT) {
  // side: 'ally'=left-facing troops | 'enemy'=right->left
  // type: infantry|mg|officer|sniper_e|general
  const isAlly = (side==='ally');
  const alpha = dying ? Math.max(0,1-deathT/0.65) : 1;
  const bobY = Math.sin(phase)*1.5;
  const crouchOff = 3; // soldiers are crouching

  c.save();
  c.globalAlpha = alpha;
  c.translate(Math.round(x), Math.round(y + bobY));

  // Colors
  let helmetC, bodyC, pantC, gearC;
  if(isAlly) {
    helmetC='#2a4a8a'; bodyC='#2a3a2a'; pantC='#1a2a1a'; gearC='#3a5a3a';
  } else {
    helmetC = type==='general'?'#553300':type==='officer'?'#443300':type==='sniper_e'?'#1a2a1a':'#554433';
    bodyC   = type==='general'?'#3a1500':type==='officer'?'#2a1500':type==='sniper_e'?'#1a2a1a':'#3a2a1a';
    pantC   = type==='general'?'#2a1000':type==='officer'?'#1a1000':'#2a1a0a';
    gearC   = '#4a3a2a';
  }

  const dir = isAlly ? 1 : -1; // gun direction
  const sz  = type==='general'?1.3:type==='mg'?1.15:1;

  c.scale(sz,sz);

  // ── BODY (crouching pose) ──
  // Boots / legs
  c.fillStyle=pantC;
  c.fillRect(-4, 4, 4, 7); // left leg
  c.fillRect(1,  4, 4, 7); // right leg
  c.fillStyle='#222';
  c.fillRect(-4, 10, 4, 3); // left boot
  c.fillRect(1,  10, 4, 3); // right boot

  // Torso
  c.fillStyle=bodyC;
  c.fillRect(-5, -4, 10, 9);

  // Gear / vest
  c.fillStyle=gearC;
  c.fillRect(-4, -3, 8, 7);
  // Vest pockets
  c.fillStyle=isAlly?'#1a3a1a':'#2a1a0a';
  c.fillRect(-3, -1, 3, 3);
  c.fillRect(1, -1, 3, 3);

  // Arms
  c.fillStyle=bodyC;
  c.fillRect(-8, -4, 4, 6); // left arm
  c.fillRect(5,  -4, 4, 6); // right arm

  // Head
  c.fillStyle='#c8a074';
  c.beginPath(); c.arc(0, -9, 4, 0, Math.PI*2); c.fill();

  // Helmet
  c.fillStyle=helmetC;
  c.beginPath();
  if(type==='officer'||type==='general') {
    // Officer cap: flat top
    c.fillRect(-6,-16,12,4);
    c.beginPath(); c.arc(0,-14,5,Math.PI,0); c.fill();
    // Badge
    c.fillStyle='#f5c518';
    c.beginPath(); c.arc(0,-15,1.5,0,Math.PI*2); c.fill();
  } else {
    // Round combat helmet
    c.arc(0,-13,6,Math.PI,0);
    c.lineTo(6,-11); c.arc(0,-11,6,0,Math.PI); c.closePath(); c.fill();
    // Helmet rim
    c.fillStyle = isAlly?'#1a3a6a':'#3a2a1a';
    c.fillRect(-7,-12,14,2);
  }

  // Sniper: add camo face
  if(type==='sniper_e') {
    c.fillStyle='rgba(0,40,0,0.5)';
    c.fillRect(-4,-12,8,6);
  }
  // General: epaulettes
  if(type==='general') {
    c.fillStyle='#f5c518';
    c.fillRect(-9,-4,4,3);
    c.fillRect(6,-4,4,3);
  }

  // ── GUN ──
  c.fillStyle='#222';
  if(type==='mg') {
    // MG: longer barrel, bipod
    c.fillRect(dir*4, -2, dir*20, 4);
    // Bipod
    c.fillRect(dir*18, 2, 2, 8);
    c.fillRect(dir*22, 2, 2, 8);
    // Ammo drum
    c.fillStyle='#3a3a3a';
    c.beginPath(); c.arc(dir*10, 2, 4, 0, Math.PI*2); c.fill();
  } else if(type==='sniper_e') {
    // Long sniper rifle, low
    c.fillRect(dir*4, 0, dir*24, 3);
    // Scope on rifle
    c.fillStyle='#1a1a3a';
    c.fillRect(dir*10, -3, 8, 3);
    // Muzzle
    c.fillStyle='#444';
    c.fillRect(dir*26, -1, dir*4, 5);
  } else {
    // Assault rifle
    c.fillRect(dir*4, -1, dir*16, 4);
    // Magazine
    c.fillRect(dir*10, 3, 4, 6);
    // Grip
    c.fillRect(dir*6, 3, 3, 5);
  }

  c.restore();
}

function drawAlly(c,a) { drawSoldier(c,a.x,a.y,'ally','infantry',a.alive,false,0,a.phase,a.animT); }
function drawEnemy(c,e) { drawSoldier(c,e.x,e.y,'enemy',e.type,e.alive,e.dying,e.deathT,e.phase,e.animT); }

// ── DRAW SCENE ────────────────────────────────────────────────
function drawScene(c, isScope) {
  const W=GW, H=GH;

  // Sky gradient
  const sky=c.createLinearGradient(0,0,0,H*0.38);
  sky.addColorStop(0,'#0a1520'); sky.addColorStop(1,'#1a2a18');
  c.fillStyle=sky; c.fillRect(0,0,W,H);

  // Ground
  const gnd=c.createLinearGradient(0,H*0.35,0,H);
  gnd.addColorStop(0,'#1e3010'); gnd.addColorStop(1,'#111d08');
  c.fillStyle=gnd; c.fillRect(0,H*0.35,W,H);

  // Distant trees/hills silhouette
  c.fillStyle='#0a1808';
  for(let tx=0;tx<W;tx+=60) {
    const th=30+Math.sin(tx*0.07)*18;
    c.fillRect(tx,H*0.38-th,55,th+5);
  }

  // Terrain features
  drawTerrain(c,W,H);

  // Frontline indicator
  if(!isScope) {
    const fx = G ? G.frontlineX : W/2;
    c.save();
    c.strokeStyle='rgba(255,255,255,0.15)';
    c.lineWidth=1; c.setLineDash([6,8]);
    c.beginPath(); c.moveTo(fx,90); c.lineTo(fx,H-50); c.stroke();
    c.setLineDash([]);
    // Frontline label
    c.fillStyle='rgba(255,255,255,0.25)';
    c.font='bold 9px Orbitron'; c.textAlign='center';
    c.fillText('FRONTLINE',fx,86);
    c.restore();
  }

  if(!G) return;

  // Draw particles
  for(const p of G.particles) {
    c.save();
    c.globalAlpha=Math.max(0,p.life*2.5);
    c.fillStyle=p.col;
    c.beginPath(); c.arc(p.x,p.y,p.r,0,Math.PI*2); c.fill();
    c.restore();
  }

  // Draw ally soldiers
  for(const a of G.allies) {
    if(!a.alive) continue;
    drawAlly(c,a);
  }

  // Draw enemy soldiers
  for(const e of G.enemies) {
    if(!e.alive && !e.dying) continue;
    drawEnemy(c,e);
    // Key target marker
    if(e.key && e.alive) {
      c.save();
      c.fillStyle='rgba(255,80,0,0.7)';
      c.font='9px sans-serif'; c.textAlign='center';
      c.fillText(
        e.type==='general'?'★사령관':e.type==='officer'?'★장교':e.type==='mg'?'★기관총':'★저격',
        e.x, e.y - e.sz - 16
      );
      // HP bar above key target
      const bw=e.sz*3.5, pct=Math.max(0,e.hp/e.maxHp);
      c.fillStyle='rgba(0,0,0,.6)'; c.fillRect(e.x-bw/2, e.y-e.sz-12, bw, 5);
      c.fillStyle=pct>0.5?'#22cc44':pct>0.25?'#ccaa00':'#cc2200';
      c.fillRect(e.x-bw/2, e.y-e.sz-12, bw*pct, 5);
      c.restore();
    } else if(e.alive && !e.key) {
      // Tiny HP bar for normal infantry
      const pct=Math.max(0,e.hp/e.maxHp);
      if(pct<1) {
        c.save();
        c.fillStyle='rgba(0,0,0,.5)'; c.fillRect(e.x-8,e.y-e.sz-8,16,3);
        c.fillStyle='#cc2200'; c.fillRect(e.x-8,e.y-e.sz-8,16*pct,3);
        c.restore();
      }
    }
  }

  // Draw bullets
  for(const b of G.bullets) {
    c.save();
    c.fillStyle=b.isPlayer?'#ffffa0':b.faction==='ally'?'#88aaff':'#ff8844';
    c.shadowColor=c.fillStyle; c.shadowBlur=6;
    c.beginPath(); c.arc(b.x,b.y,b.isPlayer?3:2,0,Math.PI*2); c.fill();
    c.shadowBlur=0; c.restore();
  }

  // Player sniper position (bottom-left)
  if(!isScope) drawSniperPos(c);
}

function drawTerrain(c,W,H) {
  // Sandbags (cover) - ally side
  c.save();
  const sbColor='#3a2a10';
  const sandbagPositions=[[90,300],[90,200],[90,420],[150,260],[150,370]];
  for(const[sx,sy]of sandbagPositions) {
    c.fillStyle=sbColor;
    c.beginPath(); c.ellipse(sx,sy,18,8,0,0,Math.PI*2); c.fill();
    c.fillStyle='#4a3a18';
    c.beginPath(); c.ellipse(sx-5,sy-2,10,5,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(sx+5,sy-2,10,5,0,0,Math.PI*2); c.fill();
  }
  // Enemy side rocks/cover
  const rockPositions=[[780,280],[780,400],[740,200],[740,450],[820,340]];
  c.fillStyle='#2a2a2a';
  for(const[rx,ry]of rockPositions) {
    c.beginPath(); c.ellipse(rx,ry,16,10,0.3,0,Math.PI*2); c.fill();
    c.fillStyle='#3a3a3a';
    c.beginPath(); c.ellipse(rx-4,ry-3,9,6,0.2,0,Math.PI*2); c.fill();
    c.fillStyle='#2a2a2a';
  }
  // Craters
  const craterPos=[[320,310],[500,270],[650,390],[420,180],[560,440]];
  for(const[cx,cy]of craterPos) {
    c.fillStyle='#0c1408';
    c.beginPath(); c.ellipse(cx,cy,22,14,0,0,Math.PI*2); c.fill();
    c.strokeStyle='#1a2210'; c.lineWidth=2;
    c.beginPath(); c.ellipse(cx,cy,22,14,0,0,Math.PI*2); c.stroke();
  }
  // Burnt tree stumps
  c.fillStyle='#1a1008';
  const stumps=[[260,380],[440,200],[700,300]];
  for(const[tx,ty]of stumps) {
    c.fillRect(tx-3,ty-20,6,20);
    c.fillRect(tx-6,ty,12,6);
  }
  c.restore();
}

function drawSniperPos(c) {
  c.save();
  // Sniper hide / ghillie position at bottom-left
  c.translate(65, GH-40);
  c.fillStyle='rgba(0,80,20,0.4)';
  c.beginPath(); c.ellipse(0,0,30,12,0,0,Math.PI*2); c.fill();
  c.fillStyle='#1a3a0a'; c.font='18px serif';
  c.textAlign='center'; c.textBaseline='middle';
  c.fillText('🎯',0,0);
  // Aim line when scoped
  if(G.scoped) {
    c.strokeStyle='rgba(0,255,100,0.08)'; c.lineWidth=1; c.setLineDash([3,7]);
    c.beginPath(); c.moveTo(0,0); c.lineTo(G.mouse.x-65,G.mouse.y-(GH-40)); c.stroke();
    c.setLineDash([]);
  }
  c.restore();

  // Suppression warning
  if(G.suppressionLevel>50) {
    c.save();
    c.globalAlpha=0.3+Math.sin(gTimer*9)*0.25;
    c.fillStyle='#ff7700'; c.font='bold 12px Orbitron';
    c.textAlign='center';
    c.fillText('⚠️ 아군 제압 중!',GW/2,75);
    c.restore();
  }

  // Cover state indicator
  if(G.coverActive) {
    c.save();
    c.fillStyle='rgba(0,255,136,0.15)';
    c.fillRect(0,GH-60,200,60);
    c.fillStyle='#00ff88'; c.font='bold 10px Orbitron';
    c.textAlign='left';
    c.fillText('▐ 엄폐 중 — 발각도 감소',10,GH-38);
    c.fillText('  발사 불가',10,GH-20);
    c.restore();
  }
}

// ── SCOPE VIEW ────────────────────────────────────────────────
function drawScopeView() {
  if(!G||!G.scoped) return;
  const zoom=3.5;
  const cx=G.mouse.x, cy=G.mouse.y;
  sCtx.save();
  sCtx.fillStyle='#0a1408';
  sCtx.fillRect(0,0,300,300);
  sCtx.scale(zoom,zoom);
  sCtx.translate(150/zoom-cx+G.swayX*0.25, 150/zoom-cy+G.swayY*0.25);
  drawScene(sCtx,true);
  sCtx.restore();

  if(!G._scopeAimX) G._scopeAimX=150;
  if(!G._scopeAimY) G._scopeAimY=150;

  const dist=Math.round(Math.hypot(G.mouse.x-65,G.mouse.y-(GH-40)));
  document.getElementById('scope-info').textContent=
    `${dist}m | ${G.breathHeld?'숨참기 ✓':'안정화 필요'} | ${G.ammo}/${G.maxAmmo}`;
  document.getElementById('breath-fill').style.width=(G.breathTimer/3*100)+'%';
}

// ── HUD UPDATE ────────────────────────────────────────────────
function updateHUD() {
  if(!G) return;
  document.getElementById('score-v').textContent=Math.round(G.score).toLocaleString();
  document.getElementById('kill-v').textContent=G.kills;
  const t=Math.max(0,G.time);
  document.getElementById('timer-v').textContent=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  document.getElementById('ammo-v').textContent=G.reloading?'장전...':`${G.ammo}/${G.maxAmmo}`;

  // Frontline bar
  const total=820-80; const pos=G.frontlineX-80;
  const allyPct=(pos/total*100).toFixed(1);
  const enemyPct=(100-allyPct).toFixed(1);
  document.getElementById('fl-fill').style.width=allyPct+'%';
  document.getElementById('fl-enemy-fill').style.width=enemyPct+'%';
  document.getElementById('fl-marker').style.left=allyPct+'%';

  // Aggro gauge
  const ap=Math.round(G.aggro);
  document.getElementById('aggro-fill').style.width=ap+'%';
  document.getElementById('aggro-fill').style.background=ap>70?'linear-gradient(90deg,#ff4400,#ff0000)':ap>40?'linear-gradient(90deg,#ffcc00,#ff6600)':'linear-gradient(90deg,#ffcc00,#ff4400)';
  document.getElementById('aggro-pct').textContent=ap+'%';
  const st=ap<30?'은폐 유지 중 — 안전':ap<60?'주의 — 노출 위험':ap<85?'⚠️ 위험! 즉시 엄폐!':'🔴 발각 직전!';
  document.getElementById('aggro-status').textContent=st;
  document.getElementById('aggro-status').style.color=ap>60?'#ff4400':'#556';

  // Player HP
  document.getElementById('php-fill').style.width=Math.round(G.playerHP)+'%';
  document.getElementById('php-fill').style.background=G.playerHP>60?'linear-gradient(90deg,#00aa44,#00ff88)':G.playerHP>30?'linear-gradient(90deg,#cc8800,#ffcc00)':'linear-gradient(90deg,#cc0000,#ff4444)';

  // Cover button highlight
  if(G.coverActive) {
    document.getElementById('cover-btn').classList.add('active');
  } else {
    document.getElementById('cover-btn').classList.remove('active');
  }
}

// ── UI HELPERS ────────────────────────────────────────────────
function showWarCry(msg) {
  const el=document.getElementById('war-cry');
  el.textContent=msg; el.classList.add('show');
  G.warCryTimer=2.5;
}

function showToast(msg) {
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2000);
}

function showKF(msg,col) {
  const kf=document.getElementById('killfeed');
  const it=document.createElement('div'); it.className='kf';
  it.style.color=col||'#ccc'; it.textContent=msg;
  kf.appendChild(it);
  setTimeout(()=>{it.style.opacity='0';it.style.transition='opacity .5s';setTimeout(()=>it.remove(),500);},2500);
  while(kf.children.length>5) kf.removeChild(kf.firstChild);
}

function spawnDmgNum(x,y,v,crit) {
  const el=document.createElement('div'); el.className='dnum';
  const r=canvas.getBoundingClientRect();
  el.style.cssText=`left:${r.left+x-20}px;top:${r.top+y-10}px;font-size:${crit?22:14}px;color:${crit?'#ffff44':'#fff'};`;
  el.textContent=crit?`${v}!!`:`${v}`;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),950);
}

// ── AUDIO ─────────────────────────────────────────────────────
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function beep(f,t,d,v=.2,delay=0){if(!ACtx)return;try{
  const o=ACtx.createOscillator(),g=ACtx.createGain();
  o.connect(g);g.connect(ACtx.destination);o.type=t;o.frequency.value=f;
  const ts=ACtx.currentTime+delay;
  g.gain.setValueAtTime(0,ts);g.gain.linearRampToValueAtTime(v,ts+.005);
  g.gain.exponentialRampToValueAtTime(.001,ts+d);o.start(ts);o.stop(ts+d+.05);
}catch(e){}}
function sfx_shoot(){ensureAudio();beep(180,'sawtooth',.1,.35);beep(85,'sine',.16,.25,.05);}
function sfx_detected(){ensureAudio();[800,600,400,200].forEach((f,i)=>beep(f,'sawtooth',.15,.4,i*.08));}
function sfx_win(){ensureAudio();[523,659,784,1047].forEach((f,i)=>beep(f,'sine',.3,.3,i*.12));}
function sfx_fail(){ensureAudio();[300,220,160].forEach((f,i)=>beep(f,'sawtooth',.3,.3,i*.14));}

// ── TITLE ─────────────────────────────────────────────────────
function buildTitle(){
  const cleared=JSON.parse(localStorage.getItem('sniper_clears')||'[]');
  const grid=document.getElementById('mission-grid');
  grid.innerHTML='';
  MISSIONS.forEach((m,i)=>{
    const locked=i>0&&!cleared.includes(i-1);
    const div=document.createElement('div');
    div.className='mis-card'+(locked?' locked':'');
    div.innerHTML=`<div class="mc-num">${i+1}</div><div class="mc-name">${m.name}</div><div class="mc-diff">${m.diff}</div>${cleared.includes(i)?'<div class="mc-clr">✅ 완료</div>':''}`;
    if(!locked){div.onclick=()=>{selMis=i;document.querySelectorAll('.mis-card').forEach(x=>x.classList.remove('sel'));div.classList.add('sel');document.getElementById('mo-start-btn').disabled=false;ensureAudio();};}
    grid.appendChild(div);
  });
}

function startMission(){
  if(selMis===null) return;
  document.getElementById('mission-ov').style.display='none';
  initGame(selMis);
}

// ── INPUT ─────────────────────────────────────────────────────
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  if(G){G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;}
  if(G&&G.scoped){
    G._scopeAimX=150+(e.clientX-r.left-G.mouse.x)*3.5;
    G._scopeAimY=150+(e.clientY-r.top -G.mouse.y)*3.5;
    G._scopeAimX=150; G._scopeAimY=150; // center by default
  }
});
canvas.addEventListener('click',e=>{if(G&&G.phase==='play'){ensureAudio();fire();}});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G&&G.phase==='play')toggleScope();});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift'&&G) G.breathHeld=true;
  if(e.key===' '){e.preventDefault();if(G&&G.phase==='play'){ensureAudio();fire();}}
  if((e.key==='r'||e.key==='R')&&G&&G.phase==='play') startReload();
  if((e.key==='z'||e.key==='Z'||e.key==='Escape')&&G&&G.phase==='play') toggleScope();
  if((e.key==='c'||e.key==='C')&&G&&G.phase==='play') setCover(true);
});
document.addEventListener('keyup',e=>{
  if(e.key==='Shift'&&G) G.breathHeld=false;
  if((e.key==='c'||e.key==='C')&&G) setCover(false);
});

// ── MAIN LOOP ─────────────────────────────────────────────────
function loop(ts) {
  const dt=Math.min((ts-lastTs)/1000,0.05); lastTs=ts;
  ctx.save();
  if(G){ctx.translate(Math.round(G.shakeX),Math.round(G.shakeY));}
  ctx.clearRect(-10,-10,GW+20,GH+20);
  if(G&&G.phase==='play'){ tick(dt); drawScene(ctx,false); drawScopeView(); }
  else{ ctx.fillStyle='#06080a'; ctx.fillRect(0,0,GW,GH); }
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

    qp = st.query_params
    if qp.get('sniper_score'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            s_score = int(qp.get('sniper_score', 0))
            s_grade = qp.get('sniper_grade', '')
            if uid and s_score > 0:
                _users = load_db(USERS_FILE, {})
                cur_rec = _users.get(uid, {}).get('game_records', st.session_state.get('game_records', {}))
                if s_score > cur_rec.get('sniper', {}).get('score', 0):
                    cur_rec.setdefault('sniper', {}).update({'score': s_score, 'grade': s_grade})
                    st.session_state.game_records = cur_rec
                    if uid in _users:
                        _users[uid]['game_records'] = cur_rec
                        save_db(USERS_FILE, _users)
                    sync_user_data()
                    st.toast(f"🏆 스나이퍼 최고기록 갱신! {s_score:,}점 ({s_grade}등급)", icon="🎯")
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <div style='background:linear-gradient(135deg,#060a06,#0c1a0c);border:1px solid rgba(0,255,100,0.2);
      border-radius:16px;padding:16px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>
      <div style='font-size:2rem;'>🎯</div>
      <div>
        <div style='font-family:"Black Han Sans",sans-serif;font-size:1.1rem;color:#e8ffe8;'>
          🎯 스나이퍼 엘리트 — 전선 돌파 작전
        </div>
        <div style='font-size:0.82rem;color:#6a9a6a;margin-top:2px;'>
          발각도를 관리하며 은밀하게 저격, 아군의 전선을 적 본진까지 밀어라!
        </div>
        <div style='font-size:0.76rem;color:#4a7a4a;margin-top:4px;'>
          🖱️ 클릭/SPACE: 발사 | 우클릭/Z: 스코프 | C(누르는 동안): 엄폐 | R: 재장전 | SHIFT: 숨참기
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)

    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'sniper_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('sniper_score', e.data.score);
        url.searchParams.set('sniper_grade', e.data.grade);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=785, scrolling=False)
