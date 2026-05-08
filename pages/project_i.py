import streamlit as st
import streamlit.components.v1 as components
import json

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0,user-scalable=no">
<title>라인 배틀 저격전</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Rajdhani:wght@500;700;900&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--grn:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--bg:#06080a;--blue:#4488ff;}
html,body{width:100%;height:100vh;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:100vh;overflow:hidden;}
canvas{display:block;}
.in-game,.in-game *{cursor:none!important;}

/* CTRL BAR */
#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,.92);border-bottom:1px solid rgba(255,255,255,.06);display:flex;justify-content:center;align-items:center;gap:10px;padding:3px 10px;font-size:9px;color:#556;flex-wrap:wrap;}
#ctrl-bar b{color:#f5c518;}

/* HUD TOP */
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

/* AMMO */
#ammo-strip{position:absolute;top:72px;right:10px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;align-items:flex-end;}
.ammo-pip{width:6px;height:18px;border-radius:2px;background:#f5c518;border:1px solid rgba(255,255,255,.2);box-shadow:0 0 4px rgba(245,197,24,.4);transition:all .15s;}
.ammo-pip.empty{background:#1a1a1a;border-color:#333;box-shadow:none;}

/* SUMMON PANEL */
#summon-panel{position:absolute;left:0;top:64px;bottom:50px;width:120px;z-index:100;display:flex;flex-direction:column;gap:4px;padding:6px;background:rgba(0,0,0,.7);border-right:1px solid rgba(0,255,136,.12);}
#summon-title{font-size:7px;color:#0f9;letter-spacing:1px;text-align:center;margin-bottom:4px;border-bottom:1px solid rgba(0,255,136,.15);padding-bottom:4px;}
#resource-row{display:flex;align-items:center;justify-content:center;gap:4px;font-family:'Rajdhani',sans-serif;font-size:13px;font-weight:900;color:#f5c518;margin-bottom:5px;}
.summon-btn{background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.25);border-radius:5px;padding:4px 5px;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;gap:2px;user-select:none;}
.summon-btn:hover{background:rgba(0,255,136,.18);border-color:#00ff88;box-shadow:0 0 8px rgba(0,255,136,.25);}
.summon-btn:active{transform:scale(0.95);}
.summon-btn.disabled{opacity:.3;cursor:not-allowed;}
.sb-ico{font-size:14px;}.sb-name{font-size:7px;color:#aaa;letter-spacing:.5px;}
.sb-cost{font-size:7px;color:#f5c518;font-family:'Rajdhani',sans-serif;font-weight:700;}

/* COVER BTN */
#cover-btn{position:absolute;bottom:14px;right:10px;z-index:100;background:rgba(0,0,0,.8);border:1px solid rgba(0,255,136,.25);border-radius:7px;padding:5px 13px;font-family:'Rajdhani',sans-serif;font-size:11px;color:#00ff88;cursor:pointer;letter-spacing:1px;user-select:none;transition:all .12s;}
#cover-btn.active{background:rgba(0,255,136,.12);border-color:#00ff88;box-shadow:0 0 12px rgba(0,255,136,.35);}

/* AMMO/RELOAD */
#php-wrap{position:absolute;left:130px;bottom:14px;z-index:100;pointer-events:none;width:150px;}
#php-label{font-size:7px;color:#445;letter-spacing:1px;margin-bottom:3px;display:flex;justify-content:space-between;}
#php-track{height:8px;background:rgba(0,0,0,.5);border-radius:99px;overflow:hidden;border:1px solid rgba(0,255,100,.1);}
#php-fill{height:100%;background:linear-gradient(90deg,#00aa44,#00ff88);border-radius:99px;transition:width .3s;}
#reload-bar-wrap{position:absolute;left:130px;bottom:26px;z-index:100;pointer-events:none;width:150px;display:none;}
#reload-bar-fill{height:5px;background:var(--cyan);border-radius:99px;width:0%;transition:width .05s;}

/* OVERLAYS */
#warning-flash{position:absolute;inset:0;z-index:190;pointer-events:none;opacity:0;background:rgba(255,0,40,.4);transition:opacity .08s;}
#cover-vignette{position:absolute;inset:0;z-index:40;pointer-events:none;background:radial-gradient(ellipse 55% 45% at 50% 50%,transparent 35%,rgba(0,0,0,.75) 100%);opacity:0;transition:opacity .3s;}
#cover-vignette.on{opacity:1;}
#muzzle-flash{position:absolute;inset:0;z-index:35;pointer-events:none;opacity:0;background:radial-gradient(ellipse at 8% 90%,rgba(255,220,100,.2),transparent 38%);transition:opacity .05s;}

/* TOAST */
#toast-wrap{position:absolute;top:58px;left:50%;transform:translateX(-50%);z-index:280;display:flex;flex-direction:column;gap:5px;align-items:center;pointer-events:none;}
.toast-item{background:rgba(4,12,4,.97);border:1px solid rgba(245,197,24,.35);border-radius:4px;padding:5px 14px;font-size:10px;color:var(--gold);letter-spacing:1px;white-space:nowrap;animation:toastSlide .2s ease,toastFade .4s ease 1.6s forwards;}
@keyframes toastSlide{from{transform:translateY(-14px);opacity:0}to{transform:none;opacity:1}}
@keyframes toastFade{to{opacity:0}}
.toast-item.red{border-color:rgba(255,50,50,.4);color:#ff6666;}
.toast-item.grn{border-color:rgba(0,255,100,.4);color:#00ff88;}
.toast-item.blue{border-color:rgba(0,200,255,.4);color:#00d4ff;}

/* KILLFEED */
#killfeed{position:absolute;top:68px;right:8px;z-index:200;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kf-item{font-family:'Rajdhani',sans-serif;font-size:9px;color:rgba(255,100,100,.9);text-align:right;letter-spacing:.5px;animation:kfFade .2s ease,kfFade .5s ease 2s forwards;}
@keyframes kfFade{to{opacity:0}}

/* BASE HP */
#ally-hp{position:absolute;left:0;bottom:50px;z-index:100;pointer-events:none;width:140px;padding:4px 6px;background:rgba(0,0,0,.7);}
#enemy-hp{position:absolute;right:0;bottom:50px;z-index:100;pointer-events:none;width:140px;padding:4px 6px;background:rgba(0,0,0,.7);text-align:right;}
.base-lbl{font-size:7px;color:#334;margin-bottom:2px;letter-spacing:.8px;}
.base-track{height:7px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;}
.base-fill-ally{height:100%;background:linear-gradient(90deg,#0066ff,#44aaff);border-radius:99px;transition:width .3s;}
.base-fill-enemy{height:100%;background:linear-gradient(90deg,#ff4400,#ff8800);border-radius:99px;float:right;transition:width .3s;}

/* SCREENS */
#title-screen,#result-screen,#difficulty-screen{position:absolute;inset:0;z-index:300;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(4,6,10,.97);}
.title-logo{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,7vw,4rem);background:linear-gradient(135deg,#f5c518,#ff8800,#ff2244);-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 30px rgba(255,100,0,.4));letter-spacing:4px;text-align:center;}
.sub-txt{font-size:clamp(.6rem,2vw,.85rem);color:#334;letter-spacing:3px;margin:8px 0 24px;}
.diff-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:16px 0;}
.diff-btn{padding:14px 24px;border-radius:10px;border:1.5px solid;cursor:pointer;font-family:'Rajdhani',sans-serif;font-size:1.05rem;font-weight:900;letter-spacing:2px;transition:all .15s;text-align:center;min-width:160px;}
.diff-btn:hover{transform:scale(1.04);filter:brightness(1.2);}
.diff-easy{border-color:#00ff88;color:#00ff88;background:rgba(0,255,136,.07);}
.diff-med{border-color:#f5c518;color:#f5c518;background:rgba(245,197,24,.07);}
.diff-hard{border-color:#ff8800;color:#ff8800;background:rgba(255,136,0,.08);}
.diff-hell{border-color:#ff2244;color:#ff2244;background:rgba(255,34,68,.08);}
.diff-sub{font-size:.62rem;color:#445;letter-spacing:1px;margin-top:3px;}
.start-btn{padding:12px 40px;border-radius:8px;border:2px solid var(--gold);color:var(--gold);background:rgba(245,197,24,.08);font-family:'Rajdhani',sans-serif;font-size:1.1rem;font-weight:900;letter-spacing:3px;cursor:pointer;transition:all .15s;margin-top:8px;}
.start-btn:hover{background:rgba(245,197,24,.18);box-shadow:0 0 20px rgba(245,197,24,.3);}
.result-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.8rem,6vw,3.5rem);letter-spacing:4px;text-align:center;margin-bottom:16px;}
.result-stat{font-family:'Rajdhani',sans-serif;font-size:1.1rem;color:#aaa;letter-spacing:2px;margin:5px 0;}
.result-stat span{color:var(--gold);}
.lb-banner{background:rgba(245,197,24,.12);border:1.5px solid rgba(245,197,24,.5);border-radius:10px;padding:10px 24px;margin:14px 0;font-family:'Rajdhani',sans-serif;font-size:1rem;color:var(--gold);letter-spacing:2px;text-align:center;animation:lbPulse 1.2s ease-in-out infinite;}
@keyframes lbPulse{0%,100%{box-shadow:0 0 10px rgba(245,197,24,.3);}50%{box-shadow:0 0 30px rgba(245,197,24,.6);}}
</style>
</head>
<body>
<div id="root">
  <canvas id="gc"></canvas>

  <!-- DIFFICULTY SELECT -->
  <div id="difficulty-screen">
    <div class="title-logo">🎯 라인 배틀 저격전</div>
    <div class="sub-txt">LINE BATTLE SNIPER</div>
    <div class="sub-txt" style="color:#556;font-size:.72rem;">난이도를 선택하세요</div>
    <div class="diff-grid">
      <div class="diff-btn diff-easy" onclick="selectDiff('easy')">초보<div class="diff-sub">적 체력 70% · 느린 스폰</div></div>
      <div class="diff-btn diff-med" onclick="selectDiff('medium')">중급<div class="diff-sub">적 체력 100% · 기본 스폰</div></div>
      <div class="diff-btn diff-hard" onclick="selectDiff('hard')">어려움<div class="diff-sub">적 체력 140% · 빠른 스폰</div></div>
      <div class="diff-btn diff-hell" onclick="selectDiff('hell')">극악<div class="diff-sub">적 체력 200% · 매우 빠름</div></div>
    </div>
    <div id="diff-chosen" style="font-family:'Rajdhani',sans-serif;font-size:.9rem;color:#556;min-height:28px;"></div>
    <button class="start-btn" id="start-btn" style="display:none" onclick="startGame()">▶ 전투 개시</button>
    <div style="margin-top:18px;font-size:.65rem;color:#223;letter-spacing:2px;">RMB·F: 스코프 | 1~5: 유닛 소환 | C: 엄폐 | 클릭: 발사</div>
  </div>

  <!-- RESULT SCREEN -->
  <div id="result-screen" style="display:none;">
    <div class="result-title" id="result-title">승리!</div>
    <div class="result-stat">총 킬 수: <span id="r-kills">0</span></div>
    <div class="result-stat">기지 잔존 HP: <span id="r-hp">0</span>%</div>
    <div class="result-stat">난이도: <span id="r-diff">-</span></div>
    <div id="lb-banner" class="lb-banner" style="display:none;">👑 전국 1위 달성! 명예의 전당 등재!</div>
    <div style="display:flex;gap:12px;margin-top:20px;">
      <button class="start-btn" onclick="goTitle()">↩ 타이틀</button>
      <button class="start-btn" style="border-color:#00ff88;color:#00ff88;" onclick="retryGame()">▶ 재도전</button>
    </div>
  </div>

  <!-- TITLE SCREEN (between games) -->
  <div id="title-screen" style="display:none;">
    <div class="title-logo">🎯 라인 배틀 저격전</div>
    <div class="sub-txt">LINE BATTLE SNIPER</div>
    <div style="font-size:.7rem;color:#445;margin-bottom:20px;letter-spacing:1px;" id="title-record"></div>
    <button class="start-btn" onclick="showDiffScreen()">▶ 게임 시작</button>
  </div>

  <!-- HUD (in-game) -->
  <div id="ctrl-bar">
    <span><b>RMB/F</b> 스코프</span><span><b>클릭</b> 발사</span>
    <span><b>C</b> 엄폐</span><span><b>1~5</b> 유닛 소환</span>
    <span><b>R</b> 재장전</span>
  </div>
  <div id="hud" style="display:none;">
    <div class="hb"><div class="hv" id="h-kills">0</div><div class="hl">KILLS</div></div>
    <div class="hb"><div class="hv" id="h-res">0</div><div class="hl">RESOURCE</div></div>
    <div id="frontline-wrap">
      <div id="fl-label"><span>아군 기지</span><span>적군 기지</span></div>
      <div id="fl-track">
        <div id="fl-ally" style="width:50%"></div>
        <div id="fl-enemy" style="width:50%"></div>
        <div id="fl-mid" style="left:50%"></div>
      </div>
    </div>
    <div class="hb"><div class="hv" id="h-ammo">5/5</div><div class="hl">AMMO</div></div>
    <div class="hb"><div class="hv" id="h-time">90</div><div class="hl">TIME</div></div>
  </div>

  <!-- SUMMON PANEL -->
  <div id="summon-panel" style="display:none;">
    <div id="summon-title">소환 패널</div>
    <div id="resource-row">💎 <span id="res-count">0</span></div>
    <div class="summon-btn" id="sb1" onclick="summonUnit(0)">
      <span class="sb-ico">🪖</span><span class="sb-name">보병</span><span class="sb-cost">[1] 30</span>
    </div>
    <div class="summon-btn" id="sb2" onclick="summonUnit(1)">
      <span class="sb-ico">⚔️</span><span class="sb-name">돌격대</span><span class="sb-cost">[2] 60</span>
    </div>
    <div class="summon-btn" id="sb3" onclick="summonUnit(2)">
      <span class="sb-ico">🛡️</span><span class="sb-name">중보병</span><span class="sb-cost">[3] 80</span>
    </div>
    <div class="summon-btn" id="sb4" onclick="summonUnit(3)">
      <span class="sb-ico">💊</span><span class="sb-name">의무병</span><span class="sb-cost">[4] 50</span>
    </div>
    <div class="summon-btn" id="sb5" onclick="summonUnit(4)">
      <span class="sb-ico">🎯</span><span class="sb-name">저격수</span><span class="sb-cost">[5] 120</span>
    </div>
  </div>

  <!-- BASE HP BARS -->
  <div id="ally-hp" style="display:none;">
    <div class="base-lbl">🏰 아군 기지</div>
    <div class="base-track"><div class="base-fill-ally" id="ally-fill" style="width:100%"></div></div>
    <div id="ally-hp-txt" style="font-size:8px;color:#2266ff;margin-top:2px;font-family:'Rajdhani',sans-serif;">100%</div>
  </div>
  <div id="enemy-hp" style="display:none;">
    <div class="base-lbl">🏯 적 기지 ▶</div>
    <div class="base-track"><div class="base-fill-enemy" id="enemy-fill" style="width:100%"></div></div>
    <div id="enemy-hp-txt" style="font-size:8px;color:#ff4400;margin-top:2px;font-family:'Rajdhani',sans-serif;">100%</div>
  </div>

  <!-- COVER BTN -->
  <button id="cover-btn" style="display:none;" onclick="toggleCover()">🛡 엄폐</button>

  <!-- AMMO STRIP -->
  <div id="ammo-strip" style="display:none;"></div>

  <!-- OVERLAYS -->
  <div id="warning-flash"></div>
  <div id="cover-vignette"></div>
  <div id="muzzle-flash"></div>
  <div id="toast-wrap"></div>
  <div id="killfeed"></div>
</div>

<script>
// ═══════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════
const DIFF = {
  easy:   {hpMul:0.7,  spawnMul:1.6, baseHp:200, resMul:1.3, label:'초보'},
  medium: {hpMul:1.0,  spawnMul:1.0, baseHp:150, resMul:1.0, label:'중급'},
  hard:   {hpMul:1.4,  spawnMul:0.7, baseHp:100, resMul:0.85,label:'어려움'},
  hell:   {hpMul:2.0,  spawnMul:0.45,baseHp:70,  resMul:0.7, label:'극악'},
};
const UNIT_TYPES = [
  {name:'보병',    emoji:'🪖', hp:80,  spd:38, atk:12, range:30, cost:30, col:'#4488ff'},
  {name:'돌격대',  emoji:'⚔️', hp:60,  spd:60, atk:20, range:28, cost:60, col:'#00ffaa'},
  {name:'중보병',  emoji:'🛡️', hp:200, spd:22, atk:8,  range:32, cost:80, col:'#88aaff'},
  {name:'의무병',  emoji:'💊', hp:50,  spd:45, atk:5,  range:25, cost:50, col:'#ff88ff', healer:true},
  {name:'저격수',  emoji:'🎯', hp:40,  spd:30, atk:80, range:280,cost:120,col:'#ffcc00'},
];
const ENEMY_TYPES = [
  {name:'적병',    emoji:'👺', hp:70,  spd:35, atk:10, range:30, col:'#ff4400'},
  {name:'중보병',  emoji:'💀', hp:180, spd:20, atk:7,  range:32, col:'#ff8800'},
  {name:'돌격',    emoji:'🔥', hp:55,  spd:58, atk:18, range:26, col:'#ff2244'},
  {name:'지휘관',  emoji:'👿', hp:400, spd:18, atk:22, range:35, col:'#cc00ff'},
];
const AMMO_MAX = 6;
const RELOAD_TIME = 2200; // ms
const GAME_DURATION = 120; // seconds
const SCOPE_ZOOM = 3.5;

// ═══════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');
let GW, GH;
let G = null;
let RAF = null;
let lastTs = 0;
let chosenDiff = null;

// Mouse
const mouse = {x:0, y:0, down:false};
let scoped = false;
let inCover = false;
let ammo = AMMO_MAX;
let reloading = false;
let reloadStart = 0;

// ═══════════════════════════════════════════════════════
// RESIZE
// ═══════════════════════════════════════════════════════
function resize(){
  GW = canvas.width  = window.innerWidth;
  GH = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// ═══════════════════════════════════════════════════════
// DIFFICULTY SELECT
// ═══════════════════════════════════════════════════════
function selectDiff(d){
  chosenDiff = d;
  document.getElementById('diff-chosen').textContent = `선택: ${DIFF[d].label}`;
  document.getElementById('start-btn').style.display = 'block';
  document.querySelectorAll('.diff-btn').forEach(b=>b.style.opacity='.5');
  const map = {easy:0,medium:1,hard:2,hell:3};
  document.querySelectorAll('.diff-btn')[map[d]].style.opacity='1';
}

function showDiffScreen(){
  document.getElementById('title-screen').style.display='none';
  document.getElementById('difficulty-screen').style.display='flex';
  chosenDiff = null;
  document.getElementById('start-btn').style.display='none';
  document.getElementById('diff-chosen').textContent='';
  document.querySelectorAll('.diff-btn').forEach(b=>b.style.opacity='1');
}

// ═══════════════════════════════════════════════════════
// GAME INIT
// ═══════════════════════════════════════════════════════
function initGame(diff){
  const dc = DIFF[diff];
  const allyBaseX = 60;
  const enemyBaseX = GW - 60;
  return {
    diff: diff,
    dc: dc,
    units: [],       // ally units
    enemies: [],     // enemy units
    bullets: [],     // sniper bullets
    enemyBullets: [],
    particles: [],
    frontline: 0.5,  // 0=ally wins, 1=enemy wins
    allyBaseHp: dc.baseHp,
    allyBaseMaxHp: dc.baseHp,
    enemyBaseHp: dc.baseHp,
    enemyBaseMaxHp: dc.baseHp,
    kills: 0,
    resource: 100,
    resourceTimer: 0,
    spawnTimer: 0,
    gameTimer: GAME_DURATION,
    over: false,
    won: null,
    allyBaseX, enemyBaseX,
    groundY: GH * 0.72,
  };
}

// ═══════════════════════════════════════════════════════
// START GAME
// ═══════════════════════════════════════════════════════
function startGame(){
  if(!chosenDiff) return;
  document.getElementById('difficulty-screen').style.display='none';
  document.getElementById('result-screen').style.display='none';
  document.getElementById('title-screen').style.display='none';
  showHUD(true);
  G = initGame(chosenDiff);
  ammo = AMMO_MAX;
  reloading = false;
  scoped = false;
  inCover = false;
  document.getElementById('root').classList.add('in-game');
  updateAmmoStrip();
  lastTs = performance.now();
  if(RAF) cancelAnimationFrame(RAF);
  RAF = requestAnimationFrame(loop);
}

function retryGame(){ startGame(); }

function goTitle(){
  if(RAF){cancelAnimationFrame(RAF);RAF=null;}
  G=null;
  showHUD(false);
  document.getElementById('result-screen').style.display='none';
  document.getElementById('difficulty-screen').style.display='none';
  document.getElementById('title-screen').style.display='flex';
  document.getElementById('root').classList.remove('in-game');
}

function showHUD(on){
  const ids=['hud','summon-panel','ally-hp','enemy-hp','cover-btn','ammo-strip'];
  ids.forEach(id=>{
    const el=document.getElementById(id);
    if(el) el.style.display=on?(id==='hud'?'flex':id==='ammo-strip'?'flex':'block'):'none';
  });
}

// ═══════════════════════════════════════════════════════
// UNIT SUMMON
// ═══════════════════════════════════════════════════════
function summonUnit(typeIdx){
  if(!G||G.over) return;
  const ut = UNIT_TYPES[typeIdx];
  if(G.resource < ut.cost){ toast('자원 부족!','red'); return; }
  G.resource -= ut.cost;
  const hpMul = 1.0; // ally units don't scale with difficulty
  G.units.push({
    type: typeIdx, x: G.allyBaseX + 10, y: G.groundY,
    hp: ut.hp, maxHp: ut.hp, spd: ut.spd,
    atk: ut.atk, range: ut.range, atkTimer: 0,
    emoji: ut.emoji, col: ut.col, healer: !!ut.healer,
    dead: false,
  });
  toast(`${ut.emoji} ${ut.name} 소환!`, 'grn');
  updateSummonBtns();
}

function updateSummonBtns(){
  if(!G) return;
  UNIT_TYPES.forEach((ut,i)=>{
    const btn = document.getElementById('sb'+(i+1));
    if(btn) btn.classList.toggle('disabled', G.resource < ut.cost);
  });
  document.getElementById('res-count').textContent = Math.floor(G.resource);
  document.getElementById('h-res').textContent = Math.floor(G.resource);
}

// ═══════════════════════════════════════════════════════
// COVER
// ═══════════════════════════════════════════════════════
function toggleCover(){
  inCover = !inCover;
  document.getElementById('cover-btn').classList.toggle('active', inCover);
  document.getElementById('cover-vignette').classList.toggle('on', inCover);
}

// ═══════════════════════════════════════════════════════
// AMMO / RELOAD
// ═══════════════════════════════════════════════════════
function updateAmmoStrip(){
  const strip = document.getElementById('ammo-strip');
  if(!strip) return;
  strip.innerHTML = '';
  for(let i=0;i<AMMO_MAX;i++){
    const pip = document.createElement('div');
    pip.className = 'ammo-pip' + (i >= ammo ? ' empty' : '');
    strip.appendChild(pip);
  }
  document.getElementById('h-ammo').textContent = `${ammo}/${AMMO_MAX}`;
}

function startReload(){
  if(reloading||ammo===AMMO_MAX) return;
  reloading = true;
  reloadStart = performance.now();
  toast('장전 중...','blue');
}

// ═══════════════════════════════════════════════════════
// SHOOT
// ═══════════════════════════════════════════════════════
function tryShoot(){
  if(!G||G.over) return;
  if(reloading){ toast('장전 중!','red'); return; }
  if(ammo<=0){ toast('탄약 없음! R로 재장전','red'); startReload(); return; }
  if(inCover) return; // can't shoot from cover (need to peek)
  ammo--;
  updateAmmoStrip();
  // Muzzle flash
  const mf = document.getElementById('muzzle-flash');
  mf.style.opacity='1'; setTimeout(()=>mf.style.opacity='0',80);
  // Bullet from bottom-left (sniper position)
  const bx = 10, by = G.groundY - 20;
  const tx = scoped ? mouse.x : mouse.x;
  const ty = scoped ? mouse.y : mouse.y;
  const dx = tx-bx, dy = ty-by;
  const len = Math.sqrt(dx*dx+dy*dy)||1;
  G.bullets.push({
    x:bx, y:by, vx:(dx/len)*900, vy:(dy/len)*900,
    mx:tx, my:ty, hit:false,
  });
  if(ammo===0) startReload();
}

// ═══════════════════════════════════════════════════════
// SPAWN ENEMY
// ═══════════════════════════════════════════════════════
function spawnEnemy(){
  if(!G) return;
  const t = ENEMY_TYPES[Math.floor(Math.random()*ENEMY_TYPES.length)];
  const hpMul = G.dc.hpMul;
  G.enemies.push({
    x: G.enemyBaseX - 12, y: G.groundY,
    hp: Math.floor(t.hp * hpMul), maxHp: Math.floor(t.hp * hpMul),
    spd: t.spd, atk: t.atk, range: t.range,
    atkTimer: Math.random()*1000,
    emoji: t.emoji, col: t.col,
    dead: false,
  });
}

// ═══════════════════════════════════════════════════════
// MAIN TICK
// ═══════════════════════════════════════════════════════
function tick(dt){
  if(!G||G.over) return;
  const dtS = dt/1000;

  // Timer
  G.gameTimer -= dtS;
  if(G.gameTimer < 0) G.gameTimer = 0;
  document.getElementById('h-time').textContent = Math.ceil(G.gameTimer);

  // Resource regen
  G.resource = Math.min(999, G.resource + dtS * 18 * G.dc.resMul);
  updateSummonBtns();

  // Spawn enemy
  G.spawnTimer += dt;
  const spawnInterval = 3000 * G.dc.spawnMul;
  if(G.spawnTimer >= spawnInterval){
    G.spawnTimer = 0;
    spawnEnemy();
    if(G.dc.spawnMul < 0.6) spawnEnemy(); // double spawn on hell
  }

  // Reload
  if(reloading){
    const elapsed = performance.now() - reloadStart;
    const prog = Math.min(1, elapsed / RELOAD_TIME);
    // show progress via HUD
    if(prog >= 1){
      reloading = false;
      ammo = AMMO_MAX;
      updateAmmoStrip();
      toast('장전 완료!','grn');
    }
  }

  // Move & fight allies
  for(const u of G.units){
    if(u.dead) continue;
    // Heal nearby allies if healer
    if(u.healer){
      for(const a of G.units){
        if(a.dead||a===u) continue;
        if(Math.abs(a.x-u.x)<60) a.hp = Math.min(a.maxHp, a.hp + dtS*15);
      }
    }
    // Find nearest enemy
    let target = null, minD = Infinity;
    for(const e of G.enemies){
      if(e.dead) continue;
      const d = Math.abs(e.x - u.x);
      if(d < minD){ minD=d; target=e; }
    }
    if(target && minD <= u.range){
      u.atkTimer += dt;
      if(u.atkTimer >= 1200){
        u.atkTimer=0;
        target.hp -= u.atk;
        if(target.hp<=0){ target.dead=true; G.kills++; G.resource=Math.min(999,G.resource+10); spawnParticle(target.x,target.y,'#ff4400'); }
      }
    } else {
      // Move toward enemy base
      u.x += u.spd * dtS;
      if(u.x > G.enemyBaseX - 15){
        // Hitting enemy base
        G.enemyBaseHp -= u.atk * dtS * 1.5;
        if(G.enemyBaseHp <= 0){ G.enemyBaseHp=0; endGame(true); return; }
      }
    }
  }

  // Move & fight enemies
  for(const e of G.enemies){
    if(e.dead) continue;
    let target=null, minD=Infinity;
    for(const u of G.units){
      if(u.dead) continue;
      const d = Math.abs(u.x-e.x);
      if(d<minD){minD=d;target=u;}
    }
    if(target && minD <= e.range){
      e.atkTimer += dt;
      if(e.atkTimer >= 1300){
        e.atkTimer=0;
        target.hp -= e.atk;
        if(target.hp<=0) target.dead=true;
      }
    } else {
      e.x -= e.spd * dtS;
      if(e.x < G.allyBaseX + 15){
        G.allyBaseHp -= e.atk * dtS * 1.2;
        if(G.allyBaseHp<=0){G.allyBaseHp=0; endGame(false); return;}
        if(!inCover){
          flashWarning();
          // damage player slightly (visual)
        }
      }
    }
  }

  // Bullets
  for(const b of G.bullets){
    if(b.hit) continue;
    b.x += b.vx * dtS;
    b.y += b.vy * dtS;
    // Hit check vs enemies
    for(const e of G.enemies){
      if(e.dead) continue;
      const dx=e.x-b.x, dy=(e.y-20)-b.y;
      if(Math.sqrt(dx*dx+dy*dy)<16){
        e.hp -= (80 + Math.random()*40);
        b.hit=true;
        spawnParticle(e.x,e.y,'#ffaa00');
        addKillFeed();
        if(e.hp<=0){
          e.dead=true; G.kills++; G.resource=Math.min(999,G.resource+15);
          spawnParticle(e.x,e.y,'#ff2244');
        }
        break;
      }
    }
    // Hit check vs enemy base
    if(!b.hit && Math.abs(b.x-G.enemyBaseX)<30 && Math.abs(b.y-(G.groundY-30))<40){
      G.enemyBaseHp -= 20;
      b.hit=true;
      if(G.enemyBaseHp<=0){G.enemyBaseHp=0; endGame(true);}
    }
    if(b.x<0||b.x>GW||b.y<0||b.y>GH) b.hit=true;
  }

  // Particles
  for(const p of G.particles){
    p.x+=p.vx*dtS; p.y+=p.vy*dtS;
    p.vy+=200*dtS;
    p.life-=dtS;
  }

  // Cleanup
  G.units    = G.units.filter(u=>!u.dead);
  G.enemies  = G.enemies.filter(e=>!e.dead);
  G.bullets  = G.bullets.filter(b=>!b.hit);
  G.particles= G.particles.filter(p=>p.life>0);

  // Time over
  if(G.gameTimer<=0){
    // Decide winner by frontline
    const ally_adv = G.allyBaseHp / G.allyBaseMaxHp - G.enemyBaseHp / G.enemyBaseMaxHp;
    endGame(ally_adv > 0);
    return;
  }

  // Update frontline bar
  const ratio = 1 - (G.enemyBaseHp / G.enemyBaseMaxHp);
  const fl = 0.2 + ratio * 0.6; // 0.2~0.8
  document.getElementById('fl-mid').style.left = (fl*100)+'%';

  // Update HP bars
  const aHpPct = Math.max(0, G.allyBaseHp/G.allyBaseMaxHp*100);
  const eHpPct = Math.max(0, G.enemyBaseHp/G.enemyBaseMaxHp*100);
  document.getElementById('ally-fill').style.width = aHpPct+'%';
  document.getElementById('enemy-fill').style.width = eHpPct+'%';
  document.getElementById('ally-hp-txt').textContent = Math.ceil(aHpPct)+'%';
  document.getElementById('enemy-hp-txt').textContent = Math.ceil(eHpPct)+'%';
  document.getElementById('h-kills').textContent = G.kills;
}

// ═══════════════════════════════════════════════════════
// END GAME
// ═══════════════════════════════════════════════════════
function endGame(won){
  if(!G||G.over) return;
  G.over=true; G.won=won;
  showHUD(false);
  document.getElementById('root').classList.remove('in-game');

  const title = won ? '🎉 승리!' : '💀 패배';
  const color = won ? '#00ff88' : '#ff2244';
  document.getElementById('result-title').textContent = title;
  document.getElementById('result-title').style.color = color;
  document.getElementById('r-kills').textContent = G.kills;
  document.getElementById('r-hp').textContent = Math.ceil(G.allyBaseHp/G.allyBaseMaxHp*100);
  document.getElementById('r-diff').textContent = DIFF[G.diff].label;

  // Report to Streamlit
  try {
    window.parent.postMessage({
      type: 'sniper_result',
      kills: G.kills,
      won: won,
      diff: G.diff,
    }, '*');
  } catch(e) {}

  document.getElementById('result-screen').style.display = 'flex';
}

// ═══════════════════════════════════════════════════════
// DRAW
// ═══════════════════════════════════════════════════════
function drawScene(){
  if(!G){ ctx.fillStyle='#06080a'; ctx.fillRect(0,0,GW,GH); return; }

  // Sky gradient
  const sky = ctx.createLinearGradient(0,0,0,G.groundY);
  sky.addColorStop(0,'#060a14');
  sky.addColorStop(1,'#0a1828');
  ctx.fillStyle=sky; ctx.fillRect(0,0,GW,GH);

  // Ground
  const grd = ctx.createLinearGradient(0,G.groundY,0,GH);
  grd.addColorStop(0,'#1a1200'); grd.addColorStop(1,'#0a0800');
  ctx.fillStyle=grd; ctx.fillRect(0,G.groundY,GW,GH-G.groundY);

  // Ally base (left castle)
  drawBase(G.allyBaseX, G.groundY, '#2266ff', '🏰', G.allyBaseHp/G.allyBaseMaxHp);
  // Enemy base (right castle)
  drawBase(G.enemyBaseX, G.groundY, '#ff4400', '🏯', G.enemyBaseHp/G.enemyBaseMaxHp);

  // Units
  for(const u of G.units) drawUnit(u, '#2266ff', false);
  for(const e of G.enemies) drawUnit(e, e.col, true);

  // Bullets
  ctx.save();
  for(const b of G.bullets){
    ctx.beginPath();
    ctx.arc(b.x, b.y, 3, 0, Math.PI*2);
    ctx.fillStyle='#ffcc00';
    ctx.fill();
    // tracer
    ctx.beginPath();
    ctx.moveTo(b.x, b.y);
    ctx.lineTo(b.x - b.vx*0.025, b.y - b.vy*0.025);
    ctx.strokeStyle='rgba(255,200,0,.4)';
    ctx.lineWidth=1.5;
    ctx.stroke();
  }
  ctx.restore();

  // Particles
  for(const p of G.particles){
    ctx.save();
    ctx.globalAlpha = Math.max(0,p.life);
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
    ctx.fillStyle=p.col; ctx.fill();
    ctx.restore();
  }

  // Scope overlay
  if(scoped) drawScope();
  else drawCrosshair(mouse.x, mouse.y);
}

function drawBase(x, groundY, col, emoji, hpRatio){
  const h = 70 * hpRatio + 20;
  ctx.save();
  ctx.strokeStyle=col; ctx.lineWidth=2;
  ctx.strokeRect(x-18, groundY-h, 36, h);
  ctx.fillStyle=col+'33'; ctx.fillRect(x-18, groundY-h, 36, h);
  ctx.font='22px serif'; ctx.textAlign='center';
  ctx.fillText(emoji, x, groundY-h/2+6);
  // HP bar above
  ctx.fillStyle='#333'; ctx.fillRect(x-20, groundY-h-12, 40, 6);
  ctx.fillStyle=col; ctx.fillRect(x-20, groundY-h-12, 40*hpRatio, 6);
  ctx.restore();
}

function drawUnit(u, col, isEnemy){
  const y = u.y;
  const x = u.x;
  ctx.save();
  // Shadow
  ctx.fillStyle='rgba(0,0,0,.3)';
  ctx.beginPath(); ctx.ellipse(x,y+2,12,4,0,0,Math.PI*2); ctx.fill();
  // Body
  ctx.font='20px serif'; ctx.textAlign='center';
  ctx.fillText(u.emoji||'👤', x, y-4);
  // HP bar
  const bw=24, bh=4;
  ctx.fillStyle='#222'; ctx.fillRect(x-bw/2, y-30, bw, bh);
  const hpPct = u.hp/u.maxHp;
  const hpCol = hpPct>0.5?'#00ff88':hpPct>0.25?'#ffaa00':'#ff2244';
  ctx.fillStyle=hpCol; ctx.fillRect(x-bw/2, y-30, bw*hpPct, bh);
  ctx.restore();
}

function drawCrosshair(cx, cy){
  const r=14, gap=5;
  ctx.save();
  ctx.strokeStyle='rgba(0,255,136,.8)'; ctx.lineWidth=1.5;
  // Cross lines
  ctx.beginPath(); ctx.moveTo(cx-(r),cy); ctx.lineTo(cx-gap,cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx+gap,cy); ctx.lineTo(cx+r,cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx,cy-r); ctx.lineTo(cx,cy-gap); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx,cy+gap); ctx.lineTo(cx,cy+r); ctx.stroke();
  ctx.beginPath(); ctx.arc(cx,cy,3,0,Math.PI*2);
  ctx.fillStyle='rgba(0,255,136,.9)'; ctx.fill();
  ctx.restore();
}

function drawScope(){
  const cx=mouse.x, cy=mouse.y;
  const R=100;
  ctx.save();

  // Dark vignette outside scope
  ctx.fillStyle='rgba(0,0,0,.88)';
  ctx.fillRect(0,0,GW,GH);
  ctx.globalCompositeOperation='destination-out';
  ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2); ctx.fill();
  ctx.globalCompositeOperation='source-over';

  // Draw zoomed scene inside scope
  ctx.save();
  ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2); ctx.clip();
  ctx.translate(cx,cy);
  ctx.scale(SCOPE_ZOOM,SCOPE_ZOOM);
  ctx.translate(-cx,-cy);
  drawScene_noScope(); // draw without scope overlay
  ctx.restore();

  // Scope ring
  ctx.strokeStyle='rgba(0,255,136,.7)'; ctx.lineWidth=2;
  ctx.beginPath(); ctx.arc(cx,cy,R,0,Math.PI*2); ctx.stroke();
  // Scope crosshair
  ctx.strokeStyle='rgba(0,255,136,.9)'; ctx.lineWidth=1;
  ctx.beginPath(); ctx.moveTo(cx-R,cy); ctx.lineTo(cx+R,cy); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(cx,cy-R); ctx.lineTo(cx,cy+R); ctx.stroke();
  ctx.beginPath(); ctx.arc(cx,cy,3,0,Math.PI*2);
  ctx.fillStyle='#ff2244'; ctx.fill();

  ctx.restore();
}

// Draw scene without scope overlay (used inside scope zoom)
function drawScene_noScope(){
  if(!G) return;
  const sky = ctx.createLinearGradient(0,0,0,G.groundY);
  sky.addColorStop(0,'#060a14'); sky.addColorStop(1,'#0a1828');
  ctx.fillStyle=sky; ctx.fillRect(0,0,GW,GH);
  const grd = ctx.createLinearGradient(0,G.groundY,0,GH);
  grd.addColorStop(0,'#1a1200'); grd.addColorStop(1,'#0a0800');
  ctx.fillStyle=grd; ctx.fillRect(0,G.groundY,GW,GH-G.groundY);
  drawBase(G.allyBaseX, G.groundY, '#2266ff', '🏰', G.allyBaseHp/G.allyBaseMaxHp);
  drawBase(G.enemyBaseX, G.groundY, '#ff4400', '🏯', G.enemyBaseHp/G.enemyBaseMaxHp);
  for(const u of G.units) drawUnit(u,'#2266ff',false);
  for(const e of G.enemies) drawUnit(e,e.col,true);
}

// ═══════════════════════════════════════════════════════
// FX
// ═══════════════════════════════════════════════════════
function spawnParticle(x,y,col){
  for(let i=0;i<6;i++){
    const a=Math.random()*Math.PI*2;
    const spd=60+Math.random()*120;
    if(!G) return;
    G.particles.push({x,y,vx:Math.cos(a)*spd,vy:Math.sin(a)*spd,r:2+Math.random()*3,col,life:0.6+Math.random()*0.4});
  }
}

function flashWarning(){
  const el=document.getElementById('warning-flash');
  el.style.opacity='1'; setTimeout(()=>el.style.opacity='0',120);
}

function addKillFeed(){
  const kf=document.getElementById('killfeed');
  const msgs=['적 제거!','헤드샷!','저격 성공!','킬!'];
  const el=document.createElement('div'); el.className='kf-item';
  el.textContent='🎯 '+msgs[Math.floor(Math.random()*msgs.length)];
  kf.appendChild(el);
  setTimeout(()=>el.remove(),2500);
}

// ═══════════════════════════════════════════════════════
// TOAST
// ═══════════════════════════════════════════════════════
function toast(msg, cls=''){
  const wrap=document.getElementById('toast-wrap');
  const el=document.createElement('div'); el.className='toast-item '+(cls||'');
  el.textContent=msg; wrap.appendChild(el);
  setTimeout(()=>el.remove(),2100);
}

// ═══════════════════════════════════════════════════════
// MAIN LOOP
// ═══════════════════════════════════════════════════════
function loop(ts){
  const dt = Math.min(ts-lastTs, 50); lastTs=ts;
  if(G && !G.over) tick(dt);
  ctx.clearRect(0,0,GW,GH);
  drawScene();
  RAF=requestAnimationFrame(loop);
}

// ═══════════════════════════════════════════════════════
// INPUT
// ═══════════════════════════════════════════════════════
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  mouse.x=e.clientX-r.left; mouse.y=e.clientY-r.top;
});
canvas.addEventListener('mousedown',e=>{
  if(e.button===0) { mouse.down=true; if(G&&!G.over&&!scoped) tryShoot(); }
  if(e.button===2) { scoped=!scoped; e.preventDefault(); }
});
canvas.addEventListener('mouseup',e=>{ if(e.button===0) mouse.down=false; });
canvas.addEventListener('contextmenu',e=>e.preventDefault());
document.addEventListener('keydown',e=>{
  const k=e.key.toLowerCase();
  if(k==='f') scoped=!scoped;
  if(k==='c') toggleCover();
  if(k==='r') startReload();
  if(k===' '||k==='enter'){ if(G&&!G.over) tryShoot(); e.preventDefault(); }
  if(k==='1') summonUnit(0);
  if(k==='2') summonUnit(1);
  if(k==='3') summonUnit(2);
  if(k==='4') summonUnit(3);
  if(k==='5') summonUnit(4);
});

// ═══════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════
// Show difficulty screen immediately
document.getElementById('difficulty-screen').style.display='flex';
document.getElementById('title-screen').style.display='none';
loop(performance.now());
</script>
</body>
</html>"""


def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import (
        load_db, save_db, load_leaderboard, update_leaderboard,
        format_leaderboard_score
    )
    from utils.config import USERS_FILE
    import json

    qp = st.query_params
    GAME_ID = "sniper"

    # ── 결과 처리 ──────────────────────────────────────────
    if qp.get('sniper_kills'):
        try:
            uid   = st.session_state.get('logged_in_user', '')
            kills = int(qp.get('sniper_kills', 0))
            won   = qp.get('sniper_won', 'false') == 'true'
            if uid and kills > 0:
                _users = load_db(USERS_FILE, {})
                cur_rec = _users.get(uid, {}).get('game_records',
                          st.session_state.get('game_records', {}))
                changed = False
                prev_best = cur_rec.get('sniper', {}).get('score', 0)
                if kills > prev_best:
                    cur_rec.setdefault('sniper', {}).update({'score': kills})
                    changed = True
                    st.toast(f"🎯 스나이퍼 최고킬 갱신! {kills:,}킬", icon="🎯")
                if changed:
                    st.session_state.game_records = cur_rec
                    if uid in _users:
                        _users[uid]['game_records'] = cur_rec
                        save_db(USERS_FILE, _users)
                    sync_user_data()
                # 전역 리더보드 갱신
                user_name = _users.get(uid, {}).get('nickname', uid) if uid else uid
                if update_leaderboard(GAME_ID, user_name, kills):
                    st.session_state['sniper_lb_new'] = True
                    st.toast(f"👑 전국 1위! 라인 배틀 {kills:,}킬", icon="🏆")
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    # ── 전역 리더보드 표시 ──────────────────────────────────
    lb = load_leaderboard()
    rec = lb.get(GAME_ID, {})
    if rec:
        score_fmt = format_leaderboard_score(GAME_ID, rec.get('top_score', 0))
        st.markdown(f"""
        <div style='background:linear-gradient(90deg,rgba(245,197,24,.12),rgba(0,0,0,0));
          border:1px solid rgba(245,197,24,.35);border-radius:10px;padding:8px 18px;
          margin-bottom:10px;font-family:"Orbitron",sans-serif;font-size:.82rem;'>
          👑 전국 1위: <b style="color:#f5c518;">{rec.get('top_user','?')}</b>
          &nbsp;|&nbsp; <span style="color:#00d4ff;">{score_fmt}</span>
          &nbsp;|&nbsp; <span style="color:#556;">{rec.get('date','')}</span>
        </div>
        """, unsafe_allow_html=True)

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
        url.searchParams.set('sniper_kills', e.data.kills);
        url.searchParams.set('sniper_won',   e.data.won ? 'true' : 'false');
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=900, scrolling=False)
