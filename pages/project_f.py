import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
html,body{width:100%;height:758px;overflow:hidden;background:#0a0a0f;touch-action:none;}
#wrap{position:relative;width:100%;height:758px;display:flex;align-items:center;justify-content:center;}
#gc{display:block;touch-action:none;}
#ui{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;display:flex;justify-content:space-between;align-items:stretch;padding:8px 10px;gap:6px;}
.hp{background:rgba(0,0,0,0.8);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:5px 10px;text-align:center;min-width:60px;}
.hv{font-family:'Orbitron',sans-serif;font-size:17px;font-weight:900;line-height:1;letter-spacing:1px;}
.hl{font-size:6px;letter-spacing:3px;color:rgba(255,255,255,0.3);margin-top:2px;font-family:'Share Tech Mono',monospace;}
#sv{color:#00ffcc;}
#wv{color:#ff8800;}
#dv{color:#88ccff;}

/* Wanted */
#wp{flex-direction:column;align-items:center;display:flex;gap:3px;}
#wp .hp{background:rgba(0,0,0,0.8);border:1px solid rgba(255,200,0,0.15);}
#stars-row{display:flex;gap:2px;}
.st{font-size:12px;opacity:.12;transition:all .25s;}
.st.on{opacity:1;filter:drop-shadow(0 0 6px gold);}
#lives{display:flex;gap:3px;margin-top:1px;}
.lp{width:9px;height:9px;border-radius:50%;background:#ff2255;box-shadow:0 0 7px rgba(255,34,85,.9);transition:all .3s;}
.lp.x{background:#1a0006;box-shadow:none;}

/* ── NITRO BAR ── */
#nb-wrap{position:absolute;bottom:96px;left:10px;right:10px;display:flex;align-items:center;gap:8px;}
#nb-lbl{font-size:7px;color:rgba(0,255,200,.55);letter-spacing:3px;font-family:'Share Tech Mono',monospace;white-space:nowrap;}
#nb-bg{flex:1;height:8px;background:rgba(255,255,255,.06);border-radius:99px;border:1px solid rgba(0,255,200,.12);overflow:hidden;}
#nb-fill{height:100%;background:linear-gradient(90deg,#006644,#00ffcc,#ccffee);border-radius:99px;transition:width .04s;}

/* ── COMBO ── */
#combo-pop{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:38px;font-weight:900;color:#ff8800;text-shadow:0 0 30px #ff8800,0 0 60px rgba(255,136,0,.4);opacity:0;pointer-events:none;white-space:nowrap;transition:opacity .15s;}
#banner{position:absolute;top:34%;left:50%;transform:translate(-50%,-50%);font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;letter-spacing:4px;opacity:0;pointer-events:none;white-space:nowrap;text-transform:uppercase;}

/* ── CONTROLS ── */
#ctrl{position:absolute;bottom:0;left:0;right:0;height:92px;display:flex;justify-content:space-between;align-items:center;padding:0 12px 8px;pointer-events:all;}
.cbtn{border-radius:14px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.11);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;user-select:none;touch-action:none;transition:all .08s;color:rgba(255,255,255,.65);}
#bl,#br{width:72px;height:60px;font-size:24px;}
.clbl{font-size:6px;letter-spacing:2px;margin-top:2px;color:rgba(0,255,200,.6);font-family:'Share Tech Mono',monospace;}
.cbtn:active,.cbtn.p{background:rgba(0,255,200,.14);border-color:rgba(0,255,200,.5);box-shadow:0 0 18px rgba(0,255,200,.3);transform:scale(.91);}
#nbtn{width:80px;height:80px;border-radius:50%;background:rgba(0,255,200,.07);border:2px solid rgba(0,255,200,.3);font-size:26px;color:#00ffcc;display:flex;flex-direction:column;align-items:center;justify-content:center;}
#nbtn.p{background:rgba(0,255,200,.22);box-shadow:0 0 28px rgba(0,255,200,.5);}

/* ── OVERLAY ── */
#ov{position:absolute;inset:0;background:rgba(0,0,8,.93);display:flex;align-items:center;justify-content:center;pointer-events:all;z-index:200;}
#oi{text-align:center;max-width:390px;width:93vw;padding:26px 18px 22px;border:1px solid rgba(0,255,200,.14);border-radius:20px;background:rgba(1,4,12,.97);}
.obadge{font-size:7px;letter-spacing:5px;color:#00ffcc;background:rgba(0,255,200,.07);border:1px solid rgba(0,255,200,.18);border-radius:99px;padding:4px 18px;display:inline-block;margin-bottom:14px;font-family:'Share Tech Mono',monospace;}
.otitle{font-family:'Orbitron',sans-serif;font-size:clamp(22px,6vw,36px);font-weight:900;margin-bottom:4px;}
.osub{font-size:7px;color:rgba(255,255,255,.22);letter-spacing:4px;margin-bottom:20px;font-family:'Share Tech Mono',monospace;}
.cgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:16px;}
.ccard{padding:10px 4px 8px;background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.07);border-radius:12px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard.sel{border-color:#00ffcc;background:rgba(0,255,200,.07);box-shadow:0 0 18px rgba(0,255,200,.12);}
.cem{font-size:26px;display:block;margin-bottom:3px;}
.cnm{font-size:7px;font-weight:700;letter-spacing:1px;font-family:'Share Tech Mono',monospace;}
.ctp{font-size:6px;color:rgba(255,255,255,.28);margin-top:1px;}
.cbars{margin-top:5px;display:flex;flex-direction:column;gap:2px;}
.cbr{display:flex;align-items:center;gap:2px;}
.cbl{font-size:5px;color:rgba(255,255,255,.28);width:14px;text-align:right;font-family:'Share Tech Mono',monospace;}
.cbt{flex:1;height:3px;background:rgba(255,255,255,.05);border-radius:99px;overflow:hidden;}
.cbf{height:100%;border-radius:99px;}
.sbtn{display:inline-block;padding:12px 34px;background:rgba(0,255,200,.09);border:1px solid rgba(0,255,200,.4);border-radius:12px;font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;color:#00ffcc;cursor:pointer;letter-spacing:2px;transition:all .18s;}
.sbtn:hover{background:rgba(0,255,200,.2);transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,255,200,.22);}
.s2btn{display:inline-block;margin-top:9px;padding:8px 20px;border:1px solid rgba(255,255,255,.09);border-radius:9px;font-size:10px;color:rgba(255,255,255,.28);cursor:pointer;transition:all .18s;font-family:'Share Tech Mono',monospace;}
.s2btn:hover{border-color:rgba(255,255,255,.22);color:rgba(255,255,255,.5);}
.statsrow{display:flex;gap:7px;justify-content:center;margin-bottom:16px;}
.sbox{padding:8px 12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:9px;text-align:center;min-width:68px;}
.snum{font-family:'Orbitron',sans-serif;font-size:15px;font-weight:700;line-height:1;}
.slbl{font-size:6px;color:rgba(255,255,255,.24);letter-spacing:2px;margin-top:3px;font-family:'Share Tech Mono',monospace;}
.brow{font-size:8px;color:rgba(255,255,255,.22);margin-bottom:14px;font-family:'Share Tech Mono',monospace;}
.bnum{color:#ff8800;font-family:'Orbitron',sans-serif;}
.instrow{font-size:8px;color:rgba(255,255,255,.18);line-height:2.2;margin-bottom:14px;font-family:'Share Tech Mono',monospace;}

#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,0.82);backdrop-filter:blur(4px);display:flex;justify-content:center;align-items:center;gap:16px;padding:5px 12px;font-size:10px;color:#778;letter-spacing:1px;flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,0.06);}
#ctrl-bar span{color:#aab;}
#ctrl-bar b{color:#00ffcc;font-weight:700;}
</style>
</head>
<body>
  <div id="ctrl-bar">
    <span><b>← →</b> / <b>A D</b> 방향 전환</span>
    <span>|</span>
    <span><b>Space / Shift</b> 부스터(니트로)</span>
    <span>|</span>
    <span>장애물 피해 달려라!</span>
  </div>
<div id="wrap">
  <canvas id="gc"></canvas>
  <div id="ui">
    <!-- HUD -->
    <div id="hud">
      <div class="hp"><div class="hv" id="sv">0</div><div class="hl">SCORE</div></div>
      <div class="hp"><div class="hv" id="wv">1</div><div class="hl">WAVE</div></div>
      <div id="wp">
        <div class="hp" style="padding:4px 8px;">
          <div id="stars-row"><span class="st" id="s0">★</span><span class="st" id="s1">★</span><span class="st" id="s2">★</span><span class="st" id="s3">★</span><span class="st" id="s4">★</span></div>
          <div id="lives"></div>
          <div class="hl" style="margin-top:1px;">WANTED</div>
        </div>
      </div>
      <div class="hp"><div class="hv" id="dv">0.0</div><div class="hl">KM</div></div>
    </div>

    <!-- Nitro bar -->
    <div id="nb-wrap">
      <div id="nb-lbl">NITRO</div>
      <div id="nb-bg"><div id="nb-fill" style="width:100%"></div></div>
    </div>

    <!-- Combo / Banner -->
    <div id="combo-pop"></div>
    <div id="banner"></div>

    <!-- Controls -->
    <div id="ctrl" style="pointer-events:all;">
      <div style="display:flex;gap:10px;">
        <div class="cbtn" id="bl">◀<span class="clbl">LEFT</span></div>
        <div class="cbtn" id="br">▶<span class="clbl">RIGHT</span></div>
      </div>
      <div class="cbtn" id="nbtn">⚡<span class="clbl">NITRO</span></div>
    </div>

    <!-- Overlay -->
    <div id="ov" style="pointer-events:all;"><div id="oi"></div></div>
  </div>
</div>

<script>
'use strict';
// ═══════════════════════════════════════════════════════
//  CANVAS
// ═══════════════════════════════════════════════════════
const gc  = document.getElementById('gc');
const ctx = gc.getContext('2d');
const ui  = document.getElementById('ui');

const BW = 420, BH = 740;
let scale = 1;

function resize() {
  const rw = innerWidth||760, rh = innerHeight||560;
  scale = Math.min(rw/BW, rh/BH);
  gc.width  = BW; gc.height = BH;
  const pw = BW*scale, ph = BH*scale;
  gc.style.cssText  = `position:absolute;left:${(rw-pw)/2}px;top:${(rh-ph)/2}px;width:${pw}px;height:${ph}px;`;
  ui.style.cssText  = `position:absolute;left:${(rw-pw)/2}px;top:${(rh-ph)/2}px;width:${pw}px;height:${ph}px;pointer-events:none;`;
}
resize(); addEventListener('resize', resize);
setTimeout(resize,100);setTimeout(resize,500);

// ═══════════════════════════════════════════════════════
//  DATA
// ═══════════════════════════════════════════════════════
const CARS = [
  {name:'SPORT',  em:'🚗', tp:'균형형',  spd:1.0,  hp:3, acc:1.0,  col:'#00ffcc', s:70,h:55,a:65},
  {name:'HYPER',  em:'🏎️', tp:'극한속도', spd:1.45, hp:2, acc:1.25, col:'#ff2255', s:96,h:28,a:88},
  {name:'SUV',    em:'🚙', tp:'탱크형',  spd:0.72, hp:5, acc:0.65, col:'#44ff88', s:42,h:95,a:38},
  {name:'MUSCLE', em:'🚘', tp:'가속형',  spd:1.15, hp:3, acc:1.55, col:'#ffaa00', s:80,h:58,a:98},
];

// Traffic: each has pixel-art style, rendered as canvas shapes
const TDEFS = [
  {col:'#e87040', col2:'#b04020', w:52, h:88, pts:20, spd:2.2, cop:false, type:'sedan'},
  {col:'#4488cc', col2:'#224466', w:58, h:110,pts:35, spd:1.5, cop:false, type:'truck'},
  {col:'#2244dd', col2:'#1122aa', w:52, h:88, pts:12, spd:5.0, cop:true,  type:'cop'},
  {col:'#cc3355', col2:'#882233', w:48, h:80, pts:18, spd:3.6, cop:false, type:'sedan'},
  {col:'#22bb66', col2:'#116633', w:54, h:92, pts:25, spd:2.8, cop:false, type:'sedan'},
  {col:'#ddaa00', col2:'#997700', w:60, h:120,pts:40, spd:1.2, cop:false, type:'truck'},
  {col:'#aa44cc', col2:'#662288', w:50, h:84, pts:22, spd:3.2, cop:false, type:'sedan'},
  {col:'#cc2222', col2:'#881111', w:52, h:88, pts:28, spd:4.0, cop:false, type:'sedan'},
];

const PWRDEFS = [
  {em:'⚡', tp:'nitro',  col:'#00ffcc', lbl:'NITRO +80%',   r:.25},
  {em:'⭐', tp:'score',  col:'#ffaa00', lbl:'+1000 BONUS',  r:.15},
  {em:'💊', tp:'heal',   col:'#44ff88', lbl:'HP RESTORED',  r:.18},
  {em:'🔱', tp:'shield', col:'#cc44ff', lbl:'SHIELD 5S',    r:.12},
  {em:'💨', tp:'boost',  col:'#88ddff', lbl:'SPEED BOOST',  r:.15},
  {em:'🧲', tp:'magnet', col:'#ff8844', lbl:'MAGNET 8S',    r:.10},
  {em:'💣', tp:'bomb',   col:'#ff4422', lbl:'KABOOM!',      r:.05},
];

// Road layout — TOP-DOWN view
// 5 lanes, each ~64px wide, centered in BW=420
const LANE_COUNT = 5;
const LANE_W     = 68;
const ROAD_W     = LANE_COUNT * LANE_W;          // 340
const ROAD_X     = (BW - ROAD_W) / 2;           // 40
const LANE_CX    = Array.from({length:LANE_COUNT},(_,i)=>ROAD_X + i*LANE_W + LANE_W/2);

// Player sits at fixed Y near bottom
const PLAYER_Y   = BH - 140;
// Enemies spawn at Y = -150, travel down to BH + 150
const SPAWN_Y    = -150;
const KILL_Y     = BH + 160;

// ═══════════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════════
let selCar = 0;
let G={}, raf=null, floats=[], particles=[], uid=0;
let lastL=false, lastR=false;

// ── 고스트 레이싱 ───────────────────────────────────────
const GHOST_KEY = 'neon_ghost_v1';
let ghostFrames = [];    // 녹화 버퍼 (현재 판)
let ghostBest   = null;  // localStorage에서 불러온 최고기록 고스트
let ghostX = 0, ghostAlpha = 0;

function ghostSave(){
  if(!ghostFrames.length) return;
  try{ localStorage.setItem(GHOST_KEY, JSON.stringify({frames: ghostFrames, score: G.score, dist: G.dist.toFixed(1)})); }catch(e){}
}

function ghostLoad(){
  try{
    const raw = localStorage.getItem(GHOST_KEY);
    if(raw){ ghostBest = JSON.parse(raw); return; }
  }catch(e){}
  ghostBest = null;
}

function ghostRecord(){
  ghostFrames.push(G.laneX);
}

function ghostDraw(ctx, frame){
  if(!ghostBest || !ghostBest.frames || !ghostBest.frames.length) return;
  const gx = ghostBest.frames[Math.min(frame, ghostBest.frames.length-1)];
  ghostX += (gx - ghostX) * 0.35;
  const car = CARS[selCar];
  const cx = gc.width/2, cy = gc.height, ch = cy;
  const carH = 72, carW = 32;
  const PLAYER_Y = ch * 0.75;
  ctx.save();
  ctx.globalAlpha = 0.38 + Math.sin(G.frame*.1)*.08;
  // Ghost outline
  ctx.strokeStyle = '#00ffff';
  ctx.lineWidth = 2;
  ctx.shadowColor = '#00ffff';
  ctx.shadowBlur = 16;
  ctx.beginPath();
  ctx.roundRect ? ctx.roundRect(ghostX - carW/2, PLAYER_Y - carH/2, carW, carH, 6)
    : ctx.rect(ghostX - carW/2, PLAYER_Y - carH/2, carW, carH);
  ctx.stroke();
  ctx.globalAlpha = 0.12;
  ctx.fillStyle = '#00ffff';
  ctx.fill();
  ctx.globalAlpha = 0.7;
  ctx.fillStyle = '#00ffff';
  ctx.font = 'bold 9px Orbitron,sans-serif';
  ctx.textAlign = 'center';
  ctx.fillText('GHOST', ghostX, PLAYER_Y - carH/2 - 5);
  ctx.restore();
}

function initGame(){
  const car = CARS[selCar];
  ghostFrames = [];
  ghostLoad();
  G = {
    run:true, dead:false, frame:0,
    score:0, dist:0,
    lane:2, laneX: LANE_CX[2], targetX: LANE_CX[2],
    laneMoving:false, laneDir:0,
    speed:0, baseSpd: 420*car.spd, maxSpd: 980*car.spd,
    nitro:100, nitroOn:false,
    hp:car.hp, maxHp:car.hp,
    shieldT:0, boostT:0, magnetT:0, flashT:0,
    combo:1, comboD:0, maxCombo:1,
    wanted:0, wantedCool:0,
    wave:1, waveKills:0, waveTarget:7,
    totalKills:0,
    traffic:[], powers:[],
    spawnT:0, pwrT:0,
    roadY:0,          // scrolling road offset
    bgY:0,            // city bg offset (parallax)
    _tL:false, _tR:false, _tN:false,
    _swL:false, _swR:false,
    // road markings state
    dashOff:0,
    // screen shake
    shake:0, shakeX:0, shakeY:0,
  };
  floats=[]; particles=[];
  buildLives(); updWanted();
  // Pre-spawn traffic spread out
  for(let i=0;i<5;i++) spawnTraffic(-(i+1)*160 - Math.random()*100);
  spawnPwr(-300);
}

// ═══════════════════════════════════════════════════════
//  SPAWN
// ═══════════════════════════════════════════════════════
let spawnUID = 0;
function spawnTraffic(y){
  const pool = TDEFS.filter(d=>!d.cop||G.wanted>=2);
  const def  = pool[Math.floor(Math.random()*pool.length)];
  // Avoid spawning on same lane as nearby traffic
  const usedLanes = G.traffic.filter(t=>t.y<100&&t.y>-200).map(t=>t.lane);
  const freeLanes = Array.from({length:LANE_COUNT},(_,i)=>i).filter(l=>!usedLanes.includes(l));
  const lane = freeLanes.length ? freeLanes[Math.floor(Math.random()*freeLanes.length)] : Math.floor(Math.random()*LANE_COUNT);
  G.traffic.push({
    id:spawnUID++, lane,
    x: LANE_CX[lane],
    y: y !== undefined ? y : SPAWN_Y - Math.random()*80,
    spd: def.spd * (0.85+Math.random()*0.3),
    col:def.col, col2:def.col2, w:def.w, h:def.h,
    pts:def.pts, cop:def.cop, type:def.type,
    alive:true, scored:false,
    siren:0, sirenT:0,
    wobble:0, wobbleV:(Math.random()-.5)*0.4,
    hit:0, // flash timer on collect
  });
}

function spawnPwr(y){
  const r=Math.random(); let acc=0, def=PWRDEFS[0];
  for(const p of PWRDEFS){acc+=p.r; if(r<=acc){def=p;break;}}
  const lane=Math.floor(Math.random()*LANE_COUNT);
  G.powers.push({
    lane, x:LANE_CX[lane],
    y: y!==undefined ? y : SPAWN_Y - Math.random()*60,
    tp:def.tp, em:def.em, col:def.col, lbl:def.lbl,
    alive:true, rot:0, pulse:0,
  });
}

// ═══════════════════════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════════════════════
function spawnFloat(txt,col,x,y){
  floats.push({txt,col, x:x||BW/2, y:y||PLAYER_Y-60, vy:-2.8, life:1.0});
}
function spawnParts(x,y,col,n){
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2, s=1.5+Math.random()*5;
    particles.push({x,y, vx:Math.cos(a)*s, vy:Math.sin(a)*s-2,
      col, life:0.7+Math.random()*.5, size:2+Math.random()*4});
  }
}

function buildLives(){
  const r=document.getElementById('lives'); r.innerHTML='';
  for(let i=0;i<G.maxHp;i++){
    const d=document.createElement('div');
    d.className='lp'+(i>=G.hp?' x':''); d.id='lp'+i;
    r.appendChild(d);
  }
}
function updLives(){
  for(let i=0;i<G.maxHp;i++){
    const e=document.getElementById('lp'+i);
    if(e) e.className='lp'+(i>=G.hp?' x':'');
  }
}
function updWanted(){
  for(let i=0;i<5;i++){
    const e=document.getElementById('s'+i);
    if(e) e.classList.toggle('on',i<G.wanted);
  }
}

let banTimer=null;
function showBanner(txt,col){
  const el=document.getElementById('banner');
  if(!el)return;
  el.textContent=txt; el.style.color=col;
  el.style.textShadow=`0 0 20px ${col}, 0 0 40px ${col}66`;
  el.style.opacity='1';
  clearTimeout(banTimer);
  banTimer=setTimeout(()=>{ if(el)el.style.opacity='0'; },1500);
}
function showCombo(n){
  const el=document.getElementById('combo-pop');
  el.textContent='×'+n+' COMBO!';
  el.style.opacity='1';
  el.style.fontSize=Math.min(42,26+n*2)+'px';
  setTimeout(()=>el.style.opacity='0', 850);
}

// ═══════════════════════════════════════════════════════
//  UPDATE
// ═══════════════════════════════════════════════════════
function update(){
  if(!G.run||G.dead) return;
  G.frame++;
  ghostRecord();

  const L = KEYS.ArrowLeft||KEYS.KeyA||G._tL||G._swL;
  const R = KEYS.ArrowRight||KEYS.KeyD||G._tR||G._swR;
  const N = KEYS.Space||KEYS.ShiftLeft||KEYS.ShiftRight||G._tN;
  G._swL=false; G._swR=false;

  // Lane switch — only when not already moving
  const car=CARS[selCar];
  const slip = G._slipFactor !== undefined ? G._slipFactor : 1.0;
  if(L&&!lastL&&!G.laneMoving&&Math.random()<slip){
    if(G.lane>0){G.lane--; G.targetX=LANE_CX[G.lane]; G.laneMoving=true; G.laneDir=-1;}
    else showBanner('WALL!','#ff2255');
  } else if(L&&!lastL&&Math.random()>=slip){ showBanner('🌧️ 미끄러짐!','#44aaff'); }
  if(R&&!lastR&&!G.laneMoving&&Math.random()<slip){
    if(G.lane<LANE_COUNT-1){G.lane++; G.targetX=LANE_CX[G.lane]; G.laneMoving=true; G.laneDir=1;}
    else showBanner('WALL!','#ff2255');
  } else if(R&&!lastR&&Math.random()>=slip){ showBanner('🌧️ 미끄러짐!','#44aaff'); }
  lastL=L; lastR=R;

  // Smooth lane slide
  const laneSpd = 14 + car.acc*6;
  if(G.laneMoving){
    const dx = G.targetX - G.laneX;
    if(Math.abs(dx)<2){ G.laneX=G.targetX; G.laneMoving=false; }
    else { G.laneX += dx * 0.22; }
  }

  // Nitro
  if(N&&G.nitro>0){ G.nitroOn=true; G.nitro=Math.max(0,G.nitro-0.7); }
  else { G.nitroOn=false; G.nitro=Math.min(100,G.nitro+0.3); }

  // Speed (px/s equivalent; we multiply by dt=1/60 in movement)
  const nitroM = G.nitroOn?2.0:(G.boostT>0?1.5:1);
  const tSpd   = G.baseSpd * nitroM;
  G.speed += (tSpd-G.speed)*(0.04+car.acc*0.015);

  // Timers
  if(G.shieldT>0) G.shieldT-=1/60;
  if(G.boostT>0)  G.boostT -=1/60;
  if(G.magnetT>0) G.magnetT-=1/60;
  if(G.flashT>0)  G.flashT -=0.08;
  if(G.shake>0)   G.shake  -=0.12;
  if(G.comboD>0)  G.comboD--;
  else if(G.combo>1){G.combo=Math.max(1,G.combo-1);G.comboD=100;}
  if(G.wantedCool>0) G.wantedCool--;
  else if(G.wanted>0&&G.frame%380===0){G.wanted=Math.max(0,G.wanted-1);updWanted();}

  // Road scroll
  const dt = 1/60;
  G.roadY  = (G.roadY + G.speed*dt*0.55) % 120;   // dash marks
  G.dashOff= (G.dashOff + G.speed*dt*0.55) % 120;
  G.bgY    = (G.bgY + G.speed*dt*0.12) % BH;       // parallax bg
  G.dist  += G.speed * dt * 0.00028;

  // ── 날씨/노면 환경 변화 ──────────────────────────────
  if(!G.weatherTimer) G.weatherTimer = 0;
  G.weatherTimer += dt;
  // 매 30초마다 날씨 전환
  if(G.weatherTimer > 30) {
    G.weatherTimer = 0;
    const weathers = ['clear','rain','fog'];
    const cur = G.weather || 'clear';
    const next = weathers.filter(w=>w!==cur)[Math.floor(Math.random()*(weathers.length-1))];
    G.weather = next;
    if(next==='rain') showBanner('🌧️ 빗길! 미끄러움 주의','#44aaff');
    else if(next==='fog') showBanner('🌫️ 안개 발생! 시야 제한','#aabbcc');
    else showBanner('☀️ 날씨 맑음','#ffdd44');
  }
  // 빗길 미끄러짐 효과: 조작 입력 일부 흡수
  G._slipFactor = (G.weather==='rain') ? 0.65 : 1.0;
  // 빗방울 파티클
  if(G.weather==='rain' && Math.random()<0.4) {
    const rx = Math.random()*BW;
    particles.push({x:rx,y:0,vx:-1,vy:18+Math.random()*8,life:1,col:'rgba(100,180,255,0.55)',sz:1.5,isRain:true});
  }

  // Move traffic (they travel DOWN the screen toward player)
  for(const tc of G.traffic){
    if(!tc.alive) continue;
    tc.wobble += tc.wobbleV * 0.05;
    if(Math.abs(tc.wobble)>3) tc.wobbleV*=-1;
    // Relative speed: player_speed - traffic_speed gives scroll rate
    const relSpd = G.speed - tc.spd*60;
    tc.y += relSpd * dt * 0.55;
    if(tc.cop) tc.sirenT=(tc.sirenT+1)%60;

    // Collision: car rect vs player rect
    if(!tc.scored){
      const px=G.laneX, py=PLAYER_Y;
      const pw=54, ph=80;
      const tx=tc.x, ty=tc.y;
      const overlapX = Math.abs(px-tx) < (pw+tc.w)*0.38;
      const overlapY = Math.abs(py-ty) < (ph+tc.h)*0.32;
      if(overlapX&&overlapY){
        if(G.shieldT>0){
          tc.alive=false;
          spawnParts(tx,ty,'#cc44ff',20);
          spawnFloat('BLOCKED! +200',  '#cc44ff',tx,ty);
          G.score+=200;
        } else {
          G.hp--; G.flashT=1.5; G.shake=1;
          G.speed*=0.3; G.combo=1; G.comboD=0;
          tc.alive=false;
          spawnParts(px,py,'#ff2255',35);
          updLives(); showBanner('CRASH! 💥','#ff2255');
          if(G.hp<=0){G.dead=true; setTimeout(showGameOver,900);}
        }
        continue;
      }
    }

    // Passed player (went below screen) → score
    if(!tc.scored&&tc.y>KILL_Y){
      tc.scored=true;
      const pts=tc.pts*G.combo;
      G.score+=pts;
      G.combo=Math.min(12,G.combo+1);
      G.maxCombo=Math.max(G.maxCombo,G.combo);
      G.comboD=140; G.waveKills++; G.totalKills++;
      spawnFloat('+'+pts, G.combo>=4?'#ffaa00':'#00ffcc', tc.x, tc.y-30);
      if(tc.cop){G.wanted=Math.min(5,G.wanted+1);G.wantedCool=700;updWanted();}
      if(G.combo>=4) showCombo(G.combo);
      if(G.combo>=4) showBanner('×'+G.combo+' COMBO!','#ffaa00');
      if(G.waveKills>=G.waveTarget){
        G.wave++; G.waveKills=0; G.waveTarget=Math.min(20,G.waveTarget+2);
        G.baseSpd=Math.min(G.maxSpd, G.baseSpd*1.09);
        G.score+=G.wave*500;
        showBanner('WAVE '+G.wave+' CLEAR! 🔥','#ffaa00');
        spawnParts(BW/2,BH/2,'#ffaa00',50);
        spawnFloat('WAVE '+G.wave+' BONUS +'+G.wave*500,'#ffaa00');
      }
    }
    if(tc.y>KILL_Y+50) tc.alive=false;
  }
  G.traffic=G.traffic.filter(t=>t.alive);
  if(G.traffic.length>30) G.traffic.splice(0,6);

  // Spawn timer (frame-based)
  G.spawnT++;
  const spawnRate = Math.max(28, 110 - G.speed*0.04 - G.wave*5);
  if(G.spawnT>=spawnRate){ G.spawnT=0; spawnTraffic(); if(G.wanted>=3) spawnTraffic(); }

  // Power-ups
  for(const pw of G.powers){
    if(!pw.alive) continue;
    pw.rot+=0.08; pw.pulse=(pw.pulse+0.09)%(Math.PI*2);
    pw.y += (G.speed-140)*dt*0.55;
    // Magnet pull
    if(G.magnetT>0){
      const dx=G.laneX-pw.x;
      if(Math.abs(dx)<200) pw.x+=dx*0.06;
    }
    // Collect
    if(Math.abs(pw.x-G.laneX)<44&&Math.abs(pw.y-PLAYER_Y)<60){
      pw.alive=false;
      spawnParts(pw.x,pw.y,pw.col,18);
      spawnFloat(pw.lbl,pw.col,pw.x,pw.y);
      if(pw.tp==='nitro')  G.nitro=Math.min(100,G.nitro+80);
      if(pw.tp==='score')  G.score+=1000*G.combo;
      if(pw.tp==='heal')   {G.hp=Math.min(G.maxHp,G.hp+1);updLives();}
      if(pw.tp==='shield') G.shieldT=5;
      if(pw.tp==='boost')  G.boostT=6;
      if(pw.tp==='magnet') G.magnetT=8;
      if(pw.tp==='bomb'){
        const n=G.traffic.length;
        G.traffic.forEach(t=>{spawnParts(t.x,t.y,'#ff4422',12);t.alive=false;});
        G.score+=n*80;
        showBanner('💣 KABOOM! ALL CLEAR!','#ff4422');
        spawnFloat('+'+n*80+' BONUS','#ff4422');
      }
    }
    if(pw.y>KILL_Y) pw.alive=false;
  }
  G.powers=G.powers.filter(p=>p.alive);
  G.pwrT++;
  if(G.pwrT>=Math.max(180,320-G.wave*12)){G.pwrT=0;spawnPwr();}

  // Particles & floats
  for(let i=particles.length-1;i>=0;i--){
    const p=particles[i];
    p.x+=p.vx; p.y+=p.vy; p.vy+=0.15;
    p.life-=0.032; p.size*=0.97;
    if(p.life<=0)particles.splice(i,1);
  }
  for(let i=floats.length-1;i>=0;i--){
    const f=floats[i];
    f.y+=f.vy; f.vy*=0.95; f.life-=0.024;
    if(f.life<=0)floats.splice(i,1);
  }

  // Passive score
  if(G.frame%5===0) G.score+=Math.floor(G.speed*G.combo*0.0008);

  // DOM
  const sv=document.getElementById('sv');
  const wv=document.getElementById('wv');
  const dv=document.getElementById('dv');
  const nf=document.getElementById('nb-fill');
  if(sv) sv.textContent=G.score.toLocaleString();
  if(wv) wv.textContent=G.wave;
  if(dv) dv.textContent=G.dist.toFixed(1);
  if(nf) nf.style.width=G.nitro+'%';
}

// ═══════════════════════════════════════════════════════
//  DRAW: pixel-art style car
// ═══════════════════════════════════════════════════════
function drawCar(x, y, w, h, body, roof, isPlayer, siren, sirenT, tilt){
  ctx.save();
  ctx.translate(x, y);
  if(tilt) ctx.rotate(tilt*Math.PI/180);

  const hw=w/2, hh=h/2;

  if(!isPlayer){
    // Shadow
    ctx.save(); ctx.globalAlpha=0.18;
    ctx.fillStyle='#000';
    ctx.beginPath(); ctx.ellipse(0, hh*0.85, hw*0.85, hh*0.22, 0,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }

  // Body
  ctx.fillStyle=body;
  roundRect(ctx,-hw,-hh,w,h,8); ctx.fill();

  // Roof highlight
  ctx.fillStyle=roof;
  roundRect(ctx,-hw*0.6,-hh*0.7,w*0.6,h*0.38,5); ctx.fill();

  // Windshield
  ctx.fillStyle='rgba(150,220,255,0.55)';
  roundRect(ctx,-hw*0.5, isPlayer?-hh*0.55:-hh*0.15, w*0.5, h*0.22, 4); ctx.fill();

  // Rear window (for traffic, facing up)
  if(!isPlayer){
    ctx.fillStyle='rgba(120,180,220,0.45)';
    roundRect(ctx,-hw*0.45, hh*0.1, w*0.45, h*0.18, 3); ctx.fill();
  }

  // Wheels
  ctx.fillStyle='#1a1a1a';
  [[-1,-1],[1,-1],[-1,1],[1,1]].forEach(([sx,sy])=>{
    ctx.save();
    ctx.translate(sx*(hw-3), sy*(hh-10));
    roundRect(ctx,-7,-10,14,18,3); ctx.fill();
    ctx.fillStyle='#888';
    roundRect(ctx,-4,-7,8,12,2); ctx.fill();
    ctx.restore();
  });

  // Headlights / taillights
  if(isPlayer){
    // Headlights (front = top)
    ctx.fillStyle='rgba(255,255,200,0.95)';
    [[-1,1],[1,1]].forEach(([sx])=>{
      ctx.save(); ctx.translate(sx*(hw-8),-hh+2);
      ctx.shadowColor='rgba(255,255,150,.8)'; ctx.shadowBlur=10;
      roundRect(ctx,-6,-4,12,8,3); ctx.fill();
      ctx.restore();
    });
    // Taillights
    ctx.fillStyle='rgba(255,50,50,0.9)';
    [[-1,1],[1,1]].forEach(([sx])=>{
      ctx.save(); ctx.translate(sx*(hw-8),hh-2);
      roundRect(ctx,-6,-4,12,7,3); ctx.fill();
      ctx.restore();
    });
  } else {
    // Traffic taillights (facing toward player = bottom)
    ctx.fillStyle='rgba(255,60,60,0.9)';
    [[-1],[1]].forEach(([sx])=>{
      ctx.save(); ctx.translate(sx*(hw-8), hh-2);
      roundRect(ctx,-6,-4,12,7,3); ctx.fill();
      ctx.restore();
    });
    // Headlights (top — faint)
    ctx.fillStyle='rgba(255,250,180,0.7)';
    [[-1],[1]].forEach(([sx])=>{
      ctx.save(); ctx.translate(sx*(hw-8),-hh+2);
      roundRect(ctx,-5,-3,10,6,3); ctx.fill();
      ctx.restore();
    });
  }

  // Cop siren lights
  if(siren&&sirenT!==undefined){
    const flash = Math.floor(sirenT/8)%2===0;
    ctx.save();
    ctx.shadowBlur=20;
    ctx.fillStyle=flash?'rgba(60,100,255,0.95)':'rgba(255,40,40,0.95)';
    ctx.shadowColor=flash?'#4466ff':'#ff2222';
    roundRect(ctx,-14,-hh+4,12,10,3); ctx.fill();
    ctx.fillStyle=flash?'rgba(255,40,40,0.95)':'rgba(60,100,255,0.95)';
    ctx.shadowColor=flash?'#ff2222':'#4466ff';
    roundRect(ctx,2,-hh+4,12,10,3); ctx.fill();
    ctx.restore();
  }

  ctx.restore();
}

function roundRect(c,x,y,w,h,r){
  c.beginPath();
  c.moveTo(x+r,y);
  c.lineTo(x+w-r,y); c.arcTo(x+w,y,x+w,y+r,r);
  c.lineTo(x+w,y+h-r); c.arcTo(x+w,y+h,x+w-r,y+h,r);
  c.lineTo(x+r,y+h); c.arcTo(x,y+h,x,y+h-r,r);
  c.lineTo(x,y+r); c.arcTo(x,y,x+r,y,r);
  c.closePath();
}

// ═══════════════════════════════════════════════════════
//  DRAW: road segment
// ═══════════════════════════════════════════════════════
function drawRoad(){
  // Asphalt base
  ctx.fillStyle='#131820';
  ctx.fillRect(ROAD_X, 0, ROAD_W, BH);

  // Subtle road texture strips
  for(let i=0;i<LANE_COUNT;i++){
    const lx=ROAD_X+i*LANE_W;
    const grad=ctx.createLinearGradient(lx,0,lx+LANE_W,0);
    grad.addColorStop(0,'rgba(0,0,0,0.15)');
    grad.addColorStop(0.5,'rgba(255,255,255,0.01)');
    grad.addColorStop(1,'rgba(0,0,0,0.15)');
    ctx.fillStyle=grad;
    ctx.fillRect(lx,0,LANE_W,BH);
  }

  // Road edge glow
  ctx.save();
  const edgeGrad=ctx.createLinearGradient(ROAD_X-20,0,ROAD_X+20,0);
  edgeGrad.addColorStop(0,'transparent');
  edgeGrad.addColorStop(1,'rgba(0,255,180,0.3)');
  ctx.fillStyle=edgeGrad; ctx.fillRect(ROAD_X-20,0,40,BH);
  const edgeGrad2=ctx.createLinearGradient(ROAD_X+ROAD_W-20,0,ROAD_X+ROAD_W+20,0);
  edgeGrad2.addColorStop(0,'rgba(0,255,180,0.3)');
  edgeGrad2.addColorStop(1,'transparent');
  ctx.fillStyle=edgeGrad2; ctx.fillRect(ROAD_X+ROAD_W-20,0,40,BH);
  ctx.restore();

  // Road borders
  ctx.save();
  ctx.strokeStyle='rgba(0,255,180,0.7)'; ctx.lineWidth=3;
  ctx.shadowColor='#00ffcc'; ctx.shadowBlur=12;
  ctx.beginPath(); ctx.moveTo(ROAD_X,0); ctx.lineTo(ROAD_X,BH); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(ROAD_X+ROAD_W,0); ctx.lineTo(ROAD_X+ROAD_W,BH); ctx.stroke();
  ctx.restore();

  // Sidewalk
  ctx.fillStyle='#0d1018';
  ctx.fillRect(0,0,ROAD_X,BH);
  ctx.fillRect(ROAD_X+ROAD_W,0,BW-ROAD_X-ROAD_W,BH);

  // Pavement markings on sidewalk
  ctx.save();
  ctx.strokeStyle='rgba(255,255,255,0.04)'; ctx.lineWidth=1;
  for(let y=-G.dashOff%40;y<BH;y+=40){
    ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(ROAD_X-2,y); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(ROAD_X+ROAD_W+2,y); ctx.lineTo(BW,y); ctx.stroke();
  }
  ctx.restore();

  // Lane dividers — dashed white
  ctx.save();
  ctx.strokeStyle='rgba(255,255,255,0.22)'; ctx.lineWidth=2;
  ctx.setLineDash([32,28]);
  for(let l=1;l<LANE_COUNT;l++){
    const lx=ROAD_X+l*LANE_W;
    ctx.lineDashOffset=-G.dashOff;
    ctx.beginPath(); ctx.moveTo(lx,0); ctx.lineTo(lx,BH); ctx.stroke();
  }
  ctx.setLineDash([]);
  ctx.restore();

  // Rumble strips (road edges, alternating colors)
  const stripW=12;
  const stripCount=Math.ceil(BH/20)+1;
  for(let i=0;i<stripCount;i++){
    const y=((i*20)-G.dashOff%20)-20;
    const even=Math.floor(i)%2===0;
    ctx.fillStyle=even?'rgba(255,40,60,0.65)':'rgba(240,240,240,0.45)';
    ctx.fillRect(ROAD_X-stripW, y, stripW, 20);
    ctx.fillRect(ROAD_X+ROAD_W, y, stripW, 20);
  }

  // Road shine/reflection
  const shine=ctx.createLinearGradient(ROAD_X,0,ROAD_X+ROAD_W,0);
  shine.addColorStop(0,'transparent');
  shine.addColorStop(0.15,'rgba(255,255,255,0.01)');
  shine.addColorStop(0.5,'rgba(255,255,255,0.025)');
  shine.addColorStop(0.85,'rgba(255,255,255,0.01)');
  shine.addColorStop(1,'transparent');
  ctx.fillStyle=shine; ctx.fillRect(ROAD_X,0,ROAD_W,BH);
}

// ═══════════════════════════════════════════════════════
//  DRAW: city background
// ═══════════════════════════════════════════════════════
const CITY_BUILDINGS = Array.from({length:28},(_,i)=>{
  const side = i%2;
  const slot  = Math.floor(i/2);
  const baseX = side===0 ? slot*(ROAD_X/12) : ROAD_X+ROAD_W+slot*((BW-ROAD_X-ROAD_W)/12);
  return {
    x: baseX + Math.random()*10-5,
    w: 24+Math.random()*22,
    h: 80+Math.random()*200,
    col: `hsl(${210+Math.random()*40},${20+Math.random()*20}%,${6+Math.random()*6}%)`,
    windows: Array.from({length:20},()=>Math.random()>0.45),
    winC: `hsl(${30+Math.random()*40},${60+Math.random()*30}%,${65+Math.random()*20}%)`,
  };
});

function drawCity(){
  // Sky gradient
  const sky=ctx.createLinearGradient(0,0,0,BH*0.3);
  sky.addColorStop(0,'#010208');
  sky.addColorStop(1,'#040c1a');
  ctx.fillStyle=sky;
  ctx.fillRect(0,0,BW,BH*0.3);

  // Distant glow
  const glow=ctx.createRadialGradient(BW/2,BH*0.05,0,BW/2,BH*0.05,BW*0.7);
  glow.addColorStop(0,'rgba(0,100,180,0.12)');
  glow.addColorStop(1,'transparent');
  ctx.fillStyle=glow; ctx.fillRect(0,0,BW,BH*0.3);

  // Ground fill for sides (dark)
  ctx.fillStyle='#0a0e14';
  ctx.fillRect(0,0,ROAD_X,BH);
  ctx.fillRect(ROAD_X+ROAD_W,0,BW-ROAD_X-ROAD_W,BH);

  // Scrolling city buildings on sides
  for(const b of CITY_BUILDINGS){
    const scrolledY = -b.h + (G.bgY % (b.h+BH*0.2));
    ctx.fillStyle=b.col;
    ctx.fillRect(b.x, scrolledY, b.w, b.h);
    // Windows
    const cols=Math.floor(b.w/8), rows=Math.floor(b.h/12);
    for(let row=0;row<rows;row++) for(let col=0;col<cols;col++){
      if(b.windows[(row*cols+col)%b.windows.length]){
        ctx.fillStyle=b.winC;
        ctx.globalAlpha=0.55+Math.random()*0.1;
        ctx.fillRect(b.x+2+col*8, scrolledY+4+row*12, 5, 7);
        ctx.globalAlpha=1;
      }
    }
  }
}

// ═══════════════════════════════════════════════════════
//  RENDER
// ═══════════════════════════════════════════════════════
function render(){
  ctx.clearRect(0,0,BW,BH);

  // Screen shake
  if(G.shake>0){
    G.shakeX=(Math.random()-.5)*G.shake*12;
    G.shakeY=(Math.random()-.5)*G.shake*8;
    ctx.save(); ctx.translate(G.shakeX,G.shakeY);
  }

  drawCity();
  drawRoad();

  // Power-ups (before traffic)
  for(const pw of G.powers){
    if(!pw.alive) continue;
    const bob=Math.sin(pw.pulse)*5;
    const sz=Math.max(24,36-Math.abs(pw.y-PLAYER_Y)*0.04);

    // Glow ring
    ctx.save();
    ctx.beginPath(); ctx.arc(pw.x,pw.y+bob,sz*0.75,0,Math.PI*2);
    ctx.strokeStyle=pw.col; ctx.lineWidth=2;
    ctx.globalAlpha=0.35+Math.sin(pw.pulse)*0.2; ctx.shadowColor=pw.col; ctx.shadowBlur=16;
    ctx.stroke(); ctx.restore();

    // Emoji
    ctx.save();
    ctx.translate(pw.x, pw.y+bob); ctx.rotate(pw.rot);
    ctx.font=sz+'px serif'; ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.shadowColor=pw.col; ctx.shadowBlur=20;
    ctx.fillText(pw.em,0,0); ctx.restore();
  }

  // Traffic (pixel-art cars)
  const sorted=[...G.traffic].sort((a,b)=>a.y-b.y);
  for(const tc of sorted){
    if(!tc.alive) continue;
    // Only draw if on screen
    if(tc.y<-tc.h*0.6||tc.y>KILL_Y) continue;
    drawCar(tc.x, tc.y, tc.w, tc.h, tc.col, tc.col2,
      false, tc.cop, tc.sirenT, tc.wobble*0.5);
  }

  // Particles
  for(const p of particles){
    ctx.save();
    ctx.globalAlpha=Math.max(0,p.life);
    ctx.fillStyle=p.col; ctx.shadowColor=p.col; ctx.shadowBlur=8;
    ctx.beginPath(); ctx.arc(p.x,p.y,Math.max(0.5,p.size),0,Math.PI*2); ctx.fill();
    ctx.restore();
  }

  // Player car
  const car=CARS[selCar];
  const tilt=G.laneMoving ? G.laneDir*8*(1-Math.abs(G.laneX-G.targetX)/LANE_W) : 0;

  // Engine glow
  const eg=ctx.createRadialGradient(G.laneX,PLAYER_Y+30,0,G.laneX,PLAYER_Y+30,55);
  eg.addColorStop(0,car.col+(G.nitroOn?'aa':'22'));
  eg.addColorStop(1,'transparent');
  ctx.fillStyle=eg; ctx.beginPath(); ctx.ellipse(G.laneX,PLAYER_Y+30,60,18,0,0,Math.PI*2); ctx.fill();

  // Shield bubble
  if(G.shieldT>0){
    ctx.save();
    ctx.strokeStyle='#cc44ff'; ctx.shadowColor='#cc44ff'; ctx.shadowBlur=24;
    ctx.lineWidth=3; ctx.globalAlpha=0.6+Math.sin(G.frame*.3)*.35;
    ctx.beginPath(); ctx.ellipse(G.laneX,PLAYER_Y-5,36,58,0,0,Math.PI*2); ctx.stroke();
    ctx.restore();
  }
  // Magnet aura
  if(G.magnetT>0){
    ctx.save();
    ctx.strokeStyle='#ff8844'; ctx.shadowColor='#ff8844'; ctx.shadowBlur=20;
    ctx.lineWidth=2; ctx.globalAlpha=.4+Math.sin(G.frame*.25)*.3;
    ctx.setLineDash([5,7]);
    ctx.beginPath(); ctx.arc(G.laneX,PLAYER_Y,90,0,Math.PI*2); ctx.stroke();
    ctx.restore();
  }

  // Nitro flames
  if(G.nitroOn){
    for(let j=0;j<3;j++){
      ctx.save();
      ctx.globalAlpha=.55+Math.random()*.4;
      ctx.font=(16+Math.random()*10)+'px serif'; ctx.textAlign='center';
      ctx.shadowColor=car.col; ctx.shadowBlur=18;
      ctx.fillText('🔥',G.laneX+(j-1)*14,PLAYER_Y+50+Math.random()*8); ctx.restore();
    }
    // Speed lines
    ctx.save(); ctx.globalAlpha=0.07; ctx.strokeStyle=car.col; ctx.lineWidth=1;
    for(let k=0;k<8;k++){
      const lx=ROAD_X+Math.random()*ROAD_W;
      const ly=PLAYER_Y+30+Math.random()*200;
      ctx.beginPath(); ctx.moveTo(lx,ly); ctx.lineTo(lx,ly+60); ctx.stroke();
    }
    ctx.restore();
  }

  // Draw player (flash on hit)
  ctx.save();
  if(G.flashT>0&&Math.floor(G.flashT*10)%2===0) ctx.filter='brightness(6) saturate(0)';
  ghostDraw(ctx, G.frame);
  drawCar(G.laneX, PLAYER_Y, 54, 90, car.col, lighten(car.col), true, false, 0, tilt);
  ctx.restore();

  // Float texts
  ctx.save();
  for(const f of floats){
    ctx.globalAlpha=Math.max(0,f.life);
    ctx.fillStyle=f.col; ctx.shadowColor=f.col; ctx.shadowBlur=14;
    ctx.font="bold 14px 'Orbitron',sans-serif";
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(f.txt,f.x,f.y);
  }
  ctx.globalAlpha=1; ctx.restore();

  // Screen overlay effects
  if(G.flashT>0&&Math.floor(G.flashT*10)%2===0){
    ctx.fillStyle='rgba(255,20,20,0.14)'; ctx.fillRect(0,0,BW,BH);
    ctx.strokeStyle='rgba(255,20,20,0.35)'; ctx.lineWidth=8;
    ctx.strokeRect(4,4,BW-8,BH-8);
  }
  if(G.shieldT>0){
    ctx.strokeStyle='rgba(204,68,255,0.18)'; ctx.lineWidth=7;
    ctx.strokeRect(4,4,BW-8,BH-8);
  }
  if(G.nitroOn){
    const nv=ctx.createRadialGradient(BW/2,BH/2,BH*.1,BW/2,BH/2,BH*.7);
    nv.addColorStop(0,'transparent');
    nv.addColorStop(1,car.col+'18');
    ctx.fillStyle=nv; ctx.fillRect(0,0,BW,BH);
  }

  // ── 날씨 오버레이 ──
  if(G.weather==='rain'){
    // 빗방울 렌더링
    for(const p of particles){
      if(!p.isRain) continue;
      ctx.save();
      ctx.globalAlpha=Math.max(0,p.life)*0.7;
      ctx.strokeStyle=p.col; ctx.lineWidth=p.sz;
      ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(p.x-2,p.y+8); ctx.stroke();
      ctx.restore();
      p.x+=p.vx; p.y+=p.vy; p.life-=0.04;
    }
    // 빗길 화면 틴트
    ctx.save(); ctx.globalAlpha=0.10; ctx.fillStyle='#2255aa'; ctx.fillRect(0,0,BW,BH); ctx.restore();
  } else if(G.weather==='fog'){
    ctx.save(); ctx.globalAlpha=0.22; ctx.fillStyle='#ccddee'; ctx.fillRect(0,0,BW,BH); ctx.restore();
  }

  if(G.shake>0) ctx.restore();
}

function lighten(hex){
  // Simple lighten: mix with white
  const r=parseInt(hex.slice(1,3),16), g=parseInt(hex.slice(3,5),16), b=parseInt(hex.slice(5,7),16);
  const m=60;
  return `rgb(${Math.min(255,r+m)},${Math.min(255,g+m)},${Math.min(255,b+m)})`;
}

// ═══════════════════════════════════════════════════════
//  LOOP
// ═══════════════════════════════════════════════════════
function loop(){
  if(!G.run) return;
  render(); update();
  raf=requestAnimationFrame(loop);
}

// ═══════════════════════════════════════════════════════
//  OVERLAY / MENUS
// ═══════════════════════════════════════════════════════
function buildCarGrid(){
  const d=document.createElement('div');
  d.className='cgrid';
  CARS.forEach((c,i)=>{
    const card=document.createElement('div');
    card.className='ccard'+(i===selCar?' sel':'');
    card.innerHTML=`
      <span class="cem">${c.em}</span>
      <div class="cnm" style="color:${c.col}">${c.name}</div>
      <div class="ctp">${c.tp}</div>
      <div class="cbars">
        <div class="cbr"><span class="cbl">SPD</span><div class="cbt"><div class="cbf" style="width:${c.s}%;background:${c.col}"></div></div></div>
        <div class="cbr"><span class="cbl">HP</span><div class="cbt"><div class="cbf" style="width:${c.h}%;background:#ff3366"></div></div></div>
        <div class="cbr"><span class="cbl">ACC</span><div class="cbt"><div class="cbf" style="width:${c.a}%;background:#ffaa00"></div></div></div>
      </div>`;
    card.onclick=()=>{ selCar=i; document.querySelectorAll('.ccard').forEach((x,j)=>x.classList.toggle('sel',j===i)); };
    d.appendChild(card);
  });
  return d;
}

function showTitle(){
  cancelAnimationFrame(raf); G.run=false;
  const best=parseInt(localStorage.getItem('nrv5')||'0');
  const oi=document.getElementById('oi');
  oi.innerHTML=`
    <div class="obadge">NEON RUNAWAY v5.0</div>
    <div class="otitle" style="color:#00ffcc">🏎️<br>네온 도주 레이싱</div>
    <div class="osub">TOP-DOWN · 5LANE · ×12 COMBO · 7 POWER-UPS · POLICE WAVE</div>`;
  oi.appendChild(buildCarGrid());
  const rest=document.createElement('div');
  rest.innerHTML=`
    <div class="instrow">
      ← → / A D / 버튼 : 레인 전환 &nbsp;|&nbsp; SPACE / ⚡ : 니트로<br>
      모바일: 화면 좌우 스와이프로 레인 전환
    </div>
    ${best>0?`<div class="brow">🏆 최고기록: <span class="bnum">${best.toLocaleString()}</span></div>`:''}
    <div class="sbtn" id="sbtn">시동 걸기 🚀</div>`;
  oi.appendChild(rest);
  document.getElementById('sbtn').onclick=startGame;
  document.getElementById('ov').style.display='flex';
}

function showGameOver(){
  G.run=false; cancelAnimationFrame(raf);
  const best=Math.max(G.score,parseInt(localStorage.getItem('nrv5')||'0'));
  localStorage.setItem('nrv5',best);
  const isRec=G.score>=best&&G.score>0;
  if(isRec) ghostSave(); // 최고 기록 갱신 시 고스트 저장
  const ghostInfo = ghostBest ? `<div class="brow" style="color:#00ffcc;font-size:11px;">👻 고스트: 이전 최고 ${ghostBest.score?.toLocaleString()}점 기록 저장됨</div>` : '';
  const oi=document.getElementById('oi');
  oi.innerHTML=`
    <div class="obadge">${isRec?'🏆 NEW RECORD!':'GAME OVER'}</div>
    <div class="otitle" style="color:#ff2255">💥 충돌!</div>
    <div class="osub">WAVE ${G.wave} · ${G.totalKills}대 회피 · MAX COMBO ×${G.maxCombo}</div>
    <div class="statsrow">
      <div class="sbox"><div class="snum" style="color:#ffaa00">${G.score.toLocaleString()}</div><div class="slbl">SCORE</div></div>
      <div class="sbox"><div class="snum" style="color:#00ffcc">${G.dist.toFixed(1)}km</div><div class="slbl">DIST</div></div>
      <div class="sbox"><div class="snum" style="color:#cc44ff">×${G.maxCombo}</div><div class="slbl">COMBO</div></div>
    </div>
    <div class="brow">🏆 최고기록: <span class="bnum">${best.toLocaleString()}</span></div>
    ${ghostInfo}
    <div class="sbtn" id="sbtn">다시 도주 🏎️</div>
    <br><div class="s2btn" id="s2btn">차량 변경</div>`;
  document.getElementById('sbtn').onclick=startGame;
  document.getElementById('s2btn').onclick=showTitle;
  document.getElementById('ov').style.display='flex';
}

function startGame(){
  document.getElementById('ov').style.display='none';
  cancelAnimationFrame(raf); floats=[]; particles=[];
  initGame(); G.run=true;
  raf=requestAnimationFrame(loop);
}

// ═══════════════════════════════════════════════════════
//  INPUT
// ═══════════════════════════════════════════════════════
const KEYS={};
addEventListener('keydown',e=>{
  KEYS[e.code]=true;
  if(['ArrowLeft','ArrowRight','Space','KeyA','KeyD'].includes(e.code)) e.preventDefault();
});
addEventListener('keyup',e=>{ KEYS[e.code]=false; });

function addTouch(id,dn,up){
  const el=document.getElementById(id); if(!el)return;
  const d=e=>{ e.preventDefault(); dn(); el.classList.add('p'); };
  const u=e=>{ e.preventDefault(); up(); el.classList.remove('p'); };
  el.addEventListener('touchstart',d,{passive:false});
  el.addEventListener('touchend',u,{passive:false});
  el.addEventListener('touchcancel',u,{passive:false});
  el.addEventListener('mousedown',d);
  el.addEventListener('mouseup',u);
  el.addEventListener('mouseleave',u);
}
addTouch('bl', ()=>G._tL=true,  ()=>G._tL=false);
addTouch('br', ()=>G._tR=true,  ()=>G._tR=false);
addTouch('nbtn',()=>G._tN=true, ()=>G._tN=false);

// Swipe on main area
let swX0=null;
document.getElementById('gc').addEventListener('touchstart',e=>{ swX0=e.touches[0].clientX; },{passive:true});
document.getElementById('gc').addEventListener('touchend',e=>{
  if(swX0===null)return;
  const dx=e.changedTouches[0].clientX-swX0;
  if(Math.abs(dx)>28){ if(dx<0)G._swL=true; else G._swR=true; }
  swX0=null;
},{passive:true});

// ═══════════════════════════════════════════════════════
//  BOOT
// ═══════════════════════════════════════════════════════
initGame();
G.run = true;
requestAnimationFrame(loop);
</script>
</body>
</html>"""


def render():
    st.markdown("<style>iframe{border:none!important;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=760, scrolling=False)
