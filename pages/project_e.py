import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>던전 크러셔 DUNGEON CRUSHER</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Jua&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
:root{
  --orange:#ff6600;--orange2:#ffaa00;--red:#ff2222;--blue:#2244ff;
  --teal:#00ffcc;--purple:#cc44ff;--gold:#ffcc00;
  --bg:#06040e;--bg2:#0d0820;--surface:rgba(255,255,255,0.04);
}
body{background:var(--bg);font-family:'Noto Sans KR',sans-serif;overflow:hidden;width:100vw;height:100vh;display:flex;align-items:center;justify-content:center;}
canvas{image-rendering:pixelated;image-rendering:crisp-edges;}

#gw{position:relative;width:900px;height:580px;user-select:none;}

/* ── HUD ── */
#hud{
  position:absolute;top:0;left:0;right:0;height:56px;
  background:linear-gradient(180deg,rgba(6,4,14,0.98),rgba(6,4,14,0.75));
  border-bottom:1px solid rgba(255,100,0,0.4);
  display:flex;align-items:center;gap:12px;padding:0 14px;z-index:100;
}
.hud-name{font-family:'Black Han Sans',sans-serif;font-size:.95rem;color:var(--gold);letter-spacing:2px;min-width:60px;}
.bars{display:flex;flex-direction:column;gap:3px;}
.bar-row{display:flex;align-items:center;gap:5px;}
.bar-lbl{font-size:.52rem;color:#888;width:16px;text-align:right;letter-spacing:1px;}
.bar-bg{width:140px;height:10px;background:rgba(255,255,255,0.07);border-radius:2px;border:1px solid rgba(255,255,255,0.08);overflow:hidden;position:relative;}
.bar-fill{height:100%;border-radius:2px;transition:width .12s;}
.bar-bg .bar-inner-text{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:.42rem;color:rgba(255,255,255,0.6);font-weight:700;}
#hp-bar{background:linear-gradient(90deg,#660000,#cc1111,#ff5555);}
#mp-bar{background:linear-gradient(90deg,#001166,#1133cc,#4488ff);}
#xp-bar-bg{width:100px;height:5px;background:rgba(255,255,255,0.07);border-radius:2px;border:1px solid rgba(255,255,255,0.05);overflow:hidden;margin-left:4px;}
#xp-bar{height:100%;background:linear-gradient(90deg,#226600,#44cc00,#88ff44);border-radius:2px;transition:width .2s;}

.stat-grid{display:flex;gap:6px;margin-left:auto;}
.stat-box{display:flex;flex-direction:column;align-items:center;background:rgba(255,255,255,0.04);border:1px solid rgba(255,150,0,0.15);border-radius:3px;padding:2px 7px;min-width:44px;}
.stat-val{font-size:.8rem;font-weight:900;color:var(--gold);}
.stat-lbl{font-size:.42rem;color:#666;letter-spacing:.5px;}
.floor-tag{font-family:'Black Han Sans',sans-serif;font-size:.78rem;color:#fff;background:rgba(255,100,0,0.15);border:1px solid rgba(255,100,0,0.4);border-radius:3px;padding:2px 9px;letter-spacing:1px;}
.buff-icons{display:flex;gap:3px;font-size:.9rem;}

/* ── CANVAS ── */
#gc{position:absolute;top:56px;left:0;width:900px;height:468px;background:#000;display:block;}

/* ── COMBO ── */
#combo{
  position:absolute;top:66px;right:14px;z-index:110;
  text-align:right;pointer-events:none;transition:opacity .3s;
}
#combo-count{font-family:'Black Han Sans',sans-serif;font-size:2.2rem;color:#ffcc00;text-shadow:0 0 20px rgba(255,200,0,.8),2px 2px 0 rgba(0,0,0,.8);line-height:1;}
#combo-label{font-size:.6rem;color:#ff9900;letter-spacing:3px;}

/* ── BOSS HP ── */
#bossHpWrap{
  position:absolute;top:62px;left:50%;transform:translateX(-50%);
  width:380px;pointer-events:none;z-index:120;opacity:0;transition:opacity .3s;
}
#bossHpWrap.show{opacity:1;}
#bossNameLbl{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:.78rem;color:#ff5555;margin-bottom:2px;text-shadow:0 0 8px rgba(255,0,0,.5);letter-spacing:1px;}
#bossHpBg{height:8px;background:rgba(255,255,255,0.05);border-radius:2px;border:1px solid rgba(255,60,60,.3);overflow:hidden;}
#bossHpFill{height:100%;background:linear-gradient(90deg,#5a0000,#cc0000,#ff3333);border-radius:2px;transition:width .15s;}
#bossPhaseLabel{text-align:center;font-size:.5rem;color:#ff8888;margin-top:2px;letter-spacing:2px;}

/* ── SKILL BAR ── */
#skillBar{
  position:absolute;bottom:0;left:0;right:0;height:56px;
  background:linear-gradient(0deg,rgba(6,4,14,0.98),rgba(6,4,14,0.75));
  border-top:1px solid rgba(255,100,0,0.4);
  display:flex;align-items:center;justify-content:center;gap:5px;padding:0 10px;z-index:100;
}
.sk{
  width:46px;height:46px;border-radius:4px;
  background:rgba(255,255,255,0.04);border:1px solid rgba(255,150,0,0.2);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:1.25rem;position:relative;cursor:default;
}
.sk.rdy{border-color:rgba(255,170,0,.7);box-shadow:0 0 8px rgba(255,150,0,.3),inset 0 0 8px rgba(255,150,0,.05);}
.sk.cool{opacity:.35;}
.sk.active{transform:scale(.92);border-color:#fff;}
.sk-cd{position:absolute;inset:0;background:rgba(0,0,0,.75);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:.68rem;color:var(--gold);font-weight:900;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.38rem;color:#777;}
.sk-mp{position:absolute;top:2px;left:3px;font-size:.38rem;color:#5599ff;}
.sk-name-bar{margin-left:10px;padding-left:10px;border-left:1px solid rgba(255,150,0,.15);font-size:.56rem;color:#666;max-width:200px;}
.sk-name-bar b{color:#ff9900;}
.controls{margin-left:auto;font-size:.5rem;color:#444;text-align:right;line-height:1.9;}

/* ── EQUIP MINI ── */
#equipMini{
  position:absolute;bottom:60px;left:10px;z-index:110;
  display:flex;gap:4px;pointer-events:none;
}
.equip-slot-mini{
  width:32px;height:32px;background:rgba(0,0,0,.6);border:1px solid rgba(255,150,0,.2);
  border-radius:3px;display:flex;align-items:center;justify-content:center;
  font-size:.85rem;position:relative;
}
.equip-slot-mini .rarity-gem{
  position:absolute;bottom:1px;right:1px;width:6px;height:6px;border-radius:50%;
}

/* ── OVERLAYS ── */
.ov{position:absolute;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;background:rgba(6,4,14,.95);}
.ov.hidden{display:none;}

/* ── TITLE ── */
#titleScreen{flex-direction:column;text-align:center;gap:0;}
.logo-wrap{margin-bottom:28px;}
.logo-main{font-family:'Black Han Sans',sans-serif;font-size:3.8rem;letter-spacing:8px;
  background:linear-gradient(135deg,#ff4400,#ff9900,#ffcc00,#ff6600);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(255,100,0,.5));line-height:1.1;}
.logo-en{font-size:.78rem;color:#555;letter-spacing:12px;margin-top:2px;}
.logo-sub{font-size:.6rem;color:#444;letter-spacing:4px;margin-top:6px;}
.char-grid{display:flex;gap:12px;margin-bottom:24px;}
.ccard{
  width:120px;background:rgba(255,255,255,.02);border:1px solid rgba(255,150,0,.12);
  border-radius:6px;padding:14px 8px;cursor:pointer;transition:all .2s;text-align:center;
}
.ccard:hover,.ccard.sel{border-color:rgba(255,170,0,.7);background:rgba(255,150,0,.06);transform:translateY(-5px);box-shadow:0 10px 30px rgba(255,100,0,.2);}
.ccard-icon{font-size:2.6rem;display:block;margin-bottom:7px;}
.ccard-name{font-family:'Black Han Sans',sans-serif;font-size:.8rem;color:var(--gold);letter-spacing:2px;}
.ccard-type{font-size:.52rem;color:#666;margin-top:2px;}
.ccard-stats{margin-top:8px;display:grid;grid-template-columns:1fr 1fr;gap:2px;}
.cstat{font-size:.48rem;color:#555;text-align:left;padding:1px 0;}
.cstat span{color:#888;}
.ccard.sel .cstat span{color:#ffaa44;}
.star-row{display:flex;justify-content:center;gap:1px;margin-top:6px;}
.star{font-size:.55rem;color:#333;}
.star.on{color:#ffcc00;}
.start-btn{
  padding:13px 52px;background:linear-gradient(135deg,#7a2e00,#ff5500);
  border:none;border-radius:4px;color:#fff;font-size:.95rem;
  font-family:'Black Han Sans',sans-serif;letter-spacing:4px;cursor:pointer;
  box-shadow:0 0 24px rgba(255,100,0,.4);transition:all .2s;
}
.start-btn:hover{transform:scale(1.06);box-shadow:0 0 36px rgba(255,100,0,.7);}
.start-btn:disabled{opacity:.25;cursor:default;transform:none;box-shadow:none;}
.version-tag{position:absolute;bottom:8px;right:10px;font-size:.42rem;color:#333;letter-spacing:2px;}

/* ── SHOP ── */
#shopScreen{flex-direction:column;text-align:center;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.8rem;color:var(--gold);letter-spacing:4px;margin-bottom:4px;}
.shop-gold{font-size:.75rem;color:#ffcc00;margin-bottom:20px;}
.shop-grid{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-bottom:20px;}
.shop-item{
  width:130px;background:rgba(255,255,255,.03);border:1px solid rgba(255,150,0,.15);
  border-radius:6px;padding:12px 8px;cursor:pointer;transition:all .2s;text-align:center;
}
.shop-item:hover:not(.cant){border-color:rgba(255,200,0,.6);background:rgba(255,180,0,.06);}
.shop-item.cant{opacity:.35;cursor:default;}
.si-icon{font-size:1.8rem;margin-bottom:5px;}
.si-name{font-size:.68rem;color:#ccc;font-weight:700;margin-bottom:2px;}
.si-desc{font-size:.52rem;color:#666;}
.si-price{font-size:.72rem;color:#ffcc00;font-weight:900;margin-top:5px;}
.si-price.cant{color:#555;}
.shop-cont-btn{padding:10px 36px;background:linear-gradient(135deg,#003344,#006699);border:none;border-radius:4px;color:#fff;font-family:'Black Han Sans',sans-serif;letter-spacing:3px;font-size:.85rem;cursor:pointer;transition:all .2s;}
.shop-cont-btn:hover{transform:scale(1.04);filter:brightness(1.2);}

/* ── STAGE CLEAR ── */
#stageClear{flex-direction:column;text-align:center;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:2.2rem;letter-spacing:4px;margin-bottom:8px;}
.clear-title{background:linear-gradient(135deg,#ffcc00,#ff9900);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 16px rgba(255,200,0,.5));}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;background:rgba(255,255,255,.03);border-radius:6px;padding:14px 20px;margin:10px 0;border:1px solid rgba(255,150,0,.1);}
.res-row{display:flex;justify-content:space-between;gap:16px;font-size:.7rem;color:#888;}
.res-row b{color:var(--gold);}
.drop-list{display:flex;gap:6px;justify-content:center;margin:8px 0;flex-wrap:wrap;}
.drop-item{padding:4px 10px;border-radius:3px;font-size:.6rem;border:1px solid rgba(255,150,0,.2);background:rgba(255,150,0,.06);color:#ffaa44;}
.drop-item.rare{border-color:rgba(100,150,255,.4);background:rgba(80,120,255,.06);color:#88aaff;}
.drop-item.epic{border-color:rgba(200,100,255,.4);background:rgba(180,80,255,.06);color:#cc88ff;}
.action-btns{display:flex;gap:8px;margin-top:10px;justify-content:center;}
.abtn{padding:9px 24px;border:none;border-radius:4px;cursor:pointer;font-family:'Black Han Sans',sans-serif;letter-spacing:2px;font-size:.8rem;transition:all .2s;}
.abtn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.btn-next{background:linear-gradient(135deg,#1a5500,#22aa00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#550000,#aa2200);color:#fff;}
.btn-title2{background:rgba(255,255,255,.07);color:#888;border:1px solid rgba(255,255,255,.08);}

/* ── GAME OVER ── */
#gameOver{flex-direction:column;text-align:center;}
.over-title{color:#ff2222;text-shadow:0 0 20px rgba(255,0,0,.5);}

/* ── ACHIEVEMENT POPUP ── */
#achiev{
  position:absolute;top:64px;left:50%;transform:translateX(-50%) translateY(-80px);
  background:linear-gradient(135deg,rgba(50,30,0,.95),rgba(80,50,0,.95));
  border:1px solid rgba(255,180,0,.5);border-radius:6px;padding:8px 20px;
  display:flex;align-items:center;gap:10px;z-index:300;
  box-shadow:0 4px 20px rgba(255,150,0,.3);transition:transform .35s ease;pointer-events:none;
}
#achiev.show{transform:translateX(-50%) translateY(0);}
#achiev-icon{font-size:1.4rem;}
#achiev-text{font-size:.62rem;color:#ffcc00;font-weight:700;letter-spacing:1px;}
#achiev-sub{font-size:.52rem;color:#aa7700;}

/* ── ITEM POPUP (drop) ── */
@keyframes itemFloat{0%{opacity:0;transform:translateY(0) scale(.8);}20%{opacity:1;transform:translateY(-10px) scale(1);}80%{opacity:1;transform:translateY(-30px);}100%{opacity:0;transform:translateY(-50px) scale(.9);}}
.item-float{position:absolute;pointer-events:none;animation:itemFloat 1.4s ease forwards;z-index:160;font-size:.65rem;font-weight:700;background:rgba(0,0,0,.7);padding:2px 6px;border-radius:3px;border:1px solid rgba(255,180,0,.4);color:#ffcc00;white-space:nowrap;}

/* ── BOSS WARNING ── */
@keyframes bwFlash{0%,100%{opacity:0;}15%,85%{opacity:1;}}
#bossWarn{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Black Han Sans',sans-serif;font-size:1.8rem;color:#ff2222;
  text-shadow:0 0 20px rgba(255,0,0,.9);letter-spacing:6px;
  animation:bwFlash 2s ease forwards;pointer-events:none;z-index:180;display:none;
  text-align:center;line-height:1.5;
}

/* ── DAMAGE NUMBERS ── */
@keyframes dmgUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-70px) scale(.65);}}
.dnum{position:absolute;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dmgUp 1s ease forwards;z-index:155;text-shadow:1px 1px 3px rgba(0,0,0,.9);}

/* ── MINIMAP ── */
#minimap{position:absolute;bottom:60px;right:10px;width:120px;height:28px;background:rgba(0,0,0,.7);border:1px solid rgba(255,150,0,.2);border-radius:3px;z-index:110;overflow:hidden;}
#minimapCanvas{width:120px;height:28px;}

/* ── PAUSE ── */
#pauseScreen{flex-direction:column;text-align:center;background:rgba(6,4,14,.85);}
.pause-title{font-family:'Black Han Sans',sans-serif;font-size:2.5rem;color:#fff;letter-spacing:6px;}
.pause-hint{font-size:.7rem;color:#555;margin-top:16px;letter-spacing:2px;}
</style>
</head>
<body>
<div id="gw">
  <!-- HUD -->
  <div id="hud">
    <div class="hud-name" id="hudName">캐릭터</div>
    <div class="bars">
      <div class="bar-row">
        <span class="bar-lbl">HP</span>
        <div class="bar-bg" style="width:130px"><div class="bar-fill" id="hp-bar" style="width:100%"></div><div class="bar-inner-text" id="hp-text"></div></div>
      </div>
      <div class="bar-row">
        <span class="bar-lbl">MP</span>
        <div class="bar-bg" style="width:130px"><div class="bar-fill" id="mp-bar" style="width:100%"></div></div>
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:3px;margin-left:6px;">
      <div style="font-size:.5rem;color:#666;">XP</div>
      <div id="xp-bar-bg"><div id="xp-bar" style="width:0%"></div></div>
      <div style="font-size:.48rem;color:#555;" id="xp-text">0 / 100</div>
    </div>
    <div class="stat-grid">
      <div class="stat-box"><div class="stat-val" id="s-lv">1</div><div class="stat-lbl">LV</div></div>
      <div class="stat-box"><div class="stat-val" id="s-kills">0</div><div class="stat-lbl">KILL</div></div>
      <div class="stat-box"><div class="stat-val" id="s-score">0</div><div class="stat-lbl">SCORE</div></div>
      <div class="stat-box"><div class="stat-val" id="s-gold">0</div><div class="stat-lbl">💰</div></div>
    </div>
    <div class="buff-icons" id="buffIcons"></div>
    <div class="floor-tag" id="floorTag">1-1</div>
  </div>

  <!-- CANVAS -->
  <canvas id="gc" width="900" height="468"></canvas>

  <!-- COMBO -->
  <div id="combo" style="opacity:0">
    <div id="combo-count">0</div>
    <div id="combo-label">COMBO</div>
  </div>

  <!-- BOSS HP -->
  <div id="bossHpWrap">
    <div id="bossNameLbl">보스</div>
    <div id="bossHpBg"><div id="bossHpFill" style="width:100%"></div></div>
    <div id="bossPhaseLabel"></div>
  </div>

  <!-- BOSS WARNING -->
  <div id="bossWarn">⚠ BOSS APPEAR ⚠<br><span style="font-size:1rem;color:#ff6600">전투 준비!</span></div>

  <!-- MINIMAP -->
  <div id="minimap"><canvas id="minimapCanvas" width="120" height="28"></canvas></div>

  <!-- EQUIP MINI -->
  <div id="equipMini">
    <div class="equip-slot-mini" id="eq-wpn" title="무기">🗡️</div>
    <div class="equip-slot-mini" id="eq-arm" title="방어구">🛡️</div>
    <div class="equip-slot-mini" id="eq-acc" title="장신구">💍</div>
  </div>

  <!-- SKILL BAR -->
  <div id="skillBar">
    <div id="skCont" style="display:flex;gap:5px;"></div>
    <div class="sk-name-bar" id="skDesc"></div>
    <div class="controls">← → 이동 &nbsp;|&nbsp; Z 점프(2단) &nbsp;|&nbsp; X 공격<br>A S D F G 스킬 &nbsp;|&nbsp; Space 회피 &nbsp;|&nbsp; P 일시정지</div>
  </div>

  <!-- ACHIEVEMENT POPUP -->
  <div id="achiev">
    <div id="achiev-icon">🏆</div>
    <div><div id="achiev-text">업적 달성!</div><div id="achiev-sub">설명</div></div>
  </div>

  <!-- ── OVERLAYS ── -->

  <!-- TITLE -->
  <div class="ov" id="titleScreen">
    <div>
      <div class="logo-wrap">
        <div class="logo-main">던전 크러셔</div>
        <div class="logo-en">DUNGEON CRUSHER</div>
        <div class="logo-sub">ULTIMATE EDITION</div>
      </div>
      <div class="char-grid" id="charGrid"></div>
      <div style="text-align:center">
        <button class="start-btn" id="startBtn" onclick="UI.startGame()" disabled>전투 시작 ▶</button>
      </div>
      <div class="version-tag">v2.0 · CLAUDE EDITION</div>
    </div>
  </div>

  <!-- SHOP -->
  <div class="ov hidden" id="shopScreen">
    <div>
      <div class="shop-title">🛒 상점</div>
      <div class="shop-gold" id="shopGoldText">보유 골드: 0💰</div>
      <div class="shop-grid" id="shopGrid"></div>
      <button class="shop-cont-btn" onclick="UI.continueFromShop()">다음 스테이지 →</button>
    </div>
  </div>

  <!-- STAGE CLEAR -->
  <div class="ov hidden" id="stageClear">
    <div>
      <div class="res-title clear-title">✦ STAGE CLEAR ✦</div>
      <div class="res-grid" id="clearGrid"></div>
      <div style="font-size:.6rem;color:#888;margin-bottom:4px;">획득 아이템</div>
      <div class="drop-list" id="dropList"></div>
      <div class="action-btns">
        <button class="abtn btn-next" onclick="UI.openShop()">상점 →</button>
        <button class="abtn btn-title2" onclick="UI.goTitle()">타이틀로</button>
      </div>
    </div>
  </div>

  <!-- GAME OVER -->
  <div class="ov hidden" id="gameOver">
    <div>
      <div class="res-title over-title">💀 GAME OVER</div>
      <div class="res-grid" id="overGrid"></div>
      <div class="action-btns">
        <button class="abtn btn-retry" onclick="UI.retryStage()">재도전 ↺</button>
        <button class="abtn btn-title2" onclick="UI.goTitle()">타이틀로</button>
      </div>
    </div>
  </div>

  <!-- PAUSE -->
  <div class="ov hidden" id="pauseScreen">
    <div>
      <div class="pause-title">⏸ PAUSE</div>
      <div class="pause-hint">P 키를 눌러 계속하세요</div>
    </div>
  </div>
</div>

<script>
'use strict';

// ══════════════════════════════════════════════════
// CONSTANTS
// ══════════════════════════════════════════════════
const CW = 900, CH = 468;
const FLOOR_Y = 388;
const GRAVITY = 0.58;
const STAGE_W = 5500;
const RARITY = ['일반','고급','희귀','에픽','전설'];
const RARITY_COL = ['#aaaaaa','#44cc44','#4488ff','#cc44ff','#ffaa00'];

// ══════════════════════════════════════════════════
// AUDIO ENGINE (Web Audio API)
// ══════════════════════════════════════════════════
const Audio = (() => {
  let ctx, master, enabled = false;
  try {
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain(); master.gain.value = 0.35;
    master.connect(ctx.destination);
    enabled = true;
  } catch(e) {}

  function resume() { if(ctx && ctx.state === 'suspended') ctx.resume(); }

  function tone(freq, type, dur, vol=0.3, atk=0.005) {
    if(!enabled) return;
    try {
      const o = ctx.createOscillator(), g = ctx.createGain();
      o.connect(g); g.connect(master);
      o.type = type; o.frequency.value = freq;
      const t = ctx.currentTime;
      g.gain.setValueAtTime(0, t);
      g.gain.linearRampToValueAtTime(vol, t+atk);
      g.gain.exponentialRampToValueAtTime(0.001, t+dur);
      o.start(t); o.stop(t+dur+0.05);
    } catch(e) {}
  }

  function noise(dur, vol=0.12, hiFreq=4000) {
    if(!enabled) return;
    try {
      const buf = ctx.createBuffer(1, ctx.sampleRate*dur, ctx.sampleRate);
      const d = buf.getChannelData(0);
      for(let i=0;i<d.length;i++) d[i] = Math.random()*2-1;
      const src = ctx.createBufferSource();
      const filt = ctx.createBiquadFilter();
      filt.type = 'highpass'; filt.frequency.value = hiFreq;
      const g = ctx.createGain();
      src.buffer = buf;
      src.connect(filt); filt.connect(g); g.connect(master);
      g.gain.setValueAtTime(vol, ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime+dur);
      src.start(); src.stop(ctx.currentTime+dur+0.01);
    } catch(e) {}
  }

  const sfx = {
    attack:  ()=>{ tone(180,'sawtooth',.1,.25); noise(.05,.12,3000); },
    hit:     ()=>{ tone(140,'square',.12,.22); noise(.06,.14,2000); },
    crit:    ()=>{ tone(280,'sawtooth',.18,.38); noise(.09,.2,1500); tone(420,'sine',.12,.15); },
    skill:   ()=>{ tone(440,'sine',.25,.3); tone(660,'sine',.18,.18); },
    bigSkill:()=>{ for(let i=0;i<3;i++) setTimeout(()=>tone(220+i*110,'sawtooth',.3,.3),i*80); },
    jump:    ()=>{ tone(340,'sine',.09,.12); },
    land:    ()=>{ tone(80,'square',.06,.1); noise(.04,.08,200); },
    levelUp: ()=>{ [523,659,784,1047].forEach((f,i)=>setTimeout(()=>tone(f,'sine',.3,.4),i*100)); },
    death:   ()=>{ for(let i=0;i<6;i++) setTimeout(()=>tone(200-i*25,'sawtooth',.22,.28),i*80); },
    itemDrop:()=>{ tone(880,'sine',.12,.18); setTimeout(()=>tone(1100,'sine',.1,.15),80); },
    bossIn:  ()=>{ for(let i=0;i<4;i++) setTimeout(()=>tone(70+i*15,'sawtooth',.45,.5),i*220); },
    dodge:   ()=>{ tone(480,'sine',.07,.14); noise(.04,.07,4000); },
    buy:     ()=>{ tone(700,'sine',.18,.25); setTimeout(()=>tone(900,'sine',.14,.2),90); },
    clear:   ()=>{ [523,659,784,523,659,784,1047].forEach((f,i)=>setTimeout(()=>tone(f,'sine',.25,.38),i*110)); },
    burn:    ()=>{ tone(300,'sawtooth',.1,.12); noise(.06,.07,3500); },
    freeze:  ()=>{ tone(800,'sine',.15,.1); tone(600,'sine',.1,.08); },
    poison:  ()=>{ tone(200,'sine',.12,.1); tone(150,'sawtooth',.1,.08); },
    equip:   ()=>{ tone(600,'sine',.12,.2); tone(800,'sine',.1,.18); tone(1000,'sine',.08,.15); },
  };

  return { resume, sfx };
})();

// ══════════════════════════════════════════════════
// PARTICLE SYSTEM
// ══════════════════════════════════════════════════
const PS = {
  p: [],
  spawn(x, y, opts={}) {
    const n = opts.n || 8;
    for(let i=0;i<n;i++) {
      const ang = (opts.dir||0) + (Math.random()-.5)*(opts.spread||Math.PI*2);
      const spd = (opts.sMin||1) + Math.random()*(opts.sMax||5);
      const col = Array.isArray(opts.col) ? opts.col[Math.floor(Math.random()*opts.col.length)] : (opts.col||'#fff');
      this.p.push({
        x, y,
        vx: Math.cos(ang)*spd+(opts.vxB||0),
        vy: Math.sin(ang)*spd+(opts.vyB||0)-(opts.upB||0),
        life:1, decay:(opts.dMin||.02)+Math.random()*(opts.dMax||.03),
        col, sz:(opts.szMin||2)+Math.random()*(opts.szMax||5),
        type:opts.type||'circle', glow:opts.glow||false,
        grav:opts.grav!==undefined?opts.grav:.12,
        spin:(Math.random()-.5)*.25, ang:Math.random()*Math.PI*2,
      });
    }
  },
  update(dt) {
    this.p = this.p.filter(p=>{
      p.x+=p.vx*dt; p.y+=p.vy*dt; p.vy+=p.grav*dt; p.vx*=.97;
      p.life-=p.decay*dt; p.ang+=p.spin*dt;
      return p.life>0;
    });
  },
  draw(ctx, camX) {
    ctx.save();
    for(const p of this.p) {
      const sx = p.x - camX, sy = p.y;
      if(sx<-60||sx>CW+60) continue;
      ctx.globalAlpha = Math.max(0,p.life);
      if(p.glow){ ctx.shadowColor=p.col; ctx.shadowBlur=p.sz*2.5; }
      ctx.fillStyle = p.col; ctx.strokeStyle = p.col;
      ctx.save(); ctx.translate(sx,sy); ctx.rotate(p.ang);
      if(p.type==='sq') ctx.fillRect(-p.sz/2,-p.sz/2,p.sz,p.sz);
      else if(p.type==='star'){ drawStar(ctx,0,0,p.sz,5); }
      else if(p.type==='line'){ ctx.lineWidth=p.sz*.4; ctx.beginPath(); ctx.moveTo(-p.sz,0); ctx.lineTo(p.sz,0); ctx.stroke(); }
      else { ctx.beginPath(); ctx.arc(0,0,p.sz,0,Math.PI*2); ctx.fill(); }
      ctx.restore();
      if(p.glow) ctx.shadowBlur=0;
    }
    ctx.globalAlpha=1; ctx.restore();
  }
};

function drawStar(ctx,x,y,r,pts) {
  const step=Math.PI/pts;
  ctx.beginPath();
  for(let i=0;i<pts*2;i++){
    const rad=i%2===0?r:r*.45;
    const a=i*step-Math.PI/2;
    i===0?ctx.moveTo(x+Math.cos(a)*rad,y+Math.sin(a)*rad):ctx.lineTo(x+Math.cos(a)*rad,y+Math.sin(a)*rad);
  }
  ctx.closePath(); ctx.fill();
}

// ══════════════════════════════════════════════════
// INPUT
// ══════════════════════════════════════════════════
const Input = {
  k:{}, jp:{},
  init() {
    window.addEventListener('keydown', e=>{
      if(!this.k[e.key]){ this.k[e.key]=true; this.jp[e.key]=true; }
      if([' ','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'].includes(e.key)) e.preventDefault();
    });
    window.addEventListener('keyup', e=>{ this.k[e.key]=false; });
  },
  flush(){ this.jp={}; },
};

// ══════════════════════════════════════════════════
// CHARACTER DATA
// ══════════════════════════════════════════════════
const CHARS = [
  {
    id:'fighter', name:'파이터', icon:'🥊', type:'격투 전문가',
    desc:'콤보 연타로 압도하는 근접 전사. 버서커 발동 시 ATK 2.5배.',
    col:'#ff6600', col2:'#ffaa00', bodyCol:'#cc4400',
    hp:340, mp:90, atk:40, def:14, spd:4.8, jmp:13.5,
    stars:{atk:5,def:3,spd:4,range:1,magic:1},
    skills:[
      {id:'s0',name:'라이징 어퍼',icon:'👊',key:'A',mp:12,cd:1.8,desc:'강력한 어퍼컷, 공중 적 추가 타격',col:'#ff6600',
       fn:(p,G)=>{ const d=calcDmg(p,1.8); hitAOE(p,G,p.x+(p.f===1?p.w:-65),p.y-30,70,80,d,d.crit); screenShake(G,4,8); Audio.sfx.hit(); PS.spawn(p.x+(p.f===1?p.w+20:-30)-G.cam,p.y+10,{n:12,col:['#ff6600','#ff9900','#ffcc00'],glow:true,upB:3,sMin:3,sMax:7,spread:.8,dir:p.f===1?0:Math.PI}); }},
      {id:'s1',name:'3단 연타',icon:'💥',key:'S',mp:22,cd:3.5,desc:'초고속 3연속 가격',col:'#ff4400',
       fn:(p,G)=>{ for(let i=0;i<3;i++) setTimeout(()=>{ if(!G||!p.alive) return; const d=calcDmg(p,1.5+i*.3); hitAOE(p,G,p.x+(p.f===1?p.w:-65),p.y,65,55,d,i===2); Audio.sfx.attack(); if(i===2) screenShake(G,3,6); },i*130); }},
      {id:'s2',name:'폭발 킥',icon:'🦵',key:'D',mp:28,cd:5,desc:'전방 돌진 폭발 발차기',col:'#ff8800',
       fn:(p,G)=>{ p.vx=p.f*28; setTimeout(()=>{ if(!G) return; const d=calcDmg(p,2.2); hitAOE(p,G,p.x+(p.f===1?p.w-10:-80),p.y-10,100,70,d,false); spawnExplosion(G,p.x+(p.f===1?p.w+40:-40),p.y+20,p.col); Audio.sfx.bigSkill(); screenShake(G,5,12); },180); }},
      {id:'s3',name:'지진 박치기',icon:'🔥',key:'F',mp:42,cd:8,desc:'지면 충격파, 광역 대미지',col:'#cc2200',
       fn:(p,G)=>{ p.vy=-5; setTimeout(()=>{ if(!G) return; hitAOE(p,G,p.x-80,p.y,220,CH-p.y,calcDmg(p,3),true); spawnExplosion(G,p.x,p.y+p.h,p.col,2.5); screenShake(G,9,20); Audio.sfx.bigSkill(); },250); }},
      {id:'s4',name:'버서커 모드',icon:'😡',key:'G',mp:65,cd:18,desc:'15초간 ATK×2.5, 속도↑↑',col:'#880000',
       fn:(p,G)=>{ p.buffAtk=2.5; p.buffSpd=1.4; p.buffTimer=900; Audio.sfx.bigSkill(); PS.spawn(p.x-G.cam,p.y+p.h/2,{n:30,col:['#ff0000','#ff4400','#ff8800'],glow:true,sMin:3,sMax:9,upB:5}); }},
    ]
  },
  {
    id:'mage', name:'마법사', icon:'🔮', type:'원소 마법사',
    desc:'다양한 원소 마법으로 광역 제압. 타임스탑으로 전장 통제.',
    col:'#4488ff', col2:'#88bbff', bodyCol:'#1133aa',
    hp:210, mp:240, atk:56, def:6, spd:4.1, jmp:12.5,
    stars:{atk:5,def:1,spd:3,range:5,magic:5},
    skills:[
      {id:'s0',name:'파이어볼',icon:'🔥',key:'A',mp:18,cd:1.5,desc:'관통 화염탄 3발 연사',col:'#ff6600',
       fn:(p,G)=>{ for(let i=0;i<3;i++) setTimeout(()=>{ if(!G) return; spawnProj(G,p.x+p.f*50,p.y+22,p.f*15+(Math.random()-.5)*.5,(Math.random()-.5)*.5,calcDmg(p,1.6),'#ff6600','player',{sz:12,emoji:'🔥',life:65,trail:true,trailCol:'#ff4400'}); },i*90); }},
      {id:'s1',name:'아이스 스피어',icon:'❄️',key:'S',mp:28,cd:4.5,desc:'빙결 마법구 - 명중 시 Freeze',col:'#44aaff',
       fn:(p,G)=>{ spawnProj(G,p.x+p.f*55,p.y+20,p.f*13,0,calcDmg(p,2.2),'#44aaff','player',{sz:14,emoji:'❄️',life:75,statusFn:(e)=>{ e.frozen=200; Audio.sfx.freeze(); PS.spawn(e.x+e.w/2,e.y+e.h/2,{n:15,col:['#88ccff','#ffffff','#aaddff'],type:'sq',grav:0,sMin:2,sMax:5}); }}); }},
      {id:'s2',name:'라이트닝',icon:'⚡',key:'D',mp:35,cd:5.5,desc:'낙뢰 연속 타격 (3회)',col:'#ffff00',
       fn:(p,G)=>{ for(let i=0;i<3;i++) setTimeout(()=>{ if(!G) return; const tx=p.x+p.f*(150+i*80); spawnProj(G,tx,-30,0,20,calcDmg(p,2),'#ffff00','player',{sz:18,emoji:'⚡',life:35,gravity:.6}); Audio.sfx.skill(); PS.spawn(tx,80,{n:8,col:['#ffff00','#ffdd44'],glow:true,spread:.3,dir:Math.PI*.5,sMin:4,sMax:10}); },i*180); }},
      {id:'s3',name:'메테오 스톰',icon:'☄️',key:'F',mp:70,cd:12,desc:'5개 운석 낙하 광역기',col:'#ff4400',
       fn:(p,G)=>{ for(let i=0;i<5;i++) setTimeout(()=>{ if(!G) return; const tx=p.x+p.f*120+(Math.random()-.5)*240; spawnProj(G,tx,-50,(Math.random()-.5)*2,17,calcDmg(p,3.5),'#ff4400','player',{sz:22,emoji:'☄️',life:70,gravity:.35}); screenShake(G,5,10); PS.spawn(tx,0,{n:6,col:['#ff6600','#ff4400'],glow:true,spread:.4,dir:Math.PI*.5,sMin:3,sMax:7}); },i*170); }},
      {id:'s4',name:'타임 스탑',icon:'⏰',key:'G',mp:90,cd:22,desc:'4초간 모든 적 완전 정지',col:'#aa44ff',
       fn:(p,G)=>{ freezeAllEnemies(G,240); Audio.sfx.bigSkill(); PS.spawn(CW/2,CH/2,{n:50,col:['#aa44ff','#cc88ff','#ffffff'],glow:true,sMin:2,sMax:8,type:'star',grav:0,sMin:3,sMax:8}); }},
    ]
  },
  {
    id:'knight', name:'나이트', icon:'⚔️', type:'철갑 검사',
    desc:'높은 방어력과 방패 스킬로 생존. 성검으로 광역 성속성 대미지.',
    col:'#bbccdd', col2:'#ddeeff', bodyCol:'#778899',
    hp:500, mp:110, atk:34, def:26, spd:3.8, jmp:11.5,
    stars:{atk:3,def:5,spd:2,range:2,magic:2},
    skills:[
      {id:'s0',name:'소드 슬래시',icon:'⚔️',key:'A',mp:14,cd:2,desc:'전방 넓은 범위 검격',col:'#aabbcc',
       fn:(p,G)=>{ hitAOE(p,G,p.x+(p.f===1?p.w-20:-100),p.y-15,120,80,calcDmg(p,1.7),false); PS.spawn(p.x+(p.f===1?p.w+30:-30)-G.cam,p.y+20,{n:10,col:['#bbccdd','#ddeeff'],type:'line',spread:.5,dir:p.f===1?0:Math.PI,sMin:4,sMax:10}); }},
      {id:'s1',name:'방패 강타',icon:'🛡️',key:'S',mp:20,cd:4,desc:'방패로 돌진 - 적 스턴 2초',col:'#8899aa',
       fn:(p,G)=>{ p.vx=p.f*18; setTimeout(()=>{ if(!G) return; hitAOE(p,G,p.x+(p.f===1?p.w:-80),p.y,80,60,calcDmg(p,1.3),true,{stun:120}); },160); }},
      {id:'s2',name:'차지 돌격',icon:'💨',key:'D',mp:26,cd:5.5,desc:'고속 돌진 - 통과 후 폭발',col:'#ccddee',
       fn:(p,G)=>{ p.vx=p.f*38; p.invincible=40; setTimeout(()=>{ if(!G) return; hitAOE(p,G,p.x-60,p.y-20,160,90,calcDmg(p,2.3),true); spawnExplosion(G,p.x+p.f*60,p.y+20,'#ccddee'); screenShake(G,6,12); },200); }},
      {id:'s3',name:'회오리 베기',icon:'🌀',key:'F',mp:40,cd:8,desc:'360도 전방위 검격',col:'#99aabb',
       fn:(p,G)=>{ hitAOE(p,G,p.x-70,p.y-40,p.w+140,p.h+80,calcDmg(p,2),false); PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:20,col:['#ccddee','#ffffff'],type:'line',grav:0,sMin:5,sMax:15,spread:Math.PI*2,glow:true}); screenShake(G,5,10); }},
      {id:'s4',name:'성스러운 검',icon:'✨',key:'G',mp:75,cd:16,desc:'성속성 광역 폭발 + 자가 회복',col:'#ffffaa',
       fn:(p,G)=>{ hitAOE(p,G,p.x+(p.f===1?-20:-160),p.y-50,200,130,calcDmg(p,4.5),true); p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.15)); screenShake(G,10,25); PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:40,col:['#ffffaa','#ffffff','#ffdd88'],glow:true,sMin:3,sMax:9,type:'star'}); Audio.sfx.bigSkill(); }},
    ]
  },
  {
    id:'gunner', name:'건너', icon:'🔫', type:'전술 사수',
    desc:'빠른 연사와 다양한 탄종으로 중거리 제압. 인피니티로 전장 제패.',
    col:'#44cc88', col2:'#88ffaa', bodyCol:'#226644',
    hp:260, mp:160, atk:46, def:9, spd:5.2, jmp:14.5,
    stars:{atk:4,def:2,spd:5,range:5,magic:2},
    skills:[
      {id:'s0',name:'버스트 파이어',icon:'🔫',key:'A',mp:14,cd:1.2,desc:'5연발 고속 총격',col:'#44cc88',
       fn:(p,G)=>{ for(let i=0;i<5;i++) setTimeout(()=>{ if(!G) return; spawnProj(G,p.x+p.f*52,p.y+25,p.f*20+(Math.random()-.5)*1.5,(Math.random()-.5)*1.5,calcDmg(p,1.0),'#44cc88','player',{sz:6,life:70}); Audio.sfx.attack(); },i*55); }},
      {id:'s1',name:'유탄 투척',icon:'💣',key:'S',mp:24,cd:4,desc:'폭발 유탄 - 범위 대미지',col:'#ffcc00',
       fn:(p,G)=>{ spawnProj(G,p.x+p.f*45,p.y+22,p.f*11,-8,calcDmg(p,2.8),'#ffcc00','player',{sz:16,emoji:'💣',life:85,grav:.42,explodeOnLand:true}); }},
      {id:'s2',name:'스나이핑',icon:'🎯',key:'D',mp:32,cd:5.5,desc:'초관통 저격 - 무한 관통',col:'#88ff44',
       fn:(p,G)=>{ spawnProj(G,p.x+p.f*52,p.y+25,p.f*35,0,calcDmg(p,4.5),'#88ff44','player',{sz:10,life:110,pierce:true}); screenShake(G,3,6); PS.spawn(p.x+p.f*60-G.cam,p.y+25,{n:8,col:['#88ff44','#ffffff'],type:'line',spread:.2,dir:p.f===1?0:Math.PI,sMin:5,sMax:12}); }},
      {id:'s3',name:'클러스터 미사일',icon:'🚀',key:'F',mp:45,cd:9,desc:'5개 추적 미사일 동시 발사',col:'#ff8800',
       fn:(p,G)=>{ for(let i=0;i<5;i++) setTimeout(()=>{ if(!G) return; spawnProj(G,p.x+p.f*42,p.y+15+i*6,p.f*9+(Math.random()-.5)*3,-8+(Math.random()-.5)*3,calcDmg(p,2),'#ff8800','player',{sz:14,emoji:'🚀',life:100,grav:.06,homing:true}); },i*90); }},
      {id:'s4',name:'인피니티 블릿',icon:'🌟',key:'G',mp:85,cd:20,desc:'전방향 72발 탄막 발사',col:'#44ffaa',
       fn:(p,G)=>{ for(let i=0;i<18;i++) setTimeout(()=>{ if(!G) return; const a=(i/18)*Math.PI*2; spawnProj(G,p.x+p.w/2,p.y+p.h/2,Math.cos(a)*17,Math.sin(a)*14,calcDmg(p,1.3),'#44ffaa','player',{sz:8,life:65,pierce:true}); },i*55); screenShake(G,6,18); Audio.sfx.bigSkill(); }},
    ]
  },
  {
    id:'ninja', name:'닌자', icon:'🥷', type:'암살 닌자',
    desc:'극한의 기동력과 극대화 확률로 초고 순간 대미지. 잔상 회피로 무적.',
    col:'#cc44ff', col2:'#ee88ff', bodyCol:'#661188',
    hp:230, mp:180, atk:52, def:7, spd:5.8, jmp:15.5,
    stars:{atk:5,def:1,spd:5,range:3,magic:3},
    skills:[
      {id:'s0',name:'인법: 베기',icon:'🗡️',key:'A',mp:14,cd:1.4,desc:'초고속 3연참, 각 타 30% 극대',col:'#cc44ff',
       fn:(p,G)=>{ for(let i=0;i<3;i++) setTimeout(()=>{ if(!G||!p.alive) return; const isCrit=Math.random()<.3; hitAOE(p,G,p.x+(p.f===1?p.w:-70),p.y-10,75,60,calcDmg(p,1.4*(isCrit?2.5:1)),isCrit); PS.spawn(p.x+(p.f===1?p.w+20:-20)-G.cam,p.y+20,{n:6,col:['#cc44ff','#ffffff'],type:'line',spread:.6,dir:p.f===1?0:Math.PI,sMin:3,sMax:8,glow:true}); },i*110); }},
      {id:'s1',name:'수리검 연타',icon:'🌸',key:'S',mp:22,cd:3,desc:'수리검 4발 동시 투척',col:'#ff88ff',
       fn:(p,G)=>{ const spread=[-6,-2,2,6]; spread.forEach(vy=>{ spawnProj(G,p.x+p.f*52,p.y+28,p.f*18,vy,calcDmg(p,1.5),'#cc44ff','player',{sz:9,emoji:'✴️',life:70}); }); }},
      {id:'s2',name:'순간이동',icon:'💨',key:'D',mp:20,cd:3.5,desc:'전방 순간이동 + 폭풍 베기',col:'#aa22ee',
       fn:(p,G)=>{ PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:15,col:['#cc44ff','#aa22ee'],grav:0,sMin:2,sMax:6}); p.x+=p.f*180; setTimeout(()=>{ if(!G) return; hitAOE(p,G,p.x+(p.f===1?p.w:-80),p.y-20,90,80,calcDmg(p,2.5),true); PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:20,col:['#cc44ff','#ffffff'],glow:true,sMin:3,sMax:7,upB:2}); },80); }},
      {id:'s3',name:'극독',icon:'☠️',key:'F',mp:38,cd:7,desc:'맹독 단검 - 지속 독 대미지',col:'#44cc44',
       fn:(p,G)=>{ spawnProj(G,p.x+p.f*52,p.y+24,p.f*17,-2,calcDmg(p,1.8),'#44cc44','player',{sz:11,emoji:'🗡️',life:80,statusFn:(e)=>{ e.poison=360; e.poisonDmg=Math.round(p.atk*.4); Audio.sfx.poison(); }}); }},
      {id:'s4',name:'죽음의 무도',icon:'💀',key:'G',mp:80,cd:18,desc:'6방향 충격파 + 5초 무적',col:'#220033',
       fn:(p,G)=>{ p.invincible=300; for(let i=0;i<6;i++){ const a=i/6*Math.PI*2; hitAOE(p,G,p.x+Math.cos(a)*80-50,p.y+Math.sin(a)*60-30,100,80,calcDmg(p,3.5),true); } screenShake(G,12,30); PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:50,col:['#cc44ff','#440088','#ffffff'],glow:true,sMin:3,sMax:10,type:'star'}); Audio.sfx.bigSkill(); }},
    ]
  },
];

// ══════════════════════════════════════════════════
// ENEMY DATA
// ══════════════════════════════════════════════════
const ENEMY_TYPES = [
  {id:'goblin',   name:'고블린',  icon:'👺',hp:90, atk:13,spd:2.8,xp:15,g:8,  col:'#33aa33',sz:28,ai:'charge'},
  {id:'orc',      name:'오크',    icon:'👹',hp:160,atk:20,spd:2.0,xp:28,g:16, col:'#887733',sz:38,ai:'brute'},
  {id:'skel',     name:'스켈레톤',icon:'💀',hp:110,atk:16,spd:3.2,xp:22,g:13, col:'#ccccaa',sz:30,ai:'normal'},
  {id:'zombie',   name:'좀비',    icon:'🧟',hp:130,atk:14,spd:1.6,xp:24,g:14, col:'#557744',sz:32,ai:'slow'},
  {id:'mage_e',   name:'마법사',  icon:'🧙',hp:100,atk:25,spd:2.6,xp:32,g:22, col:'#5533aa',sz:28,ai:'ranged',ranged:true},
  {id:'archer_e', name:'궁수',    icon:'🏹',hp:85, atk:22,spd:3,  xp:28,g:18, col:'#886622',sz:26,ai:'ranged',ranged:true},
  {id:'dragon_e', name:'드래고니언',icon:'🐊',hp:220,atk:28,spd:2.2,xp:50,g:35, col:'#336633',sz:42,ai:'brute'},
  {id:'demon',    name:'데몬',    icon:'😈',hp:180,atk:24,spd:2.8,xp:45,g:30, col:'#883333',sz:36,ai:'charge'},
  {id:'lich',     name:'리치',    icon:'👻',hp:140,atk:30,spd:2.4,xp:40,g:28, col:'#334488',sz:32,ai:'ranged',ranged:true},
  {id:'golem',    name:'골렘',    icon:'🗿',hp:320,atk:32,spd:1.4,xp:65,g:45, col:'#885544',sz:46,ai:'tank'},
];

// ══════════════════════════════════════════════════
// STAGE DATA
// ══════════════════════════════════════════════════
const STAGES = [
  {name:'어둠의 동굴',   bg:'#06040e',fl:'#100820',wall:'#0d0618',
   enemies:6,  enemySet:[0,1,2],  boss:{name:'슬라임 대왕',icon:'🟢',hp:700, atk:28,spd:2.5,col:'#22aa22'},
   ambientCol:'rgba(50,0,100,.15)', torchCol:'#ff6600'},
  {name:'용암 던전',     bg:'#120400',fl:'#220900',wall:'#1a0500',
   enemies:8,  enemySet:[0,1,3,6],boss:{name:'불꽃 골렘',  icon:'🔥',hp:1100,atk:36,spd:2.2,col:'#ff4400'},
   ambientCol:'rgba(200,50,0,.08)', torchCol:'#ff4400'},
  {name:'얼음 궁전',     bg:'#040820',fl:'#081430',wall:'#060e22',
   enemies:10, enemySet:[1,2,4,7],boss:{name:'빙결 드래곤',icon:'🐉',hp:1600,atk:45,spd:2.8,col:'#44aaff'},
   ambientCol:'rgba(0,100,200,.1)', torchCol:'#44aaff'},
  {name:'독 늪지',       bg:'#040e04',fl:'#081208',wall:'#060e06',
   enemies:12, enemySet:[3,5,8,6],boss:{name:'늪 히드라',  icon:'🐍',hp:2200,atk:52,spd:3,  col:'#44cc22'},
   ambientCol:'rgba(0,150,0,.08)', torchCol:'#44cc00'},
  {name:'마왕의 성',     bg:'#080010',fl:'#120018',wall:'#0e0014',
   enemies:15, enemySet:[4,7,8,9],boss:{name:'마왕 DARKOS',icon:'💀',hp:3000,atk:65,spd:3.2,col:'#cc00ff'},
   ambientCol:'rgba(150,0,200,.12)', torchCol:'#aa00ff', final:true},
];

// ══════════════════════════════════════════════════
// ITEM DATA
// ══════════════════════════════════════════════════
const ITEM_POOL = [
  {id:'hp_s',name:'소 HP 포션',icon:'🧪',type:'consume',fn:(p)=>{ const h=Math.round(p.maxHp*.2); p.hp=Math.min(p.maxHp,p.hp+h); return `HP +${h}`; },price:60,chance:.25,col:'#ff4444'},
  {id:'hp_l',name:'대 HP 포션',icon:'⚗️',type:'consume',fn:(p)=>{ const h=Math.round(p.maxHp*.5); p.hp=Math.min(p.maxHp,p.hp+h); return `HP +${h}`; },price:140,chance:.1,col:'#ff6666'},
  {id:'mp_s',name:'마나 포션',icon:'💙',type:'consume',fn:(p)=>{ const m=Math.round(p.maxMp*.4); p.mp=Math.min(p.maxMp,p.mp+m); return `MP +${m}`; },price:70,chance:.2,col:'#4488ff'},
  {id:'wpn1',name:'강화 검',icon:'🗡️',type:'weapon',slot:'wpn',fn:(p)=>{ p.atkBonus=(p.atkBonus||0)+15; return 'ATK +15'; },price:200,chance:.08,col:'#ffdd44',rarity:1},
  {id:'wpn2',name:'불꽃 검',icon:'🔥',type:'weapon',slot:'wpn',fn:(p)=>{ p.atkBonus=(p.atkBonus||0)+30; return 'ATK +30'; },price:350,chance:.04,col:'#ff6600',rarity:2},
  {id:'arm1',name:'강화 갑옷',icon:'🛡️',type:'armor',slot:'arm',fn:(p)=>{ p.defBonus=(p.defBonus||0)+12; p.maxHp+=40; p.hp=Math.min(p.maxHp,p.hp+40); return 'DEF +12, HP +40'; },price:220,chance:.07,col:'#88aadd',rarity:1},
  {id:'arm2',name:'마법 갑옷',icon:'💎',type:'armor',slot:'arm',fn:(p)=>{ p.defBonus=(p.defBonus||0)+22; p.maxHp+=80; p.hp=Math.min(p.maxHp,p.hp+80); return 'DEF +22, HP +80'; },price:380,chance:.035,col:'#aaddff',rarity:2},
  {id:'acc1',name:'스피드 링',icon:'💍',type:'acc',slot:'acc',fn:(p)=>{ p.spdBonus=(p.spdBonus||0)+.8; return 'SPD +0.8'; },price:180,chance:.08,col:'#ffaadd',rarity:1},
  {id:'acc2',name:'크리티컬 반지',icon:'🔮',type:'acc',slot:'acc',fn:(p)=>{ p.critBonus=(p.critBonus||0)+.15; return 'CRIT +15%'; },price:300,chance:.04,col:'#cc88ff',rarity:2},
  {id:'acc3',name:'전설의 반지',icon:'⭐',type:'acc',slot:'acc',fn:(p)=>{ p.critBonus=(p.critBonus||0)+.25; p.atkBonus=(p.atkBonus||0)+20; return 'CRIT +25%, ATK +20'; },price:600,chance:.01,col:'#ffcc00',rarity:4},
];

// ══════════════════════════════════════════════════
// ACHIEVEMENTS
// ══════════════════════════════════════════════════
const ACHIEVS = [
  {id:'first_kill',name:'첫 번째 사냥',desc:'적 1마리 처치',check:(G)=>G.player.kills>=1},
  {id:'kill10',name:'학살자',desc:'적 10마리 처치',check:(G)=>G.player.kills>=10},
  {id:'kill30',name:'전장의 악마',desc:'적 30마리 처치',check:(G)=>G.player.kills>=30},
  {id:'combo10',name:'콤보의 달인',desc:'10콤보 달성',check:(G)=>G.maxCombo>=10},
  {id:'combo25',name:'콤보 마스터',desc:'25콤보 달성',check:(G)=>G.maxCombo>=25},
  {id:'lv5',name:'성장하는 전사',desc:'레벨 5 달성',check:(G)=>G.player.level>=5},
  {id:'lv10',name:'전설의 전사',desc:'레벨 10 달성',check:(G)=>G.player.level>=10},
  {id:'boss1',name:'보스 킬러',desc:'첫 보스 처치',check:(G)=>G.bossKills>=1},
  {id:'nodamage',name:'무결점 전사',desc:'피해 없이 스테이지 클리어',check:(G)=>G.stageDmgTaken===0&&G.phase==='clear'},
  {id:'gold500',name:'부자 모험가',desc:'골드 500 획득',check:(G)=>G.player.gold>=500},
];

let unlockedAchievs = new Set(JSON.parse(localStorage.getItem('dc_achiev')||'[]'));
let highScore = parseInt(localStorage.getItem('dc_hi')||'0');

// ══════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════
let G = null;

function createPlayer(charData) {
  return {
    ...charData,
    x:150, y:FLOOR_Y-70,
    vx:0, vy:0, f:1,
    onGround:false, jumpCount:0,
    hp:charData.hp, maxHp:charData.hp,
    mp:charData.mp, maxMp:charData.mp,
    alive:true,
    invincible:0,
    skillCds: charData.skills.map(()=>0),
    buffAtk:1, buffSpd:1, buffTimer:0,
    kills:0, score:0, gold:0, level:1,
    xp:0, xpNext:100,
    comboCount:0, comboTimer:0,
    attackCd:0, attackAnim:0, hitAnim:0,
    dodgeCd:0, dodgeAnim:0,
    w:44, h:60,
    atkBonus:0, defBonus:0, spdBonus:0, critBonus:0,
    equip:{wpn:null,arm:null,acc:null},
    inventory:[],
    statusEffects:{burn:0,freeze:0,poison:0,stun:0,slow:0},
    poisonDmg:0,
    hitStopTimer:0,
  };
}

function initGame(charId, stageIdx) {
  const charData = CHARS.find(c=>c.id===charId);
  const stage = STAGES[stageIdx];
  const p = createPlayer(charData);

  G = {
    charId, stageIdx, stage,
    player:p,
    enemies:[],
    boss:null,
    bossSpawned:false,
    bossKills:0,
    projectiles:[],
    items:[],
    cam:0,
    phase:'play',
    timer:0,
    startTime:Date.now(),
    platforms:genPlatforms(stage),
    shakeAmt:0, shakeTimer:0,
    hitStopTimer:0,
    stageDmgTaken:0,
    maxCombo:0,
    droppedItems:[],
    paused:false,
    bgScroll:0,
  };

  spawnEnemies();
  PS.p=[];

  updateEquipUI();
}

function genPlatforms(stage) {
  const plats=[];
  for(let i=0;i<14;i++){
    const x=250+i*310+(Math.random()-.5)*80;
    const y=FLOOR_Y-90-Math.random()*130;
    const w=70+Math.random()*70;
    plats.push({x,y,w,h:12,col:stage.wall});
  }
  return plats;
}

function spawnEnemies() {
  const st=G.stage;
  const set=st.enemySet;
  const cnt=st.enemies;
  for(let i=0;i<cnt;i++){
    const tid=set[Math.floor(Math.random()*set.length)];
    const et={...ENEMY_TYPES[tid]};
    const sc=1+G.stageIdx*.28;
    const ex=700+i*340+Math.random()*120;
    G.enemies.push({
      ...et,
      uid:'e'+i+Date.now(),
      x:ex, y:FLOOR_Y-et.sz,
      hp:Math.round(et.hp*sc), maxHp:Math.round(et.hp*sc),
      atk:Math.round(et.atk*sc),
      vy:0, f:-1, aggro:false,
      alive:true, dying:false, deathTimer:0,
      attackTimer:60+Math.random()*80,
      stun:0, freeze:0, poison:0, poisonDmg:0, poisonTimer:0,
      slow:0, burn:0, burnTimer:0,
      w:et.sz, h:et.sz,
      hitFlash:0,
    });
  }
}

function spawnBoss() {
  const bd=G.stage.boss;
  const sc=1+G.stageIdx*.35;
  G.boss={
    name:bd.name, icon:bd.icon,
    x:STAGE_W-500, y:FLOOR_Y-90,
    hp:Math.round(bd.hp*sc), maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc), spd:bd.spd+G.stageIdx*.15,
    col:bd.col,
    f:-1, vy:0,
    alive:true,
    stun:0, freeze:0,
    attackTimer:80, projTimer:120,
    phase:1, phase2:false, phase3:false,
    w:72, h:84,
    hitFlash:0,
    enrageTimer:0,
  };
  document.getElementById('bossHpWrap').classList.add('show');
  document.getElementById('bossNameLbl').textContent='⚠ '+bd.name;
  const bw=document.getElementById('bossWarn');
  bw.style.display='block';
  setTimeout(()=>bw.style.display='none',2200);
  screenShake(G,10,35);
  Audio.sfx.bossIn();
}

// ══════════════════════════════════════════════════
// COMBAT HELPERS
// ══════════════════════════════════════════════════
function calcDmg(p, mult) {
  const base=(p.atk+(p.atkBonus||0))*p.buffAtk;
  const crit=Math.random()<(.12+(p.critBonus||0));
  const dmg=Math.round((base*mult+Math.random()*8-4)*(crit?2.0:1));
  return {dmg, crit};
}

function hitAOE(p, G, ax, ay, aw, ah, dmgRes, isCrit, opts={}) {
  const targets=[...G.enemies];
  if(G.boss&&G.boss.alive) targets.push(G.boss);
  let hitCount=0;
  for(const e of targets){
    if(!e.alive) continue;
    if(ax<e.x+e.w&&ax+aw>e.x&&ay<e.y+e.h&&ay+ah>e.y){
      const d=typeof dmgRes==='object'?dmgRes.dmg:dmgRes;
      const c=(typeof dmgRes==='object'?dmgRes.crit:false)||isCrit;
      dealDamage(G,e,d,c,opts);
      hitCount++;
    }
  }
  return hitCount>0;
}

function dealDamage(G, target, dmg, crit, opts={}) {
  if(!target.alive) return;
  const p=G.player;
  target.hp-=dmg;
  target.hitFlash=8;
  if(opts.stun) target.stun=Math.max(target.stun,opts.stun);
  if(opts.statusFn) opts.statusFn(target);

  const sx=target.x-G.cam+target.w/2;
  showDmgNum(sx,target.y-8,dmg,crit,p.col);

  G.hitStopTimer=crit?5:2;

  if(crit) Audio.sfx.crit(); else Audio.sfx.hit();

  if(target.hp<=0) killTarget(G,target);
}

function killTarget(G, target) {
  target.alive=false; target.dying=true; target.deathTimer=30;
  const p=G.player;

  if(target===G.boss){
    p.xp+=600; p.gold+=350; p.score+=6000;
    G.bossKills++;
    PS.spawn(target.x+target.w/2,target.y+target.h/2,{n:60,col:['#ffcc00','#ff6600','#ffffff'],glow:true,sMin:3,sMax:12,type:'star'});
    screenShake(G,14,50);
    Audio.sfx.stageClear||Audio.sfx.bigSkill();
    document.getElementById('bossHpWrap').classList.remove('show');
    checkAchievs(G);
    setTimeout(()=>stageClear(G),1200);
  } else {
    p.kills++; p.xp+=target.xp; p.gold+=target.g; p.score+=target.xp*2;
    PS.spawn(target.x+target.w/2,target.y+target.h/2,{n:16,col:[target.col,'#ffcc00'],sMin:2,sMax:7});
    Audio.sfx.death();
    checkLevelUp(p,G);
    tryDropItem(G,target);
    checkAchievs(G);
  }
}

function tryDropItem(G, target) {
  if(Math.random()>.35) return;
  const r=Math.random();
  let pool=ITEM_POOL.filter(it=>it.type==='consume');
  if(r<.25) pool=ITEM_POOL.filter(it=>it.type!=='consume');
  const item=pool[Math.floor(Math.random()*pool.length)];
  G.items.push({
    ...item, uid:'i'+Date.now()+Math.random(),
    x:target.x+target.w/2-14,
    y:target.y, vy:-6, alive:true,
  });
}

function checkLevelUp(p, G) {
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext; p.level++;
    p.xpNext=Math.round(p.xpNext*1.55);
    p.atk+=5; p.def+=2; p.maxHp+=35; p.hp=Math.min(p.maxHp,p.hp+50);
    p.maxMp+=12; p.mp=Math.min(p.maxMp,p.mp+25);
    PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:30,col:['#ffff00','#ffcc00','#ffffff'],glow:true,sMin:3,sMax:9,type:'star',upB:4});
    Audio.sfx.levelUp();
    showAchiev('🆙','레벨 업!',`Lv.${p.level} 달성!`);
    checkAchievs(G);
  }
}

function spawnExplosion(G, wx, wy, col, scale=1.5) {
  PS.spawn(wx,wy,{n:Math.round(25*scale),col:[col,'#ffffff','#ffcc00'],glow:true,sMin:3*scale,sMax:8*scale,upB:2});
  PS.spawn(wx,wy,{n:Math.round(15*scale),col:[col,'#ff4400'],type:'sq',sMin:2*scale,sMax:6*scale});
}

function freezeAllEnemies(G, dur) {
  for(const e of G.enemies) if(e.alive) e.freeze=Math.max(e.freeze,dur);
  if(G.boss&&G.boss.alive) G.boss.freeze=Math.max(G.boss.freeze,dur);
}

// ══════════════════════════════════════════════════
// PROJECTILE SYSTEM
// ══════════════════════════════════════════════════
function spawnProj(G, x, y, vx, vy, dmgRes, col, owner, opts={}) {
  G.projectiles.push({
    x,y,vx,vy,
    dmg: typeof dmgRes==='object'?dmgRes.dmg:dmgRes,
    crit: typeof dmgRes==='object'?dmgRes.crit:false,
    col, owner, uid:'p'+Date.now()+Math.random(),
    life:opts.life||80, sz:opts.sz||8,
    pierce:opts.pierce||false,
    grav:opts.grav!==undefined?opts.grav:0,
    emoji:opts.emoji||null,
    trail:opts.trail||false, trailCol:opts.trailCol||col,
    homing:opts.homing||false,
    statusFn:opts.statusFn||null,
    explodeOnLand:opts.explodeOnLand||false,
    alive:true,
  });
}

function updateProjectiles(G, dt) {
  const p=G.player;
  G.projectiles=G.projectiles.filter(proj=>{
    if(!proj.alive) return false;
    proj.x+=proj.vx*dt; proj.y+=proj.vy*dt;
    proj.vy+=proj.grav*dt; proj.life-=dt;
    if(proj.life<=0) return false;

    // Homing
    if(proj.homing&&proj.owner==='player'){
      const targets=[...G.enemies];
      if(G.boss&&G.boss.alive) targets.push(G.boss);
      let nearest=null, nearDist=999;
      for(const e of targets){
        if(!e.alive) continue;
        const d=Math.abs(e.x-proj.x)+Math.abs(e.y-proj.y);
        if(d<nearDist){nearDist=d;nearest=e;}
      }
      if(nearest&&nearDist<400){
        const dx=nearest.x+nearest.w/2-proj.x, dy=nearest.y+nearest.h/2-proj.y;
        const len=Math.sqrt(dx*dx+dy*dy)||1;
        proj.vx+=(dx/len*3-proj.vx)*.12;
        proj.vy+=(dy/len*3-proj.vy)*.12;
      }
    }

    if(proj.trail){
      PS.spawn(proj.x,proj.y,{n:2,col:[proj.trailCol],sMin:1,sMax:3,grav:0,decay:.1,spread:Math.PI*.3,sMax:3});
    }

    // Explode on land
    if(proj.explodeOnLand&&proj.y>=FLOOR_Y){
      spawnExplosion(G,proj.x,FLOOR_Y,proj.col);
      hitAOE(p,G,proj.x-60,FLOOR_Y-60,120,80,{dmg:proj.dmg,crit:proj.crit},false);
      screenShake(G,4,8);
      return false;
    }

    // Off screen
    if(proj.y>CH+80||proj.x<G.cam-100||proj.x>G.cam+CW+100) return false;

    // Hit detection
    if(proj.owner==='player'){
      const targets=[...G.enemies];
      if(G.boss&&G.boss.alive) targets.push(G.boss);
      for(const e of targets){
        if(!e.alive) continue;
        if(proj.x>e.x&&proj.x<e.x+e.w&&proj.y>e.y&&proj.y<e.y+e.h){
          dealDamage(G,e,proj.dmg,proj.crit,{statusFn:proj.statusFn});
          PS.spawn(proj.x-G.cam,proj.y,{n:8,col:[proj.col,'#ffffff'],sMin:2,sMax:5,glow:!!proj.emoji});
          if(!proj.pierce){ proj.alive=false; return false; }
        }
      }
    } else {
      // Enemy proj hits player
      if(p.invincible<=0&&p.dodgeAnim<=0){
        const sx=proj.x-G.cam;
        if(sx>p.x-G.cam&&sx<p.x-G.cam+p.w&&proj.y>p.y&&proj.y<p.y+p.h){
          takeDmg(G,Math.max(1,proj.dmg-Math.round((p.def+(p.defBonus||0))*.4)));
          proj.alive=false; return false;
        }
      }
    }
    return true;
  });
}

function takeDmg(G, dmg) {
  const p=G.player;
  if(p.invincible>0) return;
  p.hp-=dmg; p.hitAnim=12; p.invincible=35;
  G.stageDmgTaken+=dmg;
  showDmgNum(p.x-G.cam+p.w/2,p.y-5,dmg,false,'#ff4444');
  screenShake(G,4,10);
  Audio.sfx.hit();
  if(p.hp<=0) gameOver(G);
}

// ══════════════════════════════════════════════════
// UPDATE
// ══════════════════════════════════════════════════
function gameUpdate(dt) {
  if(!G||G.phase!=='play'||G.paused) return;
  G.timer++;
  G.bgScroll=(G.bgScroll+.3*dt)%500;

  const p=G.player;
  if(!p.alive) return;

  // Hit stop
  if(G.hitStopTimer>0){ G.hitStopTimer-=dt; return; }

  handleInput(p,G,dt);
  updatePlayer(p,G,dt);
  updateEnemies(G,dt);
  if(G.boss&&G.boss.alive) updateBoss(G,dt);
  updateProjectiles(G,dt);
  updateItems(G,dt);
  PS.update(dt);

  if(G.shakeTimer>0) G.shakeTimer-=dt;

  // Boss spawn check
  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){
    G.bossSpawned=true;
    spawnBoss();
  }

  // Win check
  if(G.bossSpawned&&G.boss&&!G.boss.alive&&!G.boss.dying) {
    // handled in killTarget
  }

  // Status effects on player
  const se=p.statusEffects||{};
  if(se.burn>0){ se.burn-=dt; if(G.timer%30===0){ takeDmg(G,Math.round(p.maxHp*.012)); PS.spawn(p.x-G.cam+p.w/2,p.y,{n:4,col:['#ff4400','#ff8800'],sMin:2,sMax:4,upB:2}); } }
  if(se.poison>0){ se.poison-=dt; if(G.timer%20===0){ takeDmg(G,Math.round(p.maxHp*.008)); PS.spawn(p.x-G.cam+p.w/2,p.y,{n:3,col:['#44cc44','#88ff44'],sMin:1,sMax:3,upB:1}); } }

  // MP regen
  if(G.timer%75===0) p.mp=Math.min(p.maxMp,p.mp+4);

  checkAchievs(G);
}

function updatePlayer(p, G, dt) {
  p.vy+=GRAVITY*dt;
  p.x+=p.vx*dt; p.y+=p.vy*dt;
  p.vx*=.82;

  // Floor
  if(p.y+p.h>=FLOOR_Y){ p.y=FLOOR_Y-p.h; p.vy=0; p.onGround=true; p.jumpCount=0; }
  else p.onGround=false;

  // Platforms
  for(const pl of G.platforms){
    if(p.vy>=0&&p.x+p.w>pl.x&&p.x<pl.x+pl.w&&p.y+p.h>pl.y&&p.y+p.h<pl.y+pl.h+16){
      p.y=pl.y-p.h; p.vy=0; p.onGround=true; p.jumpCount=0;
    }
  }

  p.x=Math.max(5,Math.min(STAGE_W-p.w-5,p.x));
  if(p.y>CH+200){ p.y=FLOOR_Y-p.h; p.vy=0; }

  // Camera
  const tc=p.x-CW*.33;
  G.cam+=(tc-G.cam)*.09*dt;
  G.cam=Math.max(0,Math.min(STAGE_W-CW,G.cam));

  // Timers
  if(p.invincible>0) p.invincible-=dt;
  if(p.attackCd>0) p.attackCd-=dt;
  if(p.attackAnim>0) p.attackAnim-=dt;
  if(p.hitAnim>0) p.hitAnim-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeAnim>0) p.dodgeAnim-=dt;
  if(p.comboTimer>0){ p.comboTimer-=dt; if(p.comboTimer<=0){ p.comboCount=0; document.getElementById('combo').style.opacity='0'; } }
  if(p.buffTimer>0){ p.buffTimer-=dt; if(p.buffTimer<=0){ p.buffAtk=1; p.buffSpd=1; } }
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;

  // Status effects on player
  const se=p.statusEffects||{};
  if(se.freeze>0) se.freeze-=dt;
  if(se.stun>0) se.stun-=dt;
  if(se.slow>0) se.slow-=dt;
}

function handleInput(p, G, dt) {
  const se=p.statusEffects||{};
  if(se.freeze>0||se.stun>0) return;

  const slowFactor=se.slow>0?.5:1;
  const baseSpd=(p.spd+(p.spdBonus||0))*p.buffSpd*slowFactor;

  if(Input.k['ArrowLeft']){ p.vx=-baseSpd*6*dt; p.f=-1; }
  if(Input.k['ArrowRight']){ p.vx=baseSpd*6*dt; p.f=1; }

  // Jump
  if(Input.jp['z']||Input.jp['Z']){
    if(p.jumpCount<2){
      p.vy=-p.jmp; p.jumpCount++;
      PS.spawn(p.x-G.cam+p.w/2,p.y+p.h,{n:8,col:['#ffffff','#cccccc'],upB:3,sMin:2,sMax:4,spread:.8});
      Audio.sfx.jump();
    }
  }

  // Attack
  if((Input.jp['x']||Input.jp['X'])&&p.attackCd<=0) doNormalAttack(p,G);

  // Dodge
  if(Input.jp[' ']&&p.dodgeCd<=0){
    p.vx=p.f*22; p.vy=-3;
    p.invincible=40; p.dodgeCd=50; p.dodgeAnim=20;
    PS.spawn(p.x-G.cam+p.w/2,p.y+p.h/2,{n:15,col:[p.col,'rgba(255,255,255,.6)'],spread:Math.PI*.5,dir:Math.PI+Math.PI/2*p.f,sMin:2,sMax:6,grav:.05});
    Audio.sfx.dodge();
  }

  // Skills
  const skMap={'a':0,'s':1,'d':2,'f':3,'g':4,'A':0,'S':1,'D':2,'F':3,'G':4};
  for(const [key,idx] of Object.entries(skMap)){
    if(Input.jp[key]&&idx<p.skills.length){ useSkill(p,G,idx); break; }
  }

  // Pause
  if(Input.jp['p']||Input.jp['P']){
    G.paused=!G.paused;
    document.getElementById('pauseScreen').classList.toggle('hidden',!G.paused);
  }
}

function doNormalAttack(p, G) {
  p.attackCd=16; p.attackAnim=14;
  p.comboCount=Math.min(6,(p.comboCount||0)+1);
  p.comboTimer=90;
  if(p.comboCount>G.maxCombo) G.maxCombo=p.comboCount;

  // Combo UI
  const ce=document.getElementById('combo');
  document.getElementById('combo-count').textContent=p.comboCount+'HIT';
  ce.style.opacity=p.comboCount>=2?'1':'0';
  const scale=1+Math.min(p.comboCount*.08,.5);
  document.getElementById('combo-count').style.transform=`scale(${scale})`;

  const comboMult=1+p.comboCount*.12;
  const dmgRes=calcDmg(p,comboMult);
  const ax=p.x+(p.f===1?p.w:-65);
  hitAOE(p,G,ax,p.y-10,70,60,dmgRes,dmgRes.crit);
  PS.spawn(ax+(p.f===1?30:0)-G.cam,p.y+25,{n:dmgRes.crit?14:7,col:[p.col,'#ffcc00'],spread:.7,dir:p.f===1?0:Math.PI,sMin:2,sMax:dmgRes.crit?7:5,glow:dmgRes.crit});
  Audio.sfx.attack();
  if(dmgRes.crit) screenShake(G,3,5);
}

function useSkill(p, G, idx) {
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;
  p.skillCds[idx]=sk.cd*60;
  sk.fn(p,G);
  Audio.sfx.skill();
}

// ══════════════════════════════════════════════════
// ENEMY AI
// ══════════════════════════════════════════════════
function updateEnemies(G, dt) {
  const p=G.player;
  for(const e of G.enemies){
    if(!e.alive) continue;
    if(e.dying){ e.deathTimer-=dt; continue; }

    // Status effects
    if(e.freeze>0){ e.freeze-=dt; continue; }
    if(e.stun>0){ e.stun-=dt; continue; }
    const slowMult=e.slow>0?.4:1;
    if(e.slow>0) e.slow-=dt;
    if(e.burn>0){ e.burn-=dt; e.burnTimer-=dt; if(e.burnTimer<=0){ e.hp-=Math.round(e.maxHp*.018); e.burnTimer=25; PS.spawn(e.x+e.w/2,e.y,{n:4,col:['#ff4400','#ff8800'],sMin:1,sMax:3,upB:2}); } }
    if(e.poison>0){ e.poison-=dt; if(!e.poisonTimer||e.poisonTimer<=0){ e.hp-=e.poisonDmg||5; e.poisonTimer=20; PS.spawn(e.x+e.w/2,e.y,{n:3,col:['#44cc44','#88ff44'],sMin:1,sMax:3,upB:1}); } if(e.poisonTimer>0) e.poisonTimer-=dt; if(e.hp<=0){ killTarget(G,e); continue; } }

    if(e.hitFlash>0) e.hitFlash-=dt;

    const dx=p.x-e.x;
    if(Math.abs(dx)<380) e.aggro=true;

    if(e.aggro){
      e.f=dx>0?1:-1;
      const spd=e.spd*slowMult;

      switch(e.ai){
        case 'charge':
          if(Math.abs(dx)>50) e.x+=e.f*spd*dt*(Math.abs(dx)<120?1.5:1);
          break;
        case 'brute':
          if(Math.abs(dx)>55) e.x+=e.f*spd*.9*dt;
          break;
        case 'slow':
          if(Math.abs(dx)>60) e.x+=e.f*spd*.7*dt;
          break;
        case 'tank':
          if(Math.abs(dx)>65) e.x+=e.f*spd*.65*dt;
          break;
        case 'normal':
          if(Math.abs(dx)>52) e.x+=e.f*spd*dt;
          break;
        case 'ranged':
          // Keep distance
          if(Math.abs(dx)<180) e.x-=e.f*spd*dt*.8;
          else if(Math.abs(dx)>300) e.x+=e.f*spd*dt*.7;
          break;
      }
    }

    // Gravity
    e.vy=(e.vy||0)+GRAVITY*dt*.55;
    e.y+=e.vy*dt;
    if(e.y+e.h>=FLOOR_Y){ e.y=FLOOR_Y-e.h; e.vy=0; }
    // Platform
    for(const pl of G.platforms){
      if(e.vy>=0&&e.x+e.w>pl.x&&e.x<pl.x+pl.w&&e.y+e.h>pl.y&&e.y+e.h<pl.y+pl.h+12){
        e.y=pl.y-e.h; e.vy=0;
      }
    }

    e.attackTimer-=dt;
    if(e.attackTimer<=0&&e.aggro){
      if(e.ranged){
        if(Math.abs(dx)<360){
          e.attackTimer=100+Math.random()*60;
          spawnProj(G,e.x+e.w/2,e.y+e.h/2,e.f*10+(Math.random()-.5)*1,-1.5+Math.random()*3,
            Math.round(e.atk*.65),'#aa44ff','enemy',{sz:9,life:85});
        }
      } else {
        if(Math.abs(dx)<64&&Math.abs(p.y-e.y)<65){
          e.attackTimer=80+Math.random()*40;
          if(p.dodgeAnim<=0){
            const dmg=Math.max(1,e.atk-Math.round((p.def+(p.defBonus||0))*.55)+Math.floor(Math.random()*6)-3);
            takeDmg(G,dmg);
          }
        }
      }
    }
  }
}

// ══════════════════════════════════════════════════
// BOSS AI
// ══════════════════════════════════════════════════
function updateBoss(G, dt) {
  const b=G.boss, p=G.player;
  if(!b.alive) return;
  if(b.dying){ b.deathTimer=(b.deathTimer||30)-dt; return; }

  if(b.freeze>0){ b.freeze-=dt; return; }
  if(b.stun>0){ b.stun-=dt; return; }
  if(b.hitFlash>0) b.hitFlash-=dt;

  // Phase transitions
  const hpPct=b.hp/b.maxHp;
  if(!b.phase2&&hpPct<.6){
    b.phase2=true; b.spd*=1.35; b.atk=Math.round(b.atk*1.3);
    document.getElementById('bossPhaseLabel').textContent='⚠ PHASE 2';
    screenShake(G,12,40);
    PS.spawn(b.x+b.w/2,b.y+b.h/2,{n:50,col:['#ff4400','#ff0000','#ff8800'],glow:true,sMin:4,sMax:12});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true; b.spd*=1.35; b.atk=Math.round(b.atk*1.3);
    document.getElementById('bossPhaseLabel').textContent='💀 PHASE 3 - ENRAGE';
    screenShake(G,18,60);
    PS.spawn(b.x+b.w/2,b.y+b.h/2,{n:80,col:['#ff0000','#cc00ff','#ffffff'],glow:true,sMin:5,sMax:15,type:'star'});
    Audio.sfx.bigSkill();
  }

  const dx=p.x-b.x;
  b.f=dx>0?1:-1;
  if(Math.abs(dx)>90) b.x+=b.f*b.spd*dt*.9;

  b.vy=(b.vy||0)+GRAVITY*dt*.5;
  b.y+=b.vy*dt;
  if(b.y+b.h>=FLOOR_Y){ b.y=FLOOR_Y-b.h; b.vy=0; }
  b.x=Math.max(50,Math.min(STAGE_W-b.w-50,b.x));

  b.attackTimer-=dt;
  if(Math.abs(dx)<95&&b.attackTimer<=0&&p.invincible<=0){
    b.attackTimer=b.phase3?45:b.phase2?60:80;
    if(Math.abs(p.y-b.y)<90&&p.dodgeAnim<=0){
      const dmg=Math.max(1,b.atk-Math.round((p.def+(p.defBonus||0))*.5)+Math.floor(Math.random()*12)-6);
      takeDmg(G,dmg);
    }
  }

  b.projTimer-=dt;
  const projInterval=b.phase3?50:b.phase2?70:110;
  if(b.projTimer<=0){
    b.projTimer=projInterval;
    if(b.phase3){
      // 3-way spread
      for(let i=-1;i<=1;i++){
        spawnProj(G,b.x+b.w/2,b.y+b.h*.4,b.f*9,i*4,Math.round(b.atk*.55),'#ff2200','enemy',{sz:14,emoji:'💥',life:85,grav:.08});
      }
    } else if(b.phase2){
      spawnProj(G,b.x+b.w/2,b.y+b.h*.4,b.f*9,-2,Math.round(b.atk*.6),'#ff4400','enemy',{sz:14,emoji:'💥',life:90,grav:.1});
      spawnProj(G,b.x+b.w/2,b.y+b.h*.4,(p.x-b.x)*.04,(p.y-b.y)*.04-2,Math.round(b.atk*.5),'#ff4400','enemy',{sz:12,life:80});
    } else {
      spawnProj(G,b.x+b.w/2,b.y+b.h*.4,b.f*8,-2,Math.round(b.atk*.6),'#ff4400','enemy',{sz:14,emoji:'💥',life:90,grav:.1});
    }
  }

  // Update boss HP bar
  document.getElementById('bossHpFill').style.width=Math.max(0,(b.hp/b.maxHp)*100)+'%';
}

// ══════════════════════════════════════════════════
// ITEMS (floor pickups)
// ══════════════════════════════════════════════════
function updateItems(G, dt) {
  const p=G.player;
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAVITY*dt*.7;
    it.y+=it.vy*dt;
    if(it.y+20>=FLOOR_Y){ it.y=FLOOR_Y-20; it.vy=0; }

    // Pickup check
    const sx=it.x-G.cam;
    if(sx>p.x-G.cam-30&&sx<p.x-G.cam+p.w+30&&it.y>p.y-10&&it.y<p.y+p.h+20){
      // Pick up
      if(it.type==='consume'){
        const result=it.fn(p);
        showItemFloat(sx,it.y,it.icon+' '+result,it.col||'#ffcc00');
        Audio.sfx.itemDrop();
      } else {
        // Equipment
        const slot=it.slot;
        p.equip[slot]=it;
        const result=it.fn(p);
        showItemFloat(sx,it.y,it.icon+' '+it.name,RARITY_COL[it.rarity||0]);
        G.droppedItems.push({icon:it.icon,name:it.name,rarity:it.rarity||0});
        Audio.sfx.equip();
        updateEquipUI();
      }
      it.alive=false;
      return false;
    }
    return true;
  });
}

function updateEquipUI() {
  if(!G) return;
  const p=G.player;
  const slots=['wpn','arm','acc'];
  const icons=['🗡️','🛡️','💍'];
  slots.forEach((s,i)=>{
    const el=document.getElementById('eq-'+s);
    if(el) el.textContent=p.equip[s]?p.equip[s].icon:icons[i];
  });
}

// ══════════════════════════════════════════════════
// RENDER
// ══════════════════════════════════════════════════
const canvas=document.getElementById('gc');
const ctx=canvas.getContext('2d');

function gameRender() {
  if(!G) return;
  ctx.save();

  // Screen shake
  if(G.shakeTimer>0){
    const s=G.shakeAmt*(G.shakeTimer/20)*.6;
    ctx.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }

  const st=G.stage;
  ctx.fillStyle=st.bg;
  ctx.fillRect(0,0,CW,CH);

  drawBG(ctx,st,G);
  drawPlatforms(ctx,G);
  drawFloor(ctx,G,st);

  PS.draw(ctx,G.cam);

  drawProjectiles(ctx,G);
  drawItems(ctx,G);
  drawEnemies(ctx,G);
  if(G.boss&&(G.boss.alive||G.boss.dying)) drawBoss(ctx,G);
  drawPlayer(ctx,G);

  ctx.restore();
  drawMinimap(G);
}

function drawBG(ctx, st, G) {
  // Animated parallax bg elements
  const layers=[
    {speed:.08,color:st.torchCol||'#ff6600',count:8,alpha:.08},
    {speed:.2, color:st.torchCol||'#ff6600',count:5,alpha:.12},
    {speed:.4, color:st.torchCol||'#ff6600',count:3,alpha:.18},
  ];

  for(const layer of layers){
    for(let i=0;i<layer.count;i++){
      const tx=((i*347+G.bgScroll*layer.speed*20-G.cam*layer.speed)%STAGE_W+STAGE_W)%(CW+100)-50;
      const ty=30+(i*97)%(FLOOR_Y-100);
      ctx.save();
      ctx.globalAlpha=layer.alpha*(Math.sin(G.timer*.05+i)*.3+.7);
      ctx.fillStyle=layer.color;
      ctx.shadowColor=layer.color;
      ctx.shadowBlur=15;
      ctx.beginPath(); ctx.arc(tx,ty,3,0,Math.PI*2); ctx.fill();
      ctx.shadowBlur=0;
      ctx.restore();
    }
  }

  // Ambient dungeon effect
  if(st.ambientCol){
    ctx.fillStyle=st.ambientCol;
    ctx.fillRect(0,0,CW,CH);
  }

  // Stage background name
  ctx.save();
  ctx.globalAlpha=.04;
  ctx.font='900 120px Black Han Sans,sans-serif';
  ctx.fillStyle='#ffffff';
  ctx.textAlign='center';
  ctx.fillText(st.name,CW/2,CH/2+40);
  ctx.restore();
}

function drawPlatforms(ctx, G) {
  const st=G.stage;
  for(const pl of G.platforms){
    const px=pl.x-G.cam;
    if(px>CW+10||px+pl.w<-10) continue;
    ctx.fillStyle=st.fl;
    ctx.fillRect(px,pl.y,pl.w,pl.h);
    ctx.fillStyle='rgba(255,150,0,.18)';
    ctx.fillRect(px,pl.y,pl.w,2);
    ctx.fillStyle='rgba(0,0,0,.3)';
    ctx.fillRect(px,pl.y+pl.h-3,pl.w,3);
  }
}

function drawFloor(ctx, G) {
  const s=G.stage;
  ctx.fillStyle=s.fl;
  ctx.fillRect(0,FLOOR_Y,CW,CH-FLOOR_Y);
  ctx.fillStyle='rgba(255,150,0,.22)';
  ctx.fillRect(0,FLOOR_Y,CW,2);
}

function drawPlayer(ctx, G) {
  const p=G.player;
  const px=p.x-G.cam;
  const flicker=p.invincible>0&&Math.floor(G.timer/3)%2===0;
  if(flicker) return;

  ctx.save();
  ctx.translate(px+p.w/2,p.y+p.h/2);
  if(p.f===-1) ctx.scale(-1,1);

  // Dodge afterimage
  if(p.dodgeAnim>0){
    for(let i=1;i<=3;i++){
      ctx.globalAlpha=(p.dodgeAnim/20)*(i/3)*.35;
      ctx.font='40px serif';
      ctx.textAlign='center';
      ctx.textBaseline='middle';
      ctx.fillText(p.icon,-i*16,0);
    }
    ctx.globalAlpha=1;
  }

  // Buff aura
  if(p.buffAtk>1){
    ctx.shadowColor='#ff2200'; ctx.shadowBlur=25;
    ctx.strokeStyle='rgba(255,50,0,.3)';
    ctx.lineWidth=3;
    ctx.beginPath();
    ctx.arc(0,0,32,0,Math.PI*2);
    ctx.stroke();
  }

  // Hit flash
  if(p.hitAnim>0){
    ctx.filter='brightness(3) saturate(0)';
  }

  // Status effect tints
  const se=p.statusEffects||{};
  if(se.freeze>0) ctx.filter='hue-rotate(200deg) brightness(1.6)';
  if(se.burn>0) ctx.filter='hue-rotate(-20deg) brightness(1.3)';
  if(se.poison>0) ctx.filter='hue-rotate(90deg) brightness(.9)';

  ctx.font='44px serif';
  ctx.textAlign='center';
  ctx.textBaseline='middle';
  ctx.fillText(p.icon,0,0);
  ctx.filter='none';

  // Attack swing
  if(p.attackAnim>0){
    const a=p.attackAnim/14;
    ctx.globalAlpha=a*.6;
    ctx.font='22px serif';
    ctx.fillText('💫',32,-18);
  }

  ctx.restore();

  // Shadow
  ctx.save();
  ctx.globalAlpha=.3;
  ctx.fillStyle='#000';
  ctx.beginPath();
  ctx.ellipse(px+p.w/2,FLOOR_Y+4,p.w*.5,6,0,0,Math.PI*2);
  ctx.fill();
  ctx.restore();

  // HP indicator (mini bar over head)
  if(p.hp<p.maxHp){
    const bw=40, bh=4;
    const bx=px+p.w/2-bw/2;
    ctx.fillStyle='rgba(0,0,0,.5)';
    ctx.fillRect(bx,p.y-10,bw,bh);
    ctx.fillStyle=p.hp/p.maxHp>.5?'#22cc22':p.hp/p.maxHp>.25?'#ccaa00':'#cc2200';
    ctx.fillRect(bx,p.y-10,bw*(p.hp/p.maxHp),bh);
  }
}

function drawEnemies(ctx, G) {
  for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const ex=e.x-G.cam;
    if(ex<-80||ex>CW+80) continue;
    const alpha=e.dying?(e.deathTimer/30):1;
    ctx.save();
    ctx.globalAlpha=alpha;
    ctx.translate(ex+e.w/2,e.y+e.h/2);
    if(e.f===1) ctx.scale(-1,1);

    if(e.freeze>0) ctx.filter='hue-rotate(200deg) brightness(1.7)';
    if(e.burn>0) ctx.filter='hue-rotate(-20deg) brightness(1.3)';
    if(e.poison>0) ctx.filter='hue-rotate(90deg) brightness(.9)';
    if(e.hitFlash>0) ctx.filter='brightness(3) saturate(0)';

    if(e.dying) ctx.filter+=' blur(2px)';

    ctx.font=`${e.sz||28}px serif`;
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(e.icon,0,0);
    ctx.filter='none';

    ctx.restore();

    // HP bar
    if(!e.dying){
      const hpPct=Math.max(0,e.hp/e.maxHp);
      const bw=e.w+10, bh=5;
      const bx=ex-5, by=e.y-12;
      ctx.fillStyle='rgba(0,0,0,.65)';
      ctx.fillRect(bx,by,bw,bh);
      ctx.fillStyle=hpPct>.5?'#22cc22':hpPct>.25?'#ccaa00':'#cc2200';
      ctx.fillRect(bx,by,bw*hpPct,bh);

      // Status icons above hp bar
      let sOffset=0;
      if(e.freeze>0){ drawStatusIcon(ctx,bx+sOffset,by-10,'❄',3); sOffset+=12; }
      if(e.burn>0){ drawStatusIcon(ctx,bx+sOffset,by-10,'🔥',3); sOffset+=12; }
      if(e.poison>0){ drawStatusIcon(ctx,bx+sOffset,by-10,'☠',3); sOffset+=12; }
      if(e.stun>0){ drawStatusIcon(ctx,bx+sOffset,by-10,'💫',3); }
    }
  }
}

function drawStatusIcon(ctx, x, y, icon, sz) {
  ctx.font=`${sz+7}px serif`;
  ctx.textAlign='left'; ctx.textBaseline='middle';
  ctx.fillText(icon,x,y);
}

function drawBoss(ctx, G) {
  const b=G.boss;
  const bx=b.x-G.cam;
  if(bx<-100||bx>CW+100) return;

  const alpha=b.dying?(b.deathTimer||30)/30:1;
  ctx.save();
  ctx.globalAlpha=alpha;
  ctx.translate(bx+b.w/2,b.y+b.h/2);
  if(b.f===1) ctx.scale(-1,1);

  // Glow aura
  ctx.shadowColor=b.col; ctx.shadowBlur=30;

  if(b.phase3){
    ctx.filter='hue-rotate(240deg) brightness(1.5)';
  } else if(b.phase2){
    ctx.filter='hue-rotate(120deg) brightness(1.25)';
  }

  if(b.hitFlash>0) ctx.filter='brightness(4) saturate(0)';

  ctx.font='72px serif';
  ctx.textAlign='center'; ctx.textBaseline='middle';
  ctx.fillText(b.icon,0,0);
  ctx.filter='none'; ctx.shadowBlur=0;
  ctx.restore();

  // HP bar above boss
  if(!b.dying){
    const hpPct=Math.max(0,b.hp/b.maxHp);
    ctx.fillStyle='rgba(0,0,0,.75)';
    ctx.fillRect(bx+b.w/2-50,b.y-16,100,8);
    ctx.fillStyle=hpPct>.4?'#ff4400':'#ff0000';
    ctx.fillRect(bx+b.w/2-50,b.y-16,100*hpPct,8);
    ctx.fillStyle='#ff8800';
    ctx.font='700 11px Noto Sans KR,sans-serif';
    ctx.textAlign='center';
    ctx.fillText(b.name,bx+b.w/2,b.y-20);
  }
}

function drawProjectiles(ctx, G) {
  for(const proj of G.projectiles){
    const px=proj.x-G.cam;
    if(px<-30||px>CW+30) continue;
    if(proj.emoji){
      ctx.font=`${proj.sz*1.8}px serif`;
      ctx.textAlign='center'; ctx.textBaseline='middle';
      ctx.fillText(proj.emoji,px,proj.y);
    } else {
      ctx.save();
      ctx.fillStyle=proj.col;
      ctx.shadowColor=proj.col; ctx.shadowBlur=10;
      ctx.beginPath();
      ctx.arc(px,proj.y,proj.sz,0,Math.PI*2);
      ctx.fill();
      ctx.shadowBlur=0;
      ctx.restore();
    }
  }
}

function drawItems(ctx, G) {
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam;
    if(ix<-30||ix>CW+30) continue;
    ctx.save();
    // Glow
    ctx.shadowColor=it.col||'#ffcc00'; ctx.shadowBlur=12;
    ctx.font='22px serif';
    ctx.textAlign='center'; ctx.textBaseline='middle';
    ctx.fillText(it.icon,ix,it.y);
    ctx.shadowBlur=0;
    // Bobbing
    const bob=Math.sin(G.timer*.08+it.x*.01)*3;
    ctx.globalAlpha=.7;
    ctx.fillStyle=RARITY_COL[it.rarity||0];
    ctx.fillRect(ix-8,it.y+14+bob,16,3);
    ctx.restore();
  }
}

function drawMinimap(G) {
  const mc=document.getElementById('minimapCanvas');
  const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,120,28);
  mctx.fillStyle='rgba(0,0,0,.5)';
  mctx.fillRect(0,0,120,28);

  const scale=120/STAGE_W;
  const p=G.player;
  // Enemies
  for(const e of G.enemies){
    if(!e.alive) continue;
    mctx.fillStyle=e.col||'#ff4444';
    mctx.fillRect(e.x*scale,8,3,3);
  }
  // Boss
  if(G.boss&&G.boss.alive){
    mctx.fillStyle='#ff0000';
    mctx.fillRect(G.boss.x*scale-1,6,5,5);
  }
  // Player
  mctx.fillStyle='#00ffaa';
  mctx.fillRect(p.x*scale-2,8,4,4);
  // Cam indicator
  mctx.strokeStyle='rgba(255,150,0,.4)';
  mctx.lineWidth=1;
  mctx.strokeRect(G.cam*scale,1,CW*scale,26);
}

// ══════════════════════════════════════════════════
// HUD UPDATE
// ══════════════════════════════════════════════════
function updateHUD() {
  if(!G) return;
  const p=G.player;
  document.getElementById('hp-bar').style.width=Math.max(0,(p.hp/p.maxHp)*100)+'%';
  document.getElementById('mp-bar').style.width=Math.max(0,(p.mp/p.maxMp)*100)+'%';
  document.getElementById('hp-text').textContent=`${Math.max(0,p.hp)}/${p.maxHp}`;
  document.getElementById('xp-bar').style.width=Math.min(100,(p.xp/p.xpNext)*100)+'%';
  document.getElementById('xp-text').textContent=`${p.xp}/${p.xpNext}`;
  document.getElementById('s-lv').textContent=p.level;
  document.getElementById('s-kills').textContent=p.kills;
  document.getElementById('s-score').textContent=p.score;
  document.getElementById('s-gold').textContent=p.gold;
  document.getElementById('hudName').textContent=p.name;
  document.getElementById('floorTag').textContent=`${G.stageIdx+1}스테이지`;

  // Buff icons
  const bi=document.getElementById('buffIcons');
  let biHtml='';
  if(p.buffAtk>1) biHtml+='<span title="공격력 강화">🔥</span>';
  const se=p.statusEffects||{};
  if(se.burn>0) biHtml+='<span title="화상">🔥</span>';
  if(se.freeze>0) biHtml+='<span title="빙결">❄️</span>';
  if(se.poison>0) biHtml+='<span title="독">☠️</span>';
  if(p.invincible>30) biHtml+='<span title="무적">🛡️</span>';
  bi.innerHTML=biHtml;

  // Skill bar
  const sc=document.getElementById('skCont');
  sc.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i];
    const cd=p.skillCds[i];
    const ready=cd<=0&&p.mp>=sk.mp;
    const div=document.createElement('div');
    div.className='sk '+(ready?'rdy':'cool');
    div.innerHTML=`${sk.icon}<span class="sk-key">${sk.key}</span><span class="sk-mp">${sk.mp}</span>`;
    if(cd>0){
      const cdDiv=document.createElement('div');
      cdDiv.className='sk-cd';
      cdDiv.textContent=Math.ceil(cd/60)+'s';
      div.appendChild(cdDiv);
    }
    div.title=`${sk.name} (MP:${sk.mp}, CD:${sk.cd}s)\n${sk.desc}`;
    sc.appendChild(div);
  }

  // Skill descriptions
  const sd=document.getElementById('skDesc');
  sd.innerHTML=p.skills.map(s=>`<b style="color:${s.col}">${s.icon}${s.key}</b>:${s.name}`).join('&nbsp;&nbsp;');
}

// ══════════════════════════════════════════════════
// UI HELPERS
// ══════════════════════════════════════════════════
function screenShake(G, amt, dur) {
  G.shakeAmt=Math.max(G.shakeAmt,amt);
  G.shakeTimer=Math.max(G.shakeTimer,dur);
}

function showDmgNum(sx, sy, dmg, crit, col) {
  const el=document.createElement('div');
  el.className='dnum';
  el.style.cssText=`left:${sx-18}px;top:${sy+56}px;font-size:${crit?'1.3':'0.95'}rem;color:${crit?'#ffff00':(col||'#ffffff')};`;
  el.textContent=crit?`${dmg}!!`:dmg;
  document.getElementById('gw').appendChild(el);
  setTimeout(()=>el.remove(),1000);
}

function showItemFloat(sx, sy, text, col) {
  const el=document.createElement('div');
  el.className='item-float';
  el.style.cssText=`left:${sx}px;top:${sy+56}px;color:${col||'#ffcc00'};border-color:${col||'#ffcc00'};`;
  el.textContent=text;
  document.getElementById('gw').appendChild(el);
  setTimeout(()=>el.remove(),1500);
}

let achievTimer=null;
function showAchiev(icon, title, sub) {
  const el=document.getElementById('achiev');
  document.getElementById('achiev-icon').textContent=icon;
  document.getElementById('achiev-text').textContent=title;
  document.getElementById('achiev-sub').textContent=sub;
  el.classList.add('show');
  clearTimeout(achievTimer);
  achievTimer=setTimeout(()=>el.classList.remove('show'),3000);
}

function checkAchievs(G) {
  for(const a of ACHIEVS){
    if(unlockedAchievs.has(a.id)) continue;
    if(a.check(G)){
      unlockedAchievs.add(a.id);
      localStorage.setItem('dc_achiev',JSON.stringify([...unlockedAchievs]));
      showAchiev('🏆',a.name,a.desc);
    }
  }
}

// ══════════════════════════════════════════════════
// STAGE TRANSITIONS
// ══════════════════════════════════════════════════
function stageClear(G) {
  G.phase='clear';
  const p=G.player;
  const elapsed=Math.round((Date.now()-G.startTime)/1000);
  const score=p.score+(G.stageDmgTaken===0?5000:0);
  p.score=score;
  if(score>highScore){ highScore=score; localStorage.setItem('dc_hi',highScore); }
  Audio.sfx.clear();
  document.getElementById('clearGrid').innerHTML=`
    <div class="res-row">처치 수 <b>${p.kills}</b></div>
    <div class="res-row">획득 골드 <b>💰${p.gold}</b></div>
    <div class="res-row">최종 점수 <b>${p.score}</b></div>
    <div class="res-row">소요 시간 <b>${elapsed}초</b></div>
    <div class="res-row">레벨 <b>Lv.${p.level}</b></div>
    <div class="res-row">무피해 보너스 <b>${G.stageDmgTaken===0?'+5000':'없음'}</b></div>
  `;
  const dl=document.getElementById('dropList');
  dl.innerHTML=G.droppedItems.map(it=>`<div class="drop-item ${it.rarity>=2?'rare':''} ${it.rarity>=3?'epic':''}">${it.icon} ${it.name}</div>`).join('')||'<div style="color:#444;font-size:.6rem">획득 아이템 없음</div>';
  document.getElementById('stageClear').classList.remove('hidden');
}

function gameOver(G) {
  if(!G||G.phase!=='play') return;
  G.phase='over';
  G.player.alive=false;
  const p=G.player;
  Audio.sfx.death();
  document.getElementById('overGrid').innerHTML=`
    <div class="res-row">처치 수 <b>${p.kills}</b></div>
    <div class="res-row">획득 골드 <b>💰${p.gold}</b></div>
    <div class="res-row">최종 점수 <b>${p.score}</b></div>
    <div class="res-row">레벨 <b>Lv.${p.level}</b></div>
    <div class="res-row">스테이지 <b>${G.stageIdx+1}</b></div>
    <div class="res-row">최고 기록 <b>${highScore}</b></div>
  `;
  setTimeout(()=>document.getElementById('gameOver').classList.remove('hidden'),700);
}

// ══════════════════════════════════════════════════
// SHOP
// ══════════════════════════════════════════════════
function buildShop(G) {
  const p=G.player;
  document.getElementById('shopGoldText').textContent=`보유 골드: ${p.gold}💰`;

  // Random selection of items to sell
  const available=[];
  // Always include potions
  available.push(ITEM_POOL[0],ITEM_POOL[1],ITEM_POOL[2]);
  // Random equipment
  const equip=ITEM_POOL.filter(it=>it.type!=='consume');
  for(let i=0;i<4;i++) available.push(equip[Math.floor(Math.random()*equip.length)]);

  const grid=document.getElementById('shopGrid');
  grid.innerHTML=available.map((it,idx)=>{
    const cant=p.gold<it.price;
    return `<div class="shop-item ${cant?'cant':''}" onclick="UI.buyItem(${idx})">
      <div class="si-icon">${it.icon}</div>
      <div class="si-name">${it.name}</div>
      <div class="si-desc">${it.type==='consume'?'소모품':'장비 ('+RARITY[it.rarity||0]+')'}</div>
      <div class="si-price ${cant?'cant':''}">${it.price}💰</div>
    </div>`;
  }).join('');

  // Store reference for buying
  G.shopItems=available;
}

// ══════════════════════════════════════════════════
// UI CONTROLLER
// ══════════════════════════════════════════════════
const UI = {
  selectedChar:null,
  animId:null,
  lastTs:0,

  buildTitle() {
    const grid=document.getElementById('charGrid');
    grid.innerHTML=CHARS.map(c=>{
      const stars=c.stars;
      const mkStars=(n,max=5)=>[...Array(max)].map((_,i)=>`<span class="star ${i<n?'on':''}">${i<n?'★':'☆'}</span>`).join('');
      return `<div class="ccard" id="cc-${c.id}" onclick="UI.selectChar('${c.id}')">
        <span class="ccard-icon">${c.icon}</span>
        <div class="ccard-name">${c.name}</div>
        <div class="ccard-type">${c.type}</div>
        <div class="ccard-stats">
          <div class="cstat">공격 <span>${mkStars(stars.atk)}</span></div>
          <div class="cstat">방어 <span>${mkStars(stars.def)}</span></div>
          <div class="cstat">속도 <span>${mkStars(stars.spd)}</span></div>
          <div class="cstat">사거리 <span>${mkStars(stars.range)}</span></div>
        </div>
        <div style="font-size:.5rem;color:#555;margin-top:6px;padding:0 2px">${c.desc}</div>
      </div>`;
    }).join('');
  },

  selectChar(id) {
    this.selectedChar=id;
    document.querySelectorAll('.ccard').forEach(c=>c.classList.remove('sel'));
    document.getElementById('cc-'+id)?.classList.add('sel');
    document.getElementById('startBtn').disabled=false;
    Audio.resume();
    Audio.sfx.itemDrop();
  },

  startGame(stageIdx=0) {
    if(!this.selectedChar) return;
    Audio.resume();
    this.hideAll();
    initGame(this.selectedChar,stageIdx);
    if(this.animId) cancelAnimationFrame(this.animId);
    this.lastTs=performance.now();
    this.loop(this.lastTs);
  },

  loop(ts) {
    const dt=Math.min((ts-this.lastTs)/16.67,3);
    this.lastTs=ts;
    gameUpdate(dt);
    gameRender();
    updateHUD();
    Input.flush();
    this.animId=requestAnimationFrame(t=>this.loop(t));
  },

  hideAll() {
    ['titleScreen','shopScreen','stageClear','gameOver','pauseScreen'].forEach(id=>{
      document.getElementById(id).classList.add('hidden');
    });
    document.getElementById('bossHpWrap').classList.remove('show');
  },

  openShop() {
    document.getElementById('stageClear').classList.add('hidden');
    buildShop(G);
    document.getElementById('shopScreen').classList.remove('hidden');
  },

  buyItem(idx) {
    if(!G) return;
    const it=G.shopItems[idx];
    if(!it||G.player.gold<it.price) return;
    G.player.gold-=it.price;
    const result=it.fn(G.player);
    Audio.sfx.buy();
    showItemFloat(400,200,it.icon+' '+result,RARITY_COL[it.rarity||0]);
    if(it.type!=='consume') updateEquipUI();
    buildShop(G); // Refresh
  },

  continueFromShop() {
    if(!G) return;
    const nextIdx=(G.stageIdx+1)%STAGES.length;
    document.getElementById('shopScreen').classList.add('hidden');
    this.startGame(nextIdx);
  },

  retryStage() {
    if(!G) return;
    const idx=G.stageIdx;
    document.getElementById('gameOver').classList.add('hidden');
    this.startGame(idx);
  },

  goTitle() {
    if(this.animId) cancelAnimationFrame(this.animId);
    G=null;
    ctx.clearRect(0,0,CW,CH);
    this.hideAll();
    document.getElementById('titleScreen').classList.remove('hidden');
    this.buildTitle();
  },
};

// ══════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════
Input.init();
UI.buildTitle();

// Idle canvas animation on title
(function idleLoop(ts) {
  if(G) return;
  const dt=Math.min((ts-UI.lastTs)/16.67,3);
  UI.lastTs=ts;
  ctx.fillStyle='#06040e';
  ctx.fillRect(0,0,CW,CH);
  ctx.save();
  ctx.font='900 80px Black Han Sans,sans-serif';
  ctx.globalAlpha=.04+Math.sin(ts*.001)*.02;
  ctx.fillStyle='#ff6600';
  ctx.textAlign='center';
  ctx.fillText('DUNGEON CRUSHER',CW/2,CH/2+40);
  ctx.restore();
  PS.update(dt); PS.draw(ctx,0);
  // Random particles on title
  if(Math.random()<.3) PS.spawn(Math.random()*CW,Math.random()*CH,{n:2,col:['#ff6600','#ffaa00','#cc44ff'],glow:true,sMin:1,sMax:3,grav:-.02,decay:.015});
  requestAnimationFrame(idleLoop);
})(0);

window.UI=UI;
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
    iframe{border:none!important;background:#06040e;}
    body{background:#06040e;}
    </style>
    """, unsafe_allow_html=True)
    components.html(GAME_HTML, height=640, scrolling=False)
