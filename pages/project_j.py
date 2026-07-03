import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>얼티밋 사커 11</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;user-select:none;}
:root{--blue:#2ea8ff;--red:#ff4757;--gold:#ffd400;--green:#0bdc6b;--bg:#04070a;--glass:rgba(255,255,255,.05);--border:rgba(255,255,255,.09);}
html,body{width:100%;height:900px;overflow:hidden;background:var(--bg);font-family:'Rajdhani',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:900px;overflow:hidden;}
canvas{position:absolute;top:120px;left:50%;transform:translateX(-50%);border-radius:14px;box-shadow:0 0 40px rgba(0,0,0,.6);}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;height:112px;z-index:100;background:linear-gradient(180deg,rgba(0,0,0,.9),rgba(0,0,0,.55));display:flex;align-items:center;justify-content:center;gap:28px;padding:0 10px;}
.hud-team{display:flex;flex-direction:column;align-items:center;min-width:90px;}
.hud-team-name{font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:2px;font-weight:900;}
.hud-team.b .hud-team-name{color:var(--blue);}
.hud-team.r .hud-team-name{color:var(--red);}
#score{font-family:'Black Han Sans',sans-serif;font-size:46px;letter-spacing:4px;text-shadow:0 0 18px rgba(255,255,255,.25);}
#center-info{display:flex;flex-direction:column;align-items:center;gap:4px;}
#timer{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;color:var(--gold);letter-spacing:2px;}
#poss-bar{width:150px;height:6px;border-radius:6px;overflow:hidden;background:rgba(255,255,255,.08);display:flex;}
#poss-b{background:var(--blue);height:100%;}
#poss-r{background:var(--red);height:100%;}
#stam-wrap{position:absolute;top:118px;left:50%;transform:translateX(-336px);width:140px;z-index:100;}
#stam-lbl{font-size:9px;color:#8aa;letter-spacing:2px;margin-bottom:2px;}
#stam-bg{height:8px;border-radius:6px;background:rgba(255,255,255,.08);overflow:hidden;border:1px solid var(--border);}
#stam-fill{height:100%;background:linear-gradient(90deg,#0bdc6b,#ffd400);width:100%;transition:width .1s;}
#power-wrap{position:absolute;bottom:26px;left:50%;transform:translateX(-50%);width:260px;z-index:100;display:none;text-align:center;}
#power-lbl{font-size:10px;color:var(--gold);letter-spacing:3px;margin-bottom:3px;font-family:'Orbitron',sans-serif;}
#power-bg{height:12px;border-radius:8px;background:rgba(255,255,255,.08);overflow:hidden;border:1.5px solid rgba(255,212,0,.4);}
#power-fill{height:100%;width:0%;background:linear-gradient(90deg,#0bdc6b,#ffd400,#ff4757);}

/* ── banners ── */
#banner{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);z-index:250;text-align:center;opacity:0;pointer-events:none;transition:opacity .2s,transform .2s;}
#banner-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(40px,8vw,64px);color:var(--gold);text-shadow:0 0 30px rgba(255,212,0,.8),0 0 60px rgba(255,212,0,.4);letter-spacing:4px;}
#banner-sub{font-size:13px;color:#cde;letter-spacing:3px;margin-top:6px;}

/* ── key guide ── */
#keyguide{position:absolute;bottom:8px;left:8px;z-index:100;background:rgba(0,0,0,.55);border:1px solid var(--border);border-radius:10px;padding:8px 12px;font-size:10.5px;color:#9fb0c0;line-height:1.65;max-width:260px;}
#keyguide b{color:var(--gold);}
#keyguide .kg-title{color:#fff;font-weight:900;font-size:11px;letter-spacing:1px;margin-bottom:3px;}
#kg-toggle{position:absolute;bottom:8px;right:8px;z-index:101;background:rgba(0,0,0,.55);border:1px solid var(--border);color:#cde;border-radius:8px;padding:6px 12px;font-size:11px;cursor:pointer;}

/* ── overlays ── */
.overlay{position:absolute;inset:0;z-index:300;background:rgba(2,4,8,.94);display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
.ov-box{width:min(560px,92vw);background:linear-gradient(160deg,#060c11,#0a1420);border:1px solid rgba(46,168,255,.25);border-radius:20px;padding:30px 26px;text-align:center;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:30px;background:linear-gradient(90deg,var(--blue),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:2px;margin-bottom:6px;}
.ov-sub{color:#8aa;font-size:12px;margin-bottom:18px;letter-spacing:1px;}
.ov-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:left;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:12px;padding:14px 16px;margin-bottom:18px;font-size:11.5px;color:#aebccb;line-height:1.75;}
.ov-grid b{color:var(--gold);}
.ov-grid .grp{color:#fff;font-weight:900;font-size:11px;margin-top:6px;letter-spacing:1px;}
.ov-grid .grp:first-child{margin-top:0;}
#startBtn,#retryBtn,#exitBtn{font-family:'Orbitron',sans-serif;font-weight:900;letter-spacing:1px;border:none;border-radius:12px;padding:14px 0;width:100%;font-size:15px;cursor:pointer;margin-top:8px;}
#startBtn{background:linear-gradient(90deg,#0bdc6b,#2ea8ff);color:#05121a;}
#retryBtn{background:linear-gradient(90deg,#ffd400,#ff8c42);color:#221400;}
#exitBtn{background:rgba(255,255,255,.08);color:#cde;border:1px solid var(--border);}
#result-score{font-family:'Black Han Sans',sans-serif;font-size:52px;margin:10px 0;letter-spacing:4px;}
#result-tag{font-size:15px;font-weight:900;letter-spacing:3px;margin-bottom:14px;}
</style>
</head>
<body>
<div id="root">
  <div id="hud">
    <div class="hud-team b"><div class="hud-team-name">BLUE (나)</div></div>
    <div id="score">0 : 0</div>
    <div class="hud-team r"><div class="hud-team-name">RED (AI)</div></div>
  </div>
  <div id="center-info" style="position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:101;">
    <div id="timer">3:00</div>
    <div id="poss-bar"><div id="poss-b" style="width:50%;"></div><div id="poss-r" style="width:50%;"></div></div>
  </div>
  <div id="stam-wrap"><div id="stam-lbl">STAMINA</div><div id="stam-bg"><div id="stam-fill"></div></div></div>
  <canvas id="pitch" width="900" height="580"></canvas>
  <div id="banner"><div id="banner-big"></div><div id="banner-sub"></div></div>
  <div id="power-wrap"><div id="power-lbl">SHOT POWER</div><div id="power-bg"><div id="power-fill"></div></div></div>

  <div id="keyguide">
    <div class="kg-title">⚽ 조작키</div>
    방향키: 이동 &nbsp; | &nbsp; <b>E</b> 스프린트 &nbsp; | &nbsp; <b>Shift+방향</b> 스킬무브<br>
    <span style="color:#2ea8ff;">[공격]</span> <b>S</b>짧은패스 <b>W</b>스루패스 <b>A</b>롱패스/크로스 <b>D</b>슛(홀드) <b>Q</b>선수호출 <b>C</b>볼보호<br>
    <span style="color:#ff4757;">[수비]</span> <b>D</b>스탠딩태클 <b>A</b>슬라이딩 <b>S</b>선수변경 <b>Q</b>압박 <b>C</b>조키<br>
    <span style="color:#ffd400;">[GK]</span> <b>A</b>멀리차기 <b>S</b>짧게던지기 <b>D</b>펀칭 <b>W</b>돌진
  </div>
  <div id="kg-toggle">⌨ 키 숨기기</div>

  <div class="overlay" id="startOverlay">
    <div class="ov-box">
      <div class="ov-title">⚽ ULTIMATE SOCCER 11</div>
      <div class="ov-sub">11 vs 11 실시간 축구 매치 · 3분 1경기</div>
      <div class="ov-grid">
        <div>
          <div class="grp">🔵 공격 (볼 소유 시)</div>
          <b>W</b> 스루패스 &nbsp;<b>A</b> 롱패스/크로스<br>
          <b>S</b> 짧은패스 &nbsp;<b>D</b> 슛(홀드=강슛)<br>
          <b>Q</b> 선수호출(런) &nbsp;<b>C</b> 볼보호<br>
          <b>E</b> 스프린트 &nbsp;<b>Shift+방향</b> 스킬무브
        </div>
        <div>
          <div class="grp">🔴 수비 (볼 미소유 시)</div>
          <b>D</b> 스탠딩 태클<br>
          <b>A</b> 슬라이딩 태클<br>
          <b>S</b> 선수 변경 &nbsp;<b>Q</b> 협력 압박<br>
          <b>C</b> 조키(견제) &nbsp;<b>E</b> 스프린트
        </div>
      </div>
      <div class="ov-sub" style="margin-top:-10px;">🧤 골키퍼 조작 시: <b style="color:#ffd400;">A</b>멀리차기 <b style="color:#ffd400;">S</b>짧게던지기 <b style="color:#ffd400;">D</b>펀칭 <b style="color:#ffd400;">W</b>돌진</div>
      <button id="startBtn">🏁 킥오프!</button>
    </div>
  </div>

  <div class="overlay" id="endOverlay" style="display:none;">
    <div class="ov-box">
      <div class="ov-title">🏁 FULL TIME</div>
      <div id="result-score">0 : 0</div>
      <div id="result-tag"></div>
      <button id="retryBtn">🔄 다시 하기</button>
      <button id="exitBtn">📋 종료</button>
    </div>
  </div>
</div>

<script>
(function(){
"use strict";
const cv = document.getElementById('pitch');
const ctx = cv.getContext('2d');
const W=900,H=580, H0=44,H1=856, V0=44,V1=536;
const GY0=232, GY1=348; // goal mouth
const GOAL_L_X=H0, GOAL_R_X=H1;
const MATCH_TIME=180;

function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function dist(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
function now(){return performance.now()/1000;}

// ── 포메이션 (4-4-2) ──
const FORM=[
 {x:.06,y:.50},
 {x:.19,y:.16},{x:.17,y:.38},{x:.17,y:.62},{x:.19,y:.84},
 {x:.47,y:.20},{x:.43,y:.42},{x:.43,y:.58},{x:.47,y:.80},
 {x:.75,y:.40},{x:.75,y:.60}
];

function makeTeam(team){
  const arr=[];
  for(let i=0;i<11;i++){
    const f=FORM[i];
    const fx = team==='B'? f.x : 1-f.x;
    arr.push({
      id:team+i, team, num:i+1, role: i===0?'GK':(i<5?'DF':(i<9?'MF':'FW')),
      isGK:i===0, baseFx:fx, baseFy:f.y,
      x:H0+fx*(H1-H0), y:V0+f.y*(V1-V0),
      vx:0, vy:0, facing:{x:team==='B'?1:-1,y:0},
      stamina:100, shielding:false, jockeying:false,
      runUntil:0, pressUntil:0, stumbleUntil:0, skillEvadeUntil:0
    });
  }
  return arr;
}

let blue, red, players, ball, score, timeLeft, activeBlueIdx, gameState, freezeUntil, lastSwitch;
let chargingShot=false, chargeStart=0;
let possAcc={b:0,r:0};

function resetKickoff(){
  blue=makeTeam('B'); red=makeTeam('R'); players=[...blue,...red];
  ball={x:W/2,y:H/2,vx:0,vy:0,owner:null,intended:null,dangerChecked:false,lofted:0};
  activeBlueIdx=6;
  freezeUntil=now()+0.8;
}

function fullReset(){
  resetKickoff();
  score={B:0,R:0};
  timeLeft=MATCH_TIME;
  gameState='playing';
  possAcc={b:1,r:1};
}

const keys=new Set();
let shiftDown=false;

function activePlayer(){ return blue[activeBlueIdx]; }

function inOwnBox(p,team){
  if(team==='B') return p.x<H0+150 && p.y>GY0-60 && p.y<GY1+60;
  return p.x>H1-150 && p.y>GY0-60 && p.y<GY1+60;
}

function slotPos(p){
  const ballFx=clamp((ball.x-H0)/(H1-H0),0,1);
  let shift=(ballFx-0.5)*0.16;
  const fx=clamp(p.baseFx + shift*(p.isGK?0.08:1),0.04,0.96);
  return {x:H0+fx*(H1-H0), y:V0+p.baseFy*(V1-V0)};
}

function steerTo(p,tx,ty,spd,dt){
  const dx=tx-p.x, dy=ty-p.y, d=Math.hypot(dx,dy)||1;
  const vx=dx/d*spd, vy=dy/d*spd;
  p.vx=vx; p.vy=vy;
  p.x+=vx*dt; p.y+=vy*dt;
  if(d>2) p.facing={x:dx/d,y:dy/d};
}

function clampP(p){
  p.x=clamp(p.x, H0-4, H1+4);
  p.y=clamp(p.y, V0+8, V1-8);
  if(!p.isGK){ p.x=clamp(p.x,H0+6,H1-6); }
}

function nearestOnTeamToBall(team, excludeGKUnlessBox, excludeP){
  const arr=team==='B'?blue:red;
  let best=null,bd=1e9;
  for(const q of arr){
    if(q===excludeP) continue;
    if(q.isGK && excludeGKUnlessBox && !inOwnBox(q,team)) continue;
    const d=dist(q,ball);
    if(d<bd){bd=d;best=q;}
  }
  return best;
}

function designatedChaser(defTeam){
  const arr= defTeam==='B'?blue:red;
  let best=null,bd=1e9;
  for(const q of arr){
    if(q.isGK) continue;
    if(defTeam==='B' && q===activePlayer()) continue;
    const d=dist(q,ball.owner||ball);
    if(d<bd){bd=d;best=q;}
  }
  return best;
}

// ── passing / shooting helpers ──
function mates(team,exclude){ return (team==='B'?blue:red).filter(p=>p!==exclude && !p.isGK); }

function pickForwardMate(passer){
  const dir=passer.team==='B'?1:-1;
  let best=null,bv=-1e9;
  for(const m of mates(passer.team,passer)){
    const v=(m.x-passer.x)*dir;
    if(v>bv){bv=v;best=m;}
  }
  return best||passer;
}
function pickNearMate(passer){
  let best=null,bd=1e9;
  for(const m of mates(passer.team,passer)){
    const d=dist(m,passer);
    if(d<bd){bd=d;best=m;}
  }
  return best||passer;
}

function kickTo(x,y,spd,lofted){
  const dx=x-ball.x, dy=y-ball.y, d=Math.hypot(dx,dy)||1;
  ball.vx=dx/d*spd; ball.vy=dy/d*spd;
  ball.owner=null; ball.lofted=lofted?1:0; ball.dangerChecked=false;
}

function doShortPass(passer){
  const t=pickNearMate(passer);
  kickTo(t.x,t.y,340,false);
  ball.intended=t;
}
function doThroughPass(passer){
  const t=pickForwardMate(passer);
  const dir=passer.team==='B'?1:-1;
  kickTo(t.x+dir*70, t.y, 430, false);
  t.runUntil=now()+1.3;
  ball.intended=t;
}
function doLongOrCross(passer){
  const nearByline = passer.team==='B' ? passer.x>H1-220 : passer.x<H0+220;
  if(nearByline){
    const bx = passer.team==='B'? H1-30 : H0+30;
    const by = 290 + (Math.random()*70-35);
    kickTo(bx,by,470,true);
  } else {
    const t=pickForwardMate(passer);
    kickTo(t.x,t.y,470,true);
  }
  ball.intended=null;
}
function doShoot(passer,power){
  const goalX = passer.team==='B'? GOAL_R_X : GOAL_L_X;
  const off=(passer.facing.y||0)*36;
  const aimY = clamp(290+off, GY0+10, GY1-10);
  const dx=goalX-passer.x, dy=aimY-passer.y, d=Math.hypot(dx,dy)||1;
  const spd=560+power*420;
  ball.vx=dx/d*spd; ball.vy=dy/d*spd;
  ball.owner=null; ball.shotBy=passer; ball.dangerChecked=false; ball.lofted=0;
}
function doCallRun(passer){
  const t=pickForwardMate(passer);
  t.runUntil=now()+1.4;
}
function doGKLongKick(gk){
  const t=pickForwardMate(gk);
  kickTo(t.x,t.y,520,true);
}
function doGKShortThrow(gk){
  const t=pickNearMate(gk);
  kickTo(t.x,t.y,300,false);
}
function doGKPunch(gk){
  ball.vx = -ball.vx*1.1 + (gk.team==='B'?260:-260);
  ball.vy = (Math.random()-0.5)*420;
  ball.owner=null; ball.dangerChecked=true;
}

function attemptStandingTackle(defender){
  const carrier=ball.owner;
  if(!carrier || carrier.team===defender.team) return;
  const d=dist(defender,carrier);
  if(d<24){
    let chance=0.5;
    if(carrier.shielding) chance-=0.22;
    if(carrier.skillEvadeUntil>now()) chance-=0.3;
    if(Math.random()<chance){
      ball.owner=defender; ball.vx=0; ball.vy=0; ball.intended=null;
    } else {
      defender.stumbleUntil=now()+0.25;
    }
  }
}
function attemptSlideTackle(defender){
  const carrier=ball.owner;
  if(!carrier || carrier.team===defender.team) return;
  const d=dist(defender,carrier);
  if(d<38){
    let chance=0.62;
    if(carrier.shielding) chance-=0.2;
    if(carrier.skillEvadeUntil>now()) chance-=0.35;
    defender.stumbleUntil=now()+0.55;
    if(Math.random()<chance){
      ball.owner=defender; ball.vx=0; ball.vy=0; ball.intended=null;
      defender.stumbleUntil=now()+0.3;
    }
  }
}

// ── input ──
window.addEventListener('keydown',(e)=>{
  if(gameState!=='playing') return;
  const code=e.code;
  if(code==='ShiftLeft'||code==='ShiftRight'){ shiftDown=true; return; }
  if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(code)){
    e.preventDefault();
    if(shiftDown && !keys.has(code)){
      const p=activePlayer();
      if(ball.owner===p){
        p.skillEvadeUntil=now()+0.5;
        const bx = code==='ArrowLeft'?-1:code==='ArrowRight'?1:0;
        const by = code==='ArrowUp'?-1:code==='ArrowDown'?1:0;
        p.vx += bx*260; p.vy += by*260;
      }
    }
    keys.add(code);
    return;
  }
  if(keys.has(code)) return;
  keys.add(code);
  const p=activePlayer();
  const hasBall = ball.owner===p;
  if(code==='KeyD'){
    if(p.isGK && !hasBall){ doGKPunch(p); }
    else if(hasBall){ chargingShot=true; chargeStart=now(); }
    else { attemptStandingTackle(p); }
  } else if(code==='KeyA'){
    if(p.isGK && hasBall){ doGKLongKick(p); }
    else if(hasBall){ doLongOrCross(p); }
    else { attemptSlideTackle(p); }
  } else if(code==='KeyS'){
    if(p.isGK && hasBall){ doGKShortThrow(p); }
    else if(hasBall){ doShortPass(p); }
    else { switchPlayer(); }
  } else if(code==='KeyW'){
    if(p.isGK){ p.rushBoost=true; }
    else if(hasBall){ doThroughPass(p); }
  } else if(code==='KeyQ'){
    if(hasBall){ doCallRun(p); }
    else { const c=designatedChaser('B'); if(c) c.pressUntil=now()+1.0; }
  } else if(code==='KeyC'){
    p.shielding = hasBall; p.jockeying = !hasBall;
  } else if(code==='KeyE'){
    p.sprint=true;
  }
});
window.addEventListener('keyup',(e)=>{
  const code=e.code;
  if(code==='ShiftLeft'||code==='ShiftRight'){ shiftDown=false; return; }
  keys.delete(code);
  const p=activePlayer();
  if(code==='KeyD'){
    if(chargingShot){
      const held=clamp(now()-chargeStart,0,0.9)/0.9;
      if(ball.owner===p) doShoot(p,held);
      chargingShot=false;
    }
  }
  if(code==='KeyC'){ p.shielding=false; p.jockeying=false; }
  if(code==='KeyE'){ p.sprint=false; }
  if(code==='KeyW' && p.isGK){ p.rushBoost=false; }
});

let switchLockUntil=0;
function switchPlayer(){
  if(now()<switchLockUntil) return;
  const cur=activePlayer();
  let cands=blue.filter(p=>p!==cur).sort((a,b)=>dist(a,ball)-dist(b,ball));
  if(cands.length){
    activeBlueIdx = blue.indexOf(cands[0]);
    switchLockUntil=now()+0.25;
  }
}
function autoSwitch(){
  if(now()<switchLockUntil) return;
  if(ball.owner && ball.owner.team==='B') return;
  const cur=activePlayer();
  const near = nearestOnTeamToBall('B', true, null);
  if(near && near!==cur && dist(near,ball) < dist(cur,ball)-14){
    activeBlueIdx=blue.indexOf(near);
  }
}

// ── AI ──
function aiCarrierDecision(p, dt){
  // random chance per frame-ish to pass/shoot/dribble forward
  const dir=p.team==='B'?1:-1;
  const goalX = p.team==='B'?GOAL_R_X:GOAL_L_X;
  const distToGoal=Math.abs(goalX-p.x);
  if(distToGoal<210 && Math.random()<0.018){
    doShoot(p, 0.55+Math.random()*0.4); return;
  }
  if(Math.random()<0.01){
    const t=pickForwardMate(p);
    kickTo(t.x,t.y, 380, false); ball.intended=t; return;
  }
  // dribble forward with slight juke
  const jitter=Math.sin(now()*3+p.num)*30;
  steerTo(p, p.x+dir*40, clamp(p.y+jitter*0.4,V0+20,V1-20), p.isGK?0:150*(p.sprintAI?1.5:1), dt);
}

function aiStep(p,dt){
  const t=now();
  if(p===activePlayer()) return;
  if(t<p.stumbleUntil){ p.x+=p.vx*0.9*dt; p.y+=p.vy*0.9*dt; clampP(p); return; }

  if(ball.owner===p){
    if(p.isGK){
      // AI GK holding ball -> clear quickly
      if(Math.random()<0.03) doGKLongKick(p);
      return;
    }
    aiCarrierDecision(p,dt);
    ball.x=p.x+p.facing.x*13; ball.y=p.y+p.facing.y*13;
    clampP(p);
    return;
  }

  let tx,ty,spd=145;
  if(p.isGK){
    tx = p.team==='B'? H0+22 : H1-22;
    ty = clamp(ball.y, GY0+16, GY1-16);
    spd=125;
    if(inOwnBox(p,p.team) && ball.owner && ball.owner.team!==p.team && dist(p,ball)<130) spd=150;
  } else if(p.runUntil>t){
    const dir=p.team==='B'?1:-1;
    tx=p.x+dir*36; ty=p.y; spd=205;
  } else if(p.pressUntil>t){
    tx=ball.x; ty=ball.y; spd=195;
  } else if(!ball.owner && nearestOnTeamToBall(p.team,true,activePlayer())===p){
    tx=ball.x; ty=ball.y; spd=185;
  } else if(ball.owner && ball.owner.team!==p.team && designatedChaser(p.team)===p){
    tx=ball.owner.x; ty=ball.owner.y; spd=190;
    if(dist(p,ball.owner)<22 && Math.random()<0.035) attemptStandingTackle(p);
  } else {
    const s=slotPos(p); tx=s.x; ty=s.y; spd=140;
  }
  steerTo(p,tx,ty,spd,dt);
  clampP(p);
}

// ── main player (user) movement ──
function humanStep(dt){
  const p=activePlayer();
  const t=now();
  if(t<p.stumbleUntil){ p.x+=p.vx*0.9*dt; p.y+=p.vy*0.9*dt; clampP(p); return; }
  let mx=0,my=0;
  if(keys.has('ArrowUp')) my-=1;
  if(keys.has('ArrowDown')) my+=1;
  if(keys.has('ArrowLeft')) mx-=1;
  if(keys.has('ArrowRight')) mx+=1;
  const mlen=Math.hypot(mx,my);
  if(mlen>0){ mx/=mlen; my/=mlen; p.facing={x:mx,y:my}; }

  let spd=175;
  const sprinting = keys.has('KeyE') && p.stamina>2;
  if(sprinting){ spd*=1.55; p.stamina=clamp(p.stamina-38*dt,0,100); }
  else { p.stamina=clamp(p.stamina+22*dt,0,100); }
  if(p.shielding||p.jockeying) spd*=0.62;
  if(p.isGK){
    spd*=0.86;
    if(p.rushBoost) spd*=1.5;
  }

  p.vx=mx*spd; p.vy=my*spd;
  p.x+=p.vx*dt; p.y+=p.vy*dt;

  if(p.isGK && !p.rushBoost){
    p.x=clamp(p.x, H0-2, H0+170);
  } else {
    clampP(p);
  }

  if(ball.owner===p){
    const fx=p.facing.x||1, fy=p.facing.y||0;
    ball.x = p.x + fx*15;
    ball.y = p.y + fy*15;
  }
}

// ── ball physics & goal check ──
function ballStep(dt){
  if(ball.owner) return;
  const fr = ball.lofted? 0.994 : 0.985;
  ball.vx*=fr; ball.vy*=fr;
  ball.x += ball.vx*dt; ball.y += ball.vy*dt;

  if(ball.y<V0+8){ ball.y=V0+8; ball.vy=Math.abs(ball.vy)*0.55; }
  if(ball.y>V1-8){ ball.y=V1-8; ball.vy=-Math.abs(ball.vy)*0.55; }

  const inGoalMouthY = ball.y>GY0 && ball.y<GY1;
  if(ball.x<H0-2){
    if(inGoalMouthY){ scoreGoal('R'); return; }
    ball.x=H0-2; ball.vx=Math.abs(ball.vx)*0.5;
  }
  if(ball.x>H1+2){
    if(inGoalMouthY){ scoreGoal('B'); return; }
    ball.x=H1+2; ball.vx=-Math.abs(ball.vx)*0.5;
  }

  // GK save roll when ball enters danger zone
  if(!ball.dangerChecked){
    if(ball.x<H0+110 && ball.vx<0){
      ball.dangerChecked=true;
      const gk=blue.find(p=>p.isGK);
      tryGKSave(gk, ball.x<H0+150);
    } else if(ball.x>H1-110 && ball.vx>0){
      ball.dangerChecked=true;
      const gk=red.find(p=>p.isGK);
      tryGKSave(gk, ball.x>H1-150);
    }
  }

  // capture
  let bestP=null,bestD=1e9;
  for(const p of players){
    if(now()<p.stumbleUntil) continue;
    const d=dist(p,ball);
    const range = (ball.intended===p)? 30 : 15;
    const spdOk = ball.intended===p ? true : Math.hypot(ball.vx,ball.vy)<300;
    if(d<range && spdOk && d<bestD){ bestD=d; bestP=p; }
  }
  if(bestP){
    ball.owner=bestP; ball.vx=0; ball.vy=0; ball.intended=null; ball.lofted=0;
  }
}

function tryGKSave(gk, close){
  if(!gk) return;
  const d=dist(gk,ball);
  const spd=Math.hypot(ball.vx,ball.vy);
  let chance = clamp(1 - d/95, 0, 0.86) * (spd>620?0.7:1);
  if(gk===activePlayer() && keys.has('KeyD')) chance=Math.min(1,chance+0.35);
  if(Math.random()<chance){
    ball.vx = -ball.vx*0.9 + (gk.team==='B'?1:-1)*180;
    ball.vy = (Math.random()-0.5)*380;
    flashBanner('SAVE!','#2ea8ff', gk.team==='B'?'#2ea8ff':'#ff4757');
  }
}

let bannerT=0;
function flashBanner(big,sub,color){
  const el=document.getElementById('banner');
  const b=document.getElementById('banner-big');
  const s=document.getElementById('banner-sub');
  b.textContent=big; b.style.color=color||'#ffd400'; s.textContent=sub||'';
  el.style.opacity='1'; el.style.transform='translate(-50%,-50%) scale(1.08)';
  bannerT=now()+1.1;
}

function scoreGoal(team){
  score[team]++;
  updateScoreHUD();
  flashBanner('GOAL!!', (team==='B'?'BLUE':'RED')+' SCORES', team==='B'?'#2ea8ff':'#ff4757');
  freezeUntil=now()+1.6;
  const keepScore={...score};
  resetKickoff();
  score=keepScore;
}

function updateScoreHUD(){
  document.getElementById('score').textContent = score.B+' : '+score.R;
}

// ── render ──
function drawPitch(){
  ctx.fillStyle='#0b3d1f';
  ctx.fillRect(0,0,W,H);
  for(let i=0;i<10;i++){
    ctx.fillStyle= i%2===0? 'rgba(255,255,255,.025)':'rgba(0,0,0,.03)';
    ctx.fillRect(H0 + i*(H1-H0)/10, V0, (H1-H0)/10, V1-V0);
  }
  ctx.strokeStyle='rgba(255,255,255,.55)'; ctx.lineWidth=2.4;
  ctx.strokeRect(H0,V0,H1-H0,V1-V0);
  ctx.beginPath(); ctx.moveTo(W/2,V0); ctx.lineTo(W/2,V1); ctx.stroke();
  ctx.beginPath(); ctx.arc(W/2,H/2,58,0,Math.PI*2); ctx.stroke();
  ctx.beginPath(); ctx.arc(W/2,H/2,3,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();
  // penalty boxes
  ctx.strokeRect(H0, GY0-46, 128, (GY1-GY0)+92);
  ctx.strokeRect(H1-128, GY0-46, 128, (GY1-GY0)+92);
  ctx.strokeRect(H0, GY0-14, 46, (GY1-GY0)+28);
  ctx.strokeRect(H1-46, GY0-14, 46, (GY1-GY0)+28);
  // goals
  ctx.fillStyle='rgba(255,255,255,.9)';
  ctx.fillRect(H0-6,GY0,6,GY1-GY0);
  ctx.fillRect(H1,GY0,6,GY1-GY0);
}

function drawPlayer(p, isActive){
  ctx.beginPath();
  ctx.arc(p.x,p.y+3,10,0,Math.PI*2);
  ctx.fillStyle='rgba(0,0,0,.28)'; ctx.fill();

  const col = p.isGK ? '#ffd400' : (p.team==='B'?'#2ea8ff':'#ff4757');
  ctx.beginPath();
  ctx.arc(p.x,p.y,10.5,0,Math.PI*2);
  ctx.fillStyle=col; ctx.fill();
  ctx.lineWidth=1.6; ctx.strokeStyle='rgba(0,0,0,.5)'; ctx.stroke();

  if(isActive){
    ctx.beginPath();
    ctx.arc(p.x,p.y,15,0,Math.PI*2);
    ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.stroke();
  }
  ctx.fillStyle='#04070a';
  ctx.font='800 9px Rajdhani, sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(p.num, p.x, p.y+0.5);

  if(p.shielding){
    ctx.beginPath(); ctx.arc(p.x,p.y,16,0,Math.PI*2);
    ctx.strokeStyle='rgba(11,220,107,.6)'; ctx.lineWidth=2; ctx.stroke();
  }
}

function drawBall(){
  const s = ball.lofted? 1.35:1;
  ctx.beginPath();
  ctx.ellipse(ball.x, ball.y+9, 7*s, 3.2*s, 0,0,Math.PI*2);
  ctx.fillStyle='rgba(0,0,0,.35)'; ctx.fill();
  ctx.beginPath();
  ctx.arc(ball.x,ball.y,6.2*s,0,Math.PI*2);
  ctx.fillStyle='#fff'; ctx.fill();
  ctx.lineWidth=1.2; ctx.strokeStyle='#333'; ctx.stroke();
}

function render(){
  drawPitch();
  for(const p of red) drawPlayer(p,false);
  for(const p of blue) drawPlayer(p, p===activePlayer());
  drawBall();
}

// ── loop ──
let lastT=null;
function loop(ts){
  requestAnimationFrame(loop);
  if(lastT===null) lastT=ts;
  let dt=(ts-lastT)/1000; lastT=ts;
  dt=Math.min(dt,0.05);

  if(gameState==='playing'){
    if(now()>=freezeUntil){
      humanStep(dt);
      for(const p of blue) if(p!==activePlayer()) aiStep(p,dt);
      for(const p of red) aiStep(p,dt);
      ballStep(dt);
      autoSwitch();

      if(ball.owner) possAcc[ball.owner.team==='B'?'b':'r'] += dt;
      const tot=possAcc.b+possAcc.r;
      if(tot>0.2){
        const pb=document.getElementById('poss-b'), pr=document.getElementById('poss-r');
        const pct=clamp(possAcc.b/tot*100,8,92);
        pb.style.width=pct+'%'; pr.style.width=(100-pct)+'%';
      }

      timeLeft-=dt;
      if(timeLeft<=0){ timeLeft=0; endMatch(); }
    }
    document.getElementById('timer').textContent = fmtTime(timeLeft);
    const stF=document.getElementById('stam-fill');
    stF.style.width = activePlayer().stamina+'%';

    if(chargingShot){
      const held=clamp(now()-chargeStart,0,0.9)/0.9;
      document.getElementById('power-wrap').style.display='block';
      document.getElementById('power-fill').style.width=(held*100)+'%';
    } else {
      document.getElementById('power-wrap').style.display='none';
    }
    if(bannerT && now()>bannerT){
      document.getElementById('banner').style.opacity='0';
      bannerT=0;
    }
  }
  render();
}

function fmtTime(s){
  s=Math.max(0,Math.ceil(s));
  const m=Math.floor(s/60), sec=s%60;
  return m+':'+(sec<10?'0':'')+sec;
}

function endMatch(){
  gameState='finished';
  const b=score.B, r=score.R;
  document.getElementById('result-score').textContent=b+' : '+r;
  const tagEl=document.getElementById('result-tag');
  let win=0;
  if(b>r){ tagEl.textContent='🎉 승리!'; tagEl.style.color='#0bdc6b'; win=1; }
  else if(b===r){ tagEl.textContent='🤝 무승부'; tagEl.style.color='#ffd400'; }
  else { tagEl.textContent='😢 패배'; tagEl.style.color='#ff4757'; }
  document.getElementById('endOverlay').style.display='flex';
  try{
    window.parent.postMessage({type:'soccer11_result', score:b, opp:r, win:win},'*');
  }catch(e){}
}

document.getElementById('startBtn').addEventListener('click',()=>{
  document.getElementById('startOverlay').style.display='none';
  fullReset();
});
document.getElementById('retryBtn').addEventListener('click',()=>{
  document.getElementById('endOverlay').style.display='none';
  fullReset();
});
document.getElementById('exitBtn').addEventListener('click',()=>{
  document.getElementById('endOverlay').style.display='none';
  document.getElementById('startOverlay').style.display='flex';
});
document.getElementById('kg-toggle').addEventListener('click',()=>{
  const kg=document.getElementById('keyguide');
  const hidden = kg.style.display==='none';
  kg.style.display = hidden? 'block':'none';
  document.getElementById('kg-toggle').textContent = hidden? '⌨ 키 숨기기':'⌨ 키 보기';
});

resetKickoff();
score={B:0,R:0}; timeLeft=MATCH_TIME; gameState='menu';
updateScoreHUD();
requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""


def render():
    import os as _os
    from utils.database import update_leaderboard, _get_col
    from utils.config import USERS_FILE

    st.markdown("<style>iframe{border:none!important;}</style>", unsafe_allow_html=True)
    st.caption("⚽ 방향키 이동 · A/S/D/W/Q/E/C 공수 전환 조작 · Shift+방향키 스킬무브 | 🏆 최고 득점 기록은 자동 저장됩니다")

    _cur_uid = st.session_state.get('logged_in_user', '')

    # ── declare_component 브리지로 게임 결과 수신 ──
    _bridge_dir = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'components', 'game_bridge')
    _bridge = st.components.v1.declare_component("game_bridge_soccer11", path=_bridge_dir)
    _result = _bridge(game_type="soccer11_result", key=f"bridge_soccer11_{_cur_uid}", default=None)

    if _result and isinstance(_result, dict) and _result.get('type') == 'soccer11_result':
        if not st.session_state.get('_soccer11_saved'):
            st.session_state['_soccer11_saved'] = True
            try:
                _s_score = int(_result.get('score', 0))
                _s_opp   = int(_result.get('opp', 0))
                _s_win   = int(_result.get('win', 0))
                if _cur_uid:
                    _col = _get_col(USERS_FILE)
                    _doc = _col.find_one({"_id": "main"}, {_cur_uid: 1})
                    if _doc and _cur_uid in _doc:
                        _udata = _doc[_cur_uid]
                        _upd = {
                            f"{_cur_uid}.game_records.soccer11.matches": _udata.get('game_records', {}).get('soccer11', {}).get('matches', 0) + 1,
                        }
                        if _s_win:
                            _upd[f"{_cur_uid}.game_records.soccer11.wins"] = _udata.get('game_records', {}).get('soccer11', {}).get('wins', 0) + 1
                        _col.update_one({"_id": "main"}, {"$set": _upd})
                        if _s_score > _udata.get('game_records', {}).get('soccer11', {}).get('score', 0):
                            _col.update_one({"_id": "main"}, {"$set": {
                                f"{_cur_uid}.game_records.soccer11.score": _s_score,
                            }})
                            update_leaderboard('soccer11', _udata.get('nickname', _cur_uid), _s_score)
                            st.toast(f"⚽ 한 경기 최다 득점 {_s_score}골 저장!", icon="🏆")
                            st.rerun()
            except Exception as _e:
                import logging; logging.error(f"[soccer11 save] {_e}")
    if not _result:
        st.session_state.pop('_soccer11_saved', None)

    components.html(GAME_HTML, height=900, scrolling=False)
