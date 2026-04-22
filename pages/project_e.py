#pages/project_e.py

import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>DUNGEON CRUSH</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#06040e;--bg2:#0d0a1a;--panel:#0a0818;
  --gold:#f5c842;--gold2:#ffe680;--red:#ff2233;--blue:#2299ff;
  --green:#22ff88;--purple:#cc44ff;--orange:#ff7722;
  --border:rgba(245,200,66,0.18);
}
html,body{width:100%;height:100%;background:var(--bg);overflow:hidden;font-family:'Noto Sans KR',sans-serif;color:#ddd;}
#wrap{width:100vw;height:100vh;display:flex;flex-direction:column;}
#hud{
  height:48px;background:linear-gradient(180deg,#0d0a18f0,#09061200);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:10px;padding:0 12px;flex-shrink:0;position:relative;z-index:50;
}
.hud-char{font-family:'Black Han Sans',sans-serif;font-size:.8rem;color:var(--gold);letter-spacing:2px;white-space:nowrap;}
.bar-group{display:flex;flex-direction:column;gap:3px;}
.bar-row{display:flex;align-items:center;gap:4px;}
.bar-label{font-size:.48rem;color:#666;width:14px;text-align:right;}
.bar-bg{height:10px;background:rgba(255,255,255,.06);border-radius:2px;border:1px solid rgba(255,255,255,.05);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:2px;transition:width .12s;}
#hp-fill{background:linear-gradient(90deg,#660000,#dd1122,#ff4455);}
#mp-fill{background:linear-gradient(90deg,#001166,#1144cc,#3388ff);}
#xp-fill{background:linear-gradient(90deg,#224400,#44aa00,#88ff44);width:0%;}
.bar-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.42rem;color:rgba(255,255,255,.65);font-weight:700;}
#stat-row{display:flex;gap:5px;margin-left:4px;}
.sbox{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:3px;padding:1px 6px;text-align:center;min-width:36px;}
.sbox-v{font-size:.75rem;font-weight:900;color:var(--gold);}
.sbox-l{font-size:.38rem;color:#555;letter-spacing:.5px;}
.floor-lbl{font-family:'Rajdhani',sans-serif;font-size:.9rem;font-weight:700;color:#fff;background:rgba(245,200,66,.1);border:1px solid var(--border);border-radius:3px;padding:1px 10px;letter-spacing:2px;margin-left:auto;}
#buff-row{display:flex;gap:3px;font-size:.85rem;}
#game-area{flex:1;position:relative;overflow:hidden;}
canvas#gc{display:block;width:100%;height:100%;}
#boss-bar{position:absolute;top:6px;left:50%;transform:translateX(-50%);width:360px;pointer-events:none;z-index:40;opacity:0;transition:opacity .3s;}
#boss-bar.show{opacity:1;}
#boss-name-lbl{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.75rem;color:#ff3344;margin-bottom:2px;text-shadow:0 0 10px rgba(255,0,50,.6);letter-spacing:2px;}
#boss-hp-bg{height:10px;background:rgba(255,255,255,.05);border-radius:2px;border:1px solid rgba(255,50,70,.3);overflow:hidden;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);border-radius:2px;transition:width .12s;}
#boss-phase-txt{text-align:center;font-size:.48rem;color:#ff7788;letter-spacing:3px;margin-top:2px;}
#skill-bar{
  position:absolute;bottom:0;left:0;right:0;height:60px;
  background:linear-gradient(0deg,#0d0a18f8,#0d0a1880);
  border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  gap:6px;padding:0 10px;z-index:50;
}
.sk-slot{width:50px;height:50px;border-radius:5px;position:relative;background:rgba(255,255,255,.04);border:1px solid rgba(245,200,66,.2);display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:default;transition:border-color .1s;}
.sk-slot.ready{border-color:rgba(245,200,66,.7);box-shadow:0 0 10px rgba(245,200,66,.25);}
.sk-slot.cooling{opacity:.38;}
.sk-icon{font-size:1.4rem;line-height:1;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.38rem;color:#666;}
.sk-mp-cost{position:absolute;top:2px;left:3px;font-size:.38rem;color:#5599ff;}
.sk-cd-overlay{position:absolute;inset:0;background:rgba(0,0,0,.75);border-radius:5px;display:flex;align-items:center;justify-content:center;font-size:.72rem;color:var(--gold);font-weight:900;}
.ctrl-hint{position:absolute;right:12px;font-size:.46rem;color:#3a3550;line-height:1.9;text-align:right;pointer-events:none;}
#combo-display{position:absolute;top:12px;right:14px;text-align:right;pointer-events:none;opacity:0;transition:opacity .3s;z-index:45;}
#combo-num{font-family:'Black Han Sans',sans-serif;font-size:2.8rem;color:var(--gold);line-height:1;text-shadow:0 0 20px rgba(245,200,66,.8),2px 2px 0 rgba(0,0,0,.8);}
#combo-lbl{font-size:.58rem;color:var(--orange);letter-spacing:4px;}
.ov{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(8,6,15,.97);}
.ov.hidden{display:none;}
#title-ov{flex-direction:column;text-align:center;}
.title-logo{font-family:'Black Han Sans',sans-serif;font-size:3.5rem;letter-spacing:8px;background:linear-gradient(135deg,#ff4400,#ff9900,#ffcc00,#ff6600);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 30px rgba(255,150,0,.6));margin-bottom:4px;}
.title-sub{font-family:'Rajdhani',sans-serif;font-size:.9rem;color:#444;letter-spacing:10px;margin-bottom:30px;}
.char-row{display:flex;gap:10px;margin-bottom:24px;flex-wrap:wrap;justify-content:center;}
.ccard{width:115px;background:rgba(255,255,255,.02);border:1px solid rgba(245,200,66,.12);border-radius:8px;padding:12px 8px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard:hover,.ccard.sel{border-color:rgba(245,200,66,.7);background:rgba(245,200,66,.05);transform:translateY(-4px);box-shadow:0 8px 30px rgba(245,200,66,.15);}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:.75rem;color:var(--gold);letter-spacing:2px;}
.ccard-role{font-size:.5rem;color:#555;margin-top:2px;}
.ccard-stars{display:flex;justify-content:center;gap:1px;margin-top:5px;}
.star{font-size:.55rem;color:#222;}.star.on{color:var(--gold);}
.ccard-desc{font-size:.48rem;color:#444;margin-top:6px;line-height:1.5;padding:0 2px;}
.start-btn{padding:13px 50px;background:linear-gradient(135deg,#7a2e00,#ff5500);border:none;border-radius:4px;color:#fff;font-family:'Black Han Sans',sans-serif;font-size:.9rem;letter-spacing:4px;cursor:pointer;box-shadow:0 0 24px rgba(255,100,0,.4);transition:all .2s;}
.start-btn:hover{transform:scale(1.06);filter:brightness(1.2);}
.start-btn:disabled{opacity:.25;cursor:default;transform:none;}
.result-box{background:rgba(13,10,26,.98);border:1px solid var(--border);border-radius:10px;padding:28px 36px;min-width:340px;text-align:center;box-shadow:0 0 60px rgba(245,200,66,.1);}
.result-title{font-family:'Black Han Sans',sans-serif;font-size:1.8rem;letter-spacing:4px;margin-bottom:14px;}
.clear-title{color:var(--gold);text-shadow:0 0 20px rgba(245,200,66,.5);}
.over-title{color:var(--red);text-shadow:0 0 20px rgba(255,30,50,.5);}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:10px 0;text-align:left;}
.res-cell{font-size:.68rem;color:#777;display:flex;justify-content:space-between;}
.res-cell b{color:var(--gold);}
.action-row{display:flex;gap:8px;justify-content:center;margin-top:14px;}
.abtn{padding:9px 22px;border:none;border-radius:4px;cursor:pointer;font-family:'Black Han Sans',sans-serif;font-size:.78rem;letter-spacing:2px;transition:all .18s;}
.abtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.btn-next{background:linear-gradient(135deg,#1a5500,#22aa00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-gray{background:rgba(255,255,255,.07);color:#888;border:1px solid rgba(255,255,255,.1);}
#shop-ov{flex-direction:column;text-align:center;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.6rem;color:var(--gold);letter-spacing:4px;margin-bottom:8px;}
.shop-grid{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:14px 0;}
.shop-card{width:120px;background:rgba(255,255,255,.03);border:1px solid rgba(245,200,66,.15);border-radius:6px;padding:10px 8px;cursor:pointer;transition:all .18s;text-align:center;}
.shop-card:hover:not(.cant){border-color:rgba(245,200,66,.6);background:rgba(245,200,66,.06);}
.shop-card.cant{opacity:.35;cursor:default;}
.sc-icon{font-size:1.6rem;margin-bottom:5px;}
.sc-name{font-size:.65rem;color:#ccc;font-weight:700;}
.sc-desc{font-size:.5rem;color:#555;margin-top:2px;}
.sc-price{font-size:.7rem;color:var(--gold);font-weight:900;margin-top:6px;}
#lvlup-ov{flex-direction:column;text-align:center;}
.lvlup-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;color:var(--gold);letter-spacing:4px;margin-bottom:10px;}
.stat-pick-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;}
.stat-pick-btn{padding:12px 10px;border:1px solid var(--border);border-radius:5px;background:rgba(255,255,255,.04);cursor:pointer;transition:all .18s;font-family:'Noto Sans KR',sans-serif;font-size:.75rem;color:#ccc;}
.stat-pick-btn:hover{border-color:var(--gold);background:rgba(245,200,66,.07);color:var(--gold);}
@keyframes dmgUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-70px) scale(.7);}}
.dnum{position:absolute;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dmgUp 1s ease forwards;z-index:150;text-shadow:1px 1px 3px rgba(0,0,0,.9);}
#minimap{position:absolute;bottom:64px;right:10px;width:110px;height:26px;background:rgba(0,0,0,.7);border:1px solid var(--border);border-radius:3px;overflow:hidden;z-index:45;}
#mm-canvas{width:110px;height:26px;}
#equip-quick{position:absolute;bottom:64px;left:10px;z-index:45;display:flex;gap:4px;}
.eq-quick{width:34px;height:34px;background:rgba(0,0,0,.7);border:1px solid rgba(245,200,66,.2);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:.9rem;position:relative;}
.eq-quick .eq-name{position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);font-size:.38rem;color:#444;white-space:nowrap;}
#hit-flash{position:absolute;inset:0;pointer-events:none;z-index:100;opacity:0;background:rgba(255,30,30,0);transition:opacity .06s;}
@keyframes bwPulse{0%,100%{opacity:0;transform:translate(-50%,-50%) scale(.8);}30%,70%{opacity:1;transform:translate(-50%,-50%) scale(1);}}
#boss-warn{position:absolute;top:45%;left:50%;z-index:180;display:none;font-family:'Black Han Sans',sans-serif;font-size:2rem;color:#ff2233;text-shadow:0 0 30px rgba(255,0,50,1);letter-spacing:6px;text-align:center;animation:bwPulse 2.2s ease forwards;pointer-events:none;}
#achiev{position:absolute;top:54px;left:50%;transform:translateX(-50%) translateY(-80px);background:rgba(40,28,4,.97);border:1px solid rgba(245,200,66,.5);border-radius:5px;padding:7px 18px;display:flex;align-items:center;gap:8px;z-index:300;transition:transform .3s;pointer-events:none;box-shadow:0 4px 20px rgba(245,200,66,.3);}
#achiev.show{transform:translateX(-50%) translateY(0);}
#ach-icon{font-size:1.3rem;}
#ach-title{font-size:.62rem;color:var(--gold);font-weight:700;}
#ach-sub{font-size:.5rem;color:#886600;}
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-thumb{background:rgba(245,200,66,.2);border-radius:2px;}
</style>
</head>
<body>
<div id="wrap">
  <div id="hud">
    <div class="hud-char" id="hud-name">—</div>
    <div class="bar-group">
      <div class="bar-row">
        <span class="bar-label">HP</span>
        <div class="bar-bg" style="width:140px"><div class="bar-fill" id="hp-fill"></div><div class="bar-text" id="hp-text"></div></div>
      </div>
      <div class="bar-row">
        <span class="bar-label">MP</span>
        <div class="bar-bg" style="width:140px"><div class="bar-fill" id="mp-fill"></div></div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;margin-left:5px;">
      <div style="font-size:.44rem;color:#444;">XP</div>
      <div class="bar-bg" style="width:90px;height:6px;"><div class="bar-fill" id="xp-fill"></div></div>
      <div style="font-size:.42rem;color:#333;" id="xp-text">0/100</div>
    </div>
    <div id="stat-row">
      <div class="sbox"><div class="sbox-v" id="s-lv">1</div><div class="sbox-l">LV</div></div>
      <div class="sbox"><div class="sbox-v" id="s-atk" style="color:#ff7755">0</div><div class="sbox-l">ATK</div></div>
      <div class="sbox"><div class="sbox-v" id="s-def" style="color:#5599ff">0</div><div class="sbox-l">DEF</div></div>
      <div class="sbox"><div class="sbox-v" id="s-kills">0</div><div class="sbox-l">KILL</div></div>
      <div class="sbox"><div class="sbox-v" id="s-score">0</div><div class="sbox-l">SCORE</div></div>
      <div class="sbox"><div class="sbox-v" id="s-gold" style="color:var(--gold)">0</div><div class="sbox-l">💰</div></div>
    </div>
    <div id="buff-row"></div>
    <div class="floor-lbl" id="floor-lbl">1스테이지</div>
  </div>

  <div id="game-area">
    <canvas id="gc"></canvas>
    <div id="hit-flash"></div>
    <div id="boss-bar">
      <div id="boss-name-lbl">BOSS</div>
      <div id="boss-hp-bg"><div id="boss-hp-fill" style="width:100%"></div></div>
      <div id="boss-phase-txt"></div>
    </div>
    <div id="combo-display">
      <div id="combo-num">0</div>
      <div id="combo-lbl">COMBO</div>
    </div>
    <div id="minimap"><canvas id="mm-canvas" width="110" height="26"></canvas></div>
    <div id="equip-quick">
      <div class="eq-quick" id="eq-wpn">🗡️<span class="eq-name">무기</span></div>
      <div class="eq-quick" id="eq-arm">🛡️<span class="eq-name">방어</span></div>
      <div class="eq-quick" id="eq-acc">💍<span class="eq-name">장신구</span></div>
    </div>
    <div id="boss-warn">⚠ BOSS ⚠</div>
    <div id="achiev">
      <div id="ach-icon">🏆</div>
      <div><div id="ach-title">업적</div><div id="ach-sub">달성</div></div>
    </div>
    <div id="skill-bar">
      <div id="sk-cont" style="display:flex;gap:6px;"></div>
      <div class="ctrl-hint">
        ←→ 이동 &nbsp;|&nbsp; Z 점프(2단)<br>
        X 공격 &nbsp;|&nbsp; A~G 스킬<br>
        Space 회피 &nbsp;|&nbsp; P 일시정지
      </div>
    </div>

    <!-- TITLE -->
    <div class="ov" id="title-ov">
      <div>
        <div class="title-logo">던전 크러시</div>
        <div class="title-sub">DUNGEON CRUSH</div>
        <div class="char-row" id="char-row"></div>
        <div style="text-align:center">
          <button class="start-btn" id="start-btn" onclick="startPressed()" disabled>전투 시작 ▶</button>
        </div>
      </div>
    </div>

    <!-- LEVEL UP -->
    <div class="ov hidden" id="lvlup-ov">
      <div class="result-box">
        <div class="lvlup-title">⬆ LEVEL UP!</div>
        <div style="font-size:.72rem;color:#666;margin-bottom:4px;">스탯을 선택하세요</div>
        <div class="stat-pick-grid" id="stat-pick-grid"></div>
      </div>
    </div>

    <!-- SHOP -->
    <div class="ov hidden" id="shop-ov">
      <div>
        <div class="shop-title">⚗ 상점</div>
        <div style="font-size:.7rem;color:#666;margin-bottom:4px;">보유 골드: <span id="shop-gold-lbl" style="color:var(--gold);font-weight:700;">0</span></div>
        <div class="shop-grid" id="shop-grid"></div>
        <button class="abtn btn-next" onclick="continueAfterShop()" style="margin-top:4px;">다음 스테이지 →</button>
      </div>
    </div>

    <!-- STAGE CLEAR -->
    <div class="ov hidden" id="clear-ov">
      <div class="result-box">
        <div class="result-title clear-title">✦ STAGE CLEAR ✦</div>
        <div class="res-grid" id="clear-grid"></div>
        <div class="action-row">
          <button class="abtn btn-next" onclick="openShop()">상점 →</button>
          <button class="abtn btn-gray" onclick="gotoTitle()">타이틀</button>
        </div>
      </div>
    </div>

    <!-- GAME OVER -->
    <div class="ov hidden" id="over-ov">
      <div class="result-box">
        <div class="result-title over-title">💀 GAME OVER</div>
        <div class="res-grid" id="over-grid"></div>
        <div class="action-row">
          <button class="abtn btn-retry" onclick="retryStage()">재도전 ↺</button>
          <button class="abtn btn-gray" onclick="gotoTitle()">타이틀</button>
        </div>
      </div>
    </div>

    <!-- PAUSE -->
    <div class="ov hidden" id="pause-ov">
      <div style="text-align:center">
        <div style="font-family:'Black Han Sans',sans-serif;font-size:2.5rem;color:#fff;letter-spacing:6px;">⏸ PAUSE</div>
        <div style="font-size:.7rem;color:#444;margin-top:12px;letter-spacing:2px;">P 키를 눌러 계속하세요</div>
      </div>
    </div>
  </div>
</div>

<script>
'use strict';
// ═══════════════════════════════════════════════════════════
//  DUNGEON CRUSH — ENHANCED ENGINE v2.0
//  - 캐릭터별 고유 애니메이션 (걷기/달리기/공격/점프)
//  - 던전 배경: 다층 시차스크롤, 기둥, 횃불, 아치, 안개
//  - 타격감: 히트스탑, 넉백, 슬래시 이펙트, 충격파
//  - 스킬 이펙트 대폭 강화
// ═══════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx    = canvas.getContext('2d');

function resize(){
  const area = document.getElementById('game-area');
  canvas.width  = area.clientWidth  || 900;
  canvas.height = area.clientHeight || 450;
}
resize();
window.addEventListener('resize', resize);

const W  = () => canvas.width;
const H  = () => canvas.height;
const GY = () => H() - 70;

// ── INPUT ──────────────────────────────────────────────────
const KEY = {}, JK = {};
window.addEventListener('keydown', e=>{
  if(!KEY[e.key]){KEY[e.key]=true;JK[e.key]=true;}
  if([' ','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e=>KEY[e.key]=false);
function flushJK(){for(const k in JK) delete JK[k];}

// ── PARTICLES ──────────────────────────────────────────────
const PARTS = [];
function spawnParts(x,y,opts={}){
  const n=opts.n||8;
  for(let i=0;i<n;i++){
    const a=(opts.dir||0)+(Math.random()-.5)*(opts.spread||Math.PI*2);
    const s=(opts.sMin||1)+Math.random()*(opts.sMax||5);
    const col=Array.isArray(opts.col)?opts.col[Math.floor(Math.random()*opts.col.length)]:(opts.col||'#fff');
    PARTS.push({
      x,y,vx:Math.cos(a)*s+(opts.vxb||0),vy:Math.sin(a)*s-(opts.upb||0),
      life:1,decay:(opts.dMin||.02)+Math.random()*(opts.dMax||.03),
      col,sz:(opts.szMin||2)+Math.random()*(opts.szMax||5),
      glow:opts.glow||false,grav:opts.grav!==undefined?opts.grav:.15,
      type:opts.type||'c',rot:Math.random()*Math.PI*2,rotV:(Math.random()-.5)*.2,
    });
  }
}
function updateParts(dt){
  for(let i=PARTS.length-1;i>=0;i--){
    const p=PARTS[i];
    p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.grav*dt;p.vx*=.96;p.life-=p.decay*dt;
    p.rot+=p.rotV;
    if(p.life<=0) PARTS.splice(i,1);
  }
}
function drawParts(camX){
  ctx.save();
  for(const p of PARTS){
    const sx=p.x-camX;
    if(sx<-60||sx>W()+60) continue;
    ctx.globalAlpha=Math.max(0,p.life);
    if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.5;}
    ctx.fillStyle=p.col;
    if(p.type==='sq'){
      ctx.save();ctx.translate(sx,p.y);ctx.rotate(p.rot);
      ctx.fillRect(-p.sz/2,-p.sz/2,p.sz,p.sz);ctx.restore();
    } else if(p.type==='slash'){
      ctx.save();ctx.translate(sx,p.y);ctx.rotate(p.rot);
      ctx.strokeStyle=p.col;ctx.lineWidth=p.sz*.6;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(-p.sz*2,0);ctx.lineTo(p.sz*2,0);ctx.stroke();
      ctx.restore();
    } else {
      ctx.beginPath();ctx.arc(sx,p.y,p.sz,0,Math.PI*2);ctx.fill();
    }
    if(p.glow) ctx.shadowBlur=0;
  }
  ctx.globalAlpha=1;ctx.restore();
}

// ── SLASH EFFECTS ────────────────────────────────────────
const SLASHES = [];
function spawnSlash(x,y,ang,len,col,dur=12){
  SLASHES.push({x,y,ang,len,col,life:1,dur,decay:1/dur,w:3});
}
function updateSlashes(dt){
  for(let i=SLASHES.length-1;i>=0;i--){
    SLASHES[i].life-=SLASHES[i].decay*dt;
    if(SLASHES[i].life<=0) SLASHES.splice(i,1);
  }
}
function drawSlashes(camX){
  for(const s of SLASHES){
    const sx=s.x-camX;
    ctx.save();
    ctx.globalAlpha=Math.max(0,s.life)*.85;
    ctx.strokeStyle=s.col;
    ctx.shadowColor=s.col;ctx.shadowBlur=10;
    ctx.lineWidth=s.w*(s.life+.3);ctx.lineCap='round';
    ctx.beginPath();
    ctx.moveTo(sx+Math.cos(s.ang+Math.PI)*s.len*.5,s.y+Math.sin(s.ang+Math.PI)*s.len*.5);
    ctx.lineTo(sx+Math.cos(s.ang)*s.len,s.y+Math.sin(s.ang)*s.len);
    ctx.stroke();
    ctx.restore();
  }
}

// ── SHOCKWAVE EFFECTS ───────────────────────────────────
const SHOCKWAVES = [];
function spawnShockwave(x,y,col,maxR=80){
  SHOCKWAVES.push({x,y,col,r:5,maxR,life:1});
}
function updateShockwaves(dt){
  for(let i=SHOCKWAVES.length-1;i>=0;i--){
    const s=SHOCKWAVES[i];
    s.r+=s.maxR*.06*dt;s.life-=.06*dt;
    if(s.life<=0) SHOCKWAVES.splice(i,1);
  }
}
function drawShockwaves(camX){
  for(const s of SHOCKWAVES){
    const sx=s.x-camX;
    ctx.save();
    ctx.globalAlpha=s.life*.5;
    ctx.strokeStyle=s.col;ctx.shadowColor=s.col;ctx.shadowBlur=15;
    ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(sx,s.y,s.r,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;ctx.restore();
  }
}

// ══════════════════════════════════════════════════════
// DUNGEON BACKGROUND SYSTEM (multi-layer parallax)
// ══════════════════════════════════════════════════════
// Each stage has 3 BG layers + floor + ceiling details
function drawDungeonBG(stage, camX, timer){
  const w=W(), h=H(), gy=GY();
  const st=STAGES[stage];

  // Layer 0: Sky/void (furthest)
  const vgr=ctx.createLinearGradient(0,0,0,gy);
  vgr.addColorStop(0,st.skyTop);
  vgr.addColorStop(1,st.skyBot);
  ctx.fillStyle=vgr;
  ctx.fillRect(0,0,w,gy);

  // Layer 1: Far background (columns/arches, slow parallax)
  drawBGLayer1(st, camX*.05, timer);

  // Layer 2: Mid columns/torches (mid parallax)
  drawBGLayer2(st, camX*.25, timer);

  // Layer 3: Near details + fog
  drawBGLayer3(st, camX*.5, timer);

  // Ceiling
  drawCeiling(st, camX*.1, timer);

  // Floor
  drawFloorDetailed(st);
}

function drawBGLayer1(st, offX, timer){
  ctx.save();
  ctx.globalAlpha=0.55;
  // Far archways
  const archW=180, archCount=8;
  for(let i=0;i<archCount;i++){
    const bx=(i*archW*2 - offX%( archW*2*2 )) - archW;
    // Arch opening
    ctx.fillStyle=st.archDark;
    ctx.beginPath();
    ctx.roundRect(bx, 30, archW, GY()-30, [0,0,archW/2,archW/2]);
    ctx.fill();
    // Arch frame
    ctx.strokeStyle=st.archCol;
    ctx.lineWidth=14;
    ctx.beginPath();
    ctx.roundRect(bx+7, 37, archW-14, GY()-37, [0,0,(archW-14)/2,(archW-14)/2]);
    ctx.stroke();
    // Keystone at top
    ctx.fillStyle=st.archCol;
    ctx.beginPath();
    ctx.arc(bx+archW/2, 30+archW*.52+7, 12, 0, Math.PI*2);
    ctx.fill();
  }
  ctx.restore();
}

function drawBGLayer2(st, offX, timer){
  const h=H(), gy=GY();
  ctx.save();
  // Pillars every 220px
  const pilW=36, pilSpacing=220;
  const startPil = Math.floor(offX/pilSpacing)*pilSpacing - pilSpacing;
  for(let px=startPil; px<W()+offX+pilSpacing; px+=pilSpacing){
    const sx=px-offX%pilSpacing;
    // Pillar body
    const pg=ctx.createLinearGradient(sx-pilW/2,0,sx+pilW/2,0);
    pg.addColorStop(0,st.pilDark);
    pg.addColorStop(.35,st.pilMid);
    pg.addColorStop(.65,st.pilMid);
    pg.addColorStop(1,st.pilDark);
    ctx.fillStyle=pg;
    ctx.fillRect(sx-pilW/2, 0, pilW, gy);
    // Capital (top decoration)
    ctx.fillStyle=st.pilMid;
    ctx.fillRect(sx-pilW/2-6, 20, pilW+12, 12);
    ctx.fillRect(sx-pilW/2-4, 32, pilW+8, 6);
    // Base
    ctx.fillStyle=st.pilMid;
    ctx.fillRect(sx-pilW/2-6, gy-18, pilW+12, 12);
    ctx.fillRect(sx-pilW/2-4, gy-6, pilW+8, 6);
    // Crack detail
    ctx.strokeStyle=st.pilDark;ctx.lineWidth=1.5;ctx.globalAlpha=0.3;
    ctx.beginPath();ctx.moveTo(sx-4,80);ctx.lineTo(sx-2,140);ctx.lineTo(sx-5,190);ctx.stroke();
    ctx.globalAlpha=1;
    // Torch between pillars
    const tx=sx+pilSpacing/2;
    drawTorch(tx, 55, st, timer);
  }
  ctx.restore();
}

function drawBGLayer3(st, offX, timer){
  const gy=GY();
  // Ambient fog strips
  ctx.save();
  for(let i=0;i<3;i++){
    const fy = gy - 40 - i*30;
    const fa = (.06 + Math.sin(timer*.003+i)*.02)*(.7-i*.2);
    ctx.globalAlpha=fa;
    ctx.fillStyle=st.fogCol;
    ctx.fillRect(0,fy,W(),20+i*10);
  }
  // Ground cracks/runes
  ctx.globalAlpha=0.12;
  ctx.strokeStyle=st.runeCol||'#ff6600';
  ctx.lineWidth=1.5;
  const runeOff = Math.floor(offX/80)*80;
  for(let rx=runeOff-80; rx<W()+80; rx+=80){
    const rsx=rx-offX%80;
    // Simple rune shape
    ctx.beginPath();ctx.arc(rsx,gy-8,6,0,Math.PI*2);ctx.stroke();
    ctx.beginPath();ctx.moveTo(rsx-3,gy-8);ctx.lineTo(rsx+3,gy-8);ctx.stroke();
    ctx.beginPath();ctx.moveTo(rsx,gy-11);ctx.lineTo(rsx,gy-5);ctx.stroke();
  }
  ctx.restore();
}

function drawTorch(x, y, st, timer){
  ctx.save();
  ctx.globalAlpha=0.7;
  // Mount
  ctx.fillStyle=st.pilDark;
  ctx.fillRect(x-3,y,6,16);
  // Flame flicker
  const flicker=Math.sin(timer*.18+x)*.3+Math.cos(timer*.11+x)*.2;
  const fSize=9+flicker*2;
  const fGr=ctx.createRadialGradient(x,y-fSize*.5,1,x,y,fSize);
  fGr.addColorStop(0,st.torchInner||'#ffffff');
  fGr.addColorStop(.4,st.torchOuter||'#ff8800');
  fGr.addColorStop(1,'rgba(255,80,0,0)');
  ctx.fillStyle=fGr;
  ctx.globalAlpha=0.8+flicker*.1;
  ctx.beginPath();
  ctx.moveTo(x-fSize*.5,y);
  ctx.quadraticCurveTo(x+flicker*3,y-fSize*.7,x,y-fSize*1.4);
  ctx.quadraticCurveTo(x+flicker*3,y-fSize*.6,x+fSize*.5,y);
  ctx.closePath();
  ctx.fill();
  // Glow on wall
  const gGr=ctx.createRadialGradient(x,y-8,2,x,y,60);
  gGr.addColorStop(0,st.torchGlow||'rgba(255,120,0,.18)');
  gGr.addColorStop(1,'rgba(0,0,0,0)');
  ctx.globalAlpha=0.5+flicker*.1;
  ctx.fillStyle=gGr;
  ctx.fillRect(x-60,y-60,120,100);
  ctx.restore();
}

function drawCeiling(st, offX, timer){
  ctx.save();
  // Base ceiling
  const cg=ctx.createLinearGradient(0,0,0,40);
  cg.addColorStop(0,st.ceilDark);
  cg.addColorStop(1,st.ceilMid);
  ctx.fillStyle=cg;
  ctx.fillRect(0,0,W(),40);
  // Stalactites
  ctx.fillStyle=st.stalCol||st.pilDark;
  const stalOff=Math.floor(offX/70)*70;
  for(let sx2=stalOff-70; sx2<W()+70; sx2+=70){
    const sx=sx2 - offX%70;
    const sh=18+Math.sin(sx*.1)*8;
    ctx.beginPath();
    ctx.moveTo(sx-7,0);ctx.lineTo(sx+7,0);ctx.lineTo(sx,sh);ctx.closePath();
    ctx.fill();
  }
  // Drip effect
  ctx.globalAlpha=0.4;
  for(let dsx=stalOff-70; dsx<W()+70; dsx+=140){
    const sx=dsx - offX%140;
    const dy=18+Math.sin(sx*.1)*8;
    const dripY=dy+(timer%90)/90*30;
    ctx.fillStyle=st.dripCol||'rgba(0,80,200,.5)';
    ctx.beginPath();ctx.arc(sx,dripY,2,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

function drawFloorDetailed(st){
  const gy=GY();
  const fg=ctx.createLinearGradient(0,gy,0,H());
  fg.addColorStop(0,st.floorTop);
  fg.addColorStop(.3,st.floorMid);
  fg.addColorStop(1,st.floorDark);
  ctx.fillStyle=fg;
  ctx.fillRect(0,gy,W(),H()-gy);
  // Floor line highlight
  ctx.fillStyle=st.floorLine||'rgba(255,180,80,.3)';
  ctx.fillRect(0,gy,W(),2);
  // Floor tiles
  ctx.save();
  ctx.globalAlpha=0.08;
  ctx.strokeStyle=st.floorTile||'#ffffff';
  ctx.lineWidth=1;
  for(let tx=0; tx<W(); tx+=60){
    ctx.beginPath();ctx.moveTo(tx,gy);ctx.lineTo(tx,H());ctx.stroke();
  }
  for(let ty=gy; ty<H(); ty+=20){
    ctx.beginPath();ctx.moveTo(0,ty);ctx.lineTo(W(),ty);ctx.stroke();
  }
  ctx.restore();
}

// ══════════════════════════════════════════════════════
// PLATFORM RENDERING
// ══════════════════════════════════════════════════════
function drawPlatforms(st){
  for(const pl of G.platforms){
    const px=pl.x-G.cam;
    if(px>W()+10||px+pl.w<-10) continue;
    // Platform body
    const pg=ctx.createLinearGradient(px,pl.y,px,pl.y+pl.h);
    pg.addColorStop(0,st.plTop||st.floorMid);
    pg.addColorStop(1,st.plBot||st.floorDark);
    ctx.fillStyle=pg;
    ctx.beginPath();ctx.roundRect(px,pl.y,pl.w,pl.h,2);ctx.fill();
    // Top edge
    ctx.fillStyle=st.floorLine||'rgba(255,180,80,.3)';
    ctx.fillRect(px,pl.y,pl.w,2);
    // Under shadow
    ctx.fillStyle='rgba(0,0,0,.35)';
    ctx.fillRect(px,pl.y+pl.h-3,pl.w,3);
    // Decorative rune
    if(pl.w>60){
      ctx.save();ctx.globalAlpha=0.15;
      ctx.fillStyle=st.runeCol||'#ff6600';
      ctx.font='14px serif';ctx.textAlign='center';
      ctx.fillText('⬡',px+pl.w/2,pl.y+pl.h*.6);
      ctx.restore();
    }
  }
}

// ══════════════════════════════════════════════════════
// CHARACTER DRAWING — ENHANCED LIMB ANIMATION
// ══════════════════════════════════════════════════════
// Animation states: idle, walk, run, jump, atk, skill, hit, dead, dodge

function lerp(a,b,t){return a+(b-a)*t;}

function drawChar(opts){
  const {x,y,f,state='idle',walkPhase=0,atkPhase=0,hitFlash=0,dead=false,
         skinCol,hairCol,torsoCol,legsCol,weapon,offhand,headDeco,skillGlow,scale=1,
         clsId,dodgeAnim=0,jumpVy=0}=opts;
  const sc=scale;
  ctx.save();
  ctx.translate(x,y);
  if(dead){ctx.globalAlpha=.35;ctx.rotate(f*Math.PI/2);}
  if(f===-1) ctx.scale(-1,1);
  if(hitFlash>0) ctx.filter=`brightness(${2.5+hitFlash*.1}) saturate(${hitFlash<5?0:.5})`;

  const isRunning=state==='run';
  const isJumping=state==='jump';
  const isAtk=state==='atk'||atkPhase>0.1;
  const isSkill=state==='skill';
  const t=walkPhase;

  // Bounce/squash for running
  const bounce = isRunning ? Math.abs(Math.sin(t))*3 : 0;
  const squashX = isRunning ? 1+Math.abs(Math.sin(t))*.04 : 1;
  const squashY = isRunning ? 1-Math.abs(Math.sin(t))*.03 : 1;
  // Jump stretch
  const jStretch = isJumping ? (jumpVy<0?1.1:1.05) : 1;
  const jSquashX = isJumping ? (jumpVy<0?.92:.96) : 1;

  ctx.scale(squashX*jSquashX, squashY*jStretch);
  ctx.translate(0, -bounce);

  // Leg swing angles - more exaggerated when running
  const legSwingMult = isRunning ? 0.75 : isAtk ? 0.15 : 0.45;
  const legSwing = dead ? 0 : Math.sin(t) * legSwingMult;
  const legLift = dead ? 0 : Math.max(0, Math.sin(t)) * (isRunning ? 8 : 4);

  // === LEFT LEG ===
  ctx.save();
  ctx.translate(-5*sc, 2*sc);
  const lLegAng = Math.PI/2 + legSwing;
  ctx.rotate(lLegAng);
  ctx.strokeStyle = legsCol; ctx.lineWidth = 7*sc; ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  const lKneeB = dead?0:Math.max(0,Math.sin(t))*(isRunning?.5:.2);
  ctx.rotate(-lKneeB);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
  ctx.translate(0,-legLift*sc);
  // Boot
  ctx.fillStyle=legsCol;
  ctx.beginPath();ctx.ellipse(4*sc,16*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();

  // === RIGHT LEG ===
  ctx.save();
  ctx.translate(5*sc, 2*sc);
  const rLegAng = Math.PI/2 - legSwing;
  ctx.rotate(rLegAng);
  ctx.strokeStyle = legsCol; ctx.lineWidth = 7*sc; ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  const rKneeB = dead?0:Math.max(0,-Math.sin(t))*(isRunning?.5:.2);
  ctx.rotate(rKneeB);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
  // Boot
  ctx.fillStyle=legsCol;
  ctx.beginPath();ctx.ellipse(4*sc,16*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();

  // === TORSO ===
  const torsoTilt = isRunning ? Math.sin(t)*.04 : 0;
  ctx.save();
  ctx.rotate(torsoTilt);
  ctx.fillStyle=torsoCol;
  ctx.beginPath();ctx.roundRect(-10*sc,-28*sc,20*sc,30*sc,4*sc);ctx.fill();
  // Belt
  ctx.fillStyle='rgba(0,0,0,.4)';ctx.fillRect(-10*sc,-2*sc,20*sc,5*sc);
  // Chest detail
  ctx.fillStyle='rgba(255,255,255,.04)';ctx.fillRect(-8*sc,-26*sc,16*sc,12*sc);

  // === WEAPON ARM (right arm in game = left in code) ===
  const atkSwing = dead ? 0 : isAtk ? Math.sin(atkPhase)*1.1 : 0;
  const armSwing = dead ? 0 : Math.sin(t+Math.PI)*0.35*(isRunning?1.5:1);
  const atkLunge = isAtk ? Math.sin(atkPhase)*.8 : 0; // body lunge forward

  ctx.save();
  ctx.translate(10*sc+atkLunge*sc, -20*sc);
  ctx.rotate(-Math.PI/6 + atkSwing + armSwing);
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  ctx.rotate(.2 + atkSwing*.6);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  drawWeapon(ctx, weapon, sc, atkPhase, skillGlow, clsId);
  ctx.restore();

  // === OFF-HAND ARM ===
  ctx.save();
  ctx.translate(-10*sc, -20*sc);
  ctx.rotate(Math.PI/6 - armSwing + (isAtk?-.3:0));
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  ctx.rotate(-.15);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  if(offhand) drawOffhand(ctx, offhand, sc);
  ctx.restore();

  // === HEAD ===
  const headBob = isRunning ? Math.sin(t*2)*.8 : 0;
  const headTilt = isAtk ? atkSwing*.2 : (isRunning?Math.sin(t)*.04:0);
  ctx.save();
  ctx.translate(0, headBob*sc);
  ctx.rotate(headTilt);
  ctx.fillStyle=skinCol;
  ctx.beginPath();ctx.arc(0,-36*sc,12*sc,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=hairCol;
  ctx.beginPath();ctx.arc(0,-38*sc,11*sc,Math.PI,Math.PI*2);ctx.fill();
  ctx.fillRect(-11*sc,-38*sc,22*sc,6*sc);
  // Eyes - direction-aware
  ctx.fillStyle='#fff';
  ctx.beginPath();ctx.arc(4*sc,-37*sc,3.5*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=dead?'#555':isAtk?'#ff4400':'#1a0a00';
  ctx.beginPath();ctx.arc(5*sc,-37*sc,2.2*sc,0,Math.PI*2);ctx.fill();
  // Eye shine
  if(!dead){ctx.fillStyle='rgba(255,255,255,.6)';ctx.beginPath();ctx.arc(5.8*sc,-38.2*sc,.8*sc,0,Math.PI*2);ctx.fill();}
  // Eyebrow - angry when attacking
  ctx.strokeStyle=isAtk?'#ff4400':'rgba(0,0,0,.6)';
  ctx.lineWidth=(isAtk?2:1.5)*sc;ctx.lineCap='round';
  ctx.beginPath();
  if(isAtk){ctx.moveTo(1*sc,-43*sc);ctx.lineTo(8*sc,-40*sc);}
  else{ctx.moveTo(1*sc,-42*sc);ctx.lineTo(7*sc,-41*sc);}
  ctx.stroke();
  // Expression mouth when attacking
  if(isAtk&&atkPhase>1.5){
    ctx.strokeStyle='#cc4422';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.arc(4*sc,-33*sc,3*sc,0,Math.PI);ctx.stroke();
  }
  if(headDeco) drawHeadDeco(ctx, headDeco, sc);
  ctx.restore();

  // === SKILL GLOW AURA ===
  if(skillGlow){
    ctx.globalAlpha=.4+Math.sin(Date.now()*.006)*.2;
    ctx.shadowColor=skillGlow;ctx.shadowBlur=30;
    ctx.strokeStyle=skillGlow;ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.arc(0,-14*sc,28*sc,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
  }

  ctx.restore(); // torso tilt
  ctx.filter='none';
  ctx.restore();
}

function drawWeapon(ctx, wpn, sc, atkPhase, glow, clsId){
  if(!wpn) return;
  const swing=Math.sin(atkPhase)*.35;
  const isAtking=atkPhase>0.1;
  ctx.save();
  ctx.rotate(-Math.PI/4+swing);
  if(glow){ctx.shadowColor=glow;ctx.shadowBlur=14;}

  switch(wpn){
    case 'sword':
      ctx.fillStyle='#8B6914';ctx.fillRect(-3*sc,0,6*sc,12*sc);
      ctx.fillStyle='#C0A020';ctx.fillRect(-8*sc,10*sc,16*sc,4*sc);
      // Blade
      ctx.fillStyle='#e8f0ff';
      ctx.beginPath();ctx.moveTo(-2*sc,14*sc);ctx.lineTo(0,-30*sc);ctx.lineTo(2*sc,14*sc);ctx.closePath();ctx.fill();
      // Edge glint
      ctx.fillStyle='rgba(255,255,255,.7)';
      ctx.beginPath();ctx.moveTo(.5*sc,14*sc);ctx.lineTo(1*sc,-30*sc);ctx.lineTo(2*sc,14*sc);ctx.closePath();ctx.fill();
      // Swing trail when attacking
      if(isAtking){
        ctx.save();ctx.globalAlpha=.3;
        ctx.strokeStyle='#aabbff';ctx.lineWidth=8*sc;ctx.lineCap='round';
        ctx.beginPath();ctx.moveTo(0,14*sc);ctx.lineTo(0,-24*sc);ctx.stroke();
        ctx.restore();
      }
      break;

    case 'axe':
      ctx.fillStyle='#664422';ctx.fillRect(-3*sc,0,6*sc,30*sc);
      ctx.fillStyle='#B08040';
      ctx.beginPath();ctx.moveTo(-2*sc,8*sc);ctx.lineTo(-22*sc,-10*sc);ctx.lineTo(-22*sc,14*sc);ctx.lineTo(-2*sc,28*sc);ctx.closePath();ctx.fill();
      // Blade edge
      ctx.fillStyle='rgba(255,220,150,.5)';
      ctx.beginPath();ctx.moveTo(-2*sc,8*sc);ctx.lineTo(-22*sc,-10*sc);ctx.lineTo(-20*sc,2*sc);ctx.lineTo(-2*sc,18*sc);ctx.closePath();ctx.fill();
      if(isAtking){ctx.save();ctx.globalAlpha=.35;ctx.fillStyle='#ffaa44';ctx.beginPath();ctx.arc(-12*sc,4*sc,14*sc,0,Math.PI*2);ctx.fill();ctx.restore();}
      break;

    case 'bow':
      ctx.strokeStyle='#774422';ctx.lineWidth=3*sc;
      ctx.beginPath();ctx.arc(0,0,20*sc,-Math.PI*.65,Math.PI*.65);ctx.stroke();
      // String
      ctx.strokeStyle='#ddd';ctx.lineWidth=1.5*sc;
      const bowPull=isAtking?Math.sin(atkPhase)*8:0;
      ctx.beginPath();ctx.moveTo(0,-18*sc);ctx.quadraticCurveTo(bowPull*sc,0,0,18*sc);ctx.stroke();
      // Arrow
      if(isAtking&&Math.sin(atkPhase)>0.3){
        ctx.fillStyle='#cc8822';
        ctx.save();ctx.translate(bowPull*.5*sc,0);
        ctx.beginPath();ctx.moveTo(-3*sc,0);ctx.lineTo(12*sc,-2*sc);ctx.lineTo(12*sc,2*sc);ctx.closePath();ctx.fill();
        ctx.restore();
      }
      break;

    case 'staff':
      // Staff shaft with gem
      const shGr=ctx.createLinearGradient(-2*sc,-32*sc,2*sc,20*sc);
      shGr.addColorStop(0,'#8844aa');shGr.addColorStop(1,'#441166');
      ctx.fillStyle=shGr;ctx.fillRect(-2.5*sc,-32*sc,5*sc,52*sc);
      // Orb
      ctx.fillStyle='rgba(220,100,255,.85)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=18;
      ctx.beginPath();ctx.arc(0,-32*sc,9*sc,0,Math.PI*2);ctx.fill();
      // Inner orb
      ctx.fillStyle='rgba(255,180,255,.6)';
      ctx.beginPath();ctx.arc(-2*sc,-34*sc,4*sc,0,Math.PI*2);ctx.fill();
      if(isAtking){
        ctx.fillStyle='rgba(255,150,255,.4)';ctx.shadowColor='#ff88ff';ctx.shadowBlur=30;
        ctx.beginPath();ctx.arc(0,-32*sc,16*sc,0,Math.PI*2);ctx.fill();
      }
      ctx.shadowBlur=0;
      break;

    case 'gun':
      ctx.fillStyle='#2a3344';ctx.fillRect(-5*sc,-4*sc,32*sc,10*sc);
      ctx.fillStyle='#1a2233';ctx.fillRect(22*sc,-8*sc,10*sc,18*sc);
      ctx.fillStyle='#3a4455';ctx.fillRect(-8*sc,0,5*sc,8*sc);
      // Barrel details
      ctx.fillStyle='#4a5566';ctx.fillRect(-3*sc,-6*sc,10*sc,3*sc);
      if(isAtking&&Math.sin(atkPhase)>0.6){
        ctx.fillStyle='rgba(255,240,100,.8)';ctx.shadowColor='#ffee00';ctx.shadowBlur=22;
        ctx.beginPath();ctx.arc(32*sc,-3*sc,6*sc,0,Math.PI*2);ctx.fill();
        ctx.shadowBlur=0;
        ctx.fillStyle='rgba(255,255,200,.4)';ctx.fillRect(32*sc,-10*sc,20*sc,14*sc);
      }
      break;

    case 'scythe':
      // Long handle
      const shaftGr=ctx.createLinearGradient(-2*sc,-42*sc,2*sc,20*sc);
      shaftGr.addColorStop(0,'#2a3322');shaftGr.addColorStop(1,'#223322');
      ctx.fillStyle=shaftGr;ctx.fillRect(-2.5*sc,-42*sc,5*sc,62*sc);
      // Blade curve
      ctx.strokeStyle='#334422';ctx.lineWidth=5*sc;
      ctx.beginPath();ctx.arc(-10*sc,-32*sc,28*sc,-Math.PI*.25,Math.PI*.45);ctx.stroke();
      // Blade edge glow
      ctx.strokeStyle=isAtking?'rgba(150,255,100,.6)':'rgba(100,200,50,.3)';ctx.lineWidth=3*sc;
      ctx.shadowColor='#88ff44';ctx.shadowBlur=isAtking?16:5;
      ctx.beginPath();ctx.arc(-10*sc,-32*sc,28*sc,-Math.PI*.25,Math.PI*.3);ctx.stroke();
      ctx.shadowBlur=0;
      break;

    case 'dual':
      // Two short swords
      ctx.save();ctx.rotate(-.25);
      ctx.fillStyle='#c8d8f0';
      ctx.beginPath();ctx.moveTo(-1.5*sc,12*sc);ctx.lineTo(0,-20*sc);ctx.lineTo(1.5*sc,12*sc);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.5)';ctx.beginPath();ctx.moveTo(.5*sc,12*sc);ctx.lineTo(1*sc,-20*sc);ctx.lineTo(1.5*sc,12*sc);ctx.closePath();ctx.fill();
      ctx.restore();
      ctx.save();ctx.rotate(.3);ctx.translate(10*sc,2*sc);
      ctx.fillStyle='#c8d8f0';
      ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-18*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();
      ctx.restore();
      if(isAtking){ctx.save();ctx.globalAlpha=.25;ctx.strokeStyle='#aaffcc';ctx.lineWidth=10*sc;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(-6*sc,12*sc);ctx.lineTo(0,-20*sc);ctx.stroke();ctx.restore();}
      break;

    case 'hammer':
      ctx.fillStyle='#554433';ctx.fillRect(-3.5*sc,-12*sc,7*sc,42*sc);
      // Head
      const hamGr=ctx.createLinearGradient(-15*sc,-22*sc,15*sc,-2*sc);
      hamGr.addColorStop(0,'#887766');hamGr.addColorStop(.5,'#aaa090');hamGr.addColorStop(1,'#776655');
      ctx.fillStyle=hamGr;ctx.fillRect(-15*sc,-22*sc,30*sc,20*sc);
      ctx.fillStyle='rgba(255,200,100,.15)';ctx.fillRect(-13*sc,-20*sc,26*sc,8*sc);
      if(isAtking){ctx.save();ctx.globalAlpha=.2;ctx.fillStyle='#ffaa00';ctx.beginPath();ctx.arc(0,-10*sc,20*sc,0,Math.PI*2);ctx.fill();ctx.restore();}
      break;
  }
  ctx.shadowBlur=0;
  ctx.restore();
}

function drawOffhand(ctx, item, sc){
  ctx.save();ctx.rotate(Math.PI*.1);
  switch(item){
    case 'shield':
      ctx.fillStyle='#334455';ctx.beginPath();ctx.roundRect(-8*sc,0,16*sc,22*sc,3*sc);ctx.fill();
      ctx.strokeStyle='#556688';ctx.lineWidth=2*sc;ctx.stroke();
      ctx.fillStyle='rgba(100,160,255,.25)';ctx.beginPath();ctx.arc(0,11*sc,5*sc,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#88aacc';ctx.fillRect(-1*sc,3*sc,2*sc,16*sc);ctx.fillRect(-6*sc,10*sc,12*sc,2*sc);
      break;
    case 'dagger':
      ctx.fillStyle='#8B6914';ctx.fillRect(-1*sc,6*sc,2*sc,5*sc);
      ctx.fillStyle='#c0a020';ctx.fillRect(-4*sc,9*sc,8*sc,3*sc);
      ctx.fillStyle='#aabbcc';ctx.beginPath();ctx.moveTo(-1.5*sc,12*sc);ctx.lineTo(0,-10*sc);ctx.lineTo(1.5*sc,12*sc);ctx.closePath();ctx.fill();
      break;
    case 'tome':
      ctx.fillStyle='#442244';ctx.fillRect(-7*sc,0,14*sc,18*sc);
      ctx.fillStyle='rgba(200,100,255,.4)';ctx.fillRect(-5*sc,2*sc,10*sc,14*sc);
      ctx.strokeStyle='rgba(200,100,255,.6)';ctx.lineWidth=1*sc;
      ctx.beginPath();ctx.moveTo(0,3*sc);ctx.lineTo(0,15*sc);ctx.stroke();
      break;
    case 'quiver':
      ctx.fillStyle='#664422';ctx.fillRect(-4*sc,0,8*sc,20*sc);
      for(let i=0;i<3;i++){ctx.fillStyle='#cc8822';ctx.fillRect(-2*sc+i*3*sc,-2*sc,2*sc,10*sc);}
      break;
  }
  ctx.restore();
}

function drawHeadDeco(ctx, deco, sc){
  switch(deco){
    case 'helm':
      const helmGr=ctx.createLinearGradient(-14*sc,-48*sc,14*sc,-38*sc);
      helmGr.addColorStop(0,'#445566');helmGr.addColorStop(.5,'#6688aa');helmGr.addColorStop(1,'#334455');
      ctx.fillStyle=helmGr;
      ctx.beginPath();ctx.arc(0,-38*sc,14*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-14*sc,-38*sc,28*sc,6*sc);
      // Visor slot
      ctx.fillStyle='rgba(0,0,0,.6)';ctx.fillRect(-12*sc,-36*sc,24*sc,4*sc);
      ctx.fillStyle='rgba(100,180,255,.2)';ctx.fillRect(-11*sc,-36*sc,22*sc,3*sc);
      // Crest
      ctx.fillStyle='#cc8800';ctx.fillRect(-2*sc,-52*sc,4*sc,14*sc);
      break;
    case 'wizard-hat':
      ctx.fillStyle='#441166';
      ctx.beginPath();ctx.moveTo(-13*sc,-28*sc);ctx.lineTo(0,-62*sc);ctx.lineTo(13*sc,-28*sc);ctx.closePath();ctx.fill();
      // Hat brim
      ctx.fillStyle='#551188';ctx.fillRect(-16*sc,-30*sc,32*sc,6*sc);
      // Stars on hat
      ctx.fillStyle='rgba(200,100,255,.5)';
      ctx.beginPath();ctx.arc(4*sc,-44*sc,2.5*sc,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.arc(-3*sc,-52*sc,2*sc,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(220,150,255,.8)';
      ctx.beginPath();ctx.arc(0,-60*sc,3.5*sc,0,Math.PI*2);ctx.fill();
      break;
    case 'hood':
      ctx.fillStyle='#1a1a2a';
      ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(80,60,160,.25)';
      ctx.beginPath();ctx.arc(0,-38*sc,11*sc,Math.PI,Math.PI*2);ctx.fill();
      // Hood shadow
      ctx.fillStyle='rgba(0,0,0,.4)';ctx.fillRect(-8*sc,-40*sc,14*sc,6*sc);
      break;
    case 'cap':
      ctx.fillStyle='#223322';ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-15*sc,-40*sc,30*sc,6*sc);
      ctx.fillStyle='#334433';ctx.fillRect(-14*sc,-38*sc,28*sc,4*sc);
      break;
    case 'headband':
      ctx.strokeStyle='#cc3322';ctx.lineWidth=5*sc;
      ctx.beginPath();ctx.arc(0,-36*sc,13*sc,Math.PI*1.1,Math.PI*1.9);ctx.stroke();
      ctx.fillStyle='#dd3322';ctx.fillRect(-3*sc,-50*sc,6*sc,6*sc);
      break;
    case 'goggles':
      ctx.fillStyle='#222';ctx.fillRect(-12*sc,-42*sc,24*sc,7*sc);
      ctx.fillStyle='rgba(0,200,255,.3)';ctx.fillRect(-11*sc,-41*sc,9*sc,5*sc);
      ctx.fillStyle='rgba(0,200,255,.3)';ctx.fillRect(2*sc,-41*sc,9*sc,5*sc);
      ctx.strokeStyle='#555';ctx.lineWidth=2*sc;
      ctx.beginPath();ctx.roundRect(-11*sc,-41*sc,9*sc,5*sc,1*sc);ctx.stroke();
      ctx.beginPath();ctx.roundRect(2*sc,-41*sc,9*sc,5*sc,1*sc);ctx.stroke();
      break;
    case 'crown':
      ctx.fillStyle='#cc8800';
      ctx.beginPath();
      ctx.moveTo(-12*sc,-38*sc);ctx.lineTo(-12*sc,-50*sc);ctx.lineTo(-6*sc,-44*sc);
      ctx.lineTo(0,-54*sc);ctx.lineTo(6*sc,-44*sc);ctx.lineTo(12*sc,-50*sc);ctx.lineTo(12*sc,-38*sc);
      ctx.closePath();ctx.fill();
      ctx.fillStyle='#ffcc00';ctx.fillRect(-12*sc,-40*sc,24*sc,3*sc);
      // Gems
      ctx.fillStyle='#ff4444';ctx.beginPath();ctx.arc(-8*sc,-44*sc,2.5*sc,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#44ff44';ctx.beginPath();ctx.arc(8*sc,-44*sc,2.5*sc,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#4444ff';ctx.beginPath();ctx.arc(0,-49*sc,3*sc,0,Math.PI*2);ctx.fill();
      break;
  }
}

// ══════════════════════════════════════════════════════
// MONSTER DRAWING — ENHANCED
// ══════════════════════════════════════════════════════
function drawMonster(e, camX){
  const x=e.x-camX, y=e.y;
  const dead=!e.alive;
  const sc=e.drawScale||1;
  ctx.save();
  ctx.translate(x+e.w/2, y+e.h*.9);
  if(dead){ctx.globalAlpha=.25;ctx.rotate(e.f*Math.PI/2);}
  if(e.f===1) ctx.scale(-1,1);
  if(e.hitFlash>0) ctx.filter=`brightness(${2.5+e.hitFlash*.15}) saturate(0)`;
  if(e.frozen>0) ctx.filter='hue-rotate(200deg) brightness(1.8) saturate(2)';
  if(e.cursed>0){ctx.shadowColor='#8833cc';ctx.shadowBlur=12;}

  const wp=e.walkPhase||0;
  const ap=e.atkPhase||0;
  const drawFn=MONSTER_DRAW[e.drawType]||drawMonster_basic;
  drawFn(ctx, sc, wp, ap, e);

  ctx.filter='none';ctx.shadowBlur=0;
  ctx.restore();

  // HP bar (only when damaged)
  if(!dead&&e.hp<e.maxHp){
    const hpPct=Math.max(0,e.hp/e.maxHp);
    const bw=Math.max(36,e.w+8),bx=x+e.w/2-bw/2,by=y-12;
    ctx.fillStyle='rgba(0,0,0,.7)';ctx.fillRect(bx,by,bw,6);
    const hCol=hpPct>.5?'#22cc22':hpPct>.25?'#ccaa00':'#cc2200';
    ctx.fillStyle=hCol;ctx.fillRect(bx,by,bw*hpPct,6);
    if(e.frozen>0){ctx.fillStyle='rgba(100,180,255,.4)';ctx.fillRect(bx,by,bw,6);}
    if(e.burn>0){ctx.fillStyle='rgba(255,100,0,.3)';ctx.fillRect(bx,by,bw,6);}
    if(e.cursed>0){ctx.fillStyle='rgba(150,0,200,.3)';ctx.fillRect(bx,by,bw,6);}
    // HP bar border
    ctx.strokeStyle='rgba(255,255,255,.15)';ctx.lineWidth=1;
    ctx.strokeRect(bx,by,bw,6);
  }

  // Status icons above enemy
  if(!dead){
    let icons='';let ix=0;
    if(e.frozen>0)icons+='❄️';
    if(e.cursed>0)icons+='💜';
    if(e.poison>0)icons+='🟢';
    if(e.burn>0)icons+='🔥';
    if(icons){
      ctx.font='11px serif';ctx.textAlign='center';
      ctx.fillText(icons.substring(0,4),x+e.w/2,y-16);
    }
  }
}

function drawMonster_basic(ctx,sc,wp,ap,e){
  const bodyCol=e.bodyCol||'#556644';
  const headCol=e.headCol||'#667755';
  const limbCol=e.limbCol||'#445533';
  const ls=Math.sin(wp)*.4;
  const as=Math.sin(ap)*.6;
  // Legs
  for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
    ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
    ctx.strokeStyle=limbCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.restore();
  }
  // Arms
  ctx.save();ctx.translate(10*sc,-14*sc);ctx.rotate(-Math.PI/6+as);
  ctx.strokeStyle=limbCol;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();ctx.restore();
  ctx.save();ctx.translate(-10*sc,-14*sc);ctx.rotate(Math.PI/6-as);
  ctx.strokeStyle=limbCol;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();ctx.restore();
  ctx.fillStyle=bodyCol;ctx.beginPath();ctx.roundRect(-10*sc,-28*sc,20*sc,28*sc,3*sc);ctx.fill();
  ctx.fillStyle=headCol;ctx.beginPath();ctx.ellipse(0,-34*sc,11*sc,10*sc,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff2200';ctx.beginPath();ctx.arc(-4*sc,-36*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(4*sc,-36*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff6600';ctx.beginPath();ctx.arc(-3*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(5*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
}

const MONSTER_DRAW = {
  goblin:(ctx,sc,wp,ap,e)=>{
    const lc=e.limbCol||'#22aa44',bc=e.bodyCol||'#338855',hc=e.headCol||'#22aa33';
    const ls=Math.sin(wp)*.55,as=Math.sin(ap)*.7;
    // Legs - more energetic
    for(const [ox,side] of [[-3*sc,-1],[3*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
      // Knee joint
      ctx.translate(0,13*sc);ctx.rotate(Math.max(0,ls*side)*.3);
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,8*sc);ctx.stroke();
      ctx.restore();
    }
    // Weapon arm
    ctx.save();ctx.translate(8*sc,-10*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    ctx.translate(0,12*sc);ctx.rotate(.25+as*.3);
    // Dagger
    ctx.fillStyle='#8B6914';ctx.fillRect(-1*sc,0,2*sc,4*sc);
    ctx.fillStyle='#aabbcc';ctx.beginPath();ctx.moveTo(-1.5*sc,4*sc);ctx.lineTo(0,-12*sc);ctx.lineTo(1.5*sc,4*sc);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-8*sc,-10*sc);ctx.rotate(Math.PI/5-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();ctx.restore();
    // Body
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-8*sc,-22*sc,16*sc,22*sc,3*sc);ctx.fill();
    // Head - goblin proportions (big)
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-28*sc,11*sc,10*sc,0,0,Math.PI*2);ctx.fill();
    // Huge ears
    ctx.fillStyle=hc;
    ctx.beginPath();ctx.ellipse(-14*sc,-27*sc,6*sc,4*sc,-Math.PI/5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(14*sc,-27*sc,6*sc,4*sc,Math.PI/5,0,Math.PI*2);ctx.fill();
    // Inner ear
    ctx.fillStyle='rgba(255,150,150,.3)';
    ctx.beginPath();ctx.ellipse(-14*sc,-27*sc,3*sc,2*sc,-Math.PI/5,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(14*sc,-27*sc,3*sc,2*sc,Math.PI/5,0,Math.PI*2);ctx.fill();
    // Eyes (yellow)
    ctx.fillStyle='#ffcc00';ctx.beginPath();ctx.arc(-3*sc,-29*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(3*sc,-29*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#222';ctx.beginPath();ctx.arc(-2.5*sc,-29*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(3.5*sc,-29*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    // Teeth
    ctx.fillStyle='#fff';ctx.fillRect(-4*sc,-22*sc,3*sc,4*sc);ctx.fillRect(1*sc,-22*sc,3*sc,4*sc);
    // Nose (little bump)
    ctx.fillStyle='rgba(0,0,0,.2)';ctx.beginPath();ctx.arc(0*sc,-24*sc,2*sc,0,Math.PI*2);ctx.fill();
  },

  skeleton:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.42,as=Math.sin(ap)*.75;
    const bc='#d4c8a0',lc='#c4b888';
    // Pelvis
    ctx.strokeStyle=bc;ctx.lineWidth=3*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(-6*sc,0);ctx.lineTo(6*sc,0);ctx.stroke();
    // Leg bones
    for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=4*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
      ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,10*sc,3.5*sc,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.moveTo(0,10*sc);ctx.lineTo(2*sc,16*sc);ctx.stroke();
      ctx.restore();
    }
    // Spine
    ctx.strokeStyle=bc;ctx.lineWidth=3*sc;
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,-28*sc);ctx.stroke();
    // Ribs
    for(let i=0;i<4;i++){
      ctx.strokeStyle=bc;ctx.lineWidth=2*sc;
      ctx.beginPath();ctx.arc(0,(-8-i*5)*sc,9*sc,0,Math.PI);ctx.stroke();
    }
    // Arms
    ctx.save();ctx.translate(10*sc,-22*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.translate(0,14*sc);ctx.rotate(.2+as*.35);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    // Sword
    ctx.translate(0,12*sc);ctx.rotate(-Math.PI/6);
    ctx.fillStyle='#c0c8d0';
    ctx.beginPath();ctx.moveTo(-1.5*sc,0);ctx.lineTo(0,-26*sc);ctx.lineTo(1.5*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-22*sc);ctx.rotate(Math.PI/5-as);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.translate(0,14*sc);ctx.rotate(-.2);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    // Shield
    ctx.fillStyle='#2a3a4a';ctx.beginPath();ctx.roundRect(-7*sc,0,14*sc,16*sc,2*sc);ctx.fill();
    ctx.strokeStyle='#3a4a5a';ctx.lineWidth=1.5*sc;ctx.stroke();
    ctx.restore();
    // Skull
    ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,-36*sc,12*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=lc;ctx.fillRect(-8*sc,-28*sc,16*sc,6*sc);
    // Eye sockets
    ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(-4.5*sc,-38*sc,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(4.5*sc,-38*sc,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();
    // Glowing eyes
    ctx.fillStyle='rgba(0,200,255,.7)';ctx.shadowColor='#00ccff';ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(-4*sc,-38*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-38*sc,2*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Teeth
    ctx.fillStyle='#111';
    for(let t=-3;t<=3;t++) ctx.fillRect((t*2.4-1)*sc,-27*sc,2*sc,4*sc);
    // Nasal cavity
    ctx.fillStyle='#111';ctx.beginPath();ctx.arc(0,-34*sc,2*sc,0,Math.PI*2);ctx.fill();
  },

  orc:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.3,as=Math.sin(ap)*.6;
    const bc='#3a5a2a',lc='#2a4a1a',hc='#4a6a3a';
    // Wide muscular legs
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=10*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.lineWidth=9*sc;ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,30*sc);ctx.stroke();
      ctx.restore();
    }
    // Big arms
    ctx.save();ctx.translate(15*sc,-22*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=lc;ctx.lineWidth=10*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.2+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    // Axe
    ctx.fillStyle='#5a5040';ctx.fillRect(-3*sc,0,6*sc,8*sc);
    ctx.fillStyle='#888070';
    ctx.beginPath();ctx.moveTo(-2*sc,6*sc);ctx.lineTo(-24*sc,-10*sc);ctx.lineTo(-24*sc,14*sc);ctx.lineTo(-2*sc,26*sc);ctx.closePath();ctx.fill();
    ctx.fillStyle='rgba(255,200,100,.3)';
    ctx.beginPath();ctx.moveTo(-2*sc,6*sc);ctx.lineTo(-24*sc,-10*sc);ctx.lineTo(-22*sc,2*sc);ctx.lineTo(-2*sc,16*sc);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-15*sc,-22*sc);ctx.rotate(Math.PI/5-as);
    ctx.strokeStyle=lc;ctx.lineWidth=10*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,20*sc);ctx.stroke();ctx.restore();
    // Muscular torso
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-15*sc,-38*sc,30*sc,38*sc,5*sc);ctx.fill();
    // Armor
    ctx.fillStyle='#445533';ctx.fillRect(-13*sc,-32*sc,26*sc,14*sc);
    ctx.strokeStyle='#556644';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.moveTo(0,-38*sc);ctx.lineTo(0,0);ctx.stroke();
    // Shoulder pads
    ctx.fillStyle='#334422';
    ctx.beginPath();ctx.arc(-15*sc,-28*sc,8*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(15*sc,-28*sc,8*sc,0,Math.PI*2);ctx.fill();
    // Big orc head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-46*sc,16*sc,14*sc,0,0,Math.PI*2);ctx.fill();
    // Tusks
    ctx.fillStyle='#eeddcc';
    ctx.beginPath();ctx.moveTo(-7*sc,-36*sc);ctx.lineTo(-12*sc,-26*sc);ctx.lineTo(-4*sc,-36*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(7*sc,-36*sc);ctx.lineTo(12*sc,-26*sc);ctx.lineTo(4*sc,-36*sc);ctx.fill();
    // Eyes
    ctx.fillStyle='#ff3300';ctx.shadowColor='#ff3300';ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(-5*sc,-48*sc,4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-48*sc,4*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.fillStyle='#220000';ctx.beginPath();ctx.arc(-5*sc,-48*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-48*sc,2*sc,0,Math.PI*2);ctx.fill();
    // Mohawk
    ctx.fillStyle='#cc2200';
    ctx.beginPath();ctx.moveTo(-3*sc,-58*sc);ctx.lineTo(0,-70*sc);ctx.lineTo(3*sc,-58*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(-3*sc,-55*sc);ctx.lineTo(0,-66*sc);ctx.lineTo(3*sc,-55*sc);ctx.closePath();ctx.fill();
    // Scar
    ctx.strokeStyle='rgba(255,100,80,.6)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-8*sc,-50*sc);ctx.lineTo(-2*sc,-42*sc);ctx.stroke();
  },

  mage_enemy:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.25,as=Math.sin(ap)*.55;
    const bc='#2a1a4a',lc='#3a2a5a',hc='#3a2a6a';
    // Robe (triangular)
    const robGr=ctx.createLinearGradient(-16*sc,-48*sc,16*sc,0);
    robGr.addColorStop(0,bc);robGr.addColorStop(1,'#1a0a2a');
    ctx.fillStyle=robGr;
    ctx.beginPath();ctx.moveTo(-16*sc,0);ctx.lineTo(16*sc,0);ctx.lineTo(10*sc,-48*sc);ctx.lineTo(-10*sc,-48*sc);ctx.closePath();ctx.fill();
    // Robe trim
    ctx.strokeStyle='rgba(150,100,255,.4)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-16*sc,0);ctx.lineTo(-10*sc,-48*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(16*sc,0);ctx.lineTo(10*sc,-48*sc);ctx.stroke();
    // Magical runes on robe
    ctx.globalAlpha=0.2+Math.sin(Date.now()*.004)*0.1;
    ctx.fillStyle='#aa88ff';ctx.font=`${8*sc}px serif`;
    ctx.textAlign='center';ctx.fillText('⬡',0,-20*sc);
    ctx.fillText('✦',-6*sc,-32*sc);ctx.fillText('✦',6*sc,-30*sc);
    ctx.globalAlpha=1;
    // Staff arm
    ctx.save();ctx.translate(10*sc,-32*sc);ctx.rotate(-Math.PI/3+as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.translate(0,16*sc);
    ctx.fillStyle='#8833bb';ctx.fillRect(-2.5*sc,0,5*sc,-32*sc);
    ctx.fillStyle='rgba(200,100,255,.9)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=16;
    ctx.beginPath();ctx.arc(0,-32*sc,8*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(255,200,255,.5)';ctx.beginPath();ctx.arc(-2*sc,-34*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.restore();
    // Other arm
    ctx.save();ctx.translate(-10*sc,-32*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();ctx.restore();
    // Floaty particles
    ctx.save();ctx.globalAlpha=0.4;
    for(let i=0;i<3;i++){
      const fa=Date.now()*.002+i*2.1;
      const fr=22*sc;
      ctx.fillStyle='rgba(180,100,255,.6)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=8;
      ctx.beginPath();ctx.arc(Math.cos(fa)*fr,-24*sc+Math.sin(fa*.7)*8*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    }
    ctx.shadowBlur=0;ctx.restore();
    // Head with wizard hat
    ctx.fillStyle=hc;ctx.beginPath();ctx.arc(0,-54*sc,12*sc,0,Math.PI*2);ctx.fill();
    // Wizard hat
    ctx.fillStyle='#330066';
    ctx.beginPath();ctx.moveTo(-14*sc,-46*sc);ctx.lineTo(0,-74*sc);ctx.lineTo(14*sc,-46*sc);ctx.closePath();ctx.fill();
    ctx.fillRect(-16*sc,-48*sc,32*sc,5*sc);
    ctx.fillStyle='rgba(180,80,255,.6)';ctx.beginPath();ctx.arc(0,-72*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    // Glowing eyes
    ctx.fillStyle='rgba(200,100,255,.95)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(-4.5*sc,-55*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4.5*sc,-55*sc,3.5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },

  zombie:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.18,as=Math.sin(ap)*.4;
    const bc='#3d5a30',lc='#2d4a22',hc='#4d5a38';
    // Shambling legs
    for(const [ox,side] of [[-5*sc,-1],[5*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side*.4);
      ctx.strokeStyle=lc;ctx.lineWidth=6.5*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,16*sc);ctx.lineTo(3*sc,28*sc);ctx.stroke();
      ctx.restore();
    }
    // Outstretched arms (zombie pose)
    ctx.save();ctx.translate(10*sc,-18*sc);ctx.rotate(-Math.PI*.65+as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=6.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,16*sc);ctx.lineTo(2*sc,30*sc);ctx.stroke();
    // Clawed hand
    for(let c=-1;c<=1;c++){ctx.strokeStyle='#88aa66';ctx.lineWidth=2*sc;ctx.beginPath();ctx.moveTo(c*3*sc,30*sc);ctx.lineTo(c*5*sc,38*sc);ctx.stroke();}
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-18*sc);ctx.rotate(-Math.PI*.58+as*.3);
    ctx.strokeStyle=lc;ctx.lineWidth=6.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();ctx.moveTo(0,14*sc);ctx.lineTo(2*sc,24*sc);ctx.stroke();ctx.restore();
    // Torn body
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-11*sc,-32*sc,22*sc,32*sc,3*sc);ctx.fill();
    // Torn cloth tears
    ctx.strokeStyle='rgba(0,0,0,.4)';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.moveTo(-8*sc,-30*sc);ctx.lineTo(-6*sc,-10*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(6*sc,-28*sc);ctx.lineTo(4*sc,-12*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-2*sc,-26*sc);ctx.lineTo(0*sc,-8*sc);ctx.stroke();
    // Blood splatters
    ctx.fillStyle='rgba(140,0,0,.7)';
    ctx.beginPath();ctx.arc(-6*sc,-20*sc,4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-14*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    // Zombie face
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-38*sc,11*sc,10*sc,.1,0,Math.PI*2);ctx.fill();
    // Decomposing details
    ctx.fillStyle='rgba(0,80,0,.3)';ctx.beginPath();ctx.arc(-3*sc,-36*sc,4*sc,0,Math.PI*2);ctx.fill();
    // Green glowing eyes
    ctx.fillStyle='#003300';ctx.beginPath();ctx.arc(-4*sc,-40*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-40*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(0,220,80,.8)';ctx.shadowColor='#00cc44';ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(-3.5*sc,-40*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4.5*sc,-40*sc,2*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Jaw hanging open
    ctx.fillStyle='#334422';ctx.fillRect(-6*sc,-30*sc,12*sc,5*sc);
    ctx.fillStyle='#223311';ctx.fillRect(-5*sc,-30*sc,10*sc,2*sc);
    // Teeth
    ctx.fillStyle='#ccccaa';
    for(let t=-2;t<=2;t++) ctx.fillRect((t*2.5-1)*sc,-30*sc,2.5*sc,4*sc);
  },

  dragon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.2,as=Math.sin(ap)*.5;
    const bc='#1a3a1a',sc2='#2a5a2a',hc='#1a4a1a';
    // Animated tail
    const tailWag=Math.sin(Date.now()*.003)*.3;
    ctx.strokeStyle=bc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(16*sc,-10*sc);
    ctx.quadraticCurveTo(42*sc+tailWag*20,10*sc,32*sc,-24*sc+tailWag*10);ctx.stroke();
    ctx.lineWidth=5*sc;ctx.beginPath();ctx.moveTo(32*sc,-24*sc+tailWag*10);
    ctx.lineTo(44*sc,-16*sc+tailWag*15);ctx.stroke();
    ctx.lineWidth=2*sc;ctx.beginPath();ctx.moveTo(44*sc,-16*sc+tailWag*15);
    ctx.lineTo(52*sc,-8*sc+tailWag*20);ctx.stroke();
    // Wings (animated)
    const wingBeat=Math.sin(Date.now()*.004)*0.15;
    ctx.fillStyle='rgba(30,60,30,.75)';
    ctx.beginPath();ctx.moveTo(-5*sc,-36*sc);ctx.lineTo(-45*sc,-65*sc+wingBeat*20*sc);
    ctx.lineTo(-40*sc,-22*sc);ctx.lineTo(-5*sc,-15*sc);ctx.closePath();ctx.fill();
    // Wing membranes
    ctx.strokeStyle='rgba(60,100,60,.4)';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.moveTo(-5*sc,-36*sc);ctx.lineTo(-30*sc,-50*sc+wingBeat*15*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-5*sc,-36*sc);ctx.lineTo(-38*sc,-40*sc+wingBeat*10*sc);ctx.stroke();
    // Legs
    for(const [ox,side] of [[-7*sc,-1],[7*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=9*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.strokeStyle='#888888';ctx.lineWidth=2*sc;
      for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,18*sc),ctx.lineTo(c*7*sc,28*sc),ctx.stroke();
      ctx.restore();
    }
    // Clawed arms
    ctx.save();ctx.translate(15*sc,-26*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=bc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.strokeStyle='#aaaaaa';ctx.lineWidth=2.5*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,16*sc),ctx.lineTo(c*7*sc,25*sc),ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-15*sc,-26*sc);ctx.rotate(Math.PI/4-as);
    ctx.strokeStyle=bc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();ctx.restore();
    // Body (ellipsoid)
    ctx.fillStyle=bc;ctx.beginPath();ctx.ellipse(0,-22*sc,18*sc,24*sc,0,0,Math.PI*2);ctx.fill();
    // Scales
    ctx.fillStyle=sc2;
    for(let i=0;i<4;i++) ctx.beginPath(),ctx.arc(0,(-32+i*9)*sc,7*sc,0,Math.PI*2),ctx.fill();
    // Neck
    ctx.fillStyle=bc;ctx.beginPath();ctx.ellipse(0,-46*sc,8*sc,12*sc,0,0,Math.PI*2);ctx.fill();
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-56*sc,16*sc,12*sc,-.25,0,Math.PI*2);ctx.fill();
    // Snout
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(10*sc,-54*sc,10*sc,6*sc,-.2,0,Math.PI*2);ctx.fill();
    // Nostrils
    ctx.fillStyle='rgba(0,0,0,.5)';ctx.beginPath();ctx.arc(16*sc,-56*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(16*sc,-51*sc,2*sc,0,Math.PI*2);ctx.fill();
    // Fire breath when attacking
    if(ap>0.4){
      const fireInt=0.5+Math.sin(ap)*0.5;
      ctx.fillStyle=`rgba(255,${Math.round(100+fireInt*100)},0,.8)`;ctx.shadowColor='#ff6600';ctx.shadowBlur=20;
      ctx.beginPath();ctx.arc(18*sc,-54*sc,6+fireInt*4,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    }
    // Dragon eye
    ctx.fillStyle='#ffaa00';ctx.beginPath();ctx.ellipse(-5*sc,-60*sc,5*sc,3.5*sc,.3,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#110000';ctx.beginPath();ctx.ellipse(-4*sc,-60*sc,2*sc,3*sc,.3,0,Math.PI*2);ctx.fill();
    // Horns
    ctx.fillStyle='#778888';ctx.strokeStyle='#778888';ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(-9*sc,-62*sc);ctx.lineTo(-14*sc,-76*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-3*sc,-64*sc);ctx.lineTo(-6*sc,-76*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-14*sc,-76*sc);ctx.lineTo(-18*sc,-70*sc);ctx.stroke();
  },

  demon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.3,as=Math.sin(ap)*.7;
    const bc='#4a0a0a',lc='#3a0808',hc='#550a0a';
    // Legs (demon has hooves)
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=8*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(3*sc,28*sc);ctx.stroke();
      ctx.fillStyle='#110000';ctx.beginPath();ctx.ellipse(3*sc,28*sc,5.5*sc,4*sc,0,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
    // Wings (large, flapping)
    const wbeat=Math.sin(Date.now()*.005)*.2;
    ctx.fillStyle='rgba(100,0,0,.85)';
    ctx.beginPath();ctx.moveTo(0,-32*sc);
    ctx.lineTo(-50*sc-wbeat*10*sc,-60*sc+wbeat*15*sc);
    ctx.lineTo(-36*sc,-12*sc);ctx.lineTo(-6*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(0,-32*sc);
    ctx.lineTo(50*sc+wbeat*10*sc,-60*sc+wbeat*15*sc);
    ctx.lineTo(36*sc,-12*sc);ctx.lineTo(6*sc,-10*sc);ctx.closePath();ctx.fill();
    // Wing bones
    ctx.strokeStyle='rgba(150,0,0,.5)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(0,-32*sc);ctx.lineTo(-50*sc-wbeat*10*sc,-60*sc+wbeat*15*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,-32*sc);ctx.lineTo(50*sc+wbeat*10*sc,-60*sc+wbeat*15*sc);ctx.stroke();
    // Arms
    ctx.save();ctx.translate(13*sc,-24*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.35+as*.5);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.strokeStyle='#ff3300';ctx.lineWidth=2*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*3.5*sc,14*sc),ctx.lineTo(c*7*sc,24*sc),ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-13*sc,-24*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();ctx.restore();
    // Torso
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-13*sc,-40*sc,26*sc,40*sc,5*sc);ctx.fill();
    ctx.fillStyle='rgba(255,0,0,.12)';ctx.beginPath();ctx.arc(0,-22*sc,11*sc,0,Math.PI*2);ctx.fill();
    // Glowing chest rune
    ctx.fillStyle='rgba(255,0,0,.4)';ctx.shadowColor='#ff0000';ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(0,-20*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-50*sc,14*sc,13*sc,0,0,Math.PI*2);ctx.fill();
    // Curved horns
    ctx.fillStyle='#550000';
    ctx.beginPath();ctx.moveTo(-8*sc,-58*sc);ctx.quadraticCurveTo(-24*sc,-74*sc,-16*sc,-64*sc);ctx.lineTo(-6*sc,-56*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(8*sc,-58*sc);ctx.quadraticCurveTo(24*sc,-74*sc,16*sc,-64*sc);ctx.lineTo(6*sc,-56*sc);ctx.closePath();ctx.fill();
    // Glowing red eyes
    ctx.fillStyle='#ff0000';ctx.shadowColor='#ff0000';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(-5*sc,-52*sc,4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-52*sc,4*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.fillStyle='#220000';ctx.beginPath();ctx.arc(-5*sc,-52*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-52*sc,2*sc,0,Math.PI*2);ctx.fill();
    // Fangs
    ctx.fillStyle='#ddcccc';ctx.fillRect(-5*sc,-40*sc,3*sc,5*sc);ctx.fillRect(2*sc,-40*sc,3*sc,5*sc);
  },

  golem:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.12,as=Math.sin(ap)*.35;
    const bc='#6a5a4a',lc='#7a6a5a',hc='#8a7a6a';
    // Stone legs
    for(const [ox,side] of [[-8*sc,-1],[8*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.fillStyle=bc;ctx.fillRect(-7*sc,-2*sc,14*sc,22*sc);
      // Stone texture lines
      ctx.strokeStyle='rgba(0,0,0,.25)';ctx.lineWidth=1*sc;
      ctx.beginPath();ctx.moveTo(-3*sc,0);ctx.lineTo(-3*sc,20*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(3*sc,2*sc);ctx.lineTo(3*sc,18*sc);ctx.stroke();
      ctx.restore();
    }
    // Massive arms
    ctx.save();ctx.translate(20*sc,-28*sc);ctx.rotate(-Math.PI/6+as);
    ctx.fillStyle=lc;ctx.fillRect(-8*sc,-2*sc,16*sc,24*sc);
    ctx.fillRect(-6*sc,24*sc,16*sc,20*sc);
    // Cracks
    ctx.strokeStyle='rgba(0,0,0,.4)';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.moveTo(-2*sc,2*sc);ctx.lineTo(1*sc,20*sc);ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-20*sc,-28*sc);ctx.rotate(Math.PI/6-as);
    ctx.fillStyle=lc;ctx.fillRect(-8*sc,-2*sc,16*sc,24*sc);ctx.fillRect(-10*sc,24*sc,16*sc,20*sc);ctx.restore();
    // Torso (massive rectangle)
    ctx.fillStyle=bc;ctx.fillRect(-20*sc,-48*sc,40*sc,48*sc);
    // Body cracks
    ctx.strokeStyle='rgba(0,0,0,.35)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-6*sc,-44*sc);ctx.lineTo(3*sc,-24*sc);ctx.lineTo(-3*sc,-10*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(9*sc,-38*sc);ctx.lineTo(14*sc,-16*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-12*sc,-22*sc);ctx.lineTo(-8*sc,-6*sc);ctx.stroke();
    // Glowing core
    const cPulse=0.7+Math.sin(Date.now()*.003)*.3;
    ctx.fillStyle=`rgba(255,${Math.round(120+cPulse*60)},0,${cPulse*.7})`;ctx.shadowColor='#ff8800';ctx.shadowBlur=22;
    ctx.beginPath();ctx.arc(0,-24*sc,8*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Shoulder pads
    ctx.fillStyle=hc;ctx.fillRect(-22*sc,-46*sc,12*sc,12*sc);ctx.fillRect(10*sc,-46*sc,12*sc,12*sc);
    // Head (stone cube)
    ctx.fillStyle=hc;ctx.fillRect(-16*sc,-66*sc,32*sc,22*sc);
    // Face indentations
    ctx.fillStyle='rgba(0,0,0,.5)';ctx.fillRect(-12*sc,-62*sc,10*sc,12*sc);ctx.fillRect(2*sc,-62*sc,10*sc,12*sc);
    // Glowing eyes
    ctx.fillStyle=`rgba(255,${Math.round(150+cPulse*80)},0,.85)`;ctx.shadowColor='#ffaa00';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(-7*sc,-56*sc,4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(7*sc,-56*sc,4*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },

  lich:(ctx,sc,wp,ap,e)=>{
    const as=Math.sin(ap)*.5;
    const bc='#1a1a3a',lc='#2a2a4a',hc='#222240';
    // Floating offset
    const float=Math.sin(Date.now()*.002)*5;
    // Robe wisps
    ctx.strokeStyle='rgba(100,100,220,.35)';ctx.lineWidth=3*sc;
    for(let i=-2;i<=2;i++){
      ctx.beginPath();
      ctx.moveTo(i*7*sc,6*sc+float);
      ctx.quadraticCurveTo(i*9*sc+Math.sin(Date.now()*.003+i)*6,22*sc+float,i*5*sc,30*sc+float);
      ctx.stroke();
    }
    // Robe body
    const robGr=ctx.createLinearGradient(-16*sc,-48*sc+float,16*sc,8*sc+float);
    robGr.addColorStop(0,bc);robGr.addColorStop(1,'rgba(20,20,50,.5)');
    ctx.fillStyle=robGr;
    ctx.beginPath();ctx.moveTo(-16*sc,-10*sc+float);ctx.lineTo(16*sc,-10*sc+float);
    ctx.lineTo(20*sc,8*sc+float);ctx.lineTo(-20*sc,8*sc+float);ctx.closePath();ctx.fill();
    ctx.fillStyle=bc;ctx.fillRect(-12*sc,-48*sc+float,24*sc,38*sc);
    // Robe runes
    ctx.globalAlpha=0.2+Math.sin(Date.now()*.005)*0.1;
    ctx.fillStyle='#6666ff';ctx.font=`${7*sc}px serif`;ctx.textAlign='center';
    ctx.fillText('⬡',0,-30*sc+float);ctx.fillText('✦',-7*sc,-40*sc+float);ctx.fillText('✦',7*sc,-38*sc+float);
    ctx.globalAlpha=1;
    // Arms with death orbs
    ctx.save();ctx.translate(13*sc,-32*sc+float);ctx.rotate(-Math.PI/3+as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.35+as*.6);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    // Death orb
    ctx.fillStyle='rgba(80,80,255,.85)';ctx.shadowColor='#4444ff';ctx.shadowBlur=18;
    ctx.beginPath();ctx.arc(0,14*sc,8*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(160,160,255,.6)';ctx.beginPath();ctx.arc(-2*sc,12*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.restore();
    ctx.save();ctx.translate(-13*sc,-32*sc+float);ctx.rotate(Math.PI/3-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.translate(0,16*sc);
    ctx.fillStyle='rgba(80,80,200,.6)';ctx.shadowColor='#4444ff';ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(0,0,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.restore();
    // Skull
    ctx.fillStyle='#d4c8a0';ctx.beginPath();ctx.arc(0,-56*sc+float,13*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#c4b888';ctx.fillRect(-9*sc,-48*sc+float,18*sc,7*sc);
    // Eye sockets with glow
    ctx.fillStyle='#111';
    ctx.beginPath();ctx.ellipse(-4.5*sc,-58*sc+float,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(4.5*sc,-58*sc+float,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(100,100,255,.95)';ctx.shadowColor='#6666ff';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(-4*sc,-58*sc+float,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-58*sc+float,2.5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Bone crown
    ctx.fillStyle='#c4b888';
    for(let i=-2;i<=2;i++) ctx.fillRect(i*5.5*sc-1.5*sc,-70*sc+float,3*sc,12*sc);
    ctx.fillStyle='rgba(100,100,255,.5)';ctx.shadowColor='#4444ff';ctx.shadowBlur=8;
    for(let i=-2;i<=2;i++) ctx.beginPath(),ctx.arc(i*5.5*sc,-70*sc+float,2.5*sc,0,Math.PI*2),ctx.fill();
    ctx.shadowBlur=0;
    // Nose hole
    ctx.fillStyle='rgba(0,0,0,.5)';ctx.beginPath();ctx.arc(0,-54*sc+float,2.5*sc,0,Math.PI*2);ctx.fill();
    // Jaw teeth
    ctx.fillStyle='#111';
    for(let t=-2;t<=2;t++) ctx.fillRect((t*2.8-1)*sc,-48*sc+float,2.5*sc,4*sc);
  },
};

// ══════════════════════════════════════════════════════
// CHARACTER CLASSES
// ══════════════════════════════════════════════════════
const PAL={
  skin1:'#f5c090',skin2:'#e8a870',skin3:'#c07840',
  hair1:'#1a0800',hair2:'#440000',hair3:'#ffd080',
};

const CLASSES={
  warrior:{name:'워리어',role:'근접 전사',icon:'⚔️',skinCol:PAL.skin1,hairCol:PAL.hair1,torsoCol:'#3a4455',legsCol:'#2a3344',headDeco:'helm',weapon:'sword',offhand:'shield',hp:380,mp:80,atk:42,def:16,spd:4.6,jmp:12.5,desc:'높은 HP·DEF. 방패방어+반격 특화.',stars:{ATK:4,DEF:5,SPD:3,RANGE:2,MAGIC:1},col:'#5588cc',
    skills:[
      {name:'검격',icon:'⚔️',key:'A',mp:10,cd:2,desc:'강력한 검 공격 1.8배',col:'#aabbcc',fn:(p,G)=>{hitAOE(p.x+(p.f>0?p.w:-75),p.y-15,80,70,dmg(p,1.8),true);spawnSlash(p.x+(p.f>0?p.w+30:-30),p.y+p.h*.3,'#aabbff',50);}},
      {name:'방패 강타',icon:'🛡️',key:'S',mp:18,cd:4,desc:'방패 충격 스턴+1.5배',col:'#8899aa',fn:(p,G)=>{p.vx=p.f*22;setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w:-80),p.y-5,80,60,dmg(p,1.5),true,{stun:110});spawnShockwave(p.x+(p.f>0?p.w+40:p.x-40),p.y+p.h*.5,'#8899aa',60);},130);}},
      {name:'돌격',icon:'💨',key:'D',mp:24,cd:5,desc:'돌진 후 강타 2.5배',col:'#ccdde0',fn:(p,G)=>{p.vx=p.f*40;p.invincible=38;setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w-10:-90),p.y-20,110,80,dmg(p,2.5),true);boom(p.x+(p.f>0?p.w+40:-40),p.y+10,'#aabbcc');shake(5,14);spawnSlash(p.x+(p.f>0?p.w+40:-40),p.y+p.h*.4,'#cce0ff',70);},200);}},
      {name:'회오리',icon:'🌀',key:'F',mp:38,cd:7,desc:'360도 광역 2.2배',col:'#99aabb',fn:(p,G)=>{hitAOE(p.x-75,p.y-45,p.w+150,p.h+90,dmg(p,2.2),false);shake(5,12);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#aabbcc',100);}},
      {name:'무적 베기',icon:'🗡️',key:'G',mp:65,cd:16,desc:'5초 무적+자힐+3.5배',col:'#eeffff',fn:(p,G)=>{p.invincible=300;p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.22));hitAOE(p.x-65,p.y-55,p.w+140,130,dmg(p,3.5),true);shake(9,24);for(let a=0;a<6;a++)spawnSlash(p.x+p.w/2-G.cam,p.y+p.h/2,a/6*Math.PI*2,'#eeffff',60);}},
    ]},
  mage:{name:'마법사',role:'원소 마법사',icon:'🔮',skinCol:PAL.skin3,hairCol:PAL.hair1,torsoCol:'#331155',legsCol:'#220f44',headDeco:'wizard-hat',weapon:'staff',offhand:'tome',hp:210,mp:280,atk:62,def:5,spd:4.0,jmp:12.0,desc:'강력한 마법. MP관리 필수.',stars:{ATK:5,DEF:1,SPD:3,RANGE:5,MAGIC:5},col:'#aa44ff',
    skills:[
      {name:'파이어볼',icon:'🔥',key:'A',mp:20,cd:1.5,desc:'화염탄 3발',col:'#ff6600',fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>proj(p.x+p.f*50,p.y+22,p.f*16,(Math.random()-.5)*.6,dmg(p,1.8),'#ff6600','player',{sz:14,emoji:'🔥',life:62,trail:true}),i*100);}},
      {name:'아이스 스피어',icon:'❄️',key:'S',mp:28,cd:4,desc:'빙결 마법구',col:'#44aaff',fn:(p,G)=>{proj(p.x+p.f*50,p.y+20,p.f*15,0,dmg(p,2.5),'#44aaff','player',{sz:15,emoji:'❄️',life:72,onHit:(e)=>{e.frozen=Math.max(e.frozen||0,200);spawnParts(e.x-G.cam+e.w/2,e.y+e.h/2,{n:15,col:['#44aaff','#aaddff'],glow:true,sMin:2,sMax:7});},glow:true});}},
      {name:'라이트닝',icon:'⚡',key:'D',mp:36,cd:5,desc:'낙뢰 3연격',col:'#ffee00',fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>{const tx=p.x+p.f*(140+i*100);proj(tx,-30,0,24,dmg(p,2.4),'#ffee00','player',{sz:20,emoji:'⚡',life:32,grav:.55});spawnParts(tx-G.cam,GY()-30,{n:12,col:['#ffee00','#ffcc44'],glow:true,spread:.5,dir:Math.PI*.5,sMin:4,sMax:12});shake(3,8);},i*180);}},
      {name:'메테오',icon:'☄️',key:'F',mp:72,cd:12,desc:'5개 운석 낙하 4배',col:'#ff4400',fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>{const tx=p.x+p.f*120+(Math.random()-.5)*300;proj(tx,-70,(Math.random()-.5)*2,18,dmg(p,4.0),'#ff4400','player',{sz:26,emoji:'☄️',life:78,grav:.32});shake(4,10);},i*165);}},
      {name:'타임스탑',icon:'⏰',key:'G',mp:90,cd:22,desc:'4초 전체 빙결',col:'#8844ff',fn:(p,G)=>{freezeAll(240);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#8844ff',200);spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2,{n:40,col:['#8844ff','#aabbff'],glow:true,sMin:3,sMax:10});}},
    ]},
  rogue:{name:'로그',role:'암살자',icon:'🗝️',skinCol:PAL.skin2,hairCol:PAL.hair1,torsoCol:'#1a2a1a',legsCol:'#111a11',headDeco:'hood',weapon:'dual',offhand:'dagger',hp:250,mp:190,atk:56,def:7,spd:5.8,jmp:15.5,desc:'초고속 이동, 크리+25%, 연속 참격.',stars:{ATK:5,DEF:1,SPD:5,RANGE:3,MAGIC:3},col:'#22cc55',
    skills:[
      {name:'3연참',icon:'🗡️',key:'A',mp:12,cd:1.5,desc:'초속 3연타 크리보정+',col:'#44ee66',fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w:-70),p.y-10,70,60,dmg(p,1.6),Math.random()<.35);spawnSlash(p.x+(p.f>0?p.w+20:-20),p.y+p.h*.35,'#44ee88',35+i*5);},i*105);}},
      {name:'수리검',icon:'✴️',key:'S',mp:20,cd:3,desc:'4방향 수리검',col:'#aaffaa',fn:(p,G)=>{[-6,-2,2,6].forEach(vy=>proj(p.x+p.f*50,p.y+27,p.f*20,vy,dmg(p,1.8),'#22dd44','player',{sz:10,emoji:'✴️',life:72}));}},
      {name:'순간이동',icon:'💨',key:'D',mp:18,cd:3.5,desc:'텔레포트+폭풍참격',col:'#aa44cc',fn:(p,G)=>{spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:18,col:['#22cc44','#88ff88'],grav:0,sMin:2,sMax:7,spread:Math.PI*2});p.x+=p.f*200;setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w:-95),p.y-22,105,85,dmg(p,2.8),true);for(let a=0;a<3;a++)spawnSlash(p.x+(p.f>0?p.w+20:p.x-20)-G.cam,p.y+p.h*.4,a*.6-.6,'#88ff88',40);},80);}},
      {name:'독 단검',icon:'☠️',key:'F',mp:35,cd:7,desc:'독 지속 피해',col:'#44cc44',fn:(p,G)=>{proj(p.x+p.f*50,p.y+24,p.f*18,-2,dmg(p,2.0),'#44cc44','player',{sz:13,emoji:'🗡️',life:82,onHit:(e)=>{e.poison=Math.max(e.poison||0,320);e.poisonDmg=Math.round(p.atk*.45);}});}},
      {name:'죽음의 무도',icon:'💀',key:'G',mp:80,cd:18,desc:'6방향 폭격+5초무적',col:'#222244',fn:(p,G)=>{p.invincible=300;for(let i=0;i<6;i++){const a=i/6*Math.PI*2;hitAOE(p.x+Math.cos(a)*85-50,p.y+Math.sin(a)*65-35,100,80,dmg(p,3.8),true);spawnSlash(p.x+Math.cos(a)*85-G.cam,p.y+Math.sin(a)*65,'#22ff88',55);}shake(14,35);}},
    ]},
  gunner:{name:'건너',role:'전술 사수',icon:'🔫',skinCol:PAL.skin1,hairCol:PAL.hair3,torsoCol:'#1a3322',legsCol:'#112211',headDeco:'cap',weapon:'gun',offhand:'quiver',hp:270,mp:170,atk:50,def:8,spd:5.2,jmp:14.0,desc:'연사 특화. 저격, 미사일, 탄막.',stars:{ATK:4,DEF:2,SPD:5,RANGE:5,MAGIC:2},col:'#44cc88',
    skills:[
      {name:'연사',icon:'🔫',key:'A',mp:12,cd:1.2,desc:'5연발',col:'#44cc88',fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>proj(p.x+p.f*56,p.y+26,p.f*24+(Math.random()-.5)*1.5,(Math.random()-.5)*1.5,dmg(p,1.0),'#44cc88','player',{sz:7,life:70}),i*50);}},
      {name:'유탄',icon:'💣',key:'S',mp:22,cd:4,desc:'폭발 유탄 광역',col:'#ffcc00',fn:(p,G)=>{proj(p.x+p.f*48,p.y+24,p.f*10,-9,dmg(p,3.2),'#ffcc00','player',{sz:18,emoji:'💣',life:92,grav:.4,explode:true});}},
      {name:'저격',icon:'🎯',key:'D',mp:30,cd:5.5,desc:'관통 저격 5배',col:'#88ff44',fn:(p,G)=>{proj(p.x+p.f*54,p.y+26,p.f*38,0,dmg(p,5.0),'#88ff44','player',{sz:11,life:115,pierce:true});shake(3,6);}},
      {name:'미사일',icon:'🚀',key:'F',mp:45,cd:9,desc:'5연 추적 미사일',col:'#ff8800',fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>proj(p.x+p.f*42,p.y+16+i*6,p.f*9+(Math.random()-.5)*3,-9+(Math.random()-.5)*3,dmg(p,2.3),'#ff8800','player',{sz:16,emoji:'🚀',life:105,grav:.05,homing:true}),i*95);}},
      {name:'탄막',icon:'🌟',key:'G',mp:85,cd:20,desc:'전방향 탄막 72발',col:'#44ffaa',fn:(p,G)=>{for(let i=0;i<18;i++)setTimeout(()=>{const a=i/18*Math.PI*2;proj(p.x+p.w/2,p.y+p.h/2,Math.cos(a)*18,Math.sin(a)*14,dmg(p,1.4),'#44ffaa','player',{sz:9,life:68,pierce:true});},i*55);shake(6,18);}},
    ]},
  berserker:{name:'버서커',role:'광전사',icon:'💢',skinCol:PAL.skin2,hairCol:PAL.hair2,torsoCol:'#4a1010',legsCol:'#3a0808',headDeco:'headband',weapon:'axe',offhand:'shield',hp:340,mp:60,atk:64,def:8,spd:5.0,jmp:13.0,desc:'ATK 극대화. HP↓ = ATK↑↑',stars:{ATK:5,DEF:3,SPD:4,RANGE:2,MAGIC:1},col:'#ff3322',
    skills:[
      {name:'분노 강타',icon:'💢',key:'A',mp:0,cd:2,desc:'2배+자신HP-8',col:'#ff4422',fn:(p,G)=>{const d=dmg(p,2.0+(1-p.hp/p.maxHp)*.8);p.hp=Math.max(1,p.hp-8);hitAOE(p.x+(p.f>0?p.w:-82),p.y-12,88,72,d,true);spawnSlash(p.x+(p.f>0?p.w+30:-30),p.y+p.h*.4,'#ff4422',55);}},
      {name:'피의 갈망',icon:'🩸',key:'S',mp:0,cd:5,desc:'1.8배+피흡50%',col:'#cc0000',fn:(p,G)=>{const d=dmg(p,1.8);hitAOE(p.x+(p.f>0?p.w:-80),p.y-10,80,70,d,false,{lifeSteal:.5});}},
      {name:'광란',icon:'🌋',key:'D',mp:20,cd:8,desc:'ATK+60%(5s)-HP20',col:'#ff8800',fn:(p,G)=>{p.hp=Math.max(1,p.hp-20);p.buffAtk=(p.buffAtk||1)*1.6;p.buffTimer=Math.max(p.buffTimer||0,300);shake(5,12);spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:20,col:['#ff4422','#ff8800'],glow:true,sMin:3,sMax:9});}},
      {name:'지진',icon:'💥',key:'F',mp:40,cd:9,desc:'전방 지진파 3.5배',col:'#cc2200',fn:(p,G)=>{setTimeout(()=>{hitAOE(p.x-80,p.y,240,GY()-p.y,dmg(p,3.5),true);boom(p.x,p.y+p.h,'#ff4422',2.5);shake(10,26);spawnShockwave(p.x+(p.f>0?p.w+60:-60)-G.cam,GY(),'#ff4422',140);},240);}},
      {name:'최후의 일격',icon:'🏴',key:'G',mp:0,cd:12,desc:'HP낮을수록 초강타5~13배',col:'#220000',fn:(p,G)=>{const mult=5+(1-p.hp/p.maxHp)*8;hitAOE(p.x+(p.f>0?p.w-10:-125),p.y-55,165,130,dmg(p,mult),true);boom(p.x+(p.f>0?p.w+40:-40),p.y,'#ff2200',3.5);shake(14,36);for(let a=0;a<8;a++)spawnSlash(p.x+p.w/2-G.cam,p.y+p.h/2,a/8*Math.PI*2,'#ff4422',60);}},
    ]},
  paladin:{name:'팔라딘',role:'성기사',icon:'✨',skinCol:PAL.skin1,hairCol:PAL.hair3,torsoCol:'#44556a',legsCol:'#334455',headDeco:'helm',weapon:'hammer',offhand:'shield',hp:520,mp:120,atk:36,def:28,spd:3.8,jmp:11.0,desc:'최고 생존력. 힐+재생+신성 폭발.',stars:{ATK:3,DEF:5,SPD:2,RANGE:2,MAGIC:4},col:'#eeddaa',
    skills:[
      {name:'망치 강타',icon:'🔨',key:'A',mp:12,cd:2,desc:'망치 1.8배+스턴',col:'#ccd0d4',fn:(p,G)=>{hitAOE(p.x+(p.f>0?p.w:-92),p.y-12,92,72,dmg(p,1.8),false,{stun:100});spawnShockwave(p.x+(p.f>0?p.w+40:-40)-G.cam,p.y+p.h*.7,'#ccd0d4',55);}},
      {name:'신성한 빛',icon:'💛',key:'S',mp:20,cd:4,desc:'HP 35% 회복',col:'#ffffaa',fn:(p,G)=>{const h=Math.round(p.maxHp*.35);p.hp=Math.min(p.maxHp,p.hp+h);spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:24,col:['#ffff88','#ffffff'],glow:true,upb:5,sMin:2,sMax:8});}},
      {name:'신성화',icon:'🔆',key:'D',mp:35,cd:7,desc:'광역 신성 피해',col:'#ffff88',fn:(p,G)=>{hitAll(dmg(p,1.6),true);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#ffff88',120);}},
      {name:'신성 방패',icon:'🌟',key:'F',mp:40,cd:9,desc:'4초 무적',col:'#aaddff',fn:(p,G)=>{p.invincible=240;spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:30,col:['#aaddff','#ffffff'],glow:true,sMin:3,sMax:9,grav:-.01});}},
      {name:'성광 폭발',icon:'💥',key:'G',mp:80,cd:16,desc:'전체 피해+자힐40%',col:'#ffffcc',fn:(p,G)=>{hitAll(dmg(p,2.8),true);p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.4));shake(11,28);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#ffffcc',180);}},
    ]},
  necromancer:{name:'네크로맨서',role:'소환사',icon:'💀',skinCol:'#c0c8d0',hairCol:'#000000',torsoCol:'#121820',legsCol:'#0a1018',headDeco:'crown',weapon:'scythe',offhand:'tome',hp:230,mp:260,atk:60,def:6,spd:4.2,jmp:12.5,desc:'암흑·소환. 저주로 적 약화.',stars:{ATK:5,DEF:1,SPD:3,RANGE:4,MAGIC:5},col:'#8833cc',
    skills:[
      {name:'암흑탄',icon:'💜',key:'A',mp:15,cd:2,desc:'암흑 마법 2.2배',col:'#8833cc',fn:(p,G)=>{proj(p.x+p.f*50,p.y+22,p.f*15,-1,dmg(p,2.2),'#8833cc','player',{sz:15,emoji:'🔮',life:68});}},
      {name:'생명 흡수',icon:'🖤',key:'S',mp:24,cd:4,desc:'피해+자힐20',col:'#440088',fn:(p,G)=>{proj(p.x+p.f*50,p.y+22,p.f*13,-1,dmg(p,1.6),'#440088','player',{sz:13,emoji:'🖤',life:62,onHit:(e)=>{p.hp=Math.min(p.maxHp,p.hp+24);spawnParts(e.x-G.cam+e.w/2,p.y+p.h/2,{n:8,col:['#440088','#880088'],glow:true});}});}},
      {name:'저주',icon:'⛧',key:'D',mp:30,cd:6,desc:'전체 적 ATK-40% 5초',col:'#332244',fn:(p,G)=>{for(const e of G.enemies) if(e.alive) e.cursed=Math.max(e.cursed||0,280);if(G.boss&&G.boss.alive) G.boss.cursed=Math.max(G.boss.cursed||0,280);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#8833cc',150);}},
      {name:'뼈 돌풍',icon:'🦴',key:'F',mp:50,cd:10,desc:'전체 광역 3배',col:'#ccbbaa',fn:(p,G)=>{hitAll(dmg(p,3.0),true);shake(7,16);}},
      {name:'죽음 폭발',icon:'☠️',key:'G',mp:90,cd:20,desc:'전체 6배 암흑 폭발',col:'#110022',fn:(p,G)=>{hitAll(dmg(p,6.0),true);shake(16,40);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#8833cc',250);}},
    ]},
  monk:{name:'몽크',role:'격투가',icon:'🥊',skinCol:PAL.skin1,hairCol:'#000000',torsoCol:'#cc8833',legsCol:'#aa6622',headDeco:'goggles',weapon:'dual',offhand:'dagger',hp:300,mp:150,atk:48,def:12,spd:6.2,jmp:16.0,desc:'초고속 연타. 기(氣) 스킬 특화.',stars:{ATK:4,DEF:3,SPD:5,RANGE:3,MAGIC:3},col:'#ffaa22',
    skills:[
      {name:'연타',icon:'🥊',key:'A',mp:10,cd:1.5,desc:'5연속 타격',col:'#ffaa22',fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w:-68),p.y-12,72,64,dmg(p,.75),i===4);if(i%2===0)spawnSlash(p.x+(p.f>0?p.w+15:-15),p.y+p.h*.4,'#ffaa22',30);},i*95);}},
      {name:'기공파',icon:'🌀',key:'S',mp:20,cd:3,desc:'기 에너지 2.8배',col:'#ffcc44',fn:(p,G)=>{proj(p.x+p.f*50,p.y+22,p.f*17,0,dmg(p,2.8),'#ffcc44','player',{sz:18,emoji:'🌀',life:72,trail:true});}},
      {name:'철갑',icon:'⛓️',key:'D',mp:15,cd:6,desc:'DEF+12 4초',col:'#888888',fn:(p,G)=>{p.defBuff=12;p.defBuffTimer=240;spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:18,col:['#888888','#aaaaaa'],sMin:2,sMax:6});}},
      {name:'회오리',icon:'🌪️',key:'F',mp:35,cd:7,desc:'360도 4배',col:'#88ccff',fn:(p,G)=>{hitAOE(p.x-85,p.y-55,p.w+170,p.h+110,dmg(p,4.0),true);shake(6,14);spawnShockwave(p.x+p.w/2-G.cam,p.y+p.h/2,'#88ccff',100);}},
      {name:'내면의 평화',icon:'☮️',key:'G',mp:0,cd:10,desc:'HP50%+MP30 회복',col:'#ffffcc',fn:(p,G)=>{p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.5));p.mp=Math.min(p.maxMp,p.mp+30);spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:24,col:['#ffffcc','#ffffff'],glow:true,upb:3,sMin:2,sMax:7});}},
    ]},
};

// ══════════════════════════════════════════════════════
// STAGE DATA — WITH FULL BG THEMING
// ══════════════════════════════════════════════════════
const STAGES=[
  {name:'어둠의 동굴',bg:'#06040e',fl:'#100820',wall:'#0d0618',
   skyTop:'#08050f',skyBot:'#120820',
   archDark:'#04020a',archCol:'#1a0d2a',
   pilDark:'#0d0618',pilMid:'#160a22',
   fogCol:'rgba(80,20,120,.4)',runeCol:'#8833cc',
   torchInner:'#fff5dd',torchOuter:'#ff8800',torchGlow:'rgba(255,120,0,.2)',
   ceilDark:'#0a0614',ceilMid:'#120822',stalCol:'#0a0416',dripCol:'rgba(80,0,150,.5)',
   floorTop:'#100820',floorMid:'#0c0618',floorDark:'#08040e',floorLine:'rgba(120,60,200,.3)',floorTile:'#ffffff',
   plTop:'#180c28',plBot:'#0e0618',
   ambCol:'rgba(60,0,120,.07)',torch:'#ff6600',
   enemySet:['goblin','skeleton','zombie'],count:7,
   boss:{name:'슬라임 대왕',drawType:'golem',hp:900,atk:28,spd:2.2,bodyCol:'#226622',headCol:'#337733',limbCol:'#115511',drawScale:1.6}},

  {name:'용암 던전',bg:'#120400',fl:'#220900',wall:'#1a0500',
   skyTop:'#160300',skyBot:'#240800',
   archDark:'#0e0200',archCol:'#2a0800',
   pilDark:'#1a0300',pilMid:'#2e0800',
   fogCol:'rgba(200,60,0,.35)',runeCol:'#ff4400',
   torchInner:'#ffffff',torchOuter:'#ff2200',torchGlow:'rgba(255,80,0,.25)',
   ceilDark:'#140200',ceilMid:'#200600',stalCol:'#200400',dripCol:'rgba(200,40,0,.5)',
   floorTop:'#220900',floorMid:'#1a0600',floorDark:'#120200',floorLine:'rgba(255,80,0,.4)',floorTile:'#ff4400',
   plTop:'#2e0800',plBot:'#180300',
   ambCol:'rgba(200,50,0,.06)',torch:'#ff4400',
   enemySet:['goblin','orc','zombie','demon'],count:9,
   boss:{name:'불꽃 골렘',drawType:'golem',hp:1400,atk:36,spd:2.0,bodyCol:'#662200',headCol:'#883300',limbCol:'#441100',drawScale:1.7}},

  {name:'얼음 궁전',bg:'#040820',fl:'#081430',wall:'#060e22',
   skyTop:'#030614',skyBot:'#080e2a',
   archDark:'#020410',archCol:'#0a1430',
   pilDark:'#060e1e',pilMid:'#0e1a30',
   fogCol:'rgba(0,100,200,.35)',runeCol:'#44aaff',
   torchInner:'#e0f8ff',torchOuter:'#44aaff',torchGlow:'rgba(0,100,255,.2)',
   ceilDark:'#040818',ceilMid:'#080e24',stalCol:'#060c1e',dripCol:'rgba(0,100,200,.5)',
   floorTop:'#081430',floorMid:'#060e22',floorDark:'#040818',floorLine:'rgba(100,200,255,.35)',floorTile:'#44aaff',
   plTop:'#0e1a30',plBot:'#060c1a',
   ambCol:'rgba(0,80,200,.08)',torch:'#44aaff',
   enemySet:['orc','skeleton','mage_e','wolf'],count:11,
   boss:{name:'빙결 드래곤',drawType:'dragon',hp:1900,atk:44,spd:2.7,bodyCol:'#224466',headCol:'#336688',limbCol:'#112244',drawScale:1.5}},

  {name:'독 늪지',bg:'#040e04',fl:'#081208',wall:'#060e06',
   skyTop:'#030a02',skyBot:'#070e05',
   archDark:'#020802',archCol:'#0a1408',
   pilDark:'#060c04',pilMid:'#0e1808',
   fogCol:'rgba(0,160,0,.3)',runeCol:'#44cc00',
   torchInner:'#efffcc',torchOuter:'#44cc00',torchGlow:'rgba(0,160,0,.2)',
   ceilDark:'#030802',ceilMid:'#070c04',stalCol:'#050a03',dripCol:'rgba(0,120,0,.5)',
   floorTop:'#081208',floorMid:'#060e06',floorDark:'#040a04',floorLine:'rgba(60,200,0,.35)',floorTile:'#44cc00',
   plTop:'#0e1a08',plBot:'#060c04',
   ambCol:'rgba(0,150,0,.07)',torch:'#44cc00',
   enemySet:['zombie','mage_e','lich','demon'],count:13,
   boss:{name:'늪 히드라',drawType:'dragon',hp:2600,atk:52,spd:3.0,bodyCol:'#225522',headCol:'#337733',limbCol:'#113311',drawScale:1.6}},

  {name:'마왕의 성',bg:'#080010',fl:'#120018',wall:'#0e0014',
   skyTop:'#050008',skyBot:'#0c0018',
   archDark:'#030006',archCol:'#160028',
   pilDark:'#0c0010',pilMid:'#180020',
   fogCol:'rgba(150,0,200,.35)',runeCol:'#aa00ff',
   torchInner:'#ffccff',torchOuter:'#aa00ff',torchGlow:'rgba(150,0,200,.25)',
   ceilDark:'#060010',ceilMid:'#0c0018',stalCol:'#0a000e',dripCol:'rgba(120,0,200,.5)',
   floorTop:'#120018',floorMid:'#0e0010',floorDark:'#08000c',floorLine:'rgba(180,0,255,.4)',floorTile:'#aa00ff',
   plTop:'#180020',plBot:'#0c0014',
   ambCol:'rgba(150,0,200,.1)',torch:'#aa00ff',
   enemySet:['demon','lich','dragon','golem'],count:16,
   boss:{name:'마왕 DARKOS',drawType:'lich',hp:3500,atk:68,spd:3.2,bodyCol:'#220033',headCol:'#330055',limbCol:'#110022',drawScale:2.0}},
];

// ══════════════════════════════════════════════════════
// ENEMY TYPES
// ══════════════════════════════════════════════════════
const ENEMIES={
  goblin:  {name:'고블린',   drawType:'goblin',     w:34,h:40,hp:80, atk:12,spd:3.2,xp:14,g:8, bodyCol:'#33aa44',headCol:'#22aa33',limbCol:'#22aa44',drawScale:.95,ai:'chase'},
  orc:     {name:'오크',     drawType:'orc',        w:54,h:64,hp:220,atk:25,spd:2.0,xp:30,g:18,bodyCol:'#3a5a2a',headCol:'#4a6a3a',limbCol:'#2a4a1a',drawScale:1.3,ai:'brute'},
  skeleton:{name:'스켈레톤', drawType:'skeleton',   w:40,h:54,hp:130,atk:18,spd:3.2,xp:22,g:14,bodyCol:'#d4c8a0',headCol:'#d4c8a0',limbCol:'#c4b888',drawScale:1.0,ai:'normal'},
  zombie:  {name:'좀비',     drawType:'zombie',     w:42,h:56,hp:160,atk:16,spd:1.7,xp:26,g:15,bodyCol:'#3d5a30',headCol:'#4d5a38',limbCol:'#2d4a22',drawScale:1.0,ai:'slow'},
  mage_e:  {name:'마법사',   drawType:'mage_enemy', w:36,h:58,hp:115,atk:30,spd:2.6,xp:34,g:24,bodyCol:'#2a1a4a',headCol:'#3a2a6a',limbCol:'#3a2a5a',drawScale:.95,ai:'ranged'},
  demon:   {name:'데몬',     drawType:'demon',      w:50,h:68,hp:200,atk:27,spd:2.8,xp:48,g:32,bodyCol:'#4a0a0a',headCol:'#550a0a',limbCol:'#3a0808',drawScale:1.1,ai:'chase'},
  dragon:  {name:'드래고니언',drawType:'dragon',    w:62,h:74,hp:280,atk:32,spd:2.3,xp:58,g:40,bodyCol:'#1a3a1a',headCol:'#1a4a1a',limbCol:'#2a5a2a',drawScale:1.3,ai:'brute'},
  golem:   {name:'골렘',     drawType:'golem',      w:70,h:78,hp:400,atk:36,spd:1.4,xp:70,g:50,bodyCol:'#6a5a4a',headCol:'#8a7a6a',limbCol:'#7a6a5a',drawScale:1.4,ai:'tank'},
  lich:    {name:'리치',     drawType:'lich',       w:46,h:66,hp:170,atk:34,spd:2.4,xp:55,g:38,bodyCol:'#1a1a3a',headCol:'#222240',limbCol:'#2a2a4a',drawScale:1.1,ai:'ranged'},
  wolf:    {name:'다크 울프',drawType:'goblin',     w:44,h:38,hp:110,atk:20,spd:4.0,xp:18,g:12,bodyCol:'#334',   headCol:'#445',   limbCol:'#223',   drawScale:1.0,ai:'chase'},
};

// ══════════════════════════════════════════════════════
// SHOP ITEMS
// ══════════════════════════════════════════════════════
const SHOP_ITEMS=[
  {name:'소형 HP 포션',icon:'🧪',desc:'HP +20%',price:60, fn:(p)=>{const h=Math.round(p.maxHp*.2);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'대형 HP 포션',icon:'⚗️', desc:'HP +55%',price:160,fn:(p)=>{const h=Math.round(p.maxHp*.55);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'마나 포션',   icon:'💙', desc:'MP +50%',price:80, fn:(p)=>{const m=Math.round(p.maxMp*.5);p.mp=Math.min(p.maxMp,p.mp+m);return `MP +${m}`;}},
  {name:'강화 무기',   icon:'⚔️', desc:'ATK +20',price:200,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+20;return 'ATK +20';},rarity:1},
  {name:'불꽃 검',     icon:'🔥', desc:'ATK +38',price:380,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+38;return 'ATK +38';},rarity:2},
  {name:'강화 갑옷',   icon:'🛡️', desc:'DEF+14 HP+45',price:220,fn:(p)=>{p.defBonus=(p.defBonus||0)+14;p.maxHp+=45;p.hp=Math.min(p.maxHp,p.hp+45);return 'DEF+14 HP+45';},rarity:1},
  {name:'마법 갑옷',   icon:'💎', desc:'DEF+24 HP+90',price:400,fn:(p)=>{p.defBonus=(p.defBonus||0)+24;p.maxHp+=90;p.hp=Math.min(p.maxHp,p.hp+90);return 'DEF+24 HP+90';},rarity:2},
  {name:'스피드 링',   icon:'💍', desc:'SPD +1.2',price:180,fn:(p)=>{p.spdBonus=(p.spdBonus||0)+1.2;return 'SPD +1.2';},rarity:1},
  {name:'크리티컬 반지',icon:'🔮',desc:'CRIT +20%',price:300,fn:(p)=>{p.critBonus=(p.critBonus||0)+.20;return 'CRIT +20%';},rarity:2},
  {name:'전설의 반지', icon:'⭐', desc:'ATK+28 CRIT+28%',price:650,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+28;p.critBonus=(p.critBonus||0)+.28;return 'ATK+28 CRIT+28%';},rarity:4},
];
const RARITY_COL=['#aaaaaa','#44cc44','#4488ff','#cc44ff','#ffcc00'];

// ══════════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════════
let G=null, RAF=null;
let selCharId=null;
const GRAVITY=0.55;
const STAGE_W=5600;

function mkPlayer(clsId){
  const c=CLASSES[clsId];
  return {
    ...c,clsId,
    x:140,y:GY()-65,vx:0,vy:0,f:1,
    onGround:false,jumpCount:0,
    hp:c.hp,maxHp:c.hp,
    mp:c.mp,maxMp:c.mp,
    alive:true,invincible:0,
    skillCds:c.skills.map(()=>0),
    buffAtk:1,buffSpd:1,buffTimer:0,
    kills:0,score:0,gold:0,level:1,xp:0,xpNext:100,
    combo:0,comboTimer:0,maxCombo:0,
    atkCd:0,atkAnim:0,hitFlash:0,dodgeCd:0,dodgeAnim:0,
    w:44,h:62,
    atkBonus:0,defBonus:0,spdBonus:0,critBonus:0,defBuff:0,defBuffTimer:0,
    walkPhase:0,atkPhase:0,
    state:'idle',
    equip:{wpn:null,arm:null,acc:null},
    statusEffects:{},
  };
}

function initGame(clsId, stageIdx){
  const p=mkPlayer(clsId);
  const stage=STAGES[stageIdx];
  G={
    clsId,stageIdx,stage,player:p,
    enemies:[],boss:null,bossSpawned:false,bossKills:0,
    projectiles:[],items:[],cam:0,phase:'play',timer:0,
    startTime:Date.now(),platforms:genPlats(stage),
    shakeAmt:0,shakeTimer:0,hitStop:0,stageDmgTaken:0,paused:false,bgOff:0,
    shopStock:[],pendingLvlUp:false,
  };
  PARTS.length=0;SLASHES.length=0;SHOCKWAVES.length=0;
  spawnEnemies();
  updateEquipUI();
}

function genPlats(stage){
  const arr=[];
  for(let i=0;i<13;i++){
    arr.push({
      x:260+i*340+(Math.random()-.5)*100,
      y:GY()-85-Math.random()*130,
      w:70+Math.random()*90,h:14,
    });
  }
  return arr;
}

function spawnEnemies(){
  const st=G.stage;
  for(let i=0;i<st.count;i++){
    const tid=st.enemySet[Math.floor(Math.random()*st.enemySet.length)];
    const et={...ENEMIES[tid]};
    const sc=1+(G.stageIdx*.25);
    const ex=620+i*320+Math.random()*120;
    G.enemies.push({
      ...et,uid:'e'+i+Date.now(),
      x:ex,y:GY()-et.h,
      hp:Math.round(et.hp*sc),maxHp:Math.round(et.hp*sc),
      atk:Math.round(et.atk*sc),
      vx:0,vy:0,f:-1,alive:true,dying:false,deathTimer:30,
      atkTimer:65+Math.random()*85,
      frozen:0,stun:0,poison:0,poisonDmg:0,poisonTimer:0,burn:0,cursed:0,
      hitFlash:0,walkPhase:Math.random()*Math.PI*2,atkPhase:0,aggro:false,
    });
  }
}

function spawnBoss(){
  const bd={...G.stage.boss};
  const sc=1+(G.stageIdx*.3);
  G.boss={
    ...bd,...ENEMIES[bd.drawType]||ENEMIES.golem,
    name:bd.name,drawType:bd.drawType,
    bodyCol:bd.bodyCol,headCol:bd.headCol,limbCol:bd.limbCol,drawScale:bd.drawScale,
    x:STAGE_W-540,y:GY()-95,
    hp:Math.round(bd.hp*sc),maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc),spd:bd.spd+G.stageIdx*.1,
    w:74,h:92,alive:true,dying:false,
    frozen:0,stun:0,cursed:0,atkTimer:80,projTimer:110,phase2:false,phase3:false,
    hitFlash:0,walkPhase:0,atkPhase:0,
  };
  document.getElementById('boss-bar').classList.add('show');
  document.getElementById('boss-name-lbl').textContent='⚠ '+bd.name;
  const bw=document.getElementById('boss-warn');
  bw.style.display='block';bw.textContent='⚠ BOSS ⚠\n'+bd.name;
  setTimeout(()=>bw.style.display='none',2400);
  shake(14,45);sfx_bossIn();
}

// ══════════════════════════════════════════════════════
// COMBAT HELPERS
// ══════════════════════════════════════════════════════
function totalAtk(p){return (p.atk+(p.atkBonus||0))*(p.buffAtk||1);}
function totalDef(p){return (p.def+(p.defBonus||0))+(p.defBuff||0);}
function totalCrit(p){return .1+(p.critBonus||0);}
function totalSpd(p){return (p.spd+(p.spdBonus||0))*(p.buffSpd||1);}

function dmg(p,mult){
  const atk=totalAtk(p);
  const isCrit=Math.random()<totalCrit(p);
  const v=Math.round((atk*mult+Math.random()*6-3)*(isCrit?2.2:1));
  return {v:Math.max(1,v),crit:isCrit};
}

function hitAOE(ax,ay,aw,ah,d,showCrit,opts={}){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  for(const e of targets){
    if(!e.alive) continue;
    if(ax<e.x+e.w&&ax+aw>e.x&&ay<e.y+e.h&&ay+ah>e.y){
      dealDmg(e,d.v,d.crit||showCrit,opts);
      // Knockback
      e.vx=(e.x<ax+aw/2?-1:1)*12;
      e.vy=-4;
    }
  }
}

function hitAll(d,showCrit){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  for(const e of targets) if(e.alive){dealDmg(e,d.v,d.crit||showCrit,{});e.vx=(Math.random()-.5)*16;e.vy=-5;}
}

function dealDmg(e,v,crit,opts){
  if(!e.alive) return;
  const p=G.player;
  if(e.cursed>0) v=Math.round(v*1.45);
  e.hp-=v;e.hitFlash=10;
  if(opts.stun) e.stun=Math.max(e.stun||0,opts.stun);
  if(opts.lifeSteal) p.hp=Math.min(p.maxHp,p.hp+Math.round(v*opts.lifeSteal));
  if(opts.onHit) opts.onHit(e);
  const sx=e.x-G.cam+e.w/2,sy=e.y;
  showDNum(sx,sy,v,crit,p.col||'#fff');
  G.hitStop=crit?6:3;
  if(e.hp<=0) killE(e);
}

function killE(e){
  e.alive=false;e.dying=true;e.deathTimer=32;
  const p=G.player;
  if(e===G.boss){
    p.xp+=700;p.gold+=400;p.score+=8000;
    G.bossKills++;
    document.getElementById('boss-bar').classList.remove('show');
    spawnParts(e.x-G.cam+e.w/2,e.y+e.h/2,{n:70,col:['#ffcc00','#ff6600','#ffffff'],glow:true,sMin:3,sMax:16,type:'c'});
    shake(16,60);sfx_clear();checkLvlUp(p);
    setTimeout(()=>stageClear(),1200);
  } else {
    p.kills++;p.xp+=e.xp;p.gold+=e.g;p.score+=e.xp*2;
    spawnParts(e.x-G.cam+e.w/2,e.y+e.h/2,{n:16,col:[e.bodyCol||'#556','#ffcc00'],sMin:2,sMax:7});
    checkLvlUp(p);tryDrop(e);
  }
}

function checkLvlUp(p){
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext;p.level++;p.xpNext=Math.round(p.xpNext*1.55);
    p.maxHp+=30;p.hp=Math.min(p.maxHp,p.hp+50);
    p.maxMp+=10;p.mp=Math.min(p.maxMp,p.mp+20);
    p.atk+=4;p.def+=2;
    G.pendingLvlUp=true;showLvlUpModal();sfx_lvl();
  }
}

function tryDrop(e){
  if(Math.random()>.38) return;
  const pool=SHOP_ITEMS.filter(i=>i.fn);
  const it={...pool[Math.floor(Math.random()*pool.length)],uid:'d'+Date.now()+Math.random(),x:e.x+e.w/2-14,y:e.y,vy:-8,alive:true};
  G.items.push(it);
}

function freezeAll(dur){
  if(!G) return;
  for(const e of G.enemies) if(e.alive) e.frozen=Math.max(e.frozen||0,dur);
  if(G.boss&&G.boss.alive) G.boss.frozen=Math.max(G.boss.frozen||0,dur);
}

function proj(x,y,vx,vy,d,col,owner,opts={}){
  if(!G) return;
  G.projectiles.push({
    x,y,vx,vy,dmg:d.v,crit:d.crit,col,owner,alive:true,
    life:opts.life||80,sz:opts.sz||8,
    pierce:opts.pierce||false,grav:opts.grav!==undefined?opts.grav:0,
    emoji:opts.emoji||null,trail:opts.trail||false,
    homing:opts.homing||false,explode:opts.explode||false,
    onHit:opts.onHit||null,glow:opts.glow||false,
    uid:'p'+Date.now()+Math.random(),
  });
}

function boom(wx,wy,col,scale=1.5){
  spawnParts(wx,wy,{n:Math.round(26*scale),col:[col,'#ffffff','#ffcc00'],glow:true,sMin:3*scale,sMax:8*scale,upb:2});
  spawnParts(wx,wy,{n:Math.round(12*scale),col:[col,'#ff4400'],type:'sq',sMin:2*scale,sMax:5*scale});
  spawnShockwave(wx,wy,col,80*scale);
}

function shake(amt,dur){
  if(!G) return;
  G.shakeAmt=Math.max(G.shakeAmt,amt);G.shakeTimer=Math.max(G.shakeTimer,dur);
}

// ══════════════════════════════════════════════════════
// GAME LOOP
// ══════════════════════════════════════════════════════
let lastTs=0;
function loop(ts){
  const dt=Math.min((ts-lastTs)/16.67,3);
  lastTs=ts;
  if(G&&G.phase==='play'&&!G.paused&&!G.pendingLvlUp){
    gameUpdate(dt);
  }
  gameRender();
  updateHUD();
  flushJK();
  RAF=requestAnimationFrame(loop);
}

function gameUpdate(dt){
  G.timer++;
  G.bgOff=(G.bgOff+.35*dt)%800;
  const p=G.player;
  if(!p.alive) return;
  if(G.hitStop>0){G.hitStop-=dt;return;}

  handleInput(p,dt);
  updatePlayer(p,dt);
  updateEnemies(dt);
  if(G.boss&&G.boss.alive) updateBoss(dt);
  updateProjs(dt);
  updateItems(dt);
  updateParts(dt);
  updateSlashes(dt);
  updateShockwaves(dt);

  if(G.shakeTimer>0) G.shakeTimer-=dt;
  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){G.bossSpawned=true;spawnBoss();}
  if(G.timer%72===0) p.mp=Math.min(p.maxMp,p.mp+3);
  if(p.clsId==='paladin'&&G.timer%90===0) p.hp=Math.min(p.maxHp,p.hp+Math.ceil(p.maxHp*.015));
  if(p.defBuffTimer>0){p.defBuffTimer-=dt;if(p.defBuffTimer<=0)p.defBuff=0;}
  if(p.buffTimer>0){p.buffTimer-=dt;if(p.buffTimer<=0){p.buffAtk=1;p.buffSpd=1;}}
}

function handleInput(p,dt){
  if(!p.alive) return;
  const spd=totalSpd(p);
  const wasMoving=Math.abs(p.vx)>0.3;
  let moving=false;

  if(KEY['ArrowLeft']){p.vx=-spd*6*dt;p.f=-1;moving=true;}
  if(KEY['ArrowRight']){p.vx=spd*6*dt;p.f=1;moving=true;}

  // Update state
  if(!p.onGround) p.state='jump';
  else if(p.atkAnim>0) p.state='atk';
  else if(moving&&Math.abs(p.vx)>spd*3) p.state='run';
  else if(moving) p.state='walk';
  else p.state='idle';

  if((JK['z']||JK['Z'])&&p.jumpCount<2){
    p.vy=-p.jmp;p.jumpCount++;
    spawnParts(p.x-G.cam+p.w/2,p.y+p.h,{n:10,col:['#fff','#ccc'],upb:3,sMin:2,sMax:5,spread:.8});
    sfx_jump();
  }

  if((JK['x']||JK['X'])&&p.atkCd<=0) doAttack(p);

  if(JK[' ']&&p.dodgeCd<=0){
    p.vx=p.f*26;p.vy=-2;p.invincible=44;p.dodgeCd=54;p.dodgeAnim=24;
    spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:16,col:[p.col||'#fff','rgba(255,255,255,.5)'],spread:Math.PI*.5,dir:Math.PI,upb:0,sMin:2,sMax:6,grav:.04});
    sfx_dodge();
  }

  const skMap={a:0,s:1,d:2,f:3,g:4,A:0,S:1,D:2,F:3,G:4};
  for(const [k,idx] of Object.entries(skMap)){
    if(JK[k]&&p.skills[idx]!==undefined){useSkill(p,idx);break;}
  }
  if(JK['p']||JK['P']){
    G.paused=!G.paused;
    document.getElementById('pause-ov').classList.toggle('hidden',!G.paused);
  }
}

function doAttack(p){
  p.atkCd=15;p.atkAnim=16;p.atkPhase=Math.PI*.6;p.state='atk';
  p.combo=Math.min(10,(p.combo||0)+1);p.comboTimer=88;
  if(p.combo>G.maxCombo) G.maxCombo=p.combo;
  const cdel=document.getElementById('combo-display');
  document.getElementById('combo-num').textContent=p.combo+'HIT';
  cdel.style.opacity=p.combo>=2?'1':'0';

  const mult=1+p.combo*.12;
  const d=dmg(p,mult);
  hitAOE(p.x+(p.f>0?p.w:-72),p.y-14,74,64,d,false);

  // Slash effect
  const ex=p.x+(p.f>0?p.w+24:-24);
  spawnSlash(ex-G.cam,p.y+p.h*.35,p.f>0?0:Math.PI,52+p.combo*3,d.crit?'#ffff88':p.col||'#fff',14);
  spawnParts(ex-G.cam,p.y+p.h*.4,{n:d.crit?18:9,col:[p.col||'#fff','#ffcc00'],spread:.7,dir:p.f>0?0:Math.PI,sMin:2,sMax:d.crit?9:6,glow:d.crit,type:d.crit?'sq':'c'});
  if(d.crit){shake(3,6);spawnShockwave(ex-G.cam,p.y+p.h*.35,p.col||'#fff',40);}
}

function useSkill(p,idx){
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;p.skillCds[idx]=sk.cd*60;p.atkPhase=Math.PI*.9;p.state='skill';
  sk.fn(p,G);
}

function updatePlayer(p,dt){
  p.vy+=GRAVITY*dt;p.x+=p.vx*dt;p.y+=p.vy*dt;p.vx*=.83;
  const gy=GY();
  if(p.y+p.h>=gy){p.y=gy-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;}
  else p.onGround=false;
  for(const pl of G.platforms){
    if(p.vy>=0&&p.x+p.w>pl.x&&p.x<pl.x+pl.w&&p.y+p.h>pl.y&&p.y+p.h<pl.y+pl.h+15){
      p.y=pl.y-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;
    }
  }
  p.x=Math.max(5,Math.min(STAGE_W-p.w-5,p.x));
  if(p.y>gy+150){p.y=gy-p.h;p.vy=0;}

  G.cam+=(p.x-W()*.35-G.cam)*.09*dt;
  G.cam=Math.max(0,Math.min(STAGE_W-W(),G.cam));

  // Walk phase - speed-dependent
  const spd=totalSpd(p);
  if(Math.abs(p.vx)>0.5&&p.onGround) p.walkPhase+=.24*dt*Math.min(1,Math.abs(p.vx)/(spd*4))*3;
  else if(p.onGround) p.walkPhase=Math.round(p.walkPhase/Math.PI)*Math.PI;
  p.atkPhase=Math.max(0,p.atkPhase-.14*dt);

  if(p.invincible>0) p.invincible-=dt;
  if(p.atkCd>0) p.atkCd-=dt;
  if(p.atkAnim>0){p.atkAnim-=dt;if(p.atkAnim<=0&&p.state==='atk')p.state='idle';}
  if(p.hitFlash>0) p.hitFlash-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeAnim>0) p.dodgeAnim-=dt;
  if(p.comboTimer>0){p.comboTimer-=dt;if(p.comboTimer<=0){p.combo=0;document.getElementById('combo-display').style.opacity='0';}}
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;
}

function updateEnemies(dt){
  const p=G.player;const gy=GY();
  for(const e of G.enemies){
    if(!e.alive){if(e.dying){e.deathTimer-=dt;}continue;}
    if(e.hitFlash>0) e.hitFlash-=dt;
    if(e.frozen>0){e.frozen-=dt;e.walkPhase=0;continue;}
    if(e.stun>0){e.stun-=dt;continue;}
    if(e.cursed>0) e.cursed-=dt;
    if(e.poison>0){
      e.poison-=dt;
      if(!e.poisonTimer||e.poisonTimer<=0){e.hp-=e.poisonDmg||5;e.poisonTimer=22;if(e.hp<=0){killE(e);continue;}}
      e.poisonTimer-=dt;
    }
    const dx=p.x-e.x;
    if(Math.abs(dx)<440) e.aggro=true;
    if(!e.aggro) continue;
    e.f=dx>0?1:-1;
    const sm=e.cursed>0?.58:1;
    const spd=(e.spd||2)*sm;
    const dist=Math.abs(dx);

    switch(e.ai){
      case 'chase': if(dist>50) e.vx=e.f*spd*.9; break;
      case 'brute': if(dist>55) e.vx=e.f*spd*.85; break;
      case 'slow':  if(dist>60) e.vx=e.f*spd*.6; break;
      case 'tank':  if(dist>65) e.vx=e.f*spd*.55; break;
      case 'ranged':
        if(dist<200) e.vx=-e.f*spd*.65;
        else if(dist>330) e.vx=e.f*spd*.65;
        else e.vx*=.8;
        break;
      default: if(dist>50) e.vx=e.f*spd*.9; break;
    }

    e.vx*=.85;
    e.vy=(e.vy||0)+GRAVITY*dt*.55;e.x+=e.vx*dt;e.y+=e.vy*dt;
    if(e.y+e.h>=gy){e.y=gy-e.h;e.vy=0;}
    for(const pl of G.platforms){
      if(e.vy>=0&&e.x+e.w>pl.x&&e.x<pl.x+pl.w&&e.y+e.h>pl.y&&e.y+e.h<pl.y+pl.h+13){e.y=pl.y-e.h;e.vy=0;}
    }
    e.x=Math.max(10,Math.min(STAGE_W-e.w-10,e.x));

    if(Math.abs(e.vx)>0.3) e.walkPhase+=.18*dt;
    e.atkPhase=Math.max(0,e.atkPhase-.12*dt);
    e.atkTimer-=dt;

    if(e.atkTimer<=0&&e.aggro){
      if(e.ai==='ranged'){
        if(dist<370){
          e.atkTimer=98+Math.random()*58;
          const vd=dmg({atk:e.atk,atkBonus:0,buffAtk:1,critBonus:0},1);
          proj(e.x+e.w/2,e.y+e.h*.45,e.f*12+(Math.random()-.5)*1,(Math.random()-.5)*2,vd,'#aa44ff','enemy',{sz:10,life:82});
          e.atkPhase=Math.PI*.8;
        }
      } else {
        if(dist<65&&Math.abs(p.y-e.y)<68){
          e.atkTimer=78+Math.random()*38;e.atkPhase=Math.PI;
          if(p.dodgeAnim<=0){
            const rawDmg=Math.max(1,e.atk-Math.round(totalDef(p)*.55)+Math.floor(Math.random()*6)-3);
            takeDmg(rawDmg);
          }
        }
      }
    }
  }
}

function updateBoss(dt){
  const b=G.boss,p=G.player;
  if(!b.alive) return;
  if(b.hitFlash>0) b.hitFlash-=dt;
  if(b.frozen>0){b.frozen-=dt;return;}
  if(b.stun>0){b.stun-=dt;return;}
  if(b.cursed>0) b.cursed-=dt;

  const hpPct=b.hp/b.maxHp;
  if(!b.phase2&&hpPct<.55){
    b.phase2=true;b.spd*=1.38;b.atk=Math.round(b.atk*1.3);
    document.getElementById('boss-phase-txt').textContent='⚡ PHASE 2';
    shake(14,44);spawnParts(b.x-G.cam+b.w/2,b.y+b.h/2,{n:55,col:['#ff4400','#ff8800'],glow:true,sMin:4,sMax:14});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true;b.spd*=1.32;b.atk=Math.round(b.atk*1.28);
    document.getElementById('boss-phase-txt').textContent='💀 PHASE 3 ENRAGE';
    shake(20,65);spawnParts(b.x-G.cam+b.w/2,b.y+b.h/2,{n:90,col:['#ff0000','#cc00ff','#ffffff'],glow:true,sMin:5,sMax:18});sfx_bossIn();
  }

  const dx=p.x-b.x;b.f=dx>0?1:-1;
  if(Math.abs(dx)>100) b.x+=b.f*b.spd*dt*.9;
  b.vy=(b.vy||0)+GRAVITY*dt*.45;b.y+=b.vy*dt;
  const gy=GY();
  if(b.y+b.h>=gy){b.y=gy-b.h;b.vy=0;}
  b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));
  b.walkPhase+=.11*dt;b.atkPhase=Math.max(0,b.atkPhase-.1*dt);
  b.atkTimer-=dt;b.projTimer-=dt;

  const projInt=b.phase3?42:b.phase2?62:100;
  if(b.projTimer<=0){
    b.projTimer=projInt;b.atkPhase=Math.PI*.85;
    const bv=dmg({atk:b.atk,atkBonus:0,buffAtk:1,critBonus:0},b.phase3?.75:.62);
    if(b.phase3){
      for(let i=-1;i<=1;i++) proj(b.x+b.w/2,b.y+b.h*.42,b.f*10,i*5,bv,'#ff2200','enemy',{sz:17,emoji:'💥',life:90,grav:.08});
    } else {
      proj(b.x+b.w/2,b.y+b.h*.42,b.f*9,-2,bv,'#ff4400','enemy',{sz:17,emoji:'💥',life:90,grav:.09});
    }
  }

  if(b.atkTimer<=0&&Math.abs(dx)<108){
    b.atkTimer=b.phase3?38:b.phase2?52:74;b.atkPhase=Math.PI;
    if(Math.abs(p.y-b.y)<100&&p.invincible<=0&&p.dodgeAnim<=0){
      const rawDmg=Math.max(1,b.atk-Math.round(totalDef(p)*.45)+Math.floor(Math.random()*14)-7);
      takeDmg(rawDmg);
      if(b.phase3) setTimeout(()=>{if(G&&p.hp>0)takeDmg(Math.round(rawDmg*.75));},220);
    }
  }
  document.getElementById('boss-hp-fill').style.width=Math.max(0,(b.hp/b.maxHp)*100)+'%';
}

function takeDmg(v){
  const p=G.player;
  if(p.invincible>0) return;
  p.hp-=v;p.hitFlash=14;p.invincible=40;G.stageDmgTaken+=v;
  const fl=document.getElementById('hit-flash');
  fl.style.opacity='1';fl.style.background='rgba(255,30,30,.4)';
  setTimeout(()=>{fl.style.opacity='0';},120);
  shake(5,12);
  if(p.hp<=0) gameOver();
}

function updateProjs(dt){
  const p=G.player;const gy=GY();
  G.projectiles=G.projectiles.filter(pr=>{
    if(!pr.alive) return false;
    pr.x+=pr.vx*dt;pr.y+=pr.vy*dt;pr.vy+=pr.grav*dt;pr.life-=dt;
    if(pr.life<=0) return false;

    if(pr.homing&&pr.owner==='player'){
      const targets=[...G.enemies];if(G.boss&&G.boss.alive) targets.push(G.boss);
      let best=null,bd=999;
      for(const e of targets){if(!e.alive) continue;const d=Math.abs(e.x-pr.x)+Math.abs(e.y-pr.y);if(d<bd){bd=d;best=e;}}
      if(best&&bd<520){const ddx=best.x+best.w/2-pr.x,ddy=best.y+best.h/2-pr.y;const l=Math.sqrt(ddx*ddx+ddy*ddy)||1;pr.vx+=(ddx/l*3-pr.vx)*.14;pr.vy+=(ddy/l*3-pr.vy)*.14;}
    }
    if(pr.trail) spawnParts(pr.x-G.cam,pr.y,{n:2,col:[pr.col],sMin:1,sMax:3,grav:0,dMax:.07,spread:Math.PI*.3});

    if(pr.explode&&pr.y>=gy){
      boom(pr.x-G.cam,gy,pr.col);hitAOE(pr.x-70,gy-75,140,90,{v:pr.dmg,crit:pr.crit},false);shake(5,10);return false;
    }
    if(pr.y>gy+90||pr.x<G.cam-120||pr.x>G.cam+W()+120) return false;

    if(pr.owner==='player'){
      const targets=[...G.enemies];if(G.boss&&G.boss.alive) targets.push(G.boss);
      for(const e of targets){
        if(!e.alive) continue;
        if(pr.x>e.x&&pr.x<e.x+e.w&&pr.y>e.y&&pr.y<e.y+e.h){
          dealDmg(e,pr.dmg,pr.crit,{onHit:pr.onHit});
          spawnParts(pr.x-G.cam,pr.y,{n:9,col:[pr.col,'#fff'],sMin:2,sMax:6,glow:!!pr.emoji});
          if(!pr.pierce){pr.alive=false;return false;}
        }
      }
    } else {
      const sx=pr.x-G.cam;
      if(p.invincible<=0&&p.dodgeAnim<=0&&sx>p.x-G.cam&&sx<p.x-G.cam+p.w&&pr.y>p.y&&pr.y<p.y+p.h){
        takeDmg(Math.max(1,pr.dmg-Math.round(totalDef(p)*.4)));
        pr.alive=false;return false;
      }
    }
    return true;
  });
}

function updateItems(dt){
  const p=G.player;const gy=GY();
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAVITY*dt*.7;it.y+=it.vy*dt;
    if(it.y+20>=gy){it.y=gy-20;it.vy=0;}
    const sx=it.x-G.cam;
    if(sx>p.x-G.cam-32&&sx<p.x-G.cam+p.w+32&&it.y>p.y-12&&it.y<p.y+p.h+22){
      const res=it.fn(p);
      showDNum(sx,it.y,'+ '+res,false,'#ffcc00');
      it.alive=false;return false;
    }
    return true;
  });
}

// ══════════════════════════════════════════════════════
// RENDER
// ══════════════════════════════════════════════════════
function gameRender(){
  if(!G){ctx.fillStyle='#06040e';ctx.fillRect(0,0,W(),H());return;}
  ctx.save();
  if(G.shakeTimer>0){
    const s=G.shakeAmt*(G.shakeTimer/20)*.5;
    ctx.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }

  // BACKGROUND
  drawDungeonBG(G.stageIdx, G.cam, G.timer);
  drawPlatforms(G.stage);

  // EFFECTS
  drawSlashes(G.cam);
  drawShockwaves(G.cam);
  drawParts(G.cam);
  drawProjs();
  drawItems();
  drawEnemies_all();
  if(G.boss&&(G.boss.alive||G.boss.dying)) drawMonster(G.boss,G.cam);
  drawPlayer();

  ctx.restore();
  drawMinimap();
}

function drawPlayer(){
  const p=G.player;const px=p.x-G.cam;
  if(p.invincible>0&&Math.floor(G.timer/3)%2===0) return;
  ctx.save();
  // Dodge afterimages
  if(p.dodgeAnim>0){
    for(let i=1;i<=3;i++){
      ctx.globalAlpha=(p.dodgeAnim/24)*(i/3)*.24;
      drawChar({x:px-p.f*i*18,y:p.y+p.h,f:p.f,state:'dodge',walkPhase:p.walkPhase,atkPhase:0,hitFlash:0,dead:false,...p,scale:.9});
    }
    ctx.globalAlpha=1;
  }
  drawChar({x:px,y:p.y+p.h,f:p.f,state:p.state,walkPhase:p.walkPhase,atkPhase:p.atkPhase,hitFlash:p.hitFlash,dead:!p.alive,jumpVy:p.vy,...p});
  // Shadow
  ctx.globalAlpha=.22+.08*(1-Math.min(1,(p.y-(GY()-p.h))/200));
  ctx.fillStyle='#000';
  ctx.beginPath();ctx.ellipse(px+p.w/2,GY()+6,p.w*.5,7,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawEnemies_all(){
  for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const ex=e.x-G.cam;
    if(ex<-120||ex>W()+120) continue;
    const alpha=e.dying?(e.deathTimer/30):1;
    ctx.save();ctx.globalAlpha=alpha;
    drawMonster(e,G.cam);
    // Enemy shadow
    ctx.globalAlpha=alpha*.15;ctx.fillStyle='#000';
    ctx.beginPath();ctx.ellipse(ex+e.w/2,GY()+5,e.w*.45*(e.drawScale||1),6,0,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
}

function drawProjs(){
  for(const pr of G.projectiles){
    const px=pr.x-G.cam;
    if(px<-40||px>W()+40) continue;
    if(pr.emoji){
      ctx.save();
      if(pr.glow){ctx.shadowColor=pr.col;ctx.shadowBlur=14;}
      ctx.font=`${pr.sz*1.9}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pr.emoji,px,pr.y);
      ctx.shadowBlur=0;ctx.restore();
    } else {
      ctx.save();
      ctx.fillStyle=pr.col;ctx.shadowColor=pr.col;ctx.shadowBlur=12;
      ctx.beginPath();ctx.arc(px,pr.y,pr.sz,0,Math.PI*2);ctx.fill();
      // Motion trail
      ctx.globalAlpha=.3;ctx.shadowBlur=0;
      ctx.beginPath();ctx.arc(px-pr.vx*.8,pr.y-pr.vy*.8,pr.sz*.6,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;ctx.restore();
    }
  }
}

function drawItems(){
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam;
    if(ix<-40||ix>W()+40) continue;
    ctx.save();
    ctx.shadowColor=RARITY_COL[it.rarity||0];ctx.shadowBlur=14;
    const bob=Math.sin(G.timer*.08+it.x*.01)*4;
    ctx.font='23px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(it.icon,ix,it.y+bob);
    // Glow ring
    ctx.globalAlpha=.2+Math.sin(G.timer*.06)*.1;
    ctx.strokeStyle=RARITY_COL[it.rarity||0];ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(ix,it.y+bob,14,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;ctx.restore();
  }
}

function drawMinimap(){
  const mc=document.getElementById('mm-canvas');
  const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,110,26);
  const scale=110/STAGE_W;
  const p=G.player;
  // BG
  mctx.fillStyle='rgba(0,0,0,.5)';mctx.fillRect(0,0,110,26);
  for(const e of G.enemies){
    if(!e.alive) continue;
    mctx.fillStyle=e.bodyCol||'#f44';mctx.fillRect(e.x*scale,9,3,3);
  }
  if(G.boss&&G.boss.alive){mctx.fillStyle='#f00';mctx.fillRect(G.boss.x*scale-1,7,6,6);}
  mctx.fillStyle='#0fa';mctx.fillRect(p.x*scale-2,9,5,5);
  mctx.strokeStyle='rgba(245,200,66,.4)';mctx.lineWidth=1;
  mctx.strokeRect(G.cam*scale,1,W()*scale,24);
}

// ══════════════════════════════════════════════════════
// HUD UPDATE
// ══════════════════════════════════════════════════════
function updateHUD(){
  if(!G) return;
  const p=G.player;
  const hp=Math.max(0,p.hp),mp=Math.max(0,p.mp);
  document.getElementById('hp-fill').style.width=Math.max(0,(hp/p.maxHp)*100)+'%';
  document.getElementById('mp-fill').style.width=Math.max(0,(mp/p.maxMp)*100)+'%';
  document.getElementById('hp-text').textContent=`${hp}/${p.maxHp}`;
  document.getElementById('xp-fill').style.width=Math.min(100,(p.xp/p.xpNext)*100)+'%';
  document.getElementById('xp-text').textContent=`${p.xp}/${p.xpNext}`;
  document.getElementById('s-lv').textContent=p.level;
  document.getElementById('s-atk').textContent=Math.round(totalAtk(p));
  document.getElementById('s-def').textContent=Math.round(totalDef(p));
  document.getElementById('s-kills').textContent=p.kills;
  document.getElementById('s-score').textContent=p.score;
  document.getElementById('s-gold').textContent=p.gold;
  document.getElementById('hud-name').textContent=p.name||'—';
  document.getElementById('floor-lbl').textContent=(G.stageIdx+1)+'스테이지';

  let bi='';
  if(p.buffAtk>1) bi+='<span title="공격강화">🔥</span>';
  if(p.defBuff>0) bi+='<span title="방어강화">🛡️</span>';
  if(p.invincible>60) bi+='<span title="무적">⭐</span>';
  document.getElementById('buff-row').innerHTML=bi;

  const sc=document.getElementById('sk-cont');
  sc.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i];const cd=p.skillCds[i];
    const rdy=cd<=0&&p.mp>=sk.mp;
    const div=document.createElement('div');
    div.className='sk-slot '+(rdy?'ready':'cooling');
    div.innerHTML=`<div class="sk-icon">${sk.icon}</div><span class="sk-key">${sk.key}</span><span class="sk-mp-cost">${sk.mp}</span>`;
    if(cd>0){
      const cdDiv=document.createElement('div');cdDiv.className='sk-cd-overlay';
      cdDiv.textContent=cd>60?Math.ceil(cd/60)+'s':cd.toFixed(1)+'s';div.appendChild(cdDiv);
    }
    div.title=`${sk.name} [${sk.key}] MP:${sk.mp} CD:${sk.cd}s\n${sk.desc}`;
    sc.appendChild(div);
  }
  updateEquipUI();
}

function updateEquipUI(){
  if(!G) return;
  const p=G.player;
  ['wpn','arm','acc'].forEach((s,i)=>{
    const el=document.getElementById('eq-'+s);if(!el) return;
    const icons=['🗡️','🛡️','💍'];
    el.textContent=p.equip[s]?p.equip[s].icon:icons[i];
  });
}

// ══════════════════════════════════════════════════════
// DAMAGE NUMBERS
// ══════════════════════════════════════════════════════
function showDNum(sx,sy,v,crit,col){
  const garea=document.getElementById('game-area');
  const el=document.createElement('div');
  el.className='dnum';
  el.style.cssText=`left:${garea.offsetLeft+sx-18}px;top:${garea.offsetTop+sy-14}px;font-size:${crit?'1.45':'1.0'}rem;color:${crit?'#ffff44':(col||'#fff')};`;
  el.textContent=crit?v+'!!':v;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),1050);
}

// ══════════════════════════════════════════════════════
// STAGE TRANSITIONS
// ══════════════════════════════════════════════════════
function stageClear(){
  G.phase='clear';
  const p=G.player;
  const el=Math.round((Date.now()-G.startTime)/1000);
  const bonus=G.stageDmgTaken===0?5000:0;
  p.score+=bonus;
  document.getElementById('clear-grid').innerHTML=`
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">점수<b>${p.score}</b></div>
    <div class="res-cell">시간<b>${el}초</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">무피해<b>${bonus?'+5000':'없음'}</b></div>`;
  document.getElementById('clear-ov').classList.remove('hidden');
}

function gameOver(){
  if(!G||G.phase!=='play') return;
  G.phase='over';G.player.alive=false;
  const p=G.player;
  document.getElementById('over-grid').innerHTML=`
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">점수<b>${p.score}</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">스테이지<b>${G.stageIdx+1}</b></div>
    <div class="res-cell">콤보<b>${G.maxCombo}HIT</b></div>`;
  setTimeout(()=>document.getElementById('over-ov').classList.remove('hidden'),800);
  sfx_death();
}

function openShop(){
  document.getElementById('clear-ov').classList.add('hidden');
  buildShop();document.getElementById('shop-ov').classList.remove('hidden');
}

function buildShop(){
  const p=G.player;
  document.getElementById('shop-gold-lbl').textContent=p.gold;
  const pool=[...SHOP_ITEMS].sort(()=>Math.random()-.5).slice(0,6);
  G.shopStock=pool.map(it=>({...it,uid:'s'+Date.now()+Math.random(),price:it.price+G.stageIdx*32}));
  const grid=document.getElementById('shop-grid');
  grid.innerHTML=G.shopStock.map((it,i)=>{
    const cant=p.gold<it.price;
    return `<div class="shop-card ${cant?'cant':''}" onclick="buyShopItem(${i})">
      <div class="sc-icon">${it.icon}</div>
      <div class="sc-name" style="color:${RARITY_COL[it.rarity||0]}">${it.name}</div>
      <div class="sc-desc">${it.desc}</div>
      <div class="sc-price">${it.price}💰</div>
    </div>`;
  }).join('');
}

function buyShopItem(i){
  const p=G.player;const it=G.shopStock[i];
  if(!it||p.gold<it.price) return;
  p.gold-=it.price;const res=it.fn(p);
  sfx_buy();buildShop();
}

function continueAfterShop(){
  document.getElementById('shop-ov').classList.add('hidden');
  const next=(G.stageIdx+1)%STAGES.length;
  initGame(G.clsId,next);
}

function retryStage(){
  document.getElementById('over-ov').classList.add('hidden');
  initGame(G.clsId,G.stageIdx);
}

function gotoTitle(){
  ['clear-ov','over-ov','shop-ov','lvlup-ov','pause-ov'].forEach(id=>document.getElementById(id).classList.add('hidden'));
  document.getElementById('title-ov').classList.remove('hidden');
  document.getElementById('boss-bar').classList.remove('show');
  G=null;
}

// ══════════════════════════════════════════════════════
// LEVEL UP
// ══════════════════════════════════════════════════════
function showLvlUpModal(){
  const grid=document.getElementById('stat-pick-grid');
  grid.innerHTML=`
    <button class="stat-pick-btn" onclick="pickStat('hp')">❤️ 최대 HP +28</button>
    <button class="stat-pick-btn" onclick="pickStat('atk')">⚔️ ATK +6</button>
    <button class="stat-pick-btn" onclick="pickStat('def')">🛡️ DEF +4</button>
    <button class="stat-pick-btn" onclick="pickStat('spd')">💨 SPD +0.6</button>
    <button class="stat-pick-btn" onclick="pickStat('mp')">🔷 최대 MP +22</button>
    <button class="stat-pick-btn" onclick="pickStat('crit')">⚡ 크리 +6%</button>`;
  document.getElementById('lvlup-ov').classList.remove('hidden');
}

function pickStat(stat){
  const p=G.player;
  if(stat==='hp'){p.maxHp+=28;p.hp=Math.min(p.maxHp,p.hp+28);}
  else if(stat==='atk') p.atk+=6;
  else if(stat==='def') p.def+=4;
  else if(stat==='spd') p.spd+=0.6;
  else if(stat==='mp'){p.maxMp+=22;p.mp=Math.min(p.maxMp,p.mp+22);}
  else if(stat==='crit') p.critBonus=(p.critBonus||0)+.06;
  document.getElementById('lvlup-ov').classList.add('hidden');
  G.pendingLvlUp=false;
}

// ══════════════════════════════════════════════════════
// AUDIO
// ══════════════════════════════════════════════════════
let ACtx=null;
function ensureAudio(){if(!ACtx) try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function synth(freq,type,dur,vol=.3,del=0){
  if(!ACtx) return;
  try{
    const o=ACtx.createOscillator(),g=ACtx.createGain();
    o.connect(g);g.connect(ACtx.destination);
    o.type=type;o.frequency.value=freq;
    const t=ACtx.currentTime+del;
    g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.005);g.gain.exponentialRampToValueAtTime(.001,t+dur);
    o.start(t);o.stop(t+dur+.05);
  }catch(e){}
}
const sfx_jump=()=>{ensureAudio();synth(340,'sine',.09,.12);};
const sfx_dodge=()=>{ensureAudio();synth(480,'sine',.07,.14);};
const sfx_lvl=()=>{ensureAudio();[523,659,784,1047].forEach((f,i)=>synth(f,'sine',.3,.35,i*.1));};
const sfx_clear=()=>{ensureAudio();[523,659,784,523,659,784,1047].forEach((f,i)=>synth(f,'sine',.25,.35,i*.11));};
const sfx_death=()=>{ensureAudio();for(let i=0;i<5;i++)synth(200-i*25,'sawtooth',.22,.28,i*.08);};
const sfx_buy=()=>{ensureAudio();synth(700,'sine',.18,.25);synth(900,'sine',.14,.2,.09);};
const sfx_bossIn=()=>{ensureAudio();for(let i=0;i<4;i++)synth(70+i*15,'sawtooth',.45,.5,i*.22);};

// ══════════════════════════════════════════════════════
// TITLE SCREEN
// ══════════════════════════════════════════════════════
function buildTitle(){
  const row=document.getElementById('char-row');
  row.innerHTML='';
  const mkStars=(n,max=5)=>[...Array(max)].map((_,i)=>`<span class="star ${i<n?'on':''}">★</span>`).join('');
  for(const [id,c] of Object.entries(CLASSES)){
    const div=document.createElement('div');
    div.className='ccard';div.id='cc-'+id;
    div.onclick=()=>{
      selCharId=id;
      document.querySelectorAll('.ccard').forEach(x=>x.classList.remove('sel'));
      div.classList.add('sel');
      document.getElementById('start-btn').disabled=false;
      ensureAudio();
    };
    const stars=c.stars;
    div.innerHTML=`
      <div style="font-size:2.2rem;margin-bottom:6px;">${c.icon}</div>
      <div class="ccard-name">${c.name}</div>
      <div class="ccard-role">${c.role}</div>
      <div class="ccard-stars">${mkStars(stars.ATK||3)}</div>
      <div class="ccard-desc">${c.desc}</div>`;
    row.appendChild(div);
  }
}

function startPressed(){
  if(!selCharId) return;
  document.getElementById('title-ov').classList.add('hidden');
  initGame(selCharId,0);
}

// TITLE IDLE
let titleRaf=null;
function titleIdle(ts){
  if(G){return;}
  ctx.fillStyle='#06040e';ctx.fillRect(0,0,W(),H());
  // Animated background archs
  ctx.save();ctx.globalAlpha=.04+Math.sin(ts*.001)*.02;
  ctx.font='900 80px sans-serif';ctx.fillStyle='#ff6600';ctx.textAlign='center';
  ctx.fillText('DUNGEON CRUSH',W()/2,H()/2+30);ctx.restore();
  updateParts(1);drawParts(0);
  if(Math.random()<.3) spawnParts(Math.random()*W(),Math.random()*H(),{n:2,col:['#ff6600','#ffaa00','#cc44ff'],glow:true,sMin:1,sMax:3,grav:-.02,dMin:.01,dMax:.015});
  titleRaf=requestAnimationFrame(titleIdle);
}

// BOOT
KEY['ArrowLeft']=false;
buildTitle();
titleRaf=requestAnimationFrame(titleIdle);
RAF=requestAnimationFrame(loop);
</script>

<!-- 📱 모바일 가상 D-패드 -->
<style>
#mobile-dpad{
  display:none;position:fixed;bottom:70px;left:12px;z-index:9999;
  width:130px;height:130px;pointer-events:auto;
}
#mobile-skills{
  display:none;position:fixed;bottom:70px;right:12px;z-index:9999;
  display:grid;grid-template-columns:1fr 1fr;gap:6px;pointer-events:auto;
}
.dpad-btn{
  position:absolute;width:40px;height:40px;
  background:rgba(245,200,66,0.15);border:1px solid rgba(245,200,66,0.4);
  border-radius:6px;display:flex;align-items:center;justify-content:center;
  font-size:1.1rem;color:rgba(245,200,66,0.8);cursor:pointer;
  user-select:none;-webkit-user-select:none;
  transition:background 0.1s;
}
.dpad-btn:active{background:rgba(245,200,66,0.4);}
#dpad-up   {top:0;   left:45px;}
#dpad-down {bottom:0;left:45px;}
#dpad-left {top:45px;left:0;}
#dpad-right{top:45px;right:0;}
.sk-touch-btn{
  width:52px;height:52px;border-radius:8px;
  background:rgba(255,255,255,0.05);border:1px solid rgba(245,200,66,0.25);
  display:flex;align-items:center;justify-content:center;
  font-size:1.3rem;cursor:pointer;user-select:none;-webkit-user-select:none;
  transition:background 0.1s;
}
.sk-touch-btn:active{background:rgba(245,200,66,0.3);}
@media (pointer: coarse) {
  #mobile-dpad, #mobile-skills { display:block !important; }
  #mobile-skills { display:grid !important; }
}
</style>
<div id="mobile-dpad">
  <div class="dpad-btn" id="dpad-up">▲</div>
  <div class="dpad-btn" id="dpad-left">◀</div>
  <div class="dpad-btn" id="dpad-right">▶</div>
  <div class="dpad-btn" id="dpad-down">▼</div>
</div>
<div id="mobile-skills">
  <div class="sk-touch-btn" data-key="z">Z</div>
  <div class="sk-touch-btn" data-key="x">X</div>
  <div class="sk-touch-btn" data-key="c">C</div>
  <div class="sk-touch-btn" data-key="v">V</div>
</div>
<script>
(function(){
  var map={
    'dpad-up':'ArrowUp','dpad-down':'ArrowDown',
    'dpad-left':'ArrowLeft','dpad-right':'ArrowRight'
  };
  Object.keys(map).forEach(function(id){
    var el=document.getElementById(id);
    if(!el)return;
    var k=map[id];
    el.addEventListener('touchstart',function(e){e.preventDefault();KEY[k]=true;},  {passive:false});
    el.addEventListener('touchend',  function(e){e.preventDefault();KEY[k]=false;}, {passive:false});
    el.addEventListener('mousedown', function(){KEY[k]=true;});
    el.addEventListener('mouseup',   function(){KEY[k]=false;});
  });
  document.querySelectorAll('.sk-touch-btn').forEach(function(el){
    var k=el.dataset.key;
    el.addEventListener('touchstart',function(e){
      e.preventDefault();
      document.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true}));
    },{passive:false});
  });
})();
</script>
</body>
</html>
"""

def render():
    st.markdown("""
<style>
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
header{display:none!important;}
footer{display:none!important;}
iframe{border:none!important;}
</style>
""", unsafe_allow_html=True)

    st.caption("🎮 키보드: WASD 또는 방향키 이동 | Z·X·C·V 스킬 | 📱 모바일: 화면 내 버튼 사용")
    components.html(GAME_HTML, height=820, scrolling=True)
