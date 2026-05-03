import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>던전 런 REBORN</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Rajdhani:wght@700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --gold:#f5c518;--red:#ff2244;--blue:#3af;--green:#2fc;
  --purple:#c04fff;--orange:#ff7700;--bg:#07050f;
}
html,body{width:100%;height:838px;overflow:hidden;background:var(--bg);font-family:'Noto Sans KR',sans-serif;touch-action:none;}
#root{position:relative;width:100%;height:838px;display:flex;align-items:center;justify-content:center;overflow:hidden;}
#gc{display:block;image-rendering:pixelated;}

/* HUD */
#hud{position:absolute;top:0;left:0;right:0;z-index:50;padding:8px 12px;
  background:linear-gradient(#000a,transparent);display:flex;align-items:center;gap:8px;pointer-events:none;}
.bar-wrap{display:flex;flex-direction:column;gap:3px;}
.bar-row{display:flex;align-items:center;gap:5px;}
.bar-lbl{font-size:10px;color:#666;width:20px;text-align:right;}
.bar-bg{height:10px;background:rgba(255,255,255,.07);border-radius:99px;border:1px solid rgba(255,255,255,.08);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:99px;transition:width .07s;}
#hp-fill{background:linear-gradient(90deg,#7b0000,#dd1122,#ff5566);}
#mp-fill{background:linear-gradient(90deg,#001166,#1144cc,#33aaff);}
#xp-fill{background:linear-gradient(90deg,#224400,#44aa00,#88ff44);}
.bar-txt{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:9px;color:rgba(255,255,255,.65);font-weight:700;}
.stat-box{background:rgba(255,255,255,.05);border:1px solid rgba(245,200,66,.15);border-radius:4px;padding:1px 7px;text-align:center;min-width:38px;}
.sv{font-size:13px;font-weight:900;color:var(--gold);}
.sl{font-size:9px;color:#444;letter-spacing:.5px;}
#timer-box{margin-left:auto;font-family:'Rajdhani',sans-serif;font-size:22px;font-weight:900;color:#fff;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:4px;padding:1px 12px;letter-spacing:2px;}
#wave-lbl{font-family:'Black Han Sans',sans-serif;font-size:11px;color:var(--red);background:rgba(255,0,50,.1);
  border:1px solid rgba(255,0,50,.25);border-radius:3px;padding:2px 10px;letter-spacing:2px;}

/* SKILL BAR */
#skillbar{position:absolute;bottom:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:center;
  gap:5px;padding:6px 10px;background:linear-gradient(transparent,#000a);pointer-events:none;}
.sk{width:52px;height:52px;border-radius:8px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.15);
  display:flex;flex-direction:column;align-items:center;justify-content:center;position:relative;}
.sk.rdy{border-color:rgba(245,200,66,.8);box-shadow:0 0 12px rgba(245,200,66,.3);}
.sk.lock{opacity:.25;}
.sk-ico{font-size:20px;}
.sk-k{position:absolute;bottom:2px;right:4px;font-size:9px;color:#555;}
.sk-cd{position:absolute;inset:0;border-radius:8px;background:rgba(0,0,0,.75);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;color:var(--gold);}
.sk-lvl{position:absolute;top:2px;left:4px;font-size:9px;color:var(--green);font-weight:900;}

/* KILL COUNTER */
#killbar{position:absolute;top:60px;right:12px;z-index:50;text-align:right;pointer-events:none;}
#kill-count{font-family:'Black Han Sans',sans-serif;font-size:20px;color:#fff;}
#kill-sub{font-size:10px;color:#444;}
#wave-progress-wrap{width:120px;height:5px;background:rgba(255,255,255,.07);border-radius:99px;margin-top:4px;overflow:hidden;}
#wave-progress{height:100%;background:var(--red);border-radius:99px;transition:width .1s;}

/* DAMAGE NUMBERS */
.dnum{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;
  animation:dUp .9s ease forwards;z-index:300;text-shadow:1px 1px 4px rgba(0,0,0,.9);}
@keyframes dUp{0%{opacity:1;transform:translateY(0) scale(1);}40%{opacity:1;transform:translateY(-30px) scale(1.1);}100%{opacity:0;transform:translateY(-70px) scale(.7);}}

/* HIT VIGNETTE */
#vignette{position:absolute;inset:0;pointer-events:none;z-index:80;opacity:0;
  background:radial-gradient(ellipse at center,transparent 40%,rgba(255,0,30,.5) 100%);transition:opacity .08s;}

/* LEVEL UP */
#lvlup{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
  background:rgba(0,0,0,.88);display:none;}
.lvlup-box{background:rgba(10,8,22,.98);border:1px solid rgba(245,200,66,.3);border-radius:14px;padding:30px;width:680px;max-width:96vw;}
.lvlup-title{font-family:'Black Han Sans',sans-serif;font-size:28px;color:var(--gold);text-align:center;letter-spacing:4px;margin-bottom:6px;}
.lvlup-sub{font-size:11px;color:#333;text-align:center;margin-bottom:20px;letter-spacing:2px;}
.cards-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
.ucard{width:145px;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.1);border-radius:10px;
  padding:14px 10px;cursor:pointer;transition:all .18s;text-align:center;}
.ucard:hover{border-color:rgba(245,200,66,.7);background:rgba(245,200,66,.07);transform:translateY(-4px);box-shadow:0 8px 30px rgba(245,200,66,.15);}
.uc-ico{font-size:28px;margin-bottom:8px;}
.uc-name{font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--gold);letter-spacing:1px;}
.uc-desc{font-size:10px;color:#444;margin-top:5px;line-height:1.5;}
.uc-type{font-size:10px;margin-top:4px;padding:2px 8px;border-radius:99px;display:inline-block;}
.uc-type.weapon{background:rgba(255,119,0,.15);color:#ff7700;}
.uc-type.passive{background:rgba(0,170,255,.1);color:#3af;}
.uc-type.active{background:rgba(0,255,180,.1);color:#2fc;}

/* BOSS ANNOUNCE */
#boss-announce{position:absolute;top:40%;left:50%;transform:translate(-50%,-50%);z-index:150;
  display:none;text-align:center;pointer-events:none;}
.ba-wave{font-family:'Black Han Sans',sans-serif;font-size:48px;color:var(--red);
  text-shadow:0 0 40px rgba(255,0,50,1),0 0 80px rgba(255,0,50,.5);letter-spacing:6px;
  animation:baPulse 2s forwards;}
.ba-name{font-size:18px;color:#ff7777;letter-spacing:4px;margin-top:8px;animation:baPulse 2s .3s forwards;}
@keyframes baPulse{0%,100%{opacity:0;}30%,70%{opacity:1;}}

/* BOSS HP BAR */
#boss-hpbar{position:absolute;top:62px;left:50%;transform:translateX(-50%);width:360px;z-index:50;
  pointer-events:none;opacity:0;transition:opacity .3s;}
#boss-hpbar.show{opacity:1;}
#boss-name-txt{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:12px;color:var(--red);
  margin-bottom:3px;letter-spacing:2px;text-shadow:0 0 12px rgba(255,0,50,.6);}
#boss-hp-bg{height:12px;background:rgba(255,255,255,.06);border-radius:2px;border:1px solid rgba(255,50,70,.3);overflow:hidden;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);transition:width .08s;}

/* GAME OVER / WIN */
#result-ov{position:absolute;inset:0;z-index:250;display:none;align-items:center;justify-content:center;
  background:rgba(0,0,0,.92);}
.res-box{background:rgba(10,8,22,.99);border:1px solid rgba(255,255,255,.1);border-radius:14px;padding:32px 40px;
  min-width:340px;text-align:center;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:32px;letter-spacing:4px;margin-bottom:14px;}
.res-stats{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:14px 0;text-align:left;}
.rs{font-size:12px;color:#555;display:flex;justify-content:space-between;}
.rs b{color:var(--gold);}
.res-btn{padding:10px 28px;border:none;border-radius:5px;cursor:pointer;font-family:'Black Han Sans',sans-serif;
  font-size:14px;letter-spacing:3px;margin:4px;transition:all .18s;}
.res-btn:hover{transform:translateY(-2px);filter:brightness(1.15);}
.btn-r{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-t{background:rgba(255,255,255,.08);color:#888;border:1px solid rgba(255,255,255,.12);}

/* TITLE */
#title-ov{position:absolute;inset:0;z-index:250;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:rgba(7,5,15,.97);gap:0;}
.game-logo{font-family:'Black Han Sans',sans-serif;font-size:52px;letter-spacing:8px;
  background:linear-gradient(135deg,#ff4400,#ff9900,#ffdd00);-webkit-background-clip:text;
  -webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 30px rgba(255,150,0,.4));
  margin-bottom:4px;}
.game-sub{font-family:'Rajdhani',sans-serif;font-size:14px;color:#333;letter-spacing:10px;margin-bottom:32px;}
.char-grid{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap;justify-content:center;}
.ccard{width:140px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.08);border-radius:12px;
  padding:16px 12px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard:hover,.ccard.sel{border-color:rgba(245,200,66,.7);background:rgba(245,200,66,.06);
  transform:translateY(-5px);box-shadow:0 10px 35px rgba(245,200,66,.15);}
.ccard-ico{font-size:32px;margin-bottom:8px;}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--gold);letter-spacing:2px;}
.ccard-role{font-size:10px;color:#333;margin-top:2px;}
.ccard-desc{font-size:10px;color:#2a2a3a;margin-top:8px;line-height:1.6;}
.cstar{font-size:10px;}
.cstat-row{display:grid;grid-template-columns:1fr 1fr;gap:3px;margin:8px 0;}
.cs{font-size:10px;color:#333;}
.start-btn{padding:14px 60px;background:linear-gradient(135deg,#7a2e00,#ff5500);border:none;border-radius:6px;
  color:#fff;font-family:'Black Han Sans',sans-serif;font-size:15px;letter-spacing:5px;
  cursor:pointer;box-shadow:0 0 28px rgba(255,100,0,.35);transition:all .2s;}
.start-btn:hover{transform:scale(1.05);filter:brightness(1.15);}
.start-btn:disabled{opacity:.2;cursor:default;transform:none;}
.tut{font-size:10px;color:#1e1e2e;margin-top:14px;text-align:center;line-height:2.2;letter-spacing:.5px;}

/* COMBO */
#combo{position:absolute;bottom:68px;right:14px;text-align:right;pointer-events:none;
  opacity:0;transition:opacity .3s;z-index:60;}

/* RELIC SELECT OVERLAY */
#relic-overlay{position:absolute;inset:0;z-index:260;display:none;align-items:center;justify-content:center;
  background:rgba(0,0,0,.88);}
.relic-box{background:rgba(10,8,22,.98);border:1px solid rgba(245,200,66,.4);border-radius:14px;padding:28px 24px;text-align:center;max-width:520px;width:96vw;}
.relic-title{font-family:'Black Han Sans',sans-serif;font-size:22px;color:#ffcc00;letter-spacing:4px;margin-bottom:4px;}
.relic-sub{font-size:10px;color:#554400;margin-bottom:18px;letter-spacing:2px;}
.relic-row{display:flex;gap:12px;justify-content:center;}
.rcard{width:140px;background:rgba(255,255,255,.03);border:1px solid rgba(245,200,66,.2);border-radius:10px;
  padding:16px 10px;cursor:pointer;transition:all .18s;text-align:center;}
.rcard:hover{border-color:rgba(245,200,66,.8);background:rgba(245,200,66,.08);transform:translateY(-4px);
  box-shadow:0 10px 30px rgba(245,200,66,.15);}
.rcard-ico{font-size:30px;margin-bottom:8px;}
.rcard-name{font-family:'Black Han Sans',sans-serif;font-size:12px;color:var(--gold);letter-spacing:1px;}
.rcard-desc{font-size:10px;color:#443300;margin-top:5px;line-height:1.5;}
#combo-n{font-family:'Black Han Sans',sans-serif;font-size:44px;color:var(--gold);
  text-shadow:0 0 22px rgba(245,200,66,.8),2px 2px 0 rgba(0,0,0,.8);line-height:1;}
#combo-l{font-size:10px;color:#ff8800;letter-spacing:4px;}

/* ACHIEV TOAST */
#toast{position:absolute;top:68px;left:50%;transform:translateX(-50%) translateY(-90px);
  background:rgba(20,15,5,.97);border:1px solid rgba(245,200,66,.5);border-radius:6px;
  padding:8px 20px;display:flex;align-items:center;gap:10px;z-index:300;pointer-events:none;
  box-shadow:0 4px 20px rgba(245,200,66,.25);transition:transform .3s;}
#toast.show{transform:translateX(-50%) translateY(0);}
#toast-ico{font-size:18px;}
#toast-t{font-size:11px;color:var(--gold);font-weight:700;}
#toast-s{font-size:9px;color:#775500;}

/* WEAPON UNLOCKED BANNER */
#unlock-banner{position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);z-index:160;
  display:none;text-align:center;pointer-events:none;}
.ub-inner{background:rgba(10,8,22,.97);border:1px solid rgba(245,200,66,.4);border-radius:12px;
  padding:18px 32px;animation:ubAnim 2.5s forwards;}
.ub-ico{font-size:36px;margin-bottom:4px;}
.ub-name{font-family:'Black Han Sans',sans-serif;font-size:18px;color:var(--gold);letter-spacing:3px;}
.ub-desc{font-size:10px;color:#665500;margin-top:4px;}
@keyframes ubAnim{0%{opacity:0;transform:scale(.8);}15%,75%{opacity:1;transform:scale(1);}100%{opacity:0;transform:scale(.95);}}

#ctrl-bar{position:absolute;top:0;left:0;right:0;z-index:200;background:rgba(0,0,0,0.82);backdrop-filter:blur(4px);display:flex;justify-content:center;align-items:center;gap:16px;padding:5px 12px;font-size:10px;color:#778;letter-spacing:1px;flex-wrap:wrap;border-bottom:1px solid rgba(255,255,255,0.06);}
#ctrl-bar span{color:#aab;}
#ctrl-bar b{color:#ffcc44;font-weight:700;}
</style>
</head>
<body>
  <div id="ctrl-bar">
    <span><b>W A S D</b> / 방향키 이동</span>
    <span>|</span>
    <span><b>Q</b> 돌진  <b>E</b> 폭발  <b>R</b> 시간정지</span>
    <span>|</span>
    <span>자동 공격</span>
  </div>
<div id="root">
  <canvas id="gc"></canvas>

  <div id="hud">
    <div id="hud-name" style="font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--gold);letter-spacing:2px;white-space:nowrap;">—</div>
    <div class="bar-wrap">
      <div class="bar-row"><span class="bar-lbl">HP</span><div class="bar-bg" style="width:140px"><div class="bar-fill" id="hp-fill"></div><div class="bar-txt" id="hp-txt"></div></div></div>
      <div class="bar-row"><span class="bar-lbl">MP</span><div class="bar-bg" style="width:140px"><div class="bar-fill" id="mp-fill"></div></div></div>
      <div class="bar-row"><span class="bar-lbl">XP</span><div class="bar-bg" style="width:100px;height:7px"><div class="bar-fill" id="xp-fill"></div></div></div>
    </div>
    <div class="stat-box"><div class="sv" id="s-lv">1</div><div class="sl">LV</div></div>
    <div class="stat-box"><div class="sv" id="s-atk" style="color:#ff7755">0</div><div class="sl">ATK</div></div>
    <div class="stat-box"><div class="sv" id="s-kill" style="color:#fff">0</div><div class="sl">KILL</div></div>
    <div class="stat-box"><div class="sv" id="s-gold" style="color:var(--gold)">0</div><div class="sl">💰</div></div>
    <div id="wave-lbl">WAVE 1</div>
    <div id="timer-box">00:00</div>
  </div>

  <div id="killbar">
    <div id="kill-count">0 / 0</div>
    <div id="kill-sub">이번 웨이브</div>
    <div id="wave-progress-wrap"><div id="wave-progress" style="width:0%"></div></div>
  </div>

  <div id="boss-hpbar">
    <div id="boss-name-txt">BOSS</div>
    <div id="boss-hp-bg"><div id="boss-hp-fill" style="width:100%"></div></div>
  </div>

  <div id="skillbar"><div id="sk-cont" style="display:flex;gap:5px;"></div></div>

  <div id="combo"><div id="combo-n">0</div><div id="combo-l">COMBO</div></div>

  <div id="vignette"></div>

  <div id="boss-announce">
    <div class="ba-wave" id="ba-wave">BOSS!</div>
    <div class="ba-name" id="ba-name">—</div>
  </div>

  <div id="toast"><div id="toast-ico">🏆</div><div><div id="toast-t">—</div><div id="toast-s">—</div></div></div>

  <div id="unlock-banner"><div class="ub-inner"><div class="ub-ico" id="ub-ico">⚔️</div><div class="ub-name" id="ub-name">새 무기 획득!</div><div class="ub-desc" id="ub-desc">—</div></div></div>

  <div id="relic-overlay">
    <div class="relic-box">
      <div class="relic-title">⚗️ 유물 선택</div>
      <div class="relic-sub">보스 처치 보상 — 3개 중 1개를 선택하세요</div>
      <div class="relic-row" id="relic-cards"></div>
    </div>
  </div>

  <div id="lvlup">
    <div class="lvlup-box">
      <div class="lvlup-title">⬆ LEVEL UP!</div>
      <div class="lvlup-sub">능력치를 선택하세요</div>
      <div class="cards-row" id="lvlup-cards"></div>
    </div>
  </div>

  <div id="result-ov" style="display:none">
    <div class="res-box">
      <div class="res-title" id="res-title">—</div>
      <div class="res-stats" id="res-stats"></div>
      <div style="margin-top:16px;">
        <button class="res-btn btn-r" onclick="retryGame()">다시 시작 ↺</button>
        <button class="res-btn btn-t" onclick="gotoTitle()">타이틀로</button>
      </div>
    </div>
  </div>

  <div id="title-ov">
    <div class="game-logo">던전 런</div>
    <div class="game-sub">SURVIVORS · REBORN</div>
    <div class="char-grid" id="char-grid"></div>
    <button class="start-btn" id="start-btn" disabled onclick="startGame()">탐험 시작 ▶</button>
    <div class="tut">
      WASD / 방향키로 이동 &nbsp;|&nbsp; 자동 공격 &nbsp;|&nbsp; Q·E·R 스킬 사용<br>
      레벨업할 때마다 무기/패시브를 획득하고 강화됩니다
    </div>
  </div>
</div>

<script>
'use strict';
// ══════════════════════════════════════════════════════════════
//  던전 런 REBORN  — 뱀서라이크 완전 리빌드 v1.0
//  자동공격 + 스킬 선택 + 무기 합성 + 웨이브 보스
// ══════════════════════════════════════════════════════════════

const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');

// ── RESPONSIVE ──────────────────────────────────────────────
let GW = 800, GH = 560, scale = 1;
function resize() {
  const root = document.getElementById('root');
  const rw = root.clientWidth||window.innerWidth||800, rh = root.clientHeight||window.innerHeight||560;
  scale = Math.min(rw / GW, rh / GH);
  canvas.width = GW; canvas.height = GH;
  canvas.style.width = (GW * scale) + 'px';
  canvas.style.height = (GH * scale) + 'px';
}
resize();
window.addEventListener('resize', resize);
setTimeout(resize,100);setTimeout(resize,500);

// ── INPUT ──────────────────────────────────────────────────
const KEYS = {}, JKEYS = {};
let MOUSE = { x: GW / 2, y: GH / 2, down: false, clicked: false };
canvas.addEventListener('mousemove', e => {
  const r = canvas.getBoundingClientRect();
  MOUSE.x = (e.clientX - r.left) / scale;
  MOUSE.y = (e.clientY - r.top) / scale;
});
canvas.addEventListener('mousedown', () => { MOUSE.down = true; MOUSE.clicked = true; });
canvas.addEventListener('mouseup', () => MOUSE.down = false);
window.addEventListener('keydown', e => {
  if (!KEYS[e.code]) { KEYS[e.code] = true; JKEYS[e.code] = true; }
  if (['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code)) e.preventDefault();
  if (e.code === 'KeyQ') { JKEYS['Q'] = true; }
  if (e.code === 'KeyE') { JKEYS['E'] = true; }
  if (e.code === 'KeyR') { JKEYS['R'] = true; }
});
window.addEventListener('keyup', e => { KEYS[e.code] = false; });
function flushJ() { for (const k in JKEYS) delete JKEYS[k]; MOUSE.clicked = false; }

// ── PARTICLES ──────────────────────────────────────────────
const PARTS = [];
function spawnP(x, y, o = {}) {
  const n = o.n || 8;
  for (let i = 0; i < n; i++) {
    const a = (o.dir || 0) + (Math.random() - .5) * (o.spread || Math.PI * 2);
    const s = (o.sMin || 1) + Math.random() * (o.sMax || 5);
    const cols = Array.isArray(o.col) ? o.col : [o.col || '#fff'];
    const col = cols[Math.floor(Math.random() * cols.length)];
    PARTS.push({
      x, y, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
      life: 1, decay: (o.dMin || .02) + Math.random() * (o.dMax || .03),
      col, sz: (o.szMin || 2) + Math.random() * (o.szMax || 5),
      glow: o.glow || false,
      rot: Math.random() * Math.PI * 2, rotV: (Math.random() - .5) * .25,
      sq: o.sq || false,
    });
  }
}
function tickP(dt) {
  for (let i = PARTS.length - 1; i >= 0; i--) {
    const p = PARTS[i];
    p.x += p.vx * dt * 60; p.y += p.vy * dt * 60;
    p.vx *= .91; p.vy *= .91;
    p.life -= p.decay * dt * 60;
    p.rot += p.rotV;
    if (p.life <= 0) PARTS.splice(i, 1);
  }
}
function drawP() {
  ctx.save();
  for (const p of PARTS) {
    ctx.globalAlpha = Math.max(0, p.life);
    if (p.glow) { ctx.shadowColor = p.col; ctx.shadowBlur = p.sz * 3; }
    ctx.fillStyle = p.col;
    if (p.sq) {
      ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
      ctx.fillRect(-p.sz / 2, -p.sz / 2, p.sz, p.sz); ctx.restore();
    } else {
      ctx.beginPath(); ctx.arc(p.x, p.y, p.sz, 0, Math.PI * 2); ctx.fill();
    }
    if (p.glow) ctx.shadowBlur = 0;
  }
  ctx.globalAlpha = 1; ctx.restore();
}

// Slashes
const SLASHES = [];
function spawnSlash(x, y, ang, len, col, dur = 12) {
  SLASHES.push({ x, y, ang, len, col, life: 1, decay: 1 / dur });
}
function tickSlashes(dt) {
  for (let i = SLASHES.length - 1; i >= 0; i--) {
    SLASHES[i].life -= SLASHES[i].decay * dt * 60;
    if (SLASHES[i].life <= 0) SLASHES.splice(i, 1);
  }
}
function drawSlashes() {
  for (const s of SLASHES) {
    ctx.save(); ctx.globalAlpha = Math.max(0, s.life) * .85;
    ctx.strokeStyle = s.col; ctx.shadowColor = s.col; ctx.shadowBlur = 10;
    ctx.lineWidth = 2.5 * (s.life + .3); ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(s.x - Math.cos(s.ang) * s.len * .4, s.y - Math.sin(s.ang) * s.len * .4);
    ctx.lineTo(s.x + Math.cos(s.ang) * s.len, s.y + Math.sin(s.ang) * s.len);
    ctx.stroke(); ctx.shadowBlur = 0; ctx.restore();
  }
}

// Shockwaves (FIXED VARIABLE NAME)
const SHOCKWAVES = [];
function spawnWave(x, y, col, maxR = 120) {
  SHOCKWAVES.push({ x, y, col, r: 5, maxR, life: 1, speed: 6 });
}
function tickWaves(dt) {
  for (let i = SHOCKWAVES.length - 1; i >= 0; i--) {
    const w = SHOCKWAVES[i];
    w.r += w.speed * dt * 60; w.life -= .04 * dt * 60;
    if (w.life <= 0 || w.r > w.maxR) SHOCKWAVES.splice(i, 1);
  }
}
function drawWaves() {
  for (const w of SHOCKWAVES) {
    ctx.save(); ctx.globalAlpha = Math.max(0, w.life) * .55;
    ctx.strokeStyle = w.col; ctx.shadowColor = w.col; ctx.shadowBlur = 8;
    ctx.lineWidth = 2.5 * w.life;
    ctx.beginPath(); ctx.arc(w.x, w.y, w.r, 0, Math.PI * 2); ctx.stroke();
    ctx.shadowBlur = 0; ctx.restore();
  }
}

// Projectiles
const PROJS = [];
function spawnProj(x, y, vx, vy, dmg, col, owner, opts = {}) {
  PROJS.push({ x, y, vx, vy, dmg, col, owner, alive: true,
    life: opts.life || 2.2, sz: opts.sz || 8,
    pierce: opts.pierce || 0, pierceHit: [],
    explode: opts.explode || false,
    homing: opts.homing || false,
    emoji: opts.emoji || null,
    trail: opts.trail || false,
    trailTimer: 0,
  });
}

// ── CLASSES ───────────────────────────────────────────────
const CLASSES = {
  warrior: {
    name: '전사', role: '근접 탱커', icon: '⚔️',
    col: '#e74c3c', hp: 240, mp: 100, atk: 38, def: 18, spd: 195, radius: 16,
    atkRange: 90, atkCd: .42,
    stars: { '공격':4,'방어':5,'속도':3,'사거리':2 },
    desc: '높은 체력·방어. 근접 광역 특화.',
  },
  mage: {
    name: '마법사', role: '원소 마법사', icon: '🔮',
    col: '#9b59b6', hp: 130, mp: 280, atk: 68, def: 5, spd: 175, radius: 14,
    atkRange: 350, atkCd: .55,
    stars: { '공격':5,'방어':1,'속도':3,'사거리':5 },
    desc: '초강력 원거리 마법. 폭발 딜.',
  },
  archer: {
    name: '궁수', role: '전술 사수', icon: '🏹',
    col: '#27ae60', hp: 165, mp: 150, atk: 50, def: 8, spd: 235, radius: 14,
    atkRange: 330, atkCd: .28,
    stars: { '공격':4,'방어':2,'속도':5,'사거리':4 },
    desc: '초고속 연사. 이동속도 1위.',
  },
  ninja: {
    name: '닌자', role: '암살자', icon: '🌀',
    col: '#2c3e50', hp: 155, mp: 180, atk: 55, def: 6, spd: 280, radius: 13,
    atkRange: 75, atkCd: .2,
    stars: { '공격':5,'방어':2,'속도':5,'사거리':2 },
    desc: '최고 속도·치명타. 순간이동 암습.',
  },
};

// ── WEAPONS (레벨업에서 획득/강화) ────────────────────────
const WEAPON_DEFS = {
  // 기본 무기 (클래스별)
  sword:    { name:'강화 검', icon:'⚔️', type:'weapon', desc:'전방 근접 타격', maxLv:8 },
  fireball: { name:'파이어볼', icon:'🔥', type:'weapon', desc:'추적 화염탄 발사', maxLv:8 },
  arrow:    { name:'관통 화살', icon:'🏹', type:'weapon', desc:'전방 관통 화살', maxLv:8 },
  shuriken: { name:'수리검', icon:'💫', type:'weapon', desc:'전방위 수리검', maxLv:8 },
  // 추가 획득 무기
  axe:      { name:'도끼 투척', icon:'🪓', type:'weapon', desc:'느리지만 강력한 도끼', maxLv:8 },
  lightning:{ name:'번개 사슬', icon:'⚡', type:'weapon', desc:'연쇄 번개 공격', maxLv:8 },
  holy:     { name:'성스러운 빛', icon:'✨', type:'weapon', desc:'HP를 회복하는 성광', maxLv:8 },
  tornado:  { name:'토네이도', icon:'🌪️', type:'weapon', desc:'주변 회전 공격', maxLv:8 },
  // 패시브
  armor:    { name:'강화 갑옷', icon:'🛡️', type:'passive', desc:'방어력 +12', maxLv:5 },
  boots:    { name:'질풍 부츠', icon:'👟', type:'passive', desc:'이동속도 +20%', maxLv:5 },
  magnet:   { name:'자석 장갑', icon:'🧲', type:'passive', desc:'아이템 흡수 범위 +100%', maxLv:5 },
  amulet:   { name:'크리 목걸이', icon:'💍', type:'passive', desc:'치명타 +15%', maxLv:5 },
  vampire:  { name:'흡혈 반지', icon:'🩸', type:'passive', desc:'처치 시 HP 회복', maxLv:5 },
  // 스킬
  dash:     { name:'공간 도약', icon:'💨', type:'active', key:'Q', desc:'전방으로 돌진+무적', maxLv:5 },
  nova:     { name:'마법 폭발', icon:'💥', type:'active', key:'E', desc:'전방위 마법 폭발', maxLv:5 },
  timeStop: { name:'시간 정지', icon:'⏱️', type:'active', key:'R', desc:'3초 간 모든 적 정지', maxLv:3 },
};

// ── RELIC SYSTEM (보스 처치 시 유물 3개 중 1개 선택) ─────
const RELIC_POOL = [
  { id:'r_atk',    name:'피의 검',     emoji:'🗡️',  desc:'공격력 +25%',          apply: p => { p.atk = Math.round(p.atk * 1.25); } },
  { id:'r_hp',     name:'철의 심장',   emoji:'❤️',  desc:'최대 HP +80',           apply: p => { p.maxHp += 80; p.hp = Math.min(p.hp + 80, p.maxHp); } },
  { id:'r_spd',    name:'바람의 신발', emoji:'👟',  desc:'이동속도 +30%',         apply: p => { p.spd = Math.round(p.spd * 1.30); } },
  { id:'r_vamp',   name:'흡혈의 반지', emoji:'💍',  desc:'처치 시 HP+8 회복',     apply: p => { p.passives.vampire = (p.passives.vampire||0) + 2; } },
  { id:'r_gold',   name:'황금 주머니', emoji:'💰',  desc:'골드 +250 즉시 획득',   apply: p => { p.gold += 250; } },
  { id:'r_range',  name:'독수리 눈',   emoji:'🦅',  desc:'공격 사거리 +30%',      apply: p => { p.atkRange = Math.round((p.atkRange||200) * 1.30); } },
  { id:'r_xp',     name:'고대 서적',   emoji:'📚',  desc:'XP 획득 +40%',          apply: p => { p._xpBonus = (p._xpBonus||1) * 1.40; } },
  { id:'r_crit',   name:'예리한 날',   emoji:'⚡',  desc:'치명타율 +25%',         apply: p => { p.passives.crit = Math.min(95, ((p.passives.crit||0) + 25)); } },
  { id:'r_mp',     name:'마나의 돌',   emoji:'🔮',  desc:'MP 최대치 +120',        apply: p => { p.maxMp += 120; p.mp = Math.min(p.mp + 120, p.maxMp); } },
  { id:'r_tradeoff',name:'악마의 계약',emoji:'😈',  desc:'공격력 +40% / 최대HP -20%', apply: p => { p.atk = Math.round(p.atk * 1.40); p.maxHp = Math.max(30, Math.round(p.maxHp * 0.80)); p.hp = Math.min(p.hp, p.maxHp); } },
  { id:'r_shield', name:'수호의 방패', emoji:'🛡️',  desc:'방어력 +20',            apply: p => { p.def = (p.def||0) + 20; } },
  { id:'r_nova',   name:'폭발의 룬',   emoji:'💥',  desc:'마법 폭발 데미지 +50%', apply: p => { p._novaBonus = (p._novaBonus||1) * 1.50; } },
];

function showRelicChoice() {
  if (!G || G.phase !== 'play') return;
  G.paused = true;
  // 이미 획득한 유물 제외한 풀에서 3개 랜덤 선택
  const available = RELIC_POOL.filter(r => !G.player.relics.includes(r.id));
  const shuffled = available.sort(() => Math.random() - .5).slice(0, Math.min(3, available.length));
  if (!shuffled.length) { G.paused = false; return; }

  const overlay = document.getElementById('relic-overlay');
  const cards = document.getElementById('relic-cards');
  cards.innerHTML = shuffled.map((r, i) => `
    <div class="rcard" onclick="pickRelic(${i})">
      <div class="rcard-ico">${r.emoji}</div>
      <div class="rcard-name">${r.name}</div>
      <div class="rcard-desc">${r.desc}</div>
    </div>`).join('');
  overlay.dataset.relics = JSON.stringify(shuffled.map(r => r.id));
  overlay.style.display = 'flex';
}

function pickRelic(idx) {
  const overlay = document.getElementById('relic-overlay');
  const ids = JSON.parse(overlay.dataset.relics || '[]');
  const rid = ids[idx];
  const relic = RELIC_POOL.find(r => r.id === rid);
  if (!relic || !G) return;
  relic.apply(G.player);
  G.player.relics.push(rid);
  overlay.style.display = 'none';
  G.paused = false;
  // 유물 획득 토스트
  showToast(relic.emoji, `유물 획득: ${relic.name}`, relic.desc);
  sfx_lvlup();
}

// ── ENEMY TYPES ──────────────────────────────────────────
const ETYPES = {
  slime:    { name:'슬라임',   col:'#2ecc71', col2:'#1a8a4a', radius:18, baseHp:60,  baseAtk:8,  baseSpd:55,  xp:12, gold:4,  ai:'bounce', draw:drawSlime },
  bat:      { name:'박쥐',     col:'#9b59b6', col2:'#5a2080', radius:11, baseHp:38,  baseAtk:12, baseSpd:155, xp:16, gold:5,  ai:'erratic', draw:drawBat },
  skeleton: { name:'해골',     col:'#ecf0f1', col2:'#aaa',    radius:15, baseHp:75,  baseAtk:15, baseSpd:88,  xp:22, gold:8,  ai:'ranged', draw:drawSkeleton },
  orc:      { name:'오크',     col:'#27ae60', col2:'#145a32', radius:23, baseHp:150, baseAtk:22, baseSpd:82,  xp:38, gold:16, ai:'charge', draw:drawOrc },
  mageE:    { name:'마법사',   col:'#8e44ad', col2:'#4a0080', radius:15, baseHp:85,  baseAtk:28, baseSpd:72,  xp:32, gold:14, ai:'mage', draw:drawMageE },
  demon:    { name:'악마',     col:'#c0392b', col2:'#7b241c', radius:20, baseHp:135, baseAtk:26, baseSpd:98,  xp:48, gold:20, ai:'flank', draw:drawDemon },
  ghost:    { name:'유령',     col:'#bdc3c7', col2:'#7f8c8d', radius:17, baseHp:65,  baseAtk:20, baseSpd:120, xp:28, gold:12, ai:'phase', draw:drawGhost },
  golem:    { name:'골렘',     col:'#7f8c8d', col2:'#5d6d7e', radius:28, baseHp:350, baseAtk:35, baseSpd:50,  xp:80, gold:35, ai:'charge', draw:drawGolem },
  // BOSSES
  spider:   { name:'🕷 거미 여왕', col:'#8e44ad', col2:'#4a006a', radius:40, baseHp:1800, baseAtk:32, baseSpd:90,  xp:600, gold:200, ai:'boss', draw:drawBossGeneric, isBoss:true },
  dragon:   { name:'🔥 화염 드래곤',col:'#e74c3c', col2:'#7b0000', radius:48, baseHp:3200, baseAtk:48, baseSpd:80,  xp:1000,gold:350, ai:'boss', draw:drawBossGeneric, isBoss:true },
  lich:     { name:'💀 리치 왕',    col:'#bdc3c7', col2:'#444',    radius:44, baseHp:5000, baseAtk:60, baseSpd:88,  xp:1500,gold:500, ai:'boss', draw:drawBossGeneric, isBoss:true },
  darkLord: { name:'☠ 마왕 다크오스',col:'#8e44ad',col2:'#1a0030', radius:55, baseHp:8000, baseAtk:80, baseSpd:95,  xp:3000,gold:800, ai:'boss', draw:drawBossGeneric, isBoss:true },
};

// ── WAVE CONFIG ──────────────────────────────────────────
// Each wave: duration(s), enemy spawn list [{type, count, spawnInterval(s)}], boss?
const WAVES = [
  { dur:30, pool:['slime','bat'],             spawnRate:.8, maxEnemy:18, boss:null },
  { dur:35, pool:['slime','bat','skeleton'],  spawnRate:.7, maxEnemy:22, boss:null },
  { dur:45, pool:['skeleton','orc','bat'],    spawnRate:.6, maxEnemy:28, boss:'spider' },
  { dur:40, pool:['orc','mageE','bat'],       spawnRate:.55,maxEnemy:30, boss:null },
  { dur:50, pool:['demon','mageE','orc'],     spawnRate:.5, maxEnemy:35, boss:'dragon' },
  { dur:45, pool:['demon','ghost','skeleton'],spawnRate:.45,maxEnemy:38, boss:null },
  { dur:55, pool:['golem','demon','mageE'],   spawnRate:.4, maxEnemy:40, boss:'lich' },
  { dur:60, pool:['golem','ghost','demon'],   spawnRate:.38,maxEnemy:45, boss:null },
  { dur:90, pool:['golem','demon','ghost'],   spawnRate:.35,maxEnemy:50, boss:'darkLord' },
];

// ── GAME STATE ─────────────────────────────────────────────
let G = null, RAF = null, selClsId = null;
let timer = 0, lastTs = 0;

function mkPlayer(clsId) {
  const c = CLASSES[clsId];
  const defaultWeapons = { warrior:'sword', mage:'fireball', archer:'arrow', ninja:'shuriken' };
  return {
    ...c, clsId,
    x: GW / 2, y: GH / 2,
    vx: 0, vy: 0,
    hp: c.hp, maxHp: c.hp,
    mp: c.mp, maxMp: c.mp,
    atk: c.atk, def: c.def, spd: c.spd,
    alive: true, invincible: 0, hitFlash: 0,
    level: 1, xp: 0, xpNext: 80,
    kills: 0, gold: 0, score: 0,
    atkCd: 0, atkDir: 0, atkAnim: 0,
    combo: 0, comboTimer: 0, maxCombo: 0,
    walkPhase: 0,
    crit: .12,
    // weapons: map weaponId -> {level, atkTimer, ...state}
    weapons: {},
    passives: {},
    actives: {},
    // skill timers
    skillCds: { Q: 0, E: 0, R: 0 },
    // derived passives (computed)
    _spdMult: 1, _atkMult: 1, _pickup: 60,
    // init default weapon
    relics: [],  // 획득한 유물 ID 목록
  };
}

function addWeapon(p, wid) {
  if (p.weapons[wid]) { p.weapons[wid].level = Math.min(p.weapons[wid].level + 1, WEAPON_DEFS[wid].maxLv); }
  else { p.weapons[wid] = { level: 1, atkTimer: 0, state: {} }; }
}
function addPassive(p, pid) {
  if (p.passives[pid]) { p.passives[pid] = Math.min((p.passives[pid] || 0) + 1, WEAPON_DEFS[pid].maxLv); }
  else { p.passives[pid] = 1; }
  applyPassives(p);
}
function addActive(p, aid) {
  if (p.actives[aid]) { p.actives[aid] = Math.min((p.actives[aid] || 0) + 1, WEAPON_DEFS[aid].maxLv); }
  else { p.actives[aid] = 1; }
  if (!p.skillCds[WEAPON_DEFS[aid].key]) p.skillCds[WEAPON_DEFS[aid].key] = 0;
}
function applyPassives(p) {
  const c = CLASSES[p.clsId];
  p._spdMult = 1;
  p._atkMult = 1;
  p._pickup = 60;
  if (p.passives.armor) p.def = c.def + p.passives.armor * 12;
  if (p.passives.boots) p._spdMult += p.passives.boots * .2;
  if (p.passives.magnet) p._pickup = 60 + p.passives.magnet * 60;
  if (p.passives.amulet) p.crit = .12 + p.passives.amulet * .15;
}

function initGame(clsId) {
  PARTS.length = 0; SLASHES.length = 0; PROJS.length = 0;

  const p = mkPlayer(clsId);
  const defaultW = { warrior:'sword', mage:'fireball', archer:'arrow', ninja:'shuriken' };
  addWeapon(p, defaultW[clsId]);

  G = {
    clsId, player: p,
    enemies: [],
    items: [],
    waveIdx: 0,
    waveTimer: 0,
    spawnTimer: 0,
    totalWaveKills: 0,
    waveKillGoal: 0,
    bossAlive: false,
    boss: null,
    phase: 'play', // play | lvlup | over | win
    paused: false,
    hitStop: 0,
    shake: 0, shakeTimer: 0,
    elapsed: 0,
    totalKills: 0,
    pendingLvlUp: false,
    lvlUpOptions: [],
  };

  startWave(0);
}

function startWave(idx) {
  G.waveIdx = idx;
  const wd = WAVES[Math.min(idx, WAVES.length - 1)];
  G.waveTimer = wd.dur;
  G.spawnTimer = 0;
  G.totalWaveKills = 0;
  G.waveKillGoal = wd.maxEnemy + Math.floor(idx * 8);
  G.bossAlive = false;
  G.boss = null;
  document.getElementById('boss-hpbar').classList.remove('show');
  showToast('🌊', `웨이브 ${idx + 1} 시작!`, wd.boss ? `보스: ${ETYPES[wd.boss]?.name}` : '모든 적을 처치하세요');
}

// ── SPAWN ENEMIES ─────────────────────────────────────────
function spawnEnemy(typeId) {
  const t = ETYPES[typeId];
  const sc = 1 + G.waveIdx * .3;
  // Spawn at edge
  const side = Math.floor(Math.random() * 4);
  let x = 0, y = 0;
  if (side === 0) { x = Math.random() * GW; y = -30; }
  else if (side === 1) { x = GW + 30; y = Math.random() * GH; }
  else if (side === 2) { x = Math.random() * GW; y = GH + 30; }
  else { x = -30; y = Math.random() * GH; }

  const hp = Math.round(t.baseHp * sc);
  G.enemies.push({
    ...t, typeId, x, y, vx: 0, vy: 0,
    hp, maxHp: hp, atk: Math.round(t.baseAtk * sc),
    spd: t.baseSpd + G.waveIdx * 4,
    alive: true, dying: false, deathTimer: .45,
    frozen: 0, stun: 0,
    hitFlash: 0,
    dir: Math.random() * Math.PI * 2,
    atkTimer: .8 + Math.random(),
    phaseTimer: .5 + Math.random() * 2,
    walkPhase: Math.random() * Math.PI * 2,
    uid: 'e' + Math.random(),
    charging: false, chargeDir: 0, chargeTimer: 0,
    projTimer: 1.5 + Math.random() * 2,
    aggroTimer: Math.random() * 2,
  });
}

function spawnBoss(typeId) {
  const t = ETYPES[typeId];
  const sc = 1 + G.waveIdx * .45;
  const hp = Math.round(t.baseHp * sc);
  const boss = {
    ...t, typeId, x: GW / 2, y: -60, vx: 0, vy: 0,
    hp, maxHp: hp, atk: Math.round(t.baseAtk * sc),
    spd: t.baseSpd,
    alive: true, dying: false, deathTimer: 1.5,
    frozen: 0, stun: 0, hitFlash: 0,
    dir: Math.PI / 2,
    atkTimer: 1.2, projTimer: 1.5, phaseTimer: 2,
    walkPhase: 0, uid: 'boss' + Math.random(),
    phase: 1, rage: false, enrage: false,
    uid: 'boss',
    isBoss: true,
  };
  G.enemies.push(boss);
  G.boss = boss;
  G.bossAlive = true;
  // Announce
  document.getElementById('ba-wave').textContent = '⚠ BOSS ⚠';
  document.getElementById('ba-name').textContent = t.name;
  const ba = document.getElementById('boss-announce');
  ba.style.display = 'block';
  setTimeout(() => ba.style.display = 'none', 2600);
  const bbar = document.getElementById('boss-hpbar');
  bbar.classList.add('show');
  document.getElementById('boss-name-txt').textContent = '⚠ ' + t.name;
  shakeScreen(14, 55); sfx_boss();
  spawnP(GW / 2, -20, { n:40, col:['#ff4400','#ff8800'], glow:true, sMin:4, sMax:14 });
}

// ── COMBAT ────────────────────────────────────────────────
function calcDmg(p, mult = 1) {
  const base = p.atk * (p._atkMult || 1);
  const crit = Math.random() < p.crit;
  const v = Math.round((base * mult + Math.random() * 5 - 2) * (crit ? 2.2 : 1));
  return { v: Math.max(1, v), crit };
}

function hitEnemy(e, dmgV, crit, knockback = { x: 0, y: 0 }) {
  if (!e.alive) return;
  let dv = dmgV;
  if (e.frozen > 0) dv = Math.round(dv * 1.45);
  e.hp -= dv; e.hitFlash = .18;
  G.hitStop = crit ? .09 : .05;
  dnum(e.x, e.y - e.radius - 6, dv, crit);
  spawnP(e.x, e.y, { n: crit ? 14 : 7, col:[e.col, '#ffcc44'], dir:Math.atan2(-knockback.y,-knockback.x), spread: crit ? Math.PI*2 : 1.2, sMin:2, sMax: crit?7:4, glow:crit });
  if (knockback.x || knockback.y) { e.vx += knockback.x; e.vy += knockback.y; }
  if (crit) shakeScreen(3, 5);
  if (e.hp <= 0) killEnemy(e);
}

function hitCircle(cx, cy, r, dmgV, crit) {
  for (const e of G.enemies.filter(e => e.alive)) {
    const dx = e.x - cx, dy = e.y - cy;
    if (dx * dx + dy * dy < (r + e.radius) ** 2) {
      const dist = Math.hypot(dx, dy) || 1;
      hitEnemy(e, dmgV, crit, { x: (dx / dist) * 180, y: (dy / dist) * 180 });
    }
  }
}

function killEnemy(e) {
  e.alive = false; e.dying = true;
  const p = G.player;
  p.kills++; G.totalKills++;
  G.totalWaveKills++;
  p.xp += e.xp; p.gold += e.gold || 8; p.score += e.xp * 2;

  if (e.isBoss) {
    p.gold += 200; p.score += e.xp * 4;
    G.bossAlive = false; G.boss = null;
    document.getElementById('boss-hpbar').classList.remove('show');
    spawnP(e.x, e.y, { n:80, col:['#ffcc00','#ff6600','#fff','#ff4400'], glow:true, sMin:5, sMax:18 });
    spawnWave(e.x, e.y, '#ffcc00', 200);
    shakeScreen(18, 70); sfx_clear();
    showToast('🏆', '보스 처치!', `+200 골드 +${e.xp} XP`);
    // ── 유물 선택 트리거 ──
    setTimeout(() => showRelicChoice(), 900);
  } else {
    spawnP(e.x, e.y, { n:10, col:[e.col,'#ffcc44'], sMin:2, sMax:6 });
    // Vampire passive
    if (p.passives.vampire) { p.hp = Math.min(p.maxHp, p.hp + p.passives.vampire * 5); }
    // Drop items
    if (Math.random() < .3) G.items.push({ x:e.x, y:e.y, type:Math.random()<.65?'hp':'mp', life:10, alive:true });
  }

  checkLvlUp(p);
  sfx_kill();
}

function checkLvlUp(p) {
  while (p.xp >= p.xpNext) {
    p.xp -= p.xpNext; p.level++;
    p.xpNext = Math.round(p.xpNext * 1.45 + 20);
    G.pendingLvlUp = true;
    buildLvlUpOptions(p);
    sfx_lvlup();
  }
}

function buildLvlUpOptions(p) {
  // 3 random options: mix of weapons/passives/actives
  const allOptions = [];
  // Weapons available
  const weaponPool = ['sword','fireball','arrow','shuriken','axe','lightning','holy','tornado'];
  const passivePool = ['armor','boots','magnet','amulet','vampire'];
  const activePool = ['dash','nova','timeStop'];

  for (const wid of weaponPool) {
    const def = WEAPON_DEFS[wid];
    const curLv = p.weapons[wid]?.level || 0;
    if (curLv < def.maxLv) {
      allOptions.push({ id:wid, def, curLv, kind:'weapon', display: curLv > 0 ? `${def.name} Lv${curLv+1}` : `신규: ${def.name}` });
    }
  }
  for (const pid of passivePool) {
    const def = WEAPON_DEFS[pid];
    const curLv = p.passives[pid] || 0;
    if (curLv < def.maxLv) allOptions.push({ id:pid, def, curLv, kind:'passive' });
  }
  for (const aid of activePool) {
    const def = WEAPON_DEFS[aid];
    const curLv = p.actives[aid] || 0;
    if (curLv < def.maxLv) allOptions.push({ id:aid, def, curLv, kind:'active' });
  }

  // Shuffle and pick 3
  for (let i = allOptions.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allOptions[i], allOptions[j]] = [allOptions[j], allOptions[i]];
  }

  G.lvlUpOptions = allOptions.slice(0, 3);
  showLvlUpModal();
}

function showLvlUpModal() {
  G.phase = 'lvlup';
  const el = document.getElementById('lvlup');
  el.style.display = 'flex';
  const c = document.getElementById('lvlup-cards');
  c.innerHTML = G.lvlUpOptions.map((opt, i) => {
    const isNew = opt.curLv === 0;
    const isMax = opt.curLv >= opt.def.maxLv - 1;
    const typeLabel = { weapon:'무기', passive:'패시브', active:'스킬' }[opt.kind];
    return `<div class="ucard" onclick="pickOption(${i})">
      <div class="uc-ico">${opt.def.icon}</div>
      <div class="uc-name">${opt.def.name}</div>
      ${opt.curLv > 0 ? `<div style="font-size:10px;color:#888;margin-top:2px;">Lv${opt.curLv} → <span style="color:var(--gold)">Lv${opt.curLv+1}</span>${isMax?'<span style="color:#ff7700"> MAX!</span>':''}</div>` : '<div style="font-size:10px;color:var(--green);margin-top:2px;">✦ 신규 획득</div>'}
      <div class="uc-desc">${opt.def.desc}</div>
      <div class="uc-type ${opt.kind}">${typeLabel}</div>
    </div>`;
  }).join('');
}

function pickOption(i) {
  const opt = G.lvlUpOptions[i];
  const p = G.player;
  if (opt.kind === 'weapon') addWeapon(p, opt.id);
  else if (opt.kind === 'passive') addPassive(p, opt.id);
  else addActive(p, opt.id);
  document.getElementById('lvlup').style.display = 'none';
  G.phase = 'play';
  G.pendingLvlUp = false;
  const isNew = opt.curLv === 0;
  if (isNew) {
    const ub = document.getElementById('unlock-banner');
    document.getElementById('ub-ico').textContent = opt.def.icon;
    document.getElementById('ub-name').textContent = opt.def.name + ' 획득!';
    document.getElementById('ub-desc').textContent = opt.def.desc;
    ub.style.display = 'block';
    setTimeout(() => ub.style.display = 'none', 2600);
  }
  sfx_buy();
}

function takeDmg(v) {
  const p = G.player;
  if (p.invincible > 0) return;
  const reduced = Math.max(1, v - Math.floor(p.def * .45));
  p.hp -= reduced; p.hitFlash = .2; p.invincible = .6;
  shakeScreen(5, 8);
  const vig = document.getElementById('vignette');
  vig.style.opacity = '1'; setTimeout(() => vig.style.opacity = '0', 180);
  dnum(p.x, p.y - p.radius - 8, reduced, false, '#ff4444');
  sfx_hit();
  if (p.hp <= 0) gameOver();
}

// ── UPDATE WEAPONS ─────────────────────────────────────────
function updateWeapons(dt, p) {
  for (const [wid, ws] of Object.entries(p.weapons)) {
    ws.atkTimer -= dt;
    if (ws.atkTimer > 0) continue;
    const lv = ws.level;
    switch (wid) {
      case 'sword':
        ws.atkTimer = Math.max(.18, .45 - lv * .03);
        doSword(p, ws, lv); break;
      case 'fireball':
        ws.atkTimer = Math.max(.22, .55 - lv * .04);
        doFireball(p, ws, lv); break;
      case 'arrow':
        ws.atkTimer = Math.max(.12, .28 - lv * .02);
        doArrow(p, ws, lv); break;
      case 'shuriken':
        ws.atkTimer = Math.max(.15, .22 - lv * .01);
        doShuriken(p, ws, lv); break;
      case 'axe':
        ws.atkTimer = Math.max(.5, .9 - lv * .05);
        doAxe(p, ws, lv); break;
      case 'lightning':
        ws.atkTimer = Math.max(.25, .5 - lv * .03);
        doLightning(p, ws, lv); break;
      case 'holy':
        ws.atkTimer = Math.max(.6, 1.2 - lv * .08);
        doHoly(p, ws, lv); break;
      case 'tornado':
        ws.atkTimer = Math.max(.08, .14 - lv * .008);
        doTornado(p, ws, lv); break;
    }
    sfx_atk();
  }
}

function nearestEnemy(p, maxR = 9999) {
  let best = null, bd = maxR * maxR;
  for (const e of G.enemies) {
    if (!e.alive) continue;
    const d2 = (e.x - p.x) ** 2 + (e.y - p.y) ** 2;
    if (d2 < bd) { bd = d2; best = e; }
  }
  return best;
}

function getAimDir(p) {
  const t = nearestEnemy(p);
  if (t) return Math.atan2(t.y - p.y, t.x - p.x);
  return p.atkDir || 0;
}

function doSword(p, ws, lv) {
  const ang = getAimDir(p);
  const range = 80 + lv * 8;
  const d = calcDmg(p, 1.1 + lv * .12);
  hitCircle(p.x + Math.cos(ang) * range * .5, p.y + Math.sin(ang) * range * .5, range * .65, d.v, d.crit);
  spawnSlash(p.x, p.y, ang, range, d.crit ? '#ffff88' : '#ff8844', 10);
  if (lv >= 5) {
    // Extra side slashes
    spawnSlash(p.x, p.y, ang + .5, range * .7, '#ff6644', 8);
    spawnSlash(p.x, p.y, ang - .5, range * .7, '#ff6644', 8);
    hitCircle(p.x + Math.cos(ang + .5) * range * .5, p.y + Math.sin(ang + .5) * range * .5, range * .4, d.v * .6, false);
    hitCircle(p.x + Math.cos(ang - .5) * range * .5, p.y + Math.sin(ang - .5) * range * .5, range * .4, d.v * .6, false);
  }
}

function doFireball(p, ws, lv) {
  const ang = getAimDir(p);
  const count = 1 + Math.floor(lv / 3);
  const d = calcDmg(p, 1.5 + lv * .15);
  for (let i = 0; i < count; i++) {
    const a = ang + (Math.random() - .5) * .25;
    spawnProj(p.x, p.y, Math.cos(a) * (360 + lv * 10), Math.sin(a) * (360 + lv * 10), d.v, '#ff6600', 'player',
      { sz: 10 + lv, homing: lv >= 4, explode: lv >= 6, emoji: '🔥', trail: true });
  }
}

function doArrow(p, ws, lv) {
  const ang = getAimDir(p);
  const d = calcDmg(p, 1.2 + lv * .12);
  const spread = lv >= 3 ? 3 : (lv >= 6 ? 5 : 1);
  for (let i = 0; i < spread; i++) {
    const a = ang + (i - Math.floor(spread / 2)) * .18;
    spawnProj(p.x, p.y, Math.cos(a) * (440 + lv * 12), Math.sin(a) * (440 + lv * 12), d.v, '#44ff88', 'player',
      { sz: 8, pierce: lv >= 2 ? lv : 0 });
  }
}

function doShuriken(p, ws, lv) {
  const count = 2 + Math.floor(lv / 2);
  const baseAng = getAimDir(p);
  const d = calcDmg(p, .9 + lv * .1);
  for (let i = 0; i < count; i++) {
    const a = baseAng + (i / count) * Math.PI * 2 * (lv >= 5 ? .8 : .4);
    spawnProj(p.x, p.y, Math.cos(a) * 380, Math.sin(a) * 380, d.v, '#44ddff', 'player', { sz: 7, pierce: 1 });
  }
}

function doAxe(p, ws, lv) {
  const ang = getAimDir(p);
  const d = calcDmg(p, 2.5 + lv * .3);
  spawnProj(p.x, p.y, Math.cos(ang) * 240, Math.sin(ang) * 240, d.v, '#ffaa00', 'player',
    { sz: 16 + lv * 2, explode: true, emoji: '🪓', life: 1.2 });
}

function doLightning(p, ws, lv) {
  // Chain lightning: hit nearest, then chain
  let target = nearestEnemy(p, 500);
  if (!target) return;
  const d = calcDmg(p, 1.4 + lv * .14);
  const chains = 1 + Math.floor(lv / 2);
  let cur = target;
  const hit = new Set();
  for (let c = 0; c < chains; c++) {
    if (!cur || hit.has(cur.uid)) break;
    hit.add(cur.uid);
    hitEnemy(cur, d.v, d.crit, { x: 0, y: 0 });
    spawnSlash(p.x, p.y, Math.atan2(cur.y - p.y, cur.x - p.x), Math.hypot(cur.x - p.x, cur.y - p.y), '#aaeeFF', 8);
    spawnP(cur.x, cur.y, { n:8, col:'#aaddff', glow:true, sMin:2, sMax:5 });
    // Find next nearest not hit
    let nextBest = null, nd = 150 * 150;
    for (const e of G.enemies) {
      if (!e.alive || hit.has(e.uid)) continue;
      const d2 = (e.x - cur.x) ** 2 + (e.y - cur.y) ** 2;
      if (d2 < nd) { nd = d2; nextBest = e; }
    }
    cur = nextBest;
  }
}

function doHoly(p, ws, lv) {
  const d = calcDmg(p, 1.3 + lv * .15);
  hitCircle(p.x, p.y, 100 + lv * 15, d.v, d.crit);
  spawnWave(p.x, p.y, '#ffffaa', 120 + lv * 15);
  spawnP(p.x, p.y, { n:12, col:['#ffffaa','#ffeeaa'], glow:true, sMin:3, sMax:8 });
  // Heal
  p.hp = Math.min(p.maxHp, p.hp + lv * 3);
}

function doTornado(p, ws, lv) {
  const ang = ws.state.ang || 0;
  ws.state.ang = (ang + .4) % (Math.PI * 2);
  const dist = 50 + lv * 5;
  const tx = p.x + Math.cos(ws.state.ang) * dist;
  const ty = p.y + Math.sin(ws.state.ang) * dist;
  const d = calcDmg(p, .6 + lv * .07);
  hitCircle(tx, ty, 28 + lv * 3, d.v, d.crit);
  spawnP(tx, ty, { n:4, col:['#88ccff','#aaddff'], sMin:2, sMax:4 });
}

// ── UPDATE ACTIVES ─────────────────────────────────────────
function tryActive(p, key) {
  const activeMap = {};
  for (const [aid, lv] of Object.entries(p.actives)) {
    if (WEAPON_DEFS[aid].key === key) activeMap[aid] = lv;
  }
  for (const [aid, lv] of Object.entries(activeMap)) {
    if (p.skillCds[key] > 0 || p.mp < 20) continue;
    doActive(p, aid, lv, key);
  }
}

function doActive(p, aid, lv, key) {
  p.mp -= 20 + lv * 5;
  p.skillCds[key] = Math.max(3, 8 - lv);
  switch (aid) {
    case 'dash': {
      const ang = getAimDir(p);
      p.vx = Math.cos(ang) * 600; p.vy = Math.sin(ang) * 600;
      p.invincible = .5;
      spawnP(p.x, p.y, { n:20, col:[p.col,'#fff'], glow:true, sMin:3, sMax:8 });
      setTimeout(() => {
        hitCircle(p.x, p.y, 70 + lv * 12, calcDmg(p, 2.2 + lv * .3).v, false);
        spawnWave(p.x, p.y, p.col, 100);
        shakeScreen(6, 12);
      }, 220);
      sfx_skill(); break;
    }
    case 'nova': {
      const d = calcDmg(p, 2.5 + lv * .4);
      hitCircle(p.x, p.y, 100 + lv * 20, d.v, d.crit);
      spawnWave(p.x, p.y, '#ff4400', 130 + lv * 20);
      spawnP(p.x, p.y, { n:40, col:['#ff4400','#ff8800','#ffcc00'], glow:true, sMin:4, sMax:12 });
      shakeScreen(8, 18); sfx_skill(); break;
    }
    case 'timeStop': {
      const dur = 2 + lv;
      for (const e of G.enemies) if (e.alive) e.frozen = Math.max(e.frozen, dur);
      spawnP(p.x, p.y, { n:60, col:['#aaddff','#44aaff','#fff'], glow:true, sMin:3, sMax:10 });
      showToast('⏱️', '시간 정지!', `${dur}초간 모든 적 동결`); sfx_skill(); break;
    }
  }
}

// ── UPDATE PLAYER ────────────────────────────────────────
function updatePlayer(dt) {
  const p = G.player;
  if (!p.alive) return;

  let mx = 0, my = 0;
  if (KEYS['ArrowLeft'] || KEYS['KeyA']) mx -= 1;
  if (KEYS['ArrowRight'] || KEYS['KeyD']) mx += 1;
  if (KEYS['ArrowUp'] || KEYS['KeyW']) my -= 1;
  if (KEYS['ArrowDown'] || KEYS['KeyS']) my += 1;

  const moving = mx !== 0 || my !== 0;
  const spd = p.spd * (p._spdMult || 1);

  if (moving) {
    const len = Math.hypot(mx, my);
    p.vx += (mx / len) * 1600 * dt;
    p.vy += (my / len) * 1600 * dt;
    const mag = Math.hypot(p.vx, p.vy);
    if (mag > spd) { p.vx = p.vx / mag * spd; p.vy = p.vy / mag * spd; }
    p.atkDir = Math.atan2(p.vy, p.vx);
    p.walkPhase += dt * 9;
  } else {
    p.vx *= Math.pow(.06, dt); p.vy *= Math.pow(.06, dt);
    if (Math.hypot(p.vx, p.vy) < 2) { p.vx = 0; p.vy = 0; }
  }

  p.x += p.vx * dt; p.y += p.vy * dt;

  // Clamp to world
  const R = p.radius;
  p.x = Math.max(R, Math.min(GW - R, p.x));
  p.y = Math.max(R, Math.min(GH - R, p.y));

  // Timers
  if (p.invincible > 0) p.invincible -= dt;
  if (p.hitFlash > 0) p.hitFlash -= dt;
  if (p.comboTimer > 0) {
    p.comboTimer -= dt;
    if (p.comboTimer <= 0) { p.combo = 0; document.getElementById('combo').style.opacity = '0'; }
  }
  if (p.mp < p.maxMp) p.mp = Math.min(p.maxMp, p.mp + dt * 3);

  // Skill inputs
  if (JKEYS['Q']) tryActive(p, 'Q');
  if (JKEYS['E']) tryActive(p, 'E');
  if (JKEYS['R']) tryActive(p, 'R');
  for (const key of ['Q', 'E', 'R']) { if (p.skillCds[key] > 0) p.skillCds[key] -= dt; }

  // Item pickup
  const pickupR = p._pickup || 60;
  G.items = G.items.filter(it => {
    if (!it.alive) return false;
    it.life -= dt;
    if (it.life <= 0) return false;
    const d = Math.hypot(it.x - p.x, it.y - p.y);
    if (d < pickupR) {
      if (d < 32) {
        if (it.type === 'hp') { p.hp = Math.min(p.maxHp, p.hp + 30); dnum(it.x, it.y - 10, '+30 HP', false, '#22ff88'); }
        else { p.mp = Math.min(p.maxMp, p.mp + 28); dnum(it.x, it.y - 10, '+28 MP', false, '#44aaff'); }
        sfx_item(); it.alive = false; return false;
      }
      // Magnet: pull toward player
      const pull = (pickupR - 60) > 0 ? 200 : 0;
      if (pull > 0) { it.x += (p.x - it.x) / d * pull * dt; it.y += (p.y - it.y) / d * pull * dt; }
    }
    return true;
  });

  // Auto weapon attack
  updateWeapons(dt, p);
}

// ── UPDATE ENEMIES ────────────────────────────────────────
function updateEnemies(dt) {
  const p = G.player;
  for (const e of G.enemies) {
    if (!e.alive) { if (e.dying) { e.deathTimer -= dt; } continue; }
    if (e.hitFlash > 0) e.hitFlash -= dt;
    e.walkPhase += dt * 5;

    if (e.frozen > 0) { e.frozen -= dt; e.vx *= .8; e.vy *= .8; e.x += e.vx * dt; e.y += e.vy * dt; continue; }
    if (e.stun > 0) { e.stun -= dt; e.vx *= .85; e.vy *= .85; continue; }

    e.vx *= Math.pow(.25, dt); e.vy *= Math.pow(.25, dt);
    e.phaseTimer -= dt;

    const dx = p.x - e.x, dy = p.y - e.y;
    const dist = Math.hypot(dx, dy) || 1;
    e.dir = Math.atan2(dy, dx);

    // AI behaviors
    switch (e.ai) {
      case 'bounce':
        if (e.phaseTimer <= 0) { e.dir += (Math.random() - .5) * 1.8; e.phaseTimer = .4 + Math.random() * .8; }
        if (dist < 420) { e.vx += Math.cos(e.dir) * e.spd * 2.5 * dt; e.vy += Math.sin(e.dir) * e.spd * 2.5 * dt; }
        break;
      case 'erratic':
        if (e.phaseTimer <= 0) { e.dir = e.dir + (Math.random() - .5) * Math.PI * 1.2; e.phaseTimer = .2 + Math.random() * .4; }
        e.vx += Math.cos(e.dir) * e.spd * 3 * dt; e.vy += Math.sin(e.dir) * e.spd * 3 * dt;
        break;
      case 'charge':
        if (!e.charging) {
          if (dist < 280 && e.phaseTimer <= 0) {
            e.charging = true; e.chargeDir = e.dir; e.chargeTimer = .55;
          } else if (dist > 50) {
            e.vx += (dx / dist) * e.spd * .7 * dt * 3.5; e.vy += (dy / dist) * e.spd * .7 * dt * 3.5;
          }
        } else {
          e.vx += Math.cos(e.chargeDir) * e.spd * 3.5 * dt * 3.5; e.vy += Math.sin(e.chargeDir) * e.spd * 3.5 * dt * 3.5;
          e.chargeTimer -= dt;
          if (e.chargeTimer <= 0) { e.charging = false; e.phaseTimer = 1.0 + Math.random() * .8; }
        }
        break;
      case 'ranged':
        if (dist < 220) { e.vx -= (dx / dist) * e.spd * dt * 3; e.vy -= (dy / dist) * e.spd * dt * 3; }
        else if (dist > 320) { e.vx += (dx / dist) * e.spd * .55 * dt * 3; e.vy += (dy / dist) * e.spd * .55 * dt * 3; }
        break;
      case 'mage':
        if (dist < 190) { e.vx -= (dx / dist) * e.spd * dt * 3; e.vy -= (dy / dist) * e.spd * dt * 3; }
        else if (dist > 300) { e.vx += (dx / dist) * e.spd * .65 * dt * 3; e.vy += (dy / dist) * e.spd * .65 * dt * 3; }
        break;
      case 'flank': // Demon: tries to get behind
        const flanks = [Math.atan2(dy, dx) + 1.2, Math.atan2(dy, dx) - 1.2];
        const fa = flanks[Math.floor(e.walkPhase * .5) % 2];
        e.vx += Math.cos(fa) * e.spd * .8 * dt * 3.5; e.vy += Math.sin(fa) * e.spd * .8 * dt * 3.5;
        break;
      case 'phase': // Ghost: phases through, teleports
        if (e.phaseTimer <= 0 && dist < 350) {
          e.x = p.x + (Math.random() - .5) * 160; e.y = p.y + (Math.random() - .5) * 160;
          e.phaseTimer = 2 + Math.random() * 2;
          spawnP(e.x, e.y, { n:12, col:['#bdc3c7','#aaa'], sMin:2, sMax:5 });
        }
        if (dist > 50) { e.vx += (dx / dist) * e.spd * .5 * dt * 3; e.vy += (dy / dist) * e.spd * .5 * dt * 3; }
        break;
      case 'boss':
        updateBossAI(e, p, dt); break;
    }

    // Speed cap
    const spd = Math.hypot(e.vx, e.vy);
    if (spd > e.spd * 3.2) { e.vx = e.vx / spd * e.spd * 3.2; e.vy = e.vy / spd * e.spd * 3.2; }

    e.x += e.vx * dt; e.y += e.vy * dt;

    // Clamp + bounce at boundary
    if (e.x < e.radius) { e.x = e.radius; e.vx = Math.abs(e.vx); }
    if (e.x > GW - e.radius) { e.x = GW - e.radius; e.vx = -Math.abs(e.vx); }
    if (e.y < e.radius) { e.y = e.radius; e.vy = Math.abs(e.vy); }
    if (e.y > GH - e.radius) { e.y = GH - e.radius; e.vy = -Math.abs(e.vy); }

    // Melee damage to player
    e.atkTimer -= dt;
    if (e.atkTimer <= 0 && dist < e.radius + p.radius + 22) {
      e.atkTimer = .75 + Math.random() * .5;
      takeDmg(e.atk);
    }

    // Ranged attacks
    if ((e.ai === 'ranged' || e.ai === 'mage' || e.ai === 'boss') && dist < 400) {
      e.projTimer -= dt;
      if (e.projTimer <= 0) {
        const cd = e.isBoss ? (e.enrage ? .5 : (e.rage ? .8 : 1.2)) : (1.2 + Math.random());
        e.projTimer = cd;
        const count = e.isBoss ? (e.enrage ? 5 : (e.rage ? 4 : 3)) : 1;
        for (let i = 0; i < count; i++) {
          const ang = e.dir + (count > 1 ? (i / count - .5) * Math.PI * (e.enrage ? 1.8 : 1) : 0);
          spawnProj(e.x, e.y, Math.cos(ang) * (e.isBoss ? 185 : 210), Math.sin(ang) * (e.isBoss ? 185 : 210),
            Math.round(e.atk * .65), e.col, 'enemy', { sz: e.isBoss ? 13 : 9 });
        }
      }
    }
  }
  // Remove dead enemies that finished death anim
  G.enemies = G.enemies.filter(e => e.alive || (e.dying && e.deathTimer > 0));
}

function updateBossAI(b, p, dt) {
  const hpPct = b.hp / b.maxHp;
  if (!b.rage && hpPct < .55) {
    b.rage = true; b.spd *= 1.4;
    spawnP(b.x, b.y, { n:60, col:['#ff4400','#ff8800','#fff'], glow:true, sMin:5, sMax:16 });
    spawnWave(b.x, b.y, '#ff4400', 200); shakeScreen(12, 40);
    showToast('🔥', `${b.name} 분노!`, '능력치가 강화됩니다!');
  }
  if (!b.enrage && hpPct < .25) {
    b.enrage = true; b.spd *= 1.2;
    spawnP(b.x, b.y, { n:100, col:['#ff0000','#ff00ff','#fff'], glow:true, sMin:6, sMax:20 });
    spawnWave(b.x, b.y, '#ff00ff', 250); shakeScreen(20, 70); sfx_boss();
    showToast('💀', `${b.name} 광란!`, '이건 진짜 위험합니다...');
  }

  const dx = p.x - b.x, dy = p.y - b.y;
  const dist = Math.hypot(dx, dy) || 1;
  b.dir = Math.atan2(dy, dx);

  const speedMult = b.enrage ? 3.5 : (b.rage ? 2.8 : 2.2);
  b.vx += (dx / dist) * b.spd * speedMult * 0.016;
  b.vy += (dy / dist) * b.spd * speedMult * 0.016;

  if (b.alive) {
    document.getElementById('boss-hp-fill').style.width = Math.max(0, (b.hp / b.maxHp) * 100) + '%';
  }
}

// ── PROJECTILE UPDATE ────────────────────────────────────
function updateProjs(dt) {
  for (let i = PROJS.length - 1; i >= 0; i--) {
    const pr = PROJS[i];
    if (!pr.alive) { PROJS.splice(i, 1); continue; }
    pr.life -= dt;
    if (pr.life <= 0) { PROJS.splice(i, 1); continue; }

    if (pr.homing && pr.owner === 'player') {
      const t = nearestEnemy(G.player);
      if (t) {
        const dx = t.x - pr.x, dy = t.y - pr.y;
        const l = Math.hypot(dx, dy) || 1;
        pr.vx += (dx / l * 350 - pr.vx) * dt * 2.8;
        pr.vy += (dy / l * 350 - pr.vy) * dt * 2.8;
      }
    }

    if (pr.trail) {
      pr.trailTimer -= dt;
      if (pr.trailTimer <= 0) {
        spawnP(pr.x, pr.y, { n:3, col:[pr.col], sMin:2, sMax:4, dMin:.04, dMax:.06 });
        pr.trailTimer = .04;
      }
    }

    pr.x += pr.vx * dt; pr.y += pr.vy * dt;

    // Out of bounds
    if (pr.x < -50 || pr.x > GW + 50 || pr.y < -50 || pr.y > GH + 50) {
      if (pr.explode) doExplodeProj(pr);
      PROJS.splice(i, 1); continue;
    }

    if (pr.owner === 'player') {
      let hit = false;
      for (const e of G.enemies) {
        if (!e.alive) continue;
        if (pr.pierceHit.includes(e.uid)) continue;
        if (Math.hypot(pr.x - e.x, pr.y - e.y) < e.radius + pr.sz) {
          hitEnemy(e, pr.dmg, false, { x: pr.vx * .3, y: pr.vy * .3 });
          if (pr.pierce > 0) { pr.pierceHit.push(e.uid); pr.pierce--; }
          else if (pr.explode) { doExplodeProj(pr); PROJS.splice(i, 1); hit = true; break; }
          else { PROJS.splice(i, 1); hit = true; break; }
        }
      }
      if (hit) continue;
    } else {
      const p = G.player;
      if (Math.hypot(pr.x - p.x, pr.y - p.y) < p.radius + pr.sz) {
        takeDmg(pr.dmg); PROJS.splice(i, 1); continue;
      }
    }
  }
}

function doExplodeProj(pr) {
  hitCircle(pr.x, pr.y, 80, pr.dmg * 1.5, false);
  spawnP(pr.x, pr.y, { n:22, col:[pr.col,'#ff8800','#fff'], glow:true, sMin:3, sMax:9 });
  spawnWave(pr.x, pr.y, pr.col, 90);
  shakeScreen(5, 10);
}

// ── WAVE MANAGER ──────────────────────────────────────────
function updateWave(dt) {
  const wd = WAVES[Math.min(G.waveIdx, WAVES.length - 1)];

  // Spawn enemies
  const liveEnemies = G.enemies.filter(e => e.alive && !e.isBoss);
  const maxAlive = Math.min(wd.maxEnemy + G.waveIdx * 5, 60);
  if (liveEnemies.length < maxAlive) {
    G.spawnTimer -= dt;
    if (G.spawnTimer <= 0) {
      G.spawnTimer = Math.max(.2, wd.spawnRate - G.waveIdx * .02);
      const pool = wd.pool;
      spawnEnemy(pool[Math.floor(Math.random() * pool.length)]);
    }
  }

  G.waveTimer -= dt;
  // Wave end: when time is up AND no boss alive AND boss hasn't spawned yet
  if (G.waveTimer <= 0 && !G.bossAlive) {
    if (wd.boss && !G.bossSpawned) {
      G.bossSpawned = true;
      spawnBoss(wd.boss);
    } else if (!wd.boss || G.bossSpawned) {
      // Start next wave
      const nextIdx = G.waveIdx + 1;
      if (nextIdx >= WAVES.length) { gameWin(); return; }
      G.bossSpawned = false;
      startWave(nextIdx);
    }
  }
}

// ── MAIN GAME TICK ────────────────────────────────────────
function tick(dt) {
  if (G.phase !== 'play' || G.paused) return;
  if (G.hitStop > 0) { G.hitStop -= dt; return; }

  G.elapsed += dt;
  updatePlayer(dt);
  updateEnemies(dt);
  updateProjs(dt);
  updateWave(dt);
  tickP(dt);
  tickSlashes(dt);
  tickWaves(dt);

  if (G.shakeTimer > 0) G.shakeTimer -= dt;
  else G.shake = 0;
}

// ── DRAW ──────────────────────────────────────────────────
const BG_THEMES = [
  { floor:'#140a1e', grid:'rgba(80,30,120,.08)', accent:'#6622aa', fogCol:'rgba(60,20,90,.4)' },
  { floor:'#1e0a0a', grid:'rgba(120,20,20,.08)', accent:'#aa2200', fogCol:'rgba(90,20,20,.4)' },
  { floor:'#0a1a1e', grid:'rgba(20,80,120,.07)', accent:'#0088aa', fogCol:'rgba(20,60,90,.4)' },
  { floor:'#0a1a0a', grid:'rgba(20,100,30,.07)', accent:'#008844', fogCol:'rgba(20,80,30,.4)' },
  { floor:'#100010', grid:'rgba(80,0,120,.08)', accent:'#8800cc', fogCol:'rgba(60,0,90,.4)' },
];

function getBGTheme() { return BG_THEMES[G.waveIdx % BG_THEMES.length]; }

function drawBG() {
  const th = getBGTheme();
  ctx.fillStyle = th.floor;
  ctx.fillRect(0, 0, GW, GH);
  // Grid pattern
  ctx.save(); ctx.globalAlpha = 1;
  ctx.strokeStyle = th.grid; ctx.lineWidth = 1;
  for (let x = 0; x < GW; x += 40) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, GH); ctx.stroke(); }
  for (let y = 0; y < GH; y += 40) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(GW, y); ctx.stroke(); }
  ctx.restore();
  // Vignette
  ctx.save();
  const vg = ctx.createRadialGradient(GW / 2, GH / 2, GH * .3, GW / 2, GH / 2, GH);
  vg.addColorStop(0, 'transparent'); vg.addColorStop(1, 'rgba(0,0,0,.55)');
  ctx.fillStyle = vg; ctx.fillRect(0, 0, GW, GH);
  ctx.restore();
}

// ── PLAYER DRAW ───────────────────────────────────────────
function drawPlayer() {
  const p = G.player;
  if (!p.alive) return;
  if (p.invincible > 0 && Math.floor(timer * 18) % 2 === 0) return;
  const R = p.radius;
  const bounce = Math.hypot(p.vx, p.vy) > 10 ? Math.abs(Math.sin(p.walkPhase)) * 3 : 0;

  ctx.save();
  ctx.translate(p.x, p.y - bounce);

  // Shadow
  ctx.globalAlpha = .2; ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.ellipse(0, R + 2, R * .7, 5, 0, 0, Math.PI * 2); ctx.fill();
  ctx.globalAlpha = 1;

  // Buff aura
  if (Object.keys(p.actives).length > 0) {
    ctx.save(); ctx.globalAlpha = .15 + Math.sin(timer * 6) * .05;
    ctx.strokeStyle = '#ffcc00'; ctx.lineWidth = 2; ctx.shadowColor = '#ffcc00'; ctx.shadowBlur = 14;
    ctx.beginPath(); ctx.arc(0, 0, R + 8, 0, Math.PI * 2); ctx.stroke();
    ctx.shadowBlur = 0; ctx.restore();
  }

  // Hit flash
  if (p.hitFlash > 0) ctx.filter = `brightness(${2 + p.hitFlash * 6}) saturate(0)`;

  // Body gradient
  const bg = ctx.createRadialGradient(-R * .3, -R * .3, 1, 0, 0, R);
  bg.addColorStop(0, lighten(p.col, 45)); bg.addColorStop(1, p.col);
  ctx.fillStyle = bg; ctx.shadowColor = p.col; ctx.shadowBlur = 16;
  ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
  ctx.shadowBlur = 0;
  ctx.fillStyle = 'rgba(255,255,255,.2)';
  ctx.beginPath(); ctx.arc(-R * .25, -R * .3, R * .42, 0, Math.PI * 2); ctx.fill();

  // Direction arrow
  const aimDir = p.atkDir || 0;
  ctx.fillStyle = 'rgba(255,255,255,.9)';
  ctx.beginPath();
  ctx.moveTo(Math.cos(aimDir) * R, Math.sin(aimDir) * R);
  ctx.lineTo(Math.cos(aimDir + 2.5) * R * .4, Math.sin(aimDir + 2.5) * R * .4);
  ctx.lineTo(Math.cos(aimDir - 2.5) * R * .4, Math.sin(aimDir - 2.5) * R * .4);
  ctx.closePath(); ctx.fill();
  ctx.filter = 'none';

  // Icon
  ctx.font = `${R * .9}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(CLASSES[p.clsId].icon, 0, 0);

  ctx.restore();

  // HP bar
  if (p.hp < p.maxHp) {
    const bw = 44, bx = p.x - bw / 2, by = p.y - R - 18;
    ctx.fillStyle = 'rgba(0,0,0,.65)'; ctx.fillRect(bx, by, bw, 5);
    const pct = Math.max(0, p.hp / p.maxHp);
    ctx.fillStyle = pct > .5 ? '#22cc44' : pct > .25 ? '#ccaa00' : '#cc2200';
    ctx.fillRect(bx, by, bw * pct, 5);
  }
}

// ── ENEMY DRAW HELPERS ────────────────────────────────────
function lighten(hex, amt) {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.min(255, (n >> 16) + amt);
  const g = Math.min(255, ((n >> 8) & 0xff) + amt);
  const b = Math.min(255, (n & 0xff) + amt);
  return `rgb(${r},${g},${b})`;
}

function drawEnemyBase(e, R, customDraw) {
  ctx.save();
  const alpha = e.dying ? Math.max(0, e.deathTimer / .45) : 1;
  ctx.globalAlpha = alpha;
  if (e.hitFlash > 0) ctx.filter = `brightness(${2.5 + e.hitFlash * 6}) saturate(0)`;
  if (e.frozen > 0) ctx.filter = 'hue-rotate(200deg) brightness(1.9) saturate(2)';

  ctx.save(); ctx.translate(e.x, e.y);
  customDraw(e, R, ctx);
  ctx.restore();

  ctx.filter = 'none';

  // HP bar
  if (!e.dying && e.hp < e.maxHp) {
    const pct = Math.max(0, e.hp / e.maxHp);
    const bw = Math.max(36, R * 2.5);
    const bx = e.x - bw / 2, by = e.y - R - 16;
    ctx.fillStyle = 'rgba(0,0,0,.7)'; ctx.fillRect(bx, by, bw, 7);
    ctx.fillStyle = pct > .5 ? '#22cc44' : pct > .25 ? '#ccaa00' : '#cc2200';
    ctx.fillRect(bx, by, bw * pct, 7);
    if (e.frozen > 0) { ctx.fillStyle = 'rgba(100,180,255,.5)'; ctx.fillRect(bx, by, bw, 7); }
    if (e.isBoss) {
      ctx.font = 'bold 12px Noto Sans KR'; ctx.textAlign = 'center'; ctx.fillStyle = '#ff3355';
      ctx.fillText(e.name, e.x, by - 5);
    }
  }
  ctx.restore();
}

function drawSlime(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const sq = 1 + Math.sin(timer * 6 + e.walkPhase) * .14;
    ctx.scale(sq, 2 - sq);
    const g = ctx.createRadialGradient(-R * .2, -R * .3, 1, 0, 0, R);
    g.addColorStop(0, '#88ffaa'); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.shadowColor = e.col; ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.ellipse(0, 0, R, R * .85, 0, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
    ctx.fillStyle = 'rgba(255,255,255,.55)';
    ctx.beginPath(); ctx.ellipse(-R * .2, -R * .3, R * .2, R * .12, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#001a00';
    ctx.beginPath(); ctx.arc(-R * .3, -R * .1, R * .18, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .3, -R * .1, R * .18, 0, Math.PI * 2); ctx.fill();
  });
}
function drawBat(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const flap = Math.sin(timer * 18 + e.walkPhase) * .4;
    ctx.fillStyle = e.col2 || '#5a2080';
    ctx.beginPath(); ctx.ellipse(-R * 1.8, flap * R, R * 1.2, R * .5, -.3, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(R * 1.8, flap * R, R * 1.2, R * .5, .3, 0, Math.PI * 2); ctx.fill();
    const g = ctx.createRadialGradient(0, 0, 1, 0, 0, R);
    g.addColorStop(0, lighten(e.col, 30)); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, 0, R, R * 1.1, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ff4400'; ctx.shadowColor = '#ff4400'; ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.arc(-R * .28, -R * .2, R * .2, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .28, -R * .2, R * .2, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  });
}
function drawSkeleton(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const w = Math.sin(e.walkPhase) * .15;
    ctx.strokeStyle = '#d4c8a0'; ctx.lineWidth = 3; ctx.lineCap = 'round';
    ctx.save(); ctx.rotate(w + .5); ctx.beginPath(); ctx.moveTo(-R * .25, R * .2); ctx.lineTo(-R * .2, R * .85); ctx.stroke(); ctx.restore();
    ctx.save(); ctx.rotate(-w - .5); ctx.beginPath(); ctx.moveTo(R * .25, R * .2); ctx.lineTo(R * .2, R * .85); ctx.stroke(); ctx.restore();
    ctx.strokeStyle = '#d4c8a0'; ctx.lineWidth = 2;
    for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(0, -R * .6 + i * R * .28, R * .5, .2, Math.PI - .2); ctx.stroke(); }
    ctx.save(); ctx.rotate(-w); ctx.beginPath(); ctx.moveTo(R * .6, -R * .5); ctx.lineTo(R * 1.1, -R * .05); ctx.stroke(); ctx.restore();
    ctx.save(); ctx.rotate(w); ctx.beginPath(); ctx.moveTo(-R * .6, -R * .5); ctx.lineTo(-R * 1.1, -R * .05); ctx.stroke(); ctx.restore();
    ctx.fillStyle = '#d4c8a0'; ctx.beginPath(); ctx.arc(0, -R * .72, R * .65, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#111'; ctx.beginPath(); ctx.ellipse(-R * .25, -R * .8, R * .22, R * .18, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(R * .25, -R * .8, R * .22, R * .18, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(0,220,255,.75)'; ctx.shadowColor = '#00ccff'; ctx.shadowBlur = 7;
    ctx.beginPath(); ctx.arc(-R * .25, -R * .8, R * .12, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .25, -R * .8, R * .12, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  });
}
function drawOrc(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const w = Math.sin(e.walkPhase) * .1;
    if (e.charging) { ctx.shadowColor = '#ff8800'; ctx.shadowBlur = 22; }
    ctx.strokeStyle = e.col2; ctx.lineWidth = 7; ctx.lineCap = 'round';
    ctx.save(); ctx.rotate(w + .4); ctx.beginPath(); ctx.moveTo(-R * .4, R * .3); ctx.lineTo(-R * .35, R); ctx.stroke(); ctx.restore();
    ctx.save(); ctx.rotate(-w - .4); ctx.beginPath(); ctx.moveTo(R * .4, R * .3); ctx.lineTo(R * .35, R); ctx.stroke(); ctx.restore();
    const g = ctx.createRadialGradient(0, -R * .2, 1, 0, 0, R * 1.1);
    g.addColorStop(0, lighten(e.col, 20)); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(0, -R * .15, R * .9, R * 1.05, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = e.col; ctx.lineWidth = 8;
    ctx.save(); ctx.rotate(-w - .2); ctx.beginPath(); ctx.moveTo(R * .8, -R * .4); ctx.lineTo(R * 1.3, R * .2); ctx.stroke(); ctx.restore();
    ctx.save(); ctx.rotate(w + .2); ctx.beginPath(); ctx.moveTo(-R * .8, -R * .4); ctx.lineTo(-R * 1.3, R * .2); ctx.stroke(); ctx.restore();
    ctx.fillStyle = e.col; ctx.beginPath(); ctx.ellipse(0, -R * 1.0, R * .75, R * .65, 0, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#eeddcc';
    ctx.beginPath(); ctx.moveTo(-R * .35, -R * .6); ctx.lineTo(-R * .55, -R * .2); ctx.lineTo(-R * .2, -R * .55); ctx.fill();
    ctx.beginPath(); ctx.moveTo(R * .35, -R * .6); ctx.lineTo(R * .55, -R * .2); ctx.lineTo(R * .2, -R * .55); ctx.fill();
    ctx.fillStyle = '#ff3300'; ctx.shadowColor = '#ff3300'; ctx.shadowBlur = 8;
    ctx.beginPath(); ctx.arc(-R * .28, -R * 1.08, R * .22, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .28, -R * 1.08, R * .22, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  });
}
function drawMageE(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const float = Math.sin(timer * 2.5 + e.x) * 4;
    ctx.translate(0, float);
    const g = ctx.createRadialGradient(0, 0, 1, 0, 0, R * 1.2);
    g.addColorStop(0, lighten(e.col, 20)); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-R, R * .6); ctx.lineTo(R, R * .6); ctx.lineTo(R * .7, -R * .5); ctx.lineTo(-R * .7, -R * .5); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(200,100,255,.9)'; ctx.shadowColor = '#cc44ff'; ctx.shadowBlur = 16;
    ctx.beginPath(); ctx.arc(R * .9, -R * .2, R * .4, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
    ctx.fillStyle = e.col; ctx.beginPath(); ctx.arc(0, -R * .85, R * .6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#330066'; ctx.beginPath(); ctx.moveTo(-R * .7, -R * .7); ctx.lineTo(0, -R * 1.8); ctx.lineTo(R * .7, -R * .7); ctx.closePath(); ctx.fill();
    ctx.fillStyle = 'rgba(200,100,255,.95)'; ctx.shadowColor = '#cc44ff'; ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.arc(-R * .2, -R * .9, R * .18, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .2, -R * .9, R * .18, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  });
}
function drawDemon(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const wf = Math.sin(timer * 4 + e.walkPhase) * .25;
    ctx.fillStyle = 'rgba(150,0,0,.75)';
    ctx.beginPath(); ctx.moveTo(-R * .3, -R * .4); ctx.lineTo(-R * 2.2, -R * 1.2 + wf * R); ctx.lineTo(-R * 1.5, R * .2); ctx.lineTo(-R * .5, R * .1); ctx.closePath(); ctx.fill();
    ctx.beginPath(); ctx.moveTo(R * .3, -R * .4); ctx.lineTo(R * 2.2, -R * 1.2 + wf * R); ctx.lineTo(R * 1.5, R * .2); ctx.lineTo(R * .5, R * .1); ctx.closePath(); ctx.fill();
    const g = ctx.createRadialGradient(0, 0, 1, 0, 0, R);
    g.addColorStop(0, '#e05050'); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(255,0,0,.3)'; ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 12;
    ctx.beginPath(); ctx.arc(0, -R * .1, R * .35, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
    ctx.fillStyle = e.col; ctx.beginPath(); ctx.arc(0, -R * .9, R * .62, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#550000';
    ctx.beginPath(); ctx.moveTo(-R * .35, -R * 1.3); ctx.quadraticCurveTo(-R * .9, -R * 2.0, -R * .5, -R * 1.7); ctx.lineTo(-R * .2, -R * 1.3); ctx.fill();
    ctx.beginPath(); ctx.moveTo(R * .35, -R * 1.3); ctx.quadraticCurveTo(R * .9, -R * 2.0, R * .5, -R * 1.7); ctx.lineTo(R * .2, -R * 1.3); ctx.fill();
    ctx.fillStyle = '#ff0000'; ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 12;
    ctx.beginPath(); ctx.arc(-R * .24, -R * .95, R * .2, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(R * .24, -R * .95, R * .2, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
  });
}
function drawGhost(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const float = Math.sin(timer * 2 + e.x) * 6;
    ctx.save(); ctx.translate(0, float);
    const alpha = .5 + Math.sin(timer * 3) * .2;
    ctx.globalAlpha = alpha;
    const g = ctx.createRadialGradient(0, 0, 1, 0, 0, R);
    g.addColorStop(0, 'rgba(255,255,255,.8)'); g.addColorStop(1, 'rgba(180,180,200,.15)');
    ctx.fillStyle = g;
    ctx.beginPath();
    ctx.arc(0, -R * .2, R, 0, Math.PI, true);
    ctx.lineTo(-R, R * .5);
    ctx.quadraticCurveTo(-R * .6, R * .3, -R * .3, R * .6);
    ctx.quadraticCurveTo(0, R * .3, R * .3, R * .6);
    ctx.quadraticCurveTo(R * .6, R * .3, R, R * .5);
    ctx.closePath(); ctx.fill();
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#222'; ctx.shadowColor = '#00aaff'; ctx.shadowBlur = 8;
    ctx.beginPath(); ctx.ellipse(-R * .28, -R * .25, R * .2, R * .25, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(R * .28, -R * .25, R * .2, R * .25, 0, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0; ctx.restore();
  });
}
function drawGolem(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const shake = e.charging ? (Math.random() - .5) * 3 : 0;
    ctx.translate(shake, shake);
    ctx.fillStyle = e.col2; ctx.fillRect(-R * .6, -R * .2, R * 1.2, R * 1.2);
    const g = ctx.createRadialGradient(-R * .2, -R * .2, 2, 0, 0, R);
    g.addColorStop(0, lighten(e.col, 20)); g.addColorStop(1, e.col);
    ctx.fillStyle = g; ctx.fillRect(-R, -R, R * 2, R * 1.8);
    ctx.fillStyle = 'rgba(0,0,0,.35)'; ctx.fillRect(-R, R * .3, R * 2, R * .3);
    ctx.fillStyle = '#ff4400'; ctx.shadowColor = '#ff4400'; ctx.shadowBlur = 14;
    ctx.beginPath(); ctx.ellipse(-R * .3, -R * .3, R * .3, R * .2, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(R * .3, -R * .3, R * .3, R * .2, 0, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;
    // Cracks
    ctx.strokeStyle = 'rgba(0,0,0,.4)'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(-R * .5, -R * .6); ctx.lineTo(-R * .2, -R * .1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(R * .3, -R * .5); ctx.lineTo(R * .1, R * .2); ctx.stroke();
  });
}
function drawBossGeneric(e) {
  const R = e.radius;
  drawEnemyBase(e, R, (e, R, ctx) => {
    const rage = e.rage || e.enrage;
    const pulse = 1 + Math.sin(timer * 8) * (rage ? .12 : .05);
    ctx.scale(pulse, pulse);
    if (rage) { ctx.shadowColor = '#ff0000'; ctx.shadowBlur = 30; }

    const g = ctx.createRadialGradient(-R * .3, -R * .3, 2, 0, 0, R);
    g.addColorStop(0, lighten(e.col, 40)); g.addColorStop(1, e.col);
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(0, 0, R, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;

    // Inner glow
    ctx.fillStyle = e.enrage ? 'rgba(255,0,255,.3)' : (e.rage ? 'rgba(255,50,0,.25)' : 'rgba(255,255,255,.12)');
    ctx.beginPath(); ctx.arc(0, 0, R * .55, 0, Math.PI * 2); ctx.fill();

    // Eyes
    ctx.fillStyle = e.enrage ? '#ff00ff' : '#ff0000';
    ctx.shadowColor = e.enrage ? '#ff00ff' : '#ff3300'; ctx.shadowBlur = 18;
    ctx.beginPath(); ctx.ellipse(-R * .3, -R * .2, R * .22, R * .15, 0, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(R * .3, -R * .2, R * .22, R * .15, 0, 0, Math.PI * 2); ctx.fill();
    ctx.shadowBlur = 0;

    // Rotating spikes
    const spikes = e.enrage ? 8 : 6;
    for (let i = 0; i < spikes; i++) {
      const a = (i / spikes) * Math.PI * 2 + timer * (e.rage ? 2.5 : 1.5);
      const rx = Math.cos(a) * R, ry = Math.sin(a) * R;
      ctx.fillStyle = lighten(e.col, 30);
      ctx.beginPath();
      ctx.moveTo(rx, ry);
      ctx.lineTo(Math.cos(a + .25) * R * .65, Math.sin(a + .25) * R * .65);
      ctx.lineTo(Math.cos(a) * (R + 16 + (e.enrage ? 8 : 0)), Math.sin(a) * (R + 16 + (e.enrage ? 8 : 0)));
      ctx.lineTo(Math.cos(a - .25) * R * .65, Math.sin(a - .25) * R * .65);
      ctx.closePath(); ctx.fill();
    }
  });
}

function drawEnemies() {
  for (const e of G.enemies) {
    if (!e.alive && !e.dying) continue;
    const drawFn = e.draw || drawBossGeneric;
    drawFn(e);
  }
}

function drawProjs() {
  for (const pr of PROJS) {
    if (!pr.alive) continue;
    ctx.save();
    if (pr.emoji) {
      ctx.shadowColor = pr.col; ctx.shadowBlur = 14;
      ctx.font = `${pr.sz * 2}px serif`; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(pr.emoji, pr.x, pr.y);
    } else {
      ctx.fillStyle = pr.col; ctx.shadowColor = pr.col; ctx.shadowBlur = 16;
      ctx.beginPath(); ctx.arc(pr.x, pr.y, pr.sz, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = .3; ctx.shadowBlur = 0;
      ctx.beginPath(); ctx.arc(pr.x - pr.vx * .018, pr.y - pr.vy * .018, pr.sz * .65, 0, Math.PI * 2); ctx.fill();
    }
    ctx.shadowBlur = 0; ctx.restore();
  }
}

function drawItems() {
  for (const it of G.items) {
    if (!it.alive) continue;
    const bob = Math.sin(timer * 5 + it.x) * 3;
    ctx.save();
    ctx.shadowColor = it.type === 'hp' ? '#22ff88' : '#44aaff'; ctx.shadowBlur = 14;
    ctx.font = '18px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(it.type === 'hp' ? '❤️' : '💙', it.x, it.y + bob);
    ctx.globalAlpha = .18 + Math.sin(timer * 4) * .08;
    ctx.strokeStyle = it.type === 'hp' ? '#22ff88' : '#44aaff'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(it.x, it.y + bob, 12, 0, Math.PI * 2); ctx.stroke();
    ctx.shadowBlur = 0; ctx.restore();
  }
}

// ── HUD UPDATE ────────────────────────────────────────────
function updateHUD() {
  if (!G) return;
  const p = G.player;
  document.getElementById('hp-fill').style.width = Math.max(0, (p.hp / p.maxHp) * 100) + '%';
  document.getElementById('hp-txt').textContent = `${Math.ceil(p.hp)}/${p.maxHp}`;
  document.getElementById('mp-fill').style.width = Math.max(0, (p.mp / p.maxMp) * 100) + '%';
  document.getElementById('xp-fill').style.width = Math.min(100, (p.xp / p.xpNext) * 100) + '%';
  document.getElementById('s-lv').textContent = p.level;
  document.getElementById('s-atk').textContent = Math.round(p.atk * (p._atkMult || 1));
  document.getElementById('s-kill').textContent = p.kills;
  document.getElementById('s-gold').textContent = p.gold;
  document.getElementById('hud-name').textContent = CLASSES[p.clsId].name;

  // Timer
  const el = G.elapsed;
  const m = String(Math.floor(el / 60)).padStart(2, '0');
  const s = String(Math.floor(el % 60)).padStart(2, '0');
  document.getElementById('timer-box').textContent = `${m}:${s}`;
  document.getElementById('wave-lbl').textContent = `웨이브 ${G.waveIdx + 1}`;

  // Wave kills
  const goal = G.waveKillGoal;
  document.getElementById('kill-count').textContent = `${G.totalWaveKills} / ${goal}`;
  document.getElementById('wave-progress').style.width = Math.min(100, G.totalWaveKills / goal * 100) + '%';

  // Skill bar
  const sc = document.getElementById('sk-cont');
  sc.innerHTML = '';
  // Weapons
  for (const [wid, ws] of Object.entries(p.weapons)) {
    const def = WEAPON_DEFS[wid];
    const cd = ws.atkTimer > 0 ? ws.atkTimer : 0;
    const div = document.createElement('div');
    const rdy = cd <= 0;
    div.className = 'sk' + (rdy ? ' rdy' : '');
    div.innerHTML = `<div class="sk-ico">${def.icon}</div><div class="sk-k">W</div><div class="sk-lvl">Lv${ws.level}</div>`;
    if (cd > 0) div.innerHTML += `<div class="sk-cd">${cd.toFixed(1)}</div>`;
    div.title = `${def.name} Lv${ws.level}\n${def.desc}`;
    sc.appendChild(div);
  }
  // Actives
  for (const [aid, lv] of Object.entries(p.actives)) {
    const def = WEAPON_DEFS[aid];
    const cd = p.skillCds[def.key] || 0;
    const rdy = cd <= 0 && p.mp >= 20;
    const div = document.createElement('div');
    div.className = 'sk' + (rdy ? ' rdy' : '');
    div.innerHTML = `<div class="sk-ico">${def.icon}</div><div class="sk-k">${def.key}</div><div class="sk-lvl">Lv${lv}</div>`;
    if (cd > 0) div.innerHTML += `<div class="sk-cd">${cd.toFixed(1)}</div>`;
    div.title = `${def.name} [${def.key}] Lv${lv}\n${def.desc}`;
    sc.appendChild(div);
  }
  // Passives (small)
  for (const [pid, lv] of Object.entries(p.passives)) {
    const def = WEAPON_DEFS[pid];
    const div = document.createElement('div');
    div.className = 'sk lock';
    div.style.width = '36px'; div.style.height = '36px';
    div.innerHTML = `<div class="sk-ico" style="font-size:16px;">${def.icon}</div><div class="sk-lvl">Lv${lv}</div>`;
    div.title = `${def.name} Lv${lv}\n${def.desc}`;
    sc.appendChild(div);
  }
}

// ── DAMAGE NUMBERS ────────────────────────────────────────
function dnum(x, y, v, crit, col) {
  const el = document.createElement('div'); el.className = 'dnum';
  const r = canvas.getBoundingClientRect();
  el.style.cssText = `left:${r.left + x * scale - 20}px;top:${r.top + y * scale}px;` +
    `font-size:${crit ? 22 : 14}px;color:${crit ? '#ffff44' : (col || '#fff')};`;
  el.textContent = crit ? `${v}!!` : `${v}`;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 950);
}

// ── SCREEN SHAKE ──────────────────────────────────────────
function shakeScreen(amt, dur) { G.shake = Math.max(G.shake, amt); G.shakeTimer = Math.max(G.shakeTimer || 0, dur * .016); }

// ── TOAST ─────────────────────────────────────────────────
function showToast(ico, title, sub) {
  document.getElementById('toast-ico').textContent = ico;
  document.getElementById('toast-t').textContent = title;
  document.getElementById('toast-s').textContent = sub;
  const t = document.getElementById('toast');
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

// ── GAME STATES ───────────────────────────────────────────
function gameOver() {
  G.phase = 'over'; G.player.alive = false;
  const p = G.player;
  const el = document.getElementById('result-ov');
  document.getElementById('res-title').style.color = '#ff2244';
  document.getElementById('res-title').textContent = '💀 GAME OVER';
  document.getElementById('res-stats').innerHTML = `
    <div class="rs">생존 시간<b>${Math.floor(G.elapsed / 60)}분 ${Math.floor(G.elapsed % 60)}초</b></div>
    <div class="rs">웨이브<b>${G.waveIdx + 1}</b></div>
    <div class="rs">총 처치<b>${p.kills}</b></div>
    <div class="rs">레벨<b>Lv${p.level}</b></div>
    <div class="rs">점수<b>${p.score}</b></div>
    <div class="rs">최고 콤보<b>${p.maxCombo} HIT</b></div>`;
  setTimeout(() => el.style.display = 'flex', 800);
  sfx_death();
  // ── 결과 전송 ──
  try { window.parent.postMessage({ type:'dungeon_result', win:false, score:p.score, kills:p.kills, wave:G.waveIdx+1, level:p.level }, '*'); } catch(e){}
}

function gameWin() {
  G.phase = 'win';
  const p = G.player;
  const el = document.getElementById('result-ov');
  document.getElementById('res-title').style.color = '#f5c518';
  document.getElementById('res-title').textContent = '🏆 클리어!';
  document.getElementById('res-stats').innerHTML = `
    <div class="rs">생존 시간<b>${Math.floor(G.elapsed / 60)}분 ${Math.floor(G.elapsed % 60)}초</b></div>
    <div class="rs">총 처치<b>${p.kills}</b></div>
    <div class="rs">최종 레벨<b>Lv${p.level}</b></div>
    <div class="rs">점수<b>${p.score}</b></div>`;
  el.style.display = 'flex';
  sfx_clear(); sfx_clear();
  // ── 결과 전송 ──
  try { window.parent.postMessage({ type:'dungeon_result', win:true, score:p.score, kills:p.kills, wave:G.waveIdx+1, level:p.level }, '*'); } catch(e){}
}

function retryGame() {
  document.getElementById('result-ov').style.display = 'none';
  initGame(G.clsId);
}
function gotoTitle() {
  document.getElementById('result-ov').style.display = 'none';
  document.getElementById('lvlup').style.display = 'none';
  document.getElementById('title-ov').style.display = 'flex';
  G = null;
}

// ── TITLE ─────────────────────────────────────────────────
function buildTitle() {
  const grid = document.getElementById('char-grid');
  grid.innerHTML = '';
  const stars = (n, max = 5) => [...Array(max)].map((_, i) => `<span class="cstar" style="color:${i < n ? '#f5c518':'#222'}">★</span>`).join('');
  for (const [id, c] of Object.entries(CLASSES)) {
    const div = document.createElement('div'); div.className = 'ccard'; div.id = 'cc-' + id;
    div.onclick = () => {
      selClsId = id;
      document.querySelectorAll('.ccard').forEach(x => x.classList.remove('sel'));
      div.classList.add('sel');
      document.getElementById('start-btn').disabled = false;
      ensureAudio();
    };
    div.innerHTML = `<div class="ccard-ico">${c.icon}</div>
      <div class="ccard-name">${c.name}</div>
      <div class="ccard-role">${c.role}</div>
      <div class="cstat-row">
        <div class="cs">공격 ${stars(c.stars['공격'])}</div>
        <div class="cs">방어 ${stars(c.stars['방어'])}</div>
        <div class="cs">속도 ${stars(c.stars['속도'])}</div>
        <div class="cs">사거리 ${stars(c.stars['사거리'])}</div>
      </div>
      <div class="ccard-desc">${c.desc}</div>`;
    grid.appendChild(div);
  }
}

function startGame() {
  if (!selClsId) return;
  document.getElementById('title-ov').style.display = 'none';
  initGame(selClsId);
}

// ── AUDIO ────────────────────────────────────────────────
let ACtx = null;
function ensureAudio() { if (!ACtx) try { ACtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){} }
function beep(f, t, d, v=.22, delay=0) {
  if (!ACtx) return;
  try {
    const o = ACtx.createOscillator(), g = ACtx.createGain();
    o.connect(g); g.connect(ACtx.destination);
    o.type = t; o.frequency.value = f;
    const ts = ACtx.currentTime + delay;
    g.gain.setValueAtTime(0,ts); g.gain.linearRampToValueAtTime(v,ts+.005); g.gain.exponentialRampToValueAtTime(.001,ts+d);
    o.start(ts); o.stop(ts+d+.05);
  } catch(e){}
}
const sfx_atk = () => { ensureAudio(); beep(300,'square',.05,.1); };
const sfx_hit = () => { ensureAudio(); beep(130,'sawtooth',.1,.2); };
const sfx_kill = () => { ensureAudio(); beep(400,'sine',.08,.12); beep(600,'sine',.06,.1,.05); };
const sfx_skill = () => { ensureAudio(); beep(500,'sine',.18,.3); beep(700,'sine',.12,.22,.08); };
const sfx_lvlup = () => { ensureAudio(); [523,659,784,1047].forEach((f,i)=>beep(f,'sine',.3,.35,i*.1)); };
const sfx_clear = () => { ensureAudio(); [523,659,784,523,659,784,1047].forEach((f,i)=>beep(f,'sine',.25,.35,i*.11)); };
const sfx_death = () => { ensureAudio(); for(let i=0;i<5;i++) beep(200-i*25,'sawtooth',.22,.28,i*.08); };
const sfx_buy = () => { ensureAudio(); beep(700,'sine',.18,.25); beep(900,'sine',.14,.2,.09); };
const sfx_boss = () => { ensureAudio(); for(let i=0;i<4;i++) beep(60+i*12,'sawtooth',.45,.45,i*.22); };
const sfx_item = () => { ensureAudio(); beep(900,'sine',.1,.2); };

// ── MAIN LOOP ─────────────────────────────────────────────
function loop(ts) {
  const dt = Math.min((ts - lastTs) / 1000, .05);
  lastTs = ts;
  timer += dt;

  if (G && G.phase === 'play' && !G.paused) tick(dt);

  render();
  if (G) updateHUD();
  flushJ();
  RAF = requestAnimationFrame(loop);
}

function render() {
  ctx.save();
  if (G && G.shakeTimer > 0 && G.shake > 0) {
    const s = G.shake * G.shakeTimer;
    ctx.translate((Math.random() - .5) * s, (Math.random() - .5) * s);
    G.shake *= .85;
  }
  ctx.fillStyle = '#07050f'; ctx.fillRect(0, 0, GW, GH);

  if (G) {
    drawBG();
    drawSlashes();
    drawItems();
    drawProjs();
    drawEnemies();
    drawPlayer();
    drawP();
    drawWaves();
  } else {
    drawTitleBG();
  }
  ctx.restore();
}

function drawTitleBG() {
  ctx.fillStyle = '#07050f'; ctx.fillRect(0, 0, GW, GH);
  ctx.save(); ctx.globalAlpha = .04 + Math.sin(timer * .6) * .015;
  ctx.font = '900 80px Black Han Sans'; ctx.fillStyle = '#ff6600';
  ctx.textAlign = 'center'; ctx.fillText('던전 런', GW / 2, GH / 2 + 35);
  ctx.restore();
  if (Math.random() < .35) spawnP(Math.random() * GW, Math.random() * GH, { n:2, col:['#ff6600','#ffaa00','#cc44ff'], glow:true, sMin:1, sMax:3, dMin:.01, dMax:.02 });
  tickP(.016); drawP();
}

// ── MOBILE CONTROLS ──────────────────────────────────────
(function setupMobile() {
  const dpad = document.createElement('div');
  dpad.id = 'mobile-dpad';
  dpad.style.cssText = `display:none;position:fixed;bottom:72px;left:10px;width:130px;height:130px;z-index:999;`;
  dpad.innerHTML = `
    <style>
    .dpb{position:absolute;width:42px;height:42px;background:rgba(245,200,66,.1);border:1px solid rgba(245,200,66,.25);
      border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px;color:rgba(245,200,66,.6);
      cursor:pointer;user-select:none;-webkit-user-select:none;}
    .dpb:active{background:rgba(245,200,66,.3);}
    #dpu{top:0;left:44px;}#dpd{bottom:0;left:44px;}#dpl{top:44px;left:0;}#dpr{top:44px;right:0;}
    @media(pointer:coarse){#mobile-dpad,#mobile-atk{display:flex!important;}}
    </style>
    <div class="dpb" id="dpu">▲</div>
    <div class="dpb" id="dpl">◀</div>
    <div class="dpb" id="dpr">▶</div>
    <div class="dpb" id="dpd">▼</div>`;
  document.getElementById('root').appendChild(dpad);

  const atkBtn = document.createElement('div');
  atkBtn.id = 'mobile-atk';
  atkBtn.style.cssText = `display:none;position:fixed;bottom:90px;right:20px;width:60px;height:60px;
    border-radius:50%;background:rgba(255,80,80,.15);border:2px solid rgba(255,80,80,.45);z-index:999;
    align-items:center;justify-content:center;font-size:24px;cursor:pointer;user-select:none;`;
  atkBtn.textContent = '🔮';
  document.getElementById('root').appendChild(atkBtn);

  const map = { dpu:'ArrowUp', dpd:'ArrowDown', dpl:'ArrowLeft', dpr:'ArrowRight' };
  Object.entries(map).forEach(([id, key]) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('touchstart', e => { e.preventDefault(); KEYS[key] = true; }, { passive: false });
    el.addEventListener('touchend', e => { e.preventDefault(); KEYS[key] = false; }, { passive: false });
  });
  atkBtn.addEventListener('touchstart', e => { e.preventDefault(); JKEYS['Q'] = true; ensureAudio(); }, { passive: false });

  // Skill Q/E/R buttons
  const skillBtns = [['Q','💫','120px'],['E','💥','190px'],['R','⏱️','260px']];
  skillBtns.forEach(([k, ico, b]) => {
    const btn = document.createElement('div');
    btn.style.cssText = `display:none;position:fixed;bottom:${b};right:15px;width:44px;height:44px;
      border-radius:8px;background:rgba(50,255,150,.1);border:1px solid rgba(50,255,150,.3);z-index:999;
      align-items:center;justify-content:center;font-size:20px;cursor:pointer;user-select:none;`;
    btn.textContent = ico;
    btn.className = 'mobile-skill-btn';
    btn.addEventListener('touchstart', e => { e.preventDefault(); JKEYS[k] = true; ensureAudio(); }, { passive: false });
    document.getElementById('root').appendChild(btn);
  });

  // Show on touch devices
  const mq = window.matchMedia('(pointer: coarse)');
  const toggle = (e) => {
    const show = e.matches ? 'flex' : 'none';
    dpad.style.display = show;
    atkBtn.style.display = show;
    document.querySelectorAll('.mobile-skill-btn').forEach(b => b.style.display = show);
  };
  mq.addEventListener('change', toggle);
  toggle(mq);
})();

// ── BOOT ──────────────────────────────────────────────────
buildTitle();
RAF = requestAnimationFrame(loop);
</script>
</body>
</html>"""

def render():
    import streamlit as st
    import streamlit.components.v1 as components
    from utils.database import load_db, save_db, log_tx, atomic_add_cash
    from utils.config import USERS_FILE
    from utils.core import sync_user_data

    uid = st.session_state.get('logged_in_user', '')

    # ── 던전 통계 로드 ──
    if 'dungeon_stats' not in st.session_state:
        users = load_db(USERS_FILE, {})
        u_data = users.get(uid, {})
        st.session_state.dungeon_stats = u_data.get('dungeon_stats', {
            'best_score': 0, 'best_kills': 0, 'clears': 0, 'games_played': 0
        })

    dstats = st.session_state.dungeon_stats

    # ── 게임 결과 수신 처리 ──
    qp = st.query_params
    # ✅ [BUG FIX] dungeon_result_processed 플래그를 query param 존재 여부 기반으로 판단
    # 이전: 세션이 살아있는 동안 두 번째 판부터 결과가 무시됨
    # 수정: query param이 있을 때만 처리하고, 처리 직후 query param을 클리어
    if qp.get('dungeon_score') and not st.session_state.get('dungeon_result_processed'):
        st.session_state.dungeon_result_processed = True
        is_win = qp.get('dungeon_win') == 'true'
        score  = int(qp.get('dungeon_score', 0))
        kills  = int(qp.get('dungeon_kills', 0))

        dstats['games_played'] = dstats.get('games_played', 0) + 1
        if score > dstats.get('best_score', 0):
            dstats['best_score'] = score
        if kills > dstats.get('best_kills', 0):
            dstats['best_kills'] = kills

        # ── 주간 랭킹 저장 ──
        from datetime import timedelta
        now_kst = datetime.now(KST)
        week_start_str = (now_kst - timedelta(days=now_kst.weekday())).replace(
            hour=0,minute=0,second=0,microsecond=0).strftime('%Y-%m-%d')
        weekly = st.session_state.get('dungeon_weekly', {})
        if weekly.get('week_start') != week_start_str:
            weekly = {'week_start': week_start_str, 'score': 0, 'kills': 0}
        if score > weekly.get('score', 0):
            weekly['score'] = score
            weekly['kills'] = kills
        st.session_state.dungeon_weekly = weekly
        if is_win:
            dstats['clears'] = dstats.get('clears', 0) + 1
            clear_reward = 200_000_000
            atomic_add_cash(uid, clear_reward)
            st.session_state.global_cash += clear_reward
            log_tx(uid, "던전", f"던전런 클리어 (점수:{score}, 킬:{kills})", clear_reward)
            st.success(f"🏆 던전 클리어 보상: +{clear_reward:,}원!")
        else:
            # 점수 기반 보상
            score_reward = score * 1000
            if score_reward > 0:
                atomic_add_cash(uid, score_reward)
                st.session_state.global_cash += score_reward
                log_tx(uid, "던전", f"던전런 점수 보상 (점수:{score}, 킬:{kills})", score_reward)
            else:
                # score=0이어도 플레이 기록은 남김
                log_tx(uid, "던전", f"던전런 종료 (점수:{score}, 킬:{kills})", 0)
        st.session_state.dungeon_stats = dstats

        # ── dungeon_weekly를 users DB에 직접 반영 ──
        from utils.database import load_db, save_db
        from utils.config import USERS_FILE
        _users = load_db(USERS_FILE, {})
        if uid in _users:
            _users[uid]['dungeon_stats'] = dstats
            _users[uid]['dungeon_weekly'] = st.session_state.get('dungeon_weekly', {})
            save_db(USERS_FILE, _users)

        # ✅ [BUG FIX] dungeon_stats는 sync_user_data()에 포함되므로 별도 save_db 불필요
        # sync_user_data()가 dungeon_stats를 포함하여 저장함 (core.py 수정 연동)
        sync_user_data()

        # ✅ [BUG FIX] 처리 후 query params 클리어 → 새로고침/재진입 시 중복 처리 방지
        st.query_params.clear()
        # ✅ [BUG FIX] 다음 판을 위해 처리 플래그 초기화
        del st.session_state['dungeon_result_processed']
        st.rerun()

    # 게임 헤더 UI
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0c1020,#111828);border:1px solid rgba(108,99,255,0.25);
      border-radius:16px;padding:16px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>
      <div style='font-size:2rem;'>⚔️</div>
      <div>
        <div style='font-family:"Black Han Sans",sans-serif;font-size:1.1rem;color:#e8f0ff;'>⚔️ 던전 런 REBORN</div>
        <div style='font-size:0.82rem;color:#8899bb;margin-top:2px;'>뱀서라이크 서바이벌. 사방에서 몰려오는 몬스터를 섬멸하고 보스를 격파하세요!</div>
        <div style='font-size:0.76rem;color:#6c63ff;margin-top:4px;'>🎮 WASD/방향키: 이동 | 자동 공격 | Q E R: 스킬 | 레벨업 시 무기/패시브 선택</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 내 던전 기록 표시 ──
    best_score  = dstats.get('best_score', 0)
    best_kills  = dstats.get('best_kills', 0)
    clears      = dstats.get('clears', 0)
    played      = dstats.get('games_played', 0)

    st.markdown(f"""
    <div style='display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap;'>
      <div style='background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.3);border-radius:10px;padding:10px 16px;flex:1;min-width:100px;text-align:center;'>
        <div style='color:#888;font-size:0.72rem;'>최고 점수</div>
        <div style='color:#FFD600;font-weight:900;font-size:1rem;'>{best_score:,}</div>
      </div>
      <div style='background:rgba(255,50,70,0.08);border:1px solid rgba(255,50,70,0.3);border-radius:10px;padding:10px 16px;flex:1;min-width:100px;text-align:center;'>
        <div style='color:#888;font-size:0.72rem;'>최고 킬</div>
        <div style='color:#FF4B4B;font-weight:900;font-size:1rem;'>{best_kills:,}</div>
      </div>
      <div style='background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.3);border-radius:10px;padding:10px 16px;flex:1;min-width:100px;text-align:center;'>
        <div style='color:#888;font-size:0.72rem;'>클리어</div>
        <div style='color:#00FF88;font-weight:900;font-size:1rem;'>{clears}회</div>
      </div>
      <div style='background:rgba(0,229,255,0.08);border:1px solid rgba(0,229,255,0.3);border-radius:10px;padding:10px 16px;flex:1;min-width:100px;text-align:center;'>
        <div style='color:#888;font-size:0.72rem;'>총 플레이</div>
        <div style='color:#00E5FF;font-weight:900;font-size:1rem;'>{played}판</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .block-container{padding:0!important;max-width:100%!important;}
    section[data-testid="stSidebar"]{display:none!important;}
    header{display:none!important;}footer{display:none!important;}
    iframe{border:none!important;}
    </style>
    """, unsafe_allow_html=True)

    st.caption("🎮 WASD/방향키: 이동 | 자동 공격 | Q E R: 스킬 | 레벨업 시 무기 선택! | 🏆 클리어 보상 2억원!")

    # postMessage 수신 리스너 (결과 → query param)
    # ✅ [BUG FIX] 리스너를 게임 iframe보다 먼저 렌더링하면 별도 iframe이라 메시지를 못 받을 수 있음
    # window.parent 기준으로 수신하므로 순서 상관없이 동작하지만,
    # 안전하게 게임 결과 수신 시 dungeon_result_processed 플래그도 초기화
    listener_html = """
    <script>
    window.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'dungeon_result') {
        const d = e.data;
        const url = new URL(window.parent.location.href);
        url.searchParams.set('dungeon_win',   d.win ? 'true' : 'false');
        url.searchParams.set('dungeon_score', d.score);
        url.searchParams.set('dungeon_kills', d.kills);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    st.components.v1.html(listener_html, height=0)
    components.html(GAME_HTML, height=840, scrolling=False)

if __name__ == "__main__":
    render()
