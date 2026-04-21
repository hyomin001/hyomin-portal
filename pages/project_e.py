import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>던전 파이터</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0a12;font-family:'Noto Sans KR',sans-serif;overflow:hidden;width:100vw;height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;}

#gameWrapper{position:relative;width:900px;height:580px;}

/* HUD */
#hud{
  position:absolute;top:0;left:0;right:0;height:56px;
  background:linear-gradient(180deg,rgba(0,0,0,0.95) 0%,rgba(0,0,0,0.7) 100%);
  border-bottom:2px solid #ff6600;
  display:flex;align-items:center;gap:16px;padding:0 16px;z-index:100;
}
.hud-name{font-family:'Black Han Sans',sans-serif;font-size:1rem;color:#ffcc00;letter-spacing:2px;}
.bar-wrap{display:flex;flex-direction:column;gap:3px;}
.bar-label{font-size:0.55rem;color:#aaa;letter-spacing:1px;}
.bar-bg{width:160px;height:12px;background:rgba(255,255,255,0.08);border-radius:2px;border:1px solid rgba(255,255,255,0.1);overflow:hidden;}
.bar-fill{height:100%;border-radius:2px;transition:width 0.15s;}
#hp-bar{background:linear-gradient(90deg,#8b0000,#ff2222,#ff6666);}
#mp-bar{background:linear-gradient(90deg,#001a6b,#1144ff,#44aaff);}
.hud-stats{display:flex;gap:10px;margin-left:auto;font-size:0.62rem;}
.hud-stat{display:flex;flex-direction:column;align-items:center;background:rgba(255,255,255,0.05);border:1px solid rgba(255,150,0,0.2);border-radius:3px;padding:3px 8px;}
.hud-stat-val{font-size:0.85rem;font-weight:700;color:#ffcc00;}
.hud-stat-lbl{color:#888;font-size:0.5rem;}
.floor-badge{font-family:'Black Han Sans',sans-serif;font-size:0.85rem;color:#fff;background:rgba(255,100,0,0.2);border:1px solid #ff6600;border-radius:3px;padding:3px 10px;}

/* CANVAS */
#gameCanvas{
  position:absolute;top:56px;left:0;
  width:900px;height:468px;
  background:#000;display:block;
  image-rendering:pixelated;
}

/* SKILL BAR */
#skillBar{
  position:absolute;bottom:0;left:0;right:0;height:56px;
  background:linear-gradient(0deg,rgba(0,0,0,0.95) 0%,rgba(0,0,0,0.7) 100%);
  border-top:2px solid #ff6600;
  display:flex;align-items:center;justify-content:center;gap:6px;padding:6px;z-index:100;
}
.skill-slot{
  width:44px;height:44px;border-radius:4px;
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,150,0,0.3);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  font-size:1.3rem;position:relative;cursor:default;
  transition:all 0.1s;
}
.skill-slot.ready{border-color:#ff9900;box-shadow:0 0 6px rgba(255,150,0,0.4);}
.skill-slot.cooling{opacity:0.4;}
.skill-cd{
  position:absolute;inset:0;background:rgba(0,0,0,0.7);
  border-radius:4px;display:flex;align-items:center;justify-content:center;
  font-size:0.7rem;color:#ffcc00;font-weight:700;
}
.skill-key{position:absolute;bottom:1px;right:2px;font-size:0.4rem;color:#aaa;}
.skill-desc-bar{
  margin-left:16px;border-left:1px solid rgba(255,150,0,0.2);
  padding-left:14px;font-size:0.62rem;color:#888;
}
.skill-desc-bar b{color:#ffcc00;}
.controls-hint{margin-left:auto;margin-right:8px;font-size:0.55rem;color:#555;text-align:right;line-height:1.8;}

/* OVERLAYS */
.overlay{
  position:absolute;inset:0;z-index:200;
  display:flex;align-items:center;justify-content:center;
  background:rgba(0,0,0,0.92);
}
.overlay.hidden{display:none;}

/* TITLE */
#titleScreen{flex-direction:column;text-align:center;}
.title-logo{
  font-family:'Black Han Sans',sans-serif;
  font-size:3.5rem;color:#ff6600;
  text-shadow:0 0 30px rgba(255,100,0,0.8),0 0 60px rgba(255,50,0,0.4);
  letter-spacing:6px;margin-bottom:4px;
}
.title-sub{font-size:0.9rem;color:#888;letter-spacing:8px;margin-bottom:40px;}
.char-select{display:flex;gap:16px;margin-bottom:36px;}
.char-card{
  width:130px;background:rgba(255,255,255,0.03);
  border:2px solid rgba(255,150,0,0.15);border-radius:6px;
  padding:16px 10px;cursor:pointer;transition:all 0.2s;text-align:center;
}
.char-card:hover,.char-card.sel{
  border-color:#ff9900;background:rgba(255,150,0,0.08);
  transform:translateY(-4px);box-shadow:0 8px 24px rgba(255,100,0,0.2);
}
.char-icon{font-size:2.8rem;display:block;margin-bottom:8px;}
.char-name{font-family:'Black Han Sans',sans-serif;font-size:0.85rem;color:#ffcc00;letter-spacing:2px;}
.char-type{font-size:0.58rem;color:#888;margin-top:3px;}
.start-btn{
  padding:12px 48px;background:linear-gradient(135deg,#8b3a00,#ff6600);
  border:none;border-radius:4px;color:#fff;font-size:1rem;
  font-family:'Black Han Sans',sans-serif;letter-spacing:3px;cursor:pointer;
  box-shadow:0 0 20px rgba(255,100,0,0.4);transition:all 0.2s;
}
.start-btn:hover{transform:scale(1.05);box-shadow:0 0 30px rgba(255,100,0,0.6);}
.start-btn:disabled{opacity:0.3;cursor:default;transform:none;}

/* STAGE CLEAR / GAME OVER */
#stageClear,#gameOver{flex-direction:column;text-align:center;}
.result-title{font-family:'Black Han Sans',sans-serif;font-size:2.5rem;letter-spacing:4px;margin-bottom:12px;}
.clear-title{color:#ffcc00;text-shadow:0 0 20px rgba(255,200,0,0.6);}
.over-title{color:#ff2222;text-shadow:0 0 20px rgba(255,0,0,0.6);}
.result-stats{
  display:grid;grid-template-columns:1fr 1fr;gap:8px;
  background:rgba(255,255,255,0.04);border-radius:6px;
  padding:16px 24px;margin:16px 0;font-size:0.75rem;
  border:1px solid rgba(255,150,0,0.15);
}
.result-stats>div{display:flex;justify-content:space-between;gap:20px;}
.result-stats b{color:#ffcc00;}
.action-btns{display:flex;gap:10px;margin-top:10px;}
.action-btn{
  padding:10px 28px;border:none;border-radius:4px;cursor:pointer;
  font-family:'Black Han Sans',sans-serif;letter-spacing:2px;font-size:0.85rem;transition:all 0.2s;
}
.btn-next{background:linear-gradient(135deg,#1a5a00,#22cc00);color:#fff;}
.btn-retry{background:linear-gradient(135deg,#5a1a00,#cc4400);color:#fff;}
.btn-title{background:rgba(255,255,255,0.08);color:#aaa;border:1px solid rgba(255,255,255,0.1);}
.action-btn:hover{transform:translateY(-2px);filter:brightness(1.2);}

/* DAMAGE NUMBERS */
@keyframes floatUp{0%{opacity:1;transform:translateY(0) scale(1);}100%{opacity:0;transform:translateY(-60px) scale(0.7);}}
.dmg-num{position:absolute;pointer-events:none;font-family:'Black Han Sans',sans-serif;font-weight:900;animation:floatUp 0.9s ease forwards;z-index:150;text-shadow:1px 1px 2px rgba(0,0,0,0.9);}

/* BOSS WARNING */
@keyframes bossWarn{0%,100%{opacity:0;}20%,80%{opacity:1;}}
#bossWarning{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  font-family:'Black Han Sans',sans-serif;font-size:2rem;color:#ff2222;
  text-shadow:0 0 20px rgba(255,0,0,0.8);letter-spacing:6px;
  animation:bossWarn 1.5s ease forwards;pointer-events:none;z-index:180;display:none;
}

/* BOSS HP */
#bossHpWrap{
  position:absolute;top:62px;left:50%;transform:translateX(-50%);
  width:400px;pointer-events:none;z-index:120;opacity:0;transition:opacity 0.3s;
}
#bossHpWrap.show{opacity:1;}
#bossName{text-align:center;font-family:'Black Han Sans',sans-serif;font-size:0.8rem;color:#ff4444;margin-bottom:3px;text-shadow:0 0 8px rgba(255,0,0,0.5);}
#bossHpBg{height:10px;background:rgba(255,255,255,0.06);border-radius:2px;border:1px solid rgba(255,50,50,0.3);}
#bossHpFill{height:100%;background:linear-gradient(90deg,#7b0000,#ff0000,#ff4444);border-radius:2px;transition:width 0.2s;}
</style>
</head>
<body>
<div id="gameWrapper">
  <!-- HUD -->
  <div id="hud">
    <div class="hud-name" id="hudName">캐릭터</div>
    <div class="bar-wrap">
      <div class="bar-label">HP</div>
      <div class="bar-bg"><div class="bar-fill" id="hp-bar" style="width:100%"></div></div>
    </div>
    <div class="bar-wrap">
      <div class="bar-label">MP</div>
      <div class="bar-bg"><div class="bar-fill" id="mp-bar" style="width:100%"></div></div>
    </div>
    <div class="hud-stats">
      <div class="hud-stat"><div class="hud-stat-val" id="stat-lv">1</div><div class="hud-stat-lbl">LV</div></div>
      <div class="hud-stat"><div class="hud-stat-val" id="stat-kills">0</div><div class="hud-stat-lbl">KILL</div></div>
      <div class="hud-stat"><div class="hud-stat-val" id="stat-score">0</div><div class="hud-stat-lbl">SCORE</div></div>
      <div class="hud-stat"><div class="hud-stat-val" id="stat-gold">0</div><div class="hud-stat-lbl">💰</div></div>
    </div>
    <div class="floor-badge" id="floorBadge">1-1</div>
  </div>

  <!-- GAME CANVAS -->
  <canvas id="gameCanvas" width="900" height="468"></canvas>

  <!-- BOSS HP -->
  <div id="bossHpWrap">
    <div id="bossName">보스</div>
    <div id="bossHpBg"><div id="bossHpFill" style="width:100%"></div></div>
  </div>

  <!-- BOSS WARNING -->
  <div id="bossWarning">⚠ BOSS APPEAR ⚠</div>

  <!-- SKILL BAR -->
  <div id="skillBar">
    <div id="skills-container" style="display:flex;gap:6px;"></div>
    <div class="skill-desc-bar" id="skill-desc"></div>
    <div class="controls-hint">
      ← → 이동 &nbsp;|&nbsp; Z 점프 &nbsp;|&nbsp; X 공격<br>
      A S D F G 스킬 &nbsp;|&nbsp; Space 긴급회피
    </div>
  </div>

  <!-- TITLE -->
  <div class="overlay" id="titleScreen">
    <div>
      <div class="title-logo">던전 파이터</div>
      <div class="title-sub">DUNGEON  FIGHTER</div>
      <div class="char-select" id="charSelect"></div>
      <div style="text-align:center;">
        <button class="start-btn" id="startBtn" onclick="startGame()" disabled>전투 시작 ▶</button>
      </div>
    </div>
  </div>

  <!-- STAGE CLEAR -->
  <div class="overlay hidden" id="stageClear">
    <div>
      <div class="result-title clear-title">✦ STAGE CLEAR ✦</div>
      <div class="result-stats" id="clearStats"></div>
      <div class="action-btns" style="justify-content:center;">
        <button class="action-btn btn-next" onclick="nextStage()">다음 스테이지 →</button>
        <button class="action-btn btn-title" onclick="goTitle()">타이틀로</button>
      </div>
    </div>
  </div>

  <!-- GAME OVER -->
  <div class="overlay hidden" id="gameOver">
    <div>
      <div class="result-title over-title">💀 GAME OVER</div>
      <div class="result-stats" id="overStats"></div>
      <div class="action-btns" style="justify-content:center;">
        <button class="action-btn btn-retry" onclick="retryStage()">재도전 ↺</button>
        <button class="action-btn btn-title" onclick="goTitle()">타이틀로</button>
      </div>
    </div>
  </div>
</div>

<script>
'use strict';
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const W = 900, H = 468;

// ── CHARACTERS ──────────────────────────────────────────
const CHARACTERS = [
  {
    id:'fighter', name:'파이터', icon:'🥊', type:'근접 격투기',
    color:'#ff6600', color2:'#ffaa00',
    hp:320, mp:80, atk:38, def:12, spd:4.5, jumpPow:13,
    skills:[
      {id:'s1',name:'맹렬한 주먹',icon:'👊',key:'A',mp:15,cd:2,desc:'전방 3타 연속 주먹',color:'#ff6600'},
      {id:'s2',name:'격파',icon:'💥',key:'S',mp:25,cd:5,desc:'강력한 하방 파괴 공격',color:'#ff2200'},
      {id:'s3',name:'날아차기',icon:'🦵',key:'D',mp:20,cd:4,desc:'앞으로 돌진 발차기',color:'#ff8800'},
      {id:'s4',name:'폭발 주먹',icon:'🔥',key:'F',mp:40,cd:8,desc:'폭발 속성 강타',color:'#ff4400'},
      {id:'s5',name:'버서커 모드',icon:'😡',key:'G',mp:60,cd:15,desc:'10초간 ATK 2배',color:'#cc0000'},
    ]
  },
  {
    id:'mage', name:'마법사', icon:'🔮', type:'원소 마법사',
    color:'#4488ff', color2:'#88bbff',
    hp:200, mp:200, atk:50, def:6, spd:4, jumpPow:12,
    skills:[
      {id:'s1',name:'파이어볼',icon:'🔥',key:'A',mp:20,cd:2,desc:'전방 화염탄 발사',color:'#ff6600'},
      {id:'s2',name:'아이스 스파이크',icon:'❄️',key:'S',mp:25,cd:4,desc:'빙결 마법탄',color:'#44aaff'},
      {id:'s3',name:'썬더',icon:'⚡',key:'D',mp:30,cd:5,desc:'번개 낙하 마법',color:'#ffff00'},
      {id:'s4',name:'메테오',icon:'☄️',key:'F',mp:60,cd:10,desc:'운석 낙하 광역기',color:'#ff4400'},
      {id:'s5',name:'타임 스탑',icon:'⏰',key:'G',mp:80,cd:20,desc:'3초간 모든 적 정지',color:'#aa44ff'},
    ]
  },
  {
    id:'knight', name:'나이트', icon:'⚔️', type:'중갑 전사',
    color:'#aabbcc', color2:'#ddeeff',
    hp:450, mp:100, atk:32, def:22, spd:3.5, jumpPow:11,
    skills:[
      {id:'s1',name:'소드 슬래시',icon:'⚔️',key:'A',mp:15,cd:2,desc:'넓은 범위 검격',color:'#aabbcc'},
      {id:'s2',name:'방패 강타',icon:'🛡️',key:'S',mp:20,cd:4,desc:'방패로 적 스턴',color:'#8899aa'},
      {id:'s3',name:'차지 돌격',icon:'💨',key:'D',mp:25,cd:5,desc:'전방 고속 돌격',color:'#ccddee'},
      {id:'s4',name:'회오리 베기',icon:'🌀',key:'F',mp:40,cd:8,desc:'주변 360도 공격',color:'#99aabb'},
      {id:'s5',name:'성스러운 검',icon:'✨',key:'G',mp:70,cd:15,desc:'광속성 강화 검격',color:'#ffffaa'},
    ]
  },
  {
    id:'archer', name:'건너', icon:'🔫', type:'총기 사수',
    color:'#44cc88', color2:'#88ffaa',
    hp:240, mp:150, atk:44, def:8, spd:5, jumpPow:14,
    skills:[
      {id:'s1',name:'연사',icon:'🔫',key:'A',mp:15,cd:1,desc:'3연발 총기 공격',color:'#44cc88'},
      {id:'s2',name:'유탄 투척',icon:'💣',key:'S',mp:25,cd:4,desc:'범위 폭발 유탄',color:'#ffcc00'},
      {id:'s3',name:'스나이핑',icon:'🎯',key:'D',mp:30,cd:5,desc:'관통 저격탄',color:'#88ff44'},
      {id:'s4',name:'유도탄',icon:'🚀',key:'F',mp:40,cd:8,desc:'추적 미사일 발사',color:'#ff8800'},
      {id:'s5',name:'인피니티 블릿',icon:'🌟',key:'G',mp:80,cd:20,desc:'화면 전체 난사',color:'#44ffaa'},
    ]
  },
];

// ── STAGE DATA ─────────────────────────────────────────
const STAGES = [
  {name:'어둠의 동굴',bgColor:'#0a0818',floorColor:'#1a1030',wallColor:'#0d0a20',enemies:5,boss:'슬라임 대왕',bossHp:600},
  {name:'용암 던전',bgColor:'#180800',floorColor:'#2a1000',wallColor:'#1a0a00',enemies:7,boss:'불꽃 골렘',bossHp:900},
  {name:'얼음 궁전',bgColor:'#080818',floorColor:'#101830',wallColor:'#0a1020',enemies:9,boss:'빙결 드래곤',bossHp:1300},
  {name:'암흑 마성',bgColor:'#0a0010',floorColor:'#150020',wallColor:'#100015',enemies:12,boss:'마왕 DARKOS',bossHp:2000},
];

const ENEMY_TYPES = [
  {name:'고블린',   icon:'👺',hp:80, atk:12,spd:2.5,xp:15,g:8, color:'#33aa33',sz:28},
  {name:'오크',     icon:'👹',hp:140,atk:18,spd:2,  xp:25,g:15,color:'#887733',sz:36},
  {name:'스켈레톤', icon:'💀',hp:100,atk:15,spd:3,  xp:20,g:12,color:'#aaaaaa',sz:30},
  {name:'좀비',     icon:'🧟',hp:120,atk:14,spd:1.5,xp:22,g:13,color:'#556633',sz:32},
  {name:'마법사',   icon:'🧙',hp:90, atk:22,spd:2.5,xp:30,g:20,color:'#5533aa',sz:28,ranged:true},
  {name:'드래고니언',icon:'🐊',hp:200,atk:25,spd:2, xp:45,g:30,color:'#336633',sz:40},
];

// ── GAME STATE ──────────────────────────────────────────
let G = null;
let selectedChar = null;
let animId = null;
let keys = {};
let justPressed = {};

// ── PHYSICS CONSTANTS ──────────────────────────────────
const GRAVITY = 0.55;
const FLOOR_Y = H - 80;
const STAGE_W = 3600;

// ── PARTICLE SYSTEM ────────────────────────────────────
let particles = [];
function spawnParticles(x, y, color, count, opts={}) {
  for(let i = 0; i < count; i++) {
    const angle = (opts.dir || 0) + (Math.random()-0.5) * (opts.spread || Math.PI*2);
    const speed = (opts.minSpd||1) + Math.random()*(opts.maxSpd||4);
    particles.push({
      x, y,
      vx: Math.cos(angle)*speed,
      vy: Math.sin(angle)*speed - (opts.upBias||0),
      life: 1,
      decay: 0.03 + Math.random()*0.04,
      color,
      size: (opts.minSz||2) + Math.random()*(opts.maxSz||5),
      type: opts.type || 'circle',
    });
  }
}

// ── PROJECTILES ─────────────────────────────────────────
let projectiles = [];
function spawnProjectile(x, y, vx, vy, dmg, color, owner, opts={}) {
  projectiles.push({
    x, y, vx, vy, dmg, color, owner,
    life: opts.life || 80,
    size: opts.size || 8,
    pierce: opts.pierce || false,
    gravity: opts.gravity || 0,
    emoji: opts.emoji || null,
    trail: opts.trail || false,
    hit: false,
  });
}

// ── DAMAGE NUMBERS ──────────────────────────────────────
let dmgNums = [];
function showDmgNum(x, y, val, color, crit) {
  const el = document.createElement('div');
  el.className = 'dmg-num';
  el.textContent = crit ? `${val}!!` : val;
  el.style.cssText = `
    left:${x-20}px; top:${y}px;
    font-size:${crit?'1.4':'1rem'};
    color:${crit?'#ffff00':color};
    position:absolute;
  `;
  document.getElementById('gameWrapper').appendChild(el);
  setTimeout(()=>el.remove(), 900);
}

// ── INIT CHARACTER ───────────────────────────────────────
function initPlayer(charData) {
  return {
    ...charData,
    x: 120, y: FLOOR_Y - charData.hp*0, // placeholder
    vy: 0, vx: 0,
    onGround: false,
    facing: 1,
    hp: charData.hp, maxHp: charData.hp,
    mp: charData.mp, maxMp: charData.mp,
    kills: 0, score: 0, gold: 0, level: 1, xp: 0, xpNext: 100,
    alive: true,
    invincible: 0,
    skillCds: charData.skills.map(()=>0),
    buffAtk: 1,
    buffAtkTimer: 0,
    frozen: 0,
    stunned: 0,
    comboCount: 0,
    comboTimer: 0,
    attackCooldown: 0,
    attackAnim: 0,
    hitAnim: 0,
    jumpCount: 0,
    dodgeTimer: 0,
    width: 44,
    height: 60,
  };
}

function initG(charId, stageIdx) {
  const charData = CHARACTERS.find(c=>c.id===charId);
  const stage = STAGES[stageIdx];
  const p = initPlayer(charData);
  p.x = 120;
  p.y = FLOOR_Y - p.height;

  G = {
    charId, stageIdx,
    stage,
    player: p,
    enemies: [],
    camera: 0,
    spawnTimer: 0,
    spawnedCount: 0,
    bossSpawned: false,
    boss: null,
    phase: 'play', // play | clear | over
    timer: 0,
    startTime: Date.now(),
    platforms: generatePlatforms(stage),
    bgParallax: 0,
    shakeTimer: 0,
    shakeAmt: 0,
  };
  spawnEnemies(stage);
  particles = [];
  projectiles = [];
}

function generatePlatforms(stage) {
  const plats = [];
  for(let i = 0; i < 12; i++) {
    const x = 300 + i * 260 + (Math.random()-0.5)*80;
    const y = FLOOR_Y - 80 - Math.random()*120;
    const w = 80 + Math.random()*60;
    plats.push({x, y, w, h:14, color: stage.wallColor});
  }
  return plats;
}

function spawnEnemies(stage) {
  G.enemies = [];
  const count = stage.enemies;
  for(let i = 0; i < count; i++) {
    const et = ENEMY_TYPES[Math.floor(Math.random()*5)];
    const sc = 1 + G.stageIdx*0.3;
    const ex = 600 + i * 280 + Math.random()*100;
    G.enemies.push({
      ...et,
      uid: 'e'+i,
      x: ex, y: FLOOR_Y - (et.sz||30),
      hp: Math.round(et.hp*sc),
      maxHp: Math.round(et.hp*sc),
      atk: Math.round(et.atk*sc),
      vy: 0, facing: -1,
      alive: true,
      stunned: 0,
      frozen: 0,
      attackTimer: 60 + Math.random()*60,
      alertRange: 320,
      width: et.sz||30,
      height: et.sz||30,
      aggro: false,
    });
  }
}

function spawnBoss() {
  const stage = G.stage;
  const sc = 1 + G.stageIdx*0.4;
  G.boss = {
    name: stage.boss,
    x: STAGE_W - 400, y: FLOOR_Y - 80,
    hp: Math.round(stage.bossHp*sc), maxHp: Math.round(stage.bossHp*sc),
    atk: Math.round((30+G.stageIdx*10)*sc),
    spd: 2.5 + G.stageIdx*0.3,
    facing: -1,
    alive: true,
    stunned: 0,
    frozen: 0,
    attackTimer: 90,
    phase2: false,
    enrageTimer: 0,
    width: 70, height: 80,
    color: '#ff2200',
    projectileTimer: 0,
  };
  document.getElementById('bossHpWrap').classList.add('show');
  document.getElementById('bossName').textContent = `⚠ ${stage.boss}`;
  const bw = document.getElementById('bossWarning');
  bw.style.display = 'block';
  setTimeout(()=>bw.style.display='none', 1600);
  screenShake(8, 30);
}

// ── MAIN GAME LOOP ───────────────────────────────────────
let lastTime = 0;
function gameLoop(ts) {
  if(!G || G.phase !== 'play') { animId = requestAnimationFrame(gameLoop); return; }
  const dt = Math.min((ts - lastTime)/16.67, 2.5);
  lastTime = ts;
  G.timer++;

  update(dt);
  render();
  updateHUD();
  justPressed = {};
  animId = requestAnimationFrame(gameLoop);
}

// ── UPDATE ──────────────────────────────────────────────
function update(dt) {
  const p = G.player;
  if(!p.alive) return;

  // Input
  handleInput(dt);

  // Player physics
  p.vy += GRAVITY * dt;
  p.x += p.vx * dt;
  p.y += p.vy * dt;
  p.vx *= 0.82;

  // Floor collision
  if(p.y + p.height >= FLOOR_Y) {
    p.y = FLOOR_Y - p.height;
    p.vy = 0;
    p.onGround = true;
    p.jumpCount = 0;
  } else {
    p.onGround = false;
  }

  // Platform collision
  for(const plat of G.platforms) {
    if(p.vy >= 0 &&
       p.x + p.width > plat.x && p.x < plat.x + plat.w &&
       p.y + p.height > plat.y && p.y + p.height < plat.y + plat.h + 16) {
      p.y = plat.y - p.height;
      p.vy = 0;
      p.onGround = true;
      p.jumpCount = 0;
    }
  }

  // Stage bounds
  p.x = Math.max(10, Math.min(STAGE_W - p.width - 10, p.x));
  if(p.y > H + 100) { p.y = FLOOR_Y - p.height; p.vy = 0; }

  // Camera
  const targetCam = p.x - W * 0.35;
  G.camera += (targetCam - G.camera) * 0.08 * dt;
  G.camera = Math.max(0, Math.min(STAGE_W - W, G.camera));

  // Timers
  if(p.invincible > 0) p.invincible -= dt;
  if(p.attackCooldown > 0) p.attackCooldown -= dt;
  if(p.attackAnim > 0) p.attackAnim -= dt;
  if(p.hitAnim > 0) p.hitAnim -= dt;
  if(p.buffAtkTimer > 0) { p.buffAtkTimer -= dt; if(p.buffAtkTimer <= 0) p.buffAtk = 1; }
  if(p.dodgeTimer > 0) p.dodgeTimer -= dt;
  if(p.comboTimer > 0) { p.comboTimer -= dt; if(p.comboTimer <= 0) p.comboCount = 0; }
  G.skillCds = G.skillCds || p.skillCds;
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i] -= dt/60;
  if(G.shakeTimer > 0) G.shakeTimer -= dt;

  // MP regen
  if(G.timer % 90 === 0) p.mp = Math.min(p.maxMp, p.mp + 3);

  // Enemies
  updateEnemies(dt);

  // Boss
  if(G.boss && G.boss.alive) updateBoss(dt);

  // Check boss spawn
  if(!G.bossSpawned && G.enemies.filter(e=>e.alive).length === 0) {
    G.bossSpawned = true;
    spawnBoss();
  }

  // Check win
  if(G.bossSpawned && G.boss && !G.boss.alive) {
    stageClear();
  }

  // Projectiles
  updateProjectiles(dt);

  // Particles
  particles = particles.filter(pt => {
    pt.x += pt.vx * dt;
    pt.y += pt.vy * dt;
    pt.vy += 0.15 * dt;
    pt.life -= pt.decay * dt;
    return pt.life > 0;
  });
}

function handleInput(dt) {
  const p = G.player;
  if(p.stunned > 0) { p.stunned -= dt; return; }
  if(p.frozen > 0) { p.frozen -= dt; return; }

  const spd = p.spd;
  if(keys['ArrowLeft'] || keys['a'] === false) {
    // handled below
  }
  if(keys['ArrowLeft']) { p.vx = -spd * 60 * 0.1 * dt * 6; p.facing = -1; }
  if(keys['ArrowRight']) { p.vx = spd * 60 * 0.1 * dt * 6; p.facing = 1; }

  // Jump (Z)
  if(justPressed['z'] || justPressed['Z']) {
    if(p.jumpCount < 2) {
      p.vy = -p.jumpPow;
      p.jumpCount++;
      spawnParticles(p.x+p.width/2, p.y+p.height, '#ffffff', 6, {upBias:2, maxSpd:3, minSz:2, maxSz:4});
    }
  }

  // Attack (X)
  if((justPressed['x'] || justPressed['X']) && p.attackCooldown <= 0) {
    doAttack(p);
  }

  // Dodge (Space)
  if(justPressed[' '] && p.dodgeTimer <= 0) {
    p.vx = p.facing * 18;
    p.vy = -4;
    p.invincible = 30;
    p.dodgeTimer = 45;
    spawnParticles(p.x+p.width/2, p.y+p.height/2, p.color, 10, {spread:Math.PI*0.5, dir:Math.PI+Math.PI/2*p.facing, minSpd:2, maxSpd:5});
  }

  // Skills
  const skillKeys = {'a':0,'s':1,'d':2,'f':3,'g':4,'A':0,'S':1,'D':2,'F':3,'G':4};
  for(const [k, idx] of Object.entries(skillKeys)) {
    if(justPressed[k] && idx < p.skills.length) {
      trySkill(p, idx);
      break;
    }
  }
}

function doAttack(p) {
  p.attackCooldown = 18;
  p.attackAnim = 15;
  p.comboCount = Math.min(4, (p.comboCount||0)+1);
  p.comboTimer = 80;

  const ax = p.x + (p.facing === 1 ? p.width : -50);
  const atkW = 65, atkH = 55;
  const baseDmg = p.atk * p.buffAtk;
  const crit = Math.random() < 0.12;
  const dmg = Math.round((baseDmg + Math.random()*10 - 5) * (crit?1.8:1) * (1+p.comboCount*0.1));

  let hit = false;
  const targets = G.boss ? [...G.enemies, G.boss] : G.enemies;
  for(const e of targets) {
    if(!e.alive) continue;
    if(ax < e.x+e.width && ax+atkW > e.x && p.y < e.y+e.height && p.y+p.height > e.y) {
      dealDmg(e, dmg, crit, p.color);
      hit = true;
    }
  }
  if(hit) {
    spawnParticles(ax+20, p.y+30, p.color, crit?15:8, {spread:Math.PI*0.6, dir:p.facing===1?0:Math.PI, minSpd:2, maxSpd:crit?8:5});
    if(crit) screenShake(3, 5);
  }
}

function dealDmg(target, dmg, crit, color) {
  if(!target.alive) return;
  target.hp -= dmg;
  const sx = target.x - G.camera + target.width/2;
  const sy = target.y - 10;
  showDmgNum(sx, sy, dmg, color||'#ffffff', crit);
  if(target.hp <= 0) killTarget(target);
  else target.stunned = crit ? 12 : 4;
}

function killTarget(target) {
  target.alive = false;
  const p = G.player;
  if(target === G.boss) {
    p.xp += 500; p.gold += 300; p.score += 5000;
    spawnParticles(target.x+target.width/2-G.camera, target.y+target.height/2, '#ffcc00', 40, {minSpd:2,maxSpd:8});
    screenShake(12, 40);
    document.getElementById('bossHpWrap').classList.remove('show');
  } else {
    p.kills++; p.xp += target.xp; p.gold += target.g; p.score += target.xp*2;
    spawnParticles(target.x+target.width/2-G.camera, target.y+target.height/2, target.color, 15);
    checkLevelUp(p);
  }
}

function checkLevelUp(p) {
  while(p.xp >= p.xpNext) {
    p.xp -= p.xpNext;
    p.level++;
    p.xpNext = Math.round(p.xpNext * 1.6);
    p.atk += 4; p.def += 2; p.maxHp += 30; p.hp = Math.min(p.maxHp, p.hp+40);
    p.maxMp += 10; p.mp = Math.min(p.maxMp, p.mp+20);
    spawnParticles(p.x+p.width/2-G.camera, p.y+p.height/2, '#ffff00', 20, {minSpd:2,maxSpd:6});
  }
}

function trySkill(p, idx) {
  const sk = p.skills[idx];
  if(!sk) return;
  if(p.skillCds[idx] > 0) return;
  if(p.mp < sk.mp) { return; }
  p.mp -= sk.mp;
  p.skillCds[idx] = sk.cd * 60;
  executeSkill(p, sk, idx);
}

function executeSkill(p, sk, idx) {
  const charId = p.id;

  if(charId === 'fighter') {
    if(idx===0) { // 맹렬한 주먹 - 3타
      for(let i=0;i<3;i++) {
        setTimeout(()=>{
          if(!G||!p.alive) return;
          const dmg = Math.round(p.atk*1.4*p.buffAtk);
          hitAoe(p.x+(p.facing===1?p.width:-60), p.y, 70, 60, dmg, false, sk.color);
        }, i*120);
      }
    } else if(idx===1) { // 격파
      const dmg = Math.round(p.atk*2.5*p.buffAtk);
      p.vy = -8;
      setTimeout(()=>{
        if(!G) return;
        hitAoe(p.x-20, p.y, 80, 60, dmg, true, sk.color);
        screenShake(6, 15);
      }, 200);
    } else if(idx===2) { // 날아차기
      p.vx = p.facing * 25;
      const dmg = Math.round(p.atk*1.8*p.buffAtk);
      hitAoe(p.x+(p.facing===1?40:-100), p.y, 100, 60, dmg, false, sk.color);
    } else if(idx===3) { // 폭발 주먹
      const dmg = Math.round(p.atk*3*p.buffAtk);
      hitAoe(p.x+(p.facing===1?p.width:-80), p.y-20, 90, 80, dmg, true, sk.color);
      spawnParticles(p.x+p.facing*80-G.camera, p.y+30, '#ff6600', 25, {minSpd:3,maxSpd:9,minSz:3,maxSz:8});
      screenShake(8, 20);
    } else if(idx===4) { // 버서커
      p.buffAtk = 2.0; p.buffAtkTimer = 600;
      spawnParticles(p.x+p.width/2-G.camera, p.y+p.height/2, '#ff0000', 30, {minSpd:2,maxSpd:7});
    }
  }
  else if(charId === 'mage') {
    if(idx===0) { // 파이어볼
      spawnProjectile(p.x+p.facing*50, p.y+20, p.facing*14, -1, Math.round(p.atk*2), '#ff6600', 'player', {size:14, emoji:'🔥', life:60, trail:true});
    } else if(idx===1) { // 아이스 스파이크
      spawnProjectile(p.x+p.facing*50, p.y+20, p.facing*12, 0, Math.round(p.atk*1.8), '#44aaff', 'player', {size:12, emoji:'❄️', life:70});
    } else if(idx===2) { // 썬더
      const tx = p.x + p.facing*200;
      spawnProjectile(tx, 0, 0, 18, Math.round(p.atk*2.5), '#ffff00', 'player', {size:16, emoji:'⚡', life:40, gravity:0.5});
    } else if(idx===3) { // 메테오
      for(let i=0;i<5;i++) {
        setTimeout(()=>{
          if(!G) return;
          const tx = p.x + p.facing*150 + (Math.random()-0.5)*200 - G.camera;
          spawnProjectile(G.camera + tx, -40, 0, 16, Math.round(p.atk*3), '#ff4400', 'player', {size:20, emoji:'☄️', life:60, gravity:0.4});
          screenShake(5, 10);
        }, i*160);
      }
    } else if(idx===4) { // 타임 스탑
      for(const e of G.enemies) e.frozen = 180;
      if(G.boss) G.boss.frozen = 180;
      spawnParticles(W/2, H/2, '#aa44ff', 40, {minSpd:3,maxSpd:10,minSz:2,maxSz:6});
    }
  }
  else if(charId === 'knight') {
    if(idx===0) { // 소드 슬래시
      const dmg = Math.round(p.atk*1.6*p.buffAtk);
      hitAoe(p.x-20, p.y-10, 110, 70, dmg, false, sk.color);
    } else if(idx===1) { // 방패 강타
      const dmg = Math.round(p.atk*1.3*p.buffAtk);
      hitAoe(p.x+(p.facing===1?20:-80), p.y, 70, 60, dmg, true, sk.color);
    } else if(idx===2) { // 차지
      p.vx = p.facing * 35;
      p.invincible = 20;
      setTimeout(()=>{
        if(!G) return;
        const dmg = Math.round(p.atk*2*p.buffAtk);
        hitAoe(p.x+(p.facing===1?p.width:-80), p.y, 80, 70, dmg, false, sk.color);
      }, 150);
    } else if(idx===3) { // 회오리
      const dmg = Math.round(p.atk*1.5*p.buffAtk);
      hitAoe(p.x-50, p.y-20, 140, 100, dmg, false, sk.color);
      spawnParticles(p.x+p.width/2-G.camera, p.y+p.height/2, '#ccddee', 20, {minSpd:3,maxSpd:7});
    } else if(idx===4) { // 성스러운 검
      const dmg = Math.round(p.atk*4*p.buffAtk);
      hitAoe(p.x+(p.facing===1?-10:-100), p.y-30, 160, 110, dmg, true, sk.color);
      screenShake(10, 25);
    }
  }
  else if(charId === 'archer') {
    if(idx===0) { // 연사
      for(let i=0;i<3;i++) {
        setTimeout(()=>{
          if(!G) return;
          spawnProjectile(p.x+p.facing*50, p.y+25, p.facing*18+(Math.random()-0.5)*2, (Math.random()-0.5)*2, Math.round(p.atk*1.2), '#44cc88', 'player', {size:7, life:70});
        }, i*80);
      }
    } else if(idx===1) { // 유탄
      spawnProjectile(p.x+p.facing*40, p.y+20, p.facing*10, -8, Math.round(p.atk*2.5), '#ffcc00', 'player', {size:15, emoji:'💣', life:80, gravity:0.4});
    } else if(idx===2) { // 스나이핑
      spawnProjectile(p.x+p.facing*50, p.y+25, p.facing*30, 0, Math.round(p.atk*4), '#88ff44', 'player', {size:10, life:100, pierce:true});
    } else if(idx===3) { // 유도탄
      for(let i=0;i<3;i++) {
        setTimeout(()=>{
          if(!G) return;
          spawnProjectile(p.x+p.facing*30, p.y+15, p.facing*8+(Math.random()-0.5)*4, -6+(Math.random()-0.5)*2, Math.round(p.atk*1.8), '#ff8800', 'player', {size:12, emoji:'🚀', life:100, gravity:0.05});
        }, i*100);
      }
    } else if(idx===4) { // 인피니티 블릿
      for(let i=0;i<12;i++) {
        setTimeout(()=>{
          if(!G) return;
          const angle = (i/12)*Math.PI*2;
          spawnProjectile(p.x+p.width/2, p.y+p.height/2, Math.cos(angle)*15, Math.sin(angle)*12, Math.round(p.atk*1.5), '#44ffaa', 'player', {size:8, life:60, pierce:true});
        }, i*50);
      }
    }
  }
}

function hitAoe(x, y, w, h, dmg, crit, color) {
  const targets = G.boss ? [...G.enemies, G.boss] : G.enemies;
  for(const e of targets) {
    if(!e.alive) continue;
    const ex = e.x, ey = e.y, ew = e.width, eh = e.height;
    if(x < ex+ew && x+w > ex && y < ey+eh && y+h > ey) {
      dealDmg(e, dmg, crit, color);
    }
  }
}

function updateEnemies(dt) {
  const p = G.player;
  for(const e of G.enemies) {
    if(!e.alive) continue;
    if(e.frozen > 0) { e.frozen -= dt; continue; }
    if(e.stunned > 0) { e.stunned -= dt; continue; }

    // Simple AI
    const dx = p.x - e.x;
    if(Math.abs(dx) < e.alertRange) e.aggro = true;

    if(e.aggro) {
      e.facing = dx > 0 ? 1 : -1;
      if(Math.abs(dx) > 50) e.x += e.facing * e.spd * dt * 0.9;
    }

    // Gravity
    e.vy = (e.vy||0) + GRAVITY * dt * 0.6;
    e.y += e.vy * dt;
    if(e.y + e.height >= FLOOR_Y) { e.y = FLOOR_Y - e.height; e.vy = 0; }

    // Attack player
    e.attackTimer -= dt;
    const dist = Math.abs(dx);
    if(e.ranged) {
      if(dist < 280 && dist > 60 && e.attackTimer <= 0) {
        e.attackTimer = 120;
        spawnProjectile(e.x+e.width/2, e.y+e.height/2, e.facing*10, -1, Math.round(e.atk*0.7), '#aa44ff', 'enemy', {size:10, life:80});
      }
    } else {
      if(dist < 60 && e.attackTimer <= 0 && p.invincible <= 0 && !e.stunned) {
        e.attackTimer = 90;
        if(Math.abs(p.y - e.y) < 60) {
          const dmg = Math.max(1, e.atk - p.def*0.5 + Math.floor(Math.random()*6)-3);
          if(p.dodgeTimer <= 0) {
            p.hp -= dmg;
            p.hitAnim = 10;
            p.invincible = 30;
            showDmgNum(p.x-G.camera+p.width/2, p.y, dmg, '#ff4444', false);
            screenShake(4, 10);
            if(p.hp <= 0) gameOver();
          }
        }
      }
    }
  }
}

function updateBoss(dt) {
  const p = G.player;
  const b = G.boss;
  if(!b.alive) return;
  if(b.frozen > 0) { b.frozen -= dt; return; }
  if(b.stunned > 0) { b.stunned -= dt; return; }

  // Phase 2
  if(!b.phase2 && b.hp < b.maxHp*0.4) {
    b.phase2 = true;
    b.spd *= 1.5;
    b.atk = Math.round(b.atk*1.5);
    screenShake(15, 50);
    spawnParticles(b.x+b.width/2-G.camera, b.y+b.height/2, '#ff0000', 40, {minSpd:3,maxSpd:10});
  }

  const dx = p.x - b.x;
  b.facing = dx > 0 ? 1 : -1;
  if(Math.abs(dx) > 80) b.x += b.facing * b.spd * dt * 0.9;

  // Gravity
  b.vy = (b.vy||0) + GRAVITY * dt * 0.5;
  b.y += b.vy * dt;
  if(b.y + b.height >= FLOOR_Y) { b.y = FLOOR_Y - b.height; b.vy = 0; }

  // Attack
  b.attackTimer -= dt;
  if(Math.abs(dx) < 90 && b.attackTimer <= 0 && p.invincible <= 0) {
    b.attackTimer = b.phase2 ? 55 : 80;
    if(Math.abs(p.y - b.y) < 80) {
      const dmg = Math.max(1, b.atk - p.def + Math.floor(Math.random()*10)-5);
      if(p.dodgeTimer <= 0) {
        p.hp -= dmg;
        p.hitAnim = 12;
        p.invincible = 25;
        showDmgNum(p.x-G.camera+p.width/2, p.y-10, dmg, '#ff2222', false);
        screenShake(7, 15);
        if(p.hp <= 0) gameOver();
      }
    }
  }

  // Boss projectile
  b.projectileTimer -= dt;
  if(b.projectileTimer <= 0) {
    b.projectileTimer = b.phase2 ? 70 : 110;
    spawnProjectile(b.x+b.width/2, b.y+b.height/3, b.facing*9, -3, Math.round(b.atk*0.6), '#ff4400', 'enemy', {size:16, emoji:'💥', life:90, gravity:0.1});
  }

  // Update boss hp bar
  document.getElementById('bossHpFill').style.width = Math.max(0,(b.hp/b.maxHp)*100)+'%';
}

function updateProjectiles(dt) {
  const p = G.player;
  projectiles = projectiles.filter(proj => {
    proj.x += proj.vx * dt;
    proj.y += proj.vy * dt;
    proj.vy += (proj.gravity||0) * dt;
    proj.life -= dt;
    if(proj.life <= 0) return false;

    if(proj.trail) {
      spawnParticles(proj.x, proj.y-G.camera, proj.color, 1, {minSpd:0.2,maxSpd:1,minSz:2,maxSz:4,spread:Math.PI*2});
    }

    // Hit detection
    if(proj.owner === 'player') {
      const targets = G.boss ? [...G.enemies, G.boss] : G.enemies;
      for(const e of targets) {
        if(!e.alive) continue;
        if(proj.x > e.x && proj.x < e.x+e.width && proj.y > e.y && proj.y < e.y+e.height) {
          dealDmg(e, proj.dmg, false, proj.color);
          spawnParticles(proj.x-G.camera, proj.y, proj.color, 8, {minSpd:1,maxSpd:4});
          if(!proj.pierce) { proj.life = 0; return false; }
        }
      }
    } else {
      // Enemy projectile hits player
      if(p.invincible <= 0 && p.dodgeTimer <= 0 && proj.owner === 'enemy') {
        const sc = proj.x - G.camera;
        if(sc > p.x-G.camera && sc < p.x-G.camera+p.width && proj.y > p.y && proj.y < p.y+p.height) {
          const dmg = Math.max(1, proj.dmg - p.def*0.3);
          p.hp -= dmg;
          p.invincible = 25;
          p.hitAnim = 10;
          showDmgNum(p.x-G.camera+p.width/2, p.y, dmg, '#ff4444', false);
          screenShake(3, 8);
          if(p.hp <= 0) gameOver();
          proj.life = 0;
          return false;
        }
      }
    }
    return true;
  });
}

// ── RENDER ──────────────────────────────────────────────
function render() {
  if(!G) return;
  ctx.save();

  // Shake
  if(G.shakeTimer > 0) {
    const s = G.shakeAmt * (G.shakeTimer/G.shakeAmt*0.5);
    ctx.translate((Math.random()-0.5)*s, (Math.random()-0.5)*s);
  }

  // Background
  const stage = G.stage;
  ctx.fillStyle = stage.bgColor;
  ctx.fillRect(0, 0, W, H);

  // Parallax BG elements
  drawBackground(stage);

  // Platforms
  for(const plat of G.platforms) {
    const px2 = plat.x - G.camera;
    if(px2 > W || px2+plat.w < 0) continue;
    ctx.fillStyle = stage.floorColor;
    ctx.fillRect(px2, plat.y, plat.w, plat.h);
    ctx.fillStyle = 'rgba(255,150,0,0.15)';
    ctx.fillRect(px2, plat.y, plat.w, 2);
  }

  // Floor
  ctx.fillStyle = stage.floorColor;
  ctx.fillRect(0, FLOOR_Y, W, H - FLOOR_Y);
  ctx.fillStyle = 'rgba(255,150,0,0.2)';
  ctx.fillRect(0, FLOOR_Y, W, 2);

  // Particles (behind entities)
  for(const pt of particles) {
    ctx.globalAlpha = pt.life;
    ctx.fillStyle = pt.color;
    ctx.beginPath();
    ctx.arc(pt.x, pt.y, pt.size, 0, Math.PI*2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;

  // Projectiles
  for(const proj of projectiles) {
    const px2 = proj.x - G.camera;
    if(proj.emoji) {
      ctx.font = `${proj.size*1.8}px serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(proj.emoji, px2, proj.y);
    } else {
      ctx.fillStyle = proj.color;
      ctx.shadowColor = proj.color;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(px2, proj.y, proj.size, 0, Math.PI*2);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  // Enemies
  for(const e of G.enemies) {
    if(!e.alive) continue;
    const ex2 = e.x - G.camera;
    if(ex2 < -60 || ex2 > W+60) continue;
    drawEnemy(e, ex2);
  }

  // Boss
  if(G.boss && G.boss.alive) {
    const bx = G.boss.x - G.camera;
    if(bx > -100 && bx < W+100) drawBoss(G.boss, bx);
  }

  // Player
  drawPlayer(G.player);

  // Attack effect
  const p = G.player;
  if(p.attackAnim > 0) {
    const ax = p.x - G.camera + (p.facing===1 ? p.width : -60);
    ctx.strokeStyle = `rgba(255,200,100,${p.attackAnim/15*0.7})`;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(ax+30, p.y+30, 35, 0, Math.PI*2);
    ctx.stroke();
  }

  ctx.restore();
}

function drawBackground(stage) {
  // Stars/torches
  ctx.globalAlpha = 0.15;
  for(let i=0;i<20;i++) {
    const tx = ((i*237 + G.camera*0.1) % STAGE_W - G.camera*0.1) % W;
    const ty = 20 + (i*113) % (FLOOR_Y-60);
    ctx.fillStyle = '#ffaa44';
    ctx.beginPath();
    ctx.arc(tx, ty, 2, 0, Math.PI*2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

function drawPlayer(p) {
  const px2 = p.x - G.camera;
  const alpha = p.invincible > 0 && Math.floor(G.timer/3)%2===0 ? 0.4 : 1;
  ctx.globalAlpha = alpha;

  // Shadow
  ctx.fillStyle = 'rgba(0,0,0,0.3)';
  ctx.beginPath();
  ctx.ellipse(px2+p.width/2, FLOOR_Y+4, p.width*0.5, 6, 0, 0, Math.PI*2);
  ctx.fill();

  // Body
  const hitOffset = p.hitAnim > 0 ? (Math.random()-0.5)*4 : 0;
  ctx.save();
  ctx.translate(px2+p.width/2+hitOffset, p.y+p.height/2);
  if(p.facing === -1) ctx.scale(-1, 1);

  // Buff aura
  if(p.buffAtk > 1) {
    ctx.shadowColor = '#ff2200';
    ctx.shadowBlur = 20;
  }

  // Draw character
  ctx.font = '40px serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(p.icon, 0, 0);
  ctx.shadowBlur = 0;

  // Weapon/attack indicator
  if(p.attackAnim > 0) {
    ctx.font = '22px serif';
    ctx.fillText('💫', 28, -15);
  }
  ctx.restore();
  ctx.globalAlpha = 1;
}

function drawEnemy(e, ex2) {
  const frozenAlpha = e.frozen > 0 ? 0.6 : 1;
  ctx.globalAlpha = frozenAlpha;

  // Shadow
  ctx.fillStyle = 'rgba(0,0,0,0.25)';
  ctx.beginPath();
  ctx.ellipse(ex2+e.width/2, FLOOR_Y+4, e.width*0.45, 5, 0, 0, Math.PI*2);
  ctx.fill();

  ctx.save();
  ctx.translate(ex2+e.width/2, e.y+e.height/2);
  if(e.facing === 1) ctx.scale(-1,1);

  if(e.frozen > 0) { ctx.filter = 'hue-rotate(180deg) brightness(1.5)'; }

  ctx.font = `${e.sz||30}px serif`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(e.icon, 0, 0);
  ctx.filter = 'none';
  ctx.restore();

  // HP bar
  const hpPct = e.hp/e.maxHp;
  const bw = e.width+10, bh = 5;
  ctx.fillStyle = 'rgba(0,0,0,0.6)';
  ctx.fillRect(ex2-5, e.y-10, bw, bh);
  ctx.fillStyle = hpPct>0.5?'#22cc22':hpPct>0.25?'#ccaa00':'#cc2200';
  ctx.fillRect(ex2-5, e.y-10, bw*hpPct, bh);
  ctx.globalAlpha = 1;
}

function drawBoss(b, bx) {
  // Glow
  ctx.shadowColor = '#ff2200';
  ctx.shadowBlur = 30;
  ctx.save();
  ctx.translate(bx+b.width/2, b.y+b.height/2);
  if(b.facing === 1) ctx.scale(-1,1);

  ctx.font = '64px serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  // Phase 2 color
  if(b.phase2) {
    ctx.filter = 'hue-rotate(120deg) brightness(1.3)';
  }

  const icons = ['😈','👹','🐉','💀'];
  ctx.fillText(icons[G.stageIdx%4], 0, 0);
  ctx.filter = 'none';
  ctx.restore();
  ctx.shadowBlur = 0;

  // HP bar above
  const hpPct = b.hp/b.maxHp;
  const bw2 = 80;
  ctx.fillStyle = 'rgba(0,0,0,0.7)';
  ctx.fillRect(bx+b.width/2-40, b.y-14, bw2, 7);
  ctx.fillStyle = hpPct>0.4?'#ff4400':'#ff0000';
  ctx.fillRect(bx+b.width/2-40, b.y-14, bw2*hpPct, 7);

  // Name
  ctx.fillStyle = '#ff8800';
  ctx.font = '600 11px Noto Sans KR';
  ctx.textAlign = 'center';
  ctx.fillText(b.name, bx+b.width/2, b.y-18);
}

function updateHUD() {
  if(!G) return;
  const p = G.player;
  document.getElementById('hp-bar').style.width = Math.max(0,(p.hp/p.maxHp)*100)+'%';
  document.getElementById('mp-bar').style.width = Math.max(0,(p.mp/p.maxMp)*100)+'%';
  document.getElementById('stat-lv').textContent = p.level;
  document.getElementById('stat-kills').textContent = p.kills;
  document.getElementById('stat-score').textContent = p.score;
  document.getElementById('stat-gold').textContent = p.gold;
  document.getElementById('hudName').textContent = p.name;
  document.getElementById('floorBadge').textContent = `${G.stageIdx+1}스테이지`;

  // Skill bar
  const sc = document.getElementById('skills-container');
  sc.innerHTML = '';
  for(let i=0;i<p.skills.length;i++) {
    const sk = p.skills[i];
    const cd = p.skillCds[i];
    const div = document.createElement('div');
    const ready = cd <= 0 && p.mp >= sk.mp;
    div.className = 'skill-slot ' + (ready?'ready':'cooling');
    div.innerHTML = `${sk.icon}<span class="skill-key">${sk.key}</span>`;
    if(cd > 0) {
      const cdDiv = document.createElement('div');
      cdDiv.className = 'skill-cd';
      cdDiv.textContent = Math.ceil(cd/60)+'s';
      div.appendChild(cdDiv);
    }
    div.title = `${sk.name} (MP:${sk.mp}, CD:${sk.cd}s)`;
    sc.appendChild(div);
  }

  // Skill desc
  const desc = document.getElementById('skill-desc');
  desc.innerHTML = p.skills.map(s=>`<b style="color:${s.color}">${s.icon}${s.key}</b>:${s.name}`).join('&nbsp;&nbsp;');
}

function screenShake(amt, dur) {
  G.shakeAmt = amt;
  G.shakeTimer = dur;
}

function stageClear() {
  G.phase = 'clear';
  const p = G.player;
  const elapsed = Math.round((Date.now()-G.startTime)/1000);
  document.getElementById('clearStats').innerHTML = `
    <div>처치 수 <b>${p.kills}</b></div>
    <div>획득 골드 <b>💰${p.gold}</b></div>
    <div>최종 점수 <b>${p.score}</b></div>
    <div>소요 시간 <b>${elapsed}초</b></div>
    <div>레벨 <b>Lv.${p.level}</b></div>
    <div>잔여 HP <b>${p.hp}/${p.maxHp}</b></div>
  `;
  document.getElementById('stageClear').classList.remove('hidden');
}

function gameOver() {
  if(!G || G.phase !== 'play') return;
  G.phase = 'over';
  G.player.alive = false;
  G.player.hp = 0;
  const p = G.player;
  document.getElementById('overStats').innerHTML = `
    <div>처치 수 <b>${p.kills}</b></div>
    <div>획득 골드 <b>💰${p.gold}</b></div>
    <div>최종 점수 <b>${p.score}</b></div>
    <div>레벨 <b>Lv.${p.level}</b></div>
    <div>스테이지 <b>${G.stageIdx+1}</b></div>
    <div>사망 원인 <b>전투 패배</b></div>
  `;
  setTimeout(()=>{
    document.getElementById('gameOver').classList.remove('hidden');
  }, 600);
}

// ── UI ──────────────────────────────────────────────────
function buildCharSelect() {
  const cs = document.getElementById('charSelect');
  cs.innerHTML = CHARACTERS.map(c=>`
    <div class="char-card" id="cc-${c.id}" onclick="selectChar('${c.id}')">
      <span class="char-icon">${c.icon}</span>
      <div class="char-name">${c.name}</div>
      <div class="char-type">${c.type}</div>
      <div style="font-size:0.52rem;color:#666;margin-top:6px;">
        HP ${c.hp} &nbsp; ATK ${c.atk}<br>
        SPD ${c.spd} &nbsp; DEF ${c.def}
      </div>
    </div>`).join('');
}

function selectChar(id) {
  selectedChar = id;
  document.querySelectorAll('.char-card').forEach(c=>c.classList.remove('sel'));
  document.getElementById('cc-'+id)?.classList.add('sel');
  document.getElementById('startBtn').disabled = false;
}

function startGame(stageIdx=0) {
  if(!selectedChar) return;
  document.getElementById('titleScreen').classList.add('hidden');
  document.getElementById('stageClear').classList.add('hidden');
  document.getElementById('gameOver').classList.add('hidden');
  initG(selectedChar, stageIdx);
  document.getElementById('bossHpWrap').classList.remove('show');
  if(animId) cancelAnimationFrame(animId);
  lastTime = performance.now();
  animId = requestAnimationFrame(gameLoop);
}

function nextStage() {
  if(!G) return;
  const nextIdx = (G.stageIdx+1) % STAGES.length;
  document.getElementById('stageClear').classList.add('hidden');
  const prevChar = G.charId;
  selectedChar = prevChar;
  startGame(nextIdx);
}

function retryStage() {
  if(!G) return;
  const idx = G.stageIdx;
  document.getElementById('gameOver').classList.add('hidden');
  startGame(idx);
}

function goTitle() {
  if(animId) cancelAnimationFrame(animId);
  G = null;
  document.getElementById('stageClear').classList.add('hidden');
  document.getElementById('gameOver').classList.add('hidden');
  document.getElementById('titleScreen').classList.remove('hidden');
  document.getElementById('bossHpWrap').classList.remove('show');
  ctx.clearRect(0,0,W,H);
}

// ── KEYBOARD ────────────────────────────────────────────
window.addEventListener('keydown', e => {
  if(!keys[e.key]) {
    keys[e.key] = true;
    justPressed[e.key] = true;
  }
  if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown',' '].includes(e.key)) e.preventDefault();
});
window.addEventListener('keyup', e => {
  keys[e.key] = false;
});

// ── START ────────────────────────────────────────────────
buildCharSelect();
</script>
</body>
</html>
"""

st.set_page_config(page_title="던전 파이터", layout="wide")
st.markdown("""
<style>
.block-container{padding:0!important;max-width:100%!important;}
section[data-testid="stSidebar"]{display:none!important;}
header{display:none!important;}
footer{display:none!important;}
iframe{border:none!important;background:#0a0a12;}
body{background:#0a0a12;}
</style>
""", unsafe_allow_html=True)

components.html(GAME_HTML, height=620, scrolling=False)
