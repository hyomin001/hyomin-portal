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
  --bg:#08060f;--bg2:#0d0a1a;--panel:#0a0818;
  --gold:#f5c842;--gold2:#ffe680;--red:#ff2233;--blue:#2299ff;
  --green:#22ff88;--purple:#cc44ff;--orange:#ff7722;
  --border:rgba(245,200,66,0.18);
}
html,body{
  width:100%;height:100%;background:var(--bg);overflow:hidden;
  font-family:'Noto Sans KR',sans-serif;color:#ddd;
}
#wrap{width:100vw;height:100vh;display:flex;flex-direction:column;}

/* ── HUD TOP ── */
#hud{
  height:46px;background:linear-gradient(180deg,#0d0a18,#09061200);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:10px;padding:0 12px;
  flex-shrink:0;position:relative;z-index:50;
}
.hud-char{
  font-family:'Black Han Sans',sans-serif;font-size:.8rem;
  color:var(--gold);letter-spacing:2px;white-space:nowrap;
}
.bar-group{display:flex;flex-direction:column;gap:2px;}
.bar-row{display:flex;align-items:center;gap:4px;}
.bar-label{font-size:.48rem;color:#666;width:14px;text-align:right;}
.bar-bg{height:9px;background:rgba(255,255,255,.06);border-radius:2px;border:1px solid rgba(255,255,255,.05);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:2px;transition:width .1s;}
#hp-fill{background:linear-gradient(90deg,#660000,#dd1122,#ff4455);width:100%;}
#mp-fill{background:linear-gradient(90deg,#001166,#1144cc,#3388ff);width:100%;}
#xp-fill{background:linear-gradient(90deg,#224400,#44aa00,#88ff44);width:0%;}
.bar-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.42rem;color:rgba(255,255,255,.65);font-weight:700;}
#stat-row{display:flex;gap:5px;margin-left:4px;}
.sbox{
  background:rgba(255,255,255,.04);border:1px solid var(--border);
  border-radius:3px;padding:1px 6px;text-align:center;min-width:36px;
}
.sbox-v{font-size:.75rem;font-weight:900;color:var(--gold);}
.sbox-l{font-size:.38rem;color:#555;letter-spacing:.5px;}
.floor-lbl{
  font-family:'Rajdhani',sans-serif;font-size:.9rem;font-weight:700;
  color:#fff;background:rgba(245,200,66,.1);border:1px solid var(--border);
  border-radius:3px;padding:1px 10px;letter-spacing:2px;margin-left:auto;
}
#buff-row{display:flex;gap:3px;font-size:.85rem;}

/* ── GAME AREA ── */
#game-area{flex:1;position:relative;overflow:hidden;}
canvas#gc{display:block;width:100%;height:100%;}

/* ── BOSS BAR ── */
#boss-bar{
  position:absolute;top:6px;left:50%;transform:translateX(-50%);
  width:360px;pointer-events:none;z-index:40;opacity:0;transition:opacity .3s;
}
#boss-bar.show{opacity:1;}
#boss-name-lbl{
  text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.75rem;
  color:#ff3344;margin-bottom:2px;text-shadow:0 0 10px rgba(255,0,50,.6);letter-spacing:2px;
}
#boss-hp-bg{height:10px;background:rgba(255,255,255,.05);border-radius:2px;border:1px solid rgba(255,50,70,.3);overflow:hidden;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);border-radius:2px;transition:width .12s;}
#boss-phase-txt{text-align:center;font-size:.48rem;color:#ff7788;letter-spacing:3px;margin-top:2px;}

/* ── SKILL BAR ── */
#skill-bar{
  position:absolute;bottom:0;left:0;right:0;height:58px;
  background:linear-gradient(0deg,#0d0a18f5,#0d0a1880);
  border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  gap:6px;padding:0 10px;z-index:50;
}
.sk-slot{
  width:48px;height:48px;border-radius:5px;position:relative;
  background:rgba(255,255,255,.04);border:1px solid rgba(245,200,66,.2);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  cursor:default;transition:border-color .1s;
}
.sk-slot.ready{border-color:rgba(245,200,66,.7);box-shadow:0 0 10px rgba(245,200,66,.25);}
.sk-slot.cooling{opacity:.38;}
.sk-icon{font-size:1.3rem;line-height:1;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.38rem;color:#666;}
.sk-mp-cost{position:absolute;top:2px;left:3px;font-size:.38rem;color:#5599ff;}
.sk-cd-overlay{
  position:absolute;inset:0;background:rgba(0,0,0,.75);border-radius:5px;
  display:flex;align-items:center;justify-content:center;
  font-size:.72rem;color:var(--gold);font-weight:900;
}
/* CD ring around skill */
.sk-ring{
  position:absolute;inset:-2px;border-radius:7px;
  border:2px solid transparent;pointer-events:none;
}
.sk-slot.ready .sk-ring{border-color:rgba(245,200,66,.4);}

.ctrl-hint{
  position:absolute;right:12px;font-size:.48rem;color:#3a3550;
  line-height:1.8;text-align:right;pointer-events:none;
}

/* ── COMBO ── */
#combo-display{
  position:absolute;top:12px;right:14px;text-align:right;
  pointer-events:none;opacity:0;transition:opacity .3s;z-index:45;
}
#combo-num{
  font-family:'Black Han Sans',sans-serif;font-size:2.4rem;
  color:var(--gold);line-height:1;
  text-shadow:0 0 20px rgba(245,200,66,.8),2px 2px 0 rgba(0,0,0,.8);
}
#combo-lbl{font-size:.58rem;color:var(--orange);letter-spacing:4px;}

/* ── OVERLAYS ── */
.ov{
  position:absolute;inset:0;z-index:200;
  display:flex;align-items:center;justify-content:center;
  background:rgba(8,6,15,.97);
}
.ov.hidden{display:none;}

/* TITLE */
#title-ov{flex-direction:column;text-align:center;}
.title-logo{
  font-family:'Black Han Sans',sans-serif;font-size:3.5rem;letter-spacing:8px;
  background:linear-gradient(135deg,#ff4400,#ff9900,#ffcc00,#ff6600);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(255,150,0,.6));margin-bottom:4px;
}
.title-sub{font-family:'Rajdhani',sans-serif;font-size:.9rem;color:#444;letter-spacing:10px;margin-bottom:30px;}
.char-row{display:flex;gap:10px;margin-bottom:24px;}
.ccard{
  width:110px;background:rgba(255,255,255,.02);border:1px solid rgba(245,200,66,.12);
  border-radius:8px;padding:12px 8px;cursor:pointer;transition:all .2s;text-align:center;
}
.ccard:hover,.ccard.sel{
  border-color:rgba(245,200,66,.7);background:rgba(245,200,66,.05);
  transform:translateY(-4px);box-shadow:0 8px 30px rgba(245,200,66,.15);
}
.ccard-preview{
  width:72px;height:72px;margin:0 auto 8px;position:relative;
  /* mini character preview drawn by canvas */
}
.ccard-preview canvas{width:72px;height:72px;}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:.75rem;color:var(--gold);letter-spacing:2px;}
.ccard-role{font-size:.5rem;color:#555;margin-top:2px;}
.ccard-stars{display:flex;justify-content:center;gap:1px;margin-top:5px;}
.star{font-size:.55rem;color:#222;}
.star.on{color:var(--gold);}
.ccard-desc{font-size:.48rem;color:#444;margin-top:6px;line-height:1.5;padding:0 2px;}
.start-btn{
  padding:13px 50px;background:linear-gradient(135deg,#7a2e00,#ff5500);
  border:none;border-radius:4px;color:#fff;
  font-family:'Black Han Sans',sans-serif;font-size:.9rem;letter-spacing:4px;
  cursor:pointer;box-shadow:0 0 24px rgba(255,100,0,.4);transition:all .2s;
}
.start-btn:hover{transform:scale(1.06);filter:brightness(1.2);}
.start-btn:disabled{opacity:.25;cursor:default;transform:none;}

/* CLEAR / OVER */
.result-box{
  background:rgba(13,10,26,.98);border:1px solid var(--border);
  border-radius:10px;padding:28px 36px;min-width:340px;text-align:center;
  box-shadow:0 0 60px rgba(245,200,66,.1);
}
.result-title{
  font-family:'Black Han Sans',sans-serif;font-size:1.8rem;letter-spacing:4px;margin-bottom:14px;
}
.clear-title{color:var(--gold);text-shadow:0 0 20px rgba(245,200,66,.5);}
.over-title{color:var(--red);text-shadow:0 0 20px rgba(255,30,50,.5);}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:10px 0;text-align:left;}
.res-cell{font-size:.68rem;color:#777;display:flex;justify-content:space-between;}
.res-cell b{color:var(--gold);}
.action-row{display:flex;gap:8px;justify-content:center;margin-top:14px;}
.abtn{
  padding:9px 22px;border:none;border-radius:4px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:.78rem;letter-spacing:2px;transition:all .18s;
}
.abtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.btn-next{background:linear-gradient(135deg,#1a5500,#22aa00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-gray{background:rgba(255,255,255,.07);color:#888;border:1px solid rgba(255,255,255,.1);}

/* SHOP */
#shop-ov{flex-direction:column;text-align:center;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.6rem;color:var(--gold);letter-spacing:4px;margin-bottom:8px;}
.shop-grid{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:14px 0;}
.shop-card{
  width:120px;background:rgba(255,255,255,.03);border:1px solid rgba(245,200,66,.15);
  border-radius:6px;padding:10px 8px;cursor:pointer;transition:all .18s;text-align:center;
}
.shop-card:hover:not(.cant){border-color:rgba(245,200,66,.6);background:rgba(245,200,66,.06);}
.shop-card.cant{opacity:.35;cursor:default;}
.sc-icon{font-size:1.6rem;margin-bottom:5px;}
.sc-name{font-size:.65rem;color:#ccc;font-weight:700;}
.sc-desc{font-size:.5rem;color:#555;margin-top:2px;}
.sc-price{font-size:.7rem;color:var(--gold);font-weight:900;margin-top:6px;}

/* LEVEL UP */
#lvlup-ov{flex-direction:column;text-align:center;}
.lvlup-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;color:var(--gold);letter-spacing:4px;margin-bottom:10px;}
.stat-pick-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;}
.stat-pick-btn{
  padding:12px 10px;border:1px solid var(--border);border-radius:5px;
  background:rgba(255,255,255,.04);cursor:pointer;transition:all .18s;
  font-family:'Noto Sans KR',sans-serif;font-size:.75rem;color:#ccc;
}
.stat-pick-btn:hover{border-color:var(--gold);background:rgba(245,200,66,.07);color:var(--gold);}

/* DAMAGE NUMBERS */
@keyframes dmgUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-65px) scale(.7);}}
.dnum{
  position:absolute;pointer-events:none;
  font-family:'Black Han Sans',sans-serif;
  animation:dmgUp .9s ease forwards;z-index:150;
  text-shadow:1px 1px 3px rgba(0,0,0,.9);
}

/* MINIMAP */
#minimap{
  position:absolute;bottom:62px;right:10px;
  width:110px;height:26px;background:rgba(0,0,0,.7);
  border:1px solid var(--border);border-radius:3px;overflow:hidden;z-index:45;
}
#mm-canvas{width:110px;height:26px;}

/* EQUIP QUICK-SLOTS */
#equip-quick{
  position:absolute;bottom:62px;left:10px;z-index:45;
  display:flex;gap:4px;
}
.eq-quick{
  width:34px;height:34px;background:rgba(0,0,0,.7);
  border:1px solid rgba(245,200,66,.2);border-radius:4px;
  display:flex;align-items:center;justify-content:center;
  font-size:.9rem;position:relative;
}
.eq-quick .eq-name{
  position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);
  font-size:.38rem;color:#444;white-space:nowrap;
}

/* SCREEN FLASH */
#hit-flash{position:absolute;inset:0;pointer-events:none;z-index:100;opacity:0;background:rgba(255,30,30,0);transition:opacity .06s;}

/* BOSS WARNING */
@keyframes bwPulse{0%,100%{opacity:0;transform:translate(-50%,-50%) scale(.8);}30%,70%{opacity:1;transform:translate(-50%,-50%) scale(1);}}
#boss-warn{
  position:absolute;top:45%;left:50%;z-index:180;display:none;
  font-family:'Black Han Sans',sans-serif;font-size:2rem;color:#ff2233;
  text-shadow:0 0 30px rgba(255,0,50,1);letter-spacing:6px;text-align:center;
  animation:bwPulse 2.2s ease forwards;pointer-events:none;
}

/* ACHIEVEMENT */
#achiev{
  position:absolute;top:54px;left:50%;
  transform:translateX(-50%) translateY(-80px);
  background:rgba(40,28,4,.97);border:1px solid rgba(245,200,66,.5);
  border-radius:5px;padding:7px 18px;display:flex;align-items:center;gap:8px;
  z-index:300;transition:transform .3s;pointer-events:none;
  box-shadow:0 4px 20px rgba(245,200,66,.3);
}
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
        <div class="bar-bg" style="width:140px">
          <div class="bar-fill" id="hp-fill"></div>
          <div class="bar-text" id="hp-text"></div>
        </div>
      </div>
      <div class="bar-row">
        <span class="bar-label">MP</span>
        <div class="bar-bg" style="width:140px">
          <div class="bar-fill" id="mp-fill"></div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;margin-left:5px;">
      <div style="font-size:.44rem;color:#444;">XP</div>
      <div class="bar-bg" style="width:90px;height:6px;">
        <div class="bar-fill" id="xp-fill"></div>
      </div>
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
    <div class="floor-lbl" id="floor-lbl">1-1</div>
  </div>

  <div id="game-area">
    <canvas id="gc"></canvas>
    <div id="hit-flash"></div>

    <!-- BOSS BAR -->
    <div id="boss-bar">
      <div id="boss-name-lbl">BOSS</div>
      <div id="boss-hp-bg"><div id="boss-hp-fill" style="width:100%"></div></div>
      <div id="boss-phase-txt"></div>
    </div>

    <!-- COMBO -->
    <div id="combo-display">
      <div id="combo-num">0</div>
      <div id="combo-lbl">COMBO</div>
    </div>

    <!-- MINIMAP -->
    <div id="minimap"><canvas id="mm-canvas" width="110" height="26"></canvas></div>

    <!-- EQUIP QUICK -->
    <div id="equip-quick">
      <div class="eq-quick" id="eq-wpn">🗡️<span class="eq-name">무기</span></div>
      <div class="eq-quick" id="eq-arm">🛡️<span class="eq-name">방어</span></div>
      <div class="eq-quick" id="eq-acc">💍<span class="eq-name">장신구</span></div>
    </div>

    <!-- BOSS WARNING -->
    <div id="boss-warn">⚠ BOSS ⚠</div>

    <!-- ACHIEVEMENT -->
    <div id="achiev">
      <div id="ach-icon">🏆</div>
      <div><div id="ach-title">업적</div><div id="ach-sub">달성</div></div>
    </div>

    <!-- SKILL BAR -->
    <div id="skill-bar">
      <div id="sk-cont" style="display:flex;gap:6px;"></div>
      <div class="ctrl-hint">
        ←→ 이동 &nbsp;|&nbsp; Z 점프(2단)<br>
        X 공격 &nbsp;|&nbsp; A~G 스킬<br>
        Space 회피 &nbsp;|&nbsp; P 일시정지
      </div>
    </div>

    <!-- OVERLAYS -->
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
//  DUNGEON CRUSH — FULL ENGINE
//  캐릭터: 팔다리 분리 렌더링, 무기별 애니메이션
//  몬스터: 팔다리+몸통 렌더링, 다양한 AI
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
const GY = () => H() - 68; // ground Y

// ── COLOUR PALETTE ──────────────────────────────────────
const PAL = {
  skin1:'#f5c090', skin2:'#e8a870', skin3:'#c07840',
  hair1:'#1a0800', hair2:'#440000', hair3:'#ffd080',
  sword:'#c8d8f0', axe:'#b08060', bow:'#885522',
  staff:'#8844aa', gun:'#445566', scythe:'#224422',
  swordBlade:'#e8f0ff', axeBlade:'#ddc0a0',
};

// ══════════════════════════════════════════════════════
// INPUT
// ══════════════════════════════════════════════════════
const KEY = {}, JK = {};
window.addEventListener('keydown', e=>{
  if(!KEY[e.key]){KEY[e.key]=true;JK[e.key]=true;}
  if([' ','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e=>KEY[e.key]=false);
function flushJK(){for(const k in JK) delete JK[k];}

// ══════════════════════════════════════════════════════
// PARTICLES
// ══════════════════════════════════════════════════════
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
      type:opts.type||'c',
    });
  }
}
function updateParts(dt){
  for(let i=PARTS.length-1;i>=0;i--){
    const p=PARTS[i];
    p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.grav*dt;p.vx*=.96;p.life-=p.decay*dt;
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
    if(p.type==='sq'){ctx.fillRect(sx-p.sz/2,p.y-p.sz/2,p.sz,p.sz);}
    else{ctx.beginPath();ctx.arc(sx,p.y,p.sz,0,Math.PI*2);ctx.fill();}
    if(p.glow) ctx.shadowBlur=0;
  }
  ctx.globalAlpha=1;ctx.restore();
}

// ══════════════════════════════════════════════════════
// CHARACTER DRAWING — LIMB-BASED
// ══════════════════════════════════════════════════════
// Each character is drawn with: head, torso, L/R arms, L/R legs, weapon
// Walk cycle: sine wave on limbs

function drawLimb(cx,cy,ang,len,thick,col){
  ctx.save();
  ctx.translate(cx,cy);ctx.rotate(ang);
  ctx.strokeStyle=col;ctx.lineWidth=thick;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(len,0);ctx.stroke();
  ctx.restore();
}

// Generic humanoid renderer
// opts: {x,y,f,walkPhase,atkPhase,hitFlash,dead,skinCol,hairCol,torsoCol,legsCol,charId,weapon,skillGlow}
function drawChar(opts){
  const {x,y,f,walkPhase,atkPhase,hitFlash,dead,skinCol,hairCol,torsoCol,legsCol,weapon,skillGlow,scale=1}=opts;
  const sc=scale;
  ctx.save();
  ctx.translate(x,y);
  if(dead){ctx.globalAlpha=.35;ctx.rotate(f*Math.PI/2);}
  if(f===-1) ctx.scale(-1,1);
  if(hitFlash>0) ctx.filter=`brightness(${3-hitFlash*.2}) saturate(0)`;

  // === LEGS ===
  const legSwing=dead?0:Math.sin(walkPhase)*0.45;
  const legBend=dead?0:Math.abs(Math.sin(walkPhase))*.15;
  // Left leg
  const lLegAng=Math.PI/2+legSwing;
  ctx.save();ctx.translate(-5*sc,2*sc);ctx.rotate(lLegAng);
  ctx.strokeStyle=legsCol;ctx.lineWidth=7*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);ctx.rotate(-legBend);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
  // Boot
  ctx.fillStyle=legsCol;ctx.beginPath();ctx.ellipse(4*sc,16*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
  // Right leg
  const rLegAng=Math.PI/2-legSwing;
  ctx.save();ctx.translate(5*sc,2*sc);ctx.rotate(rLegAng);
  ctx.strokeStyle=legsCol;ctx.lineWidth=7*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);ctx.rotate(legBend);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
  ctx.fillStyle=legsCol;ctx.beginPath();ctx.ellipse(4*sc,16*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();

  // === TORSO ===
  ctx.fillStyle=torsoCol;
  ctx.beginPath();
  ctx.roundRect(-10*sc,-28*sc,20*sc,30*sc,4*sc);
  ctx.fill();
  // Belt
  ctx.fillStyle='rgba(0,0,0,.4)';
  ctx.fillRect(-10*sc,-2*sc,20*sc,5*sc);

  // === WEAPON (back arm swings it) ===
  const atkSwing=dead?0:Math.sin(atkPhase)*0.9;
  const armSwing=dead?0:Math.sin(walkPhase+Math.PI)*0.35;

  // Left arm (weapon arm)
  ctx.save();
  ctx.translate(10*sc,-20*sc);
  ctx.rotate(-Math.PI/6+atkSwing+armSwing);
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  ctx.rotate(.2+atkSwing*.5);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  // Draw weapon at hand
  drawWeapon(ctx, weapon, sc, atkPhase, skillGlow);
  ctx.restore();

  // Right arm (shield/offhand)
  ctx.save();
  ctx.translate(-10*sc,-20*sc);
  ctx.rotate(Math.PI/6-armSwing);
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);
  ctx.rotate(-.15);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  // Offhand item
  if(opts.offhand) drawOffhand(ctx, opts.offhand, sc);
  ctx.restore();

  // === HEAD ===
  ctx.fillStyle=skinCol;
  ctx.beginPath();ctx.arc(0,-36*sc,12*sc,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=hairCol;
  ctx.beginPath();ctx.arc(0,-38*sc,11*sc,Math.PI,Math.PI*2);ctx.fill();
  ctx.fillRect(-11*sc,-38*sc,22*sc,6*sc);
  // Eyes
  ctx.fillStyle='#fff';
  ctx.beginPath();ctx.arc(4*sc,-37*sc,3.5*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=dead?'#555':'#1a0a00';
  ctx.beginPath();ctx.arc(5*sc,-37*sc,2*sc,0,Math.PI*2);ctx.fill();
  // Eyebrow
  ctx.strokeStyle='rgba(0,0,0,.6)';ctx.lineWidth=1.5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(1*sc,-42*sc);ctx.lineTo(7*sc,-41*sc);ctx.stroke();

  // Class-specific head decoration
  if(opts.headDeco) drawHeadDeco(ctx, opts.headDeco, sc);

  // Glow aura (skill buff)
  if(skillGlow){
    ctx.globalAlpha=.4+Math.sin(Date.now()*.006)*.2;
    ctx.shadowColor=skillGlow;ctx.shadowBlur=30;
    ctx.strokeStyle=skillGlow;ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.arc(0,-14*sc,28*sc,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
  }

  ctx.filter='none';
  ctx.restore();
}

function drawWeapon(ctx, wpn, sc, atkPhase, glow){
  if(!wpn) return;
  const swing=Math.sin(atkPhase)*.3;
  ctx.save();
  ctx.rotate(-Math.PI/4+swing);
  if(glow){ctx.shadowColor=glow;ctx.shadowBlur=14;}
  switch(wpn){
    case 'sword':
      // Handle
      ctx.fillStyle='#8B6914';ctx.fillRect(-3*sc,0,6*sc,12*sc);
      // Guard
      ctx.fillStyle='#C0A020';ctx.fillRect(-8*sc,10*sc,16*sc,4*sc);
      // Blade
      ctx.fillStyle=PAL.swordBlade;
      ctx.beginPath();ctx.moveTo(-2*sc,14*sc);ctx.lineTo(0,-30*sc);ctx.lineTo(2*sc,14*sc);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.6)';
      ctx.beginPath();ctx.moveTo(0*sc,14*sc);ctx.lineTo(.5*sc,-30*sc);ctx.lineTo(2*sc,14*sc);ctx.closePath();ctx.fill();
      break;
    case 'axe':
      ctx.fillStyle='#664422';ctx.fillRect(-3*sc,0,6*sc,30*sc);
      ctx.fillStyle='#B08040';
      ctx.beginPath();ctx.moveTo(-2*sc,10*sc);ctx.lineTo(-20*sc,-10*sc);ctx.lineTo(-20*sc,12*sc);ctx.lineTo(-2*sc,28*sc);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(255,200,100,.4)';
      ctx.beginPath();ctx.moveTo(-2*sc,10*sc);ctx.lineTo(-20*sc,-10*sc);ctx.lineTo(-18*sc,0);ctx.lineTo(-2*sc,18*sc);ctx.closePath();ctx.fill();
      break;
    case 'bow':
      ctx.strokeStyle='#774422';ctx.lineWidth=3*sc;
      ctx.beginPath();ctx.arc(0,0,20*sc,-Math.PI*.6,Math.PI*.6);ctx.stroke();
      ctx.strokeStyle='#ddd';ctx.lineWidth=1.5*sc;
      ctx.beginPath();ctx.moveTo(0,-18*sc);ctx.lineTo(0,18*sc);ctx.stroke();
      if(Math.sin(atkPhase)>0.5){
        ctx.fillStyle='#cc8822';
        ctx.beginPath();ctx.moveTo(-2*sc,0);ctx.lineTo(10*sc,-3*sc);ctx.lineTo(10*sc,3*sc);ctx.closePath();ctx.fill();
      }
      break;
    case 'staff':
      ctx.fillStyle='#662288';ctx.fillRect(-2.5*sc,-30*sc,5*sc,50*sc);
      ctx.fillStyle='rgba(220,100,255,.8)';
      ctx.shadowColor='#cc44ff';ctx.shadowBlur=15;
      ctx.beginPath();ctx.arc(0,-30*sc,8*sc,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;
      break;
    case 'gun':
      ctx.fillStyle='#344455';ctx.fillRect(-5*sc,-4*sc,30*sc,10*sc);
      ctx.fillStyle='#22334d';ctx.fillRect(20*sc,-8*sc,10*sc,18*sc);
      ctx.fillStyle='#556677';ctx.fillRect(-8*sc,0,5*sc,8*sc);
      if(Math.sin(atkPhase)>0.7){
        ctx.fillStyle='rgba(255,240,100,.7)';ctx.shadowColor='#ffcc00';ctx.shadowBlur=20;
        ctx.beginPath();ctx.arc(30*sc,-4*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
      }
      break;
    case 'scythe':
      ctx.fillStyle='#334422';ctx.fillRect(-2.5*sc,-40*sc,5*sc,60*sc);
      ctx.strokeStyle='#556644';ctx.lineWidth=4*sc;
      ctx.beginPath();ctx.arc(-10*sc,-30*sc,25*sc,-Math.PI*.2,Math.PI*.4);ctx.stroke();
      ctx.strokeStyle='rgba(100,255,100,.4)';ctx.lineWidth=2*sc;
      ctx.beginPath();ctx.arc(-10*sc,-30*sc,25*sc,-Math.PI*.2,Math.PI*.2);ctx.stroke();
      break;
    case 'dual':
      ctx.fillStyle=PAL.swordBlade;
      ctx.save();ctx.rotate(-.3);
      ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-22*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();
      ctx.restore();
      ctx.save();ctx.rotate(.3);ctx.translate(10*sc,0);
      ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-22*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();
      ctx.restore();
      break;
    case 'hammer':
      ctx.fillStyle='#665544';ctx.fillRect(-3.5*sc,-10*sc,7*sc,40*sc);
      ctx.fillStyle='#998877';ctx.fillRect(-14*sc,-20*sc,28*sc,20*sc);
      ctx.fillStyle='rgba(255,200,100,.2)';ctx.fillRect(-12*sc,-18*sc,24*sc,8*sc);
      break;
  }
  ctx.shadowBlur=0;
  ctx.restore();
}

function drawOffhand(ctx, item, sc){
  ctx.save();
  ctx.rotate(Math.PI*.1);
  switch(item){
    case 'shield':
      ctx.fillStyle='#334455';
      ctx.beginPath();ctx.roundRect(-8*sc,0,16*sc,20*sc,3*sc);ctx.fill();
      ctx.strokeStyle='#445566';ctx.lineWidth=2*sc;ctx.stroke();
      ctx.fillStyle='rgba(100,150,220,.3)';ctx.beginPath();ctx.arc(0,10*sc,5*sc,0,Math.PI*2);ctx.fill();
      break;
    case 'dagger':
      ctx.fillStyle='#aabbcc';
      ctx.beginPath();ctx.moveTo(-1*sc,0);ctx.lineTo(0,-16*sc);ctx.lineTo(1*sc,0);ctx.closePath();ctx.fill();
      break;
    case 'tome':
      ctx.fillStyle='#442244';ctx.fillRect(-7*sc,0,14*sc,18*sc);
      ctx.fillStyle='rgba(200,100,255,.5)';ctx.fillRect(-5*sc,2*sc,10*sc,14*sc);
      break;
    case 'quiver':
      ctx.fillStyle='#664422';ctx.fillRect(-4*sc,0,8*sc,20*sc);
      for(let i=0;i<3;i++){
        ctx.fillStyle='#cc8822';ctx.fillRect(-2*sc+i*3*sc,0,2*sc,8*sc);
      }
      break;
  }
  ctx.restore();
}

function drawHeadDeco(ctx, deco, sc){
  switch(deco){
    case 'helm':
      ctx.fillStyle='#556677';
      ctx.beginPath();ctx.arc(0,-38*sc,14*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-14*sc,-38*sc,28*sc,5*sc);
      ctx.fillStyle='rgba(150,200,255,.3)';
      ctx.beginPath();ctx.arc(0,-38*sc,12*sc,Math.PI,Math.PI*2);ctx.fill();
      break;
    case 'wizard-hat':
      ctx.fillStyle='#441166';
      ctx.beginPath();ctx.moveTo(-12*sc,-28*sc);ctx.lineTo(0,-58*sc);ctx.lineTo(12*sc,-28*sc);ctx.closePath();ctx.fill();
      ctx.fillRect(-14*sc,-30*sc,28*sc,5*sc);
      ctx.fillStyle='rgba(200,100,255,.4)';
      ctx.beginPath();ctx.arc(0,-56*sc,3*sc,0,Math.PI*2);ctx.fill();
      break;
    case 'hood':
      ctx.fillStyle='#222233';
      ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillStyle='rgba(100,80,200,.3)';
      ctx.beginPath();ctx.arc(0,-38*sc,11*sc,Math.PI,Math.PI*2);ctx.fill();
      break;
    case 'cap':
      ctx.fillStyle='#334433';
      ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-14*sc,-40*sc,28*sc,6*sc);
      break;
    case 'headband':
      ctx.strokeStyle='#cc3322';ctx.lineWidth=4*sc;
      ctx.beginPath();ctx.arc(0,-36*sc,13*sc,Math.PI*1.1,Math.PI*1.9);ctx.stroke();
      break;
    case 'goggles':
      ctx.fillStyle='#333';ctx.fillRect(-10*sc,-40*sc,8*sc,5*sc);
      ctx.fillStyle='rgba(100,200,255,.5)';ctx.fillRect(-9*sc,-39*sc,6*sc,3*sc);
      ctx.fillRect(-2*sc,-40*sc,4*sc,5*sc);
      break;
    case 'crown':
      ctx.fillStyle='#cc8800';
      ctx.beginPath();
      ctx.moveTo(-12*sc,-38*sc);ctx.lineTo(-12*sc,-50*sc);ctx.lineTo(-6*sc,-44*sc);
      ctx.lineTo(0,-52*sc);ctx.lineTo(6*sc,-44*sc);ctx.lineTo(12*sc,-50*sc);ctx.lineTo(12*sc,-38*sc);
      ctx.closePath();ctx.fill();
      break;
  }
}

// ══════════════════════════════════════════════════════
// MONSTER DRAWING — LIMB-BASED
// ══════════════════════════════════════════════════════
function drawMonster(e, camX){
  const x=e.x-camX, y=e.y;
  const dead=!e.alive;
  const sc=e.drawScale||1;
  ctx.save();
  ctx.translate(x+e.w/2, y+e.h*.9);
  if(dead){ctx.globalAlpha=.3;ctx.rotate(e.f*Math.PI/2);}
  if(e.f===1) ctx.scale(-1,1);
  if(e.hitFlash>0) ctx.filter=`brightness(${3-e.hitFlash*.15})`;
  if(e.frozen>0) ctx.filter='hue-rotate(200deg) brightness(1.8) saturate(2)';

  const wp=e.walkPhase||0;
  const ap=e.atkPhase||0;

  // Call monster-specific draw
  const drawFn=MONSTER_DRAW[e.drawType]||drawMonster_basic;
  drawFn(ctx, sc, wp, ap, e);

  ctx.filter='none';
  ctx.restore();

  // HP bar
  if(!dead&&e.hp<e.maxHp){
    const hpPct=Math.max(0,e.hp/e.maxHp);
    const bw=Math.max(36,e.w+6), bx=x+e.w/2-bw/2, by=y-10;
    ctx.fillStyle='rgba(0,0,0,.6)';ctx.fillRect(bx,by,bw,5);
    ctx.fillStyle=hpPct>.5?'#22cc22':hpPct>.25?'#ccaa00':'#cc2200';
    ctx.fillRect(bx,by,bw*hpPct,5);
    if(e.frozen>0){
      ctx.fillStyle='rgba(100,180,255,.4)';ctx.fillRect(bx,by,bw,5);
    }
    if(e.burn>0){
      ctx.fillStyle='rgba(255,100,0,.3)';ctx.fillRect(bx,by,bw,5);
    }
  }
}

// Generic monster limb draw
function drawMonster_basic(ctx,sc,wp,ap,e){
  const bodyCol=e.bodyCol||'#556644';
  const headCol=e.headCol||'#667755';
  const limbCol=e.limbCol||'#445533';
  // Legs
  const ls=Math.sin(wp)*.4;
  for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
    ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
    ctx.strokeStyle=limbCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.restore();
  }
  // Arms
  const as=Math.sin(ap)*.6;
  ctx.save();ctx.translate(10*sc,-14*sc);ctx.rotate(-Math.PI/6+as);
  ctx.strokeStyle=limbCol;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  ctx.restore();
  ctx.save();ctx.translate(-10*sc,-14*sc);ctx.rotate(Math.PI/6-as);
  ctx.strokeStyle=limbCol;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
  ctx.restore();
  // Torso
  ctx.fillStyle=bodyCol;
  ctx.beginPath();ctx.roundRect(-10*sc,-28*sc,20*sc,28*sc,3*sc);ctx.fill();
  // Head
  ctx.fillStyle=headCol;
  ctx.beginPath();ctx.ellipse(0,-34*sc,11*sc,10*sc,0,0,Math.PI*2);ctx.fill();
  // Eyes (angry)
  ctx.fillStyle='#ff2200';
  ctx.beginPath();ctx.arc(-4*sc,-36*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(4*sc,-36*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff6600';
  ctx.beginPath();ctx.arc(-3*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(5*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
}

const MONSTER_DRAW = {
  goblin:(ctx,sc,wp,ap,e)=>{
    // Goblin: small green, big ears, dagger
    const lc=e.limbCol||'#22aa44';
    const bc=e.bodyCol||'#338855';
    const hc=e.headCol||'#22aa33';
    const ls=Math.sin(wp)*.5;
    for(const [ox,side] of [[-3*sc,-1],[3*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
      ctx.restore();
    }
    const as=Math.sin(ap)*.7;
    ctx.save();ctx.translate(8*sc,-10*sc);ctx.rotate(-Math.PI/6+as);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    // Dagger
    ctx.translate(0,12*sc);ctx.rotate(.2);
    ctx.fillStyle='#aabbcc';
    ctx.beginPath();ctx.moveTo(-1*sc,0);ctx.lineTo(0,-14*sc);ctx.lineTo(1*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-8*sc,-10*sc);ctx.rotate(Math.PI/6-as);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    ctx.restore();
    // Torso
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-8*sc,-22*sc,16*sc,22*sc,3*sc);ctx.fill();
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-26*sc,10*sc,9*sc,0,0,Math.PI*2);ctx.fill();
    // Ears
    ctx.fillStyle=hc;
    ctx.beginPath();ctx.ellipse(-12*sc,-26*sc,5*sc,3*sc,-Math.PI/4,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(12*sc,-26*sc,5*sc,3*sc,Math.PI/4,0,Math.PI*2);ctx.fill();
    // Eyes
    ctx.fillStyle='#ffcc00';
    ctx.beginPath();ctx.arc(-3*sc,-28*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(3*sc,-28*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#440000';
    ctx.beginPath();ctx.arc(-2*sc,-28*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-28*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    // Teeth
    ctx.fillStyle='#fff';ctx.fillRect(-3*sc,-22*sc,2*sc,3*sc);ctx.fillRect(1*sc,-22*sc,2*sc,3*sc);
  },

  skeleton:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.4;
    const as=Math.sin(ap)*.7;
    const bc='#d4c8a0';const lc='#c4b888';
    // Leg bones
    for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=4*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
      // Knee joint
      ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,10*sc,3*sc,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.moveTo(0,10*sc);ctx.lineTo(0,16*sc);ctx.stroke();
      ctx.restore();
    }
    // Ribcage
    ctx.strokeStyle=bc;ctx.lineWidth=2*sc;
    for(let i=0;i<4;i++){
      ctx.beginPath();ctx.arc(0,(-8-i*5)*sc,8*sc,0,Math.PI);ctx.stroke();
    }
    ctx.strokeStyle=bc;ctx.lineWidth=3*sc;
    ctx.beginPath();ctx.moveTo(0,-8*sc);ctx.lineTo(0,-28*sc);ctx.stroke(); // spine
    // Arms
    ctx.save();ctx.translate(10*sc,-22*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.translate(0,14*sc);ctx.rotate(.2+as*.3);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    // Sword
    ctx.translate(0,12*sc);ctx.rotate(-Math.PI/6);
    ctx.fillStyle='#ddd';ctx.beginPath();ctx.moveTo(-1.5*sc,0);ctx.lineTo(0,-24*sc);ctx.lineTo(1.5*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-22*sc);ctx.rotate(Math.PI/5-as);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.translate(0,14*sc);ctx.rotate(-.2);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();
    ctx.restore();
    // Skull
    ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,-34*sc,11*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=bc;ctx.fillRect(-8*sc,-26*sc,16*sc,6*sc); // jaw
    // Eye sockets
    ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(-4*sc,-36*sc,3.5*sc,3*sc,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(4*sc,-36*sc,3.5*sc,3*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(0,200,255,.5)';ctx.beginPath();ctx.arc(-4*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-36*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    // Teeth marks on jaw
    ctx.fillStyle='#111';
    for(let t=-3;t<=3;t++) ctx.fillRect((t*2.5-1)*sc,-25*sc,2*sc,4*sc);
  },

  orc:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.35;
    const as=Math.sin(ap)*.6;
    const bc='#3a5a2a';const lc='#2a4a1a';const hc='#4a6a3a';
    // Big muscular legs
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.lineWidth=8*sc;ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,30*sc);ctx.stroke();
      ctx.restore();
    }
    // Arms (big)
    ctx.save();ctx.translate(14*sc,-20*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.2+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    // Axe
    ctx.fillStyle='#666';ctx.fillRect(-3*sc,0,6*sc,8*sc);
    ctx.fillStyle='#888';
    ctx.beginPath();ctx.moveTo(-2*sc,6*sc);ctx.lineTo(-20*sc,-8*sc);ctx.lineTo(-20*sc,12*sc);ctx.lineTo(-2*sc,24*sc);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-14*sc,-20*sc);ctx.rotate(Math.PI/5-as);
    ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,20*sc);ctx.stroke();
    ctx.restore();
    // Muscular torso
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-14*sc,-36*sc,28*sc,36*sc,4*sc);ctx.fill();
    // Armor plates
    ctx.fillStyle='#445533';ctx.fillRect(-12*sc,-30*sc,24*sc,12*sc);
    ctx.strokeStyle='#556644';ctx.lineWidth=1.5*sc;
    ctx.beginPath();ctx.moveTo(0,-36*sc);ctx.lineTo(0,-0*sc);ctx.stroke();
    // Head (big)
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-42*sc,14*sc,12*sc,0,0,Math.PI*2);ctx.fill();
    // Tusks
    ctx.fillStyle='#ddd';
    ctx.beginPath();ctx.moveTo(-6*sc,-34*sc);ctx.lineTo(-10*sc,-26*sc);ctx.lineTo(-4*sc,-34*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(6*sc,-34*sc);ctx.lineTo(10*sc,-26*sc);ctx.lineTo(4*sc,-34*sc);ctx.fill();
    // Eyes (red)
    ctx.fillStyle='#ff2200';ctx.beginPath();ctx.arc(-5*sc,-44*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-44*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    // Mohawk
    ctx.fillStyle='#cc2200';ctx.fillRect(-2*sc,-56*sc,4*sc,16*sc);
  },

  mage_enemy:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.3;
    const as=Math.sin(ap)*.5;
    const bc='#2a1a4a';const lc='#3a2a5a';const hc='#3a2a6a';
    // Robes (no legs visible much)
    ctx.fillStyle=bc;ctx.beginPath();ctx.moveTo(-14*sc,0);ctx.lineTo(14*sc,0);ctx.lineTo(10*sc,-44*sc);ctx.lineTo(-10*sc,-44*sc);ctx.closePath();ctx.fill();
    // Robe trim
    ctx.strokeStyle='rgba(150,100,255,.5)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-14*sc,0);ctx.lineTo(-10*sc,-44*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(14*sc,0);ctx.lineTo(10*sc,-44*sc);ctx.stroke();
    // Arms
    ctx.save();ctx.translate(10*sc,-30*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.translate(0,16*sc);
    // Staff
    ctx.fillStyle='#7733aa';ctx.fillRect(-2*sc,0,4*sc,-30*sc);
    ctx.fillStyle='rgba(200,100,255,.9)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=15;
    ctx.beginPath();ctx.arc(0,-30*sc,7*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-30*sc);ctx.rotate(Math.PI/4-as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.restore();
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.arc(0,-50*sc,11*sc,0,Math.PI*2);ctx.fill();
    // Wizard hat
    ctx.fillStyle='#330066';
    ctx.beginPath();ctx.moveTo(-13*sc,-44*sc);ctx.lineTo(0,-68*sc);ctx.lineTo(13*sc,-44*sc);ctx.closePath();ctx.fill();
    ctx.fillRect(-15*sc,-46*sc,30*sc,5*sc);
    ctx.fillStyle='rgba(180,80,255,.6)';ctx.beginPath();ctx.arc(0,-66*sc,3*sc,0,Math.PI*2);ctx.fill();
    // Glowing eyes
    ctx.fillStyle='rgba(200,100,255,.9)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(-4*sc,-51*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-51*sc,3*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },

  zombie:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.2;
    const as=Math.sin(ap)*.4;
    const bc='#3d5a30';const lc='#2d4a22';const hc='#4d5a38';
    for(const [ox,side] of [[-5*sc,-1],[5*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side*.5);
      ctx.strokeStyle=lc;ctx.lineWidth=6*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,16*sc);ctx.lineTo(3*sc,28*sc);ctx.stroke();
      ctx.restore();
    }
    // Outstretched arms (zombie pose)
    ctx.save();ctx.translate(10*sc,-18*sc);ctx.rotate(-Math.PI*.6+as);
    ctx.strokeStyle=lc;ctx.lineWidth=6*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,16*sc);ctx.lineTo(0,28*sc);ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-18*sc);ctx.rotate(-Math.PI*.5+as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=6*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(0,14*sc);ctx.lineTo(2*sc,24*sc);ctx.stroke();
    ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-10*sc,-30*sc,20*sc,30*sc,3*sc);ctx.fill();
    // Torn clothes effect
    ctx.strokeStyle='rgba(0,0,0,.3)';ctx.lineWidth=1.5*sc;
    for(let i=0;i<3;i++) ctx.beginPath(),ctx.moveTo(-8*sc+i*6*sc,-28*sc),ctx.lineTo(-6*sc+i*6*sc,-8*sc),ctx.stroke();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-35*sc,11*sc,10*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#112211';ctx.beginPath();ctx.arc(-4*sc,-37*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-37*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#22cc22';ctx.beginPath();ctx.arc(-3*sc,-37*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-37*sc,2*sc,0,Math.PI*2);ctx.fill();
    // Blood splatters
    ctx.fillStyle='rgba(150,0,0,.6)';
    ctx.beginPath();ctx.arc(-5*sc,-25*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(6*sc,-18*sc,2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(-2*sc,-38*sc,1.5*sc,0,Math.PI*2);ctx.fill();
  },

  dragon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.25;
    const as=Math.sin(ap)*.5;
    const bc='#1a3a1a';const sc2='#2a5a2a';const hc='#1a4a1a';
    // Tail
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(15*sc,-10*sc);ctx.quadraticCurveTo(40*sc,10*sc,30*sc,-20*sc);ctx.stroke();
    ctx.lineWidth=4*sc;
    ctx.beginPath();ctx.moveTo(30*sc,-20*sc);ctx.lineTo(40*sc,-15*sc);ctx.stroke();
    // Wings
    ctx.fillStyle='rgba(30,60,30,.7)';
    ctx.beginPath();ctx.moveTo(-5*sc,-35*sc);ctx.lineTo(-40*sc,-60*sc);ctx.lineTo(-35*sc,-20*sc);ctx.lineTo(-5*sc,-15*sc);ctx.closePath();ctx.fill();
    ctx.strokeStyle='rgba(60,100,60,.5)';ctx.lineWidth=1*sc;ctx.stroke();
    // Legs
    for(const [ox,side] of [[-7*sc,-1],[7*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      // Claws
      ctx.strokeStyle='#aaa';ctx.lineWidth=2*sc;
      for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,18*sc),ctx.lineTo(c*6*sc,26*sc),ctx.stroke();
      ctx.restore();
    }
    // Arms/Claws
    ctx.save();ctx.translate(14*sc,-24*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.strokeStyle='#aaa';ctx.lineWidth=2*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,16*sc),ctx.lineTo(c*7*sc,24*sc),ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-14*sc,-24*sc);ctx.rotate(Math.PI/4-as);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.restore();
    // Body
    ctx.fillStyle=bc;ctx.beginPath();ctx.ellipse(0,-20*sc,16*sc,22*sc,0,0,Math.PI*2);ctx.fill();
    // Scales
    ctx.fillStyle=sc2;
    for(let i=0;i<3;i++) ctx.beginPath(),ctx.arc(0,(-30+i*8)*sc,6*sc,0,Math.PI*2),ctx.fill();
    // Neck
    ctx.fillStyle=bc;ctx.fillRect(-7*sc,-42*sc,14*sc,14*sc);
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-50*sc,14*sc,12*sc,-.3,0,Math.PI*2);ctx.fill();
    // Snout
    ctx.beginPath();ctx.ellipse(8*sc,-48*sc,8*sc,5*sc,-.2,0,Math.PI*2);ctx.fill();
    // Nostril fire
    if(ap>0.5){
      ctx.fillStyle='rgba(255,150,0,.8)';ctx.shadowColor='#ff6600';ctx.shadowBlur=15;
      ctx.beginPath();ctx.arc(14*sc,-48*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    }
    // Eyes
    ctx.fillStyle='#ffaa00';ctx.beginPath();ctx.ellipse(-4*sc,-54*sc,4*sc,3*sc,.3,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(-3*sc,-54*sc,2*sc,2*sc,.3,0,Math.PI*2);ctx.fill();
    // Horns
    ctx.fillStyle='#888';ctx.strokeStyle='#888';ctx.lineWidth=3*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(-8*sc,-58*sc);ctx.lineTo(-12*sc,-70*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-2*sc,-60*sc);ctx.lineTo(-4*sc,-72*sc);ctx.stroke();
  },

  demon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.3;const as=Math.sin(ap)*.6;
    const bc='#4a0a0a';const lc='#3a0808';const hc='#550a0a';
    // Legs
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,28*sc);ctx.stroke();
      // Hoof
      ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(2*sc,28*sc,5*sc,4*sc,0,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
    // Wings
    ctx.fillStyle='rgba(80,0,0,.8)';
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(-45*sc,-55*sc);ctx.lineTo(-30*sc,-10*sc);ctx.lineTo(-5*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(45*sc,-55*sc);ctx.lineTo(30*sc,-10*sc);ctx.lineTo(5*sc,-10*sc);ctx.closePath();ctx.fill();
    // Arms
    ctx.save();ctx.translate(12*sc,-22*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.3+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    // Claws
    ctx.strokeStyle='#ff2200';ctx.lineWidth=2*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*3*sc,14*sc),ctx.lineTo(c*6*sc,22*sc),ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-12*sc,-22*sc);ctx.rotate(Math.PI/4-as);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-12*sc,-38*sc,24*sc,38*sc,4*sc);ctx.fill();
    ctx.fillStyle='rgba(255,0,0,.15)';ctx.beginPath();ctx.arc(0,-20*sc,10*sc,0,Math.PI*2);ctx.fill();
    // Head
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-46*sc,13*sc,12*sc,0,0,Math.PI*2);ctx.fill();
    // Horns
    ctx.fillStyle='#660000';
    ctx.beginPath();ctx.moveTo(-8*sc,-54*sc);ctx.lineTo(-14*sc,-70*sc);ctx.lineTo(-4*sc,-56*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(8*sc,-54*sc);ctx.lineTo(14*sc,-70*sc);ctx.lineTo(4*sc,-56*sc);ctx.fill();
    ctx.fillStyle='#ff0000';ctx.shadowColor='#ff0000';ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(-4*sc,-48*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-48*sc,3.5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },

  golem:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.15;const as=Math.sin(ap)*.4;
    const bc='#6a5a4a';const lc='#7a6a5a';const hc='#8a7a6a';
    // Stone legs (wide)
    for(const [ox,side] of [[-8*sc,-1],[8*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.fillStyle=bc;ctx.fillRect(-6*sc,-2*sc,12*sc,22*sc);
      ctx.fillStyle=lc;ctx.fillRect(-4*sc,0,8*sc,5*sc);
      ctx.restore();
    }
    // Arms (huge blocks)
    ctx.save();ctx.translate(18*sc,-26*sc);ctx.rotate(-Math.PI/6+as);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,24*sc);
    ctx.fillRect(-5*sc,24*sc,14*sc,18*sc); // fist
    ctx.restore();
    ctx.save();ctx.translate(-18*sc,-26*sc);ctx.rotate(Math.PI/6-as);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,24*sc);
    ctx.fillRect(-9*sc,24*sc,14*sc,18*sc);
    ctx.restore();
    // Torso (large rectangle)
    ctx.fillStyle=bc;ctx.fillRect(-18*sc,-44*sc,36*sc,44*sc);
    // Cracks
    ctx.strokeStyle='rgba(0,0,0,.4)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-5*sc,-40*sc);ctx.lineTo(2*sc,-20*sc);ctx.lineTo(-3*sc,-10*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(8*sc,-35*sc);ctx.lineTo(12*sc,-15*sc);ctx.stroke();
    // Glowing core
    ctx.fillStyle='rgba(255,150,0,.6)';ctx.shadowColor='#ff8800';ctx.shadowBlur=20;
    ctx.beginPath();ctx.arc(0,-22*sc,6*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Head (box)
    ctx.fillStyle=hc;ctx.fillRect(-14*sc,-62*sc,28*sc,22*sc);
    ctx.fillStyle='rgba(0,0,0,.4)';ctx.fillRect(-10*sc,-58*sc,8*sc,10*sc);ctx.fillRect(2*sc,-58*sc,8*sc,10*sc);
    ctx.fillStyle='rgba(255,180,50,.8)';ctx.shadowColor='#ffaa00';ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(-6*sc,-53*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(6*sc,-53*sc,3*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },

  lich:(ctx,sc,wp,ap,e)=>{
    const as=Math.sin(ap)*.5;
    const bc='#1a1a3a';const lc='#2a2a4a';const hc='#222240';
    // Floating robe
    const float=Math.sin(Date.now()*.002)*4;
    ctx.fillStyle=bc;
    ctx.beginPath();ctx.moveTo(-14*sc,-8*sc+float);ctx.lineTo(14*sc,-8*sc+float);
    ctx.lineTo(18*sc,6*sc+float);ctx.lineTo(-18*sc,6*sc+float);ctx.closePath();ctx.fill();
    // Robe bottom wisps
    ctx.strokeStyle='rgba(100,100,220,.4)';ctx.lineWidth=3*sc;
    for(let i=-2;i<=2;i++){
      ctx.beginPath();ctx.moveTo(i*7*sc,6*sc+float);
      ctx.quadraticCurveTo(i*8*sc+Math.sin(Date.now()*.003+i)*4,20*sc+float,i*6*sc,28*sc+float);
      ctx.stroke();
    }
    ctx.fillStyle=bc;ctx.fillRect(-12*sc,-44*sc+float,24*sc,36*sc);
    // Arms with orbs
    ctx.save();ctx.translate(12*sc,-30*sc+float);ctx.rotate(-Math.PI/3+as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
    ctx.translate(0,18*sc);ctx.rotate(.3+as*.5);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,14*sc);ctx.stroke();
    ctx.fillStyle='rgba(100,100,255,.8)';ctx.shadowColor='#4444ff';ctx.shadowBlur=15;
    ctx.beginPath();ctx.arc(0,14*sc,7*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.restore();
    ctx.save();ctx.translate(-12*sc,-30*sc+float);ctx.rotate(Math.PI/3-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.restore();
    // Skull head
    ctx.fillStyle='#d4c8a0';ctx.beginPath();ctx.arc(0,-52*sc+float,13*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#c4b888';ctx.fillRect(-9*sc,-44*sc+float,18*sc,6*sc);
    ctx.fillStyle='rgba(100,100,255,.9)';ctx.shadowColor='#6666ff';ctx.shadowBlur=12;
    ctx.beginPath();ctx.ellipse(-4*sc,-54*sc+float,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(4*sc,-54*sc+float,4*sc,3.5*sc,0,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    // Crown of bones
    ctx.fillStyle='#b8ac88';
    for(let i=-2;i<=2;i++) ctx.fillRect(i*5*sc-1.5*sc,-66*sc+float,3*sc,10*sc);
  },
};

// ══════════════════════════════════════════════════════
// CHARACTER CLASS DEFINITIONS (8 classes)
// ══════════════════════════════════════════════════════
const CLASSES = {
  warrior:{
    name:'워리어',role:'근접 전사',icon:'⚔️',
    skinCol:PAL.skin1,hairCol:PAL.hair1,torsoCol:'#3a4455',legsCol:'#2a3344',
    headDeco:'helm',weapon:'sword',offhand:'shield',
    hp:380,mp:80,atk:42,def:16,spd:4.6,jmp:12.5,
    desc:'높은 HP·DEF. 방패 방어로 피해 감소.',
    stars:{ATK:4,DEF:5,SPD:3,RANGE:2,MAGIC:1},
    col:'#5588cc',
    skills:[
      {name:'검격',icon:'⚔️',key:'A',mp:10,cd:2,desc:'강력한 검 공격 1.8배',col:'#aabbcc',
       fn:(p,G)=>{hitAOE(p.x+(p.f>0?p.w:(-75)),p.y-15,80,70,dmg(p,1.8),true);}},
      {name:'방패 강타',icon:'🛡️',key:'S',mp:18,cd:4,desc:'방패 충격 스턴+1.3배',col:'#8899aa',
       fn:(p,G)=>{p.vx=p.f*20;setTimeout(()=>hitAOE(p.x+(p.f>0?p.w:-80),p.y-5,80,60,dmg(p,1.3),true,{stun:100}),140);}},
      {name:'돌격',icon:'💨',key:'D',mp:24,cd:5,desc:'돌진 후 강타 2.2배',col:'#ccdde0',
       fn:(p,G)=>{p.vx=p.f*36;p.invincible=35;setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w-10:-90),p.y-20,110,80,dmg(p,2.2),true);boom(p.x+(p.f>0?p.w+40:-40),p.y+10,'#aabbcc');shake(5,12);},200);}},
      {name:'회오리',icon:'🌀',key:'F',mp:38,cd:7,desc:'360도 광역 2배',col:'#99aabb',
       fn:(p,G)=>{hitAOE(p.x-70,p.y-40,p.w+140,p.h+80,dmg(p,2),false);shake(4,10);}},
      {name:'무적 베기',icon:'🗡️',key:'G',mp:65,cd:16,desc:'5초 무적+자힐+3배',col:'#eeffff',
       fn:(p,G)=>{p.invincible=300;p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.2));hitAOE(p.x-60,p.y-50,p.w+130,120,dmg(p,3),true);shake(8,20);}},
    ]
  },
  mage:{
    name:'마법사',role:'원소 마법사',icon:'🔮',
    skinCol:PAL.skin3,hairCol:PAL.hair1,torsoCol:'#331155',legsCol:'#220f44',
    headDeco:'wizard-hat',weapon:'staff',offhand:'tome',
    hp:210,mp:280,atk:60,def:5,spd:4.0,jmp:12.0,
    desc:'강력한 마법. MP관리 필수.',
    stars:{ATK:5,DEF:1,SPD:3,RANGE:5,MAGIC:5},
    col:'#aa44ff',
    skills:[
      {name:'파이어볼',icon:'🔥',key:'A',mp:20,cd:1.5,desc:'화염탄 3발',col:'#ff6600',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>proj(p.x+p.f*50,p.y+20,p.f*16,(Math.random()-.5)*.5,dmg(p,1.7),'#ff6600','player',{sz:13,emoji:'🔥',life:60,trail:true}),i*90);}},
      {name:'아이스 스피어',icon:'❄️',key:'S',mp:28,cd:4,desc:'빙결 마법구',col:'#44aaff',
       fn:(p,G)=>{proj(p.x+p.f*50,p.y+18,p.f*14,0,dmg(p,2.3),'#44aaff','player',{sz:14,emoji:'❄️',life:70,onHit:(e)=>{e.frozen=Math.max(e.frozen||0,180);}});}},
      {name:'라이트닝',icon:'⚡',key:'D',mp:36,cd:5,desc:'낙뢰 3연격',col:'#ffee00',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>{const tx=p.x+p.f*(140+i*90);proj(tx,-30,0,22,dmg(p,2.2),'#ffee00','player',{sz:18,emoji:'⚡',life:30,grav:.6});spawnParts(tx,70,{n:8,col:['#ffee00','#ffdd44'],glow:true,spread:.4,dir:Math.PI*.5,sMin:4,sMax:10});},i*180);}},
      {name:'메테오',icon:'☄️',key:'F',mp:72,cd:12,desc:'5개 운석 낙하 3.5배',col:'#ff4400',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>{const tx=p.x+p.f*100+(Math.random()-.5)*280;proj(tx,-60,(Math.random()-.5)*2,18,dmg(p,3.5),'#ff4400','player',{sz:24,emoji:'☄️',life:72,grav:.35});shake(4,9);},i*160);}},
      {name:'타임스탑',icon:'⏰',key:'G',mp:90,cd:22,desc:'4초 전체 빙결',col:'#8844ff',
       fn:(p,G)=>{freezeAll(200);}},
    ]
  },
  rogue:{
    name:'로그',role:'암살자',icon:'🗝️',
    skinCol:PAL.skin2,hairCol:PAL.hair1,torsoCol:'#1a2a1a',legsCol:'#111a11',
    headDeco:'hood',weapon:'dual',offhand:'dagger',
    hp:250,mp:190,atk:54,def:7,spd:5.8,jmp:15.5,
    desc:'초고속 이동, 크리+25%, 연속 참격.',
    stars:{ATK:5,DEF:1,SPD:5,RANGE:3,MAGIC:3},
    col:'#22cc55',
    skills:[
      {name:'3연참',icon:'🗡️',key:'A',mp:12,cd:1.5,desc:'초속 3연타 크리보정+',col:'#44ee66',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>hitAOE(p.x+(p.f>0?p.w:-70),p.y-10,70,60,dmg(p,1.5),Math.random()<.35),i*100);}},
      {name:'수리검',icon:'✴️',key:'S',mp:20,cd:3,desc:'4방향 수리검 투척',col:'#aaffaa',
       fn:(p,G)=>{[-6,-2,2,6].forEach(vy=>proj(p.x+p.f*50,p.y+25,p.f*18,vy,dmg(p,1.6),'#22dd44','player',{sz:9,emoji:'✴️',life:70}));}},
      {name:'순간이동',icon:'💨',key:'D',mp:18,cd:3.5,desc:'텔레포트+폭풍 참격',col:'#aa44cc',
       fn:(p,G)=>{spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:15,col:['#22cc44','#88ff88'],grav:0,sMin:2,sMax:6});p.x+=p.f*190;setTimeout(()=>{hitAOE(p.x+(p.f>0?p.w:-90),p.y-20,100,80,dmg(p,2.6),true);},80);}},
      {name:'독 단검',icon:'☠️',key:'F',mp:35,cd:7,desc:'독 지속 피해',col:'#44cc44',
       fn:(p,G)=>{proj(p.x+p.f*50,p.y+22,p.f*17,-2,dmg(p,1.8),'#44cc44','player',{sz:12,emoji:'🗡️',life:80,onHit:(e)=>{e.poison=Math.max(e.poison||0,300);e.poisonDmg=Math.round(p.atk*.4);}});}},
      {name:'죽음의 무도',icon:'💀',key:'G',mp:80,cd:18,desc:'6방향 폭격+5초 무적',col:'#222244',
       fn:(p,G)=>{p.invincible=300;for(let i=0;i<6;i++){const a=i/6*Math.PI*2;hitAOE(p.x+Math.cos(a)*80-50,p.y+Math.sin(a)*60-30,100,80,dmg(p,3.5),true);}shake(12,30);}},
    ]
  },
  gunner:{
    name:'건너',role:'전술 사수',icon:'🔫',
    skinCol:PAL.skin1,hairCol:PAL.hair3,torsoCol:'#1a3322',legsCol:'#112211',
    headDeco:'cap',weapon:'gun',offhand:'quiver',
    hp:270,mp:170,atk:48,def:8,spd:5.2,jmp:14.0,
    desc:'연사 특화. 저격, 미사일, 탄막.',
    stars:{ATK:4,DEF:2,SPD:5,RANGE:5,MAGIC:2},
    col:'#44cc88',
    skills:[
      {name:'연사',icon:'🔫',key:'A',mp:12,cd:1.2,desc:'5연발',col:'#44cc88',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>proj(p.x+p.f*54,p.y+24,p.f*22+(Math.random()-.5)*1.5,(Math.random()-.5)*1.5,dmg(p,1.0),'#44cc88','player',{sz:7,life:68}),i*50);}},
      {name:'유탄',icon:'💣',key:'S',mp:22,cd:4,desc:'폭발 유탄 광역',col:'#ffcc00',
       fn:(p,G)=>{proj(p.x+p.f*46,p.y+22,p.f*10,-8,dmg(p,3.0),'#ffcc00','player',{sz:17,emoji:'💣',life:90,grav:.42,explode:true});}},
      {name:'저격',icon:'🎯',key:'D',mp:30,cd:5.5,desc:'관통 저격 4.5배',col:'#88ff44',
       fn:(p,G)=>{proj(p.x+p.f*52,p.y+24,p.f*36,0,dmg(p,4.5),'#88ff44','player',{sz:10,life:110,pierce:true});shake(2,5);}},
      {name:'미사일',icon:'🚀',key:'F',mp:45,cd:9,desc:'5연 추적 미사일',col:'#ff8800',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>proj(p.x+p.f*40,p.y+14+i*6,p.f*9+(Math.random()-.5)*3,-8+(Math.random()-.5)*3,dmg(p,2.1),'#ff8800','player',{sz:15,emoji:'🚀',life:100,grav:.06,homing:true}),i*90);}},
      {name:'탄막',icon:'🌟',key:'G',mp:85,cd:20,desc:'전방향 탄막 72발',col:'#44ffaa',
       fn:(p,G)=>{for(let i=0;i<18;i++)setTimeout(()=>{const a=i/18*Math.PI*2;proj(p.x+p.w/2,p.y+p.h/2,Math.cos(a)*17,Math.sin(a)*14,dmg(p,1.3),'#44ffaa','player',{sz:8,life:65,pierce:true});},i*55);shake(6,18);}},
    ]
  },
  berserker:{
    name:'버서커',role:'광전사',icon:'💢',
    skinCol:PAL.skin2,hairCol:PAL.hair2,torsoCol:'#4a1010',legsCol:'#3a0808',
    headDeco:'headband',weapon:'axe',offhand:'shield',
    hp:340,mp:60,atk:62,def:8,spd:5.0,jmp:13.0,
    desc:'ATK 극대화. HP↓ = ATK↑↑',
    stars:{ATK:5,DEF:3,SPD:4,RANGE:2,MAGIC:1},
    col:'#ff3322',
    skills:[
      {name:'분노 강타',icon:'💢',key:'A',mp:0,cd:2,desc:'2배+자신HP-8',col:'#ff4422',
       fn:(p,G)=>{const d=dmg(p,2.0+(1-p.hp/p.maxHp));p.hp=Math.max(1,p.hp-8);hitAOE(p.x+(p.f>0?p.w:-80),p.y-10,85,70,d,true);}},
      {name:'피의 갈망',icon:'🩸',key:'S',mp:0,cd:5,desc:'1.6배+피흡 50%',col:'#cc0000',
       fn:(p,G)=>{const d=dmg(p,1.6);hitAOE(p.x+(p.f>0?p.w:-80),p.y-10,85,70,d,false,{lifeSteal:0.5});}},
      {name:'광란',icon:'🌋',key:'D',mp:20,cd:8,desc:'ATK+20(5턴)-HP20',col:'#ff8800',
       fn:(p,G)=>{p.hp=Math.max(1,p.hp-20);p.buffAtk=(p.buffAtk||1)*1.6;p.buffTimer=Math.max(p.buffTimer||0,300);shake(4,10);}},
      {name:'지진',icon:'💥',key:'F',mp:40,cd:9,desc:'전방 지진파 3배',col:'#cc2200',
       fn:(p,G)=>{setTimeout(()=>{hitAOE(p.x-80,p.y,220,GY()-p.y,dmg(p,3),true);boom(p.x,p.y+p.h,'#ff4422',2.5);shake(9,22);},250);}},
      {name:'최후의 일격',icon:'🏴',key:'G',mp:0,cd:12,desc:'HP낮을수록 초강타 5~12배',col:'#220000',
       fn:(p,G)=>{const mult=5+(1-p.hp/p.maxHp)*7;hitAOE(p.x+(p.f>0?p.w-10:-120),p.y-50,160,120,dmg(p,mult),true);boom(p.x+(p.f>0?p.w+40:-40),p.y,'#ff2200',3);shake(12,30);}},
    ]
  },
  paladin:{
    name:'팔라딘',role:'성기사',icon:'✨',
    skinCol:PAL.skin1,hairCol:PAL.hair3,torsoCol:'#44556a',legsCol:'#334455',
    headDeco:'helm',weapon:'hammer',offhand:'shield',
    hp:520,mp:120,atk:36,def:28,spd:3.8,jmp:11.0,
    desc:'최고 생존력. 힐+재생+신성 폭발.',
    stars:{ATK:3,DEF:5,SPD:2,RANGE:2,MAGIC:4},
    col:'#eeddaa',
    skills:[
      {name:'망치 강타',icon:'🔨',key:'A',mp:12,cd:2,desc:'망치 1.7배+스턴',col:'#ccd0d4',
       fn:(p,G)=>{hitAOE(p.x+(p.f>0?p.w:-90),p.y-10,90,70,dmg(p,1.7),false,{stun:90});}},
      {name:'신성한 빛',icon:'💛',key:'S',mp:20,cd:4,desc:'HP 30% 회복',col:'#ffffaa',
       fn:(p,G)=>{const h=Math.round(p.maxHp*.30);p.hp=Math.min(p.maxHp,p.hp+h);spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:20,col:['#ffff88','#ffffff'],glow:true,upb:4,sMin:2,sMax:7});}},
      {name:'신성화',icon:'🔆',key:'D',mp:35,cd:7,desc:'광역 30피해',col:'#ffff88',
       fn:(p,G)=>{hitAll(dmg(p,1.5),true);}},
      {name:'신성 방패',icon:'🌟',key:'F',mp:40,cd:9,desc:'4초 무적',col:'#aaddff',
       fn:(p,G)=>{p.invincible=240;spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:25,col:['#aaddff','#ffffff'],glow:true,sMin:3,sMax:8,grav:-.01});}},
      {name:'성광 폭발',icon:'💥',key:'G',mp:80,cd:16,desc:'전체 50피해+자힐 40%',col:'#ffffcc',
       fn:(p,G)=>{hitAll(dmg(p,2.5),true);p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.4));shake(10,25);}},
    ]
  },
  necromancer:{
    name:'네크로맨서',role:'소환사',icon:'💀',
    skinCol:'#c0c8d0',hairCol:'#000000',torsoCol:'#121820',legsCol:'#0a1018',
    headDeco:'crown',weapon:'scythe',offhand:'tome',
    hp:230,mp:260,atk:58,def:6,spd:4.2,jmp:12.5,
    desc:'암흑·소환. 저주로 적 약화.',
    stars:{ATK:5,DEF:1,SPD:3,RANGE:4,MAGIC:5},
    col:'#8833cc',
    skills:[
      {name:'암흑탄',icon:'💜',key:'A',mp:15,cd:2,desc:'암흑 마법 2배',col:'#8833cc',
       fn:(p,G)=>{proj(p.x+p.f*50,p.y+20,p.f*14,-1,dmg(p,2.0),'#8833cc','player',{sz:14,emoji:'🔮',life:65});}},
      {name:'생명 흡수',icon:'🖤',key:'S',mp:24,cd:4,desc:'30피해+자힐 20',col:'#440088',
       fn:(p,G)=>{proj(p.x+p.f*50,p.y+20,p.f*12,-1,dmg(p,1.5),'#440088','player',{sz:12,emoji:'🖤',life:60,onHit:(e)=>{p.hp=Math.min(p.maxHp,p.hp+20);}});}},
      {name:'저주',icon:'⛧',key:'D',mp:30,cd:6,desc:'전체 적 ATK-40% 4초',col:'#332244',
       fn:(p,G)=>{for(const e of G.enemies) if(e.alive) e.cursed=Math.max(e.cursed||0,240);if(G.boss&&G.boss.alive) G.boss.cursed=Math.max(G.boss.cursed||0,240);}},
      {name:'뼈 돌풍',icon:'🦴',key:'F',mp:50,cd:10,desc:'전체 광역 2.5배',col:'#ccbbaa',
       fn:(p,G)=>{hitAll(dmg(p,2.5),true);shake(6,14);}},
      {name:'죽음 폭발',icon:'☠️',key:'G',mp:90,cd:20,desc:'전체 5배 암흑 폭발',col:'#110022',
       fn:(p,G)=>{hitAll(dmg(p,5.0),true);shake(14,35);}},
    ]
  },
  monk:{
    name:'몽크',role:'격투가',icon:'🥊',
    skinCol:PAL.skin1,hairCol:'#000000',torsoCol:'#cc8833',legsCol:'#aa6622',
    headDeco:'goggles',weapon:'dual',offhand:'dagger',
    hp:300,mp:150,atk:46,def:12,spd:6.2,jmp:16.0,
    desc:'초고속 연타. 기(氣) 스킬 특화.',
    stars:{ATK:4,DEF:3,SPD:5,RANGE:3,MAGIC:3},
    col:'#ffaa22',
    skills:[
      {name:'연타',icon:'🥊',key:'A',mp:10,cd:1.5,desc:'5연속 0.7배',col:'#ffaa22',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>hitAOE(p.x+(p.f>0?p.w:-65),p.y-10,70,60,dmg(p,.7),i===4),i*90);}},
      {name:'기공파',icon:'🌀',key:'S',mp:20,cd:3,desc:'기 에너지 2.5배',col:'#ffcc44',
       fn:(p,G)=>{proj(p.x+p.f*50,p.y+20,p.f*16,0,dmg(p,2.5),'#ffcc44','player',{sz:16,emoji:'🌀',life:70});}},
      {name:'철갑',icon:'⛓️',key:'D',mp:15,cd:6,desc:'DEF+10 4초',col:'#888888',
       fn:(p,G)=>{p.defBuff=10;p.defBuffTimer=240;spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:15,col:['#888888','#aaaaaa'],glow:false,sMin:2,sMax:5});}},
      {name:'회오리',icon:'🌪️',key:'F',mp:35,cd:7,desc:'360도 3.5배',col:'#88ccff',
       fn:(p,G)=>{hitAOE(p.x-80,p.y-50,p.w+160,p.h+100,dmg(p,3.5),true);shake(5,12);}},
      {name:'내면의 평화',icon:'☮️',key:'G',mp:0,cd:10,desc:'HP 50%+MP 30 회복',col:'#ffffcc',
       fn:(p,G)=>{p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.5));p.mp=Math.min(p.maxMp,p.mp+30);spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:20,col:['#ffffcc','#ffffff'],glow:true,upb:3,sMin:2,sMax:6});}},
    ]
  },
};

// ══════════════════════════════════════════════════════
// ENEMY TYPES
// ══════════════════════════════════════════════════════
const ENEMIES = {
  goblin:   {name:'고블린',    drawType:'goblin',    w:34,h:40, hp:80,  atk:12,spd:3.0,xp:14,g:8,  bodyCol:'#33aa44',headCol:'#22aa33',limbCol:'#22aa44',drawScale:.95,ai:'chase'},
  orc:      {name:'오크',      drawType:'orc',       w:52,h:62, hp:200, atk:24,spd:1.9,xp:30,g:18, bodyCol:'#3a5a2a',headCol:'#4a6a3a',limbCol:'#2a4a1a',drawScale:1.3,ai:'brute'},
  skeleton: {name:'스켈레톤',  drawType:'skeleton',  w:38,h:52, hp:120, atk:17,spd:3.1,xp:22,g:14, bodyCol:'#d4c8a0',headCol:'#d4c8a0',limbCol:'#c4b888',drawScale:1.0,ai:'normal'},
  zombie:   {name:'좀비',      drawType:'zombie',    w:40,h:54, hp:150, atk:15,spd:1.6,xp:26,g:15, bodyCol:'#3d5a30',headCol:'#4d5a38',limbCol:'#2d4a22',drawScale:1.0,ai:'slow'},
  mage_e:   {name:'마법사',    drawType:'mage_enemy',w:36,h:58, hp:105, atk:28,spd:2.5,xp:34,g:24, bodyCol:'#2a1a4a',headCol:'#3a2a6a',limbCol:'#3a2a5a',drawScale:.95,ai:'ranged'},
  demon:    {name:'데몬',      drawType:'demon',     w:48,h:66, hp:185, atk:26,spd:2.7,xp:48,g:32, bodyCol:'#4a0a0a',headCol:'#550a0a',limbCol:'#3a0808',drawScale:1.1,ai:'chase'},
  dragon:   {name:'드래고니언',drawType:'dragon',    w:60,h:72, hp:260, atk:30,spd:2.2,xp:58,g:40, bodyCol:'#1a3a1a',headCol:'#1a4a1a',limbCol:'#2a5a2a',drawScale:1.3,ai:'brute'},
  golem:    {name:'골렘',      drawType:'golem',     w:68,h:76, hp:380, atk:34,spd:1.3,xp:70,g:50, bodyCol:'#6a5a4a',headCol:'#8a7a6a',limbCol:'#7a6a5a',drawScale:1.4,ai:'tank'},
  lich:     {name:'리치',      drawType:'lich',      w:44,h:64, hp:160, atk:32,spd:2.3,xp:55,g:38, bodyCol:'#1a1a3a',headCol:'#222240',limbCol:'#2a2a4a',drawScale:1.1,ai:'ranged'},
  wolf:     {name:'다크 울프', drawType:'goblin',    w:44,h:38, hp:100, atk:18,spd:3.8,xp:18,g:12, bodyCol:'#334',   headCol:'#445',   limbCol:'#223',   drawScale:1.0,ai:'chase'},
};

// ══════════════════════════════════════════════════════
// STAGE DATA (5 stages)
// ══════════════════════════════════════════════════════
const STAGES=[
  {name:'어둠의 동굴', bg:'#06040e',fl:'#100820',wall:'#0d0618', ambCol:'rgba(60,0,120,.08)',torch:'#ff6600',
   enemySet:['goblin','skeleton','zombie'], count:7,
   boss:{name:'슬라임 대왕',drawType:'golem',hp:800,atk:26,spd:2.2,bodyCol:'#226622',headCol:'#337733',limbCol:'#115511',drawScale:1.6}},
  {name:'용암 던전',   bg:'#120400',fl:'#220900',wall:'#1a0500', ambCol:'rgba(200,50,0,.06)',torch:'#ff4400',
   enemySet:['goblin','orc','zombie','demon'], count:9,
   boss:{name:'불꽃 골렘',drawType:'golem',hp:1200,atk:34,spd:2.0,bodyCol:'#662200',headCol:'#883300',limbCol:'#441100',drawScale:1.7}},
  {name:'얼음 궁전',   bg:'#040820',fl:'#081430',wall:'#060e22', ambCol:'rgba(0,80,200,.08)',torch:'#44aaff',
   enemySet:['orc','skeleton','mage_e','wolf'], count:11,
   boss:{name:'빙결 드래곤',drawType:'dragon',hp:1700,atk:42,spd:2.6,bodyCol:'#224466',headCol:'#336688',limbCol:'#112244',drawScale:1.5}},
  {name:'독 늪지',     bg:'#040e04',fl:'#081208',wall:'#060e06', ambCol:'rgba(0,150,0,.07)',torch:'#44cc00',
   enemySet:['zombie','mage_e','lich','demon'], count:13,
   boss:{name:'늪 히드라',drawType:'dragon',hp:2400,atk:50,spd:2.9,bodyCol:'#225522',headCol:'#337733',limbCol:'#113311',drawScale:1.6}},
  {name:'마왕의 성',   bg:'#080010',fl:'#120018',wall:'#0e0014', ambCol:'rgba(150,0,200,.1)',torch:'#aa00ff',
   enemySet:['demon','lich','dragon','golem'], count:16,
   boss:{name:'마왕 DARKOS',drawType:'lich',hp:3200,atk:65,spd:3.1,bodyCol:'#220033',headCol:'#330055',limbCol:'#110022',drawScale:2.0}},
];

// ══════════════════════════════════════════════════════
// SHOP ITEMS
// ══════════════════════════════════════════════════════
const SHOP_ITEMS=[
  {name:'소형 HP 포션',icon:'🧪',desc:'HP +20%',price:60, fn:(p)=>{const h=Math.round(p.maxHp*.2);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'대형 HP 포션',icon:'⚗️',  desc:'HP +55%',price:160,fn:(p)=>{const h=Math.round(p.maxHp*.55);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'마나 포션',   icon:'💙',  desc:'MP +50%',price:80, fn:(p)=>{const m=Math.round(p.maxMp*.5);p.mp=Math.min(p.maxMp,p.mp+m);return `MP +${m}`;}},
  {name:'강화 무기',   icon:'⚔️',  desc:'ATK +18',price:200,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+18;return 'ATK +18';},rarity:1},
  {name:'불꽃 검',     icon:'🔥',  desc:'ATK +35',price:380,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+35;return 'ATK +35';},rarity:2},
  {name:'강화 갑옷',   icon:'🛡️',  desc:'DEF+12 HP+40',price:220,fn:(p)=>{p.defBonus=(p.defBonus||0)+12;p.maxHp+=40;p.hp=Math.min(p.maxHp,p.hp+40);return 'DEF+12 HP+40';},rarity:1},
  {name:'마법 갑옷',   icon:'💎',  desc:'DEF+22 HP+80',price:400,fn:(p)=>{p.defBonus=(p.defBonus||0)+22;p.maxHp+=80;p.hp=Math.min(p.maxHp,p.hp+80);return 'DEF+22 HP+80';},rarity:2},
  {name:'스피드 링',   icon:'💍',  desc:'SPD +1.0',price:180,fn:(p)=>{p.spdBonus=(p.spdBonus||0)+1.0;return 'SPD +1.0';},rarity:1},
  {name:'크리티컬 반지',icon:'🔮', desc:'CRIT +18%',price:300,fn:(p)=>{p.critBonus=(p.critBonus||0)+.18;return 'CRIT +18%';},rarity:2},
  {name:'전설의 반지',  icon:'⭐', desc:'ATK+25 CRIT+25%',price:650,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+25;p.critBonus=(p.critBonus||0)+.25;return 'ATK+25 CRIT+25%';},rarity:4},
];
const RARITY_COL=['#aaaaaa','#44cc44','#4488ff','#cc44ff','#ffcc00'];

// ══════════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════════
let G=null, RAF=null;
let selCharId=null;

const GRAVITY=0.55;
const STAGE_W=5500;

function mkPlayer(clsId, stageIdx=0){
  const c=CLASSES[clsId];
  return {
    ...c,clsId,
    x:140,y:GY()-65,
    vx:0,vy:0,f:1,
    onGround:false,jumpCount:0,
    hp:c.hp,maxHp:c.hp,
    mp:c.mp,maxMp:c.mp,
    alive:true,invincible:0,
    skillCds:c.skills.map(()=>0),
    buffAtk:1,buffSpd:1,buffTimer:0,
    kills:0,score:0,gold:0,level:1,
    xp:0,xpNext:100,
    combo:0,comboTimer:0,maxCombo:0,
    atkCd:0,atkAnim:0,hitFlash:0,dodgeCd:0,dodgeAnim:0,
    w:44,h:62,
    atkBonus:0,defBonus:0,spdBonus:0,critBonus:0,defBuff:0,defBuffTimer:0,
    walkPhase:0,atkPhase:0,
    equip:{wpn:null,arm:null,acc:null},
    statusEffects:{},
  };
}

function initGame(clsId, stageIdx){
  const p=mkPlayer(clsId,stageIdx);
  const stage=STAGES[stageIdx];
  G={
    clsId, stageIdx, stage,
    player:p,
    enemies:[],
    boss:null, bossSpawned:false, bossKills:0,
    projectiles:[],
    items:[],
    cam:0,
    phase:'play',
    timer:0,
    startTime:Date.now(),
    platforms:genPlats(stage),
    shakeAmt:0,shakeTimer:0,
    hitStop:0,
    stageDmgTaken:0,
    paused:false,
    bgOff:0,
    shopStock:[],
    pendingLvlUp:false,
  };
  PARTS.length=0;
  spawnEnemies();
  updateEquipUI();
}

function genPlats(stage){
  const arr=[];
  for(let i=0;i<12;i++){
    arr.push({
      x:280+i*330+(Math.random()-.5)*90,
      y:GY()-80-Math.random()*130,
      w:65+Math.random()*80,h:12,
      col:stage.wall,
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
    const ex=600+i*310+Math.random()*120;
    G.enemies.push({
      ...et,uid:'e'+i+Date.now(),
      x:ex,y:GY()-et.h,
      hp:Math.round(et.hp*sc),maxHp:Math.round(et.hp*sc),
      atk:Math.round(et.atk*sc),
      vx:0,vy:0,f:-1,
      alive:true,dying:false,deathTimer:0,
      atkTimer:60+Math.random()*80,
      frozen:0,stun:0,poison:0,poisonDmg:0,poisonTimer:0,
      burn:0,cursed:0,
      hitFlash:0,
      walkPhase:Math.random()*Math.PI*2,
      atkPhase:0,
      aggro:false,
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
    x:STAGE_W-520,y:GY()-90,
    hp:Math.round(bd.hp*sc),maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc),spd:bd.spd+G.stageIdx*.1,
    w:72,h:90,
    alive:true,dying:false,
    frozen:0,stun:0,cursed:0,
    atkTimer:75,projTimer:100,
    phase2:false,phase3:false,
    hitFlash:0,
    walkPhase:0,atkPhase:0,
  };
  document.getElementById('boss-bar').classList.add('show');
  document.getElementById('boss-name-lbl').textContent='⚠ '+bd.name;
  const bw=document.getElementById('boss-warn');
  bw.style.display='block';
  bw.textContent='⚠ BOSS ⚠\n'+bd.name;
  setTimeout(()=>bw.style.display='none',2400);
  shake(12,40);
  sfx_bossIn();
}

// ══════════════════════════════════════════════════════
// COMBAT HELPERS
// ══════════════════════════════════════════════════════
function totalAtk(p){return (p.atk+(p.atkBonus||0))*(p.buffAtk||1);}
function totalDef(p){return (p.def+(p.defBonus||0))+(p.defBuff||0);}
function totalCrit(p){return .1+(p.critBonus||0);}
function totalSpd(p){return (p.spd+(p.spdBonus||0))*(p.buffSpd||1);}

function dmg(p, mult){
  const atk=totalAtk(p);
  const isCrit=Math.random()<totalCrit(p);
  const v=Math.round((atk*mult+Math.random()*6-3)*(isCrit?2.0:1));
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
    }
  }
}

function hitAll(d,showCrit){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  for(const e of targets) if(e.alive) dealDmg(e,d.v,d.crit||showCrit,{});
}

function dealDmg(e,v,crit,opts){
  if(!e.alive) return;
  const p=G.player;
  if(e.cursed>0) v=Math.round(v*1.4); // cursed takes more dmg
  e.hp-=v;
  e.hitFlash=8;
  if(opts.stun) e.stun=Math.max(e.stun||0,opts.stun);
  if(opts.lifeSteal) p.hp=Math.min(p.maxHp,p.hp+Math.round(v*opts.lifeSteal));
  if(opts.onHit) opts.onHit(e);
  const sx=e.x-G.cam+e.w/2, sy=e.y;
  showDNum(sx,sy,v,crit,p.col||'#fff');
  G.hitStop=crit?5:2;
  if(e.hp<=0) killE(e);
}

function killE(e){
  e.alive=false;e.dying=true;e.deathTimer=28;
  const p=G.player;
  if(e===G.boss){
    p.xp+=700;p.gold+=400;p.score+=8000;
    G.bossKills++;
    document.getElementById('boss-bar').classList.remove('show');
    spawnParts(e.x-G.cam+e.w/2,e.y+e.h/2,{n:60,col:['#ffcc00','#ff6600','#ffffff'],glow:true,sMin:3,sMax:14,type:'c'});
    shake(15,55);
    sfx_clear();
    checkLvlUp(p);
    setTimeout(()=>stageClear(),1100);
  } else {
    p.kills++;p.xp+=e.xp;p.gold+=e.g;p.score+=e.xp*2;
    spawnParts(e.x-G.cam+e.w/2,e.y+e.h/2,{n:14,col:[e.bodyCol||'#556','#ffcc00'],sMin:2,sMax:6});
    checkLvlUp(p);
    tryDrop(e);
  }
}

function checkLvlUp(p){
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext;p.level++;
    p.xpNext=Math.round(p.xpNext*1.55);
    // passive gains
    p.maxHp+=30;p.hp=Math.min(p.maxHp,p.hp+50);
    p.maxMp+=10;p.mp=Math.min(p.maxMp,p.mp+20);
    p.atk+=4;p.def+=2;
    // show level up modal
    G.pendingLvlUp=true;
    showLvlUpModal();
    sfx_lvl();
  }
}

function tryDrop(e){
  if(Math.random()>.38) return;
  const shopPool=SHOP_ITEMS.filter(i=>i.fn);
  const it={...shopPool[Math.floor(Math.random()*shopPool.length)],
    uid:'d'+Date.now()+Math.random(),
    x:e.x+e.w/2-14,y:e.y,vy:-7,alive:true};
  G.items.push(it);
}

function freezeAll(dur){
  if(!G) return;
  for(const e of G.enemies) if(e.alive) e.frozen=Math.max(e.frozen||0,dur);
  if(G.boss&&G.boss.alive) G.boss.frozen=Math.max(G.boss.frozen||0,dur);
}

// ── projectile spawner ──
function proj(x,y,vx,vy,d,col,owner,opts={}){
  if(!G) return;
  G.projectiles.push({
    x,y,vx,vy,
    dmg:d.v,crit:d.crit,
    col,owner,alive:true,
    life:opts.life||80,sz:opts.sz||8,
    pierce:opts.pierce||false,
    grav:opts.grav!==undefined?opts.grav:0,
    emoji:opts.emoji||null,
    trail:opts.trail||false,
    homing:opts.homing||false,
    explode:opts.explode||false,
    onHit:opts.onHit||null,
    uid:'p'+Date.now()+Math.random(),
  });
}

// ── boom helper ──
function boom(wx,wy,col,scale=1.5){
  spawnParts(wx,wy,{n:Math.round(25*scale),col:[col,'#ffffff','#ffcc00'],glow:true,sMin:3*scale,sMax:8*scale,upb:2});
  spawnParts(wx,wy,{n:Math.round(12*scale),col:[col,'#ff4400'],type:'sq',sMin:2*scale,sMax:5*scale});
}

function shake(amt,dur){
  if(!G) return;
  G.shakeAmt=Math.max(G.shakeAmt,amt);
  G.shakeTimer=Math.max(G.shakeTimer,dur);
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
  G.bgOff=(G.bgOff+.35*dt)%500;
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

  if(G.shakeTimer>0) G.shakeTimer-=dt;

  // Boss spawn
  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){
    G.bossSpawned=true;
    spawnBoss();
  }

  // MP regen
  if(G.timer%70===0) p.mp=Math.min(p.maxMp,p.mp+3);

  // Poison on player
  const se=p.statusEffects||{};
  if(se.poison>0){
    se.poison-=dt;
    if(G.timer%22===0) takeDmg(Math.round(p.maxHp*.009));
  }

  // DefBuff tick
  if(p.defBuffTimer>0){p.defBuffTimer-=dt;if(p.defBuffTimer<=0)p.defBuff=0;}
  // BuffTimer
  if(p.buffTimer>0){p.buffTimer-=dt;if(p.buffTimer<=0){p.buffAtk=1;p.buffSpd=1;}}
}

function handleInput(p,dt){
  if(!p.alive) return;
  const spd=totalSpd(p);

  if(KEY['ArrowLeft']){p.vx=-spd*6*dt;p.f=-1;}
  if(KEY['ArrowRight']){p.vx=spd*6*dt;p.f=1;}

  // Jump
  if((JK['z']||JK['Z'])&&p.jumpCount<2){
    p.vy=-p.jmp;p.jumpCount++;
    spawnParts(p.x-G.cam+p.w/2,p.y+p.h,{n:8,col:['#fff','#ccc'],upb:3,sMin:2,sMax:4,spread:.8});
    sfx_jump();
  }

  // Attack
  if((JK['x']||JK['X'])&&p.atkCd<=0) doAttack(p);

  // Dodge
  if(JK[' ']&&p.dodgeCd<=0){
    p.vx=p.f*24;p.vy=-2;
    p.invincible=42;p.dodgeCd=52;p.dodgeAnim=22;
    spawnParts(p.x-G.cam+p.w/2,p.y+p.h/2,{n:14,col:[p.col||'#fff','rgba(255,255,255,.5)'],spread:Math.PI*.5,dir:Math.PI,upb:0,sMin:2,sMax:5,grav:.04});
    sfx_dodge();
  }

  // Skills
  const skMap={a:0,s:1,d:2,f:3,g:4,A:0,S:1,D:2,F:3,G:4};
  for(const [k,idx] of Object.entries(skMap)){
    if(JK[k]&&p.skills[idx]!==undefined){useSkill(p,idx);break;}
  }

  // Pause
  if(JK['p']||JK['P']){
    G.paused=!G.paused;
    document.getElementById('pause-ov').classList.toggle('hidden',!G.paused);
  }
}

function doAttack(p){
  p.atkCd=15;p.atkAnim=14;p.atkPhase=Math.PI*.5;
  p.combo=Math.min(10,(p.combo||0)+1);
  p.comboTimer=85;
  if(p.combo>G.maxCombo) G.maxCombo=p.combo;

  const cdel=document.getElementById('combo-display');
  document.getElementById('combo-num').textContent=p.combo+'HIT';
  cdel.style.opacity=p.combo>=2?'1':'0';

  const mult=1+p.combo*.1;
  const d=dmg(p,mult);
  hitAOE(p.x+(p.f>0?p.w:-68),p.y-12,72,62,d,false);
  spawnParts(p.x+(p.f>0?p.w+20:-30)-G.cam,p.y+22,{n:d.crit?14:7,col:[p.col||'#fff','#ffcc00'],spread:.7,dir:p.f>0?0:Math.PI,sMin:2,sMax:d.crit?8:5,glow:d.crit});
  if(d.crit) shake(3,5);
}

function useSkill(p,idx){
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;
  p.skillCds[idx]=sk.cd*60;
  p.atkPhase=Math.PI;
  sk.fn(p,G);
}

function updatePlayer(p,dt){
  p.vy+=GRAVITY*dt;
  p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vx*=.82;

  const gy=GY();
  if(p.y+p.h>=gy){p.y=gy-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;}
  else p.onGround=false;

  for(const pl of G.platforms){
    if(p.vy>=0&&p.x+p.w>pl.x&&p.x<pl.x+pl.w&&p.y+p.h>pl.y&&p.y+p.h<pl.y+pl.h+14){
      p.y=pl.y-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;
    }
  }
  p.x=Math.max(5,Math.min(STAGE_W-p.w-5,p.x));
  if(p.y>gy+150){p.y=gy-p.h;p.vy=0;}

  // Camera
  G.cam+=(p.x-W()*.35-G.cam)*.09*dt;
  G.cam=Math.max(0,Math.min(STAGE_W-W(),G.cam));

  // Walk phase
  if(Math.abs(p.vx)>0.5&&p.onGround) p.walkPhase+=.25*dt*Math.abs(p.vx)*.04;
  else if(p.onGround) p.walkPhase=Math.round(p.walkPhase/Math.PI)*Math.PI;
  p.atkPhase=Math.max(0,p.atkPhase-.15*dt);

  // Timers
  if(p.invincible>0) p.invincible-=dt;
  if(p.atkCd>0) p.atkCd-=dt;
  if(p.atkAnim>0) p.atkAnim-=dt;
  if(p.hitFlash>0) p.hitFlash-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeAnim>0) p.dodgeAnim-=dt;
  if(p.comboTimer>0){p.comboTimer-=dt;if(p.comboTimer<=0){p.combo=0;document.getElementById('combo-display').style.opacity='0';}}
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;

  // Paladin: passive regen
  if(p.clsId==='paladin'&&G.timer%90===0) p.hp=Math.min(p.maxHp,p.hp+Math.ceil(p.maxHp*.015));
}

function updateEnemies(dt){
  const p=G.player;
  const gy=GY();
  for(const e of G.enemies){
    if(!e.alive){
      if(e.dying){e.deathTimer-=dt;}
      continue;
    }
    if(e.hitFlash>0) e.hitFlash-=dt;
    if(e.frozen>0){e.frozen-=dt;e.walkPhase=0;continue;}
    if(e.stun>0){e.stun-=dt;continue;}
    if(e.cursed>0) e.cursed-=dt;
    if(e.poison>0){
      e.poison-=dt;
      if(!e.poisonTimer||e.poisonTimer<=0){e.hp-=e.poisonDmg||5;e.poisonTimer=20;if(e.hp<=0){killE(e);continue;}}
      e.poisonTimer-=dt;
    }
    if(e.burn>0){e.burn-=dt;}

    const dx=p.x-e.x;
    if(Math.abs(dx)<420) e.aggro=true;
    if(!e.aggro) continue;

    e.f=dx>0?1:-1;
    const sm=e.cursed>0?.6:1;
    const spd=(e.spd||2)*sm;

    const dist=Math.abs(dx);
    switch(e.ai){
      case 'chase': if(dist>50) e.x+=e.f*spd*dt; break;
      case 'brute': if(dist>55) e.x+=e.f*spd*.9*dt; break;
      case 'slow':  if(dist>60) e.x+=e.f*spd*.65*dt; break;
      case 'tank':  if(dist>65) e.x+=e.f*spd*.6*dt; break;
      case 'ranged':
        if(dist<190) e.x-=e.f*spd*.7*dt;
        else if(dist>320) e.x+=e.f*spd*.7*dt;
        break;
      default: if(dist>50) e.x+=e.f*spd*dt; break;
    }

    e.vy=(e.vy||0)+GRAVITY*dt*.55;
    e.y+=e.vy*dt;
    if(e.y+e.h>=gy){e.y=gy-e.h;e.vy=0;}
    for(const pl of G.platforms){
      if(e.vy>=0&&e.x+e.w>pl.x&&e.x<pl.x+pl.w&&e.y+e.h>pl.y&&e.y+e.h<pl.y+pl.h+12){
        e.y=pl.y-e.h;e.vy=0;
      }
    }

    e.walkPhase+=.2*dt;
    e.atkPhase=Math.max(0,e.atkPhase-.12*dt);
    e.atkTimer-=dt;

    if(e.atkTimer<=0&&e.aggro){
      if(e.ai==='ranged'){
        if(dist<360){
          e.atkTimer=95+Math.random()*55;
          const vd=dmg({atk:e.atk,atkBonus:0,buffAtk:1,critBonus:0,crit:0},1);
          proj(e.x+e.w/2,e.y+e.h/2,e.f*11+(Math.random()-.5)*1,(Math.random()-.5)*2,vd,'#aa44ff','enemy',{sz:9,life:80});
          e.atkPhase=Math.PI*.8;
        }
      } else {
        if(dist<60&&Math.abs(p.y-e.y)<65){
          e.atkTimer=75+Math.random()*35;
          e.atkPhase=Math.PI;
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
  const b=G.boss, p=G.player;
  if(!b.alive) return;
  if(b.hitFlash>0) b.hitFlash-=dt;
  if(b.frozen>0){b.frozen-=dt;return;}
  if(b.stun>0){b.stun-=dt;return;}
  if(b.cursed>0) b.cursed-=dt;

  const hpPct=b.hp/b.maxHp;
  if(!b.phase2&&hpPct<.55){
    b.phase2=true;b.spd*=1.35;b.atk=Math.round(b.atk*1.28);
    document.getElementById('boss-phase-txt').textContent='⚡ PHASE 2';
    shake(12,40);
    spawnParts(b.x-G.cam+b.w/2,b.y+b.h/2,{n:50,col:['#ff4400','#ff8800'],glow:true,sMin:4,sMax:12});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true;b.spd*=1.3;b.atk=Math.round(b.atk*1.25);
    document.getElementById('boss-phase-txt').textContent='💀 PHASE 3 ENRAGE';
    shake(18,60);
    spawnParts(b.x-G.cam+b.w/2,b.y+b.h/2,{n:80,col:['#ff0000','#cc00ff','#ffffff'],glow:true,sMin:5,sMax:16,type:'c'});
    sfx_bossIn();
  }

  const dx=p.x-b.x;
  b.f=dx>0?1:-1;
  if(Math.abs(dx)>95) b.x+=b.f*b.spd*dt*.92;
  b.vy=(b.vy||0)+GRAVITY*dt*.45;
  b.y+=b.vy*dt;
  const gy=GY();
  if(b.y+b.h>=gy){b.y=gy-b.h;b.vy=0;}
  b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));

  b.walkPhase+=.12*dt;
  b.atkPhase=Math.max(0,b.atkPhase-.1*dt);
  b.atkTimer-=dt;
  b.projTimer-=dt;

  const projInt=b.phase3?44:b.phase2?65:100;
  if(b.projTimer<=0){
    b.projTimer=projInt;
    b.atkPhase=Math.PI*.8;
    const bv=dmg({atk:b.atk,atkBonus:0,buffAtk:1,critBonus:0},b.phase3?.7:.6);
    if(b.phase3){
      for(let i=-1;i<=1;i++) proj(b.x+b.w/2,b.y+b.h*.4,b.f*10,i*4.5,bv,'#ff2200','enemy',{sz:16,emoji:'💥',life:88,grav:.08});
    } else {
      proj(b.x+b.w/2,b.y+b.h*.4,b.f*9,-2,bv,'#ff4400','enemy',{sz:16,emoji:'💥',life:88,grav:.09});
    }
  }

  if(b.atkTimer<=0&&Math.abs(dx)<100){
    b.atkTimer=b.phase3?40:b.phase2?55:75;
    b.atkPhase=Math.PI;
    if(Math.abs(p.y-b.y)<95&&p.invincible<=0&&p.dodgeAnim<=0){
      const rawDmg=Math.max(1,b.atk-Math.round(totalDef(p)*.45)+Math.floor(Math.random()*12)-6);
      takeDmg(rawDmg);
      if(b.phase3){
        // 2nd hit
        setTimeout(()=>{if(G&&p.hp>0)takeDmg(Math.round(rawDmg*.7));},200);
      }
    }
  }

  document.getElementById('boss-hp-fill').style.width=Math.max(0,(b.hp/b.maxHp)*100)+'%';
}

function takeDmg(v){
  const p=G.player;
  if(p.invincible>0) return;
  p.hp-=v;p.hitFlash=12;p.invincible=38;
  G.stageDmgTaken+=v;
  const fl=document.getElementById('hit-flash');
  fl.style.opacity='1';fl.style.background='rgba(255,30,30,.35)';
  setTimeout(()=>{fl.style.opacity='0';},110);
  shake(4,10);
  if(p.hp<=0) gameOver();
}

function updateProjs(dt){
  const p=G.player;
  const gy=GY();
  G.projectiles=G.projectiles.filter(pr=>{
    if(!pr.alive) return false;
    pr.x+=pr.vx*dt;pr.y+=pr.vy*dt;
    pr.vy+=pr.grav*dt;
    pr.life-=dt;
    if(pr.life<=0) return false;

    if(pr.homing&&pr.owner==='player'){
      const targets=[...G.enemies];
      if(G.boss&&G.boss.alive) targets.push(G.boss);
      let best=null,bd=999;
      for(const e of targets){if(!e.alive) continue;const d=Math.abs(e.x-pr.x)+Math.abs(e.y-pr.y);if(d<bd){bd=d;best=e;}}
      if(best&&bd<500){
        const ddx=best.x+best.w/2-pr.x,ddy=best.y+best.h/2-pr.y;
        const l=Math.sqrt(ddx*ddx+ddy*ddy)||1;
        pr.vx+=(ddx/l*3-pr.vx)*.13;pr.vy+=(ddy/l*3-pr.vy)*.13;
      }
    }

    if(pr.trail) spawnParts(pr.x,pr.y,{n:2,col:[pr.col],sMin:1,sMax:3,grav:0,dMax:.06,spread:Math.PI*.3});

    // Explode on ground
    if(pr.explode&&pr.y>=gy){
      boom(pr.x,gy,pr.col);
      hitAOE(pr.x-65,gy-70,130,85,{v:pr.dmg,crit:pr.crit},false);
      shake(4,8);
      return false;
    }
    if(pr.y>gy+80||pr.x<G.cam-100||pr.x>G.cam+W()+100) return false;

    if(pr.owner==='player'){
      const targets=[...G.enemies];
      if(G.boss&&G.boss.alive) targets.push(G.boss);
      for(const e of targets){
        if(!e.alive) continue;
        if(pr.x>e.x&&pr.x<e.x+e.w&&pr.y>e.y&&pr.y<e.y+e.h){
          dealDmg(e,pr.dmg,pr.crit,{onHit:pr.onHit});
          spawnParts(pr.x-G.cam,pr.y,{n:8,col:[pr.col,'#fff'],sMin:2,sMax:5,glow:!!pr.emoji});
          if(!pr.pierce){pr.alive=false;return false;}
        }
      }
    } else {
      // Enemy proj vs player
      const sx=pr.x-G.cam;
      if(p.invincible<=0&&p.dodgeAnim<=0&&
         sx>p.x-G.cam&&sx<p.x-G.cam+p.w&&pr.y>p.y&&pr.y<p.y+p.h){
        takeDmg(Math.max(1,pr.dmg-Math.round(totalDef(p)*.4)));
        pr.alive=false;return false;
      }
    }
    return true;
  });
}

function updateItems(dt){
  const p=G.player;
  const gy=GY();
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAVITY*dt*.7;
    it.y+=it.vy*dt;
    if(it.y+20>=gy){it.y=gy-20;it.vy=0;}
    const sx=it.x-G.cam;
    if(sx>p.x-G.cam-30&&sx<p.x-G.cam+p.w+30&&it.y>p.y-10&&it.y<p.y+p.h+20){
      const res=it.fn(p);
      showDNum(sx,it.y,'+ '+res,false,'#ffcc00');
      it.alive=false;
      return false;
    }
    return true;
  });
}

// ══════════════════════════════════════════════════════
// RENDER
// ══════════════════════════════════════════════════════
function gameRender(){
  if(!G){
    ctx.fillStyle='#08060f';ctx.fillRect(0,0,W(),H());
    return;
  }
  ctx.save();
  if(G.shakeTimer>0){
    const s=G.shakeAmt*(G.shakeTimer/20)*.5;
    ctx.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }

  const st=G.stage;
  ctx.fillStyle=st.bg;ctx.fillRect(0,0,W(),H());

  drawBG(st);
  drawPlats();
  drawFloor(st);

  drawParts(G.cam);
  drawProjs();
  drawItems();
  drawEnemies_all();
  if(G.boss&&(G.boss.alive||G.boss.dying)) drawMonster(G.boss,G.cam);
  drawPlayer();

  ctx.restore();
  drawMinimap();
}

function drawBG(st){
  ctx.save();
  ctx.globalAlpha=.05;
  ctx.font='900 90px sans-serif';ctx.fillStyle='#ffffff';ctx.textAlign='center';
  ctx.fillText(st.name,W()/2,H()/2+30);
  ctx.restore();
  // Ambient
  if(st.ambCol){ctx.fillStyle=st.ambCol;ctx.fillRect(0,0,W(),H());}
  // Torch particles
  if(G.timer%6===0){
    spawnParts((Math.random()-.5)*30+W()*.3,GY()-20,{n:1,col:[st.torch||'#ff6600'],glow:true,sMin:1,sMax:2,upb:2,grav:-.02,dMax:.04,spread:.3});
    spawnParts((Math.random()-.5)*30+W()*.7,GY()-20,{n:1,col:[st.torch||'#ff6600'],glow:true,sMin:1,sMax:2,upb:2,grav:-.02,dMax:.04,spread:.3});
  }
}

function drawPlats(){
  const st=G.stage;
  for(const pl of G.platforms){
    const px=pl.x-G.cam;
    if(px>W()+10||px+pl.w<-10) continue;
    ctx.fillStyle=st.fl;ctx.fillRect(px,pl.y,pl.w,pl.h);
    ctx.fillStyle='rgba(255,180,80,.2)';ctx.fillRect(px,pl.y,pl.w,2);
    ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(px,pl.y+pl.h-3,pl.w,3);
  }
}

function drawFloor(st){
  const gy=GY();
  ctx.fillStyle=st.fl;ctx.fillRect(0,gy,W(),H()-gy);
  ctx.fillStyle='rgba(255,180,80,.28)';ctx.fillRect(0,gy,W(),2);
}

function drawPlayer(){
  const p=G.player;
  const px=p.x-G.cam;
  if(p.invincible>0&&Math.floor(G.timer/3)%2===0) return;
  ctx.save();
  if(p.dodgeAnim>0){
    // Afterimages
    for(let i=1;i<=3;i++){
      ctx.globalAlpha=(p.dodgeAnim/22)*(i/3)*.28;
      drawChar({x:px-p.f*i*18,y:p.y+p.h,f:p.f,walkPhase:p.walkPhase,atkPhase:0,hitFlash:0,dead:false,...p,scale:.9});
    }
    ctx.globalAlpha=1;
  }
  drawChar({x:px,y:p.y+p.h,f:p.f,walkPhase:p.walkPhase,atkPhase:p.atkPhase,hitFlash:p.hitFlash,dead:!p.alive,...p});
  // Shadow
  ctx.globalAlpha=.28;ctx.fillStyle='#000';
  ctx.beginPath();ctx.ellipse(px+p.w/2,GY()+5,p.w*.5,6,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawEnemies_all(){
  for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const ex=e.x-G.cam;
    if(ex<-100||ex>W()+100) continue;
    const alpha=e.dying?(e.deathTimer/28):1;
    ctx.save();ctx.globalAlpha=alpha;
    drawMonster(e,G.cam);
    ctx.restore();
  }
}

function drawProjs(){
  for(const pr of G.projectiles){
    const px=pr.x-G.cam;
    if(px<-30||px>W()+30) continue;
    if(pr.emoji){
      ctx.font=`${pr.sz*1.8}px serif`;
      ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pr.emoji,px,pr.y);
    } else {
      ctx.save();
      ctx.fillStyle=pr.col;ctx.shadowColor=pr.col;ctx.shadowBlur=10;
      ctx.beginPath();ctx.arc(px,pr.y,pr.sz,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;ctx.restore();
    }
  }
}

function drawItems(){
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam;
    if(ix<-30||ix>W()+30) continue;
    ctx.save();
    ctx.shadowColor=RARITY_COL[it.rarity||0];ctx.shadowBlur=12;
    const bob=Math.sin(G.timer*.08+it.x*.01)*3;
    ctx.font='22px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(it.icon,ix,it.y+bob);
    ctx.shadowBlur=0;ctx.restore();
  }
}

function drawMinimap(){
  const mc=document.getElementById('mm-canvas');
  const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,110,26);
  const scale=110/STAGE_W;
  const p=G.player;
  for(const e of G.enemies){
    if(!e.alive) continue;
    mctx.fillStyle=e.bodyCol||'#f44';
    mctx.fillRect(e.x*scale,8,3,3);
  }
  if(G.boss&&G.boss.alive){mctx.fillStyle='#f00';mctx.fillRect(G.boss.x*scale-1,6,5,5);}
  mctx.fillStyle='#0fa';mctx.fillRect(p.x*scale-2,8,4,4);
  mctx.strokeStyle='rgba(245,200,66,.35)';mctx.lineWidth=1;
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

  // Buff icons
  let bi='';
  if(p.buffAtk>1) bi+='<span title="공격 강화">🔥</span>';
  if(p.defBuff>0) bi+='<span title="방어 강화">🛡️</span>';
  if(p.invincible>60) bi+='<span title="무적">⭐</span>';
  document.getElementById('buff-row').innerHTML=bi;

  // Skill slots
  const sc=document.getElementById('sk-cont');
  sc.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i];
    const cd=p.skillCds[i];
    const rdy=cd<=0&&p.mp>=sk.mp;
    const div=document.createElement('div');
    div.className='sk-slot '+(rdy?'ready':'cooling');
    div.innerHTML=`<div class="sk-icon">${sk.icon}</div>
      <span class="sk-key">${sk.key}</span>
      <span class="sk-mp-cost">${sk.mp}</span>
      <div class="sk-ring"></div>`;
    if(cd>0){
      const cdDiv=document.createElement('div');
      cdDiv.className='sk-cd-overlay';
      cdDiv.textContent=cd>60?Math.ceil(cd/60)+'s':cd.toFixed(1)+'s';
      div.appendChild(cdDiv);
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
    const el=document.getElementById('eq-'+s);
    if(!el) return;
    const icons=['🗡️','🛡️','💍'];
    el.textContent=p.equip[s]?p.equip[s].icon:icons[i];
  });
}

// ══════════════════════════════════════════════════════
// DAMAGE NUMBERS
// ══════════════════════════════════════════════════════
function showDNum(sx,sy,v,crit,col){
  const el=document.createElement('div');
  el.className='dnum';
  el.style.cssText=`left:${sx-18}px;top:${sy+H()-H()+36}px;font-size:${crit?'1.3':'0.9'}rem;color:${crit?'#ffff44':(col||'#fff')};`;
  const garea=document.getElementById('game-area');
  el.style.top=(garea.offsetTop+sy-14)+'px';
  el.style.left=(garea.offsetLeft+sx-18)+'px';
  el.textContent=crit?v+'!!':v;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),950);
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
  G.phase='over';
  G.player.alive=false;
  const p=G.player;
  document.getElementById('over-grid').innerHTML=`
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">점수<b>${p.score}</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">스테이지<b>${G.stageIdx+1}</b></div>
    <div class="res-cell">콤보<b>${G.maxCombo}HIT</b></div>`;
  setTimeout(()=>document.getElementById('over-ov').classList.remove('hidden'),750);
  sfx_death();
}

function openShop(){
  document.getElementById('clear-ov').classList.add('hidden');
  buildShop();
  document.getElementById('shop-ov').classList.remove('hidden');
}

function buildShop(){
  const p=G.player;
  document.getElementById('shop-gold-lbl').textContent=p.gold;
  const pool=[...SHOP_ITEMS].sort(()=>Math.random()-.5).slice(0,6);
  G.shopStock=pool.map(it=>({...it,uid:'s'+Date.now()+Math.random(),price:it.price+G.stageIdx*30}));
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
  const p=G.player;
  const it=G.shopStock[i];
  if(!it||p.gold<it.price) return;
  p.gold-=it.price;
  const res=it.fn(p);
  sfx_buy();
  buildShop();
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
// LEVEL UP MODAL
// ══════════════════════════════════════════════════════
function showLvlUpModal(){
  const grid=document.getElementById('stat-pick-grid');
  grid.innerHTML=`
    <button class="stat-pick-btn" onclick="pickStat('hp')">❤️ 최대 HP +25</button>
    <button class="stat-pick-btn" onclick="pickStat('atk')">⚔️ ATK +5</button>
    <button class="stat-pick-btn" onclick="pickStat('def')">🛡️ DEF +3</button>
    <button class="stat-pick-btn" onclick="pickStat('spd')">💨 SPD +0.5</button>
    <button class="stat-pick-btn" onclick="pickStat('mp')">🔷 최대 MP +20</button>
    <button class="stat-pick-btn" onclick="pickStat('crit')">⚡ 크리 +5%</button>`;
  document.getElementById('lvlup-ov').classList.remove('hidden');
}

function pickStat(stat){
  const p=G.player;
  if(stat==='hp'){p.maxHp+=25;p.hp=Math.min(p.maxHp,p.hp+25);}
  else if(stat==='atk') p.atk+=5;
  else if(stat==='def') p.def+=3;
  else if(stat==='spd') p.spd+=0.5;
  else if(stat==='mp'){p.maxMp+=20;p.mp=Math.min(p.maxMp,p.mp+20);}
  else if(stat==='crit') p.critBonus=(p.critBonus||0)+.05;
  document.getElementById('lvlup-ov').classList.add('hidden');
  G.pendingLvlUp=false;
}

// ══════════════════════════════════════════════════════
// ACHIEVEMENT
// ══════════════════════════════════════════════════════
let achTimer=null;
function showAchiev(icon,title,sub){
  const el=document.getElementById('achiev');
  document.getElementById('ach-icon').textContent=icon;
  document.getElementById('ach-title').textContent=title;
  document.getElementById('ach-sub').textContent=sub;
  el.classList.add('show');
  clearTimeout(achTimer);
  achTimer=setTimeout(()=>el.classList.remove('show'),3200);
}

// ══════════════════════════════════════════════════════
// WEB AUDIO SFX (minimal procedural)
// ══════════════════════════════════════════════════════
let ACtx=null;
function ensureAudio(){
  if(!ACtx) try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}
}
function synth(freq,type,dur,vol=.3,del=0){
  if(!ACtx) return;
  try{
    const o=ACtx.createOscillator(),g=ACtx.createGain();
    o.connect(g);g.connect(ACtx.destination);
    o.type=type;o.frequency.value=freq;
    const t=ACtx.currentTime+del;
    g.gain.setValueAtTime(0,t);
    g.gain.linearRampToValueAtTime(vol,t+.005);
    g.gain.exponentialRampToValueAtTime(.001,t+dur);
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
  const mkStars=(n,max=5)=>[...Array(max)].map((_,i)=>`<span class="star ${i<n?'on':''}">${i<n?'★':'☆'}</span>`).join('');
  for(const [id,c] of Object.entries(CLASSES)){
    const div=document.createElement('div');
    div.className='ccard';div.id='cc-'+id;
    div.onclick=()=>{selCharId=id;document.querySelectorAll('.ccard').forEach(x=>x.classList.remove('sel'));div.classList.add('sel');document.getElementById('start-btn').disabled=false;ensureAudio();};
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

// ══════════════════════════════════════════════════════
// IDLE TITLE ANIMATION
// ══════════════════════════════════════════════════════
let titleRaf=null;
function titleIdle(ts){
  if(G){return;}
  ctx.fillStyle='#08060f';ctx.fillRect(0,0,W(),H());
  ctx.save();ctx.globalAlpha=.04+Math.sin(ts*.001)*.02;
  ctx.font='900 80px sans-serif';ctx.fillStyle='#ff6600';ctx.textAlign='center';
  ctx.fillText('DUNGEON CRUSH',W()/2,H()/2+30);ctx.restore();
  updateParts(1);drawParts(0);
  if(Math.random()<.3) spawnParts(Math.random()*W(),Math.random()*H(),{n:2,col:['#ff6600','#ffaa00','#cc44ff'],glow:true,sMin:1,sMax:3,grav:-.02,dMin:.01,dMax:.015});
  titleRaf=requestAnimationFrame(titleIdle);
}

// ══════════════════════════════════════════════════════
// BOOT
// ══════════════════════════════════════════════════════
KEY['ArrowLeft']=false;
buildTitle();
titleRaf=requestAnimationFrame(titleIdle);
RAF=requestAnimationFrame(loop);
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
    components.html(GAME_HTML, height=760, scrolling=False)
