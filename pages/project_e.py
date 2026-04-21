<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>⚔️ ABYSS DUNGEON</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@300;400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root {
  --bg:     #04050a;
  --bg2:    #080b14;
  --bg3:    #0c1020;
  --panel:  #060910;
  --border: rgba(120,160,255,0.12);
  --border2:rgba(120,160,255,0.25);
  --glow:   rgba(80,140,255,0.15);
  --text:   #c8d8f8;
  --text2:  #5a78b0;
  --text3:  #2a3860;
  --gold:   #f0c040;
  --gold2:  #ffe080;
  --green:  #40ff90;
  --red:    #ff3355;
  --blue:   #40a8ff;
  --purple: #c060ff;
  --orange: #ff8830;
  --cyan:   #30e8e0;
  --teal:   #20c8a8;
  --pink:   #ff60a8;
  --r:6px;
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{
  font-family:'Noto Sans KR',sans-serif;
  background:var(--bg);color:var(--text);
  height:100vh;width:100vw;overflow:hidden;
  user-select:none;-webkit-user-select:none;
}

/* ===== SCANLINE EFFECT ===== */
body::after{
  content:'';position:fixed;inset:0;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.03) 2px,rgba(0,0,0,0.03) 4px);
  pointer-events:none;z-index:9999;
}

/* ===== LAYOUT ===== */
#app{display:flex;flex-direction:column;height:100vh;width:100vw;position:relative;}

/* ===== TOPBAR ===== */
#topbar{
  display:flex;align-items:center;justify-content:space-between;
  padding:5px 16px;
  background:linear-gradient(90deg,#04070f,#060b18,#04070f);
  border-bottom:1px solid var(--border2);
  flex-shrink:0;height:38px;
  position:relative;overflow:hidden;
}
#topbar::before{
  content:'';position:absolute;bottom:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--blue),var(--cyan),var(--blue),transparent);
  animation:scanline 3s linear infinite;
}
@keyframes scanline{0%{opacity:0.3}50%{opacity:1}100%{opacity:0.3}}
.top-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:1.1rem;letter-spacing:4px;
  background:linear-gradient(90deg,var(--blue),var(--cyan),var(--gold));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;
}
.top-badge{
  background:rgba(0,100,200,0.15);border:1px solid rgba(100,160,255,0.3);
  color:var(--cyan);padding:2px 10px;border-radius:20px;
  font-family:'Share Tech Mono',monospace;font-size:0.72rem;
}
.top-stats{display:flex;gap:14px;font-family:'Share Tech Mono',monospace;font-size:0.7rem;}
.top-stat{color:var(--text2);}
.top-stat b{color:var(--cyan);}

/* ===== MAIN AREA ===== */
#main{display:flex;flex:1;overflow:hidden;}

/* ===== DUNGEON ===== */
#dungeon-wrap{
  flex:1;display:flex;align-items:center;justify-content:center;
  background:var(--bg);overflow:hidden;position:relative;
}
canvas#gc{
  image-rendering:pixelated;
  image-rendering:crisp-edges;
  cursor:crosshair;
}

/* ===== RIGHT PANEL ===== */
#panel{
  width:240px;min-width:240px;
  background:var(--panel);
  border-left:1px solid var(--border2);
  display:flex;flex-direction:column;
  overflow:hidden;
  box-shadow:-4px 0 20px rgba(0,0,0,0.8);
}

/* Panel sections */
.psec{padding:10px 14px;border-bottom:1px solid var(--border);}
.psec-title{
  font-family:'Share Tech Mono',monospace;
  font-size:0.62rem;color:var(--text3);letter-spacing:2px;
  margin-bottom:8px;text-transform:uppercase;
}

/* Stats */
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:3px 8px;}
.s{display:flex;justify-content:space-between;align-items:center;font-size:0.72rem;}
.sl{color:var(--text2);}
.sv{font-family:'Share Tech Mono',monospace;font-weight:700;}
.bar-wrap{height:7px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;margin:3px 0 5px;}
.bar-fill{height:100%;border-radius:3px;transition:width 0.25s;}
.hp-bar{background:linear-gradient(90deg,#8b0000,var(--red),#ff6080);}
.xp-bar{background:linear-gradient(90deg,#4a0080,var(--purple),#e080ff);}

/* Minimap */
#minimap-canvas{width:100%;aspect-ratio:1;display:block;image-rendering:pixelated;}

/* Equipment */
.equip-slot{
  display:flex;align-items:center;gap:7px;
  padding:3px 6px;border-radius:4px;font-size:0.7rem;
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  margin-bottom:3px;min-height:26px;
}
.equip-icon{font-size:13px;width:16px;text-align:center;}
.equip-name{flex:1;color:var(--text);}
.equip-stat{color:var(--text2);font-size:0.62rem;font-family:'Share Tech Mono',monospace;}
.slot-empty{color:var(--text3);font-style:italic;}

/* Log */
#panel-log{flex:1;overflow-y:auto;padding:8px 14px;}
.log-e{font-size:0.68rem;margin-bottom:2px;line-height:1.45;padding:1px 0;}
.lp{color:var(--green);}
.lm{color:var(--red);}
.li{color:var(--gold);}
.ls{color:var(--cyan);}
.lb{color:var(--orange);}
.ll{color:var(--purple);}

/* ===== BOTTOM BAR ===== */
#botbar{
  padding:5px 14px;background:var(--bg2);
  border-top:1px solid var(--border2);
  display:flex;align-items:center;justify-content:space-between;
  flex-shrink:0;height:32px;font-size:0.65rem;color:var(--text2);
}
.kbd{
  display:inline-block;
  background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.18);
  border-radius:3px;padding:1px 6px;color:var(--text);
  font-family:'Share Tech Mono',monospace;font-size:0.6rem;margin:0 2px;
}

/* ===== OVERLAYS ===== */
.ov{
  position:fixed;inset:0;background:rgba(2,4,12,0.95);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  z-index:200;backdrop-filter:blur(4px);
}
.ov.hidden{display:none;}
.ovbox{
  background:linear-gradient(135deg,#08102a,#06080f);
  border:1px solid var(--border2);
  border-radius:10px;padding:28px 36px;
  max-width:520px;width:92%;
  box-shadow:0 0 60px rgba(30,60,180,0.3),0 20px 60px rgba(0,0,0,0.9);
  position:relative;overflow:hidden;
}
.ovbox::before{
  content:'';position:absolute;inset:0;border-radius:10px;
  background:radial-gradient(ellipse at 50% 0%,rgba(60,120,255,0.08),transparent 70%);
  pointer-events:none;
}
.ovtitle{
  font-family:'Black Han Sans',sans-serif;
  font-size:1.8rem;letter-spacing:3px;
  background:linear-gradient(90deg,var(--blue),var(--cyan));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;text-align:center;margin-bottom:6px;
}
.ovdesc{color:var(--text2);font-size:0.82rem;line-height:1.7;text-align:center;margin-bottom:18px;}

/* Buttons */
.btn{
  display:inline-block;padding:9px 22px;border-radius:6px;
  font-weight:700;cursor:pointer;border:none;font-size:0.84rem;
  transition:all 0.18s;margin:4px;position:relative;overflow:hidden;
}
.btn::after{content:'';position:absolute;inset:0;background:rgba(255,255,255,0);transition:background 0.15s;}
.btn:hover::after{background:rgba(255,255,255,0.12);}
.btn:hover{transform:translateY(-2px);}
.btn:active{transform:translateY(0);}
.btn-gold{background:linear-gradient(135deg,#c07010,var(--gold));color:#000;box-shadow:0 4px 15px rgba(200,150,0,0.3);}
.btn-red{background:linear-gradient(135deg,#900,var(--red));color:#fff;box-shadow:0 4px 15px rgba(255,50,80,0.3);}
.btn-blue{background:linear-gradient(135deg,#0040a0,var(--blue));color:#fff;box-shadow:0 4px 15px rgba(50,150,255,0.3);}
.btn-green{background:linear-gradient(135deg,#006030,var(--green));color:#000;box-shadow:0 4px 15px rgba(40,200,100,0.3);}
.btn-purple{background:linear-gradient(135deg,#400080,var(--purple));color:#fff;box-shadow:0 4px 15px rgba(150,50,255,0.3);}
.btn-dim{background:rgba(255,255,255,0.07);color:var(--text2);border:1px solid var(--border2);}

/* Class select */
.class-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;}
.cc{
  background:rgba(255,255,255,0.03);border:2px solid var(--border);
  border-radius:8px;padding:12px 10px;cursor:pointer;transition:all 0.18s;
}
.cc:hover,.cc.sel{
  border-color:var(--cyan);
  background:rgba(30,120,220,0.1);
  box-shadow:0 0 15px rgba(30,200,240,0.15);
}
.cc-icon{font-size:1.8rem;display:block;margin-bottom:5px;}
.cc-name{font-weight:700;color:var(--cyan);font-size:0.82rem;}
.cc-stats{color:var(--text2);font-size:0.62rem;margin-top:3px;line-height:1.5;font-family:'Share Tech Mono',monospace;}

/* Inventory */
.inv-grid-wrap{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;margin:10px 0;}
.islot{
  aspect-ratio:1;background:rgba(255,255,255,0.04);border:1px solid var(--border);
  border-radius:5px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;cursor:pointer;
  font-size:1.2rem;position:relative;transition:all 0.15s;
}
.islot:hover{border-color:var(--cyan);background:rgba(30,150,220,0.1);}
.islot.isel{border-color:var(--gold);background:rgba(200,150,0,0.12);}
.islot.ieq{border-color:var(--green);}
.islot .sn{font-size:0.48rem;color:var(--text2);text-align:center;line-height:1.1;margin-top:1px;padding:0 1px;}
.islot .sb{position:absolute;top:1px;right:1px;background:var(--green);color:#000;border-radius:2px;font-size:0.45rem;padding:1px 2px;font-weight:700;}
#iinfo{background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:6px;padding:10px;min-height:55px;font-size:0.75rem;}

/* Shop */
.shop-item{
  display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,0.03);border:1px solid var(--border);
  border-radius:7px;padding:8px 12px;cursor:pointer;transition:all 0.15s;
  margin-bottom:6px;
}
.shop-item:hover{border-color:var(--gold);background:rgba(200,150,0,0.08);}
.shop-item .si-name{font-weight:700;font-size:0.8rem;}
.shop-item .si-desc{font-size:0.68rem;color:var(--text2);}
.shop-item .si-price{color:var(--gold);font-family:'Share Tech Mono',monospace;font-weight:700;white-space:nowrap;}

/* Skill point */
.sp-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:12px 0;}

/* Death/Victory stats */
.ds-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;text-align:left;font-size:0.78rem;}
.ds-grid div{background:rgba(255,255,255,0.04);padding:6px 10px;border-radius:5px;}

/* Input */
.game-input{
  width:100%;padding:10px;border-radius:6px;
  border:1px solid var(--border2);
  background:rgba(255,255,255,0.05);color:var(--text);
  font-size:0.88rem;text-align:center;outline:none;
  font-family:'Noto Sans KR',sans-serif;
  margin-bottom:14px;
}
.game-input:focus{border-color:var(--cyan);box-shadow:0 0 10px rgba(30,200,240,0.2);}

/* ===== FX ===== */
@keyframes lvup{0%{opacity:0;transform:translate(-50%,-50%) scale(0.4)}60%{opacity:1;transform:translate(-50%,-50%) scale(1.1)}100%{opacity:0;transform:translate(-50%,-50%) scale(1.3) translateY(-40px)}}
.lvup-fx{
  position:fixed;top:50%;left:50%;
  font-family:'Black Han Sans',sans-serif;font-size:2.5rem;
  color:var(--gold);
  text-shadow:0 0 30px var(--gold),0 0 80px rgba(255,200,0,0.5);
  pointer-events:none;animation:lvup 1.4s ease forwards;z-index:300;
  white-space:nowrap;
}
@keyframes dpop{0%{opacity:1;transform:translateX(-50%) translateY(0)}100%{opacity:0;transform:translateX(-50%) translateY(-40px)}}
.dpop{
  position:absolute;
  transform:translateX(-50%);
  font-size:0.8rem;font-weight:900;pointer-events:none;
  animation:dpop 0.8s ease forwards;z-index:50;
  font-family:'Share Tech Mono',monospace;
  text-shadow:0 1px 4px rgba(0,0,0,0.9);
}
@keyframes shake{0%,100%{transform:none}20%{transform:translate(-5px,1px)}40%{transform:translate(5px,-1px)}60%{transform:translate(-3px,2px)}80%{transform:translate(3px,-1px)}}
.shake{animation:shake 0.3s ease;}

/* scrollbar */
::-webkit-scrollbar{width:3px;}
::-webkit-scrollbar-track{background:rgba(0,0,0,0.2);}
::-webkit-scrollbar-thumb{background:rgba(100,150,255,0.2);border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:rgba(100,150,255,0.4);}

/* name input */
#name-wrap{margin-bottom:10px;text-align:center;}
#name-wrap label{font-size:0.75rem;color:var(--text2);display:block;margin-bottom:5px;}

/* rarity glow */
.r-common{color:#c8d8f8;}
.r-uncommon{color:#40a8ff;}
.r-rare{color:#c060ff;}
.r-epic{color:#ff8830;}
.r-legendary{color:#f0c040;text-shadow:0 0 8px rgba(240,192,0,0.5);}
</style>
</head>
<body>
<div id="app">
  <div id="topbar">
    <div class="top-title">⚔ ABYSS DUNGEON</div>
    <div id="floor-badge" class="top-badge">B1F</div>
    <div class="top-stats">
      <span class="top-stat">💀 <b id="t-kills">0</b></span>
      <span class="top-stat">⏱ <b id="t-turns">0</b></span>
      <span class="top-stat">🌟 <b id="t-score">0</b></span>
    </div>
  </div>

  <div id="main">
    <div id="dungeon-wrap">
      <canvas id="gc"></canvas>
    </div>

    <div id="panel">
      <!-- Character -->
      <div class="psec">
        <div class="psec-title">CHARACTER</div>
        <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px;">
          <span style="font-weight:700;color:var(--gold);font-size:0.88rem;" id="p-name">—</span>
          <span style="color:var(--cyan);font-size:0.68rem;" id="p-class">—</span>
        </div>
        <div style="font-size:0.7rem;margin-bottom:3px;display:flex;justify-content:space-between;">
          <span style="color:var(--text2);">Lv <b id="p-lv" style="color:var(--purple);font-size:0.85rem;">1</b></span>
          <span id="p-hp" style="color:var(--red);font-family:'Share Tech Mono',monospace;font-size:0.72rem;">30/30</span>
        </div>
        <div class="bar-wrap"><div class="bar-fill hp-bar" id="hp-bar" style="width:100%"></div></div>
        <div style="font-size:0.68rem;color:var(--text2);display:flex;justify-content:space-between;margin-bottom:2px;">
          <span>XP</span><span id="p-xp" style="font-family:'Share Tech Mono',monospace;color:var(--purple);">0/30</span>
        </div>
        <div class="bar-wrap"><div class="bar-fill xp-bar" id="xp-bar" style="width:0%"></div></div>
        <div class="stat-grid">
          <div class="s"><span class="sl">⚔ ATK</span><span class="sv" id="p-atk" style="color:var(--orange);">5</span></div>
          <div class="s"><span class="sl">🛡 DEF</span><span class="sv" id="p-def" style="color:var(--blue);">2</span></div>
          <div class="s"><span class="sl">⚡ SPD</span><span class="sv" id="p-spd" style="color:var(--green);">5</span></div>
          <div class="s"><span class="sl">🎯 CRT</span><span class="sv" id="p-crt" style="color:var(--pink);">5%</span></div>
          <div class="s" style="grid-column:span 2"><span class="sl">💰 Gold</span><span class="sv" id="p-gold" style="color:var(--gold);">0</span></div>
        </div>
      </div>

      <!-- Minimap -->
      <div class="psec" style="padding:8px 14px;">
        <div class="psec-title">MINIMAP</div>
        <canvas id="minimap-canvas" width="212" height="212"></canvas>
      </div>

      <!-- Equipment -->
      <div class="psec" style="padding:8px 14px;flex-shrink:0;">
        <div class="psec-title">EQUIPPED</div>
        <div id="eq-list"></div>
      </div>

      <!-- Log -->
      <div id="panel-log">
        <div class="psec-title" style="position:sticky;top:0;background:var(--panel);padding:6px 0 3px;">BATTLE LOG</div>
        <div id="log-entries"></div>
      </div>
    </div>
  </div>

  <div id="botbar">
    <div>
      <span class="kbd">↑↓←→</span>이동/공격
      <span class="kbd" style="margin-left:8px;">Space</span>대기/계단
      <span class="kbd" style="margin-left:8px;">I</span>인벤토리
      <span class="kbd" style="margin-left:8px;">S</span>스킬
      <span class="kbd" style="margin-left:8px;">H</span>HP포션
    </div>
    <div id="bot-hint" style="color:var(--text3);">방향키로 이동 — 몬스터에 인접하면 자동 공격</div>
  </div>
</div>

<!-- ========== OVERLAYS ========== -->
<!-- Title -->
<div id="ov-title" class="ov">
  <div class="ovbox" style="max-width:480px;">
    <div style="text-align:center;margin-bottom:20px;">
      <div style="font-family:'Black Han Sans';font-size:3rem;letter-spacing:6px;background:linear-gradient(135deg,var(--blue),var(--cyan),var(--gold));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1;margin-bottom:6px;">ABYSS</div>
      <div style="font-family:'Black Han Sans';font-size:1.3rem;letter-spacing:8px;color:var(--text2);">DUNGEON</div>
      <div style="margin-top:10px;font-size:0.72rem;color:var(--text3);">8클래스 · 50몬스터 · 35아이템 · 보스10종 · 10층던전</div>
    </div>
    <div id="name-wrap">
      <label>캐릭터 이름</label>
      <input id="name-input" class="game-input" type="text" placeholder="이름 입력 (최대 8자)" maxlength="8">
    </div>
    <div style="text-align:center;">
      <button class="btn btn-gold" onclick="gotoClassSelect()">클래스 선택 →</button>
    </div>
    <div style="margin-top:16px;display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:0.68rem;color:var(--text2);">
      <div style="background:rgba(255,255,255,0.03);padding:7px 10px;border-radius:5px;">🗡️ 워리어 · 팔라딘 · 버서커 · 나이트</div>
      <div style="background:rgba(255,255,255,0.03);padding:7px 10px;border-radius:5px;">🔮 메이지 · 위치 · 네크로맨서 · 레인저</div>
    </div>
  </div>
</div>

<!-- Class Select -->
<div id="ov-class" class="ov hidden">
  <div class="ovbox" style="max-width:560px;">
    <div class="ovtitle" style="font-size:1.3rem;margin-bottom:4px;">⚔️ 클래스 선택</div>
    <div class="ovdesc" style="margin-bottom:12px;">당신의 전투 스타일을 선택하세요</div>
    <div class="class-grid" style="grid-template-columns:repeat(4,1fr);" id="class-grid">
      <div class="cc" onclick="pickClass('warrior')" id="cls-warrior">
        <span class="cc-icon">🗡️</span>
        <div class="cc-name">워리어</div>
        <div class="cc-stats">HP:60 ATK:10<br>DEF:5 SPD:5<br>균형잡힌 전사</div>
      </div>
      <div class="cc" onclick="pickClass('paladin')" id="cls-paladin">
        <span class="cc-icon">🛡️</span>
        <div class="cc-name">팔라딘</div>
        <div class="cc-stats">HP:80 ATK:7<br>DEF:10 SPD:4<br>재생+신성피해</div>
      </div>
      <div class="cc" onclick="pickClass('berserker')" id="cls-berserker">
        <span class="cc-icon">🪓</span>
        <div class="cc-name">버서커</div>
        <div class="cc-stats">HP:45 ATK:16<br>DEF:2 SPD:7<br>크리20% 광폭화</div>
      </div>
      <div class="cc" onclick="pickClass('knight')" id="cls-knight">
        <span class="cc-icon">⚔️</span>
        <div class="cc-name">나이트</div>
        <div class="cc-stats">HP:70 ATK:8<br>DEF:8 SPD:5<br>반격 패시브</div>
      </div>
      <div class="cc" onclick="pickClass('mage')" id="cls-mage">
        <span class="cc-icon">🔮</span>
        <div class="cc-name">메이지</div>
        <div class="cc-stats">HP:30 ATK:18<br>DEF:1 SPD:6<br>광역마법 전문</div>
      </div>
      <div class="cc" onclick="pickClass('witch')" id="cls-witch">
        <span class="cc-icon">🧙</span>
        <div class="cc-name">위치</div>
        <div class="cc-stats">HP:35 ATK:14<br>DEF:2 SPD:7<br>독+저주 디버프</div>
      </div>
      <div class="cc" onclick="pickClass('necromancer')" id="cls-necromancer">
        <span class="cc-icon">💀</span>
        <div class="cc-name">네크로맨서</div>
        <div class="cc-stats">HP:32 ATK:12<br>DEF:3 SPD:6<br>흡혈+언데드소환</div>
      </div>
      <div class="cc" onclick="pickClass('ranger')" id="cls-ranger">
        <span class="cc-icon">🏹</span>
        <div class="cc-name">레인저</div>
        <div class="cc-stats">HP:40 ATK:13<br>DEF:3 SPD:10<br>원거리+함정</div>
      </div>
    </div>
    <div style="text-align:center;">
      <button class="btn btn-gold" id="start-btn" onclick="startGame()" disabled style="opacity:0.4;">던전 입장 ⚔️</button>
      <button class="btn btn-dim" onclick="backTitle()">← 돌아가기</button>
    </div>
  </div>
</div>

<!-- Inventory -->
<div id="ov-inv" class="ov hidden">
  <div class="ovbox" style="max-width:440px;">
    <div class="ovtitle" style="font-size:1.2rem;margin-bottom:4px;">🎒 인벤토리</div>
    <div class="inv-grid-wrap" id="inv-grid"></div>
    <div id="iinfo"><span style="color:var(--text3);">아이템을 클릭하면 정보가 표시됩니다.</span></div>
    <div style="margin-top:10px;display:flex;gap:7px;justify-content:center;flex-wrap:wrap;">
      <button class="btn btn-gold" id="inv-use" onclick="invUse()" style="display:none;">사용/장착</button>
      <button class="btn btn-red" id="inv-drop" onclick="invDrop()" style="display:none;">버리기</button>
      <button class="btn btn-dim" onclick="closeInv()">닫기 (I)</button>
    </div>
  </div>
</div>

<!-- Shop -->
<div id="ov-shop" class="ov hidden">
  <div class="ovbox" style="max-width:400px;">
    <div class="ovtitle" style="font-size:1.2rem;margin-bottom:4px;">🏪 신비의 상점</div>
    <div style="text-align:center;font-size:0.78rem;color:var(--text2);margin-bottom:10px;">소지 골드: <span id="shop-gold" style="color:var(--gold);font-weight:700;font-family:'Share Tech Mono',monospace;">0</span></div>
    <div id="shop-items" style="max-height:300px;overflow-y:auto;"></div>
    <div style="text-align:center;margin-top:10px;">
      <button class="btn btn-dim" onclick="closeShop()">나가기 (Esc)</button>
    </div>
  </div>
</div>

<!-- Skill -->
<div id="ov-skill" class="ov hidden">
  <div class="ovbox" style="max-width:360px;">
    <div class="ovtitle" style="font-size:1.3rem;margin-bottom:4px;">⬆️ 레벨 업!</div>
    <div class="ovdesc">스탯 포인트를 분배하세요</div>
    <div class="sp-grid">
      <button class="btn btn-red" onclick="statUp('hp')">❤️ 최대 HP +20</button>
      <button class="btn" style="background:linear-gradient(135deg,#803000,var(--orange));color:#000;" onclick="statUp('atk')">⚔️ ATK +3</button>
      <button class="btn btn-blue" onclick="statUp('def')">🛡️ DEF +2</button>
      <button class="btn btn-green" onclick="statUp('spd')">⚡ SPD +2</button>
      <button class="btn btn-purple" onclick="statUp('crit')">🎯 CRT +5%</button>
      <button class="btn" style="background:linear-gradient(135deg,#006060,var(--teal));color:#000;" onclick="statUp('regen')">💚 재생 +2</button>
    </div>
  </div>
</div>

<!-- Death -->
<div id="ov-death" class="ov hidden">
  <div class="ovbox" style="max-width:420px;text-align:center;">
    <div style="font-size:4rem;margin-bottom:8px;filter:drop-shadow(0 0 20px rgba(255,50,80,0.6));">💀</div>
    <div style="font-family:'Black Han Sans';font-size:2rem;color:var(--red);letter-spacing:4px;margin-bottom:6px;">YOU DIED</div>
    <div id="death-cause" style="color:var(--text2);font-size:0.82rem;margin-bottom:14px;"></div>
    <div id="death-stats" class="ds-grid" style="margin-bottom:18px;"></div>
    <button class="btn btn-red" onclick="restartGame()">↺ 다시 시작</button>
  </div>
</div>

<!-- Victory -->
<div id="ov-win" class="ov hidden">
  <div class="ovbox" style="max-width:420px;text-align:center;">
    <div style="font-size:4rem;margin-bottom:8px;filter:drop-shadow(0 0 20px rgba(240,192,0,0.6));">🏆</div>
    <div style="font-family:'Black Han Sans';font-size:2rem;color:var(--gold);letter-spacing:4px;margin-bottom:6px;">VICTORY!</div>
    <div style="color:var(--text2);font-size:0.82rem;margin-bottom:14px;">최종 보스를 격파했습니다!</div>
    <div id="win-stats" class="ds-grid" style="margin-bottom:18px;"></div>
    <button class="btn btn-gold" onclick="restartGame()">⚔️ 다시 플레이</button>
  </div>
</div>

<script>
// ╔══════════════════════════════════════════════════════════╗
// ║  ABYSS DUNGEON — Full Roguelike Engine                   ║
// ╚══════════════════════════════════════════════════════════╝

const GW = 30, GH = 22; // grid size
const CS = 28;            // cell size in pixels
const MAX_FLOOR = 10;
const VISION = 6;

// Cell types
const T = {WALL:0,FLOOR:1,CORR:2,STAIR:3,SHOP:4,TRAP:5};

// ──────────────────────────────────────────────────────────
// CANVAS SETUP
// ──────────────────────────────────────────────────────────
const canvas = document.getElementById('gc');
const ctx = canvas.getContext('2d');
canvas.width  = GW * CS;
canvas.height = GH * CS;

const mmCanvas = document.getElementById('minimap-canvas');
const mmCtx = mmCanvas.getContext('2d');

// ──────────────────────────────────────────────────────────
// CLASSES
// ──────────────────────────────────────────────────────────
const CLASSES = {
  warrior:    {name:'🗡️ 워리어',   hp:60, atk:10, def:5,  spd:5,  crit:8,  regen:1, skill:'강타',   skillDesc:'3배 피해'},
  paladin:    {name:'🛡️ 팔라딘',   hp:80, atk:7,  def:10, spd:4,  crit:5,  regen:3, skill:'신성폭발', skillDesc:'인접 전체 피해+치유'},
  berserker:  {name:'🪓 버서커',   hp:45, atk:16, def:2,  spd:7,  crit:20, regen:0, skill:'광폭화',  skillDesc:'2턴간 ATK 2배'},
  knight:     {name:'⚔️ 나이트',   hp:70, atk:8,  def:8,  spd:5,  crit:8,  regen:2, skill:'반격',    skillDesc:'피격시 반격 발동'},
  mage:       {name:'🔮 메이지',   hp:30, atk:18, def:1,  spd:6,  crit:12, regen:0, skill:'화염구',  skillDesc:'모든 적에게 피해'},
  witch:      {name:'🧙 위치',     hp:35, atk:14, def:2,  spd:7,  crit:10, regen:0, skill:'독안개',  skillDesc:'모든 적 독 상태'},
  necromancer:{name:'💀 네크로맨서',hp:32, atk:12, def:3,  spd:6,  crit:10, regen:0, skill:'흡혈',   skillDesc:'적 HP 50% 흡수'},
  ranger:     {name:'🏹 레인저',   hp:40, atk:13, def:3,  spd:10, crit:18, regen:1, skill:'연사',    skillDesc:'3회 연속공격'},
};

const CLS_ICONS = {warrior:'🗡️',paladin:'🛡️',berserker:'🪓',knight:'⚔️',mage:'🔮',witch:'🧙',necromancer:'💀',ranger:'🏹'};

// ──────────────────────────────────────────────────────────
// MONSTERS (50종)
// ──────────────────────────────────────────────────────────
const MONSTERS = [
  // F1
  {id:'slime',    n:'슬라임',    e:'🟢', hp:10, atk:3,  def:0, xp:6,  g:4,  fl:1, mv:'rand'},
  {id:'bat',      n:'박쥐',      e:'🦇', hp:8,  atk:4,  def:0, xp:5,  g:3,  fl:1, mv:'chase'},
  {id:'rat',      n:'거대쥐',    e:'🐀', hp:14, atk:4,  def:1, xp:8,  g:5,  fl:1, mv:'rand'},
  {id:'mushroom', n:'독버섯',    e:'🍄', hp:18, atk:3,  def:2, xp:9,  g:5,  fl:1, mv:'rand', poison:true},
  {id:'spider',   n:'거미',      e:'🕷️', hp:12, atk:5,  def:1, xp:9,  g:6,  fl:1, mv:'chase'},
  // F2
  {id:'goblin',   n:'고블린',    e:'👺', hp:22, atk:6,  def:1, xp:14, g:10, fl:2, mv:'chase'},
  {id:'zombie',   n:'좀비',      e:'🧟', hp:35, atk:5,  def:2, xp:16, g:8,  fl:2, mv:'chase'},
  {id:'kobold',   n:'코볼드',    e:'🦎', hp:18, atk:7,  def:1, xp:14, g:10, fl:2, mv:'chase'},
  {id:'bandit',   n:'산적',      e:'🗡️', hp:25, atk:8,  def:2, xp:18, g:14, fl:2, mv:'chase'},
  {id:'wisp',     n:'도깨비불',  e:'🔥', hp:15, atk:9,  def:3, xp:16, g:11, fl:2, mv:'rand'},
  // F3
  {id:'skeleton', n:'스켈레톤',  e:'💀', hp:28, atk:9,  def:3, xp:22, g:14, fl:3, mv:'chase'},
  {id:'orc',      n:'오크',      e:'👿', hp:45, atk:10, def:4, xp:26, g:16, fl:3, mv:'chase'},
  {id:'wolf',     n:'다크울프',  e:'🐺', hp:30, atk:11, def:2, xp:24, g:15, fl:3, mv:'chase'},
  {id:'golem_s',  n:'돌 골렘',   e:'🗿', hp:60, atk:8,  def:8, xp:30, g:18, fl:3, mv:'slow'},
  {id:'dark_elf', n:'다크엘프',  e:'🧝', hp:32, atk:12, def:3, xp:28, g:20, fl:3, mv:'chase'},
  // F4
  {id:'ghost',    n:'유령',      e:'👻', hp:25, atk:13, def:6, xp:30, g:18, fl:4, mv:'phase'},
  {id:'troll',    n:'트롤',      e:'🧌', hp:65, atk:13, def:5, xp:36, g:22, fl:4, mv:'chase'},
  {id:'harpy',    n:'하피',      e:'🦅', hp:35, atk:14, def:3, xp:32, g:20, fl:4, mv:'chase'},
  {id:'medusa',   n:'메두사',    e:'🐍', hp:40, atk:15, def:4, xp:38, g:24, fl:4, mv:'chase', petrify:true},
  {id:'mummy',    n:'미라',      e:'🪦', hp:50, atk:12, def:7, xp:35, g:22, fl:4, mv:'slow', curse:true},
  // F5
  {id:'vampire',  n:'흡혈귀',    e:'🧛', hp:50, atk:16, def:6, xp:44, g:28, fl:5, mv:'chase', drain:true},
  {id:'witch_m',  n:'마녀',      e:'🧙', hp:45, atk:18, def:4, xp:46, g:30, fl:5, mv:'range'},
  {id:'gargoyle', n:'가고일',    e:'🗽', hp:70, atk:14, def:9, xp:48, g:30, fl:5, mv:'slow'},
  {id:'manticore',n:'만티코어',  e:'🦁', hp:60, atk:17, def:5, xp:50, g:34, fl:5, mv:'chase'},
  {id:'dark_mage',n:'암흑마법사',e:'🧙', hp:42, atk:20, def:3, xp:52, g:36, fl:5, mv:'range'},
  // F6
  {id:'golem_i',  n:'철 골렘',   e:'🤖', hp:100,atk:16, def:14,xp:60, g:38, fl:6, mv:'slow'},
  {id:'wyvern',   n:'와이번',    e:'🐉', hp:75, atk:19, def:7, xp:62, g:40, fl:6, mv:'chase'},
  {id:'lich',     n:'리치',      e:'🕯️', hp:65, atk:22, def:8, xp:68, g:44, fl:6, mv:'range'},
  {id:'demon',    n:'데몬',      e:'😈', hp:80, atk:21, def:8, xp:65, g:42, fl:6, mv:'chase'},
  {id:'hydra',    n:'히드라',    e:'🐲', hp:90, atk:18, def:6, xp:70, g:46, fl:6, mv:'slow'},
  // F7
  {id:'death_kn', n:'죽음의 기사',e:'⚰️',hp:90, atk:24, def:10,xp:78, g:50, fl:7, mv:'chase'},
  {id:'chimera',  n:'키메라',    e:'🦄', hp:85, atk:25, def:7, xp:80, g:54, fl:7, mv:'chase'},
  {id:'beholder', n:'비홀더',    e:'👁️', hp:70, atk:26, def:9, xp:82, g:56, fl:7, mv:'range'},
  {id:'titan_m',  n:'미니 타이탄',e:'⚡',hp:120,atk:22, def:12,xp:85, g:55, fl:7, mv:'slow'},
  {id:'banshee',  n:'밴시',      e:'👿', hp:65, atk:28, def:7, xp:88, g:58, fl:7, mv:'chase', wail:true},
  // F8
  {id:'phoenix',  n:'불사조',    e:'🔥', hp:100,atk:28, def:10,xp:96, g:64, fl:8, mv:'chase', rebirth:true},
  {id:'elder_d',  n:'장로 드래곤',e:'🐉',hp:140,atk:26, def:14,xp:100,g:70, fl:8, mv:'chase'},
  {id:'archmage', n:'아치메이지',e:'🧙', hp:80, atk:32, def:8, xp:105,g:70, fl:8, mv:'range'},
  {id:'undead_k', n:'언데드 왕',  e:'👑', hp:120,atk:28, def:12,xp:108,g:72, fl:8, mv:'chase'},
  {id:'chaos_sp', n:'혼돈의 정령',e:'🌀', hp:90, atk:30, def:10,xp:110,g:74, fl:8, mv:'rand'},
  // F9
  {id:'nightmare',n:'나이트메어',e:'🌙', hp:130,atk:33, def:12,xp:120,g:80, fl:9, mv:'chase'},
  {id:'avatar',   n:'악신의 화신',e:'😱', hp:150,atk:30, def:15,xp:125,g:85, fl:9, mv:'slow'},
  {id:'void_w',   n:'공허의 정령',e:'⬛', hp:110,atk:35, def:11,xp:128,g:88, fl:9, mv:'range'},
  {id:'celestial',n:'타락한 천사',e:'👼', hp:125,atk:32, def:13,xp:130,g:90, fl:9, mv:'chase'},
  {id:'time_m',   n:'시간 마수',  e:'⏳', hp:160,atk:28, def:16,xp:135,g:92, fl:9, mv:'slow'},
  // BOSSES
  {id:'boss1', n:'지하 군주',    e:'👁️', hp:200, atk:22, def:10, xp:200, g:300, fl:1,  mv:'boss', boss:true},
  {id:'boss2', n:'암흑 드래곤',  e:'🐲', hp:350, atk:32, def:14, xp:350, g:500, fl:2,  mv:'boss', boss:true},
  {id:'boss3', n:'리치 왕',      e:'👑', hp:400, atk:36, def:16, xp:400, g:600, fl:3,  mv:'boss', boss:true},
  {id:'boss4', n:'지옥의 군주',  e:'😈', hp:500, atk:40, def:18, xp:500, g:700, fl:5,  mv:'boss', boss:true},
  {id:'boss5', n:'혼돈신',       e:'🌀', hp:700, atk:48, def:22, xp:800, g:1200,fl:10, mv:'boss', boss:true, final:true},
];

// ──────────────────────────────────────────────────────────
// ITEMS (35+)
// ──────────────────────────────────────────────────────────
const ITEMS = [
  // Weapons
  {id:'w1', n:'낡은 단검',    e:'🔪', t:'weapon', atk:2,  r:'common',    desc:'ATK +2'},
  {id:'w2', n:'쇠 검',        e:'🗡️', t:'weapon', atk:5,  r:'common',    desc:'ATK +5'},
  {id:'w3', n:'강철 검',      e:'⚔️', t:'weapon', atk:8,  r:'uncommon',  desc:'ATK +8'},
  {id:'w4', n:'마검 다크블레이드',e:'🌑',t:'weapon',atk:13, r:'rare',     desc:'ATK +13'},
  {id:'w5', n:'전설의 신검',  e:'✨', t:'weapon', atk:20, r:'legendary', desc:'ATK +20'},
  {id:'w6', n:'도끼',         e:'🪓', t:'weapon', atk:7,  r:'common',    desc:'ATK +7'},
  {id:'w7', n:'대형 망치',    e:'🔨', t:'weapon', atk:11, r:'uncommon',  desc:'ATK +11'},
  {id:'w8', n:'마법 지팡이',  e:'🪄', t:'weapon', atk:10, r:'uncommon',  desc:'ATK +10 (마법)'},
  {id:'w9', n:'활',           e:'🏹', t:'weapon', atk:6,  r:'common',    desc:'ATK +6 (원거리)'},
  // Armor
  {id:'a1', n:'가죽 갑옷',    e:'🧥', t:'armor',  def:2,  r:'common',    desc:'DEF +2'},
  {id:'a2', n:'쇠 갑옷',      e:'🦺', t:'armor',  def:5,  r:'uncommon',  desc:'DEF +5'},
  {id:'a3', n:'미스릴 갑옷',  e:'🔷', t:'armor',  def:9,  r:'rare',      desc:'DEF +9'},
  {id:'a4', n:'드래곤 갑옷',  e:'🐉', t:'armor',  def:14, r:'legendary', desc:'DEF +14'},
  {id:'sh1',n:'나무 방패',    e:'🛡️', t:'shield', def:1,  r:'common',    desc:'DEF +1'},
  {id:'sh2',n:'강철 방패',    e:'🔵', t:'shield', def:4,  r:'uncommon',  desc:'DEF +4'},
  {id:'sh3',n:'마법 방패',    e:'💠', t:'shield', def:7,  r:'rare',      desc:'DEF +7'},
  {id:'h1', n:'철 투구',      e:'⛑️', t:'helmet', def:2, hp:10, r:'common',   desc:'DEF+2 HP+10'},
  {id:'b1', n:'빠른 장화',    e:'👟', t:'boots',  spd:3,  r:'uncommon',  desc:'SPD +3'},
  {id:'b2', n:'질풍 장화',    e:'⚡', t:'boots',  spd:5,  r:'rare',      desc:'SPD +5'},
  {id:'r1', n:'힘의 반지',    e:'💍', t:'ring',   atk:3,  r:'uncommon',  desc:'ATK +3'},
  {id:'r2', n:'수호 반지',    e:'🔮', t:'ring',   def:3,  r:'uncommon',  desc:'DEF +3'},
  {id:'r3', n:'불사 반지',    e:'♾️', t:'ring',   hp:30,  r:'rare',      desc:'최대HP +30'},
  // Potions
  {id:'p1', n:'소형 포션',    e:'🧪', t:'potion', heal:25, r:'common',   desc:'HP +25 회복'},
  {id:'p2', n:'중형 포션',    e:'💊', t:'potion', heal:55, r:'uncommon', desc:'HP +55 회복'},
  {id:'p3', n:'대형 포션',    e:'💉', t:'potion', heal:100,r:'rare',     desc:'HP +100 회복'},
  {id:'p4', n:'힘의 물약',    e:'💪', t:'potion', patk:4, r:'rare',      desc:'ATK +4 (영구)'},
  {id:'p5', n:'속도 물약',    e:'🏃', t:'potion', pspd:3, r:'rare',      desc:'SPD +3 (영구)'},
  {id:'p6', n:'불사 물약',    e:'🌿', t:'potion', fullheal:true, r:'legendary', desc:'HP 완전 회복'},
  // Scrolls
  {id:'s1', n:'화염 스크롤',  e:'🔥', t:'scroll', dmgAll:40,  r:'uncommon',  desc:'모든 적 40 피해'},
  {id:'s2', n:'빙결 스크롤',  e:'❄️', t:'scroll', freezeAll:true, r:'rare',  desc:'모든 적 빙결'},
  {id:'s3', n:'번개 스크롤',  e:'⚡', t:'scroll', dmgAll:60,  r:'rare',      desc:'모든 적 60 피해'},
  {id:'s4', n:'맵 스크롤',    e:'🗺️', t:'scroll', revealMap:true, r:'uncommon', desc:'전체 맵 공개'},
  {id:'s5', n:'회피 스크롤',  e:'💨', t:'scroll', grantDodge:true,r:'uncommon', desc:'다음 피해 회피'},
  // Special
  {id:'x1', n:'경험의 보석',  e:'💎', t:'gem',    xp:80,  r:'rare',      desc:'경험치 +80'},
  {id:'x2', n:'골드 주머니',  e:'💰', t:'gold',   gold:120,r:'common',   desc:'골드 +120'},
  {id:'x3', n:'보물 상자',    e:'📦', t:'gold',   gold:300,r:'uncommon', desc:'골드 +300'},
  {id:'x4', n:'저주받은 해골',e:'💀', t:'curse',  curse:true,r:'common', desc:'??? 저주'},
];

const RAR_COLOR = {common:'#c8d8f8',uncommon:'#40a8ff',rare:'#c060ff',epic:'#ff8830',legendary:'#f0c040'};

// ──────────────────────────────────────────────────────────
// BOSS FLOOR MAPPING
// ──────────────────────────────────────────────────────────
const BOSS_FLOORS = {1:3, 2:5, 3:6, 4:8, 5:10};

// ──────────────────────────────────────────────────────────
// GAME STATE
// ──────────────────────────────────────────────────────────
let G = {};
let selClass = null;
let selInvItem = null;
let keys = {};

function initG(name, cls) {
  const c = CLASSES[cls];
  G = {
    name, cls, clsName: c.name,
    floor: 1,
    hp: c.hp, maxHp: c.hp,
    atk: c.atk, def: c.def, spd: c.spd, crit: c.crit, regen: c.regen,
    xp: 0, level: 1, xpNext: 40,
    gold: 60,
    kills: 0, turns: 0, score: 0,
    inv: [], equipped: {weapon:null,armor:null,shield:null,ring:null,boots:null,helmet:null},
    dodge: false, berserk: 0, counterReady: false,
    skill_cd: 0,
    map: [], monsters: [], items: [],
    px: 0, py: 0,
    revealed: [], visible: [],
    rooms: [],
    over: false, won: false,
    shopStock: [],
  };
}

// ──────────────────────────────────────────────────────────
// MAP GENERATION
// ──────────────────────────────────────────────────────────
function buildMap() {
  const map = Array.from({length:GH},()=>Array(GW).fill(T.WALL));
  const rooms = [];

  function carve(x,y,w,h) {
    for(let ry=y;ry<y+h;ry++)
      for(let rx=x;rx<x+w;rx++)
        map[ry][rx] = T.FLOOR;
    rooms.push({x,y,w,h,cx:x+Math.floor(w/2),cy:y+Math.floor(h/2)});
  }
  function tunnel(ax,ay,bx,by) {
    let x=ax,y=ay;
    const horiz = Math.random()<0.5;
    if(horiz){
      while(x!==bx){map[y][x]=T.CORR;x+=x<bx?1:-1;}
      while(y!==by){map[y][x]=T.CORR;y+=y<by?1:-1;}
    } else {
      while(y!==by){map[y][x]=T.CORR;y+=y<by?1:-1;}
      while(x!==bx){map[y][x]=T.CORR;x+=x<bx?1:-1;}
    }
  }

  const numRooms = 7 + Math.floor(Math.random()*4);
  let tries = 0;
  while(rooms.length < numRooms && tries < 300) {
    tries++;
    const rw = 4+Math.floor(Math.random()*5);
    const rh = 3+Math.floor(Math.random()*4);
    const rx = 1+Math.floor(Math.random()*(GW-rw-2));
    const ry = 1+Math.floor(Math.random()*(GH-rh-2));
    if(!rooms.some(r=>rx<r.x+r.w+2&&rx+rw>r.x-2&&ry<r.y+r.h+2&&ry+rh>r.y-2))
      carve(rx,ry,rw,rh);
  }
  for(let i=1;i<rooms.length;i++) tunnel(rooms[i-1].cx,rooms[i-1].cy,rooms[i].cx,rooms[i].cy);

  // Player start
  G.px = rooms[0].cx; G.py = rooms[0].cy;

  // Stairs
  const sr = rooms[rooms.length-1];
  map[sr.cy][sr.cx] = T.STAIR;

  // Shop (mid room)
  if(rooms.length>4) { const mr=rooms[Math.floor(rooms.length/2)]; map[mr.cy][mr.cx]=T.SHOP; }

  // Traps
  for(let i=2;i<rooms.length-1;i++) {
    if(Math.random()<0.3) {
      const r=rooms[i];
      const tx=r.x+1+Math.floor(Math.random()*(r.w-2));
      const ty=r.y+1+Math.floor(Math.random()*(r.h-2));
      map[ty][tx]=T.TRAP;
    }
  }

  G.map = map; G.rooms = rooms;
  G.revealed = Array.from({length:GH},()=>Array(GW).fill(false));
  G.visible  = Array.from({length:GH},()=>Array(GW).fill(false));

  spawnMonsters();
  spawnItems();
  calcFOV();
}

function spawnMonsters() {
  G.monsters = [];
  const fl = G.floor;
  const eligible = MONSTERS.filter(m=>!m.boss && m.fl<=fl);

  // Check if boss floor
  const bossId = Object.entries(BOSS_FLOORS).find(([bid,f])=>f===fl)?.[0];
  const bossType = bossId ? MONSTERS.find(m=>m.boss && m.id===`boss${bossId}`) : null;

  for(let i=1;i<G.rooms.length;i++) {
    const r = G.rooms[i];
    if(bossType && i===G.rooms.length-1) continue; // leave boss room for boss
    const cnt = 1 + Math.floor(Math.random()*(2+Math.floor(fl/3)));
    for(let k=0;k<cnt;k++) {
      const mt = eligible[Math.floor(Math.random()*eligible.length)];
      if(!mt) continue;
      const sc = 1+(fl-1)*0.18;
      let mx, my, tries=0;
      do {
        mx = r.x+Math.floor(Math.random()*r.w);
        my = r.y+Math.floor(Math.random()*r.h);
        tries++;
      } while(tries<20 && (G.map[my]?.[mx]===T.WALL || G.monsters.some(m=>m.x===mx&&m.y===my)));
      if(G.map[my]?.[mx]!==T.WALL) {
        G.monsters.push({...mt, id:mt.id+'_'+Date.now()+'_'+k,
          hp:Math.round(mt.hp*sc), maxHp:Math.round(mt.hp*sc),
          atk:Math.round(mt.atk*sc), x:mx, y:my,
          frozen:0, poisoned:0, stunned:0,
        });
      }
    }
  }

  // Boss
  if(bossType && G.rooms.length>1) {
    const br = G.rooms[G.rooms.length-1];
    const sc = 1+(fl-1)*0.1;
    G.monsters.push({...bossType, id:bossType.id+'_boss',
      hp:Math.round(bossType.hp*sc), maxHp:Math.round(bossType.hp*sc),
      atk:Math.round(bossType.atk*sc), x:br.cx, y:br.cy,
      frozen:0, poisoned:0, stunned:0,
    });
  }
}

function spawnItems() {
  G.items = [];
  const regular = ITEMS.filter(i=>i.t!=='curse');
  for(let i=1;i<G.rooms.length;i++) {
    if(Math.random()<0.65) {
      const r = G.rooms[i];
      // Weighted rarity
      const pool = regular.filter(it=>{
        const roll = Math.random();
        if(it.r==='legendary') return roll<0.03;
        if(it.r==='rare')      return roll<0.15;
        if(it.r==='uncommon')  return roll<0.45;
        return true;
      });
      if(!pool.length) continue;
      const it = pool[Math.floor(Math.random()*pool.length)];
      G.items.push({...it, iid:it.id+'_'+Date.now(), x:r.cx, y:r.cy});
    }
  }
}

// ──────────────────────────────────────────────────────────
// FOV
// ──────────────────────────────────────────────────────────
function calcFOV() {
  G.visible = Array.from({length:GH},()=>Array(GW).fill(false));
  const r = VISION + Math.floor(G.spd/4);
  const {px:cx,py:cy} = G;
  for(let dy=-r;dy<=r;dy++) for(let dx=-r;dx<=r;dx++) {
    if(dx*dx+dy*dy>r*r) continue;
    const nx=cx+dx,ny=cy+dy;
    if(nx<0||ny<0||nx>=GW||ny>=GH) continue;
    if(los(cx,cy,nx,ny)) { G.visible[ny][nx]=true; G.revealed[ny][nx]=true; }
  }
}

function los(x0,y0,x1,y1) {
  let dx=Math.abs(x1-x0),dy=Math.abs(y1-y0),sx=x0<x1?1:-1,sy=y0<y1?1:-1,e=dx-dy,x=x0,y=y0;
  while(true) {
    if(x===x1&&y===y1) return true;
    if(G.map[y][x]===T.WALL) return false;
    const e2=2*e;
    if(e2>-dy){e-=dy;x+=sx;}
    if(e2<dx){e+=dx;y+=sy;}
  }
}

// ──────────────────────────────────────────────────────────
// RENDERING — CANVAS
// ──────────────────────────────────────────────────────────
const CELL_COLORS = {
  [T.WALL]:   '#050a14',
  [T.FLOOR]:  '#0d1830',
  [T.CORR]:   '#0b1428',
  [T.STAIR]:  '#0a1f12',
  [T.SHOP]:   '#1a100d',
  [T.TRAP]:   '#1a0d0d',
};
const BORDER_COLORS = {
  [T.WALL]:   '#08101e',
  [T.FLOOR]:  '#142048',
  [T.CORR]:   '#10193a',
  [T.STAIR]:  '#10301a',
  [T.SHOP]:   '#301a0f',
  [T.TRAP]:   '#2a1010',
};

function render() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  ctx.fillStyle='#02040c';
  ctx.fillRect(0,0,canvas.width,canvas.height);

  for(let y=0;y<GH;y++) {
    for(let x=0;x<GW;x++) {
      const vis = G.visible[y][x];
      const rev = G.revealed[y][x];
      if(!rev) continue;

      const ct = G.map[y][x];
      const alpha = vis ? 1 : 0.3;
      const px = x*CS, py = y*CS;

      ctx.globalAlpha = alpha;

      // Cell background
      ctx.fillStyle = CELL_COLORS[ct] || '#050a14';
      ctx.fillRect(px,py,CS,CS);

      // Cell border
      if(ct !== T.WALL) {
        ctx.strokeStyle = BORDER_COLORS[ct] || '#08101e';
        ctx.lineWidth = 0.5;
        ctx.strokeRect(px+0.5,py+0.5,CS-1,CS-1);
      }

      if(!vis) { ctx.globalAlpha=1; continue; }

      // Special cell icons
      ctx.font = `${CS-6}px serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';

      // Render items first (under monsters)
      const item = G.items.find(i=>i.x===x&&i.y===y);
      const mon  = G.monsters.find(m=>m.x===x&&m.y===y);
      const isPlayer = G.px===x && G.py===y;

      if(!mon && !isPlayer && item) {
        ctx.font = `${CS-10}px serif`;
        ctx.fillText(item.e, px+CS/2, py+CS/2+1);
        // Rarity glow
        ctx.globalAlpha=0.25;
        ctx.fillStyle = RAR_COLOR[item.r]||'#fff';
        ctx.fillRect(px+2,py+2,CS-4,CS-4);
        ctx.globalAlpha=1;
      }

      if(ct===T.STAIR && !mon && !isPlayer) {
        ctx.font = `${CS-8}px serif`;
        ctx.fillText('🪜', px+CS/2, py+CS/2+1);
      }
      if(ct===T.SHOP && !mon && !isPlayer) {
        ctx.font = `${CS-8}px serif`;
        ctx.fillText('🏪', px+CS/2, py+CS/2+1);
      }
      if(ct===T.TRAP && !isPlayer) {
        // Hidden trap hint — faint red
        ctx.globalAlpha=0.18;
        ctx.fillStyle='#ff3355';
        ctx.fillRect(px+1,py+1,CS-2,CS-2);
        ctx.globalAlpha=1;
      }

      // Monster
      if(mon) {
        // HP bar above monster
        const hpPct = mon.hp/mon.maxHp;
        const barW = CS-4;
        ctx.fillStyle='rgba(0,0,0,0.6)';
        ctx.fillRect(px+2,py+1,barW,3);
        ctx.fillStyle = mon.boss ? '#ff8830' : (hpPct>0.5?'#40ff90':'#ff3355');
        ctx.fillRect(px+2,py+1,Math.round(barW*hpPct),3);

        // Boss glow
        if(mon.boss) {
          ctx.shadowColor='#ff8830';
          ctx.shadowBlur=8;
        }
        ctx.font = `${CS-8}px serif`;
        ctx.fillText(mon.frozen>0?'🧊':mon.e, px+CS/2, py+CS/2+2);
        ctx.shadowBlur=0;
      }

      // Player
      if(isPlayer) {
        ctx.shadowColor='#40a8ff';
        ctx.shadowBlur=10;
        const icon = {warrior:'🗡️',paladin:'🛡️',berserker:'🪓',knight:'⚔️',mage:'🔮',witch:'🧙',necromancer:'💀',ranger:'🏹'}[G.cls]||'🧙';
        ctx.font = `${CS-6}px serif`;
        ctx.fillText(icon, px+CS/2, py+CS/2+1);
        ctx.shadowBlur=0;
      }

      ctx.globalAlpha=1;
    }
  }

  renderMinimap();
  renderPanel();
}

function renderMinimap() {
  const mw = mmCanvas.width, mh = mmCanvas.height;
  const cw = mw/GW, ch = mh/GH;
  mmCtx.fillStyle='#02040c';
  mmCtx.fillRect(0,0,mw,mh);
  for(let y=0;y<GH;y++) for(let x=0;x<GW;x++) {
    if(!G.revealed[y]?.[x]) continue;
    const ct = G.map[y][x];
    let fc='#0d1830';
    if(ct===T.WALL) fc='#050a14';
    else if(ct===T.STAIR) fc='#20c8a8';
    else if(ct===T.SHOP) fc='#c08030';
    if(G.visible[y]?.[x] && G.monsters.some(m=>m.x===x&&m.y===y)) fc='#ff3355';
    else if(G.visible[y]?.[x] && G.items.some(i=>i.x===x&&i.y===y)) fc='#f0c040';
    mmCtx.fillStyle=fc;
    mmCtx.fillRect(x*cw,y*ch,cw,ch);
  }
  // Player dot
  mmCtx.fillStyle='#40ff90';
  mmCtx.fillRect(G.px*cw,G.py*ch,cw+1,ch+1);
}

function renderPanel() {
  document.getElementById('p-name').textContent  = G.name;
  document.getElementById('p-class').textContent = G.clsName;
  document.getElementById('p-lv').textContent    = G.level;
  document.getElementById('p-hp').textContent    = `${G.hp}/${G.maxHp}`;
  document.getElementById('p-xp').textContent    = `${G.xp}/${G.xpNext}`;
  document.getElementById('p-atk').textContent   = totalAtk();
  document.getElementById('p-def').textContent   = totalDef();
  document.getElementById('p-spd').textContent   = G.spd;
  document.getElementById('p-crt').textContent   = G.crit+'%';
  document.getElementById('p-gold').textContent  = G.gold;
  document.getElementById('floor-badge').textContent = `B${G.floor}F`;
  document.getElementById('t-kills').textContent = G.kills;
  document.getElementById('t-turns').textContent = G.turns;
  document.getElementById('t-score').textContent = G.score;
  document.getElementById('hp-bar').style.width  = Math.max(0,(G.hp/G.maxHp)*100)+'%';
  document.getElementById('xp-bar').style.width  = Math.max(0,(G.xp/G.xpNext)*100)+'%';

  // Equipped
  let eh='';
  const slots = ['weapon','armor','shield','ring','boots','helmet'];
  const slabels = {weapon:'⚔ 무기',armor:'🧥 갑옷',shield:'🛡 방패',ring:'💍 반지',boots:'👟 장화',helmet:'⛑ 투구'};
  for(const sl of slots) {
    const it = G.equipped[sl];
    if(it) eh+=`<div class="equip-slot"><span class="equip-icon">${it.e}</span><span class="equip-name">${it.n}</span><span class="equip-stat">${it.desc}</span></div>`;
  }
  document.getElementById('eq-list').innerHTML = eh || '<div class="equip-slot"><span class="slot-empty">장착 없음</span></div>';
}

// ──────────────────────────────────────────────────────────
// COMBAT
// ──────────────────────────────────────────────────────────
function totalAtk() {
  let a = G.atk;
  for(const it of Object.values(G.equipped)) if(it?.atk) a+=it.atk;
  if(G.berserk>0) a = Math.round(a*2);
  return a;
}
function totalDef() {
  let d = G.def;
  for(const it of Object.values(G.equipped)) if(it?.def) d+=it.def;
  return d;
}

function pAttack(mon) {
  let dmg = Math.max(1, totalAtk() - mon.def + Math.floor(Math.random()*5) - 2);
  const crit = Math.random()*100 < G.crit;
  if(crit) dmg = Math.round(dmg * 1.8);
  if(G.dodge) { G.dodge=false; addLog('💨 회피 발동!','ls'); }
  mon.hp -= dmg;
  addLog(`⚔️ ${mon.n}에게 ${dmg}${crit?' ⚡크리!':''}`, 'lp');
  popDmg(mon.x*CS+CS/2, mon.y*CS, dmg, crit?'#ffd700':'#ff3355');
  shakeWrap();
  if(mon.hp<=0) killMon(mon);
  else if(G.cls==='knight' && G.counterReady) {
    // counter attack
    let cdmg = Math.max(1, Math.round(totalAtk()*0.5));
    G.counterReady=false;
    addLog(`⚔️ 반격! ${mon.n}에게 ${cdmg} 피해`,'lp');
    mon.hp -= cdmg;
    if(mon.hp<=0) killMon(mon);
  }
}

function mAttack(mon) {
  if(mon.stunned>0){mon.stunned--;addLog(`😵 ${mon.n} 기절!`,'ls');return;}
  if(mon.frozen>0) {mon.frozen--;addLog(`🧊 ${mon.n} 빙결!`,'ls');return;}
  let dmg = Math.max(0, mon.atk - totalDef() + Math.floor(Math.random()*4)-1);
  if(G.dodge){G.dodge=false;addLog(`💨 ${mon.n} 공격 회피!`,'lp');return;}

  G.hp = Math.max(0, G.hp - dmg);
  addLog(`👹 ${mon.n}이 ${dmg} 피해!`, 'lm');

  // Special monster effects
  if(mon.drain && mon.hp>0) { mon.hp = Math.min(mon.maxHp, mon.hp+Math.round(dmg*0.5)); addLog(`🧛 ${mon.n} HP 흡수!`,'lm'); }
  if(mon.poison && Math.random()<0.4) addLog('☠️ 독 상태!','lm');
  if(mon.wail && Math.random()<0.3) { G.atk=Math.max(1,G.atk-1); addLog('😱 밴시의 울부짖음! ATK-1','lm'); }

  // Paladin regen
  if(G.cls==='paladin' && G.regen>0 && G.turns%3===0 && G.hp<G.maxHp) {
    G.hp=Math.min(G.maxHp,G.hp+G.regen*2); addLog(`🛡️ 재생 +${G.regen*2}`,'ls');
  }

  // Knight counter
  if(G.cls==='knight' && Math.random()<0.35) G.counterReady=true;

  if(G.hp<=0) gameDie(`${mon.n}`);
}

function killMon(mon) {
  G.kills++; G.xp+=mon.xp; G.gold+=mon.g; G.score+=mon.xp*G.floor;
  addLog(`💀 ${mon.n} 처치! XP+${mon.xp} G+${mon.g}`, mon.boss?'lb':'lp');
  // Drop
  if(Math.random()<0.33) {
    const pool=ITEMS.filter(i=>i.t!=='curse');
    const drop=pool[Math.floor(Math.random()*pool.length)];
    G.items.push({...drop,iid:drop.id+'_d_'+Date.now(),x:mon.x,y:mon.y});
    addLog(`📦 드롭: ${drop.e}${drop.n}`,'li');
  }
  G.monsters=G.monsters.filter(m=>m.id!==mon.id);
  while(G.xp>=G.xpNext) doLevelUp();

  if(mon.boss && mon.final) { gameWin(); return; }
  if(mon.boss) addLog(`🏆 보스 처치!`,'lb');
}

function doLevelUp() {
  G.level++; G.xp-=G.xpNext; G.xpNext=Math.floor(G.xpNext*1.6);
  G.hp=Math.min(G.maxHp,G.hp+10);
  addLog(`⬆️ LEVEL UP! Lv${G.level}`,'ll');
  lvFX();
  document.getElementById('ov-skill').classList.remove('hidden');
}

// ──────────────────────────────────────────────────────────
// PLAYER SKILL
// ──────────────────────────────────────────────────────────
function useSkill() {
  if(G.skill_cd>0){addLog(`⏳ 스킬 쿨다운 ${G.skill_cd}턴`,'ls');return;}
  const c=G.cls;
  if(c==='warrior'){
    // 강타 — 인접 적 3배 피해
    const adj=G.monsters.filter(m=>Math.abs(m.x-G.px)<=1&&Math.abs(m.y-G.py)<=1);
    adj.forEach(m=>{const d=Math.round(totalAtk()*3);m.hp-=d;addLog(`💥 강타! ${m.n}에게 ${d}`,'lp');if(m.hp<=0)killMon(m);});
    G.skill_cd=5;
  } else if(c==='paladin'){
    const adj=G.monsters.filter(m=>Math.abs(m.x-G.px)<=1&&Math.abs(m.y-G.py)<=1);
    adj.forEach(m=>{const d=Math.round(totalAtk()*1.5);m.hp-=d;if(m.hp<=0)killMon(m);});
    G.hp=Math.min(G.maxHp,G.hp+40);
    addLog('✨ 신성폭발! 인접 피해+HP+40','lp');G.skill_cd=6;
  } else if(c==='berserker'){
    G.berserk=3;addLog('🔥 광폭화! 3턴간 ATK 2배','lp');G.skill_cd=8;
  } else if(c==='knight'){
    G.counterReady=true;addLog('⚔️ 반격 태세!','lp');G.skill_cd=4;
  } else if(c==='mage'){
    G.monsters.forEach(m=>{if(G.visible[m.y]?.[m.x]){const d=Math.round(totalAtk()*1.5+20);m.hp-=d;addLog(`🔥 화염구! ${m.n}에게 ${d}`,'lp');if(m.hp<=0)killMon(m);}});
    G.skill_cd=7;
  } else if(c==='witch'){
    G.monsters.forEach(m=>{m.poisoned=5;});addLog('☠️ 독안개! 모든 적 독','lp');G.skill_cd=6;
  } else if(c==='necromancer'){
    G.monsters.forEach(m=>{if(G.visible[m.y]?.[m.x]){const d=Math.round(m.hp*0.3);m.hp-=d;G.hp=Math.min(G.maxHp,G.hp+d);if(m.hp<=0)killMon(m);}});
    addLog('🧛 흡혈! 적 HP 흡수','lp');G.skill_cd=7;
  } else if(c==='ranger'){
    const visible=G.monsters.filter(m=>G.visible[m.y]?.[m.x]);
    if(visible.length>0){
      const t=visible[0];
      for(let i=0;i<3;i++){const d=Math.max(1,totalAtk()-t.def+Math.floor(Math.random()*4)-1);t.hp-=d;addLog(`🏹 연사${i+1}: ${d}`,'lp');}
      if(t.hp<=0)killMon(t);
    }
    G.skill_cd=5;
  }
  document.getElementById('bot-hint').textContent=`⏳ 스킬 쿨다운: ${G.skill_cd}턴`;
  endTurn();
}

// ──────────────────────────────────────────────────────────
// MOVEMENT & TURN
// ──────────────────────────────────────────────────────────
function move(dx,dy) {
  if(G.over||G.won) return;
  const nx=G.px+dx, ny=G.py+dy;
  if(nx<0||ny<0||nx>=GW||ny>=GH) return;
  const ct=G.map[ny][nx];
  if(ct===T.WALL) return;

  const mon=G.monsters.find(m=>m.x===nx&&m.y===ny);
  if(mon){pAttack(mon);endTurn();return;}

  G.px=nx; G.py=ny;
  endTurn();

  // Cell events
  if(ct===T.STAIR) addLog('🪜 계단! Space로 내려가기','ls');
  if(ct===T.SHOP) openShop();
  if(ct===T.TRAP) {
    const dmg=Math.max(1,5+G.floor*3-totalDef());
    G.hp=Math.max(0,G.hp-dmg);
    addLog(`⚠️ 함정! ${dmg} 피해!`,'lm');
    if(G.hp<=0){gameDie('함정');return;}
    G.map[ny][nx]=T.FLOOR; // disarm
  }

  // Item pickup
  const idx=G.items.findIndex(i=>i.x===nx&&i.y===ny);
  if(idx>-1){
    const it=G.items[idx];
    if(G.inv.length<24){G.inv.push(it);G.items.splice(idx,1);addLog(`🎒 ${it.e}${it.n} 획득!`,'li');}
    else addLog('🎒 인벤토리 가득!','ls');
  }
}

function endTurn() {
  G.turns++;
  if(G.skill_cd>0) G.skill_cd--;
  if(G.berserk>0) G.berserk--;

  // Regen
  if(G.regen>0 && G.hp<G.maxHp && G.turns%4===0) G.hp=Math.min(G.maxHp,G.hp+G.regen);

  calcFOV();
  monsterTurn();
  render();
}

function monsterTurn() {
  for(const m of G.monsters) {
    if(!G.visible[m.y]?.[m.x] && !m.boss) continue;
    if(m.stunned>0){m.stunned--;continue;}
    if(m.frozen>0){m.frozen--;continue;}
    if(m.poisoned>0){m.hp-=3;m.poisoned--;if(m.hp<=0){killMon(m);continue;}}

    const pdx=G.px-m.x, pdy=G.py-m.y;
    const dist=Math.abs(pdx)+Math.abs(pdy);

    if(dist===1){mAttack(m);if(G.hp<=0)return;continue;}
    if(dist===0) continue;

    // Range attack
    if(m.mv==='range'&&dist<=5){mAttack(m);if(G.hp<=0)return;continue;}

    let mx=0,my=0;
    if(m.mv==='rand'){const d=[[0,1],[0,-1],[1,0],[-1,0]][Math.floor(Math.random()*4)];mx=d[0];my=d[1];}
    else if(m.mv==='slow'){if(G.turns%2===0){mx=Math.sign(pdx)||0;my=mx?0:Math.sign(pdy);}}
    else if(m.mv==='phase'){mx=Math.sign(pdx)||0;my=mx?0:Math.sign(pdy);}
    else if(m.mv==='boss'){
      // Boss: multi-step chase
      mx=Math.sign(pdx)||0;my=mx?0:Math.sign(pdy);
      if(G.turns%3===0&&dist<=3){mAttack(m);mAttack(m);if(G.hp<=0)return;continue;}
    }
    else{mx=Math.sign(pdx)||0;my=mx?0:Math.sign(pdy);}

    const nx=m.x+mx,ny=m.y+my;
    if(nx>=0&&ny>=0&&nx<GW&&ny<GH&&G.map[ny][nx]!==T.WALL&&!G.monsters.some(o=>o.x===nx&&o.y===ny)&&!(nx===G.px&&ny===G.py)){
      m.x=nx;m.y=ny;
    }
  }
}

function waitTurn() {
  if(G.over||G.won) return;
  addLog('⏳ 대기','ls');
  if(G.cls==='paladin') G.hp=Math.min(G.maxHp,G.hp+G.regen);
  endTurn();
}

function useHpPotion() {
  // Quick-use best available potion
  const pot = G.inv.find(i=>i.t==='potion'&&i.heal);
  if(!pot){addLog('🧪 포션 없음','ls');return;}
  G.hp=Math.min(G.maxHp,G.hp+pot.heal);
  addLog(`🧪 ${pot.n} 사용! HP+${pot.heal}`,'li');
  G.inv=G.inv.filter(i=>i.iid!==pot.iid);
  render();
}

function goStairs() {
  if(G.over||G.won) return;
  if(G.map[G.py][G.px]===T.STAIR) descend();
  else addLog('🪜 계단 위에 있지 않습니다','ls');
}

function descend() {
  if(G.floor>=MAX_FLOOR){addLog('❌ 더 이상 내려갈 수 없습니다','ls');return;}
  G.floor++;
  G.hp=Math.min(G.maxHp,G.hp+Math.floor(G.maxHp*0.25));
  addLog(`🪜 B${G.floor}F으로!`,'ls');
  buildMap();
  render();
}

// ──────────────────────────────────────────────────────────
// ITEMS
// ──────────────────────────────────────────────────────────
function useItem(item) {
  const t=item.t;
  if(t==='potion'){
    if(item.heal){G.hp=Math.min(G.maxHp,G.hp+item.heal);addLog(`🧪 HP+${item.heal}`,'li');}
    if(item.fullheal){G.hp=G.maxHp;addLog('🌿 HP 완전 회복!','li');}
    if(item.patk){G.atk+=item.patk;addLog(`💪 ATK+${item.patk}`,'li');}
    if(item.pspd){G.spd+=item.pspd;addLog(`⚡ SPD+${item.pspd}`,'li');}
    rmInv(item.iid);
  } else if(['weapon','armor','shield','ring','boots','helmet'].includes(t)){
    if(G.equipped[t]) G.inv.push(G.equipped[t]);
    G.equipped[t]=item; rmInv(item.iid);
    addLog(`⚔️ ${item.n} 장착!`,'li');
  } else if(t==='scroll'){
    if(item.dmgAll) G.monsters.forEach(m=>{m.hp-=item.dmgAll;if(m.hp<=0)killMon(m);});
    if(item.freezeAll) G.monsters.forEach(m=>m.frozen=2);
    if(item.revealMap) G.revealed=G.revealed.map(r=>r.map(()=>true));
    if(item.grantDodge) G.dodge=true;
    addLog(`📜 ${item.n} 사용!`,'li');
    rmInv(item.iid);
  } else if(t==='gem'){G.xp+=item.xp;addLog(`💎 XP+${item.xp}`,'li');while(G.xp>=G.xpNext)doLevelUp();rmInv(item.iid);}
    else if(t==='gold'){G.gold+=item.gold;addLog(`💰 +${item.gold}골드`,'li');rmInv(item.iid);}
    else if(t==='curse'){G.hp=Math.floor(G.hp/2);addLog('💀 저주! HP 반감','lm');rmInv(item.iid);if(G.hp<=0)gameDie('저주');}
  render();
}

function rmInv(iid){G.inv=G.inv.filter(i=>i.iid!==iid);}

// ──────────────────────────────────────────────────────────
// SHOP
// ──────────────────────────────────────────────────────────
function openShop() {
  const pool=ITEMS.filter(i=>['potion','scroll','weapon','armor','shield','ring'].includes(i.t));
  const shuffled=[...pool].sort(()=>Math.random()-0.5);
  G.shopStock=shuffled.slice(0,5).map(i=>({...i,iid:i.id+'_s'+Date.now()+Math.random(),price:Math.round(40+Math.random()*160+G.floor*18)}));
  document.getElementById('shop-gold').textContent=G.gold;
  const si=document.getElementById('shop-items');
  si.innerHTML=G.shopStock.map(it=>`
    <div class="shop-item" onclick="buyItem('${it.iid}')">
      <span style="font-size:1.3rem;">${it.e}</span>
      <div style="flex:1;">
        <div class="si-name" style="color:${RAR_COLOR[it.r]||'#fff'};">${it.n}</div>
        <div class="si-desc">${it.desc}</div>
      </div>
      <div class="si-price">💰${it.price}</div>
    </div>
  `).join('');
  document.getElementById('ov-shop').classList.remove('hidden');
}

function buyItem(iid) {
  const it=G.shopStock.find(i=>i.iid===iid);
  if(!it) return;
  if(G.gold<it.price){addLog('💰 골드 부족!','ls');return;}
  if(G.inv.length>=24){addLog('🎒 인벤토리 가득!','ls');return;}
  G.gold-=it.price; G.inv.push(it); G.shopStock=G.shopStock.filter(i=>i.iid!==iid);
  addLog(`🛒 ${it.n} 구매!`,'li');
  document.getElementById('shop-gold').textContent=G.gold;
  openShop(); render();
}

function closeShop(){document.getElementById('ov-shop').classList.add('hidden');}

// ──────────────────────────────────────────────────────────
// INVENTORY UI
// ──────────────────────────────────────────────────────────
function openInv() {
  selInvItem=null;
  drawInv();
  document.getElementById('iinfo').innerHTML='<span style="color:var(--text3);">아이템을 클릭하면 정보가 표시됩니다.</span>';
  document.getElementById('inv-use').style.display='none';
  document.getElementById('inv-drop').style.display='none';
  document.getElementById('ov-inv').classList.remove('hidden');
}

function drawInv() {
  const g=document.getElementById('inv-grid');
  let h='';
  for(let i=0;i<24;i++){
    const it=G.inv[i];
    if(it){
      const eq=Object.values(G.equipped).some(e=>e?.iid===it.iid);
      const sel=selInvItem?.iid===it.iid;
      h+=`<div class="islot${eq?' ieq':''}${sel?' isel':''}" onclick="selInv('${it.iid}')" title="${it.n}">
        ${it.e}<div class="sn">${it.n.slice(0,4)}</div>${eq?'<div class="sb">E</div>':''}
      </div>`;
    } else h+=`<div class="islot" style="opacity:0.2;pointer-events:none;"></div>`;
  }
  g.innerHTML=h;
}

function selInv(iid) {
  selInvItem=G.inv.find(i=>i.iid===iid);
  if(!selInvItem) return;
  const rc=RAR_COLOR[selInvItem.r]||'#fff';
  document.getElementById('iinfo').innerHTML=`
    <span style="font-size:1.4rem;">${selInvItem.e}</span>
    <span style="font-weight:700;color:${rc};margin-left:6px;">${selInvItem.n}</span>
    <span style="font-size:0.65rem;color:${rc};margin-left:4px;">[${selInvItem.r||''}]</span>
    <div style="color:var(--text2);font-size:0.76rem;margin-top:4px;">${selInvItem.desc}</div>
  `;
  document.getElementById('inv-use').style.display='inline-block';
  document.getElementById('inv-drop').style.display='inline-block';
  drawInv();
}

function invUse(){if(!selInvItem)return;closeInv();useItem(selInvItem);}
function invDrop(){
  if(!selInvItem)return;
  addLog(`🗑️ ${selInvItem.n} 버림`,'ls');
  rmInv(selInvItem.iid);selInvItem=null;drawInv();
  document.getElementById('iinfo').innerHTML='<span style="color:var(--text3);">아이템을 클릭하면 정보가 표시됩니다.</span>';
  document.getElementById('inv-use').style.display='none';
  document.getElementById('inv-drop').style.display='none';
  render();
}
function closeInv(){document.getElementById('ov-inv').classList.add('hidden');}

// ──────────────────────────────────────────────────────────
// LEVEL UP STAT
// ──────────────────────────────────────────────────────────
function statUp(s) {
  if(s==='hp'){G.maxHp+=20;G.hp=Math.min(G.maxHp,G.hp+20);}
  if(s==='atk') G.atk+=3;
  if(s==='def') G.def+=2;
  if(s==='spd') G.spd+=2;
  if(s==='crit') G.crit+=5;
  if(s==='regen') G.regen+=2;
  document.getElementById('ov-skill').classList.add('hidden');
  render();
}

// ──────────────────────────────────────────────────────────
// GAME OVER / VICTORY
// ──────────────────────────────────────────────────────────
function buildStats() {
  return `
    <div>📊 레벨 <b style="color:var(--purple);">${G.level}</b></div>
    <div>🏰 B${G.floor}F 도달</div>
    <div>💀 처치 <b style="color:var(--red);">${G.kills}</b></div>
    <div>⏱ ${G.turns}턴</div>
    <div>💰 ${G.gold}골드</div>
    <div>🌟 <b style="color:var(--gold);">${G.score}점</b></div>
  `;
}

function gameDie(cause) {
  G.over=true; G.hp=0;
  document.getElementById('death-cause').textContent=`${cause}에 의해 사망...`;
  document.getElementById('death-stats').innerHTML=buildStats();
  document.getElementById('ov-death').classList.remove('hidden');
  render();
}

function gameWin() {
  G.won=true; G.score+=15000;
  document.getElementById('win-stats').innerHTML=buildStats();
  document.getElementById('ov-win').classList.remove('hidden');
}

function restartGame() {
  document.getElementById('ov-death').classList.add('hidden');
  document.getElementById('ov-win').classList.add('hidden');
  document.getElementById('ov-title').classList.remove('hidden');
  document.getElementById('log-entries').innerHTML='';
  G={};
}

// ──────────────────────────────────────────────────────────
// LOG
// ──────────────────────────────────────────────────────────
function addLog(msg,cls='ls') {
  const el=document.getElementById('log-entries');
  const d=document.createElement('div');
  d.className=`log-e ${cls}`;
  d.textContent=msg;
  el.insertBefore(d,el.firstChild);
  while(el.children.length>100) el.removeChild(el.lastChild);
}

// ──────────────────────────────────────────────────────────
// VISUAL FX
// ──────────────────────────────────────────────────────────
function shakeWrap() {
  const w=document.getElementById('dungeon-wrap');
  w.classList.add('shake');
  setTimeout(()=>w.classList.remove('shake'),320);
}

function popDmg(cx,cy,dmg,color) {
  const w=document.getElementById('dungeon-wrap');
  const d=document.createElement('div');
  d.className='dpop';
  d.style.cssText=`color:${color};left:${cx}px;top:${cy}px;`;
  d.textContent=`-${dmg}`;
  w.appendChild(d);
  setTimeout(()=>d.remove(),850);
}

function lvFX() {
  const el=document.createElement('div');
  el.className='lvup-fx';
  el.textContent='⬆️ LEVEL UP!';
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),1500);
}

// ──────────────────────────────────────────────────────────
// UI FLOW
// ──────────────────────────────────────────────────────────
function gotoClassSelect() {
  const v=document.getElementById('name-input').value.trim();
  if(!v){alert('이름을 입력하세요!');return;}
  document.getElementById('ov-title').classList.add('hidden');
  document.getElementById('ov-class').classList.remove('hidden');
}

function pickClass(cls) {
  selClass=cls;
  document.querySelectorAll('.cc').forEach(c=>c.classList.remove('sel'));
  document.getElementById('cls-'+cls).classList.add('sel');
  const b=document.getElementById('start-btn');
  b.disabled=false;b.style.opacity='1';
}

function backTitle() {
  document.getElementById('ov-class').classList.add('hidden');
  document.getElementById('ov-title').classList.remove('hidden');
}

function startGame() {
  if(!selClass) return;
  const name=document.getElementById('name-input').value.trim()||'용사';
  document.getElementById('ov-class').classList.add('hidden');
  initG(name,selClass);
  buildMap();
  addLog(`⚔️ ${name} 던전 입장!`,'ll');
  addLog('🎮 화살표 이동, 몬스터 인접시 자동공격','ls');
  addLog(`💡 S키: 스킬 | H키: 포션 | I키: 인벤`,'ls');
  render();
}

// ──────────────────────────────────────────────────────────
// KEYBOARD
// ──────────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
  if(G.over||G.won) return;
  if(!G.map||!G.map.length) return;

  const mods=['ov-inv','ov-shop','ov-skill'];
  const anyOpen=mods.some(id=>!document.getElementById(id).classList.contains('hidden'));
  if(anyOpen) {
    if(e.key==='Escape'||e.key==='i'||e.key==='I') {closeInv();closeShop();}
    return;
  }

  const dirMap={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0],
    'w':[0,-1],'s_move':[0,1],'a':[-1,0],'d':[1,0]};

  if(e.key==='ArrowUp'||e.key==='ArrowDown'||e.key==='ArrowLeft'||e.key==='ArrowRight') {
    e.preventDefault();
    const [dx,dy]={ArrowUp:[0,-1],ArrowDown:[0,1],ArrowLeft:[-1,0],ArrowRight:[1,0]}[e.key];
    move(dx,dy);
  } else if(e.key===' ') {
    e.preventDefault();
    if(G.map[G.py]?.[G.px]===T.STAIR) descend(); else waitTurn();
  } else if(e.key==='i'||e.key==='I') {openInv();
  } else if(e.key==='s'||e.key==='S') {useSkill();
  } else if(e.key==='h'||e.key==='H') {useHpPotion();
  } else if(e.key==='.') {goStairs();}
});

document.getElementById('name-input').addEventListener('keydown',e=>{if(e.key==='Enter')gotoClassSelect();});

// Resize canvas on window resize
function resizeCanvas() {
  const wrap=document.getElementById('dungeon-wrap');
  const maxW=wrap.clientWidth, maxH=wrap.clientHeight;
  const scaleX=maxW/(GW*CS), scaleY=maxH/(GH*CS);
  const scale=Math.min(scaleX,scaleY,1);
  canvas.style.width=(GW*CS*scale)+'px';
  canvas.style.height=(GH*CS*scale)+'px';
}
window.addEventListener('resize',()=>{resizeCanvas();if(G.map)render();});
resizeCanvas();
</script>
</body>
</html>
