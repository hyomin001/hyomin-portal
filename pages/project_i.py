import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>전장 저격전 v4</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Black+Han+Sans&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#03060e;--gold:#ffd700;--green:#10d96e;--red:#ff3355;
  --blue:#4dabf7;--cyan:#22d3ee;--orange:#ff8c42;--purple:#b26cf7;
  --text:#e8f0ff;--text2:#7a8fb5;--text3:#4a5f85;
  --panel:rgba(5,10,22,0.97);--border:rgba(255,255,255,0.07);
}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);overflow:hidden;width:100%;height:100%;user-select:none;}
#diff-select{position:fixed;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#03060e;background-image:radial-gradient(ellipse 80% 60% at 50% 25%,rgba(255,51,85,.08) 0%,transparent 65%);overflow-y:auto;padding:20px 16px;}
.ds-logo{font-size:3.2rem;margin-bottom:6px;animation:logoPulse 2.5s ease-in-out infinite;}
@keyframes logoPulse{0%,100%{filter:drop-shadow(0 0 18px rgba(255,69,96,.6));}50%{filter:drop-shadow(0 0 36px rgba(255,140,66,1));}}
.ds-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.8rem,5vw,3rem);background:linear-gradient(135deg,#ff3355,#ff8c42,#ffd700,#22d3ee);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:4px;margin-bottom:4px;text-align:center;}
.ds-sub{color:var(--text2);font-size:.72rem;letter-spacing:6px;margin-bottom:5px;text-align:center;}
.ds-ver{display:inline-block;background:rgba(255,140,66,.12);border:1px solid rgba(255,140,66,.4);color:var(--orange);border-radius:20px;padding:2px 14px;font-size:.68rem;font-weight:700;margin-bottom:20px;letter-spacing:2px;}
.diff-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:680px;width:95%;margin-bottom:16px;}
@media(min-width:600px){.diff-grid{grid-template-columns:repeat(4,1fr);max-width:860px;}}
.diff-card{background:rgba(255,255,255,.025);border:2px solid rgba(255,255,255,.07);border-radius:18px;padding:16px 10px;cursor:pointer;transition:all .25s;text-align:center;position:relative;overflow:hidden;}
.diff-card::before{content:'';position:absolute;inset:0;opacity:0;transition:opacity .25s;border-radius:16px;}
.diff-card[data-d="0"]::before{background:radial-gradient(ellipse at 50% -10%,rgba(16,217,110,.18),transparent 65%);}
.diff-card[data-d="1"]::before{background:radial-gradient(ellipse at 50% -10%,rgba(77,171,247,.18),transparent 65%);}
.diff-card[data-d="2"]::before{background:radial-gradient(ellipse at 50% -10%,rgba(255,140,66,.18),transparent 65%);}
.diff-card[data-d="3"]::before{background:radial-gradient(ellipse at 50% -10%,rgba(255,51,85,.2),transparent 65%);}
.diff-card:hover::before,.diff-card.sel::before{opacity:1;}
.diff-card:hover,.diff-card.sel{transform:translateY(-5px);}
.diff-card[data-d="0"]:hover,.diff-card[data-d="0"].sel{border-color:#10d96e;box-shadow:0 8px 32px rgba(16,217,110,.22);}
.diff-card[data-d="1"]:hover,.diff-card[data-d="1"].sel{border-color:#4dabf7;box-shadow:0 8px 32px rgba(77,171,247,.22);}
.diff-card[data-d="2"]:hover,.diff-card[data-d="2"].sel{border-color:#ff8c42;box-shadow:0 8px 32px rgba(255,140,66,.22);}
.diff-card[data-d="3"]:hover,.diff-card[data-d="3"].sel{border-color:#ff3355;box-shadow:0 8px 40px rgba(255,51,85,.3);}
.diff-em{font-size:2rem;margin-bottom:5px;}.diff-name{font-family:'Black Han Sans',sans-serif;font-size:1.1rem;margin-bottom:4px;}
.diff-desc{font-size:.66rem;color:var(--text2);line-height:1.75;margin-bottom:8px;}
.diff-tag{display:inline-block;font-size:.57rem;font-weight:700;border-radius:20px;padding:2px 9px;margin-bottom:6px;}
.diff-meters{display:flex;flex-direction:column;gap:3px;margin-top:4px;}
.diff-meter-row{display:flex;align-items:center;gap:5px;font-size:.55rem;color:var(--text3);}
.diff-meter-bar{flex:1;height:3px;background:rgba(255,255,255,.07);border-radius:2px;overflow:hidden;}
.diff-meter-fill{height:100%;border-radius:2px;}
.feat-row{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:860px;margin-bottom:16px;}
.feat-pill{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:20px;padding:3px 10px;font-size:.65rem;color:var(--text2);}
.feat-pill b{color:var(--cyan);}
.start-btn{padding:14px 60px;font-size:1.1rem;font-weight:900;font-family:'Black Han Sans',sans-serif;background:linear-gradient(135deg,#ff3355,#ff8c42);color:#fff;border:none;border-radius:50px;cursor:pointer;letter-spacing:3px;transition:all .22s;box-shadow:0 0 40px rgba(255,51,85,.4);}
.start-btn:hover{transform:scale(1.06) translateY(-2px);box-shadow:0 0 60px rgba(255,51,85,.65);}
.keyhint{margin-top:10px;font-size:.6rem;color:var(--text3);text-align:center;letter-spacing:1px;line-height:1.8;}
#game{display:none;width:100%;height:100vh;flex-direction:column;overflow:hidden;position:fixed;inset:0;}
.hud{background:var(--panel);border-bottom:1px solid var(--border);padding:4px 10px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:3px;z-index:50;height:46px;min-height:46px;flex-shrink:0;}
.hud-left,.hud-right{display:flex;align-items:center;gap:6px;}
.hud-title{font-family:'Orbitron',sans-serif;font-size:.68rem;font-weight:900;color:var(--orange);letter-spacing:2px;}
.base-grp{display:flex;align-items:center;gap:4px;}.base-lbl{font-size:.6rem;color:var(--text2);font-weight:700;}
.hp-bar-wrap{width:80px;height:8px;background:rgba(255,255,255,.06);border-radius:4px;overflow:hidden;border:1px solid rgba(255,255,255,.07);}
.hp-fill{height:100%;border-radius:4px;transition:width .35s;}
.hp-fill.ally{background:linear-gradient(90deg,var(--green),var(--cyan));}
.hp-fill.enemy{background:linear-gradient(90deg,var(--red),var(--orange));}
.hp-num{font-size:.62rem;font-weight:700;min-width:24px;}
.badge{border-radius:7px;padding:2px 7px;font-size:.66rem;font-weight:700;display:flex;align-items:center;gap:3px;}
.badge-res{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.25);color:var(--gold);animation:resGlow 2.5s ease-in-out infinite;}
.badge-wave{background:rgba(178,108,247,.1);border:1px solid rgba(178,108,247,.25);color:var(--purple);}
.badge-score{background:rgba(34,211,238,.1);border:1px solid rgba(34,211,238,.25);color:var(--cyan);}
.badge-kills{background:rgba(255,51,85,.1);border:1px solid rgba(255,51,85,.25);color:var(--red);}
.badge-diff{font-size:.6rem;padding:2px 8px;border-radius:16px;font-weight:700;}
.badge-weather{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);color:var(--text2);font-size:.6rem;padding:2px 7px;border-radius:7px;}
#wave-bar{height:3px;background:rgba(178,108,247,.12);flex-shrink:0;position:relative;overflow:hidden;}
#wave-fill{height:100%;position:absolute;left:0;top:0;background:linear-gradient(90deg,var(--purple),var(--cyan),var(--green));transition:width .5s;}
#lane-status{position:fixed;top:49px;left:0;right:0;z-index:48;background:rgba(5,8,15,.93);border-bottom:1px solid rgba(255,255,255,.06);display:flex;align-items:center;padding:2px 10px;gap:8px;height:24px;}
.ls-lane{display:flex;align-items:center;gap:4px;flex:1;}
.ls-name{font-size:.56rem;font-weight:900;min-width:20px;}
.ls-bar-wrap{flex:1;height:5px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden;position:relative;}
.ls-ally-fill{position:absolute;left:0;top:0;height:100%;border-radius:3px 0 0 3px;transition:width .4s;}
.ls-enemy-fill{position:absolute;right:0;top:0;height:100%;border-radius:0 3px 3px 0;transition:width .4s;}
.ls-units{font-size:.5rem;color:var(--text2);min-width:24px;text-align:center;}
#deploy-indicator{font-size:.58rem;font-weight:900;margin-left:4px;white-space:nowrap;}
#battlefield{display:block;width:100%;flex:1;min-height:0;cursor:crosshair;}
#minimap{position:fixed;bottom:92px;right:8px;z-index:200;background:rgba(3,6,14,.95);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:4px;width:122px;height:70px;}
#minimap canvas{display:block;border-radius:7px;}
.minimap-label{font-size:.44rem;color:rgba(255,255,255,.3);text-align:center;margin-top:2px;letter-spacing:2px;}
#upgrade-panel{position:fixed;bottom:92px;left:8px;z-index:200;background:rgba(3,6,14,.97);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:10px;width:200px;display:none;}
.up-title{font-size:.68rem;font-weight:900;color:var(--gold);margin-bottom:8px;}
.up-row{display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;gap:6px;}
.up-name{font-size:.58rem;color:var(--text2);flex:1;}
.up-bars{display:flex;gap:2px;}
.up-pip{width:10px;height:6px;border-radius:2px;background:rgba(255,255,255,.1);}
.up-pip.on{background:var(--cyan);}
.up-btn{font-size:.52rem;background:rgba(34,211,238,.12);border:1px solid rgba(34,211,238,.3);color:var(--cyan);border-radius:6px;padding:2px 6px;cursor:pointer;white-space:nowrap;}
.up-btn:hover{background:rgba(34,211,238,.25);}.up-btn:disabled{opacity:.35;cursor:not-allowed;}
.bot-panel{background:var(--panel);border-top:1px solid var(--border);padding:4px 7px;display:flex;align-items:center;gap:3px;z-index:50;height:86px;min-height:86px;flex-shrink:0;overflow:hidden;}
.lane-sel{display:flex;flex-direction:column;gap:3px;flex-shrink:0;margin-right:4px;}
.lane-sel-title{font-size:.48rem;color:var(--text3);text-align:center;letter-spacing:1px;}
.lane-btn{padding:3px 9px;border-radius:7px;border:1.5px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);color:var(--text2);font-size:.6rem;font-weight:900;cursor:pointer;transition:all .18s;white-space:nowrap;}
.lane-btn:hover{border-color:var(--cyan);color:var(--cyan);}
.top-active{border-color:var(--purple)!important;background:rgba(178,108,247,.14)!important;color:var(--purple)!important;}
.mid-active{border-color:var(--cyan)!important;background:rgba(34,211,238,.14)!important;color:var(--cyan)!important;}
.bot-active{border-color:var(--green)!important;background:rgba(16,217,110,.14)!important;color:var(--green)!important;}
.fallen{border-color:rgba(255,51,85,.35)!important;background:rgba(255,51,85,.07)!important;color:rgba(255,51,85,.5)!important;cursor:not-allowed!important;}
.unit-btn{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);border-radius:10px;padding:3px 4px;cursor:pointer;transition:all .18s;text-align:center;min-width:52px;max-width:58px;position:relative;flex-shrink:0;pointer-events:auto;}
.unit-btn:hover:not(:disabled){transform:translateY(-3px);border-color:var(--cyan);background:rgba(34,211,238,.07);box-shadow:0 0 14px rgba(34,211,238,.2);}
.unit-btn:disabled{opacity:.3;cursor:not-allowed;}
.unit-btn .key-badge{position:absolute;top:2px;left:3px;font-size:.46rem;color:var(--text3);font-weight:900;}
.unit-btn .uem{font-size:.95rem;display:block;margin-bottom:1px;}.unit-btn .uname{font-size:.5rem;font-weight:700;display:block;}
.unit-btn .ucost{font-size:.48rem;color:var(--gold);display:block;}.unit-btn .ulv{font-size:.44rem;color:var(--purple);display:block;}
.unit-btn .ucool{height:3px;background:rgba(255,255,255,.08);border-radius:2px;margin-top:2px;overflow:hidden;}
.unit-btn .ucool-fill{height:100%;background:var(--cyan);border-radius:2px;transition:width .1s linear;}
.ability-row{display:flex;gap:3px;margin-left:auto;align-items:center;flex-shrink:0;}
.abil-btn{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);border-radius:10px;padding:3px 4px;cursor:pointer;text-align:center;min-width:44px;transition:all .2s;position:relative;pointer-events:auto;}
.abil-btn:hover:not(.cooldown){border-color:var(--gold);background:rgba(255,215,0,.07);}
.abil-btn.cooldown{opacity:.35;cursor:not-allowed;}
.abil-btn .aem{font-size:.85rem;display:block;}.abil-btn .aname{font-size:.46rem;font-weight:700;color:var(--gold);}
.abil-btn .acool{font-size:.44rem;color:var(--text2);}
.abil-cd-bar{position:absolute;bottom:0;left:0;height:3px;background:var(--gold);border-radius:0 0 8px 8px;transition:width .1s linear;}
.snipe-hint{font-size:.54rem;color:var(--text2);line-height:1.6;padding-left:7px;border-left:2px solid rgba(255,255,255,.07);flex-shrink:0;}
#scope{position:fixed;pointer-events:none;z-index:1000;display:none;transform:translate(-50%,-50%);left:-999px;top:-999px;}
#hs-flash{position:fixed;inset:0;pointer-events:none;z-index:900;background:rgba(255,215,0,0);transition:background .06s;}
#night-overlay{position:fixed;inset:0;pointer-events:none;z-index:45;background:rgba(0,0,30,0);transition:background 3s;}
#freeze-overlay{position:fixed;inset:0;pointer-events:none;z-index:44;background:rgba(80,160,255,0);transition:background .3s;}
#fw{position:fixed;inset:0;pointer-events:none;z-index:490;overflow:hidden;}
@keyframes fwp{to{transform:translate(var(--dx),var(--dy));opacity:0;}}
#killfeed{position:fixed;top:56px;right:10px;z-index:200;display:flex;flex-direction:column;gap:3px;pointer-events:none;}
.kfi{background:rgba(3,6,14,.93);border:1px solid rgba(255,51,85,.28);border-radius:7px;padding:3px 9px;font-size:.62rem;font-weight:700;animation:kfIn .2s,kfOut .3s 2.5s forwards;white-space:nowrap;}
@keyframes kfIn{from{opacity:0;transform:translateX(18px);}to{opacity:1;transform:none;}}
@keyframes kfOut{to{opacity:0;transform:translateX(18px);}}
#twrap{position:fixed;top:56px;left:50%;transform:translateX(-50%);z-index:600;display:flex;flex-direction:column;align-items:center;gap:4px;pointer-events:none;}
.toast{padding:5px 12px;border-radius:8px;font-size:.7rem;font-weight:700;background:rgba(5,10,22,.97);border:1px solid rgba(255,255,255,.1);animation:ti .22s,to2 .22s 2.4s forwards;white-space:nowrap;}
@keyframes ti{from{opacity:0;transform:translateY(-7px);}to{opacity:1;transform:none;}}
@keyframes to2{to{opacity:0;transform:translateY(-7px);}}
.hs-toast{padding:9px 22px;border-radius:12px;font-size:.88rem;font-weight:900;background:rgba(255,215,0,.14);border:2px solid rgba(255,215,0,.55);color:var(--gold);text-shadow:0 0 12px var(--gold);animation:ti .15s,to2 .15s 1.9s forwards;font-family:'Black Han Sans',sans-serif;}
#boss-alert{position:fixed;inset:0;z-index:400;pointer-events:none;display:none;align-items:center;justify-content:center;}
.ba-box{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.8rem,5.5vw,3.6rem);text-align:center;animation:baAnim 2.4s ease-out forwards;}
@keyframes baAnim{0%{opacity:0;transform:scale(.4);}28%{opacity:1;transform:scale(1.08);}65%{opacity:1;transform:scale(1);}100%{opacity:0;transform:scale(1.15);}}
#shop-modal{display:none;position:fixed;inset:0;z-index:450;background:rgba(0,0,0,.82);align-items:center;justify-content:center;backdrop-filter:blur(10px);}
.shop-box{background:linear-gradient(160deg,#0a1530,#172045);border:1px solid rgba(255,255,255,.09);border-radius:20px;padding:22px;max-width:600px;width:95%;box-shadow:0 40px 100px rgba(0,0,0,.7);max-height:84vh;overflow-y:auto;}
.shop-ttl{font-family:'Black Han Sans',sans-serif;font-size:1.3rem;color:var(--gold);margin-bottom:3px;}
.shop-sub{color:var(--text2);font-size:.7rem;margin-bottom:8px;}
.shop-tabs{display:flex;gap:6px;margin-bottom:12px;}
.shop-tab{padding:4px 12px;border-radius:20px;border:1px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);color:var(--text2);font-size:.65rem;cursor:pointer;transition:all .18s;}
.shop-tab.active{border-color:var(--gold);background:rgba(255,215,0,.1);color:var(--gold);}
.shop-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:14px;}
.si{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:11px;padding:9px 7px;text-align:center;cursor:pointer;transition:all .2s;}
.si:hover:not(.bought){border-color:var(--gold);background:rgba(255,215,0,.07);}.si.bought{opacity:.42;cursor:not-allowed;}
.si .se{font-size:1.35rem;display:block;margin-bottom:2px;}.si .sn{font-size:.66rem;font-weight:700;display:block;margin-bottom:2px;}
.si .sd{font-size:.56rem;color:var(--text2);display:block;margin-bottom:3px;}.si .sc{font-size:.62rem;color:var(--gold);font-weight:700;}
.shop-close{padding:8px 24px;border-radius:30px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.04);color:var(--text2);cursor:pointer;font-size:.82rem;font-weight:700;transition:all .2s;}
.shop-close:hover{border-color:var(--red);color:var(--red);}
#result{display:none;position:fixed;inset:0;z-index:500;background:rgba(3,6,14,.98);flex-direction:column;align-items:center;justify-content:center;}
.res-grade{font-family:'Black Han Sans',sans-serif;font-size:4rem;margin-bottom:10px;text-shadow:0 0 30px currentColor;animation:gradePop .4s cubic-bezier(.2,.8,.3,1);}
@keyframes gradePop{from{transform:scale(0) rotate(-15deg);}to{transform:scale(1) rotate(0);}}
.res-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,5vw,3.2rem);margin-bottom:6px;}
.res-sub{font-size:.8rem;color:var(--text2);margin-bottom:22px;letter-spacing:2px;}
.res-grid{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:16px;padding:18px 22px;margin-bottom:20px;display:grid;grid-template-columns:repeat(5,1fr);gap:10px;min-width:380px;}
.ri{text-align:center;}.ri-v{font-size:1.2rem;font-weight:900;color:var(--gold);}.ri-l{font-size:.62rem;color:var(--text2);margin-top:2px;}
.res-btns{display:flex;gap:10px;}
.rbtn{padding:11px 32px;font-size:.85rem;font-weight:900;border:none;border-radius:36px;cursor:pointer;letter-spacing:2px;transition:all .2s;font-family:'Black Han Sans',sans-serif;}
.rbtn.main{background:linear-gradient(135deg,var(--gold),#ff8c00);color:#1a0500;}.rbtn.main:hover{transform:scale(1.05);}
.rbtn.menu{background:rgba(255,255,255,.06);color:var(--text2);border:1px solid rgba(255,255,255,.12);}.rbtn.menu:hover{border-color:var(--cyan);color:var(--cyan);}
@keyframes comboFlash{0%{transform:scale(1.6);}100%{transform:scale(1);}}.combo-flash{animation:comboFlash .18s ease-out;}
@keyframes resGlow{0%,100%{box-shadow:0 0 4px rgba(255,215,0,.25);}50%{box-shadow:0 0 14px rgba(255,215,0,.6);}}
</style>
</head>
<body>
<div id="fw"></div>
<div id="night-overlay"></div>
<div id="hs-flash"></div>

<!-- DIFF SELECT -->
<div id="diff-select">
  <div class="ds-logo">⚔️</div>
  <div class="ds-title">전장 저격전</div>
  <div class="ds-sub">3-LANE BATTLEFIELD · SNIPER REMASTERED</div>
  <div class="ds-ver">VERSION 6.0 · FULL REMASTER</div>
  <div class="feat-row">
    <div class="feat-pill">🗺️ <b>탑·미드·봇</b> 3라인</div>
    <div class="feat-pill">🎯 <b>헤드샷+크리티컬</b></div>
    <div class="feat-pill">💎 <b>유닛 업그레이드</b></div>
    <div class="feat-pill">🛒 <b>탭별 상점</b> 24종</div>
    <div class="feat-pill">💥 <b>스킬 6종</b></div>
    <div class="feat-pill">👹 <b>보스 4패턴</b></div>
    <div class="feat-pill">🌦️ <b>날씨 6종</b></div>
    <div class="feat-pill">🔥 <b>극악: 즉시 러시</b></div>
    <div class="feat-pill">⚡ <b>콤보 x15</b></div>
    <div class="feat-pill">🛸 <b>드론폭격 Y키</b></div>
    <div class="feat-pill">🔧 <b>X=긴급수리</b></div>
    <div class="feat-pill">★ <b>별 3단계 강화</b></div>
  </div>
  <div style="font-size:.65rem;color:var(--text2);letter-spacing:4px;margin-bottom:12px;text-align:center;">— 난이도 선택 —</div>
  <div class="diff-grid">
    <div class="diff-card sel" data-d="0">
      <div class="diff-em">🟢</div>
      <div class="diff-name" style="color:#10d96e">초 보</div>
      <div class="diff-desc">천천히 학습<br>20초 후 적 등장<br>풍부한 자원+힌트</div>
      <div class="diff-tag" style="background:rgba(16,217,110,.12);color:#10d96e;border:1px solid rgba(16,217,110,.3);">추천 입문</div>
      <div class="diff-meters">
        <div class="diff-meter-row"><span>적 강도</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:18%;background:#10d96e"></div></div></div>
        <div class="diff-meter-row"><span>자원량</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:90%;background:#10d96e"></div></div></div>
        <div class="diff-meter-row"><span>AI 공격성</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:10%;background:#10d96e"></div></div></div>
      </div>
    </div>
    <div class="diff-card" data-d="1">
      <div class="diff-em">🔵</div>
      <div class="diff-name" style="color:#4dabf7">중 급</div>
      <div class="diff-desc">균형 잡힌 전투<br>라인 분산 침투<br>전략이 필요</div>
      <div class="diff-tag" style="background:rgba(77,171,247,.12);color:#4dabf7;border:1px solid rgba(77,171,247,.3);">밸런스</div>
      <div class="diff-meters">
        <div class="diff-meter-row"><span>적 강도</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:48%;background:#4dabf7"></div></div></div>
        <div class="diff-meter-row"><span>자원량</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:62%;background:#4dabf7"></div></div></div>
        <div class="diff-meter-row"><span>AI 공격성</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:44%;background:#4dabf7"></div></div></div>
      </div>
    </div>
    <div class="diff-card" data-d="2">
      <div class="diff-em">🟠</div>
      <div class="diff-name" style="color:#ff8c42">어 려 움</div>
      <div class="diff-desc">약한 라인 집중<br>고급 유닛 편대<br>저격 필수</div>
      <div class="diff-tag" style="background:rgba(255,140,66,.12);color:#ff8c42;border:1px solid rgba(255,140,66,.3);">고수용</div>
      <div class="diff-meters">
        <div class="diff-meter-row"><span>적 강도</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:74%;background:#ff8c42"></div></div></div>
        <div class="diff-meter-row"><span>자원량</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:38%;background:#ff8c42"></div></div></div>
        <div class="diff-meter-row"><span>AI 공격성</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:76%;background:#ff8c42"></div></div></div>
      </div>
    </div>
    <div class="diff-card" data-d="3">
      <div class="diff-em">🔴</div>
      <div class="diff-name" style="color:#ff3355">극 악</div>
      <div class="diff-desc">즉시 전 라인 러시<br>끊임없는 물량<br>1초도 방심 금지</div>
      <div class="diff-tag" style="background:rgba(255,51,85,.12);color:#ff3355;border:1px solid rgba(255,51,85,.3);">🔥 지옥</div>
      <div class="diff-meters">
        <div class="diff-meter-row"><span>적 강도</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:100%;background:#ff3355"></div></div></div>
        <div class="diff-meter-row"><span>자원량</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:20%;background:#ff3355"></div></div></div>
        <div class="diff-meter-row"><span>AI 공격성</span><div class="diff-meter-bar"><div class="diff-meter-fill" style="width:100%;background:#ff3355"></div></div></div>
      </div>
    </div>
  </div>
  <button class="start-btn" id="start-btn">⚔️ 전투 시작</button>
  <div class="keyhint">🎯 클릭=저격 | 1~9=유닛 | Q/E/R/W/T/Y=스킬 | F/G/H=라인<br>S=상점 | Z=업그레이드창 | X=긴급수리(💎80)</div>
</div><!-- GAME -->
<div id="game">
  <div class="hud">
    <div class="hud-left">
      <span class="hud-title">⚔️ BATTLEFIELD v4</span>
      <div class="base-grp">
        <span class="base-lbl">🏰 아군</span>
        <div class="hp-bar-wrap"><div class="hp-fill ally" id="ally-hp-bar" style="width:100%"></div></div>
        <span class="hp-num" id="ally-hp-val" style="color:var(--green)">4500</span>
      </div>
      <div class="base-grp">
        <span class="base-lbl">🏯 적군</span>
        <div class="hp-bar-wrap"><div class="hp-fill enemy" id="enemy-hp-bar" style="width:100%"></div></div>
        <span class="hp-num" id="enemy-hp-val" style="color:var(--red)">4500</span>
      </div>
    </div>
    <div class="hud-right">
      <span class="badge badge-wave" id="wave-badge">웨이브 1</span>
      <span class="badge badge-res">💎 <span id="res-val">150</span></span>
      <span class="badge badge-score">🏆 <span id="score-val">0</span></span>
      <span class="badge badge-kills">💀 <span id="kills-val">0</span></span>
      <span class="badge badge-weather" id="weather-badge">☀️ 맑음</span>
      <span class="badge badge-diff" id="diff-badge"></span>
    </div>
  </div>
  <div id="wave-bar"><div id="wave-fill" style="width:0%"></div></div>

  <!-- 라인별 상태바 (HUD 바로 아래) -->
  <div id="lane-status">
    <div class="ls-lane">
      <span class="ls-name" style="color:#b26cf7">⬆탑</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-0" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-0" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-0">0v0</span>
    </div>
    <div class="ls-lane">
      <span class="ls-name" style="color:#22d3ee">➡미드</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-1" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-1" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-1">0v0</span>
    </div>
    <div class="ls-lane">
      <span class="ls-name" style="color:#10d96e">⬇봇</span>
      <div class="ls-bar-wrap">
        <div class="ls-ally-fill" id="ls-ally-2" style="width:50%;background:#10d96e;"></div>
        <div class="ls-enemy-fill" id="ls-enemy-2" style="width:50%;background:#ff4560;"></div>
      </div>
      <span class="ls-units" id="ls-units-2">0v0</span>
    </div>
    <span id="deploy-indicator" style="font-size:.62rem;font-weight:900;color:#22d3ee;margin-left:8px;">배치: 미드</span>
  </div>

  <canvas id="battlefield"></canvas>
  <div id="minimap"><canvas id="mm-canvas" width="114" height="60"></canvas><div class="minimap-label">MINIMAP</div></div>
  <div id="upgrade-panel">
    <div class="up-title">🔧 유닛 업그레이드</div>
    <div id="up-list"></div>
    <div style="font-size:.52rem;color:var(--text3);margin-top:6px;">Z키로 닫기</div>
  </div>

  <div class="bot-panel">
    <!-- 라인 선택 -->
    <div class="lane-sel">
      <div class="lane-sel-title">배치 라인</div>
      <button class="lane-btn" id="lane-btn-0" onclick="selectLane(0)">⬆️ 탑</button>
      <button class="lane-btn mid-active" id="lane-btn-1" onclick="selectLane(1)">➡️ 미드</button>
      <button class="lane-btn" id="lane-btn-2" onclick="selectLane(2)">⬇️ 봇</button>
    </div>

    <button class="unit-btn" id="btn0" onclick="spawnAlly(0)" title="근접·빠름·저렴">
      <span class="key-badge">1</span><span class="uem">🧍</span><span class="uname">보병</span><span class="ucost">💎30</span>
      <div class="ucool"><div class="ucool-fill" id="cool0" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn1" onclick="spawnAlly(1)" title="돌격·고HP·속전속결">
      <span class="key-badge">2</span><span class="uem">🪖</span><span class="uname">돌격대</span><span class="ucost">💎60</span>
      <div class="ucool"><div class="ucool-fill" id="cool1" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn2" onclick="spawnAlly(2)" title="원거리·고화력">
      <span class="key-badge">3</span><span class="uem">💪</span><span class="uname">중화기</span><span class="ucost">💎120</span>
      <div class="ucool"><div class="ucool-fill" id="cool2" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn3" onclick="spawnAlly(3)" title="힐러·아군 회복">
      <span class="key-badge">4</span><span class="uem">🏥</span><span class="uname">의무병💚</span><span class="ucost">💎80</span>
      <div class="ucool"><div class="ucool-fill" id="cool3" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn4" onclick="spawnAlly(4)" title="초장거리·고단발">
      <span class="key-badge">5</span><span class="uem">🎯</span><span class="uname">저격수</span><span class="ucost">💎100</span>
      <div class="ucool"><div class="ucool-fill" id="cool4" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn5" onclick="spawnAlly(5)" title="최고HP·탱커">
      <span class="key-badge">6</span><span class="uem">🛡️</span><span class="uname">전차🔒</span><span class="ucost">💎200</span>
      <div class="ucool"><div class="ucool-fill" id="cool5" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn6" onclick="spawnAlly(6)" title="장갑·내구력">
      <span class="key-badge">7</span><span class="uem">🤖</span><span class="uname">기갑🔩</span><span class="ucost">💎160</span>
      <div class="ucool"><div class="ucool-fill" id="cool6" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn7" onclick="spawnAlly(7)" title="화염·범위공격">
      <span class="key-badge">8</span><span class="uem">🔥</span><span class="uname">화염🔥</span><span class="ucost">💎90</span>
      <div class="ucool"><div class="ucool-fill" id="cool7" style="width:100%"></div></div>
    </button>
    <button class="unit-btn" id="btn8" onclick="spawnAlly(8)" title="극속·암살·관통">
      <span class="key-badge">9</span><span class="uem">🥷</span><span class="uname">닌자⚡</span><span class="ucost">💎75</span>
      <div class="ucool"><div class="ucool-fill" id="cool8" style="width:100%"></div></div>
    </button>

    <div class="ability-row">
      <div class="abil-btn" id="abil0" onclick="useAbility(0)"><span class="aem">💣</span><span class="aname">공습</span><span class="acool" id="acool0">Q</span><div class="abil-cd-bar" id="abar0" style="width:100%"></div></div>
      <div class="abil-btn" id="abil1" onclick="useAbility(1)"><span class="aem">⚡</span><span class="aname">전격전</span><span class="acool" id="acool1">E</span><div class="abil-cd-bar" id="abar1" style="width:100%"></div></div>
      <div class="abil-btn" id="abil2" onclick="useAbility(2)"><span class="aem">🛡️</span><span class="aname">방어막</span><span class="acool" id="acool2">R</span><div class="abil-cd-bar" id="abar2" style="width:100%"></div></div>
      <div class="abil-btn" id="abil3" onclick="useAbility(3)" style="border-color:rgba(255,50,50,.3);"><span class="aem">☢️</span><span class="aname">핵폭탄W</span><span class="acool" id="acool3">W</span><div class="abil-cd-bar" id="abar3" style="width:100%"></div></div>
      <div class="abil-btn" id="abil4" onclick="useAbility(4)" style="border-color:rgba(100,200,255,.3);"><span class="aem">⏸️</span><span class="aname">시간정지</span><span class="acool" id="acool4">T</span><div class="abil-cd-bar" id="abar4" style="width:100%"></div></div>
      <div class="abil-btn" id="abil5" onclick="useAbility(5)" style="border-color:rgba(178,108,247,.3);pointer-events:auto;"><span class="aem">🛸</span><span class="aname">드론폭격</span><span class="acool" id="acool5">Y</span><div class="abil-cd-bar" id="abar5" style="width:100%"></div></div>
      <button class="unit-btn" onclick="openShop()" style="border-color:rgba(255,215,0,.3);min-width:44px;max-width:50px;">
        <span class="uem">🛒</span><span class="uname" style="color:var(--gold)">상점</span><span class="ucost">S키</span>
      </button>
      <div class="snipe-hint">
        🔭 <b>클릭 저격</b> &nbsp;|&nbsp; F/G/H 라인<br>
        장전: <span id="reload-status" style="color:var(--green)">준비</span><br>
        콤보:<span id="combo-val" style="color:var(--gold)">×1</span> 관통:<span id="pierce-val" style="color:var(--purple)">×1</span>
      </div>
    </div>
  </div>
</div>

<!-- SCOPE -->
<div id="scope">
  <svg width="110" height="110" viewBox="0 0 110 110">
    <circle cx="55" cy="55" r="50" fill="rgba(0,0,0,0.12)" stroke="rgba(255,69,96,0.9)" stroke-width="2.5"/>
    <circle cx="55" cy="55" r="3" fill="rgba(255,69,96,1)"/>
    <line x1="55" y1="2" x2="55" y2="36" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="55" y1="74" x2="55" y2="108" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="2" y1="55" x2="36" y2="55" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <line x1="74" y1="55" x2="108" y2="55" stroke="rgba(255,69,96,0.8)" stroke-width="1.8"/>
    <circle cx="55" cy="55" r="18" fill="none" stroke="rgba(255,69,96,0.25)" stroke-width="1"/>
    <circle cx="55" cy="55" r="32" fill="none" stroke="rgba(255,69,96,0.15)" stroke-width="1"/>
  </svg>
</div>

<div id="killfeed"></div>
<div id="boss-alert" style="display:none;"></div>
<div id="shop-modal">
  <div class="shop-box">
    <div class="shop-ttl">🛒 전술 상점</div>
    <div class="shop-sub">💎 <span id="shop-res">0</span>
      <div class="shop-tabs">
        <div class="shop-tab active" onclick="shopTab(0)">⚔️ 전투</div>
        <div class="shop-tab" onclick="shopTab(1)">🛡️ 방어</div>
        <div class="shop-tab" onclick="shopTab(2)">🎯 저격</div>
        <div class="shop-tab" onclick="shopTab(3)">💡 특수</div>
      </div> — 전술 업그레이드</div>
    <div class="shop-grid" id="shop-grid"></div>
    <button class="shop-close" onclick="closeShop()">✕ 닫기</button>
  </div>
</div>
<div class="twrap" id="twrap"></div>
<div id="result">
  <div class="res-grade" id="res-grade">S</div>
  <div class="res-title" id="res-title">🏆 승리!</div>
  <div class="res-sub" id="res-subtitle"></div>
  <div class="res-grid">
    <div class="ri"><div class="ri-v" id="st-score">0</div><div class="ri-l">최종점수</div></div>
    <div class="ri"><div class="ri-v" id="st-kills">0</div><div class="ri-l">처치수</div></div>
    <div class="ri"><div class="ri-v" id="st-wave">0</div><div class="ri-l">웨이브</div></div>
    <div class="ri"><div class="ri-v" id="st-snipes">0</div><div class="ri-l">저격성공</div></div>
    <div class="ri"><div class="ri-v" id="st-hs">0</div><div class="ri-l">헤드샷</div></div>
  </div>
  <div class="res-btns">
    <button class="rbtn main" onclick="location.reload()">🔄 다시하기</button>
    <button class="rbtn menu" onclick="goMenu()">📋 메뉴</button>
  </div>
</div>

<script>
'use strict';

// ═══════════════════════════════════
//  UNIT DEFINITIONS
// ═══════════════════════════════════
const UNIT_DEFS = [
  {id:0,name:'보병',    em:'🧍',cost:30, hp:150, atk:18, spd:1.1, range:52, ranged:false,pri:1,reward:14,trainTime:28},
  {id:1,name:'돌격대',  em:'🪖',cost:60, hp:300, atk:36, spd:1.4, range:62, ranged:false,pri:2,reward:25,trainTime:48},
  {id:2,name:'중화기',  em:'💪',cost:120,hp:480, atk:68, spd:0.72,range:90, ranged:true, pri:4,reward:50,trainTime:75},
  {id:3,name:'의무병',  em:'🏥',cost:80, hp:200, atk:8,  spd:0.95,range:85, ranged:false,pri:1,reward:20,trainTime:58,healer:true},
  {id:4,name:'저격수',  em:'🎯',cost:100,hp:120, atk:110,spd:0.65,range:280,ranged:true, pri:3,reward:36,trainTime:68},
  {id:5,name:'전차',    em:'🛡️',cost:200,hp:1100,atk:82, spd:0.58,range:110,ranged:false,pri:5,reward:100,trainTime:118},
  {id:6,name:'기갑',    em:'🤖',cost:160,hp:680, atk:72, spd:0.65,range:90, ranged:false,pri:5,reward:78,trainTime:92,armored:true},
  {id:7,name:'화염',    em:'🔥',cost:90, hp:210, atk:52, spd:0.88,range:68, ranged:false,pri:3,reward:32,trainTime:54,flamer:true},
  {id:8,name:'닌자',    em:'🥷',cost:75, hp:130, atk:72, spd:2.0, range:50, ranged:false,pri:3,reward:28,trainTime:44,ninja:true},
  // ENEMY (9~18)
  {id:9, name:'적보병', em:'👹',cost:30, hp:120, atk:14, spd:1.0, range:48, ranged:false,pri:1,reward:12},
  {id:10,name:'장교',   em:'🎖️',cost:150,hp:380, atk:45, spd:0.92,range:66, ranged:false,pri:3,reward:60},
  {id:11,name:'로켓병', em:'🚀',cost:180,hp:200, atk:95, spd:0.62,range:220,ranged:true, pri:4,reward:70},
  {id:12,name:'적탱크', em:'🛡️',cost:280,hp:1000,atk:78, spd:0.48,range:98, ranged:false,pri:5,reward:120},
  {id:13,name:'드론',   em:'🛸',cost:120,hp:100, atk:38, spd:1.8, range:90, ranged:true, pri:3,reward:42},
  {id:14,name:'보스',   em:'💀',cost:999,hp:4500,atk:110,spd:0.55,range:115,ranged:false,pri:5,reward:350,isBoss:true},
  {id:15,name:'미니보스',em:'😈',cost:600,hp:1800,atk:75, spd:0.80,range:95, ranged:false,pri:5,reward:180,isMiniBoss:true},
  {id:16,name:'특공대', em:'💣',cost:200,hp:220, atk:88, spd:1.65,range:50, ranged:false,pri:4,reward:78,kamikaze:true},
  {id:17,name:'포격수', em:'🎖️',cost:220,hp:240, atk:112,spd:0.55,range:240,ranged:true, pri:5,reward:88},
  {id:18,name:'사이보그',em:'🦾',cost:240,hp:560, atk:90, spd:1.05,range:78, ranged:false,pri:5,reward:105},
];

// ═══════════════════════════════════
//  ABILITIES
// ═══════════════════════════════════
const ABILITY_DEFS = [
  {id:0,name:'공습',em:'💣',key:'q',cd:480,
   fx:()=>{
     const selL=G.selectedLane;
     for(let i=0;i<8;i++) setTimeout(()=>{
       if(!G.running)return;
       const x=ALLY_BASE_X+80+Math.random()*(W-200);
       airstrikeBomb(x,laneY(selL),selL);
     },i*140);
     toast('💣 공습! '+LANE_NAMES[selL]+' 라인!','gold');
   }},
  {id:1,name:'전격전',em:'⚡',key:'e',cd:400,
   fx:()=>{
     G.blitzEnd=G.frame+540;
     G.units.filter(u=>u.side===0).forEach(u=>{if(!u._blitzed){u.spd*=2.2;u._blitzed=true;}});
     toast('⚡ 전격전! 전 아군 강화 9초!','gold');
   }},
  {id:2,name:'방어막',em:'🛡️',key:'r',cd:450,
   fx:()=>{
     G.shieldEnd=G.frame+720;
     for(let i=0;i<3;i++) G.allyTowerHp[i]=Math.min(G.allyTowerHp[i]+200,G.maxTowerHp);
     toast('🛡️ 방어막 12초! + 타워 수리!','good');
   }},
  {id:3,name:'핵폭탄',em:'☢️',key:'w',cd:2400,
   fx:()=>{
     const selL=G.selectedLane;
     toast('☢️ ['+LANE_NAMES[selL]+'] 라인 핵폭탄! (쿨:40초)','bad');
     setTimeout(()=>{
       if(!G.running)return;
       const fl=document.getElementById('hs-flash');
       fl.style.background='rgba(255,255,200,0.92)';
       setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},500);
       // 선택한 라인의 적 유닛만 처치 (보스 제외)
       const toKill=[...G.units.filter(u=>u.side===1&&u.hp>0&&!u.isBoss&&u.laneIdx===selL)];
       toKill.forEach(u=>killUnit(u,0));
       G.units.filter(u=>u.side===1&&(u.isBoss||u.isMiniBoss)&&u.hp>0&&u.laneIdx===selL).forEach(u=>{
         const dmg=Math.round(u.maxHp*0.28);u.hp-=dmg;spawnHit(u.x,u.y,'#ffd700',dmg);
       });
       // 해당 라인 적 타워만 피해
       G.enemyTowerHp[selL]=Math.max(0,G.enemyTowerHp[selL]-250);
       for(let i=0;i<40;i++){
         const ang=Math.random()*Math.PI*2;
         const lx=ALLY_BASE_X+80+Math.random()*(W-200);
         G.particles.push({x:lx,y:laneY(selL),vx:Math.cos(ang)*5,vy:Math.sin(ang)*5-3,col:['#ffd700','#ff8c42','#ff4560'][i%3],life:42,size:6+Math.random()*8});
       }
     },700);
   }},
  {id:4,name:'시간정지',em:'⏸️',key:'t',cd:1200,
   fx:()=>{
     G.freezeEnd=G.frame+300;
     const fo=document.getElementById('freeze-overlay');
     if(fo){fo.style.background='rgba(80,160,255,0.15)';setTimeout(()=>{if(fo)fo.style.background='rgba(80,160,255,0)';},5000);}
     toast('⏸️ 전 라인 시간정지! 5초!','wave');
   }},
  {id:5,name:'드론폭격',em:'🛸',key:'y',cd:900,
   fx:()=>{
     for(let li=0;li<3;li++){
       const numBombs=5+G.diff*2;
       for(let i=0;i<numBombs;i++) setTimeout(()=>{
         if(!G.running)return;
         const x=ALLY_BASE_X+80+Math.random()*(W-200);
         airstrikeBomb(x,laneY(li),li);
       },li*200+i*120);
     }
     toast('🛸 드론폭격! 전 라인 폭격!','gold');
   }},
];

// ═══════════════════════════════════
//  DIFFICULTY
// ═══════════════════════════════════
const DIFF_CONFIG = [
  {name:'초보',  col:'#10d96e',bgCol:'rgba(16,217,110,.15)',bdCol:'rgba(16,217,110,.35)',
   resRate:3.2,botResRate:0.55,botPool:[9,9,9,10,10],    botDelay:4200,startRes:300,laneHp:2000,bossWave:14,miniBossWave:8,
   botStrategyInterval:4000,rushProb:0.05,maxTowerHp:2000,
   botStartDelay:20, // 초보: 봇이 약 20초 뒤부터 천천히 시작 (너무 길면 지루함)
   botActionless:true,
   tutorialSpawns:true}, // 초보: 소환 유도 튜토리얼
  {name:'중급',  col:'#4dabf7',bgCol:'rgba(77,171,247,.15)',bdCol:'rgba(77,171,247,.35)',
   resRate:1.9,botResRate:0.9,botPool:[9,9,10,10,11,13], botDelay:3000,startRes:190,laneHp:1700,bossWave:10,miniBossWave:5,
   botStrategyInterval:2000,rushProb:0.20,maxTowerHp:1700,
   botStartDelay:0,botActionless:false},
  {name:'어려움',col:'#ff8c42',bgCol:'rgba(255,140,66,.15)',bdCol:'rgba(255,140,66,.35)',
   resRate:1.3,botResRate:1.4,botPool:[10,11,11,12,13,16,17],botDelay:1900,startRes:145,laneHp:1500,bossWave:8,miniBossWave:4,
   botStrategyInterval:1200,rushProb:0.40,maxTowerHp:1500,
   botStartDelay:0,botActionless:false},
  {name:'극악',  col:'#ff4560',bgCol:'rgba(255,69,96,.15)', bdCol:'rgba(255,69,96,.35)',
   resRate:1.0,botResRate:2.0,botPool:[9,10,11,12,13,16,17,18,11,12],botDelay:950,startRes:125,laneHp:1300,bossWave:6,miniBossWave:3,
   botStrategyInterval:700,rushProb:0.60,maxTowerHp:1250,
   botStartDelay:0,botActionless:false},
];

// ═══════════════════════════════════
//  SHOP
// ═══════════════════════════════════
let shopTabIdx_=0;
const SHOP_TABS_=[
  [{id:'atk',em:'⚔️',name:'무기 강화', desc:'아군 공격력 +35%',cost:190,fx(){G.dmgBonus=(G.dmgBonus||1)*1.35;G.units.filter(u=>u.side===0).forEach(u=>u.atk=Math.round(u.atk*1.35));toast('무기 강화!','gold');}},
   {id:'spd',em:'💨',name:'기동력',    desc:'이동속도 +25%',   cost:165,fx(){G.spdBonus=(G.spdBonus||1)*1.25;G.units.filter(u=>u.side===0).forEach(u=>{u.spd*=1.25;u.baseSpd=(u.baseSpd||u.spd)*1.25;});toast('기동력!','good');}},
   {id:'spwn',em:'⚡',name:'연속생산', desc:'생산속도 +40%',   cost:215,fx(){G.spawnBoost=(G.spawnBoost||1)*0.72;toast('생산 가속!','good');}},
   {id:'emrg',em:'🆘',name:'긴급지원', desc:'전 라인 보병 소환',cost:90,rep:true,fx(){for(let i=0;i<3;i++){spawnUnit(0,0,i);spawnUnit(0,0,i);}toast('긴급 지원!','good');}},
   {id:'mass',em:'🔱',name:'학살모드', desc:'공격력 10초 2배', cost:320,rep:true,fx(){G.massacreEnd=G.frame+600;toast('학살 모드!','bad');}},
   {id:'dres',em:'💠',name:'자원2배',  desc:'15초 자원 2배',   cost:150,rep:true,fx(){G.doubleResEnd=G.frame+900;toast('자원 2배!','gold');}},
  ],
  [{id:'bhp',em:'❤️',name:'기지수리',  desc:'타워 HP +500',    cost:120,rep:true,fx(){for(let i=0;i<3;i++)G.allyTowerHp[i]=Math.min(G.allyTowerHp[i]+500,G.maxTowerHp);toast('기지 수리!','good');}},
   {id:'shld',em:'🛡️',name:'장갑강화', desc:'아군 HP +35%',    cost:195,fx(){G.units.filter(u=>u.side===0).forEach(u=>{u.maxHp=Math.round(u.maxHp*1.35);u.hp=Math.round(u.hp*1.35);});toast('장갑 강화!','good');}},
   {id:'tret',em:'🔰',name:'터렛강화', desc:'기지 터렛 강화',  cost:260,rep:true,fx(){G.turretLevel=(G.turretLevel||0)+1;toast('터렛 Lv'+G.turretLevel+'!','good');}},
   {id:'tatk',em:'🏰',name:'타워반격', desc:'타워 자동공격',   cost:280,fx(){G.towerAttack=true;toast('타워 반격!','good');}},
   {id:'rgn',em:'💚',name:'기지재생',  desc:'초당 5HP 회복',   cost:175,fx(){G.baseRegen=(G.baseRegen||0)+5;toast('기지 재생!','good');}},
   {id:'emp',em:'🌐',name:'EMP폭탄',   desc:'전 적 4초 마비',  cost:185,rep:true,fx(){G.freezeEnd=G.frame+240;toast('EMP 마비!','wave');}},
  ],
  [{id:'sdmg',em:'🎯',name:'저격강화', desc:'저격 피해 +70%',  cost:155,rep:true,fx(){G.snipeDmgBonus=(G.snipeDmgBonus||1)*1.7;toast('저격 강화!','gold');}},
   {id:'pier',em:'🔫',name:'관통탄',   desc:'관통 +1 (최대5)', cost:210,rep:true,fx(){G.pierceCount=Math.min((G.pierceCount||1)+1,5);document.getElementById('pierce-val').textContent='x'+G.pierceCount;toast('관통 +1!','gold');}},
   {id:'crit',em:'💥',name:'크리티컬', desc:'치명타율 +25%',   cost:185,rep:true,fx(){G.critBonus=Math.min((G.critBonus||0)+.25,.9);toast('크리 +25%!','gold');}},
   {id:'aoe',em:'💫',name:'범위저격',  desc:'반경40 범위 피해',cost:245,fx(){G.aoeSnipe=true;toast('범위 저격!','gold');}},
   {id:'msni',em:'🌀',name:'산탄저격', desc:'근처 4명 추가피해',cost:240,fx(){G.multiSnipe=true;toast('산탄!','gold');}},
   {id:'cdrd',em:'⚡',name:'스킬가속', desc:'쿨다운 -35%',     cost:135,fx(){G.cdBonus=(G.cdBonus||1)*1.5;toast('스킬 가속!','gold');}},
  ],
  [{id:'res',em:'💎',name:'자원증폭',  desc:'수급 +40%',       cost:130,rep:true,fx(){G.resBonus=(G.resBonus||1)*1.4;toast('자원 증폭!','good');}},
   {id:'xunt',em:'🌟',name:'영웅소환', desc:'전 라인 전차 소환',cost:280,rep:true,fx(){for(let i=0;i<3;i++)spawnUnit(5,0,i);toast('영웅 전차!','gold');}},
   {id:'spdup',em:'⌛',name:'적속도감', desc:'적 영구 속도 -20%',cost:350,fx(){G.units.filter(u=>u.side===1).forEach(u=>{u.spd*=.8;u.baseSpd=(u.baseSpd||u.spd)*.8;});toast('적 속도 -20%!','wave');}},
   {id:'clk',em:'👻',name:'은신저격',  desc:'다음 5회 2배피해',cost:200,rep:true,fx(){G.cloakShots=(G.cloakShots||0)+5;toast('은신 저격 5회!','gold');}},
   {id:'revv',em:'🔄',name:'아군부활', desc:'최근 사망 유닛 부활',cost:240,rep:true,fx(){if(!G.deadUnits||!G.deadUnits.length){toast('부활 없음','bad');return;}const du=G.deadUnits.pop();spawnUnit(du.defId||0,0,du.laneIdx||1);toast('부활!','good');}},
   {id:'nk2',em:'⚛️',name:'이중핵폭탄',desc:'탑+봇 동시 핵공격',cost:500,rep:true,fx(){[0,2].forEach(li=>G.units.filter(u=>u.side===1&&u.hp>0&&!u.isBoss&&u.laneIdx===li).forEach(u=>killUnit(u,0)));toast('이중 핵폭탄!','bad');}},
  ],
];
const SHOP_ITEMS=SHOP_TABS_.flat();

// ═══════════════════════════════════
//  WEATHER
// ═══════════════════════════════════
const WEATHERS = [
  {id:'clear',name:'☀️ 맑음',  spdMult:1.0,visRange:1.0, rain:false,night:false},
  {id:'rain', name:'🌧️ 폭우',  spdMult:0.82,visRange:0.85,rain:true, night:false},
  {id:'fog',  name:'🌫️ 안개',  spdMult:0.9, visRange:0.65,rain:false,night:false},
  {id:'night',name:'🌙 야간',  spdMult:1.0, visRange:0.72,rain:false,night:true},
  {id:'wind', name:'🌬️ 강풍',   spdMult:1.15,visRange:.9,  rain:false,night:false},
  {id:'storm',name:'⛈️ 폭풍',  spdMult:0.72,visRange:0.75,rain:true, night:true},
];

// ═══════════════════════════════════
//  LANE CONFIG
// ═══════════════════════════════════
const LANE_NAMES=['탑','미드','봇'];
const LANE_COLS=['#b26cf7','#22d3ee','#10d96e'];
// 라인별 Y 위치 비율 (캔버스 height 기준) — 기지 중심 Y
// 기지는 두 측면에 하나씩, 각 라인이 기지 높이의 1/3 지점에 연결됨
const LANE_Y_FRACS=[0.28, 0.55, 0.82]; // 탑, 미드, 봇

// ═══════════════════════════════════
//  GLOBALS
// ═══════════════════════════════════
let G={};
let W=0,H=0;
let ALLY_BASE_X=80, ENEMY_BASE_X=720;
let BASE_W=68, BASE_H=110; // 기지 크기
let shopBoughtItems=new Set();
let rainDrops=[];
let animFrameId=null;
let selectedLane=1; // 기본 미드

const canvas=document.getElementById('battlefield');
const ctx=canvas.getContext('2d');

function laneY(li){ return H*LANE_Y_FRACS[li]; }

// 기지의 각 라인 연결 포인트 (기지 오른쪽 or 왼쪽 엣지)
function allyGateX(){ return ALLY_BASE_X+BASE_W/2+4; }
function enemyGateX(){ return ENEMY_BASE_X-BASE_W/2-4; }
// 기지 내 각 라인의 Y포트 (기지 높이를 3등분)
function allyGateY(li){ return H*0.5 - BASE_H/2 + BASE_H*(li+0.5)/3; }
function enemyGateY(li){ return H*0.5 - BASE_H/2 + BASE_H*(li+0.5)/3; }

// ═══════════════════════════════════
//  RESIZE
// ═══════════════════════════════════
function resize(){
  const rect=canvas.getBoundingClientRect();
  // getBoundingClientRect()는 iframe 내 레이아웃이 확정되기 전에 0을 반환할 수 있음
  // → window.innerWidth/innerHeight를 폴백으로 사용
  const rw=rect.width>100?rect.width:(canvas.offsetWidth||window.innerWidth);
  // HUD 46px + wave-bar 3px + bot-panel 86px = 135px 제외
  const rh=rect.height>200?rect.height:(canvas.offsetHeight||(window.innerHeight-135));
  W=Math.max(rw,400);
  H=Math.max(rh,300);
  canvas.width=W;
  canvas.height=H;
  ALLY_BASE_X=80;
  ENEMY_BASE_X=W-80;
}

// ═══════════════════════════════════
//  LANE SELECT
// ═══════════════════════════════════
function selectLane(li){
  // 함락된 라인 선택 시 경고 + 자동 스킵
  if(G.running&&G.allyTowerHp&&G.allyTowerHp[li]<=0){
    toast('🚫 ['+LANE_NAMES[li]+'] 함락! 양쪽 소환 불가!','bad');
    // 살아있는 라인 자동 선택
    const alive=[0,1,2].find(x=>x!==li&&G.allyTowerHp[x]>0);
    if(alive!==undefined){
      selectLane(alive);
    }
    return;
  }
  selectedLane=li;
  G.selectedLane=li;
  [0,1,2].forEach(i=>{
    const btn=document.getElementById('lane-btn-'+i);
    const fallen=G.running&&G.allyTowerHp&&G.allyTowerHp[i]<=0;
    if(i===li) btn.className='lane-btn '+(i===0?'top-active':i===1?'mid-active':'bot-active');
    else if(fallen) btn.className='lane-btn fallen';
    else btn.className='lane-btn';
  });
  const ind=document.getElementById('deploy-indicator');
  if(ind){ ind.textContent='배치: '+LANE_NAMES[li]; ind.style.color=LANE_COLS[li]; }
}

// ═══════════════════════════════════
//  START
// ═══════════════════════════════════
function startGame(diff){
  const dc=DIFF_CONFIG[diff];
  shopBoughtItems=new Set();upgLevels_=[0,0,0,0,0,0];G.deadUnits=[];
  rainDrops=Array.from({length:200},()=>({x:Math.random()*2000,y:Math.random()*600,spd:8+Math.random()*6,len:12+Math.random()*10}));
  if(animFrameId) cancelAnimationFrame(animFrameId);

  G={
    running:true,diff,wave:1,
    resources:dc.startRes,
    allyBase:dc.laneHp*3, enemyBase:dc.laneHp*3, maxBase:dc.laneHp*3,
    // 라인별 타워 HP (기지 연결 타워)
    allyTowerHp:[dc.laneHp,dc.laneHp,dc.laneHp],
    enemyTowerHp:[dc.laneHp,dc.laneHp,dc.laneHp],
    maxTowerHp:dc.laneHp,
    units:[],bullets:[],effects:[],particles:[],
    score:0,kills:0,snipes:0,headshots:0,combo:1,comboTimer:0,
    nextId:0,reloading:false,reloadTimer:0,reloadMax:80,
    botTimers:[0,0,0],resTimer:0,waveTimer:0,frame:0,lastTime:performance.now(),
    abilities:[
      {id:0,cd:0,maxCd:ABILITY_DEFS[0].cd},{id:1,cd:0,maxCd:ABILITY_DEFS[1].cd},
      {id:2,cd:0,maxCd:ABILITY_DEFS[2].cd},{id:3,cd:0,maxCd:ABILITY_DEFS[3].cd},
      {id:4,cd:0,maxCd:ABILITY_DEFS[4].cd},{id:5,cd:0,maxCd:ABILITY_DEFS[5].cd},
    ],
    trainCooldowns:[0,0,0,0,0,0,0,0,0],
    blitzEnd:-1,shieldEnd:-1,freezeEnd:-1,
    massacreEnd:-1,doubleResEnd:-1,
    towerAttack:false,towerAttackTimer:0,
    spawnBoost:1,
    resBonus:1,dmgBonus:1,snipeDmgBonus:1,cdBonus:1,spdBonus:1,
    pierceCount:1,multiSnipe:false,aoeSnipe:false,critBonus:0,baseRegen:0,
    turretLevel:0,turretTimer:0,
    weather:WEATHERS[0],weatherTimer:0,
    mouseX:0,mouseY:0,
    selectedLane:1,
    // 봇 AI 전략
    botFocusLane:1, // AI가 집중 공격할 라인
    botStrategyTimer:0,
    craters:[],
  };

  selectedLane=1;
  selectLane(1);

  document.getElementById('diff-select').style.display='none';
  document.getElementById('game').style.display='flex';
  document.getElementById('result').style.display='none';
  document.getElementById('boss-alert').style.display='none';

  const dc2=DIFF_CONFIG[diff];
  const db=document.getElementById('diff-badge');
  db.textContent=dc2.name;
  db.style.cssText=`background:${dc2.bgCol};color:${dc2.col};border:1px solid ${dc2.bdCol};`;

  let attempts=0;
  function tryStart(){
    resize();
    // W<400 또는 H<300이면 레이아웃이 아직 안 잡힌 것 → 최대 25회 재시도
    if((W<400||H<300)&&attempts<25){attempts++;setTimeout(tryStart,80);return;}
    for(let i=0;i<6;i++) G.craters.push({x:150+Math.random()*(W-300),y:laneY(Math.floor(i/2)),r:14+Math.random()*18});
    updateHUD(); updateButtons();
    document.getElementById('scope').style.display='block';
    canvas.style.cursor='crosshair';
    document.getElementById('pierce-val').textContent='×'+G.pierceCount;
    G.lastTime=performance.now();
    initMinimap();
    animFrameId=requestAnimationFrame(loop);

    // 난이도별 시작 안내
    if(diff===0){
      setTimeout(()=>toast('🟢 초보 모드: 약 20초 후 적이 쳐들어옵니다!','good'),500);
      setTimeout(()=>toast('💡 [1]보병 [2]돌격대를 소환해서 준비하세요!','good'),2000);
      setTimeout(()=>toast('💡 미드(G) 라인 먼저 집중 수비 추천!','wave'),4500);
      setTimeout(()=>toast('💡 [3]의무병으로 아군을 치료할 수 있어요!','good'),7500);
      setTimeout(()=>toast('⚠️ 적 출현 임박! 라인 방어 준비!','bad'),18000);
    } else if(diff===3){
      setTimeout(()=>toast('🔴 극악: 즉시 전 라인 러시! 방심 금지!','bad'),500);
      setTimeout(()=>{if(G.running){[0,1,2].forEach(li=>{spawnUnit(9,1,li);spawnUnit(9,1,li);});}},900);
    }
  }
  setTimeout(tryStart,60);
}

function goMenu(){
  G.running=false;
  document.getElementById('result').style.display='none';
  document.getElementById('diff-select').style.display='flex';
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';
}

// ═══════════════════════════════════
//  LOOP
// ═══════════════════════════════════
function loop(ts){
  if(!G.running){animFrameId=null;return;}
  const dt=Math.min((ts-G.lastTime)/16.667,4);
  G.lastTime=ts; G.frame++;
  update(dt); render();
  animFrameId=requestAnimationFrame(loop);
}

// ═══════════════════════════════════
//  UPDATE
// ═══════════════════════════════════
function update(dt){
  const dc=DIFF_CONFIG[G.diff];

  // Weather
  G.weatherTimer+=dt;
  if(G.weatherTimer>1200){
    G.weatherTimer=0;
    const prev=G.weather.id; let next;
    do{next=WEATHERS[Math.floor(Math.random()*WEATHERS.length)];}while(next.id===prev);
    G.weather=next;
    document.getElementById('weather-badge').textContent=next.name;
    document.getElementById('night-overlay').style.background=next.night?'rgba(0,0,30,0.38)':'rgba(0,0,30,0)';
    toast('🌦️ 날씨: '+next.name,'wave');
  }

  // Resources
  G.resTimer+=dt;
  const doubleRes=(G.doubleResEnd>0&&G.frame<G.doubleResEnd)?2:1;
  const resInterval=60/(dc.resRate*(G.resBonus||1)*doubleRes);
  if(G.resTimer>=resInterval){G.resTimer=0;G.resources=Math.min(G.resources+7,900);}

  // Massacre Mode - 학살 모드
  if(G.massacreEnd>0){
    G.units.filter(u=>u.side===0&&u.hp>0&&!u._massBoosted).forEach(u=>{
      u.atk=Math.round(u.atk*2); u._massBoosted=true;
    });
    if(G.frame>=G.massacreEnd){
      G.units.filter(u=>u.side===0&&u.hp>0&&u._massBoosted).forEach(u=>{
        u.atk=Math.round(u.atk*0.5); u._massBoosted=false;
      });
      G.massacreEnd=-1; toast('학살 모드 종료','wave');
    }
  }

  // Tower Attack - 타워 반격 (아군 타워에서 적 공격)
  if(G.towerAttack){
    G.towerAttackTimer=(G.towerAttackTimer||0)+dt;
    if(G.towerAttackTimer>45){
      G.towerAttackTimer=0;
      for(let li=0;li<3;li++){
        if(G.allyTowerHp[li]<=0) continue;
        const towerX=ALLY_BASE_X+BASE_W+20;
        const tgts=G.units.filter(u=>u.side===1&&u.hp>0&&u.laneIdx===li&&u.x<towerX+180);
        if(tgts.length>0){
          const t=tgts.reduce((a,b)=>a.x<b.x?a:b);
          const dmg=Math.round(40*(G.dmgBonus||1));
          t.hp-=dmg; spawnHit(t.x,t.y,'#ffd700',dmg);
          G.particles.push({x:towerX,y:laneY(li),vx:2,vy:0,col:'#ffd700',life:12,size:3});
        }
      }
    }
  }

  // Base regen
  if(G.baseRegen>0) G.allyBase=Math.min(G.allyBase+G.baseRegen*dt/60,G.maxBase);

  // Wave
  G.waveTimer+=dt;
  if(G.waveTimer>=1800){
    G.waveTimer=0;G.wave++;
    G.maxBase+=200; G.maxTowerHp+=80;
    G.allyBase=Math.min(G.allyBase+60,G.maxBase);
    G.enemyBase=Math.min(G.enemyBase+60,G.maxBase);
    document.getElementById('wave-badge').textContent='웨이브 '+G.wave;
  const wf2=document.getElementById('wave-fill');if(wf2)wf2.style.width=((G.waveTimer/1800)*100).toFixed(1)+'%';
    if(G.wave%dc.bossWave===0) spawnBossWave();
    else if(G.wave%dc.miniBossWave===0) spawnMiniBoss();
    else if(G.wave%8===0) spawnEventWave();
    else toast('🌊 웨이브 '+G.wave+'!','wave');
  }

  // Bot AI: 라인별 독립 타이머
  const botDelayFrames=dc.botDelay/16.667;
  const botStartFrames=(dc.botStartDelay||0)*60; // 초 → 프레임
  for(let li=0;li<3;li++){
    G.botTimers[li]+=dt;
    // 초보 모드: 일정 시간 지나야 봇 소환 시작
    if(dc.botActionless && G.frame < botStartFrames) continue;
    // 집중 라인은 2배 빠르게 스폰
    const mult=(li===G.botFocusLane)?0.5:1.0;
    if(G.botTimers[li]>=botDelayFrames*mult){
      G.botTimers[li]=0;
      botSpawn(li);
    }
  }

  // 초보 튜토리얼: 30초마다 소환 힌트
  if(G.diff===0&&G.frame>0&&G.frame%1800===0){
    checkTutorialSpawn();
  }

  // Bot strategy update: 주기적으로 약한 라인으로 집중 전환
  G.botStrategyTimer+=dt;
  const stratInterval=dc.botStrategyInterval/16.667;
  if(G.botStrategyTimer>=stratInterval){
    G.botStrategyTimer=0;
    updateBotStrategy(dc);
  }

  const frozen=(G.frame<G.freezeEnd);

  // Training cooldowns
  G.trainCooldowns=G.trainCooldowns.map(c=>Math.max(0,c-dt));
  for(let i=0;i<9;i++){
    const pct=G.trainCooldowns[i]>0?1-G.trainCooldowns[i]/UNIT_DEFS[i].trainTime:1;
    const el=document.getElementById('cool'+i);
    if(el) el.style.width=(pct*100)+'%';
  }

  // Ability cooldowns
  while(G.abilities.length<6)G.abilities.push({id:G.abilities.length,cd:0,maxCd:600});
  G.abilities.forEach((a,i)=>{
    if(a.cd>0){
      a.cd=Math.max(0,a.cd-dt*(G.cdBonus||1));
      const el=document.getElementById('abil'+i);
      if(el) el.classList.toggle('cooldown',a.cd>0);
      const pct=1-a.cd/a.maxCd;
      const bar=document.getElementById('abar'+i);
      const lbl=document.getElementById('acool'+i);
      if(bar) bar.style.width=(pct*100)+'%';
      if(lbl) lbl.textContent=a.cd>0?Math.ceil(a.cd/60)+'s':['Q','E','R','W','T','Y'][i];
    }
  });

  if(G.blitzEnd>0&&G.frame===G.blitzEnd){
    G.units.filter(u=>u.side===0&&u._blitzed).forEach(u=>{u.spd/=2;u._blitzed=false;});
    toast('⚡ 전격전 종료','');
  }

  if(G.comboTimer>0){G.comboTimer-=dt;if(G.comboTimer<=0){G.combo=1;document.getElementById('combo-val').textContent='×1';}}

  if(G.reloading){
    G.reloadTimer+=dt;
    const pct=G.reloadTimer/G.reloadMax;
    const rs=document.getElementById('reload-status');
    if(rs){rs.textContent='재장전 '+Math.round(pct*100)+'%';rs.style.color='var(--orange)';}
    if(G.reloadTimer>=G.reloadMax){
      G.reloading=false;G.reloadTimer=0;
      if(rs){rs.textContent='준비';rs.style.color='var(--green)';}
    }
  }

  // Turret
  if(G.turretLevel>0){
    G.turretTimer+=dt;
    const turretRate=55/(G.turretLevel*1.6);
    if(G.turretTimer>=turretRate){
      G.turretTimer=0;
      const enemies=G.units.filter(u=>u.side===1&&u.hp>0).sort((a,b)=>a.x-b.x);
      if(enemies.length>0){
        const t=enemies[0];
        const tdmg=Math.round(35*G.turretLevel*(G.dmgBonus||1));
        G.bullets.push({x:ALLY_BASE_X+BASE_W/2,y:H*0.5,tx:t.x,ty:t.y-18,col:'#b26cf7',dmg:tdmg,targetId:t.uid,fromSide:0,spd:13,pierce:0,maxPierce:0});
      }
    }
  }

  updateUnits(dt,frozen);
  updateBullets(dt);
  updateEffects(dt);
  updateParticles(dt);

  // ★ 라인 함락 경고 시스템 ★
  for(let li=0;li<3;li++){
    if(!G._laneWasFallen) G._laneWasFallen=[false,false,false];
    const nowFallen=G.allyTowerHp[li]<=0;

    if(nowFallen&&!G._laneWasFallen[li]){
      G._laneWasFallen[li]=true;
      toast('💥 ['+LANE_NAMES[li]+'] 라인 함락! 양쪽 소환 불가!','bad');
      const ba=document.getElementById('boss-alert');
      ba.style.display='flex';
      ba.innerHTML='<div class="boss-alert-box" style="color:#ff4560;font-size:2rem;">⚠️ ['+LANE_NAMES[li]+'] 함락!<br><span style="font-size:1.2rem;">봇들이 왔던 길로 복귀합니다</span></div>';
      setTimeout(()=>{ba.style.display='none';},2500);

      // 함락 시 해당 라인의 아군 유닛들을 다른 라인으로 이동 명령
      const aliveUnits=G.units.filter(u=>u.side===0&&u.hp>0&&u.laneIdx===li);
      const nextLane=[0,1,2].find(x=>x!==li&&G.allyTowerHp[x]>0&&G.enemyTowerHp[x]>0);
      if(nextLane!==undefined&&aliveUnits.length>0){
        aliveUnits.forEach(u=>{
          u._roaming=true;
          u.laneIdx=nextLane;
          u.reachedLane=false;
          u.atBaseGate=false;
        });
        toast('↩️ ['+LANE_NAMES[li]+'→'+LANE_NAMES[nextLane]+'] 자동 지원 이동!','good');
      }
    }
    if(!nowFallen&&G._laneWasFallen[li]) G._laneWasFallen[li]=false;

    // 적 타워 클리어 축하
    if(!G._enemyFallen) G._enemyFallen=[false,false,false];
    if(G.enemyTowerHp[li]<=0&&!G._enemyFallen[li]){
      G._enemyFallen[li]=true;
      toast('🎉 ['+LANE_NAMES[li]+'] 라인 돌파! 지원군이 다른 라인으로!','good');
    }
  }

  // 게임 오버: 기지 전체 HP 기준
  const totalAlly=G.allyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalEnemy=G.enemyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  G.allyBase=totalAlly; G.enemyBase=totalEnemy;
  if(G.enemyBase<=0) endGame(true);
  else if(G.allyBase<=0) endGame(false);

  updateHUD();
  updateButtons();
  updateLaneStatus();
}

// ═══════════════════════════════════
//  BOT STRATEGY
// ═══════════════════════════════════
function updateBotStrategy(dc){
  // 아군 타워 HP가 낮은 라인 우선 + 랜덤 러시
  if(Math.random()<dc.rushProb){
    // 랜덤 라인 러시
    G.botFocusLane=Math.floor(Math.random()*3);
    if(G.diff>=1) toast('⚠️ 적 '+LANE_NAMES[G.botFocusLane]+' 라인 집중 공격!','bad');
  } else {
    // 아군 타워 가장 약한 라인
    let minHp=Infinity,focusLi=1;
    G.allyTowerHp.forEach((hp,li)=>{if(hp<minHp){minHp=hp;focusLi=li;}});
    G.botFocusLane=focusLi;
  }
}

// ═══════════════════════════════════
//  UNIT SPAWN
// ═══════════════════════════════════
function spawnUnit(defId,side,laneIdx){
  const def=UNIT_DEFS[defId];
  const ws=1+(G.wave-1)*0.11;
  const isBoss=def.isBoss||false;
  const isMiniBoss=def.isMiniBoss||false;
  const hpMult=isBoss?(1+G.diff*0.3):(isMiniBoss?(1+G.diff*0.22):1);
  const startX=side===0?ALLY_BASE_X+BASE_W/2+10:ENEMY_BASE_X-BASE_W/2-10;
  // 유닛은 라인 Y에서 시작
  const gy=allyGateY(laneIdx);
  const u={defId:defId,
    uid:G.nextId++,defId,side,laneIdx,
    x:startX, y:gy,
    targetY:laneY(laneIdx), // 라인 Y로 이동
    reachedLane:false, // 라인 Y에 도달했는지
    hp:Math.round(def.hp*ws*hpMult),
    maxHp:Math.round(def.hp*ws*hpMult),
    atk:Math.round(def.atk*ws*(side===0?(G.dmgBonus||1):1)),
    spd:def.spd*(side===0?(G.spdBonus||1):1)*G.weather.spdMult,
    baseSpd:def.spd*(side===0?(G.spdBonus||1):1),
    range:def.range*G.weather.visRange,
    ranged:def.ranged,cooldown:0,em:def.em,pri:def.pri,
    healer:def.healer||false,armored:def.armored||false,
    flamer:def.flamer||false,ninja:def.ninja||false,kamikaze:def.kamikaze||false,
    reward:def.reward,name:def.name,
    anim:Math.random()*Math.PI*2,isBoss,isMiniBoss,
    atBaseGate:false, // 상대 기지 앞에 도달
  };
  G.units.push(u);
}

function spawnAlly(defId){
  if(defId>8) return;
  const def=UNIT_DEFS[defId];
  if(G.resources<def.cost){toast('💎 자원 부족!','bad');return;}
  if(G.trainCooldowns[defId]>0){toast('⏳ 훈련 중!','bad');return;}
  // ★ 부서진 라인 소환 금지 (양쪽 컨트롤 불가) ★
  if(G.allyTowerHp[G.selectedLane]<=0){
    toast('🚫 ['+LANE_NAMES[G.selectedLane]+'] 함락된 라인 - 양쪽 소환 불가!','bad');
    // 살아있는 다른 라인 자동 선택
    const alive=[0,1,2].find(x=>G.allyTowerHp[x]>0);
    if(alive!==undefined) selectLane(alive);
    return;
  }
  // 추가: 아군 타워가 없어도 적 타워도 없으면 (양쪽 다 부서짐) 소환 불가
  if(G.enemyTowerHp[G.selectedLane]<=0&&G.allyTowerHp[G.selectedLane]<=0){
    toast('🚫 ['+LANE_NAMES[G.selectedLane]+'] 완전히 교전 불가!','bad');
    return;
  }
  G.resources-=def.cost;
  G.trainCooldowns[defId]=Math.round(def.trainTime*(G.spawnBoost||1));
  spawnUnit(defId,0,G.selectedLane);
  updateButtons();
}

function botSpawn(laneIdx){
  const dc=DIFF_CONFIG[G.diff];
  const pool=dc.botPool.filter(id=>id!==14&&id!==15);
  // 웨이브가 높을수록 강한 유닛 선호
  const waveBonus=Math.min(G.wave*28, 180);
  const botRes=Math.max(120, 60+G.wave*35*dc.botResRate + waveBonus);
  const affor=pool.map(id=>UNIT_DEFS[id]).filter(d=>d&&d.cost<=botRes);
  if(!affor.length){
    const ch=pool.map(id=>UNIT_DEFS[id]).filter(d=>d).sort((a,b)=>a.cost-b.cost)[0];
    if(ch)spawnUnit(ch.id,1,laneIdx);
    return;
  }

  let chosen;
  if(G.diff===0){
    // 초보: 초반은 약한 유닛, 웨이브 늘수록 가끔 강한 유닛 섞음
    const sortedAsc=affor.slice().sort((a,b)=>a.cost-b.cost);
    if(G.wave<=3) chosen=sortedAsc[0]; // 초반 보병만
    else if(G.wave<=6) chosen=sortedAsc[Math.floor(Math.random()*Math.min(2,sortedAsc.length))];
    else chosen=sortedAsc[Math.floor(Math.random()*sortedAsc.length)]; // 후반 랜덤
  } else if(G.diff>=2){
    // 어려움/극악: 강한 유닛 우선 (상위 2개 중 랜덤)
    affor.sort((a,b)=>b.cost-a.cost);
    chosen=affor[Math.floor(Math.random()*Math.min(2,affor.length))];
  } else {
    // 중급: 완전 랜덤이지만 가끔 강한 유닛
    if(Math.random()<0.35){
      affor.sort((a,b)=>b.cost-a.cost);
      chosen=affor[0];
    } else {
      chosen=affor[Math.floor(Math.random()*affor.length)];
    }
  }

  // ★ 라인 완전 함락 처리 ★
  const allyHp=G.allyTowerHp[laneIdx];
  if(allyHp<=0){
    const activeLanes=[0,1,2].filter(li=>G.allyTowerHp[li]>0&&G.enemyTowerHp[li]>0);
    if(activeLanes.length===0){
      const anyAlive=[0,1,2].filter(li=>G.allyTowerHp[li]>0);
      if(anyAlive.length>0) laneIdx=anyAlive[Math.floor(Math.random()*anyAlive.length)];
    } else {
      laneIdx=activeLanes[Math.floor(Math.random()*activeLanes.length)];
    }
  }

  spawnUnit(chosen.id,1,laneIdx);

  // 어려움: 집중 라인에 가끔 동반 소환
  if(G.diff===2&&li===G.botFocusLane&&Math.random()<0.30){
    setTimeout(()=>{if(G.running)spawnUnit(affor[Math.floor(Math.random()*affor.length)].id,1,laneIdx);},500);
  }
  // 극악: 집중 라인 추가 스폰
  if(G.diff===3&&Math.random()<0.45){
    setTimeout(()=>{if(G.running)spawnUnit(chosen.id,1,laneIdx);},380);
  }
}

function spawnBossWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="boss-alert-box">💀 보스 + 전 라인 공략!</div>';
  setTimeout(()=>{ba.style.display='none';},2200);
  const bossLane=Math.floor(Math.random()*3);
  spawnUnit(14,1,bossLane);
  for(let li=0;li<3;li++) setTimeout(()=>{if(G.running)spawnUnit(10,1,li);},li*350);
  toast('💀 보스 웨이브! 전 라인 위기!','bad');
}

function spawnMiniBoss(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  ba.innerHTML='<div class="miniboss-alert-box">😈 미니보스 출현!</div>';
  setTimeout(()=>{ba.style.display='none';},2000);
  const ml=G.botFocusLane;
  spawnUnit(15,1,ml);
  for(let i=0;i<2;i++) setTimeout(()=>{if(G.running)spawnUnit(9,1,(ml+i)%3);},i*300);
  toast('😈 미니보스! '+LANE_NAMES[ml]+' 라인!','bad');
}

function spawnEventWave(){
  const ba=document.getElementById('boss-alert');
  ba.style.display='flex';
  // 랜덤 이벤트 타입
  const evType=Math.floor(Math.random()*3);
  if(evType===0){
    ba.innerHTML='<div class="event-alert-box">🎖️ 전 라인 지원대!</div>';
    setTimeout(()=>{ba.style.display='none';},2000);
    for(let li=0;li<3;li++){
      setTimeout(()=>{if(G.running){spawnUnit(0,0,li);spawnUnit(5,0,li);}},li*250);
    }
    G.resources=Math.min(G.resources+120,900);
    toast('🎖️ 전 라인 지원 + 💎120!','good');
  } else if(evType===1){
    ba.innerHTML='<div class="event-alert-box">⚡ 전격 증원!</div>';
    setTimeout(()=>{ba.style.display='none';},2000);
    for(let li=0;li<3;li++){
      setTimeout(()=>{if(G.running){spawnUnit(1,0,li);spawnUnit(8,0,li);}},li*180);
    }
    // 돌격대+닌자 전격 부스트
    G.units.filter(u=>u.side===0).forEach(u=>{if(!u._blitzed){u.spd*=1.5;u._blitzed=true;}});
    G.blitzEnd=G.frame+360;
    toast('⚡ 전격 증원! 전 아군 가속!','gold');
  } else {
    ba.innerHTML='<div class="event-alert-box">💰 보급 지원!</div>';
    setTimeout(()=>{ba.style.display='none';},2000);
    const bonus=150+G.wave*10;
    G.resources=Math.min(G.resources+bonus,900);
    // 전 아군 소량 힐
    G.units.filter(u=>u.side===0&&u.hp>0).forEach(u=>{u.hp=Math.min(u.maxHp,u.hp+u.maxHp*0.25);});
    toast('💰 보급! 💎'+bonus+' + 전 아군 25% 회복!','gold');
  }
}

// 초보 모드 자동 소환 힌트 (처음 5웨이브 동안 유닛이 없으면 소환 유도)
function checkTutorialSpawn(){
  if(G.diff!==0||G.wave>5) return;
  const allyCount=G.units.filter(u=>u.side===0&&u.hp>0).length;
  if(allyCount===0&&G.resources>=30){
    toast('💡 유닛이 없어요! [1]보병 소환하세요!','wave');
    // 자원 충분하면 자동으로 보병 한 명 소환 (튜토리얼)
    if(G.resources>=60&&G.wave<=2){
      setTimeout(()=>{if(G.running&&G.units.filter(u=>u.side===0).length===0){spawnUnit(0,0,1);toast('🤖 자동소환: 보병 미드 배치!','good');}},1500);
    }
  }
}

// ═══════════════════════════════════
//  UPDATE UNITS
// ═══════════════════════════════════
function updateUnits(dt,frozen){
  G.units.forEach(u=>{
    u.anim+=dt*0.12;
    if(u.hp<=0) return;
    if(frozen&&u.side===1) return;

    u.spd=u.baseSpd*G.weather.spdMult*(u.side===0?(G.spdBonus||1):1);
    if(u._blitzed) u.spd=u.baseSpd*2;

    // 1단계: 기지에서 나와서 라인 Y로 이동 (대각선)
    if(!u.reachedLane){
      const targetY=laneY(u.laneIdx);
      const dy=targetY-u.y;
      const dir=u.side===0?1:-1;
      // X도 조금씩 이동, Y를 더 빠르게
      u.x+=dir*u.spd*0.5*dt;
      if(Math.abs(dy)>2){
        u.y+=Math.sign(dy)*u.spd*1.2*dt;
      } else {
        u.y=targetY;
        u.reachedLane=true;
      }
      return;
    }

    // 2단계: 라인을 따라 이동 (X축 이동)
    // 치유사: 같은 라인 아군 회복 + 전체 가장 낮은 HP 아군도 치료
    if(u.healer){
      const healRange=130;
      const hurt=G.units.filter(o=>o.side===u.side&&o.hp>0&&o.hp<o.maxHp&&Math.abs(u.x-o.x)<healRange);
      if(hurt.length>0){
        hurt.sort((a,b)=>(a.hp/a.maxHp)-(b.hp/b.maxHp)); // 가장 낮은 hp%부터
        const target=hurt[0];
        const healAmt=1.4*dt;
        target.hp=Math.min(target.maxHp,target.hp+healAmt);
        // 힐 이펙트
        if(Math.random()<0.08) G.particles.push({x:target.x,y:target.y-18,vx:(Math.random()-.5),vy:-1.2,col:'#10d96e',life:18,size:3});
        // 의무병은 적 공격 안하고 힐에 집중
        return;
      }
    }

    if(u.kamikaze&&u.side===1){
      u.x-=u.spd*dt*1.6;
      if(u.x<=allyGateX()+10){
        const shield=G.frame<G.shieldEnd?0.3:1;
        G.allyTowerHp[u.laneIdx]=Math.max(0,G.allyTowerHp[u.laneIdx]-u.atk*3*shield);
        spawnDeath(u.x,u.y,false);u.hp=0;return;
      }
    }

    // 같은 라인의 적 찾기 (앞에 있는 적 우선)
    const dir2=u.side===0?1:-1;
    const enemies=G.units.filter(o=>{
      if(o.side===u.side||o.hp<=0||o.laneIdx!==u.laneIdx||!o.reachedLane) return false;
      // ★ 지나치는 버그 수정: 상대방이 내 앞에 있는지 확인 ★
      // 아군(side=0)은 오른쪽(x큰)으로 이동 → 적은 현재위치 오른쪽에서 왼쪽으로 오는 적
      // 적(side=1)은 왼쪽(x작)으로 이동 → 아군은 현재위치 왼쪽에서 오른쪽으로 오는 유닛
      // 모든 교전 범위 내 적 + 내 진행 방향 앞에 있는 적 포함
      const inFront= u.side===0 ? o.x > u.x - u.range*0.3 : o.x < u.x + u.range*0.3;
      return inFront || Math.abs(u.x-o.x) < u.range;
    });
    let target=null,minD=Infinity;
    enemies.forEach(e=>{const d=Math.abs(u.x-e.x);if(d<minD){minD=d;target=e;}});

    // 상대 기지 게이트까지 도달했는지 확인
    const gateX=u.side===0?enemyGateX():allyGateX();
    const distToGate=u.side===0?gateX-u.x:u.x-gateX;

    // ★ 적이 지나쳐서 내 뒤에 있는 경우 → 돌아서 교전 ★
    // 뒤에 있는 적이 범위 안에 들어오면 교전 (지나침 방지)
    const behindEnemy=G.units.find(o=>{
      if(o.side===u.side||o.hp<=0||o.laneIdx!==u.laneIdx||!o.reachedLane) return false;
      const dist=Math.abs(u.x-o.x);
      const isBehind=u.side===0 ? o.x < u.x - 8 : o.x > u.x + 8;
      return isBehind && dist < u.range * 1.0; // 뒤에 있어도 범위 넓게
    });
    const effectiveTarget = target || behindEnemy;
    const effectiveDist = effectiveTarget ? Math.abs(u.x-effectiveTarget.x) : Infinity;

    if(effectiveTarget&&effectiveDist<=u.range){
      // 적과 교전
      u.cooldown-=dt;
      if(u.cooldown<=0){
        u.cooldown=26-G.diff*2;
        if(u.flamer){
          // 화염: 범위 내 모든 적 피해 + 도트 효과
          const inRange=G.units.filter(o=>o.side!==u.side&&o.hp>0&&o.laneIdx===u.laneIdx&&Math.abs(u.x-o.x)<u.range);
          inRange.forEach(e=>{
            const fd=u.atk*0.62; e.hp-=fd;
            // 화염 도트 (불꽃 파티클)
            if(Math.random()<0.4) G.particles.push({x:e.x+(Math.random()-.5)*16,y:e.y-10,vx:(Math.random()-.5)*1.5,vy:-1.5-Math.random(),col:'#ff8c42',life:14,size:3+Math.random()*3});
            spawnHit(e.x,e.y,'#ff8c42',Math.round(fd));
            if(e.hp<=0)killUnit(e,u.side===0?0:1);
          });
        } else if(u.ninja&&u.side===0){
          // 닌자: 암살 (적 HP 15% 미만이면 즉사 확률 20%)
          const ninjaTarget=effectiveTarget;
          if(ninjaTarget&&ninjaTarget.hp/ninjaTarget.maxHp<0.15&&Math.random()<0.20){
            killUnit(ninjaTarget,0);
            toast('🥷 닌자 암살!','gold');
          } else {
            ninjaTarget.hp-=u.atk;
            spawnHit(ninjaTarget.x,ninjaTarget.y,'#b26cf7',u.atk);
            if(ninjaTarget.hp<=0)killUnit(ninjaTarget,u.side===0?0:1);
          }
        } else if(u.ranged){
          G.bullets.push({x:u.x,y:u.y-18,tx:effectiveTarget.x,ty:effectiveTarget.y-18,col:u.side===0?'#22d3ee':'#ff4560',dmg:u.atk,targetId:effectiveTarget.uid,fromSide:u.side,spd:8,pierce:0,maxPierce:0});
        } else {
          effectiveTarget.hp-=u.atk;
          spawnHit(effectiveTarget.x,effectiveTarget.y,u.side===0?'#22d3ee':'#ff4560',u.atk);
          if(effectiveTarget.hp<=0)killUnit(effectiveTarget,u.side===0?0:1);
        }
      }
    } else if(distToGate<=u.range*0.5){
      // 기지 앞: 기지 공격 (멈추고 기지 깎기)
      u.atBaseGate=true;
      u.cooldown-=dt;
      if(u.cooldown<=0){
        u.cooldown=30-G.diff*2;
        const shield=G.frame<G.shieldEnd?0.3:1;
        if(u.side===0){
          // 아군이 적 타워 공격
          G.enemyTowerHp[u.laneIdx]=Math.max(0,G.enemyTowerHp[u.laneIdx]-u.atk*0.55);
          spawnHit(gateX,laneY(u.laneIdx),'#22d3ee',Math.round(u.atk*0.55));

          // ★★ 라인 클리어 시 복귀 & 지원 AI ★★
          // 적 타워가 완전히 부서졌고, 이 라인에 적이 없으면 → 위기 라인으로 이동
          if(G.enemyTowerHp[u.laneIdx]<=0 && !u._roaming){
            const enemiesOnLane=G.units.filter(o=>o.side===1&&o.hp>0&&o.laneIdx===u.laneIdx).length;
            if(enemiesOnLane===0){
              let worstLane=-1, worstScore=-Infinity;
              for(let wi=0;wi<3;wi++){
                if(wi===u.laneIdx) continue;
                const lHp=G.allyTowerHp[wi];
                const lEnemies=G.units.filter(o=>o.side===1&&o.hp>0&&o.laneIdx===wi).length;
                // 점수: 적이 많고 HP 낮을수록 높음
                const urgency=lEnemies*120-(lHp/G.maxTowerHp*100);
                if(urgency>worstScore){worstScore=urgency;worstLane=wi;}
              }
              if(worstLane===-1){
                for(let wi=0;wi<3;wi++){
                  if(wi===u.laneIdx) continue;
                  if(G.enemyTowerHp[wi]>0){worstLane=wi;break;}
                }
              }
              if(worstLane!==-1){
                u._roaming=true;
                u._roamTarget=worstLane;
                const oldLane=u.laneIdx;
                u.laneIdx=worstLane;
                u.reachedLane=false;
                u.atBaseGate=false;
                if(G.frame%120===0) toast('🔀 ['+LANE_NAMES[oldLane]+'→'+LANE_NAMES[worstLane]+'] 지원!','good');
              }
            }
          }
        } else {
          // ★ 적이 아군 타워 공격 — 타워 파괴 후 지원 AI ★
          G.allyTowerHp[u.laneIdx]=Math.max(0,G.allyTowerHp[u.laneIdx]-u.atk*0.55*shield);
          spawnHit(gateX,laneY(u.laneIdx),'#ff4560',Math.round(u.atk*0.55));
          // 아군 타워 파괴 후 → 다른 라인 지원 (적 봇도 지원)
          if(G.allyTowerHp[u.laneIdx]<=0 && !u._roaming){
            const allyOnLane=G.units.filter(o=>o.side===0&&o.hp>0&&o.laneIdx===u.laneIdx).length;
            if(allyOnLane===0){
              let nextLane=-1, nextScore=-Infinity;
              for(let wi=0;wi<3;wi++){
                if(wi===u.laneIdx) continue;
                const allyHp=G.allyTowerHp[wi];
                const allyUnits=G.units.filter(o=>o.side===0&&o.hp>0&&o.laneIdx===wi).length;
                const urgency=allyUnits*100-(allyHp/G.maxTowerHp*100);
                if(urgency>nextScore){nextScore=urgency;nextLane=wi;}
              }
              if(nextLane!==-1){
                u._roaming=true;
                u.laneIdx=nextLane;
                u.reachedLane=false;
                u.atBaseGate=false;
              }
            }
          }
        }
      }
    } else {
      // 전진
      u.atBaseGate=false;

      // ★ 로밍 유닛: 기지 방향으로 복귀 후 새 라인으로 이동 ★
      if(u._roaming && u.reachedLane){
        const homeX=u.side===0 ? ALLY_BASE_X+BASE_W/2+10 : ENEMY_BASE_X-BASE_W/2-10;
        const distHome=Math.abs(u.x-homeX);
        if(distHome>30){
          u.x+=(u.side===0?-1:1)*u.spd*dt*1.3;
          u.y=laneY(u.laneIdx);
          return;
        } else {
          u._roaming=false;
          u.reachedLane=false;
          u.x=homeX;
        }
      }

      const dir=u.side===0?1:-1;
      // ★ 막힘 감지: 앞에 있는 적 OR 아군에게 막힘 ★
      // 앞에 아군이 있으면 그 뒤에서 대기 (스택 방지)
      const allyInFront=G.units.some(o=>{
        if(o.uid===u.uid||o.side!==u.side||o.hp<=0||o.laneIdx!==u.laneIdx||!o.reachedLane) return false;
        const gap=u.side===0?(o.x-u.x):(u.x-o.x);
        return gap>0&&gap<22;
      });
      const blocked=G.units.some(o=>{
        if(o.side===u.side||o.hp<=0||o.laneIdx!==u.laneIdx||!o.reachedLane) return false;
        const inFront=u.side===0?(o.x>u.x-5&&o.x<u.x+55):(o.x<u.x+5&&o.x>u.x-55);
        return inFront&&Math.abs(u.x-o.x)<(u.ninja?22:32);
      });
      const finalBlocked=blocked||allyInFront;
      if(!finalBlocked) u.x+=dir*u.spd*dt;
      else if(u.ninja) u.x+=dir*u.spd*dt*2.2; // 닌자는 아군 관통
    }
    // Y 스냅 (라인 유지)
    u.y=laneY(u.laneIdx);
  });
  G.units=G.units.filter(u=>u.hp>0);
}

function killUnit(unit,killerSide){
  if(!G.deadUnits) G.deadUnits=[];
  G.deadUnits.push({defId:unit.defId,laneIdx:unit.laneIdx,side:unit.side,name:unit.name});
  if(unit.hp<=0) return;
  G.score+=unit.reward*G.wave*(killerSide===0?G.combo:1);
  if(killerSide===0){G.kills++;addKillFeed(unit);}
  G.resources=Math.min(G.resources+Math.floor(unit.reward*0.38),900);
  spawnDeath(unit.x,unit.y,unit.isBoss||unit.isMiniBoss);
  if(unit.isBoss){toast('💀 보스 처치!','gold');spawnFireworks();}
  else if(unit.isMiniBoss){toast('😈 미니보스 처치!','gold');}
  unit.hp=0;
}

function updateBullets(dt){
  G.bullets.forEach(b=>{
    const dx=b.tx-b.x,dy=b.ty-b.y,d=Math.sqrt(dx*dx+dy*dy);
    if(d<b.spd*dt*2){
      const t=G.units.find(u=>u.uid===b.targetId&&u.hp>0);
      if(t){
        t.hp-=b.dmg;spawnHit(t.x,t.y,b.col,b.dmg);
        if(t.hp<=0)killUnit(t,b.fromSide===0?0:1);
        if(b.pierce<b.maxPierce){
          b.pierce++;
          const ne=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==b.targetId).sort((a,c)=>Math.abs(a.x-(t.x+30))-Math.abs(c.x-(t.x+30)));
          if(ne.length>0){const nt=ne[0];b.tx=nt.x;b.ty=nt.y-18;b.targetId=nt.uid;b.x=t.x;b.y=t.y-18;return;}
        }
      }
      b.done=true;
    } else {b.x+=dx/d*b.spd*dt;b.y+=dy/d*b.spd*dt;}
  });
  G.bullets=G.bullets.filter(b=>!b.done);
}

function updateEffects(dt){
  G.effects.forEach(e=>{e.r+=dt*1.8;e.alpha-=dt*0.045;if(e.alpha<=0)e.done=true;});
  G.effects=G.effects.filter(e=>!e.done);
}
function updateParticles(dt){
  G.particles.forEach(p=>{p.x+=p.vx*dt;p.y+=p.vy*dt;p.vy+=0.15*dt;p.life-=dt;});
  G.particles=G.particles.filter(p=>p.life>0);
}

function spawnHit(x,y,col,dmg){
  G.effects.push({x,y,r:3,col,alpha:0.9,type:'hit'});
  if(dmg>0) for(let i=0;i<3;i++) G.particles.push({x,y:y-15,vx:(Math.random()-.5)*2,vy:-Math.random()*2,col,life:15,size:2+Math.random()*2});
}
function spawnDeath(x,y,big){
  const cnt=big?24:9;
  for(let i=0;i<cnt;i++){
    const ang=Math.random()*Math.PI*2,spd=1+Math.random()*3;
    G.particles.push({x,y,vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd-2,col:big?'#ffd700':'#ff4560',life:22+Math.random()*20,size:big?6:3});
    G.effects.push({x:x+(Math.random()-.5)*30,y:y+(Math.random()-.5)*30,r:2,col:big?'#ffd700':'#ff4560',alpha:0.8,type:'death'});
  }
}
function airstrikeBomb(x,y,laneIdx){
  G.effects.push({x,y,r:5,col:'#ff8c42',alpha:1,type:'bomb'});
  G.units.filter(u=>u.side===1&&u.laneIdx===laneIdx&&Math.abs(u.x-x)<65).forEach(u=>{
    const dmg=Math.round((110+G.wave*22)*(G.snipeDmgBonus||1));
    u.hp-=dmg;spawnHit(u.x,u.y,'#ff8c42',dmg);if(u.hp<=0)killUnit(u,0);
  });
  G.enemyTowerHp[laneIdx]=Math.max(0,G.enemyTowerHp[laneIdx]-35);
  for(let i=0;i<10;i++) G.particles.push({x:x+(Math.random()-.5)*45,y,vx:(Math.random()-.5)*4,vy:-Math.random()*5,col:'#ff8c42',life:28+Math.random()*15,size:4});
}

// ═══════════════════════════════════
//  SNIPER
// ═══════════════════════════════════
function tryShoot(mx,my){
  if(!G.running) return;
  if(G.reloading){toast('🔫 재장전 중!','bad');return;}

  const HITBOX=44, HEADBOX=19;
  let hit=null,bestPri=-1,isHeadshot=false;
  G.units.forEach(u=>{
    if(u.side!==1||u.hp<=0||!u.reachedLane) return;
    const uy=u.y-18, headY=u.y-31;
    const bd=Math.sqrt((mx-u.x)**2+(my-uy)**2);
    const hd=Math.sqrt((mx-u.x)**2+(my-headY)**2);
    if(bd<HITBOX&&u.pri>=bestPri){bestPri=u.pri;hit=u;isHeadshot=(hd<HEADBOX);}
  });

  const isCrit=Math.random()<(G.critBonus||0);
  const baseDmg=(140+G.diff*40)*(G.snipeDmgBonus||1)*(G.weather.id==='night'?0.82:1);

  if(hit){
    let dmg=Math.round(baseDmg*(hit.isBoss?0.48:1)*G.combo);
    let dmgLabel='';
    if(isHeadshot){dmg=Math.round(dmg*1.65);dmgLabel+=' 🎯헤드샷!';}
    if(isCrit){dmg=Math.round(dmg*1.45);dmgLabel+=' 💥크리티컬!';}

    const pierceMax=G.pierceCount-1;
    G.bullets.push({x:mx,y:my,tx:hit.x,ty:hit.y-18,col:isHeadshot?'#ffd700':'#ff4560',dmg,targetId:hit.uid,fromSide:0,spd:30,pierce:0,maxPierce:pierceMax});

    if(G.multiSnipe){
      const nearby=G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==hit.uid&&u.laneIdx===hit.laneIdx&&Math.abs(u.x-hit.x)<80);
      nearby.slice(0,3).forEach(u=>{const sd=Math.round(dmg*0.42);setTimeout(()=>{if(u.hp>0){u.hp-=sd;spawnHit(u.x,u.y,'#ff8c42',sd);if(u.hp<=0)killUnit(u,0);}},80);});
    }
    if(G.aoeSnipe){
      G.units.filter(u=>u.side===1&&u.hp>0&&u.uid!==hit.uid&&Math.sqrt((u.x-hit.x)**2+(u.y-hit.y)**2)<38).forEach(u=>{
        const ad=Math.round(dmg*0.35);setTimeout(()=>{if(u.hp>0){u.hp-=ad;spawnHit(u.x,u.y,'#b26cf7',ad);if(u.hp<=0)killUnit(u,0);}},60);
      });
    }

    G.snipes++;
    G.score+=Math.round(95*G.wave*G.combo*(isHeadshot?2:1));
    G.combo=Math.min(G.combo+1,15);G.comboTimer=190;
    const cv=document.getElementById('combo-val');
    if(cv){cv.textContent='×'+G.combo;cv.classList.remove('combo-flash');void cv.offsetWidth;cv.classList.add('combo-flash');}

    if(isHeadshot){
      G.headshots++;
      const fl=document.getElementById('hs-flash');fl.style.background='rgba(255,215,0,0.13)';
      setTimeout(()=>{fl.style.background='rgba(255,215,0,0)';},150);
      const w=document.getElementById('twrap');
      const d=document.createElement('div');d.className='hs-toast';
      d.textContent='🎯 헤드샷! ×1.65 피해'+dmgLabel;
      w.insertBefore(d,w.firstChild);setTimeout(()=>d.remove(),2200);
    } else {
      toast('🎯 ['+LANE_NAMES[hit.laneIdx]+'] '+hit.name+' -'+dmg+'HP ×'+G.combo+dmgLabel,'gold');
    }

    G.effects.push({x:hit.x,y:hit.y,r:6,col:isHeadshot?'#ffd700':'#ff4560',alpha:0.9,type:'snipe'});
    G.reloading=true;G.reloadTimer=0;
    G.reloadMax=Math.max(32,80-G.combo*4);

  } else {
    // 적 기지 직격 체크 (각 라인 게이트 근처)
    let hitGate=false;
    for(let li=0;li<3;li++){
      const gx=enemyGateX(), gy=allyGateY(li);
      if(mx>ENEMY_BASE_X-BASE_W/2-20&&Math.abs(my-gy)<30){
        const dmg=Math.round((45+G.diff*14)*(G.snipeDmgBonus||1));
        G.enemyTowerHp[li]=Math.max(0,G.enemyTowerHp[li]-dmg);
        toast('💥 '+LANE_NAMES[li]+' 타워 직격! -'+dmg,'good');
        G.effects.push({x:gx,y:gy,r:10,col:'#ff8c42',alpha:0.9,type:'snipe'});
        G.reloading=true;G.reloadTimer=0;G.reloadMax=70;
        G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';
        hitGate=true;break;
      }
    }
    if(!hitGate){G.combo=1;G.comboTimer=0;document.getElementById('combo-val').textContent='×1';}
  }
}

// ═══════════════════════════════════
//  ABILITIES / SHOP
// ═══════════════════════════════════
function useAbility(i){if(!G.running)return;const a=G.abilities[i];if(a.cd>0){toast('쿨다운 중!','bad');return;}ABILITY_DEFS[i].fx();a.cd=a.maxCd;}
function shopTab(i){
  shopTabIdx_=i;
  document.querySelectorAll('.shop-tab').forEach((t,j)=>t.classList.toggle('active',j===i));
  renderShopGrid_();
}
function renderShopGrid_(){
  document.getElementById('shop-res').textContent=Math.floor(G.resources);
  const grid=document.getElementById('shop-grid');grid.innerHTML='';
  SHOP_TABS_[shopTabIdx_].forEach(item=>{
    const bought=shopBoughtItems.has(item.id)&&!item.rep;
    const div=document.createElement('div');div.className='si'+(bought?' bought':'');
    div.innerHTML='<span class="se">'+item.em+'</span><span class="sn">'+item.name+'</span><span class="sd">'+item.desc+'</span><span class="sc">'+(bought?'구매완료':'💎'+item.cost)+'</span>';
    if(!bought)div.onclick=()=>buyShopItem(item);
    grid.appendChild(div);
  });
}
function openShop(){
  shopTabIdx_=0;
  document.querySelectorAll('.shop-tab').forEach((t,j)=>t.classList.toggle('active',j===0));
  renderShopGrid_();
  document.getElementById('shop-modal').style.display='flex';
}

function closeShop(){document.getElementById('shop-modal').style.display='none';}
function buyShopItem(item){
  if(G.resources<item.cost){toast('💎 자원 부족!','bad');return;}
  G.resources-=item.cost;item.fx();
  if(!item.repeatable)shopBoughtItems.add(item.id);
  openShop();updateHUD();
}

// ═══════════════════════════════════
//  MINIMAP
// ═══════════════════════════════════
function initMinimap(){
  // nothing needed, auto-draws in render
}

function drawMinimap(){
  const mc=document.getElementById('mm-canvas');
  if(!mc) return;
  const mw=mc.width,mh=mc.height;
  const mctx=mc.getContext('2d');
  mctx.clearRect(0,0,mw,mh);
  
  // Background
  mctx.fillStyle='#040810';
  mctx.fillRect(0,0,mw,mh);
  
  // Lane lines
  LANE_Y_FRACS.forEach((frac,li)=>{
    const my=frac*mh;
    mctx.strokeStyle=LANE_COLS[li]+'55';
    mctx.lineWidth=1;
    mctx.setLineDash([3,3]);
    mctx.beginPath();mctx.moveTo(0,my);mctx.lineTo(mw,my);mctx.stroke();
    mctx.setLineDash([]);
  });
  
  // Bases
  mctx.fillStyle='#10d96e';
  mctx.fillRect(0,mh*.5-10,4,20);
  mctx.fillStyle='#ff4560';
  mctx.fillRect(mw-4,mh*.5-10,4,20);
  
  // Units
  G.units.filter(u=>u.hp>0&&u.reachedLane).forEach(u=>{
    const mx_=(u.x/W)*mw;
    const my_=laneY(u.laneIdx)/H*mh;
    const col=u.side===0?'#22d3ee':'#ff4560';
    const r=u.isBoss?3:u.isMiniBoss?2.5:1.5;
    mctx.fillStyle=u.isBoss?'#ffd700':col;
    mctx.beginPath();mctx.arc(mx_,my_,r,0,Math.PI*2);mctx.fill();
  });
  
  // Tower HP indicators
  for(let li=0;li<3;li++){
    const my_=laneY(li)/H*mh;
    // Ally tower
    const aPct=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp);
    mctx.fillStyle=aPct>0.5?'#10d96e':aPct>0.25?'#ffd700':'#ff4560';
    mctx.fillRect(4,my_-2,8*aPct,4);
    // Enemy tower
    const ePct=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp);
    mctx.fillStyle=ePct>0.5?'#ff4560':ePct>0.25?'#ffd700':'#10d96e';
    mctx.fillRect(mw-12,my_-2,8*ePct,4);
  }
}

// ═══════════════════════════════════
//  RENDER
// ═══════════════════════════════════

// ══ UPGRADE SYSTEM ══
const UPGRADES_=[
  {id:0,name:'보병 강화', maxLv:3,cost:[50,100,180],bonus(lv,u){u.atk=Math.round(u.atk*[1.3,1.3,1.4][lv-1]);u.hp=Math.round(u.hp*[1.2,1.2,1.3][lv-1]);}},
  {id:1,name:'돌격대 강화',maxLv:3,cost:[70,130,220],bonus(lv,u){u.atk=Math.round(u.atk*[1.3,1.35,1.4][lv-1]);u.spd*=[1.1,1.1,1.15][lv-1];u.baseSpd=u.spd;}},
  {id:2,name:'중화기 강화',maxLv:3,cost:[100,180,280],bonus(lv,u){u.atk=Math.round(u.atk*[1.35,1.35,1.4][lv-1]);}},
  {id:3,name:'의무병 강화',maxLv:2,cost:[80,160],bonus(lv,u){u.healMult=(u.healMult||1)*[1.4,1.5][lv-1];}},
  {id:4,name:'전차 강화', maxLv:3,cost:[150,260,400],bonus(lv,u){u.hp=Math.round(u.hp*[1.3,1.3,1.35][lv-1]);u.maxHp=u.hp;u.atk=Math.round(u.atk*[1.2,1.25,1.3][lv-1]);}},
  {id:5,name:'닌자 강화', maxLv:2,cost:[90,170],bonus(lv,u){u.atk=Math.round(u.atk*[1.4,1.5][lv-1]);u.spd*=[1.2,1.2][lv-1];u.baseSpd=u.spd;}},
];
let upgLevels_=[0,0,0,0,0,0];
function toggleUpgradePanel(){
  const p=document.getElementById('upgrade-panel');
  p.style.display=p.style.display==='none'?'block':'none';
  if(p.style.display==='block')renderUpgradePanel_();
}
function renderUpgradePanel_(){
  const list=document.getElementById('up-list');if(!list)return;list.innerHTML='';
  UPGRADES_.forEach(up=>{
    const lv=upgLevels_[up.id]||0,maxed=lv>=up.maxLv,cost=maxed?0:up.cost[lv];
    const row=document.createElement('div');row.className='up-row';
    const pips=Array.from({length:up.maxLv},(_,i)=>'<div class="up-pip'+(i<lv?' on':'')+'"></div>').join('');
    row.innerHTML='<span class="up-name">'+up.name+'</span><div class="up-bars">'+pips+'</div><button class="up-btn"'+(maxed||!G.running?' disabled':'')+' onclick="doUpgrade_('+up.id+')">'+(maxed?'MAX':'💎'+cost)+'</button>';
    list.appendChild(row);
  });
}
function doUpgrade_(id){
  const up=UPGRADES_[id],lv=upgLevels_[id]||0;
  if(lv>=up.maxLv){toast('최대 레벨!','bad');return;}
  const cost=up.cost[lv];if(G.resources<cost){toast('자원 부족!','bad');return;}
  G.resources-=cost;upgLevels_[id]=(upgLevels_[id]||0)+1;
  G.units.filter(u=>u.side===0&&u.defId===id).forEach(u=>up.bonus(upgLevels_[id],u));
  toast(up.name+' Lv'+upgLevels_[id]+'!','gold');
  renderUpgradePanel_();updateHUD();updateButtons();
}

function drawMinimap_(){
  const mc=document.getElementById('mm-canvas');if(!mc)return;
  const mw=mc.width,mh=mc.height,mx=mc.getContext('2d');
  mx.clearRect(0,0,mw,mh);mx.fillStyle='#040810';mx.fillRect(0,0,mw,mh);
  [['.28','#b26cf7'],['.55','#22d3ee'],['.82','#10d96e']].forEach(([f,lc],li)=>{
    const my=parseFloat(f)*mh;mx.strokeStyle=lc+'44';mx.lineWidth=1;mx.setLineDash([3,3]);
    mx.beginPath();mx.moveTo(0,my);mx.lineTo(mw,my);mx.stroke();mx.setLineDash([]);
  });
  mx.fillStyle='#10d96e';mx.fillRect(0,mh*.5-10,4,20);
  mx.fillStyle='#ff3355';mx.fillRect(mw-4,mh*.5-10,4,20);
  G.units.filter(u=>u.hp>0&&u.reachedLane).forEach(u=>{
    const ux=(u.x/W)*mw,uy=(laneY(u.laneIdx)/H)*mh;
    const r=u.isBoss?3.5:u.isMiniBoss?2.8:1.8;
    mx.fillStyle=u.isBoss?'#ffd700':u.side===0?'#22d3ee':'#ff3355';
    mx.beginPath();mx.arc(ux,uy,r,0,Math.PI*2);mx.fill();
  });
  for(let li=0;li<3;li++){
    const my=laneY(li)/H*mh,ap=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp),ep=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp);
    mx.fillStyle=ap>.5?'#10d96e':ap>.25?'#ffd700':'#ff3355';mx.fillRect(4,my-2,10*ap,4);
    mx.fillStyle=ep>.5?'#ff3355':ep>.25?'#ffd700':'#10d96e';mx.fillRect(mw-14,my-2,10*ep,4);
  }
}
function render(){
  if(W===0||H===0) return;
  ctx.clearRect(0,0,W,H);

  const isNight=G.weather.night;

  // Sky (전체 배경)
  const sky=ctx.createLinearGradient(0,0,0,H);
  if(isNight){sky.addColorStop(0,'#010510');sky.addColorStop(1,'#0a1628');}
  else if(G.weather.id==='fog'){sky.addColorStop(0,'#1a2035');sky.addColorStop(1,'#2a3555');}
  else{sky.addColorStop(0,'#060a18');sky.addColorStop(1,'#152035');}
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

  // Stars
  if(isNight||G.weather.id==='fog'){
    ctx.fillStyle='rgba(255,255,255,0.7)';
    for(let i=0;i<80;i++){const sx=(i*137.5+G.frame*.01)%W,sy=(i*97.3)%(H*.4);const sz=.6+Math.sin(G.frame*.06+i)*.4;ctx.beginPath();ctx.arc(sx,sy,sz,0,Math.PI*2);ctx.fill();}
  }

  drawMountains();

  // ─── 라인 경로 그리기 (기지 → 라인 → 기지) ───
  drawLanePaths();

  // 기지 그리기
  drawBase(ALLY_BASE_X,  '🏰','#10d96e', G.allyTowerHp,  true);
  drawBase(ENEMY_BASE_X, '🏯','#ff4560', G.enemyTowerHp, false);

  // Rain
  if(G.weather.rain){
    ctx.strokeStyle='rgba(150,180,255,0.28)';ctx.lineWidth=1.2;
    rainDrops.forEach(d=>{d.y+=d.spd;d.x+=1.5;if(d.y>H){d.y=-10;d.x=Math.random()*W;}ctx.beginPath();ctx.moveTo(d.x,d.y);ctx.lineTo(d.x-3,d.y+d.len);ctx.stroke();});
  }
  if(G.weather.id==='fog'||G.weather.id==='storm'){
    const fogG=ctx.createLinearGradient(0,0,W,0);
    fogG.addColorStop(0,'rgba(180,200,220,0.07)');fogG.addColorStop(.4+Math.sin(G.frame*.005)*.1,'rgba(180,200,220,0.17)');fogG.addColorStop(1,'rgba(180,200,220,0.05)');
    ctx.fillStyle=fogG;ctx.fillRect(0,0,W,H);
  }
  if(G.freezeEnd>0&&G.frame<G.freezeEnd){
    const fPct=Math.max(0,1-(G.frame-(G.freezeEnd-240))/240);
    ctx.fillStyle='rgba(100,180,255,'+(0.07*fPct)+')';ctx.fillRect(0,0,W,H);
  }

  // Shield glow
  if(G.shieldEnd>0&&G.frame<G.shieldEnd){
    const pulse=0.4+Math.sin(G.frame*.15)*.3;
    ctx.shadowBlur=30;ctx.shadowColor='rgba(34,211,238,'+pulse+')';
    ctx.strokeStyle='rgba(34,211,238,'+pulse+')';ctx.lineWidth=3;
    ctx.beginPath();ctx.arc(ALLY_BASE_X,H*.5,60,0,Math.PI*2);ctx.stroke();
    ctx.shadowBlur=0;
  }

  // 크레이터
  G.craters.forEach(cr=>{
    ctx.fillStyle='rgba(0,0,0,0.3)';
    ctx.beginPath();ctx.ellipse(cr.x,cr.y+cr.r*.3,cr.r,cr.r*.38,0,0,Math.PI*2);ctx.fill();
  });

  // Effects
  G.effects.forEach(e=>{
    ctx.globalAlpha=Math.max(0,e.alpha);
    if(e.type==='bomb'){ctx.shadowBlur=30;ctx.shadowColor='#ff8c42';ctx.fillStyle='rgba(255,140,66,'+e.alpha+')';ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;}
    else{ctx.strokeStyle=e.col;ctx.lineWidth=e.type==='snipe'?3.5:e.type==='death'?1.5:1.8;ctx.shadowBlur=e.type==='snipe'?20:0;ctx.shadowColor=e.col;ctx.beginPath();ctx.arc(e.x,e.y,e.r,0,Math.PI*2);ctx.stroke();ctx.shadowBlur=0;}
    ctx.globalAlpha=1;
  });

  // Units (Z-sort by Y)
  G.units.filter(u=>u.hp>0).sort((a,b)=>a.y-b.y).forEach(drawUnit);

  // Bullets
  G.bullets.forEach(b=>{
    ctx.shadowBlur=8;ctx.shadowColor=b.col;
    ctx.fillStyle=b.col;
    const bsize=b.col==='#ffd700'?6:b.col==='#b26cf7'?4.5:4;
    ctx.beginPath();ctx.arc(b.x,b.y,bsize,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
  });

  // Particles
  G.particles.forEach(p=>{ctx.globalAlpha=Math.min(1,p.life/10);ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill();ctx.globalAlpha=1;});

  // Vignette
  if(!G.reloading&&G.running&&G.mouseX>0){
    const vg=ctx.createRadialGradient(G.mouseX,G.mouseY,55,G.mouseX,G.mouseY,Math.max(W,H)*.72);
    vg.addColorStop(0,'rgba(0,0,0,0)');vg.addColorStop(1,'rgba(0,0,0,0.4)');
    ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  }

  // Minimap
  drawMinimap();

  // Headshot hint
  if(!G.reloading&&G.running){
    const hovered=G.units.find(u=>u.side===1&&u.hp>0&&u.reachedLane&&Math.sqrt((G.mouseX-u.x)**2+(G.mouseY-(u.y-18))**2)<44);
    if(hovered){ctx.strokeStyle='rgba(255,215,0,0.4)';ctx.lineWidth=1.5;ctx.setLineDash([3,3]);ctx.beginPath();ctx.arc(hovered.x,hovered.y-31,19,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);}
  }
}

// ─── 라인 경로 그리기 ───
function drawLanePaths(){
  const agx=allyGateX(), egx=enemyGateX();
  for(let li=0;li<3;li++){
    const agy=allyGateY(li);
    const egy=enemyGateY(li);
    const ly=laneY(li);
    const lc=LANE_COLS[li];
    const isFocus=(li===G.botFocusLane);
    const isSel=(li===G.selectedLane);

    // 라인 배경 (지면)
    const bandTop=li===0?0:(li===1?laneY(0)+28:laneY(1)+28);
    const bandBot=li===2?H:(li===1?laneY(1)+28:laneY(0)+28);
    const bh=li===0?ly+40:li===2?H-(ly-40):80;
    ctx.fillStyle='rgba(20,35,12,0.55)';
    if(li===0) ctx.fillRect(agx,0,egx-agx,ly+35);
    else if(li===2) ctx.fillRect(agx,ly-35,egx-agx,H-(ly-35));
    else ctx.fillRect(agx,ly-38,egx-agx,76);

    // 경로 라인 (기지 게이트 → 라인 → 기지 게이트)
    // 경로: (agx, agy) → (agx+60, ly) → (egx-60, ly) → (egx, egy)
    const mx1=agx+65, mx2=egx-65;
    ctx.beginPath();
    ctx.moveTo(agx, agy);
    ctx.bezierCurveTo(mx1, agy, mx1, ly, mx1, ly);
    ctx.lineTo(mx2, ly);
    ctx.bezierCurveTo(mx2, ly, mx2, egy, egx, egy);

    const alpha=isFocus?0.85:isSel?0.7:0.35;
    ctx.strokeStyle=isFocus?'rgba(255,69,96,'+alpha+')':lc.replace('#','rgba(').replace(/(..)(..)(..)/, (m,r,g,b)=>`rgba(${parseInt(r,16)},${parseInt(g,16)},${parseInt(b,16)},`)+alpha+')';

    // 더 간단하게
    ctx.strokeStyle=isFocus?`rgba(255,69,96,${alpha})`:`${lc}${Math.round(alpha*255).toString(16).padStart(2,'0')}`;
    ctx.lineWidth=isFocus?3.5:isSel?3:1.8;
    ctx.setLineDash(isFocus?[]:[6,6]);
    ctx.stroke();
    ctx.setLineDash([]);

    // 지면 풀 (경로 아래 선)
    ctx.strokeStyle=isSel?lc+'aa':'rgba(80,140,40,0.25)';
    ctx.lineWidth=isSel?2:1;
    ctx.beginPath();ctx.moveTo(mx1,ly);ctx.lineTo(mx2,ly);ctx.stroke();

    // 라인 레이블
    const lbl=LANE_NAMES[li]+(isSel?' ◀':'');
    ctx.fillStyle=isSel?lc:isFocus?'#ff4560':'rgba(255,255,255,0.35)';
    ctx.font=`bold ${isSel?13:11}px "Noto Sans KR"`;
    ctx.textAlign='center';
    ctx.fillText(lbl,(mx1+mx2)/2,ly-10);
    if(isFocus&&!isSel){ctx.fillStyle='rgba(255,69,96,0.7)';ctx.font='bold 10px sans-serif';ctx.fillText('⚠️',mx1+(mx2-mx1)*.7,ly-10);}
    ctx.textAlign='left';

    // 타워 HP 바 (라인 경로 시작/끝에 표시)
    const barW=55, barH=5;
    // 아군 타워 HP (왼쪽 경로 시작)
    const aHpPct=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp);
    ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(mx1-barW/2,ly+8,barW,barH);
    ctx.fillStyle=aHpPct>0.5?'#10d96e':aHpPct>0.25?'#ffd700':'#ff4560';
    ctx.fillRect(mx1-barW/2,ly+8,barW*aHpPct,barH);
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=0.5;ctx.strokeRect(mx1-barW/2,ly+8,barW,barH);
    // 적 타워 HP (오른쪽 경로 끝)
    const eHpPct=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp);
    ctx.fillStyle='rgba(0,0,0,0.5)';ctx.fillRect(mx2-barW/2,ly+8,barW,barH);
    ctx.fillStyle=eHpPct>0.5?'#ff4560':eHpPct>0.25?'#ffd700':'#10d96e';
    ctx.fillRect(mx2-barW/2,ly+8,barW*eHpPct,barH);
    ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=0.5;ctx.strokeRect(mx2-barW/2,ly+8,barW,barH);
  }
}

function drawMountains(){
  ctx.fillStyle='rgba(10,18,38,0.65)';
  ctx.beginPath();ctx.moveTo(0,H*.3);
  for(let x=0;x<=W;x+=80) ctx.lineTo(x,H*.3-40-Math.sin(x*.01)*30-Math.sin(x*.025)*18);
  ctx.lineTo(W,H*.3);ctx.closePath();ctx.fill();
  ctx.fillStyle='rgba(12,22,44,0.45)';
  ctx.beginPath();ctx.moveTo(0,H*.3);
  for(let x=0;x<=W;x+=55) ctx.lineTo(x,H*.3-20-Math.sin(x*.018+1)*18-Math.sin(x*.04)*10);
  ctx.lineTo(W,H*.3);ctx.closePath();ctx.fill();
}

// 기지 그리기 — 3개 라인 게이트 포함
function drawBase(cx, em, col, towerHps, isAlly){
  const bx=isAlly?cx-BASE_W/2:cx-BASE_W/2, by=H*.5-BASE_H/2;

  // 기지 본체
  ctx.shadowBlur=24;ctx.shadowColor=col;
  ctx.fillStyle='rgba(12,22,46,0.95)';ctx.strokeStyle=col;ctx.lineWidth=2.4;
  rr(ctx,bx,by,BASE_W,BASE_H,8);ctx.fill();ctx.stroke();ctx.shadowBlur=0;

  // 기지 전체 HP 바
  const totalHp=towerHps.reduce((s,h)=>s+h,0);
  const totalMax=G.maxTowerHp*3;
  const hbw=BASE_W-10;
  ctx.fillStyle='rgba(0,0,0,0.55)';rr(ctx,bx+5,by+7,hbw,9,4);ctx.fill();
  const hcol=(totalHp/totalMax)>0.5?col:(totalHp/totalMax)>0.25?'#ffd700':'#ff4560';
  ctx.fillStyle=hcol;rr(ctx,bx+5,by+7,Math.max(0,hbw*(totalHp/totalMax)),9,4);ctx.fill();

  // 기지 아이콘
  ctx.font='24px sans-serif';ctx.textAlign='center';ctx.fillText(em,bx+BASE_W/2,by+BASE_H-16);

  // 3개 라인 게이트 (기지 측면)
  for(let li=0;li<3;li++){
    const gy=allyGateY(li);
    const hpPct=Math.max(0,towerHps[li]/G.maxTowerHp);
    const lc=LANE_COLS[li];
    const gateX=isAlly?bx+BASE_W:bx;

    // 게이트 포트 표시
    ctx.fillStyle=hpPct>0.5?lc:hpPct>0.25?'#ffd700':'#ff4560';
    ctx.shadowBlur=hpPct>0.25?6:12;ctx.shadowColor=ctx.fillStyle;
    ctx.beginPath();ctx.arc(gateX,gy,5,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;

    // 라인 HP 작은 바
    const lbw=BASE_W-16, lbh=3;
    const lby=by+16+li*(BASE_H-22)/3;
    ctx.fillStyle='rgba(0,0,0,0.45)';ctx.fillRect(bx+8,lby,lbw,lbh);
    ctx.fillStyle=hpPct>0.5?lc:hpPct>0.25?'#ffd700':'#ff4560';
    ctx.fillRect(bx+8,lby,lbw*hpPct,lbh);
  }

  // 터렛
  if(isAlly&&G.turretLevel>0){
    ctx.fillStyle='#b26cf7';ctx.shadowBlur=10;ctx.shadowColor='#b26cf7';
    ctx.fillRect(bx+BASE_W/2-4,by-20,8,14);ctx.fillRect(bx+BASE_W/2-2,by-26,4,8);ctx.shadowBlur=0;
    ctx.font='bold 9px sans-serif';ctx.fillStyle='#b26cf7';ctx.textAlign='center';ctx.fillText('Lv'+G.turretLevel,bx+BASE_W/2,by-30);
  }

  // HP 수치
  ctx.font='bold 8px sans-serif';ctx.fillStyle='rgba(255,255,255,0.55)';ctx.textAlign='center';
  ctx.fillText(Math.round(Math.max(0,totalHp)),bx+BASE_W/2,by+BASE_H+12);
}

function drawUnit(u){
  const x=u.x,y=u.y;
  const col=u.side===0?'#22d3ee':'#ff4560';
  const bounce=Math.sin(u.anim)*2.2;
  const scale=u.isBoss?1.7:u.isMiniBoss?1.35:1;
  const frozen=(G.freezeEnd>0&&G.frame<G.freezeEnd&&u.side===1);

  ctx.fillStyle='rgba(0,0,0,0.22)';
  ctx.beginPath();ctx.ellipse(x,y+2,13*scale,4*scale,0,0,Math.PI*2);ctx.fill();

  const r=14*scale;
  ctx.fillStyle=frozen?'rgba(30,60,120,0.9)':u.side===0?'rgba(0,45,75,0.88)':'rgba(75,0,20,0.88)';
  ctx.strokeStyle=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'#4dacf7':col;
  ctx.lineWidth=u.isBoss?2.5:u.isMiniBoss?2:1.8;
  ctx.shadowBlur=u.isBoss?18:u.isMiniBoss?12:7;
  ctx.shadowColor=u.isBoss?'#ffd700':u.isMiniBoss?'#ff8c42':frozen?'rgba(100,180,255,0.8)':col;
  ctx.beginPath();ctx.arc(x,y-r+bounce,r,0,Math.PI*2);ctx.fill();ctx.stroke();ctx.shadowBlur=0;

  ctx.font=(u.isBoss?'22':u.isMiniBoss?'18':'14')+'px sans-serif';ctx.textAlign='center';
  ctx.fillText(u.em,x,y-r+bounce+5);

  if(u.isBoss){ctx.font='bold 10px "Noto Sans KR"';ctx.fillStyle='#ffd700';ctx.fillText('💀 BOSS',x,y-r*2+bounce-4);}
  if(u.isMiniBoss){ctx.font='bold 9px "Noto Sans KR"';ctx.fillStyle='#ff8c42';ctx.fillText('😈 MINI',x,y-r*2+bounce-4);}

  if(frozen){
    ctx.strokeStyle='rgba(100,220,255,0.5)';ctx.lineWidth=1;
    for(let i=0;i<4;i++){const ang=(i/4)*Math.PI*2;ctx.beginPath();ctx.moveTo(x,y-r+bounce);ctx.lineTo(x+Math.cos(ang)*(r+6),y-r+bounce+Math.sin(ang)*(r+6));ctx.stroke();}
  }

  // 기지 공격 중 표시
  if(u.atBaseGate){
    ctx.strokeStyle=u.side===0?'#22d3ee':'#ff4560';ctx.lineWidth=1.5;ctx.setLineDash([2,3]);
    ctx.beginPath();ctx.arc(x,y-r+bounce,r+5,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);
  }

  const pct=u.hp/u.maxHp;
  const bw2=u.isBoss?54:u.isMiniBoss?38:28;
  ctx.fillStyle='rgba(0,0,0,0.5)';rr(ctx,x-bw2/2,y-r*2+bounce-2,bw2,5,2);ctx.fill();
  ctx.fillStyle=pct>0.5?'#10d96e':pct>0.25?'#ffd700':'#ff4560';
  rr(ctx,x-bw2/2,y-r*2+bounce-2,Math.max(0,bw2*pct),5,2);ctx.fill();
}

function rr(ctx,x,y,w,h,r){
  ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);
  ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();
}

// ═══════════════════════════════════
//  HUD
// ═══════════════════════════════════
function updateHUD(){
  if(!G.running) return;
  const totalAlly=G.allyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalEnemy=G.enemyTowerHp.reduce((s,h)=>s+Math.max(0,h),0);
  const totalMax=G.maxTowerHp*3;
  document.getElementById('ally-hp-val').textContent=Math.round(totalAlly);
  document.getElementById('enemy-hp-val').textContent=Math.round(totalEnemy);
  document.getElementById('ally-hp-bar').style.width=(totalAlly/totalMax*100)+'%';
  document.getElementById('enemy-hp-bar').style.width=(totalEnemy/totalMax*100)+'%';
  document.getElementById('res-val').textContent=Math.floor(G.resources);
  document.getElementById('score-val').textContent=G.score.toLocaleString();
  document.getElementById('kills-val').textContent=G.kills;
  // Wave progress
  const wavePct=((G.waveTimer/1800)*100).toFixed(1);
  const wf=document.getElementById('wave-fill');
  if(wf) wf.style.width=wavePct+'%';
}

function updateLaneStatus(){
  if(!G.lanes&&!G.allyTowerHp) return;
  for(let li=0;li<3;li++){
    const aHp=Math.max(0,G.allyTowerHp[li]/G.maxTowerHp*100);
    const eHp=Math.max(0,G.enemyTowerHp[li]/G.maxTowerHp*100);
    const af=document.getElementById('ls-ally-'+li);
    const ef=document.getElementById('ls-enemy-'+li);
    if(af) af.style.width=aHp*.48+'%';
    if(ef) ef.style.width=eHp*.48+'%';
    const ally=G.units.filter(u=>u.side===0&&u.hp>0&&u.laneIdx===li).length;
    const enemy=G.units.filter(u=>u.side===1&&u.hp>0&&u.laneIdx===li).length;
    const uel=document.getElementById('ls-units-'+li);
    if(uel) uel.textContent=ally+'v'+enemy;
    // ★ 라인 버튼에 함락/클리어 상태 표시 ★
    const lbtn=document.getElementById('lane-btn-'+li);
    if(lbtn){
      const allyFallen=G.allyTowerHp[li]<=0;
      const enemyFallen=G.enemyTowerHp[li]<=0;
      if(allyFallen){
        lbtn.style.opacity='0.45';
        lbtn.title='함락됨 - 소환 불가';
        // 빨간 테두리로 강조
        if(li===G.selectedLane){
          // 함락된 라인이 선택되면 자동으로 다른 라인 선택
          const newLane=[0,1,2].find(x=>x!==li&&G.allyTowerHp[x]>0);
          if(newLane!==undefined) selectLane(newLane);
        }
      } else {
        lbtn.style.opacity='1';
        lbtn.title='';
      }
      // 적 타워 클리어 표시
      const lnameArr=['⬆️ 탑','➡️ 미드','⬇️ 봇'];
      if(allyFallen&&enemyFallen){
        lbtn.textContent=lnameArr[li]+' 🚫'; // 완전 폐쇄
        lbtn.title='완전 함락 - 양쪽 소환 불가';
      } else if(enemyFallen&&!allyFallen){
        lbtn.textContent=lnameArr[li]+' ✅'; // 적 라인 클리어
      } else if(allyFallen){
        lbtn.textContent=lnameArr[li]+' 💀'; // 아군 함락
      } else {
        lbtn.textContent=lnameArr[li];
      }
    }
  }
}

function updateButtons(){
  // 업그레이드 레벨 표시
  for(let i=0;i<9;i++){
    const lv=upgLevels_[i]||0;
    const el=document.getElementById('ulv'+i);
    if(el)el.textContent=lv>0?'★'.repeat(lv):'';
  }
  const laneBlocked=G.allyTowerHp&&G.allyTowerHp[G.selectedLane]<=0;
  for(let i=0;i<9;i++){
    const btn=document.getElementById('btn'+i);
    if(!btn) continue;
    btn.disabled=!G.running||G.resources<UNIT_DEFS[i].cost||G.trainCooldowns[i]>0||laneBlocked;
    if(laneBlocked) btn.style.opacity='0.3';
    else btn.style.opacity='';
  }
}

// ═══════════════════════════════════
//  KILL FEED
// ═══════════════════════════════════
function addKillFeed(unit){
  const kf=document.getElementById('killfeed');
  const d=document.createElement('div');d.className='kfi';
  d.textContent='['+LANE_NAMES[unit.laneIdx]+'] 🎯 '+unit.em+' '+unit.name+(unit.isBoss?' 🏆':unit.isMiniBoss?' 👑':'');
  d.style.borderColor=unit.isBoss?'rgba(255,215,0,.6)':unit.isMiniBoss?'rgba(255,140,66,.5)':'rgba(255,69,96,.3)';
  d.style.color=unit.isBoss?'#ffd700':unit.isMiniBoss?'#ff8c42':'var(--text)';
  kf.insertBefore(d,kf.firstChild);
  setTimeout(()=>d.remove(),3000);
  while(kf.children.length>5)kf.removeChild(kf.lastChild);
}

// ═══════════════════════════════════
//  GAME END
// ═══════════════════════════════════
function endGame(win){
  if(!G.running) return;
  G.running=false;
  document.getElementById('scope').style.display='none';
  canvas.style.cursor='default';
  const maxScore=G.wave*1200*(G.diff+1);
  const ratio=G.score/Math.max(maxScore,1);
  const grade=win?(ratio>0.8?'S':ratio>0.6?'A':ratio>0.4?'B':'C'):'D';
  const gradeCol={S:'#ffd700',A:'#10d96e',B:'#4dabf7',C:'#ff8c42',D:'#ff4560'}[grade];
  const rs=document.getElementById('result');rs.style.display='flex';
  document.getElementById('res-grade').textContent=grade;
  document.getElementById('res-grade').style.color=gradeCol;
  document.getElementById('res-title').textContent=win?'🏆 승리!':'💀 패배...';
  document.getElementById('res-title').style.color=win?'#10d96e':'#ff4560';
  document.getElementById('res-subtitle').textContent=DIFF_CONFIG[G.diff].name+' · 웨이브 '+G.wave+' · 등급 '+grade+' · 헤드샷 '+G.headshots+'회';
  document.getElementById('st-score').textContent=G.score.toLocaleString();
  document.getElementById('st-kills').textContent=G.kills;
  document.getElementById('st-wave').textContent=G.wave;
  document.getElementById('st-snipes').textContent=G.snipes;
  const sths=document.getElementById('st-hs');if(sths)sths.textContent=G.headshots||0;
  if(win)spawnFireworks();
  try{window.parent.postMessage({type:'sniper_result',score:G.score,kills:G.kills,wave:G.wave,snipes:G.snipes,win:win?1:0,diff:G.diff},'*');}catch(e){}
}

function spawnFireworks(){
  const bg=document.getElementById('fw');
  const cols=['#ffd700','#ff4560','#4dabf7','#10d96e','#b26cf7','#22d3ee'];
  for(let f=0;f<14;f++) setTimeout(()=>{
    const x=10+Math.random()*80,y=5+Math.random()*55,col=cols[f%6];
    for(let i=0;i<28;i++){
      const p=document.createElement('div');
      const ang=(i/28)*Math.PI*2,dist=55+Math.random()*110,dur=.55+Math.random()*.65;
      p.style.cssText='position:absolute;left:'+x+'%;top:'+y+'%;width:5px;height:5px;border-radius:50%;background:'+col+';animation:fwp '+dur+'s ease-out forwards;--dx:'+Math.cos(ang)*dist+'px;--dy:'+Math.sin(ang)*dist+'px;';
      bg.appendChild(p);setTimeout(()=>p.remove(),(dur+.1)*1000);
    }
  },f*350);
}

function toast(txt,type){
  const w=document.getElementById('twrap');
  const d=document.createElement('div');d.className='toast';
  const colors={good:'rgba(16,217,110,.4)',bad:'rgba(255,69,96,.4)',gold:'rgba(255,215,0,.4)',wave:'rgba(178,108,247,.4)'};
  d.style.borderColor=colors[type]||'rgba(255,255,255,.1)';
  d.textContent=txt;w.insertBefore(d,w.firstChild);
  setTimeout(()=>d.remove(),2800);
  while(w.children.length>5)w.removeChild(w.lastChild);
}

// ═══════════════════════════════════
//  EVENTS
// ═══════════════════════════════════
document.addEventListener('mousemove',e=>{
  const sc=document.getElementById('scope');sc.style.left=e.clientX+'px';sc.style.top=e.clientY+'px';
  if(G.running){const rect=canvas.getBoundingClientRect();G.mouseX=e.clientX-rect.left;G.mouseY=e.clientY-rect.top;}
  const col=G.reloading?'rgba(120,120,120,0.6)':'rgba(255,69,96,0.9)';
  sc.querySelectorAll('circle[stroke],line').forEach(el=>{if(el.getAttribute('stroke'))el.setAttribute('stroke',col);});
});

canvas.addEventListener('click',e=>{
  if(!G.running)return;
  const rect=canvas.getBoundingClientRect();
  tryShoot(e.clientX-rect.left,e.clientY-rect.top);
});

document.addEventListener('keydown',e=>{
  if(!G.running)return;
  if(['1','2','3','4','5','6','7','8','9','q','e','r','w','t','s','f','g','h'].includes(e.key.toLowerCase()))e.preventDefault();
  const keys={'1':0,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8};
  if(keys[e.key]!==undefined){spawnAlly(parseInt(e.key)-1);return;}
  if(e.key.toLowerCase()==='q')useAbility(0);
  if(e.key.toLowerCase()==='e')useAbility(1);
  if(e.key.toLowerCase()==='r')useAbility(2);
  if(e.key.toLowerCase()==='w')useAbility(3);
  if(e.key.toLowerCase()==='t')useAbility(4);
  if(e.key.toLowerCase()==='s')openShop();
  // 라인 전환: F=탑, G=미드, H=봇
  if(e.key.toLowerCase()==='f')selectLane(0);
  if(e.key.toLowerCase()==='g')selectLane(1);
  if(e.key.toLowerCase()==='h')selectLane(2);
  if(e.key.toLowerCase()==='y')useAbility(5);
  if(e.key.toLowerCase()==='z')toggleUpgradePanel();
  if(e.key.toLowerCase()==='x'){
    if(G.resources>=80){G.resources-=80;for(let i=0;i<3;i++)G.allyTowerHp[i]=Math.min(G.allyTowerHp[i]+120,G.maxTowerHp);toast('긴급수리!','good');}
    else toast('자원부족!','bad');
  }
});

let selDiff=0;
document.querySelectorAll('.diff-card').forEach(card=>{
  card.addEventListener('click',()=>{
    document.querySelectorAll('.diff-card').forEach(c=>c.classList.remove('sel'));
    card.classList.add('sel');selDiff=parseInt(card.dataset.d);
  });
});
document.getElementById('start-btn').addEventListener('click',()=>startGame(selDiff));

window.addEventListener('resize',()=>{if(G.running)resize();});

// ResizeObserver: iframe 내 캔버스 크기가 뒤늦게 확정될 때도 대응
if(window.ResizeObserver){
  const _ro=new ResizeObserver(()=>{
    if(G.running){
      const prev_W=W,prev_H=H;
      resize();
      // 크기가 의미있게 변했을 때만 재초기화
      if(Math.abs(W-prev_W)>20||Math.abs(H-prev_H)>20){
        // 크레이터 재배치
        G.craters=[];
        for(let i=0;i<6;i++) G.craters.push({x:150+Math.random()*(W-300),y:laneY(Math.floor(i/2)),r:14+Math.random()*18});
      }
    }
  });
  _ro.observe(canvas);
  // game div도 감시 (flex 레이아웃)
  const gameDiv=document.getElementById('game');
  if(gameDiv) _ro.observe(gameDiv);
}
</script>
</body>
</html>"""


def render():
    import os as _os
    from utils.database import update_leaderboard, _get_col
    from utils.config import USERS_FILE

    st.markdown("""<style>
iframe[title="components.html"] {
  border: none !important;
  border-radius: 14px !important;
  display: block !important;
  pointer-events: auto !important;
}
</style>""", unsafe_allow_html=True)
    st.caption("🎯 마우스 클릭: 저격 | 1~9: 유닛 소환 | Q/E/R/W/T: 스킬 | S: 상점 | F/G/H: 라인전환")

    _cur_uid = st.session_state.get('logged_in_user', '')

    _bridge_dir = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'components', 'game_bridge')
    _bridge = st.components.v1.declare_component("game_bridge_sniper", path=_bridge_dir)
    _result = _bridge(game_type="sniper_result", key=f"bridge_sniper_{_cur_uid}", default=None)

    if _result and isinstance(_result, dict) and _result.get('type') == 'sniper_result':
        if not st.session_state.get('_sniper_saved'):
            st.session_state['_sniper_saved'] = True
            try:
                _s_score = int(_result.get('score', 0))
                _s_kills = int(_result.get('kills', 0))
                _s_wave  = int(_result.get('wave', 1))
                if _s_score > 0 and _cur_uid:
                    _col = _get_col(USERS_FILE)
                    _doc = _col.find_one({"_id": "main"}, {_cur_uid: 1})
                    if _doc and _cur_uid in _doc:
                        _udata = _doc[_cur_uid]
                        if _s_score > _udata.get('game_records', {}).get('sniper', {}).get('score', 0):
                            _col.update_one({"_id": "main"}, {"$set": {
                                f"{_cur_uid}.game_records.sniper.score": _s_score,
                                f"{_cur_uid}.game_records.sniper.kills": _s_kills,
                                f"{_cur_uid}.game_records.sniper.wave":  _s_wave,
                            }})
                            update_leaderboard('sniper', _udata.get('nickname', _cur_uid), _s_score)
                            st.toast(f"🎯 저격전 최고기록 {_s_score:,}점 저장!", icon="🏆")
                            st.rerun()
            except Exception as _e:
                import logging; logging.error(f"[sniper save] {_e}")
    if not _result:
        st.session_state.pop('_sniper_saved', None)

    # 게임 높이를 충분히 확보
    components.html(GAME_HTML, height=940, scrolling=False)
