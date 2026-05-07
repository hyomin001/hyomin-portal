import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스나이퍼 엘리트 ULTRA — 전장의 저격수</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@400;600;700;900&family=Rajdhani:wght@400;500;600;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
:root{
  --red:#ff2244;--red2:#ff6680;--green:#00ff88;--green2:#00cc66;
  --gold:#f5c518;--gold2:#ffd966;--cyan:#00d4ff;--cyan2:#80eaff;
  --bg:#04060a;--bg2:#080e14;--bg3:#0c1a24;
  --panel:rgba(6,12,20,0.92);--border:rgba(0,200,255,0.12);
  --border2:rgba(0,200,255,0.25);--border3:rgba(0,200,255,0.5);
  --text:#c8dde8;--textDim:#4a6a7a;
  --allyBlue:#3388ff;--enemyRed:#ff3322;
  --scope:rgba(0,255,100,0.85);--scopeDim:rgba(0,255,100,0.35);
}
html,body{width:100%;height:800px;overflow:hidden;background:var(--bg);
  font-family:'Rajdhani',sans-serif;touch-action:none;cursor:crosshair;}
#root{position:relative;width:100%;height:800px;overflow:hidden;}
canvas{display:block;image-rendering:pixelated;}

/* ── SCANLINE OVERLAY ──────────── */
#scanlines{position:absolute;inset:0;pointer-events:none;z-index:9;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.08) 2px,rgba(0,0,0,0.08) 4px);
  mix-blend-mode:multiply;}

/* ── TOP HUD ──────────── */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;pointer-events:none;
  background:linear-gradient(180deg,rgba(4,6,10,0.97) 0%,rgba(4,6,10,0.8) 80%,transparent 100%);
  padding:8px 14px 16px;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--border);}

.hud-block{display:flex;flex-direction:column;align-items:center;
  background:rgba(0,200,255,0.04);border:1px solid var(--border);
  border-radius:6px;padding:4px 10px;min-width:58px;}
.hud-val{font-family:'Orbitron',sans-serif;font-size:15px;font-weight:700;
  color:var(--gold);line-height:1;letter-spacing:0.5px;}
.hud-lbl{font-size:8px;color:var(--textDim);letter-spacing:2px;margin-top:2px;font-family:'Share Tech Mono',monospace;}
.hud-val.pulse{animation:valPulse 0.3s ease;}
@keyframes valPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.2);color:#fff;}}

/* ── AMMO DISPLAY ──────────── */
#ammo-block{display:flex;flex-direction:column;align-items:center;gap:3px;padding:4px 10px;}
#ammo-bullets{display:flex;gap:3px;align-items:flex-end;}
.bullet-pip{width:5px;height:14px;border-radius:2px 2px 1px 1px;
  background:linear-gradient(180deg,var(--gold) 0%,#c8930a 100%);
  border:1px solid rgba(255,200,0,0.4);transition:all 0.2s;}
.bullet-pip.spent{background:rgba(255,255,255,0.06);border-color:rgba(255,255,255,0.08);}
.bullet-pip.reloading{animation:bulletLoad 0.3s ease forwards;}
@keyframes bulletLoad{from{transform:translateY(8px);opacity:0}to{transform:none;opacity:1}}

/* ── MISSION / BATTLE BAR ──────────── */
#battle-wrap{flex:1;margin:0 6px;display:flex;flex-direction:column;gap:4px;}
#battle-header{display:flex;justify-content:space-between;align-items:center;}
#mission-name{font-family:'Black Han Sans',sans-serif;font-size:12px;color:var(--cyan);letter-spacing:1px;}
#battle-info{font-size:10px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
#battle-track{height:8px;background:rgba(255,255,255,0.04);border-radius:99px;
  overflow:hidden;position:relative;border:1px solid var(--border);}
#ally-bar{height:100%;background:linear-gradient(90deg,#1144cc,#3388ff,#66aaff);
  transition:width 0.4s ease;box-shadow:0 0 8px rgba(51,136,255,0.6);}
#enemy-bar{position:absolute;top:0;right:0;height:100%;
  background:linear-gradient(270deg,#cc1100,#ff3322,#ff6644);
  transition:width 0.4s ease;box-shadow:0 0 8px rgba(255,51,34,0.6);}
#objective-row{display:flex;gap:8px;font-size:9px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
.obj-item{display:flex;align-items:center;gap:3px;}
.obj-dot{width:5px;height:5px;border-radius:50%;background:var(--textDim);}
.obj-item.done .obj-dot{background:var(--green);}
.obj-item.done{color:var(--green);}

/* ── HP BAR (ally health) ──────────── */
#hp-wrap{display:flex;flex-direction:column;gap:2px;width:90px;}
#hp-lbl{display:flex;justify-content:space-between;font-size:9px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
#hp-track{height:6px;background:rgba(255,255,255,0.04);border-radius:99px;overflow:hidden;border:1px solid var(--border);}
#hp-fill{height:100%;transition:width 0.3s,background 0.5s;border-radius:99px;}

/* ── SCOPE OVERLAY ──────────── */
#scope-wrap{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-blackout{position:absolute;inset:0;background:rgba(0,0,0,0.97);}
#scope-lens{position:absolute;border-radius:50%;overflow:hidden;
  left:50%;top:50%;transform:translate(-50%,-50%);
  width:320px;height:320px;
  box-shadow:0 0 0 2000px rgba(0,0,0,0.97),0 0 40px rgba(0,255,100,0.2),inset 0 0 30px rgba(0,0,0,0.5);}
#scope-cv{display:block;width:320px;height:320px;}
#scope-reticle{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:320px;height:320px;pointer-events:none;}
#scope-vignette{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:320px;height:320px;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,transparent 55%,rgba(0,0,0,0.8) 100%);}
#scope-bottom{position:absolute;bottom:13%;left:50%;transform:translateX(-50%);
  text-align:center;pointer-events:none;}
#scope-dist{font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--scope);letter-spacing:3px;margin-bottom:4px;}
#scope-state{font-size:10px;color:rgba(0,255,100,0.5);letter-spacing:2px;}
#breath-wrap{width:200px;margin:5px auto 0;}
#breath-track{height:4px;background:rgba(255,255,255,0.08);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:var(--green);border-radius:99px;transition:width 0.05s;}
.scope-corner{position:absolute;width:20px;height:20px;border-color:var(--scope);border-style:solid;opacity:0.6;}
.sc-tl{top:30px;left:30px;border-width:2px 0 0 2px;}
.sc-tr{top:30px;right:30px;border-width:2px 2px 0 0;}
.sc-bl{bottom:30px;left:30px;border-width:0 0 2px 2px;}
.sc-br{bottom:30px;right:30px;border-width:0 2px 2px 0;}

/* ── EFFECT OVERLAYS ──────────── */
#vignette-hit{position:absolute;inset:0;pointer-events:none;z-index:80;
  border-radius:4px;border:6px solid transparent;transition:border-color 0.1s,opacity 0.4s;}
#vignette-hit.flash{border-color:rgba(255,20,50,0.7);
  box-shadow:inset 0 0 80px rgba(255,0,40,0.3);opacity:1;}
#vignette-hit{opacity:0;}
#crit-flash{position:absolute;inset:0;pointer-events:none;z-index:79;
  background:rgba(255,220,0,0.12);opacity:0;transition:opacity 0.15s;}
#crit-flash.show{opacity:1;}
#night-overlay{position:absolute;inset:0;pointer-events:none;z-index:8;
  background:radial-gradient(ellipse at 50% 60%,transparent 22%,rgba(0,0,0,0.85) 70%);display:none;}

/* ── TOAST / KILL FEED ──────────── */
#toast{position:absolute;top:56px;left:50%;transform:translateX(-50%) translateY(-90px);
  background:var(--panel);border:1px solid var(--border2);
  border-radius:6px;padding:7px 20px;z-index:280;pointer-events:none;
  transition:transform 0.25s cubic-bezier(.34,1.56,.64,1);white-space:nowrap;
  font-size:11px;color:var(--gold);letter-spacing:1px;
  font-family:'Share Tech Mono',monospace;
  box-shadow:0 4px 20px rgba(0,0,0,0.6);}
#toast.show{transform:translateX(-50%) translateY(0);}

#killfeed{position:absolute;top:60px;right:10px;z-index:200;pointer-events:none;
  display:flex;flex-direction:column;gap:3px;max-width:260px;}
.kf{background:rgba(0,0,0,0.8);border-left:3px solid var(--red);border-radius:3px;
  padding:4px 10px;font-size:10px;color:#ccc;font-family:'Rajdhani',sans-serif;font-weight:600;
  animation:kfIn 0.3s cubic-bezier(.34,1.56,.64,1);letter-spacing:.5px;
  backdrop-filter:blur(4px);}
.kf.boss-kf{border-left-color:var(--gold);color:var(--gold2);}
.kf.ally-kf{border-left-color:var(--allyBlue);color:#88bbff;}
@keyframes kfIn{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}

/* ── DAMAGE NUMBERS ──────────── */
.dnum{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;
  animation:dUp 0.95s ease forwards;z-index:300;text-shadow:2px 2px 6px rgba(0,0,0,0.9);}
@keyframes dUp{
  0%{opacity:1;transform:translateY(0) scale(1);}
  30%{opacity:1;transform:translateY(-22px) scale(1.15);}
  100%{opacity:0;transform:translateY(-70px) scale(0.6);}}
.dnum.crit-num{animation:dCrit 0.95s ease forwards;}
@keyframes dCrit{
  0%{opacity:1;transform:translateY(0) scale(1.2) rotate(-3deg);}
  20%{transform:translateY(-18px) scale(1.5) rotate(2deg);}
  100%{opacity:0;transform:translateY(-80px) scale(0.5);}}

/* ── STATUS BAR (bottom) ──────────── */
#status-bar{position:absolute;bottom:0;left:0;right:0;z-index:100;pointer-events:none;
  background:linear-gradient(0deg,rgba(4,6,10,0.95) 0%,rgba(4,6,10,0.6) 80%,transparent 100%);
  padding:10px 14px 8px;display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid var(--border);font-family:'Share Tech Mono',monospace;font-size:10px;}
#status-left{display:flex;gap:14px;color:var(--textDim);}
.sl-item{display:flex;gap:4px;align-items:center;}
.sl-item .sv{color:var(--text);}
#status-right{display:flex;gap:10px;align-items:center;color:var(--textDim);}
#reload-bar{width:80px;height:4px;background:rgba(255,255,255,0.06);
  border-radius:99px;overflow:hidden;display:none;}
#reload-fill{height:100%;background:var(--gold);border-radius:99px;
  transition:width 0.05s linear;}
#wind-arrow{font-size:12px;transition:transform 0.5s;}

/* ── CONTROLS BAR ──────────── */
#ctrl-bar{position:absolute;top:62px;left:50%;transform:translateX(-50%);
  z-index:90;pointer-events:none;
  background:var(--panel);border:1px solid var(--border);
  border-radius:20px;padding:4px 14px;
  font-size:9px;color:var(--textDim);letter-spacing:1px;
  display:flex;gap:10px;align-items:center;
  font-family:'Share Tech Mono',monospace;
  backdrop-filter:blur(6px);opacity:0.7;}
#ctrl-bar span{display:flex;gap:4px;align-items:center;}
#ctrl-bar kbd{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
  border-radius:3px;padding:1px 5px;color:var(--text);font-size:9px;font-family:inherit;}

/* ── MISSION SELECT ──────────── */
#mission-ov{position:absolute;inset:0;z-index:300;
  background:radial-gradient(ellipse at 50% 30%,#061018 0%,#020508 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;
  overflow:hidden;}
#mission-ov::before{content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,200,255,0.015) 2px,rgba(0,200,255,0.015) 4px);
  pointer-events:none;}
.mo-eyebrow{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--cyan);
  letter-spacing:6px;margin-bottom:8px;opacity:0.6;}
.mo-title{font-family:'Black Han Sans',sans-serif;font-size:2.8rem;
  color:var(--gold);letter-spacing:8px;
  text-shadow:0 0 60px rgba(245,197,24,0.4),0 0 120px rgba(245,197,24,0.15);
  margin-bottom:4px;}
.mo-sub{font-size:0.75rem;color:var(--textDim);letter-spacing:4px;
  font-family:'Share Tech Mono',monospace;margin-bottom:24px;}
.mo-stats-row{display:flex;gap:20px;margin-bottom:20px;}
.mo-stat{text-align:center;background:rgba(0,200,255,0.04);border:1px solid var(--border);
  border-radius:6px;padding:8px 16px;}
.mo-stat-v{font-family:'Orbitron',sans-serif;font-size:16px;font-weight:700;color:var(--gold);}
.mo-stat-l{font-size:9px;color:var(--textDim);letter-spacing:2px;margin-top:2px;font-family:'Share Tech Mono',monospace;}

.mission-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  max-width:600px;width:100%;margin-bottom:20px;padding:0 10px;}
.mis-card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
  border-radius:10px;padding:14px 12px;cursor:pointer;
  transition:all 0.22s cubic-bezier(.34,1.56,.64,1);text-align:left;
  position:relative;overflow:hidden;}
.mis-card::before{content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(0,200,255,0.04) 0%,transparent 60%);
  opacity:0;transition:opacity 0.2s;}
.mis-card:hover:not(.locked),.mis-card.sel{
  border-color:rgba(245,197,24,0.5);
  background:rgba(245,197,24,0.04);
  transform:translateY(-2px);
  box-shadow:0 8px 24px rgba(0,0,0,0.4),0 0 20px rgba(245,197,24,0.1);}
.mis-card:hover::before,.mis-card.sel::before{opacity:1;}
.mis-card.locked{opacity:0.25;cursor:default;}
.mc-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;}
.mc-num{font-family:'Orbitron',sans-serif;font-size:24px;font-weight:900;color:var(--gold);line-height:1;}
.mc-stars{font-size:10px;}
.mc-name{font-family:'Black Han Sans',sans-serif;font-size:13px;color:var(--text);margin-bottom:4px;}
.mc-desc{font-size:9px;color:var(--textDim);line-height:1.5;margin-bottom:6px;}
.mc-meta{display:flex;gap:6px;flex-wrap:wrap;}
.mc-tag{font-family:'Share Tech Mono',monospace;font-size:8px;
  background:rgba(0,200,255,0.08);border:1px solid var(--border);
  border-radius:3px;padding:2px 5px;color:var(--cyan);}
.mc-clr{position:absolute;top:8px;right:8px;font-size:9px;color:var(--green);
  font-family:'Share Tech Mono',monospace;letter-spacing:1px;}
.mc-reward{font-size:9px;color:var(--gold2);margin-top:4px;font-family:'Share Tech Mono',monospace;}

.mo-start{padding:12px 56px;
  background:linear-gradient(135deg,rgba(20,60,5,0.9),rgba(40,110,5,0.9));
  border:1px solid rgba(80,180,0,0.5);border-radius:6px;
  color:#88ff44;font-family:'Black Han Sans',sans-serif;font-size:14px;
  letter-spacing:4px;cursor:pointer;transition:all 0.2s;
  box-shadow:0 0 20px rgba(60,160,0,0.2);}
.mo-start:hover:not(:disabled){transform:scale(1.05);
  box-shadow:0 0 30px rgba(60,160,0,0.35);}
.mo-start:disabled{opacity:0.3;cursor:default;}

/* ── RESULT OVERLAY ──────────── */
#result-ov{position:absolute;inset:0;z-index:300;
  background:rgba(0,0,0,0.95);
  backdrop-filter:blur(8px);
  display:none;flex-direction:column;align-items:center;justify-content:center;gap:14px;}
.res-eyebrow{font-family:'Share Tech Mono',monospace;font-size:10px;
  letter-spacing:6px;margin-bottom:4px;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:2.4rem;letter-spacing:6px;}
.grade-display{width:80px;height:80px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  font-family:'Orbitron',sans-serif;font-size:36px;font-weight:900;
  border:3px solid currentColor;margin:0 auto;}
.res-panel{background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:12px;padding:18px 24px;min-width:360px;}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;}
.rs{display:flex;justify-content:space-between;align-items:center;
  font-size:12px;color:var(--textDim);font-family:'Share Tech Mono',monospace;
  padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.rs:last-child{border-bottom:none;}
.rs b{color:var(--gold);font-weight:600;}
.rs.highlight b{color:var(--green);font-size:14px;}
.new-record{font-size:10px;color:var(--green);letter-spacing:3px;
  font-family:'Share Tech Mono',monospace;text-align:center;}
.res-btns{display:flex;gap:10px;}
.rbtn{padding:10px 30px;border:none;border-radius:6px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:13px;letter-spacing:2px;
  transition:all 0.18s;}
.rbtn:hover{transform:translateY(-2px);}
.rbtn.retry{background:linear-gradient(135deg,rgba(20,60,5,0.9),rgba(40,110,5,0.9));
  color:#88ff44;border:1px solid rgba(80,180,0,0.5);}
.rbtn.back{background:rgba(255,255,255,0.05);color:#666;border:1px solid rgba(255,255,255,0.1);}

/* ── MINI MAP ──────────── */
#minimap{position:absolute;bottom:30px;right:12px;z-index:100;
  width:130px;height:78px;border-radius:6px;overflow:hidden;
  border:1px solid var(--border2);opacity:0.8;}
#minimap-cv{display:block;width:130px;height:78px;}

/* ── SNIPER WARNING ──────────── */
#sniper-warn{position:absolute;inset:0;z-index:60;pointer-events:none;
  border:4px solid transparent;transition:border-color 0.1s;}
#sniper-warn.active{border-color:rgba(255,0,50,0.8);
  box-shadow:inset 0 0 100px rgba(255,0,40,0.2);}

/* ── ARTILLERY SHAKE ──────────── */
@keyframes artShake{
  0%,100%{transform:translate(0,0) rotate(0deg);}
  10%{transform:translate(-3px,2px) rotate(-0.5deg);}
  20%{transform:translate(3px,-3px) rotate(0.5deg);}
  30%{transform:translate(-2px,3px) rotate(-0.3deg);}
  40%{transform:translate(2px,-2px) rotate(0.3deg);}
  50%{transform:translate(-3px,1px);}
  60%{transform:translate(3px,-1px);}
  70%{transform:translate(-1px,3px);}
  80%{transform:translate(1px,-2px);}
  90%{transform:translate(-2px,2px);}
}
#root.shaking{animation:artShake 0.5s ease;}

/* ── OBJECTIVE POPUP ──────────── */
#obj-popup{position:absolute;top:90px;left:50%;transform:translateX(-50%) translateY(-80px);
  background:var(--panel);border:1px solid var(--border3);
  border-radius:8px;padding:8px 18px;z-index:290;pointer-events:none;
  transition:transform 0.3s cubic-bezier(.34,1.56,.64,1);
  font-family:'Rajdhani',sans-serif;font-size:13px;font-weight:700;
  color:var(--gold);letter-spacing:2px;text-align:center;
  box-shadow:0 0 30px rgba(0,200,255,0.15);display:none;}
#obj-popup.show{transform:translateX(-50%) translateY(0);}

/* ── ANIMATIONS ──────────── */
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
</style>
</head>
<body>
<div id="root">
  <canvas id="gc"></canvas>
  <div id="scanlines"></div>
  <div id="night-overlay"></div>

  <!-- TOP HUD -->
  <div id="hud">
    <div class="hud-block">
      <div class="hud-val" id="score-v">0</div>
      <div class="hud-lbl">SCORE</div>
    </div>
    <div class="hud-block">
      <div class="hud-val" id="kill-v">0</div>
      <div class="hud-lbl">KILLS</div>
    </div>
    <div class="hud-block">
      <div class="hud-val" id="combo-v">x1</div>
      <div class="hud-lbl">COMBO</div>
    </div>
    <div class="hud-block" style="min-width:70px;">
      <div class="hud-val" id="timer-v">--:--</div>
      <div class="hud-lbl">TIME</div>
    </div>

    <!-- AMMO DISPLAY -->
    <div class="hud-block" id="ammo-block">
      <div id="ammo-bullets"></div>
      <div class="hud-lbl">AMMO</div>
    </div>

    <!-- BATTLE BAR + OBJECTIVES -->
    <div id="battle-wrap">
      <div id="battle-header">
        <span id="mission-name">임무 선택</span>
        <span id="battle-info">0 VS 0</span>
      </div>
      <div id="battle-track">
        <div id="ally-bar" style="width:50%"></div>
        <div id="enemy-bar" style="width:50%"></div>
      </div>
      <div id="objective-row"></div>
    </div>

    <!-- ALLY HP -->
    <div id="hp-wrap" class="hud-block" style="min-width:90px;padding:4px 8px;">
      <div id="hp-lbl"><span>아군</span><span id="hp-pct">100%</span></div>
      <div id="hp-track"><div id="hp-fill" style="width:100%;background:var(--green);"></div></div>
      <div class="hud-lbl">ALLY HP</div>
    </div>
  </div>

  <!-- CONTROLS HINT -->
  <div id="ctrl-bar">
    <span><kbd>CLICK</kbd><kbd>SPACE</kbd> 발사</span>
    <span><kbd>Z</kbd><kbd>우클릭</kbd> 스코프</span>
    <span><kbd>R</kbd> 재장전</span>
    <span><kbd>SHIFT</kbd> 숨참기</span>
    <span><kbd>ESC</kbd> 타이틀</span>
  </div>

  <!-- SCOPE -->
  <div id="scope-wrap">
    <div id="scope-blackout"></div>
    <div id="scope-lens">
      <canvas id="scope-cv"></canvas>
      <div id="scope-vignette"></div>
      <svg id="scope-reticle" viewBox="0 0 320 320" xmlns="http://www.w3.org/2000/svg">
        <!-- outer ring -->
        <circle cx="160" cy="160" r="157" stroke="rgba(0,255,100,0.25)" stroke-width="1" fill="none"/>
        <!-- main crosshair -->
        <line x1="0" y1="160" x2="122" y2="160" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="198" y1="160" x2="320" y2="160" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="160" y1="0" x2="160" y2="122" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="160" y1="198" x2="160" y2="320" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <!-- center dot -->
        <circle cx="160" cy="160" r="2.5" stroke="rgba(0,255,100,1)" stroke-width="1.5" fill="none"/>
        <!-- mil-dot horizontals -->
        <line x1="90" y1="170" x2="230" y2="170" stroke="rgba(0,255,100,0.25)" stroke-width="0.8"/>
        <line x1="90" y1="150" x2="230" y2="150" stroke="rgba(0,255,100,0.25)" stroke-width="0.8"/>
        <line x1="90" y1="185" x2="230" y2="185" stroke="rgba(0,255,100,0.15)" stroke-width="0.6"/>
        <line x1="90" y1="135" x2="230" y2="135" stroke="rgba(0,255,100,0.15)" stroke-width="0.6"/>
        <!-- mil dots -->
        <circle cx="130" cy="160" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="190" cy="160" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="160" cy="130" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="160" cy="190" r="2" fill="rgba(0,255,100,0.5)"/>
        <!-- diagonal tick marks -->
        <line x1="140" y1="140" x2="147" y2="147" stroke="rgba(0,255,100,0.3)" stroke-width="0.8"/>
        <line x1="180" y1="140" x2="173" y2="147" stroke="rgba(0,255,100,0.3)" stroke-width="0.8"/>
        <line x1="140" y1="180" x2="147" y2="173" stroke="rgba(0,255,100,0.3)" stroke-width="0.8"/>
        <line x1="180" y1="180" x2="173" y2="173" stroke="rgba(0,255,100,0.3)" stroke-width="0.8"/>
      </svg>
      <!-- corner brackets -->
      <div class="scope-corner sc-tl"></div>
      <div class="scope-corner sc-tr"></div>
      <div class="scope-corner sc-bl"></div>
      <div class="scope-corner sc-br"></div>
    </div>
    <div id="scope-bottom">
      <div id="scope-dist"></div>
      <div id="scope-state"></div>
      <div id="breath-wrap">
        <div id="breath-track"><div id="breath-fill" style="width:100%"></div></div>
      </div>
    </div>
  </div>

  <!-- EFFECT OVERLAYS -->
  <div id="vignette-hit"></div>
  <div id="crit-flash"></div>
  <div id="sniper-warn"></div>

  <!-- MINIMAP -->
  <canvas id="minimap-cv" width="130" height="78"></canvas>
  <div id="minimap" style="display:none;bottom:30px;right:12px;"></div>

  <!-- TOAST / KILLFEED / STATUS -->
  <div id="toast"></div>
  <div id="killfeed"></div>
  <div id="obj-popup"></div>

  <div id="status-bar">
    <div id="status-left">
      <span class="sl-item">WIND <span class="sv" id="wind-dir">→</span> <span class="sv" id="wind-spd">3m/s</span></span>
      <span class="sl-item">RANGE <span class="sv" id="range-v">---m</span></span>
      <span class="sl-item">ELEV <span class="sv" id="elev-v">+0.0°</span></span>
      <span class="sl-item">CRIT <span class="sv" id="crit-pct">15%</span></span>
    </div>
    <div id="status-right">
      <div id="reload-bar"><div id="reload-fill" style="width:0%"></div></div>
      <span id="reload-lbl" style="display:none;color:var(--gold);animation:blink 0.5s infinite;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;">재장전중...</span>
      <span id="ally-count-v" style="color:var(--textDim);font-family:'Share Tech Mono',monospace;font-size:10px;"></span>
    </div>
  </div>

  <!-- ── MISSION SELECT ── -->
  <div id="mission-ov">
    <div class="mo-eyebrow">OPERATION BRIEFING</div>
    <div class="mo-title">🎯 스나이퍼 엘리트</div>
    <div class="mo-sub">전장의 저격수 — WAR SNIPER ULTRA</div>
    <div class="mo-stats-row" id="global-stats-row">
      <div class="mo-stat"><div class="mo-stat-v" id="gs-total">0</div><div class="mo-stat-l">TOTAL KILLS</div></div>
      <div class="mo-stat"><div class="mo-stat-v" id="gs-best">0</div><div class="mo-stat-l">BEST SCORE</div></div>
      <div class="mo-stat"><div class="mo-stat-v" id="gs-mis">0/6</div><div class="mo-stat-l">MISSIONS</div></div>
    </div>
    <div class="mission-grid" id="mission-grid"></div>
    <button class="mo-start" id="mo-start-btn" disabled onclick="startMission()">임무 시작 ▶</button>
  </div>

  <!-- ── RESULT OVERLAY ── -->
  <div id="result-ov">
    <div class="res-eyebrow" id="res-eyebrow"></div>
    <div class="res-title" id="res-title"></div>
    <div class="grade-display" id="grade-disp"></div>
    <div id="new-rec-lbl" class="new-record" style="display:none;">🏆 신기록!</div>
    <div class="res-panel">
      <div class="res-grid" id="res-stats"></div>
    </div>
    <div class="res-btns">
      <button class="rbtn retry" onclick="retryMission()">재시도 ↺</button>
      <button class="rbtn back" onclick="gotoTitle()">타이틀 ⬛</button>
    </div>
  </div>
</div>

<script>
'use strict';

// ══════════════════════════════════════════
//  CANVAS + CONSTANTS
// ══════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');
const scopeCV = document.getElementById('scope-cv');
const sCtx = scopeCV.getContext('2d');
const mmCV = document.getElementById('minimap-cv');
const mmCtx = mmCV.getContext('2d');

const GW = 920, GH = 660;
canvas.width = GW; canvas.height = GH;

let G = null, selMis = null, RAF, lastTs = 0, timer = 0;

// ══════════════════════════════════════════
//  MISSION DATA
// ══════════════════════════════════════════
const MISSIONS = [
  {id:1, name:'전선 사수', diff:'초급', stars:1,
   timeLimit:90, killGoal:15, bossGoal:0, allyHPMin:50,
   desc:'전선이 붕괴 직전! 적군 15명을 신속히 제거해 전선을 사수하라.',
   reward:5000000, zoom:3.5, critBonus:1.0,
   spawns:[{t:'infantry',n:15}]},
  {id:2, name:'지휘관 암살', diff:'보통', stars:2,
   timeLimit:120, killGoal:10, bossGoal:1, allyHPMin:30,
   desc:'적 지휘관이 이동 중. 경호대를 제거하고 지휘관을 처치하라.',
   reward:15000000, zoom:4.0, critBonus:1.2,
   spawns:[{t:'infantry',n:8},{t:'commander',n:1},{t:'guard',n:5}]},
  {id:3, name:'포병 무력화', diff:'어려움', stars:3,
   timeLimit:150, killGoal:20, bossGoal:2, allyHPMin:40,
   desc:'아군이 포격에 노출됐다. 포병 거점을 파괴하고 장교 2명을 제거하라.',
   reward:30000000, zoom:4.0, critBonus:1.3,
   spawns:[{t:'artillery',n:3},{t:'officer',n:2},{t:'infantry',n:15},{t:'guard',n:5}]},
  {id:4, name:'포위 돌파', diff:'전문가', stars:4,
   timeLimit:180, killGoal:40, bossGoal:3, allyHPMin:20,
   desc:'아군이 포위됐다! 사방에서 밀려오는 적을 격퇴해 포위망을 돌파하라.',
   reward:60000000, zoom:4.5, critBonus:1.4,
   spawns:[{t:'infantry',n:25},{t:'officer',n:3},{t:'sniper_e',n:2},{t:'guard',n:10}]},
  {id:5, name:'총사령관 처치', diff:'전설', stars:5,
   timeLimit:240, killGoal:30, bossGoal:1, allyHPMin:10,
   desc:'최정예 경호대를 돌파하고 적 총사령관을 처치하라. 단 한 번의 기회.',
   reward:200000000, zoom:5.0, critBonus:1.5,
   spawns:[{t:'infantry',n:15},{t:'guard',n:10},{t:'sniper_e',n:3},{t:'general',n:1}]},
  {id:6, name:'야간 특수작전', diff:'전설+', stars:5,
   timeLimit:300, killGoal:60, bossGoal:4, allyHPMin:5,
   desc:'야음을 틈타 잠입. 플래시라이트만 의지해 전략 목표를 전부 제거하라.',
   reward:500000000, zoom:5.0, critBonus:1.8, night:true,
   spawns:[{t:'infantry',n:25},{t:'guard',n:15},{t:'officer',n:5},{t:'sniper_e',n:4},{t:'commander',n:3},{t:'general',n:1}]},
];

const ETYPES = {
  infantry:  {name:'보병',  hp:100, col:'#bb2200', sz:8,  spd:0.9, xp:100, boss:false, icon:'🪖', outline:'#ff4422'},
  guard:     {name:'경호원', hp:150, col:'#881100', sz:9,  spd:1.2, xp:180, boss:false, icon:'🔴', outline:'#cc3311'},
  officer:   {name:'장교',  hp:220, col:'#660000', sz:11, spd:0.8, xp:400, boss:true,  icon:'⭐', outline:'#aa2200'},
  commander: {name:'지휘관', hp:400, col:'#440000', sz:14, spd:0.6, xp:800, boss:true,  icon:'🎖️', outline:'#880000'},
  general:   {name:'총사령관',hp:700,col:'#220000', sz:18, spd:0.5, xp:3000,boss:true,  icon:'🏅', outline:'#660000'},
  artillery: {name:'포병',  hp:450, col:'#6a3800', sz:22, spd:0,   xp:600, boss:true,  icon:'💣', outline:'#cc7700'},
  sniper_e:  {name:'적저격수',hp:120,col:'#003322', sz:8,  spd:0.4, xp:500, boss:true,  icon:'🎯', outline:'#006644'},
};

// ══════════════════════════════════════════
//  GAME STATE INIT
// ══════════════════════════════════════════
function initGame(midx) {
  const mis = MISSIONS[midx];
  G = {
    midx, mis, phase: 'play',
    time: mis.timeLimit, score: 0, kills: 0, bossKills: 0,
    allyHP: 100, allyPower: 50,
    enemies: [], allies: [], bullets: [], particles: [], bloodSplats: [],
    scoped: false,
    mouse: {x: GW/2, y: GH/2},
    swayX: 0, swayY: 0, swayT: 0,
    breathHeld: false, breathTimer: 3,
    reloading: false, reloadTimer: 0, reloadTotal: 2.5,
    ammo: 5, maxAmmo: 5, shootCd: 0,
    spawnQueue: buildQueue(mis), spawnTimer: 0,
    artilleryActive: 0, sniperWarning: 0,
    allyWarnTimer: 3, frame: 0, done: false,
    combo: 1, comboTimer: 0,
    wind: {angle: Math.random()*Math.PI*2, speed: 1+Math.random()*5},
    critBonus: mis.critBonus || 1,
    terrainSeed: Math.random()*1000,
    particles: [],
    muzzleFlash: 0,
    totalDamage: 0,
    shotsTotal: 0,
    shotsHit: 0,
    headshots: 0,
  };
  if(mis.night) {
    document.getElementById('night-overlay').style.display='block';
  } else {
    document.getElementById('night-overlay').style.display='none';
  }
  updateMinimap();
  for(let i=0;i<12;i++) spawnAlly();
  buildAmmoUI();
  updateHUD();
  showObjPopup(`임무: ${mis.name}`);
}

function buildQueue(mis) {
  const q = []; let d = 1.5;
  for(const s of mis.spawns) {
    for(let i=0;i<s.n;i++) {
      q.push({t:s.t, delay:d + i*(1.1+Math.random()*0.7)});
    }
    d += s.n*1.1 + 3;
  }
  q.sort((a,b)=>a.delay-b.delay);
  return q;
}

function spawnAlly() {
  const y = 130+Math.random()*(GH-230);
  G.allies.push({
    x: 40+Math.random()*80, y,
    vx: 0.3+Math.random()*0.3,
    phase: Math.random()*Math.PI*2,
    atkT: 0.5+Math.random(),
    col: `hsl(${210+Math.random()*20},80%,${50+Math.random()*15}%)`
  });
}

function spawnEnemy(type) {
  const t = ETYPES[type];
  const sc = 1 + G.midx*0.22;
  const y = 125+Math.random()*(GH-210);
  G.enemies.push({
    type, x: GW+30+Math.random()*80, y,
    vx: -(t.spd*(0.7+Math.random()*0.5)),
    vy: (Math.random()-0.5)*0.3,
    hp: Math.round(t.hp*sc), maxHp: Math.round(t.hp*sc),
    col: t.col, outline: t.outline, sz: t.sz,
    xp: Math.round(t.xp*sc), boss: t.boss,
    icon: t.icon, name: t.name,
    alive: true, dying: false, deathT: 0,
    phase: Math.random()*Math.PI*2,
    atkT: 1+Math.random()*2,
    fireT: type==='sniper_e' ? 3+Math.random()*5 : 0,
    special: type,
    flashT: 0,
    hitPulse: 0,
  });
}

// ══════════════════════════════════════════
//  TICK / UPDATE
// ══════════════════════════════════════════
function tick(dt) {
  if(!G || G.phase!=='play' || G.done) return;
  G.frame++; timer += dt; G.time -= dt;
  G.swayT += dt;
  const swayMult = G.breathHeld ? 0.06 : 1;
  G.swayX = Math.sin(G.swayT*0.85)*6*swayMult + Math.sin(G.swayT*2.2)*2.5*swayMult;
  G.swayY = Math.cos(G.swayT*0.68)*5*swayMult + Math.cos(G.swayT*1.9)*2*swayMult;
  G.shootCd = Math.max(0, G.shootCd-dt);
  G.muzzleFlash = Math.max(0, G.muzzleFlash-dt*8);
  if(G.breathHeld) { G.breathTimer -= dt*0.45; if(G.breathTimer<=0){G.breathHeld=false;G.breathTimer=0;} }
  else G.breathTimer = Math.min(3, G.breathTimer+dt*0.55);
  if(G.reloading) {
    G.reloadTimer -= dt;
    const pct = Math.max(0, 1-(G.reloadTimer/G.reloadTotal));
    document.getElementById('reload-fill').style.width = (pct*100)+'%';
    if(G.reloadTimer<=0) {
      G.reloading=false;
      G.ammo=G.maxAmmo;
      document.getElementById('reload-bar').style.display='none';
      document.getElementById('reload-lbl').style.display='none';
      buildAmmoUI();
      sfx_reload_done();
      showToast('탄창 장전 완료!');
    }
  }
  if(G.sniperWarning>0) {
    G.sniperWarning -= dt;
    document.getElementById('sniper-warn').className = G.sniperWarning>0?'active':'';
  }
  if(G.artilleryActive>0) { G.artilleryActive -= dt; G.allyHP -= dt*7; }
  // combo decay
  if(G.comboTimer>0) { G.comboTimer -= dt; if(G.comboTimer<=0){G.combo=1;updateComboUI();} }
  // spawn
  G.spawnTimer += dt;
  while(G.spawnQueue.length && G.spawnQueue[0].delay<=G.spawnTimer) spawnEnemy(G.spawnQueue.shift().t);
  updEnemies(dt); updAllies(dt); updBullets(dt); updParticles(dt);
  // battle ratio
  const ae=G.enemies.filter(e=>e.alive).length, aa=G.allies.length;
  const r = aa/Math.max(1,aa+ae);
  G.allyPower += (r*100-G.allyPower)*dt*0.09;
  G.allyHP = Math.max(0, Math.min(100, G.allyHP));
  // ally warn
  if(G.allyHP<30) { G.allyWarnTimer-=dt; if(G.allyWarnTimer<=0){G.allyWarnTimer=4;showToast('⚠️ 아군이 위험합니다!');} }
  updateHUD(); checkEnd();
}

function updEnemies(dt) {
  for(let i=G.enemies.length-1;i>=0;i--) {
    const e = G.enemies[i];
    e.flashT = Math.max(0, (e.flashT||0)-dt*8);
    e.hitPulse = Math.max(0, (e.hitPulse||0)-dt*5);
    if(e.dying) { e.deathT+=dt; if(e.deathT>0.8)G.enemies.splice(i,1); continue; }
    if(!e.alive) continue;
    e.phase += dt*2;
    if(e.special!=='artillery') {
      e.x += e.vx;
      e.y = Math.max(110, Math.min(GH-60, e.y+e.vy+Math.sin(e.phase)*0.3));
    }
    if(e.x<90) {
      G.allyHP -= dt*9; e.vx=0;
      e.atkT -= dt;
      if(e.atkT<=0) {
        e.atkT=0.7+Math.random();
        G.allyHP -= 3+Math.random()*4;
        if(G.allies.length>0&&Math.random()<0.35)
          G.allies.splice(Math.floor(Math.random()*G.allies.length),1);
      }
    }
    if(e.special==='artillery') {
      e.atkT -= dt;
      if(e.atkT<=0) {
        e.atkT=4+Math.random()*4;
        G.artilleryActive=2.2;
        document.getElementById('root').classList.add('shaking');
        setTimeout(()=>document.getElementById('root').classList.remove('shaking'),500);
        showKF('💥 포격 개시!','#ff7700');
        // spawn shell impact particles
        for(let p=0;p<20;p++) spawnParticle(400+Math.random()*400, 200+Math.random()*300, '#ff6600', '#ffaa00', 2+Math.random()*3);
      }
    }
    if(e.special==='sniper_e') {
      e.fireT -= dt;
      if(e.fireT<=0 && e.x<GW-60) {
        e.fireT=3.5+Math.random()*5;
        G.sniperWarning=1.8;
        G.allyHP-=2.5;
        showKF('⚠️ 적 저격수 사격!','#ff4400');
        sfx_enemy_shot();
      }
    }
  }
}

function updAllies(dt) {
  if(G.frame%240===0 && G.allies.length<14 && G.allyHP>20) spawnAlly();
  for(const a of G.allies) {
    a.phase += dt*2.2;
    const ne = G.enemies.filter(e=>e.alive).sort((a,b)=>a.x-b.x)[0];
    if(ne) {
      const dx=ne.x-a.x, dy=ne.y-a.y, d=Math.hypot(dx,dy);
      if(d>55) { a.x+=(dx/d)*a.vx; a.y+=(dy/d)*a.vx; }
      else {
        a.atkT -= dt;
        if(a.atkT<=0) {
          a.atkT=0.5+Math.random();
          const dmg = 5+Math.random()*5;
          ne.hp -= dmg;
          ne.flashT = 0.15;
          if(ne.hp<=0) killE(ne,false);
        }
      }
    } else { a.x=Math.min(a.x+a.vx*0.3, GW-120); }
    a.y = Math.max(110, Math.min(GH-60, a.y+Math.sin(a.phase)*0.25));
  }
}

function updBullets(dt) {
  for(let i=G.bullets.length-1;i>=0;i--) {
    const b = G.bullets[i];
    
    // 1. 이번 프레임에서 총알이 이동할 전체 X, Y 거리 계산
    const moveX = b.vx*dt*60 + G.wind.speed*Math.cos(G.wind.angle)*dt*0.8;
    const moveY = b.vy*dt*60 + G.wind.speed*Math.sin(G.wind.angle)*dt*0.4;
    
    // 2. 이동 거리를 10픽셀 단위로 잘게 쪼갬 (터널링 방지)
    const steps = Math.max(1, Math.ceil(Math.hypot(moveX, moveY) / 10));
    const stepX = moveX / steps;
    const stepY = moveY / steps;
    
    let hit = false;
    
    // 3. 쪼갠 거리(step)만큼 이동시키면서 매번 충돌 검사
    for(let s = 0; s < steps; s++) {
      b.x += stepX;
      b.y += stepY;
      
      for(const e of G.enemies) {
        if(!e.alive) continue;
        
        // 충돌 판정
        if(Math.hypot(e.x-b.x, e.y-b.y) < e.sz + 5) {
          const headshot = Math.random() < (b.crit ? 0.6 : 0.15);
          const dmg = b.dmg * (headshot ? 2 : 1);
          e.hp -= dmg; 
          e.flashT = 0.2; 
          e.hitPulse = 1;
          G.totalDamage += dmg;
          G.shotsHit++;
          if(headshot) G.headshots++;
          
          spawnDN(e.x, e.y, Math.round(dmg), b.crit, headshot);
          
          if(b.crit || headshot) {
            document.getElementById('crit-flash').classList.add('show');
            setTimeout(()=>document.getElementById('crit-flash').classList.remove('show'), 150);
          }
          
          // 피격 파티클 및 흔적
          for(let p=0; p<12; p++) spawnParticle(e.x, e.y, '#cc1100', '#ff2200', 1+Math.random()*2);
          G.bloodSplats.push({x:e.x, y:e.y, r:2+Math.random()*4, a:0.4});
          
          if(e.hp <= 0) killE(e, true);
          
          hit = true;
          break; // 적을 맞췄으므로 현재 총알의 적 탐색 루프 탈출
        }
      }
      if(hit) break; // 맞췄으면 스텝(이동) 루프도 탈출
    }
    
    b.life -= dt;
    
    // 총알 궤적 파티클
    if(G.frame%2===0 && !hit) spawnParticle(b.x, b.y, '#ffff88','#ffaa44',1);
    
    // 4. 충돌했거나, 수명이 다했거나, 맵 밖으로 나가면 총알 삭제
    if(hit || b.life<=0 || b.x<0 || b.x>GW || b.y<0 || b.y>GH) { 
      G.bullets.splice(i,1); 
    }
  }
}

function updParticles(dt) {
  for(let i=G.particles.length-1;i>=0;i--) {
    const p=G.particles[i];
    p.x+=p.vx*dt*60; p.y+=p.vy*dt*60;
    p.vy+=0.15*dt*60;
    p.life-=dt*p.decay;
    if(p.life<=0) G.particles.splice(i,1);
  }
}

function spawnParticle(x,y,col1,col2,size) {
  const angle=Math.random()*Math.PI*2, spd=0.5+Math.random()*3;
  G.particles.push({
    x,y,vx:Math.cos(angle)*spd,vy:Math.sin(angle)*spd-1,
    col:Math.random()>0.5?col1:col2,
    size, life:1, decay:1.5+Math.random()*2
  });
}

// ══════════════════════════════════════════
//  COMBAT FUNCTIONS
// ══════════════════════════════════════════
function killE(e,byPlayer) {
  if(!e.alive) return;
  e.alive=false; e.dying=true; e.deathT=0;
  // death particles
  for(let p=0;p<(e.boss?25:15);p++) spawnParticle(e.x,e.y,'#cc1100','#ff4422',1.5+Math.random()*2);
  if(byPlayer) {
    G.kills++; G.shotsHit++;
    // combo
    G.combo = Math.min(G.combo+1, 10);
    G.comboTimer = 3.5;
    const comboBonus = 1 + (G.combo-1)*0.15;
    const scoreAdd = Math.round(e.xp * comboBonus);
    G.score += scoreAdd;
    updateComboUI();
    if(e.boss) {
      G.bossKills++;
      sfx_boss_kill();
      showToast(`🏆 ${e.name} 처치! +${scoreAdd.toLocaleString()} (x${G.combo}콤보)`);
      showKF(`🏆 ${e.icon} ${e.name} 격파!`, '#f5c518', true);
      showObjPopup(`${e.name} 처치!`);
    } else {
      showKF(`${e.icon} ${e.name} +${scoreAdd}`, G.combo>=3?'#f5c518':'#ccc', false);
    }
    if(e.special==='artillery') { G.artilleryActive=0; showToast('💣 포병 파괴 완료!'); }
    // update global stats
    const stats = JSON.parse(localStorage.getItem('sniper_ultra_stats')||'{}');
    stats.totalKills = (stats.totalKills||0)+1;
    stats.bestScore = Math.max(stats.bestScore||0, G.score);
    localStorage.setItem('sniper_ultra_stats', JSON.stringify(stats));
  }
}

function fire() {
  if(!G||G.phase!=='play') return;
  if(G.reloading){showToast('재장전 중!');return;}
  if(G.shootCd>0) return;
  if(G.ammo<=0){startReload();return;}
  G.ammo--; G.shootCd=0.85; G.shotsTotal++;
  G.muzzleFlash=1;
  buildAmmoUI();
  const crit = Math.random()<(0.15*G.critBonus);
  let wx=G.mouse.x, wy=G.mouse.y;
  const sw = G.breathHeld ? 0.25 : 3.5;
  wx += (Math.random()-0.5)*sw*2 + G.swayX*0.35;
  wy += (Math.random()-0.5)*sw*2 + G.swayY*0.35;
  // wind effect on aim
  wx += G.wind.speed*Math.cos(G.wind.angle)*0.4;
  const ang = Math.atan2(wy-(GH-55), wx-55);
  const spd = 920;
  G.bullets.push({
    x:55, y:GH-55,
    vx:Math.cos(ang)*spd, vy:Math.sin(ang)*spd,
    dmg: 80*(crit?2.8:1), crit, life:2
  });
  // muzzle particles
  for(let p=0;p<15;p++) spawnParticle(55,GH-55,'#ffff88','#ffaa00',1.5+Math.random()*2);
  sfx_shoot();
  if(G.ammo===0) setTimeout(startReload,400);
}

function startReload() {
  if(!G||G.reloading||G.ammo===G.maxAmmo) return;
  G.reloading=true; G.reloadTimer=G.reloadTotal;
  document.getElementById('reload-bar').style.display='block';
  document.getElementById('reload-lbl').style.display='block';
  document.getElementById('reload-fill').style.width='0%';
  sfx_reload_start();
  showToast('재장전 중...');
}

function checkEnd() {
  if(G.done) return;
  const mis=G.mis;
  if(G.time<=0||G.allyHP<=0) { G.done=true; showResult(false); return; }
  const bossRem=G.enemies.filter(e=>e.alive&&e.boss).length;
  const allBossSpawned=G.spawnQueue.filter(s=>ETYPES[s.t]?.boss).length===0;
  const won=G.kills>=mis.killGoal && (mis.bossGoal===0||G.bossKills>=mis.bossGoal);
  if(won && allBossSpawned && bossRem===0) { G.done=true; showResult(true); }
}

function showResult(win) {
  G.phase='result';
  if(G.scoped) toggleScope();
  const el=document.getElementById('result-ov');
  const eyebrow=document.getElementById('res-eyebrow');
  const title=document.getElementById('res-title');
  const gradeEl=document.getElementById('grade-disp');
  eyebrow.textContent = win ? 'MISSION COMPLETE' : 'MISSION FAILED';
  eyebrow.style.color = win ? 'var(--green)' : 'var(--red)';
  title.textContent = win ? '임무 완료!' : '임무 실패';
  title.style.color = win ? 'var(--gold)' : 'var(--red)';
  const g=grade();
  const gColors={S:'#f5c518',A:'#00d4ff',B:'#00ff88',C:'#aabbcc',D:'#ff6644'};
  gradeEl.textContent=g; gradeEl.style.color=gColors[g]||'#aaa';
  const elapsed=G.mis.timeLimit-G.time;
  const acc=G.shotsTotal>0?Math.round(G.shotsHit/G.shotsTotal*100):0;
  document.getElementById('res-stats').innerHTML=`
    <div class="rs highlight">점수<b>${Math.round(G.score).toLocaleString()}</b></div>
    <div class="rs">등급<b>${g}</b></div>
    <div class="rs">킬수<b>${G.kills}</b></div>
    <div class="rs">보스처치<b>${G.bossKills}</b></div>
    <div class="rs">정확도<b>${acc}%</b></div>
    <div class="rs">헤드샷<b>${G.headshots}</b></div>
    <div class="rs">최고콤보<b>x${Math.max(1,G.combo)}</b></div>
    <div class="rs">경과시간<b>${Math.floor(elapsed/60)}m ${Math.floor(elapsed%60)}s</b></div>
    <div class="rs">아군HP<b>${Math.round(G.allyHP)}%</b></div>
    <div class="rs">총피해<b>${Math.round(G.totalDamage).toLocaleString()}</b></div>
  `;
  // check new record
  const saved=JSON.parse(localStorage.getItem('sniper_ultra_records')||'{}');
  const prevBest=saved[G.midx]?.score||0;
  if(win && Math.round(G.score)>prevBest) {
    document.getElementById('new-rec-lbl').style.display='block';
  } else {
    document.getElementById('new-rec-lbl').style.display='none';
  }
  el.style.display='flex';
  if(win) {
    const cl=JSON.parse(localStorage.getItem('sniper_ultra_clears')||'[]');
    if(!cl.includes(G.midx)) cl.push(G.midx);
    localStorage.setItem('sniper_ultra_clears',JSON.stringify(cl));
    if(!saved[G.midx]||Math.round(G.score)>prevBest) {
      saved[G.midx]={score:Math.round(G.score),grade:g};
      localStorage.setItem('sniper_ultra_records',JSON.stringify(saved));
    }
    sfx_win();
    try{window.parent.postMessage({type:'sniper_result',score:Math.round(G.score),grade:g},'*');}catch(e){}
  } else sfx_fail();
}

function grade() {
  const s=G.score;
  const acc=G.shotsTotal>0?G.shotsHit/G.shotsTotal:0;
  if(s>=80000&&acc>=0.9) return 'S';
  if(s>=50000) return 'A';
  if(s>=30000) return 'B';
  if(s>=15000) return 'C';
  return 'D';
}

function retryMission() { document.getElementById('result-ov').style.display='none'; initGame(G.midx); }
function gotoTitle() {
  document.getElementById('result-ov').style.display='none';
  G=null;
  document.getElementById('night-overlay').style.display='none';
  buildTitle();
  document.getElementById('mission-ov').style.display='flex';
}
function toggleScope() {
  if(!G) return;
  G.scoped=!G.scoped;
  document.getElementById('scope-wrap').style.display=G.scoped?'block':'none';
}

// ══════════════════════════════════════════
//  DRAWING
// ══════════════════════════════════════════
function drawScene(c, w, h, forScope) {
  const night = G && G.mis.night;
  // Sky gradient
  const skyG = c.createLinearGradient(0,0,0,h*0.45);
  if(night) {
    skyG.addColorStop(0,'#020408'); skyG.addColorStop(1,'#0a1018');
  } else {
    skyG.addColorStop(0,'#152030'); skyG.addColorStop(1,'#253040');
  }
  c.fillStyle=skyG; c.fillRect(0,0,w,h);

  // Stars (night mode)
  if(night && !forScope) {
    c.save();
    for(let i=0;i<80;i++) {
      const sx=(Math.sin(i*137.5)*0.5+0.5)*w;
      const sy=(Math.cos(i*97.3)*0.5+0.5)*h*0.38;
      const br=0.3+Math.sin(timer*2+i)*0.35;
      c.globalAlpha=br; c.fillStyle='#ffffff';
      c.beginPath(); c.arc(sx,sy,0.7,0,Math.PI*2); c.fill();
    }
    c.restore();
  }

  // Ground
  const gndG=c.createLinearGradient(0,h*0.28,0,h);
  if(night) {
    gndG.addColorStop(0,'#0a140a'); gndG.addColorStop(1,'#060c06');
  } else {
    gndG.addColorStop(0,'#1a3a0a'); gndG.addColorStop(1,'#0f2608');
  }
  c.fillStyle=gndG; c.fillRect(0,h*0.28,w,h);

  drawTerrain(c, w, h, night);

  // Blood splats
  if(G) for(const s of G.bloodSplats) {
    c.save(); c.globalAlpha=s.a*0.6;
    c.fillStyle='#550000'; c.beginPath(); c.arc(s.x,s.y,s.r,0,Math.PI*2); c.fill();
    c.restore();
    s.a -= 0.0003;
  }
  if(G) G.bloodSplats=G.bloodSplats.filter(s=>s.a>0);

  // Particles
  if(G) for(const p of G.particles) {
    c.save(); c.globalAlpha=p.life*0.8;
    c.fillStyle=p.col;
    c.beginPath(); c.arc(p.x,p.y,p.size,0,Math.PI*2); c.fill();
    c.restore();
  }

  // Allies
  if(G) for(const a of G.allies) {
    const bob=Math.sin(a.phase)*2;
    c.save(); c.translate(a.x,a.y+bob);
    // body
    c.shadowColor='#3388ff'; c.shadowBlur=6;
    c.fillStyle='#1a55cc';
    c.beginPath(); c.arc(0,0,7,0,Math.PI*2); c.fill();
    // head
    c.fillStyle='#3388ff';
    c.beginPath(); c.arc(0,-9,4.5,0,Math.PI*2); c.fill();
    c.shadowBlur=0;
    // helmet
    c.fillStyle='#2266dd';
    c.beginPath(); c.arc(0,-10,3.5,-Math.PI,0); c.fill();
    c.restore();
  }

  // Enemies
  if(G) for(const e of G.enemies) {
    if(!e.alive&&!e.dying) continue;
    const dying_a = e.dying ? Math.max(0,1-e.deathT/0.8) : 1;
    const flash = e.flashT>0 ? 1 : 0;
    c.save(); c.globalAlpha=dying_a;
    c.translate(e.x, e.y+Math.sin(e.phase)*2);
    if(e.dying) c.scale(1+e.deathT*0.5, 1+e.deathT*0.5);
    // glow for boss
    if(e.boss && !e.dying) {
      c.shadowColor=e.outline; c.shadowBlur=14+Math.sin(timer*3)*4;
    }
    // body
    if(flash) {
      c.fillStyle='#ffffff'; c.globalAlpha=dying_a*Math.min(1,e.flashT*8);
    } else {
      c.fillStyle=e.col;
    }
    if(e.special==='artillery') {
      // tank/artillery shape
      c.fillStyle=flash?'#ffffff':e.col;
      c.fillRect(-16,-8,32,14);
      c.fillStyle=flash?'#ffffff':'#cc7700';
      c.fillRect(-4,-20,8,16);
      c.fillStyle=flash?'#ffffff':'#885500';
      c.fillRect(-20,-5,40,4);
      // wheels
      for(let wx=-14;wx<=14;wx+=10) {
        c.fillStyle=flash?'#ffffff':'#333';
        c.beginPath(); c.arc(wx,6,5,0,Math.PI*2); c.fill();
      }
    } else {
      c.beginPath(); c.arc(0,0,e.sz,0,Math.PI*2); c.fill();
      // head
      const flashCol = flash?'#ffffff':(e.boss?e.outline:e.col);
      c.fillStyle=flashCol;
      c.beginPath(); c.arc(0,-e.sz-4,e.sz*0.65,0,Math.PI*2); c.fill();
    }
    c.shadowBlur=0;
    // Boss icon
    if(e.boss && e.sz>=11 && !e.dying) {
      c.font=`${e.sz+2}px serif`;
      c.textAlign='center'; c.textBaseline='middle';
      c.globalAlpha=dying_a*0.9;
      c.fillText(e.icon,0,0);
    }
    // HP bar
    if(!e.dying && e.hp<e.maxHp) {
      const bw=e.sz*3.5, pct=Math.max(0,e.hp/e.maxHp);
      const by=-e.sz-14;
      c.globalAlpha=dying_a*0.85;
      c.fillStyle='rgba(0,0,0,0.8)';
      c.fillRect(-bw/2,by,bw,5);
      const hpCol=pct>0.6?'#22cc44':pct>0.3?'#ccaa00':'#cc2200';
      c.fillStyle=hpCol;
      c.fillRect(-bw/2,by,bw*pct,5);
      // boss name above HP
      if(e.boss&&!e.dying) {
        c.globalAlpha=dying_a*0.7;
        c.font='9px Rajdhani'; c.textAlign='center'; c.textBaseline='bottom';
        c.fillStyle='#ffddaa'; c.fillText(e.name,-0,by-2);
      }
    }
    c.restore();
  }

  // Bullets
  if(G) for(const b of G.bullets) {
    c.save();
    c.shadowColor='#ffff88'; c.shadowBlur=12;
    c.fillStyle='#ffffcc';
    c.beginPath(); c.arc(b.x,b.y,3.5,0,Math.PI*2); c.fill();
    c.shadowBlur=0; c.restore();
  }

  // Player position
  const pFlash = G && G.muzzleFlash>0;
  c.save(); c.translate(55, GH-55);
  if(pFlash) {
    c.shadowColor='#ffff88'; c.shadowBlur=30;
  }
  c.fillStyle=pFlash?'rgba(255,255,120,0.25)':'rgba(0,255,100,0.12)';
  c.beginPath(); c.arc(0,0,18,0,Math.PI*2); c.fill();
  if(pFlash) {
    c.shadowBlur=0;
    c.fillStyle='rgba(255,255,120,0.6)';
    c.beginPath(); c.arc(0,0,10,0,Math.PI*2); c.fill();
  }
  c.font='20px serif'; c.textAlign='center'; c.textBaseline='middle';
  c.fillText('🎯',0,0);
  c.restore();

  // Scope aim line
  if(G&&G.scoped) {
    c.save(); c.strokeStyle='rgba(0,255,100,0.08)'; c.lineWidth=1;
    c.setLineDash([4,10]);
    c.beginPath(); c.moveTo(55,GH-55); c.lineTo(G.mouse.x,G.mouse.y); c.stroke();
    c.restore();
  }

  // Artillery warning
  if(G&&G.artilleryActive>0) {
    c.save(); c.globalAlpha=0.25+Math.sin(timer*10)*0.2;
    c.fillStyle='#ff6600';
    c.font='bold 13px Orbitron'; c.textAlign='center';
    c.fillText('⚠ 포격 중',w/2,76); c.restore();
  }
}

function drawTerrain(c, w, h, night) {
  // Allied position (left trench)
  const trenchG=c.createLinearGradient(0,90,100,90);
  trenchG.addColorStop(0,'#0a1a06'); trenchG.addColorStop(1,'#152a0a');
  c.fillStyle=trenchG; c.fillRect(10,90,100,h-160);
  // sandbags
  for(let y=110;y<h-80;y+=22) {
    c.fillStyle=night?'#1a1408':'#2a2010';
    c.beginPath(); c.ellipse(28,y,14,6,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(55,y,14,6,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(82,y,14,6,0,0,Math.PI*2); c.fill();
  }
  // enemy area
  c.fillStyle=night?'#1a0a06':'#221008';
  c.fillRect(w-120,90,120,h-160);

  // Trees
  const seed=G?G.terrainSeed:0;
  const trees=[[180,150],[330,240],[500,175],[600,340],[700,200],[750,290],[390,400],[540,440],[250,310]];
  for(let i=0;i<trees.length;i++) {
    const [tx,ty]=trees[i];
    const sway=Math.sin(timer*0.7+i*0.8)*2;
    c.save(); c.translate(tx,ty);
    // trunk
    c.fillStyle=night?'#0a0804':'#1a1208';
    c.fillRect(-3,0,6,20);
    // canopy layers
    c.fillStyle=night?'#050e04':'#1a4a0a';
    c.beginPath(); c.ellipse(sway,0,18,24,0,0,Math.PI*2); c.fill();
    c.fillStyle=night?'#060f05':'#246a12';
    c.beginPath(); c.ellipse(sway,-12,14,18,0,0,Math.PI*2); c.fill();
    c.fillStyle=night?'#081208':'#2a7a18';
    c.beginPath(); c.ellipse(sway,-22,9,13,0,0,Math.PI*2); c.fill();
    c.restore();
  }
  // Craters
  const craters=[[290,310],[510,295],[640,280],[380,430]];
  for(const [cx,cy] of craters) {
    c.fillStyle=night?'#050800':'#080f00';
    c.beginPath(); c.ellipse(cx,cy,30,18,0,0,Math.PI*2); c.fill();
    c.strokeStyle=night?'#0a1200':'#122000';
    c.lineWidth=2; c.beginPath(); c.ellipse(cx,cy,30,18,0,0,Math.PI*2); c.stroke();
    c.fillStyle=night?'#060a00':'#0a1800';
    c.beginPath(); c.ellipse(cx,cy,16,10,0,0,Math.PI*2); c.fill();
  }
  // Horizon
  c.strokeStyle=night?'rgba(60,80,40,0.2)':'rgba(80,110,50,0.3)';
  c.lineWidth=2; c.setLineDash([]);
  c.beginPath(); c.moveTo(0,h*0.28); c.lineTo(w,h*0.28); c.stroke();

  // Night spotlight / torch
  if(night && G) {
    const nightOv=document.getElementById('night-overlay');
    nightOv.style.display='block';
    // draw spotlight on scope canvas later
  }
}

function drawScopeView() {
  if(!G||!G.scoped) return;
  const zoom=G.mis.zoom||3.5;
  const cx=G.mouse.x, cy=G.mouse.y;
  sCtx.save();
  sCtx.fillStyle='#020806'; sCtx.fillRect(0,0,320,320);
  // slight green tint for scope
  sCtx.globalCompositeOperation='source-over';
  sCtx.scale(zoom,zoom);
  sCtx.translate(160/zoom-cx+G.swayX*0.35, 160/zoom-cy+G.swayY*0.35);
  drawScene(sCtx, GW, GH, true);
  sCtx.restore();
  // green tint overlay
  sCtx.save();
  sCtx.globalCompositeOperation='multiply';
  sCtx.fillStyle='rgba(0,30,10,0.25)'; sCtx.fillRect(0,0,320,320);
  sCtx.restore();
  // noise / grain
  sCtx.save();
  sCtx.globalAlpha=0.04;
  for(let i=0;i<200;i++) {
    const gx=Math.random()*320, gy=Math.random()*320;
    sCtx.fillStyle=Math.random()>0.5?'#ffffff':'#000000';
    sCtx.fillRect(gx,gy,1,1);
  }
  sCtx.restore();
  // scope info
  const dist=Math.round(Math.hypot(G.mouse.x-55, G.mouse.y-(GH-55)));
  // wind
  const wAngle=G.wind.angle*180/Math.PI;
  const wDirLabel=['N','NE','E','SE','S','SW','W','NW'][Math.round(wAngle/45)%8];
  document.getElementById('scope-dist').textContent=
    `${dist}m  |  WIND ${G.wind.speed.toFixed(1)}m/s ${wDirLabel}`;
  document.getElementById('scope-state').textContent=
    G.breathHeld ? '● 숨참기 안정' : '○ 흔들림';
  document.getElementById('breath-fill').style.width=(G.breathTimer/3*100)+'%';
}

function drawMinimap() {
  if(!G) return;
  const mw=130, mh=78;
  mmCtx.fillStyle='#04080c'; mmCtx.fillRect(0,0,mw,mh);
  // scale
  const sx=mw/GW, sy=mh/GH;
  // allies
  for(const a of G.allies) {
    mmCtx.fillStyle='#3388ff';
    mmCtx.fillRect(a.x*sx-1.5,a.y*sy-1.5,3,3);
  }
  // enemies
  for(const e of G.enemies) {
    if(!e.alive) continue;
    mmCtx.fillStyle=e.boss?'#ffaa00':'#ff3322';
    mmCtx.fillRect(e.x*sx-1.5,e.y*sy-1.5,3,3);
  }
  // bullets
  for(const b of G.bullets) {
    mmCtx.fillStyle='#ffff88';
    mmCtx.fillRect(b.x*sx-0.5,b.y*sy-0.5,2,2);
  }
  // player
  mmCtx.fillStyle='#00ff88';
  mmCtx.beginPath(); mmCtx.arc(55*sx,(GH-55)*sy,3,0,Math.PI*2); mmCtx.fill();
  // border
  mmCtx.strokeStyle='rgba(0,200,255,0.3)'; mmCtx.lineWidth=1;
  mmCtx.strokeRect(0,0,mw,mh);
  // copy to display
  const disp=document.getElementById('minimap-cv');
  if(disp._ctx) {
    disp._ctx.drawImage(mmCV,0,0);
  }
}

// ══════════════════════════════════════════
//  HUD UPDATES
// ══════════════════════════════════════════
function buildAmmoUI() {
  if(!G) return;
  const container=document.getElementById('ammo-bullets');
  container.innerHTML='';
  for(let i=0;i<G.maxAmmo;i++) {
    const pip=document.createElement('div');
    pip.className='bullet-pip'+(i>=G.ammo?' spent':'');
    if(G.reloading && i<G.ammo) pip.classList.add('reloading');
    container.appendChild(pip);
  }
}

function updateComboUI() {
  if(!G) return;
  const el=document.getElementById('combo-v');
  el.textContent='x'+G.combo;
  el.style.color=G.combo>=5?'#ff2244':G.combo>=3?'#ffaa00':'var(--gold)';
  if(G.combo>1) el.classList.add('pulse');
  setTimeout(()=>el.classList.remove('pulse'),300);
}

function updateHUD() {
  if(!G) return;
  const sv=document.getElementById('score-v');
  sv.textContent=Math.round(G.score).toLocaleString();
  document.getElementById('kill-v').textContent=G.kills;
  const t=Math.max(0,G.time);
  const ts=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  const tv=document.getElementById('timer-v');
  tv.textContent=ts;
  tv.style.color=t<20?'var(--red)':t<60?'var(--gold)':'var(--gold)';
  if(t<20&&G.frame%30<15) tv.style.opacity='0.5'; else tv.style.opacity='1';
  // battle bar
  const ap=Math.max(0,Math.min(100,G.allyPower));
  document.getElementById('ally-bar').style.width=ap+'%';
  document.getElementById('enemy-bar').style.width=(100-ap)+'%';
  const aliveE=G.enemies.filter(e=>e.alive).length;
  document.getElementById('battle-info').textContent=`${G.allies.length} VS ${aliveE}`;
  // HP
  const hpPct=Math.round(G.allyHP);
  document.getElementById('hp-pct').textContent=hpPct+'%';
  document.getElementById('hp-fill').style.width=hpPct+'%';
  const hpFill=document.getElementById('hp-fill');
  hpFill.style.background=hpPct>60?'var(--green)':hpPct>30?'#ccaa00':'var(--red)';
  if(hpPct<20) hpFill.style.animation='blink 0.5s infinite';
  else hpFill.style.animation='none';
  // objectives
  const mis=G.mis;
  const objRow=document.getElementById('objective-row');
  objRow.innerHTML=`
    <span class="obj-item ${G.kills>=mis.killGoal?'done':''}">
      <span class="obj-dot"></span>킬 ${G.kills}/${mis.killGoal}
    </span>
    ${mis.bossGoal>0?`<span class="obj-item ${G.bossKills>=mis.bossGoal?'done':''}">
      <span class="obj-dot"></span>보스 ${G.bossKills}/${mis.bossGoal}
    </span>`:''}
  `;
  // status bar
  const dist=G?Math.round(Math.hypot(G.mouse.x-55,G.mouse.y-(GH-55))):0;
  document.getElementById('range-v').textContent=dist+'m';
  const elev=G?Math.atan2(G.mouse.y-(GH-55),G.mouse.x-55)*180/Math.PI:0;
  document.getElementById('elev-v').textContent=(elev>0?'+':'')+elev.toFixed(1)+'°';
  // wind
  const wd=G.wind.angle*180/Math.PI;
  const wDirs=['→','↗','↑','↖','←','↙','↓','↘'];
  document.getElementById('wind-dir').textContent=wDirs[Math.round(wd/45)%8];
  document.getElementById('wind-spd').textContent=G.wind.speed.toFixed(1)+'m/s';
  // ally count
  document.getElementById('ally-count-v').textContent=`🔵 아군 ${G.allies.length} | 적 ${G.enemies.filter(e=>e.alive).length}`;
  // minimap
  drawMinimap();
}

// ══════════════════════════════════════════
//  UI HELPERS
// ══════════════════════════════════════════
function spawnDN(x,y,v,crit,headshot) {
  const el=document.createElement('div');
  el.className='dnum'+(crit||headshot?' crit-num':'');
  const r=canvas.getBoundingClientRect();
  const size=headshot?26:crit?22:14;
  const col=headshot?'#ffff44':crit?'#ffaa00':'#ffffff';
  el.style.cssText=`left:${r.left+x-24}px;top:${r.top+y-10}px;font-size:${size}px;color:${col};`;
  const label=headshot?`💀 ${v}!`:crit?`${v}!!`:`${v}`;
  el.textContent=label;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(), 980);
}

let toastTimer=null;
function showToast(msg) {
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>t.classList.remove('show'),2200);
}

function showObjPopup(msg) {
  const p=document.getElementById('obj-popup');
  p.style.display='block'; p.textContent=msg; p.classList.add('show');
  setTimeout(()=>{p.classList.remove('show');setTimeout(()=>p.style.display='none',300);},2500);
}

function showKF(msg,col,boss) {
  const kf=document.getElementById('killfeed');
  const it=document.createElement('div');
  it.className='kf'+(boss?' boss-kf':'');
  it.style.color=col||'#ccc'; it.textContent=msg;
  kf.appendChild(it);
  setTimeout(()=>{it.style.opacity='0';it.style.transition='opacity 0.5s';
    setTimeout(()=>it.remove(),550);},2800);
  while(kf.children.length>6) kf.removeChild(kf.firstChild);
}

function triggerHit() {
  const el=document.getElementById('vignette-hit');
  el.classList.add('flash'); el.style.opacity='1';
  setTimeout(()=>{el.classList.remove('flash');el.style.opacity='0';},400);
}

// ══════════════════════════════════════════
//  AUDIO ENGINE (Web Audio API)
// ══════════════════════════════════════════
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}

function createEnvelope(g, vol, attack, decay, delay=0) {
  const ts=ACtx.currentTime+delay;
  g.gain.setValueAtTime(0.0001,ts);
  g.gain.linearRampToValueAtTime(vol,ts+attack);
  g.gain.exponentialRampToValueAtTime(0.0001,ts+attack+decay);
}

function playTone(type,freq,vol,attack,decay,delay=0) {
  if(!ACtx)return;
  try{
    const o=ACtx.createOscillator(), g=ACtx.createGain();
    o.connect(g); g.connect(ACtx.destination);
    o.type=type; o.frequency.value=freq;
    createEnvelope(g,vol,attack,decay,delay);
    o.start(ACtx.currentTime+delay);
    o.stop(ACtx.currentTime+delay+attack+decay+0.05);
  }catch(e){}
}

function playNoise(vol,freq,q,decay,delay=0) {
  if(!ACtx)return;
  try{
    const buf=ACtx.createBuffer(1,ACtx.sampleRate*0.3,ACtx.sampleRate);
    const data=buf.getChannelData(0);
    for(let i=0;i<data.length;i++)data[i]=(Math.random()*2-1);
    const src=ACtx.createBufferSource();
    src.buffer=buf;
    const filter=ACtx.createBiquadFilter();
    filter.type='bandpass'; filter.frequency.value=freq; filter.Q.value=q;
    const g=ACtx.createGain();
    src.connect(filter); filter.connect(g); g.connect(ACtx.destination);
    createEnvelope(g,vol,0.002,decay,delay);
    src.start(ACtx.currentTime+delay);
  }catch(e){}
}

function sfx_shoot() {
  ensureAudio();
  playNoise(0.6, 180, 0.8, 0.15);
  playNoise(0.4, 80, 0.5, 0.22, 0.03);
  playTone('sawtooth',55,0.3,0.003,0.12);
  playNoise(0.2, 1200, 0.3, 0.06, 0.01);
}
function sfx_reload_start() {
  ensureAudio();
  playTone('sine',300,0.15,0.02,0.1);
  playTone('sine',200,0.1,0.02,0.12,0.12);
}
function sfx_reload_done() {
  ensureAudio();
  playTone('square',400,0.15,0.01,0.08);
  playTone('square',600,0.1,0.01,0.06,0.09);
}
function sfx_boss_kill() {
  ensureAudio();
  [440,554,659,880].forEach((f,i)=>playTone('sine',f,0.25,0.03,0.25,i*0.08));
  playNoise(0.3,200,0.5,0.3);
}
function sfx_win() {
  ensureAudio();
  const notes=[523,659,784,880,1047,1319];
  notes.forEach((f,i)=>playTone('sine',f,0.3,0.04,0.3,i*0.1));
}
function sfx_fail() {
  ensureAudio();
  [400,300,200,150].forEach((f,i)=>playTone('sawtooth',f,0.25,0.05,0.4,i*0.18));
}
function sfx_enemy_shot() {
  ensureAudio();
  playNoise(0.25, 250, 0.6, 0.2);
  playTone('sawtooth',80,0.15,0.01,0.15);
}

// ══════════════════════════════════════════
//  TITLE SCREEN
// ══════════════════════════════════════════
function buildTitle() {
  const cleared=JSON.parse(localStorage.getItem('sniper_ultra_clears')||'[]');
  const records=JSON.parse(localStorage.getItem('sniper_ultra_records')||'{}');
  const stats=JSON.parse(localStorage.getItem('sniper_ultra_stats')||'{}');
  // global stats
  document.getElementById('gs-total').textContent=(stats.totalKills||0).toLocaleString();
  document.getElementById('gs-best').textContent=(stats.bestScore||0).toLocaleString();
  document.getElementById('gs-mis').textContent=`${cleared.length}/6`;
  const grid=document.getElementById('mission-grid');
  grid.innerHTML='';
  MISSIONS.forEach((m,i)=>{
    const locked=i>0&&!cleared.includes(i-1);
    const div=document.createElement('div');
    div.className='mis-card'+(locked?' locked':'');
    const rec=records[i];
    const starsHtml='⭐'.repeat(m.stars)+'<span style="opacity:0.2">⭐</span>'.repeat(5-m.stars);
    div.innerHTML=`
      <div class="mc-header">
        <div class="mc-num">${String(i+1).padStart(2,'0')}</div>
        <div class="mc-stars">${starsHtml}</div>
      </div>
      ${cleared.includes(i)?`<div class="mc-clr">✓ 완료</div>`:''}
      <div class="mc-name">${m.name}</div>
      <div class="mc-desc">${m.desc}</div>
      <div class="mc-meta">
        <span class="mc-tag">${m.diff}</span>
        <span class="mc-tag">제한 ${m.timeLimit}s</span>
        <span class="mc-tag">킬 ${m.killGoal}</span>
        ${m.bossGoal>0?`<span class="mc-tag">보스 ${m.bossGoal}</span>`:''}
        ${m.night?`<span class="mc-tag" style="color:#aaddff;border-color:rgba(150,200,255,0.3)">야간</span>`:''}
      </div>
      ${rec?`<div class="mc-reward">최고: ${rec.score.toLocaleString()} [${rec.grade}]</div>`:`<div class="mc-reward">${m.reward.toLocaleString()}원 보상</div>`}
    `;
    if(!locked) {
      div.onclick=()=>{
        selMis=i;
        document.querySelectorAll('.mis-card').forEach(x=>x.classList.remove('sel'));
        div.classList.add('sel');
        document.getElementById('mo-start-btn').disabled=false;
        document.getElementById('mission-name').textContent=m.name;
        ensureAudio();
      };
    }
    grid.appendChild(div);
  });
}

function startMission() {
  if(selMis===null) return;
  document.getElementById('mission-ov').style.display='none';
  initGame(selMis);
}

// ══════════════════════════════════════════
//  INPUT
// ══════════════════════════════════════════
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  if(G){G.mouse.x=e.clientX-r.left;G.mouse.y=e.clientY-r.top;}
});
canvas.addEventListener('click',e=>{
  if(G&&G.phase==='play'){ensureAudio();fire();}
});
canvas.addEventListener('contextmenu',e=>{
  e.preventDefault();
  if(G&&G.phase==='play'){ensureAudio();toggleScope();}
});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift'&&G)G.breathHeld=true;
  if(e.key===' '){e.preventDefault();if(G&&G.phase==='play'){ensureAudio();fire();}}
  if((e.key==='r'||e.key==='R')&&G&&G.phase==='play')startReload();
  if((e.key==='z'||e.key==='Z')&&G&&G.phase==='play'){ensureAudio();toggleScope();}
  if(e.key==='Escape') {
    if(G&&G.scoped){toggleScope();}
    else if(G&&G.phase==='play'&&!G.done){if(confirm('타이틀로 돌아가시겠습니까?'))gotoTitle();}
  }
});
document.addEventListener('keyup',e=>{
  if(e.key==='Shift'&&G)G.breathHeld=false;
});

// ══════════════════════════════════════════
//  MAIN LOOP
// ══════════════════════════════════════════
function loop(ts) {
  const dt=Math.min((ts-lastTs)/1000, 0.05);
  lastTs=ts; timer+=dt;
  ctx.clearRect(0,0,GW,GH);
  if(G&&G.phase==='play'){
    tick(dt);
    drawScene(ctx, GW, GH, false);
    drawScopeView();
  } else {
    ctx.fillStyle='#04060a'; ctx.fillRect(0,0,GW,GH);
  }
  RAF=requestAnimationFrame(loop);
}

// ══════════════════════════════════════════
//  MINIMAP SETUP
// ══════════════════════════════════════════
function updateMinimap() {
  const mm=document.getElementById('minimap');
  const cv=document.getElementById('minimap-cv');
  if(G) {
    mm.style.display='block';
    cv.style.display='block';
    cv._ctx=cv.getContext('2d');
  } else {
    mm.style.display='none';
  }
}

// ══════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════
buildTitle();
RAF=requestAnimationFrame(loop);
</script>
</body>
</html>"""


def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import load_db, save_db
    from utils.config import USERS_FILE

    qp = st.query_params
    if qp.get('sniper_score'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            s_score = int(qp.get('sniper_score', 0))
            s_grade = qp.get('sniper_grade', '')
            if uid and s_score > 0:
                _users = load_db(USERS_FILE, {})
                cur_rec = _users.get(uid, {}).get(
                    'game_records',
                    st.session_state.get('game_records', {})
                )
                if s_score > cur_rec.get('sniper', {}).get('score', 0):
                    cur_rec.setdefault('sniper', {}).update(
                        {'score': s_score, 'grade': s_grade}
                    )
                    st.session_state.game_records = cur_rec
                    if uid in _users:
                        _users[uid]['game_records'] = cur_rec
                        save_db(USERS_FILE, _users)
                    sync_user_data()
                    st.toast(
                        f"🏆 스나이퍼 신기록! {s_score:,}점 ({s_grade}등급)",
                        icon="🎯"
                    )
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Orbitron:wght@700;900&family=Share+Tech+Mono&display=swap');
    </style>
    <div style='
      background:linear-gradient(135deg,#04080c,#080e18,#04080c);
      border:1px solid rgba(0,200,255,0.2);
      border-radius:16px;padding:14px 22px;margin-bottom:10px;
      display:flex;align-items:center;gap:18px;
      box-shadow:0 4px 24px rgba(0,0,0,0.5),inset 0 1px 0 rgba(0,200,255,0.08);
      position:relative;overflow:hidden;'>
      <div style='position:absolute;inset:0;
        background:repeating-linear-gradient(0deg,transparent,transparent 3px,rgba(0,200,255,0.015) 3px,rgba(0,200,255,0.015) 4px);
        pointer-events:none;'></div>
      <div style='font-size:2.2rem;filter:drop-shadow(0 0 8px rgba(245,197,24,0.5));'>🎯</div>
      <div>
        <div style='font-family:"Orbitron",sans-serif;font-size:1.15rem;font-weight:900;
          color:#f5c518;letter-spacing:3px;
          text-shadow:0 0 20px rgba(245,197,24,0.4);'>
          스나이퍼 엘리트 ULTRA
        </div>
        <div style='font-family:"Share Tech Mono",monospace;font-size:0.78rem;color:#00ccff;
          margin-top:3px;letter-spacing:2px;'>
          ELITE WAR SNIPER — 전장의 저격수
        </div>
        <div style='font-size:0.74rem;color:#3a5a6a;margin-top:5px;
          font-family:"Share Tech Mono",monospace;letter-spacing:1px;'>
          🖱 클릭/SPACE: 발사 &nbsp;|&nbsp; 우클릭/Z: 스코프 &nbsp;|&nbsp;
          R: 재장전 &nbsp;|&nbsp; SHIFT: 숨참기 &nbsp;|&nbsp; ESC: 타이틀
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
      iframe{border:none!important;border-radius:14px;
        box-shadow:0 8px 40px rgba(0,0,0,0.6);}
    </style>
    """, unsafe_allow_html=True)

    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'sniper_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('sniper_score', e.data.score);
        url.searchParams.set('sniper_grade', e.data.grade);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=810, scrolling=False)
