import streamlit as st
import streamlit.components.v1 as components

def render():
    # 💡 주의: app.py 메인 파일에서 이미 st.set_page_config()를 설정했다면 
    # 에러가 날 수 있으니 아래 줄은 주석 처리하거나 지워주세요!
    # st.set_page_config(layout="wide")
    
    st.title("던전파이터 REBORN ⚔️")

    # 1. HTML 코드를 삼중 따옴표(""")로 묶어서 문자열 변수에 저장합니다.
    game_html_code = """
    
    <!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>던전파이터 REBORN</title>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#000;overflow:hidden;font-family:'Noto Sans KR',sans-serif;}
#gameCanvas{display:block;image-rendering:pixelated;}
#ui{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;}

/* HUD */
#hud{position:absolute;top:0;left:0;right:0;height:64px;background:linear-gradient(180deg,rgba(0,0,0,.95),transparent);padding:8px 16px;display:flex;align-items:center;gap:16px;}
#char-portrait{width:48px;height:48px;border:2px solid #c8a800;border-radius:4px;background:#1a1208;display:flex;align-items:center;justify-content:center;font-size:28px;flex-shrink:0;position:relative;}
#char-portrait::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,220,50,.1),transparent);border-radius:2px;}
#bars{display:flex;flex-direction:column;gap:4px;flex:0 0 220px;}
.bar-wrap{position:relative;height:14px;background:rgba(0,0,0,.8);border:1px solid rgba(255,255,255,.15);border-radius:2px;overflow:hidden;}
.bar-fill{height:100%;border-radius:2px;transition:width .12s;}
#hp-bar{background:linear-gradient(90deg,#8b0000,#dc143c,#ff4466);}
#mp-bar{background:linear-gradient(90deg,#00008b,#1e56dc,#44aaff);}
#xp-bar{background:linear-gradient(90deg,#006400,#32cd32);}
.bar-label{position:absolute;left:6px;top:50%;transform:translateY(-50%);font-size:.48rem;color:rgba(255,255,255,.8);font-weight:700;letter-spacing:1px;z-index:2;text-shadow:1px 1px 0 #000;}
.bar-val{position:absolute;right:6px;top:50%;transform:translateY(-50%);font-size:.44rem;color:rgba(255,255,255,.7);z-index:2;text-shadow:1px 1px 0 #000;}
#stats{display:flex;gap:6px;margin-left:8px;}
.stat{background:rgba(0,0,0,.7);border:1px solid rgba(200,168,0,.3);border-radius:3px;padding:2px 8px;text-align:center;min-width:42px;}
.stat-val{font-family:'Black Han Sans',sans-serif;font-size:.9rem;color:#f5c842;}
.stat-lbl{font-size:.38rem;color:#666;letter-spacing:.5px;}
#floor-badge{margin-left:auto;background:rgba(0,0,0,.8);border:1px solid #c8a800;border-radius:3px;padding:4px 14px;font-family:'Black Han Sans',sans-serif;font-size:.8rem;color:#f5c842;letter-spacing:3px;}
#kill-counter{position:absolute;top:68px;right:16px;font-family:'Black Han Sans',sans-serif;font-size:.75rem;color:#888;letter-spacing:2px;}

/* BOSS HP */
#boss-ui{position:absolute;top:68px;left:50%;transform:translateX(-50%);width:420px;opacity:0;transition:opacity .4s;pointer-events:none;}
#boss-ui.visible{opacity:1;}
#boss-name{font-family:'Black Han Sans',sans-serif;font-size:.85rem;color:#ff3344;text-align:center;margin-bottom:4px;text-shadow:0 0 12px rgba(255,0,50,.8);letter-spacing:3px;}
#boss-hp-wrap{height:12px;background:rgba(0,0,0,.8);border:1px solid rgba(255,50,70,.4);border-radius:2px;overflow:hidden;position:relative;}
#boss-hp-fill{height:100%;background:linear-gradient(90deg,#550000,#cc0022,#ff2244);transition:width .1s;}
#boss-phase{text-align:center;font-size:.44rem;color:#ff7788;letter-spacing:4px;margin-top:3px;}

/* SKILL BAR */
#skillbar{position:absolute;bottom:0;left:0;right:0;height:72px;background:linear-gradient(0deg,rgba(0,0,0,.97),rgba(0,0,0,.7));border-top:1px solid rgba(200,168,0,.2);display:flex;align-items:center;justify-content:center;gap:6px;padding:8px 12px;}
.sk{width:52px;height:52px;border-radius:4px;background:rgba(20,15,5,.9);border:1px solid rgba(200,168,0,.25);position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:default;}
.sk.ready{border-color:rgba(200,168,0,.8);box-shadow:0 0 12px rgba(200,168,0,.3),inset 0 0 8px rgba(200,168,0,.05);}
.sk.active{border-color:#fff;box-shadow:0 0 20px rgba(255,255,255,.6);}
.sk-icon{font-size:1.5rem;line-height:1;}
.sk-key{position:absolute;bottom:2px;right:3px;font-size:.36rem;color:#555;}
.sk-mp{position:absolute;top:2px;left:3px;font-size:.35rem;color:#4488ff;}
.sk-cd{position:absolute;inset:0;background:rgba(0,0,0,.82);border-radius:4px;display:flex;align-items:center;justify-content:center;font-family:'Black Han Sans',sans-serif;font-size:.72rem;color:#c8a800;}
.ctrl{position:absolute;right:14px;font-size:.45rem;color:#2a2520;line-height:2;text-align:right;}

/* COMBO */
#combo{position:absolute;top:80px;right:18px;text-align:right;pointer-events:none;opacity:0;transition:opacity .2s;}
#combo-num{font-family:'Black Han Sans',sans-serif;font-size:3rem;line-height:1;text-shadow:3px 3px 0 rgba(0,0,0,.8);}
#combo-lbl{font-size:.55rem;color:#f5c842;letter-spacing:5px;}

/* OVERLAYS */
.ov{position:fixed;inset:0;z-index:100;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,.95);}
.ov.hidden{display:none;}

/* TITLE */
#title-ov{flex-direction:column;align-items:center;}
.game-logo{font-family:'Black Han Sans',sans-serif;font-size:4rem;letter-spacing:6px;line-height:1;text-align:center;position:relative;}
.logo-main{display:block;background:linear-gradient(135deg,#ff6600,#ffcc00,#ff8800);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 40px rgba(255,150,0,.5));}
.logo-sub{display:block;font-size:1rem;letter-spacing:16px;color:#444;margin-top:-4px;}
.logo-eng{display:block;font-size:.7rem;letter-spacing:8px;color:#2a2520;margin-top:6px;}
.class-select{display:flex;gap:8px;margin:28px 0 20px;flex-wrap:wrap;justify-content:center;}
.cls-card{width:100px;background:rgba(10,8,2,.95);border:1px solid rgba(200,168,0,.1);border-radius:6px;padding:12px 6px;cursor:pointer;transition:all .18s;text-align:center;position:relative;overflow:hidden;}
.cls-card::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,150,0,.03),transparent);opacity:0;transition:opacity .18s;}
.cls-card:hover,.cls-card.sel{border-color:rgba(200,168,0,.8);box-shadow:0 0 24px rgba(200,168,0,.2);}
.cls-card:hover::before,.cls-card.sel::before{opacity:1;}
.cls-card.sel{background:rgba(20,15,0,.98);}
.cls-emoji{font-size:2.4rem;display:block;margin-bottom:6px;}
.cls-name{font-family:'Black Han Sans',sans-serif;font-size:.72rem;color:#c8a800;letter-spacing:1px;}
.cls-type{font-size:.42rem;color:#444;margin-top:3px;}
.cls-tags{display:flex;flex-wrap:wrap;gap:2px;justify-content:center;margin-top:5px;}
.tag{font-size:.36rem;padding:1px 4px;border-radius:2px;background:rgba(255,255,255,.05);color:#555;}
.tag.high{color:#ff6644;background:rgba(255,100,50,.08);}
.start-btn{padding:14px 60px;background:linear-gradient(135deg,#6b2800,#ff5500,#ff8800);border:none;border-radius:3px;color:#fff;font-family:'Black Han Sans',sans-serif;font-size:1rem;letter-spacing:5px;cursor:pointer;box-shadow:0 0 30px rgba(255,100,0,.4);transition:all .2s;position:relative;}
.start-btn:not(:disabled):hover{transform:scale(1.05);filter:brightness(1.2);}
.start-btn:disabled{opacity:.2;cursor:default;}
.key-hint{font-size:.48rem;color:#2a2520;margin-top:12px;letter-spacing:2px;}

/* RESULT */
.result-panel{background:rgba(5,3,0,.99);border:1px solid rgba(200,168,0,.2);border-radius:6px;padding:32px 40px;min-width:360px;text-align:center;}
.result-title{font-family:'Black Han Sans',sans-serif;font-size:2rem;letter-spacing:4px;margin-bottom:18px;}
.result-clear{color:#f5c842;text-shadow:0 0 20px rgba(245,200,66,.4);}
.result-over{color:#ff2233;text-shadow:0 0 20px rgba(255,30,50,.4);}
.result-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:12px 0;text-align:left;}
.rc{font-size:.7rem;color:#555;display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid rgba(255,255,255,.04);}
.rc b{color:#c8a800;}
.btn-row{display:flex;gap:8px;justify-content:center;margin-top:16px;}
.gbtn{padding:10px 24px;border:none;border-radius:3px;cursor:pointer;font-family:'Black Han Sans',sans-serif;font-size:.78rem;letter-spacing:2px;transition:all .15s;}
.gbtn:hover{transform:translateY(-2px);}
.gbtn-ok{background:linear-gradient(135deg,#1a5500,#33bb00);color:#fff;}
.gbtn-retry{background:linear-gradient(135deg,#550000,#cc2200);color:#fff;}
.gbtn-gray{background:rgba(255,255,255,.06);color:#666;border:1px solid rgba(255,255,255,.08);}

/* SHOP */
#shop-ov{flex-direction:column;}
.shop-title{font-family:'Black Han Sans',sans-serif;font-size:1.8rem;color:#f5c842;letter-spacing:4px;margin-bottom:4px;}
.shop-gold{font-size:.75rem;color:#888;margin-bottom:16px;}
.shop-gold span{color:#f5c842;font-weight:900;}
.shop-grid{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;max-width:680px;}
.shop-item{width:110px;background:rgba(10,8,2,.98);border:1px solid rgba(200,168,0,.1);border-radius:4px;padding:10px 6px;cursor:pointer;text-align:center;transition:all .15s;}
.shop-item:hover:not(.cant){border-color:rgba(200,168,0,.7);background:rgba(20,15,0,.99);}
.shop-item.cant{opacity:.3;cursor:default;}
.si-icon{font-size:1.8rem;margin-bottom:4px;}
.si-name{font-size:.62rem;color:#aaa;font-weight:700;}
.si-desc{font-size:.48rem;color:#444;margin:3px 0;}
.si-price{font-size:.7rem;color:#f5c842;font-weight:900;margin-top:5px;}

/* LVL UP */
#lvl-ov{flex-direction:column;}
.lvl-title{font-family:'Black Han Sans',sans-serif;font-size:2.2rem;color:#f5c842;letter-spacing:4px;margin-bottom:8px;}
.lvl-sub{font-size:.72rem;color:#555;margin-bottom:16px;}
.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;}
.spbtn{padding:12px 10px;border:1px solid rgba(200,168,0,.2);border-radius:4px;background:rgba(10,8,2,.9);cursor:pointer;font-size:.75rem;color:#aaa;transition:all .15s;font-family:'Noto Sans KR',sans-serif;}
.spbtn:hover{border-color:#f5c842;background:rgba(20,15,0,.99);color:#f5c842;}

/* PAUSE */
#pause-ov{background:rgba(0,0,0,.8);}
.pause-txt{font-family:'Black Han Sans',sans-serif;font-size:3rem;color:#fff;letter-spacing:8px;text-align:center;}
.pause-sub{font-size:.65rem;color:#333;margin-top:12px;letter-spacing:3px;text-align:center;}

/* BOSS WARNING */
@keyframes bossWarn{0%,100%{opacity:0;transform:translate(-50%,-50%) scale(.85);}40%,60%{opacity:1;transform:translate(-50%,-50%) scale(1);}}
#boss-warn{position:fixed;top:45%;left:50%;z-index:200;display:none;font-family:'Black Han Sans',sans-serif;font-size:2.8rem;color:#ff0000;text-shadow:0 0 40px rgba(255,0,0,1);letter-spacing:6px;text-align:center;animation:bossWarn 2.5s ease forwards;pointer-events:none;}

/* HIT FLASH */
#hit-flash{position:fixed;inset:0;pointer-events:none;z-index:50;opacity:0;transition:opacity .06s;background:radial-gradient(ellipse at center,transparent 40%,rgba(255,0,0,.35) 100%);}

/* DMGNUMS */
@keyframes dmgFloat{0%{opacity:1;transform:translateY(0) scale(1);}80%{opacity:.8;}100%{opacity:0;transform:translateY(-80px) scale(.7);}}
.dmg{position:fixed;pointer-events:none;font-family:'Black Han Sans',sans-serif;animation:dmgFloat 1s ease forwards;z-index:300;text-shadow:2px 2px 0 rgba(0,0,0,.9),0 0 10px currentColor;}

/* ACHIVEMENT */
@keyframes achIn{from{transform:translateX(-50%) translateY(-70px);}to{transform:translateX(-50%) translateY(0);}}
#achievement{position:fixed;top:70px;left:50%;transform:translateX(-50%) translateY(-70px);background:rgba(20,14,0,.97);border:1px solid rgba(200,168,0,.5);border-radius:4px;padding:8px 20px;display:flex;align-items:center;gap:10px;z-index:200;pointer-events:none;box-shadow:0 4px 20px rgba(200,168,0,.25);}
#achievement.show{animation:achIn .35s ease forwards;}
#ach-ico{font-size:1.4rem;}
#ach-t{font-size:.65rem;color:#f5c842;font-weight:900;}
#ach-s{font-size:.5rem;color:#664400;}

::-webkit-scrollbar{width:0;}
</style>
</head>
<body>
<canvas id="gameCanvas"></canvas>
<div id="ui">
  <!-- HUD -->
  <div id="hud">
    <div id="char-portrait">⚔️</div>
    <div id="bars">
      <div class="bar-wrap"><div class="bar-fill" id="hp-bar" style="width:100%"></div><span class="bar-label">HP</span><span class="bar-val" id="hp-val">500/500</span></div>
      <div class="bar-wrap"><div class="bar-fill" id="mp-bar" style="width:100%"></div><span class="bar-label">MP</span></div>
      <div class="bar-wrap" style="height:8px"><div class="bar-fill" id="xp-bar" style="width:0%"></div></div>
    </div>
    <div id="stats">
      <div class="stat"><div class="stat-val" id="s-lv">1</div><div class="stat-lbl">LV</div></div>
      <div class="stat"><div class="stat-val" id="s-atk" style="color:#ff8866">0</div><div class="stat-lbl">ATK</div></div>
      <div class="stat"><div class="stat-val" id="s-def" style="color:#66aaff">0</div><div class="stat-lbl">DEF</div></div>
      <div class="stat"><div class="stat-val" id="s-gold" style="color:#f5c842">0</div><div class="stat-lbl">GOLD</div></div>
      <div class="stat"><div class="stat-val" id="s-score">0</div><div class="stat-lbl">SCORE</div></div>
    </div>
    <div id="floor-badge">1F</div>
  </div>
  <div id="kill-counter"></div>

  <!-- BOSS -->
  <div id="boss-ui">
    <div id="boss-name">BOSS</div>
    <div id="boss-hp-wrap"><div id="boss-hp-fill"></div></div>
    <div id="boss-phase"></div>
  </div>

  <!-- COMBO -->
  <div id="combo"><div id="combo-num">0</div><div id="combo-lbl">COMBO</div></div>

  <!-- SKILL BAR -->
  <div id="skillbar">
    <div id="sk-slots"></div>
    <div class="ctrl">←→ 이동 | Z 점프(2단)<br>X 기본공격 | A~G 스킬<br>SPACE 회피 | P 일시정지</div>
  </div>

  <!-- HIT FLASH -->
  <div id="hit-flash"></div>
  <!-- BOSS WARN -->
  <div id="boss-warn"></div>
  <!-- ACHIEVEMENT -->
  <div id="achievement"><div id="ach-ico">🏆</div><div><div id="ach-t"></div><div id="ach-s"></div></div></div>

  <!-- TITLE -->
  <div class="ov" id="title-ov">
    <div style="text-align:center">
      <div class="game-logo">
        <span class="logo-main">던전파이터</span>
        <span class="logo-sub">REBORN</span>
        <span class="logo-eng">DUNGEON FIGHTER · REBORN</span>
      </div>
      <div class="class-select" id="class-select"></div>
      <button class="start-btn" id="start-btn" disabled onclick="startGame()">전투 시작 ▶</button>
      <div class="key-hint">클래스를 선택하세요</div>
    </div>
  </div>

  <!-- LEVEL UP -->
  <div class="ov hidden" id="lvl-ov">
    <div style="text-align:center">
      <div class="lvl-title">⬆ LEVEL UP!</div>
      <div class="lvl-sub">스탯을 선택하세요</div>
      <div class="stat-grid" id="stat-grid"></div>
    </div>
  </div>

  <!-- SHOP -->
  <div class="ov hidden" id="shop-ov">
    <div style="text-align:center">
      <div class="shop-title">⚗ 상점</div>
      <div class="shop-gold">보유 골드: <span id="sg-val">0</span></div>
      <div class="shop-grid" id="shop-grid"></div>
      <div style="margin-top:16px"><button class="gbtn gbtn-ok" onclick="nextStage()">다음 스테이지 →</button></div>
    </div>
  </div>

  <!-- CLEAR -->
  <div class="ov hidden" id="clear-ov">
    <div class="result-panel">
      <div class="result-title result-clear">✦ STAGE CLEAR ✦</div>
      <div class="result-grid" id="clear-grid"></div>
      <div class="btn-row">
        <button class="gbtn gbtn-ok" onclick="openShop()">상점 →</button>
        <button class="gbtn gbtn-gray" onclick="gotoTitle()">타이틀</button>
      </div>
    </div>
  </div>

  <!-- OVER -->
  <div class="ov hidden" id="over-ov">
    <div class="result-panel">
      <div class="result-title result-over">💀 GAME OVER</div>
      <div class="result-grid" id="over-grid"></div>
      <div class="btn-row">
        <button class="gbtn gbtn-retry" onclick="retryStage()">재도전 ↺</button>
        <button class="gbtn gbtn-gray" onclick="gotoTitle()">타이틀</button>
      </div>
    </div>
  </div>

  <!-- PAUSE -->
  <div class="ov hidden" id="pause-ov">
    <div><div class="pause-txt">⏸ PAUSE</div><div class="pause-sub">P 키 · 계속</div></div>
  </div>
</div>

<script>
'use strict';
// ═══════════════════════════════════════════════════════
//  던전파이터 REBORN — 완전 리빌드
//  픽셀아트 스타일 스프라이트 + 타격감 중심 설계
// ═══════════════════════════════════════════════════════

const CV = document.getElementById('gameCanvas');
const CX = CV.getContext('2d');

function resize(){
  CV.width = window.innerWidth;
  CV.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

const W = ()=>CV.width, H = ()=>CV.height;
const GY = ()=>H()-72; // ground y

// ═══ INPUT ═══
const KEY={}, JK={};
addEventListener('keydown',e=>{if(!KEY[e.key]){KEY[e.key]=true;JK[e.key]=true;}e.preventDefault();});
addEventListener('keyup',e=>{KEY[e.key]=false;});
function clearJK(){for(const k in JK) delete JK[k];}

// ═══ AUDIO ═══
let AC=null;
function ac(){if(!AC)try{AC=new(AudioContext||webkitAudioContext)();}catch(e){}return AC;}
function beep(freq,type,dur,vol=.25,delay=0){
  const a=ac();if(!a)return;
  try{
    const o=a.createOscillator(),g=a.createGain();
    o.connect(g);g.connect(a.destination);
    o.type=type;o.frequency.value=freq;
    const t=a.currentTime+delay;
    g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(vol,t+.004);
    g.gain.exponentialRampToValueAtTime(.001,t+dur);
    o.start(t);o.stop(t+dur+.05);
  }catch(e){}
}
const SFX={
  hit:()=>{ beep(120,'square',.04,.4); beep(80,'sawtooth',.06,.3,.02); },
  crit:()=>{ beep(200,'square',.03,.5); beep(300,'sawtooth',.05,.4,.02); beep(180,'square',.08,.3,.04); },
  jump:()=>beep(340,'sine',.09,.15),
  skill:()=>{ beep(440,'sine',.06,.2); beep(660,'sine',.1,.2,.05); },
  death:()=>{ for(let i=0;i<5;i++) beep(150-i*20,'sawtooth',.3,.4,i*.08); },
  clear:()=>{ [523,659,784,1047].forEach((f,i)=>beep(f,'sine',.3,.35,i*.1)); },
  boss:()=>{ for(let i=0;i<4;i++) beep(55+i*12,'sawtooth',.5,.5,i*.25); },
  buy:()=>{ beep(660,'sine',.12,.25); beep(880,'sine',.1,.2,.1); },
  lvl:()=>{ [523,659,784,523,659,784,1047].forEach((f,i)=>beep(f,'sine',.22,.35,i*.09)); },
  dodge:()=>beep(500,'sine',.06,.12),
};

// ═══ PARTICLES ═══
const PARTS=[];
function spark(x,y,opts={}){
  const n=opts.n||8;
  for(let i=0;i<n;i++){
    const a=(opts.dir||0)+(Math.random()-.5)*(opts.spread||Math.PI*2);
    const s=(opts.smin||1)+Math.random()*(opts.smax||5);
    const col=Array.isArray(opts.col)?opts.col[~~(Math.random()*opts.col.length)]:(opts.col||'#fff');
    PARTS.push({
      x,y,vx:Math.cos(a)*s+(opts.vxb||0),vy:Math.sin(a)*s-(opts.ub||0),
      life:1,dec:(opts.dmin||.02)+Math.random()*(opts.dmax||.03),
      col,sz:(opts.szmin||2)+Math.random()*(opts.szmax||5),
      glow:opts.glow||false,grav:opts.grav!==undefined?opts.grav:.18,
      type:opts.sq?'sq':'c',
    });
  }
}
function tickParts(dt){
  for(let i=PARTS.length-1;i>=0;i--){
    const p=PARTS[i];
    p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=p.grav*dt;p.vx*=.93;
    p.life-=p.dec*dt;
    if(p.life<=0) PARTS.splice(i,1);
  }
}
function drawParts(cam){
  CX.save();
  for(const p of PARTS){
    const sx=p.x-cam;
    if(sx<-60||sx>W()+60) continue;
    CX.globalAlpha=Math.max(0,p.life);
    if(p.glow){CX.shadowColor=p.col;CX.shadowBlur=p.sz*2.5;}
    CX.fillStyle=p.col;
    if(p.type==='sq') CX.fillRect(sx-p.sz/2,p.y-p.sz/2,p.sz,p.sz);
    else{CX.beginPath();CX.arc(sx,p.y,p.sz,0,Math.PI*2);CX.fill();}
    if(p.glow) CX.shadowBlur=0;
  }
  CX.globalAlpha=1;CX.restore();
}

// ═══ PIXEL SPRITE RENDERER ═══
// 던파 스타일 픽셀 스프라이트 (16x32 기준 스케일업)
const PX=4; // pixel size

function px(ctx, x, y, col){
  ctx.fillStyle=col;
  ctx.fillRect(x*PX, y*PX, PX, PX);
}

// 캐릭터 스프라이트 정의 (픽셀 좌표)
// 각 클래스별로 색상 팔레트가 다름
function drawSprite(ctx, sprite, ox, oy, flipX=false, alpha=1, glowCol=null){
  ctx.save();
  if(alpha!==1) ctx.globalAlpha=alpha;
  if(glowCol){ctx.shadowColor=glowCol;ctx.shadowBlur=16;}
  ctx.translate(ox, oy);
  if(flipX){ ctx.scale(-1,1); ctx.translate(-sprite.w*PX, 0); }
  sprite.draw(ctx);
  if(glowCol) ctx.shadowBlur=0;
  ctx.restore();
}

// ── 워리어 스프라이트 ──
function makeWarriorSprite(pal, frame=0, action='idle'){
  const w=14, h=28;
  const f = frame;
  return {
    w, h,
    draw(ctx){
      const {body,legs,hair,skin,armor,weapon}=pal;
      const legOff = action==='walk'?[Math.sin(f*.5)*2,Math.sin(f*.5+Math.PI)*2]:[0,0];
      const armOff = action==='atk'?Math.sin(f*1.2)*4:0;
      const bodyBob = action==='walk'?Math.abs(Math.sin(f*.5))*.5:0;

      // Shadow
      ctx.fillStyle='rgba(0,0,0,.3)';
      ctx.beginPath();ctx.ellipse(w/2*PX,(h)*PX,w/3*PX,PX,0,0,Math.PI*2);ctx.fill();

      // Legs
      px(ctx,3,h-8+legOff[0]|0,legs); px(ctx,4,h-8+legOff[0]|0,legs);
      px(ctx,3,h-7+legOff[0]|0,legs); px(ctx,4,h-7+legOff[0]|0,legs);
      px(ctx,3,h-6+legOff[0]|0,legs); px(ctx,4,h-6+legOff[0]|0,legs);
      px(ctx,3,h-5+legOff[0]|0,'#222'); px(ctx,4,h-5+legOff[0]|0,'#222'); // boot
      px(ctx,7,h-8+legOff[1]|0,legs); px(ctx,8,h-8+legOff[1]|0,legs);
      px(ctx,7,h-7+legOff[1]|0,legs); px(ctx,8,h-7+legOff[1]|0,legs);
      px(ctx,7,h-6+legOff[1]|0,legs); px(ctx,8,h-6+legOff[1]|0,legs);
      px(ctx,7,h-5+legOff[1]|0,'#222'); px(ctx,8,h-5+legOff[1]|0,'#222');

      const yb=bodyBob|0;
      // Belt
      for(let x=3;x<=10;x++) px(ctx,x,h-9+yb,'#5a4020');

      // Torso/Armor
      for(let x=3;x<=10;x++) for(let y=h-17;y<=h-10;y++) px(ctx,x,y+yb,armor);
      // Armor details
      px(ctx,6,h-15+yb,'#445566'); px(ctx,7,h-15+yb,'#445566');
      px(ctx,5,h-14+yb,'#445566'); px(ctx,6,h-14+yb,'#334455'); px(ctx,7,h-14+yb,'#334455'); px(ctx,8,h-14+yb,'#445566');

      // Shoulder pads
      for(let y=h-17;y<=h-14;y++){px(ctx,2,y+yb,'#6a7a8a');px(ctx,11,y+yb,'#6a7a8a');}

      // Right arm (weapon arm)
      const ra = armOff|0;
      px(ctx,11,h-16+yb-ra,skin); px(ctx,12,h-16+yb-ra,skin);
      px(ctx,11,h-15+yb-ra,skin); px(ctx,12,h-15+yb-ra,skin);
      px(ctx,11,h-14+yb+ra/2|0,skin); px(ctx,12,h-14+yb+ra/2|0,skin);
      // Sword
      ctx.fillStyle='#c8d8f0';
      ctx.fillRect(12*PX,(h-22+yb-ra)*PX,PX,8*PX);
      ctx.fillStyle='#c0a030';
      ctx.fillRect(11*PX,(h-15+yb-ra)*PX,3*PX,PX); // guard

      // Left arm (shield)
      px(ctx,1,h-16+yb,skin); px(ctx,2,h-16+yb,skin);
      px(ctx,1,h-15+yb,skin); px(ctx,2,h-15+yb,skin);
      // Shield
      ctx.fillStyle='#2a3d5a';
      ctx.fillRect(0,(h-17+yb)*PX,2*PX,6*PX);
      ctx.fillStyle='#c0a030';
      ctx.fillRect(0,(h-14+yb)*PX,2*PX,PX);

      // Neck
      px(ctx,6,h-18+yb,skin); px(ctx,7,h-18+yb,skin);

      // Head
      for(let x=4;x<=9;x++) for(let y=h-25;y<=h-19;y++) px(ctx,x,y+yb,skin);
      // Helmet
      ctx.fillStyle='#556677';
      for(let x=4;x<=9;x++) for(let y=h-27;y<=h-24;y++) ctx.fillRect(x*PX,(y+yb)*PX,PX,PX);
      ctx.fillStyle='#445566';
      for(let x=3;x<=10;x++) ctx.fillRect(x*PX,(h-24+yb)*PX,PX,PX);
      // Visor slit
      ctx.fillStyle='rgba(100,200,255,.6)';
      for(let x=5;x<=8;x++) ctx.fillRect(x*PX,(h-22+yb)*PX,PX,PX);

      // Eyes
      px(ctx,5,h-22+yb,'#88ccff'); px(ctx,8,h-22+yb,'#88ccff');
    }
  };
}

function makeMageSprite(pal, frame=0, action='idle'){
  const w=12, h=26;
  const f=frame;
  return {
    w,h,
    draw(ctx){
      const {robe,accent,skin,hair}=pal;
      const bob=action==='idle'?Math.sin(f*.08)*1.5:0;
      const armSwing=action==='atk'?Math.sin(f*1.5)*5:0;
      const yb=bob|0;

      ctx.fillStyle='rgba(0,0,0,.25)';
      ctx.beginPath();ctx.ellipse(w/2*PX,(h+1)*PX,w/3*PX,PX*.6,0,0,Math.PI*2);ctx.fill();

      // Robe (floating effect)
      for(let x=2;x<=9;x++) for(let y=h-14;y<=h;y++) px(ctx,x,y+yb,robe);
      // Robe gradient effect
      ctx.fillStyle='rgba(0,0,0,.2)';
      for(let x=2;x<=9;x++) ctx.fillRect(x*PX,(h+yb)*PX,PX,PX*.5);
      // Robe trim
      ctx.fillStyle=accent;
      for(let x=2;x<=9;x++) ctx.fillRect(x*PX,(h-14+yb)*PX,PX,PX);
      for(let x=2;x<=9;x++) ctx.fillRect(x*PX,(h+yb)*PX,PX,PX*.8);

      // Body under robe
      for(let x=3;x<=8;x++) for(let y=h-20;y<=h-15;y++) px(ctx,x,y+yb,robe);

      // Left arm + staff
      const la = armSwing|0;
      px(ctx,1,h-19+yb-la,skin); px(ctx,1,h-18+yb-la,skin);
      // Staff
      ctx.fillStyle='#6633aa';
      ctx.fillRect(0,(h-24+yb-la)*PX,PX,10*PX);
      ctx.fillStyle=accent;ctx.shadowColor=accent;ctx.shadowBlur=10;
      ctx.beginPath();ctx.arc(PX*.5,(h-24+yb-la)*PX,PX*1.5,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;
      // Orb glow pulse
      ctx.globalAlpha=(0.3+Math.sin(f*.12)*.15);
      ctx.fillStyle=accent;ctx.shadowColor=accent;ctx.shadowBlur=20;
      ctx.beginPath();ctx.arc(PX*.5,(h-24+yb-la)*PX,PX*2.5,0,Math.PI*2);ctx.fill();
      ctx.shadowBlur=0;ctx.globalAlpha=1;

      // Right arm
      px(ctx,10,h-19+yb+la/2|0,skin); px(ctx,10,h-18+yb+la/2|0,skin);

      // Neck
      px(ctx,5,h-21+yb,skin); px(ctx,6,h-21+yb,skin);

      // Head
      for(let x=3;x<=8;x++) for(let y=h-28;y<=h-22;y++) px(ctx,x,y+yb,skin);
      // Wizard hat
      ctx.fillStyle='#33006a';
      for(let x=2;x<=9;x++) ctx.fillRect(x*PX,(h-28+yb)*PX,PX,PX);
      ctx.fillStyle='#440088';
      for(let x=4;x<=7;x++) ctx.fillRect(x*PX,(h-31+yb)*PX,PX,3*PX);
      ctx.fillStyle='#5500aa';
      for(let x=5;x<=6;x++) ctx.fillRect(x*PX,(h-34+yb)*PX,PX,4*PX);
      // Hat tip
      ctx.fillStyle=accent;ctx.shadowColor=accent;ctx.shadowBlur=8;
      ctx.fillRect(5*PX,(h-35+yb)*PX,PX*2,PX*2);ctx.shadowBlur=0;
      // Eyes
      ctx.fillStyle=accent;
      px(ctx,4,h-26+yb,'#aa55ff'); px(ctx,7,h-26+yb,'#aa55ff');
    }
  };
}

function makeRogueSprite(pal, frame=0, action='idle'){
  const w=11, h=24;
  const f=frame;
  return {
    w,h,
    draw(ctx){
      const {body,legs,skin,accent}=pal;
      const legOff=action==='walk'?[Math.sin(f*.6)*2.5,Math.sin(f*.6+Math.PI)*2.5]:[0,0];
      const armSwing=action==='atk'?Math.sin(f*1.8)*6:0;
      const dash=action==='dash'?1:0;

      ctx.fillStyle='rgba(0,0,0,.25)';
      ctx.beginPath();ctx.ellipse(w/2*PX,(h+1)*PX,w/3*PX,PX*.6,0,0,Math.PI*2);ctx.fill();

      // Legs
      for(let y=h-6;y<=h;y++){
        px(ctx,2,y+legOff[0]|0,legs); px(ctx,3,y+legOff[0]|0,legs);
        px(ctx,7,y+legOff[1]|0,legs); px(ctx,8,y+legOff[1]|0,legs);
      }
      px(ctx,2,h+legOff[0]|0,'#111'); px(ctx,3,h+legOff[0]|0,'#111');
      px(ctx,7,h+legOff[1]|0,'#111'); px(ctx,8,h+legOff[1]|0,'#111');

      // Torso
      for(let x=1;x<=9;x++) for(let y=h-15;y<=h-7;y++) px(ctx,x,y,body);
      // Hood cloak
      ctx.fillStyle='rgba(10,20,10,.6)';
      for(let x=0;x<=10;x++) ctx.fillRect(x*PX,(h-15)*PX,PX,6*PX);

      // Dual blades
      const la=armSwing|0;
      // Left dagger
      ctx.fillStyle='#88ccaa';
      ctx.fillRect(0,(h-18-la)*PX,PX,8*PX);
      ctx.fillStyle=accent;ctx.fillRect(0,(h-11-la)*PX,2*PX,PX);
      // Right dagger
      ctx.fillStyle='#88ccaa';
      ctx.fillRect(10*PX,(h-18+la)*PX,PX,8*PX);
      ctx.fillStyle=accent;ctx.fillRect(9*PX,(h-11+la)*PX,2*PX,PX);

      // Arms
      px(ctx,0,h-16-la/2|0,skin); px(ctx,0,h-15-la/2|0,skin);
      px(ctx,10,h-16+la/2|0,skin); px(ctx,10,h-15+la/2|0,skin);

      // Head
      for(let x=2;x<=8;x++) for(let y=h-22;y<=h-16;y++) px(ctx,x,y,skin);
      // Hood
      ctx.fillStyle='#152215';
      for(let x=1;x<=9;x++) ctx.fillRect(x*PX,(h-23)*PX,PX,5*PX);
      ctx.fillRect(0,(h-22)*PX,PX,3*PX);
      ctx.fillRect(10*PX,(h-22)*PX,PX,3*PX);
      // Mask
      ctx.fillStyle='rgba(0,0,0,.7)';
      for(let x=2;x<=8;x++) ctx.fillRect(x*PX,(h-20)*PX,PX,2*PX);
      // Eyes
      ctx.fillStyle=accent;ctx.shadowColor=accent;ctx.shadowBlur=6;
      px(ctx,3,h-20,'#22ff44'); px(ctx,7,h-20,'#22ff44');ctx.shadowBlur=0;
    }
  };
}

function makeGunnerSprite(pal, frame=0, action='idle'){
  const w=13, h=24;
  const f=frame;
  return {
    w,h,
    draw(ctx){
      const {body,legs,skin,accent}=pal;
      const legOff=action==='walk'?[Math.sin(f*.5)*2,Math.sin(f*.5+Math.PI)*2]:[0,0];
      const recoil=action==='atk'?Math.min(f*2,4):0;

      ctx.fillStyle='rgba(0,0,0,.25)';
      ctx.beginPath();ctx.ellipse(w/2*PX,(h+1)*PX,w/3*PX,PX*.6,0,0,Math.PI*2);ctx.fill();

      for(let y=h-7;y<=h;y++){
        px(ctx,2,y+(legOff[0]|0),legs); px(ctx,3,y+(legOff[0]|0),legs);
        px(ctx,8,y+(legOff[1]|0),legs); px(ctx,9,y+(legOff[1]|0),legs);
      }

      for(let x=2;x<=10;x++) for(let y=h-16;y<=h-8;y++) px(ctx,x,y,body);
      ctx.fillStyle='#334';
      for(let x=2;x<=10;x++) ctx.fillRect(x*PX,(h-16)*PX,PX,3*PX); // vest

      // Big gun
      ctx.fillStyle='#3a4455';
      ctx.fillRect(10*PX,(h-15-recoil)*PX,6*PX,4*PX);
      ctx.fillRect(14*PX,(h-16-recoil)*PX,3*PX,6*PX);
      ctx.fillStyle=accent;
      ctx.fillRect(16*PX,(h-14-recoil)*PX,2*PX,2*PX); // muzzle
      if(action==='atk'&&f<3){
        ctx.fillStyle='#ffee88';ctx.shadowColor='#ffcc00';ctx.shadowBlur=20;
        ctx.beginPath();ctx.arc(18*PX,(h-13-recoil)*PX,PX*2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
      }

      px(ctx,11,h-15-recoil/2|0,skin); px(ctx,11,h-14-recoil/2|0,skin);
      px(ctx,1,h-15,skin); px(ctx,1,h-14,skin);

      px(ctx,6,h-17,skin); px(ctx,7,h-17,skin);
      for(let x=3;x<=9;x++) for(let y=h-23;y<=h-18;y++) px(ctx,x,y,skin);
      // Cap
      ctx.fillStyle='#223322';
      for(let x=2;x<=10;x++) ctx.fillRect(x*PX,(h-24)*PX,PX,3*PX);
      ctx.fillRect(1*PX,(h-22)*PX,11*PX,PX); // brim
      // Goggles
      ctx.fillStyle='#334';ctx.fillRect(3*PX,(h-22)*PX,3*PX,2*PX);ctx.fillRect(7*PX,(h-22)*PX,3*PX,2*PX);
      ctx.fillStyle='rgba(50,200,255,.6)';ctx.fillRect(3*PX,(h-22)*PX,3*PX,2*PX);ctx.fillRect(7*PX,(h-22)*PX,3*PX,2*PX);
      ctx.fillStyle=accent;
      px(ctx,3,h-22,'#55aaff');px(ctx,7,h-22,'#55aaff');
    }
  };
}

// ═══ ENEMY SPRITES ═══
function makeEnemySprite(type, frame=0, hp_pct=1){
  const f=frame;
  switch(type){
    case 'goblin': return makeGoblinSprite(f);
    case 'orc': return makeOrcSprite(f);
    case 'skeleton': return makeSkeletonSprite(f);
    case 'slime': return makeSlimeSprite(f, hp_pct);
    case 'demon': return makeDemonSprite(f);
    case 'dragon': return makeDragonSprite(f, hp_pct);
    default: return makeGoblinSprite(f);
  }
}

function makeGoblinSprite(f=0){
  const w=10, h=18;
  const legOff=[Math.sin(f*.5)*2,Math.sin(f*.5+Math.PI)*2];
  return {w,h,draw(ctx){
    // Feet
    px(ctx,1,(h+legOff[0]|0),'#228'); px(ctx,2,(h+legOff[0]|0),'#228');
    px(ctx,6,(h+legOff[1]|0),'#228'); px(ctx,7,(h+legOff[1]|0),'#228');
    // Legs
    for(let y=h-4;y<h;y++){px(ctx,1,y+(legOff[0]|0),'#33aa44');px(ctx,2,y+(legOff[0]|0),'#33aa44');}
    for(let y=h-4;y<h;y++){px(ctx,6,y+(legOff[1]|0),'#33aa44');px(ctx,7,y+(legOff[1]|0),'#33aa44');}
    // Body
    for(let x=1;x<=8;x++) for(let y=h-11;y<=h-5;y++) px(ctx,x,y,'#22aa33');
    // Dagger arm
    const arm=Math.sin(f*.8)*2|0;
    px(ctx,9,h-10-arm,'#33aa44'); px(ctx,9,h-9-arm,'#33aa44');
    ctx.fillStyle='#aabbcc';ctx.fillRect(9*PX,(h-14-arm)*PX,PX,5*PX);
    // Head
    for(let x=2;x<=7;x++) for(let y=h-17;y<=h-12;y++) px(ctx,x,y,'#22aa33');
    // Big ears
    ctx.fillStyle='#22aa33';
    ctx.fillRect(0,(h-16)*PX,2*PX,3*PX);ctx.fillRect(8*PX,(h-16)*PX,2*PX,3*PX);
    ctx.fillStyle='rgba(255,100,100,.4)';
    ctx.fillRect(0,(h-15)*PX,PX,2*PX);ctx.fillRect(9*PX,(h-15)*PX,PX,2*PX);
    // Eyes
    ctx.fillStyle='#ffcc00';px(ctx,3,h-15,'#ffcc00');px(ctx,6,h-15,'#ffcc00');
    ctx.fillStyle='#000';px(ctx,3,h-15,'#440000');px(ctx,6,h-15,'#440000');
    // Teeth
    ctx.fillStyle='#fff';ctx.fillRect(3*PX,(h-13)*PX,PX,PX);ctx.fillRect(5*PX,(h-13)*PX,PX,PX);
  }};
}

function makeOrcSprite(f=0){
  const w=14, h=24;
  const legOff=[Math.sin(f*.35)*1.5,Math.sin(f*.35+Math.PI)*1.5];
  return {w,h,draw(ctx){
    for(let y=h-8;y<=h;y++){
      px(ctx,2,y+(legOff[0]|0),'#2a4a1a');px(ctx,3,y+(legOff[0]|0),'#2a4a1a');px(ctx,4,y+(legOff[0]|0),'#2a4a1a');
      px(ctx,9,y+(legOff[1]|0),'#2a4a1a');px(ctx,10,y+(legOff[1]|0),'#2a4a1a');px(ctx,11,y+(legOff[1]|0),'#2a4a1a');
    }
    for(let x=2;x<=11;x++) for(let y=h-17;y<=h-9;y++) px(ctx,x,y,'#3a5a2a');
    // Chest plate
    ctx.fillStyle='#445533';ctx.fillRect(3*PX,(h-16)*PX,8*PX,5*PX);
    ctx.fillStyle='rgba(255,200,100,.15)';ctx.fillRect(3*PX,(h-16)*PX,8*PX,2*PX);
    // Axe arm
    const a=Math.sin(f*.6)*3|0;
    for(let y=h-18;y<=h-12;y++) px(ctx,12,y-a,'#2a4a1a');
    ctx.fillStyle='#664422';ctx.fillRect(12*PX,(h-22-a)*PX,2*PX,8*PX);
    ctx.fillStyle='#c08040';
    ctx.beginPath();
    ctx.moveTo(12*PX,(h-22-a)*PX); ctx.lineTo(6*PX,(h-24-a)*PX);
    ctx.lineTo(6*PX,(h-18-a)*PX); ctx.lineTo(12*PX,(h-20-a)*PX);
    ctx.fill();
    ctx.fillStyle='rgba(255,200,100,.3)';
    ctx.beginPath();ctx.moveTo(12*PX,(h-22-a)*PX);ctx.lineTo(7*PX,(h-24-a)*PX);ctx.lineTo(8*PX,(h-21-a)*PX);ctx.fill();

    for(let y=h-18;y<=h-12;y++) px(ctx,1,y,'#2a4a1a');
    for(let x=3;x<=10;x++) for(let y=h-23;y<=h-18;y++) px(ctx,x,y,'#4a6a3a');
    // Mohawk
    ctx.fillStyle='#cc2200';
    for(let y=h-27;y<=h-24;y++) ctx.fillRect(6*PX,y*PX,2*PX,PX);
    ctx.fillRect(6*PX,(h-29)*PX,2*PX,PX);
    // Eyes
    ctx.fillStyle='#ff2200';px(ctx,4,h-21,'#ff2200');px(ctx,8,h-21,'#ff2200');
    // Tusks
    ctx.fillStyle='#eee';ctx.fillRect(4*PX,(h-18)*PX,PX,3*PX);ctx.fillRect(8*PX,(h-18)*PX,PX,3*PX);
  }};
}

function makeSkeletonSprite(f=0){
  const w=11, h=22;
  const legOff=[Math.sin(f*.45)*2,Math.sin(f*.45+Math.PI)*2];
  return {w,h,draw(ctx){
    const bc='#d4c8a0';
    // Leg bones
    for(let y=h-7;y<=h;y++) px(ctx,2,y+(legOff[0]|0),bc);
    px(ctx,2,h-4+(legOff[0]|0),'#b4a880'); // knee
    for(let y=h-7;y<=h;y++) px(ctx,7,y+(legOff[1]|0),bc);
    px(ctx,7,h-4+(legOff[1]|0),'#b4a880');
    // Ribcage
    for(let x=2;x<=8;x++) ctx.fillStyle=x%2?bc:'#b4a880',ctx.fillRect(x*PX,(h-16)*PX,PX,6*PX);
    ctx.fillStyle='rgba(0,0,0,.3)';
    for(let x=2;x<=8;x+=2) for(let y=h-15;y<=h-12;y++) ctx.fillRect(x*PX,y*PX,PX,PX);
    // Spine
    ctx.fillStyle=bc;ctx.fillRect(5*PX,(h-16)*PX,PX,16*PX);
    // Sword arm
    const a=Math.sin(f*.7)*3|0;
    ctx.fillStyle=bc;ctx.fillRect(9*PX,(h-18-a)*PX,PX,8*PX);
    ctx.fillStyle='#ddeeff';ctx.fillRect(9*PX,(h-22-a)*PX,PX,5*PX);
    ctx.fillStyle='rgba(200,220,255,.4)';ctx.fillRect(9*PX,(h-22-a)*PX,PX,2*PX);
    // Off arm
    ctx.fillStyle=bc;ctx.fillRect(1*PX,(h-18)*PX,PX,8*PX);
    // Skull
    for(let x=3;x<=8;x++) for(let y=h-22;y<=h-17;y++) px(ctx,x,y,bc);
    ctx.fillStyle='rgba(0,0,0,.4)';
    ctx.fillRect(3*PX,(h-17)*PX,5*PX,PX); // jaw
    // Eye sockets
    ctx.fillStyle='#111';ctx.fillRect(3*PX,(h-21)*PX,2*PX,2*PX);ctx.fillRect(7*PX,(h-21)*PX,2*PX,2*PX);
    ctx.fillStyle='rgba(50,200,255,.6)';ctx.fillRect(4*PX,(h-21)*PX,PX,2*PX);ctx.fillRect(7*PX,(h-21)*PX,PX,2*PX);
    // Teeth
    ctx.fillStyle='#fff';for(let x=4;x<=7;x++) ctx.fillRect(x*PX,(h-17)*PX,PX,PX);
  }};
}

function makeSlimeSprite(f=0, hp=1){
  const w=16, h=14;
  const squish=Math.sin(f*.06)*1.5;
  return {w,h,draw(ctx){
    const col=hp>.5?'#44cc88':hp>.25?'#88cc44':'#cc4444';
    const dark=hp>.5?'#228855':hp>.25?'#558822':'#882222';
    ctx.save();
    ctx.scale(1+squish*.05, 1-squish*.05);
    for(let x=2;x<=13;x++) for(let y=h-10;y<=h;y++){
      const d=Math.abs(x-7.5)+Math.abs(y-(h-5));
      if(d<7) {px(ctx,x,y,d<4?col:dark);}
    }
    // Eyes
    ctx.fillStyle='#fff';ctx.fillRect(4*PX,(h-8)*PX,2*PX,2*PX);ctx.fillRect(9*PX,(h-8)*PX,2*PX,2*PX);
    ctx.fillStyle='#000';ctx.fillRect(5*PX,(h-8)*PX,PX,PX);ctx.fillRect(10*PX,(h-8)*PX,PX,PX);
    // Smile
    ctx.fillStyle='rgba(0,0,0,.4)';
    ctx.fillRect(5*PX,(h-5)*PX,6*PX,PX);
    ctx.fillRect(4*PX,(h-6)*PX,PX,PX);ctx.fillRect(11*PX,(h-6)*PX,PX,PX);
    ctx.restore();
  }};
}

function makeDemonSprite(f=0){
  const w=16, h=28;
  const legOff=[Math.sin(f*.4)*2,Math.sin(f*.4+Math.PI)*2];
  return {w,h,draw(ctx){
    // Hooves
    for(let y=h-8;y<=h;y++){
      px(ctx,2,y+(legOff[0]|0),'#3a0808');px(ctx,3,y+(legOff[0]|0),'#3a0808');
      px(ctx,11,y+(legOff[1]|0),'#3a0808');px(ctx,12,y+(legOff[1]|0),'#3a0808');
    }
    ctx.fillStyle='#110000';ctx.fillRect(1*PX,(h)*PX,4*PX,PX*1.5);ctx.fillRect(10*PX,(h)*PX,4*PX,PX*1.5);
    // Wings
    ctx.fillStyle='rgba(80,0,0,.8)';
    ctx.beginPath();ctx.moveTo(4*PX,(h-20)*PX);ctx.lineTo(0,(h-30)*PX);ctx.lineTo(0,(h-12)*PX);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(12*PX,(h-20)*PX);ctx.lineTo(16*PX,(h-30)*PX);ctx.lineTo(16*PX,(h-12)*PX);ctx.closePath();ctx.fill();
    // Body
    for(let x=3;x<=12;x++) for(let y=h-20;y<=h-9;y++) px(ctx,x,y,'#4a0a0a');
    ctx.fillStyle='rgba(255,0,0,.1)';ctx.beginPath();ctx.arc(8*PX,(h-14)*PX,3*PX,0,Math.PI*2);ctx.fill();
    // Claws
    const a=Math.sin(f*.6)*3|0;
    for(let y=h-22;y<=h-15;y++) px(ctx,13,y-a,'#3a0808');
    ctx.fillStyle='#ff2200';
    for(let i=0;i<3;i++) ctx.fillRect((13+i)*PX,(h-15-a)*PX,PX,2*PX);
    for(let y=h-22;y<=h-15;y++) px(ctx,2,y,'#3a0808');
    // Head
    for(let x=4;x<=11;x++) for(let y=h-27;y<=h-21;y++) px(ctx,x,y,'#550a0a');
    // Horns
    ctx.fillStyle='#660000';
    ctx.fillRect(4*PX,(h-31)*PX,2*PX,5*PX);ctx.fillRect(3*PX,(h-32)*PX,PX,2*PX);
    ctx.fillRect(10*PX,(h-31)*PX,2*PX,5*PX);ctx.fillRect(12*PX,(h-32)*PX,PX,2*PX);
    // Eyes
    ctx.fillStyle='#ff0000';ctx.shadowColor='#ff0000';ctx.shadowBlur=8;
    px(ctx,5,h-25,'#ff0000');px(ctx,9,h-25,'#ff0000');ctx.shadowBlur=0;
  }};
}

function makeDragonSprite(f=0, hp=1){
  const w=24, h=32;
  const tail=Math.sin(f*.05)*3;
  const col=hp>.5?'#1a3a1a':hp>.25?'#3a2a00':'#3a0000';
  const sc=hp>.5?'#2a5a2a':hp>.25?'#5a4400':'#5a0000';
  return {w,h,draw(ctx){
    // Tail
    ctx.fillStyle=col;
    for(let i=0;i<6;i++) ctx.fillRect((16+i)*PX,(h-8+tail*i/5|0)*PX,2*PX,(3-i/3|0)*PX+PX);
    // Wings
    ctx.fillStyle='rgba(20,50,20,.7)';
    ctx.beginPath();ctx.moveTo(6*PX,(h-22)*PX);ctx.lineTo(0,(h-30)*PX);ctx.lineTo(0,(h-16)*PX);ctx.lineTo(6*PX,(h-14)*PX);ctx.closePath();ctx.fill();
    // Legs
    const legO=[Math.sin(f*.4)*1.5,Math.sin(f*.4+Math.PI)*1.5];
    for(let y=h-8;y<=h;y++){
      px(ctx,4,y+(legO[0]|0),col);px(ctx,5,y+(legO[0]|0),col);
      px(ctx,13,y+(legO[1]|0),col);px(ctx,14,y+(legO[1]|0),col);
    }
    // Body
    for(let x=4;x<=17;x++) for(let y=h-20;y<=h-9;y++) px(ctx,x,y,col);
    // Scales
    for(let i=0;i<4;i++) px(ctx,8+i*2,h-18,sc);
    // Arm claws
    const a=Math.sin(f*.5)*2|0;
    for(let y=h-24;y<=h-16;y++) px(ctx,18,y-a,col);
    ctx.fillStyle='#999';for(let i=0;i<3;i++) ctx.fillRect((18+i)*PX,(h-16-a)*PX,PX,2*PX);
    // Neck+head
    for(let x=6;x<=11;x++) for(let y=h-26;y<=h-21;y++) px(ctx,x,y,col);
    for(let x=5;x<=13;x++) for(let y=h-32;y<=h-27;y++) px(ctx,x,y,col);
    // Snout
    for(let x=12;x<=16;x++) for(let y=h-31;y<=h-28;y++) px(ctx,x,y,col);
    // Eyes
    ctx.fillStyle='#ffaa00';ctx.shadowColor='#ffaa00';ctx.shadowBlur=8;
    px(ctx,6,h-30,'#ffaa00');ctx.shadowBlur=0;
    // Horns
    ctx.fillStyle='#777';ctx.fillRect(5*PX,(h-36)*PX,PX,5*PX);ctx.fillRect(7*PX,(h-37)*PX,PX,6*PX);
    // Fire breath at low hp
    if(hp<.3){
      ctx.fillStyle='rgba(255,100,0,.8)';ctx.shadowColor='#ff6600';ctx.shadowBlur=15;
      ctx.beginPath();ctx.arc(16*PX,(h-29)*PX,PX*2.5,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
    }
  }};
}

// ═══ CLASS DEFINITIONS ═══
const CLASSES={
  warrior:{name:'검사',icon:'⚔️',portrait:'⚔️',col:'#4488cc',
    hp:420,mp:80,atk:45,def:18,spd:4.8,jmp:13,
    spriteType:'warrior',
    pal:{skin:'#f5c090',hair:'#1a0800',body:'#3a4455',armor:'#445566',legs:'#334',weapon:'sword'},
    desc:'높은 HP와 방어력. 방패 콤보로 강력한 근접전.',
    tags:['근접','탱커','방어'],
    skills:[
      {n:'검격',icon:'⚔️',key:'A',mp:8,cd:1.5,col:'#aabbcc',
       fn:(p,G)=>aoe(p.x+(p.f>0?p.w:-72),p.y-15,80,70,dmg(p,1.8),true)},
      {n:'방패 강타',icon:'🛡️',key:'S',mp:16,cd:3.5,col:'#8899bb',
       fn:(p,G)=>{p.vx=p.f*18;setTimeout(()=>aoe(p.x+(p.f>0?p.w:-80),p.y-5,85,65,dmg(p,1.4),true,{stun:90}),120);}},
      {n:'돌격',icon:'💨',key:'D',mp:22,cd:5,col:'#ccd8e0',
       fn:(p,G)=>{p.vx=p.f*38;p.inv=40;setTimeout(()=>{aoe(p.x+(p.f>0?p.w-10:-100),p.y-25,120,90,dmg(p,2.5),true);boom(p.x+(p.f>0?p.w+40:-40),p.y+10,'#aabbcc');shake(6,14);},180);}},
      {n:'회오리',icon:'🌀',key:'F',mp:36,cd:7,col:'#99aabb',
       fn:(p,G)=>{aoe(p.x-80,p.y-45,p.w+160,p.h+90,dmg(p,2.2),false);shake(5,12);}},
      {n:'무적 참격',icon:'🗡️',key:'G',mp:60,cd:15,col:'#eeffff',
       fn:(p,G)=>{p.inv=300;p.hp=Math.min(p.maxHp,p.hp+Math.round(p.maxHp*.18));aoe(p.x-65,p.y-55,p.w+140,130,dmg(p,3.2),true);shake(9,22);}},
    ]},
  mage:{name:'마법사',icon:'🔮',portrait:'🔮',col:'#aa44ff',
    hp:210,mp:280,atk:65,def:5,spd:4.0,jmp:12,
    spriteType:'mage',
    pal:{skin:'#c07840',hair:'#1a0800',robe:'#331155',accent:'#aa44ff'},
    desc:'강력한 마법 공격. MP 관리가 핵심.',
    tags:['원거리','마법','고화력'],
    skills:[
      {n:'파이어볼',icon:'🔥',key:'A',mp:18,cd:1.5,col:'#ff6600',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>proj(p.x+p.f*52,p.y+18,p.f*17,(Math.random()-.5)*.4,dmg(p,1.8),'#ff6600','player',{sz:14,emoji:'🔥',life:65,trail:true}),i*85);}},
      {n:'아이스 스피어',icon:'❄️',key:'S',mp:26,cd:4,col:'#44aaff',
       fn:(p,G)=>proj(p.x+p.f*52,p.y+18,p.f*15,0,dmg(p,2.5),'#44aaff','player',{sz:16,emoji:'❄️',life:75,onHit:(e)=>{e.frozen=Math.max(e.frozen||0,180);}})},
      {n:'낙뢰',icon:'⚡',key:'D',mp:34,cd:5,col:'#ffee00',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>{const tx=p.x+p.f*(130+i*100);proj(tx,-20,0,24,dmg(p,2.4),'#ffee00','player',{sz:20,emoji:'⚡',life:28,grav:.7});spark(tx-G.cam,70,{n:10,col:['#ffee00','#ffdd44'],glow:true,spread:.4,dir:Math.PI*.5,smin:4,smax:10});},i*170);}},
      {n:'메테오',icon:'☄️',key:'F',mp:70,cd:12,col:'#ff4400',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>{const tx=p.x+p.f*100+(Math.random()-.5)*280;proj(tx,-70,(Math.random()-.5)*2,20,dmg(p,3.8),'#ff4400','player',{sz:26,emoji:'☄️',life:80,grav:.3});shake(4,9);},i*150);}},
      {n:'타임스탑',icon:'⏰',key:'G',mp:85,cd:20,col:'#8844ff',
       fn:(p,G)=>freezeAll(220)},
    ]},
  rogue:{name:'로그',icon:'🗝️',portrait:'🗝️',col:'#22cc55',
    hp:255,mp:190,atk:56,def:7,spd:6.2,jmp:16,
    spriteType:'rogue',
    pal:{skin:'#e8a870',hair:'#1a0800',body:'#1a2a1a',legs:'#111a11',accent:'#22ff44'},
    desc:'초고속 이동과 연속 참격. 크리티컬 특화.',
    tags:['근접','고속','암살'],
    skills:[
      {n:'3연참',icon:'🗡️',key:'A',mp:10,cd:1.2,col:'#44ee66',
       fn:(p,G)=>{for(let i=0;i<3;i++)setTimeout(()=>aoe(p.x+(p.f>0?p.w:-68),p.y-8,72,62,dmg(p,1.6),Math.random()<.4),i*90);}},
      {n:'수리검',icon:'✴️',key:'S',mp:18,cd:3,col:'#aaffaa',
       fn:(p,G)=>[-5,-1,3,7].forEach(vy=>proj(p.x+p.f*52,p.y+22,p.f*20,vy,dmg(p,1.7),'#22dd44','player',{sz:10,emoji:'✴️',life:75}))},
      {n:'순간이동',icon:'💨',key:'D',mp:16,cd:3.5,col:'#aa44cc',
       fn:(p,G)=>{spark(p.x-G.cam+p.w/2,p.y+p.h/2,{n:18,col:['#22cc44','#88ff88'],grav:0,smin:2,smax:7});p.x+=p.f*200;setTimeout(()=>aoe(p.x+(p.f>0?p.w:-95),p.y-22,105,85,dmg(p,2.8),true),70);}},
      {n:'독 단검',icon:'☠️',key:'F',mp:32,cd:7,col:'#44cc44',
       fn:(p,G)=>proj(p.x+p.f*52,p.y+22,p.f*18,-2,dmg(p,2.0),'#44cc44','player',{sz:13,emoji:'🗡️',life:85,onHit:(e)=>{e.poison=Math.max(e.poison||0,300);e.pdmg=Math.round(p.atk*.4);}})},
      {n:'죽음의 무도',icon:'💀',key:'G',mp:78,cd:18,col:'#222244',
       fn:(p,G)=>{p.inv=310;for(let i=0;i<6;i++){const a=i/6*Math.PI*2;aoe(p.x+Math.cos(a)*90-55,p.y+Math.sin(a)*65-35,110,90,dmg(p,3.8),true);}shake(14,32);}},
    ]},
  gunner:{name:'건너',icon:'🔫',portrait:'🔫',col:'#44cc88',
    hp:270,mp:170,atk:50,def:8,spd:5.4,jmp:14,
    spriteType:'gunner',
    pal:{skin:'#f5c090',hair:'#ffd080',body:'#1a3322',legs:'#112211',accent:'#44ffaa'},
    desc:'빠른 연사와 폭발물. 원거리 전투 특화.',
    tags:['원거리','연사','폭발'],
    skills:[
      {n:'연사',icon:'🔫',key:'A',mp:10,cd:1,col:'#44cc88',
       fn:(p,G)=>{for(let i=0;i<6;i++)setTimeout(()=>proj(p.x+p.f*58,p.y+22,p.f*24+(Math.random()-.5)*1.5,(Math.random()-.5)*1.5,dmg(p,1.0),'#44cc88','player',{sz:7,life:72}),i*45);}},
      {n:'유탄',icon:'💣',key:'S',mp:20,cd:4,col:'#ffcc00',
       fn:(p,G)=>proj(p.x+p.f*48,p.y+22,p.f*10,-9,dmg(p,3.2),'#ffcc00','player',{sz:18,emoji:'💣',life:95,grav:.4,explode:true})},
      {n:'저격',icon:'🎯',key:'D',mp:28,cd:5.5,col:'#88ff44',
       fn:(p,G)=>{proj(p.x+p.f*55,p.y+22,p.f*38,0,dmg(p,5.0),'#88ff44','player',{sz:11,life:115,pierce:true});shake(2,5);}},
      {n:'미사일',icon:'🚀',key:'F',mp:44,cd:9,col:'#ff8800',
       fn:(p,G)=>{for(let i=0;i<5;i++)setTimeout(()=>proj(p.x+p.f*42,p.y+16+i*5,p.f*10,(Math.random()-.5)*3,-9+(Math.random()-.5)*3,dmg(p,2.2),'#ff8800','player',{sz:16,emoji:'🚀',life:105,grav:.05,homing:true}),i*85);}},
      {n:'탄막',icon:'🌟',key:'G',mp:80,cd:18,col:'#44ffaa',
       fn:(p,G)=>{for(let i=0;i<20;i++)setTimeout(()=>{const a=i/20*Math.PI*2;proj(p.x+p.w/2,p.y+p.h/2,Math.cos(a)*18,Math.sin(a)*15,dmg(p,1.4),'#44ffaa','player',{sz:9,life:70,pierce:true});},i*50);shake(7,20);}},
    ]},
};

// ═══ ENEMY DATA ═══
const ENEMIES={
  goblin:  {name:'고블린',  type:'goblin',  w:40,h:44, hp:80, atk:12,spd:3.2,xp:14,g:8,  ai:'chase'},
  skeleton:{name:'스켈레톤',type:'skeleton',w:44,h:52, hp:120,atk:18,spd:3.0,xp:22,g:14, ai:'normal'},
  orc:     {name:'오크',    type:'orc',     w:56,h:60, hp:200,atk:25,spd:1.8,xp:30,g:18, ai:'brute'},
  slime:   {name:'슬라임',  type:'slime',   w:60,h:44, hp:160,atk:10,spd:1.4,xp:18,g:10, ai:'slow'},
  demon:   {name:'데몬',    type:'demon',   w:52,h:64, hp:190,atk:28,spd:2.8,xp:50,g:34, ai:'chase'},
};

const STAGES=[
  {name:'고블린 굴',   bg:'#05030c',fl:'#0d0820',wall:'#0a0618',fg:'#090515',torch:'#ff7700',
   mobs:['goblin','goblin','skeleton','goblin'],cnt:8,
   boss:{name:'왕 고블린',type:'goblin',hp:900,atk:28,spd:2.8,w:72,h:64,drawScale:1.7}},
  {name:'오크 요새',   bg:'#0c0300',fl:'#180700',wall:'#150500',fg:'#110400',torch:'#ff4400',
   mobs:['orc','goblin','skeleton','orc'],cnt:10,
   boss:{name:'전쟁족장',type:'orc',hp:1400,atk:36,spd:2.0,w:84,h:76,drawScale:1.6}},
  {name:'해골 묘지',   bg:'#030812',fl:'#060f24',wall:'#040a1c',fg:'#030820',torch:'#6644ff',
   mobs:['skeleton','slime','goblin','skeleton'],cnt:12,
   boss:{name:'대마법사 리치',type:'skeleton',hp:2000,atk:45,spd:2.8,w:76,h:80,drawScale:1.65}},
  {name:'악마의 성',   bg:'#0a0000',fl:'#160000',wall:'#120000',fg:'#0e0000',torch:'#ff0044',
   mobs:['demon','orc','skeleton','demon'],cnt:14,
   boss:{name:'마왕 DARKOS',type:'demon',hp:3000,atk:58,spd:3.0,w:88,h:88,drawScale:1.7}},
];

// ═══ SHOP ═══
const SHOP=[
  {n:'HP 포션',icon:'🧪',desc:'HP +25%',price:70,fn:p=>{const h=Math.round(p.maxHp*.25);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {n:'대형 HP 포션',icon:'⚗️',desc:'HP +60%',price:170,fn:p=>{const h=Math.round(p.maxHp*.6);p.hp=Math.min(p.maxHp,p.hp+h);return `HP +${h}`;}},
  {n:'마나 포션',icon:'💙',desc:'MP +50%',price:85,fn:p=>{const m=Math.round(p.maxMp*.5);p.mp=Math.min(p.maxMp,p.mp+m);return `MP +${m}`;}},
  {n:'강화 무기',icon:'⚔️',desc:'ATK +20',price:200,fn:p=>{p.atkBonus=(p.atkBonus||0)+20;return 'ATK +20';}},
  {n:'불꽃 검',icon:'🔥',desc:'ATK +40',price:400,fn:p=>{p.atkBonus=(p.atkBonus||0)+40;return 'ATK +40';}},
  {n:'강화 갑옷',icon:'🛡️',desc:'DEF+14 HP+50',price:230,fn:p=>{p.defBonus=(p.defBonus||0)+14;p.maxHp+=50;p.hp=Math.min(p.maxHp,p.hp+50);return 'DEF+14 HP+50';}},
  {n:'스피드 링',icon:'💍',desc:'SPD +1.2',price:190,fn:p=>{p.spdBonus=(p.spdBonus||0)+1.2;return 'SPD +1.2';}},
  {n:'크리티컬 반지',icon:'🔮',desc:'CRIT +20%',price:310,fn:p=>{p.critBonus=(p.critBonus||0)+.20;return 'CRIT +20%';}},
  {n:'전설 반지',icon:'⭐',desc:'ATK+28 CRIT+28%',price:680,fn:p=>{p.atkBonus=(p.atkBonus||0)+28;p.critBonus=(p.critBonus||0)+.28;return 'ATK+28 CRIT+28%';}},
];

// ═══ GAME STATE ═══
let G=null, selCls=null;
const GRAVITY=.58, STAGEW=5600;

// ═══ COMBAT ═══
function atkTotal(p){ return (p.atk+(p.atkBonus||0))*(p.buffAtk||1); }
function defTotal(p){ return (p.def+(p.defBonus||0))+(p.defBuff||0); }
function critTotal(p){ return .1+(p.critBonus||0); }
function spdTotal(p){ return (p.spd+(p.spdBonus||0))*(p.buffSpd||1); }

function dmg(p,mult){
  const a=atkTotal(p);
  const c=Math.random()<critTotal(p);
  const v=Math.round((a*mult+Math.random()*5-2)*(c?2.2:1));
  return {v:Math.max(1,v),crit:c};
}

function aoe(ax,ay,aw,ah,d,showCrit,opts={}){
  if(!G) return;
  const tgts=[...G.enemies];
  if(G.boss&&G.boss.alive) tgts.push(G.boss);
  for(const e of tgts){
    if(!e.alive) continue;
    if(ax<e.x+e.w&&ax+aw>e.x&&ay<e.y+e.h&&ay+ah>e.y)
      hit(e,d.v,d.crit||showCrit,opts);
  }
}

function hitAll(d){
  if(!G) return;
  const tgts=[...G.enemies];
  if(G.boss&&G.boss.alive) tgts.push(G.boss);
  for(const e of tgts) if(e.alive) hit(e,d.v,d.crit,{});
}

function hit(e,v,crit,opts){
  if(!e.alive) return;
  const p=G.player;
  if(e.cursed>0) v=Math.round(v*1.4);
  e.hp-=v;e.hitFlash=10;
  if(opts.stun) e.stun=Math.max(e.stun||0,opts.stun);
  if(opts.lifeSteal) p.hp=Math.min(p.maxHp,p.hp+Math.round(v*opts.lifeSteal));
  if(opts.onHit) opts.onHit(e);
  showDmg((e.x-G.cam+e.w/2)|0,(e.y)|0,v,crit,p.col||'#fff');
  G.hitstop=crit?6:2;
  if(crit) SFX.crit(); else SFX.hit();
  if(e.hp<=0) kill(e);
}

function kill(e){
  e.alive=false;
  const p=G.player;
  if(e===G.boss){
    p.xp+=600;p.gold+=380;p.score+=7000;
    document.getElementById('boss-ui').classList.remove('visible');
    spark(e.x-G.cam+e.w/2,e.y+e.h/2,{n:70,col:['#ffcc00','#ff6600','#fff'],glow:true,smin:3,smax:14});
    shake(16,60); SFX.clear();
    checkLvl(p);
    setTimeout(()=>stageClear(),1200);
  } else {
    p.kills++;p.xp+=e.xp;p.gold+=e.g;p.score+=e.xp*2;
    spark(e.x-G.cam+e.w/2,e.y+e.h/2,{n:16,col:['#ffcc00','#ff4400'],smin:2,smax:6});
    checkLvl(p);
    drop(e);
  }
}

function checkLvl(p){
  while(p.xp>=p.xpNext){
    p.xp-=p.xpNext;p.level++;p.xpNext=Math.round(p.xpNext*1.6);
    p.maxHp+=28;p.hp=Math.min(p.maxHp,p.hp+45);
    p.maxMp+=8;p.mp=Math.min(p.maxMp,p.mp+15);
    p.atk+=4;p.def+=2;
    G.pendLvl=true;showLvlModal();SFX.lvl();
  }
}

function drop(e){
  if(Math.random()>.4) return;
  const it={...SHOP[~~(Math.random()*SHOP.length)],
    uid:'d'+Date.now()+Math.random(),
    x:e.x+e.w/2-14,y:e.y,vy:-7,alive:true};
  G.items.push(it);
}

function freezeAll(dur){
  if(!G) return;
  [...G.enemies,...(G.boss&&G.boss.alive?[G.boss]:[])].forEach(e=>{if(e.alive)e.frozen=Math.max(e.frozen||0,dur);});
}

function proj(x,y,vx,vy,d,col,owner,opts={}){
  if(!G) return;
  G.projs.push({x,y,vx,vy,dmg:d.v,crit:d.crit,col,owner,alive:true,
    life:opts.life||80,sz:opts.sz||8,pierce:opts.pierce||false,
    grav:opts.grav||0,emoji:opts.emoji||null,trail:opts.trail||false,
    homing:opts.homing||false,explode:opts.explode||false,onHit:opts.onHit||null});
}

function boom(wx,wy,col,sc=1.6){
  spark(wx,wy,{n:Math.round(28*sc),col:[col,'#fff','#ffcc00'],glow:true,smin:3*sc,smax:9*sc,ub:2});
  spark(wx,wy,{n:Math.round(12*sc),col:[col,'#ff4400'],sq:true,smin:2*sc,smax:5*sc});
}

function shake(amt,dur){
  if(!G) return;
  G.shakeAmt=Math.max(G.shakeAmt,amt);
  G.shakeDur=Math.max(G.shakeDur,dur);
}

// ═══ INIT ═══
function mkPlayer(clsId){
  const c=CLASSES[clsId];
  return {
    ...c,clsId,
    x:160,y:GY()-70,vx:0,vy:0,f:1,
    onGround:false,jumpCount:0,
    hp:c.hp,maxHp:c.hp,mp:c.mp,maxMp:c.mp,
    alive:true,inv:0,
    skillCds:c.skills.map(()=>0),
    buffAtk:1,buffSpd:1,buffTimer:0,
    kills:0,score:0,gold:0,level:1,
    xp:0,xpNext:100,
    combo:0,comboT:0,maxCombo:0,
    atkCd:0,atkFrame:0,hitFlash:0,dodgeCd:0,dodgeT:0,
    w:c.spriteType==='orc'?56:44,h:c.spriteType==='dragon'?80:62,
    atkBonus:0,defBonus:0,spdBonus:0,critBonus:0,defBuff:0,defBuffT:0,
    walkPhase:0,atkPhase:0,animFrame:0,
  };
}

function initGame(clsId,stageIdx){
  const p=mkPlayer(clsId);
  const stage=STAGES[stageIdx];
  G={
    clsId,stageIdx,stage,player:p,
    enemies:[],boss:null,bossSpawned:false,
    projs:[],items:[],
    cam:0,timer:0,startTime:Date.now(),
    platforms:genPlats(stage),
    shakeAmt:0,shakeDur:0,hitstop:0,
    phase:'play',paused:false,
    pendLvl:false,
    dmgTaken:0,shopStock:[],
    bgScroll:0,
  };
  PARTS.length=0;
  spawnEnemies();
  document.getElementById('char-portrait').textContent=CLASSES[clsId].portrait;
  updateEquipUI();
}

function genPlats(stage){
  const arr=[];
  for(let i=0;i<14;i++){
    arr.push({
      x:300+i*320+(Math.random()-.5)*80,
      y:GY()-70-Math.random()*120,
      w:70+Math.random()*90,h:14,
    });
  }
  return arr;
}

function spawnEnemies(){
  const s=G.stage;
  for(let i=0;i<s.cnt;i++){
    const tid=s.mobs[~~(Math.random()*s.mobs.length)];
    const et={...ENEMIES[tid]};
    const sc=1+G.stageIdx*.22;
    G.enemies.push({
      ...et,uid:'e'+i,
      x:700+i*280+Math.random()*100,
      y:GY()-et.h,
      hp:Math.round(et.hp*sc),maxHp:Math.round(et.hp*sc),
      atk:Math.round(et.atk*sc),
      vx:0,vy:0,f:-1,alive:true,
      atkTimer:60+Math.random()*80,
      frozen:0,stun:0,poison:0,pdmg:0,poisonT:0,
      cursed:0,hitFlash:0,
      walkPhase:Math.random()*Math.PI*2,atkPhase:0,
      aggro:false,animFrame:0,
    });
  }
}

function spawnBoss(){
  const bd=G.stage.boss;
  const sc=1+G.stageIdx*.28;
  G.boss={
    ...bd,...ENEMIES[bd.type],
    name:bd.name,type:bd.type,drawScale:bd.drawScale,
    x:STAGEW-600,y:GY()-bd.h,
    hp:Math.round(bd.hp*sc),maxHp:Math.round(bd.hp*sc),
    atk:Math.round(bd.atk*sc),spd:bd.spd,
    w:bd.w,h:bd.h,
    alive:true,frozen:0,stun:0,cursed:0,
    atkTimer:70,projTimer:90,
    phase2:false,phase3:false,
    hitFlash:0,walkPhase:0,atkPhase:0,animFrame:0,
    vy:0,
  };
  document.getElementById('boss-ui').classList.add('visible');
  document.getElementById('boss-name').textContent='⚠ '+bd.name+' ⚠';
  const bw=document.getElementById('boss-warn');
  bw.style.display='block';
  bw.textContent='⚠ BOSS\n'+bd.name;
  setTimeout(()=>bw.style.display='none',2600);
  shake(14,50); SFX.boss();
}

// ═══ GAME LOOP ═══
let lastT=0, raf=null;
function loop(t){
  const dt=Math.min((t-lastT)/16.67,3);lastT=t;
  if(G&&G.phase==='play'&&!G.paused&&!G.pendLvl){
    update(dt);
  }
  render();
  updateHUD();
  clearJK();
  raf=requestAnimationFrame(loop);
}

function update(dt){
  G.timer++;
  G.bgScroll+=.4*dt;
  const p=G.player;
  if(!p.alive) return;
  if(G.hitstop>0){G.hitstop-=dt;return;}
  handleInput(p,dt);
  updatePlayer(p,dt);
  updateEnemies(dt);
  if(G.boss&&G.boss.alive) updateBoss(dt);
  updateProjs(dt);
  updateItems(dt);
  tickParts(dt);
  if(G.shakeDur>0) G.shakeDur-=dt;
  if(!G.bossSpawned&&G.enemies.filter(e=>e.alive).length===0){
    G.bossSpawned=true;spawnBoss();
  }
  if(G.timer%75===0) p.mp=Math.min(p.maxMp,p.mp+3);
  if(p.defBuffT>0){p.defBuffT-=dt;if(p.defBuffT<=0)p.defBuff=0;}
  if(p.buffTimer>0){p.buffTimer-=dt;if(p.buffTimer<=0){p.buffAtk=1;p.buffSpd=1;}}
}

function handleInput(p,dt){
  if(!p.alive) return;
  const spd=spdTotal(p);
  if(KEY['ArrowLeft']){p.vx=-spd*6.2*dt;p.f=-1;}
  if(KEY['ArrowRight']){p.vx=spd*6.2*dt;p.f=1;}

  if((JK['z']||JK['Z'])&&p.jumpCount<2){
    p.vy=-p.jmp;p.jumpCount++;
    spark(p.x-G.cam+p.w/2,p.y+p.h,{n:10,col:['#fff','#ccc'],ub:3,smin:2,smax:4,spread:.8});
    SFX.jump();
  }
  if((JK['x']||JK['X'])&&p.atkCd<=0) doAttack(p);
  if(JK[' ']&&p.dodgeCd<=0){
    p.vx=p.f*26;p.vy=-2;p.inv=44;p.dodgeCd=54;p.dodgeT=24;
    spark(p.x-G.cam+p.w/2,p.y+p.h/2,{n:16,col:[p.col||'#fff','rgba(255,255,255,.5)'],spread:Math.PI*.5,dir:Math.PI,smin:2,smax:5,grav:.04});
    SFX.dodge();
  }
  const skMap={a:0,s:1,d:2,f:3,g:4,A:0,S:1,D:2,F:3,G:4};
  for(const [k,idx] of Object.entries(skMap)){
    if(JK[k]&&p.skills[idx]!==undefined){useSkill(p,idx);break;}
  }
  if(JK['p']||JK['P']){
    G.paused=!G.paused;
    document.getElementById('pause-ov').classList.toggle('hidden',!G.paused);
  }
}

function doAttack(p){
  p.atkCd=14;p.atkFrame=14;p.atkPhase=Math.PI*.5;
  p.combo=Math.min(12,(p.combo||0)+1);p.comboT=90;
  if(p.combo>G.maxCombo) G.maxCombo=p.combo;
  document.getElementById('combo-num').textContent=p.combo+'HIT';
  document.getElementById('combo-num').style.color=p.combo>=6?'#ff4422':p.combo>=3?'#ffcc22':p.col||'#f5c842';
  document.getElementById('combo').style.opacity=p.combo>=2?'1':'0';
  const d=dmg(p,1+(p.combo*.08));
  aoe(p.x+(p.f>0?p.w:-70),p.y-14,76,66,d,false);
  spark(p.x+(p.f>0?p.w+18:-28)-G.cam,p.y+24,{n:d.crit?16:8,col:[p.col||'#fff','#ffcc00'],spread:.7,dir:p.f>0?0:Math.PI,smin:2,smax:d.crit?9:5,glow:d.crit});
  if(d.crit) shake(3,6);
}

function useSkill(p,idx){
  const sk=p.skills[idx];
  if(!sk||p.skillCds[idx]>0||p.mp<sk.mp) return;
  p.mp-=sk.mp;p.skillCds[idx]=sk.cd*60;
  p.atkPhase=Math.PI;
  sk.fn(p,G); SFX.skill();
}

function updatePlayer(p,dt){
  p.vy+=GRAVITY*dt;
  p.x+=p.vx*dt;p.y+=p.vy*dt;
  p.vx*=.80;
  const gy=GY();
  if(p.y+p.h>=gy){p.y=gy-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;}
  else p.onGround=false;
  for(const pl of G.platforms){
    if(p.vy>=0&&p.x+p.w>pl.x&&p.x<pl.x+pl.w&&p.y+p.h>pl.y&&p.y+p.h<pl.y+pl.h+14){
      p.y=pl.y-p.h;p.vy=0;p.onGround=true;p.jumpCount=0;
    }
  }
  p.x=Math.max(5,Math.min(STAGEW-p.w-5,p.x));
  if(p.y>gy+160){p.y=gy-p.h;p.vy=0;}
  G.cam+=(p.x-W()*.38-G.cam)*.1*dt;
  G.cam=Math.max(0,Math.min(STAGEW-W(),G.cam));
  if(Math.abs(p.vx)>.5&&p.onGround) p.walkPhase+=.28*dt*Math.abs(p.vx)*.04;
  p.atkPhase=Math.max(0,p.atkPhase-.14*dt);
  if(p.inv>0) p.inv-=dt;
  if(p.atkCd>0) p.atkCd-=dt;
  if(p.atkFrame>0) p.atkFrame-=dt;
  if(p.hitFlash>0) p.hitFlash-=dt;
  if(p.dodgeCd>0) p.dodgeCd-=dt;
  if(p.dodgeT>0) p.dodgeT-=dt;
  if(p.comboT>0){p.comboT-=dt;if(p.comboT<=0){p.combo=0;document.getElementById('combo').style.opacity='0';}}
  for(let i=0;i<p.skillCds.length;i++) if(p.skillCds[i]>0) p.skillCds[i]-=dt/60;
  p.animFrame+=dt;
}

function updateEnemies(dt){
  const p=G.player,gy=GY();
  for(const e of G.enemies){
    if(!e.alive) continue;
    if(e.hitFlash>0) e.hitFlash-=dt;
    if(e.frozen>0){e.frozen-=dt;continue;}
    if(e.stun>0){e.stun-=dt;continue;}
    if(e.cursed>0) e.cursed-=dt;
    if(e.poison>0){
      e.poison-=dt;
      if(!e.poisonT||e.poisonT<=0){e.hp-=e.pdmg||5;e.poisonT=22;if(e.hp<=0){kill(e);continue;}}
      e.poisonT-=dt;
    }
    const dx=p.x-e.x;
    if(Math.abs(dx)<450) e.aggro=true;
    if(!e.aggro) continue;
    e.f=dx>0?1:-1;
    const spd=(e.spd||2)*(e.cursed>0?.55:1);
    const dist=Math.abs(dx);
    if(e.ai==='ranged'){
      if(dist<200) e.x-=e.f*spd*.7*dt;
      else if(dist>340) e.x+=e.f*spd*.7*dt;
    } else if(e.ai==='slow'){
      if(dist>55) e.x+=e.f*spd*.6*dt;
    } else if(e.ai==='tank'){
      if(dist>65) e.x+=e.f*spd*.55*dt;
    } else {
      if(dist>50) e.x+=e.f*spd*dt;
    }
    e.vy=(e.vy||0)+GRAVITY*dt*.5;e.y+=e.vy*dt;
    if(e.y+e.h>=gy){e.y=gy-e.h;e.vy=0;}
    for(const pl of G.platforms){
      if(e.vy>=0&&e.x+e.w>pl.x&&e.x<pl.x+pl.w&&e.y+e.h>pl.y&&e.y+e.h<pl.y+pl.h+12){
        e.y=pl.y-e.h;e.vy=0;
      }
    }
    e.walkPhase+=.2*dt;e.atkPhase=Math.max(0,e.atkPhase-.12*dt);
    e.atkTimer-=dt;e.animFrame=(e.animFrame||0)+dt;
    if(e.atkTimer<=0&&e.aggro){
      if(e.ai==='ranged'&&dist<370){
        e.atkTimer=100+Math.random()*55;e.atkPhase=Math.PI*.8;
        const vd=dmg({atk:e.atk,atkBonus:0,buffAtk:1,critBonus:0},1);
        proj(e.x+e.w/2,e.y+e.h/2,e.f*11+(Math.random()-.5),( Math.random()-.5)*2,vd,'#aa44ff','enemy',{sz:10,life:85});
      } else if(dist<65&&Math.abs(p.y-e.y)<70){
        e.atkTimer=78+Math.random()*32;e.atkPhase=Math.PI;
        if(p.dodgeT<=0){
          const rd=Math.max(1,e.atk-Math.round(defTotal(p)*.5)+Math.floor(Math.random()*6)-3);
          takeDmg(rd);
        }
      }
    }
  }
}

function updateBoss(dt){
  const b=G.boss,p=G.player;
  if(b.hitFlash>0) b.hitFlash-=dt;
  if(b.frozen>0){b.frozen-=dt;return;}
  if(b.stun>0){b.stun-=dt;return;}
  if(b.cursed>0) b.cursed-=dt;
  const hpPct=b.hp/b.maxHp;
  if(!b.phase2&&hpPct<.55){
    b.phase2=true;b.spd*=1.4;b.atk=Math.round(b.atk*1.3);
    document.getElementById('boss-phase').textContent='⚡ PHASE 2';
    shake(13,45);
    spark(b.x-G.cam+b.w/2,b.y+b.h/2,{n:55,col:['#ff4400','#ff8800'],glow:true,smin:4,smax:12});
  }
  if(!b.phase3&&hpPct<.25){
    b.phase3=true;b.spd*=1.35;b.atk=Math.round(b.atk*1.25);
    document.getElementById('boss-phase').textContent='💀 PHASE 3 ENRAGE';
    shake(20,70);
    spark(b.x-G.cam+b.w/2,b.y+b.h/2,{n:90,col:['#ff0000','#cc00ff','#fff'],glow:true,smin:5,smax:18});
    SFX.boss();
  }
  const dx=p.x-b.x;
  b.f=dx>0?1:-1;
  if(Math.abs(dx)>90) b.x+=b.f*b.spd*dt*.9;
  b.vy=(b.vy||0)+GRAVITY*dt*.42;b.y+=b.vy*dt;
  const gy=GY();
  if(b.y+b.h>=gy){b.y=gy-b.h;b.vy=0;}
  b.x=Math.max(50,Math.min(STAGEW-b.w-50,b.x));
  b.walkPhase+=.1*dt;b.atkPhase=Math.max(0,b.atkPhase-.1*dt);
  b.atkTimer-=dt;b.projTimer-=dt;b.animFrame=(b.animFrame||0)+dt;
  const pi=b.phase3?42:b.phase2?62:95;
  if(b.projTimer<=0){
    b.projTimer=pi;b.atkPhase=Math.PI*.8;
    const bv=dmg({atk:b.atk,atkBonus:0,buffAtk:1,critBonus:0},.65);
    if(b.phase3){
      for(let i=-1;i<=1;i++) proj(b.x+b.w/2,b.y+b.h*.35,b.f*10,i*5,bv,'#ff1100','enemy',{sz:17,emoji:'💥',life:90,grav:.07});
    } else {
      proj(b.x+b.w/2,b.y+b.h*.35,b.f*9,-1.5,bv,'#ff3300','enemy',{sz:16,emoji:'💥',life:90,grav:.09});
    }
  }
  if(b.atkTimer<=0&&Math.abs(dx)<110){
    b.atkTimer=b.phase3?38:b.phase2?52:72;b.atkPhase=Math.PI;
    if(Math.abs(p.y-b.y)<100&&p.inv<=0&&p.dodgeT<=0){
      const rd=Math.max(1,b.atk-Math.round(defTotal(p)*.42)+Math.floor(Math.random()*14)-7);
      takeDmg(rd);
      if(b.phase3) setTimeout(()=>{if(G&&p.hp>0)takeDmg(Math.round(rd*.65));},210);
    }
  }
  document.getElementById('boss-hp-fill').style.width=Math.max(0,hpPct*100)+'%';
}

function takeDmg(v){
  const p=G.player;
  if(p.inv>0) return;
  p.hp-=v;p.hitFlash=14;p.inv=40;G.dmgTaken+=v;
  const fl=document.getElementById('hit-flash');
  fl.style.opacity='1';setTimeout(()=>fl.style.opacity='0',120);
  shake(5,12);
  if(p.hp<=0) gameOver();
}

function updateProjs(dt){
  const p=G.player,gy=GY();
  G.projs=G.projs.filter(pr=>{
    if(!pr.alive) return false;
    pr.x+=pr.vx*dt;pr.y+=pr.vy*dt;pr.vy+=pr.grav*dt;pr.life-=dt;
    if(pr.life<=0) return false;
    if(pr.homing&&pr.owner==='player'){
      const tgts=[...G.enemies,...(G.boss&&G.boss.alive?[G.boss]:[])].filter(e=>e.alive);
      let best=null,bd=999;
      for(const e of tgts){const d=Math.abs(e.x-pr.x)+Math.abs(e.y-pr.y);if(d<bd){bd=d;best=e;}}
      if(best&&bd<500){const ddx=best.x+best.w/2-pr.x,ddy=best.y+best.h/2-pr.y,l=Math.sqrt(ddx*ddx+ddy*ddy)||1;pr.vx+=(ddx/l*3-pr.vx)*.12;pr.vy+=(ddy/l*3-pr.vy)*.12;}
    }
    if(pr.trail) spark(pr.x-G.cam,pr.y,{n:2,col:[pr.col],smin:1,smax:3,grav:0,dmax:.06,spread:Math.PI*.3});
    if(pr.explode&&pr.y>=gy){
      boom(pr.x-G.cam,gy,pr.col);
      aoe(pr.x-70,gy-75,140,90,{v:pr.dmg,crit:pr.crit},false);
      shake(5,10);return false;
    }
    if(pr.y>gy+90||pr.x<G.cam-100||pr.x>G.cam+W()+100) return false;
    if(pr.owner==='player'){
      const tgts=[...G.enemies,...(G.boss&&G.boss.alive?[G.boss]:[])];
      for(const e of tgts){
        if(!e.alive) continue;
        if(pr.x>e.x&&pr.x<e.x+e.w&&pr.y>e.y&&pr.y<e.y+e.h){
          hit(e,pr.dmg,pr.crit,{onHit:pr.onHit});
          spark(pr.x-G.cam,pr.y,{n:9,col:[pr.col,'#fff'],smin:2,smax:5,glow:!!pr.emoji});
          if(!pr.pierce){pr.alive=false;return false;}
        }
      }
    } else {
      const sx=pr.x-G.cam;
      if(p.inv<=0&&p.dodgeT<=0&&sx>p.x-G.cam&&sx<p.x-G.cam+p.w&&pr.y>p.y&&pr.y<p.y+p.h){
        takeDmg(Math.max(1,pr.dmg-Math.round(defTotal(p)*.4)));
        pr.alive=false;return false;
      }
    }
    return true;
  });
}

function updateItems(dt){
  const p=G.player,gy=GY();
  G.items=G.items.filter(it=>{
    if(!it.alive) return false;
    it.vy=(it.vy||0)+GRAVITY*dt*.7;it.y+=it.vy*dt;
    if(it.y+20>=gy){it.y=gy-20;it.vy=0;}
    const sx=it.x-G.cam;
    if(sx>p.x-G.cam-32&&sx<p.x-G.cam+p.w+32&&it.y>p.y-12&&it.y<p.y+p.h+24){
      const res=it.fn(p);
      showDmg(sx|0,it.y|0,'+ '+res,false,'#ffcc00');
      it.alive=false;return false;
    }
    return true;
  });
}

// ═══ RENDER ═══
function render(){
  if(!G){
    CX.fillStyle='#050310';CX.fillRect(0,0,W(),H());
    return;
  }
  CX.save();
  if(G.shakeDur>0){
    const s=G.shakeAmt*(G.shakeDur/22)*.6;
    CX.translate((Math.random()-.5)*s,(Math.random()-.5)*s);
  }
  const st=G.stage;
  drawBackground(st);
  drawPlatforms(st);
  drawFloor(st);
  drawParts(G.cam);
  drawProjectiles();
  drawDropItems();
  drawEnemies();
  if(G.boss&&G.boss.alive) drawBossSprite();
  drawPlayerSprite();
  CX.restore();
}

function drawBackground(st){
  // Deep background gradient
  const grad=CX.createLinearGradient(0,0,0,H());
  grad.addColorStop(0,st.bg);
  grad.addColorStop(.6,st.fl);
  grad.addColorStop(1,'#000');
  CX.fillStyle=grad;CX.fillRect(0,0,W(),H());

  // Parallax background details
  CX.save();CX.globalAlpha=.08;
  CX.fillStyle='#ffffff';
  for(let i=0;i<20;i++){
    const x=((i*173+G.bgScroll*.3)%W()|0);
    const y=(i*97)%(GY()-80);
    CX.fillRect(x,y,2,2+i%4);
  }
  CX.globalAlpha=.04;
  for(let i=0;i<8;i++){
    const x=((i*220+G.bgScroll*.1)%W()|0);
    const y=((i*140)%(GY()-120));
    CX.font='900 28px sans-serif';CX.textAlign='center';
    CX.fillText(['🗡️','💀','⚔️','🏚️'][i%4],x,y);
  }
  CX.restore();

  // Torches flicker
  if(G.timer%5===0){
    spark(W()*.25,GY()-18,{n:1,col:[st.torch||'#ff6600'],glow:true,smin:1,smax:2,ub:2.5,grav:-.02,dmax:.04,spread:.3});
    spark(W()*.75,GY()-18,{n:1,col:[st.torch||'#ff6600'],glow:true,smin:1,smax:2,ub:2.5,grav:-.02,dmax:.04,spread:.3});
  }
  // Torch holders
  CX.fillStyle='rgba(80,50,0,.6)';
  CX.fillRect(W()*.25-4,GY()-28,8,20);
  CX.fillRect(W()*.75-4,GY()-28,8,20);
  CX.fillStyle='rgba(255,150,0,.9)';
  CX.beginPath();CX.arc(W()*.25,GY()-28,5,0,Math.PI*2);CX.fill();
  CX.beginPath();CX.arc(W()*.75,GY()-28,5,0,Math.PI*2);CX.fill();
}

function drawPlatforms(st){
  for(const pl of G.platforms){
    const px=pl.x-G.cam;
    if(px>W()+10||px+pl.w<-10) continue;
    // Platform body
    CX.fillStyle=st.wall||'#0a0618';
    CX.fillRect(px,pl.y,pl.w,pl.h);
    // Top edge highlight
    CX.fillStyle='rgba(255,180,80,.25)';
    CX.fillRect(px,pl.y,pl.w,2);
    // Bottom shadow
    CX.fillStyle='rgba(0,0,0,.5)';
    CX.fillRect(px,pl.y+pl.h-3,pl.w,3);
    // Chain texture
    CX.fillStyle='rgba(255,255,255,.04)';
    for(let i=0;i<pl.w/12;i++) CX.fillRect(px+i*12,pl.y+3,6,pl.h-6);
  }
}

function drawFloor(st){
  const gy=GY();
  // Stone floor tiles
  const tw=64;
  for(let fx=-(G.cam%tw)|0;fx<W();fx+=tw){
    CX.fillStyle=fx%(tw*2)<tw?st.fl:'rgba(0,0,0,.2)';
    CX.fillRect(fx,gy,tw,H()-gy);
    CX.fillStyle='rgba(255,255,255,.03)';
    CX.fillRect(fx,gy,tw,2);
    // Grout lines
    CX.fillStyle='rgba(0,0,0,.3)';
    CX.fillRect(fx,gy,1,H()-gy);
  }
  CX.fillStyle='rgba(255,180,80,.3)';
  CX.fillRect(0,gy,W(),2);
  // Floor depth shadow
  CX.fillStyle='rgba(0,0,0,.4)';
  CX.fillRect(0,gy+2,W(),8);
}

function drawPlayerSprite(){
  const p=G.player;
  const px=p.x-G.cam;
  if(p.inv>0&&Math.floor(G.timer/3)%2===0) return;

  // Afterimages during dodge
  if(p.dodgeT>0){
    for(let i=1;i<=4;i++){
      CX.save();CX.globalAlpha=(p.dodgeT/24)*(i/4)*.22;
      drawCharSprite(p, px-p.f*i*20, p.y, i%2===0);
      CX.restore();
    }
  }
  // Shadow
  CX.globalAlpha=.3;CX.fillStyle='#000';
  CX.beginPath();CX.ellipse(px+p.w/2,GY()+6,p.w*.45,7,0,0,Math.PI*2);CX.fill();
  CX.globalAlpha=1;
  drawCharSprite(p, px, p.y, false);
}

function drawCharSprite(p, sx, sy, ghost=false){
  const action=p.atkFrame>0?'atk':Math.abs(p.vx)>.5&&p.onGround?'walk':'idle';
  let sprite;
  switch(p.spriteType){
    case 'mage': sprite=makeMageSprite(p.pal,p.animFrame,action); break;
    case 'rogue': sprite=makeRogueSprite(p.pal,p.animFrame,action); break;
    case 'gunner': sprite=makeGunnerSprite(p.pal,p.animFrame,action); break;
    default: sprite=makeWarriorSprite(p.pal,p.animFrame,action); break;
  }
  CX.save();
  if(p.hitFlash>0) CX.filter='brightness(4) saturate(0)';
  if(p.buffAtk>1){CX.shadowColor='#ff6600';CX.shadowBlur=14;}
  drawSprite(CX, sprite, sx, sy, p.f<0, ghost?.4:1);
  CX.shadowBlur=0;CX.filter='none';
  CX.restore();
}

function drawEnemies(){
  for(const e of G.enemies){
    if(!e.alive) continue;
    const ex=e.x-G.cam;
    if(ex<-120||ex>W()+120) continue;
    drawEnemyEntity(e, ex);
  }
}

function drawEnemyEntity(e, ex){
  const hpPct=e.hp/e.maxHp;
  const sc=e.drawScale||1;
  const sprite=makeEnemySprite(e.type,e.animFrame||0,hpPct);

  CX.save();
  if(e.hitFlash>0) CX.filter='brightness(4) saturate(0)';
  if(e.frozen>0) CX.filter='hue-rotate(200deg) brightness(1.8) saturate(2)';
  if(e.poison>0){CX.shadowColor='#44cc44';CX.shadowBlur=8;}
  if(e.cursed>0){CX.shadowColor='#cc44cc';CX.shadowBlur=8;}

  // Scale up
  CX.translate(ex+e.w/2, e.y+e.h);
  CX.scale(sc,sc);
  CX.translate(-sprite.w*PX/2, -sprite.h*PX);

  if(e.f>0) CX.scale(-1,1),CX.translate(-sprite.w*PX,0);
  sprite.draw(CX);

  CX.shadowBlur=0;CX.filter='none';
  CX.restore();

  // HP bar
  if(e.hp<e.maxHp){
    const bw=Math.max(40,e.w+8), bx=ex+e.w/2-bw/2, by=e.y-12;
    CX.fillStyle='rgba(0,0,0,.7)';CX.fillRect(bx,by,bw,6);
    CX.fillStyle=hpPct>.5?'#22cc22':hpPct>.25?'#ccaa00':'#cc2200';
    CX.fillRect(bx,by,bw*hpPct,6);
    if(e.frozen>0){CX.fillStyle='rgba(100,180,255,.5)';CX.fillRect(bx,by,bw,6);}
    if(e.poison>0){CX.fillStyle='rgba(50,200,50,.3)';CX.fillRect(bx,by,bw*hpPct,6);}
  }
}

function drawBossSprite(){
  const b=G.boss;
  const ex=b.x-G.cam;
  if(ex<-200||ex>W()+200) return;
  drawEnemyEntity(b, ex);
}

function drawProjectiles(){
  for(const pr of G.projs){
    const px=pr.x-G.cam;
    if(px<-30||px>W()+30) continue;
    if(pr.emoji){
      CX.font=`${pr.sz*1.8}px serif`;
      CX.textAlign='center';CX.textBaseline='middle';
      CX.fillText(pr.emoji,px,pr.y);
    } else {
      CX.save();
      CX.fillStyle=pr.col;CX.shadowColor=pr.col;CX.shadowBlur=14;
      CX.beginPath();CX.arc(px,pr.y,pr.sz,0,Math.PI*2);CX.fill();
      CX.shadowBlur=0;CX.restore();
    }
  }
}

function drawDropItems(){
  for(const it of G.items){
    if(!it.alive) continue;
    const ix=it.x-G.cam;
    if(ix<-30||ix>W()+30) continue;
    CX.save();
    CX.shadowColor='#f5c842';CX.shadowBlur=14;
    const bob=Math.sin(G.timer*.09+it.x*.01)*3;
    CX.font='22px serif';CX.textAlign='center';CX.textBaseline='middle';
    CX.fillText(it.icon,ix,it.y+bob);
    CX.shadowBlur=0;CX.restore();
  }
}

// ═══ HUD ═══
function updateHUD(){
  if(!G) return;
  const p=G.player;
  document.getElementById('hp-bar').style.width=Math.max(0,p.hp/p.maxHp*100)+'%';
  document.getElementById('mp-bar').style.width=Math.max(0,p.mp/p.maxMp*100)+'%';
  document.getElementById('xp-bar').style.width=Math.min(100,p.xp/p.xpNext*100)+'%';
  document.getElementById('hp-val').textContent=Math.max(0,p.hp)+'/'+ p.maxHp;
  document.getElementById('s-lv').textContent=p.level;
  document.getElementById('s-atk').textContent=Math.round(atkTotal(p));
  document.getElementById('s-def').textContent=Math.round(defTotal(p));
  document.getElementById('s-gold').textContent=p.gold;
  document.getElementById('s-score').textContent=p.score;
  document.getElementById('floor-badge').textContent=(G.stageIdx+1)+'F';
  const alv=G.enemies.filter(e=>e.alive).length+(G.boss&&G.boss.alive?1:0);
  document.getElementById('kill-counter').textContent=`처치: ${p.kills} | 남은 적: ${alv}`;
  // Skills
  const sl=document.getElementById('sk-slots');sl.innerHTML='';
  for(let i=0;i<p.skills.length;i++){
    const sk=p.skills[i],cd=p.skillCds[i],rdy=cd<=0&&p.mp>=sk.mp;
    const d=document.createElement('div');
    d.className='sk '+(rdy?'ready':'')+(cd<=0&&p.mp<sk.mp?' cooling':'');
    d.innerHTML=`<div class="sk-icon">${sk.icon}</div><span class="sk-key">${sk.key}</span><span class="sk-mp">${sk.mp}</span>`;
    if(cd>0){const c=document.createElement('div');c.className='sk-cd';c.textContent=cd>60?Math.ceil(cd/60)+'s':cd.toFixed(1);d.appendChild(c);}
    d.title=`${sk.n} [${sk.key}] MP:${sk.mp} CD:${sk.cd}s`;
    sl.appendChild(d);
  }
}
function updateEquipUI(){}

// ═══ DAMAGE NUMBERS ═══
function showDmg(sx,sy,v,crit,col){
  const el=document.createElement('div');
  el.className='dmg';
  const garea=document.getElementById('ui');
  const gy=garea.getBoundingClientRect();
  el.style.cssText=`left:${sx+gy.left}px;top:${sy+50}px;font-size:${crit?'1.4':'0.95'}rem;color:${crit?'#ffff00':(col||'#fff')};`;
  el.textContent=crit?v+'!':v;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),1000);
}

// ═══ STAGE FLOW ═══
function stageClear(){
  G.phase='clear';
  const p=G.player;
  const t=Math.round((Date.now()-G.startTime)/1000);
  const bonus=G.dmgTaken===0?5000:0;
  p.score+=bonus;
  document.getElementById('clear-grid').innerHTML=`
    <div class="rc">처치 수 <b>${p.kills}</b></div>
    <div class="rc">골드 <b>💰${p.gold}</b></div>
    <div class="rc">점수 <b>${p.score}</b></div>
    <div class="rc">클리어 타임 <b>${t}초</b></div>
    <div class="rc">레벨 <b>Lv.${p.level}</b></div>
    <div class="rc">무피해 보너스 <b>${bonus?'+5000':'없음'}</b></div>`;
  document.getElementById('clear-ov').classList.remove('hidden');
}

function gameOver(){
  if(!G||G.phase!=='play') return;
  G.phase='over';G.player.alive=false;
  const p=G.player;
  document.getElementById('over-grid').innerHTML=`
    <div class="rc">처치 수 <b>${p.kills}</b></div>
    <div class="rc">골드 <b>💰${p.gold}</b></div>
    <div class="rc">점수 <b>${p.score}</b></div>
    <div class="rc">레벨 <b>Lv.${p.level}</b></div>
    <div class="rc">스테이지 <b>${G.stageIdx+1}F</b></div>
    <div class="rc">최대 콤보 <b>${G.maxCombo}HIT</b></div>`;
  setTimeout(()=>document.getElementById('over-ov').classList.remove('hidden'),800);
  SFX.death();
}

function openShop(){
  document.getElementById('clear-ov').classList.add('hidden');
  buildShop();
  document.getElementById('shop-ov').classList.remove('hidden');
}

function buildShop(){
  const p=G.player;
  document.getElementById('sg-val').textContent=p.gold;
  const pool=[...SHOP].sort(()=>Math.random()-.5).slice(0,6);
  G.shopStock=pool.map((it,i)=>({...it,uid:'s'+i,price:it.price+G.stageIdx*28}));
  document.getElementById('shop-grid').innerHTML=G.shopStock.map((it,i)=>`
    <div class="shop-item ${p.gold<it.price?'cant':''}" onclick="buyItem(${i})">
      <div class="si-icon">${it.icon}</div>
      <div class="si-name">${it.n}</div>
      <div class="si-desc">${it.desc}</div>
      <div class="si-price">${it.price}💰</div>
    </div>`).join('');
}

function buyItem(i){
  const p=G.player,it=G.shopStock[i];
  if(!it||p.gold<it.price) return;
  p.gold-=it.price;it.fn(p);SFX.buy();buildShop();
}

function nextStage(){
  document.getElementById('shop-ov').classList.add('hidden');
  initGame(G.clsId,(G.stageIdx+1)%STAGES.length);
}

function retryStage(){
  document.getElementById('over-ov').classList.add('hidden');
  initGame(G.clsId,G.stageIdx);
}

function gotoTitle(){
  ['clear-ov','over-ov','shop-ov','lvl-ov','pause-ov'].forEach(id=>document.getElementById(id).classList.add('hidden'));
  document.getElementById('title-ov').classList.remove('hidden');
  document.getElementById('boss-ui').classList.remove('visible');
  G=null;
}

// ═══ LEVEL UP ═══
function showLvlModal(){
  document.getElementById('stat-grid').innerHTML=`
    <button class="spbtn" onclick="pickStat('hp')">❤️ 최대 HP +30</button>
    <button class="spbtn" onclick="pickStat('atk')">⚔️ ATK +6</button>
    <button class="spbtn" onclick="pickStat('def')">🛡️ DEF +4</button>
    <button class="spbtn" onclick="pickStat('spd')">💨 SPD +0.6</button>
    <button class="spbtn" onclick="pickStat('mp')">🔷 최대 MP +22</button>
    <button class="spbtn" onclick="pickStat('crit')">⚡ 크리 +6%</button>`;
  document.getElementById('lvl-ov').classList.remove('hidden');
}

function pickStat(s){
  const p=G.player;
  if(s==='hp'){p.maxHp+=30;p.hp=Math.min(p.maxHp,p.hp+30);}
  else if(s==='atk') p.atk+=6;
  else if(s==='def') p.def+=4;
  else if(s==='spd') p.spd+=.6;
  else if(s==='mp'){p.maxMp+=22;p.mp=Math.min(p.maxMp,p.mp+22);}
  else if(s==='crit') p.critBonus=(p.critBonus||0)+.06;
  document.getElementById('lvl-ov').classList.add('hidden');
  G.pendLvl=false;
}

// ═══ TITLE SCREEN ═══
function buildTitle(){
  const row=document.getElementById('class-select');row.innerHTML='';
  for(const [id,c] of Object.entries(CLASSES)){
    const d=document.createElement('div');
    d.className='cls-card';d.id='cc-'+id;
    d.onclick=()=>{selCls=id;document.querySelectorAll('.cls-card').forEach(x=>x.classList.remove('sel'));d.classList.add('sel');document.getElementById('start-btn').disabled=false;ac();};
    d.innerHTML=`<span class="cls-emoji">${c.icon}</span>
      <div class="cls-name">${c.name}</div>
      <div class="cls-type">${c.desc.slice(0,18)}...</div>
      <div class="cls-tags">${c.tags.map(t=>`<span class="tag">${t}</span>`).join('')}</div>`;
    row.appendChild(d);
  }
}

function startGame(){
  if(!selCls) return;
  document.getElementById('title-ov').classList.add('hidden');
  initGame(selCls,0);
}

// ═══ ACHIEVEMENT ═══
let _achT=null;
function achieve(icon,title,sub){
  const el=document.getElementById('achievement');
  document.getElementById('ach-ico').textContent=icon;
  document.getElementById('ach-t').textContent=title;
  document.getElementById('ach-s').textContent=sub;
  el.classList.add('show');
  clearTimeout(_achT);
  _achT=setTimeout(()=>el.classList.remove('show'),3400);
}

// ═══ TITLE ANIMATION ═══
function titleLoop(t){
  if(G) return;
  CX.fillStyle='#050310';CX.fillRect(0,0,W(),H());
  // Animated background
  CX.save();
  for(let i=0;i<5;i++){
    const x=W()/2+(Math.cos(t*.0003+i*1.2)*W()*.35);
    const y=H()/2+(Math.sin(t*.0004+i*.9)*H()*.3);
    const g=CX.createRadialGradient(x,y,0,x,y,150);
    g.addColorStop(0,['rgba(255,80,0,.05)','rgba(0,80,255,.04)','rgba(150,0,255,.04)','rgba(255,200,0,.04)','rgba(255,0,80,.04)'][i]);
    g.addColorStop(1,'transparent');
    CX.fillStyle=g;CX.fillRect(0,0,W(),H());
  }
  CX.restore();
  tickParts(1);drawParts(0);
  if(Math.random()<.4) spark(Math.random()*W(),Math.random()*H(),{n:2,col:['#ff6600','#ffaa00','#cc44ff'],glow:true,smin:1,smax:3,grav:-.02,dmin:.008,dmax:.014});
  requestAnimationFrame(titleLoop);
}

buildTitle();
requestAnimationFrame(titleLoop);
requestAnimationFrame(loop);
</script>
</body>
</html>
 
    """
    components.html(game_html_code, height=800, scrolling=False)
