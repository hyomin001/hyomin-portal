import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
html,body{width:100%;height:100%;overflow:hidden;background:#000;touch-action:none;}
#wrap{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center;overflow:hidden;}
#gameCanvas{display:block;touch-action:none;}
#ui{position:absolute;top:0;left:0;font-family:'Rajdhani',sans-serif;}
#hud{position:absolute;top:12px;left:16px;right:16px;display:flex;justify-content:space-between;align-items:flex-start;}
.hud-box{background:rgba(0,0,0,.7);border:1px solid rgba(0,220,255,.25);border-radius:8px;padding:4px 12px;text-align:center;}
.hud-val{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:700;color:#fff;line-height:1;}
.hud-lbl{font-size:9px;color:rgba(0,220,255,.6);letter-spacing:2px;margin-top:1px;}
#score-val{color:#00dcff;}
#wanted-box{display:flex;flex-direction:column;align-items:center;gap:3px;}
#stars{display:flex;gap:3px;}
.star{font-size:14px;opacity:.2;transition:all .2s;}
.star.on{opacity:1;filter:drop-shadow(0 0 6px gold);}
#nitro-bar-wrap{position:absolute;bottom:110px;left:50%;transform:translateX(-50%);width:200px;text-align:center;}
#nitro-label{font-size:9px;color:rgba(0,220,255,.7);letter-spacing:3px;margin-bottom:4px;}
#nitro-bg{height:8px;background:rgba(255,255,255,.08);border-radius:99px;overflow:hidden;border:1px solid rgba(0,220,255,.2);}
#nitro-fill{height:100%;background:linear-gradient(90deg,#0088bb,#00dcff,#aaffff);border-radius:99px;transition:width .04s;width:100%;}
#combo-display{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:36px;font-weight:900;color:#f5c518;text-shadow:0 0 20px #f5c518;opacity:0;transition:opacity .2s;pointer-events:none;text-align:center;}
#announce{position:absolute;top:38%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:clamp(16px,4vw,26px);font-weight:900;letter-spacing:3px;opacity:0;pointer-events:none;text-align:center;white-space:nowrap;}
#controls{position:absolute;bottom:14px;left:0;right:0;display:flex;justify-content:space-between;align-items:flex-end;padding:0 14px;pointer-events:all;}
#dpad{display:flex;gap:8px;}
.btn{width:64px;height:56px;border-radius:12px;background:rgba(255,255,255,.07);border:1.5px solid rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;user-select:none;-webkit-user-select:none;touch-action:none;transition:all .1s;color:rgba(255,255,255,.8);}
.btn:active,.btn.pressed{background:rgba(0,220,255,.2);border-color:rgba(0,220,255,.6);box-shadow:0 0 16px rgba(0,220,255,.4);transform:scale(.91);}
#nitro-btn{width:80px;height:80px;border-radius:50%;background:rgba(0,220,255,.1);border:2px solid rgba(0,220,255,.4);flex-direction:column;font-size:24px;color:#00dcff;}
.btn-lbl{font-size:8px;letter-spacing:2px;margin-top:2px;color:rgba(0,220,255,.8);}
#overlay{position:absolute;inset:0;background:rgba(0,0,0,.92);display:flex;align-items:center;justify-content:center;pointer-events:all;z-index:200;}
#overlay-inner{text-align:center;max-width:380px;width:92vw;padding:28px 20px;border:1px solid rgba(0,220,255,.2);border-radius:18px;background:rgba(2,8,18,.97);}
.ov-tag{font-size:8px;letter-spacing:4px;color:#00dcff;background:rgba(0,220,255,.1);border:1px solid rgba(0,220,255,.2);border-radius:99px;padding:4px 16px;display:inline-block;margin-bottom:16px;}
.ov-title{font-family:'Orbitron',sans-serif;font-size:clamp(22px,6vw,36px);font-weight:900;margin-bottom:6px;}
.ov-sub{font-size:9px;color:rgba(255,255,255,.3);letter-spacing:3px;margin-bottom:20px;}
.car-grid{display:flex;gap:8px;margin-bottom:18px;}
.car-card{flex:1;padding:10px 6px;background:rgba(255,255,255,.04);border:1.5px solid rgba(255,255,255,.08);border-radius:10px;cursor:pointer;transition:all .2s;text-align:center;}
.car-card.sel{border-color:#00dcff;background:rgba(0,220,255,.1);}
.car-emoji{font-size:26px;display:block;margin-bottom:4px;}
.car-name{font-size:9px;font-weight:700;letter-spacing:1px;}
.car-stat{font-size:7px;color:rgba(255,255,255,.3);margin-top:2px;}
.start-btn{display:inline-block;padding:13px 40px;background:rgba(0,220,255,.15);border:1px solid rgba(0,220,255,.5);border-radius:12px;font-family:'Orbitron',sans-serif;font-size:15px;font-weight:700;color:#00dcff;cursor:pointer;letter-spacing:2px;transition:all .2s;}
.start-btn:hover{background:rgba(0,220,255,.3);transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,220,255,.3);}
.stats-row{display:flex;gap:10px;justify-content:center;margin-bottom:18px;}
.stat-box{padding:8px 16px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.08);border-radius:8px;text-align:center;}
.stat-num{font-family:'Orbitron',sans-serif;font-size:18px;font-weight:700;color:#fff;}
.stat-lbl{font-size:8px;color:rgba(255,255,255,.3);letter-spacing:2px;margin-top:2px;}
#lives-row{display:flex;gap:5px;margin-top:4px;}
.life-dot{width:10px;height:10px;border-radius:50%;background:#ff2244;box-shadow:0 0 6px rgba(255,34,68,.8);}
.life-dot.dead{background:#2a0508;box-shadow:none;}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="gameCanvas"></canvas>
  <div id="ui" style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;">
    <div id="hud">
      <div class="hud-box"><div class="hud-val" id="score-val">0</div><div class="hud-lbl">SCORE</div></div>
      <div class="hud-box"><div class="hud-val" id="dist-val">0.00</div><div class="hud-lbl">KM</div></div>
      <div class="hud-box" id="wanted-box">
        <div id="stars"><span class="star" id="s0">★</span><span class="star" id="s1">★</span><span class="star" id="s2">★</span><span class="star" id="s3">★</span><span class="star" id="s4">★</span></div>
        <div id="lives-row"></div>
        <div class="hud-lbl">WANTED</div>
      </div>
    </div>
    <div id="nitro-bar-wrap"><div id="nitro-label">NITRO</div><div id="nitro-bg"><div id="nitro-fill"></div></div></div>
    <div id="combo-display"></div>
    <div id="announce"></div>
    <div id="controls" style="pointer-events:all;">
      <div id="dpad">
        <div class="btn" id="btn-left">◀</div>
        <div class="btn" id="btn-right">▶</div>
      </div>
      <div class="btn" id="nitro-btn" style="display:flex;">⚡<span class="btn-lbl">NITRO</span></div>
    </div>
    <div id="overlay" style="pointer-events:all;"><div id="overlay-inner"></div></div>
  </div>
</div>

<script>
'use strict';
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const wrap = document.getElementById('wrap');
const uiEl = document.getElementById('ui');

const BASE_W = 420, BASE_H = 720;
let W = BASE_W, H = BASE_H;

function resize() {
  const rw = window.innerWidth, rh = window.innerHeight;
  const sc = Math.min(rw / BASE_W, rh / BASE_H);
  canvas.width = W; canvas.height = H;
  const pw = BASE_W * sc, ph = BASE_H * sc;
  canvas.style.width = pw + 'px';
  canvas.style.height = ph + 'px';
  canvas.style.position = 'absolute';
  canvas.style.left = ((rw - pw) / 2) + 'px';
  canvas.style.top = ((rh - ph) / 2) + 'px';
  uiEl.style.width = pw + 'px';
  uiEl.style.height = ph + 'px';
  uiEl.style.left = ((rw - pw) / 2) + 'px';
  uiEl.style.top = ((rh - ph) / 2) + 'px';
}
resize();
window.addEventListener('resize', resize);

const CARS = [
  {name:'스포츠', emoji:'🚗', spd:1.0, col:'#00dcff', hp:3},
  {name:'슈퍼카', emoji:'🏎️', spd:1.35, col:'#ff2244', hp:2},
  {name:'SUV',   emoji:'🚙', spd:0.78, col:'#00ff88', hp:4},
  {name:'머슬',  emoji:'🚘', spd:1.1,  col:'#f5c518', hp:3},
];

const TRAFFIC = [
  {emoji:'🚌', spd:2.2, pts:20, cop:false},
  {emoji:'🚛', spd:1.8, pts:30, cop:false},
  {emoji:'🚓', spd:4.8, pts:10, cop:true },
  {emoji:'🏍️', spd:4.2, pts:12, cop:false},
  {emoji:'🚑', spd:2.8, pts:22, cop:false},
  {emoji:'🚜', spd:1.4, pts:35, cop:false},
  {emoji:'🚐', spd:2.5, pts:18, cop:false},
];

const PWRS = [
  {emoji:'⚡', type:'nitro', col:'#00dcff', label:'NITRO +60%'},
  {emoji:'⭐', type:'score', col:'#f5c518', label:'+500 BONUS!'},
  {emoji:'💊', type:'heal',  col:'#00ff88', label:'HP RESTORED'},
  {emoji:'🔱', type:'shield',col:'#c04fff', label:'INVINCIBLE 5S'},
  {emoji:'💨', type:'boost', col:'#88ffff', label:'SPEED BOOST'},
];

const LANES = 5;
const LANE_XS = [0.13, 0.295, 0.46, 0.625, 0.79];
const ROAD_LEFT = 0.08 * BASE_W, ROAD_RIGHT = 0.92 * BASE_W;
const ROAD_W = ROAD_RIGHT - ROAD_LEFT;
const HORIZON_Y = BASE_H * 0.43;
const VANISH_X = BASE_W / 2;

function laneScreenX(laneIdx, depthY) {
  const laneCenter = ROAD_LEFT + (laneIdx + 0.5) * (ROAD_W / LANES);
  return VANISH_X + (laneCenter - VANISH_X) * depthY;
}
function roadScreenW(depthY) { return ROAD_W * depthY; }
function screenY(depthY) { return HORIZON_Y + (BASE_H - HORIZON_Y) * depthY; }

const KEYS = {};
window.addEventListener('keydown', e => {
  KEYS[e.code] = true;
  if (['ArrowLeft','ArrowRight','Space'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e => KEYS[e.code] = false);

let selCar = 0, G = {}, raf = null, floats = [];
let lastLeft = false, lastRight = false, uid = 0;

function initGame() {
  const car = CARS[selCar];
  G = {
    running:true, dead:false, frame:0,
    score:0, dist:0,
    lane:2, laneT:1, laneFrom:2, laneTarget:2,
    speed:0, baseSpd:3.2*car.spd, maxSpd:7.8*car.spd,
    nitro:100, nitroOn:false,
    hp:car.hp, maxHp:car.hp,
    shieldT:0, boostT:0, flashT:0,
    combo:1, comboD:0,
    wanted:0, wantedD:0,
    traffic:[], powers:[],
    spawnD:0, pwrD:0,
    scroll:0, bgShift:0,
    wave:1, waveKills:0, waveTarget:6,
    stars: Array.from({length:80}, () => ({
      x:Math.random()*BASE_W, y:Math.random()*HORIZON_Y,
      r:Math.random()*1.4+0.3, t:Math.random()*Math.PI*2
    })),
    _annTimer:null,
    _tLeft:false, _tRight:false, _tNitro:false,
  };
  floats = [];
  lastLeft = false; lastRight = false;
  buildLives(); updWanted();
  for (let i = 0; i < 5; i++) spawnTraffic(true);
  spawnPwr();
}

function buildLives() {
  const r = document.getElementById('lives-row');
  r.innerHTML = '';
  for (let i = 0; i < G.maxHp; i++) {
    const d = document.createElement('div');
    d.className = 'life-dot' + (i >= G.hp ? ' dead' : '');
    d.id = 'ld' + i;
    r.appendChild(d);
  }
}
function updLives() {
  for (let i = 0; i < G.maxHp; i++) {
    const d = document.getElementById('ld' + i);
    if (d) d.className = 'life-dot' + (i >= G.hp ? ' dead' : '');
  }
}
function updWanted() {
  for (let i = 0; i < 5; i++) {
    const el = document.getElementById('s' + i);
    if (el) el.classList.toggle('on', i < G.wanted);
  }
}

function spawnTraffic(far) {
  const def = TRAFFIC[Math.floor(Math.random() * TRAFFIC.length)];
  if (def.cop && G.wanted < 2) return;
  G.traffic.push({
    id: uid++,
    lane: Math.floor(Math.random() * LANES),
    depth: far ? Math.random()*0.18+0.02 : 0.02+Math.random()*0.06,
    spd: def.spd*(0.9+Math.random()*0.3),
    emoji:def.emoji, pts:def.pts, cop:def.cop,
    alive:true, scored:false, siren:0,
  });
}
function spawnPwr() {
  const def = PWRS[Math.floor(Math.random() * PWRS.length)];
  G.powers.push({
    lane:Math.floor(Math.random()*LANES), depth:0.02,
    type:def.type, emoji:def.emoji, col:def.col, label:def.label,
    alive:true, rot:0,
  });
}
function spawnFloat(txt, col) {
  floats.push({txt, col, x:BASE_W/2, y:BASE_H*0.52, vy:-2.2, life:1});
}
function announce(txt, col) {
  const el = document.getElementById('announce');
  if (!el) return;
  el.textContent = txt; el.style.color = col;
  el.style.textShadow = '0 0 24px ' + col; el.style.opacity = '1';
  clearTimeout(G._annTimer);
  G._annTimer = setTimeout(() => { el.style.opacity = '0'; }, 1400);
}
function getLaneX(t) {
  const ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
  return LANE_XS[G.laneFrom]*BASE_W + (LANE_XS[G.laneTarget]-LANE_XS[G.laneFrom])*BASE_W*ease;
}
function playerScreenX() {
  return G.laneT >= 1 ? LANE_XS[G.lane]*BASE_W : getLaneX(G.laneT);
}

function update() {
  if (!G.running || G.dead) return;
  G.frame++;

  const left  = KEYS['ArrowLeft']  || KEYS['KeyA'] || G._tLeft;
  const right = KEYS['ArrowRight'] || KEYS['KeyD'] || G._tRight;
  const nitro = KEYS['Space'] || KEYS['ShiftLeft'] || G._tNitro;

  if (left && !lastLeft && G.laneT >= 1) {
    if (G.lane > 0) { G.laneFrom=G.lane; G.laneTarget=G.lane-1; G.laneT=0; G.lane--; }
    else announce('WALL!', '#ff2244');
  }
  if (right && !lastRight && G.laneT >= 1) {
    if (G.lane < LANES-1) { G.laneFrom=G.lane; G.laneTarget=G.lane+1; G.laneT=0; G.lane++; }
    else announce('WALL!', '#ff2244');
  }
  lastLeft = left; lastRight = right;
  if (G.laneT < 1) G.laneT = Math.min(1, G.laneT + 0.18);

  if (nitro && G.nitro > 0) { G.nitroOn=true; G.nitro=Math.max(0,G.nitro-0.7); }
  else { G.nitroOn=false; G.nitro=Math.min(100,G.nitro+0.22); }

  const nitroM = G.nitroOn ? 1.9 : (G.boostT > 0 ? 1.4 : 1);
  G.speed += (G.baseSpd*nitroM - G.speed) * 0.04;

  if (G.shieldT > 0) G.shieldT -= 1/60;
  if (G.boostT  > 0) G.boostT  -= 1/60;
  if (G.flashT  > 0) G.flashT  -= 0.06;
  if (G.comboD  > 0) G.comboD--;
  else if (G.combo > 1) { G.combo=Math.max(1,G.combo-1); G.comboD=90; }
  if (G.wantedD > 0) G.wantedD--;
  else if (G.wanted > 0) { G.wanted=Math.max(0,G.wanted-1); G.wantedD=550; updWanted(); }

  G.scroll  += G.speed * 0.012;
  G.bgShift  = (G.bgShift + G.speed*0.0006) % 1;
  G.dist    += G.speed * 0.00025;

  G.spawnD -= G.speed;
  if (G.spawnD <= 0) {
    spawnTraffic(false);
    if (G.wanted >= 3) spawnTraffic(false);
    G.spawnD = Math.max(60, 280 - G.speed*12 - G.wave*8 + Math.random()*80);
  }

  for (const tc of G.traffic) {
    if (!tc.alive) continue;
    tc.depth += (G.speed - tc.spd*(tc.cop ? 0.85+G.wanted*0.06 : 0.85)) * 0.00022;
    if (tc.cop) tc.siren = (tc.siren+1) % 60;

    if (tc.depth >= 0.72 && tc.depth <= 1.05) {
      const pLane = G.laneT >= 0.5 ? G.laneTarget : G.laneFrom;
      if (Math.abs(pLane - tc.lane) < 0.6) {
        if (G.shieldT > 0) {
          tc.alive=false; spawnFloat('BLOCKED! +100','#c04fff'); G.score+=100;
        } else {
          G.hp--; G.flashT=1; G.speed=Math.max(G.baseSpd*0.3,G.speed*0.4);
          G.combo=1; G.comboD=0; tc.alive=false;
          updLives(); announce('CRASH!','#ff2244');
          if (G.hp <= 0) { G.dead=true; setTimeout(showGameOver,700); }
        }
        continue;
      }
    }
    if (!tc.scored && tc.depth > 1.05) {
      tc.scored=true;
      const pts = tc.pts*G.combo;
      G.score+=pts; G.combo=Math.min(8,G.combo+1); G.comboD=120; G.waveKills++;
      spawnFloat('+'+pts, G.combo>=3?'#f5c518':'#00dcff');
      if (tc.cop) { G.wanted=Math.min(5,G.wanted+1); G.wantedD=600; updWanted(); }
      if (G.combo >= 3) announce('×'+G.combo+' COMBO!','#f5c518');
      if (G.waveKills >= G.waveTarget) {
        G.wave++; G.waveKills=0; G.waveTarget=Math.min(15,G.waveTarget+2);
        G.baseSpd=Math.min(G.maxSpd,G.baseSpd*1.07);
        announce('WAVE '+G.wave+'!','#00ff88');
      }
    }
    if (tc.depth > 1.3) tc.alive=false;
  }
  G.traffic = G.traffic.filter(t=>t.alive);
  if (G.traffic.length > 22) G.traffic.splice(0,5);

  G.pwrD -= G.speed;
  if (G.pwrD <= 0) { spawnPwr(); G.pwrD=320+Math.random()*300; }

  for (const pw of G.powers) {
    if (!pw.alive) continue;
    pw.rot+=0.06; pw.depth+=G.speed*0.00022;
    if (pw.depth >= 0.74 && pw.depth <= 1.05) {
      const pLane = G.laneT >= 0.5 ? G.laneTarget : G.laneFrom;
      if (Math.abs(pLane - pw.lane) < 0.55) {
        pw.alive=false; spawnFloat(pw.label,pw.col);
        if (pw.type==='nitro')  G.nitro=Math.min(100,G.nitro+60);
        if (pw.type==='score')  G.score+=500;
        if (pw.type==='heal')   { G.hp=Math.min(G.maxHp,G.hp+1); updLives(); }
        if (pw.type==='shield') G.shieldT=5;
        if (pw.type==='boost')  G.boostT=5;
      }
    }
    if (pw.depth > 1.3) pw.alive=false;
  }
  G.powers = G.powers.filter(p=>p.alive);

  if (G.frame % 6 === 0) G.score += Math.floor(G.speed*G.combo*0.15);

  for (let i=floats.length-1; i>=0; i--) {
    floats[i].y+=floats[i].vy; floats[i].life-=0.024;
    if (floats[i].life<=0) floats.splice(i,1);
  }

  const sv=document.getElementById('score-val');
  const dv=document.getElementById('dist-val');
  const nf=document.getElementById('nitro-fill');
  const cd=document.getElementById('combo-display');
  if (sv) sv.textContent=G.score.toLocaleString();
  if (dv) dv.textContent=G.dist.toFixed(2);
  if (nf) nf.style.width=G.nitro+'%';
  if (cd) { if(G.combo>=2){cd.textContent='×'+G.combo;cd.style.opacity='1';}else cd.style.opacity='0'; }
}

function render() {
  ctx.clearRect(0,0,W,H);

  // Sky
  const sky=ctx.createLinearGradient(0,0,0,HORIZON_Y);
  sky.addColorStop(0,'#010208'); sky.addColorStop(1,'#040c1e');
  ctx.fillStyle=sky; ctx.fillRect(0,0,W,HORIZON_Y);

  // Stars
  ctx.save();
  for (const s of G.stars) {
    s.t+=0.01; ctx.globalAlpha=0.4+Math.sin(s.t)*0.35;
    ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2); ctx.fill();
  }
  ctx.globalAlpha=1; ctx.restore();

  // City
  ctx.fillStyle='#020509';
  for (let i=0;i<14;i++) {
    const bw=24+Math.sin(i*2.1)*12, bh=45+Math.sin(i*1.7)*40+12;
    ctx.fillRect(i*(W/13.2)-10, HORIZON_Y-bh, bw, bh);
  }

  // Horizon glow
  ctx.save();
  const hg=ctx.createLinearGradient(0,HORIZON_Y-8,0,HORIZON_Y+8);
  hg.addColorStop(0,'transparent'); hg.addColorStop(0.5,'rgba(192,79,255,0.3)'); hg.addColorStop(1,'transparent');
  ctx.fillStyle=hg; ctx.fillRect(0,HORIZON_Y-8,W,16); ctx.restore();

  // Ground
  const grd=ctx.createLinearGradient(0,HORIZON_Y,0,H);
  grd.addColorStop(0,'#050c1a'); grd.addColorStop(1,'#030810');
  ctx.fillStyle=grd; ctx.fillRect(0,HORIZON_Y,W,H-HORIZON_Y);

  // Road
  const topL=laneScreenX(-0.5,0), topR=laneScreenX(LANES-0.5,0);
  ctx.beginPath(); ctx.moveTo(topL,HORIZON_Y); ctx.lineTo(topR,HORIZON_Y);
  ctx.lineTo(ROAD_RIGHT,H); ctx.lineTo(ROAD_LEFT,H); ctx.closePath();
  ctx.fillStyle='#060d1c'; ctx.fill();

  // Road borders
  ctx.save(); ctx.shadowColor='#c04fff'; ctx.shadowBlur=14;
  ctx.strokeStyle='rgba(192,79,255,0.6)'; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(topL,HORIZON_Y); ctx.lineTo(ROAD_LEFT,H); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(topR,HORIZON_Y); ctx.lineTo(ROAD_RIGHT,H); ctx.stroke();
  ctx.restore();

  // Lane dividers
  for (let l=1; l<LANES; l++) {
    for (let d=0; d<12; d++) {
      const t1=((d+G.scroll*0.3)%12)/12;
      const t2=((d+G.scroll*0.3)%12+0.45)/12;
      const y1=screenY(t1), y2=screenY(t2);
      if (y2<HORIZON_Y||y1>H) continue;
      ctx.save(); ctx.globalAlpha=Math.min(1,t1*2.5)*0.35;
      ctx.strokeStyle='rgba(0,220,255,0.55)'; ctx.lineWidth=Math.max(0.5,t1*2.5);
      ctx.beginPath(); ctx.moveTo(laneScreenX(l-0.5,t1),y1); ctx.lineTo(laneScreenX(l-0.5,t2),y2); ctx.stroke();
      ctx.restore();
    }
  }

  // Rumble strips
  for (let d=0; d<10; d++) {
    const t=(d/10+G.bgShift)%1, t2=((d+0.5)/10+G.bgShift)%1;
    const y1=screenY(t), y2=screenY(t2);
    if (y2<HORIZON_Y||y1>H) continue;
    const col=Math.floor(t*10)%2===0?'rgba(255,34,68,0.6)':'rgba(255,255,255,0.4)';
    const lx1=laneScreenX(-0.5,t), lx2=laneScreenX(-0.5,t2);
    const rx1=laneScreenX(LANES-0.5,t), rx2=laneScreenX(LANES-0.5,t2);
    const rw=roadScreenW(t)*0.04;
    ctx.fillStyle=col;
    ctx.beginPath(); ctx.moveTo(lx1-rw,y1); ctx.lineTo(lx1,y1); ctx.lineTo(lx2,y2); ctx.lineTo(lx2-rw,y2); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(rx1,y1); ctx.lineTo(rx1+rw,y1); ctx.lineTo(rx2+rw,y2); ctx.lineTo(rx2,y2); ctx.closePath(); ctx.fill();
  }

  // Traffic
  const sorted=[...G.traffic].sort((a,b)=>a.depth-b.depth);
  for (const tc of sorted) {
    if (!tc.alive) continue;
    const d=tc.depth;
    if (d<0.01||d>1.15) continue;
    const px=laneScreenX(tc.lane+0.5,d), py=screenY(d), sz=Math.max(10,d*70);
    ctx.save();
    if (tc.cop&&tc.siren>0) { ctx.shadowColor=Math.floor(tc.siren/10)%2===0?'rgba(50,80,255,0.6)':'rgba(255,30,30,0.6)'; ctx.shadowBlur=sz*0.8; }
    ctx.font=sz+'px serif'; ctx.textAlign='center'; ctx.textBaseline='bottom';
    ctx.fillText(tc.emoji,px,py-2); ctx.restore();
  }

  // Powers
  for (const pw of G.powers) {
    if (!pw.alive) continue;
    const d=pw.depth;
    if (d<0.01||d>1.15) continue;
    const px=laneScreenX(pw.lane+0.5,d), py=screenY(d), sz=Math.max(8,d*58);
    ctx.save(); ctx.translate(px,py-sz*0.5); ctx.rotate(pw.rot);
    ctx.shadowColor=pw.col; ctx.shadowBlur=sz*0.8;
    ctx.font=sz+'px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(pw.emoji,0,0); ctx.restore();
  }

  // Player
  const car=CARS[selCar];
  const px=playerScreenX(), py=H-90;
  const tilt=G.laneT<1?(G.laneTarget>G.laneFrom?1:-1)*(1-G.laneT)*12:0;

  ctx.save(); ctx.globalAlpha=0.3; ctx.fillStyle='#000';
  ctx.beginPath(); ctx.ellipse(px,py+30,32,9,0,0,Math.PI*2); ctx.fill(); ctx.restore();

  const ug=ctx.createRadialGradient(px,py+18,0,px,py+18,44);
  ug.addColorStop(0,car.col+(G.nitroOn?'bb':'44')); ug.addColorStop(1,'transparent');
  ctx.fillStyle=ug; ctx.beginPath(); ctx.ellipse(px,py+22,42,14,0,0,Math.PI*2); ctx.fill();

  if (G.shieldT>0) {
    ctx.save(); ctx.strokeStyle='#c04fff'; ctx.shadowColor='#c04fff'; ctx.shadowBlur=20;
    ctx.lineWidth=3; ctx.globalAlpha=0.7+Math.sin(G.frame*0.2)*0.3;
    ctx.beginPath(); ctx.ellipse(px,py-8,38,52,0,0,Math.PI*2); ctx.stroke(); ctx.restore();
  }
  if (G.nitroOn) {
    for (let j=0;j<2;j++) {
      ctx.save(); ctx.globalAlpha=0.5+Math.random()*0.45; ctx.font='18px serif'; ctx.textAlign='center';
      ctx.shadowColor=car.col; ctx.shadowBlur=14;
      ctx.fillText('🔥',px+(j===0?-10:10),py+34+Math.random()*8); ctx.restore();
    }
  }

  ctx.save(); ctx.translate(px,py); ctx.rotate(tilt*Math.PI/180);
  if (G.flashT>0&&Math.floor(G.flashT*10)%2===0) ctx.filter='brightness(5) saturate(0)';
  if (G.nitroOn) { ctx.shadowColor=car.col; ctx.shadowBlur=24; }
  ctx.font='58px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(car.emoji,0,0); ctx.restore();

  // Floats
  ctx.save();
  for (const f of floats) {
    ctx.globalAlpha=Math.max(0,f.life); ctx.shadowColor=f.col; ctx.shadowBlur=10;
    ctx.fillStyle=f.col; ctx.font="bold 15px 'Orbitron',sans-serif";
    ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(f.txt,f.x,f.y);
  }
  ctx.shadowBlur=0; ctx.globalAlpha=1; ctx.restore();

  if (G.flashT>0&&Math.floor(G.flashT*10)%2===0) { ctx.fillStyle='rgba(255,30,30,0.2)'; ctx.fillRect(0,0,W,H); }
  if (G.nitroOn) { ctx.fillStyle='rgba(0,220,255,0.06)'; ctx.fillRect(0,0,W,H); }
  if (G.shieldT>0) { ctx.strokeStyle='rgba(192,79,255,0.25)'; ctx.lineWidth=6; ctx.strokeRect(3,3,W-6,H-6); }
}

function loop() {
  if (!G.running) return;
  render(); update();
  raf = requestAnimationFrame(loop);
}

function buildCarGrid() {
  const div=document.createElement('div');
  div.className='car-grid';
  CARS.forEach((c,i)=>{
    const card=document.createElement('div');
    card.className='car-card'+(i===selCar?' sel':'');
    card.innerHTML='<span class="car-emoji">'+c.emoji+'</span><div class="car-name" style="color:'+c.col+'">'+c.name+'</div><div class="car-stat">'+['균형형','극한속도','내구형','가속형'][i]+'</div>';
    card.onclick=()=>{selCar=i;document.querySelectorAll('.car-card').forEach((x,j)=>x.classList.toggle('sel',j===i));};
    div.appendChild(card);
  });
  return div;
}

function showTitle() {
  const best=parseInt(localStorage.getItem('nrBest')||'0');
  const ov=document.getElementById('overlay-inner');
  ov.innerHTML='<div class="ov-tag">NEON RUNAWAY v3.0</div><div class="ov-title" style="color:#00dcff">🏎️<br>네온 도주 레이싱</div><div class="ov-sub">5-LANE · POLICE WAVE · NITRO · ×8 COMBO</div>';
  ov.appendChild(buildCarGrid());
  const rest=document.createElement('div');
  rest.innerHTML='<div style="font-size:10px;color:rgba(255,255,255,.25);line-height:2.2;margin-bottom:16px;">←→ 방향키 / 버튼 — 레인 전환 &nbsp;|&nbsp; SPACE — 니트로<br>경찰을 따돌리고 웨이브를 클리어하라!</div>'+
    (best>0?'<div style="font-size:10px;color:rgba(255,255,255,.3);margin-bottom:14px;">🏆 최고기록: <span style="color:#f5c518;font-family:Orbitron">'+best.toLocaleString()+'</span></div>':'')+
    '<div class="start-btn" id="start-btn">시동 걸기 🚀</div>';
  ov.appendChild(rest);
  document.getElementById('start-btn').onclick=startGame;
  document.getElementById('overlay').style.display='flex';
}

function showGameOver() {
  G.running=false; cancelAnimationFrame(raf);
  const best=Math.max(G.score,parseInt(localStorage.getItem('nrBest')||'0'));
  localStorage.setItem('nrBest',best);
  const ov=document.getElementById('overlay-inner');
  ov.innerHTML='<div class="ov-tag">'+(G.score>=best&&G.score>0?'🏆 NEW RECORD!':'GAME OVER')+'</div>'+
    '<div class="ov-title" style="color:#ff2244">💥 충돌!</div>'+
    '<div class="ov-sub">YOU CRASHED · WAVE '+G.wave+'</div>'+
    '<div class="stats-row"><div class="stat-box"><div class="stat-num" style="color:#f5c518">'+G.score.toLocaleString()+'</div><div class="stat-lbl">SCORE</div></div>'+
    '<div class="stat-box"><div class="stat-num" style="color:#00dcff">'+G.dist.toFixed(2)+' KM</div><div class="stat-lbl">DIST</div></div>'+
    '<div class="stat-box"><div class="stat-num" style="color:#00ff88">×'+G.combo+'</div><div class="stat-lbl">COMBO</div></div></div>'+
    '<div style="font-size:10px;color:rgba(255,255,255,.3);margin-bottom:16px;">🏆 최고기록: <span style="color:#f5c518;font-family:Orbitron">'+best.toLocaleString()+'</span></div>'+
    '<div class="start-btn" id="start-btn">다시 도주 🏎️</div>'+
    '<br><div style="display:inline-block;margin-top:10px;padding:9px 22px;border:1px solid rgba(255,255,255,.1);border-radius:10px;font-size:12px;color:rgba(255,255,255,.3);cursor:pointer;" id="cfg-btn">차량 변경</div>';
  document.getElementById('start-btn').onclick=startGame;
  document.getElementById('cfg-btn').onclick=showTitle;
  document.getElementById('overlay').style.display='flex';
}

function startGame() {
  document.getElementById('overlay').style.display='none';
  cancelAnimationFrame(raf); floats=[]; initGame();
  raf=requestAnimationFrame(loop);
}

function addTouch(id,dn,up) {
  const el=document.getElementById(id); if(!el)return;
  const d=e=>{e.preventDefault();dn();el.classList.add('pressed');};
  const u=e=>{e.preventDefault();up();el.classList.remove('pressed');};
  el.addEventListener('touchstart',d,{passive:false});
  el.addEventListener('touchend',u,{passive:false});
  el.addEventListener('touchcancel',u,{passive:false});
  el.addEventListener('mousedown',d);
  el.addEventListener('mouseup',u);
  el.addEventListener('mouseleave',u);
}
addTouch('btn-left',  ()=>G._tLeft=true,  ()=>G._tLeft=false);
addTouch('btn-right', ()=>G._tRight=true, ()=>G._tRight=false);
addTouch('nitro-btn', ()=>G._tNitro=true, ()=>G._tNitro=false);

showTitle();
</script>
</body>
</html>"""


def render():
    st.markdown("<style>iframe{border:none!important;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
