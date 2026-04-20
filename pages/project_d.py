# pages/project_d.py
# 🎲 부루마블 — 울트라 고퀄 보드게임
# 주사위 애니메이션 / 이동 모션 / 집사 멘트 / 집·호텔 / 저당 / 무인도 / 봇 AI

import streamlit as st
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════════
#  FULL GAME HTML (self-contained, injected via components.html)
# ══════════════════════════════════════════════════════════════════════

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>부루마블</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Nanum+Gothic:wght@400;700;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#1a1a2e;font-family:'Nanum Gothic',sans-serif;color:#eee;overflow:hidden}
#bm{width:100%;height:100vh;position:relative;background:#1a1a2e;display:flex;flex-direction:column}

/* ─── Setup Screen ─── */
#setup-screen{
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:100vh;padding:40px 20px;
  background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);
}
.setup-title{
  font-family:'Black Han Sans',sans-serif;font-size:3.2rem;
  color:#e94560;text-shadow:0 0 40px rgba(233,69,96,0.6);
  margin-bottom:6px;letter-spacing:3px;
}
.setup-subtitle{font-size:0.9rem;color:#a8a8b3;margin-bottom:36px;letter-spacing:1px;}
.setup-form{
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:16px;padding:28px;width:100%;max-width:420px;
  backdrop-filter:blur(10px);
}
.form-group{margin-bottom:18px;}
.form-group label{display:block;font-size:0.78rem;color:#a8a8b3;margin-bottom:6px;letter-spacing:0.8px;text-transform:uppercase;}
.form-group input,.form-group select{
  width:100%;background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.15);border-radius:8px;
  color:#eee;padding:10px 14px;font-size:0.9rem;
  font-family:'Nanum Gothic',sans-serif;outline:none;transition:border 0.2s;
}
.form-group input:focus,.form-group select:focus{border-color:#e94560;}
.form-group select option{background:#16213e;}
.start-btn{
  width:100%;background:linear-gradient(135deg,#e94560,#c0392b);
  border:none;border-radius:10px;color:#fff;
  font-size:1.1rem;font-weight:700;font-family:'Black Han Sans',sans-serif;
  padding:15px;cursor:pointer;letter-spacing:3px;
  transition:transform 0.15s,box-shadow 0.2s;
  box-shadow:0 4px 20px rgba(233,69,96,0.45);
  margin-top:8px;
}
.start-btn:hover{transform:translateY(-2px);box-shadow:0 8px 30px rgba(233,69,96,0.65);}
.start-btn:active{transform:scale(0.97);}
.rules-box{
  margin-top:22px;background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.07);border-radius:10px;
  padding:14px 18px;font-size:0.78rem;color:#777;line-height:1.8;
  max-width:420px;width:100%;
}
.rules-box strong{color:#aaa;}

/* ─── Game Screen ─── */
#game-screen{
  display:none;flex-direction:row;height:100vh;
}
.board-area{
  flex:1;padding:8px;display:flex;align-items:center;
  justify-content:center;position:relative;overflow:hidden;
}
#board-svg-wrap{
  width:100%;max-width:520px;aspect-ratio:1;position:relative;
}
#board-svg-wrap svg{width:100%;height:100%;}

/* ─── Side Panel ─── */
.side-panel{
  width:220px;background:#0f0f1a;
  border-left:1px solid rgba(255,255,255,0.07);
  display:flex;flex-direction:column;overflow:hidden;
}
.panel-section{
  padding:10px 12px;
  border-bottom:1px solid rgba(255,255,255,0.06);
  flex-shrink:0;
}
.panel-section h4{
  font-size:0.65rem;letter-spacing:1.5px;color:#555;
  text-transform:uppercase;margin-bottom:8px;
}
.player-row{
  display:flex;align-items:center;gap:7px;padding:5px 0;
  border-radius:6px;transition:background 0.2s;
}
.player-row.active-turn{
  background:rgba(233,69,96,0.12);
  margin:0 -6px;padding:5px 6px;
}
.player-dot{width:9px;height:9px;border-radius:50%;flex-shrink:0;}
.player-name{flex:1;font-size:0.77rem;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.player-money{font-size:0.73rem;color:#2ecc71;font-weight:700;white-space:nowrap;}
.player-jail{font-size:0.62rem;color:#e74c3c;margin-left:2px;}
.player-bankrupt{opacity:0.3;text-decoration:line-through;}

/* ─── Action Area ─── */
.action-area{
  flex:1;padding:10px 12px;display:flex;
  flex-direction:column;gap:6px;overflow-y:auto;
}
.action-area::-webkit-scrollbar{width:3px;}
.action-area::-webkit-scrollbar-track{background:transparent;}
.action-area::-webkit-scrollbar-thumb{background:#333;}

.dice-display{
  display:flex;justify-content:center;align-items:center;
  gap:14px;padding:8px 0;
}
.die{
  width:46px;height:46px;
  background:linear-gradient(145deg,#f5f5f5,#ddd);
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  font-size:1.8rem;
  box-shadow:0 4px 14px rgba(0,0,0,0.5),inset 0 1px 2px rgba(255,255,255,0.8);
  transition:transform 0.1s,box-shadow 0.3s;
  color:#1a1a2e;border:1px solid rgba(0,0,0,0.12);
  user-select:none;
}
.die.rolling{animation:diceRoll 0.65s ease-out;}
@keyframes diceRoll{
  0%  {transform:rotate(0deg) scale(1);}
  15% {transform:rotate(-18deg) scale(1.12) translateY(-5px);}
  30% {transform:rotate(12deg) scale(1.18) translateY(-10px);}
  50% {transform:rotate(-10deg) scale(1.14) translateY(-6px);}
  70% {transform:rotate(6deg) scale(1.08) translateY(-2px);}
  85% {transform:rotate(-3deg) scale(1.03);}
  100%{transform:rotate(0deg) scale(1);}
}
.die.double-glow{
  box-shadow:0 0 18px rgba(255,215,0,0.9),0 4px 14px rgba(0,0,0,0.5);
  border-color:gold;
}

/* ─── Buttons ─── */
.btn{
  border:none;border-radius:8px;padding:9px 14px;
  font-size:0.78rem;font-weight:700;
  font-family:'Nanum Gothic',sans-serif;
  cursor:pointer;transition:all 0.15s;
  letter-spacing:0.5px;white-space:nowrap;
}
.btn:active{transform:scale(0.96);}
.btn:disabled{opacity:0.3;cursor:not-allowed;transform:none!important;}
.btn-primary{
  background:linear-gradient(135deg,#e94560,#c0392b);color:#fff;
  box-shadow:0 3px 12px rgba(233,69,96,0.35);
}
.btn-primary:hover:not(:disabled){
  box-shadow:0 5px 20px rgba(233,69,96,0.55);transform:translateY(-1px);
}
.btn-secondary{
  background:rgba(255,255,255,0.09);color:#ddd;
  border:1px solid rgba(255,255,255,0.12);
}
.btn-secondary:hover:not(:disabled){background:rgba(255,255,255,0.16);}
.btn-success{
  background:linear-gradient(135deg,#27ae60,#1e8449);color:#fff;
  box-shadow:0 3px 10px rgba(39,174,96,0.3);
}
.btn-success:hover:not(:disabled){box-shadow:0 5px 16px rgba(39,174,96,0.5);transform:translateY(-1px);}
.btn-warning{
  background:linear-gradient(135deg,#f39c12,#d68910);color:#fff;
  box-shadow:0 3px 10px rgba(243,156,18,0.3);
}
.btn-warning:hover:not(:disabled){box-shadow:0 5px 16px rgba(243,156,18,0.5);transform:translateY(-1px);}
.btn-full{width:100%;}

/* ─── Card Popup ─── */
.card-popup{
  background:linear-gradient(135deg,#1c1a30,#16213e);
  border:1px solid rgba(255,215,0,0.35);
  border-radius:10px;padding:12px;text-align:center;
  animation:cardPop 0.4s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes cardPop{
  from{transform:scale(0.75) translateY(12px);opacity:0;}
  to{transform:scale(1) translateY(0);opacity:1;}
}
.card-popup .card-emoji{font-size:1.6rem;margin-bottom:4px;}
.card-popup .card-text{font-weight:700;font-size:0.85rem;color:#f0e6a0;margin-bottom:2px;}
.card-popup .card-effect{font-size:0.72rem;color:#a0c4ff;}

/* ─── Info / jail msg ─── */
.info-msg{
  background:rgba(52,152,219,0.12);
  border:1px solid rgba(52,152,219,0.25);
  border-radius:8px;padding:7px 10px;
  font-size:0.76rem;color:#a0c4ff;text-align:center;
}

/* ─── Jail buttons ─── */
.jail-btns{display:flex;gap:6px;}
.jail-btns .btn{flex:1;font-size:0.7rem;padding:7px 4px;}

/* ─── Turn label ─── */
.turn-label{
  font-size:0.7rem;color:#888;text-align:center;padding:2px 0 4px;
}

/* ─── Phase badge ─── */
.phase-badge{
  text-align:center;font-size:0.67rem;letter-spacing:1px;
  padding:3px;color:#555;
}

/* ─── Build / Mortgage ─── */
.expand-btn{
  background:none;border:1px solid rgba(255,255,255,0.1);
  border-radius:6px;color:#777;font-size:0.68rem;padding:4px 8px;
  cursor:pointer;font-family:'Nanum Gothic',sans-serif;width:100%;
  transition:all 0.2s;text-align:left;
}
.expand-btn:hover{background:rgba(255,255,255,0.05);color:#bbb;}
.build-section{overflow:hidden;max-height:0;transition:max-height 0.3s ease;}
.build-section.open{max-height:220px;}
.build-list{max-height:210px;overflow-y:auto;padding-right:2px;}
.build-list::-webkit-scrollbar{width:2px;}
.build-list::-webkit-scrollbar-thumb{background:#333;}
.build-item{
  display:flex;align-items:center;gap:4px;padding:4px 0;
  border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.7rem;
}
.build-item:last-child{border:none;}
.build-item-name{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.build-item-btns{display:flex;gap:2px;flex-shrink:0;}
.mini-btn{
  padding:3px 5px;font-size:0.6rem;border-radius:4px;border:none;
  cursor:pointer;font-family:'Nanum Gothic',sans-serif;font-weight:700;
  transition:all 0.15s;white-space:nowrap;
}
.mini-btn:disabled{opacity:0.25;cursor:not-allowed;}
.mini-btn:active:not(:disabled){transform:scale(0.93);}
.mini-btn-build{background:#27ae60;color:#fff;}
.mini-btn-build:hover:not(:disabled){background:#2ecc71;}
.mini-btn-mort{background:#c0392b;color:#fff;}
.mini-btn-mort:hover:not(:disabled){background:#e74c3c;}
.mini-btn-unmort{background:#2980b9;color:#fff;}
.mini-btn-unmort:hover:not(:disabled){background:#3498db;}
.color-dot{width:7px;height:7px;border-radius:1px;flex-shrink:0;}
.h-dot{
  width:5px;height:5px;background:#27ae60;
  border-radius:1px;display:inline-block;margin-right:1px;
}
.hotel-icon{
  width:9px;height:7px;background:#e74c3c;
  border-radius:1px;display:inline-block;
}

/* ─── Log ─── */
.log-section{
  padding:0 12px 8px;flex:1;overflow:hidden;display:flex;flex-direction:column;min-height:0;
}
.log-section h4{
  font-size:0.65rem;letter-spacing:1.5px;color:#555;
  text-transform:uppercase;margin:8px 0 5px;flex-shrink:0;
}
.log-area{overflow-y:auto;flex:1;}
.log-area::-webkit-scrollbar{width:3px;}
.log-area::-webkit-scrollbar-thumb{background:#333;}
.log-entry{
  font-size:0.68rem;padding:3px 0;
  border-bottom:1px solid rgba(255,255,255,0.03);
  color:#888;line-height:1.4;
}
.log-entry:last-child{border:none;}
.log-entry.gain{color:#27ae60;}
.log-entry.lose{color:#c0392b;}
.log-entry.important{color:#f39c12;font-weight:700;}
.log-entry.move{color:#3498db;}

/* ─── Butler Bubble ─── */
#butler-bubble{
  position:absolute;bottom:14px;left:14px;
  background:rgba(10,10,25,0.94);
  border:1px solid rgba(233,69,96,0.4);
  border-radius:10px;padding:9px 13px;
  font-size:0.73rem;max-width:210px;z-index:50;
  display:none;animation:bubblePop 0.3s ease-out;
  line-height:1.55;pointer-events:none;
  box-shadow:0 4px 20px rgba(0,0,0,0.5);
}
@keyframes bubblePop{
  from{transform:translateY(10px);opacity:0;}
  to{transform:translateY(0);opacity:1;}
}
.butler-name{color:#e94560;font-weight:700;margin-bottom:3px;font-size:0.68rem;letter-spacing:0.5px;}

/* ─── Game Over ─── */
#gameover-screen{
  display:none;position:fixed;inset:0;
  background:rgba(8,8,18,0.96);z-index:200;
  flex-direction:column;align-items:center;justify-content:center;
  padding:30px;text-align:center;
}
.winner-title{
  font-family:'Black Han Sans',sans-serif;font-size:2.8rem;
  color:#f39c12;
  text-shadow:0 0 50px rgba(243,156,18,0.7);
  animation:winnerPop 0.9s cubic-bezier(0.34,1.56,0.64,1);
  margin-bottom:8px;
}
@keyframes winnerPop{
  from{transform:scale(0.4) rotate(-5deg);opacity:0;}
  to{transform:scale(1) rotate(0);opacity:1;}
}
.winner-sub{font-size:0.88rem;color:#a8a8b3;margin-bottom:26px;letter-spacing:1px;}
.rank-list{
  background:rgba(255,255,255,0.04);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:14px;padding:18px;
  width:100%;max-width:340px;margin-bottom:28px;
}
.rank-row{
  display:flex;align-items:center;gap:12px;
  padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.06);
  font-size:0.85rem;
}
.rank-row:last-child{border:none;}
.rank-medal{font-size:1.2rem;min-width:28px;}
.rank-name{flex:1;font-weight:700;}
.rank-money{color:#2ecc71;font-weight:700;}
.rank-bankrupt{color:#e74c3c;font-size:0.73rem;}
</style>
</head>
<body>
<div id="bm">

  <!-- ════ SETUP SCREEN ════ -->
  <div id="setup-screen">
    <div class="setup-title">🎲 부루마블</div>
    <div class="setup-subtitle">효민 월드 — 봇 AI · 집·호텔 · 저당 · 무인도</div>
    <div class="setup-form">
      <div class="form-group">
        <label>내 이름</label>
        <input id="inp-name" value="플레이어" maxlength="8">
      </div>
      <div class="form-group">
        <label>봇 수</label>
        <select id="inp-bots">
          <option value="1">봇 1명 (2인 게임)</option>
          <option value="2" selected>봇 2명 (3인 게임)</option>
          <option value="3">봇 3명 (4인 게임)</option>
        </select>
      </div>
      <div class="form-group">
        <label>봇 난이도</label>
        <select id="inp-diff">
          <option value="easy">🟢 쉬움 — 무작위 행동</option>
          <option value="normal" selected>🟡 보통 — 상황 판단</option>
          <option value="hard">🔴 어려움 — 공격적 전략</option>
        </select>
      </div>
      <button class="start-btn" onclick="startGame()">🎲 게임 시작!</button>
    </div>
    <div class="rules-box">
      <strong>게임 규칙 요약</strong><br>
      시작 자금: <strong>8,000</strong> · 출발 통과: <strong>+200</strong><br>
      독점 시 통행료 2배 · 집/호텔 건설로 최대 80배<br>
      무인도 탈출: 더블 또는 보석금 <strong>500</strong><br>
      저당: 매입가 50% 환급 · 해제 시 60% 납부<br>
      철도 보유수에 따라 통행료 ×1~4배
    </div>
  </div>

  <!-- ════ GAME SCREEN ════ -->
  <div id="game-screen">
    <div class="board-area">
      <div id="board-svg-wrap"></div>
      <div id="butler-bubble">
        <div class="butler-name">🎩 집사</div>
        <span id="butler-text"></span>
      </div>
    </div>
    <div class="side-panel">
      <div class="panel-section">
        <h4>플레이어</h4>
        <div id="players-list"></div>
      </div>
      <div class="action-area" id="action-area"></div>
      <div class="log-section">
        <h4>게임 로그</h4>
        <div class="log-area" id="log-area"></div>
      </div>
    </div>
  </div>

  <!-- ════ GAME OVER SCREEN ════ -->
  <div id="gameover-screen">
    <div id="winner-title" class="winner-title"></div>
    <div class="winner-sub">최후의 승자가 결정되었습니다</div>
    <div class="rank-list" id="rank-list"></div>
    <button class="btn btn-primary" onclick="resetGame()"
      style="padding:14px 50px;font-size:1.05rem;letter-spacing:3px;">
      🔄 다시 하기
    </button>
  </div>

</div>

<script>
// ══════════════════════════════════════════════════════════
//  DATA DEFINITIONS
// ══════════════════════════════════════════════════════════
const CELLS=[
  {name:"출발",    type:"go",     price:0,    rent:0,   group:-1, color:""},
  {name:"서울",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"부산",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"소득세",  type:"tax",    price:200,  rent:0,   group:-1, color:""},
  {name:"철도A",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"인천",    type:"prop",   price:800,  rent:80,  group:1,  color:"#8e44ad"},
  {name:"운명",    type:"fate",   price:0,    rent:0,   group:-1, color:""},
  {name:"대전",    type:"prop",   price:800,  rent:80,  group:1,  color:"#8e44ad"},
  {name:"제주",    type:"prop",   price:900,  rent:90,  group:1,  color:"#8e44ad"},
  {name:"여행",    type:"visit",  price:0,    rent:0,   group:-1, color:""},
  {name:"광주",    type:"prop",   price:1000, rent:100, group:2,  color:"#d35400"},
  {name:"전기",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"울산",    type:"prop",   price:1000, rent:100, group:2,  color:"#d35400"},
  {name:"대구",    type:"prop",   price:1100, rent:110, group:2,  color:"#d35400"},
  {name:"철도B",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"수원",    type:"prop",   price:1200, rent:120, group:3,  color:"#c0392b"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"고양",    type:"prop",   price:1300, rent:130, group:3,  color:"#c0392b"},
  {name:"성남",    type:"prop",   price:1400, rent:140, group:3,  color:"#c0392b"},
  {name:"무인도",  type:"jail",   price:0,    rent:0,   group:-1, color:""},
  {name:"청주",    type:"prop",   price:1400, rent:140, group:4,  color:"#27ae60"},
  {name:"운명",    type:"fate",   price:0,    rent:0,   group:-1, color:""},
  {name:"전주",    type:"prop",   price:1500, rent:150, group:4,  color:"#27ae60"},
  {name:"춘천",    type:"prop",   price:1600, rent:160, group:4,  color:"#27ae60"},
  {name:"철도C",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"강릉",    type:"prop",   price:1600, rent:160, group:5,  color:"#2980b9"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"원주",    type:"prop",   price:1700, rent:170, group:5,  color:"#2980b9"},
  {name:"속초",    type:"prop",   price:1800, rent:180, group:5,  color:"#2980b9"},
  {name:"무료주차",type:"free",   price:0,    rent:0,   group:-1, color:""},
  {name:"평택",    type:"prop",   price:1800, rent:180, group:6,  color:"#e74c3c"},
  {name:"운명",    type:"fate",   price:0,    rent:0,   group:-1, color:""},
  {name:"천안",    type:"prop",   price:1900, rent:190, group:6,  color:"#e74c3c"},
  {name:"아산",    type:"prop",   price:2000, rent:200, group:6,  color:"#e74c3c"},
  {name:"철도D",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"파주",    type:"prop",   price:2200, rent:220, group:7,  color:"#f39c12"},
  {name:"가스",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"김포",    type:"prop",   price:2200, rent:220, group:7,  color:"#f39c12"},
  {name:"사치세",  type:"tax",    price:300,  rent:0,   group:-1, color:""},
];

const GRP_SIZE={0:2,1:3,2:3,3:3,4:3,5:3,6:3,7:2};
const BUILD_COST={0:200,1:250,2:300,3:350,4:350,5:400,6:400,7:500};
const RENT_MULT=[1,5,15,45,80];
const PCOLORS=["#e74c3c","#3498db","#2ecc71","#f39c12"];
const PTOKENS=["▲","●","◆","★"];
const BOT_NAMES=["봇 알파","봇 베타","봇 감마"];
const JAIL_BAIL=500, START_MONEY=8000, PASS_GO=200;
const MORT_RATE=0.5, UNMORT_RATE=0.6;
const DICE_FACES=["⚀","⚁","⚂","⚃","⚄","⚅"];

// ── 찬스 카드 ──────────────────────────────────────────────
const CHANCE_CARDS=[
  {emoji:"💰",text:"은행 배당금",      type:"money",amount:100},
  {emoji:"📋",text:"세금 환급",         type:"money",amount:150},
  {emoji:"🎂",text:"생일선물! 각자 50씩",type:"birthday",amount:50},
  {emoji:"🔧",text:"수리비 청구",       type:"money",amount:-100},
  {emoji:"🏥",text:"의료비 청구",       type:"money",amount:-150},
  {emoji:"📚",text:"학교 수업료",       type:"money",amount:-200},
  {emoji:"📈",text:"투자 수익",         type:"money",amount:200},
  {emoji:"🚩",text:"출발점으로! +200",  type:"goto",target:0},
  {emoji:"🔒",text:"무인도로 이동!",    type:"goto_jail"},
  {emoji:"⬅️",text:"뒤로 3칸",         type:"move",amount:-3},
  {emoji:"➡️",text:"앞으로 6칸",        type:"move",amount:6},
  {emoji:"🚂",text:"가장 가까운 철도로",type:"nearest_rail"},
  {emoji:"🔨",text:"집 40·호텔 115 납부",type:"repair"},
  {emoji:"🏦",text:"은행 오류! +500",   type:"money",amount:500},
];

// ── 운명 카드 ──────────────────────────────────────────────
const FATE_CARDS=[
  {emoji:"🎫",text:"복권 당첨! +300",   type:"money",amount:300},
  {emoji:"🚦",text:"과태료 -50",         type:"money",amount:-50},
  {emoji:"💊",text:"보험금 수령 +100",   type:"money",amount:100},
  {emoji:"🚗",text:"자동차 수리비 -100", type:"money",amount:-100},
  {emoji:"🎵",text:"콘서트 수익 +150",   type:"money",amount:150},
  {emoji:"✈️",text:"여행 경비 -100",     type:"money",amount:-100},
  {emoji:"🚩",text:"출발점으로! +200",   type:"goto",target:0},
  {emoji:"🔒",text:"무인도로 이동!",     type:"goto_jail"},
  {emoji:"➡️",text:"앞으로 3칸",         type:"move",amount:3},
  {emoji:"🎂",text:"각자 50씩 받기",     type:"birthday",amount:50},
  {emoji:"💸",text:"탈세 적발 -200",     type:"money",amount:-200},
  {emoji:"🏦",text:"은행 이자 +200",     type:"money",amount:200},
];

// ── 집사 멘트 ──────────────────────────────────────────────
const BUTLER_MSGS={
  buy:    ["마음에 드시는 부동산이군요, 주인님.","투자하시겠습니까, 주인님?","좋은 선택이 될 것 같습니다.","현명한 투자입니다, 주인님!"],
  pass:   ["다음 기회를 노리시는군요.","현명한 판단이십니다, 주인님.","자금을 아끼는 것도 전략입니다.","때를 기다리십시오, 주인님."],
  rent:   ["통행료를 받으셨습니다, 주인님!","수익이 들어왔습니다. 훌륭해요!","당신의 부동산이 일하고 있습니다.","멋진 수입이군요, 주인님!"],
  pay_rent:["안타깝습니다, 주인님.","통행료를 납부하셨습니다.","이런, 조심하셔야겠습니다.","다음엔 피해 가시길 바랍니다."],
  jail:   ["무인도로 가셔야겠습니다...","안타깝게도 구금되셨군요.","탈출 방법을 찾아드리겠습니다.","걱정 마세요, 곧 나오실 겁니다."],
  chance: ["찬스 카드입니다! 행운을 빕니다!","무엇이 나올지 모릅니다, 주인님.","좋은 소식이 오길 바랍니다!"],
  fate:   ["운명 카드입니다. 두근두근!","운명은 아무도 모르지요.","무엇이든 받아들이십시오, 주인님."],
  bankrupt:["파산하셨습니다...괜찮으세요?","이런 결과가 나오다니 유감입니다.","다음 게임엔 반드시 이기실 겁니다!"],
  double: ["더블입니다! 한 번 더 굴리세요!","연속 이동의 기회입니다, 주인님!","행운이 따르는군요, 주인님!"],
  build:  ["건설을 완료했습니다, 주인님!","수익이 오를 것입니다. 훌륭해요!","이제 통행료가 올라갑니다!"],
  win:    ["축하드립니다, 주인님! 최고이십니다!","당신의 승리입니다! 만세!","역시 주인님이십니다!"],
  triple: ["3연속 더블! 무인도로 가십시오!","너무 과하셨습니다, 주인님..."],
  go_pass:["출발점을 통과하셨습니다! +200","통과 보너스입니다, 주인님!"],
};

// ══════════════════════════════════════════════════════════
//  BUTLER
// ══════════════════════════════════════════════════════════
let butlerTimer=null;
function butlerSay(category){
  const msgs=BUTLER_MSGS[category]||["..."];
  const msg=msgs[Math.floor(Math.random()*msgs.length)];
  const bb=document.getElementById('butler-bubble');
  const bt=document.getElementById('butler-text');
  if(!bb||!bt)return;
  bt.textContent=msg;
  bb.style.display='block';
  if(butlerTimer)clearTimeout(butlerTimer);
  butlerTimer=setTimeout(()=>{bb.style.display='none';},3000);
}

// ══════════════════════════════════════════════════════════
//  GAME STATE
// ══════════════════════════════════════════════════════════
let G=null;

function freshCells(){
  return CELLS.map(c=>({...c,owner:null,houses:0,mortgaged:false}));
}

function initGame(name,botCount,diff){
  const players=[{
    name,money:START_MONEY,pos:0,
    color:PCOLORS[0],token:PTOKENS[0],
    is_bot:false,bankrupt:false,jail_turns:0,jail_free:0
  }];
  for(let i=0;i<botCount;i++)
    players.push({
      name:BOT_NAMES[i],money:START_MONEY,pos:0,
      color:PCOLORS[i+1],token:PTOKENS[i+1],
      is_bot:true,bankrupt:false,jail_turns:0,jail_free:0
    });
  return{
    players,cells:freshCells(),
    turn:0,doubles:0,phase:'roll',
    log:[],diff,
    pending_card:null,winner:null,
    d1:1,d2:2,animating:false
  };
}

function addLog(msg,style=''){
  G.log.unshift({msg,style});
  if(G.log.length>80)G.log=G.log.slice(0,80);
}

function alive(){return G.players.filter(p=>!p.bankrupt);}

function checkWinner(){
  const a=alive();
  if(a.length===1){G.winner=a[0].name;G.phase='gameover';return true;}
  return false;
}

function ownsGroup(pidx,group){
  if(group<0)return false;
  const total=GRP_SIZE[group]||0;
  return G.cells.filter(c=>c.group===group&&c.owner===pidx).length===total;
}

function calcRent(ci,roll=0){
  const c=G.cells[ci];
  if(c.owner===null||c.mortgaged)return 0;
  const{type,owner,houses,rent,group}=c;
  if(type==='prop'){
    const h=Math.min(houses,4);
    if(h===0&&ownsGroup(owner,group))return rent*2;
    return rent*RENT_MULT[h];
  }
  if(type==='rail'){
    const n=G.cells.filter(c2=>c2.type==='rail'&&c2.owner===owner).length;
    return 100*n;
  }
  if(type==='util'){
    const n=G.cells.filter(c2=>c2.type==='util'&&c2.owner===owner).length;
    const r=roll||Math.floor(Math.random()*11)+2;
    return r*(n===1?4:10);
  }
  return 0;
}

function nearestRailIdx(pos){
  const rails=[5,15,25,35];
  return rails.reduce((b,r)=>((r-pos+40)%40)<((b-pos+40)%40)?r:b);
}

// ── Move ───────────────────────────────────────────────────
function movePlayer(pidx,steps){
  const p=G.players[pidx];
  const old=p.pos;
  const nw=(old+steps+40)%40;
  if(steps>0&&nw<old){
    p.money+=PASS_GO;
    addLog(`🚩 ${p.name} 출발 통과! +${PASS_GO}`,'gain');
    butlerSay('go_pass');
  }
  p.pos=nw;
}

function sendToJail(pidx){
  const p=G.players[pidx];
  p.pos=20;p.jail_turns=3;
  addLog(`🔒 ${p.name} 무인도로!`,'lose');
  butlerSay('jail');
}

// ── Pay rent ──────────────────────────────────────────────
function payRent(fromIdx,toIdx,amt,name){
  const pay=G.players[fromIdx],rec=G.players[toIdx];
  const actual=Math.min(amt,Math.max(0,pay.money));
  pay.money-=actual;rec.money+=actual;
  addLog(`💸 ${pay.name}→${rec.name} 통행료 ${actual} (${name})`,'lose');
  butlerSay(fromIdx===0?'pay_rent':'rent');
  maybeBankrupt(fromIdx);
}

// ── Bankrupt ──────────────────────────────────────────────
function maybeBankrupt(pidx){
  const p=G.players[pidx];
  if(p.money>=0)return;
  // 긴급 저당
  for(let ci=0;ci<G.cells.length;ci++){
    const c=G.cells[ci];
    if(c.owner===pidx&&!c.mortgaged&&c.houses===0&&p.money<0){
      const val=Math.floor(c.price*MORT_RATE);
      c.mortgaged=true;p.money+=val;
      addLog(`📋 ${p.name} ${c.name} 긴급저당 +${val}`,'lose');
    }
  }
  if(p.money<0){
    p.bankrupt=true;p.money=0;
    G.cells.forEach(c=>{
      if(c.owner===pidx){c.owner=null;c.houses=0;c.mortgaged=false;}
    });
    addLog(`💀 ${p.name} 파산!`,'important');
    butlerSay('bankrupt');
    checkWinner();
  }
}

function mortgageProp(pidx,ci){
  const c=G.cells[ci];
  if(c.owner!==pidx||c.mortgaged||c.houses>0)return false;
  const val=Math.floor(c.price*MORT_RATE);
  c.mortgaged=true;G.players[pidx].money+=val;
  addLog(`📋 ${G.players[pidx].name} ${c.name} 저당 +${val}`,'lose');
  return true;
}

function unmortgageProp(pidx,ci){
  const c=G.cells[ci];
  if(c.owner!==pidx||!c.mortgaged)return false;
  const cost=Math.floor(c.price*UNMORT_RATE);
  if(G.players[pidx].money<cost)return false;
  c.mortgaged=false;G.players[pidx].money-=cost;
  addLog(`✅ ${G.players[pidx].name} ${c.name} 저당해제 -${cost}`);
  return true;
}

// ── Apply card ────────────────────────────────────────────
function applyCard(pidx,card){
  const p=G.players[pidx];
  const{type,amount,target,text}=card;
  if(type==='money'){
    p.money+=amount;
    addLog(`🃏 ${p.name}: ${text} (${amount>0?'+':''}${amount})`,amount>0?'gain':'lose');
    if(amount<0)maybeBankrupt(pidx);
  }else if(type==='birthday'){
    G.players.forEach((o,i)=>{
      if(i!==pidx&&!o.bankrupt){
        const a=Math.min(amount,Math.max(0,o.money));
        o.money-=a;p.money+=a;
      }
    });
    addLog(`🎂 ${p.name} 생일! 각자 ${amount} 받음`,'gain');
  }else if(type==='goto'){
    if(target===0)p.money+=PASS_GO;
    p.pos=target;
    addLog(`🚀 ${p.name} ${CELLS[target].name}으로!`,'move');
    landCell(pidx,0);return;
  }else if(type==='goto_jail'){
    sendToJail(pidx);
  }else if(type==='move'){
    movePlayer(pidx,amount);
    addLog(`👣 ${p.name} ${amount>0?'+':''}${amount}칸`,'move');
    landCell(pidx,0);return;
  }else if(type==='nearest_rail'){
    const nr=nearestRailIdx(p.pos);
    const steps=(nr-p.pos+40)%40||40;
    movePlayer(pidx,steps);
    addLog(`🚂 ${p.name} 철도로!`,'move');
    landCell(pidx,0);return;
  }else if(type==='repair'){
    const h=G.cells.filter(c=>c.owner===pidx&&c.houses>0&&c.houses<4).length;
    const ht=G.cells.filter(c=>c.owner===pidx&&c.houses===4).length;
    const cost=h*40+ht*115;
    p.money-=cost;
    addLog(`🔧 ${p.name} 수리비 -${cost} (집${h}/호텔${ht})`,'lose');
    maybeBankrupt(pidx);
  }
  if(G.phase!=='gameover')G.phase='roll';
}

// ── Land cell ─────────────────────────────────────────────
function landCell(pidx,roll){
  const p=G.players[pidx];
  const ci=p.pos;
  const c=G.cells[ci];
  addLog(`📍 ${p.name} → ${c.name}`,'move');
  if(c.type==='go'){
    p.money+=PASS_GO;
    addLog(`🎉 출발 착지! +${PASS_GO}`,'gain');
  }else if(['prop','rail','util'].includes(c.type)){
    const owner=c.owner;
    if(owner===null){G.phase='buy';return;}
    else if(owner===pidx){addLog('🏠 자기 소유지');}
    else{
      if(c.mortgaged)addLog(`📋 ${c.name} 저당 중`);
      else{const rent=calcRent(ci,roll);payRent(pidx,owner,rent,c.name);}
    }
    checkWinner();
  }else if(c.type==='chance'||c.type==='fate'){
    const pool=c.type==='chance'?CHANCE_CARDS:FATE_CARDS;
    G.pending_card=pool[Math.floor(Math.random()*pool.length)];
    G.phase='card';
    butlerSay(c.type);
    return;
  }else if(c.type==='tax'){
    p.money-=c.price;
    addLog(`💸 ${p.name} 세금 -${c.price}`,'lose');
    maybeBankrupt(pidx);
  }else if(c.type==='jail'){
    sendToJail(pidx);
  }else{
    addLog(`✅ ${c.name}`);
  }
  if(G.phase!=='gameover')G.phase='roll';
}

// ── Advance turn ──────────────────────────────────────────
function advanceTurn(){
  if(G.phase==='gameover')return;
  const n=G.players.length;
  let nxt=(G.turn+1)%n,att=0;
  while(G.players[nxt].bankrupt&&att<n){nxt=(nxt+1)%n;att++;}
  G.turn=nxt;G.phase='roll';
}

// ══════════════════════════════════════════════════════════
//  BOT AI
// ══════════════════════════════════════════════════════════
function botThink(pidx){
  const p=G.players[pidx];
  const diff=G.diff;

  if(G.phase==='buy'){
    const ci=p.pos,cell=G.cells[ci],price=cell.price;
    let buy=false;
    if(diff==='easy'){
      buy=Math.random()>0.35&&p.money>=price;
    }else if(diff==='normal'){
      buy=p.money>=price*1.5;
    }else{
      const g=cell.group;
      if(g>=0){
        const need=GRP_SIZE[g]||0;
        const have=G.cells.filter(c=>c.group===g&&c.owner===pidx).length;
        if(have===need-1&&p.money>=price)buy=true;
        else buy=p.money>=price*1.2;
      }else buy=p.money>=price;
    }
    if(buy){
      cell.owner=pidx;p.money-=price;
      addLog(`🏠 ${p.name} ${cell.name} 매입 -${price}`,'lose');
    }else{
      addLog(`↩️ ${p.name} ${cell.name} 패스`);
    }
    G.phase='roll';return;
  }

  if(G.phase==='card'){
    if(G.pending_card){applyCard(pidx,G.pending_card);G.pending_card=null;}
    return;
  }

  // hard 봇 건설 로직
  if(diff==='hard'){
    G.cells.forEach((c,ci)=>{
      if(c.owner!==pidx||c.type!=='prop')return;
      if(!ownsGroup(pidx,c.group)||c.houses>=4||c.mortgaged)return;
      const cost=BUILD_COST[c.group]||300;
      if(p.money>=cost*1.3){
        c.houses++;p.money-=cost;
        const lbl=c.houses===4?'호텔 🏨':`집 ${c.houses}채`;
        addLog(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
        butlerSay('build');
      }
    });
  }
}

// ══════════════════════════════════════════════════════════
//  ANIMATION HELPERS
// ══════════════════════════════════════════════════════════
function rollDice(){
  const d1=Math.floor(Math.random()*6)+1;
  const d2=Math.floor(Math.random()*6)+1;
  return{d1,d2,total:d1+d2,isDouble:d1===d2};
}

function animateDice(d1,d2,cb){
  const el1=document.getElementById('die1');
  const el2=document.getElementById('die2');
  if(!el1||!el2){if(cb)cb();return;}
  el1.classList.add('rolling');el2.classList.add('rolling');
  let frames=0;
  const interval=setInterval(()=>{
    el1.textContent=DICE_FACES[Math.floor(Math.random()*6)];
    el2.textContent=DICE_FACES[Math.floor(Math.random()*6)];
    frames++;
    if(frames>=10){
      clearInterval(interval);
      el1.textContent=DICE_FACES[d1-1];
      el2.textContent=DICE_FACES[d2-1];
      el1.classList.remove('rolling');el2.classList.remove('rolling');
      if(d1===d2){el1.classList.add('double-glow');el2.classList.add('double-glow');}
      else{el1.classList.remove('double-glow');el2.classList.remove('double-glow');}
      if(cb)cb();
    }
  },70);
}

function animateMove(pidx,from,to,cb){
  if(from===to){if(cb)cb();return;}
  const steps=[];
  let cur=from;
  while(cur!==to){cur=(cur+1)%40;steps.push(cur);}
  let i=0;
  const interval=setInterval(()=>{
    G.players[pidx].pos=steps[i];
    renderBoard();
    i++;
    if(i>=steps.length){clearInterval(interval);if(cb)cb();}
  },110);
}

// ══════════════════════════════════════════════════════════
//  PLAYER ACTIONS (human)
// ══════════════════════════════════════════════════════════
function doPlayerRoll(){
  if(!G||G.animating)return;
  G.animating=true;
  const{d1,d2,total,isDouble}=rollDice();
  G.d1=d1;G.d2=d2;
  renderAll();
  animateDice(d1,d2,()=>{
    if(isDouble){
      G.doubles++;
      if(G.doubles>=3){
        addLog(`3연속 더블! ${G.players[G.turn].name} 무인도!`,'important');
        butlerSay('triple');
        sendToJail(G.turn);G.doubles=0;
        advanceTurn();G.animating=false;renderAll();
        setTimeout(checkBotTurn,500);return;
      }
      addLog(`🎲 더블! (${d1}+${d2})`);
      butlerSay('double');
    }else{
      G.doubles=0;
      addLog(`🎲 ${d1}+${d2}=${total}`);
    }
    const from=G.players[G.turn].pos;
    renderAll();
    setTimeout(()=>{
      animateMove(G.turn,from,(from+total)%40,()=>{
        movePlayer(G.turn,total);
        landCell(G.turn,total);
        G.animating=false;
        if(!isDouble&&G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover')
          advanceTurn();
        renderAll();
        if(G.phase==='gameover')showGameOver();
      });
    },150);
  });
}

function doPlayerBuy(buy){
  const pidx=G.turn,ci=G.players[pidx].pos,cell=G.cells[ci];
  if(buy){
    cell.owner=pidx;G.players[pidx].money-=cell.price;
    addLog(`🏠 ${G.players[pidx].name} ${cell.name} 매입 -${cell.price}`,'lose');
    butlerSay('buy');
  }else{
    addLog(`↩️ ${G.players[pidx].name} ${cell.name} 패스`);
    butlerSay('pass');
  }
  G.phase='roll';advanceTurn();renderAll();
  setTimeout(checkBotTurn,400);
}

function doPlayerCard(){
  if(!G||!G.pending_card)return;
  applyCard(G.turn,G.pending_card);
  G.pending_card=null;
  if(G.phase!=='gameover'){advanceTurn();renderAll();setTimeout(checkBotTurn,400);}
  else{renderAll();showGameOver();}
}

function doPlayerJail(payBail){
  if(!G)return;
  const p=G.players[G.turn];
  if(payBail){
    if(p.money<JAIL_BAIL)return;
    p.money-=JAIL_BAIL;p.jail_turns=0;
    addLog(`💰 ${p.name} 보석금 납부!`,'lose');
    renderAll();
    // 보석 후 바로 주사위
    setTimeout(doPlayerRoll,300);
  }else{
    const{d1,d2,total,isDouble}=rollDice();
    G.d1=d1;G.d2=d2;
    renderAll();
    animateDice(d1,d2,()=>{
      if(isDouble){
        p.jail_turns=0;addLog(`🎉 더블 탈출!`);
        animateMove(G.turn,p.pos,(p.pos+total)%40,()=>{
          movePlayer(G.turn,total);landCell(G.turn,total);
          if(G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover')advanceTurn();
          renderAll();setTimeout(checkBotTurn,500);
        });
      }else{
        p.jail_turns--;
        addLog(`😔 더블 실패 (${p.jail_turns}턴 남음)`);
        if(p.jail_turns<=0){
          p.jail_turns=0;addLog(`${p.name} 강제 석방`);
          animateMove(G.turn,p.pos,(p.pos+total)%40,()=>{
            movePlayer(G.turn,total);landCell(G.turn,total);
            if(G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover')advanceTurn();
            renderAll();setTimeout(checkBotTurn,500);
          });
        }else{advanceTurn();renderAll();setTimeout(checkBotTurn,400);}
      }
    });
  }
}

function doBuild(pidx,ci){
  const c=G.cells[ci],p=G.players[pidx];
  const cost=BUILD_COST[c.group]||300;
  if(p.money<cost)return;
  c.houses++;p.money-=cost;
  const lbl=c.houses===4?'호텔 🏨':`집 ${c.houses}채`;
  addLog(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
  butlerSay('build');
  renderAll();
}

function doMortgage(pidx,ci){mortgageProp(pidx,ci);renderAll();}
function doUnmortgage(pidx,ci){unmortgageProp(pidx,ci);renderAll();}

// ══════════════════════════════════════════════════════════
//  BOT TURN RUNNER
// ══════════════════════════════════════════════════════════
function checkBotTurn(){
  if(!G||G.phase==='gameover')return;
  const p=G.players[G.turn];
  if(p.is_bot&&!p.bankrupt)doBotTurn();
}

function doBotTurn(){
  if(!G||G.phase==='gameover')return;
  const pidx=G.turn;
  const p=G.players[pidx];
  if(!p.is_bot||p.bankrupt)return;

  setTimeout(()=>{
    // 무인도 처리
    if(p.jail_turns>0&&G.phase==='roll'){
      if(G.diff==='hard'&&p.money>=JAIL_BAIL){
        p.money-=JAIL_BAIL;p.jail_turns=0;
        addLog(`💰 ${p.name} 보석금!`,'lose');
        renderAll();
        setTimeout(()=>doBotRoll(pidx),400);
      }else{
        const{d1,d2,total,isDouble}=rollDice();
        G.d1=d1;G.d2=d2;
        if(isDouble){
          p.jail_turns=0;addLog(`🎉 ${p.name} 더블 탈출!`);renderAll();
          setTimeout(()=>{
            animateMove(pidx,p.pos,(p.pos+total)%40,()=>{
              movePlayer(pidx,total);landCell(pidx,total);
              if(G.phase==='buy'||G.phase==='card')botThink(pidx);
              if(G.phase!=='gameover')advanceTurn();
              renderAll();if(G.phase==='gameover')showGameOver();
              else setTimeout(checkBotTurn,500);
            });
          },300);
        }else{
          p.jail_turns--;
          addLog(`😔 ${p.name} 더블 실패`);
          if(p.jail_turns<=0){
            p.jail_turns=0;renderAll();
            setTimeout(()=>{
              animateMove(pidx,p.pos,(p.pos+total)%40,()=>{
                movePlayer(pidx,total);landCell(pidx,total);
                if(G.phase==='buy'||G.phase==='card')botThink(pidx);
                if(G.phase!=='gameover')advanceTurn();
                renderAll();if(G.phase==='gameover')showGameOver();
                else setTimeout(checkBotTurn,500);
              });
            },300);
          }else{
            advanceTurn();renderAll();setTimeout(checkBotTurn,400);
          }
        }
      }
      return;
    }

    if(G.phase==='buy'||G.phase==='card'){
      botThink(pidx);
      if(G.phase!=='gameover')advanceTurn();
      renderAll();if(G.phase==='gameover')showGameOver();
      else setTimeout(checkBotTurn,400);
      return;
    }

    if(G.phase==='roll'){
      botThink(pidx); // 건설 먼저
      doBotRoll(pidx);
    }
  },550);
}

function doBotRoll(pidx){
  if(!G||G.phase==='gameover')return;
  const p=G.players[pidx];
  const{d1,d2,total,isDouble}=rollDice();
  G.d1=d1;G.d2=d2;
  if(isDouble){
    G.doubles++;
    if(G.doubles>=3){
      addLog(`3연속 더블! ${p.name} 무인도!`,'important');
      butlerSay('triple');
      sendToJail(pidx);G.doubles=0;
      advanceTurn();renderAll();setTimeout(checkBotTurn,500);return;
    }
    addLog(`🎲 ${p.name} 더블! (${d1}+${d2})`);
  }else{
    G.doubles=0;
    addLog(`🎲 ${p.name} ${d1}+${d2}=${total}`);
  }
  renderAll();
  const from=p.pos;
  setTimeout(()=>{
    animateMove(pidx,from,(from+total)%40,()=>{
      movePlayer(pidx,total);
      landCell(pidx,total);
      if(G.phase==='buy'||G.phase==='card')botThink(pidx);
      if(!isDouble&&G.phase!=='gameover')advanceTurn();
      renderAll();
      if(G.phase==='gameover')showGameOver();
      else if(isDouble&&G.phase==='roll')
        setTimeout(()=>doBotRoll(pidx),700);
      else
        setTimeout(checkBotTurn,500);
    });
  },200);
}

// ══════════════════════════════════════════════════════════
//  BOARD SVG RENDERER
// ══════════════════════════════════════════════════════════
function getCellCoords(ci){
  const S=500,CR=82,IW=(S-2*CR)/9;
  if(ci===0) return{x:S-CR,y:S-CR,w:CR,h:CR};
  if(ci===10)return{x:0,   y:S-CR,w:CR,h:CR};
  if(ci===20)return{x:0,   y:0,   w:CR,h:CR};
  if(ci===30)return{x:S-CR,y:0,   w:CR,h:CR};
  if(ci<10){  const idx=10-ci;return{x:S-CR-idx*IW,y:S-CR,w:IW,h:CR};}
  if(ci<20){  const idx=ci-10; return{x:0,y:S-CR-idx*IW,w:CR,h:IW};}
  if(ci<30){  const idx=ci-20; return{x:CR+(idx-1)*IW,y:0,w:IW,h:CR};}
  const idx=ci-30;return{x:S-CR,y:CR+(idx-1)*IW,w:CR,h:IW};
}

function cellBg(c){
  if(c.type==='go')    return'#193d28';
  if(c.type==='jail')  return'#2a1845';
  if(c.type==='visit') return'#18354f';
  if(c.type==='free')  return'#193228';
  if(c.type==='chance')return'#281845';
  if(c.type==='fate')  return'#381818';
  if(c.type==='tax')   return'#38281a';
  if(c.type==='rail')  return'#18283a';
  if(c.type==='util')  return'#283a18';
  if(c.mortgaged)      return'#151515';
  return'#1c1f30';
}

function cellIcon(c){
  const m={go:'🚩',jail:'🔒',visit:'✈️',free:'🅿️',chance:'?',fate:'★',tax:'💸',rail:'🚂'};
  if(m[c.type])return m[c.type];
  if(c.type==='util')return c.name==='전기'?'⚡':'🔥';
  return'';
}

function renderBoard(){
  if(!G)return;
  const wrap=document.getElementById('board-svg-wrap');
  if(!wrap)return;
  const S=500,CR=82,IW=(S-2*CR)/9;

  const cellPlayers={};
  G.players.forEach((p,i)=>{
    if(!p.bankrupt)cellPlayers[p.pos]=(cellPlayers[p.pos]||[]).concat(i);
  });

  let svg=`<svg viewBox="0 0 ${S} ${S}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
    <feGaussianBlur stdDeviation="2.5" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="softglow" x="-50%" y="-50%" width="200%" height="200%">
    <feGaussianBlur stdDeviation="4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<rect width="${S}" height="${S}" fill="#0c0c1a" rx="10"/>
<rect x="1" y="1" width="${S-2}" height="${S-2}" fill="none" stroke="#252540" stroke-width="2" rx="9"/>`;

  // ── Draw cells ─────────────────────────────────────────
  G.cells.forEach((c,ci)=>{
    const{x,y,w,h}=getCellCoords(ci);
    const bg=cellBg(c);
    const isCorner=ci===0||ci===10||ci===20||ci===30;
    const owner=c.owner!==null?G.players[c.owner]:null;

    svg+=`<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${bg}" stroke="#252540" stroke-width="0.5"/>`;

    // Color bar
    if(c.color&&c.type==='prop'){
      if(ci<10||ci>=20)
        svg+=`<rect x="${x+0.5}" y="${y+0.5}" width="${w-1}" height="11" fill="${c.color}" opacity="0.8" rx="0"/>`;
      else if(ci<20)
        svg+=`<rect x="${x+w-11}" y="${y+0.5}" width="10" height="${h-1}" fill="${c.color}" opacity="0.8" rx="0"/>`;
      else
        svg+=`<rect x="${x+0.5}" y="${y+h-11}" width="${w-1}" height="11" fill="${c.color}" opacity="0.8" rx="0"/>`;
    }
    if(c.type==='rail'){
      if(ci<10||ci>=20)
        svg+=`<rect x="${x+0.5}" y="${y+0.5}" width="${w-1}" height="9" fill="#1c2d3a" opacity="0.95"/>`;
      else if(ci<20)
        svg+=`<rect x="${x+w-9}" y="${y+0.5}" width="8" height="${h-1}" fill="#1c2d3a" opacity="0.95"/>`;
      else
        svg+=`<rect x="${x+0.5}" y="${y+h-9}" width="${w-1}" height="9" fill="#1c2d3a" opacity="0.95"/>`;
    }

    const icon=cellIcon(c);
    const cx=x+w/2, cy=y+h/2;

    if(isCorner){
      svg+=`<text x="${cx}" y="${cy-6}" text-anchor="middle" font-size="18" fill="#fff" opacity="0.85">${icon}</text>`;
      const nm=c.name;
      svg+=`<text x="${cx}" y="${cy+10}" text-anchor="middle" font-size="7.5" fill="#bbb" font-family="Nanum Gothic,sans-serif">${nm}</text>`;
    }else if(ci<10||ci>=20){
      // horizontal cell
      const midY=y+h/2;
      if(icon)svg+=`<text x="${cx}" y="${midY-6}" text-anchor="middle" font-size="10" fill="#ccc">${icon}</text>`;
      const nm=c.name.length>3?c.name.slice(0,3):c.name;
      svg+=`<text x="${cx}" y="${midY+7}" text-anchor="middle" font-size="7" fill="#aaa" font-family="Nanum Gothic,sans-serif">${nm}</text>`;
      if(c.price>0)
        svg+=`<text x="${cx}" y="${midY+17}" text-anchor="middle" font-size="6" fill="#666" font-family="Nanum Gothic,sans-serif">${c.price}</text>`;
      // houses
      if(c.type==='prop'&&c.houses>0){
        if(c.houses===4){
          svg+=`<rect x="${cx-7}" y="${y+h-14}" width="14" height="9" fill="#c0392b" rx="1" opacity="0.9"/>`;
          svg+=`<text x="${cx}" y="${y+h-7}" text-anchor="middle" font-size="5.5" fill="#fff" font-family="sans-serif">H</text>`;
        }else{
          for(let hh=0;hh<c.houses;hh++)
            svg+=`<rect x="${cx-c.houses*3.5+hh*7}" y="${y+h-12}" width="6" height="7" fill="#27ae60" rx="1" opacity="0.9"/>`;
        }
      }
    }else{
      // vertical cell (left/right sides)
      if(icon)svg+=`<text x="${x+w/2}" y="${cy+4}" text-anchor="middle" font-size="10" fill="#ccc">${icon}</text>`;
      const nm2=c.name.length>3?c.name.slice(0,3):c.name;
      svg+=`<text x="${x+w/2}" y="${cy+16}" text-anchor="middle" font-size="7" fill="#aaa" font-family="Nanum Gothic,sans-serif">${nm2}</text>`;
      // houses
      if(c.type==='prop'&&c.houses>0){
        if(c.houses===4){
          svg+=`<rect x="${x+3}" y="${cy-8}" width="9" height="14" fill="#c0392b" rx="1" opacity="0.9"/>`;
        }else{
          for(let hh=0;hh<c.houses;hh++)
            svg+=`<rect x="${x+3}" y="${cy-c.houses*4+hh*8}" width="6" height="7" fill="#27ae60" rx="1" opacity="0.9"/>`;
        }
      }
    }

    // Owner dot
    if(owner&&!c.mortgaged){
      svg+=`<circle cx="${x+w-6}" cy="${y+6}" r="3.5" fill="${owner.color}" opacity="0.85" stroke="#0c0c1a" stroke-width="0.8"/>`;
    }
    if(c.mortgaged){
      svg+=`<text x="${cx}" y="${cy+4}" text-anchor="middle" font-size="7.5" fill="#c0392b" opacity="0.65" font-family="Nanum Gothic,sans-serif">저당</text>`;
    }
  });

  // ── Center panel ───────────────────────────────────────
  svg+=`<rect x="${CR}" y="${CR}" width="${S-2*CR}" height="${S-2*CR}" fill="#080812" rx="6"/>`;
  svg+=`<text x="${S/2}" y="${S/2-22}" text-anchor="middle" font-size="26"
    fill="#e94560" font-family="Black Han Sans,sans-serif" filter="url(#softglow)" opacity="0.9">부루마블</text>`;
  svg+=`<text x="${S/2}" y="${S/2-4}" text-anchor="middle" font-size="9.5"
    fill="#555" font-family="Nanum Gothic,sans-serif">효민 월드</text>`;
  // Dice display in center
  if(G.d1&&G.d2){
    svg+=`<text x="${S/2-16}" y="${S/2+20}" text-anchor="middle" font-size="18" fill="#fff" opacity="0.8">${DICE_FACES[G.d1-1]}</text>`;
    svg+=`<text x="${S/2+16}" y="${S/2+20}" text-anchor="middle" font-size="18" fill="#fff" opacity="0.8">${DICE_FACES[G.d2-1]}</text>`;
  }

  // ── Tokens ─────────────────────────────────────────────
  const tokenOffset={};
  G.players.forEach((p,pi)=>{
    if(p.bankrupt)return;
    const{x,y,w,h}=getCellCoords(p.pos);
    const slot=tokenOffset[p.pos]||0;
    tokenOffset[p.pos]=slot+1;
    const isCorner=p.pos===0||p.pos===10||p.pos===20||p.pos===30;
    let tx,ty;
    if(isCorner){
      tx=x+w/2-10+(slot%2)*18;
      ty=y+h-18+Math.floor(slot/2)*(-18);
    }else if(p.pos<10||p.pos>=20){
      tx=x+w/2-8+(slot%2)*16;
      ty=y+h-17;
    }else{
      tx=x+3;
      ty=y+h/2-8+slot*16;
    }
    svg+=`<circle cx="${tx+8}" cy="${ty+8}" r="9" fill="${p.color}" stroke="#fff" stroke-width="1.4"
      filter="url(#glow)" opacity="0.96"/>`;
    svg+=`<text x="${tx+8}" y="${ty+12}" text-anchor="middle" font-size="8.5"
      fill="#fff" font-weight="700" font-family="sans-serif">${p.token}</text>`;
  });

  svg+=`</svg>`;
  wrap.innerHTML=svg;
}

// ══════════════════════════════════════════════════════════
//  SIDE PANEL RENDERERS
// ══════════════════════════════════════════════════════════
function renderPlayers(){
  const el=document.getElementById('players-list');
  if(!el)return;
  el.innerHTML=G.players.map((p,i)=>{
    const isActive=i===G.turn&&!p.bankrupt;
    if(p.bankrupt){
      return`<div class="player-row player-bankrupt">
        <div class="player-dot" style="background:${p.color};opacity:0.25"></div>
        <span class="player-name" style="color:#555">${p.token} ${p.name}</span>
        <span style="font-size:0.62rem;color:#c0392b">💀파산</span>
      </div>`;
    }
    const jailTxt=p.jail_turns>0
      ?`<span class="player-jail">🔒${p.jail_turns}</span>`:'';
    const botTxt=p.is_bot?' 🤖':'';
    return`<div class="player-row${isActive?' active-turn':''}">
      <div class="player-dot" style="background:${p.color}"></div>
      <span class="player-name" style="color:${p.color}">${p.token} ${p.name}${botTxt}</span>
      <span class="player-money">${p.money.toLocaleString()}</span>
      ${jailTxt}
    </div>`;
  }).join('');
}

let buildOpen=false;

function renderAction(){
  const aa=document.getElementById('action-area');
  if(!aa||!G)return;
  const pidx=G.turn,p=G.players[pidx],phase=G.phase;
  let html='';
  html+=`<div class="turn-label" style="color:${p.color}">${p.token} ${p.name}${p.is_bot?' 🤖':''} 차례</div>`;
  html+=`<div class="dice-display">
    <div class="die" id="die1">${DICE_FACES[(G.d1||1)-1]}</div>
    <div class="die" id="die2">${DICE_FACES[(G.d2||2)-1]}</div>
  </div>`;

  if(p.is_bot){
    html+=`<div class="phase-badge">⚙️ 봇 생각 중...</div>`;
    aa.innerHTML=html;return;
  }
  if(p.bankrupt){aa.innerHTML=html;return;}

  // 무인도
  if(p.jail_turns>0&&phase==='roll'){
    html+=`<div class="info-msg">🔒 무인도 구금 중 (${p.jail_turns}턴 남음)</div>`;
    html+=`<div class="jail-btns">
      <button class="btn btn-warning" onclick="doPlayerJail(true)" ${p.money<JAIL_BAIL?'disabled':''}>
        💰 보석 (${JAIL_BAIL})
      </button>
      <button class="btn btn-primary" onclick="doPlayerJail(false)">🎲 더블 도전</button>
    </div>`;
  }
  // 주사위
  else if(phase==='roll'){
    html+=`<button class="btn btn-primary btn-full" onclick="doPlayerRoll()"
      ${G.animating?'disabled':''}>🎲 주사위 굴리기</button>`;
    html+=`<button class="expand-btn" onclick="toggleBuild()">
      ${buildOpen?'▲':'▼'} 🏗️ 건설 · 저당 관리
    </button>`;
    html+=`<div class="build-section${buildOpen?' open':''}" id="build-section">
      <div class="build-list" id="build-list"></div>
    </div>`;
  }
  // 구매
  else if(phase==='buy'){
    const ci=p.pos,cell=G.cells[ci];
    const icon=cell.type==='prop'?'🏠':cell.type==='rail'?'🚂':'⚡';
    html+=`<div class="card-popup">
      <div class="card-emoji">${icon}</div>
      <div class="card-text">${cell.name}</div>
      <div class="card-effect">매입가 ${cell.price.toLocaleString()} · 기본통행료 ${cell.rent}</div>
    </div>`;
    html+=`<button class="btn btn-success btn-full" onclick="doPlayerBuy(true)"
      ${p.money<cell.price?'disabled':''}>✅ 매입 (-${cell.price.toLocaleString()})</button>`;
    html+=`<button class="btn btn-secondary btn-full" onclick="doPlayerBuy(false)">↩️ 패스</button>`;
  }
  // 카드
  else if(phase==='card'&&G.pending_card){
    const card=G.pending_card;
    const amtTxt=card.amount!==undefined
      ?`<span style="color:${card.amount>0?'#2ecc71':'#e74c3c'}">${card.amount>0?'+':''}${card.amount}</span>`:'';
    html+=`<div class="card-popup">
      <div class="card-emoji">${card.emoji}</div>
      <div class="card-text">${card.text}</div>
      <div class="card-effect">${amtTxt}</div>
    </div>`;
    html+=`<button class="btn btn-primary btn-full" onclick="doPlayerCard()">확인</button>`;
  }

  aa.innerHTML=html;

  // 건설 목록 렌더
  if(phase==='roll'&&buildOpen)renderBuildList();
}

function toggleBuild(){
  buildOpen=!buildOpen;
  renderAction();
}

function renderBuildList(){
  const el=document.getElementById('build-list');
  if(!el)return;
  const pidx=G.turn,p=G.players[pidx];
  const my=G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx);
  if(!my.length){
    el.innerHTML=`<div style="font-size:0.68rem;color:#555;padding:5px 0">소유한 땅이 없습니다.</div>`;
    return;
  }
  el.innerHTML=my.map(({c,ci})=>{
    if(c.type!=='prop'&&c.type!=='rail'&&c.type!=='util')return'';
    const canBuild=c.type==='prop'&&ownsGroup(pidx,c.group)&&!c.mortgaged&&c.houses<4;
    const cost=BUILD_COST[c.group]||300;
    const canAfford=p.money>=cost;
    let hLabel='';
    if(c.houses===4)hLabel=`<span class="hotel-icon"></span>`;
    else for(let hh=0;hh<c.houses;hh++)hLabel+=`<span class="h-dot"></span>`;
    const dotStyle=c.color?`background:${c.color}`:'background:#555';
    const mortLabel=c.mortgaged?`<span style="color:#c0392b;font-size:0.58rem"> 저당</span>`:'';
    return`<div class="build-item">
      <div class="color-dot" style="${dotStyle}"></div>
      <span class="build-item-name" style="color:${c.mortgaged?'#c0392b':'#ccc'}">${c.name}${hLabel}${mortLabel}</span>
      <div class="build-item-btns">
        ${canBuild&&canAfford
          ?`<button class="mini-btn mini-btn-build" onclick="doBuild(${pidx},${ci})">${c.houses===3?'🏨':'🏠'}</button>`
          :''}
        ${!c.mortgaged&&c.houses===0
          ?`<button class="mini-btn mini-btn-mort" onclick="doMortgage(${pidx},${ci})">저당</button>`
          :''}
        ${c.mortgaged
          ?`<button class="mini-btn mini-btn-unmort" onclick="doUnmortgage(${pidx},${ci})"
              ${p.money<Math.floor(c.price*UNMORT_RATE)?'disabled':''}>해제</button>`
          :''}
      </div>
    </div>`;
  }).join('');
}

function renderLog(){
  const el=document.getElementById('log-area');
  if(!el)return;
  el.innerHTML=G.log.slice(0,30).map(e=>
    `<div class="log-entry ${e.style||''}">${e.msg}</div>`
  ).join('');
}

function renderAll(){
  if(!G)return;
  renderBoard();
  renderPlayers();
  renderAction();
  renderLog();
}

// ══════════════════════════════════════════════════════════
//  GAME START / RESET / OVER
// ══════════════════════════════════════════════════════════
function startGame(){
  const name=document.getElementById('inp-name').value.trim()||'플레이어';
  const bots=parseInt(document.getElementById('inp-bots').value);
  const diff=document.getElementById('inp-diff').value;
  G=initGame(name,bots,diff);
  document.getElementById('setup-screen').style.display='none';
  const gs=document.getElementById('game-screen');
  gs.style.display='flex';
  addLog('🎲 게임 시작!','important');
  renderAll();
  setTimeout(checkBotTurn,800);
}

function resetGame(){
  G=null;buildOpen=false;
  document.getElementById('gameover-screen').style.display='none';
  document.getElementById('game-screen').style.display='none';
  document.getElementById('setup-screen').style.display='flex';
}

function showGameOver(){
  if(!G||!G.winner)return;
  document.getElementById('winner-title').textContent=`🏆 ${G.winner} 우승!`;
  const ranked=[...G.players].sort((a,b)=>b.money-a.money);
  const medals=['🥇','🥈','🥉','4️⃣'];
  document.getElementById('rank-list').innerHTML=ranked.map((p,i)=>`
    <div class="rank-row">
      <span class="rank-medal">${medals[i]||''}</span>
      <span class="rank-name" style="color:${p.color}">${p.token} ${p.name}</span>
      ${p.bankrupt
        ?`<span class="rank-bankrupt">💀 파산</span>`
        :`<span class="rank-money">${p.money.toLocaleString()}</span>`}
    </div>`).join('');
  document.getElementById('gameover-screen').style.display='flex';
  butlerSay('win');
  spawnConfetti();
}

// ── Confetti ───────────────────────────────────────────────
function spawnConfetti(){
  const colors=['#e74c3c','#3498db','#2ecc71','#f39c12','#e91e63','#9c27b0','#00bcd4'];
  const style=document.createElement('style');
  style.textContent=`@keyframes cfall{0%{transform:translateY(-20px) rotate(0deg);opacity:1}
    100%{transform:translateY(110vh) rotate(720deg);opacity:0}}`;
  document.head.appendChild(style);
  for(let i=0;i<80;i++){
    const d=document.createElement('div');
    const size=5+Math.random()*8;
    d.style.cssText=`
      position:fixed;top:-20px;left:${Math.random()*100}%;
      width:${size}px;height:${size}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      border-radius:${Math.random()>0.5?'50%':'2px'};
      z-index:9999;pointer-events:none;
      animation:cfall ${1.5+Math.random()*2.5}s ease-in ${Math.random()*2}s forwards;
    `;
    document.body.appendChild(d);
    setTimeout(()=>d.remove(),5000);
  }
}
</script>
</body>
</html>
"""


# ══════════════════════════════════════════════════════════
#  STREAMLIT ENTRY POINT
# ══════════════════════════════════════════════════════════

def render():
    st.set_page_config(
        page_title="부루마블",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    # 기본 streamlit 여백 제거
    st.markdown("""
    <style>
    #MainMenu{visibility:hidden}
    footer{visibility:hidden}
    header{visibility:hidden}
    .block-container{padding:0!important;max-width:100%!important}
    </style>
    """, unsafe_allow_html=True)

    components.html(GAME_HTML, height=620, scrolling=False)


if __name__ == "__main__":
    render()
