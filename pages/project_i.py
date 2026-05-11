import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>전장 저격전 v4</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Black+Han+Sans&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#05080f;--gold:#ffd700;--green:#10d96e;--red:#ff4560;
  --blue:#4dabf7;--cyan:#22d3ee;--orange:#ff8c42;--purple:#b26cf7;
  --text:#e8f0ff;--text2:#7a8fb5;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);overflow:hidden;width:100%;height:100%;user-select:none;pointer-events:auto;}

#diff-select{position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(5,8,15,.98);background-image:radial-gradient(ellipse 70% 50% at 50% 30%,rgba(255,69,96,.07) 0%,transparent 70%);overflow-y:auto;pointer-events:auto;}
.ds-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.8rem,5vw,3rem);background:linear-gradient(135deg,#ff4560,#ff8c42,#ffd700);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px;margin-bottom:4px;text-align:center;}
.ds-sub{color:var(--text2);font-size:.76rem;letter-spacing:5px;margin-bottom:6px;text-align:center;}
.ds-version{display:inline-block;background:rgba(255,140,66,.15);border:1px solid rgba(255,140,66,.4);color:var(--orange);border-radius:20px;padding:2px 12px;font-size:.72rem;font-weight:700;margin-bottom:20px;letter-spacing:2px;}
.diff-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;max-width:600px;width:92%;margin-bottom:16px;}
@media(min-width:600px){.diff-grid{grid-template-columns:repeat(4,1fr);max-width:800px;}}
.diff-card{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 12px;cursor:pointer;transition:all .22s;text-align:center;position:relative;overflow:hidden;pointer-events:auto;}
.diff-card:hover,.diff-card.sel{transform:translateY(-5px);}
.diff-card[data-d="0"]:hover,.diff-card[data-d="0"].sel{border-color:#10d96e;box-shadow:0 0 28px rgba(16,217,110,.25);}
.diff-card[data-d="1"]:hover,.diff-card[data-d="1"].sel{border-color:#4dabf7;box-shadow:0 0 28px rgba(77,171,247,.25);}
.diff-card[data-d="2"]:hover,.diff-card[data-d="2"].sel{border-color:#ff8c42;box-shadow:0 0 28px rgba(255,140,66,.25);}
.diff-card[data-d="3"]:hover,.diff-card[data-d="3"].sel{border-color:#ff4560;box-shadow:0 0 28px rgba(255,69,96,.25);}
.diff-em{font-size:2rem;margin-bottom:6px;}
.diff-name{font-family:'Black Han Sans',sans-serif;font-size:1.05rem;margin-bottom:5px;}
.diff-desc{font-size:.7rem;color:var(--text2);line-height:1.65;}
.diff-tag{display:inline-block;font-size:.6rem;font-weight:700;border-radius:20px;padding:2px 8px;margin-top:6px;}
.feature-row{display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;justify-content:center;max-width:800px;}
.feat-pill{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:4px 12px;font-size:.7rem;color:var(--text2);}
.feat-pill span{color:var(--cyan);}
.start-btn{padding:13px 52px;font-size:1.05rem;font-weight:900;font-family:'Black Han Sans',sans-serif;background:linear-gradient(135deg,#ff4560,#ff8c42);color:#fff;border:none;border-radius:40px;cursor:pointer;letter-spacing:2px;transition:all .2s;box-shadow:0 0 32px rgba(255,69,96,.4);pointer-events:auto;}
.start-btn:hover{transform:scale(1.05);box-shadow:0 0 50px rgba(255,69,96,.6);}

#game{display:none;width:100%;height:100vh;flex-direction:column;overflow:hidden;position:fixed;inset:0;}

.hud{background:rgba(5,8,15,.96);border-bottom:1px solid rgba(255,255,255,.07);padding:5px 12px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:3px;position:relative;z-index:50;height:48px;min-height:48px;max-height:48px;flex-shrink:0;}
.hud-left,.hud-right{display:flex;align-items:center;gap:7px;flex-wrap:wrap;}
.hud-title{font-family:'Orbitron',sans-serif;font-size:.75rem;font-weight:700;color:var(--orange);}
.base-hp-wrap{display:flex;align-items:center;gap:5px;}
.base-label{font-size:.65rem;color:var(--text2);font-weight:700;min-width:32px;}
.hp-bar-outer{width:90px;height:10px;background:rgba(255,255,255,.06);border-radius:5px;overflow:hidden;border:1px solid rgba(255,255,255,.08);}
.hp-fill{height:100%;border-radius:5px;transition:width .3s;}
.hp-fill.ally{background:linear-gradient(90deg,#10d96e,#22d3ee);}
.hp-fill.enemy{background:linear-gradient(90deg,#ff4560,#ff8c42);}
.hp-val{font-size:.68rem;font-weight:700;min-width:28px;}
.hud-badge{border-radius:8px;padding:2px 8px;font-size:.7rem;font-weight:700;}
.res-badge{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);color:var(--gold);}
.wave-badge{background:rgba(178,108,247,.12);border:1px solid rgba(178,108,247,.3);color:var(--purple);}
.score-badge{background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.3);color:var(--cyan);}
.kills-badge{background:rgba(255,69,96,.1);border:1px solid rgba(255,69,96,.3);color:var(--red);}
.diff-hud-badge{font-size:.65rem;padding:2px 7px;border-radius:20px;font-weight:700;}
.weather-badge{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);color:var(--text2);font-size:.65rem;padding:2px 7px;border-radius:8px;}

#battlefield{display:block;width:100%;flex:1;min-height:0;cursor:crosshair;}

/* BOTTOM PANEL */
.bot-panel{background:rgba(5,8,15,.96);border-top:1px solid rgba(255,255,255,.07);padding:4px 8px;display:flex;align-items:center;gap:4px;flex-wrap:nowrap;position:relative;z-index:50;height:80px;min-height:80px;max-height:80px;flex-shrink:0;overflow:hidden;}

/* LANE SELECTOR */
.lane-sel{display:flex;flex-direction:column;gap:3px;flex-shrink:0;margin-right:4px;}
.lane-sel-title{font-size:.52rem;color:var(--text2);text-align:center;font-weight:700;}
.lane-btn{padding:3px 10px;border-radius:7px;border:1.5px solid rgba(255,255,255,.15);background:rgba(255,255,255,.04);color:var(--text2);font-size:.65rem;font-weight:900;cursor:pointer;transition:all .18s;text-align:center;pointer-events:auto;white-space:nowrap;}
.lane-btn:hover{border-color:var(--cyan);color:var(--cyan);}
.lane-btn.top-active{border-color:#b26cf7;background:rgba(178,108,247,.18);color:#b26cf7;}
.lane-btn.mid-active{border-color:#22d3ee;background:rgba(34,211,238,.18);color:#22d3ee;}
.lane-btn.bot-active{border-color:#10d96e;background:rgba(16,217,110,.18);color:#10d96e;}

.unit-btn{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:3px 5px;cursor:pointer;transition:all .18s;text-align:center;min-width:52px;max-width:58px;position:relative;pointer-events:auto;flex-shrink:0;}
.unit-btn:hover:not(:disabled){transform:translateY(-2px);border-color:var(--cyan);background:rgba(34,211,238,.07);}
.unit-btn:disabled{opacity:.35;cursor:not-allowed;}
.unit-btn .key-badge{position:absolute;top:2px;left:3px;font-size:.5rem;color:var(--text2);font-weight:900;}
.unit-btn .uem{font-size:1rem;display:block;margin-bottom:1px;}
.unit-btn .uname{font-size:.55rem;font-weight:700;display:block;}
.unit-btn .ucost{font-size:.52rem;color:var(--gold);display:block;}
.unit-btn .ucool{height:3px;background:rgba(255,255,255,.08);border-radius:2px;margin-top:2px;overflow:hidden;}
.unit-btn .ucool-fill{height:100%;background:var(--cyan);border-radius:2px;transition:width .1s linear;}

.ability-row{display:flex;gap:4px;margin-left:auto;align-items:center;flex-shrink:0;}
.abil-btn{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);border-radius:10px;padding:3px 5px;cursor:pointer;text-align:center;min-width:48px;transition:all .2s;position:relative;pointer-events:auto;}
.abil-btn:hover:not(.cooldown){border-color:var(--gold);background:rgba(255,215,0,.08);}
.abil-btn.cooldown{opacity:.45;cursor:not-allowed;}
.abil-btn .aem{font-size:.9rem;display:block;}
.abil-btn .aname{font-size:.5rem;font-weight:700;color:var(--gold);}
.abil-btn .acool{font-size:.5rem;color:var(--text2);}
.abil-cd-bar{position:absolute;bottom:0;left:0;height:3px;background:var(--gold);border-radius:0 0 8px 8px;transition:width .1s linear;}
.snipe-hint{font-size:.58rem;color:var(--text2);line-height:1.45;padding-left:8px;border-left:2px solid rgba(255,255,255,.08);flex-shrink:0;}

/* SCOPE */
#scope{position:fixed;pointer-events:none;z-index:1000;display:none;filter:drop-shadow(0 0 6px rgba(255,69,96,0.5));transform:translate(-50%,-50%);left:-999px;top:-999px;}

/* FLASH / OVERLAY */
#hs-flash{position:fixed;inset:0;pointer-events:none;z-index:900;background:rgba(255,215,0,0);transition:background .05s;}
#night-overlay{position:fixed;inset:0;pointer-events:none;z-index:45;background:rgba(0,0,30,0);transition:background 3s;}
#fw{position:fixed;inset:0;pointer-events:none;z-index:490;overflow:hidden;}
@keyframes fwp{to{transform:translate(var(--dx),var(--dy));opacity:0;}}

/* KILL FEED */
#killfeed{position:fixed;top:55px;right:14px;z-index:200;display:flex;flex-direction:column;gap:3px;pointer-events:none;}
.kf-item{background:rgba(5,8,15,.9);border:1px solid rgba(255,69,96,.3);border-radius:7px;padding:3px 10px;font-size:.67rem;font-weight:700;animation:kfIn .2s,kfOut .3s 2.5s forwards;white-space:nowrap;}
@keyframes kfIn{from{opacity:0;transform:translateX(20px);}to{opacity:1;transform:none;}}
@keyframes kfOut{to{opacity:0;transform:translateX(20px);}}

/* TOAST */
.twrap{position:fixed;top:60px;left:50%;transform:translateX(-50%);z-index:600;display:flex;flex-direction:column;align-items:center;gap:5px;pointer-events:none;}
.toast{padding:5px 13px;border-radius:9px;font-size:.75rem;font-weight:700;background:rgba(8,13,26,.96);border:1px solid rgba(255,255,255,.1);animation:ti .22s,to2 .22s 2.3s forwards;white-space:nowrap;}
@keyframes ti{from{opacity:0;transform:translateY(-8px);}to{opacity:1;transform:none;}}
@keyframes to2{to{opacity:0;transform:translateY(-8px);}}
.hs-toast{padding:8px 20px;border-radius:12px;font-size:.88rem;font-weight:900;background:rgba(255,215,0,.15);border:2px solid rgba(255,215,0,.6);color:#ffd700;text-shadow:0 0 10px #ffd700;animation:ti .15s,to2 .15s 1.8s forwards;white-space:nowrap;font-family:'Black Han Sans',sans-serif;}

/* BOSS ALERT */
#boss-alert{position:fixed;inset:0;z-index:400;pointer-events:none;display:flex;align-items:center;justify-content:center;}
.boss-alert-box{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,6vw,4rem);color:#ff4560;text-shadow:0 0 40px #ff4560,0 0 80px #ff4560;animation:bossAlert 2.2s ease-out forwards;}
.event-alert-box{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.5rem,4vw,3rem);color:#10d96e;text-shadow:0 0 30px #10d96e;animation:bossAlert 2.2s ease-out forwards;}
.miniboss-alert-box{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.5rem,4vw,2.8rem);color:#ff8c42;text-shadow:0 0 30px #ff8c42;animation:bossAlert 2.2s ease-out forwards;}
@keyframes bossAlert{0%{opacity:0;transform:scale(.5);}30%{opacity:1;transform:scale(1.1);}70%{opacity:1;transform:scale(1);}100%{opacity:0;transform:scale(1.2);}}

/* RESULT */
#result{display:none;position:fixed;inset:0;z-index:500;background:rgba(5,8,15,.97);flex-direction:column;align-items:center;justify-content:center;background-image:radial-gradient(ellipse 60% 50% at 50% 40%,rgba(255,215,0,.06) 0%,transparent 70%);pointer-events:auto;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(2.5rem,7vw,4rem);margin-bottom:6px;text-align:center;}
.res-subtitle{font-size:.85rem;color:var(--text2);margin-bottom:22px;text-align:center;letter-spacing:2px;}
.res-stats{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 24px;margin-bottom:20px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px;min-width:360px;}
.stat-item{text-align:center;}
.stat-v{font-size:1.3rem;font-weight:900;color:var(--gold);}
.stat-l{font-size:.68rem;color:var(--text2);margin-top:2px;}
.grade-box{font-family:'Black Han Sans',sans-serif;font-size:3.5rem;margin-bottom:14px;text-shadow:0 0 30px currentColor;}
.res-btn-row{display:flex;gap:10px;}
.res-btn{padding:11px 32px;font-size:.88rem;font-weight:900;border:none;border-radius:36px;cursor:pointer;letter-spacing:2px;transition:all .2s;pointer-events:auto;}
.res-btn.main{background:linear-gradient(135deg,var(--gold),#ff8c00);color:#1a0500;}
.res-btn.main:hover{transform:scale(1.05);}
.res-btn.menu{background:rgba(255,255,255,.06);color:var(--text2);border:1px solid rgba(255,255,255,.12);}
.res-btn.menu:hover{border-color:var(--cyan);color:var(--cyan);}

/* SHOP */
#shop-modal{display:none;position:fixed;inset:0;z-index:450;background:rgba(0,0,0,.75);align-items:center;justify-content:center;backdrop-filter:blur(6px);pointer-events:auto;}
.shop-box{background:linear-gradient(160deg,#0d1830,#1a2545);border:1px solid rgba(255,255,255,.1);border-radius:18px;padding:20px;max-width:540px;width:94%;box-shadow:0 30px 80px rgba(0,0,0,.7);max-height:85vh;overflow-y:auto;pointer-events:auto;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.3rem;color:var(--gold);margin-bottom:4px;}
.shop-sub{color:var(--text2);font-size:.74rem;margin-bottom:12px;}
.shop-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:12px;}
.shop-item{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:9px 6px;text-align:center;cursor:pointer;transition:all .2s;pointer-events:auto;}
.shop-item:hover:not(.bought){border-color:var(--gold);background:rgba(255,215,0,.07);}
.shop-item.bought{opacity:.5;cursor:not-allowed;}
.shop-item .sem{font-size:1.4rem;display:block;margin-bottom:2px;}
.shop-item .sname{font-size:.7rem;font-weight:700;display:block;margin-bottom:2px;}
.shop-item .sdesc{font-size:.6rem;color:var(--text2);display:block;margin-bottom:3px;}
.shop-item .scost{font-size:.68rem;color:var(--gold);font-weight:700;}
.shop-close{padding:8px 24px;border-radius:30px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);color:var(--text2);cursor:pointer;font-size:.85rem;font-weight:700;transition:all .2s;pointer-events:auto;}
.shop-close:hover{border-color:var(--red);color:var(--red);}

/* LANE STATUS BAR (위에 표시) */
#lane-status{position:fixed;top:48px;left:0;right:0;z-index:48;background:rgba(5,8,15,.92);border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;padding:2px 12px;gap:10px;height:26px;}
.ls-lane{display:flex;align-items:center;gap:5px;flex:1;}
.ls-name{font-size:.6rem;font-weight:900;min-width:22px;}
.ls-bar-wrap{flex:1;height:6px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden;position:relative;}
.ls-ally-fill{position:absolute;left:0;top:0;height:100%;border-radius:3px 0 0 3px;transition:width .3s;}
.ls-enemy-fill{position:absolute;right:0;top:0;height:100%;border-radius:0 3px 3px 0;transition:width .3s;}
.ls-units{font-size:.55rem;color:var(--text2);min-width:28px;text-align:center;}
.ls-sel{font-size:.6rem;font-weight:900;margin-left:3px;}
</style>
</head>
<body>
<div id="fw"></div>
<div id="night-overlay"></div>
<div id="hs-flash"></div>

<!-- DIFF SELECT -->
<div id="diff-select">
  <div class="ds-title">⚔️ 전장 저격전</div>
  <div class="ds-sub">3-LANE BATTLEFIELD · SNIPER EDITION</div>
  <div class="ds-version">VERSION 4.0</div>
  <div class="feature-row">
    <div class="feat-pill">🗺️ <span>탑·미드·바텀 3라인</span></div>
    <div class="feat-pill">🎯 <span>헤드샷 시스템</span></div>
    <div class="feat-pill">🛡️ <span>라인별 타워 HP</span></div>
    <div class="feat-pill">💥 <span>스킬 5종</span></div>
    <div class="feat-pill">👹 <span>보스+미니보스</span></div>
    <div class="feat-pill">🌦️ <span>날씨 시스템</span></div>
    <div class="feat-pill">🛒 <span>전술 상점</span></div>
    <div class="feat-pill">🤖 <span>스마트 봇 AI</span></div>
  </div>
  <div class="diff-grid">
    <div class="diff-card sel" data-d="0">
      <div class="diff-em">🟢</div>
      <div class="diff-name" style="color:#10d96e">초 보</div>
      <div class="diff-desc">느린 적 AI<br>풍부한 자원<br>라인 학습용</div>
      <div class="diff-tag" style="background:rgba(16,217,110,.15);color:#10d96e;border:1px solid rgba(16,217,110,.3);">추천 입문</div>
    </div>
    <div class="diff-card" data-d="1">
      <div class="diff-em">🔵</div>
      <div class="diff-name" style="color:#4dabf7">중 급</div>
      <div class="diff-desc">균형 잡힌 전투<br>라인 분산 침투<br>저격 집중 필요</div>
      <div class="diff-tag" style="background:rgba(77,171,247,.15);color:#4dabf7;border:1px solid rgba(77,171,247,.3);">밸런스</div>
    </div>
    <div class="diff-card" data-d="2">
      <div class="diff-em">🟠</div>
      <div class="diff-name" style="color:#ff8c42">어 려 움</div>
      <div class="diff-desc">스마트 AI<br>약한 라인 집중<br>빠른 강유닛</div>
      <div class="diff-tag" style="background:rgba(255,140,66,.15);color:#ff8c42;border:1px solid rgba(255,140,66,.3);">고수용</div>
    </div>
    <div class="diff-card" data-d="3">
      <div class="diff-em">🔴</div>
      <div class="diff-name" style="color:#ff4560">극 악</div>
      <div class="diff-desc">전 라인 동시 러시<br>최강 유닛 폭격<br>1초도 방심 금지</div>
      <div class="diff-tag" style="background:rgba(255,69,96,.15);color:#ff4560;border:1px solid rgba(255,69,96,.3);">🔥 지옥</div>
    </div>
  </div>
  <button class="start-btn" id="start-btn">⚔️ 전투 시작</button>
</div>

<!-- GAME -->
<div id="game">
  <div class="hud">
    <div class="hud-left">
      <span class="hud-title">⚔️ BATTLEFIELD v4</span>
      <div class="base-hp-wrap">
        <span class="base-label">🏰 아군</span>
        <div class="hp-bar-outer"><div class="hp-fill ally" id="ally-hp-bar" style="width:100%"></div></div>
        <span class="hp-val" id="ally-hp-val" style="color:var(--green)">4500</span>
      </div>
      <div class="base-hp-wrap">
        <span class="base-label">🏯 적군</span>
        <div class="hp-bar-outer"><div class="hp-fill enemy" id="enemy-hp-bar" style="width:100%"></div></div>
        <span class="hp-val" id="enemy-hp-val" style="color:var(--red)">4500</span>
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

  <!-- 라인별 상태바 (HUD 바로 아래) -->
  <div id="lane-status">
    <div class="ls-lane">
      <span class="ls-name" style="color:#b26cf7">⬆탑</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-0" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-0" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-0">0v0</span>
    </div>
    <div class="ls-lane">
      <span class="ls-name" style="color:#22d3ee">➡미드</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-1" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-1" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-1">0v0</span>
    </div>
    <div class="ls-lane">
      <span class="ls-name" style="color:#10d96e">⬇봇</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-2" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-2" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-2">0v0</span>
    </div>
    <span id="deploy-indicator" style="font-size:.62rem;font-weight:900;color:#22d3ee;margin-left:8px;">배치: 미드</span>
  </div>

  <canvas id="battlefield"></canvas>

  <div class="bot-panel">
    <!-- 라인 선택 -->
    <div class="lane-sel">
      <div class="lane-sel-title">배치 라인</div>
      <button class="lane-btn" id="lane-btn-0" onclick="selectLane(0)">⬆️ 탑</button>
      <button class="lane-btn mid-active" id="lane-btn-1" onclick="selectLane(1)">➡️ 미드</button>
      <button class="lane-btn" id="lane-btn-2" onclick="selectLane(2)">⬇️ 봇</button>
    </div>

    <button class="unit-btn" id="btn0" onclick="spawnAlly(0)">
      <span class="key-badge">1</span><span class="uem">🧍</span><span class="uname">보병</span><span class="ucost">💎30</span>
      <div class="ucool"><div class="ucool-fill" id="cool0" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn1" onclick="spawnAlly(1)">
      <span class="key-badge">2</span><span class="uem">🪖</span><span class="uname">돌격대</span><span class="ucost">💎60</span>
      <div class="ucool"><div class="ucool-fill" id="cool1" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn2" onclick="spawnAlly(2)">
      <span class="key-badge">3</span><span class="uem">💪</span><span class="uname">중화기</span><span class="ucost">💎120</span>
      <div class="ucool"><div class="ucool-fill" id="cool2" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn3" onclick="spawnAlly(3)">
      <span class="key-badge">4</span><span class="uem">🏥</span><span class="uname">의무병</span><span class="ucost">💎80</span>
      <div class="ucool"><div class="ucool-fill" id="cool3" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn4" onclick="spawnAlly(4)">
      <span class="key-badge">5</span><span class="uem">🎯</span><span class="uname">저격수</span><span class="ucost">💎100</span>
      <div class="ucool"><div class="ucool-fill" id="cool4" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn5" onclick="spawnAlly(5)">
      <span class="key-badge">6</span><span class="uem">🛡️</span><span class="uname">전차</span><span class="ucost">💎200</span>
      <div class="ucool"><div class="ucool-fill" id="cool5" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn6" onclick="spawnAlly(6)">
      <span class="key-badge">7</span><span class="uem">🤖</span><span class="uname">기갑</span><span class="ucost">💎160</span>
      <div class="ucool"><div class="ucool-fill" id="cool6" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn7" onclick="spawnAlly(7)">
      <span class="key-badge">8</span><span class="uem">🔥</span><span class="uname">화염</span><span class="ucost">💎90</span>
      <div class="ucool"><div class="ucool-fill" id="cool7" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn8" onclick="spawnAlly(8)">
      <span class="key-badge">9</span><span class="uem">🥷</span><span class="uname">닌자</span><span class="ucost">💎75</span>
      <div class="ucool"><div class="ucool-fill" id="cool8" style="width:100%"></div></div>
    </button>

    <div class="ability-row">
      <div class="abil-btn" id="abil0" onclick="useAbility(0)"><span class="aem">💣</span><span class="aname">공습</span><span class="acool" id="acool0">Q</span><div class="abil-cd-bar" id="abar0" style="width:100%"></div></div>
      <div class="abil-btn" id="abil1" onclick="useAbility(1)"><span class="aem">⚡</span><span class="aname">전격전</span><span class="acool" id="acool1">E</span><div class="abil-cd-bar" id="abar1" style="width:100%"></div></div>
      <div class="abil-btn" id="abil2" onclick="useAbility(2)"><span class="aem">🛡️</span><span class="aname">방어막</span><span class="acool" id="acool2">R</span><div class="abil-cd-bar" id="abar2" style="width:100%"></div></div>
      <div class="abil-btn" id="abil3" onclick="useAbility(3)" style="border-color:rgba(255,50,50,.3);"><span class="aem">☢️</span><span class="aname">핵폭탄</span><span class="acool" id="acool3">W</span><div class="abil-cd-bar" id="abar3" style="width:100%"></div></div>
      <div class="abil-btn" id="abil4" onclick="useAbility(4)" style="border-color:rgba(100,200,255,.3);"><span class="aem">⏸️</span><span class="aname">시간정지</span><span class="acool" id="acool4">T</span><div class="abil-cd-bar" id="abar4" style="width:100%"></div></div>
      <button class="unit-btn" onclick="openShop()" style="border-color:rgba(255,215,0,.3);min-width:44px;max-width:50px;">
        <span class="uem">🛒</span><span class="uname" style="color:var(--gold)">상점</span><span class="ucost">S키</span>
      </button>
      <div class="snipe-hint">
        🔭 <b>클릭 저격</b><br>
        장전: <span id="reload-status" style="color:var(--green)">준비</span><br>
        콤보:<span id="combo-val" style="color:var(--gold)">×1</span> 관통:<span id="pierce-val" style="color:var(--purple)">×1</span>
      </div>
    </div>
  </div>
</div>

<!-- SCOPE -->
<div id="scope">
  <svg width="110" height="110" viewBox="0 0 110 110">
    <circle cx="55" cy="55" r="50" fill="rgba(0,0,0,0.12)" stroke="rgba(255,69,96,0.9)" stroke-width="2.5"/>
    <circle cx="55" cy="55" r="3" fill="rgba(255,69,96,1)"/>
    <line x1="55" y1="2" x2="55" y2="36" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="55" y1="74" x2="55" y2="108" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="2" y1="55" x2="36" y2="55" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
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
    <div class="shop-sub">💎 <span id="shop-res">0</span> — 전술 업그레이드</div>
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

// ═══════════════════════════════════
//  UNIT DEFINITIONS
// ═══════════════════════════════════
const UNIT_DEFS = [
  {id:0,name:'보병',    em:'🧍',cost:30, hp:130, atk:14, spd:1.0, range:48, ranged:false,pri:1,reward:14,trainTime:32},
  {id:1,name:'돌격대',  em:'🪖',cost:60, hp:260, atk:30, spd:1.3, range:58, ranged:false,pri:2,reward:25,trainTime:52},
  {id:2,name:'중화기',  em:'💪',cost:120,hp:420, atk:58, spd:0.65,range:82, ranged:true, pri:4,reward:50,trainTime:80},
  {id:3,name:'의무병',  em:'🏥',cost:80, hp:160, atk:5,  spd:0.85,range:80, ranged:false,pri:1,reward:20,trainTime:62,healer:true},
  {id:4,name:'저격수',  em:'🎯',cost:100,hp:100, atk:95, spd:0.58,range:260,ranged:true, pri:3,reward:36,trainTime:72},
  {id:5,name:'전차',    em:'🛡️',cost:200,hp:900, atk:70, spd:0.45,range:100,ranged:false,pri:5,reward:100,trainTime:128},
  {id:6,name:'기갑',    em:'🤖',cost:160,hp:580, atk:62, spd:0.56,range:85, ranged:false,pri:5,reward:78,trainTime:98,armored:true},
  {id:7,name:'화염',    em:'🔥',cost:90, hp:180, atk:44, spd:0.78,range:62, ranged:false,pri:3,reward:32,trainTime:58,flamer:true},
  {id:8,name:'닌자',    em:'🥷',cost:75, hp:110, atk:58, spd:2.6, range:46, ranged:false,pri:3,reward:28,trainTime:48,ninja:true},
  // ENEMY (9~18)
  {id:9, name:'적보병', em:'👹',cost:30, hp:110, atk:11, spd:0.9, range:44, ranged:false,pri:1,reward:11},
  {id:10,name:'장교',   em:'🎖️',cost:150,hp:320, atk:40, spd:0.85,range:62, ranged:false,pri:3,reward:60},
  {id:11,name:'로켓병', em:'🚀',cost:180,hp:175, atk:85, spd:0.55,range:210,ranged:true, pri:4,reward:70},
  {id:12,name:'적탱크', em:'🛡️',cost:280,hp:900, atk:70, spd:0.42,range:92, ranged:false,pri:5,reward:120},
  {id:13,name:'드론',   em:'🛸',cost:120,hp:85,  atk:32, spd:1.7, range:85, ranged:true, pri:3,reward:42},
  {id:14,name:'보스',   em:'💀',cost:999,hp:4000,atk:100,spd:0.5, range:110,ranged:false,pri:5,reward:350,isBoss:true},
  {id:15,name:'미니보스',em:'😈',cost:600,hp:1600,atk:68, spd:0.72,range:92, ranged:false,pri:5,reward:180,isMiniBoss:true},
  {id:16,name:'특공대', em:'💣',cost:200,hp:190, atk:75, spd:1.5, range:46, ranged:false,pri:4,reward:78,kamikaze:true},
  {id:17,name:'포격수', em:'🎖️',cost:220,hp:210, atk:100,spd:0.5, range:230,ranged:true, pri:5,reward:88},
  {id:18,name:'사이보그',em:'🦾',cost:240,hp:480, atk:80, spd:0.95,range:72, ranged:false,pri:5,reward:105},
];

// ═══════════════════════════════════
//  ABILITIES
// ═══════════════════════════════════
const ABILITY_DEFS = [
  {id:0,name:'공습',em:'💣',key:'q',cd:480,
   fx:()=>{
     const selL=G.selectedLane;
     for(let i=0;i<8;i++) setTimeout(()=>{
       if(!G.running)return;
       const x=ALLY_BASE_X+80+Math.random()*(W-200);
       airstrikeBomb(x,laneY(selL),selL);
     },i*140);
     toast('💣 공습! '+LANE_NAMES[selL]+' 라인!','gold');
   }},
  {id:1,name:'전격전',em:'⚡',key:'e',cd:400,
   fx:()=>{
     G.blitzEnd=G.frame+540;
     G.units.filter(u=>u.side===0).forEach(u=>{if(!u._blitzed){u.spd*=2.2;u._blitzed=true;}});
     toast('⚡ 전격전! 전 아군 강화 9초!','gold');
   }},
  {id:2,name:'방어막',em:'🛡️',key:'r',cd:450,
   fx:()=>{
     G.shieldEnd=G.frame+720;
     for(let i=0;i<3;i++) G.allyTowerHp[i]=Math.min(G.allyTowerHp[i]+200,G.maxTowerHp);
     toast('🛡️ 방어막 12초! + 타워 수리!','good');
   }},
  {id:3,name:'핵폭탄',em:'☢️',key:'w',cd:900,
   fx:()=>{
     toast('☢️ 전 라인 핵폭탄!!!','bad');
     setTimeout(()=>{
       if(!G.running)return;
       const fl=document.getElementById('hs-flash');
       fl.style.background='rgba(255,255,200,0.92)';
       setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},500);
       const toKill=[...G.units.filter(u=>u.side===1&&u.hp>0&&!u.isBoss)];
       toKill.forEach(u=>killUnit(u,0));
       G.units.filter(u=>u.side===1&&u.isBoss&&u.hp>0).forEach(u=>{
         const dmg=Math.round(u.maxHp*0.45);u.hp-=dmg;spawnHit(u.x,u.y,'#ffd700',dmg);
       });
       for(let li=0;li<3;li++) G.enemyTowerHp[li]=Math.max(0,G.enemyTowerHp[li]-400);
       for(let i=0;i<70;i++){
         const ang=Math.random()*Math.PI*2;
         G.particles.push({x:W/2+(Math.random()-.5)*W*.7,y:laneY(1),vx:Math.cos(ang)*5,vy:Math.sin(ang)*5-3,col:['#ffd700','#ff8c42','#ff4560'][i%3],life:42,size:6+Math.random()*8});
       }
     },700);
   }},
  {id:4,name:'시간정지',em:'⏸️',key:'t',cd:600,
   fx:()=>{G.freezeEnd=G.frame+300;toast('⏸️ 전 라인 시간정지! 5초!','wave');}},
];

// ═══════════════════════════════════
//  DIFFICULTY
// ═══════════════════════════════════
const DIFF_CONFIG = [
  {name:'초보',  col:'#10d96e',bgCol:'rgba(16,217,110,.15)',bdCol:'rgba(16,217,110,.35)',
   resRate:2.8,botResRate:0.38,botPool:[9,9,9],           botDelay:5500,startRes:250,laneHp:1800,bossWave:13,miniBossWave:7,
   botStrategyInterval:3500,rushProb:0.08,maxTowerHp:1800},
  {name:'중급',  col:'#4dabf7',bgCol:'rgba(77,171,247,.15)',bdCol:'rgba(77,171,247,.35)',
   resRate:1.8,botResRate:0.85,botPool:[9,10,10,11],      botDelay:3400,startRes:180,laneHp:1600,bossWave:10,miniBossWave:5,
   botStrategyInterval:2200,rushProb:0.22,maxTowerHp:1600},
  {name:'어려움',col:'#ff8c42',bgCol:'rgba(255,140,66,.15)',bdCol:'rgba(255,140,66,.35)',
   resRate:1.25,botResRate:1.35,botPool:[10,11,11,12,13], botDelay:2100,startRes:145,laneHp:1400,bossWave:8, miniBossWave:4,
   botStrategyInterval:1300,rushProb:0.42,maxTowerHp:1400},
  {name:'극악',  col:'#ff4560',bgCol:'rgba(255,69,96,.15)', bdCol:'rgba(255,69,96,.35)',
   resRate:0.98,botResRate:1.9,botPool:[11,12,13,16,17,18],botDelay:1200,startRes:120,laneHp:1200,bossWave:6,miniBossWave:3,
   botStrategyInterval:750,rushProb:0.62,maxTowerHp:1200},
];

// ═══════════════════════════════════
//  SHOP
// ═══════════════════════════════════
const SHOP_ITEMS = [
  {id:'u_hp',    em:'❤️',name:'기지 수리',   desc:'아군 기지 HP +400',        cost:120,fx:()=>{G.allyBase=Math.min(G.allyBase+400,G.maxBase);toast('❤️ 기지 수리 +400!','good');}},
  {id:'u_thp',   em:'🏛️',name:'타워 수리',   desc:'전 라인 타워 HP +300',     cost:150,fx:()=>{for(let i=0;i<3;i++)G.allyTowerHp[i]=Math.min(G.allyTowerHp[i]+300,G.maxTowerHp);toast('🏛️ 전 라인 타워 수리!','good');}},
  {id:'u_res',   em:'💎',name:'자원 증폭',   desc:'자원 수급 +30%',            cost:140,repeatable:true,fx:()=>{G.resBonus=(G.resBonus||1)*1.3;toast('💎 자원 증폭!','good');}},
  {id:'u_atk',   em:'⚔️',name:'무기 강화',   desc:'아군 공격력 +30%',          cost:190,fx:()=>{G.dmgBonus=(G.dmgBonus||1)*1.3;G.units.filter(u=>u.side===0).forEach(u=>u.atk=Math.round(u.atk*1.3));toast('⚔️ 무기 강화!','gold');}},
  {id:'u_snipe', em:'🎯',name:'저격 강화',   desc:'저격 피해 +60%',            cost:160,fx:()=>{G.snipeDmgBonus=(G.snipeDmgBonus||1)*1.6;toast('🎯 저격 강화!','gold');}},
  {id:'u_shield',em:'🛡️',name:'장갑 강화',   desc:'아군 HP +30%',              cost:200,fx:()=>{G.units.filter(u=>u.side===0).forEach(u=>{u.maxHp=Math.round(u.maxHp*1.3);u.hp=Math.round(u.hp*1.3);});toast('🛡️ 장갑 강화!','good');}},
  {id:'u_cd',    em:'⚡',name:'스킬 가속',   desc:'스킬 쿨다운 -30%',         cost:140,fx:()=>{G.cdBonus=(G.cdBonus||1)*0.7;toast('⚡ 스킬 가속!','gold');}},
  {id:'u_pierce',em:'🔫',name:'관통탄',       desc:'저격 관통 +1 (최대4)',      cost:220,repeatable:true,fx:()=>{G.pierceCount=Math.min((G.pierceCount||1)+1,4);document.getElementById('pierce-val').textContent='×'+G.pierceCount;toast('🔫 관통 +1!','gold');}},
  {id:'u_turret',em:'🔰',name:'기지 터렛',   desc:'아군 기지 자동 터렛 강화', cost:280,repeatable:true,fx:()=>{G.turretLevel=(G.turretLevel||0)+1;toast('🔰 터렛 Lv'+G.turretLevel+'!','good');}},
  {id:'u_speed', em:'💨',name:'기동력',       desc:'아군 이동속도 +25%',        cost:170,fx:()=>{G.units.filter(u=>u.side===0).forEach(u=>u.spd*=1.25);G.spdBonus=(G.spdBonus||1)*1.25;toast('💨 기동력 강화!','good');}},
  {id:'u_multi', em:'🌀',name:'산탄 저격',   desc:'저격 시 근처 3명 추가 피해',cost:250,fx:()=>{G.multiSnipe=true;toast('🌀 산탄 저격!','gold');}},
  {id:'u_regen', em:'💚',name:'기지 재생',   desc:'기지 HP 초당 3씩 회복',    cost:180,fx:()=>{G.baseRegen=(G.baseRegen||0)+3;toast('💚 기지 재생!','good');}},
  {id:'u_crit',  em:'💥',name:'크리티컬',    desc:'저격 치명타율 +25%',       cost:190,repeatable:true,fx:()=>{G.critBonus=(G.critBonus||0)+0.25;toast('💥 크리티컬 강화!','gold');}},
  {id:'u_aoe',   em:'💫',name:'범위 저격',   desc:'저격 반경 30 범위 피해',   cost:260,fx:()=>{G.aoeSnipe=true;toast('💫 범위 저격!','gold');}},
  {id:'u_tower_atk',em:'🏰',name:'타워 반격',   desc:'아군 타워 자동 공격 활성화', cost:300,fx:()=>{G.towerAttack=true;toast('🏰 타워 반격 활성화!','good');}},
  {id:'u_spawn_boost',em:'⚡',name:'연속 생산',  desc:'유닛 생산 속도 +40%',       cost:220,fx:()=>{G.spawnBoost=(G.spawnBoost||1)*0.72;toast('⚡ 유닛 생산 가속!','good');}},
  {id:'u_double_res',em:'💠',name:'자원 2배',    desc:'다음 15초 자원 2배',        cost:160,repeatable:true,fx:()=>{G.doubleResEnd=G.frame+900;toast('💠 자원 2배 발동!','gold');}},
  {id:'u_massacre',em:'🔱',name:'학살 모드',    desc:'아군 공격력 일시 +100%',    cost:350,fx:()=>{G.massacreEnd=G.frame+480;toast('🔱 학살 모드 15초!','bad');}},
];

// ═══════════════════════════════════
//  WEATHER
// ═══════════════════════════════════
const WEATHERS = [
  {id:'clear',name:'☀️ 맑음',  spdMult:1.0,visRange:1.0, rain:false,night:false},
  {id:'rain', name:'🌧️ 폭우',  spdMult:0.82,visRange:0.85,rain:true, night:false},
  {id:'fog',  name:'🌫️ 안개',  spdMult:0.9, visRange:0.65,rain:false,night:false},
  {id:'night',name:'🌙 야간',  spdMult:1.0, visRange:0.72,rain:false,night:true},
  {id:'storm',name:'⛈️ 폭풍',  spdMult:0.72,visRange:0.75,rain:true, night:true},
];

// ═══════════════════════════════════
//  LANE CONFIG
// ═══════════════════════════════════
const LANE_NAMES=['탑','미드','봇'];
const LANE_COLS=['#b26cf7','#22d3ee','#10d96e'];
// 라인별 Y 위치 비율 (캔버스 height 기준) — 기지 중심 Y
// 기지는 두 측면에 하나씩, 각 라인이 기지 높이의 1/3 지점에 연결됨
const LANE_Y_FRACS=[0.28, 0.55, 0.82]; // 탑, 미드, 봇

// ═══════════════════════════════════
//  GLOBALS
// ═══════════════════════════════════
let G={};
let W=0,H=0;
let ALLY_BASE_X=80, ENEMY_BASE_X=720;
let BASE_W=68, BASE_H=110; // 기지 크기
let shopBoughtItems=new Set();
let rainDrops=[];
let animFrameId=null;
let selectedLane=1; // 기본 미드

const canvas=document.getElementById('battlefield');
const ctx=canvas.getContext('2d');

function laneY(li){ return H*LANE_Y_FRACS[li]; }

// 기지의 각 라인 연결 포인트 (기지 오른쪽 or 왼쪽 엣지)
function allyGateX(){ return ALLY_BASE_X+BASE_W/2+4; }
function enemyGateX(){ return ENEMY_BASE_X-BASE_W/2-4; }
// 기지 내 각 라인의 Y포트 (기지 높이를 3등분)
function allyGateY(li){ return H*0.5 - BASE_H/2 + BASE_H*(li+0.5)/3; }
function enemyGateY(li){ return H*0.5 - BASE_H/2 + BASE_H*(li+0.5)/3; }

// ═══════════════════════════════════
//  RESIZE
// ═══════════════════════════════════
function resize(){
  const rect=canvas.getBoundingClientRect();
  W=Math.max(rect.width,300);
  H=Math.max(rect.height,200);
  canvas.width=W;
  canvas.height=H;
  ALLY_BASE_X=80;
  ENEMY_BASE_X=W-80;
}

// ═══════════════════════════════════
//  LANE SELECT
// ═══════════════════════════════════
function selectLane(li){
  selectedLane=li;
  G.selectedLane=li;
  [0,1,2].forEach(i=>{
    const btn=document.getElementById('lane-btn-'+i);
    btn.className='lane-btn';
    if(i===li) btn.className='lane-btn '+(i===0?'top-active':i===1?'mid-active':'bot-active');
  });
  const ind=document.getElementById('deploy-indicator');
  if(ind){ ind.textContent='배치: '+LANE_NAMES[li]; ind.style.color=LANE_COLS[li]; }
}

// ═══════════════════════════════════
//  START
// ═══════════════════════════════════
function startGame(diff){
  const dc=DIFF_CONFIG[diff];
  shopBoughtItems=new Set();
  rainDrops=Array.from({length:200},()=>({x:Math.random()*2000,y:Math.random()*600,spd:8+Math.random()*6,len:12+Math.random()*10}));
  if(animFrameId) cancelAnimationFrame(animFrameId);

  G={
    running:true,diff,wave:1,
    resources:dc.startRes,
    allyBase:dc.laneHp*3, enemyBase:dc.laneHp*3, maxBase:dc.laneHp*3,
    // 라인별 타워 HP (기지 연결 타워)
    allyTowerHp:[dc.laneHp,dc.laneHp,dc.laneHp],
    enemyTowerHp:[dc.laneHp,dc.laneHp,dc.laneHp],
    maxTowerHp:dc.laneHp,
    units:[],bullets:[],effects:[],particles:[],
    score:0,kills:0,snipes:0,headshots:0,combo:1,comboTimer:0,
    nextId:0,reloading:false,reloadTimer:0,reloadMax:80,
    botTimers:[0,0,0],resTimer:0,waveTimer:0,frame:0,lastTime:performance.now(),
    abilities:[
      {id:0,cd:0,maxCd:ABILITY_DEFS[0].cd},{id:1,cd:0,maxCd:ABILITY_DEFS[1].cd},
      {id:2,cd:0,maxCd:ABILITY_DEFS[2].cd},{id:3,cd:0,maxCd:ABILITY_DEFS[3].cd},
      {id:4,cd:0,maxCd:ABILITY_DEFS[4].cd},
    ],
    trainCooldowns:[0,0,0,0,0,0,0,0,0],
    blitzEnd:-1,shieldEnd:-1,freezeEnd:-1,
    massacreEnd:-1,doubleResEnd:-1,
    towerAttack:false,towerAttackTimer:0,
    spawnBoost:1,
    resBonus:1,dmgBonus:1,snipeDmgBonus:1,cdBonus:1,spdBonus:1,
    pierceCount:1,multiSnipe:false,aoeSnipe:false,critBonus:0,baseRegen:0,
    turretLevel:0,turretTimer:0,
    weather:WEATHERS[0],weatherTimer:0,
    mouseX:0,mouseY:0,
    selectedLane:1,
    // 봇 AI 전략
    botFocusLane:1, // AI가 집중 공격할 라인
    botStrategyTimer:0,
    craters:[],
  };

  selectedLane=1;
  selectLane(1);

  document.getElementById('diff-select').style.display='none';
  document.getElementById('game').style.display='flex';
  document.getElementById('result').style.display='none';
  document.getElementById('boss-alert').style.display='none';

  const dc2=DIFF_CONFIG[diff];
  const db=document.getElementById('diff-badge');
  db.textContent=dc2.name;
  db.style.cssText=`background:${dc2.bgCol};color:${dc2.col};border:1px solid ${dc2.bdCol};`;

  let attempts=0;
  function tryStart(){
    resize();
    if(W<100&&attempts<10){attempts++;setTimeout(tryStart,50);return;}
    for(let i=0;i<6;i++) G.craters.push({x:150+Math.random()*(W-300),y:laneY(Math.floor(i/2)),r:14+Math.random()*18});
    updateHUD(); updateButtons();
    document.getElementById('scope').style.display='block';
    canvas.style.cursor='crosshair';
    document.getElementById('pierce-val').textContent='×'+G.pierceCount;
    G.lastTime=performance.now();
    animFrameId=requestAnimationFrame(loop);
  }
  setTimeout(tryStart,60);
}

function goMenu(){
  G.running=false;
  document.getElementById('result').style.display='none';
  document.getElementById('diff-select').style.display='flex';
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';
}

// ═══════════════════════════════════
//  LOOP
// ═══════════════════════════════════
function loop(ts){
  if(!G.running){animFrameId=null;return;}
  const dt=Math.min((ts-G.lastTime)/16.667,4);
  G.lastTime=ts; G.frame++;
  update(dt); render();
  animFrameId=requestAnimationFrame(loop);
}

// ═══════════════════════════════════
//  UPDATE
// ═══════════════════════════════════
function update(dt){
  const dc=DIFF_CONFIG[G.diff];

  // Weather
  G.weatherTimer+=dt;
  if(G.weatherTimer>1200){
    G.weatherTimer=0;
    const prev=G.weather.id; let next;
    do{next=WEATHERS[Math.floor(Math.random()*WEATHERS.length)];}while(next.id===prev);
    G.weather=next;
    document.getElementById('weather-badge').textContent=next.name;
    document.getElementById('night-overlay').style.background=next.night?'rgba(0,0,30,0.38)':'rgba(0,0,30,0)';
    toast('🌦️ 날씨: '+next.name,'wave');
  }

  // Resources
  G.resTimer+=dt;
  const doubleRes=(G.doubleResEnd>0&&G.frame<G.doubleResEnd)?2:1;
  const resInterval=60/(dc.resRate*(G.resBonus||1)*doubleRes);
  if(G.resTimer>=resInterval){G.resTimer=0;G.resources=Math.min(G.resources+7,900);}

  // Massacre Mode - 학살 모드
  if(G.massacreEnd>0){
    G.units.filter(u=>u.side===0&&u.hp>0&&!u._massBoosted).forEach(u=>{
      u.atk=Math.round(u.atk*2); u._massBoosted=true;
    });
    if(G.frame>=G.massacreEnd){
      G.units.filter(u=>u.side===0&&u.hp>0&&u._massBoosted).forEach(u=>{
        u.atk=Math.round(u.atk*0.5); u._massBoosted=false;
      });
      G.massacreEnd=-1; toast('학살 모드 종료','wave');
    }
  }

  // Tower Attack - 타워 반격 (아군 타워에서 적 공격)
  if(G.towerAttack){
    G.towerAttackTimer=(G.towerAttackTimer||0)+dt;
    if(G.towerAttackTimer>45){
      G.towerAttackTimer=0;
      for(let li=0;li<3;li++){
        if(G.allyTowerHp[li]<=0) continue;
        const towerX=ALLY_BASE_X+BASE_W+20;
        const tgts=G.units.filter(u=>u.side===1&&u.hp>0&&u.laneIdx===li&&u.x<towerX+180);
        if(tgts.length>0){
          const t=tgts.reduce((a,b)=>a.x<b.x?a:b);
          const dmg=Math.round(40*(G.dmgBonus||1));
          t.hp-=dmg; spawnHit(t.x,t.y,'#ffd700',dmg);
          G.particles.push({x:towerX,y:laneY(li),vx:2,vy:0,col:'#ffd700',life:12,size:3});
        }
      }
    }
  }

  // Base regen
  if(G.baseRegen>0) G.allyBase=Math.min(G.allyBase+G.baseRegen*dt/60,G.maxBase);

  // Wave
  G.waveTimer+=dt;
  if(G.waveTimer>=1800){
    G.waveTimer=0;G.wave++;
    G.maxBase+=200; G.maxTowerHp+=80;
    G.allyBase=Math.min(G.allyBase+60,G.maxBase);
    G.enemyBase=Math.min(G.enemyBase+60,G.maxBase);
    document.getElementById('wave-badge').textContent='웨이브 '+G.wave;
    if(G.wave%dc.bossWave===0) spawnBossWave();
    else if(G.wave%dc.miniBossWave===0) spawnMiniBoss();
    else if(G.wave%8===0) spawnEventWave();
    else toast('🌊 웨이브 '+G.wave+'!','wave');
  }

  // Bot AI: 라인별 독립 타이머
  const botDelayFrames=dc.botDelay/16.667;
  for(let li=0;li<3;li++){
    G.botTimers[li]+=dt;
    // 집중 라인은 2배 빠르게 스폰
    const mult=(li===G.botFocusLane)?0.5:1.0;
    if(G.botTimers[li]>=botDelayFrames*mult){
      G.botTimers[li]=0;
      botSpawn(li);
    }
  }

  // Bot strategy update: 주기적으로 약한 라인으로 집중 전환
  G.botStrategyTimer+=dt;
  const stratInterval=dc.botStrategyInterval/16.667;
  if(G.botStrategyTimer>=stratInterval){
    G.botStrategyTimer=0;
    updateBotStrategy(dc);
  }

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

  if(G.blitzEnd>0&&G.frame===G.blitzEnd){
    G.units.filter(u=>u.side===0&&u._blitzed).forEach(u=>{u.spd/=2;u._blitzed=false;});
    toast('⚡ 전격전 종료','');
  }

  if(G.comboTimer>0){G.comboTimer-=dt;if(G.comboTimer<=0){G.combo=1;document.getElementById('combo-val').textContent='×1';}}

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
    const turretRate=55/(G.turretLevel*1.6);
    if(G.turretTimer>=turretRate){
      G.turretTimer=0;
      const enemies=G.units.filter(u=>u.side===1&&u.hp>0).sort((a,b)=>a.x-b.x);
      if(enemies.length>0){
        const t=enemies[0];
        const tdmg=Math.round(35*G.turretLevel*(G.dmgBonus||1));
        G.bullets.push({x:ALLY_BASE_X+BASE_W/2,y:H*0.5,tx:t.x,ty:t.y-18,col:'#b26cf7',dmg:tdmg,targetId:t.uid,fromSide:0,spd:13,pierce:0,maxPierce:0});
      }
    }
  }

  updateUnits(dt,frozen);
  updateBullets(dt);
  updateEffects(dt);
  updateParticles(dt);

  // 게임 오버: 기지 전체 HP 기준
  const totalAlly=G.allyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalEnemy=G.enemyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  G.allyBase=totalAlly; G.enemyBase=totalEnemy;
  if(G.enemyBase<=0) endGame(true);
  else if(G.allyBase<=0) endGame(false);

  updateHUD();
  updateButtons();
  updateLaneStatus();
}

// ═══════════════════════════════════
//  BOT STRATEGY
// ═══════════════════════════════════
function updateBotStrategy(dc){
  // 아군 타워 HP가 낮은 라인 우선 + 랜덤 러시
  if(Math.random()<dc.rushProb){
    // 랜덤 라인 러시
    G.botFocusLane=Math.floor(Math.random()*3);
    if(G.diff>=1) toast('⚠️ 적 '+LANE_NAMES[G.botFocusLane]+' 라인 집중 공격!','bad');
  } else {
    // 아군 타워 가장 약한 라인
    let minHp=Infinity,focusLi=1;
    G.allyTowerHp.forEach((hp,li)=>{if(hp<minHp){minHp=hp;focusLi=li;}});
    G.botFocusLane=focusLi;
  }
}

// ═══════════════════════════════════
//  UNIT SPAWN
// ═══════════════════════════════════
function spawnUnit(defId,side,laneIdx){
  const def=UNIT_DEFS[defId];
  const ws=1+(G.wave-1)*0.11;
  const isBoss=def.isBoss||false;
  const isMiniBoss=def.isMiniBoss||false;
  const hpMult=isBoss?(1+G.diff*0.3):(isMiniBoss?(1+G.diff*0.22):1);
  const startX=side===0?ALLY_BASE_X+BASE_W/2+10:ENEMY_BASE_X-BASE_W/2-10;
  // 유닛은 라인 Y에서 시작
  const gy=allyGateY(laneIdx);
  const u={
    uid:G.nextId++,defId,side,laneIdx,
    x:startX, y:gy,
    targetY:laneY(laneIdx), // 라인 Y로 이동
    reachedLane:false, // 라인 Y에 도달했는지
    hp:Math.round(def.hp*ws*hpMult),
    maxHp:Math.round(def.hp*ws*hpMult),
    atk:Math.round(def.atk*ws*(side===0?(G.dmgBonus||1):1)),
    spd:def.spd*(side===0?(G.spdBonus||1):1)*G.weather.spdMult,
    baseSpd:def.spd*(side===0?(G.spdBonus||1):1),
    range:def.range*G.weather.visRange,
    ranged:def.ranged,cooldown:0,em:def.em,pri:def.pri,
    healer:def.healer||false,armored:def.armored||false,
    flamer:def.flamer||false,ninja:def.ninja||false,kamikaze:def.kamikaze||false,
    reward:def.reward,name:def.name,
    anim:Math.random()*Math.PI*2,isBoss,isMiniBoss,
    atBaseGate:false, // 상대 기지 앞에 도달
  };
  G.units.push(u);
}

function spawnAlly(defId){
  if(defId>8) return;
  const def=UNIT_DEFS[defId];
  if(G.resources<def.cost){toast('💎 자원 부족!','bad');return;}
  if(G.trainCooldowns[defId]>0){toast('⏳ 훈련 중!','bad');return;}
  G.resources-=def.cost;
  G.trainCooldowns[defId]=Math.round(def.trainTime*(G.spawnBoost||1));
  spawnUnit(defId,0,G.selectedLane);
  updateButtons();
}

function botSpawn(laneIdx){
  const dc=DIFF_CONFIG[G.diff];
  const pool=dc.botPool.filter(id=>id!==14&&id!==15);
  const botRes=65+G.wave*22*dc.botResRate;
  const affor=pool.map(id=>UNIT_DEFS[id]).filter(d=>d.cost<=botRes);
  if(!affor.length) return;
  let chosen;
  if(G.diff>=2){affor.sort((a,b)=>b.cost-a.cost);chosen=affor[Math.floor(Math.random()*Math.min(2,affor.length))];}
  else{chosen=affor[Math.floor(Math.random()*affor.length)];}
  spawnUnit(chosen.id,1,laneIdx);
  // 극악 난이도: 동일 라인 추가 스폰
  if(G.diff===3&&Math.random()<0.45){
    setTimeout(()=>{if(G.running)spawnUnit(chosen.id,1,laneIdx);},400);
  }
}

function spawnBossWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="boss-alert-box">💀 보스 + 전 라인 공략!</div>';
  setTimeout(()=>{ba.style.display='none';},2200);
  const bossLane=Math.floor(Math.random()*3);
  spawnUnit(14,1,bossLane);
  for(let li=0;li<3;li++) setTimeout(()=>{if(G.running)spawnUnit(10,1,li);},li*350);
  toast('💀 보스 웨이브! 전 라인 위기!','bad');
}

function spawnMiniBoss(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="miniboss-alert-box">😈 미니보스 출현!</div>';
  setTimeout(()=>{ba.style.display='none';},2000);
  const ml=G.botFocusLane;
  spawnUnit(15,1,ml);
  for(let i=0;i<2;i++) setTimeout(()=>{if(G.running)spawnUnit(9,1,(ml+i)%3);},i*300);
  toast('😈 미니보스! '+LANE_NAMES[ml]+' 라인!','bad');
}

function spawnEventWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="event-alert-box">🎖️ 전 라인 지원대!</div>';
  setTimeout(()=>{ba.style.display='none';},2000);
  for(let li=0;li<3;li++){
    setTimeout(()=>{if(G.running){spawnUnit(0,0,li);spawnUnit(5,0,li);}},li*250);
  }
  G.resources=Math.min(G.resources+120,900);
  toast('🎖️ 전 라인 지원 + 💎120!','good');
}

// ═══════════════════════════════════
//  UPDATE UNITS
// ═══════════════════════════════════
function updateUnits(dt,frozen){
  G.units.forEach(u=>{
    u.anim+=dt*0.12;
    if(u.hp<=0) return;
    if(frozen&&u.side===1) return;

    u.spd=u.baseSpd*G.weather.spdMult*(u.side===0?(G.spdBonus||1):1);
    if(u._blitzed) u.spd=u.baseSpd*2;

    // 1단계: 기지에서 나와서 라인 Y로 이동 (대각선)
    if(!u.reachedLane){
      const targetY=laneY(u.laneIdx);
      const dy=targetY-u.y;
      const dir=u.side===0?1:-1;
      // X도 조금씩 이동, Y를 더 빠르게
      u.x+=dir*u.spd*0.5*dt;
      if(Math.abs(dy)>2){
        u.y+=Math.sign(dy)*u.spd*1.2*dt;
      } else {
        u.y=targetY;
        u.reachedLane=true;
      }
      return;
    }

    // 2단계: 라인을 따라 이동 (X축 이동)
    // 치유사: 같은 라인 아군 회복
    if(u.healer){
      const hurt=G.units.filter(o=>o.side===u.side&&o.laneIdx===u.laneIdx&&o.hp>0&&o.hp<o.maxHp&&Math.abs(u.x-o.x)<100);
      if(hurt.length>0){hurt[0].hp=Math.min(hurt[0].maxHp,hurt[0].hp+0.6*dt);return;}
    }

    if(u.kamikaze&&u.side===1){
      u.x-=u.spd*dt*1.6;
      if(u.x<=allyGateX()+10){
        const shield=G.frame<G.shieldEnd?0.3:1;
        G.allyTowerHp[u.laneIdx]=Math.max(0,G.allyTowerHp[u.laneIdx]-u.atk*3*shield);
        spawnDeath(u.x,u.y,false);u.hp=0;return;
      }
    }

    // 같은 라인의 적 찾기
    const enemies=G.units.filter(o=>o.side!==u.side&&o.hp>0&&o.laneIdx===u.laneIdx&&o.reachedLane);
    let target=null,minD=Infinity;
    enemies.forEach(e=>{const d=Math.abs(u.x-e.x);if(d<minD){minD=d;target=e;}});

    // 상대 기지 게이트까지 도달했는지 확인
    const gateX=u.side===0?enemyGateX():allyGateX();
    const distToGate=u.side===0?gateX-u.x:u.x-gateX;

    if(target&&minD<=u.range){
      // 적과 교전
      u.cooldown-=dt;
      if(u.cooldown<=0){
        u.cooldown=26-G.diff*2;
        if(u.flamer){
          const inRange=G.units.filter(o=>o.side!==u.side&&o.hp>0&&o.laneIdx===u.laneIdx&&Math.abs(u.x-o.x)<u.range);
          inRange.forEach(e=>{
            const fd=u.atk*0.55; e.hp-=fd;
            spawnHit(e.x,e.y,'#ff8c42',Math.round(fd));
            if(e.hp<=0)killUnit(e,u.side===0?0:1);
          });
        } else if(u.ranged){
          G.bullets.push({x:u.x,y:u.y-18,tx:target.x,ty:target.y-18,col:u.side===0?'#22d3ee':'#ff4560',dmg:u.atk,targetId:target.uid,fromSide:u.side,spd:8,pierce:0,maxPierce:0});
        } else {
          target.hp-=u.atk;
          spawnHit(target.x,target.y,u.side===0?'#22d3ee':'#ff4560',u.atk);
          if(target.hp<=0)killUnit(target,u.side===0?0:1);
        }
      }
    } else if(distToGate<=u.range*0.5){
      // 기지 앞: 기지 공격 (멈추고 기지 깎기)
      u.atBaseGate=true;
      u.cooldown-=dt;
      if(u.cooldown<=0){
        u.cooldown=30-G.diff*2;
        const shield=G.frame<G.shieldEnd?0.3:1;
        if(u.side===0){
          // 아군이 적 타워 공격
          G.enemyTowerHp[u.laneIdx]=Math.max(0,G.enemyTowerHp[u.laneIdx]-u.atk*0.55);
          spawnHit(gateX,laneY(u.laneIdx),'#22d3ee',Math.round(u.atk*0.55));

          // ★ 라인 클리어 시 복귀 & 지원 AI ★
          // 적 타워가 완전히 부서졌고, 이 라인에 적이 없으면 → 가장 위기인 라인으로 이동
          if(G.enemyTowerHp[u.laneIdx]<=0 && !u._roaming){
            const enemiesOnLane=G.units.filter(o=>o.side===1&&o.hp>0&&o.laneIdx===u.laneIdx).length;
            if(enemiesOnLane===0){
              // 가장 약한 아군 타워 라인 찾기 (현재 라인 제외)
              let worstLane=-1, worstHp=Infinity;
              for(let wi=0;wi<3;wi++){
                if(wi===u.laneIdx) continue;
                const lHp=G.allyTowerHp[wi];
                const lEnemies=G.units.filter(o=>o.side===1&&o.hp>0&&o.laneIdx===wi).length;
                if(lEnemies>0&&lHp<worstHp){worstHp=lHp;worstLane=wi;}
              }
              if(worstLane===-1){
                // 적 전방 타워 남아있는 라인으로 지원
                for(let wi=0;wi<3;wi++){
                  if(wi===u.laneIdx) continue;
                  const eHp=G.enemyTowerHp[wi];
                  if(eHp>0&&eHp<worstHp){worstHp=eHp;worstLane=wi;}
                }
              }
              if(worstLane!==-1){
                u._roaming=true;
                u._roamTarget=worstLane;
                u.laneIdx=worstLane; // 라인 전환
                u.reachedLane=false; // 라인 Y 재설정 트리거
                u.atBaseGate=false;
                toast('🔀 ['+LANE_NAMES[u.laneIdx]+'] 라인 지원!','good');
              }
            }
          }
        } else {
          // 적이 아군 타워 공격
          G.allyTowerHp[u.laneIdx]=Math.max(0,G.allyTowerHp[u.laneIdx]-u.atk*0.55*shield);
          spawnHit(gateX,laneY(u.laneIdx),'#ff4560',Math.round(u.atk*0.55));
        }
      }
    } else {
      // 전진
      u.atBaseGate=false;

      // ★ 로밍 유닛: 기지 방향으로 복귀 후 새 라인으로 이동 ★
      if(u._roaming && u.side===0 && u.reachedLane){
        const homeX=ALLY_BASE_X+BASE_W/2+10;
        const distHome=Math.abs(u.x-homeX);
        if(distHome>30){
          // 기지로 복귀 중
          u.x-=u.spd*dt*1.2;
          u.y=laneY(u.laneIdx);
          return; // forEach 콜백에서 return = continue
        } else {
          // 기지 도착 → 새 라인 진입
          u._roaming=false;
          u.reachedLane=false;
          u.x=homeX;
        }
      }

      const dir=u.side===0?1:-1;
      const blocked=G.units.some(o=>o.side!==u.side&&o.hp>0&&o.laneIdx===u.laneIdx&&o.reachedLane&&Math.abs(u.x-o.x)<(u.ninja?22:30));
      if(!blocked) u.x+=dir*u.spd*dt;
      else if(u.ninja) u.x+=dir*u.spd*dt*2.2;
    }
    // Y 스냅 (라인 유지)
    u.y=laneY(u.laneIdx);
  });
  G.units=G.units.filter(u=>u.hp>0);
}

function killUnit(unit,killerSide){
  if(unit.hp<=0) return;
  G.score+=unit.reward*G.wave*(killerSide===0?G.combo:1);
  if(killerSide===0){G.kills++;addKillFeed(unit);}
  G.resources=Math.min(G.resources+Math.floor(unit.reward*0.38),900);
  spawnDeath(unit.x,unit.y,unit.isBoss||unit.isMiniBoss);
  if(unit.isBoss){toast('💀 보스 처치!','gold');spawnFireworks();}
  else if(unit.isMiniBoss){toast('😈 미니보스 처치!','gold');}
  unit.hp=0;
}

function updateBullets(dt){
  G.bullets.forEach(b=>{
    const dx=b.tx-b.x,dy=b.ty-b.y,d=Math.sqrt(dx*dx+dy*dy);
    if(d<b.spd*dt*2){
      const t=G.units.find(u=>u.uid===b.targetId&&u.hp>0);
      if(t){
        t.hp-=b.dmg;spawnHit(t.x,t.y,b.col,b.dmg);
        if(t.hp<=0)killUnit(t,b.fromSide===0?0:1);
        if(b.pierce<b.maxPierce){
          b.pierce++;
          const ne=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==b.targetId).sort((a,c)=>Math.abs(a.x-(t.x+30))-Math.abs(c.x-(t.x+30)));
          if(ne.length>0){const nt=ne[0];b.tx=nt.x;b.ty=nt.y-18;b.targetId=nt.uid;b.x=t.x;b.y=t.y-18;return;}
        }
      }
      b.done=true;
    } else {b.x+=dx/d*b.spd*dt;b.y+=dy/d*b.spd*dt;}
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
  if(dmg>0) for(let i=0;i<3;i++) G.particles.push({x,y:y-15,vx:(Math.random()-.5)*2,vy:-Math.random()*2,col,life:15,size:2+Math.random()*2});
}
function spawnDeath(x,y,big){
  const cnt=big?24:9;
  for(let i=0;i<cnt;i++){
    const ang=Math.random()*Math.PI*2,spd=1+Math.random()*3;
    G.particles.push({x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd-2,col:big?'#ffd700':'#ff4560',life:22+Math.random()*20,size:big?6:3});
    G.effects.push({x:x+(Math.random()-.5)*30,y:y+(Math.random()-.5)*30,r:2,col:big?'#ffd700':'#ff4560',alpha:0.8,type:'death'});
  }
}
function airstrikeBomb(x,y,laneIdx){
  G.effects.push({x,y,r:5,col:'#ff8c42',alpha:1,type:'bomb'});
  G.units.filter(u=>u.side===1&&u.laneIdx===laneIdx&&Math.abs(u.x-x)<65).forEach(u=>{
    const dmg=Math.round((110+G.wave*22)*(G.snipeDmgBonus||1));
    u.hp-=dmg;spawnHit(u.x,u.y,'#ff8c42',dmg);if(u.hp<=0)killUnit(u,0);
  });
  G.enemyTowerHp[laneIdx]=Math.max(0,G.enemyTowerHp[laneIdx]-35);
  for(let i=0;i<10;i++) G.particles.push({x:x+(Math.random()-.5)*45,y,vx:(Math.random()-.5)*4,vy:-Math.random()*5,col:'#ff8c42',life:28+Math.random()*15,size:4});
}

// ═══════════════════════════════════
//  SNIPER
// ═══════════════════════════════════
function tryShoot(mx,my){
  if(!G.running) return;
  if(G.reloading){toast('🔫 재장전 중!','bad');return;}

  const HITBOX=44, HEADBOX=19;
  let hit=null,bestPri=-1,isHeadshot=false;
  G.units.forEach(u=>{
    if(u.side!==1||u.hp<=0||!u.reachedLane) return;
    const uy=u.y-18, headY=u.y-31;
    const bd=Math.sqrt((mx-u.x)**2+(my-uy)**2);
    const hd=Math.sqrt((mx-u.x)**2+(my-headY)**2);
    if(bd<HITBOX&&u.pri>=bestPri){bestPri=u.pri;hit=u;isHeadshot=(hd<HEADBOX);}
  });

  const isCrit=Math.random()<(G.critBonus||0);
  const baseDmg=(140+G.diff*40)*(G.snipeDmgBonus||1)*(G.weather.id==='night'?0.82:1);

  if(hit){
    let dmg=Math.round(baseDmg*(hit.isBoss?0.48:1)*G.combo);
    let dmgLabel='';
    if(isHeadshot){dmg=Math.round(dmg*1.65);dmgLabel+=' 🎯헤드샷!';}
    if(isCrit){dmg=Math.round(dmg*1.45);dmgLabel+=' 💥크리티컬!';}

    const pierceMax=G.pierceCount-1;
    G.bullets.push({x:mx,y:my,tx:hit.x,ty:hit.y-18,col:isHeadshot?'#ffd700':'#ff4560',dmg,targetId:hit.uid,fromSide:0,spd:30,pierce:0,maxPierce:pierceMax});

    if(G.multiSnipe){
      const nearby=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==hit.uid&&u.laneIdx===hit.laneIdx&&Math.abs(u.x-hit.x)<80);
      nearby.slice(0,3).forEach(u=>{const sd=Math.round(dmg*0.42);setTimeout(()=>{if(u.hp>0){u.hp-=sd;spawnHit(u.x,u.y,'#ff8c42',sd);if(u.hp<=0)killUnit(u,0);}},80);});
    }
    if(G.aoeSnipe){
      G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==hit.uid&&Math.sqrt((u.x-hit.x)**2+(u.y-hit.y)**2)<38).forEach(u=>{
        const ad=Math.round(dmg*0.35);setTimeout(()=>{if(u.hp>0){u.hp-=ad;spawnHit(u.x,u.y,'#b26cf7',ad);if(u.hp<=0)killUnit(u,0);}},60);
      });
    }

    G.snipes++;
    G.score+=Math.round(95*G.wave*G.combo*(isHeadshot?2:1));
    G.combo=Math.min(G.combo+1,12);G.comboTimer=190;
    document.getElementById('combo-val').textContent='×'+G.combo;

    if(isHeadshot){
      G.headshots++;
      const fl=document.getElementById('hs-flash');fl.style.background='rgba(255,215,0,0.13)';
      setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},150);
      const w=document.getElementById('twrap');
      const d=document.createElement('div');d.className='hs-toast';
      d.textContent='🎯 헤드샷! ×1.65 피해'+dmgLabel;
      w.insertBefore(d,w.firstChild);setTimeout(()=>d.remove(),2200);
    } else {
      toast('🎯 ['+LANE_NAMES[hit.laneIdx]+'] '+hit.name+' -'+dmg+'HP ×'+G.combo+dmgLabel,'gold');
    }

    G.effects.push({x:hit.x,y:hit.y,r:6,col:isHeadshot?'#ffd700':'#ff4560',alpha:0.9,type:'snipe'});
    G.reloading=true;G.reloadTimer=0;
    G.reloadMax=Math.max(32,80-G.combo*4);

  } else {
    // 적 기지 직격 체크 (각 라인 게이트 근처)
    let hitGate=false;
    for(let li=0;li<3;li++){
      const gx=enemyGateX(), gy=allyGateY(li);
      if(mx>ENEMY_BASE_X-BASE_W/2-20&&Math.abs(my-gy)<30){
        const dmg=Math.round((45+G.diff*14)*(G.snipeDmgBonus||1));
        G.enemyTowerHp[li]=Math.max(0,G.enemyTowerHp[li]-dmg);
        toast('💥 '+LANE_NAMES[li]+' 타워 직격! -'+dmg,'good');
        G.effects.push({x:gx,y:gy,r:10,col:'#ff8c42',alpha:0.9,type:'snipe'});
        G.reloading=true;G.reloadTimer=0;G.reloadMax=70;
        G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';
        hitGate=true;break;
      }
    }
    if(!hitGate){G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';}
  }
}

// ═══════════════════════════════════
//  ABILITIES / SHOP
// ═══════════════════════════════════
function useAbility(i){if(!G.running)return;const a=G.abilities[i];if(a.cd>0){toast('쿨다운 중!','bad');return;}ABILITY_DEFS[i].fx();a.cd=a.maxCd;}
function openShop(){
  document.getElementById('shop-res').textContent=Math.floor(G.resources);
  const grid=document.getElementById('shop-grid');grid.innerHTML='';
  SHOP_ITEMS.forEach(item=>{
    const bought=shopBoughtItems.has(item.id)&&!item.repeatable;
    const div=document.createElement('div');div.className='shop-item'+(bought?' bought':'');
    div.innerHTML=`<span class="sem">${item.em}</span><span class="sname">${item.name}</span><span class="sdesc">${item.desc}</span><span class="scost">${bought?'구매완료':'💎'+item.cost}</span>`;
    if(!bought)div.onclick=()=>buyShopItem(item);
    grid.appendChild(div);
  });
  document.getElementById('shop-modal').style.display='flex';
}
function closeShop(){document.getElementById('shop-modal').style.display='none';}
function buyShopItem(item){
  if(G.resources<item.cost){toast('💎 자원 부족!','bad');return;}
  G.resources-=item.cost;item.fx();
  if(!item.repeatable)shopBoughtItems.add(item.id);
  openShop();updateHUD();
}

// ═══════════════════════════════════
//  RENDER
// ═══════════════════════════════════
function render(){
  if(W===0||H===0) return;
  ctx.clearRect(0,0,W,H);

  const isNight=G.weather.night;

  // Sky (전체 배경)
  const sky=ctx.createLinearGradient(0,0,0,H);
  if(isNight){sky.addColorStop(0,'#010510');sky.addColorStop(1,'#0a1628');}
  else if(G.weather.id==='fog'){sky.addColorStop(0,'#1a2035');sky.addColorStop(1,'#2a3555');}
  else{sky.addColorStop(0,'#060a18');sky.addColorStop(1,'#152035');}
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

  // Stars
  if(isNight||G.weather.id==='fog'){
    ctx.fillStyle='rgba(255,255,255,0.7)';
    for(let i=0;i<80;i++){const sx=(i*137.5+G.frame*.01)%W,sy=(i*97.3)%(H*.4);const sz=.6+Math.sin(G.frame*.06+i)*.4;ctx.beginPath();ctx.arc(sx,sy,sz,0,Math.PI*2);ctx.fill();}
  }

  drawMountains();

  // ─── 라인 경로 그리기 (기지 → 라인 → 기지) ───
  drawLanePaths();

  // 기지 그리기
  drawBase(ALLY_BASE_X,  '🏰','#10d96e', G.allyTowerHp,  true);
  drawBase(ENEMY_BASE_X, '🏯','#ff4560', G.enemyTowerHp, false);

  // Rain
  if(G.weather.rain){
    ctx.strokeStyle='rgba(150,180,255,0.28)';ctx.lineWidth=1.2;
    rainDrops.forEach(d=>{d.y+=d.spd;d.x+=1.5;if(d.y>H){d.y=-10;d.x=Math.random()*W;}ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x-3,d.y+d.len);ctx.stroke();});
  }
  if(G.weather.id==='fog'||G.weather.id==='storm'){
    const fogG=ctx.createLinearGradient(0,0,W,0);
    fogG.addColorStop(0,'rgba(180,200,220,0.07)');fogG.addColorStop(.4+Math.sin(G.frame*.005)*.1,'rgba(180,200,220,0.17)');fogG.addColorStop(1,'rgba(180,200,220,0.05)');
    ctx.fillStyle=fogG;ctx.fillRect(0,0,W,H);
  }
  if(G.freezeEnd>0&&G.frame<G.freezeEnd){
    const fPct=Math.max(0,1-(G.frame-(G.freezeEnd-240))/240);
    ctx.fillStyle='rgba(100,180,255,'+(0.07*fPct)+')';ctx.fillRect(0,0,W,H);
  }

  // Shield glow
  if(G.shieldEnd>0&&G.frame<G.shieldEnd){
    const pulse=0.4+Math.sin(G.frame*.15)*.3;
    ctx.shadowBlur=30;ctx.shadowColor='rgba(34,211,238,'+pulse+')';
    ctx.strokeStyle='rgba(34,211,238,'+pulse+')';ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(ALLY_BASE_X,H*.5,60,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;
  }

  // 크레이터
  G.craters.forEach(cr=>{
    ctx.fillStyle='rgba(0,0,0,0.3)';
    ctx.beginPath();ctx.ellipse(cr.x,cr.y+cr.r*.3,cr.r,cr.r*.38,0,0,Math.PI*2);ctx.fill();
  });

  // Effects
  G.effects.forEach(e=>{
    ctx.globalAlpha=Math.max(0,e.alpha);
    if(e.type==='bomb'){ctx.shadowBlur=30;ctx.shadowColor='#ff8c42';ctx.fillStyle='rgba(255,140,66,'+e.alpha+')';ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
    else{ctx.strokeStyle=e.col;ctx.lineWidth=e.type==='snipe'?3.5:e.type==='death'?1.5:1.8;ctx.shadowBlur=e.type==='snipe'?20:0;ctx.shadowColor=e.col;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;}
    ctx.globalAlpha=1;
  });

  // Units (Z-sort by Y)
  G.units.filter(u=>u.hp>0).sort((a,b)=>a.y-b.y).forEach(drawUnit);

  // Bullets
  G.bullets.forEach(b=>{
    ctx.shadowBlur=8;ctx.shadowColor=b.col;
    ctx.fillStyle=b.col;
    const bsize=b.col==='#ffd700'?6:b.col==='#b26cf7'?4.5:4;
    ctx.beginPath();ctx.arc(b.x,b.y,bsize,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  });

  // Particles
  G.particles.forEach(p=>{ctx.globalAlpha=Math.min(1,p.life/10);ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;});

  // Vignette
  if(!G.reloading&&G.running&&G.mouseX>0){
    const vg=ctx.createRadialGradient(G.mouseX,G.mouseY,55,G.mouseX,G.mouseY,Math.max(W,H)*.72);
    vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,0.4)');
    ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  }

  // Headshot hint
  if(!G.reloading&&G.running){
    const hovered=G.units.find(u=>u.side===1&&u.hp>0&&u.reachedLane&&Math.sqrt((G.mouseX-u.x)**2+(G.mouseY-(u.y-18))**2)<44);
    if(hovered){ctx.strokeStyle='rgba(255,215,0,0.4)';ctx.lineWidth=1.5;ctx.setLineDash([3,3]);ctx.beginPath();ctx.arc(hovered.x,hovered.y-31,19,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);}
  }
}

// ─── 라인 경로 그리기 ───
function drawLanePaths(){
  const agx=allyGateX(), egx=enemyGateX();
  for(let li=0;li<3;li++){
    const agy=allyGateY(li);
    const egy=enemyGateY(li);
    const ly=laneY(li);
    const lc=LANE_COLS[li];
    const isFocus=(li===G.botFocusLane);
    const isSel=(li===G.selectedLane);

    // 라인 배경 (지면)
    const bandTop=li===0?0:(li===1?laneY(0)+28:laneY(1)+28);
    const bandBot=li===2?H:(li===1?laneY(1)+28:laneY(0)+28);
    const bh=li===0?ly+40:li===2?H-(ly-40):80;
    ctx.fillStyle='rgba(20,35,12,0.55)';
    if(li===0) ctx.fillRect(agx,0,egx-agx,ly+35);
    else if(li===2) ctx.fillRect(agx,ly-35,egx-agx,H-(ly-35));
    else ctx.fillRect(agx,ly-38,egx-agx,76);

    // 경로 라인 (기지 게이트 → 라인 → 기지 게이트)
    // 경로: (agx, agy) → (agx+60, ly) → (egx-60, ly) → (egx, egy)
    const mx1=agx+65, mx2=egx-65;
    ctx.beginPath();
    ctx.moveTo(agx, agy);
    ctx.bezierCurveTo(mx1, agy, mx1, ly, mx1, ly);
    ctx.lineTo(mx2, ly);
    ctx.bezierCurveTo(mx2, ly, mx2, egy, egx, egy);

    const alpha=isFocus?0.85:isSel?0.7:0.35;
    ctx.strokeStyle=isFocus?'rgba(255,69,96,'+alpha+')':lc.replace('#','rgba(').replace(/(..)(..)(..)/, (m,r,g,b)=>`rgba(${parseInt(r,16)},${parseInt(g,16)},${parseInt(b,16)},`)+alpha+')';

    // 더 간단하게
    ctx.strokeStyle=isFocus?`rgba(255,69,96,${alpha})`:`${lc}${Math.round(alpha*255).toString(16).padStart(2,'0')}`;
    ctx.lineWidth=isFocus?3.5:isSel?3:1.8;
    ctx.setLineDash(isFocus?[]:[6,6]);
    ctx.stroke();
    ctx.setLineDash([]);

    // 지면 풀 (경로 아래 선)
    ctx.strokeStyle=isSel?lc+'aa':'rgba(80,140,40,0.25)';
    ctx.lineWidth=isSel?2:1;
    ctx.beginPath();ctx.moveTo(mx1,ly);ctx.lineTo(mx2,ly);ctx.stroke();

    // 라인 레이블
    const lbl=LANE_NAMES[li]+(isSel?' ◀':'');
    ctx.fillStyle=isSel?lc:isFocus?'#ff4560':'rgba(255,255,255,0.35)';
    ctx.font=`bold ${isSel?13:11}px "Noto Sans KR"`;
    ctx.textAlign='center';
    ctx.fillText(lbl,(mx1+mx2)/2,ly-10);
    if(isFocus&&!isSel){ctx.fillStyle='rgba(255,69,96,0.7)';ctx.font='bold 10px sans-serif';ctx.fillText('⚠️',mx1+(mx2-mx1)*.7,ly-10);}
    ctx.textAlign='left';

    // 타워 HP 바 (라인 경로 시작/끝에 표시)
    const barW=55, barH=5;
    // 아군 타워 HP (왼쪽 경로 시작)
    const aHpPct=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp);
    ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(mx1-barW/2,ly+8,barW,barH);
    ctx.fillStyle=aHpPct>0.5?'#10d96e':aHpPct>0.25?'#ffd700':'#ff4560';
    ctx.fillRect(mx1-barW/2,ly+8,barW*aHpPct,barH);
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=0.5;ctx.strokeRect(mx1-barW/2,ly+8,barW,barH);
    // 적 타워 HP (오른쪽 경로 끝)
    const eHpPct=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp);
    ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(mx2-barW/2,ly+8,barW,barH);
    ctx.fillStyle=eHpPct>0.5?'#ff4560':eHpPct>0.25?'#ffd700':'#10d96e';
    ctx.fillRect(mx2-barW/2,ly+8,barW*eHpPct,barH);
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=0.5;ctx.strokeRect(mx2-barW/2,ly+8,barW,barH);
  }
}

function drawMountains(){
  ctx.fillStyle='rgba(10,18,38,0.65)';
  ctx.beginPath();ctx.moveTo(0,H*.3);
  for(let x=0;x<=W;x+=80) ctx.lineTo(x,H*.3-40-Math.sin(x*.01)*30-Math.sin(x*.025)*18);
  ctx.lineTo(W,H*.3);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(12,22,44,0.45)';
  ctx.beginPath();ctx.moveTo(0,H*.3);
  for(let x=0;x<=W;x+=55) ctx.lineTo(x,H*.3-20-Math.sin(x*.018+1)*18-Math.sin(x*.04)*10);
  ctx.lineTo(W,H*.3);ctx.closePath();ctx.fill();
}

// 기지 그리기 — 3개 라인 게이트 포함
function drawBase(cx, em, col, towerHps, isAlly){
  const bx=isAlly?cx-BASE_W/2:cx-BASE_W/2, by=H*.5-BASE_H/2;

  // 기지 본체
  ctx.shadowBlur=24;ctx.shadowColor=col;
  ctx.fillStyle='rgba(12,22,46,0.95)';ctx.strokeStyle=col;ctx.lineWidth=2.4;
  rr(ctx,bx,by,BASE_W,BASE_H,8);ctx.fill();ctx.stroke();ctx.shadowBlur=0;

  // 기지 전체 HP 바
  const totalHp=towerHps.reduce((s,h)=>s+h,0);
  const totalMax=G.maxTowerHp*3;
  const hbw=BASE_W-10;
  ctx.fillStyle='rgba(0,0,0,0.55)';rr(ctx,bx+5,by+7,hbw,9,4);ctx.fill();
  const hcol=(totalHp/totalMax)>0.5?col:(totalHp/totalMax)>0.25?'#ffd700':'#ff4560';
  ctx.fillStyle=hcol;rr(ctx,bx+5,by+7,Math.max(0,hbw*(totalHp/totalMax)),9,4);ctx.fill();

  // 기지 아이콘
  ctx.font='24px sans-serif';ctx.textAlign='center';ctx.fillText(em,bx+BASE_W/2,by+BASE_H-16);

  // 3개 라인 게이트 (기지 측면)
  for(let li=0;li<3;li++){
    const gy=allyGateY(li);
    const hpPct=Math.max(0,towerHps[li]/G.maxTowerHp);
    const lc=LANE_COLS[li];
    const gateX=isAlly?bx+BASE_W:bx;

    // 게이트 포트 표시
    ctx.fillStyle=hpPct>0.5?lc:hpPct>0.25?'#ffd700':'#ff4560';
    ctx.shadowBlur=hpPct>0.25?6:12;ctx.shadowColor=ctx.fillStyle;
    ctx.beginPath();ctx.arc(gateX,gy,5,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;

    // 라인 HP 작은 바
    const lbw=BASE_W-16, lbh=3;
    const lby=by+16+li*(BASE_H-22)/3;
    ctx.fillStyle='rgba(0,0,0,0.45)';ctx.fillRect(bx+8,lby,lbw,lbh);
    ctx.fillStyle=hpPct>0.5?lc:hpPct>0.25?'#ffd700':'#ff4560';
    ctx.fillRect(bx+8,lby,lbw*hpPct,lbh);
  }

  // 터렛
  if(isAlly&&G.turretLevel>0){
    ctx.fillStyle='#b26cf7';ctx.shadowBlur=10;ctx.shadowColor='#b26cf7';
    ctx.fillRect(bx+BASE_W/2-4,by-20,8,14);ctx.fillRect(bx+BASE_W/2-2,by-26,4,8);ctx.shadowBlur=0;
    ctx.font='bold 9px sans-serif';ctx.fillStyle='#b26cf7';ctx.textAlign='center';ctx.fillText('Lv'+G.turretLevel,bx+BASE_W/2,by-30);
  }

  // HP 수치
  ctx.font='bold 8px sans-serif';ctx.fillStyle='rgba(255,255,255,0.55)';ctx.textAlign='center';
  ctx.fillText(Math.round(Math.max(0,totalHp)),bx+BASE_W/2,by+BASE_H+12);
}

function drawUnit(u){
  const x=u.x,y=u.y;
  const col=u.side===0?'#22d3ee':'#ff4560';
  const bounce=Math.sin(u.anim)*2.2;
  const scale=u.isBoss?1.7:u.isMiniBoss?1.35:1;
  const frozen=(G.freezeEnd>0&&G.frame<G.freezeEnd&&u.side===1);

  ctx.fillStyle='rgba(0,0,0,0.22)';
  ctx.beginPath();ctx.ellipse(x,y+2,13*scale,4*scale,0,0,Math.PI*2);ctx.fill();

  const r=14*scale;
  ctx.fillStyle=frozen?'rgba(30,60,120,0.9)':u.side===0?'rgba(0,45,75,0.88)':'rgba(75,0,20,0.88)';
  ctx.strokeStyle=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'#4dacf7':col;
  ctx.lineWidth=u.isBoss?2.5:u.isMiniBoss?2:1.8;
  ctx.shadowBlur=u.isBoss?18:u.isMiniBoss?12:7;
  ctx.shadowColor=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'rgba(100,180,255,0.8)':col;
  ctx.beginPath();ctx.arc(x,y-r+bounce,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.shadowBlur=0;

  ctx.font=(u.isBoss?'22':u.isMiniBoss?'18':'14')+'px sans-serif';ctx.textAlign='center';
  ctx.fillText(u.em,x,y-r+bounce+5);

  if(u.isBoss){ctx.font='bold 10px "Noto Sans KR"';ctx.fillStyle='#ffd700';ctx.fillText('💀 BOSS',x,y-r*2+bounce-4);}
  if(u.isMiniBoss){ctx.font='bold 9px "Noto Sans KR"';ctx.fillStyle='#ff8c42';ctx.fillText('😈 MINI',x,y-r*2+bounce-4);}

  if(frozen){
    ctx.strokeStyle='rgba(100,220,255,0.5)';ctx.lineWidth=1;
    for(let i=0;i<4;i++){const ang=(i/4)*Math.PI*2;ctx.beginPath();ctx.moveTo(x,y-r+bounce);ctx.lineTo(x+Math.cos(ang)*(r+6),y-r+bounce+Math.sin(ang)*(r+6));ctx.stroke();}
  }

  // 기지 공격 중 표시
  if(u.atBaseGate){
    ctx.strokeStyle=u.side===0?'#22d3ee':'#ff4560';ctx.lineWidth=1.5;ctx.setLineDash([2,3]);
    ctx.beginPath();ctx.arc(x,y-r+bounce,r+5,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
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

// ═══════════════════════════════════
//  HUD
// ═══════════════════════════════════
function updateHUD(){
  if(!G.running) return;
  const totalAlly=G.allyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalEnemy=G.enemyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalMax=G.maxTowerHp*3;
  document.getElementById('ally-hp-val').textContent=Math.round(totalAlly);
  document.getElementById('enemy-hp-val').textContent=Math.round(totalEnemy);
  document.getElementById('ally-hp-bar').style.width=(totalAlly/totalMax*100)+'%';
  document.getElementById('enemy-hp-bar').style.width=(totalEnemy/totalMax*100)+'%';
  document.getElementById('res-val').textContent=Math.floor(G.resources);
  document.getElementById('score-val').textContent=G.score.toLocaleString();
  document.getElementById('kills-val').textContent=G.kills;
}

function updateLaneStatus(){
  if(!G.lanes&&!G.allyTowerHp) return;
  for(let li=0;li<3;li++){
    const aHp=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp*100);
    const eHp=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp*100);
    const af=document.getElementById('ls-ally-'+li);
    const ef=document.getElementById('ls-enemy-'+li);
    if(af) af.style.width=aHp*.48+'%';
    if(ef) ef.style.width=eHp*.48+'%';
    const ally=G.units.filter(u=>u.side===0&&u.hp>0&&u.laneIdx===li).length;
    const enemy=G.units.filter(u=>u.side===1&&u.hp>0&&u.laneIdx===li).length;
    const uel=document.getElementById('ls-units-'+li);
    if(uel) uel.textContent=ally+'v'+enemy;
  }
}

function updateButtons(){
  for(let i=0;i<9;i++){
    const btn=document.getElementById('btn'+i);
    if(!btn) continue;
    btn.disabled=!G.running||G.resources<UNIT_DEFS[i].cost||G.trainCooldowns[i]>0;
  }
}

// ═══════════════════════════════════
//  KILL FEED
// ═══════════════════════════════════
function addKillFeed(unit){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kf-item';
  d.textContent='['+LANE_NAMES[unit.laneIdx]+'] 🎯 '+unit.em+' '+unit.name+(unit.isBoss?' 🏆':unit.isMiniBoss?' 👑':'');
  d.style.borderColor=unit.isBoss?'rgba(255,215,0,.6)':unit.isMiniBoss?'rgba(255,140,66,.5)':'rgba(255,69,96,.3)';
  d.style.color=unit.isBoss?'#ffd700':unit.isMiniBoss?'#ff8c42':'var(--text)';
  kf.insertBefore(d,kf.firstChild);
  setTimeout(()=>d.remove(),3000);
  while(kf.children.length>5)kf.removeChild(kf.lastChild);
}

// ═══════════════════════════════════
//  GAME END
// ═══════════════════════════════════
function endGame(win){
  if(!G.running) return;
  G.running=false;
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';
  const maxScore=G.wave*1200*(G.diff+1);
  const ratio=G.score/Math.max(maxScore,1);
  const grade=win?(ratio>0.8?'S':ratio>0.6?'A':ratio>0.4?'B':'C'):'D';
  const gradeCol={S:'#ffd700',A:'#10d96e',B:'#4dabf7',C:'#ff8c42',D:'#ff4560'}[grade];
  const rs=document.getElementById('result');rs.style.display='flex';
  document.getElementById('res-grade').textContent=grade;
  document.getElementById('res-grade').style.color=gradeCol;
  document.getElementById('res-title').textContent=win?'🏆 승리!':'💀 패배...';
  document.getElementById('res-title').style.color=win?'#10d96e':'#ff4560';
  document.getElementById('res-subtitle').textContent=DIFF_CONFIG[G.diff].name+' · 웨이브 '+G.wave+' · 등급 '+grade+' · 헤드샷 '+G.headshots+'회';
  document.getElementById('st-score').textContent=G.score.toLocaleString();
  document.getElementById('st-kills').textContent=G.kills;
  document.getElementById('st-wave').textContent=G.wave;
  document.getElementById('st-snipes').textContent=G.snipes;
  if(win)spawnFireworks();
  try{window.parent.postMessage({type:'sniper_result',score:G.score,kills:G.kills,wave:G.wave,snipes:G.snipes,win:win?1:0,diff:G.diff},'*');}catch(e){}
}

function spawnFireworks(){
  const bg=document.getElementById('fw');
  const cols=['#ffd700','#ff4560','#4dabf7','#10d96e','#b26cf7','#22d3ee'];
  for(let f=0;f<14;f++) setTimeout(()=>{
    const x=10+Math.random()*80,y=5+Math.random()*55,col=cols[f%6];
    for(let i=0;i<28;i++){
      const p=document.createElement('div');
      const ang=(i/28)*Math.PI*2,dist=55+Math.random()*110,dur=.55+Math.random()*.65;
      p.style.cssText='position:absolute;left:'+x+'%;top:'+y+'%;width:5px;height:5px;border-radius:50%;background:'+col+';animation:fwp '+dur+'s ease-out forwards;--dx:'+Math.cos(ang)*dist+'px;--dy:'+Math.sin(ang)*dist+'px;';
      bg.appendChild(p);setTimeout(()=>p.remove(),(dur+.1)*1000);
    }
  },f*350);
}

function toast(txt,type){
  const w=document.getElementById('twrap');
  const d=document.createElement('div');d.className='toast';
  const colors={good:'rgba(16,217,110,.4)',bad:'rgba(255,69,96,.4)',gold:'rgba(255,215,0,.4)',wave:'rgba(178,108,247,.4)'};
  d.style.borderColor=colors[type]||'rgba(255,255,255,.1)';
  d.textContent=txt;w.insertBefore(d,w.firstChild);
  setTimeout(()=>d.remove(),2800);
  while(w.children.length>5)w.removeChild(w.lastChild);
}

// ═══════════════════════════════════
//  EVENTS
// ═══════════════════════════════════
document.addEventListener('mousemove',e=>{
  const sc=document.getElementById('scope');sc.style.left=e.clientX+'px';sc.style.top=e.clientY+'px';
  if(G.running){const rect=canvas.getBoundingClientRect();G.mouseX=e.clientX-rect.left;G.mouseY=e.clientY-rect.top;}
  const col=G.reloading?'rgba(120,120,120,0.6)':'rgba(255,69,96,0.9)';
  sc.querySelectorAll('circle[stroke],line').forEach(el=>{if(el.getAttribute('stroke'))el.setAttribute('stroke',col);});
});

canvas.addEventListener('click',e=>{
  if(!G.running)return;
  const rect=canvas.getBoundingClientRect();
  tryShoot(e.clientX-rect.left,e.clientY-rect.top);
});

document.addEventListener('keydown',e=>{
  if(!G.running)return;
  if(['1','2','3','4','5','6','7','8','9','q','e','r','w','t','s','f','g','h'].includes(e.key.toLowerCase()))e.preventDefault();
  const keys={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8};
  if(keys[e.key]!==undefined){spawnAlly(parseInt(e.key)-1);return;}
  if(e.key.toLowerCase()==='q')useAbility(0);
  if(e.key.toLowerCase()==='e')useAbility(1);
  if(e.key.toLowerCase()==='r')useAbility(2);
  if(e.key.toLowerCase()==='w')useAbility(3);
  if(e.key.toLowerCase()==='t')useAbility(4);
  if(e.key.toLowerCase()==='s')openShop();
  // 라인 전환: F=탑, G=미드, H=봇
  if(e.key.toLowerCase()==='f')selectLane(0);
  if(e.key.toLowerCase()==='g')selectLane(1);
  if(e.key.toLowerCase()==='h')selectLane(2);
});

let selDiff=0;
document.querySelectorAll('.diff-card').forEach(card=>{
  card.addEventListener('click',()=>{
    document.querySelectorAll('.diff-card').forEach(c=>c.classList.remove('sel'));
    card.classList.add('sel');selDiff=parseInt(card.dataset.d);
  });
});
document.getElementById('start-btn').addEventListener('click',()=>startGame(selDiff));

window.addEventListener('resize',()=>{if(G.running)resize();});
</script>
</body>
</html>"""


def render():
    import os as _os
    from utils.database import update_leaderboard, _get_col
    from utils.config import USERS_FILE

    st.markdown("<style>iframe{border:none!important;border-radius:14px;}</style>", unsafe_allow_html=True)
    st.caption("🎯 마우스: 조준 | 클릭: 발사 | R: 재장전 | 스테이지 클리어로 진행")

    _cur_uid = st.session_state.get('logged_in_user', '')

    _bridge_dir = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'components', 'game_bridge')
    _bridge = st.components.v1.declare_component("game_bridge_sniper", path=_bridge_dir)
    _result = _bridge(key=f"bridge_sniper_{_cur_uid}", default=None)

    if _result and isinstance(_result, dict) and _result.get('type') == 'sniper_result':
        if not st.session_state.get('_sniper_saved'):
            st.session_state['_sniper_saved'] = True
            try:
                _s_score = int(_result.get('score', 0))
                _s_kills = int(_result.get('kills', 0))
                _s_wave  = int(_result.get('wave', 1))
                if _s_score > 0 and _cur_uid:
                    _col = _get_col(USERS_FILE)
                    _doc = _col.find_one({"_id": "main"}, {_cur_uid: 1})
                    if _doc and _cur_uid in _doc:
                        _udata = _doc[_cur_uid]
                        if _s_score > _udata.get('game_records', {}).get('sniper', {}).get('score', 0):
                            _col.update_one({"_id": "main"}, {"$set": {
                                f"{_cur_uid}.game_records.sniper.score": _s_score,
                                f"{_cur_uid}.game_records.sniper.kills": _s_kills,
                                f"{_cur_uid}.game_records.sniper.wave":  _s_wave,
                            }})
                            update_leaderboard('sniper', _udata.get('nickname', _cur_uid), _s_score)
                            st.toast(f"🎯 저격전 최고기록 {_s_score:,}점 저장!", icon="🏆")
                            st.rerun()
            except Exception as _e:
                import logging; logging.error(f"[sniper save] {_e}")
    if not _result:
        st.session_state.pop('_sniper_saved', None)

    components.html(GAME_HTML, height=920, scrolling=False)
