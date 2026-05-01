import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스나이퍼 엘리트</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--green:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--purple:#c04fff;--bg:#06080a;--border:rgba(255,255,255,.07);}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;}
canvas{position:absolute;top:0;left:0;}

/* HUD */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;padding:10px 14px;
  background:linear-gradient(180deg,rgba(0,0,0,.88)0%,transparent 100%);
  display:flex;align-items:center;gap:8px;pointer-events:none;}
.hb{background:rgba(0,0,0,.44);border:1px solid var(--border);border-radius:9px;padding:4px 11px;text-align:center;}
.hv{font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:900;color:#fff;line-height:1.1;}
.hl{font-size:7px;color:#445;letter-spacing:2px;text-transform:uppercase;}
#hud-right{margin-left:auto;display:flex;gap:6px;align-items:center;}
#wind-box{font-size:9px;color:var(--cyan);display:flex;align-items:center;gap:5px;}
#wind-arr{font-size:18px;transition:transform .5s;}

/* MISSION BOX */
#mission-box{position:absolute;top:65px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;
  background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.07);border-radius:10px;padding:7px 16px;text-align:center;}
#ms-title{font-size:7px;color:#446;letter-spacing:3px;}
#ms-text{font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--gold);letter-spacing:1px;}
#ms-prog{font-size:8px;color:#556;margin-top:2px;}

/* AMMO BAR */
#ammo-bar{position:absolute;bottom:90px;right:14px;z-index:100;pointer-events:none;}
.a-col{display:flex;flex-direction:column;gap:3px;}
.adot{width:9px;height:20px;border-radius:3px;background:rgba(245,197,24,.1);border:1px solid rgba(245,197,24,.18);transition:all .1s;}
.adot.live{background:var(--gold);box-shadow:0 0 5px rgba(245,197,24,.6);}
#ammo-lbl{font-size:7px;color:#555;letter-spacing:2px;text-align:center;margin-top:4px;}

/* BREATH */
#breath-wrap{position:absolute;bottom:90px;left:50%;transform:translateX(-50%);z-index:100;text-align:center;pointer-events:none;}
#breath-lbl{font-size:7px;color:#446;letter-spacing:2px;margin-bottom:3px;}
#breath-bg{width:130px;height:6px;background:rgba(0,212,255,.08);border:1px solid rgba(0,212,255,.18);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:linear-gradient(90deg,#004466,var(--cyan));border-radius:99px;transition:width .08s;}

/* SCOPE */
#scope{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-overlay{position:absolute;inset:0;background:rgba(0,0,0,.88);}
#scope-lens{position:absolute;width:260px;height:260px;border-radius:50%;overflow:hidden;
  left:50%;top:50%;transform:translate(-50%,-50%);border:3px solid rgba(0,200,0,.55);box-shadow:0 0 0 2000px rgba(0,0,0,.88);}
#scope-cv{width:100%;height:100%;display:block;}
#scope-ui{position:absolute;inset:0;pointer-events:none;}

/* RELOAD RING */
#rl-ring{position:absolute;bottom:105px;left:50%;transform:translateX(-50%);z-index:100;text-align:center;display:none;}
#rl-cv{display:block;margin:0 auto 2px;}
#rl-txt{font-size:7px;color:var(--gold);letter-spacing:2px;}

/* KILL FEED */
#killfeed{position:absolute;top:70px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kfe{background:rgba(0,0,0,.5);border-left:3px solid var(--red);padding:4px 8px;font-size:9px;color:#ccc;
  border-radius:0 6px 6px 0;animation:kfs .25s ease;white-space:nowrap;}
@keyframes kfs{from{opacity:0;transform:translateX(14px);}to{opacity:1;transform:none;}}

/* SLOWMO FLASH */
#slowmo{position:absolute;inset:0;z-index:80;pointer-events:none;opacity:0;
  box-shadow:inset 0 0 0 5px rgba(255,215,0,.4);transition:opacity .2s;}

/* MISSION CLEAR */
#mc-banner{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;
  text-align:center;opacity:0;transition:opacity .25s;}
.mcb-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(28px,6vw,42px);letter-spacing:4px;text-shadow:0 0 28px currentColor;}
.mcb-sub{font-size:10px;color:#bbb;letter-spacing:3px;margin-top:4px;}

/* TOUCH BUTTONS */
#touch-btns{position:absolute;bottom:12px;left:50%;transform:translateX(-50%);display:flex;gap:10px;z-index:100;}
.tch{padding:11px 20px;border-radius:10px;border:1.5px solid;font-family:'Black Han Sans',sans-serif;font-size:13px;
  cursor:pointer;user-select:none;touch-action:none;transition:all .12s;}
.tch:active{transform:scale(.91);}
#tch-scope{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.38);color:var(--cyan);}
#tch-hold{background:rgba(0,255,136,.08);border-color:rgba(0,255,136,.32);color:var(--green);}
#tch-fire{background:rgba(255,34,68,.18);border-color:rgba(255,34,68,.48);color:var(--red);}
#tch-reload{background:rgba(245,197,24,.08);border-color:rgba(245,197,24,.32);color:var(--gold);}

/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:400;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:32px 24px;background:linear-gradient(160deg,#050808,#080e10);
  border:1px solid rgba(0,255,136,.18);border-radius:20px;min-width:310px;max-width:92vw;}
.ov-badge{display:inline-block;font-size:7px;letter-spacing:4px;color:var(--green);background:rgba(0,255,136,.08);
  border:1px solid rgba(0,255,136,.2);border-radius:99px;padding:3px 12px;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5.5vw,34px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#335;letter-spacing:4px;margin-bottom:16px;}
.diff-row{display:flex;gap:7px;justify-content:center;margin-bottom:14px;flex-wrap:wrap;}
.dt{padding:8px 16px;border-radius:99px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);cursor:pointer;color:#556;font-size:9px;transition:all .18s;text-align:center;}
.dt.sel{border-color:var(--green);color:var(--green);background:rgba(0,255,136,.08);}
.ov-btn{display:inline-block;padding:12px 30px;background:linear-gradient(135deg,rgba(0,255,136,.16),rgba(0,212,255,.1));
  border:1px solid rgba(0,255,136,.42);border-radius:12px;font-family:'Black Han Sans',sans-serif;
  font-size:16px;color:var(--green);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(0,255,136,.3),rgba(0,212,255,.2));transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,255,136,.28);}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.s-chip{padding:6px 12px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:8px;text-align:center;}
.s-v{font-family:'Rajdhani',sans-serif;font-size:15px;font-weight:900;color:#fff;}
.s-l{font-size:7px;color:#446;letter-spacing:2px;}
</style>
</head>
<body>
<div id="root">
  <canvas id="bgc"></canvas>
  <canvas id="gc"></canvas>

  <div id="hud">
    <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
    <div class="hb"><div class="hv" id="target-v">0/0</div><div class="hl">TARGETS</div></div>
    <div class="hb"><div class="hv" id="time-v">--</div><div class="hl">TIME</div></div>
    <div id="hud-right">
      <div id="wind-box"><div id="wind-arr">→</div>
        <div><div style="font-size:11px;font-weight:900" id="wind-spd">0 m/s</div><div style="font-size:7px;color:#334;letter-spacing:2px">WIND</div></div>
      </div>
    </div>
  </div>

  <div id="mission-box">
    <div id="ms-title">CURRENT MISSION</div>
    <div id="ms-text">대기 중...</div>
    <div id="ms-prog"></div>
  </div>

  <div id="ammo-bar"><div class="a-col" id="ammo-col"></div><div id="ammo-lbl">AMMO</div></div>
  <div id="breath-wrap"><div id="breath-lbl">호흡 (HOLD)</div><div id="breath-bg"><div id="breath-fill" style="width:100%"></div></div></div>

  <div id="scope">
    <div id="scope-overlay"></div>
    <div id="scope-lens">
      <canvas id="scope-cv" width="260" height="260"></canvas>
      <svg id="scope-ui" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <line x1="50" y1="0" x2="50" y2="43" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
        <line x1="50" y1="57" x2="50" y2="100" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
        <line x1="0" y1="50" x2="43" y2="50" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
        <line x1="57" y1="50" x2="100" y2="50" stroke="rgba(0,255,0,.65)" stroke-width=".7"/>
        <circle cx="50" cy="50" r="2.2" fill="none" stroke="rgba(0,255,0,.85)" stroke-width=".9"/>
        <circle cx="50" cy="50" r="14" fill="none" stroke="rgba(0,255,0,.28)" stroke-width=".4"/>
        <circle cx="50" cy="50" r="26" fill="none" stroke="rgba(0,255,0,.18)" stroke-width=".3"/>
        <line x1="50" y1="34" x2="50" y2="36" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
        <line x1="50" y1="64" x2="50" y2="66" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
        <line x1="34" y1="50" x2="36" y2="50" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
        <line x1="64" y1="50" x2="66" y2="50" stroke="rgba(0,255,0,.5)" stroke-width=".6"/>
        <text x="55" y="33" fill="rgba(0,255,0,.4)" font-size="3">200m</text>
        <text x="55" y="65" fill="rgba(0,255,0,.4)" font-size="3">400m</text>
      </svg>
    </div>
  </div>

  <div id="rl-ring"><canvas id="rl-cv" width="50" height="50"></canvas><div id="rl-txt">장전중...</div></div>
  <div id="killfeed"></div>
  <div id="slowmo"></div>

  <div id="mc-banner">
    <div class="mcb-big" id="mc-big" style="color:var(--gold)">✅ 미션 클리어!</div>
    <div class="mcb-sub" id="mc-sub"></div>
  </div>

  <div id="touch-btns">
    <div class="tch" id="tch-scope">🔭 조준경</div>
    <div class="tch" id="tch-hold">🫁 호흡</div>
    <div class="tch" id="tch-fire">🔫 발사</div>
    <div class="tch" id="tch-reload">🔄 장전</div>
  </div>

  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>
<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  스나이퍼 엘리트 v2.0
//  5 미션 시스템 · 스코프 4배율 · 바람 보정 · 헤드샷 판정
//  슬로우모션 이펙트 · 파티클 · 난이도 3단계
// ══════════════════════════════════════════════════════════════
const bgc  =document.getElementById('bgc');
const bgCtx=bgc.getContext('2d');
const canvas=document.getElementById('gc');
const ctx  =canvas.getContext('2d');
const scopeCV=document.getElementById('scope-cv');
const sCtx =scopeCV.getContext('2d');
const root =document.getElementById('root');

function resize(){canvas.width=bgc.width=root.clientWidth;canvas.height=bgc.height=root.clientHeight;}
resize();window.addEventListener('resize',()=>{resize();if(G.running)drawStaticBg();});

// MISSIONS
const MISSIONS=[
  {name:'표적 사격장',  desc:'정지 표적 5개 제거',   n:5,  time:90,moving:false,boss:false},
  {name:'이동 표적 추적',desc:'이동 표적 4개 제거',   n:4,  time:80,moving:true, boss:false},
  {name:'제한 시간 전투',desc:'60초에 7개 격파',      n:7,  time:60,moving:false,boss:false},
  {name:'바람 속 저격',  desc:'바람을 고려해 5개 격파',n:5, time:90,moving:true, boss:false},
  {name:'최종 임무 HVT', desc:'도주하는 고가치 표적!', n:1,  time:55,moving:true, boss:true},
];

const TARGET_TYPES=[
  {emoji:'🎯',sz:22,col:'#cc2200',pts:100,head:.35},
  {emoji:'💣',sz:24,col:'#3311aa',pts:150,head:.32},
  {emoji:'🪖',sz:20,col:'#334422',pts:120,head:.33},
  {emoji:'📦',sz:26,col:'#553311',pts:80, head:.4},
];

let G={running:false,diffLv:1};
let PARTS=[];

function initGame(){
  G={
    running:true,diffLv:G.diffLv,
    mIdx:0,score:0,totalKills:0,
    ammo:5,maxAmmo:5,reloading:false,relT:0,
    scoped:false,breathHeld:false,breath:100,
    wind:{dir:1,spd:0},
    targets:[],bullets:[],
    missionComplete:false,
    mouse:{x:canvas.width/2,y:canvas.height/2},
    scopeX:canvas.width/2,scopeY:canvas.height/2,
    frame:0,timer:0,
  };
  PARTS=[];
  drawStaticBg();buildAmmoBar();setWind();loadMission();
}

// BG
function drawStaticBg(){
  const W=canvas.width,H=canvas.height;
  bgCtx.fillStyle='#060809';bgCtx.fillRect(0,0,W,H);
  // Stars
  for(let i=0;i<100;i++){
    const sx=Math.random()*W,sy=Math.random()*H*.5;
    bgCtx.fillStyle=`rgba(255,255,220,${.3+Math.random()*.6})`;
    bgCtx.beginPath();bgCtx.arc(sx,sy,Math.random()<.05?1.4:.7,0,Math.PI*2);bgCtx.fill();
  }
  // Mountains
  const mcols=['#08100a','#0c1a0d','#102010','#152814'];
  for(let l=0;l<4;l++){
    bgCtx.fillStyle=mcols[l];bgCtx.beginPath();bgCtx.moveTo(0,H);
    const p=6+l*2;
    for(let i=0;i<=p;i++){
      const mx=i*(W/p),my=H*(.32+l*.07)+Math.sin(i*2.4+l)*H*(.13-l*.025);
      i===0?bgCtx.lineTo(mx,my):bgCtx.quadraticCurveTo((mx+(i-1)*(W/p))/2,my+18,mx,my);
    }
    bgCtx.lineTo(W,H);bgCtx.closePath();bgCtx.fill();
  }
  const fY=H*.62;
  // Trees
  bgCtx.fillStyle='#050e05';
  for(let i=0;i<38;i++){
    const tx=Math.random()*W,ty=fY-3,th=18+Math.random()*44,tw=10+Math.random()*16;
    bgCtx.beginPath();bgCtx.moveTo(tx,ty);bgCtx.lineTo(tx-tw/2,ty+th*.38);bgCtx.lineTo(tx-tw*.28,ty+th*.38);
    bgCtx.lineTo(tx-tw*.38,ty+th*.7);bgCtx.lineTo(tx,ty+th);bgCtx.lineTo(tx+tw*.38,ty+th*.7);bgCtx.lineTo(tx+tw*.28,ty+th*.38);bgCtx.lineTo(tx+tw/2,ty+th*.38);bgCtx.closePath();bgCtx.fill();
  }
  // Ground
  const gr=bgCtx.createLinearGradient(0,fY,0,H);
  gr.addColorStop(0,'#182a12');gr.addColorStop(1,'#0a1408');
  bgCtx.fillStyle=gr;bgCtx.fillRect(0,fY,W,H-fY);
  bgCtx.strokeStyle='rgba(0,80,0,.07)';bgCtx.lineWidth=1;
  for(let gy=fY;gy<H;gy+=20){bgCtx.beginPath();bgCtx.moveTo(0,gy);bgCtx.lineTo(W,gy);bgCtx.stroke();}
  // Buildings
  for(let i=0;i<8;i++){
    const bx=i*(W/7.5)-18,bw=28+Math.random()*46,bh=36+Math.random()*72;
    bgCtx.fillStyle='#050c04';bgCtx.fillRect(bx,fY-bh,bw,bh);
    for(let wx=bx+5;wx<bx+bw-5;wx+=10)for(let wy=fY-bh+5;wy<fY-5;wy+=13)
      if(Math.random()>.4){bgCtx.fillStyle='rgba(255,215,100,.3)';bgCtx.fillRect(wx,wy,4,7);}
  }
}

function setWind(){
  const wSpds=[0,1.5+Math.random()*1.5,2.5+Math.random()*2.5];
  G.wind.dir=Math.random()<.5?1:-1;
  G.wind.spd=G.wind.dir*wSpds[G.diffLv];
  document.getElementById('wind-arr').textContent=G.wind.spd===0?'○':G.wind.spd>0?'→':'←';
  document.getElementById('wind-spd').textContent=Math.abs(G.wind.spd).toFixed(1)+' m/s';
}

function loadMission(){
  const ms=MISSIONS[G.mIdx];
  G.missionComplete=false;G.timer=ms.time*60;
  G.ammo=G.maxAmmo;G.reloading=false;G.relT=0;
  spawnTargets(ms);buildAmmoBar();
  document.getElementById('ms-text').textContent=ms.desc;
  document.getElementById('ms-title').textContent='MISSION '+(G.mIdx+1)+'/5';
  updateHUD();
}

function spawnTargets(ms){
  const W=canvas.width,H=canvas.height;
  G.targets=[];
  const isBoss=ms.boss;
  for(let i=0;i<ms.n;i++){
    const t=isBoss?{emoji:'👹',sz:50,col:'#880000',pts:500,head:.28}:TARGET_TYPES[Math.floor(Math.random()*TARGET_TYPES.length)];
    const x=W*.1+Math.random()*W*.8;
    const zones=[.28,.36,.44,.56];
    const y=H*zones[Math.floor(Math.random()*zones.length)];
    G.targets.push({
      x,y,baseX:x,baseY:y,sz:isBoss?t.sz:t.sz+Math.random()*10,
      emoji:t.emoji,col:t.col,pts:t.pts,head:t.head,
      spd:ms.moving?(isBoss?2.2:0.8+Math.random()*1.2):0,
      phase:Math.random()*Math.PI*2,amp:W*(.04+Math.random()*.08),
      alive:true,flash:0,
      dist:200+Math.random()*600|0,
      isBoss,
    });
  }
}

// PARTICLES
function spawnParts(x,y,opt={}){
  const n=opt.n||8;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2,v=(opt.vMin||1.5)+Math.random()*(opt.vMax||5);
    const cols=Array.isArray(opt.col)?opt.col:[opt.col||'#ff2244'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      decay:(opt.dMin||.025)+Math.random()*(opt.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],sz:(opt.szMin||2)+Math.random()*(opt.szMax||5),glow:opt.glow||false});
  }
}

function buildAmmoBar(){
  const ac=document.getElementById('ammo-col');ac.innerHTML='';
  for(let i=0;i<G.maxAmmo;i++){const d=document.createElement('div');d.className='adot'+(i<G.ammo?' live':'');ac.appendChild(d);}
}

function startReload(){
  if(G.reloading||G.ammo>=G.maxAmmo)return;
  G.reloading=true;G.relT=100+G.diffLv*20;
  document.getElementById('rl-ring').style.display='block';
}

function fire(){
  if(G.ammo<=0||G.reloading||G.missionComplete)return;
  G.ammo--;buildAmmoBar();
  const drift=G.wind.spd*(G.diffLv>0?1:0)*14;
  const sway=G.breathHeld?0:G.diffLv*3.5;
  const swayOff={x:(Math.random()-.5)*sway,y:(Math.random()-.5)*sway};
  const hitX=(G.scoped?G.scopeX:G.mouse.x)+drift+swayOff.x;
  const hitY=(G.scoped?G.scopeY:G.mouse.y)+swayOff.y;

  let hit=false;
  G.targets.forEach(t=>{
    if(!t.alive||hit)return;
    const dx=hitX-t.x,dy=hitY-t.y;
    const dist=Math.sqrt(dx*dx+dy*dy);
    if(dist<t.sz*.9){
      hit=true;t.alive=false;
      const isHead=dist<t.sz*t.head;
      const pts=(isHead?300:100)*(t.isBoss?6:1);
      G.score+=pts;G.totalKills++;
      addKillfeed(t,isHead,pts);
      spawnParts(t.x,t.y,{n:isHead?20:12,col:['#cc0000','#ff2244','#880000'],glow:isHead,vMax:8,szMax:isHead?10:7});
      if(isHead||t.isBoss){
        document.getElementById('slowmo').style.opacity='1';
        setTimeout(()=>document.getElementById('slowmo').style.opacity='0',600);
      }
    }
  });
  if(!hit)spawnParts(hitX,hitY,{n:5,col:'rgba(180,180,180,.4)',vMax:3,szMax:3});
  // Tracer
  G.bullets.push({x:canvas.width/2,y:canvas.height/2,tx:hitX,ty:hitY,life:1});
  if(G.ammo<=0)setTimeout(startReload,250);
  checkClear();
}

function addKillfeed(t,head,pts){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kfe';
  d.innerHTML=`${t.emoji} ${head?'💀 헤드샷!':'격파'} <span style="color:var(--gold)">${t.dist}m</span> +${pts}pt`;
  if(head){d.style.borderLeftColor='var(--gold)';d.style.color='var(--gold)';}
  if(t.isBoss){d.style.borderLeftColor='var(--purple)';d.style.fontSize='11px';}
  kf.appendChild(d);setTimeout(()=>d.remove(),3000);
  while(kf.children.length>5)kf.removeChild(kf.firstChild);
}

function checkClear(){
  if(G.targets.filter(t=>t.alive).length===0&&!G.missionComplete){
    G.missionComplete=true;
    const bonus=(G.mIdx+1)*600;G.score+=bonus;
    const mc=document.getElementById('mc-banner');
    document.getElementById('mc-big').textContent=G.mIdx<4?'✅ 미션 클리어!':'🏆 전 임무 완료!';
    document.getElementById('mc-sub').textContent=`+${bonus.toLocaleString()} 보너스`;
    mc.style.opacity='1';
    setTimeout(()=>{
      mc.style.opacity='0';
      if(G.mIdx<4){G.mIdx++;setWind();loadMission();}
      else setTimeout(()=>showResult(true),400);
    },2600);
  }
}

function showResult(victory){
  G.running=false;
  const best=Math.max(G.score,parseInt(localStorage.getItem('snipeBest')||'0'));
  localStorage.setItem('snipeBest',best);
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-badge">${victory?'ALL MISSIONS CLEARED':'MISSION FAILED'}</div>
    <div class="ov-title" style="color:${victory?'var(--gold)':'var(--red)'}">${victory?'🏆 임무 완료!':'⏱️ 시간 초과'}</div>
    <div class="ov-sub">${victory?'MISSION COMPLETE':'TIME OVER'}</div>
    <div class="stats-row">
      <div class="s-chip"><div class="s-v" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="s-l">점수</div></div>
      <div class="s-chip"><div class="s-v">${G.totalKills}</div><div class="s-l">처치</div></div>
      <div class="s-chip"><div class="s-v" style="color:var(--cyan)">MISSION ${G.mIdx+1}</div><div class="s-l">도달</div></div>
    </div>
    <div style="font-size:8px;color:#446;margin-bottom:14px">최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>
    <button class="ov-btn" onclick="location.reload()">재배치 🎯</button>
  </div>`;
  ov.style.display='flex';
}

// SCOPE DRAW
function drawScope(){
  const el=document.getElementById('scope');
  if(!G.scoped){el.style.display='none';return;}
  el.style.display='block';
  const W=canvas.width,H=canvas.height,SW=260,SH=260;
  const zoom=4,srcW=W/zoom,srcH=H/zoom;
  const srcX=G.scopeX-srcW/2,srcY=G.scopeY-srcH/2;
  sCtx.drawImage(bgc,srcX,srcY,srcW,srcH,0,0,SW,SH);
  const scX=SW/srcW,scY=SH/srcH;
  G.targets.forEach(t=>{
    if(!t.alive)return;
    const tx=(t.x-srcX)*scX,ty=(t.y-srcY)*scY;
    sCtx.save();sCtx.font=`${t.sz*scX*1.5}px serif`;sCtx.textAlign='center';sCtx.textBaseline='middle';
    sCtx.shadowBlur=12;sCtx.shadowColor='rgba(255,50,0,.6)';sCtx.fillText(t.emoji,tx,ty);
    sCtx.strokeStyle='rgba(255,0,0,.22)';sCtx.lineWidth=1;sCtx.beginPath();sCtx.arc(tx,ty,t.sz*scX*.92,0,Math.PI*2);sCtx.stroke();
    sCtx.strokeStyle='rgba(255,255,0,.18)';sCtx.beginPath();sCtx.arc(tx,ty,t.sz*scX*t.head,0,Math.PI*2);sCtx.stroke();
    sCtx.restore();
  });
  // Green tint + vignette
  sCtx.fillStyle='rgba(0,25,0,.1)';sCtx.fillRect(0,0,SW,SH);
  const vg=sCtx.createRadialGradient(SW/2,SH/2,SW*.28,SW/2,SH/2,SW*.58);
  vg.addColorStop(0,'transparent');vg.addColorStop(1,'rgba(0,0,0,.48)');
  sCtx.fillStyle=vg;sCtx.fillRect(0,0,SW,SH);
  // Sway (when not holding breath)
  if(G.diffLv>0&&!G.breathHeld){
    const t=G.frame*.03;
    const sx=Math.sin(t*.65)*G.diffLv*2.2,sy=Math.cos(t)*G.diffLv*2.2;
    document.getElementById('scope-lens').style.transform=`translate(calc(-50% + ${sx}px),calc(-50% + ${sy}px))`;
  } else document.getElementById('scope-lens').style.transform='translate(-50%,-50%)';
}

function updateHUD(){
  document.getElementById('score-v').textContent=G.score.toLocaleString();
  const ms=MISSIONS[G.mIdx];
  const alive=G.targets.filter(t=>t.alive).length;
  document.getElementById('target-v').textContent=`${ms.n-alive}/${ms.n}`;
  document.getElementById('time-v').textContent=Math.max(0,Math.ceil(G.timer/60));
  document.getElementById('ms-prog').textContent=`${ms.n-alive}/${ms.n} 처치`;
  // reload ring
  if(G.reloading){
    const rlc=document.getElementById('rl-cv');
    const rc=rlc.getContext('2d');const pct=1-(G.relT/(100+G.diffLv*20));
    rc.clearRect(0,0,50,50);rc.strokeStyle='rgba(245,197,24,.14)';rc.lineWidth=4;
    rc.beginPath();rc.arc(25,25,20,0,Math.PI*2);rc.stroke();
    rc.strokeStyle='rgba(245,197,24,.8)';rc.shadowColor='rgba(245,197,24,.5)';rc.shadowBlur=7;
    rc.beginPath();rc.arc(25,25,20,-Math.PI*.5,-Math.PI*.5+Math.PI*2*pct);rc.stroke();
  }
}

function update(){
  G.frame++;
  if(!G.missionComplete){
    G.timer--;
    if(G.timer<=0){setTimeout(()=>showResult(false),300);}
  }
  if(G.reloading){
    G.relT--;
    if(G.relT<=0){G.ammo=G.maxAmmo;G.reloading=false;document.getElementById('rl-ring').style.display='none';buildAmmoBar();}
  }
  G.breathHeld?G.breath=Math.max(0,G.breath-.55):G.breath=Math.min(100,G.breath+.24);
  if(G.breath<=0)G.breathHeld=false;
  document.getElementById('breath-fill').style.width=G.breath+'%';

  G.targets.forEach(t=>{
    if(!t.alive)return;
    if(t.spd>0){t.phase+=.008*t.spd;t.x=t.baseX+Math.sin(t.phase)*t.amp;}
    if(t.flash>0)t.flash--;
  });
  for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.decay;p.life<=0&&PARTS.splice(i,1);}
  G.bullets=G.bullets.filter(b=>{b.life-=.14;return b.life>0;});
  updateHUD();
}

function draw(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  // Targets on main canvas
  G.targets.forEach(t=>{
    if(!t.alive)return;
    ctx.save();ctx.font=`${t.sz*1.6}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.shadowBlur=8;ctx.shadowColor='rgba(255,50,0,.4)';ctx.fillText(t.emoji,t.x,t.y);
    // Range text
    ctx.shadowBlur=0;ctx.fillStyle='rgba(255,255,255,.35)';ctx.font=`${t.sz*.38}px Orbitron,monospace`;ctx.fillText(t.dist+'m',t.x,t.y+t.sz*.9);
    ctx.restore();
  });
  // Bullet tracers
  for(const b of G.bullets){
    ctx.save();ctx.globalAlpha=b.life*.8;ctx.strokeStyle='rgba(255,220,100,.7)';ctx.lineWidth=1.5;
    ctx.shadowColor='rgba(255,200,50,.5)';ctx.shadowBlur=5;
    ctx.beginPath();ctx.moveTo(b.x,b.y);ctx.lineTo(b.tx,b.ty);ctx.stroke();ctx.restore();
  }
  // Particles
  for(const p of PARTS){
    ctx.save();ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}
    ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.08,p.life),0,Math.PI*2);ctx.fill();
    if(p.glow)ctx.shadowBlur=0;ctx.restore();
  }
  // Crosshair
  if(!G.scoped){
    const mx=G.mouse.x,my=G.mouse.y;
    ctx.save();ctx.strokeStyle='rgba(255,255,255,.6)';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(mx-9,my);ctx.lineTo(mx+9,my);ctx.moveTo(mx,my-9);ctx.lineTo(mx,my+9);ctx.stroke();
    ctx.beginPath();ctx.arc(mx,my,4,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  drawScope();
  update();
}

function loop(){if(!G.running)return;draw();requestAnimationFrame(loop);}

// TITLE
function showTitle(){
  const best=parseInt(localStorage.getItem('snipeBest')||'0');
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'],ddesc=['바람 없음·고정 표적','약한 바람·이동 표적','강풍+흔들림'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-badge">SNIPER ELITE KOREA</div>
    <div class="ov-title" style="color:var(--green)">🎯 스나이퍼<br>엘리트</div>
    <div class="ov-sub">5 MISSIONS · WIND BALLISTICS · HEADSHOT</div>
    <div style="font-size:8px;color:#446;line-height:2.2;margin-bottom:14px">
      우클릭(또는 조준경)으로 스코프 모드<br>
      HOLD/Shift으로 호흡 유지 → 정확도 향상<br>
      바람 방향·세기를 고려해 좌우 리드샷 적용<br>
      R·🔄 로 재장전 · 5개 미션 전부 클리어!
    </div>
    <div style="font-size:9px;color:#334;margin-bottom:10px;letter-spacing:2px">난이도</div>
    <div class="diff-row">${dnames.map((n,i)=>`<div class="dt${i===G.diffLv?' sel':''}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:2px">${ddesc[i]}</div></div>`).join('')}</div>
    ${best>0?`<div style="font-size:9px;color:#446;margin-bottom:12px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>`:''}
    <button class="ov-btn" onclick="startGame()">임무 시작 🎯</button>`;
  document.getElementById('overlay').style.display='flex';
}
window.setDiff=d=>{G.diffLv=d;document.querySelectorAll('.dt').forEach((t,i)=>t.classList.toggle('sel',i===d));};
window.startGame=()=>{document.getElementById('overlay').style.display='none';initGame();requestAnimationFrame(loop);};

// INPUT
canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect();G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;if(G.scoped){G.scopeX=G.mouse.x;G.scopeY=G.mouse.y;}});
canvas.addEventListener('click',()=>{if(G.running&&!G.missionComplete)fire();});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G.running)G.scoped=!G.scoped;});
canvas.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[0];const r=canvas.getBoundingClientRect();G.mouse.x=t.clientX-r.left;G.mouse.y=t.clientY-r.top;if(G.scoped){G.scopeX=G.mouse.x;G.scopeY=G.mouse.y;}},{passive:false});
canvas.addEventListener('touchend',e=>{e.preventDefault();if(G.running&&G.scoped)fire();},{passive:false});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift')G.breathHeld=true;
  if(e.key==='r'||e.key==='R')startReload();
  if(e.key==='z'||e.key==='Z'||e.key==='Escape'){if(G.running)G.scoped=!G.scoped;}
  if(e.key===' '){e.preventDefault();if(G.running)fire();}
});
document.addEventListener('keyup',e=>{if(e.key==='Shift')G.breathHeld=false;});

function addT(id,dn,up){
  const el=document.getElementById(id);if(!el)return;
  const d=e=>{e.preventDefault();if(dn)dn();};
  const u=e=>{e.preventDefault();if(up)up();};
  el.addEventListener('touchstart',d,{passive:false});el.addEventListener('touchend',u,{passive:false});
  el.addEventListener('mousedown',d);el.addEventListener('mouseup',u);
}
addT('tch-scope',()=>{if(G.running)G.scoped=!G.scoped;},null);
addT('tch-fire',()=>{if(G.running&&!G.missionComplete)fire();},null);
addT('tch-reload',()=>startReload(),null);
addT('tch-hold',()=>G.breathHeld=true,()=>G.breathHeld=false);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
