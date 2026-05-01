import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
html,body{width:100%;height:100%;overflow:hidden;background:#000;touch-action:none;font-family:'Rajdhani',sans-serif;}
#wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden;}
#gameCanvas{display:block;touch-action:none;image-rendering:pixelated;}
#ui{position:absolute;top:0;left:0;pointer-events:none;}

/* HUD */
#hud{position:absolute;top:0;left:0;right:0;padding:10px 12px;display:flex;justify-content:space-between;align-items:flex-start;gap:6px;}
.hud-panel{background:rgba(0,0,0,0.75);border:1px solid rgba(0,255,180,0.2);border-radius:8px;padding:5px 10px;text-align:center;backdrop-filter:blur(4px);}
.hud-val{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:900;color:#fff;line-height:1.1;letter-spacing:1px;}
.hud-lbl{font-size:7px;color:rgba(0,255,180,0.5);letter-spacing:3px;margin-top:1px;font-family:'Share Tech Mono',monospace;}
#score-val{color:#00ffb4;}
#wave-val{color:#ff9500;}
#dist-val{color:#88ddff;}

/* Wanted stars */
#wanted-panel{display:flex;flex-direction:column;align-items:center;gap:4px;}
#stars{display:flex;gap:2px;}
.star{font-size:13px;opacity:0.15;transition:all 0.3s;filter:none;}
.star.on{opacity:1;filter:drop-shadow(0 0 8px gold) drop-shadow(0 0 16px rgba(255,200,0,0.5));}

/* Lives */
#lives-row{display:flex;gap:4px;margin-top:2px;}
.life-pip{width:8px;height:8px;border-radius:50%;background:#ff3366;box-shadow:0 0 8px rgba(255,51,102,0.9);transition:all 0.3s;}
.life-pip.dead{background:#1a0008;box-shadow:none;}

/* Speedometer */
#speedo-wrap{position:absolute;bottom:108px;right:12px;width:70px;height:70px;}
#speedo-canvas{width:70px;height:70px;}

/* Nitro bar */
#nitro-wrap{position:absolute;bottom:108px;left:12px;display:flex;flex-direction:column;align-items:flex-start;gap:3px;}
#nitro-lbl{font-size:7px;color:rgba(0,255,180,0.6);letter-spacing:3px;font-family:'Share Tech Mono',monospace;}
#nitro-track{width:90px;height:10px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;border:1px solid rgba(0,255,180,0.15);position:relative;}
#nitro-fill{height:100%;background:linear-gradient(90deg,#007755,#00ffb4,#aaffee);border-radius:99px;transition:width 0.05s linear;position:relative;}
#nitro-fill::after{content:'';position:absolute;top:0;right:0;width:4px;height:100%;background:rgba(255,255,255,0.8);border-radius:99px;filter:blur(2px);}

/* Minimap */
#minimap-wrap{position:absolute;bottom:108px;left:108px;}
#minimap{background:rgba(0,0,0,0.6);border:1px solid rgba(0,255,180,0.15);border-radius:4px;}

/* Combo */
#combo-hud{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:42px;font-weight:900;color:#ff9500;text-shadow:0 0 30px #ff9500, 0 0 60px rgba(255,149,0,0.4);opacity:0;transition:opacity 0.2s;pointer-events:none;text-align:center;white-space:nowrap;}

/* Announce banner */
#announce{position:absolute;top:35%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:clamp(14px,3.5vw,24px);font-weight:900;letter-spacing:4px;opacity:0;pointer-events:none;text-align:center;white-space:nowrap;text-transform:uppercase;}

/* Heat meter */
#heat-wrap{position:absolute;top:64px;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:2px;}
#heat-lbl{font-size:7px;color:rgba(255,100,50,0.6);letter-spacing:3px;font-family:'Share Tech Mono',monospace;}
#heat-track{width:120px;height:6px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;border:1px solid rgba(255,100,50,0.2);}
#heat-fill{height:100%;background:linear-gradient(90deg,#ff6600,#ff3300,#ff0044);border-radius:99px;width:0%;transition:width 0.1s;}

/* Controls */
#controls{position:absolute;bottom:0;left:0;right:0;height:100px;display:flex;justify-content:space-between;align-items:center;padding:0 14px 10px;pointer-events:all;}
#dpad{display:flex;gap:10px;}
.ctrl-btn{border-radius:14px;background:rgba(255,255,255,0.06);border:1.5px solid rgba(255,255,255,0.12);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;user-select:none;-webkit-user-select:none;touch-action:none;transition:all 0.1s;color:rgba(255,255,255,0.7);}
#btn-left,#btn-right{width:68px;height:58px;font-size:22px;}
.ctrl-btn:active,.ctrl-btn.pressed{background:rgba(0,255,180,0.15);border-color:rgba(0,255,180,0.5);box-shadow:0 0 20px rgba(0,255,180,0.3);transform:scale(0.92);}
#nitro-btn{width:84px;height:84px;border-radius:50%;background:rgba(0,255,180,0.08);border:2px solid rgba(0,255,180,0.35);font-size:26px;color:#00ffb4;box-shadow:inset 0 0 20px rgba(0,255,180,0.05);}
#nitro-btn.pressed{background:rgba(0,255,180,0.25);box-shadow:0 0 30px rgba(0,255,180,0.5),inset 0 0 20px rgba(0,255,180,0.1);}
.ctrl-lbl{font-size:7px;letter-spacing:2px;margin-top:3px;color:rgba(0,255,180,0.7);font-family:'Share Tech Mono',monospace;}

/* Swipe zone overlay */
#swipe-zone{position:absolute;top:0;left:0;right:0;bottom:100px;pointer-events:all;z-index:50;}

/* Main overlay */
#overlay{position:absolute;inset:0;background:rgba(0,0,5,0.94);display:flex;align-items:center;justify-content:center;pointer-events:all;z-index:200;}
#overlay-inner{text-align:center;max-width:400px;width:94vw;padding:28px 20px 24px;border:1px solid rgba(0,255,180,0.15);border-radius:20px;background:rgba(1,5,15,0.98);position:relative;overflow:hidden;}
#overlay-inner::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(ellipse at center,rgba(0,255,180,0.03) 0%,transparent 60%);pointer-events:none;}
.ov-badge{font-size:7px;letter-spacing:5px;color:#00ffb4;background:rgba(0,255,180,0.08);border:1px solid rgba(0,255,180,0.2);border-radius:99px;padding:4px 18px;display:inline-block;margin-bottom:18px;font-family:'Share Tech Mono',monospace;}
.ov-title{font-family:'Orbitron',sans-serif;font-size:clamp(24px,6vw,38px);font-weight:900;margin-bottom:4px;line-height:1.1;}
.ov-sub{font-size:8px;color:rgba(255,255,255,0.25);letter-spacing:4px;margin-bottom:22px;font-family:'Share Tech Mono',monospace;}

/* Car selection */
.car-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:18px;}
.car-card{padding:10px 4px;background:rgba(255,255,255,0.03);border:1.5px solid rgba(255,255,255,0.07);border-radius:12px;cursor:pointer;transition:all 0.2s;text-align:center;position:relative;overflow:hidden;}
.car-card.sel{border-color:#00ffb4;background:rgba(0,255,180,0.08);box-shadow:0 0 20px rgba(0,255,180,0.15);}
.car-card:hover{border-color:rgba(0,255,180,0.4);}
.car-emoji{font-size:28px;display:block;margin-bottom:4px;}
.car-name{font-size:8px;font-weight:700;letter-spacing:1px;font-family:'Share Tech Mono',monospace;}
.car-type{font-size:6px;color:rgba(255,255,255,0.3);margin-top:2px;letter-spacing:1px;}
.car-bars{margin-top:6px;display:flex;flex-direction:column;gap:2px;}
.car-bar-row{display:flex;align-items:center;gap:3px;}
.car-bar-label{font-size:5px;color:rgba(255,255,255,0.3);width:16px;text-align:right;font-family:'Share Tech Mono',monospace;}
.car-bar-track{flex:1;height:3px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;}
.car-bar-fill{height:100%;border-radius:99px;transition:width 0.3s;}

/* Stats row */
.stats-row{display:flex;gap:8px;justify-content:center;margin-bottom:18px;}
.stat-box{padding:8px 14px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);border-radius:10px;text-align:center;min-width:70px;}
.stat-num{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:700;color:#fff;line-height:1;}
.stat-lbl{font-size:7px;color:rgba(255,255,255,0.25);letter-spacing:2px;margin-top:3px;font-family:'Share Tech Mono',monospace;}

/* Instructions */
.inst-row{font-size:9px;color:rgba(255,255,255,0.2);line-height:2.4;margin-bottom:16px;font-family:'Share Tech Mono',monospace;}

/* Best score */
.best-row{font-size:9px;color:rgba(255,255,255,0.25);margin-bottom:16px;font-family:'Share Tech Mono',monospace;}
.best-num{color:#ff9500;font-family:'Orbitron',sans-serif;}

/* Buttons */
.action-btn{display:inline-block;padding:13px 36px;background:rgba(0,255,180,0.1);border:1px solid rgba(0,255,180,0.45);border-radius:12px;font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;color:#00ffb4;cursor:pointer;letter-spacing:2px;transition:all 0.2s;position:relative;overflow:hidden;}
.action-btn::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,255,180,0.1),transparent);opacity:0;transition:opacity 0.2s;}
.action-btn:hover{background:rgba(0,255,180,0.2);transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,255,180,0.25);}
.action-btn:hover::before{opacity:1;}
.sec-btn{display:inline-block;margin-top:10px;padding:9px 22px;border:1px solid rgba(255,255,255,0.1);border-radius:10px;font-size:11px;color:rgba(255,255,255,0.3);cursor:pointer;transition:all 0.2s;font-family:'Share Tech Mono',monospace;letter-spacing:1px;}
.sec-btn:hover{border-color:rgba(255,255,255,0.25);color:rgba(255,255,255,0.5);}

/* Weather/environment indicator */
#env-badge{position:absolute;top:64px;right:12px;font-size:7px;color:rgba(255,255,255,0.3);font-family:'Share Tech Mono',monospace;letter-spacing:2px;background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.08);border-radius:6px;padding:3px 8px;}

/* Damage flash */
#dmg-overlay{position:absolute;inset:0;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,transparent 40%,rgba(255,0,50,0.4) 100%);transition:opacity 0.1s;}
/* Nitro vignette */
#nitro-vignette{position:absolute;inset:0;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,transparent 30%,rgba(0,255,180,0.15) 100%);transition:opacity 0.15s;}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="gameCanvas"></canvas>
  <div id="ui" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;">

    <div id="dmg-overlay"></div>
    <div id="nitro-vignette"></div>

    <!-- HUD -->
    <div id="hud">
      <div class="hud-panel">
        <div class="hud-val" id="score-val">0</div>
        <div class="hud-lbl">SCORE</div>
      </div>
      <div class="hud-panel">
        <div class="hud-val" id="wave-val">1</div>
        <div class="hud-lbl">WAVE</div>
      </div>
      <div class="hud-panel" id="wanted-panel">
        <div id="stars">
          <span class="star" id="s0">★</span>
          <span class="star" id="s1">★</span>
          <span class="star" id="s2">★</span>
          <span class="star" id="s3">★</span>
          <span class="star" id="s4">★</span>
        </div>
        <div id="lives-row"></div>
        <div class="hud-lbl">WANTED</div>
      </div>
      <div class="hud-panel">
        <div class="hud-val" id="dist-val">0.00</div>
        <div class="hud-lbl">KM</div>
      </div>
    </div>

    <!-- Heat meter -->
    <div id="heat-wrap">
      <div id="heat-lbl">HEAT</div>
      <div id="heat-track"><div id="heat-fill"></div></div>
    </div>

    <!-- Env badge -->
    <div id="env-badge">🌆 CITY NIGHT</div>

    <!-- Nitro -->
    <div id="nitro-wrap">
      <div id="nitro-lbl">NITRO</div>
      <div id="nitro-track"><div id="nitro-fill"></div></div>
    </div>

    <!-- Speedo -->
    <div id="speedo-wrap"><canvas id="speedo-canvas" width="70" height="70"></canvas></div>

    <!-- Minimap -->
    <div id="minimap-wrap"><canvas id="minimap" width="70" height="40"></canvas></div>

    <!-- Combo -->
    <div id="combo-hud"></div>
    <!-- Announce -->
    <div id="announce"></div>

    <!-- Controls -->
    <div id="controls" style="pointer-events:all;">
      <div id="dpad">
        <div class="ctrl-btn" id="btn-left">◀<span class="ctrl-lbl">LEFT</span></div>
        <div class="ctrl-btn" id="btn-right">▶<span class="ctrl-lbl">RIGHT</span></div>
      </div>
      <div class="ctrl-btn" id="nitro-btn">⚡<span class="ctrl-lbl">NITRO</span></div>
    </div>

    <!-- Swipe zone -->
    <div id="swipe-zone"></div>

    <!-- Main overlay -->
    <div id="overlay" style="pointer-events:all;"><div id="overlay-inner"></div></div>
  </div>
</div>

<script>
'use strict';

// ─── CANVAS SETUP ───────────────────────────────────────────────────
const canvas  = document.getElementById('gameCanvas');
const ctx     = canvas.getContext('2d');
const speedoC = document.getElementById('speedo-canvas');
const speedoX = speedoC.getContext('2d');
const mapC    = document.getElementById('minimap');
const mapX    = mapC.getContext('2d');
const wrap    = document.getElementById('wrap');
const uiEl    = document.getElementById('ui');

const BASE_W = 420, BASE_H = 740;
let W = BASE_W, H = BASE_H, UIScale = 1;

function resize() {
  const rw = window.innerWidth, rh = window.innerHeight;
  const sc = Math.min(rw / BASE_W, rh / BASE_H);
  canvas.width = W; canvas.height = H;
  const pw = BASE_W * sc, ph = BASE_H * sc;
  ['position:absolute',
   `left:${(rw-pw)/2}px`, `top:${(rh-ph)/2}px`,
   `width:${pw}px`, `height:${ph}px`]
   .join(';');
  canvas.style.cssText = `position:absolute;left:${(rw-pw)/2}px;top:${(rh-ph)/2}px;width:${pw}px;height:${ph}px;`;
  uiEl.style.cssText   = `position:absolute;left:${(rw-pw)/2}px;top:${(rh-ph)/2}px;width:${pw}px;height:${ph}px;`;
  UIScale = sc;
}
resize();
window.addEventListener('resize', resize);

// ─── CAR DEFINITIONS ───────────────────────────────────────────────
const CARS = [
  {name:'SPORT',   emoji:'🚗', type:'균형형',   spd:1.00, hp:3, acc:1.00, col:'#00ffb4', statSpd:70, statHp:60, statAcc:65},
  {name:'HYPER',   emoji:'🏎️', type:'극한속도', spd:1.40, hp:2, acc:1.20, col:'#ff3355', statSpd:95, statHp:30, statAcc:85},
  {name:'SUV',     emoji:'🚙', type:'탱크형',   spd:0.75, hp:5, acc:0.70, col:'#44ff88', statSpd:45, statHp:90, statAcc:40},
  {name:'MUSCLE',  emoji:'🚘', type:'가속형',   spd:1.12, hp:3, acc:1.50, col:'#ffaa00', statSpd:78, statHp:60, statAcc:95},
];

// ─── TRAFFIC ───────────────────────────────────────────────────────
const TRAFFIC_DEFS = [
  {emoji:'🚌', spd:2.0, pts:25,  cop:false, size:1.2},
  {emoji:'🚛', spd:1.6, pts:35,  cop:false, size:1.3},
  {emoji:'🚓', spd:5.2, pts:15,  cop:true,  size:1.0},
  {emoji:'🏍️', spd:4.8, pts:15,  cop:false, size:0.7},
  {emoji:'🚑', spd:2.6, pts:28,  cop:false, size:1.1},
  {emoji:'🚜', spd:1.2, pts:40,  cop:false, size:1.2},
  {emoji:'🚐', spd:2.3, pts:20,  cop:false, size:1.1},
  {emoji:'🚕', spd:3.2, pts:18,  cop:false, size:1.0},
  {emoji:'🏎️', spd:5.5, pts:12,  cop:false, size:0.9},
  {emoji:'🛻', spd:2.8, pts:22,  cop:false, size:1.1},
];

// ─── POWER-UPS ─────────────────────────────────────────────────────
const PWR_DEFS = [
  {emoji:'⚡', type:'nitro',  col:'#00ffb4', label:'NITRO +80%',     rarity:0.25},
  {emoji:'⭐', type:'score',  col:'#ffaa00', label:'+1000 BONUS!',   rarity:0.15},
  {emoji:'💊', type:'heal',   col:'#44ff88', label:'HP RESTORED',    rarity:0.20},
  {emoji:'🔱', type:'shield', col:'#cc44ff', label:'SHIELD 6 SEC',   rarity:0.12},
  {emoji:'💨', type:'boost',  col:'#88eeFF', label:'SPEED BOOST!',   rarity:0.15},
  {emoji:'🧲', type:'magnet', col:'#ff8844', label:'MAGNET ON!',     rarity:0.08},
  {emoji:'💣', type:'bomb',   col:'#ff4422', label:'ROAD CLEAR!',    rarity:0.05},
];

// ─── ENVIRONMENTS ──────────────────────────────────────────────────
const ENVS = [
  {name:'🌆 CITY NIGHT',   sky1:'#010208', sky2:'#040c1e', glow:'#cc44ff', road:'#060d1c', stripe:'rgba(192,79,255,0.6)'},
  {name:'🌅 SUNSET BLVD',  sky1:'#1a0608', sky2:'#3a1520', glow:'#ff6622', road:'#0d0808', stripe:'rgba(255,100,50,0.7)'},
  {name:'🌊 NEON COAST',   sky1:'#010d1a', sky2:'#021228', glow:'#00ffb4', road:'#050e18', stripe:'rgba(0,255,180,0.6)'},
  {name:'❄️ ICE HIGHWAY',  sky1:'#080e18', sky2:'#0a1520', glow:'#88ddff', road:'#0a0f18', stripe:'rgba(136,221,255,0.7)'},
];

// ─── LAYOUT ────────────────────────────────────────────────────────
const LANES       = 5;
const LANE_FRAC   = [0.13, 0.295, 0.46, 0.625, 0.79];
const ROAD_L      = 0.07 * BASE_W;
const ROAD_R      = 0.93 * BASE_W;
const ROAD_W      = ROAD_R - ROAD_L;
const HORIZON_Y   = BASE_H * 0.42;
const VANISH_X    = BASE_W / 2;

function laneX(laneF, depth) {
  const cx = ROAD_L + laneF * ROAD_W;
  return VANISH_X + (cx - VANISH_X) * depth;
}
function screenY(depth) { return HORIZON_Y + (BASE_H - HORIZON_Y) * depth; }
function roadW(depth)   { return ROAD_W * depth; }

// ─── INPUT ─────────────────────────────────────────────────────────
const KEYS = {};
window.addEventListener('keydown', e => {
  KEYS[e.code] = true;
  if (['ArrowLeft','ArrowRight','Space','KeyA','KeyD'].includes(e.code)) e.preventDefault();
});
window.addEventListener('keyup', e => { KEYS[e.code] = false; });

// ─── SWIPE INPUT ───────────────────────────────────────────────────
let swipeStartX = null;
const swipeZone = document.getElementById('swipe-zone');
swipeZone.addEventListener('touchstart', e => {
  swipeStartX = e.touches[0].clientX;
}, {passive:true});
swipeZone.addEventListener('touchend', e => {
  if (swipeStartX === null) return;
  const dx = e.changedTouches[0].clientX - swipeStartX;
  if (Math.abs(dx) > 30) {
    if (dx < 0) G._swipeLeft = true;
    else         G._swipeRight = true;
  }
  swipeStartX = null;
}, {passive:true});

// ─── STATE ─────────────────────────────────────────────────────────
let selCar = 0;
let G = {}, raf = null, floats = [], particles = [];
let lastLeft = false, lastRight = false, uid = 0;
let envIdx = 0;

function playerX() {
  if (G.laneT >= 1) return LANE_FRAC[G.lane] * BASE_W;
  const ease = G.laneT < 0.5 ? 2*G.laneT*G.laneT : -1+(4-2*G.laneT)*G.laneT;
  const a = LANE_FRAC[G.laneFrom] * BASE_W;
  const b = LANE_FRAC[G.laneTarget] * BASE_W;
  return a + (b - a) * ease;
}

function initGame() {
  const car = CARS[selCar];
  envIdx = Math.floor(Math.random() * ENVS.length);
  document.getElementById('env-badge').textContent = ENVS[envIdx].name;

  G = {
    running:true, dead:false, frame:0,
    score:0, dist:0,
    lane:2, laneT:1, laneFrom:2, laneTarget:2,
    speed:0, baseSpd: 3.0*car.spd, maxSpd: 8.5*car.spd,
    nitro:100, nitroOn:false,
    hp: car.hp, maxHp: car.hp,
    shieldT:0, boostT:0, flashT:0, magnetT:0,
    combo:1, comboD:0, maxCombo:1,
    heat:0, heatD:0,
    wanted:0, wantedCool:0,
    traffic:[], powers:[],
    spawnD:0, pwrD:0,
    scroll:0, bgShift:0,
    wave:1, waveKills:0, waveTarget:7,
    totalKills:0,
    stars: Array.from({length:100}, () => ({
      x:Math.random()*BASE_W, y:Math.random()*HORIZON_Y,
      r:Math.random()*1.5+0.2, t:Math.random()*Math.PI*2, spd:Math.random()*0.008+0.004
    })),
    buildings: Array.from({length:20}, (_,i) => ({
      x: i * (BASE_W/18) - 10,
      w: 20+Math.random()*18,
      h: 40+Math.random()*60,
      lit: Array.from({length:8}, () => Math.random() > 0.5),
    })),
    _annTimer:null,
    _tLeft:false, _tRight:false, _tNitro:false,
    _swipeLeft:false, _swipeRight:false,
    roadCracks: Array.from({length:15}, () => ({
      lane: Math.floor(Math.random()*LANES),
      d: Math.random(),
      alpha: 0.05+Math.random()*0.1
    })),
  };
  floats = []; particles = [];
  buildLives(); updateWanted();

  for (let i = 0; i < 6; i++) spawnTraffic(true);
  spawnPwr();
}

// ─── SPAWN ─────────────────────────────────────────────────────────
function spawnTraffic(far) {
  const pool = TRAFFIC_DEFS.filter(d => !d.cop || G.wanted >= 2);
  const def  = pool[Math.floor(Math.random() * pool.length)];
  G.traffic.push({
    id: uid++,
    lane: Math.floor(Math.random() * LANES),
    depth: far ? Math.random()*0.20+0.01 : 0.01+Math.random()*0.05,
    spd: def.spd * (0.85+Math.random()*0.3),
    emoji: def.emoji, pts: def.pts, cop: def.cop, size: def.size,
    alive: true, scored: false, siren: 0,
    wobble: 0, wobbleD: (Math.random()-0.5)*0.004,
  });
}

function spawnPwr() {
  const r = Math.random();
  let acc = 0, def = PWR_DEFS[0];
  for (const p of PWR_DEFS) { acc += p.rarity; if (r <= acc) { def = p; break; } }
  G.powers.push({
    lane: Math.floor(Math.random()*LANES), depth:0.01,
    type: def.type, emoji: def.emoji, col: def.col, label: def.label,
    alive: true, rot: 0, pulse: 0,
  });
}

function spawnFloat(txt, col, x) {
  floats.push({txt, col, x: x || BASE_W/2, y: BASE_H*0.50, vy:-2.5, life:1.0, scale:1});
}

function spawnParticles(x, y, col, count) {
  for (let i = 0; i < count; i++) {
    const a = Math.random() * Math.PI * 2;
    const spd = 1 + Math.random() * 4;
    particles.push({x, y, vx: Math.cos(a)*spd, vy: Math.sin(a)*spd - 2,
      col, life: 0.8+Math.random()*0.6, size: 2+Math.random()*4});
  }
}

// ─── UI HELPERS ────────────────────────────────────────────────────
function buildLives() {
  const r = document.getElementById('lives-row');
  r.innerHTML = '';
  for (let i = 0; i < G.maxHp; i++) {
    const d = document.createElement('div');
    d.className = 'life-pip' + (i >= G.hp ? ' dead' : '');
    d.id = 'lp' + i;
    r.appendChild(d);
  }
}
function updateLives() {
  for (let i = 0; i < G.maxHp; i++) {
    const el = document.getElementById('lp'+i);
    if (el) el.className = 'life-pip' + (i >= G.hp ? ' dead' : '');
  }
}
function updateWanted() {
  for (let i = 0; i < 5; i++) {
    const el = document.getElementById('s'+i);
    if (el) el.classList.toggle('on', i < G.wanted);
  }
}

let annTimer = null;
function announce(txt, col) {
  const el = document.getElementById('announce');
  if (!el) return;
  el.textContent = txt; el.style.color = col;
  el.style.textShadow = `0 0 20px ${col}, 0 0 40px ${col}44`;
  el.style.opacity = '1';
  clearTimeout(annTimer);
  annTimer = setTimeout(() => { if(el) el.style.opacity='0'; }, 1600);
}

// ─── SPEEDO ────────────────────────────────────────────────────────
function drawSpeedo(speed, maxSpd) {
  const c = speedoX, R = 32, cx = 35, cy = 38;
  c.clearRect(0, 0, 70, 70);
  const pct = Math.min(1, speed / maxSpd);

  // Track
  c.beginPath(); c.arc(cx, cy, R, Math.PI*0.75, Math.PI*2.25);
  c.strokeStyle = 'rgba(255,255,255,0.08)'; c.lineWidth = 5; c.stroke();

  // Fill
  const grad = c.createLinearGradient(cx-R, cy, cx+R, cy);
  grad.addColorStop(0, '#00ffb4'); grad.addColorStop(0.6, '#ffaa00'); grad.addColorStop(1, '#ff3355');
  c.beginPath(); c.arc(cx, cy, R, Math.PI*0.75, Math.PI*0.75 + Math.PI*1.5*pct);
  c.strokeStyle = grad; c.lineWidth = 5; c.lineCap = 'round'; c.stroke();

  // Needle
  const angle = Math.PI*0.75 + Math.PI*1.5*pct;
  c.save(); c.translate(cx, cy);
  c.strokeStyle = '#fff'; c.lineWidth = 2; c.shadowColor = '#fff'; c.shadowBlur = 6;
  c.beginPath(); c.moveTo(0,0); c.lineTo(Math.cos(angle)*22, Math.sin(angle)*22); c.stroke();
  c.restore();

  // KM label
  const kmh = Math.round(speed * 28);
  c.fillStyle = 'rgba(255,255,255,0.6)';
  c.font = "bold 8px 'Share Tech Mono'";
  c.textAlign = 'center'; c.textBaseline = 'top';
  c.fillText(kmh+'km', cx, cy+4);

  c.fillStyle = 'rgba(255,255,255,0.2)';
  c.font = "5px 'Share Tech Mono'";
  c.fillText('SPD', cx, cy-16);
}

// ─── MINIMAP ───────────────────────────────────────────────────────
function drawMinimap() {
  const c = mapX, mW = 70, mH = 40;
  c.clearRect(0, 0, mW, mH);
  c.fillStyle = 'rgba(0,0,0,0.6)'; c.fillRect(0, 0, mW, mH);
  // Road
  c.fillStyle = 'rgba(255,255,255,0.05)';
  c.fillRect(8, 0, mW-16, mH);
  // Traffic blips
  for (const tc of G.traffic) {
    if (!tc.alive) continue;
    const mx = 8 + (tc.lane / (LANES-1)) * (mW-16);
    const my = mH * (1 - tc.depth);
    c.fillStyle = tc.cop ? '#ff3355' : 'rgba(255,255,255,0.4)';
    c.fillRect(mx-2, my-2, 4, 4);
  }
  // Player
  const px = 8 + (G.lane / (LANES-1)) * (mW-16);
  c.fillStyle = '#00ffb4'; c.shadowColor = '#00ffb4'; c.shadowBlur = 6;
  c.fillRect(px-3, mH-8, 6, 6);
  c.shadowBlur = 0;
}

// ─── UPDATE ────────────────────────────────────────────────────────
function update() {
  if (!G.running || G.dead) return;
  G.frame++;

  const left  = KEYS['ArrowLeft']  || KEYS['KeyA'] || G._tLeft  || G._swipeLeft;
  const right = KEYS['ArrowRight'] || KEYS['KeyD'] || G._tRight || G._swipeRight;
  const nitro = KEYS['Space'] || KEYS['ShiftLeft'] || KEYS['ShiftRight'] || G._tNitro;

  G._swipeLeft = false; G._swipeRight = false;

  // Lane change
  if (left && !lastLeft && G.laneT >= 1) {
    if (G.lane > 0) {
      G.laneFrom = G.lane; G.laneTarget = G.lane-1; G.laneT = 0; G.lane--;
    } else announce('BARRIER!', '#ff3355');
  }
  if (right && !lastRight && G.laneT >= 1) {
    if (G.lane < LANES-1) {
      G.laneFrom = G.lane; G.laneTarget = G.lane+1; G.laneT = 0; G.lane++;
    } else announce('BARRIER!', '#ff3355');
  }
  lastLeft = left; lastRight = right;

  const car = CARS[selCar];
  const laneSpd = 0.14 + car.acc * 0.06;
  if (G.laneT < 1) G.laneT = Math.min(1, G.laneT + laneSpd);

  // Nitro
  if (nitro && G.nitro > 0) {
    G.nitroOn = true;
    G.nitro = Math.max(0, G.nitro - 0.65);
  } else {
    G.nitroOn = false;
    G.nitro = Math.min(100, G.nitro + 0.28);
  }

  // Speed
  const nitroM = G.nitroOn ? 2.1 : (G.boostT > 0 ? 1.5 : 1);
  const targetSpd = G.baseSpd * nitroM;
  G.speed += (targetSpd - G.speed) * (0.035 + car.acc * 0.012);

  // Timers
  if (G.shieldT > 0) G.shieldT -= 1/60;
  if (G.boostT  > 0) G.boostT  -= 1/60;
  if (G.magnetT > 0) G.magnetT -= 1/60;
  if (G.flashT  > 0) G.flashT  -= 0.07;
  if (G.comboD  > 0) G.comboD--;
  else if (G.combo > 1) { G.combo = Math.max(1, G.combo-1); G.comboD = 100; }

  // Wanted cooldown
  if (G.wantedCool > 0) G.wantedCool--;
  else if (G.wanted > 0 && G.frame % 400 === 0) { G.wanted = Math.max(0, G.wanted-1); updateWanted(); }

  // Heat (high wanted → heat builds up, makes cops faster)
  if (G.wanted >= 3) G.heat = Math.min(100, G.heat + 0.08 * G.wanted);
  else G.heat = Math.max(0, G.heat - 0.05);

  // Scroll
  G.scroll  += G.speed * 0.014;
  G.bgShift  = (G.bgShift + G.speed * 0.0007) % 1;
  G.dist    += G.speed * 0.00026;

  // Spawn traffic
  G.spawnD -= G.speed;
  if (G.spawnD <= 0) {
    spawnTraffic(false);
    if (G.wanted >= 3) spawnTraffic(false);
    if (G.wave >= 5)   spawnTraffic(false);
    G.spawnD = Math.max(50, 300 - G.speed*14 - G.wave*10 + Math.random()*80);
  }

  // Update traffic
  const heatBonus = 1 + G.heat * 0.004;
  for (const tc of G.traffic) {
    if (!tc.alive) continue;
    tc.wobble += tc.wobbleD;
    if (Math.abs(tc.wobble) > 0.08) tc.wobbleD *= -1;
    const copSpd = tc.cop ? (0.88 + G.wanted*0.07) * heatBonus : 0.85;
    tc.depth += (G.speed - tc.spd * copSpd) * 0.00023;
    if (tc.cop) tc.siren = (tc.siren + 1) % 60;

    // Magnet: pull powers toward player
    if (G.magnetT > 0) {
      const pxPos = playerX();
      for (const pw of G.powers) {
        if (!pw.alive) continue;
        const pwX = laneX(LANE_FRAC[pw.lane], pw.depth);
        if (Math.abs(pwX - pxPos) < 120) {
          const dir = pxPos > pwX ? 1 : -1;
          pw.lane = Math.max(0, Math.min(LANES-1, pw.lane + dir * 0.04));
        }
      }
    }

    // Collision zone: depth 0.70..1.08
    if (tc.depth >= 0.70 && tc.depth <= 1.08) {
      const pLane = G.laneT >= 0.5 ? G.laneTarget : G.laneFrom;
      if (Math.abs(pLane - tc.lane) < 0.55) {
        if (G.shieldT > 0) {
          tc.alive = false;
          spawnParticles(playerX(), H-100, '#cc44ff', 20);
          spawnFloat('BLOCKED!', '#cc44ff');
          G.score += 150;
        } else {
          G.hp--; G.flashT = 1.2;
          G.speed = Math.max(G.baseSpd*0.25, G.speed*0.35);
          G.combo = 1; G.comboD = 0;
          tc.alive = false;
          spawnParticles(playerX(), H-100, '#ff3355', 30);
          updateLives();
          announce('CRASH! 💥', '#ff3355');
          document.getElementById('dmg-overlay').style.opacity = '1';
          setTimeout(() => { document.getElementById('dmg-overlay').style.opacity='0'; }, 350);
          if (G.hp <= 0) { G.dead = true; setTimeout(showGameOver, 900); }
        }
        continue;
      }
    }

    // Passed
    if (!tc.scored && tc.depth > 1.08) {
      tc.scored = true;
      const pts = tc.pts * G.combo;
      G.score += pts;
      G.combo = Math.min(12, G.combo+1);
      G.maxCombo = Math.max(G.maxCombo, G.combo);
      G.comboD = 130;
      G.waveKills++;
      G.totalKills++;
      spawnFloat('+'+pts, G.combo >= 4 ? '#ffaa00' : '#00ffb4',
        laneX(LANE_FRAC[tc.lane], 1.0));
      if (tc.cop) {
        G.wanted = Math.min(5, G.wanted+1);
        G.wantedCool = 700;
        updateWanted();
      }
      if (G.combo >= 4) {
        const comboEl = document.getElementById('combo-hud');
        comboEl.textContent = '×'+G.combo+' COMBO!';
        comboEl.style.opacity = '1';
        comboEl.style.fontSize = Math.min(42, 28 + G.combo*2)+'px';
        setTimeout(() => { comboEl.style.opacity='0'; }, 900);
        announce('×'+G.combo+' COMBO!', '#ffaa00');
      }
      if (G.waveKills >= G.waveTarget) {
        G.wave++; G.waveKills = 0;
        G.waveTarget = Math.min(18, G.waveTarget + 2);
        G.baseSpd = Math.min(G.maxSpd, G.baseSpd * 1.08);
        envIdx = (envIdx + 1) % ENVS.length;
        document.getElementById('env-badge').textContent = ENVS[envIdx].name;
        announce('WAVE '+G.wave+'! 🔥', '#ffaa00');
        spawnParticles(BASE_W/2, BASE_H/2, '#ffaa00', 40);
        // Wave bonus
        G.score += G.wave * 500;
        spawnFloat('WAVE '+G.wave+' CLEAR! +'+G.wave*500, '#ffaa00');
      }
    }
    if (tc.depth > 1.35) tc.alive = false;
  }
  G.traffic = G.traffic.filter(t => t.alive);
  if (G.traffic.length > 28) G.traffic.splice(0, 6);

  // Power-up spawn
  G.pwrD -= G.speed;
  if (G.pwrD <= 0) { spawnPwr(); G.pwrD = 280 + Math.random()*280; }

  // Power-up update
  for (const pw of G.powers) {
    if (!pw.alive) continue;
    pw.rot += 0.07; pw.pulse = (pw.pulse + 0.08) % (Math.PI*2);
    pw.depth += G.speed * 0.00023;
    if (pw.depth >= 0.70 && pw.depth <= 1.08) {
      const pLane = G.laneT >= 0.5 ? G.laneTarget : G.laneFrom;
      if (Math.abs(pLane - pw.lane) < 0.60 || G.magnetT > 0 && Math.abs(pLane - pw.lane) < 1.5) {
        pw.alive = false;
        spawnParticles(playerX(), H-100, pw.col, 16);
        spawnFloat(pw.label, pw.col);
        if (pw.type==='nitro')  G.nitro = Math.min(100, G.nitro+80);
        if (pw.type==='score')  { G.score += 1000 * G.combo; }
        if (pw.type==='heal')   { G.hp = Math.min(G.maxHp, G.hp+1); updateLives(); }
        if (pw.type==='shield') G.shieldT = 6;
        if (pw.type==='boost')  G.boostT = 6;
        if (pw.type==='magnet') G.magnetT = 8;
        if (pw.type==='bomb') {
          // Clear all traffic
          const killed = G.traffic.length;
          G.traffic.forEach(t => {
            spawnParticles(laneX(LANE_FRAC[t.lane], t.depth), screenY(t.depth), '#ff4422', 8);
            t.alive = false;
          });
          G.score += killed * 50;
          spawnFloat('ROAD CLEAR! +'+killed*50, '#ff4422');
          announce('💣 KABOOM!', '#ff4422');
        }
      }
    }
    if (pw.depth > 1.35) pw.alive = false;
  }
  G.powers = G.powers.filter(p => p.alive);

  // Passive score
  if (G.frame % 5 === 0) G.score += Math.floor(G.speed * G.combo * 0.18);

  // Update floats
  for (let i = floats.length-1; i >= 0; i--) {
    floats[i].y  += floats[i].vy;
    floats[i].vy *= 0.96;
    floats[i].life -= 0.022;
    if (floats[i].life <= 0) floats.splice(i, 1);
  }

  // Update particles
  for (let i = particles.length-1; i >= 0; i--) {
    const p = particles[i];
    p.x += p.vx; p.y += p.vy; p.vy += 0.12;
    p.life -= 0.03; p.size *= 0.97;
    if (p.life <= 0) particles.splice(i, 1);
  }

  // Update DOM
  const sv = document.getElementById('score-val');
  const wv = document.getElementById('wave-val');
  const dv = document.getElementById('dist-val');
  const nf = document.getElementById('nitro-fill');
  const hf = document.getElementById('heat-fill');
  if (sv) sv.textContent = G.score.toLocaleString();
  if (wv) wv.textContent = G.wave;
  if (dv) dv.textContent = G.dist.toFixed(2);
  if (nf) nf.style.width = G.nitro + '%';
  if (hf) hf.style.width = G.heat + '%';

  // Nitro vignette
  const nv = document.getElementById('nitro-vignette');
  if (nv) nv.style.opacity = G.nitroOn ? '1' : '0';

  drawSpeedo(G.speed, G.maxSpd);
  drawMinimap();
}

// ─── RENDER ────────────────────────────────────────────────────────
function render() {
  ctx.clearRect(0, 0, W, H);
  const env = ENVS[envIdx];

  // ── SKY ──
  const sky = ctx.createLinearGradient(0, 0, 0, HORIZON_Y);
  sky.addColorStop(0, env.sky1);
  sky.addColorStop(1, env.sky2);
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, W, HORIZON_Y);

  // ── STARS ──
  ctx.save();
  for (const s of G.stars) {
    s.t += s.spd;
    ctx.globalAlpha = 0.3 + Math.sin(s.t)*0.4;
    ctx.fillStyle = '#fff';
    ctx.beginPath(); ctx.arc(s.x, s.y, s.r, 0, Math.PI*2); ctx.fill();
  }
  ctx.globalAlpha = 1; ctx.restore();

  // ── CITY BUILDINGS ──
  for (const b of G.buildings) {
    const scrolledX = ((b.x + G.bgShift * 40) % (BASE_W + 40)) - 20;
    ctx.fillStyle = 'rgba(2,5,12,0.95)';
    ctx.fillRect(scrolledX, HORIZON_Y - b.h, b.w, b.h);
    // Windows
    const cols = Math.floor(b.w / 6), rows = Math.floor(b.h / 9);
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        if (b.lit[(row+col)%b.lit.length]) {
          const wx = scrolledX + 2 + col*6, wy = HORIZON_Y - b.h + 4 + row*9;
          ctx.fillStyle = `rgba(${200+Math.random()*55},${180+Math.random()*40},${100+Math.random()*60},0.6)`;
          ctx.fillRect(wx, wy, 3, 5);
        }
      }
    }
  }

  // ── HORIZON GLOW ──
  ctx.save();
  const hg = ctx.createLinearGradient(0, HORIZON_Y-12, 0, HORIZON_Y+12);
  hg.addColorStop(0, 'transparent');
  hg.addColorStop(0.5, env.glow+'55');
  hg.addColorStop(1, 'transparent');
  ctx.fillStyle = hg;
  ctx.fillRect(0, HORIZON_Y-12, W, 24);
  ctx.restore();

  // ── GROUND ──
  const grd = ctx.createLinearGradient(0, HORIZON_Y, 0, H);
  grd.addColorStop(0, env.road);
  grd.addColorStop(1, '#020609');
  ctx.fillStyle = grd;
  ctx.fillRect(0, HORIZON_Y, W, H - HORIZON_Y);

  // ── ROAD SURFACE ──
  const topL = laneX(0, 0), topR = laneX(1, 0);
  ctx.beginPath();
  ctx.moveTo(topL, HORIZON_Y); ctx.lineTo(topR, HORIZON_Y);
  ctx.lineTo(ROAD_R, H); ctx.lineTo(ROAD_L, H);
  ctx.closePath();
  // Road texture gradient
  const roadGrad = ctx.createLinearGradient(ROAD_L, H, ROAD_R, H);
  roadGrad.addColorStop(0, 'rgba(8,14,28,0.9)');
  roadGrad.addColorStop(0.5, 'rgba(12,20,38,0.95)');
  roadGrad.addColorStop(1, 'rgba(8,14,28,0.9)');
  ctx.fillStyle = roadGrad;
  ctx.fill();

  // ── ROAD CRACKS / TEXTURE ──
  for (const crack of G.roadCracks) {
    const d = (crack.d + G.bgShift * 1.2) % 1;
    if (d < 0.1) continue;
    const cx = laneX(LANE_FRAC[crack.lane], d);
    const cy = screenY(d);
    ctx.save();
    ctx.globalAlpha = crack.alpha * d;
    ctx.strokeStyle = 'rgba(100,150,200,0.3)';
    ctx.lineWidth = 0.5;
    ctx.beginPath(); ctx.moveTo(cx-5, cy); ctx.lineTo(cx+3, cy+4); ctx.lineTo(cx+6, cy-2);
    ctx.stroke();
    ctx.restore();
  }

  // ── ROAD BORDERS (glowing) ──
  ctx.save();
  ctx.shadowColor = env.stripe;
  ctx.shadowBlur = 16;
  ctx.strokeStyle = env.stripe;
  ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.moveTo(topL, HORIZON_Y); ctx.lineTo(ROAD_L, H); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(topR, HORIZON_Y); ctx.lineTo(ROAD_R, H); ctx.stroke();
  ctx.restore();

  // ── LANE DIVIDERS ──
  for (let l = 1; l < LANES; l++) {
    for (let d = 0; d < 14; d++) {
      const t1 = ((d + G.scroll*0.32) % 14) / 14;
      const t2 = ((d + G.scroll*0.32) % 14 + 0.42) / 14;
      const y1 = screenY(t1), y2 = screenY(t2);
      if (y2 < HORIZON_Y || y1 > H) continue;
      const frac = LANE_FRAC[l] - (LANE_FRAC[1]-LANE_FRAC[0])*0.5;
      ctx.save();
      ctx.globalAlpha = Math.min(1, t1*2.8) * 0.3;
      ctx.strokeStyle = 'rgba(180,220,255,0.55)';
      ctx.lineWidth = Math.max(0.5, t1*2.2);
      ctx.beginPath();
      ctx.moveTo(laneX(frac, t1), y1);
      ctx.lineTo(laneX(frac, t2), y2);
      ctx.stroke();
      ctx.restore();
    }
  }

  // ── RUMBLE STRIPS ──
  for (let d = 0; d < 12; d++) {
    const t  = (d/12 + G.bgShift) % 1;
    const t2 = ((d+0.5)/12 + G.bgShift) % 1;
    if (t < 0.05) continue;
    const y1 = screenY(t), y2 = screenY(t2);
    if (y2 < HORIZON_Y || y1 > H) continue;
    const col = Math.floor(t*12)%2===0 ? 'rgba(255,40,70,0.65)' : 'rgba(255,255,255,0.4)';
    const lx1 = laneX(0, t), lx2 = laneX(0, t2);
    const rx1 = laneX(1, t), rx2 = laneX(1, t2);
    const rw  = roadW(t) * 0.035;
    ctx.fillStyle = col;
    ctx.beginPath(); ctx.moveTo(lx1-rw,y1); ctx.lineTo(lx1,y1); ctx.lineTo(lx2,y2); ctx.lineTo(lx2-rw,y2); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(rx1,y1); ctx.lineTo(rx1+rw,y1); ctx.lineTo(rx2+rw,y2); ctx.lineTo(rx2,y2); ctx.closePath(); ctx.fill();
  }

  // ── TRAFFIC ──
  const sorted = [...G.traffic].sort((a,b) => a.depth - b.depth);
  for (const tc of sorted) {
    if (!tc.alive) continue;
    const d = tc.depth;
    if (d < 0.01 || d > 1.18) continue;
    const px = laneX(LANE_FRAC[tc.lane] + tc.wobble, d);
    const py = screenY(d);
    const sz = Math.max(10, d * 72 * tc.size);

    ctx.save();
    // Shadow
    ctx.globalAlpha = 0.25 * d;
    ctx.fillStyle = '#000';
    ctx.beginPath(); ctx.ellipse(px, py+sz*0.35, sz*0.4, sz*0.1, 0, 0, Math.PI*2); ctx.fill();
    ctx.globalAlpha = 1;

    // Cop siren
    if (tc.cop && tc.siren > 0) {
      const sirenFlash = Math.floor(tc.siren/10)%2===0;
      ctx.shadowColor  = sirenFlash ? 'rgba(50,80,255,0.9)' : 'rgba(255,30,50,0.9)';
      ctx.shadowBlur   = sz * 1.2;
    }
    ctx.font = sz + 'px serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'bottom';
    ctx.fillText(tc.emoji, px, py);
    ctx.restore();
  }

  // ── POWER-UPS ──
  for (const pw of G.powers) {
    if (!pw.alive) continue;
    const d = pw.depth;
    if (d < 0.01 || d > 1.18) continue;
    const px = laneX(LANE_FRAC[Math.round(pw.lane)], d);
    const py = screenY(d);
    const sz = Math.max(8, d * 60);
    const bob = Math.sin(pw.pulse) * sz * 0.08;

    ctx.save();
    ctx.translate(px, py - sz*0.4 + bob);
    ctx.rotate(pw.rot);
    ctx.shadowColor = pw.col;
    ctx.shadowBlur  = sz * (0.8 + Math.sin(pw.pulse)*0.4);
    ctx.font = sz + 'px serif';
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(pw.emoji, 0, 0);
    ctx.restore();

    // Ring
    ctx.save();
    ctx.globalAlpha = (0.3 + Math.sin(pw.pulse)*0.2) * d;
    ctx.strokeStyle = pw.col;
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(px, py - sz*0.4 + bob, sz*0.65, 0, Math.PI*2);
    ctx.stroke();
    ctx.restore();
  }

  // ── PARTICLES ──
  for (const p of particles) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, p.life);
    ctx.fillStyle   = p.col;
    ctx.shadowColor = p.col; ctx.shadowBlur = 8;
    ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(0.5, p.size), 0, Math.PI*2); ctx.fill();
    ctx.restore();
  }

  // ── PLAYER ──
  const car  = CARS[selCar];
  const pxPos = playerX();
  const pyPos = H - 95;
  const tilt  = G.laneT < 1 ? (G.laneTarget > G.laneFrom ? 1 : -1) * (1-G.laneT) * 14 : 0;

  // Ground shadow
  ctx.save();
  ctx.globalAlpha = 0.25;
  ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.ellipse(pxPos, pyPos+32, 34, 9, 0, 0, Math.PI*2); ctx.fill();
  ctx.restore();

  // Engine glow under car
  const ug = ctx.createRadialGradient(pxPos, pyPos+18, 0, pxPos, pyPos+18, 50);
  ug.addColorStop(0, car.col + (G.nitroOn ? 'cc' : '33'));
  ug.addColorStop(1, 'transparent');
  ctx.fillStyle = ug;
  ctx.beginPath(); ctx.ellipse(pxPos, pyPos+22, 48, 15, 0, 0, Math.PI*2); ctx.fill();

  // Shield bubble
  if (G.shieldT > 0) {
    ctx.save();
    ctx.strokeStyle = '#cc44ff';
    ctx.shadowColor = '#cc44ff'; ctx.shadowBlur = 24;
    ctx.lineWidth = 3;
    ctx.globalAlpha = 0.65 + Math.sin(G.frame*0.25)*0.3;
    ctx.beginPath(); ctx.ellipse(pxPos, pyPos-10, 40, 58, 0, 0, Math.PI*2); ctx.stroke();
    ctx.restore();
  }

  // Magnet aura
  if (G.magnetT > 0) {
    ctx.save();
    ctx.strokeStyle = '#ff8844';
    ctx.shadowColor = '#ff8844'; ctx.shadowBlur = 30;
    ctx.lineWidth = 2;
    ctx.globalAlpha = 0.4 + Math.sin(G.frame*0.3)*0.3;
    ctx.setLineDash([4, 6]);
    ctx.beginPath(); ctx.arc(pxPos, pyPos-10, 80, 0, Math.PI*2); ctx.stroke();
    ctx.restore();
  }

  // Nitro flames
  if (G.nitroOn) {
    for (let j = 0; j < 3; j++) {
      ctx.save();
      ctx.globalAlpha = 0.55 + Math.random()*0.4;
      ctx.font = (14+Math.random()*10) + 'px serif';
      ctx.textAlign = 'center';
      ctx.shadowColor = car.col; ctx.shadowBlur = 16;
      ctx.fillText('🔥', pxPos + (j-1)*12, pyPos + 36 + Math.random()*10);
      ctx.restore();
    }
  }

  // Car
  ctx.save();
  ctx.translate(pxPos, pyPos);
  ctx.rotate(tilt * Math.PI / 180);
  if (G.flashT > 0 && Math.floor(G.flashT*12)%2===0) ctx.filter = 'brightness(6) saturate(0)';
  if (G.nitroOn) { ctx.shadowColor = car.col; ctx.shadowBlur = 30; }
  ctx.font = '60px serif';
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(car.emoji, 0, 0);
  ctx.restore();

  // ── FLOAT TEXTS ──
  ctx.save();
  for (const f of floats) {
    ctx.globalAlpha = Math.max(0, f.life);
    ctx.shadowColor = f.col; ctx.shadowBlur = 12;
    ctx.fillStyle = f.col;
    ctx.font = "bold 14px 'Orbitron',sans-serif";
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(f.txt, f.x, f.y);
  }
  ctx.shadowBlur = 0; ctx.globalAlpha = 1;
  ctx.restore();

  // ── SCREEN EFFECTS ──
  if (G.flashT > 0 && Math.floor(G.flashT*12)%2===0) {
    ctx.fillStyle = 'rgba(255,30,30,0.18)';
    ctx.fillRect(0, 0, W, H);
  }
  if (G.nitroOn) {
    // Speed lines
    ctx.save();
    ctx.globalAlpha = 0.04 * (G.speed / G.maxSpd);
    ctx.fillStyle = car.col;
    ctx.fillRect(0, 0, W, H);
    ctx.restore();
    for (let i = 0; i < 12; i++) {
      const lx = Math.random() * W;
      const ly = HORIZON_Y + Math.random() * (H - HORIZON_Y);
      const ll = 20 + Math.random() * 60;
      ctx.save();
      ctx.globalAlpha = 0.12 + Math.random()*0.1;
      ctx.strokeStyle = car.col;
      ctx.lineWidth = 0.8;
      ctx.beginPath(); ctx.moveTo(lx, ly); ctx.lineTo(lx, ly+ll); ctx.stroke();
      ctx.restore();
    }
  }
  if (G.shieldT > 0) {
    ctx.strokeStyle = 'rgba(204,68,255,0.18)';
    ctx.lineWidth = 8;
    ctx.strokeRect(4, 4, W-8, H-8);
  }
}

// ─── LOOP ──────────────────────────────────────────────────────────
function loop() {
  if (!G.running) return;
  render(); update();
  raf = requestAnimationFrame(loop);
}

// ─── CAR GRID ──────────────────────────────────────────────────────
function buildCarGrid() {
  const div = document.createElement('div');
  div.className = 'car-grid';
  CARS.forEach((c, i) => {
    const card = document.createElement('div');
    card.className = 'car-card' + (i===selCar?' sel':'');
    card.innerHTML = `
      <span class="car-emoji">${c.emoji}</span>
      <div class="car-name" style="color:${c.col}">${c.name}</div>
      <div class="car-type">${c.type}</div>
      <div class="car-bars">
        <div class="car-bar-row"><span class="car-bar-label">SPD</span><div class="car-bar-track"><div class="car-bar-fill" style="width:${c.statSpd}%;background:${c.col}"></div></div></div>
        <div class="car-bar-row"><span class="car-bar-label">HP</span><div class="car-bar-track"><div class="car-bar-fill" style="width:${c.statHp}%;background:#ff3366"></div></div></div>
        <div class="car-bar-row"><span class="car-bar-label">ACC</span><div class="car-bar-track"><div class="car-bar-fill" style="width:${c.statAcc}%;background:#ffaa00"></div></div></div>
      </div>`;
    card.onclick = () => {
      selCar = i;
      document.querySelectorAll('.car-card').forEach((x,j) => x.classList.toggle('sel', j===i));
    };
    div.appendChild(card);
  });
  return div;
}

// ─── OVERLAYS ──────────────────────────────────────────────────────
function showTitle() {
  cancelAnimationFrame(raf); G.running = false;
  const best = parseInt(localStorage.getItem('nrBest2')||'0');
  const ov = document.getElementById('overlay-inner');
  ov.innerHTML = `
    <div class="ov-badge">NEON RUNAWAY v4.0</div>
    <div class="ov-title" style="color:#00ffb4">🏎️<br>네온 도주</div>
    <div class="ov-sub">5-LANE · POLICE WAVES · NITRO · ×12 COMBO · 7 POWER-UPS</div>`;
  ov.appendChild(buildCarGrid());
  const rest = document.createElement('div');
  rest.innerHTML = `
    <div class="inst-row">
      ← → / A D / 버튼 — 레인 전환 &nbsp;|&nbsp; SPACE / ⚡ — 니트로<br>
      모바일: 좌우 스와이프로 레인 전환<br>
      경찰을 따돌리고 웨이브를 클리어하라!
    </div>
    ${best>0 ? `<div class="best-row">🏆 최고기록: <span class="best-num">${best.toLocaleString()}</span></div>` : ''}
    <div class="action-btn" id="start-btn">시동 걸기 🚀</div>`;
  ov.appendChild(rest);
  document.getElementById('start-btn').onclick = startGame;
  document.getElementById('overlay').style.display = 'flex';
}

function showGameOver() {
  G.running = false; cancelAnimationFrame(raf);
  const best = Math.max(G.score, parseInt(localStorage.getItem('nrBest2')||'0'));
  localStorage.setItem('nrBest2', best);
  const isRecord = G.score >= best && G.score > 0;
  const ov = document.getElementById('overlay-inner');
  ov.innerHTML = `
    <div class="ov-badge">${isRecord ? '🏆 NEW RECORD!' : 'GAME OVER'}</div>
    <div class="ov-title" style="color:#ff3355">💥 충돌!</div>
    <div class="ov-sub">YOU CRASHED · WAVE ${G.wave} · ${G.totalKills} VEHICLES DODGED</div>
    <div class="stats-row">
      <div class="stat-box"><div class="stat-num" style="color:#ffaa00">${G.score.toLocaleString()}</div><div class="stat-lbl">SCORE</div></div>
      <div class="stat-box"><div class="stat-num" style="color:#00ffb4">${G.dist.toFixed(2)}km</div><div class="stat-lbl">DIST</div></div>
      <div class="stat-box"><div class="stat-num" style="color:#cc44ff">×${G.maxCombo}</div><div class="stat-lbl">BEST COMBO</div></div>
    </div>
    <div class="best-row">🏆 최고기록: <span class="best-num">${best.toLocaleString()}</span></div>
    <div class="action-btn" id="start-btn">다시 도주 🏎️</div>
    <br><div class="sec-btn" id="cfg-btn">차량 변경</div>`;
  document.getElementById('start-btn').onclick = startGame;
  document.getElementById('cfg-btn').onclick = showTitle;
  document.getElementById('overlay').style.display = 'flex';
}

function startGame() {
  document.getElementById('overlay').style.display = 'none';
  cancelAnimationFrame(raf);
  floats = []; particles = [];
  initGame();
  raf = requestAnimationFrame(loop);
}

// ─── TOUCH CONTROLS ────────────────────────────────────────────────
function addTouch(id, dn, up) {
  const el = document.getElementById(id); if (!el) return;
  const d = e => { e.preventDefault(); dn(); el.classList.add('pressed'); };
  const u = e => { e.preventDefault(); up(); el.classList.remove('pressed'); };
  el.addEventListener('touchstart', d, {passive:false});
  el.addEventListener('touchend',   u, {passive:false});
  el.addEventListener('touchcancel',u, {passive:false});
  el.addEventListener('mousedown',  d);
  el.addEventListener('mouseup',    u);
  el.addEventListener('mouseleave', u);
}
addTouch('btn-left',  () => G._tLeft  = true, () => G._tLeft  = false);
addTouch('btn-right', () => G._tRight = true, () => G._tRight = false);
addTouch('nitro-btn', () => G._tNitro = true, () => G._tNitro = false);

// ─── INIT ──────────────────────────────────────────────────────────
showTitle();
</script>
</body>
</html>"""


def render():
    st.markdown("<style>iframe{border:none!important;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=760, scrolling=False)
