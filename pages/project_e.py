import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>⚔️ 로그라이크 던전</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700;900&family=Orbitron:wght@400;700;900&family=Black+Han+Sans&display=swap" rel="stylesheet">
<style>
:root {
  --bg:      #04070f;
  --bg2:     #070d1c;
  --bg3:     #0b1228;
  --border:  rgba(255,255,255,0.08);
  --border2: rgba(255,255,255,0.18);
  --text:    #dce8ff;
  --text2:   #6a82b4;
  --text3:   #2e3f66;
  --gold:    #ffd700;
  --green:   #39ff7a;
  --red:     #ff4560;
  --blue:    #4fc3f7;
  --purple:  #ce93d8;
  --orange:  #ffb347;
  --cyan:    #26c6da;
  --fog:     rgba(4,7,15,0.92);
  --r: 8px;
  --shadow: 0 8px 32px rgba(0,0,0,0.9);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{
  font-family:'Noto Sans KR',sans-serif;
  background:var(--bg);
  color:var(--text);
  height:100vh;width:100vw;
  overflow:hidden;
  user-select:none;
}

/* ── Layout ─────────────────────────────────── */
#app{display:flex;flex-direction:column;height:100vh;width:100vw;}
#topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:6px 14px;background:var(--bg2);
  border-bottom:1px solid var(--border2);
  font-family:'Orbitron',monospace;font-size:0.78rem;
  flex-shrink:0;
}
#topbar .title{color:var(--gold);font-weight:900;font-size:1rem;letter-spacing:2px;}
#topbar .floor-badge{
  background:rgba(255,215,0,0.12);border:1px solid rgba(255,215,0,0.3);
  color:var(--gold);padding:3px 10px;border-radius:20px;font-size:0.72rem;
}
#main{display:flex;flex:1;overflow:hidden;}

/* ── Dungeon Grid Area ───────────────────────── */
#dungeon-wrap{
  flex:1;display:flex;align-items:center;justify-content:center;
  background:var(--bg);overflow:hidden;position:relative;
}
#dungeon-canvas{
  display:grid;
  gap:1px;
  image-rendering:pixelated;
}
.cell{
  width:34px;height:34px;
  display:flex;align-items:center;justify-content:center;
  font-size:18px;line-height:1;
  border-radius:2px;
  transition:background 0.1s;
  position:relative;
}
.cell.wall{background:#0a0f1a;}
.cell.floor{background:#10192e;}
.cell.fog{background:var(--fog);color:transparent!important;}
.cell.visible{background:#10192e;}
.cell.corridor{background:#0d1525;}
.cell.stairs{background:#0d1a0f;}
.cell.shop{background:#1a100d;}
.cell.boss-room{background:#1a0d0d;}

/* ── Right Panel ─────────────────────────────── */
#panel{
  width:220px;min-width:220px;
  background:var(--bg2);
  border-left:1px solid var(--border2);
  display:flex;flex-direction:column;
  overflow:hidden;
}
#panel-stats{padding:10px 12px;border-bottom:1px solid var(--border);}
.stat-row{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:5px;font-size:0.78rem;
}
.stat-label{color:var(--text2);}
.stat-val{font-weight:700;font-family:'Orbitron',monospace;}
.bar-wrap{height:8px;background:rgba(255,255,255,0.07);border-radius:4px;overflow:hidden;margin-bottom:6px;}
.bar-fill{height:100%;border-radius:4px;transition:width 0.3s;}
.hp-bar{background:linear-gradient(90deg,#c0392b,var(--red));}
.xp-bar{background:linear-gradient(90deg,#8e44ad,var(--purple));}

#panel-minimap{
  padding:8px 12px;border-bottom:1px solid var(--border);
}
#minimap{
  width:100%;aspect-ratio:1;
  display:grid;gap:0;
  image-rendering:pixelated;margin-top:4px;
}
.mm-cell{width:100%;height:100%;}
.mm-wall{background:#07101f;}
.mm-floor{background:#1a2a45;}
.mm-player{background:var(--green);}
.mm-monster{background:var(--red);}
.mm-item{background:var(--gold);}
.mm-stairs{background:var(--cyan);}
.mm-fog{background:#05080f;}

#panel-inv{
  flex:1;overflow-y:auto;padding:8px 12px;border-bottom:1px solid var(--border);
}
#panel-inv h4{font-size:0.72rem;color:var(--text2);letter-spacing:1px;margin-bottom:6px;}
.inv-item{
  display:flex;align-items:center;gap:6px;
  padding:4px 6px;border-radius:4px;
  font-size:0.75rem;margin-bottom:3px;
  background:rgba(255,255,255,0.04);border:1px solid var(--border);
  cursor:pointer;transition:background 0.15s;
}
.inv-item:hover{background:rgba(255,255,255,0.09);}
.inv-item.equipped{border-color:var(--gold);background:rgba(255,215,0,0.07);}
.inv-item .item-icon{font-size:14px;flex-shrink:0;}
.inv-item .item-name{flex:1;color:var(--text);}
.inv-item .item-stat{color:var(--text2);font-size:0.68rem;}

#panel-log{height:130px;overflow-y:auto;padding:8px 12px;}
#panel-log h4{font-size:0.72rem;color:var(--text2);letter-spacing:1px;margin-bottom:4px;}
.log-entry{font-size:0.7rem;margin-bottom:2px;line-height:1.4;}
.log-player{color:var(--green);}
.log-monster{color:var(--red);}
.log-item{color:var(--gold);}
.log-system{color:var(--cyan);}
.log-boss{color:var(--orange);}

/* ── Bottom Controls ─────────────────────────── */
#controls{
  padding:6px 10px;background:var(--bg2);
  border-top:1px solid var(--border2);
  display:flex;align-items:center;justify-content:space-between;
  flex-shrink:0;font-size:0.7rem;color:var(--text2);
}
#controls .ctrl-keys{display:flex;gap:8px;}
.kbd{
  background:rgba(255,255,255,0.07);border:1px solid var(--border2);
  border-radius:4px;padding:2px 7px;color:var(--text);
  font-family:'Orbitron',monospace;font-size:0.65rem;
}

/* ── Overlays ────────────────────────────────── */
.overlay{
  position:fixed;inset:0;background:rgba(4,7,15,0.93);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  z-index:100;
}
.overlay.hidden{display:none;}
.overlay-box{
  background:var(--bg2);border:1px solid var(--border2);
  border-radius:var(--r);padding:32px 40px;max-width:420px;width:90%;
  text-align:center;box-shadow:var(--shadow);
}
.overlay-box h2{font-family:'Orbitron',monospace;color:var(--gold);margin-bottom:12px;}
.overlay-box p{color:var(--text2);font-size:0.88rem;line-height:1.7;margin-bottom:16px;}
.btn{
  display:inline-block;padding:10px 24px;border-radius:6px;
  font-weight:700;cursor:pointer;border:none;font-size:0.88rem;
  transition:all 0.2s;margin:4px;
}
.btn-gold{background:linear-gradient(135deg,#f5a623,var(--gold));color:#000;}
.btn-red{background:linear-gradient(135deg,#c0392b,var(--red));color:#fff;}
.btn-blue{background:linear-gradient(135deg,#1a6fa0,var(--blue));color:#fff;}
.btn-green{background:linear-gradient(135deg,#1a6b40,var(--green));color:#000;}
.btn:hover{transform:translateY(-2px);filter:brightness(1.15);}

/* ── Class Select ────────────────────────────── */
.class-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:16px;}
.class-card{
  background:rgba(255,255,255,0.04);border:2px solid var(--border);
  border-radius:8px;padding:14px 10px;cursor:pointer;transition:all 0.2s;
  text-align:left;
}
.class-card:hover,.class-card.selected{border-color:var(--gold);background:rgba(255,215,0,0.07);}
.class-card .cc-icon{font-size:2rem;display:block;margin-bottom:6px;}
.class-card .cc-name{font-weight:700;color:var(--gold);font-size:0.88rem;}
.class-card .cc-desc{color:var(--text2);font-size:0.7rem;margin-top:3px;line-height:1.5;}

/* ── Inventory Modal ─────────────────────────── */
#inv-modal .inv-grid{
  display:grid;grid-template-columns:repeat(5,1fr);gap:6px;
  max-height:260px;overflow-y:auto;margin-bottom:12px;
}
.inv-slot{
  aspect-ratio:1;background:rgba(255,255,255,0.05);border:1px solid var(--border);
  border-radius:6px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:pointer;
  font-size:1.4rem;position:relative;transition:all 0.15s;
}
.inv-slot:hover{border-color:var(--gold);background:rgba(255,215,0,0.07);}
.inv-slot.equipped-slot{border-color:var(--gold);}
.inv-slot .slot-name{font-size:0.52rem;color:var(--text2);margin-top:2px;text-align:center;line-height:1.2;}
.inv-slot .slot-badge{
  position:absolute;top:2px;right:2px;
  background:var(--gold);color:#000;
  border-radius:3px;font-size:0.52rem;padding:1px 3px;font-weight:700;
}
#item-info{
  background:rgba(255,255,255,0.04);border:1px solid var(--border);
  border-radius:6px;padding:10px 12px;min-height:60px;font-size:0.78rem;
}

/* ── Effects ─────────────────────────────────── */
@keyframes shake{
  0%,100%{transform:translate(0,0);}
  25%{transform:translate(-4px,0);}
  75%{transform:translate(4px,0);}
}
@keyframes levelup{
  0%{opacity:0;transform:scale(0.5);}
  50%{opacity:1;transform:scale(1.2);}
  100%{opacity:0;transform:scale(1.5) translateY(-30px);}
}
.shake{animation:shake 0.25s ease;}
.levelup-fx{
  position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Orbitron',monospace;font-size:2rem;font-weight:900;
  color:var(--gold);text-shadow:0 0 20px var(--gold),0 0 60px rgba(255,215,0,0.5);
  pointer-events:none;animation:levelup 1.2s ease forwards;z-index:200;
}
@keyframes dmg-pop{
  0%{opacity:1;transform:translateY(0);}
  100%{opacity:0;transform:translateY(-30px);}
}
.dmg-pop{
  position:absolute;top:-10px;left:50%;transform:translateX(-50%);
  font-size:0.75rem;font-weight:900;pointer-events:none;
  animation:dmg-pop 0.7s ease forwards;z-index:50;
  font-family:'Orbitron',monospace;
}

/* scrollbar */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:rgba(0,0,0,0.3);}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:2px;}
</style>
</head>
<body>
<div id="app">
  <!-- Topbar -->
  <div id="topbar">
    <div class="title">⚔️ ROGUELIKE DUNGEON</div>
    <div id="floor-badge" class="floor-badge">B1F</div>
    <div id="top-stats" style="display:flex;gap:16px;font-size:0.72rem;">
      <span>🏆 <span id="top-kills">0</span>킬</span>
      <span>⏱ <span id="top-turns">0</span>턴</span>
      <span>🌟 <span id="top-score">0</span>점</span>
    </div>
  </div>

  <!-- Main -->
  <div id="main">
    <!-- Dungeon -->
    <div id="dungeon-wrap">
      <div id="dungeon-canvas"></div>
    </div>

    <!-- Panel -->
    <div id="panel">
      <div id="panel-stats">
        <div style="font-size:0.7rem;color:var(--text2);margin-bottom:8px;letter-spacing:1px;">CHARACTER</div>
        <div class="stat-row">
          <span class="stat-label">이름</span>
          <span class="stat-val" id="p-name" style="color:var(--gold);font-size:0.78rem;">—</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">클래스</span>
          <span class="stat-val" id="p-class" style="color:var(--cyan);font-size:0.72rem;">—</span>
        </div>
        <div class="stat-row">
          <span class="stat-label">Lv</span>
          <span class="stat-val" id="p-level" style="color:var(--purple);">1</span>
        </div>
        <div class="stat-row"><span class="stat-label">❤️ HP</span><span class="stat-val" id="p-hp" style="color:var(--red);">30/30</span></div>
        <div class="bar-wrap"><div class="bar-fill hp-bar" id="hp-bar" style="width:100%"></div></div>
        <div class="stat-row"><span class="stat-label">⭐ XP</span><span class="stat-val" id="p-xp" style="color:var(--purple);">0/30</span></div>
        <div class="bar-wrap"><div class="bar-fill xp-bar" id="xp-bar" style="width:0%"></div></div>
        <div class="stat-row"><span class="stat-label">⚔️ ATK</span><span class="stat-val" id="p-atk" style="color:var(--orange);">5</span></div>
        <div class="stat-row"><span class="stat-label">🛡️ DEF</span><span class="stat-val" id="p-def" style="color:var(--blue);">2</span></div>
        <div class="stat-row"><span class="stat-label">💨 SPD</span><span class="stat-val" id="p-spd" style="color:var(--green);">5</span></div>
        <div class="stat-row"><span class="stat-label">💰 Gold</span><span class="stat-val" id="p-gold" style="color:var(--gold);">0</span></div>
      </div>

      <div id="panel-minimap">
        <div style="font-size:0.7rem;color:var(--text2);letter-spacing:1px;margin-bottom:4px;">MINIMAP</div>
        <div id="minimap"></div>
      </div>

      <div id="panel-inv">
        <h4>EQUIPPED</h4>
        <div id="equipped-list"><div style="font-size:0.72rem;color:var(--text3);">없음</div></div>
      </div>

      <div id="panel-log">
        <h4>BATTLE LOG</h4>
        <div id="log-entries"></div>
      </div>
    </div>
  </div>

  <!-- Controls -->
  <div id="controls">
    <div class="ctrl-keys">
      <span class="kbd">↑↓←→</span><span style="color:var(--text2)">이동/공격</span>
      <span class="kbd">Space</span><span style="color:var(--text2)">대기</span>
      <span class="kbd">I</span><span style="color:var(--text2)">인벤토리</span>
      <span class="kbd">.</span><span style="color:var(--text2)">계단이동</span>
    </div>
    <div id="ctrl-right" style="color:var(--text2);">방향키로 완전 지배</div>
  </div>
</div>

<!-- ── Overlays ── -->
<!-- Title Screen -->
<div id="title-overlay" class="overlay">
  <div class="overlay-box" style="max-width:500px;">
    <div style="font-family:'Orbitron',monospace;font-size:2.2rem;font-weight:900;color:var(--gold);margin-bottom:6px;text-shadow:0 0 20px rgba(255,215,0,0.5);">⚔️ ROGUELIKE</div>
    <div style="font-family:'Orbitron',monospace;font-size:1.2rem;color:var(--red);margin-bottom:16px;letter-spacing:4px;">DUNGEON</div>
    <p>랜덤 생성 던전을 탐험하며 몬스터를 처치하고<br>아이템을 모아 보스를 격파하세요.<br><b style="color:var(--red);">죽으면 처음부터 — 매 판이 다른 경험.</b></p>
    <div style="margin-bottom:18px;font-size:0.8rem;color:var(--text2);">
      🗺️ 10층 던전 &nbsp;|&nbsp; 👹 20종 몬스터 &nbsp;|&nbsp; 🎒 30종+ 아이템 &nbsp;|&nbsp; 🏆 보스 3종
    </div>
    <div style="margin-bottom:12px;font-size:0.8rem;color:var(--text2);">캐릭터 이름을 입력하세요</div>
    <input id="name-input" type="text" placeholder="이름 입력 (1~8자)" maxlength="8"
      style="width:100%;padding:10px;border-radius:6px;border:1px solid var(--border2);
             background:rgba(255,255,255,0.05);color:var(--text);font-size:0.9rem;
             text-align:center;margin-bottom:16px;outline:none;">
    <button class="btn btn-gold" onclick="showClassSelect()">클래스 선택 →</button>
  </div>
</div>

<!-- Class Select -->
<div id="class-overlay" class="overlay hidden">
  <div class="overlay-box" style="max-width:480px;">
    <h2>⚔️ 클래스 선택</h2>
    <p style="margin-bottom:12px;">당신의 전투 스타일을 선택하세요</p>
    <div class="class-grid" id="class-grid">
      <div class="class-card" onclick="selectClass('warrior')" id="cls-warrior">
        <span class="cc-icon">🗡️</span>
        <div class="cc-name">워리어</div>
        <div class="cc-desc">ATK+3 DEF+3 HP+20<br>근접 전투의 달인</div>
      </div>
      <div class="class-card" onclick="selectClass('mage')" id="cls-mage">
        <span class="cc-icon">🔮</span>
        <div class="cc-name">메이지</div>
        <div class="cc-desc">ATK+6 SPD+2<br>강력한 마법 공격</div>
      </div>
      <div class="class-card" onclick="selectClass('rogue')" id="cls-rogue">
        <span class="cc-icon">🗝️</span>
        <div class="cc-name">로그</div>
        <div class="cc-desc">SPD+5 ATK+2 크리티컬+<br>빠른 기습 전문가</div>
      </div>
      <div class="class-card" onclick="selectClass('paladin')" id="cls-paladin">
        <span class="cc-icon">🛡️</span>
        <div class="cc-name">팔라딘</div>
        <div class="cc-desc">DEF+6 HP+30 재생+<br>불굴의 성기사</div>
      </div>
    </div>
    <button class="btn btn-gold" id="start-btn" onclick="startGame()" disabled style="opacity:0.5;">던전 입장 ⚔️</button>
    <button class="btn btn-blue" onclick="backToTitle()">← 돌아가기</button>
  </div>
</div>

<!-- Inventory Modal -->
<div id="inv-modal" class="overlay hidden">
  <div class="overlay-box" style="max-width:420px;">
    <h2>🎒 인벤토리</h2>
    <div class="inv-grid" id="inv-grid"></div>
    <div id="item-info"><span style="color:var(--text3);">아이템을 클릭하면 정보가 표시됩니다.</span></div>
    <div style="margin-top:12px;display:flex;gap:8px;justify-content:center;">
      <button class="btn btn-gold" id="inv-use-btn" onclick="useSelectedItem()" style="display:none;">사용/장착</button>
      <button class="btn btn-red" id="inv-drop-btn" onclick="dropSelectedItem()" style="display:none;">버리기</button>
      <button class="btn btn-blue" onclick="closeInventory()">닫기 (I)</button>
    </div>
  </div>
</div>

<!-- Shop Modal -->
<div id="shop-modal" class="overlay hidden">
  <div class="overlay-box" style="max-width:400px;">
    <h2>🏪 신비의 상점</h2>
    <p style="font-size:0.78rem;">소지 골드: <span id="shop-gold" style="color:var(--gold);font-weight:700;">0</span></p>
    <div id="shop-items" style="display:grid;grid-template-columns:1fr;gap:8px;margin:12px 0;max-height:280px;overflow-y:auto;"></div>
    <button class="btn btn-blue" onclick="closeShop()">나가기</button>
  </div>
</div>

<!-- Death Screen -->
<div id="death-overlay" class="overlay hidden">
  <div class="overlay-box">
    <div style="font-size:3rem;margin-bottom:10px;">💀</div>
    <h2 style="color:var(--red);">YOU DIED</h2>
    <p id="death-msg">어둠에 잠들었습니다...</p>
    <div id="death-stats" style="background:rgba(255,255,255,0.04);border-radius:6px;padding:12px;margin-bottom:16px;font-size:0.82rem;text-align:left;"></div>
    <button class="btn btn-red" onclick="restartGame()">다시 시작 ↺</button>
  </div>
</div>

<!-- Victory Screen -->
<div id="victory-overlay" class="overlay hidden">
  <div class="overlay-box">
    <div style="font-size:3rem;margin-bottom:10px;">🏆</div>
    <h2 style="color:var(--gold);">VICTORY!</h2>
    <p>최종 보스를 처치했습니다!<br>당신은 진정한 던전 영웅입니다!</p>
    <div id="victory-stats" style="background:rgba(255,255,255,0.04);border-radius:6px;padding:12px;margin-bottom:16px;font-size:0.82rem;text-align:left;"></div>
    <button class="btn btn-gold" onclick="restartGame()">다시 플레이 ⚔️</button>
  </div>
</div>

<!-- Skill Points -->
<div id="skillpt-overlay" class="overlay hidden">
  <div class="overlay-box">
    <h2>⬆️ 레벨 업!</h2>
    <p>스탯 포인트 1개를 분배하세요</p>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0;">
      <button class="btn btn-red" onclick="allocateStat('hp')">❤️ 최대 HP +15</button>
      <button class="btn btn-orange" onclick="allocateStat('atk')" style="background:linear-gradient(135deg,#a04000,var(--orange));color:#000;">⚔️ ATK +2</button>
      <button class="btn btn-blue" onclick="allocateStat('def')">🛡️ DEF +2</button>
      <button class="btn btn-green" onclick="allocateStat('spd')">💨 SPD +1</button>
    </div>
  </div>
</div>

<script>
// ══════════════════════════════════════════════════════════
// CONSTANTS
// ══════════════════════════════════════════════════════════
const GRID_W = 25, GRID_H = 18;
const MAX_FLOOR = 10;
const CELL = { WALL:0, FLOOR:1, CORRIDOR:2, STAIRS:3, SHOP:4 };
const DIR = { ArrowUp:[0,-1], ArrowDown:[0,1], ArrowLeft:[-1,0], ArrowRight:[1,0] };

// Item definitions
const ITEM_POOL = [
  // Weapons
  {id:'sw1',name:'낡은 검',icon:'🗡️',type:'weapon',atk:3,desc:'ATK +3',rarity:'common'},
  {id:'sw2',name:'강철 검',icon:'⚔️',type:'weapon',atk:6,desc:'ATK +6',rarity:'uncommon'},
  {id:'sw3',name:'마검',icon:'🌟',type:'weapon',atk:10,desc:'ATK +10',rarity:'rare'},
  {id:'sw4',name:'전설의 검',icon:'✨',type:'weapon',atk:16,desc:'ATK +16',rarity:'legendary'},
  {id:'ax1',name:'도끼',icon:'🪓',type:'weapon',atk:5,desc:'ATK +5',rarity:'common'},
  {id:'st1',name:'지팡이',icon:'🪄',type:'weapon',atk:4,desc:'ATK +4 (마법)',rarity:'uncommon'},
  {id:'dg1',name:'단검',icon:'🔪',type:'weapon',atk:2,desc:'ATK +2 크리↑',rarity:'common'},
  // Armor
  {id:'ar1',name:'가죽 갑옷',icon:'🧥',type:'armor',def:2,desc:'DEF +2',rarity:'common'},
  {id:'ar2',name:'철 갑옷',icon:'🦺',type:'armor',def:4,desc:'DEF +4',rarity:'uncommon'},
  {id:'ar3',name:'미스릴 갑옷',icon:'🔷',type:'armor',def:7,desc:'DEF +7',rarity:'rare'},
  {id:'sh1',name:'나무 방패',icon:'🛡️',type:'shield',def:1,desc:'DEF +1',rarity:'common'},
  {id:'sh2',name:'철 방패',icon:'🔵',type:'shield',def:3,desc:'DEF +3',rarity:'uncommon'},
  // Potions
  {id:'hp1',name:'소형 포션',icon:'🧪',type:'potion',heal:20,desc:'HP +20 회복',rarity:'common'},
  {id:'hp2',name:'중형 포션',icon:'💊',type:'potion',heal:40,desc:'HP +40 회복',rarity:'uncommon'},
  {id:'hp3',name:'대형 포션',icon:'💉',type:'potion',heal:80,desc:'HP +80 회복',rarity:'rare'},
  {id:'mp1',name:'속도 포션',icon:'⚡',type:'potion',spd:3,desc:'SPD +3 (영구)',rarity:'uncommon'},
  {id:'str1',name:'힘의 물약',icon:'💪',type:'potion',atk:3,desc:'ATK +3 (영구)',rarity:'rare'},
  // Scrolls
  {id:'sc1',name:'화염 스크롤',icon:'🔥',type:'scroll',dmgAll:30,desc:'모든 적 30 피해',rarity:'uncommon'},
  {id:'sc2',name:'빙결 스크롤',icon:'❄️',type:'scroll',freeze:true,desc:'모든 적 1턴 행동 불가',rarity:'rare'},
  {id:'sc3',name:'회피 스크롤',icon:'💨',type:'scroll',dodge:true,desc:'다음 피해 회피',rarity:'rare'},
  {id:'sc4',name:'맵 스크롤',icon:'🗺️',type:'scroll',reveal:true,desc:'전체 맵 공개',rarity:'uncommon'},
  {id:'sc5',name:'저주 스크롤',icon:'💀',type:'scroll',curse:true,desc:'???',rarity:'common'},
  // Special
  {id:'ring1',name:'힘의 반지',icon:'💍',type:'ring',atk:2,def:1,desc:'ATK+2 DEF+1',rarity:'uncommon'},
  {id:'boot1',name:'질풍 장화',icon:'👟',type:'boots',spd:3,desc:'SPD +3',rarity:'uncommon'},
  {id:'helm1',name:'전사 투구',icon:'⛑️',type:'helmet',def:2,hp:10,desc:'DEF+2 HP+10',rarity:'uncommon'},
  {id:'gem1',name:'경험의 보석',icon:'💎',type:'gem',xp:50,desc:'경험치 +50',rarity:'rare'},
  {id:'key1',name:'황금 열쇠',icon:'🗝️',type:'key',desc:'비밀방 열기',rarity:'uncommon'},
  {id:'coin1',name:'금화 주머니',icon:'💰',type:'gold',gold:100,desc:'골드 +100',rarity:'common'},
  {id:'coin2',name:'보물 상자',icon:'📦',type:'gold',gold:250,desc:'골드 +250',rarity:'uncommon'},
];

const RARITY_COLOR = {common:'#dce8ff',uncommon:'#4fc3f7',rare:'#ce93d8',legendary:'#ffd700'};

// Monster definitions
const MONSTER_TYPES = [
  {id:'slime',name:'슬라임',icon:'🟢',hp:12,atk:3,def:0,xp:8,gold:5,move:'random',floor:1},
  {id:'bat',name:'박쥐',icon:'🦇',hp:8,atk:4,def:0,xp:6,gold:4,move:'chase',floor:1},
  {id:'rat',name:'거대 쥐',icon:'🐀',hp:15,atk:4,def:1,xp:10,gold:6,move:'random',floor:1},
  {id:'goblin',name:'고블린',icon:'👺',hp:20,atk:6,def:1,xp:15,gold:10,move:'chase',floor:2},
  {id:'zombie',name:'좀비',icon:'🧟',hp:30,atk:5,def:2,xp:18,gold:8,move:'chase',floor:2},
  {id:'skeleton',name:'스켈레톤',icon:'💀',hp:22,atk:8,def:2,xp:20,gold:12,move:'chase',floor:3},
  {id:'orc',name:'오크',icon:'👿',hp:40,atk:9,def:3,xp:25,gold:15,move:'chase',floor:3},
  {id:'wolf',name:'다크 울프',icon:'🐺',hp:28,atk:10,def:2,xp:22,gold:14,move:'chase',floor:4},
  {id:'ghost',name:'유령',icon:'👻',hp:20,atk:11,def:5,xp:28,gold:16,move:'phase',floor:4},
  {id:'troll',name:'트롤',icon:'🧌',hp:55,atk:12,def:4,xp:35,gold:20,move:'chase',floor:5},
  {id:'medusa',name:'메두사',icon:'🐍',hp:38,atk:14,def:3,xp:38,gold:22,move:'chase',floor:5},
  {id:'vampire',name:'흡혈귀',icon:'🧛',hp:45,atk:13,def:5,xp:40,gold:25,move:'chase',floor:6},
  {id:'golem',name:'골렘',icon:'🗿',hp:80,atk:11,def:8,xp:45,gold:28,move:'slow',floor:6},
  {id:'witch',name:'마녀',icon:'🧙',hp:40,atk:16,def:3,xp:48,gold:30,move:'ranged',floor:7},
  {id:'demon',name:'데몬',icon:'😈',hp:60,atk:17,def:6,xp:55,gold:35,move:'chase',floor:7},
  {id:'death',name:'저승사자',icon:'⚰️',hp:50,atk:20,def:7,xp:60,gold:40,move:'chase',floor:8},
  {id:'dragon_young',name:'어린 드래곤',icon:'🐉',hp:90,atk:18,def:8,xp:70,gold:50,move:'chase',floor:8},
  {id:'lich',name:'리치',icon:'🕯️',hp:70,atk:22,def:9,xp:80,gold:55,move:'ranged',floor:9},
  {id:'titan',name:'타이탄',icon:'⚡',hp:120,atk:20,def:12,xp:90,gold:60,move:'slow',floor:9},
  // Bosses
  {id:'boss_b3',name:'지하의 군주',icon:'👁️',hp:150,atk:20,def:8,xp:150,gold:200,move:'boss',floor:3,boss:true},
  {id:'boss_b6',name:'암흑 드래곤',icon:'🐲',hp:250,atk:28,def:12,xp:300,gold:400,move:'boss',floor:6,boss:true},
  {id:'boss_b10',name:'지옥의 신',icon:'👿',hp:400,atk:38,def:18,xp:500,gold:800,move:'boss',floor:10,boss:true},
];

const CLASS_DEF = {
  warrior:{name:'🗡️ 워리어',hp:50,atk:8,def:5,spd:5,crit:5},
  mage:   {name:'🔮 메이지', hp:30,atk:14,def:2,spd:7,crit:10},
  rogue:  {name:'🗝️ 로그',   hp:35,atk:10,def:3,spd:10,crit:20},
  paladin:{name:'🛡️ 팔라딘', hp:60,atk:7,def:8,spd:4,crit:5},
};

const SHOP_ITEMS_POOL = ITEM_POOL.filter(i=>['potion','scroll','weapon','armor'].includes(i.type));

// ══════════════════════════════════════════════════════════
// GAME STATE
// ══════════════════════════════════════════════════════════
let G = {}; // main game state
let selectedClass = null;
let selectedInvItem = null;

function initState(name, cls) {
  const cd = CLASS_DEF[cls];
  G = {
    name, cls, className: cd.name,
    floor: 1,
    hp: cd.hp, maxHp: cd.hp,
    atk: cd.atk, def: cd.def, spd: cd.spd, crit: cd.crit,
    xp: 0, level: 1, xpNext: 30,
    gold: 50,
    kills: 0, turns: 0, score: 0,
    inventory: [],
    equipped: { weapon:null, armor:null, shield:null, ring:null, boots:null, helmet:null },
    dodge: false, frozen: false,
    map: [], monsters: [], items: [],
    player: {x:0,y:0},
    revealed: [],
    visible: [],
    shopOpen: false,
    shopStock: [],
    gameOver: false,
    victory: false,
  };
}

// ══════════════════════════════════════════════════════════
// MAP GENERATION (BSP rooms)
// ══════════════════════════════════════════════════════════
function makeMap() {
  const map = Array.from({length:GRID_H}, ()=>Array(GRID_W).fill(CELL.WALL));
  const rooms = [];

  function carveRoom(x,y,w,h) {
    for(let ry=y;ry<y+h;ry++)
      for(let rx=x;rx<x+w;rx++)
        map[ry][rx] = CELL.FLOOR;
    rooms.push({x,y,w,h,cx:Math.floor(x+w/2),cy:Math.floor(y+h/2)});
  }
  function corridor(ax,ay,bx,by) {
    let x=ax,y=ay;
    if(Math.random()<0.5){
      while(x!==bx){map[y][x]=CELL.CORRIDOR;x+=x<bx?1:-1;}
      while(y!==by){map[y][x]=CELL.CORRIDOR;y+=y<by?1:-1;}
    } else {
      while(y!==by){map[y][x]=CELL.CORRIDOR;y+=y<by?1:-1;}
      while(x!==bx){map[y][x]=CELL.CORRIDOR;x+=x<bx?1:-1;}
    }
  }

  // Generate 6-9 rooms
  const numRooms = 6 + Math.floor(Math.random()*4);
  let attempts = 0;
  while(rooms.length < numRooms && attempts < 200) {
    attempts++;
    const rw = 3+Math.floor(Math.random()*5);
    const rh = 3+Math.floor(Math.random()*4);
    const rx = 1+Math.floor(Math.random()*(GRID_W-rw-2));
    const ry = 1+Math.floor(Math.random()*(GRID_H-rh-2));
    const overlap = rooms.some(r=>
      rx<r.x+r.w+1 && rx+rw>r.x-1 && ry<r.y+r.h+1 && ry+rh>r.y-1
    );
    if(!overlap) carveRoom(rx,ry,rw,rh);
  }

  // Connect rooms
  for(let i=1;i<rooms.length;i++)
    corridor(rooms[i-1].cx,rooms[i-1].cy,rooms[i].cx,rooms[i].cy);

  // Place player in first room
  G.player = {x:rooms[0].cx, y:rooms[0].cy};

  // Place stairs in last room
  const stairRoom = rooms[rooms.length-1];
  map[stairRoom.cy][stairRoom.cx] = CELL.STAIRS;

  // Place shop in middle room
  if(rooms.length>3) {
    const shopRoom = rooms[Math.floor(rooms.length/2)];
    map[shopRoom.cy][shopRoom.cx] = CELL.SHOP;
  }

  G.map = map;
  G.rooms = rooms;
  G.revealed = Array.from({length:GRID_H},()=>Array(GRID_W).fill(false));
  G.visible = Array.from({length:GRID_H},()=>Array(GRID_W).fill(false));

  // Spawn monsters
  G.monsters = [];
  const floor = G.floor;
  const eligible = MONSTER_TYPES.filter(m=>m.floor<=floor && !m.boss);
  const boss = MONSTER_TYPES.find(m=>m.boss && m.floor===floor);

  // Monsters per room (skip first room)
  for(let i=1;i<rooms.length;i++) {
    const r = rooms[i];
    const count = 1 + Math.floor(Math.random()*3);
    for(let k=0;k<count;k++) {
      const mt = eligible[Math.floor(Math.random()*eligible.length)];
      if(!mt) continue;
      const scale = 1 + (floor-1)*0.15;
      G.monsters.push({
        ...mt,
        id: mt.id+'_'+Date.now()+'_'+Math.random(),
        hp: Math.round(mt.hp*scale),
        maxHp: Math.round(mt.hp*scale),
        atk: Math.round(mt.atk*scale),
        x: r.x+1+Math.floor(Math.random()*(r.w-2)),
        y: r.y+1+Math.floor(Math.random()*(r.h-2)),
        frozen: false,
      });
    }
  }

  // Boss in last room
  if(boss && rooms.length>1) {
    const br = rooms[rooms.length-1];
    const scale = 1 + (floor-1)*0.1;
    G.monsters.push({
      ...boss,
      id: boss.id+'_boss',
      hp: Math.round(boss.hp*scale),
      maxHp: Math.round(boss.hp*scale),
      atk: Math.round(boss.atk*scale),
      x: br.cx, y: br.cy,
      frozen: false,
    });
  }

  // Spawn items
  G.items = [];
  for(let i=1;i<rooms.length;i++) {
    if(Math.random()<0.6) {
      const r = rooms[i];
      const pool = ITEM_POOL.filter(it=>it.id!=='sc5');
      const item = pool[Math.floor(Math.random()*pool.length)];
      G.items.push({
        ...item, iid: item.id+'_'+Date.now()+'_'+Math.random(),
        x: r.x+Math.floor(r.w/2), y: r.y+Math.floor(r.h/2),
      });
    }
  }

  updateFOV();
}

// ══════════════════════════════════════════════════════════
// FOV (simple line-of-sight radius)
// ══════════════════════════════════════════════════════════
function updateFOV() {
  G.visible = Array.from({length:GRID_H},()=>Array(GRID_W).fill(false));
  const radius = 5;
  const {x,y} = G.player;
  for(let dy=-radius;dy<=radius;dy++) {
    for(let dx=-radius;dx<=radius;dx++) {
      if(dx*dx+dy*dy>radius*radius) continue;
      const nx=x+dx, ny=y+dy;
      if(nx<0||ny<0||nx>=GRID_W||ny>=GRID_H) continue;
      if(hasLOS(x,y,nx,ny)) {
        G.visible[ny][nx]=true;
        G.revealed[ny][nx]=true;
      }
    }
  }
}

function hasLOS(x0,y0,x1,y1) {
  let dx=Math.abs(x1-x0),dy=Math.abs(y1-y0);
  let sx=x0<x1?1:-1,sy=y0<y1?1:-1;
  let err=dx-dy, x=x0,y=y0;
  while(true) {
    if(x===x1&&y===y1) return true;
    if(G.map[y][x]===CELL.WALL) return false;
    let e2=2*err;
    if(e2>-dy){err-=dy;x+=sx;}
    if(e2<dx){err+=dx;y+=sy;}
  }
}

// ══════════════════════════════════════════════════════════
// RENDERING
// ══════════════════════════════════════════════════════════
function render() {
  const canvas = document.getElementById('dungeon-canvas');
  canvas.style.gridTemplateColumns = `repeat(${GRID_W},34px)`;
  canvas.style.gridTemplateRows    = `repeat(${GRID_H},34px)`;

  const playerPos = G.player;

  // Build cell data
  const cells = [];
  for(let y=0;y<GRID_H;y++) {
    for(let x=0;x<GRID_W;x++) {
      const vis = G.visible[y][x];
      const rev = G.revealed[y][x];
      const ct  = G.map[y][x];

      let classes = 'cell';
      let content = '';

      if(!rev) { classes+=' fog'; cells.push({classes,content}); continue; }

      if(ct===CELL.WALL) classes+=' wall';
      else if(ct===CELL.STAIRS) { classes+=' stairs'; if(vis) content='🪜'; }
      else if(ct===CELL.SHOP)   { classes+=' shop';   if(vis) content='🏪'; }
      else classes+=' floor';

      if(!vis) { cells.push({classes,content:'',extra:'opacity:0.35'}); continue; }

      // Player
      if(playerPos.x===x && playerPos.y===y) {
        content = ['🗡️','🔮','🗝️','🛡️'][['warrior','mage','rogue','paladin'].indexOf(G.cls)] || '🧙';
      }

      // Monster
      const mon = G.monsters.find(m=>m.x===x&&m.y===y);
      if(mon) content = mon.frozen ? '🧊' : mon.icon;

      // Item
      if(!mon && !(playerPos.x===x&&playerPos.y===y)) {
        const itm = G.items.find(i=>i.x===x&&i.y===y);
        if(itm) content = itm.icon;
      }

      cells.push({classes, content});
    }
  }

  // Render diff
  const existing = canvas.children;
  if(existing.length !== GRID_W*GRID_H) {
    canvas.innerHTML = '';
    cells.forEach(c=>{
      const div = document.createElement('div');
      div.className = c.classes;
      div.textContent = c.content;
      if(c.extra) div.style.cssText = c.extra;
      canvas.appendChild(div);
    });
  } else {
    cells.forEach((c,i)=>{
      const div = existing[i];
      if(div.className!==c.classes) div.className=c.classes;
      if(div.textContent!==c.content) div.textContent=c.content;
    });
  }

  renderPanel();
  renderMinimap();
}

function renderPanel() {
  document.getElementById('p-name').textContent  = G.name;
  document.getElementById('p-class').textContent = G.className;
  document.getElementById('p-level').textContent = G.level;
  document.getElementById('p-hp').textContent    = `${G.hp}/${G.maxHp}`;
  document.getElementById('p-xp').textContent    = `${G.xp}/${G.xpNext}`;
  document.getElementById('p-atk').textContent   = getTotalAtk();
  document.getElementById('p-def').textContent   = getTotalDef();
  document.getElementById('p-spd').textContent   = G.spd;
  document.getElementById('p-gold').textContent  = G.gold;
  document.getElementById('floor-badge').textContent = `B${G.floor}F`;
  document.getElementById('top-kills').textContent = G.kills;
  document.getElementById('top-turns').textContent = G.turns;
  document.getElementById('top-score').textContent = G.score;

  const hpPct = Math.max(0,(G.hp/G.maxHp)*100);
  document.getElementById('hp-bar').style.width = hpPct+'%';
  const xpPct = Math.max(0,(G.xp/G.xpNext)*100);
  document.getElementById('xp-bar').style.width = xpPct+'%';

  // Equipped
  const eq = G.equipped;
  let ehtml = '';
  for(const [slot,item] of Object.entries(eq)) {
    if(item) ehtml+=`<div class="inv-item equipped"><span class="item-icon">${item.icon}</span><span class="item-name">${item.name}</span><span class="item-stat">${item.desc}</span></div>`;
  }
  document.getElementById('equipped-list').innerHTML = ehtml || '<div style="font-size:0.72rem;color:var(--text3);">없음</div>';
}

function renderMinimap() {
  const mm = document.getElementById('minimap');
  const s = Math.floor(140/GRID_W);
  mm.style.gridTemplateColumns = `repeat(${GRID_W},${s}px)`;
  mm.style.gridTemplateRows    = `repeat(${GRID_H},${s}px)`;

  const cells = [];
  for(let y=0;y<GRID_H;y++) {
    for(let x=0;x<GRID_W;x++) {
      let cls = 'mm-cell ';
      if(!G.revealed[y][x]) { cls+='mm-fog'; }
      else if(G.player.x===x&&G.player.y===y) cls+='mm-player';
      else if(G.monsters.some(m=>m.x===x&&m.y===y&&G.visible[y][x])) cls+='mm-monster';
      else if(G.items.some(i=>i.x===x&&i.y===y&&G.visible[y][x])) cls+='mm-item';
      else if(G.map[y][x]===CELL.STAIRS) cls+='mm-stairs';
      else if(G.map[y][x]===CELL.WALL) cls+='mm-wall';
      else cls+='mm-floor';
      cells.push(cls);
    }
  }

  if(mm.children.length!==GRID_W*GRID_H) {
    mm.innerHTML = cells.map(c=>`<div class="${c}"></div>`).join('');
  } else {
    Array.from(mm.children).forEach((d,i)=>{ if(d.className!==cells[i]) d.className=cells[i]; });
  }
}

// ══════════════════════════════════════════════════════════
// COMBAT
// ══════════════════════════════════════════════════════════
function getTotalAtk() {
  let a = G.atk;
  for(const item of Object.values(G.equipped)) if(item?.atk) a+=item.atk;
  return a;
}
function getTotalDef() {
  let d = G.def;
  for(const item of Object.values(G.equipped)) if(item?.def) d+=item.def;
  return d;
}

function playerAttack(mon) {
  let dmg = Math.max(1, getTotalAtk() - mon.def + Math.floor(Math.random()*4)-1);
  const isCrit = Math.random()*100 < G.crit;
  if(isCrit) { dmg = Math.round(dmg*1.7); }
  if(G.dodge) { G.dodge=false; addLog('💨 다음 피해를 회피합니다!','system'); }
  mon.hp -= dmg;
  const critTxt = isCrit ? ' ⚡크리티컬!' : '';
  addLog(`⚔️ ${mon.name}에게 ${dmg} 피해!${critTxt}`, 'player');
  showDmgPop(dmg, isCrit ? '#ffd700' : '#ff4560');
  shakeScreen();
  if(mon.hp <= 0) killMonster(mon);
}

function monsterAttack(mon) {
  if(mon.frozen) { mon.frozen=false; addLog(`🧊 ${mon.name}은 얼어있어 행동 불가!`,'system'); return; }
  let dmg = Math.max(0, mon.atk - getTotalDef() + Math.floor(Math.random()*3)-1);
  if(G.dodge) { G.dodge=false; addLog(`💨 ${mon.name}의 공격을 회피!`,'player'); return; }
  G.hp = Math.max(0, G.hp - dmg);
  // Paladin regen
  if(G.cls==='paladin' && G.turns%5===0 && G.hp<G.maxHp) {
    G.hp = Math.min(G.maxHp, G.hp+3);
    addLog('🛡️ 팔라딘 재생: HP+3','system');
  }
  addLog(`👹 ${mon.name}이 ${dmg} 피해!`, 'monster');
  if(G.hp <= 0) gameDie(mon.name);
}

function killMonster(mon) {
  G.kills++;
  G.xp += mon.xp;
  G.gold += mon.gold;
  G.score += mon.xp * G.floor;
  addLog(`💀 ${mon.name} 처치! XP+${mon.xp} Gold+${mon.gold}`, mon.boss?'boss':'player');

  // Drop item chance
  if(Math.random()<0.3) {
    const pool = ITEM_POOL.filter(i=>i.type!=='gold');
    const drop = pool[Math.floor(Math.random()*pool.length)];
    G.items.push({...drop, iid:drop.id+'_'+Date.now(), x:mon.x, y:mon.y});
    addLog(`📦 아이템 드롭: ${drop.icon}${drop.name}`, 'item');
  }

  G.monsters = G.monsters.filter(m=>m.id!==mon.id);

  // Check XP
  while(G.xp >= G.xpNext) levelUp();

  // Boss victory
  if(mon.boss && G.floor===MAX_FLOOR) { gameVictory(); return; }
  if(mon.boss && G.floor===3)  addLog('🌟 B3F 보스 처치!','boss');
  if(mon.boss && G.floor===6)  addLog('🌟 B6F 보스 처치!','boss');
}

function levelUp() {
  G.level++;
  G.xp -= G.xpNext;
  G.xpNext = Math.floor(G.xpNext * 1.5);
  addLog(`⬆️ 레벨 업! Lv${G.level}`, 'system');
  showLevelUpFX();
  document.getElementById('skillpt-overlay').classList.remove('hidden');
}

// ══════════════════════════════════════════════════════════
// MOVEMENT & TURN
// ══════════════════════════════════════════════════════════
function tryMove(dx, dy) {
  if(G.gameOver || G.victory) return;
  const nx = G.player.x + dx;
  const ny = G.player.y + dy;
  if(nx<0||ny<0||nx>=GRID_W||ny>=GRID_H) return;
  const ct = G.map[ny][nx];
  if(ct===CELL.WALL) return;

  // Check monster at target
  const mon = G.monsters.find(m=>m.x===nx&&m.y===ny);
  if(mon) {
    playerAttack(mon);
    endTurn();
    return;
  }

  // Move
  G.player = {x:nx,y:ny};
  endTurn();

  // Check cell events
  const cell = G.map[ny][nx];
  if(cell===CELL.STAIRS) {
    addLog(`🪜 B${G.floor}F 계단 발견! Space로 내려가기`, 'system');
  }
  if(cell===CELL.SHOP) {
    openShop();
    return;
  }

  // Pick up item
  const itemIdx = G.items.findIndex(i=>i.x===nx&&i.y===ny);
  if(itemIdx>-1) {
    const item = G.items[itemIdx];
    if(G.inventory.length<20) {
      G.inventory.push(item);
      G.items.splice(itemIdx,1);
      addLog(`🎒 ${item.icon}${item.name} 획득!`, 'item');
    } else {
      addLog('🎒 인벤토리 가득! 아이템을 버려야 합니다.','system');
    }
  }
}

function endTurn() {
  G.turns++;
  updateFOV();
  monsterTurn();
  render();
}

function monsterTurn() {
  for(const mon of G.monsters) {
    if(!G.visible[mon.y]?.[mon.x]) continue; // only active if visible
    if(mon.frozen) { mon.frozen=false; continue; }

    const pdx = G.player.x - mon.x;
    const pdy = G.player.y - mon.y;
    const dist = Math.abs(pdx)+Math.abs(pdy);

    if(dist===1) { monsterAttack(mon); continue; }
    if(G.hp<=0) return;

    // Move toward player
    let mx=0,my=0;
    if(mon.move==='random') {
      const dirs=[[0,1],[0,-1],[1,0],[-1,0]];
      const d=dirs[Math.floor(Math.random()*4)];
      mx=d[0];my=d[1];
    } else if(mon.move==='slow') {
      if(G.turns%2===0) { mx=Math.sign(pdx); my=0; if(!mx) my=Math.sign(pdy); }
    } else if(mon.move==='ranged') {
      if(dist<=4) { monsterAttack(mon); continue; }
      mx=Math.sign(pdx); my=0; if(!mx) my=Math.sign(pdy);
    } else {
      mx=Math.sign(pdx); my=0; if(!mx) my=Math.sign(pdy);
    }

    const nx=mon.x+mx,ny=mon.y+my;
    if(nx>=0&&ny>=0&&nx<GRID_W&&ny<GRID_H) {
      const ct=G.map[ny][nx];
      if(ct!==CELL.WALL && !G.monsters.some(m=>m.x===nx&&m.y===ny)) {
        mon.x=nx; mon.y=ny;
      }
    }
  }
}

function waitTurn() {
  if(G.gameOver||G.victory) return;
  // Heal slightly if paladin
  if(G.cls==='paladin') G.hp=Math.min(G.maxHp,G.hp+2);
  addLog('⏳ 1턴 대기...','system');
  endTurn();
}

function goStairs() {
  if(G.map[G.player.y][G.player.x]===CELL.STAIRS || 
     G.items.length===0) { // Auto-navigate if on stairs
    if(G.map[G.player.y][G.player.x]!==CELL.STAIRS) {
      // Find nearest stairs
      let best=null,bd=9999;
      for(let y=0;y<GRID_H;y++)
        for(let x=0;x<GRID_W;x++)
          if(G.map[y][x]===CELL.STAIRS){
            const d=Math.abs(x-G.player.x)+Math.abs(y-G.player.y);
            if(d<bd){bd=d;best={x,y};}
          }
      if(best) addLog(`🪜 계단 위치: (${best.x},${best.y})에서 찾았습니다.`,'system');
      return;
    }
    descend();
  }
}

function descend() {
  if(G.floor >= MAX_FLOOR) { gameDie('더 이상 내려갈 수 없습니다.'); return; }
  G.floor++;
  addLog(`🪜 B${G.floor}F으로 내려갑니다!`, 'system');
  // Heal 30% on descent
  G.hp = Math.min(G.maxHp, G.hp + Math.floor(G.maxHp*0.3));
  makeMap();
  render();
}

// ══════════════════════════════════════════════════════════
// ITEMS
// ══════════════════════════════════════════════════════════
function useItem(item) {
  if(item.type==='potion') {
    if(item.heal) {
      G.hp = Math.min(G.maxHp, G.hp+item.heal);
      addLog(`🧪 ${item.name} 사용! HP+${item.heal}`,'item');
    }
    if(item.atk) { G.atk+=item.atk; addLog(`💪 ATK+${item.atk}`,'item'); }
    if(item.spd) { G.spd+=item.spd; addLog(`⚡ SPD+${item.spd}`,'item'); }
    removeFromInventory(item.iid);
  } else if(['weapon','armor','shield','ring','boots','helmet'].includes(item.type)) {
    if(G.equipped[item.type]) G.inventory.push(G.equipped[item.type]);
    G.equipped[item.type] = item;
    removeFromInventory(item.iid);
    addLog(`⚔️ ${item.name} 장착!`,'item');
  } else if(item.type==='scroll') {
    useScroll(item);
    removeFromInventory(item.iid);
  } else if(item.type==='gem') {
    G.xp += item.xp;
    addLog(`💎 경험치+${item.xp}`,'item');
    while(G.xp>=G.xpNext) levelUp();
    removeFromInventory(item.iid);
  } else if(item.type==='gold') {
    G.gold += item.gold;
    addLog(`💰 골드+${item.gold}`,'item');
    removeFromInventory(item.iid);
  }
  render();
}

function useScroll(item) {
  if(item.dmgAll) {
    G.monsters.forEach(m=>{ m.hp-=item.dmgAll; addLog(`🔥 ${m.name}에게 ${item.dmgAll} 피해!`,'boss'); });
    G.monsters = G.monsters.filter(m=>{ if(m.hp<=0){ killMonster(m); return false; } return true; });
  }
  if(item.freeze) { G.monsters.forEach(m=>m.frozen=true); addLog('❄️ 모든 적 빙결!','system'); }
  if(item.dodge)  { G.dodge=true; addLog('💨 회피 준비 완료!','system'); }
  if(item.reveal) {
    G.revealed = G.revealed.map(row=>row.map(()=>true));
    addLog('🗺️ 전체 맵 공개!','system');
  }
  if(item.curse)  { G.hp = Math.floor(G.hp/2); addLog('💀 저주! HP 반감...','monster'); }
  if(G.hp<=0) gameDie('저주 스크롤');
}

function removeFromInventory(iid) {
  G.inventory = G.inventory.filter(i=>i.iid!==iid);
}

// ══════════════════════════════════════════════════════════
// SHOP
// ══════════════════════════════════════════════════════════
function openShop() {
  // Generate 4 random shop items
  const shuffled = [...SHOP_ITEMS_POOL].sort(()=>Math.random()-0.5);
  G.shopStock = shuffled.slice(0,4).map(i=>({
    ...i,
    iid:i.id+'_shop_'+Date.now(),
    price: Math.round(50 + Math.random()*150 + G.floor*20)
  }));
  document.getElementById('shop-gold').textContent = G.gold;
  const si = document.getElementById('shop-items');
  si.innerHTML = G.shopStock.map(item=>`
    <div style="display:flex;align-items:center;gap:10px;background:rgba(255,255,255,0.04);
      border:1px solid var(--border);border-radius:6px;padding:8px 12px;cursor:pointer;"
      onclick="buyShopItem('${item.iid}')">
      <span style="font-size:1.4rem;">${item.icon}</span>
      <div style="flex:1;">
        <div style="font-weight:700;color:${RARITY_COLOR[item.rarity]};">${item.name}</div>
        <div style="font-size:0.72rem;color:var(--text2);">${item.desc}</div>
      </div>
      <div style="color:var(--gold);font-weight:700;">💰${item.price}</div>
    </div>
  `).join('');
  document.getElementById('shop-modal').classList.remove('hidden');
}

function buyShopItem(iid) {
  const item = G.shopStock.find(i=>i.iid===iid);
  if(!item) return;
  if(G.gold<item.price) { addLog('💰 골드 부족!','system'); return; }
  if(G.inventory.length>=20) { addLog('🎒 인벤토리 가득!','system'); return; }
  G.gold -= item.price;
  G.inventory.push(item);
  G.shopStock = G.shopStock.filter(i=>i.iid!==iid);
  addLog(`🛒 ${item.name} 구매!`,'item');
  document.getElementById('shop-gold').textContent = G.gold;
  openShop();
  render();
}

function closeShop() {
  document.getElementById('shop-modal').classList.add('hidden');
}

// ══════════════════════════════════════════════════════════
// INVENTORY UI
// ══════════════════════════════════════════════════════════
function openInventory() {
  selectedInvItem = null;
  renderInventoryUI();
  document.getElementById('inv-modal').classList.remove('hidden');
}

function renderInventoryUI() {
  const grid = document.getElementById('inv-grid');
  const slots = 20;
  let html='';
  for(let i=0;i<slots;i++) {
    const item = G.inventory[i];
    if(item) {
      const eq = Object.values(G.equipped).some(e=>e?.iid===item.iid);
      html+=`<div class="inv-slot${eq?' equipped-slot':''}" onclick="selectInvItem('${item.iid}')"
        title="${item.name}">
        ${item.icon}
        <div class="slot-name">${item.name}</div>
        ${eq?'<div class="slot-badge">E</div>':''}
      </div>`;
    } else {
      html+=`<div class="inv-slot" style="opacity:0.3;cursor:default;"></div>`;
    }
  }
  grid.innerHTML = html;
}

function selectInvItem(iid) {
  selectedInvItem = G.inventory.find(i=>i.iid===iid);
  if(!selectedInvItem) return;
  const rc = RARITY_COLOR[selectedInvItem.rarity]||'#dce8ff';
  document.getElementById('item-info').innerHTML = `
    <span style="font-size:1.5rem;">${selectedInvItem.icon}</span>
    <span style="font-weight:700;color:${rc};margin-left:6px;">${selectedInvItem.name}</span>
    <span style="margin-left:6px;font-size:0.7rem;color:${rc};">[${selectedInvItem.rarity||''}]</span>
    <div style="color:var(--text2);font-size:0.78rem;margin-top:4px;">${selectedInvItem.desc}</div>
  `;
  document.getElementById('inv-use-btn').style.display='inline-block';
  document.getElementById('inv-drop-btn').style.display='inline-block';
}

function useSelectedItem() {
  if(!selectedInvItem) return;
  closeInventory();
  useItem(selectedInvItem);
}

function dropSelectedItem() {
  if(!selectedInvItem) return;
  addLog(`🗑️ ${selectedInvItem.name} 버림`,'system');
  removeFromInventory(selectedInvItem.iid);
  selectedInvItem=null;
  renderInventoryUI();
  document.getElementById('item-info').innerHTML='<span style="color:var(--text3);">아이템을 클릭하면 정보가 표시됩니다.</span>';
  document.getElementById('inv-use-btn').style.display='none';
  document.getElementById('inv-drop-btn').style.display='none';
  render();
}

function closeInventory() {
  document.getElementById('inv-modal').classList.add('hidden');
}

// ══════════════════════════════════════════════════════════
// LEVEL UP
// ══════════════════════════════════════════════════════════
function allocateStat(stat) {
  if(stat==='hp')  { G.maxHp+=15; G.hp=Math.min(G.maxHp,G.hp+15); }
  if(stat==='atk') G.atk+=2;
  if(stat==='def') G.def+=2;
  if(stat==='spd') G.spd+=1;
  document.getElementById('skillpt-overlay').classList.add('hidden');
  render();
}

// ══════════════════════════════════════════════════════════
// GAME OVER / VICTORY
// ══════════════════════════════════════════════════════════
function gameDie(cause) {
  G.gameOver=true;
  G.hp=0;
  const stats = buildStats();
  document.getElementById('death-msg').textContent = `${cause}에 의해 사망...`;
  document.getElementById('death-stats').innerHTML = stats;
  document.getElementById('death-overlay').classList.remove('hidden');
}

function gameVictory() {
  G.victory=true;
  G.score += 10000;
  const stats = buildStats();
  document.getElementById('victory-stats').innerHTML = stats;
  document.getElementById('victory-overlay').classList.remove('hidden');
}

function buildStats() {
  return `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
      <div>📊 최종 레벨: <b>${G.level}</b></div>
      <div>🏆 최대 층수: <b>B${G.floor}F</b></div>
      <div>💀 처치 수: <b>${G.kills}</b></div>
      <div>⏱ 소요 턴: <b>${G.turns}</b></div>
      <div>💰 보유 골드: <b>${G.gold}</b></div>
      <div>🌟 최종 점수: <b>${G.score}</b></div>
    </div>
  `;
}

function restartGame() {
  document.getElementById('death-overlay').classList.add('hidden');
  document.getElementById('victory-overlay').classList.add('hidden');
  document.getElementById('title-overlay').classList.remove('hidden');
  document.getElementById('dungeon-canvas').innerHTML='';
  document.getElementById('log-entries').innerHTML='';
}

// ══════════════════════════════════════════════════════════
// LOG
// ══════════════════════════════════════════════════════════
const MAX_LOG = 80;
function addLog(msg, type='system') {
  const el = document.getElementById('log-entries');
  const div = document.createElement('div');
  div.className = `log-entry log-${type}`;
  div.textContent = msg;
  el.insertBefore(div, el.firstChild);
  while(el.children.length>MAX_LOG) el.removeChild(el.lastChild);
}

// ══════════════════════════════════════════════════════════
// EFFECTS
// ══════════════════════════════════════════════════════════
function shakeScreen() {
  const dw = document.getElementById('dungeon-wrap');
  dw.classList.add('shake');
  setTimeout(()=>dw.classList.remove('shake'),300);
}

function showDmgPop(dmg, color='#ff4560') {
  const dw = document.getElementById('dungeon-wrap');
  const pop = document.createElement('div');
  pop.className='dmg-pop';
  pop.style.color=color;
  pop.textContent=`-${dmg}`;
  pop.style.top=Math.random()*40+30+'%';
  pop.style.left=Math.random()*30+35+'%';
  dw.appendChild(pop);
  setTimeout(()=>pop.remove(),750);
}

function showLevelUpFX() {
  const el = document.createElement('div');
  el.className='levelup-fx';
  el.textContent='⬆️ LEVEL UP!';
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),1300);
}

// ══════════════════════════════════════════════════════════
// UI FLOW
// ══════════════════════════════════════════════════════════
function showClassSelect() {
  const nameInput = document.getElementById('name-input').value.trim();
  if(!nameInput) { alert('이름을 입력하세요!'); return; }
  document.getElementById('title-overlay').classList.add('hidden');
  document.getElementById('class-overlay').classList.remove('hidden');
}

function selectClass(cls) {
  selectedClass=cls;
  document.querySelectorAll('.class-card').forEach(c=>c.classList.remove('selected'));
  document.getElementById('cls-'+cls).classList.add('selected');
  const btn=document.getElementById('start-btn');
  btn.disabled=false; btn.style.opacity='1';
}

function backToTitle() {
  document.getElementById('class-overlay').classList.add('hidden');
  document.getElementById('title-overlay').classList.remove('hidden');
}

function startGame() {
  if(!selectedClass) return;
  const name=document.getElementById('name-input').value.trim()||'용사';
  document.getElementById('class-overlay').classList.add('hidden');
  initState(name, selectedClass);
  makeMap();
  addLog(`⚔️ ${name}이(가) 던전에 입장했습니다!`,'system');
  addLog(`🎮 방향키로 이동, 몬스터에 인접하면 자동 공격!`,'system');
  render();
}

// ══════════════════════════════════════════════════════════
// KEYBOARD INPUT
// ══════════════════════════════════════════════════════════
document.addEventListener('keydown', e=>{
  if(G.gameOver||G.victory) return;
  if(!G.map || !G.map.length) return;

  // Block if any modal open
  const modals=['inv-modal','shop-modal','skillpt-overlay'];
  if(modals.some(id=>!document.getElementById(id).classList.contains('hidden'))) {
    if(e.key==='i'||e.key==='I'||e.key==='Escape') closeInventory();
    return;
  }

  if(DIR[e.key]) {
    e.preventDefault();
    const [dx,dy]=DIR[e.key];
    tryMove(dx,dy);
  } else if(e.key===' ') {
    e.preventDefault();
    if(G.map[G.player.y][G.player.x]===CELL.STAIRS) descend();
    else waitTurn();
  } else if(e.key==='i'||e.key==='I') {
    openInventory();
  } else if(e.key==='.') {
    goStairs();
  }
});

// ══════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════
document.getElementById('name-input').addEventListener('keydown', e=>{
  if(e.key==='Enter') showClassSelect();
});
</script>
</body>
</html>"""


def render():
    st.markdown("""
<style>
iframe { border: none !important; }
.block-container { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

    components.html(GAME_HTML, height=700, scrolling=False)
