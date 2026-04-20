import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>모두의마블 🌍</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Black+Han+Sans&family=Fredoka+One&display=swap" rel="stylesheet">
<style>
/* ══════════════════════════════════════════════════════
   ROOT VARIABLES & RESET
══════════════════════════════════════════════════════ */
:root {
  --bg:       #080c18;
  --bg2:      #0f1628;
  --bg3:      #161e35;
  --bg4:      #1d2640;
  --glass:    rgba(255,255,255,0.04);
  --glass2:   rgba(255,255,255,0.08);
  --border:   rgba(255,255,255,0.08);
  --border2:  rgba(255,255,255,0.15);
  --text:     #f0f4ff;
  --text2:    #8899bb;
  --text3:    #445577;
  --gold:     #ffd700;
  --gold2:    #ffb800;
  --green:    #22c55e;
  --red:      #ef4444;
  --blue:     #3b82f6;
  --purple:   #a855f7;
  --orange:   #f97316;
  --pink:     #ec4899;
  --teal:     #14b8a6;
  --cyan:     #06b6d4;
  --r:        14px;
  --r2:       9px;
  --shadow:   0 8px 32px rgba(0,0,0,0.6);
  --shadow2:  0 3px 14px rgba(0,0,0,0.4);
}

*{box-sizing:border-box;margin:0;padding:0;}
html,body{
  font-family:'Noto Sans KR',sans-serif;
  background:var(--bg);
  color:var(--text);
  overflow:hidden;
  height:100vh;
  width:100vw;
  user-select:none;
}

/* ══════════════════════════════════════════════════════
   CHARACTER SELECT SCREEN
══════════════════════════════════════════════════════ */
#char-select{
  position:fixed;inset:0;
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  background:radial-gradient(ellipse at 30% 0%,#1a0a3e 0%,#080c18 55%),
             radial-gradient(ellipse at 80% 100%,#0a1a3e 0%,transparent 50%);
  z-index:200;
  overflow:hidden;
}
.char-bg-stars{
  position:absolute;inset:0;
  pointer-events:none;
  overflow:hidden;
}
.star{
  position:absolute;
  background:#fff;
  border-radius:50%;
  animation:twinkle var(--dur,2s) ease-in-out infinite;
  opacity:0;
}
@keyframes twinkle{
  0%,100%{opacity:0;transform:scale(0.5);}
  50%{opacity:var(--op,0.8);transform:scale(1);}
}
.char-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:3.2rem;
  background:linear-gradient(135deg,#ffd700 0%,#ff6b35 40%,#ff4d6d 70%,#c026d3 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  text-align:center;
  letter-spacing:3px;
  margin-bottom:4px;
  filter:drop-shadow(0 0 30px rgba(255,215,0,0.3));
  animation:titlePulse 3s ease-in-out infinite;
}
@keyframes titlePulse{
  0%,100%{filter:drop-shadow(0 0 30px rgba(255,215,0,0.3));}
  50%{filter:drop-shadow(0 0 50px rgba(255,215,0,0.5));}
}
.char-subtitle{
  color:var(--text3);
  font-size:0.75rem;
  letter-spacing:4px;
  text-transform:uppercase;
  margin-bottom:32px;
}
.char-prompt{
  color:var(--text2);
  font-size:0.9rem;
  margin-bottom:20px;
  font-weight:500;
}
.char-grid{
  display:grid;
  grid-template-columns:repeat(3,1fr);
  gap:14px;
  margin-bottom:28px;
}
.char-card{
  width:130px;height:160px;
  border-radius:18px;
  border:2px solid var(--border2);
  background:var(--bg3);
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  gap:6px;
  cursor:pointer;
  transition:all 0.25s cubic-bezier(0.34,1.56,0.64,1);
  position:relative;
  overflow:hidden;
}
.char-card::before{
  content:'';
  position:absolute;inset:0;
  background:var(--char-color,#3b82f6);
  opacity:0;
  transition:opacity 0.25s;
  border-radius:16px;
}
.char-card:hover{
  transform:translateY(-6px) scale(1.05);
  border-color:var(--char-color,#3b82f6);
  box-shadow:0 12px 40px rgba(0,0,0,0.5), 0 0 30px rgba(var(--char-rgb,59,130,246),0.3);
}
.char-card:hover::before{opacity:0.08;}
.char-card.selected{
  border-color:var(--char-color,#3b82f6);
  box-shadow:0 0 0 3px var(--char-color,#3b82f6),0 12px 40px rgba(0,0,0,0.6);
  transform:translateY(-4px) scale(1.03);
}
.char-card.selected::before{opacity:0.12;}
.char-avatar{
  font-size:3.2rem;
  animation:charFloat 3s ease-in-out infinite;
  filter:drop-shadow(0 4px 8px rgba(0,0,0,0.5));
  line-height:1;
}
.char-card:nth-child(2) .char-avatar{animation-delay:0.3s;}
.char-card:nth-child(3) .char-avatar{animation-delay:0.6s;}
.char-card:nth-child(4) .char-avatar{animation-delay:0.9s;}
.char-card:nth-child(5) .char-avatar{animation-delay:1.2s;}
.char-card:nth-child(6) .char-avatar{animation-delay:1.5s;}
@keyframes charFloat{
  0%,100%{transform:translateY(0);}
  50%{transform:translateY(-6px);}
}
.char-name{
  font-size:0.85rem;
  font-weight:700;
  color:var(--text);
  position:relative;z-index:1;
}
.char-desc{
  font-size:0.65rem;
  color:var(--text3);
  text-align:center;
  padding:0 6px;
  position:relative;z-index:1;
  line-height:1.4;
}
.char-ability{
  position:absolute;bottom:8px;
  font-size:0.6rem;
  color:var(--char-color,#3b82f6);
  background:rgba(0,0,0,0.3);
  border-radius:4px;
  padding:2px 6px;
}
.selected-check{
  position:absolute;top:8px;right:8px;
  width:20px;height:20px;
  border-radius:50%;
  background:var(--char-color,#3b82f6);
  display:none;
  align-items:center;justify-content:center;
  font-size:0.7rem;
  color:#fff;
  z-index:2;
}
.char-card.selected .selected-check{display:flex;}
.char-next-btn{
  background:linear-gradient(135deg,#ffd700,#ff6b35);
  border:none;
  border-radius:14px;
  color:#fff;
  font-family:'Black Han Sans',sans-serif;
  font-size:1.1rem;
  letter-spacing:3px;
  padding:14px 48px;
  cursor:pointer;
  box-shadow:0 6px 24px rgba(255,107,53,0.4);
  transition:all 0.2s;
  opacity:0.4;
  pointer-events:none;
}
.char-next-btn.active{
  opacity:1;
  pointer-events:all;
}
.char-next-btn.active:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 32px rgba(255,107,53,0.6);
}

/* ══════════════════════════════════════════════════════
   SETUP SCREEN
══════════════════════════════════════════════════════ */
#setup{
  position:fixed;inset:0;
  display:none;flex-direction:column;
  align-items:center;justify-content:center;
  background:radial-gradient(ellipse at 50% 0%,#12082a 0%,#080c18 60%);
  z-index:150;
}
.setup-card{
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:22px;
  padding:36px;
  width:420px;
  box-shadow:var(--shadow);
  position:relative;
  overflow:hidden;
}
.setup-card::before{
  content:'';
  position:absolute;
  top:-80px;left:-80px;
  width:200px;height:200px;
  background:radial-gradient(circle,rgba(255,215,0,0.08),transparent 70%);
  pointer-events:none;
}
.setup-char-preview{
  display:flex;
  align-items:center;
  gap:14px;
  background:var(--bg3);
  border-radius:14px;
  padding:14px 18px;
  margin-bottom:24px;
  border:1px solid var(--border);
}
.setup-char-avatar{
  font-size:2.8rem;
  animation:charFloat 3s ease-in-out infinite;
}
.setup-char-info{
  flex:1;
}
.setup-char-name{
  font-family:'Black Han Sans',sans-serif;
  font-size:1.1rem;
  color:var(--gold);
}
.setup-char-desc{
  font-size:0.75rem;
  color:var(--text3);
  margin-top:2px;
}
.setup-char-ability-tag{
  display:inline-block;
  margin-top:5px;
  font-size:0.65rem;
  padding:2px 8px;
  border-radius:20px;
  background:rgba(255,215,0,0.12);
  color:var(--gold2);
  border:1px solid rgba(255,215,0,0.2);
}
.setup-logo{
  font-family:'Black Han Sans',sans-serif;
  font-size:2rem;
  background:linear-gradient(135deg,#ffd700,#ff4d6d);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  text-align:center;
  letter-spacing:3px;
  margin-bottom:6px;
}
.setup-sub{
  color:var(--text3);
  font-size:0.7rem;
  letter-spacing:3px;
  margin-bottom:28px;
  text-align:center;
  text-transform:uppercase;
}
.form-row{margin-bottom:16px;}
.form-label{
  display:block;
  font-size:0.68rem;
  font-weight:700;
  color:var(--text3);
  text-transform:uppercase;
  letter-spacing:1.5px;
  margin-bottom:6px;
}
.form-input,.form-select{
  width:100%;
  background:var(--bg3);
  border:1px solid var(--border2);
  border-radius:var(--r2);
  color:var(--text);
  padding:11px 14px;
  font-size:0.9rem;
  font-family:'Noto Sans KR',sans-serif;
  outline:none;
  transition:border-color 0.2s,box-shadow 0.2s;
}
.form-input:focus,.form-select:focus{
  border-color:var(--gold);
  box-shadow:0 0 0 3px rgba(255,215,0,0.12);
}
.form-select option{background:#1a2040;}
.btn-start{
  width:100%;
  background:linear-gradient(135deg,#ffd700,#ff6b35);
  border:none;
  border-radius:14px;
  color:#fff;
  font-family:'Black Han Sans',sans-serif;
  font-size:1.15rem;
  letter-spacing:3px;
  padding:16px;
  cursor:pointer;
  margin-top:10px;
  transition:all 0.2s;
  box-shadow:0 6px 28px rgba(255,107,53,0.4);
}
.btn-start:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 38px rgba(255,107,53,0.6);
}
.btn-start:active{transform:scale(0.97);}
.btn-back-setup{
  background:transparent;
  border:1px solid var(--border2);
  border-radius:10px;
  color:var(--text2);
  font-size:0.82rem;
  padding:9px 20px;
  cursor:pointer;
  margin-top:8px;
  width:100%;
  transition:all 0.2s;
}
.btn-back-setup:hover{background:var(--glass2);color:var(--text);}
.rules-mini{
  margin-top:18px;
  background:var(--bg3);
  border-radius:var(--r2);
  padding:12px 16px;
  font-size:0.72rem;
  color:var(--text3);
  line-height:2;
  border:1px solid var(--border);
}
.rules-mini b{color:var(--text2);}

/* ══════════════════════════════════════════════════════
   GAME LAYOUT
══════════════════════════════════════════════════════ */
#game{
  display:none;
  width:100vw;height:100vh;
  flex-direction:row;
}
.board-wrap{
  flex:1;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:12px;
  min-width:0;
  position:relative;
  background:radial-gradient(ellipse at center,#10163a 0%,#080c18 100%);
  overflow:hidden;
}
.board-wrap::before{
  content:'';
  position:absolute;inset:0;
  background:
    radial-gradient(ellipse at 20% 20%,rgba(168,85,247,0.06) 0%,transparent 50%),
    radial-gradient(ellipse at 80% 80%,rgba(59,130,246,0.06) 0%,transparent 50%);
  pointer-events:none;
}

/* ══════════════════════════════════════════════════════
   BOARD
══════════════════════════════════════════════════════ */
#board{
  position:relative;
  background:linear-gradient(135deg,#0a1020 0%,#0d1530 50%,#0a1020 100%);
  border:2px solid rgba(255,215,0,0.18);
  border-radius:6px;
  box-shadow:
    0 0 0 1px rgba(255,215,0,0.08),
    0 0 80px rgba(255,215,0,0.06),
    var(--shadow);
  aspect-ratio:1;
  flex-shrink:0;
  overflow:hidden;
}

/* Cell base */
.cell{
  position:absolute;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  border:1px solid rgba(255,255,255,0.055);
  cursor:default;
  overflow:hidden;
  transition:filter 0.2s;
}
.cell:hover{filter:brightness(1.25);}

/* Cell text */
.cell-name{
  text-align:center;
  color:#c8d8f8;
  line-height:1.2;
  font-weight:600;
  font-size:0;
  position:relative;z-index:1;
}
.cell-price{
  color:#556688;
  text-align:center;
  font-weight:400;
  font-size:0;
  position:relative;z-index:1;
}
.cell-icon{
  line-height:1;
  position:relative;z-index:1;
}

/* Color bar for properties */
.color-bar{
  position:absolute;
  z-index:0;
  opacity:0.9;
}

/* Special cell corner */
.cell-corner{
  background:#080e24 !important;
}

/* Houses & hotels */
.house-dot{
  display:inline-block;
  background:#22c55e;
  border-radius:2px;
  box-shadow:0 1px 4px rgba(0,0,0,0.5);
}
.hotel-marker{
  display:inline-block;
  background:linear-gradient(135deg,#ef4444,#dc2626);
  border-radius:2px;
  box-shadow:0 1px 4px rgba(239,68,68,0.5);
}

/* Owner badge */
.owner-badge{
  position:absolute;
  top:2px;right:2px;
  border-radius:50%;
  border:1px solid rgba(0,0,0,0.5);
  z-index:3;
  box-shadow:0 0 6px currentColor;
}

/* Mortgaged overlay */
.mortgaged-overlay{
  position:absolute;inset:0;
  background:rgba(0,0,0,0.65);
  display:none;
  align-items:center;justify-content:center;
  color:#ef4444;
  font-weight:700;
  letter-spacing:1px;
  z-index:4;
  backdrop-filter:blur(1px);
}

/* Airport indicator */
.airport-bar{
  position:absolute;
  background:linear-gradient(90deg,#06b6d4,#3b82f6);
  opacity:0.8;
}

/* Casino shimmer */
.casino-cell{
  animation:casinoShimmer 2s ease-in-out infinite;
}
@keyframes casinoShimmer{
  0%,100%{box-shadow:inset 0 0 10px rgba(255,215,0,0.1);}
  50%{box-shadow:inset 0 0 20px rgba(255,215,0,0.25);}
}

/* ── Player tokens ── */
.token-cluster{
  position:absolute;
  display:flex;
  flex-wrap:wrap;
  gap:2px;
  align-items:center;
  justify-content:center;
  pointer-events:none;
  z-index:10;
}
.token{
  border-radius:50%;
  border:2px solid rgba(255,255,255,0.9);
  display:flex;
  align-items:center;justify-content:center;
  font-size:0;
  color:#fff;
  box-shadow:0 2px 10px rgba(0,0,0,0.7);
  position:relative;
  transition:all 0.35s cubic-bezier(0.34,1.56,0.64,1);
}
.token::after{
  content:'';
  position:absolute;
  bottom:-4px;
  left:50%;
  transform:translateX(-50%);
  width:60%;
  height:4px;
  background:rgba(0,0,0,0.3);
  border-radius:50%;
  filter:blur(2px);
}
.token.active-token{
  animation:tokenBounce 0.8s ease-in-out;
  box-shadow:0 0 16px var(--tok-color,#fff), 0 2px 10px rgba(0,0,0,0.7);
  z-index:20;
}
@keyframes tokenBounce{
  0%,100%{transform:translateY(0);}
  20%{transform:translateY(-8px);}
  40%{transform:translateY(-4px);}
  60%{transform:translateY(-6px);}
  80%{transform:translateY(-2px);}
}

/* ── Board center ── */
.board-center{
  position:absolute;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  background:linear-gradient(135deg,#060a18,#0d1530);
  overflow:hidden;
}
.board-center::before{
  content:'';
  position:absolute;
  inset:-20px;
  background:url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='30' cy='30' r='1' fill='rgba(255,255,255,0.03)'/%3E%3C/svg%3E");
  pointer-events:none;
}

.board-logo{
  font-family:'Black Han Sans',sans-serif;
  background:linear-gradient(135deg,#ffd700 0%,#ff6b35 50%,#ff4d6d 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  text-align:center;
  line-height:1.0;
  letter-spacing:2px;
  filter:drop-shadow(0 0 20px rgba(255,215,0,0.25));
}
.board-sub{
  color:rgba(255,255,255,0.12);
  text-align:center;
  letter-spacing:3px;
  text-transform:uppercase;
}

/* Center dice */
.dice-center{
  display:flex;
  gap:10px;
  position:relative;
}
.die-face{
  background:linear-gradient(135deg,#ffffff,#e8e8f0);
  border-radius:8px;
  display:flex;
  align-items:center;
  justify-content:center;
  color:#1a1a30;
  box-shadow:
    inset 0 1px 3px rgba(255,255,255,0.9),
    inset 0 -2px 4px rgba(0,0,0,0.2),
    0 4px 16px rgba(0,0,0,0.6);
  transition:transform 0.1s;
  position:relative;
}
.die-face.rolling{animation:diceRoll 0.7s cubic-bezier(0.25,0.46,0.45,0.94);}
.die-face.double-glow{
  box-shadow:
    inset 0 1px 3px rgba(255,255,255,0.9),
    0 0 24px rgba(255,215,0,1),
    0 0 48px rgba(255,215,0,0.5),
    0 4px 16px rgba(0,0,0,0.6);
}
@keyframes diceRoll{
  0%  {transform:rotate(0)scale(1);}
  15% {transform:rotate(-25deg)scale(1.2)translateY(-6px);}
  30% {transform:rotate(20deg)scale(1.25)translateY(-10px);}
  50% {transform:rotate(-12deg)scale(1.15)translateY(-5px);}
  70% {transform:rotate(6deg)scale(1.06);}
  85% {transform:rotate(-2deg)scale(1.02);}
  100%{transform:rotate(0)scale(1);}
}

/* World map decoration */
.center-map{
  opacity:0.04;
  pointer-events:none;
  font-size:0;
}

/* ══════════════════════════════════════════════════════
   SIDE PANEL
══════════════════════════════════════════════════════ */
.side{
  width:250px;
  background:var(--bg2);
  border-left:1px solid var(--border);
  display:flex;
  flex-direction:column;
  overflow:hidden;
  flex-shrink:0;
  position:relative;
}

/* Player section */
.side-players{
  padding:12px 14px 8px;
  border-bottom:1px solid var(--border);
  flex-shrink:0;
}
.sec-label{
  font-size:0.58rem;
  font-weight:700;
  color:var(--text3);
  text-transform:uppercase;
  letter-spacing:2px;
  margin-bottom:10px;
}
.player-card{
  display:flex;
  align-items:center;
  gap:9px;
  padding:8px 10px;
  border-radius:10px;
  transition:all 0.2s;
  margin-bottom:4px;
  position:relative;
  overflow:hidden;
}
.player-card::before{
  content:'';
  position:absolute;inset:0;
  background:var(--p-color,#fff);
  opacity:0;
  transition:opacity 0.2s;
  border-radius:10px;
}
.player-card.active::before{opacity:0.08;}
.player-card.active{
  box-shadow:0 0 0 1px var(--p-color,#fff),
             0 4px 16px rgba(0,0,0,0.3);
}
.player-avatar{
  font-size:1.4rem;
  flex-shrink:0;
  position:relative;z-index:1;
  filter:drop-shadow(0 2px 4px rgba(0,0,0,0.5));
}
.player-card.active .player-avatar{
  animation:avatarPulse 1.5s ease-in-out infinite;
}
@keyframes avatarPulse{
  0%,100%{transform:scale(1);}
  50%{transform:scale(1.15);}
}
.player-info{
  flex:1;
  min-width:0;
  position:relative;z-index:1;
}
.player-name-row{
  display:flex;align-items:center;gap:4px;
}
.player-name-txt{
  font-size:0.78rem;
  font-weight:700;
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
  flex:1;
}
.bot-badge{
  font-size:0.55rem;
  background:rgba(255,255,255,0.08);
  color:var(--text3);
  border-radius:4px;
  padding:1px 4px;
  flex-shrink:0;
}
.player-money{
  font-family:'Fredoka One',cursive;
  font-size:0.92rem;
  color:var(--green);
  margin-top:1px;
}
.player-money.losing{
  color:var(--red);
  animation:moneyShake 0.4s ease;
}
@keyframes moneyShake{
  0%,100%{transform:translateX(0);}
  25%{transform:translateX(-3px);}
  75%{transform:translateX(3px);}
}
.net-worth-bar{
  height:3px;
  border-radius:2px;
  background:rgba(255,255,255,0.08);
  margin-top:5px;
  overflow:hidden;
  position:relative;z-index:1;
}
.net-worth-fill{
  height:100%;
  border-radius:2px;
  background:var(--p-color,#22c55e);
  transition:width 0.6s ease;
  position:relative;
}
.net-worth-fill::after{
  content:'';
  position:absolute;top:0;right:0;
  width:40%;height:100%;
  background:rgba(255,255,255,0.4);
  border-radius:2px;
}
.player-badges{
  display:flex;gap:3px;margin-top:3px;
  position:relative;z-index:1;
}
.badge-jail{
  font-size:0.55rem;
  background:rgba(239,68,68,0.15);
  color:#ef4444;
  border-radius:4px;
  padding:1px 5px;
}
.badge-bankrupt{
  font-size:0.55rem;
  background:rgba(100,100,100,0.2);
  color:#888;
  border-radius:4px;
  padding:1px 5px;
}
.badge-ability{
  font-size:0.55rem;
  background:rgba(255,215,0,0.15);
  color:var(--gold);
  border-radius:4px;
  padding:1px 5px;
}
.player-card.bankrupt{opacity:0.45;}
.player-card.bankrupt .player-name-txt{text-decoration:line-through;}

/* Action zone */
.action-zone{
  flex:1;
  padding:12px 14px;
  overflow-y:auto;
  display:flex;
  flex-direction:column;
  gap:9px;
  min-height:0;
}
.action-zone::-webkit-scrollbar{width:3px;}
.action-zone::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}

.turn-banner{
  text-align:center;
  font-size:0.68rem;
  font-weight:700;
  padding:2px 0;
  color:var(--text2);
  display:flex;
  align-items:center;
  justify-content:center;
  gap:5px;
}
.turn-avatar{
  font-size:1.1rem;
  animation:charFloat 2s ease-in-out infinite;
}

.dice-display{
  display:flex;
  justify-content:center;
  gap:12px;
  padding:6px 0;
}
.dice-mini{
  width:36px;height:36px;
  background:linear-gradient(135deg,#fff,#e8e8f0);
  border-radius:7px;
  display:flex;
  align-items:center;justify-content:center;
  font-size:1.5rem;
  color:#1a1a30;
  box-shadow:
    inset 0 1px 2px rgba(255,255,255,0.9),
    0 3px 10px rgba(0,0,0,0.5);
}
.dice-mini.double-mini{
  box-shadow:0 0 16px rgba(255,215,0,0.9),0 3px 10px rgba(0,0,0,0.5);
}

/* Buttons */
.btn{
  border:none;
  border-radius:var(--r2);
  padding:10px 14px;
  font-family:'Noto Sans KR',sans-serif;
  font-size:0.8rem;
  font-weight:700;
  cursor:pointer;
  transition:all 0.15s;
  width:100%;
  position:relative;
  overflow:hidden;
}
.btn::after{
  content:'';
  position:absolute;inset:0;
  background:rgba(255,255,255,0);
  transition:background 0.15s;
}
.btn:hover::after{background:rgba(255,255,255,0.08);}
.btn:active:not(:disabled){transform:scale(0.96);}
.btn:disabled{opacity:0.3;cursor:not-allowed;}

.btn-roll{
  background:linear-gradient(135deg,#ff4d6d,#c0392b);
  color:#fff;
  box-shadow:0 4px 16px rgba(255,77,109,0.35);
  font-size:0.9rem;
  padding:13px;
}
.btn-roll:hover:not(:disabled){box-shadow:0 6px 24px rgba(255,77,109,0.55);transform:translateY(-1px);}

.btn-green{
  background:linear-gradient(135deg,#22c55e,#16a34a);
  color:#fff;
  box-shadow:0 4px 14px rgba(34,197,94,0.3);
}
.btn-green:hover:not(:disabled){box-shadow:0 6px 20px rgba(34,197,94,0.5);transform:translateY(-1px);}

.btn-ghost{
  background:var(--bg3);
  color:var(--text2);
  border:1px solid var(--border2);
}
.btn-ghost:hover:not(:disabled){background:var(--glass2);color:var(--text);}

.btn-orange{
  background:linear-gradient(135deg,#f97316,#ea580c);
  color:#fff;
  box-shadow:0 4px 14px rgba(249,115,22,0.3);
}
.btn-orange:hover:not(:disabled){box-shadow:0 6px 20px rgba(249,115,22,0.5);transform:translateY(-1px);}

.btn-purple{
  background:linear-gradient(135deg,#a855f7,#7c3aed);
  color:#fff;
  box-shadow:0 4px 14px rgba(168,85,247,0.3);
}
.btn-purple:hover:not(:disabled){box-shadow:0 6px 20px rgba(168,85,247,0.5);transform:translateY(-1px);}

.btn-row{display:flex;gap:7px;}
.btn-row .btn{flex:1;}

/* Info box */
.info-box{
  background:var(--bg3);
  border:1px solid var(--border);
  border-radius:var(--r2);
  padding:9px 12px;
  font-size:0.75rem;
  color:var(--text2);
  text-align:center;
  line-height:1.6;
}

/* ══════════════════════════════════════════════════════
   PROPERTY PURCHASE CARD POPUP
══════════════════════════════════════════════════════ */
.prop-card-popup{
  background:linear-gradient(160deg,var(--bg3),var(--bg2));
  border:1px solid rgba(255,215,0,0.2);
  border-radius:16px;
  padding:16px;
  text-align:center;
  animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);
  position:relative;
  overflow:hidden;
}
.prop-card-popup::before{
  content:'';
  position:absolute;
  top:-40px;left:-40px;
  width:120px;height:120px;
  background:radial-gradient(circle,var(--card-color,rgba(255,215,0,0.15)),transparent 70%);
  pointer-events:none;
}
@keyframes cardSlideUp{
  from{opacity:0;transform:translateY(20px) scale(0.95);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
.prop-card-flag{
  font-size:2rem;
  margin-bottom:3px;
  filter:drop-shadow(0 3px 6px rgba(0,0,0,0.4));
}
.prop-card-color-band{
  position:absolute;
  top:0;left:0;right:0;
  height:4px;
  border-radius:16px 16px 0 0;
}
.prop-card-city{
  font-family:'Black Han Sans',sans-serif;
  font-size:1.2rem;
  color:var(--text);
  letter-spacing:2px;
}
.prop-card-country{
  font-size:0.68rem;
  color:var(--text3);
  margin-bottom:8px;
  letter-spacing:1px;
}
.prop-card-price{
  font-family:'Fredoka One',cursive;
  font-size:1.5rem;
  color:var(--gold);
  margin:5px 0;
  text-shadow:0 0 20px rgba(255,215,0,0.4);
}
.prop-card-rent-row{
  display:flex;
  justify-content:space-between;
  font-size:0.65rem;
  color:var(--text3);
  padding:2px 0;
  border-bottom:1px solid var(--border);
}
.prop-card-rent-row:last-child{border:none;}
.prop-card-rent-row span:last-child{color:var(--text2);}

/* Chance/Fate card */
.card-box{
  background:linear-gradient(160deg,var(--bg3),var(--bg2));
  border:1px solid rgba(255,215,0,0.22);
  border-radius:16px;
  padding:14px 12px;
  text-align:center;
  animation:cardFlip 0.5s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes cardFlip{
  0%{opacity:0;transform:rotateY(90deg) scale(0.8);}
  60%{transform:rotateY(-8deg) scale(1.02);}
  100%{opacity:1;transform:rotateY(0) scale(1);}
}
.card-emoji{
  font-size:2.4rem;
  margin-bottom:6px;
  filter:drop-shadow(0 3px 8px rgba(0,0,0,0.4));
}
.card-title{
  font-size:0.85rem;
  font-weight:700;
  color:var(--text);
  margin-bottom:3px;
}
.card-effect{
  font-size:0.8rem;
  color:var(--text2);
}
.card-effect.gain{color:#4ade80;}
.card-effect.lose{color:#f87171;}

/* Casino popup */
.casino-box{
  background:linear-gradient(160deg,#1a0a2e,#12082a);
  border:1px solid rgba(255,215,0,0.35);
  border-radius:16px;
  padding:14px 12px;
  text-align:center;
  animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);
  box-shadow:0 0 30px rgba(255,215,0,0.1);
}
.casino-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:1.1rem;
  color:var(--gold);
  margin-bottom:4px;
  letter-spacing:2px;
}
.casino-desc{
  font-size:0.7rem;
  color:var(--text3);
  margin-bottom:10px;
  line-height:1.6;
}
.casino-amount{
  font-family:'Fredoka One',cursive;
  font-size:1.3rem;
  color:var(--gold2);
  margin-bottom:8px;
}

/* Property manager */
.mgr-toggle{
  background:var(--bg3);
  border:1px solid var(--border2);
  border-radius:var(--r2);
  color:var(--text2);
  font-size:0.75rem;
  font-family:'Noto Sans KR',sans-serif;
  padding:8px 12px;
  cursor:pointer;
  width:100%;
  text-align:left;
  display:flex;
  align-items:center;
  gap:6px;
  transition:all 0.2s;
}
.mgr-toggle:hover{background:var(--glass2);color:var(--text);}
.mgr-toggle-arrow{margin-left:auto;transition:transform 0.2s;}
.mgr-toggle.open .mgr-toggle-arrow{transform:rotate(180deg);}

.mgr-list{
  display:none;
  flex-direction:column;
  gap:4px;
}
.mgr-list.open{display:flex;}
.prop-row{
  display:flex;
  align-items:center;
  gap:7px;
  padding:5px 4px;
  border-radius:6px;
  transition:background 0.15s;
}
.prop-row:hover{background:var(--glass);}
.prop-color{
  width:8px;height:8px;
  border-radius:2px;
  flex-shrink:0;
}
.prop-name{
  flex:1;
  font-size:0.7rem;
  color:var(--text2);
  overflow:hidden;
  text-overflow:ellipsis;
  white-space:nowrap;
}
.prop-name.mortgaged{color:var(--text3);text-decoration:line-through;}
.prop-btns{display:flex;gap:3px;}
.mini-b{
  font-size:0.6rem;
  border:none;
  border-radius:4px;
  padding:2px 7px;
  cursor:pointer;
  font-family:'Noto Sans KR',sans-serif;
  transition:all 0.15s;
}
.mini-b:active{transform:scale(0.95);}
.mini-b-build{background:rgba(34,197,94,0.15);color:#22c55e;border:1px solid rgba(34,197,94,0.3);}
.mini-b-build:hover{background:rgba(34,197,94,0.25);}
.mini-b-mort{background:rgba(249,115,22,0.15);color:#f97316;border:1px solid rgba(249,115,22,0.25);}
.mini-b-mort:hover{background:rgba(249,115,22,0.25);}
.mini-b-unmort{background:rgba(59,130,246,0.15);color:#3b82f6;border:1px solid rgba(59,130,246,0.25);}
.mini-b-unmort:hover:not(:disabled){background:rgba(59,130,246,0.25);}
.mini-b:disabled{opacity:0.35;cursor:not-allowed;}

/* Log */
.log-wrap{
  border-top:1px solid var(--border);
  padding:8px 14px 10px;
  flex-shrink:0;
  max-height:180px;
  display:flex;
  flex-direction:column;
  overflow:hidden;
}
.log-inner{
  flex:1;
  overflow-y:auto;
  scrollbar-width:none;
}
.log-inner::-webkit-scrollbar{display:none;}
.log-row{
  padding:2px 0;
  font-size:0.68rem;
  color:var(--text3);
  border-bottom:1px solid rgba(255,255,255,0.03);
  line-height:1.5;
}
.log-row.gain{color:#4ade80;}
.log-row.lose{color:#f87171;}
.log-row.move{color:#60a5fa;}
.log-row.important{color:var(--gold);font-weight:700;}

/* ══════════════════════════════════════════════════════
   BUTLER / SPEECH BUBBLE
══════════════════════════════════════════════════════ */
#butler{
  position:absolute;
  bottom:20px;left:20px;
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:14px;
  padding:10px 14px;
  font-size:0.78rem;
  color:var(--text);
  max-width:200px;
  display:none;
  z-index:20;
  box-shadow:var(--shadow2);
  animation:butlerPop 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.butler-char{margin-right:6px;}
@keyframes butlerPop{
  from{opacity:0;transform:translateY(10px) scale(0.9);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
#butler::after{
  content:'';
  position:absolute;
  bottom:-8px;left:20px;
  width:0;height:0;
  border-left:8px solid transparent;
  border-right:8px solid transparent;
  border-top:8px solid var(--border2);
}

/* ══════════════════════════════════════════════════════
   FLOATING MONEY / PARTICLES
══════════════════════════════════════════════════════ */
.float-text{
  position:fixed;
  font-family:'Fredoka One',cursive;
  font-size:1.2rem;
  font-weight:700;
  pointer-events:none;
  z-index:9999;
  white-space:nowrap;
  animation:floatUp 1.2s ease-out forwards;
}
@keyframes floatUp{
  0%{opacity:1;transform:translateY(0) scale(1);}
  30%{opacity:1;transform:translateY(-20px) scale(1.2);}
  100%{opacity:0;transform:translateY(-60px) scale(0.8);}
}
.coin{
  position:fixed;
  pointer-events:none;
  z-index:9998;
  font-size:1.2rem;
  animation:coinFly var(--dur,0.8s) cubic-bezier(0.25,0.46,0.45,0.94) forwards;
}
@keyframes coinFly{
  0%{opacity:1;transform:translate(0,0) scale(1) rotate(0deg);}
  50%{opacity:1;transform:translate(var(--mx,20px),var(--my,-30px)) scale(1.3) rotate(180deg);}
  100%{opacity:0;transform:translate(var(--ex,40px),var(--ey,-50px)) scale(0.5) rotate(360deg);}
}

/* ══════════════════════════════════════════════════════
   TOAST NOTIFICATION
══════════════════════════════════════════════════════ */
#toast-container{
  position:fixed;
  top:20px;
  left:50%;
  transform:translateX(-50%);
  z-index:9997;
  display:flex;
  flex-direction:column;
  gap:8px;
  pointer-events:none;
  align-items:center;
}
.toast{
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:24px;
  padding:10px 22px;
  font-size:0.82rem;
  font-weight:600;
  color:var(--text);
  box-shadow:var(--shadow);
  animation:toastIn 0.35s cubic-bezier(0.34,1.56,0.64,1),
            toastOut 0.3s ease 2s forwards;
  white-space:nowrap;
  display:flex;
  align-items:center;
  gap:8px;
}
.toast.toast-gain{border-color:rgba(34,197,94,0.4);background:rgba(34,197,94,0.08);}
.toast.toast-lose{border-color:rgba(239,68,68,0.4);background:rgba(239,68,68,0.08);}
.toast.toast-special{border-color:rgba(255,215,0,0.4);background:rgba(255,215,0,0.06);}
@keyframes toastIn{
  from{opacity:0;transform:translateY(-12px) scale(0.9);}
  to{opacity:1;transform:translateY(0) scale(1);}
}
@keyframes toastOut{
  from{opacity:1;transform:translateY(0);}
  to{opacity:0;transform:translateY(-8px);}
}

/* ══════════════════════════════════════════════════════
   TOOLTIP
══════════════════════════════════════════════════════ */
.cell-tooltip{
  position:fixed;
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:12px;
  padding:12px 14px;
  font-size:0.72rem;
  z-index:50;
  pointer-events:none;
  box-shadow:var(--shadow);
  min-width:160px;
  display:none;
  animation:tooltipFade 0.2s ease;
}
@keyframes tooltipFade{
  from{opacity:0;transform:scale(0.95);}
  to{opacity:1;transform:scale(1);}
}
.tooltip-title{
  font-weight:700;
  color:var(--text);
  margin-bottom:4px;
  font-size:0.78rem;
  display:flex;align-items:center;gap:5px;
}
.tooltip-band{
  display:inline-block;
  width:10px;height:10px;
  border-radius:2px;
}
.tooltip-row{
  display:flex;
  justify-content:space-between;
  gap:16px;
  color:var(--text3);
  padding:2px 0;
  border-bottom:1px solid var(--border);
}
.tooltip-row:last-child{border:none;}
.tooltip-row span:last-child{color:var(--text2);}
.tooltip-own{
  margin-top:4px;
  font-size:0.65rem;
  text-align:center;
  border-radius:4px;
  padding:3px;
}

/* ══════════════════════════════════════════════════════
   GAME OVER SCREEN
══════════════════════════════════════════════════════ */
#gameover{
  position:fixed;inset:0;
  background:rgba(5,8,18,0.95);
  backdrop-filter:blur(12px);
  display:none;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  z-index:100;
}
.gameover-winner{
  font-family:'Black Han Sans',sans-serif;
  font-size:3rem;
  background:linear-gradient(135deg,#ffd700,#ff6b35);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
  animation:winnerPop 0.6s cubic-bezier(0.34,1.56,0.64,1);
  filter:drop-shadow(0 0 30px rgba(255,215,0,0.4));
  text-align:center;
  margin-bottom:4px;
}
@keyframes winnerPop{
  from{opacity:0;transform:scale(0.3) rotate(-10deg);}
  60%{transform:scale(1.1) rotate(2deg);}
  to{opacity:1;transform:scale(1) rotate(0);}
}
.gameover-sub{
  color:var(--text3);
  font-size:0.8rem;
  letter-spacing:3px;
  margin-bottom:10px;
  text-transform:uppercase;
}
.gameover-avatar{
  font-size:4rem;
  margin-bottom:10px;
  animation:charFloat 2s ease-in-out infinite;
  filter:drop-shadow(0 4px 16px rgba(255,215,0,0.3));
}
.rank-card{
  background:var(--bg2);
  border:1px solid var(--border2);
  border-radius:18px;
  padding:20px 28px;
  width:100%;max-width:360px;
  margin-bottom:24px;
}
.rank-row{
  display:flex;align-items:center;gap:12px;
  padding:9px 0;
  border-bottom:1px solid var(--border);
  font-size:0.84rem;
}
.rank-row:last-child{border:none;}
.rank-medal{font-size:1.3rem;min-width:28px;}
.rank-avatar{font-size:1.2rem;}
.rank-player{flex:1;font-weight:700;}
.rank-money{color:var(--green);font-weight:700;font-family:'Fredoka One',cursive;}
.rank-dead{color:var(--red);font-size:0.7rem;}
.btn-restart{
  background:linear-gradient(135deg,#ffd700,#ff6b35);
  border:none;
  border-radius:14px;
  color:#fff;
  font-family:'Black Han Sans',sans-serif;
  font-size:1.1rem;
  letter-spacing:3px;
  padding:14px 48px;
  cursor:pointer;
  box-shadow:0 6px 24px rgba(255,107,53,0.4);
  transition:all 0.2s;
}
.btn-restart:hover{transform:translateY(-2px);box-shadow:0 10px 32px rgba(255,107,53,0.6);}

/* ══════════════════════════════════════════════════════
   CONFETTI
══════════════════════════════════════════════════════ */
.confetti-piece{
  position:fixed;
  pointer-events:none;
  z-index:9999;
  animation:confettiFall linear forwards;
}
@keyframes confettiFall{
  0%{transform:translateY(-20px) rotate(0) scale(1);opacity:1;}
  100%{transform:translateY(110vh) rotate(720deg) scale(0.5);opacity:0;}
}

/* ══════════════════════════════════════════════════════
   SPECIAL EFFECTS
══════════════════════════════════════════════════════ */
.blackhole-pulse{
  animation:bholePulse 2s ease-in-out infinite;
}
@keyframes bholePulse{
  0%,100%{box-shadow:inset 0 0 15px rgba(168,85,247,0.3);}
  50%{box-shadow:inset 0 0 30px rgba(168,85,247,0.5);}
}

/* Double ring animation */
.double-ring{
  position:fixed;
  border-radius:50%;
  border:3px solid var(--gold);
  animation:doubleRing 0.8s ease-out forwards;
  pointer-events:none;
  z-index:9996;
}
@keyframes doubleRing{
  from{transform:translate(-50%,-50%) scale(0.5);opacity:1;}
  to{transform:translate(-50%,-50%) scale(2.5);opacity:0;}
}

/* Special tile glow */
.casino-glow{
  animation:casinoGlow 2.5s ease-in-out infinite;
}
@keyframes casinoGlow{
  0%,100%{box-shadow:inset 0 0 12px rgba(255,215,0,0.15),0 0 8px rgba(255,215,0,0.08);}
  50%{box-shadow:inset 0 0 24px rgba(255,215,0,0.3),0 0 16px rgba(255,215,0,0.2);}
}

/* Ability use flash */
.ability-flash{
  position:fixed;inset:0;
  background:var(--char-color,rgba(255,215,0,0.1));
  pointer-events:none;
  z-index:9990;
  animation:abilityFlash 0.5s ease-out forwards;
}
@keyframes abilityFlash{
  0%{opacity:0.3;}
  100%{opacity:0;}
}

/* Net worth indicator ring */
.wealth-ring{
  position:absolute;
  inset:-3px;
  border-radius:50%;
  border:2px solid transparent;
  animation:wealthPulse 2s ease-in-out infinite;
}
@keyframes wealthPulse{
  0%,100%{opacity:0.5;}
  50%{opacity:1;}
}

/* Move trail */
.move-trail{
  position:absolute;
  border-radius:50%;
  background:rgba(255,255,255,0.25);
  pointer-events:none;
  animation:trailFade 0.5s ease-out forwards;
  z-index:9;
}
@keyframes trailFade{
  from{opacity:0.8;transform:scale(1);}
  to{opacity:0;transform:scale(2);}
}
</style>
</head>
<body>

<!-- ════════ TOAST CONTAINER ════════ -->
<div id="toast-container"></div>

<!-- ════════ CHARACTER SELECT ════════ -->
<div id="char-select">
  <div class="char-bg-stars" id="stars-container"></div>
  <div class="char-title">🌍 모두의마블</div>
  <div class="char-subtitle">WORLD MARBLE · BOARD GAME</div>
  <div class="char-prompt">캐릭터를 선택하세요</div>
  <div class="char-grid" id="char-grid"></div>
  <button class="char-next-btn" id="char-next-btn" onclick="goToSetup()">다음 →</button>
</div>

<!-- ════════ SETUP ════════ -->
<div id="setup">
  <div class="setup-card">
    <div class="setup-logo">🌍 모두의마블</div>
    <div class="setup-sub">세계 부동산 정복 게임</div>
    <div class="setup-char-preview" id="setup-preview">
      <div class="setup-char-avatar" id="preview-avatar"></div>
      <div class="setup-char-info">
        <div class="setup-char-name" id="preview-name"></div>
        <div class="setup-char-desc" id="preview-desc"></div>
        <div class="setup-char-ability-tag" id="preview-ability"></div>
      </div>
    </div>
    <div class="form-row">
      <label class="form-label">내 닉네임</label>
      <input class="form-input" id="inp-name" value="여행자" maxlength="8" placeholder="닉네임 입력">
    </div>
    <div class="form-row">
      <label class="form-label">AI 플레이어 수</label>
      <select class="form-select" id="inp-bots">
        <option value="1">AI 1명 (2인 게임)</option>
        <option value="2" selected>AI 2명 (3인 게임)</option>
        <option value="3">AI 3명 (4인 게임)</option>
      </select>
    </div>
    <div class="form-row">
      <label class="form-label">난이도</label>
      <select class="form-select" id="inp-diff">
        <option value="easy">🟢 쉬움 — AI 실수 잦음</option>
        <option value="normal" selected>🟡 보통 — 균형 잡힌 플레이</option>
        <option value="hard">🔴 어려움 — 전략적 AI</option>
      </select>
    </div>
    <button class="btn-start" onclick="startGame()">🎲 게임 시작!</button>
    <button class="btn-back-setup" onclick="goBackToChar()">← 캐릭터 변경</button>
    <div class="rules-mini">
      시작자금 <b>₩10,000</b> · 출발 통과 <b>+₩300</b> · 착지 <b>+₩500</b><br>
      독점 시 임료 2배 · 집(최대 4채) → 호텔<br>
      블랙홀: 더블 탈출 또는 보석금 <b>₩600</b><br>
      ✈️ 공항 독점 시 임료 폭증 · 🎰 카지노 베팅 이벤트
    </div>
  </div>
</div>

<!-- ════════ GAME ════════ -->
<div id="game">
  <div class="board-wrap">
    <div id="board"></div>
    <div id="butler">
      <span class="butler-char" id="butler-char"></span>
      <span id="butler-text"></span>
    </div>
  </div>
  <div class="side">
    <div class="side-players">
      <div class="sec-label">🌍 여행자 현황</div>
      <div id="players-list"></div>
    </div>
    <div class="action-zone" id="action-zone"></div>
    <div class="log-wrap">
      <div class="sec-label" style="padding:6px 0 4px;flex-shrink:0">📋 게임 로그</div>
      <div class="log-inner" id="log-area"></div>
    </div>
  </div>
</div>

<!-- ════════ GAME OVER ════════ -->
<div id="gameover">
  <div class="gameover-avatar" id="winner-avatar"></div>
  <div class="gameover-winner" id="winner-name"></div>
  <div class="gameover-sub">세계 정복 완료!</div>
  <div class="rank-card">
    <div id="rank-list"></div>
  </div>
  <button class="btn-restart" onclick="resetToChar()">🔄 다시 하기</button>
</div>

<!-- Tooltip -->
<div class="cell-tooltip" id="tooltip">
  <div class="tooltip-title" id="tt-title"></div>
  <div id="tt-body"></div>
</div>

<script>
// ══════════════════════════════════════════════════════════
//  CHARACTERS
// ══════════════════════════════════════════════════════════
const CHARACTERS = [
  {
    id:0, name:'영웅이',  emoji:'🦸', color:'#3b82f6',
    desc:'안정적인 투자 전략가',
    ability:'첫 매입 10% 할인', abilityKey:'discount',
    butler:'주인님, 신중한 투자가 최고입니다!',
    rgb:'59,130,246'
  },
  {
    id:1, name:'마법사',  emoji:'🧙', color:'#a855f7',
    desc:'카드 운이 좋은 마법사',
    ability:'불리한 카드 1회 무효', abilityKey:'card_immune',
    butler:'마법으로 운명을 바꾸겠습니다!',
    rgb:'168,85,247'
  },
  {
    id:2, name:'공주님',  emoji:'👸', color:'#ec4899',
    desc:'럭셔리 자산 전문가',
    ability:'임료 수입 10% 추가', abilityKey:'rent_bonus',
    butler:'품위 있게, 그리고 부유하게!',
    rgb:'236,72,153'
  },
  {
    id:3, name:'로봇',    emoji:'🤖', color:'#6b7280',
    desc:'완벽하게 계산된 전략',
    ability:'세금 1회 면제', abilityKey:'tax_immune',
    butler:'확률 계산 완료. 최적 루트 선택.',
    rgb:'107,114,128'
  },
  {
    id:4, name:'여우',    emoji:'🦊', color:'#f97316',
    desc:'빠르고 영리한 상인',
    ability:'이동 +1칸 1회 사용', abilityKey:'speed_boost',
    butler:'빠르게 움직여야 기회를 잡죠!',
    rgb:'249,115,22'
  },
  {
    id:5, name:'용사',    emoji:'⚔️', color:'#22c55e',
    desc:'적극적인 개척자',
    ability:'상대 임료 50% 차감 1회', abilityKey:'rent_cut',
    butler:'두려움 없이 전진이다!',
    rgb:'34,197,94'
  },
];

// ══════════════════════════════════════════════════════════
//  WORLD CITIES BOARD (40 cells)
// ══════════════════════════════════════════════════════════
const CELLS = [
  // --- BOTTOM ROW (0-10) ---
  {name:'출발',      type:'go',      price:0,    rent:0,   group:-1, color:'',        flag:'🚩', country:''},
  {name:'서울',      type:'prop',    price:600,  rent:60,  group:0,  color:'#ef4444', flag:'🇰🇷', country:'한국'},
  {name:'찬스',      type:'chance',  price:0,    rent:0,   group:-1, color:'',        flag:'❓', country:''},
  {name:'도쿄',      type:'prop',    price:600,  rent:60,  group:0,  color:'#ef4444', flag:'🇯🇵', country:'일본'},
  {name:'소득세',    type:'tax',     price:200,  rent:0,   group:-1, color:'',        flag:'💸', country:''},
  {name:'✈️ 인천',   type:'airport', price:400,  rent:100, group:-1, color:'',        flag:'✈️', country:'공항'},
  {name:'방콕',      type:'prop',    price:800,  rent:80,  group:1,  color:'#a855f7', flag:'🇹🇭', country:'태국'},
  {name:'운명',      type:'fate',    price:0,    rent:0,   group:-1, color:'',        flag:'⭐', country:''},
  {name:'싱가포르',  type:'prop',    price:900,  rent:90,  group:1,  color:'#a855f7', flag:'🇸🇬', country:'싱가포르'},
  {name:'상하이',    type:'prop',    price:1000, rent:100, group:1,  color:'#a855f7', flag:'🇨🇳', country:'중국'},
  // --- LEFT COLUMN (10-20) ---
  {name:'여행',      type:'visit',   price:0,    rent:0,   group:-1, color:'',        flag:'✈️', country:''},
  {name:'두바이',    type:'prop',    price:1000, rent:100, group:2,  color:'#f97316', flag:'🇦🇪', country:'UAE'},
  {name:'⚡ 전기',   type:'util',    price:300,  rent:0,   group:-1, color:'',        flag:'⚡', country:'공용'},
  {name:'카이로',    type:'prop',    price:1100, rent:110, group:2,  color:'#f97316', flag:'🇪🇬', country:'이집트'},
  {name:'뭄바이',    type:'prop',    price:1200, rent:120, group:2,  color:'#f97316', flag:'🇮🇳', country:'인도'},
  {name:'✈️ 파리',   type:'airport', price:400,  rent:100, group:-1, color:'',        flag:'✈️', country:'공항'},
  {name:'파리',      type:'prop',    price:1400, rent:140, group:3,  color:'#ec4899', flag:'🇫🇷', country:'프랑스'},
  {name:'찬스',      type:'chance',  price:0,    rent:0,   group:-1, color:'',        flag:'❓', country:''},
  {name:'베를린',    type:'prop',    price:1500, rent:150, group:3,  color:'#ec4899', flag:'🇩🇪', country:'독일'},
  {name:'런던',      type:'prop',    price:1600, rent:160, group:3,  color:'#ec4899', flag:'🇬🇧', country:'영국'},
  // --- TOP ROW (20-30) ---
  {name:'블랙홀',    type:'jail',    price:0,    rent:0,   group:-1, color:'',        flag:'⚫', country:''},
  {name:'로마',      type:'prop',    price:1600, rent:160, group:4,  color:'#22c55e', flag:'🇮🇹', country:'이탈리아'},
  {name:'운명',      type:'fate',    price:0,    rent:0,   group:-1, color:'',        flag:'⭐', country:''},
  {name:'마드리드',  type:'prop',    price:1700, rent:170, group:4,  color:'#22c55e', flag:'🇪🇸', country:'스페인'},
  {name:'바르셀로나',type:'prop',    price:1800, rent:180, group:4,  color:'#22c55e', flag:'🇪🇸', country:'스페인'},
  {name:'✈️ JFK',    type:'airport', price:400,  rent:100, group:-1, color:'',        flag:'✈️', country:'공항'},
  {name:'뉴욕',      type:'prop',    price:2000, rent:200, group:5,  color:'#3b82f6', flag:'🇺🇸', country:'미국'},
  {name:'찬스',      type:'chance',  price:0,    rent:0,   group:-1, color:'',        flag:'❓', country:''},
  {name:'시카고',    type:'prop',    price:2100, rent:210, group:5,  color:'#3b82f6', flag:'🇺🇸', country:'미국'},
  {name:'LA',        type:'prop',    price:2200, rent:220, group:5,  color:'#3b82f6', flag:'🇺🇸', country:'미국'},
  // --- RIGHT COLUMN (30-40) ---
  {name:'무료주차',  type:'free',    price:0,    rent:0,   group:-1, color:'',        flag:'🅿️', country:''},
  {name:'라스베가스',type:'casino',  price:0,    rent:0,   group:-1, color:'',        flag:'🎰', country:'미국'},
  {name:'운명',      type:'fate',    price:0,    rent:0,   group:-1, color:'',        flag:'⭐', country:''},
  {name:'토론토',    type:'prop',    price:2200, rent:220, group:6,  color:'#fbbf24', flag:'🇨🇦', country:'캐나다'},
  {name:'상파울루',  type:'prop',    price:2400, rent:240, group:6,  color:'#fbbf24', flag:'🇧🇷', country:'브라질'},
  {name:'✈️ SYD',    type:'airport', price:400,  rent:100, group:-1, color:'',        flag:'✈️', country:'공항'},
  {name:'시드니',    type:'prop',    price:2600, rent:260, group:7,  color:'#06b6d4', flag:'🇦🇺', country:'호주'},
  {name:'🔥 오일',   type:'util',    price:300,  rent:0,   group:-1, color:'',        flag:'🔥', country:'공용'},
  {name:'멜버른',    type:'prop',    price:2800, rent:280, group:7,  color:'#06b6d4', flag:'🇦🇺', country:'호주'},
  {name:'사치세',    type:'tax',     price:400,  rent:0,   group:-1, color:'',        flag:'💎', country:''},
];

const GRP_SIZE    = {0:2, 1:3, 2:3, 3:3, 4:3, 5:3, 6:2, 7:2};
const BUILD_COST  = {0:200,1:250,2:300,3:350,4:400,5:450,6:500,7:600};
const RENT_MULT   = [1, 5, 15, 45, 80];
const PCOLORS     = ['#3b82f6','#ec4899','#22c55e','#f97316'];
const PCHARS      = [null,null,null,null]; // filled from BOT_CHAR_IDS
const BOT_NAMES   = ['알파','베타','감마'];
const DICE_FACES  = ['⚀','⚁','⚂','⚃','⚄','⚅'];
const JAIL_BAIL   = 600;
const START_MONEY = 10000;
const PASS_GO     = 300;
const GO_LAND     = 500;

// ── Chance Cards ──
const CHANCE_CARDS = [
  {emoji:'💰', text:'은행 배당금!',             type:'money',   amount:200},
  {emoji:'📋', text:'세금 환급!',               type:'money',   amount:250},
  {emoji:'🎂', text:'생일! 모두에게 받기',      type:'birthday',amount:100},
  {emoji:'🔧', text:'수리비 청구서',            type:'money',   amount:-180},
  {emoji:'🏥', text:'의료비 지출',              type:'money',   amount:-250},
  {emoji:'📚', text:'학교 수업료',              type:'money',   amount:-300},
  {emoji:'📈', text:'주식 투자 대박!',          type:'money',   amount:400},
  {emoji:'🚩', text:'출발로 GO! +₩300',        type:'goto',    target:0},
  {emoji:'⚫', text:'블랙홀로 빠져든다!',       type:'goto_jail'},
  {emoji:'⬅️', text:'뒤로 3칸 이동',           type:'move',    amount:-3},
  {emoji:'➡️', text:'앞으로 5칸 이동',          type:'move',    amount:5},
  {emoji:'✈️', text:'가장 가까운 공항으로!',    type:'nearest_airport'},
  {emoji:'🔨', text:'건물 수리비: 집×50 호텔×150', type:'repair'},
  {emoji:'🏦', text:'은행 전산 오류! +₩700',   type:'money',   amount:700},
  {emoji:'🌧️', text:'보험료 납부',              type:'money',   amount:-150},
  {emoji:'🎶', text:'콘서트 수익!',             type:'money',   amount:350},
];

// ── Fate Cards ──
const FATE_CARDS = [
  {emoji:'🎫', text:'복권 당첨! 대박!',         type:'money',   amount:500},
  {emoji:'🚦', text:'과태료',                   type:'money',   amount:-100},
  {emoji:'💊', text:'보험금 수령',              type:'money',   amount:200},
  {emoji:'🚗', text:'자동차 수리비',            type:'money',   amount:-200},
  {emoji:'🎵', text:'콘서트 대성공!',           type:'money',   amount:300},
  {emoji:'✈️', text:'여행 경비 지출',           type:'money',   amount:-180},
  {emoji:'🚩', text:'출발로 GO! +₩300',        type:'goto',    target:0},
  {emoji:'⚫', text:'블랙홀로 순간이동!',       type:'goto_jail'},
  {emoji:'➡️', text:'앞으로 4칸!',             type:'move',    amount:4},
  {emoji:'🎂', text:'생일! 모두에게 받기',      type:'birthday',amount:100},
  {emoji:'💸', text:'탈세 적발! 벌금',         type:'money',   amount:-350},
  {emoji:'🏦', text:'은행 이자 지급',           type:'money',   amount:400},
  {emoji:'🌈', text:'행운! 다음 임료 면제',     type:'special', special:'rent_free'},
  {emoji:'🎁', text:'깜짝 선물! 모두에게 지급', type:'birthday',amount:80},
  {emoji:'🏅', text:'사업 성공 보너스',         type:'money',   amount:600},
];

// ── Butler Messages ──
const BUTLER_MSGS = {
  buy:       ['훌륭한 선택입니다!','좋은 투자예요!','마음에 드는군요!'],
  pass:      ['다음 기회에...','신중하시군요.','때를 기다리세요.'],
  rent_in:   ['통행료 수입!','부동산이 돈을 법니다!','수익 창출!'],
  rent_out:  ['아이고, 임료를...','피해야 했는데...','잘 내셨습니다...'],
  jail:      ['블랙홀로!','잠시 구금되셨군요.','곧 탈출하세요!'],
  double:    ['더블! 한번 더!','행운이 따르네요!','연속 이동!'],
  triple:    ['3연속 더블! 블랙홀!','너무 과하셨어요...'],
  build:     ['건설 완료! 임료↑','훌륭한 투자입니다!','이제 돈이 쏟아집니다!'],
  bankrupt:  ['파산하셨습니다...','다음엔 꼭 이기세요!'],
  win:       ['세계 정복 완료!','역시 주인님!','대단합니다!'],
  go_pass:   ['출발 통과! +₩300!','보너스 획득!'],
  go_land:   ['출발 착지! +₩500!','대박 보너스!'],
  casino:    ['🎰 라스베가스에 오신 것을!','운에 맡겨보세요!'],
  airport:   ['✈️ 공항 도착!','여행이 계속됩니다!'],
};

// ══════════════════════════════════════════════════════════
//  STATE
// ══════════════════════════════════════════════════════════
let G = null;
let selectedChar = null;
let mgrOpen      = false;
let butlerTmr    = null;
let animating    = false;
let boardSize    = 560;
let maxNetWorth  = START_MONEY;

// ══════════════════════════════════════════════════════════
//  STARS INIT
// ══════════════════════════════════════════════════════════
function initStars() {
  const container = document.getElementById('stars-container');
  for (let i = 0; i < 80; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = 1 + Math.random() * 2.5;
    s.style.cssText = `
      left:${Math.random()*100}%;
      top:${Math.random()*100}%;
      width:${size}px;height:${size}px;
      --dur:${1.5 + Math.random()*3}s;
      --op:${0.4 + Math.random()*0.6};
      animation-delay:${Math.random()*3}s;
    `;
    container.appendChild(s);
  }
}

// ══════════════════════════════════════════════════════════
//  CHARACTER SELECT
// ══════════════════════════════════════════════════════════
function renderCharGrid() {
  const grid = document.getElementById('char-grid');
  grid.innerHTML = CHARACTERS.map(c => `
    <div class="char-card" id="char-card-${c.id}"
         style="--char-color:${c.color};--char-rgb:${c.rgb}"
         onclick="selectChar(${c.id})">
      <div class="selected-check">✓</div>
      <div class="char-avatar">${c.emoji}</div>
      <div class="char-name" style="color:${c.color}">${c.name}</div>
      <div class="char-desc">${c.desc}</div>
      <div class="char-ability">✨ ${c.ability}</div>
    </div>
  `).join('');
}

function selectChar(id) {
  selectedChar = CHARACTERS[id];
  document.querySelectorAll('.char-card').forEach(el => el.classList.remove('selected'));
  document.getElementById('char-card-' + id).classList.add('selected');
  const btn = document.getElementById('char-next-btn');
  btn.classList.add('active');
  playSound('click');
}

function goToSetup() {
  if (!selectedChar) return;
  document.getElementById('char-select').style.display = 'none';
  const setup = document.getElementById('setup');
  setup.style.display = 'flex';
  // Update preview
  document.getElementById('preview-avatar').textContent  = selectedChar.emoji;
  document.getElementById('preview-name').textContent    = selectedChar.name;
  document.getElementById('preview-desc').textContent    = selectedChar.desc;
  document.getElementById('preview-ability').textContent = '✨ ' + selectedChar.ability;
  document.getElementById('preview-name').style.color    = selectedChar.color;
}

function goBackToChar() {
  document.getElementById('setup').style.display = 'none';
  document.getElementById('char-select').style.display = 'flex';
}

// ══════════════════════════════════════════════════════════
//  GAME INIT
// ══════════════════════════════════════════════════════════
function newCells() {
  return CELLS.map(c => ({
    ...c,
    owner:null, houses:0, mortgaged:false
  }));
}

function pickBotChar(exclude) {
  const available = CHARACTERS.filter(c => c.id !== exclude);
  return available[Math.floor(Math.random() * available.length)];
}

function initGame(playerName, botCount, diff) {
  const char0 = selectedChar || CHARACTERS[0];
  const players = [{
    name:     playerName,
    money:    START_MONEY,
    pos:      0,
    color:    char0.color,
    char:     char0,
    is_bot:   false,
    bankrupt: false,
    jail_turns: 0,
    ability_used: false,
    rent_free: false,
  }];
  const usedCharIds = new Set([char0.id]);
  for (let i = 0; i < botCount; i++) {
    let bc;
    do { bc = pickBotChar(-1); } while (usedCharIds.has(bc.id));
    usedCharIds.add(bc.id);
    players.push({
      name:     BOT_NAMES[i],
      money:    START_MONEY,
      pos:      0,
      color:    PCOLORS[i+1] || PCOLORS[0],
      char:     bc,
      is_bot:   true,
      bankrupt: false,
      jail_turns: 0,
      ability_used: false,
      rent_free: false,
    });
  }
  return {
    players,
    cells:    newCells(),
    turn:     0,
    doubles:  0,
    phase:    'roll',
    log:      [],
    diff,
    pending_card: null,
    winner:   null,
    d1: 1, d2: 1,
  };
}

// ══════════════════════════════════════════════════════════
//  BUTLER
// ══════════════════════════════════════════════════════════
function butler(key, customMsg) {
  const msgs = BUTLER_MSGS[key] || ['...'];
  const msg  = customMsg || msgs[Math.floor(Math.random() * msgs.length)];
  const el   = document.getElementById('butler');
  const txt  = document.getElementById('butler-text');
  const chr  = document.getElementById('butler-char');
  if (!G) return;
  const p    = G.players[G.turn];
  txt.textContent = msg;
  chr.textContent = p.char.emoji;
  el.style.display = 'block';
  if (butlerTmr) clearTimeout(butlerTmr);
  butlerTmr = setTimeout(() => { el.style.display = 'none'; }, 3500);
}

// ══════════════════════════════════════════════════════════
//  GAME LOGIC
// ══════════════════════════════════════════════════════════
function log(msg, style='') {
  G.log.unshift({msg, style});
  if (G.log.length > 120) G.log.length = 120;
}

function alive() { return G.players.filter(p => !p.bankrupt); }

function checkWin() {
  const a = alive();
  if (a.length === 1) {
    G.winner = a[0].name;
    G.winnerIdx = G.players.indexOf(a[0]);
    G.phase = 'gameover';
    return true;
  }
  return false;
}

function ownsGroup(pidx, grp) {
  if (grp < 0) return false;
  const total = GRP_SIZE[grp] || 0;
  return G.cells.filter(c => c.group === grp && c.owner === pidx).length === total;
}

function getNetWorth(pidx) {
  const p = G.players[pidx];
  let nw = p.money;
  G.cells.forEach((c,ci) => {
    if (c.owner !== pidx) return;
    nw += c.mortgaged ? Math.floor(c.price * 0.5) : c.price;
    nw += (c.houses || 0) * (BUILD_COST[c.group] || 300);
  });
  return nw;
}

function calcRent(ci, roll) {
  const c = G.cells[ci];
  if (!c || c.owner === null || c.mortgaged) return 0;
  const {type, owner, houses, rent, group} = c;
  if (type === 'prop') {
    const h = Math.min(houses||0, 4);
    if (h === 0 && ownsGroup(owner, group)) return rent * 2;
    return rent * RENT_MULT[h];
  }
  if (type === 'airport') {
    const n = G.cells.filter(c2 => c2.type==='airport' && c2.owner===owner).length;
    return 100 * (n * n);
  }
  if (type === 'util') {
    const n = G.cells.filter(c2 => c2.type==='util' && c2.owner===owner).length;
    const r = roll || (Math.floor(Math.random()*11)+2);
    return r * (n === 1 ? 4 : 12);
  }
  return 0;
}

function nearestAirport(pos) {
  const airports = [5,15,25,35];
  return airports.reduce((b,r) => ((r-pos+40)%40) < ((b-pos+40)%40) ? r : b);
}

function movePlayer(pidx, steps) {
  const p = G.players[pidx];
  const old = p.pos;
  const nw  = ((old + steps) % 40 + 40) % 40;
  if (steps > 0 && nw <= old && nw !== old) {
    p.money += PASS_GO;
    log(`🚩 ${p.name} 출발 통과! +₩${PASS_GO}`, 'gain');
    butler('go_pass');
    toast(`+₩${PASS_GO} 출발 통과!`, 'gain');
  }
  p.pos = nw;
}

function sendToJail(pidx) {
  const p = G.players[pidx];
  p.pos = 20;
  p.jail_turns = 3;
  log(`⚫ ${p.name} 블랙홀!`, 'lose');
  butler('jail');
  toast('⚫ 블랙홀!', 'lose');
}

function payRent(fromIdx, toIdx, amt) {
  const payer = G.players[fromIdx];
  const recv  = G.players[toIdx];
  // Ability: rent_free
  if (payer.rent_free) {
    payer.rent_free = false;
    log(`🌈 ${payer.name} 행운! 임료 면제!`, 'gain');
    toast('🌈 임료 면제!', 'gain');
    return;
  }
  // Ability: rent_cut (defender)
  let actual = amt;
  if (payer.char.abilityKey === 'rent_cut' && !payer.ability_used) {
    actual = Math.floor(amt * 0.5);
    payer.ability_used = true;
    log(`⚔️ ${payer.name} 특수기술! 임료 50% 감면!`, 'gain');
    toast('⚔️ 임료 50% 감면!', 'gain');
  }
  // Ability: rent_bonus (receiver)
  let recvAmt = actual;
  if (recv.char.abilityKey === 'rent_bonus') {
    recvAmt = Math.floor(actual * 1.1);
  }
  const pay = Math.min(actual, Math.max(0, payer.money));
  payer.money -= pay;
  recv.money  += Math.min(recvAmt, pay);
  log(`💸 ${payer.name}→${recv.name}: ₩${pay}`, 'lose');
  if (fromIdx === 0) butler('rent_out'); else butler('rent_in');
  spawnFloatText(`-₩${pay}`, payer.color, true);
  spawnFloatText(`+₩${Math.min(recvAmt,pay)}`, recv.color, false);
  checkBankrupt(fromIdx);
}

function checkBankrupt(pidx) {
  const p = G.players[pidx];
  if (p.money >= 0) return;
  // Emergency mortgage
  for (let ci=0; ci<G.cells.length; ci++) {
    const c = G.cells[ci];
    if (c.owner===pidx && !c.mortgaged && (c.houses||0)===0 && p.money<0) {
      const val = Math.floor(c.price*0.5);
      c.mortgaged = true;
      p.money += val;
      log(`📋 ${p.name} ${c.name} 긴급저당 +₩${val}`, 'lose');
    }
  }
  if (p.money < 0) {
    p.bankrupt = true;
    p.money = 0;
    G.cells.forEach(c => { if(c.owner===pidx){c.owner=null;c.houses=0;c.mortgaged=false;} });
    log(`💀 ${p.name} 파산!`, 'important');
    butler('bankrupt');
    toast(`💀 ${p.name} 파산!`, 'lose');
    checkWin();
  }
}

function doMortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner!==pidx || c.mortgaged || (c.houses||0)>0) return;
  const val = Math.floor(c.price*0.5);
  c.mortgaged = true;
  p.money += val;
  log(`📋 ${p.name} ${c.name} 저당 +₩${val}`, 'lose');
  renderAll();
}

function doUnmortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner!==pidx || !c.mortgaged) return;
  const cost = Math.floor(c.price*0.6);
  if (p.money < cost) return;
  c.mortgaged = false;
  p.money -= cost;
  log(`✅ ${p.name} ${c.name} 저당해제 -₩${cost}`);
  renderAll();
}

function doBuild(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  const cost = BUILD_COST[c.group] || 300;
  if (p.money<cost || (c.houses||0)>=4 || c.mortgaged) return;
  c.houses = (c.houses||0) + 1;
  p.money -= cost;
  const lbl = c.houses===4 ? '호텔🏨' : `집 ${c.houses}채🏠`;
  log(`🔨 ${p.name} ${c.name} ${lbl} -₩${cost}`);
  butler('build');
  toast(`🏠 ${c.name} ${lbl}!`, 'gain');
  renderAll();
}

// ── Ability use (player) ──
function useAbility() {
  if (!G || animating) return;
  const pidx = G.turn, p = G.players[pidx];
  if (p.is_bot || p.ability_used || p.bankrupt) return;
  const key = p.char.abilityKey;
  if (key === 'discount') {
    // next purchase 10% off - handled in doBuy
    p.ability_used = true;
    p._discount_pending = true;
    log(`✨ ${p.name} 능력 사용: 다음 매입 10% 할인!`, 'important');
    toast(`✨ 할인 능력 사용!`, 'special');
    renderAll();
  } else if (key === 'speed_boost') {
    if (G.phase !== 'roll') return;
    p.ability_used = true;
    log(`✨ ${p.name} 능력 사용: +1칸 이동!`, 'important');
    toast('✨ 이동 +1칸!', 'special');
    // Add 1 to next roll — handled via flag
    p._speed_boost = true;
    renderAll();
  } else if (key === 'card_immune') {
    p.ability_used = true;
    p._card_immune = true;
    log(`✨ ${p.name} 능력 사용: 다음 카드 무효!`, 'important');
    toast('✨ 카드 무효 준비!', 'special');
    renderAll();
  } else if (key === 'tax_immune') {
    p.ability_used = true;
    p._tax_immune = true;
    log(`✨ ${p.name} 능력 사용: 다음 세금 면제!`, 'important');
    toast('✨ 세금 면제 준비!', 'special');
    renderAll();
  }
}

function applyCard(pidx, card) {
  const p = G.players[pidx];
  // card_immune ability
  if (p._card_immune && (card.type==='money'&&card.amount<0 || card.type==='goto_jail' || card.type==='repair')) {
    p._card_immune = false;
    log(`🧙 ${p.name} 카드 마법으로 무효화!`, 'gain');
    toast('🧙 카드 무효화!', 'gain');
    if (G.phase !== 'gameover') G.phase = 'roll';
    return;
  }
  const {type, amount, target} = card;
  if (type === 'money') {
    // tax_immune
    if (amount < 0 && p._tax_immune) {
      p._tax_immune = false;
      log(`🤖 ${p.name} 세금 면제!`, 'gain');
      toast('🤖 세금 면제!', 'gain');
    } else {
      p.money += amount;
      log(`🃏 ${p.name}: ${card.text} (${amount>0?'+':''}${amount})`, amount>0?'gain':'lose');
      spawnFloatText(`${amount>0?'+':''}₩${Math.abs(amount)}`, p.color, amount<0);
      if (amount < 0) checkBankrupt(pidx);
    }
  } else if (type === 'birthday') {
    G.players.forEach((o,i) => {
      if (i!==pidx && !o.bankrupt) {
        const a = Math.min(amount, Math.max(0, o.money));
        o.money -= a;
        p.money += a;
      }
    });
    log(`🎂 ${p.name} 생일! 각자 ₩${amount}`, 'gain');
    toast(`🎂 생일! +₩${(alive().length-1)*amount}`, 'gain');
  } else if (type === 'goto') {
    if (target===0) p.money += PASS_GO;
    p.pos = target;
    log(`🚀 ${p.name} → ${CELLS[target].name}`, 'move');
    landCell(pidx, 0);
    return;
  } else if (type === 'goto_jail') {
    sendToJail(pidx);
  } else if (type === 'move') {
    movePlayer(pidx, amount);
    log(`👣 ${p.name} ${amount>0?'+':''}${amount}칸`, 'move');
    landCell(pidx, 0);
    return;
  } else if (type === 'nearest_airport') {
    const nr = nearestAirport(p.pos);
    const steps = ((nr - p.pos + 40) % 40) || 40;
    movePlayer(pidx, steps);
    log(`✈️ ${p.name} 공항으로!`, 'move');
    landCell(pidx, 0);
    return;
  } else if (type === 'repair') {
    const h  = G.cells.filter(c=>c.owner===pidx&&(c.houses||0)>0&&c.houses<4).length;
    const ht = G.cells.filter(c=>c.owner===pidx&&c.houses===4).length;
    const cost = h*50 + ht*150;
    p.money -= cost;
    log(`🔧 ${p.name} 수리비 -₩${cost}`, 'lose');
    checkBankrupt(pidx);
  } else if (type === 'special' && card.special === 'rent_free') {
    p.rent_free = true;
    log(`🌈 ${p.name} 다음 임료 면제!`, 'gain');
    toast('🌈 다음 임료 면제!', 'gain');
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

// ── Casino event ──
let pendingCasino = false;

function landCell(pidx, roll) {
  const p   = G.players[pidx];
  const ci  = p.pos;
  const c   = G.cells[ci];
  if (!c) return;
  log(`📍 ${p.name} → ${c.flag||''} ${c.name}`, 'move');

  if (c.type === 'go') {
    p.money += GO_LAND;
    log(`🎉 출발 착지! +₩${GO_LAND}`, 'gain');
    butler('go_land');
    toast(`+₩${GO_LAND} 출발 착지!`, 'gain');
  } else if (['prop','airport','util'].includes(c.type)) {
    if (c.owner === null) {
      G.phase = 'buy';
      return;
    } else if (c.owner === pidx) {
      log(`🏠 자기 소유지`);
    } else {
      if (c.mortgaged) {
        log(`📋 ${c.name} 저당 중`);
      } else {
        const rent = calcRent(ci, roll);
        payRent(pidx, c.owner, rent);
      }
    }
    if (!checkWin()) {}
  } else if (c.type === 'chance' || c.type === 'fate') {
    const pool = c.type === 'chance' ? CHANCE_CARDS : FATE_CARDS;
    G.pending_card = pool[Math.floor(Math.random() * pool.length)];
    G.phase = 'card';
    return;
  } else if (c.type === 'tax') {
    if (p._tax_immune) {
      p._tax_immune = false;
      log(`🤖 ${p.name} 세금 면제!`, 'gain');
      toast('🤖 세금 면제!', 'gain');
    } else {
      p.money -= c.price;
      log(`💸 ${p.name} 세금 -₩${c.price}`, 'lose');
      spawnFloatText(`-₩${c.price}`, p.color, true);
      checkBankrupt(pidx);
    }
  } else if (c.type === 'jail') {
    sendToJail(pidx);
  } else if (c.type === 'casino') {
    G.phase = 'casino';
    return;
  } else {
    log(`✅ ${c.name}`);
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

function nextTurn() {
  if (G.phase === 'gameover') return;
  const n = G.players.length;
  let nxt = (G.turn + 1) % n, att = 0;
  while (G.players[nxt].bankrupt && att < n) { nxt=(nxt+1)%n; att++; }
  G.turn = nxt;
  G.phase = 'roll';
  G.doubles = 0;
}

// ══════════════════════════════════════════════════════════
//  ANIMATIONS
// ══════════════════════════════════════════════════════════
function rollDice() {
  const d1 = Math.floor(Math.random()*6)+1;
  const d2 = Math.floor(Math.random()*6)+1;
  return {d1, d2, total:d1+d2, isDouble:d1===d2};
}

function animateDice(d1, d2, cb) {
  const el1 = document.getElementById('die1');
  const el2 = document.getElementById('die2');
  if (!el1 || !el2) { cb&&cb(); return; }
  el1.classList.add('rolling');
  el2.classList.add('rolling');
  el1.classList.remove('double-glow');
  el2.classList.remove('double-glow');
  let n = 0;
  const iv = setInterval(() => {
    el1.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    el2.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    n++;
    if (n >= 14) {
      clearInterval(iv);
      el1.textContent = DICE_FACES[d1-1];
      el2.textContent = DICE_FACES[d2-1];
      el1.classList.remove('rolling');
      el2.classList.remove('rolling');
      if (d1===d2) {
        el1.classList.add('double-glow');
        el2.classList.add('double-glow');
        spawnDoubleRing();
      }
      cb&&cb();
    }
  }, 55);
}

function spawnDoubleRing() {
  const center = document.querySelector('.board-center');
  if (!center) return;
  const rect = center.getBoundingClientRect();
  const ring = document.createElement('div');
  ring.className = 'double-ring';
  ring.style.cssText = `
    left:${rect.left + rect.width/2}px;
    top:${rect.top + rect.height/2}px;
    width:60px;height:60px;
  `;
  document.body.appendChild(ring);
  setTimeout(() => ring.remove(), 900);
}

function animateMove(pidx, from, to, cb) {
  if (from === to) { cb&&cb(); return; }
  const steps = [];
  let cur = from;
  while (cur !== to) { cur=(cur+1)%40; steps.push(cur); }
  let i = 0;
  const iv = setInterval(() => {
    G.players[pidx].pos = steps[i];
    spawnTrail(steps[i]);
    renderTokens();
    i++;
    if (i >= steps.length) { clearInterval(iv); cb&&cb(); }
  }, 110);
}

function spawnTrail(ci) {
  const tc = document.getElementById('tc-'+ci);
  if (!tc) return;
  const rect = tc.getBoundingClientRect();
  const trail = document.createElement('div');
  trail.className = 'move-trail';
  const size = 12;
  trail.style.cssText = `
    left:${rect.left + rect.width/2 - size/2}px;
    top:${rect.top + rect.height/2 - size/2}px;
    width:${size}px;height:${size}px;
    position:fixed;z-index:11;
  `;
  document.body.appendChild(trail);
  setTimeout(() => trail.remove(), 600);
}

// ══════════════════════════════════════════════════════════
//  FLOATING TEXT & EFFECTS
// ══════════════════════════════════════════════════════════
let floatSide = 0;
function spawnFloatText(text, color, isLoss) {
  const el = document.createElement('div');
  el.className = 'float-text';
  const x = window.innerWidth/2 + (floatSide % 2 === 0 ? -80 : 80);
  floatSide++;
  el.style.cssText = `
    left:${x}px;
    top:${window.innerHeight/2 - 60}px;
    color:${isLoss ? '#f87171' : '#4ade80'};
    text-shadow:0 2px 8px rgba(0,0,0,0.6);
  `;
  el.textContent = text;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 1300);
}

function toast(msg, type='') {
  const container = document.getElementById('toast-container');
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = msg;
  container.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}

function spawnCoinsFly(fromColor) {
  for (let i=0; i<6; i++) {
    const coin = document.createElement('div');
    coin.className = 'coin';
    const angle = (Math.random()*180 - 90) * (Math.PI/180);
    const dist  = 60 + Math.random()*80;
    const mx    = Math.cos(angle) * dist/2;
    const my    = -dist/2;
    const ex    = Math.cos(angle) * dist;
    const ey    = -dist;
    coin.style.cssText = `
      left:${window.innerWidth/2 + (Math.random()-0.5)*100}px;
      top:${window.innerHeight/2}px;
      --mx:${mx}px;--my:${my}px;
      --ex:${ex}px;--ey:${ey}px;
      --dur:${0.5 + Math.random()*0.5}s;
      animation-delay:${i*0.05}s;
    `;
    coin.textContent = '🪙';
    document.body.appendChild(coin);
    setTimeout(() => coin.remove(), 1200);
  }
}

// ══════════════════════════════════════════════════════════
//  PLAYER ACTIONS
// ══════════════════════════════════════════════════════════
function doRoll() {
  if (!G || animating) return;
  animating = true;
  const p = G.players[G.turn];
  let {d1, d2, total, isDouble} = rollDice();
  // Speed boost ability
  if (p._speed_boost) {
    total++;
    p._speed_boost = false;
    toast('✨ +1칸 이동!', 'special');
  }
  G.d1 = d1; G.d2 = d2;
  playSound('roll');
  renderDiceCenter();
  animateDice(d1, d2, () => {
    if (isDouble) {
      G.doubles++;
      if (G.doubles >= 3) {
        log(`3연속 더블! ${p.name} 블랙홀!`, 'important');
        butler('triple');
        toast('3연속 더블! 블랙홀!', 'lose');
        sendToJail(G.turn);
        G.doubles = 0;
        nextTurn();
        animating = false;
        renderAll();
        setTimeout(checkBotTurn, 600);
        return;
      }
      log(`🎲 더블! (${d1}+${d2})`);
      butler('double');
      toast(`🎲 더블!`, 'special');
    } else {
      G.doubles = 0;
      log(`🎲 ${d1}+${d2}=${total}`);
    }
    const from = p.pos;
    renderAll();
    setTimeout(() => {
      animateMove(G.turn, from, (from+total)%40, () => {
        movePlayer(G.turn, total);
        landCell(G.turn, total);
        animating = false;
        if (!isDouble && G.phase!=='buy' && G.phase!=='card' && G.phase!=='casino' && G.phase!=='gameover')
          nextTurn();
        renderAll();
        if (G.phase === 'gameover') showGameOver();
      });
    }, 200);
  });
}

function doBuy(buy) {
  const pidx  = G.turn;
  const ci    = G.players[pidx].pos;
  const cell  = G.cells[ci];
  const p     = G.players[pidx];
  if (buy) {
    let price = cell.price;
    // discount ability
    if (p._discount_pending) {
      price = Math.floor(price * 0.9);
      p._discount_pending = false;
      log(`✨ ${p.name} 10% 할인 매입!`, 'gain');
      toast(`✨ 10% 할인! -₩${cell.price - price}`, 'gain');
    }
    cell.owner   = pidx;
    p.money -= price;
    log(`🏠 ${p.name} ${cell.flag||''} ${cell.name} 매입 -₩${price}`, 'lose');
    butler('buy');
    playSound('buy');
  } else {
    log(`↩️ ${p.name} ${cell.name} 패스`);
    butler('pass');
  }
  G.phase = 'roll';
  nextTurn();
  renderAll();
  setTimeout(checkBotTurn, 500);
}

function doCard() {
  if (!G || !G.pending_card) return;
  playSound('card');
  applyCard(G.turn, G.pending_card);
  G.pending_card = null;
  if (G.phase !== 'gameover') {
    nextTurn();
    renderAll();
    setTimeout(checkBotTurn, 500);
  } else {
    renderAll();
    showGameOver();
  }
}

function doJail(payBail) {
  if (!G) return;
  const p = G.players[G.turn];
  if (payBail) {
    if (p.money < JAIL_BAIL) return;
    p.money -= JAIL_BAIL;
    p.jail_turns = 0;
    log(`💰 ${p.name} 보석금 납부!`, 'lose');
    renderAll();
    setTimeout(doRoll, 300);
  } else {
    if (animating) return;
    animating = true;
    const {d1,d2,total,isDouble} = rollDice();
    G.d1=d1; G.d2=d2;
    renderDiceCenter();
    animateDice(d1, d2, () => {
      if (isDouble) {
        p.jail_turns = 0;
        log(`🎉 더블 탈출!`);
        toast('🎉 더블 탈출!', 'gain');
        animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
          movePlayer(G.turn, total);
          landCell(G.turn, total);
          if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='casino'&&G.phase!=='gameover') nextTurn();
          animating = false;
          renderAll();
          if (G.phase==='gameover') showGameOver();
          else setTimeout(checkBotTurn, 600);
        });
      } else {
        p.jail_turns--;
        log(`😔 더블 실패 (${p.jail_turns}턴 남음)`);
        if (p.jail_turns <= 0) {
          p.jail_turns = 0;
          animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
            movePlayer(G.turn, total);
            landCell(G.turn, total);
            if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='casino'&&G.phase!=='gameover') nextTurn();
            animating = false;
            renderAll();
            if (G.phase==='gameover') showGameOver();
            else setTimeout(checkBotTurn, 600);
          });
        } else {
          nextTurn();
          animating = false;
          renderAll();
          setTimeout(checkBotTurn, 500);
        }
      }
    });
  }
}

// Casino handler
function doCasino(bet) {
  const pidx = G.turn, p = G.players[pidx];
  const casinoBet = 300;
  if (!bet) {
    log(`🎰 ${p.name} 베팅 거부`);
    G.phase = 'roll';
    nextTurn();
    renderAll();
    setTimeout(checkBotTurn, 400);
    return;
  }
  if (p.money < casinoBet) {
    toast('💸 베팅금 부족!', 'lose');
    G.phase = 'roll';
    nextTurn();
    renderAll();
    setTimeout(checkBotTurn, 400);
    return;
  }
  p.money -= casinoBet;
  playSound('casino');
  const win = Math.random() < 0.45;
  if (win) {
    p.money += casinoBet * 3;
    log(`🎰 ${p.name} 🎉 대박! +₩${casinoBet*2}`, 'gain');
    toast(`🎰 대박! +₩${casinoBet*2}`, 'gain');
    spawnFloatText(`+₩${casinoBet*2}`, p.color, false);
    spawnCoinsFly(p.color);
  } else {
    log(`🎰 ${p.name} 💸 꽝! -₩${casinoBet}`, 'lose');
    toast(`🎰 꽝! -₩${casinoBet}`, 'lose');
    spawnFloatText(`-₩${casinoBet}`, p.color, true);
    checkBankrupt(pidx);
  }
  G.phase = 'roll';
  if (G.phase !== 'gameover') nextTurn();
  renderAll();
  if (G.phase === 'gameover') showGameOver();
  else setTimeout(checkBotTurn, 500);
}

// ══════════════════════════════════════════════════════════
//  BOT AI
// ══════════════════════════════════════════════════════════
function checkBotTurn() {
  if (!G || G.phase==='gameover') return;
  const p = G.players[G.turn];
  if (p.is_bot && !p.bankrupt) doBotTurn();
}

function doBotTurn() {
  setTimeout(() => {
    if (!G || G.phase==='gameover') return;
    const pidx = G.turn, p = G.players[pidx];
    if (!p.is_bot || p.bankrupt) return;

    // Bot auto-use ability occasionally
    if (!p.ability_used && Math.random() < 0.25) {
      const key = p.char.abilityKey;
      if (key==='tax_immune' || key==='card_immune' || key==='rent_cut') {
        p.ability_used = true;
        if (key==='tax_immune') p._tax_immune = true;
        if (key==='card_immune') p._card_immune = true;
        // rent_cut activated on demand in payRent
      }
    }

    if (p.jail_turns>0 && G.phase==='roll') {
      if (G.diff==='hard' && p.money>=JAIL_BAIL) {
        p.money -= JAIL_BAIL;
        p.jail_turns = 0;
        log(`💰 ${p.name} 보석금!`, 'lose');
        renderAll();
        setTimeout(() => doBotRoll(pidx), 400);
      } else {
        const {d1,d2,total,isDouble} = rollDice();
        G.d1=d1; G.d2=d2;
        if (isDouble) {
          p.jail_turns=0;
          log(`🎉 ${p.name} 더블 탈출!`);
          renderAll();
          animateMove(pidx, p.pos, (p.pos+total)%40, () => {
            movePlayer(pidx, total); landCell(pidx, total);
            botDecide(pidx);
            if (G.phase!=='gameover') nextTurn();
            renderAll();
            G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 600);
          });
        } else {
          p.jail_turns--;
          log(`😔 ${p.name} 더블 실패`);
          if (p.jail_turns<=0) {
            p.jail_turns=0; renderAll();
            animateMove(pidx, p.pos, (p.pos+total)%40, () => {
              movePlayer(pidx, total); landCell(pidx, total);
              botDecide(pidx);
              if (G.phase!=='gameover') nextTurn();
              renderAll();
              G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 600);
            });
          } else {
            nextTurn(); renderAll(); setTimeout(checkBotTurn, 500);
          }
        }
      }
      return;
    }

    if (G.phase==='buy' || G.phase==='card') {
      botDecide(pidx);
      if (G.phase!=='gameover') nextTurn();
      renderAll();
      G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 500);
      return;
    }

    if (G.phase==='casino') {
      // Bot casino decision
      const casinoBet = 300;
      if (G.diff==='hard' && p.money >= casinoBet * 2) {
        doCasino(true);
      } else if (G.diff==='normal' && p.money >= casinoBet && Math.random() < 0.5) {
        doCasino(true);
      } else {
        doCasino(false);
      }
      return;
    }

    if (G.phase==='roll') {
      botBuildSmart(pidx);
      doBotRoll(pidx);
    }
  }, 700);
}

function doBotRoll(pidx) {
  if (!G || G.phase==='gameover') return;
  const p = G.players[pidx];
  const {d1, d2, total, isDouble} = rollDice();
  G.d1=d1; G.d2=d2;
  if (isDouble) {
    G.doubles++;
    if (G.doubles>=3) {
      log(`3연속 더블! ${p.name} 블랙홀!`, 'important');
      butler('triple');
      sendToJail(pidx);
      G.doubles=0;
      nextTurn();
      renderAll();
      setTimeout(checkBotTurn, 600);
      return;
    }
    log(`🎲 ${p.name} 더블! (${d1}+${d2})`);
  } else {
    G.doubles=0;
    log(`🎲 ${p.name} ${d1}+${d2}=${total}`);
  }
  renderAll();
  const from = p.pos;
  setTimeout(() => {
    animateMove(pidx, from, (from+total)%40, () => {
      movePlayer(pidx, total);
      landCell(pidx, total);
      botDecide(pidx);
      if (!isDouble && G.phase!=='gameover') nextTurn();
      renderAll();
      if (G.phase==='gameover') showGameOver();
      else if (isDouble && G.phase==='roll') setTimeout(() => doBotRoll(pidx), 800);
      else setTimeout(checkBotTurn, 600);
    });
  }, 200);
}

function botDecide(pidx) {
  const p = G.players[pidx], diff = G.diff;
  if (G.phase==='buy') {
    const ci = p.pos, cell=G.cells[ci], price=cell.price;
    let buy = false;
    if (diff==='easy') {
      buy = Math.random()>0.3 && p.money>=price;
    } else if (diff==='normal') {
      buy = p.money >= price * 1.4;
    } else {
      const g = cell.group;
      if (g>=0) {
        const have = G.cells.filter(c=>c.group===g&&c.owner===pidx).length;
        if (have===(GRP_SIZE[g]||0)-1 && p.money>=price) buy=true;
        else buy = p.money >= price*1.2;
      } else {
        buy = p.money >= price * 1.1;
      }
    }
    if (buy) {
      cell.owner=pidx; p.money-=price;
      log(`🏠 ${p.name} ${cell.flag||''} ${cell.name} 매입 -₩${price}`, 'lose');
    } else {
      log(`↩️ ${p.name} ${cell.name} 패스`);
    }
    G.phase='roll';
  } else if (G.phase==='card' && G.pending_card) {
    applyCard(pidx, G.pending_card);
    G.pending_card=null;
  } else if (G.phase==='casino') {
    const casinoBet=300;
    if (diff==='hard'&&p.money>=casinoBet*2) {
      doCasino(true); return;
    } else {
      doCasino(false); return;
    }
  }
}

function botBuildSmart(pidx) {
  const p = G.players[pidx], diff=G.diff;
  if (diff==='easy') return;
  G.cells.forEach((c,ci) => {
    if (c.owner!==pidx || c.type!=='prop') return;
    if (!ownsGroup(pidx, c.group) || (c.houses||0)>=4 || c.mortgaged) return;
    const cost = BUILD_COST[c.group]||300;
    const threshold = diff==='hard' ? 1.2 : 1.6;
    if (p.money >= cost * threshold) {
      c.houses=(c.houses||0)+1; p.money-=cost;
      const lbl = c.houses===4?'호텔':'집'+c.houses;
      log(`🔨 ${p.name} ${c.name} ${lbl} -₩${cost}`);
      butler('build');
    }
  });
}

// ══════════════════════════════════════════════════════════
//  BOARD LAYOUT CALCULATIONS
// ══════════════════════════════════════════════════════════
function getCellRect(ci) {
  const S = boardSize;
  const C = S / 7;
  const W = (S - 2*C) / 9;

  if (ci===0)  return {x:S-C,    y:S-C,    w:C, h:C};
  if (ci===10) return {x:0,      y:S-C,    w:C, h:C};
  if (ci===20) return {x:0,      y:0,      w:C, h:C};
  if (ci===30) return {x:S-C,    y:0,      w:C, h:C};

  if (ci<10) {
    const idx = 10-ci;
    return {x:S-C-idx*W, y:S-C, w:W, h:C};
  }
  if (ci<20) {
    const idx = ci-10;
    return {x:0, y:S-C-idx*W, w:C, h:W};
  }
  if (ci<30) {
    const idx = ci-20;
    return {x:C+(idx-1)*W, y:0, w:W, h:C};
  }
  const idx = ci-30;
  return {x:S-C, y:C+(idx-1)*W, w:C, h:W};
}

// ══════════════════════════════════════════════════════════
//  BUILD BOARD DOM
// ══════════════════════════════════════════════════════════
function buildBoard() {
  const boardEl = document.getElementById('board');
  const S = boardSize;
  boardEl.style.width  = S+'px';
  boardEl.style.height = S+'px';
  boardEl.innerHTML = '';

  const C  = S/7;
  const W  = (S-2*C)/9;
  const fs = Math.max(6, Math.round(S/80));

  const cellBg = {
    go:     'linear-gradient(135deg,#0a2015,#0c2818)',
    jail:   'linear-gradient(135deg,#1a0835,#12052a)',
    visit:  'linear-gradient(135deg,#0a1830,#0c2040)',
    free:   'linear-gradient(135deg,#0a1a0a,#0c200e)',
    chance: 'linear-gradient(135deg,#1a1030,#12082a)',
    fate:   'linear-gradient(135deg,#280a12,#1e0810)',
    tax:    'linear-gradient(135deg,#281808,#1e1206)',
    airport:'linear-gradient(135deg,#0a1828,#0c2038)',
    util:   'linear-gradient(135deg,#0a2010,#0c2816)',
    prop:   'linear-gradient(135deg,#0d1025,#0a0d20)',
    casino: 'linear-gradient(135deg,#1a100a,#28180a)',
  };

  for (let ci=0; ci<40; ci++) {
    const {x,y,w,h} = getCellRect(ci);
    const cellData = G.cells[ci];
    const isCorner = ci===0||ci===10||ci===20||ci===30;
    const isHoriz  = ci<10||ci>=30;
    const isLeft   = ci>=10&&ci<20;
    const isTop    = ci>=20&&ci<30;

    const div = document.createElement('div');
    div.className = 'cell' + (isCorner?' cell-corner':'');
    div.id = 'cell-'+ci;
    div.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;
    div.style.background = cellBg[cellData.type]||cellBg.prop;

    // Special class for casino
    if (cellData.type==='casino') div.classList.add('casino-glow');
    if (cellData.type==='jail') div.classList.add('blackhole-pulse');

    // Color bar for properties
    if (cellData.color && cellData.type==='prop') {
      const bar = document.createElement('div');
      bar.className = 'color-bar';
      bar.id = 'bar-'+ci;
      bar.style.background = cellData.color;
      const bThick = Math.round(Math.min(h,w) * 0.18);
      if (isHoriz) {
        bar.style.cssText = `top:0;left:0;width:100%;height:${bThick}px;background:${cellData.color};opacity:0.9;`;
      } else if (isLeft) {
        bar.style.cssText = `top:0;right:0;width:${bThick}px;height:100%;background:${cellData.color};opacity:0.9;`;
      } else if (isTop) {
        bar.style.cssText = `bottom:0;left:0;width:100%;height:${bThick}px;background:${cellData.color};opacity:0.9;`;
      }
      div.appendChild(bar);
    }

    // Airport bar
    if (cellData.type==='airport') {
      const bar = document.createElement('div');
      bar.className = 'airport-bar';
      if (isHoriz) {
        bar.style.cssText = `top:0;left:0;width:100%;height:${Math.round(Math.min(h,w)*0.18)}px;`;
      } else {
        bar.style.cssText = `top:0;right:0;width:${Math.round(Math.min(w,h)*0.18)}px;height:100%;`;
      }
      div.appendChild(bar);
    }

    // Text wrap
    const tw = document.createElement('div');
    tw.id = 'tw-'+ci;
    tw.style.cssText = `position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;gap:1px;z-index:1;`;

    // Icon/flag
    const iconMap = {
      go:'🚩', jail:'⚫', visit:'✈️', free:'🅿️',
      chance:'❓', fate:'⭐', tax:'💸',
      airport:'✈️', casino:'🎰',
    };
    let icon = cellData.flag || iconMap[cellData.type] || '';
    if (cellData.type==='util') {
      icon = cellData.name.includes('전기') ? '⚡' : '🔥';
    }
    if (cellData.type==='prop') icon = cellData.flag || '';

    if (icon) {
      const iconEl = document.createElement('div');
      iconEl.className = 'cell-icon';
      iconEl.textContent = icon;
      const iconFs = isCorner ? Math.round(fs*2.2) : Math.round(fs*1.5);
      iconEl.style.fontSize = iconFs + 'px';
      tw.appendChild(iconEl);
    }

    const nameEl = document.createElement('div');
    nameEl.className = 'cell-name';
    nameEl.id = 'cn-'+ci;
    const short = cellData.name.length>4 ? cellData.name.slice(0,4) : cellData.name;
    nameEl.textContent = isCorner ? cellData.name : short;
    nameEl.style.fontSize = (isCorner ? fs+2 : fs) + 'px';
    nameEl.style.padding = '0 1px';
    tw.appendChild(nameEl);

    if (cellData.price>0 && !isCorner) {
      const priceEl = document.createElement('div');
      priceEl.className = 'cell-price';
      priceEl.textContent = cellData.price.toLocaleString();
      priceEl.style.fontSize = Math.max(5,fs-1)+'px';
      priceEl.style.opacity = '0.7';
      tw.appendChild(priceEl);
    }

    div.appendChild(tw);

    // Houses indicator
    const housesEl = document.createElement('div');
    housesEl.id = 'houses-'+ci;
    housesEl.style.cssText = `position:absolute;display:flex;gap:1px;align-items:center;z-index:2;`;
    if (isHoriz) {
      housesEl.style.bottom='2px';
      housesEl.style.left='50%';
      housesEl.style.transform='translateX(-50%)';
    } else {
      housesEl.style.left='2px';
      housesEl.style.top='50%';
      housesEl.style.flexDirection='column';
      housesEl.style.transform='translateY(-50%)';
    }
    div.appendChild(housesEl);

    // Owner badge
    const badge = document.createElement('div');
    badge.className='owner-badge';
    badge.id='ob-'+ci;
    const badgeSize = Math.max(5, Math.round(fs*0.7));
    badge.style.cssText = `width:${badgeSize}px;height:${badgeSize}px;display:none;top:2px;right:2px;position:absolute;z-index:3;border-radius:50%;border:1px solid rgba(0,0,0,0.5);`;
    div.appendChild(badge);

    // Mortgaged overlay
    const mort = document.createElement('div');
    mort.className='mortgaged-overlay';
    mort.id='mo-'+ci;
    mort.style.cssText='display:none;';
    mort.textContent='저당';
    mort.style.fontSize = Math.max(5,fs-1)+'px';
    div.appendChild(mort);

    div.addEventListener('mouseenter', e=>showTooltip(ci,e));
    div.addEventListener('mouseleave', hideTooltip);
    boardEl.appendChild(div);
  }

  // Center area
  const C2=C;
  const center = document.createElement('div');
  center.className='board-center';
  center.style.cssText=`left:${C2}px;top:${C2}px;width:${S-2*C2}px;height:${S-2*C2}px;`;
  const logoFs = Math.round(S/13);
  const dieSize = Math.round(S/11);
  const diceFs  = Math.round(dieSize*0.55);
  center.innerHTML=`
    <div class="board-logo" style="font-size:${logoFs}px;">🌍<br>모두의마블</div>
    <div class="board-sub" style="font-size:${Math.round(S/90)}px;margin-bottom:10px;">WORLD MARBLE</div>
    <div class="dice-center">
      <div class="die-face" id="die1" style="width:${dieSize}px;height:${dieSize}px;font-size:${diceFs}px;">⚀</div>
      <div class="die-face" id="die2" style="width:${dieSize}px;height:${dieSize}px;font-size:${diceFs}px;">⚁</div>
    </div>
  `;
  boardEl.appendChild(center);

  // Token clusters
  for (let ci=0; ci<40; ci++) {
    const {x,y,w,h} = getCellRect(ci);
    const cluster = document.createElement('div');
    cluster.className='token-cluster';
    cluster.id='tc-'+ci;
    cluster.style.cssText=`left:${x}px;top:${y}px;width:${w}px;height:${h}px;position:absolute;`;
    boardEl.appendChild(cluster);
  }
}

// ══════════════════════════════════════════════════════════
//  RENDER FUNCTIONS
// ══════════════════════════════════════════════════════════
function renderBoard() {
  if (!G) return;
  const S  = boardSize;
  const FS = Math.max(6, Math.round(S/80));

  G.cells.forEach((c,ci) => {
    // Houses
    const housesEl = document.getElementById('houses-'+ci);
    if (housesEl) {
      housesEl.innerHTML='';
      if (c.type==='prop' && (c.houses||0)>0 && !c.mortgaged) {
        if (c.houses===4) {
          const h=document.createElement('div');
          h.className='hotel-marker';
          h.style.width=Math.round(FS*1.5)+'px';
          h.style.height=Math.round(FS*1.0)+'px';
          housesEl.appendChild(h);
        } else {
          for (let i=0;i<c.houses;i++) {
            const hd=document.createElement('div');
            hd.className='house-dot';
            hd.style.width=hd.style.height=Math.round(FS*0.85)+'px';
            housesEl.appendChild(hd);
          }
        }
      }
    }

    // Owner badge
    const ob = document.getElementById('ob-'+ci);
    if (ob) {
      if (c.owner!==null && !c.mortgaged) {
        ob.style.display='block';
        ob.style.background=G.players[c.owner].color;
        ob.style.boxShadow=`0 0 8px ${G.players[c.owner].color}`;
      } else {
        ob.style.display='none';
      }
    }

    // Mortgaged
    const mo = document.getElementById('mo-'+ci);
    if (mo) mo.style.display = c.mortgaged?'flex':'none';
  });
}

function renderDiceCenter() {
  const el1=document.getElementById('die1');
  const el2=document.getElementById('die2');
  if (el1) el1.textContent=DICE_FACES[(G.d1||1)-1];
  if (el2) el2.textContent=DICE_FACES[(G.d2||1)-1];
}

function renderTokens() {
  for (let ci=0;ci<40;ci++) {
    const tc=document.getElementById('tc-'+ci);
    if (tc) tc.innerHTML='';
  }
  const slotMap={};
  G.players.forEach((p,pi) => {
    if (p.bankrupt) return;
    const slot=slotMap[p.pos]||0;
    slotMap[p.pos]=slot+1;
    const tc=document.getElementById('tc-'+p.pos);
    if (!tc) return;
    const tk=document.createElement('div');
    tk.className='token';
    const isActive = pi===G.turn && !animating;
    if (isActive) {
      tk.classList.add('active-token');
      tk.style.setProperty('--tok-color', p.color);
    }
    const tSize=Math.max(14,Math.round(boardSize/36));
    tk.style.cssText=`
      width:${tSize}px;height:${tSize}px;
      background:${p.color};
      font-size:${Math.round(tSize*0.6)}px;
      border-color:rgba(255,255,255,0.9);
    `;
    tk.textContent = p.char.emoji;
    tc.appendChild(tk);
  });
}

function renderPlayers() {
  const el=document.getElementById('players-list');
  if (!el||!G) return;

  // compute max net worth for bars
  const nws = G.players.map((_,i)=>getNetWorth(i));
  const maxNW = Math.max(...nws, START_MONEY);

  el.innerHTML = G.players.map((p,i) => {
    const isAct = i===G.turn && !p.bankrupt;
    const nw = nws[i];
    const nwPct = Math.round((nw/maxNW)*100);
    const jailBadge = p.jail_turns>0
      ? `<span class="badge-jail">⚫${p.jail_turns}</span>` : '';
    const abilBadge = !p.ability_used && !p.is_bot
      ? `<span class="badge-ability">✨능력</span>` : '';
    if (p.bankrupt) {
      return `
      <div class="player-card bankrupt" style="--p-color:${p.color}">
        <div class="player-avatar" style="opacity:0.4">${p.char.emoji}</div>
        <div class="player-info">
          <div class="player-name-row">
            <span class="player-name-txt" style="color:${p.color}">${p.name}</span>
            <span class="badge-bankrupt">💀파산</span>
          </div>
          <div class="player-money" style="color:#555">₩0</div>
        </div>
      </div>`;
    }
    return `
    <div class="player-card${isAct?' active':''}" style="--p-color:${p.color}">
      <div class="player-avatar">${p.char.emoji}</div>
      <div class="player-info">
        <div class="player-name-row">
          <span class="player-name-txt" style="color:${p.color}">${p.name}</span>
          ${p.is_bot?'<span class="bot-badge">AI</span>':''}
          ${jailBadge}
          ${abilBadge}
        </div>
        <div class="player-money">₩${p.money.toLocaleString()}</div>
        <div class="net-worth-bar">
          <div class="net-worth-fill" style="width:${nwPct}%;background:${p.color}"></div>
        </div>
      </div>
    </div>`;
  }).join('');
}

function renderAction() {
  const az=document.getElementById('action-zone');
  if (!az||!G) return;
  const pidx=G.turn, p=G.players[pidx], phase=G.phase;

  let html=`
    <div class="turn-banner" style="color:${p.color}">
      <span class="turn-avatar">${p.char.emoji}</span>
      ${p.name}${p.is_bot?' AI':''} 차례
    </div>`;
  html+=`
    <div class="dice-display">
      <div class="dice-mini${G.d1===G.d2?' double-mini':''}">${DICE_FACES[(G.d1||1)-1]}</div>
      <div class="dice-mini${G.d1===G.d2?' double-mini':''}">${DICE_FACES[(G.d2||1)-1]}</div>
    </div>`;

  if (p.is_bot) {
    html+=`<div class="info-box">🤖 AI 처리 중...</div>`;
    az.innerHTML=html;
    return;
  }
  if (p.bankrupt) { az.innerHTML=html; return; }

  if (phase==='roll') {
    // Jail check
    if (p.jail_turns>0) {
      html+=`<div class="info-box">⚫ 블랙홀 구금 (${p.jail_turns}턴 남음)<br>보석금: ₩${JAIL_BAIL}</div>`;
      html+=`<div class="btn-row">
        <button class="btn btn-orange" onclick="doJail(true)" ${p.money<JAIL_BAIL?'disabled':''}>💰 보석금</button>
        <button class="btn btn-roll" style="flex:1.5" onclick="doJail(false)">🎲 더블 도전</button>
      </div>`;
    } else {
      // Ability button
      if (!p.ability_used) {
        html+=`<button class="btn btn-purple" onclick="useAbility()">✨ ${p.char.ability}</button>`;
      }
      html+=`<button class="btn btn-roll" onclick="doRoll()" ${animating?'disabled':''}>🎲 주사위 굴리기!</button>`;
      html+=`
        <button class="mgr-toggle${mgrOpen?' open':''}" onclick="toggleMgr()">
          🏗️ 부동산 관리
          <span class="mgr-toggle-arrow">▼</span>
        </button>
        <div class="mgr-list${mgrOpen?' open':''}" id="mgr-list"></div>`;
    }
  } else if (phase==='buy') {
    const ci=p.pos, cell=G.cells[ci];
    const ico=cell.flag||'🏠';
    const rentTable=[
      ['기본 임료', `₩${cell.rent}`],
      ['독점 임료', `₩${cell.rent*2}`],
      ['집 1채', `₩${cell.rent*RENT_MULT[1]}`],
      ['집 2채', `₩${cell.rent*RENT_MULT[2]}`],
      ['집 3채', `₩${cell.rent*RENT_MULT[3]}`],
      ['호텔', `₩${cell.rent*RENT_MULT[4]}`],
    ];
    const rentHtml = (cell.type==='prop')
      ? rentTable.map(r=>`<div class="prop-card-rent-row"><span>${r[0]}</span><span>${r[1]}</span></div>`).join('')
      : '';
    html+=`
      <div class="prop-card-popup" style="--card-color:${cell.color||'rgba(255,215,0,0.15)'}">
        <div class="prop-card-color-band" style="background:${cell.color||'linear-gradient(90deg,#ffd700,#ff6b35)'}"></div>
        <div class="prop-card-flag">${ico}</div>
        <div class="prop-card-city">${cell.name}</div>
        <div class="prop-card-country">${cell.country||''}</div>
        <div class="prop-card-price">₩${cell.price.toLocaleString()}</div>
        ${rentHtml}
      </div>
      <button class="btn btn-green" onclick="doBuy(true)" ${p.money<cell.price?'disabled':''}>
        ✅ 매입! -₩${cell.price.toLocaleString()}
      </button>
      <button class="btn btn-ghost" onclick="doBuy(false)">↩️ 패스</button>`;
  } else if (phase==='card' && G.pending_card) {
    const card=G.pending_card;
    const amtHtml = card.amount!==undefined
      ? `<div class="card-effect ${card.amount>0?'gain':'lose'}">${card.amount>0?'+':''}₩${Math.abs(card.amount)}</div>`
      : `<div class="card-effect">${card.type==='goto_jail'?'⚫ 블랙홀!':card.type==='nearest_airport'?'✈️ 공항으로!':card.type==='special'?'🌈 특별 혜택!':''}</div>`;
    html+=`
      <div class="card-box">
        <div class="card-emoji">${card.emoji}</div>
        <div class="card-title">${card.text}</div>
        ${amtHtml}
      </div>
      <button class="btn btn-roll" onclick="doCard()">확인!</button>`;
  } else if (phase==='casino') {
    const casinoBet=300;
    html+=`
      <div class="casino-box">
        <div class="casino-title">🎰 라스베가스 카지노!</div>
        <div class="casino-desc">행운에 도전하세요!<br>당첨 확률 45% · 당첨 시 3배 지급</div>
        <div class="casino-amount">베팅: ₩${casinoBet.toLocaleString()}</div>
      </div>
      <div class="btn-row">
        <button class="btn btn-roll" onclick="doCasino(true)" ${p.money<casinoBet?'disabled':''}>🎲 베팅!</button>
        <button class="btn btn-ghost" onclick="doCasino(false)">패스</button>
      </div>`;
  }

  az.innerHTML=html;
  if (phase==='roll' && !p.jail_turns && mgrOpen) renderMgr();
}

function toggleMgr() {
  mgrOpen=!mgrOpen;
  renderAction();
}

function renderMgr() {
  const el=document.getElementById('mgr-list');
  if (!el) return;
  const pidx=G.turn, p=G.players[pidx];
  const mine=G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx);
  if (!mine.length) {
    el.innerHTML=`<div style="font-size:0.68rem;color:var(--text3);padding:4px 2px">소유 부동산 없음</div>`;
    return;
  }
  el.innerHTML=mine.map(({c,ci})=>{
    if (!['prop','airport','util'].includes(c.type)) return '';
    const canBuild=c.type==='prop'&&ownsGroup(pidx,c.group)&&!c.mortgaged&&(c.houses||0)<4;
    const cost=BUILD_COST[c.group]||300;
    const dotStyle=c.color?`background:${c.color}`:`background:#555`;
    let hIcons='';
    if (c.houses===4) hIcons='<span style="color:#ef4444;font-size:0.6rem">🏨</span>';
    else for(let i=0;i<(c.houses||0);i++) hIcons+='<span style="color:#22c55e;font-size:0.6rem">■</span>';
    return `
    <div class="prop-row">
      <div class="prop-color" style="${dotStyle}"></div>
      <span class="prop-name${c.mortgaged?' mortgaged':''}">${c.flag||''}${c.name}${hIcons}</span>
      <div class="prop-btns">
        ${canBuild&&p.money>=cost?`<button class="mini-b mini-b-build" onclick="doBuild(${pidx},${ci})">${(c.houses||0)===3?'🏨':'🏠'}</button>`:''}
        ${!c.mortgaged&&(c.houses||0)===0?`<button class="mini-b mini-b-mort" onclick="doMortgage(${pidx},${ci})">저당</button>`:''}
        ${c.mortgaged?`<button class="mini-b mini-b-unmort" onclick="doUnmortgage(${pidx},${ci})" ${p.money<Math.floor(c.price*0.6)?'disabled':''}>해제</button>`:''}
      </div>
    </div>`;
  }).join('');
}

function renderLog() {
  const el=document.getElementById('log-area');
  if (!el) return;
  el.innerHTML=G.log.slice(0,50).map(e=>
    `<div class="log-row log-${e.style||''}">${e.msg}</div>`
  ).join('');
}

function renderAll() {
  if (!G) return;
  renderBoard();
  renderTokens();
  renderDiceCenter();
  renderPlayers();
  renderAction();
  renderLog();
}

// ══════════════════════════════════════════════════════════
//  TOOLTIP
// ══════════════════════════════════════════════════════════
function showTooltip(ci, e) {
  if (!G) return;
  const c=G.cells[ci];
  const tt=document.getElementById('tooltip');
  const ttTitle=document.getElementById('tt-title');
  const ttBody=document.getElementById('tt-body');

  let bandHtml='';
  if (c.color) {
    bandHtml=`<span class="tooltip-band" style="background:${c.color}"></span>`;
  }
  ttTitle.innerHTML=`${bandHtml}${c.flag||''} ${c.name}`;

  let rows='';
  if (c.type==='prop') {
    rows+=`<div class="tooltip-row"><span>국가</span><span>${c.country||'-'}</span></div>`;
    rows+=`<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner!==null) {
      rows+=`<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      if (!c.mortgaged) {
        const rent=calcRent(ci,7);
        rows+=`<div class="tooltip-row"><span>현재 임료</span><span style="color:#4ade80">₩${rent.toLocaleString()}</span></div>`;
      }
    }
    if ((c.houses||0)>0) {
      rows+=`<div class="tooltip-row"><span>건물</span><span>${c.houses===4?'🏨 호텔':'🏠 집'+c.houses+'채'}</span></div>`;
    }
    if (c.mortgaged) rows+=`<div class="tooltip-row" style="color:#ef4444"><span>저당 중</span><span>⚠️</span></div>`;
  } else if (c.type==='airport') {
    rows+=`<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner!==null) {
      const n=G.cells.filter(c2=>c2.type==='airport'&&c2.owner===c.owner).length;
      rows+=`<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      rows+=`<div class="tooltip-row"><span>임료</span><span>₩${(100*n*n).toLocaleString()}</span></div>`;
    }
    rows+=`<div class="tooltip-row"><span>1개</span><span>₩100</span></div>`;
    rows+=`<div class="tooltip-row"><span>2개</span><span>₩400</span></div>`;
    rows+=`<div class="tooltip-row"><span>3개</span><span>₩900</span></div>`;
    rows+=`<div class="tooltip-row"><span>4개</span><span>₩1,600</span></div>`;
  } else if (c.type==='tax') {
    rows+=`<div class="tooltip-row"><span>세금</span><span style="color:#f87171">₩${c.price.toLocaleString()}</span></div>`;
  } else if (c.type==='util') {
    rows+=`<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    rows+=`<div class="tooltip-row"><span>1개</span><span>주사위×4</span></div>`;
    rows+=`<div class="tooltip-row"><span>2개</span><span>주사위×12</span></div>`;
  } else if (c.type==='casino') {
    rows+=`<div class="tooltip-row"><span>베팅</span><span>₩300</span></div>`;
    rows+=`<div class="tooltip-row"><span>당첨시</span><span style="color:#4ade80">₩900 (3배)</span></div>`;
    rows+=`<div class="tooltip-row"><span>당첨율</span><span>45%</span></div>`;
  }

  ttBody.innerHTML=rows;
  tt.style.display='block';
  const rect=e.target.getBoundingClientRect();
  let lx=rect.right+10, ly=rect.top;
  if (lx+180>window.innerWidth) lx=rect.left-190;
  if (ly+160>window.innerHeight) ly=window.innerHeight-170;
  tt.style.left=lx+'px';
  tt.style.top=ly+'px';
}

function hideTooltip() {
  document.getElementById('tooltip').style.display='none';
}

// ══════════════════════════════════════════════════════════
//  SOUND EFFECTS (Web Audio API)
// ══════════════════════════════════════════════════════════
let audioCtx = null;
function getAudioCtx() {
  if (!audioCtx) {
    try { audioCtx = new (window.AudioContext||window.webkitAudioContext)(); } catch(e){}
  }
  return audioCtx;
}

function playSound(type) {
  const ctx = getAudioCtx();
  if (!ctx) return;
  try {
    const osc = ctx.createOscillator();
    const gain= ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    const now = ctx.currentTime;
    if (type==='roll') {
      osc.type='square';
      osc.frequency.setValueAtTime(300,now);
      osc.frequency.exponentialRampToValueAtTime(600,now+0.1);
      osc.frequency.exponentialRampToValueAtTime(200,now+0.2);
      gain.gain.setValueAtTime(0.08,now);
      gain.gain.exponentialRampToValueAtTime(0.001,now+0.25);
      osc.start(now);osc.stop(now+0.25);
    } else if (type==='buy') {
      osc.type='sine';
      osc.frequency.setValueAtTime(523,now);
      osc.frequency.setValueAtTime(659,now+0.1);
      osc.frequency.setValueAtTime(784,now+0.2);
      gain.gain.setValueAtTime(0.1,now);
      gain.gain.exponentialRampToValueAtTime(0.001,now+0.4);
      osc.start(now);osc.stop(now+0.4);
    } else if (type==='card') {
      osc.type='triangle';
      osc.frequency.setValueAtTime(440,now);
      osc.frequency.exponentialRampToValueAtTime(880,now+0.15);
      gain.gain.setValueAtTime(0.07,now);
      gain.gain.exponentialRampToValueAtTime(0.001,now+0.3);
      osc.start(now);osc.stop(now+0.3);
    } else if (type==='casino') {
      // Slot machine sound
      osc.type='sawtooth';
      osc.frequency.setValueAtTime(800,now);
      osc.frequency.setValueAtTime(400,now+0.05);
      osc.frequency.setValueAtTime(1200,now+0.1);
      osc.frequency.setValueAtTime(600,now+0.15);
      osc.frequency.setValueAtTime(1600,now+0.2);
      gain.gain.setValueAtTime(0.06,now);
      gain.gain.exponentialRampToValueAtTime(0.001,now+0.3);
      osc.start(now);osc.stop(now+0.3);
    } else if (type==='click') {
      osc.type='sine';
      osc.frequency.setValueAtTime(1000,now);
      osc.frequency.exponentialRampToValueAtTime(600,now+0.05);
      gain.gain.setValueAtTime(0.05,now);
      gain.gain.exponentialRampToValueAtTime(0.001,now+0.08);
      osc.start(now);osc.stop(now+0.08);
    } else if (type==='win') {
      // Fanfare
      const notes=[523,659,784,1047];
      notes.forEach((freq,i) => {
        const o2=ctx.createOscillator();
        const g2=ctx.createGain();
        o2.connect(g2);g2.connect(ctx.destination);
        o2.type='sine';
        o2.frequency.setValueAtTime(freq,now+i*0.12);
        g2.gain.setValueAtTime(0.12,now+i*0.12);
        g2.gain.exponentialRampToValueAtTime(0.001,now+i*0.12+0.25);
        o2.start(now+i*0.12);o2.stop(now+i*0.12+0.25);
      });
    }
  } catch(e){}
}

// ══════════════════════════════════════════════════════════
//  GAME START / OVER / RESET
// ══════════════════════════════════════════════════════════
function startGame() {
  const name = document.getElementById('inp-name').value.trim() || '여행자';
  const bots = parseInt(document.getElementById('inp-bots').value);
  const diff = document.getElementById('inp-diff').value;
  G = initGame(name, bots, diff);

  document.getElementById('setup').style.display='none';
  const gameEl=document.getElementById('game');
  gameEl.style.display='flex';

  setTimeout(() => {
    const bw=document.querySelector('.board-wrap');
    if (bw) {
      const avail=Math.min(bw.offsetWidth-24, bw.offsetHeight-24);
      boardSize=Math.max(340, Math.min(660, avail));
    }
    buildBoard();
    log('🌍 세계 정복 게임 시작!', 'important');
    log('✨ 캐릭터 능력을 잘 활용하세요!');
    renderAll();
    setTimeout(checkBotTurn, 900);
  }, 60);
}

function showGameOver() {
  if (!G||!G.winner) return;
  const winnerP=G.players[G.winnerIdx];
  playSound('win');
  document.getElementById('winner-avatar').textContent=winnerP.char.emoji;
  document.getElementById('winner-name').textContent=`${winnerP.name} 우승!`;

  const ranked=[...G.players].sort((a,b) => getNetWorth(G.players.indexOf(b)) - getNetWorth(G.players.indexOf(a)));
  const medals=['🥇','🥈','🥉','4️⃣'];
  document.getElementById('rank-list').innerHTML=ranked.map((p,i) => {
    const ri=G.players.indexOf(p);
    return `
    <div class="rank-row">
      <span class="rank-medal">${medals[i]||''}</span>
      <span class="rank-avatar">${p.char.emoji}</span>
      <span class="rank-player" style="color:${p.color}">${p.name}</span>
      ${p.bankrupt
        ? `<span class="rank-dead">💀 파산</span>`
        : `<span class="rank-money">₩${getNetWorth(ri).toLocaleString()}</span>`}
    </div>`;
  }).join('');
  document.getElementById('gameover').style.display='flex';
  butler('win');
  spawnConfetti();
}

function resetToChar() {
  G=null; mgrOpen=false; animating=false; selectedChar=null;
  document.getElementById('gameover').style.display='none';
  document.getElementById('game').style.display='none';
  document.getElementById('setup').style.display='none';
  const cs=document.getElementById('char-select');
  cs.style.display='flex';
  // Reset char selection
  document.querySelectorAll('.char-card').forEach(el=>el.classList.remove('selected'));
  document.getElementById('char-next-btn').classList.remove('active');
}

// ══════════════════════════════════════════════════════════
//  CONFETTI
// ══════════════════════════════════════════════════════════
function spawnConfetti() {
  const colors=['#ff4d6d','#3b82f6','#22c55e','#f97316','#a855f7','#ffd700','#14b8a6','#ec4899'];
  const shapes=['50%','4px','0'];
  for (let i=0;i<140;i++) {
    const d=document.createElement('div');
    d.className='confetti-piece';
    const size=4+Math.random()*10;
    const dur=1.8+Math.random()*2.5;
    const delay=Math.random()*2;
    const shape=shapes[Math.floor(Math.random()*shapes.length)];
    d.style.cssText=`
      left:${Math.random()*100}%;
      top:-20px;
      width:${size}px;height:${size*0.6}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      border-radius:${shape};
      animation-duration:${dur}s;
      animation-delay:${delay}s;
    `;
    document.body.appendChild(d);
    setTimeout(()=>d.remove(),(dur+delay+0.5)*1000);
  }
}

// ══════════════════════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════════════════════
window.addEventListener('DOMContentLoaded', () => {
  initStars();
  renderCharGrid();
});
</script>
</body>
</html>
"""

def main():
    st.set_page_config(
        page_title="모두의마블 🌍",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}
    footer{visibility:hidden;}
    header{visibility:hidden;}
    .block-container{
        padding:0 !important;
        max-width:100% !important;
    }
    iframe{border:none;}
    </style>
    """, unsafe_allow_html=True)
    components.html(GAME_HTML, height=820, scrolling=False)

if __name__ == "__main__":
    main()
