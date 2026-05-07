import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스나이퍼 엘리트 - 전장의 저격수</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--green:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--bg:#060a06;}
html,body{width:100%;height:780px;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100%;height:780px;overflow:hidden;}
canvas{display:block;}
#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,0.82);backdrop-filter:blur(4px);display:flex;justify-content:center;align-items:center;gap:16px;padding:5px 12px;font-size:10px;color:#778;letter-spacing:1px;flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,0.06);}
#ctrl-bar span{color:#aab;}
#ctrl-bar b{color:#f5c518;font-weight:700;}
#hud{position:absolute;top:34px;left:0;right:0;z-index:100;pointer-events:none;display:flex;gap:6px;padding:6px 10px;align-items:center;}
.hb{background:rgba(0,0,0,.65);border:1px solid rgba(255,255,255,.1);border-radius:7px;padding:4px 10px;text-align:center;min-width:54px;}
.hv{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:900;color:var(--gold);}
.hl{font-size:9px;color:#556;letter-spacing:.5px;}
#battle-bar-wrap{flex:1;margin:0 8px;}
#battle-label{display:flex;justify-content:space-between;font-size:9px;color:#556;margin-bottom:3px;}
#battle-bg{height:10px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;position:relative;}
#ally-fill{height:100%;background:linear-gradient(90deg,#1155ff,#3399ff);transition:width .3s;}
#enemy-fill{position:absolute;top:0;right:0;height:100%;background:linear-gradient(270deg,#ff2244,#ff6600);transition:width .3s;}
#scope-wrap{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-bg{position:absolute;inset:0;background:rgba(0,0,0,.94);}
#scope-lens{position:absolute;border-radius:50%;overflow:hidden;left:50%;top:50%;transform:translate(-50%,-50%);border:3px solid rgba(0,255,100,.4);box-shadow:0 0 0 2000px rgba(0,0,0,.94),0 0 30px rgba(0,255,100,.3);width:300px;height:300px;}
#scope-cv{display:block;width:300px;height:300px;}
#scope-cross{position:absolute;inset:0;pointer-events:none;}
#scope-info{position:absolute;bottom:18%;left:50%;transform:translateX(-50%);font-family:'Rajdhani',sans-serif;font-size:11px;color:#0f9;letter-spacing:2px;text-align:center;}
#breath-bar{position:absolute;bottom:14%;left:50%;transform:translateX(-50%);width:180px;}
#breath-bg{height:5px;background:rgba(255,255,255,.1);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:#00ff88;transition:width .05s;}
#warning{position:absolute;inset:0;z-index:200;pointer-events:none;border:4px solid transparent;}
#warning.show{border:4px solid rgba(255,0,50,.7);box-shadow:inset 0 0 70px rgba(255,0,50,.3);}
#toast{position:absolute;top:52px;left:50%;transform:translateX(-50%) translateY(-80px);background:rgba(10,20,5,.97);border:1px solid rgba(245,197,24,.4);border-radius:6px;padding:7px 18px;z-index:280;pointer-events:none;transition:transform .25s;white-space:nowrap;font-size:11px;color:var(--gold);letter-spacing:1px;}
#toast.show{transform:translateX(-50%) translateY(0);}
#killfeed{position:absolute;top:60px;right:10px;z-index:200;pointer-events:none;display:flex;flex-direction:column;gap:3px;}
.kf{background:rgba(0,0,0,.75);border-left:3px solid var(--red);border-radius:3px;padding:3px 9px;font-size:10px;color:#ccc;animation:kfIn .3s ease;}
@keyframes kfIn{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}
#ally-status{position:absolute;bottom:8px;left:10px;z-index:100;pointer-events:none;font-size:10px;color:#4488ff;font-family:'Rajdhani',sans-serif;letter-spacing:.5px;}
#mission-ov{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.93);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;}
.mo-title{font-family:'Black Han Sans',sans-serif;font-size:2.4rem;color:var(--gold);letter-spacing:8px;text-shadow:0 0 30px rgba(245,197,24,.5);margin-bottom:6px;}
.mo-sub{font-size:.73rem;color:#334;letter-spacing:4px;margin-bottom:24px;}
.mission-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;max-width:560px;margin-bottom:20px;}
.mis-card{background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:14px 10px;cursor:pointer;transition:all .2s;text-align:center;}
.mis-card:hover,.mis-card.sel{border-color:rgba(245,197,24,.6);background:rgba(245,197,24,.05);}
.mis-card.locked{opacity:.3;cursor:default;}
.mc-num{font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:var(--gold);}
.mc-name{font-family:'Black Han Sans',sans-serif;font-size:11px;color:#aab;margin:4px 0 2px;}
.mc-diff{font-size:9px;color:#445;}
.mc-clr{font-size:9px;color:#0f9;margin-top:3px;}
.mo-start{padding:12px 48px;background:linear-gradient(135deg,#1a3a00,#2a6600);border:1px solid #4a9a00;border-radius:6px;color:#88ff44;font-family:'Black Han Sans',sans-serif;font-size:14px;letter-spacing:4px;cursor:pointer;transition:all .2s;}
.mo-start:hover{transform:scale(1.05);filter:brightness(1.2);}
.mo-start:disabled{opacity:.3;cursor:default;transform:none;}
#result-ov{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.9);display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;letter-spacing:6px;}
.res-stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:16px 22px;min-width:320px;}
.rs{font-size:11px;color:#556;display:flex;justify-content:space-between;gap:16px;}
.rs b{color:var(--gold);}
.res-btns{display:flex;gap:10px;}
.rbtn{padding:9px 28px;border:none;border-radius:5px;cursor:pointer;font-family:'Black Han Sans',sans-serif;font-size:13px;letter-spacing:2px;transition:all .18s;}
.rbtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.rbtn.retry{background:linear-gradient(135deg,#1a3a00,#2a6600);color:#88ff44;border:1px solid #4a9a00;}
.rbtn.back{background:rgba(255,255,255,.06);color:#666;border:1px solid rgba(255,255,255,.1);}
.dnum{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dUp .9s ease forwards;z-index:300;text-shadow:1px 1px 4px rgba(0,0,0,.9);}
@keyframes dUp{0%{opacity:1;transform:translateY(0) scale(1);}50%{opacity:1;transform:translateY(-30px) scale(1.1);}100%{opacity:0;transform:translateY(-60px) scale(.7);}}
</style>
</head>
<body>
<div id="root">
<canvas id="gc"></canvas>
<div id="ctrl-bar">
  <span><b>마우스</b> 조준</span><span>|</span>
  <span><b>클릭/SPACE</b> 발사</span><span>|</span>
  <span><b>Z/우클릭</b> 스코프</span><span>|</span>
  <span><b>R</b> 재장전</span><span>|</span>
  <span><b>SHIFT</b> 숨참기</span>
</div>
<div id="hud">
  <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
  <div class="hb"><div class="hv" id="kill-v">0</div><div class="hl">킬</div></div>
  <div class="hb"><div class="hv" id="timer-v">--:--</div><div class="hl">TIME</div></div>
  <div class="hb"><div class="hv" id="ammo-v">5/5</div><div class="hl">탄약</div></div>
  <div id="battle-bar-wrap">
    <div id="battle-label"><span>🔵 아군</span><span>적군 🔴</span></div>
    <div id="battle-bg">
      <div id="ally-fill" style="width:50%"></div>
      <div id="enemy-fill" style="width:50%"></div>
    </div>
  </div>
</div>
<div id="scope-wrap">
  <div id="scope-bg"></div>
  <div id="scope-lens"><canvas id="scope-cv"></canvas></div>
  <svg id="scope-cross" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg"
    style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:300px;height:300px;pointer-events:none;">
    <circle cx="150" cy="150" r="148" stroke="rgba(0,255,100,.4)" stroke-width="1.5" fill="none"/>
    <line x1="0" y1="150" x2="118" y2="150" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="182" y1="150" x2="300" y2="150" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="150" y1="0" x2="150" y2="118" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <line x1="150" y1="182" x2="150" y2="300" stroke="rgba(0,255,100,.8)" stroke-width="1"/>
    <circle cx="150" cy="150" r="3" stroke="rgba(0,255,100,.9)" stroke-width="1" fill="none"/>
    <line x1="115" y1="165" x2="185" y2="165" stroke="rgba(0,255,100,.3)" stroke-width=".8"/>
    <line x1="115" y1="135" x2="185" y2="135" stroke="rgba(0,255,100,.3)" stroke-width=".8"/>
  </svg>
  <div id="scope-info"></div>
  <div id="breath-bar"><div style="font-size:9px;color:#445;margin-bottom:3px;text-align:center;">BREATH</div><div id="breath-bg"><div id="breath-fill" style="width:100%"></div></div></div>
</div>
<div id="warning"></div>
<div id="toast"></div>
<div id="killfeed"></div>
<div id="ally-status"></div>
<div id="mission-ov">
  <div class="mo-title">🎯 스나이퍼 엘리트</div>
  <div class="mo-sub">전장의 저격수 — WAR SNIPER</div>
  <div class="mission-grid" id="mission-grid"></div>
  <button class="mo-start" id="mo-start-btn" disabled onclick="startMission()">임무 시작 ▶</button>
</div>
<div id="result-ov">
  <div class="res-title" id="res-title"></div>
  <div class="res-stats" id="res-stats"></div>
  <div class="res-btns">
    <button class="rbtn retry" onclick="retryMission()">재시도 ↺</button>
    <button class="rbtn back" onclick="gotoTitle()">타이틀</button>
  </div>
</div>
</div>
<script>
'use strict';
const canvas=document.getElementById('gc'),ctx=canvas.getContext('2d');
const scopeCV=document.getElementById('scope-cv'),sCtx=scopeCV.getContext('2d');
const GW=900,GH=640;
canvas.width=GW;canvas.height=GH;

let G=null,selMis=null,RAF,lastTs=0,timer=0;

const MISSIONS=[
  {id:1,name:'전선 사수',diff:'⭐ 초급',timeLimit:90,killGoal:15,bossGoal:0,allyHPMin:50,
   desc:'적군 15명을 제거해 전선을 사수하라.',reward:5000000,
   spawns:[{t:'infantry',n:15}]},
  {id:2,name:'지휘관 암살',diff:'⭐⭐ 보통',timeLimit:120,killGoal:10,bossGoal:1,allyHPMin:30,
   desc:'적 지휘관 1명과 경호원들을 처치하라.',reward:15000000,
   spawns:[{t:'infantry',n:8},{t:'commander',n:1},{t:'guard',n:5}]},
  {id:3,name:'포병 무력화',diff:'⭐⭐⭐ 어려움',timeLimit:150,killGoal:20,bossGoal:2,allyHPMin:40,
   desc:'포병 파괴 및 적 장교 2명 제거.',reward:30000000,
   spawns:[{t:'artillery',n:3},{t:'officer',n:2},{t:'infantry',n:15},{t:'guard',n:5}]},
  {id:4,name:'포위 돌파',diff:'⭐⭐⭐⭐ 전문가',timeLimit:180,killGoal:40,bossGoal:3,allyHPMin:20,
   desc:'포위된 아군을 구출하기 위해 사방의 적을 제거하라.',reward:60000000,
   spawns:[{t:'infantry',n:25},{t:'officer',n:3},{t:'sniper_e',n:2},{t:'guard',n:10}]},
  {id:5,name:'총사령관 처치',diff:'⭐⭐⭐⭐⭐ 전설',timeLimit:240,killGoal:30,bossGoal:1,allyHPMin:10,
   desc:'최정예 경호대를 돌파하고 적 총사령관을 처치하라.',reward:200000000,
   spawns:[{t:'infantry',n:15},{t:'guard',n:10},{t:'sniper_e',n:3},{t:'general',n:1}]},
  {id:6,name:'야간 특수작전',diff:'⭐⭐⭐⭐⭐ 전설+',timeLimit:300,killGoal:60,bossGoal:4,allyHPMin:5,
   desc:'야음을 틈타 전략 목표를 모두 제거하라.',reward:500000000,
   spawns:[{t:'infantry',n:25},{t:'guard',n:15},{t:'officer',n:5},{t:'sniper_e',n:4},{t:'commander',n:3},{t:'general',n:1}],night:true},
];

const ETYPES={
  infantry:  {name:'보병',hp:100,col:'#cc2200',sz:8,spd:0.9,xp:100,boss:false,icon:'🪖'},
  guard:     {name:'경호원',hp:150,col:'#991100',sz:9,spd:1.2,xp:180,boss:false,icon:'🔴'},
  officer:   {name:'장교',hp:220,col:'#880000',sz:11,spd:0.8,xp:400,boss:true,icon:'⭐'},
  commander: {name:'지휘관',hp:400,col:'#550000',sz:14,spd:0.6,xp:800,boss:true,icon:'🎖️'},
  general:   {name:'총사령관',hp:700,col:'#330000',sz:17,spd:0.5,xp:3000,boss:true,icon:'🏅'},
  artillery: {name:'포병',hp:450,col:'#7a4500',sz:20,spd:0,xp:600,boss:true,icon:'💣'},
  sniper_e:  {name:'적저격수',hp:120,col:'#003322',sz:8,spd:0.4,xp:500,boss:true,icon:'🎯'},
};

function initGame(midx){
  const mis=MISSIONS[midx];
  G={
    midx,mis,phase:'play',
    time:mis.timeLimit,score:0,kills:0,bossKills:0,
    allyHP:100,allyPower:50,
    enemies:[],allies:[],bullets:[],explosions:[],
    scoped:false,mouse:{x:GW/2,y:GH/2},
    swayX:0,swayY:0,swayT:0,
    breathHeld:false,breathTimer:3,
    reloading:false,reloadTimer:0,
    ammo:5,maxAmmo:5,shootCd:0,
    spawnQueue:buildQueue(mis),spawnTimer:0,
    artilleryActive:0,sniperWarning:0,
    allyWarnTimer:0,frame:0,
    done:false,
  };
  for(let i=0;i<12;i++) spawnAlly();
  updateHUD();
}

function buildQueue(mis){
  const q=[];let d=2;
  for(const s of mis.spawns){
    for(let i=0;i<s.n;i++){
      q.push({t:s.t,delay:d+i*(1.2+Math.random()*0.8)});
    }
    d+=s.n*1.2+4;
  }
  q.sort((a,b)=>a.delay-b.delay);
  return q;
}

function spawnAlly(){
  const y=120+Math.random()*(GH-220);
  G.allies.push({x:40+Math.random()*80,y,vx:0.3+Math.random()*0.3,phase:Math.random()*Math.PI*2,atkT:0.5+Math.random()});
}

function spawnEnemy(type){
  const t=ETYPES[type];const sc=1+G.midx*0.2;
  const y=120+Math.random()*(GH-200);
  const x=GW+30+Math.random()*60;
  G.enemies.push({
    type,x,y,vx:-(t.spd*(0.7+Math.random()*0.5)),vy:(Math.random()-0.5)*0.3,
    hp:Math.round(t.hp*sc),maxHp:Math.round(t.hp*sc),
    col:t.col,sz:t.sz,xp:Math.round(t.xp*sc),boss:t.boss,
    icon:t.icon,name:t.name,
    alive:true,dying:false,deathT:0,
    phase:Math.random()*Math.PI*2,
    atkT:1+Math.random()*2,
    fireT:type==='sniper_e'?3+Math.random()*5:0,
    special:type,
  });
}

function tick(dt){
  if(!G||G.phase!=='play'||G.done)return;
  G.frame++;timer+=dt;G.time-=dt;
  G.swayT+=dt;
  const swayMult=G.breathHeld?0.08:1;
  G.swayX=Math.sin(G.swayT*0.9)*5*swayMult+Math.sin(G.swayT*2.3)*2*swayMult;
  G.swayY=Math.cos(G.swayT*0.7)*4*swayMult+Math.cos(G.swayT*1.8)*2*swayMult;
  G.shootCd=Math.max(0,G.shootCd-dt);
  if(G.breathHeld){G.breathTimer-=dt*0.4;if(G.breathTimer<=0){G.breathHeld=false;G.breathTimer=0;}}
  else G.breathTimer=Math.min(3,G.breathTimer+dt*0.55);
  if(G.reloading){G.reloadTimer-=dt;if(G.reloadTimer<=0){G.reloading=false;G.ammo=G.maxAmmo;showToast('탄창 장전!');updateHUD();}}
  if(G.sniperWarning>0){G.sniperWarning-=dt;document.getElementById('warning').className=G.sniperWarning>0?'show':'';}
  if(G.artilleryActive>0){G.artilleryActive-=dt;G.allyHP-=dt*8;}
  // Spawn
  G.spawnTimer+=dt;
  while(G.spawnQueue.length&&G.spawnQueue[0].delay<=G.spawnTimer){spawnEnemy(G.spawnQueue.shift().t);}
  // Update
  updEnemies(dt);updAllies(dt);updBullets(dt);
  // Battle ratio
  const ae=G.enemies.filter(e=>e.alive).length,aa=G.allies.length;
  const r=aa/Math.max(1,aa+ae);G.allyPower+=(r*100-G.allyPower)*dt*0.08;
  G.allyHP=Math.max(0,Math.min(100,G.allyHP));
  // Ally warn
  if(G.allyHP<30){G.allyWarnTimer-=dt;if(G.allyWarnTimer<=0){G.allyWarnTimer=3;showToast('⚠️ 아군 위험!');}}
  updateHUD();checkEnd();
}

function updEnemies(dt){
  for(let i=G.enemies.length-1;i>=0;i--){
    const e=G.enemies[i];
    if(e.dying){e.deathT+=dt;if(e.deathT>0.7)G.enemies.splice(i,1);continue;}
    if(!e.alive)continue;
    e.phase+=dt*2;
    if(e.special!=='artillery'){e.x+=e.vx;e.y=Math.max(100,Math.min(GH-50,e.y+e.vy+Math.sin(e.phase)*0.25));}
    if(e.x<80){
      G.allyHP-=dt*10;e.vx=0;
      e.atkT-=dt;
      if(e.atkT<=0){e.atkT=0.8+Math.random();G.allyHP-=4+Math.random()*4;
        if(G.allies.length>0&&Math.random()<0.3)G.allies.splice(Math.floor(Math.random()*G.allies.length),1);}
    }
    if(e.special==='artillery'){
      e.atkT-=dt;if(e.atkT<=0){e.atkT=5+Math.random()*4;G.artilleryActive=2;showKF('💥 포격!','#ff7700');}}
    if(e.special==='sniper_e'){
      e.fireT-=dt;if(e.fireT<=0&&e.x<GW-60){e.fireT=4+Math.random()*5;
        G.sniperWarning=1.5;G.allyHP-=2;showKF('⚠️ 적 저격수 공격!','#ff4400');}}
  }
}

function updAllies(dt){
  if(G.frame%300===0&&G.allies.length<14&&G.allyHP>25)spawnAlly();
  for(const a of G.allies){
    a.phase+=dt*2;
    const ne=G.enemies.filter(e=>e.alive).sort((a,b)=>a.x-b.x)[0];
    if(ne){
      const dx=ne.x-a.x,dy=ne.y-a.y,d=Math.hypot(dx,dy);
      if(d>60){a.x+=(dx/d)*a.vx;a.y+=(dy/d)*a.vx;}
      else{a.atkT-=dt;if(a.atkT<=0){a.atkT=0.6+Math.random();ne.hp-=6+Math.random()*4;if(ne.hp<=0)killE(ne,false);}}
    } else {a.x=Math.min(a.x+a.vx*0.3,GW-100);}
    a.y=Math.max(100,Math.min(GH-50,a.y+Math.sin(a.phase)*0.2));
  }
}

function updBullets(dt){
  for(let i=G.bullets.length-1;i>=0;i--){
    const b=G.bullets[i];b.x+=b.vx*dt*60;b.y+=b.vy*dt*60;b.life-=dt;
    if(b.life<=0||b.x<0||b.x>GW||b.y<0||b.y>GH){G.bullets.splice(i,1);continue;}
    let hit=false;
    for(const e of G.enemies){
      if(!e.alive)continue;
      if(Math.hypot(e.x-b.x,e.y-b.y)<e.sz+4){
        e.hp-=b.dmg;spawnDN(e.x,e.y,b.dmg,b.crit);
        addExp(e.x,e.y,b.crit?'#ffff44':'#ff8844');
        if(e.hp<=0)killE(e,true);
        G.bullets.splice(i,1);hit=true;break;
      }
    }
    if(hit)continue;
  }
}

function killE(e,byPlayer){
  if(!e.alive)return;
  e.alive=false;e.dying=true;e.deathT=0;
  addExp(e.x,e.y,e.col);
  if(byPlayer){
    G.kills++;G.score+=e.xp;
    if(e.boss){G.bossKills++;showToast(`🏆 ${e.name} 처치! +${e.xp.toLocaleString()}XP`);showKF(`🏆 ${e.icon} ${e.name} 처치!`,'#f5c518');}
    else showKF(`${e.icon} ${e.name} +${e.xp}`,'#ccc');
    if(e.special==='artillery'){G.artilleryActive=0;showToast('💣 포병 파괴!');}
  }
}

function addExp(x,y,col){G.explosions.push({x,y,col,r:3,lr:1.8,life:0.4});}

function fire(){
  if(!G||G.phase!=='play'||G.done)return;
  if(G.reloading||G.shootCd>0)return;
  if(G.ammo<=0){startReload();return;}
  G.ammo--;G.shootCd=0.9;updateHUD();
  const crit=Math.random()<0.15;
  let wx=G.mouse.x,wy=G.mouse.y;
  if(G.scoped){const z=3.5;wx=G.mouse.x+(150-150)/z;wy=G.mouse.y+(150-150)/z;}
  const sw=G.breathHeld?0.3:3;
  wx+=(Math.random()-0.5)*sw*2+G.swayX*0.3;
  wy+=(Math.random()-0.5)*sw*2+G.swayY*0.3;
  const ang=Math.atan2(wy-(GH-50),wx-50);
  G.bullets.push({x:50,y:GH-50,vx:Math.cos(ang)*900,vy:Math.sin(ang)*900,
    dmg:85*(crit?2.5:1),crit,life:2});
  addExp(50,GH-50,'#ffffaa');sfx_shoot();
  if(G.ammo===0)setTimeout(startReload,300);
}

function startReload(){
  if(G.reloading||G.ammo===G.maxAmmo)return;
  G.reloading=true;G.reloadTimer=2.2;showToast('재장전 중...');
}

function checkEnd(){
  if(G.done)return;
  const mis=G.mis;
  if(G.time<=0||G.allyHP<=0){G.done=true;showResult(false);return;}
  const bossRem=G.enemies.filter(e=>e.alive&&e.boss).length;
  const allBossesSpawned=G.spawnQueue.filter(s=>ETYPES[s.t]?.boss).length===0;
  let won=G.kills>=mis.killGoal&&(mis.bossGoal===0||G.bossKills>=mis.bossGoal);
  if(won&&allBossesSpawned&&bossRem===0){G.done=true;showResult(true);}
}

function showResult(win){
  G.phase='result';if(G.scoped)toggleScope();
  const el=document.getElementById('result-ov');
  const t=document.getElementById('res-title');
  t.textContent=win?'🏆 임무 완료!':'💀 임무 실패';
  t.style.color=win?'#f5c518':'#ff2244';
  const elapsed=G.mis.timeLimit-G.time;
  document.getElementById('res-stats').innerHTML=`
    <div class="rs">킬<b>${G.kills}</b></div>
    <div class="rs">점수<b>${Math.round(G.score).toLocaleString()}</b></div>
    <div class="rs">경과시간<b>${Math.floor(elapsed/60)}m ${Math.floor(elapsed%60)}s</b></div>
    <div class="rs">아군HP<b>${Math.round(G.allyHP)}%</b></div>
    <div class="rs">보스처치<b>${G.bossKills}</b></div>
    <div class="rs">등급<b>${grade()}</b></div>`;
  el.style.display='flex';
  if(win){
    const cl=JSON.parse(localStorage.getItem('sniper_clears')||'[]');
    if(!cl.includes(G.midx))cl.push(G.midx);
    localStorage.setItem('sniper_clears',JSON.stringify(cl));
    sfx_win();
    try{window.parent.postMessage({type:'sniper_result',score:Math.round(G.score),grade:grade()},'*');}catch(e){}
  }else sfx_fail();
}

function grade(){const s=G.score;if(s>=50000)return'S';if(s>=30000)return'A';if(s>=15000)return'B';return'C';}
function retryMission(){document.getElementById('result-ov').style.display='none';initGame(G.midx);}
function gotoTitle(){document.getElementById('result-ov').style.display='none';G=null;buildTitle();document.getElementById('mission-ov').style.display='flex';}
function toggleScope(){G.scoped=!G.scoped;document.getElementById('scope-wrap').style.display=G.scoped?'block':'none';}

// ── DRAW ──────────────────────────────────────────────────
function drawScene(c){
  // Sky
  const sky=c.createLinearGradient(0,0,0,GH*0.5);
  sky.addColorStop(0,'#1a2a3a');sky.addColorStop(1,'#2a3a2a');
  c.fillStyle=sky;c.fillRect(0,0,GW,GH);
  // Ground
  const gnd=c.createLinearGradient(0,GH*0.3,0,GH);
  gnd.addColorStop(0,'#2a4a1a');gnd.addColorStop(1,'#1a3a0a');
  c.fillStyle=gnd;c.fillRect(0,GH*0.3,GW,GH);
  drawTerrain(c);
  // Explosions
  if(G)for(const ex of G.explosions){
    const a=ex.life/0.4;c.save();c.globalAlpha=a*0.55;
    c.fillStyle=ex.col;c.shadowColor=ex.col;c.shadowBlur=14;
    c.beginPath();c.arc(ex.x,ex.y,ex.r*2,0,Math.PI*2);c.fill();
    c.shadowBlur=0;c.restore();ex.life-=0.016;ex.r+=ex.lr;
  }
  if(G)G.explosions=G.explosions.filter(e=>e.life>0);
  // Allies
  if(G)for(const a of G.allies){
    const bob=Math.sin(a.phase)*2;c.save();c.translate(a.x,a.y+bob);
    c.fillStyle='#2255cc';c.beginPath();c.arc(0,0,6,0,Math.PI*2);c.fill();
    c.fillStyle='#4488ff';c.beginPath();c.arc(0,-8,4,0,Math.PI*2);c.fill();
    c.restore();
  }
  // Enemies
  if(G)for(const e of G.enemies){
    if(!e.alive&&!e.dying)continue;
    const a=e.dying?Math.max(0,1-e.deathT/0.7):1;
    c.save();c.globalAlpha=a;c.translate(e.x,e.y+Math.sin(e.phase)*2);
    if(e.boss){c.shadowColor=e.special==='general'?'#ff0000':'#ff4400';c.shadowBlur=18;}
    c.fillStyle=e.col;c.beginPath();c.arc(0,0,e.sz,0,Math.PI*2);c.fill();
    c.shadowBlur=0;
    // Artillery special shape
    if(e.special==='artillery'){
      c.fillStyle='#ff7700';c.fillRect(-12,-5,24,10);
      c.fillStyle='#ffaa00';c.fillRect(-3,-14,6,14);
    }
    // Icon for bosses
    if(e.boss&&e.sz>=11){c.font=`${e.sz}px serif`;c.textAlign='center';c.textBaseline='middle';c.fillText(e.icon,0,0);}
    // HP bar
    if(!e.dying&&e.hp<e.maxHp){
      const bw=e.sz*3,pct=Math.max(0,e.hp/e.maxHp);
      c.fillStyle='rgba(0,0,0,.7)';c.fillRect(-bw/2,-e.sz-10,bw,5);
      c.fillStyle=pct>0.5?'#22cc44':pct>0.25?'#ccaa00':'#cc2200';
      c.fillRect(-bw/2,-e.sz-10,bw*pct,5);
    }
    c.restore();
  }
  // Bullets
  if(G)for(const b of G.bullets){
    c.save();c.fillStyle='#ffff88';c.shadowColor='#ffff88';c.shadowBlur=8;
    c.beginPath();c.arc(b.x,b.y,3,0,Math.PI*2);c.fill();c.shadowBlur=0;c.restore();
  }
  // Player sniper position
  c.save();c.translate(50,GH-50);
  c.fillStyle='rgba(0,255,100,0.15)';c.beginPath();c.arc(0,0,16,0,Math.PI*2);c.fill();
  c.font='18px serif';c.textAlign='center';c.textBaseline='middle';c.fillText('🎯',0,0);
  c.restore();
  // Aim line when scoped
  if(G&&G.scoped){
    c.save();c.strokeStyle='rgba(0,255,100,0.1)';c.lineWidth=1;c.setLineDash([4,8]);
    c.beginPath();c.moveTo(50,GH-50);c.lineTo(G.mouse.x,G.mouse.y);c.stroke();c.restore();
  }
  // Artillery warning
  if(G&&G.artilleryActive>0){
    c.save();c.globalAlpha=0.3+Math.sin(timer*8)*0.25;c.fillStyle='#ff7700';
    c.font='bold 15px Orbitron';c.textAlign='center';
    c.fillText('⚠️ 포격중!',GW/2,72);c.restore();
  }
}

function drawTerrain(c){
  // Allied trench (left)
  c.fillStyle='#1a2a0a';c.fillRect(15,90,90,GH-160);
  // Enemy area (right)
  c.fillStyle='#2a1a0a';c.fillRect(GW-110,90,110,GH-160);
  // Cover/trees
  const trees=[[200,160],[360,260],[510,190],[620,360],[720,210],[760,300],[410,420],[560,460]];
  for(const[x,y]of trees){
    c.fillStyle='#1a4a0a';c.beginPath();c.arc(x,y,18,0,Math.PI*2);c.fill();
    c.fillStyle='#2a6a1a';c.beginPath();c.arc(x,y-8,13,0,Math.PI*2);c.fill();
  }
  // Craters
  const craters=[[300,320],[520,310],[660,290]];
  for(const[x,y]of craters){
    c.fillStyle='#0a1a00';c.beginPath();c.ellipse(x,y,28,16,0,0,Math.PI*2);c.fill();
    c.strokeStyle='#1a2a00';c.lineWidth=2;c.beginPath();c.ellipse(x,y,28,16,0,0,Math.PI*2);c.stroke();
  }
  // Horizon line
  c.strokeStyle='rgba(100,120,80,0.3)';c.lineWidth=2;c.beginPath();c.moveTo(0,GH*0.3);c.lineTo(GW,GH*0.3);c.stroke();
}

function drawScopeView(){
  if(!G||!G.scoped)return;
  const zoom=3.5;const cx=G.mouse.x,cy=G.mouse.y;
  sCtx.save();
  sCtx.fillStyle='#0a1a00';sCtx.fillRect(0,0,300,300);
  sCtx.scale(zoom,zoom);
  sCtx.translate(150/zoom-cx+G.swayX*0.3,150/zoom-cy+G.swayY*0.3);
  drawScene(sCtx);
  sCtx.restore();
  // Scope info
  const dist=Math.round(Math.hypot(G.mouse.x-50,G.mouse.y-(GH-50)));
  document.getElementById('scope-info').textContent=
    `${dist}m | ${G.breathHeld?'숨참기 ✓':'안정화 필요'} | ${G.ammo}/${G.maxAmmo}`;
  document.getElementById('breath-fill').style.width=(G.breathTimer/3*100)+'%';
}

function updateHUD(){
  if(!G)return;
  document.getElementById('score-v').textContent=Math.round(G.score).toLocaleString();
  document.getElementById('kill-v').textContent=G.kills;
  const t=Math.max(0,G.time);
  document.getElementById('timer-v').textContent=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  document.getElementById('ammo-v').textContent=G.reloading?'장전...':`${G.ammo}/${G.maxAmmo}`;
  document.getElementById('ally-fill').style.width=G.allyPower+'%';
  document.getElementById('enemy-fill').style.width=(100-G.allyPower)+'%';
  document.getElementById('ally-status').textContent=
    `🔵 아군HP ${Math.round(G.allyHP)}% | 잔여적 ${G.enemies.filter(e=>e.alive).length} | 킬 ${G.kills}/${G.mis.killGoal} | 지휘부 ${G.bossKills}/${G.mis.bossGoal}`;
}

function spawnDN(x,y,v,crit){
  const el=document.createElement('div');el.className='dnum';
  const r=canvas.getBoundingClientRect();
  el.style.cssText=`left:${r.left+x-20}px;top:${r.top+y}px;font-size:${crit?22:14}px;color:${crit?'#ffff44':'#fff'};`;
  el.textContent=crit?`${Math.round(v)}!!`:`${Math.round(v)}`;
  document.body.appendChild(el);setTimeout(()=>el.remove(),950);
}

function showToast(msg){
  const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2000);
}

function showKF(msg,col){
  const kf=document.getElementById('killfeed');
  const it=document.createElement('div');it.className='kf';it.style.color=col||'#ccc';it.textContent=msg;
  kf.appendChild(it);
  setTimeout(()=>{it.style.opacity='0';setTimeout(()=>it.remove(),600);},2500);
  while(kf.children.length>5)kf.removeChild(kf.firstChild);
}

// Audio
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function beep(f,t,d,v=.2,delay=0){if(!ACtx)return;try{
  const o=ACtx.createOscillator(),g=ACtx.createGain();o.connect(g);g.connect(ACtx.destination);
  o.type=t;o.frequency.value=f;const ts=ACtx.currentTime+delay;
  g.gain.setValueAtTime(0,ts);g.gain.linearRampToValueAtTime(v,ts+.005);g.gain.exponentialRampToValueAtTime(.001,ts+d);
  o.start(ts);o.stop(ts+d+.05);}catch(e){}}
function sfx_shoot(){ensureAudio();beep(180,'sawtooth',.12,.4);beep(90,'sine',.18,.3,.06);}
function sfx_win(){ensureAudio();[523,659,784,1047].forEach((f,i)=>beep(f,'sine',.3,.35,i*.12));}
function sfx_fail(){ensureAudio();[300,200,150].forEach((f,i)=>beep(f,'sawtooth',.3,.3,i*.15));}

// Build title
function buildTitle(){
  const cleared=JSON.parse(localStorage.getItem('sniper_clears')||'[]');
  const grid=document.getElementById('mission-grid');
  grid.innerHTML='';
  MISSIONS.forEach((m,i)=>{
    const locked=i>0&&!cleared.includes(i-1);
    const div=document.createElement('div');
    div.className='mis-card'+(locked?' locked':'');
    div.innerHTML=`<div class="mc-num">${i+1}</div><div class="mc-name">${m.name}</div><div class="mc-diff">${m.diff}</div>${cleared.includes(i)?'<div class="mc-clr">✅ 완료</div>':''}`;
    if(!locked){div.onclick=()=>{selMis=i;document.querySelectorAll('.mis-card').forEach(x=>x.classList.remove('sel'));div.classList.add('sel');document.getElementById('mo-start-btn').disabled=false;ensureAudio();};}
    grid.appendChild(div);
  });
}

function startMission(){
  if(selMis===null)return;
  document.getElementById('mission-ov').style.display='none';
  initGame(selMis);
}

// Input
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  if(G){G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;}
});
canvas.addEventListener('click',e=>{if(G&&G.phase==='play'){ensureAudio();fire();}});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G&&G.phase==='play')toggleScope();});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift'&&G)G.breathHeld=true;
  if(e.key===' '){e.preventDefault();if(G&&G.phase==='play'){ensureAudio();fire();}}
  if((e.key==='r'||e.key==='R')&&G&&G.phase==='play')startReload();
  if((e.key==='z'||e.key==='Z'||e.key==='Escape')&&G&&G.phase==='play')toggleScope();
});
document.addEventListener('keyup',e=>{if(e.key==='Shift'&&G)G.breathHeld=false;});

// Main loop
function loop(ts){
  const dt=Math.min((ts-lastTs)/1000,0.05);lastTs=ts;timer+=dt;
  ctx.clearRect(0,0,GW,GH);
  if(G&&G.phase==='play'){tick(dt);drawScene(ctx);drawScopeView();}
  else{ctx.fillStyle='#060a06';ctx.fillRect(0,0,GW,GH);}
  RAF=requestAnimationFrame(loop);
}

buildTitle();
RAF=requestAnimationFrame(loop);
</script>
</body>
</html>"""

def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import load_db, save_db
    from utils.config import USERS_FILE

    qp = st.query_params
    if qp.get('sniper_score'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            s_score = int(qp.get('sniper_score', 0))
            s_grade = qp.get('sniper_grade', '')
            if uid and s_score > 0:
                _users = load_db(USERS_FILE, {})
                cur_rec = _users.get(uid, {}).get('game_records', st.session_state.get('game_records', {}))
                if s_score > cur_rec.get('sniper', {}).get('score', 0):
                    cur_rec.setdefault('sniper', {}).update({'score': s_score, 'grade': s_grade})
                    st.session_state.game_records = cur_rec
                    if uid in _users:
                        _users[uid]['game_records'] = cur_rec
                        save_db(USERS_FILE, _users)
                    sync_user_data()
                    st.toast(f"🏆 스나이퍼 최고기록 갱신! {s_score:,}점 ({s_grade}등급)", icon="🎯")
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <div style='background:linear-gradient(135deg,#060a06,#0c1a0c);border:1px solid rgba(0,255,100,0.2);
      border-radius:16px;padding:16px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>
      <div style='font-size:2rem;'>🎯</div>
      <div>
        <div style='font-family:"Black Han Sans",sans-serif;font-size:1.1rem;color:#e8ffe8;'>🎯 스나이퍼 엘리트 — 전장의 저격수</div>
        <div style='font-size:0.82rem;color:#6a9a6a;margin-top:2px;'>대규모 전쟁에서 아군을 지원하는 엘리트 저격수! 6가지 작전 미션 도전!</div>
        <div style='font-size:0.76rem;color:#4a7a4a;margin-top:4px;'>🖱️ 클릭/SPACE: 발사 | 우클릭/Z: 스코프 | R: 재장전 | SHIFT: 숨참기</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)

    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'sniper_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('sniper_score', e.data.score);
        url.searchParams.set('sniper_grade', e.data.grade);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=785, scrolling=False)
