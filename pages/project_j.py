import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>얼티밋 사커 11</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;user-select:none;}
:root{--blue:#2ea8ff;--blueD:#0e5fa8;--red:#ff4757;--redD:#a8202c;--gold:#ffd400;--green:#0bdc6b;--bg:#03050a;--glass:rgba(255,255,255,.05);--border:rgba(255,255,255,.09);}
html,body{width:100%;height:900px;overflow:hidden;background:radial-gradient(ellipse at 50% 0%,#0a1420 0%,#03050a 70%);font-family:'Rajdhani',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:900px;overflow:hidden;}
#pitch3d-wrap{position:absolute;top:126px;left:50%;transform:translateX(-50%);width:1040px;height:660px;border-radius:16px;overflow:hidden;box-shadow:0 10px 50px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.06);background:#040a06;}
#pitch3d-wrap canvas{position:absolute;top:0;left:0;}
#overlay2d{pointer-events:none;}

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
#commentary{position:absolute;top:118px;left:50%;transform:translateX(-50%);z-index:100;font-size:11px;color:#cde;background:rgba(0,0,0,.5);border:1px solid var(--border);border-radius:8px;padding:4px 14px;max-width:420px;text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;opacity:0;transition:opacity .3s;}
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

/* ── meta screens (hub / difficulty / country / tables) ── */
.meta-title{font-family:'Black Han Sans',sans-serif;font-size:26px;background:linear-gradient(90deg,var(--blue),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:1.5px;margin-bottom:5px;}
.meta-sub{color:#8aa;font-size:11.5px;margin-bottom:16px;letter-spacing:.5px;line-height:1.5;}
.mode-grid{display:grid;grid-template-columns:1fr;gap:10px;margin-bottom:6px;}
.mode-btn{display:flex;align-items:center;gap:12px;text-align:left;background:rgba(255,255,255,.045);border:1px solid var(--border);border-radius:12px;padding:14px 16px;cursor:pointer;transition:transform .12s,border-color .12s;color:#fff;}
.mode-btn:hover{border-color:rgba(46,168,255,.5);transform:translateY(-1px);}
.mode-btn .mi{font-size:26px;}
.mode-btn .mt{font-weight:900;font-size:14.5px;letter-spacing:.5px;}
.mode-btn .md{font-size:11px;color:#8aa;margin-top:2px;}
.diff-grid,.country-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px;}
.country-grid{grid-template-columns:repeat(4,1fr);}
.opt-btn{background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:10px;padding:11px 6px;color:#dfe8f0;font-size:12px;font-weight:700;cursor:pointer;transition:border-color .12s,transform .12s;}
.opt-btn:hover{border-color:rgba(255,212,0,.55);transform:translateY(-1px);}
.opt-btn.sel{border-color:var(--gold);background:rgba(255,212,0,.12);box-shadow:0 0 10px rgba(255,212,0,.25);}
.opt-btn.swatch{padding:0;border-width:2px;}
.opt-btn.swatch.sel{border-color:#fff;box-shadow:0 0 0 2px var(--gold);}
.opt-btn b{display:block;font-size:14px;margin-bottom:2px;}
.meta-table{width:100%;border-collapse:collapse;margin-bottom:14px;font-size:11.5px;}
.meta-table th{color:#8aa;font-weight:700;font-size:10px;letter-spacing:.5px;padding:5px 4px;border-bottom:1px solid var(--border);text-align:center;}
.meta-table td{padding:6px 4px;text-align:center;border-bottom:1px solid rgba(255,255,255,.04);color:#dfe8f0;}
.meta-table td.tname{text-align:left;font-weight:700;}
.meta-table tr.me td{color:var(--gold);}
.fixture-box{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:12px;padding:12px 14px;margin-bottom:14px;font-size:12.5px;color:#cde;}
.fixture-box b{color:var(--gold);}
.continue-btn{font-family:'Orbitron',sans-serif;font-weight:900;letter-spacing:1px;border:none;border-radius:12px;padding:14px 0;width:100%;font-size:14.5px;cursor:pointer;margin-top:4px;background:linear-gradient(90deg,#0bdc6b,#2ea8ff);color:#05121a;}
.ghost-btn{font-family:'Rajdhani',sans-serif;font-weight:700;border:1px solid var(--border);background:rgba(255,255,255,.05);border-radius:10px;padding:9px 0;width:100%;font-size:12.5px;cursor:pointer;margin-top:8px;color:#aebccb;}
.mini-btn{display:inline-block;background:rgba(255,212,0,.14);border:1px solid rgba(255,212,0,.4);color:var(--gold);border-radius:6px;padding:3px 9px;font-size:10.5px;font-weight:800;cursor:pointer;white-space:nowrap;margin:1px;}
.mini-btn.disabled{opacity:0.3;pointer-events:none;}
.mini-btn:hover{background:rgba(255,212,0,.28);}
.trophy-emoji{font-size:56px;margin:6px 0;}
</style>
</head>
<body>
<div id="root">
  <div id="hud">
    <div class="hud-team b"><div class="hud-crest">B</div><div class="hud-team-name">BLUE (나)</div></div>
    <div id="score">0 : 0</div>
    <div class="hud-team r"><div class="hud-crest">R</div><div class="hud-team-name" id="hud-r-name">RED (AI)</div></div>
  </div>
  <div id="center-info" style="position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:101;">
    <div id="timer">3:00</div>
    <div id="poss-bar"><div id="poss-b" style="width:50%;"></div><div id="poss-r" style="width:50%;"></div></div>
    <div id="commentary"></div>
  </div>
  <div id="stam-wrap"><div id="stam-lbl">STAMINA</div><div id="stam-bg"><div id="stam-fill"></div></div></div>
  <div id="active-tag">조작 중: <b id="active-num">#—</b> · 전술 <b id="tactic-tag">균형</b> (T)</div>
  <div id="pitch3d-wrap">
    <canvas id="overlay2d" width="1040" height="660"></canvas>
  </div>
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
    <div class="ov-box" id="metaBox">
      <div id="metaBody"></div>
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
        <div>패스성공률<br><b id="rs-pass">0%</b></div>
      </div>
      <div style="font-size:10px;color:#ffd400;letter-spacing:1px;margin:8px 0 4px;">⭐ MAN OF THE MATCH</div>
      <div id="rs-mom" style="font-size:13px;color:#fff;font-weight:800;margin-bottom:10px;">—</div>
      <div style="font-size:9.5px;color:#8aa;letter-spacing:1px;margin-bottom:4px;">우리 팀 볼터치 히트맵</div>
      <canvas id="heatmapCanvas" width="180" height="110" style="border-radius:8px;display:block;margin:0 auto 12px;"></canvas>
      <button id="retryBtn">🔄 다시 하기</button>
      <button id="exitBtn">📋 종료</button>
    </div>
  </div>
</div>

<script>
(function(){
"use strict";
const octx = document.getElementById('overlay2d').getContext('2d');
let scene, camera, renderer;
const W=1040,H=660, H0=50,H1=1040, V0=30,V1=780;
let camX=0, camInit=false;
const GY0=316, GY1=494; // goal mouth
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
const FORMATIONS = {
  '4-4-2': { roles:['GK','DF','DF','DF','DF','MF','MF','MF','MF','FW','FW'],
    slots:[ {x:.06,y:.50},
      {x:.19,y:.16},{x:.17,y:.38},{x:.17,y:.62},{x:.19,y:.84},
      {x:.47,y:.20},{x:.43,y:.42},{x:.43,y:.58},{x:.47,y:.80},
      {x:.75,y:.40},{x:.75,y:.60} ] },
  '4-3-3': { roles:['GK','DF','DF','DF','DF','MF','MF','MF','FW','FW','FW'],
    slots:[ {x:.06,y:.50},
      {x:.19,y:.16},{x:.17,y:.38},{x:.17,y:.62},{x:.19,y:.84},
      {x:.44,y:.30},{x:.40,y:.50},{x:.44,y:.70},
      {x:.78,y:.20},{x:.80,y:.50},{x:.78,y:.80} ] }
};
const FORM = FORMATIONS['4-4-2'].slots; // 하위호환용 기본 참조

function genAttrs(role, ovr){
  const bias = { GK:{pace:-15,shoot:-30,pass:-5,tackle:-10,stam:0},
    DF:{pace:0,shoot:-15,pass:-5,tackle:15,stam:5},
    MF:{pace:0,shoot:-5,pass:15,tackle:0,stam:10},
    FW:{pace:8,shoot:15,pass:-5,tackle:-15,stam:-5} }[role];
  function rnd(base,spread){ return clamp(Math.round(base+(Math.random()*2-1)*spread), 28, 99); }
  return { pace:rnd(ovr+bias.pace,9), shoot:rnd(ovr+bias.shoot,9), pass:rnd(ovr+bias.pass,9),
            tackle:rnd(ovr+bias.tackle,9), stam:rnd(ovr+bias.stam,9) };
}

function makeTeam(team, ovr, formationName){
  ovr = ovr||72;
  const F = FORMATIONS[formationName||'4-4-2'] || FORMATIONS['4-4-2'];
  const arr=[];
  for(let i=0;i<11;i++){
    const f=F.slots[i];
    const role=F.roles[i];
    const fx = team==='B'? f.x : 1-f.x;
    const attrs=genAttrs(role, ovr);
    arr.push({
      id:team+i, team, num:i+1, role, isGK:role==='GK', baseFx:fx, baseFy:f.y,
      x:H0+fx*(H1-H0), y:V0+f.y*(V1-V0),
      vx:0, vy:0, facing:{x:team==='B'?1:-1,y:0},
      attrs, ovr, pname: NAME_POOL[Math.floor(Math.random()*NAME_POOL.length)],
      stamina:100, shielding:false, jockeying:false, aiState:'HOLD',
      runUntil:0, pressUntil:0, stumbleUntil:0, skillEvadeUntil:0,
      matchGoals:0, matchAssists:0, matchTackles:0
    });
  }
  return arr;
}
function paceMul(p){ return 0.78 + (p.attrs.pace/99)*0.5; }
function staminaMul(p){ return 0.6 + (p.attrs.stam/99)*0.8; }

function simScoreline(ovrA, ovrB){
  const expA = clamp(1.25 + (ovrA-ovrB)/16, 0.15, 4.2);
  const expB = clamp(1.25 + (ovrB-ovrA)/16, 0.15, 4.2);
  const ga = Math.max(0, Math.round(expA + (Math.random()-0.5)*1.7));
  const gb = Math.max(0, Math.round(expB + (Math.random()-0.5)*1.7));
  return [ga,gb];
}

let blue, red, players, ball, score, timeLeft, activeBlueIdx, gameState, freezeUntil;
let chargingShot=false, chargeStart=0;
let possAcc={b:0,r:0};
let stats={shots:0, tackles:0, passOk:0, passTry:0};
let particles=[], floatTexts=[];
let shakeT=0, flashT=0;
let userFormation='4-4-2';
let opponentOVR=72;
let tactic='balanced'; // 'attacking' | 'balanced' | 'defensive'
let touchLog=[];
let replayBuffer=[], goalReplay=null, replaySampleAcc=0;
let adaptCheckAt=0;

// ── 메타 레이어 (허브 / 친선전 / 월드컵 토너먼트 / 리그) ──
const SAVED_LEAGUE = __SAVED_LEAGUE_JSON__;
const SAVED_ACHIEVEMENTS = __SAVED_ACHIEVEMENTS_JSON__ || {};
let metaMode=null;          // null(hub) | 'friendly' | 'wc' | 'league'
let aiDifficulty=1.0;
let lastMatchScore={b:0,r:0};

const COUNTRIES=[
  {n:'🇰🇷 대한민국'},{n:'🇧🇷 브라질'},{n:'🇩🇪 독일'},{n:'🇫🇷 프랑스'},
  {n:'🇦🇷 아르헨티나'},{n:'🇪🇸 스페인'},{n:'🏴 잉글랜드'},{n:'🇵🇹 포르투갈'},
  {n:'🇳🇱 네덜란드'},{n:'🇯🇵 일본'},{n:'🇧🇪 벨기에'},{n:'🇭🇷 크로아티아'},
  {n:'🇮🇹 이탈리아'},{n:'🇺🇾 우루과이'},{n:'🇺🇸 미국'},{n:'🇲🇽 멕시코'}
];
const LEAGUE_CLUB_NAMES=['FC 라이온즈','유나이티드 드래곤즈','아틀레티코 팰컨즈','레알 타이거스','보루시아 울프스','인터 코브라스','스톰 레인저스'];

let wcState=null;
let leagueState = SAVED_LEAGUE && SAVED_LEAGUE.teams ? SAVED_LEAGUE : null;

function placeAtKickoff(arr, team){
  for(const p of arr){
    let x = H0+p.baseFx*(H1-H0);
    x = team==='B'? Math.min(x, CX-6) : Math.max(x, CX+6);
    p.x = x;
    p.y = V0+p.baseFy*(V1-V0);
    p.vx=0; p.vy=0; p.facing={x:team==='B'?1:-1,y:0};
    p.shielding=false; p.jockeying=false; p.aiState='HOLD';
    p.runUntil=0; p.pressUntil=0; p.stumbleUntil=0; p.skillEvadeUntil=0;
    p.stamina=100;
  }
}

function resetKickoff(){
  if(!blue || !blue.length) blue=makeTeam('B', 74, userFormation);
  if(!red || !red.length) red=makeTeam('R', opponentOVR, '4-4-2');
  placeAtKickoff(blue,'B'); placeAtKickoff(red,'R');
  players=[...blue,...red];
  ball={x:CX,y:CY,vx:0,vy:0,z:0,vz:0,owner:null,intended:null,dangerChecked:false,lofted:0,spin:0,trail:[],lastPasser:null,shotBy:null,assistCandidate:null};
  activeBlueIdx=6;
  freezeUntil=now()+0.8;
  camInit=false;
  markAssignAt=0; markAssignB={}; markAssignR={};
}

function fullReset(){
  blue = (blueRosterSource==='career' && typeof careerState!=='undefined' && careerState)
    ? makeTeamFromSquad(careerState.squad, 'B', userFormation, getLineupForFormation(userFormation))
    : makeTeam('B', 74, userFormation);
  red=makeTeam('R', opponentOVR, '4-4-2');
  resetKickoff();
  score={B:0,R:0};
  timeLeft=MATCH_TIME;
  gameState='playing';
  possAcc={b:1,r:1};
  stats={shots:0, tackles:0, passOk:0, passTry:0};
  particles=[]; floatTexts=[];
  touchLog=[];
  tactic='balanced';
  adaptCheckAt=now()+8;
  commentate('🎙️ 킥오프! 경기가 시작됩니다.');
}

const keys=new Set();
let shiftDown=false;

function activePlayer(){ return blue[activeBlueIdx]; }

function inOwnBox(p,team){
  if(team==='B') return p.x<H0+183 && p.y>GY0-92 && p.y<GY1+92;
  return p.x>H1-183 && p.y>GY0-92 && p.y<GY1+92;
}

function slotPos(p){
  const ballFx=clamp((ball.x-H0)/(H1-H0),0,1);
  let shift=(ballFx-0.5)*0.16;
  const mul = p.isGK?0.08 : (p.role==='DF'?0.65 : p.role==='FW'?1.25 : 1.0);
  let tacticShift = 0;
  if(p.team==='B' && !p.isGK){
    tacticShift = tactic==='attacking'? 0.05 : (tactic==='defensive'? -0.05 : 0);
  }
  const fx=clamp(p.baseFx + shift*mul + tacticShift,0.04,0.96);
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

const GRAVITY=520;
function kickTo(x,y,spd,lofted){
  const dx=x-ball.x, dy=y-ball.y, d=Math.hypot(dx,dy)||1;
  ball.vx=dx/d*spd; ball.vy=dy/d*spd;
  ball.owner=null; ball.lofted=lofted?1:0; ball.dangerChecked=false;
  ball.vz = lofted? (150+Math.min(d,500)*0.28) : 0;
  if(!lofted) ball.z=0;
}

function addFloat(x,y,text,color){
  floatTexts.push({x,y,text,color,born:now()});
}
let commentaryTimer=null;
function commentate(text){
  const el=document.getElementById('commentary');
  if(!el) return;
  el.textContent=text;
  el.style.opacity='1';
  if(commentaryTimer) clearTimeout(commentaryTimer);
  commentaryTimer=setTimeout(()=>{ el.style.opacity='0'; }, 3000);
}
function burst(x,y,color,n,spread){
  spread=spread||220;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2, sp=40+Math.random()*spread;
    particles.push({x,y,vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,life:0.5+Math.random()*0.4,age:0,color,size:2+Math.random()*2.4});
  }
}

function passInaccuracy(passer){ return (99-passer.attrs.pass)/99; }
function applyPassError(passer,x,y){
  const inacc=passInaccuracy(passer);
  return { x: x+(Math.random()*2-1)*46*inacc, y: y+(Math.random()*2-1)*46*inacc };
}
function isOffside(team, receiverX){
  const opp = team==='B'? red:blue;
  let lastLineX = team==='B'? -Infinity : Infinity;
  for(const o of opp){
    if(o.isGK) continue;
    if(team==='B'){ if(o.x>lastLineX) lastLineX=o.x; }
    else { if(o.x<lastLineX) lastLineX=o.x; }
  }
  return team==='B'? receiverX>lastLineX : receiverX<lastLineX;
}

function doShortPass(passer){
  const t=bestShortPassTarget(passer)||pickNearMate(passer);
  const pt=applyPassError(passer,t.x,t.y);
  kickTo(pt.x,pt.y,290,false);
  ball.intended=t; ball.lastPasser=passer;
  stats.passTry++; if(passer.team==='B' && Math.hypot(pt.x-t.x,pt.y-t.y)<12) stats.passOk++;
  addFloat(passer.x,passer.y-22,'PASS','#2ea8ff');
  if(passer===activePlayer()) autoSwitchCooldown=now()+0.55;
}
function doThroughPass(passer){
  const t=bestThroughTarget(passer)||pickNearMate(passer);
  const dir=passer.team==='B'?1:-1;
  const targetX=t.x+dir*72;
  if(isOffside(passer.team, targetX)){
    addFloat(t.x, t.y-26, 'OFFSIDE!', '#ff4757');
    commentate('🚩 오프사이드! 판정이 무효로 돌아갑니다.');
    const opp=nearestOpponent(passer);
    ball.owner = opp || null;
    ball.x=passer.x; ball.y=passer.y; ball.vx=0; ball.vy=0; ball.vz=0; ball.z=0;
    ball.intended=null; ball.lastPasser=null;
    return;
  }
  const pt=applyPassError(passer, targetX, t.y);
  kickTo(pt.x, pt.y, 360, false);
  t.runUntil=now()+1.3;
  ball.intended=t; ball.lastPasser=passer;
  stats.passTry++;
  addFloat(passer.x,passer.y-22,'THROUGH!','#ffd400');
  if(passer===activePlayer()) autoSwitchCooldown=now()+0.55;
}
function doLongOrCross(passer){
  const nearByline = passer.team==='B' ? passer.x>H1-268 : passer.x<H0+268;
  ball.lastPasser=passer;
  if(nearByline){
    const bx = passer.team==='B'? H1-30 : H0+30;
    const by = CY + (Math.random()*70-35);
    const pt=applyPassError(passer,bx,by);
    kickTo(pt.x,pt.y,390,true);
    addFloat(passer.x,passer.y-22,'CROSS!','#ff8c42');
  } else {
    const t=bestThroughTarget(passer)||pickNearMate(passer);
    const pt=applyPassError(passer,t.x,t.y);
    kickTo(pt.x,pt.y,390,true);
    addFloat(passer.x,passer.y-22,'LONG BALL','#ff8c42');
  }
  ball.intended=null;
  stats.passTry++;
  if(passer===activePlayer()) autoSwitchCooldown=now()+0.55;
}
function doShoot(passer,power){
  const goalX = passer.team==='B'? GOAL_R_X : GOAL_L_X;
  const shootMul = 0.84 + (passer.attrs.shoot/99)*0.32;
  const inaccuracy = (99-passer.attrs.shoot)/99;
  const off=(passer.facing.y||0)*36 + (Math.random()*18-9)*(1+inaccuracy*1.6);
  const aimY = clamp(CY+off, GY0+15, GY1-15);
  const dx=goalX-passer.x, dy=aimY-passer.y, d=Math.hypot(dx,dy)||1;
  const spd=(470+power*350)*shootMul;
  ball.vx=dx/d*spd; ball.vy=dy/d*spd; ball.vz=0; ball.z=0;
  ball.owner=null; ball.shotBy=passer; ball.dangerChecked=false; ball.lofted=0;
  ball.assistCandidate = (ball.lastPasser && ball.lastPasser!==passer && ball.lastPasser.team===passer.team) ? ball.lastPasser : null;
  if(passer.team==='B') stats.shots++;
  addFloat(passer.x,passer.y-24, power>0.75?'강슛!!':'슈팅!', '#ff4757');
  if(power>0.7) commentate(passer.team==='B'? '💥 강력한 슈팅을 시도합니다!' : '⚠️ 상대의 위협적인 슈팅!');
  if(passer===activePlayer()) autoSwitchCooldown=now()+0.55;
}
function doCallRun(passer){
  const t=bestThroughTarget(passer)||pickNearMate(passer);
  t.runUntil=now()+1.4;
  addFloat(passer.x,passer.y-22,'CALL!','#0bdc6b');
}
function doGKLongKick(gk){
  const t=bestThroughTarget(gk)||pickNearMate(gk);
  kickTo(t.x,t.y,440,true);
  ball.lastPasser=gk;
  addFloat(gk.x,gk.y-22,'GK KICK','#ffd400');
}
function doGKShortThrow(gk){
  const t=pickNearMate(gk);
  kickTo(t.x,t.y,250,false);
  ball.lastPasser=gk;
  addFloat(gk.x,gk.y-22,'THROW','#ffd400');
}
function doGKPunch(gk){
  ball.vx = -ball.vx*1.1 + (gk.team==='B'?220:-220);
  ball.vy = (Math.random()-0.5)*420;
  ball.owner=null; ball.dangerChecked=true; ball.lastPasser=null;
  addFloat(gk.x,gk.y-22,'PUNCH!','#ffd400');
  burst(ball.x,ball.y,'#ffd400',10,180);
}

function attemptStandingTackle(defender){
  const carrier=ball.owner;
  if(!carrier || carrier.team===defender.team) return;
  if(ball.z>16) return;
  const d=dist(defender,carrier);
  if(d<24){
    let chance=0.42 + (defender.attrs.tackle-70)/220;
    if(carrier.shielding) chance-=0.22;
    if(carrier.skillEvadeUntil>now()) chance-=0.3;
    if(Math.random()<chance){
      ball.owner=defender; ball.vx=0; ball.vy=0; ball.vz=0; ball.z=0; ball.intended=null; ball.lastPasser=null;
      addFloat(defender.x,defender.y-22,'TACKLE!','#0bdc6b');
      if(defender.team==='B') commentate('🛡️ 깔끔한 태클로 공을 따냅니다!');
      if(defender.team==='B') stats.tackles++;
      defender.matchTackles=(defender.matchTackles||0)+1;
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
  if(ball.z>16) return;
  const d=dist(defender,carrier);
  if(d<38){
    let chance=0.54 + (defender.attrs.tackle-70)/220;
    if(carrier.shielding) chance-=0.2;
    if(carrier.skillEvadeUntil>now()) chance-=0.35;
    defender.stumbleUntil=now()+0.55;
    const dx=carrier.x-defender.x, dy=carrier.y-defender.y, dl=Math.hypot(dx,dy)||1;
    defender.vx=dx/dl*330; defender.vy=dy/dl*330;
    if(Math.random()<chance){
      ball.owner=defender; ball.vx=0; ball.vy=0; ball.vz=0; ball.z=0; ball.intended=null; ball.lastPasser=null;
      defender.stumbleUntil=now()+0.3;
      addFloat(defender.x,defender.y-22,'SLIDE TACKLE!','#0bdc6b');
      if(defender.team==='B') commentate('🛡️ 과감한 슬라이딩 태클 성공!');
      if(defender.team==='B') stats.tackles++;
      defender.matchTackles=(defender.matchTackles||0)+1;
    } else {
      addFloat(defender.x,defender.y-22,'MISS!','#8899aa');
    }
    burst(defender.x,defender.y,'#c9a36a',9,150);
  }
}

// ══════════════════════════════════════════
// 메타 레이어: 허브 / 친선전 / 월드컵 / 리그
// ══════════════════════════════════════════
function shuffle(arr){
  const a=arr.slice();
  for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
function keyGuideHtml(){
  return `<div class="fixture-box" style="font-size:10.8px;line-height:1.7;">
    <b>조작키</b> — 방향키 이동 · <b style="color:#ffd400;">E</b>스프린트 · <b style="color:#ffd400;">Shift+방향</b>스킬무브<br>
    <span style="color:#2ea8ff;">공격</span> S패스 W스루패스 A롱/크로스 D슛(홀드) Q호출 C볼보호 &nbsp;
    <span style="color:#ff4757;">수비</span> D태클 A슬라이딩 S선수변경 Q압박 C조키 &nbsp;
    <span style="color:#0bdc6b;">경기중</span> <b style="color:#ffd400;">T</b>전술전환(공격/균형/수비)
  </div>`;
}
function showMeta(){ document.getElementById('startOverlay').style.display='flex'; }
function hideMeta(){ document.getElementById('startOverlay').style.display='none'; }
function setMetaBody(html){ document.getElementById('metaBody').innerHTML=html; }

function achievementsHtml(){
  const a=SAVED_ACHIEVEMENTS||{};
  return `<div class="fixture-box" style="font-size:10.8px;line-height:1.8;margin-top:10px;">
    <b style="color:var(--gold);">🏅 업적</b><br>
    🎩 해트트릭 ${a.hattrick||0}회 &nbsp; 🧤 클린시트 ${a.cleanSheet||0}회 &nbsp;
    🔥 대승(4골차+) ${a.bigWin||0}회 &nbsp; 📈 최다연승 ${a.winStreakMax||0}
  </div>`;
}
function renderHub(){
  metaMode=null;
  const leagueTag = leagueState ? `<div class="md">진행 중인 시즌 있음 · ${leagueState.matchday}/7 라운드</div>` : `<div class="md">8팀 리그 · 기록 자동 저장</div>`;
  setMetaBody(`
    <div class="meta-title">⚽ ULTIMATE SOCCER 11</div>
    <div class="meta-sub">모드를 선택해줘</div>
    <div class="mode-grid">
      <div class="mode-btn" data-action="go_friendly"><div class="mi">🤝</div><div><div class="mt">친선전</div><div class="md">난이도 선택 후 AI와 단판 매치</div></div></div>
      <div class="mode-btn" data-action="go_wc"><div class="mi">🏆</div><div><div class="mt">월드컵 토너먼트</div><div class="md">국가 선택 → 조별리그 → 결승</div></div></div>
      <div class="mode-btn" data-action="go_league"><div class="mi">📅</div><div><div class="mt">리그 모드</div><div class="md">8팀 풀리그 · ${leagueState?'이어서 진행':'새 시즌 시작'}</div></div></div>
      <div class="mode-btn" data-action="go_career"><div class="mi">🏟️</div><div><div class="mt">커리어 모드</div><div class="md">${careerState? careerState.crest+' '+careerState.clubName+' · 시즌 '+careerState.season : '구단 창단 · 이적시장 · 스쿼드 육성'}</div></div></div>
    </div>
    ${achievementsHtml()}
    ${keyGuideHtml()}
  `);
}

// ── 친선전 ──
function renderFriendlySetup(){
  metaMode='friendly';
  setMetaBody(`
    <div class="meta-title">🤝 친선전</div>
    <div class="meta-sub">포메이션과 난이도를 선택하면 바로 킥오프!</div>
    <div class="meta-sub" style="margin-bottom:6px;color:#fff;font-weight:800;">우리 팀 포메이션</div>
    <div class="diff-grid">
      <div class="opt-btn ${userFormation==='4-4-2'?'sel':''}" data-action="pick_formation" data-form="4-4-2"><b>4-4-2</b>균형형</div>
      <div class="opt-btn ${userFormation==='4-3-3'?'sel':''}" data-action="pick_formation" data-form="4-3-3"><b>4-3-3</b>공격형</div>
    </div>
    <div class="meta-sub" style="margin:10px 0 6px;color:#fff;font-weight:800;">난이도</div>
    <div class="diff-grid">
      <div class="opt-btn" data-action="friendly_pick" data-diff="0.82"><b>쉬움</b>여유롭게</div>
      <div class="opt-btn" data-action="friendly_pick" data-diff="1.0"><b>보통</b>표준</div>
      <div class="opt-btn" data-action="friendly_pick" data-diff="1.22"><b>어려움</b>빡세게</div>
    </div>
    <div class="ghost-btn" data-action="goto_hub">◀ 메인으로</div>
  `);
}
function pickFormation(f){
  userFormation = FORMATIONS[f]? f : '4-4-2';
  if(metaMode==='career') renderCareerHub();
  else renderFriendlySetup();
}
function startFriendly(diff){
  blueRosterSource=null;
  aiDifficulty=diff;
  opponentOVR = diff<0.9? 60 : (diff>1.1? 85 : 72);
  startRealMatch('RED (AI)');
}

// ── 월드컵 토너먼트 (16개국, 4개조 조별리그 → 8강 → 4강 → 결승) ──
function wcStart(country){
  metaMode='wc';
  const pool=shuffle(COUNTRIES.map(c=>c.n).filter(n=>n!==country));
  const myGroup=[country, ...pool.slice(0,3)];
  const otherGroups=[pool.slice(3,7), pool.slice(7,11), pool.slice(11,15)];
  const ovrMap={};
  [...myGroup, ...otherGroups.flat()].forEach(n=>{ if(n!==country) ovrMap[n]=Math.round(62+Math.random()*28); });
  wcState = {
    country, myGroup, otherGroups, opponents: myGroup.filter(n=>n!==country),
    opponentOVR: ovrMap, results:[], matchIdx:0, stage:'group',
    bracket:null, bracketRound:'', roundOpp:'', outcome:''
  };
  aiDifficulty=1.0;
  renderWcScreen();
}
function wcGroupStandingsFor(teams, matches){
  const table={}; teams.forEach(n=> table[n]={p:0,w:0,d:0,l:0,gf:0,ga:0,pts:0});
  function apply(a,b,ga,gb){
    if(!table[a]||!table[b]) return;
    table[a].p++; table[a].gf+=ga; table[a].ga+=gb;
    table[b].p++; table[b].gf+=gb; table[b].ga+=ga;
    if(ga>gb){ table[a].w++; table[a].pts+=3; table[b].l++; }
    else if(ga<gb){ table[b].w++; table[b].pts+=3; table[a].l++; }
    else { table[a].d++; table[b].d++; table[a].pts++; table[b].pts++; }
  }
  matches.forEach(m=> apply(m.a,m.b,m.ga,m.gb));
  const arr=Object.keys(table).map(n=>({name:n,...table[n]}));
  arr.sort((x,y)=> y.pts-x.pts || (y.gf-y.ga)-(x.gf-x.ga) || y.gf-x.gf);
  return arr;
}
function wcGroupStandings(){
  const matches = wcState.results.map(r=>({a:'나의 팀', b:r.opp, ga:r.gf, gb:r.ga}));
  if(wcState._simmed) matches.push(...wcState._simmed);
  const teams=['나의 팀', ...wcState.opponents];
  return wcGroupStandingsFor(teams, matches);
}
function wcSimRestOfGroup(){
  if(wcState._simmed) return;
  wcState._simmed=[];
  const opps=wcState.opponents;
  const pairs=[[opps[0],opps[1]],[opps[0],opps[2]],[opps[1],opps[2]]];
  for(const [a,b] of pairs){
    const [ga,gb]=simScoreline(wcState.opponentOVR[a]||70, wcState.opponentOVR[b]||70);
    wcState._simmed.push({a,b,ga,gb});
  }
}
function wcSimOtherGroups(){
  // 각 그룹(4팀) 풀리그 6경기 시뮬레이션 후 상위 2팀 반환
  return wcState.otherGroups.map(group=>{
    const matches=[];
    for(let i=0;i<group.length;i++) for(let j=i+1;j<group.length;j++){
      const [ga,gb]=simScoreline(wcState.opponentOVR[group[i]]||70, wcState.opponentOVR[group[j]]||70);
      matches.push({a:group[i],b:group[j],ga,gb});
    }
    const table=wcGroupStandingsFor(group, matches);
    return [table[0].name, table[1].name];
  });
}
function wcBuildBracket(){
  const myGroupTable=wcGroupStandings();
  const others=wcSimOtherGroups(); // [[g2w,g2r],[g3w,g3r],[g4w,g4r]]
  const myIdx=myGroupTable.findIndex(t=>t.name==='나의 팀');
  const myRank = myIdx; // 0=1위, 1=2위
  const myOpp = myRank===0? others[0][1] : others[0][0];
  // 남은 8강 2경기(내 경기 제외)는 즉시 시뮬레이션해서 승자만 기록
  const rest=[[others[1][0],others[2][1]],[others[2][0],others[1][1]]];
  const restResults=rest.map(([a,b])=>{
    const [ga,gb]=simScoreline(wcState.opponentOVR[a]||70, wcState.opponentOVR[b]||70);
    return ga>=gb? a:b;
  });
  wcState.bracket = { qfOpp: myOpp, qfWinners: restResults, stage:'QF' };
  wcState.roundOpp = myOpp;
}
function wcAdvanceBracket(iWon){
  const br=wcState.bracket;
  if(!iWon){ wcState.stage='out_knockout'; return; }
  if(br.stage==='QF'){
    // 4강: 나 + restResults(2팀) 중 하나 + 나머지 하나는 부전(이미 3팀뿐이므로 임의 매칭)
    const semiOpp = br.qfWinners[Math.floor(Math.random()*br.qfWinners.length)];
    br.stage='SF';
    wcState.roundOpp = semiOpp;
  } else if(br.stage==='SF'){
    br.stage='F';
    wcState.roundOpp = br.qfWinners.find(t=>t!==wcState.roundOpp) || br.qfWinners[0];
  } else if(br.stage==='F'){
    wcState.stage='champion';
  }
}
function renderWcScreen(){
  if(!wcState){ renderHub(); return; }
  if(wcState.stage==='country'){
    const grid = COUNTRIES.map(c=>`<div class="opt-btn" data-action="wc_pick_country" data-country="${c.n}"><b>${c.n}</b></div>`).join('');
    setMetaBody(`
      <div class="meta-title">🏆 월드컵 토너먼트</div>
      <div class="meta-sub">대표할 국가를 선택해줘 · 16개국 · 4개조 조별리그 → 8강 → 4강 → 결승</div>
      <div class="country-grid">${grid}</div>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로</div>
    `);
  } else if(wcState.stage==='group'){
    const played = wcState.results.map(r=>`${r.opp} 전 ${r.gf}:${r.ga}`).join(' · ')||'아직 없음';
    const next = wcState.opponents[wcState.matchIdx];
    setMetaBody(`
      <div class="meta-title">🏆 ${wcState.country} · 조별리그 (E조)</div>
      <div class="meta-sub">${wcState.matchIdx}/3 경기 완료 · ${played}</div>
      <div class="fixture-box">다음 상대: <b>${next}</b> (OVR ${wcState.opponentOVR[next]})</div>
      <div class="fixture-box" style="font-size:10.5px;color:#8aa;">🔼 조 1~2위만 8강 토너먼트 진출</div>
      <button class="continue-btn" data-action="wc_start_group_match">⚽ 경기 시작</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로 (진행상황 유지)</div>
    `);
  } else if(wcState.stage==='knockout_intro'){
    const rn = wcState.bracket.stage==='QF'?'8강':(wcState.bracket.stage==='SF'?'4강':'결승');
    setMetaBody(`
      <div class="meta-title">🎉 조별리그 통과!</div>
      <div class="meta-sub">토너먼트 대진표가 확정됐어.</div>
      ${wcBracketHtml()}
      <button class="continue-btn" data-action="wc_start_knockout">🏁 ${rn} 시작</button>
    `);
  } else if(wcState.stage==='knockout'){
    const rn = wcState.bracket.stage==='QF'?'8강':(wcState.bracket.stage==='SF'?'4강':'결승');
    setMetaBody(`
      <div class="meta-title">🏆 ${rn}</div>
      ${wcBracketHtml()}
      <div class="fixture-box">상대: <b>${wcState.roundOpp}</b></div>
      <button class="continue-btn" data-action="wc_start_knockout">⚽ ${rn} 경기 시작</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로 (진행상황 유지)</div>
    `);
  } else if(wcState.stage==='out'){
    const table=wcGroupStandings();
    setMetaBody(`
      <div class="meta-title">😢 조별리그 탈락</div>
      <div class="meta-sub">최종 순위 안에 들지 못했어. 다음 기회에!</div>
      ${wcTableHtml(table)}
      <button class="continue-btn" data-action="goto_hub">메인으로</button>
    `);
  } else if(wcState.stage==='out_knockout'){
    const rn = wcState.bracket.stage==='QF'?'8강':(wcState.bracket.stage==='SF'?'4강':'결승');
    setMetaBody(`
      <div class="meta-title">😢 ${rn} 탈락</div>
      <div class="meta-sub">토너먼트에서 여기까지 왔어! 다음엔 우승까지 노려보자.</div>
      <button class="continue-btn" data-action="goto_hub">메인으로</button>
    `);
  } else if(wcState.stage==='champion'){
    setMetaBody(`
      <div class="meta-title" style="color:var(--gold);">🏆 챔피언!</div>
      <div class="trophy-emoji">🏆</div>
      <div class="meta-sub">${wcState.country}, 16개국을 뚫고 월드컵 우승을 차지했다!</div>
      <button class="continue-btn" data-action="goto_hub">메인으로</button>
    `);
  } else if(wcState.stage==='runnerup'){
    setMetaBody(`
      <div class="meta-title">🥈 준우승</div>
      <div class="trophy-emoji">🥈</div>
      <div class="meta-sub">결승에서 아쉽게 패배했어. 다음엔 우승이야!</div>
      <button class="continue-btn" data-action="goto_hub">메인으로</button>
    `);
  }
}
function wcTableHtml(table){
  const rows = table.map(t=>`<tr class="${t.name==='나의 팀'?'me':''}"><td class="tname">${t.name}</td><td>${t.p}</td><td>${t.w}</td><td>${t.d}</td><td>${t.l}</td><td>${t.gf}:${t.ga}</td><td><b>${t.pts}</b></td></tr>`).join('');
  return `<table class="meta-table"><tr><th>팀</th><th>경기</th><th>승</th><th>무</th><th>패</th><th>득실</th><th>승점</th></tr>${rows}</table>`;
}
function wcBracketHtml(){
  const br=wcState.bracket;
  const stageLabel=(s)=> s==='QF'?'8강':(s==='SF'?'4강':'결승');
  return `<div class="fixture-box" style="line-height:1.9;">
    <b style="color:var(--gold);">${stageLabel(br.stage)} 진행 중</b><br>
    ${wcState.country} vs ${wcState.roundOpp||br.qfOpp}<br>
    <span style="color:#8aa;font-size:10px;">나머지 대진은 자동 진행됩니다</span>
  </div>`;
}
function wcStartNextGroupMatch(){
  blueRosterSource=null;
  const opp=wcState.opponents[wcState.matchIdx];
  hud('r', opp);
  opponentOVR = wcState.opponentOVR[opp] || 70;
  startRealMatch(opp);
}
function wcStartKnockoutMatch(){
  blueRosterSource=null;
  hud('r', wcState.roundOpp);
  aiDifficulty = wcState.bracket.stage==='QF'? 1.05 : (wcState.bracket.stage==='SF'? 1.12 : 1.2);
  opponentOVR = (wcState.opponentOVR[wcState.roundOpp] || 74) + 3;
  wcState.stage='knockout';
  startRealMatch(wcState.roundOpp);
}
function wcOnMatchEnd(b,r,win){
  if(wcState.stage==='group'){
    wcState.results.push({opp:wcState.opponents[wcState.matchIdx], gf:b, ga:r});
    wcState.matchIdx++;
    if(wcState.matchIdx<3) return '⚽ 다음 조별리그 경기';
    wcSimRestOfGroup();
    const table=wcGroupStandings();
    const myIdx=table.findIndex(t=>t.name==='나의 팀');
    if(myIdx<2){
      wcBuildBracket();
      wcState.stage='knockout_intro';
      return '🏁 토너먼트 대진표 확인';
    } else {
      wcState.stage='out';
      return '📋 결과 확인';
    }
  } else if(wcState.stage==='knockout'){
    wcAdvanceBracket(win===1);
    if(wcState.stage==='champion') return '🏆 우승 세리머니';
    if(wcState.stage==='out_knockout') return '📋 결과 확인';
    wcState.stage='knockout_intro';
    return '🏁 다음 라운드 대진표 확인';
  }
  return '계속하기';
}

// ── 리그 모드 ──
function makeRoundRobin(n){
  const teams=[...Array(n).keys()];
  const rounds=[];
  for(let r=0;r<n-1;r++){
    const pairs=[];
    for(let i=0;i<n/2;i++) pairs.push([teams[i], teams[n-1-i]]);
    rounds.push(pairs);
    const last=teams.pop();
    teams.splice(1,0,last);
  }
  return rounds;
}
function leagueNew(){
  const names=['나의 팀', ...shuffle(LEAGUE_CLUB_NAMES)];
  const ovrs=names.map((n,i)=> i===0?74:Math.round(60+Math.random()*25));
  leagueState = {
    teams:names,
    ovr:ovrs,
    table:names.map(()=>({p:0,w:0,d:0,l:0,gf:0,ga:0,pts:0})),
    fixtures:makeRoundRobin(8),
    matchday:0,
    done:false
  };
  persistLeague();
}
function leagueApply(ai,bi,gfA,gaA){
  const A=leagueState.table[ai], B=leagueState.table[bi];
  A.p++; B.p++; A.gf+=gfA; A.ga+=gaA; B.gf+=gaA; B.ga+=gfA;
  if(gfA>gaA){ A.w++; A.pts+=3; B.l++; }
  else if(gfA<gaA){ B.w++; B.pts+=3; A.l++; }
  else { A.d++; B.d++; A.pts++; B.pts++; }
}
function leagueStandingsSorted(){
  return leagueState.teams.map((n,i)=>({name:n, idx:i, ...leagueState.table[i]}))
    .sort((x,y)=> y.pts-x.pts || (y.gf-y.ga)-(x.gf-x.ga) || y.gf-x.gf);
}
function persistLeague(){
  try{ window.parent.postMessage({type:'soccer11_league_state', state:leagueState}, '*'); }catch(e){}
}
function renderLeagueHome(){
  metaMode='league';
  if(!leagueState){
    setMetaBody(`
      <div class="meta-title">📅 리그 모드</div>
      <div class="meta-sub">8팀이 한 번씩 맞붙는 풀리그야. 매 라운드 결과는 자동 저장돼서 다음에 이어서 할 수 있어.</div>
      <button class="continue-btn" data-action="league_new">🏁 새 시즌 시작</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로</div>
    `);
    return;
  }
  const table=leagueStandingsSorted();
  if(leagueState.done){
    const champ=table[0];
    setMetaBody(`
      <div class="meta-title" style="color:var(--gold);">🏆 시즌 종료!</div>
      <div class="meta-sub"><b style="color:#fff;">${champ.name}</b> 우승 (${champ.pts}점)</div>
      ${leagueTableHtml(table)}
      <button class="continue-btn" data-action="league_new">🔄 새 시즌 시작</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로</div>
    `);
  } else {
    const round=leagueState.fixtures[leagueState.matchday];
    const userPair = round.find(pr=>pr.includes(0));
    const oppIdx = userPair[0]===0?userPair[1]:userPair[0];
    setMetaBody(`
      <div class="meta-title">📅 리그 모드 · ${leagueState.matchday+1}/7 라운드</div>
      <div class="fixture-box">이번 라운드 상대: <b>${leagueState.teams[oppIdx]}</b></div>
      ${leagueTableHtml(table)}
      <button class="continue-btn" data-action="league_play">⚽ 경기 시작</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로 (진행상황 저장됨)</div>
    `);
  }
}
function leagueTableHtml(table){
  const rows = table.map(t=>`<tr class="${t.idx===0?'me':''}"><td class="tname">${t.name}</td><td>${t.p}</td><td>${t.w}</td><td>${t.d}</td><td>${t.l}</td><td>${t.gf}:${t.ga}</td><td><b>${t.pts}</b></td></tr>`).join('');
  return `<table class="meta-table"><tr><th>팀</th><th>경기</th><th>승</th><th>무</th><th>패</th><th>득실</th><th>승점</th></tr>${rows}</table>`;
}
function leaguePlayMatchday(){
  blueRosterSource=null;
  const round=leagueState.fixtures[leagueState.matchday];
  let userPair=null; const others=[];
  for(const pr of round){ if(pr.includes(0)) userPair=pr; else others.push(pr); }
  for(const [ai,bi] of others){
    const [ga,gb]=simScoreline(leagueState.ovr?leagueState.ovr[ai]:70, leagueState.ovr?leagueState.ovr[bi]:70);
    leagueApply(ai,bi, ga, gb);
  }
  const oppIdx = userPair[0]===0?userPair[1]:userPair[0];
  leagueState._pendingOpp=oppIdx;
  aiDifficulty=1.0;
  opponentOVR = (leagueState.ovr && leagueState.ovr[oppIdx]) || 70;
  hud('r', leagueState.teams[oppIdx]);
  startRealMatch(leagueState.teams[oppIdx]);
}
function leagueOnMatchEnd(b,r,win){
  const oppIdx=leagueState._pendingOpp;
  leagueApply(0, oppIdx, b, r);
  leagueState.matchday++;
  if(leagueState.matchday>=7) leagueState.done=true;
  persistLeague();
  return leagueState.done? '🏆 시즌 최종 결과 보기' : '📅 다음 라운드로';
}

// ── 커리어 모드 / 이적시장 ──
const NAME_POOL=['김민준','이서준','박도윤','최시우','정하준','강주원','조은우','윤지호','장현우','임도현',
  '한지훈','오승민','서준혁','권태양','신동욱','배재현','황인성','문성민','안재원','송민호',
  '카를로스','디에고','루카스','안토니오','마르코','유키','하비에르','토마스','브루노','니콜라스'];
const CREST_POOL=['⚽','🦁','🐉','⚡','🔥','🛡️','⭐','🦅','👑','💎'];

function ovrOf(p){ const a=p.attrs; return Math.round((a.pace+a.shoot+a.pass+a.tackle+a.stam)/5); }
function genSquadPlayer(role, ovrTarget, age){
  const a = age||(18+Math.floor(Math.random()*17));
  const room = a<23? 8+Math.floor(Math.random()*13) : (a<27? 2+Math.floor(Math.random()*7) : Math.floor(Math.random()*3));
  return {
    id:'sq'+Math.random().toString(36).slice(2,9),
    name: NAME_POOL[Math.floor(Math.random()*NAME_POOL.length)],
    role, age: a,
    contract: 1+Math.floor(Math.random()*3),
    potential: clamp((ovrTarget||60)+room, 45, 99),
    attrs: genAttrs(role, ovrTarget)
  };
}
function playerValue(p){
  const ovr=ovrOf(p);
  const ageFactor = p.age<=22? (0.75+(p.age-18)*0.05) : (p.age<=29? 1.15 : Math.max(0.22, 1.15-(p.age-29)*0.13));
  return Math.max(300000, Math.round(ovr*ovr*900*ageFactor/1000)*1000);
}
function tierOvrRange(tier){
  const base = 50+(tier-1)*10;
  return [base, base+25];
}
function genInitialSquad(){
  const roles=[...Array(2).fill('GK'), ...Array(5).fill('DF'), ...Array(5).fill('MF'), ...Array(4).fill('FW')];
  return roles.map(r=> genSquadPlayer(r, 58+Math.floor(Math.random()*16)));
}
function genMarketPlayer(omin,omax){
  omin=omin||55; omax=omax||93;
  const roles=['GK','DF','MF','FW'];
  const r=roles[Math.floor(Math.random()*roles.length)];
  const p=genSquadPlayer(r, omin+Math.floor(Math.random()*Math.max(1,omax-omin)));
  p.price=playerValue(p);
  return p;
}
function genMarketPool(n,omin,omax){ const arr=[]; for(let i=0;i<n;i++) arr.push(genMarketPlayer(omin,omax)); return arr; }

function pickSquadForFormation(squad, formationName){
  const F=FORMATIONS[formationName]||FORMATIONS['4-4-2'];
  const need={GK:0,DF:0,MF:0,FW:0};
  F.roles.forEach(r=>need[r]++);
  const byRole={GK:[],DF:[],MF:[],FW:[]};
  squad.forEach(pl=> byRole[pl.role] && byRole[pl.role].push(pl));
  Object.keys(byRole).forEach(r=> byRole[r].sort((a,b)=> ovrOf(b)-ovrOf(a)));
  const chosen=[];
  for(const role of ['GK','DF','MF','FW']){
    const picks=byRole[role].slice(0, need[role]);
    while(picks.length<need[role]) picks.push(genSquadPlayer(role,60));
    chosen.push(...picks);
  }
  return chosen;
}
function getLineupForFormation(formationName){
  if(!careerState) return null;
  careerState.lineup = careerState.lineup||{};
  const F=FORMATIONS[formationName]||FORMATIONS['4-4-2'];
  const saved = careerState.lineup[formationName];
  const bySlotRole = F.roles;
  const squadById={}; careerState.squad.forEach(p=> squadById[p.id]=p);
  // 저장된 라인업 검증: id 존재 + 역할 일치 + 중복 없어야 유효
  if(saved && saved.length===11){
    const used=new Set(); let valid=true;
    for(let i=0;i<11;i++){
      const pid=saved[i];
      if(!pid || !squadById[pid] || squadById[pid].role!==bySlotRole[i] || used.has(pid)){ valid=false; break; }
      used.add(pid);
    }
    if(valid) return saved.slice();
  }
  // 유효하지 않으면 자동 베스트11로 채우고 저장
  const auto=pickSquadForFormation(careerState.squad, formationName).map(p=>p.id);
  careerState.lineup[formationName]=auto;
  return auto;
}
function makeTeamFromSquad(squad, team, formationName, explicitIds){
  const F=FORMATIONS[formationName]||FORMATIONS['4-4-2'];
  let chosen;
  if(explicitIds && explicitIds.length===11){
    const squadById={}; squad.forEach(p=> squadById[p.id]=p);
    chosen = explicitIds.map((id,i)=> squadById[id] || genSquadPlayer(F.roles[i],60));
  } else {
    chosen = pickSquadForFormation(squad, formationName);
  }
  const arr=[];
  for(let i=0;i<11;i++){
    const f=F.slots[i], role=F.roles[i];
    const src=chosen[i];
    const fx = team==='B'? f.x : 1-f.x;
    arr.push({
      id:team+i, team, num:i+1, role, isGK:role==='GK', baseFx:fx, baseFy:f.y,
      x:H0+fx*(H1-H0), y:V0+f.y*(V1-V0),
      vx:0, vy:0, facing:{x:team==='B'?1:-1,y:0},
      attrs:src.attrs, ovr:ovrOf(src), pname:src.name, squadId:src.id, appearance:src.appearance||null,
      stamina:100, shielding:false, jockeying:false, aiState:'HOLD',
      runUntil:0, pressUntil:0, stumbleUntil:0, skillEvadeUntil:0,
      matchGoals:0, matchAssists:0, matchTackles:0
    });
  }
  return arr;
}

const SAVED_CAREER = __SAVED_CAREER_JSON__;
let careerState = SAVED_CAREER && SAVED_CAREER.squad ? SAVED_CAREER : null;
let blueRosterSource=null; // null | 'career'

function persistCareer(){
  try{ window.parent.postMessage({type:'soccer11_career_state', state:careerState}, '*'); }catch(e){}
}
function fmtMoney(v){ return (v/10000).toFixed(0)+'만'; }

function careerCreate(name, crest){
  const tier=2;
  const [omin,omax]=tierOvrRange(tier);
  careerState = {
    clubName: name && name.trim()? name.trim() : '나의 구단',
    crest: crest||'⚽',
    budget: 50000000,
    season: 1,
    tier,
    trainingPoints: 20,
    squad: genInitialSquad(),
    market: genMarketPool(10, omin, omax),
    league: {
      teams: ['__CLUB__', ...shuffle(LEAGUE_CLUB_NAMES)],
      ovr: [70, ...LEAGUE_CLUB_NAMES.map(()=> omin+Math.round(Math.random()*(omax-omin)))],
      table: Array(8).fill(0).map(()=>({p:0,w:0,d:0,l:0,gf:0,ga:0,pts:0})),
      fixtures: makeRoundRobin(8),
      matchday: 0, done:false
    }
  };
  careerState.league.teams[0]=careerState.clubName;
  persistCareer();
}
function careerStandingsSorted(){
  return careerState.league.teams.map((n,i)=>({name:n, idx:i, ...careerState.league.table[i]}))
    .sort((x,y)=> y.pts-x.pts || (y.gf-y.ga)-(x.gf-x.ga) || y.gf-x.gf);
}
function careerPlayMatchday(){
  if(!careerState || careerState.league.done) return;
  const round=careerState.league.fixtures[careerState.league.matchday];
  if(!round) return;
  let userPair=null; const others=[];
  for(const pr of round){ if(pr.includes(0)) userPair=pr; else others.push(pr); }
  for(const [ai,bi] of others){
    const [ga,gb]=simScoreline(careerState.league.ovr[ai], careerState.league.ovr[bi]);
    const A=careerState.league.table[ai], B=careerState.league.table[bi];
    A.p++; B.p++; A.gf+=ga; A.ga+=gb; B.gf+=gb; B.ga+=ga;
    if(ga>gb){ A.w++; A.pts+=3; B.l++; } else if(ga<gb){ B.w++; B.pts+=3; A.l++; } else { A.d++;B.d++;A.pts++;B.pts++; }
  }
  const oppIdx = userPair[0]===0?userPair[1]:userPair[0];
  careerState.league._pendingOpp=oppIdx;
  aiDifficulty=1.0;
  opponentOVR = careerState.league.ovr[oppIdx];
  blueRosterSource='career';
  hud('r', careerState.league.teams[oppIdx]);
  startRealMatch(careerState.league.teams[oppIdx]);
}
function careerOnMatchEnd(b,r,win){
  const oppIdx=careerState.league._pendingOpp;
  const A=careerState.league.table[0], B=careerState.league.table[oppIdx];
  A.p++; B.p++; A.gf+=b; A.ga+=r; B.gf+=r; B.ga+=b;
  if(b>r){ A.w++; A.pts+=3; B.l++; } else if(b<r){ B.w++; B.pts+=3; A.l++; } else { A.d++;B.d++;A.pts++;B.pts++; }
  careerState.league.matchday++;
  if(careerState.league.matchday>=7) careerState.league.done=true;

  let gained=5+(win?2:0);
  if(typeof blue!=='undefined' && blue){
    for(const p of blue){
      gained += (p.matchGoals||0)*3 + (p.matchAssists||0)*2 + (p.matchTackles||0)*1;
    }
  }
  careerState.trainingPoints = (careerState.trainingPoints||0) + Math.round(gained);

  persistCareer();
  return careerState.league.done? '🏆 시즌 결산 보기' : '📅 다음 라운드로';
}
function careerSeasonEnd(){
  const table=careerStandingsSorted();
  const myPos = table.findIndex(t=>t.idx===0)+1;
  const prize = myPos===1? 30000000 : (myPos<=3? 15000000 : (myPos<=6? 8000000 : 3000000));
  careerState.budget += prize;

  let tierChange=0;
  careerState.tier = careerState.tier||2;
  if(myPos<=2 && careerState.tier<4){ careerState.tier++; tierChange=1; }
  else if(myPos>=7 && careerState.tier>1){ careerState.tier--; tierChange=-1; }

  const retired=[], departed=[];
  careerState.squad.forEach(p=>{
    p.age++;
    p.contract = (p.contract===undefined?2:p.contract)-1;
    const a=p.attrs;
    const grow=(k)=>{
      if(p.age<24) a[k]=clamp(a[k]+Math.round(Math.random()*3),28,99);
      else if(p.age<=29) a[k]=clamp(a[k]+Math.round(Math.random()*2-1),28,99);
      else a[k]=clamp(a[k]-Math.round(1+Math.random()*2),20,99);
    };
    ['pace','shoot','pass','tackle','stam'].forEach(grow);
  });
  careerState.squad = careerState.squad.filter(p=>{
    if(p.age>=36){ retired.push(p.name); return false; }
    if(p.contract<=0){
      if(Math.random()<0.4){ departed.push(p.name); return false; }
      p.contract=1+Math.floor(Math.random()*3);
    }
    return true;
  });
  while(careerState.squad.filter(p=>p.role==='GK').length<2) careerState.squad.push(genSquadPlayer('GK',60,21));
  while(careerState.squad.length<16) careerState.squad.push(genSquadPlayer(['DF','MF','FW'][Math.floor(Math.random()*3)],60,20));

  const [omin,omax]=tierOvrRange(careerState.tier);
  careerState.market = genMarketPool(10, omin, omax);
  let academyProspect=null;
  if(Math.random()<0.45){
    const role=['DF','MF','FW'][Math.floor(Math.random()*3)];
    const prospect=genSquadPlayer(role, 62+Math.floor(Math.random()*10), 17+Math.floor(Math.random()*3));
    prospect.price=Math.round(playerValue(prospect)*0.5);
    prospect.academy=true;
    careerState.market.unshift(prospect);
    academyProspect=prospect.name;
  }

  careerState.season++;
  careerState.league.table = Array(8).fill(0).map(()=>({p:0,w:0,d:0,l:0,gf:0,ga:0,pts:0}));
  careerState.league.fixtures = makeRoundRobin(8);
  careerState.league.matchday = 0;
  careerState.league.done = false;
  careerState.league.ovr = [70, ...LEAGUE_CLUB_NAMES.map(()=> omin+Math.round(Math.random()*(omax-omin)))];
  persistCareer();
  return {myPos, prize, retired, departed, tierChange, academyProspect};
}
function careerBuy(id){
  const p=careerState.market.find(m=>m.id===id);
  if(!p) return;
  if(careerState.budget<p.price){ renderCareerMarket('예산이 부족합니다.'); return; }
  careerState.budget-=p.price;
  careerState.squad.push({id:p.id,name:p.name,role:p.role,age:p.age,contract:p.contract||2,attrs:p.attrs});
  careerState.market=careerState.market.filter(m=>m.id!==id);
  persistCareer();
  renderCareerMarket(`✅ ${p.name} 영입 완료!`);
}
function careerSell(id){
  const p=careerState.squad.find(s=>s.id===id);
  if(!p) return;
  const gkCount=careerState.squad.filter(s=>s.role==='GK').length;
  if(careerState.squad.length<=12 || (p.role==='GK' && gkCount<=1)){
    renderCareerSquad('최소 스쿼드 인원(또는 GK)은 유지해야 해!');
    return;
  }
  const value=Math.round(playerValue(p)*0.7);
  careerState.budget+=value;
  careerState.squad=careerState.squad.filter(s=>s.id!==id);
  persistCareer();
  renderCareerSquad(`✅ ${p.name} 방출 완료 (+${fmtMoney(value)})`);
}

const TIER_NAMES=['','4부 리그','3부 리그','2부 리그','1부 리그(최상위)'];
function careerSquadRowsHtml(){
  const rows=[...careerState.squad].sort((a,b)=> ovrOf(b)-ovrOf(a));
  return rows.map(p=>`<tr><td class="tname">${p.name}</td><td>${p.role}</td><td>${p.age}</td><td><b>${ovrOf(p)}</b></td><td>${fmtMoney(playerValue(p))}</td><td>${p.contract||1}년</td>
    <td><div class="mini-btn" data-action="career_sell" data-id="${p.id}">방출</div></td></tr>`).join('');
}
function renderCareerSquad(msg){
  metaMode='career';
  const hasCustom = careerState.squad.some(p=>p.custom);
  setMetaBody(`
    <div class="meta-title">👥 스쿼드 (${careerState.squad.length}명)</div>
    <div class="meta-sub">${msg||'선수를 방출해 예산을 확보할 수 있어. 최소 12명은 유지해야 해. 계약이 0년이면 시즌 종료 시 이적할 수도 있어.'}</div>
    <table class="meta-table"><tr><th>이름</th><th>포지션</th><th>나이</th><th>OVR</th><th>시장가</th><th>계약</th><th></th></tr>${careerSquadRowsHtml()}</table>
    ${hasCustom? '' : '<button class="continue-btn" data-action="career_custom_create" style="margin-bottom:10px;">✨ 나만의 선수 만들기</button>'}
    <div class="ghost-btn" data-action="career_hub">◀ 구단 사무실로</div>
  `);
}

// ── 나만의 선수 만들기 (커스텀 선수 생성) ──
let customDraft={ name:'', role:'FW', skin:0, hair:1, hairStyle:'short', height:'medium' };
function syncCustomName(){
  const ni=document.getElementById('customNameInput');
  if(ni) customDraft.name = ni.value;
}
function renderCareerCustomCreate(){
  metaMode='career';
  const heightVal={small:0.92, medium:1.0, large:1.08}[customDraft.height];
  setMetaBody(`
    <div class="meta-title">✨ 나만의 선수 만들기</div>
    <div class="meta-sub">이름, 포지션, 외형을 직접 골라서 나만의 유망주를 만들어봐. 한 커리어당 1명만 만들 수 있어.</div>
    <input id="customNameInput" type="text" placeholder="선수 이름 입력" maxlength="10" value="${customDraft.name}" style="width:100%;padding:10px;border-radius:10px;border:1px solid var(--border);background:rgba(255,255,255,.05);color:#fff;font-size:13px;margin-bottom:10px;">
    <div class="meta-sub" style="color:#fff;font-weight:800;margin-bottom:4px;">포지션</div>
    <div class="diff-grid" style="grid-template-columns:repeat(4,1fr);">
      ${['GK','DF','MF','FW'].map(r=>`<div class="opt-btn ${customDraft.role===r?'sel':''}" data-action="custom_pick_role" data-role="${r}"><b>${r}</b></div>`).join('')}
    </div>
    <div class="meta-sub" style="color:#fff;font-weight:800;margin:8px 0 4px;">피부톤</div>
    <div class="diff-grid" style="grid-template-columns:repeat(6,1fr);">
      ${SKIN_TONES.map((c,i)=>`<div class="opt-btn swatch ${customDraft.skin===i?'sel':''}" data-action="custom_pick_skin" data-idx="${i}" style="background:#${c.toString(16).padStart(6,'0')};height:30px;"></div>`).join('')}
    </div>
    <div class="meta-sub" style="color:#fff;font-weight:800;margin:8px 0 4px;">헤어 컬러</div>
    <div class="diff-grid" style="grid-template-columns:repeat(8,1fr);">
      ${HAIR_COLORS.map((c,i)=>`<div class="opt-btn swatch ${customDraft.hair===i?'sel':''}" data-action="custom_pick_hair" data-idx="${i}" style="background:#${c.toString(16).padStart(6,'0')};height:26px;"></div>`).join('')}
    </div>
    <div class="meta-sub" style="color:#fff;font-weight:800;margin:8px 0 4px;">헤어 스타일</div>
    <div class="diff-grid" style="grid-template-columns:repeat(4,1fr);">
      ${HAIR_STYLES.map(s=>`<div class="opt-btn ${customDraft.hairStyle===s?'sel':''}" data-action="custom_pick_hairstyle" data-style="${s}">${s==='bald'?'대머리':s==='short'?'짧은':s==='full'?'풍성한':'모히칸'}</div>`).join('')}
    </div>
    <div class="meta-sub" style="color:#fff;font-weight:800;margin:8px 0 4px;">체형(키)</div>
    <div class="diff-grid">
      ${['small','medium','large'].map(h=>`<div class="opt-btn ${customDraft.height===h?'sel':''}" data-action="custom_pick_height" data-h="${h}">${h==='small'?'작은형':h==='medium'?'표준형':'큰형'}</div>`).join('')}
    </div>
    <button class="continue-btn" data-action="career_custom_confirm" style="margin-top:12px;">✨ 선수 생성하기</button>
    <div class="ghost-btn" data-action="career_squad">◀ 취소하고 스쿼드로</div>
  `);
}
function careerCustomConfirm(){
  const name = (customDraft.name && customDraft.name.trim())? customDraft.name.trim() : '나의 선수';
  const role=customDraft.role;
  const heightVal={small:0.92, medium:1.0, large:1.08}[customDraft.height];
  const p = genSquadPlayer(role, 63+Math.floor(Math.random()*6), 17+Math.floor(Math.random()*2));
  p.name = name;
  p.custom = true;
  p.potential = clamp(p.potential+6, 45, 92);
  p.appearance = {
    skin: SKIN_TONES[customDraft.skin],
    hairColor: HAIR_COLORS[customDraft.hair],
    hairStyle: customDraft.hairStyle,
    heightScale: heightVal
  };
  careerState.squad.push(p);
  persistCareer();
  renderCareerSquad(`✨ ${name} 선수가 유스팀에서 데뷔했어! 라인업에 배치해보자.`);
}

function careerMarketRowsHtml(){
  return careerState.market.map(p=>`<tr><td class="tname">${p.academy?'🌱 ':''}${p.name}</td><td>${p.role}</td><td>${p.age}</td><td><b>${ovrOf(p)}</b></td><td>${fmtMoney(p.price)}</td>
    <td><div class="mini-btn" data-action="career_buy" data-id="${p.id}">영입</div></td></tr>`).join('');
}
function renderCareerMarket(msg){
  metaMode='career';
  const hasAcademy = careerState.market.some(p=>p.academy);
  setMetaBody(`
    <div class="meta-title">💰 이적시장</div>
    <div class="meta-sub">보유 예산: <b style="color:var(--gold);">${fmtMoney(careerState.budget)}</b>${msg? ' · '+msg:''}</div>
    ${hasAcademy? `<div class="fixture-box">🌱 유스 스카우팅 유망주가 시장에 나왔어! 성장 가능성이 높은 특가 매물이야.</div>`:''}
    <table class="meta-table"><tr><th>이름</th><th>포지션</th><th>나이</th><th>OVR</th><th>가격</th><th></th></tr>${careerMarketRowsHtml()}</table>
    <div class="ghost-btn" data-action="career_hub">◀ 구단 사무실로</div>
  `);
}
function renderCareerCreate(){
  metaMode='career';
  setMetaBody(`
    <div class="meta-title">🏟️ 커리어 모드 시작</div>
    <div class="meta-sub">구단 이름과 엠블럼을 골라줘. 2부 리그에서 시작해서 승강제를 거치며 성장하는 모드야.</div>
    <input id="clubNameInput" type="text" placeholder="구단 이름 입력" maxlength="14" style="width:100%;padding:10px;border-radius:10px;border:1px solid var(--border);background:rgba(255,255,255,.05);color:#fff;font-size:13px;margin-bottom:10px;">
    <div class="diff-grid" style="grid-template-columns:repeat(5,1fr);">
      ${CREST_POOL.map(c=>`<div class="opt-btn" data-action="career_pick_crest" data-crest="${c}" style="font-size:20px;">${c}</div>`).join('')}
    </div>
    <button class="continue-btn" data-action="career_confirm_create" style="margin-top:12px;">🏁 창단하기</button>
    <div class="ghost-btn" data-action="goto_hub">◀ 메인으로</div>
  `);
}
let pendingCrest='⚽';
function renderCareerHub(){
  metaMode='career';
  if(!careerState){ renderCareerCreate(); return; }
  const table=careerStandingsSorted();
  const myPos=table.findIndex(t=>t.idx===0)+1;
  const tierTag = TIER_NAMES[careerState.tier||2];
  if(careerState.league.done){
    setMetaBody(`
      <div class="meta-title">${careerState.crest} ${careerState.clubName}</div>
      <div class="meta-sub">${tierTag} · 시즌 ${careerState.season} 종료 · 최종 순위 ${myPos}위 · 예산 <b style="color:var(--gold);">${fmtMoney(careerState.budget)}</b></div>
      ${leagueTableHtml(table)}
      <button class="continue-btn" data-action="career_season_end">🔄 시즌 결산 처리</button>
      <div class="ghost-btn" data-action="goto_hub">◀ 메인으로 (진행상황 저장됨)</div>
    `);
    return;
  }
  const round=careerState.league.fixtures[careerState.league.matchday];
  const userPair=round.find(pr=>pr.includes(0));
  const oppIdx=userPair[0]===0?userPair[1]:userPair[0];
  setMetaBody(`
    <div class="meta-title">${careerState.crest} ${careerState.clubName}</div>
    <div class="meta-sub">${tierTag} · 시즌 ${careerState.season} · ${careerState.league.matchday+1}/7 라운드 · 예산 <b style="color:var(--gold);">${fmtMoney(careerState.budget)}</b> · ${myPos}위</div>
    <div class="fixture-box">이번 라운드 상대: <b>${careerState.league.teams[oppIdx]}</b> (OVR ${careerState.league.ovr[oppIdx]})</div>
    <div class="fixture-box" style="font-size:10.5px;color:#8aa;">🔼 1~2위: 승격 &nbsp; 🔽 7~8위: 강등</div>
    ${leagueTableHtml(table)}
    <div class="diff-grid">
      <div class="opt-btn ${userFormation==='4-4-2'?'sel':''}" data-action="pick_formation" data-form="4-4-2"><b>4-4-2</b></div>
      <div class="opt-btn ${userFormation==='4-3-3'?'sel':''}" data-action="pick_formation" data-form="4-3-3"><b>4-3-3</b></div>
    </div>
    <button class="continue-btn" data-action="career_play" style="margin-top:10px;">⚽ 경기 시작</button>
    <div class="diff-grid" style="margin-top:8px;grid-template-columns:repeat(4,1fr);">
      <div class="opt-btn" data-action="career_lineup">🧩 라인업</div>
      <div class="opt-btn" data-action="career_training">🏋️ 선수 성장</div>
      <div class="opt-btn" data-action="career_squad">👥 스쿼드</div>
      <div class="opt-btn" data-action="career_market">💰 이적시장</div>
    </div>
    <div class="ghost-btn" data-action="goto_hub">◀ 메인으로 (진행상황 저장됨)</div>
  `);
}
const ATTR_LABEL={pace:'속도',shoot:'슈팅',pass:'패스',tackle:'태클',stam:'스태미나'};
function trainCost(p){
  const ovr=ovrOf(p);
  return 8 + Math.floor(Math.max(0,ovr-55)/4)*2;
}
function careerTrain(id, attrKey){
  const p=careerState.squad.find(s=>s.id===id);
  if(!p) return '선수를 찾을 수 없어.';
  if(ovrOf(p)>=p.potential) return `${p.name}은(는) 이미 잠재력 한계(${p.potential})에 도달했어.`;
  const cost=trainCost(p);
  if((careerState.trainingPoints||0)<cost) return `훈련 포인트가 부족해 (필요 ${cost}, 보유 ${careerState.trainingPoints||0}).`;
  careerState.trainingPoints -= cost;
  p.attrs[attrKey] = clamp(p.attrs[attrKey]+1, 28, 99);
  persistCareer();
  return `✅ ${p.name}의 ${ATTR_LABEL[attrKey]} 능력치가 상승했어! (${cost}P 사용)`;
}
function careerTrainRowsHtml(){
  const rows=[...careerState.squad].sort((a,b)=> ovrOf(b)-ovrOf(a));
  return rows.map(p=>{
    const capped = ovrOf(p)>=p.potential;
    const cost=trainCost(p);
    const btns = ['pace','shoot','pass','tackle','stam'].map(k=>
      `<div class="mini-btn ${capped?'disabled':''}" data-action="career_train" data-id="${p.id}" data-attr="${k}" title="${ATTR_LABEL[k]} +1">${ATTR_LABEL[k][0]}+</div>`
    ).join(' ');
    return `<tr><td class="tname">${p.name}</td><td>${p.role}</td><td>${p.age}</td><td><b>${ovrOf(p)}</b></td><td>${capped?'⭐MAX':p.potential}</td>
      <td style="white-space:nowrap;">${btns}</td></tr>`;
  }).join('');
}
function renderCareerTraining(msg){
  metaMode='career';
  setMetaBody(`
    <div class="meta-title">🏋️ 선수 성장</div>
    <div class="meta-sub">훈련 포인트: <b style="color:var(--gold);">${careerState.trainingPoints||0}P</b>${msg? ' · '+msg:''}</div>
    <div class="fixture-box" style="font-size:10.5px;color:#8aa;">경기 결과와 개인 활약(골·어시스트·태클)에 따라 훈련 포인트를 획득해. 능력치를 올릴수록 다음 훈련 비용이 비싸지고, 잠재력(POT) 한계에 도달하면 더 이상 성장하지 않아.</div>
    <table class="meta-table"><tr><th>이름</th><th>포지션</th><th>나이</th><th>OVR</th><th>POT</th><th>훈련</th></tr>${careerTrainRowsHtml()}</table>
    <div class="ghost-btn" data-action="career_hub">◀ 구단 사무실로</div>
  `);
}

const ROLE_LABEL={GK:'GK 골키퍼',DF:'DF 수비수',MF:'MF 미드필더',FW:'FW 공격수'};
function renderCareerLineup(pickSlot){
  metaMode='career';
  const F=FORMATIONS[userFormation]||FORMATIONS['4-4-2'];
  const ids=getLineupForFormation(userFormation);
  const squadById={}; careerState.squad.forEach(p=> squadById[p.id]=p);

  if(pickSlot!==null && pickSlot!==undefined){
    const role=F.roles[pickSlot];
    const usedIds=new Set(ids.filter((id,i)=>i!==pickSlot));
    const candidates=careerState.squad.filter(p=>p.role===role).sort((a,b)=>ovrOf(b)-ovrOf(a));
    const rows=candidates.map(p=>{
      const isStarting=usedIds.has(p.id);
      const isCurrent=ids[pickSlot]===p.id;
      return `<tr class="${isCurrent?'me':''}"><td class="tname">${p.name}${isStarting&&!isCurrent?' <span style="color:#ff8c42;font-size:9.5px;">(주전 중복)</span>':''}</td><td>${p.age}</td><td><b>${ovrOf(p)}</b></td>
        <td><div class="mini-btn" data-action="lineup_assign" data-slot="${pickSlot}" data-id="${p.id}">${isCurrent?'현재 선발':'선발 배치'}</div></td></tr>`;
    }).join('');
    setMetaBody(`
      <div class="meta-title">🧩 ${ROLE_LABEL[role]} 슬롯 배치</div>
      <div class="meta-sub">이 자리에 배치할 선수를 선택해줘. 다른 슬롯에 이미 있는 선수를 고르면 서로 자리가 바뀌어.</div>
      <table class="meta-table"><tr><th>이름</th><th>나이</th><th>OVR</th><th></th></tr>${rows}</table>
      <div class="ghost-btn" data-action="career_lineup">◀ 라인업으로 돌아가기</div>
    `);
    return;
  }

  const rows = ids.map((id,i)=>{
    const p=squadById[id];
    const role=F.roles[i];
    return `<tr><td>${ROLE_LABEL[role]}</td><td class="tname">${p?p.name:'—'}</td><td>${p?p.age:'-'}</td><td><b>${p?ovrOf(p):'-'}</b></td>
      <td><div class="mini-btn" data-action="lineup_pick_slot" data-slot="${i}">교체</div></td></tr>`;
  }).join('');
  const benchCount = careerState.squad.length - 11;
  setMetaBody(`
    <div class="meta-title">🧩 라인업 편집 (${userFormation})</div>
    <div class="meta-sub">현재 선발 11명 · 후보 ${benchCount}명. 슬롯의 '교체' 버튼으로 같은 포지션 후보와 바꿀 수 있어.</div>
    <table class="meta-table"><tr><th>포지션</th><th>선수</th><th>나이</th><th>OVR</th><th></th></tr>${rows}</table>
    <div class="ghost-btn" data-action="career_hub">◀ 구단 사무실로</div>
  `);
}
function lineupAssign(slot, pickedId){
  const F=FORMATIONS[userFormation]||FORMATIONS['4-4-2'];
  const ids=getLineupForFormation(userFormation);
  const dupIdx = ids.indexOf(pickedId);
  if(dupIdx!==-1 && dupIdx!==slot){
    const tmp=ids[slot]; ids[slot]=pickedId; ids[dupIdx]=tmp;
  } else {
    ids[slot]=pickedId;
  }
  careerState.lineup[userFormation]=ids;
  persistCareer();
  renderCareerLineup(null);
}

function renderCareerSeasonEndResult(res){
  metaMode='career';
  const tierMsg = res.tierChange>0? `🔼 승격! 다음 시즌부터 ${TIER_NAMES[careerState.tier]}에서 경쟁해` :
    (res.tierChange<0? `🔽 강등... 다음 시즌은 ${TIER_NAMES[careerState.tier]}에서 재도전이야` : `순위 유지 · ${TIER_NAMES[careerState.tier]} 잔류`);
  setMetaBody(`
    <div class="meta-title" style="color:var(--gold);">📋 시즌 ${careerState.season-1} 결산</div>
    <div class="meta-sub">최종 순위 ${res.myPos}위 · 상금 +${fmtMoney(res.prize)}</div>
    <div class="fixture-box">${tierMsg}</div>
    ${res.retired.length? `<div class="fixture-box">🎗️ 은퇴한 선수: ${res.retired.join(', ')}</div>`:''}
    ${res.departed.length? `<div class="fixture-box">📤 계약 만료로 떠난 선수: ${res.departed.join(', ')}</div>`:''}
    ${res.academyProspect? `<div class="fixture-box">🌱 유스 스카우팅: <b>${res.academyProspect}</b> 선수가 이적시장에 특가로 나왔어!</div>`:''}
    <div class="fixture-box">선수단이 한 살씩 나이를 먹고 능력치가 조정됐어.</div>
    <button class="continue-btn" data-action="career_hub">🏁 시즌 ${careerState.season} 시작하기</button>
  `);
}

// ── 공용 헬퍼 ──
function hud(side, name){
  if(side==='r') document.getElementById('hud-r-name').textContent = name;
}
function startRealMatch(oppLabel){
  hud('r', oppLabel||'RED (AI)');
  hideMeta();
  fullReset();
}

document.getElementById('metaBox').addEventListener('click',(e)=>{
  const el=e.target.closest('[data-action]');
  if(!el) return;
  const act=el.dataset.action;
  if(act==='go_friendly') renderFriendlySetup();
  else if(act==='go_wc'){ wcState={stage:'country'}; renderWcScreen(); }
  else if(act==='go_league') renderLeagueHome();
  else if(act==='go_career') renderCareerHub();
  else if(act==='goto_hub') renderHub();
  else if(act==='friendly_pick') startFriendly(parseFloat(el.dataset.diff));
  else if(act==='pick_formation') pickFormation(el.dataset.form);
  else if(act==='wc_pick_country') wcStart(el.dataset.country);
  else if(act==='wc_start_group_match') wcStartNextGroupMatch();
  else if(act==='wc_start_knockout') wcStartKnockoutMatch();
  else if(act==='league_new'){ leagueNew(); renderLeagueHome(); }
  else if(act==='league_play') leaguePlayMatchday();
  else if(act==='career_pick_crest'){
    pendingCrest=el.dataset.crest;
    document.querySelectorAll('#metaBody .opt-btn[data-action="career_pick_crest"]').forEach(b=>b.classList.remove('sel'));
    el.classList.add('sel');
  }
  else if(act==='career_confirm_create'){
    const nameEl=document.getElementById('clubNameInput');
    careerCreate(nameEl? nameEl.value : '', pendingCrest);
    renderCareerHub();
  }
  else if(act==='career_hub') renderCareerHub();
  else if(act==='career_play') careerPlayMatchday();
  else if(act==='career_squad') renderCareerSquad();
  else if(act==='career_lineup') renderCareerLineup(null);
  else if(act==='career_training'){ const m=null; renderCareerTraining(m); }
  else if(act==='career_train'){ const m=careerTrain(el.dataset.id, el.dataset.attr); renderCareerTraining(m); }
  else if(act==='career_custom_create') renderCareerCustomCreate();
  else if(act==='custom_pick_role'){ syncCustomName(); customDraft.role=el.dataset.role; renderCareerCustomCreate(); }
  else if(act==='custom_pick_skin'){ syncCustomName(); customDraft.skin=parseInt(el.dataset.idx,10); renderCareerCustomCreate(); }
  else if(act==='custom_pick_hair'){ syncCustomName(); customDraft.hair=parseInt(el.dataset.idx,10); renderCareerCustomCreate(); }
  else if(act==='custom_pick_hairstyle'){ syncCustomName(); customDraft.hairStyle=el.dataset.style; renderCareerCustomCreate(); }
  else if(act==='custom_pick_height'){ syncCustomName(); customDraft.height=el.dataset.h; renderCareerCustomCreate(); }
  else if(act==='career_custom_confirm'){
    syncCustomName();
    careerCustomConfirm();
  }
  else if(act==='lineup_pick_slot') renderCareerLineup(parseInt(el.dataset.slot,10));
  else if(act==='lineup_assign') lineupAssign(parseInt(el.dataset.slot,10), el.dataset.id);
  else if(act==='career_market') renderCareerMarket();
  else if(act==='career_sell') careerSell(el.dataset.id);
  else if(act==='career_buy') careerBuy(el.dataset.id);
  else if(act==='career_season_end'){ const res=careerSeasonEnd(); renderCareerSeasonEndResult(res); }
});

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
  } else if(code==='KeyT'){
    tactic = tactic==='balanced'? 'attacking' : (tactic==='attacking'? 'defensive' : 'balanced');
    const tagEl=document.getElementById('tactic-tag');
    if(tagEl) tagEl.textContent = tactic==='attacking'?'공격적':(tactic==='defensive'?'수비적':'균형');
    addFloat(p.x,p.y-30, tactic==='attacking'?'전술: 공격적':(tactic==='defensive'?'전술: 수비적':'전술: 균형'), '#0bdc6b');
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
  if(now()<switchLockUntil) return;
  const cur=activePlayer();
  // 공을 우리 팀 다른 선수가 잡으면 즉시 그 선수로 전환 (최우선 규칙)
  if(ball.owner && ball.owner.team==='B' && ball.owner!==cur){
    activeBlueIdx=blue.indexOf(ball.owner);
    switchLockUntil=now()+0.2;
    autoSwitchCooldown=now()+0.5;
    return;
  }
  if(ball.owner) return;
  if(now()<autoSwitchCooldown) return;
  const near = nearestOnTeamToBall('B', true, null);
  if(near && near!==cur && dist(near,ball) < dist(cur,ball)-34){
    activeBlueIdx=blue.indexOf(near);
    autoSwitchCooldown=now()+0.45;
  }
}

// ── AI ──
function aiCarrierDecision(p,dt){
  const diff = p.team==='R'? aiDifficulty : 1;
  const dir=p.team==='B'?1:-1;
  const goalX=p.team==='B'?GOAL_R_X:GOAL_L_X;
  const distGoal=Math.abs(goalX-p.x);
  const pressure=nearestOpponentDist(p);

  if(distGoal<212 && pressure>26 && Math.random()<0.022*diff){
    doShoot(p, 0.5+Math.random()*0.45);
    return;
  }
  if(pressure<34){
    const t=bestShortPassTarget(p);
    if(t && Math.random()<0.6){
      const pt=applyPassError(p,t.x,t.y);
      kickTo(pt.x,pt.y,300,false); ball.intended=t; ball.lastPasser=p; return;
    }
  }
  if(Math.random()<0.007*diff){
    const t=bestThroughTarget(p);
    if(t){
      const targetX=t.x+dir*60;
      if(!isOffside(p.team,targetX)){
        const pt=applyPassError(p,targetX,t.y);
        kickTo(pt.x,pt.y,350,false); ball.intended=t; ball.lastPasser=p; t.runUntil=now()+1.2; return;
      }
    }
  }
  const opp=nearestOpponent(p);
  let jx=0,jy=0;
  if(opp){
    const ax=p.x-opp.x, ay=p.y-opp.y, al=Math.hypot(ax,ay)||1;
    jx=ax/al; jy=ay/al;
  }
  const tx=p.x+dir*36 + jx*14;
  const ty=clamp(p.y+jy*14, V0+24, V1-24);
  steerTo(p,tx,ty,(p.isGK?0:112*diff*paceMul(p)),dt);
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

function nearestOpponentAttacker(p){
  const opp=p.team==='B'?red:blue;
  let best=null,bd=1e9;
  for(const o of opp){
    if(o.isGK || o.role==='DF') continue;
    const d=dist(p,o);
    if(d<bd){bd=d;best=o;}
  }
  return best || nearestOpponent(p);
}

let markAssignB={}, markAssignR={}, markAssignAt=0;
function computeMarkFor(defTeam){
  const defenders=(defTeam==='B'?blue:red).filter(p=>!p.isGK);
  const attackers=(defTeam==='B'?red:blue).filter(p=>!p.isGK && p.role!=='DF');
  if(!attackers.length) return {};
  const pairs=[];
  for(const d of defenders) for(const a of attackers) pairs.push({d,a,dist:dist(d,a)});
  pairs.sort((x,y)=>x.dist-y.dist);
  const defClaimed=new Set(), atkClaimed=new Set(), result={};
  for(const pr of pairs){
    if(defClaimed.has(pr.d.id) || atkClaimed.has(pr.a.id)) continue;
    result[pr.d.id]=pr.a;
    defClaimed.add(pr.d.id); atkClaimed.add(pr.a.id);
  }
  return result;
}
function updateMarkAssignments(){
  if(now()<markAssignAt) return;
  markAssignAt=now()+0.5;
  markAssignB=computeMarkFor('B');
  markAssignR=computeMarkFor('R');
}

function aiStep(p,dt){
  const t=now();
  if(p===activePlayer()) return;
  if(t<p.stumbleUntil){ p.aiState='STUMBLE'; p.x+=p.vx*0.9*dt; p.y+=p.vy*0.9*dt; clampP(p); return; }

  if(ball.owner===p){
    p.aiState='CARRY';
    if(p.isGK){
      if(Math.random()<0.03) doGKLongKick(p);
      return;
    }
    aiCarrierDecision(p,dt);
    ball.x=p.x+p.facing.x*13; ball.y=p.y+p.facing.y*13; ball.z=0; ball.vz=0;
    touchLog.push({x:p.x,y:p.y,team:p.team});
    if(touchLog.length>500) touchLog.shift();
    clampP(p);
    return;
  }

  // 패스 경로 차단(인터셉트) 시도
  if(ball.intended && !ball.owner && ball.intended.team!==p.team && !p.isGK){
    const r=pointSegDist(p.x,p.y, ball.x,ball.y, ball.intended.x,ball.intended.y);
    if(r.t>0.08 && r.t<0.96 && r.d<74 && isNearestInterceptor(p,r.d)){
      p.aiState='PRESS';
      steerTo(p, r.x, r.y, 168*paceMul(p), dt);
      clampP(p);
      return;
    }
  }

  let tx,ty,spd=108;
  if(p.isGK){
    p.aiState='GK_HOME';
    tx = p.team==='B'? H0+26 : H1-26;
    ty = clamp(ball.y, GY0+24, GY1-24);
    spd=94;
    if(inOwnBox(p,p.team) && ball.owner && ball.owner.team!==p.team && dist(p,ball)<130) spd=112;
  } else if(p.runUntil>t){
    p.aiState='MAKE_RUN';
    const dir=p.team==='B'?1:-1;
    tx=p.x+dir*36; ty=p.y; spd=156;
  } else if(p.pressUntil>t){
    p.aiState='PRESS';
    tx=ball.x; ty=ball.y; spd=146;
  } else if(!ball.owner && nearestOnTeamToBall(p.team,true,activePlayer())===p){
    p.aiState='CHASE';
    tx=ball.x; ty=ball.y; spd=138;
  } else if(ball.owner && ball.owner.team!==p.team && designatedChaser(p.team)===p){
    p.aiState='PRESS';
    tx=ball.owner.x; ty=ball.owner.y; spd=144;
    const tackleChance = p.team==='R'? 0.035*aiDifficulty : 0.035;
    if(dist(p,ball.owner)<22 && Math.random()<tackleChance) attemptStandingTackle(p);
  } else if(ball.owner && ball.owner.team!==p.team && !p.isGK){
    p.aiState='MARK';
    const s=slotPos(p);
    const markMap = p.team==='B'? markAssignB : markAssignR;
    const mark = markMap[p.id] || nearestOpponentAttacker(p);
    const goalX = p.team==='B'? H0 : H1;
    tx = mark.x*0.6 + s.x*0.2 + goalX*0.2;
    ty = mark.y*0.5 + s.y*0.5;
    spd=112;
  } else {
    p.aiState='HOLD';
    const s=slotPos(p); tx=s.x; ty=s.y; spd=105;
  }
  if(p.team==='R') spd*=aiDifficulty;
  spd*=paceMul(p);
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

  let spd=118*paceMul(p);
  const sprinting = keys.has('KeyE') && p.stamina>2;
  const stamMul=staminaMul(p);
  if(sprinting){ spd*=1.38; p.stamina=clamp(p.stamina-32*dt/stamMul,0,100); }
  else { p.stamina=clamp(p.stamina+24*dt*stamMul,0,100); }
  if(p.shielding||p.jockeying) spd*=0.62;
  if(p.isGK){
    spd*=0.86;
    if(p.rushBoost) spd*=1.4;
  }

  const dvx=mx*spd, dvy=my*spd;
  const speedNow=Math.hypot(p.vx,p.vy);
  const wantDirDot = speedNow>1 ? (p.vx*mx + p.vy*my)/speedNow : 1;
  const accelRate = wantDirDot < -0.15 ? 4400 : 2600;
  p.vx=lerpTowards(p.vx,dvx,accelRate*dt);
  p.vy=lerpTowards(p.vy,dvy,accelRate*dt);
  p.x+=p.vx*dt; p.y+=p.vy*dt;

  if(p.isGK && !p.rushBoost){
    p.x=clamp(p.x, H0-2, H0+206);
    if(p.team==='R') p.x=clamp(p.x, H1-206, H1+2);
  } else {
    clampP(p);
  }

  if(ball.owner===p){
    const fx=p.facing.x||1, fy=p.facing.y||0;
    ball.x = lerpTowards(ball.x, p.x+fx*15, 900*dt);
    ball.y = lerpTowards(ball.y, p.y+fy*15, 900*dt);
    ball.z=0; ball.vz=0;
    touchLog.push({x:p.x,y:p.y,team:p.team});
    if(touchLog.length>500) touchLog.shift();
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

  if(ball.z>0 || ball.vz>0){
    ball.vz -= GRAVITY*dt;
    ball.z = Math.max(0, ball.z+ball.vz*dt);
    if(ball.z<=0){ ball.z=0; ball.vz = ball.vz<-40? -ball.vz*0.32 : 0; }
  }

  if(ball.y<V0+8){ ball.y=V0+8; ball.vy=Math.abs(ball.vy)*0.55; }
  if(ball.y>V1-8){ ball.y=V1-8; ball.vy=-Math.abs(ball.vy)*0.55; }

  const inGoalMouthY = ball.y>GY0 && ball.y<GY1;
  if(ball.x<H0-2){
    if(inGoalMouthY && ball.z<30){ scoreGoal('R'); return; }
    ball.x=H0-2; ball.vx=Math.abs(ball.vx)*0.5;
  }
  if(ball.x>H1+2){
    if(inGoalMouthY && ball.z<30){ scoreGoal('B'); return; }
    ball.x=H1+2; ball.vx=-Math.abs(ball.vx)*0.5;
  }

  if(!ball.dangerChecked){
    if(ball.x<H0+134 && ball.vx<0){
      ball.dangerChecked=true;
      tryGKSave(blue.find(p=>p.isGK), true);
    } else if(ball.x>H1-134 && ball.vx>0){
      ball.dangerChecked=true;
      tryGKSave(red.find(p=>p.isGK), true);
    }
  }

  if(ball.z<16){
    let bestP=null,bestD=1e9;
    for(const p of players){
      if(now()<p.stumbleUntil) continue;
      const d=dist(p,ball);
      const range = (ball.intended===p)? 30 : 15;
      const spdOk = ball.intended===p ? true : Math.hypot(ball.vx,ball.vy)<300;
      if(d<range && spdOk && d<bestD){ bestD=d; bestP=p; }
    }
    if(bestP){
      ball.owner=bestP; ball.vx=0; ball.vy=0; ball.vz=0; ball.z=0; ball.intended=null; ball.lofted=0;
      touchLog.push({x:bestP.x,y:bestP.y,team:bestP.team});
      if(touchLog.length>500) touchLog.shift();
      if(ball.lastPasser && ball.lastPasser.team!==bestP.team) ball.lastPasser=null;
    }
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
    commentate(gk.team==='B'? '🧤 골키퍼의 환상적인 선방!' : '😮 상대 골키퍼도 잘 막아냅니다.');
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
  const scorer=ball.shotBy;
  if(scorer && scorer.team===team){
    scorer.matchGoals=(scorer.matchGoals||0)+1;
    if(ball.assistCandidate && ball.assistCandidate.team===team && ball.assistCandidate!==scorer){
      ball.assistCandidate.matchAssists=(ball.assistCandidate.matchAssists||0)+1;
    }
  }
  goalReplay = replayBuffer.slice(-26);
  score[team]++;
  updateScoreHUD();
  flashBanner('GOAL!!', (team==='B'?'BLUE':'RED')+' SCORES', team==='B'?'#2ea8ff':'#ff4757');
  commentate(team==='B'? '🎉 GOOOOAL! 우리 팀이 득점에 성공합니다!' : '😱 아... 상대에게 실점을 허용합니다.');
  shakeT=now()+0.5;
  flashT=now()+0.35;
  burst(team==='B'?GOAL_R_X-14:GOAL_L_X+14, (GY0+GY1)/2, team==='B'?'#2ea8ff':'#ff4757', 26, 260);
  burst(team==='B'?GOAL_R_X-14:GOAL_L_X+14, (GY0+GY1)/2, '#ffd400', 14, 220);
  const keepScore={...score};
  resetKickoff();
  score=keepScore;
  freezeUntil=now()+2.6;
}

function updateScoreHUD(){
  document.getElementById('score').textContent = score.B+' : '+score.R;
}

// ── render ──
// ── 각도 있는 브로드캐스트 카메라 (원근 투영) ──
const HORIZON_Y=150, VIEW_HEIGHT=470;
const FAR_SCALE=0.56, NEAR_SCALE=1.18, DEPTH_EASE=0.78;

const SCALE3D=0.034, HEIGHT3D=0.05;
const PITCH_W3D=(H1-H0)*SCALE3D, PITCH_D3D=(V1-V0)*SCALE3D;
const GOAL_H3D=0.9;
const CAM_HEIGHT=17.5, CAM_BACK=21.5;
let blueMeshes=[], redMeshes=[], ballMesh=null, ballSeam=null, refereeMesh=null;
let refX=CX, refY=CY;
let camPosX=0, camPosZ=0, camInit3D=false;

function worldToScreen(wx, wy, wz){
  const wp = new THREE.Vector3((wx-CX)*SCALE3D, (wz||0)*SCALE3D*1.6+0.05, (wy-CY)*SCALE3D);
  const dist = camera.position.distanceTo(wp);
  const v = wp.clone().project(camera);
  const scale = clamp(9/Math.max(dist,1), 0.4, 1.7);
  return { x:(v.x*0.5+0.5)*W, y:(1-(v.y*0.5+0.5))*H, scale };
}

function makePitchTexture(){
  const tw=1024, th=Math.round(1024*((V1-V0)/(H1-H0)));
  const tc=document.createElement('canvas');
  tc.width=tw; tc.height=th;
  const tctx=tc.getContext('2d');
  tctx.fillStyle='#0e3a1f'; tctx.fillRect(0,0,tw,th);
  const bands=10;
  for(let i=0;i<bands;i++){
    tctx.fillStyle = i%2===0? 'rgba(255,255,255,.05)':'rgba(0,0,0,.07)';
    tctx.fillRect(0, Math.round(i*th/bands), tw, Math.ceil(th/bands));
  }
  const sx=tw/(H1-H0), sy=th/(V1-V0);
  const X=(wx)=> (wx-H0)*sx, Y=(wy)=> (wy-V0)*sy;
  tctx.strokeStyle='rgba(255,255,255,.92)'; tctx.lineWidth=4;
  tctx.strokeRect(2,2,tw-4,th-4);
  tctx.beginPath(); tctx.moveTo(tw/2,0); tctx.lineTo(tw/2,th); tctx.stroke();
  tctx.beginPath(); tctx.arc(tw/2,th/2, 70*sx, 0, Math.PI*2); tctx.stroke();
  tctx.beginPath(); tctx.arc(tw/2,th/2,4,0,Math.PI*2); tctx.fillStyle='#fff'; tctx.fill();

  tctx.lineWidth=3;
  tctx.strokeRect(X(H0), Y(GY0-71), 157*sx, (GY1-GY0+142)*sy);
  tctx.strokeRect(X(H1)-157*sx, Y(GY0-71), 157*sx, (GY1-GY0+142)*sy);
  tctx.strokeRect(X(H0), Y(GY0-21), 56*sx, (GY1-GY0+42)*sy);
  tctx.strokeRect(X(H1)-56*sx, Y(GY0-21), 56*sx, (GY1-GY0+42)*sy);

  [[H0+114,CY],[H1-114,CY]].forEach(([px,py])=>{
    tctx.beginPath(); tctx.arc(X(px),Y(py),4,0,Math.PI*2); tctx.fillStyle='#fff'; tctx.fill();
  });
  tctx.beginPath(); tctx.arc(X(H0+114),Y(CY),60*sx,-0.65,0.65); tctx.stroke();
  tctx.beginPath(); tctx.arc(X(H1-114),Y(CY),60*sx,Math.PI-0.65,Math.PI+0.65); tctx.stroke();

  tctx.lineWidth=2.4;
  tctx.beginPath(); tctx.arc(X(H0),Y(V0),13*sx,0,Math.PI/2); tctx.stroke();
  tctx.beginPath(); tctx.arc(X(H1),Y(V0),13*sx,Math.PI/2,Math.PI); tctx.stroke();
  tctx.beginPath(); tctx.arc(X(H0),Y(V1),13*sx,-Math.PI/2,0); tctx.stroke();
  tctx.beginPath(); tctx.arc(X(H1),Y(V1),13*sx,Math.PI,Math.PI*1.5); tctx.stroke();

  const tex=new THREE.CanvasTexture(tc);
  tex.needsUpdate=true;
  return tex;
}

function addGoalMesh(xPos, dir){
  const grp=new THREE.Group();
  const postMat=new THREE.MeshStandardMaterial({color:0xffffff});
  const goalWidth3D=(GY1-GY0)*SCALE3D;
  const post1=new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.045,GOAL_H3D,8), postMat);
  post1.position.set(xPos, GOAL_H3D/2, -goalWidth3D/2);
  const post2=new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.045,GOAL_H3D,8), postMat);
  post2.position.set(xPos, GOAL_H3D/2, goalWidth3D/2);
  const bar=new THREE.Mesh(new THREE.CylinderGeometry(0.045,0.045,goalWidth3D,8), postMat);
  bar.rotation.z=Math.PI/2; bar.position.set(xPos, GOAL_H3D, 0);
  grp.add(post1,post2,bar);
  const netMat=new THREE.MeshBasicMaterial({color:0xffffff, transparent:true, opacity:0.18, side:THREE.DoubleSide});
  const net=new THREE.Mesh(new THREE.PlaneGeometry(goalWidth3D, GOAL_H3D), netMat);
  net.position.set(xPos+dir*0.35, GOAL_H3D/2, 0);
  net.rotation.y=Math.PI/2;
  grp.add(net);
  scene.add(grp);
}

function addStands(){
  const standMat=new THREE.MeshStandardMaterial({color:0x141a20});
  const s1=new THREE.Mesh(new THREE.BoxGeometry(PITCH_W3D+5, 2.2, 1.3), standMat);
  s1.position.set(0, 1.1, -PITCH_D3D/2-2.2);
  scene.add(s1);
  const s2=s1.clone(); s2.position.z=PITCH_D3D/2+2.2; scene.add(s2);

  const lightMat=new THREE.MeshBasicMaterial({color:0xfff4d0});
  [[-PITCH_W3D/2-1, -PITCH_D3D/2-1],[PITCH_W3D/2+1, -PITCH_D3D/2-1],
   [-PITCH_W3D/2-1, PITCH_D3D/2+1],[PITCH_W3D/2+1, PITCH_D3D/2+1]].forEach(([lx,lz])=>{
    const pole=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,4,6), new THREE.MeshStandardMaterial({color:0x222222}));
    pole.position.set(lx,2,lz);
    scene.add(pole);
    const lamp=new THREE.Mesh(new THREE.BoxGeometry(0.5,0.3,0.5), lightMat);
    lamp.position.set(lx,4,lz);
    scene.add(lamp);
  });
}

const SKIN_TONES=[0xffe0bd,0xf1c27d,0xe0ac69,0xc68642,0x8d5524,0x5a3825];
const HAIR_COLORS=[0x1a1410,0x2c1b0e,0x4a2e18,0x6b4226,0xa8763e,0xd4a520,0x8a8a8a,0xe8e8e8];
const HAIR_STYLES=['bald','short','full','mohawk'];
function hashStr(str){
  let h=0;
  for(let i=0;i<str.length;i++){ h=(h*31 + str.charCodeAt(i))|0; }
  return Math.abs(h);
}
function getAppearance(seedStr){
  const h=hashStr(seedStr||'player');
  return {
    skin: SKIN_TONES[h%SKIN_TONES.length],
    hairColor: HAIR_COLORS[(h>>3)%HAIR_COLORS.length],
    hairStyle: HAIR_STYLES[(h>>6)%HAIR_STYLES.length],
    heightScale: 0.92 + ((h>>9)%17)/100 // 0.92~1.08
  };
}
function buildHairMesh(style, color){
  let geo;
  if(style==='full') geo=new THREE.SphereGeometry(0.205,10,8,0,Math.PI*2,0,Math.PI*0.62);
  else if(style==='short') geo=new THREE.SphereGeometry(0.2,10,8,0,Math.PI*2,0,Math.PI*0.42);
  else if(style==='mohawk') geo=new THREE.BoxGeometry(0.06,0.12,0.32);
  else geo=null; // bald
  if(!geo) return null;
  const mesh=new THREE.Mesh(geo, new THREE.MeshStandardMaterial({color}));
  mesh.position.y = style==='mohawk'? 1.29 : 1.18;
  return mesh;
}
function applyAppearance(grp, appearance){
  grp.userData.head.material.color.setHex(appearance.skin);
  if(grp.userData.hair){ grp.remove(grp.userData.hair); grp.userData.hair=null; }
  const hairMesh=buildHairMesh(appearance.hairStyle, appearance.hairColor);
  if(hairMesh){ grp.add(hairMesh); grp.userData.hair=hairMesh; }
  grp.scale.set(appearance.heightScale, appearance.heightScale, appearance.heightScale);
}

function makePlayerMesh(){
  const grp=new THREE.Group();
  const torso=new THREE.Mesh(
    new THREE.CylinderGeometry(0.24,0.3,0.76,8),
    new THREE.MeshStandardMaterial({color:0x2ea8ff})
  );
  torso.position.y=0.62;
  grp.add(torso);
  const head=new THREE.Mesh(
    new THREE.SphereGeometry(0.19,10,8),
    new THREE.MeshStandardMaterial({color:0xe8b48a})
  );
  head.position.y=1.15;
  grp.add(head);
  const ring=new THREE.Mesh(
    new THREE.RingGeometry(0.34,0.43,24),
    new THREE.MeshBasicMaterial({color:0xffd400, transparent:true, opacity:0, side:THREE.DoubleSide})
  );
  ring.rotation.x=-Math.PI/2; ring.position.y=0.02;
  grp.add(ring);
  grp.userData={torso,head,ring,hair:null,_apId:null};
  scene.add(grp);
  return grp;
}

function init3D(){
  scene=new THREE.Scene();
  scene.background=new THREE.Color(0x040a06);
  if(THREE.FogExp2) scene.fog=new THREE.FogExp2(0x040a06, 0.02);

  camera=new THREE.PerspectiveCamera(62, W/H, 0.1, 260);

  renderer=new THREE.WebGLRenderer({antialias:true, alpha:false});
  renderer.setSize(W,H);
  try{ renderer.setPixelRatio(Math.min(window.devicePixelRatio||1, 2)); }catch(e){}
  const wrap=document.getElementById('pitch3d-wrap');
  const overlayEl=document.getElementById('overlay2d');
  wrap.insertBefore(renderer.domElement, overlayEl);

  scene.add(new THREE.AmbientLight(0xffffff, 0.78));
  const dl=new THREE.DirectionalLight(0xffffff, 0.62);
  dl.position.set(8,20,6);
  scene.add(dl);
  const dl2=new THREE.DirectionalLight(0x88aaff, 0.22);
  dl2.position.set(-10,14,-10);
  scene.add(dl2);

  const pitchMesh=new THREE.Mesh(
    new THREE.PlaneGeometry(PITCH_W3D+2, PITCH_D3D+2),
    new THREE.MeshStandardMaterial({map: makePitchTexture()})
  );
  pitchMesh.rotation.x=-Math.PI/2;
  scene.add(pitchMesh);

  addGoalMesh(-PITCH_W3D/2-0.05, -1);
  addGoalMesh(PITCH_W3D/2+0.05, 1);
  addStands();

  for(let i=0;i<11;i++) blueMeshes.push(makePlayerMesh());
  for(let i=0;i<11;i++) redMeshes.push(makePlayerMesh());

  refereeMesh = makePlayerMesh();
  refereeMesh.userData.torso.material.color.setHex(0x111318);
  refereeMesh.userData.head.material.color.setHex(0xe8b48a);
  refereeMesh.scale.set(0.92,0.92,0.92);
  refereeMesh.userData.ring.material.opacity=0;

  ballMesh=new THREE.Mesh(
    new THREE.SphereGeometry(0.24, 14, 12),
    new THREE.MeshStandardMaterial({color:0xffffff, roughness:0.5})
  );
  scene.add(ballMesh);
  ballSeam=new THREE.Mesh(
    new THREE.TorusGeometry(0.24, 0.014, 6, 20),
    new THREE.MeshBasicMaterial({color:0x222222})
  );
  ballMesh.add(ballSeam);
}

function updateOnePlayerMesh(mesh, p, dt){
  if(!p){ mesh.visible=false; return; }
  mesh.visible=true;
  const apId = p.squadId || p.pname || p.id;
  if(mesh.userData._apId !== apId){
    applyAppearance(mesh, p.appearance || getAppearance(apId));
    mesh.userData._apId = apId;
  }
  mesh.position.set((p.x-CX)*SCALE3D, 0, (p.y-CY)*SCALE3D);
  mesh.rotation.y = Math.atan2(p.facing.x||0, p.facing.y||0);
  const speed=Math.hypot(p.vx,p.vy);
  p.animPhase=(p.animPhase||0)+(now()<p.stumbleUntil?0:speed*(dt||0.016)*0.05);
  const bob=Math.abs(Math.sin(p.animPhase))*0.05*clamp(speed/85,0,1);
  mesh.userData.torso.position.y=0.62+bob;
  mesh.userData.torso.material.color.setHex(p.isGK?0xffd400:(p.team==='B'?0x2ea8ff:0xff4757));
  const isActive=(p.team==='B' && p===activePlayer());
  mesh.userData.ring.material.opacity = isActive? (0.55+Math.sin(now()*7)*0.18) : 0;
}

let camZoomMul=1;
function updateCamera3D(dt){
  const p=activePlayer();
  const tx=(ball.x*0.62+p.x*0.38-CX)*SCALE3D;
  const tz=(ball.y*0.55+p.y*0.45-CY)*SCALE3D;
  if(!camInit3D){ camPosX=tx; camPosZ=tz; camInit3D=true; }
  camPosX += (tx-camPosX)*Math.min(1, dt*4);
  camPosZ += (tz-camPosZ)*Math.min(1, dt*4);
  const ballSpeed=Math.hypot(ball.vx,ball.vy);
  const targetZoom = 1 + clamp(ballSpeed/900, 0, 0.32);
  camZoomMul += (targetZoom-camZoomMul)*Math.min(1, dt*2.2);
  camera.position.set(camPosX, CAM_HEIGHT*camZoomMul, camPosZ+CAM_BACK*camZoomMul);
  camera.lookAt(camPosX, 0.4, camPosZ);
}

function updateReferee(dt){
  const dir = (ball.y>CY)? -1:1;
  const targetX = clamp(ball.x + dir*4, H0+20, H1-20);
  const targetY = clamp(ball.y - dir*22, V0+30, V1-30);
  refX += (targetX-refX)*Math.min(1, dt*2.4);
  refY += (targetY-refY)*Math.min(1, dt*2.4);
  refereeMesh.visible = true;
  refereeMesh.position.set((refX-CX)*SCALE3D, 0, (refY-CY)*SCALE3D);
  const dx=targetX-refX, dy=targetY-refY;
  if(Math.hypot(dx,dy)>1) refereeMesh.rotation.y = Math.atan2(dx,dy);
}

function updateScene3D(dt){
  for(let i=0;i<11;i++) updateOnePlayerMesh(blueMeshes[i], blue[i], dt);
  for(let i=0;i<11;i++) updateOnePlayerMesh(redMeshes[i], red[i], dt);
  updateReferee(dt);
  ballMesh.position.set((ball.x-CX)*SCALE3D, 0.24+(ball.z||0)*SCALE3D*1.6, (ball.y-CY)*SCALE3D);
  ballMesh.rotation.y += (ball.spin||0)*0.02;
  updateCamera3D(dt);
  renderer.render(scene, camera);
}

function drawMinimap(){
  const mx=W-186, my=14, mw=174, mh=94;
  octx.save();
  octx.fillStyle='rgba(0,0,0,.5)';
  octx.fillRect(mx-5,my-5,mw+10,mh+10);
  octx.strokeStyle='rgba(255,255,255,.55)'; octx.lineWidth=1;
  octx.strokeRect(mx,my,mw,mh);
  octx.beginPath(); octx.moveTo(mx+mw/2,my); octx.lineTo(mx+mw/2,my+mh); octx.stroke();

  const sx=mw/(H1-H0), sy=mh/(V1-V0);
  function mproj(x,y){ return {x:mx+(x-H0)*sx, y:my+(y-V0)*sy}; }

  for(const p of red){ const q=mproj(p.x,p.y); octx.beginPath(); octx.arc(q.x,q.y,1.7,0,Math.PI*2); octx.fillStyle='#ff4757'; octx.fill(); }
  for(const p of blue){ const q=mproj(p.x,p.y); octx.beginPath(); octx.arc(q.x,q.y,1.7,0,Math.PI*2); octx.fillStyle=(p===activePlayer())?'#ffd400':'#2ea8ff'; octx.fill(); }
  const bq=mproj(ball.x,ball.y);
  octx.beginPath(); octx.arc(bq.x,bq.y,1.9,0,Math.PI*2); octx.fillStyle='#fff'; octx.fill();
  octx.restore();
}

function drawParticles(dt){
  for(let i=particles.length-1;i>=0;i--){
    const pt=particles[i];
    pt.age+=dt;
    if(pt.age>pt.life){ particles.splice(i,1); continue; }
    pt.x+=pt.vx*dt; pt.y+=pt.vy*dt; pt.vy+=140*dt;
    const P=worldToScreen(pt.x,pt.y,0);
    const a=1-pt.age/pt.life;
    octx.beginPath();
    octx.arc(P.x,P.y,pt.size*P.scale,0,Math.PI*2);
    octx.fillStyle=hexA(pt.color,a);
    octx.fill();
  }
}
function hexA(hex,a){
  const c=hex.replace('#','');
  const r=parseInt(c.substring(0,2),16), g=parseInt(c.substring(2,4),16), b=parseInt(c.substring(4,6),16);
  return `rgba(${r},${g},${b},${clamp(a,0,1)})`;
}
function drawPlayerNames(){
  const drawOne=(p)=>{
    if(!p || !p.pname) return;
    const P=worldToScreen(p.x, p.y, 0);
    if(P.scale<0.55) return; // 너무 멀면 생략(가독성)
    const isActive = p.team==='B' && p===activePlayer();
    octx.font=`700 ${Math.max(9,10.5*P.scale)}px Rajdhani, sans-serif`;
    octx.textAlign='center';
    octx.fillStyle = isActive? 'rgba(255,212,0,.95)' : 'rgba(255,255,255,.82)';
    octx.strokeStyle='rgba(0,0,0,.65)'; octx.lineWidth=2.4;
    const label = p.pname;
    const ty = P.y - 26*P.scale;
    octx.strokeText(label, P.x, ty);
    octx.fillText(label, P.x, ty);
  };
  for(const p of blue) drawOne(p);
  for(const p of red) drawOne(p);
}

function drawFloatTexts(){
  for(let i=floatTexts.length-1;i>=0;i--){
    const ft=floatTexts[i];
    const age=now()-ft.born;
    if(age>0.75){ floatTexts.splice(i,1); continue; }
    const a=1-age/0.75;
    const P=worldToScreen(ft.x,ft.y,0);
    octx.font=`900 ${Math.max(10,12*P.scale)}px Orbitron, sans-serif`;
    octx.textAlign='center';
    octx.fillStyle=hexA(ft.color,a);
    octx.fillText(ft.text, P.x, P.y-age*26);
  }
}

function snapshotNow(){
  return {
    bx:ball.x, by:ball.y, bz:ball.z||0,
    blue: blue.map(p=>({x:p.x,y:p.y,isGK:p.isGK,active:p===activePlayer()})),
    red: red.map(p=>({x:p.x,y:p.y,isGK:p.isGK}))
  };
}
function updateOnePlayerMeshFromSnap(mesh, sp, team){
  if(!sp){ mesh.visible=false; return; }
  mesh.visible=true;
  mesh.position.set((sp.x-CX)*SCALE3D, 0, (sp.y-CY)*SCALE3D);
  mesh.userData.torso.material.color.setHex(sp.isGK?0xffd400:(team==='B'?0x2ea8ff:0xff4757));
  mesh.userData.ring.material.opacity = sp.active? 0.6 : 0;
}
function renderReplay3D(dt){
  const dur=2.2, elapsed=clamp(dur-(freezeUntil-now()),0,dur);
  const idx=clamp(Math.floor((elapsed/dur)*(goalReplay.length-1)),0,goalReplay.length-1);
  const snap=goalReplay[idx];
  for(let i=0;i<11;i++) updateOnePlayerMeshFromSnap(blueMeshes[i], snap.blue[i], 'B');
  for(let i=0;i<11;i++) updateOnePlayerMeshFromSnap(redMeshes[i], snap.red[i], 'R');
  refereeMesh.visible=false;
  ballMesh.position.set((snap.bx-CX)*SCALE3D, 0.24+(snap.bz||0)*SCALE3D*1.6, (snap.by-CY)*SCALE3D);

  const bx=(snap.bx-CX)*SCALE3D, bz=(snap.by-CY)*SCALE3D;
  camPosX += (bx-camPosX)*Math.min(1, dt*3);
  camPosZ += (bz-camPosZ)*Math.min(1, dt*3);
  camera.position.set(camPosX, CAM_HEIGHT*0.62, camPosZ+CAM_BACK*0.62);
  camera.lookAt(camPosX, 0.5, camPosZ);
  renderer.render(scene, camera);

  octx.font='900 15px Orbitron, sans-serif'; octx.textAlign='center';
  octx.fillStyle='rgba(255,212,0,.95)';
  octx.fillText('🎬 GOAL REPLAY', W/2, 30);
}

function render(dt){
  octx.clearRect(0,0,W,H);

  if(goalReplay && goalReplay.length && now()<freezeUntil){
    renderReplay3D(dt);
  } else {
    if(goalReplay) goalReplay=null;
    updateScene3D(dt);
    drawPlayerNames();
    drawParticles(dt);
    drawFloatTexts();
  }

  const vig=octx.createRadialGradient(W/2,H/2,H*0.3,W/2,H/2,H*0.8);
  vig.addColorStop(0,'rgba(0,0,0,0)');
  vig.addColorStop(1,'rgba(0,0,0,.4)');
  octx.fillStyle=vig; octx.fillRect(0,0,W,H);

  if(now()<flashT){
    octx.fillStyle=`rgba(255,255,255,${clamp((flashT-now())/0.35,0,1)*0.5})`;
    octx.fillRect(0,0,W,H);
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
      updateMarkAssignments();
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

      replaySampleAcc+=dt;
      if(replaySampleAcc>0.08){
        replaySampleAcc=0;
        replayBuffer.push(snapshotNow());
        if(replayBuffer.length>40) replayBuffer.shift();
      }

      if(now()>adaptCheckAt){
        adaptCheckAt=now()+8;
        const diff=score.B-score.R;
        if(diff>=2) aiDifficulty=clamp(aiDifficulty+0.05,0.6,1.55);
        else if(diff<=-2) aiDifficulty=clamp(aiDifficulty-0.05,0.6,1.55);
      }
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

function computeMOM(){
  let best=null,bv=-1;
  for(const p of players){
    const rating = 6.0 + (p.matchGoals||0)*1.6 + (p.matchAssists||0)*1.0 + (p.matchTackles||0)*0.28;
    if(rating>bv){ bv=rating; best=p; }
  }
  if(!best) return null;
  return { teamLabel: best.team==='B'?'BLUE':'RED', num:best.num, role:best.role, rating:bv.toFixed(1) };
}

function drawHeatmap(){
  const hc=document.getElementById('heatmapCanvas');
  if(!hc || typeof hc.getContext!=='function') return;
  const hctx=hc.getContext('2d');
  if(!hctx) return;
  hctx.clearRect(0,0,180,110);
  hctx.fillStyle='#0e3a1f'; hctx.fillRect(0,0,180,110);
  const cols=9, rows=6;
  const grid=Array.from({length:rows},()=>Array(cols).fill(0));
  let maxV=1;
  for(const t of touchLog){
    if(t.team!=='B') continue;
    const cx=clamp(Math.floor((t.x-H0)/(H1-H0)*cols),0,cols-1);
    const cy=clamp(Math.floor((t.y-V0)/(V1-V0)*rows),0,rows-1);
    grid[cy][cx]++; if(grid[cy][cx]>maxV) maxV=grid[cy][cx];
  }
  const cw=180/cols, ch=110/rows;
  for(let ry=0;ry<rows;ry++) for(let rx=0;rx<cols;rx++){
    const v=grid[ry][rx]/maxV;
    if(v<=0) continue;
    hctx.fillStyle=`rgba(46,168,255,${0.15+v*0.75})`;
    hctx.fillRect(rx*cw,ry*ch,cw,ch);
  }
  hctx.strokeStyle='rgba(255,255,255,.3)'; hctx.lineWidth=1;
  hctx.strokeRect(0.5,0.5,179,109);
}

function endMatch(){
  gameState='finished';
  const b=score.B, r=score.R;
  lastMatchScore={b,r};
  document.getElementById('result-score').textContent=b+' : '+r;
  const tagEl=document.getElementById('result-tag');
  let win=0;
  if(b>r){ tagEl.textContent='🎉 승리!'; tagEl.style.color='#0bdc6b'; win=1; }
  else if(b===r){ tagEl.textContent='🤝 무승부'; tagEl.style.color='#ffd400'; }
  else { tagEl.textContent='😢 패배'; tagEl.style.color='#ff4757'; }
  commentate('🏁 경기 종료! 최종 스코어 '+b+' : '+r);
  const tot=possAcc.b+possAcc.r || 1;
  const pb=Math.round(possAcc.b/tot*100);
  document.getElementById('rs-poss').textContent = pb+' : '+(100-pb);
  document.getElementById('rs-shots').textContent = stats.shots;
  document.getElementById('rs-tackles').textContent = stats.tackles;
  const passPct = stats.passTry>0? Math.round(stats.passOk/stats.passTry*100) : 0;
  const rsPassEl=document.getElementById('rs-pass');
  if(rsPassEl) rsPassEl.textContent = passPct+'%';
  const mom=computeMOM();
  const rsMomEl=document.getElementById('rs-mom');
  if(rsMomEl) rsMomEl.textContent = mom? `${mom.teamLabel} #${mom.num} (${mom.role}) · 평점 ${mom.rating}` : '—';
  drawHeatmap();

  let label='🔄 다시 하기';
  if(metaMode==='wc') label = wcOnMatchEnd(b,r,win) || label;
  else if(metaMode==='league') label = leagueOnMatchEnd(b,r,win) || label;
  else if(metaMode==='career') label = careerOnMatchEnd(b,r,win) || label;
  document.getElementById('retryBtn').textContent = label;

  document.getElementById('endOverlay').style.display='flex';
  const hattrick = blue.some(p=>(p.matchGoals||0)>=3);
  const cleanSheet = (r===0);
  const bigWin = win===1 && (b-r)>=4;
  try{
    window.parent.postMessage({type:'soccer11_result', score:b, opp:r, win:win, hattrick, cleanSheet, bigWin},'*');
  }catch(e){}
}

document.getElementById('retryBtn').addEventListener('click',()=>{
  document.getElementById('endOverlay').style.display='none';
  showMeta();
  if(metaMode==='friendly') renderFriendlySetup();
  else if(metaMode==='wc') renderWcScreen();
  else if(metaMode==='league') renderLeagueHome();
  else if(metaMode==='career') renderCareerHub();
  else renderHub();
});
document.getElementById('exitBtn').addEventListener('click',()=>{
  document.getElementById('endOverlay').style.display='none';
  showMeta();
  renderHub();
});
document.getElementById('kg-toggle').addEventListener('click',()=>{
  const kg=document.getElementById('keyguide');
  const hidden = kg.style.display==='none';
  kg.style.display = hidden? 'block':'none';
  document.getElementById('kg-toggle').textContent = hidden? '⌨ 키 숨기기':'⌨ 키 보기';
});

init3D();
resetKickoff();
score={B:0,R:0}; timeLeft=MATCH_TIME; gameState='menu';
updateScoreHUD();
renderHub();
requestAnimationFrame(loop);
})();
</script>
</body>
</html>
"""


def render():
    import os as _os
    import json as _json
    from utils.database import update_leaderboard, _get_col
    from utils.config import USERS_FILE

    st.markdown("<style>iframe{border:none!important;}</style>", unsafe_allow_html=True)
    st.caption("⚽ 방향키 이동 · A/S/D/W/Q/E/C 공수 전환 조작 · Shift+방향키 스킬무브 | 🏆 최고 득점·리그 진행상황은 자동 저장됩니다")

    _cur_uid = st.session_state.get('logged_in_user', '')

    _bridge_dir = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'components', 'game_bridge')
    _bridge = st.components.v1.declare_component("game_bridge_soccer11", path=_bridge_dir)
    _league_bridge = st.components.v1.declare_component("game_bridge_soccer11_league", path=_bridge_dir)
    _career_bridge = st.components.v1.declare_component("game_bridge_soccer11_career", path=_bridge_dir)

    _result = _bridge(game_type="soccer11_result", key=f"bridge_soccer11_{_cur_uid}", default=None)
    _league_result = _league_bridge(game_type="soccer11_league_state", key=f"bridge_soccer11_league_{_cur_uid}", default=None)
    _career_result = _career_bridge(game_type="soccer11_career_state", key=f"bridge_soccer11_career_{_cur_uid}", default=None)

    if _result and isinstance(_result, dict) and _result.get('type') == 'soccer11_result':
        if not st.session_state.get('_soccer11_saved'):
            st.session_state['_soccer11_saved'] = True
            try:
                _s_score = int(_result.get('score', 0))
                _s_opp   = int(_result.get('opp', 0))
                _s_win   = int(_result.get('win', 0))
                _s_hattrick = bool(_result.get('hattrick', False))
                _s_cleanSheet = bool(_result.get('cleanSheet', False))
                _s_bigWin = bool(_result.get('bigWin', False))
                if _cur_uid:
                    _col = _get_col(USERS_FILE)
                    _doc = _col.find_one({"_id": "main"}, {_cur_uid: 1})
                    if _doc and _cur_uid in _doc:
                        _udata = _doc[_cur_uid]
                        _s11 = _udata.get('game_records', {}).get('soccer11', {})
                        _ach = _s11.get('achievements', {})
                        _streak_cur = _ach.get('winStreakCurrent', 0) + 1 if _s_win else 0
                        _streak_max = max(_ach.get('winStreakMax', 0), _streak_cur)
                        _upd = {
                            f"{_cur_uid}.game_records.soccer11.matches": _s11.get('matches', 0) + 1,
                            f"{_cur_uid}.game_records.soccer11.achievements.hattrick": _ach.get('hattrick', 0) + (1 if _s_hattrick else 0),
                            f"{_cur_uid}.game_records.soccer11.achievements.cleanSheet": _ach.get('cleanSheet', 0) + (1 if _s_cleanSheet else 0),
                            f"{_cur_uid}.game_records.soccer11.achievements.bigWin": _ach.get('bigWin', 0) + (1 if _s_bigWin else 0),
                            f"{_cur_uid}.game_records.soccer11.achievements.winStreakCurrent": _streak_cur,
                            f"{_cur_uid}.game_records.soccer11.achievements.winStreakMax": _streak_max,
                        }
                        if _s_win:
                            _upd[f"{_cur_uid}.game_records.soccer11.wins"] = _s11.get('wins', 0) + 1
                        _col.update_one({"_id": "main"}, {"$set": _upd})
                        if _s_score > _s11.get('score', 0):
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

    if _league_result and isinstance(_league_result, dict) and _league_result.get('type') == 'soccer11_league_state':
        try:
            _league_state = _league_result.get('state')
            if _cur_uid and isinstance(_league_state, dict):
                _col = _get_col(USERS_FILE)
                _col.update_one({"_id": "main"}, {"$set": {
                    f"{_cur_uid}.game_records.soccer11.league": _league_state,
                }})
        except Exception as _e:
            import logging; logging.error(f"[soccer11 league save] {_e}")

    if _career_result and isinstance(_career_result, dict) and _career_result.get('type') == 'soccer11_career_state':
        try:
            _career_state = _career_result.get('state')
            if _cur_uid and isinstance(_career_state, dict):
                _col = _get_col(USERS_FILE)
                _col.update_one({"_id": "main"}, {"$set": {
                    f"{_cur_uid}.game_records.soccer11.career": _career_state,
                }})
        except Exception as _e:
            import logging; logging.error(f"[soccer11 career save] {_e}")

    _saved_league = None
    _saved_achievements = None
    _saved_career = None
    try:
        if _cur_uid:
            _col = _get_col(USERS_FILE)
            _doc = _col.find_one({"_id": "main"}, {f"{_cur_uid}.game_records.soccer11": 1})
            if _doc and _cur_uid in _doc:
                _s11 = _doc[_cur_uid].get('game_records', {}).get('soccer11', {})
                _saved_league = _s11.get('league')
                _saved_achievements = _s11.get('achievements')
                _saved_career = _s11.get('career')
    except Exception:
        _saved_league = None
        _saved_achievements = None
        _saved_career = None

    _html = GAME_HTML.replace("__SAVED_LEAGUE_JSON__", _json.dumps(_saved_league) if _saved_league else "null")
    _html = _html.replace("__SAVED_ACHIEVEMENTS_JSON__", _json.dumps(_saved_achievements) if _saved_achievements else "null")
    _html = _html.replace("__SAVED_CAREER_JSON__", _json.dumps(_saved_career) if _saved_career else "null")
    components.html(_html, height=900, scrolling=False)
