import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>네온 도주 레이싱</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--gold:#f5c518;--red:#ff2244;--cyan:#00d4ff;--green:#00ff88;--purple:#c04fff;--orange:#ff7700;--bg:#03060f;--glass:rgba(255,255,255,.05);--border:rgba(255,255,255,.08);}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);touch-action:none;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;display:flex;align-items:center;justify-content:center;}
#gc{display:block;}
/* HUD */
#hud{position:absolute;top:0;left:0;right:0;z-index:60;pointer-events:none;background:linear-gradient(180deg,rgba(0,0,0,.85)0%,transparent 100%);padding:10px 16px;}
#hud-row{display:flex;align-items:flex-start;gap:8px;}
.hb{background:rgba(0,0,0,.5);border:1px solid var(--border);border-radius:10px;padding:5px 12px;text-align:center;}
.hv{font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:#fff;letter-spacing:1px;line-height:1.1;}
.hl{font-size:7px;color:#445;letter-spacing:3px;text-transform:uppercase;}
#hv-speed{color:var(--cyan);font-size:26px;}
#hud-right{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:5px;}
#lives-row{display:flex;gap:4px;}
.lp{width:13px;height:13px;border-radius:50%;background:var(--red);box-shadow:0 0 8px rgba(255,34,68,.8);transition:all .3s;}
.lp.dead{background:#1a0408;box-shadow:none;}
#wanted-row{display:flex;gap:3px;align-items:center;}
.ws{font-size:13px;filter:grayscale(1);opacity:.25;transition:all .2s;}
.ws.lit{filter:none;opacity:1;text-shadow:0 0 8px rgba(255,215,0,.9);}
#center-hud{position:absolute;top:10px;left:50%;transform:translateX(-50%);z-index:65;pointer-events:none;text-align:center;}
#dist-val{font-family:'Rajdhani',sans-serif;font-size:24px;font-weight:900;color:#fff;letter-spacing:2px;}
#dist-lbl{font-size:7px;color:#336;letter-spacing:3px;}
#combo-wrap{position:absolute;top:66px;right:16px;z-index:65;pointer-events:none;text-align:right;}
#combo-num{font-family:'Black Han Sans',sans-serif;font-size:30px;letter-spacing:2px;text-shadow:0 0 20px currentColor;opacity:0;transition:opacity .15s;line-height:1;}
#combo-lbl{font-size:7px;color:#444;letter-spacing:3px;}
#nitro-wrap{position:absolute;bottom:90px;left:50%;transform:translateX(-50%);width:min(210px,52vw);z-index:65;pointer-events:none;text-align:center;}
#nitro-lbl{font-size:7px;color:rgba(0,212,255,.5);letter-spacing:3px;margin-bottom:3px;}
#nitro-track{display:flex;gap:2px;}
.ns{flex:1;height:6px;border-radius:99px;background:rgba(0,212,255,.07);border:1px solid rgba(0,212,255,.12);overflow:hidden;}
.nf{height:100%;background:linear-gradient(90deg,#006688,#00d4ff,#88ffff);border-radius:99px;width:0%;transition:width .04s;}
#gear-box{position:absolute;bottom:92px;right:16px;z-index:65;pointer-events:none;background:rgba(0,0,0,.5);border:1.5px solid var(--border);border-radius:10px;padding:4px 10px;text-align:center;}
#gear-num{font-family:'Black Han Sans',sans-serif;font-size:24px;color:var(--gold);text-shadow:0 0 12px rgba(245,197,24,.6);}
#gear-lbl{font-size:7px;color:#445;letter-spacing:2px;}
#minimap-box{position:absolute;top:60px;left:14px;z-index:65;pointer-events:none;width:78px;height:78px;border-radius:50%;overflow:hidden;background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.1);}
#mm{width:100%;height:100%;display:block;}
#weather-box{position:absolute;top:62px;right:14px;z-index:65;pointer-events:none;text-align:center;}
#w-ico{font-size:20px;}
#w-lbl{font-size:7px;color:#446;letter-spacing:1px;}
#boost-ov{position:absolute;inset:0;z-index:70;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,rgba(0,212,255,.18)0%,transparent 65%);transition:opacity .05s;}
#hit-vig{position:absolute;inset:0;z-index:72;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,transparent 35%,rgba(255,0,30,.55)100%);transition:opacity .12s;}
#drift-ov{position:absolute;inset:0;z-index:67;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,transparent 50%,rgba(255,119,0,.12)100%);transition:opacity .1s;}
#shield-ov{position:absolute;inset:0;z-index:66;pointer-events:none;opacity:0;background:rgba(192,79,255,.04);}
#slow-ov{position:absolute;inset:0;z-index:66;pointer-events:none;opacity:0;box-shadow:inset 0 0 0 5px rgba(255,119,0,.4);}
#announce{position:absolute;top:44%;left:50%;transform:translate(-50%,-50%);z-index:90;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-size:clamp(20px,5vw,34px);letter-spacing:4px;text-shadow:0 0 28px currentColor;opacity:0;transition:opacity .2s;text-align:center;white-space:nowrap;}
/* DPAD */
#dpad{position:absolute;bottom:14px;left:14px;z-index:100;display:grid;grid-template-columns:60px 60px 60px;grid-template-rows:56px 56px;gap:5px;}
.dp{border-radius:12px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;user-select:none;-webkit-user-select:none;touch-action:none;transition:all .1s;}
.dp:active,.dp.pr{background:rgba(0,212,255,.18);border-color:rgba(0,212,255,.55);box-shadow:0 0 14px rgba(0,212,255,.35);transform:scale(.93);}
#dp-up{grid-column:2;grid-row:1;}#dp-left{grid-column:1;grid-row:2;}#dp-down{grid-column:2;grid-row:2;}#dp-right{grid-column:3;grid-row:2;}
#nitro-btn{position:absolute;bottom:14px;right:14px;z-index:100;width:80px;height:80px;border-radius:50%;background:rgba(0,212,255,.1);border:2px solid rgba(0,212,255,.38);display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:26px;cursor:pointer;user-select:none;-webkit-user-select:none;touch-action:none;transition:all .1s;}
#nitro-btn:active,#nitro-btn.pr{background:rgba(0,212,255,.32);box-shadow:0 0 24px rgba(0,212,255,.58);transform:scale(.91);}
.nb-lbl{font-size:7px;color:var(--cyan);letter-spacing:2px;margin-top:2px;}
/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(3,6,15,.94);backdrop-filter:blur(5px);}
.ov-wrap{text-align:center;max-width:480px;width:93vw;padding:32px 22px;background:linear-gradient(160deg,rgba(5,10,20,.98),rgba(8,15,28,.98));border:1px solid rgba(0,212,255,.18);border-radius:22px;box-shadow:0 0 80px rgba(0,212,255,.07);}
.ov-eye{font-size:7px;letter-spacing:5px;color:var(--cyan);background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.2);border-radius:99px;padding:3px 14px;display:inline-block;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(24px,6vw,40px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#334;letter-spacing:4px;margin-bottom:16px;}
.car-row{display:flex;gap:8px;margin-bottom:14px;overflow-x:auto;padding-bottom:2px;}
.car-row::-webkit-scrollbar{height:3px;}
.car-row::-webkit-scrollbar-thumb{background:rgba(0,212,255,.3);border-radius:99px;}
.cc{min-width:88px;flex:1;padding:9px 5px;background:var(--glass);border:1.5px solid var(--border);border-radius:12px;cursor:pointer;transition:all .2s;text-align:center;}
.cc:hover{border-color:rgba(0,212,255,.38);}
.cc.sel{border-color:var(--cyan);background:rgba(0,212,255,.1);box-shadow:0 0 16px rgba(0,212,255,.2);}
.cc-ico{font-size:28px;display:block;margin-bottom:3px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:10px;letter-spacing:1px;}
.cc-stat{font-size:7px;color:#446;margin-top:3px;line-height:1.6;}
.sb{height:4px;border-radius:99px;margin-top:3px;background:rgba(255,255,255,.06);overflow:hidden;}
.sbf{height:100%;border-radius:99px;}
.tab-row{display:flex;gap:6px;justify-content:center;margin-bottom:12px;flex-wrap:wrap;}
.tb{padding:7px 13px;border-radius:99px;background:var(--glass);border:1px solid var(--border);font-size:9px;color:#556;cursor:pointer;transition:all .18s;text-align:center;}
.tb.sel{border-color:var(--gold);color:var(--gold);background:rgba(245,197,24,.08);}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.sc{padding:6px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.sv{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:#fff;}
.sl{font-size:7px;color:#446;letter-spacing:2px;}
.go-btn{display:inline-block;padding:13px 36px;background:linear-gradient(135deg,rgba(0,212,255,.22),rgba(108,99,255,.15));border:1px solid rgba(0,212,255,.5);border-radius:13px;font-family:'Black Han Sans',sans-serif;font-size:18px;color:var(--cyan);letter-spacing:2px;cursor:pointer;transition:all .22s;margin-top:2px;}
.go-btn:hover{background:linear-gradient(135deg,rgba(0,212,255,.4),rgba(108,99,255,.28));transform:translateY(-3px);box-shadow:0 12px 32px rgba(0,212,255,.35);}
.tag-strip{overflow:hidden;margin-bottom:14px;}
.tag-inner{display:flex;gap:8px;animation:tgs 16s linear infinite;width:max-content;}
@keyframes tgs{0%{transform:translateX(0);}100%{transform:translateX(-50%)}}
.tpill{font-size:8px;border:1px solid var(--border);border-radius:99px;padding:3px 11px;white-space:nowrap;letter-spacing:1px;color:#445;}
.tpill.c{color:var(--cyan);border-color:rgba(0,212,255,.3);}
.tpill.g{color:var(--gold);border-color:rgba(245,197,24,.3);}
.tpill.r{color:var(--red);border-color:rgba(255,34,68,.3);}
.tpill.p{color:var(--purple);border-color:rgba(192,79,255,.3);}
</style>
</head>
<body>
<div id="root">
  <canvas id="gc"></canvas>
  <div id="hud">
    <div id="hud-row">
      <div class="hb"><div class="hv" id="hv-score">0</div><div class="hl">SCORE</div></div>
      <div class="hb"><div class="hv" id="hv-speed">0</div><div class="hl">KM/H</div></div>
      <div id="hud-right">
        <div id="lives-row"></div>
        <div id="wanted-row">
          <span style="font-size:7px;color:#445;letter-spacing:2px;margin-right:3px">WANTED</span>
          <span class="ws" id="ws0">⭐</span><span class="ws" id="ws1">⭐</span><span class="ws" id="ws2">⭐</span><span class="ws" id="ws3">⭐</span><span class="ws" id="ws4">⭐</span>
        </div>
      </div>
    </div>
  </div>
  <div id="center-hud"><div id="dist-val">0.00</div><div id="dist-lbl">KM</div></div>
  <div id="combo-wrap"><div id="combo-num" style="color:var(--gold)">×3</div><div id="combo-lbl">COMBO</div></div>
  <div id="nitro-wrap"><div id="nitro-lbl">NITRO</div><div id="nitro-track"></div></div>
  <div id="gear-box"><div id="gear-num">N</div><div id="gear-lbl">GEAR</div></div>
  <div id="minimap-box"><canvas id="mm" width="78" height="78"></canvas></div>
  <div id="weather-box"><div id="w-ico">☀️</div><div id="w-lbl">CLEAR</div></div>
  <div id="boost-ov"></div>
  <div id="hit-vig"></div>
  <div id="drift-ov"></div>
  <div id="shield-ov"></div>
  <div id="slow-ov"></div>
  <div id="announce"></div>
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
// ================================================================
//  네온 도주 레이싱 v3.0
//  Pseudo-3D Perspective Road (Outrun style segment renderer)
//  드리프트 물리 · 기어 시스템 · 경찰 추격 AI · 날씨 4종
//  수배 레벨(5성) · 파워업 6종 · 미니맵 · 파티클 · 콤보×8
// ================================================================
const canvas=document.getElementById('gc');
const ctx=canvas.getContext('2d');
const mmCv=document.getElementById('mm');
const mmCtx=mmCv.getContext('2d');
const root=document.getElementById('root');

// VIEWPORT
let VW=420,VH=720,SC=1;
function resize(){
  const rw=root.clientWidth,rh=root.clientHeight;
  SC=Math.min(rw/VW,rh/VH);
  canvas.width=VW;canvas.height=VH;
  canvas.style.width=(VW*SC)+'px';canvas.style.height=(VH*SC)+'px';
}
resize();window.addEventListener('resize',resize);

// INPUT
const KEYS={};
window.addEventListener('keydown',e=>{KEYS[e.code]=true;['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)&&e.preventDefault();});
window.addEventListener('keyup',e=>KEYS[e.code]=false);

// ================================================================
//  PSEUDO-3D ROAD ENGINE (Outrun/SNES F-Zero approach)
//  Each segment has a curve value; we project them in screen space
//  by accumulating curve offset as we render from back to front.
// ================================================================
const SEG_LEN   = 200;    // world units per segment
const ROAD_W    = 2000;   // road half-width in world units
const CAM_H     = 1500;   // camera height above road
const CAM_DEPTH = 0.84;   // perspective constant
const DRAW_SEGS = 180;    // how many segments we render
const TRACK_N   = 400;    // total segments in looping track

// Segment color pairs (light / dark alternating)
const COL={
  road_l:'#0c1422', road_d:'#09101e',
  grass_l:'#0a1c0d',grass_d:'#081408',
  rumble_l:'#cc2244',rumble_d:'#0e1a2e',
  lane_l:'rgba(255,255,255,.20)',lane_d:null,
  curb_l:'#ffffff', curb_d:'#cc2244',
};

let SEGS=[];

function makeSeg(curve,hillY){
  const i=SEGS.length;
  return{
    i,curve,hillY:hillY||0,
    p1:{world:{z:i*SEG_LEN},scr:{}},
    p2:{world:{z:(i+1)*SEG_LEN},scr:{}},
    isLight:Math.floor(i/3)%2===0,
    cars:[],powers:[]
  };
}

function buildTrack(){
  SEGS=[];
  const add=(n,c,dy)=>{for(let i=0;i<n;i++)SEGS.push(makeSeg(c||0,dy||0));};
  add(60);        // straight start
  add(50,-0.6);   // gentle left
  add(30);
  add(40,3.2);    // sharp right
  add(20);
  add(50,-2.5,25);// left + uphill
  add(15,0,-20);  // downhill
  add(40);
  add(25,3.0);    // chicane right
  add(25,-3.0);
  add(30);
  add(60,-1.0);   // long sweeper left
  add(30);
  add(20,4.5);    // hairpin
  add(60);
  // Accumulate hill heights
  let yAcc=0;
  SEGS.forEach(s=>{s.p1.world.y=yAcc;yAcc+=s.hillY;s.p2.world.y=yAcc;});
}

// Project world point → screen
function proj(p,camX,camY,camZ,depth){
  p.cam={};
  p.cam.x=(p.world.x||0)-camX;
  p.cam.y=(p.world.y||0)-camY;
  p.cam.z=(p.world.z||0)-camZ;
  if(p.cam.z<=0){p.scr.scale=0;return;}
  p.scr.scale=depth/p.cam.z;
  p.scr.x=Math.round((1+p.scr.scale*p.cam.x)*VW/2);
  p.scr.y=Math.round((1-p.scr.scale*p.cam.y)*VH/2);
  p.scr.w=Math.round(p.scr.scale*ROAD_W*VW/2);
}

function segAt(z){
  const i=Math.floor(z/SEG_LEN)%SEGS.length;
  return SEGS[(i+SEGS.length)%SEGS.length];
}

// Draw a road segment trapezoid
function drawSeg(x1,y1,w1,x2,y2,w2,col,fog,light){
  const r1=Math.max(4,w1*0.06),r2=Math.max(4,w2*0.06);
  // Grass
  const gc=fog?'#06090e':light?COL.grass_l:COL.grass_d;
  ctx.fillStyle=gc;ctx.fillRect(0,y2,VW,y1-y2);
  // Rumble strips
  const rc=fog?'#0e1a2e':light?COL.rumble_l:COL.rumble_d;
  poly(x1-w1-r1,y1,x1-w1,y1,x2-w2,y2,x2-w2-r2,y2,rc);
  poly(x1+w1+r1,y1,x1+w1,y1,x2+w2,y2,x2+w2+r2,y2,rc);
  // Road surface
  const road=fog?'#060a14':light?COL.road_l:COL.road_d;
  poly(x1-w1,y1,x1+w1,y1,x2+w2,y2,x2-w2,y2,road);
  // Lane marking
  if(light){
    const lw1=w1*0.06,lw2=w2*0.06;
    poly(x1-lw1,y1,x1+lw1,y1,x2+lw2,y2,x2-lw2,y2,COL.lane_l);
    // side lane lines (dividers)
    const dl1=w1*0.65,dl2=w2*0.65;
    poly(x1-dl1-lw1,y1,x1-dl1+lw1,y1,x2-dl2+lw2,y2,x2-dl2-lw2,y2,'rgba(255,255,255,.1)');
    poly(x1+dl1-lw1,y1,x1+dl1+lw1,y1,x2+dl2+lw2,y2,x2+dl2-lw2,y2,'rgba(255,255,255,.1)');
  }
}

function poly(x1,y1,x2,y2,x3,y3,x4,y4,c){
  if(!c)return;
  ctx.fillStyle=c;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.lineTo(x3,y3);ctx.lineTo(x4,y4);ctx.closePath();ctx.fill();
}

// ================================================================
//  GAME DATA
// ================================================================
const CAR_DEFS=[
  {name:'스포츠',emoji:'🚗',top:175,acc:0.42,brk:0.72,hand:3.4,drift:0.88,nitro:1.85,hp:3,col:'#00d4ff',bars:[75,65,65,60]},
  {name:'슈퍼카',emoji:'🏎️',top:240,acc:0.68,brk:0.58,hand:2.7,drift:0.77,nitro:2.2, hp:2,col:'#ff2244',bars:[100,90,45,40]},
  {name:'SUV',   emoji:'🚙',top:148,acc:0.36,brk:0.92,hand:4.6,drift:0.96,nitro:1.55,hp:4,col:'#00ff88',bars:[60,48,92,88]},
  {name:'머슬카',emoji:'🚘',top:193,acc:0.56,brk:0.62,hand:3.1,drift:0.80,nitro:2.0, hp:3,col:'#f5c518',bars:[85,80,60,55]},
];

const TRF=[
  {emoji:'🚌',spd:55, pts:20,cop:false,w:120},
  {emoji:'🚛',spd:48, pts:30,cop:false,w:130},
  {emoji:'🚓',spd:145,pts:10,cop:true, w:100},
  {emoji:'🏍️',spd:130,pts:12,cop:false,w:55 },
  {emoji:'🚑',spd:78, pts:22,cop:false,w:110},
  {emoji:'🚜',spd:38, pts:35,cop:false,w:130},
  {emoji:'🚐',spd:68, pts:18,cop:false,w:108},
  {emoji:'🛻',spd:72, pts:20,cop:false,w:100},
];

const PWR=[
  {emoji:'⚡',type:'nitro', col:'#00d4ff',label:'NITRO +60%'},
  {emoji:'⭐',type:'score', col:'#f5c518',label:'+500 BONUS'},
  {emoji:'💊',type:'heal',  col:'#00ff88',label:'HP 회복!'},
  {emoji:'🔱',type:'shield',col:'#c04fff',label:'무적 5초'},
  {emoji:'🌀',type:'slow',  col:'#ff7700',label:'슬로우 모션'},
  {emoji:'💨',type:'boost', col:'#88ffff',label:'가속 부스터'},
];

const WEATHER=[
  {name:'맑음',ico:'☀️',fog:false,rain:0,   spdM:1.0, gripM:1.0 },
  {name:'비',  ico:'🌧️',fog:true, rain:0.55, spdM:0.9, gripM:0.72},
  {name:'폭풍',ico:'⛈️',fog:true, rain:0.88, spdM:0.78,gripM:0.58},
  {name:'야간',ico:'🌙',fog:false,rain:0,   spdM:1.05,gripM:1.0 },
];

// ================================================================
//  PARTICLES + FLOATERS
// ================================================================
let PARTS=[],FLOATS=[];
function spawnP(x,y,o={}){
  const n=o.n||8;
  for(let i=0;i<n;i++){
    const a=o.dir!==undefined?o.dir+(Math.random()-.5)*(o.spread||Math.PI*2):Math.random()*Math.PI*2;
    const v=(o.vMin||1)+Math.random()*(o.vMax||4);
    const cols=Array.isArray(o.col)?o.col:[o.col||'#fff'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      dec:(o.dMin||.025)+Math.random()*(o.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(o.szMin||2)+Math.random()*(o.szMax||5),glow:o.glow||false});
  }
}
function spawnF(x,y,t,c){FLOATS.push({x,y:y-10,t,c,life:1,vy:-.6});}
function tickP(){for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.dec;p.life<=0&&PARTS.splice(i,1);}}
function tickF(){for(let i=FLOATS.length-1;i>=0;i--){const f=FLOATS[i];f.y+=f.vy;f.life-=.022;f.life<=0&&FLOATS.splice(i,1);}}
function drawP(){ctx.save();for(const p of PARTS){ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*3;}ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.1,p.life),0,Math.PI*2);ctx.fill();if(p.glow)ctx.shadowBlur=0;}ctx.globalAlpha=1;ctx.restore();}
function drawF(){ctx.save();for(const f of FLOATS){ctx.globalAlpha=Math.max(0,f.life);ctx.shadowColor=f.c;ctx.shadowBlur=8;ctx.fillStyle=f.c;ctx.font="bold 14px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(f.t,f.x,f.y);}ctx.shadowBlur=0;ctx.globalAlpha=1;ctx.restore();}

// RAIN
let RAIN=[];
function initRain(){RAIN=[];for(let i=0;i<200;i++)RAIN.push({x:Math.random()*VW,y:Math.random()*VH,len:8+Math.random()*16,spd:11+Math.random()*10});}
function drawRain(a){
  if(a<=0)return;
  ctx.save();ctx.globalAlpha=a*.6;ctx.strokeStyle='#88ccff';ctx.lineWidth=.8;
  for(const r of RAIN){r.y+=r.spd;r.x-=1.4;if(r.y>VH){r.y=-r.len;r.x=Math.random()*VW;}if(r.x<0){r.x=VW;r.y=Math.random()*VH;}ctx.beginPath();ctx.moveTo(r.x,r.y);ctx.lineTo(r.x+1.5,r.y+r.len);ctx.stroke();}
  ctx.restore();
}

// ================================================================
//  GAME STATE
// ================================================================
let selCar=0,diffLv=1,weatherIdx=0,G={},raf=null;

function initGame(){
  buildTrack();initRain();
  const car=CAR_DEFS[selCar];
  const dm=[.72,1.0,1.38][diffLv];
  const W=WEATHER[weatherIdx];
  G={
    running:true,dead:false,frame:0,
    score:0,dist:0,
    // player track position
    pZ:0,pX:0,pVX:0,
    speed:0,
    drift:false,driftAngle:0,
    nitro:100,nitroOn:false,
    gear:1,
    hp:car.hp,maxHp:car.hp,
    shieldT:0,slowT:0,boostT:0,flashT:0,
    combo:1,comboD:0,
    wanted:0,wantedD:0,
    dm,W,
    camX:0,
    traffic:[],spawnT:0,
    powers:[],powerT:0,
    trackLen:SEGS.length*SEG_LEN,
    _ann:null,
  };
  buildNitroUI();buildLives();
  PARTS=[];FLOATS=[];
  // pre-spawn traffic
  for(let i=0;i<8;i++)spawnTrf();
}

function buildNitroUI(){
  const t=document.getElementById('nitro-track');t.innerHTML='';
  for(let i=0;i<10;i++){const s=document.createElement('div');s.className='ns';const f=document.createElement('div');f.className='nf';s.appendChild(f);t.appendChild(s);}
}
function updNitro(){document.querySelectorAll('.ns .nf').forEach((f,i)=>f.style.width=Math.min(100,Math.max(0,(G.nitro-i*10)*10))+'%');}
function buildLives(){
  const r=document.getElementById('lives-row');r.innerHTML='';
  for(let i=0;i<G.maxHp;i++){const p=document.createElement('div');p.className='lp'+(i>=G.hp?' dead':'');p.id='lp'+i;r.appendChild(p);}
}
function updLives(){for(let i=0;i<G.maxHp;i++){const p=document.getElementById('lp'+i);if(p)p.classList.toggle('dead',i>=G.hp);}}
function updWanted(){for(let i=0;i<5;i++)document.getElementById('ws'+i)?.classList.toggle('lit',i<G.wanted);}

let uid=0;
function spawnTrf(){
  const def=TRF[Math.floor(Math.random()*TRF.length)];
  if(def.cop&&G.wanted<2)return;
  const z=(G.pZ+350+Math.random()*G.trackLen*.75)%G.trackLen;
  const x=(Math.random()-.5)*1.4;
  G.traffic.push({id:uid++,z,x,spd:def.spd*G.W.spdM*(1+diffLv*.1),emoji:def.emoji,pts:def.pts,
    isCop:def.cop,w:def.w,alive:true,scored:false,flash:0,siren:0});
}
function spawnPwr(){
  const def=PWR[Math.floor(Math.random()*PWR.length)];
  const z=(G.pZ+420+Math.random()*700)%G.trackLen;
  const x=(Math.random()-.5)*1.3;
  G.powers.push({z,x,type:def.type,emoji:def.emoji,col:def.col,label:def.label,alive:true,rot:0});
}

function zDist(a,b){const d=Math.abs(a-b);return Math.min(d,G.trackLen-d);}

// ================================================================
//  UPDATE
// ================================================================
function update(){
  if(!G.running||G.dead)return;
  G.frame++;
  const car=CAR_DEFS[selCar];
  const W=G.W;

  // --- Input ---
  const up   =KEYS['ArrowUp']   ||KEYS['KeyW']||G._tUp;
  const down =KEYS['ArrowDown'] ||KEYS['KeyS']||G._tDown;
  const left =KEYS['ArrowLeft'] ||KEYS['KeyA']||G._tLeft;
  const right=KEYS['ArrowRight']||KEYS['KeyD']||G._tRight;
  const nKey =KEYS['Space']||KEYS['ShiftLeft']||G._tNitro;
  const dKey =KEYS['KeyX']||KEYS['ControlLeft'];

  // --- Nitro ---
  if(nKey&&G.nitro>0){G.nitroOn=true;G.nitro=Math.max(0,G.nitro-.65);document.getElementById('boost-ov').style.opacity='.18';}
  else{G.nitroOn=false;G.nitro=Math.min(100,G.nitro+.19);document.getElementById('boost-ov').style.opacity='0';}

  // --- Timers ---
  if(G.shieldT>0)G.shieldT-=1/60;
  if(G.slowT>0)G.slowT-=1/60;
  if(G.boostT>0)G.boostT-=1/60;
  if(G.flashT>0)G.flashT-=.05;
  if(G.comboD>0)G.comboD--;else if(G.combo>1){G.combo=Math.max(1,G.combo-1);G.comboD=100;}
  if(G.wantedD>0)G.wantedD--;else if(G.wanted>0){G.wanted=Math.max(0,G.wanted-1);G.wantedD=600;updWanted();}

  // --- Speed ---
  const grip=W.gripM*(G.drift?.55:1);
  const nitroM=G.nitroOn?car.nitro:(G.boostT>0?1.35:1);
  const spdM=G.slowT>0?.42:W.spdM;
  const topSpd=car.top*nitroM*spdM*(1+G.dm*.1);
  if(up)G.speed=Math.min(topSpd,G.speed+car.acc*nitroM*spdM*(1+G.dm*.05));
  else if(down)G.speed=Math.max(0,G.speed-car.brk*2);
  else G.speed=Math.max(0,G.speed-.8);

  // --- Gear (visual) ---
  const gt=[0,55,95,135,168,210,999];
  for(let g=1;g<=6;g++){if(G.speed<gt[g]){G.gear=g;break;}}

  // --- Steer / Drift ---
  G.drift=dKey&&G.speed>55&&(left||right);
  const sf=G.speed/car.top;
  const steer=car.hand*sf*grip;
  if(left) G.pVX-=steer*(G.drift?2.2:1);
  if(right)G.pVX+=steer*(G.drift?2.2:1);
  if(G.drift){
    G.driftAngle+=(left?-1:right?1:0)*.028;G.driftAngle*=.95;
    document.getElementById('drift-ov').style.opacity='.9';
    if(G.frame%3===0)spawnP(VW/2+G.driftAngle*25,VH*.83,{n:3,col:['rgba(200,200,200,.65)'],vMin:.4,vMax:1.8,dir:Math.PI*.5,spread:.7,szMin:5,szMax:13,dMin:.01,dMax:.018});
  }else{G.driftAngle*=.88;document.getElementById('drift-ov').style.opacity='0';}
  G.pVX*=(G.drift?car.drift:.76);
  const seg=segAt(G.pZ);
  G.pX+=G.pVX*.01-seg.curve*sf*.005;
  // Off-road penalty
  if(Math.abs(G.pX)>.92){G.speed*=.97;if(G.frame%5===0)spawnP(VW/2,VH*.82,{n:2,col:'#5a4a22',vMax:3,szMax:5});}
  G.pX=Math.max(-1,Math.min(1,G.pX));G.pVX=Math.max(-6,Math.min(6,G.pVX));
  // Camera curve
  G.camX+=-seg.curve*sf*.04;G.camX*=.9;
  // Move forward
  const mps=G.speed/3.6;
  G.pZ=(G.pZ+mps*.8)%G.trackLen;
  G.dist+=mps*.001;

  // --- Shield / slow overlays ---
  document.getElementById('shield-ov').style.opacity=G.shieldT>0?'1':'0';
  document.getElementById('slow-ov').style.opacity=G.slowT>0?'1':'0';

  // --- Spawn ---
  G.spawnT--;
  const si=Math.max(55,210-G.speed*.6-diffLv*18);
  if(G.spawnT<=0){
    spawnTrf();
    if(G.speed>75&&Math.random()<.3)spawnTrf();
    if(G.wanted>3&&Math.random()<.4)spawnTrf();
    G.spawnT=si+Math.random()*55;
  }
  G.powerT--;
  if(G.powerT<=0){if(Math.random()<.7)spawnPwr();G.powerT=210+Math.random()*280;}

  // --- Traffic update & collision ---
  for(const tc of G.traffic){
    if(!tc.alive)continue;
    if(tc.isCop&&G.wanted>=2){tc.spd=Math.min(tc.spd+.2,G.speed*1.12+18);}
    tc.z=(tc.z+tc.spd*.008)%G.trackLen;
    if(tc.isCop)tc.siren=(tc.siren+1)%60;
    // Collision
    const dz=zDist(tc.z,G.pZ);
    const dx=Math.abs(tc.x-G.pX)*ROAD_W;
    if(dz<140&&dx<tc.w*.5+28){
      if(G.shieldT>0){
        tc.alive=false;
        spawnP(VW/2,VH*.78,{n:14,col:['#c04fff','#8833ff'],glow:true,vMax:6,szMax:7});
        spawnF(VW/2,VH*.62,'BLOCKED!','#c04fff');G.score+=100;
      }else{
        G.hp--;G.flashT=.9;G.speed=Math.max(0,G.speed*.42);G.combo=1;G.comboD=0;
        G.pVX+=(G.pX<tc.x?-3:3);tc.alive=false;
        spawnP(VW/2,VH*.78,{n:24,col:['#ff2244','#ff6644','#ffaa00'],glow:true,vMax:7,szMax:9});
        document.getElementById('hit-vig').style.opacity='.85';
        setTimeout(()=>document.getElementById('hit-vig').style.opacity='0',380);
        updLives();if(G.hp<=0){G.dead=true;setTimeout(showGO,700);}
      }
    }
    // Score: passed car
    if(!tc.scored&&dz>200&&tc.z<G.pZ){
      tc.scored=true;
      const pts=tc.pts*G.combo;G.score+=pts;G.combo=Math.min(8,G.combo+1);G.comboD=130;
      spawnF(VW/2+(Math.random()-.5)*80,VH*.66,'+'+pts,G.combo>2?'#f5c518':'#00d4ff');
      if(tc.isCop){G.wanted=Math.min(5,G.wanted+1);G.wantedD=600;updWanted();}
      if(G.combo>=3)ann(`×${G.combo} COMBO!`,'#f5c518');
    }
  }
  // Cull
  G.traffic=G.traffic.filter(tc=>tc.alive&&zDist(tc.z,G.pZ)<SEG_LEN*DRAW_SEGS*1.1);
  if(G.traffic.length>28)G.traffic.splice(0,5);

  // --- Power-up collision ---
  for(const pw of G.powers){
    if(!pw.alive)continue;pw.rot+=.07;
    const dz=zDist(pw.z,G.pZ),dx=Math.abs(pw.x-G.pX)*ROAD_W;
    if(dz<110&&dx<180){
      pw.alive=false;
      spawnP(VW/2,VH*.73,{n:14,col:pw.col,glow:true,vMax:6,szMax:7});
      spawnF(VW/2,VH*.62,pw.label,pw.col);
      if(pw.type==='nitro')G.nitro=Math.min(100,G.nitro+60);
      if(pw.type==='score')G.score+=500;
      if(pw.type==='heal'){G.hp=Math.min(G.maxHp,G.hp+1);updLives();}
      if(pw.type==='shield')G.shieldT=5;
      if(pw.type==='slow')G.slowT=4;
      if(pw.type==='boost')G.boostT=6;
    }
  }
  G.powers=G.powers.filter(pw=>pw.alive||zDist(pw.z,G.pZ)<SEG_LEN*DRAW_SEGS*1.2);

  // Passive score
  if(G.frame%5===0)G.score+=Math.max(1,Math.floor(G.speed/40))*G.combo;
  if(G.frame%3===0&&G.nitroOn)G.score+=3;

  // Exhaust particles
  if(G.speed>15&&G.frame%4===0){
    const col=G.nitroOn?CAR_DEFS[selCar].col:'rgba(100,100,120,.6)';
    spawnP(VW/2+G.driftAngle*25,VH*.85,{n:1,col,vMin:.3,vMax:1.5,dir:Math.PI*.5,spread:.5,szMin:2,szMax:G.nitroOn?6:3,dMin:.04,dMax:.07,glow:G.nitroOn});
  }

  tickP();tickF();
  updHUD();
}

// ANNOUNCE
function ann(txt,col){
  const el=document.getElementById('announce');
  el.textContent=txt;el.style.color=col;el.style.opacity='1';
  clearTimeout(G._ann);
  G._ann=setTimeout(()=>el.style.opacity='0',1500);
}

function updHUD(){
  document.getElementById('hv-score').textContent=G.score.toLocaleString();
  document.getElementById('hv-speed').textContent=Math.round(G.speed);
  document.getElementById('dist-val').textContent=G.dist.toFixed(2);
  document.getElementById('gear-num').textContent='N123456'[G.gear]||G.gear;
  updNitro();
  const cn=document.getElementById('combo-num');
  if(G.combo>=2){cn.style.opacity='1';cn.textContent='×'+G.combo;}else cn.style.opacity='0';
}

// ================================================================
//  RENDER ROAD (Pseudo-3D)
// ================================================================
function renderRoad(){
  const W=G.W;
  // Sky
  const isNight=W===WEATHER[3];
  const isRain=W.rain>0;
  const skyG=ctx.createLinearGradient(0,0,0,VH*.5);
  if(isNight){skyG.addColorStop(0,'#010208');skyG.addColorStop(1,'#040820');}
  else if(isRain){skyG.addColorStop(0,'#050810');skyG.addColorStop(1,'#0c141c');}
  else{skyG.addColorStop(0,'#020512');skyG.addColorStop(1,'#060c20');}
  ctx.fillStyle=skyG;ctx.fillRect(0,0,VW,VH);

  // Stars
  if(isNight||(!isRain&&G.frame%2===0)){
    ctx.save();ctx.globalAlpha=isNight?.9:.35;
    for(let s=0;s<100;s++){
      const sx=((s*137.5+s*s*.002)%1)*VW;
      const sy=((s*98.3+s*.4)%.48)*VH;
      ctx.fillStyle=`rgba(255,255,220,.${55+s%45})`;
      ctx.beginPath();ctx.arc(sx,sy,s%7===0?1.1:.55,0,Math.PI*2);ctx.fill();
    }
    ctx.restore();
  }

  // City silhouette
  const hY=VH*.44;
  ctx.fillStyle=isNight?'#010208':'#020508';
  for(let ci=0;ci<16;ci++){
    const bw=22+Math.sin(ci*1.9)*11+7,bh=50+Math.sin(ci*2.4)*48+18;
    const bx=ci*(VW/15.2)-12;
    ctx.fillRect(bx,hY-bh,bw,bh);
    for(let wy=hY-bh+5;wy<hY-4;wy+=11){
      if(Math.random()<.54)continue;
      const lc=Math.random()<.4?'0,200,255':'255,190,50';
      ctx.fillStyle=`rgba(${lc},.26)`;ctx.fillRect(bx+3+Math.floor(Math.random()*(bw-9)),wy,4,7);
      ctx.fillStyle=isNight?'#010208':'#020508';
    }
  }
  // Horizon neon glow
  ctx.save();ctx.shadowColor='rgba(192,79,255,.35)';ctx.shadowBlur=22;
  ctx.strokeStyle='rgba(192,79,255,.15)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(0,hY+2);ctx.lineTo(VW,hY+2);ctx.stroke();ctx.restore();

  // -- Segment render --
  const cameraDepth=CAM_DEPTH;
  const pSegIdx=Math.floor(G.pZ/SEG_LEN)%SEGS.length;
  const cameraZ=G.pZ;
  const camY=CAM_H+(segAt(G.pZ).p1.world.y||0);

  let curveX=0,maxY=VH;

  for(let n=0;n<DRAW_SEGS;n++){
    const idx=(pSegIdx+n)%SEGS.length;
    const seg=SEGS[idx];
    // Segment world Z relative to camera
    let wz1=seg.p1.world.z-cameraZ;
    let wz2=seg.p2.world.z-cameraZ;
    // Handle track wrap
    if(wz1<0)wz1+=G.trackLen;
    if(wz2<0)wz2+=G.trackLen;
    if(wz1<=0||wz2<=0)continue;

    const sc1=cameraDepth/wz1,sc2=cameraDepth/wz2;
    const wy1=seg.p1.world.y||0,wy2=seg.p2.world.y||0;
    const sx1=(VW/2)+(sc1*(G.pX*ROAD_W+G.camX*ROAD_W*.3-curveX))*VW;
    const sy1=(VH/2)-(sc1*(camY-wy1))*VH;
    const sw1=sc1*ROAD_W*VW;
    curveX+=seg.curve;
    const sx2=(VW/2)+(sc2*(G.pX*ROAD_W+G.camX*ROAD_W*.3-curveX))*VW;
    const sy2=(VH/2)-(sc2*(camY-wy2))*VH;
    const sw2=sc2*ROAD_W*VW;

    if(sy2>=maxY)continue;
    maxY=sy2;

    // Fog (distance)
    const fogT=W.fog?Math.min(.9,n/DRAW_SEGS*1.8):0;
    const light=seg.isLight;
    drawSeg(sx1,sy1,sw1,sx2,sy2,sw2,null,fogT>.5,light);

    // Render traffic in this segment
    G.traffic.forEach(tc=>{
      if(!tc.alive)return;
      const ti=Math.floor(tc.z/SEG_LEN)%SEGS.length;
      if(ti!==idx)return;
      const ts=sc1*.9;
      const tx=sx1+ts*(tc.x-G.pX)*ROAD_W*.5;
      const ty=sy1-ts*220;
      const tsz=Math.max(10,ts*580);
      drawVehSprite(tc.emoji,tx,ty,tsz,tc.isCop?tc.siren:0);
    });
    // Powers
    G.powers.forEach(pw=>{
      if(!pw.alive)return;
      const pi=Math.floor(pw.z/SEG_LEN)%SEGS.length;
      if(pi!==idx)return;
      const ps=sc1*.9;
      const px=sx1+ps*(pw.x-G.pX)*ROAD_W*.5;
      const py=sy1-ps*160;
      const psz=Math.max(8,ps*380);
      drawPwrSprite(pw.emoji,pw.col,px,py,psz,pw.rot);
    });
  }
}

function drawVehSprite(emoji,x,y,sz,siren){
  if(sz<8||y<-10||y>VH+10||x<-sz*2||x>VW+sz*2)return;
  ctx.save();
  if(siren>0){const c=Math.floor(siren/10)%2===0?'rgba(0,80,255,.55)':'rgba(255,30,30,.55)';ctx.shadowColor=c;ctx.shadowBlur=sz*.6;}
  ctx.font=sz+'px serif';ctx.textAlign='center';ctx.textBaseline='bottom';ctx.fillText(emoji,x,y);
  ctx.restore();
}
function drawPwrSprite(emoji,col,x,y,sz,rot){
  if(sz<8||y<-10||y>VH+10)return;
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);
  ctx.shadowColor=col;ctx.shadowBlur=sz*.55;
  ctx.font=sz+'px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(emoji,0,0);
  ctx.restore();
}

function drawPlayerCar(){
  const car=CAR_DEFS[selCar];
  const cx=VW/2,cy=VH*.83;
  const tilt=G.pVX*5+G.driftAngle*16;
  const bob=Math.sin(G.frame*.22)*(G.speed>8?1.4:0);
  // Shadow
  ctx.save();ctx.fillStyle='rgba(0,0,0,.34)';ctx.beginPath();ctx.ellipse(cx,cy+26,38,10,0,0,Math.PI*2);ctx.fill();ctx.restore();
  // Underbody glow
  const ug=ctx.createRadialGradient(cx,cy+20,0,cx,cy+20,52);
  ug.addColorStop(0,G.nitroOn?car.col+'66':car.col+'22');ug.addColorStop(1,'transparent');
  ctx.fillStyle=ug;ctx.beginPath();ctx.ellipse(cx,cy+24,48,16,0,0,Math.PI*2);ctx.fill();
  // Shield ring
  if(G.shieldT>0){
    ctx.save();const sr=Math.sin(G.frame*.16)*.3+.7;
    ctx.globalAlpha=sr;ctx.strokeStyle='#c04fff';ctx.shadowColor='#c04fff';ctx.shadowBlur=18;ctx.lineWidth=3;
    ctx.beginPath();ctx.ellipse(cx,cy-10,40,54,0,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  // Nitro exhaust
  if(G.nitroOn){
    for(let j=0;j<3;j++){
      ctx.save();ctx.globalAlpha=.5+Math.random()*.4;ctx.font='18px serif';ctx.textAlign='center';
      ctx.shadowColor=car.col;ctx.shadowBlur=16;ctx.fillText('🔥',cx+(j-1)*8,cy+32+j*5+Math.random()*4);ctx.restore();
    }
  }
  // Car
  ctx.save();ctx.translate(cx,cy+bob);ctx.rotate(tilt*Math.PI/180);
  if(G.flashT>0&&Math.floor(G.flashT*12)%2===0)ctx.filter='brightness(4) saturate(0)';
  if(G.nitroOn){ctx.shadowColor=car.col;ctx.shadowBlur=22;}
  ctx.font='60px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(car.emoji,0,0);
  ctx.restore();
}

function drawMinimap(){
  const W=78,H=78,cx=39,cy=39,r=30;
  mmCtx.clearRect(0,0,W,H);
  // Track ring
  mmCtx.strokeStyle='rgba(255,255,255,.12)';mmCtx.lineWidth=8;
  mmCtx.beginPath();mmCtx.arc(cx,cy,r,0,Math.PI*2);mmCtx.stroke();
  // Traffic dots
  for(const tc of G.traffic){
    if(!tc.alive)continue;
    const a=(tc.z/G.trackLen)*Math.PI*2-Math.PI/2;
    const tx=cx+Math.cos(a)*r,ty=cy+Math.sin(a)*r;
    mmCtx.fillStyle=tc.isCop?'#4466ff':'#ff6633';
    mmCtx.beginPath();mmCtx.arc(tx,ty,2.2,0,Math.PI*2);mmCtx.fill();
  }
  // Player dot
  const pa=(G.pZ/G.trackLen)*Math.PI*2-Math.PI/2;
  const px=cx+Math.cos(pa)*r,py=cy+Math.sin(pa)*r;
  const cc=CAR_DEFS[selCar].col;
  mmCtx.fillStyle=cc;mmCtx.shadowColor=cc;mmCtx.shadowBlur=6;
  mmCtx.beginPath();mmCtx.arc(px,py,4,0,Math.PI*2);mmCtx.fill();
  mmCtx.shadowBlur=0;
}

// ================================================================
//  MAIN LOOP
// ================================================================
function loop(){
  if(!G.running)return;
  ctx.clearRect(0,0,VW,VH);
  renderRoad();
  drawPlayerCar();
  drawP();drawF();
  drawRain(G.W.rain);
  drawMinimap();
  update();
  raf=requestAnimationFrame(loop);
}

// ================================================================
//  UI: TITLE & GAMEOVER
// ================================================================
function showTitle(){
  const best=parseInt(localStorage.getItem('neonRaceBest')||'0');
  const tags=['🏎️ 투시 3D 도로','⚡ 니트로 부스터','🚓 경찰 추격 AI','🌧️ 날씨 4종','💨 드리프트 물리','⭐ 수배 레벨 5성','🎯 파워업 6종','×8 콤보 배율','🛡️ 무적 실드','🌙 야간 모드','🗺️ 미니맵','⚙️ 6단 기어'];
  const tp=[...tags,...tags].map((t,i)=>`<span class="tpill ${['c','g','r','p'][i%4]}">${t}</span>`).join('');
  const wn=['맑음 ☀️','비 🌧️','폭풍 ⛈️','야간 🌙'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">NEON HIGHWAY ESCAPE v3.0</div>
    <div class="ov-title" style="color:var(--cyan)">🏎️<br>네온 도주 레이싱</div>
    <div class="ov-sub">PSEUDO-3D · DRIFT · POLICE AI · WEATHER</div>
    <div class="tag-strip"><div class="tag-inner">${tp}</div></div>
    <div class="car-row" id="cr"></div>
    <div style="font-size:8px;color:#336;margin-bottom:8px;letter-spacing:2px">난이도</div>
    <div class="tab-row" id="dt">${['신병 🟢','특전사 🟡','전설 🔴'].map((n,i)=>`<div class="tb${i===diffLv?' sel':''}" onclick="setDiff(${i})">${n}</div>`).join('')}</div>
    <div style="font-size:8px;color:#336;margin-bottom:8px;letter-spacing:2px">날씨</div>
    <div class="tab-row" id="wt">${wn.map((n,i)=>`<div class="tb${i===weatherIdx?' sel':''}" onclick="setWeather(${i})">${n}</div>`).join('')}</div>
    <div style="font-size:8px;color:#334;line-height:2.2;margin-bottom:12px">↑↓ — 가속/감속 &nbsp;|&nbsp; ←→ — 조향<br>SPACE/SHIFT — 니트로 &nbsp;|&nbsp; X/CTRL — 드리프트<br>경찰을 따돌리고 수배 레벨을 낮춰라!</div>
    ${best>0?`<div style="font-size:9px;color:#446;margin-bottom:12px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>`:''}
    <div class="go-btn" onclick="startGame()">시동 걸기 🚀</div>`;
  buildCarRow();
  document.getElementById('overlay').style.display='flex';
}

function buildCarRow(){
  const g=document.getElementById('cr');if(!g)return;g.innerHTML='';
  const bnames=['최고속','가속','내구','핸들'];
  CAR_DEFS.forEach((c,i)=>{
    const d=document.createElement('div');d.className='cc'+(i===selCar?' sel':'');
    const bH=c.bars.map((v,bi)=>`<div style="display:flex;align-items:center;gap:3px;margin-top:2px"><div style="font-size:6px;color:#445;width:22px">${bnames[bi]}</div><div class="sb" style="flex:1"><div class="sbf" style="width:${v}%;background:${c.col}"></div></div></div>`).join('');
    d.innerHTML=`<span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-stat">${['4종 균형','극한 속도','고내구 안정','강한 가속'][i]}</div>${bH}`;
    d.onclick=()=>{selCar=i;document.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};
    g.appendChild(d);
  });
}

window.setDiff=d=>{diffLv=d;document.querySelectorAll('#dt .tb').forEach((t,i)=>t.classList.toggle('sel',i===d));};
window.setWeather=w=>{weatherIdx=w;document.querySelectorAll('#wt .tb').forEach((t,i)=>t.classList.toggle('sel',i===w));};

function showGO(){
  G.running=false;cancelAnimationFrame(raf);
  const best=Math.max(G.score,parseInt(localStorage.getItem('neonRaceBest')||'0'));
  localStorage.setItem('neonRaceBest',best);
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">${G.score>=best&&G.score>0?'🏆 NEW RECORD!':'GAME OVER'}</div>
    <div class="ov-title" style="color:var(--red)">💥 충돌!</div>
    <div class="ov-sub">YOU CRASHED</div>
    <div class="stats-row">
      <div class="sc"><div class="sv" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="sl">점수</div></div>
      <div class="sc"><div class="sv" style="color:var(--cyan)">${G.dist.toFixed(2)}<small style="font-size:10px"> km</small></div><div class="sl">주행</div></div>
      <div class="sc"><div class="sv" style="color:var(--green)">×${G.combo}</div><div class="sl">콤보</div></div>
      <div class="sc"><div class="sv">${Math.round(G.speed)}<small style="font-size:10px"> km/h</small></div><div class="sl">속도</div></div>
    </div>
    <div style="font-size:9px;color:#446;margin-bottom:14px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>
    <div class="go-btn" onclick="startGame()">다시 도주 🏎️</div>
    <br><div class="go-btn" style="margin-top:10px;font-size:13px;padding:9px 22px;color:#667;border-color:rgba(255,255,255,.1)" onclick="showTitle()">차량·설정 변경</div>`;
  document.getElementById('overlay').style.display='flex';
}

window.startGame=function(){
  document.getElementById('overlay').style.display='none';
  cancelAnimationFrame(raf);PARTS=[];FLOATS=[];
  initGame();
  document.getElementById('w-ico').textContent=G.W.ico;
  document.getElementById('w-lbl').textContent=G.W.name;
  raf=requestAnimationFrame(loop);
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
addT('dp-up',   ()=>G._tUp=true,   ()=>G._tUp=false);
addT('dp-down', ()=>G._tDown=true, ()=>G._tDown=false);
addT('dp-left', ()=>G._tLeft=true, ()=>G._tLeft=false);
addT('dp-right',()=>G._tRight=true,()=>G._tRight=false);
addT('nitro-btn',()=>G._tNitro=true,()=>G._tNitro=false);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
