import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스트리트 파이터 EX</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--blue:#33aaff;--gold:#f5c518;--green:#00ff88;--purple:#c04fff;--cyan:#00d4ff;--bg:#0a050f;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.08);}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;display:flex;flex-direction:column;}
#gc{display:block;width:100%;}

/* HUD TOP */
#hud{display:flex;align-items:center;gap:8px;padding:10px 14px;background:linear-gradient(180deg,rgba(0,0,0,.88)0%,transparent 100%);pointer-events:none;position:relative;z-index:50;}
.hp-col{flex:1;}
.fn{font-size:9px;letter-spacing:2px;margin-bottom:3px;}
#fn-p1{color:var(--blue);}#fn-p2{color:var(--red);text-align:right;}
.hp-bg{height:14px;border-radius:99px;overflow:hidden;border:1.5px solid rgba(255,255,255,.1);background:rgba(0,0,0,.4);}
#hf-p1{height:100%;background:linear-gradient(90deg,#1155ff,#33aaff,#88ddff);border-radius:99px;transition:width .07s;}
#hf-p2{height:100%;background:linear-gradient(90deg,#ff0022,#ff4444,#ff8866);float:right;border-radius:99px;transition:width .07s;}
.center-hud{text-align:center;min-width:82px;}
#rnd-info{font-size:10px;color:var(--gold);letter-spacing:2px;font-weight:900;}
#timer-val{font-family:'Rajdhani',sans-serif;font-size:34px;font-weight:900;color:#fff;line-height:1;}

/* SUPER BARS */
#superbars{display:flex;justify-content:space-between;padding:3px 14px;pointer-events:none;gap:4px;}
.sb-row{display:flex;gap:3px;}
.sseg{width:30px;height:5px;border-radius:99px;background:rgba(255,215,0,.08);border:1px solid rgba(255,215,0,.14);overflow:hidden;}
.sfill{height:100%;background:linear-gradient(90deg,#886600,var(--gold),#ffeeaa);border-radius:99px;}

/* CANVAS AREA */
#canvas-wrap{flex:1;position:relative;overflow:hidden;}
#gc{position:absolute;top:0;left:0;width:100%;height:100%;}

/* ROUND RESULT */
#rnd-result{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;
  font-family:'Black Han Sans',sans-serif;font-size:clamp(32px,8vw,52px);letter-spacing:4px;
  text-shadow:0 0 30px currentColor;opacity:0;transition:opacity .2s;text-align:center;white-space:nowrap;}

/* WIN DOTS */
#win-dots{position:absolute;top:60px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;display:flex;gap:8px;}
.wd{width:12px;height:12px;border-radius:50%;border:1.5px solid rgba(255,255,255,.2);background:rgba(255,255,255,.05);}
.wd.p1{background:var(--blue);box-shadow:0 0 8px rgba(51,170,255,.8);}
.wd.p2{background:var(--red);box-shadow:0 0 8px rgba(255,34,68,.8);}

/* TOUCH LEFT (DPAD) */
#dpad{position:absolute;bottom:12px;left:12px;z-index:100;display:grid;grid-template-columns:58px 58px 58px;grid-template-rows:52px 52px;gap:5px;}
.dp{border-radius:11px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.1);
  display:flex;align-items:center;justify-content:center;font-size:20px;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;}
.dp:active,.dp.pr{background:rgba(51,170,255,.2);border-color:rgba(51,170,255,.5);box-shadow:0 0 10px rgba(51,170,255,.3);transform:scale(.93);}
#dp-up{grid-column:2;grid-row:1;}#dp-left{grid-column:1;grid-row:2;}#dp-down{grid-column:2;grid-row:2;}#dp-right{grid-column:3;grid-row:2;}

/* TOUCH RIGHT (ATTACK BUTTONS) */
#atk-btns{position:absolute;bottom:12px;right:12px;z-index:100;display:grid;grid-template-columns:64px 64px;grid-template-rows:58px 58px;gap:6px;}
.ab{border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;border:2px solid;gap:2px;}
.ab:active,.ab.pr{transform:scale(.91);filter:brightness(1.5);}
.ab span{font-size:8px;letter-spacing:1px;font-weight:700;}
#ab-p{background:rgba(255,34,68,.12);border-color:rgba(255,34,68,.45);color:var(--red);font-size:22px;}
#ab-k{background:rgba(245,197,24,.1);border-color:rgba(245,197,24,.4);color:var(--gold);font-size:22px;}
#ab-j{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.4);color:var(--cyan);font-size:22px;}
#ab-s{background:rgba(192,79,255,.12);border-color:rgba(192,79,255,.45);color:var(--purple);font-size:22px;}

/* KEYS HINT */
#keys-hint{position:absolute;bottom:130px;left:50%;transform:translateX(-50%);z-index:80;pointer-events:none;
  display:flex;gap:22px;font-size:8px;color:#334;letter-spacing:1px;text-align:center;white-space:nowrap;}
.kh-col{display:flex;flex-direction:column;gap:2px;}

/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:300;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:32px 24px;background:linear-gradient(160deg,rgba(10,5,15,.98),rgba(15,8,22,.98));
  border:1px solid rgba(192,79,255,.22);border-radius:20px;min-width:340px;max-width:94vw;}
.ov-badge{display:inline-block;font-size:7px;letter-spacing:4px;color:var(--purple);background:rgba(192,79,255,.1);
  border:1px solid rgba(192,79,255,.22);border-radius:99px;padding:3px 12px;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5.5vw,34px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#334;letter-spacing:4px;margin-bottom:16px;}
.char-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px;}
.cc{padding:10px 6px;background:var(--glass);border:1.5px solid var(--border);border-radius:12px;cursor:pointer;transition:all .2s;text-align:center;}
.cc:hover{border-color:rgba(0,212,255,.3);}
.cc.sel{border-color:var(--blue);background:rgba(51,170,255,.1);box-shadow:0 0 14px rgba(51,170,255,.2);}
.cc-ico{font-size:28px;display:block;margin-bottom:4px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:11px;letter-spacing:1px;}
.cc-stats{font-size:7px;color:#446;margin-top:3px;line-height:1.6;}
.diff-row{display:flex;gap:6px;justify-content:center;margin-bottom:14px;}
.dt{padding:7px 14px;border-radius:99px;background:var(--glass);border:1px solid var(--border);font-size:9px;color:#556;cursor:pointer;transition:all .18s;}
.dt.sel{border-color:var(--gold);color:var(--gold);background:rgba(245,197,24,.08);}
.ov-btn{display:inline-block;padding:12px 32px;background:linear-gradient(135deg,rgba(192,79,255,.22),rgba(108,99,255,.14));
  border:1px solid rgba(192,79,255,.48);border-radius:12px;font-family:'Black Han Sans',sans-serif;
  font-size:17px;color:var(--purple);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:2px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(192,79,255,.38),rgba(108,99,255,.28));transform:translateY(-2px);box-shadow:0 8px 24px rgba(192,79,255,.3);}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.s-chip{padding:6px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.s-v{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:#fff;}
.s-l{font-size:7px;color:#446;letter-spacing:2px;}
</style>
</head>
<body>
<div id="root">
  <div id="hud">
    <div class="hp-col">
      <div class="fn" id="fn-p1">P1</div>
      <div class="hp-bg"><div id="hf-p1" style="width:100%"></div></div>
    </div>
    <div class="center-hud"><div id="rnd-info">ROUND 1</div><div id="timer-val">99</div></div>
    <div class="hp-col">
      <div class="fn" id="fn-p2" style="text-align:right">CPU</div>
      <div class="hp-bg"><div id="hf-p2" style="width:100%"></div></div>
    </div>
  </div>
  <div id="superbars">
    <div class="sb-row" id="sb-p1"></div>
    <div style="font-size:7px;color:#334;letter-spacing:2px;align-self:center">SUPER</div>
    <div class="sb-row" id="sb-p2"></div>
  </div>
  <div id="win-dots" id="wdots"></div>
  <div id="canvas-wrap"><canvas id="gc"></canvas></div>
  <div id="rnd-result"></div>
  <div id="dpad">
    <div class="dp" id="dp-up">⬆</div>
    <div class="dp" id="dp-left">⬅</div>
    <div class="dp" id="dp-down">⬇</div>
    <div class="dp" id="dp-right">➡</div>
  </div>
  <div id="atk-btns">
    <div class="ab" id="ab-j"><span>⬆</span><span>점프</span></div>
    <div class="ab" id="ab-p"><span>👊</span><span>펀치</span></div>
    <div class="ab" id="ab-k"><span>🦵</span><span>킥</span></div>
    <div class="ab" id="ab-s"><span>✨</span><span>필살기</span></div>
  </div>
  <div id="keys-hint">
    <div class="kh-col"><div style="color:#3af">이동: ←→</div><div style="color:#3af">점프: ↑ / Z</div></div>
    <div class="kh-col"><div style="color:#f55">펀치: X / J</div><div style="color:var(--gold)">킥: C / K</div></div>
    <div class="kh-col"><div style="color:var(--purple)">필살기: V / L</div><div style="color:#555">가드: ↓ / S</div></div>
  </div>
  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>
<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  스트리트 파이터 EX v2.0
//  1v1 격투 게임 · 6 캐릭터 · AI CPU · 슈퍼 게이지 · 파티클
//  3라운드제 · 레벨별 CPU AI · 필살기 이펙트
// ══════════════════════════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');
const cWrap  = document.getElementById('canvas-wrap');

let CW=560, CH=380, SC=1;
function resize(){
  const w=cWrap.clientWidth,h=cWrap.clientHeight;
  SC=Math.min(w/CW,h/CH);
  canvas.width=CW;canvas.height=CH;
  canvas.style.width=(CW*SC)+'px';canvas.style.height=(CH*SC)+'px';
  canvas.style.left=((w-CW*SC)/2)+'px';
  canvas.style.top=((h-CH*SC)/2)+'px';
}
resize();window.addEventListener('resize',resize);

// KEYS
const KEYS={};
window.addEventListener('keydown',e=>{
  KEYS[e.code]=true;
  if(!G.running)return;
  if(e.code==='KeyX'||e.code==='KeyJ')doAtk(P1,'punch');
  if(e.code==='KeyC'||e.code==='KeyK')doAtk(P1,'kick');
  if(e.code==='KeyV'||e.code==='KeyL')doAtk(P1,'special');
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();
});
window.addEventListener('keyup',e=>KEYS[e.code]=false);

// CHARS
const CHARS=[
  {name:'류',   emoji:'🥋',hp:200,atk:22,spd:4.5,jump:17,supCost:25,col:'#33aaff',desc:'균형형・파동권'},
  {name:'블레이즈',emoji:'🔥',hp:178,atk:30,spd:5.2,jump:16,supCost:22,col:'#ff6600',desc:'공격형・화염 돌진'},
  {name:'아이스',  emoji:'❄️',hp:225,atk:18,spd:3.7,jump:18,supCost:28,col:'#88ccff',desc:'수비형・빙결 탄'},
  {name:'라이트닝',emoji:'⚡',hp:172,atk:27,spd:6.6,jump:20,supCost:20,col:'#f5c518',desc:'스피드형・전격'},
  {name:'철권',  emoji:'🦾',hp:245,atk:32,spd:3.3,jump:13,supCost:30,col:'#c04fff',desc:'파워형・지진권'},
  {name:'닌자',  emoji:'🥷',hp:182,atk:25,spd:6.2,jump:22,supCost:22,col:'#00ff88',desc:'민첩형・분신 베기'},
];

const FLOOR_Y=()=>CH-75;
const GRAV=0.85;

let G={running:false},P1,P2,PARTS=[],HITS=[],PROJS=[],selChar=0,diffLv=1;
let p1Wins=0,p2Wins=0,round=1,roundActive=false,roundTimer=0,raf=null;

function makeF(cIdx,isP2){
  const c=CHARS[cIdx];
  return {
    x:isP2?CW*.72:CW*.22,y:FLOOR_Y(),vx:0,vy:0,
    w:56,h:80,char:c,facing:isP2?-1:1,
    hp:c.hp,maxHp:c.hp,super:0,
    onGround:true,
    state:'idle',stateT:0,animF:0,
    hitCD:0,comboN:0,comboT:0,
    attackBox:null,isP2,
    ai:{rT:0,act:'idle'},
    _tL:false,_tR:false,_tJ:false,_tDown:false,
    blockT:0,
  };
}

// PARTICLES
function spawnParts(x,y,opt={}){
  const n=opt.n||8;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2,v=(opt.vMin||1.5)+Math.random()*(opt.vMax||5);
    const cols=Array.isArray(opt.col)?opt.col:[opt.col||'#fff'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      decay:(opt.dMin||.028)+Math.random()*(opt.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],sz:(opt.szMin||2)+Math.random()*(opt.szMax||5),
      glow:opt.glow||false});
  }
}
function spawnHN(x,y,txt,col,combo){
  HITS.push({x,y:y-20,txt:combo>1?`${combo}HIT! ${txt}`:txt,col,life:1,vy:-.6});
}

// COMBAT
function applyHit(atk,def,dmg,kb,type='normal'){
  if(def.state==='ko'||def.hitCD>0)return;
  if(def.state==='block'&&def.blockT>0&&type!=='special'){
    def.hp=Math.max(0,def.hp-dmg*.12);
    def.vx=atk.facing*2;
    spawnParts(def.x,def.y,{n:5,col:'rgba(0,200,255,.8)',glow:true,vMax:3});
    spawnHN(def.x,def.y-20,'BLOCK!','#3af',0);return;
  }
  def.hp=Math.max(0,def.hp-dmg);
  def.vx=atk.facing*kb;def.vy=-3.5;
  def.state='hurt';def.stateT=16;def.hitCD=10;
  atk.comboN++;atk.comboT=100;
  atk.super=Math.min(100,atk.super+9);def.super=Math.min(100,def.super+4);
  spawnParts(def.x,def.y,{n:type==='special'?16:10,col:[atk.char.col,'#ffaa44'],glow:type==='special',vMax:6,szMax:type==='special'?8:5});
  spawnHN(def.x,def.y-30,dmg+'!',atk.char.col,atk.comboN);
  if(def.hp<=0){def.state='ko';def.stateT=200;roundEnd(atk.isP2?'p2':'p1');}
}

function doAtk(p,type){
  if((p.stateT>0&&p.state!=='idle'&&p.state!=='walk')||p.state==='ko')return;
  if(type==='special'&&p.super<p.char.supCost)return;
  p.state=type;p.stateT=type==='punch'?18:type==='kick'?24:32;p.attackBox=null;
  if(type==='special'){
    p.super-=p.char.supCost;
    // Projectile
    PROJS.push({x:p.x+p.facing*40,y:p.y-p.h*.4,vx:p.facing*11,vy:0,
      life:65,sz:18,col:p.char.col,owner:p,dmg:Math.round(p.char.atk*2.3),glow:true});
    spawnParts(p.x,p.y,{n:12,col:p.char.col,glow:true,vMax:5,szMax:7});
  }
}

// AI
const AI_LEVELS=[.55,.72,.9];
function updateAI(cpu,opp){
  cpu.ai.rT--;
  if(cpu.ai.rT>0)return;
  cpu.ai.rT=6+Math.random()*14|0;
  const al=AI_LEVELS[diffLv];
  const dx=opp.x-cpu.x,dist=Math.abs(dx);
  cpu.facing=dx>0?1:-1;
  const r=Math.random();
  if(dist<110&&r<al*.5){
    if(r<al*.12&&cpu.super>=cpu.char.supCost)doAtk(cpu,'special');
    else if(r<al*.26)doAtk(cpu,'kick');
    else doAtk(cpu,'punch');
  } else if(dist>170&&r<al*.7){cpu.vx=cpu.facing*cpu.char.spd*.9;}
  else if(dist<55&&r<al*.25){cpu.vx=-cpu.facing*cpu.char.spd;}
  else if(r<al*.16&&cpu.onGround){cpu.vy=-cpu.char.jump;cpu.onGround=false;cpu.state='jump';}
  else if(r<al*.22){cpu.state='block';cpu.blockT=25;}
  else{cpu.vx=cpu.facing*cpu.char.spd*.5;}
}

function updateFighter(p,opp){
  p.vy+=GRAV;p.y+=p.vy;p.x+=p.vx;p.vx*=.74;
  if(p.y>=FLOOR_Y()){p.y=FLOOR_Y();p.vy=0;p.onGround=true;if(p.state==='jump')p.state='idle';}
  if(p.x<p.w/2)p.x=p.w/2;if(p.x>CW-p.w/2)p.x=CW-p.w/2;
  if(p.stateT>0)p.stateT--;
  else if(!['idle','walk','jump','block','ko'].includes(p.state)){p.state='idle';p.attackBox=null;}
  if(p.hitCD>0)p.hitCD--;
  if(p.comboT>0)p.comboT--;else p.comboN=0;
  if(p.blockT>0)p.blockT--;
  p.animF=(p.animF+1)%60;
  if(p.state==='idle'||p.state==='walk')p.facing=opp.x>p.x?1:-1;

  // Attack box check
  if((p.state==='punch'||p.state==='kick')&&p.stateT<9&&p.stateT>2){
    const reach=p.state==='kick'?88:68, dmg=p.state==='punch'?p.char.atk:Math.round(p.char.atk*1.55);
    const bx=p.x+p.facing*reach*.55, by=p.y-p.h*.5;
    if(Math.abs(bx-opp.x)<reach*.85&&Math.abs(by-opp.y)<p.h*.75){
      applyHit(p,opp,dmg,p.state==='punch'?5:7,p.state);
    }
  }
}

// ROUND
function roundEnd(winner){
  roundActive=false;
  const res=document.getElementById('rnd-result');
  if(winner==='p1'){p1Wins++;res.style.color='var(--blue)';res.textContent='🏆 P1 WIN!';}
  else{p2Wins++;res.style.color='var(--red)';res.textContent='CPU WIN!';}
  res.style.opacity='1';
  updateWinDots();
  setTimeout(()=>{
    res.style.opacity='0';
    if(p1Wins>=2||p2Wins>=2){setTimeout(showFightResult,400);}
    else{round++;newRound();}
  },2200);
}

function newRound(){
  P1=makeF(selChar,false);
  const cpuC=Math.floor(Math.random()*CHARS.length);
  P2=makeF(cpuC,true);
  P2.facing=-1;PROJS=[];
  roundTimer=99*60;roundActive=true;
  document.getElementById('rnd-info').textContent='ROUND '+round;
  document.getElementById('fn-p1').textContent=P1.char.name;
  document.getElementById('fn-p2').textContent='CPU·'+P2.char.name;
  buildSuperBars();
}

function updateWinDots(){
  const wd=document.getElementById('win-dots');wd.innerHTML='';
  for(let i=0;i<3;i++){
    const d=document.createElement('div');d.className='wd'+(i<p2Wins?' p2':i<p1Wins?' p1':'');wd.appendChild(d);
  }
}

function buildSuperBars(){
  ['p1','p2'].forEach(id=>{
    const el=document.getElementById('sb-'+id);el.innerHTML='';
    for(let i=0;i<4;i++){const s=document.createElement('div');s.className='sseg';const f=document.createElement('div');f.className='sfill';f.style.width='0%';s.appendChild(f);el.appendChild(s);}
  });
}

function updateSuperBars(){
  [[P1,'p1'],[P2,'p2']].forEach(([p,id])=>{
    const segs=document.querySelectorAll('#sb-'+id+' .sfill');
    const pct=p.super;
    segs.forEach((s,i)=>s.style.width=Math.min(100,Math.max(0,(pct-i*25)*4))+'%');
  });
}

// BACKGROUND DRAW
function drawBg(){
  // Sky-to-ground gradient
  const sky=ctx.createLinearGradient(0,0,0,CH);
  sky.addColorStop(0,'#120820'); sky.addColorStop(.55,'#180530'); sky.addColorStop(1,'#1a0340');
  ctx.fillStyle=sky;ctx.fillRect(0,0,CW,CH);

  // City silhouette back
  ctx.fillStyle='#0c0318';
  for(let i=0;i<16;i++){
    const bw=22+Math.sin(i*1.9)*10+6, bh=55+Math.sin(i*2.5)*40+20;
    const bx=i*(CW/15)-10;
    ctx.fillRect(bx,CH*.2-bh,bw,bh);
    for(let wy=CH*.2-bh+5;wy<CH*.2-4;wy+=10){
      if(Math.random()<.55)continue;
      ctx.fillStyle=`rgba(${Math.random()<.5?'0,200,255':'255,180,50'},.28)`;
      ctx.fillRect(bx+3+Math.random()*(bw-8),wy,3,6);ctx.fillStyle='#0c0318';
    }
  }

  // Ground
  const gr=ctx.createLinearGradient(0,CH*.7,0,CH);
  gr.addColorStop(0,'#1a0040');gr.addColorStop(1,'#0e0025');
  ctx.fillStyle=gr;ctx.fillRect(0,CH*.7,CW,CH*.3);

  // Neon floor line
  ctx.save();ctx.strokeStyle='rgba(192,79,255,.4)';ctx.shadowColor='rgba(192,79,255,.6)';ctx.shadowBlur=14;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(0,FLOOR_Y()+5);ctx.lineTo(CW,FLOOR_Y()+5);ctx.stroke();ctx.restore();

  // Floor grid
  ctx.strokeStyle='rgba(108,99,255,.06)';ctx.lineWidth=1;
  for(let gx=0;gx<CW;gx+=50){ctx.beginPath();ctx.moveTo(gx,FLOOR_Y());ctx.lineTo(gx,CH);ctx.stroke();}
  for(let gy=FLOOR_Y();gy<CH;gy+=25){ctx.beginPath();ctx.moveTo(0,gy);ctx.lineTo(CW,gy);ctx.stroke();}

  // Stage spotlights
  [[CW*.25,'rgba(0,100,255,.12)'],[CW*.75,'rgba(255,0,50,.1)']].forEach(([lx,col])=>{
    const sl=ctx.createRadialGradient(lx,FLOOR_Y()+10,0,lx,FLOOR_Y()+10,CW*.22);
    sl.addColorStop(0,col);sl.addColorStop(1,'transparent');
    ctx.fillStyle=sl;ctx.fillRect(0,0,CW,CH);
  });
}

function drawShadow(p){
  ctx.save();ctx.fillStyle='rgba(0,0,0,.3)';
  ctx.beginPath();ctx.ellipse(p.x,FLOOR_Y()+6,p.w*.5,9,0,0,Math.PI*2);ctx.fill();ctx.restore();
}

let gFrame=0;
function drawFighter(p){
  const x=p.x,y=p.y;
  ctx.save();ctx.translate(x,y);if(p.facing===-1)ctx.scale(-1,1);
  let sz=1,offY=0,rot=0,glow=null;
  if(p.state==='punch'){sz=1.2;ctx.shadowBlur=15;ctx.shadowColor=p.char.col;
    ctx.font='26px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('👊',p.w*.28,p.stateT>10?-p.h*.38:-p.h*.48);}
  else if(p.state==='kick'){sz=1.1;ctx.font='22px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('🦵',p.w*.25,-p.h*.22);}
  else if(p.state==='jump'){offY=-8-Math.abs(p.vy)*1.8;rot=p.facing*.18;}
  else if(p.state==='hurt'){sz=.88;rot=p.facing*-.16;ctx.filter='brightness(2.5) hue-rotate(300deg)';}
  else if(p.state==='block'&&p.blockT>0){
    ctx.save();ctx.strokeStyle='rgba(0,200,255,.5)';ctx.shadowColor='rgba(0,200,255,.4)';ctx.shadowBlur=14;ctx.lineWidth=2.5;
    ctx.fillStyle='rgba(0,200,255,.1)';ctx.beginPath();ctx.arc(p.w*.18,-p.h*.42,p.h*.55,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();}
  else if(p.state==='special'){sz=1.3;glow=p.char.col;}
  else if(p.state==='ko'){rot=p.facing*.75;offY=12;}
  else if(p.state==='idle'||p.state==='walk'){offY=Math.sin(p.animF*.12)*2;}
  ctx.rotate(rot);
  ctx.font=`${p.h*1.12*sz}px serif`;ctx.textAlign='center';ctx.textBaseline='bottom';
  if(glow){ctx.shadowBlur=22;ctx.shadowColor=glow;}
  ctx.fillText(p.char.emoji,0,-p.h*.02+offY);
  if(glow)ctx.shadowBlur=0;
  ctx.restore();
  // Super aura
  if(p.super>=100){
    ctx.save();ctx.strokeStyle=p.char.col+'77';ctx.lineWidth=2.5;
    ctx.shadowBlur=16+Math.sin(gFrame*.08)*8;ctx.shadowColor=p.char.col;
    ctx.beginPath();ctx.arc(p.x,p.y-p.h*.5,p.h*.72+Math.sin(gFrame*.07)*4,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
}

function drawProjs(){
  for(const pr of PROJS){
    ctx.save();ctx.shadowBlur=20;ctx.shadowColor=pr.col;ctx.fillStyle=pr.col;
    ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.8)';ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz*.35,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
}

function drawParts(){
  for(const p of PARTS){
    ctx.save();ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}
    ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.08,p.life),0,Math.PI*2);ctx.fill();
    if(p.glow)ctx.shadowBlur=0;ctx.restore();
  }
}

function drawHits(){
  for(const h of HITS){
    ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;
    ctx.fillStyle=h.col;ctx.font="bold 14px 'Black Han Sans',sans-serif";ctx.textAlign='center';
    ctx.fillText(h.txt,h.x,h.y);ctx.restore();
  }
}

function drawHPBars(){
  document.getElementById('hf-p1').style.width=(P1.hp/P1.maxHp*100)+'%';
  document.getElementById('hf-p2').style.width=(P2.hp/P2.maxHp*100)+'%';
}

function update(){
  gFrame++;
  for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.decay;p.life<=0&&PARTS.splice(i,1);}
  for(let i=HITS.length-1;i>=0;i--){const h=HITS[i];h.y+=h.vy;h.life-=.022;h.life<=0&&HITS.splice(i,1);}

  if(!roundActive)return;
  roundTimer--;
  document.getElementById('timer-val').textContent=Math.max(0,Math.ceil(roundTimer/60));
  if(roundTimer<=0){const w=P1.hp>=P2.hp?'p1':'p2';P2.state=w==='p1'?'ko':'idle';P1.state=w==='p2'?'ko':'idle';roundEnd(w);}

  // Projs
  for(let i=PROJS.length-1;i>=0;i--){
    const pr=PROJS[i];pr.x+=pr.vx;pr.life--;
    spawnParts(pr.x,pr.y,{n:1,col:pr.col,vMin:0,vMax:.5,szMin:.8,szMax:pr.sz*.5,dMin:.12,dMax:.16,glow:true});
    const opp=pr.owner.isP2?P1:P2;
    const dx=pr.x-opp.x,dy=pr.y-(opp.y-opp.h*.5);
    if(Math.abs(dx)<opp.w&&Math.abs(dy)<opp.h){applyHit(pr.owner,opp,pr.dmg,8,'special');pr.life=0;}
    if(pr.life<=0||pr.x<-40||pr.x>CW+40)PROJS.splice(i,1);
  }

  updateFighter(P1,P2);updateFighter(P2,P1);
  updateAI(P2,P1);
  updateSuperBars();

  // Player input
  const gl=KEYS['ArrowLeft']||KEYS['KeyA']||P1._tL;
  const gr=KEYS['ArrowRight']||KEYS['KeyD']||P1._tR;
  const gj=KEYS['ArrowUp']||KEYS['KeyZ']||P1._tJ;
  const gd=KEYS['ArrowDown']||KEYS['KeyS']||P1._tDown;
  if(P1.state==='idle'||P1.state==='walk'){
    if(gl){P1.vx=-P1.char.spd;P1.state='walk';}
    else if(gr){P1.vx=P1.char.spd;P1.state='walk';}
    else{P1.vx*=.55;if(Math.abs(P1.vx)<.5)P1.state='idle';}
    if(gj&&P1.onGround){P1.vy=-P1.char.jump;P1.onGround=false;P1.state='jump';}
    if(gd){P1.state='block';P1.blockT=4;}
  }
  drawHPBars();
}

function draw(){
  ctx.clearRect(0,0,CW,CH);
  drawBg();drawShadow(P1);drawShadow(P2);
  drawParts();drawProjs();drawFighter(P1);drawFighter(P2);drawHits();
}

function loop(){if(!G.running)return;update();draw();raf=requestAnimationFrame(loop);}

// TITLE
function showTitle(){
  buildSuperBars();updateWinDots();
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'],ddesc=['느린 CPU 반응','표준 CPU 속도','공격적 AI'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-badge">STREET FIGHTER EX v2.0</div>
    <div class="ov-title" style="color:var(--purple)">🥊 스트리트<br>파이터 EX</div>
    <div class="ov-sub">1 VS 1 · 6 CHARACTERS · AI CPU</div>
    <div style="font-size:8px;color:#446;line-height:2.2;margin-bottom:12px">캐릭터를 선택하고 CPU와 대전하세요<br>3라운드 2선승 · X/C/V 또는 버튼으로 공격</div>
    <div class="char-grid" id="char-grid-inner"></div>
    <div class="diff-row">${dnames.map((n,i)=>`<div class="dt${i===diffLv?' sel':''}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:1px">${ddesc[i]}</div></div>`).join('')}</div>
    <button class="ov-btn" onclick="startGame()">대전 시작 ⚡</button>`;
  buildCharGrid();
  document.getElementById('overlay').style.display='flex';
}

function buildCharGrid(){
  const g=document.getElementById('char-grid-inner');if(!g)return;g.innerHTML='';
  CHARS.forEach((c,i)=>{const d=document.createElement('div');d.className='cc'+(i===selChar?' sel':'');
    d.innerHTML=`<span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-stats">${c.desc}</div>`;
    d.onclick=()=>{selChar=i;document.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};
    g.appendChild(d);});
}
window.setDiff=d=>{diffLv=d;document.querySelectorAll('.dt').forEach((t,i)=>t.classList.toggle('sel',i===d));};

function showFightResult(){
  G.running=false;cancelAnimationFrame(raf);
  const win=p1Wins>=2;
  document.getElementById('ovc').innerHTML=`
    <div class="ov-badge">${win?'🏆 VICTORY':'DEFEAT'}</div>
    <div class="ov-title" style="color:${win?'var(--blue)':'var(--red)'}">${win?'승리!':'패배!'}</div>
    <div class="ov-sub">${win?'CHAMPION · YOU WIN':'TRY AGAIN'}</div>
    <div class="stats-row">
      <div class="s-chip"><div class="s-v" style="color:var(--blue)">${p1Wins}</div><div class="s-l">P1 승리</div></div>
      <div class="s-chip"><div class="s-v">${round}</div><div class="s-l">총 라운드</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--red)">${p2Wins}</div><div class="s-l">CPU 승리</div></div>
    </div>
    <button class="ov-btn" onclick="startGame()">다시 대전 🥊</button>
    <br><button class="ov-btn" style="margin-top:8px;font-size:12px;padding:8px 20px;color:#556;border-color:rgba(255,255,255,.08)" onclick="showTitle()">캐릭터 변경</button>`;
  document.getElementById('overlay').style.display='flex';
}

window.startGame=function(){
  document.getElementById('overlay').style.display='none';
  cancelAnimationFrame(raf);PARTS=[];HITS=[];PROJS=[];p1Wins=0;p2Wins=0;round=1;
  G={running:true};
  newRound();raf=requestAnimationFrame(loop);
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
addT('dp-left',()=>P1._tL=true,()=>P1._tL=false);
addT('dp-right',()=>P1._tR=true,()=>P1._tR=false);
addT('dp-up',()=>P1._tJ=true,()=>P1._tJ=false);
addT('dp-down',()=>P1._tDown=true,()=>P1._tDown=false);
addT('ab-j',()=>{if(G.running)P1._tJ=true;},()=>P1._tJ=false);
addT('ab-p',()=>{if(G.running)doAtk(P1,'punch');},null);
addT('ab-k',()=>{if(G.running)doAtk(P1,'kick');},null);
addT('ab-s',()=>{if(G.running)doAtk(P1,'special');},null);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
