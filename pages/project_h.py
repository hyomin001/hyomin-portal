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
html,body{width:100%;height:728px;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:728px;overflow:hidden;display:flex;flex-direction:column;}

/* HUD */
#hud{display:flex;align-items:center;gap:8px;padding:10px 12px 6px;background:linear-gradient(180deg,rgba(0,0,0,.9)0%,transparent 100%);pointer-events:none;position:relative;z-index:50;}
.hp-col{flex:1;display:flex;flex-direction:column;gap:3px;}
.fn{font-size:9px;letter-spacing:2px;font-weight:700;}
#fn-p1{color:var(--blue);}#fn-p2{color:var(--red);text-align:right;}
.hp-wrap{height:14px;background:rgba(0,0,0,.5);border:1.5px solid rgba(255,255,255,.1);border-radius:3px;overflow:hidden;position:relative;}
#hf-p1{height:100%;background:linear-gradient(90deg,#1144ff,#33aaff,#88ddff);border-radius:2px;transition:width .06s;}
#hf-p2{height:100%;background:linear-gradient(90deg,#ff0022,#ff4444,#ff8866);border-radius:2px;transition:width .06s;float:right;}
#hg-p1{position:absolute;top:0;left:0;height:100%;background:rgba(255,200,0,.35);transition:width .5s ease;}
#hg-p2{position:absolute;top:0;right:0;height:100%;background:rgba(255,200,0,.35);transition:width .5s ease;}
.center-hud{text-align:center;min-width:82px;flex-shrink:0;}
#rnd-lbl{font-size:8px;color:var(--gold);letter-spacing:3px;font-weight:900;}
#timer{font-family:'Rajdhani',sans-serif;font-size:34px;font-weight:900;color:#fff;line-height:1;}
#timer.low{color:var(--red);animation:tpulse .5s infinite;}
@keyframes tpulse{0%,100%{transform:scale(1);}50%{transform:scale(1.1);}}

/* SUPER BARS */
#superbars{display:flex;justify-content:space-between;padding:3px 12px;pointer-events:none;align-items:center;}
.sb-side{display:flex;gap:3px;}
.sseg{width:32px;height:5px;border-radius:1px;background:rgba(255,215,0,.07);border:1px solid rgba(255,215,0,.12);overflow:hidden;}
.sfill{height:100%;background:linear-gradient(90deg,#664400,var(--gold),#ffeeaa);border-radius:1px;transition:width .08s;}
.sseg.full .sfill{animation:spulse .6s infinite;}
@keyframes spulse{0%,100%{opacity:1;}50%{opacity:.6;}}
#super-lbl{font-size:7px;color:#334;letter-spacing:3px;}

/* ARCADE PROGRESS */
#arcade-progress{display:flex;justify-content:space-between;align-items:center;padding:2px 12px;pointer-events:none;}
.prog-dots{display:flex;gap:5px;align-items:center;}
.pdot{width:10px;height:10px;border-radius:50%;border:1.5px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);transition:all .3s;font-size:10px;display:flex;align-items:center;justify-content:center;}
.pdot.done{background:var(--gold);box-shadow:0 0 8px rgba(245,197,24,.7);border-color:var(--gold);}
.pdot.current{background:var(--blue);box-shadow:0 0 10px rgba(51,170,255,.8);border-color:var(--blue);animation:cpulse .8s infinite;}
.pdot.boss{border-color:var(--red);}
.pdot.boss.current{background:var(--red);box-shadow:0 0 10px rgba(255,34,68,.8);}
@keyframes cpulse{0%,100%{transform:scale(1);}50%{transform:scale(1.2);}}
#stage-lbl{font-size:9px;color:var(--gold);letter-spacing:2px;font-weight:900;}

/* CANVAS */
#canvas-wrap{flex:1;position:relative;overflow:hidden;}
#gc{position:absolute;top:0;left:0;width:100%;height:100%;}

/* RESULT OVERLAY (mid-battle) */
#rnd-result{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-size:clamp(28px,6vw,50px);letter-spacing:4px;text-shadow:0 0 30px currentColor;opacity:0;transition:opacity .18s;text-align:center;white-space:nowrap;}

/* COMBO */
#combo-display{position:absolute;z-index:150;pointer-events:none;opacity:0;transition:opacity .15s;}
#combo-n{font-family:'Black Han Sans',sans-serif;font-size:clamp(26px,5vw,42px);line-height:1;text-shadow:0 0 20px currentColor;}
#combo-hits{font-size:8px;color:#aaa;letter-spacing:3px;margin-top:2px;}

/* SPECIAL EVENT BANNER */
#event-banner{position:absolute;top:36%;left:50%;transform:translate(-50%,-50%);z-index:210;pointer-events:none;text-align:center;opacity:0;transition:opacity .2s;}
#eb-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(20px,4.5vw,32px);letter-spacing:3px;text-shadow:0 0 25px currentColor;}
#eb-sub{font-size:10px;color:#bbb;letter-spacing:3px;margin-top:4px;}

/* KEYS HINT */
#keys-hint{position:absolute;bottom:130px;left:50%;transform:translateX(-50%);z-index:80;pointer-events:none;display:flex;gap:20px;font-size:8px;color:#334;letter-spacing:1px;text-align:center;white-space:nowrap;}

/* DPAD */
#dpad{position:absolute;bottom:12px;left:12px;z-index:100;display:grid;grid-template-columns:58px 58px 58px;grid-template-rows:52px 52px;gap:5px;}
.dp{border-radius:11px;background:rgba(255,255,255,.06);border:1.5px solid rgba(255,255,255,.1);display:flex;align-items:center;justify-content:center;font-size:22px;cursor:pointer;user-select:none;touch-action:none;transition:all .08s;}
.dp:active,.dp.pr{background:rgba(51,170,255,.2);border-color:rgba(51,170,255,.55);box-shadow:0 0 12px rgba(51,170,255,.35);transform:scale(.93);}
#dp-up{grid-column:2;grid-row:1;}#dp-left{grid-column:1;grid-row:2;}#dp-down{grid-column:2;grid-row:2;}#dp-right{grid-column:3;grid-row:2;}

/* ATK BUTTONS */
#atk-btns{position:absolute;bottom:12px;right:12px;z-index:100;display:grid;grid-template-columns:62px 62px;grid-template-rows:56px 56px;gap:6px;}
.ab{border-radius:12px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;user-select:none;touch-action:none;transition:all .08s;border:2px solid;gap:2px;}
.ab:active,.ab.pr{transform:scale(.9);filter:brightness(1.6);}
#ab-p{background:rgba(255,34,68,.12);border-color:rgba(255,34,68,.45);color:var(--red);font-size:24px;}
#ab-k{background:rgba(245,197,24,.1);border-color:rgba(245,197,24,.4);color:var(--gold);font-size:24px;}
#ab-j{background:rgba(0,212,255,.1);border-color:rgba(0,212,255,.4);color:var(--cyan);font-size:24px;}
#ab-s{background:rgba(192,79,255,.12);border-color:rgba(192,79,255,.45);color:var(--purple);font-size:24px;}
.ab-lbl{font-size:7px;letter-spacing:1px;font-weight:700;}

/* STAGE CLEAR / NEXT STAGE SCREEN */
#stage-screen{position:absolute;inset:0;z-index:300;display:none;align-items:center;justify-content:center;background:rgba(0,0,0,.88);backdrop-filter:blur(4px);}
.ss-box{text-align:center;padding:32px 24px;background:linear-gradient(160deg,rgba(8,3,15,.98),rgba(14,6,24,.98));border:1px solid rgba(192,79,255,.22);border-radius:20px;min-width:320px;max-width:92vw;}
.ss-eye{font-size:7px;letter-spacing:4px;color:var(--gold);background:rgba(245,197,24,.1);border:1px solid rgba(245,197,24,.22);border-radius:99px;padding:3px 12px;display:inline-block;margin-bottom:10px;}
.ss-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5vw,34px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ss-rival{font-size:9px;letter-spacing:3px;color:#556;margin-bottom:14px;}
.rival-card{display:flex;align-items:center;gap:16px;background:var(--glass);border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin-bottom:14px;text-align:left;}
.rc-ico{font-size:48px;}
.rc-name{font-family:'Black Han Sans',sans-serif;font-size:20px;letter-spacing:2px;margin-bottom:3px;}
.rc-type{font-size:9px;letter-spacing:2px;color:#556;margin-bottom:6px;}
.rc-desc{font-size:9px;color:#667;line-height:1.7;}
.rc-bars{margin-top:8px;display:flex;flex-direction:column;gap:3px;}
.rcb-row{display:flex;align-items:center;gap:5px;}
.rcb-lbl{font-size:7px;color:#445;width:22px;}
.rcb-bg{flex:1;height:3px;background:rgba(255,255,255,.06);border-radius:99px;overflow:hidden;}
.rcb-fill{height:100%;border-radius:99px;}
.ss-rules{background:rgba(255,215,0,.06);border:1px solid rgba(255,215,0,.18);border-radius:10px;padding:10px 14px;margin-bottom:14px;font-size:9px;color:var(--gold);letter-spacing:1px;line-height:1.8;text-align:left;}
.ss-stats{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.ss-sc{padding:6px 10px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.ss-sv{font-family:'Rajdhani',sans-serif;font-size:14px;font-weight:900;color:#fff;}
.ss-sl{font-size:7px;color:#446;letter-spacing:2px;}
.ss-btn{display:inline-block;padding:12px 30px;background:linear-gradient(135deg,rgba(192,79,255,.22),rgba(108,99,255,.14));border:1px solid rgba(192,79,255,.48);border-radius:12px;font-family:'Black Han Sans',sans-serif;font-size:17px;color:var(--purple);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:2px;}
.ss-btn:hover{background:linear-gradient(135deg,rgba(192,79,255,.38),rgba(108,99,255,.28));transform:translateY(-2px);}
.ss-btn.gold{background:linear-gradient(135deg,rgba(245,197,24,.22),rgba(255,150,0,.14));border-color:rgba(245,197,24,.48);color:var(--gold);}
.ss-btn.red{background:linear-gradient(135deg,rgba(255,34,68,.22),rgba(192,79,255,.14));border-color:rgba(255,34,68,.48);color:var(--red);}

/* OVERLAY (title/end) */
#overlay{position:absolute;inset:0;z-index:400;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:30px 22px;background:linear-gradient(160deg,rgba(8,3,15,.98),rgba(14,6,24,.98));border:1px solid rgba(192,79,255,.22);border-radius:20px;min-width:340px;max-width:95vw;max-height:680px;overflow-y:auto;}
.ov-eye{font-size:7px;letter-spacing:4px;color:var(--purple);background:rgba(192,79,255,.1);border:1px solid rgba(192,79,255,.22);border-radius:99px;padding:3px 12px;display:inline-block;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(22px,5.5vw,36px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#aab;letter-spacing:4px;margin-bottom:14px;}
.char-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:14px;}
.cc{padding:10px 5px;background:var(--glass);border:1.5px solid var(--border);border-radius:12px;cursor:pointer;transition:all .18s;text-align:center;position:relative;}
.cc:hover{border-color:rgba(0,212,255,.35);}
.cc.sel{border-color:var(--blue);background:rgba(51,170,255,.12);box-shadow:0 0 16px rgba(51,170,255,.25);}
.cc-ico{font-size:28px;display:block;margin-bottom:3px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:11px;letter-spacing:1px;}
.cc-type{font-size:7px;color:#446;margin-top:2px;}
.cc-badge{position:absolute;top:4px;right:4px;font-size:6px;padding:1px 5px;border-radius:99px;font-weight:700;}
.diff-row{display:flex;gap:6px;justify-content:center;margin-bottom:14px;flex-wrap:wrap;}
.dt{padding:7px 13px;border-radius:99px;background:var(--glass);border:1px solid var(--border);font-size:9px;color:#556;cursor:pointer;transition:all .18s;text-align:center;}
.dt.sel{border-color:var(--gold);color:var(--gold);background:rgba(245,197,24,.08);}
.ov-btn{display:inline-block;padding:12px 30px;background:linear-gradient(135deg,rgba(192,79,255,.22),rgba(108,99,255,.14));border:1px solid rgba(192,79,255,.48);border-radius:12px;font-family:'Black Han Sans',sans-serif;font-size:17px;color:var(--purple);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(192,79,255,.38),rgba(108,99,255,.28));transform:translateY(-2px);}

@keyframes shake{0%,100%{transform:translate(0,0);}20%{transform:translate(-5px,3px);}40%{transform:translate(5px,-3px);}60%{transform:translate(-3px,2px);}80%{transform:translate(3px,-2px);}}
.shaking{animation:shake .18s ease;}
</style>
</head>
<body>
<div id="root">
  <div id="hud">
    <div class="hp-col">
      <div class="fn" id="fn-p1">P1</div>
      <div class="hp-wrap"><div id="hg-p1" style="width:100%"></div><div id="hf-p1" style="width:100%"></div></div>
    </div>
    <div class="center-hud"><div id="rnd-lbl">ROUND 1</div><div id="timer">99</div></div>
    <div class="hp-col">
      <div class="fn" id="fn-p2" style="text-align:right">CPU</div>
      <div class="hp-wrap"><div id="hg-p2" style="width:100%"></div><div id="hf-p2" style="width:100%"></div></div>
    </div>
  </div>
  <div id="superbars">
    <div class="sb-side" id="sb-p1"></div>
    <div id="super-lbl">SUPER</div>
    <div class="sb-side" id="sb-p2"></div>
  </div>
  <div id="arcade-progress">
    <div class="prog-dots" id="prog-dots"></div>
    <div id="stage-lbl">STAGE 1</div>
  </div>

  <div id="canvas-wrap">
    <canvas id="gc"></canvas>
    <div id="rnd-result"></div>
    <div id="combo-display"><div id="combo-n">0</div><div id="combo-hits">HIT COMBO</div></div>
    <div id="event-banner"><div id="eb-big">RIVAL FIGHT!</div><div id="eb-sub">특수 규칙 발동</div></div>
  </div>

  <div id="keys-hint">
    <div>← → 이동 | ↑/Z 점프 | ↓ 가드</div>
    <div>X/J 펀치 | C/K 킥 | B 강공격 | V/L 필살기</div>
    <div>M 슈퍼기술(게이지MAX)</div>
  </div>

  <div id="dpad">
    <div class="dp" id="dp-up">⬆</div>
    <div class="dp" id="dp-left">⬅</div>
    <div class="dp" id="dp-down">⬇</div>
    <div class="dp" id="dp-right">➡</div>
  </div>
  <div id="atk-btns">
    <div class="ab" id="ab-j"><span>⬆</span><span class="ab-lbl">점프</span></div>
    <div class="ab" id="ab-p"><span>👊</span><span class="ab-lbl">펀치</span></div>
    <div class="ab" id="ab-k"><span>🦵</span><span class="ab-lbl">킥</span></div>
    <div class="ab" id="ab-s"><span>✨</span><span class="ab-lbl">필살기</span></div>
  </div>

  <div id="stage-screen"><div class="ss-box" id="ssc"></div></div>
  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>
<script>
'use strict';
// ================================================================
//  스트리트 파이터 EX  v4.0  ─  ARCADE STORY MODE
//  8스테이지 스토리 진행 · 스테이지별 특수 규칙
//  라이벌전 · 태그전 · 핸디캡전 · 보스전 · 리매치
//  히트스톱 · 가드 · 기절 · 슈퍼기술 · 콤보 카운터
// ================================================================
const canvas=document.getElementById('gc');
const ctx=canvas.getContext('2d');
const cWrap=document.getElementById('canvas-wrap');

let CW=560,CH=380,SC=1;
function resize(){
  const w=cWrap.clientWidth||window.innerWidth||560;
  const h=cWrap.clientHeight||window.innerHeight||380;
  SC=Math.min(w/CW,h/CH);
  canvas.width=CW;canvas.height=CH;
  canvas.style.width=(CW*SC)+'px';canvas.style.height=(CH*SC)+'px';
  canvas.style.left=((w-CW*SC)/2)+'px';canvas.style.top=((h-CH*SC)/2)+'px';
}
setTimeout(resize,100);setTimeout(resize,500);
resize();window.addEventListener('resize',resize);

const KEYS={};
window.addEventListener('keydown',e=>{
  KEYS[e.code]=true;
  if(!G.running)return;
  // P1 attacks
  if(e.code==='KeyX'||e.code==='KeyJ')doAtk(P1,'punch',P2);
  if(e.code==='KeyC'||e.code==='KeyK')doAtk(P1,'kick',P2);
  if(e.code==='KeyB')doAtk(P1,'heavy',P2);
  if(e.code==='KeyV'||e.code==='KeyL')doAtk(P1,'special',P2);
  if(e.code==='KeyM')doAtk(P1,'super',P2);
  // P2 attacks (VS 2P 모드)
  if(vsMode){
    if(e.code==='Numpad1'||e.code==='KeyU')doAtk(P2,'punch',P1);
    if(e.code==='Numpad2'||e.code==='KeyI')doAtk(P2,'kick',P1);
    if(e.code==='Numpad3'||e.code==='KeyO')doAtk(P2,'heavy',P1);
    if(e.code==='Numpad0'||e.code==='KeyP')doAtk(P2,'special',P1);
    if(e.code==='NumpadEnter'||e.code==='BracketLeft')doAtk(P2,'super',P1);
  }
  ['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)&&e.preventDefault();
});
window.addEventListener('keyup',e=>KEYS[e.code]=false);

// ================================================================
//  CHARACTERS
// ================================================================
const CHARS=[
  {name:'류',emoji:'🥋',hp:220,atk:22,def:1.0,spd:4.6,jump:17,supCost:25,col:'#33aaff',type:'균형형',badge:'표준',badgeCol:'#33aaff',
   bars:[75,70,72,68],lore:'파동권의 후계자. 모든 면에서 균형잡힌 파이터.',
   moves:{punch:{dmg:22,kbx:4,kby:-2,reach:72,low:false,startup:5,active:4,recovery:6,stun:0},
          kick:{dmg:32,kbx:6,kby:-3,reach:88,low:false,startup:7,active:5,recovery:8,stun:0},
          heavy:{dmg:42,kbx:8,kby:-5,reach:80,low:false,startup:11,active:4,recovery:14,stun:8},
          low:{dmg:18,kbx:3,kby:0,reach:66,low:true,startup:4,active:4,recovery:5,stun:0},
          airPunch:{dmg:28,kbx:5,kby:-4,reach:68,low:false,startup:4,active:5,recovery:4,stun:0},
          special:{name:'파동권',emoji:'🌊',dmg:55,kbx:10,kby:-6,stun:12,cost:25,col:'#3399ff',isProjectile:true},
          super:{name:'승룡권',emoji:'🔥',dmg:110,kbx:6,kby:-14,stun:20,cost:100,col:'#ffaa00',isLauncher:true}}},
  {name:'블레이즈',emoji:'🔥',hp:195,atk:30,def:0.9,spd:5.4,jump:15,supCost:22,col:'#ff6600',type:'공격형',badge:'어택',badgeCol:'#ff4400',
   bars:[100,92,50,42],lore:'화염을 다루는 격투가. 압도적 공격력이 특기.',
   moves:{punch:{dmg:28,kbx:5,kby:-2,reach:70,low:false,startup:4,active:4,recovery:5,stun:0},
          kick:{dmg:38,kbx:7,kby:-3,reach:86,low:false,startup:6,active:5,recovery:7,stun:0},
          heavy:{dmg:50,kbx:10,kby:-5,reach:78,low:false,startup:10,active:4,recovery:13,stun:10},
          low:{dmg:22,kbx:4,kby:0,reach:64,low:true,startup:4,active:4,recovery:5,stun:0},
          airPunch:{dmg:34,kbx:6,kby:-5,reach:66,low:false,startup:4,active:5,recovery:4,stun:0},
          special:{name:'화염권',emoji:'💥',dmg:65,kbx:12,kby:-4,stun:14,cost:22,col:'#ff6600',isDash:true},
          super:{name:'인페르노',emoji:'🌋',dmg:130,kbx:8,kby:-10,stun:25,cost:100,col:'#ff3300',isProjectile:true}}},
  {name:'아이스',emoji:'❄️',hp:245,atk:18,def:1.3,spd:3.6,jump:19,supCost:28,col:'#88ccff',type:'수비형',badge:'탱커',badgeCol:'#4488cc',
   bars:[58,46,95,90],lore:'철벽 방어로 상대를 지치게 만드는 전략가.',
   moves:{punch:{dmg:20,kbx:3,kby:-1,reach:74,low:false,startup:6,active:5,recovery:6,stun:0},
          kick:{dmg:30,kbx:5,kby:-3,reach:90,low:false,startup:8,active:5,recovery:9,stun:0},
          heavy:{dmg:40,kbx:7,kby:-4,reach:82,low:false,startup:12,active:5,recovery:15,stun:10},
          low:{dmg:16,kbx:2,kby:0,reach:68,low:true,startup:5,active:4,recovery:5,stun:0},
          airPunch:{dmg:25,kbx:4,kby:-3,reach:70,low:false,startup:5,active:5,recovery:5,stun:0},
          special:{name:'빙결탄',emoji:'🧊',dmg:45,kbx:6,kby:-2,stun:18,cost:28,col:'#88ddff',isProjectile:true,freeze:true},
          super:{name:'빙하폭풍',emoji:'❄️',dmg:100,kbx:5,kby:-8,stun:30,cost:100,col:'#aaeeff',isFreeze:true}}},
  {name:'라이트닝',emoji:'⚡',hp:175,atk:26,def:0.85,spd:6.8,jump:21,supCost:20,col:'#f5c518',type:'스피드형',badge:'스피드',badgeCol:'#cc9900',
   bars:[82,100,42,38],lore:'눈에 보이지 않는 속도. 10번의 주먹이 순식간에.',
   moves:{punch:{dmg:23,kbx:5,kby:-2,reach:66,low:false,startup:3,active:3,recovery:4,stun:0},
          kick:{dmg:34,kbx:7,kby:-3,reach:82,low:false,startup:5,active:4,recovery:6,stun:0},
          heavy:{dmg:44,kbx:9,kby:-5,reach:76,low:false,startup:9,active:3,recovery:11,stun:8},
          low:{dmg:20,kbx:4,kby:0,reach:62,low:true,startup:3,active:3,recovery:4,stun:0},
          airPunch:{dmg:30,kbx:6,kby:-5,reach:64,low:false,startup:3,active:4,recovery:3,stun:0},
          special:{name:'전격',emoji:'⚡',dmg:60,kbx:11,kby:-8,stun:10,cost:20,col:'#ffee00',isDash:true},
          super:{name:'뇌신강림',emoji:'🌩️',dmg:120,kbx:6,kby:-12,stun:22,cost:100,col:'#ffff00',isLauncher:true}}},
  {name:'철권',emoji:'🦾',hp:260,atk:34,def:1.2,spd:3.2,jump:13,supCost:30,col:'#c04fff',type:'파워형',badge:'파워',badgeCol:'#8822cc',
   bars:[90,80,88,96],lore:'압도적 체중과 파괴력. 한 방에 경기가 끝난다.',
   moves:{punch:{dmg:32,kbx:6,kby:-2,reach:68,low:false,startup:7,active:5,recovery:8,stun:5},
          kick:{dmg:46,kbx:9,kby:-4,reach:84,low:false,startup:9,active:5,recovery:11,stun:8},
          heavy:{dmg:60,kbx:14,kby:-6,reach:78,low:false,startup:14,active:5,recovery:18,stun:15},
          low:{dmg:28,kbx:5,kby:0,reach:64,low:true,startup:6,active:4,recovery:7,stun:5},
          airPunch:{dmg:40,kbx:8,kby:-5,reach:66,low:false,startup:6,active:5,recovery:6,stun:5},
          special:{name:'지진권',emoji:'💥',dmg:70,kbx:14,kby:-3,stun:20,cost:30,col:'#cc44ff',isSlam:true},
          super:{name:'오버드라이브',emoji:'💪',dmg:150,kbx:10,kby:-14,stun:35,cost:100,col:'#ff00ff',isLauncher:true}}},
  {name:'닌자',emoji:'🥷',hp:188,atk:25,def:0.88,spd:6.2,jump:22,supCost:22,col:'#00ff88',type:'민첩형',badge:'닌자',badgeCol:'#00aa55',
   bars:[78,95,55,50],lore:'그림자처럼 움직이는 분신술의 달인.',
   moves:{punch:{dmg:22,kbx:4,kby:-2,reach:68,low:false,startup:4,active:4,recovery:5,stun:0},
          kick:{dmg:33,kbx:6,kby:-3,reach:84,low:false,startup:6,active:4,recovery:7,stun:0},
          heavy:{dmg:44,kbx:8,kby:-5,reach:78,low:false,startup:10,active:4,recovery:12,stun:8},
          low:{dmg:19,kbx:3,kby:0,reach:64,low:true,startup:4,active:4,recovery:5,stun:0},
          airPunch:{dmg:29,kbx:5,kby:-5,reach:66,low:false,startup:3,active:4,recovery:3,stun:0},
          special:{name:'분신 베기',emoji:'👥',dmg:58,kbx:9,kby:-7,stun:12,cost:22,col:'#00ff88',isDash:true},
          super:{name:'천수관음',emoji:'🌀',dmg:115,kbx:7,kby:-11,stun:22,cost:100,col:'#88ffcc',isMultiHit:true}}},
  // HIDDEN BOSS
  {name:'다크 류',emoji:'😈',hp:300,atk:38,def:1.1,spd:5.0,jump:18,supCost:20,col:'#ff0044',type:'보스형',badge:'BOSS',badgeCol:'#ff0044',
   bars:[110,110,88,80],lore:'어둠에 잠식된 최강의 파이터. 모든 기술이 강화되어있다.',
   moves:{punch:{dmg:38,kbx:7,kby:-3,reach:76,low:false,startup:4,active:5,recovery:6,stun:5},
          kick:{dmg:52,kbx:10,kby:-5,reach:92,low:false,startup:6,active:5,recovery:8,stun:8},
          heavy:{dmg:68,kbx:14,kby:-7,reach:84,low:false,startup:10,active:5,recovery:14,stun:15},
          low:{dmg:30,kbx:6,kby:0,reach:70,low:true,startup:4,active:4,recovery:5,stun:5},
          airPunch:{dmg:44,kbx:8,kby:-7,reach:72,low:false,startup:3,active:5,recovery:4,stun:5},
          special:{name:'암흑파동',emoji:'🌑',dmg:85,kbx:14,kby:-8,stun:18,cost:20,col:'#880000',isProjectile:true},
          super:{name:'멸살권',emoji:'💀',dmg:200,kbx:12,kby:-18,stun:40,cost:100,col:'#ff0044',isLauncher:true}}},
];

// ================================================================
//  ARCADE STAGE DEFINITIONS
// ================================================================
const STAGES=[
  {stageN:1, cpuIdx:0, ruleKey:'normal',   title:'첫 번째 도전자',   rounds:2,
   rule:'표준 2선승제',    ruleTip:'기본 규칙. 상대를 파악하자.',       bg:'neon'},
  {stageN:2, cpuIdx:1, ruleKey:'normal',   title:'불꽃의 투사',       rounds:2,
   rule:'표준 2선승제',    ruleTip:'공격적인 상대. 가드를 적극 활용!',   bg:'fire'},
  {stageN:3, cpuIdx:2, ruleKey:'handicap', title:'핸디캡전',           rounds:2,
   rule:'⚠️ 핸디캡전: P1 HP 70%로 시작!', ruleTip:'불리한 조건. 슈퍼 게이지를 빠르게 모아라.', bg:'ice'},
  {stageN:4, cpuIdx:3, ruleKey:'timeKill', title:'타임 어택',          rounds:2,
   rule:'⏱️ 타임어택: 제한 60초!',         ruleTip:'시간이 줄었다. 공격적으로 싸워라.',         bg:'lightning'},
  {stageN:5, cpuIdx:5, ruleKey:'rival',    title:'🔥 라이벌전!',       rounds:3,
   rule:'🏆 라이벌전: 3선승제!',           ruleTip:'숙명의 라이벌. 반드시 꺾어야 한다.',       bg:'neon'},
  {stageN:6, cpuIdx:4, ruleKey:'superCharged', title:'슈퍼 게이지 전',  rounds:2,
   rule:'💫 슈퍼 게이지가 계속 차오른다!', ruleTip:'처음부터 슈퍼 기술을 쓸 수 있다.',        bg:'purple'},
  {stageN:7, cpuIdx:1, ruleKey:'sudden',   title:'서든데스',            rounds:1,
   rule:'☠️ 서든데스: 선취점 승리!',        ruleTip:'단 한 방이라도 먼저 맞으면 진다.',          bg:'dark'},
  {stageN:8, cpuIdx:6, ruleKey:'boss',     title:'👹 최후의 보스',      rounds:3,
   rule:'💀 보스전: 3선승제 · 보스 HP 150%!', ruleTip:'전설의 보스. 모든 것을 쏟아내라.',      bg:'boss'},
];

// ================================================================
//  PARTICLES + HELPERS
// ================================================================
let PARTS=[],HITS=[],PROJS=[];
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
function spawnHN(x,y,txt,col){HITS.push({x,y:y-18,txt,col,life:1,vy:-.55});}
function tickParts(){
  for(let i=PARTS.length-1;i>=0;i--){const p=PARTS[i];p.x+=p.vx;p.y+=p.vy;p.vx*=.88;p.vy*=.88;p.life-=p.dec;p.life<=0&&PARTS.splice(i,1);}
  for(let i=HITS.length-1;i>=0;i--){const h=HITS[i];h.y+=h.vy;h.life-=.022;h.life<=0&&HITS.splice(i,1);}
}

// ================================================================
//  GAME STATE
// ================================================================
let G={running:false},P1,P2;
let selChar=0,selChar2=1,diffLv=1;
let vsMode=false; // false=아케이드(CPU) true=2P대전
let arcadeStage=0, p1StageWins=0, cpuStageWins=0, roundN=1, roundActive=false, roundTimer=0;
let arcadeScore=0, arcadePerfects=0, arcadeMaxCombo=0;
let superChargeMode=false; // for stage 6

const FLOOR=()=>CH-72;
const GRAV=0.88;

function makeF(cIdx,isP2){
  const c=CHARS[cIdx];
  const stage=STAGES[arcadeStage];
  let hpMul=1;
  if(isP2&&stage.ruleKey==='boss') hpMul=1.5;
  if(!isP2&&stage.ruleKey==='handicap') hpMul=0.7;
  const hp=Math.round(c.hp*hpMul);
  return{
    x:isP2?CW*.74:CW*.22,y:FLOOR(),vx:0,vy:0,
    char:c,facing:isP2?-1:1,
    hp,maxHp:hp,super:superChargeMode?100:0,stun:0,stunMax:0,
    onGround:true,state:'idle',stateT:0,animF:0,
    hitCD:0,invT:0,hitstop:0,
    comboN:0,comboT:0,
    blocking:false,blockT:0,blockLow:false,
    airAtk:false,curMove:null,
    _tL:false,_tR:false,_tJ:false,_tDown:false,
    ai:{rt:0,aggro:.65,phase:'neutral'},
    isP2,
  };
}

// ================================================================
//  COMBAT
// ================================================================
function doAtk(f,moveKey,opp){
  if(f.stateT>0&&!['idle','walk'].includes(f.state))return;
  if(['ko','stun'].includes(f.state))return;
  const move=f.char.moves[moveKey];
  if(!move)return;
  if(moveKey==='special'&&f.super<move.cost)return;
  if(moveKey==='super'&&f.super<100)return;
  f.state=moveKey;f.stateT=move.startup+(move.active||5)+(move.recovery||8);
  f.curMove={...move,_key:moveKey,_hit:false};
  if(moveKey==='special')f.super=Math.max(0,f.super-move.cost);
  if(moveKey==='super')f.super=0;
  if(moveKey==='special'||moveKey==='super')spawnP(f.x,f.y,{n:14,col:move.col,glow:true,vMax:6,szMax:8});
  if(move.isProjectile){
    PROJS.push({x:f.x+f.facing*40,y:f.y-40,vx:f.facing*(moveKey==='super'?13:9),vy:0,
      life:85,sz:moveKey==='super'?22:16,col:move.col,owner:f,dmg:move.dmg,
      kb:{x:move.kbx,y:move.kby},stun:move.stun||0,freeze:move.freeze||false});
  }
  if(move.isDash){f.vx=f.facing*10;f.vy=-3;}
  if(move.isLauncher){f.vy=-2;}
  if(move.isMultiHit){
    for(let i=1;i<=4;i++)setTimeout(()=>{
      if(!roundActive)return;
      const tgt=f.isP2?P1:P2;
      if(Math.abs(f.x-tgt.x)<90)applyHit(f,tgt,move.dmg*.4,{x:move.kbx*.3,y:move.kby*.3},0,true);
    },i*80);
  }
}

function applyHit(atk,def,dmg,kb,stun,skipState){
  if(def.state==='ko'||def.hitCD>0||def.invT>0)return;
  // ── 퍼펙트 가드 / 카운터 ──
  // 가드 버튼을 공격 직전 12프레임 내에 눌렀으면 퍼펙트 가드
  if(def.blocking&&def.blockT>0){
    const move=atk.curMove;
    const isLow=move&&move.low;
    if(!isLow||def.blockLow){
      // 퍼펙트 가드 판정: blockT가 높을수록(방금 눌렀을수록) 퍼펙트
      const isPerfect = def.blockT >= 18; // 18프레임 이내 = 퍼펙트
      if(isPerfect){
        // 피해 0 + 카운터 데미지
        const ctrDmg = Math.round(dmg * 0.4);
        atk.hp=Math.max(0,atk.hp-ctrDmg);
        def.vx=0;
        spawnP(def.x,def.y,{n:22,col:['#00ffcc','#ffffff','#44ffff'],glow:true,vMax:8,szMax:10});
        spawnHN(def.x,def.y-48,'⚡ PERFECT!','#00ffcc');
        spawnHN(atk.x,atk.y-38,'-'+ctrDmg+'','#ff4444');
        atk.hitstop=8;def.hitstop=8;
        atk.super=Math.min(100,atk.super+3);def.super=Math.min(100,def.super+8);
        triggerHPGhost(atk);triggerHPGhost(def);return;
      }
      // 일반 가드
      def.hp=Math.max(0,def.hp-Math.round(dmg*.1));
      def.vx=atk.facing*2;
      spawnP(def.x,def.y,{n:5,col:'rgba(180,220,255,.7)',glow:true,vMax:3});
      spawnHN(def.x,def.y-38,'GUARD!','#4499ff');
      atk.hitstop=4;def.hitstop=4;
      atk.super=Math.min(100,atk.super+4);def.super=Math.min(100,def.super+3);
      triggerHPGhost(def);return;
    }
  }
  // Sudden death: 1 hit = KO
  if(STAGES[arcadeStage].ruleKey==='sudden'){
    def.hp=0;
  }else{
    def.hp=Math.max(0,def.hp-Math.round(dmg/def.char.def));
  }
  def.vx=atk.facing*kb.x;def.vy=kb.y;
  def.hitCD=12;def.invT=8;
  if(stun>0){def.stun=Math.min(def.stun+stun,def.stunMax+stun);def.stunMax+=stun;}
  atk.comboN++;atk.comboT=100;
  atk.super=Math.min(100,atk.super+(superChargeMode?15:9));
  def.super=Math.min(100,def.super+(superChargeMode?8:5));
  spawnP(def.x,def.y,{n:12,col:[atk.char.col,'#ffaa44','#fff'],glow:true,vMax:6,szMax:7});
  const rd=Math.round(dmg/def.char.def);
  spawnHN(def.x,def.y-30,rd+'',atk.comboN>2?'#f5c518':'#ffaa44');
  if(rd>60)spawnHN(def.x,def.y-50,rd>100?'BRUTAL!':'HEAVY!',atk.char.col);
  if(!skipState){def.state=def.onGround?'hurt':'airHurt';def.stateT=14+(rd>40?8:0);}
  atk.hitstop=stun>0?10:6;def.hitstop=stun>0?10:6;
  screenShake();
  if(arcadeMaxCombo<atk.comboN)arcadeMaxCombo=atk.comboN;
  if(def.hp<=0){
    def.state='ko';def.stateT=200;def.vy=-5;def.vx=atk.facing*6;
    roundEnd(atk.isP2?'cpu':'p1');
  }
  triggerHPGhost(def);
  if(atk.comboN>=2)showComboDisplay(atk.comboN,atk.char.col,atk.isP2);
}

function triggerHPGhost(f){
  const id=f.isP2?'hg-p2':'hg-p1';
  const el=document.getElementById(id);
  if(el)el.style.width=(f.hp/f.maxHp*100)+'%';
}
function screenShake(){
  cWrap.classList.remove('shaking');void cWrap.offsetWidth;cWrap.classList.add('shaking');
  setTimeout(()=>cWrap.classList.remove('shaking'),200);
}

// ================================================================
//  AI
// ================================================================
const AI_AGGRESSIONS=[.52,.72,.92];
const AI_REACT=[16,9,5];

function updateAI(cpu,opp){
  if(cpu.hitstop>0)return;
  cpu.ai.rt--;if(cpu.ai.rt>0)return;
  cpu.ai.rt=AI_REACT[diffLv]+Math.random()*8|0;
  const dx=opp.x-cpu.x,dist=Math.abs(dx),aggro=AI_AGGRESSIONS[diffLv];
  cpu.facing=dx>0?1:-1;
  const r=Math.random();
  // Boss stage: more aggressive
  const aBoost=STAGES[arcadeStage].ruleKey==='boss'?.15:0;
  const eff=Math.min(1,aggro+aBoost);
  if(cpu.super>=100&&dist<120&&r<eff*.5){doAtk(cpu,'super',opp);return;}
  if(cpu.hp/cpu.maxHp<.25&&cpu.super>=cpu.char.supCost&&r<eff*.55){doAtk(cpu,'super',opp);return;}
  if(dist<105){
    const rr=r*100;
    if(rr<eff*28)doAtk(cpu,'punch',opp);
    else if(rr<eff*52)doAtk(cpu,'kick',opp);
    else if(rr<eff*62)doAtk(cpu,'heavy',opp);
    else if(rr<eff*70&&cpu.super>=cpu.char.supCost)doAtk(cpu,'special',opp);
    else if(rr<eff*73)doAtk(cpu,'low',opp);
    else if(rr<82&&cpu.onGround&&r<.55){cpu.vy=-cpu.char.jump;cpu.onGround=false;cpu.state='jump';}
    else{cpu.blocking=true;cpu.blockT=22;}
  }else if(dist<200){
    if(r<eff*.55)cpu.vx=cpu.facing*cpu.char.spd*.9;
    else if(r<eff*.65&&cpu.super>=cpu.char.supCost)doAtk(cpu,'special',opp);
    else if(r<eff*.7&&cpu.onGround){cpu.vy=-cpu.char.jump;cpu.onGround=false;cpu.state='jump';}
    else cpu.vx=cpu.facing*cpu.char.spd*.5;
  }else{
    if(r<eff*.68)cpu.vx=cpu.facing*cpu.char.spd*.88;
    else if(r<eff*.75&&cpu.super>=cpu.char.supCost)doAtk(cpu,'special',opp);
    else cpu.vx=cpu.facing*cpu.char.spd*.4;
  }
}

// ================================================================
//  FIGHTER UPDATE
// ================================================================
function updateFighter(f,opp){
  if(f.hitstop>0){f.hitstop--;return;}
  f.vy+=GRAV;f.y+=f.vy;f.x+=f.vx;f.vx*=(f.onGround?.7:.88);
  if(f.y>=FLOOR()){
    f.y=FLOOR();f.vy=0;f.onGround=true;f.airAtk=false;
    if(['jump','airHurt'].includes(f.state)){f.state='idle';f.stateT=0;}
  }else f.onGround=false;
  f.x=Math.max(24,Math.min(CW-24,f.x));
  if(Math.abs(f.x-opp.x)>CW*.73)f.x+=(opp.x-f.x)*.035;
  if(f.stateT>0)f.stateT--;
  else if(!['idle','walk','jump','block','ko','stun'].includes(f.state)){f.state='idle';f.curMove=null;}
  if(f.hitCD>0)f.hitCD--;if(f.invT>0)f.invT--;
  if(f.blockT>0)f.blockT--;else f.blocking=false;
  if(f.comboT>0)f.comboT--;else if(f.comboT===0){f.comboN=0;comboOff();}
  if(f.stun>0){f.stun--;if(f.stun>0&&f.state!=='ko')f.state='stun';else if(f.state==='stun'){f.state='idle';f.stunMax=0;}}
  f.animF=(f.animF+1)%60;
  if(['idle','walk'].includes(f.state))f.facing=opp.x>f.x?1:-1;
  // Super charge mode
  if(superChargeMode&&f.frame%90===0)f.super=Math.min(100,f.super+15);
  // Attack hitbox
  const cm=f.curMove;
  if(cm&&!cm._hit&&!cm.isProjectile&&!cm.isDash&&!cm.isLauncher&&!cm.isMultiHit&&!cm.isSlam&&!cm.isFreeze){
    const prog=(cm.startup+(cm.active||5)+(cm.recovery||8))-f.stateT;
    if(prog>=cm.startup&&prog<cm.startup+(cm.active||5)){
      const hx=f.x+f.facing*cm.reach*.55,hy=f.y-40;
      if(Math.abs(hx-opp.x)<cm.reach*.88&&Math.abs(hy-(opp.y-40))<80){
        applyHit(f,opp,cm.dmg*f.char.atk/22,{x:cm.kbx,y:cm.kby},cm.stun||0);cm._hit=true;
      }
    }
  }
  if(cm&&!cm._hit&&(cm.isDash||cm.isSlam||cm.isLauncher)){
    if(Math.abs(f.x-opp.x)<100&&f.stateT<(cm.recovery||8)+(cm.active||5)){
      applyHit(f,opp,cm.dmg*f.char.atk/22,{x:cm.kbx,y:cm.kby},cm.stun||0);cm._hit=true;
      if(cm.isLauncher){opp.vy=-12;opp.onGround=false;}
      if(cm.isSlam)spawnP(f.x,f.y,{n:20,col:f.char.col,glow:true,vMax:8,szMax:10});
    }
  }
}

function handlePlayerInput(p,opp){
  if(p.hitstop>0)return;
  const gl=KEYS['ArrowLeft']||KEYS['KeyA']||p._tL;
  const gr=KEYS['ArrowRight']||KEYS['KeyD']||p._tR;
  const gj=KEYS['ArrowUp']||KEYS['KeyZ']||p._tJ;
  const gd=KEYS['ArrowDown']||KEYS['KeyS']||p._tDown;
  const holdBack=(p.facing===1&&gl)||(p.facing===-1&&gr);
  if(gd&&holdBack){p.blocking=true;p.blockT=4;p.blockLow=true;}
  else if(holdBack&&p.onGround){p.blocking=true;p.blockT=4;p.blockLow=false;}
  if(['idle','walk'].includes(p.state)){
    if(gl){p.vx=-p.char.spd;p.state='walk';}
    else if(gr){p.vx=p.char.spd;p.state='walk';}
    else{p.vx*=.55;if(Math.abs(p.vx)<.5)p.state='idle';}
    if(gj&&p.onGround){p.vy=-p.char.jump;p.onGround=false;p.state='jump';}
  }
}

// P2 별도 입력 핸들러 (2P VS 모드)
function handleP2Input(p,opp){
  if(p.hitstop>0)return;
  // P2: WASD 이동, E 점프
  const gl=KEYS['KeyA']||p._tL;
  const gr=KEYS['KeyD']||p._tR;
  const gj=KEYS['KeyW']||KEYS['KeyE']||p._tJ;
  const gd=KEYS['KeyS']||p._tDown;
  const holdBack=(p.facing===1&&gl)||(p.facing===-1&&gr);
  if(gd&&holdBack){p.blocking=true;p.blockT=4;p.blockLow=true;}
  else if(holdBack&&p.onGround){p.blocking=true;p.blockT=4;p.blockLow=false;}
  if(['idle','walk'].includes(p.state)){
    if(gl){p.vx=-p.char.spd;p.state='walk';}
    else if(gr){p.vx=p.char.spd;p.state='walk';}
    else{p.vx*=.55;if(Math.abs(p.vx)<.5)p.state='idle';}
    if(gj&&p.onGround){p.vy=-p.char.jump;p.onGround=false;p.state='jump';}
  }
}

function updateProjs(){
  for(let i=PROJS.length-1;i>=0;i--){
    const pr=PROJS[i];pr.x+=pr.vx;pr.life--;
    if(pr.life%2===0)spawnP(pr.x,pr.y,{n:2,col:pr.col,vMin:0,vMax:.8,szMin:1,szMax:pr.sz*.5,dMin:.1,dMax:.15,glow:true});
    const opp=pr.owner.isP2?P1:P2;
    const dx=pr.x-opp.x,dy=pr.y-(opp.y-40);
    if(Math.abs(dx)<opp.char.atk*.08+pr.sz&&Math.abs(dy)<55){
      applyHit(pr.owner,opp,pr.dmg,pr.kb,pr.stun||0);
      if(pr.freeze)opp.stun=Math.max(opp.stun,45);
      spawnP(pr.x,pr.y,{n:18,col:[pr.col,'#fff'],glow:true,vMax:7,szMax:8});
      PROJS.splice(i,1);continue;
    }
    if(pr.life<=0||pr.x<-60||pr.x>CW+60)PROJS.splice(i,1);
  }
}

// ================================================================
//  ROUND / STAGE SYSTEM
// ================================================================
function startRound(){
  const stage=vsMode?{cpuIdx:selChar2,ruleKey:'normal',rounds:3}:STAGES[arcadeStage];
  const cpuChar=CHARS[stage.cpuIdx];
  P1=makeF(selChar,false);P2=makeF(stage.cpuIdx,true);P2.facing=-1;
  PROJS=[];PARTS=[];HITS=[];
  roundTimer=(stage.ruleKey==='timeKill'?60:99)*60;
  roundActive=true;
  document.getElementById('rnd-lbl').textContent='ROUND '+roundN;
  document.getElementById('fn-p1').textContent=CHARS[selChar].name;
  document.getElementById('fn-p2').textContent=vsMode?'P2 · '+cpuChar.name:cpuChar.name;
  document.getElementById('fn-p2').style.color=cpuChar.col;
  document.getElementById('hf-p2').style.background=`linear-gradient(90deg,#ff0022,${cpuChar.col})`;
  document.getElementById('hg-p1').style.width='100%';
  document.getElementById('hg-p2').style.width='100%';
  if(!vsMode)updateProgress();buildSuperBars();comboOff();
}

function roundEnd(winner){\n  roundActive=false;\n  const res=document.getElementById('rnd-result');\n  const stage=vsMode?{rounds:3}:STAGES[arcadeStage];\n  const maxRounds=stage.rounds;\n  if(winner==='p1'){\n    p1StageWins++;\n    res.style.color='var(--blue)';res.textContent='🏆 P1 WIN!';\n    if(!vsMode&&P1.hp===P1.maxHp){arcadeScore+=500;arcadePerfects++;}\n    if(!vsMode)arcadeScore+=200+Math.round((P1.hp/P1.maxHp)*300);\n  }else{\n    cpuStageWins++;\n    res.style.color='var(--red)';res.textContent=vsMode?'🏆 P2 WIN!':'CPU WIN!';\n  }\n  res.style.opacity='1';\n  setTimeout(()=>{\n    res.style.opacity='0';\n    const needWins=Math.ceil(maxRounds/2+.5);\n    if(vsMode){\n      if(p1StageWins>=needWins||cpuStageWins>=needWins){ showVSResult(); }\n      else{ roundN++;startRound(); }\n    }else{\n      if(p1StageWins>=needWins){ stageWon(); }\n      else if(cpuStageWins>=needWins){ stageLost(); }\n      else{ roundN++;startRound(); }\n    }\n  },2200);\n}

// ── VS 2P 결과 ──
function showVSResult(){
  G.running=false;
  const winner=p1StageWins>cpuStageWins?'P1':'P2';
  const wChar=p1StageWins>cpuStageWins?CHARS[selChar]:CHARS[selChar2];
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-eye">2P VS MODE</div>
    <div class="ov-title" style="color:var(--gold)">🏆 ${winner} WIN!</div>
    <div style="font-size:52px;margin:10px 0">${wChar.emoji}</div>
    <div style="font-family:'Black Han Sans',sans-serif;font-size:16px;color:${wChar.col};letter-spacing:2px;margin-bottom:16px">${wChar.name}</div>
    <div class="ss-stats" style="justify-content:center">
      <div class="ss-sc"><div class="ss-sv" style="color:var(--blue)">${p1StageWins}</div><div class="ss-sl">P1 승</div></div>
      <div class="ss-sc"><div class="ss-sv" style="color:var(--red)">${cpuStageWins}</div><div class="ss-sl">P2 승</div></div>
    </div>
    <button class="ov-btn" onclick="window.startVS()">리매치 🥊</button>
    <br><button class="ov-btn2" onclick="showTitle()">모드 선택</button>
  </div>`;
  ov.style.display='flex';
}

window.startVS=function(){
  document.getElementById('overlay').style.display='none';
  vsMode=true;
  p1StageWins=0;cpuStageWins=0;roundN=1;
  arcadeScore=0;arcadePerfects=0;arcadeMaxCombo=0;
  superChargeMode=false;PROJS=[];PARTS=[];HITS=[];
  initStars(); updateProgress();
  G={running:true}; startRound(); requestAnimationFrame(loop);
};

function stageWon(){
  arcadeStage++;
  if(arcadeStage>=STAGES.length){
    // ALL STAGES CLEARED
    showArcadeClear();return;
  }
  p1StageWins=0;cpuStageWins=0;roundN=1;
  superChargeMode=(STAGES[arcadeStage].ruleKey==='superCharged');
  showStageScreen('win');
}

function stageLost(){
  showStageScreen('lose');
}

// ================================================================
//  STAGE SCREEN (between stages)
// ================================================================
function showStageScreen(type){
  G.running=false;
  const ss=document.getElementById('stage-screen');
  const ssc=document.getElementById('ssc');
  const nextStage=STAGES[arcadeStage];
  const nextCpuChar=nextStage?CHARS[nextStage.cpuIdx]:null;
  const bnames=['속도','공격','방어','체력'];

  if(type==='win'&&nextStage){
    const barsH=nextCpuChar.bars.map((v,bi)=>
      `<div class="rcb-row"><div class="rcb-lbl">${bnames[bi]}</div><div class="rcb-bg"><div class="rcb-fill" style="width:${Math.min(100,v)}%;background:${nextCpuChar.col}"></div></div></div>`).join('');
    ssc.innerHTML=`
      <div class="ss-eye">STAGE ${nextStage.stageN} / ${STAGES.length}</div>
      <div class="ss-title" style="color:var(--gold)">${nextStage.title}</div>
      <div class="ss-rival">다음 상대</div>
      <div class="rival-card">
        <div class="rc-ico">${nextCpuChar.emoji}</div>
        <div><div class="rc-name" style="color:${nextCpuChar.col}">${nextCpuChar.name}</div>
          <div class="rc-type">${nextCpuChar.type}</div>
          <div class="rc-desc">${nextCpuChar.lore}</div>
          <div class="rc-bars">${barsH}</div>
        </div>
      </div>
      <div class="ss-rules">⚡ 규칙: ${nextStage.rule}<br>💡 ${nextStage.ruleTip}</div>
      <div class="ss-stats">
        <div class="ss-sc"><div class="ss-sv" style="color:var(--gold)">${arcadeScore.toLocaleString()}</div><div class="ss-sl">누적 점수</div></div>
        <div class="ss-sc"><div class="ss-sv" style="color:var(--red)">${arcadePerfects}</div><div class="ss-sl">퍼펙트</div></div>
        <div class="ss-sc"><div class="ss-sv" style="color:var(--cyan)">${arcadeMaxCombo}</div><div class="ss-sl">최고 콤보</div></div>
      </div>
      <button class="ss-btn gold" onclick="continueArcade()">다음 스테이지 ⚡</button>`;
  }else if(type==='lose'){
    ssc.innerHTML=`
      <div class="ss-eye">CONTINUE?</div>
      <div class="ss-title" style="color:var(--red)">💀 패배...</div>
      <div class="ss-rival">STAGE ${STAGES[arcadeStage].stageN} — ${STAGES[arcadeStage].title}</div>
      <div class="ss-rules">포기하지 마! 다시 도전하면 같은 스테이지부터 시작한다.<br>이번엔 상대의 패턴을 파악했을 것이다.</div>
      <div class="ss-stats">
        <div class="ss-sc"><div class="ss-sv" style="color:var(--gold)">${arcadeScore.toLocaleString()}</div><div class="ss-sl">현재 점수</div></div>
        <div class="ss-sc"><div class="ss-sv" style="color:var(--cyan)">${arcadeMaxCombo}</div><div class="ss-sl">최고 콤보</div></div>
      </div>
      <button class="ss-btn" style="margin-right:8px" onclick="retryStage()">다시 도전 🔄</button>
      <button class="ss-btn red" onclick="showTitle()">처음부터 💀</button>`;
  }
  ss.style.display='flex';
}

window.continueArcade=function(){
  document.getElementById('stage-screen').style.display='none';
  G.running=true;startRound();requestAnimationFrame(loop);
};
window.retryStage=function(){
  p1StageWins=0;cpuStageWins=0;roundN=1;
  document.getElementById('stage-screen').style.display='none';
  G.running=true;startRound();requestAnimationFrame(loop);
};

// ================================================================
//  ARCADE CLEAR
// ================================================================
function showArcadeClear(){
  const best=Math.max(arcadeScore,parseInt(localStorage.getItem('sfBest')||'0'));
  localStorage.setItem('sfBest',best);
  document.getElementById('stage-screen').style.display='none';
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-eye">🏆 ARCADE CLEAR!</div>
    <div class="ov-title" style="color:var(--gold)">👑 챔피언 달성!</div>
    <div class="ov-sub">ALL 8 STAGES CLEARED</div>
    <div style="font-size:36px;margin-bottom:12px">${CHARS[selChar].emoji}</div>
    <div style="font-family:'Black Han Sans',sans-serif;font-size:14px;color:${CHARS[selChar].col};letter-spacing:2px;margin-bottom:14px">${CHARS[selChar].name}의 전설이 시작된다!</div>
    <div class="ss-stats" style="justify-content:center">
      <div class="ss-sc"><div class="ss-sv" style="color:var(--gold)">${arcadeScore.toLocaleString()}</div><div class="ss-sl">최종 점수</div></div>
      <div class="ss-sc"><div class="ss-sv" style="color:var(--red)">${arcadePerfects}</div><div class="ss-sl">퍼펙트</div></div>
      <div class="ss-sc"><div class="ss-sv" style="color:var(--cyan)">${arcadeMaxCombo}HIT</div><div class="ss-sl">최고 콤보</div></div>
    </div>
    <div style="font-size:9px;color:#446;margin-bottom:14px">🏆 최고기록: <span style="color:var(--gold)">${best.toLocaleString()}</span> PT</div>
    <button class="ov-btn" onclick="startArcade()">다시 플레이 🏆</button>
    <br><button class="ov-btn2" onclick="showTitle()">캐릭터 변경</button>
  </div>`;
  ov.style.display='flex';
}

// ================================================================
//  PROGRESS HUD
// ================================================================
function updateProgress(){
  const dots=document.getElementById('prog-dots');dots.innerHTML='';
  STAGES.forEach((s,i)=>{
    const d=document.createElement('div');
    d.className='pdot'+(s.ruleKey==='boss'?' boss':'');
    if(i<arcadeStage)d.classList.add('done');
    if(i===arcadeStage)d.classList.add('current');
    d.title=s.title;
    if(s.ruleKey==='boss')d.textContent='👹';
    else if(s.ruleKey==='rival')d.textContent='🔥';
    else if(i<arcadeStage)d.textContent='✓';
    dots.appendChild(d);
  });
  document.getElementById('stage-lbl').textContent='STAGE '+STAGES[arcadeStage].stageN+' / '+STAGES.length;
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
    segs.forEach((s,i)=>{
      s.style.width=Math.min(100,Math.max(0,(p.super-i*25)*4))+'%';
      s.closest('.sseg').classList.toggle('full',p.super>=(i+1)*25);
    });
  });
}
function updateHPBars(){
  document.getElementById('hf-p1').style.width=(P1.hp/P1.maxHp*100)+'%';
  document.getElementById('hf-p2').style.width=(P2.hp/P2.maxHp*100)+'%';
}

// COMBO
let comboDT=0;
function showComboDisplay(n,col,isP2){
  const cd=document.getElementById('combo-display');
  cd.style.left=isP2?'14px':'auto';cd.style.right=isP2?'auto':'14px';cd.style.top='50%';cd.style.transform='translateY(-50%)';
  document.getElementById('combo-n').textContent=n;document.getElementById('combo-n').style.color=col;
  cd.style.opacity='1';comboDT=90;
}
function comboOff(){document.getElementById('combo-display').style.opacity='0';}

// ================================================================
//  DRAW
// ================================================================
let bgStars=[];
function initStars(){bgStars=[];for(let i=0;i<80;i++)bgStars.push({x:Math.random()*CW,y:Math.random()*CH*.45,r:Math.random()<.05?1.2:.6,a:.2+Math.random()*.7});}

function drawBg(){
  // Sky
  const st=STAGES[arcadeStage];
  const bgCols={
    neon:  ['#0a0318','#180530','#1a0340'],
    fire:  ['#180a03','#2a0a00','#1a0500'],
    ice:   ['#030a18','#050a20','#030818'],
    lightning:['#0a0a03','#181800','#0a0a00'],
    purple:['#0e0318','#1a0530','#150228'],
    dark:  ['#050505','#0a0a0a','#080808'],
    boss:  ['#180003','#2a0005','#1a0004'],
  };
  const cols=bgCols[st.bg]||bgCols.neon;
  const sky=ctx.createLinearGradient(0,0,0,CH);
  sky.addColorStop(0,cols[0]);sky.addColorStop(.55,cols[1]);sky.addColorStop(1,cols[2]);
  ctx.fillStyle=sky;ctx.fillRect(0,0,CW,CH);
  // Stars
  for(const s of bgStars){ctx.save();ctx.globalAlpha=s.a*(st.bg==='dark'?.3:1);ctx.fillStyle='rgba(220,200,255,1)';ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fill();ctx.restore();}
  // City
  ctx.fillStyle={neon:'#0d0320',fire:'#1a0500',ice:'#030a18',lightning:'#0a0a03',purple:'#0e0318',dark:'#030303',boss:'#1a0003'}[st.bg]||'#0d0320';
  for(let ci=0;ci<18;ci++){
    const bw=18+Math.sin(ci*1.9)*9+5,bh=42+Math.sin(ci*2.4)*36+14,bx=ci*(CW/17)-10;
    ctx.fillRect(bx,CH*.22-bh,bw,bh);
    for(let wy=CH*.22-bh+4;wy<CH*.22-3;wy+=9){
      if(Math.random()<.55)continue;
      const lc=Math.random()<.4?'0,200,255':'255,180,50';
      ctx.fillStyle=`rgba(${lc},.25)`;ctx.fillRect(bx+3+Math.floor(Math.random()*(bw-8)),wy,3,6);
      ctx.fillStyle={neon:'#0d0320',fire:'#1a0500',ice:'#030a18',lightning:'#0a0a03',purple:'#0e0318',dark:'#030303',boss:'#1a0003'}[st.bg]||'#0d0320';
    }
  }
  // Ground
  const gr=ctx.createLinearGradient(0,CH*.7,0,CH);
  const gCols={neon:['#1a0040','#0e0025'],fire:['#3a0005','#200003'],ice:['#001830','#000a18'],
    lightning:['#201800','#100e00'],purple:['#1a0040','#100028'],dark:['#050505','#020202'],boss:['#300008','#1a0004']};
  const gc=gCols[st.bg]||gCols.neon;
  gr.addColorStop(0,gc[0]);gr.addColorStop(1,gc[1]);
  ctx.fillStyle=gr;ctx.fillRect(0,CH*.7,CW,CH*.3);
  // Floor neon
  const floorCols={neon:'rgba(192,79,255,.45)',fire:'rgba(255,60,0,.45)',ice:'rgba(0,180,255,.45)',
    lightning:'rgba(255,220,0,.45)',purple:'rgba(192,79,255,.45)',dark:'rgba(100,100,100,.3)',boss:'rgba(255,0,50,.55)'};
  ctx.save();ctx.strokeStyle=floorCols[st.bg]||floorCols.neon;ctx.shadowColor=floorCols[st.bg];ctx.shadowBlur=16;ctx.lineWidth=2.5;
  ctx.beginPath();ctx.moveTo(0,FLOOR()+5);ctx.lineTo(CW,FLOOR()+5);ctx.stroke();ctx.restore();
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

let gFrame=0;
function drawFighter(f){
  const x=f.x,y=f.y,h=f.char.hp*.35;
  ctx.save();ctx.translate(x,y);if(f.facing===-1)ctx.scale(-1,1);
  let sz=1,offY=0,rot=0,glow=null,alpha=1;
  if(f.state==='punch'){sz=1.18;ctx.shadowColor=f.char.col;ctx.shadowBlur=12;ctx.font='22px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('👊',h*.28,f.stateT>8?-h*.5:-h*.6);ctx.shadowBlur=0;}
  else if(f.state==='kick'){sz=1.1;ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('🦵',h*.22,-h*.28);}
  else if(f.state==='heavy'){sz=1.25;glow=f.char.col;ctx.shadowColor=f.char.col;ctx.shadowBlur=14;ctx.font='24px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('👊',h*.3,f.stateT>10?-h*.45:-h*.62);ctx.shadowBlur=0;}
  else if(f.state==='low'){sz=.88;offY=12;ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('👊',h*.25,-h*.1);}
  else if(f.state==='airPunch'){sz=1.15;rot=-f.facing*.22;ctx.shadowColor=f.char.col;ctx.shadowBlur=10;ctx.font='20px serif';ctx.textAlign='left';ctx.textBaseline='middle';ctx.fillText('👊',h*.22,-h*.55);ctx.shadowBlur=0;}
  else if(f.state==='jump'){offY=-8-Math.abs(f.vy)*2.2;rot=f.facing*.14;}
  else if(f.state==='hurt'||f.state==='airHurt'){sz=.88;rot=f.facing*-.18;ctx.filter='brightness(2.5) hue-rotate(310deg)';alpha=f.hitCD%2===0?.6:1;}
  else if(f.state==='stun'){sz=.85;offY=5;rot=Math.sin(f.animF*.25)*.1;ctx.filter='brightness(2) sepia(1)';
    ['⭐','✨','💫'].forEach((s,si)=>{ctx.save();ctx.font='14px serif';ctx.textAlign='center';const sa=f.animF*.15+si*(Math.PI*2/3);ctx.fillText(s,Math.cos(sa)*24,-h*.75+Math.sin(sa)*12);ctx.restore();});}
  else if(f.state==='block'||f.blocking){ctx.save();ctx.strokeStyle='rgba(0,200,255,.5)';ctx.shadowColor='rgba(0,200,255,.4)';ctx.shadowBlur=16;ctx.lineWidth=2.5;ctx.fillStyle='rgba(0,200,255,.1)';ctx.beginPath();ctx.arc(h*.22,-h*.44,h*.62,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.restore();}
  else if(f.state==='special'){sz=1.3;glow=f.char.col;spawnP(x,y,{n:2,col:f.char.col,glow:true,vMax:4,szMax:6,dMin:.06,dMax:.1});}
  else if(f.state==='super'){sz=1.4;glow=f.char.col;if(f.animF%4<2)ctx.filter='brightness(3) saturate(2)';spawnP(x,y,{n:3,col:[f.char.col,'#fff'],glow:true,vMax:5,szMax:8,dMin:.05,dMax:.09});}
  else if(f.state==='ko'){rot=f.facing*.8;offY=14;sz=.82;}
  else if(f.state==='idle'||f.state==='walk'){offY=Math.sin(f.animF*.1)*2;}
  ctx.rotate(rot);ctx.globalAlpha*=alpha;ctx.font=`${h*1.15*sz}px serif`;ctx.textAlign='center';ctx.textBaseline='bottom';
  if(glow){ctx.shadowBlur=24;ctx.shadowColor=glow;}
  ctx.fillText(f.char.emoji,0,-h*.02+offY);
  if(glow)ctx.shadowBlur=0;ctx.restore();
  // Super aura
  if(f.super>=100){ctx.save();ctx.strokeStyle=f.char.col+'88';ctx.lineWidth=2.5;ctx.shadowBlur=14+Math.sin(gFrame*.07)*7;ctx.shadowColor=f.char.col;ctx.beginPath();ctx.arc(f.x,f.y-h*.5,h*.78+Math.sin(gFrame*.06)*5,0,Math.PI*2);ctx.stroke();ctx.restore();}
  if(f.stun>0&&f.stun%8<3){ctx.save();ctx.strokeStyle='#ffee00';ctx.lineWidth=2;ctx.globalAlpha=.5;ctx.beginPath();ctx.arc(f.x,f.y-h*.5,h*.85,0,Math.PI*2);ctx.stroke();ctx.restore();}
  // Shadow
  ctx.save();ctx.globalAlpha=.28;ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(x,FLOOR()+7,h*.7+12,8,0,0,Math.PI*2);ctx.fill();ctx.restore();
}

function drawProjs(){
  for(const pr of PROJS){ctx.save();ctx.shadowBlur=22;ctx.shadowColor=pr.col;ctx.fillStyle=pr.col;ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz,0,Math.PI*2);ctx.fill();ctx.fillStyle='rgba(255,255,255,.85)';ctx.beginPath();ctx.arc(pr.x,pr.y,pr.sz*.35,0,Math.PI*2);ctx.fill();ctx.restore();}
}
function drawParts(){
  for(const p of PARTS){ctx.save();ctx.globalAlpha=Math.max(0,p.life);if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.sz*Math.max(.08,p.life),0,Math.PI*2);ctx.fill();if(p.glow)ctx.shadowBlur=0;ctx.restore();}
  for(const h of HITS){ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;ctx.fillStyle=h.col;ctx.font="bold 12px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.fillText(h.txt,h.x,h.y);ctx.restore();}
}

// ================================================================
//  MAIN LOOP
// ================================================================
function loop(){
  if(!G.running)return;
  gFrame++;
  if(comboDT>0){comboDT--;if(comboDT===0)comboOff();}
  ctx.clearRect(0,0,CW,CH);
  drawBg();drawParts();drawProjs();drawFighter(P1);drawFighter(P2);drawParts();
  if(roundActive){
    roundTimer--;
    const sec=Math.max(0,Math.ceil(roundTimer/60));
    document.getElementById('timer').textContent=sec;
    document.getElementById('timer').classList.toggle('low',sec<=10);
    if(roundTimer<=0){const w=P1.hp>=P2.hp?'p1':'cpu';roundEnd(w);}
    updateFighter(P1,P2);updateFighter(P2,P1);
    updateProjs();
    if(vsMode){ handleP2Input(P2,P1); } else { updateAI(P2,P1); }
    handlePlayerInput(P1,P2);
    updateSuperBars();updateHPBars();
    // Supercharge mode: passive fill
    if(superChargeMode&&gFrame%90===0){P1.super=Math.min(100,P1.super+15);P2.super=Math.min(100,P2.super+15);}
    tickParts();
  }else tickParts();
  requestAnimationFrame(loop);
}

// ================================================================
//  TITLE
// ================================================================
function showTitle(){
  initStars();
  document.getElementById('overlay').style.display='flex';
  document.getElementById('stage-screen').style.display='none';
  const dnames=['신병 🟢','특전사 🟡','전설 🔴'],ddesc=['느린 AI·입문용','균형 AI·표준','공격적 AI·고수용'];
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">ARCADE MODE · 8 STAGES</div>
    <div class="ov-title" style="color:var(--purple)">🥊 스트리트<br>파이터 EX</div>
    <div class="ov-sub">8 STAGES · STORY · BOSS · SPECIAL RULES</div>
    <div style="font-size:9px;color:#446;line-height:1.9;margin-bottom:12px;background:rgba(245,197,24,.06);border:1px solid rgba(245,197,24,.18);border-radius:8px;padding:8px 12px;text-align:left">
      🏆 <b style="color:var(--gold)">아케이드 모드</b> — 8명의 상대를 순서대로 격파하라!<br>
      🔥 Stage 5: 라이벌전(3선승제) &nbsp;|&nbsp; ⚠️ Stage 3: 핸디캡전<br>
      ☠️ Stage 7: 서든데스 &nbsp;|&nbsp; 👹 Stage 8: 최종 보스전
    </div>
    <div style="font-size:9px;color:var(--blue);letter-spacing:2px;margin-bottom:6px;font-weight:700">🎮 P1 캐릭터 선택</div>
    <div class="char-grid" id="cg"></div>
    <div id="vs-p2-section" style="display:none">
      <div style="font-size:9px;color:var(--red);letter-spacing:2px;margin-bottom:6px;margin-top:10px;font-weight:700">🎮 P2 캐릭터 선택</div>
      <div class="char-grid" id="cg2"></div>
      <div style="font-size:8px;color:#446;line-height:2.2;margin:10px 0;background:rgba(255,34,68,.06);border:1px solid rgba(255,34,68,.18);border-radius:8px;padding:8px 12px;text-align:left">
        P1: ← → 이동 | ↑/Z 점프 | ↓ 가드 | X 펀치 | C 킥 | B 강공격 | V 필살기 | M 슈퍼기술<br>
        P2: A D 이동 | W 점프 | S 가드 | U 펀치 | I 킥 | O 강공격 | P 필살기 | [ 슈퍼기술
      </div>
      <button class="ov-btn" style="background:linear-gradient(135deg,rgba(255,34,68,.22),rgba(192,79,255,.14));border-color:rgba(255,34,68,.55);color:var(--red)" onclick="window.startVS()">2P 대전 시작 🥊</button>
    </div>
    <div id="vs-arcade-section">
      <div style="font-size:8px;color:#336;margin-bottom:8px;letter-spacing:2px">CPU 난이도</div>
      <div class="diff-row">${dnames.map((n,i)=>`<div class="dt${i===diffLv?' sel':''}" onclick="setDiff(${i})"><div>${n}</div><div style="font-size:7px;color:#446;margin-top:1px">${ddesc[i]}</div></div>`).join('')}</div>
      <div style="font-size:8px;color:#334;line-height:2.3;margin-bottom:12px">
        ← → 이동 | ↑/Z 점프 | ↓ 가드<br>
        X/J 펀치 | C/K 킥 | B 강공격 | V/L 필살기 | M 슈퍼기술
      </div>
      <button class="ov-btn" onclick="startArcade()">아케이드 시작 🏆</button>
      <br><button class="ov-btn" style="margin-top:8px;background:linear-gradient(135deg,rgba(255,34,68,.18),rgba(100,80,200,.1));border-color:rgba(255,34,68,.4);color:var(--red)" onclick="toggleVSMode()">👥 2P 대전 모드</button>
    </div>`;
  buildCharGrid();
}

window.toggleVSMode=function(){
  const s1=document.getElementById('vs-arcade-section');
  const s2=document.getElementById('vs-p2-section');
  const isVS=s2.style.display==='block';
  s2.style.display=isVS?'none':'block';
  s1.style.display=isVS?'block':'none';
  if(!isVS) buildCharGrid2();
};

function buildCharGrid(){
  const g=document.getElementById('cg');if(!g)return;g.innerHTML='';
  CHARS.slice(0,6).forEach((c,i)=>{
    const d=document.createElement('div');d.className='cc'+(i===selChar?' sel':'');
    d.innerHTML=`<div class="cc-badge" style="background:${c.badgeCol}22;color:${c.badgeCol};border:1px solid ${c.badgeCol}44">${c.badge}</div><span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-type">${c.type}</div>`;
    d.onclick=()=>{selChar=i;g.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};
    g.appendChild(d);
  });
}

function buildCharGrid2(){
  const g=document.getElementById('cg2');if(!g)return;g.innerHTML='';
  CHARS.slice(0,6).forEach((c,i)=>{
    const d=document.createElement('div');d.className='cc'+(i===selChar2?' sel':'');
    d.innerHTML=`<div class="cc-badge" style="background:${c.badgeCol}22;color:${c.badgeCol};border:1px solid ${c.badgeCol}44">${c.badge}</div><span class="cc-ico">${c.emoji}</span><div class="cc-name" style="color:${c.col}">${c.name}</div><div class="cc-type">${c.type}</div>`;
    d.onclick=()=>{selChar2=i;g.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');};
    g.appendChild(d);
  });
}
window.setDiff=d=>{diffLv=d;document.querySelectorAll('.dt').forEach((t,i)=>t.classList.toggle('sel',i===d));};

window.startArcade=function(){
  document.getElementById('overlay').style.display='none';
  vsMode=false;
  arcadeStage=0;p1StageWins=0;cpuStageWins=0;roundN=1;
  arcadeScore=0;arcadePerfects=0;arcadeMaxCombo=0;
  superChargeMode=false;PROJS=[];PARTS=[];HITS=[];
  initStars();updateProgress();
  // Show first stage intro
  const st=STAGES[0];const cpuChar=CHARS[st.cpuIdx];
  const ssc=document.getElementById('ssc');
  const bnames=['속도','공격','방어','체력'];
  const barsH=cpuChar.bars.map((v,bi)=>
    `<div class="rcb-row"><div class="rcb-lbl">${bnames[bi]}</div><div class="rcb-bg"><div class="rcb-fill" style="width:${Math.min(100,v)}%;background:${cpuChar.col}"></div></div></div>`).join('');
  ssc.innerHTML=`
    <div class="ss-eye">STAGE 1 / ${STAGES.length}</div>
    <div class="ss-title" style="color:var(--gold)">${st.title}</div>
    <div class="ss-rival">첫 번째 도전자</div>
    <div class="rival-card"><div class="rc-ico">${cpuChar.emoji}</div>
      <div><div class="rc-name" style="color:${cpuChar.col}">${cpuChar.name}</div><div class="rc-type">${cpuChar.type}</div><div class="rc-desc">${cpuChar.lore}</div><div class="rc-bars">${barsH}</div></div>
    </div>
    <div class="ss-rules">⚡ 규칙: ${st.rule}<br>💡 ${st.ruleTip}</div>
    <button class="ss-btn gold" onclick="continueArcade()">대전 시작 ⚡</button>`;
  document.getElementById('stage-screen').style.display='flex';
  G={running:false};
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
addT('dp-left', ()=>{if(G.running)P1._tL=true;},()=>P1._tL=false);
addT('dp-right',()=>{if(G.running)P1._tR=true;},()=>P1._tR=false);
addT('dp-up',   ()=>{if(G.running)P1._tJ=true;},()=>P1._tJ=false);
addT('dp-down', ()=>{if(G.running)P1._tDown=true;},()=>P1._tDown=false);
addT('ab-j',    ()=>{if(G.running)P1._tJ=true;},()=>P1._tJ=false);
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
