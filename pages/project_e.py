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
  --bg:#08060f;--gold:#f5c842;--red:#ff2233;--blue:#2299ff;
  --green:#22ff88;--purple:#cc44ff;--orange:#ff7722;
  --border:rgba(245,200,66,0.18);
}
html,body{width:100%;height:100%;background:var(--bg);overflow:hidden;font-family:'Noto Sans KR',sans-serif;color:#ddd;}
#wrap{width:100vw;height:100vh;display:flex;flex-direction:column;}

/* HUD */
#hud{height:50px;background:linear-gradient(180deg,#0d0a18,#09061200);border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:8px;padding:0 10px;flex-shrink:0;position:relative;z-index:50;}
.hud-char{font-family:'Black Han Sans',sans-serif;font-size:.78rem;color:var(--gold);letter-spacing:2px;white-space:nowrap;}
.bar-group{display:flex;flex-direction:column;gap:2px;}
.bar-row{display:flex;align-items:center;gap:4px;}
.bar-label{font-size:.46rem;color:#666;width:14px;text-align:right;}
.bar-bg{height:9px;background:rgba(255,255,255,.06);border-radius:2px;border:1px solid rgba(255,255,255,.05);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:2px;transition:width .08s;}
#hp-fill{background:linear-gradient(90deg,#660000,#dd1122,#ff4455);width:100%;}
#mp-fill{background:linear-gradient(90deg,#001166,#1144cc,#3388ff);width:100%;}
#xp-fill{background:linear-gradient(90deg,#224400,#44aa00,#88ff44);width:0%;}
.bar-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.42rem;color:rgba(255,255,255,.7);font-weight:700;}
#stat-row{display:flex;gap:4px;margin-left:4px;}
.sbox{background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:3px;padding:1px 5px;text-align:center;min-width:34px;}
.sbox-v{font-size:.72rem;font-weight:900;color:var(--gold);}
.sbox-l{font-size:.36rem;color:#555;letter-spacing:.5px;}
.floor-lbl{font-family:'Rajdhani',sans-serif;font-size:.88rem;font-weight:700;color:#fff;
  background:rgba(245,200,66,.1);border:1px solid var(--border);border-radius:3px;padding:1px 8px;letter-spacing:2px;margin-left:auto;}
#buff-row{display:flex;gap:3px;font-size:.85rem;}

/* GAME AREA */
#game-area{flex:1;position:relative;overflow:hidden;}
canvas#gc{display:block;width:100%;height:100%;}

/* BOSS BAR */
#boss-bar{position:absolute;top:6px;left:50%;transform:translateX(-50%);width:380px;pointer-events:none;z-index:40;opacity:0;transition:opacity .3s;}
#boss-bar.show{opacity:1;}
#boss-name-lbl{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.75rem;color:#ff3344;margin-bottom:2px;text-shadow:0 0 10px rgba(255,0,50,.6);letter-spacing:2px;}
#boss-hp-bg{height:11px;background:rgba(255,255,255,.05);border-radius:2px;border:1px solid rgba(255,50,70,.3);overflow:hidden;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);border-radius:2px;transition:width .1s;}
#boss-phase-txt{text-align:center;font-size:.48rem;color:#ff7788;letter-spacing:3px;margin-top:2px;}

/* SKILL BAR */
#skill-bar{position:absolute;bottom:0;left:0;right:0;height:62px;
  background:linear-gradient(0deg,#0d0a18f8,#0d0a1880);border-top:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;gap:5px;padding:0 10px;z-index:50;}
.sk-slot{width:50px;height:52px;border-radius:6px;position:relative;
  background:rgba(255,255,255,.04);border:1px solid rgba(245,200,66,.2);
  display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:default;transition:all .15s;}
.sk-slot.ready{border-color:rgba(245,200,66,.75);box-shadow:0 0 12px rgba(245,200,66,.3);}
.sk-slot.cooling{opacity:.4;}
.sk-icon{font-size:1.35rem;line-height:1;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.38rem;color:#666;}
.sk-mp{position:absolute;top:2px;left:3px;font-size:.38rem;color:#5599ff;}
.sk-cd{position:absolute;inset:0;background:rgba(0,0,0,.78);border-radius:6px;
  display:flex;align-items:center;justify-content:center;font-size:.7rem;color:var(--gold);font-weight:900;}
.ctrl-hint{position:absolute;right:10px;font-size:.46rem;color:#3a3550;line-height:1.9;text-align:right;pointer-events:none;}

/* COMBO */
#combo-disp{position:absolute;top:10px;right:12px;text-align:right;pointer-events:none;opacity:0;transition:opacity .25s;z-index:45;}
#combo-num{font-family:'Black Han Sans',sans-serif;font-size:2.6rem;color:var(--gold);line-height:1;
  text-shadow:0 0 24px rgba(245,200,66,.9),2px 2px 0 rgba(0,0,0,.9);}
#combo-lbl{font-size:.56rem;color:var(--orange);letter-spacing:4px;}

/* OVERLAYS */
.ov{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(8,6,15,.97);}
.ov.hidden{display:none;}

/* TITLE */
#title-ov{flex-direction:column;text-align:center;}
.title-logo{font-family:'Black Han Sans',sans-serif;font-size:3.2rem;letter-spacing:8px;
  background:linear-gradient(135deg,#ff4400,#ff9900,#ffcc00,#ff6600);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(255,150,0,.6));margin-bottom:4px;}
.title-sub{font-family:'Rajdhani',sans-serif;font-size:.88rem;color:#444;letter-spacing:10px;margin-bottom:28px;}
.char-row{display:flex;gap:8px;margin-bottom:22px;flex-wrap:wrap;justify-content:center;max-width:820px;}
.ccard{width:100px;background:rgba(255,255,255,.02);border:1px solid rgba(245,200,66,.12);
  border-radius:8px;padding:10px 7px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard:hover,.ccard.sel{border-color:rgba(245,200,66,.75);background:rgba(245,200,66,.06);
  transform:translateY(-4px);box-shadow:0 8px 30px rgba(245,200,66,.18);}
.ccard-icon{font-size:2rem;margin-bottom:5px;}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:.72rem;color:var(--gold);letter-spacing:2px;}
.ccard-role{font-size:.48rem;color:#555;margin-top:2px;}
.ccard-desc{font-size:.46rem;color:#444;margin-top:5px;line-height:1.5;}
.start-btn{padding:12px 48px;background:linear-gradient(135deg,#7a2e00,#ff5500);
  border:none;border-radius:4px;color:#fff;font-family:'Black Han Sans',sans-serif;font-size:.88rem;
  letter-spacing:4px;cursor:pointer;box-shadow:0 0 24px rgba(255,100,0,.4);transition:all .2s;}
.start-btn:hover{transform:scale(1.06);filter:brightness(1.2);}
.start-btn:disabled{opacity:.25;cursor:default;transform:none;}

/* RESULT BOXES */
.result-box{background:rgba(13,10,26,.98);border:1px solid var(--border);border-radius:10px;
  padding:26px 34px;min-width:340px;text-align:center;box-shadow:0 0 60px rgba(245,200,66,.1);}
.result-title{font-family:'Black Han Sans',sans-serif;font-size:1.75rem;letter-spacing:4px;margin-bottom:12px;}
.clear-title{color:var(--gold);text-shadow:0 0 20px rgba(245,200,66,.5);}
.over-title{color:var(--red);text-shadow:0 0 20px rgba(255,30,50,.5);}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:10px 0;text-align:left;}
.res-cell{font-size:.66rem;color:#777;display:flex;justify-content:space-between;}
.res-cell b{color:var(--gold);}
.action-row{display:flex;gap:8px;justify-content:center;margin-top:12px;}
.abtn{padding:9px 22px;border:none;border-radius:4px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:.76rem;letter-spacing:2px;transition:all .18s;}
.abtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.btn-next{background:linear-gradient(135deg,#1a5500,#22aa00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-gray{background:rgba(255,255,255,.07);color:#888;border:1px solid rgba(255,255,255,.1);}

/* SHOP */
#shop-ov{flex-direction:column;text-align:center;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.55rem;color:var(--gold);letter-spacing:4px;margin-bottom:6px;}
.shop-grid{display:flex;gap:9px;flex-wrap:wrap;justify-content:center;margin:12px 0;}
.shop-card{width:118px;background:rgba(255,255,255,.03);border:1px solid rgba(245,200,66,.15);
  border-radius:6px;padding:9px 7px;cursor:pointer;transition:all .18s;text-align:center;}
.shop-card:hover:not(.cant){border-color:rgba(245,200,66,.6);background:rgba(245,200,66,.06);}
.shop-card.cant{opacity:.3;cursor:default;}
.sc-icon{font-size:1.55rem;margin-bottom:4px;}
.sc-name{font-size:.63rem;color:#ccc;font-weight:700;}
.sc-desc{font-size:.48rem;color:#555;margin-top:2px;}
.sc-price{font-size:.68rem;color:var(--gold);font-weight:900;margin-top:5px;}

/* LEVEL UP */
#lvlup-ov{flex-direction:column;text-align:center;}
.lvlup-title{font-family:'Black Han Sans',sans-serif;font-size:1.9rem;color:var(--gold);letter-spacing:4px;margin-bottom:8px;}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0;}
.stat-btn{padding:11px 9px;border:1px solid var(--border);border-radius:5px;
  background:rgba(255,255,255,.04);cursor:pointer;transition:all .18s;
  font-family:'Noto Sans KR',sans-serif;font-size:.73rem;color:#ccc;}
.stat-btn:hover{border-color:var(--gold);background:rgba(245,200,66,.08);color:var(--gold);}

/* DAMAGE NUMBERS */
@keyframes dmgUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-70px) scale(.65);}}
.dnum{position:absolute;pointer-events:none;font-family:'Black Han Sans',sans-serif;
  animation:dmgUp 1s ease forwards;z-index:160;text-shadow:1px 1px 4px rgba(0,0,0,.95);}

/* MINIMAP */
#minimap{position:absolute;bottom:66px;right:10px;
  width:120px;height:28px;background:rgba(0,0,0,.75);
  border:1px solid var(--border);border-radius:3px;overflow:hidden;z-index:45;}

/* EQUIP */
#equip-quick{position:absolute;bottom:66px;left:10px;z-index:45;display:flex;gap:4px;}
.eq-quick{width:36px;height:36px;background:rgba(0,0,0,.72);border:1px solid rgba(245,200,66,.22);
  border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:.9rem;position:relative;}
.eq-name{position:absolute;bottom:-13px;left:50%;transform:translateX(-50%);font-size:.37rem;color:#444;white-space:nowrap;}

/* HIT FLASH */
#hit-flash{position:absolute;inset:0;pointer-events:none;z-index:100;opacity:0;transition:opacity .06s;}

/* BOSS WARNING */
@keyframes bwPulse{0%,100%{opacity:0;transform:translate(-50%,-50%) scale(.8);}40%,60%{opacity:1;transform:translate(-50%,-50%) scale(1);}}
#boss-warn{position:absolute;top:45%;left:50%;z-index:180;display:none;
  font-family:'Black Han Sans',sans-serif;font-size:1.9rem;color:#ff2233;
  text-shadow:0 0 30px rgba(255,0,50,1);letter-spacing:6px;text-align:center;
  animation:bwPulse 2.4s ease forwards;pointer-events:none;}

/* ACHIEVEMENT */
#achiev{position:absolute;top:56px;left:50%;transform:translateX(-50%) translateY(-90px);
  background:rgba(40,28,4,.97);border:1px solid rgba(245,200,66,.5);border-radius:5px;
  padding:6px 16px;display:flex;align-items:center;gap:7px;z-index:300;transition:transform .3s;pointer-events:none;}
#achiev.show{transform:translateX(-50%) translateY(0);}

/* LADDER INDICATOR */
.ladder-hint{position:absolute;font-size:.58rem;color:rgba(245,200,66,.7);
  text-align:center;pointer-events:none;animation:ladder-glow 1.5s ease-in-out infinite;}
@keyframes ladder-glow{0%,100%{opacity:.5;}50%{opacity:1;}}

/* SCREEN EFFECTS */
@keyframes crit-flash{0%{opacity:.6;}100%{opacity:0;}}
#crit-flash{position:absolute;inset:0;pointer-events:none;z-index:95;opacity:0;
  background:radial-gradient(circle,rgba(255,220,0,.3) 0%,transparent 70%);}
</style>
</head>
<body>
<div id="wrap">
  <div id="hud">
    <div class="hud-char" id="hud-name">—</div>
    <div class="bar-group">
      <div class="bar-row">
        <span class="bar-label">HP</span>
        <div class="bar-bg" style="width:148px">
          <div class="bar-fill" id="hp-fill"></div>
          <div class="bar-text" id="hp-text"></div>
        </div>
      </div>
      <div class="bar-row">
        <span class="bar-label">MP</span>
        <div class="bar-bg" style="width:148px">
          <div class="bar-fill" id="mp-fill"></div>
          <div class="bar-text" id="mp-text"></div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;margin-left:6px;">
      <div style="font-size:.43rem;color:#444;">EXP</div>
      <div class="bar-bg" style="width:95px;height:6px;"><div class="bar-fill" id="xp-fill"></div></div>
      <div style="font-size:.41rem;color:#333;" id="xp-text">0/100</div>
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
    <div class="floor-lbl" id="floor-lbl">1F</div>
  </div>

  <div id="game-area">
    <canvas id="gc"></canvas>
    <div id="hit-flash"></div>
    <div id="crit-flash"></div>

    <div id="boss-bar">
      <div id="boss-name-lbl">BOSS</div>
      <div id="boss-hp-bg"><div id="boss-hp-fill" style="width:100%"></div></div>
      <div id="boss-phase-txt"></div>
    </div>

    <div id="combo-disp">
      <div id="combo-num">0</div>
      <div id="combo-lbl">COMBO</div>
    </div>

    <div id="minimap"><canvas id="mm-canvas" width="120" height="28"></canvas></div>
    <div id="equip-quick">
      <div class="eq-quick" id="eq-wpn">🗡️<span class="eq-name">무기</span></div>
      <div class="eq-quick" id="eq-arm">🛡️<span class="eq-name">방어</span></div>
      <div class="eq-quick" id="eq-acc">💍<span class="eq-name">장신구</span></div>
    </div>

    <div id="boss-warn">⚠ BOSS ⚠</div>
    <div id="achiev"><div id="ach-icon">🏆</div><div><div id="ach-title">업적</div><div id="ach-sub" style="font-size:.48rem;color:#886600;">달성</div></div></div>

    <div id="skill-bar">
      <div id="sk-cont" style="display:flex;gap:5px;"></div>
      <div class="ctrl-hint">
        ←→ 이동 &nbsp;|&nbsp; Z 점프(2단)<br>
        ↑↓ 사다리 오르내리기<br>
        X 공격 &nbsp;|&nbsp; A~G 스킬<br>
        Space 회피 &nbsp;|&nbsp; P 일시정지
      </div>
    </div>

    <!-- OVERLAYS -->
    <div class="ov" id="title-ov">
      <div>
        <div class="title-logo">던전 크러시</div>
        <div class="title-sub">DUNGEON CRUSH v2</div>
        <div class="char-row" id="char-row"></div>
        <button class="start-btn" id="start-btn" onclick="startPressed()" disabled>전투 시작 ▶</button>
      </div>
    </div>
    <div class="ov hidden" id="lvlup-ov">
      <div class="result-box">
        <div class="lvlup-title">⬆ LEVEL UP!</div>
        <div style="font-size:.7rem;color:#666;margin-bottom:4px;">강화할 스탯을 고르세요</div>
        <div class="stat-grid" id="stat-grid"></div>
      </div>
    </div>
    <div class="ov hidden" id="shop-ov">
      <div>
        <div class="shop-title">⚗ 상점</div>
        <div style="font-size:.68rem;color:#666;margin-bottom:4px;">보유 골드: <span id="shop-gold-lbl" style="color:var(--gold);font-weight:700">0</span></div>
        <div class="shop-grid" id="shop-grid"></div>
        <button class="abtn btn-next" onclick="continueAfterShop()" style="margin-top:6px;">다음 스테이지 →</button>
      </div>
    </div>
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
    <div class="ov hidden" id="pause-ov">
      <div style="text-align:center">
        <div style="font-family:'Black Han Sans',sans-serif;font-size:2.4rem;color:#fff;letter-spacing:6px;">⏸ PAUSE</div>
        <div style="font-size:.68rem;color:#444;margin-top:12px;letter-spacing:2px;">P 키를 눌러 계속</div>
      </div>
    </div>
  </div>
</div>

<script>
'use strict';
// ═══════════════════════════════════════════════════════════
//  DUNGEON CRUSH v2 — VERTICAL MULTI-FLOOR ENGINE
//  새 기능: 사다리/수직 이동, 강화된 스킬 이펙트, 개선된 전투감
// ═══════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');

function resize(){
  const area = document.getElementById('game-area');
  canvas.width = area.clientWidth || 900;
  canvas.height = area.clientHeight || 440;
}
resize();
window.addEventListener('resize', ()=>{ resize(); if(G) buildLayout(); });

const W = () => canvas.width;
const H = () => canvas.height;

// ══════════════════════════════════════════════════════
// INPUT
// ══════════════════════════════════════════════════════
const KEY={}, JK={};
window.addEventListener('keydown', e=>{
  if(!KEY[e.key]){KEY[e.key]=true;JK[e.key]=true;}
  if([' ','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e=>KEY[e.key]=false);
function flushJK(){for(const k in JK) delete JK[k];}

// ══════════════════════════════════════════════════════
// PARTICLES — ENHANCED
// ══════════════════════════════════════════════════════
const PARTS=[];
function spawnParts(x,y,opts={}){
  const n=opts.n||8;
  for(let i=0;i<n;i++){
    const a=(opts.dir||0)+(Math.random()-.5)*(opts.spread||Math.PI*2);
    const s=(opts.sMin||1)+Math.random()*(opts.sMax||5);
    const col=Array.isArray(opts.col)?opts.col[Math.floor(Math.random()*opts.col.length)]:(opts.col||'#fff');
    PARTS.push({
      x,y,vx:Math.cos(a)*s+(opts.vxb||0),vy:Math.sin(a)*s-(opts.upb||0),
      life:1,decay:(opts.dMin||.018)+Math.random()*(opts.dMax||.028),
      col,sz:(opts.szMin||2)+Math.random()*(opts.szMax||5),
      glow:opts.glow||false,grav:opts.grav!==undefined?opts.grav:.14,
      type:opts.type||'c',spin:opts.spin?Math.random()*Math.PI*2:0,
    });
  }
}
function updateParts(dt){
  for(let i=PARTS.length-1;i>=0;i--){
    const p=PARTS[i];
    p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.grav*dt;p.vx*=.95;p.life-=p.decay*dt;
    if(p.spin) p.spin+=.08*dt;
    if(p.life<=0) PARTS.splice(i,1);
  }
}
function drawParts(camX,camY){
  ctx.save();
  for(const p of PARTS){
    const sx=p.x-camX, sy=p.y-camY;
    if(sx<-80||sx>W()+80||sy<-80||sy>H()+80) continue;
    ctx.globalAlpha=Math.max(0,p.life);
    if(p.glow){ctx.shadowColor=p.col;ctx.shadowBlur=p.sz*2.8;}
    ctx.fillStyle=p.col;
    if(p.type==='sq'){
      ctx.save();ctx.translate(sx,sy);ctx.rotate(p.spin);
      ctx.fillRect(-p.sz/2,-p.sz/2,p.sz,p.sz);ctx.restore();
    } else if(p.type==='star'){
      drawStar(ctx,sx,sy,p.sz,p.col,p.spin);
    } else {
      ctx.beginPath();ctx.arc(sx,sy,p.sz,0,Math.PI*2);ctx.fill();
    }
    if(p.glow) ctx.shadowBlur=0;
  }
  ctx.globalAlpha=1;ctx.restore();
}
function drawStar(ctx,x,y,r,col,rot=0){
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);
  ctx.fillStyle=col;ctx.beginPath();
  for(let i=0;i<5;i++){
    const a=i*Math.PI*2/5-Math.PI/2;
    const bi=a+Math.PI/5;
    if(i===0)ctx.moveTo(Math.cos(a)*r,Math.sin(a)*r);
    else ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r);
    ctx.lineTo(Math.cos(bi)*r*.4,Math.sin(bi)*r*.4);
  }
  ctx.closePath();ctx.fill();ctx.restore();
}

// ══════════════════════════════════════════════════════
// SKILL EFFECTS — VISUAL SYSTEM
// ══════════════════════════════════════════════════════
const EFFECTS=[];
function addEffect(type,x,y,opts={}){
  EFFECTS.push({type,x,y,life:1,maxLife:opts.life||1,t:0,...opts});
}
function updateEffects(dt){
  for(let i=EFFECTS.length-1;i>=0;i--){
    const e=EFFECTS[i];
    e.t+=dt;e.life=1-e.t/e.maxLife;
    if(e.life<=0) EFFECTS.splice(i,1);
  }
}
function drawEffects(camX,camY){
  ctx.save();
  for(const e of EFFECTS){
    const x=e.x-camX, y=e.y-camY;
    const a=Math.max(0,e.life);
    ctx.globalAlpha=a;
    switch(e.type){
      case 'slash': drawSlash(ctx,x,y,e); break;
      case 'circle': drawCircleWave(ctx,x,y,e); break;
      case 'beam': drawBeam(ctx,x,y,e); break;
      case 'explosion': drawExplosion(ctx,x,y,e); break;
      case 'holy': drawHoly(ctx,x,y,e); break;
      case 'poison_cloud': drawPoisonCloud(ctx,x,y,e); break;
      case 'ice_shard': drawIceShard(ctx,x,y,e); break;
      case 'lightning': drawLightningBolt(ctx,x,y,e); break;
      case 'dark_void': drawDarkVoid(ctx,x,y,e); break;
      case 'fire_pillar': drawFirePillar(ctx,x,y,e); break;
    }
  }
  ctx.globalAlpha=1;ctx.restore();
}

function drawSlash(ctx,x,y,e){
  const p=1-e.life;
  const r=(60+p*80)*e.scale;
  ctx.strokeStyle=e.col||'#fff';ctx.lineWidth=6*(e.life*.8+.2);
  ctx.shadowColor=e.col||'#fff';ctx.shadowBlur=20;
  ctx.beginPath();
  ctx.arc(x,y,r,e.ang-Math.PI*.3,e.ang+Math.PI*.3*(p*2+.3));
  ctx.stroke();ctx.shadowBlur=0;
  // extra lines
  for(let i=0;i<3;i++){
    const off=i*.12;
    ctx.globalAlpha=e.life*(1-i*.3);
    ctx.beginPath();ctx.arc(x,y,r*(1-off),e.ang-Math.PI*.15+off,e.ang+Math.PI*.2+off);
    ctx.stroke();
  }
}
function drawCircleWave(ctx,x,y,e){
  const p=1-e.life;
  const r=(20+p*150)*e.scale;
  ctx.strokeStyle=e.col||'#fff';ctx.lineWidth=4*e.life;
  ctx.shadowColor=e.col||'#fff';ctx.shadowBlur=18;
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();
  ctx.shadowBlur=0;
  if(e.life>.5){
    ctx.strokeStyle=e.col2||e.col||'#fff';ctx.lineWidth=2*e.life;
    ctx.beginPath();ctx.arc(x,y,r*.7,0,Math.PI*2);ctx.stroke();
  }
}
function drawBeam(ctx,x,y,e){
  const w=Math.max(2,20*e.life);
  const len=e.len||200;
  const grd=ctx.createLinearGradient(x,y,x+Math.cos(e.ang)*len,y+Math.sin(e.ang)*len);
  grd.addColorStop(0,e.col||'#fff');grd.addColorStop(1,'transparent');
  ctx.strokeStyle=grd;ctx.lineWidth=w;
  ctx.shadowColor=e.col||'#fff';ctx.shadowBlur=30;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+Math.cos(e.ang)*len,y+Math.sin(e.ang)*len);
  ctx.stroke();ctx.shadowBlur=0;
}
function drawExplosion(ctx,x,y,e){
  const p=1-e.life;
  const r=(10+p*120)*e.scale;
  const grd=ctx.createRadialGradient(x,y,0,x,y,r);
  grd.addColorStop(0,e.col||'#ff6600');grd.addColorStop(.4,e.col2||'#ff2200');grd.addColorStop(1,'transparent');
  ctx.fillStyle=grd;ctx.shadowColor=e.col||'#ff6600';ctx.shadowBlur=40;
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  // Smoke rings
  for(let i=0;i<3;i++){
    const rr=r*(1.2+i*.3);ctx.globalAlpha=e.life*(1-i*.28);
    ctx.strokeStyle='rgba(255,200,100,.4)';ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(x,y,rr,0,Math.PI*2);ctx.stroke();
  }
}
function drawHoly(ctx,x,y,e){
  const p=1-e.life;
  const r=(30+p*100)*e.scale;
  ctx.strokeStyle='rgba(255,240,150,.9)';ctx.lineWidth=5*e.life;
  ctx.shadowColor='#ffffaa';ctx.shadowBlur=35;
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;
  // Cross rays
  for(let i=0;i<8;i++){
    const a=i/8*Math.PI*2+e.t*.05;
    const rLen=r*(1+Math.sin(e.t*.1+i)*.2);
    ctx.globalAlpha=e.life*.7;ctx.strokeStyle='rgba(255,255,200,.6)';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(x+Math.cos(a)*r*.5,y+Math.sin(a)*r*.5);
    ctx.lineTo(x+Math.cos(a)*rLen,y+Math.sin(a)*rLen);ctx.stroke();
  }
}
function drawPoisonCloud(ctx,x,y,e){
  const p=1-e.life;
  for(let i=0;i<6;i++){
    const cx=x+Math.cos(i/6*Math.PI*2+e.t*.02)*30*(1+p);
    const cy=y+Math.sin(i/6*Math.PI*2+e.t*.02)*20*(1+p);
    const r=(25+p*40+i*8)*e.scale;
    const grd=ctx.createRadialGradient(cx,cy,0,cx,cy,r);
    grd.addColorStop(0,'rgba(80,200,60,.6)');grd.addColorStop(1,'transparent');
    ctx.globalAlpha=e.life*.7;ctx.fillStyle=grd;
    ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.fill();
  }
}
function drawIceShard(ctx,x,y,e){
  const p=1-e.life;
  for(let i=0;i<8;i++){
    const a=i/8*Math.PI*2+e.t*.03;
    const dist=p*80*(e.scale||1);
    const sx=x+Math.cos(a)*dist, sy=y+Math.sin(a)*dist;
    ctx.save();ctx.translate(sx,sy);ctx.rotate(a+e.t*.1);
    ctx.fillStyle=`rgba(100,200,255,${e.life*.9})`;
    ctx.shadowColor='#88ccff';ctx.shadowBlur=12;
    ctx.beginPath();ctx.moveTo(0,-12*e.life);ctx.lineTo(4*e.life,0);ctx.lineTo(0,12*e.life);ctx.lineTo(-4*e.life,0);
    ctx.closePath();ctx.fill();ctx.shadowBlur=0;ctx.restore();
  }
}
function drawLightningBolt(ctx,x,y,e){
  ctx.strokeStyle=`rgba(255,240,80,${e.life})`;ctx.lineWidth=3+e.life*4;
  ctx.shadowColor='#ffee00';ctx.shadowBlur=25;
  ctx.beginPath();
  const pts=[];const n=10;
  for(let i=0;i<=n;i++){
    pts.push({
      x:x+(Math.random()-.5)*60,
      y:y-200+i*(200/n)+(Math.random()-.5)*20
    });
  }
  ctx.moveTo(pts[0].x,pts[0].y);
  for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i].x,pts[i].y);
  ctx.stroke();ctx.shadowBlur=0;
  // glow core
  ctx.strokeStyle=`rgba(255,255,200,${e.life*.6})`;ctx.lineWidth=1;
  ctx.moveTo(x,y-200);ctx.lineTo(x,y);ctx.stroke();
}
function drawDarkVoid(ctx,x,y,e){
  const p=1-e.life;
  const r=(20+p*90)*e.scale;
  const grd=ctx.createRadialGradient(x,y,0,x,y,r);
  grd.addColorStop(0,'rgba(150,0,200,.95)');grd.addColorStop(.5,'rgba(80,0,120,.7)');grd.addColorStop(1,'transparent');
  ctx.fillStyle=grd;ctx.shadowColor='#8800cc';ctx.shadowBlur=40;
  ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  // spiral tendrils
  for(let i=0;i<6;i++){
    const a=i/6*Math.PI*2+e.t*.08+p*Math.PI;
    ctx.globalAlpha=e.life*.6;
    ctx.strokeStyle='rgba(200,80,255,.7)';ctx.lineWidth=2;
    ctx.beginPath();ctx.moveTo(x,y);
    ctx.quadraticCurveTo(x+Math.cos(a+.5)*r*.7,y+Math.sin(a+.5)*r*.7,x+Math.cos(a)*r,y+Math.sin(a)*r);
    ctx.stroke();
  }
}
function drawFirePillar(ctx,x,y,e){
  const w=(30+e.life*20)*e.scale;
  const h=200*e.scale;
  for(let i=0;i<8;i++){
    const yy=y-i*(h/8);
    const ww=w*(1-i/9);
    const grd=ctx.createRadialGradient(x,yy,0,x,yy,ww);
    const alpha=e.life*(1-i/9)*.8;
    grd.addColorStop(0,`rgba(255,240,100,${alpha})`);
    grd.addColorStop(.5,`rgba(255,100,0,${alpha*.7})`);
    grd.addColorStop(1,'transparent');
    ctx.fillStyle=grd;ctx.beginPath();ctx.arc(x,yy,ww,0,Math.PI*2);ctx.fill();
  }
}

// ══════════════════════════════════════════════════════
// CHARACTER RENDERER
// ══════════════════════════════════════════════════════
function drawChar(opts){
  const {x,y,f,walkPhase=0,atkPhase=0,hitFlash=0,dead=false,
    skinCol,hairCol,torsoCol,legsCol,weapon,offhand,headDeco,skillGlow,scale=1}=opts;
  const sc=scale;
  ctx.save();ctx.translate(x,y);
  if(dead){ctx.globalAlpha=.3;ctx.rotate(f*Math.PI/2);}
  if(f===-1) ctx.scale(-1,1);
  if(hitFlash>0) ctx.filter=`brightness(${2.5-hitFlash*.1}) saturate(.1)`;

  const ls=dead?0:Math.sin(walkPhase)*.44;
  const lb=dead?0:Math.abs(Math.sin(walkPhase))*.14;
  // Left leg
  ctx.save();ctx.translate(-5*sc,2*sc);ctx.rotate(Math.PI/2+ls);
  ctx.strokeStyle=legsCol;ctx.lineWidth=7*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);ctx.rotate(-lb);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();
  ctx.fillStyle=legsCol;ctx.beginPath();ctx.ellipse(4*sc,15*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
  // Right leg
  ctx.save();ctx.translate(5*sc,2*sc);ctx.rotate(Math.PI/2-ls);
  ctx.strokeStyle=legsCol;ctx.lineWidth=7*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
  ctx.translate(0,18*sc);ctx.rotate(lb);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();
  ctx.fillStyle=legsCol;ctx.beginPath();ctx.ellipse(4*sc,15*sc,7*sc,4*sc,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
  // Torso
  ctx.fillStyle=torsoCol;ctx.beginPath();ctx.roundRect(-10*sc,-28*sc,20*sc,30*sc,4*sc);ctx.fill();
  ctx.fillStyle='rgba(0,0,0,.35)';ctx.fillRect(-10*sc,-2*sc,20*sc,4*sc);
  // Arms
  const as=dead?0:Math.sin(walkPhase+Math.PI)*.32;
  const atk=dead?0:Math.sin(atkPhase)*.85;
  // Weapon arm
  ctx.save();ctx.translate(10*sc,-20*sc);ctx.rotate(-Math.PI/6+atk+as);
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();
  ctx.translate(0,17*sc);ctx.rotate(.2+atk*.5);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
  drawWeapon(ctx,weapon,sc,atkPhase,skillGlow);
  ctx.restore();
  // Off arm
  ctx.save();ctx.translate(-10*sc,-20*sc);ctx.rotate(Math.PI/6-as);
  ctx.strokeStyle=skinCol;ctx.lineWidth=6*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();
  ctx.translate(0,17*sc);ctx.rotate(-.15);
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
  if(offhand) drawOffhand(ctx,offhand,sc);
  ctx.restore();
  // Head
  ctx.fillStyle=skinCol;ctx.beginPath();ctx.arc(0,-36*sc,12*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=hairCol;ctx.beginPath();ctx.arc(0,-38*sc,11*sc,Math.PI,Math.PI*2);ctx.fill();
  ctx.fillRect(-11*sc,-38*sc,22*sc,6*sc);
  ctx.fillStyle='#fff';ctx.beginPath();ctx.arc(4*sc,-37*sc,3.2*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=dead?'#555':'#1a0a00';ctx.beginPath();ctx.arc(5*sc,-37*sc,1.8*sc,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle='rgba(0,0,0,.55)';ctx.lineWidth=1.4*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(1*sc,-42*sc);ctx.lineTo(7*sc,-41*sc);ctx.stroke();
  if(headDeco) drawHeadDeco(ctx,headDeco,sc);
  if(skillGlow){
    ctx.globalAlpha=.38+Math.sin(Date.now()*.006)*.18;
    ctx.shadowColor=skillGlow;ctx.shadowBlur=28;
    ctx.strokeStyle=skillGlow;ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.arc(0,-14*sc,28*sc,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;ctx.globalAlpha=1;
  }
  ctx.filter='none';ctx.restore();
}

function drawWeapon(ctx,wpn,sc,atkPhase,glow){
  if(!wpn) return;
  const sw=Math.sin(atkPhase)*.28;
  ctx.save();ctx.rotate(-Math.PI/4+sw);
  if(glow){ctx.shadowColor=glow;ctx.shadowBlur=16;}
  switch(wpn){
    case 'sword':
      ctx.fillStyle='#8B6914';ctx.fillRect(-3*sc,0,6*sc,11*sc);
      ctx.fillStyle='#C0A020';ctx.fillRect(-8*sc,9*sc,16*sc,4*sc);
      ctx.fillStyle='#d0e8ff';ctx.beginPath();ctx.moveTo(-2*sc,13*sc);ctx.lineTo(0,-30*sc);ctx.lineTo(2*sc,13*sc);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.55)';ctx.beginPath();ctx.moveTo(0,13*sc);ctx.lineTo(.5*sc,-30*sc);ctx.lineTo(2*sc,13*sc);ctx.closePath();ctx.fill();
      break;
    case 'axe':
      ctx.fillStyle='#664422';ctx.fillRect(-3*sc,0,6*sc,30*sc);
      ctx.fillStyle='#a07838';ctx.beginPath();ctx.moveTo(-2*sc,10*sc);ctx.lineTo(-20*sc,-10*sc);ctx.lineTo(-20*sc,12*sc);ctx.lineTo(-2*sc,28*sc);ctx.closePath();ctx.fill();
      ctx.fillStyle='rgba(255,200,80,.35)';ctx.beginPath();ctx.moveTo(-2*sc,10*sc);ctx.lineTo(-20*sc,-10*sc);ctx.lineTo(-18*sc,2*sc);ctx.lineTo(-2*sc,18*sc);ctx.closePath();ctx.fill();
      break;
    case 'staff':
      ctx.fillStyle='#662288';ctx.fillRect(-2.5*sc,-30*sc,5*sc,50*sc);
      ctx.fillStyle='rgba(210,90,255,.85)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=14;
      ctx.beginPath();ctx.arc(0,-30*sc,8*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
      break;
    case 'gun':
      ctx.fillStyle='#334455';ctx.fillRect(-5*sc,-4*sc,30*sc,10*sc);
      ctx.fillStyle='#22334d';ctx.fillRect(20*sc,-8*sc,10*sc,18*sc);
      ctx.fillStyle='#556677';ctx.fillRect(-8*sc,0,5*sc,8*sc);
      if(Math.sin(atkPhase)>.6){ctx.fillStyle='rgba(255,240,100,.8)';ctx.shadowColor='#ffcc00';ctx.shadowBlur=18;ctx.beginPath();ctx.arc(30*sc,-4*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
      break;
    case 'dual':
      ctx.fillStyle='#d0e8ff';
      ctx.save();ctx.rotate(-.28);ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-22*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();ctx.restore();
      ctx.save();ctx.rotate(.28);ctx.translate(9*sc,0);ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-22*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();ctx.restore();
      break;
    case 'scythe':
      ctx.fillStyle='#334422';ctx.fillRect(-2.5*sc,-40*sc,5*sc,60*sc);
      ctx.strokeStyle='#556644';ctx.lineWidth=4*sc;
      ctx.beginPath();ctx.arc(-10*sc,-30*sc,25*sc,-Math.PI*.22,Math.PI*.38);ctx.stroke();
      ctx.strokeStyle='rgba(100,255,100,.38)';ctx.lineWidth=2*sc;
      ctx.beginPath();ctx.arc(-10*sc,-30*sc,25*sc,-Math.PI*.2,Math.PI*.22);ctx.stroke();
      break;
    case 'hammer':
      ctx.fillStyle='#665544';ctx.fillRect(-3.5*sc,-10*sc,7*sc,42*sc);
      ctx.fillStyle='#998877';ctx.fillRect(-14*sc,-22*sc,28*sc,22*sc);
      ctx.fillStyle='rgba(255,200,100,.18)';ctx.fillRect(-12*sc,-20*sc,24*sc,8*sc);
      break;
  }
  ctx.shadowBlur=0;ctx.restore();
}
function drawOffhand(ctx,item,sc){
  ctx.save();ctx.rotate(Math.PI*.1);
  switch(item){
    case 'shield':
      ctx.fillStyle='#334455';ctx.beginPath();ctx.roundRect(-8*sc,0,16*sc,20*sc,3*sc);ctx.fill();
      ctx.strokeStyle='#445566';ctx.lineWidth=2*sc;ctx.stroke();
      ctx.fillStyle='rgba(100,150,220,.3)';ctx.beginPath();ctx.arc(0,10*sc,5*sc,0,Math.PI*2);ctx.fill();
      break;
    case 'dagger':
      ctx.fillStyle='#aabbcc';ctx.beginPath();ctx.moveTo(-1*sc,0);ctx.lineTo(0,-15*sc);ctx.lineTo(1*sc,0);ctx.closePath();ctx.fill();
      break;
    case 'tome':
      ctx.fillStyle='#442244';ctx.fillRect(-7*sc,0,14*sc,18*sc);
      ctx.fillStyle='rgba(200,100,255,.5)';ctx.fillRect(-5*sc,2*sc,10*sc,14*sc);
      break;
  }
  ctx.restore();
}
function drawHeadDeco(ctx,deco,sc){
  switch(deco){
    case 'helm':
      ctx.fillStyle='#556677';ctx.beginPath();ctx.arc(0,-38*sc,14*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-14*sc,-38*sc,28*sc,5*sc);
      ctx.fillStyle='rgba(150,200,255,.28)';ctx.beginPath();ctx.arc(0,-38*sc,12*sc,Math.PI,Math.PI*2);ctx.fill();
      break;
    case 'wizard-hat':
      ctx.fillStyle='#441166';ctx.beginPath();ctx.moveTo(-12*sc,-28*sc);ctx.lineTo(0,-58*sc);ctx.lineTo(12*sc,-28*sc);ctx.closePath();ctx.fill();
      ctx.fillRect(-14*sc,-30*sc,28*sc,5*sc);
      ctx.fillStyle='rgba(200,100,255,.45)';ctx.beginPath();ctx.arc(0,-56*sc,3*sc,0,Math.PI*2);ctx.fill();
      break;
    case 'hood':
      ctx.fillStyle='#222233';ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      break;
    case 'cap':
      ctx.fillStyle='#334433';ctx.beginPath();ctx.arc(0,-38*sc,13*sc,Math.PI,Math.PI*2);ctx.fill();
      ctx.fillRect(-14*sc,-40*sc,28*sc,6*sc);
      break;
    case 'headband':
      ctx.strokeStyle='#cc3322';ctx.lineWidth=4*sc;
      ctx.beginPath();ctx.arc(0,-36*sc,13*sc,Math.PI*1.1,Math.PI*1.9);ctx.stroke();
      break;
    case 'crown':
      ctx.fillStyle='#cc8800';
      ctx.beginPath();ctx.moveTo(-12*sc,-38*sc);ctx.lineTo(-12*sc,-50*sc);ctx.lineTo(-6*sc,-44*sc);
      ctx.lineTo(0,-52*sc);ctx.lineTo(6*sc,-44*sc);ctx.lineTo(12*sc,-50*sc);ctx.lineTo(12*sc,-38*sc);ctx.closePath();ctx.fill();
      break;
  }
}

// ══════════════════════════════════════════════════════
// MONSTER RENDERER
// ══════════════════════════════════════════════════════
function drawMonster(e,camX,camY){
  const x=e.x-camX, y=e.y-camY;
  const dead=!e.alive;
  const sc=e.drawScale||1;
  ctx.save();ctx.translate(x+e.w/2,y+e.h*.88);
  if(dead){ctx.globalAlpha=.28;ctx.rotate(e.f*Math.PI/2);}
  if(e.f===1) ctx.scale(-1,1);
  if(e.hitFlash>0) ctx.filter=`brightness(${2.8-e.hitFlash*.12})`;
  if(e.frozen>0) ctx.filter='hue-rotate(195deg) brightness(1.85) saturate(2.2)';

  const wp=e.walkPhase||0,ap=e.atkPhase||0;
  const drawFn=MONSTER_DRAW[e.drawType]||drawMonster_basic;
  drawFn(ctx,sc,wp,ap,e);

  ctx.filter='none';ctx.restore();

  // HP bar (only when damaged)
  if(!dead&&e.hp<e.maxHp){
    const hpPct=Math.max(0,e.hp/e.maxHp);
    const bw=Math.max(38,e.w+8),bx=x+e.w/2-bw/2,by=y-12;
    ctx.fillStyle='rgba(0,0,0,.65)';ctx.fillRect(bx,by,bw,6);
    ctx.fillStyle=hpPct>.5?'#22cc22':hpPct>.25?'#ccaa00':'#cc2200';
    ctx.fillRect(bx,by,bw*hpPct,6);
    if(e.frozen>0){ctx.fillStyle='rgba(100,180,255,.42)';ctx.fillRect(bx,by,bw,6);}
    // status dots
    if(e.poison>0){ctx.fillStyle='#44ff44';ctx.beginPath();ctx.arc(bx+bw+5,by+3,3,0,Math.PI*2);ctx.fill();}
    if(e.cursed>0){ctx.fillStyle='#aa44ff';ctx.beginPath();ctx.arc(bx+bw+12,by+3,3,0,Math.PI*2);ctx.fill();}
  }
}

function drawMonster_basic(ctx,sc,wp,ap,e){
  const bc=e.bodyCol||'#556644';const hc=e.headCol||'#667755';const lc=e.limbCol||'#445533';
  const ls=Math.sin(wp)*.38;
  for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
    ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
    ctx.strokeStyle=lc;ctx.lineWidth=6*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();ctx.restore();
  }
  const as=Math.sin(ap)*.6;
  ctx.save();ctx.translate(10*sc,-13*sc);ctx.rotate(-Math.PI/6+as);
  ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();ctx.restore();
  ctx.save();ctx.translate(-10*sc,-13*sc);ctx.rotate(Math.PI/6-as);
  ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();ctx.restore();
  ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-10*sc,-26*sc,20*sc,26*sc,3*sc);ctx.fill();
  ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-32*sc,10*sc,9*sc,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff2200';ctx.beginPath();ctx.arc(-4*sc,-34*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(4*sc,-34*sc,3*sc,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#ff6600';ctx.beginPath();ctx.arc(-3*sc,-34*sc,1.4*sc,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(5*sc,-34*sc,1.4*sc,0,Math.PI*2);ctx.fill();
}

const MONSTER_DRAW = {
  goblin:(ctx,sc,wp,ap,e)=>{
    const lc=e.limbCol||'#22aa44';const bc=e.bodyCol||'#338855';const hc=e.headCol||'#22aa33';
    const ls=Math.sin(wp)*.5;const as=Math.sin(ap)*.7;
    for(const [ox,side] of [[-3*sc,-1],[3*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();ctx.restore();
    }
    ctx.save();ctx.translate(8*sc,-10*sc);ctx.rotate(-Math.PI/6+as);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,11*sc);ctx.stroke();
    ctx.translate(0,11*sc);ctx.rotate(.2);
    ctx.fillStyle='#aabbcc';ctx.beginPath();ctx.moveTo(-1*sc,0);ctx.lineTo(0,-13*sc);ctx.lineTo(1*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-8*sc,-10*sc);ctx.rotate(Math.PI/6-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,11*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-8*sc,-20*sc,16*sc,20*sc,3*sc);ctx.fill();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-24*sc,10*sc,8*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=hc;
    ctx.beginPath();ctx.ellipse(-12*sc,-24*sc,4.5*sc,3*sc,-Math.PI/4,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(12*sc,-24*sc,4.5*sc,3*sc,Math.PI/4,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ffcc00';ctx.beginPath();ctx.arc(-3*sc,-26*sc,2.4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(3*sc,-26*sc,2.4*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#440000';ctx.beginPath();ctx.arc(-2*sc,-26*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-26*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';ctx.fillRect(-3*sc,-20*sc,2*sc,2.5*sc);ctx.fillRect(1*sc,-20*sc,2*sc,2.5*sc);
  },
  skeleton:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.38;const as=Math.sin(ap)*.65;const bc='#d4c8a0';const lc='#c4b888';
    for(const [ox,side] of [[-4*sc,-1],[4*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=4*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();
      ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,9*sc,3*sc,0,Math.PI*2);ctx.fill();
      ctx.beginPath();ctx.moveTo(0,9*sc);ctx.lineTo(0,15*sc);ctx.stroke();ctx.restore();
    }
    ctx.strokeStyle=bc;ctx.lineWidth=2*sc;
    for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(0,(-6-i*5)*sc,8*sc,0,Math.PI);ctx.stroke();}
    ctx.strokeStyle=bc;ctx.lineWidth=3*sc;ctx.beginPath();ctx.moveTo(0,-6*sc);ctx.lineTo(0,-27*sc);ctx.stroke();
    ctx.save();ctx.translate(10*sc,-21*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
    ctx.translate(0,13*sc);ctx.rotate(.2+as*.3);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,11*sc);ctx.stroke();
    ctx.translate(0,11*sc);ctx.rotate(-Math.PI/6);
    ctx.fillStyle='#ddd';ctx.beginPath();ctx.moveTo(-1.5*sc,0);ctx.lineTo(0,-22*sc);ctx.lineTo(1.5*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-10*sc,-21*sc);ctx.rotate(Math.PI/5-as*.5);
    ctx.strokeStyle=bc;ctx.lineWidth=3.5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.arc(0,-33*sc,11*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=bc;ctx.fillRect(-8*sc,-25*sc,16*sc,6*sc);
    ctx.fillStyle='#111';ctx.beginPath();ctx.ellipse(-4*sc,-35*sc,3.5*sc,3*sc,0,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(4*sc,-35*sc,3.5*sc,3*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(0,200,255,.55)';ctx.beginPath();ctx.arc(-4*sc,-35*sc,1.4*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-35*sc,1.4*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#111';for(let t=-3;t<=3;t++) ctx.fillRect((t*2.4-1)*sc,-24*sc,2*sc,4*sc);
  },
  orc:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.32;const as=Math.sin(ap)*.55;
    const bc='#3a5a2a';const lc='#2a4a1a';const hc='#4a6a3a';
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.lineWidth=8*sc;ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,28*sc);ctx.stroke();
      ctx.restore();
    }
    ctx.save();ctx.translate(14*sc,-19*sc);ctx.rotate(-Math.PI/5+as);
    ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();
    ctx.translate(0,17*sc);ctx.rotate(.2+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();
    ctx.fillStyle='#666';ctx.fillRect(-3*sc,0,6*sc,8*sc);
    ctx.fillStyle='#888';ctx.beginPath();ctx.moveTo(-2*sc,6*sc);ctx.lineTo(-20*sc,-8*sc);ctx.lineTo(-20*sc,12*sc);ctx.lineTo(-2*sc,22*sc);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-14*sc,-19*sc);ctx.rotate(Math.PI/5-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,19*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-14*sc,-35*sc,28*sc,35*sc,4*sc);ctx.fill();
    ctx.fillStyle='#445533';ctx.fillRect(-12*sc,-29*sc,24*sc,12*sc);
    ctx.strokeStyle='#556644';ctx.lineWidth=1.5*sc;ctx.beginPath();ctx.moveTo(0,-35*sc);ctx.lineTo(0,0);ctx.stroke();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-41*sc,14*sc,12*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ddd';
    ctx.beginPath();ctx.moveTo(-6*sc,-33*sc);ctx.lineTo(-10*sc,-25*sc);ctx.lineTo(-4*sc,-33*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(6*sc,-33*sc);ctx.lineTo(10*sc,-25*sc);ctx.lineTo(4*sc,-33*sc);ctx.fill();
    ctx.fillStyle='#ff2200';ctx.beginPath();ctx.arc(-5*sc,-43*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-43*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#cc2200';ctx.fillRect(-2*sc,-55*sc,4*sc,16*sc);
  },
  mage_enemy:(ctx,sc,wp,ap,e)=>{
    const as=Math.sin(ap)*.45;const bc='#2a1a4a';const lc='#3a2a5a';const hc='#3a2a6a';
    ctx.fillStyle=bc;ctx.beginPath();ctx.moveTo(-14*sc,0);ctx.lineTo(14*sc,0);ctx.lineTo(10*sc,-44*sc);ctx.lineTo(-10*sc,-44*sc);ctx.closePath();ctx.fill();
    ctx.strokeStyle='rgba(140,90,255,.48)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-14*sc,0);ctx.lineTo(-10*sc,-44*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(14*sc,0);ctx.lineTo(10*sc,-44*sc);ctx.stroke();
    ctx.save();ctx.translate(10*sc,-29*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();
    ctx.translate(0,15*sc);ctx.fillStyle='#7733aa';ctx.fillRect(-2*sc,0,4*sc,-28*sc);
    ctx.fillStyle='rgba(190,90,255,.9)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(0,-28*sc,7*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.restore();
    ctx.save();ctx.translate(-10*sc,-29*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,15*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=hc;ctx.beginPath();ctx.arc(0,-49*sc,11*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#330066';ctx.beginPath();ctx.moveTo(-13*sc,-43*sc);ctx.lineTo(0,-67*sc);ctx.lineTo(13*sc,-43*sc);ctx.closePath();ctx.fill();
    ctx.fillRect(-15*sc,-45*sc,30*sc,5*sc);
    ctx.fillStyle='rgba(180,80,255,.6)';ctx.beginPath();ctx.arc(0,-65*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='rgba(200,100,255,.9)';ctx.shadowColor='#cc44ff';ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(-4*sc,-50*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-50*sc,3*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },
  demon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.28;const as=Math.sin(ap)*.55;
    const bc='#4a0a0a';const lc='#3a0808';const hc='#550a0a';
    for(const [ox,side] of [[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,27*sc);ctx.stroke();
      ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(2*sc,27*sc,5*sc,4*sc,0,0,Math.PI*2);ctx.fill();ctx.restore();
    }
    ctx.fillStyle='rgba(80,0,0,.78)';
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(-44*sc,-55*sc);ctx.lineTo(-30*sc,-10*sc);ctx.lineTo(-5*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(44*sc,-55*sc);ctx.lineTo(30*sc,-10*sc);ctx.lineTo(5*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.save();ctx.translate(12*sc,-21*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();
    ctx.translate(0,17*sc);ctx.rotate(.3+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();
    ctx.strokeStyle='#ff2200';ctx.lineWidth=2*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*3*sc,13*sc),ctx.lineTo(c*6*sc,21*sc),ctx.stroke();
    ctx.restore();
    ctx.save();ctx.translate(-12*sc,-21*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-12*sc,-37*sc,24*sc,37*sc,4*sc);ctx.fill();
    ctx.fillStyle='rgba(255,0,0,.14)';ctx.beginPath();ctx.arc(0,-19*sc,10*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-44*sc,13*sc,11*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#660000';
    ctx.beginPath();ctx.moveTo(-8*sc,-52*sc);ctx.lineTo(-14*sc,-68*sc);ctx.lineTo(-4*sc,-54*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(8*sc,-52*sc);ctx.lineTo(14*sc,-68*sc);ctx.lineTo(4*sc,-54*sc);ctx.fill();
    ctx.fillStyle='#ff0000';ctx.shadowColor='#ff0000';ctx.shadowBlur=9;
    ctx.beginPath();ctx.arc(-4*sc,-46*sc,3.3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-46*sc,3.3*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },
  golem:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.13;const as=Math.sin(ap)*.35;
    const bc='#6a5a4a';const lc='#7a6a5a';const hc='#8a7a6a';
    for(const [ox,side] of [[-8*sc,-1],[8*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side*.5);
      ctx.fillStyle=bc;ctx.fillRect(-6*sc,-2*sc,12*sc,22*sc);
      ctx.fillStyle=lc;ctx.fillRect(-4*sc,0,8*sc,5*sc);ctx.restore();
    }
    ctx.save();ctx.translate(18*sc,-25*sc);ctx.rotate(-Math.PI/6+as);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,22*sc);ctx.fillRect(-5*sc,22*sc,14*sc,17*sc);ctx.restore();
    ctx.save();ctx.translate(-18*sc,-25*sc);ctx.rotate(Math.PI/6-as*.5);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,22*sc);ctx.fillRect(-9*sc,22*sc,14*sc,17*sc);ctx.restore();
    ctx.fillStyle=bc;ctx.fillRect(-18*sc,-43*sc,36*sc,43*sc);
    ctx.strokeStyle='rgba(0,0,0,.38)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-5*sc,-39*sc);ctx.lineTo(2*sc,-19*sc);ctx.lineTo(-3*sc,-9*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(8*sc,-34*sc);ctx.lineTo(12*sc,-14*sc);ctx.stroke();
    ctx.fillStyle='rgba(255,150,0,.62)';ctx.shadowColor='#ff8800';ctx.shadowBlur=18;
    ctx.beginPath();ctx.arc(0,-21*sc,6*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.fillStyle=hc;ctx.fillRect(-14*sc,-61*sc,28*sc,21*sc);
    ctx.fillStyle='rgba(0,0,0,.4)';ctx.fillRect(-10*sc,-57*sc,8*sc,10*sc);ctx.fillRect(2*sc,-57*sc,8*sc,10*sc);
    ctx.fillStyle='rgba(255,180,50,.85)';ctx.shadowColor='#ffaa00';ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(-6*sc,-52*sc,3*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(6*sc,-52*sc,3*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },
  dragon:(ctx,sc,wp,ap,e)=>{
    const ls=Math.sin(wp)*.22;const as=Math.sin(ap)*.48;
    const bc='#1a3a1a';const sc2='#2a5a2a';const hc='#1a4a1a';
    // tail
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(15*sc,-10*sc);ctx.quadraticCurveTo(40*sc,10*sc,30*sc,-20*sc);ctx.stroke();
    ctx.lineWidth=4*sc;ctx.beginPath();ctx.moveTo(30*sc,-20*sc);ctx.lineTo(40*sc,-14*sc);ctx.stroke();
    // wing
    ctx.fillStyle='rgba(30,60,30,.7)';
    ctx.beginPath();ctx.moveTo(-5*sc,-35*sc);ctx.lineTo(-40*sc,-60*sc);ctx.lineTo(-35*sc,-20*sc);ctx.lineTo(-5*sc,-15*sc);ctx.closePath();ctx.fill();
    for(const [ox,side] of [[-7*sc,-1],[7*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*side);
      ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.strokeStyle='#aaa';ctx.lineWidth=2*sc;
      for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,18*sc),ctx.lineTo(c*6*sc,25*sc),ctx.stroke();ctx.restore();
    }
    ctx.save();ctx.translate(14*sc,-23*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();
    ctx.strokeStyle='#aaa';ctx.lineWidth=2*sc;
    for(let c=-1;c<=1;c++) ctx.beginPath(),ctx.moveTo(c*4*sc,16*sc),ctx.lineTo(c*7*sc,24*sc),ctx.stroke();ctx.restore();
    ctx.save();ctx.translate(-14*sc,-23*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.ellipse(0,-19*sc,16*sc,21*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=sc2;for(let i=0;i<3;i++) ctx.beginPath(),ctx.arc(0,(-29+i*8)*sc,6*sc,0,Math.PI*2),ctx.fill();
    ctx.fillStyle=bc;ctx.fillRect(-7*sc,-41*sc,14*sc,13*sc);
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-49*sc,14*sc,12*sc,-.28,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(8*sc,-47*sc,8*sc,5*sc,-.18,0,Math.PI*2);ctx.fill();
    if(ap>.5){ctx.fillStyle='rgba(255,150,0,.85)';ctx.shadowColor='#ff6600';ctx.shadowBlur=14;ctx.beginPath();ctx.arc(14*sc,-47*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
    ctx.fillStyle='#ffaa00';ctx.beginPath();ctx.ellipse(-4*sc,-53*sc,4*sc,3*sc,.28,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(-3*sc,-53*sc,2*sc,2*sc,.28,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#888';ctx.strokeStyle='#888';ctx.lineWidth=3*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(-8*sc,-57*sc);ctx.lineTo(-12*sc,-69*sc);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-2*sc,-59*sc);ctx.lineTo(-4*sc,-71*sc);ctx.stroke();
  },
};

// ══════════════════════════════════════════════════════
// LAYOUT — MULTI-FLOOR WITH LADDERS
// ══════════════════════════════════════════════════════
const STAGE_W = 3800;
let layout = null; // {floors, ladders, spawnPoints}

function buildLayout(){
  const floorCount = 4;
  const floorH = Math.round((H()-66-62) / floorCount);
  const floors = [];
  const ladders = [];
  const baseY = H() - 62; // bottom floor y

  for(let f=0; f<floorCount; f++){
    const y = baseY - f * floorH;
    floors.push({y, idx:f});
  }

  // Ground floor spans entire width
  floors[0].platforms = [{x:0, w:STAGE_W, y:floors[0].y, ground:true}];

  // Upper floors: multiple platforms per floor
  for(let f=1; f<floorCount; f++){
    const y = floors[f].y;
    const plats = [];
    const segW = 320 + Math.random()*100;
    for(let x=200; x < STAGE_W-400; x += segW + 80 + Math.random()*120){
      const w = 250 + Math.random()*150;
      plats.push({x, w, y, ground:false});
    }
    floors[f].platforms = plats;
  }

  // Ladders: connect each floor pair at random positions
  for(let f=0; f<floorCount-1; f++){
    const f0 = floors[f], f1 = floors[f+1];
    const laddersOnFloor = 3 + Math.floor(Math.random()*2);
    const placed = new Set();
    const candidates = f1.platforms || [];
    for(let i=0; i<laddersOnFloor; i++){
      let lx;
      if(candidates.length && Math.random()>.3){
        const pl = candidates[Math.floor(Math.random()*candidates.length)];
        lx = pl.x + pl.w/2 + (Math.random()-.5)*80;
      } else {
        lx = 400 + Math.random()*(STAGE_W-800);
      }
      lx = Math.round(lx / 40) * 40; // snap
      if(placed.has(lx)) continue;
      placed.add(lx);
      ladders.push({
        x: lx, w: 24,
        y1: f1.y,   // top of ladder
        y2: f0.y,   // bottom of ladder
        floorFrom: f, floorTo: f+1,
      });
    }
  }

  layout = {floors, ladders};
  return layout;
}

function getGroundY(){
  return layout ? layout.floors[0].y : (H()-62);
}

// Check if entity is on a platform/ground
function getFloorBelow(x, y, vy){
  if(!layout) return null;
  let best = null, bestDist = 999;
  for(const floor of layout.floors){
    for(const pl of floor.platforms){
      if(x+20 >= pl.x && x < pl.x + pl.w){
        const dist = pl.y - (y);
        if(dist >= -4 && dist < bestDist + 12 && vy >= -1){
          bestDist = dist;
          best = pl;
        }
      }
    }
  }
  return best;
}

// Check if on a ladder
function getNearbyLadder(x, y, h){
  if(!layout) return null;
  for(const ld of layout.ladders){
    if(Math.abs(x + 20 - ld.x) < 28 && y < ld.y2 + 20 && y + h > ld.y1 - 20){
      return ld;
    }
  }
  return null;
}

// ══════════════════════════════════════════════════════
// CHARACTER CLASSES
// ══════════════════════════════════════════════════════
const CLASSES = {
  warrior:{
    name:'워리어',role:'근접 전사',icon:'⚔️',
    skinCol:'#f5c090',hairCol:'#1a0800',torsoCol:'#3a4455',legsCol:'#2a3344',
    headDeco:'helm',weapon:'sword',offhand:'shield',
    hp:380,mp:80,atk:42,def:16,spd:4.6,jmp:13.5,
    desc:'높은 HP·DEF. 방패 방어로 피해 감소.',col:'#5588cc',
    skills:[
      {name:'검격',icon:'⚔️',key:'A',mp:8,cd:1.5,desc:'강력한 검 공격 1.8배',col:'#aabbcc',
       fn:(p,G)=>{
         hitAOE(p.x+(p.f>0?p.w:-80),p.y-20,85,75,dmg(p,1.8),true);
         addEffect('slash',p.x+(p.f>0?p.w+20:-20)-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#aabbcc',ang:p.f>0?0:Math.PI,scale:1});
       }},
      {name:'방패 강타',icon:'🛡️',key:'S',mp:18,cd:4,desc:'방패 충격 스턴',col:'#8899aa',
       fn:(p,G)=>{
         p.vx=p.f*22;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-85),p.y-5,85,65,dmg(p,1.4),true,{stun:110});
           addEffect('circle',p.x+(p.f>0?p.w+30:-30)-G.cam,p.y+p.h/2-G.camY,{life:22,col:'#8899aa',col2:'#aabbff',scale:.8});
         },130);
       }},
      {name:'돌격',icon:'💨',key:'D',mp:24,cd:5,desc:'돌진 후 강타 2.2배',col:'#ccdde0',
       fn:(p,G)=>{
         p.vx=p.f*38;p.invincible=40;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w-10:-95),p.y-22,115,85,dmg(p,2.2),true);
           addEffect('explosion',p.x+(p.f>0?p.w+50:-50)-G.cam,p.y+p.h/2-G.camY,{life:25,col:'#aabbcc',col2:'#8899cc',scale:1.2});
           shake(5,14);
         },210);
       }},
      {name:'회오리',icon:'🌀',key:'F',mp:38,cd:7,desc:'360도 광역 2배',col:'#99aabb',
       fn:(p,G)=>{
         hitAOE(p.x-75,p.y-45,p.w+155,p.h+90,dmg(p,2),false);
         for(let i=0;i<8;i++){
           const a=i/8*Math.PI*2;
           addEffect('beam',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:15,col:'#aabbff',ang:a,len:80,scale:1});
         }
         shake(5,12);
       }},
      {name:'무적 베기',icon:'🗡️',key:'G',mp:65,cd:16,desc:'5초 무적+자힐+3배',col:'#eeffff',
       fn:(p,G)=>{
         p.invincible=300;p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.2));
         hitAOE(p.x-65,p.y-55,p.w+140,125,dmg(p,3),true);
         addEffect('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#eeffff',scale:2});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:30,col:['#eeffff','#aaddff'],glow:true,sMin:2,sMax:8});
         shake(8,22);
       }},
    ]
  },
  mage:{
    name:'마법사',role:'원소 마법사',icon:'🔮',
    skinCol:'#c07840',hairCol:'#1a0800',torsoCol:'#331155',legsCol:'#220f44',
    headDeco:'wizard-hat',weapon:'staff',offhand:'tome',
    hp:210,mp:280,atk:62,def:5,spd:4.0,jmp:13.0,
    desc:'강력한 마법. MP관리 필수.',col:'#aa44ff',
    skills:[
      {name:'파이어볼',icon:'🔥',key:'A',mp:18,cd:1.5,desc:'화염탄 3발',col:'#ff6600',
       fn:(p,G)=>{
         for(let i=0;i<3;i++) setTimeout(()=>proj(p.x+p.f*52,p.y+20,p.f*16,(Math.random()-.5)*.6,dmg(p,1.7),'#ff6600','player',{sz:13,emoji:'🔥',life:62,trail:true}),i*95);
       }},
      {name:'아이스 스피어',icon:'❄️',key:'S',mp:28,cd:4,desc:'빙결 마법구',col:'#44aaff',
       fn:(p,G)=>{
         proj(p.x+p.f*52,p.y+18,p.f*15,0,dmg(p,2.4),'#44aaff','player',{sz:15,emoji:'❄️',life:72,
           onHit:(e)=>{
             e.frozen=Math.max(e.frozen||0,200);
             addEffect('ice_shard',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:30,scale:1.2});
           }});
       }},
      {name:'라이트닝',icon:'⚡',key:'D',mp:36,cd:5,desc:'낙뢰 3연격',col:'#ffee00',
       fn:(p,G)=>{
         for(let i=0;i<3;i++) setTimeout(()=>{
           const tx=p.x+p.f*(140+i*100)-G.cam;const ty=p.y+p.h/2-G.camY;
           addEffect('lightning',tx+G.cam,ty+G.camY,{life:20,scale:1});
           setTimeout(()=>hitAOE(G.cam+tx-30,ty+G.camY-200,60,220,dmg(p,2.2),true),60);
           spawnParts(tx,ty,{n:10,col:['#ffee00','#ffdd44'],glow:true,spread:.5,dir:Math.PI*.5,sMin:3,sMax:9});
         },i*180);
       }},
      {name:'메테오',icon:'☄️',key:'F',mp:72,cd:12,desc:'운석 5개 낙하 3.5배',col:'#ff4400',
       fn:(p,G)=>{
         for(let i=0;i<5;i++) setTimeout(()=>{
           const tx=p.x+p.f*100+(Math.random()-.5)*300;
           proj(tx,-60,(Math.random()-.5)*2.5,18,dmg(p,3.5),'#ff4400','player',{sz:22,emoji:'☄️',life:75,grav:.38,
             onHit:(e)=>{addEffect('explosion',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:30,col:'#ff4400',col2:'#ff8800',scale:1.5});}
           });
           shake(4,9);
         },i*165);
       }},
      {name:'타임스탑',icon:'⏰',key:'G',mp:90,cd:22,desc:'4초 전체 빙결',col:'#8844ff',
       fn:(p,G)=>{
         freezeAll(240);
         addEffect('dark_void',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:50,col:'#8844ff',scale:2.5});
       }},
    ]
  },
  rogue:{
    name:'로그',role:'암살자',icon:'🗝️',
    skinCol:'#e8a870',hairCol:'#1a0800',torsoCol:'#1a2a1a',legsCol:'#111a11',
    headDeco:'hood',weapon:'dual',offhand:'dagger',
    hp:250,mp:190,atk:56,def:7,spd:6.0,jmp:16.0,
    desc:'초고속 이동, 크리+25%, 연속 참격.',col:'#22cc55',
    skills:[
      {name:'3연참',icon:'🗡️',key:'A',mp:10,cd:1.2,desc:'초속 3연타',col:'#44ee66',
       fn:(p,G)=>{
         for(let i=0;i<3;i++) setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-72),p.y-12,74,64,dmg(p,1.5),Math.random()<.35);
           addEffect('slash',p.x+(p.f>0?p.w+15:-15)-G.cam,p.y+p.h/2-G.camY,{life:12,col:'#44ee66',ang:p.f>0?-.2:.2,scale:.8});
         },i*105);
       }},
      {name:'수리검',icon:'✴️',key:'S',mp:20,cd:3,desc:'4방향 수리검',col:'#aaffaa',
       fn:(p,G)=>{[-7,-2,2,7].forEach(vy=>proj(p.x+p.f*52,p.y+26,p.f*19,vy,dmg(p,1.65),'#22dd44','player',{sz:9,emoji:'✴️',life:72}));}},
      {name:'순간이동',icon:'💨',key:'D',mp:18,cd:3.5,desc:'텔레포트+폭풍 참격',col:'#aa44cc',
       fn:(p,G)=>{
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:18,col:['#22cc44','#88ff88'],grav:0,sMin:2,sMax:7});
         p.x+=p.f*200;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-95),p.y-22,105,85,dmg(p,2.7),true);
           addEffect('circle',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:20,col:'#22cc44',scale:1.2});
         },85);
       }},
      {name:'독 단검',icon:'☠️',key:'F',mp:35,cd:7,desc:'독 지속 피해',col:'#44cc44',
       fn:(p,G)=>{
         proj(p.x+p.f*52,p.y+24,p.f*18,-2,dmg(p,1.85),'#44cc44','player',{sz:12,emoji:'🗡️',life:82,
           onHit:(e)=>{
             e.poison=Math.max(e.poison||0,320);e.poisonDmg=Math.round(p.atk*.42);
             addEffect('poison_cloud',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:35,scale:1.2});
           }});
       }},
      {name:'죽음의 무도',icon:'💀',key:'G',mp:80,cd:18,desc:'6방향 폭격+5초 무적',col:'#222244',
       fn:(p,G)=>{
         p.invincible=300;
         for(let i=0;i<6;i++){
           const a=i/6*Math.PI*2;
           hitAOE(p.x+Math.cos(a)*85-50,p.y+Math.sin(a)*65-30,100,82,dmg(p,3.5),true);
           addEffect('slash',p.x+Math.cos(a)*85-G.cam,p.y+Math.sin(a)*65-G.camY,{life:22,col:'#22cc44',ang:a,scale:1.3});
         }
         shake(14,34);
       }},
    ]
  },
  berserker:{
    name:'버서커',role:'광전사',icon:'💢',
    skinCol:'#e8a870',hairCol:'#440000',torsoCol:'#4a1010',legsCol:'#3a0808',
    headDeco:'headband',weapon:'axe',offhand:'shield',
    hp:340,mp:60,atk:64,def:8,spd:5.1,jmp:13.5,
    desc:'ATK 극대화. HP↓ = ATK↑↑',col:'#ff3322',
    skills:[
      {name:'분노 강타',icon:'💢',key:'A',mp:0,cd:2,desc:'2배+HP-8',col:'#ff4422',
       fn:(p,G)=>{
         const d=dmg(p,2.0+(1-p.hp/p.maxHp));p.hp=Math.max(1,p.hp-8);
         hitAOE(p.x+(p.f>0?p.w:-85),p.y-12,88,74,d,true);
         addEffect('explosion',p.x+(p.f>0?p.w+30:-30)-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#ff4422',col2:'#ff8800',scale:.9});
       }},
      {name:'피의 갈망',icon:'🩸',key:'S',mp:0,cd:5,desc:'1.6배+피흡 50%',col:'#cc0000',
       fn:(p,G)=>{
         const d=dmg(p,1.6);
         hitAOE(p.x+(p.f>0?p.w:-85),p.y-12,88,72,d,false,{lifeSteal:.5});
         addEffect('beam',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:16,col:'#cc0000',ang:p.f>0?0:Math.PI,len:120,scale:1});
       }},
      {name:'광란',icon:'🌋',key:'D',mp:20,cd:8,desc:'ATK+60%(5s)-HP20',col:'#ff8800',
       fn:(p,G)=>{
         p.hp=Math.max(1,p.hp-20);p.buffAtk=(p.buffAtk||1)*1.6;p.buffTimer=Math.max(p.buffTimer||0,300);
         addEffect('fire_pillar',p.x+p.w/2-G.cam,p.y+p.h-G.camY,{life:35,scale:1.3});
         shake(5,12);
       }},
      {name:'지진',icon:'💥',key:'F',mp:40,cd:9,desc:'전방 지진파 3배',col:'#cc2200',
       fn:(p,G)=>{
         setTimeout(()=>{
           hitAOE(p.x-85,p.y,230,getGroundY()-p.y+40,dmg(p,3),true);
           addEffect('explosion',p.x+(p.f>0?60:-60)-G.cam,getGroundY()-G.camY,{life:32,col:'#ff4422',col2:'#ffaa00',scale:2});
           for(let i=0;i<5;i++) addEffect('circle',(p.x+p.f*(60+i*40))-G.cam,getGroundY()-G.camY,{life:20+i*5,col:'#ff8800',scale:.6+i*.2});
           shake(10,26);
         },260);
       }},
      {name:'최후의 일격',icon:'🏴',key:'G',mp:0,cd:12,desc:'HP낮을수록 최대 12배',col:'#220000',
       fn:(p,G)=>{
         const mult=5+(1-p.hp/p.maxHp)*7;
         hitAOE(p.x+(p.f>0?p.w-10:-125),p.y-55,165,125,dmg(p,mult),true);
         addEffect('explosion',p.x+(p.f>0?p.w+50:-50)-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#ff2200',col2:'#ff8800',scale:2.5});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:40,col:['#ff2200','#ffcc00'],glow:true,sMin:3,sMax:12,type:'star',spin:true});
         shake(14,35);
       }},
    ]
  },
  paladin:{
    name:'팔라딘',role:'성기사',icon:'✨',
    skinCol:'#f5c090',hairCol:'#ffd080',torsoCol:'#44556a',legsCol:'#334455',
    headDeco:'helm',weapon:'hammer',offhand:'shield',
    hp:520,mp:120,atk:36,def:28,spd:3.8,jmp:11.5,
    desc:'최고 생존력. 힐+재생+신성 폭발.',col:'#eeddaa',
    skills:[
      {name:'망치 강타',icon:'🔨',key:'A',mp:12,cd:2,desc:'망치 1.7배+스턴',col:'#ccd0d4',
       fn:(p,G)=>{
         hitAOE(p.x+(p.f>0?p.w:-92),p.y-12,92,72,dmg(p,1.7),false,{stun:95});
         addEffect('circle',p.x+(p.f>0?p.w+30:-30)-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#ccd0d4',scale:.7});
       }},
      {name:'신성한 빛',icon:'💛',key:'S',mp:20,cd:4,desc:'HP 30% 회복',col:'#ffffaa',
       fn:(p,G)=>{
         const h=Math.round(p.maxHp*.30);p.hp=Math.min(p.maxHp,p.hp+h);
         addEffect('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:35,col:'#ffffaa',scale:1.5});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:22,col:['#ffff88','#ffffff'],glow:true,upb:4,sMin:2,sMax:8});
       }},
      {name:'신성화',icon:'🔆',key:'D',mp:35,cd:7,desc:'광역 신성 폭발',col:'#ffff88',
       fn:(p,G)=>{
         hitAll(dmg(p,1.5),true);
         addEffect('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:45,col:'#ffffaa',scale:2.2});
       }},
      {name:'신성 방패',icon:'🌟',key:'F',mp:40,cd:9,desc:'4초 무적',col:'#aaddff',
       fn:(p,G)=>{
         p.invincible=240;
         addEffect('circle',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:30,col:'#aaddff',col2:'#ffffff',scale:1.8});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:28,col:['#aaddff','#ffffff'],glow:true,sMin:3,sMax:9,grav:-.01});
       }},
      {name:'성광 폭발',icon:'💥',key:'G',mp:80,cd:16,desc:'전체 피해+자힐 40%',col:'#ffffcc',
       fn:(p,G)=>{
         hitAll(dmg(p,2.5),true);p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.4));
         addEffect('explosion',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#ffffcc',col2:'#ffdd88',scale:2.5});
         shake(10,26);
       }},
    ]
  },
  necromancer:{
    name:'네크로맨서',role:'소환사',icon:'💀',
    skinCol:'#c0c8d0',hairCol:'#000000',torsoCol:'#121820',legsCol:'#0a1018',
    headDeco:'crown',weapon:'scythe',offhand:'tome',
    hp:230,mp:260,atk:60,def:6,spd:4.2,jmp:13.0,
    desc:'암흑·소환. 저주로 적 약화.',col:'#8833cc',
    skills:[
      {name:'암흑탄',icon:'💜',key:'A',mp:14,cd:2,desc:'암흑 마법 2배',col:'#8833cc',
       fn:(p,G)=>{
         proj(p.x+p.f*52,p.y+22,p.f*15,-1,dmg(p,2.0),'#8833cc','player',{sz:14,emoji:'🔮',life:67,
           onHit:(e)=>{addEffect('dark_void',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:25,col:'#8833cc',scale:.9});}});
       }},
      {name:'생명 흡수',icon:'🖤',key:'S',mp:24,cd:4,desc:'30피해+자힐 25',col:'#440088',
       fn:(p,G)=>{
         proj(p.x+p.f*52,p.y+22,p.f*13,-1,dmg(p,1.55),'#440088','player',{sz:12,emoji:'🖤',life:62,
           onHit:(e)=>{p.hp=Math.min(p.maxHp,p.hp+25);addEffect('beam',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:18,col:'#440088',ang:Math.random()*Math.PI*2,len:60});}});
       }},
      {name:'저주',icon:'⛧',key:'D',mp:30,cd:6,desc:'전체 적 ATK-40% 4초',col:'#332244',
       fn:(p,G)=>{
         for(const e of G.enemies) if(e.alive) e.cursed=Math.max(e.cursed||0,240);
         if(G.boss&&G.boss.alive) G.boss.cursed=Math.max(G.boss.cursed||0,240);
         addEffect('dark_void',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#332244',scale:2});
       }},
      {name:'뼈 돌풍',icon:'🦴',key:'F',mp:50,cd:10,desc:'전체 광역 2.5배',col:'#ccbbaa',
       fn:(p,G)=>{
         hitAll(dmg(p,2.5),true);
         addEffect('circle',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:30,col:'#ccbbaa',col2:'#8833cc',scale:2});
         shake(6,15);
       }},
      {name:'죽음 폭발',icon:'☠️',key:'G',mp:90,cd:20,desc:'전체 5배 암흑 폭발',col:'#110022',
       fn:(p,G)=>{
         hitAll(dmg(p,5.0),true);
         addEffect('explosion',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:50,col:'#8833cc',col2:'#110022',scale:3});
         for(let i=0;i<12;i++) addEffect('dark_void',(Math.random()*W()),Math.random()*H(),{life:25,col:'#8833cc',scale:.8+Math.random()});
         shake(16,40);
       }},
    ]
  },
  monk:{
    name:'몽크',role:'격투가',icon:'🥊',
    skinCol:'#f5c090',hairCol:'#000000',torsoCol:'#cc8833',legsCol:'#aa6622',
    headDeco:'headband',weapon:'dual',offhand:'dagger',
    hp:300,mp:150,atk:46,def:12,spd:6.2,jmp:16.5,
    desc:'초고속 연타. 기(氣) 스킬 특화.',col:'#ffaa22',
    skills:[
      {name:'연타',icon:'🥊',key:'A',mp:8,cd:1.2,desc:'5연속 0.7배',col:'#ffaa22',
       fn:(p,G)=>{
         for(let i=0;i<5;i++) setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-67),p.y-12,70,62,dmg(p,.72),i===4);
           addEffect('slash',p.x+(p.f>0?p.w+10:-10)-G.cam,p.y+p.h/2-G.camY,{life:10,col:'#ffaa22',ang:i%2===0?-.3:.3,scale:.65});
         },i*92);
       }},
      {name:'기공파',icon:'🌀',key:'S',mp:20,cd:3,desc:'기 에너지 2.5배',col:'#ffcc44',
       fn:(p,G)=>{
         proj(p.x+p.f*52,p.y+22,p.f*17,0,dmg(p,2.5),'#ffcc44','player',{sz:17,emoji:'🌀',life:72,
           onHit:(e)=>{addEffect('circle',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:20,col:'#ffcc44',scale:1.1});}});
       }},
      {name:'철갑',icon:'⛓️',key:'D',mp:15,cd:6,desc:'DEF+10 4초',col:'#888888',
       fn:(p,G)=>{
         p.defBuff=12;p.defBuffTimer=240;
         addEffect('circle',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:22,col:'#aaaaaa',scale:1});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:16,col:['#888','#aaa'],sMin:2,sMax:5,type:'sq',spin:true});
       }},
      {name:'회오리',icon:'🌪️',key:'F',mp:35,cd:7,desc:'360도 3.5배',col:'#88ccff',
       fn:(p,G)=>{
         hitAOE(p.x-85,p.y-55,p.w+170,p.h+110,dmg(p,3.5),true);
         for(let i=0;i<6;i++){
           const a=i/6*Math.PI*2;
           addEffect('beam',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#88ccff',ang:a,len:100,scale:1});
         }
         shake(6,14);
       }},
      {name:'내면의 평화',icon:'☮️',key:'G',mp:0,cd:10,desc:'HP 50%+MP 30 회복',col:'#ffffcc',
       fn:(p,G)=>{
         p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.5));p.mp=Math.min(p.maxMp,p.mp+30);
         addEffect('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#ffffcc',scale:1.6});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:24,col:['#ffffcc','#fff'],glow:true,upb:3,sMin:2,sMax:6});
       }},
    ]
  },
};

// ══════════════════════════════════════════════════════
// ENEMY TYPES
// ══════════════════════════════════════════════════════
const ENEMIES = {
  goblin:   {name:'고블린',  drawType:'goblin',  w:34,h:40, hp:85,  atk:12,spd:3.2,xp:14,g:8,  bodyCol:'#33aa44',headCol:'#22aa33',limbCol:'#22aa44',drawScale:.95,ai:'chase'},
  orc:      {name:'오크',    drawType:'orc',     w:52,h:62, hp:210, atk:25,spd:2.0,xp:30,g:18, bodyCol:'#3a5a2a',headCol:'#4a6a3a',limbCol:'#2a4a1a',drawScale:1.3,ai:'brute'},
  skeleton: {name:'스켈레톤',drawType:'skeleton',w:38,h:52, hp:125, atk:18,spd:3.2,xp:22,g:14, bodyCol:'#d4c8a0',headCol:'#d4c8a0',limbCol:'#c4b888',drawScale:1.0,ai:'normal'},
  mage_e:   {name:'마법사',  drawType:'mage_enemy',w:36,h:58,hp:110,atk:29,spd:2.6,xp:34,g:24,bodyCol:'#2a1a4a',headCol:'#3a2a6a',limbCol:'#3a2a5a',drawScale:.95,ai:'ranged'},
  demon:    {name:'데몬',    drawType:'demon',   w:48,h:66, hp:190, atk:27,spd:2.8,xp:48,g:32, bodyCol:'#4a0a0a',headCol:'#550a0a',limbCol:'#3a0808',drawScale:1.1,ai:'chase'},
  dragon:   {name:'드래고니언',drawType:'dragon',w:60,h:72, hp:270, atk:32,spd:2.3,xp:58,g:40, bodyCol:'#1a3a1a',headCol:'#1a4a1a',limbCol:'#2a5a2a',drawScale:1.3,ai:'brute'},
  golem:    {name:'골렘',    drawType:'golem',   w:68,h:76, hp:400, atk:36,spd:1.4,xp:70,g:50, bodyCol:'#6a5a4a',headCol:'#8a7a6a',limbCol:'#7a6a5a',drawScale:1.4,ai:'tank'},
};

// ══════════════════════════════════════════════════════
// STAGE DATA
// ══════════════════════════════════════════════════════
const STAGES=[
  {name:'어둠의 동굴',  bg:'#06040e',fl:'#100820',wall:'#0d0618',torch:'#ff6600',
   enemySet:['goblin','skeleton'], count:8,
   boss:{name:'슬라임 대왕',drawType:'golem',hp:900,atk:28,spd:2.3,bodyCol:'#226622',headCol:'#337733',limbCol:'#115511',drawScale:1.6}},
  {name:'용암 던전',    bg:'#120400',fl:'#220900',wall:'#1a0500',torch:'#ff4400',
   enemySet:['goblin','orc','demon'], count:10,
   boss:{name:'불꽃 골렘',drawType:'golem',hp:1400,atk:36,spd:2.1,bodyCol:'#662200',headCol:'#883300',limbCol:'#441100',drawScale:1.7}},
  {name:'얼음 궁전',    bg:'#040820',fl:'#081430',wall:'#060e22',torch:'#44aaff',
   enemySet:['orc','skeleton','mage_e'], count:12,
   boss:{name:'빙결 드래곤',drawType:'dragon',hp:1900,atk:45,spd:2.7,bodyCol:'#224466',headCol:'#336688',limbCol:'#112244',drawScale:1.5}},
  {name:'독 늪지',      bg:'#040e04',fl:'#081208',wall:'#060e06',torch:'#44cc00',
   enemySet:['demon','mage_e','dragon'], count:14,
   boss:{name:'늪 히드라',drawType:'dragon',hp:2600,atk:52,spd:3.0,bodyCol:'#225522',headCol:'#337733',limbCol:'#113311',drawScale:1.6}},
  {name:'마왕의 성',    bg:'#080010',fl:'#120018',wall:'#0e0014',torch:'#aa00ff',
   enemySet:['demon','dragon','golem'], count:16,
   boss:{name:'마왕 DARKOS',drawType:'golem',hp:3500,atk:68,spd:3.2,bodyCol:'#220033',headCol:'#330055',limbCol:'#110022',drawScale:2.0}},
];

// ══════════════════════════════════════════════════════
// SHOP
// ══════════════════════════════════════════════════════
const SHOP_ITEMS=[
  {name:'소형 HP 포션',icon:'🧪',desc:'HP +25%',price:60, fn:(p)=>{const h=Math.round(p.maxHp*.25);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'대형 HP 포션',icon:'⚗️', desc:'HP +60%',price:165,fn:(p)=>{const h=Math.round(p.maxHp*.6);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'마나 포션',   icon:'💙', desc:'MP +55%',price:85, fn:(p)=>{const m=Math.round(p.maxMp*.55);p.mp=Math.min(p.maxMp,p.mp+m);return `MP +${m}`;}},
  {name:'강화 무기',   icon:'⚔️', desc:'ATK +20',price:210,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+20;return 'ATK +20';},rarity:1},
  {name:'불꽃 검',     icon:'🔥', desc:'ATK +38',price:390,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+38;return 'ATK +38';},rarity:2},
  {name:'강화 갑옷',   icon:'🛡️', desc:'DEF+14 HP+45',price:230,fn:(p)=>{p.defBonus=(p.defBonus||0)+14;p.maxHp+=45;p.hp=Math.min(p.maxHp,p.hp+45);return 'DEF+14 HP+45';},rarity:1},
  {name:'마법 갑옷',   icon:'💎', desc:'DEF+24 HP+85',price:420,fn:(p)=>{p.defBonus=(p.defBonus||0)+24;p.maxHp+=85;p.hp=Math.min(p.maxHp,p.hp+85);return 'DEF+24 HP+85';},rarity:2},
  {name:'스피드 링',   icon:'💍', desc:'SPD +1.2',price:190,fn:(p)=>{p.spdBonus=(p.spdBonus||0)+1.2;return 'SPD +1.2';},rarity:1},
  {name:'크리티컬 링', icon:'🔮', desc:'CRIT +20%',price:310,fn:(p)=>{p.critBonus=(p.critBonus||0)+.2;return 'CRIT +20%';},rarity:2},
  {name:'전설의 반지', icon:'⭐', desc:'ATK+28 CRIT+28%',price:680,fn:(p)=>{p.atkBonus=(p.atkBonus||0)+28;p.critBonus=(p.critBonus||0)+.28;return 'ATK+28 CRIT+28%';},rarity:4},
];
const RARITY_COL=['#aaaaaa','#44cc44','#4488ff','#cc44ff','#ffcc00'];

// ══════════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════════
let G=null,RAF=null,selCharId=null;
const GRAVITY=0.52;

function mkPlayer(clsId){
  const c=CLASSES[clsId];
  const gy=getGroundY();
  return {
    ...c,clsId,
    x:140,y:gy-65,vx:0,vy:0,f:1,
    onGround:false,jumpCount:0,
    hp:c.hp,maxHp:c.hp,mp:c.mp,maxMp:c.mp,
    alive:true,invincible:0,
    skillCds:c.skills.map(()=>0),
    buffAtk:1,buffSpd:1,buffTimer:0,
    kills:0,score:0,gold:0,level:1,xp:0,xpNext:100,
    combo:0,comboTimer:0,maxCombo:0,
    atkCd:0,atkAnim:0,hitFlash:0,dodgeCd:0,dodgeAnim:0,
    w:44,h:62,
    atkBonus:0,defBonus:0,spdBonus:0,critBonus:0,defBuff:0,defBuffTimer:0,
    walkPhase:0,atkPhase:0,
    equip:{wpn:null,arm:null,acc:null},
    onLadder:false,
  };
}

function initGame(clsId,stageIdx){
  buildLayout();
  const p=mkPlayer(clsId);
  const stage=STAGES[stageIdx];
  G={
    clsId,stageIdx,stage,
    player:p,
    enemies:[],
    boss:null,bossSpawned:false,
    projectiles:[],items:[],
    cam:0,camY:0,
    phase:'play',timer:0,
    startTime:Date.now(),
    shakeAmt:0,shakeTimer:0,hitStop:0,
    stageDmgTaken:0,paused:false,
    shopStock:[],pendingLvlUp:false,
    maxCombo:0,
  };
  PARTS.length=0;EFFECTS.length=0;
  spawnEnemies();
  updateEquipUI();
}

function spawnEnemies(){
  const st=G.stage;
  const floors=layout.floors;
  for(let i=0;i<st.count;i++){
    const tid=st.enemySet[Math.floor(Math.random()*st.enemySet.length)];
    const et={...ENEMIES[tid]};
    const sc=1+(G.stageIdx*.22);
    // Distribute enemies across floors
    const floorIdx=Math.floor(Math.random()*floors.length);
    const floor=floors[floorIdx];
    let ex, ey;
    if(floorIdx===0){
      ex=600+i*280+Math.random()*100;
      ey=floor.y-et.h;
    } else {
      // Find a platform on this floor
      const plats=floor.platforms;
      if(plats&&plats.length){
        const pl=plats[Math.floor(Math.random()*plats.length)];
        ex=pl.x+Math.random()*Math.max(10,pl.w-et.w);
        ey=pl.y-et.h;
      } else {
        ex=600+i*280+Math.random()*100;
        ey=floor.y-et.h;
      }
    }
    G.enemies.push({
      ...et,uid:'e'+i+Date.now(),
      x:ex,y:ey,hp:Math.round(et.hp*sc),maxHp:Math.round(et.hp*sc),atk:Math.round(et.atk*sc),
      vx:0,vy:0,f:-1,alive:true,dying:false,deathTimer:0,
      atkTimer:65+Math.random()*75,
      frozen:0,stun:0,poison:0,poisonDmg:0,poisonTimer:0,cursed:0,
      hitFlash:0,walkPhase:Math.random()*Math.PI*2,atkPhase:0,aggro:false,
      floorY:ey+et.h, // remember home floor
    });
  }
}

function spawnBoss(){
  const bd=G.stage.boss;
  const sc=1+(G.stageIdx*.28);
  G.boss={
    ...bd,...ENEMIES[bd.drawType]||ENEMIES.golem,
    name:bd.name,drawType:bd.drawType,
    bodyCol:bd.bodyCol,headCol:bd.headCol,limbCol:bd.limbCol,drawScale:bd.drawScale,
    x:STAGE_W-600,y:getGroundY()-95,
    hp:Math.round(bd.hp*sc),maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc),spd:bd.spd+G.stageIdx*.08,
    w:78,h:95,alive:true,dying:false,
    frozen:0,stun:0,cursed:0,
    atkTimer:70,projTimer:90,
    phase2:false,phase3:false,hitFlash:0,walkPhase:0,atkPhase:0,
  };
  document.getElementById('boss-bar').classList.add('show');
  document.getElementById('boss-name-lbl').textContent='⚠ '+bd.name;
  const bw=document.getElementById('boss-warn');
  bw.style.display='block';bw.textContent='⚠ BOSS ⚠\n'+bd.name;
  setTimeout(()=>bw.style.display='none',2500);
  shake(14,45);
  sfx_bossIn();
}

// ══════════════════════════════════════════════════════
// COMBAT
// ══════════════════════════════════════════════════════
function totalAtk(p){return (p.atk+(p.atkBonus||0))*(p.buffAtk||1);}
function totalDef(p){return (p.def+(p.defBonus||0))+(p.defBuff||0);}
function totalCrit(p){return .1+(p.critBonus||0);}
function totalSpd(p){return (p.spd+(p.spdBonus||0))*(p.buffSpd||1);}

function dmg(p,mult){
  const atk=totalAtk(p);
  const isCrit=Math.random()<totalCrit(p);
  const v=Math.round((atk*mult+Math.random()*7-3.5)*(isCrit?2.1:1));
  return {v:Math.max(1,v),crit:isCrit};
}

function hitAOE(ax,ay,aw,ah,d,showCrit,opts={}){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  for(const e of targets){
    if(!e.alive) continue;
    if(ax<e.x+e.w&&ax+aw>e.x&&ay<e.y+e.h&&ay+ah>e.y) dealDmg(e,d.v,d.crit||showCrit,opts);
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
  if(e.cursed>0) v=Math.round(v*1.42);
  e.hp-=v;e.hitFlash=9;
  if(opts.stun) e.stun=Math.max(e.stun||0,opts.stun);
  if(opts.lifeSteal) p.hp=Math.min(p.maxHp,p.hp+Math.round(v*opts.lifeSteal));
  if(opts.onHit) opts.onHit(e);
  const sx=e.x-G.cam+e.w/2, sy=e.y-G.camY;
  showDNum(sx,sy,v,crit,p.col||'#fff');
  G.hitStop=crit?6:2;
  if(crit){
    const cf=document.getElementById('crit-flash');
    cf.style.animation='none';cf.offsetHeight;cf.style.animation='crit-flash .4s ease';
  }
  if(e.hp<=0) killE(e);
}

function killE(e){
  e.alive=false;e.dying=true;e.deathTimer=30;
  const p=G.player;
  if(e===G.boss){
    p.xp+=750;p.gold+=450;p.score+=9000;
    G.bossKills=(G.bossKills||0)+1;
    document.getElementById('boss-bar').classList.remove('show');
    spawnParts(e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,{n:70,col:['#ffcc00','#ff6600','#fff'],glow:true,sMin:3,sMax:15,type:'star',spin:true});
    shake(18,60);sfx_clear();checkLvlUp(p);
    setTimeout(()=>stageClear(),1200);
  } else {
    p.kills++;p.xp+=e.xp;p.gold+=e.g;p.score+=e.xp*2;
    spawnParts(e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,{n:15,col:[e.bodyCol||'#556','#ffcc00'],sMin:2,sMax:6});
    checkLvlUp(p);tryDrop(e);
  }
}

function checkLvlUp(p){
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext;p.level++;p.xpNext=Math.round(p.xpNext*1.52);
    p.maxHp+=32;p.hp=Math.min(p.maxHp,p.hp+52);
    p.maxMp+=12;p.mp=Math.min(p.maxMp,p.mp+22);
    p.atk+=4;p.def+=2;
    G.pendingLvlUp=true;showLvlUpModal();sfx_lvl();
  }
}

function tryDrop(e){
  if(Math.random()>.4) return;
  const it={...SHOP_ITEMS[Math.floor(Math.random()*SHOP_ITEMS.length)],uid:'d'+Date.now(),x:e.x+e.w/2-14,y:e.y,vy:-7,alive:true};
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
    life:opts.life||80,sz:opts.sz||8,pierce:opts.pierce||false,
    grav:opts.grav!==undefined?opts.grav:0,emoji:opts.emoji||null,
    trail:opts.trail||false,homing:opts.homing||false,
    explode:opts.explode||false,onHit:opts.onHit||null,
  });
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
  const dt=Math.min((ts-lastTs)/16.67,3);lastTs=ts;
  if(G&&G.phase==='play'&&!G.paused&&!G.pendingLvlUp) gameUpdate(dt);
  gameRender();updateHUD();flushJK();
  RAF=requestAnimationFrame(loop);
}

function gameUpdate(dt){
  G.timer++;
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
  updateEffects(dt);

  if(G.shakeTimer>0) G.shakeTimer-=dt;
  if(G.timer%72===0) p.mp=Math.min(p.maxMp,p.mp+3);
  if(p.defBuffTimer>0){p.defBuffTimer-=dt;if(p.defBuffTimer<=0) p.defBuff=0;}
  if(p.buffTimer>0){p.buffTimer-=dt;if(p.buffTimer<=0){p.buffAtk=1;p.buffSpd=1;}}

  // Boss spawn when all enemies dead
  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){
    G.bossSpawned=true;spawnBoss();
  }

  // Camera: follow player
  const targetCamX=p.x-W()*.36;
  const targetCamY=p.y-H()*.45;
  G.cam+=(targetCamX-G.cam)*.1*dt;
  G.camY+=(targetCamY-G.camY)*.1*dt;
  G.cam=Math.max(0,Math.min(STAGE_W-W(),G.cam));
  G.camY=Math.max(0,Math.min(layout.floors[layout.floors.length-1].y-H()*.9,G.camY));
}

function handleInput(p,dt){
  if(!p.alive) return;
  const spd=totalSpd(p);

  if(KEY['ArrowLeft']){p.vx=-spd*6*dt;p.f=-1;}
  if(KEY['ArrowRight']){p.vx=spd*6*dt;p.f=1;}

  // Ladder logic
  const ld=getNearbyLadder(p.x,p.y,p.h);
  if(ld){
    if(KEY['ArrowUp']||KEY['ArrowDown']){
      p.onLadder=true;p.vy=0;p.jumpCount=0;
    }
    if(p.onLadder){
      if(KEY['ArrowUp']) p.y-=spd*4*dt;
      if(KEY['ArrowDown']) p.y+=spd*4*dt;
      p.vx*=.7;p.vy=0;
      // Exit ladder at top or bottom
      if(p.y<=ld.y1-p.h){p.onLadder=false;}
      if(p.y+p.h>=ld.y2+10){p.onLadder=false;}
    }
  } else {
    p.onLadder=false;
  }

  // Jump
  if((JK['z']||JK['Z'])&&p.jumpCount<2&&!p.onLadder){
    p.vy=-p.jmp;p.jumpCount++;p.onLadder=false;
    spawnParts(p.x+p.w/2-G.cam,p.y+p.h-G.camY,{n:9,col:['#fff','#ccc'],upb:3,sMin:2,sMax:4,spread:.8});
    sfx_jump();
  }

  // Attack
  if((JK['x']||JK['X'])&&p.atkCd<=0) doAttack(p);

  // Dodge
  if(JK[' ']&&p.dodgeCd<=0&&!p.onLadder){
    p.vx=p.f*26;p.vy=-2.5;p.invincible=45;p.dodgeCd=55;p.dodgeAnim=24;
    spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:15,col:[p.col||'#fff','rgba(255,255,255,.4)'],spread:Math.PI*.5,dir:Math.PI,upb:0,sMin:2,sMax:5,grav:.05});
    sfx_dodge();
  }

  // Skills
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
  p.atkCd=13;p.atkAnim=13;p.atkPhase=Math.PI*.5;
  p.combo=Math.min(12,(p.combo||0)+1);p.comboTimer=88;
  if(p.combo>G.maxCombo) G.maxCombo=p.combo;
  const cd=document.getElementById('combo-disp');
  document.getElementById('combo-num').textContent=p.combo+'HIT';
  cd.style.opacity=p.combo>=2?'1':'0';
  const mult=1+p.combo*.08;
  const d=dmg(p,mult);
  hitAOE(p.x+(p.f>0?p.w:-70),p.y-14,74,64,d,false);
  spawnParts(p.x+(p.f>0?p.w+22:-32)-G.cam,p.y+22-G.camY,{n:d.crit?15:8,col:[p.col||'#fff','#ffcc00'],spread:.65,dir:p.f>0?0:Math.PI,sMin:2,sMax:d.crit?9:5,glow:d.crit});
  if(d.crit){shake(3,6);addEffect('slash',p.x+(p.f>0?p.w+15:-15)-G.cam,p.y+p.h/2-G.camY,{life:14,col:p.col||'#fff',ang:p.f>0?-.15:.15,scale:1.1});}
}

function useSkill(p,idx){
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;p.skillCds[idx]=sk.cd*60;p.atkPhase=Math.PI;
  sk.fn(p,G);
}

function updatePlayer(p,dt){
  if(p.onLadder){
    p.x+=p.vx*dt;p.y=Math.max(layout.floors[layout.floors.length-1].y-H(),Math.min(getGroundY()-p.h,p.y));
    p.vx*=.8;
  } else {
    p.vy+=GRAVITY*dt;
    p.x+=p.vx*dt;p.y+=p.vy*dt;
    p.vx*=.82;

    // Floor collision
    let landed=false;
    const pl=getFloorBelow(p.x,p.y+p.h,p.vy);
    if(pl&&p.vy>=0){
      p.y=pl.y-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;landed=true;
    }
    if(!landed){p.onGround=false;}
    // Ground
    if(p.y+p.h>getGroundY()+10) p.y=getGroundY()-p.h,p.vy=0,p.onGround=true,p.jumpCount=0;
    if(p.y>H()+100) p.y=getGroundY()-p.h,p.vy=0;
  }

  p.x=Math.max(5,Math.min(STAGE_W-p.w-5,p.x));

  if(Math.abs(p.vx)>0.5&&p.onGround) p.walkPhase+=.24*dt*Math.abs(p.vx)*.035;
  else if(p.onGround) p.walkPhase=Math.round(p.walkPhase/Math.PI)*Math.PI;
  p.atkPhase=Math.max(0,p.atkPhase-.14*dt);
  if(p.invincible>0) p.invincible-=dt;
  if(p.atkCd>0) p.atkCd-=dt;
  if(p.atkAnim>0) p.atkAnim-=dt;
  if(p.hitFlash>0) p.hitFlash-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeAnim>0) p.dodgeAnim-=dt;
  if(p.comboTimer>0){p.comboTimer-=dt;if(p.comboTimer<=0){p.combo=0;document.getElementById('combo-disp').style.opacity='0';}}
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;
  // Paladin passive regen
  if(p.clsId==='paladin'&&G.timer%92===0) p.hp=Math.min(p.maxHp,p.hp+Math.ceil(p.maxHp*.014));
}

function updateEnemies(dt){
  const p=G.player;
  for(const e of G.enemies){
    if(!e.alive){if(e.dying) e.deathTimer-=dt;continue;}
    if(e.hitFlash>0) e.hitFlash-=dt;
    if(e.frozen>0){e.frozen-=dt;e.walkPhase=0;continue;}
    if(e.stun>0){e.stun-=dt;continue;}
    if(e.cursed>0) e.cursed-=dt;
    if(e.poison>0){
      e.poison-=dt;
      if(!e.poisonTimer||e.poisonTimer<=0){
        e.hp-=e.poisonDmg||5;e.poisonTimer=22;
        if(e.hp<=0){killE(e);continue;}
      }
      e.poisonTimer-=dt;
    }

    const dx=p.x-e.x,dy=p.y-e.y;
    const distH=Math.abs(dx);
    if(distH<500) e.aggro=true;
    if(!e.aggro) continue;

    e.f=dx>0?1:-1;
    const sm=e.cursed>0?.58:1;
    const spd=(e.spd||2)*sm;

    // Only chase on same floor (same Y range)
    const onSameFloor=Math.abs(dy)<100;
    if(onSameFloor||e.ai==='ranged'){
      switch(e.ai){
        case 'chase': if(distH>52) e.x+=e.f*spd*dt; break;
        case 'brute': if(distH>58) e.x+=e.f*spd*.88*dt; break;
        case 'slow':  if(distH>62) e.x+=e.f*spd*.6*dt; break;
        case 'tank':  if(distH>68) e.x+=e.f*spd*.55*dt; break;
        case 'ranged':
          if(distH<180) e.x-=e.f*spd*.65*dt;
          else if(distH>300) e.x+=e.f*spd*.65*dt;
          break;
        default: if(distH>52) e.x+=e.f*spd*dt; break;
      }
    }

    // Gravity
    e.vy=(e.vy||0)+GRAVITY*dt*.5;
    e.y+=e.vy*dt;
    const epl=getFloorBelow(e.x+e.w/2-10,e.y+e.h,e.vy);
    if(epl&&e.vy>=0){e.y=epl.y-e.h;e.vy=0;}
    if(e.y+e.h>getGroundY()+8){e.y=getGroundY()-e.h;e.vy=0;}
    e.x=Math.max(10,Math.min(STAGE_W-e.w-10,e.x));

    e.walkPhase+=.18*dt;
    e.atkPhase=Math.max(0,e.atkPhase-.11*dt);
    e.atkTimer-=dt;

    if(e.atkTimer<=0&&e.aggro){
      if(e.ai==='ranged'){
        if(distH<380&&onSameFloor){
          e.atkTimer=100+Math.random()*55;
          const vd=dmg({atk:e.atk,atkBonus:0,buffAtk:1,critBonus:0},1);
          proj(e.x+e.w/2,e.y+e.h*.4,e.f*11+(Math.random()-.5)*1,(Math.random()-.5)*2.5,vd,'#aa44ff','enemy',{sz:9,life:82});
          e.atkPhase=Math.PI*.8;
        }
      } else {
        if(distH<62&&onSameFloor){
          e.atkTimer=78+Math.random()*38;e.atkPhase=Math.PI;
          if(p.dodgeAnim<=0){
            const rawDmg=Math.max(1,e.atk-Math.round(totalDef(p)*.52)+Math.floor(Math.random()*6)-3);
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
    b.phase2=true;b.spd*=1.35;b.atk=Math.round(b.atk*1.28);
    document.getElementById('boss-phase-txt').textContent='⚡ PHASE 2';
    shake(13,42);addEffect('explosion',b.x-G.cam+b.w/2,b.y-G.camY+b.h/2,{life:40,col:'#ff4400',col2:'#ffcc00',scale:2});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true;b.spd*=1.28;b.atk=Math.round(b.atk*1.22);
    document.getElementById('boss-phase-txt').textContent='💀 ENRAGE';
    shake(20,65);addEffect('dark_void',b.x-G.cam+b.w/2,b.y-G.camY+b.h/2,{life:55,col:'#ff0000',scale:3});
    sfx_bossIn();
  }

  const dx=p.x-b.x;
  b.f=dx>0?1:-1;
  if(Math.abs(dx)>100) b.x+=b.f*b.spd*dt*.9;
  b.vy=(b.vy||0)+GRAVITY*dt*.42;
  b.y+=b.vy*dt;
  const bpl=getFloorBelow(b.x+b.w/2,b.y+b.h,b.vy);
  if(bpl&&b.vy>=0){b.y=bpl.y-b.h;b.vy=0;}
  if(b.y+b.h>getGroundY()+8){b.y=getGroundY()-b.h;b.vy=0;}
  b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));
  b.walkPhase+=.11*dt;b.atkPhase=Math.max(0,b.atkPhase-.09*dt);
  b.atkTimer-=dt;b.projTimer-=dt;

  const pInt=b.phase3?42:b.phase2?62:95;
  if(b.projTimer<=0){
    b.projTimer=pInt;b.atkPhase=Math.PI*.8;
    const bv=dmg({atk:b.atk,atkBonus:0,buffAtk:1,critBonus:0},b.phase3?.75:.62);
    if(b.phase3){
      for(let i=-1;i<=1;i++) proj(b.x+b.w/2,b.y+b.h*.38,b.f*10.5,i*4.8,bv,'#ff2200','enemy',{sz:16,emoji:'💥',life:90,grav:.09});
    } else {
      proj(b.x+b.w/2,b.y+b.h*.38,b.f*9,-1.5,bv,'#ff4400','enemy',{sz:16,emoji:'💥',life:90,grav:.1});
    }
  }

  if(b.atkTimer<=0&&Math.abs(dx)<106){
    b.atkTimer=b.phase3?38:b.phase2?52:72;b.atkPhase=Math.PI;
    if(Math.abs(p.y-b.y)<100&&p.invincible<=0&&p.dodgeAnim<=0){
      const rawDmg=Math.max(1,b.atk-Math.round(totalDef(p)*.42)+Math.floor(Math.random()*14)-7);
      takeDmg(rawDmg);
      if(b.phase3) setTimeout(()=>{if(G&&p.hp>0) takeDmg(Math.round(rawDmg*.72));},210);
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
  setTimeout(()=>fl.style.opacity='0',120);
  shake(5,12);
  if(p.hp<=0) gameOver();
}

function updateProjs(dt){
  const p=G.player;
  const gy=getGroundY()+30;
  G.projectiles=G.projectiles.filter(pr=>{
    if(!pr.alive) return false;
    pr.x+=pr.vx*dt;pr.y+=pr.vy*dt;pr.vy+=pr.grav*dt;pr.life-=dt;
    if(pr.life<=0) return false;
    if(pr.trail) spawnParts(pr.x-G.cam,pr.y-G.camY,{n:2,col:[pr.col],sMin:1,sMax:3,grav:0,dMax:.06,spread:.3});
    if(pr.explode&&pr.y>=gy){
      addEffect('explosion',pr.x-G.cam,gy-G.camY,{life:30,col:pr.col,col2:'#ff8800',scale:1.4});
      hitAOE(pr.x-70,gy-80,140,90,{v:pr.dmg,crit:pr.crit},false);shake(4,9);return false;
    }
    if(pr.y>gy+100) return false;
    if(pr.owner==='player'){
      const targets=[...G.enemies];if(G.boss&&G.boss.alive) targets.push(G.boss);
      for(const e of targets){
        if(!e.alive) continue;
        if(pr.x>e.x&&pr.x<e.x+e.w&&pr.y>e.y&&pr.y<e.y+e.h){
          dealDmg(e,pr.dmg,pr.crit,{onHit:pr.onHit});
          spawnParts(pr.x-G.cam,pr.y-G.camY,{n:9,col:[pr.col,'#fff'],sMin:2,sMax:5,glow:!!pr.emoji});
          if(!pr.pierce){pr.alive=false;return false;}
        }
      }
    } else {
      const sx=pr.x-G.cam, sy=pr.y-G.camY;
      const px=p.x-G.cam, py=p.y-G.camY;
      if(p.invincible<=0&&p.dodgeAnim<=0&&sx>px&&sx<px+p.w&&sy>py&&sy<py+p.h){
        takeDmg(Math.max(1,pr.dmg-Math.round(totalDef(p)*.38)));pr.alive=false;return false;
      }
    }
    return true;
  });
}

function updateItems(dt){
  const p=G.player;const gy=getGroundY();
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAVITY*dt*.68;it.y+=it.vy*dt;
    if(it.y+20>=gy){it.y=gy-20;it.vy=0;}
    const sx=it.x-G.cam, sy=it.y-G.camY;
    const px=p.x-G.cam, py=p.y-G.camY;
    if(sx>px-32&&sx<px+p.w+32&&sy>py-12&&sy<py+p.h+22){
      showDNum(sx,sy,'+ '+it.fn(p),false,'#ffcc00');it.alive=false;return false;
    }
    return true;
  });
}

// ══════════════════════════════════════════════════════
// RENDER
// ══════════════════════════════════════════════════════
function gameRender(){
  if(!G){ctx.fillStyle='#08060f';ctx.fillRect(0,0,W(),H());return;}
  ctx.save();
  if(G.shakeTimer>0){
    const s=G.shakeAmt*(G.shakeTimer/22)*.48;
    ctx.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }
  const st=G.stage;
  ctx.fillStyle=st.bg;ctx.fillRect(0,0,W(),H());

  drawBG(st);
  drawLayout();
  drawLadderIndicators();
  drawParts(G.cam,G.camY);
  drawEffects(G.cam,G.camY);
  drawProjs();
  drawItems();
  drawEnemies_all();
  if(G.boss&&(G.boss.alive||G.boss.dying)) drawMonster(G.boss,G.cam,G.camY);
  drawPlayer();

  ctx.restore();
  drawMinimap();
}

function drawBG(st){
  ctx.save();ctx.globalAlpha=.04;ctx.font='900 80px sans-serif';ctx.fillStyle='#fff';ctx.textAlign='center';
  ctx.fillText(st.name,W()/2,H()/2+28);ctx.restore();
  // Torches
  if(G.timer%7===0){
    for(let i=0;i<3;i++){
      const tx=W()*.2+i*W()*.3;
      spawnParts(tx+G.cam*.02,getGroundY()-G.camY-18,{n:1,col:[st.torch||'#ff6600'],glow:true,sMin:1,sMax:2,upb:2.5,grav:-.025,dMax:.04,spread:.3});
    }
  }
}

function drawLayout(){
  if(!layout) return;
  const st=G.stage;
  for(const floor of layout.floors){
    for(const pl of floor.platforms){
      const px=pl.x-G.cam, py=pl.y-G.camY;
      if(px>W()+20||px+pl.w<-20) continue;
      if(pl.ground){
        // Ground floor
        ctx.fillStyle=st.fl;ctx.fillRect(0,py,W(),H()-py);
        ctx.fillStyle='rgba(255,180,80,.3)';ctx.fillRect(0,py,W(),2);
        ctx.fillStyle='rgba(0,0,0,.3)';ctx.fillRect(0,py+2,W(),4);
      } else {
        // Platform
        ctx.fillStyle=st.fl;ctx.fillRect(px,py,pl.w,14);
        ctx.fillStyle='rgba(255,180,80,.25)';ctx.fillRect(px,py,pl.w,2);
        ctx.fillStyle='rgba(0,0,0,.3)';ctx.fillRect(px,py+12,pl.w,3);
        // Platform pillars
        ctx.fillStyle=st.wall||'#0d0618';
        ctx.fillRect(px+8,py+14,6,30);
        if(pl.w>100) ctx.fillRect(px+pl.w-14,py+14,6,30);
      }
    }
  }
  // Ladders
  for(const ld of layout.ladders){
    const lx=ld.x-G.cam, ly1=ld.y1-G.camY, ly2=ld.y2-G.camY;
    if(lx<-30||lx>W()+30) continue;
    // Ladder side rails
    ctx.strokeStyle='rgba(180,130,60,.7)';ctx.lineWidth=4;
    ctx.beginPath();ctx.moveTo(lx-8,ly1);ctx.lineTo(lx-8,ly2);ctx.stroke();
    ctx.beginPath();ctx.moveTo(lx+8,ly1);ctx.lineTo(lx+8,ly2);ctx.stroke();
    // Rungs
    ctx.strokeStyle='rgba(220,170,80,.6)';ctx.lineWidth=3;
    const rungs=Math.round((ly2-ly1)/18);
    for(let r=0;r<=rungs;r++){
      const ry=ly1+r*(ly2-ly1)/rungs;
      ctx.beginPath();ctx.moveTo(lx-8,ry);ctx.lineTo(lx+8,ry);ctx.stroke();
    }
  }
}

function drawLadderIndicators(){
  if(!G||!G.player) return;
  const p=G.player;
  const ld=getNearbyLadder(p.x,p.y,p.h);
  if(ld&&!p.onLadder){
    const lx=ld.x-G.cam;
    const ly=ld.y1-G.camY-30;
    ctx.save();ctx.font='bold 12px sans-serif';ctx.fillStyle='rgba(245,200,66,.8)';ctx.textAlign='center';
    ctx.fillText('↑↓ 사다리',lx,ly);ctx.restore();
  }
}

function drawPlayer(){
  const p=G.player;const px=p.x-G.cam,py=p.y-G.camY;
  if(p.invincible>0&&Math.floor(G.timer/3)%2===0) return;
  ctx.save();
  // Ladder climbing anim
  const wp=p.onLadder?G.timer*.08:p.walkPhase;
  if(p.dodgeAnim>0){
    for(let i=1;i<=3;i++){
      ctx.globalAlpha=(p.dodgeAnim/24)*(i/3)*.25;
      drawChar({x:px-p.f*i*20,y:py+p.h,f:p.f,walkPhase:wp,atkPhase:0,hitFlash:0,dead:false,...p,scale:.9});
    }
    ctx.globalAlpha=1;
  }
  drawChar({x:px,y:py+p.h,f:p.f,walkPhase:wp,atkPhase:p.atkPhase,hitFlash:p.hitFlash,dead:!p.alive,...p});
  ctx.globalAlpha=.25;ctx.fillStyle='#000';
  ctx.beginPath();ctx.ellipse(px+p.w/2,getGroundY()-G.camY+5,p.w*.48,5,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawEnemies_all(){
  for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const ex=e.x-G.cam;const ey=e.y-G.camY;
    if(ex<-120||ex>W()+120) continue;
    const alpha=e.dying?(e.deathTimer/30):1;
    ctx.save();ctx.globalAlpha=alpha;
    drawMonster(e,G.cam,G.camY);
    ctx.restore();
  }
}

function drawProjs(){
  for(const pr of G.projectiles){
    const px=pr.x-G.cam,py=pr.y-G.camY;
    if(px<-35||px>W()+35) continue;
    if(pr.emoji){
      ctx.font=`${pr.sz*1.8}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pr.emoji,px,py);
    } else {
      ctx.save();ctx.fillStyle=pr.col;ctx.shadowColor=pr.col;ctx.shadowBlur=11;
      ctx.beginPath();ctx.arc(px,py,pr.sz,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;ctx.restore();
    }
  }
}

function drawItems(){
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam,iy=it.y-G.camY;
    if(ix<-35||ix>W()+35) continue;
    ctx.save();
    ctx.shadowColor=RARITY_COL[it.rarity||0];ctx.shadowBlur=13;
    const bob=Math.sin(G.timer*.08+it.x*.01)*3;
    ctx.font='22px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(it.icon,ix,iy+bob);ctx.shadowBlur=0;ctx.restore();
  }
}

function drawMinimap(){
  if(!layout) return;
  const mc=document.getElementById('mm-canvas');
  const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,120,28);
  const scale=120/STAGE_W;
  const p=G.player;
  for(const e of G.enemies){
    if(!e.alive) continue;
    mctx.fillStyle=e.bodyCol||'#f44';mctx.fillRect(e.x*scale,10,3,3);
  }
  if(G.boss&&G.boss.alive){mctx.fillStyle='#f00';mctx.fillRect(G.boss.x*scale-1,8,5,5);}
  mctx.fillStyle='#0fa';mctx.fillRect(p.x*scale-2,9,4,5);
  mctx.strokeStyle='rgba(245,200,66,.35)';mctx.lineWidth=1;
  mctx.strokeRect(G.cam*scale,1,W()*scale,26);
}

// ══════════════════════════════════════════════════════
// HUD
// ══════════════════════════════════════════════════════
function updateHUD(){
  if(!G) return;
  const p=G.player;
  const hp=Math.max(0,p.hp),mp=Math.max(0,p.mp);
  document.getElementById('hp-fill').style.width=Math.max(0,(hp/p.maxHp)*100)+'%';
  document.getElementById('mp-fill').style.width=Math.max(0,(mp/p.maxMp)*100)+'%';
  document.getElementById('hp-text').textContent=`${hp}/${p.maxHp}`;
  document.getElementById('mp-text').textContent=`${mp}/${p.maxMp}`;
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
  if(p.buffAtk>1) bi+='<span>🔥</span>';if(p.defBuff>0) bi+='<span>🛡️</span>';if(p.invincible>65) bi+='<span>⭐</span>';
  document.getElementById('buff-row').innerHTML=bi;
  // Skills
  const sc=document.getElementById('sk-cont');
  sc.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i];const cd=p.skillCds[i];const rdy=cd<=0&&p.mp>=sk.mp;
    const div=document.createElement('div');
    div.className='sk-slot '+(rdy?'ready':'cooling');
    div.innerHTML=`<div class="sk-icon">${sk.icon}</div><span class="sk-key">${sk.key}</span><span class="sk-mp">${sk.mp}</span>`;
    if(cd>0){const cdDiv=document.createElement('div');cdDiv.className='sk-cd';cdDiv.textContent=cd>60?Math.ceil(cd/60)+'s':cd.toFixed(1);div.appendChild(cdDiv);}
    div.title=`${sk.name} [${sk.key}] MP:${sk.mp} CD:${sk.cd}s — ${sk.desc}`;
    sc.appendChild(div);
  }
  updateEquipUI();
}

function updateEquipUI(){
  if(!G) return;const p=G.player;
  ['wpn','arm','acc'].forEach((s,i)=>{
    const el=document.getElementById('eq-'+s);if(!el) return;
    el.textContent=p.equip[s]?p.equip[s].icon:['🗡️','🛡️','💍'][i];
  });
}

// ══════════════════════════════════════════════════════
// DAMAGE NUMBERS
// ══════════════════════════════════════════════════════
function showDNum(sx,sy,v,crit,col){
  const el=document.createElement('div');el.className='dnum';
  const area=document.getElementById('game-area');
  el.style.cssText=`left:${area.offsetLeft+sx-18}px;top:${area.offsetTop+sy-14}px;font-size:${crit?'1.35':'0.88'}rem;color:${crit?'#ffff44':(col||'#fff')};`;
  el.textContent=crit?'💥'+v+'!!':v;
  document.body.appendChild(el);setTimeout(()=>el.remove(),980);
}

// ══════════════════════════════════════════════════════
// STAGE TRANSITIONS
// ══════════════════════════════════════════════════════
function stageClear(){
  G.phase='clear';const p=G.player;
  const el=Math.round((Date.now()-G.startTime)/1000);
  const bonus=G.stageDmgTaken===0?5000:0;p.score+=bonus;
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
  G.phase='over';G.player.alive=false;const p=G.player;
  document.getElementById('over-grid').innerHTML=`
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">점수<b>${p.score}</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">스테이지<b>${G.stageIdx+1}</b></div>
    <div class="res-cell">콤보<b>${G.maxCombo}HIT</b></div>`;
  setTimeout(()=>document.getElementById('over-ov').classList.remove('hidden'),780);
  sfx_death();
}

function openShop(){document.getElementById('clear-ov').classList.add('hidden');buildShop();document.getElementById('shop-ov').classList.remove('hidden');}
function buildShop(){
  const p=G.player;document.getElementById('shop-gold-lbl').textContent=p.gold;
  const pool=[...SHOP_ITEMS].sort(()=>Math.random()-.5).slice(0,6);
  G.shopStock=pool.map(it=>({...it,uid:'s'+Date.now(),price:it.price+G.stageIdx*28}));
  const grid=document.getElementById('shop-grid');
  grid.innerHTML=G.shopStock.map((it,i)=>{
    const cant=p.gold<it.price;
    return `<div class="shop-card ${cant?'cant':''}" onclick="buyShopItem(${i})">
      <div class="sc-icon">${it.icon}</div>
      <div class="sc-name" style="color:${RARITY_COL[it.rarity||0]}">${it.name}</div>
      <div class="sc-desc">${it.desc}</div><div class="sc-price">${it.price}💰</div></div>`;
  }).join('');
}
function buyShopItem(i){
  const p=G.player;const it=G.shopStock[i];
  if(!it||p.gold<it.price) return;
  p.gold-=it.price;it.fn(p);sfx_buy();buildShop();
}
function continueAfterShop(){document.getElementById('shop-ov').classList.add('hidden');initGame(G.clsId,(G.stageIdx+1)%STAGES.length);}
function retryStage(){document.getElementById('over-ov').classList.add('hidden');initGame(G.clsId,G.stageIdx);}
function gotoTitle(){
  ['clear-ov','over-ov','shop-ov','lvlup-ov','pause-ov'].forEach(id=>document.getElementById(id).classList.add('hidden'));
  document.getElementById('title-ov').classList.remove('hidden');
  document.getElementById('boss-bar').classList.remove('show');G=null;
}

// LEVEL UP
function showLvlUpModal(){
  document.getElementById('stat-grid').innerHTML=`
    <button class="stat-btn" onclick="pickStat('hp')">❤️ 최대 HP +30</button>
    <button class="stat-btn" onclick="pickStat('atk')">⚔️ ATK +6</button>
    <button class="stat-btn" onclick="pickStat('def')">🛡️ DEF +4</button>
    <button class="stat-btn" onclick="pickStat('spd')">💨 SPD +0.5</button>
    <button class="stat-btn" onclick="pickStat('mp')">🔷 최대 MP +22</button>
    <button class="stat-btn" onclick="pickStat('crit')">⚡ 크리 +6%</button>`;
  document.getElementById('lvlup-ov').classList.remove('hidden');
}
function pickStat(stat){
  const p=G.player;
  if(stat==='hp'){p.maxHp+=30;p.hp=Math.min(p.maxHp,p.hp+30);}
  else if(stat==='atk') p.atk+=6;
  else if(stat==='def') p.def+=4;
  else if(stat==='spd') p.spd+=.5;
  else if(stat==='mp'){p.maxMp+=22;p.mp=Math.min(p.maxMp,p.mp+22);}
  else if(stat==='crit') p.critBonus=(p.critBonus||0)+.06;
  document.getElementById('lvlup-ov').classList.add('hidden');G.pendingLvlUp=false;
}

// TITLE
function buildTitle(){
  const row=document.getElementById('char-row');row.innerHTML='';
  for(const [id,c] of Object.entries(CLASSES)){
    const div=document.createElement('div');div.className='ccard';div.id='cc-'+id;
    div.onclick=()=>{selCharId=id;document.querySelectorAll('.ccard').forEach(x=>x.classList.remove('sel'));div.classList.add('sel');document.getElementById('start-btn').disabled=false;ensureAudio();};
    div.innerHTML=`<div class="ccard-icon">${c.icon}</div>
      <div class="ccard-name">${c.name}</div><div class="ccard-role">${c.role}</div>
      <div class="ccard-desc">${c.desc}</div>`;
    row.appendChild(div);
  }
}
function startPressed(){if(!selCharId) return;document.getElementById('title-ov').classList.add('hidden');buildLayout();initGame(selCharId,0);}

// WEB AUDIO
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function synth(freq,type,dur,vol=.3,del=0){
  if(!ACtx) return;
  try{
    const o=ACtx.createOscillator(),g=ACtx.createGain();
    o.connect(g);g.connect(ACtx.destination);o.type=type;o.frequency.value=freq;
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

// IDLE ANIMATION
function titleIdle(ts){
  if(G) return;
  ctx.fillStyle='#08060f';ctx.fillRect(0,0,W(),H());
  ctx.save();ctx.globalAlpha=.04+Math.sin(ts*.001)*.02;
  ctx.font='900 70px sans-serif';ctx.fillStyle='#ff6600';ctx.textAlign='center';
  ctx.fillText('DUNGEON CRUSH',W()/2,H()/2+30);ctx.restore();
  updateParts(1);drawParts(0,0);
  if(Math.random()<.28) spawnParts(Math.random()*W(),Math.random()*H(),{n:2,col:['#ff6600','#ffaa00','#cc44ff'],glow:true,sMin:1,sMax:3,grav:-.02,dMin:.01,dMax:.015});
  requestAnimationFrame(titleIdle);
}

// BOOT
buildTitle();
requestAnimationFrame(titleIdle);
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
header{display:none!important;}footer{display:none!important;}iframe{border:none!important;}
</style>
""", unsafe_allow_html=True)
    components.html(GAME_HTML, height=780, scrolling=False)
