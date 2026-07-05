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
:root{--blue:#2ea8ff;--blueD:#0e5fa8;--red:#ff4757;--redD:#a8202c;--gold:#ffd400;--green:#0bdc6b;--bg:#03050a;--glass:rgba(255,255,255,.05);--border:rgba(255,255,255,.09);}
html,body{width:100%;height:940px;overflow:hidden;background:radial-gradient(ellipse at 50% 0%,#0a1420 0%,#03050a 70%);font-family:'Rajdhani',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:940px;overflow:hidden;}
canvas{position:absolute;top:126px;left:50%;transform:translateX(-50%);border-radius:16px;box-shadow:0 10px 50px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.06);}

/* ── HUD ── */
#hud{position:absolute;top:0;left:0;right:0;height:118px;z-index:100;background:linear-gradient(180deg,rgba(0,0,0,.92),rgba(0,0,0,.5));display:flex;align-items:center;justify-content:center;gap:30px;padding:0 10px;}
.hud-team{display:flex;flex-direction:column;align-items:center;min-width:96px;}
.hud-team-name{font-family:'Orbitron',sans-serif;font-size:11px;letter-spacing:2px;font-weight:900;}
.hud-team.b .hud-team-name{color:var(--blue);text-shadow:0 0 12px rgba(46,168,255,.6);}
.hud-team.r .hud-team-name{color:var(--red);text-shadow:0 0 12px rgba(255,71,87,.6);}
.hud-crest{width:26px;height:26px;border-radius:50%;margin-bottom:4px;display:flex;align-items:center;justify-content:center;font-size:13px;}
.hud-team.b .hud-crest{background:radial-gradient(circle at 35% 30%,#63c4ff,#0e5fa8);box-shadow:0 0 12px rgba(46,168,255,.55);}
.hud-team.r .hud-crest{background:radial-gradient(circle at 35% 30%,#ff8a94,#a8202c);box-shadow:0 0 12px rgba(255,71,87,.55);}
#score{font-family:'Black Han Sans',sans-serif;font-size:48px;letter-spacing:5px;text-shadow:0 0 20px rgba(255,255,255,.28);}
#center-info{display:flex;flex-direction:column;align-items:center;gap:5px;}
#timer{font-family:'Orbitron',sans-serif;font-size:23px;font-weight:900;color:var(--gold);letter-spacing:2px;text-shadow:0 0 10px rgba(255,212,0,.5);}
#poss-bar{width:160px;height:6px;border-radius:6px;overflow:hidden;background:rgba(255,255,255,.08);display:flex;box-shadow:inset 0 0 4px rgba(0,0,0,.5);}
#poss-b{background:linear-gradient(90deg,#0e5fa8,#2ea8ff);height:100%;transition:width .3s;}
#poss-r{background:linear-gradient(90deg,#ff4757,#a8202c);height:100%;transition:width .3s;}
#stam-wrap{position:absolute;top:128px;left:50%;transform:translateX(-368px);width:150px;z-index:100;}
#stam-lbl{font-size:9px;color:#8aa;letter-spacing:2px;margin-bottom:2px;}
#stam-bg{height:9px;border-radius:6px;background:rgba(255,255,255,.08);overflow:hidden;border:1px solid var(--border);}
#stam-fill{height:100%;background:linear-gradient(90deg,#0bdc6b,#ffd400,#ff4757);width:100%;transition:width .1s;}
#active-tag{position:absolute;top:128px;right:calc(50% - 368px);transform:translateX(368px);z-index:100;font-size:10px;color:#9fb0c0;letter-spacing:1.5px;background:rgba(0,0,0,.4);border:1px solid var(--border);border-radius:8px;padding:4px 10px;}
#active-tag b{color:var(--gold);}
#power-wrap{position:absolute;bottom:30px;left:50%;transform:translateX(-50%);width:280px;z-index:100;display:none;text-align:center;}
#power-lbl{font-size:10px;color:var(--gold);letter-spacing:3px;margin-bottom:3px;font-family:'Orbitron',sans-serif;}
#power-bg{height:13px;border-radius:8px;background:rgba(255,255,255,.08);overflow:hidden;border:1.5px solid rgba(255,212,0,.45);box-shadow:0 0 14px rgba(255,212,0,.15);}
#power-fill{height:100%;width:0%;background:linear-gradient(90deg,#0bdc6b,#ffd400,#ff4757);}

/* ── banners ── */
#banner{position:absolute;top:47%;left:50%;transform:translate(-50%,-50%);z-index:250;text-align:center;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s;}
#banner-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(42px,8vw,68px);color:var(--gold);text-shadow:0 0 34px rgba(255,212,0,.85),0 0 70px rgba(255,212,0,.45);letter-spacing:4px;}
#banner-sub{font-size:13px;color:#cde;letter-spacing:3px;margin-top:6px;}

/* ── key guide ── */
#keyguide{position:absolute;bottom:8px;left:8px;z-index:100;background:rgba(0,0,0,.6);border:1px solid var(--border);border-radius:10px;padding:9px 13px;font-size:10.5px;color:#9fb0c0;line-height:1.68;max-width:270px;backdrop-filter:blur(3px);}
#keyguide b{color:var(--gold);}
#keyguide .kg-title{color:#fff;font-weight:900;font-size:11px;letter-spacing:1px;margin-bottom:3px;}
#kg-toggle{position:absolute;bottom:8px;right:8px;z-index:101;background:rgba(0,0,0,.6);border:1px solid var(--border);color:#cde;border-radius:8px;padding:6px 12px;font-size:11px;cursor:pointer;}

/* ── overlays ── */
.overlay{position:absolute;inset:0;z-index:300;background:rgba(2,4,8,.95);display:flex;align-items:center;justify-content:center;backdrop-filter:blur(5px);}
.ov-box{width:min(580px,92vw);background:linear-gradient(160deg,#060c11,#0a1420);border:1px solid rgba(46,168,255,.25);border-radius:20px;padding:32px 28px;text-align:center;box-shadow:0 20px 60px rgba(0,0,0,.6);}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:32px;background:linear-gradient(90deg,var(--blue),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:2px;margin-bottom:6px;}
.ov-sub{color:#8aa;font-size:12px;margin-bottom:18px;letter-spacing:1px;}
.ov-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:left;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:12px;padding:15px 17px;margin-bottom:18px;font-size:11.5px;color:#aebccb;line-height:1.8;}
.ov-grid b{color:var(--gold);}
.ov-grid .grp{color:#fff;font-weight:900;font-size:11px;margin-top:6px;letter-spacing:1px;}
.ov-grid .grp:first-child{margin-top:0;}
#startBtn,#retryBtn,#exitBtn{font-family:'Orbitron',sans-serif;font-weight:900;letter-spacing:1px;border:none;border-radius:12px;padding:15px 0;width:100%;font-size:15px;cursor:pointer;margin-top:8px;transition:transform .12s;}
#startBtn:active,#retryBtn:active,#exitBtn:active{transform:scale(.97);}
#startBtn{background:linear-gradient(90deg,#0bdc6b,#2ea8ff);color:#05121a;box-shadow:0 8px 24px rgba(46,168,255,.3);}
#retryBtn{background:linear-gradient(90deg,#ffd400,#ff8c42);color:#221400;box-shadow:0 8px 24px rgba(255,140,66,.3);}
#exitBtn{background:rgba(255,255,255,.08);color:#cde;border:1px solid var(--border);}
#result-score{font-family:'Black Han Sans',sans-serif;font-size:56px;margin:10px 0;letter-spacing:5px;}
#result-tag{font-size:16px;font-weight:900;letter-spacing:3px;margin-bottom:16px;}
#result-stats{display:flex;justify-content:center;gap:22px;margin-bottom:6px;font-size:11px;color:#8aa;letter-spacing:1px;}
#result-stats b{color:#fff;font-size:13px;display:block;}
</style>
</head>
<body>
<div id="root">
  <div id="hud">
    <div class="hud-team b"><div class="hud-crest">B</div><div class="hud-team-name">BLUE (나)</div></div>
    <div id="score">0 : 0</div>
    <div class="hud-team r"><div class="hud-crest">R</div><div class="hud-team-name">RED (AI)</div></div>
  </div>
  <div id="center-info" style="position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:101;">
    <div id="timer">3:00</div>
    <div id="poss-bar"><div id="poss-b" style="width:50%;"></div><div id="poss-r" style="width:50%;"></div></div>
  </div>
  <div id="stam-wrap"><div id="stam-lbl">STAMINA</div><div id="stam-bg"><div id="stam-fill"></div></div></div>
  <div id="active-tag">조작 중: <b id="active-num">#—</b></div>
  <canvas id="pitch" width="900" height="580"></canvas>
  <div id="banner"><div id="banner-big"></div><div id="banner-sub"></div></div>
  <div id="power-wrap"><div id="power-lbl">SHOT POWER</div><div id="power-bg"><div id="power-fill"></div></div></div>

  <div id="keyguide">
    <div class="kg-title">⚽ 조작키</div>
    방향키 이동 &nbsp;|&nbsp; <b>E</b> 스프린트 &nbsp;|&nbsp; <b>Shift+방향</b> 스킬무브<br>
    <span style="color:#2ea8ff;">[공격]</span> <b>S</b>패스 <b>W</b>스루패스 <b>A</b>롱/크로스 <b>D</b>슛(홀드) <b>Q</b>선수호출 <b>C</b>볼보호<br>
    <span style="color:#ff4757;">[수비]</span> <b>D</b>스탠딩태클 <b>A</b>슬라이딩 <b>S</b>선수변경 <b>Q</b>압박 <b>C</b>조키<br>
    <span style="color:#ffd400;">[GK]</span> <b>A</b>멀리차기 <b>S</b>짧게던지기 <b>D</b>펀칭 <b>W</b>돌진
  </div>
  <div id="kg-toggle">⌨ 키 숨기기</div>

  <div class="overlay" id="startOverlay">
    <div class="ov-box">
      <div class="ov-title">⚽ ULTIMATE SOCCER 11</div>
      <div class="ov-sub">11 vs 11 실시간 축구 매치 · 3분 1경기 · 팀워크 AI</div>
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
      <div id="result-stats">
        <div>점유율<br><b id="rs-poss">50 : 50</b></div>
        <div>슈팅<br><b id="rs-shots">0</b></div>
        <div>태클성공<br><b id="rs-tackles">0</b></div>
      </div>
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
const ZOOM=1.5;
let camX=0, camY=0, camInit=false;
const GY0=232, GY1=348; // goal mouth
const GOAL_L_X=H0, GOAL_R_X=H1;
const MATCH_TIME=180;
const CX=(H0+H1)/2, CY=(V0+V1)/2;

function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function dist(a,b){return Math.hypot(a.x-b.x,a.y-b.y);}
function now(){return performance.now()/1000;}
function lerpTowards(cur,target,maxDelta){
  const d=target-cur;
  if(Math.abs(d)<=maxDelta) return target;
  return cur+Math.sign(d)*maxDelta;
}
function pointSegDist(px,py,x1,y1,x2,y2){
  const dx=x2-x1, dy=y2-y1;
  const len2=dx*dx+dy*dy;
  let t = len2>1e-6 ? ((px-x1)*dx+(py-y1)*dy)/len2 : 0;
  t=clamp(t,0,1);
  const cx=x1+t*dx, cy=y1+t*dy;
  return {d:Math.hypot(px-cx,py-cy), t, x:cx, y:cy};
}

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

let blue, red, players, ball, score, timeLeft, activeBlueIdx, gameState, freezeUntil;
let chargingShot=false, chargeStart=0;
let possAcc={b:0,r:0};
let stats={shots:0, tackles:0};
let particles=[], floatTexts=[];
let shakeT=0, flashT=0;

function resetKickoff(){
  blue=makeTeam('B'); red=makeTeam('R'); players=[...blue,...red];
  ball={x:CX,y:CY,vx:0,vy:0,owner:null,intended:null,dangerChecked:false,lofted:0,spin:0,trail:[]};
  activeBlueIdx=6;
  freezeUntil=now()+0.8;
  camInit=false;
}

function fullReset(){
  resetKickoff();
  score={B:0,R:0};
  timeLeft=MATCH_TIME;
  gameState='playing';
  possAcc={b:1,r:1};
  stats={shots:0, tackles:0};
  particles=[]; floatTexts=[];
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
  const mul = p.isGK?0.08 : (p.role==='DF'?0.65 : p.role==='FW'?1.25 : 1.0);
  const fx=clamp(p.baseFx + shift*mul,0.04,0.96);
  return {x:H0+fx*(H1-H0), y:V0+p.baseFy*(V1-V0)};
}

function steerTo(p,tx,ty,spd,dt){
  const dx=tx-p.x, dy=ty-p.y, d=Math.hypot(dx,dy)||1;
  const vx=dx/d*spd, vy=dy/d*spd;
  p.vx=lerpTowards(p.vx,vx,1400*dt);
  p.vy=lerpTowards(p.vy,vy,1400*dt);
  p.x+=p.vx*dt; p.y+=p.vy*dt;
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

function nearestOpponent(p){
  const opp=p.team==='B'?red:blue;
  let best=null,bd=1e9;
  for(const o of opp){ const d=dist(p,o); if(d<bd){bd=d;best=o;} }
  return best;
}
function nearestOpponentDist(p){
  const o=nearestOpponent(p);
  return o? dist(p,o) : 999;
}

// ── passing intelligence ──
function mates(team,exclude){ return (team==='B'?blue:red).filter(p=>p!==exclude && !p.isGK); }

function openness(passer,mate){
  const opp=passer.team==='B'?red:blue;
  let minD=1e9;
  for(const o of opp){
    if(o.isGK) continue;
    const r=pointSegDist(o.x,o.y,passer.x,passer.y,mate.x,mate.y);
    if(r.d<minD) minD=r.d;
  }
  return minD;
}
function spaceInFront(p,dir){
  const opp=p.team==='B'?red:blue;
  let minD=1e9;
  for(const o of opp){ const d=Math.hypot((p.x+dir*55)-o.x,p.y-o.y); if(d<minD) minD=d; }
  return minD;
}

function bestShortPassTarget(passer){
  let best=null,bestScore=-1e9;
  for(const m of mates(passer.team,passer)){
    const d=dist(passer,m);
    if(d>240) continue;
    const open=openness(passer,m);
    const fwd=(m.x-passer.x)*(passer.team==='B'?1:-1);
    const score = open*1.35 + fwd*0.28 - d*0.14;
    if(score>bestScore){bestScore=score;best=m;}
  }
  return best;
}
function bestThroughTarget(passer){
  const dir=passer.team==='B'?1:-1;
  let best=null,bestScore=-1e9;
  for(const m of mates(passer.team,passer)){
    const space=spaceInFront(m,dir);
    const fwd=(m.x-passer.x)*dir;
    const roleBonus = m.role==='FW'?26:(m.role==='MF'?10:0);
    const score = space*1.15 + fwd*0.5 + roleBonus;
    if(score>bestScore){bestScore=score;best=m;}
  }
  return best;
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

function addFloat(x,y,text,color){
  floatTexts.push({x,y,text,color,born:now()});
}
function burst(x,y,color,n,spread){
  spread=spread||220;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2, sp=40+Math.random()*spread;
    particles.push({x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,life:0.5+Math.random()*0.4,age:0,color,size:2+Math.random()*2.4});
  }
}

function doShortPass(passer){
  const t=bestShortPassTarget(passer)||pickNearMate(passer);
  kickTo(t.x,t.y,290,false);
  ball.intended=t;
  addFloat(passer.x,passer.y-22,'PASS','#2ea8ff');
}
function doThroughPass(passer){
  const t=bestThroughTarget(passer)||pickNearMate(passer);
  const dir=passer.team==='B'?1:-1;
  kickTo(t.x+dir*72, t.y, 360, false);
  t.runUntil=now()+1.3;
  ball.intended=t;
  addFloat(passer.x,passer.y-22,'THROUGH!','#ffd400');
}
function doLongOrCross(passer){
  const nearByline = passer.team==='B' ? passer.x>H1-220 : passer.x<H0+220;
  if(nearByline){
    const bx = passer.team==='B'? H1-30 : H0+30;
    const by = 290 + (Math.random()*70-35);
    kickTo(bx,by,390,true);
    addFloat(passer.x,passer.y-22,'CROSS!','#ff8c42');
  } else {
    const t=bestThroughTarget(passer)||pickNearMate(passer);
    kickTo(t.x,t.y,390,true);
    addFloat(passer.x,passer.y-22,'LONG BALL','#ff8c42');
  }
  ball.intended=null;
}
function doShoot(passer,power){
  const goalX = passer.team==='B'? GOAL_R_X : GOAL_L_X;
  const off=(passer.facing.y||0)*36 + (Math.random()*18-9);
  const aimY = clamp(290+off, GY0+10, GY1-10);
  const dx=goalX-passer.x, dy=aimY-passer.y, d=Math.hypot(dx,dy)||1;
  const spd=470+power*350;
  ball.vx=dx/d*spd; ball.vy=dy/d*spd;
  ball.owner=null; ball.shotBy=passer; ball.dangerChecked=false; ball.lofted=0;
  if(passer.team==='B') stats.shots++;
  addFloat(passer.x,passer.y-24, power>0.75?'강슛!!':'슈팅!', '#ff4757');
}
function doCallRun(passer){
  const t=bestThroughTarget(passer)||pickNearMate(passer);
  t.runUntil=now()+1.4;
  addFloat(passer.x,passer.y-22,'CALL!','#0bdc6b');
}
function doGKLongKick(gk){
  const t=bestThroughTarget(gk)||pickNearMate(gk);
  kickTo(t.x,t.y,440,true);
  addFloat(gk.x,gk.y-22,'GK KICK','#ffd400');
}
function doGKShortThrow(gk){
  const t=pickNearMate(gk);
  kickTo(t.x,t.y,250,false);
  addFloat(gk.x,gk.y-22,'THROW','#ffd400');
}
function doGKPunch(gk){
  ball.vx = -ball.vx*1.1 + (gk.team==='B'?220:-220);
  ball.vy = (Math.random()-0.5)*420;
  ball.owner=null; ball.dangerChecked=true;
  addFloat(gk.x,gk.y-22,'PUNCH!','#ffd400');
  burst(ball.x,ball.y,'#ffd400',10,180);
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
      addFloat(defender.x,defender.y-22,'TACKLE!','#0bdc6b');
      if(defender.team==='B') stats.tackles++;
      burst(defender.x,defender.y,'#c9a36a',7,120);
    } else {
      defender.stumbleUntil=now()+0.25;
      addFloat(defender.x,defender.y-22,'MISS','#8899aa');
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
    const dx=carrier.x-defender.x, dy=carrier.y-defender.y, dl=Math.hypot(dx,dy)||1;
    defender.vx=dx/dl*330; defender.vy=dy/dl*330;
    if(Math.random()<chance){
      ball.owner=defender; ball.vx=0; ball.vy=0; ball.intended=null;
      defender.stumbleUntil=now()+0.3;
      addFloat(defender.x,defender.y-22,'SLIDE TACKLE!','#0bdc6b');
      if(defender.team==='B') stats.tackles++;
    } else {
      addFloat(defender.x,defender.y-22,'MISS!','#8899aa');
    }
    burst(defender.x,defender.y,'#c9a36a',9,150);
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
        p.vx += bx*230; p.vy += by*230;
        addFloat(p.x,p.y-22,'SKILL!','#c04fff');
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
let autoSwitchCooldown=0;
function switchPlayer(){
  if(now()<switchLockUntil) return;
  const cur=activePlayer();
  let cands=blue.filter(p=>p!==cur).sort((a,b)=>dist(a,ball)-dist(b,ball));
  if(cands.length){
    activeBlueIdx = blue.indexOf(cands[0]);
    switchLockUntil=now()+0.25;
    autoSwitchCooldown=now()+0.5;
  }
}
function autoSwitch(){
  if(now()<switchLockUntil || now()<autoSwitchCooldown) return;
  if(ball.owner && ball.owner.team==='B') return;
  const cur=activePlayer();
  const near = nearestOnTeamToBall('B', true, null);
  if(near && near!==cur && dist(near,ball) < dist(cur,ball)-34){
    activeBlueIdx=blue.indexOf(near);
    autoSwitchCooldown=now()+0.45;
  }
}

// ── AI ──
function aiCarrierDecision(p,dt){
  const dir=p.team==='B'?1:-1;
  const goalX=p.team==='B'?GOAL_R_X:GOAL_L_X;
  const distGoal=Math.abs(goalX-p.x);
  const pressure=nearestOpponentDist(p);

  if(distGoal<200 && pressure>26 && Math.random()<0.022){
    doShoot(p, 0.5+Math.random()*0.45);
    if(p.team==='R') stats.shots=stats.shots; // no-op, red shots not tracked in stat card
    return;
  }
  if(pressure<34){
    const t=bestShortPassTarget(p);
    if(t && Math.random()<0.6){ kickTo(t.x,t.y,300,false); ball.intended=t; return; }
  }
  if(Math.random()<0.007){
    const t=bestThroughTarget(p);
    if(t){ kickTo(t.x+dir*60,t.y,350,false); ball.intended=t; t.runUntil=now()+1.2; return; }
  }
  const opp=nearestOpponent(p);
  let jx=0,jy=0;
  if(opp){
    const ax=p.x-opp.x, ay=p.y-opp.y, al=Math.hypot(ax,ay)||1;
    jx=ax/al; jy=ay/al;
  }
  const tx=p.x+dir*36 + jx*14;
  const ty=clamp(p.y+jy*14, V0+24, V1-24);
  steerTo(p,tx,ty,(p.isGK?0:112),dt);
}

function isNearestInterceptor(p, laneD){
  const arr=p.team==='B'?blue:red;
  for(const q of arr){
    if(q===p || q.isGK) continue;
    if(q===activePlayer()) continue;
    const r=pointSegDist(q.x,q.y, ball.x,ball.y, ball.intended.x,ball.intended.y);
    if(r.t>0.08 && r.t<0.96 && r.d<laneD) return false;
  }
  return true;
}

function aiStep(p,dt){
  const t=now();
  if(p===activePlayer()) return;
  if(t<p.stumbleUntil){ p.x+=p.vx*0.9*dt; p.y+=p.vy*0.9*dt; clampP(p); return; }

  if(ball.owner===p){
    if(p.isGK){
      if(Math.random()<0.03) doGKLongKick(p);
      return;
    }
    aiCarrierDecision(p,dt);
    ball.x=p.x+p.facing.x*13; ball.y=p.y+p.facing.y*13;
    clampP(p);
    return;
  }

  // 패스 경로 차단(인터셉트) 시도
  if(ball.intended && !ball.owner && ball.intended.team!==p.team && !p.isGK){
    const r=pointSegDist(p.x,p.y, ball.x,ball.y, ball.intended.x,ball.intended.y);
    if(r.t>0.08 && r.t<0.96 && r.d<74 && isNearestInterceptor(p,r.d)){
      steerTo(p, r.x, r.y, 168, dt);
      clampP(p);
      return;
    }
  }

  let tx,ty,spd=108;
  if(p.isGK){
    tx = p.team==='B'? H0+22 : H1-22;
    ty = clamp(ball.y, GY0+16, GY1-16);
    spd=94;
    if(inOwnBox(p,p.team) && ball.owner && ball.owner.team!==p.team && dist(p,ball)<130) spd=112;
  } else if(p.runUntil>t){
    const dir=p.team==='B'?1:-1;
    tx=p.x+dir*36; ty=p.y; spd=156;
  } else if(p.pressUntil>t){
    tx=ball.x; ty=ball.y; spd=146;
  } else if(!ball.owner && nearestOnTeamToBall(p.team,true,activePlayer())===p){
    tx=ball.x; ty=ball.y; spd=138;
  } else if(ball.owner && ball.owner.team!==p.team && designatedChaser(p.team)===p){
    tx=ball.owner.x; ty=ball.owner.y; spd=144;
    if(dist(p,ball.owner)<22 && Math.random()<0.035) attemptStandingTackle(p);
  } else {
    const s=slotPos(p); tx=s.x; ty=s.y; spd=105;
  }
  steerTo(p,tx,ty,spd,dt);
  clampP(p);
}

// ── main player (human) movement ──
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

  let spd=118;
  const sprinting = keys.has('KeyE') && p.stamina>2;
  if(sprinting){ spd*=1.38; p.stamina=clamp(p.stamina-32*dt,0,100); }
  else { p.stamina=clamp(p.stamina+24*dt,0,100); }
  if(p.shielding||p.jockeying) spd*=0.62;
  if(p.isGK){
    spd*=0.86;
    if(p.rushBoost) spd*=1.4;
  }

  const dvx=mx*spd, dvy=my*spd;
  p.vx=lerpTowards(p.vx,dvx,1500*dt);
  p.vy=lerpTowards(p.vy,dvy,1500*dt);
  p.x+=p.vx*dt; p.y+=p.vy*dt;

  if(p.isGK && !p.rushBoost){
    p.x=clamp(p.x, H0-2, H0+170);
    if(p.team==='R') p.x=clamp(p.x, H1-170, H1+2);
  } else {
    clampP(p);
  }

  if(ball.owner===p){
    const fx=p.facing.x||1, fy=p.facing.y||0;
    ball.x = lerpTowards(ball.x, p.x+fx*15, 900*dt);
    ball.y = lerpTowards(ball.y, p.y+fy*15, 900*dt);
  }
}

// ── ball physics & goal check ──
function ballStep(dt){
  ball.trail.push({x:ball.x,y:ball.y});
  if(ball.trail.length>6) ball.trail.shift();

  if(ball.owner) return;
  const spd0=Math.hypot(ball.vx,ball.vy);
  ball.spin += spd0*dt*0.05;
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

  if(!ball.dangerChecked){
    if(ball.x<H0+110 && ball.vx<0){
      ball.dangerChecked=true;
      tryGKSave(blue.find(p=>p.isGK), true);
    } else if(ball.x>H1-110 && ball.vx>0){
      ball.dangerChecked=true;
      tryGKSave(red.find(p=>p.isGK), true);
    }
  }

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

function tryGKSave(gk){
  if(!gk) return;
  const d=dist(gk,ball);
  const spd=Math.hypot(ball.vx,ball.vy);
  let chance = clamp(1 - d/95, 0, 0.86) * (spd>620?0.7:1);
  if(gk===activePlayer() && keys.has('KeyD')) chance=Math.min(1,chance+0.35);
  if(Math.random()<chance){
    ball.vx = -ball.vx*0.9 + (gk.team==='B'?1:-1)*180;
    ball.vy = (Math.random()-0.5)*380;
    flashBanner('SAVE!', gk.team==='B'?'BLUE GK':'RED GK', gk.team==='B'?'#2ea8ff':'#ff4757');
    burst(ball.x,ball.y,'#ffffff',10,200);
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
  freezeUntil=now()+1.7;
  shakeT=now()+0.5;
  flashT=now()+0.35;
  burst(team==='B'?GOAL_R_X-14:GOAL_L_X+14, (GY0+GY1)/2, team==='B'?'#2ea8ff':'#ff4757', 26, 260);
  burst(team==='B'?GOAL_R_X-14:GOAL_L_X+14, (GY0+GY1)/2, '#ffd400', 14, 220);
  const keepScore={...score};
  resetKickoff();
  score=keepScore;
}

function updateScoreHUD(){
  document.getElementById('score').textContent = score.B+' : '+score.R;
}

// ── render ──
function updateCamera(dt){
  const p=activePlayer();
  const halfW=(W/ZOOM)/2, halfH=(H/ZOOM)/2;
  const targetX = clamp(ball.x*0.68 + p.x*0.32, H0+halfW, H1-halfW);
  const targetY = clamp(ball.y*0.55 + p.y*0.45, V0+halfH, V1-halfH);
  if(!camInit){ camX=targetX; camY=targetY; camInit=true; return; }
  const k=Math.min(1, dt*4.2);
  camX += (targetX-camX)*k;
  camY += (targetY-camY)*k;
}

function drawMinimap(){
  const mx=W-166, my=14, mw=156, mh=84;
  ctx.save();
  ctx.fillStyle='rgba(0,0,0,.5)';
  ctx.fillRect(mx-5,my-5,mw+10,mh+10);
  ctx.strokeStyle='rgba(255,255,255,.55)'; ctx.lineWidth=1;
  ctx.strokeRect(mx,my,mw,mh);
  ctx.beginPath(); ctx.moveTo(mx+mw/2,my); ctx.lineTo(mx+mw/2,my+mh); ctx.stroke();

  const sx=mw/(H1-H0), sy=mh/(V1-V0);
  function proj(x,y){ return {x:mx+(x-H0)*sx, y:my+(y-V0)*sy}; }

  for(const p of red){ const q=proj(p.x,p.y); ctx.beginPath(); ctx.arc(q.x,q.y,1.7,0,Math.PI*2); ctx.fillStyle='#ff4757'; ctx.fill(); }
  for(const p of blue){ const q=proj(p.x,p.y); ctx.beginPath(); ctx.arc(q.x,q.y,1.7,0,Math.PI*2); ctx.fillStyle=(p===activePlayer())?'#ffd400':'#2ea8ff'; ctx.fill(); }
  const bq=proj(ball.x,ball.y);
  ctx.beginPath(); ctx.arc(bq.x,bq.y,1.9,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();

  const halfW=(W/ZOOM)/2, halfH=(H/ZOOM)/2;
  const vp1=proj(camX-halfW,camY-halfH), vp2=proj(camX+halfW,camY+halfH);
  ctx.strokeStyle='rgba(255,255,255,.7)'; ctx.lineWidth=1;
  ctx.strokeRect(vp1.x,vp1.y,vp2.x-vp1.x,vp2.y-vp1.y);
  ctx.restore();
}

function drawPitch(){
  const bgGrad=ctx.createRadialGradient(W/2,H*0.15,60,W/2,H/2,W*0.75);
  bgGrad.addColorStop(0,'#12351f');
  bgGrad.addColorStop(1,'#061e10');
  ctx.fillStyle=bgGrad;
  ctx.fillRect(0,0,W,H);

  for(let i=0;i<10;i++){
    ctx.fillStyle= i%2===0? 'rgba(255,255,255,.03)':'rgba(0,0,0,.035)';
    ctx.fillRect(H0 + i*(H1-H0)/10, V0, (H1-H0)/10, V1-V0);
  }

  ctx.save();
  ctx.strokeStyle='rgba(255,255,255,.14)'; ctx.lineWidth=5;
  ctx.strokeRect(H0,V0,H1-H0,V1-V0);
  ctx.strokeStyle='rgba(255,255,255,.62)'; ctx.lineWidth=2.2;
  ctx.strokeRect(H0,V0,H1-H0,V1-V0);
  ctx.beginPath(); ctx.moveTo(W/2,V0); ctx.lineTo(W/2,V1); ctx.stroke();
  ctx.beginPath(); ctx.arc(CX,CY,58,0,Math.PI*2); ctx.stroke();
  ctx.beginPath(); ctx.arc(CX,CY,3,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();

  ctx.strokeRect(H0, GY0-46, 128, (GY1-GY0)+92);
  ctx.strokeRect(H1-128, GY0-46, 128, (GY1-GY0)+92);
  ctx.strokeRect(H0, GY0-14, 46, (GY1-GY0)+28);
  ctx.strokeRect(H1-46, GY0-14, 46, (GY1-GY0)+28);
  ctx.beginPath(); ctx.arc(H0+94,CY,3,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();
  ctx.beginPath(); ctx.arc(H1-94,CY,3,0,Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();
  ctx.beginPath(); ctx.arc(H0+94,CY,50,-0.6,0.6); ctx.stroke();
  ctx.beginPath(); ctx.arc(H1-94,CY,50,Math.PI-0.6,Math.PI+0.6); ctx.stroke();

  ctx.beginPath(); ctx.arc(H0,V0,10,0,Math.PI/2); ctx.stroke();
  ctx.beginPath(); ctx.arc(H1,V0,10,Math.PI/2,Math.PI); ctx.stroke();
  ctx.beginPath(); ctx.arc(H0,V1,10,-Math.PI/2,0); ctx.stroke();
  ctx.beginPath(); ctx.arc(H1,V1,10,Math.PI,Math.PI*1.5); ctx.stroke();
  ctx.restore();

  drawGoalNet(H0-14, GY0, 14, GY1-GY0, -1);
  drawGoalNet(H1, GY0, 14, GY1-GY0, 1);
  ctx.fillStyle='rgba(255,255,255,.95)';
  ctx.fillRect(H0-3,GY0-3,3,GY1-GY0+6);
  ctx.fillRect(H1,GY0-3,3,GY1-GY0+6);
  ctx.fillRect(H0-3,GY0-3,6,3);
  ctx.fillRect(H0-3,GY1,6,3);
  ctx.fillRect(H1-3,GY0-3,6,3);
  ctx.fillRect(H1-3,GY1,6,3);
}

function drawGoalNet(x,y,w,h,dir){
  ctx.save();
  ctx.strokeStyle='rgba(255,255,255,.28)'; ctx.lineWidth=1;
  const step=8;
  for(let i=0;i<=w;i+=step){
    ctx.beginPath(); ctx.moveTo(x+i,y); ctx.lineTo(x+i,y+h); ctx.stroke();
  }
  for(let j=0;j<=h;j+=step){
    ctx.beginPath(); ctx.moveTo(x,y+j); ctx.lineTo(x+w,y+j); ctx.stroke();
  }
  ctx.restore();
}

function drawPlayer(p, isActive){
  ctx.beginPath();
  ctx.ellipse(p.x,p.y+9,10,4,0,0,Math.PI*2);
  ctx.fillStyle='rgba(0,0,0,.32)'; ctx.fill();

  const base = p.isGK ? '#ffd400' : (p.team==='B'?'#2ea8ff':'#ff4757');
  const dark = p.isGK ? '#a88400' : (p.team==='B'?'#0e5fa8':'#a8202c');
  const grad=ctx.createRadialGradient(p.x-3,p.y-4,1,p.x,p.y,12);
  grad.addColorStop(0, isActive? '#ffffff': base);
  grad.addColorStop(0.55, base);
  grad.addColorStop(1, dark);

  ctx.beginPath();
  ctx.arc(p.x,p.y,10.5,0,Math.PI*2);
  ctx.fillStyle=grad; ctx.fill();
  ctx.lineWidth=1.4; ctx.strokeStyle='rgba(0,0,0,.55)'; ctx.stroke();

  if(p.facing){
    const fx=p.x+p.facing.x*13, fy=p.y+p.facing.y*13;
    ctx.beginPath();
    ctx.arc(fx,fy,2.6,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,255,.85)'; ctx.fill();
  }

  if(isActive){
    const pulse = 14.5 + Math.sin(now()*7)*1.6;
    ctx.beginPath();
    ctx.arc(p.x,p.y,pulse,0,Math.PI*2);
    ctx.strokeStyle='#fff'; ctx.lineWidth=2.2; ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(p.x-5,p.y-19); ctx.lineTo(p.x+5,p.y-19); ctx.lineTo(p.x,p.y-12);
    ctx.fillStyle='#ffd400'; ctx.fill();
  }

  ctx.fillStyle='#04070a';
  ctx.font='800 9px Rajdhani, sans-serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(p.num, p.x, p.y+0.5);

  if(p.shielding){
    ctx.beginPath(); ctx.arc(p.x,p.y,16,0,Math.PI*2);
    ctx.strokeStyle='rgba(11,220,107,.6)'; ctx.lineWidth=2; ctx.stroke();
  }
  if(p===activePlayer() && p.stamina<22){
    ctx.beginPath(); ctx.arc(p.x+11,p.y-11,3.2,0,Math.PI*2);
    ctx.fillStyle='#ff4757'; ctx.fill();
  }
}

function drawBall(){
  for(let i=0;i<ball.trail.length;i++){
    const tpt=ball.trail[i];
    const a=(i+1)/ball.trail.length*0.28;
    ctx.beginPath();
    ctx.arc(tpt.x,tpt.y,5,0,Math.PI*2);
    ctx.fillStyle=`rgba(255,255,255,${a})`; ctx.fill();
  }
  const s = ball.lofted? 1.35:1;
  ctx.beginPath();
  ctx.ellipse(ball.x, ball.y+9, 7*s, 3.2*s, 0,0,Math.PI*2);
  ctx.fillStyle='rgba(0,0,0,.35)'; ctx.fill();

  ctx.save();
  ctx.translate(ball.x,ball.y);
  ctx.rotate(ball.spin||0);
  const bg=ctx.createRadialGradient(-2,-2,1,0,0,6.4*s);
  bg.addColorStop(0,'#ffffff'); bg.addColorStop(1,'#c9ccd2');
  ctx.beginPath(); ctx.arc(0,0,6.2*s,0,Math.PI*2); ctx.fillStyle=bg; ctx.fill();
  ctx.lineWidth=1; ctx.strokeStyle='#333';
  ctx.beginPath(); ctx.arc(0,0,2.2*s,0,Math.PI*2); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(-6.2*s,0); ctx.lineTo(6.2*s,0); ctx.stroke();
  ctx.restore();
}

function drawParticles(dt){
  for(let i=particles.length-1;i>=0;i--){
    const pt=particles[i];
    pt.age+=dt;
    if(pt.age>pt.life){ particles.splice(i,1); continue; }
    pt.x+=pt.vx*dt; pt.y+=pt.vy*dt; pt.vy+=140*dt;
    const a=1-pt.age/pt.life;
    ctx.beginPath();
    ctx.arc(pt.x,pt.y,pt.size,0,Math.PI*2);
    ctx.fillStyle=hexA(pt.color,a);
    ctx.fill();
  }
}
function hexA(hex,a){
  const c=hex.replace('#','');
  const r=parseInt(c.substring(0,2),16), g=parseInt(c.substring(2,4),16), b=parseInt(c.substring(4,6),16);
  return `rgba(${r},${g},${b},${clamp(a,0,1)})`;
}
function drawFloatTexts(){
  for(let i=floatTexts.length-1;i>=0;i--){
    const ft=floatTexts[i];
    const age=now()-ft.born;
    if(age>0.75){ floatTexts.splice(i,1); continue; }
    const a=1-age/0.75;
    ctx.font='900 12px Orbitron, sans-serif';
    ctx.textAlign='center';
    ctx.fillStyle=hexA(ft.color,a);
    ctx.fillText(ft.text, ft.x, ft.y-age*26);
  }
}

function render(dt){
  updateCamera(dt);
  ctx.save();
  if(now()<shakeT){
    ctx.translate((Math.random()-0.5)*7,(Math.random()-0.5)*7);
  }
  ctx.translate(W/2,H/2);
  ctx.scale(ZOOM,ZOOM);
  ctx.translate(-camX,-camY);

  drawPitch();
  for(const p of red) drawPlayer(p,false);
  for(const p of blue) drawPlayer(p, p===activePlayer());
  drawBall();
  drawParticles(dt);
  drawFloatTexts();
  ctx.restore();

  const vig=ctx.createRadialGradient(W/2,H/2,H*0.3,W/2,H/2,H*0.8);
  vig.addColorStop(0,'rgba(0,0,0,0)');
  vig.addColorStop(1,'rgba(0,0,0,.4)');
  ctx.fillStyle=vig; ctx.fillRect(0,0,W,H);

  if(now()<flashT){
    ctx.fillStyle=`rgba(255,255,255,${clamp((flashT-now())/0.35,0,1)*0.5})`;
    ctx.fillRect(0,0,W,H);
  }

  drawMinimap();
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
    document.getElementById('stam-fill').style.width = activePlayer().stamina+'%';
    document.getElementById('active-num').textContent = '#'+activePlayer().num+(activePlayer().isGK?' (GK)':'');

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
  render(dt);
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
  const tot=possAcc.b+possAcc.r || 1;
  const pb=Math.round(possAcc.b/tot*100);
  document.getElementById('rs-poss').textContent = pb+' : '+(100-pb);
  document.getElementById('rs-shots').textContent = stats.shots;
  document.getElementById('rs-tackles').textContent = stats.tackles;
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

    components.html(GAME_HTML, height=940, scrolling=False)
