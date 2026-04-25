import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>인베스트마블 REMASTERED 🌍</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Black+Han+Sans&family=Fredoka+One&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#05080f;--bg2:#080d1a;--bg3:#0d1525;--bg4:#121d32;
  --glass:rgba(255,255,255,0.03);--glass2:rgba(255,255,255,0.07);
  --border:rgba(255,255,255,0.07);--border2:rgba(255,255,255,0.13);
  --text:#e8f0ff;--text2:#7a8fb5;--text3:#3a4a6b;
  --gold:#ffd700;--gold2:#ffb800;--gold3:#ff9500;
  --green:#10d96e;--red:#ff4560;--blue:#4dabf7;--purple:#b26cf7;
  --orange:#ff8c42;--pink:#f472b6;--teal:#2dd4bf;--cyan:#22d3ee;
  --r:16px;--r2:10px;
  --shadow:0 12px 48px rgba(0,0,0,0.8);--shadow2:0 4px 20px rgba(0,0,0,0.5);
  --glow-gold:0 0 20px rgba(255,215,0,0.3),0 0 60px rgba(255,215,0,0.1);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);overflow:hidden;height:100vh;width:100vw;user-select:none;}
.bg-mesh{position:fixed;inset:0;pointer-events:none;z-index:0;
  background:radial-gradient(ellipse 60% 40% at 20% 20%,rgba(75,0,130,0.12) 0%,transparent 60%),
    radial-gradient(ellipse 50% 60% at 80% 80%,rgba(0,50,120,0.12) 0%,transparent 60%),
    radial-gradient(ellipse 40% 50% at 60% 10%,rgba(200,100,0,0.06) 0%,transparent 50%);
  animation:meshDrift 20s ease-in-out infinite alternate;}
@keyframes meshDrift{0%{filter:hue-rotate(0deg);}100%{filter:hue-rotate(30deg);}}
.star-field{position:fixed;inset:0;pointer-events:none;z-index:0;overflow:hidden;}
.star{position:absolute;background:#fff;border-radius:50%;animation:twinkle var(--dur,2s) ease-in-out infinite;opacity:0;}
@keyframes twinkle{0%,100%{opacity:0;transform:scale(0.5);}50%{opacity:var(--op,0.7);transform:scale(1);}}

/* ── CHARACTER SELECT ── */
#char-select{position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;align-items:center;justify-content:center;}
.char-header{text-align:center;margin-bottom:20px;}
.char-title-main{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,5vw,3.8rem);
  background:linear-gradient(135deg,#ffd700 0%,#ff8c00 35%,#ff4d6d 65%,#c026d3 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  letter-spacing:4px;animation:titleGlow 3s ease-in-out infinite;}
@keyframes titleGlow{0%,100%{filter:drop-shadow(0 0 30px rgba(255,165,0,0.3));}50%{filter:drop-shadow(0 0 60px rgba(255,165,0,0.6));}}
.char-title-sub{font-family:'Orbitron',sans-serif;font-size:0.65rem;color:var(--text3);letter-spacing:6px;text-transform:uppercase;margin-top:4px;}
.char-prompt{color:var(--text2);font-size:0.88rem;font-weight:500;letter-spacing:1px;margin-bottom:12px;}
.char-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:20px;}
.char-card{width:128px;height:170px;border-radius:20px;border:1.5px solid var(--border2);
  background:linear-gradient(160deg,var(--bg3),var(--bg2));
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:6px;
  cursor:pointer;position:relative;overflow:hidden;
  transition:all 0.3s cubic-bezier(0.34,1.56,0.64,1);}
.char-card:hover{transform:translateY(-8px) scale(1.06);border-color:var(--char-color,#3b82f6);
  box-shadow:0 16px 48px rgba(0,0,0,0.6),0 0 40px rgba(var(--char-rgb,59,130,246),0.35);}
.char-card.selected{border-color:var(--char-color,#3b82f6);
  box-shadow:0 0 0 3px var(--char-color,#3b82f6),0 16px 48px rgba(0,0,0,0.7);}
.char-avatar{font-size:3.4rem;animation:charFloat 3s ease-in-out infinite;}
@keyframes charFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-7px);}}
.char-name{font-size:0.88rem;font-weight:800;color:var(--text);}
.char-desc{font-size:0.62rem;color:var(--text3);text-align:center;padding:0 8px;line-height:1.5;}
.char-ability-tag{position:absolute;bottom:0;left:0;right:0;background:linear-gradient(0deg,rgba(0,0,0,0.8),transparent);
  padding:8px 6px 6px;font-size:0.58rem;color:var(--char-color,#3b82f6);text-align:center;border-radius:0 0 20px 20px;}
.selected-check{position:absolute;top:8px;right:8px;width:22px;height:22px;border-radius:50%;
  background:var(--char-color,#3b82f6);display:none;align-items:center;justify-content:center;
  font-size:0.75rem;color:#fff;z-index:2;}
.char-card.selected .selected-check{display:flex;}
.char-rarity{position:absolute;top:8px;left:8px;font-size:0.5rem;letter-spacing:1px;text-transform:uppercase;
  padding:2px 6px;border-radius:4px;background:rgba(0,0,0,0.4);border:1px solid var(--char-color,#3b82f6);
  color:var(--char-color,#3b82f6);z-index:2;}
.char-next-btn{background:linear-gradient(135deg,#ffd700,#ff8c00);border:none;border-radius:16px;
  color:#fff;font-family:'Black Han Sans',sans-serif;font-size:1.1rem;letter-spacing:3px;
  padding:15px 52px;cursor:pointer;box-shadow:0 8px 32px rgba(255,140,0,0.5);
  transition:all 0.25s;opacity:0.35;pointer-events:none;}
.char-next-btn.active{opacity:1;pointer-events:all;}
.char-next-btn.active:hover{transform:translateY(-3px) scale(1.02);}

/* ── SETUP ── */
#setup{position:fixed;inset:0;z-index:150;display:none;flex-direction:column;align-items:center;justify-content:center;}
.setup-card{background:linear-gradient(160deg,var(--bg3),var(--bg2));border:1px solid var(--border2);border-radius:24px;
  padding:34px 32px;width:430px;box-shadow:var(--shadow);}
.setup-logo{font-family:'Black Han Sans',sans-serif;font-size:1.9rem;
  background:linear-gradient(135deg,#ffd700,#ff4d6d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  text-align:center;letter-spacing:3px;margin-bottom:4px;}
.setup-sub{color:var(--text3);font-size:0.65rem;letter-spacing:4px;margin-bottom:20px;text-align:center;text-transform:uppercase;}
.setup-char-preview{display:flex;align-items:center;gap:14px;background:linear-gradient(135deg,var(--bg4),var(--bg3));
  border-radius:14px;padding:14px 18px;margin-bottom:20px;border:1px solid var(--border2);}
.setup-char-avatar{font-size:2.6rem;animation:charFloat 3s ease-in-out infinite;}
.setup-char-name{font-family:'Black Han Sans',sans-serif;font-size:1.05rem;color:var(--gold);}
.setup-char-ability-tag{display:inline-block;margin-top:5px;font-size:0.62rem;padding:3px 10px;border-radius:20px;
  background:rgba(255,215,0,0.1);color:var(--gold2);border:1px solid rgba(255,215,0,0.2);}
.form-row{margin-bottom:14px;}
.form-label{display:block;font-size:0.65rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:2px;margin-bottom:7px;}
.form-input,.form-select{width:100%;background:var(--bg4);border:1.5px solid var(--border2);border-radius:var(--r2);
  color:var(--text);padding:11px 14px;font-size:0.88rem;font-family:'Noto Sans KR',sans-serif;outline:none;transition:border-color 0.2s;}
.form-input:focus,.form-select:focus{border-color:var(--gold);}
.form-select option{background:#0d1525;color:var(--text);}
.btn-start{width:100%;background:linear-gradient(135deg,#ffd700,#ff8c00);border:none;border-radius:14px;color:#fff;
  font-family:'Black Han Sans',sans-serif;font-size:1.1rem;letter-spacing:3px;padding:16px;cursor:pointer;
  margin-top:10px;transition:all 0.2s;box-shadow:0 8px 32px rgba(255,140,0,0.4);}
.btn-start:hover{transform:translateY(-2px);}
.btn-back-setup{background:transparent;border:1px solid var(--border2);border-radius:10px;
  color:var(--text2);font-size:0.8rem;padding:9px 20px;cursor:pointer;margin-top:8px;width:100%;transition:all 0.2s;}
.btn-back-setup:hover{background:var(--glass2);}
.rules-mini{margin-top:16px;background:var(--bg4);border-radius:var(--r2);padding:12px 16px;
  font-size:0.7rem;color:var(--text3);line-height:2;border:1px solid var(--border);}
.rules-mini b{color:var(--text2);}

/* ── GAME LAYOUT ── */
#game{display:none;width:100vw;height:100vh;flex-direction:row;}
.board-wrap{flex:1;display:flex;align-items:center;justify-content:center;padding:10px;min-width:0;position:relative;overflow:hidden;
  background:radial-gradient(ellipse at center,#0c1535 0%,#05080f 100%);}

/* ── BOARD ── */
#board{position:relative;background:linear-gradient(135deg,#060c1c 0%,#0a1228 50%,#060c1c 100%);
  border:2px solid rgba(255,215,0,0.2);border-radius:8px;
  box-shadow:0 0 0 1px rgba(255,215,0,0.07),0 0 100px rgba(255,215,0,0.08),var(--shadow);
  aspect-ratio:1;flex-shrink:0;overflow:hidden;}

/* CELL */
.cell{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;
  border:1px solid rgba(255,255,255,0.04);cursor:default;overflow:hidden;transition:filter 0.2s,transform 0.2s;}
.cell:hover{filter:brightness(1.35);transform:scale(1.02);z-index:5;}
.cell-name{text-align:center;color:#b8cae8;line-height:1.2;font-weight:600;font-size:0;position:relative;z-index:1;}
.cell-price{color:#445577;text-align:center;font-weight:400;font-size:0;position:relative;z-index:1;}
.cell-icon{line-height:1;position:relative;z-index:1;}
.color-bar{position:absolute;z-index:0;opacity:1;}
.cell-corner{background:#050b18 !important;}
.own-ring{position:absolute;inset:1px;border-radius:3px;border:2px solid transparent;pointer-events:none;z-index:4;transition:all 0.3s;}
.house-dot{display:inline-block;background:linear-gradient(135deg,#10d96e,#059a4d);border-radius:2px;}
.hotel-marker{display:inline-block;background:linear-gradient(135deg,#ff4560,#cc2040);border-radius:2px;}
.owner-badge{position:absolute;top:2px;right:2px;border-radius:50%;border:1.5px solid rgba(0,0,0,0.6);z-index:3;}
.mortgaged-overlay{position:absolute;inset:0;background:rgba(0,0,0,0.72);display:none;align-items:center;justify-content:center;
  color:#ff4560;font-weight:700;letter-spacing:1px;z-index:4;}
.airport-bar{position:absolute;background:linear-gradient(90deg,#22d3ee,#4dabf7);opacity:0.85;}
.casino-cell{animation:casinoShimmer 2.5s ease-in-out infinite;}
@keyframes casinoShimmer{0%,100%{box-shadow:inset 0 0 12px rgba(255,215,0,0.1);}50%{box-shadow:inset 0 0 28px rgba(255,215,0,0.3);}}
.jail-cell{animation:jailPulse 3s ease-in-out infinite;}
@keyframes jailPulse{0%,100%{box-shadow:inset 0 0 15px rgba(168,85,247,0.2);}50%{box-shadow:inset 0 0 35px rgba(168,85,247,0.45);}}
.event-cell{animation:eventGlow 2s ease-in-out infinite;}
@keyframes eventGlow{0%,100%{box-shadow:inset 0 0 10px rgba(34,211,238,0.15);}50%{box-shadow:inset 0 0 25px rgba(34,211,238,0.35);}}

/* ── TOKEN ── */
.token-cluster{position:absolute;display:flex;flex-wrap:wrap;gap:2px;align-items:center;justify-content:center;pointer-events:none;z-index:10;}
.token{border-radius:50%;border:2.5px solid rgba(255,255,255,0.95);display:flex;align-items:center;justify-content:center;
  box-shadow:0 3px 14px rgba(0,0,0,0.8);position:relative;transition:all 0.15s;}

/* 이동 중 토큰 점프 애니메이션 */
.token.moving{animation:tokenJump 0.22s ease-in-out;}
@keyframes tokenJump{0%,100%{transform:translateY(0) scale(1);}40%{transform:translateY(-12px) scale(1.15);}70%{transform:translateY(-4px) scale(1.05);}}
.token.active-token{
  box-shadow:0 0 20px var(--tok-color,#fff),0 0 40px rgba(255,255,255,0.2),0 3px 14px rgba(0,0,0,0.8);}
.token.landed{animation:tokenLand 0.35s cubic-bezier(0.34,1.56,0.64,1);}
@keyframes tokenLand{0%{transform:scale(0.6);}60%{transform:scale(1.2);}100%{transform:scale(1);}}
.token::after{content:'';position:absolute;bottom:-5px;left:50%;transform:translateX(-50%);
  width:65%;height:5px;background:rgba(0,0,0,0.35);border-radius:50%;filter:blur(3px);}

/* ── BOARD CENTER ── */
.board-center{position:absolute;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:linear-gradient(135deg,#040810,#070e1e,#040810);overflow:hidden;}
.board-logo{font-family:'Black Han Sans',sans-serif;
  background:linear-gradient(135deg,#ffd700 0%,#ff8c00 40%,#ff4d6d 70%,#c026d3 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  text-align:center;line-height:1.05;letter-spacing:2px;animation:logoPulse 4s ease-in-out infinite;}
@keyframes logoPulse{0%,100%{filter:drop-shadow(0 0 20px rgba(255,215,0,0.25));}50%{filter:drop-shadow(0 0 40px rgba(255,215,0,0.5));}}
.board-sub{color:rgba(255,255,255,0.08);text-align:center;letter-spacing:4px;text-transform:uppercase;}

/* ── 주사위 (크게, 화려하게) ── */
.dice-center{display:flex;gap:14px;position:relative;margin-top:10px;}
.die-face{background:linear-gradient(145deg,#f8f9ff,#dde0f5);border-radius:12px;
  display:flex;align-items:center;justify-content:center;color:#1a1a30;
  box-shadow:inset 0 2px 4px rgba(255,255,255,0.8),inset 0 -3px 6px rgba(0,0,0,0.2),0 6px 20px rgba(0,0,0,0.7);
  transition:transform 0.15s;position:relative;font-weight:700;font-family:'Noto Sans KR',sans-serif;}
.die-face.rolling{animation:diceRoll 0.7s cubic-bezier(0.25,0.46,0.45,0.94);}
.die-face.double-glow{
  box-shadow:inset 0 2px 4px rgba(255,255,255,0.8),0 0 30px rgba(255,215,0,1),0 0 60px rgba(255,215,0,0.6),0 6px 20px rgba(0,0,0,0.7);}
@keyframes diceRoll{
  0%{transform:rotate(0) scale(1);}
  15%{transform:rotate(-30deg) scale(1.3) translateY(-10px);}
  30%{transform:rotate(25deg) scale(1.35) translateY(-14px);}
  50%{transform:rotate(-18deg) scale(1.2) translateY(-7px);}
  70%{transform:rotate(10deg) scale(1.08);}
  85%{transform:rotate(-3deg) scale(1.03);}
  100%{transform:rotate(0) scale(1);}
}
/* 주사위 숫자 표시 (도트 패턴) */
.die-dots{display:grid;width:100%;height:100%;padding:15%;position:relative;}
.dot{background:#1a1a30;border-radius:50%;width:100%;height:100%;}
/* 1도트 */
.dots-1{grid-template-columns:1fr;grid-template-rows:1fr;place-items:center;}
.dots-1 .dot{width:28%;height:28%;}
/* 2도트 */
.dots-2{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:2px;}
.dots-2 .dot:nth-child(1){grid-column:2;grid-row:1;width:70%;height:70%;margin:auto;}
.dots-2 .dot:nth-child(2){grid-column:1;grid-row:2;width:70%;height:70%;margin:auto;}
/* 3도트 */
.dots-3{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:2px;}
.dots-3 .dot:nth-child(1){grid-column:2;grid-row:1;width:70%;height:70%;margin:auto;}
.dots-3 .dot:nth-child(2){grid-column:1;grid-row:2;grid-column:1/3;width:35%;height:35%;margin:auto;}
.dots-3 .dot:nth-child(3){grid-column:1;grid-row:3;width:70%;height:70%;margin:auto;}
/* 4도트 */
.dots-4{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:10%;}
.dots-4 .dot{width:70%;height:70%;margin:auto;}
/* 5도트 */
.dots-5{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:5%;}
.dots-5 .dot:nth-child(1){width:70%;height:70%;margin:auto;}
.dots-5 .dot:nth-child(2){width:70%;height:70%;margin:auto;}
.dots-5 .dot:nth-child(3){grid-column:1/3;width:35%;height:35%;margin:auto;}
.dots-5 .dot:nth-child(4){width:70%;height:70%;margin:auto;}
.dots-5 .dot:nth-child(5){width:70%;height:70%;margin:auto;}
/* 6도트 */
.dots-6{grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr 1fr;gap:8%;}
.dots-6 .dot{width:70%;height:70%;margin:auto;}

/* 주사위 합계 표시 */
.dice-sum{font-family:'Fredoka One',cursive;text-align:center;color:var(--gold);
  animation:sumPop 0.4s cubic-bezier(0.34,1.56,0.64,1);}
@keyframes sumPop{from{opacity:0;transform:scale(0.5);}to{opacity:1;transform:scale(1);}}
.dice-sum.double{color:#fff;text-shadow:0 0 20px var(--gold),0 0 40px rgba(255,165,0,0.5);}

/* ── SIDE PANEL ── */
.side{width:256px;background:var(--bg2);border-left:1px solid var(--border);display:flex;flex-direction:column;overflow:hidden;flex-shrink:0;}
.side-players{padding:12px 13px 8px;border-bottom:1px solid var(--border);flex-shrink:0;}
.sec-label{font-size:0.57rem;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:2.5px;margin-bottom:10px;display:flex;align-items:center;gap:6px;}
.sec-label::after{content:'';flex:1;height:1px;background:var(--border);}
.player-card{display:flex;align-items:center;gap:9px;padding:8px 9px;border-radius:11px;transition:all 0.25s;margin-bottom:4px;position:relative;overflow:hidden;}
.player-card::before{content:'';position:absolute;inset:0;background:var(--p-color,#fff);opacity:0;transition:opacity 0.25s;border-radius:11px;}
.player-card.active::before{opacity:0.07;}
.player-card.active{box-shadow:0 0 0 1.5px var(--p-color,#fff),0 6px 20px rgba(0,0,0,0.4);}
.player-avatar{font-size:1.35rem;flex-shrink:0;position:relative;z-index:1;}
.player-card.active .player-avatar{animation:avatarPulse 1.8s ease-in-out infinite;}
@keyframes avatarPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.18) translateY(-2px);}}
.player-info{flex:1;min-width:0;position:relative;z-index:1;}
.player-name-row{display:flex;align-items:center;gap:4px;}
.player-name-txt{font-size:0.78rem;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;}
.bot-badge{font-size:0.52rem;background:rgba(255,255,255,0.07);color:var(--text3);border-radius:4px;padding:1px 4px;flex-shrink:0;}
.player-money{font-family:'Fredoka One',cursive;font-size:0.94rem;color:var(--green);margin-top:1px;transition:color 0.3s;}
.net-worth-bar{height:3px;border-radius:2px;background:rgba(255,255,255,0.06);margin-top:5px;overflow:hidden;}
.net-worth-fill{height:100%;border-radius:2px;background:linear-gradient(90deg,var(--p-color,#22c55e),rgba(255,255,255,0.4));transition:width 0.7s cubic-bezier(0.4,0,0.2,1);}
.player-badges{display:flex;gap:3px;margin-top:3px;flex-wrap:wrap;position:relative;z-index:1;}
.badge-jail{font-size:0.52rem;background:rgba(255,69,96,0.15);color:#ff4560;border-radius:4px;padding:1px 5px;border:1px solid rgba(255,69,96,0.2);}
.badge-bankrupt{font-size:0.52rem;background:rgba(100,100,100,0.15);color:#666;border-radius:4px;padding:1px 5px;}
.badge-ability{font-size:0.52rem;background:rgba(255,215,0,0.12);color:var(--gold);border-radius:4px;padding:1px 5px;border:1px solid rgba(255,215,0,0.2);}
.badge-trade{font-size:0.52rem;background:rgba(34,211,238,0.12);color:var(--cyan);border-radius:4px;padding:1px 5px;}
.player-card.bankrupt{opacity:0.4;}
.player-card.bankrupt .player-name-txt{text-decoration:line-through;}

/* ACTION ZONE */
.action-zone{flex:1;padding:11px 13px;overflow-y:auto;display:flex;flex-direction:column;gap:8px;min-height:0;}
.action-zone::-webkit-scrollbar{width:3px;}
.action-zone::-webkit-scrollbar-thumb{background:var(--border2);border-radius:2px;}
.turn-banner{text-align:center;font-size:0.67rem;font-weight:700;padding:2px 0;color:var(--text2);display:flex;align-items:center;justify-content:center;gap:5px;}
.turn-avatar{font-size:1.1rem;animation:charFloat 2s ease-in-out infinite;}

/* 주사위 패널 (사이드바) - 크게 강조 */
.dice-panel{background:linear-gradient(135deg,var(--bg3),var(--bg4));border:1px solid var(--border2);border-radius:14px;
  padding:12px;text-align:center;position:relative;overflow:hidden;}
.dice-panel::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse at center top,rgba(255,215,0,0.05),transparent 60%);pointer-events:none;}
.dice-panel-row{display:flex;justify-content:center;gap:12px;align-items:center;margin-bottom:6px;}
.die-side{background:linear-gradient(145deg,#f8f9ff,#dde0f5);border-radius:10px;
  display:flex;align-items:center;justify-content:center;
  box-shadow:inset 0 2px 4px rgba(255,255,255,0.9),0 4px 14px rgba(0,0,0,0.6);}
.die-side.double-side{box-shadow:inset 0 2px 4px rgba(255,255,255,0.9),0 0 20px rgba(255,215,0,1),0 4px 14px rgba(0,0,0,0.6);}
.dice-result{font-family:'Fredoka One',cursive;font-size:1rem;color:var(--text2);margin-top:2px;}
.dice-result .total-num{font-size:1.5rem;color:var(--gold);margin:0 4px;}
.dice-result.is-double .total-num{color:#fff;text-shadow:0 0 16px var(--gold);}
.dice-double-badge{display:inline-block;font-size:0.6rem;background:linear-gradient(135deg,var(--gold),var(--gold3));
  color:#1a0a00;border-radius:20px;padding:2px 8px;font-weight:700;letter-spacing:1px;margin-left:4px;vertical-align:middle;}

/* Buttons */
.btn{border:none;border-radius:var(--r2);padding:10px 14px;font-family:'Noto Sans KR',sans-serif;font-size:0.8rem;font-weight:700;cursor:pointer;transition:all 0.18s;width:100%;position:relative;overflow:hidden;}
.btn:active:not(:disabled){transform:scale(0.95);}
.btn:disabled{opacity:0.28;cursor:not-allowed;}
.btn-roll{background:linear-gradient(135deg,#ff4560,#c01030);color:#fff;box-shadow:0 4px 20px rgba(255,69,96,0.4);font-size:0.92rem;padding:14px;}
.btn-roll:hover:not(:disabled){box-shadow:0 8px 32px rgba(255,69,96,0.65);transform:translateY(-2px);}
.btn-green{background:linear-gradient(135deg,#10d96e,#069a4d);color:#fff;box-shadow:0 4px 16px rgba(16,217,110,0.35);}
.btn-green:hover:not(:disabled){transform:translateY(-2px);}
.btn-ghost{background:var(--bg3);color:var(--text2);border:1.5px solid var(--border2);}
.btn-ghost:hover:not(:disabled){background:var(--glass2);color:var(--text);}
.btn-orange{background:linear-gradient(135deg,#ff8c42,#e06018);color:#fff;}
.btn-orange:hover:not(:disabled){transform:translateY(-2px);}
.btn-purple{background:linear-gradient(135deg,#b26cf7,#7c3aed);color:#fff;}
.btn-purple:hover:not(:disabled){transform:translateY(-2px);}
.btn-cyan{background:linear-gradient(135deg,#22d3ee,#0891b2);color:#fff;}
.btn-cyan:hover:not(:disabled){transform:translateY(-2px);}
.btn-gold{background:linear-gradient(135deg,#ffd700,#ff9500);color:#fff;}
.btn-gold:hover:not(:disabled){transform:translateY(-2px);}
.btn-row{display:flex;gap:7px;}
.btn-row .btn{flex:1;}
.info-box{background:linear-gradient(135deg,var(--bg3),var(--bg4));border:1px solid var(--border);border-radius:var(--r2);padding:10px 13px;font-size:0.75rem;color:var(--text2);text-align:center;line-height:1.7;}

/* Property purchase card */
.prop-card-popup{background:linear-gradient(160deg,var(--bg3),var(--bg2));border:1px solid rgba(255,215,0,0.2);border-radius:18px;
  padding:16px;text-align:center;animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);position:relative;overflow:hidden;}
@keyframes cardSlideUp{from{opacity:0;transform:translateY(24px) scale(0.93);}to{opacity:1;transform:translateY(0) scale(1);}}
.prop-card-flag{font-size:2.2rem;margin-bottom:3px;}
.prop-card-color-band{position:absolute;top:0;left:0;right:0;height:5px;border-radius:18px 18px 0 0;}
.prop-card-city{font-family:'Black Han Sans',sans-serif;font-size:1.18rem;color:var(--text);letter-spacing:2px;}
.prop-card-country{font-size:0.65rem;color:var(--text3);margin-bottom:8px;}
.prop-card-price{font-family:'Fredoka One',cursive;font-size:1.6rem;color:var(--gold);margin:5px 0;}
.prop-card-rent-row{display:flex;justify-content:space-between;font-size:0.62rem;color:var(--text3);padding:2px 0;border-bottom:1px solid var(--border);}
.prop-card-rent-row:last-child{border:none;}
.prop-card-rent-row span:last-child{color:var(--text2);}

/* Chance / Fate card */
.card-box{background:linear-gradient(160deg,var(--bg3),var(--bg2));border:1px solid rgba(255,215,0,0.2);border-radius:18px;
  padding:16px 14px;text-align:center;animation:cardFlip3d 0.55s cubic-bezier(0.34,1.56,0.64,1);}
@keyframes cardFlip3d{0%{opacity:0;transform:rotateY(90deg) scale(0.75);}60%{transform:rotateY(-8deg) scale(1.03);}100%{opacity:1;transform:rotateY(0) scale(1);}}
.card-emoji{font-size:2.6rem;margin-bottom:7px;}
.card-title{font-size:0.87rem;font-weight:700;color:var(--text);margin-bottom:4px;}
.card-effect{font-size:0.82rem;color:var(--text2);}
.card-effect.gain{color:#10d96e;}
.card-effect.lose{color:#ff4560;}

/* Auction */
.auction-box{background:linear-gradient(160deg,#120a28,#0d0820);border:1.5px solid rgba(178,108,247,0.3);border-radius:18px;
  padding:16px;text-align:center;animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);}
.auction-title{font-family:'Black Han Sans',sans-serif;font-size:1.05rem;color:var(--purple);letter-spacing:2px;margin-bottom:4px;}
.auction-current{font-family:'Fredoka One',cursive;font-size:1.5rem;color:var(--gold);margin:8px 0;}
.auction-leader{font-size:0.68rem;color:var(--text3);margin-bottom:8px;}
.bid-input{flex:1;background:var(--bg4);border:1.5px solid var(--border2);border-radius:8px;color:var(--text);padding:8px 12px;font-size:0.85rem;font-family:'Noto Sans KR',sans-serif;outline:none;}
.bid-input:focus{border-color:var(--purple);}

/* Trade */
.trade-box{background:linear-gradient(160deg,#0a1828,#061018);border:1.5px solid rgba(34,211,238,0.25);border-radius:18px;
  padding:15px;animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);}
.trade-title{font-family:'Black Han Sans',sans-serif;font-size:1rem;color:var(--cyan);letter-spacing:2px;margin-bottom:8px;text-align:center;}
.trade-section{font-size:0.65rem;color:var(--text3);text-transform:uppercase;letter-spacing:2px;margin:8px 0 5px;}
.trade-prop-list{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:6px;}
.trade-prop-chip{font-size:0.62rem;padding:3px 8px;border-radius:6px;background:rgba(34,211,238,0.1);border:1px solid rgba(34,211,238,0.2);color:var(--cyan);cursor:pointer;transition:all 0.15s;}
.trade-prop-chip:hover,.trade-prop-chip.selected-trade{background:rgba(34,211,238,0.25);border-color:var(--cyan);}
.trade-money-input{width:100%;background:var(--bg4);border:1.5px solid var(--border2);border-radius:8px;color:var(--text);padding:7px 11px;font-size:0.82rem;font-family:'Noto Sans KR',sans-serif;outline:none;margin-bottom:6px;}
.trade-money-input:focus{border-color:var(--cyan);}
.trade-target-select{width:100%;background:var(--bg4);border:1.5px solid var(--border2);border-radius:8px;color:var(--text);padding:7px 11px;font-size:0.82rem;font-family:'Noto Sans KR',sans-serif;outline:none;margin-bottom:8px;}
.trade-target-select option{background:var(--bg4);color:var(--text);}

/* Casino */
.casino-box{background:linear-gradient(160deg,#180a08,#220e0a);border:1.5px solid rgba(255,165,0,0.3);border-radius:18px;
  padding:16px;text-align:center;animation:cardSlideUp 0.4s cubic-bezier(0.34,1.56,0.64,1);}
.casino-title{font-family:'Black Han Sans',sans-serif;font-size:1.05rem;color:var(--gold);letter-spacing:2px;margin-bottom:4px;}
.casino-slots{font-size:2rem;letter-spacing:8px;margin:8px 0;}
.casino-odds{font-size:0.68rem;color:var(--text3);line-height:1.8;margin-bottom:8px;}
.casino-amount{font-family:'Fredoka One',cursive;font-size:1.3rem;color:var(--gold2);margin-bottom:10px;}

/* Property manager */
.mgr-toggle{background:var(--bg3);border:1.5px solid var(--border2);border-radius:var(--r2);color:var(--text2);font-size:0.74rem;font-family:'Noto Sans KR',sans-serif;padding:8px 12px;cursor:pointer;width:100%;text-align:left;display:flex;align-items:center;gap:6px;transition:all 0.2s;}
.mgr-toggle:hover{background:var(--glass2);}
.mgr-toggle-arrow{margin-left:auto;transition:transform 0.25s;}
.mgr-toggle.open .mgr-toggle-arrow{transform:rotate(180deg);}
.mgr-list{display:none;flex-direction:column;gap:4px;}
.mgr-list.open{display:flex;}
.prop-row{display:flex;align-items:center;gap:7px;padding:5px 3px;border-radius:7px;transition:background 0.15s;}
.prop-row:hover{background:var(--glass);}
.prop-color{width:8px;height:8px;border-radius:2px;flex-shrink:0;}
.prop-name{flex:1;font-size:0.68rem;color:var(--text2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.prop-name.mortgaged{color:var(--text3);text-decoration:line-through;}
.prop-btns{display:flex;gap:3px;}
.mini-b{font-size:0.58rem;border:none;border-radius:4px;padding:2px 7px;cursor:pointer;font-family:'Noto Sans KR',sans-serif;transition:all 0.15s;}
.mini-b-build{background:rgba(16,217,110,0.12);color:#10d96e;border:1px solid rgba(16,217,110,0.25);}
.mini-b-mort{background:rgba(255,140,66,0.12);color:#ff8c42;border:1px solid rgba(255,140,66,0.2);}
.mini-b-unmort{background:rgba(77,171,247,0.12);color:#4dabf7;border:1px solid rgba(77,171,247,0.2);}
.mini-b:disabled{opacity:0.3;cursor:not-allowed;}

/* Log */
.log-wrap{border-top:1px solid var(--border);padding:8px 13px 10px;flex-shrink:0;max-height:170px;display:flex;flex-direction:column;overflow:hidden;}
.log-inner{flex:1;overflow-y:auto;scrollbar-width:none;}
.log-inner::-webkit-scrollbar{display:none;}
.log-row{padding:2px 0;font-size:0.66rem;color:var(--text3);border-bottom:1px solid rgba(255,255,255,0.025);line-height:1.55;}
.log-row.gain{color:#10d96e;}
.log-row.lose{color:#ff4560;}
.log-row.move{color:#4dabf7;}
.log-row.important{color:var(--gold);font-weight:700;}
.log-row.trade{color:var(--cyan);}
.log-row.auction{color:var(--purple);}

/* Butler */
#butler{position:absolute;bottom:16px;left:16px;background:linear-gradient(160deg,var(--bg2),var(--bg3));
  border:1px solid var(--border2);border-radius:14px;padding:10px 14px;font-size:0.76rem;color:var(--text);
  max-width:210px;display:none;z-index:20;box-shadow:var(--shadow2);animation:butlerPop 0.35s cubic-bezier(0.34,1.56,0.64,1);}
.butler-char{margin-right:6px;}
@keyframes butlerPop{from{opacity:0;transform:translateY(12px) scale(0.88);}to{opacity:1;transform:translateY(0) scale(1);}}
#butler::after{content:'';position:absolute;bottom:-9px;left:20px;width:0;height:0;border-left:9px solid transparent;border-right:9px solid transparent;border-top:9px solid var(--border2);}

/* Float text */
.float-text{position:fixed;font-family:'Fredoka One',cursive;font-size:1.3rem;font-weight:700;pointer-events:none;z-index:9999;white-space:nowrap;animation:floatUp 1.3s ease-out forwards;text-shadow:0 2px 12px rgba(0,0,0,0.8);}
@keyframes floatUp{0%{opacity:1;transform:translateY(0) scale(1);}30%{opacity:1;transform:translateY(-24px) scale(1.25);}100%{opacity:0;transform:translateY(-70px) scale(0.75);}}
.coin{position:fixed;pointer-events:none;z-index:9998;font-size:1.3rem;animation:coinFly var(--dur,0.9s) cubic-bezier(0.25,0.46,0.45,0.94) forwards;}
@keyframes coinFly{0%{opacity:1;transform:translate(0,0) scale(1) rotate(0);}50%{opacity:1;transform:translate(var(--mx,20px),var(--my,-35px)) scale(1.4) rotate(180deg);}100%{opacity:0;transform:translate(var(--ex,40px),var(--ey,-55px)) scale(0.4) rotate(400deg);}}

/* Toast */
#toast-container{position:fixed;top:18px;left:50%;transform:translateX(-50%);z-index:9997;display:flex;flex-direction:column;gap:8px;pointer-events:none;align-items:center;}
.toast{background:linear-gradient(160deg,var(--bg2),var(--bg3));border:1px solid var(--border2);border-radius:26px;
  padding:10px 24px;font-size:0.82rem;font-weight:600;color:var(--text);box-shadow:var(--shadow);
  animation:toastIn 0.38s cubic-bezier(0.34,1.56,0.64,1),toastOut 0.35s ease 2.2s forwards;
  white-space:nowrap;display:flex;align-items:center;gap:8px;}
.toast.toast-gain{border-color:rgba(16,217,110,0.4);}
.toast.toast-lose{border-color:rgba(255,69,96,0.4);}
.toast.toast-special{border-color:rgba(255,215,0,0.4);}
.toast.toast-trade{border-color:rgba(34,211,238,0.4);}
.toast.toast-auction{border-color:rgba(178,108,247,0.4);}
@keyframes toastIn{from{opacity:0;transform:translateY(-14px) scale(0.88);}to{opacity:1;transform:translateY(0) scale(1);}}
@keyframes toastOut{from{opacity:1;}to{opacity:0;transform:translateY(-10px);}}

/* Tooltip */
.cell-tooltip{position:fixed;background:linear-gradient(160deg,var(--bg2),var(--bg3));border:1px solid var(--border2);border-radius:14px;
  padding:13px 15px;font-size:0.7rem;z-index:50;pointer-events:none;box-shadow:var(--shadow);min-width:170px;display:none;}
.tooltip-title{font-weight:700;color:var(--text);margin-bottom:5px;font-size:0.78rem;display:flex;align-items:center;gap:6px;}
.tooltip-band{display:inline-block;width:10px;height:10px;border-radius:2px;}
.tooltip-row{display:flex;justify-content:space-between;gap:18px;color:var(--text3);padding:2.5px 0;border-bottom:1px solid var(--border);}
.tooltip-row:last-child{border:none;}
.tooltip-row span:last-child{color:var(--text2);}

/* Game over */
#gameover{position:fixed;inset:0;background:rgba(3,5,12,0.96);backdrop-filter:blur(16px);display:none;flex-direction:column;align-items:center;justify-content:center;z-index:100;}
.fireworks-bg{position:absolute;inset:0;pointer-events:none;overflow:hidden;}
.gameover-winner{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,5vw,3.2rem);
  background:linear-gradient(135deg,#ffd700,#ff8c00,#ff4d6d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:winnerPop 0.7s cubic-bezier(0.34,1.56,0.64,1);text-align:center;margin-bottom:4px;}
@keyframes winnerPop{from{opacity:0;transform:scale(0.2) rotate(-15deg);}60%{transform:scale(1.12) rotate(3deg);}to{opacity:1;transform:scale(1) rotate(0);}}
.gameover-sub{color:var(--text3);font-size:0.78rem;letter-spacing:4px;margin-bottom:8px;text-transform:uppercase;}
.gameover-avatar{font-size:4.5rem;margin-bottom:8px;animation:charFloat 2.5s ease-in-out infinite;}
.rank-card{background:linear-gradient(160deg,var(--bg2),var(--bg3));border:1px solid var(--border2);border-radius:20px;
  padding:20px 28px;width:100%;max-width:380px;margin-bottom:24px;box-shadow:var(--shadow);}
.rank-row{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);font-size:0.85rem;}
.rank-row:last-child{border:none;}
.rank-medal{font-size:1.4rem;min-width:28px;}
.rank-avatar{font-size:1.25rem;}
.rank-player{flex:1;font-weight:700;}
.rank-money{color:var(--green);font-weight:700;font-family:'Fredoka One',cursive;}
.btn-restart{background:linear-gradient(135deg,#ffd700,#ff8c00);border:none;border-radius:16px;
  color:#fff;font-family:'Black Han Sans',sans-serif;font-size:1.1rem;letter-spacing:3px;
  padding:15px 52px;cursor:pointer;box-shadow:0 8px 32px rgba(255,140,0,0.5);transition:all 0.2s;}
.btn-restart:hover{transform:translateY(-3px);}

/* Confetti & effects */
.confetti-piece{position:fixed;pointer-events:none;z-index:9999;animation:confettiFall linear forwards;}
@keyframes confettiFall{0%{transform:translateY(-20px) rotate(0) scale(1);opacity:1;}100%{transform:translateY(110vh) rotate(800deg) scale(0.4);opacity:0;}}
.double-ring{position:fixed;border-radius:50%;border:3px solid var(--gold);animation:doubleRing 0.9s ease-out forwards;pointer-events:none;z-index:9996;}
@keyframes doubleRing{from{transform:translate(-50%,-50%) scale(0.4);opacity:1;}to{transform:translate(-50%,-50%) scale(3);opacity:0;}}
.ability-flash{position:fixed;inset:0;pointer-events:none;z-index:9990;animation:abilityFlash 0.6s ease-out forwards;}
@keyframes abilityFlash{0%{opacity:0.4;}100%{opacity:0;}}
.move-trail{position:fixed;border-radius:50%;pointer-events:none;animation:trailFade 0.45s ease-out forwards;z-index:9;}
@keyframes trailFade{from{opacity:0.8;transform:scale(1);}to{opacity:0;transform:scale(2.2);}}
.sparkle{position:fixed;pointer-events:none;z-index:9998;animation:sparkleFly var(--dur,0.7s) ease-out forwards;}
@keyframes sparkleFly{0%{opacity:1;transform:translate(0,0) scale(1);}100%{opacity:0;transform:translate(var(--dx,0),var(--dy,-40px)) scale(0);}}
.screen-flash{position:fixed;inset:0;pointer-events:none;z-index:9989;animation:screenFlash 0.35s ease-out forwards;}
@keyframes screenFlash{0%{opacity:var(--intensity,0.15);}100%{opacity:0;}}

/* 이동 경로 하이라이트 */
.cell.path-highlight{filter:brightness(1.6) !important;z-index:6 !important;}

/* 도착 셀 강조 */
.cell.landing-cell{animation:landingGlow 0.6s ease-out !important;z-index:7 !important;}
@keyframes landingGlow{0%{filter:brightness(2.5) saturate(2);}100%{filter:brightness(1);}}
</style>
</head>
<body>
<div class="bg-mesh"></div>
<div class="star-field" id="star-field"></div>
<div id="toast-container"></div>

<!-- CHARACTER SELECT -->
<div id="char-select">
  <div class="char-header">
    <div class="char-title-main">🌍 인베스트마블</div>
    <div class="char-title-sub">WORLD MARBLE · REMASTERED</div>
  </div>
  <div class="char-prompt">캐릭터를 선택하세요</div>
  <div class="char-grid" id="char-grid"></div>
  <button class="char-next-btn" id="char-next-btn" onclick="goToSetup()">다음 →</button>
</div>

<!-- SETUP -->
<div id="setup">
  <div class="setup-card">
    <div class="setup-logo">🌍 인베스트마블</div>
    <div class="setup-sub">WORLD MARBLE · REMASTERED</div>
    <div class="setup-char-preview" id="setup-preview">
      <div class="setup-char-avatar" id="preview-avatar"></div>
      <div>
        <div class="setup-char-name" id="preview-name"></div>
        <div style="font-size:0.72rem;color:var(--text3);margin-top:2px" id="preview-desc"></div>
        <div class="setup-char-ability-tag" id="preview-ability"></div>
      </div>
    </div>
    <div class="form-row">
      <label class="form-label">내 닉네임</label>
      <input class="form-input" id="inp-name" value="여행자" maxlength="8">
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
        <option value="easy">🟢 쉬움</option>
        <option value="normal" selected>🟡 보통</option>
        <option value="hard">🔴 어려움</option>
      </select>
    </div>
    <button class="btn-start" onclick="startGame()">🎲 게임 시작!</button>
    <button class="btn-back-setup" onclick="goBackToChar()">← 캐릭터 변경</button>
    <div class="rules-mini">
      시작자금 <b>₩10,000</b> · 출발 통과 <b>+₩300</b> · 출발 착지 <b>+₩500</b><br>
      독점 시 임료 2배 · 집(최대 4채) → 호텔 · 더블 시 한번 더!<br>
      블랙홀: 더블 탈출 또는 보석금 <b>₩600</b><br>
      🔨 <b>경매</b>: 패스 시 자동 경매 · 🤝 <b>협상</b>: 부동산 교환
    </div>
  </div>
</div>

<!-- GAME -->
<div id="game">
  <div class="board-wrap">
    <div id="board"></div>
    <div id="butler"><span class="butler-char" id="butler-char"></span><span id="butler-text"></span></div>
  </div>
  <div class="side">
    <div class="side-players">
      <div class="sec-label">🌍 여행자 현황</div>
      <div id="players-list"></div>
    </div>
    <div class="action-zone" id="action-zone"></div>
    <div class="log-wrap">
      <div class="sec-label" style="padding:6px 0 5px;flex-shrink:0">📋 게임 로그</div>
      <div class="log-inner" id="log-area"></div>
    </div>
  </div>
</div>

<!-- GAME OVER -->
<div id="gameover">
  <div class="fireworks-bg" id="fireworks-bg"></div>
  <div class="gameover-avatar" id="winner-avatar"></div>
  <div class="gameover-winner" id="winner-name"></div>
  <div class="gameover-sub">세계 정복 완료!</div>
  <div class="rank-card"><div id="rank-list"></div></div>
  <button class="btn-restart" onclick="resetToChar()">🔄 다시 하기</button>
</div>

<!-- Tooltip -->
<div class="cell-tooltip" id="tooltip">
  <div class="tooltip-title" id="tt-title"></div>
  <div id="tt-body"></div>
</div>

<script>
// ═══════════════════════════════════════════════════════════
//  DATA
// ═══════════════════════════════════════════════════════════
const CHARACTERS = [
  {id:0,name:'영웅이',emoji:'🦸',color:'#4dabf7',desc:'안정적인 투자 전략가',ability:'첫 매입 15% 할인',abilityKey:'discount',butler:'신중한 투자가 최고입니다!',rgb:'77,171,247',rarity:'RARE'},
  {id:1,name:'마법사',emoji:'🧙',color:'#b26cf7',desc:'카드 운이 좋은 마법사',ability:'불리한 카드 1회 무효',abilityKey:'card_immune',butler:'마법으로 운명을 바꾸겠습니다!',rgb:'178,108,247',rarity:'EPIC'},
  {id:2,name:'공주님',emoji:'👸',color:'#f472b6',desc:'럭셔리 자산 전문가',ability:'임료 수입 12% 추가',abilityKey:'rent_bonus',butler:'품위 있게, 그리고 부유하게!',rgb:'244,114,182',rarity:'EPIC'},
  {id:3,name:'로봇',emoji:'🤖',color:'#94a3b8',desc:'완벽하게 계산된 전략',ability:'세금 1회 면제',abilityKey:'tax_immune',butler:'확률 계산 완료. 최적 루트 선택.',rgb:'148,163,184',rarity:'RARE'},
  {id:4,name:'여우',emoji:'🦊',color:'#ff8c42',desc:'빠르고 영리한 상인',ability:'이동 +2칸 1회 사용',abilityKey:'speed_boost',butler:'빠르게 움직여야 기회를 잡죠!',rgb:'255,140,66',rarity:'RARE'},
  {id:5,name:'용사',emoji:'⚔️',color:'#10d96e',desc:'적극적인 개척자',ability:'상대 임료 60% 감면 1회',abilityKey:'rent_cut',butler:'두려움 없이 전진이다!',rgb:'16,217,110',rarity:'LEGENDARY'},
];

const CELLS = [
  {name:'출발',type:'go',price:0,rent:0,group:-1,color:'',flag:'🚩',country:''},
  {name:'서울',type:'prop',price:600,rent:60,group:0,color:'#ef4444',flag:'🇰🇷',country:'한국'},
  {name:'찬스',type:'chance',price:0,rent:0,group:-1,color:'',flag:'❓',country:''},
  {name:'도쿄',type:'prop',price:600,rent:60,group:0,color:'#ef4444',flag:'🇯🇵',country:'일본'},
  {name:'소득세',type:'tax',price:200,rent:0,group:-1,color:'',flag:'💸',country:''},
  {name:'✈️ 인천',type:'airport',price:400,rent:100,group:-1,color:'',flag:'✈️',country:'공항'},
  {name:'방콕',type:'prop',price:800,rent:80,group:1,color:'#a855f7',flag:'🇹🇭',country:'태국'},
  {name:'운명',type:'fate',price:0,rent:0,group:-1,color:'',flag:'⭐',country:''},
  {name:'싱가포르',type:'prop',price:900,rent:90,group:1,color:'#a855f7',flag:'🇸🇬',country:'싱가포르'},
  {name:'상하이',type:'prop',price:1000,rent:100,group:1,color:'#a855f7',flag:'🇨🇳',country:'중국'},
  {name:'여행',type:'visit',price:0,rent:0,group:-1,color:'',flag:'✈️',country:''},
  {name:'두바이',type:'prop',price:1000,rent:100,group:2,color:'#f97316',flag:'🇦🇪',country:'UAE'},
  {name:'⚡ 전기',type:'util',price:300,rent:0,group:-1,color:'',flag:'⚡',country:'공용'},
  {name:'카이로',type:'prop',price:1100,rent:110,group:2,color:'#f97316',flag:'🇪🇬',country:'이집트'},
  {name:'뭄바이',type:'prop',price:1200,rent:120,group:2,color:'#f97316',flag:'🇮🇳',country:'인도'},
  {name:'✈️ 파리',type:'airport',price:400,rent:100,group:-1,color:'',flag:'✈️',country:'공항'},
  {name:'파리',type:'prop',price:1400,rent:140,group:3,color:'#ec4899',flag:'🇫🇷',country:'프랑스'},
  {name:'찬스',type:'chance',price:0,rent:0,group:-1,color:'',flag:'❓',country:''},
  {name:'베를린',type:'prop',price:1500,rent:150,group:3,color:'#ec4899',flag:'🇩🇪',country:'독일'},
  {name:'런던',type:'prop',price:1600,rent:160,group:3,color:'#ec4899',flag:'🇬🇧',country:'영국'},
  {name:'블랙홀',type:'jail',price:0,rent:0,group:-1,color:'',flag:'⚫',country:''},
  {name:'로마',type:'prop',price:1600,rent:160,group:4,color:'#22c55e',flag:'🇮🇹',country:'이탈리아'},
  {name:'운명',type:'fate',price:0,rent:0,group:-1,color:'',flag:'⭐',country:''},
  {name:'마드리드',type:'prop',price:1700,rent:170,group:4,color:'#22c55e',flag:'🇪🇸',country:'스페인'},
  {name:'바르셀로나',type:'prop',price:1800,rent:180,group:4,color:'#22c55e',flag:'🇪🇸',country:'스페인'},
  {name:'✈️ JFK',type:'airport',price:400,rent:100,group:-1,color:'',flag:'✈️',country:'공항'},
  {name:'뉴욕',type:'prop',price:2000,rent:200,group:5,color:'#3b82f6',flag:'🇺🇸',country:'미국'},
  {name:'찬스',type:'chance',price:0,rent:0,group:-1,color:'',flag:'❓',country:''},
  {name:'시카고',type:'prop',price:2100,rent:210,group:5,color:'#3b82f6',flag:'🇺🇸',country:'미국'},
  {name:'LA',type:'prop',price:2200,rent:220,group:5,color:'#3b82f6',flag:'🇺🇸',country:'미국'},
  {name:'무료주차',type:'free',price:0,rent:0,group:-1,color:'',flag:'🅿️',country:''},
  {name:'라스베가스',type:'casino',price:0,rent:0,group:-1,color:'',flag:'🎰',country:'미국'},
  {name:'운명',type:'fate',price:0,rent:0,group:-1,color:'',flag:'⭐',country:''},
  {name:'토론토',type:'prop',price:2200,rent:220,group:6,color:'#fbbf24',flag:'🇨🇦',country:'캐나다'},
  {name:'상파울루',type:'prop',price:2400,rent:240,group:6,color:'#fbbf24',flag:'🇧🇷',country:'브라질'},
  {name:'✈️ SYD',type:'airport',price:400,rent:100,group:-1,color:'',flag:'✈️',country:'공항'},
  {name:'시드니',type:'prop',price:2600,rent:260,group:7,color:'#06b6d4',flag:'🇦🇺',country:'호주'},
  {name:'🔥 오일',type:'util',price:300,rent:0,group:-1,color:'',flag:'🔥',country:'공용'},
  {name:'멜버른',type:'prop',price:2800,rent:280,group:7,color:'#06b6d4',flag:'🇦🇺',country:'호주'},
  {name:'사치세',type:'tax',price:400,rent:0,group:-1,color:'',flag:'💎',country:''},
];

const GRP_SIZE={0:2,1:3,2:3,3:3,4:3,5:3,6:2,7:2};
const BUILD_COST={0:200,1:250,2:300,3:350,4:400,5:450,6:500,7:600};
const RENT_MULT=[1,5,15,45,80];
const PCOLORS=['#4dabf7','#f472b6','#10d96e','#ff8c42'];
const BOT_NAMES=['알파','베타','감마'];
const JAIL_BAIL=600;
const START_MONEY=10000;
const PASS_GO=300;
const GO_LAND=500;

// 주사위 도트 패턴
const DICE_DOTS = [
  null, // 0
  '<div class="die-dots dots-1"><div class="dot"></div></div>',
  '<div class="die-dots dots-2"><div class="dot"></div><div class="dot"></div></div>',
  '<div class="die-dots dots-3"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
  '<div class="die-dots dots-4"><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
  '<div class="die-dots dots-5"><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
  '<div class="die-dots dots-6"><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>',
];

const CHANCE_CARDS=[
  {emoji:'💰',text:'은행 배당금 지급!',type:'money',amount:200},
  {emoji:'📋',text:'세금 환급!',type:'money',amount:250},
  {emoji:'🎂',text:'생일! 모두에게 받기',type:'birthday',amount:100},
  {emoji:'🔧',text:'수리비 청구서',type:'money',amount:-180},
  {emoji:'🏥',text:'의료비 지출',type:'money',amount:-250},
  {emoji:'📚',text:'학교 수업료 납부',type:'money',amount:-300},
  {emoji:'📈',text:'주식 투자 대박!',type:'money',amount:400},
  {emoji:'🚩',text:'출발로 GO! +₩300',type:'goto',target:0},
  {emoji:'⚫',text:'블랙홀로 빠져든다!',type:'goto_jail'},
  {emoji:'⬅️',text:'뒤로 3칸 이동',type:'move',amount:-3},
  {emoji:'➡️',text:'앞으로 5칸 이동',type:'move',amount:5},
  {emoji:'✈️',text:'가장 가까운 공항으로!',type:'nearest_airport'},
  {emoji:'🔨',text:'건물 수리비: 집×50 호텔×150',type:'repair'},
  {emoji:'🏦',text:'은행 전산 오류! 지급',type:'money',amount:700},
  {emoji:'🌧️',text:'보험료 납부',type:'money',amount:-150},
  {emoji:'🎶',text:'콘서트 수익!',type:'money',amount:350},
];
const FATE_CARDS=[
  {emoji:'🎫',text:'복권 당첨! 대박!',type:'money',amount:500},
  {emoji:'🚦',text:'교통 과태료',type:'money',amount:-100},
  {emoji:'💊',text:'보험금 수령',type:'money',amount:200},
  {emoji:'🚗',text:'자동차 수리비',type:'money',amount:-200},
  {emoji:'🎵',text:'콘서트 대성공!',type:'money',amount:300},
  {emoji:'✈️',text:'여행 경비 지출',type:'money',amount:-180},
  {emoji:'🚩',text:'출발로 GO! +₩300',type:'goto',target:0},
  {emoji:'⚫',text:'블랙홀로 순간이동!',type:'goto_jail'},
  {emoji:'➡️',text:'앞으로 4칸!',type:'move',amount:4},
  {emoji:'🎂',text:'생일! 모두에게 받기',type:'birthday',amount:100},
  {emoji:'💸',text:'탈세 적발! 벌금',type:'money',amount:-350},
  {emoji:'🏦',text:'은행 이자 지급',type:'money',amount:400},
  {emoji:'🌈',text:'행운! 다음 임료 면제',type:'special',special:'rent_free'},
  {emoji:'🎁',text:'깜짝 선물! 모두 지급',type:'birthday',amount:80},
  {emoji:'🏅',text:'사업 성공 보너스',type:'money',amount:600},
  {emoji:'🤝',text:'협상 보너스! 현금 지급',type:'money',amount:320},
];

const BUTLER_MSGS={
  buy:['훌륭한 선택!','좋은 투자예요!'],
  pass:['다음 기회에...','신중하시군요.'],
  rent_in:['임료 수입!','부동산이 돈을 법니다!'],
  rent_out:['아이고, 임료를...'],
  jail:['블랙홀로!','잠시 구금됐군요.'],
  double:['더블! 한번 더!','행운이 따르네요!'],
  triple:['3연속 더블! 블랙홀!'],
  build:['건설 완료!','임료가 올랐습니다!'],
  bankrupt:['파산하셨습니다...'],
  win:['세계 정복 완료!'],
  go_pass:['출발 통과! +₩300!'],
  go_land:['출발 착지! +₩500!'],
  casino:['🎰 라스베가스!'],
  auction_win:['경매 낙찰! 축하드립니다!'],
  trade_ok:['거래 성사! 🤝'],
  trade_no:['거래 거절...'],
};

// ═══════════════════════════════════════════════════════════
//  STATE
// ═══════════════════════════════════════════════════════════
let G=null;
let selectedChar=null;
let mgrOpen=false;
let butlerTmr=null;
let animating=false;
let boardSize=560;
let floatSide=0;

// ═══════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════
function initStars(){
  const sf=document.getElementById('star-field');
  for(let i=0;i<90;i++){
    const s=document.createElement('div');s.className='star';
    const sz=1+Math.random()*2.5;
    s.style.cssText=`left:${Math.random()*100}%;top:${Math.random()*100}%;width:${sz}px;height:${sz}px;--dur:${1.5+Math.random()*3.5}s;--op:${0.3+Math.random()*0.7};animation-delay:${Math.random()*4}s;`;
    sf.appendChild(s);
  }
}

function renderCharGrid(){
  const grid=document.getElementById('char-grid');
  grid.innerHTML=CHARACTERS.map(c=>`
    <div class="char-card" id="char-card-${c.id}" style="--char-color:${c.color};--char-rgb:${c.rgb}" onclick="selectChar(${c.id})">
      <div class="char-rarity" style="border-color:${c.color};color:${c.color}">${c.rarity}</div>
      <div class="selected-check">✓</div>
      <div class="char-avatar">${c.emoji}</div>
      <div class="char-name" style="color:${c.color}">${c.name}</div>
      <div class="char-desc">${c.desc}</div>
      <div class="char-ability-tag">✨ ${c.ability}</div>
    </div>`).join('');
}

function selectChar(id){
  selectedChar=CHARACTERS[id];
  document.querySelectorAll('.char-card').forEach(el=>el.classList.remove('selected'));
  document.getElementById('char-card-'+id).classList.add('selected');
  document.getElementById('char-next-btn').classList.add('active');
  playSound('click');
  spawnSparkles(window.innerWidth/2,window.innerHeight/2,selectedChar.color,8);
}

function goToSetup(){
  if(!selectedChar)return;
  document.getElementById('char-select').style.display='none';
  document.getElementById('setup').style.display='flex';
  document.getElementById('preview-avatar').textContent=selectedChar.emoji;
  document.getElementById('preview-name').textContent=selectedChar.name;
  document.getElementById('preview-name').style.color=selectedChar.color;
  document.getElementById('preview-desc').textContent=selectedChar.desc;
  document.getElementById('preview-ability').textContent='✨ '+selectedChar.ability;
}
function goBackToChar(){document.getElementById('setup').style.display='none';document.getElementById('char-select').style.display='flex';}

// ═══════════════════════════════════════════════════════════
//  GAME INIT
// ═══════════════════════════════════════════════════════════
function newCells(){return CELLS.map(c=>({...c,owner:null,houses:0,mortgaged:false}));}

function pickBotChar(exclude){
  const avail=CHARACTERS.filter(c=>!exclude.has(c.id));
  return avail[Math.floor(Math.random()*avail.length)];
}

function initGame(playerName,botCount,diff){
  const char0=selectedChar||CHARACTERS[0];
  const usedIds=new Set([char0.id]);
  const players=[{name:playerName,money:START_MONEY,pos:0,color:char0.color,char:char0,is_bot:false,bankrupt:false,jail_turns:0,ability_used:false,rent_free:false,consecutive_doubles:0}];
  for(let i=0;i<botCount;i++){
    const bc=pickBotChar(usedIds);usedIds.add(bc.id);
    players.push({name:BOT_NAMES[i],money:START_MONEY,pos:0,color:PCOLORS[i+1]||PCOLORS[0],char:bc,is_bot:true,bankrupt:false,jail_turns:0,ability_used:false,rent_free:false,consecutive_doubles:0});
  }
  return{players,cells:newCells(),turn:0,doubles:0,phase:'roll',log:[],diff,pending_card:null,winner:null,d1:1,d2:1,auction:null,trade:null};
}

// ═══════════════════════════════════════════════════════════
//  BUTLER
// ═══════════════════════════════════════════════════════════
function butler(key,custom){
  if(!G)return;
  const msgs=BUTLER_MSGS[key]||['...'];
  const msg=custom||msgs[Math.floor(Math.random()*msgs.length)];
  const el=document.getElementById('butler');
  document.getElementById('butler-text').textContent=msg;
  document.getElementById('butler-char').textContent=G.players[G.turn].char.emoji;
  el.style.display='block';
  if(butlerTmr)clearTimeout(butlerTmr);
  butlerTmr=setTimeout(()=>el.style.display='none',3800);
}

// ═══════════════════════════════════════════════════════════
//  GAME LOGIC
// ═══════════════════════════════════════════════════════════
function log(msg,style=''){G.log.unshift({msg,style});if(G.log.length>150)G.log.length=150;}
function alive(){return G.players.filter(p=>!p.bankrupt);}

function checkWin(){
  const a=alive();
  if(a.length===1){G.winner=a[0].name;G.winnerIdx=G.players.indexOf(a[0]);G.phase='gameover';return true;}
  return false;
}

function ownsGroup(pidx,grp){
  if(grp<0)return false;
  return G.cells.filter(c=>c.group===grp&&c.owner===pidx).length===(GRP_SIZE[grp]||0);
}

function getNetWorth(pidx){
  const p=G.players[pidx];let nw=p.money;
  G.cells.forEach((c,ci)=>{if(c.owner!==pidx)return;nw+=c.mortgaged?Math.floor(c.price*0.5):c.price;nw+=(c.houses||0)*(BUILD_COST[c.group]||300);});
  return nw;
}

function calcRent(ci,roll){
  const c=G.cells[ci];if(!c||c.owner===null||c.mortgaged)return 0;
  const{type,owner,houses,rent,group}=c;
  if(type==='prop'){const h=Math.min(houses||0,4);if(h===0&&ownsGroup(owner,group))return rent*2;return rent*RENT_MULT[h];}
  if(type==='airport'){const n=G.cells.filter(c2=>c2.type==='airport'&&c2.owner===owner).length;return 100*(n*n);}
  if(type==='util'){const n=G.cells.filter(c2=>c2.type==='util'&&c2.owner===owner).length;const r=roll||(Math.floor(Math.random()*11)+2);return r*(n===1?4:12);}
  return 0;
}

function nearestAirport(pos){
  const airports=[5,15,25,35];
  return airports.reduce((b,r)=>((r-pos+40)%40)<((b-pos+40)%40)?r:b);
}

function movePlayer(pidx,steps){
  const p=G.players[pidx],old=p.pos;
  const nw=((old+steps)%40+40)%40;
  if(steps>0&&nw<=old&&nw!==old){
    p.money+=PASS_GO;log(`🚩 ${p.name} 출발 통과! +₩${PASS_GO}`,'gain');
    if(!p.is_bot)butler('go_pass');toast(`+₩${PASS_GO} 출발 통과!`,'gain');
  }
  p.pos=nw;
}

function sendToJail(pidx){
  const p=G.players[pidx];p.pos=20;p.jail_turns=3;
  log(`⚫ ${p.name} 블랙홀!`,'lose');butler('jail');toast('⚫ 블랙홀!','lose');
  spawnScreenFlash('rgba(168,85,247,0.15)');
}

function payRent(fromIdx,toIdx,amt){
  const payer=G.players[fromIdx],recv=G.players[toIdx];
  if(payer.rent_free){payer.rent_free=false;log(`🌈 ${payer.name} 행운! 임료 면제!`,'gain');toast('🌈 임료 면제!','gain');return;}
  let actual=amt;
  if(payer.char.abilityKey==='rent_cut'&&!payer.ability_used){actual=Math.floor(amt*0.4);payer.ability_used=true;log(`⚔️ ${payer.name} 임료 60% 감면!`,'gain');toast('⚔️ 임료 60% 감면!','gain');spawnAbilityFlash(payer.color);}
  let recvAmt=actual;
  if(recv.char.abilityKey==='rent_bonus')recvAmt=Math.floor(actual*1.12);
  const pay=Math.min(actual,Math.max(0,payer.money));
  payer.money-=pay;recv.money+=Math.min(recvAmt,pay);
  log(`💸 ${payer.name}→${recv.name}: ₩${pay}`,'lose');
  if(fromIdx===0)butler('rent_out');else if(toIdx===0)butler('rent_in');
  spawnFloatText(`-₩${pay}`,payer.color,true);spawnFloatText(`+₩${Math.min(recvAmt,pay)}`,recv.color,false);
  checkBankrupt(fromIdx);
}

function checkBankrupt(pidx){
  const p=G.players[pidx];if(p.money>=0)return;
  for(let ci=0;ci<G.cells.length;ci++){const c=G.cells[ci];if(c.owner===pidx&&!c.mortgaged&&(c.houses||0)===0&&p.money<0){const val=Math.floor(c.price*0.5);c.mortgaged=true;p.money+=val;log(`📋 ${p.name} ${c.name} 긴급저당 +₩${val}`,'lose');}}
  if(p.money<0){p.bankrupt=true;p.money=0;G.cells.forEach(c=>{if(c.owner===pidx){c.owner=null;c.houses=0;c.mortgaged=false;}});log(`💀 ${p.name} 파산!`,'important');butler('bankrupt');toast(`💀 ${p.name} 파산!`,'lose');spawnScreenFlash('rgba(255,69,96,0.2)');checkWin();}
}

function doMortgage(pidx,ci){const c=G.cells[ci],p=G.players[pidx];if(c.owner!==pidx||c.mortgaged||(c.houses||0)>0)return;const val=Math.floor(c.price*0.5);c.mortgaged=true;p.money+=val;log(`📋 ${p.name} ${c.name} 저당 +₩${val}`,'lose');renderAll();}
function doUnmortgage(pidx,ci){const c=G.cells[ci],p=G.players[pidx];if(c.owner!==pidx||!c.mortgaged)return;const cost=Math.floor(c.price*0.6);if(p.money<cost)return;c.mortgaged=false;p.money-=cost;log(`✅ ${p.name} ${c.name} 저당해제 -₩${cost}`);renderAll();}
function doBuild(pidx,ci){
  const c=G.cells[ci],p=G.players[pidx];const cost=BUILD_COST[c.group]||300;
  if(p.money<cost||(c.houses||0)>=4||c.mortgaged)return;
  c.houses=(c.houses||0)+1;p.money-=cost;
  const lbl=c.houses===4?'호텔🏨':`집 ${c.houses}채🏠`;
  log(`🔨 ${p.name} ${c.name} ${lbl} -₩${cost}`);butler('build');toast(`🏠 ${c.name} ${lbl}!`,'gain');
  spawnSparkles(window.innerWidth*0.6,window.innerHeight*0.5,'#10d96e',10);renderAll();
}

function useAbility(){
  if(!G||animating)return;
  const pidx=G.turn,p=G.players[pidx];if(p.is_bot||p.ability_used||p.bankrupt)return;
  const key=p.char.abilityKey;p.ability_used=true;
  spawnAbilityFlash(p.char.color);
  if(key==='discount'){p._discount_pending=true;log(`✨ ${p.name} 능력: 다음 매입 15% 할인!`,'important');toast('✨ 할인 능력 사용!','special');}
  else if(key==='speed_boost'){p._speed_boost=true;log(`✨ ${p.name} 능력: +2칸!`,'important');toast('✨ 이동 +2칸!','special');}
  else if(key==='card_immune'){p._card_immune=true;log(`✨ ${p.name} 능력: 다음 카드 무효!`,'important');toast('✨ 카드 무효 준비!','special');}
  else if(key==='tax_immune'){p._tax_immune=true;log(`✨ ${p.name} 능력: 세금 면제!`,'important');toast('✨ 세금 면제 준비!','special');}
  renderAll();
}

function applyCard(pidx,card){
  const p=G.players[pidx];
  if(p._card_immune&&(card.type==='money'&&card.amount<0||card.type==='goto_jail'||card.type==='repair')){
    p._card_immune=false;log(`🧙 ${p.name} 카드 마법 무효화!`,'gain');toast('🧙 카드 무효화!','gain');if(G.phase!=='gameover')G.phase='roll';return;
  }
  const{type,amount,target}=card;
  if(type==='money'){if(amount<0&&p._tax_immune){p._tax_immune=false;log(`🤖 ${p.name} 세금 면제!`,'gain');}else{p.money+=amount;log(`🃏 ${p.name}: ${card.text} (${amount>0?'+':''}${amount})`,amount>0?'gain':'lose');spawnFloatText(`${amount>0?'+':''}₩${Math.abs(amount)}`,p.color,amount<0);if(amount<0)checkBankrupt(pidx);}}
  else if(type==='birthday'){G.players.forEach((o,i)=>{if(i!==pidx&&!o.bankrupt){const a=Math.min(amount,Math.max(0,o.money));o.money-=a;p.money+=a;}});log(`🎂 ${p.name} 생일! 각자 ₩${amount}`,'gain');}
  else if(type==='goto'){if(target===0)p.money+=PASS_GO;p.pos=target;log(`🚀 ${p.name} → ${CELLS[target].name}`,'move');landCell(pidx,0);return;}
  else if(type==='goto_jail'){sendToJail(pidx);}
  else if(type==='move'){movePlayer(pidx,amount);log(`👣 ${p.name} ${amount>0?'+':''}${amount}칸`,'move');landCell(pidx,0);return;}
  else if(type==='nearest_airport'){const nr=nearestAirport(p.pos);const steps=((nr-p.pos+40)%40)||40;movePlayer(pidx,steps);log(`✈️ ${p.name} 공항으로!`,'move');landCell(pidx,0);return;}
  else if(type==='repair'){const h=G.cells.filter(c=>c.owner===pidx&&(c.houses||0)>0&&c.houses<4).length;const ht=G.cells.filter(c=>c.owner===pidx&&c.houses===4).length;const cost=h*50+ht*150;p.money-=cost;log(`🔧 ${p.name} 수리비 -₩${cost}`,'lose');checkBankrupt(pidx);}
  else if(type==='special'&&card.special==='rent_free'){p.rent_free=true;log(`🌈 ${p.name} 다음 임료 면제!`,'gain');}
  if(G.phase!=='gameover')G.phase='roll';
}

// ═══════════════════════════════════════════════════════════
//  LANDING
// ═══════════════════════════════════════════════════════════
function landCell(pidx,roll){
  const p=G.players[pidx],ci=p.pos,c=G.cells[ci];if(!c)return;
  log(`📍 ${p.name} → ${c.flag||''}${c.name}`,'move');
  // 도착 셀 강조
  const cellEl=document.getElementById('cell-'+ci);
  if(cellEl){cellEl.classList.add('landing-cell');setTimeout(()=>cellEl.classList.remove('landing-cell'),700);}
  if(c.type==='go'){p.money+=GO_LAND;log(`🎉 출발 착지! +₩${GO_LAND}`,'gain');if(!p.is_bot)butler('go_land');toast(`+₩${GO_LAND} 출발 착지!`,'gain');spawnCoinsFly(p.color);}
  else if(['prop','airport','util'].includes(c.type)){
    if(c.owner===null){G.phase='buy';return;}
    else if(c.owner===pidx){log(`🏠 자기 소유지`);}
    else{if(c.mortgaged){log(`📋 ${c.name} 저당 중`);}else{const rent=calcRent(ci,roll);payRent(pidx,c.owner,rent);}}
    if(!checkWin()){}
  }
  else if(c.type==='chance'||c.type==='fate'){const pool=c.type==='chance'?CHANCE_CARDS:FATE_CARDS;G.pending_card=pool[Math.floor(Math.random()*pool.length)];G.phase='card';return;}
  else if(c.type==='tax'){if(p._tax_immune){p._tax_immune=false;log(`🤖 ${p.name} 세금 면제!`,'gain');}else{p.money-=c.price;log(`💸 ${p.name} 세금 -₩${c.price}`,'lose');spawnFloatText(`-₩${c.price}`,p.color,true);checkBankrupt(pidx);}}
  else if(c.type==='jail'){sendToJail(pidx);}
  else if(c.type==='casino'){G.phase='casino';return;}
  else{log(`✅ ${c.name}`);}
  if(G.phase!=='gameover')G.phase='roll';
}

function nextTurn(){
  if(G.phase==='gameover')return;
  const n=G.players.length;let nxt=(G.turn+1)%n,att=0;
  while(G.players[nxt].bankrupt&&att<n){nxt=(nxt+1)%n;att++;}
  G.turn=nxt;G.phase='roll';G.doubles=0;
}

// ═══════════════════════════════════════════════════════════
//  AUCTION
// ═══════════════════════════════════════════════════════════
function startAuction(ci){
  const c=G.cells[ci];const livePlayers=alive();
  G.auction={ci,currentBid:Math.floor(c.price*0.5),leaderId:-1,bids:{},participants:[...livePlayers.map(p=>G.players.indexOf(p))],round:0,phase:'bidding'};
  G.phase='auction';
  log(`🔨 ${c.flag}${c.name} 경매 시작! 최저가: ₩${G.auction.currentBid}`,'auction');
  toast(`🔨 경매 시작! ${c.name}`,'auction');renderAll();
  if(G.players[G.turn].is_bot)setTimeout(()=>botAuctionBid(G.turn),700);
}

function playerBid(amount){
  if(!G||!G.auction)return;
  const pidx=G.turn,p=G.players[pidx];const minBid=G.auction.currentBid+50;
  if(amount<minBid){toast(`최소 입찰가: ₩${minBid}`,'lose');return;}
  if(p.money<amount){toast('자금 부족!','lose');return;}
  G.auction.currentBid=amount;G.auction.leaderId=pidx;G.auction.bids[pidx]=amount;
  log(`🔨 ${p.name} 입찰: ₩${amount}`,'auction');toast(`🔨 ₩${amount} 입찰!`,'auction');
  finishPlayerAuctionTurn();
}

function playerPass(){if(!G||!G.auction)return;log(`↩️ ${G.players[G.turn].name} 경매 패스`,'auction');finishPlayerAuctionTurn();}

function finishPlayerAuctionTurn(){
  const auction=G.auction;auction.round++;
  if(auction.round>=auction.participants.length){resolveAuction();}
  else{const nextIdx=auction.participants[auction.round%auction.participants.length];if(nextIdx===G.turn){resolveAuction();return;}if(G.players[nextIdx].is_bot){setTimeout(()=>botAuctionBid(nextIdx),700);}else{renderAll();}}
}

function botAuctionBid(botIdx){
  if(!G||!G.auction)return;
  const bot=G.players[botIdx];const auction=G.auction;const cell=G.cells[auction.ci];
  const diff=G.diff;const willingness=diff==='hard'?0.92:diff==='normal'?0.78:0.55;
  let groupBonus=1;
  if(cell.group>=0){const have=G.cells.filter(c=>c.group===cell.group&&c.owner===botIdx).length;if(have===(GRP_SIZE[cell.group]||0)-1)groupBonus=1.4;else if(have>0)groupBonus=1.15;}
  const adjustedMax=Math.min(Math.floor(cell.price*willingness*groupBonus),Math.floor(bot.money*0.75));
  if(auction.currentBid+50<=adjustedMax&&bot.money>auction.currentBid+50){
    const bidAmount=Math.min(auction.currentBid+Math.floor(50+Math.random()*150),adjustedMax);
    auction.currentBid=bidAmount;auction.leaderId=botIdx;auction.bids[botIdx]=bidAmount;
    log(`🤖 ${bot.name} 입찰: ₩${bidAmount}`,'auction');
  }else{auction.bids[botIdx]='pass';log(`🤖 ${bot.name} 패스`,'auction');}
  auction.round++;
  if(auction.round>=auction.participants.length){setTimeout(resolveAuction,500);}
  else{const nextIdx=auction.participants[auction.round%auction.participants.length];if(!G.players[nextIdx].is_bot)renderAll();else setTimeout(()=>botAuctionBid(nextIdx),600);}
}

function resolveAuction(){
  if(!G||!G.auction)return;
  const auction=G.auction;const ci=auction.ci;const cell=G.cells[ci];
  if(auction.leaderId>=0){const winner=G.players[auction.leaderId];winner.money-=auction.currentBid;cell.owner=auction.leaderId;log(`🔨 ${winner.name} ${cell.flag}${cell.name} 낙찰! ₩${auction.currentBid}`,'auction');toast(`🔨 ${winner.name} 낙찰!`,'auction');if(auction.leaderId===0)butler('auction_win');spawnSparkles(window.innerWidth*0.5,window.innerHeight*0.4,'#b26cf7',12);checkBankrupt(auction.leaderId);}
  else{log(`🔨 유찰 — ${cell.name}`,'auction');toast(`🔨 유찰!`,'lose');}
  G.auction=null;if(G.phase!=='gameover'){G.phase='roll';nextTurn();}renderAll();
  if(G.phase==='gameover')showGameOver();else setTimeout(checkBotTurn,500);
}

// ═══════════════════════════════════════════════════════════
//  TRADE
// ═══════════════════════════════════════════════════════════
function initiateTrade(){
  if(!G||animating)return;
  const pidx=G.turn,p=G.players[pidx];if(p.is_bot||p.bankrupt)return;
  const otherAlive=alive().filter(o=>G.players.indexOf(o)!==pidx);
  if(!otherAlive.length){toast('거래 상대가 없습니다','lose');return;}
  G.trade={fromIdx:pidx,toIdx:G.players.indexOf(otherAlive[0]),fromProps:[],toProps:[],fromMoney:0,toMoney:0,phase:'offer'};
  G.phase='trade_offer';renderAll();
}
function updateTradeTarget(selectEl){if(!G||!G.trade)return;G.trade.toIdx=parseInt(selectEl.value);G.trade.toProps=[];renderAll();}
function toggleTradeProp(side,ci){if(!G||!G.trade)return;const arr=side==='from'?G.trade.fromProps:G.trade.toProps;const idx=arr.indexOf(ci);if(idx>=0)arr.splice(idx,1);else arr.push(ci);renderAll();}
function updateTradeFromMoney(val){if(G&&G.trade)G.trade.fromMoney=parseInt(val)||0;}
function updateTradeToMoney(val){if(G&&G.trade)G.trade.toMoney=parseInt(val)||0;}

function submitTrade(){
  if(!G||!G.trade)return;const t=G.trade;const from=G.players[t.fromIdx],to=G.players[t.toIdx];
  if(from.money<t.fromMoney){toast('자금 부족!','lose');return;}
  if(t.fromProps.some(ci=>G.cells[ci].owner!==t.fromIdx)){toast('소유하지 않은 부동산!','lose');return;}
  if(t.toProps.some(ci=>G.cells[ci].owner!==t.toIdx)){toast('상대가 소유하지 않음!','lose');return;}
  if(to.is_bot){const accepted=botEvaluateTrade(t);if(accepted){executeTrade(t);toast(`🤝 ${to.name} 거래 수락!`,'trade');butler('trade_ok');}else{log(`❌ ${to.name} 거래 거절`,'trade');toast(`❌ 거래 거절`,'lose');butler('trade_no');G.trade=null;G.phase='roll';renderAll();}}
  else{G.trade.phase='respond';G.phase='trade_respond';renderAll();}
}

function respondTrade(accept){
  if(!G||!G.trade)return;const t=G.trade;const to=G.players[t.toIdx];
  if(accept){executeTrade(t);toast(`🤝 거래 성사!`,'trade');butler('trade_ok');}
  else{log(`❌ ${to.name} 거래 거절`,'trade');toast(`❌ 거래 거절`,'lose');butler('trade_no');}
  G.trade=null;G.phase='roll';renderAll();
}

function cancelTrade(){if(!G)return;G.trade=null;G.phase='roll';renderAll();}

function executeTrade(t){
  const from=G.players[t.fromIdx],to=G.players[t.toIdx];
  t.fromProps.forEach(ci=>G.cells[ci].owner=t.toIdx);t.toProps.forEach(ci=>G.cells[ci].owner=t.fromIdx);
  from.money-=t.fromMoney;to.money+=t.fromMoney;to.money-=t.toMoney;from.money+=t.toMoney;
  log(`🤝 거래: ${from.name} ⇌ ${to.name}`,'trade');G.trade=null;G.phase='roll';checkBankrupt(t.fromIdx);checkBankrupt(t.toIdx);renderAll();
}

function botEvaluateTrade(t){
  const diff=G.diff;let valueReceived=t.fromMoney,valueGiven=t.toMoney;
  t.fromProps.forEach(ci=>{const c=G.cells[ci];valueReceived+=c.price+(c.houses||0)*(BUILD_COST[c.group]||300);if(c.group>=0){const have=G.cells.filter(cx=>cx.group===c.group&&cx.owner===t.toIdx).length;if(have===(GRP_SIZE[c.group]||0)-1)valueReceived+=c.price*0.5;}});
  t.toProps.forEach(ci=>{const c=G.cells[ci];valueGiven+=c.price+(c.houses||0)*(BUILD_COST[c.group]||300);});
  if(diff==='easy')return Math.random()<0.6;
  return valueReceived>=valueGiven*(diff==='hard'?1.1:0.95);
}

// ═══════════════════════════════════════════════════════════
//  DICE & MOVEMENT (핵심 업그레이드)
// ═══════════════════════════════════════════════════════════
function rollDice(){return{d1:Math.floor(Math.random()*6)+1,d2:Math.floor(Math.random()*6)+1};}

// 주사위 도트 렌더링
function makeDieFace(n,size){
  const div=document.createElement('div');div.className='die-face';
  div.style.cssText=`width:${size}px;height:${size}px;`;
  div.innerHTML=DICE_DOTS[n]||DICE_DOTS[1];
  return div;
}

// 보드 중앙 주사위 애니메이션 (화려하게)
function animateDice(d1,d2,cb){
  const el1=document.getElementById('die1'),el2=document.getElementById('die2');
  if(!el1||!el2){cb&&cb();return;}
  const isDouble=d1===d2;
  el1.classList.add('rolling');el2.classList.add('rolling');
  el1.classList.remove('double-glow');el2.classList.remove('double-glow');
  const FACES=[1,2,3,4,5,6];let n=0;
  const iv=setInterval(()=>{
    // 굴리는 동안 랜덤 도트 보여주기
    const rn1=FACES[Math.floor(Math.random()*6)],rn2=FACES[Math.floor(Math.random()*6)];
    el1.innerHTML=DICE_DOTS[rn1];el2.innerHTML=DICE_DOTS[rn2];n++;
    if(n>=18){
      clearInterval(iv);
      el1.innerHTML=DICE_DOTS[d1];el2.innerHTML=DICE_DOTS[d2];
      el1.classList.remove('rolling');el2.classList.remove('rolling');
      if(isDouble){el1.classList.add('double-glow');el2.classList.add('double-glow');spawnDoubleRing();}
      cb&&cb();
    }
  },45);
}

function spawnDoubleRing(){
  const center=document.querySelector('.board-center');if(!center)return;
  const rect=center.getBoundingClientRect();
  for(let i=0;i<3;i++){
    const ring=document.createElement('div');ring.className='double-ring';
    ring.style.cssText=`left:${rect.left+rect.width/2}px;top:${rect.top+rect.height/2}px;width:80px;height:80px;animation-delay:${i*0.18}s;`;
    document.body.appendChild(ring);setTimeout(()=>ring.remove(),1200);
  }
}

// 토큰 이동 - 한 칸씩 천천히 점프
function animateMove(pidx,from,to,cb){
  if(from===to){cb&&cb();return;}
  const steps=[];let cur=from;
  while(cur!==to){cur=(cur+1)%40;steps.push(cur);}
  let i=0;
  const stepDelay=120; // 한 칸 이동 속도 (ms)
  function doStep(){
    if(i>=steps.length){cb&&cb();return;}
    G.players[pidx].pos=steps[i];
    spawnTrail(steps[i]);
    // 중간 칸 잠깐 하이라이트
    if(i>0){const prev=document.getElementById('cell-'+steps[i-1]);if(prev)prev.classList.remove('path-highlight');}
    const cur2=document.getElementById('cell-'+steps[i]);if(cur2)cur2.classList.add('path-highlight');
    renderTokensAnimating(pidx);
    i++;
    setTimeout(doStep,stepDelay);
  }
  doStep();
}

// 이동 중 토큰만 업데이트 (점프 애니메이션)
function renderTokensAnimating(movingIdx){
  for(let ci=0;ci<40;ci++){const tc=document.getElementById('tc-'+ci);if(tc)tc.innerHTML='';}
  G.players.forEach((p,pi)=>{
    if(p.bankrupt)return;
    const tc=document.getElementById('tc-'+p.pos);if(!tc)return;
    const tk=document.createElement('div');tk.className='token';
    const isMoving=pi===movingIdx;
    if(isMoving)tk.classList.add('moving');
    if(pi===G.turn)tk.style.setProperty('--tok-color',p.color);
    const tSize=Math.max(14,Math.round(boardSize/36));
    tk.style.cssText=`width:${tSize}px;height:${tSize}px;background:${p.color};font-size:${Math.round(tSize*0.62)}px;`;
    tk.textContent=p.char.emoji;tc.appendChild(tk);
  });
}

function spawnTrail(ci){
  const tc=document.getElementById('tc-'+ci);if(!tc)return;
  const rect=tc.getBoundingClientRect();
  const trail=document.createElement('div');trail.className='move-trail';
  const size=14;
  trail.style.cssText=`left:${rect.left+rect.width/2-size/2}px;top:${rect.top+rect.height/2-size/2}px;width:${size}px;height:${size}px;background:${G.players[G.turn].color};`;
  document.body.appendChild(trail);setTimeout(()=>trail.remove(),550);
}

// ═══════════════════════════════════════════════════════════
//  EFFECTS
// ═══════════════════════════════════════════════════════════
function spawnFloatText(text,color,isLoss){
  const el=document.createElement('div');el.className='float-text';
  const x=window.innerWidth/2+(floatSide%2===0?-90:90);floatSide++;
  el.style.cssText=`left:${x}px;top:${window.innerHeight/2-70}px;color:${isLoss?'#ff4560':'#10d96e'};`;
  el.textContent=text;document.body.appendChild(el);setTimeout(()=>el.remove(),1400);
}

function toast(msg,type=''){
  const container=document.getElementById('toast-container');const t=document.createElement('div');
  t.className=`toast toast-${type}`;t.innerHTML=msg;container.appendChild(t);setTimeout(()=>t.remove(),2600);
}

function spawnCoinsFly(color){
  for(let i=0;i<8;i++){
    const coin=document.createElement('div');coin.className='coin';
    const angle=(Math.random()*200-100)*(Math.PI/180);const dist=70+Math.random()*90;
    coin.style.cssText=`left:${window.innerWidth/2+(Math.random()-0.5)*120}px;top:${window.innerHeight/2}px;--mx:${Math.cos(angle)*dist/2}px;--my:${-dist/2}px;--ex:${Math.cos(angle)*dist}px;--ey:${-dist}px;--dur:${0.5+Math.random()*0.6}s;animation-delay:${i*0.06}s;`;
    coin.textContent='🪙';document.body.appendChild(coin);setTimeout(()=>coin.remove(),1400);
  }
}

function spawnSparkles(x,y,color,count){
  for(let i=0;i<count;i++){
    const sp=document.createElement('div');sp.className='sparkle';
    const angle=(i/count)*Math.PI*2;const dist=40+Math.random()*60;
    sp.style.cssText=`left:${x}px;top:${y}px;--dx:${Math.cos(angle)*dist}px;--dy:${Math.sin(angle)*dist-40}px;--dur:${0.4+Math.random()*0.4}s;animation-delay:${i*0.03}s;color:${color};font-size:${0.8+Math.random()}rem;`;
    sp.textContent='✨';document.body.appendChild(sp);setTimeout(()=>sp.remove(),900);
  }
}
function spawnAbilityFlash(color){const fl=document.createElement('div');fl.className='ability-flash';fl.style.background=`rgba(255,215,0,0.1)`;document.body.appendChild(fl);setTimeout(()=>fl.remove(),700);}
function spawnScreenFlash(colorRgba){const fl=document.createElement('div');fl.className='screen-flash';fl.style.cssText=`background:${colorRgba};--intensity:0.2;`;document.body.appendChild(fl);setTimeout(()=>fl.remove(),450);}

// ═══════════════════════════════════════════════════════════
//  PLAYER ACTIONS
// ═══════════════════════════════════════════════════════════
function doRoll(){
  if(!G||animating)return;
  animating=true;
  const p=G.players[G.turn];
  let{d1,d2}=rollDice();let total=d1+d2;const isDouble=d1===d2;
  if(p._speed_boost){total+=2;p._speed_boost=false;toast('✨ +2칸!','special');}
  G.d1=d1;G.d2=d2;
  playSound('roll');
  renderDiceCenter(); // 즉시 주사위 패널 업데이트
  animateDice(d1,d2,()=>{
    if(isDouble){
      G.doubles++;
      if(G.doubles>=3){log(`3연속 더블! ${p.name} 블랙홀!`,'important');butler('triple');toast('3연속 더블! 블랙홀!','lose');sendToJail(G.turn);G.doubles=0;nextTurn();animating=false;renderAll();setTimeout(checkBotTurn,600);return;}
      log(`🎲 더블! (${d1}+${d2})`);butler('double');toast('🎲 더블!','special');
    }else{G.doubles=0;log(`🎲 ${d1}+${d2}=${total}`);}
    renderAll();
    setTimeout(()=>{
      const from=p.pos;
      animateMove(G.turn,from,(from+total)%40,()=>{
        // 하이라이트 제거
        document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));
        // 도착 토큰 랜딩 애니메이션
        const destTc=document.getElementById('tc-'+((from+total)%40));
        if(destTc){const tk=destTc.querySelector('.token');if(tk)tk.classList.add('landed');}
        movePlayer(G.turn,total);landCell(G.turn,total);
        animating=false;
        if(!isDouble&&G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='casino'&&G.phase!=='auction'&&G.phase!=='trade_offer'&&G.phase!=='gameover')nextTurn();
        renderAll();
        if(G.phase==='gameover')showGameOver();
      });
    },180);
  });
}

function doBuy(buy){
  const pidx=G.turn,ci=G.players[pidx].pos,cell=G.cells[ci],p=G.players[pidx];
  if(buy){
    let price=cell.price;
    if(p._discount_pending){price=Math.floor(price*0.85);p._discount_pending=false;log(`✨ 15% 할인 매입!`,'gain');}
    cell.owner=pidx;p.money-=price;log(`🏠 ${p.name} ${cell.flag||''}${cell.name} 매입 -₩${price}`,'lose');
    butler('buy');playSound('buy');spawnSparkles(window.innerWidth*0.6,window.innerHeight*0.5,cell.color||'#ffd700',8);
  }else{log(`↩️ ${p.name} ${cell.name} 패스 — 경매 시작!`);startAuction(ci);return;}
  G.phase='roll';nextTurn();renderAll();setTimeout(checkBotTurn,500);
}

function doCard(){
  if(!G||!G.pending_card)return;
  playSound('card');applyCard(G.turn,G.pending_card);G.pending_card=null;
  if(G.phase!=='gameover'){nextTurn();renderAll();setTimeout(checkBotTurn,500);}else{renderAll();showGameOver();}
}

function doJail(payBail){
  if(!G)return;
  const p=G.players[G.turn];
  if(payBail){if(p.money<JAIL_BAIL)return;p.money-=JAIL_BAIL;p.jail_turns=0;log(`💰 ${p.name} 보석금 납부!`,'lose');renderAll();setTimeout(doRoll,300);}
  else{
    if(animating)return;animating=true;
    const{d1,d2}=rollDice();const total=d1+d2;const isDouble=d1===d2;
    G.d1=d1;G.d2=d2;renderDiceCenter();
    animateDice(d1,d2,()=>{
      if(isDouble){p.jail_turns=0;log(`🎉 더블 탈출!`);toast('🎉 더블 탈출!','gain');
        animateMove(G.turn,p.pos,(p.pos+total)%40,()=>{document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));movePlayer(G.turn,total);landCell(G.turn,total);if(G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='casino'&&G.phase!=='gameover')nextTurn();animating=false;renderAll();G.phase==='gameover'?showGameOver():setTimeout(checkBotTurn,600);});
      }else{
        p.jail_turns--;log(`😔 더블 실패 (${p.jail_turns}턴 남음)`);
        if(p.jail_turns<=0){p.jail_turns=0;animateMove(G.turn,p.pos,(p.pos+total)%40,()=>{document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));movePlayer(G.turn,total);landCell(G.turn,total);if(G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='casino'&&G.phase!=='gameover')nextTurn();animating=false;renderAll();G.phase==='gameover'?showGameOver():setTimeout(checkBotTurn,600);});}
        else{nextTurn();animating=false;renderAll();setTimeout(checkBotTurn,500);}
      }
    });
  }
}

function doCasino(bet){
  const pidx=G.turn,p=G.players[pidx];const casinoBet=300;
  if(!bet){log(`🎰 ${p.name} 베팅 거부`);G.phase='roll';nextTurn();renderAll();setTimeout(checkBotTurn,400);return;}
  if(p.money<casinoBet){toast('💸 베팅금 부족!','lose');G.phase='roll';nextTurn();renderAll();setTimeout(checkBotTurn,400);return;}
  p.money-=casinoBet;playSound('casino');
  const win=Math.random()<0.45;
  if(win){p.money+=casinoBet*3;log(`🎰 ${p.name} 🎉 대박! +₩${casinoBet*2}`,'gain');toast(`🎰 대박! +₩${casinoBet*2}`,'gain');spawnFloatText(`+₩${casinoBet*2}`,p.color,false);spawnCoinsFly(p.color);}
  else{log(`🎰 ${p.name} 💸 꽝! -₩${casinoBet}`,'lose');toast(`🎰 꽝! -₩${casinoBet}`,'lose');spawnFloatText(`-₩${casinoBet}`,p.color,true);checkBankrupt(pidx);}
  G.phase='roll';if(G.phase!=='gameover')nextTurn();renderAll();
  if(G.phase==='gameover')showGameOver();else setTimeout(checkBotTurn,500);
}

// ═══════════════════════════════════════════════════════════
//  BOT AI
// ═══════════════════════════════════════════════════════════
function checkBotTurn(){if(!G||G.phase==='gameover')return;const p=G.players[G.turn];if(p.is_bot&&!p.bankrupt)doBotTurn();}

function doBotTurn(){
  setTimeout(()=>{
    if(!G||G.phase==='gameover')return;
    const pidx=G.turn,p=G.players[pidx];if(!p.is_bot||p.bankrupt)return;
    if(!p.ability_used&&Math.random()<0.3){const key=p.char.abilityKey;if(key==='tax_immune')p._tax_immune=true;if(key==='card_immune')p._card_immune=true;if(key==='speed_boost')p._speed_boost=true;p.ability_used=true;}
    if(p.jail_turns>0&&G.phase==='roll'){
      if(G.diff==='hard'&&p.money>=JAIL_BAIL){p.money-=JAIL_BAIL;p.jail_turns=0;log(`💰 ${p.name} 보석금!`,'lose');renderAll();setTimeout(()=>doBotRoll(pidx),400);}
      else{const{d1,d2}=rollDice();const total=d1+d2;const isDouble=d1===d2;G.d1=d1;G.d2=d2;if(isDouble){p.jail_turns=0;log(`🎉 ${p.name} 더블 탈출!`);renderAll();animateMove(pidx,p.pos,(p.pos+total)%40,()=>{document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));movePlayer(pidx,total);landCell(pidx,total);botDecide(pidx);if(G.phase!=='gameover')nextTurn();renderAll();G.phase==='gameover'?showGameOver():setTimeout(checkBotTurn,600);});}else{p.jail_turns--;log(`😔 ${p.name} 더블 실패`);if(p.jail_turns<=0){p.jail_turns=0;renderAll();animateMove(pidx,p.pos,(p.pos+total)%40,()=>{document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));movePlayer(pidx,total);landCell(pidx,total);botDecide(pidx);if(G.phase!=='gameover')nextTurn();renderAll();G.phase==='gameover'?showGameOver():setTimeout(checkBotTurn,600);});}else{nextTurn();renderAll();setTimeout(checkBotTurn,500);}}}
      return;
    }
    if(G.phase==='buy'||G.phase==='card'){botDecide(pidx);if(G.phase!=='gameover')nextTurn();renderAll();G.phase==='gameover'?showGameOver():setTimeout(checkBotTurn,500);return;}
    if(G.phase==='casino'){if(G.diff==='hard'&&G.players[pidx].money>=600)doCasino(true);else if(G.diff==='normal'&&G.players[pidx].money>=600&&Math.random()<0.5)doCasino(true);else doCasino(false);return;}
    if(G.phase==='roll'){botBuildSmart(pidx);doBotRoll(pidx);}
  },700);
}

function doBotRoll(pidx){
  if(!G||G.phase==='gameover')return;
  const p=G.players[pidx];let{d1,d2}=rollDice();let total=d1+d2;const isDouble=d1===d2;
  if(p._speed_boost){total+=2;p._speed_boost=false;}
  G.d1=d1;G.d2=d2;
  if(isDouble){G.doubles++;if(G.doubles>=3){log(`3연속 더블! ${p.name} 블랙홀!`,'important');sendToJail(pidx);G.doubles=0;nextTurn();renderAll();setTimeout(checkBotTurn,600);return;}log(`🎲 ${p.name} 더블! (${d1}+${d2})`);}
  else{G.doubles=0;log(`🎲 ${p.name} ${d1}+${d2}=${total}`);}
  renderAll();const from=p.pos;
  setTimeout(()=>{
    animateMove(pidx,from,(from+total)%40,()=>{
      document.querySelectorAll('.path-highlight').forEach(el=>el.classList.remove('path-highlight'));
      movePlayer(pidx,total);landCell(pidx,total);botDecide(pidx);
      if(!isDouble&&G.phase!=='gameover')nextTurn();renderAll();
      if(G.phase==='gameover')showGameOver();
      else if(isDouble&&G.phase==='roll')setTimeout(()=>doBotRoll(pidx),800);
      else setTimeout(checkBotTurn,600);
    });
  },180);
}

function botDecide(pidx){
  const p=G.players[pidx],diff=G.diff;
  if(G.phase==='buy'){
    const ci=p.pos,cell=G.cells[ci],price=cell.price;let buy=false;
    if(diff==='easy')buy=Math.random()>0.3&&p.money>=price;
    else if(diff==='normal')buy=p.money>=price*1.35;
    else{if(cell.group>=0){const have=G.cells.filter(c=>c.group===cell.group&&c.owner===pidx).length;if(have===(GRP_SIZE[cell.group]||0)-1&&p.money>=price)buy=true;else buy=p.money>=price*1.15;}else buy=p.money>=price*1.05;}
    if(buy){cell.owner=pidx;p.money-=price;log(`🏠 ${p.name} ${cell.flag||''}${cell.name} 매입 -₩${price}`,'lose');}
    else{log(`↩️ ${p.name} 패스 — 경매`);startAuction(ci);return;}
    G.phase='roll';
  }else if(G.phase==='card'&&G.pending_card){applyCard(pidx,G.pending_card);G.pending_card=null;}
  else if(G.phase==='casino'){if(diff==='hard'&&p.money>=600)doCasino(true);else doCasino(false);return;}
}

function botBuildSmart(pidx){
  const p=G.players[pidx],diff=G.diff;if(diff==='easy')return;
  G.cells.forEach((c,ci)=>{if(c.owner!==pidx||c.type!=='prop')return;if(!ownsGroup(pidx,c.group)||(c.houses||0)>=4||c.mortgaged)return;const cost=BUILD_COST[c.group]||300;const thresh=diff==='hard'?1.15:1.5;if(p.money>=cost*thresh){c.houses=(c.houses||0)+1;p.money-=cost;log(`🔨 ${p.name} ${c.name} 집${c.houses}`)}});
}

// ═══════════════════════════════════════════════════════════
//  BOARD LAYOUT
// ═══════════════════════════════════════════════════════════
function getCellRect(ci){
  const S=boardSize,C=S/7,W=(S-2*C)/9;
  if(ci===0)return{x:S-C,y:S-C,w:C,h:C};
  if(ci===10)return{x:0,y:S-C,w:C,h:C};
  if(ci===20)return{x:0,y:0,w:C,h:C};
  if(ci===30)return{x:S-C,y:0,w:C,h:C};
  if(ci<10){const idx=10-ci;return{x:S-C-idx*W,y:S-C,w:W,h:C};}
  if(ci<20){const idx=ci-10;return{x:0,y:S-C-idx*W,w:C,h:W};}
  if(ci<30){const idx=ci-20;return{x:C+(idx-1)*W,y:0,w:W,h:C};}
  const idx=ci-30;return{x:S-C,y:C+(idx-1)*W,w:C,h:W};
}

// ═══════════════════════════════════════════════════════════
//  BUILD BOARD
// ═══════════════════════════════════════════════════════════
function buildBoard(){
  const boardEl=document.getElementById('board');
  const S=boardSize;boardEl.style.width=S+'px';boardEl.style.height=S+'px';boardEl.innerHTML='';
  const C=S/7,W=(S-2*C)/9,fs=Math.max(6,Math.round(S/82));

  const cellBg={go:'linear-gradient(135deg,#02100a,#041812)',jail:'linear-gradient(135deg,#120820,#0d0618)',visit:'linear-gradient(135deg,#02080f,#041018)',free:'linear-gradient(135deg,#020e04,#041408)',chance:'linear-gradient(135deg,#120820,#0d0618)',fate:'linear-gradient(135deg,#180408,#120206)',tax:'linear-gradient(135deg,#100802,#0e0602)',airport:'linear-gradient(135deg,#020a10,#040e1a)',util:'linear-gradient(135deg,#021008,#040e06)',prop:'linear-gradient(135deg,#05080f,#030610)',casino:'linear-gradient(135deg,#100602,#180a02)'};

  for(let ci=0;ci<40;ci++){
    const{x,y,w,h}=getCellRect(ci);
    const cellData=G.cells[ci];
    const isCorner=ci===0||ci===10||ci===20||ci===30;
    const isHoriz=ci<10||ci>=30;
    const isLeft=ci>=10&&ci<20;
    const isTop=ci>=20&&ci<30;

    const div=document.createElement('div');div.className='cell'+(isCorner?' cell-corner':'');div.id='cell-'+ci;
    div.style.cssText=`left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;
    div.style.background=cellBg[cellData.type]||cellBg.prop;
    if(cellData.type==='casino')div.classList.add('casino-cell');
    if(cellData.type==='jail')div.classList.add('jail-cell');
    if(cellData.type==='chance'||cellData.type==='fate')div.classList.add('event-cell');

    // 컬러 바
    if(cellData.color&&cellData.type==='prop'){const bar=document.createElement('div');bar.className='color-bar';bar.id='bar-'+ci;const bThick=Math.round(Math.min(h,w)*0.18);if(isHoriz)bar.style.cssText=`top:0;left:0;width:100%;height:${bThick}px;background:${cellData.color};`;else if(isLeft)bar.style.cssText=`top:0;right:0;width:${bThick}px;height:100%;background:${cellData.color};`;else if(isTop)bar.style.cssText=`bottom:0;left:0;width:100%;height:${bThick}px;background:${cellData.color};`;div.appendChild(bar);}
    if(cellData.type==='airport'){const bar=document.createElement('div');bar.className='airport-bar';if(isHoriz)bar.style.cssText=`top:0;left:0;width:100%;height:${Math.round(Math.min(h,w)*0.16)}px;`;else bar.style.cssText=`top:0;right:0;width:${Math.round(Math.min(w,h)*0.16)}px;height:100%;`;div.appendChild(bar);}

    // 텍스트/아이콘
    const tw=document.createElement('div');tw.id='tw-'+ci;
    tw.style.cssText=`position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;gap:1px;z-index:1;`;
    const iconMap={go:'🚩',jail:'⚫',visit:'✈️',free:'🅿️',chance:'❓',fate:'⭐',tax:'💸',airport:'✈️',casino:'🎰'};
    let icon=cellData.flag||iconMap[cellData.type]||'';
    if(cellData.type==='util')icon=cellData.name.includes('전기')?'⚡':'🔥';
    if(cellData.type==='prop')icon=cellData.flag||'';
    if(icon){const iconEl=document.createElement('div');iconEl.className='cell-icon';iconEl.textContent=icon;iconEl.style.fontSize=(isCorner?Math.round(fs*2.3):Math.round(fs*1.5))+'px';tw.appendChild(iconEl);}
    const nameEl=document.createElement('div');nameEl.className='cell-name';nameEl.id='cn-'+ci;
    nameEl.textContent=isCorner?cellData.name:cellData.name.length>4?cellData.name.slice(0,4):cellData.name;nameEl.style.fontSize=(isCorner?fs+2:fs)+'px';nameEl.style.padding='0 1px';tw.appendChild(nameEl);
    if(cellData.price>0&&!isCorner){const priceEl=document.createElement('div');priceEl.className='cell-price';priceEl.textContent=cellData.price.toLocaleString();priceEl.style.fontSize=Math.max(4,fs-1)+'px';priceEl.style.opacity='0.6';tw.appendChild(priceEl);}
    div.appendChild(tw);

    // 집/호텔
    const housesEl=document.createElement('div');housesEl.id='houses-'+ci;
    housesEl.style.cssText=`position:absolute;display:flex;gap:1px;align-items:center;z-index:2;`;
    if(isHoriz){housesEl.style.bottom='2px';housesEl.style.left='50%';housesEl.style.transform='translateX(-50%)';}
    else{housesEl.style.left='2px';housesEl.style.top='50%';housesEl.style.flexDirection='column';housesEl.style.transform='translateY(-50%)';}
    div.appendChild(housesEl);

    // 소유자 배지
    const badge=document.createElement('div');badge.className='owner-badge';badge.id='ob-'+ci;const bs=Math.max(5,Math.round(fs*0.7));
    badge.style.cssText=`width:${bs}px;height:${bs}px;display:none;top:2px;right:2px;position:absolute;z-index:3;border-radius:50%;border:1.5px solid rgba(0,0,0,0.6);`;
    div.appendChild(badge);
    const ownRing=document.createElement('div');ownRing.className='own-ring';ownRing.id='or-'+ci;div.appendChild(ownRing);
    const mort=document.createElement('div');mort.className='mortgaged-overlay';mort.id='mo-'+ci;mort.style.cssText='display:none;';mort.textContent='저당';mort.style.fontSize=Math.max(4,fs-1)+'px';div.appendChild(mort);

    div.addEventListener('mouseenter',e=>showTooltip(ci,e));div.addEventListener('mouseleave',hideTooltip);
    boardEl.appendChild(div);
  }

  // 보드 중앙 (주사위 크게)
  const center=document.createElement('div');center.className='board-center';
  center.style.cssText=`left:${C}px;top:${C}px;width:${S-2*C}px;height:${S-2*C}px;`;
  const logoFs=Math.round(S/13);
  const dieSize=Math.round(S/9); // 주사위 더 크게

  center.innerHTML=`
    <div class="board-logo" style="font-size:${logoFs}px;">🌍<br>인베스트마블</div>
    <div class="board-sub" style="font-size:${Math.round(S/92)}px;margin-bottom:10px;">REMASTERED</div>
    <div class="dice-center">
      <div class="die-face" id="die1" style="width:${dieSize}px;height:${dieSize}px;">${DICE_DOTS[1]}</div>
      <div class="die-face" id="die2" style="width:${dieSize}px;height:${dieSize}px;">${DICE_DOTS[2]}</div>
    </div>
    <div class="dice-sum" id="dice-sum-center" style="font-size:${Math.round(dieSize*0.38)}px;margin-top:6px;">합계 <span style="font-size:${Math.round(dieSize*0.6)}px;color:var(--gold)">3</span></div>`;
  boardEl.appendChild(center);

  // 토큰 클러스터
  for(let ci=0;ci<40;ci++){
    const{x,y,w,h}=getCellRect(ci);
    const cluster=document.createElement('div');cluster.className='token-cluster';cluster.id='tc-'+ci;
    cluster.style.cssText=`left:${x}px;top:${y}px;width:${w}px;height:${h}px;position:absolute;`;
    boardEl.appendChild(cluster);
  }
}

// ═══════════════════════════════════════════════════════════
//  RENDER
// ═══════════════════════════════════════════════════════════
function renderBoard(){
  if(!G)return;
  const fs=Math.max(6,Math.round(boardSize/82));
  G.cells.forEach((c,ci)=>{
    const housesEl=document.getElementById('houses-'+ci);
    if(housesEl){housesEl.innerHTML='';if(c.type==='prop'&&(c.houses||0)>0&&!c.mortgaged){if(c.houses===4){const h=document.createElement('div');h.className='hotel-marker';h.style.width=Math.round(fs*1.6)+'px';h.style.height=Math.round(fs*1.1)+'px';housesEl.appendChild(h);}else{for(let i=0;i<c.houses;i++){const hd=document.createElement('div');hd.className='house-dot';hd.style.width=hd.style.height=Math.round(fs*0.88)+'px';housesEl.appendChild(hd);}}}}
    const ob=document.getElementById('ob-'+ci);if(ob){if(c.owner!==null&&!c.mortgaged){ob.style.display='block';ob.style.background=G.players[c.owner].color;ob.style.boxShadow=`0 0 10px ${G.players[c.owner].color}`;}else ob.style.display='none';}
    const orEl=document.getElementById('or-'+ci);if(orEl){if(c.owner!==null&&!c.mortgaged){orEl.style.borderColor=G.players[c.owner].color+'55';orEl.style.boxShadow=`inset 0 0 8px ${G.players[c.owner].color}18`;}else{orEl.style.borderColor='transparent';orEl.style.boxShadow='none';}}
    const mo=document.getElementById('mo-'+ci);if(mo)mo.style.display=c.mortgaged?'flex':'none';
  });
}

function renderDiceCenter(){
  if(!G)return;
  // 보드 중앙 주사위
  const el1=document.getElementById('die1'),el2=document.getElementById('die2');
  if(el1)el1.innerHTML=DICE_DOTS[G.d1]||DICE_DOTS[1];
  if(el2)el2.innerHTML=DICE_DOTS[G.d2]||DICE_DOTS[1];
  const sumEl=document.getElementById('dice-sum-center');
  if(sumEl){
    const isDouble=G.d1===G.d2;
    sumEl.className='dice-sum'+(isDouble?' double':'');
    sumEl.innerHTML=`합계 <span>${G.d1+G.d2}</span>${isDouble?'<span class="dice-double-badge">🎲 더블!</span>':''}`;
  }
}

function renderTokens(){
  for(let ci=0;ci<40;ci++){const tc=document.getElementById('tc-'+ci);if(tc)tc.innerHTML='';}
  G.players.forEach((p,pi)=>{
    if(p.bankrupt)return;
    const tc=document.getElementById('tc-'+p.pos);if(!tc)return;
    const tk=document.createElement('div');tk.className='token';
    const isActive=pi===G.turn&&!animating;
    if(isActive){tk.classList.add('active-token');tk.style.setProperty('--tok-color',p.color);}
    const tSize=Math.max(14,Math.round(boardSize/36));
    tk.style.cssText=`width:${tSize}px;height:${tSize}px;background:${p.color};font-size:${Math.round(tSize*0.62)}px;`;
    tk.textContent=p.char.emoji;tc.appendChild(tk);
  });
}

function renderPlayers(){
  const el=document.getElementById('players-list');if(!el||!G)return;
  const nws=G.players.map((_,i)=>getNetWorth(i));const maxNW=Math.max(...nws,START_MONEY);
  el.innerHTML=G.players.map((p,i)=>{
    const isAct=i===G.turn&&!p.bankrupt;const nwPct=Math.round((nws[i]/maxNW)*100);
    const jailBadge=p.jail_turns>0?`<span class="badge-jail">⚫${p.jail_turns}</span>`:'';
    const abilBadge=!p.ability_used&&!p.is_bot?`<span class="badge-ability">✨능력</span>`:'';
    const tradeBadge=G.phase==='trade_respond'&&G.trade&&G.trade.toIdx===i&&!p.is_bot?`<span class="badge-trade">🤝제안</span>`:'';
    if(p.bankrupt)return`<div class="player-card bankrupt" style="--p-color:${p.color}"><div class="player-avatar" style="opacity:0.35">${p.char.emoji}</div><div class="player-info"><div class="player-name-row"><span class="player-name-txt" style="color:${p.color}">${p.name}</span><span class="badge-bankrupt">💀파산</span></div><div class="player-money" style="color:#444">₩0</div></div></div>`;
    return`<div class="player-card${isAct?' active':''}" style="--p-color:${p.color}"><div class="player-avatar">${p.char.emoji}</div><div class="player-info"><div class="player-name-row"><span class="player-name-txt" style="color:${p.color}">${p.name}</span>${p.is_bot?'<span class="bot-badge">AI</span>':''}${jailBadge}${abilBadge}${tradeBadge}</div><div class="player-money">₩${p.money.toLocaleString()}</div><div class="net-worth-bar"><div class="net-worth-fill" style="width:${nwPct}%;background:${p.color}"></div></div></div></div>`;
  }).join('');
}

function renderAction(){
  const az=document.getElementById('action-zone');if(!az||!G)return;
  const pidx=G.turn,p=G.players[pidx],phase=G.phase;
  let html=`<div class="turn-banner" style="color:${p.color}"><span class="turn-avatar">${p.char.emoji}</span>${p.name}${p.is_bot?' AI':''} 차례</div>`;

  // ★ 주사위 패널 (크고 화려하게)
  const dieS=46;
  const isDouble=G.d1===G.d2;
  html+=`<div class="dice-panel">
    <div class="dice-panel-row">
      <div class="die-side${isDouble?' double-side':''}" style="width:${dieS}px;height:${dieS}px;">${DICE_DOTS[G.d1]||DICE_DOTS[1]}</div>
      <div class="die-side${isDouble?' double-side':''}" style="width:${dieS}px;height:${dieS}px;">${DICE_DOTS[G.d2]||DICE_DOTS[1]}</div>
    </div>
    <div class="dice-result${isDouble?' is-double':''}">
      🎲<span class="total-num">${G.d1+G.d2}</span>${isDouble?'<span class="dice-double-badge">더블!</span>':''}
    </div>
  </div>`;

  if(p.is_bot){html+=`<div class="info-box">🤖 AI 처리 중...</div>`;az.innerHTML=html;return;}
  if(p.bankrupt){az.innerHTML=html;return;}

  // Trade respond
  if(phase==='trade_respond'&&G.trade&&G.trade.toIdx===pidx){
    const t=G.trade;const from=G.players[t.fromIdx];
    const fp=t.fromProps.map(ci=>CELLS[ci].name).join(', ')||'없음';
    const tp=t.toProps.map(ci=>CELLS[ci].name).join(', ')||'없음';
    html+=`<div class="trade-box"><div class="trade-title">🤝 거래 제안!</div>
      <div style="font-size:0.7rem;color:var(--text3);margin-bottom:8px"><b style="color:${from.color}">${from.name}</b>의 제안:</div>
      <div style="font-size:0.7rem;color:var(--cyan);margin-bottom:4px">📤 ${from.name}: ${fp} + ₩${t.fromMoney.toLocaleString()}</div>
      <div style="font-size:0.7rem;color:var(--pink);margin-bottom:10px">📥 내 지불: ${tp} + ₩${t.toMoney.toLocaleString()}</div></div>
    <div class="btn-row"><button class="btn btn-green" onclick="respondTrade(true)">✅ 수락</button><button class="btn btn-ghost" onclick="respondTrade(false)">❌ 거절</button></div>`;
    az.innerHTML=html;return;
  }

  if(phase==='trade_offer'&&G.trade&&G.trade.fromIdx===pidx){
    const t=G.trade;
    const myProps=G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx&&['prop','airport','util'].includes(c.type)&&!c.mortgaged);
    const otherAlive=alive().filter(o=>G.players.indexOf(o)!==pidx);
    const targetChips=()=>{const tIdx=t.toIdx;return G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===tIdx&&['prop','airport','util'].includes(c.type)&&!c.mortgaged).map(({c,ci})=>`<div class="trade-prop-chip${t.toProps.includes(ci)?' selected-trade':''}" onclick="toggleTradeProp('to',${ci})">${c.flag||''}${c.name}</div>`).join('')||'<span style="font-size:0.65rem;color:var(--text3)">소유 없음</span>';};
    html+=`<div class="trade-box"><div class="trade-title">🤝 거래 협상</div>
      <div class="trade-section">상대 선택</div>
      <select class="trade-target-select" onchange="updateTradeTarget(this)">${otherAlive.map(o=>{const i=G.players.indexOf(o);return`<option value="${i}"${t.toIdx===i?' selected':''}>${o.char.emoji} ${o.name}</option>`;}).join('')}</select>
      <div class="trade-section">📤 내가 줄 것</div>
      <div class="trade-prop-list">${myProps.map(({c,ci})=>`<div class="trade-prop-chip${t.fromProps.includes(ci)?' selected-trade':''}" onclick="toggleTradeProp('from',${ci})">${c.flag||''}${c.name}</div>`).join('')||'<span style="font-size:0.65rem;color:var(--text3)">소유 없음</span>'}</div>
      <input class="trade-money-input" type="number" placeholder="추가 지불 금액 (₩)" min="0" max="${p.money}" value="${t.fromMoney}" oninput="updateTradeFromMoney(this.value)">
      <div class="trade-section">📥 내가 받을 것</div>
      <div class="trade-prop-list">${targetChips()}</div>
      <input class="trade-money-input" type="number" placeholder="상대 추가 지불 요청 (₩)" min="0" value="${t.toMoney}" oninput="updateTradeToMoney(this.value)">
    </div>
    <div class="btn-row"><button class="btn btn-cyan" onclick="submitTrade()">📨 제안 보내기</button><button class="btn btn-ghost" onclick="cancelTrade()">취소</button></div>`;
    az.innerHTML=html;return;
  }

  if(phase==='roll'){
    if(p.jail_turns>0){
      html+=`<div class="info-box">⚫ 블랙홀 구금 (${p.jail_turns}턴 남음)<br>보석금: ₩${JAIL_BAIL.toLocaleString()}</div>`;
      html+=`<div class="btn-row"><button class="btn btn-orange" onclick="doJail(true)" ${p.money<JAIL_BAIL?'disabled':''}>💰 보석금</button><button class="btn btn-roll" style="flex:1.4" onclick="doJail(false)">🎲 더블 도전</button></div>`;
    }else{
      if(!p.ability_used)html+=`<button class="btn btn-purple" onclick="useAbility()">✨ ${p.char.ability}</button>`;
      html+=`<button class="btn btn-roll" onclick="doRoll()" ${animating?'disabled':''}>🎲 주사위 굴리기!</button>`;
      html+=`<div class="btn-row"><button class="btn btn-cyan" onclick="initiateTrade()">🤝 협상</button><button class="mgr-toggle${mgrOpen?' open':''}" style="flex:1.4;border-radius:var(--r2);font-size:0.74rem;padding:8px 10px" onclick="toggleMgr()">🏗️ 관리 <span class="mgr-toggle-arrow">▼</span></button></div>`;
      html+=`<div class="mgr-list${mgrOpen?' open':''}" id="mgr-list"></div>`;
    }
  }else if(phase==='buy'){
    const ci=p.pos,cell=G.cells[ci];
    const rentTable=cell.type==='prop'?[['기본',`₩${cell.rent}`],['독점',`₩${cell.rent*2}`],['집1',`₩${cell.rent*RENT_MULT[1]}`],['집2',`₩${cell.rent*RENT_MULT[2]}`],['집3',`₩${cell.rent*RENT_MULT[3]}`],['호텔',`₩${cell.rent*RENT_MULT[4]}`]]:[];
    html+=`<div class="prop-card-popup" style="--card-color:${cell.color||'rgba(255,215,0,0.15)'}">
      <div class="prop-card-color-band" style="background:${cell.color||'linear-gradient(90deg,#ffd700,#ff8c00)'}"></div>
      <div class="prop-card-flag">${cell.flag||'🏠'}</div>
      <div class="prop-card-city">${cell.name}</div>
      <div class="prop-card-country">${cell.country||''}</div>
      <div class="prop-card-price">₩${cell.price.toLocaleString()}</div>
      ${rentTable.map(r=>`<div class="prop-card-rent-row"><span>${r[0]}</span><span>${r[1]}</span></div>`).join('')}
    </div>
    <button class="btn btn-green" onclick="doBuy(true)" ${p.money<cell.price?'disabled':''}>✅ 매입! -₩${cell.price.toLocaleString()}</button>
    <button class="btn btn-purple" onclick="doBuy(false)">🔨 경매 시작</button>`;
  }else if(phase==='card'&&G.pending_card){
    const card=G.pending_card;
    const amtHtml=card.amount!==undefined?`<div class="card-effect ${card.amount>0?'gain':'lose'}">${card.amount>0?'+':''}₩${Math.abs(card.amount).toLocaleString()}</div>`:`<div class="card-effect">${card.type==='goto_jail'?'⚫ 블랙홀!':card.type==='nearest_airport'?'✈️ 공항으로!':card.type==='special'?'🌈 특별 혜택!':''}</div>`;
    html+=`<div class="card-box"><div class="card-emoji">${card.emoji}</div><div class="card-title">${card.text}</div>${amtHtml}</div><button class="btn btn-roll" onclick="doCard()">확인!</button>`;
  }else if(phase==='casino'){
    const casinoBet=300;
    html+=`<div class="casino-box">
      <div class="casino-title">🎰 라스베가스!</div>
      <div class="casino-slots" id="casino-slots">🍒🍋🔔</div>
      <div class="casino-odds">당첨 확률 45% · 당첨 시 베팅의 3배<br>꽝 시 베팅금 손실</div>
      <div class="casino-amount">베팅: ₩${casinoBet.toLocaleString()}</div>
    </div>
    <div class="btn-row">
      <button class="btn btn-gold" onclick="doCasino(true)" ${p.money<casinoBet?'disabled':''}>🎲 베팅!</button>
      <button class="btn btn-ghost" onclick="doCasino(false)">패스</button>
    </div>`;
  }else if(phase==='auction'&&G.auction){
    const auction=G.auction;const ci=auction.ci;const cell=G.cells[ci];
    const leader=auction.leaderId>=0?G.players[auction.leaderId].name:'없음';
    const minBid=auction.currentBid+50;const amIPart=auction.participants.includes(pidx);
    html+=`<div class="auction-box">
      <div class="auction-title">🔨 경매!</div>
      <div style="font-size:1.6rem;margin:6px 0">${cell.flag||'🏠'}</div>
      <div style="font-weight:800;font-size:0.9rem;color:var(--text)">${cell.name} · ${cell.country||''}</div>
      <div class="auction-current">₩${auction.currentBid.toLocaleString()}</div>
      <div class="auction-leader">최고 입찰자: <b style="color:${auction.leaderId>=0?G.players[auction.leaderId].color:'#666'}">${leader}</b></div>
    </div>`;
    if(amIPart&&!p.bankrupt){
      html+=`<div class="btn-row" style="margin-bottom:6px"><input class="bid-input" type="number" id="bid-input" placeholder="입찰가" min="${minBid}" value="${Math.min(minBid,p.money)}" step="50"></div>
      <div class="btn-row"><button class="btn btn-purple" onclick="playerBid(parseInt(document.getElementById('bid-input').value)||0)" ${p.money<minBid?'disabled':''}>🔨 입찰!</button><button class="btn btn-ghost" onclick="playerPass()">↩️ 패스</button></div>`;
    }else{html+=`<div class="info-box">🤖 AI 입찰 중...</div>`;}
  }

  az.innerHTML=html;
  if(phase==='roll'&&!p.jail_turns&&mgrOpen)renderMgr();
  animateCasinoSlots();
}

function animateCasinoSlots(){
  const el=document.getElementById('casino-slots');if(!el)return;
  const symbols=['🍒','🍋','🔔','💎','7️⃣','🍀'];
  const iv=setInterval(()=>{if(!document.getElementById('casino-slots')){clearInterval(iv);return;}el.textContent=symbols[Math.floor(Math.random()*symbols.length)]+symbols[Math.floor(Math.random()*symbols.length)]+symbols[Math.floor(Math.random()*symbols.length)];},120);
  setTimeout(()=>clearInterval(iv),5000);
}

function toggleMgr(){mgrOpen=!mgrOpen;renderAction();}
function renderMgr(){
  const el=document.getElementById('mgr-list');if(!el)return;
  const pidx=G.turn,p=G.players[pidx];
  const mine=G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx);
  if(!mine.length){el.innerHTML=`<div style="font-size:0.66rem;color:var(--text3);padding:4px 2px">소유 부동산 없음</div>`;return;}
  const fs=Math.max(6,Math.round(boardSize/82));
  el.innerHTML=mine.map(({c,ci})=>{
    if(!['prop','airport','util'].includes(c.type))return'';
    const canBuild=c.type==='prop'&&ownsGroup(pidx,c.group)&&!c.mortgaged&&(c.houses||0)<4;
    const cost=BUILD_COST[c.group]||300;
    let hIcons='';if(c.houses===4)hIcons='<span style="color:#ff4560;font-size:0.6rem">🏨</span>';else for(let i=0;i<(c.houses||0);i++)hIcons+='<span style="color:#10d96e;font-size:0.6rem">■</span>';
    return`<div class="prop-row"><div class="prop-color" style="background:${c.color||'#555'}"></div><span class="prop-name${c.mortgaged?' mortgaged':''}">${c.flag||''}${c.name}${hIcons}</span><div class="prop-btns">${canBuild&&p.money>=cost?`<button class="mini-b mini-b-build" onclick="doBuild(${pidx},${ci})">${(c.houses||0)===3?'🏨':'🏠'}</button>`:''}${!c.mortgaged&&(c.houses||0)===0?`<button class="mini-b mini-b-mort" onclick="doMortgage(${pidx},${ci})">저당</button>`:''}${c.mortgaged?`<button class="mini-b mini-b-unmort" onclick="doUnmortgage(${pidx},${ci})" ${p.money<Math.floor(c.price*0.6)?'disabled':''}>해제</button>`:''}</div></div>`;
  }).join('');
}

function renderLog(){
  const el=document.getElementById('log-area');if(!el)return;
  el.innerHTML=G.log.slice(0,60).map(e=>`<div class="log-row log-${e.style||''}">${e.msg}</div>`).join('');
}

function renderAll(){if(!G)return;renderBoard();renderTokens();renderDiceCenter();renderPlayers();renderAction();renderLog();}

// ═══════════════════════════════════════════════════════════
//  TOOLTIP
// ═══════════════════════════════════════════════════════════
function showTooltip(ci,e){
  if(!G)return;const c=G.cells[ci];const tt=document.getElementById('tooltip');
  document.getElementById('tt-title').innerHTML=`${c.color?`<span class="tooltip-band" style="background:${c.color}"></span>`:''}${c.flag||''} ${c.name}`;
  let rows='';
  if(c.type==='prop'){rows+=`<div class="tooltip-row"><span>국가</span><span>${c.country||'-'}</span></div><div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;if(c.owner!==null){rows+=`<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;if(!c.mortgaged){const rent=calcRent(ci,7);rows+=`<div class="tooltip-row"><span>현재 임료</span><span style="color:#10d96e">₩${rent.toLocaleString()}</span></div>`;}}if((c.houses||0)>0)rows+=`<div class="tooltip-row"><span>건물</span><span>${c.houses===4?'🏨 호텔':'🏠 집'+c.houses+'채'}</span></div>`;if(c.mortgaged)rows+=`<div class="tooltip-row" style="color:#ff4560"><span>저당 중</span><span>⚠️</span></div>`;}
  else if(c.type==='airport'){rows+=`<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;if(c.owner!==null){const n=G.cells.filter(c2=>c2.type==='airport'&&c2.owner===c.owner).length;rows+=`<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div><div class="tooltip-row"><span>현재 임료</span><span style="color:#10d96e">₩${(100*n*n).toLocaleString()}</span></div>`;}rows+=`<div class="tooltip-row"><span>1/2/3/4개</span><span>₩100/400/900/1600</span></div>`;}
  else if(c.type==='tax'){rows+=`<div class="tooltip-row"><span>세금</span><span style="color:#ff4560">₩${c.price.toLocaleString()}</span></div>`;}
  else if(c.type==='util'){rows+=`<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div><div class="tooltip-row"><span>1개</span><span>주사위×4</span></div><div class="tooltip-row"><span>2개</span><span>주사위×12</span></div>`;}
  else if(c.type==='casino'){rows+=`<div class="tooltip-row"><span>베팅</span><span>₩300</span></div><div class="tooltip-row"><span>당첨시</span><span style="color:#10d96e">₩900</span></div><div class="tooltip-row"><span>당첨율</span><span>45%</span></div>`;}
  document.getElementById('tt-body').innerHTML=rows;
  tt.style.display='block';
  let lx=e.target.getBoundingClientRect().right+10,ly=e.target.getBoundingClientRect().top;
  if(lx+185>window.innerWidth)lx=e.target.getBoundingClientRect().left-195;if(ly+170>window.innerHeight)ly=window.innerHeight-180;
  tt.style.left=lx+'px';tt.style.top=ly+'px';
}
function hideTooltip(){document.getElementById('tooltip').style.display='none';}

// ═══════════════════════════════════════════════════════════
//  SOUND
// ═══════════════════════════════════════════════════════════
let audioCtx=null;
function getAudioCtx(){if(!audioCtx)try{audioCtx=new(window.AudioContext||window.webkitAudioContext)();}catch(e){}return audioCtx;}
function playSound(type){
  const ctx=getAudioCtx();if(!ctx)return;
  try{const osc=ctx.createOscillator(),gain=ctx.createGain();osc.connect(gain);gain.connect(ctx.destination);const now=ctx.currentTime;
    if(type==='roll'){osc.type='square';osc.frequency.setValueAtTime(300,now);osc.frequency.exponentialRampToValueAtTime(650,now+0.1);osc.frequency.exponentialRampToValueAtTime(200,now+0.22);gain.gain.setValueAtTime(0.07,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.27);osc.start(now);osc.stop(now+0.27);}
    else if(type==='buy'){osc.type='sine';[523,659,784].forEach((f,i)=>{osc.frequency.setValueAtTime(f,now+i*0.1);});gain.gain.setValueAtTime(0.09,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.42);osc.start(now);osc.stop(now+0.42);}
    else if(type==='card'){osc.type='triangle';osc.frequency.setValueAtTime(440,now);osc.frequency.exponentialRampToValueAtTime(920,now+0.18);gain.gain.setValueAtTime(0.06,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.32);osc.start(now);osc.stop(now+0.32);}
    else if(type==='casino'){osc.type='sawtooth';[800,400,1200,600,1800].forEach((f,i)=>{osc.frequency.setValueAtTime(f,now+i*0.05);});gain.gain.setValueAtTime(0.05,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.32);osc.start(now);osc.stop(now+0.32);}
    else if(type==='click'){osc.type='sine';osc.frequency.setValueAtTime(1100,now);osc.frequency.exponentialRampToValueAtTime(700,now+0.06);gain.gain.setValueAtTime(0.04,now);gain.gain.exponentialRampToValueAtTime(0.001,now+0.09);osc.start(now);osc.stop(now+0.09);}
    else if(type==='win'){[523,659,784,1047,1319].forEach((freq,i)=>{const o2=ctx.createOscillator(),g2=ctx.createGain();o2.connect(g2);g2.connect(ctx.destination);o2.type='sine';o2.frequency.setValueAtTime(freq,now+i*0.1);g2.gain.setValueAtTime(0.11,now+i*0.1);g2.gain.exponentialRampToValueAtTime(0.001,now+i*0.1+0.28);o2.start(now+i*0.1);o2.stop(now+i*0.1+0.28);});}
  }catch(e){}}

// ═══════════════════════════════════════════════════════════
//  START / OVER / RESET
// ═══════════════════════════════════════════════════════════
function startGame(){
  const name=document.getElementById('inp-name').value.trim()||'여행자';
  const bots=parseInt(document.getElementById('inp-bots').value);
  const diff=document.getElementById('inp-diff').value;
  G=initGame(name,bots,diff);
  document.getElementById('setup').style.display='none';
  document.getElementById('game').style.display='flex';
  setTimeout(()=>{
    const bw=document.querySelector('.board-wrap');
    if(bw){const avail=Math.min(bw.offsetWidth-20,bw.offsetHeight-20);boardSize=Math.max(340,Math.min(680,avail));}
    buildBoard();
    log('🌍 인베스트마블 REMASTERED 시작!','important');
    log('🎲 주사위 도트 · 천천히 이동 · 도착 강조 효과 추가!');
    renderAll();setTimeout(checkBotTurn,1000);
  },60);
}

function showGameOver(){
  if(!G||!G.winner)return;
  const winnerP=G.players[G.winnerIdx];playSound('win');
  document.getElementById('winner-avatar').textContent=winnerP.char.emoji;
  document.getElementById('winner-name').textContent=`${winnerP.name} 우승!`;
  const ranked=[...G.players].sort((a,b)=>getNetWorth(G.players.indexOf(b))-getNetWorth(G.players.indexOf(a)));
  const medals=['🥇','🥈','🥉','4️⃣'];
  document.getElementById('rank-list').innerHTML=ranked.map((p,i)=>{const ri=G.players.indexOf(p);return`<div class="rank-row"><span class="rank-medal">${medals[i]||''}</span><span style="font-size:1.25rem">${p.char.emoji}</span><span class="rank-player" style="color:${p.color}">${p.name}</span>${p.bankrupt?`<span style="color:var(--red);font-size:0.7rem">💀 파산</span>`:`<span class="rank-money">₩${getNetWorth(ri).toLocaleString()}</span>`}</div>`;}).join('');
  document.getElementById('gameover').style.display='flex';
  butler('win');spawnConfetti();spawnFireworks();
}

function resetToChar(){
  G=null;mgrOpen=false;animating=false;selectedChar=null;
  document.getElementById('gameover').style.display='none';document.getElementById('game').style.display='none';document.getElementById('setup').style.display='none';document.getElementById('char-select').style.display='flex';
  document.querySelectorAll('.char-card').forEach(el=>el.classList.remove('selected'));document.getElementById('char-next-btn').classList.remove('active');
}

function spawnConfetti(){
  const colors=['#ff4560','#4dabf7','#10d96e','#ff8c42','#b26cf7','#ffd700','#2dd4bf','#f472b6'];
  for(let i=0;i<160;i++){const d=document.createElement('div');d.className='confetti-piece';const size=5+Math.random()*12,dur=2+Math.random()*3,delay=Math.random()*2.5;d.style.cssText=`left:${Math.random()*100}%;top:-20px;width:${size}px;height:${size*0.6}px;background:${colors[Math.floor(Math.random()*colors.length)]};border-radius:50%;animation-duration:${dur}s;animation-delay:${delay}s;`;document.body.appendChild(d);setTimeout(()=>d.remove(),(dur+delay+0.5)*1000);}
}

function spawnFireworks(){
  const bg=document.getElementById('fireworks-bg');if(!bg)return;
  for(let fw=0;fw<6;fw++){setTimeout(()=>{const x=20+Math.random()*60,y=10+Math.random()*50;const colors=['#ffd700','#ff4560','#4dabf7','#10d96e','#b26cf7'];const color=colors[Math.floor(Math.random()*colors.length)];for(let i=0;i<20;i++){const p=document.createElement('div');const angle=(i/20)*Math.PI*2,dist=60+Math.random()*80,dur=0.6+Math.random()*0.6;p.style.cssText=`position:absolute;left:${x}%;top:${y}%;width:5px;height:5px;border-radius:50%;background:${color};animation:sparkleFly ${dur}s ease-out forwards;--dx:${Math.cos(angle)*dist}px;--dy:${Math.sin(angle)*dist}px;`;bg.appendChild(p);setTimeout(()=>p.remove(),(dur+0.1)*1000);}},fw*500);}
}

window.addEventListener('DOMContentLoaded',()=>{initStars();renderCharGrid();});
</script>
</body>
</html>
"""

def render():
    import streamlit as st
    # 게임 헤더 UI
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0c1020,#111828);border:1px solid rgba(108,99,255,0.25);
      border-radius:16px;padding:16px 24px;margin-bottom:12px;display:flex;align-items:center;gap:16px;'>
      <div style='font-size:2rem;'>🎲</div>
      <div>
        <div style='font-family:"Black Han Sans",sans-serif;font-size:1.1rem;color:#e8f0ff;'>🎲 인베스트 마블 REMASTERED</div>
        <div style='font-size:0.82rem;color:#8899bb;margin-top:2px;'>모노폴리 기반 투자 보드게임. AI 봇과 세계 랜드마크를 독점하여 최고 부자가 되세요!</div>
        <div style='font-size:0.76rem;color:#6c63ff;margin-top:4px;'>🎮 주사위 굴리기 → 부지 매입 → 집/호텔 건설 → 임대료 수익 | 같은 색 독점 시 임대료 2배!</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
    .block-container{padding:0 !important;max-width:100% !important;}
    iframe{border:none;}
    </style>
    """, unsafe_allow_html=True)
    st.caption("📱 모바일: 가로 화면 권장 | 🖥️ 권장: 1280px 이상")
    components.html(GAME_HTML, height=880, scrolling=True)

if __name__ == "__main__":
    render()
