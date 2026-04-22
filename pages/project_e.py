#pages/project_e.py
import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>던전 런: 지하 대탈출</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&family=Rajdhani:wght@600;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --gold:#f5c842;--red:#ff3355;--blue:#44aaff;--green:#22ff88;
  --purple:#cc44ff;--bg:#06040e;
}
html,body{width:100%;height:100%;overflow:hidden;background:var(--bg);font-family:'Noto Sans KR',sans-serif;}
#root{position:relative;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center;}

/* === GAME CANVAS === */
#gc{display:block;image-rendering:pixelated;}

/* === HUD OVERLAY === */
#hud{
  position:absolute;top:0;left:0;width:100%;pointer-events:none;z-index:100;
  padding:8px 12px;display:flex;align-items:center;gap:10px;
  background:linear-gradient(180deg,rgba(0,0,0,.85) 0%,transparent 100%);
}
.hud-cls{font-family:'Black Han Sans',sans-serif;font-size:.85rem;color:var(--gold);letter-spacing:2px;white-space:nowrap;}
.bar-wrap{display:flex;flex-direction:column;gap:3px;}
.bar-row{display:flex;align-items:center;gap:5px;}
.bar-lbl{font-size:.42rem;color:#777;width:16px;text-align:right;}
.bar-bg{height:11px;background:rgba(255,255,255,.07);border-radius:99px;border:1px solid rgba(255,255,255,.1);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:99px;transition:width .08s;}
#hp-fill{background:linear-gradient(90deg,#7b0000,#dd1122,#ff5566);}
#mp-fill{background:linear-gradient(90deg,#001166,#1144cc,#33aaff);}
#xp-fill{background:linear-gradient(90deg,#224400,#44aa00,#88ff44);}
.bar-txt{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.4rem;color:rgba(255,255,255,.7);font-weight:700;}
.stat-box{background:rgba(255,255,255,.05);border:1px solid rgba(245,200,66,.15);border-radius:4px;padding:1px 7px;text-align:center;min-width:38px;}
.stat-v{font-size:.8rem;font-weight:900;color:var(--gold);}
.stat-l{font-size:.37rem;color:#555;letter-spacing:.5px;}
#room-lbl{margin-left:auto;font-family:'Rajdhani',sans-serif;font-size:.9rem;font-weight:700;
  color:#fff;background:rgba(245,200,66,.1);border:1px solid rgba(245,200,66,.2);
  border-radius:3px;padding:1px 10px;letter-spacing:2px;white-space:nowrap;}
#skill-row{position:absolute;bottom:0;left:0;width:100%;pointer-events:none;z-index:100;
  display:flex;align-items:center;justify-content:center;gap:6px;padding:6px 10px;
  background:linear-gradient(0deg,rgba(0,0,0,.8) 0%,transparent 100%);}
.sk{width:48px;height:48px;border-radius:6px;background:rgba(255,255,255,.04);
  border:1px solid rgba(245,200,66,.2);display:flex;flex-direction:column;align-items:center;
  justify-content:center;position:relative;transition:border-color .1s;}
.sk.ready{border-color:rgba(245,200,66,.7);box-shadow:0 0 10px rgba(245,200,66,.25);}
.sk.cooling{opacity:.4;}
.sk-icon{font-size:1.3rem;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.36rem;color:#666;}
.sk-cd{position:absolute;inset:0;background:rgba(0,0,0,.7);border-radius:6px;
  display:flex;align-items:center;justify-content:center;font-size:.75rem;color:var(--gold);font-weight:900;}
#ctrl-hint{font-size:.4rem;color:#333;line-height:1.8;text-align:left;margin-left:8px;}

/* === MINIMAP === */
#minimap{position:absolute;top:64px;right:10px;width:120px;height:90px;
  background:rgba(0,0,0,.75);border:1px solid rgba(245,200,66,.2);border-radius:4px;
  pointer-events:none;z-index:100;overflow:hidden;}
#mm-canvas{width:120px;height:90px;}

/* === OVERLAYS === */
.ov{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
  background:rgba(6,4,14,.97);}
.ov.hidden{display:none;}

/* TITLE */
#title-ov{flex-direction:column;gap:0;}
.game-logo{font-family:'Black Han Sans',sans-serif;font-size:3.2rem;letter-spacing:6px;
  background:linear-gradient(135deg,#ff4400,#ff9900,#ffdd00);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(255,150,0,.5));margin-bottom:4px;text-align:center;}
.game-sub{font-family:'Rajdhani',sans-serif;font-size:.9rem;color:#333;letter-spacing:8px;margin-bottom:28px;text-align:center;}
.char-grid{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;justify-content:center;}
.ccard{width:130px;background:rgba(255,255,255,.02);border:1px solid rgba(245,200,66,.1);
  border-radius:10px;padding:14px 10px 12px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard:hover,.ccard.sel{border-color:rgba(245,200,66,.7);background:rgba(245,200,66,.05);
  transform:translateY(-4px);box-shadow:0 8px 30px rgba(245,200,66,.15);}
.ccard-icon{font-size:2.4rem;margin-bottom:6px;}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:.78rem;color:var(--gold);letter-spacing:2px;}
.ccard-role{font-size:.5rem;color:#444;margin-top:2px;}
.ccard-stats{display:grid;grid-template-columns:1fr 1fr;gap:3px;margin:8px 0;text-align:left;}
.cstat{font-size:.45rem;color:#555;}
.cstat b{color:#777;}
.ccard-desc{font-size:.46rem;color:#333;margin-top:4px;line-height:1.5;}
.start-btn{padding:12px 50px;background:linear-gradient(135deg,#7a2e00,#ff5500);border:none;
  border-radius:5px;color:#fff;font-family:'Black Han Sans',sans-serif;font-size:.9rem;
  letter-spacing:4px;cursor:pointer;box-shadow:0 0 24px rgba(255,100,0,.4);transition:all .2s;}
.start-btn:hover{transform:scale(1.05);filter:brightness(1.15);}
.start-btn:disabled{opacity:.25;cursor:default;transform:none;}
.tut-hint{font-size:.5rem;color:#2a2a3a;margin-top:12px;letter-spacing:1px;text-align:center;line-height:2;}

/* LEVEL UP */
#lvlup-ov{flex-direction:column;}
.lvlup-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;color:var(--gold);letter-spacing:4px;margin-bottom:8px;}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;}
.sbtn{padding:12px;border:1px solid rgba(245,200,66,.2);border-radius:6px;background:rgba(255,255,255,.04);
  cursor:pointer;font-size:.75rem;color:#aaa;font-family:'Noto Sans KR';transition:all .18s;}
.sbtn:hover{border-color:var(--gold);background:rgba(245,200,66,.07);color:var(--gold);}

/* FLOOR CLEAR */
.result-box{background:rgba(10,8,20,.98);border:1px solid rgba(245,200,66,.2);
  border-radius:12px;padding:28px 36px;min-width:340px;text-align:center;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:1.8rem;letter-spacing:4px;margin-bottom:14px;}
.clear-c{color:var(--gold);text-shadow:0 0 20px rgba(245,200,66,.5);}
.dead-c{color:var(--red);text-shadow:0 0 20px rgba(255,50,80,.5);}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin:10px 0;text-align:left;}
.res-cell{font-size:.68rem;color:#555;display:flex;justify-content:space-between;}
.res-cell b{color:var(--gold);}
.abtn{padding:9px 22px;border:none;border-radius:4px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:.78rem;letter-spacing:2px;transition:all .18s;}
.abtn:hover{transform:translateY(-2px);filter:brightness(1.15);}
.btn-next{background:linear-gradient(135deg,#1a5500,#22aa00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-gray{background:rgba(255,255,255,.07);color:#888;border:1px solid rgba(255,255,255,.1);}
.action-row{display:flex;gap:8px;justify-content:center;margin-top:14px;}

/* SHOP */
#shop-ov{flex-direction:column;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.6rem;color:var(--gold);letter-spacing:4px;margin-bottom:8px;}
.shop-grid{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:14px 0;}
.shop-card{width:120px;background:rgba(255,255,255,.03);border:1px solid rgba(245,200,66,.12);
  border-radius:8px;padding:10px 8px;cursor:pointer;transition:all .18s;text-align:center;}
.shop-card:hover:not(.sold){border-color:rgba(245,200,66,.6);background:rgba(245,200,66,.06);transform:translateY(-2px);}
.shop-card.sold{opacity:.3;cursor:default;}
.sc-icon{font-size:1.6rem;margin-bottom:5px;}
.sc-name{font-size:.62rem;color:#ccc;font-weight:700;}
.sc-desc{font-size:.5rem;color:#444;margin-top:2px;line-height:1.4;}
.sc-price{font-size:.68rem;color:var(--gold);font-weight:900;margin-top:5px;}

/* DAMAGE NUMBERS */
.dnum{position:absolute;pointer-events:none;font-family:'Black Han Sans',sans-serif;
  animation:dUp 1s ease forwards;z-index:300;text-shadow:1px 1px 3px rgba(0,0,0,.9);}
@keyframes dUp{0%{opacity:1;transform:translateY(0);}100%{opacity:0;transform:translateY(-60px) scale(.8);}}

/* BOSS WARN */
#boss-warn{position:absolute;top:45%;left:50%;transform:translate(-50%,-50%);
  font-family:'Black Han Sans',sans-serif;font-size:2.2rem;color:var(--red);
  text-shadow:0 0 30px rgba(255,0,50,1);letter-spacing:6px;pointer-events:none;
  z-index:180;display:none;animation:bwPulse 2.4s forwards;}
@keyframes bwPulse{0%,100%{opacity:0;}30%,70%{opacity:1;}}
#boss-bar{position:absolute;top:64px;left:50%;transform:translateX(-50%);width:300px;
  pointer-events:none;z-index:100;opacity:0;transition:opacity .3s;}
#boss-bar.show{opacity:1;}
#boss-name-lbl{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.72rem;
  color:var(--red);margin-bottom:2px;text-shadow:0 0 10px rgba(255,0,50,.6);letter-spacing:2px;}
#boss-hp-bg{height:10px;background:rgba(255,255,255,.05);border-radius:2px;
  border:1px solid rgba(255,50,70,.3);overflow:hidden;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);transition:width .1s;}

/* ACHIEV */
#achiev{position:absolute;top:60px;left:50%;transform:translateX(-50%) translateY(-80px);
  background:rgba(30,20,4,.97);border:1px solid rgba(245,200,66,.5);border-radius:5px;
  padding:7px 18px;display:flex;align-items:center;gap:8px;z-index:300;transition:transform .3s;
  pointer-events:none;box-shadow:0 4px 20px rgba(245,200,66,.3);}
#achiev.show{transform:translateX(-50%) translateY(0);}
#ach-icon{font-size:1.3rem;}
#ach-title{font-size:.6rem;color:var(--gold);font-weight:700;}
#ach-sub{font-size:.48rem;color:#886600;}

/* HIT FLASH */
#hit-flash{position:absolute;inset:0;pointer-events:none;z-index:150;opacity:0;
  background:rgba(255,30,30,.3);transition:opacity .07s;}

/* COMBO */
#combo-wrap{position:absolute;bottom:64px;right:14px;text-align:right;pointer-events:none;
  opacity:0;transition:opacity .3s;z-index:120;}
#combo-num{font-family:'Black Han Sans',sans-serif;font-size:3rem;color:var(--gold);
  line-height:1;text-shadow:0 0 20px rgba(245,200,66,.8),2px 2px 0 rgba(0,0,0,.8);}
#combo-lbl{font-size:.55rem;color:#ff8800;letter-spacing:4px;}

/* PAUSE */
#pause-ov{flex-direction:column;gap:16px;}
</style>
</head>
<body>
<div id="root">
  <canvas id="gc"></canvas>

  <!-- HUD TOP -->
  <div id="hud">
    <div class="hud-cls" id="hud-name">—</div>
    <div class="bar-wrap">
      <div class="bar-row">
        <span class="bar-lbl">HP</span>
        <div class="bar-bg" style="width:130px"><div class="bar-fill" id="hp-fill"></div><div class="bar-txt" id="hp-txt"></div></div>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">MP</span>
        <div class="bar-bg" style="width:130px"><div class="bar-fill" id="mp-fill"></div></div>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">XP</span>
        <div class="bar-bg" style="width:90px;height:7px;"><div class="bar-fill" id="xp-fill"></div></div>
      </div>
    </div>
    <div class="stat-box"><div class="stat-v" id="s-lv">1</div><div class="stat-l">LV</div></div>
    <div class="stat-box"><div class="stat-v" id="s-atk" style="color:#ff7755">0</div><div class="stat-l">ATK</div></div>
    <div class="stat-box"><div class="stat-v" id="s-kills">0</div><div class="stat-l">KILL</div></div>
    <div class="stat-box"><div class="stat-v" id="s-gold" style="color:var(--gold)">0</div><div class="stat-l">💰</div></div>
    <div id="room-lbl">B1F · 1/1방</div>
  </div>

  <!-- SKILL BAR -->
  <div id="skill-row">
    <div id="sk-cont" style="display:flex;gap:6px;"></div>
    <div id="ctrl-hint">
      WASD 이동 &nbsp;|&nbsp; SPACE·클릭 공격<br>
      Q 스킬 &nbsp;|&nbsp; E 스킬2 &nbsp;|&nbsp; P 일시정지
    </div>
  </div>

  <!-- MINIMAP -->
  <div id="minimap"><canvas id="mm-canvas" width="120" height="90"></canvas></div>

  <!-- BOSS BAR -->
  <div id="boss-bar">
    <div id="boss-name-lbl">BOSS</div>
    <div id="boss-hp-bg"><div id="boss-hp-fill" style="width:100%"></div></div>
  </div>

  <!-- COMBO -->
  <div id="combo-wrap"><div id="combo-num">0</div><div id="combo-lbl">COMBO</div></div>

  <!-- BOSS WARN -->
  <div id="boss-warn">⚠ BOSS ⚠</div>

  <!-- ACHIEVEMENT -->
  <div id="achiev"><div id="ach-icon">🏆</div><div><div id="ach-title">업적</div><div id="ach-sub">달성</div></div></div>

  <!-- HIT FLASH -->
  <div id="hit-flash"></div>

  <!-- ============ OVERLAYS ============ -->
  <!-- TITLE -->
  <div class="ov" id="title-ov">
    <div class="game-logo">던전 런</div>
    <div class="game-sub">DUNGEON RUN : REBORN</div>
    <div class="char-grid" id="char-grid"></div>
    <button class="start-btn" id="start-btn" disabled onclick="startGame()">탐험 시작 ▶</button>
    <div class="tut-hint">
      WASD 또는 방향키로 이동 &nbsp;|&nbsp; SPACE·클릭으로 공격<br>
      Q·E로 스킬 사용 &nbsp;|&nbsp; 방의 모든 적을 처치하면 출구가 열립니다
    </div>
  </div>

  <!-- LEVEL UP -->
  <div class="ov hidden" id="lvlup-ov">
    <div class="result-box">
      <div class="lvlup-title">⬆ LEVEL UP!</div>
      <div style="font-size:.72rem;color:#444;margin-bottom:4px;">능력치를 선택하세요</div>
      <div class="stat-grid" id="stat-pick"></div>
    </div>
  </div>

  <!-- FLOOR CLEAR -->
  <div class="ov hidden" id="clear-ov">
    <div class="result-box">
      <div class="res-title clear-c" id="clear-title">✦ FLOOR CLEAR ✦</div>
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
      <div class="res-title dead-c">💀 GAME OVER</div>
      <div class="res-grid" id="over-grid"></div>
      <div class="action-row">
        <button class="abtn btn-retry" onclick="retryFloor()">재도전 ↺</button>
        <button class="abtn btn-gray" onclick="gotoTitle()">타이틀</button>
      </div>
    </div>
  </div>

  <!-- SHOP -->
  <div class="ov hidden" id="shop-ov">
    <div>
      <div class="shop-title">⚗ 상점</div>
      <div style="font-size:.7rem;color:#444;margin-bottom:4px;">보유 골드: <span id="shop-gold-lbl" style="color:var(--gold);font-weight:700;">0</span></div>
      <div class="shop-grid" id="shop-grid"></div>
      <button class="abtn btn-next" onclick="nextFloor()" style="margin-top:4px;">다음 층으로 ↓</button>
    </div>
  </div>

  <!-- WIN -->
  <div class="ov hidden" id="win-ov">
    <div class="result-box">
      <div class="res-title clear-c">🏆 완전 클리어!</div>
      <div style="font-size:.75rem;color:#777;margin:12px 0;">마왕을 물리치고 던전을 탈출했습니다!</div>
      <div class="res-grid" id="win-grid"></div>
      <div class="action-row">
        <button class="abtn btn-next" onclick="gotoTitle()">타이틀로</button>
      </div>
    </div>
  </div>

  <!-- PAUSE -->
  <div class="ov hidden" id="pause-ov">
    <div style="text-align:center;">
      <div style="font-family:'Black Han Sans',sans-serif;font-size:2.5rem;color:#fff;letter-spacing:6px;">⏸ PAUSE</div>
      <div style="font-size:.7rem;color:#333;margin-top:12px;">P 키를 눌러 계속하기</div>
      <button class="abtn btn-gray" onclick="gotoTitle()" style="margin-top:20px;">타이틀로</button>
    </div>
  </div>
</div>

<script>
'use strict';
// ══════════════════════════════════════════════════════════════════
//  던전 런 : REBORN  v3.0
//  탑다운 던전 크롤러 - 완전 재작성
//  - 8방향 부드러운 이동 (가속/감속)
//  - 방 기반 던전 탐험 (최대 5층)
//  - 다채로운 적 AI (추적/원거리/돌진/반동)
//  - 4개 직업 고유 스킬
//  - 파티클/슬래시/충격파 이펙트
//  - 레벨업 / 상점 / 보스전
// ══════════════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');

// Responsive sizing
function resize() {
  const root = document.getElementById('root');
  const rw = root.clientWidth, rh = root.clientHeight;
  const GAME_W = 800, GAME_H = 560;
  const scale = Math.min(rw / GAME_W, rh / GAME_H);
  canvas.width = GAME_W; canvas.height = GAME_H;
  canvas.style.width = (GAME_W * scale) + 'px';
  canvas.style.height = (GAME_H * scale) + 'px';
}
resize();
window.addEventListener('resize', resize);

const GW = () => canvas.width;
const GH = () => canvas.height;

// ── CONSTANTS ──────────────────────────────────────────────────
const TILE = 40;
const ROOM_COLS = 20; // tiles
const ROOM_ROWS = 14; // tiles
const RW = ROOM_COLS * TILE; // 800
const RH = ROOM_ROWS * TILE; // 560
const MX = RW / 2;  // mid x
const MY = RH / 2;  // mid y
const GRAVITY_NONE = 0; // top-down, no gravity

// ── INPUT ──────────────────────────────────────────────────────
const KEYS = {}, JKEYS = {};
let MOUSE = { x: 0, y: 0, down: false, clicked: false };
canvas.addEventListener('mousemove', e => {
  const r = canvas.getBoundingClientRect();
  const sx = canvas.width / parseFloat(canvas.style.width || canvas.width);
  MOUSE.x = (e.clientX - r.left) * sx;
  MOUSE.y = (e.clientY - r.top) * sx;
});
canvas.addEventListener('mousedown', e => { MOUSE.down = true; MOUSE.clicked = true; });
canvas.addEventListener('mouseup', () => MOUSE.down = false);
window.addEventListener('keydown', e => {
  if (!KEYS[e.key]) { KEYS[e.key] = true; JKEYS[e.key] = true; }
  if ([' ', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e => KEYS[e.key] = false);
function flushJ() { for (const k in JKEYS) delete JKEYS[k]; MOUSE.clicked = false; }

// ── PARTICLE SYSTEM ────────────────────────────────────────────
const PARTS = [];
function spawnParts(x, y, opts = {}) {
  const n = opts.n || 8;
  for (let i = 0; i < n; i++) {
    const a = (opts.dir || 0) + (Math.random() - .5) * (opts.spread || Math.PI * 2);
    const s = (opts.sMin || 1) + Math.random() * (opts.sMax || 5);
    const col = Array.isArray(opts.col) ? opts.col[Math.floor(Math.random() * opts.col.length)] : (opts.col || '#fff');
    PARTS.push({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
      life: 1, decay: (opts.dMin || .025) + Math.random() * (opts.dMax || .03),
      col, sz: (opts.szMin || 2) + Math.random() * (opts.szMax || 5),
      glow: opts.glow || false, type: opts.type || 'c',
      rot: Math.random() * Math.PI * 2, rotV: (Math.random() - .5) * .2,
    });
  }
}
function updateParts(dt) {
  for (let i = PARTS.length - 1; i >= 0; i--) {
    const p = PARTS[i];
    p.x += p.vx * dt * 60; p.y += p.vy * dt * 60;
    p.vx *= .93; p.vy *= .93;
    p.life -= p.decay * dt * 60;
    p.rot += p.rotV;
    if (p.life <= 0) PARTS.splice(i, 1);
  }
}
function drawParts() {
  ctx.save();
  for (const p of PARTS) {
    ctx.globalAlpha = Math.max(0, p.life);
    if (p.glow) { ctx.shadowColor = p.col; ctx.shadowBlur = p.sz * 2.5; }
    ctx.fillStyle = p.col;
    if (p.type === 'sq') {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.fillRect(-p.sz / 2, -p.sz / 2, p.sz, p.sz); ctx.restore();
    } else {
      ctx.beginPath(); ctx.arc(p.x, p.y, p.sz, 0, Math.PI * 2); ctx.fill();
    }
    if (p.glow) ctx.shadowBlur = 0;
  }
  ctx.globalAlpha = 1; ctx.restore();
}

// Slash effects
const SLASHES = [];
function spawnSlash(x, y, ang, len, col, dur = 12) {
  SLASHES.push({ x, y, ang, len, col, life: 1, decay: 1 / dur });
}
function updateSlashes(dt) {
  for (let i = SLASHES.length - 1; i >= 0; i--) {
    SLASHES[i].life -= SLASHES[i].decay * dt * 60;
    if (SLASHES[i].life <= 0) SLASHES.splice(i, 1);
  }
}
function drawSlashes() {
  for (const s of SLASHES) {
    ctx.save();
    ctx.globalAlpha = Math.max(0, s.life) * .9;
    ctx.strokeStyle = s.col; ctx.shadowColor = s.col; ctx.shadowBlur = 10;
    ctx.lineWidth = 2.5 * (s.life + .3); ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(s.x + Math.cos(s.ang + Math.PI) * s.len * .5, s.y + Math.sin(s.ang + Math.PI) * s.len * .5);
    ctx.lineTo(s.x + Math.cos(s.ang) * s.len, s.y + Math.sin(s.ang) * s.len);
    ctx.stroke(); ctx.shadowBlur = 0; ctx.restore();
  }
}

// ── DUNGEON TILE TYPES ─────────────────────────────────────────
const T = { FLOOR: 0, WALL: 1, DOOR_N: 2, DOOR_S: 3, DOOR_W: 4, DOOR_E: 5, EXIT: 6, PILLAR: 7 };
const DOOR_OPEN = { 2: false, 3: false, 4: false, 5: false };

// ── ROOM GENERATION ────────────────────────────────────────────
function makeRoom(exits, isBoss, floorNum) {
  const cols = ROOM_COLS, rows = ROOM_ROWS;
  const tiles = Array.from({ length: rows }, () => Array(cols).fill(T.FLOOR));

  // Walls
  for (let x = 0; x < cols; x++) { tiles[0][x] = T.WALL; tiles[rows - 1][x] = T.WALL; }
  for (let y = 0; y < rows; y++) { tiles[y][0] = T.WALL; tiles[y][cols - 1] = T.WALL; }

  // Exits
  const mid_x = Math.floor(cols / 2), mid_y = Math.floor(rows / 2);
  if (exits.n) { tiles[0][mid_x - 1] = T.DOOR_N; tiles[0][mid_x] = T.DOOR_N; }
  if (exits.s) { tiles[rows - 1][mid_x - 1] = T.DOOR_S; tiles[rows - 1][mid_x] = T.DOOR_S; }
  if (exits.w) { tiles[mid_y - 1][0] = T.DOOR_W; tiles[mid_y][0] = T.DOOR_W; }
  if (exits.e) { tiles[mid_y - 1][cols - 1] = T.DOOR_E; tiles[mid_y][cols - 1] = T.DOOR_E; }

  // Random pillars (not near center or exits)
  if (!isBoss) {
    const pillarCandidates = [
      [3, 3], [3, 10], [3, 16], [10, 3], [10, 16],
      [5, 6], [5, 13], [8, 4], [8, 15],
    ];
    const pillarCount = 2 + floorNum;
    for (let i = 0; i < Math.min(pillarCount, pillarCandidates.length); i++) {
      const [py, px] = pillarCandidates[i];
      if (py > 1 && py < rows - 2 && px > 1 && px < cols - 2) {
        // Check not blocking exits
        const distToCenter = Math.hypot(py - mid_y, px - mid_x);
        if (distToCenter > 4) tiles[py][px] = T.PILLAR;
      }
    }
  }

  return tiles;
}

// ── FLOOR GENERATION ──────────────────────────────────────────
// Layout: linear with branches
// Node grid: max 5 rooms per floor
function generateFloor(floorNum) {
  const numRooms = 3 + Math.min(floorNum, 3); // 4-6 rooms per floor
  const rooms = [];
  const ENEMY_SETS = [
    ['slime', 'bat'],
    ['slime', 'bat', 'skeleton'],
    ['skeleton', 'orc', 'bat'],
    ['orc', 'skeleton', 'mageE'],
    ['orc', 'demon', 'mageE'],
  ];
  const eSet = ENEMY_SETS[Math.min(floorNum - 1, 4)];

  for (let i = 0; i < numRooms; i++) {
    const isFirst = i === 0;
    const isLast = i === numRooms - 1;
    const isBoss = isLast;
    const exits = {
      n: false, s: !isLast, w: false,
      e: i > 0 && i < numRooms - 1 && i % 2 === 1 // side branch
    };
    if (i === 0) exits.n = false;
    else exits.n = true;

    const tiles = makeRoom(exits, isBoss, floorNum);
    const numEnemies = isFirst ? 0 : (isBoss ? 0 : 2 + Math.floor(Math.random() * 3) + Math.floor(floorNum * .5));

    rooms.push({
      id: i, tiles, exits, isBoss, cleared: isFirst,
      doorsOpen: isFirst,
      enemies: [],
      _numE: numEnemies, _eSet: eSet,
      visited: isFirst,
      gridX: 0, gridY: i, // for minimap
    });
  }

  // Add boss to last room
  const bossRoom = rooms[numRooms - 1];
  bossRoom.isBoss = true;

  return rooms;
}

// Spawn enemies for a room
function spawnRoomEnemies(room, floorNum) {
  if (room._spawned) return;
  room._spawned = true;
  const n = room._numE;
  const eSet = room._eSet;
  const cx = RW / 2, cy = RH / 2;

  for (let i = 0; i < n; i++) {
    const typeId = eSet[Math.floor(Math.random() * eSet.length)];
    const angle = (i / n) * Math.PI * 2;
    const dist = 140 + Math.random() * 100;
    const ex = cx + Math.cos(angle) * dist;
    const ey = cy + Math.sin(angle) * dist;
    room.enemies.push(mkEnemy(typeId, ex, ey, floorNum));
  }

  if (room.isBoss) {
    room.enemies.push(mkBoss(floorNum, cx, cy - 60));
  }
}

// ── CHARACTER CLASSES ─────────────────────────────────────────
const CLASSES = {
  warrior: {
    name: '전사', role: '근접 탱커', icon: '⚔️',
    col: '#e74c3c', col2: '#8b0000',
    hp: 220, mp: 80, atk: 40, def: 18, spd: 195, radius: 16,
    atkRange: 85, atkCd: 0.4,
    desc: '높은 체력·방어력. 근접 광역 베기 특화.',
    stars: { ATK: 4, DEF: 5, SPD: 3, RNG: 2 },
    skills: [
      { name: '회오리베기', icon: '🌀', key: 'Q', mp: 18, cd: 4, desc: '주변 360도 강타',
        fn: (p) => {
          hitCircle(p.x, p.y, 110, dmg(p, 2.5), true);
          spawnParts(p.x, p.y, { n: 20, col: ['#ff4444', '#ff8800'], glow: true, sMin: 3, sMax: 8 });
          spawnSlash(p.x, p.y, 0, 100, '#ff8888', 18);
          spawnSlash(p.x, p.y, Math.PI / 2, 100, '#ff8888', 18);
          spawnSlash(p.x, p.y, Math.PI, 100, '#ff8888', 18);
          shake(6, 18);
        }
      },
      { name: '방패 돌격', icon: '🛡️', key: 'E', mp: 25, cd: 6, desc: '전방 돌진+스턴',
        fn: (p) => {
          const ang = getPlayerAimAngle(p);
          p.vx = Math.cos(ang) * 500; p.vy = Math.sin(ang) * 500;
          p.invincible = 0.5;
          setTimeout(() => {
            hitCircle(p.x, p.y, 80, dmg(p, 2.0), true, { stun: 1.5 });
            shake(5, 14);
          }, 200);
        }
      },
    ],
  },
  mage: {
    name: '마법사', role: '원소 마법사', icon: '🔮',
    col: '#9b59b6', col2: '#4a0080',
    hp: 130, mp: 260, atk: 65, def: 5, spd: 175, radius: 14,
    atkRange: 340, atkCd: 0.55,
    desc: '초강력 원거리 마법. 높은 폭발 딜.',
    stars: { ATK: 5, DEF: 1, SPD: 3, RNG: 5 },
    skills: [
      { name: '파이어볼', icon: '🔥', key: 'Q', mp: 22, cd: 2, desc: '추적 화염탄 3발',
        fn: (p) => {
          for (let i = 0; i < 3; i++) setTimeout(() => {
            const ang = getPlayerAimAngle(p) + (Math.random() - .5) * .3;
            spawnProj(p.x, p.y, Math.cos(ang) * 380, Math.sin(ang) * 380, dmg(p, 1.8), '#ff6600', 'player', { sz: 12, emoji: '🔥', homing: true });
          }, i * 90);
        }
      },
      { name: '블리자드', icon: '❄️', key: 'E', mp: 50, cd: 10, desc: '전체 빙결 + 피해',
        fn: (p) => {
          hitAll(dmg(p, 1.5), true, { frozen: 2.5 });
          spawnParts(p.x, p.y, { n: 35, col: ['#44aaff', '#aaddff'], glow: true, sMin: 3, sMax: 10 });
        }
      },
    ],
  },
  archer: {
    name: '궁수', role: '전술 사수', icon: '🏹',
    col: '#27ae60', col2: '#145a32',
    hp: 160, mp: 150, atk: 48, def: 8, spd: 230, radius: 14,
    atkRange: 320, atkCd: 0.3,
    desc: '빠른 이동속도. 화살 연사 특화.',
    stars: { ATK: 4, DEF: 2, SPD: 5, RNG: 5 },
    skills: [
      { name: '폭발 화살', icon: '💥', key: 'Q', mp: 20, cd: 3, desc: '폭발 광역 화살',
        fn: (p) => {
          const ang = getPlayerAimAngle(p);
          spawnProj(p.x, p.y, Math.cos(ang) * 420, Math.sin(ang) * 420, dmg(p, 3.5), '#ffcc00', 'player', { sz: 14, emoji: '💣', explode: true });
        }
      },
      { name: '5연사', icon: '⚡', key: 'E', mp: 30, cd: 5, desc: '화살 5발 연속',
        fn: (p) => {
          const baseAng = getPlayerAimAngle(p);
          for (let i = 0; i < 5; i++) setTimeout(() => {
            const ang = baseAng + (i - 2) * .12;
            spawnProj(p.x, p.y, Math.cos(ang) * 450, Math.sin(ang) * 450, dmg(p, 1.2), '#44ff88', 'player', { sz: 8, pierce: true });
          }, i * 60);
        }
      },
    ],
  },
  ninja: {
    name: '닌자', role: '암살자', icon: '🌀',
    col: '#2c3e50', col2: '#0a1525',
    hp: 150, mp: 180, atk: 52, def: 6, spd: 280, radius: 13,
    atkRange: 75, atkCd: 0.22,
    desc: '초고속 이동. 텔레포트 암습 특화.',
    stars: { ATK: 5, DEF: 2, SPD: 5, RNG: 2 },
    skills: [
      { name: '순간이동 강습', icon: '💨', key: 'Q', mp: 20, cd: 3, desc: '타겟에 순간이동 후 강타',
        fn: (p) => {
          const target = getNearestEnemy(p);
          if (target) {
            spawnParts(p.x, p.y, { n: 15, col: ['#2c3e50', '#44ddff'], grav: 0, sMin: 2, sMax: 6 });
            p.x = target.x + 40; p.y = target.y;
            hitCircle(p.x, p.y, 70, dmg(p, 3.5), true);
            spawnSlash(p.x, p.y, 0, 80, '#44ddff', 14);
            shake(5, 12);
          } else {
            const ang = getPlayerAimAngle(p);
            p.x += Math.cos(ang) * 180; p.y += Math.sin(ang) * 180;
          }
          p.invincible = .8;
        }
      },
      { name: '분신 공격', icon: '👥', key: 'E', mp: 40, cd: 8, desc: '6방향 동시 타격',
        fn: (p) => {
          for (let i = 0; i < 6; i++) {
            const a = i / 6 * Math.PI * 2;
            hitCircle(p.x + Math.cos(a) * 60, p.y + Math.sin(a) * 60, 50, dmg(p, 2.8), true);
            spawnSlash(p.x + Math.cos(a) * 60, p.y + Math.sin(a) * 60, a, 60, '#44ffaa', 12);
          }
          shake(8, 20);
        }
      },
    ],
  },
};

// ── ENEMY TYPES ───────────────────────────────────────────────
const ETYPES = {
  slime: {
    name: '슬라임', col: '#2ecc71', col2: '#1a8a4a', radius: 20,
    hp: 60, atk: 8, spd: 65, xp: 15, gold: 5,
    ai: 'bounce', drawFn: drawSlime,
  },
  bat: {
    name: '박쥐', col: '#9b59b6', col2: '#5a2080', radius: 12,
    hp: 40, atk: 12, spd: 160, xp: 20, gold: 7,
    ai: 'erratic', drawFn: drawBat,
  },
  skeleton: {
    name: '해골', col: '#ecf0f1', col2: '#aaa', radius: 16,
    hp: 80, atk: 15, spd: 90, xp: 25, gold: 10,
    ai: 'ranged', drawFn: drawSkeleton,
  },
  orc: {
    name: '오크', col: '#27ae60', col2: '#145a32', radius: 24,
    hp: 160, atk: 22, spd: 85, xp: 40, gold: 18,
    ai: 'charge', drawFn: drawOrc,
  },
  mageE: {
    name: '마법사', col: '#8e44ad', col2: '#4a0080', radius: 16,
    hp: 90, atk: 28, spd: 75, xp: 35, gold: 15,
    ai: 'mage', drawFn: drawMageEnemy,
  },
  demon: {
    name: '악마', col: '#c0392b', col2: '#7b241c', radius: 20,
    hp: 140, atk: 26, spd: 100, xp: 50, gold: 22,
    ai: 'charge', drawFn: drawDemon,
  },
};

function mkEnemy(typeId, x, y, floorNum) {
  const t = ETYPES[typeId];
  const sc = 1 + (floorNum - 1) * .28;
  return {
    ...t, typeId, x, y, vx: 0, vy: 0,
    hp: Math.round(t.hp * sc), maxHp: Math.round(t.hp * sc),
    atk: Math.round(t.atk * sc),
    alive: true, dying: false, deathTimer: 0.5,
    frozen: 0, stun: 0, burn: 0, cursed: 0,
    hitFlash: 0,
    dir: Math.random() * Math.PI * 2,
    atkTimer: 1 + Math.random(),
    phaseTimer: 1 + Math.random() * 2,
    uid: 'e' + Math.random(),
    // AI state
    chargeDir: 0, charging: false, chargeTimer: 0,
    projTimer: 1 + Math.random() * 1.5,
    walkPhase: Math.random() * Math.PI * 2,
  };
}

// ── BOSSES ────────────────────────────────────────────────────
const BOSS_DEFS = [
  { name: '🕷 거미 여왕', col: '#8e44ad', col2: '#4a006a', radius: 35, hp: 800, atk: 30, spd: 100, xp: 500 },
  { name: '🐉 화염 드래곤', col: '#e74c3c', col2: '#7b0000', radius: 42, hp: 1400, atk: 42, spd: 90, xp: 800 },
  { name: '💀 리치 왕', col: '#bdc3c7', col2: '#444', radius: 38, hp: 2000, atk: 55, spd: 95, xp: 1100 },
  { name: '👿 악마 군주', col: '#c0392b', col2: '#5b0000', radius: 44, hp: 2800, atk: 65, spd: 100, xp: 1500 },
  { name: '☠ 마왕 다크오스', col: '#8e44ad', col2: '#1a0030', radius: 50, hp: 4000, atk: 80, spd: 110, xp: 3000 },
];

function mkBoss(floorNum, x, y) {
  const def = BOSS_DEFS[Math.min(floorNum - 1, 4)];
  return {
    ...def, typeId: 'boss', x, y, vx: 0, vy: 0,
    alive: true, dying: false, deathTimer: 1,
    hitFlash: 0, frozen: 0, stun: 0,
    dir: Math.PI / 2,
    atkTimer: 1.5,
    projTimer: 1.8,
    phaseTimer: 2,
    uid: 'boss' + Math.random(),
    phase: 1, phase2: false, phase3: false,
    walkPhase: 0,
    isBoss: true,
  };
}

// ── GAME STATE ────────────────────────────────────────────────
let G = null, RAF = null;
let selClassId = null;
let timer = 0, lastTs = 0;

const SHOP_ITEMS = [
  { name: 'HP 포션', icon: '🧪', desc: 'HP 30% 회복', price: 60, fn: p => { p.hp = Math.min(p.maxHp, p.hp + p.maxHp * .3); return 'HP +30%'; } },
  { name: '대형 HP 포션', icon: '⚗️', desc: 'HP 완전 회복', price: 160, fn: p => { p.hp = p.maxHp; return 'HP 완전 회복!'; } },
  { name: 'MP 포션', icon: '💙', desc: 'MP 50% 회복', price: 80, fn: p => { p.mp = Math.min(p.maxMp, p.mp + p.maxMp * .5); return 'MP +50%'; } },
  { name: '강화 검', icon: '⚔️', desc: 'ATK +15', price: 200, fn: p => { p.atk += 15; return 'ATK +15'; } },
  { name: '전설의 검', icon: '🗡️', desc: 'ATK +35', price: 400, fn: p => { p.atk += 35; return 'ATK +35'; } },
  { name: '방어 갑옷', icon: '🛡️', desc: 'DEF+12 MaxHP+40', price: 220, fn: p => { p.def += 12; p.maxHp += 40; p.hp = Math.min(p.maxHp, p.hp + 40); return 'DEF+12 HP+40'; } },
  { name: '스피드 부츠', icon: '👟', desc: '이동속도 +25', price: 180, fn: p => { p.spd += 25; return 'SPD +25'; } },
  { name: '크리티컬 반지', icon: '💍', desc: '치명타 확률 +15%', price: 300, fn: p => { p.crit = (p.crit || .1) + .15; return 'CRIT +15%'; } },
  { name: '전설의 목걸이', icon: '📿', desc: 'ATK+20 CRIT+20%', price: 500, fn: p => { p.atk += 20; p.crit = (p.crit || .1) + .2; return 'ATK+20 CRIT+20%'; } },
];

function initGame(classId, floorNum = 1, keepPlayer = null) {
  const cls = CLASSES[classId];
  let player;
  if (keepPlayer) {
    player = keepPlayer;
    player.x = MX; player.y = MY + 80;
    player.vx = 0; player.vy = 0;
    player.invincible = 0;
    player.atkCd = 0;
  } else {
    player = {
      ...cls, clsId: classId,
      x: MX, y: MY + 80,
      vx: 0, vy: 0,
      hp: cls.hp, maxHp: cls.hp,
      mp: cls.mp, maxMp: cls.mp,
      atk: cls.atk, def: cls.def, spd: cls.spd,
      crit: .1,
      alive: true,
      invincible: 0,
      atkCd: 0, atkAnim: 0, atkDir: 0,
      hitFlash: 0,
      skillCds: cls.skills.map(() => 0),
      level: 1, xp: 0, xpNext: 100,
      kills: 0, gold: 0, score: 0,
      combo: 0, comboTimer: 0, maxCombo: 0,
      walkPhase: 0,
      state: 'idle',
      buffTimer: 0,
      shield: false,
      atkBonus: 0,
    };
  }

  const rooms = generateFloor(floorNum);

  G = {
    classId, floorNum,
    player, rooms,
    currentRoomIdx: 0,
    projectiles: [],
    items: [],
    particles: PARTS,
    shakeAmt: 0, shakeTimer: 0,
    hitStop: 0,
    phase: 'play',
    paused: false,
    pendingLvlUp: false,
    roomKills: 0,
    startTime: Date.now(),
    totalKills: 0,
    shopStock: [],
  };

  PARTS.length = 0; SLASHES.length = 0;
  spawnRoomEnemies(rooms[0], floorNum);
  updateBossUI();
}

// ── CURRENT ROOM ──────────────────────────────────────────────
function room() { return G.rooms[G.currentRoomIdx]; }
function enemies() { return room().enemies.filter(e => e.alive || e.dying); }
function liveEnemies() { return room().enemies.filter(e => e.alive); }

// ── COMBAT HELPERS ────────────────────────────────────────────
function totalAtk(p) { return (p.atk + (p.atkBonus || 0)) * (p.buffAtk || 1); }
function totalDef(p) { return p.def; }
function totalCrit(p) { return p.crit || .1; }

function dmg(p, mult) {
  const a = totalAtk(p);
  const isCrit = Math.random() < totalCrit(p);
  const v = Math.round((a * mult + Math.random() * 5 - 2) * (isCrit ? 2.1 : 1));
  return { v: Math.max(1, v), crit: isCrit };
}

function dealDmgTo(e, v, crit) {
  if (!e.alive) return;
  if (e.frozen > 0) v = Math.round(v * 1.4);
  e.hp -= v; e.hitFlash = .15;
  G.hitStop = crit ? .08 : .04;
  showDNum(e.x, e.y - e.radius - 8, v, crit);
  if (e.hp <= 0) killEnemy(e);
}

function hitCircle(cx, cy, r, d, showCrit, opts = {}) {
  for (const e of liveEnemies()) {
    const dx = e.x - cx, dy = e.y - cy;
    if (dx * dx + dy * dy < (r + e.radius) ** 2) {
      dealDmgTo(e, d.v, d.crit || showCrit);
      if (opts.stun) e.stun = Math.max(e.stun || 0, opts.stun);
      const kd = Math.hypot(dx, dy) || 1;
      e.vx += (dx / kd) * 200; e.vy += (dy / kd) * 200;
    }
  }
  if (G.boss && G.boss.alive) {
    const dx = G.boss.x - cx, dy = G.boss.y - cy;
    if (dx * dx + dy * dy < (r + G.boss.radius) ** 2) {
      dealDmgTo(G.boss, d.v, d.crit || showCrit);
      if (opts.stun) G.boss.stun = Math.max(G.boss.stun || 0, opts.stun);
    }
  }
}

function hitAll(d, showCrit, opts = {}) {
  for (const e of liveEnemies()) {
    dealDmgTo(e, d.v, d.crit || showCrit);
    if (opts.frozen) e.frozen = Math.max(e.frozen || 0, opts.frozen);
  }
  if (G.boss && G.boss.alive) {
    dealDmgTo(G.boss, d.v, d.crit || showCrit);
    if (opts.frozen) G.boss.frozen = Math.max(G.boss.frozen || 0, opts.frozen);
  }
}

function getNearestEnemy(p) {
  let best = null, bd = Infinity;
  for (const e of liveEnemies()) {
    const d = Math.hypot(e.x - p.x, e.y - p.y);
    if (d < bd) { bd = d; best = e; }
  }
  if (G.boss && G.boss.alive) {
    const d = Math.hypot(G.boss.x - p.x, G.boss.y - p.y);
    if (d < bd) best = G.boss;
  }
  return best;
}

function getPlayerAimAngle(p) {
  // First try mouse, then nearest enemy
  const dx = MOUSE.x - p.x, dy = MOUSE.y - p.y;
  if (Math.hypot(dx, dy) > 20) return Math.atan2(dy, dx);
  const t = getNearestEnemy(p);
  if (t) return Math.atan2(t.y - p.y, t.x - p.x);
  return p.dir || 0;
}

function killEnemy(e) {
  e.alive = false; e.dying = true;
  const p = G.player;
  if (e.isBoss) {
    p.xp += e.xp; p.gold += 200; p.score += e.xp * 3;
    G.totalKills++;
    spawnParts(e.x, e.y, { n: 60, col: ['#ffcc00', '#ff6600', '#fff'], glow: true, sMin: 4, sMax: 15 });
    shake(16, 60);
    sfx_clear();
    document.getElementById('boss-bar').classList.remove('show');
    setTimeout(() => floorClear(), 1200);
  } else {
    p.kills++; p.xp += e.xp; p.gold += e.gold || 10; p.score += e.xp * 2;
    G.totalKills++; G.roomKills++;
    spawnParts(e.x, e.y, { n: 12, col: [e.col, '#ffcc00'], sMin: 2, sMax: 6 });
    checkLvlUp(p);
    tryDropItem(e);
  }
  checkRoomClear();
}

function checkRoomClear() {
  const r = room();
  if (r.cleared) return;
  if (liveEnemies().length === 0) {
    r.cleared = true;
    r.doorsOpen = true;
    spawnParts(MX, MY, { n: 25, col: ['#ffcc00', '#44ff88', '#fff'], glow: true, upb: 3, sMin: 3, sMax: 8 });
    sfx_roomClear();
    showAchiev('✅ 방 클리어!', '출구가 열렸습니다');
  }
}

function checkLvlUp(p) {
  while (p.xp >= p.xpNext) {
    p.xp -= p.xpNext; p.level++;
    p.xpNext = Math.round(p.xpNext * 1.5);
    p.maxHp += 25; p.hp = Math.min(p.maxHp, p.hp + 40);
    p.maxMp += 10; p.mp = Math.min(p.maxMp, p.mp + 15);
    G.pendingLvlUp = true;
    showLvlUpModal();
    sfx_lvlup();
  }
}

function tryDropItem(e) {
  if (Math.random() > .35) return;
  G.items.push({
    x: e.x, y: e.y,
    type: Math.random() < .7 ? 'hp' : 'mp',
    life: 12, uid: 'i' + Math.random(), alive: true,
  });
}

function takeDmg(v) {
  const p = G.player;
  if (p.invincible > 0 || p.shield) return;
  const reduced = Math.max(1, v - Math.floor(totalDef(p) * .5));
  p.hp -= reduced; p.hitFlash = .2; p.invincible = .55;
  G.shakeAmt = Math.max(G.shakeAmt, 5); G.shakeTimer = Math.max(G.shakeTimer, .3);
  const fl = document.getElementById('hit-flash');
  fl.style.opacity = '1'; fl.style.background = 'rgba(255,30,30,.35)';
  setTimeout(() => fl.style.opacity = '0', 140);
  sfx_hit();
  if (p.hp <= 0) gameOver();
}

// ── PROJECTILES ───────────────────────────────────────────────
function spawnProj(x, y, vx, vy, d, col, owner, opts = {}) {
  G.projectiles.push({
    x, y, vx, vy, dmgV: d.v, dmgCrit: d.crit, col, owner, alive: true,
    life: opts.life || 2, sz: opts.sz || 8,
    pierce: opts.pierce || false, emoji: opts.emoji || null,
    homing: opts.homing || false, explode: opts.explode || false,
    glow: opts.glow !== undefined ? opts.glow : true,
    uid: 'p' + Math.random(),
  });
}

function updateProjs(dt) {
  G.projectiles = G.projectiles.filter(pr => {
    if (!pr.alive) return false;
    pr.life -= dt;
    if (pr.life <= 0) return false;

    if (pr.homing && pr.owner === 'player') {
      const t = getNearestEnemy(G.player);
      if (t) {
        const dx = t.x - pr.x, dy = t.y - pr.y;
        const l = Math.hypot(dx, dy) || 1;
        pr.vx += (dx / l * 300 - pr.vx) * dt * 3;
        pr.vy += (dy / l * 300 - pr.vy) * dt * 3;
      }
    }

    pr.x += pr.vx * dt; pr.y += pr.vy * dt;

    // Wall collision
    if (pr.x < 40 || pr.x > RW - 40 || pr.y < 40 || pr.y > RH - 40) {
      if (pr.explode) { explodeProj(pr); }
      return false;
    }

    if (pr.owner === 'player') {
      const targets = liveEnemies();
      if (G.boss && G.boss.alive) targets.push(G.boss);
      for (const e of targets) {
        if (Math.hypot(pr.x - e.x, pr.y - e.y) < e.radius + pr.sz) {
          dealDmgTo(e, pr.dmgV, pr.dmgCrit);
          if (pr.explode) { explodeProj(pr); return false; }
          if (!pr.pierce) { pr.alive = false; return false; }
        }
      }
    } else { // enemy proj
      const p = G.player;
      if (Math.hypot(pr.x - p.x, pr.y - p.y) < p.radius + pr.sz) {
        takeDmg(pr.dmgV);
        pr.alive = false; return false;
      }
    }
    return true;
  });
}

function explodeProj(pr) {
  hitCircle(pr.x, pr.y, 80, { v: pr.dmgV, crit: pr.dmgCrit }, false);
  spawnParts(pr.x, pr.y, { n: 20, col: [pr.col, '#ff8800', '#fff'], glow: true, sMin: 3, sMax: 9 });
  shake(5, 12);
}

// ── ROOM TRANSITION ───────────────────────────────────────────
function tryRoomTransition(p) {
  const r = room();
  if (!r.doorsOpen) return;

  const MARGIN = 20;
  const nextRoomIdx = G.currentRoomIdx;
  let nx = p.x, ny = p.y, changed = false;

  // South exit -> next room
  if (p.y > RH - MARGIN && r.exits.s) {
    G.currentRoomIdx = Math.min(G.currentRoomIdx + 1, G.rooms.length - 1);
    changed = true; nx = MX; ny = 60;
  }
  // North exit -> prev room
  if (p.y < MARGIN && r.exits.n) {
    G.currentRoomIdx = Math.max(G.currentRoomIdx - 1, 0);
    changed = true; nx = MX; ny = RH - 60;
  }
  // East
  if (p.x > RW - MARGIN && r.exits.e) {
    G.currentRoomIdx = Math.min(G.currentRoomIdx + 1, G.rooms.length - 1);
    changed = true; nx = 60; ny = MY;
  }
  // West
  if (p.x < MARGIN && r.exits.w) {
    G.currentRoomIdx = Math.max(G.currentRoomIdx - 1, 0);
    changed = true; nx = RW - 60; ny = MY;
  }

  if (changed && G.currentRoomIdx !== nextRoomIdx) {
    p.x = nx; p.y = ny; p.vx = 0; p.vy = 0;
    PARTS.length = 0; G.projectiles = [];
    const newRoom = room();
    if (!newRoom.visited) { newRoom.visited = true; }
    spawnRoomEnemies(newRoom, G.floorNum);
    G.roomKills = 0;
    updateBossUI();
    sfx_door();
  }
}

function updateBossUI() {
  const r = room();
  const boss = r.enemies.find(e => e.isBoss && e.alive);
  G.boss = boss || null;
  if (boss) {
    const bbar = document.getElementById('boss-bar');
    bbar.classList.add('show');
    document.getElementById('boss-name-lbl').textContent = '⚠ ' + boss.name;
    const bw = document.getElementById('boss-warn');
    bw.style.display = 'block';
    bw.textContent = '⚠ BOSS ⚠\n' + boss.name;
    setTimeout(() => bw.style.display = 'none', 2500);
    shake(14, 50); sfx_boss();
  } else {
    document.getElementById('boss-bar').classList.remove('show');
  }
}

// ── PLAYER UPDATE ────────────────────────────────────────────
function updatePlayer(dt) {
  const p = G.player;
  if (!p.alive) return;

  // Input
  let mx = 0, my = 0;
  if (KEYS['ArrowLeft'] || KEYS['a'] || KEYS['A']) mx -= 1;
  if (KEYS['ArrowRight'] || KEYS['d'] || KEYS['D']) mx += 1;
  if (KEYS['ArrowUp'] || KEYS['w'] || KEYS['W']) my -= 1;
  if (KEYS['ArrowDown'] || KEYS['s'] || KEYS['S']) my += 1;

  const len = Math.hypot(mx, my) || 1;
  const nm_x = mx / len, nm_y = my / len;
  const spd = p.spd;
  const accel = 1500;

  if (mx !== 0 || my !== 0) {
    p.vx += nm_x * accel * dt;
    p.vy += nm_y * accel * dt;
    const mag = Math.hypot(p.vx, p.vy);
    if (mag > spd) { p.vx = p.vx / mag * spd; p.vy = p.vy / mag * spd; }
    p.state = 'walk';
    p.dir = Math.atan2(p.vy, p.vx);
  } else {
    p.vx *= Math.pow(.08, dt);
    p.vy *= Math.pow(.08, dt);
    if (Math.hypot(p.vx, p.vy) < 2) { p.vx = 0; p.vy = 0; }
    p.state = 'idle';
  }

  p.x += p.vx * dt; p.y += p.vy * dt;

  // Wall collision
  const R = p.radius;
  if (p.x < R + TILE) { p.x = R + TILE; p.vx = Math.max(0, p.vx); }
  if (p.x > RW - R - TILE) { p.x = RW - R - TILE; p.vx = Math.min(0, p.vx); }
  if (p.y < R + TILE) { p.y = R + TILE; p.vy = Math.max(0, p.vy); }
  if (p.y > RH - R - TILE) { p.y = RH - R - TILE; p.vy = Math.min(0, p.vy); }

  // Pillar collision
  const r = room();
  for (let ty = 0; ty < ROOM_ROWS; ty++) {
    for (let tx = 0; tx < ROOM_COLS; tx++) {
      if (r.tiles[ty][tx] === T.PILLAR || r.tiles[ty][tx] === T.WALL) {
        const wx = tx * TILE, wy = ty * TILE;
        if (p.x + R > wx && p.x - R < wx + TILE && p.y + R > wy && p.y - R < wy + TILE) {
          const cx = wx + TILE / 2, cy = wy + TILE / 2;
          const dx = p.x - cx, dy = p.y - cy;
          const overlap = R + TILE / 2 - Math.hypot(dx, dy) + 2;
          if (overlap > 0) {
            const l = Math.hypot(dx, dy) || 1;
            p.x += (dx / l) * overlap; p.y += (dy / l) * overlap;
          }
        }
      }
    }
  }

  // Attack
  if (p.atkCd > 0) p.atkCd -= dt;
  if ((JKEYS[' '] || MOUSE.clicked || KEYS[' '] || MOUSE.down) && p.atkCd <= 0) {
    doPlayerAttack(p);
  }

  // Aim direction
  const dxm = MOUSE.x - p.x, dym = MOUSE.y - p.y;
  if (Math.hypot(dxm, dym) > 10) p.aimDir = Math.atan2(dym, dxm);

  // Skills
  for (const [ki, sk] of p.skills.entries()) {
    const key = sk.key;
    if (JKEYS[key] || JKEYS[key.toLowerCase()]) useSkill(p, ki);
  }
  for (let i = 0; i < p.skillCds.length; i++) if (p.skillCds[i] > 0) p.skillCds[i] -= dt;

  // Pause
  if (JKEYS['p'] || JKEYS['P']) {
    G.paused = !G.paused;
    document.getElementById('pause-ov').classList.toggle('hidden', !G.paused);
  }

  // Timers
  if (p.invincible > 0) p.invincible -= dt;
  if (p.hitFlash > 0) p.hitFlash -= dt;
  if (p.comboTimer > 0) {
    p.comboTimer -= dt;
    if (p.comboTimer <= 0) { p.combo = 0; document.getElementById('combo-wrap').style.opacity = '0'; }
  }
  if (p.atkAnim > 0) p.atkAnim -= dt;
  if (p.buffTimer > 0) { p.buffTimer -= dt; if (p.buffTimer <= 0) p.buffAtk = 1; }

  // Walk animation
  const moving = Math.hypot(p.vx, p.vy) > 10;
  if (moving) p.walkPhase += dt * 8;

  // MP regen
  p.mp = Math.min(p.maxMp, p.mp + dt * 2);

  // Item pickup
  G.items = G.items.filter(it => {
    if (!it.alive) return false;
    it.life -= dt;
    if (it.life <= 0) { it.alive = false; return false; }
    if (Math.hypot(it.x - p.x, it.y - p.y) < 32) {
      if (it.type === 'hp') { p.hp = Math.min(p.maxHp, p.hp + 30); showDNum(it.x, it.y - 10, '+30 HP', false, '#22ff88'); }
      else { p.mp = Math.min(p.maxMp, p.mp + 25); showDNum(it.x, it.y - 10, '+25 MP', false, '#44aaff'); }
      sfx_item();
      it.alive = false; return false;
    }
    return true;
  });

  tryRoomTransition(p);
}

function doPlayerAttack(p) {
  p.atkCd = p.atkCd_base || (p.cls ? p.cls.atkCd : 0.35);
  p.atkAnim = .25;
  p.combo = Math.min(10, (p.combo || 0) + 1); p.comboTimer = 1.2;
  if (p.combo > p.maxCombo) p.maxCombo = p.combo;

  const cw = document.getElementById('combo-wrap');
  document.getElementById('combo-num').textContent = p.combo + ' HIT';
  cw.style.opacity = p.combo >= 2 ? '1' : '0';

  const aimDir = p.aimDir || 0;
  const mult = 1 + p.combo * .08;
  const d = dmg(p, mult);

  if (p.atkRange > 200) {
    // Ranged
    const spd = p.clsId === 'mage' ? 360 : 420;
    spawnProj(p.x, p.y, Math.cos(aimDir) * spd, Math.sin(aimDir) * spd, d, p.col, 'player', { sz: p.clsId === 'mage' ? 12 : 8, glow: true });
  } else {
    // Melee
    hitCircle(p.x + Math.cos(aimDir) * p.atkRange * .5, p.y + Math.sin(aimDir) * p.atkRange * .5, p.atkRange * .6, d, false);
    spawnSlash(p.x, p.y, aimDir, p.atkRange, d.crit ? '#ffff88' : p.col, 10);
    spawnParts(p.x + Math.cos(aimDir) * 40, p.y + Math.sin(aimDir) * 40, {
      n: d.crit ? 14 : 7, col: [p.col, '#ffcc00'], dir: aimDir, spread: .8, sMin: 2, sMax: d.crit ? 7 : 5, glow: d.crit,
    });
    if (d.crit) shake(3, 6);
  }
  sfx_atk();
}

function useSkill(p, idx) {
  const sk = p.skills[idx];
  if (!sk || p.skillCds[idx] > 0 || p.mp < sk.mp) return;
  p.mp -= sk.mp; p.skillCds[idx] = sk.cd;
  sk.fn(p);
  sfx_skill();
}

// ── ENEMY UPDATE ──────────────────────────────────────────────
function updateEnemies(dt) {
  const p = G.player;
  for (const e of enemies()) {
    if (!e.alive) {
      if (e.dying) { e.deathTimer -= dt; }
      continue;
    }
    if (e.hitFlash > 0) e.hitFlash -= dt;
    if (e.frozen > 0) { e.frozen -= dt; e.vx *= .85; e.vy *= .85; continue; }
    if (e.stun > 0) { e.stun -= dt; e.vx *= .9; e.vy *= .9; continue; }

    e.vx *= Math.pow(.2, dt); e.vy *= Math.pow(.2, dt);
    e.walkPhase += dt * 5;

    const dx = p.x - e.x, dy = p.y - e.y;
    const dist = Math.hypot(dx, dy);
    if (dist > 650) continue; // culling

    e.dir = Math.atan2(dy, dx);
    e.phaseTimer -= dt;

    switch (e.ai) {
      case 'bounce':
        if (e.phaseTimer <= 0) {
          e.dir = e.dir + (Math.random() - .5) * 1.5;
          e.phaseTimer = .5 + Math.random();
        }
        if (dist < 380) {
          e.vx += Math.cos(e.dir) * e.spd * dt * 3;
          e.vy += Math.sin(e.dir) * e.spd * dt * 3;
        }
        break;
      case 'erratic':
        if (e.phaseTimer <= 0) { e.dir = e.dir + (Math.random() - .5) * Math.PI; e.phaseTimer = .3 + Math.random() * .5; }
        e.vx += Math.cos(e.dir) * e.spd * dt * 4;
        e.vy += Math.sin(e.dir) * e.spd * dt * 4;
        break;
      case 'chase':
        if (dist > 30) { e.vx += (dx / dist) * e.spd * dt * 4; e.vy += (dy / dist) * e.spd * dt * 4; }
        break;
      case 'charge':
        if (!e.charging) {
          if (dist < 250 && e.phaseTimer <= 0) {
            e.charging = true; e.chargeDir = e.dir; e.chargeTimer = .5;
          } else if (dist > 60) {
            e.vx += (dx / dist) * e.spd * .6 * dt * 4;
            e.vy += (dy / dist) * e.spd * .6 * dt * 4;
          }
        } else {
          e.vx += Math.cos(e.chargeDir) * e.spd * 3 * dt * 4;
          e.vy += Math.sin(e.chargeDir) * e.spd * 3 * dt * 4;
          e.chargeTimer -= dt;
          if (e.chargeTimer <= 0) { e.charging = false; e.phaseTimer = 1.2 + Math.random(); }
        }
        break;
      case 'ranged':
        if (dist < 200) { e.vx -= (dx / dist) * e.spd * .8 * dt * 4; e.vy -= (dy / dist) * e.spd * .8 * dt * 4; }
        else if (dist > 350) { e.vx += (dx / dist) * e.spd * .6 * dt * 4; e.vy += (dy / dist) * e.spd * .6 * dt * 4; }
        break;
      case 'mage':
        if (dist < 180) { e.vx -= (dx / dist) * e.spd * dt * 4; e.vy -= (dy / dist) * e.spd * dt * 4; }
        else if (dist > 300) { e.vx += (dx / dist) * e.spd * .7 * dt * 4; e.vy += (dy / dist) * e.spd * .7 * dt * 4; }
        break;
      case 'phase':
        e.vx += (dx / dist) * e.spd * dt * 3.5; e.vy += (dy / dist) * e.spd * dt * 3.5;
        break;
    }

    // Clamp speed
    const spd = Math.hypot(e.vx, e.vy);
    if (spd > e.spd * 3) { e.vx = e.vx / spd * e.spd * 3; e.vy = e.vy / spd * e.spd * 3; }

    e.x += e.vx * dt; e.y += e.vy * dt;

    // Wall bounce
    if (e.x < TILE + e.radius) { e.x = TILE + e.radius; e.vx = Math.abs(e.vx); }
    if (e.x > RW - TILE - e.radius) { e.x = RW - TILE - e.radius; e.vx = -Math.abs(e.vx); }
    if (e.y < TILE + e.radius) { e.y = TILE + e.radius; e.vy = Math.abs(e.vy); }
    if (e.y > RH - TILE - e.radius) { e.y = RH - TILE - e.radius; e.vy = -Math.abs(e.vy); }

    // Attack player
    e.atkTimer -= dt;
    if (e.atkTimer <= 0 && dist < e.radius + p.radius + 30) {
      e.atkTimer = .8 + Math.random() * .5;
      takeDmg(e.atk);
    }

    // Ranged attack
    if ((e.ai === 'ranged' || e.ai === 'mage') && dist < 380) {
      e.projTimer = (e.projTimer || 2) - dt;
      if (e.projTimer <= 0) {
        e.projTimer = 1.5 + Math.random();
        const dv = { v: Math.round(e.atk * .75), crit: false };
        spawnProj(e.x, e.y, (dx / dist) * 220, (dy / dist) * 220, dv, e.col, 'enemy', { sz: 10 });
      }
    }

    // Boss AI
    if (e.isBoss) updateBossAI(e, p, dt);
  }
}

function updateBossAI(b, p, dt) {
  const hpPct = b.hp / b.maxHp;
  if (!b.phase2 && hpPct < .55) {
    b.phase2 = true; b.spd *= 1.35;
    spawnParts(b.x, b.y, { n: 50, col: ['#ff4400', '#ff8800'], glow: true, sMin: 4, sMax: 14 });
    shake(12, 40);
  }
  if (!b.phase3 && hpPct < .25) {
    b.phase3 = true; b.spd *= 1.25;
    spawnParts(b.x, b.y, { n: 80, col: ['#ff0000', '#aa00ff', '#fff'], glow: true, sMin: 5, sMax: 18 });
    shake(18, 60); sfx_boss();
  }

  // Burst projectile
  b.projTimer = (b.projTimer || 2) - dt;
  if (b.projTimer <= 0) {
    b.projTimer = b.phase3 ? .8 : (b.phase2 ? 1.2 : 1.8);
    const count = b.phase3 ? 6 : (b.phase2 ? 4 : 3);
    for (let i = 0; i < count; i++) {
      const ang = b.dir + (i / count - .5) * Math.PI * (b.phase3 ? 2 : 1.2);
      const dv = { v: Math.round(b.atk * .65), crit: false };
      spawnProj(b.x, b.y, Math.cos(ang) * 200, Math.sin(ang) * 200, dv, b.col, 'enemy', { sz: 12, emoji: '💥' });
    }
  }

  if (b.alive) {
    document.getElementById('boss-hp-fill').style.width = Math.max(0, (b.hp / b.maxHp) * 100) + '%';
  }
}

// ── SHAKE ──────────────────────────────────────────────────────
function shake(amt, dur) { G.shakeAmt = Math.max(G.shakeAmt, amt); G.shakeTimer = Math.max(G.shakeTimer, dur * .016); }

// ── DRAWING ────────────────────────────────────────────────────
// Floor themes per floor
const FLOOR_THEMES = [
  { floor: '#1a0f2a', wall: '#0d0816', wall2: '#160c22', pillar: '#220e30', torchCol: '#ff8800', floorLine: 'rgba(100,50,150,.12)', accent: '#6622aa' },
  { floor: '#200808', wall: '#0e0404', wall2: '#1a0606', pillar: '#280a0a', torchCol: '#ff4400', floorLine: 'rgba(150,30,20,.12)', accent: '#aa2200' },
  { floor: '#0a1a1a', wall: '#050d0d', wall2: '#0c1518', pillar: '#0e2020', torchCol: '#00ccff', floorLine: 'rgba(0,100,150,.1)', accent: '#0088aa' },
  { floor: '#0a100a', wall: '#050805', wall2: '#0a120a', pillar: '#0e160e', torchCol: '#00ff88', floorLine: 'rgba(0,150,50,.1)', accent: '#008844' },
  { floor: '#100010', wall: '#080008', wall2: '#120012', pillar: '#1a001a', torchCol: '#cc00ff', floorLine: 'rgba(120,0,150,.12)', accent: '#8800cc' },
];

function drawDungeon() {
  const r = room();
  const th = FLOOR_THEMES[Math.min(G.floorNum - 1, 4)];
  const t = timer;

  // Background fill
  ctx.fillStyle = th.floor;
  ctx.fillRect(0, 0, RW, RH);

  // Floor lines (grid)
  ctx.save();
  ctx.globalAlpha = .04;
  ctx.strokeStyle = '#ffffff';
  ctx.lineWidth = 1;
  for (let x = 0; x <= RW; x += TILE) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, RH); ctx.stroke(); }
  for (let y = 0; y <= RH; y += TILE) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(RW, y); ctx.stroke(); }
  ctx.restore();

  // Tiles
  for (let ty = 0; ty < ROOM_ROWS; ty++) {
    for (let tx = 0; tx < ROOM_COLS; tx++) {
      const ttype = r.tiles[ty][tx];
      const wx = tx * TILE, wy = ty * TILE;

      if (ttype === T.WALL) {
        // Wall
        const wg = ctx.createLinearGradient(wx, wy, wx, wy + TILE);
        wg.addColorStop(0, th.wall2); wg.addColorStop(1, th.wall);
        ctx.fillStyle = wg; ctx.fillRect(wx, wy, TILE, TILE);
        ctx.fillStyle = 'rgba(0,0,0,.4)'; ctx.fillRect(wx, wy + TILE - 4, TILE, 4);
        ctx.fillStyle = 'rgba(255,255,255,.03)'; ctx.fillRect(wx, wy, TILE, 3);
        // Crack
        if ((tx + ty) % 5 === 0) {
          ctx.save(); ctx.globalAlpha = .15; ctx.strokeStyle = '#000'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(wx + 8, wy + 5); ctx.lineTo(wx + 14, wy + 18); ctx.stroke();
          ctx.restore();
        }
      } else if (ttype === T.PILLAR) {
        // Floor underneath
        ctx.fillStyle = th.floor; ctx.fillRect(wx, wy, TILE, TILE);
        // Pillar
        ctx.fillStyle = th.pillar; ctx.beginPath(); ctx.roundRect(wx + 6, wy + 6, TILE - 12, TILE - 12, 3); ctx.fill();
        ctx.fillStyle = 'rgba(255,255,255,.05)'; ctx.beginPath(); ctx.roundRect(wx + 6, wy + 6, TILE - 12, 8, 3); ctx.fill();
        ctx.fillStyle = 'rgba(0,0,0,.3)'; ctx.beginPath(); ctx.roundRect(wx + 6, wy + TILE - 14, TILE - 12, 8, 3); ctx.fill();
      } else if (ttype >= T.DOOR_N) {
        // Door tile - color based on open state
        const isOpen = r.doorsOpen;
        ctx.fillStyle = isOpen ? 'rgba(60,200,100,.15)' : 'rgba(200,60,60,.2)';
        ctx.fillRect(wx, wy, TILE, TILE);
        ctx.fillStyle = isOpen ? '#22cc55' : '#cc2222';
        ctx.font = '12px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(isOpen ? '▷' : '✕', wx + TILE / 2, wy + TILE / 2);
      }
    }
  }

  // Torches on walls (animated)
  for (let tx = 3; tx < ROOM_COLS - 2; tx += 5) {
    drawTorch(tx * TILE + TILE / 2, TILE - 2, th, t);
    drawTorch(tx * TILE + TILE / 2, RH - TILE + 2, th, t);
  }
  for (let ty = 3; ty < ROOM_ROWS - 2; ty += 4) {
    drawTorch(TILE - 2, ty * TILE + TILE / 2, th, t);
    drawTorch(RW - TILE + 2, ty * TILE + TILE / 2, th, t);
  }

  // Room clear indicator
  if (r.cleared && !r.isBoss) {
    ctx.save(); ctx.globalAlpha = .08 + Math.sin(t * 3) * .04;
    ctx.fillStyle = '#22ff88';
    ctx.fillRect(0, 0, RW, RH);
    ctx.restore();
  }

  // Enemy count display
  const alive = liveEnemies().length;
  if (!r.cleared && alive > 0) {
    ctx.save();
    ctx.font = 'bold 11px Noto Sans KR';
    ctx.textAlign = 'center';
    ctx.fillStyle = 'rgba(255,100,100,.6)';
    ctx.fillText(`적 ${alive}명 남음`, RW / 2, 52);
    ctx.restore();
  }
}

function drawTorch(x, y, th, t) {
  const flicker = Math.sin(t * 12 + x) * .4 + Math.cos(t * 7 + y) * .2;
  const fSize = 7 + flicker * 2;
  const fGr = ctx.createRadialGradient(x, y - fSize * .5, 1, x, y, fSize);
  fGr.addColorStop(0, '#ffffffcc'); fGr.addColorStop(.4, th.torchCol + 'dd');
  fGr.addColorStop(1, 'rgba(255,80,0,0)');
  ctx.save(); ctx.globalAlpha = .7 + flicker * .1;
  ctx.fillStyle = fGr; ctx.beginPath(); ctx.arc(x, y - fSize * .5, fSize, 0, Math.PI * 2); ctx.fill();
  const gGr = ctx.createRadialGradient(x, y, 2, x, y, 45);
  gGr.addColorStop(0, th.torchCol + '22'); gGr.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.globalAlpha = .4 + flicker * .1; ctx.fillStyle = gGr; ctx.fillRect(x - 45, y - 45, 90, 90);
  ctx.restore();
}

// ── DRAW PLAYER ───────────────────────────────────────────────
function drawPlayer() {
  const p = G.player;
  if (p.invincible > 0 && Math.floor(timer * 20) % 2 === 0) return; // blink

  ctx.save();
  const aimDir = p.aimDir || 0;
  const isWalking = Math.hypot(p.vx, p.vy) > 10;
  const bounce = isWalking ? Math.abs(Math.sin(p.walkPhase)) * 3 : 0;
  const R = p.radius;

  // Shadow
  ctx.globalAlpha = .2;
  ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.ellipse(p.x, p.y + R + 2, R * .7, 5, 0, 0, Math.PI * 2); ctx.fill();
  ctx.globalAlpha = 1;

  ctx.translate(p.x, p.y - bounce);

  // Glow aura
  if (p.buffTimer > 0 || p.atkAnim > 0) {
    ctx.save();
    ctx.globalAlpha = .3 + Math.sin(timer * 8) * .1;
    ctx.shadowColor = p.col; ctx.shadowBlur = 22;
    ctx.strokeStyle = p.col; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(0, 0, R + 6, 0, Math.PI * 2); ctx.stroke();
    ctx.restore();
  }

  // Hit flash
  if (p.hitFlash > 0) { ctx.filter = `brightness(${2.5 + p.hitFlash * 5}) saturate(0)`; }

  // Body
  const bodyGr = ctx.createRadialGradient(-R * .3, -R * .3, 1, 0, 0, R);
  bodyGr.addColorStop(0, lightenColor(p.col, 40)); bodyGr.addColorStop(1, p.col);
  ctx.fillStyle = bodyGr; ctx.shadowColor = p.col; ctx.shadowBlur = 12;
  ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;

  // Inner highlight
  ctx.fillStyle = 'rgba(255,255,255,.18)';
  ctx.beginPath(); ctx.arc(-R * .25, -R * .3, R * .45, 0, Math.PI * 2); ctx.fill();

  // Direction indicator
  ctx.fillStyle = 'rgba(255,255,255,.8)';
  ctx.beginPath(); ctx.moveTo(Math.cos(aimDir) * R, Math.sin(aimDir) * R);
  ctx.lineTo(Math.cos(aimDir + 2.4) * R * .45, Math.sin(aimDir + 2.4) * R * .45);
  ctx.lineTo(Math.cos(aimDir - 2.4) * R * .45, Math.sin(aimDir - 2.4) * R * .45);
  ctx.closePath(); ctx.fill();

  // Class icon (small)
  ctx.filter = 'none';
  ctx.font = `${R * .9}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(CLASSES[p.clsId].icon, 0, 0);

  ctx.restore();

  // HP bar above player
  if (p.hp < p.maxHp) {
    const bw = 40, bx = p.x - bw / 2, by = p.y - p.radius - 16;
    ctx.fillStyle = 'rgba(0,0,0,.6)'; ctx.fillRect(bx, by, bw, 5);
    const hpPct = Math.max(0, p.hp / p.maxHp);
    ctx.fillStyle = hpPct > .5 ? '#22cc44' : hpPct > .25 ? '#ccaa00' : '#cc2200';
    ctx.fillRect(bx, by, bw * hpPct, 5);
  }
}

function lightenColor(hex, amt) {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.min(255, (n >> 16) + amt);
  const g = Math.min(255, ((n >> 8) & 0xff) + amt);
  const b = Math.min(255, (n & 0xff) + amt);
  return `rgb(${r},${g},${b})`;
}

// ── DRAW ENEMIES ──────────────────────────────────────────────
function drawEnemies() {
  for (const e of enemies()) {
    const alpha = e.dying ? Math.max(0, e.deathTimer / .5) : 1;
    ctx.save(); ctx.globalAlpha = alpha;
    if (e.hitFlash > 0) ctx.filter = `brightness(${2.5 + e.hitFlash * 6}) saturate(0)`;
    if (e.frozen > 0) ctx.filter = 'hue-rotate(200deg) brightness(1.8) saturate(2)';

    // Shadow
    ctx.globalAlpha = alpha * .2; ctx.fillStyle = '#000';
    ctx.beginPath(); ctx.ellipse(e.x, e.y + e.radius + 1, e.radius * .7, 5, 0, 0, Math.PI * 2); ctx.fill();
    ctx.globalAlpha = alpha;

    if (e.drawFn) e.drawFn(ctx, e, timer);
    else drawGenericEnemy(ctx, e, timer);

    ctx.filter = 'none';

    // HP bar
    if (!e.dying && e.hp < e.maxHp) {
      const hpPct = Math.max(0, e.hp / e.maxHp);
      const bw = Math.max(36, e.radius * 2.4);
      const bx = e.x - bw / 2, by = e.y - e.radius - 14;
      ctx.globalAlpha = alpha;
      ctx.fillStyle = 'rgba(0,0,0,.7)'; ctx.fillRect(bx, by, bw, 6);
      ctx.fillStyle = hpPct > .5 ? '#22cc44' : hpPct > .25 ? '#ccaa00' : '#cc2200';
      ctx.fillRect(bx, by, bw * hpPct, 6);
      if (e.frozen > 0) { ctx.fillStyle = 'rgba(100,180,255,.5)'; ctx.fillRect(bx, by, bw, 6); }
      // Name
      if (e.isBoss) {
        ctx.font = 'bold 11px Noto Sans KR'; ctx.textAlign = 'center'; ctx.fillStyle = '#ff3355';
        ctx.fillText(e.name, e.x, by - 4);
      }
    }
    ctx.restore();
  }
}

function drawGenericEnemy(ctx, e, t) {
  const R = e.radius;
  const gr = ctx.createRadialGradient(-R * .3, -R * .3, 1, 0, 0, R);
  gr.addColorStop(0, lightenColor(e.col, 30)); gr.addColorStop(1, e.col);
  ctx.save(); ctx.translate(e.x, e.y);
  ctx.fillStyle = gr; ctx.shadowColor = e.col; ctx.shadowBlur = 8;
  ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = 'rgba(0,0,0,.5)'; ctx.beginPath(); ctx.arc(R * .25, -R * .25, R * .22, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(-R * .25, -R * .25, R * .22, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

function drawSlime(ctx, e, t) {
  const R = e.radius;
  const squash = 1 + Math.sin(t * 6 + e.walkPhase) * .12;
  ctx.save(); ctx.translate(e.x, e.y);
  ctx.scale(squash, 2 - squash);
  const gr = ctx.createRadialGradient(-R * .2, -R * .3, 1, 0, 0, R);
  gr.addColorStop(0, '#88ffaa'); gr.addColorStop(1, e.col);
  ctx.fillStyle = gr; ctx.shadowColor = e.col; ctx.shadowBlur = 10;
  ctx.beginPath(); ctx.ellipse(0, 0, R, R * .85, 0, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = 'rgba(255,255,255,.5)'; ctx.beginPath(); ctx.ellipse(-R * .2, -R * .3, R * .2, R * .13, 0, 0, Math.PI * 2); ctx.fill();
  // Eyes
  ctx.fillStyle = '#001a00'; ctx.beginPath(); ctx.arc(-R * .3, -R * .1, R * .18, 0, Math.PI * 2); ctx.fill(); ctx.beginPath(); ctx.arc(R * .3, -R * .1, R * .18, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

function drawBat(ctx, e, t) {
  const R = e.radius;
  const wingFlap = Math.sin(t * 18 + e.walkPhase) * .4;
  ctx.save(); ctx.translate(e.x, e.y);
  // Wings
  ctx.fillStyle = e.col2 || '#5a2080';
  ctx.beginPath(); ctx.ellipse(-R * 1.8, wingFlap * R, R * 1.2, R * .5, -0.3, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(R * 1.8, wingFlap * R, R * 1.2, R * .5, 0.3, 0, Math.PI * 2); ctx.fill();
  // Body
  const gr = ctx.createRadialGradient(0, 0, 1, 0, 0, R);
  gr.addColorStop(0, lightenColor(e.col, 30)); gr.addColorStop(1, e.col);
  ctx.fillStyle = gr; ctx.beginPath(); ctx.ellipse(0, 0, R, R * 1.1, 0, 0, Math.PI * 2); ctx.fill();
  // Eyes
  ctx.fillStyle = '#ff4400'; ctx.shadowColor = '#ff4400'; ctx.shadowBlur = 6;
  ctx.beginPath(); ctx.arc(-R * .28, -R * .2, R * .2, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(R * .28, -R * .2, R * .2, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();
}

function drawSkeleton(ctx, e, t) {
  const R = e.radius;
  const walk = Math.sin(e.walkPhase) * .15;
  ctx.save(); ctx.translate(e.x, e.y);
  // Legs
  ctx.strokeStyle = '#d4c8a0'; ctx.lineWidth = 3; ctx.lineCap = 'round';
  ctx.save(); ctx.rotate(walk + .5);
  ctx.beginPath(); ctx.moveTo(-R * .25, R * .2); ctx.lineTo(-R * .2, R * .85); ctx.stroke();
  ctx.restore(); ctx.save(); ctx.rotate(-walk - .5);
  ctx.beginPath(); ctx.moveTo(R * .25, R * .2); ctx.lineTo(R * .2, R * .85); ctx.stroke();
  ctx.restore();
  // Body ribs
  ctx.strokeStyle = '#d4c8a0'; ctx.lineWidth = 2;
  for (let i = 0; i < 3; i++) ctx.beginPath(), ctx.arc(0, (-R * .6 + i * R * .28), R * .5, .2, Math.PI - .2), ctx.stroke();
  // Arms
  ctx.save(); ctx.rotate(-walk); ctx.beginPath(); ctx.moveTo(R * .6, -R * .5); ctx.lineTo(R * 1.1, -R * .05); ctx.stroke(); ctx.restore();
  ctx.save(); ctx.rotate(walk); ctx.beginPath(); ctx.moveTo(-R * .6, -R * .5); ctx.lineTo(-R * 1.1, -R * .05); ctx.stroke(); ctx.restore();
  // Skull
  ctx.fillStyle = '#d4c8a0'; ctx.beginPath(); ctx.arc(0, -R * .72, R * .65, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#111'; ctx.beginPath(); ctx.ellipse(-R * .25, -R * .8, R * .22, R * .18, 0, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.ellipse(R * .25, -R * .8, R * .22, R * .18, 0, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = 'rgba(0,220,255,.7)'; ctx.shadowColor = '#00ccff'; ctx.shadowBlur = 6;
  ctx.beginPath(); ctx.arc(-R * .25, -R * .8, R * .12, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(R * .25, -R * .8, R * .12, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();
}

function drawOrc(ctx, e, t) {
  const R = e.radius;
  const walk = Math.sin(e.walkPhase) * .1;
  ctx.save(); ctx.translate(e.x, e.y);
  if (e.charging) { ctx.shadowColor = '#ff8800'; ctx.shadowBlur = 18; }
  // Legs - wide
  ctx.strokeStyle = e.col2 || '#145a32'; ctx.lineWidth = 7; ctx.lineCap = 'round';
  ctx.save(); ctx.rotate(walk + .4); ctx.beginPath(); ctx.moveTo(-R * .4, R * .3); ctx.lineTo(-R * .35, R); ctx.stroke(); ctx.restore();
  ctx.save(); ctx.rotate(-walk - .4); ctx.beginPath(); ctx.moveTo(R * .4, R * .3); ctx.lineTo(R * .35, R); ctx.stroke(); ctx.restore();
  // Body
  const gr = ctx.createRadialGradient(0, -R * .2, 1, 0, 0, R * 1.1);
  gr.addColorStop(0, lightenColor(e.col, 20)); gr.addColorStop(1, e.col);
  ctx.fillStyle = gr; ctx.beginPath(); ctx.ellipse(0, -R * .15, R * .9, R * 1.05, 0, 0, Math.PI * 2); ctx.fill();
  // Arms
  ctx.strokeStyle = e.col; ctx.lineWidth = 8;
  ctx.save(); ctx.rotate(-walk - .2); ctx.beginPath(); ctx.moveTo(R * .8, -R * .4); ctx.lineTo(R * 1.3, R * .2); ctx.stroke(); ctx.restore();
  ctx.save(); ctx.rotate(walk + .2); ctx.beginPath(); ctx.moveTo(-R * .8, -R * .4); ctx.lineTo(-R * 1.3, R * .2); ctx.stroke(); ctx.restore();
  // Head
  ctx.fillStyle = e.col; ctx.beginPath(); ctx.ellipse(0, -R * 1.0, R * .75, R * .65, 0, 0, Math.PI * 2); ctx.fill();
  // Tusks
  ctx.fillStyle = '#eeddcc'; ctx.beginPath(); ctx.moveTo(-R * .35, -R * .6); ctx.lineTo(-R * .55, -R * .2); ctx.lineTo(-R * .2, -R * .55); ctx.fill();
  ctx.beginPath(); ctx.moveTo(R * .35, -R * .6); ctx.lineTo(R * .55, -R * .2); ctx.lineTo(R * .2, -R * .55); ctx.fill();
  // Eyes
  ctx.fillStyle = '#ff3300'; ctx.shadowColor = '#ff3300'; ctx.shadowBlur = 8;
  ctx.beginPath(); ctx.arc(-R * .28, -R * 1.08, R * .22, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(R * .28, -R * 1.08, R * .22, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();
}

function drawMageEnemy(ctx, e, t) {
  const R = e.radius;
  const float = Math.sin(t * 2.5 + e.x) * 4;
  ctx.save(); ctx.translate(e.x, e.y + float);
  // Robe
  const gr = ctx.createRadialGradient(0, 0, 1, 0, 0, R * 1.2);
  gr.addColorStop(0, lightenColor(e.col, 20)); gr.addColorStop(1, e.col);
  ctx.fillStyle = gr; ctx.beginPath(); ctx.moveTo(-R, R * .6); ctx.lineTo(R, R * .6); ctx.lineTo(R * .7, -R * .5); ctx.lineTo(-R * .7, -R * .5); ctx.closePath(); ctx.fill();
  // Orb
  ctx.fillStyle = 'rgba(200,100,255,.9)'; ctx.shadowColor = '#cc44ff'; ctx.shadowBlur = 16;
  ctx.beginPath(); ctx.arc(R * .9, -R * .2, R * .4, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  // Head
  ctx.fillStyle = e.col; ctx.beginPath(); ctx.arc(0, -R * .85, R * .6, 0, Math.PI * 2); ctx.fill();
  // Hat
  ctx.fillStyle = '#330066'; ctx.beginPath(); ctx.moveTo(-R * .7, -R * .7); ctx.lineTo(0, -R * 1.8); ctx.lineTo(R * .7, -R * .7); ctx.closePath(); ctx.fill();
  // Eyes
  ctx.fillStyle = 'rgba(200,100,255,.95)'; ctx.shadowColor = '#cc44ff'; ctx.shadowBlur = 10;
  ctx.beginPath(); ctx.arc(-R * .2, -R * .9, R * .18, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(R * .2, -R * .9, R * .18, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  // Floating runes
  ctx.globalAlpha = .3 + Math.sin(t * 3 + e.x) * .15;
  ctx.font = '11px serif'; ctx.textAlign = 'center'; ctx.fillStyle = '#cc44ff';
  ctx.fillText('⬡', Math.cos(t * 1.8) * R * 1.5, Math.sin(t * 1.8) * R * 1.5 - R * .3);
  ctx.globalAlpha = 1;
  ctx.restore();
}

function drawDemon(ctx, e, t) {
  const R = e.radius;
  const wingFlap = Math.sin(t * 4 + e.walkPhase) * .25;
  ctx.save(); ctx.translate(e.x, e.y);
  // Wings
  ctx.fillStyle = 'rgba(150,0,0,.75)';
  ctx.beginPath(); ctx.moveTo(-R * .3, -R * .4); ctx.lineTo(-R * 2.2, -R * 1.2 + wingFlap * R); ctx.lineTo(-R * 1.5, R * .2); ctx.lineTo(-R * .5, R * .1); ctx.closePath(); ctx.fill();
  ctx.beginPath(); ctx.moveTo(R * .3, -R * .4); ctx.lineTo(R * 2.2, -R * 1.2 + wingFlap * R); ctx.lineTo(R * 1.5, R * .2); ctx.lineTo(R * .5, R * .1); ctx.closePath(); ctx.fill();
  // Body
  const gr = ctx.createRadialGradient(0, 0, 1, 0, 0, R);
  gr.addColorStop(0, '#e05050'); gr.addColorStop(1, e.col);
  ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
  // Chest glow
  ctx.fillStyle = 'rgba(255,0,0,.3)'; ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 12;
  ctx.beginPath(); ctx.arc(0, -R * .1, R * .35, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  // Head
  ctx.fillStyle = e.col; ctx.beginPath(); ctx.arc(0, -R * .9, R * .62, 0, Math.PI * 2); ctx.fill();
  // Horns
  ctx.fillStyle = '#550000'; ctx.beginPath(); ctx.moveTo(-R * .35, -R * 1.3); ctx.quadraticCurveTo(-R * .9, -R * 2.0, -R * .5, -R * 1.7); ctx.lineTo(-R * .2, -R * 1.3); ctx.fill();
  ctx.beginPath(); ctx.moveTo(R * .35, -R * 1.3); ctx.quadraticCurveTo(R * .9, -R * 2.0, R * .5, -R * 1.7); ctx.lineTo(R * .2, -R * 1.3); ctx.fill();
  // Eyes
  ctx.fillStyle = '#ff0000'; ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 12;
  ctx.beginPath(); ctx.arc(-R * .24, -R * .95, R * .2, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.arc(R * .24, -R * .95, R * .2, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.restore();
}

// ── DRAW ITEMS ────────────────────────────────────────────────
function drawItems() {
  for (const it of G.items) {
    if (!it.alive) continue;
    const bob = Math.sin(timer * 5 + it.x) * 3;
    ctx.save();
    ctx.shadowColor = it.type === 'hp' ? '#22ff88' : '#44aaff'; ctx.shadowBlur = 14;
    ctx.font = '20px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(it.type === 'hp' ? '❤️' : '💙', it.x, it.y + bob);
    ctx.globalAlpha = .2 + Math.sin(timer * 4) * .1;
    ctx.strokeStyle = it.type === 'hp' ? '#22ff88' : '#44aaff'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(it.x, it.y + bob, 14, 0, Math.PI * 2); ctx.stroke();
    ctx.shadowBlur = 0; ctx.restore();
  }
}

// ── DRAW PROJECTILES ──────────────────────────────────────────
function drawProjs() {
  for (const pr of G.projectiles) {
    if (!pr.alive) continue;
    ctx.save();
    if (pr.emoji) {
      if (pr.glow) { ctx.shadowColor = pr.col; ctx.shadowBlur = 12; }
      ctx.font = `${pr.sz * 2}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(pr.emoji, pr.x, pr.y);
    } else {
      ctx.fillStyle = pr.col; ctx.shadowColor = pr.col; ctx.shadowBlur = 14;
      ctx.beginPath(); ctx.arc(pr.x, pr.y, pr.sz, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = .35; ctx.shadowBlur = 0;
      ctx.beginPath(); ctx.arc(pr.x - pr.vx * .015, pr.y - pr.vy * .015, pr.sz * .65, 0, Math.PI * 2); ctx.fill();
    }
    ctx.shadowBlur = 0; ctx.restore();
  }
}

// ── MINIMAP ───────────────────────────────────────────────────
function drawMinimap() {
  const mc = document.getElementById('mm-canvas');
  const mctx = mc.getContext('2d');
  mctx.clearRect(0, 0, 120, 90);
  mctx.fillStyle = 'rgba(0,0,0,.6)'; mctx.fillRect(0, 0, 120, 90);

  const rooms = G.rooms;
  const cellW = 22, cellH = 18, padX = 4, padY = 4;

  rooms.forEach((r, i) => {
    if (!r.visited) return;
    const col = i % 3;
    const row = Math.floor(i / 3);
    const rx = padX + col * (cellW + 4);
    const ry = padY + row * (cellH + 4);
    mctx.fillStyle = r.isBoss ? '#ff2244' : (r.cleared ? '#22cc55' : '#4466aa');
    mctx.fillRect(rx, ry, cellW, cellH);
    if (i === G.currentRoomIdx) {
      mctx.strokeStyle = '#fff'; mctx.lineWidth = 2; mctx.strokeRect(rx, ry, cellW, cellH);
    }
    if (r.isBoss && !r.cleared) {
      mctx.font = '10px serif'; mctx.textAlign = 'center'; mctx.fillStyle = '#fff';
      mctx.fillText('⚠', rx + cellW / 2, ry + cellH * .7);
    }
  });

  // Legend
  mctx.font = '8px sans-serif'; mctx.fillStyle = 'rgba(255,255,255,.4)'; mctx.textAlign = 'left';
  mctx.fillText('● 현재', 4, 85);
}

// ── HUD UPDATE ────────────────────────────────────────────────
function updateHUD() {
  if (!G) return;
  const p = G.player;
  document.getElementById('hp-fill').style.width = Math.max(0, (p.hp / p.maxHp) * 100) + '%';
  document.getElementById('hp-txt').textContent = `${Math.ceil(p.hp)}/${p.maxHp}`;
  document.getElementById('mp-fill').style.width = Math.max(0, (p.mp / p.maxMp) * 100) + '%';
  document.getElementById('xp-fill').style.width = Math.min(100, (p.xp / p.xpNext) * 100) + '%';
  document.getElementById('s-lv').textContent = p.level;
  document.getElementById('s-atk').textContent = Math.round(totalAtk(p));
  document.getElementById('s-kills').textContent = p.kills;
  document.getElementById('s-gold').textContent = p.gold;
  document.getElementById('hud-name').textContent = CLASSES[p.clsId].name;

  const r = room();
  const alive = liveEnemies().length;
  document.getElementById('room-lbl').textContent = `B${G.floorNum}F · ${G.currentRoomIdx + 1}/${G.rooms.length}방${r.cleared ? ' ✓' : ` (${alive})`}`;

  // Skills
  const sc = document.getElementById('sk-cont');
  sc.innerHTML = '';
  for (let i = 0; i < p.skills.length; i++) {
    const sk = p.skills[i]; const cd = p.skillCds[i];
    const rdy = cd <= 0 && p.mp >= sk.mp;
    const div = document.createElement('div');
    div.className = 'sk ' + (rdy ? 'ready' : 'cooling');
    div.innerHTML = `<div class="sk-icon">${sk.icon}</div><span class="sk-key">${sk.key}</span>`;
    if (cd > 0) {
      const cdDiv = document.createElement('div'); cdDiv.className = 'sk-cd';
      cdDiv.textContent = cd.toFixed(1); div.appendChild(cdDiv);
    }
    div.title = `${sk.name} [${sk.key}] MP:${sk.mp} CD:${sk.cd}s\n${sk.desc}`;
    sc.appendChild(div);
  }
}

// ── DAMAGE NUMBERS ────────────────────────────────────────────
function showDNum(x, y, v, crit, col) {
  const el = document.createElement('div'); el.className = 'dnum';
  const root = document.getElementById('root');
  const scale = parseFloat(canvas.style.width) / canvas.width;
  const rx = canvas.getBoundingClientRect();
  el.style.cssText = `left:${rx.left + x * scale - 20}px;top:${rx.top + y * scale}px;` +
    `font-size:${crit ? 1.4 : .95}rem;color:${crit ? '#ffff44' : (col || '#fff')};`;
  el.textContent = crit ? v + '!!' : v;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1050);
}

// ── ACHIEVEMENT ───────────────────────────────────────────────
function showAchiev(title, sub) {
  const el = document.getElementById('achiev');
  document.getElementById('ach-title').textContent = title;
  document.getElementById('ach-sub').textContent = sub;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2500);
}

// ── FLOOR TRANSITIONS ─────────────────────────────────────────
function floorClear() {
  if (!G || G.phase !== 'play') return;
  G.phase = 'clear';
  const p = G.player;
  document.getElementById('clear-grid').innerHTML = `
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">점수<b>${p.score}</b></div>`;
  document.getElementById('clear-ov').classList.remove('hidden');
}

function gameOver() {
  if (!G || G.phase !== 'play') return;
  G.phase = 'over'; G.player.alive = false;
  const p = G.player;
  document.getElementById('over-grid').innerHTML = `
    <div class="res-cell">처치 수<b>${p.kills}</b></div>
    <div class="res-cell">레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">골드<b>💰${p.gold}</b></div>
    <div class="res-cell">층<b>B${G.floorNum}F</b></div>`;
  setTimeout(() => document.getElementById('over-ov').classList.remove('hidden'), 900);
  sfx_death();
}

function openShop() {
  document.getElementById('clear-ov').classList.add('hidden');
  buildShop(); document.getElementById('shop-ov').classList.remove('hidden');
}

function buildShop() {
  const p = G.player;
  document.getElementById('shop-gold-lbl').textContent = p.gold;
  const pool = [...SHOP_ITEMS].sort(() => Math.random() - .5).slice(0, 6);
  G.shopStock = pool.map(it => ({ ...it, sold: false, uid: 's' + Math.random(), price: it.price + G.floorNum * 20 }));
  const grid = document.getElementById('shop-grid');
  grid.innerHTML = G.shopStock.map((it, i) => {
    const cant = p.gold < it.price;
    return `<div class="shop-card ${cant ? 'sold' : ''}" onclick="buyItem(${i})">
      <div class="sc-icon">${it.icon}</div>
      <div class="sc-name">${it.name}</div>
      <div class="sc-desc">${it.desc}</div>
      <div class="sc-price">${it.price} 💰</div></div>`;
  }).join('');
}

function buyItem(i) {
  const p = G.player; const it = G.shopStock[i];
  if (!it || it.sold || p.gold < it.price) return;
  p.gold -= it.price; it.sold = true; it.fn(p);
  sfx_buy(); buildShop();
}

function nextFloor() {
  document.getElementById('shop-ov').classList.add('hidden');
  const next = G.floorNum + 1;
  if (next > 5) {
    winGame(); return;
  }
  initGame(G.classId, next, G.player);
}

function winGame() {
  const p = G.player;
  document.getElementById('win-grid').innerHTML = `
    <div class="res-cell">총 처치<b>${p.kills}</b></div>
    <div class="res-cell">최종 레벨<b>Lv${p.level}</b></div>
    <div class="res-cell">최고 콤보<b>${p.maxCombo}HIT</b></div>
    <div class="res-cell">총 점수<b>${p.score}</b></div>`;
  document.getElementById('win-ov').classList.remove('hidden');
}

function retryFloor() {
  document.getElementById('over-ov').classList.add('hidden');
  initGame(G.classId, G.floorNum);
}

function gotoTitle() {
  ['clear-ov', 'over-ov', 'shop-ov', 'win-ov', 'pause-ov', 'lvlup-ov'].forEach(id => document.getElementById(id).classList.add('hidden'));
  document.getElementById('title-ov').classList.remove('hidden');
  document.getElementById('boss-bar').classList.remove('show');
  G = null;
}

// ── LEVEL UP ──────────────────────────────────────────────────
function showLvlUpModal() {
  const picks = document.getElementById('stat-pick');
  picks.innerHTML = `
    <button class="sbtn" onclick="pickStat('hp')">❤️ 최대HP +30</button>
    <button class="sbtn" onclick="pickStat('atk')">⚔️ ATK +8</button>
    <button class="sbtn" onclick="pickStat('def')">🛡️ DEF +5</button>
    <button class="sbtn" onclick="pickStat('spd')">💨 SPD +18</button>
    <button class="sbtn" onclick="pickStat('mp')">💙 최대MP +20</button>
    <button class="sbtn" onclick="pickStat('crit')">⚡ 치명타 +8%</button>`;
  document.getElementById('lvlup-ov').classList.remove('hidden');
}

function pickStat(stat) {
  const p = G.player;
  if (stat === 'hp') { p.maxHp += 30; p.hp = Math.min(p.maxHp, p.hp + 30); }
  else if (stat === 'atk') p.atk += 8;
  else if (stat === 'def') p.def += 5;
  else if (stat === 'spd') p.spd += 18;
  else if (stat === 'mp') { p.maxMp += 20; p.mp = Math.min(p.maxMp, p.mp + 20); }
  else if (stat === 'crit') p.crit = (p.crit || .1) + .08;
  document.getElementById('lvlup-ov').classList.add('hidden');
  G.pendingLvlUp = false;
}

// ── AUDIO ─────────────────────────────────────────────────────
let ACtx = null;
function ensureAudio() { if (!ACtx) try { ACtx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) {} }
function beep(freq, type, dur, vol = .25, del = 0) {
  if (!ACtx) return;
  try {
    const o = ACtx.createOscillator(), g = ACtx.createGain();
    o.connect(g); g.connect(ACtx.destination);
    o.type = type; o.frequency.value = freq;
    const t = ACtx.currentTime + del;
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(vol, t + .005);
    g.gain.exponentialRampToValueAtTime(.001, t + dur);
    o.start(t); o.stop(t + dur + .05);
  } catch (e) {}
}
const sfx_atk = () => { ensureAudio(); beep(280, 'square', .06, .12); };
const sfx_hit = () => { ensureAudio(); beep(150, 'sawtooth', .1, .18); };
const sfx_skill = () => { ensureAudio(); beep(440, 'sine', .18, .3); beep(550, 'sine', .12, .2, .08); };
const sfx_door = () => { ensureAudio(); beep(500, 'sine', .12, .2); beep(650, 'sine', .1, .15, .1); };
const sfx_roomClear = () => { ensureAudio(); [440, 554, 659, 880].forEach((f, i) => beep(f, 'sine', .2, .3, i * .08)); };
const sfx_lvlup = () => { ensureAudio(); [523, 659, 784, 1047].forEach((f, i) => beep(f, 'sine', .3, .35, i * .1)); };
const sfx_clear = () => { ensureAudio(); [523, 659, 784, 523, 659, 784, 1047].forEach((f, i) => beep(f, 'sine', .25, .35, i * .11)); };
const sfx_death = () => { ensureAudio(); for (let i = 0; i < 5; i++) beep(200 - i * 25, 'sawtooth', .22, .28, i * .08); };
const sfx_buy = () => { ensureAudio(); beep(700, 'sine', .18, .25); beep(900, 'sine', .14, .2, .09); };
const sfx_boss = () => { ensureAudio(); for (let i = 0; i < 4; i++) beep(70 + i * 15, 'sawtooth', .45, .45, i * .22); };
const sfx_item = () => { ensureAudio(); beep(800, 'sine', .1, .2); };

// ── MAIN LOOP ─────────────────────────────────────────────────
function loop(ts) {
  const dt = Math.min((ts - lastTs) / 1000, .05);
  lastTs = ts;
  timer += dt;

  if (G && G.phase === 'play' && !G.paused && !G.pendingLvlUp) {
    if (G.hitStop > 0) { G.hitStop -= dt; }
    else {
      updatePlayer(dt);
      updateEnemies(dt);
      updateProjs(dt);
      updateParts(dt);
      updateSlashes(dt);
    }
    if (G.shakeTimer > 0) G.shakeTimer -= dt;
  }

  render();
  updateHUD();
  if (G) drawMinimap();
  flushJ();
  RAF = requestAnimationFrame(loop);
}

function render() {
  ctx.save();
  if (G && G.shakeTimer > 0) {
    const s = G.shakeAmt * G.shakeTimer * .8;
    ctx.translate((Math.random() - .5) * s, (Math.random() - .5) * s);
  }

  ctx.fillStyle = '#06040e'; ctx.fillRect(0, 0, RW, RH);

  if (G && G.phase) {
    drawDungeon();
    drawSlashes();
    drawItems();
    drawProjs();
    drawEnemies();
    drawPlayer();
    drawParts();
  } else {
    // Title idle animation
    drawTitleIdle();
  }

  ctx.restore();
}

function drawTitleIdle() {
  ctx.fillStyle = '#06040e'; ctx.fillRect(0, 0, RW, RH);
  ctx.save(); ctx.globalAlpha = .04 + Math.sin(timer * .8) * .02;
  ctx.font = '900 70px Black Han Sans'; ctx.fillStyle = '#ff6600';
  ctx.textAlign = 'center'; ctx.fillText('던전 런', RW / 2, RH / 2 + 30);
  ctx.restore();
  // Idle particles
  if (Math.random() < .4) spawnParts(Math.random() * RW, Math.random() * RH, { n: 2, col: ['#ff6600', '#ffaa00', '#cc44ff'], glow: true, sMin: 1, sMax: 3, dMin: .01, dMax: .015 });
  updateParts(.016); drawParts();
}

// ── TITLE SCREEN ──────────────────────────────────────────────
function buildTitle() {
  const grid = document.getElementById('char-grid');
  grid.innerHTML = '';
  const mkStars = (n, max = 5) => [...Array(max)].map((_, i) => `<span style="color:${i < n ? '#f5c842' : '#222'}">★</span>`).join('');
  for (const [id, c] of Object.entries(CLASSES)) {
    const div = document.createElement('div'); div.className = 'ccard'; div.id = 'cc-' + id;
    div.onclick = () => {
      selClassId = id;
      document.querySelectorAll('.ccard').forEach(x => x.classList.remove('sel'));
      div.classList.add('sel');
      document.getElementById('start-btn').disabled = false;
      ensureAudio();
    };
    div.innerHTML = `
      <div class="ccard-icon">${c.icon}</div>
      <div class="ccard-name">${c.name}</div>
      <div class="ccard-role">${c.role}</div>
      <div class="ccard-stats">
        <div class="cstat">ATK ${mkStars(c.stars.ATK)}</div>
        <div class="cstat">DEF ${mkStars(c.stars.DEF)}</div>
        <div class="cstat">SPD ${mkStars(c.stars.SPD)}</div>
        <div class="cstat">RNG ${mkStars(c.stars.RNG)}</div>
      </div>
      <div class="ccard-desc">${c.desc}</div>`;
    grid.appendChild(div);
  }
}

function startGame() {
  if (!selClassId) return;
  document.getElementById('title-ov').classList.add('hidden');
  initGame(selClassId, 1);
}

// Boot
buildTitle();
RAF = requestAnimationFrame(loop);

// ── MOBILE TOUCH ──────────────────────────────────────────────
</script>

<!-- 📱 Mobile Controls -->
<style>
#mobile-dpad{display:none;position:fixed;bottom:68px;left:10px;width:130px;height:130px;z-index:999;pointer-events:auto;}
#mobile-atk{display:none;position:fixed;bottom:90px;right:20px;width:60px;height:60px;border-radius:50%;background:rgba(255,80,80,.2);border:2px solid rgba(255,80,80,.5);z-index:999;display:none;align-items:center;justify-content:center;font-size:1.5rem;cursor:pointer;}
.dpad-btn{position:absolute;width:42px;height:42px;background:rgba(245,200,66,.12);border:1px solid rgba(245,200,66,.3);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;color:rgba(245,200,66,.7);cursor:pointer;user-select:none;-webkit-user-select:none;transition:background .1s;}
.dpad-btn:active{background:rgba(245,200,66,.35);}
#dp-u{top:0;left:44px;}#dp-d{bottom:0;left:44px;}#dp-l{top:44px;left:0;}#dp-r{top:44px;right:0;}
@media(pointer:coarse){#mobile-dpad,#mobile-atk{display:flex!important;}}
</style>
<div id="mobile-dpad">
  <div class="dpad-btn" id="dp-u">▲</div>
  <div class="dpad-btn" id="dp-l">◀</div>
  <div class="dpad-btn" id="dp-r">▶</div>
  <div class="dpad-btn" id="dp-d">▼</div>
</div>
<div id="mobile-atk">⚔️</div>
<script>
(function(){
  const map={dp_u:'ArrowUp',dp_d:'ArrowDown',dp_l:'ArrowLeft',dp_r:'ArrowRight'};
  Object.entries(map).forEach(([id,k])=>{
    const el=document.getElementById(id.replace('_','-'));
    if(!el)return;
    el.addEventListener('touchstart',e=>{e.preventDefault();KEYS[k]=true;},{passive:false});
    el.addEventListener('touchend',e=>{e.preventDefault();KEYS[k]=false;},{passive:false});
  });
  const atk=document.getElementById('mobile-atk');
  if(atk){
    atk.addEventListener('touchstart',e=>{e.preventDefault();JKEYS[' ']=true;},{passive:false});
    atk.addEventListener('touchend',e=>{e.preventDefault();},{passive:false});
  }
})();
</script>
</body>
</html>"""

def render():
    st.markdown("""
<style>
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
header{display:none!important;}footer{display:none!important;}
iframe{border:none!important;}
</style>
""", unsafe_allow_html=True)

    st.caption("🎮 WASD/방향키: 이동 | SPACE/클릭: 공격 | Q·E: 스킬 | P: 일시정지 | 적을 모두 처치하면 출구가 열립니다!")
    components.html(GAME_HTML, height=840, scrolling=False)
