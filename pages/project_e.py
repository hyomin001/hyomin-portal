import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>DUNGEON FIGHTER</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Rajdhani:wght@600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --bg:#04020a;--gold:#f5c518;--red:#ff1a2e;--blue:#1a8fff;
  --green:#00ff88;--purple:#cc00ff;--orange:#ff6a00;
  --border:rgba(245,197,24,0.2);--dark:#0a0614;
}
html,body{width:100%;height:100%;background:var(--bg);overflow:hidden;
  font-family:'Noto Sans KR',sans-serif;color:#ddd;cursor:default;}
#wrap{width:100vw;height:100vh;display:flex;flex-direction:column;}

/* ── HUD ── */
#hud{
  height:54px;background:linear-gradient(180deg,rgba(4,2,10,1),rgba(4,2,10,0.85));
  border-bottom:1px solid rgba(245,197,24,0.15);
  display:flex;align-items:center;gap:10px;padding:0 14px;flex-shrink:0;
  position:relative;z-index:50;
}
.hud-name{
  font-family:'Black Han Sans',sans-serif;font-size:.82rem;
  color:var(--gold);letter-spacing:3px;min-width:68px;
  text-shadow:0 0 12px rgba(245,197,24,0.5);
}
.bar-wrap{display:flex;flex-direction:column;gap:3px;}
.bar-row{display:flex;align-items:center;gap:5px;}
.bar-lbl{font-size:.44rem;color:#555;width:16px;text-align:right;letter-spacing:.5px;}
.bar-bg{
  height:10px;border-radius:2px;overflow:hidden;position:relative;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.06);
}
.bar-fill{height:100%;border-radius:2px;transition:width .07s linear;}
#hp-fill{background:linear-gradient(90deg,#550000,#cc0011,#ff2233,#ff5566);width:100%;}
#mp-fill{background:linear-gradient(90deg,#001155,#0033bb,#1166ff,#33aaff);width:100%;}
#xp-fill{background:linear-gradient(90deg,#223300,#448800,#66cc00,#aaff33);width:0%;}
.bar-val{
  position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-size:.42rem;color:rgba(255,255,255,.78);font-weight:900;letter-spacing:.5px;
}
.statbox{
  background:rgba(255,255,255,.03);border:1px solid var(--border);
  border-radius:3px;padding:2px 7px;text-align:center;min-width:38px;
}
.statbox-v{font-size:.76rem;font-weight:900;color:var(--gold);line-height:1.1;}
.statbox-l{font-size:.36rem;color:#444;letter-spacing:.5px;}
.floor-badge{
  font-family:'Rajdhani',sans-serif;font-size:.92rem;font-weight:700;
  color:#fff;background:rgba(245,197,24,.08);
  border:1px solid var(--border);border-radius:3px;
  padding:2px 10px;letter-spacing:2px;margin-left:auto;
}
#buff-icons{display:flex;gap:3px;font-size:.9rem;}

/* ── GAME AREA ── */
#game-area{flex:1;position:relative;overflow:hidden;}
canvas#gc{display:block;width:100%;height:100%;}

/* ── SKILL BAR ── */
#skill-bar{
  position:absolute;bottom:0;left:0;right:0;height:64px;
  background:linear-gradient(0deg,rgba(4,2,10,.98),rgba(4,2,10,.75));
  border-top:1px solid rgba(245,197,24,.12);
  display:flex;align-items:center;justify-content:center;
  gap:6px;padding:0 12px;z-index:50;
}
.sk{
  width:52px;height:54px;border-radius:5px;position:relative;
  background:rgba(255,255,255,.04);border:1px solid rgba(245,197,24,.18);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  cursor:default;transition:border-color .12s,box-shadow .12s;
}
.sk.ready{border-color:rgba(245,197,24,.7);box-shadow:0 0 14px rgba(245,197,24,.28);}
.sk.active{border-color:#fff;box-shadow:0 0 20px rgba(255,255,255,.5);}
.sk.cd{opacity:.38;}
.sk-ico{font-size:1.45rem;line-height:1;}
.sk-key{position:absolute;bottom:2px;right:4px;font-size:.38rem;color:#555;}
.sk-mp{position:absolute;top:2px;left:4px;font-size:.38rem;color:#4488ff;}
.sk-cd-txt{
  position:absolute;inset:0;border-radius:5px;
  background:rgba(0,0,0,.8);display:flex;align-items:center;justify-content:center;
  font-size:.72rem;color:var(--gold);font-weight:900;
}
.ctrl-hint{
  position:absolute;right:12px;font-size:.44rem;color:#2a2038;
  line-height:2;text-align:right;pointer-events:none;
}

/* ── BOSS BAR ── */
#boss-bar{
  position:absolute;top:8px;left:50%;transform:translateX(-50%);
  width:420px;pointer-events:none;z-index:40;opacity:0;transition:opacity .35s;
}
#boss-bar.show{opacity:1;}
#boss-name-txt{
  text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.78rem;
  color:#ff2233;margin-bottom:3px;text-shadow:0 0 14px rgba(255,0,40,.7);
  letter-spacing:3px;
}
#boss-hp-outer{
  height:13px;background:rgba(255,255,255,.04);
  border-radius:2px;border:1px solid rgba(255,40,60,.3);overflow:hidden;
}
#boss-hp-inner{
  height:100%;border-radius:2px;
  background:linear-gradient(90deg,#440000,#bb0011,#ff1122,#ff4455);
  transition:width .12s;
}
#boss-phase-lbl{text-align:center;font-size:.5rem;color:#ff6677;letter-spacing:3px;margin-top:2px;}

/* ── COMBO ── */
#combo{position:absolute;top:12px;right:14px;text-align:right;pointer-events:none;z-index:45;}
#combo-n{
  font-family:'Black Han Sans',sans-serif;font-size:2.8rem;
  color:var(--gold);line-height:1;
  text-shadow:0 0 28px rgba(245,197,24,.9),2px 2px 0 rgba(0,0,0,.9);
  transition:transform .06s;
}
#combo-l{font-size:.56rem;color:var(--orange);letter-spacing:4px;}
#combo.hidden{opacity:0;}
#combo.pop #combo-n{transform:scale(1.25);}

/* ── HIT FLASH / CRIT ── */
#hit-vfx{position:absolute;inset:0;pointer-events:none;z-index:100;opacity:0;}
@keyframes crit-burst{0%{opacity:.7;}100%{opacity:0;}}
#crit-vfx{
  position:absolute;inset:0;pointer-events:none;z-index:95;opacity:0;
  background:radial-gradient(circle at 50% 50%,rgba(255,220,0,.35) 0%,transparent 65%);
}

/* ── BOSS WARNING ── */
@keyframes bwPop{0%,100%{opacity:0;transform:translate(-50%,-50%) scale(.7);}45%,55%{opacity:1;transform:translate(-50%,-50%) scale(1);}}
#boss-warn{
  position:absolute;top:46%;left:50%;z-index:180;display:none;
  font-family:'Black Han Sans',sans-serif;font-size:2rem;
  color:#ff1122;text-shadow:0 0 35px rgba(255,0,40,1);
  letter-spacing:8px;text-align:center;
  animation:bwPop 2.6s ease forwards;pointer-events:none;
}

/* ── ACHIEVEMENT ── */
#achiev{
  position:absolute;top:60px;left:50%;
  transform:translateX(-50%) translateY(-110px);
  background:rgba(30,18,2,.97);border:1px solid rgba(245,197,24,.55);
  border-radius:6px;padding:7px 18px;display:flex;align-items:center;
  gap:9px;z-index:300;transition:transform .35s cubic-bezier(.34,1.56,.64,1);
  pointer-events:none;
}
#achiev.show{transform:translateX(-50%) translateY(0);}
#ach-icon{font-size:1.2rem;}
#ach-title{font-size:.72rem;color:var(--gold);font-family:'Black Han Sans',sans-serif;}
#ach-sub{font-size:.46rem;color:#886600;}

/* ── MINIMAP ── */
#minimap{
  position:absolute;bottom:68px;right:12px;
  width:128px;height:30px;background:rgba(0,0,0,.8);
  border:1px solid var(--border);border-radius:3px;overflow:hidden;z-index:45;
}

/* ── EQUIP QUICK ── */
#equip-row{position:absolute;bottom:68px;left:12px;z-index:45;display:flex;gap:5px;}
.eq-slot{
  width:38px;height:38px;background:rgba(0,0,0,.75);
  border:1px solid rgba(245,197,24,.22);border-radius:4px;
  display:flex;align-items:center;justify-content:center;font-size:.95rem;
  position:relative;
}
.eq-lbl{
  position:absolute;bottom:-14px;left:50%;transform:translateX(-50%);
  font-size:.37rem;color:#333;white-space:nowrap;
}

/* ── OVERLAYS ── */
.ov{
  position:absolute;inset:0;z-index:200;
  display:flex;align-items:center;justify-content:center;
  background:rgba(4,2,10,.97);
}
.ov.hidden{display:none;}

/* ── TITLE ── */
#title-ov{flex-direction:column;text-align:center;}
.logo{
  font-family:'Black Han Sans',sans-serif;font-size:3.4rem;
  letter-spacing:10px;
  background:linear-gradient(135deg,#ff4400 0%,#ff9900 30%,#ffdd00 55%,#ff6600 80%,#ff2200 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 36px rgba(255,140,0,.7));margin-bottom:4px;
}
.logo-sub{
  font-family:'Rajdhani',sans-serif;font-size:.88rem;color:#333;
  letter-spacing:12px;margin-bottom:32px;
}
.char-grid{
  display:flex;gap:9px;margin-bottom:24px;flex-wrap:wrap;
  justify-content:center;max-width:840px;
}
.cc{
  width:96px;background:rgba(255,255,255,.02);
  border:1px solid rgba(245,197,24,.1);border-radius:8px;
  padding:11px 8px;cursor:pointer;transition:all .18s;text-align:center;
}
.cc:hover,.cc.sel{
  border-color:rgba(245,197,24,.8);background:rgba(245,197,24,.07);
  transform:translateY(-5px);box-shadow:0 10px 32px rgba(245,197,24,.22);
}
.cc-ico{font-size:2.1rem;margin-bottom:6px;}
.cc-name{font-family:'Black Han Sans',sans-serif;font-size:.7rem;color:var(--gold);letter-spacing:2px;}
.cc-role{font-size:.46rem;color:#444;margin-top:2px;}
.cc-desc{font-size:.44rem;color:#333;margin-top:6px;line-height:1.55;}
.start-btn{
  padding:13px 52px;
  background:linear-gradient(135deg,#6a2000,#dd4400,#ff6600);
  border:none;border-radius:4px;color:#fff;
  font-family:'Black Han Sans',sans-serif;font-size:.92rem;
  letter-spacing:5px;cursor:pointer;
  box-shadow:0 0 28px rgba(255,100,0,.45);transition:all .18s;
}
.start-btn:hover{transform:scale(1.07);filter:brightness(1.2);}
.start-btn:disabled{opacity:.2;cursor:default;transform:none;filter:none;}

/* ── RESULT ── */
.res-box{
  background:rgba(8,4,18,.98);border:1px solid var(--border);
  border-radius:10px;padding:28px 38px;min-width:360px;
  text-align:center;box-shadow:0 0 70px rgba(245,197,24,.1);
}
.res-title{
  font-family:'Black Han Sans',sans-serif;font-size:1.85rem;
  letter-spacing:5px;margin-bottom:14px;
}
.clear-col{color:var(--gold);text-shadow:0 0 22px rgba(245,197,24,.6);}
.over-col{color:var(--red);text-shadow:0 0 22px rgba(255,30,50,.6);}
.res-stats{
  display:grid;grid-template-columns:1fr 1fr;gap:6px;
  margin:12px 0;text-align:left;
}
.rs{font-size:.68rem;color:#666;display:flex;justify-content:space-between;}
.rs b{color:var(--gold);}
.btn-row{display:flex;gap:9px;justify-content:center;margin-top:14px;}
.btn{
  padding:10px 24px;border:none;border-radius:4px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:.78rem;
  letter-spacing:2px;transition:all .16s;
}
.btn:hover{transform:translateY(-2px);filter:brightness(1.25);}
.btn-g{background:linear-gradient(135deg,#115500,#22aa00);color:#fff;}
.btn-r{background:linear-gradient(135deg,#440000,#990000);color:#fff;}
.btn-gray{background:rgba(255,255,255,.06);color:#666;border:1px solid rgba(255,255,255,.1);}

/* ── SHOP ── */
#shop-ov{flex-direction:column;text-align:center;}
.shop-hd{
  font-family:'Black Han Sans',sans-serif;font-size:1.6rem;
  color:var(--gold);letter-spacing:5px;margin-bottom:6px;
}
.shop-grid{display:flex;gap:9px;flex-wrap:wrap;justify-content:center;margin:13px 0;}
.sc{
  width:120px;background:rgba(255,255,255,.03);
  border:1px solid rgba(245,197,24,.14);border-radius:6px;
  padding:10px 8px;cursor:pointer;transition:all .16s;text-align:center;
}
.sc:hover:not(.cant){border-color:rgba(245,197,24,.65);background:rgba(245,197,24,.06);}
.sc.cant{opacity:.28;cursor:default;}
.sc-ico{font-size:1.6rem;margin-bottom:4px;}
.sc-nm{font-size:.64rem;color:#ccc;font-weight:700;}
.sc-dc{font-size:.48rem;color:#484;margin-top:2px;}
.sc-pr{font-size:.7rem;color:var(--gold);font-weight:900;margin-top:6px;}

/* ── LEVEL UP ── */
#lvlup-ov{flex-direction:column;text-align:center;}
.lvlup-t{
  font-family:'Black Han Sans',sans-serif;font-size:2rem;
  color:var(--gold);letter-spacing:5px;margin-bottom:8px;
}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0;}
.stat-btn{
  padding:12px 10px;border:1px solid var(--border);border-radius:5px;
  background:rgba(255,255,255,.04);cursor:pointer;transition:all .16s;
  font-family:'Noto Sans KR',sans-serif;font-size:.74rem;color:#ccc;
}
.stat-btn:hover{
  border-color:var(--gold);background:rgba(245,197,24,.1);
  color:var(--gold);transform:scale(1.02);
}

/* ── PAUSE ── */
#pause-ov{background:rgba(4,2,10,.94);}

/* ── DAMAGE NUMBERS ── */
@keyframes dmgRise{
  0%{opacity:1;transform:translateY(0) scale(1);}
  20%{transform:translateY(-12px) scale(1.18);}
  100%{opacity:0;transform:translateY(-80px) scale(.6);}
}
.dnum{
  position:absolute;pointer-events:none;
  font-family:'Black Han Sans',sans-serif;
  animation:dmgRise 1.05s ease forwards;z-index:160;
  text-shadow:1px 1px 0 rgba(0,0,0,1),2px 2px 6px rgba(0,0,0,.9);
  white-space:nowrap;
}
</style>
</head>
<body>
<div id="wrap">
  <!-- HUD -->
  <div id="hud">
    <div class="hud-name" id="hud-nm">—</div>
    <div class="bar-wrap">
      <div class="bar-row">
        <span class="bar-lbl">HP</span>
        <div class="bar-bg" style="width:156px">
          <div class="bar-fill" id="hp-fill"></div>
          <div class="bar-val" id="hp-val"></div>
        </div>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">MP</span>
        <div class="bar-bg" style="width:156px">
          <div class="bar-fill" id="mp-fill"></div>
          <div class="bar-val" id="mp-val"></div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:2px;margin-left:8px;">
      <div style="font-size:.42rem;color:#333;letter-spacing:1px;">EXP</div>
      <div class="bar-bg" style="width:100px;height:7px;"><div class="bar-fill" id="xp-fill"></div></div>
      <div style="font-size:.4rem;color:#2a2a2a;" id="xp-val">0/100</div>
    </div>
    <div style="display:flex;gap:5px;margin-left:7px;" id="stat-row">
      <div class="statbox"><div class="statbox-v" id="s-lv">1</div><div class="statbox-l">LV</div></div>
      <div class="statbox"><div class="statbox-v" id="s-atk" style="color:#ff8866">0</div><div class="statbox-l">ATK</div></div>
      <div class="statbox"><div class="statbox-v" id="s-def" style="color:#4499ff">0</div><div class="statbox-l">DEF</div></div>
      <div class="statbox"><div class="statbox-v" id="s-kill">0</div><div class="statbox-l">KILL</div></div>
      <div class="statbox"><div class="statbox-v" id="s-scr">0</div><div class="statbox-l">SCR</div></div>
      <div class="statbox"><div class="statbox-v" id="s-gld" style="color:var(--gold)">0</div><div class="statbox-l">💰</div></div>
    </div>
    <div id="buff-icons"></div>
    <div class="floor-badge" id="floor-b">1F</div>
  </div>

  <!-- GAME -->
  <div id="game-area">
    <canvas id="gc"></canvas>
    <div id="hit-vfx"></div>
    <div id="crit-vfx"></div>

    <!-- Boss bar -->
    <div id="boss-bar">
      <div id="boss-name-txt">BOSS</div>
      <div id="boss-hp-outer"><div id="boss-hp-inner" style="width:100%"></div></div>
      <div id="boss-phase-lbl"></div>
    </div>

    <!-- Combo -->
    <div id="combo" class="hidden">
      <div id="combo-n">0</div>
      <div id="combo-l">COMBO</div>
    </div>

    <!-- Minimap -->
    <div id="minimap"><canvas id="mm" width="128" height="30"></canvas></div>

    <!-- Equip row -->
    <div id="equip-row">
      <div class="eq-slot" id="eq-w">🗡️<span class="eq-lbl">무기</span></div>
      <div class="eq-slot" id="eq-a">🛡️<span class="eq-lbl">방어</span></div>
      <div class="eq-slot" id="eq-c">💍<span class="eq-lbl">장신구</span></div>
    </div>

    <div id="boss-warn">⚠ BOSS ⚠</div>
    <div id="achiev">
      <div id="ach-icon">🏆</div>
      <div><div id="ach-title">업적</div><div id="ach-sub">달성</div></div>
    </div>

    <!-- Skill bar -->
    <div id="skill-bar">
      <div id="sk-cont" style="display:flex;gap:6px;"></div>
      <div class="ctrl-hint">
        ←→ 이동 &nbsp;|&nbsp; Z 점프(2단)<br>
        X 공격 &nbsp;|&nbsp; ↑+X 어퍼 &nbsp;|&nbsp; ↓+X 다운<br>
        A~G 스킬 &nbsp;|&nbsp; Space 회피 &nbsp;|&nbsp; P 일시정지
      </div>
    </div>

    <!-- OVERLAYS -->
    <div class="ov" id="title-ov">
      <div>
        <div class="logo">던전 파이터</div>
        <div class="logo-sub">DUNGEON FIGHTER ONLINE v3</div>
        <div class="char-grid" id="char-grid"></div>
        <button class="start-btn" id="start-btn" onclick="startPressed()" disabled>전투 시작 ▶</button>
      </div>
    </div>

    <div class="ov hidden" id="lvlup-ov">
      <div class="res-box">
        <div class="lvlup-t">⬆ LEVEL UP!</div>
        <div style="font-size:.7rem;color:#444;margin-bottom:6px;">강화할 스탯 선택</div>
        <div class="stat-grid" id="stat-grid"></div>
      </div>
    </div>

    <div class="ov hidden" id="shop-ov">
      <div>
        <div class="shop-hd">⚗ 상 점</div>
        <div style="font-size:.7rem;color:#444;">보유 골드: <span id="shop-gold" style="color:var(--gold);font-weight:700">0</span></div>
        <div class="shop-grid" id="shop-grid"></div>
        <button class="btn btn-g" onclick="continueAfterShop()">다음 스테이지 →</button>
      </div>
    </div>

    <div class="ov hidden" id="clear-ov">
      <div class="res-box">
        <div class="res-title clear-col">✦ STAGE CLEAR ✦</div>
        <div class="res-stats" id="clear-stats"></div>
        <div class="btn-row">
          <button class="btn btn-g" onclick="openShop()">상점 →</button>
          <button class="btn btn-gray" onclick="gotoTitle()">타이틀</button>
        </div>
      </div>
    </div>

    <div class="ov hidden" id="over-ov">
      <div class="res-box">
        <div class="res-title over-col">💀 GAME OVER</div>
        <div class="res-stats" id="over-stats"></div>
        <div class="btn-row">
          <button class="btn btn-r" onclick="retryStage()">재도전 ↺</button>
          <button class="btn btn-gray" onclick="gotoTitle()">타이틀</button>
        </div>
      </div>
    </div>

    <div class="ov hidden" id="pause-ov">
      <div style="text-align:center">
        <div style="font-family:'Black Han Sans',sans-serif;font-size:2.5rem;color:#fff;letter-spacing:8px;">⏸ PAUSE</div>
        <div style="font-size:.7rem;color:#333;margin-top:14px;letter-spacing:3px;">P 키로 계속</div>
      </div>
    </div>
  </div>
</div>

<script>
'use strict';
// ═══════════════════════════════════════════════════════════
//  DUNGEON FIGHTER v3 — DNF 스타일 횡스크롤 액션
//  히트스톱 / 넉백 / 슈퍼아머 / 공중콤보 / 풀 이펙트
// ═══════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');

function resize() {
  const a = document.getElementById('game-area');
  canvas.width  = a.clientWidth  || 960;
  canvas.height = a.clientHeight || 500;
}
resize();
window.addEventListener('resize', () => { resize(); });

const W = () => canvas.width;
const H = () => canvas.height;
const GY = () => H() - 62; // ground y

// ── INPUT ────────────────────────────────────────────────
const KEY = {}, JUST = {};
window.addEventListener('keydown', e => {
  if (!KEY[e.key]) { KEY[e.key] = true; JUST[e.key] = true; }
  if ([' ','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e => { KEY[e.key] = false; });
function flushJust() { for (const k in JUST) delete JUST[k]; }

// ── PARTICLES ────────────────────────────────────────────
const PARTS = [];
function spawnParts(x, y, o = {}) {
  const n = o.n || 8;
  for (let i = 0; i < n; i++) {
    const a = (o.dir || 0) + (Math.random() - .5) * (o.spread || Math.PI * 2);
    const s = (o.sMin || 1) + Math.random() * (o.sMax || 5);
    const col = Array.isArray(o.col) ? o.col[Math.floor(Math.random()*o.col.length)] : (o.col || '#fff');
    PARTS.push({
      x, y,
      vx: Math.cos(a)*s + (o.vxb||0),
      vy: Math.sin(a)*s - (o.upb||0),
      life: 1,
      decay: (o.dMin||.018) + Math.random()*(o.dMax||.03),
      col, sz: (o.szMin||2) + Math.random()*(o.szMax||5),
      glow: !!o.glow, grav: o.grav !== undefined ? o.grav : .15,
      type: o.type||'c', spin: o.spin ? Math.random()*Math.PI*2 : 0,
    });
  }
}
function tickParts(dt) {
  for (let i = PARTS.length-1; i >= 0; i--) {
    const p = PARTS[i];
    p.x += p.vx*dt; p.y += p.vy*dt;
    p.vy += p.grav*dt; p.vx *= .94;
    p.life -= p.decay*dt;
    if (p.spin) p.spin += .09*dt;
    if (p.life <= 0) PARTS.splice(i, 1);
  }
}
function drawParts(cx, cy) {
  ctx.save();
  for (const p of PARTS) {
    const sx = p.x - cx, sy = p.y - cy;
    if (sx < -80 || sx > W()+80 || sy < -80 || sy > H()+80) continue;
    ctx.globalAlpha = Math.max(0, p.life);
    if (p.glow) { ctx.shadowColor = p.col; ctx.shadowBlur = p.sz*3; }
    ctx.fillStyle = p.col;
    if (p.type === 'sq') {
      ctx.save(); ctx.translate(sx,sy); ctx.rotate(p.spin);
      ctx.fillRect(-p.sz/2,-p.sz/2,p.sz,p.sz); ctx.restore();
    } else if (p.type === 'star') {
      drawStar5(ctx, sx, sy, p.sz, p.col, p.spin);
    } else {
      ctx.beginPath(); ctx.arc(sx,sy,p.sz,0,Math.PI*2); ctx.fill();
    }
    if (p.glow) ctx.shadowBlur = 0;
  }
  ctx.globalAlpha = 1; ctx.restore();
}
function drawStar5(ctx, x, y, r, col, rot=0) {
  ctx.save(); ctx.translate(x,y); ctx.rotate(rot); ctx.fillStyle=col;
  ctx.beginPath();
  for (let i = 0; i < 5; i++) {
    const a = i*Math.PI*2/5 - Math.PI/2;
    const b = a + Math.PI/5;
    if (i===0) ctx.moveTo(Math.cos(a)*r, Math.sin(a)*r);
    else ctx.lineTo(Math.cos(a)*r, Math.sin(a)*r);
    ctx.lineTo(Math.cos(b)*r*.42, Math.sin(b)*r*.42);
  }
  ctx.closePath(); ctx.fill(); ctx.restore();
}

// ── VISUAL EFFECTS ───────────────────────────────────────
const FX = [];
function addFx(type, x, y, opts={}) {
  FX.push({ type, x, y, t:0, life:1, maxLife: opts.life||1, ...opts });
}
function tickFx(dt) {
  for (let i = FX.length-1; i >= 0; i--) {
    const f = FX[i];
    f.t += dt; f.life = 1 - f.t / f.maxLife;
    if (f.life <= 0) FX.splice(i, 1);
  }
}
function drawFx(cx, cy) {
  ctx.save();
  for (const f of FX) {
    const x = f.x - cx, y = f.y - cy;
    ctx.globalAlpha = Math.max(0, f.life);
    switch (f.type) {
      case 'slash':      _fxSlash(ctx, x, y, f); break;
      case 'wave':       _fxWave(ctx, x, y, f);  break;
      case 'explosion':  _fxExp(ctx, x, y, f);   break;
      case 'beam':       _fxBeam(ctx, x, y, f);  break;
      case 'holy':       _fxHoly(ctx, x, y, f);  break;
      case 'darkwave':   _fxDark(ctx, x, y, f);  break;
      case 'firepillar': _fxFire(ctx, x, y, f);  break;
      case 'iceburst':   _fxIce(ctx, x, y, f);   break;
      case 'lightning':  _fxLightning(ctx, x, y, f); break;
      case 'shockwave':  _fxShock(ctx, x, y, f); break;
      case 'hit':        _fxHit(ctx, x, y, f);   break;
    }
  }
  ctx.globalAlpha = 1; ctx.restore();
}
function _fxSlash(ctx,x,y,f){
  const p=1-f.life; const r=(55+p*100)*(f.sc||1);
  ctx.strokeStyle=f.col||'#fff'; ctx.lineWidth=7*f.life;
  ctx.shadowColor=f.col||'#fff'; ctx.shadowBlur=22;
  ctx.beginPath();
  ctx.arc(x,y,r,f.ang-.3,f.ang+.3+p*1.1);
  ctx.stroke();
  ctx.shadowBlur=0;
  for(let i=0;i<3;i++){
    ctx.globalAlpha=f.life*(1-i*.3);
    ctx.lineWidth=3-i;
    ctx.beginPath();
    ctx.arc(x,y,r*(1.06+i*.05),f.ang-.22+i*.04,f.ang+.18+i*.04+p*.7);
    ctx.stroke();
  }
}
function _fxWave(ctx,x,y,f){
  const p=1-f.life; const r=(18+p*180)*(f.sc||1);
  ctx.strokeStyle=f.col||'#fff'; ctx.lineWidth=5*f.life;
  ctx.shadowColor=f.col||'#fff'; ctx.shadowBlur=18;
  ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke();
  ctx.shadowBlur=0;
  if(f.life>.6){ ctx.lineWidth=2*f.life; ctx.beginPath(); ctx.arc(x,y,r*.65,0,Math.PI*2); ctx.stroke(); }
}
function _fxExp(ctx,x,y,f){
  const p=1-f.life; const r=(8+p*130)*(f.sc||1);
  const g=ctx.createRadialGradient(x,y,0,x,y,r);
  g.addColorStop(0,f.col||'#ff8800'); g.addColorStop(.4,f.col2||'#ff3300'); g.addColorStop(1,'transparent');
  ctx.fillStyle=g; ctx.shadowColor=f.col||'#ff8800'; ctx.shadowBlur=40;
  ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;
  for(let i=0;i<3;i++){
    ctx.globalAlpha=f.life*(1-i*.3);
    ctx.strokeStyle='rgba(255,200,80,.35)'; ctx.lineWidth=3;
    ctx.beginPath(); ctx.arc(x,y,r*(1.1+i*.25),0,Math.PI*2); ctx.stroke();
  }
}
function _fxBeam(ctx,x,y,f){
  const w=Math.max(2,22*f.life); const len=f.len||220;
  const g=ctx.createLinearGradient(x,y,x+Math.cos(f.ang)*len,y+Math.sin(f.ang)*len);
  g.addColorStop(0,f.col||'#fff'); g.addColorStop(1,'transparent');
  ctx.strokeStyle=g; ctx.lineWidth=w;
  ctx.shadowColor=f.col||'#fff'; ctx.shadowBlur=32;
  ctx.beginPath(); ctx.moveTo(x,y);
  ctx.lineTo(x+Math.cos(f.ang)*len,y+Math.sin(f.ang)*len);
  ctx.stroke(); ctx.shadowBlur=0;
}
function _fxHoly(ctx,x,y,f){
  const p=1-f.life; const r=(28+p*120)*(f.sc||1);
  ctx.strokeStyle='rgba(255,245,160,.95)'; ctx.lineWidth=5*f.life;
  ctx.shadowColor='#ffff88'; ctx.shadowBlur=38;
  ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke(); ctx.shadowBlur=0;
  for(let i=0;i<8;i++){
    const a=i/8*Math.PI*2+f.t*.06;
    ctx.globalAlpha=f.life*.65;
    ctx.strokeStyle='rgba(255,255,180,.55)'; ctx.lineWidth=2;
    ctx.beginPath();
    ctx.moveTo(x+Math.cos(a)*r*.5,y+Math.sin(a)*r*.5);
    ctx.lineTo(x+Math.cos(a)*r*(1+Math.sin(f.t*.12+i)*.15),y+Math.sin(a)*r*(1+Math.sin(f.t*.12+i)*.15));
    ctx.stroke();
  }
}
function _fxDark(ctx,x,y,f){
  const p=1-f.life; const r=(18+p*100)*(f.sc||1);
  const g=ctx.createRadialGradient(x,y,0,x,y,r);
  g.addColorStop(0,'rgba(160,0,220,.98)'); g.addColorStop(.5,'rgba(80,0,130,.7)'); g.addColorStop(1,'transparent');
  ctx.fillStyle=g; ctx.shadowColor='#9900cc'; ctx.shadowBlur=45;
  ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;
  for(let i=0;i<6;i++){
    const a=i/6*Math.PI*2+f.t*.1+p*Math.PI;
    ctx.globalAlpha=f.life*.6; ctx.strokeStyle='rgba(210,80,255,.7)'; ctx.lineWidth=2;
    ctx.beginPath(); ctx.moveTo(x,y);
    ctx.quadraticCurveTo(x+Math.cos(a+.5)*r*.72,y+Math.sin(a+.5)*r*.72,x+Math.cos(a)*r,y+Math.sin(a)*r);
    ctx.stroke();
  }
}
function _fxFire(ctx,x,y,f){
  const w=(32+f.life*22)*(f.sc||1); const h=220*(f.sc||1);
  for(let i=0;i<8;i++){
    const yy=y-i*(h/8); const ww=w*(1-i/9);
    const g=ctx.createRadialGradient(x,yy,0,x,yy,ww);
    const alpha=f.life*(1-i/9)*.85;
    g.addColorStop(0,`rgba(255,245,110,${alpha})`);
    g.addColorStop(.5,`rgba(255,110,0,${alpha*.7})`);
    g.addColorStop(1,'transparent');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(x,yy,ww,0,Math.PI*2); ctx.fill();
  }
}
function _fxIce(ctx,x,y,f){
  const p=1-f.life;
  for(let i=0;i<8;i++){
    const a=i/8*Math.PI*2+f.t*.04;
    const d=p*90*(f.sc||1);
    const sx=x+Math.cos(a)*d, sy=y+Math.sin(a)*d;
    ctx.save(); ctx.translate(sx,sy); ctx.rotate(a+f.t*.12);
    ctx.fillStyle=`rgba(100,210,255,${f.life*.88})`;
    ctx.shadowColor='#88ccff'; ctx.shadowBlur=14;
    const sz=14*f.life*(f.sc||1);
    ctx.beginPath(); ctx.moveTo(0,-sz); ctx.lineTo(sz*.3,0); ctx.lineTo(0,sz); ctx.lineTo(-sz*.3,0);
    ctx.closePath(); ctx.fill(); ctx.shadowBlur=0; ctx.restore();
  }
}
function _fxLightning(ctx,x,y,f){
  ctx.strokeStyle=`rgba(255,245,80,${f.life})`; ctx.lineWidth=3+f.life*5;
  ctx.shadowColor='#ffee00'; ctx.shadowBlur=28;
  const pts=[]; const n=12;
  for(let i=0;i<=n;i++) pts.push({x:x+(Math.random()-.5)*70,y:y-220+i*(220/n)+(Math.random()-.5)*22});
  ctx.beginPath(); ctx.moveTo(pts[0].x,pts[0].y);
  for(let i=1;i<pts.length;i++) ctx.lineTo(pts[i].x,pts[i].y);
  ctx.stroke(); ctx.shadowBlur=0;
}
function _fxShock(ctx,x,y,f){
  const p=1-f.life; const r=(30+p*200)*(f.sc||1);
  ctx.strokeStyle=f.col||'rgba(255,255,200,.7)';
  ctx.lineWidth=Math.max(.5,4*f.life*(f.sc||1));
  ctx.shadowColor=f.col||'#fff'; ctx.shadowBlur=16;
  ctx.beginPath(); ctx.ellipse(x,y,r,r*.22,0,0,Math.PI*2); ctx.stroke(); ctx.shadowBlur=0;
}
function _fxHit(ctx,x,y,f){
  const p=1-f.life; const r=(10+p*55)*(f.sc||1);
  ctx.strokeStyle=f.col||'#fff'; ctx.lineWidth=4*f.life;
  ctx.shadowColor=f.col||'#fff'; ctx.shadowBlur=16;
  const spikes=6;
  for(let i=0;i<spikes;i++){
    const a=i/spikes*Math.PI*2+f.ang;
    const len=r*(0.6+Math.random()*.6);
    ctx.beginPath();
    ctx.moveTo(x+Math.cos(a)*r*.25,y+Math.sin(a)*r*.25);
    ctx.lineTo(x+Math.cos(a)*len,y+Math.sin(a)*len);
    ctx.stroke();
  }
  ctx.shadowBlur=0;
}

// ── CHARACTER RENDERER ───────────────────────────────────
function drawChar(opts) {
  const {
    x, y, f, wp=0, ap=0, hitFlash=0, dead=false,
    skin, hair, torso, legs, weapon, offhand, headDeco,
    skillGlow, sc=1, dodging=false, onGround=true
  } = opts;
  ctx.save(); ctx.translate(x, y);
  if (dead) { ctx.globalAlpha=.3; ctx.rotate(f*Math.PI/2); }
  if (f===-1) ctx.scale(-1,1);
  if (hitFlash>0) ctx.filter=`brightness(${2.5-hitFlash*.1}) saturate(.05)`;
  if (dodging) ctx.globalAlpha=.55;

  const ls = dead ? 0 : Math.sin(wp)*.44;
  const lb = dead ? 0 : Math.abs(Math.sin(wp))*.15;
  // Legs
  for (const [ox, side] of [[-5*sc,-1],[5*sc,1]]) {
    ctx.save(); ctx.translate(ox, 2*sc); ctx.rotate(Math.PI/2+ls*side);
    ctx.strokeStyle=legs; ctx.lineWidth=7*sc; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,19*sc); ctx.stroke();
    ctx.translate(0,19*sc); ctx.rotate(-lb*side);
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,16*sc); ctx.stroke();
    ctx.fillStyle=legs;
    ctx.beginPath(); ctx.ellipse(3*sc,16*sc,7*sc,4*sc,0,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }
  // Torso
  ctx.fillStyle=torso;
  ctx.beginPath(); ctx.roundRect(-11*sc,-30*sc,22*sc,32*sc,4*sc); ctx.fill();
  ctx.fillStyle='rgba(0,0,0,.28)'; ctx.fillRect(-11*sc,-2*sc,22*sc,4*sc);
  // Arms
  const as = dead ? 0 : Math.sin(wp+Math.PI)*.32;
  const atk = dead ? 0 : Math.sin(ap)*.88;
  // Weapon arm
  ctx.save(); ctx.translate(11*sc,-22*sc); ctx.rotate(-Math.PI/5+atk+as);
  ctx.strokeStyle=skin; ctx.lineWidth=6*sc; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,18*sc); ctx.stroke();
  ctx.translate(0,18*sc); ctx.rotate(.22+atk*.5);
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,14*sc); ctx.stroke();
  drawWeapon(ctx, weapon, sc, ap, skillGlow);
  ctx.restore();
  // Off arm
  ctx.save(); ctx.translate(-11*sc,-22*sc); ctx.rotate(Math.PI/5-as);
  ctx.strokeStyle=skin; ctx.lineWidth=6*sc; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,18*sc); ctx.stroke();
  ctx.translate(0,18*sc); ctx.rotate(-.18);
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,14*sc); ctx.stroke();
  if (offhand) drawOffhand(ctx, offhand, sc);
  ctx.restore();
  // Head
  ctx.fillStyle=skin; ctx.beginPath(); ctx.arc(0,-38*sc,13*sc,0,Math.PI*2); ctx.fill();
  ctx.fillStyle=hair; ctx.beginPath(); ctx.arc(0,-40*sc,12*sc,Math.PI,Math.PI*2); ctx.fill();
  ctx.fillRect(-12*sc,-40*sc,24*sc,7*sc);
  // Eyes
  ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(5*sc,-39*sc,3.4*sc,0,Math.PI*2); ctx.fill();
  ctx.fillStyle=dead?'#555':'#100600';
  ctx.beginPath(); ctx.arc(6*sc,-39*sc,1.9*sc,0,Math.PI*2); ctx.fill();
  ctx.strokeStyle='rgba(0,0,0,.5)'; ctx.lineWidth=1.5*sc; ctx.lineCap='round';
  ctx.beginPath(); ctx.moveTo(2*sc,-44*sc); ctx.lineTo(8*sc,-43*sc); ctx.stroke();
  if (headDeco) drawHeadDeco(ctx, headDeco, sc);
  if (skillGlow) {
    ctx.globalAlpha=.36+Math.sin(Date.now()*.006)*.16;
    ctx.shadowColor=skillGlow; ctx.shadowBlur=26;
    ctx.strokeStyle=skillGlow; ctx.lineWidth=2*sc;
    ctx.beginPath(); ctx.arc(0,-15*sc,30*sc,0,Math.PI*2); ctx.stroke();
    ctx.shadowBlur=0; ctx.globalAlpha=1;
  }
  ctx.filter='none'; ctx.restore();
}
function drawWeapon(ctx, wpn, sc, ap, glow) {
  if (!wpn) return;
  const sw=Math.sin(ap)*.3; ctx.save(); ctx.rotate(-Math.PI/4+sw);
  if (glow) { ctx.shadowColor=glow; ctx.shadowBlur=18; }
  switch(wpn){
    case 'sword':
      ctx.fillStyle='#7a5810'; ctx.fillRect(-3*sc,0,6*sc,12*sc);
      ctx.fillStyle='#b89020'; ctx.fillRect(-9*sc,10*sc,18*sc,4*sc);
      ctx.fillStyle='#d8eeff'; ctx.beginPath();
      ctx.moveTo(-2*sc,14*sc); ctx.lineTo(0,-32*sc); ctx.lineTo(2*sc,14*sc); ctx.closePath(); ctx.fill();
      ctx.fillStyle='rgba(255,255,255,.5)';
      ctx.beginPath(); ctx.moveTo(0,14*sc); ctx.lineTo(.5*sc,-32*sc); ctx.lineTo(2*sc,14*sc); ctx.closePath(); ctx.fill();
      break;
    case 'axe':
      ctx.fillStyle='#553311'; ctx.fillRect(-3*sc,0,6*sc,32*sc);
      ctx.fillStyle='#997733'; ctx.beginPath();
      ctx.moveTo(-2*sc,9*sc); ctx.lineTo(-22*sc,-12*sc); ctx.lineTo(-22*sc,14*sc); ctx.lineTo(-2*sc,30*sc); ctx.closePath(); ctx.fill();
      ctx.fillStyle='rgba(255,200,80,.32)'; ctx.beginPath();
      ctx.moveTo(-2*sc,9*sc); ctx.lineTo(-22*sc,-12*sc); ctx.lineTo(-18*sc,2*sc); ctx.lineTo(-2*sc,19*sc); ctx.closePath(); ctx.fill();
      break;
    case 'staff':
      ctx.fillStyle='#551177'; ctx.fillRect(-2.5*sc,-32*sc,5*sc,52*sc);
      ctx.fillStyle='rgba(200,80,255,.88)'; ctx.shadowColor='#cc44ff'; ctx.shadowBlur=16;
      ctx.beginPath(); ctx.arc(0,-32*sc,9*sc,0,Math.PI*2); ctx.fill(); ctx.shadowBlur=0;
      break;
    case 'gun':
      ctx.fillStyle='#2a3344'; ctx.fillRect(-5*sc,-4*sc,32*sc,11*sc);
      ctx.fillStyle='#1a2234'; ctx.fillRect(22*sc,-9*sc,11*sc,20*sc);
      ctx.fillStyle='#445566'; ctx.fillRect(-8*sc,0,5*sc,9*sc);
      if(Math.sin(ap)>.6){ctx.fillStyle='rgba(255,240,100,.85)';ctx.shadowColor='#ffcc00';ctx.shadowBlur=20;ctx.beginPath();ctx.arc(33*sc,-4*sc,5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
      break;
    case 'dual':
      ctx.fillStyle='#c8e4ff';
      ctx.save();ctx.rotate(-.26);ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-24*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();ctx.restore();
      ctx.save();ctx.rotate(.26);ctx.translate(10*sc,0);ctx.beginPath();ctx.moveTo(-1.5*sc,10*sc);ctx.lineTo(0,-24*sc);ctx.lineTo(1.5*sc,10*sc);ctx.closePath();ctx.fill();ctx.restore();
      break;
    case 'scythe':
      ctx.fillStyle='#223311'; ctx.fillRect(-2.5*sc,-44*sc,5*sc,64*sc);
      ctx.strokeStyle='#445522'; ctx.lineWidth=5*sc;
      ctx.beginPath(); ctx.arc(-11*sc,-32*sc,27*sc,-Math.PI*.22,Math.PI*.4); ctx.stroke();
      ctx.strokeStyle='rgba(80,255,80,.35)'; ctx.lineWidth=2*sc;
      ctx.beginPath(); ctx.arc(-11*sc,-32*sc,27*sc,-Math.PI*.2,Math.PI*.22); ctx.stroke();
      break;
    case 'hammer':
      ctx.fillStyle='#554433'; ctx.fillRect(-3.5*sc,-12*sc,7*sc,44*sc);
      ctx.fillStyle='#887755'; ctx.fillRect(-15*sc,-24*sc,30*sc,24*sc);
      ctx.fillStyle='rgba(255,210,100,.16)'; ctx.fillRect(-13*sc,-22*sc,26*sc,9*sc);
      break;
  }
  ctx.shadowBlur=0; ctx.restore();
}
function drawOffhand(ctx, item, sc) {
  ctx.save(); ctx.rotate(Math.PI*.1);
  switch(item){
    case 'shield':
      ctx.fillStyle='#2a3b4d';
      ctx.beginPath(); ctx.roundRect(-8*sc,0,17*sc,22*sc,3*sc); ctx.fill();
      ctx.strokeStyle='#3a4c5e'; ctx.lineWidth=2*sc; ctx.stroke();
      ctx.fillStyle='rgba(80,140,220,.28)';
      ctx.beginPath(); ctx.arc(0,11*sc,5*sc,0,Math.PI*2); ctx.fill();
      break;
    case 'dagger':
      ctx.fillStyle='#aabccc';
      ctx.beginPath(); ctx.moveTo(-1*sc,0); ctx.lineTo(0,-17*sc); ctx.lineTo(1*sc,0); ctx.closePath(); ctx.fill();
      break;
    case 'tome':
      ctx.fillStyle='#3a1a3a'; ctx.fillRect(-8*sc,0,16*sc,20*sc);
      ctx.fillStyle='rgba(180,80,255,.45)'; ctx.fillRect(-6*sc,2*sc,12*sc,16*sc);
      break;
  }
  ctx.restore();
}
function drawHeadDeco(ctx, d, sc) {
  switch(d){
    case 'helm':
      ctx.fillStyle='#445566'; ctx.beginPath(); ctx.arc(0,-40*sc,15*sc,Math.PI,Math.PI*2); ctx.fill();
      ctx.fillRect(-15*sc,-40*sc,30*sc,5*sc);
      ctx.fillStyle='rgba(140,190,255,.26)'; ctx.beginPath(); ctx.arc(0,-40*sc,13*sc,Math.PI,Math.PI*2); ctx.fill();
      break;
    case 'wizard-hat':
      ctx.fillStyle='#38004e'; ctx.beginPath();
      ctx.moveTo(-13*sc,-30*sc); ctx.lineTo(0,-62*sc); ctx.lineTo(13*sc,-30*sc); ctx.closePath(); ctx.fill();
      ctx.fillRect(-15*sc,-32*sc,30*sc,5*sc);
      ctx.fillStyle='rgba(190,80,255,.48)'; ctx.beginPath(); ctx.arc(0,-60*sc,3.5*sc,0,Math.PI*2); ctx.fill();
      break;
    case 'hood':
      ctx.fillStyle='#1a1a22'; ctx.beginPath(); ctx.arc(0,-40*sc,14*sc,Math.PI,Math.PI*2); ctx.fill();
      break;
    case 'headband':
      ctx.strokeStyle='#cc2211'; ctx.lineWidth=4.5*sc;
      ctx.beginPath(); ctx.arc(0,-38*sc,14*sc,Math.PI*1.08,Math.PI*1.92); ctx.stroke();
      break;
    case 'crown':
      ctx.fillStyle='#bb7700';
      ctx.beginPath();
      ctx.moveTo(-13*sc,-40*sc); ctx.lineTo(-13*sc,-52*sc);
      ctx.lineTo(-7*sc,-46*sc); ctx.lineTo(0,-54*sc);
      ctx.lineTo(7*sc,-46*sc); ctx.lineTo(13*sc,-52*sc); ctx.lineTo(13*sc,-40*sc);
      ctx.closePath(); ctx.fill();
      break;
    case 'cap':
      ctx.fillStyle='#2a3322'; ctx.beginPath(); ctx.arc(0,-40*sc,14*sc,Math.PI,Math.PI*2); ctx.fill();
      ctx.fillRect(-16*sc,-42*sc,32*sc,7*sc);
      break;
  }
}

// ── MONSTER RENDERER ──────────────────────────────────────
const MDRAW = {
  goblin(ctx,sc,wp,ap,e){
    const lc=e.limbCol||'#22aa44';const bc=e.bodyCol||'#338855';const hc=e.headCol||'#22aa33';
    const ls=Math.sin(wp)*.5;const as=Math.sin(ap)*.7;
    for(const[ox,s]of[[-3*sc,-1],[3*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s);
      ctx.strokeStyle=lc;ctx.lineWidth=5*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,12*sc);ctx.stroke();ctx.restore();
    }
    ctx.save();ctx.translate(8*sc,-10*sc);ctx.rotate(-Math.PI/6+as);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,11*sc);ctx.stroke();
    ctx.translate(0,11*sc);ctx.rotate(.22);
    ctx.fillStyle='#aabbcc';ctx.beginPath();ctx.moveTo(-1*sc,0);ctx.lineTo(0,-13*sc);ctx.lineTo(1*sc,0);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-8*sc,-10*sc);ctx.rotate(Math.PI/6-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=4*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,11*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-8*sc,-20*sc,16*sc,20*sc,3*sc);ctx.fill();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-24*sc,10*sc,8*sc,0,0,Math.PI*2);ctx.fill();
    // Ears
    ctx.fillStyle=hc;
    ctx.beginPath();ctx.ellipse(-12*sc,-24*sc,4.5*sc,3*sc,-Math.PI/4,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(12*sc,-24*sc,4.5*sc,3*sc,Math.PI/4,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ffcc00';ctx.beginPath();ctx.arc(-3*sc,-26*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(3*sc,-26*sc,2.5*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#330000';ctx.beginPath();ctx.arc(-2*sc,-26*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-26*sc,1.2*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#fff';ctx.fillRect(-3*sc,-20*sc,2*sc,2.5*sc);ctx.fillRect(1*sc,-20*sc,2*sc,2.5*sc);
  },
  skeleton(ctx,sc,wp,ap,e){
    const ls=Math.sin(wp)*.38;const as=Math.sin(ap)*.65;const bc='#d4c8a0';const lc='#c4b888';
    for(const[ox,s]of[[-4*sc,-1],[4*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s);
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
    ctx.fillStyle='rgba(0,180,255,.6)';ctx.beginPath();ctx.arc(-4*sc,-35*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-35*sc,1.5*sc,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#111';for(let t=-3;t<=3;t++)ctx.fillRect((t*2.4-1)*sc,-24*sc,2*sc,4*sc);
  },
  orc(ctx,sc,wp,ap,e){
    const ls=Math.sin(wp)*.3;const as=Math.sin(ap)*.55;
    const bc='#3a5a2a';const lc='#2a4a1a';const hc='#4a6a3a';
    for(const[ox,s]of[[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s);
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
    ctx.fillStyle='#666';ctx.fillRect(-3*sc,0,6*sc,9*sc);
    ctx.fillStyle='#888';ctx.beginPath();ctx.moveTo(-2*sc,7*sc);ctx.lineTo(-22*sc,-9*sc);ctx.lineTo(-22*sc,13*sc);ctx.lineTo(-2*sc,23*sc);ctx.closePath();ctx.fill();
    ctx.restore();
    ctx.save();ctx.translate(-14*sc,-19*sc);ctx.rotate(Math.PI/5-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=9*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,19*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-14*sc,-35*sc,28*sc,35*sc,4*sc);ctx.fill();
    ctx.fillStyle='#445533';ctx.fillRect(-12*sc,-29*sc,24*sc,12*sc);
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-41*sc,14*sc,12*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#ddd';
    ctx.beginPath();ctx.moveTo(-6*sc,-33*sc);ctx.lineTo(-10*sc,-25*sc);ctx.lineTo(-4*sc,-33*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(6*sc,-33*sc);ctx.lineTo(10*sc,-25*sc);ctx.lineTo(4*sc,-33*sc);ctx.fill();
    ctx.fillStyle='#ff2200';ctx.beginPath();ctx.arc(-5*sc,-43*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(5*sc,-43*sc,3.5*sc,0,Math.PI*2);ctx.fill();
  },
  demon(ctx,sc,wp,ap,e){
    const ls=Math.sin(wp)*.28;const as=Math.sin(ap)*.55;
    const bc='#4a0a0a';const lc='#3a0808';const hc='#550a0a';
    for(const[ox,s]of[[-6*sc,-1],[6*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s);
      ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();
      ctx.beginPath();ctx.moveTo(0,18*sc);ctx.lineTo(2*sc,27*sc);ctx.stroke();
      ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(2*sc,27*sc,5*sc,4*sc,0,0,Math.PI*2);ctx.fill();ctx.restore();
    }
    ctx.fillStyle='rgba(80,0,0,.78)';
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(-46*sc,-57*sc);ctx.lineTo(-30*sc,-10*sc);ctx.lineTo(-5*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(0,-30*sc);ctx.lineTo(46*sc,-57*sc);ctx.lineTo(30*sc,-10*sc);ctx.lineTo(5*sc,-10*sc);ctx.closePath();ctx.fill();
    ctx.save();ctx.translate(12*sc,-21*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();
    ctx.translate(0,17*sc);ctx.rotate(.3+as*.4);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,13*sc);ctx.stroke();ctx.restore();
    ctx.save();ctx.translate(-12*sc,-21*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=lc;ctx.lineWidth=7*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,17*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.roundRect(-12*sc,-37*sc,24*sc,37*sc,4*sc);ctx.fill();
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-44*sc,13*sc,11*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#660000';
    ctx.beginPath();ctx.moveTo(-8*sc,-52*sc);ctx.lineTo(-14*sc,-70*sc);ctx.lineTo(-4*sc,-54*sc);ctx.fill();
    ctx.beginPath();ctx.moveTo(8*sc,-52*sc);ctx.lineTo(14*sc,-70*sc);ctx.lineTo(4*sc,-54*sc);ctx.fill();
    ctx.fillStyle='#ff0000';ctx.shadowColor='#ff0000';ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(-4*sc,-46*sc,3.5*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(4*sc,-46*sc,3.5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },
  golem(ctx,sc,wp,ap,e){
    const ls=Math.sin(wp)*.12;const as=Math.sin(ap)*.35;
    const bc='#6a5a4a';const lc='#7a6a5a';const hc='#8a7a6a';
    for(const[ox,s]of[[-8*sc,-1],[8*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s*.5);
      ctx.fillStyle=bc;ctx.fillRect(-6*sc,-2*sc,12*sc,22*sc);
      ctx.fillStyle=lc;ctx.fillRect(-4*sc,0,8*sc,5*sc);ctx.restore();
    }
    ctx.save();ctx.translate(18*sc,-25*sc);ctx.rotate(-Math.PI/6+as);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,22*sc);ctx.fillRect(-5*sc,22*sc,14*sc,17*sc);ctx.restore();
    ctx.save();ctx.translate(-18*sc,-25*sc);ctx.rotate(Math.PI/6-as*.5);
    ctx.fillStyle=lc;ctx.fillRect(-7*sc,-2*sc,14*sc,22*sc);ctx.fillRect(-9*sc,22*sc,14*sc,17*sc);ctx.restore();
    ctx.fillStyle=bc;ctx.fillRect(-18*sc,-43*sc,36*sc,43*sc);
    ctx.strokeStyle='rgba(0,0,0,.35)';ctx.lineWidth=2*sc;
    ctx.beginPath();ctx.moveTo(-5*sc,-39*sc);ctx.lineTo(2*sc,-19*sc);ctx.lineTo(-3*sc,-9*sc);ctx.stroke();
    ctx.fillStyle='rgba(255,160,0,.65)';ctx.shadowColor='#ff9900';ctx.shadowBlur=20;
    ctx.beginPath();ctx.arc(0,-21*sc,7*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    ctx.fillStyle=hc;ctx.fillRect(-14*sc,-62*sc,28*sc,22*sc);
    ctx.fillStyle='rgba(0,0,0,.42)';ctx.fillRect(-10*sc,-58*sc,8*sc,10*sc);ctx.fillRect(2*sc,-58*sc,8*sc,10*sc);
    ctx.fillStyle='rgba(255,190,55,.88)';ctx.shadowColor='#ffaa00';ctx.shadowBlur=14;
    ctx.beginPath();ctx.arc(-6*sc,-53*sc,3.2*sc,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.arc(6*sc,-53*sc,3.2*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  },
  dragon(ctx,sc,wp,ap,e){
    const ls=Math.sin(wp)*.22;const as=Math.sin(ap)*.48;
    const bc='#1a3a1a';const sc2='#2a5a2a';const hc='#1a4a1a';
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(15*sc,-10*sc);ctx.quadraticCurveTo(42*sc,12*sc,32*sc,-22*sc);ctx.stroke();
    ctx.lineWidth=4*sc;ctx.beginPath();ctx.moveTo(32*sc,-22*sc);ctx.lineTo(42*sc,-16*sc);ctx.stroke();
    ctx.fillStyle='rgba(28,58,28,.72)';
    ctx.beginPath();ctx.moveTo(-5*sc,-35*sc);ctx.lineTo(-42*sc,-62*sc);ctx.lineTo(-36*sc,-20*sc);ctx.lineTo(-5*sc,-15*sc);ctx.closePath();ctx.fill();
    for(const[ox,s]of[[-7*sc,-1],[7*sc,1]]){
      ctx.save();ctx.translate(ox,0);ctx.rotate(Math.PI/2+ls*s);
      ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
      ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,18*sc);ctx.stroke();ctx.restore();
    }
    ctx.save();ctx.translate(14*sc,-23*sc);ctx.rotate(-Math.PI/4+as);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();ctx.restore();
    ctx.save();ctx.translate(-14*sc,-23*sc);ctx.rotate(Math.PI/4-as*.5);
    ctx.strokeStyle=bc;ctx.lineWidth=8*sc;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,16*sc);ctx.stroke();ctx.restore();
    ctx.fillStyle=bc;ctx.beginPath();ctx.ellipse(0,-19*sc,16*sc,21*sc,0,0,Math.PI*2);ctx.fill();
    ctx.fillStyle=sc2;for(let i=0;i<3;i++)ctx.beginPath(),ctx.arc(0,(-29+i*8)*sc,6*sc,0,Math.PI*2),ctx.fill();
    ctx.fillStyle=bc;ctx.fillRect(-7*sc,-41*sc,14*sc,13*sc);
    ctx.fillStyle=hc;ctx.beginPath();ctx.ellipse(0,-49*sc,14*sc,12*sc,-.28,0,Math.PI*2);ctx.fill();
    ctx.beginPath();ctx.ellipse(8*sc,-47*sc,8*sc,5*sc,-.18,0,Math.PI*2);ctx.fill();
    if(ap>.5){ctx.fillStyle='rgba(255,160,0,.88)';ctx.shadowColor='#ff7700';ctx.shadowBlur=16;ctx.beginPath();ctx.arc(14*sc,-47*sc,5.5*sc,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
    ctx.fillStyle='#ffaa00';ctx.beginPath();ctx.ellipse(-4*sc,-53*sc,4*sc,3*sc,.28,0,Math.PI*2);ctx.fill();
    ctx.fillStyle='#220000';ctx.beginPath();ctx.ellipse(-3*sc,-53*sc,2*sc,2*sc,.28,0,Math.PI*2);ctx.fill();
  },
};

function drawMonster(e, camX, camY) {
  const x = e.x - camX, y = e.y - camY;
  if (x < -150 || x > W()+150) return;
  const dead = !e.alive;
  const sc = e.drawScale || 1;
  ctx.save(); ctx.translate(x+e.w/2, y+e.h*.9);
  if (dead) { ctx.globalAlpha=.25; ctx.rotate(e.f*Math.PI/2); }
  if (e.f===1) ctx.scale(-1,1);
  if (e.hitFlash>0) ctx.filter=`brightness(${2.8-e.hitFlash*.12})`;
  if (e.frozen>0)   ctx.filter='hue-rotate(195deg) brightness(1.9) saturate(2.3)';

  const fn = MDRAW[e.drawType] || MDRAW.goblin;
  fn(ctx, sc, e.walkPhase||0, e.atkPhase||0, e);

  ctx.filter='none'; ctx.restore();

  // HP bar
  if (!dead && e.hp < e.maxHp) {
    const pct = Math.max(0, e.hp/e.maxHp);
    const bw = Math.max(40, e.w+10), bx = x+e.w/2-bw/2, by = y-13;
    ctx.fillStyle='rgba(0,0,0,.7)'; ctx.fillRect(bx,by,bw,7);
    ctx.fillStyle = pct>.5 ? '#22cc22' : pct>.25 ? '#ccaa00' : '#cc2200';
    ctx.fillRect(bx,by,bw*pct,7);
    if (e.frozen>0) { ctx.fillStyle='rgba(80,170,255,.42)'; ctx.fillRect(bx,by,bw,7); }
    if (e.poison>0) { ctx.fillStyle='#44ff44'; ctx.beginPath(); ctx.arc(bx+bw+5,by+3,3,0,Math.PI*2); ctx.fill(); }
    if (e.cursed>0) { ctx.fillStyle='#aa44ff'; ctx.beginPath(); ctx.arc(bx+bw+12,by+3,3,0,Math.PI*2); ctx.fill(); }
    // Stun stars
    if (e.stun>40) {
      for (let i=0;i<3;i++) {
        const a=G.timer*.12+i*Math.PI*2/3;
        ctx.font='12px serif'; ctx.textAlign='center';
        ctx.fillText('⭐',x+e.w/2+Math.cos(a)*12,by-8);
      }
    }
  }

  // Superarmor / guard flash
  if (e.superArmor && e.alive) {
    ctx.strokeStyle='rgba(255,200,0,.5)'; ctx.lineWidth=2;
    ctx.strokeRect(x,y,e.w,e.h);
  }
}

// ── CHARACTER CLASSES ────────────────────────────────────
const CLASSES = {
  warrior:{
    name:'워리어',role:'근접 전사',icon:'⚔️',
    skin:'#f5c090',hair:'#1a0800',torso:'#3a4455',legs:'#2a3344',
    headDeco:'helm',weapon:'sword',offhand:'shield',
    hp:400,mp:80,atk:44,def:18,spd:4.6,jmp:14,
    desc:'높은 HP·DEF. 방패로 피해 감소.',col:'#5588cc',
    skills:[
      {name:'검격',icon:'⚔️',key:'A',mp:8,cd:1.2,desc:'강베기 2배+넉백',col:'#aabbcc',
       fn(p,G){
         const d=dmg(p,2.0);
         hitAOE(p.x+(p.f>0?p.w:-88),p.y-18,90,70,d,true,{kb:18});
         addFx('slash',p.x+(p.f>0?p.w+25:-25)-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#aabbcc',ang:p.f>0?0:Math.PI,sc:1,t:0,maxLife:18});
         addFx('hit',p.x+(p.f>0?p.w+40:-40)-G.cam,p.y+p.h/2-G.camY,{life:12,col:'#ccddff',ang:Math.random()*Math.PI*2,sc:1,t:0,maxLife:12});
         shake(5,12);
       }},
      {name:'방패 돌진',icon:'🛡️',key:'S',mp:20,cd:4.5,desc:'돌진+스턴+1.8배',col:'#8899aa',
       fn(p,G){
         p.vx=p.f*28;p.invincible=35;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-90),p.y-8,90,65,dmg(p,1.8),true,{stun:140,kb:10});
           addFx('wave',p.x+(p.f>0?p.w+30:-30)-G.cam,p.y+p.h/2-G.camY,{life:22,col:'#8899cc',sc:.8,t:0,maxLife:22});
           addFx('shockwave',p.x+(p.f>0?p.w+30:-30)-G.cam,GY()-G.camY,{life:18,col:'#aabbff',sc:1,t:0,maxLife:18});
           shake(6,14);
         },140);
       }},
      {name:'폭풍 베기',icon:'🌀',key:'D',mp:30,cd:5.5,desc:'360도 광역 1.9배',col:'#99aabb',
       fn(p,G){
         const cx=p.x+p.w/2,cy=p.y+p.h/2;
         hitAOE(cx-85,cy-55,170,110,dmg(p,1.9),false,{kb:14});
         for(let i=0;i<8;i++){
           const a=i/8*Math.PI*2;
           addFx('beam',cx-G.cam,cy-G.camY,{life:16,col:'#aabbff',ang:a,len:88,sc:1,t:0,maxLife:16});
         }
         addFx('wave',cx-G.cam,cy-G.camY,{life:25,col:'#99bbff',sc:1.5,t:0,maxLife:25});
         shake(7,18);
       }},
      {name:'블레이드 스톰',icon:'💥',key:'F',mp:55,cd:10,desc:'5연타 총 8배+대넉백',col:'#ccdde0',
       fn(p,G){
         for(let i=0;i<5;i++) setTimeout(()=>{
           const d=dmg(p,1.6);
           hitAOE(p.x+(p.f>0?p.w-10:-100),p.y-25,120,90,d,i===4,{kb:i===4?28:8});
           addFx('slash',p.x+(p.f>0?p.w+18+i*8:-18-i*8)-G.cam,p.y+p.h/2-G.camY,
             {life:14,col:'#cceeff',ang:p.f>0?-.2+i*.08:.2-i*.08,sc:1+i*.08,t:0,maxLife:14});
           if(i===4) shake(12,30);
         },i*90);
       }},
      {name:'무적 참격',icon:'🗡️',key:'G',mp:72,cd:18,desc:'5초무적+자힐+4배',col:'#eeffff',
       fn(p,G){
         p.invincible=300;p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.22));
         hitAOE(p.x-70,p.y-60,p.w+148,130,dmg(p,4),true,{kb:22,stun:200});
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:45,col:'#eeffff',sc:2.2,t:0,maxLife:45});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:35,col:['#eeffff','#aaddff','#fff'],glow:true,sMin:2,sMax:9,type:'star',spin:true});
         shake(14,35);
       }},
    ]
  },
  mage:{
    name:'마법사',role:'원소 마법사',icon:'🔮',
    skin:'#c07840',hair:'#1a0800',torso:'#331155',legs:'#220f44',
    headDeco:'wizard-hat',weapon:'staff',offhand:'tome',
    hp:215,mp:300,atk:68,def:5,spd:4.0,jmp:13.5,
    desc:'폭발적 마법 데미지. MP 관리 필수.',col:'#aa44ff',
    skills:[
      {name:'파이어볼',icon:'🔥',key:'A',mp:16,cd:1.4,desc:'화염탄 3발 연사',col:'#ff6600',
       fn(p,G){
         for(let i=0;i<3;i++) setTimeout(()=>{
           sproj(p.x+p.f*55,p.y+22,p.f*17,(Math.random()-.5)*.7,dmg(p,1.8),'#ff6600','player',
             {sz:14,emoji:'🔥',life:65,trail:true,
              onHit(e){addFx('explosion',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:22,col:'#ff6600',col2:'#ff3300',sc:.9,t:0,maxLife:22});}
             });
         },i*100);
       }},
      {name:'아이스 스피어',icon:'❄️',key:'S',mp:28,cd:4,desc:'빙결 마법구',col:'#44aaff',
       fn(p,G){
         sproj(p.x+p.f*55,p.y+20,p.f*16,0,dmg(p,2.6),'#44aaff','player',
           {sz:16,emoji:'❄️',life:75,
            onHit(e){e.frozen=Math.max(e.frozen||0,220);addFx('iceburst',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:32,sc:1.3,t:0,maxLife:32});}
           });
       }},
      {name:'체인 라이트닝',icon:'⚡',key:'D',mp:38,cd:5.5,desc:'낙뢰 4연격',col:'#ffee00',
       fn(p,G){
         for(let i=0;i<4;i++) setTimeout(()=>{
           const tx=(p.x+p.f*(160+i*95)-G.cam);
           const ty=p.y+p.h/2-G.camY;
           addFx('lightning',tx+G.cam,ty+G.camY,{life:22,sc:1,t:0,maxLife:22});
           setTimeout(()=>{
             hitAOE(G.cam+tx-35,ty+G.camY-220,70,240,dmg(p,2.4),true,{stun:80,kb:12});
             addFx('shockwave',tx,ty,{life:18,col:'#ffee00',sc:.8+i*.15,t:0,maxLife:18});
             spawnParts(tx,ty,{n:12,col:['#ffee00','#ffdd44'],glow:true,spread:.5,dir:Math.PI/2,sMin:3,sMax:10});
           },70);
         },i*185);
       }},
      {name:'메테오',icon:'☄️',key:'F',mp:78,cd:14,desc:'운석 6발 낙하 4배',col:'#ff4400',
       fn(p,G){
         for(let i=0;i<6;i++) setTimeout(()=>{
           const tx=p.x+p.f*80+(Math.random()-.5)*340;
           sproj(tx,-80,(Math.random()-.5)*2.8,20,dmg(p,4),'#ff4400','player',
             {sz:24,emoji:'☄️',life:78,grav:.42,
              onHit(e){
                addFx('explosion',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:32,col:'#ff4400',col2:'#ffaa00',sc:1.6,t:0,maxLife:32});
                shake(5,11);
              }
             });
         },i*170);
       }},
      {name:'타임스탑',icon:'⏰',key:'G',mp:95,cd:24,desc:'4초 전체 빙결+광역',col:'#8844ff',
       fn(p,G){
         freezeAll(260);
         hitAll(dmg(p,2.8),true,{kb:0});
         addFx('darkwave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:55,sc:2.8,t:0,maxLife:55});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#8844ff',sc:3,t:0,maxLife:40});
         shake(12,30);
       }},
    ]
  },
  rogue:{
    name:'로그',role:'암살자',icon:'🗝️',
    skin:'#e8a870',hair:'#1a0800',torso:'#1a2a1a',legs:'#111a11',
    headDeco:'hood',weapon:'dual',offhand:'dagger',
    hp:255,mp:200,atk:58,def:8,spd:6.2,jmp:17,
    desc:'초고속 이동. 크리+25%. 연속 참격.',col:'#22cc55',
    skills:[
      {name:'5연참',icon:'🗡️',key:'A',mp:10,cd:1.0,desc:'초속 5연타',col:'#44ee66',
       fn(p,G){
         for(let i=0;i<5;i++) setTimeout(()=>{
           const d=dmg(p,1.55);
           hitAOE(p.x+(p.f>0?p.w:-75),p.y-12,77,65,d,i===4&&Math.random()<.4,{kb:i===4?14:4});
           addFx('slash',p.x+(p.f>0?p.w+14:-14)-G.cam,p.y+p.h/2-G.camY,
             {life:11,col:'#44ee88',ang:p.f>0?-.22+i*.05:.22-i*.05,sc:.85,t:0,maxLife:11});
           addFx('hit',p.x+(p.f>0?p.w+30:-30)-G.cam,p.y+p.h/2-G.camY,
             {life:9,col:'#88ff88',ang:Math.random()*Math.PI*2,sc:.7,t:0,maxLife:9});
         },i*88);
       }},
      {name:'수리검',icon:'✴️',key:'S',mp:22,cd:3,desc:'4방향 수리검 연사',col:'#aaffaa',
       fn(p,G){
         [-7,-2,2,7].forEach(vy=>sproj(p.x+p.f*55,p.y+28,p.f*20,vy,dmg(p,1.7),'#22dd44','player',{sz:10,emoji:'✴️',life:72}));
       }},
      {name:'잔상 이동',icon:'💨',key:'D',mp:18,cd:3.5,desc:'텔레포트+폭풍 참',col:'#aa44cc',
       fn(p,G){
         // Ghost trail
         for(let i=1;i<=4;i++) {
           const gx=p.x+p.w/2-G.cam, gy2=p.y+p.h/2-G.camY;
           spawnParts(gx,gy2,{n:8,col:['#22cc44','#88ff88'],grav:0,sMin:2,sMax:6,spread:.8,dMin:.04,dMax:.06});
         }
         p.x+=p.f*210;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-105),p.y-25,110,88,dmg(p,3.0),true,{kb:20,stun:100});
           addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:22,col:'#22cc44',sc:1.3,t:0,maxLife:22});
           addFx('shockwave',p.x+p.w/2-G.cam,GY()-G.camY,{life:18,col:'#22cc44',sc:1.2,t:0,maxLife:18});
           shake(8,18);
         },80);
       }},
      {name:'독 단검',icon:'☠️',key:'F',mp:36,cd:7.5,desc:'독 지속피해+2배',col:'#44cc44',
       fn(p,G){
         sproj(p.x+p.f*55,p.y+26,p.f*19,-1.5,dmg(p,2.0),'#44cc44','player',
           {sz:13,emoji:'🗡️',life:85,
            onHit(e){
              e.poison=Math.max(e.poison||0,340);e.poisonDmg=Math.round(p.atk*.44);
              addFx('wave',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:30,col:'#44cc44',sc:1.3,t:0,maxLife:30});
              spawnParts(e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{n:12,col:['#44cc44','#88ff88'],glow:true,sMin:2,sMax:6,upb:2});
            }
           });
       }},
      {name:'죽음의 무도',icon:'💀',key:'G',mp:84,cd:20,desc:'8방향 폭격+6초무적',col:'#112233',
       fn(p,G){
         p.invincible=360;
         for(let i=0;i<8;i++){
           const a=i/8*Math.PI*2;
           setTimeout(()=>{
             hitAOE(p.x+Math.cos(a)*95-55,p.y+Math.sin(a)*70-35,110,88,dmg(p,3.8),true,{kb:22});
             addFx('slash',p.x+Math.cos(a)*95-G.cam,p.y+Math.sin(a)*70-G.camY,
               {life:20,col:'#22cc44',ang:a,sc:1.4,t:0,maxLife:20});
           },i*55);
         }
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:35,col:'#22cc44',sc:2,t:0,maxLife:35});
         shake(16,42);
       }},
    ]
  },
  berserker:{
    name:'버서커',role:'광전사',icon:'💢',
    skin:'#e8a070',hair:'#440000',torso:'#4a1010',legs:'#3a0808',
    headDeco:'headband',weapon:'axe',offhand:'shield',
    hp:350,mp:60,atk:68,def:10,spd:5.2,jmp:14,
    desc:'ATK 극대화. HP↓ = ATK↑↑↑',col:'#ff3322',
    skills:[
      {name:'분노 강타',icon:'💢',key:'A',mp:0,cd:1.8,desc:'광란 강타 HP-8',col:'#ff4422',
       fn(p,G){
         const rage=1+(1-p.hp/p.maxHp)*1.4;
         const d=dmg(p,1.9*rage);p.hp=Math.max(1,p.hp-8);
         hitAOE(p.x+(p.f>0?p.w:-92),p.y-14,94,76,d,true,{kb:20});
         addFx('explosion',p.x+(p.f>0?p.w+32:-32)-G.cam,p.y+p.h/2-G.camY,{life:20,col:'#ff4422',col2:'#ff9900',sc:.95,t:0,maxLife:20});
         addFx('shockwave',p.x+(p.f>0?p.w+32:-32)-G.cam,GY()-G.camY,{life:16,col:'#ff4422',sc:1,t:0,maxLife:16});
         shake(6,14);
       }},
      {name:'피의 갈망',icon:'🩸',key:'S',mp:0,cd:5,desc:'1.8배 흡혈 55%',col:'#cc0000',
       fn(p,G){
         const d=dmg(p,1.8);
         hitAOE(p.x+(p.f>0?p.w:-92),p.y-14,94,74,d,false,{lifeSteal:.55,kb:12});
         addFx('beam',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#cc0000',ang:p.f>0?0:Math.PI,len:130,sc:1,t:0,maxLife:18});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:14,col:['#ff0000','#cc0000'],glow:true,upb:3,sMin:2,sMax:6});
       }},
      {name:'광란',icon:'🌋',key:'D',mp:22,cd:8,desc:'ATK+70% 5초 HP-22',col:'#ff8800',
       fn(p,G){
         p.hp=Math.max(1,p.hp-22);
         p.buffAtk=(p.buffAtk||1)*1.7;p.buffTimer=Math.max(p.buffTimer||0,300);
         addFx('firepillar',p.x+p.w/2-G.cam,GY()-G.camY,{life:38,sc:1.4,t:0,maxLife:38});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:28,col:['#ff4400','#ffaa00'],glow:true,sMin:3,sMax:10,type:'star',spin:true,upb:2});
         shake(7,18);
       }},
      {name:'대지 강타',icon:'💥',key:'F',mp:44,cd:9.5,desc:'지면 충격파 3.5배',col:'#cc2200',
       fn(p,G){
         p.vy=-4;
         setTimeout(()=>{
           hitAOE(p.x-100,p.y-10,220,GY()-p.y+50,dmg(p,3.5),true,{kb:25,stun:130});
           addFx('explosion',p.x+(p.f>0?70:-70)-G.cam,GY()-G.camY,{life:35,col:'#ff4422',col2:'#ffaa00',sc:2.2,t:0,maxLife:35});
           for(let i=0;i<5;i++) addFx('shockwave',(p.x+p.f*(50+i*55))-G.cam,GY()-G.camY,{life:18+i*4,col:'#ff8800',sc:.5+i*.25,t:0,maxLife:18+i*4});
           shake(14,38);sfx_ground();
         },280);
       }},
      {name:'최후의 일격',icon:'🏴',key:'G',mp:0,cd:14,desc:'HP낮을수록 최대14배',col:'#0a0000',
       fn(p,G){
         const mult=4+(1-p.hp/p.maxHp)*10;
         hitAOE(p.x+(p.f>0?p.w-10:-138),p.y-60,178,136,dmg(p,mult),true,{kb:32,stun:250});
         addFx('explosion',p.x+(p.f>0?p.w+55:-55)-G.cam,p.y+p.h/2-G.camY,{life:45,col:'#ff2200',col2:'#ff9900',sc:2.8,t:0,maxLife:45});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:30,col:'#ff4400',sc:2.5,t:0,maxLife:30});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:50,col:['#ff2200','#ffcc00','#fff'],glow:true,sMin:4,sMax:14,type:'star',spin:true});
         shake(20,55);
       }},
    ]
  },
  paladin:{
    name:'팔라딘',role:'성기사',icon:'✨',
    skin:'#f5c090',hair:'#ffd080',torso:'#44556a',legs:'#334455',
    headDeco:'helm',weapon:'hammer',offhand:'shield',
    hp:560,mp:120,atk:37,def:30,spd:3.8,jmp:12,
    desc:'최고 생존력. 힐+재생+신성 폭발.',col:'#eeddaa',
    skills:[
      {name:'망치 강타',icon:'🔨',key:'A',mp:12,cd:2,desc:'망치 2배+스턴+넉백',col:'#ccd0d4',
       fn(p,G){
         hitAOE(p.x+(p.f>0?p.w:-96),p.y-14,96,74,dmg(p,2.0),false,{stun:120,kb:14});
         addFx('wave',p.x+(p.f>0?p.w+32:-32)-G.cam,p.y+p.h/2-G.camY,{life:20,col:'#ccd0d4',sc:.75,t:0,maxLife:20});
         addFx('shockwave',p.x+(p.f>0?p.w+32:-32)-G.cam,GY()-G.camY,{life:16,col:'#ccd0d4',sc:.9,t:0,maxLife:16});
         shake(5,11);
       }},
      {name:'신성 치유',icon:'💛',key:'S',mp:22,cd:4,desc:'HP 32% 회복',col:'#ffffaa',
       fn(p,G){
         const h=Math.round(p.maxHp*.32);p.hp=Math.min(p.maxHp,p.hp+h);
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:40,col:'#ffffaa',sc:1.6,t:0,maxLife:40});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:26,col:['#ffff88','#ffffff'],glow:true,upb:4,sMin:2,sMax:9,type:'star'});
       }},
      {name:'신성화',icon:'🔆',key:'D',mp:38,cd:7.5,desc:'전체 신성 폭발 1.6배',col:'#ffff88',
       fn(p,G){
         hitAll(dmg(p,1.6),true,{kb:16,stun:80});
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:50,col:'#ffffaa',sc:2.5,t:0,maxLife:50});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:35,col:'#ffffaa',sc:2,t:0,maxLife:35});
         shake(6,14);
       }},
      {name:'신성 방패',icon:'🌟',key:'F',mp:42,cd:9.5,desc:'4초 무적+재생',col:'#aaddff',
       fn(p,G){
         p.invincible=245;p.regenTimer=(p.regenTimer||0)+180;
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:35,col:'#aaddff',sc:1.9,t:0,maxLife:35});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:28,col:'#ffffff',sc:1.6,t:0,maxLife:28});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:32,col:['#aaddff','#ffffff'],glow:true,sMin:3,sMax:10,grav:-.015,spread:.8});
       }},
      {name:'성광 폭발',icon:'💥',key:'G',mp:82,cd:18,desc:'전체 3배+자힐 45%',col:'#ffffcc',
       fn(p,G){
         hitAll(dmg(p,3),true,{kb:24,stun:160});
         p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.45));
         addFx('explosion',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:44,col:'#ffffcc',col2:'#ffdd88',sc:2.8,t:0,maxLife:44});
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:38,col:'#ffffcc',sc:2.4,t:0,maxLife:38});
         shake(12,28);
       }},
    ]
  },
  necromancer:{
    name:'네크로맨서',role:'소환사',icon:'💀',
    skin:'#c0c8d0',hair:'#000000',torso:'#121820',legs:'#0a1018',
    headDeco:'crown',weapon:'scythe',offhand:'tome',
    hp:234,mp:270,atk:62,def:6,spd:4.2,jmp:13.5,
    desc:'암흑·저주. 죽음의 폭발로 대학살.',col:'#8833cc',
    skills:[
      {name:'암흑탄',icon:'💜',key:'A',mp:14,cd:1.8,desc:'암흑 2.2배+저주',col:'#8833cc',
       fn(p,G){
         sproj(p.x+p.f*55,p.y+24,p.f*16,-1,dmg(p,2.2),'#8833cc','player',
           {sz:15,emoji:'🔮',life:70,
            onHit(e){
              e.cursed=Math.max(e.cursed||0,200);
              addFx('darkwave',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:26,sc:.95,t:0,maxLife:26});
            }
           });
       }},
      {name:'생명 흡수',icon:'🖤',key:'S',mp:26,cd:4.5,desc:'흡혈+자힐 28',col:'#440088',
       fn(p,G){
         sproj(p.x+p.f*55,p.y+24,p.f*14,-1,dmg(p,1.65),'#440088','player',
           {sz:13,emoji:'🖤',life:65,
            onHit(e){
              p.hp=Math.min(p.maxHp,p.hp+28);
              addFx('beam',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:20,col:'#440088',ang:Math.random()*Math.PI*2,len:65,sc:1,t:0,maxLife:20});
              spawnParts(e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{n:10,col:['#440088','#880044'],glow:true,upb:3,sMin:2,sMax:6});
            }
           });
       }},
      {name:'저주의 낫',icon:'⛧',key:'D',mp:32,cd:6,desc:'전체 ATK-42% 저주',col:'#332244',
       fn(p,G){
         for(const e of G.enemies) if(e.alive) e.cursed=Math.max(e.cursed||0,260);
         if(G.boss&&G.boss.alive) G.boss.cursed=Math.max(G.boss.cursed||0,260);
         addFx('darkwave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:45,sc:2.2,t:0,maxLife:45});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:35,col:'#8833cc',sc:2,t:0,maxLife:35});
       }},
      {name:'뼈 돌풍',icon:'🦴',key:'F',mp:52,cd:11,desc:'전체 광역 3배',col:'#ccbbaa',
       fn(p,G){
         hitAll(dmg(p,3.0),true,{kb:18,stun:100});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:32,col:'#ccbbaa',sc:2.2,t:0,maxLife:32});
         addFx('darkwave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:28,sc:1.8,t:0,maxLife:28});
         shake(8,18);
       }},
      {name:'죽음 폭발',icon:'☠️',key:'G',mp:96,cd:22,desc:'전체 6배 암흑 폭발',col:'#110022',
       fn(p,G){
         hitAll(dmg(p,6.0),true,{kb:30,stun:300});
         addFx('explosion',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:55,col:'#8833cc',col2:'#110022',sc:3.2,t:0,maxLife:55});
         addFx('darkwave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:50,sc:3.5,t:0,maxLife:50});
         for(let i=0;i<14;i++) setTimeout(()=>addFx('darkwave',Math.random()*W()+G.cam,Math.random()*(H()-62)+G.camY,{life:28,sc:.7+Math.random()*.6,t:0,maxLife:28}),i*40);
         shake(22,60);
       }},
    ]
  },
  monk:{
    name:'몽크',role:'격투가',icon:'🥊',
    skin:'#f5c090',hair:'#000000',torso:'#cc8833',legs:'#aa6622',
    headDeco:'headband',weapon:'dual',offhand:'dagger',
    hp:310,mp:155,atk:48,def:13,spd:6.5,jmp:17.5,
    desc:'초고속 연타. 기(氣) 폭발 특화.',col:'#ffaa22',
    skills:[
      {name:'7연타',icon:'🥊',key:'A',mp:8,cd:1.0,desc:'7연속 고속 타격',col:'#ffaa22',
       fn(p,G){
         for(let i=0;i<7;i++) setTimeout(()=>{
           const d=dmg(p,.75);
           hitAOE(p.x+(p.f>0?p.w:-70),p.y-12,73,65,d,i===6,{kb:i===6?16:3});
           addFx('hit',p.x+(p.f>0?p.w+22:-22)-G.cam,p.y+p.h/2-G.camY,
             {life:9,col:'#ffaa22',ang:Math.random()*Math.PI*2,sc:.75,t:0,maxLife:9});
           if(i===6) addFx('explosion',p.x+(p.f>0?p.w+28:-28)-G.cam,p.y+p.h/2-G.camY,{life:18,col:'#ffaa22',col2:'#ff8800',sc:.8,t:0,maxLife:18});
         },i*80);
       }},
      {name:'기공파',icon:'🌀',key:'S',mp:22,cd:3,desc:'기 에너지파 2.8배',col:'#ffcc44',
       fn(p,G){
         sproj(p.x+p.f*55,p.y+24,p.f*18,0,dmg(p,2.8),'#ffcc44','player',
           {sz:18,emoji:'🌀',life:75,
            onHit(e){
              addFx('wave',e.x+e.w/2-G.cam,e.y+e.h/2-G.camY,{life:22,col:'#ffcc44',sc:1.2,t:0,maxLife:22});
              addFx('shockwave',e.x+e.w/2-G.cam,GY()-G.camY,{life:16,col:'#ffcc44',sc:1,t:0,maxLife:16});
            }
           });
       }},
      {name:'기천보',icon:'⚡',key:'D',mp:16,cd:3.5,desc:'초고속 순간이동+베기',col:'#88aaff',
       fn(p,G){
         for(let i=0;i<5;i++) spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:6,col:['#ffcc44','#fff'],grav:0,sMin:2,sMax:5,spread:.6});
         p.x+=p.f*225;p.invincible=30;
         setTimeout(()=>{
           hitAOE(p.x+(p.f>0?p.w:-108),p.y-28,115,95,dmg(p,3.2),true,{kb:22,stun:90});
           addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:22,col:'#ffcc44',sc:1.3,t:0,maxLife:22});
           shake(8,18);
         },75);
       }},
      {name:'회오리 발차기',icon:'🌪️',key:'F',mp:36,cd:7,desc:'360도 4배',col:'#88ccff',
       fn(p,G){
         const cx=p.x+p.w/2,cy=p.y+p.h/2;
         hitAOE(cx-92,cy-60,184,120,dmg(p,4),true,{kb:20});
         for(let i=0;i<8;i++){
           const a=i/8*Math.PI*2;
           addFx('beam',cx-G.cam,cy-G.camY,{life:18,col:'#88ccff',ang:a,len:105,sc:1,t:0,maxLife:18});
         }
         addFx('wave',cx-G.cam,cy-G.camY,{life:26,col:'#88ccff',sc:1.6,t:0,maxLife:26});
         shake(8,18);
       }},
      {name:'내공 폭발',icon:'☮️',key:'G',mp:0,cd:11,desc:'HP+55% MP+35 회복',col:'#ffffcc',
       fn(p,G){
         p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.55));
         p.mp=Math.min(p.maxMp,p.mp+35);
         addFx('holy',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:44,col:'#ffffcc',sc:1.7,t:0,maxLife:44});
         addFx('wave',p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{life:30,col:'#ffcc88',sc:1.4,t:0,maxLife:30});
         spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,{n:28,col:['#ffffcc','#fff'],glow:true,upb:3.5,sMin:2,sMax:7,type:'star'});
       }},
    ]
  },
};

// ── ENEMY TYPES ──────────────────────────────────────────
const ENEMIES = {
  goblin:   {name:'고블린',  drawType:'goblin',  w:34,h:40, hp:80,  atk:11,spd:3.4,xp:14,g:8,  bodyCol:'#33aa44',headCol:'#22aa33',limbCol:'#22aa44',drawScale:.95,ai:'chase'},
  orc:      {name:'오크',    drawType:'orc',     w:52,h:62, hp:220, atk:26,spd:2.0,xp:30,g:18, bodyCol:'#3a5a2a',headCol:'#4a6a3a',limbCol:'#2a4a1a',drawScale:1.3,ai:'brute'},
  skeleton: {name:'스켈레톤',drawType:'skeleton',w:38,h:52, hp:118, atk:17,spd:3.3,xp:22,g:14, bodyCol:'#d4c8a0',headCol:'#d4c8a0',limbCol:'#c4b888',drawScale:1.0,ai:'normal'},
  mage_e:   {name:'마법사',  drawType:'goblin',  w:36,h:52, hp:105, atk:28,spd:2.6,xp:34,g:24, bodyCol:'#2a1a4a',headCol:'#3a2a6a',limbCol:'#3a2a5a',drawScale:.9, ai:'ranged'},
  demon:    {name:'데몬',    drawType:'demon',   w:48,h:66, hp:195, atk:27,spd:2.9,xp:48,g:32, bodyCol:'#4a0a0a',headCol:'#550a0a',limbCol:'#3a0808',drawScale:1.1,ai:'chase'},
  dragon:   {name:'드래고니언',drawType:'dragon',w:60,h:72, hp:280, atk:32,spd:2.4,xp:58,g:40, bodyCol:'#1a3a1a',headCol:'#1a4a1a',limbCol:'#2a5a2a',drawScale:1.3,ai:'brute'},
  golem:    {name:'골렘',    drawType:'golem',   w:68,h:76, hp:420, atk:36,spd:1.4,xp:70,g:50, bodyCol:'#6a5a4a',headCol:'#8a7a6a',limbCol:'#7a6a5a',drawScale:1.4,ai:'tank',superArmor:true},
};

// ── STAGES ───────────────────────────────────────────────
const STAGES=[
  {name:'어둠의 동굴',  bg:'#05030d',fl:'#0e0618',wall:'#0a0412',torch:'#ff6600',
   enemySet:['goblin','skeleton'],count:8,
   boss:{name:'슬라임 대왕',drawType:'golem',hp:980,atk:28,spd:2.4,bodyCol:'#226622',headCol:'#337733',limbCol:'#115511',drawScale:1.7}},
  {name:'용암 던전',    bg:'#110300',fl:'#200800',wall:'#180400',torch:'#ff4400',
   enemySet:['goblin','orc','demon'],count:10,
   boss:{name:'화염 골렘',drawType:'golem',hp:1500,atk:38,spd:2.2,bodyCol:'#662200',headCol:'#883300',limbCol:'#441100',drawScale:1.8}},
  {name:'얼음 궁전',    bg:'#030718',fl:'#071028',wall:'#050c1a',torch:'#44aaff',
   enemySet:['orc','skeleton','mage_e'],count:12,
   boss:{name:'빙결 드래곤',drawType:'dragon',hp:2000,atk:46,spd:2.8,bodyCol:'#224466',headCol:'#336688',limbCol:'#112244',drawScale:1.6}},
  {name:'독 늪지',      bg:'#030c03',fl:'#071007',wall:'#050d05',torch:'#44cc00',
   enemySet:['demon','mage_e','dragon'],count:14,
   boss:{name:'늪 히드라',drawType:'dragon',hp:2700,atk:54,spd:3.1,bodyCol:'#225522',headCol:'#337733',limbCol:'#113311',drawScale:1.7}},
  {name:'마왕의 성',    bg:'#07000e',fl:'#110016',wall:'#0c0012',torch:'#aa00ff',
   enemySet:['demon','dragon','golem'],count:16,
   boss:{name:'마왕 DARKOS',drawType:'golem',hp:3700,atk:72,spd:3.4,bodyCol:'#220033',headCol:'#330055',limbCol:'#110022',drawScale:2.1}},
];

// ── SHOP ─────────────────────────────────────────────────
const SHOP_ITEMS=[
  {name:'HP 포션 소',icon:'🧪',desc:'HP +25%', price:60,  fn(p){const h=Math.round(p.maxHp*.25);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'HP 포션 대',icon:'⚗️', desc:'HP +60%', price:170, fn(p){const h=Math.round(p.maxHp*.6);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {name:'마나 포션', icon:'💙', desc:'MP +55%', price:88,  fn(p){const m=Math.round(p.maxMp*.55);p.mp=Math.min(p.maxMp,p.mp+m);return `MP +${m}`;}},
  {name:'강화 검',   icon:'⚔️', desc:'ATK +22', price:220, fn(p){p.atkBonus=(p.atkBonus||0)+22;return 'ATK +22';},rarity:1},
  {name:'불꽃 검',   icon:'🔥', desc:'ATK +42', price:400, fn(p){p.atkBonus=(p.atkBonus||0)+42;return 'ATK +42';},rarity:2},
  {name:'강화 갑옷', icon:'🛡️', desc:'DEF+15 HP+50',price:238,fn(p){p.defBonus=(p.defBonus||0)+15;p.maxHp+=50;p.hp=Math.min(p.maxHp,p.hp+50);return 'DEF+15 HP+50';},rarity:1},
  {name:'마법 갑옷', icon:'💎', desc:'DEF+26 HP+90',price:430,fn(p){p.defBonus=(p.defBonus||0)+26;p.maxHp+=90;p.hp=Math.min(p.maxHp,p.hp+90);return 'DEF+26 HP+90';},rarity:2},
  {name:'스피드 링', icon:'💍', desc:'SPD +1.4',price:195, fn(p){p.spdBonus=(p.spdBonus||0)+1.4;return 'SPD +1.4';},rarity:1},
  {name:'크리 반지',  icon:'🔮', desc:'CRIT+22%',price:320, fn(p){p.critBonus=(p.critBonus||0)+.22;return 'CRIT+22%';},rarity:2},
  {name:'전설 반지',  icon:'⭐', desc:'ATK+30 CRIT+30%',price:700,fn(p){p.atkBonus=(p.atkBonus||0)+30;p.critBonus=(p.critBonus||0)+.3;return 'ATK+30 CRIT+30%';},rarity:4},
];
const RARITY_COL=['#aaaaaa','#44cc44','#4488ff','#cc44ff','#ffcc00'];
const STAGE_W=3600;

// ── GAME STATE ───────────────────────────────────────────
let G=null,selCls=null;
const GRAV=0.52;

function mkPlayer(clsId){
  const c=CLASSES[clsId];
  return {
    ...c,clsId,
    x:140,y:GY()-68,vx:0,vy:0,f:1,
    onGround:false,jumpCount:0,
    hp:c.hp,maxHp:c.hp,mp:c.mp,maxMp:c.mp,
    alive:true,invincible:0,
    skillCds:c.skills.map(()=>0),
    buffAtk:1,buffSpd:1,buffTimer:0,
    kills:0,score:0,gold:0,level:1,xp:0,xpNext:100,
    combo:0,comboTimer:0,maxCombo:0,
    atkCd:0,atkAnim:0,hitFlash:0,
    dodgeCd:0,dodgeAnim:0,dodgeTrail:[],
    w:44,h:65,walkPhase:0,atkPhase:0,
    atkBonus:0,defBonus:0,spdBonus:0,critBonus:0,
    defBuff:0,defBuffTimer:0,regenTimer:0,
    equip:{wpn:null,arm:null,acc:null},
    // DNF specific
    superArmor:0,      // frames of super armor
    hitstop:0,         // frozen frames on hit
    airCombo:0,        // air combo count
    upAttack:false,
    downAttack:false,
  };
}

function initGame(clsId,stageIdx){
  const p=mkPlayer(clsId);
  const stage=STAGES[stageIdx];
  G={
    clsId,stageIdx,stage,
    player:p,
    enemies:[],boss:null,bossSpawned:false,
    projectiles:[],items:[],
    cam:0,camY:0,
    phase:'play',timer:0,
    startTime:Date.now(),
    shakeAmt:0,shakeTimer:0,
    hitStop:0,
    stageDmgTaken:0,
    paused:false,
    pendingLvlUp:false,
    maxCombo:0,
    shopStock:[],
  };
  PARTS.length=0;FX.length=0;
  spawnEnemies();
  updateEquipUI();
}

function spawnEnemies(){
  const st=G.stage;
  for(let i=0;i<st.count;i++){
    const tid=st.enemySet[Math.floor(Math.random()*st.enemySet.length)];
    const et={...ENEMIES[tid]};
    const sc=1+G.stageIdx*.22;
    G.enemies.push({
      ...et,uid:'e'+i,
      x:580+i*240+Math.random()*80,y:GY()-et.h,
      hp:Math.round(et.hp*sc),maxHp:Math.round(et.hp*sc),
      atk:Math.round(et.atk*sc),
      vx:0,vy:0,f:-1,alive:true,dying:false,deathTimer:0,
      atkTimer:60+Math.random()*70,
      frozen:0,stun:0,poison:0,poisonDmg:0,poisonTimer:0,cursed:0,
      hitFlash:0,walkPhase:Math.random()*Math.PI*2,atkPhase:0,aggro:false,
      knockbackTimer:0,
    });
  }
}

function spawnBoss(){
  const bd=G.stage.boss;
  const sc=1+G.stageIdx*.28;
  G.boss={
    ...ENEMIES[bd.drawType]||ENEMIES.golem,
    ...bd,
    x:STAGE_W-550,y:GY()-95,
    hp:Math.round(bd.hp*sc),maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc),spd:bd.spd+G.stageIdx*.07,
    w:82,h:98,alive:true,dying:false,
    frozen:0,stun:0,cursed:0,
    atkTimer:68,projTimer:88,
    phase2:false,phase3:false,
    hitFlash:0,walkPhase:0,atkPhase:0,
    knockbackTimer:0,vx:0,vy:0,
  };
  document.getElementById('boss-bar').classList.add('show');
  document.getElementById('boss-name-txt').textContent='⚠ '+bd.name;
  const bw=document.getElementById('boss-warn');
  bw.style.display='block';bw.textContent='⚠ BOSS ⚠\n'+bd.name;
  setTimeout(()=>bw.style.display='none',2600);
  shake(16,55);sfx_bossIn();
}

// ── COMBAT CORE ──────────────────────────────────────────
function totalAtk(p){return (p.atk+(p.atkBonus||0))*(p.buffAtk||1);}
function totalDef(p){return (p.def+(p.defBonus||0))+(p.defBuff||0);}
function totalCrit(p){return .1+(p.critBonus||0)+(p.clsId==='rogue'?.25:0);}
function totalSpd(p){return (p.spd+(p.spdBonus||0))*(p.buffSpd||1);}

function dmg(p,mult){
  const atk=totalAtk(p);
  const isCrit=Math.random()<totalCrit(p);
  const v=Math.round((atk*mult+Math.random()*8-4)*(isCrit?2.15:1));
  return {v:Math.max(1,v),crit:isCrit};
}

function hitAOE(ax,ay,aw,ah,d,showCrit,opts={}){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  let hitAny=false;
  for(const e of targets){
    if(!e.alive) continue;
    if(ax<e.x+e.w&&ax+aw>e.x&&ay<e.y+e.h&&ay+ah>e.y){
      // Super armor: reduce knockback but still take damage
      const kbMult=(e.superArmor||e.stun>0)?0.2:1;
      dealDmg(e,d.v,d.crit||showCrit,{...opts,kb:(opts.kb||0)*kbMult});
      hitAny=true;
    }
  }
  return hitAny;
}

function hitAll(d,showCrit,opts={}){
  if(!G) return;
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  for(const e of targets) if(e.alive) dealDmg(e,d.v,d.crit||showCrit,opts);
}

function dealDmg(e,v,crit,opts){
  if(!e.alive) return;
  const p=G.player;
  if(e.cursed>0) v=Math.round(v*1.44);
  e.hp-=v;e.hitFlash=10;
  if(opts.stun&&!(e.superArmor)) e.stun=Math.max(e.stun||0,opts.stun);
  if(opts.kb&&opts.kb>0){
    // DNF style knockback — big and satisfying
    e.vx=(e.f>0?-1:1)*opts.kb;
    e.vy=-opts.kb*.45;
    e.knockbackTimer=Math.round(opts.kb*1.2);
  }
  if(opts.lifeSteal) p.hp=Math.min(p.maxHp,p.hp+Math.round(v*opts.lifeSteal));
  if(opts.onHit) opts.onHit(e);

  const sx=e.x-G.cam+e.w/2, sy=e.y-G.camY;
  showDNum(sx,sy,v,crit,p.col||'#fff');

  // Hit stop: freeze both attacker and target briefly for impact feel
  if(crit) G.hitStop=7;
  else if(v>80) G.hitStop=4;
  else G.hitStop=Math.max(G.hitStop,2);

  if(crit){
    document.getElementById('crit-vfx').style.animation='none';
    document.getElementById('crit-vfx').offsetHeight;
    document.getElementById('crit-vfx').style.animation='crit-burst .42s ease';
  }
  if(e.hp<=0) killE(e);
  else {
    // Hitstun: enemy briefly can't attack
    e.atkTimer=Math.max(e.atkTimer,38);
  }
}

function killE(e){
  e.alive=false;e.dying=true;e.deathTimer=32;
  const p=G.player;
  if(e===G.boss){
    p.xp+=800;p.gold+=500;p.score+=10000;
    document.getElementById('boss-bar').classList.remove('show');
    spawnParts(e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,
      {n:80,col:['#ffcc00','#ff6600','#fff','#ff4400'],glow:true,sMin:3,sMax:16,type:'star',spin:true});
    addFx('explosion',e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,{life:55,col:'#ffcc00',col2:'#ff4400',sc:3,t:0,maxLife:55});
    shake(22,75);sfx_clear();checkLvlUp(p);
    setTimeout(()=>stageClear(),1400);
  } else {
    p.kills++;p.xp+=e.xp;p.gold+=e.g;p.score+=e.xp*2;
    // Death burst
    spawnParts(e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,
      {n:22,col:[e.bodyCol||'#556','#ffcc00','#fff'],sMin:2,sMax:7,glow:true,upb:1});
    addFx('explosion',e.x-G.cam+e.w/2,e.y-G.camY+e.h/2,{life:22,col:e.bodyCol||'#556',col2:'#ffcc00',sc:.8,t:0,maxLife:22});
    checkLvlUp(p);
    tryDrop(e);
  }
}

function checkLvlUp(p){
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext;p.level++;p.xpNext=Math.round(p.xpNext*1.52);
    p.maxHp+=34;p.hp=Math.min(p.maxHp,p.hp+55);
    p.maxMp+=13;p.mp=Math.min(p.maxMp,p.mp+24);
    p.atk+=4;p.def+=2;
    G.pendingLvlUp=true;showLvlUpModal();sfx_lvl();
  }
}

function tryDrop(e){
  if(Math.random()>.42) return;
  const it={...SHOP_ITEMS[Math.floor(Math.random()*SHOP_ITEMS.length)],uid:'d'+Date.now(),x:e.x+e.w/2-14,y:e.y,vy:-8,alive:true};
  G.items.push(it);
}

function freezeAll(dur){
  if(!G) return;
  for(const e of G.enemies) if(e.alive) e.frozen=Math.max(e.frozen||0,dur);
  if(G.boss&&G.boss.alive) G.boss.frozen=Math.max(G.boss.frozen||0,dur);
}

function sproj(x,y,vx,vy,d,col,owner,opts={}){
  if(!G) return;
  G.projectiles.push({
    x,y,vx,vy,dmg:d.v,crit:d.crit,col,owner,alive:true,
    life:opts.life||80,sz:opts.sz||8,
    grav:opts.grav!==undefined?opts.grav:0,
    emoji:opts.emoji||null,trail:!!opts.trail,
    onHit:opts.onHit||null,pierce:!!opts.pierce,
  });
}

function shake(amt,dur){
  if(!G) return;
  G.shakeAmt=Math.max(G.shakeAmt,amt);G.shakeTimer=Math.max(G.shakeTimer,dur);
}

// ── MAIN LOOP ────────────────────────────────────────────
let lastTs=0;
function loop(ts){
  const dt=Math.min((ts-lastTs)/16.67,3);lastTs=ts;
  if(G&&G.phase==='play'&&!G.paused&&!G.pendingLvlUp) gameUpdate(dt);
  gameRender();updateHUD();flushJust();
  requestAnimationFrame(loop);
}

function gameUpdate(dt){
  G.timer++;
  const p=G.player;
  if(!p.alive) return;

  // Global hit stop — freeze everything
  if(G.hitStop>0){G.hitStop-=dt;return;}

  handleInput(p,dt);
  updatePlayer(p,dt);
  updateEnemies(dt);
  if(G.boss&&G.boss.alive) updateBoss(dt);
  updateProjs(dt);
  updateItems(dt);
  tickParts(dt);
  tickFx(dt);

  if(G.shakeTimer>0) G.shakeTimer-=dt;
  if(G.timer%75===0) p.mp=Math.min(p.maxMp,p.mp+3);
  if(p.defBuffTimer>0){p.defBuffTimer-=dt;if(p.defBuffTimer<=0) p.defBuff=0;}
  if(p.buffTimer>0){p.buffTimer-=dt;if(p.buffTimer<=0){p.buffAtk=1;p.buffSpd=1;}}
  if(p.regenTimer>0){
    p.regenTimer-=dt;
    if(G.timer%18===0) p.hp=Math.min(p.maxHp,p.hp+Math.ceil(p.maxHp*.012));
  }
  if(p.superArmor>0) p.superArmor-=dt;

  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){
    G.bossSpawned=true;spawnBoss();
  }

  // Camera
  const tx=p.x-W()*.35;
  G.cam+=(tx-G.cam)*.12*dt;
  G.cam=Math.max(0,Math.min(STAGE_W-W(),G.cam));
}

function handleInput(p,dt){
  if(!p.alive) return;
  const spd=totalSpd(p);

  if(KEY['ArrowLeft']){p.vx=-spd*6*dt;p.f=-1;}
  if(KEY['ArrowRight']){p.vx=spd*6*dt;p.f=1;}

  // Jump — 2x
  if((JUST['z']||JUST['Z'])&&p.jumpCount<2){
    p.vy=-(p.jmp||14);p.jumpCount++;
    spawnParts(p.x+p.w/2-G.cam,p.y+p.h-G.camY,
      {n:11,col:['#fff','#ccc'],upb:3,sMin:2,sMax:5,spread:.88});
    sfx_jump();
  }

  // Attack — normal / up / down
  if((JUST['x']||JUST['X'])&&p.atkCd<=0){
    if(KEY['ArrowUp']) doAttack(p,'up');
    else if(KEY['ArrowDown']&&!p.onGround) doAttack(p,'down');
    else doAttack(p,'normal');
  }

  // Dodge — i-frames + dash
  if(JUST[' ']&&p.dodgeCd<=0){
    p.vx=p.f*28;p.vy=p.onGround?-1.5:-2;
    p.invincible=48;p.dodgeCd=58;p.dodgeAnim=26;
    p.dodgeTrail=[];
    for(let i=0;i<5;i++) p.dodgeTrail.push({x:p.x,y:p.y,a:1-i*.18});
    spawnParts(p.x+p.w/2-G.cam,p.y+p.h/2-G.camY,
      {n:18,col:[p.col||'#fff','rgba(255,255,255,.35)'],spread:Math.PI*.55,dir:Math.PI,sMin:2,sMax:6,grav:.04});
    sfx_dodge();
  }

  // Skills
  const skMap={a:0,s:1,d:2,f:3,g:4,A:0,S:1,D:2,F:3,G:4};
  for(const[k,idx] of Object.entries(skMap)){
    if(JUST[k]&&p.skills[idx]!==undefined){useSkill(p,idx);break;}
  }

  if(JUST['p']||JUST['P']){
    G.paused=!G.paused;
    document.getElementById('pause-ov').classList.toggle('hidden',!G.paused);
  }
}

function doAttack(p,type){
  p.atkCd=12;p.atkAnim=14;p.atkPhase=Math.PI*.55;
  p.combo=Math.min(16,(p.combo||0)+1);p.comboTimer=92;
  if(p.combo>G.maxCombo) G.maxCombo=p.combo;

  // Combo display
  const cd=document.getElementById('combo');
  cd.classList.remove('hidden');
  document.getElementById('combo-n').textContent=p.combo+'HIT';
  cd.classList.remove('pop');void cd.offsetWidth;cd.classList.add('pop');
  setTimeout(()=>cd.classList.remove('pop'),80);

  const comboMult=1+p.combo*.09;

  if(type==='up'){
    // Uppercut — launches enemy
    const d=dmg(p,comboMult*1.6);
    hitAOE(p.x+(p.f>0?p.w-10:-90),p.y-60,100,100,d,false,{kb:0,stun:60,launcher:true});
    for(const e of [...G.enemies,G.boss].filter(Boolean)){
      if(e&&e.alive&&Math.abs(e.x+e.w/2-(p.x+p.w/2))<100&&Math.abs(e.y-p.y)<100){
        e.vy=-14;// launch up
      }
    }
    addFx('slash',p.x+p.w/2-G.cam,p.y-30-G.camY,{life:14,col:p.col||'#ffcc00',ang:-Math.PI/2,sc:1,t:0,maxLife:14});
    p.vy=-4;// small hop
  } else if(type==='down'){
    // Smash down
    p.vy=12;
    const d=dmg(p,comboMult*1.8);
    setTimeout(()=>{
      hitAOE(p.x-20,p.y+p.h-10,p.w+40,30,d,true,{kb:22,stun:100});
      addFx('shockwave',p.x+p.w/2-G.cam,GY()-G.camY,{life:20,col:'#ffcc00',sc:1.5,t:0,maxLife:20});
      addFx('explosion',p.x+p.w/2-G.cam,GY()-G.camY,{life:22,col:'#ffaa00',col2:'#ff6600',sc:1.1,t:0,maxLife:22});
      shake(6,14);sfx_ground();
    },120);
  } else {
    // Normal attack
    const d=dmg(p,comboMult);
    hitAOE(p.x+(p.f>0?p.w:-72),p.y-15,75,66,d,false,{kb:7+Math.floor(p.combo/3)*3});
    spawnParts(p.x+(p.f>0?p.w+24:-34)-G.cam,p.y+24-G.camY,
      {n:d.crit?18:9,col:[p.col||'#fff','#ffcc00'],spread:.7,dir:p.f>0?0:Math.PI,
       sMin:2,sMax:d.crit?10:5.5,glow:d.crit,upb:d.crit?.5:0});
    if(d.crit){
      shake(3,7);
      addFx('slash',p.x+(p.f>0?p.w+18:-18)-G.cam,p.y+p.h/2-G.camY,
        {life:14,col:p.col||'#fff',ang:p.f>0?-.18:.18,sc:1.15,t:0,maxLife:14});
      addFx('hit',p.x+(p.f>0?p.w+35:-35)-G.cam,p.y+p.h/2-G.camY,
        {life:10,col:'#ffee44',ang:Math.random()*Math.PI*2,sc:1,t:0,maxLife:10});
    } else if(p.combo>=4){
      addFx('hit',p.x+(p.f>0?p.w+25:-25)-G.cam,p.y+p.h/2-G.camY,
        {life:9,col:p.col||'#fff',ang:Math.random()*Math.PI*2,sc:.8,t:0,maxLife:9});
    }
  }
}

function useSkill(p,idx){
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;p.skillCds[idx]=sk.cd*60;p.atkPhase=Math.PI;
  p.superArmor=60;// skills grant super armor
  sk.fn(p,G);
  sfx_skill();
}

function updatePlayer(p,dt){
  if(!p.onGround||p.dodgeAnim>0) {
    p.vy+=GRAV*dt;
  }
  p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vx*=(p.onGround?.8:.92);

  // Ground
  if(p.y+p.h>=GY()){p.y=GY()-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;}
  else p.onGround=false;
  if(p.y<-80){p.y=-80;p.vy=0;}
  p.x=Math.max(5,Math.min(STAGE_W-p.w-5,p.x));

  if(Math.abs(p.vx)>.5&&p.onGround) p.walkPhase+=.26*dt*Math.abs(p.vx)*.034;
  else if(p.onGround) p.walkPhase=Math.round(p.walkPhase/Math.PI)*Math.PI;

  p.atkPhase=Math.max(0,p.atkPhase-.15*dt);
  if(p.invincible>0) p.invincible-=dt;
  if(p.atkCd>0) p.atkCd-=dt;
  if(p.atkAnim>0) p.atkAnim-=dt;
  if(p.hitFlash>0) p.hitFlash-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeAnim>0) p.dodgeAnim-=dt;
  if(p.comboTimer>0){
    p.comboTimer-=dt;
    if(p.comboTimer<=0){
      p.combo=0;
      document.getElementById('combo').classList.add('hidden');
    }
  }
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;
  if(p.clsId==='paladin'&&G.timer%95===0) p.hp=Math.min(p.maxHp,p.hp+Math.ceil(p.maxHp*.015));
}

function updateEnemies(dt){
  const p=G.player;
  for(const e of G.enemies){
    if(!e.alive){if(e.dying) e.deathTimer-=dt;continue;}
    if(e.hitFlash>0) e.hitFlash-=dt;
    if(e.frozen>0){e.frozen-=dt;e.walkPhase=0;continue;}
    if(e.stun>0){e.stun-=dt;continue;}
    if(e.cursed>0) e.cursed-=dt;

    // Knockback physics
    if(e.knockbackTimer>0){
      e.knockbackTimer-=dt;
      e.x+=e.vx*dt;e.y+=e.vy*dt;
      e.vy+=GRAV*dt*.7;
      e.vx*=.88;
      if(e.y+e.h>=GY()){e.y=GY()-e.h;e.vy=0;}
      e.x=Math.max(10,Math.min(STAGE_W-e.w-10,e.x));
      continue;
    }

    if(e.poison>0){
      e.poison-=dt;
      if(!e.poisonTimer||e.poisonTimer<=0){
        e.hp-=e.poisonDmg||5;e.poisonTimer=22;
        if(e.hp<=0){killE(e);continue;}
      }
      e.poisonTimer-=dt;
    }

    const dx=p.x-e.x;
    const dist=Math.abs(dx);
    if(dist<520) e.aggro=true;
    if(!e.aggro) continue;

    e.f=dx>0?1:-1;
    const sm=e.cursed>0?.55:1;
    const spd=(e.spd||2)*sm;

    switch(e.ai){
      case 'chase':  if(dist>52) e.x+=e.f*spd*dt;break;
      case 'brute':  if(dist>58) e.x+=e.f*spd*.88*dt;break;
      case 'slow':   if(dist>62) e.x+=e.f*spd*.6*dt;break;
      case 'tank':   if(dist>68) e.x+=e.f*spd*.5*dt;break;
      case 'ranged':
        if(dist<185) e.x-=e.f*spd*.62*dt;
        else if(dist>310) e.x+=e.f*spd*.62*dt;
        break;
      default: if(dist>52) e.x+=e.f*spd*dt;break;
    }

    // Gravity
    e.vy=(e.vy||0)+GRAV*dt*.52;
    e.y+=e.vy*dt;
    if(e.y+e.h>=GY()){e.y=GY()-e.h;e.vy=0;}
    e.x=Math.max(10,Math.min(STAGE_W-e.w-10,e.x));
    e.walkPhase+=.19*dt;
    e.atkPhase=Math.max(0,e.atkPhase-.12*dt);
    e.atkTimer-=dt;

    if(e.atkTimer<=0&&e.aggro){
      if(e.ai==='ranged'){
        if(dist<400){
          e.atkTimer=95+Math.random()*50;
          const vd=dmg({atk:e.atk,atkBonus:0,buffAtk:1,critBonus:0},1);
          sproj(e.x+e.w/2,e.y+e.h*.38,e.f*11.5+(Math.random()-.5)*1,(Math.random()-.5)*2.5,vd,'#aa44ff','enemy',{sz:10,life:85});
          e.atkPhase=Math.PI*.85;
        }
      } else {
        if(dist<66&&Math.abs(p.y-e.y)<70){
          e.atkTimer=72+Math.random()*36;e.atkPhase=Math.PI;
          if(p.invincible<=0&&p.dodgeAnim<=0){
            const rawDmg=Math.max(1,e.atk-Math.round(totalDef(p)*.5)+Math.floor(Math.random()*7)-3);
            takeDmg(rawDmg,e);
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

  if(b.knockbackTimer>0){
    b.knockbackTimer-=dt;
    b.x+=b.vx*dt;b.y+=(b.vy||0)*dt;
    b.vy=(b.vy||0)+GRAV*dt*.4;
    b.vx*=.9;
    if(b.y+b.h>=GY()){b.y=GY()-b.h;b.vy=0;}
    b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));
  }

  const hpPct=b.hp/b.maxHp;
  if(!b.phase2&&hpPct<.55){
    b.phase2=true;b.spd*=1.38;b.atk=Math.round(b.atk*1.3);
    document.getElementById('boss-phase-lbl').textContent='⚡ PHASE 2';
    shake(15,50);
    addFx('explosion',b.x-G.cam+b.w/2,b.y-G.camY+b.h/2,{life:44,col:'#ff4400',col2:'#ffcc00',sc:2.2,t:0,maxLife:44});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true;b.spd*=1.3;b.atk=Math.round(b.atk*1.25);
    document.getElementById('boss-phase-lbl').textContent='💀 ENRAGE!';
    shake(24,80);
    addFx('explosion',b.x-G.cam+b.w/2,b.y-G.camY+b.h/2,{life:58,col:'#ff0000',col2:'#aa0000',sc:3.2,t:0,maxLife:58});
    sfx_bossIn();
  }

  const dx=p.x-b.x;
  b.f=dx>0?1:-1;
  if(Math.abs(dx)>105&&b.knockbackTimer<=0) b.x+=b.f*b.spd*dt*.92;
  b.vy=(b.vy||0)+GRAV*dt*.42;
  b.y+=(b.vy||0)*dt;
  if(b.y+b.h>=GY()){b.y=GY()-b.h;b.vy=0;}
  b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));
  b.walkPhase+=.12*dt;b.atkPhase=Math.max(0,b.atkPhase-.1*dt);
  b.atkTimer-=dt;b.projTimer-=dt;

  const pInt=b.phase3?40:b.phase2?62:92;
  if(b.projTimer<=0){
    b.projTimer=pInt;b.atkPhase=Math.PI*.82;
    const bv=dmg({atk:b.atk,atkBonus:0,buffAtk:1,critBonus:0},b.phase3?.8:.65);
    if(b.phase3){
      for(let i=-1;i<=1;i++) sproj(b.x+b.w/2,b.y+b.h*.36,b.f*11,i*5,bv,'#ff2200','enemy',{sz:17,emoji:'💥',life:92,grav:.1});
    } else {
      sproj(b.x+b.w/2,b.y+b.h*.36,b.f*9.5,-1.5,bv,'#ff4400','enemy',{sz:17,emoji:'💥',life:92,grav:.1});
    }
  }

  if(b.atkTimer<=0&&Math.abs(dx)<110&&b.knockbackTimer<=0){
    b.atkTimer=b.phase3?36:b.phase2?50:70;b.atkPhase=Math.PI;
    if(Math.abs(p.y-b.y)<105&&p.invincible<=0&&p.dodgeAnim<=0){
      const raw=Math.max(1,b.atk-Math.round(totalDef(p)*.4)+Math.floor(Math.random()*15)-7);
      takeDmg(raw,b);
      if(b.phase3) setTimeout(()=>{if(G&&p.hp>0) takeDmg(Math.round(raw*.75),b);},230);
    }
  }
  document.getElementById('boss-hp-inner').style.width=Math.max(0,(b.hp/b.maxHp)*100)+'%';
}

function takeDmg(v,src){
  const p=G.player;
  if(p.invincible>0||p.superArmor>0) return;
  p.hp-=v;p.hitFlash=16;p.invincible=42;G.stageDmgTaken+=v;
  G.hitStop=3;
  const fl=document.getElementById('hit-vfx');
  fl.style.background='rgba(255,20,20,.45)';fl.style.opacity='1';
  fl.style.transition='opacity .12s';setTimeout(()=>fl.style.opacity='0',130);
  // Knockback player slightly
  if(src) p.vx=(p.x>src.x?1:-1)*8;
  shake(6,14);
  if(p.hp<=0) gameOver();
}

function updateProjs(dt){
  const p=G.player;
  const gy=GY()+30;
  G.projectiles=G.projectiles.filter(pr=>{
    if(!pr.alive) return false;
    pr.x+=pr.vx*dt;pr.y+=pr.vy*dt;pr.vy+=pr.grav*dt;pr.life-=dt;
    if(pr.life<=0) return false;
    if(pr.trail) spawnParts(pr.x-G.cam,pr.y-G.camY,{n:2,col:[pr.col],sMin:1,sMax:3,grav:0,dMax:.07,spread:.35});
    if(pr.y>gy+100) return false;
    if(pr.owner==='player'){
      const targets=[...G.enemies];if(G.boss&&G.boss.alive) targets.push(G.boss);
      for(const e of targets){
        if(!e.alive) continue;
        if(pr.x>e.x&&pr.x<e.x+e.w&&pr.y>e.y&&pr.y<e.y+e.h){
          const d={v:pr.dmg,crit:pr.crit};
          dealDmg(e,d.v,d.crit,{onHit:pr.onHit,kb:8});
          spawnParts(pr.x-G.cam,pr.y-G.camY,{n:11,col:[pr.col,'#fff'],sMin:2,sMax:6,glow:!!pr.emoji});
          if(!pr.pierce){pr.alive=false;return false;}
        }
      }
    } else {
      if(p.invincible<=0&&p.dodgeAnim<=0){
        const px=pr.x-G.cam,py=pr.y-G.camY,ppx=p.x-G.cam,ppy=p.y-G.camY;
        if(px>ppx&&px<ppx+p.w&&py>ppy&&py<ppy+p.h){
          takeDmg(Math.max(1,pr.dmg-Math.round(totalDef(p)*.36)));pr.alive=false;return false;
        }
      }
    }
    return true;
  });
}

function updateItems(dt){
  const p=G.player;
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAV*dt*.66;it.y+=it.vy*dt;
    if(it.y+20>=GY()){it.y=GY()-20;it.vy=0;}
    const sx=it.x-G.cam,sy=it.y-G.camY,px=p.x-G.cam,py=p.y-G.camY;
    if(sx>px-35&&sx<px+p.w+35&&sy>py-14&&sy<py+p.h+24){
      showDNum(sx,sy,'✦ '+it.fn(p),false,'#ffcc00');it.alive=false;return false;
    }
    return true;
  });
}

// ── RENDER ───────────────────────────────────────────────
function gameRender(){
  if(!G){
    ctx.fillStyle='#04020a';ctx.fillRect(0,0,W(),H());
    tickParts(1);drawParts(0,0);
    return;
  }
  ctx.save();
  if(G.shakeTimer>0){
    const s=G.shakeAmt*(G.shakeTimer/24)*.5;
    ctx.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }
  const st=G.stage;
  ctx.fillStyle=st.bg;ctx.fillRect(0,0,W(),H());

  drawBackground(st);
  drawGround(st);
  drawParts(G.cam,G.camY);
  drawFx(G.cam,G.camY);
  drawProjs();
  drawItems();
  drawAllEnemies();
  if(G.boss&&(G.boss.alive||G.boss.dying)) drawMonster(G.boss,G.cam,0);
  drawPlayerChar();
  ctx.restore();

  drawMinimap();
}

function drawBackground(st){
  // Parallax background layers
  const cx=G.cam;
  // Subtle dungeon pillars in BG
  ctx.save();ctx.globalAlpha=.06;
  const pillarSpacing=180;
  for(let px=-(cx*.2)%pillarSpacing-pillarSpacing;px<W()+pillarSpacing;px+=pillarSpacing){
    ctx.fillStyle='#888';
    ctx.fillRect(px,0,22,GY());
    ctx.fillRect(px+22,0,W()-22,8);// "ceiling"
  }
  ctx.restore();
  // Torch particles
  if(G.timer%8===0){
    for(let i=0;i<4;i++){
      const tx=((i+.5)*W()*.25)+G.cam*.04-((cx*.04)%pillarSpacing);
      spawnParts(tx,GY()-22,{n:1,col:[st.torch||'#ff6600'],glow:true,sMin:1,sMax:2.5,upb:2.8,grav:-.03,dMax:.045,spread:.32});
    }
  }
  // Distance foggy wall tint
  ctx.save();ctx.globalAlpha=.03;
  ctx.fillStyle='#fff';ctx.fillRect(0,0,W(),H()*.15);
  ctx.restore();
}

function drawGround(st){
  const gy=GY();
  // Main floor
  ctx.fillStyle=st.fl;ctx.fillRect(0,gy,W(),H()-gy);
  // Floor line — DNF style bright edge
  const grd=ctx.createLinearGradient(0,gy,0,gy+6);
  grd.addColorStop(0,'rgba(255,200,80,.45)');grd.addColorStop(1,'transparent');
  ctx.fillStyle=grd;ctx.fillRect(0,gy,W(),6);
  // Shadow under floor
  ctx.fillStyle='rgba(0,0,0,.28)';ctx.fillRect(0,gy+5,W(),5);
  // Floor tile lines
  ctx.strokeStyle='rgba(255,255,255,.03)';ctx.lineWidth=1;
  for(let x=(-G.cam%80);x<W();x+=80){
    ctx.beginPath();ctx.moveTo(x,gy);ctx.lineTo(x,gy+18);ctx.stroke();
  }
}

function drawPlayerChar(){
  const p=G.player;
  const px=p.x-G.cam,py=p.y;
  if(p.invincible>0&&Math.floor(G.timer/3)%2===0) return;

  // Dodge trail
  if(p.dodgeAnim>0&&p.dodgeTrail){
    for(let i=0;i<p.dodgeTrail.length;i++){
      const t=p.dodgeTrail[i];
      ctx.save();ctx.globalAlpha=(p.dodgeAnim/26)*t.a*.32;
      drawChar({x:t.x-G.cam,y:t.y+p.h,f:p.f,wp:p.walkPhase,ap:0,hitFlash:0,dead:false,...p,sc:.92,dodging:true});
      ctx.restore();
    }
    // Slide trail forward
    p.dodgeTrail.unshift({x:p.x,y:p.y,a:1});
    if(p.dodgeTrail.length>6) p.dodgeTrail.pop();
  }

  // Super armor glow
  if(p.superArmor>0){
    ctx.save();ctx.globalAlpha=Math.min(.5,p.superArmor/60*.5);
    ctx.fillStyle=p.col||'#fff';
    ctx.shadowColor=p.col||'#fff';ctx.shadowBlur=18;
    ctx.beginPath();ctx.arc(px+p.w/2,py+p.h/2-G.camY,38,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;ctx.restore();
  }

  ctx.save();
  drawChar({x:px,y:py+p.h-G.camY,f:p.f,wp:p.walkPhase,ap:p.atkPhase,hitFlash:p.hitFlash,dead:!p.alive,...p,sc:1,skillGlow:p.buffAtk>1?p.col:null});
  // Shadow
  ctx.globalAlpha=.22;ctx.fillStyle='#000';
  ctx.beginPath();ctx.ellipse(px+p.w/2,GY()-G.camY+5,p.w*.46,5,0,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

function drawAllEnemies(){
  for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const ex=e.x-G.cam;
    if(ex<-140||ex>W()+140) continue;
    const alpha=e.dying?(e.deathTimer/32):1;
    ctx.save();ctx.globalAlpha=alpha;
    drawMonster(e,G.cam,0);
    ctx.restore();
  }
}

function drawProjs(){
  ctx.save();
  for(const pr of G.projectiles){
    const px=pr.x-G.cam,py=pr.y;
    if(px<-40||px>W()+40) continue;
    if(pr.emoji){
      ctx.font=`${pr.sz*1.85}px serif`;ctx.textAlign='center';ctx.textBaseline='middle';
      ctx.fillText(pr.emoji,px,py);
    } else {
      ctx.fillStyle=pr.col;ctx.shadowColor=pr.col;ctx.shadowBlur=12;
      ctx.beginPath();ctx.arc(px,py,pr.sz,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    }
  }
  ctx.restore();
}

function drawItems(){
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam,iy=it.y;
    if(ix<-40||ix>W()+40) continue;
    ctx.save();
    ctx.shadowColor=RARITY_COL[it.rarity||0];ctx.shadowBlur=14;
    const bob=Math.sin(G.timer*.09+it.x*.01)*3.5;
    ctx.font='24px serif';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.fillText(it.icon,ix,iy+bob);ctx.shadowBlur=0;ctx.restore();
  }
}

function drawMinimap(){
  if(!G) return;
  const mc=document.getElementById('mm');const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,128,30);
  const sc=128/STAGE_W;const p=G.player;
  for(const e of G.enemies){
    if(!e.alive) continue;
    mctx.fillStyle=e.bodyCol||'#f44';mctx.fillRect(e.x*sc,12,3,3);
  }
  if(G.boss&&G.boss.alive){mctx.fillStyle='#f00';mctx.fillRect(G.boss.x*sc-1,9,5,5);}
  mctx.fillStyle='#0fa';mctx.fillRect(p.x*sc-2,10,4,5);
  mctx.strokeStyle='rgba(245,197,24,.35)';mctx.lineWidth=1;
  mctx.strokeRect(G.cam*sc,1,W()*sc,28);
}

// ── HUD ──────────────────────────────────────────────────
function updateHUD(){
  if(!G) return;
  const p=G.player;
  const hp=Math.max(0,p.hp),mp=Math.max(0,p.mp);
  document.getElementById('hp-fill').style.width=Math.max(0,(hp/p.maxHp)*100)+'%';
  document.getElementById('mp-fill').style.width=Math.max(0,(mp/p.maxMp)*100)+'%';
  document.getElementById('hp-val').textContent=`${hp}/${p.maxHp}`;
  document.getElementById('mp-val').textContent=`${mp}/${p.maxMp}`;
  document.getElementById('xp-fill').style.width=Math.min(100,(p.xp/p.xpNext)*100)+'%';
  document.getElementById('xp-val').textContent=`${p.xp}/${p.xpNext}`;
  document.getElementById('s-lv').textContent=p.level;
  document.getElementById('s-atk').textContent=Math.round(totalAtk(p));
  document.getElementById('s-def').textContent=Math.round(totalDef(p));
  document.getElementById('s-kill').textContent=p.kills;
  document.getElementById('s-scr').textContent=p.score;
  document.getElementById('s-gld').textContent=p.gold;
  document.getElementById('hud-nm').textContent=p.name;
  document.getElementById('floor-b').textContent=`${G.stageIdx+1} STAGE`;

  let bi='';
  if(p.buffAtk>1) bi+='<span title="ATK 버프">🔥</span>';
  if(p.defBuff>0) bi+='<span title="DEF 버프">🛡️</span>';
  if(p.invincible>65) bi+='<span title="무적">⭐</span>';
  if(p.superArmor>0) bi+='<span title="슈퍼아머">💪</span>';
  document.getElementById('buff-icons').innerHTML=bi;

  // Skill bar
  const skCont=document.getElementById('sk-cont');skCont.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i];const cd=p.skillCds[i];const rdy=cd<=0&&p.mp>=sk.mp;
    const div=document.createElement('div');
    div.className='sk '+(rdy?'ready':cd>0?'cd':'');
    div.innerHTML=`<div class="sk-ico">${sk.icon}</div><span class="sk-key">${sk.key}</span><span class="sk-mp">${sk.mp}</span>`;
    if(cd>0){const t=document.createElement('div');t.className='sk-cd-txt';t.textContent=cd>60?Math.ceil(cd/60)+'s':cd.toFixed(1);div.appendChild(t);}
    div.title=`${sk.name} [${sk.key}] MP:${sk.mp} CD:${sk.cd}s — ${sk.desc}`;
    skCont.appendChild(div);
  }
  updateEquipUI();
}

function updateEquipUI(){
  if(!G) return;const p=G.player;
  ['w','a','c'].forEach((s,i)=>{
    const el=document.getElementById('eq-'+s);if(!el) return;
    el.textContent=p.equip?.[['wpn','arm','acc'][i]]?.icon||['🗡️','🛡️','💍'][i];
  });
}

// ── DAMAGE NUMBERS ───────────────────────────────────────
function showDNum(sx,sy,v,crit,col){
  const el=document.createElement('div');el.className='dnum';
  const area=document.getElementById('game-area');
  const ox=area.getBoundingClientRect().left;
  const oy=area.getBoundingClientRect().top;
  el.style.cssText=`
    left:${ox+sx-22}px;top:${oy+sy-16}px;
    font-size:${crit?'1.44':'0.92'}rem;
    color:${crit?'#ffff33':(col||'#fff')};
    ${crit?'text-shadow:0 0 18px #ffff00,1px 1px 0 #000;':''}
  `;
  el.textContent=crit?'💥'+v+'!!':v;
  document.body.appendChild(el);setTimeout(()=>el.remove(),1020);
}

// ── TRANSITIONS ──────────────────────────────────────────
function stageClear(){
  G.phase='clear';const p=G.player;
  const secs=Math.round((Date.now()-G.startTime)/1000);
  const bonus=G.stageDmgTaken===0?5500:0;p.score+=bonus;
  document.getElementById('clear-stats').innerHTML=`
    <div class="rs">처치 수<b>${p.kills}</b></div>
    <div class="rs">골드<b>💰${p.gold}</b></div>
    <div class="rs">점수<b>${p.score}</b></div>
    <div class="rs">시간<b>${secs}초</b></div>
    <div class="rs">레벨<b>Lv${p.level}</b></div>
    <div class="rs">무피해 보너스<b>${bonus?'+5500':'없음'}</b></div>`;
  document.getElementById('clear-ov').classList.remove('hidden');
}

function gameOver(){
  if(!G||G.phase!=='play') return;
  G.phase='over';G.player.alive=false;const p=G.player;
  document.getElementById('over-stats').innerHTML=`
    <div class="rs">처치 수<b>${p.kills}</b></div>
    <div class="rs">골드<b>💰${p.gold}</b></div>
    <div class="rs">점수<b>${p.score}</b></div>
    <div class="rs">레벨<b>Lv${p.level}</b></div>
    <div class="rs">스테이지<b>${G.stageIdx+1}</b></div>
    <div class="rs">최대 콤보<b>${G.maxCombo}HIT</b></div>`;
  setTimeout(()=>document.getElementById('over-ov').classList.remove('hidden'),850);
  sfx_death();
}

function openShop(){
  document.getElementById('clear-ov').classList.add('hidden');
  buildShop();document.getElementById('shop-ov').classList.remove('hidden');
}
function buildShop(){
  const p=G.player;document.getElementById('shop-gold').textContent=p.gold;
  const pool=[...SHOP_ITEMS].sort(()=>Math.random()-.5).slice(0,6);
  G.shopStock=pool.map(it=>({...it,uid:'s'+Date.now(),price:it.price+G.stageIdx*30}));
  document.getElementById('shop-grid').innerHTML=G.shopStock.map((it,i)=>{
    const cant=p.gold<it.price;
    return `<div class="sc${cant?' cant':''}" onclick="buyItem(${i})">
      <div class="sc-ico">${it.icon}</div>
      <div class="sc-nm" style="color:${RARITY_COL[it.rarity||0]}">${it.name}</div>
      <div class="sc-dc">${it.desc}</div>
      <div class="sc-pr">${it.price}💰</div></div>`;
  }).join('');
}
function buyItem(i){
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

function showLvlUpModal(){
  document.getElementById('stat-grid').innerHTML=`
    <button class="stat-btn" onclick="pickStat('hp')">❤️ 최대 HP +32</button>
    <button class="stat-btn" onclick="pickStat('atk')">⚔️ ATK +7</button>
    <button class="stat-btn" onclick="pickStat('def')">🛡️ DEF +5</button>
    <button class="stat-btn" onclick="pickStat('spd')">💨 SPD +0.6</button>
    <button class="stat-btn" onclick="pickStat('mp')">🔷 최대 MP +24</button>
    <button class="stat-btn" onclick="pickStat('crit')">⚡ 크리 +7%</button>`;
  document.getElementById('lvlup-ov').classList.remove('hidden');
}
function pickStat(stat){
  const p=G.player;
  if(stat==='hp'){p.maxHp+=32;p.hp=Math.min(p.maxHp,p.hp+32);}
  else if(stat==='atk') p.atk+=7;
  else if(stat==='def') p.def+=5;
  else if(stat==='spd') p.spd+=.6;
  else if(stat==='mp'){p.maxMp+=24;p.mp=Math.min(p.maxMp,p.mp+24);}
  else if(stat==='crit') p.critBonus=(p.critBonus||0)+.07;
  document.getElementById('lvlup-ov').classList.add('hidden');G.pendingLvlUp=false;
}

// ── TITLE SCREEN ─────────────────────────────────────────
function buildTitle(){
  const row=document.getElementById('char-grid');row.innerHTML='';
  for(const[id,c] of Object.entries(CLASSES)){
    const div=document.createElement('div');div.className='cc';div.id='cc-'+id;
    div.onclick=()=>{
      selCls=id;
      document.querySelectorAll('.cc').forEach(x=>x.classList.remove('sel'));
      div.classList.add('sel');
      document.getElementById('start-btn').disabled=false;
      ensureAudio();
    };
    div.innerHTML=`<div class="cc-ico">${c.icon}</div>
      <div class="cc-name">${c.name}</div><div class="cc-role">${c.role}</div>
      <div class="cc-desc">${c.desc}</div>`;
    row.appendChild(div);
  }
}
function startPressed(){
  if(!selCls) return;
  document.getElementById('title-ov').classList.add('hidden');
  initGame(selCls,0);
}

// ── WEB AUDIO ────────────────────────────────────────────
let AC=null;
function ensureAudio(){if(!AC)try{AC=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function osc(f,type,dur,vol=.28,del=0){
  if(!AC) return;
  try{
    const o=AC.createOscillator(),g=AC.createGain();
    o.connect(g);g.connect(AC.destination);
    o.type=type;o.frequency.value=f;
    const t=AC.currentTime+del;
    g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.005);
    g.gain.exponentialRampToValueAtTime(.001,t+dur);
    o.start(t);o.stop(t+dur+.05);
  }catch(e){}
}
const sfx_jump=()=>{ensureAudio();osc(360,'sine',.09,.12);};
const sfx_dodge=()=>{ensureAudio();osc(520,'sine',.07,.14);osc(720,'sine',.05,.1,.04);};
const sfx_lvl=()=>{ensureAudio();[550,700,850,1100].forEach((f,i)=>osc(f,'sine',.3,.32,i*.1));};
const sfx_clear=()=>{ensureAudio();[550,700,880,550,700,880,1100].forEach((f,i)=>osc(f,'sine',.28,.32,i*.1));};
const sfx_death=()=>{ensureAudio();for(let i=0;i<6;i++)osc(200-i*25,'sawtooth',.24,.26,i*.08);};
const sfx_buy=()=>{ensureAudio();osc(760,'sine',.18,.24);osc(960,'sine',.14,.18,.08);};
const sfx_bossIn=()=>{ensureAudio();for(let i=0;i<5;i++)osc(65+i*14,'sawtooth',.48,.48,i*.24);};
const sfx_skill=()=>{ensureAudio();osc(800+Math.random()*400,'sine',.06,.18);};
const sfx_ground=()=>{ensureAudio();osc(80,'sawtooth',.18,.38);osc(120,'sawtooth',.14,.28,.05);};

// ── BOOT ─────────────────────────────────────────────────
buildTitle();
requestAnimationFrame(loop);
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
    components.html(GAME_HTML, height=800, scrolling=False)

if __name__ == "__main__":
    render()
