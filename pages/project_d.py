import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>부루마블 🎲</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Black+Han+Sans&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0e0e14;
  --bg2: #16161f;
  --bg3: #1e1e2a;
  --border: rgba(255,255,255,0.08);
  --border2: rgba(255,255,255,0.14);
  --text: #f0f0f5;
  --text2: #9090a8;
  --text3: #5a5a6e;
  --accent: #ff4d6d;
  --accent2: #ff8fa3;
  --gold: #ffd700;
  --green: #22c55e;
  --blue: #3b82f6;
  --red: #ef4444;
  --orange: #f97316;
  --purple: #a855f7;
  --teal: #14b8a6;
  --r: 12px;
  --r2: 8px;
  --shadow: 0 4px 24px rgba(0,0,0,0.5);
  --shadow2: 0 2px 12px rgba(0,0,0,0.4);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Noto Sans KR', sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow: hidden;
  height: 100vh;
  width: 100vw;
}

/* ══════════════════════════════════
   SETUP SCREEN
══════════════════════════════════ */
#setup {
  position: fixed; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% 0%, #1a0a2e 0%, #0e0e14 60%);
  z-index: 100;
}

.setup-glow {
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 600px; height: 300px;
  background: radial-gradient(ellipse, rgba(255,77,109,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.setup-logo {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 4rem;
  background: linear-gradient(135deg, #ff4d6d 0%, #ffd700 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  margin-bottom: 4px;
  filter: drop-shadow(0 0 40px rgba(255,77,109,0.4));
}

.setup-sub {
  color: var(--text3);
  font-size: 0.78rem;
  letter-spacing: 3px;
  margin-bottom: 36px;
  text-transform: uppercase;
}

.setup-card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: 32px;
  width: 380px;
  box-shadow: var(--shadow);
}

.form-row { margin-bottom: 18px; }
.form-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 7px;
}

.form-input, .form-select {
  width: 100%;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--r2);
  color: var(--text);
  padding: 11px 14px;
  font-size: 0.9rem;
  font-family: 'Noto Sans KR', sans-serif;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-input:focus, .form-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255,77,109,0.15);
}
.form-select option { background: #1e1e2a; }

.btn-start {
  width: 100%;
  background: linear-gradient(135deg, #ff4d6d, #c0392b);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.2rem;
  letter-spacing: 4px;
  padding: 16px;
  cursor: pointer;
  margin-top: 8px;
  transition: transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 6px 30px rgba(255,77,109,0.4);
}
.btn-start:hover { transform: translateY(-2px); box-shadow: 0 10px 40px rgba(255,77,109,0.55); }
.btn-start:active { transform: scale(0.97); }

.rules-mini {
  margin-top: 20px;
  background: var(--bg3);
  border-radius: var(--r2);
  padding: 12px 14px;
  font-size: 0.73rem;
  color: var(--text3);
  line-height: 1.85;
  border: 1px solid var(--border);
}
.rules-mini b { color: var(--text2); }

/* ══════════════════════════════════
   GAME LAYOUT
══════════════════════════════════ */
#game {
  display: none;
  width: 100vw;
  height: 100vh;
  flex-direction: row;
}

/* Board wrapper */
.board-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  min-width: 0;
  position: relative;
  background: radial-gradient(ellipse at center, #14142a 0%, #0a0a12 100%);
}

/* ══════════════════════════════════
   THE BOARD
══════════════════════════════════ */
#board {
  position: relative;
  background: #0a1520;
  border: 2px solid rgba(255,215,0,0.2);
  border-radius: 4px;
  box-shadow: 0 0 60px rgba(255,215,0,0.08), var(--shadow);
  aspect-ratio: 1;
  flex-shrink: 0;
}

.cell {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255,255,255,0.06);
  cursor: default;
  transition: background 0.15s;
  overflow: hidden;
  user-select: none;
}

.cell-name {
  font-size: 0;
  text-align: center;
  color: var(--text2);
  line-height: 1.2;
  font-weight: 500;
  white-space: nowrap;
}

.cell-price {
  color: var(--text3);
  text-align: center;
  font-weight: 400;
  font-size: 0;
}

.cell-icon {
  font-size: 0;
  line-height: 1;
  margin-bottom: 1px;
}

.color-bar {
  position: absolute;
  border-radius: 2px;
}

/* Side cells: bottom row (0-10), left col (10-20), top row (20-30), right col (30-40) */
/* Corner cells are bigger */

.cell-corner {
  background: #0f1a10;
}

/* Houses / hotel markers */
.house-dot {
  width: 5px; height: 5px;
  background: var(--green);
  border-radius: 1px;
  display: inline-block;
  margin: 0 0.5px;
}
.hotel-marker {
  width: 8px; height: 6px;
  background: var(--red);
  border-radius: 1px;
  display: inline-block;
}

.owner-badge {
  position: absolute;
  width: 5px; height: 5px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.5);
  top: 2px; right: 2px;
}

.mortgaged-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0;
  color: #ef4444;
  font-weight: 700;
  letter-spacing: 1px;
}

/* ── Player tokens on board ── */
.token-cluster {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 10;
  transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
}

.token {
  width: 16px; height: 16px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.8);
  display: flex; align-items: center; justify-content: center;
  font-size: 7px;
  font-weight: 900;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.6);
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}

/* ── Center board ── */
.board-center {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #080a18;
}

.board-title {
  font-family: 'Black Han Sans', sans-serif;
  background: linear-gradient(135deg, #ff4d6d, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  line-height: 1.1;
  letter-spacing: 2px;
}

.dice-center {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.die-face {
  background: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  color: #1a1a2e;
  box-shadow: 0 3px 12px rgba(0,0,0,0.5),
              inset 0 1px 2px rgba(255,255,255,0.7);
  transition: transform 0.1s;
}
.die-face.rolling { animation: diceRoll 0.6s ease-out; }
.die-face.double { box-shadow: 0 0 16px rgba(255,215,0,0.9), 0 3px 12px rgba(0,0,0,0.5); }

@keyframes diceRoll {
  0%   { transform: rotate(0deg) scale(1); }
  20%  { transform: rotate(-20deg) scale(1.15) translateY(-4px); }
  40%  { transform: rotate(15deg) scale(1.2) translateY(-8px); }
  60%  { transform: rotate(-8deg) scale(1.12) translateY(-3px); }
  80%  { transform: rotate(4deg) scale(1.04); }
  100% { transform: rotate(0deg) scale(1); }
}

/* ══════════════════════════════════
   SIDE PANEL
══════════════════════════════════ */
.side {
  width: 240px;
  background: var(--bg2);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}

.side-section {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.sec-label {
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

/* Players */
.player-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 4px;
  border-radius: 8px;
  transition: background 0.2s;
}
.player-item.active {
  background: rgba(255,77,109,0.1);
  margin: 0 -4px;
  padding: 6px 8px;
}
.player-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 8px currentColor;
}
.player-name-txt {
  flex: 1;
  font-size: 0.77rem;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.player-cash {
  font-size: 0.73rem;
  font-weight: 700;
  color: var(--green);
  font-variant-numeric: tabular-nums;
}
.player-bankrupt .player-name-txt { color: var(--text3); text-decoration: line-through; }
.player-bankrupt .player-cash { color: var(--text3); }
.jail-badge {
  font-size: 0.6rem;
  background: rgba(239,68,68,0.15);
  color: #ef4444;
  border-radius: 4px;
  padding: 1px 4px;
  flex-shrink: 0;
}

/* Actions */
.action-zone {
  flex: 1;
  padding: 12px 14px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}
.action-zone::-webkit-scrollbar { width: 3px; }
.action-zone::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.turn-banner {
  text-align: center;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 0;
  color: var(--text2);
}

.dice-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 6px 0;
}

.btn {
  border: none;
  border-radius: var(--r2);
  padding: 9px 14px;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
  width: 100%;
}
.btn:active:not(:disabled) { transform: scale(0.97); }
.btn:disabled { opacity: 0.3; cursor: not-allowed; }

.btn-red {
  background: linear-gradient(135deg, #ff4d6d, #c0392b);
  color: #fff;
  box-shadow: 0 3px 12px rgba(255,77,109,0.3);
}
.btn-red:hover:not(:disabled) { box-shadow: 0 5px 20px rgba(255,77,109,0.5); transform: translateY(-1px); }

.btn-green {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  box-shadow: 0 3px 10px rgba(34,197,94,0.3);
}
.btn-green:hover:not(:disabled) { box-shadow: 0 5px 16px rgba(34,197,94,0.5); transform: translateY(-1px); }

.btn-ghost {
  background: var(--bg3);
  color: var(--text2);
  border: 1px solid var(--border2);
}
.btn-ghost:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: var(--text); }

.btn-orange {
  background: linear-gradient(135deg, #f97316, #ea580c);
  color: #fff;
  box-shadow: 0 3px 10px rgba(249,115,22,0.3);
}
.btn-orange:hover:not(:disabled) { box-shadow: 0 5px 16px rgba(249,115,22,0.5); transform: translateY(-1px); }

.btn-row { display: flex; gap: 6px; }
.btn-row .btn { flex: 1; }

/* Card popup */
.card-box {
  background: linear-gradient(135deg, var(--bg3), var(--bg2));
  border: 1px solid rgba(255,215,0,0.25);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  animation: popIn 0.35s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes popIn {
  from { transform: scale(0.7) translateY(10px); opacity: 0; }
  to   { transform: scale(1) translateY(0);     opacity: 1; }
}
.card-emoji { font-size: 1.8rem; margin-bottom: 5px; }
.card-title { font-weight: 700; font-size: 0.85rem; color: #ffd700; margin-bottom: 3px; }
.card-effect { font-size: 0.72rem; color: #93c5fd; }

.info-box {
  background: rgba(59,130,246,0.08);
  border: 1px solid rgba(59,130,246,0.2);
  border-radius: var(--r2);
  padding: 8px 10px;
  font-size: 0.73rem;
  color: #93c5fd;
  text-align: center;
}

/* Property manager */
.mgr-toggle {
  width: 100%;
  background: none;
  border: 1px solid var(--border2);
  border-radius: 6px;
  color: var(--text3);
  font-size: 0.7rem;
  padding: 5px 10px;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
  text-align: left;
  transition: all 0.2s;
}
.mgr-toggle:hover { background: var(--bg3); color: var(--text2); }

.mgr-list { overflow: hidden; max-height: 0; transition: max-height 0.3s ease; }
.mgr-list.open { max-height: 250px; overflow-y: auto; }
.mgr-list::-webkit-scrollbar { width: 2px; }
.mgr-list::-webkit-scrollbar-thumb { background: var(--border2); }

.prop-row {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 2px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.68rem;
}
.prop-row:last-child { border: none; }
.prop-color { width: 6px; height: 6px; border-radius: 1px; flex-shrink: 0; }
.prop-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text2); }
.prop-name.mortgaged { color: #ef4444; opacity: 0.7; }
.prop-btns { display: flex; gap: 2px; flex-shrink: 0; }
.mini-b {
  padding: 2px 5px;
  font-size: 0.6rem;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  transition: all 0.12s;
}
.mini-b:disabled { opacity: 0.2; cursor: not-allowed; }
.mini-b:active:not(:disabled) { transform: scale(0.92); }
.mini-b-build { background: #22c55e; color: #fff; }
.mini-b-build:hover:not(:disabled) { background: #4ade80; }
.mini-b-mort { background: #ef4444; color: #fff; }
.mini-b-mort:hover:not(:disabled) { background: #f87171; }
.mini-b-unmort { background: #3b82f6; color: #fff; }
.mini-b-unmort:hover:not(:disabled) { background: #60a5fa; }

/* Log */
.log-wrap {
  padding: 0 14px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.log-inner {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}
.log-inner::-webkit-scrollbar { width: 3px; }
.log-inner::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.log-row {
  font-size: 0.65rem;
  padding: 2.5px 0;
  color: var(--text3);
  border-bottom: 1px solid rgba(255,255,255,0.025);
  line-height: 1.5;
}
.log-row:last-child { border: none; }
.log-gain { color: #4ade80; }
.log-lose { color: #f87171; }
.log-move { color: #60a5fa; }
.log-important { color: #fbbf24; font-weight: 700; }

/* ══════════════════════════════════
   BUTLER BUBBLE
══════════════════════════════════ */
#butler {
  position: absolute;
  bottom: 14px; left: 14px;
  background: rgba(8,8,20,0.96);
  border: 1px solid rgba(255,77,109,0.35);
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 200px;
  font-size: 0.72rem;
  line-height: 1.6;
  z-index: 30;
  pointer-events: none;
  animation: bubbleIn 0.25s ease;
  display: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}
@keyframes bubbleIn {
  from { transform: translateY(8px); opacity: 0; }
  to   { transform: translateY(0);   opacity: 1; }
}
.butler-head { color: var(--accent); font-weight: 700; font-size: 0.65rem; margin-bottom: 3px; }

/* ══════════════════════════════════
   GAME OVER
══════════════════════════════════ */
#gameover {
  display: none;
  position: fixed; inset: 0;
  background: rgba(5,5,14,0.97);
  z-index: 200;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  text-align: center;
}
.winner-crown { font-size: 3rem; animation: bounce 0.8s ease 0.2s both; }
@keyframes bounce {
  0%  { transform: translateY(-40px) scale(0.5); opacity: 0; }
  60% { transform: translateY(8px) scale(1.1); opacity: 1; }
  100%{ transform: translateY(0) scale(1); }
}
.winner-name {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 2.4rem;
  background: linear-gradient(135deg, #ffd700, #ff4d6d);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin: 8px 0;
  animation: winPop 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
}
@keyframes winPop {
  from { transform: scale(0.3); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
.winner-sub { font-size: 0.8rem; color: var(--text3); margin-bottom: 28px; letter-spacing: 2px; }

.rank-card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 16px;
  padding: 20px 28px;
  width: 100%; max-width: 340px;
  margin-bottom: 28px;
}
.rank-row {
  display: flex; align-items: center; gap: 14px;
  padding: 9px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.84rem;
}
.rank-row:last-child { border: none; }
.rank-medal { font-size: 1.3rem; min-width: 30px; }
.rank-player { flex: 1; font-weight: 700; }
.rank-money { color: var(--green); font-weight: 700; }
.rank-dead { color: var(--red); font-size: 0.72rem; }

/* Confetti */
.confetti-piece {
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  animation: confettiFall linear forwards;
}
@keyframes confettiFall {
  0%   { transform: translateY(-20px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(105vh) rotate(720deg); opacity: 0; }
}

/* Tooltip on cell hover */
.cell-tooltip {
  position: fixed;
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.73rem;
  z-index: 50;
  pointer-events: none;
  box-shadow: var(--shadow);
  min-width: 140px;
  display: none;
}
.tooltip-title { font-weight: 700; color: var(--text); margin-bottom: 4px; }
.tooltip-row { display: flex; justify-content: space-between; gap: 16px; color: var(--text3); font-size: 0.68rem; padding: 1.5px 0; }
.tooltip-row span:last-child { color: var(--text2); }

</style>
</head>
<body>

<!-- ════════ SETUP ════════ -->
<div id="setup">
  <div class="setup-glow"></div>
  <div class="setup-logo">부루마블</div>
  <div class="setup-sub">BURUMABL · BOARD GAME</div>
  <div class="setup-card">
    <div class="form-row">
      <label class="form-label">내 이름</label>
      <input class="form-input" id="inp-name" value="플레이어" maxlength="8">
    </div>
    <div class="form-row">
      <label class="form-label">봇 수</label>
      <select class="form-select" id="inp-bots">
        <option value="1">봇 1명 (2인)</option>
        <option value="2" selected>봇 2명 (3인)</option>
        <option value="3">봇 3명 (4인)</option>
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
    <button class="btn-start" onclick="startGame()">🎲 게임 시작</button>
    <div class="rules-mini">
      시작자금 <b>₩8,000</b> · 출발 통과 <b>+₩200</b><br>
      독점 시 임료 2배 · 집(4채) → 호텔<br>
      무인도 탈출: 더블 또는 보석금 <b>₩500</b><br>
      저당 50% 환급 · 해제 60% 납부
    </div>
  </div>
</div>

<!-- ════════ GAME ════════ -->
<div id="game">
  <div class="board-wrap">
    <div id="board"></div>
    <div id="butler">
      <div class="butler-head">🎩 집사</div>
      <span id="butler-text"></span>
    </div>
  </div>
  <div class="side">
    <div class="side-section">
      <div class="sec-label">플레이어</div>
      <div id="players-list"></div>
    </div>
    <div class="action-zone" id="action-zone"></div>
    <div class="log-wrap">
      <div class="sec-label" style="padding:8px 0 5px;flex-shrink:0">게임 로그</div>
      <div class="log-inner" id="log-area"></div>
    </div>
  </div>
</div>

<!-- ════════ GAME OVER ════════ -->
<div id="gameover">
  <div class="winner-crown">🏆</div>
  <div class="winner-name" id="winner-name"></div>
  <div class="winner-sub">최후의 승자!</div>
  <div class="rank-card" id="rank-list"></div>
  <button class="btn btn-red" style="max-width:240px;font-family:'Black Han Sans',sans-serif;font-size:1.1rem;letter-spacing:3px" onclick="resetGame()">🔄 다시 하기</button>
</div>

<!-- Tooltip -->
<div class="cell-tooltip" id="tooltip">
  <div class="tooltip-title" id="tt-title"></div>
  <div id="tt-body"></div>
</div>

<script>
// ════════════════════════════════════════════
//  CONSTANTS & DATA
// ════════════════════════════════════════════
const CELLS = [
  {name:"출발",    type:"go",     price:0,    rent:0,   group:-1, color:""},
  {name:"서울",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"부산",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"소득세",  type:"tax",    price:200,  rent:0,   group:-1, color:""},
  {name:"철도A",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"인천",    type:"prop",   price:800,  rent:80,  group:1,  color:"#9b59b6"},
  {name:"운명",    type:"fate",   price:0,    rent:0,   group:-1, color:""},
  {name:"대전",    type:"prop",   price:800,  rent:80,  group:1,  color:"#9b59b6"},
  {name:"제주",    type:"prop",   price:900,  rent:90,  group:1,  color:"#9b59b6"},
  {name:"여행",    type:"visit",  price:0,    rent:0,   group:-1, color:""},
  {name:"광주",    type:"prop",   price:1000, rent:100, group:2,  color:"#e67e22"},
  {name:"전기",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"울산",    type:"prop",   price:1000, rent:100, group:2,  color:"#e67e22"},
  {name:"대구",    type:"prop",   price:1100, rent:110, group:2,  color:"#e67e22"},
  {name:"철도B",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"수원",    type:"prop",   price:1200, rent:120, group:3,  color:"#e74c3c"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"고양",    type:"prop",   price:1300, rent:130, group:3,  color:"#e74c3c"},
  {name:"성남",    type:"prop",   price:1400, rent:140, group:3,  color:"#e74c3c"},
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
  {name:"파주",    type:"prop",   price:2200, rent:220, group:7,  color:"#f1c40f"},
  {name:"가스",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"김포",    type:"prop",   price:2200, rent:220, group:7,  color:"#f1c40f"},
  {name:"사치세",  type:"tax",    price:300,  rent:0,   group:-1, color:""},
];

const GRP_SIZE = {0:2,1:3,2:3,3:3,4:3,5:3,6:3,7:2};
const BUILD_COST = {0:200,1:250,2:300,3:350,4:350,5:400,6:400,7:500};
const RENT_MULT = [1,5,15,45,80];
const PCOLORS = ["#ff4d6d","#3b82f6","#22c55e","#f97316"];
const PTOKENS = ["▲","●","◆","★"];
const BOT_NAMES = ["알파봇","베타봇","감마봇"];
const DICE_FACES = ["⚀","⚁","⚂","⚃","⚄","⚅"];
const JAIL_BAIL = 500, START_MONEY = 8000, PASS_GO = 200;

const CHANCE_CARDS = [
  {emoji:"💰",text:"은행 배당금",      type:"money", amount:100},
  {emoji:"📋",text:"세금 환급",         type:"money", amount:150},
  {emoji:"🎂",text:"생일! 각자 50 받기",type:"birthday", amount:50},
  {emoji:"🔧",text:"수리비 청구",       type:"money", amount:-100},
  {emoji:"🏥",text:"의료비 청구",       type:"money", amount:-150},
  {emoji:"📚",text:"학교 수업료",       type:"money", amount:-200},
  {emoji:"📈",text:"투자 수익",         type:"money", amount:200},
  {emoji:"🚩",text:"출발로! +200",      type:"goto",  target:0},
  {emoji:"🔒",text:"무인도로!",         type:"goto_jail"},
  {emoji:"⬅️",text:"뒤로 3칸",         type:"move",  amount:-3},
  {emoji:"➡️",text:"앞으로 6칸",        type:"move",  amount:6},
  {emoji:"🚂",text:"가장 가까운 철도로",type:"nearest_rail"},
  {emoji:"🔨",text:"수리비: 집×40 호텔×115", type:"repair"},
  {emoji:"🏦",text:"은행 오류! +500",   type:"money", amount:500},
];

const FATE_CARDS = [
  {emoji:"🎫",text:"복권 당첨! +300",   type:"money", amount:300},
  {emoji:"🚦",text:"과태료 -50",         type:"money", amount:-50},
  {emoji:"💊",text:"보험금 수령 +100",   type:"money", amount:100},
  {emoji:"🚗",text:"수리비 -100",        type:"money", amount:-100},
  {emoji:"🎵",text:"콘서트 수익 +150",   type:"money", amount:150},
  {emoji:"✈️",text:"여행 경비 -100",     type:"money", amount:-100},
  {emoji:"🚩",text:"출발로! +200",       type:"goto",  target:0},
  {emoji:"🔒",text:"무인도로!",          type:"goto_jail"},
  {emoji:"➡️",text:"앞으로 3칸",         type:"move",  amount:3},
  {emoji:"🎂",text:"각자 50씩 받기",     type:"birthday", amount:50},
  {emoji:"💸",text:"탈세 적발 -200",     type:"money", amount:-200},
  {emoji:"🏦",text:"은행 이자 +200",     type:"money", amount:200},
];

const BUTLER = {
  buy:      ["마음에 드시는군요, 주인님!","투자하실 만합니다!","좋은 선택입니다!"],
  pass:     ["다음 기회를 기다리시는군요.","현명한 판단입니다.","때를 기다리십시오."],
  rent_in:  ["통행료 수령! 훌륭합니다!","수익이 들어왔습니다!","부동산이 일하는군요!"],
  rent_out: ["통행료를 납부하셨습니다...","아이고, 피하셔야 했는데.","다음엔 조심하십시오."],
  jail:     ["무인도로 가십니다...","잠시 구금되셨습니다.","곧 탈출하실 겁니다!"],
  double:   ["더블! 한 번 더 굴리세요!","행운이 따르는군요!","연속 이동 기회입니다!"],
  triple:   ["3연속 더블! 무인도입니다!","너무 과하셨습니다..."],
  build:    ["건설 완료! 수익이 오릅니다!","이제 통행료가 올라갑니다!","훌륭한 투자입니다!"],
  bankrupt: ["파산하셨습니다... 유감입니다.","다음엔 반드시 이기실 겁니다!"],
  win:      ["우승 축하드립니다, 주인님!","역시 주인님이십니다!","최고이십니다!"],
  go_pass:  ["출발 통과! +200 수령!","통과 보너스입니다, 주인님!"],
};

// ════════════════════════════════════════════
//  STATE
// ════════════════════════════════════════════
let G = null;
let mgrOpen = false;
let butlerTmr = null;
let animating = false;
let boardSize = 560;

function newCells() {
  return CELLS.map(c => ({...c, owner:null, houses:0, mortgaged:false}));
}

function initGame(name, bots, diff) {
  const players = [{
    name, money:START_MONEY, pos:0,
    color:PCOLORS[0], token:PTOKENS[0],
    is_bot:false, bankrupt:false, jail_turns:0
  }];
  for (let i = 0; i < bots; i++) {
    players.push({
      name:BOT_NAMES[i], money:START_MONEY, pos:0,
      color:PCOLORS[i+1], token:PTOKENS[i+1],
      is_bot:true, bankrupt:false, jail_turns:0
    });
  }
  return { players, cells:newCells(), turn:0, doubles:0,
           phase:'roll', log:[], diff,
           pending_card:null, winner:null, d1:1, d2:1 };
}

// ════════════════════════════════════════════
//  BUTLER
// ════════════════════════════════════════════
function butler(key) {
  const msgs = BUTLER[key] || ["..."];
  const msg = msgs[Math.floor(Math.random() * msgs.length)];
  const el = document.getElementById('butler');
  const txt = document.getElementById('butler-text');
  txt.textContent = msg;
  el.style.display = 'block';
  if (butlerTmr) clearTimeout(butlerTmr);
  butlerTmr = setTimeout(() => el.style.display = 'none', 3200);
}

// ════════════════════════════════════════════
//  GAME LOGIC
// ════════════════════════════════════════════
function log(msg, style='') {
  G.log.unshift({msg, style});
  if (G.log.length > 100) G.log.length = 100;
}

function alive() { return G.players.filter(p => !p.bankrupt); }

function checkWin() {
  const a = alive();
  if (a.length === 1) { G.winner = a[0].name; G.phase = 'gameover'; return true; }
  return false;
}

function ownsGroup(pidx, grp) {
  if (grp < 0) return false;
  const total = GRP_SIZE[grp] || 0;
  return G.cells.filter(c => c.group === grp && c.owner === pidx).length === total;
}

function calcRent(ci, roll) {
  const c = G.cells[ci];
  if (c.owner === null || c.mortgaged) return 0;
  const {type, owner, houses, rent, group} = c;
  if (type === 'prop') {
    const h = Math.min(houses, 4);
    if (h === 0 && ownsGroup(owner, group)) return rent * 2;
    return rent * RENT_MULT[h];
  }
  if (type === 'rail') {
    const n = G.cells.filter(c2 => c2.type === 'rail' && c2.owner === owner).length;
    return 100 * n;
  }
  if (type === 'util') {
    const n = G.cells.filter(c2 => c2.type === 'util' && c2.owner === owner).length;
    const r = roll || (Math.floor(Math.random()*11)+2);
    return r * (n === 1 ? 4 : 10);
  }
  return 0;
}

function nearestRail(pos) {
  const rails = [5,15,25,35];
  return rails.reduce((b,r) => ((r-pos+40)%40) < ((b-pos+40)%40) ? r : b);
}

function movePlayer(pidx, steps) {
  const p = G.players[pidx];
  const old = p.pos;
  const nw = ((old + steps) % 40 + 40) % 40;
  if (steps > 0 && nw < old) {
    p.money += PASS_GO;
    log(`🚩 ${p.name} 출발 통과! +${PASS_GO}`, 'gain');
    butler('go_pass');
  }
  p.pos = nw;
}

function sendJail(pidx) {
  const p = G.players[pidx];
  p.pos = 20; p.jail_turns = 3;
  log(`🔒 ${p.name} 무인도!`, 'lose');
  butler('jail');
}

function payRent(from, to, amt) {
  const payer = G.players[from], recv = G.players[to];
  const actual = Math.min(amt, Math.max(0, payer.money));
  payer.money -= actual; recv.money += actual;
  log(`💸 ${payer.name}→${recv.name}: 임료 ${actual}`, 'lose');
  butler(from === 0 ? 'rent_out' : 'rent_in');
  checkBankrupt(from);
}

function checkBankrupt(pidx) {
  const p = G.players[pidx];
  if (p.money >= 0) return;
  // 긴급 저당
  for (let ci = 0; ci < G.cells.length; ci++) {
    const c = G.cells[ci];
    if (c.owner === pidx && !c.mortgaged && c.houses === 0 && p.money < 0) {
      const val = Math.floor(c.price * 0.5);
      c.mortgaged = true; p.money += val;
      log(`📋 ${p.name} ${c.name} 긴급저당 +${val}`, 'lose');
    }
  }
  if (p.money < 0) {
    p.bankrupt = true; p.money = 0;
    G.cells.forEach(c => { if (c.owner === pidx) { c.owner=null; c.houses=0; c.mortgaged=false; } });
    log(`💀 ${p.name} 파산!`, 'important');
    butler('bankrupt');
    checkWin();
  }
}

function doMortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner !== pidx || c.mortgaged || c.houses > 0) return;
  const val = Math.floor(c.price * 0.5);
  c.mortgaged = true; p.money += val;
  log(`📋 ${p.name} ${c.name} 저당 +${val}`, 'lose');
  renderAll();
}

function doUnmortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner !== pidx || !c.mortgaged) return;
  const cost = Math.floor(c.price * 0.6);
  if (p.money < cost) return;
  c.mortgaged = false; p.money -= cost;
  log(`✅ ${p.name} ${c.name} 저당해제 -${cost}`);
  renderAll();
}

function doBuild(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  const cost = BUILD_COST[c.group] || 300;
  if (p.money < cost || c.houses >= 4 || c.mortgaged) return;
  c.houses++; p.money -= cost;
  const lbl = c.houses === 4 ? '호텔🏨' : `집 ${c.houses}채`;
  log(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
  butler('build');
  renderAll();
}

function applyCard(pidx, card) {
  const p = G.players[pidx];
  const {type, amount, target, text} = card;
  if (type === 'money') {
    p.money += amount;
    log(`🃏 ${p.name}: ${text} (${amount>0?'+':''}${amount})`, amount>0?'gain':'lose');
    if (amount < 0) checkBankrupt(pidx);
  } else if (type === 'birthday') {
    G.players.forEach((o, i) => {
      if (i !== pidx && !o.bankrupt) {
        const a = Math.min(amount, Math.max(0, o.money));
        o.money -= a; p.money += a;
      }
    });
    log(`🎂 ${p.name} 생일! 각자 ${amount}`, 'gain');
  } else if (type === 'goto') {
    if (target === 0) p.money += PASS_GO;
    p.pos = target;
    log(`🚀 ${p.name} → ${CELLS[target].name}`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'goto_jail') {
    sendJail(pidx);
  } else if (type === 'move') {
    movePlayer(pidx, amount);
    log(`👣 ${p.name} ${amount>0?'+':''}${amount}칸`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'nearest_rail') {
    const nr = nearestRail(p.pos);
    const steps = ((nr - p.pos + 40) % 40) || 40;
    movePlayer(pidx, steps);
    log(`🚂 ${p.name} 철도로!`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'repair') {
    const h = G.cells.filter(c => c.owner===pidx && c.houses>0 && c.houses<4).length;
    const ht = G.cells.filter(c => c.owner===pidx && c.houses===4).length;
    const cost = h*40 + ht*115;
    p.money -= cost;
    log(`🔧 ${p.name} 수리비 -${cost}`, 'lose');
    checkBankrupt(pidx);
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

function landCell(pidx, roll) {
  const p = G.players[pidx];
  const ci = p.pos;
  const c = G.cells[ci];
  log(`📍 ${p.name} → ${c.name}`, 'move');
  if (c.type === 'go') {
    p.money += PASS_GO;
    log(`🎉 출발 착지! +${PASS_GO}`, 'gain');
  } else if (['prop','rail','util'].includes(c.type)) {
    if (c.owner === null) { G.phase = 'buy'; return; }
    else if (c.owner === pidx) { log('🏠 자기 소유지'); }
    else {
      if (c.mortgaged) log(`📋 ${c.name} 저당 중`);
      else { const rent = calcRent(ci, roll); payRent(pidx, c.owner, rent); }
    }
    checkWin();
  } else if (c.type === 'chance' || c.type === 'fate') {
    const pool = c.type === 'chance' ? CHANCE_CARDS : FATE_CARDS;
    G.pending_card = pool[Math.floor(Math.random() * pool.length)];
    G.phase = 'card';
    return;
  } else if (c.type === 'tax') {
    p.money -= c.price;
    log(`💸 ${p.name} 세금 -${c.price}`, 'lose');
    checkBankrupt(pidx);
  } else if (c.type === 'jail') {
    sendJail(pidx);
  } else {
    log(`✅ ${c.name}`);
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

function nextTurn() {
  if (G.phase === 'gameover') return;
  const n = G.players.length;
  let nxt = (G.turn + 1) % n, att = 0;
  while (G.players[nxt].bankrupt && att < n) { nxt = (nxt+1)%n; att++; }
  G.turn = nxt; G.phase = 'roll';
}

// ════════════════════════════════════════════
//  ANIMATIONS
// ════════════════════════════════════════════
function rollDice() {
  const d1 = Math.floor(Math.random()*6)+1;
  const d2 = Math.floor(Math.random()*6)+1;
  return { d1, d2, total:d1+d2, isDouble:d1===d2 };
}

function animateDice(d1, d2, cb) {
  const el1 = document.getElementById('die1');
  const el2 = document.getElementById('die2');
  if (!el1 || !el2) { cb && cb(); return; }
  el1.classList.add('rolling'); el2.classList.add('rolling');
  el1.classList.remove('double'); el2.classList.remove('double');
  let n = 0;
  const iv = setInterval(() => {
    el1.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    el2.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    n++;
    if (n >= 12) {
      clearInterval(iv);
      el1.textContent = DICE_FACES[d1-1];
      el2.textContent = DICE_FACES[d2-1];
      el1.classList.remove('rolling'); el2.classList.remove('rolling');
      if (d1 === d2) { el1.classList.add('double'); el2.classList.add('double'); }
      cb && cb();
    }
  }, 60);
}

function animateMove(pidx, from, to, cb) {
  if (from === to) { cb && cb(); return; }
  const steps = [];
  let cur = from;
  while (cur !== to) { cur = (cur+1)%40; steps.push(cur); }
  let i = 0;
  const iv = setInterval(() => {
    G.players[pidx].pos = steps[i];
    renderTokens();
    i++;
    if (i >= steps.length) { clearInterval(iv); cb && cb(); }
  }, 120);
}

// ════════════════════════════════════════════
//  PLAYER ACTIONS
// ════════════════════════════════════════════
function doRoll() {
  if (!G || animating) return;
  animating = true;
  const {d1, d2, total, isDouble} = rollDice();
  G.d1 = d1; G.d2 = d2;
  renderDiceCenter();
  animateDice(d1, d2, () => {
    if (isDouble) {
      G.doubles++;
      if (G.doubles >= 3) {
        log(`3연속 더블! ${G.players[G.turn].name} 무인도!`, 'important');
        butler('triple');
        sendJail(G.turn); G.doubles = 0;
        nextTurn(); animating = false; renderAll();
        setTimeout(checkBotTurn, 500); return;
      }
      log(`🎲 더블! (${d1}+${d2})`);
      butler('double');
    } else {
      G.doubles = 0;
      log(`🎲 ${d1}+${d2}=${total}`);
    }
    const from = G.players[G.turn].pos;
    renderAll();
    setTimeout(() => {
      animateMove(G.turn, from, (from+total)%40, () => {
        movePlayer(G.turn, total);
        landCell(G.turn, total);
        animating = false;
        if (!isDouble && G.phase !== 'buy' && G.phase !== 'card' && G.phase !== 'gameover')
          nextTurn();
        renderAll();
        if (G.phase === 'gameover') showGameOver();
      });
    }, 200);
  });
}

function doBuy(buy) {
  const pidx = G.turn, ci = G.players[pidx].pos, cell = G.cells[ci];
  if (buy) {
    cell.owner = pidx; G.players[pidx].money -= cell.price;
    log(`🏠 ${G.players[pidx].name} ${cell.name} 매입 -${cell.price}`, 'lose');
    butler('buy');
  } else {
    log(`↩️ ${G.players[pidx].name} ${cell.name} 패스`);
    butler('pass');
  }
  G.phase = 'roll'; nextTurn(); renderAll();
  setTimeout(checkBotTurn, 400);
}

function doCard() {
  if (!G || !G.pending_card) return;
  applyCard(G.turn, G.pending_card);
  G.pending_card = null;
  if (G.phase !== 'gameover') { nextTurn(); renderAll(); setTimeout(checkBotTurn, 400); }
  else { renderAll(); showGameOver(); }
}

function doJail(payBail) {
  if (!G) return;
  const p = G.players[G.turn];
  if (payBail) {
    if (p.money < JAIL_BAIL) return;
    p.money -= JAIL_BAIL; p.jail_turns = 0;
    log(`💰 ${p.name} 보석금 납부!`, 'lose');
    renderAll();
    setTimeout(doRoll, 300);
  } else {
    if (animating) return;
    animating = true;
    const {d1, d2, total, isDouble} = rollDice();
    G.d1 = d1; G.d2 = d2;
    renderDiceCenter();
    animateDice(d1, d2, () => {
      if (isDouble) {
        p.jail_turns = 0;
        log(`🎉 더블 탈출!`);
        animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
          movePlayer(G.turn, total); landCell(G.turn, total);
          if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover') nextTurn();
          animating = false; renderAll();
          if (G.phase==='gameover') showGameOver();
          else setTimeout(checkBotTurn, 500);
        });
      } else {
        p.jail_turns--;
        log(`😔 더블 실패 (${p.jail_turns}턴 남음)`);
        if (p.jail_turns <= 0) {
          p.jail_turns = 0;
          animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
            movePlayer(G.turn, total); landCell(G.turn, total);
            if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover') nextTurn();
            animating = false; renderAll();
            if (G.phase==='gameover') showGameOver();
            else setTimeout(checkBotTurn, 500);
          });
        } else {
          nextTurn(); animating = false; renderAll(); setTimeout(checkBotTurn, 400);
        }
      }
    });
  }
}

// ════════════════════════════════════════════
//  BOT AI
// ════════════════════════════════════════════
function checkBotTurn() {
  if (!G || G.phase === 'gameover') return;
  const p = G.players[G.turn];
  if (p.is_bot && !p.bankrupt) doBotTurn();
}

function doBotTurn() {
  setTimeout(() => {
    if (!G || G.phase === 'gameover') return;
    const pidx = G.turn, p = G.players[pidx];
    if (!p.is_bot || p.bankrupt) return;

    if (p.jail_turns > 0 && G.phase === 'roll') {
      if (G.diff === 'hard' && p.money >= JAIL_BAIL) {
        p.money -= JAIL_BAIL; p.jail_turns = 0;
        log(`💰 ${p.name} 보석금!`, 'lose');
        renderAll();
        setTimeout(() => doBotRoll(pidx), 400);
      } else {
        const {d1,d2,total,isDouble} = rollDice();
        G.d1=d1; G.d2=d2;
        if (isDouble) {
          p.jail_turns = 0; log(`🎉 ${p.name} 더블 탈출!`);
          renderAll();
          animateMove(pidx, p.pos, (p.pos+total)%40, () => {
            movePlayer(pidx, total); landCell(pidx, total);
            botDecide(pidx);
            if (G.phase!=='gameover') nextTurn();
            renderAll();
            G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 500);
          });
        } else {
          p.jail_turns--;
          log(`😔 ${p.name} 더블 실패`);
          if (p.jail_turns <= 0) {
            p.jail_turns = 0; renderAll();
            animateMove(pidx, p.pos, (p.pos+total)%40, () => {
              movePlayer(pidx, total); landCell(pidx, total);
              botDecide(pidx);
              if (G.phase!=='gameover') nextTurn();
              renderAll();
              G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 500);
            });
          } else {
            nextTurn(); renderAll(); setTimeout(checkBotTurn, 400);
          }
        }
      }
      return;
    }

    if (G.phase === 'buy' || G.phase === 'card') {
      botDecide(pidx);
      if (G.phase !== 'gameover') nextTurn();
      renderAll();
      G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 400);
      return;
    }

    if (G.phase === 'roll') {
      botBuild(pidx);
      doBotRoll(pidx);
    }
  }, 600);
}

function doBotRoll(pidx) {
  if (!G || G.phase === 'gameover') return;
  const p = G.players[pidx];
  const {d1, d2, total, isDouble} = rollDice();
  G.d1 = d1; G.d2 = d2;
  if (isDouble) {
    G.doubles++;
    if (G.doubles >= 3) {
      log(`3연속 더블! ${p.name} 무인도!`, 'important');
      butler('triple');
      sendJail(pidx); G.doubles = 0;
      nextTurn(); renderAll(); setTimeout(checkBotTurn, 500); return;
    }
    log(`🎲 ${p.name} 더블! (${d1}+${d2})`);
  } else {
    G.doubles = 0;
    log(`🎲 ${p.name} ${d1}+${d2}=${total}`);
  }
  renderAll();
  const from = p.pos;
  setTimeout(() => {
    animateMove(pidx, from, (from+total)%40, () => {
      movePlayer(pidx, total); landCell(pidx, total);
      botDecide(pidx);
      if (!isDouble && G.phase !== 'gameover') nextTurn();
      renderAll();
      if (G.phase === 'gameover') showGameOver();
      else if (isDouble && G.phase === 'roll') setTimeout(() => doBotRoll(pidx), 700);
      else setTimeout(checkBotTurn, 500);
    });
  }, 200);
}

function botDecide(pidx) {
  const p = G.players[pidx], diff = G.diff;
  if (G.phase === 'buy') {
    const ci = p.pos, cell = G.cells[ci], price = cell.price;
    let buy = false;
    if (diff === 'easy') buy = Math.random() > 0.35 && p.money >= price;
    else if (diff === 'normal') buy = p.money >= price * 1.5;
    else {
      const g = cell.group;
      if (g >= 0) {
        const have = G.cells.filter(c => c.group===g && c.owner===pidx).length;
        if (have === (GRP_SIZE[g]||0) - 1 && p.money >= price) buy = true;
        else buy = p.money >= price * 1.2;
      } else buy = p.money >= price;
    }
    if (buy) {
      cell.owner = pidx; p.money -= price;
      log(`🏠 ${p.name} ${cell.name} 매입 -${price}`, 'lose');
    } else {
      log(`↩️ ${p.name} ${cell.name} 패스`);
    }
    G.phase = 'roll';
  } else if (G.phase === 'card' && G.pending_card) {
    applyCard(pidx, G.pending_card);
    G.pending_card = null;
  }
}

function botBuild(pidx) {
  if (G.diff !== 'hard') return;
  const p = G.players[pidx];
  G.cells.forEach((c, ci) => {
    if (c.owner !== pidx || c.type !== 'prop') return;
    if (!ownsGroup(pidx, c.group) || c.houses >= 4 || c.mortgaged) return;
    const cost = BUILD_COST[c.group] || 300;
    if (p.money >= cost * 1.3) {
      c.houses++; p.money -= cost;
      const lbl = c.houses===4 ? '호텔' : `집${c.houses}`;
      log(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
      butler('build');
    }
  });
}

// ════════════════════════════════════════════
//  BOARD LAYOUT CALCULATIONS
// ════════════════════════════════════════════
// Board: 11×11 grid. Corners are bigger.
// CORNER size = S/11 * 1.5, side cells = (S - 2*C) / 9

function getBoardSize() {
  const bw = document.getElementById('board');
  return bw ? bw.offsetWidth : 560;
}

function getCellRect(ci) {
  const S = boardSize;
  const C = S / 7.5; // corner size
  const W = (S - 2*C) / 9; // non-corner cell width
  const H = C;

  if (ci === 0)  return {x: S-C,    y: S-C,    w: C, h: C};
  if (ci === 10) return {x: 0,      y: S-C,    w: C, h: C};
  if (ci === 20) return {x: 0,      y: 0,      w: C, h: C};
  if (ci === 30) return {x: S-C,    y: 0,      w: C, h: C};

  if (ci < 10) {
    const idx = 10 - ci;
    return {x: S-C-idx*W, y: S-C, w: W, h: H};
  }
  if (ci < 20) {
    const idx = ci - 10;
    return {x: 0, y: S-C-idx*W, w: H, h: W};
  }
  if (ci < 30) {
    const idx = ci - 20;
    return {x: C+(idx-1)*W, y: 0, w: W, h: H};
  }
  // 30-39
  const idx = ci - 30;
  return {x: S-C, y: C+(idx-1)*W, w: H, h: W};
}

// ════════════════════════════════════════════
//  BUILD BOARD DOM
// ════════════════════════════════════════════
function buildBoard() {
  const boardEl = document.getElementById('board');
  const S = boardSize;
  boardEl.style.width  = S + 'px';
  boardEl.style.height = S + 'px';
  boardEl.innerHTML = '';

  const C = S / 7.5;
  const W = (S - 2*C) / 9;
  const fs = Math.max(6, Math.round(S / 80));

  // Create cells
  for (let ci = 0; ci < 40; ci++) {
    const {x, y, w, h} = getCellRect(ci);
    const cellData = G.cells[ci];
    const isCorner = ci===0||ci===10||ci===20||ci===30;
    const isSide10  = ci < 10 || ci >= 30; // horizontal
    const isSide20  = ci >= 10 && ci < 20; // left vertical
    const isSide30  = ci >= 20 && ci < 30; // top horizontal

    const div = document.createElement('div');
    div.className = 'cell' + (isCorner ? ' cell-corner' : '');
    div.id = 'cell-' + ci;
    div.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;

    // Background per type
    const bg = {
      go:'#0a2015', jail:'#1a0a2e', visit:'#0a1828',
      free:'#0a1a0a', chance:'#1a1028', fate:'#280a0a',
      tax:'#28180a', rail:'#0a1428', util:'#0a2010',
      prop:'#0d1020'
    }[cellData.type] || '#0d1020';
    div.style.background = bg;

    // Color bar for properties
    if (cellData.color && cellData.type === 'prop') {
      const bar = document.createElement('div');
      bar.className = 'color-bar';
      bar.id = 'bar-' + ci;
      bar.style.background = cellData.color;
      const bThick = Math.round(h * 0.18);
      if (ci < 10 || ci >= 30) {
        bar.style.cssText = `top:0;left:0;width:100%;height:${bThick}px;border-radius:0;`;
      } else if (ci >= 10 && ci < 20) {
        bar.style.cssText = `top:0;right:0;width:${bThick}px;height:100%;border-radius:0;`;
      } else if (ci >= 20 && ci < 30) {
        bar.style.cssText = `bottom:0;left:0;width:100%;height:${bThick}px;border-radius:0;`;
      }
      div.appendChild(bar);
    }

    // Rail bar
    if (cellData.type === 'rail') {
      const bar = document.createElement('div');
      bar.style.cssText = `position:absolute;background:#1c3a5a;opacity:0.9;border-radius:0;`;
      if (ci < 10 || ci >= 30) {
        bar.style.cssText += `top:0;left:0;width:100%;height:${Math.round(h*0.18)}px;`;
      } else {
        bar.style.cssText += `top:0;right:0;width:${Math.round(w*0.18)}px;height:100%;`;
      }
      div.appendChild(bar);
    }

    // Text container
    const textWrap = document.createElement('div');
    textWrap.id = 'tw-' + ci;
    textWrap.style.cssText = `position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;gap:1px;z-index:1;`;

    // Icon
    const iconMap = {
      go:'🚩', jail:'🔒', visit:'✈️', free:'🅿️', chance:'?', fate:'★', tax:'💸', rail:'🚂'
    };
    let icon = iconMap[cellData.type] || '';
    if (cellData.type === 'util') icon = cellData.name==='전기'?'⚡':'🔥';

    if (icon) {
      const iconEl = document.createElement('div');
      iconEl.className = 'cell-icon';
      iconEl.textContent = icon;
      iconEl.style.fontSize = Math.round(fs * 1.3) + 'px';
      textWrap.appendChild(iconEl);
    }

    const nameEl = document.createElement('div');
    nameEl.className = 'cell-name';
    nameEl.id = 'cn-' + ci;
    const shortName = cellData.name.length > 3 ? cellData.name.slice(0,3) : cellData.name;
    nameEl.textContent = isCorner ? cellData.name : shortName;
    nameEl.style.fontSize = (isCorner ? fs+1 : fs) + 'px';
    textWrap.appendChild(nameEl);

    if (cellData.price > 0 && !isCorner) {
      const priceEl = document.createElement('div');
      priceEl.className = 'cell-price';
      priceEl.textContent = cellData.price.toLocaleString();
      priceEl.style.fontSize = Math.max(5, fs-1) + 'px';
      textWrap.appendChild(priceEl);
    }

    div.appendChild(textWrap);

    // House indicators
    const housesEl = document.createElement('div');
    housesEl.id = 'houses-' + ci;
    housesEl.style.cssText = `position:absolute;display:flex;gap:1px;align-items:center;z-index:2;`;
    if (ci < 10 || ci >= 30) {
      housesEl.style.bottom = '2px';
      housesEl.style.left = '50%';
      housesEl.style.transform = 'translateX(-50%)';
    } else {
      housesEl.style.left = '2px';
      housesEl.style.top = '50%';
      housesEl.style.flexDirection = 'column';
      housesEl.style.transform = 'translateY(-50%)';
    }
    div.appendChild(housesEl);

    // Owner badge
    const badge = document.createElement('div');
    badge.className = 'owner-badge';
    badge.id = 'ob-' + ci;
    badge.style.display = 'none';
    div.appendChild(badge);

    // Mortgaged overlay
    const mort = document.createElement('div');
    mort.className = 'mortgaged-overlay';
    mort.id = 'mo-' + ci;
    mort.textContent = '저당';
    mort.style.cssText += `font-size:${Math.max(6,fs-1)}px;display:none;`;
    div.appendChild(mort);

    div.addEventListener('mouseenter', (e) => showTooltip(ci, e));
    div.addEventListener('mouseleave', hideTooltip);
    boardEl.appendChild(div);
  }

  // Center area
  const C2 = C;
  const center = document.createElement('div');
  center.className = 'board-center';
  center.style.cssText = `left:${C2}px;top:${C2}px;width:${S-2*C2}px;height:${S-2*C2}px;`;
  center.innerHTML = `
    <div class="board-title" style="font-size:${Math.round(S/14)}px;">부루마블</div>
    <div style="font-size:${Math.round(S/80)}px;color:#333;letter-spacing:2px;margin-bottom:8px;">BOARD GAME</div>
    <div class="dice-center">
      <div class="die-face" id="die1" style="width:${Math.round(S/12)}px;height:${Math.round(S/12)}px;">⚀</div>
      <div class="die-face" id="die2" style="width:${Math.round(S/12)}px;height:${Math.round(S/12)}px;">⚁</div>
    </div>
  `;
  boardEl.appendChild(center);

  // Token clusters
  for (let ci = 0; ci < 40; ci++) {
    const {x, y, w, h} = getCellRect(ci);
    const cluster = document.createElement('div');
    cluster.className = 'token-cluster';
    cluster.id = 'tc-' + ci;
    cluster.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;
    boardEl.appendChild(cluster);
  }
}

// ════════════════════════════════════════════
//  RENDER FUNCTIONS
// ════════════════════════════════════════════
function renderBoard() {
  if (!G) return;
  const S = boardSize;
  const FS = Math.max(6, Math.round(S / 80));

  G.cells.forEach((c, ci) => {
    // Houses
    const housesEl = document.getElementById('houses-' + ci);
    if (housesEl) {
      housesEl.innerHTML = '';
      if (c.type === 'prop' && c.houses > 0 && !c.mortgaged) {
        if (c.houses === 4) {
          const h = document.createElement('div');
          h.className = 'hotel-marker';
          h.style.width = Math.round(FS*1.4) + 'px';
          h.style.height = Math.round(FS*1.0) + 'px';
          housesEl.appendChild(h);
        } else {
          for (let i = 0; i < c.houses; i++) {
            const hd = document.createElement('div');
            hd.className = 'house-dot';
            hd.style.width = hd.style.height = Math.round(FS*0.8) + 'px';
            housesEl.appendChild(hd);
          }
        }
      }
    }

    // Owner badge
    const ob = document.getElementById('ob-' + ci);
    if (ob) {
      if (c.owner !== null && !c.mortgaged) {
        ob.style.display = 'block';
        ob.style.background = G.players[c.owner].color;
        ob.style.boxShadow = `0 0 6px ${G.players[c.owner].color}80`;
      } else {
        ob.style.display = 'none';
      }
    }

    // Mortgaged
    const mo = document.getElementById('mo-' + ci);
    if (mo) mo.style.display = c.mortgaged ? 'flex' : 'none';
  });
}

function renderDiceCenter() {
  const el1 = document.getElementById('die1');
  const el2 = document.getElementById('die2');
  if (el1) el1.textContent = DICE_FACES[(G.d1||1)-1];
  if (el2) el2.textContent = DICE_FACES[(G.d2||1)-1];
}

function renderTokens() {
  for (let ci = 0; ci < 40; ci++) {
    const tc = document.getElementById('tc-' + ci);
    if (!tc) continue;
    tc.innerHTML = '';
  }
  const slotMap = {};
  G.players.forEach((p, pi) => {
    if (p.bankrupt) return;
    const slot = slotMap[p.pos] || 0;
    slotMap[p.pos] = slot + 1;
    const tc = document.getElementById('tc-' + p.pos);
    if (!tc) return;
    const tk = document.createElement('div');
    tk.className = 'token';
    const tSize = Math.max(12, Math.round(boardSize / 38));
    tk.style.cssText = `width:${tSize}px;height:${tSize}px;background:${p.color};font-size:${Math.round(tSize*0.45)}px;`;
    tk.textContent = p.token;
    tc.appendChild(tk);
  });
}

function renderPlayers() {
  const el = document.getElementById('players-list');
  if (!el) return;
  el.innerHTML = G.players.map((p, i) => {
    const isAct = i === G.turn && !p.bankrupt;
    if (p.bankrupt) return `
      <div class="player-item player-bankrupt">
        <div class="player-dot" style="background:${p.color};opacity:0.2"></div>
        <span class="player-name-txt" style="color:#444">${p.token} ${p.name}</span>
        <span style="font-size:0.65rem;color:#ef4444">💀파산</span>
      </div>`;
    const jailTxt = p.jail_turns > 0 ? `<span class="jail-badge">🔒${p.jail_turns}</span>` : '';
    return `
      <div class="player-item${isAct?' active':''}">
        <div class="player-dot" style="background:${p.color};color:${p.color}"></div>
        <span class="player-name-txt" style="color:${p.color}">${p.token} ${p.name}${p.is_bot?' 🤖':''}</span>
        <span class="player-cash">₩${p.money.toLocaleString()}</span>
        ${jailTxt}
      </div>`;
  }).join('');
}

function renderAction() {
  const az = document.getElementById('action-zone');
  if (!az || !G) return;
  const pidx = G.turn, p = G.players[pidx], phase = G.phase;
  const diceFS = Math.round(boardSize / 18);

  let html = `<div class="turn-banner" style="color:${p.color}">${p.token} ${p.name}${p.is_bot?' 🤖':''} 차례</div>`;
  html += `
    <div class="dice-row">
      <div style="width:40px;height:40px;background:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#1a1a2e;box-shadow:0 3px 12px rgba(0,0,0,0.5);">${DICE_FACES[(G.d1||1)-1]}</div>
      <div style="width:40px;height:40px;background:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#1a1a2e;box-shadow:0 3px 12px rgba(0,0,0,0.5);">${DICE_FACES[(G.d2||1)-1]}</div>
    </div>`;

  if (p.is_bot) {
    html += `<div style="text-align:center;font-size:0.7rem;color:var(--text3);padding:8px">⚙️ 봇 처리 중...</div>`;
    az.innerHTML = html; return;
  }
  if (p.bankrupt) { az.innerHTML = html; return; }

  if (p.jail_turns > 0 && phase === 'roll') {
    html += `<div class="info-box">🔒 무인도 구금 중 (${p.jail_turns}턴 남음)</div>`;
    html += `<div class="btn-row">
      <button class="btn btn-orange" onclick="doJail(true)" ${p.money<JAIL_BAIL?'disabled':''}>💰 보석 (${JAIL_BAIL})</button>
      <button class="btn btn-red" onclick="doJail(false)">🎲 더블 도전</button>
    </div>`;
  } else if (phase === 'roll') {
    html += `<button class="btn btn-red" onclick="doRoll()" ${animating?'disabled':''}>🎲 주사위 굴리기</button>`;
    html += `<button class="mgr-toggle" onclick="toggleMgr()">
      ${mgrOpen?'▲':'▼'} 🏗️ 부동산 관리
    </button>
    <div class="mgr-list${mgrOpen?' open':''}" id="mgr-list"></div>`;
  } else if (phase === 'buy') {
    const ci = p.pos, cell = G.cells[ci];
    const ico = cell.type==='prop'?'🏠':cell.type==='rail'?'🚂':'⚡';
    html += `<div class="card-box">
      <div class="card-emoji">${ico}</div>
      <div class="card-title">${cell.name}</div>
      <div class="card-effect">매입가 ₩${cell.price.toLocaleString()} · 기본임료 ₩${cell.rent}</div>
    </div>
    <button class="btn btn-green" onclick="doBuy(true)" ${p.money<cell.price?'disabled':''}>✅ 매입 (-₩${cell.price.toLocaleString()})</button>
    <button class="btn btn-ghost" onclick="doBuy(false)">↩️ 패스</button>`;
  } else if (phase === 'card' && G.pending_card) {
    const card = G.pending_card;
    const amtHtml = card.amount !== undefined
      ? `<span style="color:${card.amount>0?'#4ade80':'#f87171'}">${card.amount>0?'+':''}${card.amount}</span>` : '';
    html += `<div class="card-box">
      <div class="card-emoji">${card.emoji}</div>
      <div class="card-title">${card.text}</div>
      <div class="card-effect">${amtHtml}</div>
    </div>
    <button class="btn btn-red" onclick="doCard()">확인</button>`;
  }

  az.innerHTML = html;
  if (phase === 'roll' && mgrOpen) renderMgr();
}

function toggleMgr() { mgrOpen = !mgrOpen; renderAction(); }

function renderMgr() {
  const el = document.getElementById('mgr-list');
  if (!el) return;
  const pidx = G.turn, p = G.players[pidx];
  const mine = G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx);
  if (!mine.length) {
    el.innerHTML = `<div style="font-size:0.68rem;color:var(--text3);padding:6px 2px">소유 부동산 없음</div>`;
    return;
  }
  el.innerHTML = mine.map(({c,ci}) => {
    if (c.type!=='prop'&&c.type!=='rail'&&c.type!=='util') return '';
    const canBuild = c.type==='prop' && ownsGroup(pidx,c.group) && !c.mortgaged && c.houses<4;
    const cost = BUILD_COST[c.group]||300;
    const dotStyle = c.color ? `background:${c.color}` : `background:#555`;
    let hIcons = '';
    if (c.houses===4) hIcons = '<span style="color:#ef4444;font-size:0.6rem">🏨</span>';
    else for(let i=0;i<c.houses;i++) hIcons+='<span style="color:#22c55e;font-size:0.6rem">■</span>';
    return `<div class="prop-row">
      <div class="prop-color" style="${dotStyle}"></div>
      <span class="prop-name${c.mortgaged?' mortgaged':''}">${c.name}${hIcons}</span>
      <div class="prop-btns">
        ${canBuild&&p.money>=cost?`<button class="mini-b mini-b-build" onclick="doBuild(${pidx},${ci})">${c.houses===3?'🏨':'🏠'}</button>`:''}
        ${!c.mortgaged&&c.houses===0?`<button class="mini-b mini-b-mort" onclick="doMortgage(${pidx},${ci})">저당</button>`:''}
        ${c.mortgaged?`<button class="mini-b mini-b-unmort" onclick="doUnmortgage(${pidx},${ci})" ${p.money<Math.floor(c.price*0.6)?'disabled':''}>해제</button>`:''}
      </div>
    </div>`;
  }).join('');
}

function renderLog() {
  const el = document.getElementById('log-area');
  if (!el) return;
  el.innerHTML = G.log.slice(0, 40).map(e =>
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

// ════════════════════════════════════════════
//  TOOLTIP
// ════════════════════════════════════════════
function showTooltip(ci, e) {
  if (!G) return;
  const c = G.cells[ci];
  const tt = document.getElementById('tooltip');
  const ttTitle = document.getElementById('tt-title');
  const ttBody = document.getElementById('tt-body');
  ttTitle.textContent = c.name;
  let rows = '';
  if (c.type === 'prop') {
    rows += `<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner !== null) {
      rows += `<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      if (!c.mortgaged) {
        const rent = calcRent(ci, 7);
        rows += `<div class="tooltip-row"><span>현재 임료</span><span>₩${rent.toLocaleString()}</span></div>`;
      }
    }
    if (c.houses > 0) {
      rows += `<div class="tooltip-row"><span>건물</span><span>${c.houses === 4 ? '호텔' : '집'+c.houses+'채'}</span></div>`;
    }
    if (c.mortgaged) rows += `<div class="tooltip-row"><span style="color:#ef4444">저당 중</span><span></span></div>`;
  } else if (c.type === 'rail') {
    rows += `<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner !== null) {
      rows += `<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      const n = G.cells.filter(c2=>c2.type==='rail'&&c2.owner===c.owner).length;
      rows += `<div class="tooltip-row"><span>임료</span><span>₩${(100*n).toLocaleString()}</span></div>`;
    }
  } else if (c.type === 'tax') {
    rows += `<div class="tooltip-row"><span>세금</span><span>₩${c.price.toLocaleString()}</span></div>`;
  }
  ttBody.innerHTML = rows;
  tt.style.display = 'block';
  const rect = e.target.getBoundingClientRect();
  let lx = rect.right + 8, ly = rect.top;
  if (lx + 160 > window.innerWidth) lx = rect.left - 168;
  if (ly + 120 > window.innerHeight) ly = window.innerHeight - 130;
  tt.style.left = lx + 'px';
  tt.style.top  = ly + 'px';
}

function hideTooltip() {
  document.getElementById('tooltip').style.display = 'none';
}

// ════════════════════════════════════════════
//  GAME START / OVER / RESET
// ════════════════════════════════════════════
function startGame() {
  const name = document.getElementById('inp-name').value.trim() || '플레이어';
  const bots = parseInt(document.getElementById('inp-bots').value);
  const diff = document.getElementById('inp-diff').value;
  G = initGame(name, bots, diff);

  document.getElementById('setup').style.display = 'none';
  const gameEl = document.getElementById('game');
  gameEl.style.display = 'flex';

  // Determine board size based on available space
  setTimeout(() => {
    const bw = document.querySelector('.board-wrap');
    if (bw) {
      const avail = Math.min(bw.offsetWidth - 24, bw.offsetHeight - 24);
      boardSize = Math.max(360, Math.min(640, avail));
    }
    buildBoard();
    log('🎲 게임 시작!', 'important');
    renderAll();
    setTimeout(checkBotTurn, 800);
  }, 50);
}

function showGameOver() {
  if (!G || !G.winner) return;
  document.getElementById('winner-name').textContent = `🏆 ${G.winner} 우승!`;
  const ranked = [...G.players].sort((a,b) => b.money - a.money);
  const medals = ['🥇','🥈','🥉','4️⃣'];
  document.getElementById('rank-list').innerHTML = ranked.map((p,i) => `
    <div class="rank-row">
      <span class="rank-medal">${medals[i]||''}</span>
      <span class="rank-player" style="color:${p.color}">${p.token} ${p.name}</span>
      ${p.bankrupt
        ? `<span class="rank-dead">💀 파산</span>`
        : `<span class="rank-money">₩${p.money.toLocaleString()}</span>`}
    </div>`).join('');
  document.getElementById('gameover').style.display = 'flex';
  butler('win');
  spawnConfetti();
}

function resetGame() {
  G = null; mgrOpen = false; animating = false;
  document.getElementById('gameover').style.display = 'none';
  document.getElementById('game').style.display = 'none';
  document.getElementById('setup').style.display = 'flex';
}

// ════════════════════════════════════════════
//  CONFETTI
// ════════════════════════════════════════════
function spawnConfetti() {
  const colors = ['#ff4d6d','#3b82f6','#22c55e','#f97316','#a855f7','#ffd700','#14b8a6'];
  for (let i = 0; i < 100; i++) {
    const d = document.createElement('div');
    d.className = 'confetti-piece';
    const size = 5 + Math.random() * 8;
    const dur  = 1.5 + Math.random() * 2.5;
    const delay = Math.random() * 1.8;
    d.style.cssText = `
      left:${Math.random()*100}%;
      top:-20px;
      width:${size}px;height:${size}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      border-radius:${Math.random()>0.5?'50%':'2px'};
      animation-duration:${dur}s;
      animation-delay:${delay}s;
    `;
    document.body.appendChild(d);
    setTimeout(() => d.remove(), (dur + delay + 0.5) * 1000);
  }
}
</script>
</body>
</html>

"""

def main():
    st.set_page_config(
        page_title="부루마블 🎲",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    components.html(GAME_HTML, height=800, scrolling=False)

if __name__ == "__main__":
    main()import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>부루마블 🎲</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&family=Black+Han+Sans&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0e0e14;
  --bg2: #16161f;
  --bg3: #1e1e2a;
  --border: rgba(255,255,255,0.08);
  --border2: rgba(255,255,255,0.14);
  --text: #f0f0f5;
  --text2: #9090a8;
  --text3: #5a5a6e;
  --accent: #ff4d6d;
  --accent2: #ff8fa3;
  --gold: #ffd700;
  --green: #22c55e;
  --blue: #3b82f6;
  --red: #ef4444;
  --orange: #f97316;
  --purple: #a855f7;
  --teal: #14b8a6;
  --r: 12px;
  --r2: 8px;
  --shadow: 0 4px 24px rgba(0,0,0,0.5);
  --shadow2: 0 2px 12px rgba(0,0,0,0.4);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Noto Sans KR', sans-serif;
  background: var(--bg);
  color: var(--text);
  overflow: hidden;
  height: 100vh;
  width: 100vw;
}

/* ══════════════════════════════════
   SETUP SCREEN
══════════════════════════════════ */
#setup {
  position: fixed; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  background: radial-gradient(ellipse at 50% 0%, #1a0a2e 0%, #0e0e14 60%);
  z-index: 100;
}

.setup-glow {
  position: absolute; top: 0; left: 50%;
  transform: translateX(-50%);
  width: 600px; height: 300px;
  background: radial-gradient(ellipse, rgba(255,77,109,0.15) 0%, transparent 70%);
  pointer-events: none;
}

.setup-logo {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 4rem;
  background: linear-gradient(135deg, #ff4d6d 0%, #ffd700 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 4px;
  margin-bottom: 4px;
  filter: drop-shadow(0 0 40px rgba(255,77,109,0.4));
}

.setup-sub {
  color: var(--text3);
  font-size: 0.78rem;
  letter-spacing: 3px;
  margin-bottom: 36px;
  text-transform: uppercase;
}

.setup-card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 20px;
  padding: 32px;
  width: 380px;
  box-shadow: var(--shadow);
}

.form-row { margin-bottom: 18px; }
.form-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 1.5px;
  margin-bottom: 7px;
}

.form-input, .form-select {
  width: 100%;
  background: var(--bg3);
  border: 1px solid var(--border2);
  border-radius: var(--r2);
  color: var(--text);
  padding: 11px 14px;
  font-size: 0.9rem;
  font-family: 'Noto Sans KR', sans-serif;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-input:focus, .form-select:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(255,77,109,0.15);
}
.form-select option { background: #1e1e2a; }

.btn-start {
  width: 100%;
  background: linear-gradient(135deg, #ff4d6d, #c0392b);
  border: none;
  border-radius: 12px;
  color: #fff;
  font-family: 'Black Han Sans', sans-serif;
  font-size: 1.2rem;
  letter-spacing: 4px;
  padding: 16px;
  cursor: pointer;
  margin-top: 8px;
  transition: transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 6px 30px rgba(255,77,109,0.4);
}
.btn-start:hover { transform: translateY(-2px); box-shadow: 0 10px 40px rgba(255,77,109,0.55); }
.btn-start:active { transform: scale(0.97); }

.rules-mini {
  margin-top: 20px;
  background: var(--bg3);
  border-radius: var(--r2);
  padding: 12px 14px;
  font-size: 0.73rem;
  color: var(--text3);
  line-height: 1.85;
  border: 1px solid var(--border);
}
.rules-mini b { color: var(--text2); }

/* ══════════════════════════════════
   GAME LAYOUT
══════════════════════════════════ */
#game {
  display: none;
  width: 100vw;
  height: 100vh;
  flex-direction: row;
}

/* Board wrapper */
.board-wrap {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px;
  min-width: 0;
  position: relative;
  background: radial-gradient(ellipse at center, #14142a 0%, #0a0a12 100%);
}

/* ══════════════════════════════════
   THE BOARD
══════════════════════════════════ */
#board {
  position: relative;
  background: #0a1520;
  border: 2px solid rgba(255,215,0,0.2);
  border-radius: 4px;
  box-shadow: 0 0 60px rgba(255,215,0,0.08), var(--shadow);
  aspect-ratio: 1;
  flex-shrink: 0;
}

.cell {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(255,255,255,0.06);
  cursor: default;
  transition: background 0.15s;
  overflow: hidden;
  user-select: none;
}

.cell-name {
  font-size: 0;
  text-align: center;
  color: var(--text2);
  line-height: 1.2;
  font-weight: 500;
  white-space: nowrap;
}

.cell-price {
  color: var(--text3);
  text-align: center;
  font-weight: 400;
  font-size: 0;
}

.cell-icon {
  font-size: 0;
  line-height: 1;
  margin-bottom: 1px;
}

.color-bar {
  position: absolute;
  border-radius: 2px;
}

/* Side cells: bottom row (0-10), left col (10-20), top row (20-30), right col (30-40) */
/* Corner cells are bigger */

.cell-corner {
  background: #0f1a10;
}

/* Houses / hotel markers */
.house-dot {
  width: 5px; height: 5px;
  background: var(--green);
  border-radius: 1px;
  display: inline-block;
  margin: 0 0.5px;
}
.hotel-marker {
  width: 8px; height: 6px;
  background: var(--red);
  border-radius: 1px;
  display: inline-block;
}

.owner-badge {
  position: absolute;
  width: 5px; height: 5px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.5);
  top: 2px; right: 2px;
}

.mortgaged-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0;
  color: #ef4444;
  font-weight: 700;
  letter-spacing: 1px;
}

/* ── Player tokens on board ── */
.token-cluster {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
  align-items: center;
  justify-content: center;
  pointer-events: none;
  z-index: 10;
  transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1);
}

.token {
  width: 16px; height: 16px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.8);
  display: flex; align-items: center; justify-content: center;
  font-size: 7px;
  font-weight: 900;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.6);
  transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}

/* ── Center board ── */
.board-center {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #080a18;
}

.board-title {
  font-family: 'Black Han Sans', sans-serif;
  background: linear-gradient(135deg, #ff4d6d, #ffd700);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-align: center;
  line-height: 1.1;
  letter-spacing: 2px;
}

.dice-center {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.die-face {
  background: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  color: #1a1a2e;
  box-shadow: 0 3px 12px rgba(0,0,0,0.5),
              inset 0 1px 2px rgba(255,255,255,0.7);
  transition: transform 0.1s;
}
.die-face.rolling { animation: diceRoll 0.6s ease-out; }
.die-face.double { box-shadow: 0 0 16px rgba(255,215,0,0.9), 0 3px 12px rgba(0,0,0,0.5); }

@keyframes diceRoll {
  0%   { transform: rotate(0deg) scale(1); }
  20%  { transform: rotate(-20deg) scale(1.15) translateY(-4px); }
  40%  { transform: rotate(15deg) scale(1.2) translateY(-8px); }
  60%  { transform: rotate(-8deg) scale(1.12) translateY(-3px); }
  80%  { transform: rotate(4deg) scale(1.04); }
  100% { transform: rotate(0deg) scale(1); }
}

/* ══════════════════════════════════
   SIDE PANEL
══════════════════════════════════ */
.side {
  width: 240px;
  background: var(--bg2);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  flex-shrink: 0;
}

.side-section {
  padding: 12px 14px;
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.sec-label {
  font-size: 0.6rem;
  font-weight: 700;
  color: var(--text3);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

/* Players */
.player-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 4px;
  border-radius: 8px;
  transition: background 0.2s;
}
.player-item.active {
  background: rgba(255,77,109,0.1);
  margin: 0 -4px;
  padding: 6px 8px;
}
.player-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  box-shadow: 0 0 8px currentColor;
}
.player-name-txt {
  flex: 1;
  font-size: 0.77rem;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.player-cash {
  font-size: 0.73rem;
  font-weight: 700;
  color: var(--green);
  font-variant-numeric: tabular-nums;
}
.player-bankrupt .player-name-txt { color: var(--text3); text-decoration: line-through; }
.player-bankrupt .player-cash { color: var(--text3); }
.jail-badge {
  font-size: 0.6rem;
  background: rgba(239,68,68,0.15);
  color: #ef4444;
  border-radius: 4px;
  padding: 1px 4px;
  flex-shrink: 0;
}

/* Actions */
.action-zone {
  flex: 1;
  padding: 12px 14px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}
.action-zone::-webkit-scrollbar { width: 3px; }
.action-zone::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.turn-banner {
  text-align: center;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 3px 0;
  color: var(--text2);
}

.dice-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 6px 0;
}

.btn {
  border: none;
  border-radius: var(--r2);
  padding: 9px 14px;
  font-family: 'Noto Sans KR', sans-serif;
  font-size: 0.78rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s;
  width: 100%;
}
.btn:active:not(:disabled) { transform: scale(0.97); }
.btn:disabled { opacity: 0.3; cursor: not-allowed; }

.btn-red {
  background: linear-gradient(135deg, #ff4d6d, #c0392b);
  color: #fff;
  box-shadow: 0 3px 12px rgba(255,77,109,0.3);
}
.btn-red:hover:not(:disabled) { box-shadow: 0 5px 20px rgba(255,77,109,0.5); transform: translateY(-1px); }

.btn-green {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  box-shadow: 0 3px 10px rgba(34,197,94,0.3);
}
.btn-green:hover:not(:disabled) { box-shadow: 0 5px 16px rgba(34,197,94,0.5); transform: translateY(-1px); }

.btn-ghost {
  background: var(--bg3);
  color: var(--text2);
  border: 1px solid var(--border2);
}
.btn-ghost:hover:not(:disabled) { background: rgba(255,255,255,0.08); color: var(--text); }

.btn-orange {
  background: linear-gradient(135deg, #f97316, #ea580c);
  color: #fff;
  box-shadow: 0 3px 10px rgba(249,115,22,0.3);
}
.btn-orange:hover:not(:disabled) { box-shadow: 0 5px 16px rgba(249,115,22,0.5); transform: translateY(-1px); }

.btn-row { display: flex; gap: 6px; }
.btn-row .btn { flex: 1; }

/* Card popup */
.card-box {
  background: linear-gradient(135deg, var(--bg3), var(--bg2));
  border: 1px solid rgba(255,215,0,0.25);
  border-radius: 12px;
  padding: 12px;
  text-align: center;
  animation: popIn 0.35s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes popIn {
  from { transform: scale(0.7) translateY(10px); opacity: 0; }
  to   { transform: scale(1) translateY(0);     opacity: 1; }
}
.card-emoji { font-size: 1.8rem; margin-bottom: 5px; }
.card-title { font-weight: 700; font-size: 0.85rem; color: #ffd700; margin-bottom: 3px; }
.card-effect { font-size: 0.72rem; color: #93c5fd; }

.info-box {
  background: rgba(59,130,246,0.08);
  border: 1px solid rgba(59,130,246,0.2);
  border-radius: var(--r2);
  padding: 8px 10px;
  font-size: 0.73rem;
  color: #93c5fd;
  text-align: center;
}

/* Property manager */
.mgr-toggle {
  width: 100%;
  background: none;
  border: 1px solid var(--border2);
  border-radius: 6px;
  color: var(--text3);
  font-size: 0.7rem;
  padding: 5px 10px;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
  text-align: left;
  transition: all 0.2s;
}
.mgr-toggle:hover { background: var(--bg3); color: var(--text2); }

.mgr-list { overflow: hidden; max-height: 0; transition: max-height 0.3s ease; }
.mgr-list.open { max-height: 250px; overflow-y: auto; }
.mgr-list::-webkit-scrollbar { width: 2px; }
.mgr-list::-webkit-scrollbar-thumb { background: var(--border2); }

.prop-row {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 2px;
  border-bottom: 1px solid rgba(255,255,255,0.04);
  font-size: 0.68rem;
}
.prop-row:last-child { border: none; }
.prop-color { width: 6px; height: 6px; border-radius: 1px; flex-shrink: 0; }
.prop-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text2); }
.prop-name.mortgaged { color: #ef4444; opacity: 0.7; }
.prop-btns { display: flex; gap: 2px; flex-shrink: 0; }
.mini-b {
  padding: 2px 5px;
  font-size: 0.6rem;
  border-radius: 3px;
  border: none;
  cursor: pointer;
  font-family: 'Noto Sans KR', sans-serif;
  font-weight: 700;
  transition: all 0.12s;
}
.mini-b:disabled { opacity: 0.2; cursor: not-allowed; }
.mini-b:active:not(:disabled) { transform: scale(0.92); }
.mini-b-build { background: #22c55e; color: #fff; }
.mini-b-build:hover:not(:disabled) { background: #4ade80; }
.mini-b-mort { background: #ef4444; color: #fff; }
.mini-b-mort:hover:not(:disabled) { background: #f87171; }
.mini-b-unmort { background: #3b82f6; color: #fff; }
.mini-b-unmort:hover:not(:disabled) { background: #60a5fa; }

/* Log */
.log-wrap {
  padding: 0 14px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.log-inner {
  overflow-y: auto;
  flex: 1;
  min-height: 0;
}
.log-inner::-webkit-scrollbar { width: 3px; }
.log-inner::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

.log-row {
  font-size: 0.65rem;
  padding: 2.5px 0;
  color: var(--text3);
  border-bottom: 1px solid rgba(255,255,255,0.025);
  line-height: 1.5;
}
.log-row:last-child { border: none; }
.log-gain { color: #4ade80; }
.log-lose { color: #f87171; }
.log-move { color: #60a5fa; }
.log-important { color: #fbbf24; font-weight: 700; }

/* ══════════════════════════════════
   BUTLER BUBBLE
══════════════════════════════════ */
#butler {
  position: absolute;
  bottom: 14px; left: 14px;
  background: rgba(8,8,20,0.96);
  border: 1px solid rgba(255,77,109,0.35);
  border-radius: 12px;
  padding: 10px 14px;
  max-width: 200px;
  font-size: 0.72rem;
  line-height: 1.6;
  z-index: 30;
  pointer-events: none;
  animation: bubbleIn 0.25s ease;
  display: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}
@keyframes bubbleIn {
  from { transform: translateY(8px); opacity: 0; }
  to   { transform: translateY(0);   opacity: 1; }
}
.butler-head { color: var(--accent); font-weight: 700; font-size: 0.65rem; margin-bottom: 3px; }

/* ══════════════════════════════════
   GAME OVER
══════════════════════════════════ */
#gameover {
  display: none;
  position: fixed; inset: 0;
  background: rgba(5,5,14,0.97);
  z-index: 200;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 30px;
  text-align: center;
}
.winner-crown { font-size: 3rem; animation: bounce 0.8s ease 0.2s both; }
@keyframes bounce {
  0%  { transform: translateY(-40px) scale(0.5); opacity: 0; }
  60% { transform: translateY(8px) scale(1.1); opacity: 1; }
  100%{ transform: translateY(0) scale(1); }
}
.winner-name {
  font-family: 'Black Han Sans', sans-serif;
  font-size: 2.4rem;
  background: linear-gradient(135deg, #ffd700, #ff4d6d);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin: 8px 0;
  animation: winPop 0.7s cubic-bezier(0.34,1.56,0.64,1) 0.3s both;
}
@keyframes winPop {
  from { transform: scale(0.3); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
.winner-sub { font-size: 0.8rem; color: var(--text3); margin-bottom: 28px; letter-spacing: 2px; }

.rank-card {
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 16px;
  padding: 20px 28px;
  width: 100%; max-width: 340px;
  margin-bottom: 28px;
}
.rank-row {
  display: flex; align-items: center; gap: 14px;
  padding: 9px 0;
  border-bottom: 1px solid var(--border);
  font-size: 0.84rem;
}
.rank-row:last-child { border: none; }
.rank-medal { font-size: 1.3rem; min-width: 30px; }
.rank-player { flex: 1; font-weight: 700; }
.rank-money { color: var(--green); font-weight: 700; }
.rank-dead { color: var(--red); font-size: 0.72rem; }

/* Confetti */
.confetti-piece {
  position: fixed;
  pointer-events: none;
  z-index: 9999;
  animation: confettiFall linear forwards;
}
@keyframes confettiFall {
  0%   { transform: translateY(-20px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(105vh) rotate(720deg); opacity: 0; }
}

/* Tooltip on cell hover */
.cell-tooltip {
  position: fixed;
  background: var(--bg2);
  border: 1px solid var(--border2);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 0.73rem;
  z-index: 50;
  pointer-events: none;
  box-shadow: var(--shadow);
  min-width: 140px;
  display: none;
}
.tooltip-title { font-weight: 700; color: var(--text); margin-bottom: 4px; }
.tooltip-row { display: flex; justify-content: space-between; gap: 16px; color: var(--text3); font-size: 0.68rem; padding: 1.5px 0; }
.tooltip-row span:last-child { color: var(--text2); }

</style>
</head>
<body>

<!-- ════════ SETUP ════════ -->
<div id="setup">
  <div class="setup-glow"></div>
  <div class="setup-logo">부루마블</div>
  <div class="setup-sub">BURUMABL · BOARD GAME</div>
  <div class="setup-card">
    <div class="form-row">
      <label class="form-label">내 이름</label>
      <input class="form-input" id="inp-name" value="플레이어" maxlength="8">
    </div>
    <div class="form-row">
      <label class="form-label">봇 수</label>
      <select class="form-select" id="inp-bots">
        <option value="1">봇 1명 (2인)</option>
        <option value="2" selected>봇 2명 (3인)</option>
        <option value="3">봇 3명 (4인)</option>
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
    <button class="btn-start" onclick="startGame()">🎲 게임 시작</button>
    <div class="rules-mini">
      시작자금 <b>₩8,000</b> · 출발 통과 <b>+₩200</b><br>
      독점 시 임료 2배 · 집(4채) → 호텔<br>
      무인도 탈출: 더블 또는 보석금 <b>₩500</b><br>
      저당 50% 환급 · 해제 60% 납부
    </div>
  </div>
</div>

<!-- ════════ GAME ════════ -->
<div id="game">
  <div class="board-wrap">
    <div id="board"></div>
    <div id="butler">
      <div class="butler-head">🎩 집사</div>
      <span id="butler-text"></span>
    </div>
  </div>
  <div class="side">
    <div class="side-section">
      <div class="sec-label">플레이어</div>
      <div id="players-list"></div>
    </div>
    <div class="action-zone" id="action-zone"></div>
    <div class="log-wrap">
      <div class="sec-label" style="padding:8px 0 5px;flex-shrink:0">게임 로그</div>
      <div class="log-inner" id="log-area"></div>
    </div>
  </div>
</div>

<!-- ════════ GAME OVER ════════ -->
<div id="gameover">
  <div class="winner-crown">🏆</div>
  <div class="winner-name" id="winner-name"></div>
  <div class="winner-sub">최후의 승자!</div>
  <div class="rank-card" id="rank-list"></div>
  <button class="btn btn-red" style="max-width:240px;font-family:'Black Han Sans',sans-serif;font-size:1.1rem;letter-spacing:3px" onclick="resetGame()">🔄 다시 하기</button>
</div>

<!-- Tooltip -->
<div class="cell-tooltip" id="tooltip">
  <div class="tooltip-title" id="tt-title"></div>
  <div id="tt-body"></div>
</div>

<script>
// ════════════════════════════════════════════
//  CONSTANTS & DATA
// ════════════════════════════════════════════
const CELLS = [
  {name:"출발",    type:"go",     price:0,    rent:0,   group:-1, color:""},
  {name:"서울",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"부산",    type:"prop",   price:600,  rent:60,  group:0,  color:"#c0392b"},
  {name:"소득세",  type:"tax",    price:200,  rent:0,   group:-1, color:""},
  {name:"철도A",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"인천",    type:"prop",   price:800,  rent:80,  group:1,  color:"#9b59b6"},
  {name:"운명",    type:"fate",   price:0,    rent:0,   group:-1, color:""},
  {name:"대전",    type:"prop",   price:800,  rent:80,  group:1,  color:"#9b59b6"},
  {name:"제주",    type:"prop",   price:900,  rent:90,  group:1,  color:"#9b59b6"},
  {name:"여행",    type:"visit",  price:0,    rent:0,   group:-1, color:""},
  {name:"광주",    type:"prop",   price:1000, rent:100, group:2,  color:"#e67e22"},
  {name:"전기",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"울산",    type:"prop",   price:1000, rent:100, group:2,  color:"#e67e22"},
  {name:"대구",    type:"prop",   price:1100, rent:110, group:2,  color:"#e67e22"},
  {name:"철도B",   type:"rail",   price:400,  rent:100, group:-1, color:""},
  {name:"수원",    type:"prop",   price:1200, rent:120, group:3,  color:"#e74c3c"},
  {name:"찬스",    type:"chance", price:0,    rent:0,   group:-1, color:""},
  {name:"고양",    type:"prop",   price:1300, rent:130, group:3,  color:"#e74c3c"},
  {name:"성남",    type:"prop",   price:1400, rent:140, group:3,  color:"#e74c3c"},
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
  {name:"파주",    type:"prop",   price:2200, rent:220, group:7,  color:"#f1c40f"},
  {name:"가스",    type:"util",   price:300,  rent:0,   group:-1, color:""},
  {name:"김포",    type:"prop",   price:2200, rent:220, group:7,  color:"#f1c40f"},
  {name:"사치세",  type:"tax",    price:300,  rent:0,   group:-1, color:""},
];

const GRP_SIZE = {0:2,1:3,2:3,3:3,4:3,5:3,6:3,7:2};
const BUILD_COST = {0:200,1:250,2:300,3:350,4:350,5:400,6:400,7:500};
const RENT_MULT = [1,5,15,45,80];
const PCOLORS = ["#ff4d6d","#3b82f6","#22c55e","#f97316"];
const PTOKENS = ["▲","●","◆","★"];
const BOT_NAMES = ["알파봇","베타봇","감마봇"];
const DICE_FACES = ["⚀","⚁","⚂","⚃","⚄","⚅"];
const JAIL_BAIL = 500, START_MONEY = 8000, PASS_GO = 200;

const CHANCE_CARDS = [
  {emoji:"💰",text:"은행 배당금",      type:"money", amount:100},
  {emoji:"📋",text:"세금 환급",         type:"money", amount:150},
  {emoji:"🎂",text:"생일! 각자 50 받기",type:"birthday", amount:50},
  {emoji:"🔧",text:"수리비 청구",       type:"money", amount:-100},
  {emoji:"🏥",text:"의료비 청구",       type:"money", amount:-150},
  {emoji:"📚",text:"학교 수업료",       type:"money", amount:-200},
  {emoji:"📈",text:"투자 수익",         type:"money", amount:200},
  {emoji:"🚩",text:"출발로! +200",      type:"goto",  target:0},
  {emoji:"🔒",text:"무인도로!",         type:"goto_jail"},
  {emoji:"⬅️",text:"뒤로 3칸",         type:"move",  amount:-3},
  {emoji:"➡️",text:"앞으로 6칸",        type:"move",  amount:6},
  {emoji:"🚂",text:"가장 가까운 철도로",type:"nearest_rail"},
  {emoji:"🔨",text:"수리비: 집×40 호텔×115", type:"repair"},
  {emoji:"🏦",text:"은행 오류! +500",   type:"money", amount:500},
];

const FATE_CARDS = [
  {emoji:"🎫",text:"복권 당첨! +300",   type:"money", amount:300},
  {emoji:"🚦",text:"과태료 -50",         type:"money", amount:-50},
  {emoji:"💊",text:"보험금 수령 +100",   type:"money", amount:100},
  {emoji:"🚗",text:"수리비 -100",        type:"money", amount:-100},
  {emoji:"🎵",text:"콘서트 수익 +150",   type:"money", amount:150},
  {emoji:"✈️",text:"여행 경비 -100",     type:"money", amount:-100},
  {emoji:"🚩",text:"출발로! +200",       type:"goto",  target:0},
  {emoji:"🔒",text:"무인도로!",          type:"goto_jail"},
  {emoji:"➡️",text:"앞으로 3칸",         type:"move",  amount:3},
  {emoji:"🎂",text:"각자 50씩 받기",     type:"birthday", amount:50},
  {emoji:"💸",text:"탈세 적발 -200",     type:"money", amount:-200},
  {emoji:"🏦",text:"은행 이자 +200",     type:"money", amount:200},
];

const BUTLER = {
  buy:      ["마음에 드시는군요, 주인님!","투자하실 만합니다!","좋은 선택입니다!"],
  pass:     ["다음 기회를 기다리시는군요.","현명한 판단입니다.","때를 기다리십시오."],
  rent_in:  ["통행료 수령! 훌륭합니다!","수익이 들어왔습니다!","부동산이 일하는군요!"],
  rent_out: ["통행료를 납부하셨습니다...","아이고, 피하셔야 했는데.","다음엔 조심하십시오."],
  jail:     ["무인도로 가십니다...","잠시 구금되셨습니다.","곧 탈출하실 겁니다!"],
  double:   ["더블! 한 번 더 굴리세요!","행운이 따르는군요!","연속 이동 기회입니다!"],
  triple:   ["3연속 더블! 무인도입니다!","너무 과하셨습니다..."],
  build:    ["건설 완료! 수익이 오릅니다!","이제 통행료가 올라갑니다!","훌륭한 투자입니다!"],
  bankrupt: ["파산하셨습니다... 유감입니다.","다음엔 반드시 이기실 겁니다!"],
  win:      ["우승 축하드립니다, 주인님!","역시 주인님이십니다!","최고이십니다!"],
  go_pass:  ["출발 통과! +200 수령!","통과 보너스입니다, 주인님!"],
};

// ════════════════════════════════════════════
//  STATE
// ════════════════════════════════════════════
let G = null;
let mgrOpen = false;
let butlerTmr = null;
let animating = false;
let boardSize = 560;

function newCells() {
  return CELLS.map(c => ({...c, owner:null, houses:0, mortgaged:false}));
}

function initGame(name, bots, diff) {
  const players = [{
    name, money:START_MONEY, pos:0,
    color:PCOLORS[0], token:PTOKENS[0],
    is_bot:false, bankrupt:false, jail_turns:0
  }];
  for (let i = 0; i < bots; i++) {
    players.push({
      name:BOT_NAMES[i], money:START_MONEY, pos:0,
      color:PCOLORS[i+1], token:PTOKENS[i+1],
      is_bot:true, bankrupt:false, jail_turns:0
    });
  }
  return { players, cells:newCells(), turn:0, doubles:0,
           phase:'roll', log:[], diff,
           pending_card:null, winner:null, d1:1, d2:1 };
}

// ════════════════════════════════════════════
//  BUTLER
// ════════════════════════════════════════════
function butler(key) {
  const msgs = BUTLER[key] || ["..."];
  const msg = msgs[Math.floor(Math.random() * msgs.length)];
  const el = document.getElementById('butler');
  const txt = document.getElementById('butler-text');
  txt.textContent = msg;
  el.style.display = 'block';
  if (butlerTmr) clearTimeout(butlerTmr);
  butlerTmr = setTimeout(() => el.style.display = 'none', 3200);
}

// ════════════════════════════════════════════
//  GAME LOGIC
// ════════════════════════════════════════════
function log(msg, style='') {
  G.log.unshift({msg, style});
  if (G.log.length > 100) G.log.length = 100;
}

function alive() { return G.players.filter(p => !p.bankrupt); }

function checkWin() {
  const a = alive();
  if (a.length === 1) { G.winner = a[0].name; G.phase = 'gameover'; return true; }
  return false;
}

function ownsGroup(pidx, grp) {
  if (grp < 0) return false;
  const total = GRP_SIZE[grp] || 0;
  return G.cells.filter(c => c.group === grp && c.owner === pidx).length === total;
}

function calcRent(ci, roll) {
  const c = G.cells[ci];
  if (c.owner === null || c.mortgaged) return 0;
  const {type, owner, houses, rent, group} = c;
  if (type === 'prop') {
    const h = Math.min(houses, 4);
    if (h === 0 && ownsGroup(owner, group)) return rent * 2;
    return rent * RENT_MULT[h];
  }
  if (type === 'rail') {
    const n = G.cells.filter(c2 => c2.type === 'rail' && c2.owner === owner).length;
    return 100 * n;
  }
  if (type === 'util') {
    const n = G.cells.filter(c2 => c2.type === 'util' && c2.owner === owner).length;
    const r = roll || (Math.floor(Math.random()*11)+2);
    return r * (n === 1 ? 4 : 10);
  }
  return 0;
}

function nearestRail(pos) {
  const rails = [5,15,25,35];
  return rails.reduce((b,r) => ((r-pos+40)%40) < ((b-pos+40)%40) ? r : b);
}

function movePlayer(pidx, steps) {
  const p = G.players[pidx];
  const old = p.pos;
  const nw = ((old + steps) % 40 + 40) % 40;
  if (steps > 0 && nw < old) {
    p.money += PASS_GO;
    log(`🚩 ${p.name} 출발 통과! +${PASS_GO}`, 'gain');
    butler('go_pass');
  }
  p.pos = nw;
}

function sendJail(pidx) {
  const p = G.players[pidx];
  p.pos = 20; p.jail_turns = 3;
  log(`🔒 ${p.name} 무인도!`, 'lose');
  butler('jail');
}

function payRent(from, to, amt) {
  const payer = G.players[from], recv = G.players[to];
  const actual = Math.min(amt, Math.max(0, payer.money));
  payer.money -= actual; recv.money += actual;
  log(`💸 ${payer.name}→${recv.name}: 임료 ${actual}`, 'lose');
  butler(from === 0 ? 'rent_out' : 'rent_in');
  checkBankrupt(from);
}

function checkBankrupt(pidx) {
  const p = G.players[pidx];
  if (p.money >= 0) return;
  // 긴급 저당
  for (let ci = 0; ci < G.cells.length; ci++) {
    const c = G.cells[ci];
    if (c.owner === pidx && !c.mortgaged && c.houses === 0 && p.money < 0) {
      const val = Math.floor(c.price * 0.5);
      c.mortgaged = true; p.money += val;
      log(`📋 ${p.name} ${c.name} 긴급저당 +${val}`, 'lose');
    }
  }
  if (p.money < 0) {
    p.bankrupt = true; p.money = 0;
    G.cells.forEach(c => { if (c.owner === pidx) { c.owner=null; c.houses=0; c.mortgaged=false; } });
    log(`💀 ${p.name} 파산!`, 'important');
    butler('bankrupt');
    checkWin();
  }
}

function doMortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner !== pidx || c.mortgaged || c.houses > 0) return;
  const val = Math.floor(c.price * 0.5);
  c.mortgaged = true; p.money += val;
  log(`📋 ${p.name} ${c.name} 저당 +${val}`, 'lose');
  renderAll();
}

function doUnmortgage(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  if (c.owner !== pidx || !c.mortgaged) return;
  const cost = Math.floor(c.price * 0.6);
  if (p.money < cost) return;
  c.mortgaged = false; p.money -= cost;
  log(`✅ ${p.name} ${c.name} 저당해제 -${cost}`);
  renderAll();
}

function doBuild(pidx, ci) {
  const c = G.cells[ci], p = G.players[pidx];
  const cost = BUILD_COST[c.group] || 300;
  if (p.money < cost || c.houses >= 4 || c.mortgaged) return;
  c.houses++; p.money -= cost;
  const lbl = c.houses === 4 ? '호텔🏨' : `집 ${c.houses}채`;
  log(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
  butler('build');
  renderAll();
}

function applyCard(pidx, card) {
  const p = G.players[pidx];
  const {type, amount, target, text} = card;
  if (type === 'money') {
    p.money += amount;
    log(`🃏 ${p.name}: ${text} (${amount>0?'+':''}${amount})`, amount>0?'gain':'lose');
    if (amount < 0) checkBankrupt(pidx);
  } else if (type === 'birthday') {
    G.players.forEach((o, i) => {
      if (i !== pidx && !o.bankrupt) {
        const a = Math.min(amount, Math.max(0, o.money));
        o.money -= a; p.money += a;
      }
    });
    log(`🎂 ${p.name} 생일! 각자 ${amount}`, 'gain');
  } else if (type === 'goto') {
    if (target === 0) p.money += PASS_GO;
    p.pos = target;
    log(`🚀 ${p.name} → ${CELLS[target].name}`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'goto_jail') {
    sendJail(pidx);
  } else if (type === 'move') {
    movePlayer(pidx, amount);
    log(`👣 ${p.name} ${amount>0?'+':''}${amount}칸`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'nearest_rail') {
    const nr = nearestRail(p.pos);
    const steps = ((nr - p.pos + 40) % 40) || 40;
    movePlayer(pidx, steps);
    log(`🚂 ${p.name} 철도로!`, 'move');
    landCell(pidx, 0); return;
  } else if (type === 'repair') {
    const h = G.cells.filter(c => c.owner===pidx && c.houses>0 && c.houses<4).length;
    const ht = G.cells.filter(c => c.owner===pidx && c.houses===4).length;
    const cost = h*40 + ht*115;
    p.money -= cost;
    log(`🔧 ${p.name} 수리비 -${cost}`, 'lose');
    checkBankrupt(pidx);
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

function landCell(pidx, roll) {
  const p = G.players[pidx];
  const ci = p.pos;
  const c = G.cells[ci];
  log(`📍 ${p.name} → ${c.name}`, 'move');
  if (c.type === 'go') {
    p.money += PASS_GO;
    log(`🎉 출발 착지! +${PASS_GO}`, 'gain');
  } else if (['prop','rail','util'].includes(c.type)) {
    if (c.owner === null) { G.phase = 'buy'; return; }
    else if (c.owner === pidx) { log('🏠 자기 소유지'); }
    else {
      if (c.mortgaged) log(`📋 ${c.name} 저당 중`);
      else { const rent = calcRent(ci, roll); payRent(pidx, c.owner, rent); }
    }
    checkWin();
  } else if (c.type === 'chance' || c.type === 'fate') {
    const pool = c.type === 'chance' ? CHANCE_CARDS : FATE_CARDS;
    G.pending_card = pool[Math.floor(Math.random() * pool.length)];
    G.phase = 'card';
    return;
  } else if (c.type === 'tax') {
    p.money -= c.price;
    log(`💸 ${p.name} 세금 -${c.price}`, 'lose');
    checkBankrupt(pidx);
  } else if (c.type === 'jail') {
    sendJail(pidx);
  } else {
    log(`✅ ${c.name}`);
  }
  if (G.phase !== 'gameover') G.phase = 'roll';
}

function nextTurn() {
  if (G.phase === 'gameover') return;
  const n = G.players.length;
  let nxt = (G.turn + 1) % n, att = 0;
  while (G.players[nxt].bankrupt && att < n) { nxt = (nxt+1)%n; att++; }
  G.turn = nxt; G.phase = 'roll';
}

// ════════════════════════════════════════════
//  ANIMATIONS
// ════════════════════════════════════════════
function rollDice() {
  const d1 = Math.floor(Math.random()*6)+1;
  const d2 = Math.floor(Math.random()*6)+1;
  return { d1, d2, total:d1+d2, isDouble:d1===d2 };
}

function animateDice(d1, d2, cb) {
  const el1 = document.getElementById('die1');
  const el2 = document.getElementById('die2');
  if (!el1 || !el2) { cb && cb(); return; }
  el1.classList.add('rolling'); el2.classList.add('rolling');
  el1.classList.remove('double'); el2.classList.remove('double');
  let n = 0;
  const iv = setInterval(() => {
    el1.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    el2.textContent = DICE_FACES[Math.floor(Math.random()*6)];
    n++;
    if (n >= 12) {
      clearInterval(iv);
      el1.textContent = DICE_FACES[d1-1];
      el2.textContent = DICE_FACES[d2-1];
      el1.classList.remove('rolling'); el2.classList.remove('rolling');
      if (d1 === d2) { el1.classList.add('double'); el2.classList.add('double'); }
      cb && cb();
    }
  }, 60);
}

function animateMove(pidx, from, to, cb) {
  if (from === to) { cb && cb(); return; }
  const steps = [];
  let cur = from;
  while (cur !== to) { cur = (cur+1)%40; steps.push(cur); }
  let i = 0;
  const iv = setInterval(() => {
    G.players[pidx].pos = steps[i];
    renderTokens();
    i++;
    if (i >= steps.length) { clearInterval(iv); cb && cb(); }
  }, 120);
}

// ════════════════════════════════════════════
//  PLAYER ACTIONS
// ════════════════════════════════════════════
function doRoll() {
  if (!G || animating) return;
  animating = true;
  const {d1, d2, total, isDouble} = rollDice();
  G.d1 = d1; G.d2 = d2;
  renderDiceCenter();
  animateDice(d1, d2, () => {
    if (isDouble) {
      G.doubles++;
      if (G.doubles >= 3) {
        log(`3연속 더블! ${G.players[G.turn].name} 무인도!`, 'important');
        butler('triple');
        sendJail(G.turn); G.doubles = 0;
        nextTurn(); animating = false; renderAll();
        setTimeout(checkBotTurn, 500); return;
      }
      log(`🎲 더블! (${d1}+${d2})`);
      butler('double');
    } else {
      G.doubles = 0;
      log(`🎲 ${d1}+${d2}=${total}`);
    }
    const from = G.players[G.turn].pos;
    renderAll();
    setTimeout(() => {
      animateMove(G.turn, from, (from+total)%40, () => {
        movePlayer(G.turn, total);
        landCell(G.turn, total);
        animating = false;
        if (!isDouble && G.phase !== 'buy' && G.phase !== 'card' && G.phase !== 'gameover')
          nextTurn();
        renderAll();
        if (G.phase === 'gameover') showGameOver();
      });
    }, 200);
  });
}

function doBuy(buy) {
  const pidx = G.turn, ci = G.players[pidx].pos, cell = G.cells[ci];
  if (buy) {
    cell.owner = pidx; G.players[pidx].money -= cell.price;
    log(`🏠 ${G.players[pidx].name} ${cell.name} 매입 -${cell.price}`, 'lose');
    butler('buy');
  } else {
    log(`↩️ ${G.players[pidx].name} ${cell.name} 패스`);
    butler('pass');
  }
  G.phase = 'roll'; nextTurn(); renderAll();
  setTimeout(checkBotTurn, 400);
}

function doCard() {
  if (!G || !G.pending_card) return;
  applyCard(G.turn, G.pending_card);
  G.pending_card = null;
  if (G.phase !== 'gameover') { nextTurn(); renderAll(); setTimeout(checkBotTurn, 400); }
  else { renderAll(); showGameOver(); }
}

function doJail(payBail) {
  if (!G) return;
  const p = G.players[G.turn];
  if (payBail) {
    if (p.money < JAIL_BAIL) return;
    p.money -= JAIL_BAIL; p.jail_turns = 0;
    log(`💰 ${p.name} 보석금 납부!`, 'lose');
    renderAll();
    setTimeout(doRoll, 300);
  } else {
    if (animating) return;
    animating = true;
    const {d1, d2, total, isDouble} = rollDice();
    G.d1 = d1; G.d2 = d2;
    renderDiceCenter();
    animateDice(d1, d2, () => {
      if (isDouble) {
        p.jail_turns = 0;
        log(`🎉 더블 탈출!`);
        animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
          movePlayer(G.turn, total); landCell(G.turn, total);
          if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover') nextTurn();
          animating = false; renderAll();
          if (G.phase==='gameover') showGameOver();
          else setTimeout(checkBotTurn, 500);
        });
      } else {
        p.jail_turns--;
        log(`😔 더블 실패 (${p.jail_turns}턴 남음)`);
        if (p.jail_turns <= 0) {
          p.jail_turns = 0;
          animateMove(G.turn, p.pos, (p.pos+total)%40, () => {
            movePlayer(G.turn, total); landCell(G.turn, total);
            if (G.phase!=='buy'&&G.phase!=='card'&&G.phase!=='gameover') nextTurn();
            animating = false; renderAll();
            if (G.phase==='gameover') showGameOver();
            else setTimeout(checkBotTurn, 500);
          });
        } else {
          nextTurn(); animating = false; renderAll(); setTimeout(checkBotTurn, 400);
        }
      }
    });
  }
}

// ════════════════════════════════════════════
//  BOT AI
// ════════════════════════════════════════════
function checkBotTurn() {
  if (!G || G.phase === 'gameover') return;
  const p = G.players[G.turn];
  if (p.is_bot && !p.bankrupt) doBotTurn();
}

function doBotTurn() {
  setTimeout(() => {
    if (!G || G.phase === 'gameover') return;
    const pidx = G.turn, p = G.players[pidx];
    if (!p.is_bot || p.bankrupt) return;

    if (p.jail_turns > 0 && G.phase === 'roll') {
      if (G.diff === 'hard' && p.money >= JAIL_BAIL) {
        p.money -= JAIL_BAIL; p.jail_turns = 0;
        log(`💰 ${p.name} 보석금!`, 'lose');
        renderAll();
        setTimeout(() => doBotRoll(pidx), 400);
      } else {
        const {d1,d2,total,isDouble} = rollDice();
        G.d1=d1; G.d2=d2;
        if (isDouble) {
          p.jail_turns = 0; log(`🎉 ${p.name} 더블 탈출!`);
          renderAll();
          animateMove(pidx, p.pos, (p.pos+total)%40, () => {
            movePlayer(pidx, total); landCell(pidx, total);
            botDecide(pidx);
            if (G.phase!=='gameover') nextTurn();
            renderAll();
            G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 500);
          });
        } else {
          p.jail_turns--;
          log(`😔 ${p.name} 더블 실패`);
          if (p.jail_turns <= 0) {
            p.jail_turns = 0; renderAll();
            animateMove(pidx, p.pos, (p.pos+total)%40, () => {
              movePlayer(pidx, total); landCell(pidx, total);
              botDecide(pidx);
              if (G.phase!=='gameover') nextTurn();
              renderAll();
              G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 500);
            });
          } else {
            nextTurn(); renderAll(); setTimeout(checkBotTurn, 400);
          }
        }
      }
      return;
    }

    if (G.phase === 'buy' || G.phase === 'card') {
      botDecide(pidx);
      if (G.phase !== 'gameover') nextTurn();
      renderAll();
      G.phase==='gameover' ? showGameOver() : setTimeout(checkBotTurn, 400);
      return;
    }

    if (G.phase === 'roll') {
      botBuild(pidx);
      doBotRoll(pidx);
    }
  }, 600);
}

function doBotRoll(pidx) {
  if (!G || G.phase === 'gameover') return;
  const p = G.players[pidx];
  const {d1, d2, total, isDouble} = rollDice();
  G.d1 = d1; G.d2 = d2;
  if (isDouble) {
    G.doubles++;
    if (G.doubles >= 3) {
      log(`3연속 더블! ${p.name} 무인도!`, 'important');
      butler('triple');
      sendJail(pidx); G.doubles = 0;
      nextTurn(); renderAll(); setTimeout(checkBotTurn, 500); return;
    }
    log(`🎲 ${p.name} 더블! (${d1}+${d2})`);
  } else {
    G.doubles = 0;
    log(`🎲 ${p.name} ${d1}+${d2}=${total}`);
  }
  renderAll();
  const from = p.pos;
  setTimeout(() => {
    animateMove(pidx, from, (from+total)%40, () => {
      movePlayer(pidx, total); landCell(pidx, total);
      botDecide(pidx);
      if (!isDouble && G.phase !== 'gameover') nextTurn();
      renderAll();
      if (G.phase === 'gameover') showGameOver();
      else if (isDouble && G.phase === 'roll') setTimeout(() => doBotRoll(pidx), 700);
      else setTimeout(checkBotTurn, 500);
    });
  }, 200);
}

function botDecide(pidx) {
  const p = G.players[pidx], diff = G.diff;
  if (G.phase === 'buy') {
    const ci = p.pos, cell = G.cells[ci], price = cell.price;
    let buy = false;
    if (diff === 'easy') buy = Math.random() > 0.35 && p.money >= price;
    else if (diff === 'normal') buy = p.money >= price * 1.5;
    else {
      const g = cell.group;
      if (g >= 0) {
        const have = G.cells.filter(c => c.group===g && c.owner===pidx).length;
        if (have === (GRP_SIZE[g]||0) - 1 && p.money >= price) buy = true;
        else buy = p.money >= price * 1.2;
      } else buy = p.money >= price;
    }
    if (buy) {
      cell.owner = pidx; p.money -= price;
      log(`🏠 ${p.name} ${cell.name} 매입 -${price}`, 'lose');
    } else {
      log(`↩️ ${p.name} ${cell.name} 패스`);
    }
    G.phase = 'roll';
  } else if (G.phase === 'card' && G.pending_card) {
    applyCard(pidx, G.pending_card);
    G.pending_card = null;
  }
}

function botBuild(pidx) {
  if (G.diff !== 'hard') return;
  const p = G.players[pidx];
  G.cells.forEach((c, ci) => {
    if (c.owner !== pidx || c.type !== 'prop') return;
    if (!ownsGroup(pidx, c.group) || c.houses >= 4 || c.mortgaged) return;
    const cost = BUILD_COST[c.group] || 300;
    if (p.money >= cost * 1.3) {
      c.houses++; p.money -= cost;
      const lbl = c.houses===4 ? '호텔' : `집${c.houses}`;
      log(`🔨 ${p.name} ${c.name} ${lbl} -${cost}`);
      butler('build');
    }
  });
}

// ════════════════════════════════════════════
//  BOARD LAYOUT CALCULATIONS
// ════════════════════════════════════════════
// Board: 11×11 grid. Corners are bigger.
// CORNER size = S/11 * 1.5, side cells = (S - 2*C) / 9

function getBoardSize() {
  const bw = document.getElementById('board');
  return bw ? bw.offsetWidth : 560;
}

function getCellRect(ci) {
  const S = boardSize;
  const C = S / 7.5; // corner size
  const W = (S - 2*C) / 9; // non-corner cell width
  const H = C;

  if (ci === 0)  return {x: S-C,    y: S-C,    w: C, h: C};
  if (ci === 10) return {x: 0,      y: S-C,    w: C, h: C};
  if (ci === 20) return {x: 0,      y: 0,      w: C, h: C};
  if (ci === 30) return {x: S-C,    y: 0,      w: C, h: C};

  if (ci < 10) {
    const idx = 10 - ci;
    return {x: S-C-idx*W, y: S-C, w: W, h: H};
  }
  if (ci < 20) {
    const idx = ci - 10;
    return {x: 0, y: S-C-idx*W, w: H, h: W};
  }
  if (ci < 30) {
    const idx = ci - 20;
    return {x: C+(idx-1)*W, y: 0, w: W, h: H};
  }
  // 30-39
  const idx = ci - 30;
  return {x: S-C, y: C+(idx-1)*W, w: H, h: W};
}

// ════════════════════════════════════════════
//  BUILD BOARD DOM
// ════════════════════════════════════════════
function buildBoard() {
  const boardEl = document.getElementById('board');
  const S = boardSize;
  boardEl.style.width  = S + 'px';
  boardEl.style.height = S + 'px';
  boardEl.innerHTML = '';

  const C = S / 7.5;
  const W = (S - 2*C) / 9;
  const fs = Math.max(6, Math.round(S / 80));

  // Create cells
  for (let ci = 0; ci < 40; ci++) {
    const {x, y, w, h} = getCellRect(ci);
    const cellData = G.cells[ci];
    const isCorner = ci===0||ci===10||ci===20||ci===30;
    const isSide10  = ci < 10 || ci >= 30; // horizontal
    const isSide20  = ci >= 10 && ci < 20; // left vertical
    const isSide30  = ci >= 20 && ci < 30; // top horizontal

    const div = document.createElement('div');
    div.className = 'cell' + (isCorner ? ' cell-corner' : '');
    div.id = 'cell-' + ci;
    div.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;

    // Background per type
    const bg = {
      go:'#0a2015', jail:'#1a0a2e', visit:'#0a1828',
      free:'#0a1a0a', chance:'#1a1028', fate:'#280a0a',
      tax:'#28180a', rail:'#0a1428', util:'#0a2010',
      prop:'#0d1020'
    }[cellData.type] || '#0d1020';
    div.style.background = bg;

    // Color bar for properties
    if (cellData.color && cellData.type === 'prop') {
      const bar = document.createElement('div');
      bar.className = 'color-bar';
      bar.id = 'bar-' + ci;
      bar.style.background = cellData.color;
      const bThick = Math.round(h * 0.18);
      if (ci < 10 || ci >= 30) {
        bar.style.cssText = `top:0;left:0;width:100%;height:${bThick}px;border-radius:0;`;
      } else if (ci >= 10 && ci < 20) {
        bar.style.cssText = `top:0;right:0;width:${bThick}px;height:100%;border-radius:0;`;
      } else if (ci >= 20 && ci < 30) {
        bar.style.cssText = `bottom:0;left:0;width:100%;height:${bThick}px;border-radius:0;`;
      }
      div.appendChild(bar);
    }

    // Rail bar
    if (cellData.type === 'rail') {
      const bar = document.createElement('div');
      bar.style.cssText = `position:absolute;background:#1c3a5a;opacity:0.9;border-radius:0;`;
      if (ci < 10 || ci >= 30) {
        bar.style.cssText += `top:0;left:0;width:100%;height:${Math.round(h*0.18)}px;`;
      } else {
        bar.style.cssText += `top:0;right:0;width:${Math.round(w*0.18)}px;height:100%;`;
      }
      div.appendChild(bar);
    }

    // Text container
    const textWrap = document.createElement('div');
    textWrap.id = 'tw-' + ci;
    textWrap.style.cssText = `position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;width:100%;height:100%;gap:1px;z-index:1;`;

    // Icon
    const iconMap = {
      go:'🚩', jail:'🔒', visit:'✈️', free:'🅿️', chance:'?', fate:'★', tax:'💸', rail:'🚂'
    };
    let icon = iconMap[cellData.type] || '';
    if (cellData.type === 'util') icon = cellData.name==='전기'?'⚡':'🔥';

    if (icon) {
      const iconEl = document.createElement('div');
      iconEl.className = 'cell-icon';
      iconEl.textContent = icon;
      iconEl.style.fontSize = Math.round(fs * 1.3) + 'px';
      textWrap.appendChild(iconEl);
    }

    const nameEl = document.createElement('div');
    nameEl.className = 'cell-name';
    nameEl.id = 'cn-' + ci;
    const shortName = cellData.name.length > 3 ? cellData.name.slice(0,3) : cellData.name;
    nameEl.textContent = isCorner ? cellData.name : shortName;
    nameEl.style.fontSize = (isCorner ? fs+1 : fs) + 'px';
    textWrap.appendChild(nameEl);

    if (cellData.price > 0 && !isCorner) {
      const priceEl = document.createElement('div');
      priceEl.className = 'cell-price';
      priceEl.textContent = cellData.price.toLocaleString();
      priceEl.style.fontSize = Math.max(5, fs-1) + 'px';
      textWrap.appendChild(priceEl);
    }

    div.appendChild(textWrap);

    // House indicators
    const housesEl = document.createElement('div');
    housesEl.id = 'houses-' + ci;
    housesEl.style.cssText = `position:absolute;display:flex;gap:1px;align-items:center;z-index:2;`;
    if (ci < 10 || ci >= 30) {
      housesEl.style.bottom = '2px';
      housesEl.style.left = '50%';
      housesEl.style.transform = 'translateX(-50%)';
    } else {
      housesEl.style.left = '2px';
      housesEl.style.top = '50%';
      housesEl.style.flexDirection = 'column';
      housesEl.style.transform = 'translateY(-50%)';
    }
    div.appendChild(housesEl);

    // Owner badge
    const badge = document.createElement('div');
    badge.className = 'owner-badge';
    badge.id = 'ob-' + ci;
    badge.style.display = 'none';
    div.appendChild(badge);

    // Mortgaged overlay
    const mort = document.createElement('div');
    mort.className = 'mortgaged-overlay';
    mort.id = 'mo-' + ci;
    mort.textContent = '저당';
    mort.style.cssText += `font-size:${Math.max(6,fs-1)}px;display:none;`;
    div.appendChild(mort);

    div.addEventListener('mouseenter', (e) => showTooltip(ci, e));
    div.addEventListener('mouseleave', hideTooltip);
    boardEl.appendChild(div);
  }

  // Center area
  const C2 = C;
  const center = document.createElement('div');
  center.className = 'board-center';
  center.style.cssText = `left:${C2}px;top:${C2}px;width:${S-2*C2}px;height:${S-2*C2}px;`;
  center.innerHTML = `
    <div class="board-title" style="font-size:${Math.round(S/14)}px;">부루마블</div>
    <div style="font-size:${Math.round(S/80)}px;color:#333;letter-spacing:2px;margin-bottom:8px;">BOARD GAME</div>
    <div class="dice-center">
      <div class="die-face" id="die1" style="width:${Math.round(S/12)}px;height:${Math.round(S/12)}px;">⚀</div>
      <div class="die-face" id="die2" style="width:${Math.round(S/12)}px;height:${Math.round(S/12)}px;">⚁</div>
    </div>
  `;
  boardEl.appendChild(center);

  // Token clusters
  for (let ci = 0; ci < 40; ci++) {
    const {x, y, w, h} = getCellRect(ci);
    const cluster = document.createElement('div');
    cluster.className = 'token-cluster';
    cluster.id = 'tc-' + ci;
    cluster.style.cssText = `left:${x}px;top:${y}px;width:${w}px;height:${h}px;`;
    boardEl.appendChild(cluster);
  }
}

// ════════════════════════════════════════════
//  RENDER FUNCTIONS
// ════════════════════════════════════════════
function renderBoard() {
  if (!G) return;
  const S = boardSize;
  const FS = Math.max(6, Math.round(S / 80));

  G.cells.forEach((c, ci) => {
    // Houses
    const housesEl = document.getElementById('houses-' + ci);
    if (housesEl) {
      housesEl.innerHTML = '';
      if (c.type === 'prop' && c.houses > 0 && !c.mortgaged) {
        if (c.houses === 4) {
          const h = document.createElement('div');
          h.className = 'hotel-marker';
          h.style.width = Math.round(FS*1.4) + 'px';
          h.style.height = Math.round(FS*1.0) + 'px';
          housesEl.appendChild(h);
        } else {
          for (let i = 0; i < c.houses; i++) {
            const hd = document.createElement('div');
            hd.className = 'house-dot';
            hd.style.width = hd.style.height = Math.round(FS*0.8) + 'px';
            housesEl.appendChild(hd);
          }
        }
      }
    }

    // Owner badge
    const ob = document.getElementById('ob-' + ci);
    if (ob) {
      if (c.owner !== null && !c.mortgaged) {
        ob.style.display = 'block';
        ob.style.background = G.players[c.owner].color;
        ob.style.boxShadow = `0 0 6px ${G.players[c.owner].color}80`;
      } else {
        ob.style.display = 'none';
      }
    }

    // Mortgaged
    const mo = document.getElementById('mo-' + ci);
    if (mo) mo.style.display = c.mortgaged ? 'flex' : 'none';
  });
}

function renderDiceCenter() {
  const el1 = document.getElementById('die1');
  const el2 = document.getElementById('die2');
  if (el1) el1.textContent = DICE_FACES[(G.d1||1)-1];
  if (el2) el2.textContent = DICE_FACES[(G.d2||1)-1];
}

function renderTokens() {
  for (let ci = 0; ci < 40; ci++) {
    const tc = document.getElementById('tc-' + ci);
    if (!tc) continue;
    tc.innerHTML = '';
  }
  const slotMap = {};
  G.players.forEach((p, pi) => {
    if (p.bankrupt) return;
    const slot = slotMap[p.pos] || 0;
    slotMap[p.pos] = slot + 1;
    const tc = document.getElementById('tc-' + p.pos);
    if (!tc) return;
    const tk = document.createElement('div');
    tk.className = 'token';
    const tSize = Math.max(12, Math.round(boardSize / 38));
    tk.style.cssText = `width:${tSize}px;height:${tSize}px;background:${p.color};font-size:${Math.round(tSize*0.45)}px;`;
    tk.textContent = p.token;
    tc.appendChild(tk);
  });
}

function renderPlayers() {
  const el = document.getElementById('players-list');
  if (!el) return;
  el.innerHTML = G.players.map((p, i) => {
    const isAct = i === G.turn && !p.bankrupt;
    if (p.bankrupt) return `
      <div class="player-item player-bankrupt">
        <div class="player-dot" style="background:${p.color};opacity:0.2"></div>
        <span class="player-name-txt" style="color:#444">${p.token} ${p.name}</span>
        <span style="font-size:0.65rem;color:#ef4444">💀파산</span>
      </div>`;
    const jailTxt = p.jail_turns > 0 ? `<span class="jail-badge">🔒${p.jail_turns}</span>` : '';
    return `
      <div class="player-item${isAct?' active':''}">
        <div class="player-dot" style="background:${p.color};color:${p.color}"></div>
        <span class="player-name-txt" style="color:${p.color}">${p.token} ${p.name}${p.is_bot?' 🤖':''}</span>
        <span class="player-cash">₩${p.money.toLocaleString()}</span>
        ${jailTxt}
      </div>`;
  }).join('');
}

function renderAction() {
  const az = document.getElementById('action-zone');
  if (!az || !G) return;
  const pidx = G.turn, p = G.players[pidx], phase = G.phase;
  const diceFS = Math.round(boardSize / 18);

  let html = `<div class="turn-banner" style="color:${p.color}">${p.token} ${p.name}${p.is_bot?' 🤖':''} 차례</div>`;
  html += `
    <div class="dice-row">
      <div style="width:40px;height:40px;background:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#1a1a2e;box-shadow:0 3px 12px rgba(0,0,0,0.5);">${DICE_FACES[(G.d1||1)-1]}</div>
      <div style="width:40px;height:40px;background:#fff;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.6rem;color:#1a1a2e;box-shadow:0 3px 12px rgba(0,0,0,0.5);">${DICE_FACES[(G.d2||1)-1]}</div>
    </div>`;

  if (p.is_bot) {
    html += `<div style="text-align:center;font-size:0.7rem;color:var(--text3);padding:8px">⚙️ 봇 처리 중...</div>`;
    az.innerHTML = html; return;
  }
  if (p.bankrupt) { az.innerHTML = html; return; }

  if (p.jail_turns > 0 && phase === 'roll') {
    html += `<div class="info-box">🔒 무인도 구금 중 (${p.jail_turns}턴 남음)</div>`;
    html += `<div class="btn-row">
      <button class="btn btn-orange" onclick="doJail(true)" ${p.money<JAIL_BAIL?'disabled':''}>💰 보석 (${JAIL_BAIL})</button>
      <button class="btn btn-red" onclick="doJail(false)">🎲 더블 도전</button>
    </div>`;
  } else if (phase === 'roll') {
    html += `<button class="btn btn-red" onclick="doRoll()" ${animating?'disabled':''}>🎲 주사위 굴리기</button>`;
    html += `<button class="mgr-toggle" onclick="toggleMgr()">
      ${mgrOpen?'▲':'▼'} 🏗️ 부동산 관리
    </button>
    <div class="mgr-list${mgrOpen?' open':''}" id="mgr-list"></div>`;
  } else if (phase === 'buy') {
    const ci = p.pos, cell = G.cells[ci];
    const ico = cell.type==='prop'?'🏠':cell.type==='rail'?'🚂':'⚡';
    html += `<div class="card-box">
      <div class="card-emoji">${ico}</div>
      <div class="card-title">${cell.name}</div>
      <div class="card-effect">매입가 ₩${cell.price.toLocaleString()} · 기본임료 ₩${cell.rent}</div>
    </div>
    <button class="btn btn-green" onclick="doBuy(true)" ${p.money<cell.price?'disabled':''}>✅ 매입 (-₩${cell.price.toLocaleString()})</button>
    <button class="btn btn-ghost" onclick="doBuy(false)">↩️ 패스</button>`;
  } else if (phase === 'card' && G.pending_card) {
    const card = G.pending_card;
    const amtHtml = card.amount !== undefined
      ? `<span style="color:${card.amount>0?'#4ade80':'#f87171'}">${card.amount>0?'+':''}${card.amount}</span>` : '';
    html += `<div class="card-box">
      <div class="card-emoji">${card.emoji}</div>
      <div class="card-title">${card.text}</div>
      <div class="card-effect">${amtHtml}</div>
    </div>
    <button class="btn btn-red" onclick="doCard()">확인</button>`;
  }

  az.innerHTML = html;
  if (phase === 'roll' && mgrOpen) renderMgr();
}

function toggleMgr() { mgrOpen = !mgrOpen; renderAction(); }

function renderMgr() {
  const el = document.getElementById('mgr-list');
  if (!el) return;
  const pidx = G.turn, p = G.players[pidx];
  const mine = G.cells.map((c,ci)=>({c,ci})).filter(({c})=>c.owner===pidx);
  if (!mine.length) {
    el.innerHTML = `<div style="font-size:0.68rem;color:var(--text3);padding:6px 2px">소유 부동산 없음</div>`;
    return;
  }
  el.innerHTML = mine.map(({c,ci}) => {
    if (c.type!=='prop'&&c.type!=='rail'&&c.type!=='util') return '';
    const canBuild = c.type==='prop' && ownsGroup(pidx,c.group) && !c.mortgaged && c.houses<4;
    const cost = BUILD_COST[c.group]||300;
    const dotStyle = c.color ? `background:${c.color}` : `background:#555`;
    let hIcons = '';
    if (c.houses===4) hIcons = '<span style="color:#ef4444;font-size:0.6rem">🏨</span>';
    else for(let i=0;i<c.houses;i++) hIcons+='<span style="color:#22c55e;font-size:0.6rem">■</span>';
    return `<div class="prop-row">
      <div class="prop-color" style="${dotStyle}"></div>
      <span class="prop-name${c.mortgaged?' mortgaged':''}">${c.name}${hIcons}</span>
      <div class="prop-btns">
        ${canBuild&&p.money>=cost?`<button class="mini-b mini-b-build" onclick="doBuild(${pidx},${ci})">${c.houses===3?'🏨':'🏠'}</button>`:''}
        ${!c.mortgaged&&c.houses===0?`<button class="mini-b mini-b-mort" onclick="doMortgage(${pidx},${ci})">저당</button>`:''}
        ${c.mortgaged?`<button class="mini-b mini-b-unmort" onclick="doUnmortgage(${pidx},${ci})" ${p.money<Math.floor(c.price*0.6)?'disabled':''}>해제</button>`:''}
      </div>
    </div>`;
  }).join('');
}

function renderLog() {
  const el = document.getElementById('log-area');
  if (!el) return;
  el.innerHTML = G.log.slice(0, 40).map(e =>
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

// ════════════════════════════════════════════
//  TOOLTIP
// ════════════════════════════════════════════
function showTooltip(ci, e) {
  if (!G) return;
  const c = G.cells[ci];
  const tt = document.getElementById('tooltip');
  const ttTitle = document.getElementById('tt-title');
  const ttBody = document.getElementById('tt-body');
  ttTitle.textContent = c.name;
  let rows = '';
  if (c.type === 'prop') {
    rows += `<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner !== null) {
      rows += `<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      if (!c.mortgaged) {
        const rent = calcRent(ci, 7);
        rows += `<div class="tooltip-row"><span>현재 임료</span><span>₩${rent.toLocaleString()}</span></div>`;
      }
    }
    if (c.houses > 0) {
      rows += `<div class="tooltip-row"><span>건물</span><span>${c.houses === 4 ? '호텔' : '집'+c.houses+'채'}</span></div>`;
    }
    if (c.mortgaged) rows += `<div class="tooltip-row"><span style="color:#ef4444">저당 중</span><span></span></div>`;
  } else if (c.type === 'rail') {
    rows += `<div class="tooltip-row"><span>매입가</span><span>₩${c.price.toLocaleString()}</span></div>`;
    if (c.owner !== null) {
      rows += `<div class="tooltip-row"><span>소유자</span><span style="color:${G.players[c.owner].color}">${G.players[c.owner].name}</span></div>`;
      const n = G.cells.filter(c2=>c2.type==='rail'&&c2.owner===c.owner).length;
      rows += `<div class="tooltip-row"><span>임료</span><span>₩${(100*n).toLocaleString()}</span></div>`;
    }
  } else if (c.type === 'tax') {
    rows += `<div class="tooltip-row"><span>세금</span><span>₩${c.price.toLocaleString()}</span></div>`;
  }
  ttBody.innerHTML = rows;
  tt.style.display = 'block';
  const rect = e.target.getBoundingClientRect();
  let lx = rect.right + 8, ly = rect.top;
  if (lx + 160 > window.innerWidth) lx = rect.left - 168;
  if (ly + 120 > window.innerHeight) ly = window.innerHeight - 130;
  tt.style.left = lx + 'px';
  tt.style.top  = ly + 'px';
}

function hideTooltip() {
  document.getElementById('tooltip').style.display = 'none';
}

// ════════════════════════════════════════════
//  GAME START / OVER / RESET
// ════════════════════════════════════════════
function startGame() {
  const name = document.getElementById('inp-name').value.trim() || '플레이어';
  const bots = parseInt(document.getElementById('inp-bots').value);
  const diff = document.getElementById('inp-diff').value;
  G = initGame(name, bots, diff);

  document.getElementById('setup').style.display = 'none';
  const gameEl = document.getElementById('game');
  gameEl.style.display = 'flex';

  // Determine board size based on available space
  setTimeout(() => {
    const bw = document.querySelector('.board-wrap');
    if (bw) {
      const avail = Math.min(bw.offsetWidth - 24, bw.offsetHeight - 24);
      boardSize = Math.max(360, Math.min(640, avail));
    }
    buildBoard();
    log('🎲 게임 시작!', 'important');
    renderAll();
    setTimeout(checkBotTurn, 800);
  }, 50);
}

function showGameOver() {
  if (!G || !G.winner) return;
  document.getElementById('winner-name').textContent = `🏆 ${G.winner} 우승!`;
  const ranked = [...G.players].sort((a,b) => b.money - a.money);
  const medals = ['🥇','🥈','🥉','4️⃣'];
  document.getElementById('rank-list').innerHTML = ranked.map((p,i) => `
    <div class="rank-row">
      <span class="rank-medal">${medals[i]||''}</span>
      <span class="rank-player" style="color:${p.color}">${p.token} ${p.name}</span>
      ${p.bankrupt
        ? `<span class="rank-dead">💀 파산</span>`
        : `<span class="rank-money">₩${p.money.toLocaleString()}</span>`}
    </div>`).join('');
  document.getElementById('gameover').style.display = 'flex';
  butler('win');
  spawnConfetti();
}

function resetGame() {
  G = null; mgrOpen = false; animating = false;
  document.getElementById('gameover').style.display = 'none';
  document.getElementById('game').style.display = 'none';
  document.getElementById('setup').style.display = 'flex';
}

// ════════════════════════════════════════════
//  CONFETTI
// ════════════════════════════════════════════
function spawnConfetti() {
  const colors = ['#ff4d6d','#3b82f6','#22c55e','#f97316','#a855f7','#ffd700','#14b8a6'];
  for (let i = 0; i < 100; i++) {
    const d = document.createElement('div');
    d.className = 'confetti-piece';
    const size = 5 + Math.random() * 8;
    const dur  = 1.5 + Math.random() * 2.5;
    const delay = Math.random() * 1.8;
    d.style.cssText = `
      left:${Math.random()*100}%;
      top:-20px;
      width:${size}px;height:${size}px;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      border-radius:${Math.random()>0.5?'50%':'2px'};
      animation-duration:${dur}s;
      animation-delay:${delay}s;
    `;
    document.body.appendChild(d);
    setTimeout(() => d.remove(), (dur + delay + 0.5) * 1000);
  }
}
</script>
</body>
</html>

"""

def main():
    st.set_page_config(
        page_title="부루마블 🎲",
        page_icon="🎲",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    components.html(GAME_HTML, height=800, scrolling=False)

if __name__ == "__main__":
    main()
