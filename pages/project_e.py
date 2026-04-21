import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>⚔️ DUNGEON CRAWLER</title>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Noto+Sans+KR:wght@300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#000;--bg2:#050810;--bg3:#0a1020;
  --border:rgba(180,120,40,0.25);--border2:rgba(180,120,40,0.5);
  --gold:#e8a020;--gold2:#ffd060;--gold3:#ffec90;
  --red:#c0392b;--red2:#e74c3c;--redbright:#ff4444;
  --green:#27ae60;--green2:#2ecc71;
  --blue:#1a6fa0;--blue2:#3498db;
  --purple:#6c3483;--purple2:#9b59b6;
  --cyan:#0e7490;--cyan2:#22d3ee;
  --text:#d4b896;--text2:#8a7060;--text3:#4a3a2a;
  --stone:#1a1510;--stone2:#2a2018;--stone3:#3a2e22;
  --glow-gold:0 0 12px rgba(232,160,32,0.6),0 0 40px rgba(232,160,32,0.2);
  --glow-red:0 0 12px rgba(192,57,43,0.7),0 0 40px rgba(192,57,43,0.25);
  --shadow:0 8px 40px rgba(0,0,0,0.95);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{width:100%;height:100%;background:#000;overflow:hidden;font-family:'Share Tech Mono',monospace;}

/* ── LAYOUT ── */
#app{display:flex;flex-direction:column;width:100vw;height:100vh;background:#000;}
#topbar{
  height:38px;background:linear-gradient(180deg,#0d0a06,#060403);
  border-bottom:1px solid var(--border2);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 14px;flex-shrink:0;
  box-shadow:0 2px 12px rgba(0,0,0,0.8);
}
#topbar .logo{
  font-family:'Cinzel',serif;font-size:0.9rem;font-weight:900;
  color:var(--gold);letter-spacing:3px;
  text-shadow:var(--glow-gold);
}
.top-stat{display:flex;align-items:center;gap:5px;font-size:0.65rem;color:var(--text2);}
.top-stat span{color:var(--gold);font-weight:700;}
.floor-badge{
  font-family:'Cinzel',serif;font-size:0.72rem;
  background:rgba(232,160,32,0.1);border:1px solid var(--border2);
  color:var(--gold);padding:2px 10px;border-radius:3px;
  text-shadow:var(--glow-gold);
}
#main{display:flex;flex:1;overflow:hidden;}

/* ── 3D VIEW ── */
#view3d-wrap{
  flex:1;position:relative;background:#000;
  display:flex;flex-direction:column;
}
#view3d{
  flex:1;position:relative;overflow:hidden;cursor:default;
}
canvas#dungeon3d{
  width:100%;height:100%;display:block;
  image-rendering:pixelated;
}
/* combat flash */
#hit-flash{
  position:absolute;inset:0;pointer-events:none;
  background:rgba(192,57,43,0);transition:background 0.08s;
  z-index:10;
}
/* center crosshair */
#crosshair{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:20px;height:20px;pointer-events:none;z-index:5;
}
#crosshair::before,#crosshair::after{
  content:'';position:absolute;background:rgba(232,160,32,0.7);
}
#crosshair::before{width:2px;height:12px;top:4px;left:9px;}
#crosshair::after{width:12px;height:2px;top:9px;left:4px;}

/* ── MINIMAP ── */
#minimap-wrap{
  position:absolute;top:8px;right:8px;
  width:110px;height:110px;
  background:rgba(0,0,0,0.85);border:1px solid var(--border2);
  border-radius:4px;overflow:hidden;z-index:20;
}
#minimap-canvas{width:100%;height:100%;}
#minimap-label{
  position:absolute;bottom:2px;left:0;right:0;text-align:center;
  font-size:0.5rem;color:var(--text2);letter-spacing:1px;
}

/* ── HUD bars ── */
#hud{
  position:absolute;bottom:0;left:0;right:0;
  padding:6px 10px;background:linear-gradient(0deg,rgba(0,0,0,0.95),transparent);
  display:flex;gap:10px;align-items:flex-end;z-index:15;
}
.hud-bar-wrap{flex:1;max-width:180px;}
.hud-bar-label{font-size:0.58rem;color:var(--text2);margin-bottom:2px;display:flex;justify-content:space-between;}
.hud-bar-label span{color:var(--gold);}
.hud-bar{height:8px;background:rgba(255,255,255,0.07);border-radius:2px;overflow:hidden;border:1px solid rgba(255,255,255,0.05);}
.hud-bar-fill{height:100%;border-radius:2px;transition:width 0.25s;}
.hp-fill{background:linear-gradient(90deg,#7b1a1a,var(--redbright));}
.xp-fill{background:linear-gradient(90deg,#3a1a6a,var(--purple2));}
.mp-fill{background:linear-gradient(90deg,#0a3a5a,var(--cyan2));}

/* skill bar */
#skillbar{
  display:flex;gap:4px;margin-left:auto;align-items:flex-end;
}
.skill-slot{
  width:36px;height:36px;border-radius:4px;
  background:rgba(0,0,0,0.8);border:1px solid var(--border);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:16px;position:relative;cursor:pointer;transition:all 0.15s;
}
.skill-slot:hover{border-color:var(--gold);}
.skill-slot.active-skill{border-color:var(--gold);box-shadow:var(--glow-gold);}
.skill-slot.on-cooldown{opacity:0.4;}
.skill-slot .sk-key{
  position:absolute;bottom:1px;right:2px;
  font-size:0.45rem;color:var(--text2);font-family:'Share Tech Mono',monospace;
}
.skill-slot .sk-cd{
  position:absolute;inset:0;background:rgba(0,0,0,0.7);
  display:flex;align-items:center;justify-content:center;
  font-size:0.6rem;color:var(--gold);border-radius:4px;
}

/* ── RIGHT PANEL ── */
#panel{
  width:230px;min-width:230px;background:var(--bg2);
  border-left:1px solid var(--border2);
  display:flex;flex-direction:column;overflow:hidden;
}
/* ── Panel sections ── */
.panel-sec{padding:8px 10px;border-bottom:1px solid var(--border);}
.psec-title{
  font-family:'Cinzel',serif;font-size:0.58rem;
  color:var(--text2);letter-spacing:2px;margin-bottom:6px;
  border-bottom:1px solid rgba(232,160,32,0.1);padding-bottom:3px;
}

/* stat grid */
.stat-grid2{display:grid;grid-template-columns:1fr 1fr;gap:3px;}
.sg-item{
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:3px;padding:3px 5px;
}
.sg-label{font-size:0.55rem;color:var(--text2);}
.sg-val{font-size:0.72rem;font-weight:700;color:var(--gold);}

/* equipped */
#equipped-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-top:2px;}
.eq-slot{
  aspect-ratio:1;background:rgba(255,255,255,0.03);
  border:1px solid var(--border);border-radius:3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:14px;cursor:pointer;transition:all 0.15s;position:relative;
}
.eq-slot:hover{border-color:var(--gold);}
.eq-slot.filled{border-color:rgba(232,160,32,0.4);}
.eq-slot .eq-label{font-size:0.4rem;color:var(--text2);margin-top:2px;text-align:center;}

/* log */
#log-wrap{flex:1;overflow-y:auto;padding:6px 10px;}
#log-wrap h4{font-family:'Cinzel',serif;font-size:0.55rem;color:var(--text2);letter-spacing:2px;margin-bottom:4px;}
.le{font-size:0.62rem;line-height:1.5;margin-bottom:1px;padding:1px 3px;border-radius:2px;}
.le-player{color:#4ade80;}
.le-monster{color:#f87171;}
.le-item{color:var(--gold2);}
.le-system{color:var(--cyan2);}
.le-boss{color:#fb923c;font-weight:700;}
.le-skill{color:var(--purple2);}
.le-crit{color:var(--gold3);background:rgba(255,215,0,0.07);}

/* ── CONTROLS BAR ── */
#ctrlbar{
  height:28px;background:#030202;border-top:1px solid var(--border);
  display:flex;align-items:center;gap:12px;padding:0 12px;
  font-size:0.6rem;color:var(--text2);flex-shrink:0;
}
.kb{
  background:rgba(232,160,32,0.08);border:1px solid var(--border2);
  border-radius:2px;padding:1px 5px;color:var(--gold);
  font-family:'Share Tech Mono',monospace;font-size:0.58rem;
}

/* ── OVERLAYS ── */
.overlay{
  position:fixed;inset:0;background:rgba(0,0,0,0.97);
  display:flex;align-items:center;justify-content:center;z-index:200;
}
.overlay.hidden{display:none;}
.obox{
  background:linear-gradient(180deg,#0d0a06,#070503);
  border:1px solid var(--border2);border-radius:6px;
  padding:28px 32px;max-width:540px;width:92%;
  box-shadow:var(--shadow),inset 0 1px 0 rgba(232,160,32,0.1);
  position:relative;overflow:hidden;
}
.obox::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold),transparent);
}
.obox h1{
  font-family:'Cinzel',serif;font-size:1.6rem;font-weight:900;
  color:var(--gold);text-align:center;letter-spacing:4px;
  text-shadow:var(--glow-gold);margin-bottom:4px;
}
.obox h2{
  font-family:'Cinzel',serif;font-size:1rem;color:var(--gold);
  text-align:center;letter-spacing:3px;margin-bottom:12px;
}
.obox p{color:var(--text2);font-size:0.75rem;text-align:center;line-height:1.8;margin-bottom:12px;}
.btn{
  padding:9px 20px;border-radius:4px;font-weight:700;
  cursor:pointer;border:none;font-size:0.78rem;
  transition:all 0.18s;margin:3px;font-family:'Share Tech Mono',monospace;
  letter-spacing:1px;
}
.btn-gold{
  background:linear-gradient(135deg,#8a5a10,var(--gold));color:#000;
  border:1px solid var(--gold2);box-shadow:var(--glow-gold);
}
.btn-red{background:linear-gradient(135deg,#5a0a0a,var(--red2));color:#fff;border:1px solid var(--red2);}
.btn-blue{background:linear-gradient(135deg,#0a2a4a,var(--blue2));color:#fff;border:1px solid var(--blue2);}
.btn-gray{background:rgba(255,255,255,0.07);color:var(--text);border:1px solid var(--border2);}
.btn:hover{transform:translateY(-2px);filter:brightness(1.2);}
.btn:active{transform:translateY(0);}

/* Name input */
.name-inp{
  width:100%;padding:9px 12px;border-radius:4px;
  border:1px solid var(--border2);background:rgba(255,255,255,0.04);
  color:var(--gold);font-size:0.88rem;text-align:center;
  outline:none;font-family:'Share Tech Mono',monospace;letter-spacing:2px;
  margin-bottom:14px;
}
.name-inp:focus{border-color:var(--gold);box-shadow:var(--glow-gold);}

/* Class grid */
.cls-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:10px 0 14px;}
.cls-card{
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:5px;padding:10px 6px;cursor:pointer;transition:all 0.18s;text-align:center;
}
.cls-card:hover,.cls-card.sel{
  border-color:var(--gold);background:rgba(232,160,32,0.07);
  box-shadow:inset 0 0 12px rgba(232,160,32,0.06);
}
.cls-icon{font-size:1.5rem;display:block;margin-bottom:5px;}
.cls-name{font-family:'Cinzel',serif;font-size:0.6rem;color:var(--gold);letter-spacing:1px;}
.cls-desc{font-size:0.52rem;color:var(--text2);margin-top:3px;line-height:1.5;}

/* Monster HP bar in 3D view */
#mob-hpbar-wrap{
  position:absolute;top:8px;left:50%;transform:translateX(-50%);
  width:200px;pointer-events:none;z-index:20;
  opacity:0;transition:opacity 0.2s;
}
#mob-hpbar-wrap.show{opacity:1;}
#mob-hpbar-name{
  text-align:center;font-size:0.65rem;color:var(--redbright);
  text-shadow:var(--glow-red);margin-bottom:3px;font-family:'Cinzel',serif;
}
#mob-hpbar{height:6px;background:rgba(255,255,255,0.08);border-radius:2px;border:1px solid rgba(255,50,50,0.3);}
#mob-hpbar-fill{height:100%;background:linear-gradient(90deg,#7b1a1a,var(--redbright));border-radius:2px;transition:width 0.2s;}

/* Inventory overlay */
#inv-modal .inv-grid-g{
  display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin-bottom:10px;max-height:200px;overflow-y:auto;
}
.inv-slot2{
  aspect-ratio:1;background:rgba(255,255,255,0.04);
  border:1px solid var(--border);border-radius:3px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:1.1rem;cursor:pointer;transition:all 0.15s;position:relative;
}
.inv-slot2:hover,.inv-slot2.sel-slot{border-color:var(--gold);background:rgba(232,160,32,0.08);}
.inv-slot2 .sn{font-size:0.38rem;color:var(--text2);margin-top:1px;text-align:center;line-height:1.2;}
.inv-slot2 .se{
  position:absolute;top:1px;right:1px;
  background:var(--gold);color:#000;border-radius:2px;
  font-size:0.38rem;padding:0 2px;font-weight:700;
}
#iinfo{
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:4px;padding:8px 10px;min-height:50px;font-size:0.7rem;
  margin-bottom:8px;
}

/* Skill points modal */
#sp-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0;}

/* Scrollbar */
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-track{background:rgba(0,0,0,0.5);}
::-webkit-scrollbar-thumb{background:rgba(232,160,32,0.2);border-radius:2px;}

/* ── LEVEL UP FX ── */
@keyframes lvlfx{
  0%{opacity:0;transform:translate(-50%,-50%) scale(0.6);}
  40%{opacity:1;transform:translate(-50%,-60%) scale(1.1);}
  100%{opacity:0;transform:translate(-50%,-100%) scale(1.3);}
}
.lvl-fx{
  position:fixed;top:45%;left:50%;
  font-family:'Cinzel',serif;font-size:1.6rem;font-weight:900;
  color:var(--gold);text-shadow:var(--glow-gold);
  pointer-events:none;animation:lvlfx 1.4s ease forwards;z-index:300;
}
@keyframes dmgfx{
  0%{opacity:1;transform:translateY(0) scale(1);}
  100%{opacity:0;transform:translateY(-50px) scale(0.8);}
}
.dmg-fx{
  position:absolute;pointer-events:none;
  font-family:'Cinzel',serif;font-size:0.9rem;font-weight:700;
  animation:dmgfx 0.8s ease forwards;z-index:30;
}

/* ── DEATH / WIN ── */
@keyframes deathAnim{0%{opacity:0;}100%{opacity:1;}}
#death-overlay,#win-overlay{animation:deathAnim 0.4s ease;}
.result-icon{font-size:3.5rem;display:block;text-align:center;margin-bottom:10px;}
.stat-table{
  display:grid;grid-template-columns:1fr 1fr;gap:5px;
  background:rgba(255,255,255,0.03);border-radius:4px;
  padding:10px 12px;margin:10px 0;font-size:0.7rem;
}
.stat-table>div{display:flex;justify-content:space-between;}
.stat-table b{color:var(--gold);}

/* ── RARITY COLORS ── */
.r-common{color:#b0c0d0;}
.r-uncommon{color:var(--blue2);}
.r-rare{color:var(--purple2);}
.r-epic{color:#f97316;}
.r-legendary{color:var(--gold3);text-shadow:0 0 8px rgba(255,236,144,0.5);}
</style>
</head>
<body>
<div id="app">
  <!-- TOPBAR -->
  <div id="topbar">
    <div class="logo">⚔ DUNGEON CRAWLER</div>
    <div style="display:flex;gap:14px;align-items:center;">
      <div id="floor-badge" class="floor-badge">B1F</div>
      <div class="top-stat">💀 <span id="t-kills">0</span></div>
      <div class="top-stat">⏱ <span id="t-turns">0</span>T</div>
      <div class="top-stat">🌟 <span id="t-score">0</span></div>
    </div>
  </div>

  <!-- MAIN -->
  <div id="main">
    <!-- 3D View -->
    <div id="view3d-wrap">
      <div id="view3d">
        <canvas id="dungeon3d"></canvas>
        <div id="hit-flash"></div>
        <div id="crosshair"></div>

        <!-- Minimap -->
        <div id="minimap-wrap">
          <canvas id="minimap-canvas" width="110" height="110"></canvas>
          <div id="minimap-label">MINIMAP</div>
        </div>

        <!-- Target HP bar -->
        <div id="mob-hpbar-wrap">
          <div id="mob-hpbar-name">—</div>
          <div id="mob-hpbar"><div id="mob-hpbar-fill" style="width:100%"></div></div>
        </div>

        <!-- HUD -->
        <div id="hud">
          <div class="hud-bar-wrap">
            <div class="hud-bar-label">❤️ HP <span id="h-hp">30/30</span></div>
            <div class="hud-bar"><div class="hud-bar-fill hp-fill" id="hp-fill" style="width:100%"></div></div>
          </div>
          <div class="hud-bar-wrap">
            <div class="hud-bar-label">✨ XP <span id="h-xp">0/30</span></div>
            <div class="hud-bar"><div class="hud-bar-fill xp-fill" id="xp-fill" style="width:0%"></div></div>
          </div>
          <div class="hud-bar-wrap">
            <div class="hud-bar-label">🔷 MP <span id="h-mp">20/20</span></div>
            <div class="hud-bar"><div class="hud-bar-fill mp-fill" id="mp-fill" style="width:100%"></div></div>
          </div>
          <div id="skillbar"></div>
        </div>
      </div>

      <!-- Controls -->
      <div id="ctrlbar">
        <span class="kb">↑↓←→</span><span style="color:var(--text2)">이동</span>
        <span class="kb">A/D</span><span style="color:var(--text2)">회전</span>
        <span class="kb">Space</span><span style="color:var(--text2)">공격/확인</span>
        <span class="kb">I</span><span style="color:var(--text2)">인벤</span>
        <span class="kb">1-5</span><span style="color:var(--text2)">스킬</span>
        <span class="kb">E</span><span style="color:var(--text2)">상호작용</span>
        <span class="kb">.</span><span style="color:var(--text2)">계단</span>
      </div>
    </div>

    <!-- Panel -->
    <div id="panel">
      <div class="panel-sec">
        <div class="psec-title">CHARACTER</div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px;">
          <span style="font-family:'Cinzel',serif;font-size:0.72rem;color:var(--gold);" id="p-name">—</span>
          <span style="font-size:0.6rem;color:var(--cyan2);" id="p-class">—</span>
        </div>
        <div class="stat-grid2">
          <div class="sg-item"><div class="sg-label">LEVEL</div><div class="sg-val" id="p-lv">1</div></div>
          <div class="sg-item"><div class="sg-label">GOLD</div><div class="sg-val" id="p-gold" style="color:var(--gold2);">0</div></div>
          <div class="sg-item"><div class="sg-label">ATK</div><div class="sg-val" id="p-atk" style="color:var(--redbright);">5</div></div>
          <div class="sg-item"><div class="sg-label">DEF</div><div class="sg-val" id="p-def" style="color:var(--blue2);">2</div></div>
          <div class="sg-item"><div class="sg-label">SPD</div><div class="sg-val" id="p-spd" style="color:var(--green2);">5</div></div>
          <div class="sg-item"><div class="sg-label">CRIT</div><div class="sg-val" id="p-crit" style="color:var(--gold2);">5%</div></div>
        </div>
      </div>

      <div class="panel-sec">
        <div class="psec-title">EQUIPPED</div>
        <div id="equipped-grid"></div>
      </div>

      <div id="log-wrap">
        <h4>COMBAT LOG</h4>
        <div id="log-entries"></div>
      </div>
    </div>
  </div>
</div>

<!-- ──── OVERLAYS ──── -->
<!-- TITLE -->
<div id="title-overlay" class="overlay">
  <div class="obox" style="max-width:520px;text-align:center;">
    <div style="font-family:'Cinzel',serif;font-size:2.4rem;font-weight:900;color:var(--gold);
      text-shadow:var(--glow-gold),0 0 80px rgba(232,160,32,0.3);letter-spacing:6px;margin-bottom:4px;">
      DUNGEON
    </div>
    <div style="font-family:'Cinzel',serif;font-size:1rem;color:var(--text2);letter-spacing:8px;margin-bottom:18px;">
      C R A W L E R
    </div>
    <div style="font-size:0.68rem;color:var(--text2);margin-bottom:16px;line-height:2;">
      🗺 15층 던전 &nbsp;·&nbsp; 👹 50종 몬스터 &nbsp;·&nbsp; 🎒 40종 아이템 &nbsp;·&nbsp; 👑 10종 보스 &nbsp;·&nbsp; ⚔ 8개 클래스
    </div>
    <input id="name-inp" class="name-inp" type="text" placeholder="영웅의 이름을 새기라..." maxlength="10">
    <div style="display:flex;justify-content:center;gap:8px;">
      <button class="btn btn-gold" onclick="goClassSelect()">클래스 선택 →</button>
    </div>
  </div>
</div>

<!-- CLASS SELECT -->
<div id="class-overlay" class="overlay hidden">
  <div class="obox" style="max-width:640px;">
    <h2>⚔ 클래스 선택</h2>
    <div class="cls-grid" id="cls-grid">
      <!-- injected by JS -->
    </div>
    <div style="text-align:center;">
      <button class="btn btn-gold" id="cls-start-btn" onclick="startGame()" disabled style="opacity:0.4;">던전 입장 ⚔</button>
      <button class="btn btn-gray" onclick="backTitle()">← 뒤로</button>
    </div>
  </div>
</div>

<!-- INVENTORY -->
<div id="inv-modal" class="overlay hidden">
  <div class="obox" style="max-width:480px;">
    <h2>🎒 인벤토리</h2>
    <div class="inv-grid-g" id="inv-grid-g"></div>
    <div id="iinfo"><span style="color:var(--text2);font-size:0.68rem;">아이템을 클릭하여 정보 확인</span></div>
    <div style="margin-top:8px;display:flex;gap:6px;justify-content:center;">
      <button class="btn btn-gold" id="inv-use-btn" onclick="useSelItem()" style="display:none;">사용 / 장착</button>
      <button class="btn btn-red" id="inv-drop-btn" onclick="dropSelItem()" style="display:none;">버리기</button>
      <button class="btn btn-gray" onclick="closeInv()">닫기 (I)</button>
    </div>
  </div>
</div>

<!-- SHOP -->
<div id="shop-modal" class="overlay hidden">
  <div class="obox" style="max-width:420px;">
    <h2>⚗ 신비의 상점</h2>
    <div style="font-size:0.7rem;margin-bottom:10px;">소지 골드: <span id="sh-gold" style="color:var(--gold);font-weight:700;">0</span></div>
    <div id="sh-items" style="display:flex;flex-direction:column;gap:6px;max-height:300px;overflow-y:auto;margin-bottom:12px;"></div>
    <button class="btn btn-gray" onclick="closeShop()">나가기 (E)</button>
  </div>
</div>

<!-- LEVEL UP -->
<div id="lvl-modal" class="overlay hidden">
  <div class="obox" style="max-width:360px;text-align:center;">
    <h2>⬆ LEVEL UP!</h2>
    <p>스탯 포인트를 분배하세요</p>
    <div id="sp-grid">
      <button class="btn btn-red" onclick="allocate('hp')">❤️ 최대 HP +20</button>
      <button class="btn" style="background:linear-gradient(135deg,#5a2a00,#fb923c);color:#000;border:1px solid #fb923c;" onclick="allocate('atk')">⚔️ ATK +3</button>
      <button class="btn btn-blue" onclick="allocate('def')">🛡️ DEF +2</button>
      <button class="btn" style="background:linear-gradient(135deg,#0a3a1a,#22c55e);color:#000;border:1px solid #22c55e;" onclick="allocate('spd')">💨 SPD +1</button>
      <button class="btn" style="background:linear-gradient(135deg,#2a0a4a,var(--purple2));color:#fff;border:1px solid var(--purple2);" onclick="allocate('mp')">🔷 최대 MP +15</button>
      <button class="btn" style="background:linear-gradient(135deg,#3a2a00,var(--gold));color:#000;border:1px solid var(--gold);" onclick="allocate('crit')">⚡ 크리율 +3%</button>
    </div>
  </div>
</div>

<!-- DEATH -->
<div id="death-overlay" class="overlay hidden">
  <div class="obox" style="text-align:center;">
    <span class="result-icon">💀</span>
    <h1 style="color:var(--redbright);text-shadow:var(--glow-red);font-size:1.8rem;">YOU DIED</h1>
    <p id="death-cause">어둠에 잠들었습니다</p>
    <div class="stat-table" id="death-stats"></div>
    <button class="btn btn-red" onclick="restartToTitle()">다시 시작 ↺</button>
  </div>
</div>

<!-- VICTORY -->
<div id="win-overlay" class="overlay hidden">
  <div class="obox" style="text-align:center;">
    <span class="result-icon">🏆</span>
    <h1 style="color:var(--gold);">VICTORY!</h1>
    <p>최종 보스를 처치했습니다!<br>당신은 진정한 던전의 정복자입니다.</p>
    <div class="stat-table" id="win-stats"></div>
    <button class="btn btn-gold" onclick="restartToTitle()">다시 플레이</button>
  </div>
</div>

<script>
'use strict';
// ══════════════════════════════════════════════════════
// ██████  ██████  ██  ██  ███████  ████████  ██████
// ██   ██ ██   ██ ██  ██  ██       ██    ██  ██   ██
// ██████  ██████  ██  ██  ███████     ██     ██   ██
// ██   ██ ██   ██ ██  ██       ██     ██     ██   ██
// ██████  ██   ██  ████   ███████     ██     ██████
// 1st-PERSON DUNGEON CRAWLER — FULL ENGINE
// ══════════════════════════════════════════════════════

// ── CONSTANTS ─────────────────────────────────────────
const MAP_W = 32, MAP_H = 32;
const MAX_FLOOR = 15;
const CELL = {WALL:0,FLOOR:1,CORRIDOR:2,STAIRS:3,SHOP:4,CHEST:5};
const DIRS = [[0,-1],[1,0],[0,1],[-1,0]]; // N E S W
const DIR_NAMES = ['N','E','S','W'];

// FACING — player direction index into DIRS
// 0=North(up), 1=East(right), 2=South(down), 3=West(left)

// ── 3D RAYCASTING CONSTANTS ────────────────────────────
const SCREEN_W = 600, SCREEN_H = 380;
const FOV = Math.PI / 2.5;        // ~72°
const MAX_RAY_DIST = 20;
const HALF_FOV = FOV / 2;
const NUM_RAYS = 120;

// ── CLASSES (8) ────────────────────────────────────────
const CLASSES = {
  warrior: {name:'워리어',     icon:'🗡️', color:'#e74c3c',
    hp:80, mp:20, atk:12, def:7, spd:5, crit:8,
    desc:'근접 전투 특화. 높은 HP·DEF.',
    skills:['slash','shield_bash','war_cry','execute','berserker']},
  paladin: {name:'팔라딘',     icon:'🛡️', color:'#f39c12',
    hp:90, mp:30, atk:9,  def:10,spd:4, crit:5,
    desc:'방어와 치유. 재생 패시브.',
    skills:['holy_strike','heal','divine_shield','consecrate','holy_nova']},
  rogue:   {name:'로그',       icon:'🗝️', color:'#27ae60',
    hp:55, mp:25, atk:11, def:4, spd:10,crit:25,
    desc:'초고속·초크리. 독 공격.',
    skills:['backstab','poison','smoke','evasion','shadowstep']},
  mage:    {name:'메이지',     icon:'🔮', color:'#9b59b6',
    hp:45, mp:60, atk:15, def:2, spd:6, crit:12,
    desc:'마법 극딜. MP 관리 필요.',
    skills:['fireball','icespike','thunder','arcane_blast','meteor']},
  archer:  {name:'아처',       icon:'🏹', color:'#16a085',
    hp:58, mp:30, atk:13, def:3, spd:9, crit:18,
    desc:'원거리 특화. 연속 사격.',
    skills:['arrow_shot','multi_shot','eagle_eye','trap','rain_of_arrows']},
  berserker:{name:'버서커',    icon:'💢', color:'#c0392b',
    hp:70, mp:15, atk:18, def:3, spd:7, crit:10,
    desc:'ATK 극대화. 체력 낮을수록 강함.',
    skills:['rage_strike','bloodlust','frenzy','battle_scream','last_stand']},
  necromancer:{name:'네크로맨서',icon:'💀',color:'#8e44ad',
    hp:50, mp:50, atk:14, def:3, spd:5, crit:15,
    desc:'언데드 소환·저주 마법.',
    skills:['dark_bolt','summon_undead','life_drain','curse','death_nova']},
  monk:    {name:'몽크',       icon:'🥊', color:'#1abc9c',
    hp:65, mp:35, atk:10, def:5, spd:11,crit:20,
    desc:'빠른 연타. MP로 스킬 폭발.',
    skills:['combo','ki_blast','iron_skin','whirlwind','inner_peace']},
};

// ── SKILL DEFINITIONS ──────────────────────────────────
const SKILL_DEFS = {
  slash:         {name:'슬래시',    icon:'⚔️', mp:0,  cd:0,  dmgMult:1.5, type:'melee',  desc:'1.5배 근접 피해'},
  shield_bash:   {name:'방패 강타', icon:'🛡️', mp:8,  cd:3,  dmgMult:1.2, stun:1, type:'melee', desc:'스턴+1.2배'},
  war_cry:       {name:'전투 함성', icon:'📯', mp:10, cd:5,  buffAtk:5, buffTurns:4, type:'buff', desc:'ATK+5(4턴)'},
  execute:       {name:'처형',      icon:'🗡️', mp:15, cd:6,  execHp:0.3, type:'melee', desc:'HP30% 이하 즉사'},
  berserker:     {name:'광전사화',  icon:'💢', mp:20, cd:8,  buffAtk:15, buffTurns:5, type:'buff', desc:'ATK+15(5턴)'},
  holy_strike:   {name:'성스러운 타격',icon:'✨',mp:12,cd:4, dmgMult:1.8, healSelf:10, type:'melee', desc:'1.8배+HP10회복'},
  heal:          {name:'힐',        icon:'💚', mp:15, cd:3,  healPct:0.3, type:'heal', desc:'최대HP 30% 회복'},
  divine_shield: {name:'신성 방패', icon:'🌟', mp:18, cd:7,  shieldTurns:3, type:'buff', desc:'3턴 무적'},
  consecrate:    {name:'신성화',    icon:'🔆', mp:20, cd:6,  dmgAll:25, type:'aoe', desc:'모든 적 25 피해'},
  holy_nova:     {name:'성광 폭발', icon:'💥', mp:30, cd:10, dmgAll:50, healSelf:30, type:'aoe', desc:'전체50피해+회복'},
  backstab:      {name:'기습',      icon:'🗝️', mp:0,  cd:2,  dmgMult:2.5, critForce:true, type:'melee', desc:'확정 크리 2.5배'},
  poison:        {name:'독',        icon:'☠️', mp:8,  cd:4,  poisonTurns:5, dmgMult:0.8, type:'melee', desc:'독5턴+0.8배'},
  smoke:         {name:'연막',      icon:'💨', mp:10, cd:5,  dodgeTurns:2, type:'buff', desc:'2턴 회피'},
  evasion:       {name:'회피기동',  icon:'🌀', mp:12, cd:6,  dodgeTurns:3, type:'buff', desc:'3턴 회피'},
  shadowstep:    {name:'그림자 걸음',icon:'👤',mp:15, cd:8,  dmgMult:3.0, type:'melee', desc:'3.0배 기습'},
  fireball:      {name:'파이어볼',  icon:'🔥', mp:15, cd:3,  dmgFlat:45, type:'magic', desc:'불 45 마법피해'},
  icespike:      {name:'아이스 스파이크',icon:'❄️',mp:12,cd:3,dmgFlat:35, freeze:1, type:'magic', desc:'얼음35+빙결'},
  thunder:       {name:'썬더',      icon:'⚡', mp:18, cd:4,  dmgFlat:55, type:'magic', desc:'번개 55 피해'},
  arcane_blast:  {name:'아케인 폭발',icon:'🌀',mp:20,cd:5,  dmgAll:30, type:'aoe', desc:'전체 30 피해'},
  meteor:        {name:'메테오',    icon:'☄️', mp:35, cd:10, dmgAll:80, type:'aoe', desc:'전체 80 피해'},
  arrow_shot:    {name:'정밀 사격', icon:'🏹', mp:5,  cd:2,  dmgMult:1.4, type:'ranged', desc:'1.4배 원거리'},
  multi_shot:    {name:'다연 사격', icon:'🪃', mp:12, cd:4,  dmgAll:20, type:'aoe', desc:'전체 20 피해'},
  eagle_eye:     {name:'매의 눈',   icon:'👁️', mp:8,  cd:5,  critBuff:15, buffTurns:4, type:'buff', desc:'크리율+15%(4턴)'},
  trap:          {name:'트랩',      icon:'🪤', mp:10, cd:5,  dmgFlat:40, stun:2, type:'magic', desc:'40피해+스턴2'},
  rain_of_arrows:{name:'화살비',    icon:'🌧️', mp:25, cd:8,  dmgAll:45, type:'aoe', desc:'전체 45 피해'},
  rage_strike:   {name:'분노 강타', icon:'💢', mp:0,  cd:3,  dmgMult:2.0, selfHp:-10, type:'melee', desc:'2.0배, 자신HP-10'},
  bloodlust:     {name:'피의 갈망', icon:'🩸', mp:0,  cd:6,  dmgMult:1.5, lifeSteal:0.5, type:'melee', desc:'1.5배+피흡50%'},
  frenzy:        {name:'광란',      icon:'🌋', mp:20, cd:8,  buffAtk:20, buffTurns:3, selfHp:-20, type:'buff', desc:'ATK+20-HP20'},
  battle_scream: {name:'전투 함성', icon:'📢', mp:12, cd:5,  buffAtk:8, buffTurns:5, type:'buff', desc:'ATK+8(5턴)'},
  last_stand:    {name:'최후의 저항',icon:'🏴',mp:0,  cd:10, execSelf:true, type:'special', desc:'HP낮을수록 강화'},
  dark_bolt:     {name:'암흑탄',    icon:'💜', mp:10, cd:2,  dmgFlat:40, type:'magic', desc:'암흑 40 피해'},
  summon_undead: {name:'언데드 소환',icon:'💀',mp:25, cd:8,  summon:true, type:'special', desc:'언데드 소환'},
  life_drain:    {name:'생명 흡수', icon:'🖤', mp:15, cd:4,  dmgFlat:30, healSelf:20, type:'magic', desc:'30피해+자신20회복'},
  curse:         {name:'저주',      icon:'⛧',  mp:12, cd:5,  curseTurns:4, type:'debuff', desc:'저주4턴(ATK-30%)'},
  death_nova:    {name:'죽음의 폭발',icon:'☠️',mp:30,cd:10,  dmgAll:70, type:'aoe', desc:'전체 70 피해'},
  combo:         {name:'연타',      icon:'🥊', mp:8,  cd:2,  hits:3, dmgMult:0.6, type:'melee', desc:'3연타×0.6배'},
  ki_blast:      {name:'기공파',    icon:'🌀', mp:15, cd:4,  dmgFlat:50, type:'magic', desc:'기 50 피해'},
  iron_skin:     {name:'철갑',      icon:'⛓️', mp:10, cd:6,  buffDef:8, buffTurns:4, type:'buff', desc:'DEF+8(4턴)'},
  whirlwind:     {name:'회오리',    icon:'🌪️', mp:20, cd:6,  dmgAll:35, type:'aoe', desc:'전체 35 피해'},
  inner_peace:   {name:'내면의 평화',icon:'☮️',mp:0,  cd:8,  healPct:0.5, mpRestore:20, type:'heal', desc:'HP50%+MP20회복'},
};

// ── MONSTERS (50) ──────────────────────────────────────
const MON_DATA = [
  // FL1
  {id:'slime',    n:'슬라임',     i:'🟢',hp:15, atk:4,  def:0, xp:8,  g:5,  mv:'rnd', fl:1},
  {id:'bat',      n:'박쥐',       i:'🦇',hp:10, atk:5,  def:0, xp:6,  g:4,  mv:'ch',  fl:1},
  {id:'rat',      n:'거대 쥐',    i:'🐀',hp:18, atk:5,  def:1, xp:10, g:6,  mv:'rnd', fl:1},
  {id:'mushroom', n:'독버섯',     i:'🍄',hp:20, atk:4,  def:2, xp:10, g:5,  mv:'rnd', fl:1},
  {id:'spider',   n:'독거미',     i:'🕷️',hp:14, atk:6,  def:1, xp:9,  g:7,  mv:'ch',  fl:1},
  // FL2
  {id:'goblin',   n:'고블린',     i:'👺',hp:25, atk:7,  def:1, xp:15, g:10, mv:'ch',  fl:2},
  {id:'zombie',   n:'좀비',       i:'🧟',hp:35, atk:6,  def:2, xp:18, g:8,  mv:'ch',  fl:2},
  {id:'kobold',   n:'코볼트',     i:'🐊',hp:22, atk:8,  def:2, xp:14, g:9,  mv:'ch',  fl:2},
  {id:'crow',     n:'어둠 까마귀',i:'🐦',hp:18, atk:8,  def:1, xp:12, g:8,  mv:'ch',  fl:2},
  {id:'snail',    n:'강화 달팽이',i:'🐌',hp:40, atk:5,  def:5, xp:16, g:10, mv:'slow',fl:2},
  // FL3
  {id:'skeleton', n:'스켈레톤',   i:'💀',hp:28, atk:9,  def:2, xp:20, g:12, mv:'ch',  fl:3},
  {id:'orc',      n:'오크',       i:'👿',hp:45, atk:10, def:3, xp:25, g:15, mv:'ch',  fl:3},
  {id:'ghost',    n:'유령',       i:'👻',hp:22, atk:11, def:6, xp:28, g:16, mv:'phase',fl:3},
  {id:'witch_f',  n:'마녀 제자',  i:'🧙',hp:30, atk:12, def:2, xp:22, g:14, mv:'rng', fl:3},
  {id:'lizard',   n:'도마뱀 전사',i:'🦎',hp:36, atk:9,  def:4, xp:20, g:13, mv:'ch',  fl:3},
  // FL4
  {id:'wolf',     n:'다크 울프',  i:'🐺',hp:35, atk:12, def:2, xp:22, g:14, mv:'ch',  fl:4},
  {id:'armored',  n:'강철 기사',  i:'⚔️',hp:50, atk:11, def:8, xp:30, g:20, mv:'slow',fl:4},
  {id:'harpy',    n:'하피',       i:'🦅',hp:28, atk:13, def:2, xp:25, g:17, mv:'ch',  fl:4},
  {id:'ogre',     n:'오우거',     i:'👹',hp:60, atk:12, def:4, xp:30, g:18, mv:'slow',fl:4},
  {id:'wraith',   n:'레이스',     i:'🌫️',hp:25, atk:14, def:5, xp:28, g:18, mv:'phase',fl:4},
  // FL5
  {id:'troll',    n:'트롤',       i:'🧌',hp:65, atk:13, def:5, xp:35, g:20, mv:'ch',  fl:5},
  {id:'medusa',   n:'메두사',     i:'🐍',hp:40, atk:15, def:3, xp:38, g:22, mv:'rng', fl:5},
  {id:'vampire',  n:'흡혈귀',     i:'🧛',hp:50, atk:14, def:5, xp:40, g:25, mv:'ch',  fl:5},
  {id:'mummy',    n:'미라',       i:'🪦',hp:55, atk:12, def:7, xp:36, g:22, mv:'slow',fl:5},
  {id:'basilisk', n:'바실리스크', i:'🐲',hp:45, atk:14, def:4, xp:38, g:24, mv:'ch',  fl:5},
  // FL6
  {id:'golem',    n:'골렘',       i:'🗿',hp:90, atk:13, def:10,xp:45, g:28, mv:'slow',fl:6},
  {id:'demon',    n:'데몬',       i:'😈',hp:65, atk:18, def:6, xp:55, g:35, mv:'ch',  fl:6},
  {id:'banshee',  n:'밴시',       i:'👾',hp:42, atk:17, def:4, xp:48, g:30, mv:'rng', fl:6},
  {id:'hellhound',n:'지옥 하운드',i:'🐕',hp:52, atk:16, def:4, xp:45, g:30, mv:'ch',  fl:6},
  {id:'sorcerer', n:'어둠 마법사',i:'🧙',hp:48, atk:19, def:3, xp:50, g:32, mv:'rng', fl:6},
  // FL7
  {id:'witch2',   n:'마녀',       i:'🧙',hp:55, atk:18, def:4, xp:55, g:35, mv:'rng', fl:7},
  {id:'golem2',   n:'마석 골렘',  i:'💠',hp:100,atk:15, def:12,xp:60, g:38, mv:'slow',fl:7},
  {id:'succubus', n:'서큐버스',   i:'🦹',hp:58, atk:20, def:5, xp:58, g:36, mv:'ch',  fl:7},
  {id:'death_kn', n:'죽음의 기사',i:'⛓️',hp:70, atk:19, def:9, xp:62, g:40, mv:'ch',  fl:7},
  {id:'manticore',n:'만티코어',   i:'🦁',hp:65, atk:21, def:6, xp:65, g:40, mv:'ch',  fl:7},
  // FL8
  {id:'dragon_y', n:'어린 드래곤',i:'🐉',hp:100,atk:20, def:8, xp:70, g:50, mv:'ch',  fl:8},
  {id:'lich',     n:'리치',       i:'🕯️',hp:75, atk:23, def:9, xp:80, g:55, mv:'rng', fl:8},
  {id:'titan',    n:'타이탄',     i:'⚡',hp:130,atk:21, def:13,xp:90, g:60, mv:'slow',fl:8},
  {id:'dark_elf', n:'다크 엘프',  i:'🧝',hp:60, atk:22, def:6, xp:72, g:48, mv:'ch',  fl:8},
  {id:'abomination',n:'혐오체',   i:'🧫',hp:85, atk:19, def:10,xp:78, g:52, mv:'ch',  fl:8},
  // FL9
  {id:'balrog',   n:'발로그',     i:'🔥',hp:110,atk:25, def:11,xp:100,g:70, mv:'ch',  fl:9},
  {id:'hydra',    n:'히드라',     i:'🐲',hp:120,atk:22, def:10,xp:95, g:65, mv:'slow',fl:9},
  {id:'lich2',    n:'고대 리치',  i:'☠️',hp:90, atk:26, def:11,xp:105,g:72, mv:'rng', fl:9},
  {id:'phoenix',  n:'불사조',     i:'🦤',hp:95, atk:24, def:8, xp:98, g:68, mv:'ch',  fl:9},
  {id:'ancient',  n:'고대 골렘',  i:'🪨',hp:150,atk:20, def:16,xp:110,g:75, mv:'slow',fl:9},
  // FL10-15 harder mobs
  {id:'hellspawn',n:'지옥 소환체',i:'👺',hp:130,atk:28, def:12,xp:120,g:80, mv:'ch',  fl:10},
  {id:'archlich', n:'아크 리치',  i:'💀',hp:110,atk:30, def:13,xp:130,g:90, mv:'rng', fl:10},
  {id:'inferno',  n:'인페르노',   i:'🌋',hp:140,atk:27, def:10,xp:125,g:85, mv:'ch',  fl:11},
  {id:'void_w',   n:'보이드 워커',i:'🌑',hp:100,atk:32, def:14,xp:140,g:95, mv:'phase',fl:12},
  {id:'celestial',n:'타락한 천사',i:'😇',hp:120,atk:34, def:15,xp:155,g:100,mv:'ch',  fl:13},
  // BOSSES (10)
  {id:'boss1',   n:'지하 군주',   i:'👁️',hp:200, atk:22,def:10,xp:200,g:300, mv:'boss',fl:1, boss:true},
  {id:'boss2',   n:'석화의 여왕', i:'🐸',hp:280, atk:26,def:12,xp:280,g:400, mv:'boss',fl:2, boss:true},
  {id:'boss3',   n:'뼈의 왕',     i:'🦴',hp:360, atk:30,def:14,xp:360,g:500, mv:'boss',fl:3, boss:true},
  {id:'boss4',   n:'심연의 수호자',i:'🌊',hp:440, atk:34,def:16,xp:440,g:600, mv:'boss',fl:4, boss:true},
  {id:'boss5',   n:'불꽃 골렘왕', i:'🌋',hp:520, atk:36,def:18,xp:520,g:700, mv:'boss',fl:5, boss:true},
  {id:'boss6',   n:'암흑 드래곤', i:'🐲',hp:620, atk:40,def:20,xp:620,g:800, mv:'boss',fl:6, boss:true},
  {id:'boss7',   n:'저주받은 왕', i:'👑',hp:700, atk:43,def:22,xp:700,g:900, mv:'boss',fl:7, boss:true},
  {id:'boss8',   n:'심연의 마왕', i:'😈',hp:800, atk:46,def:24,xp:800,g:1000,mv:'boss',fl:8, boss:true},
  {id:'boss9',   n:'고대의 드래곤',i:'🐉',hp:950, atk:50,def:26,xp:950,g:1200,mv:'boss',fl:9, boss:true},
  {id:'boss10',  n:'지옥신 THANATOS',i:'💀',hp:1200,atk:58,def:30,xp:1500,g:3000,mv:'boss',fl:15,boss:true},
];

// ── ITEMS (40) ────────────────────────────────────────
const ITEMS = [
  // Weapons
  {id:'sw1', n:'녹슨 검',      i:'🗡️', t:'weapon',atk:3, r:'common',  desc:'ATK+3'},
  {id:'sw2', n:'철제 검',      i:'⚔️', t:'weapon',atk:7, r:'uncommon',desc:'ATK+7'},
  {id:'sw3', n:'강화 검',      i:'🌟', t:'weapon',atk:12,r:'rare',     desc:'ATK+12'},
  {id:'sw4', n:'마검 엑스칼리버',i:'✨',t:'weapon',atk:18,r:'epic',     desc:'ATK+18'},
  {id:'sw5', n:'전설의 성검',  i:'🏅', t:'weapon',atk:28,r:'legendary',desc:'ATK+28 크리+10%'},
  {id:'ax1', n:'전투 도끼',    i:'🪓', t:'weapon',atk:9, r:'uncommon',desc:'ATK+9'},
  {id:'sp1', n:'용기병 창',    i:'🔱', t:'weapon',atk:10,r:'uncommon',desc:'ATK+10'},
  {id:'bow1',n:'사냥 활',      i:'🏹', t:'weapon',atk:8, r:'uncommon',desc:'ATK+8 원거리'},
  {id:'st1', n:'마법 지팡이',  i:'🪄', t:'weapon',atk:6, r:'uncommon',desc:'ATK+6 MP+15'},
  {id:'dg1', n:'독 단검',      i:'🔪', t:'weapon',atk:5, r:'common',  desc:'ATK+5 독 부여'},
  // Armor
  {id:'ar1', n:'낡은 가죽 갑옷',i:'🧥',t:'armor', def:2, r:'common',  desc:'DEF+2'},
  {id:'ar2', n:'쇠사슬 갑옷',  i:'🦺', t:'armor', def:5, r:'uncommon',desc:'DEF+5'},
  {id:'ar3', n:'판금 갑옷',    i:'🔷', t:'armor', def:9, r:'rare',    desc:'DEF+9'},
  {id:'ar4', n:'미스릴 갑옷',  i:'💠', t:'armor', def:14,r:'epic',    desc:'DEF+14'},
  {id:'ar5', n:'드래곤 스케일',i:'🐲', t:'armor', def:22,r:'legendary',desc:'DEF+22 HP+30'},
  // Shield
  {id:'sh1', n:'나무 방패',    i:'🛡️', t:'shield',def:2, r:'common',  desc:'DEF+2'},
  {id:'sh2', n:'강철 방패',    i:'🔵', t:'shield',def:5, r:'uncommon',desc:'DEF+5'},
  {id:'sh3', n:'타워 쉴드',    i:'🟦', t:'shield',def:9, r:'rare',    desc:'DEF+9'},
  // Helmet
  {id:'hm1', n:'가죽 투구',    i:'⛑️', t:'helmet',def:1,hp:5,r:'common', desc:'DEF+1 HP+5'},
  {id:'hm2', n:'철 투구',      i:'🪖', t:'helmet',def:3,hp:10,r:'uncommon',desc:'DEF+3 HP+10'},
  {id:'hm3', n:'용사 투구',    i:'👑', t:'helmet',def:5,hp:20,r:'rare', desc:'DEF+5 HP+20'},
  // Boots / Rings
  {id:'bt1', n:'질풍 장화',    i:'👟', t:'boots', spd:3, r:'uncommon',desc:'SPD+3'},
  {id:'bt2', n:'마법사 부츠',  i:'🥾', t:'boots', spd:2,mp:10,r:'rare',desc:'SPD+2 MP+10'},
  {id:'rg1', n:'힘의 반지',    i:'💍', t:'ring',  atk:3,def:1,r:'uncommon',desc:'ATK+3 DEF+1'},
  {id:'rg2', n:'지혜의 반지',  i:'🔮', t:'ring',  mp:20, r:'uncommon',desc:'MP+20'},
  {id:'rg3', n:'생명의 반지',  i:'❤️', t:'ring',  hp:25, r:'rare',    desc:'HP+25'},
  // Potions
  {id:'hp1', n:'소형 포션',    i:'🧪', t:'potion',heal:25,r:'common',  desc:'HP+25 회복'},
  {id:'hp2', n:'중형 포션',    i:'💊', t:'potion',heal:60,r:'uncommon',desc:'HP+60 회복'},
  {id:'hp3', n:'대형 포션',    i:'💉', t:'potion',heal:120,r:'rare',   desc:'HP+120 회복'},
  {id:'mp1', n:'마나 포션',    i:'🔵', t:'potion',mpHeal:30,r:'uncommon',desc:'MP+30 회복'},
  {id:'mp2', n:'엘릭서',       i:'⚗️', t:'potion',heal:50,mpHeal:50,r:'rare',desc:'HP+50 MP+50'},
  // Scrolls
  {id:'sc1', n:'화염 스크롤',  i:'🔥', t:'scroll',dmgAll:40,r:'uncommon',desc:'전체 적 40 피해'},
  {id:'sc2', n:'빙결 스크롤',  i:'❄️', t:'scroll',freeze:2, r:'rare',  desc:'모든 적 2턴 빙결'},
  {id:'sc3', n:'맵 스크롤',    i:'🗺️', t:'scroll',reveal:true,r:'uncommon',desc:'전체 맵 공개'},
  {id:'sc4', n:'텔레포트 스크롤',i:'🌀',t:'scroll',tele:true,r:'rare',desc:'무작위 이동'},
  {id:'sc5', n:'저주 스크롤',  i:'⛧',  t:'scroll',curse:true,r:'common',desc:'??? (저주)'},
  // Special
  {id:'gem1',n:'경험의 보석',  i:'💎', t:'gem',   xp:80, r:'rare',    desc:'경험치+80'},
  {id:'key1',n:'황금 열쇠',    i:'🗝️', t:'key',          r:'uncommon',desc:'보물상자 열기'},
  {id:'g1',  n:'금화 주머니',  i:'💰', t:'gold',  gold:150,r:'common', desc:'골드+150'},
  {id:'g2',  n:'보물 상자',    i:'📦', t:'gold',  gold:350,r:'uncommon',desc:'골드+350'},
];
const RARITY_COL={common:'#b0c0d0',uncommon:'#3498db',rare:'#9b59b6',epic:'#e67e22',legendary:'#f1c40f'};

// ── GAME STATE ──────────────────────────────────────────
let G = null;
let selectedCls = null;
let selInvItem = null;
let animFrame = null;

// ── INIT STATE ──────────────────────────────────────────
function initG(name, clsId) {
  const cd = CLASSES[clsId];
  const skillIds = cd.skills.slice(0,5);
  const skills = skillIds.map(id => ({
    id, ...SKILL_DEFS[id],
    cdLeft:0, active: false
  }));

  G = {
    name, clsId, clsName:cd.name+' '+cd.icon,
    floor:1,
    hp:cd.hp, maxHp:cd.hp,
    mp:cd.mp, maxMp:cd.mp,
    atk:cd.atk, def:cd.def, spd:cd.spd, crit:cd.crit,
    xp:0, level:1, xpNext:40,
    gold:80,
    kills:0, turns:0, score:0,
    inv:[], equipped:{weapon:null,armor:null,shield:null,helmet:null,boots:null,ring:null},
    skills,
    buffs:[], // {type,val,turns}
    poison:0, frozen:0, stunned:0, dodgeTurns:0,
    shieldTurns:0,
    map:[], rooms:[], monsters:[], items:[],
    px:0, py:0, dir:0, // dir: 0=N 1=E 2=S 3=W (index into DIRS)
    revealed:[], visible:[],
    gameOver:false, victory:false,
    summon:null,
  };
}

// ── MAP GENERATION ──────────────────────────────────────
function makeMap(){
  const map = Array.from({length:MAP_H},()=>Array(MAP_W).fill(CELL.WALL));
  const rooms = [];
  function carve(x,y,w,h){
    for(let ry=y;ry<y+h;ry++)
      for(let rx=x;rx<x+w;rx++)
        map[ry][rx]=CELL.FLOOR;
    rooms.push({x,y,w,h,cx:x+Math.floor(w/2),cy:y+Math.floor(h/2)});
  }
  function corr(ax,ay,bx,by){
    let x=ax,y=ay;
    const hFirst=Math.random()<0.5;
    if(hFirst){
      while(x!==bx){map[y][x]=CELL.CORRIDOR;x+=x<bx?1:-1;}
      while(y!==by){map[y][x]=CELL.CORRIDOR;y+=y<by?1:-1;}
    } else {
      while(y!==by){map[y][x]=CELL.CORRIDOR;y+=y<by?1:-1;}
      while(x!==bx){map[y][x]=CELL.CORRIDOR;x+=x<bx?1:-1;}
    }
  }
  const nRooms = 8 + Math.floor(Math.random()*6);
  let att=0;
  while(rooms.length<nRooms && att<400){
    att++;
    const rw=4+Math.floor(Math.random()*5);
    const rh=3+Math.floor(Math.random()*4);
    const rx=1+Math.floor(Math.random()*(MAP_W-rw-2));
    const ry=1+Math.floor(Math.random()*(MAP_H-rh-2));
    const ok=!rooms.some(r=>rx<r.x+r.w+2&&rx+rw>r.x-2&&ry<r.y+r.h+2&&ry+rh>r.y-2);
    if(ok) carve(rx,ry,rw,rh);
  }
  for(let i=1;i<rooms.length;i++) corr(rooms[i-1].cx,rooms[i-1].cy,rooms[i].cx,rooms[i].cy);

  // Player start
  G.px=rooms[0].cx; G.py=rooms[0].cy; G.dir=0;

  // Stairs
  const sr=rooms[rooms.length-1];
  map[sr.cy][sr.cx]=CELL.STAIRS;

  // Shops (1-2 shops in middle rooms)
  const shopCount=1+(rooms.length>6?1:0);
  for(let k=0;k<shopCount;k++){
    const si=1+Math.floor(Math.random()*(rooms.length-2));
    const r=rooms[si]; map[r.cy][r.cx]=CELL.SHOP;
  }

  // Chests
  for(let i=1;i<rooms.length;i++){
    if(Math.random()<0.25){
      const r=rooms[i];
      const cx=r.x+1+Math.floor(Math.random()*(r.w-2));
      const cy=r.y+1+Math.floor(Math.random()*(r.h-2));
      if(map[cy][cx]===CELL.FLOOR) map[cy][cx]=CELL.CHEST;
    }
  }

  G.map=map; G.rooms=rooms;
  G.revealed=Array.from({length:MAP_H},()=>Array(MAP_W).fill(false));
  G.visible=Array.from({length:MAP_H},()=>Array(MAP_W).fill(false));

  spawnMonsters();
  spawnItems();
  updateFOV();
}

function spawnMonsters(){
  G.monsters=[];
  const fl=G.floor;
  const eligible=MON_DATA.filter(m=>!m.boss&&m.fl<=Math.min(fl,15));
  // Boss for this floor (every floor has one boss)
  const bossData=MON_DATA.filter(m=>m.boss&&m.fl<=fl).sort((a,b)=>b.fl-a.fl)[0];

  for(let i=1;i<G.rooms.length;i++){
    const r=G.rooms[i];
    const cnt=1+Math.floor(Math.random()*3);
    for(let k=0;k<cnt;k++){
      const mt=eligible[Math.floor(Math.random()*eligible.length)];
      if(!mt) continue;
      const sc=1+(fl-1)*0.18;
      const mx=r.x+1+Math.floor(Math.random()*(r.w-2));
      const my=r.y+1+Math.floor(Math.random()*(r.h-2));
      G.monsters.push({
        ...mt,
        uid:mt.id+'_'+Math.random().toString(36).slice(2),
        hp:Math.round(mt.hp*sc), maxHp:Math.round(mt.hp*sc),
        atk:Math.round(mt.atk*sc),
        x:mx,y:my,
        frozen:0, stunned:0,
      });
    }
  }
  // Boss in last room
  if(bossData){
    const br=G.rooms[G.rooms.length-1];
    const sc=1+(fl-1)*0.12;
    G.monsters.push({
      ...bossData,
      uid:bossData.id+'_boss_'+fl,
      hp:Math.round(bossData.hp*sc), maxHp:Math.round(bossData.hp*sc),
      atk:Math.round(bossData.atk*sc),
      x:br.cx,y:br.cy,
      frozen:0, stunned:0,
    });
  }
}

function spawnItems(){
  G.items=[];
  for(let i=1;i<G.rooms.length;i++){
    if(Math.random()<0.55){
      const r=G.rooms[i];
      const pool=ITEMS.filter(it=>it.id!=='sc5');
      const item=pool[Math.floor(Math.random()*pool.length)];
      G.items.push({...item, uid:item.id+'_'+Math.random().toString(36).slice(2),
        x:r.x+Math.floor(r.w/2), y:r.y+Math.floor(r.h/2)});
    }
  }
}

// ── FOV ─────────────────────────────────────────────────
function updateFOV(){
  G.visible=Array.from({length:MAP_H},()=>Array(MAP_W).fill(false));
  const R=7;
  const {px,py}=G;
  for(let dy=-R;dy<=R;dy++){
    for(let dx=-R;dx<=R;dx++){
      if(dx*dx+dy*dy>R*R) continue;
      const nx=px+dx,ny=py+dy;
      if(nx<0||ny<0||nx>=MAP_W||ny>=MAP_H) continue;
      if(hasLOS(px,py,nx,ny)){G.visible[ny][nx]=true;G.revealed[ny][nx]=true;}
    }
  }
}
function hasLOS(x0,y0,x1,y1){
  let dx=Math.abs(x1-x0),dy=Math.abs(y1-y0);
  let sx=x0<x1?1:-1,sy=y0<y1?1:-1;
  let err=dx-dy,x=x0,y=y0;
  for(;;){
    if(x===x1&&y===y1) return true;
    if(G.map[y][x]===CELL.WALL) return false;
    const e2=2*err;
    if(e2>-dy){err-=dy;x+=sx;}
    if(e2<dx){err+=dx;y+=sy;}
  }
}

// ── RAYCASTER (1st person 3D) ────────────────────────────
const canvas3d = document.getElementById('dungeon3d');
const ctx3d    = canvas3d.getContext('2d');
canvas3d.width = SCREEN_W;
canvas3d.height= SCREEN_H;

// Wall textures — simple procedural patterns
const WALL_COLS = [
  ['#1a1208','#2a1e10'],   // stone
  ['#0a1020','#0d1830'],   // dungeon
  ['#180806','#280e0a'],   // lava
  ['#050a05','#0a1408'],   // moss
];
const FLOOR_COL = '#0a0c10';
const CEIL_COL  = '#050508';

function render3D(){
  if(!G||!G.map||!G.map.length) return;
  ctx3d.clearRect(0,0,SCREEN_W,SCREEN_H);

  // Ceiling
  ctx3d.fillStyle=CEIL_COL;
  ctx3d.fillRect(0,0,SCREEN_W,SCREEN_H/2);
  // Floor
  const flGrad=ctx3d.createLinearGradient(0,SCREEN_H/2,0,SCREEN_H);
  flGrad.addColorStop(0,'#0e1018');
  flGrad.addColorStop(1,'#070810');
  ctx3d.fillStyle=flGrad;
  ctx3d.fillRect(0,SCREEN_H/2,SCREEN_W,SCREEN_H/2);

  // Player direction → angle
  const baseAngle = (G.dir * Math.PI/2);

  for(let col=0;col<NUM_RAYS;col++){
    const rayAngle = baseAngle - HALF_FOV + (col/NUM_RAYS)*FOV;
    const cosA=Math.cos(rayAngle), sinA=Math.sin(rayAngle);

    // DDA
    let rx=G.px+0.5, ry=G.py+0.5;
    const dx=cosA, dy=sinA;
    let dist=0;
    let hit=false;
    let hitCell=CELL.WALL;
    let side=0; // 0=x-side, 1=y-side

    // Step DDA
    const stepX=dx>=0?1:-1, stepY=dy>=0?1:-1;
    let mapX=Math.floor(rx), mapY=Math.floor(ry);
    const deltaDistX=Math.abs(1/dx)||1e30;
    const deltaDistY=Math.abs(1/dy)||1e30;
    let sideDistX=(dx>=0?(mapX+1-rx):(rx-mapX))*deltaDistX;
    let sideDistY=(dy>=0?(mapY+1-ry):(ry-mapY))*deltaDistY;

    for(let steps=0;steps<MAX_RAY_DIST*2;steps++){
      if(sideDistX<sideDistY){sideDistX+=deltaDistX;mapX+=stepX;side=0;}
      else{sideDistY+=deltaDistY;mapY+=stepY;side=1;}
      if(mapX<0||mapY<0||mapX>=MAP_W||mapY>=MAP_H){hit=true;dist=MAX_RAY_DIST;break;}
      if(G.map[mapY][mapX]===CELL.WALL){
        hit=true;
        dist=side===0?(sideDistX-deltaDistX):(sideDistY-deltaDistY);
        dist=Math.max(0.1,dist);
        hitCell=CELL.WALL;
        break;
      }
    }

    if(!hit) dist=MAX_RAY_DIST;
    // Correct fisheye
    dist*=Math.cos(rayAngle-baseAngle);

    const wallH=Math.min(SCREEN_H, Math.floor(SCREEN_H/Math.max(0.01,dist)));
    const wallTop=Math.floor((SCREEN_H-wallH)/2);

    // Wall color based on distance + side
    const ci=Math.floor((G.floor-1)/3)%WALL_COLS.length;
    const [darkC,brightC]=WALL_COLS[ci];
    const fog=Math.min(1,dist/MAX_RAY_DIST);
    const brightness=side===1?0.7:1.0;
    const alpha=1-fog*0.85;

    // Draw wall strip
    const sliceW=Math.ceil(SCREEN_W/NUM_RAYS)+1;
    const x0=Math.floor(col*(SCREEN_W/NUM_RAYS));

    ctx3d.globalAlpha=alpha;
    // subtle stripe texture
    const shade=brightness*(1-fog*0.7);
    ctx3d.fillStyle=interpolateColor(darkC,brightC,shade*(0.4+Math.random()*0.05));
    ctx3d.fillRect(x0,wallTop,sliceW,wallH);
    ctx3d.globalAlpha=1;

    // Torch flicker lines (atmospheric lines)
    if(col%8===0 && dist<6){
      ctx3d.strokeStyle=`rgba(180,100,20,${0.04*(1-dist/6)})`;
      ctx3d.lineWidth=1;
      ctx3d.beginPath();
      ctx3d.moveTo(x0,wallTop);
      ctx3d.lineTo(x0,wallTop+wallH);
      ctx3d.stroke();
    }
  }

  // Draw sprites (monsters, items on floor)
  drawSprites(baseAngle);

  // Torch vignette
  const vign=ctx3d.createRadialGradient(SCREEN_W/2,SCREEN_H/2,SCREEN_H*0.2,SCREEN_W/2,SCREEN_H/2,SCREEN_H*0.75);
  vign.addColorStop(0,'rgba(0,0,0,0)');
  vign.addColorStop(1,'rgba(0,0,0,0.75)');
  ctx3d.fillStyle=vign;
  ctx3d.fillRect(0,0,SCREEN_W,SCREEN_H);

  // Torch light flicker (bottom glow)
  const torchAlpha=0.04+Math.sin(G.turns*0.5)*0.015;
  const torchGrad=ctx3d.createRadialGradient(SCREEN_W/2,SCREEN_H,0,SCREEN_W/2,SCREEN_H,SCREEN_H*0.6);
  torchGrad.addColorStop(0,`rgba(220,140,30,${torchAlpha})`);
  torchGrad.addColorStop(1,'rgba(0,0,0,0)');
  ctx3d.fillStyle=torchGrad;
  ctx3d.fillRect(0,0,SCREEN_W,SCREEN_H);
}

function interpolateColor(c1,c2,t){
  const r1=parseInt(c1.slice(1,3),16),g1=parseInt(c1.slice(3,5),16),b1=parseInt(c1.slice(5,7),16);
  const r2=parseInt(c2.slice(1,3),16),g2=parseInt(c2.slice(3,5),16),b2=parseInt(c2.slice(5,7),16);
  const r=Math.round(r1+(r2-r1)*t),g=Math.round(g1+(g2-g1)*t),b=Math.round(b1+(b2-b1)*t);
  return `rgb(${r},${g},${b})`;
}

function drawSprites(baseAngle){
  const px=G.px+0.5, py=G.py+0.5;

  // Collect visible entities
  const entities=[];
  for(const mon of G.monsters){
    if(!G.visible[mon.y]?.[mon.x]) continue;
    entities.push({x:mon.x+0.5,y:mon.y+0.5,icon:mon.i,type:'monster',ref:mon});
  }
  for(const it of G.items){
    if(!G.visible[it.y]?.[it.x]) continue;
    entities.push({x:it.x+0.5,y:it.y+0.5,icon:it.i,type:'item',ref:it});
  }
  // Special tiles
  for(let ty=0;ty<MAP_H;ty++){
    for(let tx=0;tx<MAP_W;tx++){
      if(!G.visible[ty][tx]) continue;
      const ct=G.map[ty][tx];
      if(ct===CELL.STAIRS) entities.push({x:tx+0.5,y:ty+0.5,icon:'🪜',type:'tile'});
      else if(ct===CELL.SHOP) entities.push({x:tx+0.5,y:ty+0.5,icon:'🏪',type:'tile'});
      else if(ct===CELL.CHEST) entities.push({x:tx+0.5,y:ty+0.5,icon:'📦',type:'tile'});
    }
  }

  // Sort by distance desc
  entities.sort((a,b)=>{
    const da=(a.x-px)**2+(a.y-py)**2;
    const db=(b.x-px)**2+(b.y-py)**2;
    return db-da;
  });

  for(const ent of entities){
    const dx=ent.x-px, dy=ent.y-py;
    const dist=Math.sqrt(dx*dx+dy*dy);
    if(dist<0.5||dist>12) continue;

    // Transform to view space
    const invDet=1/(Math.cos(baseAngle)*Math.sin(baseAngle+Math.PI/2)-Math.sin(baseAngle)*Math.cos(baseAngle+Math.PI/2));
    const tx2=invDet*(Math.cos(baseAngle+Math.PI/2)*dx-Math.sin(baseAngle+Math.PI/2)*dy);
    const ty2=invDet*(-Math.sin(baseAngle)*dx+Math.cos(baseAngle)*dy);

    // Simple billboard: ty2 is depth
    const depth=dist*Math.cos(Math.atan2(dy,dx)-baseAngle);
    if(depth<=0.2) continue;

    const sprH=Math.min(SCREEN_H, Math.abs(Math.floor(SCREEN_H/depth)));
    const drawStart=Math.floor((SCREEN_H-sprH)/2);

    // Center X
    const sprX=Math.floor((SCREEN_W/2)*(1+tx2/ty2));
    const sprW=sprH;

    if(sprX+sprW<0||sprX>SCREEN_W) continue;
    if(dist>8) continue;

    const fog=Math.min(1,dist/8);
    ctx3d.globalAlpha=Math.max(0.1,1-fog);

    // Draw emoji sprite
    ctx3d.font=`${Math.max(8,sprW*0.6)}px serif`;
    ctx3d.textAlign='center';
    ctx3d.textBaseline='middle';
    ctx3d.fillText(ent.icon, sprX, drawStart+sprH/2);

    // Monster HP bar
    if(ent.type==='monster' && dist<4){
      const barW=sprW*1.2;
      const barX=sprX-barW/2;
      const barY=drawStart-6;
      ctx3d.fillStyle='rgba(0,0,0,0.6)';
      ctx3d.fillRect(barX,barY,barW,4);
      const pct=ent.ref.hp/ent.ref.maxHp;
      ctx3d.fillStyle=pct>0.5?'#22c55e':pct>0.25?'#f59e0b':'#ef4444';
      ctx3d.fillRect(barX,barY,barW*pct,4);
    }
    ctx3d.globalAlpha=1;
  }
}

// ── MINIMAP CANVAS ──────────────────────────────────────
const mmCanvas=document.getElementById('minimap-canvas');
const mmCtx=mmCanvas.getContext('2d');

function renderMinimap(){
  if(!G||!G.map) return;
  mmCtx.clearRect(0,0,110,110);
  const cellW=110/MAP_W, cellH=110/MAP_H;
  for(let y=0;y<MAP_H;y++){
    for(let x=0;x<MAP_W;x++){
      if(!G.revealed[y][x]){mmCtx.fillStyle='#000';mmCtx.fillRect(x*cellW,y*cellH,cellW,cellH);continue;}
      const ct=G.map[y][x];
      let c='#1a2a45';
      if(ct===CELL.WALL) c='#060c18';
      else if(ct===CELL.STAIRS) c='#22d3ee';
      else if(ct===CELL.SHOP) c='#f59e0b';
      else if(ct===CELL.CHEST) c='#e8a020';
      if(!G.visible[y][x]) c=mixColor(c,'#000',0.5);
      mmCtx.fillStyle=c;
      mmCtx.fillRect(x*cellW,y*cellH,cellW,cellH);
      // monsters
      if(G.visible[y][x]&&G.monsters.some(m=>m.x===x&&m.y===y)){
        mmCtx.fillStyle=m=>m.boss?'#ff8000':'#ef4444';
        mmCtx.fillStyle='#ef4444';
        mmCtx.fillRect(x*cellW+cellW*0.2,y*cellH+cellH*0.2,cellW*0.6,cellH*0.6);
      }
    }
  }
  // Player triangle
  const px2=(G.px+0.5)*cellW, py2=(G.py+0.5)*cellH;
  const angle=G.dir*Math.PI/2;
  const sz=3;
  mmCtx.fillStyle='#39ff7a';
  mmCtx.beginPath();
  mmCtx.moveTo(px2+Math.cos(angle)*sz*1.5, py2+Math.sin(angle)*sz*1.5);
  mmCtx.lineTo(px2+Math.cos(angle+2.4)*sz, py2+Math.sin(angle+2.4)*sz);
  mmCtx.lineTo(px2+Math.cos(angle-2.4)*sz, py2+Math.sin(angle-2.4)*sz);
  mmCtx.closePath();
  mmCtx.fill();
}

function mixColor(c1,c2,t){
  if(!c1.startsWith('#')||!c2.startsWith('#')) return c1;
  const r1=parseInt(c1.slice(1,3),16),g1=parseInt(c1.slice(3,5),16),b1=parseInt(c1.slice(5,7),16);
  const r2=parseInt(c2.slice(1,3),16),g2=parseInt(c2.slice(3,5),16),b2=parseInt(c2.slice(5,7),16);
  const r=Math.round(r1*(1-t)+r2*t),g=Math.round(g1*(1-t)+g2*t),b=Math.round(b1*(1-t)+b2*t);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`;
}

// ── HUD UPDATE ──────────────────────────────────────────
function updateHUD(){
  document.getElementById('h-hp').textContent=`${G.hp}/${G.maxHp}`;
  document.getElementById('h-xp').textContent=`${G.xp}/${G.xpNext}`;
  document.getElementById('h-mp').textContent=`${G.mp}/${G.maxMp}`;
  document.getElementById('hp-fill').style.width=Math.max(0,(G.hp/G.maxHp)*100)+'%';
  document.getElementById('xp-fill').style.width=Math.max(0,(G.xp/G.xpNext)*100)+'%';
  document.getElementById('mp-fill').style.width=Math.max(0,(G.mp/G.maxMp)*100)+'%';
  document.getElementById('floor-badge').textContent=`B${G.floor}F`;
  document.getElementById('t-kills').textContent=G.kills;
  document.getElementById('t-turns').textContent=G.turns;
  document.getElementById('t-score').textContent=G.score;
  document.getElementById('p-name').textContent=G.name;
  document.getElementById('p-class').textContent=G.clsName;
  document.getElementById('p-lv').textContent=G.level;
  document.getElementById('p-gold').textContent=G.gold;
  document.getElementById('p-atk').textContent=totalAtk();
  document.getElementById('p-def').textContent=totalDef();
  document.getElementById('p-spd').textContent=G.spd;
  document.getElementById('p-crit').textContent=G.crit+'%';

  // Skill bar
  const sb=document.getElementById('skillbar');
  sb.innerHTML='';
  G.skills.forEach((sk,i)=>{
    const div=document.createElement('div');
    div.className='skill-slot'+(sk.cdLeft>0?' on-cooldown':'');
    div.title=`${sk.name}: ${sk.desc} (MP:${sk.mp})`;
    div.innerHTML=sk.icon;
    const kl=document.createElement('span');kl.className='sk-key';kl.textContent=i+1;
    div.appendChild(kl);
    if(sk.cdLeft>0){const cd=document.createElement('div');cd.className='sk-cd';cd.textContent=sk.cdLeft;div.appendChild(cd);}
    sb.appendChild(div);
  });

  // Equipped panel
  const slots=[
    {key:'weapon',label:'무기',empty:'⚔️'},
    {key:'armor',label:'갑옷',empty:'🧥'},
    {key:'shield',label:'방패',empty:'🛡️'},
    {key:'helmet',label:'투구',empty:'⛑️'},
    {key:'boots',label:'장화',empty:'👟'},
    {key:'ring',label:'반지',empty:'💍'},
  ];
  const eg=document.getElementById('equipped-grid');
  eg.innerHTML='';
  slots.forEach(s=>{
    const item=G.equipped[s.key];
    const div=document.createElement('div');
    div.className='eq-slot'+(item?' filled':'');
    div.title=item?`${item.n}: ${item.desc}`:s.label;
    div.innerHTML=`${item?item.i:s.empty}<div class="eq-label">${s.label}</div>`;
    div.onclick=()=>{if(item){unequipItem(s.key);}};
    eg.appendChild(div);
  });

  // Target HP bar
  const frontMon=getAdjacentMonster();
  const mwrap=document.getElementById('mob-hpbar-wrap');
  if(frontMon){
    mwrap.classList.add('show');
    document.getElementById('mob-hpbar-name').textContent=`${frontMon.i} ${frontMon.n} ${frontMon.boss?'[BOSS]':''}`;
    document.getElementById('mob-hpbar-fill').style.width=Math.max(0,(frontMon.hp/frontMon.maxHp)*100)+'%';
  } else {
    mwrap.classList.remove('show');
  }
}

// ── GAME LOOP ────────────────────────────────────────────
let lastRender=0;
function gameLoop(ts){
  if(!G||G.gameOver||G.victory) return;
  if(ts-lastRender>50){ // ~20fps
    render3D();
    renderMinimap();
    updateHUD();
    lastRender=ts;
  }
  animFrame=requestAnimationFrame(gameLoop);
}

// ── MOVEMENT ────────────────────────────────────────────
function move(forward){
  if(!G||G.gameOver||G.victory) return;
  if(G.stunned>0){addLog('⛔ 스턴 상태!','system');endTurn();return;}
  const [dx,dy]=DIRS[G.dir];
  const nx=G.px+(forward?dx:-dx);
  const ny=G.py+(forward?dy:-dy);
  if(nx<0||ny<0||nx>=MAP_W||ny>=MAP_H) return;
  const ct=G.map[ny][nx];
  if(ct===CELL.WALL) return;

  // Monster block
  const mon=G.monsters.find(m=>m.x===nx&&m.y===ny);
  if(mon){playerAttack(mon);endTurn();return;}

  G.px=nx; G.py=ny;
  handleCellEvent(nx,ny);
  endTurn();
}

function strafe(right){
  if(!G||G.gameOver||G.victory) return;
  if(G.stunned>0){addLog('⛔ 스턴 상태!','system');endTurn();return;}
  const strafeDir=(G.dir+(right?1:3))%4;
  const [dx,dy]=DIRS[strafeDir];
  const nx=G.px+dx, ny=G.py+dy;
  if(nx<0||ny<0||nx>=MAP_W||ny>=MAP_H) return;
  if(G.map[ny][nx]===CELL.WALL) return;
  const mon=G.monsters.find(m=>m.x===nx&&m.y===ny);
  if(mon){playerAttack(mon);endTurn();return;}
  G.px=nx; G.py=ny;
  handleCellEvent(nx,ny);
  endTurn();
}

function turn(right){
  if(!G||G.gameOver||G.victory) return;
  G.dir=(G.dir+(right?1:3))%4;
  updateFOV();
  render3D();renderMinimap();updateHUD();
}

function interact(){
  if(!G||G.gameOver||G.victory) return;
  // Check front cell
  const [dx,dy]=DIRS[G.dir];
  const fx=G.px+dx, fy=G.py+dy;
  if(fx<0||fy<0||fx>=MAP_W||fy>=MAP_H) return;
  const ct=G.map[fy][fx];
  const mon=G.monsters.find(m=>m.x===fx&&m.y===fy);
  if(mon){playerAttack(mon);endTurn();return;}
  if(ct===CELL.SHOP){openShop();return;}
  if(ct===CELL.CHEST){openChest(fx,fy);return;}
  if(ct===CELL.STAIRS){descend();return;}
  // Check current cell
  const cc=G.map[G.py][G.px];
  if(cc===CELL.STAIRS){descend();return;}
  if(cc===CELL.SHOP){openShop();return;}
  addLog('상호작용할 대상 없음','system');
}

function handleCellEvent(x,y){
  const ct=G.map[y][x];
  if(ct===CELL.STAIRS) addLog('🪜 계단 발견! Space/E 로 내려가기','system');
  else if(ct===CELL.SHOP) openShop();
  else if(ct===CELL.CHEST){openChest(x,y);return;}
  // Pick up items
  const idx=G.items.findIndex(i=>i.x===x&&i.y===y);
  if(idx>-1){
    const it=G.items[idx];
    if(G.inv.length<24){
      G.inv.push(it);G.items.splice(idx,1);
      addLog(`🎒 ${it.i}${it.n} 획득!`,'item');
    } else {addLog('🎒 인벤토리 가득!','system');}
  }
}

function openChest(x,y){
  G.map[y][x]=CELL.FLOOR;
  const pool=ITEMS.filter(i=>i.id!=='sc5'&&['uncommon','rare','epic'].includes(i.r));
  const item=pool[Math.floor(Math.random()*pool.length)];
  const gold=50+Math.floor(Math.random()*150)*G.floor;
  G.gold+=gold;
  if(G.inv.length<24){
    G.inv.push({...item,uid:item.id+'_'+Math.random().toString(36).slice(2),x,y});
    addLog(`📦 보물상자! ${item.i}${item.n} + 💰${gold}골드`,'item');
  } else {
    addLog(`📦 보물상자! 💰${gold}골드 (인벤 가득)`,'item');
  }
}

function descend(){
  if(G.floor>=MAX_FLOOR){gameVictory();return;}
  G.floor++;
  addLog(`🪜 B${G.floor}F으로 하강...`,'system');
  G.hp=Math.min(G.maxHp,G.hp+Math.floor(G.maxHp*0.25));
  G.mp=Math.min(G.maxMp,G.mp+Math.floor(G.maxMp*0.5));
  makeMap();
}

function waitTurn(){
  if(!G||G.gameOver||G.victory) return;
  if(G.clsId==='paladin') G.hp=Math.min(G.maxHp,G.hp+Math.ceil(G.maxHp*0.04));
  G.mp=Math.min(G.maxMp,G.mp+2);
  addLog('⏳ 대기 (HP·MP 소폭 회복)','system');
  endTurn();
}

// ── COMBAT ──────────────────────────────────────────────
function totalAtk(){
  let a=G.atk;
  for(const it of Object.values(G.equipped)) if(it?.atk) a+=it.atk;
  for(const b of G.buffs) if(b.type==='atk') a+=b.val;
  return a;
}
function totalDef(){
  let d=G.def;
  for(const it of Object.values(G.equipped)) if(it?.def) d+=it.def;
  for(const b of G.buffs) if(b.type==='def') d+=b.val;
  return d;
}
function totalCrit(){
  let c=G.crit;
  for(const b of G.buffs) if(b.type==='crit') c+=b.val;
  return c;
}

function getAdjacentMonster(){
  const [dx,dy]=DIRS[G.dir];
  return G.monsters.find(m=>m.x===G.px+dx&&m.y===G.py+dy)||null;
}

function playerAttack(mon){
  let atk=totalAtk();
  // Berserker bonus: more HP lost = more ATK
  if(G.clsId==='berserker'){
    const hpLostPct=1-(G.hp/G.maxHp);
    atk=Math.round(atk*(1+hpLostPct*0.8));
  }
  let dmg=Math.max(1, atk-mon.def + Math.floor(Math.random()*5)-2);
  const crit=Math.random()*100<totalCrit();
  if(crit) dmg=Math.round(dmg*1.8);

  // Dodge
  if(G.dodgeTurns>0){G.dodgeTurns--;addLog(`💨 회피 발동 (${G.dodgeTurns}턴 남음)`,'skill');}

  mon.hp-=dmg;
  addLog(`⚔️ ${mon.n}에게 ${dmg}${crit?' ⚡크리!':''}`,'player');
  hitFlash();
  if(mon.hp<=0){killMonster(mon);return;}
}

function useSkill(idx){
  if(!G||G.gameOver||G.victory) return;
  if(idx>=G.skills.length) return;
  const sk=G.skills[idx];
  if(sk.cdLeft>0){addLog(`⛔ ${sk.name} 쿨다운: ${sk.cdLeft}턴`,'system');return;}
  if(sk.mp>0&&G.mp<sk.mp){addLog(`🔷 MP 부족! (${G.mp}/${sk.mp})`,'system');return;}

  G.mp=Math.max(0,G.mp-sk.mp);
  sk.cdLeft=sk.cd;

  const front=getAdjacentMonster();
  let used=false;

  // Execute skill
  if(sk.dmgMult&&front){
    let atk=totalAtk();
    if(G.clsId==='berserker'){const hp2=(1-G.hp/G.maxHp);atk=Math.round(atk*(1+hp2*0.8));}
    let dmg=Math.max(1,Math.round((atk-front.def+Math.floor(Math.random()*5)-2)*sk.dmgMult));
    if(sk.critForce||Math.random()*100<totalCrit()*1.5) dmg=Math.round(dmg*1.8);
    if(sk.execHp&&front.hp/front.maxHp<sk.execHp){front.hp=0;addLog(`💀 처형! ${front.n} 즉사!`,'boss');}
    else{
      front.hp-=dmg;
      addLog(`✨[${sk.name}] ${front.n}에게 ${dmg} 피해`,'skill');
    }
    if(sk.lifeSteal) G.hp=Math.min(G.maxHp,G.hp+Math.round(dmg*sk.lifeSteal));
    if(sk.healSelf) G.hp=Math.min(G.maxHp,G.hp+sk.healSelf);
    if(sk.stun&&front.hp>0) front.stunned=(sk.stun||1);
    if(sk.poisonTurns&&front.hp>0) front.poisoned=(sk.poisonTurns||3);
    if(sk.freeze&&front.hp>0) front.frozen=(sk.freeze||1);
    if(sk.selfHp) G.hp=Math.max(1,G.hp+sk.selfHp);
    if(sk.hits&&front.hp>0){
      for(let h=1;h<sk.hits;h++){
        let d=Math.max(1,Math.round((totalAtk()-front.def+Math.floor(Math.random()*3))*sk.dmgMult));
        front.hp-=d;
        addLog(`  ${h+1}타: ${d} 피해`,'skill');
        if(front.hp<=0) break;
      }
    }
    if(front.hp<=0) killMonster(front);
    used=true;
  }
  if(sk.dmgFlat){
    const t=front||G.monsters.find(m=>G.visible[m.y]?.[m.x]);
    if(t){
      let dmg=sk.dmgFlat+Math.floor(Math.random()*10);
      // mage INT bonus
      if(G.clsId==='mage') dmg=Math.round(dmg*1.3);
      t.hp-=dmg;
      addLog(`✨[${sk.name}] ${t.n}에게 ${dmg} 마법 피해`,'skill');
      if(sk.stun) t.stunned=(sk.stun||1);
      if(sk.freeze) t.frozen=(sk.freeze||1);
      if(sk.healSelf) G.hp=Math.min(G.maxHp,G.hp+sk.healSelf);
      if(t.hp<=0) killMonster(t);
      used=true;
    }
  }
  if(sk.dmgAll){
    let total=0;
    const dead=[];
    for(const m of G.monsters){
      if(!G.visible[m.y]?.[m.x]) continue;
      let d=sk.dmgAll+Math.floor(Math.random()*15);
      if(G.clsId==='mage') d=Math.round(d*1.3);
      m.hp-=d;total+=d;
      if(sk.stun) m.stunned=1;
      if(m.hp<=0) dead.push(m);
    }
    dead.forEach(m=>killMonster(m));
    G.monsters=G.monsters.filter(m=>m.hp>0);
    addLog(`✨[${sk.name}] 전체 피해! 총 ${total}`,'skill');
    if(sk.healSelf) G.hp=Math.min(G.maxHp,G.hp+sk.healSelf);
    used=true;
  }
  if(sk.healPct){
    const h=Math.round(G.maxHp*sk.healPct);
    G.hp=Math.min(G.maxHp,G.hp+h);
    addLog(`💚[${sk.name}] HP+${h} 회복!`,'skill');
    used=true;
  }
  if(sk.mpRestore){G.mp=Math.min(G.maxMp,G.mp+sk.mpRestore);addLog(`🔷 MP+${sk.mpRestore}`,'skill');used=true;}
  if(sk.buffAtk){G.buffs.push({type:'atk',val:sk.buffAtk,turns:sk.buffTurns||3});addLog(`⬆️[${sk.name}] ATK+${sk.buffAtk} (${sk.buffTurns}턴)`,'skill');used=true;}
  if(sk.buffDef){G.buffs.push({type:'def',val:sk.buffDef,turns:sk.buffTurns||3});addLog(`⬆️[${sk.name}] DEF+${sk.buffDef} (${sk.buffTurns}턴)`,'skill');used=true;}
  if(sk.critBuff){G.buffs.push({type:'crit',val:sk.critBuff,turns:sk.buffTurns||3});addLog(`⬆️[${sk.name}] 크리+${sk.critBuff}% (${sk.buffTurns}턴)`,'skill');used=true;}
  if(sk.shieldTurns){G.shieldTurns=sk.shieldTurns;addLog(`🛡️[${sk.name}] ${sk.shieldTurns}턴 무적!`,'skill');used=true;}
  if(sk.dodgeTurns){G.dodgeTurns=sk.dodgeTurns;addLog(`💨[${sk.name}] ${sk.dodgeTurns}턴 회피!`,'skill');used=true;}
  if(sk.curseTurns&&front){front.cursed=sk.curseTurns;addLog(`⛧[${sk.name}] ${front.n} 저주!`,'skill');used=true;}
  if(sk.summon){
    // Summon a basic undead ally
    const summonMon=MON_DATA.find(m=>m.id==='zombie');
    const sc=1+(G.floor-1)*0.15;
    G.monsters.push({
      ...summonMon,uid:'summon_'+Date.now(),
      hp:Math.round(summonMon.hp*sc*1.5),maxHp:Math.round(summonMon.hp*sc*1.5),
      atk:Math.round(summonMon.atk*sc),
      x:G.px+(Math.random()<0.5?1:-1),y:G.py+(Math.random()<0.5?1:-1),
      friendly:true, frozen:0, stunned:0
    });
    addLog(`💀[${sk.name}] 언데드 소환!`,'skill');
    used=true;
  }
  if(sk.execSelf&&front){
    // Last Stand: damage based on HP lost
    const missingHp=G.maxHp-G.hp;
    let dmg=Math.max(1,Math.round(missingHp*1.2));
    front.hp-=dmg;
    addLog(`🏴[${sk.name}] ${front.n}에게 ${dmg} 피해! (HP 손실 비례)`,'boss');
    if(front.hp<=0) killMonster(front);
    used=true;
  }

  if(!used) addLog(`[${sk.name}] 사용 (대상 없음)`,'system');
  endTurn();
}

function killMonster(mon){
  G.kills++;
  G.xp+=mon.xp;
  G.gold+=mon.gold;
  G.score+=mon.xp*(G.floor+1);
  addLog(`💀 ${mon.n} 처치! XP+${mon.xp} G+${mon.gold}`,mon.boss?'boss':'player');
  // Drop
  if(Math.random()<0.35){
    const pool=ITEMS.filter(i=>i.t!=='gold');
    const drop=pool[Math.floor(Math.random()*pool.length)];
    G.items.push({...drop,uid:drop.id+'_'+Date.now(),x:mon.x,y:mon.y});
    addLog(`📦 드롭: ${drop.i}${drop.n}`,'item');
  }
  G.monsters=G.monsters.filter(m=>m.uid!==mon.uid);
  while(G.xp>=G.xpNext) levelUp();
  if(mon.boss&&G.floor===MAX_FLOOR) gameVictory();
}

function monstersTurn(){
  for(const mon of [...G.monsters]){
    if(mon.friendly) continue; // friendly summons don't attack
    if(!G.visible[mon.y]?.[mon.x]) continue;
    if(mon.frozen>0){mon.frozen--;continue;}
    if(mon.stunned>0){mon.stunned--;continue;}

    const pdx=G.px-mon.x, pdy=G.py-mon.y;
    const dist=Math.abs(pdx)+Math.abs(pdy);

    if(dist===1){
      // Attack player
      if(G.shieldTurns>0){addLog(`🛡️ 무적! ${mon.n}의 공격 무효화`,'skill');}
      else {
        let dmg=Math.max(0,mon.atk-totalDef()+Math.floor(Math.random()*4)-2);
        if(mon.cursed) dmg=Math.round(dmg*0.7);
        if(G.dodgeTurns>0){G.dodgeTurns--;addLog(`💨 회피! ${mon.n}의 공격 회피`,'player');continue;}
        G.hp=Math.max(0,G.hp-dmg);
        addLog(`👹 ${mon.n}이 ${dmg} 피해!`,'monster');
        // paladin regen passive
        if(G.clsId==='paladin'&&G.turns%3===0&&G.hp<G.maxHp)
          G.hp=Math.min(G.maxHp,G.hp+Math.ceil(G.maxHp*0.02));
        // poison from monster
        if(mon.id==='spider'||mon.id==='medusa'||mon.id==='basilisk'){
          if(Math.random()<0.3){G.poison=3;addLog('☠️ 독에 감염!','monster');}
        }
        if(G.hp<=0){gameDie(mon.n);return;}
      }
      continue;
    }

    // Move
    let mx=0, my=0;
    if(mon.mv==='rnd'){
      const d=DIRS[Math.floor(Math.random()*4)];mx=d[0];my=d[1];
    } else if(mon.mv==='slow'){
      if(G.turns%2===0){mx=Math.sign(pdx);my=0;if(!mx)my=Math.sign(pdy);}
    } else if(mon.mv==='phase'){
      mx=Math.sign(pdx);my=Math.sign(pdy);
    } else if(mon.mv==='rng'){
      // ranged: attack if close enough
      if(dist<=5){
        let dmg=Math.max(0,Math.round(mon.atk*0.8)-totalDef()/2+Math.floor(Math.random()*4));
        if(G.shieldTurns<=0){
          G.hp=Math.max(0,G.hp-dmg);
          addLog(`🎯 ${mon.n}의 원거리 공격! ${dmg} 피해`,'monster');
          if(G.hp<=0){gameDie(mon.n);return;}
        }
        continue;
      }
      mx=Math.sign(pdx);my=0;if(!mx)my=Math.sign(pdy);
    } else if(mon.mv==='boss'){
      mx=Math.sign(pdx);my=0;if(!mx)my=Math.sign(pdy);
      // Boss: multi-hit occasionally
      if(G.turns%4===0&&dist===1){
        for(let h=0;h<2;h++){
          if(G.hp<=0) break;
          let dmg=Math.max(0,mon.atk-totalDef()+Math.floor(Math.random()*6));
          if(G.shieldTurns<=0){G.hp=Math.max(0,G.hp-dmg);addLog(`💥 [보스 연속] ${dmg} 피해!`,'boss');}
        }
        if(G.hp<=0){gameDie(mon.n);return;}
        continue;
      }
    } else {
      mx=Math.sign(pdx);my=0;if(!mx)my=Math.sign(pdy);
    }

    const nx=mon.x+mx, ny=mon.y+my;
    if(nx>=0&&ny>=0&&nx<MAP_W&&ny<MAP_H){
      if(G.map[ny][nx]!==CELL.WALL&&!G.monsters.some(m=>m.x===nx&&m.y===ny&&m.uid!==mon.uid)){
        mon.x=nx;mon.y=ny;
      }
    }
  }

  // Poison tick
  if(G.poison>0){
    const pd=Math.ceil(G.maxHp*0.04);
    G.hp=Math.max(1,G.hp-pd);
    G.poison--;
    addLog(`☠️ 독 피해 ${pd} (${G.poison}턴 남음)`,'monster');
    if(G.hp<=0){gameDie('독');return;}
  }
}

function endTurn(){
  G.turns++;
  // Buff ticks
  G.buffs=G.buffs.filter(b=>{b.turns--;return b.turns>0;});
  if(G.shieldTurns>0) G.shieldTurns--;
  // Skill CD
  G.skills.forEach(sk=>{if(sk.cdLeft>0)sk.cdLeft--;});
  // MP regen
  G.mp=Math.min(G.maxMp,G.mp+1);
  monstersTurn();
  updateFOV();
}

function levelUp(){
  G.level++;
  G.xp-=G.xpNext;
  G.xpNext=Math.floor(G.xpNext*1.6);
  addLog(`⬆️ 레벨 UP! Lv${G.level}`,'system');
  showLvlFX();
  // Passive stat gain
  G.maxHp+=5;G.hp=Math.min(G.maxHp,G.hp+10);
  G.maxMp+=3;G.mp=Math.min(G.maxMp,G.mp+5);
  document.getElementById('lvl-modal').classList.remove('hidden');
}

function allocate(stat){
  if(stat==='hp'){G.maxHp+=20;G.hp=Math.min(G.maxHp,G.hp+20);}
  else if(stat==='atk') G.atk+=3;
  else if(stat==='def') G.def+=2;
  else if(stat==='spd') G.spd+=1;
  else if(stat==='mp'){G.maxMp+=15;G.mp=Math.min(G.maxMp,G.mp+15);}
  else if(stat==='crit') G.crit+=3;
  document.getElementById('lvl-modal').classList.add('hidden');
}

// ── ITEMS ────────────────────────────────────────────────
function useItemObj(item){
  if(item.t==='potion'){
    if(item.heal){G.hp=Math.min(G.maxHp,G.hp+item.heal);addLog(`🧪 ${item.n}: HP+${item.heal}`,'item');}
    if(item.mpHeal){G.mp=Math.min(G.maxMp,G.mp+item.mpHeal);addLog(`🔵 MP+${item.mpHeal}`,'item');}
    removeInv(item.uid);
  } else if(['weapon','armor','shield','helmet','boots','ring'].includes(item.t)){
    if(G.equipped[item.t]) G.inv.push(G.equipped[item.t]);
    G.equipped[item.t]=item;
    removeInv(item.uid);
    // Apply ring/boot/helm bonuses immediately
    if(item.hp){G.maxHp+=item.hp;G.hp=Math.min(G.maxHp,G.hp+item.hp);}
    if(item.mp){G.maxMp+=item.mp;G.mp=Math.min(G.maxMp,G.mp+item.mp);}
    if(item.spd) G.spd+=item.spd;
    addLog(`⚔️ ${item.n} 장착!`,'item');
  } else if(item.t==='scroll'){
    useScroll(item);removeInv(item.uid);
  } else if(item.t==='gem'){
    G.xp+=item.xp;addLog(`💎 경험치+${item.xp}`,'item');
    while(G.xp>=G.xpNext) levelUp();
    removeInv(item.uid);
  } else if(item.t==='gold'){
    G.gold+=item.gold;addLog(`💰 골드+${item.gold}`,'item');
    removeInv(item.uid);
  } else if(item.t==='key'){
    addLog('🗝️ 황금 열쇠 (보물상자 위에서 사용)','item');
  }
}

function unequipItem(slot){
  const item=G.equipped[slot];
  if(!item) return;
  if(G.inv.length>=24){addLog('인벤 가득!','system');return;}
  // Remove stat bonuses from accessories
  if(item.hp){G.maxHp-=item.hp;G.hp=Math.min(G.maxHp,G.hp);}
  if(item.mp){G.maxMp-=item.mp;G.mp=Math.min(G.maxMp,G.mp);}
  if(item.spd) G.spd-=item.spd;
  G.inv.push(item);
  G.equipped[slot]=null;
  addLog(`↩️ ${item.n} 해제`,'item');
}

function useScroll(item){
  if(item.dmgAll){
    let tot=0;const dead=[];
    G.monsters.forEach(m=>{if(!G.visible[m.y]?.[m.x])return;m.hp-=item.dmgAll;tot+=item.dmgAll;if(m.hp<=0)dead.push(m);});
    dead.forEach(m=>killMonster(m));
    G.monsters=G.monsters.filter(m=>m.hp>0);
    addLog(`🔥 화염 스크롤! 전체 ${tot} 피해`,'skill');
  }
  if(item.freeze){G.monsters.forEach(m=>m.frozen=item.freeze);addLog('❄️ 빙결 스크롤!','skill');}
  if(item.reveal){G.revealed=G.revealed.map(r=>r.map(()=>true));addLog('🗺️ 전체 맵 공개!','system');}
  if(item.tele){G.px=G.rooms[Math.floor(Math.random()*G.rooms.length)].cx;G.py=G.rooms[Math.floor(Math.random()*G.rooms.length)].cy;addLog('🌀 텔레포트!','system');}
  if(item.curse){G.hp=Math.floor(G.hp/2);addLog('⛧ 저주! HP 반감','monster');}
}

function removeInv(uid){G.inv=G.inv.filter(i=>i.uid!==uid);}

// ── SHOP ─────────────────────────────────────────────────
let shopStock=[];
function openShop(){
  const pool=ITEMS.filter(i=>['potion','scroll','weapon','armor','ring','boots'].includes(i.t));
  const shuf=[...pool].sort(()=>Math.random()-0.5);
  shopStock=shuf.slice(0,5).map(i=>({
    ...i,uid:i.id+'_s'+Date.now(),
    price:Math.round(60+Math.random()*200+G.floor*25)
  }));
  document.getElementById('sh-gold').textContent=G.gold;
  const si=document.getElementById('sh-items');
  si.innerHTML=shopStock.map(item=>`
    <div onclick="buyItem('${item.uid}')" style="display:flex;align-items:center;gap:10px;
      background:rgba(255,255,255,0.04);border:1px solid rgba(232,160,32,0.2);
      border-radius:4px;padding:7px 10px;cursor:pointer;transition:all 0.15s;"
      onmouseenter="this.style.borderColor='rgba(232,160,32,0.5)'"
      onmouseleave="this.style.borderColor='rgba(232,160,32,0.2)'">
      <span style="font-size:1.3rem;">${item.i}</span>
      <div style="flex:1;">
        <div style="font-size:0.72rem;font-weight:700;color:${RARITY_COL[item.r]||'#ddd'};">${item.n}</div>
        <div style="font-size:0.62rem;color:#6a82b4;">${item.desc}</div>
      </div>
      <div style="color:var(--gold);font-size:0.72rem;font-weight:700;">💰${item.price}</div>
    </div>`).join('');
  document.getElementById('shop-modal').classList.remove('hidden');
}
function buyItem(uid){
  const item=shopStock.find(i=>i.uid===uid);
  if(!item) return;
  if(G.gold<item.price){addLog('💰 골드 부족!','system');return;}
  if(G.inv.length>=24){addLog('🎒 인벤토리 가득!','system');return;}
  G.gold-=item.price;
  G.inv.push(item);
  shopStock=shopStock.filter(i=>i.uid!==uid);
  addLog(`🛒 ${item.n} 구매!`,'item');
  document.getElementById('sh-gold').textContent=G.gold;
  openShop();
}
function closeShop(){document.getElementById('shop-modal').classList.add('hidden');}

// ── INVENTORY UI ─────────────────────────────────────────
let selUid=null;
function openInv(){
  selUid=null;selInvItem=null;
  renderInv();
  document.getElementById('inv-modal').classList.remove('hidden');
}
function renderInv(){
  const g=document.getElementById('inv-grid-g');
  const slots=24;let html='';
  for(let i=0;i<slots;i++){
    const it=G.inv[i];
    const eq=it&&Object.values(G.equipped).some(e=>e?.uid===it.uid);
    if(it) html+=`<div class="inv-slot2${selUid===it.uid?' sel-slot':''}" onclick="selSlot('${it.uid}')" title="${it.n}">
      ${it.i}<div class="sn">${it.n}</div>${eq?'<div class="se">E</div>':''}
    </div>`;
    else html+=`<div class="inv-slot2" style="opacity:0.25;cursor:default;"></div>`;
  }
  g.innerHTML=html;
}
function selSlot(uid){
  selUid=uid;selInvItem=G.inv.find(i=>i.uid===uid);
  if(!selInvItem) return;
  const rc=RARITY_COL[selInvItem.r]||'#ddd';
  document.getElementById('iinfo').innerHTML=`
    <span style="font-size:1.3rem">${selInvItem.i}</span>
    <span style="font-weight:700;color:${rc};margin-left:6px">${selInvItem.n}</span>
    <span style="font-size:0.6rem;color:${rc};margin-left:4px">[${selInvItem.r}]</span>
    <div style="color:#6a82b4;font-size:0.68rem;margin-top:4px">${selInvItem.desc}</div>
  `;
  document.getElementById('inv-use-btn').style.display='inline-block';
  document.getElementById('inv-drop-btn').style.display='inline-block';
  renderInv();
}
function useSelItem(){if(!selInvItem) return;closeInv();useItemObj(selInvItem);}
function dropSelItem(){
  if(!selInvItem) return;
  addLog(`🗑️ ${selInvItem.n} 버림`,'system');
  removeInv(selInvItem.uid);
  selUid=null;selInvItem=null;
  document.getElementById('iinfo').innerHTML='<span style="color:#4a3a2a;font-size:0.68rem">아이템을 클릭하여 정보 확인</span>';
  document.getElementById('inv-use-btn').style.display='none';
  document.getElementById('inv-drop-btn').style.display='none';
  renderInv();
}
function closeInv(){document.getElementById('inv-modal').classList.add('hidden');}

// ── EFFECTS ──────────────────────────────────────────────
function hitFlash(){
  const f=document.getElementById('hit-flash');
  f.style.background='rgba(192,57,43,0.3)';
  setTimeout(()=>f.style.background='rgba(192,57,43,0)',120);
}
function showLvlFX(){
  const el=document.createElement('div');
  el.className='lvl-fx';el.textContent='⬆ LEVEL UP!';
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),1500);
}

// ── LOG ──────────────────────────────────────────────────
const MAX_LOG=100;
function addLog(msg,type='system'){
  const el=document.getElementById('log-entries');
  const d=document.createElement('div');
  d.className='le le-'+type;d.textContent=msg;
  el.insertBefore(d,el.firstChild);
  while(el.children.length>MAX_LOG) el.removeChild(el.lastChild);
}

// ── GAME OVER / WIN ──────────────────────────────────────
function gameDie(cause){
  G.gameOver=true;G.hp=0;
  if(animFrame) cancelAnimationFrame(animFrame);
  document.getElementById('death-cause').textContent=`${cause}에 의해 사망`;
  document.getElementById('death-stats').innerHTML=buildStats();
  document.getElementById('death-overlay').classList.remove('hidden');
}
function gameVictory(){
  G.victory=true;
  if(animFrame) cancelAnimationFrame(animFrame);
  G.score+=50000;
  document.getElementById('win-stats').innerHTML=buildStats();
  document.getElementById('win-overlay').classList.remove('hidden');
}
function buildStats(){
  return `
    <div>📊 최종 레벨</div><div><b>${G.level}</b></div>
    <div>🗺️ 최대 층수</div><div><b>B${G.floor}F</b></div>
    <div>💀 처치 수</div><div><b>${G.kills}</b></div>
    <div>⏱ 소요 턴</div><div><b>${G.turns}</b></div>
    <div>💰 골드</div><div><b>${G.gold}</b></div>
    <div>🌟 최종 점수</div><div><b>${G.score}</b></div>
  `;
}

// ── UI FLOW ──────────────────────────────────────────────
function buildClassGrid(){
  const g=document.getElementById('cls-grid');
  g.innerHTML=Object.entries(CLASSES).map(([id,c])=>`
    <div class="cls-card" id="cls-${id}" onclick="selectCls('${id}')">
      <span class="cls-icon">${c.icon}</span>
      <div class="cls-name">${c.name}</div>
      <div class="cls-desc">${c.desc}<br>
        <span style="color:${c.color};font-size:0.48rem;">
          HP${c.hp} MP${c.mp} ATK${c.atk} DEF${c.def} SPD${c.spd}
        </span>
      </div>
    </div>`).join('');
}
function selectCls(id){
  selectedCls=id;
  document.querySelectorAll('.cls-card').forEach(c=>c.classList.remove('sel'));
  document.getElementById('cls-'+id)?.classList.add('sel');
  const btn=document.getElementById('cls-start-btn');
  btn.disabled=false;btn.style.opacity='1';
}
function goClassSelect(){
  const name=document.getElementById('name-inp').value.trim();
  if(!name){document.getElementById('name-inp').style.borderColor='var(--redbright)';return;}
  document.getElementById('title-overlay').classList.add('hidden');
  document.getElementById('class-overlay').classList.remove('hidden');
}
function backTitle(){
  document.getElementById('class-overlay').classList.add('hidden');
  document.getElementById('title-overlay').classList.remove('hidden');
}
function startGame(){
  if(!selectedCls) return;
  const name=document.getElementById('name-inp').value.trim()||'용사';
  document.getElementById('class-overlay').classList.add('hidden');
  initG(name,selectedCls);
  makeMap();
  addLog(`⚔️ ${name}이(가) 던전에 입장!`,'system');
  addLog(`[↑↓] 전진/후진  [A/D] 회전  [Space/E] 공격/상호작용`,'system');
  addLog(`[←/→] 또는 [Q/E] 옆이동  [1-5] 스킬  [I] 인벤토리`,'system');
  if(animFrame) cancelAnimationFrame(animFrame);
  animFrame=requestAnimationFrame(gameLoop);
}
function restartToTitle(){
  if(animFrame) cancelAnimationFrame(animFrame);
  document.getElementById('death-overlay').classList.add('hidden');
  document.getElementById('win-overlay').classList.add('hidden');
  document.getElementById('title-overlay').classList.remove('hidden');
  G=null;selectedCls=null;
  ctx3d.clearRect(0,0,SCREEN_W,SCREEN_H);
  mmCtx.clearRect(0,0,110,110);
}

// ── KEYBOARD ─────────────────────────────────────────────
const modals=['inv-modal','shop-modal','lvl-modal'];
function anyModalOpen(){return modals.some(id=>!document.getElementById(id).classList.contains('hidden'));}

document.addEventListener('keydown',e=>{
  if(anyModalOpen()){
    if(e.key==='Escape'||e.key==='i'||e.key==='I') closeInv();
    if(e.key==='Escape'){closeShop();}
    return;
  }
  if(!G||!G.map||!G.map.length) return;
  if(G.gameOver||G.victory) return;

  switch(e.key){
    case 'ArrowUp':   case 'w': case 'W': e.preventDefault();move(true);break;
    case 'ArrowDown': case 's': case 'S': e.preventDefault();move(false);break;
    case 'ArrowLeft': case 'q': case 'Q': e.preventDefault();strafe(false);break;
    case 'ArrowRight':case 'e_strafe':    e.preventDefault();strafe(true);break;
    case 'a': case 'A': e.preventDefault();turn(false);break;
    case 'd': case 'D': e.preventDefault();turn(true);break;
    case 'e': case 'E': e.preventDefault();interact();break;
    case ' ':           e.preventDefault();
      if(getAdjacentMonster()) playerAttack(getAdjacentMonster()),endTurn();
      else if(G.map[G.py][G.px]===CELL.STAIRS) descend();
      else waitTurn();
      break;
    case 'i': case 'I': openInv();break;
    case '.': descend();break;
    case '1': useSkill(0);break;
    case '2': useSkill(1);break;
    case '3': useSkill(2);break;
    case '4': useSkill(3);break;
    case '5': useSkill(4);break;
    case 'ArrowRight': e.preventDefault();strafe(true);break;
  }
  // Fix: right arrow strafe
});

// Fix ArrowRight conflict
document.addEventListener('keydown',e=>{
  if(anyModalOpen()) return;
  if(!G||!G.map||!G.map.length||G.gameOver||G.victory) return;
  if(e.key==='ArrowRight'){e.preventDefault();strafe(true);}
},true);

// ── INIT ─────────────────────────────────────────────────
buildClassGrid();
document.getElementById('name-inp').addEventListener('keydown',e=>{
  if(e.key==='Enter') goClassSelect();
});
</script>
</body>
</html>"""


def render():
    st.markdown("""
<style>
iframe{border:none!important;}
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none;}
header{display:none!important;}
footer{display:none!important;}
</style>
""", unsafe_allow_html=True)
    components.html(GAME_HTML, height=760, scrolling=False)
