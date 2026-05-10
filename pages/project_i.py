import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>라인 배틀 저격전 v3</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Black+Han+Sans&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#05080f;--bg2:#080d1a;--gold:#ffd700;--green:#10d96e;--red:#ff4560;
  --blue:#4dabf7;--cyan:#22d3ee;--orange:#ff8c42;--purple:#b26cf7;
  --text:#e8f0ff;--text2:#7a8fb5;--border:rgba(255,255,255,.08);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{
  font-family:'Noto Sans KR',sans-serif;
  background:var(--bg);color:var(--text);
  /* FIX: overflow auto instead of hidden so nothing gets clipped */
  overflow:hidden;
  width:100%;height:100%;
  user-select:none;
  /* FIX: ensure pointer events work */
  pointer-events:auto;
}

/* ══ DIFF SELECT ══ */
#diff-select{
  position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:rgba(5,8,15,.98);
  background-image:radial-gradient(ellipse 70% 50% at 50% 30%,rgba(255,69,96,.07) 0%,transparent 70%);
  overflow-y:auto;
  /* FIX: ensure clicks register */
  pointer-events:auto;
}
.ds-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:clamp(1.8rem,5vw,3.2rem);
  background:linear-gradient(135deg,#ff4560,#ff8c42,#ffd700);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  letter-spacing:3px;margin-bottom:4px;text-align:center;
}
.ds-sub{color:var(--text2);font-size:.76rem;letter-spacing:5px;margin-bottom:6px;text-align:center;}
.ds-version{
  display:inline-block;
  background:rgba(255,140,66,.15);border:1px solid rgba(255,140,66,.4);
  color:var(--orange);border-radius:20px;padding:2px 12px;
  font-size:.72rem;font-weight:700;margin-bottom:24px;letter-spacing:2px;
}
.diff-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:600px;width:92%;margin-bottom:18px;}
@media(min-width:600px){.diff-grid{grid-template-columns:repeat(4,1fr);max-width:780px;}}
.diff-card{
  background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.08);
  border-radius:14px;padding:20px 12px;cursor:pointer;transition:all .22s;
  text-align:center;position:relative;overflow:hidden;
  /* FIX: explicit pointer events */
  pointer-events:auto;
}
.diff-card:hover,.diff-card.sel{transform:translateY(-5px);}
.diff-card[data-d="0"]:hover,.diff-card[data-d="0"].sel{border-color:#10d96e;box-shadow:0 0 28px rgba(16,217,110,.2);}
.diff-card[data-d="1"]:hover,.diff-card[data-d="1"].sel{border-color:#4dabf7;box-shadow:0 0 28px rgba(77,171,247,.2);}
.diff-card[data-d="2"]:hover,.diff-card[data-d="2"].sel{border-color:#ff8c42;box-shadow:0 0 28px rgba(255,140,66,.2);}
.diff-card[data-d="3"]:hover,.diff-card[data-d="3"].sel{border-color:#ff4560;box-shadow:0 0 28px rgba(255,69,96,.2);}
.diff-em{font-size:2.2rem;margin-bottom:7px;}
.diff-name{font-family:'Black Han Sans',sans-serif;font-size:1.1rem;margin-bottom:5px;}
.diff-desc{font-size:.72rem;color:var(--text2);line-height:1.65;}
.diff-tag{display:inline-block;font-size:.62rem;font-weight:700;border-radius:20px;padding:2px 8px;margin-top:7px;}
.feature-row{display:flex;gap:8px;margin-bottom:18px;flex-wrap:wrap;justify-content:center;max-width:780px;}
.feat-pill{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);
  border-radius:20px;padding:4px 12px;font-size:.72rem;color:var(--text2);
}
.feat-pill span{color:var(--cyan);}
.start-btn{
  padding:13px 52px;font-size:1.05rem;font-weight:900;
  font-family:'Black Han Sans',sans-serif;
  background:linear-gradient(135deg,#ff4560,#ff8c42);color:#fff;
  border:none;border-radius:40px;cursor:pointer;letter-spacing:2px;
  transition:all .2s;box-shadow:0 0 32px rgba(255,69,96,.4);
  pointer-events:auto;
}
.start-btn:hover{transform:scale(1.05);box-shadow:0 0 50px rgba(255,69,96,.6);}

/* ══ GAME LAYOUT ══ */
#game{
  display:none;
  width:100%;height:100vh;
  flex-direction:column;
  /* FIX: prevent overflow clipping the canvas */
  overflow:hidden;
  position:fixed;inset:0;
}

/* HUD */
.hud{
  background:rgba(5,8,15,.96);
  border-bottom:1px solid rgba(255,255,255,.07);
  padding:6px 12px;
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:4px;
  position:relative;z-index:50;
  /* FIX: fixed height so canvas calculation is predictable */
  height:50px;min-height:50px;max-height:50px;
  flex-shrink:0;
}
.hud-left,.hud-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.hud-title{font-family:'Orbitron',sans-serif;font-size:.78rem;font-weight:700;color:var(--orange);}
.base-hp-wrap{display:flex;align-items:center;gap:6px;}
.base-label{font-size:.68rem;color:var(--text2);font-weight:700;min-width:34px;}
.hp-bar-outer{
  width:100px;height:11px;
  background:rgba(255,255,255,.06);border-radius:6px;overflow:hidden;
  border:1px solid rgba(255,255,255,.08);
}
.hp-fill{height:100%;border-radius:6px;transition:width .3s;}
.hp-fill.ally{background:linear-gradient(90deg,#10d96e,#22d3ee);}
.hp-fill.enemy{background:linear-gradient(90deg,#ff4560,#ff8c42);}
.hp-val{font-size:.7rem;font-weight:700;min-width:30px;}
.hud-badge{border-radius:8px;padding:2px 8px;font-size:.72rem;font-weight:700;}
.res-badge{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);color:var(--gold);}
.wave-badge{background:rgba(178,108,247,.12);border:1px solid rgba(178,108,247,.3);color:var(--purple);}
.score-badge{background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.3);color:var(--cyan);}
.kills-badge{background:rgba(255,69,96,.1);border:1px solid rgba(255,69,96,.3);color:var(--red);}
.diff-hud-badge{font-size:.68rem;padding:2px 8px;border-radius:20px;font-weight:700;}
.weather-badge{
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  color:var(--text2);font-size:.68rem;padding:2px 8px;border-radius:8px;
}

/* CANVAS: fills remaining space */
#battlefield{
  display:block;
  width:100%;
  /* FIX: flex:1 with min-height:0 so it actually fills space */
  flex:1;min-height:0;
  cursor:crosshair;
}

/* BOTTOM PANEL */
.bot-panel{
  background:rgba(5,8,15,.96);
  border-top:1px solid rgba(255,255,255,.07);
  padding:5px 8px;
  display:flex;align-items:center;gap:5px;flex-wrap:wrap;
  position:relative;z-index:50;
  /* FIX: fixed height */
  height:72px;min-height:72px;max-height:72px;
  flex-shrink:0;
  overflow:hidden;
}
.unit-btn{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
  border-radius:10px;padding:4px 6px;cursor:pointer;transition:all .18s;
  text-align:center;min-width:58px;max-width:62px;
  position:relative;
  pointer-events:auto;
}
.unit-btn:hover:not(:disabled){
  transform:translateY(-2px);border-color:var(--cyan);
  background:rgba(34,211,238,.07);box-shadow:0 4px 14px rgba(34,211,238,.15);
}
.unit-btn:disabled{opacity:.35;cursor:not-allowed;}
.unit-btn .key-badge{position:absolute;top:2px;left:4px;font-size:.55rem;color:var(--text2);font-weight:900;}
.unit-btn .uem{font-size:1.1rem;display:block;margin-bottom:1px;}
.unit-btn .uname{font-size:.58rem;font-weight:700;display:block;}
.unit-btn .ucost{font-size:.55rem;color:var(--gold);display:block;}
.unit-btn .ucool{height:3px;background:rgba(255,255,255,.08);border-radius:2px;margin-top:2px;overflow:hidden;}
.unit-btn .ucool-fill{height:100%;background:var(--cyan);border-radius:2px;transition:width .1s linear;}

/* ABILITY ROW */
.ability-row{display:flex;gap:5px;margin-left:auto;align-items:center;flex-wrap:wrap;}
.abil-btn{
  background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);
  border-radius:10px;padding:4px 6px;cursor:pointer;text-align:center;min-width:52px;
  transition:all .2s;position:relative;pointer-events:auto;
}
.abil-btn:hover:not(.cooldown){border-color:var(--gold);background:rgba(255,215,0,.08);}
.abil-btn.cooldown{opacity:.45;cursor:not-allowed;}
.abil-btn .aem{font-size:1rem;display:block;}
.abil-btn .aname{font-size:.55rem;font-weight:700;color:var(--gold);}
.abil-btn .acool{font-size:.52rem;color:var(--text2);}
.abil-cd-bar{position:absolute;bottom:0;left:0;height:3px;background:var(--gold);border-radius:0 0 8px 8px;transition:width .1s linear;}

.snipe-hint{
  font-size:.62rem;color:var(--text2);line-height:1.4;padding-left:8px;
  border-left:2px solid rgba(255,255,255,.08);
}

/* SCOPE */
#scope{
  position:fixed;pointer-events:none;z-index:1000;display:none;
  filter:drop-shadow(0 0 6px rgba(255,69,96,0.5));
  /* FIX: translate so center of SVG is at cursor */
  transform:translate(-50%,-50%);
  left:-999px;top:-999px;
}
#scope svg{display:block;}

/* HEADSHOT FLASH */
#hs-flash{
  position:fixed;inset:0;pointer-events:none;z-index:900;
  background:rgba(255,215,0,0);transition:background .05s;
}

/* KILL FEED */
#killfeed{
  position:fixed;top:60px;right:14px;z-index:200;
  display:flex;flex-direction:column;gap:4px;pointer-events:none;
}
.kf-item{
  background:rgba(5,8,15,.88);border:1px solid rgba(255,69,96,.3);
  border-radius:7px;padding:4px 10px;font-size:.7rem;font-weight:700;
  animation:kfIn .2s,kfOut .3s 2.5s forwards;white-space:nowrap;
}
@keyframes kfIn{from{opacity:0;transform:translateX(20px);}to{opacity:1;transform:translateX(0);}}
@keyframes kfOut{to{opacity:0;transform:translateX(20px);}}

/* TOAST */
.twrap{
  position:fixed;top:70px;left:50%;transform:translateX(-50%);
  z-index:600;display:flex;flex-direction:column;align-items:center;
  gap:6px;pointer-events:none;
}
.toast{
  padding:6px 14px;border-radius:9px;font-size:.78rem;font-weight:700;
  background:rgba(8,13,26,.96);border:1px solid rgba(255,255,255,.1);
  animation:ti .22s,to2 .22s 2.3s forwards;white-space:nowrap;
}
@keyframes ti{from{opacity:0;transform:translateY(-8px);}to{opacity:1;transform:translateY(0);}}
@keyframes to2{to{opacity:0;transform:translateY(-8px);}}
.hs-toast{
  padding:8px 20px;border-radius:12px;font-size:.9rem;font-weight:900;
  background:rgba(255,215,0,.15);border:2px solid rgba(255,215,0,.6);
  color:#ffd700;text-shadow:0 0 10px #ffd700;
  animation:ti .15s,to2 .15s 1.8s forwards;white-space:nowrap;
  font-family:'Black Han Sans',sans-serif;
}

/* BOSS / EVENT ALERT */
#boss-alert{
  position:fixed;inset:0;z-index:400;pointer-events:none;
  display:flex;align-items:center;justify-content:center;
}
.boss-alert-box{
  font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,6vw,4rem);
  color:#ff4560;text-shadow:0 0 40px #ff4560,0 0 80px #ff4560;
  animation:bossAlert 2s ease-out forwards;
}
.event-alert-box{
  font-family:'Black Han Sans',sans-serif;font-size:clamp(1.5rem,4vw,3rem);
  color:#10d96e;text-shadow:0 0 30px #10d96e,0 0 60px #10d96e;
  animation:bossAlert 2s ease-out forwards;
}
.miniboss-alert-box{
  font-family:'Black Han Sans',sans-serif;font-size:clamp(1.5rem,4vw,2.8rem);
  color:#ff8c42;text-shadow:0 0 30px #ff8c42,0 0 60px #ff8c42;
  animation:bossAlert 2s ease-out forwards;
}
@keyframes bossAlert{
  0%{opacity:0;transform:scale(0.5);}
  30%{opacity:1;transform:scale(1.1);}
  70%{opacity:1;transform:scale(1);}
  100%{opacity:0;transform:scale(1.2);}
}

/* RESULT */
#result{
  display:none;position:fixed;inset:0;z-index:500;
  background:rgba(5,8,15,.97);
  flex-direction:column;align-items:center;justify-content:center;
  background-image:radial-gradient(ellipse 60% 50% at 50% 40%,rgba(255,215,0,.06) 0%,transparent 70%);
  pointer-events:auto;
}
.res-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:clamp(2.5rem,7vw,4rem);margin-bottom:6px;text-align:center;
}
.res-subtitle{font-size:.85rem;color:var(--text2);margin-bottom:22px;text-align:center;letter-spacing:2px;}
.res-stats{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:14px;padding:18px 24px;margin-bottom:20px;
  display:grid;grid-template-columns:repeat(4,1fr);gap:10px;min-width:360px;
}
.stat-item{text-align:center;}
.stat-v{font-size:1.3rem;font-weight:900;color:var(--gold);}
.stat-l{font-size:.68rem;color:var(--text2);margin-top:2px;}
.grade-box{
  font-family:'Black Han Sans',sans-serif;font-size:3.5rem;margin-bottom:14px;
  text-shadow:0 0 30px currentColor;
}
.res-btn-row{display:flex;gap:10px;}
.res-btn{
  padding:11px 32px;font-size:.88rem;font-weight:900;border:none;
  border-radius:36px;cursor:pointer;letter-spacing:2px;transition:all .2s;
  pointer-events:auto;
}
.res-btn.main{background:linear-gradient(135deg,var(--gold),#ff8c00);color:#1a0500;}
.res-btn.main:hover{transform:scale(1.05);}
.res-btn.menu{background:rgba(255,255,255,.06);color:var(--text2);border:1px solid rgba(255,255,255,.12);}
.res-btn.menu:hover{border-color:var(--cyan);color:var(--cyan);}

/* FW */
#fw{position:fixed;inset:0;pointer-events:none;z-index:490;overflow:hidden;}
@keyframes fwp{to{transform:translate(var(--dx),var(--dy));opacity:0;}}

/* SHOP MODAL */
#shop-modal{
  display:none;position:fixed;inset:0;z-index:450;
  background:rgba(0,0,0,.75);
  align-items:center;justify-content:center;
  backdrop-filter:blur(6px);pointer-events:auto;
}
.shop-box{
  background:linear-gradient(160deg,#0d1830,#1a2545);
  border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:20px;
  max-width:540px;width:94%;
  box-shadow:0 30px 80px rgba(0,0,0,.7);
  max-height:85vh;overflow-y:auto;pointer-events:auto;
}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.35rem;color:var(--gold);margin-bottom:4px;}
.shop-sub{color:var(--text2);font-size:.76rem;margin-bottom:12px;}
.shop-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:12px;}
.shop-item{
  background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
  border-radius:10px;padding:9px 6px;text-align:center;
  cursor:pointer;transition:all .2s;pointer-events:auto;
}
.shop-item:hover:not(.bought){border-color:var(--gold);background:rgba(255,215,0,.07);}
.shop-item.bought{opacity:.5;cursor:not-allowed;}
.shop-item .sem{font-size:1.4rem;display:block;margin-bottom:2px;}
.shop-item .sname{font-size:.7rem;font-weight:700;display:block;margin-bottom:2px;}
.shop-item .sdesc{font-size:.6rem;color:var(--text2);display:block;margin-bottom:3px;}
.shop-item .scost{font-size:.68rem;color:var(--gold);font-weight:700;}
.shop-close{
  padding:8px 24px;border-radius:30px;border:1px solid rgba(255,255,255,.12);
  background:rgba(255,255,255,.04);color:var(--text2);
  cursor:pointer;font-size:.85rem;font-weight:700;transition:all .2s;pointer-events:auto;
}
.shop-close:hover{border-color:var(--red);color:var(--red);}

/* NIGHT OVERLAY */
#night-overlay{
  position:fixed;inset:0;pointer-events:none;z-index:45;
  background:rgba(0,0,30,0);transition:background 3s;
}
</style>
</head>
<body>
<div id="fw"></div>
<div id="night-overlay"></div>
<div id="hs-flash"></div>

<!-- ══════════ DIFF SELECT ══════════ -->
<div id="diff-select">
  <div class="ds-title">⚔️ 라인 배틀 저격전</div>
  <div class="ds-sub">AGE OF WAR · SNIPER EDITION</div>
  <div class="ds-version">VERSION 3.0</div>

  <div class="feature-row">
    <div class="feat-pill">🛒 <span>웨이브 상점</span></div>
    <div class="feat-pill">💥 <span>특수 스킬 5종</span></div>
    <div class="feat-pill">👹 <span>보스+미니보스</span></div>
    <div class="feat-pill">🎯 <span>헤드샷 시스템</span></div>
    <div class="feat-pill">🌦️ <span>날씨 시스템</span></div>
    <div class="feat-pill">🔰 <span>기지 터렛</span></div>
    <div class="feat-pill">⚡ <span>이벤트 웨이브</span></div>
    <div class="feat-pill">🏆 <span>S~F 등급</span></div>
  </div>

  <div class="diff-grid">
    <div class="diff-card sel" data-d="0">
      <div class="diff-em">🟢</div>
      <div class="diff-name" style="color:#10d96e">초 보</div>
      <div class="diff-desc">느린 적 AI<br>빠른 자원 재생<br>풍부한 시작 자원</div>
      <div class="diff-tag" style="background:rgba(16,217,110,.15);color:#10d96e;border:1px solid rgba(16,217,110,.3);">추천 입문</div>
    </div>
    <div class="diff-card" data-d="1">
      <div class="diff-em">🔵</div>
      <div class="diff-name" style="color:#4dabf7">중 급</div>
      <div class="diff-desc">균형 잡힌 전투<br>다양한 유닛 소환<br>적당한 압박</div>
      <div class="diff-tag" style="background:rgba(77,171,247,.15);color:#4dabf7;border:1px solid rgba(77,171,247,.3);">밸런스</div>
    </div>
    <div class="diff-card" data-d="2">
      <div class="diff-em">🟠</div>
      <div class="diff-name" style="color:#ff8c42">어 려 움</div>
      <div class="diff-desc">최적화된 AI<br>강유닛 집중 소환<br>전략 필수</div>
      <div class="diff-tag" style="background:rgba(255,140,66,.15);color:#ff8c42;border:1px solid rgba(255,140,66,.3);">고수용</div>
    </div>
    <div class="diff-card" data-d="3">
      <div class="diff-em">🔴</div>
      <div class="diff-name" style="color:#ff4560">극 악</div>
      <div class="diff-desc">완벽한 자원 활용<br>최강 유닛 러시<br>강화된 보스</div>
      <div class="diff-tag" style="background:rgba(255,69,96,.15);color:#ff4560;border:1px solid rgba(255,69,96,.3);">🔥 불가능?</div>
    </div>
  </div>
  <button class="start-btn" id="start-btn">⚔️ 전투 시작</button>
</div>

<!-- ══════════ GAME ══════════ -->
<div id="game">
  <div class="hud">
    <div class="hud-left">
      <span class="hud-title">⚔️ AGE OF WAR v3</span>
      <div class="base-hp-wrap">
        <span class="base-label">🏰 아군</span>
        <div class="hp-bar-outer"><div class="hp-fill ally" id="ally-hp-bar" style="width:100%"></div></div>
        <span class="hp-val" id="ally-hp-val" style="color:var(--green)">1500</span>
      </div>
      <div class="base-hp-wrap">
        <span class="base-label">🏯 적군</span>
        <div class="hp-bar-outer"><div class="hp-fill enemy" id="enemy-hp-bar" style="width:100%"></div></div>
        <span class="hp-val" id="enemy-hp-val" style="color:var(--red)">1500</span>
      </div>
    </div>
    <div class="hud-right">
      <span class="hud-badge wave-badge" id="wave-badge">웨이브 1</span>
      <span class="hud-badge res-badge">💎 <span id="res-val">150</span></span>
      <span class="hud-badge score-badge">🏆 <span id="score-val">0</span></span>
      <span class="hud-badge kills-badge">💀 <span id="kills-val">0</span></span>
      <span class="weather-badge" id="weather-badge">☀️ 맑음</span>
      <span class="hud-badge diff-hud-badge" id="diff-badge"></span>
    </div>
  </div>

  <canvas id="battlefield"></canvas>

  <div class="bot-panel">
    <!-- 라인 선택 버튼 -->
    <div id="lane-selector" style="display:flex;gap:6px;width:100%;margin-bottom:6px;justify-content:center;">
      <button onclick="selectLane(0)" id="lane-btn-0" style="flex:1;padding:5px 4px;border-radius:8px;border:1.5px solid rgba(178,108,247,0.5);background:rgba(178,108,247,0.15);color:#b26cf7;font-size:0.75rem;font-weight:900;cursor:pointer;transition:all 0.2s;">⬆️ 탑</button>
      <button onclick="selectLane(1)" id="lane-btn-1" style="flex:1;padding:5px 4px;border-radius:8px;border:2px solid rgba(34,211,238,0.8);background:rgba(34,211,238,0.2);color:#22d3ee;font-size:0.75rem;font-weight:900;cursor:pointer;transition:all 0.2s;">➡️ 미드 ✓</button>
      <button onclick="selectLane(2)" id="lane-btn-2" style="flex:1;padding:5px 4px;border-radius:8px;border:1.5px solid rgba(16,217,110,0.5);background:rgba(16,217,110,0.15);color:#10d96e;font-size:0.75rem;font-weight:900;cursor:pointer;transition:all 0.2s;">⬇️ 바텀</button>
    </div>
    <button class="unit-btn" id="btn0" onclick="spawnAlly(0)">
      <span class="key-badge">1</span><span class="uem">🧍</span>
      <span class="uname">보병</span><span class="ucost">💎30</span>
      <div class="ucool"><div class="ucool-fill" id="cool0" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn1" onclick="spawnAlly(1)">
      <span class="key-badge">2</span><span class="uem">🪖</span>
      <span class="uname">돌격대</span><span class="ucost">💎60</span>
      <div class="ucool"><div class="ucool-fill" id="cool1" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn2" onclick="spawnAlly(2)">
      <span class="key-badge">3</span><span class="uem">💪</span>
      <span class="uname">중화기</span><span class="ucost">💎120</span>
      <div class="ucool"><div class="ucool-fill" id="cool2" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn3" onclick="spawnAlly(3)">
      <span class="key-badge">4</span><span class="uem">🏥</span>
      <span class="uname">의무병</span><span class="ucost">💎80</span>
      <div class="ucool"><div class="ucool-fill" id="cool3" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn4" onclick="spawnAlly(4)">
      <span class="key-badge">5</span><span class="uem">🎯</span>
      <span class="uname">저격수</span><span class="ucost">💎100</span>
      <div class="ucool"><div class="ucool-fill" id="cool4" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn5" onclick="spawnAlly(5)">
      <span class="key-badge">6</span><span class="uem">🛡️</span>
      <span class="uname">전차</span><span class="ucost">💎200</span>
      <div class="ucool"><div class="ucool-fill" id="cool5" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn6" onclick="spawnAlly(6)" style="border-color:rgba(178,108,247,.25);">
      <span class="key-badge">7</span><span class="uem">🤖</span>
      <span class="uname">기갑부대</span><span class="ucost">💎160</span>
      <div class="ucool"><div class="ucool-fill" id="cool6" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn7" onclick="spawnAlly(7)" style="border-color:rgba(255,100,50,.25);">
      <span class="key-badge">8</span><span class="uem">🔥</span>
      <span class="uname">화염방사</span><span class="ucost">💎90</span>
      <div class="ucool"><div class="ucool-fill" id="cool7" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn8" onclick="spawnAlly(8)" style="border-color:rgba(34,211,238,.25);">
      <span class="key-badge">9</span><span class="uem">🥷</span>
      <span class="uname">닌자</span><span class="ucost">💎75</span>
      <div class="ucool"><div class="ucool-fill" id="cool8" style="width:100%"></div></div>
    </button>

    <div class="ability-row">
      <div class="abil-btn" id="abil0" onclick="useAbility(0)">
        <span class="aem">💣</span>
        <span class="aname">공습</span>
        <span class="acool" id="acool0">Q</span>
        <div class="abil-cd-bar" id="abar0" style="width:100%"></div>
      </div>
      <div class="abil-btn" id="abil1" onclick="useAbility(1)">
        <span class="aem">⚡</span>
        <span class="aname">전격전</span>
        <span class="acool" id="acool1">E</span>
        <div class="abil-cd-bar" id="abar1" style="width:100%"></div>
      </div>
      <div class="abil-btn" id="abil2" onclick="useAbility(2)">
        <span class="aem">🛡️</span>
        <span class="aname">방어막</span>
        <span class="acool" id="acool2">R</span>
        <div class="abil-cd-bar" id="abar2" style="width:100%"></div>
      </div>
      <div class="abil-btn" id="abil3" onclick="useAbility(3)" style="border-color:rgba(255,50,50,.3);">
        <span class="aem">☢️</span>
        <span class="aname">핵폭탄</span>
        <span class="acool" id="acool3">W</span>
        <div class="abil-cd-bar" id="abar3" style="width:100%"></div>
      </div>
      <div class="abil-btn" id="abil4" onclick="useAbility(4)" style="border-color:rgba(100,200,255,.3);">
        <span class="aem">⏸️</span>
        <span class="aname">시간정지</span>
        <span class="acool" id="acool4">T</span>
        <div class="abil-cd-bar" id="abar4" style="width:100%"></div>
      </div>
      <button class="unit-btn" id="shop-btn" onclick="openShop()" style="border-color:rgba(255,215,0,.3);min-width:46px;max-width:52px;">
        <span class="uem">🛒</span>
        <span class="uname" style="color:var(--gold)">상점</span>
        <span class="ucost">S키</span>
      </button>
      <div class="snipe-hint">
        🔭 <b>클릭 저격</b><br>
        재장전: <span id="reload-status" style="color:var(--green)">준비</span>
        콤보: <span id="combo-val" style="color:var(--gold)">×1</span>
        관통: <span id="pierce-val" style="color:var(--purple)">×1</span>
      </div>
    </div>
  </div>
</div>

<!-- SCOPE -->
<div id="scope">
  <svg width="110" height="110" viewBox="0 0 110 110">
    <circle cx="55" cy="55" r="50" fill="rgba(0,0,0,0.12)" stroke="rgba(255,69,96,0.9)" stroke-width="2.5"/>
    <circle cx="55" cy="55" r="3" fill="rgba(255,69,96,1)"/>
    <line x1="55" y1="2"  x2="55" y2="36" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="55" y1="74" x2="55" y2="108" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="2"  y1="55" x2="36" y2="55" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="74" y1="55" x2="108" y2="55" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <circle cx="55" cy="55" r="18" fill="none" stroke="rgba(255,69,96,0.25)" stroke-width="1"/>
    <circle cx="55" cy="55" r="32" fill="none" stroke="rgba(255,69,96,0.15)" stroke-width="1"/>
  </svg>
</div>

<div id="killfeed"></div>
<div id="boss-alert" style="display:none;"></div>
<div id="shop-modal">
  <div class="shop-box">
    <div class="shop-title">🛒 전술 상점</div>
    <div class="shop-sub">💎 <span id="shop-res">0</span> — 업그레이드</div>
    <div class="shop-grid" id="shop-grid"></div>
    <button class="shop-close" onclick="closeShop()">✕ 닫기</button>
  </div>
</div>
<div class="twrap" id="twrap"></div>
<div id="result">
  <div class="grade-box" id="res-grade">S</div>
  <div class="res-title" id="res-title">🏆 승리!</div>
  <div class="res-subtitle" id="res-subtitle"></div>
  <div class="res-stats">
    <div class="stat-item"><div class="stat-v" id="st-score">0</div><div class="stat-l">최종 점수</div></div>
    <div class="stat-item"><div class="stat-v" id="st-kills">0</div><div class="stat-l">처치 수</div></div>
    <div class="stat-item"><div class="stat-v" id="st-wave">0</div><div class="stat-l">최고 웨이브</div></div>
    <div class="stat-item"><div class="stat-v" id="st-snipes">0</div><div class="stat-l">저격 성공</div></div>
  </div>
  <div class="res-btn-row">
    <button class="res-btn main" onclick="location.reload()">🔄 다시하기</button>
    <button class="res-btn menu" onclick="goMenu()">📋 메뉴</button>
  </div>
</div>

<script>
'use strict';
// ════════════════════════════════════════════════
//  UNIT DEFINITIONS
// ════════════════════════════════════════════════
const UNIT_DEFS = [
  // ALLY (0~8)
  {id:0, name:'보병',     em:'🧍',cost:30,  hp:100,  atk:10, spd:0.85,range:42,  ranged:false,pri:1,reward:12,  trainTime:40},
  {id:1, name:'돌격대',   em:'🪖',cost:60,  hp:190,  atk:22, spd:1.15,range:52,  ranged:false,pri:2,reward:22,  trainTime:60},
  {id:2, name:'중화기병', em:'💪',cost:120, hp:320,  atk:42, spd:0.6, range:70,  ranged:true, pri:4,reward:45,  trainTime:90},
  {id:3, name:'의무병',   em:'🏥',cost:80,  hp:120,  atk:4,  spd:0.75,range:65,  ranged:false,pri:1,reward:18,  trainTime:70, healer:true},
  {id:4, name:'저격수',   em:'🎯',cost:100, hp:80,   atk:70, spd:0.55,range:220, ranged:true, pri:3,reward:32,  trainTime:80},
  {id:5, name:'전차',     em:'🛡️',cost:200, hp:700,  atk:55, spd:0.4, range:90,  ranged:false,pri:5,reward:90,  trainTime:140},
  {id:6, name:'기갑부대', em:'🤖',cost:160, hp:450,  atk:50, spd:0.5, range:78,  ranged:false,pri:5,reward:70,  trainTime:110, armored:true},
  {id:7, name:'화염방사', em:'🔥',cost:90,  hp:140,  atk:35, spd:0.7, range:55,  ranged:false,pri:3,reward:28,  trainTime:65,  flamer:true},
  {id:8, name:'닌자',     em:'🥷',cost:75,  hp:90,   atk:45, spd:2.2, range:40,  ranged:false,pri:3,reward:24,  trainTime:55,  ninja:true},
  // ENEMY only (9~17)
  {id:9,  name:'적보병',  em:'👹',cost:30,  hp:95,   atk:9,  spd:0.9, range:42,  ranged:false,pri:1,reward:10},
  {id:10, name:'장교',    em:'🎖️',cost:150, hp:260,  atk:32, spd:0.8, range:58,  ranged:false,pri:5,reward:55},
  {id:11, name:'로켓병',  em:'🚀',cost:180, hp:140,  atk:70, spd:0.5, range:190, ranged:true, pri:5,reward:65},
  {id:12, name:'적탱크',  em:'🛡️',cost:280, hp:700,  atk:58, spd:0.38,range:85,  ranged:false,pri:5,reward:110},
  {id:13, name:'드론',    em:'🛸',cost:120, hp:70,   atk:25, spd:1.5, range:75,  ranged:true, pri:4,reward:38},
  {id:14, name:'보스',    em:'💀',cost:999, hp:3000, atk:80, spd:0.5, range:100, ranged:false,pri:5,reward:300, isBoss:true},
  {id:15, name:'미니보스',em:'😈',cost:600, hp:1200, atk:55, spd:0.65,range:85,  ranged:false,pri:5,reward:160, isMiniBoss:true},
  {id:16, name:'특공대',  em:'💣',cost:200, hp:160,  atk:60, spd:1.3, range:45,  ranged:false,pri:4,reward:70,  kamikaze:true},
  {id:17, name:'포격수',  em:'🎖️',cost:220, hp:180,  atk:85, spd:0.45,range:210, ranged:true, pri:5,reward:80},
];

// ════════════════════════════════════════════════
//  ABILITY DEFINITIONS
// ════════════════════════════════════════════════
const ABILITY_DEFS = [
  {id:0,name:'공습',em:'💣',key:'q',cd:600,
   fx:()=>{
     for(let i=0;i<5;i++) setTimeout(()=>{
       if(!G.running)return;
       const x=ALLY_BASE_X+100+Math.random()*(W-200);
       airstrikeBomb(x,GROUND-10);
     },i*200);
     toast('💣 공습 발동!','gold');
   }},
  {id:1,name:'전격전',em:'⚡',key:'e',cd:450,
   fx:()=>{
     G.blitzEnd=G.frame+480;
     G.units.filter(u=>u.side===0).forEach(u=>{if(!u._blitzed){u.spd*=2;u._blitzed=true;}});
     toast('⚡ 전격전! 아군 강화 8초!','gold');
   }},
  {id:2,name:'방어막',em:'🛡️',key:'r',cd:500,
   fx:()=>{
     G.shieldEnd=G.frame+600;
     toast('🛡️ 방어막 활성화! 10초!','good');
   }},
  {id:3,name:'핵폭탄',em:'☢️',key:'w',cd:900,
   fx:()=>{
     toast('☢️ 핵폭탄 투하!!!','bad');
     setTimeout(()=>{
       if(!G.running)return;
       const fl=document.getElementById('hs-flash');
       fl.style.background='rgba(255,255,200,0.85)';
       setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},400);
       const toKill=[...G.units.filter(u=>u.side===1&&u.hp>0&&!u.isBoss)];
       toKill.forEach(u=>{killUnit(u,0);});
       G.units.filter(u=>u.side===1&&u.isBoss&&u.hp>0).forEach(u=>{
         const dmg=Math.round(u.maxHp*0.35);
         u.hp-=dmg; spawnHit(u.x,u.y,'#ffd700',dmg);
       });
       G.enemyBase-=200+(G.wave*10);
       for(let i=0;i<40;i++){
         const ang=Math.random()*Math.PI*2;
         G.particles.push({x:W/2+(Math.random()-.5)*W*0.6,y:GROUND-30,
           vx:Math.cos(ang)*4,vy:Math.sin(ang)*4-3,
           col:['#ffd700','#ff8c42','#ff4560'][Math.floor(Math.random()*3)],life:35,size:6+Math.random()*6});
         G.effects.push({x:W/2+(Math.random()-.5)*W*0.5,y:GROUND-20,r:4,col:'#ff8c42',alpha:0.9,type:'bomb'});
       }
     },800);
   }},
  {id:4,name:'시간정지',em:'⏸️',key:'t',cd:700,
   fx:()=>{
     G.freezeEnd=G.frame+240;
     toast('⏸️ 시간정지! 4초간 적 동결!','wave');
   }},
];

// ════════════════════════════════════════════════
//  DIFFICULTY CONFIG
// ════════════════════════════════════════════════
const DIFF_CONFIG = [
  {name:'초보',   col:'#10d96e',bgCol:'rgba(16,217,110,.15)',bdCol:'rgba(16,217,110,.35)',
   resRate:2.2, botResRate:0.5, botPool:[9,9,9,1],       botDelay:3500,startRes:200,baseHp:1500,bossWave:10,miniBossWave:5},
  {name:'중급',   col:'#4dabf7',bgCol:'rgba(77,171,247,.15)',bdCol:'rgba(77,171,247,.35)',
   resRate:1.6, botResRate:1.0, botPool:[9,10,10,1,11],  botDelay:2300,startRes:150,baseHp:1500,bossWave:8, miniBossWave:4},
  {name:'어려움', col:'#ff8c42',bgCol:'rgba(255,140,66,.15)',bdCol:'rgba(255,140,66,.35)',
   resRate:1.1, botResRate:1.5, botPool:[10,11,11,12,13],botDelay:1700,startRes:120,baseHp:1500,bossWave:6, miniBossWave:3},
  {name:'극악',   col:'#ff4560',bgCol:'rgba(255,69,96,.15)',bdCol:'rgba(255,69,96,.35)',
   resRate:0.9, botResRate:2.2, botPool:[11,12,12,13,16,17],botDelay:1000,startRes:100,baseHp:1500,bossWave:5,miniBossWave:3},
];

// ════════════════════════════════════════════════
//  SHOP ITEMS
// ════════════════════════════════════════════════
const SHOP_ITEMS = [
  {id:'u_hp',    em:'❤️', name:'기지 수리',  desc:'아군 기지 HP +300',   cost:120,
   fx:()=>{G.allyBase=Math.min(G.allyBase+300,G.maxBase);toast('❤️ 기지 수리! +300 HP','good');}},
  {id:'u_res',   em:'💎', name:'자원 증폭',  desc:'자원 수급 +30%',       cost:150,repeatable:true,
   fx:()=>{G.resBonus=(G.resBonus||1)*1.3;toast('💎 자원 증폭!','good');}},
  {id:'u_atk',   em:'⚔️', name:'무기 강화',  desc:'아군 공격력 +25%',    cost:180,
   fx:()=>{G.dmgBonus=(G.dmgBonus||1)*1.25;G.units.filter(u=>u.side===0).forEach(u=>u.atk=Math.round(u.atk*1.25));toast('⚔️ 무기 강화!','gold');}},
  {id:'u_snipe', em:'🎯', name:'저격 강화',  desc:'저격 피해 +50%',       cost:160,
   fx:()=>{G.snipeDmgBonus=(G.snipeDmgBonus||1)*1.5;toast('🎯 저격 강화!','gold');}},
  {id:'u_shield',em:'🛡️', name:'장갑 강화',  desc:'아군 HP +25%',         cost:200,
   fx:()=>{G.units.filter(u=>u.side===0).forEach(u=>{u.maxHp=Math.round(u.maxHp*1.25);u.hp=Math.round(u.hp*1.25);});toast('🛡️ 장갑 강화!','good');}},
  {id:'u_cd',    em:'⚡', name:'스킬 가속',  desc:'스킬 쿨다운 -25%',    cost:140,
   fx:()=>{G.cdBonus=(G.cdBonus||1)*0.75;toast('⚡ 스킬 가속!','gold');}},
  {id:'u_pierce',em:'🔫', name:'관통탄',      desc:'저격 관통 +1 (최대3)', cost:220,repeatable:true,
   fx:()=>{G.pierceCount=Math.min((G.pierceCount||1)+1,3);
     document.getElementById('pierce-val').textContent='×'+G.pierceCount;
     toast('🔫 관통탄! 관통 +1','gold');}},
  {id:'u_turret',em:'🔰', name:'기지 터렛',   desc:'아군 기지에 자동 터렛', cost:300,repeatable:true,
   fx:()=>{G.turretLevel=(G.turretLevel||0)+1;toast('🔰 기지 터렛 Lv'+G.turretLevel+' 설치!','good');}},
  {id:'u_speed', em:'💨', name:'기동력 강화', desc:'아군 이동속도 +20%',   cost:170,
   fx:()=>{G.units.filter(u=>u.side===0).forEach(u=>u.spd*=1.2);G.spdBonus=(G.spdBonus||1)*1.2;toast('💨 기동력 강화!','good');}},
  {id:'u_multi', em:'🌀', name:'산탄 저격',   desc:'저격 시 근처 적 추가 피해', cost:250,
   fx:()=>{G.multiSnipe=true;toast('🌀 산탄 저격 활성화!','gold');}},
  {id:'u_regen', em:'💚', name:'기지 재생',   desc:'기지 HP 초당 2씩 회복', cost:180,
   fx:()=>{G.baseRegen=(G.baseRegen||0)+2;toast('💚 기지 재생 활성화!','good');}},
  {id:'u_crit',  em:'💥', name:'크리티컬',    desc:'저격 치명타율 +20%',   cost:190,repeatable:true,
   fx:()=>{G.critBonus=(G.critBonus||0)+0.2;toast('💥 크리티컬 강화!','gold');}},
];

// ════════════════════════════════════════════════
//  WEATHER SYSTEM
// ════════════════════════════════════════════════
const WEATHERS = [
  {id:'clear', name:'☀️ 맑음',   spdMult:1.0, visRange:1.0, rain:false, night:false},
  {id:'rain',  name:'🌧️ 폭우',   spdMult:0.8, visRange:0.85,rain:true,  night:false},
  {id:'fog',   name:'🌫️ 안개',   spdMult:0.9, visRange:0.65,rain:false, night:false},
  {id:'night', name:'🌙 야간',   spdMult:1.0, visRange:0.7, rain:false, night:true},
  {id:'storm', name:'⛈️ 폭풍',   spdMult:0.7, visRange:0.75,rain:true,  night:true},
];

// ════════════════════════════════════════════════
//  GLOBALS
// ════════════════════════════════════════════════
let G={};
let W=0, H=0, GROUND=0;
// FIX: these are recalculated on resize; initialize safely
let ALLY_BASE_X=70, ENEMY_BASE_X=700;
let shopBoughtItems=new Set();
let rainDrops=[];
let animFrameId=null;

// ── 3라인 시스템 ──
const LANES = [
  {id:0, name:'탑', em:'⬆️', yFrac:0.42},
  {id:1, name:'미드', em:'➡️', yFrac:0.62},
  {id:2, name:'바텀', em:'⬇️', yFrac:0.82},
];
let selectedLane = 1; // 기본: 미드

const canvas=document.getElementById('battlefield');
const ctx=canvas.getContext('2d');

// ════════════════════════════════════════════════
//  RESIZE — FIX: measure canvas actual rendered size reliably
// ════════════════════════════════════════════════
function resize(){
  // Read the rendered size from the layout
  const rect = canvas.getBoundingClientRect();
  W = Math.max(rect.width, 300);
  H = Math.max(rect.height, 200);
  canvas.width  = W;
  canvas.height = H;
  // GROUND은 미드 라인 기준값으로만 사용 (레인별 Y는 laneY()로 계산)
  GROUND = H * 0.62;
  ALLY_BASE_X  = 70;
  ENEMY_BASE_X = W - 70;
}

// 라인별 Y 좌표 반환
function laneY(laneId){ return H * LANES[laneId].yFrac; }

// ════════════════════════════════════════════════
//  START
// ════════════════════════════════════════════════
function startGame(diff){
  const dc=DIFF_CONFIG[diff];
  shopBoughtItems=new Set();
  rainDrops=Array.from({length:200},()=>({
    x:Math.random()*2000,y:Math.random()*600,
    spd:8+Math.random()*6,len:12+Math.random()*10
  }));

  // FIX: cancel any previous loop
  if(animFrameId) cancelAnimationFrame(animFrameId);

  G={
    running:true,diff,wave:1,
    resources:dc.startRes,
    allyBase:dc.baseHp,enemyBase:dc.baseHp,maxBase:dc.baseHp,
    // 3라인 기지 HP (각 라인의 타워)
    laneAllyHp:[dc.baseHp*0.5, dc.baseHp*0.5, dc.baseHp*0.5],
    laneEnemyHp:[dc.baseHp*0.5, dc.baseHp*0.5, dc.baseHp*0.5],
    laneMaxTowerHp: dc.baseHp*0.5,
    units:[],bullets:[],effects:[],particles:[],
    score:0,kills:0,snipes:0,headshots:0,combo:1,comboTimer:0,
    nextId:0,reloading:false,reloadTimer:0,reloadMax:80,
    botTimer:0,resTimer:0,waveTimer:0,frame:0,lastTime:performance.now(),
    abilities:[
      {id:0,cd:0,maxCd:ABILITY_DEFS[0].cd},
      {id:1,cd:0,maxCd:ABILITY_DEFS[1].cd},
      {id:2,cd:0,maxCd:ABILITY_DEFS[2].cd},
      {id:3,cd:0,maxCd:ABILITY_DEFS[3].cd},
      {id:4,cd:0,maxCd:ABILITY_DEFS[4].cd},
    ],
    trainCooldowns:[0,0,0,0,0,0,0,0,0],
    blitzEnd:-1,shieldEnd:-1,freezeEnd:-1,
    resBonus:1,dmgBonus:1,snipeDmgBonus:1,cdBonus:1,spdBonus:1,
    pierceCount:1,multiSnipe:false,critBonus:0,baseRegen:0,
    turretLevel:0,turretTimer:0,
    bossSpawned:false,
    weather:WEATHERS[0],weatherTimer:0,
    mouseX:0,mouseY:0,
    craters:[],
  };

  // Show game, hide menu
  document.getElementById('diff-select').style.display='none';
  const gEl=document.getElementById('game');
  gEl.style.display='flex';
  document.getElementById('result').style.display='none';
  document.getElementById('boss-alert').style.display='none';

  // Diff badge
  const dc2=DIFF_CONFIG[diff];
  const db=document.getElementById('diff-badge');
  db.textContent=dc2.name;
  db.style.cssText=`background:${dc2.bgCol};color:${dc2.col};border:1px solid ${dc2.bdCol};`;

  // FIX: Use multiple retries to get a valid canvas size after layout
  let attempts = 0;
  function tryStart(){
    resize();
    if(W < 100 && attempts < 10){
      attempts++;
      setTimeout(tryStart, 50);
      return;
    }
    // generate craters after we know W
    for(let i=0;i<5;i++)
      G.craters.push({x:150+Math.random()*(W-300),r:15+Math.random()*20});

    updateHUD();
    updateButtons();
    document.getElementById('scope').style.display='block';
    // FIX: DON'T hide cursor on the whole page — only show custom scope
    // canvas.style.cursor='none'; // removed - this was breaking clicks in some browsers
    canvas.style.cursor='crosshair';
    document.getElementById('pierce-val').textContent='×'+G.pierceCount;
    G.lastTime=performance.now();
    animFrameId=requestAnimationFrame(loop);
  }
  setTimeout(tryStart, 60);
}

function goMenu(){
  G.running=false;
  document.getElementById('result').style.display='none';
  document.getElementById('diff-select').style.display='flex';
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';
}

// ════════════════════════════════════════════════
//  MAIN LOOP — FIX: robust dt calc
// ════════════════════════════════════════════════
function loop(ts){
  if(!G.running){animFrameId=null;return;}
  const raw = ts - G.lastTime;
  const dt  = Math.min(raw / 16.667, 4); // cap at 4 frames to avoid spiral
  G.lastTime = ts;
  G.frame++;
  update(dt);
  render();
  animFrameId=requestAnimationFrame(loop);
}

// ════════════════════════════════════════════════
//  UPDATE
// ════════════════════════════════════════════════
function update(dt){
  const dc=DIFF_CONFIG[G.diff];

  // Weather
  G.weatherTimer+=dt;
  if(G.weatherTimer>1200){
    G.weatherTimer=0;
    const prev=G.weather.id;
    let next;
    do{ next=WEATHERS[Math.floor(Math.random()*WEATHERS.length)]; }while(next.id===prev);
    G.weather=next;
    document.getElementById('weather-badge').textContent=next.name;
    document.getElementById('night-overlay').style.background=
      next.night?'rgba(0,0,30,0.38)':'rgba(0,0,30,0)';
    toast('🌦️ 날씨 변화: '+next.name,'wave');
  }

  // Resources
  G.resTimer+=dt;
  const resInterval=60/(dc.resRate*(G.resBonus||1));
  if(G.resTimer>=resInterval){G.resTimer=0;G.resources=Math.min(G.resources+6,800);}

  // Base regen
  if(G.baseRegen>0) G.allyBase=Math.min(G.allyBase+G.baseRegen*dt/60,G.maxBase);

  // Wave timer
  G.waveTimer+=dt;
  if(G.waveTimer>=1800){
    G.waveTimer=0;G.wave++;
    G.maxBase+=300;
    G.allyBase=Math.min(G.allyBase+80,G.maxBase);
    G.enemyBase=Math.min(G.enemyBase+80,G.maxBase);
    document.getElementById('wave-badge').textContent='웨이브 '+G.wave;
    if(G.wave%dc.bossWave===0) spawnBossWave();
    else if(G.wave%dc.miniBossWave===0) spawnMiniBoss();
    else if(G.wave%7===0) spawnEventWave();
    else toast('🌊 웨이브 '+G.wave+'! 대비하라!','wave');
  }

  // Bot AI
  G.botTimer+=dt;
  // FIX: botDelay is in ms, convert to frames (60fps = 16.67ms/frame)
  const botDelayFrames = dc.botDelay / 16.667;
  if(G.botTimer>=botDelayFrames){G.botTimer=0;botSpawn();}

  const frozen=(G.frame<G.freezeEnd);

  // Training cooldowns
  G.trainCooldowns=G.trainCooldowns.map(c=>Math.max(0,c-dt));
  for(let i=0;i<9;i++){
    const pct=G.trainCooldowns[i]>0?1-G.trainCooldowns[i]/UNIT_DEFS[i].trainTime:1;
    const el=document.getElementById('cool'+i);
    if(el) el.style.width=(pct*100)+'%';
  }

  // Ability cooldowns
  G.abilities.forEach((a,i)=>{
    if(a.cd>0){
      a.cd=Math.max(0,a.cd-dt*(G.cdBonus||1));
      const el=document.getElementById('abil'+i);
      if(el) el.classList.toggle('cooldown',a.cd>0);
      const pct=1-a.cd/a.maxCd;
      const bar=document.getElementById('abar'+i);
      const lbl=document.getElementById('acool'+i);
      if(bar) bar.style.width=(pct*100)+'%';
      if(lbl) lbl.textContent=a.cd>0?Math.ceil(a.cd/60)+'s':['Q','E','R','W','T'][i];
    }
  });

  // Blitz end
  if(G.blitzEnd>0&&G.frame===G.blitzEnd){
    G.units.filter(u=>u.side===0&&u._blitzed).forEach(u=>{u.spd/=2;u._blitzed=false;});
    toast('⚡ 전격전 종료','');
  }

  // Combo decay
  if(G.comboTimer>0){G.comboTimer-=dt;if(G.comboTimer<=0){G.combo=1;document.getElementById('combo-val').textContent='×1';}}

  // Reload
  if(G.reloading){
    G.reloadTimer+=dt;
    const pct=G.reloadTimer/G.reloadMax;
    const rs=document.getElementById('reload-status');
    if(rs){rs.textContent='재장전 '+Math.round(pct*100)+'%';rs.style.color='var(--orange)';}
    if(G.reloadTimer>=G.reloadMax){
      G.reloading=false;G.reloadTimer=0;
      if(rs){rs.textContent='준비';rs.style.color='var(--green)';}
    }
  }

  // Turret
  if(G.turretLevel>0){
    G.turretTimer+=dt;
    const turretRate=60/(G.turretLevel*1.5);
    if(G.turretTimer>=turretRate){
      G.turretTimer=0;
      const enemies=G.units.filter(u=>u.side===1&&u.hp>0).sort((a,b)=>a.x-b.x);
      if(enemies.length>0){
        const t=enemies[0];
        const tdmg=Math.round(30*G.turretLevel*(G.dmgBonus||1));
        G.bullets.push({x:ALLY_BASE_X,y:GROUND-60,tx:t.x,ty:t.y-18,
          col:'#b26cf7',dmg:tdmg,targetId:t.uid,fromSide:0,spd:12,pierce:0,maxPierce:0});
      }
    }
  }

  updateUnits(dt,frozen);
  updateBullets(dt);
  updateEffects(dt);
  updateParticles(dt);

  if(G.enemyBase<=0) endGame(true);
  else if(G.allyBase<=0) endGame(false);

  updateHUD();
  updateButtons();
}

// ════════════════════════════════════════════════
//  UNITS
// ════════════════════════════════════════════════
function spawnUnit(defId,side,x,lane){\
  const def=UNIT_DEFS[defId];
  const laneId = (lane !== undefined) ? lane : 1; // 기본 미드
  const groundY = laneY(laneId);
  const ws=1+(G.wave-1)*0.13;
  const isBoss=def.isBoss||false;
  const isMiniBoss=def.isMiniBoss||false;
  const hpMult=isBoss?(1+G.diff*0.3):(isMiniBoss?(1+G.diff*0.2):1);
  const u={
    uid:G.nextId++,defId,side,x,y:groundY-2,lane:laneId,
    hp:Math.round(def.hp*ws*hpMult),
    maxHp:Math.round(def.hp*ws*hpMult),
    atk:Math.round(def.atk*ws*(side===0?(G.dmgBonus||1):1)),
    spd:def.spd*(side===0?(G.spdBonus||1):1)*G.weather.spdMult,
    baseSpd:def.spd*(side===0?(G.spdBonus||1):1),
    range:def.range*G.weather.visRange,
    ranged:def.ranged,cooldown:0,em:def.em,pri:def.pri,
    healer:def.healer||false,armored:def.armored||false,
    flamer:def.flamer||false,ninja:def.ninja||false,
    kamikaze:def.kamikaze||false,
    reward:def.reward,name:def.name,
    anim:Math.random()*Math.PI*2,isBoss,isMiniBoss,
  };
  G.units.push(u);
}

function spawnAlly(defId){
  if(defId>8) return;
  const def=UNIT_DEFS[defId];
  if(G.resources<def.cost){toast('💎 자원 부족!','bad');return;}
  if(G.trainCooldowns[defId]>0){toast('⏳ 훈련 중!','bad');return;}
  G.resources-=def.cost;
  G.trainCooldowns[defId]=def.trainTime;
  spawnUnit(defId,0,ALLY_BASE_X+55, selectedLane);
  toast(LANES[selectedLane].em+' '+LANES[selectedLane].name+' 라인 파견!','good');
  updateButtons();
}

function botSpawn(){
  const dc=DIFF_CONFIG[G.diff];
  const pool=dc.botPool.filter(id=>id!==14&&id!==15);
  // FIX: botRes calculation was wrong — scale with wave
  const botRes=60+G.wave*20*(dc.botResRate);
  const affor=pool.map(id=>UNIT_DEFS[id]).filter(d=>d.cost<=botRes);
  if(!affor.length) return;
  let chosen;
  if(G.diff>=2){
    affor.sort((a,b)=>b.cost-a.cost);
    chosen=affor[Math.floor(Math.random()*Math.min(2,affor.length))];
  } else {
    chosen=affor[Math.floor(Math.random()*affor.length)];
  }
  // 3라인에 랜덤 배치 (AI는 약한 라인 우선 공략)
  const botLane=pickBotLane();
  spawnUnit(chosen.id,1,ENEMY_BASE_X-55, botLane);
  if(G.diff===3&&Math.random()<0.4){
    const lane2=(botLane+1+Math.floor(Math.random()*2))%3;
    setTimeout(()=>{if(G.running)spawnUnit(chosen.id,1,ENEMY_BASE_X-55,lane2);},350);
  }
}

// AI가 공략할 라인 결정 (아군 타워 HP가 낮은 라인 우선)
function pickBotLane(){
  // 가중치: 아군 타워 HP가 낮을수록 더 많이 공격
  const weights=G.laneAllyHp.map(hp=>Math.max(1,G.laneMaxTowerHp-hp+50));
  const total=weights.reduce((a,b)=>a+b,0);
  let r=Math.random()*total;
  for(let i=0;i<3;i++){r-=weights[i];if(r<=0)return i;}
  return Math.floor(Math.random()*3);
}

function spawnBossWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="boss-alert-box">💀 보스 등장! 모든 라인 공략!</div>';
  setTimeout(()=>{ba.style.display='none';},2200);
  // 보스는 랜덤 라인에 등장, 미니언은 전 라인
  const bossLane=Math.floor(Math.random()*3);
  spawnUnit(14,1,ENEMY_BASE_X-60, bossLane);
  for(let i=0;i<3;i++) setTimeout(()=>{if(G.running)spawnUnit(10,1,ENEMY_BASE_X-80-i*30, i%3);},i*400);
  toast('💀 보스 웨이브! 전력을 다하라!','bad');
}

function spawnMiniBoss(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="miniboss-alert-box">😈 미니보스 출현!</div>';
  setTimeout(()=>{ba.style.display='none';},2000);
  const ml=Math.floor(Math.random()*3);
  spawnUnit(15,1,ENEMY_BASE_X-60, ml);
  for(let i=0;i<2;i++) setTimeout(()=>{if(G.running)spawnUnit(9,1,ENEMY_BASE_X-80-i*25,(ml+i)%3);},i*300);
  toast('😈 미니보스 출현! 조심해!','bad');
}

function spawnEventWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="event-alert-box">🎖️ 전 라인 아군 지원대 도착!</div>';
  setTimeout(()=>{ba.style.display='none';},2000);
  // 3라인 전체에 지원군 배치
  [0,1,2].forEach(lane=>{
    [0,5].forEach((id,i)=>setTimeout(()=>{if(G.running)spawnUnit(id,0,ALLY_BASE_X+55+i*15,lane);},lane*200+i*300));
  });
  G.resources=Math.min(G.resources+100,800);
  toast('🎖️ 전 라인 지원! 💎100 보너스!','good');
}

function updateUnits(dt,frozen){
  G.units.forEach(u=>{
    u.anim+=dt*0.12;
    if(u.hp<=0) return;
    if(frozen && u.side===1) return;

    u.spd=u.baseSpd*G.weather.spdMult*(u.side===0?(G.spdBonus||1):1);
    if(u._blitzed) u.spd=u.baseSpd*2;

    if(u.healer){
      const hurt=G.units.filter(o=>o.side===u.side&&o.lane===u.lane&&o.hp>0&&o.hp<o.maxHp&&Math.abs(u.x-o.x)<90);
      if(hurt.length>0){hurt[0].hp=Math.min(hurt[0].maxHp,hurt[0].hp+0.5*dt);return;}
    }

    if(u.kamikaze&&u.side===1){
      u.x-=u.spd*dt*1.5;
      if(u.x<=ALLY_BASE_X+40){
        const shield=G.frame<G.shieldEnd?0.3:1;
        G.allyBase-=u.atk*2*shield;
        G.laneAllyHp[u.lane]=Math.max(0,G.laneAllyHp[u.lane]-u.atk*3*shield);
        spawnDeath(u.x,u.y,false);
        u.hp=0; return;
      }
    }

    // 같은 라인의 적만 타겟
    const enemies=G.units.filter(o=>o.side!==u.side&&o.hp>0&&o.lane===u.lane);
    let target=null,minD=Infinity;
    enemies.forEach(e=>{const d=Math.abs(u.x-e.x);if(d<minD){minD=d;target=e;}});

    if(target&&minD<=u.range){
      u.cooldown-=dt;
      if(u.cooldown<=0){
        u.cooldown=28-G.diff*2;
        if(u.flamer){
          const inRange=G.units.filter(o=>o.side!==u.side&&o.hp>0&&o.lane===u.lane&&Math.abs(u.x-o.x)<u.range);
          inRange.forEach(e=>{
            e.hp-=u.atk*0.5;
            spawnHit(e.x,e.y,'#ff8c42',Math.round(u.atk*0.5));
            if(e.hp<=0) killUnit(e,u.side===0?0:1);
          });
        } else if(u.ranged){
          G.bullets.push({x:u.x,y:u.y-18,tx:target.x,ty:target.y-18,
            col:u.side===0?'#22d3ee':'#ff4560',dmg:u.atk,
            targetId:target.uid,fromSide:u.side,spd:8,pierce:0,maxPierce:0});
        } else {
          target.hp-=u.atk;
          spawnHit(target.x,target.y,u.side===0?'#22d3ee':'#ff4560',u.atk);
          if(target.hp<=0) killUnit(target,u.side===0?0:1);
        }
      }
    } else {
      const dir=u.side===0?1:-1;
      const blocked=G.units.some(o=>o.side!==u.side&&o.hp>0&&o.lane===u.lane&&Math.abs(u.x-o.x)<(u.ninja?20:28));
      if(!blocked) u.x+=dir*u.spd*dt;
      if(u.ninja&&blocked) u.x+=dir*u.spd*dt*2;
    }

    const shield=G.frame<G.shieldEnd?0.3:1;
    // 라인 타워 + 메인 기지 동시 피해
    if(u.side===0&&u.x>=ENEMY_BASE_X-32){
      G.enemyBase-=u.atk*0.07*dt;
      G.laneEnemyHp[u.lane]=Math.max(0,G.laneEnemyHp[u.lane]-u.atk*0.12*dt);
    }
    if(u.side===1&&u.x<=ALLY_BASE_X+32){
      G.allyBase-=u.atk*0.07*dt*shield;
      G.laneAllyHp[u.lane]=Math.max(0,G.laneAllyHp[u.lane]-u.atk*0.12*dt*shield);
    }
  });
  G.units=G.units.filter(u=>u.hp>0);
}

function killUnit(unit,killerSide){
  if(unit.hp<=0) return; // FIX: prevent double-kill
  G.score+=unit.reward*G.wave*(killerSide===0?G.combo:1);
  if(killerSide===0){G.kills++;addKillFeed(unit);}
  G.resources=Math.min(G.resources+Math.floor(unit.reward*0.35),800);
  spawnDeath(unit.x,unit.y,unit.isBoss||unit.isMiniBoss);
  if(unit.isBoss){toast('💀 보스 처치! 전설의 승리!','gold');spawnFireworks();}
  else if(unit.isMiniBoss){toast('😈 미니보스 처치!','gold');}
  unit.hp=0;
}

function updateBullets(dt){
  G.bullets.forEach(b=>{
    const dx=b.tx-b.x, dy=b.ty-b.y, d=Math.sqrt(dx*dx+dy*dy);
    if(d<b.spd*dt*2){
      const t=G.units.find(u=>u.uid===b.targetId&&u.hp>0);
      if(t){
        t.hp-=b.dmg;
        spawnHit(t.x,t.y,b.col,b.dmg);
        if(t.hp<=0) killUnit(t,b.fromSide===0?0:1);
        if(b.pierce<b.maxPierce){
          b.pierce++;
          const nextEnemies=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==b.targetId)
            .sort((a,c)=>Math.abs(a.x-(t.x+30))-Math.abs(c.x-(t.x+30)));
          if(nextEnemies.length>0){
            const nt=nextEnemies[0];
            b.tx=nt.x;b.ty=nt.y-18;b.targetId=nt.uid;
            b.x=t.x;b.y=t.y-18;
            return;
          }
        }
      }
      b.done=true;
    } else {
      b.x+=dx/d*b.spd*dt;
      b.y+=dy/d*b.spd*dt;
    }
  });
  G.bullets=G.bullets.filter(b=>!b.done);
}

function updateEffects(dt){
  G.effects.forEach(e=>{e.r+=dt*1.8;e.alpha-=dt*0.045;if(e.alpha<=0)e.done=true;});
  G.effects=G.effects.filter(e=>!e.done);
}

function updateParticles(dt){
  G.particles.forEach(p=>{p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=0.15*dt;p.life-=dt;});
  G.particles=G.particles.filter(p=>p.life>0);
}

function spawnHit(x,y,col,dmg){
  G.effects.push({x,y,r:3,col,alpha:0.9,type:'hit'});
  if(dmg>0){
    for(let i=0;i<3;i++)
      G.particles.push({x,y:y-15,vx:(Math.random()-.5)*2,vy:-Math.random()*2,col,life:15,size:2+Math.random()*2});
  }
}

function spawnDeath(x,y,big){
  const cnt=big?22:8;
  for(let i=0;i<cnt;i++){
    const ang=Math.random()*Math.PI*2,spd=1+Math.random()*3;
    G.particles.push({x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd-2,
      col:big?'#ffd700':'#ff4560',life:20+Math.random()*20,size:big?6:3});
    G.effects.push({x:x+(Math.random()-.5)*30,y:y+(Math.random()-.5)*30,
      r:2,col:big?'#ffd700':'#ff4560',alpha:0.8,type:'death'});
  }
}

// FIX: airstrikeBomb no longer takes G as param — uses global G
function airstrikeBomb(x,y){
  G.effects.push({x,y,r:5,col:'#ff8c42',alpha:1,type:'bomb'});
  G.units.filter(u=>u.side===1&&Math.abs(u.x-x)<60).forEach(u=>{
    const dmg=Math.round((100+G.wave*20)*(G.snipeDmgBonus||1));
    u.hp-=dmg;spawnHit(u.x,u.y,'#ff8c42',dmg);if(u.hp<=0)killUnit(u,0);
  });
  G.enemyBase-=30;
  for(let i=0;i<10;i++)
    G.particles.push({x:x+(Math.random()-.5)*40,y,vx:(Math.random()-.5)*4,vy:-Math.random()*5,col:'#ff8c42',life:25+Math.random()*15,size:4});
}

// ════════════════════════════════════════════════
//  SNIPER — HEADSHOT SYSTEM
// ════════════════════════════════════════════════
function tryShoot(mx,my){
  if(!G.running) return;
  if(G.reloading){toast('🔫 재장전 중!','bad');return;}

  const HITBOX_FULL=42;
  const HEADBOX=18;

  let hit=null,bestPri=-1,isHeadshot=false;
  G.units.forEach(u=>{
    if(u.side!==1||u.hp<=0) return;
    const uy=u.y-18;
    const headY=u.y-30;
    const bodyDist=Math.sqrt((mx-u.x)**2+(my-uy)**2);
    const headDist=Math.sqrt((mx-u.x)**2+(my-headY)**2);
    if(bodyDist<HITBOX_FULL&&u.pri>=bestPri){
      bestPri=u.pri; hit=u;
      isHeadshot=(headDist<HEADBOX);
    }
  });

  const isCrit=Math.random()<(G.critBonus||0);
  const baseDmg=(130+G.diff*35)*(G.snipeDmgBonus||1)*(G.weather.id==='night'?0.85:1);

  if(hit){
    let dmg=Math.round(baseDmg*(hit.isBoss?0.5:1)*G.combo);
    let dmgLabel='';
    if(isHeadshot){dmg=Math.round(dmg*1.6);dmgLabel+=' 🎯헤드샷!';}
    if(isCrit){dmg=Math.round(dmg*1.4);dmgLabel+=' 💥크리티컬!';}

    const pierceMax=G.pierceCount-1;
    G.bullets.push({x:mx,y:my,tx:hit.x,ty:hit.y-18,
      col:isHeadshot?'#ffd700':'#ff4560',dmg,targetId:hit.uid,
      fromSide:0,spd:28,pierce:0,maxPierce:pierceMax});

    if(G.multiSnipe){
      const nearby=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==hit.uid&&Math.abs(u.x-hit.x)<70);
      nearby.slice(0,2).forEach(u=>{
        const sdmg=Math.round(dmg*0.4);
        setTimeout(()=>{if(u.hp>0){u.hp-=sdmg;spawnHit(u.x,u.y,'#ff8c42',sdmg);if(u.hp<=0)killUnit(u,0);}},80);
      });
    }

    G.snipes++;
    G.score+=Math.round(90*G.wave*G.combo*(isHeadshot?2:1));
    G.combo=Math.min(G.combo+1,10);G.comboTimer=180;
    document.getElementById('combo-val').textContent='×'+G.combo;

    if(isHeadshot){
      G.headshots++;
      const fl=document.getElementById('hs-flash');
      fl.style.background='rgba(255,215,0,0.12)';
      setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},150);
      const w=document.getElementById('twrap');
      const d=document.createElement('div');d.className='hs-toast';
      d.textContent='🎯 헤드샷! +×1.6 피해'+dmgLabel;
      w.insertBefore(d,w.firstChild);setTimeout(()=>d.remove(),2200);
    } else {
      toast('🎯 저격! '+hit.name+' -'+dmg+'HP ×'+G.combo+'콤보'+dmgLabel,'gold');
    }

    G.effects.push({x:hit.x,y:hit.y,r:6,col:isHeadshot?'#ffd700':'#ff4560',alpha:0.9,type:'snipe'});
    G.reloading=true;G.reloadTimer=0;
    G.reloadMax=Math.max(35,80-G.combo*4);

  } else if(mx>ENEMY_BASE_X-90){
    const dmg=Math.round((40+G.diff*12)*(G.snipeDmgBonus||1));
    G.enemyBase-=dmg;
    toast('💥 기지 직격! -'+dmg,'good');
    G.effects.push({x:ENEMY_BASE_X,y:GROUND-40,r:10,col:'#ff8c42',alpha:0.9,type:'snipe'});
    G.reloading=true;G.reloadTimer=0;G.reloadMax=70;
    G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';
  } else {
    G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';
  }
}

// ════════════════════════════════════════════════
//  ABILITIES
// ════════════════════════════════════════════════
function useAbility(i){
  if(!G.running) return;
  const a=G.abilities[i];
  if(a.cd>0){toast('쿨다운 중!','bad');return;}
  ABILITY_DEFS[i].fx();
  a.cd=a.maxCd;
}

// ════════════════════════════════════════════════
//  SHOP
// ════════════════════════════════════════════════
function openShop(){
  document.getElementById('shop-res').textContent=Math.floor(G.resources);
  const grid=document.getElementById('shop-grid');
  grid.innerHTML='';
  SHOP_ITEMS.forEach(item=>{
    const bought=shopBoughtItems.has(item.id)&&!item.repeatable;
    const div=document.createElement('div');
    div.className='shop-item'+(bought?' bought':'');
    div.innerHTML=`<span class="sem">${item.em}</span><span class="sname">${item.name}</span>
      <span class="sdesc">${item.desc}</span>
      <span class="scost">${bought?'구매완료':'💎'+item.cost}</span>`;
    if(!bought) div.onclick=()=>buyShopItem(item);
    grid.appendChild(div);
  });
  document.getElementById('shop-modal').style.display='flex';
}
function closeShop(){document.getElementById('shop-modal').style.display='none';}
function buyShopItem(item){
  if(G.resources<item.cost){toast('💎 자원 부족!','bad');return;}
  G.resources-=item.cost;
  item.fx();
  if(!item.repeatable) shopBoughtItems.add(item.id);
  openShop();updateHUD();
}

// ════════════════════════════════════════════════
//  RENDER
// ════════════════════════════════════════════════
function render(){
  if(W===0||H===0) return;
  ctx.clearRect(0,0,W,H);

  const isNight=G.weather.night;
  const sky=ctx.createLinearGradient(0,0,0,GROUND);
  if(isNight){sky.addColorStop(0,'#010510');sky.addColorStop(1,'#0a1628');}
  else if(G.weather.id==='fog'){sky.addColorStop(0,'#1a2035');sky.addColorStop(1,'#2a3555');}
  else{sky.addColorStop(0,'#060a18');sky.addColorStop(1,'#152035');}
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,GROUND);

  // Stars
  if(isNight||G.weather.id==='fog'){
    ctx.fillStyle='rgba(255,255,255,0.75)';
    for(let i=0;i<80;i++){
      const sx=(i*137.5+G.frame*0.01)%W, sy=(i*97.3)%(GROUND*0.8);
      const sz=0.6+Math.sin(G.frame*0.06+i)*0.4;
      ctx.beginPath();ctx.arc(sx,sy,sz,0,Math.PI*2);ctx.fill();
    }
  } else {
    ctx.fillStyle='rgba(255,255,255,0.4)';
    for(let i=0;i<40;i++){
      const sx=(i*137.5+G.frame*0.015)%W, sy=(i*97.3)%(GROUND*0.85);
      ctx.beginPath();ctx.arc(sx,sy,0.5+Math.sin(G.frame*0.05+i)*0.25,0,Math.PI*2);ctx.fill();
    }
  }

  // Sun/Moon
  if(isNight){
    ctx.shadowBlur=30;ctx.shadowColor='rgba(200,220,255,0.5)';
    ctx.fillStyle='rgba(220,230,255,0.92)';
    ctx.beginPath();ctx.arc(W*0.8,GROUND*0.18,22,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  } else {
    ctx.shadowBlur=40;ctx.shadowColor='rgba(255,220,100,0.4)';
    ctx.fillStyle='rgba(255,220,80,0.85)';
    ctx.beginPath();ctx.arc(W*0.75,GROUND*0.15,18,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  }

  drawMountains();

  // Ground
  const grd=ctx.createLinearGradient(0,GROUND,0,H);
  grd.addColorStop(0,isNight?'#182508':'#253510');
  grd.addColorStop(0.4,isNight?'#0e1804':'#172209');
  grd.addColorStop(1,'#0c1505');
  ctx.fillStyle=grd;ctx.fillRect(0,GROUND,W,H-GROUND);
  ctx.strokeStyle='rgba(80,130,35,0.5)';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(0,GROUND);ctx.lineTo(W,GROUND);ctx.stroke();

  for(let i=0;i<W;i+=25){
    const h=3+Math.sin(i*0.3)*2;
    ctx.strokeStyle='rgba(80,140,40,0.3)';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(i,GROUND);ctx.lineTo(i-3,GROUND-h);ctx.stroke();
    ctx.beginPath();ctx.moveTo(i,GROUND);ctx.lineTo(i+3,GROUND-h-1);ctx.stroke();
  }

  G.craters.forEach(cr=>{
    ctx.fillStyle='rgba(0,0,0,0.35)';
    ctx.beginPath();ctx.ellipse(cr.x,GROUND+cr.r*0.3,cr.r,cr.r*0.4,0,0,Math.PI*2);ctx.fill();
  });

  // Rain
  if(G.weather.rain){
    ctx.strokeStyle='rgba(150,180,255,0.3)';ctx.lineWidth=1.2;
    rainDrops.forEach(d=>{
      d.y+=d.spd;d.x+=1.5;
      if(d.y>H){d.y=-10;d.x=Math.random()*W;}
      ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x-3,d.y+d.len);ctx.stroke();
    });
  }

  // Fog
  if(G.weather.id==='fog'||G.weather.id==='storm'){
    const fogG=ctx.createLinearGradient(0,0,W,0);
    fogG.addColorStop(0,'rgba(180,200,220,0.08)');
    fogG.addColorStop(0.3+Math.sin(G.frame*0.005)*0.1,'rgba(180,200,220,0.18)');
    fogG.addColorStop(1,'rgba(180,200,220,0.06)');
    ctx.fillStyle=fogG;ctx.fillRect(0,0,W,GROUND);
  }

  // Freeze
  if(G.freezeEnd>0&&G.frame<G.freezeEnd){
    const elapsed=G.frame-(G.freezeEnd-240);
    const fPct=Math.max(0,1-elapsed/240);
    ctx.fillStyle='rgba(100,180,255,'+(0.08*fPct)+')';
    ctx.fillRect(0,0,W,H);
  }

  // Shield glow
  if(G.shieldEnd>0&&G.frame<G.shieldEnd){
    const pulse=0.4+Math.sin(G.frame*0.15)*0.3;
    ctx.shadowBlur=30;ctx.shadowColor='rgba(34,211,238,'+pulse+')';
    ctx.strokeStyle='rgba(34,211,238,'+pulse+')';ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(ALLY_BASE_X,GROUND-45,55,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;
  }

  // ── 3라인 구분선 및 라인 레이블 ──
  LANES.forEach((lane,li)=>{
    const ly=laneY(li);
    const laneColors=['#b26cf7','#22d3ee','#10d96e'];
    const lc=laneColors[li];
    // 라인 구분 배경 띠
    const bandH=H/3;
    const bandY=li===0?0:(li===1?H*0.33:H*0.66);
    ctx.fillStyle=li===selectedLane?'rgba(255,255,255,0.025)':'rgba(0,0,0,0)';
    ctx.fillRect(0,bandY,W,bandH);
    // 라인 레인 구분선
    if(li>0){
      ctx.strokeStyle='rgba(255,255,255,0.08)';ctx.lineWidth=1;ctx.setLineDash([6,6]);
      ctx.beginPath();ctx.moveTo(0,bandY);ctx.lineTo(W,bandY);ctx.stroke();
      ctx.setLineDash([]);
    }
    // 지면 선
    ctx.strokeStyle=li===selectedLane?lc+'88':'rgba(80,130,35,0.3)';ctx.lineWidth=li===selectedLane?2:1;
    ctx.beginPath();ctx.moveTo(0,ly);ctx.lineTo(W,ly);ctx.stroke();
    // 라인 레이블
    const lbl=lane.name+(li===selectedLane?' ◀':' ');
    ctx.fillStyle=li===selectedLane?lc:'rgba(255,255,255,0.3)';
    ctx.font=`bold ${li===selectedLane?13:11}px "Noto Sans KR"`;
    ctx.textAlign='center';
    ctx.fillText(lbl,W/2,ly-6);
    ctx.textAlign='left';
    // 라인 타워 HP 바 (아군)
    const allyTowerPct=G.laneAllyHp[li]/G.laneMaxTowerHp;
    const enemyTowerPct=G.laneEnemyHp[li]/G.laneMaxTowerHp;
    const barW=60,barH=5,barY=ly-22;
    // 아군 타워 HP
    ctx.fillStyle='rgba(0,0,0,0.4)';ctx.fillRect(ALLY_BASE_X+5,barY,barW,barH);
    ctx.fillStyle=allyTowerPct>0.5?'#10d96e':allyTowerPct>0.25?'#ffd700':'#ff4560';
    ctx.fillRect(ALLY_BASE_X+5,barY,barW*allyTowerPct,barH);
    // 적 타워 HP
    ctx.fillStyle='rgba(0,0,0,0.4)';ctx.fillRect(ENEMY_BASE_X-65,barY,barW,barH);
    ctx.fillStyle=enemyTowerPct>0.5?'#ff4560':enemyTowerPct>0.25?'#ffd700':'#10d96e';
    ctx.fillRect(ENEMY_BASE_X-65,barY,barW*enemyTowerPct,barH);
  });

  // 메인 기지 그리기
  drawBase(ALLY_BASE_X,'🏰','#10d96e',G.allyBase/G.maxBase,true);
  drawBase(ENEMY_BASE_X,'🏯','#ff4560',G.enemyBase/G.maxBase,false);

  G.units.sort((a,b)=>a.y-b.y).forEach(u=>{if(u.hp>0)drawUnit(u);});

  // Bullets
  G.bullets.forEach(b=>{
    ctx.shadowBlur=8;ctx.shadowColor=b.col;
    ctx.fillStyle=b.col;
    const bsize=b.col==='#ffd700'?5.5:b.col==='#b26cf7'?4:3.5;
    ctx.beginPath();ctx.arc(b.x,b.y,bsize,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  });

  // Effects
  G.effects.forEach(e=>{
    ctx.globalAlpha=Math.max(0,e.alpha);
    if(e.type==='bomb'){
      ctx.shadowBlur=30;ctx.shadowColor='#ff8c42';
      ctx.fillStyle='rgba(255,140,66,'+e.alpha+')';
      ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;
    } else {
      ctx.strokeStyle=e.col;
      ctx.lineWidth=e.type==='snipe'?3.5:e.type==='death'?1.5:1.8;
      ctx.shadowBlur=e.type==='snipe'?20:0;ctx.shadowColor=e.col;
      ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.stroke();
      ctx.shadowBlur=0;
    }
    ctx.globalAlpha=1;
  });

  G.particles.forEach(p=>{
    ctx.globalAlpha=Math.min(1,p.life/10);
    ctx.fillStyle=p.col;
    ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();
    ctx.globalAlpha=1;
  });

  // Vignette (scope effect)
  if(!G.reloading&&G.running&&G.mouseX>0){
    const vg=ctx.createRadialGradient(G.mouseX,G.mouseY,55,G.mouseX,G.mouseY,Math.max(W,H)*0.72);
    vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,0.42)');
    ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  }

  // Headshot zone hint
  if(!G.reloading&&G.running){
    const hovered=G.units.find(u=>u.side===1&&u.hp>0&&Math.sqrt((G.mouseX-u.x)**2+(G.mouseY-(u.y-18))**2)<42);
    if(hovered){
      ctx.strokeStyle='rgba(255,215,0,0.4)';ctx.lineWidth=1.5;ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.arc(hovered.x,hovered.y-30,18,0,Math.PI*2);ctx.stroke();
      ctx.setLineDash([]);
    }
  }
}

function drawMountains(){
  ctx.fillStyle='rgba(10,18,38,0.7)';
  ctx.beginPath();ctx.moveTo(0,GROUND);
  for(let x=0;x<=W;x+=80) ctx.lineTo(x,GROUND-50-Math.sin(x*0.01)*35-Math.sin(x*0.025)*20);
  ctx.lineTo(W,GROUND);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(12,22,44,0.5)';
  ctx.beginPath();ctx.moveTo(0,GROUND);
  for(let x=0;x<=W;x+=55) ctx.lineTo(x,GROUND-25-Math.sin(x*0.018+1)*22-Math.sin(x*0.04)*12);
  ctx.lineTo(W,GROUND);ctx.closePath();ctx.fill();
}

function drawBase(x,em,col,hpPct,isAlly){
  const bw=64,bh=90;
  const bx=x<W/2?x-bw/2+12:x-bw/2-12, by=GROUND-bh;
  ctx.shadowBlur=20;ctx.shadowColor=col;
  ctx.fillStyle='rgba(15,25,48,0.92)';ctx.strokeStyle=col;ctx.lineWidth=2.2;
  rr(ctx,bx,by,bw,bh,7);ctx.fill();ctx.stroke();ctx.shadowBlur=0;
  const hbw=bw-10;
  ctx.fillStyle='rgba(0,0,0,0.55)';rr(ctx,bx+5,by+7,hbw,9,4);ctx.fill();
  const hcol=hpPct>0.5?col:hpPct>0.25?'#ffd700':'#ff4560';
  ctx.fillStyle=hcol;rr(ctx,bx+5,by+7,Math.max(0,hbw*hpPct),9,4);ctx.fill();
  ctx.fillStyle=col;
  for(let i=0;i<4;i++) ctx.fillRect(bx+i*(bw/4)+3,by-6,10,8);
  ctx.font='26px sans-serif';ctx.textAlign='center';ctx.fillText(em,bx+bw/2,by+bh-14);
  if(isAlly&&G.turretLevel>0){
    ctx.fillStyle='#b26cf7';ctx.shadowBlur=10;ctx.shadowColor='#b26cf7';
    ctx.fillRect(bx+bw/2-4,by-20,8,14);
    ctx.fillRect(bx+bw/2-2,by-26,4,8);
    ctx.shadowBlur=0;
    ctx.font='bold 9px sans-serif';ctx.fillStyle='#b26cf7';ctx.textAlign='center';
    ctx.fillText('Lv'+G.turretLevel,bx+bw/2,by-28);
  }
  if(hpPct<0.35){
    ctx.strokeStyle='rgba(255,100,50,0.55)';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(bx+14,by+18);ctx.lineTo(bx+22,by+52);ctx.lineTo(bx+18,by+72);ctx.stroke();
  }
  ctx.font='bold 9px sans-serif';ctx.fillStyle='rgba(255,255,255,0.6)';ctx.textAlign='center';
  ctx.fillText(Math.round(Math.max(0,x<W/2?G.allyBase:G.enemyBase)),bx+bw/2,by+bh+12);
}

function drawUnit(u){
  const x=u.x, y=u.y;
  const col=u.side===0?'#22d3ee':'#ff4560';
  const bounce=Math.sin(u.anim)*2.2;
  const scale=u.isBoss?1.7:u.isMiniBoss?1.35:1;
  const frozen=(G.freezeEnd>0&&G.frame<G.freezeEnd&&u.side===1);

  ctx.fillStyle='rgba(0,0,0,0.25)';
  ctx.beginPath();ctx.ellipse(x,y+2,13*scale,4*scale,0,0,Math.PI*2);ctx.fill();

  const r=14*scale;
  ctx.fillStyle=frozen?'rgba(30,60,120,0.9)':u.side===0?'rgba(0,45,75,0.88)':'rgba(75,0,20,0.88)';
  ctx.strokeStyle=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'#4dacf7':col;
  ctx.lineWidth=u.isBoss?2.5:u.isMiniBoss?2:1.8;
  ctx.shadowBlur=u.isBoss?18:u.isMiniBoss?12:7;
  ctx.shadowColor=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'rgba(100,180,255,0.8)':col;
  ctx.beginPath();ctx.arc(x,y-r+bounce,r,0,Math.PI*2);ctx.fill();ctx.stroke();
  ctx.shadowBlur=0;

  ctx.font=(u.isBoss?'22':u.isMiniBoss?'18':'14')+'px sans-serif';ctx.textAlign='center';
  ctx.fillText(u.em,x,y-r+bounce+5);

  if(u.isBoss){ctx.font='bold 10px "Noto Sans KR"';ctx.fillStyle='#ffd700';ctx.fillText('💀 BOSS',x,y-r*2+bounce-4);}
  if(u.isMiniBoss){ctx.font='bold 9px "Noto Sans KR"';ctx.fillStyle='#ff8c42';ctx.fillText('😈 MINI',x,y-r*2+bounce-4);}

  if(frozen){
    ctx.strokeStyle='rgba(100,220,255,0.5)';ctx.lineWidth=1;
    for(let i=0;i<4;i++){
      const ang=(i/4)*Math.PI*2;
      ctx.beginPath();ctx.moveTo(x,y-r+bounce);
      ctx.lineTo(x+Math.cos(ang)*(r+6),y-r+bounce+Math.sin(ang)*(r+6));ctx.stroke();
    }
  }

  const pct=u.hp/u.maxHp;
  const bw2=u.isBoss?54:u.isMiniBoss?38:28;
  ctx.fillStyle='rgba(0,0,0,0.5)';rr(ctx,x-bw2/2,y-r*2+bounce-2,bw2,5,2);ctx.fill();
  ctx.fillStyle=pct>0.5?'#10d96e':pct>0.25?'#ffd700':'#ff4560';
  rr(ctx,x-bw2/2,y-r*2+bounce-2,Math.max(0,bw2*pct),5,2);ctx.fill();
}

function rr(ctx,x,y,w,h,r){
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);
  ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
}

// ════════════════════════════════════════════════
//  HUD / BUTTONS
// ════════════════════════════════════════════════
function updateHUD(){
  if(!G.running&&!document.getElementById('result').style.display) return;
  const ah=Math.max(0,G.allyBase), eh=Math.max(0,G.enemyBase);
  document.getElementById('ally-hp-val').textContent=Math.round(ah);
  document.getElementById('enemy-hp-val').textContent=Math.round(eh);
  document.getElementById('ally-hp-bar').style.width=(ah/G.maxBase*100)+'%';
  document.getElementById('enemy-hp-bar').style.width=(eh/G.maxBase*100)+'%';
  document.getElementById('res-val').textContent=Math.floor(G.resources);
  document.getElementById('score-val').textContent=G.score.toLocaleString();
  document.getElementById('kills-val').textContent=G.kills;
}

function updateButtons(){
  for(let i=0;i<9;i++){
    const btn=document.getElementById('btn'+i);
    if(!btn) continue;
    const cost=UNIT_DEFS[i].cost;
    btn.disabled=!G.running||G.resources<cost||G.trainCooldowns[i]>0;
  }
}

// ════════════════════════════════════════════════
//  KILL FEED
// ════════════════════════════════════════════════
function addKillFeed(unit){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kf-item';
  d.textContent='🎯 '+unit.em+' '+unit.name+' 처치'+(unit.isBoss?' 🏆':unit.isMiniBoss?' 👑':'');
  d.style.borderColor=unit.isBoss?'rgba(255,215,0,.6)':unit.isMiniBoss?'rgba(255,140,66,.5)':'rgba(255,69,96,.3)';
  d.style.color=unit.isBoss?'#ffd700':unit.isMiniBoss?'#ff8c42':'var(--text)';
  kf.insertBefore(d,kf.firstChild);
  setTimeout(()=>d.remove(),3000);
  while(kf.children.length>5) kf.removeChild(kf.lastChild);
}

// ════════════════════════════════════════════════
//  GAME END
// ════════════════════════════════════════════════
function endGame(win){
  if(!G.running) return;
  G.running=false;
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';

  const maxScore=G.wave*1000*(G.diff+1);
  const ratio=G.score/Math.max(maxScore,1);
  const grade=win?(ratio>0.8?'S':ratio>0.6?'A':ratio>0.4?'B':'C'):'D';
  const gradeCol={S:'#ffd700',A:'#10d96e',B:'#4dabf7',C:'#ff8c42',D:'#ff4560'}[grade];

  const rs=document.getElementById('result');
  rs.style.display='flex';
  document.getElementById('res-grade').textContent=grade;
  document.getElementById('res-grade').style.color=gradeCol;
  document.getElementById('res-title').textContent=win?'🏆 승리!':'💀 패배...';
  document.getElementById('res-title').style.color=win?'#10d96e':'#ff4560';
  document.getElementById('res-subtitle').textContent=
    DIFF_CONFIG[G.diff].name+' 난이도 · 웨이브 '+G.wave+' · 등급 '+grade+' · 헤드샷 '+G.headshots+'회';
  document.getElementById('st-score').textContent=G.score.toLocaleString();
  document.getElementById('st-kills').textContent=G.kills;
  document.getElementById('st-wave').textContent=G.wave;
  document.getElementById('st-snipes').textContent=G.snipes;

  if(win) spawnFireworks();

  try{
    window.parent.postMessage({
      type:'sniper_result',
      score:G.score,kills:G.kills,wave:G.wave,snipes:G.snipes,win:win?1:0,diff:G.diff,
    },'*');
  }catch(e){}
}

// ════════════════════════════════════════════════
//  FIREWORKS
// ════════════════════════════════════════════════
function spawnFireworks(){
  const bg=document.getElementById('fw');
  const cols=['#ffd700','#ff4560','#4dabf7','#10d96e','#b26cf7','#22d3ee'];
  for(let f=0;f<12;f++) setTimeout(()=>{
    const x=10+Math.random()*80, y=5+Math.random()*55;
    const col=cols[Math.floor(Math.random()*cols.length)];
    for(let i=0;i<28;i++){
      const p=document.createElement('div');
      const ang=(i/28)*Math.PI*2, dist=55+Math.random()*110, dur=0.55+Math.random()*0.65;
      p.style.cssText='position:absolute;left:'+x+'%;top:'+y+'%;width:5px;height:5px;border-radius:50%;'
        +'background:'+col+';animation:fwp '+dur+'s ease-out forwards;'
        +'--dx:'+Math.cos(ang)*dist+'px;--dy:'+Math.sin(ang)*dist+'px;';
      bg.appendChild(p);
      setTimeout(()=>p.remove(),(dur+0.1)*1000);
    }
  },f*350);
}

// ════════════════════════════════════════════════
//  TOAST
// ════════════════════════════════════════════════
function toast(txt,type){
  const w=document.getElementById('twrap');
  const d=document.createElement('div');d.className='toast';
  const colors={good:'rgba(16,217,110,.4)',bad:'rgba(255,69,96,.4)',gold:'rgba(255,215,0,.4)',wave:'rgba(178,108,247,.4)'};
  d.style.borderColor=colors[type]||'rgba(255,255,255,.1)';
  d.textContent=txt;
  w.insertBefore(d,w.firstChild);
  setTimeout(()=>d.remove(),2800);
  while(w.children.length>5) w.removeChild(w.lastChild);
}

// ════════════════════════════════════════════════
//  EVENTS
// ════════════════════════════════════════════════
// FIX: track mouse on document, offset to canvas coords for gameplay
document.addEventListener('mousemove',e=>{
  // Update scope position
  const sc=document.getElementById('scope');
  sc.style.left=e.clientX+'px';
  sc.style.top=e.clientY+'px';

  // Update game mouse coords relative to canvas
  if(G.running){
    const rect=canvas.getBoundingClientRect();
    G.mouseX=e.clientX-rect.left;
    G.mouseY=e.clientY-rect.top;
  }

  // Scope color based on reload state
  const col=G.reloading?'rgba(120,120,120,0.6)':'rgba(255,69,96,0.9)';
  sc.querySelectorAll('circle[stroke],line').forEach(el=>{
    if(el.getAttribute('stroke')) el.setAttribute('stroke',col);
  });
});

// FIX: listen on canvas for clicks, properly subtract canvas offset
canvas.addEventListener('click',e=>{
  if(!G.running) return;
  const rect=canvas.getBoundingClientRect();
  tryShoot(e.clientX-rect.left, e.clientY-rect.top);
});

document.addEventListener('keydown',e=>{
  if(!G.running) return;
  // Prevent default for game keys to stop page scroll
  if(['1','2','3','4','5','6','7','8','9','q','e','r','w','t','s'].includes(e.key.toLowerCase()))
    e.preventDefault();
  const keys={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8};
  if(keys[e.key]!==undefined){spawnAlly(parseInt(e.key)-1);return;}
  if(e.key.toLowerCase()==='q') useAbility(0);
  if(e.key.toLowerCase()==='e') useAbility(1);
  if(e.key.toLowerCase()==='r') useAbility(2);
  if(e.key.toLowerCase()==='w') useAbility(3);
  if(e.key.toLowerCase()==='t') useAbility(4);
  if(e.key.toLowerCase()==='s') openShop();
});

// DIFF SELECT
let selDiff=0;
document.querySelectorAll('.diff-card').forEach(card=>{
  card.addEventListener('click',()=>{
    document.querySelectorAll('.diff-card').forEach(c=>c.classList.remove('sel'));
    card.classList.add('sel');
    selDiff=parseInt(card.dataset.d);
  });
});
document.getElementById('start-btn').addEventListener('click',()=>{
  startGame(selDiff);
});

// FIX: handle resize properly
window.addEventListener('resize',()=>{
  if(G.running){
    resize();
    // Regenerate craters for new width
    G.craters=[];
    for(let i=0;i<5;i++) G.craters.push({x:150+Math.random()*(W-300),r:15+Math.random()*20});
  }
});
</script>
</body>
</html>"""


def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import (
        load_db, save_db, load_leaderboard, update_leaderboard,
        format_leaderboard_score,
    )
    from utils.config import USERS_FILE

    qp = st.query_params
    GAME_ID = "sniper"

    # ── 결과 처리 ──────────────────────────────────────────
    if qp.get('sniper_score'):
        try:
            uid     = st.session_state.get('logged_in_user', '')
            s_score = int(qp.get('sniper_score', 0))
            s_kills = int(qp.get('sniper_kills', 0))
            s_wave  = int(qp.get('sniper_wave', 1))
            s_win   = qp.get('sniper_win', '0') == '1'
            s_diff  = int(qp.get('sniper_diff', 0))

            if uid and s_score > 0:
                _users = load_db(USERS_FILE, {})
                if uid in _users:
                    gr = _users[uid].setdefault('game_records', {})
                    sn = gr.setdefault('sniper', {'score': 0, 'kills': 0, 'wave': 1})
                    changed = False
                    if s_score > sn.get('score', 0):
                        sn['score'] = s_score
                        sn['kills'] = s_kills
                        sn['wave']  = s_wave
                        changed = True
                        st.toast(f"🎯 저격전 최고점수 갱신! {s_score:,}점", icon="🏆")
                    if changed:
                        gr['sniper'] = sn
                        _users[uid]['game_records'] = gr
                        save_db(USERS_FILE, _users)
                        st.session_state.game_records = gr
                        sync_user_data()

                user_name = _users.get(uid, {}).get('nickname', uid) if uid else uid
                if update_leaderboard(GAME_ID, user_name, s_score):
                    st.session_state['sniper_lb_new'] = True
                    st.toast(f"👑 전국 1위! 라인 배틀 {s_score:,}점", icon="🏆")

        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    # ── 전국 리더보드 표시 ──────────────────────────────────
    lb = load_leaderboard()
    rec = lb.get(GAME_ID, {})
    if rec:
        score_fmt = format_leaderboard_score(GAME_ID, rec.get('top_score', 0))
        st.markdown(f"""
        <div style='background:linear-gradient(90deg,rgba(255,140,66,.12),rgba(0,0,0,0));
          border:1px solid rgba(255,140,66,.35);border-radius:10px;padding:8px 18px;
          margin-bottom:10px;font-family:"Orbitron",sans-serif;font-size:.82rem;'>
          👑 전국 1위: <b style="color:#ffd700;">{rec.get('top_user','?')}</b>
          &nbsp;|&nbsp; <span style="color:#22d3ee;">{score_fmt}</span>
          &nbsp;|&nbsp; <span style="color:#7a8fb5;">{rec.get('date','')}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
    .block-container{padding:0!important;max-width:100%!important;}
    iframe{border:none!important;}
    </style>
    """, unsafe_allow_html=True)

    # postMessage listener
    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'sniper_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('sniper_score',  e.data.score);
        url.searchParams.set('sniper_kills',  e.data.kills);
        url.searchParams.set('sniper_wave',   e.data.wave);
        url.searchParams.set('sniper_win',    e.data.win);
        url.searchParams.set('sniper_diff',   e.data.diff);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)

    # FIX: increase height to 860 to prevent UI clipping
    components.html(GAME_HTML, height=860, scrolling=False)
