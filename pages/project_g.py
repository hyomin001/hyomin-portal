import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>좀비 아포칼립스</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--green:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--purple:#c04fff;--orange:#ff7700;--bg:#060a0c;--bg2:#0a0f10;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.07);}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;}
canvas{position:absolute;top:0;left:0;}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;
  background:linear-gradient(180deg,rgba(0,0,0,.85)0%,transparent 100%);
  padding:10px 14px;display:flex;align-items:center;gap:8px;pointer-events:none;}
.hb{background:rgba(0,0,0,.42);border:1px solid var(--border);border-radius:9px;padding:4px 11px;text-align:center;}
.hv{font-family:'Rajdhani',sans-serif;font-size:20px;font-weight:900;color:#fff;letter-spacing:1px;line-height:1.1;}
.hl{font-size:7px;color:#445;letter-spacing:2px;text-transform:uppercase;}
#hp-block{display:flex;flex-direction:column;gap:3px;padding:6px 12px;min-width:100px;}
#hp-lbl{font-size:7px;color:#633;letter-spacing:3px;}
#hp-bar-bg{height:10px;background:rgba(255,0,50,.08);border:1px solid rgba(255,0,50,.2);border-radius:99px;overflow:hidden;}
#hp-bar{height:100%;background:linear-gradient(90deg,#7b0000,#cc1122,#ff5566);border-radius:99px;transition:width .1s;}
#hud-right{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:4px;}
#coin-v{color:var(--gold);}
#wave-v{color:var(--red);}

/* RELOAD RING */
#reload-ring{position:absolute;bottom:100px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;text-align:center;display:none;}
#rl-circle{width:52px;height:52px;border-radius:50%;border:3px solid rgba(245,197,24,.15);position:relative;margin:0 auto 3px;}
#rl-fill{width:52px;height:52px;border-radius:50%;position:absolute;inset:0;}
#rl-ico{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:18px;}
#rl-txt{font-size:7px;color:var(--gold);letter-spacing:2px;}

/* AMMO */
#ammo-bar{position:absolute;bottom:90px;right:14px;z-index:100;pointer-events:none;}
.ammo-col{display:flex;flex-direction:column;gap:3px;}
.a-dot{width:9px;height:20px;border-radius:3px;background:rgba(245,197,24,.12);border:1px solid rgba(245,197,24,.2);transition:all .1s;}
.a-dot.live{background:var(--gold);box-shadow:0 0 6px rgba(245,197,24,.6);}
#ammo-lbl{font-size:7px;color:#555;letter-spacing:2px;text-align:center;margin-top:4px;}

/* WEAPON BAR */
#weapbar{position:absolute;bottom:0;left:0;right:0;z-index:100;
  background:linear-gradient(transparent,rgba(0,0,0,.8)100%);
  padding:8px 12px 10px;display:flex;gap:7px;justify-content:center;}
.wslot{min-width:60px;height:70px;border-radius:11px;background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.08);
  display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all .18s;position:relative;padding:2px;}
.wslot.active{border-color:var(--gold);box-shadow:0 0 16px rgba(245,197,24,.35);}
.wslot.empty{opacity:.3;}
.ws-ico{font-size:22px;}
.ws-name{font-size:7px;color:#667;letter-spacing:1px;margin-top:2px;}
.ws-ammo{position:absolute;top:3px;right:5px;font-size:8px;color:var(--gold);font-weight:900;}
.ws-key{position:absolute;bottom:3px;left:5px;font-size:7px;color:#334;}

/* JOYSTICK */
#joyzone{position:absolute;bottom:90px;left:16px;width:105px;height:105px;z-index:100;
  border-radius:50%;background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.07);}
#joyknob{position:absolute;width:42px;height:42px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,rgba(255,255,255,.2),rgba(255,255,255,.08));
  border:1.5px solid rgba(255,255,255,.18);top:50%;left:50%;transform:translate(-50%,-50%);transition:transform .05s;}

/* FIRE / RELOAD BTNS */
#fire-btn{position:absolute;bottom:100px;right:14px;width:74px;height:74px;border-radius:50%;z-index:100;
  background:rgba(255,34,68,.18);border:2px solid rgba(255,34,68,.45);
  display:flex;align-items:center;justify-content:center;font-size:28px;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;}
#fire-btn:active,#fire-btn.pr{background:rgba(255,34,68,.38);transform:scale(.91);box-shadow:0 0 18px rgba(255,34,68,.5);}
#rel-btn{position:absolute;bottom:186px;right:22px;width:52px;height:52px;border-radius:50%;z-index:100;
  background:rgba(245,197,24,.1);border:1.5px solid rgba(245,197,24,.35);
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:16px;cursor:pointer;user-select:none;touch-action:none;}
#rel-btn:active{background:rgba(245,197,24,.25);}
#rel-btn .rb-lbl{font-size:7px;color:var(--gold);letter-spacing:1px;}

/* WAVE BANNER */
#wave-ann{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;
  text-align:center;opacity:0;transition:opacity .25s;}
#wa-wave{font-family:'Black Han Sans',sans-serif;font-size:36px;color:var(--red);letter-spacing:4px;
  text-shadow:0 0 30px rgba(255,0,50,.8);}
#wa-name{font-size:14px;color:var(--gold);letter-spacing:3px;margin-top:4px;}

/* KILL FEED */
#killfeed{position:absolute;top:70px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kfe{background:rgba(0,0,0,.5);border-left:3px solid var(--red);padding:4px 8px;font-size:9px;color:#ccc;
  border-radius:0 6px 6px 0;animation:kfSlide .25s ease;white-space:nowrap;}
@keyframes kfSlide{from{opacity:0;transform:translateX(16px);}to{opacity:1;transform:none;}}

/* VIGNETTE / HIT FLASH */
#vignette{position:absolute;inset:0;z-index:90;pointer-events:none;opacity:0;
  background:radial-gradient(ellipse at center,transparent 40%,rgba(255,0,30,.6)100%);transition:opacity .08s;}

/* SHOP OVERLAY */
#shop{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;backdrop-filter:blur(3px);}
.shop-box{background:linear-gradient(160deg,#040a0c,#060e10);border:1px solid rgba(0,212,255,.18);border-radius:18px;padding:28px 22px;width:min(480px,94vw);}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:22px;color:var(--cyan);text-align:center;letter-spacing:3px;margin-bottom:4px;}
.shop-wave{font-size:9px;color:#335;text-align:center;letter-spacing:3px;margin-bottom:4px;}
.shop-coins{text-align:center;font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:var(--gold);margin-bottom:16px;}
.shop-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:14px;}
.si{background:var(--glass);border:1px solid var(--border);border-radius:12px;padding:12px;cursor:pointer;transition:all .2s;text-align:center;}
.si:hover{border-color:rgba(245,197,24,.4);background:rgba(245,197,24,.06);}
.si.bought{opacity:.4;pointer-events:none;}
.si-ico{font-size:22px;margin-bottom:4px;}
.si-name{font-size:11px;font-weight:700;letter-spacing:1px;}
.si-desc{font-size:8px;color:#445;margin-top:3px;line-height:1.6;}
.si-cost{font-size:11px;color:var(--gold);margin-top:6px;font-weight:900;}
.shop-cont{display:block;width:100%;padding:12px;background:linear-gradient(135deg,rgba(0,212,255,.18),rgba(108,99,255,.12));
  border:1px solid rgba(0,212,255,.4);border-radius:11px;font-family:'Black Han Sans',sans-serif;
  font-size:16px;color:var(--cyan);cursor:pointer;letter-spacing:2px;text-align:center;transition:all .2s;}
.shop-cont:hover{background:linear-gradient(135deg,rgba(0,212,255,.32),rgba(108,99,255,.24));transform:translateY(-2px);}

/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:400;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:36px 26px;background:linear-gradient(160deg,#040a0c,#060e10);
  border:1px solid rgba(0,255,136,.18);border-radius:20px;min-width:310px;max-width:92vw;}
.ov-badge{display:inline-block;font-size:7px;letter-spacing:4px;color:var(--green);
  background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.2);border-radius:99px;padding:3px 12px;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(24px,6vw,36px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#335;letter-spacing:4px;margin-bottom:18px;}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.s-chip{padding:6px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.s-v{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:900;color:#fff;}
.s-l{font-size:7px;color:#446;letter-spacing:2px;}
.ov-btn{display:inline-block;padding:12px 32px;background:linear-gradient(135deg,rgba(255,34,68,.2),rgba(192,79,255,.12));
  border:1px solid rgba(255,34,68,.45);border-radius:12px;font-family:'Black Han Sans',sans-serif;
  font-size:16px;color:var(--red);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(255,34,68,.38),rgba(192,79,255,.26));transform:translateY(-2px);box-shadow:0 8px 24px rgba(255,34,68,.3);}
</style>
</head>
<body>
<div id="root">
  <canvas id="bgc"></canvas>
  <canvas id="gc"></canvas>

  <div id="hud">
    <div id="hp-block" class="hb">
      <div id="hp-lbl">HP</div>
      <div id="hp-bar-bg"><div id="hp-bar" style="width:100%"></div></div>
    </div>
    <div class="hb"><div class="hv" id="wave-v">1</div><div class="hl">WAVE</div></div>
    <div class="hb"><div class="hv" id="kill-v">0</div><div class="hl">KILLS</div></div>
    <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
    <div id="hud-right"><div class="hb"><div class="hv" id="coin-v">💰 0</div><div class="hl">COINS</div></div></div>
  </div>

  <div id="ammo-bar"><div class="ammo-col" id="ammo-col"></div><div id="ammo-lbl">AMMO</div></div>
  <div id="reload-ring">
    <div id="rl-circle"><canvas id="rl-canvas" width="52" height="52"></canvas><div id="rl-ico">🔄</div></div>
    <div id="rl-txt">장전중...</div>
  </div>

  <div id="joyzone"><div id="joyknob"></div></div>
  <div id="fire-btn">🔫</div>
  <div id="rel-btn"><span>🔄</span><span class="rb-lbl">R</span></div>

  <div id="weapbar"></div>
  <div id="killfeed"></div>
  <div id="vignette"></div>
  <div id="wave-ann"><div id="wa-wave">WAVE!</div><div id="wa-name"></div></div>

  <div id="shop">
    <div class="shop-box">
      <div class="shop-title">🛒 웨이브 클리어!</div>
      <div class="shop-wave" id="shop-wave-txt"></div>
      <div class="shop-coins" id="shop-coins-txt"></div>
      <div class="shop-grid" id="shop-grid"></div>
      <button class="shop-cont" id="shop-cont">다음 웨이브 ⚡</button>
    </div>
  </div>

  <div id="overlay">
    <div class="ov-box">
      <div class="ov-badge">ZOMBIE APOCALYPSE</div>
      <div class="ov-title" style="color:var(--red)">🧟<br>좀비 아포칼립스</div>
      <div class="ov-sub">WAVE SURVIVAL SHOOTER</div>
      <div style="font-size:9px;color:#446;line-height:2.2;margin-bottom:16px">
        WASD · 조이스틱 — 이동<br>
        마우스클릭 · 🔫 — 발사 &nbsp;|&nbsp; R · 🔄 — 재장전<br>
        1~4 키 · 슬롯 탭 — 무기 변경<br>
        웨이브 클리어 후 상점에서 업그레이드!
      </div>
      <button class="ov-btn" id="start-btn">생존 시작 💀</button>
    </div>
  </div>
</div>
<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  좀비 아포칼립스 v2.0
//  탑다운 슈터 · 4무기 · 웨이브 시스템 · 상점 업그레이드
//  보스 좀비 · 혈흔 시스템 · 풀 파티클 이펙트
// ══════════════════════════════════════════════════════════════
const bgc  = document.getElementById('bgc');
const bgCtx= bgc.getContext('2d');
const canvas= document.getElementById('gc');
const ctx  = canvas.getContext('2d');
const root = document.getElementById('root');

// RESIZE
function resize(){
  canvas.width=bgc.width=root.clientWidth;
  canvas.height=bgc.height=root.clientHeight;
}
resize(); window.addEventListener('resize',()=>{resize();drawBg();});

// ── WEAPON DEFS ───────────────────────────────────────────────
const WDEFS=[
  {id:0,name:'권총',   emoji:'🔫',dmg:28, rof:18,mag:12,maxMag:12,rel:85, spd:17,spread:.04,auto:false,cost:0,  desc:'빠른 재장전·단발',col:'#00d4ff',pellets:1},
  {id:1,name:'샷건',   emoji:'🪖',dmg:22, rof:38,mag:8, maxMag:8, rel:130,spd:13,spread:.22,auto:false,cost:90, desc:'근거리 산탄·강력',col:'#ff7700',pellets:6},
  {id:2,name:'돌격소총',emoji:'⚙️',dmg:20, rof:7, mag:30,maxMag:30,rel:110,spd:21,spread:.07,auto:true, cost:130,desc:'완전자동·높은 DPS',col:'#00ff88',pellets:1},
  {id:3,name:'스나이퍼',emoji:'🎯',dmg:130,rof:65,mag:5, maxMag:5, rel:160,spd:32,spread:.01,auto:false,cost:220,desc:'원샷 킬·관통',col:'#c04fff',pellets:1,pierce:true},
];

// ── ZOMBIE TYPES ───────────────────────────────────────────────
const ZDEFS=[
  {name:'일반',emoji:'🧟',hp:60, spd:1.1,dmg:8, sz:22,col:'#2d5a1a',score:10,coin:5},
  {name:'달리기',emoji:'🏃',hp:40, spd:2.6,dmg:6, sz:18,col:'#1a4d2d',score:15,coin:8},
  {name:'뚱보',  emoji:'😈',hp:220,spd:0.65,dmg:22,sz:34,col:'#4a1a0a',score:32,coin:22},
  {name:'폭탄',  emoji:'💣',hp:80, spd:1.9,dmg:45,sz:24,col:'#1a1a4a',score:28,coin:18},
  {name:'보스',  emoji:'👹',hp:900,spd:0.9,dmg:40,sz:50,col:'#6a0000',score:250,coin:120},
];

// ── SHOP ITEMS ─────────────────────────────────────────────────
const SHOP_ITEMS=[
  {id:'heal',   name:'응급 치료',  emoji:'💊',desc:'HP 60 즉시 회복',     cost:60,col:'#00ff88'},
  {id:'ammo',   name:'탄약 보급',  emoji:'🎁',desc:'전 무기 탄약 풀 충전', cost:50,col:'#00d4ff'},
  {id:'maxhp',  name:'HP 증가',    emoji:'❤️',desc:'최대 HP +40',          cost:100,col:'#ff2244'},
  {id:'dmg',    name:'화력 강화',  emoji:'⚡',desc:'전 무기 데미지 +25%',  cost:120,col:'#f5c518'},
  {id:'spd',    name:'이동속도 UP',emoji:'💨',desc:'이동속도 +30%',        cost:80, col:'#c04fff'},
  {id:'reload', name:'장전 감소',  emoji:'⏱️',desc:'전 무기 장전속도 -25%',cost:90, col:'#ff7700'},
];

// ── STATE ──────────────────────────────────────────────────────
let G={running:false};
let PARTS=[],BLOODS=[],HNS=[];

function initGame(){
  G={
    running:true,shopOpen:false,
    wave:0,score:0,totalKills:0,coins:160,
    hp:100,maxHp:100,
    player:{x:canvas.width/2,y:canvas.height/2,angle:0,spd:2.6,spdMul:1},
    weapons:[{...WDEFS[0],ammo:WDEFS[0].maxMag}],
    wIdx:0,reloading:false,relTimer:0,fireTimer:0,
    bullets:[],zombies:[],
    waveActive:false,toSpawn:0,spawnT:0,waveKills:0,wNeeded:0,
    keys:{w:false,a:false,s:false,d:false},
    mouse:{x:canvas.width/2,y:canvas.height/2,down:false},
    joy:{active:false,dx:0,dy:0},
    touchFire:false,frame:0,
  };
  PARTS=[];BLOODS=[];HNS=[];
  drawBg();
  rebuildWeapBar();
  buildAmmoDisplay();
  nextWave();
}

// ── BACKGROUND ─────────────────────────────────────────────────
function drawBg(){
  const W=canvas.width,H=canvas.height;
  bgCtx.fillStyle='#060a0c'; bgCtx.fillRect(0,0,W,H);
  // tile grid
  const ts=64;
  for(let x=0;x<W;x+=ts)for(let y=0;y<H;y+=ts){
    bgCtx.strokeStyle='rgba(255,255,255,.02)'; bgCtx.lineWidth=1;
    bgCtx.strokeRect(x+.5,y+.5,ts,ts);
    if(Math.random()<.08){
      bgCtx.fillStyle=`rgba(0,0,0,${.03+Math.random()*.05})`;
      bgCtx.fillRect(x+Math.random()*ts*.7,y+Math.random()*ts*.7,ts*.3*Math.random(),ts*.3*Math.random());
    }
  }
  // blood stains
  for(let i=0;i<12;i++){
    const bx=Math.random()*W,by=Math.random()*H;
    const gr=bgCtx.createRadialGradient(bx,by,0,bx,by,18+Math.random()*28);
    gr.addColorStop(0,'rgba(100,0,0,.32)'); gr.addColorStop(1,'transparent');
    bgCtx.fillStyle=gr;bgCtx.beginPath();bgCtx.ellipse(bx,by,22+Math.random()*18,12+Math.random()*14,Math.random()*Math.PI,0,Math.PI*2);bgCtx.fill();
  }
  // debris
  ['💊','🔩','📦','🧱','🔫'].forEach(e=>{
    for(let d=0;d<4;d++){
      bgCtx.save();bgCtx.globalAlpha=.15;bgCtx.font='16px serif';bgCtx.textAlign='center';
      bgCtx.fillText(e,Math.random()*W,Math.random()*H);bgCtx.restore();
    }
  });
}

// ── WAVE SYSTEM ────────────────────────────────────────────────
function nextWave(){
  G.wave++;
  G.waveKills=0;
  G.wNeeded=8+G.wave*5+(G.wave>5?G.wave*2:0);
  G.toSpawn=G.wNeeded;
  G.spawnT=80;
  G.waveActive=true;
  // announce
  const ann=document.getElementById('wave-ann');
  const isBoss=G.wave%5===0;
  document.getElementById('wa-wave').textContent=isBoss?`👹 BOSS WAVE ${G.wave}`:`⚡ WAVE ${G.wave}`;
  document.getElementById('wa-name').textContent=isBoss?'강력한 보스가 등장합니다!':G.wNeeded+'마리 제거';
  ann.style.opacity='1';setTimeout(()=>ann.style.opacity='0',2200);
  updateHUD();
}

function spawnZombie(){
  const W=canvas.width,H=canvas.height;
  // spawn outside view
  const side=Math.random()*4|0;
  let x,y;
  if(side===0){x=Math.random()*W;y=-40;}
  else if(side===1){x=W+40;y=Math.random()*H;}
  else if(side===2){x=Math.random()*W;y=H+40;}
  else{x=-40;y=Math.random()*H;}
  // type based on wave
  let ti=0;
  const r=Math.random();
  if(G.wave>=2&&r<.12)ti=1; // runner
  if(G.wave>=3&&r<.09)ti=2; // fat
  if(G.wave>=5&&r<.08)ti=3; // bomber
  const isBoss=G.wave%5===0&&G.waveKills===0&&G.toSpawn===G.wNeeded;
  if(isBoss)ti=4;
  const t=ZDEFS[ti];
  const hpScale=1+G.wave*.12;
  G.zombies.push({
    x,y,hp:t.hp*hpScale,maxHp:t.hp*hpScale,
    spd:t.spd*(1+G.wave*.04),dmg:t.dmg,sz:t.sz,
    emoji:t.emoji,col:t.col,score:t.score,coin:t.coin,
    typeIdx:ti,alive:true,attackCool:0,
    flash:0,wobble:Math.random()*Math.PI*2,
    explodes:ti===3,isBoss:ti===4,
  });
}

// ── PARTICLES ──────────────────────────────────────────────────
function spawnParts(x,y,opt={}){
  const n=opt.n||10;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2,v=(opt.vMin||1.5)+Math.random()*(opt.vMax||5);
    const cols=Array.isArray(opt.col)?opt.col:[opt.col||'#ff2244'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      decay:(opt.dMin||.025)+Math.random()*(opt.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(opt.szMin||2)+Math.random()*(opt.szMax||5),glow:opt.glow||false});
  }
}
function spawnBlood(x,y){
  spawnParts(x,y,{n:16,col:['#8b0000','#cc0000','#ee1122','#550000'],vMax:6,szMin:3,szMax:8,dMin:.02,dMax:.04});
  // permanent stain
  bgCtx.save();bgCtx.fillStyle='rgba(80,0,0,.38)';bgCtx.beginPath();bgCtx.ellipse(x,y,6+Math.random()*10,4+Math.random()*8,Math.random()*Math.PI,0,Math.PI*2);bgCtx.fill();bgCtx.restore();
}
function spawnHN(x,y,txt,col){HNS.push({x,y:y-15,txt,col,life:1,vy:-.65});}

// ── SHOOT ──────────────────────────────────────────────────────
function shoot(){
  const w=G.weapons[G.wIdx];
  if(!w||G.reloading||w.ammo<=0||G.fireTimer>0)return;
  w.ammo--;G.fireTimer=w.rof;
  updateAmmoDisplay();
  const p=G.player,pellets=w.pellets||1;
  for(let pe=0;pe<pellets;pe++){
    const spr=(Math.random()-.5)*w.spread*2;
    const ang=p.angle+spr;
    G.bullets.push({
      x:p.x+Math.cos(p.angle)*24,y:p.y+Math.sin(p.angle)*24,
      vx:Math.cos(ang)*w.spd,vy:Math.sin(ang)*w.spd,
      dmg:w.dmg,r:w.id===3?5:w.id===1?4:3,
      life:w.id===3?90:60,col:w.col,
      pierce:w.pierce||false,hitIds:[],
    });
  }
  if(w.ammo<=0)startReload();
  // muzzle flash
  spawnParts(p.x+Math.cos(p.angle)*28,p.y+Math.sin(p.angle)*28,{n:6,col:w.col,vMin:2,vMax:5,dMin:.08,dMax:.12,glow:true});
}

function startReload(){
  if(G.reloading)return;
  const w=G.weapons[G.wIdx];if(!w||w.ammo>=w.maxMag)return;
  G.reloading=true;G.relTimer=w.rel;
  document.getElementById('reload-ring').style.display='block';
}

function switchWeapon(i){
  if(i>=G.weapons.length)return;
  if(G.reloading){G.reloading=false;G.relTimer=0;document.getElementById('reload-ring').style.display='none';}
  G.wIdx=i;G.fireTimer=0;rebuildWeapBar();updateAmmoDisplay();
}

// ── UPDATE ─────────────────────────────────────────────────────
function update(){
  if(!G.running||G.shopOpen)return;
  G.frame++;

  // timers
  if(G.fireTimer>0)G.fireTimer--;
  if(G.reloading){
    G.relTimer--;
    // draw reload ring
    const rlc=document.getElementById('rl-canvas');
    if(rlc){
      const rc=rlc.getContext('2d'),pct=1-(G.relTimer/G.weapons[G.wIdx].rel);
      rc.clearRect(0,0,52,52);rc.strokeStyle='rgba(245,197,24,.15)';rc.lineWidth=4;
      rc.beginPath();rc.arc(26,26,22,0,Math.PI*2);rc.stroke();
      rc.strokeStyle='rgba(245,197,24,.8)';rc.shadowColor='rgba(245,197,24,.6)';rc.shadowBlur=8;
      rc.beginPath();rc.arc(26,26,22,-Math.PI*.5,-Math.PI*.5+Math.PI*2*pct);rc.stroke();
    }
    if(G.relTimer<=0){
      const w=G.weapons[G.wIdx];w.ammo=w.maxMag;G.reloading=false;
      document.getElementById('reload-ring').style.display='none';updateAmmoDisplay();
    }
  }

  // player movement
  const p=G.player;
  let mx=0,my=0;
  if(G.keys.w)my-=1;if(G.keys.s)my+=1;
  if(G.keys.a)mx-=1;if(G.keys.d)mx+=1;
  if(G.joy.active){mx=G.joy.dx;my=G.joy.dy;}
  const mlen=Math.sqrt(mx*mx+my*my);if(mlen>0){mx/=mlen;my/=mlen;}
  const ms=p.spd*p.spdMul;
  p.x=Math.max(20,Math.min(canvas.width-20,p.x+mx*ms));
  p.y=Math.max(20,Math.min(canvas.height-20,p.y+my*ms));
  p.angle=Math.atan2(G.mouse.y-p.y,G.mouse.x-p.x);

  // auto fire
  const w=G.weapons[G.wIdx];
  if((G.mouse.down||G.touchFire)&&w&&w.auto)shoot();

  // wave spawn
  if(G.waveActive&&G.toSpawn>0){
    G.spawnT--;
    const interval=Math.max(22,90-G.wave*6);
    if(G.spawnT<=0){spawnZombie();G.toSpawn--;G.spawnT=interval;}
  }

  // bullets
  for(const b of G.bullets){
    b.x+=b.vx;b.y+=b.vy;b.life--;
    if(G.frame%2===0)spawnParts(b.x,b.y,{n:1,col:b.col,vMin:0,vMax:1,szMin:1,szMax:b.r*.7,dMin:.1,dMax:.15,glow:true});
    for(const z of G.zombies){
      if(!z.alive||b.life<=0)continue;
      if(b.pierce&&b.hitIds.includes(z))continue;
      const dx=b.x-z.x,dy=b.y-z.y;
      if(dx*dx+dy*dy<z.sz*z.sz){
        z.hp-=b.dmg;z.flash=6;
        spawnParts(b.x,b.y,{n:5,col:'#ff4400',vMax:4,szMax:4});
        if(b.pierce)b.hitIds.push(z);else b.life=0;
        if(z.hp<=0)killZombie(z);
      }
    }
  }
  G.bullets=G.bullets.filter(b=>b.life>0&&b.x>-100&&b.x<canvas.width+100&&b.y>-100&&b.y<canvas.height+100);

  // zombies
  for(const z of G.zombies){
    if(!z.alive)continue;
    z.wobble+=.05;
    const dx=p.x-z.x,dy=p.y-z.y,d=Math.sqrt(dx*dx+dy*dy);
    const ang=Math.atan2(dy,dx);
    if(d>z.sz+18){z.x+=Math.cos(ang)*z.spd;z.y+=Math.sin(ang)*z.spd;}
    else{if(z.attackCool<=0){G.hp-=z.dmg;z.attackCool=60;document.getElementById('vignette').style.opacity='.7';setTimeout(()=>document.getElementById('vignette').style.opacity='0',300);if(G.hp<=0){G.hp=0;setTimeout(showGameOver,500);}}}
    if(z.attackCool>0)z.attackCool--;
    if(z.flash>0)z.flash--;
  }

  // particles/HNs
  for(let i=PARTS.length-1;i>=0;i--){const p2=PARTS[i];p2.x+=p2.vx;p2.y+=p2.vy;p2.vx*=.88;p2.vy*=.88;p2.life-=p2.decay;p2.life<=0&&PARTS.splice(i,1);}
  for(let i=HNS.length-1;i>=0;i--){const h=HNS[i];h.y+=h.vy;h.life-=.02;h.life<=0&&HNS.splice(i,1);}

  // wave clear
  if(G.waveActive&&G.toSpawn===0&&G.zombies.filter(z=>z.alive).length===0){
    G.waveActive=false;setTimeout(openShop,900);
  }

  updateHUD();
}

function killZombie(z){
  z.alive=false;spawnBlood(z.x,z.y);
  G.totalKills++;G.waveKills++;G.coins+=z.coin;G.score+=z.score;
  spawnHN(z.x,z.y,`+${z.score}`,z.isBoss?'#f5c518':'#00ff88');
  if(z.explodes){
    spawnParts(z.x,z.y,{n:20,col:['#ff7700','#ff4400','#ffaa00'],glow:true,vMax:8,szMax:10});
    G.zombies.forEach(z2=>{if(!z2.alive)return;const dx=z2.x-z.x,dy=z2.y-z.y;if(dx*dx+dy*dy<6400){z2.hp-=70;if(z2.hp<=0)killZombie(z2);}});
    const dp=G.player,dx=dp.x-z.x,dy=dp.y-z.y;if(dx*dx+dy*dy<6400)G.hp-=45;
  }
  // kill feed
  addKillfeed(z);
}

function addKillfeed(z){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kfe';
  const pts=z.score;d.innerHTML=`${z.emoji} <span style="color:${z.col.replace('#','var(--') }">${ZDEFS[z.typeIdx].name}</span> 처치 <b style="color:var(--gold)">+${pts}pt</b>`;
  if(z.isBoss)d.style.borderLeftColor='var(--gold)';
  kf.appendChild(d);setTimeout(()=>d.remove(),2800);
  // trim
  while(kf.children.length>5)kf.removeChild(kf.firstChild);
}

// ── SHOP ──────────────────────────────────────────────────────
function openShop(){
  G.shopOpen=true;
  document.getElementById('shop-wave-txt').textContent=`WAVE ${G.wave} 클리어!`;
  document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
  const grid=document.getElementById('shop-grid');grid.innerHTML='';

  // Weapons not owned
  const items=[...SHOP_ITEMS];
  WDEFS.forEach(wd=>{if(!G.weapons.find(w=>w.id===wd.id)&&wd.cost>0)
    items.push({id:'weapon_'+wd.id,name:wd.name,emoji:wd.emoji,desc:wd.desc+' · 장전 탄창',cost:wd.cost,col:wd.col,isWeapon:true,wDef:wd});});

  // Shuffle pick 4
  const picks=items.sort(()=>Math.random()-.5).slice(0,4);
  picks.forEach(item=>{
    const div=document.createElement('div');div.className='si';
    div.innerHTML=`<div class="si-ico">${item.emoji}</div><div class="si-name" style="color:${item.col}">${item.name}</div><div class="si-desc">${item.desc}</div><div class="si-cost">💰 ${item.cost}</div>`;
    div.onclick=()=>{
      if(G.coins<item.cost){div.style.borderColor='var(--red)';div.style.animation='shake .3s';return;}
      G.coins-=item.cost;div.classList.add('bought');
      document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
      applyShopItem(item);
    };
    grid.appendChild(div);
  });
  document.getElementById('shop').style.display='flex';
}

function applyShopItem(item){
  if(item.isWeapon){G.weapons.push({...item.wDef,ammo:item.wDef.maxMag});rebuildWeapBar();}
  else if(item.id==='heal'){G.hp=Math.min(G.maxHp,G.hp+60);}
  else if(item.id==='ammo'){G.weapons.forEach(w=>w.ammo=w.maxMag);updateAmmoDisplay();}
  else if(item.id==='maxhp'){G.maxHp+=40;G.hp=Math.min(G.maxHp,G.hp+40);}
  else if(item.id==='dmg'){G.weapons.forEach(w=>w.dmg=Math.round(w.dmg*1.25));}
  else if(item.id==='spd'){G.player.spdMul=Math.min(2,(G.player.spdMul||1)*1.3);}
  else if(item.id==='reload'){G.weapons.forEach(w=>w.rel=Math.max(40,Math.round(w.rel*.75)));}
  updateHUD();
}

document.getElementById('shop-cont').onclick=()=>{
  document.getElementById('shop').style.display='none';G.shopOpen=false;nextWave();};

// ── WEAPON BAR ────────────────────────────────────────────────
function rebuildWeapBar(){
  const bar=document.getElementById('weapbar');bar.innerHTML='';
  G.weapons.forEach((w,i)=>{
    const d=document.createElement('div');d.className='wslot'+(i===G.wIdx?' active':'');
    d.innerHTML=`<div class="ws-key">${i+1}</div><div class="ws-ammo">${w.ammo}</div><div class="ws-ico">${w.emoji}</div><div class="ws-name">${w.name}</div>`;
    d.onclick=()=>switchWeapon(i);bar.appendChild(d);
  });
}
function buildAmmoDisplay(){
  const ac=document.getElementById('ammo-col');ac.innerHTML='';
  const w=G.weapons[G.wIdx];if(!w)return;
  for(let i=0;i<w.maxMag;i++){const d=document.createElement('div');d.className='a-dot'+(i<w.ammo?' live':'');d.id='ad'+i;ac.appendChild(d);}
}
function updateAmmoDisplay(){
  buildAmmoDisplay();
  const bar=document.getElementById('weapbar');
  const slots=bar.querySelectorAll('.wslot');
  slots.forEach((s,i)=>{if(G.weapons[i])s.querySelector('.ws-ammo').textContent=G.weapons[i].ammo;});
}

// ── HUD ────────────────────────────────────────────────────────
function updateHUD(){
  document.getElementById('hp-bar').style.width=(G.hp/G.maxHp*100)+'%';
  document.getElementById('hp-bar').style.background=G.hp<G.maxHp*.3?'linear-gradient(90deg,#550000,#ff0022)':'linear-gradient(90deg,#7b0000,#cc1122,#ff5566)';
  document.getElementById('wave-v').textContent=G.wave;
  document.getElementById('kill-v').textContent=G.totalKills;
  document.getElementById('score-v').textContent=G.score.toLocaleString();
  document.getElementById('coin-v').textContent='💰 '+G.coins;
}

// ── DRAW ──────────────────────────────────────────────────────
function drawZombies(){
  G.zombies.forEach(z=>{
    if(!z.alive)return;
    ctx.save();ctx.translate(z.x,z.y);
    if(z.flash>0&&z.flash%2===0)ctx.filter='brightness(4) saturate(0)';
    // shadow
    ctx.fillStyle='rgba(0,0,0,.32)';ctx.beginPath();ctx.ellipse(0,z.sz*.65,z.sz*.55,z.sz*.18,0,0,Math.PI*2);ctx.fill();
    ctx.font=`${z.sz*1.5}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(z.emoji,Math.sin(z.wobble)*3,Math.cos(z.wobble)*2);
    ctx.restore();
    if(z.hp<z.maxHp){
      const bw=z.sz*2.2,bh=5,bx=z.x-bw/2,by=z.y-z.sz-10;
      ctx.fillStyle='rgba(0,0,0,.55)';ctx.fillRect(bx,by,bw,bh);
      const pct=z.hp/z.maxHp;
      ctx.fillStyle=pct>.5?'#00ff88':pct>.25?'#ffaa00':'#ff2244';ctx.fillRect(bx,by,bw*pct,bh);
    }
  });
}

function drawPlayer(){
  const p=G.player;
  // shadow
  ctx.save();ctx.fillStyle='rgba(0,0,0,.3)';ctx.beginPath();ctx.ellipse(p.x,p.y+18,18,7,0,0,Math.PI*2);ctx.fill();ctx.restore();
  // body
  ctx.save();ctx.font='46px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🧑',p.x,p.y);ctx.restore();
  // weapon aim line
  const w=G.weapons[G.wIdx];
  if(w){
    ctx.save();ctx.strokeStyle=w.col;ctx.lineWidth=1.5;ctx.setLineDash([3,5]);
    ctx.shadowColor=w.col;ctx.shadowBlur=6;ctx.globalAlpha=.55;
    ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x+Math.cos(p.angle)*35,p.y+Math.sin(p.angle)*35);ctx.stroke();
    ctx.restore();
  }
  // crosshair at mouse
  ctx.save();ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=1;
  const mx=G.mouse.x,my=G.mouse.y;
  ctx.beginPath();ctx.moveTo(mx-8,my);ctx.lineTo(mx+8,my);ctx.moveTo(mx,my-8);ctx.lineTo(mx,my+8);ctx.stroke();
  ctx.beginPath();ctx.arc(mx,my,4,0,Math.PI*2);ctx.stroke();ctx.restore();
}

function drawBullets(){
  for(const b of G.bullets){
    ctx.save();ctx.shadowColor=b.col;ctx.shadowBlur=10;ctx.fillStyle=b.col;
    ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();ctx.restore();
  }
}

function drawParts(){
  for(const p of PARTS){
    ctx.save();ctx.globalAlpha=Math.max(0,p.life);
    if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}
    ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.1,p.life),0,Math.PI*2);ctx.fill();
    if(p.glow)ctx.shadowBlur=0;ctx.restore();
  }
}

function drawHNs(){
  for(const h of HNS){
    ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;
    ctx.fillStyle=h.col;ctx.font="bold 14px 'Black Han Sans',sans-serif";ctx.textAlign='center';
    ctx.fillText(h.txt,h.x,h.y);ctx.restore();
  }
}

// ── LOOP ──────────────────────────────────────────────────────
function loop(){
  if(!G.running)return;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  drawBullets();drawZombies();drawPlayer();drawParts();drawHNs();
  update();
  requestAnimationFrame(loop);
}

// ── GAMEOVER ──────────────────────────────────────────────────
function showGameOver(){
  G.running=false;
  const best=parseInt(localStorage.getItem('zbBest')||'0');
  if(G.wave>best)localStorage.setItem('zbBest',G.wave);
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-badge">GAME OVER</div>
    <div class="ov-title" style="color:var(--red)">💀<br>감염됨!</div>
    <div class="ov-sub">YOU HAVE FALLEN</div>
    <div class="stats-row">
      <div class="s-chip"><div class="s-v" style="color:var(--red)">WAVE ${G.wave}</div><div class="s-l">도달 웨이브</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="s-l">점수</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--green)">${G.totalKills}</div><div class="s-l">처치수</div></div>
    </div>
    <div style="font-size:9px;color:#446;margin-bottom:14px">최고기록: <span style="color:var(--gold)">${Math.max(G.wave,best)} WAVE</span></div>
    <button class="ov-btn" onclick="location.reload()">다시 생존 💀</button>
  </div>`;
  ov.style.display='flex';
}

// ── INPUT ─────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
  if(e.key==='w'||e.key==='W'||e.key==='ArrowUp')G.keys.w=true;
  if(e.key==='s'||e.key==='S'||e.key==='ArrowDown')G.keys.s=true;
  if(e.key==='a'||e.key==='A'||e.key==='ArrowLeft')G.keys.a=true;
  if(e.key==='d'||e.key==='D'||e.key==='ArrowRight')G.keys.d=true;
  if(e.key==='r'||e.key==='R')startReload();
  if(e.key==='1')switchWeapon(0);if(e.key==='2')switchWeapon(1);
  if(e.key==='3')switchWeapon(2);if(e.key==='4')switchWeapon(3);
});
document.addEventListener('keyup',e=>{
  if(e.key==='w'||e.key==='W'||e.key==='ArrowUp')G.keys.w=false;
  if(e.key==='s'||e.key==='S'||e.key==='ArrowDown')G.keys.s=false;
  if(e.key==='a'||e.key==='A'||e.key==='ArrowLeft')G.keys.a=false;
  if(e.key==='d'||e.key==='D'||e.key==='ArrowRight')G.keys.d=false;
});
canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect();G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;});
canvas.addEventListener('mousedown',e=>{G.mouse.down=true;if(G.running)shoot();});
canvas.addEventListener('mouseup',()=>G.mouse.down=false);
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[e.touches.length-1];const r=canvas.getBoundingClientRect();G.mouse.x=t.clientX-r.left;G.mouse.y=t.clientY-r.top;},{passive:false});

// Joystick
const joy=document.getElementById('joyzone'),knob=document.getElementById('joyknob');
let jO=null;
joy.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=joy.getBoundingClientRect();jO={x:r.left+r.width/2,y:r.top+r.height/2};G.joy.active=true;},{passive:false});
joy.addEventListener('touchmove',e=>{e.preventDefault();if(!jO)return;const t=e.touches[0];let dx=t.clientX-jO.x,dy=t.clientY-jO.y;const d=Math.sqrt(dx*dx+dy*dy),max=40;if(d>max){dx=dx/d*max;dy=dy/d*max;}G.joy.dx=dx/max;G.joy.dy=dy/max;knob.style.transform=`translate(calc(-50% + ${dx}px),calc(-50% + ${dy}px))`;},{passive:false});
['touchend','touchcancel'].forEach(ev=>joy.addEventListener(ev,e=>{e.preventDefault();G.joy.active=false;G.joy.dx=0;G.joy.dy=0;knob.style.transform='translate(-50%,-50%)';},{passive:false}));

// Fire btn
const fb=document.getElementById('fire-btn');
fb.addEventListener('touchstart',e=>{e.preventDefault();G.touchFire=true;if(G.running)shoot();},{passive:false});
fb.addEventListener('touchend',e=>{e.preventDefault();G.touchFire=false;},{passive:false});
fb.addEventListener('mousedown',()=>{G.touchFire=true;if(G.running)shoot();});
fb.addEventListener('mouseup',()=>G.touchFire=false);

document.getElementById('rel-btn').addEventListener('click',startReload);
document.getElementById('rel-btn').addEventListener('touchstart',e=>{e.preventDefault();startReload();},{passive:false});
document.getElementById('start-btn').addEventListener('click',()=>{document.getElementById('overlay').style.display='none';initGame();requestAnimationFrame(loop);});
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
