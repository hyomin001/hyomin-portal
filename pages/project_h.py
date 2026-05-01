import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스트리트 파이터 EX</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--blue:#33aaff;--gold:#f5c518;--green:#00ff88;--purple:#c04fff;--cyan:#00d4ff;--orange:#ff7700;--bg:#08030f;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.08);}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100vw;height:100vh;overflow:hidden;display:flex;flex-direction:column;}

/* ── HUD TOP ── */
#hud{display:flex;align-items:center;gap:8px;padding:10px 12px 6px;background:linear-gradient(180deg,rgba(0,0,0,.9)0%,transparent 100%);pointer-events:none;position:relative;z-index:50;}
.hp-col{flex:1;display:flex;flex-direction:column;gap:3px;}
.fn{font-size:9px;letter-spacing:2px;font-weight:700;}
#fn-p1{color:var(--blue);}#fn-p2{color:var(--red);text-align:right;}
.hp-wrap{height:15px;background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.1);border-radius:3px;overflow:hidden;position:relative;}
#hf-p1{height:100%;background:linear-gradient(90deg,#1144ff,#33aaff,#88ddff);border-radius:2px;transition:width .06s linear;transform-origin:left;}
#hf-p2{height:100%;background:linear-gradient(90deg,#ff0022,#ff4444,#ff8866);border-radius:2px;transition:width .06s linear;transform-origin:right;float:right;}
/* HP damage ghost */
.hp-ghost{position:absolute;top:0;right:0;height:100%;background:rgba(255,200,0,.4);transition:width .5s ease;}
#hg-p1{left:0;right:auto;background:rgba(255,200,0,.35);}
#hg-p2{right:0;left:auto;background:rgba(255,200,0,.35);}

/* CENTER */
.center-hud{text-align:center;min-width:86px;flex-shrink:0;}
#rnd-lbl{font-size:8px;color:var(--gold);letter-spacing:3px;font-weight:900;}
#timer{font-family:'Rajdhani',sans-serif;font-size:36px;font-weight:900;color:#fff;line-height:1;}
#timer.low{color:var(--red);animation:timerPulse .5s infinite;}
@keyframes timerPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.1);}}

/* SUPER BARS */
#superbars{display:flex;justify-content:space-between;padding:3px 12px;pointer-events:none;align-items:center;}
.sb-side{display:flex;gap:3px;}
.sseg{width:32px;height:5px;border-radius:1px;background:rgba(255,215,0,.07);border:1px solid rgba(255,215,0,.12);overflow:hidden;transition:all .15s;}
.sfill{height:100%;background:linear-gradient(90deg,#664400,var(--gold),#ffeeaa);border-radius:1px;transition:width .08s;}
.sseg.full .sfill{animation:segPulse .6s infinite;}
@keyframes segPulse{0%,100%{opacity:1;}50%{opacity:.6;}}
#super-lbl{font-size:7px;color:#334;letter-spacing:3px;}

/* WIN DOTS */
#win-row{display:flex;justify-content:space-between;padding:2px 12px;pointer-events:none;}
.wd-group{display:flex;gap:5px;}
.wd{width:11px;height:11px;border-radius:50%;border:1.5px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);}
.wd.p1w{background:var(--blue);box-shadow:0 0 8px rgba(51,170,255,.8);border-color:var(--blue);}
.wd.p2w{background:var(--red);box-shadow:0 0 8px rgba(255,34,68,.8);border-color:var(--red);}

/* CANVAS */
#canvas-wrap{flex:1;position:relative;overflow:hidden;}
#gc{position:absolute;top:0;left:0;width:100%;height:100%;}

/* ROUND RESULT */
#rnd-result{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-size:clamp(30px,7vw,52px);letter-spacing:4px;text-shadow:0 0 30px currentColor;opacity:0;transition:opacity .18s;text-align:center;white-space:nowrap;}

/* COMBO COUNTER */
#combo-display{position:absolute;z-index:150;pointer-events:none;opacity:0;transition:opacity .15s;text-align:left;}
#combo-n{font-family:'Black Han Sans',sans-serif;font-size:clamp(28px,6vw,44px);line-height:1;text-shadow:0 0 20px currentColor;}
#combo-hits{font-size:9px;color:#aaa;letter-spacing:3px;margin-top:2px;}

/* KEYS HINT */
#keys-hint{position:absolute;bottom:130px;left:50%;transform:translateX(-50%);z-index:80;pointer-events:none;display:flex;gap:20px;font-size:8px;color:#334;letter-spacing:1px;text-align:center;white-space:nowrap;}

/* ── DPAD ── */
#dpad{position:absolute;bottom:12px;left:12px;z-index:100;display:grid;grid-template-columns:58px 58px 58px;grid-template-rows:52px 52px;gap:5px;}
.dp{border-radius:11px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;user-select:none;touch-action:none;transition:all .08s;}
.dp:active,.dp.pr{background:rgba(51,170,255,.2);border-color:rgba(51,170,255,.55);box-shadow:0 0 12px rgba(51,170,255,.35);transform:scale(.93);}
#dp-up{grid-column:2;grid-row:1;}#dp-left{grid-column:1;grid-row:2;}#dp-down{grid-column:2;grid-row:2;}#dp-right{grid-column:3;grid-row:2;}

/* ── ATK BUTTONS ── */
#atk-btns{position:absolute;bottom:12px;right:12px;z-index:100;display:grid;grid-template-columns:62px 62px;grid-template-rows:56px 56px;gap:6px;}
.ab{border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;user-select:none;touch-action:none;transition:all .08s;border:2px solid;gap:2px;}
.ab:active,.ab.pr{transform:scale(.9);filter:brightness(1.6);}
#ab-p{background:rgba(255,34,68,.12);border-color:rgba(255,34,68,.45);color:var(--red);font-size:24px;}
#ab-k{background:rgba(245,197,24,.1);border-color:rgba(245,197,24,.4);color:var(--gold);font-size:24px;}
#ab-j{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.4);color:var(--cyan);font-size:24px;}
#ab-s{background:rgba(192,79,255,.12);border-color:rgba(192,79,255,.45);color:var(--purple);font-size:24px;}
.ab-lbl{font-size:7px;letter-spacing:1px;font-weight:700;}

/* ── OVERLAY ── */
#overlay{position:absolute;inset:0;z-index:300;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:30px 22px;background:linear-gradient(160deg,rgba(8,3,15,.98),rgba(14,6,24,.98));border:1px solid rgba(192,79,255,.22);border-radius:20px;min-width:340px;max-width:95vw;max-height:90vh;overflow-y:auto;}
.ov-eye{font-size:7px;letter-spacing:4px;color:var(--purple);background:rgba(192,79,255,.1);border:1px solid rgba(192,79,255,.22);border-radius:99px;padding:3px 12px;display:inline-block;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5.5vw,36px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#334;letter-spacing:4px;margin-bottom:14px;}

/* CHAR SELECT */
.char-select-wrap{margin-bottom:14px;}
.char-select-title{font-size:8px;color:#446;letter-spacing:3px;margin-bottom:8px;}
.char-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;}
.cc{padding:10px 5px;background:var(--glass);border:1.5px solid var(--border);border-radius:12px;cursor:pointer;transition:all .18s;text-align:center;position:relative;}
.cc:hover{border-color:rgba(0,212,255,.35);}
.cc.sel{border-color:var(--blue);background:rgba(51,170,255,.12);box-shadow:0 0 16px rgba(51,170,255,.25);}
.cc-ico{font-size:30px;display:block;margin-bottom:3px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:11px;letter-spacing:1px;}
.cc-type{font-size:7px;color:#446;margin-top:2px;letter-spacing:1px;}
.cc-bars{margin-top:5px;display:flex;flex-direction:column;gap:2px;}
.cc-bar-row{display:flex;align-items:center;gap:3px;}
.cc-bar-lbl{font-size:6px;color:#445;width:18px;}
.cc-bar-bg{flex:1;height:3px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;}
.cc-bar-fill{height:100%;border-radius:99px;}
.cc-badge{position:absolute;top:4px;right:4px;font-size:6px;padding:1px 5px;border-radius:99px;letter-spacing:1px;font-weight:700;}

/* DIFF TABS */
.diff-row{display:flex;gap:6px;justify-content:center;margin-bottom:14px;flex-wrap:wrap;}
.dt{padding:7px 14px;border-radius:99px;background:var(--glass);border:1px solid var(--border);font-size:9px;color:#556;cursor:pointer;transition:all .18s;text-align:center;}
.dt.sel{border-color:var(--gold);color:var(--gold);background:rgba(245,197,24,.08);}

/* STATS */
.stats-row{display:flex;gap:7px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.sc{padding:6px 11px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.sv{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:900;color:#fff;}
.sl{font-size:7px;color:#446;letter-spacing:2px;}
.ov-btn{display:inline-block;padding:12px 30px;background:linear-gradient(135deg,rgba(192,79,255,.22),rgba(108,99,255,.14));border:1px solid rgba(192,79,255,.48);border-radius:12px;font-family:'Black Han Sans',sans-serif;font-size:17px;color:var(--purple);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(192,79,255,.38),rgba(108,99,255,.28));transform:translateY(-2px);box-shadow:0 8px 24px rgba(192,79,255,.3);}
.ov-btn2{display:inline-block;padding:9px 20px;background:var(--glass);border:1px solid var(--border);border-radius:10px;font-family:'Black Han Sans',sans-serif;font-size:12px;color:#556;cursor:pointer;letter-spacing:1px;transition:all .18s;margin-top:8px;}
.ov-btn2:hover{border-color:rgba(255,255,255,.2);color:#888;}

/* SCREEN SHAKE (applied to canvas-wrap) */
@keyframes shake{0%,100%{transform:translate(0,0);}20%{transform:translate(-6px,4px);}40%{transform:translate(6px,-4px);}60%{transform:translate(-4px,2px);}80%{transform:translate(4px,-2px);}}
.shaking{animation:shake .18s ease;}
</style>
</head>
<body>
<div id="root">
  <!-- HUD -->
  <div id="hud">
    <div class="hp-col">
      <div class="fn" id="fn-p1">P1</div>
      <div class="hp-wrap">
        <div id="hg-p1" class="hp-ghost" style="width:100%"></div>
        <div id="hf-p1" style="width:100%"></div>
      </div>
    </div>
    <div class="center-hud">
      <div id="rnd-lbl">ROUND 1</div>
      <div id="timer">99</div>
    </div>
    <div class="hp-col">
      <div class="fn" id="fn-p2" style="text-align:right">CPU</div>
      <div class="hp-wrap">
        <div id="hg-p2" class="hp-ghost" style="width:100%"></div>
        <div id="hf-p2" style="width:100%"></div>
      </div>
    </div>
  </div>
  <div id="superbars">
    <div class="sb-side" id="sb-p1"></div>
    <div id="super-lbl">SUPER</div>
    <div class="sb-side" id="sb-p2"></div>
  </div>
  <div id="win-row">
    <div class="wd-group" id="wd-p1"></div>
    <div class="wd-group" id="wd-p2"></div>
  </div>

  <!-- Canvas -->
  <div id="canvas-wrap">
    <canvas id="gc"></canvas>
    <div id="rnd-result"></div>
    <div id="combo-display"><div id="combo-n">0</div><div id="combo-hits">HIT COMBO</div></div>
  </div>

  <!-- Controls hint -->
  <div id="keys-hint">
    <div>← → 이동 &nbsp;|&nbsp; ↑ / Z 점프</div>
    <div>X/J 펀치 &nbsp;|&nbsp; C/K 킥 &nbsp;|&nbsp; V/L 필살기</div>
    <div>↓ 가드 &nbsp;|&nbsp; X+↓ 하단 공격</div>
  </div>

  <!-- Touch DPAD -->
  <div id="dpad">
    <div class="dp" id="dp-up">⬆</div>
    <div class="dp" id="dp-left">⬅</div>
    <div class="dp" id="dp-down">⬇</div>
    <div class="dp" id="dp-right">➡</div>
  </div>

  <!-- Touch ATK -->
  <div id="atk-btns">
    <div class="ab" id="ab-j"><span>⬆</span><span class="ab-lbl">점프</span></div>
    <div class="ab" id="ab-p"><span>👊</span><span class="ab-lbl">펀치</span></div>
    <div class="ab" id="ab-k"><span>🦵</span><span class="ab-lbl">킥</span></div>
    <div class="ab" id="ab-s"><span>✨</span><span class="ab-lbl">필살기</span></div>
  </div>

  <!-- Overlay -->
  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>

<script>
'use strict';
// ================================================================
//  스트리트 파이터 EX  v3.0
//  진짜 격투 게임 물리 · 6 캐릭터 · 풀 AI 패턴
//  히트스톱 · 화면 흔들림 · 콤보 카운터 · 기절 시스템
//  가드 · 하단 공격 · 공중 공격 · 슈퍼 게이지 · 3선승제
//  필살기 이펙트 · 파티클 · 투명 무적 · 오버드라이브
// ================================================================

const canvas=document.getElementById('gc');
const ctx=canvas.getContext('2d');
const cWrap=document.getElementById('canvas-wrap');

let CW=560,CH=380,SC=1;
function resize(){
  const w=cWrap.clientWidth,h=cWrap.clientHeight;
  SC=Math.min(w/CW,h/CH);
  canvas.width=CW;canvas.height=CH;
  canvas.style.width=(CW*SC)+'px';canvas.style.height=(CH*SC)+'px';
  canvas.style.left=((w-CW*SC)/2)+'px';canvas.style.top=((h-CH*SC)/2)+'px';
}
resize();window.addEventListener('resize',resize);

// ================================================================
//  CHARACTER DATA
// ================================================================
const CHARS=[
  {
    name:'류',emoji:'🥋',hp:220,
    atk:22,def:1.0,spd:4.6,jump:17,
    supCost:25,col:'#33aaff',
    type:'균형형',badge:'표준',badgeCol:'#33aaff',
    desc:'균형잡힌 파이터',
    bars:[75,70,72,68],
    moves:{
      punch:{dmg:22,kbx:4,kby:-2,stun:0,reach:72,low:false,startup:5,active:4,recovery:6},
      kick:  {dmg:32,kbx:6,kby:-3,stun:0,reach:88,low:false,startup:7,active:5,recovery:8},
      heavy: {dmg:42,kbx:8,kby:-5,stun:8,reach:80,low:false,startup:11,active:4,recovery:14},
      low:   {dmg:18,kbx:3,kby:0, stun:0,reach:66,low:true, startup:4,active:4,recovery:5},
      airPunch:{dmg:28,kbx:5,kby:-4,stun:0,reach:68,low:false,startup:4,active:5,recovery:4},
      special:{name:'파동권',emoji:'🌊',dmg:55,kbx:10,kby:-6,stun:12,cost:25,col:'#3399ff',isProjectile:true},
      super:  {name:'승룡권',emoji:'🔥',dmg:110,kbx:6,kby:-14,stun:20,cost:100,col:'#ffaa00',isLauncher:true},
    }
  },
  {
    name:'블레이즈',emoji:'🔥',hp:195,
    atk:30,def:0.9,spd:5.4,jump:15,
    supCost:22,col:'#ff6600',
    type:'공격형',badge:'어택',badgeCol:'#ff4400',
    desc:'폭발적 공격력',
    bars:[100,92,50,42],
    moves:{
      punch:{dmg:28,kbx:5,kby:-2,stun:0,reach:70,low:false,startup:4,active:4,recovery:5},
      kick:  {dmg:38,kbx:7,kby:-3,stun:0,reach:86,low:false,startup:6,active:5,recovery:7},
      heavy: {dmg:50,kbx:10,kby:-5,stun:10,reach:78,low:false,startup:10,active:4,recovery:13},
      low:   {dmg:22,kbx:4,kby:0, stun:0,reach:64,low:true, startup:4,active:4,recovery:5},
      airPunch:{dmg:34,kbx:6,kby:-5,stun:0,reach:66,low:false,startup:4,active:5,recovery:4},
      special:{name:'화염권',emoji:'💥',dmg:65,kbx:12,kby:-4,stun:14,cost:22,col:'#ff6600',isDash:true},
      super:  {name:'인페르노',emoji:'🌋',dmg:130,kbx:8,kby:-10,stun:25,cost:100,col:'#ff3300',isProjectile:true},
    }
  },
  {
    name:'아이스',emoji:'❄️',hp:245,
    atk:18,def:1.3,spd:3.6,jump:19,
    supCost:28,col:'#88ccff',
    type:'수비형',badge:'탱커',badgeCol:'#4488cc',
    desc:'강력한 방어력',
    bars:[58,46,95,90],
    moves:{
      punch:{dmg:20,kbx:3,kby:-1,stun:0,reach:74,low:false,startup:6,active:5,recovery:6},
      kick:  {dmg:30,kbx:5,kby:-3,stun:0,reach:90,low:false,startup:8,active:5,recovery:9},
      heavy: {dmg:40,kbx:7,kby:-4,stun:10,reach:82,low:false,startup:12,active:5,recovery:15},
      low:   {dmg:16,kbx:2,kby:0, stun:0,reach:68,low:true, startup:5,active:4,recovery:5},
      airPunch:{dmg:25,kbx:4,kby:-3,stun:0,reach:70,low:false,startup:5,active:5,recovery:5},
      special:{name:'빙결탄',emoji:'🧊',dmg:45,kbx:6,kby:-2,stun:18,cost:28,col:'#88ddff',isProjectile:true,freeze:true},
      super:  {name:'빙하폭풍',emoji:'❄️',dmg:100,kbx:5,kby:-8,stun:30,cost:100,col:'#aaeeff',isFreeze:true},
    }
  },
  {
    name:'라이트닝',emoji:'⚡',hp:175,
    atk:26,def:0.85,spd:6.8,jump:21,
    supCost:20,col:'#f5c518',
    type:'스피드형',badge:'스피드',badgeCol:'#cc9900',
    desc:'초고속 기동력',
    bars:[82,100,42,38],
    moves:{
      punch:{dmg:23,kbx:5,kby:-2,stun:0,reach:66,low:false,startup:3,active:3,recovery:4},
      kick:  {dmg:34,kbx:7,kby:-3,stun:0,reach:82,low:false,startup:5,active:4,recovery:6},
      heavy: {dmg:44,kbx:9,kby:-5,stun:8,reach:76,low:false,startup:9,active:3,recovery:11},
      low:   {dmg:20,kbx:4,kby:0, stun:0,reach:62,low:true, startup:3,active:3,recovery:4},
      airPunch:{dmg:30,kbx:6,kby:-5,stun:0,reach:64,low:false,startup:3,active:4,recovery:3},
      special:{name:'전격',emoji:'⚡',dmg:60,kbx:11,kby:-8,stun:10,cost:20,col:'#ffee00',isDash:true},
      super:  {name:'뇌신강림',emoji:'🌩️',dmg:120,kbx:6,kby:-12,stun:22,cost:100,col:'#ffff00',isLauncher:true},
    }
  },
  {
    name:'철권',emoji:'🦾',hp:260,
    atk:34,def:1.2,spd:3.2,jump:13,
    supCost:30,col:'#c04fff',
    type:'파워형',badge:'파워',badgeCol:'#8822cc',
    desc:'압도적 파괴력',
    bars:[90,80,88,96],
    moves:{
      punch:{dmg:32,kbx:6,kby:-2,stun:5,reach:68,low:false,startup:7,active:5,recovery:8},
      kick:  {dmg:46,kbx:9,kby:-4,stun:8,reach:84,low:false,startup:9,active:5,recovery:11},
      heavy: {dmg:60,kbx:14,kby:-6,stun:15,reach:78,low:false,startup:14,active:5,recovery:18},
      low:   {dmg:28,kbx:5,kby:0, stun:5,reach:64,low:true, startup:6,active:4,recovery:7},
      airPunch:{dmg:40,kbx:8,kby:-5,stun:5,reach:66,low:false,startup:6,active:5,recovery:6},
      special:{name:'지진권',emoji:'💥',dmg:70,kbx:14,kby:-3,stun:20,cost:30,col:'#cc44ff',isSlam:true},
      super:  {name:'오버드라이브',emoji:'💪',dmg:150,kbx:10,kby:-14,stun:35,cost:100,col:'#ff00ff',isLauncher:true},
    }
  },
  {
    name:'닌자',emoji:'🥷',hp:188,
    atk:25,def:0.88,spd:6.2,jump:22,
    supCost:22,col:'#00ff88',
    type:'민첩형',badge:'닌자',badgeCol:'#00aa55',
    desc:'분신술·기습 전법',
    bars:[78,95,55,50],
    moves:{
      punch:{dmg:22,kbx:4,kby:-2,stun:0,reach:68,low:false,startup:4,active:4,recovery:5},
      kick:  {dmg:33,kbx:6,kby:-3,stun:0,reach:84,low:false,startup:6,active:4,recovery:7},
      heavy: {dmg:44,kbx:8,kby:-5,stun:8,reach:78,low:false,startup:10,active:4,recovery:12},
      low:   {dmg:19,kbx:3,kby:0, stun:0,reach:64,low:true, startup:4,active:4,recovery:5},
      airPunch:{dmg:29,kbx:5,kby:-5,stun:0,reach:66,low:false,startup:3,active:4,recovery:3},
      special:{name:'분신 베기',emoji:'👥',dmg:58,kbx:9,kby:-7,stun:12,cost:22,col:'#00ff88',isDash:true},
      super:  {name:'천수관음',emoji:'🌀',dmg:115,kbx:7,kby:-11,stun:22,cost:100,col:'#88ffcc',isMultiHit:true},
    }
  },
];

// ================================================================
//  PARTICLES
// ================================================================
let PARTS=[],HITS=[];
function spawnP(x,y,o={}){
  const n=o.n||8;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2,v=(o.vMin||1.5)+Math.random()*(o.vMax||5);
    const cols=Array.isArray(o.col)?o.col:[o.col||'#fff'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      dec:(o.dMin||.028)+Math.random()*(o.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(o.szMin||2)+Math.random()*(o.szMax||5),glow:o.glow||false});
  }
}
function spawnHit(x,y,txt,col){HITS.push({x,y:y-18,txt,col,life:1,vy:-.55});}
function tickParts(){
  for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.dec;p.life<=0&&PARTS.splice(i,1);}
  for(let i=HITS.length-1;i>=0;i--){const h=HITS[i];h.y+=h.vy;h.life-=.022;h.life<=0&&HITS.splice(i,1);}
}
function drawParts(){
  for(const p of PARTS){ctx.save();ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.08,p.life),0,Math.PI*2);ctx.fill();if(p.glow)ctx.shadowBlur=0;ctx.restore();}
  for(const h of HITS){ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;ctx.fillStyle=h.col;ctx.font="bold 13px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.fillText(h.txt,h.x,h.y);ctx.restore();}
}

// PROJECTILES
let PROJS=[];

// ================================================================
//  FIGHTER FACTORY
// ================================================================
const FLOOR=()=>CH-72;
const GRAV=0.88;

function makeF(cIdx,isP2){
  const c=CHARS[cIdx];
  return {
    x:isP2?CW*.74:CW*.22,y:FLOOR(),
    vx:0,vy:0,
    char:c,facing:isP2?-1:1,
    hp:c.hp,maxHp:c.hp,
    super:0,stun:0,stunMax:0,
    onGround:true,
    // State machine
    state:'idle',stateT:0,animF:0,
    // Hit cooldown
    hitCD:0,
    // Combo
    comboN:0,comboT:0,
    // Block
    blocking:false,blockT:0,blockDir:false,
    // Invincible frames (after hit)
    invT:0,
    // Air attack used
    airAtk:false,
    // Hitstop
    hitstop:0,
    // Current attack data
    curMove:null,
    // Touch input
    _tL:false,_tR:false,_tJ:false,_tDown:false,
    // AI
    ai:{rt:0,lastAct:'',aggro:0.65,phaseCd:0,phase:'neutral'},
    isP2,
  };
}

// ================================================================
//  COMBAT CORE
// ================================================================
function doAtk(f,moveKey,opp){
  if(f.stateT>0&&!['idle','walk'].includes(f.state))return;
  if(f.state==='ko'||f.state==='stun')return;
  // special cost check
  const move=f.char.moves[moveKey];
  if(!move)return;
  if(moveKey==='special'&&f.super<move.cost)return;
  if(moveKey==='super'&&f.super<100)return;
  f.state=moveKey;
  f.stateT=move.startup+move.active+move.recovery;
  f.curMove=move;
  f.curMove._key=moveKey;
  f.curMove._hit=false;  // hasn't connected yet

  if(moveKey==='special'){f.super=Math.max(0,f.super-move.cost);}
  if(moveKey==='super'){f.super=0;}

  // Visual effects for special/super
  if(moveKey==='special'||moveKey==='super'){
    spawnP(f.x,f.y,{n:14,col:move.col,glow:true,vMax:6,szMax:8});
  }

  // Projectile spawn
  if(move.isProjectile){
    PROJS.push({
      x:f.x+f.facing*40,y:f.y-f.char.hp*.15,
      vx:f.facing*(moveKey==='super'?13:9),vy:0,
      life:80,sz:move.isFreeze?22:16,
      col:move.col,owner:f,dmg:move.dmg,
      kb:{x:move.kbx,y:move.kby},stun:move.stun,
      glow:true,freeze:move.freeze||false,
    });
  }
  // Dash attack (moves fighter forward)
  if(move.isDash){
    f.vx=f.facing*10;
    f.vy=-3;
  }
  // Launcher (anti-air)
  if(move.isLauncher){f.vy=-2;}
  // Multi-hit super
  if(move.isMultiHit){
    for(let i=1;i<=4;i++){
      setTimeout(()=>{
        if(!roundActive)return;
        const target=f.isP2?P1:P2;
        if(Math.abs(f.x-target.x)<90)applyHit(f,target,move.dmg*.4,{x:move.kbx*.3,y:move.kby*.3},0,true);
      },i*80);
    }
  }
}

function applyHit(atk,def,dmg,kb,stun,skipState){
  if(def.state==='ko')return;
  if(def.hitCD>0)return;
  if(def.invT>0)return;
  // Guard check
  if(def.blocking&&def.blockT>0){
    const isLow=atk.curMove&&atk.curMove.low;
    const blockWorks=isLow?def.blockDir:!def.blockDir||true; // simplification
    if(blockWorks){
      def.hp=Math.max(0,def.hp-Math.round(dmg*.1));
      def.vx=atk.facing*2;
      spawnP(def.x,def.y,{n:6,col:'rgba(180,220,255,.7)',glow:true,vMax:3,szMax:5});
      spawnHit(def.x,def.y-40,'GUARD!','#4499ff');
      // Build super on guard
      atk.super=Math.min(100,atk.super+4);def.super=Math.min(100,def.super+3);
      // Hitstop
      atk.hitstop=4;def.hitstop=4;
      triggerHPAnim(def);return;
    }
  }
  // Apply damage
  const defVal=def.char.def;
  const realDmg=Math.round(dmg/defVal);
  def.hp=Math.max(0,def.hp-realDmg);
  def.vx=atk.facing*kb.x;
  def.vy=kb.y;
  def.hitCD=12;
  def.invT=8;
  // Stun
  if(stun>0){def.stun=Math.min(def.stun+stun,def.stunMax+stun);def.stunMax+=stun;}
  // Combo counter
  atk.comboN++;atk.comboT=100;
  // Super gauge
  atk.super=Math.min(100,atk.super+9);def.super=Math.min(100,def.super+5);
  // Particles + hit numbers
  spawnP(def.x,def.y,{n:12,col:[atk.char.col,'#ffaa44','#fff'],glow:true,vMax:6,szMax:7});
  const hitTxt=realDmg>80?'K.O BLOW!':realDmg>50?'HEAVY!':realDmg>30?'HIT!':'';
  if(hitTxt)spawnHit(def.x,def.y-50,hitTxt,atk.char.col);
  spawnHit(def.x,def.y-32,realDmg+'',atk.comboN>2?'#f5c518':'#ffaa44');
  // Hit state
  if(!skipState){
    if(def.onGround){def.state='hurt';def.stateT=14+(realDmg>40?8:0);}
    else{def.state='airHurt';def.stateT=16;}
  }
  // Hitstop
  const hs=stun>0?10:6;atk.hitstop=hs;def.hitstop=hs;
  // Screen shake
  screenShake();
  // KO check
  if(def.hp<=0){def.state='ko';def.stateT=200;def.vy=-5;def.vx=atk.facing*6;roundEnd(atk.isP2?'p2':'p1');}
  // HP ghost update
  triggerHPAnim(def);
  // Combo display
  if(atk.comboN>=2)showComboDisplay(atk.comboN,atk.char.col,atk.isP2);
}

function triggerHPAnim(f){
  const id=f.isP2?'hg-p2':'hg-p1';
  const el=document.getElementById(id);
  if(!el)return;
  el.style.width=(f.hp/f.maxHp*100)+'%';
}

// Screen shake
function screenShake(){
  const cw=document.getElementById('canvas-wrap');
  cw.classList.remove('shaking');
  void cw.offsetWidth;
  cw.classList.add('shaking');
  setTimeout(()=>cw.classList.remove('shaking'),200);
}

// ================================================================
//  AI ENGINE
// ================================================================
const AI_AGGRESSIONS=[0.52,0.70,0.90];
const AI_REACT_BASE=[16,10,6];  // frames between decisions

function updateAI(cpu,opp,diffLv){
  if(cpu.hitstop>0)return;
  cpu.ai.rt--;
  if(cpu.ai.rt>0)return;
  cpu.ai.rt=AI_REACT_BASE[diffLv]+Math.random()*8|0;

  const dx=opp.x-cpu.x;
  const dist=Math.abs(dx);
  const aggro=AI_AGGRESSIONS[diffLv];
  cpu.facing=dx>0?1:-1;
  const r=Math.random();
  const myHpPct=cpu.hp/cpu.maxHp;
  const oppHpPct=opp.hp/opp.maxHp;

  // Phase logic
  if(myHpPct<0.25&&cpu.super>=cpu.char.supCost){
    // Desperate: try super
    if(dist<110&&r<aggro*.55){doAtk(cpu,'super',opp);return;}
  }
  if(cpu.super>=100&&dist<120&&r<aggro*.45){doAtk(cpu,'super',opp);return;}

  // Close range
  if(dist<100){
    const rAtk=r*100;
    if(rAtk<aggro*28){doAtk(cpu,'punch',opp);}
    else if(rAtk<aggro*52){doAtk(cpu,'kick',opp);}
    else if(rAtk<aggro*62){doAtk(cpu,'heavy',opp);}
    else if(rAtk<aggro*68&&cpu.super>=cpu.char.supCost){doAtk(cpu,'special',opp);}
    else if(rAtk<aggro*72&&opp.onGround===false){doAtk(cpu,'airPunch',opp);}
    else if(rAtk<aggro*75){doAtk(cpu,'low',opp);}
    else if(rAtk<80){
      // Jump
      if(cpu.onGround&&r<.6){cpu.vy=-cpu.char.jump;cpu.onGround=false;cpu.state='jump';}
    }else{
      // Block
      cpu.blocking=true;cpu.blockT=20;
    }
  }else if(dist<200){
    // Mid range
    if(r<aggro*.5){cpu.vx=cpu.facing*cpu.char.spd*.9;}
    else if(r<aggro*.6&&cpu.super>=cpu.char.supCost){doAtk(cpu,'special',opp);}
    else if(r<aggro*.65&&cpu.onGround){cpu.vy=-cpu.char.jump;cpu.onGround=false;cpu.state='jump';}
    else{cpu.vx=cpu.facing*cpu.char.spd*.5;}
  }else{
    // Far
    if(r<aggro*.65){cpu.vx=cpu.facing*cpu.char.spd*.85;}
    else if(r<aggro*.7&&cpu.super>=cpu.char.supCost){doAtk(cpu,'special',opp);}
    else{cpu.vx=cpu.facing*cpu.char.spd*.4;}
  }
}

// ================================================================
//  FIGHTER UPDATE
// ================================================================
function updateFighter(f,opp){
  if(f.hitstop>0){f.hitstop--;return;}
  f.vy+=GRAV;
  if(f.state!=='ko'||(f.y<FLOOR())){f.y+=f.vy;}
  f.x+=f.vx;
  f.vx*=(f.onGround?.7:.88);

  // Floor
  if(f.y>=FLOOR()){
    f.y=FLOOR();f.vy=0;f.onGround=true;f.airAtk=false;
    if(f.state==='jump'||f.state==='airHurt'){f.state='idle';f.stateT=0;}
    if(f.state==='ko'&&f.vx!==0){f.vx*=.5;}
  }else{f.onGround=false;}

  // Walls
  if(f.x<f.char.emoji.length*10)f.x=f.char.emoji.length*10;
  if(f.x>CW-f.char.emoji.length*10)f.x=CW-f.char.emoji.length*10;
  // Keep together (push towards center if too far)
  const maxDist=CW*.72;
  if(Math.abs(f.x-opp.x)>maxDist){f.x+=(opp.x-f.x)*.03;}

  // State timer
  if(f.stateT>0)f.stateT--;
  else if(!['idle','walk','jump','block','ko','stun'].includes(f.state)){
    f.state='idle';f.curMove=null;
  }
  if(f.hitCD>0)f.hitCD--;
  if(f.invT>0)f.invT--;
  if(f.blockT>0)f.blockT--;else f.blocking=false;
  if(f.comboT>0)f.comboT--;else if(f.comboT===0){f.comboN=0;comboDisplayOff();}
  f.animF=(f.animF+1)%60;

  // Auto-face
  if(['idle','walk'].includes(f.state))f.facing=opp.x>f.x?1:-1;

  // Stun system
  if(f.stun>0){
    f.stun-=1;
    if(f.stun>0&&f.state!=='ko'){f.state='stun';f.stateT=f.stun;}
    else if(f.state==='stun'){f.state='idle';f.stunMax=0;}
  }

  // ATTACK HIT DETECTION (melee moves)
  const cm=f.curMove;
  if(cm&&!cm._hit&&!cm.isProjectile&&!cm.isDash&&!cm.isLauncher&&!cm.isMultiHit&&!cm.isSlam&&!cm.isFreeze){
    const prog=cm.startup+cm.active+cm.recovery-f.stateT;
    if(prog>=cm.startup&&prog<cm.startup+cm.active){
      // Active frames
      const hx=f.x+f.facing*cm.reach*.55;
      const hy=f.y-(cm.low?f.char.hp*.02:f.char.hp*.18);
      const ofy=opp.y-opp.char.hp*.18;
      if(Math.abs(hx-opp.x)<cm.reach*.9&&Math.abs(hy-ofy)<80){
        const isAir=(f.state==='jump'||f.state==='airPunch');
        const move=isAir?f.char.moves.airPunch:cm;
        applyHit(f,opp,move.dmg*f.char.atk/22,{x:move.kbx,y:move.kby},move.stun||0);
        cm._hit=true;
      }
    }
  }
  // Dash/Slam/Launcher melee check
  if(cm&&!cm._hit&&(cm.isDash||cm.isSlam||cm.isLauncher)){
    const dx=Math.abs(f.x-opp.x);
    if(dx<100&&f.stateT<cm.recovery+cm.active){
      applyHit(f,opp,cm.dmg*f.char.atk/22,{x:cm.kbx,y:cm.kby},cm.stun||0);
      cm._hit=true;
      if(cm.isLauncher){opp.vy=-12;opp.onGround=false;}
      if(cm.isSlam){spawnP(f.x,f.y,{n:20,col:f.char.col,glow:true,vMax:8,szMax:10});}
    }
  }
}

// Player input
function handlePlayerInput(p,opp){
  if(p.hitstop>0)return;
  const gl=KEYS['ArrowLeft']||KEYS['KeyA']||p._tL;
  const gr=KEYS['ArrowRight']||KEYS['KeyD']||p._tR;
  const gj=KEYS['ArrowUp']||KEYS['KeyZ']||p._tJ;
  const gd=KEYS['ArrowDown']||KEYS['KeyS']||p._tDown;

  // Block: hold back (away from opponent)
  const holdBack=(p.facing===1&&gl)||(p.facing===-1&&gr);
  if(gd&&holdBack){p.blocking=true;p.blockT=4;p.blockDir=true;} // crouch block (handles lows)
  else if(holdBack&&p.onGround){p.blocking=true;p.blockT=4;p.blockDir=false;}

  if(['idle','walk'].includes(p.state)){
    if(gl){p.vx=-p.char.spd;p.state='walk';}
    else if(gr){p.vx=p.char.spd;p.state='walk';}
    else{p.vx*=.55;if(Math.abs(p.vx)<.5)p.state='idle';}
    if(gj&&p.onGround){p.vy=-p.char.jump;p.onGround=false;p.state='jump';}
  }
  if(p.state==='jump'&&!p.airAtk){
    if(gj){/* allow air movement */}
  }
}

// ================================================================
//  PROJECTILE UPDATE
// ================================================================
function updateProjs(p1,p2){
  for(let i=PROJS.length-1;i>=0;i--){
    const pr=PROJS[i];
    pr.x+=pr.vx;pr.y+=pr.vy||0;pr.life--;
    // Trail
    if(pr.life%2===0)spawnP(pr.x,pr.y,{n:2,col:pr.col,vMin:0,vMax:.8,szMin:1,szMax:pr.sz*.5,dMin:.1,dMax:.15,glow:true});
    // Hit target
    const opp=pr.owner.isP2?p1:p2;
    const dx=pr.x-opp.x,dy=pr.y-(opp.y-40);
    if(Math.abs(dx)<opp.char.hp*.08+pr.sz&&Math.abs(dy)<50){
      applyHit(pr.owner,opp,pr.dmg,pr.kb,pr.stun||0);
      if(pr.freeze)opp.stun=Math.max(opp.stun,45);
      spawnP(pr.x,pr.y,{n:18,col:[pr.col,'#fff'],glow:true,vMax:7,szMax:8});
      PROJS.splice(i,1);continue;
    }
    if(pr.life<=0||pr.x<-50||pr.x>CW+50)PROJS.splice(i,1);
  }
}

// ================================================================
//  DRAW
// ================================================================
let bgStars=[];
function initBgStars(){bgStars=[];for(let i=0;i<80;i++)bgStars.push({x:Math.random()*CW,y:Math.random()*CH*.45,r:Math.random()<.05?1.2:.6,a:.2+Math.random()*.7});}

function drawBackground(){
  // Sky
  const sky=ctx.createLinearGradient(0,0,0,CH);
  sky.addColorStop(0,'#0a0318');sky.addColorStop(.55,'#180530');sky.addColorStop(1,'#1a0340');
  ctx.fillStyle=sky;ctx.fillRect(0,0,CW,CH);
  // Stars
  for(const s of bgStars){ctx.save();ctx.globalAlpha=s.a;ctx.fillStyle='rgba(220,200,255,1)';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();ctx.restore();}
  // City silhouette
  ctx.fillStyle='#0d0320';
  for(let ci=0;ci<18;ci++){
    const bw=18+Math.sin(ci*1.9)*9+5,bh=42+Math.sin(ci*2.4)*36+14;
    const bx=ci*(CW/17)-10;
    ctx.fillRect(bx,CH*.22-bh,bw,bh);
    for(let wy=CH*.22-bh+4;wy<CH*.22-3;wy+=9){
      if(Math.random()<.55)continue;
      const lc=Math.random()<.4?'0,200,255':'255,180,50';
      ctx.fillStyle=`rgba(${lc},.25)`;ctx.fillRect(bx+3+Math.floor(Math.random()*(bw-8)),wy,3,6);ctx.fillStyle='#0d0320';
    }
  }
  // Ground
  const gr=ctx.createLinearGradient(0,CH*.7,0,CH);
  gr.addColorStop(0,'#1a0040');gr.addColorStop(1,'#0e0025');
  ctx.fillStyle=gr;ctx.fillRect(0,CH*.7,CW,CH*.3);
  // Floor neon line
  ctx.save();ctx.strokeStyle='rgba(192,79,255,.45)';ctx.shadowColor='rgba(192,79,255,.7)';ctx.shadowBlur=16;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(0,FLOOR()+5);ctx.lineTo(CW,FLOOR()+5);ctx.stroke();ctx.restore();
  // Grid
  ctx.strokeStyle='rgba(108,99,255,.05)';ctx.lineWidth=1;
  for(let gx=0;gx<CW;gx+=50){ctx.beginPath();ctx.moveTo(gx,FLOOR());ctx.lineTo(gx,CH);ctx.stroke();}
  for(let gy=FLOOR();gy<CH;gy+=24){ctx.beginPath();ctx.moveTo(0,gy);ctx.lineTo(CW,gy);ctx.stroke();}
  // Spotlights
  [[CW*.26,'rgba(0,80,255,.13)'],[CW*.74,'rgba(255,0,50,.11)']].forEach(([lx,col])=>{
    const sl=ctx.createRadialGradient(lx,FLOOR()+12,0,lx,FLOOR()+12,CW*.24);
    sl.addColorStop(0,col);sl.addColorStop(1,'transparent');
    ctx.fillStyle=sl;ctx.fillRect(0,0,CW,CH);
  });
}

function drawShadow(f){
  ctx.save();ctx.globalAlpha=.28;ctx.fillStyle='#000';
  ctx.beginPath();ctx.ellipse(f.x,FLOOR()+7,f.char.bars[2]*.24+12,8,0,0,Math.PI*2);ctx.fill();ctx.restore();
}

let gFrame=0;
function drawFighter(f){
  const x=f.x,y=f.y;
  const h=f.char.hp*.35; // scale fighter size to HP stat
  ctx.save();ctx.translate(x,y);if(f.facing===-1)ctx.scale(-1,1);
  // State-based visuals
  let sz=1,offY=0,rot=0,glow=null,alpha=1;
  if(f.state==='punch'){
    sz=1.18;
    // Punch fist extension
    ctx.font='22px serif';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.shadowColor=f.char.col;ctx.shadowBlur=12;
    ctx.fillText('👊',h*.28,f.stateT>8?-h*.5:-h*.6);
    ctx.shadowBlur=0;
  }else if(f.state==='kick'){
    sz=1.1;
    ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.fillText('🦵',h*.22,-h*.28);
  }else if(f.state==='heavy'){
    sz=1.25;glow=f.char.col;
    ctx.font='24px serif';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.shadowColor=f.char.col;ctx.shadowBlur=14;
    ctx.fillText('👊',h*.3,f.stateT>10?-h*.45:-h*.62);
    ctx.shadowBlur=0;
  }else if(f.state==='low'){
    sz=0.88;offY=12;
    ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.fillText('👊',h*.25,-h*.1);
  }else if(f.state==='airPunch'){
    sz=1.15;rot=-f.facing*.22;
    ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';
    ctx.shadowColor=f.char.col;ctx.shadowBlur=10;ctx.fillText('👊',h*.22,-h*.55);ctx.shadowBlur=0;
  }else if(f.state==='jump'){
    offY=-8-Math.abs(f.vy)*2.2;rot=f.facing*.14;
  }else if(f.state==='hurt'||f.state==='airHurt'){
    sz=.88;rot=f.facing*-.18;
    ctx.filter='brightness(2.5) hue-rotate(310deg)';alpha=f.hitCD%2===0?.6:1;
  }else if(f.state==='stun'){
    sz=.85;offY=5;rot=Math.sin(f.animF*.25)*.1;
    ctx.filter='brightness(2) sepia(1)';
    // Stars around stunned
    ['⭐','✨','💫'].forEach((s,si)=>{
      ctx.save();ctx.font='14px serif';ctx.textAlign='center';
      const sa=f.animF*.15+si*(Math.PI*2/3);
      ctx.fillText(s,Math.cos(sa)*24,-h*.75+Math.sin(sa)*12);ctx.restore();
    });
  }else if(f.state==='block'||f.blocking){
    ctx.save();ctx.strokeStyle='rgba(0,200,255,.5)';ctx.shadowColor='rgba(0,200,255,.4)';ctx.shadowBlur=16;ctx.lineWidth=2.5;
    ctx.fillStyle='rgba(0,200,255,.1)';
    ctx.beginPath();ctx.arc(h*.22,-h*.44,h*.62,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();
  }else if(f.state==='special'){
    sz=1.3;glow=f.char.col;
    spawnP(x,y,{n:2,col:f.char.col,glow:true,vMax:4,szMax:6,dMin:.06,dMax:.1});
  }else if(f.state==='super'){
    sz=1.4;glow=f.char.col;
    if(f.animF%4<2){ctx.filter='brightness(3) saturate(2)';}
    spawnP(x,y,{n:3,col:[f.char.col,'#fff'],glow:true,vMax:5,szMax:8,dMin:.05,dMax:.09});
  }else if(f.state==='ko'){
    rot=f.facing*.8;offY=14;sz=.82;
  }else if(f.state==='idle'||f.state==='walk'){
    offY=Math.sin(f.animF*.1)*2;
  }
  ctx.rotate(rot);ctx.globalAlpha*=alpha;
  ctx.font=`${h*1.15*sz}px serif`;ctx.textAlign='center';ctx.textBaseline='bottom';
  if(glow){ctx.shadowBlur=24;ctx.shadowColor=glow;}
  ctx.fillText(f.char.emoji,0,-h*.02+offY);
  if(glow)ctx.shadowBlur=0;
  ctx.restore();
  // Super aura ring
  if(f.super>=100){
    ctx.save();
    ctx.strokeStyle=f.char.col+'88';ctx.lineWidth=2.5;
    ctx.shadowBlur=14+Math.sin(gFrame*.07)*7;ctx.shadowColor=f.char.col;
    ctx.beginPath();ctx.arc(f.x,f.y-h*.5,h*.78+Math.sin(gFrame*.06)*5,0,Math.PI*2);ctx.stroke();
    ctx.restore();
  }
  // Stun flash if stunned
  if(f.stun>0&&f.stun%8<3){
    ctx.save();ctx.strokeStyle='#ffee00';ctx.lineWidth=2;ctx.globalAlpha=.5;
    ctx.beginPath();ctx.arc(f.x,f.y-h*.5,h*.85,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
}

function drawProjectiles(){
  for(const pr of PROJS){
    ctx.save();ctx.shadowBlur=22;ctx.shadowColor=pr.col;ctx.fillStyle=pr.col;
    ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,255,255,.85)';ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz*.35,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
}

// ================================================================
//  ROUND SYSTEM
// ================================================================
let P1,P2,round,p1Wins,p2Wins,roundTimer,roundActive,diffLv,selChar;
let G={running:false};

function buildSuperBars(){
  ['p1','p2'].forEach(id=>{
    const el=document.getElementById('sb-'+id);el.innerHTML='';
    for(let i=0;i<4;i++){const s=document.createElement('div');s.className='sseg';const f=document.createElement('div');f.className='sfill';f.style.width='0%';s.appendChild(f);el.appendChild(s);}
  });
}
function updateSuperBars(){
  [[P1,'p1'],[P2,'p2']].forEach(([p,id])=>{
    const segs=document.querySelectorAll('#sb-'+id+' .sfill');
    segs.forEach((s,i)=>{
      const pct=Math.min(100,Math.max(0,(p.super-i*25)*4));
      s.style.width=pct+'%';
      s.closest('.sseg').classList.toggle('full',p.super>=(i+1)*25);
    });
  });
}
function updateHPBars(){
  [[P1,'p1'],[P2,'p2']].forEach(([p,id])=>{
    document.getElementById('hf-'+id).style.width=(p.hp/p.maxHp*100)+'%';
  });
}
function buildWinDots(){
  ['p1','p2'].forEach(id=>{const g=document.getElementById('wd-'+id);g.innerHTML='';for(let i=0;i<3;i++){const d=document.createElement('div');d.className='wd';g.appendChild(d);}});
}
function updateWinDots(){
  const dots1=document.querySelectorAll('#wd-p1 .wd');
  const dots2=document.querySelectorAll('#wd-p2 .wd');
  dots1.forEach((d,i)=>d.classList.toggle('p1w',i<p1Wins));
  dots2.forEach((d,i)=>d.classList.toggle('p2w',i<p2Wins));
}

// COMBO DISPLAY
let comboDisplayTimer=0;
function showComboDisplay(n,col,isP2){
  const cd=document.getElementById('combo-display');
  const cn=document.getElementById('combo-n');
  cd.style.left=(isP2?'14px':'auto');cd.style.right=(isP2?'auto':'14px');
  cd.style.top='50%';cd.style.transform='translateY(-50%)';
  cn.textContent=n;cn.style.color=col;
  cd.style.opacity='1';comboDisplayTimer=90;
}
function comboDisplayOff(){document.getElementById('combo-display').style.opacity='0';}

function newRound(){
  P1=makeF(selChar,false);
  const cpuIdx=Math.floor(Math.random()*CHARS.length);
  P2=makeF(cpuIdx,true);P2.facing=-1;
  PROJS=[];PARTS=[];HITS=[];
  roundTimer=99*60;roundActive=true;
  document.getElementById('rnd-lbl').textContent='ROUND '+round;
  document.getElementById('fn-p1').textContent=P1.char.name;
  document.getElementById('fn-p2').textContent='CPU·'+P2.char.name;
  document.getElementById('fn-p2').style.color=P2.char.col;
  document.getElementById('hf-p2').style.background=`linear-gradient(90deg,#ff0022,${P2.char.col})`;
  // Ghost HP reset
  document.getElementById('hg-p1').style.width='100%';
  document.getElementById('hg-p2').style.width='100%';
  buildSuperBars();comboDisplayOff();
}

function roundEnd(winner){
  roundActive=false;
  const res=document.getElementById('rnd-result');
  if(winner==='p1'){p1Wins++;res.style.color='var(--blue)';res.textContent='🏆 P1 WIN!';}
  else{p2Wins++;res.style.color='var(--red)';res.textContent='CPU WIN!';}
  res.style.opacity='1';
  updateWinDots();
  setTimeout(()=>{
    res.style.opacity='0';
    if(p1Wins>=2||p2Wins>=2){setTimeout(showFightResult,350);}
    else{round++;newRound();}
  },2400);
}

// ================================================================
//  MAIN LOOP
// ================================================================
function loop(){
  if(!G.running)return;
  gFrame++;
  if(comboDisplayTimer>0){comboDisplayTimer--;if(comboDisplayTimer===0)comboDisplayOff();}
  const W=canvas.width,H=canvas.height;
  ctx.clearRect(0,0,W,H);
  drawBackground();
  drawShadow(P1);drawShadow(P2);
  drawParts();drawProjectiles();drawFighter(P1);drawFighter(P2);drawParts();
  drawHNs_local();
  // Timer + HP
  if(roundActive){
    roundTimer--;
    const sec=Math.max(0,Math.ceil(roundTimer/60));
    document.getElementById('timer').textContent=sec;
    document.getElementById('timer').classList.toggle('low',sec<=10);
    if(roundTimer<=0){const w=P1.hp>=P2.hp?'p1':'p2';roundEnd(w);}
    updateFighter(P1,P2);updateFighter(P2,P1);
    updateProjs(P1,P2);
    handlePlayerInput(P1,P2);
    updateAI(P2,P1,diffLv);
    updateSuperBars();updateHPBars();
    tickParts();
  }else{tickParts();}
  requestAnimationFrame(loop);
}
function drawHNs_local(){
  for(const h of HITS){ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;ctx.fillStyle=h.col;ctx.font="bold 12px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.fillText(h.txt,h.x,h.y);ctx.restore();}
}

// ================================================================
//  TITLE & GAMEOVER
// ================================================================
const KEYS={};
window.addEventListener('keydown',e=>{
  KEYS[e.code]=true;
  if(!G.running)return;
  if(e.code==='KeyX'||e.code==='KeyJ')doAtk(P1,'punch',P2);
  if(e.code==='KeyC'||e.code==='KeyK')doAtk(P1,'kick',P2);
  if(e.code==='KeyV'||e.code==='KeyL')doAtk(P1,'special',P2);
  if(e.code==='KeyB')doAtk(P1,'heavy',P2);
  if(e.code==='KeyN')doAtk(P1,'low',P2);
  if(e.code==='KeyM')doAtk(P1,'super',P2);
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();
});
window.addEventListener('keyup',e=>KEYS[e.code]=false);

function showTitle(){
  selChar=selChar||0;diffLv=diffLv||1;
  initBgStars();buildWinDots();buildSuperBars();
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'],ddesc=['느린 AI·학습용','균형잡힌 AI','공격적·예측 불가'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">STREET FIGHTER EX v3.0</div>
    <div class="ov-title" style="color:var(--purple)">🥊 스트리트<br>파이터 EX</div>
    <div class="ov-sub">6 캐릭터 · AI CPU · 필살기 · 콤보 시스템</div>
    <div class="char-select-wrap">
      <div class="char-select-title">캐릭터 선택</div>
      <div class="char-grid" id="cg"></div>
    </div>
    <div class="char-select-title">CPU 난이도</div>
    <div class="diff-row">${dnames.map((n,i)=>`<div class="dt${i===diffLv?' sel':''}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:1px">${ddesc[i]}</div></div>`).join('')}</div>
    <div style="font-size:8px;color:#336;line-height:2.3;margin-bottom:14px">
      ← → 이동 &nbsp;|&nbsp; ↑ / Z 점프 &nbsp;|&nbsp; ↓ 가드<br>
      X/J 펀치 &nbsp;|&nbsp; C/K 킥 &nbsp;|&nbsp; B 강공격 &nbsp;|&nbsp; N 하단공격<br>
      V/L 필살기 &nbsp;|&nbsp; M 슈퍼기술 (게이지 MAX)<br>
      3선승제 · 99초 타임아웃
    </div>
    <button class="ov-btn" onclick="startGame()">대전 시작 ⚡</button>`;
  buildCharGrid();
  document.getElementById('overlay').style.display='flex';
}

function buildCharGrid(){
  const g=document.getElementById('cg');if(!g)return;g.innerHTML='';
  const bnames=['속도','공격','방어','체력'];
  CHARS.forEach((c,i)=>{
    const d=document.createElement('div');d.className='cc'+(i===selChar?' sel':'');
    const barsH=c.bars.map((v,bi)=>`<div class="cc-bar-row"><div class="cc-bar-lbl">${bnames[bi]}</div><div class="cc-bar-bg"><div class="cc-bar-fill" style="width:${v}%;background:${c.col}"></div></div></div>`).join('');
    d.innerHTML=`<div class="cc-badge" style="background:${c.badgeCol}22;color:${c.badgeCol};border:1px solid ${c.badgeCol}44">${c.badge}</div><span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-type">${c.type}</div><div class="cc-bars">${barsH}</div>`;
    d.onclick=()=>{selChar=i;document.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};
    g.appendChild(d);
  });
}
window.setDiff=d=>{diffLv=d;document.querySelectorAll('.dt').forEach((t,i)=>t.classList.toggle('sel',i===d));};

function showFightResult(){
  G.running=false;
  const win=p1Wins>=2;
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">${win?'🏆 VICTORY':'DEFEAT'}</div>
    <div class="ov-title" style="color:${win?'var(--blue)':'var(--red)'}">${win?'승리!':'패배!'}</div>
    <div class="ov-sub">${win?'PERFECT CHAMPION':'TRY AGAIN'}</div>
    <div class="stats-row">
      <div class="sc"><div class="sv" style="color:var(--blue)">${p1Wins}</div><div class="sl">P1 승리</div></div>
      <div class="sc"><div class="sv">${round}</div><div class="sl">총 라운드</div></div>
      <div class="sc"><div class="sv" style="color:var(--red)">${p2Wins}</div><div class="sl">CPU 승리</div></div>
    </div>
    <button class="ov-btn" onclick="startGame()">다시 대전 🥊</button>
    <br><button class="ov-btn2" onclick="showTitle()">캐릭터 변경</button>`;
  document.getElementById('overlay').style.display='flex';
}

window.startGame=function(){
  document.getElementById('overlay').style.display='none';
  G={running:true};p1Wins=0;p2Wins=0;round=1;
  PARTS=[];HITS=[];PROJS=[];
  initBgStars();buildWinDots();
  newRound();requestAnimationFrame(loop);
};
window.showTitle=showTitle;

// TOUCH CONTROLS
function addT(id,dn,up){
  const el=document.getElementById(id);if(!el)return;
  const d=e=>{e.preventDefault();if(dn)dn();el.classList.add('pr');};
  const u=e=>{e.preventDefault();if(up)up();el.classList.remove('pr');};
  el.addEventListener('touchstart',d,{passive:false});el.addEventListener('touchend',u,{passive:false});el.addEventListener('touchcancel',u,{passive:false});
  el.addEventListener('mousedown',d);el.addEventListener('mouseup',u);
}
addT('dp-left', ()=>{if(G.running)P1._tL=true;},()=>P1._tL=false);
addT('dp-right',()=>{if(G.running)P1._tR=true;},()=>P1._tR=false);
addT('dp-up',   ()=>{if(G.running)P1._tJ=true;},()=>P1._tJ=false);
addT('dp-down', ()=>{if(G.running)P1._tDown=true;},()=>P1._tDown=false);
addT('ab-j',    ()=>{if(G.running){P1._tJ=true;}},()=>P1._tJ=false);
addT('ab-p',    ()=>{if(G.running)doAtk(P1,'punch',P2);},null);
addT('ab-k',    ()=>{if(G.running)doAtk(P1,'kick',P2);},null);
addT('ab-s',    ()=>{if(G.running&&P1.super>=100)doAtk(P1,'super',P2);else if(G.running)doAtk(P1,'special',P2);},null);

showTitle();
</script>
</body>
</html>"""

def render():
    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    components.html(GAME_HTML, height=730, scrolling=False)
