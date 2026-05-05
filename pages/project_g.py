import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>좀비 아포칼립스</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{--red:#ff2244;--green:#00ff88;--gold:#f5c518;--cyan:#00d4ff;--purple:#c04fff;--orange:#ff7700;--bg:#050809;--glass:rgba(255,255,255,.04);--border:rgba(255,255,255,.07);}
html,body{width:100%;height:728px;overflow:hidden;background:var(--bg);font-family:'Orbitron',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100%;height:728px;overflow:hidden;}
canvas{position:absolute;top:0;left:0;}

/* HUD */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;background:linear-gradient(180deg,rgba(0,0,0,.88)0%,transparent 100%);padding:10px 14px;display:flex;align-items:flex-start;gap:7px;pointer-events:none;}
.hb{background:rgba(0,0,0,.45);border:1px solid var(--border);border-radius:9px;padding:4px 10px;text-align:center;}
.hv{font-family:'Rajdhani',sans-serif;font-size:19px;font-weight:900;color:#fff;letter-spacing:1px;line-height:1.1;}
.hl{font-size:7px;color:#445;letter-spacing:2px;text-transform:uppercase;}
#hp-block{padding:6px 10px;min-width:110px;}
#hp-lbl{font-size:7px;color:#633;letter-spacing:3px;margin-bottom:3px;}
#hp-bg{height:11px;background:rgba(255,0,50,.08);border:1px solid rgba(255,0,50,.2);border-radius:99px;overflow:hidden;}
#hp-bar{height:100%;background:linear-gradient(90deg,#7b0000,#cc1122,#ff5566);border-radius:99px;transition:width .1s;}
#hud-right{margin-left:auto;display:flex;flex-direction:column;align-items:flex-end;gap:5px;}

/* KILL STREAK */
#streak-box{position:absolute;top:68px;left:14px;z-index:100;pointer-events:none;text-align:center;}
#streak-num{font-family:'Black Han Sans',sans-serif;font-size:28px;color:var(--red);text-shadow:0 0 18px rgba(255,34,68,.8);opacity:0;transition:opacity .15s;line-height:1;}
#streak-lbl{font-size:7px;color:#445;letter-spacing:2px;}

/* WAVE ANNOUNCE */
#wave-ann{position:absolute;top:46%;left:50%;transform:translate(-50%,-50%);z-index:200;pointer-events:none;text-align:center;opacity:0;transition:opacity .22s;}
#wa-big{font-family:'Black Han Sans',sans-serif;font-size:clamp(26px,6vw,40px);letter-spacing:4px;text-shadow:0 0 30px currentColor;}
#wa-sub{font-size:11px;color:var(--gold);letter-spacing:3px;margin-top:4px;}

/* WEAPON BAR */
#weapbar{position:absolute;bottom:0;left:0;right:0;z-index:100;background:linear-gradient(transparent,rgba(0,0,0,.82)100%);padding:8px 10px 10px;display:flex;gap:6px;justify-content:center;pointer-events:auto;}
.wslot{min-width:60px;height:72px;border-radius:11px;background:rgba(0,0,0,.52);border:1.5px solid rgba(255,255,255,.08);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;transition:all .18s;position:relative;padding:3px 5px;}
.wslot.active{border-color:var(--gold);box-shadow:0 0 18px rgba(245,197,24,.38);}
.wslot.empty{opacity:.3;pointer-events:none;}
.ws-ico{font-size:22px;}
.ws-name{font-size:6px;color:#667;letter-spacing:1px;margin-top:2px;text-align:center;}
.ws-ammo{position:absolute;top:3px;right:5px;font-size:8px;color:var(--gold);font-weight:900;}
.ws-key{position:absolute;bottom:3px;left:5px;font-size:7px;color:#334;}
.ws-type{position:absolute;top:3px;left:4px;font-size:6px;color:#336;}

/* AMMO BAR */
#ammo-bar{position:absolute;bottom:90px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;align-items:center;gap:3px;}
.ammo-col{display:flex;flex-direction:column;gap:2px;}
.adot{width:9px;height:18px;border-radius:3px;background:rgba(245,197,24,.1);border:1px solid rgba(245,197,24,.18);transition:all .1s;}
.adot.live{background:var(--gold);box-shadow:0 0 5px rgba(245,197,24,.6);}
#ammo-label{font-size:7px;color:#555;letter-spacing:2px;margin-top:2px;}

/* RELOAD RING */
#rl-ring{position:absolute;bottom:110px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;text-align:center;display:none;}
#rl-cv{display:block;margin:0 auto 2px;}
#rl-text{font-size:7px;color:var(--gold);letter-spacing:2px;}

/* JOYSTICK */
#joyzone{position:absolute;bottom:92px;left:16px;width:108px;height:108px;z-index:100;border-radius:50%;background:rgba(255,255,255,.03);border:1.5px solid rgba(255,255,255,.07);}
#knob{position:absolute;width:44px;height:44px;border-radius:50%;background:radial-gradient(circle at 35% 35%,rgba(255,255,255,.2),rgba(255,255,255,.07));border:1.5px solid rgba(255,255,255,.18);top:50%;left:50%;transform:translate(-50%,-50%);transition:transform .05s;}

/* FIRE / RELOAD BUTTONS */
#fire-btn{position:absolute;bottom:108px;right:14px;width:76px;height:76px;border-radius:50%;z-index:100;background:rgba(255,34,68,.18);border:2px solid rgba(255,34,68,.48);display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:30px;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;}
#fire-btn:active,#fire-btn.pr{background:rgba(255,34,68,.4);transform:scale(.9);box-shadow:0 0 20px rgba(255,34,68,.55);}
#rl-btn{position:absolute;bottom:196px;right:22px;width:52px;height:52px;border-radius:50%;z-index:100;background:rgba(245,197,24,.1);border:1.5px solid rgba(245,197,24,.35);display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:17px;cursor:pointer;user-select:none;touch-action:none;transition:all .1s;}
#rl-btn:active{background:rgba(245,197,24,.28);}
.rb-lbl{font-size:7px;color:var(--gold);letter-spacing:1px;margin-top:1px;}

/* KILL FEED */
#killfeed{position:absolute;top:70px;right:14px;z-index:100;pointer-events:none;display:flex;flex-direction:column;gap:3px;max-width:180px;}
.kfe{background:rgba(0,0,0,.52);border-left:3px solid var(--red);padding:4px 8px;font-size:8px;color:#ccc;border-radius:0 6px 6px 0;animation:kfs .25s ease;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
@keyframes kfs{from{opacity:0;transform:translateX(14px);}to{opacity:1;transform:none;}}

/* VIGNETTE */
#vignette{position:absolute;inset:0;z-index:90;pointer-events:none;opacity:0;background:radial-gradient(ellipse at center,transparent 38%,rgba(255,0,30,.6)100%);transition:opacity .1s;}
#shield-ov{position:absolute;inset:0;z-index:88;pointer-events:none;opacity:0;background:rgba(192,79,255,.04);}

/* BOSS HP BAR */
#boss-bar{position:absolute;top:60px;left:50%;transform:translateX(-50%);z-index:100;pointer-events:none;width:min(320px,85vw);display:none;}
#boss-lbl{font-family:'Black Han Sans',sans-serif;font-size:12px;color:var(--red);text-align:center;letter-spacing:2px;margin-bottom:4px;text-shadow:0 0 12px rgba(255,34,68,.7);}
#boss-bg{height:12px;background:rgba(255,0,50,.1);border:1px solid rgba(255,0,50,.3);border-radius:99px;overflow:hidden;}
#boss-fill{height:100%;background:linear-gradient(90deg,#7b0000,#cc1122,#ff5566);border-radius:99px;transition:width .1s;}

/* SHOP */
#shop{position:absolute;inset:0;z-index:300;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;backdrop-filter:blur(4px);}
.shop-box{background:linear-gradient(160deg,#040a0c,#060e10);border:1px solid rgba(0,212,255,.18);border-radius:18px;padding:26px 20px;width:min(490px,95vw);max-height:90vh;overflow-y:auto;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:22px;color:var(--cyan);text-align:center;letter-spacing:3px;margin-bottom:3px;}
.shop-wave{font-size:8px;color:#335;text-align:center;letter-spacing:3px;margin-bottom:4px;}
.shop-coins{text-align:center;font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:var(--gold);margin-bottom:14px;}
.shop-section{font-size:8px;color:#336;letter-spacing:3px;text-transform:uppercase;margin-bottom:8px;padding-bottom:3px;border-bottom:1px solid rgba(255,255,255,.05);}
.shop-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;}
.si{background:var(--glass);border:1px solid var(--border);border-radius:11px;padding:11px;cursor:pointer;transition:all .18s;text-align:center;}
.si:hover{border-color:rgba(245,197,24,.4);background:rgba(245,197,24,.06);}
.si.bought{opacity:.38;pointer-events:none;}
.si-ico{font-size:22px;margin-bottom:3px;}
.si-name{font-size:11px;font-weight:700;letter-spacing:1px;}
.si-desc{font-size:8px;color:#445;margin-top:3px;line-height:1.6;}
.si-cost{font-size:11px;color:var(--gold);margin-top:6px;font-weight:900;}
.si-owned{font-size:9px;color:var(--green);margin-top:4px;}
.shop-cont{display:block;width:100%;padding:12px;background:linear-gradient(135deg,rgba(0,212,255,.18),rgba(108,99,255,.12));border:1px solid rgba(0,212,255,.4);border-radius:11px;font-family:'Black Han Sans',sans-serif;font-size:16px;color:var(--cyan);cursor:pointer;letter-spacing:2px;text-align:center;transition:all .2s;margin-top:4px;}
.shop-cont:hover{background:linear-gradient(135deg,rgba(0,212,255,.32),rgba(108,99,255,.24));transform:translateY(-2px);}

/* OVERLAY */
#overlay{position:absolute;inset:0;z-index:400;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.93);}
.ov-box{text-align:center;padding:32px 22px;background:linear-gradient(160deg,#040a0c,#060e10);border:1px solid rgba(0,255,136,.18);border-radius:20px;min-width:310px;max-width:94vw;max-height:90vh;overflow-y:auto;}
.ov-eye{font-size:7px;letter-spacing:4px;color:var(--green);background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.2);border-radius:99px;padding:3px 12px;display:inline-block;margin-bottom:12px;}
.ov-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(24px,6vw,36px);letter-spacing:3px;line-height:1.1;margin-bottom:4px;}
.ov-sub{font-size:8px;color:#335;letter-spacing:4px;margin-bottom:16px;}
.stats-row{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:14px;}
.sc{padding:6px 12px;background:var(--glass);border:1px solid var(--border);border-radius:8px;text-align:center;}
.sv{font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:900;color:#fff;}
.sl{font-size:7px;color:#446;letter-spacing:2px;}
.ov-btn{display:inline-block;padding:12px 30px;background:linear-gradient(135deg,rgba(255,34,68,.2),rgba(192,79,255,.12));border:1px solid rgba(255,34,68,.45);border-radius:12px;font-family:'Black Han Sans',sans-serif;font-size:16px;color:var(--red);cursor:pointer;letter-spacing:2px;transition:all .2s;margin-top:4px;}
.ov-btn:hover{background:linear-gradient(135deg,rgba(255,34,68,.38),rgba(192,79,255,.26));transform:translateY(-2px);box-shadow:0 8px 24px rgba(255,34,68,.3);}
.tag-strip{overflow:hidden;margin-bottom:14px;}
.tag-inner{display:flex;gap:8px;animation:tgs 16s linear infinite;width:max-content;}
@keyframes tgs{0%{transform:translateX(0);}100%{transform:translateX(-50%)}}
.tpill{font-size:8px;border:1px solid var(--border);border-radius:99px;padding:3px 11px;white-space:nowrap;letter-spacing:1px;color:#445;}
.tpill.c{color:var(--cyan);border-color:rgba(0,212,255,.3);}
.tpill.g{color:var(--gold);border-color:rgba(245,197,24,.3);}
.tpill.r{color:var(--red);border-color:rgba(255,34,68,.3);}
.tpill.p{color:var(--purple);border-color:rgba(192,79,255,.3);}

#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,0.82);backdrop-filter:blur(4px);display:flex;justify-content:center;align-items:center;gap:16px;padding:5px 12px;font-size:10px;color:#778;letter-spacing:1px;flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,0.06);}
#ctrl-bar span{color:#aab;}
#ctrl-bar b{color:#00ff88;font-weight:700;}
</style>
</head>
<body>
  <div id="ctrl-bar">
    <span><b>W A S D</b> 이동</span>
    <span>|</span>
    <span><b>마우스</b> 조준·발사</span>
    <span>|</span>
    <span><b>R</b> 재장전  <b>1~5</b> 무기교체</span>
    <span>|</span>
    <span><b>Q</b> 화염탄  <b>E</b> 섬광탄  <b>T</b> 공중폭격</span>
  </div>
<div id="root">
  <canvas id="bgc"></canvas>
  <canvas id="gc"></canvas>

  <div id="hud">
    <div class="hb" id="hp-block">
      <div id="hp-lbl">HP</div>
      <div id="hp-bg"><div id="hp-bar" style="width:100%"></div></div>
    </div>
    <div class="hb"><div class="hv" id="wave-v">1</div><div class="hl">WAVE</div></div>
    <div class="hb"><div class="hv" id="kill-v">0</div><div class="hl">KILLS</div></div>
    <div class="hb"><div class="hv" id="score-v">0</div><div class="hl">SCORE</div></div>
    <div id="hud-right"><div class="hb"><div class="hv" id="coin-v" style="color:var(--gold)">💰 0</div><div class="hl">COINS</div></div></div>
  </div>

  <div id="streak-box"><div id="streak-num">🔥×5</div><div id="streak-lbl">STREAK</div></div>
  <div id="boss-bar"><div id="boss-lbl">👹 BOSS</div><div id="boss-bg"><div id="boss-fill" style="width:100%"></div></div></div>
  <div id="wave-ann"><div id="wa-big" style="color:var(--red)">WAVE!</div><div id="wa-sub"></div></div>
  <div id="barricade-hint" style="display:none;position:absolute;top:10px;left:50%;transform:translateX(-50%);z-index:250;background:rgba(0,0,0,.85);border:1.5px solid #c8860a;border-radius:8px;padding:8px 18px;font-size:11px;color:#c8860a;letter-spacing:1px;pointer-events:none;"></div>

  <div id="ammo-bar"><div class="ammo-col" id="ammo-col"></div><div id="ammo-label">AMMO</div></div>
  <div id="rl-ring"><canvas id="rl-cv" width="52" height="52"></canvas><div id="rl-text">장전중...</div></div>

  <div id="joyzone"><div id="knob"></div></div>
  <div id="fire-btn">🔫</div>
  <div id="rl-btn"><span>🔄</span><span class="rb-lbl">R</span></div>
  <div id="weapbar"></div>
  <div id="killfeed"></div>
  <div id="vignette"></div>
  <div id="shield-ov"></div>

  <!-- 특수 스킬바 -->
  <div id="skill-hud" style="position:absolute;bottom:8px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:90;pointer-events:none;">
    <div style="text-align:center;">
      <div style="width:48px;height:48px;background:rgba(255,100,0,.15);border:1px solid rgba(255,100,0,.5);border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:20px;position:relative;">🔥<div id="sk-cd-fire" style="position:absolute;inset:0;border-radius:8px;background:rgba(0,0,0,.65);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:#ff8800;"></div></div>
      <div style="font-size:9px;color:#884400;margin-top:2px;">Q 화염탄</div>
    </div>
    <div style="text-align:center;">
      <div style="width:48px;height:48px;background:rgba(255,255,0,.1);border:1px solid rgba(255,255,0,.4);border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:20px;position:relative;">💥<div id="sk-cd-flash" style="position:absolute;inset:0;border-radius:8px;background:rgba(0,0,0,.65);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:#ffff44;"></div></div>
      <div style="font-size:9px;color:#888800;margin-top:2px;">E 섬광탄</div>
    </div>
    <div style="text-align:center;">
      <div style="width:48px;height:48px;background:rgba(255,50,50,.12);border:1px solid rgba(255,50,50,.4);border-radius:8px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:20px;position:relative;">💣<div id="sk-cd-airstrike" style="position:absolute;inset:0;border-radius:8px;background:rgba(0,0,0,.65);display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:900;color:#ff4444;"></div></div>
      <div style="font-size:9px;color:#882222;margin-top:2px;">T 폭격</div>
    </div>
  </div>

  <div id="shop">
    <div class="shop-box">
      <div class="shop-title">🛒 무기 상점</div>
      <div class="shop-wave" id="shop-wave-txt"></div>
      <div class="shop-coins" id="shop-coins-txt"></div>
      <div class="shop-section">무기 구매</div>
      <div class="shop-grid" id="shop-weapons"></div>
      <div class="shop-section">업그레이드</div>
      <div class="shop-grid" id="shop-upgrades"></div>
      <button class="shop-cont" id="shop-cont">다음 웨이브 시작 ⚡</button>
    </div>
  </div>

  <div id="overlay"><div class="ov-box" id="ovc"></div></div>
</div>
<script>
'use strict';
// ================================================================
//  좀비 아포칼립스 v3.0
//  탑다운 좀비 슈터 · 5종 무기 · 10+ 웨이브 · 보스 시스템
//  상점 업그레이드 · 킬스트릭 · 혈흔 · 파티클 · 조이스틱
//  5종 좀비 타입 · 폭발/결빙/독 특수효과 · 드롭 아이템
// ================================================================
const bgc=document.getElementById('bgc');
const bgCtx=bgc.getContext('2d');
const canvas=document.getElementById('gc');
const ctx=canvas.getContext('2d');
const root=document.getElementById('root');

function resize(){canvas.width=bgc.width=root.clientWidth||window.innerWidth||730;canvas.height=bgc.height=root.clientHeight||window.innerHeight||560;}
resize();window.addEventListener('resize',()=>{resize();drawBg();});
setTimeout(()=>{resize();drawBg();},100);setTimeout(()=>{resize();drawBg();},500);

// ================================================================
//  DATA DEFS
// ================================================================
const WDEFS=[
  {id:0,name:'권총',   emoji:'🔫',dmg:30, rof:18,mag:12,maxMag:12,relSpd:80, bSpd:17,spread:.04,auto:false,cost:0,  desc:'빠른 재장전·단발',  col:'#00d4ff',pellets:1,pierce:false},
  {id:1,name:'샷건',   emoji:'💥',dmg:24, rof:40,mag:8, maxMag:8, relSpd:135,bSpd:13,spread:.23,auto:false,cost:90, desc:'근거리 산탄·강력',   col:'#ff7700',pellets:7,pierce:false},
  {id:2,name:'돌격소총',emoji:'⚙️',dmg:22, rof:7, mag:30,maxMag:30,relSpd:108,bSpd:22,spread:.07,auto:true, cost:130,desc:'완전자동·높은 DPS',  col:'#00ff88',pellets:1,pierce:false},
  {id:3,name:'스나이퍼',emoji:'🎯',dmg:140,rof:68,mag:5, maxMag:5, relSpd:165,bSpd:34,spread:.01,auto:false,cost:220,desc:'원샷 킬·관통',        col:'#c04fff',pellets:1,pierce:true},
  {id:4,name:'로켓런처',emoji:'🚀',dmg:200,rof:90,mag:3, maxMag:3, relSpd:180,bSpd:14,spread:.02,auto:false,cost:350,desc:'폭발 범위 공격',       col:'#ff2244',pellets:1,pierce:false,rocket:true},
];

const ZDEFS=[
  {name:'일반',   emoji:'🧟',hp:65, spd:1.1, dmg:8, sz:22,col:'#2d5a1a',score:10, coin:5,  special:null},
  {name:'달리기', emoji:'🏃',hp:42, spd:2.7, dmg:6, sz:18,col:'#1a4d2d',score:15, coin:8,  special:'fast'},
  {name:'뚱보',   emoji:'😈',hp:240,spd:0.62,dmg:24,sz:36,col:'#4a1a0a',score:35, coin:22, special:'tank'},
  {name:'폭탄',   emoji:'💣',hp:85, spd:1.95,dmg:50,sz:25,col:'#1a1a4a',score:30, coin:18, special:'explode'},
  {name:'독',     emoji:'☠️',hp:70, spd:1.6, dmg:12,sz:22,col:'#2a4a0a',score:25, coin:15, special:'poison'},
  {name:'보스',   emoji:'👹',hp:1000,spd:0.95,dmg:42,sz:54,col:'#6a0000',score:280,coin:150,special:'boss'},
];

const SHOP_UPGRADES=[
  {id:'heal',   name:'응급 치료',   emoji:'💊',desc:'HP 70 즉시 회복',              cost:60, col:'#00ff88'},
  {id:'ammo',   name:'탄약 보급',   emoji:'🎁',desc:'전 무기 탄약 풀 충전',          cost:50, col:'#00d4ff'},
  {id:'maxhp',  name:'HP 증가',     emoji:'❤️',desc:'최대 HP +50',                 cost:100,col:'#ff2244'},
  {id:'dmg',    name:'화력 강화',   emoji:'⚡',desc:'전 무기 데미지 +30%',           cost:130,col:'#f5c518'},
  {id:'spd',    name:'이동속도 UP', emoji:'💨',desc:'이동속도 +35%',               cost:90, col:'#c04fff'},
  {id:'reload', name:'장전 감소',   emoji:'⏱️',desc:'전 무기 장전속도 -30%',        cost:95, col:'#ff7700'},
  {id:'nitro',  name:'관통탄',      emoji:'🔱',desc:'권총·소총 탄환 관통 활성화',    cost:180,col:'#88ffff'},
  {id:'mag',    name:'탄창 확장',   emoji:'📦',desc:'전 무기 탄창 +40%',            cost:120,col:'#aaffaa'},
];

const DROP_DEFS=[
  {emoji:'❤️',type:'heal',  col:'#ff4466',prob:.12},
  {emoji:'⚡',type:'ammo',  col:'#f5c518',prob:.18},
  {emoji:'🛡️',type:'shield',col:'#c04fff',prob:.06},
  {emoji:'💰',type:'coins', col:'#f5c518',prob:.22},
];

// ================================================================
//  STATE
// ================================================================
let G={running:false};
let PARTS=[],BLOODPOOL=[],HNS=[],DROPS=[];

// ================================================================
//  특수 탄약 스킬 (Q=화염탄, E=섬광탄, T=공중폭격)
// ================================================================
const SKILL_CD = { fire:0, flash:0, airstrike:0 };
const SKILL_MAX_CD = { fire:12*60, flash:15*60, airstrike:20*60 };

function useSkill(type){
  if(!G||!G.running)return;
  if(SKILL_CD[type]>0){ spawnHN(G.player.x,G.player.y-40,'쿨타임!','#888'); return; }
  SKILL_CD[type]=SKILL_MAX_CD[type];
  const p=G.player;
  if(type==='fire'){
    // 화염탄: 마우스 방향 화염 범위 공격
    const ang=Math.atan2(G.mouse.y-p.y,G.mouse.x-p.x);
    for(let i=-2;i<=2;i++){
      const a=ang+i*0.2;
      G.bullets.push({x:p.x,y:p.y,vx:Math.cos(a)*9,vy:Math.sin(a)*9,dmg:60,col:'#ff7700',r:8,pierce:true,hitIds:[],life:55,special:'fire'});
    }
    spawnP(p.x,p.y,{n:20,col:['#ff4400','#ff8800','#ffaa00'],glow:true,vMax:7,szMax:9});
    spawnHN(p.x,p.y-40,'🔥 화염탄!','#ff7700');
  } else if(type==='flash'){
    // 섬광탄: 전방 적 2초 스턴
    G.zombies.forEach(z=>{if(!z.alive)return;const dx=G.mouse.x-z.x,dy=G.mouse.y-z.y;if(dx*dx+dy*dy<90000){z.frozen=2;}});
    spawnP(G.mouse.x,G.mouse.y,{n:30,col:['#fff','#ffff88','#aaffff'],glow:true,vMax:8,szMax:10});
    spawnHN(G.mouse.x,G.mouse.y-40,'💥 섬광탄!','#ffff44');
  } else if(type==='airstrike'){
    // 공중폭격: 마우스 위치 폭발
    setTimeout(()=>{
      spawnExplosion(G.mouse.x,G.mouse.y);
      G.zombies.forEach(z=>{if(!z.alive)return;const dx=z.x-G.mouse.x,dy=z.y-G.mouse.y;if(dx*dx+dy*dy<14000)hitZombie(z,120);});
      spawnP(G.mouse.x,G.mouse.y,{n:50,col:['#ff4400','#ff8800','#ffdd00','#fff'],glow:true,vMax:12,szMax:14});
      spawnHN(G.mouse.x,G.mouse.y-50,'💣 공중폭격!','#ff4400');
    },600);
    spawnHN(G.mouse.x,G.mouse.y-30,'⚠️ 폭격 예정','#ff8800');
  }
  updateSkillBar();
}

function updateSkillBar(){
  ['fire','flash','airstrike'].forEach((sk,i)=>{
    const el=document.getElementById('sk-cd-'+sk);if(!el)return;
    if(SKILL_CD[sk]>0) el.textContent=Math.ceil(SKILL_CD[sk]/60)+'s';
    else el.textContent='';
  });
}

// ── 보급 상자 시스템 ─────────────────────────────────────
let SUPPLY_BOXES=[];
function spawnSupplyBox(){
  if(!G||!G.running)return;
  const W=canvas.width,H=canvas.height;
  const x=60+Math.random()*(W-120),y=60+Math.random()*(H-120);
  SUPPLY_BOXES.push({x,y,life:600,rot:0,alive:true});
  spawnHN(x,y-30,'📦 보급 상자 도착!','#00ffcc');
}

function updateSupplyBoxes(){
  if(!G)return;
  // 매 30초마다 스폰
  if(G.frame%1800===900) spawnSupplyBox();
  // 쿨타임 카운트다운
  for(const sk in SKILL_CD) if(SKILL_CD[sk]>0) SKILL_CD[sk]--;
  updateSkillBar();
  const p=G.player;
  for(let i=SUPPLY_BOXES.length-1;i>=0;i--){
    const b=SUPPLY_BOXES[i];
    b.rot+=0.02;b.life--;
    if(b.life<=0){SUPPLY_BOXES.splice(i,1);continue;}
    const dx=p.x-b.x,dy=p.y-b.y;
    if(dx*dx+dy*dy<900){
      // 먹기
      const roll=Math.random();
      if(roll<0.4){G.hp=Math.min(G.maxHp,G.hp+35);spawnHN(b.x,b.y-30,'+35 HP 💊','#00ff88');}
      else if(roll<0.75){const w=G.weapons[G.wIdx];if(w)w.ammo=w.maxMag;spawnHN(b.x,b.y-30,'🔫 탄약 보충!','#ffaa00');}
      else{G.score+=500;spawnHN(b.x,b.y-30,'+500점 🎁','#ff00ff');}
      spawnP(b.x,b.y,{n:18,col:['#00ffcc','#ffcc00','#ff88ff'],glow:true,vMax:7,szMax:8});
      SUPPLY_BOXES.splice(i,1);
    }
  }
}

function drawSupplyBoxes(){
  for(const b of SUPPLY_BOXES){
    const alpha=Math.min(1,b.life/60);
    ctx.save();ctx.globalAlpha=alpha;
    ctx.translate(b.x,b.y);ctx.rotate(b.rot);
    // 상자 본체
    ctx.fillStyle='#3a2a0a';ctx.fillRect(-14,-12,28,24);
    ctx.strokeStyle='#c8a800';ctx.lineWidth=2;ctx.strokeRect(-14,-12,28,24);
    // 십자 리본
    ctx.strokeStyle='#ffcc00';ctx.lineWidth=3;
    ctx.beginPath();ctx.moveTo(0,-12);ctx.lineTo(0,12);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-14,0);ctx.lineTo(14,0);ctx.stroke();
    // 아이콘
    ctx.font='14px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText('📦',0,0);
    ctx.restore();
    // 펄스 링
    ctx.save();ctx.globalAlpha=alpha*0.4;
    ctx.strokeStyle='#00ffcc';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(b.x,b.y,18+Math.sin(b.life*0.08)*4,0,Math.PI*2);ctx.stroke();
    ctx.restore();
  }
}

function initGame(){
  G={
    running:true,shopOpen:false,
    wave:0,score:0,totalKills:0,coins:180,
    hp:100,maxHp:100,
    streak:0,streakTimer:0,
    player:{x:canvas.width/2,y:canvas.height/2,angle:0,spd:2.8,spdMul:1},
    weapons:[{...WDEFS[0],ammo:WDEFS[0].maxMag}],
    wIdx:0,reloading:false,relT:0,fireT:0,
    bullets:[],zombies:[],
    waveActive:false,toSpawn:0,spawnT:0,waveKills:0,wNeeded:0,
    boss:null,
    keys:{w:false,a:false,s:false,d:false},
    mouse:{x:canvas.width/2,y:canvas.height/2,down:false},
    joy:{active:false,dx:0,dy:0},
    touchFire:false,frame:0,
    shieldT:0,poisonT:0,
    upgrades:{pierce:false},
    barricades:[],  // 바리케이드 목록
    barricadePlacing:false, // 배치 모드 여부
  };
  PARTS=[];BLOODPOOL=[];HNS=[];DROPS=[];SUPPLY_BOXES=[];
  drawBg();rebuildWeaponBar();buildAmmoDisplay();
  nextWave();
}

// ================================================================
//  BACKGROUND - detailed tile-based arena
// ================================================================
function drawBg(){
  const W=canvas.width,H=canvas.height;
  bgCtx.fillStyle='#050809';bgCtx.fillRect(0,0,W,H);
  // Tile grid with variation
  const ts=72;
  for(let x=0;x<W;x+=ts)for(let y=0;y<H;y+=ts){
    const shade=Math.random()<.15?'rgba(255,255,255,.025)':'rgba(255,255,255,.014)';
    bgCtx.strokeStyle=shade;bgCtx.lineWidth=1;bgCtx.strokeRect(x+.5,y+.5,ts,ts);
    // Cracked tile occasionally
    if(Math.random()<.05){
      bgCtx.save();bgCtx.globalAlpha=.12;bgCtx.strokeStyle='#888';bgCtx.lineWidth=.7;
      bgCtx.beginPath();bgCtx.moveTo(x+ts*.3,y+ts*.4);bgCtx.lineTo(x+ts*.6,y+ts*.55);bgCtx.lineTo(x+ts*.7,y+ts*.8);bgCtx.stroke();
      bgCtx.restore();
    }
  }
  // Existing blood stains
  for(let i=0;i<18;i++){
    const bx=Math.random()*W,by=Math.random()*H,br=14+Math.random()*26;
    const gr=bgCtx.createRadialGradient(bx,by,0,bx,by,br);
    gr.addColorStop(0,'rgba(100,0,0,.4)');gr.addColorStop(1,'transparent');
    bgCtx.fillStyle=gr;bgCtx.beginPath();bgCtx.ellipse(bx,by,br,br*.55+Math.random()*br*.3,Math.random()*Math.PI,0,Math.PI*2);bgCtx.fill();
  }
  // Scattered debris props
  const props=['💊','🔩','📦','🧱','🔫','🪣','🩸','💀'];
  props.forEach(e=>{
    for(let d=0;d<3;d++){
      bgCtx.save();bgCtx.globalAlpha=.14;bgCtx.font='14px serif';bgCtx.textAlign='center';
      bgCtx.fillText(e,Math.random()*W,Math.random()*H);bgCtx.restore();
    }
  });
  // Arena walls (darker edges)
  const edgeG=bgCtx.createRadialGradient(W/2,H/2,Math.min(W,H)*.3,W/2,H/2,Math.min(W,H)*.75);
  edgeG.addColorStop(0,'transparent');edgeG.addColorStop(1,'rgba(0,0,0,.55)');
  bgCtx.fillStyle=edgeG;bgCtx.fillRect(0,0,W,H);
}

// ================================================================
//  WAVE SYSTEM
// ================================================================
function nextWave(){
  G.wave++;
  G.waveKills=0;
  const isBossWave=G.wave%5===0;
  G.wNeeded=isBossWave?1:(8+G.wave*5+(G.wave>5?G.wave*2:0));
  G.toSpawn=G.wNeeded;
  G.spawnT=90;
  G.waveActive=true;
  G.boss=null;
  // Announce
  const wa=document.getElementById('wave-ann');
  document.getElementById('wa-big').textContent=isBossWave?`👹 BOSS WAVE ${G.wave}`:`⚡ WAVE ${G.wave}`;
  document.getElementById('wa-big').style.color=isBossWave?'var(--red)':'var(--gold)';
  document.getElementById('wa-sub').textContent=isBossWave?'강력한 보스가 등장합니다!':`${G.wNeeded}마리를 처치하라!`;
  wa.style.opacity='1';setTimeout(()=>wa.style.opacity='0',2400);
  document.getElementById('boss-bar').style.display=isBossWave?'block':'none';
  updHUD();
}

function spawnZombie(){
  const W=canvas.width,H=canvas.height;
  const side=Math.random()*4|0;
  let x,y;
  if(side===0){x=Math.random()*W;y=-45;}
  else if(side===1){x=W+45;y=Math.random()*H;}
  else if(side===2){x=Math.random()*W;y=H+45;}
  else{x=-45;y=Math.random()*H;}
  const isBossWave=G.wave%5===0;
  let ti=0;
  if(isBossWave){ti=5;}
  else{
    const r=Math.random();
    if(G.wave>=3&&r<.12)ti=1;
    if(G.wave>=2&&r<.09)ti=2;
    if(G.wave>=5&&r<.08)ti=3;
    if(G.wave>=4&&r<.07)ti=4;
  }
  const t=ZDEFS[ti];
  const hpScale=1+G.wave*.13;
  const z={
    x,y,hp:t.hp*hpScale,maxHp:t.hp*hpScale,
    spd:t.spd*(1+G.wave*.04),dmg:t.dmg,sz:t.sz,
    emoji:t.emoji,col:t.col,score:t.score,coin:t.coin,
    name:t.name,special:t.special,
    alive:true,attackCD:0,flash:0,wobble:Math.random()*Math.PI*2,
    poisoned:0,frozen:0,
    isBoss:t.special==='boss',
    id:Math.random(),
  };
  if(z.isBoss)G.boss=z;
  G.zombies.push(z);
}

// ================================================================
//  PARTICLES + BLOOD
// ================================================================
function spawnP(x,y,o={}){
  const n=o.n||8;
  for(let i=0;i<n;i++){
    const a=Math.random()*Math.PI*2,v=(o.vMin||1.5)+Math.random()*(o.vMax||5);
    const cols=Array.isArray(o.col)?o.col:[o.col||'#ff2244'];
    PARTS.push({x,y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:1,
      dec:(o.dMin||.025)+Math.random()*(o.dMax||.04),
      col:cols[Math.floor(Math.random()*cols.length)],
      sz:(o.szMin||2)+Math.random()*(o.szMax||5),glow:o.glow||false,sq:o.sq||false});
  }
}
function spawnHN(x,y,txt,col){HNS.push({x,y:y-15,txt,col,life:1,vy:-.7});}
function spawnBlood(x,y,sz=1){
  spawnP(x,y,{n:14+sz*4|0,col:['#8b0000','#cc0000','#ee1122','#550000'],vMax:5+sz*2,szMin:3,szMax:7+sz*2,dMin:.02,dMax:.04});
  // Permanent stain
  bgCtx.save();bgCtx.globalAlpha=.42;
  bgCtx.fillStyle='rgba(80,0,0,.4)';
  bgCtx.beginPath();bgCtx.ellipse(x,y,6+sz*5+Math.random()*8,4+sz*4+Math.random()*6,Math.random()*Math.PI,0,Math.PI*2);
  bgCtx.fill();bgCtx.restore();
}
function spawnExplosion(x,y,r=90){
  spawnP(x,y,{n:28,col:['#ff7700','#ff4400','#ffaa00','#ff2200','#ffffff'],glow:true,vMax:8,szMin:3,szMax:12,dMin:.015,dMax:.03});
  // Scorch mark
  bgCtx.save();const gr=bgCtx.createRadialGradient(x,y,0,x,y,r*.7);
  gr.addColorStop(0,'rgba(50,20,0,.6)');gr.addColorStop(1,'transparent');
  bgCtx.fillStyle=gr;bgCtx.beginPath();bgCtx.arc(x,y,r*.7,0,Math.PI*2);bgCtx.fill();bgCtx.restore();
}
function spawnDrop(x,y){
  const r=Math.random();let cumP=0;
  for(const d of DROP_DEFS){cumP+=d.prob;if(r<cumP){DROPS.push({x,y,type:d.type,emoji:d.emoji,col:d.col,life:1,rot:0,bob:Math.random()*Math.PI*2});break;}}
}

// ================================================================
//  SHOOT
// ================================================================
function shoot(){
  const w=G.weapons[G.wIdx];
  if(!w||G.reloading||w.ammo<=0||G.fireT>0)return;
  w.ammo--;G.fireT=w.rof;
  buildAmmoDisplay();
  const p=G.player,pellets=w.pellets||1;
  for(let pe=0;pe<pellets;pe++){
    const spr=(Math.random()-.5)*w.spread*2;
    const ang=p.angle+spr;
    G.bullets.push({
      x:p.x+Math.cos(p.angle)*26,y:p.y+Math.sin(p.angle)*26,
      vx:Math.cos(ang)*w.bSpd,vy:Math.sin(ang)*w.bSpd,
      dmg:w.dmg,r:w.id===3?5:w.id===1?4:3,
      life:w.id===3?100:65,col:w.col,
      pierce:w.pierce||(G.upgrades.pierce&&(w.id===0||w.id===2)),
      rocket:w.rocket||false,hitIds:[],wId:w.id,
    });
  }
  // Muzzle flash
  spawnP(p.x+Math.cos(p.angle)*30,p.y+Math.sin(p.angle)*30,
    {n:6,col:w.col,vMin:2,vMax:5,dMin:.08,dMax:.13,glow:true,szMin:2,szMax:5});
  if(w.ammo<=0)startReload();
}

function startReload(){
  if(G.reloading)return;
  const w=G.weapons[G.wIdx];if(!w||w.ammo>=w.maxMag)return;
  G.reloading=true;G.relT=w.relSpd;
  document.getElementById('rl-ring').style.display='block';
}
function switchWeapon(i){
  if(i>=G.weapons.length)return;
  if(G.reloading){G.reloading=false;G.relT=0;document.getElementById('rl-ring').style.display='none';}
  G.wIdx=i;G.fireT=0;rebuildWeaponBar();buildAmmoDisplay();
}

// ================================================================
//  UPDATE
// ================================================================
function update(){
  if(!G.running||G.shopOpen||G.barricadePlacing)return;
  G.frame++;
  const p=G.player;
  // ── 보급 상자 & 스킬 쿨타임 ──
  updateSupplyBoxes();
  updateBarricades();

  // Timers
  if(G.fireT>0)G.fireT--;
  if(G.shieldT>0)G.shieldT-=1/60;
  if(G.poisonT>0){G.poisonT-=1/60;if(G.frame%90===0){G.hp-=5;if(G.hp<=0)G.hp=1;}}
  document.getElementById('shield-ov').style.opacity=G.shieldT>0?'1':'0';

  // Reload
  if(G.reloading){
    G.relT--;
    drawReloadRing();
    if(G.relT<=0){const w=G.weapons[G.wIdx];w.ammo=w.maxMag;G.reloading=false;document.getElementById('rl-ring').style.display='none';buildAmmoDisplay();}
  }

  // Player movement
  let mx=0,my=0;
  if(G.keys.w)my-=1;if(G.keys.s)my+=1;if(G.keys.a)mx-=1;if(G.keys.d)mx+=1;
  if(G.joy.active){mx=G.joy.dx;my=G.joy.dy;}
  const mlen=Math.sqrt(mx*mx+my*my);if(mlen>0){mx/=mlen;my/=mlen;}
  const ms=p.spd*p.spdMul;
  p.x=Math.max(20,Math.min(canvas.width-20, p.x+mx*ms));
  p.y=Math.max(20,Math.min(canvas.height-20,p.y+my*ms));
  p.angle=Math.atan2(G.mouse.y-p.y,G.mouse.x-p.x);

  // Auto fire
  const w=G.weapons[G.wIdx];
  if((G.mouse.down||G.touchFire)&&w&&w.auto)shoot();

  // Streak decay
  if(G.streakTimer>0)G.streakTimer--;
  else if(G.streak>0){G.streak=0;document.getElementById('streak-num').style.opacity='0';}

  // Wave spawn
  if(G.waveActive&&G.toSpawn>0){
    G.spawnT--;const intvl=Math.max(20,95-G.wave*7);
    if(G.spawnT<=0){spawnZombie();G.toSpawn--;G.spawnT=intvl;}
  }

  // Bullets
  for(let bi=G.bullets.length-1;bi>=0;bi--){
    const b=G.bullets[bi];b.x+=b.vx;b.y+=b.vy;b.life--;
    if(G.frame%2===0)spawnP(b.x,b.y,{n:1,col:b.col,vMin:0,vMax:.8,szMin:.8,szMax:b.r*.6,dMin:.1,dMax:.15,glow:true});
    // Rocket trail
    if(b.rocket&&G.frame%3===0)spawnP(b.x,b.y,{n:3,col:['#ff7700','#ffaa00'],vMin:.5,vMax:2,szMin:3,szMax:7,dMin:.03,dMax:.06});

    for(const z of G.zombies){
      if(!z.alive||b.life<=0)continue;
      if(b.pierce&&b.hitIds.includes(z.id))continue;
      const dx=b.x-z.x,dy=b.y-z.y;
      if(dx*dx+dy*dy<z.sz*z.sz){
        if(b.rocket){
          // Rocket explosion
          spawnExplosion(b.x,b.y);
          G.zombies.forEach(z2=>{if(!z2.alive)return;const ex=z2.x-b.x,ey=z2.y-b.y;if(ex*ex+ey*ey<9000){hitZombie(z2,b.dmg*(1-(Math.sqrt(ex*ex+ey*ey)/95)*.5));}});
          b.life=0;break;
        }
        hitZombie(z,b.dmg);
        spawnP(b.x,b.y,{n:5,col:'#ff4400',vMax:4,szMax:4});
        if(b.pierce)b.hitIds.push(z.id);else b.life=0;
      }
    }
    if(b.life<=0||b.x<-50||b.x>canvas.width+50||b.y<-50||b.y>canvas.height+50)G.bullets.splice(bi,1);
  }

  // Zombies
  for(const z of G.zombies){
    if(!z.alive)continue;
    z.wobble+=.05;
    if(z.frozen>0){z.frozen-=1/60;}
    else{
      const dx=p.x-z.x,dy=p.y-z.y,d=Math.sqrt(dx*dx+dy*dy);
      const ang=Math.atan2(dy,dx);
      const eff=z.poisoned>0?.7:1;
      if(d>z.sz+16){z.x+=Math.cos(ang)*z.spd*eff;z.y+=Math.sin(ang)*z.spd*eff;}
      else{
        if(z.attackCD<=0){
          if(G.shieldT>0){spawnP(p.x,p.y,{n:8,col:'#c04fff',glow:true,vMax:5});spawnHN(p.x,p.y-30,'BLOCKED!','#c04fff');}
          else{G.hp-=z.dmg;z.attackCD=60;document.getElementById('vignette').style.opacity='.8';setTimeout(()=>document.getElementById('vignette').style.opacity='0',300);if(G.hp<=0){G.hp=0;setTimeout(showGO,500);}}
        }
      }
    }
    if(z.attackCD>0)z.attackCD--;
    if(z.flash>0)z.flash--;
    if(z.poisoned>0){z.poisoned-=1/60;if(G.frame%60===0){z.hp-=15;if(z.hp<=0)killZombie(z);}}
    // Boss HP bar
    if(z.isBoss&&z.alive){document.getElementById('boss-fill').style.width=(z.hp/z.maxHp*100)+'%';}
  }

  // Drops
  for(let di=DROPS.length-1;di>=0;di--){
    const d=DROPS[di];d.rot+=.06;d.bob+=.08;d.life-=.003;
    const dx=p.x-d.x,dy=p.y-d.y;
    if(dx*dx+dy*dy<1100){
      spawnP(d.x,d.y,{n:8,col:d.col,glow:true,vMax:5,szMax:6});
      spawnHN(d.x,d.y-20,d.type==='coins'?'+30💰':d.type==='heal'?'+30 HP':d.type==='ammo'?'AMMO!':'🛡️ SHIELD',d.col);
      if(d.type==='heal'){G.hp=Math.min(G.maxHp,G.hp+30);}
      if(d.type==='ammo'){G.weapons.forEach(ww=>ww.ammo=ww.maxMag);buildAmmoDisplay();}
      if(d.type==='shield')G.shieldT=4;
      if(d.type==='coins')G.coins+=30;
      DROPS.splice(di,1);continue;
    }
    if(d.life<=0)DROPS.splice(di,1);
  }

  // Particles
  for(let i=PARTS.length-1;i>=0;i--){const pp=PARTS[i];pp.x+=pp.vx;pp.y+=pp.vy;pp.vx*=.88;pp.vy*=.88;pp.life-=pp.dec;pp.life<=0&&PARTS.splice(i,1);}
  for(let i=HNS.length-1;i>=0;i--){const h=HNS[i];h.y+=h.vy;h.life-=.022;h.life<=0&&HNS.splice(i,1);}

  // Wave clear
  if(G.waveActive&&G.toSpawn===0&&G.zombies.filter(z=>z.alive).length===0){
    G.waveActive=false;setTimeout(openShop,950);
  }
  updHUD();
}

function hitZombie(z,dmg){
  z.hp-=dmg;z.flash=7;
  spawnHN(z.x,z.y-z.sz-5,Math.round(dmg)+'!',z.isBoss?'#ff2244':'#ffaa44');
  if(z.hp<=0)killZombie(z);
}

function killZombie(z){
  if(!z.alive)return;
  z.alive=false;
  spawnBlood(z.x,z.y,z.sz*.06);
  G.totalKills++;G.waveKills++;G.coins+=z.coin;G.score+=z.score;
  // Streak
  G.streak++;G.streakTimer=200;
  if(G.streak>=3){
    const sn=document.getElementById('streak-num');
    sn.textContent=`🔥×${G.streak}`;sn.style.opacity='1';
    G.score+=G.streak*5;
  }
  // Special death effects
  if(z.special==='explode'){
    spawnExplosion(z.x,z.y);
    G.zombies.forEach(z2=>{if(!z2.alive)return;const ex=z2.x-z.x,ey=z2.y-z.y;if(ex*ex+ey*ey<8100){hitZombie(z2,65);}});
    const ep=G.player,dx=ep.x-z.x,dy=ep.y-z.y;if(dx*dx+dy*dy<8100&&G.shieldT<=0){G.hp-=45;}
  }
  if(z.special==='poison'){spawnP(z.x,z.y,{n:12,col:['#44bb00','#88ff44','#226600'],glow:true,vMax:5});}
  if(z.isBoss){
    document.getElementById('boss-bar').style.display='none';
    spawnExplosion(z.x,z.y,160);spawnExplosion(z.x+60,z.y-40,80);spawnExplosion(z.x-60,z.y+40,80);
    G.coins+=100;
  }
  // Drop
  if(Math.random()<(z.isBoss?.9:.35))spawnDrop(z.x,z.y);
  addKillfeed(z);
}

function addKillfeed(z){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kfe';
  d.innerHTML=`${z.emoji} ${z.name} 처치 <b style="color:var(--gold)">+${z.score}pt</b>`;
  if(z.isBoss){d.style.borderLeftColor='var(--gold)';d.style.fontSize='10px';}
  kf.appendChild(d);setTimeout(()=>d.remove(),2800);
  while(kf.children.length>5)kf.removeChild(kf.firstChild);
}

// ================================================================
//  RELOAD RING DRAW
// ================================================================
function drawReloadRing(){
  const w=G.weapons[G.wIdx];if(!w)return;
  const rlc=document.getElementById('rl-cv');const rc=rlc.getContext('2d');
  const pct=1-(G.relT/w.relSpd);
  rc.clearRect(0,0,52,52);
  rc.strokeStyle='rgba(245,197,24,.12)';rc.lineWidth=4;rc.beginPath();rc.arc(26,26,22,0,Math.PI*2);rc.stroke();
  rc.strokeStyle='rgba(245,197,24,.85)';rc.shadowColor='rgba(245,197,24,.5)';rc.shadowBlur=8;rc.lineWidth=4;
  rc.beginPath();rc.arc(26,26,22,-Math.PI*.5,-Math.PI*.5+Math.PI*2*pct);rc.stroke();
}

// ================================================================
//  SHOP
// ================================================================
function openShop(){
  G.shopOpen=true;
  document.getElementById('shop-wave-txt').textContent=`WAVE ${G.wave} 클리어! 다음 웨이브를 준비하세요`;
  document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
  // Weapon slots
  const wg=document.getElementById('shop-weapons');wg.innerHTML='';
  WDEFS.forEach(wd=>{
    const owned=!!G.weapons.find(w=>w.id===wd.id);
    const d=document.createElement('div');d.className='si'+(owned?' bought':'');
    d.innerHTML=`<div class="si-ico">${wd.emoji}</div><div class="si-name" style="color:${wd.col}">${wd.name}</div><div class="si-desc">${wd.desc}</div><div class="${owned?'si-owned':'si-cost'}">${owned?'✅ 보유중':'💰 '+wd.cost}</div>`;
    if(!owned&&wd.cost>0){d.onclick=()=>buyWeapon(wd,d);}
    wg.appendChild(d);
  });
  // Upgrades
  const ug=document.getElementById('shop-upgrades');ug.innerHTML='';
  SHOP_UPGRADES.forEach(item=>{
    const d=document.createElement('div');d.className='si';
    d.innerHTML=`<div class="si-ico">${item.emoji}</div><div class="si-name" style="color:${item.col}">${item.name}</div><div class="si-desc">${item.desc}</div><div class="si-cost">💰 ${item.cost}</div>`;
    d.onclick=()=>buyUpgrade(item,d);
    ug.appendChild(d);
  });

  // ── 바리케이드 구매 섹션 ──
  const barSection = document.createElement('div');
  barSection.innerHTML = `
    <div class="shop-section" style="margin-top:10px;">🧱 바리케이드 설치</div>
    <div style="font-size:9px;color:#446;margin-bottom:8px;line-height:1.7;">
      웨이브 사이 인터미션에 바리케이드를 배치해 좀비의 접근 경로를 막을 수 있습니다.<br>
      최대 5개 설치 가능 (현재: ${G.barricades.length}/5)
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
      <div class="si" id="buy-barricade-light">
        <div class="si-ico">🪵</div>
        <div class="si-name" style="color:#c8860a">나무 바리케이드</div>
        <div class="si-desc">HP 80 · 좀비 3마리 차단</div>
        <div class="si-cost">💰 40</div>
      </div>
      <div class="si" id="buy-barricade-heavy">
        <div class="si-ico">🧱</div>
        <div class="si-name" style="color:#88aacc">강화 바리케이드</div>
        <div class="si-desc">HP 200 · 좀비 8마리 차단</div>
        <div class="si-cost">💰 90</div>
      </div>
    </div>`;
  document.getElementById('shop').querySelector('.shop-box').insertBefore(barSection, document.getElementById('shop-cont'));

  document.getElementById('buy-barricade-light').onclick=()=>buyBarricade('light',40,80);
  document.getElementById('buy-barricade-heavy').onclick=()=>buyBarricade('heavy',90,200);

  document.getElementById('shop').style.display='flex';
}

function buyBarricade(type, cost, hp){
  if(G.barricades.length>=5){alert('바리케이드는 최대 5개까지 설치 가능합니다.');return;}
  if(G.coins<cost){
    const btn=document.getElementById(`buy-barricade-${type}`);
    if(btn){btn.style.borderColor='var(--red)';setTimeout(()=>btn.style.borderColor='',600);}
    return;
  }
  G.coins-=cost;
  document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
  // 닫고 배치 모드 진입
  document.getElementById('shop').style.display='none';
  G.shopOpen=false;
  G.barricadePlacing={type, hp, maxHp:hp};
  // 안내 HUD 표시
  const hint=document.getElementById('barricade-hint');
  if(hint){hint.style.display='block';hint.textContent='🧱 클릭해서 바리케이드를 배치하세요 (ESC: 취소)';}
}
function buyWeapon(wd,el){
  if(G.coins<wd.cost){el.style.borderColor='var(--red)';setTimeout(()=>el.style.borderColor='',600);return;}
  G.coins-=wd.cost;G.weapons.push({...wd,ammo:wd.maxMag});rebuildWeaponBar();
  el.classList.add('bought');el.querySelector('.si-cost').className='si-owned';el.querySelector('.si-owned').textContent='✅ 구매 완료';
  el.onclick=null;document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
}
function buyUpgrade(item,el){
  if(G.coins<item.cost){el.style.borderColor='var(--red)';setTimeout(()=>el.style.borderColor='',600);return;}
  G.coins-=item.cost;el.classList.add('bought');el.onclick=null;
  document.getElementById('shop-coins-txt').textContent=`💰 보유 코인: ${G.coins}`;
  if(item.id==='heal'){G.hp=Math.min(G.maxHp,G.hp+70);}
  if(item.id==='ammo'){G.weapons.forEach(w=>w.ammo=w.maxMag);buildAmmoDisplay();}
  if(item.id==='maxhp'){G.maxHp+=50;G.hp=Math.min(G.maxHp,G.hp+50);}
  if(item.id==='dmg'){G.weapons.forEach(w=>w.dmg=Math.round(w.dmg*1.3));}
  if(item.id==='spd'){G.player.spdMul=Math.min(2.2,(G.player.spdMul||1)*1.35);}
  if(item.id==='reload'){G.weapons.forEach(w=>w.relSpd=Math.max(35,Math.round(w.relSpd*.7)));}
  if(item.id==='nitro'){G.upgrades.pierce=true;}
  if(item.id==='mag'){G.weapons.forEach(w=>{w.maxMag=Math.round(w.maxMag*1.4);w.ammo=Math.min(w.ammo,w.maxMag);});buildAmmoDisplay();}
  updHUD();
}
document.getElementById('shop-cont').onclick=()=>{
  document.getElementById('shop').style.display='none';G.shopOpen=false;nextWave();
};

// ================================================================
//  BARRICADES
// ================================================================
function drawBarricades(){
  for(const b of G.barricades){
    const pct=b.hp/b.maxHp;
    const col=b.type==='heavy'?'#5588cc':'#c8860a';
    const crackedAlpha=1-pct;
    ctx.save();
    ctx.fillStyle=col;
    ctx.globalAlpha=0.82;
    ctx.shadowColor=col;ctx.shadowBlur=8;
    ctx.fillRect(b.x-b.w/2,b.y-b.h/2,b.w,b.h);
    // HP bar
    ctx.shadowBlur=0;ctx.globalAlpha=1;
    ctx.fillStyle='rgba(0,0,0,.5)';
    ctx.fillRect(b.x-b.w/2,b.y-b.h/2-7,b.w,4);
    ctx.fillStyle=pct>0.5?'#2fc':pct>0.25?'#ffaa00':'#ff2244';
    ctx.fillRect(b.x-b.w/2,b.y-b.h/2-7,b.w*pct,4);
    // Crack overlay at low HP
    if(crackedAlpha>0.4){
      ctx.globalAlpha=crackedAlpha*0.6;
      ctx.strokeStyle='rgba(0,0,0,.7)';ctx.lineWidth=1.5;
      ctx.beginPath();ctx.moveTo(b.x-b.w*.3,b.y-b.h*.4);ctx.lineTo(b.x+b.w*.1,b.y+b.h*.4);ctx.stroke();
      ctx.beginPath();ctx.moveTo(b.x+b.w*.25,b.y-b.h*.5);ctx.lineTo(b.x-b.w*.1,b.y+b.h*.5);ctx.stroke();
    }
    // Emoji icon
    ctx.globalAlpha=0.9;
    ctx.font=`${b.type==='heavy'?14:12}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(b.type==='heavy'?'🧱':'🪵',b.x,b.y);
    ctx.restore();
  }

  // 배치 미리보기
  if(G.barricadePlacing){
    const bp=G.barricadePlacing;
    const col=bp.type==='heavy'?'#5588cc':'#c8860a';
    const w=bp.type==='heavy'?64:48, h=bp.type==='heavy'?24:18;
    ctx.save();
    ctx.globalAlpha=0.5;ctx.strokeStyle=col;ctx.lineWidth=2;ctx.setLineDash([4,4]);
    ctx.strokeRect(G.mouse.x-w/2,G.mouse.y-h/2,w,h);
    ctx.fillStyle=col;ctx.globalAlpha=0.2;
    ctx.fillRect(G.mouse.x-w/2,G.mouse.y-h/2,w,h);
    ctx.restore();
  }
}

function updateBarricades(){
  for(let bi=G.barricades.length-1;bi>=0;bi--){
    const b=G.barricades[bi];
    if(b.hp<=0){G.barricades.splice(bi,1);continue;}
    // 좀비 충돌: 바리케이드에 접촉한 좀비는 이동 차단 + HP 소모
    for(const z of G.zombies){
      if(!z.alive)continue;
      const dx=z.x-b.x, dy=z.y-b.y;
      if(Math.abs(dx)<b.w/2+z.radius&&Math.abs(dy)<b.h/2+z.radius){
        // 방향 반발
        const norm=Math.hypot(dx,dy)||1;
        z.x+=dx/norm*1.8; z.y+=dy/norm*1.8;
        // 바리케이드 피해 (매 60프레임)
        if(G.frame%60===0){
          b.hp-=z.dmg||8;
          // 파티클
          spawnP(b.x+(Math.random()-.5)*b.w,b.y+(Math.random()-.5)*b.h,4,'#c8860a',2);
        }
      }
    }
  }
}

function drawBarricadePlacingHint(){}
// ================================================================
function rebuildWeaponBar(){
  const bar=document.getElementById('weapbar');bar.innerHTML='';
  // Show all 5 slots (empty if not owned)
  for(let i=0;i<5;i++){
    const w=G.weapons[i];
    const d=document.createElement('div');d.className='wslot'+(i===G.wIdx?' active':'')+(w?'':' empty');
    if(w){
      d.innerHTML=`<div class="ws-key">${i+1}</div><div class="ws-ammo">${w.ammo}</div><div class="ws-ico">${w.emoji}</div><div class="ws-name">${w.name}</div>`;
      d.onclick=()=>switchWeapon(i);
    }else{
      d.innerHTML=`<div class="ws-key">${i+1}</div><div class="ws-ico" style="opacity:.3">🔒</div><div class="ws-name">미해금</div>`;
    }
    bar.appendChild(d);
  }
}
function buildAmmoDisplay(){
  const ac=document.getElementById('ammo-col');ac.innerHTML='';
  const w=G.weapons[G.wIdx];if(!w)return;
  for(let i=0;i<Math.min(w.maxMag,30);i++){const d=document.createElement('div');d.className='adot'+(i<w.ammo?' live':'');ac.appendChild(d);}
  // Update weapon bar ammo numbers
  document.querySelectorAll('.wslot').forEach((s,i)=>{
    const ww=G.weapons[i];if(ww){const am=s.querySelector('.ws-ammo');if(am)am.textContent=ww.ammo;}
  });
}

// ================================================================
//  HUD
// ================================================================
function updHUD(){
  const hp=G.hp,mhp=G.maxHp;
  document.getElementById('hp-bar').style.width=(hp/mhp*100)+'%';
  document.getElementById('hp-bar').style.background=hp<mhp*.3?'linear-gradient(90deg,#550000,#ff0022)':'linear-gradient(90deg,#7b0000,#cc1122,#ff5566)';
  document.getElementById('wave-v').textContent=G.wave;
  document.getElementById('kill-v').textContent=G.totalKills;
  document.getElementById('score-v').textContent=G.score.toLocaleString();
  document.getElementById('coin-v').textContent='💰 '+G.coins;
}

// ================================================================
//  DRAW
// ================================================================
function drawZombies(){
  for(const z of G.zombies){
    if(!z.alive)continue;
    ctx.save();ctx.translate(z.x,z.y);
    if(z.flash>0&&z.flash%2===0)ctx.filter='brightness(4) saturate(0)';
    if(z.poisoned>0)ctx.filter='hue-rotate(80deg) brightness(1.3)';
    if(z.frozen>0)ctx.filter='saturate(0) brightness(.7)';
    // Shadow
    ctx.globalAlpha=.28;ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(0,z.sz*.65,z.sz*.55,z.sz*.18,0,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;
    // Emoji
    ctx.font=`${z.sz*1.52}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(z.emoji,Math.sin(z.wobble)*3,Math.cos(z.wobble*1.3)*2);
    // Boss aura
    if(z.isBoss){ctx.shadowColor='rgba(255,0,50,.6)';ctx.shadowBlur=z.sz*.8;ctx.strokeStyle='rgba(255,0,50,.25)';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,0,z.sz*1.1+Math.sin(G.frame*.08)*4,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;}
    ctx.restore();
    // HP bar
    if(z.hp<z.maxHp){
      const bw=z.sz*2.3,bh=5,bx=z.x-bw/2,by=z.y-z.sz-10;
      ctx.fillStyle='rgba(0,0,0,.55)';ctx.fillRect(bx,by,bw,bh);
      const pct=z.hp/z.maxHp;
      ctx.fillStyle=pct>.5?'#00ff88':pct>.25?'#ffaa00':'#ff2244';ctx.fillRect(bx,by,bw*pct,bh);
    }
    // Frozen ring
    if(z.frozen>0){ctx.save();ctx.strokeStyle='rgba(100,200,255,.5)';ctx.lineWidth=2;ctx.beginPath();ctx.arc(z.x,z.y,z.sz+4,0,Math.PI*2);ctx.stroke();ctx.restore();}
  }
}
function drawPlayer(){
  const p=G.player;
  // Shadow
  ctx.save();ctx.globalAlpha=.3;ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(p.x,p.y+18,18,7,0,0,Math.PI*2);ctx.fill();ctx.restore();
  // Crosshair direction line
  const w=G.weapons[G.wIdx];
  if(w){
    ctx.save();ctx.strokeStyle=w.col;ctx.lineWidth=1.5;ctx.setLineDash([3,5]);ctx.shadowColor=w.col;ctx.shadowBlur=5;ctx.globalAlpha=.5;
    ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(p.x+Math.cos(p.angle)*38,p.y+Math.sin(p.angle)*38);ctx.stroke();
    ctx.restore();
  }
  // Shield aura
  if(G.shieldT>0){
    ctx.save();const sa=Math.sin(G.frame*.14)*.25+.75;ctx.globalAlpha=sa;ctx.strokeStyle='#c04fff';ctx.shadowColor='#c04fff';ctx.shadowBlur=16;ctx.lineWidth=2.5;
    ctx.beginPath();ctx.arc(p.x,p.y,28,0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  // Player body
  ctx.save();ctx.font='46px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🧑',p.x,p.y);ctx.restore();
}
function drawBullets(){
  for(const b of G.bullets){
    ctx.save();ctx.shadowColor=b.col;ctx.shadowBlur=b.rocket?16:10;ctx.fillStyle=b.col;
    ctx.beginPath();ctx.arc(b.x,b.y,b.r,0,Math.PI*2);ctx.fill();
    if(b.rocket){ctx.font='14px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🚀',b.x,b.y);}
    ctx.restore();
  }
}
function drawDrops(){
  for(const d of DROPS){
    ctx.save();ctx.translate(d.x,d.y+Math.sin(d.bob)*4);ctx.rotate(d.rot);
    ctx.shadowColor=d.col;ctx.shadowBlur=12;ctx.globalAlpha=d.life;
    ctx.font='22px serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(d.emoji,0,0);
    ctx.restore();
  }
}
function drawParts(){
  for(const pp of PARTS){
    ctx.save();ctx.globalAlpha=Math.max(0,pp.life);
    if(pp.glow){ctx.shadowColor=pp.col;ctx.shadowBlur=pp.sz*2.5;}
    ctx.fillStyle=pp.col;ctx.beginPath();ctx.arc(pp.x,pp.y,pp.sz*Math.max(.08,pp.life),0,Math.PI*2);ctx.fill();
    if(pp.glow)ctx.shadowBlur=0;ctx.restore();
  }
}
function drawHNs(){
  for(const h of HNS){
    ctx.save();ctx.globalAlpha=Math.max(0,h.life);ctx.shadowColor=h.col;ctx.shadowBlur=8;ctx.fillStyle=h.col;
    ctx.font="bold 13px 'Black Han Sans',sans-serif";ctx.textAlign='center';ctx.fillText(h.txt,h.x,h.y);ctx.restore();
  }
}
function drawCrosshair(){
  const mx=G.mouse.x,my=G.mouse.y;
  const w=G.weapons[G.wIdx];const col=w?w.col:'rgba(255,255,255,.6)';
  ctx.save();ctx.strokeStyle=col;ctx.lineWidth=1.2;ctx.globalAlpha=.7;
  ctx.beginPath();ctx.moveTo(mx-10,my);ctx.lineTo(mx+10,my);ctx.moveTo(mx,my-10);ctx.lineTo(mx,my+10);ctx.stroke();
  ctx.beginPath();ctx.arc(mx,my,4,0,Math.PI*2);ctx.stroke();
  ctx.restore();
}

// ================================================================
//  MAIN LOOP
// ================================================================
function loop(){
  if(!G.running)return;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  drawBullets();drawDrops();drawSupplyBoxes();drawBarricades();drawZombies();drawPlayer();drawParts();drawHNs();drawCrosshair();
  update();requestAnimationFrame(loop);
}

// ================================================================
//  GAME OVER
// ================================================================
function showGO(){
  G.running=false;
  const best=parseInt(localStorage.getItem('zbBest')||'0');
  if(G.wave>best)localStorage.setItem('zbBest',G.wave);
  // ✅ [NEW] 게임 결과 포털 전송
  try{window.parent.postMessage({type:'zombie_result',wave:G.wave,score:G.score,kills:G.totalKills},'*');}catch(e){}
  const ov=document.getElementById('overlay');
  ov.innerHTML=`<div class="ov-box">
    <div class="ov-eye">GAME OVER</div>
    <div class="ov-title" style="color:var(--red)">💀<br>감염됨!</div>
    <div class="ov-sub">YOU HAVE FALLEN</div>
    <div class="stats-row">
      <div class="sc"><div class="sv" style="color:var(--red)">WAVE ${G.wave}</div><div class="sl">도달 웨이브</div></div>
      <div class="sc"><div class="sv" style="color:var(--gold)">${G.score.toLocaleString()}</div><div class="sl">점수</div></div>
      <div class="sc"><div class="sv" style="color:var(--green)">${G.totalKills}</div><div class="sl">처치수</div></div>
      <div class="sc"><div class="sv" style="color:var(--purple)">${G.streak}</div><div class="sl">최고 연속</div></div>
    </div>
    <div style="font-size:9px;color:#446;margin-bottom:14px">최고기록: <span style="color:var(--gold)">${Math.max(G.wave,best)} WAVE</span></div>
    <button class="ov-btn" onclick="location.reload()">다시 생존 💀</button>
  </div>`;
  ov.style.display='flex';
}

// ================================================================
//  TITLE
// ================================================================
function showTitle(){
  const best=parseInt(localStorage.getItem('zbBest')||'0');
  const tags=['🧟 5종 좀비 타입','💥 폭발·독 특수효과','🚀 로켓런처','🎯 스나이퍼 관통','⚡ 킬스트릭 보너스','🛒 웨이브 상점','❤️ 드롭 아이템','👹 보스 5웨이브','🔱 관통탄 업그레이드','💰 코인 경제','🛡️ 무적 실드','⭐ 최고 점수'];
  const tp=[...tags,...tags].map((t,i)=>`<span class="tpill ${['c','g','r','p'][i%4]}">${t}</span>`).join('');
  document.getElementById('ovc').innerHTML=`
    <div class="ov-eye">ZOMBIE APOCALYPSE v3.0</div>
    <div class="ov-title" style="color:var(--red)">🧟<br>좀비 아포칼립스</div>
    <div class="ov-sub">WAVE SURVIVAL · 5 WEAPONS · BOSS RAIDS</div>
    <div class="tag-strip"><div class="tag-inner">${tp}</div></div>
    <div style="font-size:9px;color:#446;line-height:2.2;margin-bottom:14px">
      WASD / 조이스틱 — 이동<br>
      마우스 클릭 / 🔫 — 발사 &nbsp;|&nbsp; R / 🔄 — 재장전<br>
      1~5 키 / 슬롯 탭 — 무기 변경<br>
      웨이브 클리어 후 상점에서 무기·업그레이드 구매!
    </div>
    ${best>0?`<div style="font-size:9px;color:#446;margin-bottom:12px">🏆 최고기록: <span style="color:var(--gold)">${best} WAVE</span></div>`:''}
    <button class="ov-btn" onclick="startGame()">생존 시작 💀</button>`;
  document.getElementById('overlay').style.display='flex';
}

// ================================================================
//  INPUT
// ================================================================
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&G.barricadePlacing){
    G.barricadePlacing=false;
    const hint=document.getElementById('barricade-hint');
    if(hint)hint.style.display='none';
    openShop();
  }
  if(e.key==='w'||e.key==='W'||e.key==='ArrowUp')G.keys.w=true;
  if(e.key==='s'||e.key==='S'||e.key==='ArrowDown')G.keys.s=true;
  if(e.key==='a'||e.key==='A'||e.key==='ArrowLeft')G.keys.a=true;
  if(e.key==='d'||e.key==='D'||e.key==='ArrowRight')G.keys.d=true;
  if(e.key==='r'||e.key==='R')startReload();
  if(e.key==='1')switchWeapon(0);if(e.key==='2')switchWeapon(1);
  if(e.key==='3')switchWeapon(2);if(e.key==='4')switchWeapon(3);if(e.key==='5')switchWeapon(4);
  // ── 특수 탄약 스킬 ──
  if(e.key==='q'||e.key==='Q')useSkill('fire');
  if(e.key==='e'||e.key==='E')useSkill('flash');
  if((e.key==='t'||e.key==='T'))useSkill('airstrike');
});
document.addEventListener('keyup',e=>{
  if(e.key==='w'||e.key==='W'||e.key==='ArrowUp')G.keys.w=false;
  if(e.key==='s'||e.key==='S'||e.key==='ArrowDown')G.keys.s=false;
  if(e.key==='a'||e.key==='A'||e.key==='ArrowLeft')G.keys.a=false;
  if(e.key==='d'||e.key==='D'||e.key==='ArrowRight')G.keys.d=false;
});
canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect();G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;});
canvas.addEventListener('mousedown',()=>{
  if(G.barricadePlacing){
    // 바리케이드 배치
    const bp=G.barricadePlacing;
    G.barricades.push({
      x:G.mouse.x,y:G.mouse.y,
      type:bp.type, hp:bp.hp, maxHp:bp.maxHp,
      w:bp.type==='heavy'?64:48, h:bp.type==='heavy'?24:18,
    });
    G.barricadePlacing=false;
    const hint=document.getElementById('barricade-hint');
    if(hint)hint.style.display='none';
    openShop(); // 상점으로 복귀
    return;
  }
  G.mouse.down=true;if(G.running)shoot();
});
canvas.addEventListener('mouseup',()=>G.mouse.down=false);
canvas.addEventListener('contextmenu',e=>e.preventDefault());
canvas.addEventListener('touchmove',e=>{e.preventDefault();const t=e.touches[e.touches.length-1];const r=canvas.getBoundingClientRect();G.mouse.x=t.clientX-r.left;G.mouse.y=t.clientY-r.top;},{passive:false});

// Joystick
const jz=document.getElementById('joyzone'),kn=document.getElementById('knob');let jO=null;
jz.addEventListener('touchstart',e=>{e.preventDefault();const t=e.touches[0];const r=jz.getBoundingClientRect();jO={x:r.left+r.width/2,y:r.top+r.height/2};G.joy.active=true;},{passive:false});
jz.addEventListener('touchmove',e=>{e.preventDefault();if(!jO)return;const t=e.touches[0];let dx=t.clientX-jO.x,dy=t.clientY-jO.y;const d=Math.sqrt(dx*dx+dy*dy),max=42;if(d>max){dx=dx/d*max;dy=dy/d*max;}G.joy.dx=dx/max;G.joy.dy=dy/max;kn.style.transform=`translate(calc(-50% + ${dx}px),calc(-50% + ${dy}px))`;},{passive:false});
['touchend','touchcancel'].forEach(ev=>jz.addEventListener(ev,e=>{e.preventDefault();G.joy.active=false;G.joy.dx=0;G.joy.dy=0;kn.style.transform='translate(-50%,-50%)';},{passive:false}));

// Fire / Reload buttons
function addT(id,dn,up){
  const el=document.getElementById(id);if(!el)return;
  const d=e=>{e.preventDefault();if(dn)dn();el.classList.add('pr');};
  const u=e=>{e.preventDefault();if(up)up();el.classList.remove('pr');};
  el.addEventListener('touchstart',d,{passive:false});el.addEventListener('touchend',u,{passive:false});el.addEventListener('touchcancel',u,{passive:false});
  el.addEventListener('mousedown',d);el.addEventListener('mouseup',u);
}
addT('fire-btn',()=>{G.touchFire=true;if(G.running)shoot();},()=>G.touchFire=false);
addT('rl-btn',()=>startReload(),null);

window.startGame=()=>{document.getElementById('overlay').style.display='none';initGame();requestAnimationFrame(loop);};
showTitle();
</script>
</body>
</html>"""

def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data

    # ── 결과 처리 ──
    qp = st.query_params
    if qp.get('zombie_wave'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            z_wave  = int(qp.get('zombie_wave', 0))
            z_score = int(qp.get('zombie_score', 0))
            z_kills = int(qp.get('zombie_kills', 0))
            if uid and z_wave > 0:
                cur_rec = st.session_state.get('game_records', {})
                if z_wave > cur_rec.get('zombie', {}).get('wave', 0):
                    cur_rec.setdefault('zombie', {}).update({'wave': z_wave, 'score': z_score, 'kills': z_kills})
                    st.session_state.game_records = cur_rec
                    sync_user_data()
                    st.toast(f"🏆 좀비 최고기록 갱신! Wave {z_wave}", icon="🧟")
        except Exception:
            pass
        st.query_params.clear()

    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    st.caption("🧟 WASD/조이스틱: 이동 | 마우스/터치: 조준·사격 | 1~5: 무기 전환 | Q: 화염탄 E: 섬광 T: 공습")

    listener_html = """
    <script>
    window.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'zombie_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('zombie_wave',  e.data.wave);
        url.searchParams.set('zombie_score', e.data.score);
        url.searchParams.set('zombie_kills', e.data.kills);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=730, scrolling=False)
