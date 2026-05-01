import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>네온 도주 레이싱</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --gold:#f5c518;--red:#ff2244;--cyan:#00d4ff;--green:#00ff88;--purple:#c04fff;--orange:#ff7700;
  --bg:#04070f;--bg2:#070d1a;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.08);
}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;display:flex;align-items:center;justify-content:center;}
#gc{display:block;background:var(--bg);}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;z-index:50;padding:10px 16px;
  background:linear-gradient(180deg,rgba(0,0,0,.85)0%,transparent 100%);
  display:flex;align-items:flex-start;gap:8px;pointer-events:none;}
.hud-block{display:flex;flex-direction:column;align-items:center;
  background:rgba(0,0,0,.45);border:1px solid var(--border);border-radius:10px;padding:5px 12px;}
.hud-val{font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:#fff;letter-spacing:1px;line-height:1.1;}
.hud-lbl{font-size:7px;color:#445;letter-spacing:3px;text-transform:uppercase;}
#hv-speed{color:var(--cyan);}
#hv-combo{color:var(--gold);transition:all .1s;}
#hv-combo.pop{transform:scale(1.4);color:var(--red);}
#hud-right{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
.life-pip{width:12px;height:12px;border-radius:50%;background:var(--red);
  box-shadow:0 0 8px rgba(255,34,68,.8);display:inline-block;margin:0 2px;transition:all .3s;}
.life-pip.dead{background:#1a0a0a;box-shadow:none;}

/* NITRO BAR */
#nitro-wrap{position:absolute;bottom:88px;left:50%;transform:translateX(-50%);
  width:min(200px,50vw);z-index:60;pointer-events:none;text-align:center;}
#nitro-lbl{font-size:7px;color:rgba(0,212,255,.5);letter-spacing:3px;margin-bottom:3px;}
#nitro-track{display:flex;gap:2px;}
.n-seg{flex:1;height:6px;border-radius:99px;background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.12);overflow:hidden;}
.n-fill{height:100%;background:linear-gradient(90deg,#0088aa,#00d4ff,#88ffff);border-radius:99px;width:0%;transition:width .04s;}

/* DIST */
#dist-box{position:absolute;top:10px;left:50%;transform:translateX(-50%);z-index:60;pointer-events:none;text-align:center;}
#dist-val{font-family:'Rajdhani',sans-serif;font-size:26px;font-weight:900;color:#fff;letter-spacing:2px;}
#dist-lbl{font-size:7px;color:#335;letter-spacing:3px;}

/* COMBO POPUP */
#combo-pop{position:absolute;top:28%;left:50%;transform:translateX(-50%);z-index:80;pointer-events:none;text-align:center;opacity:0;transition:opacity .15s;}
.cp-big{font-family:'Black Han Sans',sans-serif;font-size:40px;letter-spacing:3px;}
.cp-sub{font-size:9px;color:#bbb;letter-spacing:3px;margin-top:2px;}

/* BOOST / VIGNETTE */
#boost-flash{position:absolute;inset:0;z-index:70;pointer-events:none;opacity:0;
  background:radial-gradient(ellipse at center,rgba(0,212,255,.18)0%,transparent 65%);transition:opacity .05s;}
#vignette{position:absolute;inset:0;z-index:75;pointer-events:none;opacity:0;
  background:radial-gradient(ellipse at center,transparent 40%,rgba(255,0,30,.5)100%);transition:opacity .1s;}
#slowmo-frame{position:absolute;inset:0;z-index:65;pointer-events:none;opacity:0;
  box-shadow:inset 0 0 0 4px rgba(255,119,0,.4);transition:opacity .2s;}

/* WAVE BANNER */
#wave-banner{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);z-index:90;pointer-events:none;
  font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5vw,32px);letter-spacing:4px;
  text-shadow:0 0 25px currentColor;opacity:0;transition:opacity .2s;white-space:nowrap;text-align:center;}

/* DPAD */
#dpad{position:absolute;bottom:14px;left:14px;z-index:100;
  display:grid;grid-template-columns:60px 60px 60px;grid-template-rows:55px 55px;gap:5px;}
.dp{border-radius:12px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.1);
  display:flex;align-items:center;justify-content:center;font-size:22px;
  cursor:pointer;user-select:none;-webkit-user-select:none;transition:all .1s;touch-action:none;}
.dp:active,.dp.pr{background:rgba(0,212,255,.18);border-color:rgba(0,212,255,.5);box-shadow:0 0 12px rgba(0,212,255,.3);transform:scale(.93);}
#dp-up{grid-column:2;grid-row:1;}
#dp-left{grid-column:1;grid-row:2;}
#dp-down{grid-column:2;grid-row:2;}
#dp-right{grid-column:3;grid-row:2;}

/* NITRO BTN */
#nitro-btn{position:absolute;bottom:14px;right:14px;z-index:100;width:78px;height:78px;border-radius:50%;
  background:rgba(0,212,255,.1);border:2px solid rgba(0,212,255,.35);
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:24px;
  cursor:pointer;user-select:none;-webkit-user-select:none;touch-action:none;transition:all .1s;}
#nitro-btn:active,#nitro-btn.pr{background:rgba(0,212,255,.3);box-shadow:0 0 20px rgba(0,212,255,.5);transform:scale(.92);}
.nb-lbl{font-size:7px;color:var(--cyan);letter-spacing:2px;margin-top:2px;}

/* ── OVERLAY ── */
#overlay{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
  background:rgba(4,7,15,.93);backdrop-filter:blur(4px);}
.ov-wrap{text-align:center;max-width:460px;width:92vw;padding:32px 24px;
  background:linear-gradient(160deg,rgba(7,13,26,.98),rgba(10,18,32,.98));
  border:1px solid rgba(0,212,255,.2);border-radius:20px;
  box-shadow:0 0 80px rgba(0,212,255,.07),inset 0 1px 0 rgba(255,255,255,.04);}
.ov-badge{display:inline-block;font-size:8px;letter-spacing:4px;color:var(--cyan);
  background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.2);border-radius:99px;padding:3px 14px;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(24px,6vw,38px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#334;letter-spacing:4px;margin-bottom:16px;}
.ov-score{font-family:'Rajdhani',sans-serif;font-size:32px;font-weight:900;color:var(--gold);}
.ov-best{font-size:9px;color:#445;margin-bottom:16px;}

/* CAR GRID */
.car-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px;margin-bottom:16px;}
.car-card{padding:9px 4px;background:var(--glass);border:1.5px solid var(--border);border-radius:12px;cursor:pointer;transition:all .2s;text-align:center;}
.car-card:hover{border-color:rgba(0,212,255,.35);}
.car-card.sel{border-color:var(--cyan);background:rgba(0,212,255,.1);box-shadow:0 0 16px rgba(0,212,255,.22);}
.cc-ico{font-size:26px;display:block;margin-bottom:3px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:10px;letter-spacing:1px;}
.cc-bar{height:4px;border-radius:99px;margin-top:4px;background:rgba(255,255,255,.06);overflow:hidden;}
.cc-fill{height:100%;border-radius:99px;}

/* DIFF TABS */
.diff-row{display:flex;gap:6px;justify-content:center;margin-bottom:16px;}
.d-tab{padding:7px 14px;border-radius:99px;background:var(--glass);border:1px solid var(--border);
  font-size:9px;color:#556;cursor:pointer;transition:all .18s;text-align:center;}
.d-tab.sel{border-color:var(--gold);color:var(--gold);background:rgba(245,197,24,.08);}

/* STATS */
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.s-chip{padding:6px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.s-v{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:#fff;}
.s-l{font-size:7px;color:#446;letter-spacing:2px;}

/* START BTN */
.start-btn{display:inline-block;padding:12px 34px;background:linear-gradient(135deg,rgba(0,212,255,.2),rgba(108,99,255,.14));
  border:1px solid rgba(0,212,255,.48);border-radius:12px;font-family:'Black Han Sans',sans-serif;
  font-size:17px;color:var(--cyan);letter-spacing:2px;cursor:pointer;transition:all .2s;margin-top:2px;}
.start-btn:hover{background:linear-gradient(135deg,rgba(0,212,255,.36),rgba(108,99,255,.26));transform:translateY(-3px);box-shadow:0 10px 28px rgba(0,212,255,.3);}
.start-btn:active{transform:translateY(0);}

/* SCROLL TAG */
.tag-strip{overflow:hidden;width:100%;margin-bottom:14px;}
.tag-inner{display:flex;gap:8px;animation:tagRoll 14s linear infinite;width:max-content;}
@keyframes tagRoll{0%{transform:translateX(0);}100%{transform:translateX(-50%)}}
.tpill{font-size:8px;border:1px solid var(--border);border-radius:99px;padding:3px 10px;white-space:nowrap;letter-spacing:1px;color:#445;}
.tpill.r{color:var(--red);border-color:rgba(255,34,68,.3);}
.tpill.g{color:var(--gold);border-color:rgba(245,197,24,.3);}
.tpill.c{color:var(--cyan);border-color:rgba(0,212,255,.3);}
.tpill.p{color:var(--purple);border-color:rgba(192,79,255,.3);}
</style>
</head>
<body>
<div id="root">
  <canvas id="gc"></canvas>
  <div id="hud">
    <div class="hud-block"><div class="hud-val" id="hv-score">0</div><div class="hud-lbl">SCORE</div></div>
    <div class="hud-block"><div class="hud-val" id="hv-speed">0</div><div class="hud-lbl">KM/H</div></div>
    <div class="hud-block"><div class="hud-val" id="hv-combo">×1</div><div class="hud-lbl">COMBO</div></div>
    <div id="hud-right"><div id="lives-row"></div></div>
  </div>
  <div id="dist-box"><div id="dist-val">0.0</div><div id="dist-lbl">KM</div></div>
  <div id="nitro-wrap"><div id="nitro-lbl">NITRO</div><div id="nitro-track"></div></div>
  <div id="combo-pop"><div class="cp-big" id="cp-big" style="color:var(--gold)">×3 COMBO!</div><div class="cp-sub">DODGE BONUS</div></div>
  <div id="boost-flash"></div>
  <div id="vignette"></div>
  <div id="slowmo-frame"></div>
  <div id="wave-banner"></div>
  <div id="dpad">
    <div class="dp" id="dp-up">▲</div>
    <div class="dp" id="dp-left">◀</div>
    <div class="dp" id="dp-down">▼</div>
    <div class="dp" id="dp-right">▶</div>
  </div>
  <div id="nitro-btn"><span>⚡</span><span class="nb-lbl">NITRO</span></div>
  <div id="overlay"><div class="ov-wrap" id="ovc"></div></div>
</div>
<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  네온 도주 레이싱 v2.0
//  무한 5레인 · 경찰 추격 · 니트로 · 파워업 · 콤보 · 3 난이도
// ══════════════════════════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
const root   = document.getElementById('root');

// RESPONSIVE
let GW=420, GH=720, SC=1;
function resize(){
  const rw=root.clientWidth, rh=root.clientHeight;
  SC = Math.min(rw/GW, rh/GH);
  canvas.width=GW; canvas.height=GH;
  canvas.style.width=(GW*SC)+'px'; canvas.style.height=(GH*SC)+'px';
}
resize(); window.addEventListener('resize',resize);

// KEYS
const KEYS={};
window.addEventListener('keydown',e=>{ KEYS[e.code]=true; ['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)&&e.preventDefault(); });
window.addEventListener('keyup',e=>KEYS[e.code]=false);

// CONSTS
const LANES=5;
const RL=0.07, RR=0.93; // road left/right pct

const CAR_DEFS=[
  {name:'스포츠',  emoji:'🚗', spd:5.5,acc:0.018,nitroMul:2.0,hand:0.9, hp:3,col:'#00d4ff'},
  {name:'슈퍼카',  emoji:'🏎️', spd:7.0,acc:0.022,nitroMul:2.4,hand:0.65,hp:2,col:'#ff2244'},
  {name:'SUV',     emoji:'🚙', spd:4.5,acc:0.013,nitroMul:1.7,hand:1.1, hp:4,col:'#00ff88'},
  {name:'머슬카',  emoji:'🚘', spd:5.8,acc:0.016,nitroMul:2.0,hand:0.8, hp:3,col:'#f5c518'},
];
const ENEMY_DEFS=[
  {emoji:'🚌',w:40,h:70,rs:-0.4,pts:20,col:'#4455ff'},
  {emoji:'🚛',w:44,h:80,rs:-0.2,pts:30,col:'#663311'},
  {emoji:'🚓',w:36,h:62,rs:1.1, pts:15,col:'#2255ee',cop:true},
  {emoji:'🏍️',w:22,h:44,rs:1.3, pts:12,col:'#ffaa00'},
  {emoji:'🚑',w:38,h:66,rs:0.6, pts:22,col:'#ff4488'},
  {emoji:'🚜',w:42,h:74,rs:-0.5,pts:35,col:'#556633'},
  {emoji:'🚐',w:38,h:64,rs:0.2, pts:18,col:'#334466'},
  {emoji:'🛻',w:36,h:62,rs:0.4, pts:20,col:'#446655'},
];
const POWER_DEFS=[
  {emoji:'⚡',type:'nitro', col:'#00d4ff',pts:0,  lbl:'NITRO +50%'},
  {emoji:'⭐',type:'score', col:'#f5c518',pts:250, lbl:'BONUS +250'},
  {emoji:'💊',type:'heal',  col:'#00ff88',pts:50,  lbl:'HP 회복!'},
  {emoji:'🔱',type:'shield',col:'#c04fff',pts:0,   lbl:'무적 4초'},
  {emoji:'🌀',type:'slow',  col:'#ff7700',pts:0,   lbl:'슬로우 모션'},
];

let selCar=0, diffLv=1;
let G={}, raf=null;

// PARTICLES
let PARTS=[], FLOATS=[];
function spawnParts(x,y,o={}){
  const n=o.n||10;
  for(let i=0;i<n;i++){
    const a=o.dir!==undefined?o.dir+(Math.random()-.5)*(o.spread||Math.PI*2):Math.random()*Math.PI*2;
    const v=(o.vMin||1)+Math.random()*(o.vMax||4);
    const cols=Array.isArray(o.col)?o.col:[o.col||'#fff'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      decay:(o.dMin||.025)+Math.random()*(o.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(o.szMin||2)+Math.random()*(o.szMax||5),glow:o.glow||false});
  }
}
function spawnFloat(x,y,txt,col){FLOATS.push({x,y:y-10,txt,col,life:1,vy:-0.6});}
function tickParts(){for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.87;p.vy*=.87;p.life-=p.decay;p.life<=0&&PARTS.splice(i,1);}}
function tickFloats(){for(let i=FLOATS.length-1;i>=0;i--){const f=FLOATS[i];f.y+=f.vy;f.life-=.02;f.life<=0&&FLOATS.splice(i,1);}}
function drawParts(){ctx.save();for(const p of PARTS){ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*3;}ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.1,p.life),0,Math.PI*2);ctx.fill();if(p.glow)ctx.shadowBlur=0;}ctx.globalAlpha=1;ctx.restore();}
function drawFloats(){ctx.save();for(const f of FLOATS){ctx.globalAlpha=Math.max(0,f.life);ctx.shadowColor=f.col;ctx.shadowBlur=8;ctx.fillStyle=f.col;ctx.font="bold 14px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(f.txt,f.x,f.y);}ctx.shadowBlur=0;ctx.globalAlpha=1;ctx.restore();}

// ROAD HELPERS
function laneX(i){return GW*RL+(GW*(RR-RL)/LANES)*(i+.5);}
function laneEdge(i){return GW*RL+(GW*(RR-RL)/LANES)*i;}

// ROAD DRAW
let roadY=0, polF=0;
function drawRoad(spd){
  const L=GW*RL, R=GW*RR, lw=(R-L)/LANES;
  // sky
  const sky=ctx.createLinearGradient(0,0,0,GH*.25);
  sky.addColorStop(0,'#020408'); sky.addColorStop(1,'#030810');
  ctx.fillStyle=sky; ctx.fillRect(0,0,GW,GH);
  // city silhouette
  for(let ci=0;ci<14;ci++){
    const bw=24+Math.sin(ci*1.7)*12+8, bh=50+Math.sin(ci*2.3)*45+25;
    const bx=ci*(GW/13.5)-12;
    ctx.fillStyle='#02050a'; ctx.fillRect(bx,GH*.16-bh,bw,bh);
    for(let wy=GH*.16-bh+6;wy<GH*.16-5;wy+=11){
      if(Math.random()<.55)continue;
      ctx.fillStyle=`rgba(${Math.random()<.5?'0,200,255':'255,190,50'},.28)`;
      ctx.fillRect(bx+3+Math.random()*(bw-10),wy,4,7);ctx.fillStyle='#02050a';
    }
  }
  // road surface
  const rg=ctx.createLinearGradient(0,0,0,GH);
  rg.addColorStop(0,'#0c1422'); rg.addColorStop(.5,'#0a1120'); rg.addColorStop(1,'#070d18');
  ctx.fillStyle=rg; ctx.fillRect(L,0,R-L,GH);
  // sidewalks
  ctx.fillStyle='#050b16'; ctx.fillRect(0,0,L,GH); ctx.fillRect(R,0,GW-R,GH);
  // edge neon
  [L,R].forEach(ex=>{
    ctx.save();ctx.strokeStyle='rgba(0,212,255,.5)';ctx.shadowColor='rgba(0,212,255,.6)';ctx.shadowBlur=14;ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(ex,0);ctx.lineTo(ex,GH);ctx.stroke();ctx.restore();
  });
  // lane dashes
  const dl=48,dg=42, tot=dl+dg, off=roadY%tot;
  ctx.setLineDash([dl,dg]); ctx.lineDashOffset=-off;
  ctx.strokeStyle='rgba(255,255,255,.08)'; ctx.lineWidth=1.5;
  for(let li=1;li<LANES;li++){const lx=laneEdge(li);ctx.beginPath();ctx.moveTo(lx,0);ctx.lineTo(lx,GH);ctx.stroke();}
  ctx.setLineDash([]);
  // speed glow on sides
  if(spd>5){
    const a=Math.min(.35,(spd-5)/10);
    const gL=ctx.createLinearGradient(0,0,L,0);gL.addColorStop(0,'transparent');gL.addColorStop(1,`rgba(0,212,255,${a})`);
    ctx.fillStyle=gL;ctx.fillRect(0,0,L,GH);
    const gR=ctx.createLinearGradient(R,0,GW,0);gR.addColorStop(0,`rgba(0,212,255,${a})`);gR.addColorStop(1,'transparent');
    ctx.fillStyle=gR;ctx.fillRect(R,0,GW-R,GH);
  }
}

function drawVeh(x,y,emoji,sz,flash,glow,alpha=1){
  ctx.save();ctx.globalAlpha=alpha;
  if(flash&&Math.floor(flash*12)%2===0)ctx.filter='brightness(4) saturate(0)';
  if(glow){ctx.shadowColor=glow;ctx.shadowBlur=18;}
  // reflection
  ctx.save();ctx.globalAlpha*=.1;ctx.scale(1,-.28);ctx.font=sz+'px serif';ctx.textAlign='center';ctx.fillText(emoji,x,-y-10);ctx.restore();
  ctx.font=sz+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(emoji,x,y);
  if(glow)ctx.shadowBlur=0;ctx.restore();
}

function drawPlayerCar(){
  const p=G.player, def=CAR_DEFS[selCar];
  // tire marks
  ctx.save();ctx.globalAlpha=.06;ctx.strokeStyle='#fff';ctx.lineWidth=5;
  ctx.beginPath();ctx.moveTo(p.x-10,p.y+22);ctx.lineTo(p.x-10,p.y+46);
  ctx.moveTo(p.x+10,p.y+22);ctx.lineTo(p.x+10,p.y+46);ctx.stroke();ctx.restore();
  // nitro exhaust
  if(G.nitroOn){
    for(let j=0;j<3;j++){
      ctx.save();ctx.globalAlpha=.45+Math.random()*.45;
      ctx.shadowColor=def.col;ctx.shadowBlur=18;ctx.font='18px serif';ctx.textAlign='center';
      ctx.fillText('🔥',p.x+(j-1)*7,p.y+34+j*5+Math.random()*5);ctx.restore();
    }
    // trailing streaks
    for(let s=0;s<5;s++){
      ctx.save();ctx.globalAlpha=.1*Math.random();ctx.strokeStyle=def.col;ctx.lineWidth=1;
      const sx=p.x+(Math.random()-.5)*28, sy=p.y+30+Math.random()*35;
      ctx.beginPath();ctx.moveTo(sx,sy);ctx.lineTo(sx,sy+18+Math.random()*25);ctx.stroke();ctx.restore();
    }
  }
  // underbody glow
  const ug=ctx.createRadialGradient(p.x,p.y+22,0,p.x,p.y+22,42);
  ug.addColorStop(0,G.nitroOn?def.col+'66':def.col+'22'); ug.addColorStop(1,'transparent');
  ctx.fillStyle=ug;ctx.beginPath();ctx.ellipse(p.x,p.y+28,38,14,0,0,Math.PI*2);ctx.fill();
  // shield ring
  if(G.shieldT>0){
    ctx.save();const sr=Math.sin(G.frame*.14)*.3+.7;
    ctx.globalAlpha=sr;ctx.strokeStyle='#c04fff';ctx.shadowColor='#c04fff';ctx.shadowBlur=14;ctx.lineWidth=2.5;
    ctx.beginPath();ctx.ellipse(p.x,p.y,32,42,0,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  drawVeh(p.x,p.y,def.emoji,52,G.flashT,G.nitroOn?def.col:null);
}

function drawEnemy(e){
  polF++;
  if(e.cop){
    const col=Math.sin(polF*.22)>0?'rgba(0,100,255,.7)':'rgba(255,30,30,.7)';
    ctx.save();ctx.shadowColor=col;ctx.shadowBlur=16;ctx.fillStyle=col.replace('.7)','.12)');
    ctx.beginPath();ctx.ellipse(e.x,e.y-26,20,9,0,0,Math.PI*2);ctx.fill();ctx.restore();
  }
  drawVeh(e.x,e.y,e.emoji,e.h*.7,e.flash,null);
}

// GAME INIT
function initGame(){
  const def=CAR_DEFS[selCar];
  const dms=[.75,1,1.35];
  G={
    running:true,dead:false,
    score:0,dist:0,frame:0,
    hp:def.hp,maxHp:def.hp,
    spd:def.spd,baseSpd:def.spd,topSpd:def.spd*(1.6+diffLv*.2),
    dm:dms[diffLv],
    player:{lane:2,x:laneX(2),y:GH*.78},
    laneT:2,laneCC:0,
    nitro:100,nitroOn:false,
    combo:1,comboD:0,
    flashT:0,shieldT:0,slowT:0,
    enemies:[],spawnT:0,
    powers:[],powerT:0,
  };
  buildNitroBar(); buildLives(); PARTS=[]; FLOATS=[]; roadY=0;
}

function buildNitroBar(){
  const t=document.getElementById('nitro-track');t.innerHTML='';
  for(let i=0;i<10;i++){const s=document.createElement('div');s.className='n-seg';const f=document.createElement('div');f.className='n-fill';s.appendChild(f);t.appendChild(s);}
}
function updateNitroBar(){
  const segs=document.querySelectorAll('.n-seg');
  segs.forEach((s,i)=>{const p=Math.min(100,Math.max(0,(G.nitro-i*10)*10));s.querySelector('.n-fill').style.width=p+'%';});
}
function buildLives(){
  const lr=document.getElementById('lives-row');lr.innerHTML='';
  for(let i=0;i<G.maxHp;i++){const p=document.createElement('div');p.className='life-pip'+(i>=G.hp?' dead':'');p.id='lp'+i;lr.appendChild(p);}
}
function updateLives(){for(let i=0;i<G.maxHp;i++){const p=document.getElementById('lp'+i);if(p)p.classList.toggle('dead',i>=G.hp);}}

function spawnEnemy(){
  const t=ENEMY_DEFS[Math.floor(Math.random()*ENEMY_DEFS.length)];
  const lane=Math.floor(Math.random()*LANES);
  if(lane===G.laneT&&Math.random()<.45)return;
  G.enemies.push({lane,x:laneX(lane),y:-95,w:t.w,h:t.h,emoji:t.emoji,pts:t.pts,col:t.col,cop:t.cop||false,rs:t.rs,alive:true,scored:false,flash:0});
}
function spawnPower(){
  const t=POWER_DEFS[Math.floor(Math.random()*POWER_DEFS.length)];
  const lane=Math.floor(Math.random()*LANES);
  G.powers.push({lane,x:laneX(lane),y:-32,type:t.type,emoji:t.emoji,col:t.col,pts:t.pts,lbl:t.lbl,alive:true,rot:0});
}
function rectsOvlp(ax,ay,aw,ah,bx,by,bw,bh){return ax-aw/2<bx+bw/2&&ax+aw/2>bx-bw/2&&ay-ah/2<by+bh/2&&ay+ah/2>by-bh/2;}

let popT=0;
function showPop(combo){
  const pop=document.getElementById('combo-pop');
  document.getElementById('cp-big').textContent=`×${combo} COMBO!`;
  pop.style.opacity='1';popT=90;
}

function update(){
  if(!G.running||G.dead)return;
  G.frame++;
  const spd=G.nitroOn?G.spd*CAR_DEFS[selCar].nitroMul:G.spd;
  const effSpd=spd*(G.slowT>0?.4:1);

  G.dist+=effSpd*.012; roadY=(roadY+effSpd)%96;
  G.spd=Math.min(G.topSpd,G.spd+CAR_DEFS[selCar].acc*G.dm);

  if(G.flashT>0) G.flashT-=.016;
  if(G.shieldT>0) G.shieldT-=.017;
  if(G.slowT>0) G.slowT-=.017;
  if(G.laneCC>0) G.laneCC--;
  if(popT>0){popT--;if(popT===0)document.getElementById('combo-pop').style.opacity='0';}
  if(G.comboD>0)G.comboD--;
  else if(G.combo>1){G.combo=Math.max(1,G.combo-1);G.comboD=100;}

  // nitro
  const nk=KEYS['Space']||KEYS['ShiftLeft']||G._tNitro;
  if(nk&&G.nitro>0){G.nitroOn=true;G.nitro=Math.max(0,G.nitro-.7);document.getElementById('boost-flash').style.opacity='.14';
    spawnParts(G.player.x,G.player.y+30,{n:2,col:CAR_DEFS[selCar].col,vMin:1,vMax:3,dir:Math.PI*.5,spread:.4,szMin:2,szMax:5,glow:true,dMin:.05,dMax:.09});}
  else{G.nitroOn=false;G.nitro=Math.min(100,G.nitro+.2);document.getElementById('boost-flash').style.opacity='0';}

  // lane change
  const gl=KEYS['ArrowLeft']||KEYS['KeyA']||G._tLeft;
  const gr=KEYS['ArrowRight']||KEYS['KeyD']||G._tRight;
  if(gl&&G.laneT>0&&G.laneCC===0){G.laneT--;G.laneCC=14;spawnParts(G.player.x,G.player.y,{n:6,col:'rgba(255,255,255,.4)',vMin:1,vMax:3,dir:Math.PI,spread:.7});}
  if(gr&&G.laneT<LANES-1&&G.laneCC===0){G.laneT++;G.laneCC=14;spawnParts(G.player.x,G.player.y,{n:6,col:'rgba(255,255,255,.4)',vMin:1,vMax:3,dir:0,spread:.7});}
  G.player.x+=(laneX(G.laneT)-G.player.x)*(.15*CAR_DEFS[selCar].hand);

  // spawn enemies
  G.spawnT--;
  const si=Math.max(55,240-G.spd*13-G.dm*18);
  if(G.spawnT<=0){spawnEnemy();if(G.spd>6&&Math.random()<.28)spawnEnemy();if(G.spd>9&&Math.random()<.15)spawnEnemy();G.spawnT=si+Math.random()*75;}

  // spawn powers
  G.powerT--;
  if(G.powerT<=0){if(Math.random()<.65)spawnPower();G.powerT=210+Math.random()*260;}

  // update enemies
  for(const e of G.enemies){
    if(!e.alive)continue;
    e.y+=effSpd-e.rs*(G.slowT>0?.3:1);
    e.x+=(laneX(e.lane)-e.x)*.1;
    if(e.flash>0)e.flash-=.1;
    if(!G.dead){
      const p=G.player;
      if(rectsOvlp(p.x,p.y,24,44,e.x,e.y,e.w*.82,e.h*.72)){
        if(G.shieldT>0){e.alive=false;spawnParts(p.x,p.y,{n:14,col:['#c04fff','#8833ff'],glow:true,vMax:6,szMax:7});spawnFloat(p.x,p.y-40,'BLOCKED!','#c04fff');}
        else{G.hp--;G.flashT=.9;G.combo=1;G.comboD=0;e.alive=false;
          spawnParts(p.x,p.y,{n:20,col:['#ff2244','#ff6644','#ffaa00'],glow:true,vMax:6,szMax:8});
          document.getElementById('vignette').style.opacity='.75';setTimeout(()=>document.getElementById('vignette').style.opacity='0',380);
          updateLives();if(G.hp<=0){G.dead=true;setTimeout(showGameOver,650);}}
      }
      if(!e.scored&&e.y>p.y+45){e.scored=true;const pts=e.pts*G.combo;G.score+=pts;G.combo=Math.min(8,G.combo+1);G.comboD=130;
        spawnFloat(e.x,e.y-30,'+'+pts,G.combo>2?'#f5c518':'#00d4ff');if(G.combo>=3)showPop(G.combo);}
    }
  }
  G.enemies=G.enemies.filter(e=>e.y<GH+130);

  // powers
  for(const pw of G.powers){
    if(!pw.alive)continue;
    pw.y+=effSpd*.62; pw.rot+=.055;
    const p=G.player;
    if(rectsOvlp(p.x,p.y,28,48,pw.x,pw.y,26,26)){
      pw.alive=false;spawnParts(pw.x,pw.y,{n:12,col:pw.col,glow:true,vMax:5,szMax:6});spawnFloat(pw.x,pw.y-30,pw.lbl,pw.col);G.score+=pw.pts;
      if(pw.type==='nitro')G.nitro=Math.min(100,G.nitro+50);
      if(pw.type==='heal'){G.hp=Math.min(G.maxHp,G.hp+1);updateLives();}
      if(pw.type==='shield')G.shieldT=4;
      if(pw.type==='slow'){G.slowT=4;document.getElementById('slowmo-frame').style.opacity='1';setTimeout(()=>document.getElementById('slowmo-frame').style.opacity='0',3800);}
    }
  }
  G.powers=G.powers.filter(pw=>pw.y<GH+65);

  if(G.frame%6===0)G.score+=G.combo;
  if(G.frame%3===0&&G.nitroOn)G.score+=2;

  tickParts();tickFloats();
  updateNitroBar();
  document.getElementById('hv-score').textContent=G.score.toLocaleString();
  document.getElementById('hv-speed').textContent=Math.round(spd*43);
  document.getElementById('dist-val').textContent=G.dist.toFixed(1);
  const cv=document.getElementById('hv-combo');cv.textContent='×'+G.combo;
  if(G.combo>=3){cv.classList.add('pop');setTimeout(()=>cv.classList.remove('pop'),150);}
}

function draw(){
  ctx.clearRect(0,0,GW,GH);
  const spd=G.nitroOn?G.spd*CAR_DEFS[selCar].nitroMul:G.spd;
  drawRoad(spd);
  for(const pw of G.powers){if(!pw.alive)continue;
    ctx.save();ctx.translate(pw.x,pw.y);ctx.rotate(pw.rot);
    ctx.shadowColor=pw.col;ctx.shadowBlur=14;ctx.font='24px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(pw.emoji,0,0);
    ctx.restore();}
  for(const e of G.enemies)if(e.alive)drawEnemy(e);
  drawPlayerCar();
  drawParts();drawFloats();
  if(G.slowT>0){ctx.save();ctx.fillStyle='rgba(255,119,0,.04)';ctx.fillRect(0,0,GW,GH);ctx.restore();}
}

function loop(){if(!G.running)return;update();draw();raf=requestAnimationFrame(loop);}

// ── TITLE ──────────────────────────────────────────────────
function showTitle(){
  const best=parseInt(localStorage.getItem('raceBest')||'0');
  const tags=['🏎️ 5레인 무한도로','⚡ 니트로 부스터','🚓 경찰 추격전','×8 콤보 시스템','🔱 무적 실드','🌀 슬로우 모션','💊 HP 회복 아이템','⭐ 보너스 점수','🚛 8종 차량 장애물'];
  const tHTML=[...tags,...tags].map((t,i)=>`<span class="tpill ${i%4===0?'r':i%4===1?'g':i%4===2?'c':'p'}">${t}</span>`).join('');
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'], ddesc=['여유있는 교통량','표준 교통량','경찰 집중 출동'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-badge">NEON HIGHWAY ESCAPE v2.0</div>
    <div class="ov-title" style="color:var(--cyan)">🏎️ 네온<br>도주 레이싱</div>
    <div class="ov-sub">INFINITE 5-LANE · COMBO · POWERUP</div>
    <div class="tag-strip"><div class="tag-inner">${tHTML}</div></div>
    <div class="car-grid" id="car-grid-inner"></div>
    <div class="diff-row">${dnames.map((n,i)=>`<div class="d-tab${i===diffLv?' sel':''}" data-d="${i}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:1px">${ddesc[i]}</div></div>`).join('')}</div>
    <div style="font-size:8px;color:#334;margin-bottom:12px;line-height:2">◀▶ · A/D — 레인 이동 &nbsp;|&nbsp; SPACE / SHIFT — 니트로<br>교통차를 회피해 콤보를 쌓고 최고 점수를 달성하라!</div>
    ${best>0?`<div class="ov-best">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>`:''}
    <button class="start-btn" onclick="startGame()">시동 걸기 🚀</button>`;
  buildCarGrid2();
  document.getElementById('overlay').style.display='flex';
}
function buildCarGrid2(){
  const g=document.getElementById('car-grid-inner');if(!g)return;g.innerHTML='';
  CAR_DEFS.forEach((c,i)=>{const d=document.createElement('div');d.className='car-card'+(i===selCar?' sel':'');
    d.innerHTML=`<span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-bar"><div class="cc-fill" style="width:${(c.spd/7*100).toFixed(0)}%;background:${c.col}"></div></div><div style="font-size:7px;color:#445;margin-top:2px">HP ${c.hp} · 핸들 ${c.hand.toFixed(1)}</div>`;
    d.onclick=()=>{selCar=i;document.querySelectorAll('.car-card').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};g.appendChild(d);});
}
window.setDiff=function(d){diffLv=d;document.querySelectorAll('.d-tab').forEach((t,i)=>t.classList.toggle('sel',i===d));};

function showGameOver(){
  G.running=false;cancelAnimationFrame(raf);
  const best=Math.max(G.score,parseInt(localStorage.getItem('raceBest')||'0'));
  localStorage.setItem('raceBest',best);
  document.getElementById('ovc').innerHTML=`
    <div class="ov-badge">${G.score>=best?'🏆 NEW RECORD!':'GAME OVER'}</div>
    <div class="ov-title" style="color:var(--red)">💥 충돌!</div>
    <div class="ov-sub">YOU CRASHED</div>
    <div class="stats-row">
      <div class="s-chip"><div class="s-v" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="s-l">점수</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--cyan)">${G.dist.toFixed(1)} km</div><div class="s-l">주행거리</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--green)">×${G.combo}</div><div class="s-l">콤보</div></div>
    </div>
    <div class="ov-best">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>
    <button class="start-btn" onclick="startGame()">다시 도주 🏎️</button>
    <br><button class="start-btn" style="margin-top:8px;font-size:12px;padding:8px 20px;color:#556;border-color:rgba(255,255,255,.08)" onclick="showTitle()">차량 변경</button>`;
  document.getElementById('overlay').style.display='flex';
}
window.startGame=function(){
  document.getElementById('overlay').style.display='none';
  cancelAnimationFrame(raf);PARTS=[];FLOATS=[];
  initGame();raf=requestAnimationFrame(loop);
};
window.showTitle=showTitle;

// TOUCH
function addT(id,dn,up){
  const el=document.getElementById(id);if(!el)return;
  const d=e=>{e.preventDefault();if(dn)dn();el.classList.add('pr');};
  const u=e=>{e.preventDefault();if(up)up();el.classList.remove('pr');};
  el.addEventListener('touchstart',d,{passive:false});el.addEventListener('touchend',u,{passive:false});el.addEventListener('touchcancel',u,{passive:false});
  el.addEventListener('mousedown',d);el.addEventListener('mouseup',u);
}
addT('dp-left',()=>G._tLeft=true,()=>G._tLeft=false);
addT('dp-right',()=>G._tRight=true,()=>G._tRight=false);
addT('nitro-btn',()=>G._tNitro=true,()=>G._tNitro=false);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
