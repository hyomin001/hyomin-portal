import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>스나이퍼 엘리트 ULTRA — 전선의 저격수</title>
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
  --aggro-low:#00ff88;--aggro-mid:#ffaa00;--aggro-high:#ff2244;
}
html,body{width:100%;height:100vh;margin:0;padding:0;overflow:hidden;background:#020305;
  font-family:'Rajdhani',sans-serif;touch-action:none;cursor:crosshair;
  display:flex;align-items:center;justify-content:center;}
#root{position:relative;width:100%;max-width:920px;aspect-ratio:920/660;overflow:hidden;
  background:var(--bg);box-shadow:0 0 30px rgba(0,0,0,0.8);border:1px solid rgba(0,255,100,0.1);}
canvas{width:100%;height:100%;display:block;image-rendering:pixelated;}

#scanlines{position:absolute;inset:0;pointer-events:none;z-index:9;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.08) 2px,rgba(0,0,0,0.08) 4px);
  mix-blend-mode:multiply;}

/* ── TOP HUD ── */
#hud{position:absolute;top:0;left:0;right:0;z-index:100;pointer-events:none;
  background:linear-gradient(180deg,rgba(4,6,10,0.97) 0%,rgba(4,6,10,0.8) 80%,transparent 100%);
  padding:7px 12px 14px;display:flex;align-items:center;gap:7px;border-bottom:1px solid var(--border);}
.hud-block{display:flex;flex-direction:column;align-items:center;
  background:rgba(0,200,255,0.04);border:1px solid var(--border);
  border-radius:6px;padding:3px 9px;min-width:52px;}
.hud-val{font-family:'Orbitron',sans-serif;font-size:14px;font-weight:700;
  color:var(--gold);line-height:1;letter-spacing:0.5px;}
.hud-lbl{font-size:8px;color:var(--textDim);letter-spacing:2px;margin-top:2px;font-family:'Share Tech Mono',monospace;}
.hud-val.pulse{animation:valPulse 0.3s ease;}
@keyframes valPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.2);color:#fff;}}

/* ── AMMO ── */
#ammo-block{display:flex;flex-direction:column;align-items:center;gap:3px;padding:3px 9px;}
#ammo-bullets{display:flex;gap:3px;align-items:flex-end;}
.bullet-pip{width:5px;height:13px;border-radius:2px 2px 1px 1px;
  background:linear-gradient(180deg,var(--gold) 0%,#c8930a 100%);
  border:1px solid rgba(255,200,0,0.4);transition:all 0.2s;}
.bullet-pip.spent{background:rgba(255,255,255,0.06);border-color:rgba(255,255,255,0.08);}

/* ── FRONTLINE BAR ── */
#battle-wrap{flex:1;margin:0 5px;display:flex;flex-direction:column;gap:3px;}
#battle-header{display:flex;justify-content:space-between;align-items:center;}
#mission-name{font-family:'Black Han Sans',sans-serif;font-size:11px;color:var(--cyan);letter-spacing:1px;}
#battle-info{font-size:10px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
#battle-track{height:10px;background:rgba(255,255,255,0.04);border-radius:99px;
  overflow:hidden;position:relative;border:1px solid var(--border);}
#ally-bar{height:100%;background:linear-gradient(90deg,#1144cc,#3388ff,#66aaff);
  transition:width 0.6s ease;box-shadow:0 0 8px rgba(51,136,255,0.6);position:absolute;left:0;top:0;}
#enemy-bar{position:absolute;top:0;right:0;height:100%;
  background:linear-gradient(270deg,#cc1100,#ff3322,#ff6644);
  transition:width 0.6s ease;box-shadow:0 0 8px rgba(255,51,34,0.6);}
#front-marker{position:absolute;top:-2px;height:14px;width:3px;background:#fff;
  border-radius:2px;transform:translateX(-50%);transition:left 0.6s ease;
  box-shadow:0 0 6px #fff;}
#objective-row{display:flex;gap:7px;font-size:9px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
.obj-item{display:flex;align-items:center;gap:3px;}
.obj-dot{width:5px;height:5px;border-radius:50%;background:var(--textDim);}
.obj-item.done .obj-dot{background:var(--green);}
.obj-item.done{color:var(--green);}

/* ── HP & AGGRO ── */
#right-hud{display:flex;flex-direction:column;gap:5px;width:100px;}
#hp-wrap{display:flex;flex-direction:column;gap:2px;}
#hp-lbl{display:flex;justify-content:space-between;font-size:9px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
#hp-track{height:5px;background:rgba(255,255,255,0.04);border-radius:99px;overflow:hidden;border:1px solid var(--border);}
#hp-fill{height:100%;transition:width 0.3s,background 0.5s;border-radius:99px;}
#aggro-wrap{display:flex;flex-direction:column;gap:2px;}
#aggro-lbl{display:flex;justify-content:space-between;font-size:9px;color:var(--textDim);font-family:'Share Tech Mono',monospace;}
#aggro-track{height:5px;background:rgba(255,255,255,0.04);border-radius:99px;overflow:hidden;border:1px solid rgba(255,34,68,0.2);}
#aggro-fill{height:100%;transition:width 0.1s,background 0.3s;border-radius:99px;}

/* ── COVER STATUS ── */
#cover-status{position:absolute;bottom:38px;left:50%;transform:translateX(-50%);
  z-index:110;pointer-events:none;
  background:rgba(0,0,0,0.8);border:1px solid rgba(0,200,100,0.4);
  border-radius:6px;padding:4px 14px;
  font-family:'Share Tech Mono',monospace;font-size:10px;color:#00ff88;letter-spacing:2px;
  opacity:0;transition:opacity 0.25s;}
#cover-status.active{opacity:1;}

/* ── SCOPE OVERLAY ── */
#scope-wrap{position:absolute;inset:0;z-index:50;pointer-events:none;display:none;}
#scope-blackout{position:absolute;inset:0;background:rgba(0,0,0,0.97);}
#scope-lens{position:absolute;border-radius:50%;overflow:hidden;
  left:50%;top:50%;transform:translate(-50%,-50%);
  width:300px;height:300px;
  box-shadow:0 0 0 2000px rgba(0,0,0,0.97),0 0 40px rgba(0,255,100,0.2),inset 0 0 30px rgba(0,0,0,0.5);}
#scope-cv{display:block;width:300px;height:300px;}
#scope-reticle{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:300px;height:300px;pointer-events:none;}
#scope-vignette{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:300px;height:300px;border-radius:50%;pointer-events:none;
  background:radial-gradient(circle,transparent 55%,rgba(0,0,0,0.8) 100%);}
#scope-bottom{position:absolute;bottom:13%;left:50%;transform:translateX(-50%);
  text-align:center;pointer-events:none;}
#scope-dist{font-family:'Share Tech Mono',monospace;font-size:11px;color:var(--scope);letter-spacing:3px;margin-bottom:4px;}
#scope-state{font-size:9px;color:rgba(0,255,100,0.5);letter-spacing:2px;}
#breath-wrap{width:180px;margin:4px auto 0;}
#breath-track{height:3px;background:rgba(255,255,255,0.08);border-radius:99px;overflow:hidden;}
#breath-fill{height:100%;background:var(--green);border-radius:99px;transition:width 0.05s;}
.scope-corner{position:absolute;width:18px;height:18px;border-color:var(--scope);border-style:solid;opacity:0.6;}
.sc-tl{top:28px;left:28px;border-width:2px 0 0 2px;}
.sc-tr{top:28px;right:28px;border-width:2px 2px 0 0;}
.sc-bl{bottom:28px;left:28px;border-width:0 0 2px 2px;}
.sc-br{bottom:28px;right:28px;border-width:0 2px 2px 0;}

/* ── COVER OVERLAY ── */
#cover-overlay{position:absolute;inset:0;z-index:45;pointer-events:none;
  background:rgba(0,0,0,0);transition:background 0.3s;}
#cover-overlay.covering{background:rgba(0,30,10,0.65);}
#cover-vignette{position:absolute;inset:0;
  border-radius:50%;
  background:radial-gradient(ellipse at 50% 80%,transparent 30%,rgba(0,0,0,0.9) 80%);
  opacity:0;transition:opacity 0.3s;}
#cover-overlay.covering #cover-vignette{opacity:1;}

/* ── EFFECTS ── */
#vignette-hit{position:absolute;inset:0;pointer-events:none;z-index:80;
  border-radius:4px;border:6px solid transparent;transition:border-color 0.1s,opacity 0.4s;opacity:0;}
#vignette-hit.flash{border-color:rgba(255,20,50,0.7);
  box-shadow:inset 0 0 80px rgba(255,0,40,0.3);opacity:1;}
#crit-flash{position:absolute;inset:0;pointer-events:none;z-index:79;
  background:rgba(255,220,0,0.12);opacity:0;transition:opacity 0.15s;}
#crit-flash.show{opacity:1;}
#night-overlay{position:absolute;inset:0;pointer-events:none;z-index:8;
  background:radial-gradient(ellipse at 50% 60%,transparent 22%,rgba(0,0,0,0.85) 70%);display:none;}
#aggro-flash{position:absolute;inset:0;pointer-events:none;z-index:81;
  background:rgba(255,0,50,0);transition:background 0.1s;}
#aggro-flash.danger{background:rgba(255,0,50,0.15);animation:aggroPulse 0.5s ease infinite;}
@keyframes aggroPulse{0%,100%{background:rgba(255,0,50,0.1);}50%{background:rgba(255,0,50,0.25);}}

/* ── TOAST / KILLFEED ── */
#toast{position:absolute;top:56px;left:50%;transform:translateX(-50%) translateY(-90px);
  background:var(--panel);border:1px solid var(--border2);
  border-radius:6px;padding:6px 18px;z-index:280;pointer-events:none;
  transition:transform 0.25s cubic-bezier(.34,1.56,.64,1);white-space:nowrap;
  font-size:11px;color:var(--gold);letter-spacing:1px;
  font-family:'Share Tech Mono',monospace;box-shadow:0 4px 20px rgba(0,0,0,0.6);}
#toast.show{transform:translateX(-50%) translateY(0);}
#killfeed{position:absolute;top:58px;right:10px;z-index:200;pointer-events:none;
  display:flex;flex-direction:column;gap:3px;max-width:240px;}
.kf{background:rgba(0,0,0,0.8);border-left:3px solid var(--red);border-radius:3px;
  padding:3px 9px;font-size:10px;color:#ccc;font-family:'Rajdhani',sans-serif;font-weight:600;
  animation:kfIn 0.3s cubic-bezier(.34,1.56,.64,1);letter-spacing:.5px;backdrop-filter:blur(4px);}
.kf.boss-kf{border-left-color:var(--gold);color:var(--gold2);}
.kf.ally-kf{border-left-color:var(--allyBlue);color:#88bbff;}
.kf.front-kf{border-left-color:var(--green);color:#aaffcc;}
@keyframes kfIn{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}

/* ── DAMAGE NUMBERS ── */
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

/* ── STATUS BAR ── */
#status-bar{position:absolute;bottom:0;left:0;right:0;z-index:100;pointer-events:none;
  background:linear-gradient(0deg,rgba(4,6,10,0.95) 0%,rgba(4,6,10,0.6) 80%,transparent 100%);
  padding:8px 12px 6px;display:flex;align-items:center;justify-content:space-between;
  border-top:1px solid var(--border);font-family:'Share Tech Mono',monospace;font-size:10px;}
#status-left{display:flex;gap:12px;color:var(--textDim);}
.sl-item .sv{color:var(--text);}
#status-right{display:flex;gap:9px;align-items:center;color:var(--textDim);}
#reload-bar{width:70px;height:3px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;display:none;}
#reload-fill{height:100%;background:var(--gold);border-radius:99px;transition:width 0.05s linear;}

/* ── CONTROLS BAR ── */
#ctrl-bar{position:absolute;top:60px;left:50%;transform:translateX(-50%);
  z-index:90;pointer-events:none;
  background:var(--panel);border:1px solid var(--border);
  border-radius:20px;padding:4px 13px;
  font-size:9px;color:var(--textDim);letter-spacing:1px;
  display:flex;gap:9px;align-items:center;
  font-family:'Share Tech Mono',monospace;backdrop-filter:blur(6px);opacity:0.7;}
#ctrl-bar kbd{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
  border-radius:3px;padding:1px 5px;color:var(--text);font-size:9px;}

/* ── AGGRO METER (big) ── */
#aggro-meter{position:absolute;bottom:28px;left:50%;transform:translateX(-50%);
  z-index:110;pointer-events:none;display:flex;align-items:center;gap:8px;
  background:rgba(0,0,0,0.7);border:1px solid rgba(255,34,68,0.2);
  border-radius:20px;padding:4px 14px;opacity:0;transition:opacity 0.3s;}
#aggro-meter.visible{opacity:1;}
#aggro-icon{font-size:13px;}
#aggro-bar-big{width:120px;height:6px;background:rgba(255,255,255,0.06);border-radius:99px;overflow:hidden;}
#aggro-fill-big{height:100%;border-radius:99px;transition:width 0.1s,background 0.3s;}
#aggro-pct-lbl{font-family:'Share Tech Mono',monospace;font-size:9px;color:#aaa;min-width:28px;text-align:right;}

/* ── FRONTLINE PUSH EFFECT ── */
#frontline-push{position:absolute;inset:0;z-index:70;pointer-events:none;
  background:transparent;opacity:0;transition:opacity 0.3s;}
#frontline-push.ally-push{background:linear-gradient(90deg,rgba(51,136,255,0.15),transparent 60%);opacity:1;}
#frontline-push.enemy-push{background:linear-gradient(270deg,rgba(255,51,34,0.15),transparent 60%);opacity:1;}

/* ── MISSION SELECT ── */
#mission-ov{position:absolute;inset:0;z-index:300;
  background:radial-gradient(ellipse at 50% 30%,#061018 0%,#020508 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;overflow:hidden;}
#mission-ov::before{content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,200,255,0.015) 2px,rgba(0,200,255,0.015) 4px);
  pointer-events:none;}
.mo-eyebrow{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--cyan);
  letter-spacing:6px;margin-bottom:8px;opacity:0.6;}
.mo-title{font-family:'Black Han Sans',sans-serif;font-size:2.5rem;
  color:var(--gold);letter-spacing:6px;
  text-shadow:0 0 60px rgba(245,197,24,0.4),0 0 120px rgba(245,197,24,0.15);margin-bottom:4px;}
.mo-sub{font-size:0.72rem;color:var(--textDim);letter-spacing:4px;
  font-family:'Share Tech Mono',monospace;margin-bottom:20px;}
.mo-stats-row{display:flex;gap:18px;margin-bottom:18px;}
.mo-stat{text-align:center;background:rgba(0,200,255,0.04);border:1px solid var(--border);
  border-radius:6px;padding:7px 14px;}
.mo-stat-v{font-family:'Orbitron',sans-serif;font-size:15px;font-weight:700;color:var(--gold);}
.mo-stat-l{font-size:9px;color:var(--textDim);letter-spacing:2px;margin-top:2px;font-family:'Share Tech Mono',monospace;}
.mission-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;
  max-width:580px;width:100%;margin-bottom:18px;padding:0 10px;}
.mis-card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
  border-radius:10px;padding:13px 11px;cursor:pointer;
  transition:all 0.22s cubic-bezier(.34,1.56,.64,1);text-align:left;position:relative;overflow:hidden;}
.mis-card:hover:not(.locked),.mis-card.sel{
  border-color:rgba(245,197,24,0.5);background:rgba(245,197,24,0.04);
  transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,0.4),0 0 20px rgba(245,197,24,0.1);}
.mis-card.locked{opacity:0.25;cursor:default;}
.mc-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;}
.mc-num{font-family:'Orbitron',sans-serif;font-size:22px;font-weight:900;color:var(--gold);line-height:1;}
.mc-stars{font-size:9px;}
.mc-name{font-family:'Black Han Sans',sans-serif;font-size:12px;color:var(--text);margin-bottom:3px;}
.mc-desc{font-size:9px;color:var(--textDim);line-height:1.5;margin-bottom:5px;}
.mc-meta{display:flex;gap:5px;flex-wrap:wrap;}
.mc-tag{font-family:'Share Tech Mono',monospace;font-size:8px;
  background:rgba(0,200,255,0.08);border:1px solid var(--border);border-radius:3px;padding:2px 4px;color:var(--cyan);}
.mc-clr{position:absolute;top:7px;right:7px;font-size:9px;color:var(--green);font-family:'Share Tech Mono',monospace;}
.mc-reward{font-size:9px;color:var(--gold2);margin-top:3px;font-family:'Share Tech Mono',monospace;}
.mo-start{padding:11px 50px;
  background:linear-gradient(135deg,rgba(20,60,5,0.9),rgba(40,110,5,0.9));
  border:1px solid rgba(80,180,0,0.5);border-radius:6px;
  color:#88ff44;font-family:'Black Han Sans',sans-serif;font-size:13px;
  letter-spacing:4px;cursor:pointer;transition:all 0.2s;box-shadow:0 0 20px rgba(60,160,0,0.2);}
.mo-start:hover:not(:disabled){transform:scale(1.05);box-shadow:0 0 30px rgba(60,160,0,0.35);}
.mo-start:disabled{opacity:0.3;cursor:default;}

/* ── RESULT OVERLAY ── */
#result-ov{position:absolute;inset:0;z-index:300;
  background:rgba(0,0,0,0.95);backdrop-filter:blur(8px);
  display:none;flex-direction:column;align-items:center;justify-content:center;gap:12px;}
.res-eyebrow{font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:6px;margin-bottom:4px;}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:2.2rem;letter-spacing:6px;}
.grade-display{width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-family:'Orbitron',sans-serif;font-size:32px;font-weight:900;border:3px solid currentColor;margin:0 auto;}
.res-panel{background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:12px;padding:16px 22px;min-width:340px;}
.res-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;}
.rs{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--textDim);
  font-family:'Share Tech Mono',monospace;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);}
.rs:last-child{border-bottom:none;}
.rs b{color:var(--gold);font-weight:600;}
.rs.highlight b{color:var(--green);font-size:13px;}
.new-record{font-size:10px;color:var(--green);letter-spacing:3px;font-family:'Share Tech Mono',monospace;text-align:center;}
.res-btns{display:flex;gap:9px;}
.rbtn{padding:9px 26px;border:none;border-radius:6px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;font-size:12px;letter-spacing:2px;transition:all 0.18s;}
.rbtn:hover{transform:translateY(-2px);}
.rbtn.retry{background:linear-gradient(135deg,rgba(20,60,5,0.9),rgba(40,110,5,0.9));color:#88ff44;border:1px solid rgba(80,180,0,0.5);}
.rbtn.back{background:rgba(255,255,255,0.05);color:#666;border:1px solid rgba(255,255,255,0.1);}

/* ── MINIMAP ── */
#minimap{position:absolute;bottom:28px;right:10px;z-index:100;
  width:120px;height:72px;border-radius:6px;overflow:hidden;
  border:1px solid var(--border2);opacity:0.8;display:none;}
#minimap-cv{display:block;width:120px;height:72px;}

/* ── OBJ POPUP ── */
#obj-popup{position:absolute;top:88px;left:50%;transform:translateX(-50%) translateY(-80px);
  background:var(--panel);border:1px solid var(--border3);border-radius:8px;padding:7px 16px;
  z-index:290;pointer-events:none;transition:transform 0.3s cubic-bezier(.34,1.56,.64,1);
  font-family:'Rajdhani',sans-serif;font-size:12px;font-weight:700;color:var(--gold);
  letter-spacing:2px;text-align:center;box-shadow:0 0 30px rgba(0,200,255,0.15);display:none;}
#obj-popup.show{transform:translateX(-50%) translateY(0);}

/* ── SNIPER WARN ── */
#sniper-warn{position:absolute;inset:0;z-index:60;pointer-events:none;border:4px solid transparent;transition:border-color 0.1s;}
#sniper-warn.active{border-color:rgba(255,0,50,0.8);box-shadow:inset 0 0 100px rgba(255,0,40,0.2);}

/* ── SHAKE ── */
@keyframes artShake{
  0%,100%{transform:translate(0,0);}10%{transform:translate(-3px,2px);}20%{transform:translate(3px,-3px);}
  30%{transform:translate(-2px,3px);}40%{transform:translate(2px,-2px);}50%{transform:translate(-3px,1px);}
  60%{transform:translate(3px,-1px);}70%{transform:translate(-1px,3px);}80%{transform:translate(1px,-2px);}
  90%{transform:translate(-2px,2px);}
}
#root.shaking{animation:artShake 0.5s ease;}
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
    <div class="hud-block" style="min-width:64px;">
      <div class="hud-val" id="timer-v">--:--</div>
      <div class="hud-lbl">TIME</div>
    </div>
    <div class="hud-block" id="ammo-block">
      <div id="ammo-bullets"></div>
      <div class="hud-lbl">AMMO</div>
    </div>
    <div id="battle-wrap">
      <div id="battle-header">
        <span id="mission-name">임무 선택</span>
        <span id="battle-info"></span>
      </div>
      <div id="battle-track">
        <div id="ally-bar" style="width:50%"></div>
        <div id="enemy-bar" style="width:50%"></div>
        <div id="front-marker" style="left:50%"></div>
      </div>
      <div id="objective-row"></div>
    </div>
    <div id="right-hud">
      <div class="hud-block" id="hp-wrap" style="padding:3px 7px;">
        <div id="hp-lbl"><span>아군</span><span id="hp-pct">100%</span></div>
        <div id="hp-track"><div id="hp-fill" style="width:100%;background:var(--green);"></div></div>
        <div class="hud-lbl">ALLY HP</div>
      </div>
      <div class="hud-block" id="aggro-wrap" style="padding:3px 7px;">
        <div id="aggro-lbl"><span>발각</span><span id="aggro-pct">0%</span></div>
        <div id="aggro-track"><div id="aggro-fill" style="width:0%;background:var(--aggro-low);"></div></div>
        <div class="hud-lbl">AGGRO</div>
      </div>
    </div>
  </div>

  <!-- CONTROLS -->
  <div id="ctrl-bar">
    <span><kbd>CLICK</kbd><kbd>SPC</kbd> 발사</span>
    <span><kbd>Z</kbd><kbd>우클</kbd> 스코프</span>
    <span><kbd>C</kbd><kbd>CTRL</kbd> 은폐</span>
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
      <svg id="scope-reticle" viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg">
        <circle cx="150" cy="150" r="147" stroke="rgba(0,255,100,0.25)" stroke-width="1" fill="none"/>
        <line x1="0" y1="150" x2="112" y2="150" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="188" y1="150" x2="300" y2="150" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="150" y1="0" x2="150" y2="112" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <line x1="150" y1="188" x2="150" y2="300" stroke="rgba(0,255,100,0.9)" stroke-width="1.2"/>
        <circle cx="150" cy="150" r="2.5" stroke="rgba(0,255,100,1)" stroke-width="1.5" fill="none"/>
        <line x1="90" y1="160" x2="210" y2="160" stroke="rgba(0,255,100,0.2)" stroke-width="0.8"/>
        <line x1="90" y1="140" x2="210" y2="140" stroke="rgba(0,255,100,0.2)" stroke-width="0.8"/>
        <circle cx="120" cy="150" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="180" cy="150" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="150" cy="120" r="2" fill="rgba(0,255,100,0.5)"/>
        <circle cx="150" cy="180" r="2" fill="rgba(0,255,100,0.5)"/>
      </svg>
      <div class="scope-corner sc-tl"></div>
      <div class="scope-corner sc-tr"></div>
      <div class="scope-corner sc-bl"></div>
      <div class="scope-corner sc-br"></div>
    </div>
    <div id="scope-bottom">
      <div id="scope-dist"></div>
      <div id="scope-state"></div>
      <div id="breath-wrap"><div id="breath-track"><div id="breath-fill" style="width:100%"></div></div></div>
    </div>
  </div>

  <!-- COVER OVERLAY -->
  <div id="cover-overlay"><div id="cover-vignette"></div></div>

  <!-- EFFECTS -->
  <div id="vignette-hit"></div>
  <div id="crit-flash"></div>
  <div id="sniper-warn"></div>
  <div id="aggro-flash"></div>
  <div id="frontline-push"></div>

  <!-- AGGRO METER -->
  <div id="aggro-meter">
    <div id="aggro-icon">👁</div>
    <div id="aggro-bar-big"><div id="aggro-fill-big" style="width:0%;background:var(--aggro-low);"></div></div>
    <div id="aggro-pct-lbl">0%</div>
  </div>

  <!-- COVER STATUS -->
  <div id="cover-status">🛡 은폐 중 — 발각도 감소</div>

  <!-- MINIMAP -->
  <div id="minimap"><canvas id="minimap-cv" width="120" height="72"></canvas></div>

  <!-- TOAST / KILLFEED / OBJ -->
  <div id="toast"></div>
  <div id="killfeed"></div>
  <div id="obj-popup"></div>

  <!-- STATUS BAR -->
  <div id="status-bar">
    <div id="status-left">
      <span class="sl-item">WIND <span class="sv" id="wind-dir">→</span> <span class="sv" id="wind-spd">3m/s</span></span>
      <span class="sl-item">RANGE <span class="sv" id="range-v">---m</span></span>
      <span class="sl-item">ELEV <span class="sv" id="elev-v">+0.0°</span></span>
      <span class="sl-item">FRONT <span class="sv" id="front-v">50%</span></span>
    </div>
    <div id="status-right">
      <div id="reload-bar"><div id="reload-fill" style="width:0%"></div></div>
      <span id="reload-lbl" style="display:none;color:var(--gold);animation:blink 0.5s infinite;font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;">재장전중...</span>
      <span id="ally-count-v" style="color:var(--textDim);font-family:'Share Tech Mono',monospace;font-size:10px;"></span>
    </div>
  </div>

  <!-- MISSION SELECT -->
  <div id="mission-ov">
    <div class="mo-eyebrow">OPERATION BRIEFING</div>
    <div class="mo-title">🎯 스나이퍼 엘리트</div>
    <div class="mo-sub">전선의 저격수 — TACTICAL FRONTLINE SNIPER</div>
    <div class="mo-stats-row" id="global-stats-row">
      <div class="mo-stat"><div class="mo-stat-v" id="gs-total">0</div><div class="mo-stat-l">TOTAL KILLS</div></div>
      <div class="mo-stat"><div class="mo-stat-v" id="gs-best">0</div><div class="mo-stat-l">BEST SCORE</div></div>
      <div class="mo-stat"><div class="mo-stat-v" id="gs-mis">0/6</div><div class="mo-stat-l">MISSIONS</div></div>
    </div>
    <div class="mission-grid" id="mission-grid"></div>
    <button class="mo-start" id="mo-start-btn" disabled onclick="startMission()">임무 시작 ▶</button>
  </div>

  <!-- RESULT -->
  <div id="result-ov">
    <div class="res-eyebrow" id="res-eyebrow"></div>
    <div class="res-title" id="res-title"></div>
    <div class="grade-display" id="grade-disp"></div>
    <div id="new-rec-lbl" class="new-record" style="display:none;">🏆 신기록!</div>
    <div class="res-panel"><div class="res-grid" id="res-stats"></div></div>
    <div class="res-btns">
      <button class="rbtn retry" onclick="retryMission()">재시도 ↺</button>
      <button class="rbtn back" onclick="gotoTitle()">타이틀 ⬛</button>
    </div>
  </div>
</div>

<script>
'use strict';

// ══════════════════════════════════════════
//  CANVAS SETUP
// ══════════════════════════════════════════
const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');
const scopeCV = document.getElementById('scope-cv');
const sCtx = scopeCV.getContext('2d');
const mmCV = document.getElementById('minimap-cv');
const mmCtx = mmCV.getContext('2d');

const GW = 920, GH = 660;
canvas.width = GW; canvas.height = GH;
scopeCV.width = 300; scopeCV.height = 300;

let G = null, selMis = null, RAF, lastTs = 0, timer = 0;

// ══════════════════════════════════════════
//  MISSION DATA
// ══════════════════════════════════════════
const MISSIONS = [
  {id:1,name:'전선 사수',diff:'초급',stars:1,timeLimit:90,killGoal:15,bossGoal:0,allyHPMin:50,
   desc:'전선이 붕괴 직전! 적군 15명을 제거해 전선을 사수하라.',
   reward:5000000,zoom:3.5,critBonus:1.0,
   spawns:[{t:'infantry',n:15}]},
  {id:2,name:'지휘관 암살',diff:'보통',stars:2,timeLimit:120,killGoal:10,bossGoal:1,allyHPMin:30,
   desc:'적 지휘관을 경호대와 함께 제거하라. 지휘관 제거 시 전선이 크게 밀린다.',
   reward:15000000,zoom:4.0,critBonus:1.2,
   spawns:[{t:'infantry',n:8},{t:'commander',n:1},{t:'guard',n:5}]},
  {id:3,name:'포병 무력화',diff:'어려움',stars:3,timeLimit:150,killGoal:20,bossGoal:2,allyHPMin:40,
   desc:'포병 거점을 파괴하고 장교 2명을 제거하라. 발각 시 즉각 포격!',
   reward:30000000,zoom:4.0,critBonus:1.3,
   spawns:[{t:'artillery',n:3},{t:'officer',n:2},{t:'infantry',n:15},{t:'guard',n:5}]},
  {id:4,name:'포위 돌파',diff:'전문가',stars:4,timeLimit:180,killGoal:40,bossGoal:3,allyHPMin:20,
   desc:'사방의 적을 격퇴해 포위망을 돌파하라. 은폐 전술이 핵심!',
   reward:60000000,zoom:4.5,critBonus:1.4,
   spawns:[{t:'infantry',n:25},{t:'officer',n:3},{t:'sniper_e',n:2},{t:'guard',n:10}]},
  {id:5,name:'총사령관 처치',diff:'전설',stars:5,timeLimit:240,killGoal:30,bossGoal:1,allyHPMin:10,
   desc:'최정예 경호대를 돌파하고 총사령관을 제거하라. 발각 즉시 사살 위험.',
   reward:200000000,zoom:5.0,critBonus:1.5,
   spawns:[{t:'infantry',n:15},{t:'guard',n:10},{t:'sniper_e',n:3},{t:'general',n:1}]},
  {id:6,name:'야간 특수작전',diff:'전설+',stars:5,timeLimit:300,killGoal:60,bossGoal:4,allyHPMin:5,
   desc:'야음을 틈타 잠입. 발각도 관리가 생존의 열쇠다.',
   reward:500000000,zoom:5.0,critBonus:1.8,night:true,
   spawns:[{t:'infantry',n:25},{t:'guard',n:15},{t:'officer',n:5},{t:'sniper_e',n:4},{t:'commander',n:3},{t:'general',n:1}]},
];

const ETYPES = {
  infantry:  {name:'보병',   hp:100,col:'#8b2500',sz:8, spd:0.9,xp:100,boss:false,outline:'#cc4422'},
  guard:     {name:'경호원', hp:150,col:'#7a1800',sz:9, spd:1.2,xp:180,boss:false,outline:'#bb3311'},
  officer:   {name:'장교',   hp:220,col:'#5a1200',sz:11,spd:0.8,xp:400,boss:true, outline:'#993300'},
  commander: {name:'지휘관', hp:400,col:'#440000',sz:14,spd:0.6,xp:800,boss:true, outline:'#880000'},
  general:   {name:'총사령관',hp:700,col:'#220000',sz:18,spd:0.5,xp:3000,boss:true,outline:'#660000'},
  artillery: {name:'포병',   hp:450,col:'#5a3200',sz:22,spd:0,  xp:600,boss:true, outline:'#bb6600'},
  sniper_e:  {name:'적저격수',hp:120,col:'#003322',sz:8, spd:0.4,xp:500,boss:true, outline:'#006644'},
};

// ══════════════════════════════════════════
//  GAME STATE
// ══════════════════════════════════════════
function initGame(midx) {
  const mis = MISSIONS[midx];
  G = {
    midx, mis, phase: 'play',
    time: mis.timeLimit, score: 0, kills: 0, bossKills: 0,
    allyHP: 100, allyPower: 50,
    // FRONTLINE: 0=enemy_base, 100=ally_base, starts at 50
    frontline: 50,
    frontlinePushTimer: 0,
    enemies: [], allies: [], bullets: [], particles: [], bloodSplats: [],
    scoped: false, covering: false,
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
    critBonus: mis.critBonus||1,
    terrainSeed: Math.random()*1000,
    muzzleFlash: 0,
    totalDamage: 0, shotsTotal: 0, shotsHit: 0, headshots: 0,
    // AGGRO SYSTEM
    aggro: 0,           // 0–100
    aggroCooldown: 0,   // delay before decay starts
    aggroExposed: false,// TRUE if caught (aggro==100)
    aggroWarnTimer: 0,
    playerHP: 100,      // player's own health
    coverCooldown: 0,
    frontAdvance: 0,    // track ally progress toward 100
    allyChargeT: 0,
    pushFxTimer: 0,
    pushFxDir: 0,       // 1=ally, -1=enemy
  };
  if(mis.night) document.getElementById('night-overlay').style.display='block';
  else document.getElementById('night-overlay').style.display='none';
  document.getElementById('minimap').style.display='block';
  for(let i=0;i<12;i++) spawnAlly();
  buildAmmoUI();
  updateHUD();
  showObjPopup(`임무: ${mis.name}`);
  setCovering(false);
}

function buildQueue(mis) {
  const q=[]; let d=1.5;
  for(const s of mis.spawns) {
    for(let i=0;i<s.n;i++) q.push({t:s.t, delay:d+i*(1.1+Math.random()*0.7)});
    d += s.n*1.1+3;
  }
  q.sort((a,b)=>a.delay-b.delay);
  return q;
}

function spawnAlly() {
  // Allies spawn at/near the frontline X
  const frontX = (G.frontline/100)*(GW-200)+80;
  const y = 130+Math.random()*(GH-230);
  G.allies.push({
    x: Math.max(50, frontX-60+Math.random()*40), y,
    vx: 0.25+Math.random()*0.25,
    phase: Math.random()*Math.PI*2,
    atkT: 0.5+Math.random(),
    col: `hsl(${210+Math.random()*20},80%,${50+Math.random()*15}%)`,
    inCover: false, coverT: 0,
    charging: false, chargeT: 0,
  });
}

function spawnEnemy(type) {
  const t = ETYPES[type];
  const sc = 1+G.midx*0.22;
  const y = 125+Math.random()*(GH-210);
  G.enemies.push({
    type, x: GW+30+Math.random()*80, y,
    vx: -(t.spd*(0.7+Math.random()*0.5)),
    vy: (Math.random()-0.5)*0.3,
    hp: Math.round(t.hp*sc), maxHp: Math.round(t.hp*sc),
    col: t.col, outline: t.outline, sz: t.sz,
    xp: Math.round(t.xp*sc), boss: t.boss,
    name: t.name, alive: true, dying: false, deathT: 0,
    phase: Math.random()*Math.PI*2,
    atkT: 1+Math.random()*2,
    fireT: type==='sniper_e' ? 3+Math.random()*5 : 0,
    special: type, flashT: 0, hitPulse: 0,
    inCover: false, coverT: 2+Math.random()*3,
    suppressT: 0, // suppressed by near-misses
  });
}

// ══════════════════════════════════════════
//  COVER SYSTEM
// ══════════════════════════════════════════
function setCovering(val) {
  G.covering = val;
  const el = document.getElementById('cover-overlay');
  const st = document.getElementById('cover-status');
  if(val) {
    el.classList.add('covering');
    st.classList.add('active');
    if(G.scoped) toggleScope();
  } else {
    el.classList.remove('covering');
    st.classList.remove('active');
  }
}

// ══════════════════════════════════════════
//  AGGRO SYSTEM
// ══════════════════════════════════════════
function addAggro(amount) {
  if(!G) return;
  G.aggro = Math.min(100, G.aggro + amount);
  G.aggroCooldown = 3.5; // seconds before decay starts
  if(G.aggro >= 100 && !G.aggroExposed) triggerAggroMax();
  updateAggroUI();
}

function triggerAggroMax() {
  G.aggroExposed = true;
  G.aggro = 100;
  // Enemy retaliation barrage
  G.playerHP -= 30+Math.random()*20;
  showToast('🚨 발각! 적이 집중 사격합니다!');
  showKF('🚨 발각 — 집중 포격!','#ff0033',false);
  document.getElementById('aggro-flash').classList.add('danger');
  document.getElementById('root').classList.add('shaking');
  setTimeout(()=>{
    document.getElementById('root').classList.remove('shaking');
    document.getElementById('aggro-flash').classList.remove('danger');
  }, 800);
  triggerHit();
  sfx_aggro_max();
  // Extra penalty: artillery/sniper barrage
  G.artilleryActive = 3.0;
  for(let p=0;p<30;p++) spawnParticle(200+Math.random()*500,150+Math.random()*300,'#ff4400','#ffaa00',2+Math.random()*3);
  // Reset aggro with cooldown
  setTimeout(()=>{ G.aggroExposed=false; G.aggro=40; updateAggroUI(); }, 2500);
}

function updateAggroUI() {
  if(!G) return;
  const pct = Math.round(G.aggro);
  document.getElementById('aggro-pct').textContent = pct+'%';
  document.getElementById('aggro-fill').style.width = pct+'%';
  document.getElementById('aggro-pct-lbl').textContent = pct+'%';
  document.getElementById('aggro-fill-big').style.width = pct+'%';
  const col = pct<40 ? 'var(--aggro-low)' : pct<70 ? 'var(--aggro-mid)' : 'var(--aggro-high)';
  document.getElementById('aggro-fill').style.background = col;
  document.getElementById('aggro-fill-big').style.background = col;
  // show meter when non-trivial
  const meter = document.getElementById('aggro-meter');
  meter.className = pct > 5 ? 'visible' : '';
  const icon = pct < 40 ? '👁' : pct < 70 ? '⚠️' : '🔴';
  document.getElementById('aggro-icon').textContent = icon;
}

// ══════════════════════════════════════════
//  FRONTLINE SYSTEM
// ══════════════════════════════════════════
function pushFrontline(amount, byPlayer) {
  const old = G.frontline;
  G.frontline = Math.max(5, Math.min(95, G.frontline + amount));
  if(Math.abs(G.frontline-old) > 0.1) {
    G.pushFxDir = amount > 0 ? 1 : -1;
    G.pushFxTimer = 0.6;
  }
  // Reposition allies toward new frontline
  if(amount > 0) {
    for(const a of G.allies) {
      if(!a.charging) { a.chargeT = 0.5+Math.random()*1.5; a.charging = true; }
    }
    if(byPlayer) {
      showKF(`⬆ 전선 전진! +${Math.abs(amount).toFixed(1)}%`, '#00ff88', false);
    }
  }
}

function getFrontlineX() {
  return (G.frontline/100)*(GW-200)+80;
}

// ══════════════════════════════════════════
//  TICK
// ══════════════════════════════════════════
function tick(dt) {
  if(!G||G.phase!=='play'||G.done) return;
  G.frame++; timer+=dt; G.time-=dt;
  G.swayT+=dt;
  const swayMult = G.breathHeld ? 0.05 : 1;
  G.swayX = Math.sin(G.swayT*0.85)*6*swayMult + Math.sin(G.swayT*2.2)*2.5*swayMult;
  G.swayY = Math.cos(G.swayT*0.68)*5*swayMult + Math.cos(G.swayT*1.9)*2*swayMult;
  G.shootCd = Math.max(0, G.shootCd-dt);
  G.muzzleFlash = Math.max(0, G.muzzleFlash-dt*8);

  // Breath hold
  if(G.breathHeld){ G.breathTimer-=dt*0.45; if(G.breathTimer<=0){G.breathHeld=false;G.breathTimer=0;} }
  else G.breathTimer = Math.min(3, G.breathTimer+dt*0.55);

  // Reload
  if(G.reloading){
    G.reloadTimer-=dt;
    document.getElementById('reload-fill').style.width=Math.max(0,1-G.reloadTimer/G.reloadTotal)*100+'%';
    if(G.reloadTimer<=0){
      G.reloading=false; G.ammo=G.maxAmmo;
      document.getElementById('reload-bar').style.display='none';
      document.getElementById('reload-lbl').style.display='none';
      buildAmmoUI(); sfx_reload_done(); showToast('탄창 장전 완료!');
    }
  }

  // AGGRO decay
  if(G.covering){
    // Fast decay while in cover
    G.aggro = Math.max(0, G.aggro - dt*22);
    updateAggroUI();
  } else {
    G.aggroCooldown = Math.max(0, G.aggroCooldown-dt);
    if(G.aggroCooldown<=0) {
      G.aggro = Math.max(0, G.aggro - dt*4);
      updateAggroUI();
    }
  }

  // Frontline push effect timer
  if(G.pushFxTimer>0) {
    G.pushFxTimer-=dt;
    const el=document.getElementById('frontline-push');
    if(G.pushFxTimer>0){
      el.className=G.pushFxDir>0?'ally-push':'enemy-push';
    } else { el.className=''; }
  }

  // Artillery
  if(G.artilleryActive>0){ G.artilleryActive-=dt; G.allyHP-=dt*7; }

  // Sniper warning
  if(G.sniperWarning>0){
    G.sniperWarning-=dt;
    document.getElementById('sniper-warn').className=G.sniperWarning>0?'active':'';
  }

  // Combo decay
  if(G.comboTimer>0){ G.comboTimer-=dt; if(G.comboTimer<=0){G.combo=1;updateComboUI();} }

  // Spawn enemies
  G.spawnTimer+=dt;
  while(G.spawnQueue.length&&G.spawnQueue[0].delay<=G.spawnTimer) spawnEnemy(G.spawnQueue.shift().t);

  // FRONTLINE auto push from ally power
  const frontX = getFrontlineX();
  const aliveE = G.enemies.filter(e=>e.alive);
  const nearFront = aliveE.filter(e=>Math.abs(e.x-frontX)<120).length;
  // Allies push if fewer enemies near frontline
  if(nearFront < G.allies.length*0.6 && aliveE.length>0) {
    pushFrontline(dt*0.8, false);
  } else if(nearFront > G.allies.length*1.2) {
    pushFrontline(-dt*1.2, false);
  }

  updEnemies(dt); updAllies(dt); updBullets(dt); updParticles(dt);

  // battle ratio
  const ae=G.enemies.filter(e=>e.alive).length, aa=G.allies.length;
  const r=aa/Math.max(1,aa+ae);
  G.allyPower+=(r*100-G.allyPower)*dt*0.09;
  G.allyHP=Math.max(0,Math.min(100,G.allyHP));
  G.playerHP=Math.max(0,Math.min(100,G.playerHP));

  if(G.allyHP<30){ G.allyWarnTimer-=dt; if(G.allyWarnTimer<=0){G.allyWarnTimer=4;showToast('⚠️ 아군이 위험합니다!');} }

  updateHUD(); checkEnd();
}

// ══════════════════════════════════════════
//  ENEMY UPDATE
// ══════════════════════════════════════════
function updEnemies(dt) {
  const frontX = getFrontlineX();
  for(let i=G.enemies.length-1;i>=0;i--){
    const e=G.enemies[i];
    e.flashT=Math.max(0,(e.flashT||0)-dt*8);
    e.hitPulse=Math.max(0,(e.hitPulse||0)-dt*5);
    e.suppressT=Math.max(0,(e.suppressT||0)-dt);
    if(e.dying){e.deathT+=dt;if(e.deathT>0.8)G.enemies.splice(i,1);continue;}
    if(!e.alive) continue;
    e.phase+=dt*2;

    // Cover behavior for enemies
    if(e.coverT>0){
      e.inCover=true;
      e.coverT-=dt;
    } else {
      e.inCover=false;
      if(Math.random()<0.003) e.coverT=1.5+Math.random()*2; // randomly take cover
    }

    // Enemy stops and takes cover when suppressed
    const suppressed = e.suppressT>0;

    if(e.special!=='artillery' && !suppressed) {
      // Enemies advance to/hold frontline position
      const targetX = frontX - e.sz*2 - 10;
      if(e.x > targetX + 20) {
        e.x+=e.vx;
      } else {
        // At frontline, sway/fire
        e.x=targetX+Math.sin(e.phase*0.5)*8;
      }
      e.y=Math.max(110,Math.min(GH-60,e.y+e.vy+Math.sin(e.phase)*0.3));
    }

    // Enemy reaches ally base
    if(e.x<90){
      G.allyHP-=dt*9; e.vx=0;
      e.atkT-=dt;
      if(e.atkT<=0){
        e.atkT=0.7+Math.random();
        G.allyHP-=3+Math.random()*4;
        if(G.allies.length>0&&Math.random()<0.35)
          G.allies.splice(Math.floor(Math.random()*G.allies.length),1);
      }
    }

    // Artillery special
    if(e.special==='artillery'){
      e.atkT-=dt;
      if(e.atkT<=0){
        e.atkT=4+Math.random()*4;
        // Only fire if aggro is high or artillery is not suppressed
        if(!suppressed){
          G.artilleryActive=2.2;
          document.getElementById('root').classList.add('shaking');
          setTimeout(()=>document.getElementById('root').classList.remove('shaking'),500);
          showKF('💥 포격 개시!','#ff7700');
          for(let p=0;p<20;p++) spawnParticle(400+Math.random()*400,200+Math.random()*300,'#ff6600','#ffaa00',2+Math.random()*3);
        }
      }
    }

    // Enemy sniper fires at player
    if(e.special==='sniper_e'){
      e.fireT-=dt;
      if(e.fireT<=0&&e.x<GW-60&&!suppressed){
        e.fireT=3.5+Math.random()*5;
        G.sniperWarning=1.8;
        // Enemy sniper hits player if not in cover
        if(!G.covering){
          G.playerHP-=15+Math.random()*10;
          G.allyHP-=1.5;
          triggerHit();
          showKF('⚠️ 적 저격수 명중!','#ff4400');
        } else {
          showKF('🛡 은폐로 저격 회피!','#00ff88');
        }
        sfx_enemy_shot();
      }
    }
  }
}

// ══════════════════════════════════════════
//  ALLY UPDATE
// ══════════════════════════════════════════
function updAllies(dt) {
  if(G.frame%240===0&&G.allies.length<14&&G.allyHP>20) spawnAlly();
  const frontX = getFrontlineX();
  for(const a of G.allies){
    a.phase+=dt*2.2;
    if(a.charging){
      a.chargeT-=dt;
      if(a.chargeT<=0) a.charging=false;
    }
    // Find nearest enemy at/near frontline
    const ne=G.enemies.filter(e=>e.alive).sort((a,b)=>a.x-b.x)[0];
    if(ne){
      const dx=ne.x-a.x, dy=ne.y-a.y, d=Math.hypot(dx,dy);
      const speed = a.charging ? a.vx*2.5 : a.vx;
      if(d>55){
        a.x+=((dx/d)*speed);
        a.y+=((dy/d)*speed*0.5);
      } else {
        a.atkT-=dt;
        if(a.atkT<=0){
          a.atkT=0.5+Math.random();
          const dmg=5+Math.random()*5;
          ne.hp-=dmg; ne.flashT=0.15;
          if(ne.hp<=0) killE(ne,false);
        }
      }
      // Allies go into cover if many enemies
    } else {
      // No enemy, advance toward frontline
      const tgt=frontX+20+Math.random()*30;
      if(a.x<tgt) a.x+=a.vx*0.4;
    }
    a.y=Math.max(110,Math.min(GH-60,a.y+Math.sin(a.phase)*0.22));
  }
}

// ══════════════════════════════════════════
//  BULLET UPDATE
// ══════════════════════════════════════════
function updBullets(dt) {
  for(let i=G.bullets.length-1;i>=0;i--){
    const b=G.bullets[i];
    const moveX=b.vx*dt*60+G.wind.speed*Math.cos(G.wind.angle)*dt*0.8;
    const moveY=b.vy*dt*60+G.wind.speed*Math.sin(G.wind.angle)*dt*0.4;
    const steps=Math.max(1,Math.ceil(Math.hypot(moveX,moveY)/10));
    const stepX=moveX/steps, stepY=moveY/steps;
    let hit=false;
    for(let s=0;s<steps;s++){
      b.x+=stepX; b.y+=stepY;
      for(const e of G.enemies){
        if(!e.alive) continue;
        const dist = Math.hypot(e.x-b.x,e.y-b.y);
        if(dist<e.sz+5){
          // HIT
          const headshot=Math.random()<(b.crit?0.6:0.15);
          const dmg=b.dmg*(headshot?2:1);
          e.hp-=dmg; e.flashT=0.2; e.hitPulse=1;
          G.totalDamage+=dmg; G.shotsHit++;
          if(headshot) G.headshots++;
          spawnDN(e.x,e.y,Math.round(dmg),b.crit,headshot);
          if(b.crit||headshot){
            document.getElementById('crit-flash').classList.add('show');
            setTimeout(()=>document.getElementById('crit-flash').classList.remove('show'),150);
          }
          for(let p=0;p<12;p++) spawnParticle(e.x,e.y,'#cc1100','#ff2200',1+Math.random()*2);
          G.bloodSplats.push({x:e.x,y:e.y,r:2+Math.random()*4,a:0.4});
          // AGGRO from shooting (suppressed by scoped precision)
          addAggro(G.scoped ? 6 : 12);
          if(e.hp<=0) killE(e,true);
          hit=true; break;
        }
        // Near-miss: suppress enemy, small aggro
        if(dist<e.sz+25 && !hit){
          e.suppressT=Math.max(e.suppressT,1.2+Math.random()*1.5);
          addAggro(G.scoped ? 2 : 4);
        }
      }
      if(hit) break;
    }
    b.life-=dt;
    if(G.frame%2===0&&!hit) spawnParticle(b.x,b.y,'#ffff88','#ffaa44',1);
    if(hit||b.life<=0||b.x<0||b.x>GW||b.y<0||b.y>GH) G.bullets.splice(i,1);
  }
}

function updParticles(dt) {
  for(let i=G.particles.length-1;i>=0;i--){
    const p=G.particles[i];
    p.x+=p.vx*dt*60; p.y+=p.vy*dt*60; p.vy+=0.15*dt*60;
    p.life-=dt*p.decay;
    if(p.life<=0) G.particles.splice(i,1);
  }
}

function spawnParticle(x,y,c1,c2,size){
  const angle=Math.random()*Math.PI*2, spd=0.5+Math.random()*3;
  G.particles.push({x,y,vx:Math.cos(angle)*spd,vy:Math.sin(angle)*spd-1,
    col:Math.random()>0.5?c1:c2,size,life:1,decay:1.5+Math.random()*2});
}

// ══════════════════════════════════════════
//  COMBAT
// ══════════════════════════════════════════
function killE(e,byPlayer){
  if(!e.alive) return;
  e.alive=false; e.dying=true; e.deathT=0;
  for(let p=0;p<(e.boss?25:15);p++) spawnParticle(e.x,e.y,'#cc1100','#ff4422',1.5+Math.random()*2);
  if(byPlayer){
    G.kills++; 
    G.combo=Math.min(G.combo+1,10); G.comboTimer=3.5;
    const comboBonus=1+(G.combo-1)*0.15;
    const scoreAdd=Math.round(e.xp*comboBonus);
    G.score+=scoreAdd; updateComboUI();
    // FRONTLINE PUSH on kill
    const pushAmt = e.boss ? 6 : e.special==='officer'||e.special==='commander'||e.special==='general' ? 5 : 2;
    pushFrontline(pushAmt, true);
    if(e.boss){
      G.bossKills++;
      sfx_boss_kill();
      showToast(`🏆 ${e.name} 처치! 전선 대폭 전진!`);
      showKF(`🏆 ${e.name} 격파! ⬆+${pushAmt}%`,'#f5c518',true);
      showObjPopup(`${e.name} 처치! 전선 전진!`);
    } else {
      showKF(`${e.name} +${scoreAdd} ⬆+${pushAmt}%`,G.combo>=3?'#f5c518':'#ccc',false);
    }
    if(e.special==='artillery'){G.artilleryActive=0;showToast('💣 포병 파괴! 전선 안정화!');}
    const stats=JSON.parse(localStorage.getItem('sniper_ultra_stats')||'{}');
    stats.totalKills=(stats.totalKills||0)+1;
    stats.bestScore=Math.max(stats.bestScore||0,G.score);
    localStorage.setItem('sniper_ultra_stats',JSON.stringify(stats));
  }
}

function fire(){
  if(!G||G.phase!=='play') return;
  if(G.covering){showToast('은폐 해제 후 사격 가능');return;}
  if(G.reloading){showToast('재장전 중!');return;}
  if(G.shootCd>0) return;
  if(G.ammo<=0){startReload();return;}
  G.ammo--; G.shootCd=0.85; G.shotsTotal++;
  G.muzzleFlash=1; buildAmmoUI();
  const crit=Math.random()<(0.15*G.critBonus);
  let wx=G.mouse.x, wy=G.mouse.y;
  const sw=G.breathHeld?0.25:3.5;
  if(G.scoped){wx-=G.swayX*0.35;wy-=G.swayY*0.35;}
  else{wx+=G.swayX*0.35;wy+=G.swayY*0.35;}
  wx+=(Math.random()-0.5)*sw*2;
  wy+=(Math.random()-0.5)*sw*2;
  const ang=Math.atan2(wy-(GH-55),wx-55);
  const spd=920;
  G.bullets.push({x:55,y:GH-55,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd,dmg:80*(crit?2.8:1),crit,life:2});
  for(let p=0;p<15;p++) spawnParticle(55,GH-55,'#ffff88','#ffaa00',1.5+Math.random()*2);
  sfx_shoot();
  if(G.ammo===0) setTimeout(startReload,400);
}

function startReload(){
  if(!G||G.reloading||G.ammo===G.maxAmmo) return;
  G.reloading=true; G.reloadTimer=G.reloadTotal;
  document.getElementById('reload-bar').style.display='block';
  document.getElementById('reload-lbl').style.display='block';
  document.getElementById('reload-fill').style.width='0%';
  sfx_reload_start(); showToast('재장전 중...');
}

function checkEnd(){
  if(G.done) return;
  const mis=G.mis;
  // Lose conditions
  if(G.time<=0||G.allyHP<=0||G.playerHP<=0){G.done=true;showResult(false);return;}
  // Win: frontline reaches enemy base AND kill goal met
  const allBossSpawned=G.spawnQueue.filter(s=>ETYPES[s.t]?.boss).length===0;
  const bossRem=G.enemies.filter(e=>e.alive&&e.boss).length;
  const frontWin=G.frontline>=92;
  const killWin=G.kills>=mis.killGoal&&(mis.bossGoal===0||G.bossKills>=mis.bossGoal);
  if(frontWin&&killWin&&allBossSpawned&&bossRem===0){G.done=true;showResult(true);}
}

function showResult(win){
  G.phase='result';
  if(G.scoped) toggleScope();
  setCovering(false);
  const el=document.getElementById('result-ov');
  document.getElementById('res-eyebrow').textContent=win?'MISSION COMPLETE':'MISSION FAILED';
  document.getElementById('res-eyebrow').style.color=win?'var(--green)':'var(--red)';
  document.getElementById('res-title').textContent=win?'임무 완료!':'임무 실패';
  document.getElementById('res-title').style.color=win?'var(--gold)':'var(--red)';
  const g=grade();
  const gColors={S:'#f5c518',A:'#00d4ff',B:'#00ff88',C:'#aabbcc',D:'#ff6644'};
  const gd=document.getElementById('grade-disp');
  gd.textContent=g; gd.style.color=gColors[g]||'#aaa';
  const elapsed=G.mis.timeLimit-G.time;
  const acc=G.shotsTotal>0?Math.round(G.shotsHit/G.shotsTotal*100):0;
  document.getElementById('res-stats').innerHTML=`
    <div class="rs highlight">점수<b>${Math.round(G.score).toLocaleString()}</b></div>
    <div class="rs">등급<b>${g}</b></div>
    <div class="rs">킬수<b>${G.kills}</b></div>
    <div class="rs">보스처치<b>${G.bossKills}</b></div>
    <div class="rs">정확도<b>${acc}%</b></div>
    <div class="rs">헤드샷<b>${G.headshots}</b></div>
    <div class="rs">전선전진<b>${Math.round(G.frontline)}%</b></div>
    <div class="rs">최고콤보<b>x${Math.max(1,G.combo)}</b></div>
    <div class="rs">경과시간<b>${Math.floor(elapsed/60)}m ${Math.floor(elapsed%60)}s</b></div>
    <div class="rs">아군HP<b>${Math.round(G.allyHP)}%</b></div>
    <div class="rs">플레이어HP<b>${Math.round(G.playerHP)}%</b></div>
    <div class="rs">총피해<b>${Math.round(G.totalDamage).toLocaleString()}</b></div>
  `;
  const saved=JSON.parse(localStorage.getItem('sniper_ultra_records')||'{}');
  const prevBest=saved[G.midx]?.score||0;
  document.getElementById('new-rec-lbl').style.display=(win&&Math.round(G.score)>prevBest)?'block':'none';
  el.style.display='flex';
  if(win){
    const cl=JSON.parse(localStorage.getItem('sniper_ultra_clears')||'[]');
    if(!cl.includes(G.midx)) cl.push(G.midx);
    localStorage.setItem('sniper_ultra_clears',JSON.stringify(cl));
    if(!saved[G.midx]||Math.round(G.score)>prevBest){
      saved[G.midx]={score:Math.round(G.score),grade:g};
      localStorage.setItem('sniper_ultra_records',JSON.stringify(saved));
    }
    sfx_win();
    try{window.parent.postMessage({type:'sniper_result',score:Math.round(G.score),grade:g},'*');}catch(e){}
  } else sfx_fail();
}

function grade(){
  const s=G.score, acc=G.shotsTotal>0?G.shotsHit/G.shotsTotal:0;
  if(s>=80000&&acc>=0.9) return 'S';
  if(s>=50000) return 'A';
  if(s>=30000) return 'B';
  if(s>=15000) return 'C';
  return 'D';
}

function retryMission(){document.getElementById('result-ov').style.display='none';initGame(G.midx);}
function gotoTitle(){
  document.getElementById('result-ov').style.display='none';
  G=null;
  document.getElementById('night-overlay').style.display='none';
  document.getElementById('minimap').style.display='none';
  buildTitle();
  document.getElementById('mission-ov').style.display='flex';
}
function toggleScope(){
  if(!G) return;
  if(G.covering){showToast('은폐 해제 후 스코프 가능');return;}
  G.scoped=!G.scoped;
  document.getElementById('scope-wrap').style.display=G.scoped?'block':'none';
}

// ══════════════════════════════════════════
//  DRAWING
// ══════════════════════════════════════════
function drawScene(c,w,h,forScope){
  const night=G&&G.mis.night;
  // Sky
  const skyG=c.createLinearGradient(0,0,0,h*0.45);
  if(night){skyG.addColorStop(0,'#020408');skyG.addColorStop(1,'#0a1018');}
  else{skyG.addColorStop(0,'#152030');skyG.addColorStop(1,'#253040');}
  c.fillStyle=skyG; c.fillRect(0,0,w,h);

  if(night&&!forScope){
    c.save();
    for(let i=0;i<80;i++){
      const sx=(Math.sin(i*137.5)*0.5+0.5)*w, sy=(Math.cos(i*97.3)*0.5+0.5)*h*0.38;
      const br=0.3+Math.sin(timer*2+i)*0.35;
      c.globalAlpha=br; c.fillStyle='#ffffff';
      c.beginPath(); c.arc(sx,sy,0.7,0,Math.PI*2); c.fill();
    }
    c.restore();
  }

  // Ground
  const gndG=c.createLinearGradient(0,h*0.28,0,h);
  if(night){gndG.addColorStop(0,'#0a140a');gndG.addColorStop(1,'#060c06');}
  else{gndG.addColorStop(0,'#1a3a0a');gndG.addColorStop(1,'#0f2608');}
  c.fillStyle=gndG; c.fillRect(0,h*0.28,w,h);
  drawTerrain(c,w,h,night);

  // Draw frontline indicator on ground
  if(G&&!forScope){
    const fx=getFrontlineX();
    c.save();
    c.globalAlpha=0.25+Math.sin(timer*3)*0.1;
    // Gradient across ground from ally side (blue) to enemy (red)
    const allyG=c.createLinearGradient(0,h*0.28,fx,h);
    allyG.addColorStop(0,'rgba(51,136,255,0.12)');
    allyG.addColorStop(1,'rgba(51,136,255,0.04)');
    c.fillStyle=allyG; c.fillRect(0,h*0.28,fx,h);
    const enemG=c.createLinearGradient(fx,h*0.28,w,h);
    enemG.addColorStop(0,'rgba(255,51,34,0.04)');
    enemG.addColorStop(1,'rgba(255,51,34,0.12)');
    c.fillStyle=enemG; c.fillRect(fx,h*0.28,w-fx,h);
    // Frontline vertical line
    c.globalAlpha=0.35+Math.sin(timer*4)*0.15;
    c.strokeStyle='rgba(255,255,255,0.6)';
    c.lineWidth=2; c.setLineDash([6,8]);
    c.beginPath(); c.moveTo(fx,h*0.28); c.lineTo(fx,h); c.stroke();
    c.setLineDash([]);
    // Label
    c.globalAlpha=0.5;
    c.font='bold 10px Share Tech Mono'; c.textAlign='center';
    c.fillStyle='#ffffff'; c.fillText('FRONT',fx,h*0.30);
    c.restore();
  }

  // Blood splats
  if(G){
    for(const s of G.bloodSplats){
      c.save(); c.globalAlpha=s.a*0.6;
      c.fillStyle='#550000'; c.beginPath(); c.arc(s.x,s.y,s.r,0,Math.PI*2); c.fill();
      c.restore(); s.a-=0.0003;
    }
    G.bloodSplats=G.bloodSplats.filter(s=>s.a>0);
  }

  // Particles
  if(G) for(const p of G.particles){
    c.save(); c.globalAlpha=p.life*0.8;
    c.fillStyle=p.col; c.beginPath(); c.arc(p.x,p.y,p.size,0,Math.PI*2); c.fill();
    c.restore();
  }

  // ── ALLIES (draw as proper soldiers) ──
  if(G) for(const a of G.allies){
    const bob=Math.sin(a.phase)*2;
    c.save(); c.translate(a.x,a.y+bob);
    drawSoldierAlly(c, a.charging);
    c.restore();
  }

  // ── ENEMIES (draw as proper soldiers) ──
  if(G) for(const e of G.enemies){
    if(!e.alive&&!e.dying) continue;
    const da=e.dying?Math.max(0,1-e.deathT/0.8):1;
    c.save(); c.globalAlpha=da;
    c.translate(e.x,e.y+Math.sin(e.phase)*2);
    if(e.dying) c.scale(1+e.deathT*0.5,1+e.deathT*0.5);
    const flash=e.flashT>0;
    const suppressed=e.suppressT>0;
    if(e.special==='artillery'){
      drawArtillery(c,flash,e.inCover,suppressed);
    } else {
      drawSoldierEnemy(c,e,flash,suppressed);
    }
    // HP bar
    if(!e.dying&&e.hp<e.maxHp){
      const bw=e.sz*3.5, pct=Math.max(0,e.hp/e.maxHp), by=-e.sz-14;
      c.globalAlpha=da*0.85;
      c.fillStyle='rgba(0,0,0,0.8)'; c.fillRect(-bw/2,by,bw,5);
      c.fillStyle=pct>0.6?'#22cc44':pct>0.3?'#ccaa00':'#cc2200';
      c.fillRect(-bw/2,by,bw*pct,5);
      if(e.boss&&!e.dying){
        c.globalAlpha=da*0.7;
        c.font='9px Rajdhani'; c.textAlign='center'; c.textBaseline='bottom';
        c.fillStyle='#ffddaa'; c.fillText(e.name,0,by-2);
      }
    }
    c.restore();
  }

  // Bullets
  if(G) for(const b of G.bullets){
    c.save(); c.shadowColor='#ffff88'; c.shadowBlur=12;
    c.fillStyle='#ffffcc'; c.beginPath(); c.arc(b.x,b.y,3.5,0,Math.PI*2); c.fill();
    c.shadowBlur=0; c.restore();
  }

  // Player icon (bottom left)
  const pFlash=G&&G.muzzleFlash>0;
  c.save(); c.translate(55,GH-55);
  if(pFlash){c.shadowColor='#ffff88';c.shadowBlur=30;}
  c.fillStyle=pFlash?'rgba(255,255,120,0.25)':'rgba(0,255,100,0.12)';
  c.beginPath(); c.arc(0,0,18,0,Math.PI*2); c.fill();
  if(pFlash){c.shadowBlur=0;c.fillStyle='rgba(255,255,120,0.6)';c.beginPath();c.arc(0,0,10,0,Math.PI*2);c.fill();}
  // Draw the player sniper
  drawPlayerSniper(c, pFlash, G&&G.covering, G&&G.scoped);
  c.restore();

  if(G&&G.scoped){
    c.save(); c.strokeStyle='rgba(0,255,100,0.08)'; c.lineWidth=1; c.setLineDash([4,10]);
    c.beginPath(); c.moveTo(55,GH-55); c.lineTo(G.mouse.x,G.mouse.y); c.stroke();
    c.restore();
  }
  if(G&&G.artilleryActive>0){
    c.save(); c.globalAlpha=0.25+Math.sin(timer*10)*0.2;
    c.fillStyle='#ff6600'; c.font='bold 13px Orbitron'; c.textAlign='center';
    c.fillText('⚠ 포격 중',w/2,76); c.restore();
  }
}

// ── SOLDIER DRAWING FUNCTIONS ──
function drawPlayerSniper(c, flash, covering, scoped){
  // Body (prone/cover)
  if(covering){
    c.fillStyle='#1a4428'; // dark camo
    c.fillRect(-10,2,20,6); // prone body
    c.fillStyle='#2a5538';
    c.beginPath(); c.arc(10,4,5,0,Math.PI*2); c.fill(); // helmet
    // rifle down
    c.strokeStyle='#444'; c.lineWidth=2;
    c.beginPath(); c.moveTo(-8,6); c.lineTo(0,8); c.stroke();
  } else {
    // Upright sniper
    c.fillStyle=flash?'#88ff88':'#1a4428';
    c.fillRect(-5,-14,10,14); // body
    c.fillStyle=flash?'#ffffff':'#2a5538';
    c.beginPath(); c.arc(0,-18,6,0,Math.PI*2); c.fill(); // head
    // helmet
    c.fillStyle='#1a3a20';
    c.beginPath(); c.arc(0,-19,5,-Math.PI,0); c.fill();
    // rifle
    if(scoped){
      c.strokeStyle='#888'; c.lineWidth=2.5;
      c.beginPath(); c.moveTo(5,-12); c.lineTo(28,-14); c.stroke();
      c.fillStyle='#555'; c.fillRect(10,-17,14,4); // scope box
    } else {
      c.strokeStyle='#666'; c.lineWidth=2;
      c.beginPath(); c.moveTo(5,-12); c.lineTo(22,-13); c.stroke();
    }
  }
}

function drawSoldierAlly(c, charging){
  // Blue team soldier
  const bodyCol = charging ? '#4499ff' : '#1a55cc';
  const helmetCol = charging ? '#66aaff' : '#3366cc';
  // Body
  c.fillStyle=bodyCol;
  c.fillRect(-5,-13,10,13);
  // Head/helmet
  c.fillStyle=helmetCol;
  c.beginPath(); c.arc(0,-17,5.5,0,Math.PI*2); c.fill();
  c.fillStyle='#2255aa';
  c.beginPath(); c.arc(0,-18,4.5,-Math.PI,0); c.fill();
  // Rifle
  c.strokeStyle='#aac'; c.lineWidth=2;
  c.beginPath(); c.moveTo(4,-11); c.lineTo(18,-12); c.stroke();
  // Legs (walking bob)
  c.fillStyle='#0f3388';
  c.fillRect(-4,0,3,7);
  c.fillRect(1,0,3,7);
  // Shadow
  c.save(); c.globalAlpha=0.2; c.fillStyle='#000';
  c.beginPath(); c.ellipse(0,2,6,2,0,0,Math.PI*2); c.fill();
  c.restore();
  // Charge flash
  if(charging){
    c.save(); c.globalAlpha=0.35;
    c.strokeStyle='#88ccff'; c.lineWidth=2;
    c.beginPath(); c.arc(0,-8,12,0,Math.PI*2); c.stroke();
    c.restore();
  }
}

function drawSoldierEnemy(c,e,flash,suppressed){
  const sz=e.sz;
  const baseCol=flash?'#ffffff':e.col;
  const darkCol=flash?'#ffdddd':e.outline;
  const helmetCol=flash?'#ffffff':(e.boss?e.outline:'#550000');
  // Suppressed = crouching
  const crouching=suppressed||e.inCover;
  const yOff=crouching?6:0;
  // Body
  c.fillStyle=baseCol;
  if(crouching){
    c.fillRect(-sz*0.6,yOff-sz*0.8,sz*1.2,sz*0.8);
  } else {
    c.fillRect(-sz*0.55,-sz*1.4,sz*1.1,sz*1.4);
  }
  // Head
  c.fillStyle=darkCol;
  const hy=crouching?yOff-sz*0.9:-sz*1.5;
  c.beginPath(); c.arc(0,hy,sz*0.7,0,Math.PI*2); c.fill();
  // Helmet
  c.fillStyle=helmetCol;
  c.beginPath(); c.arc(0,hy-sz*0.1,sz*0.65,-Math.PI,0); c.fill();
  // Boss star
  if(e.boss&&sz>=11&&!e.dying){
    c.font=`${sz+2}px serif`; c.textAlign='center'; c.textBaseline='middle';
    c.globalAlpha=0.9; c.fillText(e.sz>=14?'⭐':'★',0,hy);
  }
  // Rifle (pointing left)
  const ry=crouching?yOff-sz*0.5:-sz*0.8;
  c.strokeStyle=flash?'#ffaaaa':'#444'; c.lineWidth=1.5;
  c.beginPath(); c.moveTo(-sz*0.5,ry); c.lineTo(-sz*2,ry-sz*0.1); c.stroke();
  // Legs
  if(!crouching){
    c.fillStyle=baseCol;
    c.fillRect(-sz*0.45,0,sz*0.4,sz*0.7);
    c.fillRect(sz*0.05,0,sz*0.4,sz*0.7);
  }
  // Suppressed indicator
  if(suppressed){
    c.save(); c.globalAlpha=0.6;
    c.font='9px Arial'; c.textAlign='center';
    c.fillStyle='#ffff00'; c.fillText('!',0,hy-sz);
    c.restore();
  }
  // Shadow
  c.save(); c.globalAlpha=0.2; c.fillStyle='#000';
  c.beginPath(); c.ellipse(0,crouching?yOff:0,sz*0.7,sz*0.25,0,0,Math.PI*2); c.fill();
  c.restore();
}

function drawArtillery(c,flash,inCover,suppressed){
  const col=flash?'#ffffff':'#5a3200';
  const col2=flash?'#ffffff':'#885500';
  // Tank/Artillery body
  c.fillStyle=col; c.fillRect(-18,-8,36,15);
  c.fillStyle=col2; c.fillRect(-5,-22,10,17);
  // Barrel
  c.strokeStyle=flash?'#ffffff':'#553000'; c.lineWidth=3;
  c.beginPath(); c.moveTo(-5,-18); c.lineTo(suppressed?-5:-18,-18); c.stroke();
  // Wheels
  for(let wx=-14;wx<=14;wx+=10){
    c.fillStyle=flash?'#ffffff':'#2a1800';
    c.beginPath(); c.arc(wx,7,5,0,Math.PI*2); c.fill();
    c.strokeStyle='#1a0e00'; c.lineWidth=1;
    c.beginPath(); c.arc(wx,7,5,0,Math.PI*2); c.stroke();
  }
  // Treads
  c.fillStyle='#222'; c.fillRect(-20,5,40,5);
  // Shadow
  c.save(); c.globalAlpha=0.3; c.fillStyle='#000';
  c.beginPath(); c.ellipse(0,13,20,4,0,0,Math.PI*2); c.fill();
  c.restore();
  // Smoke if suppressed
  if(suppressed){
    c.save(); c.globalAlpha=0.4; c.fillStyle='#aaa';
    c.beginPath(); c.arc(-15,-25+Math.sin(timer*5)*3,8,0,Math.PI*2); c.fill();
    c.restore();
  }
}

function drawScopeView(){
  if(!G||!G.scoped) return;
  const zoom=G.mis.zoom||3.5;
  const cx=G.mouse.x, cy=G.mouse.y;
  sCtx.save();
  sCtx.fillStyle='#020806'; sCtx.fillRect(0,0,300,300);
  sCtx.scale(zoom,zoom);
  sCtx.translate(150/zoom-cx+G.swayX*0.35, 150/zoom-cy+G.swayY*0.35);
  drawScene(sCtx,GW,GH,true);
  sCtx.restore();
  sCtx.save(); sCtx.globalCompositeOperation='multiply';
  sCtx.fillStyle='rgba(0,30,10,0.25)'; sCtx.fillRect(0,0,300,300);
  sCtx.restore();
  sCtx.save(); sCtx.globalAlpha=0.04;
  for(let i=0;i<200;i++){
    const gx=Math.random()*300, gy=Math.random()*300;
    sCtx.fillStyle=Math.random()>0.5?'#ffffff':'#000000';
    sCtx.fillRect(gx,gy,1,1);
  }
  sCtx.restore();
  const dist=Math.round(Math.hypot(G.mouse.x-55,G.mouse.y-(GH-55)));
  const wDirLabel=['N','NE','E','SE','S','SW','W','NW'][Math.round(G.wind.angle*4/Math.PI)%8];
  document.getElementById('scope-dist').textContent=`${dist}m  |  WIND ${G.wind.speed.toFixed(1)}m/s ${wDirLabel}`;
  document.getElementById('scope-state').textContent=G.breathHeld?'● 숨참기 안정':'○ 흔들림';
  document.getElementById('breath-fill').style.width=(G.breathTimer/3*100)+'%';
}

function drawMinimap(){
  if(!G) return;
  const mw=120, mh=72;
  mmCtx.fillStyle='#04080c'; mmCtx.fillRect(0,0,mw,mh);
  const sx=mw/GW, sy=mh/GH;
  // Frontline
  const fx=getFrontlineX()*sx;
  mmCtx.fillStyle='rgba(51,136,255,0.15)'; mmCtx.fillRect(0,0,fx,mh);
  mmCtx.fillStyle='rgba(255,51,34,0.15)'; mmCtx.fillRect(fx,0,mw-fx,mh);
  mmCtx.strokeStyle='rgba(255,255,255,0.4)'; mmCtx.lineWidth=1;
  mmCtx.beginPath(); mmCtx.moveTo(fx,0); mmCtx.lineTo(fx,mh); mmCtx.stroke();
  for(const a of G.allies){mmCtx.fillStyle='#3388ff';mmCtx.fillRect(a.x*sx-1.5,a.y*sy-1.5,3,3);}
  for(const e of G.enemies){
    if(!e.alive) continue;
    mmCtx.fillStyle=e.boss?'#ffaa00':'#ff3322';
    mmCtx.fillRect(e.x*sx-1.5,e.y*sy-1.5,3,3);
  }
  for(const b of G.bullets){mmCtx.fillStyle='#ffff88';mmCtx.fillRect(b.x*sx-0.5,b.y*sy-0.5,2,2);}
  mmCtx.fillStyle='#00ff88';
  mmCtx.beginPath(); mmCtx.arc(55*sx,(GH-55)*sy,3,0,Math.PI*2); mmCtx.fill();
  mmCtx.strokeStyle='rgba(0,200,255,0.3)'; mmCtx.lineWidth=1;
  mmCtx.strokeRect(0,0,mw,mh);
}

// ══════════════════════════════════════════
//  HUD UPDATES
// ══════════════════════════════════════════
function buildAmmoUI(){
  if(!G) return;
  const c=document.getElementById('ammo-bullets'); c.innerHTML='';
  for(let i=0;i<G.maxAmmo;i++){
    const pip=document.createElement('div');
    pip.className='bullet-pip'+(i>=G.ammo?' spent':'');
    c.appendChild(pip);
  }
}

function updateComboUI(){
  if(!G) return;
  const el=document.getElementById('combo-v');
  el.textContent='x'+G.combo;
  el.style.color=G.combo>=5?'#ff2244':G.combo>=3?'#ffaa00':'var(--gold)';
  el.classList.add('pulse');
  setTimeout(()=>el.classList.remove('pulse'),300);
}

function updateHUD(){
  if(!G) return;
  document.getElementById('score-v').textContent=Math.round(G.score).toLocaleString();
  document.getElementById('kill-v').textContent=G.kills;
  const t=Math.max(0,G.time);
  const ts=`${String(Math.floor(t/60)).padStart(2,'0')}:${String(Math.floor(t%60)).padStart(2,'0')}`;
  const tv=document.getElementById('timer-v');
  tv.textContent=ts;
  tv.style.color=t<20?'var(--red)':'var(--gold)';
  if(t<20&&G.frame%30<15) tv.style.opacity='0.5'; else tv.style.opacity='1';
  // Frontline bar
  const fl=G.frontline;
  document.getElementById('ally-bar').style.width=fl+'%';
  document.getElementById('enemy-bar').style.width=(100-fl)+'%';
  document.getElementById('front-marker').style.left=fl+'%';
  document.getElementById('front-v').textContent=Math.round(fl)+'%';
  const aliveE=G.enemies.filter(e=>e.alive).length;
  document.getElementById('battle-info').textContent=`🔵${G.allies.length} 전선 ${Math.round(fl)}% 🔴${aliveE}`;
  // HP
  const hpPct=Math.round(G.allyHP);
  document.getElementById('hp-pct').textContent=hpPct+'%';
  document.getElementById('hp-fill').style.width=hpPct+'%';
  document.getElementById('hp-fill').style.background=hpPct>60?'var(--green)':hpPct>30?'#ccaa00':'var(--red)';
  // Objectives
  const mis=G.mis;
  document.getElementById('objective-row').innerHTML=`
    <span class="obj-item ${G.kills>=mis.killGoal?'done':''}">
      <span class="obj-dot"></span>킬 ${G.kills}/${mis.killGoal}
    </span>
    ${mis.bossGoal>0?`<span class="obj-item ${G.bossKills>=mis.bossGoal?'done':''}">
      <span class="obj-dot"></span>보스 ${G.bossKills}/${mis.bossGoal}
    </span>`:''}
    <span class="obj-item ${G.frontline>=92?'done':''}">
      <span class="obj-dot"></span>전진 ${Math.round(G.frontline)}%
    </span>
  `;
  // Status bar
  const dist=Math.round(Math.hypot(G.mouse.x-55,G.mouse.y-(GH-55)));
  document.getElementById('range-v').textContent=dist+'m';
  const elev=Math.atan2(G.mouse.y-(GH-55),G.mouse.x-55)*180/Math.PI;
  document.getElementById('elev-v').textContent=(elev>0?'+':'')+elev.toFixed(1)+'°';
  const wDirs=['→','↗','↑','↖','←','↙','↓','↘'];
  document.getElementById('wind-dir').textContent=wDirs[Math.round(G.wind.angle*4/Math.PI)%8];
  document.getElementById('wind-spd').textContent=G.wind.speed.toFixed(1)+'m/s';
  document.getElementById('ally-count-v').textContent=`플레이어HP ${Math.round(G.playerHP)}%`;
  drawMinimap();
}

// ══════════════════════════════════════════
//  UI HELPERS
// ══════════════════════════════════════════
function spawnDN(x,y,v,crit,headshot){
  const el=document.createElement('div');
  el.className='dnum'+(crit||headshot?' crit-num':'');
  const r=canvas.getBoundingClientRect();
  const size=headshot?26:crit?22:14;
  const col=headshot?'#ffff44':crit?'#ffaa00':'#ffffff';
  const screenX=r.left+x*(r.width/canvas.width);
  const screenY=r.top+y*(r.height/canvas.height);
  el.style.cssText=`left:${screenX-24}px;top:${screenY-10}px;font-size:${size}px;color:${col};`;
  el.textContent=headshot?`💀 ${v}!`:crit?`${v}!!`:`${v}`;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),980);
}

let toastTimer=null;
function showToast(msg){
  const t=document.getElementById('toast');
  t.textContent=msg; t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer=setTimeout(()=>t.classList.remove('show'),2200);
}
function showObjPopup(msg){
  const p=document.getElementById('obj-popup');
  p.style.display='block'; p.textContent=msg; p.classList.add('show');
  setTimeout(()=>{p.classList.remove('show');setTimeout(()=>p.style.display='none',300);},2500);
}
function showKF(msg,col,boss){
  const kf=document.getElementById('killfeed');
  const it=document.createElement('div');
  it.className='kf'+(boss?' boss-kf':'');
  it.style.color=col||'#ccc'; it.textContent=msg;
  kf.appendChild(it);
  setTimeout(()=>{it.style.opacity='0';it.style.transition='opacity 0.5s';setTimeout(()=>it.remove(),550);},2800);
  while(kf.children.length>6) kf.removeChild(kf.firstChild);
}
function triggerHit(){
  const el=document.getElementById('vignette-hit');
  el.classList.add('flash'); el.style.opacity='1';
  setTimeout(()=>{el.classList.remove('flash');el.style.opacity='0';},400);
}

// ══════════════════════════════════════════
//  AUDIO
// ══════════════════════════════════════════
let ACtx=null;
function ensureAudio(){if(!ACtx)try{ACtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}}
function createEnvelope(g,vol,attack,decay,delay=0){
  const ts=ACtx.currentTime+delay;
  g.gain.setValueAtTime(0.0001,ts);
  g.gain.linearRampToValueAtTime(vol,ts+attack);
  g.gain.exponentialRampToValueAtTime(0.0001,ts+attack+decay);
}
function playTone(type,freq,vol,attack,decay,delay=0){
  if(!ACtx)return;
  try{
    const o=ACtx.createOscillator(),g=ACtx.createGain();
    o.connect(g);g.connect(ACtx.destination);
    o.type=type;o.frequency.value=freq;
    createEnvelope(g,vol,attack,decay,delay);
    o.start(ACtx.currentTime+delay);
    o.stop(ACtx.currentTime+delay+attack+decay+0.05);
  }catch(e){}
}
function playNoise(vol,freq,q,decay,delay=0){
  if(!ACtx)return;
  try{
    const buf=ACtx.createBuffer(1,ACtx.sampleRate*0.3,ACtx.sampleRate);
    const data=buf.getChannelData(0);
    for(let i=0;i<data.length;i++) data[i]=(Math.random()*2-1);
    const src=ACtx.createBufferSource();
    src.buffer=buf;
    const filter=ACtx.createBiquadFilter();
    filter.type='bandpass';filter.frequency.value=freq;filter.Q.value=q;
    const g=ACtx.createGain();
    src.connect(filter);filter.connect(g);g.connect(ACtx.destination);
    createEnvelope(g,vol,0.002,decay,delay);
    src.start(ACtx.currentTime+delay);
  }catch(e){}
}
function sfx_shoot(){ensureAudio();playNoise(0.6,180,0.8,0.15);playNoise(0.4,80,0.5,0.22,0.03);playTone('sawtooth',55,0.3,0.003,0.12);}
function sfx_reload_start(){ensureAudio();playTone('sine',300,0.15,0.02,0.1);playTone('sine',200,0.1,0.02,0.12,0.12);}
function sfx_reload_done(){ensureAudio();playTone('square',400,0.15,0.01,0.08);playTone('square',600,0.1,0.01,0.06,0.09);}
function sfx_boss_kill(){ensureAudio();[440,554,659,880].forEach((f,i)=>playTone('sine',f,0.25,0.03,0.25,i*0.08));playNoise(0.3,200,0.5,0.3);}
function sfx_win(){ensureAudio();[523,659,784,880,1047,1319].forEach((f,i)=>playTone('sine',f,0.3,0.04,0.3,i*0.1));}
function sfx_fail(){ensureAudio();[400,300,200,150].forEach((f,i)=>playTone('sawtooth',f,0.25,0.05,0.4,i*0.18));}
function sfx_enemy_shot(){ensureAudio();playNoise(0.25,250,0.6,0.2);playTone('sawtooth',80,0.15,0.01,0.15);}
function sfx_aggro_max(){
  ensureAudio();
  playNoise(0.5,300,0.4,0.3);
  [200,150,100].forEach((f,i)=>playTone('sawtooth',f,0.3,0.03,0.3,i*0.12));
}

// ══════════════════════════════════════════
//  TITLE SCREEN
// ══════════════════════════════════════════
function buildTitle(){
  const cleared=JSON.parse(localStorage.getItem('sniper_ultra_clears')||'[]');
  const records=JSON.parse(localStorage.getItem('sniper_ultra_records')||'{}');
  const stats=JSON.parse(localStorage.getItem('sniper_ultra_stats')||'{}');
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
    if(!locked){
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

function startMission(){
  if(selMis===null) return;
  document.getElementById('mission-ov').style.display='none';
  initGame(selMis);
}

// ══════════════════════════════════════════
//  INPUT
// ══════════════════════════════════════════
canvas.addEventListener('mousemove',e=>{
  const r=canvas.getBoundingClientRect();
  if(G){
    G.mouse.x=(e.clientX-r.left)*(canvas.width/r.width);
    G.mouse.y=(e.clientY-r.top)*(canvas.height/r.height);
  }
});
canvas.addEventListener('click',e=>{if(G&&G.phase==='play'){ensureAudio();fire();}});
canvas.addEventListener('contextmenu',e=>{e.preventDefault();if(G&&G.phase==='play'){ensureAudio();toggleScope();}});
document.addEventListener('keydown',e=>{
  if(e.key==='Shift'&&G) G.breathHeld=true;
  if(e.key===' '){e.preventDefault();if(G&&G.phase==='play'){ensureAudio();fire();}}
  if((e.key==='r'||e.key==='R')&&G&&G.phase==='play') startReload();
  if((e.key==='z'||e.key==='Z')&&G&&G.phase==='play'){ensureAudio();toggleScope();}
  if((e.key==='c'||e.key==='C'||e.key==='Control')&&G&&G.phase==='play'){
    ensureAudio();
    setCovering(!G.covering);
  }
  if(e.key==='Escape'){
    if(G&&G.scoped) toggleScope();
    else if(G&&G.covering) setCovering(false);
    else if(G&&G.phase==='play'&&!G.done){if(confirm('타이틀로 돌아가시겠습니까?'))gotoTitle();}
  }
});
document.addEventListener('keyup',e=>{if(e.key==='Shift'&&G) G.breathHeld=false;});

// ══════════════════════════════════════════
//  MAIN LOOP
// ══════════════════════════════════════════
function loop(ts){
  const dt=Math.min((ts-lastTs)/1000,0.05);
  lastTs=ts; timer+=dt;
  ctx.clearRect(0,0,GW,GH);
  if(G&&G.phase==='play'){
    tick(dt);
    drawScene(ctx,GW,GH,false);
    drawScopeView();
  } else {
    ctx.fillStyle='#04060a'; ctx.fillRect(0,0,GW,GH);
  }
  RAF=requestAnimationFrame(loop);
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
          TACTICAL FRONTLINE SNIPER — 전선의 저격수
        </div>
        <div style='font-size:0.74rem;color:#3a5a6a;margin-top:5px;
          font-family:"Share Tech Mono",monospace;letter-spacing:1px;'>
          🖱 클릭/SPACE: 발사 &nbsp;|&nbsp; 우클릭/Z: 스코프 &nbsp;|&nbsp;
          C/CTRL: 은폐 &nbsp;|&nbsp; R: 재장전 &nbsp;|&nbsp; SHIFT: 숨참기 &nbsp;|&nbsp; ESC: 타이틀
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
