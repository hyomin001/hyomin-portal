import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>인베스트마블 ULTRA MAX</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=Black+Han+Sans&family=Orbitron:wght@600;700;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#03060e;--bg2:#06091a;--bg3:#0a1028;--bg4:#0d1535;
  --gold:#ffd700;--gold2:#ffb800;--gold3:#ff8c00;
  --green:#00ff88;--green2:#10d96e;--green3:#00c965;
  --red:#ff3355;--red2:#ff4560;
  --blue:#4dabf7;--blue2:#228be6;
  --purple:#c084fc;--purple2:#a855f7;
  --cyan:#22d3ee;--cyan2:#06b6d4;
  --orange:#fb923c;--orange2:#f97316;
  --pink:#f472b6;
  --text:#e8f0ff;--text2:#6b7fa8;--text3:#3d4f6e;
  --border:rgba(255,255,255,0.06);
  --border2:rgba(255,255,255,0.12);
  --glow-gold:rgba(255,215,0,0.3);
  --glow-green:rgba(0,255,136,0.25);
  --glow-red:rgba(255,51,85,0.3);
  --glow-cyan:rgba(34,211,238,0.25);
  --r:14px;--r2:10px;--r3:8px;
  --shadow:0 20px 60px rgba(0,0,0,0.8);
  --transition:all 0.22s cubic-bezier(0.4,0,0.2,1);
}
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent;}
html,body{
  font-family:'Noto Sans KR',sans-serif;
  background:var(--bg);color:var(--text);
  overflow-x:hidden;min-height:100vh;
  user-select:none;
}

/* ===== AMBIENT BG ===== */
.ambient{
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background:
    radial-gradient(ellipse 80% 50% at 10% 0%,rgba(120,0,220,.06) 0%,transparent 60%),
    radial-gradient(ellipse 60% 60% at 90% 100%,rgba(0,80,200,.07) 0%,transparent 55%),
    radial-gradient(ellipse 40% 40% at 50% 50%,rgba(255,215,0,.02) 0%,transparent 70%);
}
.grid-bg{
  position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(255,255,255,.015) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,.015) 1px,transparent 1px);
  background-size:40px 40px;
  mask-image:radial-gradient(ellipse 80% 80% at 50% 50%,black 30%,transparent 100%);
}

/* ===== SCANLINE ===== */
@keyframes scan{0%{transform:translateY(-100%);}100%{transform:translateY(100vh);}}
.scanline{
  position:fixed;inset:0;pointer-events:none;z-index:1;overflow:hidden;
}
.scanline::after{
  content:'';position:absolute;left:0;right:0;height:2px;
  background:linear-gradient(transparent,rgba(34,211,238,.04),transparent);
  animation:scan 8s linear infinite;
}

/* ===== PARTICLES ===== */
#particles{position:fixed;inset:0;pointer-events:none;z-index:0;}
.pt{
  position:absolute;width:2px;height:2px;border-radius:50%;
  background:rgba(255,215,0,.4);
  animation:ptf var(--dur,8s) ease-in-out infinite var(--delay,0s);
}
@keyframes ptf{
  0%{transform:translate(0,0);opacity:0;}
  10%{opacity:1;}
  90%{opacity:.5;}
  100%{transform:translate(var(--tx,20px),var(--ty,-80px));opacity:0;}
}

/* ===== FIREWORKS ===== */
#fw{position:fixed;inset:0;pointer-events:none;z-index:490;overflow:hidden;}
@keyframes fwp{to{transform:translate(var(--dx),var(--dy)) scale(0);opacity:0;}}
@keyframes fwt{0%{transform:translateY(0);opacity:1;}100%{transform:translateY(-200px);opacity:0;}}

/* ========================================
   CHARACTER SELECT
   ======================================== */
#cs{
  position:fixed;inset:0;z-index:200;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:var(--bg);
  overflow-y:auto;padding:20px 16px 40px;
}
.cs-logo{margin-bottom:4px;text-align:center;}
.cs-logo .globe{font-size:2.8rem;animation:globeSpin 8s linear infinite;}
@keyframes globeSpin{from{filter:hue-rotate(0deg);}to{filter:hue-rotate(360deg);}}
.cs-title{
  font-family:'Black Han Sans',sans-serif;
  font-size:clamp(2rem,5vw,3.2rem);
  background:linear-gradient(135deg,#ffd700 0%,#ff8c00 40%,#ff3355 80%,#c084fc 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  letter-spacing:2px;text-align:center;
  filter:drop-shadow(0 0 20px rgba(255,215,0,.3));
}
.cs-sub{
  color:var(--text2);font-size:.72rem;letter-spacing:6px;
  margin:6px 0 28px;text-align:center;
  font-family:'Rajdhani',sans-serif;font-weight:600;
}
.section-label{
  font-size:.68rem;letter-spacing:4px;color:var(--text3);
  font-family:'Rajdhani',sans-serif;font-weight:600;
  margin-bottom:12px;text-align:center;
  text-transform:uppercase;
}
.cgrid{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:10px;max-width:740px;width:100%;margin-bottom:28px;
}
.ccard{
  background:rgba(255,255,255,.03);
  border:1.5px solid rgba(255,255,255,.07);
  border-radius:var(--r);padding:16px 10px 14px;
  cursor:pointer;transition:var(--transition);text-align:center;
  position:relative;overflow:hidden;
}
.ccard::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse at 50% 0%,rgba(255,215,0,.06),transparent 70%);
  opacity:0;transition:opacity .3s;
}
.ccard:hover::before,.ccard.sel::before{opacity:1;}
.ccard:hover,.ccard.sel{
  transform:translateY(-5px);
  border-color:var(--gold);
  box-shadow:0 0 0 1px rgba(255,215,0,.1),0 12px 40px rgba(0,0,0,.5),0 0 30px rgba(255,215,0,.15);
}
.ccard.sel{background:rgba(255,215,0,.04);}
.ccard .em{font-size:2.5rem;display:block;margin-bottom:8px;filter:drop-shadow(0 4px 8px rgba(0,0,0,.5));}
.ccard .cn{font-weight:700;font-size:.88rem;margin-bottom:2px;}
.ccard .ct{font-size:.68rem;color:var(--text2);margin-bottom:6px;}
.ccard .cb{
  font-size:.66rem;color:var(--cyan);font-weight:700;
  background:rgba(34,211,238,.08);border:1px solid rgba(34,211,238,.2);
  border-radius:20px;padding:3px 8px;display:inline-block;
}
.ccard .cstat{
  display:flex;gap:4px;justify-content:center;margin-top:8px;
}
.cstat-bar{height:3px;border-radius:2px;flex:1;background:rgba(255,255,255,.06);}
.cstat-bar .fill{height:100%;border-radius:2px;transition:width .5s .2s;}

/* TURN + DIFF SELECTORS */
.select-row{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;margin-bottom:10px;}
.pill-btn{
  padding:8px 18px;border-radius:22px;
  border:1.5px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.03);
  color:var(--text2);cursor:pointer;
  font-size:.8rem;font-weight:700;
  font-family:'Rajdhani',sans-serif;
  transition:var(--transition);letter-spacing:1px;
}
.pill-btn:hover,.pill-btn.a{
  border-color:var(--cyan);color:var(--cyan);
  background:rgba(34,211,238,.08);
  box-shadow:0 0 16px rgba(34,211,238,.15);
}

/* DIFF PILLS */
.diff-btn{
  padding:8px 18px;border-radius:22px;
  border:1.5px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.03);
  color:var(--text2);cursor:pointer;
  font-size:.78rem;font-weight:700;
  font-family:'Rajdhani',sans-serif;
  transition:var(--transition);letter-spacing:1px;
}
.diff-btn.a-easy{border-color:var(--green2);color:var(--green2);background:rgba(16,217,110,.06);}
.diff-btn.a-normal{border-color:var(--cyan);color:var(--cyan);background:rgba(34,211,238,.06);}
.diff-btn.a-hard{border-color:var(--red2);color:var(--red2);background:rgba(255,69,96,.06);}

.start-btn{
  margin-top:22px;padding:14px 56px;
  font-size:1.05rem;font-weight:900;
  font-family:'Black Han Sans',sans-serif;
  background:linear-gradient(135deg,#ffd700,#ff8c00);
  color:#100800;border:none;border-radius:40px;
  cursor:pointer;letter-spacing:3px;
  box-shadow:0 0 40px rgba(255,165,0,.35),0 8px 24px rgba(0,0,0,.4);
  transition:var(--transition);position:relative;overflow:hidden;
}
.start-btn::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,transparent 40%,rgba(255,255,255,.2) 60%,transparent 80%);
  transform:translateX(-100%);transition:transform .4s;
}
.start-btn:hover::before{transform:translateX(100%);}
.start-btn:hover{transform:scale(1.04);box-shadow:0 0 60px rgba(255,165,0,.5),0 12px 32px rgba(0,0,0,.5);}

/* ========================================
   GAME MAIN
   ======================================== */
#gm{display:none;flex-direction:column;min-height:100vh;position:relative;z-index:1;}

/* TOP BAR */
.tbar{
  background:rgba(6,9,26,.92);
  border-bottom:1px solid rgba(255,255,255,.06);
  padding:8px 16px;
  display:flex;align-items:center;justify-content:space-between;
  flex-wrap:wrap;gap:8px;
  backdrop-filter:blur(16px);
  position:sticky;top:0;z-index:100;
}
.tbar-brand{
  font-family:'Black Han Sans',sans-serif;font-size:.95rem;
  background:linear-gradient(135deg,var(--gold),var(--orange));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.tbar-center{display:flex;gap:8px;align-items:center;flex-wrap:wrap;}
.turn-display{
  background:rgba(255,215,0,.08);
  border:1px solid rgba(255,215,0,.2);
  border-radius:8px;padding:4px 12px;
  font-size:.82rem;font-weight:700;color:var(--gold);
  font-family:'Rajdhani',sans-serif;letter-spacing:1px;
  position:relative;overflow:hidden;
}
.turn-display.urgent{
  animation:urgPulse .7s ease-in-out infinite;
  border-color:rgba(255,51,85,.5);color:var(--red);
  background:rgba(255,51,85,.08);
}
@keyframes urgPulse{0%,100%{box-shadow:0 0 0 0 rgba(255,51,85,.3);}50%{box-shadow:0 0 0 5px rgba(255,51,85,.0);}}
.round-badge{
  background:rgba(192,132,252,.08);
  border:1px solid rgba(192,132,252,.2);
  border-radius:8px;padding:4px 10px;
  font-size:.78rem;color:var(--purple);
  font-family:'Rajdhani',sans-serif;font-weight:600;
}
.cur-badge{
  background:rgba(34,211,238,.06);
  border:1px solid rgba(34,211,238,.15);
  border-radius:8px;padding:4px 10px;
  font-size:.78rem;color:var(--cyan);
  font-family:'Rajdhani',sans-serif;font-weight:600;
  max-width:160px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
}

/* MAIN LAYOUT */
.bwrap{
  display:flex;gap:14px;padding:14px;
  align-items:flex-start;justify-content:center;flex-wrap:wrap;
}
#bc{
  background:var(--bg2);
  border:1.5px solid rgba(255,255,255,.07);
  border-radius:16px;
  box-shadow:0 0 0 1px rgba(255,255,255,.03),var(--shadow);
  position:relative;flex-shrink:0;
  cursor:default;
}

/* SIDE PANEL */
.spanel{width:280px;display:flex;flex-direction:column;gap:10px;flex-shrink:0;}

/* PLAYER CARDS */
.pc{
  background:rgba(255,255,255,.03);
  border:1px solid rgba(255,255,255,.06);
  border-radius:var(--r2);padding:12px;
  position:relative;overflow:hidden;
  transition:var(--transition);
}
.pc::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:2px;
  background:linear-gradient(to bottom,transparent,currentColor,transparent);
  opacity:0;transition:opacity .3s;
}
.pc.act{
  border-color:rgba(255,215,0,.25);
  background:rgba(255,215,0,.03);
  box-shadow:0 0 20px rgba(255,215,0,.08),inset 0 0 20px rgba(255,215,0,.02);
}
.pc.act::before{opacity:1;color:var(--gold);}
.pc.bk{opacity:.4;filter:grayscale(.8);pointer-events:none;}
.pch{display:flex;align-items:center;gap:10px;margin-bottom:10px;}
.pcav{
  font-size:1.6rem;width:42px;height:42px;
  display:flex;align-items:center;justify-content:center;
  border-radius:10px;background:rgba(255,255,255,.05);
  border:1px solid rgba(255,255,255,.07);
  position:relative;flex-shrink:0;
}
.pcav .act-ring{
  position:absolute;inset:-2px;border-radius:11px;
  border:2px solid var(--gold);
  animation:actRing 2s ease-in-out infinite;opacity:0;
}
.pc.act .pcav .act-ring{opacity:1;}
@keyframes actRing{0%,100%{opacity:.6;transform:scale(1);}50%{opacity:1;transform:scale(1.05);}}
.pcn{font-weight:700;font-size:.85rem;line-height:1.2;}
.pcbadge{
  font-size:.62rem;padding:1px 6px;border-radius:10px;
  font-family:'Rajdhani',sans-serif;font-weight:600;letter-spacing:.5px;
  display:inline-block;margin-top:2px;
}
.pcbadge.you{background:rgba(34,211,238,.12);color:var(--cyan);border:1px solid rgba(34,211,238,.2);}
.pcbadge.bot{background:rgba(107,127,168,.1);color:var(--text2);border:1px solid rgba(107,127,168,.15);}
.pcloc{font-size:.68rem;color:var(--text2);margin-top:1px;}
.pcc{
  font-size:1.1rem;font-weight:900;color:var(--green);
  font-family:'Orbitron',sans-serif;letter-spacing:-0.5px;
}
.pcnet{font-size:.7rem;color:var(--text2);margin-top:1px;}
.pcstats{display:flex;gap:6px;margin-top:8px;}
.pcstat{
  flex:1;background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.05);
  border-radius:6px;padding:5px 4px;text-align:center;
}
.pcstat .sv{font-size:.8rem;font-weight:700;color:var(--text);}
.pcstat .sl{font-size:.58rem;color:var(--text2);}
.pbar{height:3px;background:rgba(255,255,255,.05);border-radius:2px;overflow:hidden;margin-top:8px;}
.pfill{height:100%;border-radius:2px;transition:width .6s cubic-bezier(.4,0,.2,1);}

/* STOCK TICKER */
.stock-ticker{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(255,255,255,.05);
  border-radius:var(--r2);padding:10px;overflow:hidden;
}
.ticker-label{font-size:.65rem;letter-spacing:3px;color:var(--text3);margin-bottom:7px;font-family:'Rajdhani',sans-serif;}
.ticker-wrap{overflow:hidden;position:relative;}
.ticker-inner{display:flex;gap:10px;animation:tickerScroll 20s linear infinite;}
.ticker-inner:hover{animation-play-state:paused;}
@keyframes tickerScroll{0%{transform:translateX(0);}100%{transform:translateX(-50%);}  }
.tick-item{
  display:flex;align-items:center;gap:5px;white-space:nowrap;
  font-size:.72rem;font-family:'Rajdhani',sans-serif;font-weight:600;
  padding:3px 8px;border-radius:6px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.05);
  flex-shrink:0;
}
.tick-up{color:var(--green);}
.tick-dn{color:var(--red);}

/* DICE AREA */
.dice-panel{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(255,255,255,.06);
  border-radius:var(--r2);padding:14px;text-align:center;
}
.ddisp{display:flex;justify-content:center;gap:12px;margin:10px 0;}
.die{
  width:58px;height:58px;
  background:linear-gradient(135deg,#111827,#1e2d4a);
  border:1.5px solid rgba(255,255,255,.1);
  border-radius:11px;display:flex;align-items:center;justify-content:center;
  font-size:2rem;font-weight:900;
  box-shadow:0 4px 16px rgba(0,0,0,.5),inset 0 1px 0 rgba(255,255,255,.05);
  transition:transform .1s;
  position:relative;overflow:hidden;
}
.die::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,.05) 0%,transparent 60%);
  pointer-events:none;
}
.die.rolling{animation:dieRoll .06s ease-in-out infinite;}
@keyframes dieRoll{0%{transform:rotate(-12deg) scale(.95);}50%{transform:rotate(12deg) scale(1.05);}100%{transform:rotate(-12deg) scale(.95);}}
.die.landed{animation:dieLand .3s cubic-bezier(.3,.7,.4,1.5) forwards;}
@keyframes dieLand{0%{transform:scale(1.2);}100%{transform:scale(1);}}
.die-sum{
  font-family:'Orbitron',sans-serif;font-size:1.5rem;font-weight:900;
  color:var(--gold);margin:4px 0;opacity:0;transition:opacity .3s;
}
.die-sum.show{opacity:1;}
.double-badge{
  display:inline-block;background:linear-gradient(135deg,var(--gold),var(--orange));
  color:#100800;font-weight:900;font-size:.7rem;
  padding:2px 10px;border-radius:20px;margin-left:6px;
  font-family:'Rajdhani',sans-serif;letter-spacing:1px;
  animation:badgePop .4s cubic-bezier(.3,.7,.4,1.5);
}
@keyframes badgePop{0%{transform:scale(0) rotate(-10deg);}100%{transform:scale(1) rotate(0);}}

.roll-btn{
  padding:11px 32px;font-size:.9rem;font-weight:900;
  font-family:'Black Han Sans',sans-serif;letter-spacing:2px;
  background:linear-gradient(135deg,var(--purple2),#7c3aed);
  color:#fff;border:none;border-radius:28px;cursor:pointer;
  box-shadow:0 0 30px rgba(168,85,247,.3),0 4px 16px rgba(0,0,0,.4);
  transition:var(--transition);margin-top:8px;position:relative;overflow:hidden;
}
.roll-btn::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,transparent 30%,rgba(255,255,255,.15) 50%,transparent 70%);
  transform:translateX(-100%);transition:transform .35s;
}
.roll-btn:hover:not(:disabled)::before{transform:translateX(100%);}
.roll-btn:hover:not(:disabled){transform:scale(1.05);box-shadow:0 0 45px rgba(168,85,247,.5),0 8px 24px rgba(0,0,0,.5);}
.roll-btn:disabled{opacity:.35;cursor:not-allowed;transform:none;box-shadow:none;}
.roll-hint{font-size:.72rem;color:var(--text2);margin-top:6px;font-family:'Rajdhani',sans-serif;}

/* PROPERTY LEGEND */
.prop-legend{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(255,255,255,.05);
  border-radius:var(--r2);padding:10px;
}
.legend-title{font-size:.65rem;letter-spacing:3px;color:var(--text3);margin-bottom:8px;font-family:'Rajdhani',sans-serif;}
.legend-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;}
.legend-item{
  display:flex;flex-direction:column;align-items:center;gap:3px;
  padding:6px 4px;border-radius:7px;
  background:rgba(255,255,255,.02);cursor:pointer;
  transition:var(--transition);
}
.legend-item:hover{background:rgba(255,255,255,.05);}
.legend-dot{width:10px;height:10px;border-radius:3px;}
.legend-flag{font-size:.9rem;}
.legend-name{font-size:.6rem;color:var(--text2);}
.legend-own{font-size:.58rem;font-weight:700;}

/* LOG */
.log-panel{
  background:rgba(255,255,255,.02);
  border:1px solid rgba(255,255,255,.05);
  border-radius:var(--r2);padding:10px;
}
.log-title{font-size:.65rem;letter-spacing:3px;color:var(--text3);margin-bottom:7px;font-family:'Rajdhani',sans-serif;}
.lbox{max-height:180px;overflow-y:auto;font-size:.74rem;line-height:1.75;}
.le{
  padding:3px 0;border-bottom:1px solid rgba(255,255,255,.03);
  display:flex;gap:6px;align-items:baseline;
}
.le:last-child{border:none;}
.le-turn{font-size:.6rem;color:var(--text3);font-family:'Rajdhani',sans-serif;flex-shrink:0;}
.le.good{color:var(--green2);}
.le.bad{color:var(--red2);}
.le.sys{color:var(--cyan);}
.le.gold{color:var(--gold);}
.le.purple{color:var(--purple);}

/* ========================================
   PROPERTY POPUP
   ======================================== */
.pov{
  position:fixed;inset:0;background:rgba(0,0,0,.7);
  z-index:300;display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(8px);
}
.pbox{
  background:linear-gradient(160deg,#08102a,#111e3a);
  border:1px solid rgba(255,255,255,.08);
  border-radius:18px;padding:24px;max-width:420px;width:92%;
  box-shadow:var(--shadow);
  animation:popIn .3s cubic-bezier(.3,.7,.4,1.5);
  position:relative;overflow:hidden;
}
.pbox::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.15),transparent);
}
@keyframes popIn{0%{opacity:0;transform:scale(.9) translateY(10px);}100%{opacity:1;transform:scale(1) translateY(0);}}
.ptitle{
  font-family:'Black Han Sans',sans-serif;font-size:1.4rem;margin-bottom:4px;
}
.pctry{
  font-size:.7rem;color:var(--text2);margin-bottom:16px;
  letter-spacing:3px;font-family:'Rajdhani',sans-serif;font-weight:600;
}
.prow{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:8px;font-size:.84rem;
  padding:7px 0;border-bottom:1px solid rgba(255,255,255,.04);
}
.prow:last-child{border:none;}
.prlbl{color:var(--text2);}
.prval{font-weight:700;color:var(--gold);}
.rent-table{
  background:rgba(255,255,255,.03);border-radius:8px;padding:10px;
  margin:10px 0;font-size:.75rem;
}
.rent-row{display:flex;justify-content:space-between;padding:3px 0;}
.rent-row.cur{color:var(--cyan);font-weight:700;}
.pbtns{display:flex;gap:9px;margin-top:18px;}
.pbtn{
  flex:1;padding:12px;border-radius:10px;border:none;
  font-size:.85rem;font-weight:700;cursor:pointer;
  transition:var(--transition);font-family:'Noto Sans KR',sans-serif;
}
.pbtn.buy{
  background:linear-gradient(135deg,var(--green3),#00a854);
  color:#001a0d;
  box-shadow:0 4px 16px rgba(0,201,101,.25);
}
.pbtn.buy:hover{transform:scale(1.02);box-shadow:0 6px 24px rgba(0,201,101,.4);}
.pbtn.buy:disabled{opacity:.35;cursor:not-allowed;transform:none;}
.pbtn.pass{
  background:rgba(255,255,255,.04);color:var(--text2);
  border:1px solid rgba(255,255,255,.08);
}
.pbtn.pass:hover{border-color:var(--red2);color:var(--red2);}

/* ========================================
   EVENT / CHANCE POPUP
   ======================================== */
.event-ov{
  position:fixed;inset:0;background:rgba(0,0,0,.75);
  z-index:320;display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(10px);
}
.event-box{
  background:linear-gradient(160deg,#08102a,#111e3a);
  border:1.5px solid;border-radius:18px;padding:28px;
  max-width:380px;width:90%;text-align:center;
  box-shadow:var(--shadow);
  animation:popIn .35s cubic-bezier(.3,.7,.4,1.5);
}
.event-icon{font-size:3rem;margin-bottom:12px;display:block;animation:iconBounce .5s ease-out;}
@keyframes iconBounce{0%{transform:scale(0) rotate(-20deg);}70%{transform:scale(1.2) rotate(5deg);}100%{transform:scale(1) rotate(0);}}
.event-type{font-size:.68rem;letter-spacing:4px;color:var(--text2);margin-bottom:6px;font-family:'Rajdhani',sans-serif;}
.event-title{font-family:'Black Han Sans',sans-serif;font-size:1.2rem;margin-bottom:8px;}
.event-desc{font-size:.88rem;color:var(--text);line-height:1.6;margin-bottom:6px;}
.event-effect{
  font-family:'Orbitron',sans-serif;font-size:1.3rem;font-weight:700;
  margin:12px 0;padding:10px;border-radius:10px;
  background:rgba(255,255,255,.04);
}
.event-ok{
  margin-top:16px;padding:11px 36px;border-radius:28px;border:none;
  font-weight:700;cursor:pointer;font-size:.9rem;transition:var(--transition);
}
.event-ok:hover{transform:scale(1.04);}

/* ========================================
   MINIGAME
   ======================================== */
#mgo{
  position:fixed;inset:0;z-index:400;
  background:rgba(0,0,0,.88);
  align-items:center;justify-content:center;
  backdrop-filter:blur(10px);
}
.mgbox{
  background:linear-gradient(160deg,#08102a,#0d1a38);
  border:2px solid var(--cyan);border-radius:18px;
  padding:28px;max-width:480px;width:92%;text-align:center;
  box-shadow:0 0 60px rgba(34,211,238,.15),var(--shadow);
  animation:popIn .35s cubic-bezier(.3,.7,.4,1.5);
}
.mgtitle{
  font-family:'Black Han Sans',sans-serif;font-size:1.5rem;
  color:var(--cyan);margin-bottom:6px;
}
.mgdesc{color:var(--text2);font-size:.82rem;margin-bottom:16px;}
.mg-timer-wrap{position:relative;width:70px;height:70px;margin:0 auto 16px;}
.mg-timer-svg{transform:rotate(-90deg);}
.mg-timer-track{fill:none;stroke:rgba(255,255,255,.08);stroke-width:5;}
.mg-timer-prog{fill:none;stroke:var(--cyan);stroke-width:5;stroke-linecap:round;transition:stroke-dashoffset .9s linear,stroke .3s;}
.mg-timer-num{
  position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-family:'Orbitron',sans-serif;font-size:1.2rem;font-weight:700;color:var(--gold);
}
.mgq{font-size:.98rem;font-weight:700;margin-bottom:18px;line-height:1.6;color:var(--text);}
.mgopts{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:14px;}
.mgopt{
  padding:12px;border-radius:10px;
  border:1.5px solid rgba(255,255,255,.07);
  background:rgba(255,255,255,.03);
  color:var(--text);cursor:pointer;
  font-size:.86rem;font-weight:700;
  transition:var(--transition);line-height:1.4;
}
.mgopt:hover{
  border-color:var(--cyan);background:rgba(34,211,238,.06);
  transform:translateY(-2px);
}
.mgopt.ok{border-color:var(--green2);background:rgba(16,217,110,.1);color:var(--green);animation:optPop .3s ease-out;}
.mgopt.no{border-color:var(--red2);background:rgba(255,69,96,.1);color:var(--red2);}
@keyframes optPop{0%{transform:scale(.96);}100%{transform:scale(1);}}
.mg-reward{
  font-family:'Orbitron',sans-serif;font-size:1.1rem;font-weight:700;
  padding:8px;border-radius:8px;display:inline-block;
}

/* ========================================
   MARKET POPUP (새 기능)
   ======================================== */
.market-ov{
  position:fixed;inset:0;background:rgba(0,0,0,.75);
  z-index:310;display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(8px);
}
.market-box{
  background:linear-gradient(160deg,#07102a,#0f1d3a);
  border:1.5px solid rgba(192,132,252,.3);
  border-radius:18px;padding:24px;
  max-width:480px;width:92%;
  box-shadow:0 0 50px rgba(192,132,252,.1),var(--shadow);
  animation:popIn .3s cubic-bezier(.3,.7,.4,1.5);
  max-height:85vh;overflow-y:auto;
}
.market-title{
  font-family:'Black Han Sans',sans-serif;font-size:1.2rem;
  color:var(--purple);margin-bottom:4px;
}
.market-sub{font-size:.72rem;color:var(--text2);margin-bottom:16px;letter-spacing:2px;}
.market-list{display:flex;flex-direction:column;gap:8px;margin-bottom:16px;}
.market-row{
  display:flex;align-items:center;gap:10px;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);
  border-radius:10px;padding:10px 12px;
  transition:var(--transition);
}
.market-row:hover{background:rgba(255,255,255,.05);}
.market-col{width:10px;height:10px;border-radius:3px;flex-shrink:0;}
.market-name{flex:1;font-size:.85rem;font-weight:700;}
.market-info{font-size:.75rem;color:var(--text2);}
.market-price{font-size:.85rem;font-weight:700;color:var(--gold);}
.market-sell{
  padding:6px 14px;border-radius:8px;border:1px solid rgba(255,69,96,.3);
  background:rgba(255,69,96,.06);color:var(--red2);
  cursor:pointer;font-size:.78rem;font-weight:700;
  transition:var(--transition);
}
.market-sell:hover{background:rgba(255,69,96,.15);border-color:var(--red2);}

/* ========================================
   ACHIEVEMENT TOAST
   ======================================== */
.ach-toast{
  position:fixed;top:70px;left:50%;transform:translateX(-50%) translateY(-10px);
  z-index:600;
  background:linear-gradient(135deg,rgba(15,25,50,.97),rgba(20,35,60,.97));
  border:1.5px solid;border-radius:14px;padding:14px 20px;
  display:flex;align-items:center;gap:12px;
  box-shadow:0 0 40px rgba(255,215,0,.2),var(--shadow);
  min-width:280px;max-width:400px;
  animation:achIn .4s cubic-bezier(.3,.7,.4,1.5),achOut .4s 3.5s ease-in forwards;
}
@keyframes achIn{0%{opacity:0;transform:translateX(-50%) translateY(-30px) scale(.9);}100%{opacity:1;transform:translateX(-50%) translateY(0) scale(1);}}
@keyframes achOut{0%{opacity:1;}100%{opacity:0;transform:translateX(-50%) translateY(-20px);}}
.ach-icon{font-size:1.8rem;}
.ach-content{flex:1;}
.ach-label{font-size:.6rem;letter-spacing:3px;color:var(--gold);font-family:'Rajdhani',sans-serif;font-weight:600;}
.ach-name{font-weight:700;font-size:.9rem;}
.ach-desc{font-size:.74rem;color:var(--text2);}

/* ========================================
   RESULT SCREEN
   ======================================== */
#rs{
  position:fixed;inset:0;z-index:500;
  background:var(--bg);
  align-items:center;justify-content:center;flex-direction:column;
  overflow:auto;padding:20px;
}
.rs-backdrop{
  position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse 60% 50% at 50% 0%,rgba(255,215,0,.06) 0%,transparent 60%),
    radial-gradient(ellipse 50% 40% at 20% 100%,rgba(192,132,252,.05) 0%,transparent 60%);
}
.rtitle{
  font-family:'Black Han Sans',sans-serif;
  font-size:clamp(2rem,6vw,3.5rem);
  background:linear-gradient(135deg,var(--gold),var(--orange),var(--red2));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  margin-bottom:8px;text-align:center;
  filter:drop-shadow(0 0 30px rgba(255,215,0,.2));
  animation:titlePop 1s cubic-bezier(.3,.7,.4,1.5);
}
@keyframes titlePop{0%{opacity:0;transform:scale(.8);}100%{opacity:1;transform:scale(1);}}
.rsub{color:var(--text2);font-size:.88rem;margin-bottom:32px;text-align:center;letter-spacing:2px;}
.rcards{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-bottom:32px;}
.rcard{
  background:rgba(255,255,255,.03);
  border:1.5px solid rgba(255,255,255,.07);
  border-radius:16px;padding:20px 22px;text-align:center;
  min-width:155px;
  transition:var(--transition);
  animation:cardIn .5s cubic-bezier(.3,.7,.4,1.5) var(--delay,.1s) both;
}
@keyframes cardIn{0%{opacity:0;transform:translateY(20px);}100%{opacity:1;transform:translateY(0);}}
.rcard.win{
  border-color:rgba(255,215,0,.4);
  background:rgba(255,215,0,.04);
  box-shadow:0 0 40px rgba(255,215,0,.15),inset 0 0 30px rgba(255,215,0,.03);
}
.rrk{font-size:1.8rem;margin-bottom:6px;}
.rn{font-weight:700;font-size:.92rem;margin-bottom:4px;}
.rv{
  color:var(--gold);font-weight:900;font-size:1.1rem;
  font-family:'Orbitron',sans-serif;
}
.rchange{font-size:.75rem;margin-top:3px;}
.rchange.pos{color:var(--green2);}
.rchange.neg{color:var(--red2);}
.rstats-grid{
  display:grid;grid-template-columns:repeat(3,1fr);gap:10px;
  max-width:500px;width:100%;margin-bottom:28px;
}
.rstat{
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.06);
  border-radius:12px;padding:12px;text-align:center;
}
.rstat-v{font-size:1.1rem;font-weight:700;color:var(--cyan);font-family:'Orbitron',sans-serif;}
.rstat-l{font-size:.68rem;color:var(--text2);margin-top:3px;}
.rbtns{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;}
.rrbtn{
  padding:13px 40px;font-size:.9rem;font-weight:900;
  font-family:'Black Han Sans',sans-serif;letter-spacing:2px;
  background:linear-gradient(135deg,var(--gold),var(--gold2));
  color:#1a0a00;border:none;border-radius:38px;
  cursor:pointer;transition:var(--transition);
  box-shadow:0 0 30px rgba(255,165,0,.3);
}
.rrbtn:hover{transform:scale(1.04);box-shadow:0 0 50px rgba(255,165,0,.5);}
.rrbtn.sec{
  background:rgba(255,255,255,.05);color:var(--text);
  border:1.5px solid rgba(255,255,255,.1);
  box-shadow:none;
}
.rrbtn.sec:hover{background:rgba(255,255,255,.08);}

/* ========================================
   TOAST NOTIFICATIONS
   ======================================== */
.twrap{
  position:fixed;top:70px;right:16px;z-index:600;
  display:flex;flex-direction:column;gap:6px;
  pointer-events:none;
}
.toast{
  padding:9px 14px;border-radius:10px;
  font-size:.79rem;font-weight:700;
  background:rgba(10,16,40,.95);
  border:1px solid rgba(255,255,255,.07);
  animation:tIn .28s cubic-bezier(.3,.7,.4,1.5),tOut .28s 2.8s ease-in forwards;
  max-width:240px;line-height:1.4;
  backdrop-filter:blur(8px);
}
@keyframes tIn{0%{opacity:0;transform:translateX(24px);}100%{opacity:1;transform:translateX(0);}}
@keyframes tOut{0%{opacity:1;}100%{opacity:0;transform:translateX(24px);}}

/* ========================================
   MARKET EVENT OVERLAY (경제 이벤트)
   ======================================== */
.mev-bar{
  position:fixed;bottom:0;left:0;right:0;z-index:350;
  background:rgba(6,9,26,.96);border-top:1px solid rgba(255,215,0,.2);
  padding:10px 20px;display:flex;align-items:center;gap:14px;
  backdrop-filter:blur(10px);
  animation:slideUp .4s ease-out;
  flex-wrap:wrap;
}
@keyframes slideUp{0%{transform:translateY(100%);}100%{transform:translateY(0);}}
.mev-icon{font-size:1.5rem;flex-shrink:0;}
.mev-content{flex:1;min-width:0;}
.mev-label{font-size:.62rem;letter-spacing:3px;color:var(--gold);font-family:'Rajdhani',sans-serif;font-weight:600;}
.mev-title{font-weight:700;font-size:.9rem;}
.mev-desc{font-size:.78rem;color:var(--text2);}
.mev-close{
  padding:6px 16px;border-radius:20px;border:1px solid rgba(255,215,0,.3);
  background:rgba(255,215,0,.06);color:var(--gold);
  cursor:pointer;font-size:.78rem;font-weight:700;
  transition:var(--transition);flex-shrink:0;
}
.mev-close:hover{background:rgba(255,215,0,.15);}

/* SCROLLBAR */
::-webkit-scrollbar{width:4px;}
::-webkit-scrollbar-track{background:transparent;}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.1);border-radius:2px;}
::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,.2);}

/* RESPONSIVE */
@media(max-width:700px){
  .cgrid{grid-template-columns:repeat(2,1fr);}
  .bwrap{flex-direction:column;align-items:center;}
  .spanel{width:100%;max-width:500px;}
  #bc{width:min(500px,96vw) !important;height:min(500px,96vw) !important;}
}
</style>
</head>
<body>
<div class="ambient"></div>
<div class="grid-bg"></div>
<div class="scanline"></div>
<div id="particles"></div>
<div id="fw"></div>

<!-- ===== CHARACTER SELECT ===== -->
<div id="cs">
  <div class="cs-logo"><span class="globe">🌍</span></div>
  <div class="cs-title">인베스트 마블 ULTRA</div>
  <div class="cs-sub">INVEST MARBLE · SEASON 1 · ULTRA MAX</div>

  <div class="section-label">▸ 캐릭터 선택</div>
  <div class="cgrid" id="cgrid"></div>

  <div class="section-label">▸ 게임 난이도</div>
  <div class="select-row" id="drow">
    <button class="diff-btn" data-d="easy">🌱 이지 (₩20,000)</button>
    <button class="diff-btn a-normal" data-d="normal">⚔️ 노멀 (₩15,000)</button>
    <button class="diff-btn" data-d="hard">💀 하드 (₩10,000)</button>
  </div>

  <div class="section-label">▸ 최대 턴 수</div>
  <div class="select-row" id="trow">
    <button class="pill-btn" data-t="20">20턴</button>
    <button class="pill-btn a" data-t="30">30턴</button>
    <button class="pill-btn" data-t="40">40턴</button>
    <button class="pill-btn" data-t="50">50턴</button>
  </div>

  <div class="section-label">▸ 경제 이벤트</div>
  <div class="select-row">
    <button class="pill-btn a" id="evtToggle" data-on="1">🌐 경제 이벤트 ON</button>
  </div>

  <button class="start-btn" id="sbtn">🎲 게임 시작</button>
</div>

<!-- ===== GAME MAIN ===== -->
<div id="gm">
  <div class="tbar">
    <span class="tbar-brand">🌍 인베스트 마블 ULTRA</span>
    <div class="tbar-center">
      <div id="tdsp" class="turn-display">🕐 —턴</div>
      <div id="rdsp" class="round-badge">라운드 0</div>
      <div id="cdsp" class="cur-badge">대기 중</div>
    </div>
    <div style="display:flex;gap:7px;">
      <button id="marketBtn" style="padding:5px 12px;border-radius:8px;border:1px solid rgba(192,132,252,.3);background:rgba(192,132,252,.07);color:var(--purple);cursor:pointer;font-size:.75rem;font-weight:700;">📊 자산관리</button>
      <button id="moreBtn" style="padding:5px 12px;border-radius:8px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);color:var(--text2);cursor:pointer;font-size:.75rem;font-weight:700;">⚙️</button>
    </div>
  </div>

  <div class="bwrap">
    <canvas id="bc" width="600" height="600"></canvas>

    <div class="spanel">
      <!-- DICE (상단 고정! 항상 보임) -->
      <div class="dice-panel" style="border-color:rgba(168,85,247,.5);background:rgba(168,85,247,.08);flex-shrink:0;">
        <div style="font-size:.58rem;letter-spacing:3px;color:#b26cf7;font-weight:700;margin-bottom:2px;font-family:'Rajdhani',sans-serif;">🎲 DICE ROLL</div>
        <div class="ddisp" style="margin:6px 0;">
          <div class="die" id="d1" style="border-color:rgba(168,85,247,.4);">🎲</div>
          <div class="die" id="d2" style="border-color:rgba(168,85,247,.4);">🎲</div>
        </div>
        <div class="die-sum" id="dsum">0</div>
        <button class="roll-btn" id="rbtn" disabled>🎲 주사위 굴리기</button>
        <div class="roll-hint" id="dhint"></div>
      </div>

      <!-- STOCK TICKER -->
      <div class="stock-ticker">
        <div class="ticker-label">LIVE MARKET</div>
        <div class="ticker-wrap"><div class="ticker-inner" id="tickerInner"></div></div>
      </div>

      <!-- PLAYER CARDS -->
      <div id="pcards"></div>

      <!-- PROPERTY LEGEND -->
      <div class="prop-legend">
        <div class="legend-title">PROPERTY MAP</div>
        <div class="legend-grid" id="legendGrid"></div>
      </div>

      <!-- LOG -->
      <div class="log-panel">
        <div class="log-title">GAME LOG</div>
        <div class="lbox" id="lbox"></div>
      </div>
    </div>
  </div>
</div>

<!-- ===== PROPERTY POPUP ===== -->
<div class="pov" id="pp2" style="display:none;">
  <div class="pbox">
    <div class="pctry" id="pctry"></div>
    <div class="ptitle" id="ptitle"></div>
    <div id="pinfo"></div>
    <div class="pbtns" id="pbtns"></div>
  </div>
</div>

<!-- ===== EVENT POPUP ===== -->
<div class="event-ov" id="evPop" style="display:none;">
  <div class="event-box" id="evBox">
    <span class="event-icon" id="evIcon"></span>
    <div class="event-type" id="evType"></div>
    <div class="event-title" id="evTitle"></div>
    <div class="event-desc" id="evDesc"></div>
    <div class="event-effect" id="evEffect"></div>
    <button class="event-ok" id="evOk">확인</button>
  </div>
</div>

<!-- ===== MINIGAME ===== -->
<div id="mgo" style="display:none;">
  <div class="mgbox">
    <div class="mgtitle" id="mgt">🎮 미니게임 찬스!</div>
    <div class="mgdesc" id="mgd">정답을 맞혀 보상을 획득하세요</div>
    <div class="mg-timer-wrap">
      <svg class="mg-timer-svg" width="70" height="70" viewBox="0 0 70 70">
        <circle class="mg-timer-track" cx="35" cy="35" r="30"/>
        <circle class="mg-timer-prog" id="mgTimerCirc" cx="35" cy="35" r="30"
          stroke-dasharray="188.5" stroke-dashoffset="0"/>
      </svg>
      <div class="mg-timer-num" id="mgtime">10</div>
    </div>
    <div class="mgq" id="mgq"></div>
    <div class="mgopts" id="mgopts"></div>
    <div class="mg-reward" id="mgReward"></div>
  </div>
</div>

<!-- ===== MARKET PANEL ===== -->
<div class="market-ov" id="marketOv" style="display:none;">
  <div class="market-box">
    <div class="market-title">📊 자산 관리</div>
    <div class="market-sub" id="marketSub"></div>
    <div class="market-list" id="marketList"></div>
    <div style="display:flex;gap:9px;">
      <button class="pbtn pass" style="flex:1;padding:11px;" onclick="closeMarket()">닫기</button>
    </div>
  </div>
</div>

<!-- ===== RESULT ===== -->
<div id="rs" style="display:none;">
  <div class="rs-backdrop"></div>
  <div class="rtitle" id="rtitle">🏆 게임 종료!</div>
  <div class="rsub" id="rsub"></div>
  <div class="rcards" id="rcards"></div>
  <div class="rstats-grid" id="rstats"></div>
  <div class="rbtns">
    <button class="rrbtn" onclick="location.reload()">🔄 다시하기</button>
    <button class="rrbtn sec" onclick="showFinalStats()">📊 상세 통계</button>
  </div>
</div>

<!-- ===== TOAST ===== -->
<div class="twrap" id="twrap"></div>

<script>
// ============================================================
//  CONSTANTS
// ============================================================
const DF=['⚀','⚁','⚂','⚃','⚄','⚅'];
const S=600, CELL=S/11;
const PERIM=40;
const CIRCUMFERENCE=188.5;

const DIFF_CASH={easy:20000,normal:15000,hard:10000};

const CHARS=[
  {name:'이효민',em:'👑',col:'#ffd700',trait:'경제학과 수재',bonus:'건물 할인 15%',bk:'build',
   stats:[90,60,70,80],desc:'건물 투자 특화 마스터'},
  {name:'봇 알파',em:'🤖',col:'#4dabf7',trait:'AI 투자 봇',bonus:'임대료 +12%',bk:'rent',
   stats:[75,85,80,65],desc:'데이터 기반 수익 최적화'},
  {name:'미스터 K',em:'🎩',col:'#c084fc',trait:'연쇄 투자자',bonus:'독점 보너스 2배',bk:'mono',
   stats:[80,70,95,75],desc:'국가 독점 전략 전문가'},
  {name:'탐정 J',em:'🕵️',col:'#22d3ee',trait:'정보 수집가',bonus:'다시 굴리기 +기회',bk:'reroll',
   stats:[70,80,75,90],desc:'찬스 카드 확률 극대화'},
  {name:'재벌 손자',em:'💎',col:'#f472b6',trait:'3세 재벌',bonus:'시작 자금 +₩3000',bk:'rich',
   stats:[85,65,70,85],desc:'초기 자본 우위 전략'},
  {name:'스타트업 K',em:'🚀',col:'#00ff88',trait:'유니콘 CEO',bonus:'출발 통과 +₩100',bk:'pass',
   stats:[65,90,80,70],desc:'패시브 수입 누적 전략'},
  {name:'헤지펀드',em:'📈',col:'#fb923c',trait:'펀드 매니저',bonus:'세금 30% 감면',bk:'tax',
   stats:[75,75,65,95],desc:'세금 최적화 전문가'},
  {name:'소매치기',em:'🦊',col:'#ff3355',trait:'???',bonus:'임대료 통과 10%',bk:'dodge',
   stats:[60,70,85,80],desc:'위기 회피 능력'},
];

const COUNTRIES=[
  {name:'한국',col:'#ff6b6b',flag:'🇰🇷'},
  {name:'일본',col:'#ff9f43',flag:'🇯🇵'},
  {name:'미국',col:'#54a0ff',flag:'🇺🇸'},
  {name:'유럽',col:'#7c4dff',flag:'🇪🇺'},
  {name:'중국',col:'#ee5a24',flag:'🇨🇳'},
  {name:'중동',col:'#01a3a4',flag:'🏜️'},
  {name:'브라질',col:'#10ac84',flag:'🇧🇷'},
  {name:'인도',col:'#f368e0',flag:'🇮🇳'},
];

const RAW_CELLS=[
  {t:'go',name:'🚀 출발',col:'#10d96e'},
  {t:'prop',name:'서울',ctry:0,price:60,rent:[2,10,30,90,160,250],col:'#ff6b6b'},
  {t:'prop',name:'도쿄',ctry:1,price:60,rent:[4,20,60,180,320,450],col:'#ff9f43'},
  {t:'chance',name:'찬스!',col:'#ffd700'},
  {t:'prop',name:'뉴욕',ctry:2,price:100,rent:[6,30,90,270,400,550],col:'#54a0ff'},
  {t:'prop',name:'LA',ctry:2,price:120,rent:[8,40,100,300,450,600],col:'#54a0ff'},
  {t:'airport',name:'서울공항',col:'#22d3ee'},
  {t:'prop',name:'파리',ctry:3,price:140,rent:[10,50,150,450,625,750],col:'#7c4dff'},
  {t:'tax',name:'소득세',amt:200,col:'#ff4560'},
  {t:'prop',name:'런던',ctry:3,price:160,rent:[12,60,180,500,700,900],col:'#7c4dff'},
  {t:'island',name:'🏝️ 무인도',col:'#ff8c42'},
  {t:'prop',name:'베이징',ctry:4,price:180,rent:[14,70,200,550,750,950],col:'#ee5a24'},
  {t:'community',name:'공동체기금',col:'#10ac84'},
  {t:'prop',name:'상하이',ctry:4,price:200,rent:[16,80,220,600,800,1000],col:'#ee5a24'},
  {t:'tax',name:'사치세',amt:100,col:'#ff4560'},
  {t:'airport',name:'도쿄공항',col:'#22d3ee'},
  {t:'prop',name:'두바이',ctry:5,price:220,rent:[18,90,250,700,875,1050],col:'#01a3a4'},
  {t:'chance',name:'찬스!',col:'#ffd700'},
  {t:'prop',name:'아부다비',ctry:5,price:240,rent:[20,100,300,750,925,1100],col:'#01a3a4'},
  {t:'prop',name:'리우',ctry:6,price:260,rent:[22,110,330,800,975,1150],col:'#10ac84'},
  {t:'golden',name:'✨황금시대',col:'#ffd700'},
  {t:'prop',name:'상파울루',ctry:6,price:260,rent:[22,110,330,800,975,1150],col:'#10ac84'},
  {t:'prop',name:'뭄바이',ctry:7,price:280,rent:[24,120,360,850,1025,1200],col:'#f368e0'},
  {t:'community',name:'공동체기금',col:'#10ac84'},
  {t:'prop',name:'델리',ctry:7,price:280,rent:[24,120,360,850,1025,1200],col:'#f368e0'},
  {t:'airport',name:'파리공항',col:'#22d3ee'},
  {t:'chance',name:'찬스!',col:'#ffd700'},
  {t:'prop',name:'모스크바',ctry:0,price:300,rent:[26,130,390,900,1100,1275],col:'#ff6b6b'},
  {t:'prop',name:'성수동',ctry:0,price:320,rent:[28,150,450,1000,1200,1400],col:'#ff6b6b'},
  {t:'tax',name:'법인세',amt:150,col:'#ff4560'},
  {t:'taxhub',name:'💼세금징수소',col:'#ff4560'},
  {t:'prop',name:'홍대',ctry:1,price:350,rent:[35,175,500,1100,1300,1500],col:'#ff9f43'},
  {t:'airport',name:'뉴욕공항',col:'#22d3ee'},
  {t:'prop',name:'강남',ctry:1,price:400,rent:[50,200,600,1400,1700,2000],col:'#ff9f43'},
  {t:'prop',name:'청담',ctry:2,price:350,rent:[35,175,500,1100,1300,1500],col:'#54a0ff'},
  {t:'chance',name:'찬스!',col:'#ffd700'},
  {t:'prop',name:'마카오',ctry:3,price:300,rent:[26,130,390,900,1100,1275],col:'#7c4dff'},
  {t:'prop',name:'싱가포르',ctry:3,price:320,rent:[28,150,450,1000,1200,1400],col:'#7c4dff'},
  {t:'community',name:'공동체기금',col:'#10ac84'},
  {t:'prop',name:'방콕',ctry:4,price:280,rent:[24,120,360,850,1025,1200],col:'#ee5a24'},
];

// ── CHANCE CARDS ──
const CHANCE=[
  {txt:'📈 주식 대박!',desc:'오늘 시장 급등 +20%',fx:p=>{const a=400+Math.floor(Math.random()*500);p.cash+=a;return'+₩'+a;},col:'#00ff88'},
  {txt:'🎁 경품 당첨!',desc:'연말 황금 추첨 1등',fx:p=>{p.cash+=1500;return'+₩1,500';},col:'#ffd700'},
  {txt:'💰 배당금 수령',desc:'전 플레이어에게 배당 징수',fx:(p,ps)=>{let t=0;ps.forEach(o=>{if(o!==p&&o.cash>0){const a=Math.min(o.cash,300);o.cash-=a;p.cash+=a;t+=a;}});return'+₩'+t;},col:'#00ff88'},
  {txt:'🏛️ 정부 지원금',desc:'소상공인 특별 지원',fx:p=>{p.cash+=500;return'+₩500';},col:'#ffd700'},
  {txt:'🎰 즉석복권',desc:'오늘 운이 따른다면...',fx:p=>{const r=Math.random();const a=r<.1?2000:r<.35?800:r<.7?200:-150;p.cash+=a;return(a>=0?'+':'')+a;},col:'#c084fc'},
  {txt:'💸 과태료',desc:'신호위반 + 주정차 위반',fx:p=>{p.cash-=350;return'-₩350';},col:'#ff3355'},
  {txt:'🚀 출발로 이동!',desc:'빠른 귀환 + 통과 보너스',fx:p=>{p.pos=0;p.cash+=300;return'+₩300 이동';},col:'#ffd700'},
  {txt:'🔙 3칸 후진',desc:'갑작스러운 방향 전환',fx:p=>{p.pos=(p.pos-3+40)%40;return'3칸 ↩';},col:'#ff8c42'},
  {txt:'🎲 한 번 더!',desc:'연속 기회 발동!',fx:p=>{p._ex=true;return'추가 턴!';},col:'#22d3ee'},
  {txt:'💼 미니게임 찬스',desc:'퀴즈를 맞히면 큰 보상',fx:p=>{p._mg=true;return'도전!';},col:'#22d3ee'},
  {txt:'🏦 건물 수익 보너스',desc:'모든 건물에서 즉시 수익',fx:(p,_,cells)=>{let b=0;cells.forEach(c=>{if(c.own===p.id&&c.t==='prop'){b+=80*((c.hs||0)*1+(c.ho?5:0));}});p.cash+=b;return'+₩'+b;},col:'#ffd700'},
  {txt:'✈️ 최근 공항으로',desc:'비즈니스 클래스 이동',fx:(p,_,cells)=>{const a=[6,15,25,32];let n=a[0],md=99;a.forEach(i=>{const d=(i-p.pos+40)%40;if(d>0&&d<md){md=d;n=i;}});p.pos=n;return'공항 이동';},col:'#22d3ee'},
  {txt:'🌊 시장 폭락',desc:'글로벌 경기침체! 자산 손실',fx:p=>{const a=Math.floor(p.cash*0.18);p.cash-=a;return'-₩'+a;},col:'#ff3355'},
  {txt:'💡 특허 수익',desc:'혁신 아이디어 로열티',fx:p=>{p.cash+=800;return'+₩800';},col:'#ffd700'},
  {txt:'🤝 기업 합병',desc:'경쟁사 인수로 현금 확보',fx:p=>{const a=600+Math.floor(Math.random()*400);p.cash+=a;return'+₩'+a;},col:'#00ff88'},
  {txt:'🏗️ 재개발 보상',desc:'도시 재개발 구역 보상금',fx:p=>{p.cash+=700;return'+₩700';},col:'#ffd700'},
  {txt:'🎪 이벤트 수익',desc:'지역 축제 스폰서십',fx:p=>{p.cash+=450;return'+₩450';},col:'#c084fc'},
  {txt:'⚡ 전략적 이동',desc:'5칸 앞으로 전진!',fx:p=>{p.pos=(p.pos+5)%40;return'5칸 ↗';},col:'#22d3ee'},
];

// ── COMMUNITY CARDS ──
const COMMUNITY=[
  {txt:'🏥 의료비 납부',desc:'종합 건강검진 비용',fx:p=>{p.cash-=450;return'-₩450';},col:'#ff3355'},
  {txt:'🎓 장학금 수령',desc:'우수 장학생 선발',fx:p=>{p.cash+=700;return'+₩700';},col:'#00ff88'},
  {txt:'🏠 임대수익 공유',desc:'커뮤니티 임대수익 배분',fx:(p,ps)=>{let t=0;ps.forEach(o=>{if(o!==p&&o.cash>0){const a=Math.min(o.cash,200);o.cash-=a;p.cash+=a;t+=a;}});return'+₩'+t;},col:'#00ff88'},
  {txt:'💸 수리비 청구',desc:'건물 유지보수 비용',fx:(p,_,cells)=>{let c=0;cells.forEach(cl=>{if(cl.own===p.id)c+=cl.hs*90+cl.ho*220;});p.cash-=c;return'-₩'+c;},col:'#ff3355'},
  {txt:'🎉 생일 축하!',desc:'모두에게 축하금 받기',fx:p=>{p.cash+=400;return'+₩400';},col:'#ffd700'},
  {txt:'📉 주가 폭락',desc:'보유 자산 일부 손실',fx:p=>{const a=Math.floor(p.cash*0.18);p.cash-=a;return'-₩'+a;},col:'#ff3355'},
  {txt:'🏆 우수 시민상',desc:'지역사회 공헌 수상',fx:p=>{p.cash+=900;return'+₩900';},col:'#ffd700'},
  {txt:'🔧 긴급 수선',desc:'배관 파손으로 긴급 수리',fx:p=>{p.cash-=120;return'-₩120';},col:'#ff8c42'},
  {txt:'🌱 ESG 보조금',desc:'친환경 기업 인증',fx:p=>{p.cash+=400;return'+₩400';},col:'#00ff88'},
  {txt:'💰 로또 1등',desc:'기적은 일어난다!',fx:p=>{const ok=Math.random()<.1;const a=ok?2500:0;p.cash+=a;return ok?'+₩2,500 🎊🎊':'아쉽게 꽝...';},col:'#c084fc'},
  {txt:'🤑 배당 재투자',desc:'주식 배당금 복리 수령',fx:p=>{p.cash+=550;return'+₩550';},col:'#00ff88'},
  {txt:'🌐 글로벌 수출',desc:'해외 수출 계약 성사',fx:p=>{p.cash+=650;return'+₩650';},col:'#ffd700'},
  {txt:'🏋️ 자기계발',desc:'역량 개발로 임금 상승',fx:p=>{p.cash+=300;return'+₩300';},col:'#00ff88'},
  {txt:'💔 이혼 소송',desc:'합의금 지급 (당하는 쪽)',fx:p=>{const a=Math.floor(p.cash*0.12);p.cash-=a;return'-₩'+a;},col:'#ff3355'},
];

// ── MINIGAME QUESTIONS ──
const MG=[
  {q:'한국의 수도는?',o:['서울','부산','인천','광주'],a:0,reward:800},
  {q:'세계에서 인구가 가장 많은 나라는?',o:['중국','인도','미국','인도네시아'],a:1,reward:900},
  {q:'가장 큰 대륙은?',o:['아시아','아프리카','유럽','남미'],a:0,reward:700},
  {q:'비트코인 최초 발행 연도는?',o:['2005','2007','2009','2011'],a:2,reward:1000},
  {q:'GDP가 가장 높은 나라는?',o:['중국','미국','일본','독일'],a:1,reward:900},
  {q:'달에 처음 착륙한 우주선은?',o:['아폴로 11','아폴로 13','아르테미스','보스토크'],a:0,reward:800},
  {q:'지구에서 가장 긴 강은?',o:['아마존','나일','양쯔강','미시시피'],a:1,reward:800},
  {q:'세계 최초 스마트폰 출시 회사는?',o:['삼성','애플','IBM','소니'],a:1,reward:1000},
  {q:'블록체인 기술을 처음 적용한 것은?',o:['이더리움','비트코인','리플','도지코인'],a:1,reward:1000},
  {q:'세계 최대 전자상거래 기업은?',o:['알리바바','아마존','이베이','쿠팡'],a:1,reward:900},
  {q:'주식시장에서 PER란?',o:['주가/순이익','매출/순이익','자산/부채','시총/매출'],a:0,reward:1100},
  {q:'인플레이션이란?',o:['물가 하락','물가 상승','금리 인상','통화 감소'],a:1,reward:800},
  {q:'세계 금융의 중심지는?',o:['런던','도쿄','뉴욕','상하이'],a:2,reward:900},
  {q:'KOSPI는 어느 나라 주가지수?',o:['일본','중국','한국','미국'],a:2,reward:700},
  {q:'FED(연준)의 역할은?',o:['재정정책','통화정책','무역정책','환경정책'],a:1,reward:1000},
];

// ── GLOBAL ECONOMIC EVENTS ──
const ECO_EVENTS=[
  {icon:'📉',type:'위기',title:'글로벌 금융위기',desc:'전 세계 부동산 임대료 20% 감소',fx:(cells,players)=>{cells.forEach(c=>{if(c.t==='prop')c._rentMod=(c._rentMod||1)*.8;});},dur:3,col:'#ff3355',border:'rgba(255,51,85,.4)'},
  {icon:'📈',type:'호황',title:'글로벌 경제 대호황',desc:'모든 임대료 25% 상승!',fx:(cells)=>{cells.forEach(c=>{if(c.t==='prop')c._rentMod=(c._rentMod||1)*1.25;});},dur:4,col:'#00ff88',border:'rgba(0,255,136,.4)'},
  {icon:'🏛️',type:'정책',title:'중앙은행 금리 인상',desc:'건물 건설 비용 20% 상승',fx:(_,__,G)=>{G._buildCostMod=1.2;},dur:3,col:'#fb923c',border:'rgba(251,146,60,.4)'},
  {icon:'🌪️',type:'재해',title:'자연재해 발생',desc:'무작위 플레이어 건물 손실',fx:(_,players,G)=>{const alive=players.filter(p=>!p.bkrt);if(alive.length>0){const t=alive[Math.floor(Math.random()*alive.length)];const props=G.cells.filter(c=>c.own===t.id&&c.t==='prop'&&(c.hs>0||c.ho));if(props.length>0){const p=props[Math.floor(Math.random()*props.length)];if(p.ho){p.ho=0;}else{p.hs=Math.max(0,p.hs-1);}}}},dur:1,col:'#ff3355',border:'rgba(255,51,85,.4)'},
  {icon:'🚀',type:'혁신',title:'AI 기술 혁신 붐',desc:'모든 플레이어 ₩500 획득',fx:(_,players)=>{players.forEach(p=>{if(!p.bkrt)p.cash+=500;});},dur:1,col:'#ffd700',border:'rgba(255,215,0,.4)'},
  {icon:'🌐',type:'무역',title:'자유무역 협정 체결',desc:'공항 임대료 3배 폭등!',fx:(cells)=>{cells.forEach(c=>{if(c.t==='airport')c._airportMod=3;});},dur:4,col:'#22d3ee',border:'rgba(34,211,238,.4)'},
  {icon:'💹',type:'투자',title:'외국인 직접투자 급증',desc:'무인도 탈출 무료 + ₩200',fx:(_,__,G)=>{G._islandFree=true;},dur:3,col:'#c084fc',border:'rgba(192,132,252,.4)'},
  {icon:'💰',type:'보너스',title:'국가 배당금 지급',desc:'부동산 소유자 1인당 ₩300',fx:(cells,players)=>{const owners=new Set();cells.forEach(c=>{if(c.t==='prop'&&c.own>=0)owners.add(c.own);});players.forEach(p=>{if(owners.has(p.id))p.cash+=300;});},dur:1,col:'#ffd700',border:'rgba(255,215,0,.4)'},
  {icon:'🔥',type:'버블',title:'부동산 버블 붕괴',desc:'전체 임대료 30% 감소!',fx:(cells)=>{cells.forEach(c=>{if(c.t==='prop')c._rentMod=(c._rentMod||1)*.7;});},dur:2,col:'#ff6b35',border:'rgba(255,107,53,.4)'},
  {icon:'💎',type:'황금기',title:'경제 황금기 도래',desc:'임대료 50% 증가 & 배당금!',fx:(cells,players)=>{cells.forEach(c=>{if(c.t==='prop')c._rentMod=(c._rentMod||1)*1.5;});players.forEach(p=>{if(!p.bkrt)p.cash+=200;});},dur:3,col:'#ffd700',border:'rgba(255,215,0,.6)'},
  {icon:'🛢️',type:'에너지',title:'에너지 대란 발생',desc:'세금 2배 & 임대료 감소',fx:(_,__,G)=>{G._taxMod=2;},dur:2,col:'#ff3355',border:'rgba(255,51,85,.4)'},
  {icon:'🌊',type:'정치',title:'경제 제재 발동',desc:'해외 자산 임대료 40% 감소',fx:(cells)=>{['JP','US','EU','CN','BR','IN'].forEach(ctry=>{cells.forEach(c=>{if(c.t==='prop'&&c.ctry===ctry)c._rentMod=(c._rentMod||1)*.6;});});},dur:2,col:'#ff3355',border:'rgba(255,51,85,.4)'},
];

// ── ACHIEVEMENTS ──
const ACHIEVEMENTS=[
  {id:'firstBuy',icon:'🏠',name:'첫 부동산',desc:'첫 번째 부동산을 구매했습니다',check:(_,G)=>G.cells.some(c=>c.own===0&&c.t==='prop')},
  {id:'monopoly',icon:'🌟',name:'독점왕',desc:'한 국가를 완전 독점했습니다',check:(_,G)=>COUNTRIES.some((_,ci)=>mono(0,ci,G))},
  {id:'hotel',icon:'🏨',name:'호텔리어',desc:'첫 번째 호텔을 건설했습니다',check:(_,G)=>G.cells.some(c=>c.own===0&&c.ho>0)},
  {id:'rich10k',icon:'💰',name:'1억 클럽',desc:'순자산 ₩10,000 달성',check:(p)=>nw(p)>=10000},
  {id:'rich20k',icon:'💎',name:'재벌',desc:'순자산 ₩20,000 달성',check:(p)=>nw(p)>=20000},
  {id:'rich50k',icon:'👑',name:'억만장자',desc:'순자산 ₩50,000 달성',check:(p)=>nw(p)>=50000},
  {id:'airportKing',icon:'✈️',name:'항공왕',desc:'공항 3개 이상 보유',check:(_,G)=>G.cells.filter(c=>c.own===0&&c.t==='airport').length>=3},
  {id:'mgWin',icon:'🎓',name:'퀴즈왕',desc:'미니게임에서 승리했습니다',check:(p)=>p._mgWins>0},
  {id:'survivor',icon:'🛡️',name:'생존왕',desc:'파산 위기에서 살아남았습니다',check:(p)=>p._survived>0},
  {id:'landlord',icon:'🏙️',name:'건물주',desc:'5개 이상 부동산 보유',check:(_,G)=>G.cells.filter(c=>c.own===0&&c.t==='prop').length>=5},
];

// ============================================================
//  GAME STATE
// ============================================================
let G={
  phase:'s',players:[],cur:0,round:1,
  maxT:30,tot:0,cells:[],
  ecoEvent:null,ecoTurns:0,
  _buildCostMod:1,_islandFree:false,
  eventsEnabled:true,
  diff:'normal',
  charIdx:0,
  gameStats:{totalRent:0,totalTax:0,totalChance:0,doublesRolled:0},
};

let unlockedAch=new Set();

function initCells(){
  G.cells=RAW_CELLS.map((c,i)=>({...c,idx:i,own:-1,hs:0,ho:0,_rentMod:1,_airportMod:1}));
}

// ============================================================
//  PARTICLES
// ============================================================
function initParticles(){
  const container=document.getElementById('particles');
  for(let i=0;i<18;i++){
    const p=document.createElement('div');p.className='pt';
    p.style.left=Math.random()*100+'%';
    p.style.top=Math.random()*100+'%';
    const cols=['rgba(255,215,0,.3)','rgba(34,211,238,.2)','rgba(192,132,252,.2)','rgba(0,255,136,.2)'];
    p.style.background=cols[Math.floor(Math.random()*cols.length)];
    p.style.setProperty('--dur',(6+Math.random()*8)+'s');
    p.style.setProperty('--delay',(-Math.random()*8)+'s');
    p.style.setProperty('--tx',(Math.random()*60-30)+'px');
    p.style.setProperty('--ty',(-40-Math.random()*60)+'px');
    container.appendChild(p);
  }
}

// ============================================================
//  TICKER
// ============================================================
function updateTicker(){
  const items=COUNTRIES.map(c=>{
    const chg=(Math.random()*8-3).toFixed(1);
    const up=parseFloat(chg)>=0;
    return `<div class="tick-item ${up?'tick-up':'tick-dn'}">${c.flag} ${c.name} <span>${up?'▲':'▼'}${Math.abs(chg)}%</span></div>`;
  });
  const doubled=[...items,...items];
  document.getElementById('tickerInner').innerHTML=doubled.join('');
}

// ============================================================
//  START GAME
// ============================================================
function startGame(ci,mt,diff){
  initCells();
  G.maxT=mt;G.tot=0;G.round=1;G.cur=0;
  G.diff=diff;G.charIdx=ci;
  G._buildCostMod=1;G._islandFree=false;
  G.ecoEvent=null;G.ecoTurns=0;
  G.gameStats={totalRent:0,totalTax:0,totalChance:0,doublesRolled:0};
  unlockedAch=new Set();

  const startCash=DIFF_CASH[diff]||15000;
  const pc=CHARS[ci];
  const botPool=CHARS.filter((_,i)=>i!==ci);
  const bots=botPool.slice(0,3);

  // 캐릭터 보너스 적용
  let pCash=startCash;
  if(pc.bk==='rich')pCash+=3000;

  G.players=[
    {id:0,name:pc.name,em:pc.em,col:pc.col,bk:pc.bk,isBot:false,
     cash:pCash,pos:0,bkrt:false,jl:false,jt:0,
     _ex:false,_mg:false,_mgWins:0,_survived:0,
     initCash:pCash,totalEarned:0,totalLost:0},
    ...bots.map((c,i)=>({
      id:i+1,name:c.name,em:c.em,col:c.col,bk:c.bk,isBot:true,
      cash:startCash,pos:0,bkrt:false,jl:false,jt:0,
      _ex:false,_mg:false,_mgWins:0,_survived:0,
      initCash:startCash,totalEarned:0,totalLost:0,
    }))
  ];

  document.getElementById('cs').style.display='none';
  document.getElementById('gm').style.display='flex';
  document.getElementById('rs').style.display='none';
  document.getElementById('mgo').style.display='none';

  updateTicker();
  setInterval(updateTicker,15000);
  renderLegend();
  renderPCards();
  drawBoard();
  startTurn();
}

// ============================================================
//  CANVAS DRAWING
// ============================================================
const cv=document.getElementById('bc');
const ctx=cv.getContext('2d');

function cellXY(i){
  if(i<=10)return{x:i*CELL,y:S-CELL,w:CELL,h:CELL};
  if(i<=20)return{x:S-CELL,y:S-CELL-(i-10)*CELL,w:CELL,h:CELL};
  if(i<=30)return{x:S-CELL-(i-20)*CELL,y:0,w:CELL,h:CELL};
  return{x:0,y:(i-30)*CELL,w:CELL,h:CELL};
}

function rrRect(x,y,w,h,r){
  ctx.beginPath();
  ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);
  ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);
  ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);
  ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);
  ctx.closePath();
}

function wrapText(text,x,y,mw,lh){
  const chars=[...text];let line='';const lines=[];
  chars.forEach(c=>{
    const test=line+c;
    if(ctx.measureText(test).width>mw&&line){lines.push(line);line=c;}else line=test;
  });
  if(line)lines.push(line);
  const sy=y-(lines.length-1)*lh/2;
  lines.forEach((s,i)=>ctx.fillText(s,x,sy+i*lh));
}

function drawBoard(trail=[],tcol='rgba(255,215,0,0.4)'){
  ctx.clearRect(0,0,S,S);

  // ── 배경: 다층 그라디언트 ──
  const bg=ctx.createLinearGradient(0,0,S,S);
  bg.addColorStop(0,'#04060f');bg.addColorStop(0.5,'#070d1e');bg.addColorStop(1,'#04060f');
  ctx.fillStyle=bg;ctx.fillRect(0,0,S,S);

  // ── 코너 빛 효과 ──
  [0,S].forEach(cx=>[0,S].forEach(cy=>{
    const rg=ctx.createRadialGradient(cx,cy,0,cx,cy,CELL*1.6);
    rg.addColorStop(0,'rgba(255,215,0,0.06)');rg.addColorStop(1,'transparent');
    ctx.fillStyle=rg;ctx.fillRect(0,0,S,S);
  }));

  // ── 내부 영역 ──
  const ig=ctx.createRadialGradient(S/2,S/2,0,S/2,S/2,S*.48);
  ig.addColorStop(0,'#0d1930');ig.addColorStop(1,'#06091a');
  ctx.fillStyle=ig;
  rrRect(ctx,CELL,CELL,S-CELL*2,S-CELL*2,14);ctx.fill();

  // ── 내부 테두리 글로우 ──
  ctx.save();ctx.shadowBlur=18;ctx.shadowColor='rgba(255,215,0,0.12)';
  ctx.strokeStyle='rgba(255,215,0,0.1)';ctx.lineWidth=1.5;
  rrRect(ctx,CELL,CELL,S-CELL*2,S-CELL*2,14);ctx.stroke();
  ctx.restore();

  // ── 세계지도 격자 무늬 ──
  ctx.save();ctx.globalAlpha=0.025;ctx.strokeStyle='#4dabf7';ctx.lineWidth=0.5;
  for(let i=1;i<8;i++){
    ctx.beginPath();ctx.moveTo(CELL+i*(S-2*CELL)/8,CELL);ctx.lineTo(CELL+i*(S-2*CELL)/8,S-CELL);ctx.stroke();
    ctx.beginPath();ctx.moveTo(CELL,CELL+i*(S-2*CELL)/8);ctx.lineTo(S-CELL,CELL+i*(S-2*CELL)/8);ctx.stroke();
  }
  ctx.restore();

  // ── 중앙 글로브 장식 ──
  ctx.save();
  // 글로브 외곽선들
  [60,90,118,145].forEach((r,i)=>{
    ctx.globalAlpha=0.04+i*0.01;
    ctx.strokeStyle='#ffd700';ctx.lineWidth=1;
    ctx.beginPath();ctx.arc(S/2,S/2,r,0,Math.PI*2);ctx.stroke();
  });
  // 글로브 경선 (대각선)
  ctx.globalAlpha=0.04;
  for(let a=0;a<Math.PI;a+=Math.PI/5){
    ctx.beginPath();ctx.ellipse(S/2,S/2,145,60,a,0,Math.PI*2);ctx.stroke();
  }
  ctx.restore();

  // ── 중앙 텍스트 ──
  ctx.textAlign='center';
  ctx.font=`bold ${CELL*.36}px "Black Han Sans"`;
  ctx.fillStyle='rgba(255,215,0,0.18)';
  ctx.fillText('인베스트',S/2,S/2-8);
  ctx.fillText('마블',S/2,S/2+CELL*.32);
  ctx.font=`700 ${CELL*.15}px "Orbitron"`;
  ctx.fillStyle='rgba(34,211,238,0.15)';
  ctx.fillText('ULTRA',S/2,S/2+CELL*.52);
  ctx.font=`${CELL*.14}px "Rajdhani"`;
  ctx.fillStyle='rgba(178,108,247,0.2)';
  ctx.fillText('⏳ '+(G.maxT-G.tot)+'턴 남음',S/2,S/2+CELL*.7);

  // ── 경제 이벤트 표시 ──
  if(G.ecoEvent){
    ctx.save();
    ctx.shadowBlur=30;ctx.shadowColor='rgba(255,215,0,0.4)';
    ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText(G.ecoEvent.icon,S/2,S/2-CELL*.52);
    ctx.shadowBlur=0;
    ctx.font=`bold ${CELL*.13}px "Noto Sans KR"`;
    ctx.fillStyle='rgba(255,215,0,0.28)';ctx.fillText(G.ecoEvent.title,S/2,S/2-CELL*.3);
    ctx.restore();
  }

  G.cells.forEach((c,i)=>{
    const{x,y,w,h}=cellXY(i);
    const isT=trail.includes(i);

    // Trail glow
    if(isT){
      ctx.save();ctx.shadowBlur=20;ctx.shadowColor=tcol;
      ctx.fillStyle=tcol.replace('0.4','0.1');
      rrRect(ctx,x,y,w,h,4);ctx.fill();
      ctx.restore();
    }

    // Cell bg
    let bg='#090f20';
    if(c.t==='go')bg='#001a10';
    else if(c.t==='island')bg='#1a0d00';
    else if(c.t==='golden')bg='#130f00';
    else if(c.t==='taxhub'||c.t==='tax')bg='#120505';
    else if(c.t==='chance')bg='#121000';
    else if(c.t==='community')bg='#001512';
    else if(c.t==='airport')bg='#001220';

    ctx.fillStyle=bg;rrRect(ctx,x+1,y+1,w-2,h-2,3);ctx.fill();

    // Border
    let bc='rgba(255,255,255,.04)';
    if(c.t==='prop'&&c.own>=0){
      const oc=G.players[c.own]?.col||'#fff';
      bc=oc+'66';
      // Owned glow
      ctx.save();ctx.shadowBlur=6;ctx.shadowColor=oc+'44';
      ctx.strokeStyle=oc+'55';ctx.lineWidth=1.5;
      rrRect(ctx,x+1,y+1,w-2,h-2,3);ctx.stroke();
      ctx.restore();
    } else {
      ctx.strokeStyle=bc;ctx.lineWidth=1;
      rrRect(ctx,x+1,y+1,w-2,h-2,3);ctx.stroke();
    }

    // Color stripe
    if(c.t==='prop'&&c.col){
      const sg=ctx.createLinearGradient(x,y+2,x+w,y+6);
      sg.addColorStop(0,c.col+'00');sg.addColorStop(.3,c.col);
      sg.addColorStop(.7,c.col);sg.addColorStop(1,c.col+'00');
      ctx.fillStyle=sg;ctx.fillRect(x+2,y+2,w-4,4);
    }

    // Content
    const mx=x+w/2,my=y+h/2;
    ctx.textAlign='center';

    if(c.t==='go'){
      ctx.font=`${CELL*.28}px sans-serif`;ctx.fillText('🚀',mx,my-4);
      ctx.font=`bold ${CELL*.16}px "Noto Sans KR"`;
      ctx.fillStyle='#10d96e';ctx.fillText('출발',mx,my+CELL*.22);
    } else if(c.t==='island'){
      ctx.font=`${CELL*.28}px sans-serif`;ctx.fillText('🏝️',mx,my-4);
      ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ff8c42';
      ctx.fillText('무인도',mx,my+CELL*.22);
    } else if(c.t==='golden'){
      ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText('✨',mx,my-3);
      ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ffd700';
      ctx.fillText('황금시대',mx,my+CELL*.22);
    } else if(c.t==='taxhub'){
      ctx.font=`${CELL*.24}px sans-serif`;ctx.fillText('💼',mx,my-3);
      ctx.font=`${CELL*.11}px "Noto Sans KR"`;ctx.fillStyle='#ff4560';
      ctx.fillText('세금징수소',mx,my+CELL*.2);
    } else if(c.t==='chance'){
      ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText('🎲',mx,my-3);
      ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ffd700';
      ctx.fillText('찬스!',mx,my+CELL*.22);
    } else if(c.t==='community'){
      ctx.font=`${CELL*.24}px sans-serif`;ctx.fillText('🏦',mx,my-3);
      ctx.font=`${CELL*.11}px "Noto Sans KR"`;ctx.fillStyle='#10ac84';
      ctx.fillText('공동체기금',mx,my+CELL*.2);
    } else if(c.t==='airport'){
      ctx.font=`${CELL*.24}px sans-serif`;ctx.fillText('✈️',mx,my-3);
      ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#22d3ee';
      ctx.fillText(c.name.replace('공항',''),mx,my+CELL*.18);
      ctx.font=`${CELL*.1}px "Noto Sans KR"`;ctx.fillStyle='#22d3ee88';
      ctx.fillText('공항',mx,my+CELL*.3);
    } else if(c.t==='tax'){
      ctx.font=`${CELL*.22}px sans-serif`;ctx.fillText('💸',mx,my-4);
      ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#ff4560';
      ctx.fillText(c.name,mx,my+CELL*.16);
      ctx.font=`${CELL*.12}px "Orbitron"`;ctx.fillStyle='#ff456077';
      ctx.fillText('₩'+c.amt,mx,my+CELL*.3);
    } else if(c.t==='prop'){
      ctx.font=`${CELL*.145}px "Noto Sans KR"`;
      ctx.fillStyle=c.own>=0?'rgba(255,255,255,.95)':'rgba(255,255,255,.7)';
      wrapText(c.name,mx,my-5,w-6,CELL*.16);

      // Buildings
      if(c.ho>0){
        ctx.font=`${CELL*.22}px sans-serif`;ctx.fillText('🏨',mx,my+CELL*.18);
      } else if((c.hs||0)>0){
        const icons='🏠'.repeat(Math.min(c.hs,4));
        ctx.font=`${CELL*.15}px sans-serif`;ctx.fillText(icons,mx,my+CELL*.22);
      }

      // Price
      ctx.font=`600 ${CELL*.12}px "Rajdhani"`;
      ctx.fillStyle='rgba(255,215,0,.5)';
      ctx.fillText('₩'+c.price,mx,my+CELL*.38);

      // Owner dot
      if(c.own>=0){
        const oc=G.players[c.own]?.col||'#fff';
        ctx.save();ctx.shadowBlur=6;ctx.shadowColor=oc;
        ctx.fillStyle=oc;ctx.beginPath();ctx.arc(x+w-7,y+8,4.5,0,Math.PI*2);ctx.fill();
        ctx.restore();
      }
    }
  });

  // PLAYERS (강화된 토큰)
  G.players.forEach(p=>{
    if(p.bkrt)return;
    const{x,y,w,h}=cellXY(p.pos);
    const offsets=[[-8,-8],[8,-8],[-8,8],[8,8]];
    const[ox,oy]=offsets[p.id]||[0,0];
    const px=x+w/2+ox,py=y+h/2+oy;
    const isActive=G.cur===p.id;
    const r=isActive?11:8;

    ctx.save();
    // 외곽 글로우 링 (활성 플레이어)
    if(isActive){
      ctx.shadowBlur=28;ctx.shadowColor=p.col;
      // 펄스 링
      const pulse=0.4+0.6*Math.abs(Math.sin(Date.now()*0.004));
      ctx.globalAlpha=pulse*0.5;
      ctx.strokeStyle=p.col;ctx.lineWidth=2;
      ctx.beginPath();ctx.arc(px,py,r+5,0,Math.PI*2);ctx.stroke();
      ctx.globalAlpha=1;
    }

    // 토큰 본체 (그라디언트)
    const tg=ctx.createRadialGradient(px-r*.3,py-r*.3,0,px,py,r);
    tg.addColorStop(0,p.col+'ff');tg.addColorStop(1,p.col+'88');
    ctx.shadowBlur=isActive?22:10;ctx.shadowColor=p.col;
    ctx.fillStyle=isActive?tg:p.col+'77';
    ctx.beginPath();ctx.arc(px,py,r,0,Math.PI*2);ctx.fill();

    // 테두리
    ctx.strokeStyle=isActive?'rgba(255,255,255,0.8)':'rgba(255,255,255,0.3)';
    ctx.lineWidth=isActive?1.8:1;
    ctx.beginPath();ctx.arc(px,py,r,0,Math.PI*2);ctx.stroke();

    // 이모지
    ctx.shadowBlur=0;ctx.globalAlpha=1;
    ctx.font=(isActive?'12':'10')+'px sans-serif';
    ctx.textAlign='center';ctx.fillText(p.em,px,py+4);
    ctx.restore();
  });
}

// ============================================================
//  UI RENDERS
// ============================================================
function mono(pid,ctry,Gs=G){
  const cp=Gs.cells.filter(c=>c.t==='prop'&&c.ctry===ctry);
  return cp.length>0&&cp.every(c=>c.own===pid);
}

function nw(p){
  let v=p.cash;
  G.cells.forEach(c=>{if(c.own===p.id&&c.t==='prop')v+=Math.floor(c.price*(0.6+(c.hs||0)*.4+(c.ho?.5:0)));});
  return Math.max(0,v);
}

function renderPCards(){
  const container=document.getElementById('pcards');
  container.innerHTML='';
  const maxNW=Math.max(...G.players.map(nw),1);

  G.players.forEach((p,i)=>{
    const pnw=nw(p);const pct=Math.max(2,Math.round(pnw/maxNW*100));
    const propCount=G.cells.filter(c=>c.own===p.id&&c.t==='prop').length;
    const bldCount=G.cells.reduce((s,c)=>s+(c.own===p.id?((c.hs||0)+(c.ho?5:0)):0),0);
    const cashChange=pnw-p.initCash;

    const d=document.createElement('div');
    d.className='pc'+(i===G.cur?' act':'')+(p.bkrt?' bk':'');
    d.id='pc'+i;

    const gradStart=p.col+'22';
    const fillGrad=`linear-gradient(90deg,${p.col},${p.col}88)`;

    d.innerHTML=`
      <div class="pch">
        <div class="pcav" style="border-color:${p.col}33;">
          <span>${p.em}</span>
          <div class="act-ring" style="border-color:${p.col};"></div>
        </div>
        <div style="flex:1;min-width:0;">
          <div class="pcn" style="color:${p.col}">${p.name}</div>
          <span class="pcbadge ${p.isBot?'bot':'you'}">${p.isBot?'BOT':'YOU'}</span>
          <div class="pcloc">${p.bkrt?'💀 파산':'📍 '+G.cells[p.pos]?.name}</div>
        </div>
        <div style="text-align:right;">
          <div class="pcc" style="color:${p.bkrt?'#ff3355':'#00ff88'}">₩${p.cash.toLocaleString()}</div>
          <div class="pcnet">순자산 ₩${pnw.toLocaleString()}</div>
        </div>
      </div>
      <div class="pcstats">
        <div class="pcstat"><div class="sv">₩${pnw.toLocaleString()}</div><div class="sl">순자산</div></div>
        <div class="pcstat"><div class="sv">${propCount}</div><div class="sl">부동산</div></div>
        <div class="pcstat"><div class="sv">${bldCount}</div><div class="sl">건물</div></div>
      </div>
      <div class="pbar"><div class="pfill" style="width:${pct}%;background:${fillGrad};"></div></div>
    `;
    container.appendChild(d);
  });
}

function renderLegend(){
  const g=document.getElementById('legendGrid');g.innerHTML='';
  COUNTRIES.forEach((c,ci)=>{
    const owned=G.cells.filter(x=>x.t==='prop'&&x.ctry===ci&&x.own>=0);
    const total=G.cells.filter(x=>x.t==='prop'&&x.ctry===ci).length;
    const d=document.createElement('div');d.className='legend-item';
    const ownerCol=owned.length>0?G.players[owned[0].own]?.col||'#fff':'var(--text3)';
    d.innerHTML=`
      <div class="legend-dot" style="background:${c.col};"></div>
      <div class="legend-flag">${c.flag}</div>
      <div class="legend-name">${c.name}</div>
      <div class="legend-own" style="color:${ownerCol}">${owned.length}/${total}</div>
    `;
    g.appendChild(d);
  });
}

// ============================================================
//  TURN LOGIC
// ============================================================
function startTurn(){
  const p=G.players[G.cur];
  if(p.bkrt){nextTurn();return;}

  // Island check
  if(p.jl){
    p.jt=(p.jt||0)+1;
    if(p.jt>=3||(G._islandFree)){
      p.jl=false;p.jt=0;
      addLog(p.em+' 무인도 탈출!','good');
      toast('🏝️ 탈출 성공!','good');
    } else {
      addLog(p.em+' 무인도 '+p.jt+'턴째...','bad');
      toast('🏝️ 고립 중 ('+p.jt+'/3)','bad');
      endAct(p.id,false);return;
    }
  }

  const rem=G.maxT-G.tot;
  const td=document.getElementById('tdsp');
  td.textContent='🕐 '+rem+'턴 남음';
  td.className='turn-display'+(rem<=5?' urgent':'');
  document.getElementById('rdsp').textContent='라운드 '+G.round;
  document.getElementById('cdsp').textContent=p.em+' '+p.name;

  if(p.isBot){
    document.getElementById('rbtn').disabled=true;
    document.getElementById('dhint').textContent=p.em+' '+p.name+' 분석 중...';
    setTimeout(()=>doRoll(true),800+Math.random()*600);
  } else {
    document.getElementById('rbtn').disabled=false;
    document.getElementById('dhint').textContent='▶ 주사위를 굴려 이동하세요';
  }

  checkAchievements();
}

function doRoll(isBot){
  document.getElementById('rbtn').disabled=true;
  document.getElementById('dhint').textContent='🎲 굴리는 중...';

  const d1El=document.getElementById('d1'),d2El=document.getElementById('d2');
  const dsumEl=document.getElementById('dsum');
  dsumEl.classList.remove('show');
  d1El.classList.remove('landed');d2El.classList.remove('landed');
  d1El.classList.add('rolling');d2El.classList.add('rolling');

  let t=0;
  const iv=setInterval(()=>{
    d1El.textContent=DF[Math.floor(Math.random()*6)];
    d2El.textContent=DF[Math.floor(Math.random()*6)];
    t++;
    if(t>=16){
      clearInterval(iv);
      const v1=Math.floor(Math.random()*6)+1,v2=Math.floor(Math.random()*6)+1;
      d1El.textContent=DF[v1-1];d2El.textContent=DF[v2-1];
      d1El.classList.remove('rolling');d2El.classList.remove('rolling');
      d1El.classList.add('landed');d2El.classList.add('landed');

      const tot=v1+v2,dbl=v1===v2;
      if(dbl){G.gameStats.doublesRolled++;}

      dsumEl.innerHTML=tot+(dbl?`<span class="double-badge">DOUBLE!</span>`:'');
      dsumEl.classList.add('show');

      const p=G.players[G.cur];
      if(dbl)toast('🎉 더블! '+v1+'+'+v2,'gold');
      else addLog(p.em+' '+v1+'+'+v2+'='+tot+'칸','');

      moveP(G.cur,tot,dbl);
    }
  },70);
}

async function moveP(pi,steps,dbl){
  const p=G.players[pi];const trail=[];
  for(let s=1;s<=steps;s++){
    p.pos=(p.pos+1)%40;trail.push(p.pos);
    if(p.pos===0){
      let bonus=200;
      if(p.bk==='pass')bonus+=100;
      p.cash+=bonus;p.totalEarned+=bonus;
      addLog(p.em+' 출발 통과! +₩'+bonus,'good');
      toast('🚀 출발 통과 +₩'+bonus,'good');
    }
    drawBoard([...trail],p.col+'66');
    renderPCards();
    await sl(100);
  }
  await sl(150);
  drawBoard();renderPCards();
  await land(pi,dbl);
}

async function land(pi,dbl){
  const p=G.players[pi];const c=G.cells[p.pos];
  addLog(p.em+' → '+c.name,'');

  if(c.t==='go'){
    p.cash+=200;p.totalEarned+=200;
    addLog('🚀 출발칸 +₩200','good');toast('🚀 +₩200','good');
    endAct(pi,dbl);
  } else if(c.t==='island'){
    if(G._islandFree){
      addLog(p.em+' 무인도 통과 (FTA 혜택)','sys');
      toast('🌐 무인도 면제!','sys');endAct(pi,dbl);
    } else if(p.jl){
      // Already handled in startTurn
      endAct(pi,dbl);
    } else {
      p.jl=true;p.jt=0;
      showEventPop('🏝️','무인도 고립','island',p.name+' 이(가) 무인도에 고립됩니다!','3턴 동안 이동 불가',p.em+' 3턴 고립','#ff8c42','rgba(255,140,66,.3)',null,pi,dbl);
    }
  } else if(c.t==='golden'){
    p.cash+=1000;p.totalEarned+=1000;
    showEventPop('✨','황금시대','golden','부동산 시장이 황금기를 맞이했습니다!','황금시대','+₩1,000 획득','#ffd700','rgba(255,215,0,.3)',null,pi,dbl);
  } else if(c.t==='taxhub'){
    const tx=Math.floor(p.cash*.1);
    p.cash-=tx;p.totalLost+=tx;
    G.gameStats.totalTax+=tx;
    showEventPop('💼','세금징수소','tax','국세청이 재산의 10%를 징수합니다','세금 납부','-₩'+tx,'#ff3355','rgba(255,51,85,.3)',()=>ckBk(pi),pi,dbl);
  } else if(c.t==='tax'){
    const txAmt=G.diff==='easy'?Math.floor(c.amt*.7):(G.diff==='hard'?Math.floor(c.amt*1.3):c.amt);
    p.cash-=txAmt;p.totalLost+=txAmt;
    G.gameStats.totalTax+=txAmt;
    addLog(p.em+' 💸 세금 -₩'+txAmt,'bad');
    toast('💸 세금 -₩'+txAmt,'bad');ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);
  } else if(c.t==='chance'){
    G.gameStats.totalChance++;
    const cd=CHANCE[Math.floor(Math.random()*CHANCE.length)];
    const result=cd.fx(p,G.players,G.cells,G);
    if(!p._ex&&!p._mg){
      showEventPop('🎲','찬스!','chance',cd.txt,cd.desc||'',result,cd.col,'rgba(255,215,0,.25)',()=>ckBk(pi),pi,dbl);
    } else if(p._ex){
      p._ex=false;addLog('🎲 '+cd.txt+' → 추가 굴리기!','gold');
      drawBoard();renderPCards();
      toast('🎲 한 번 더!','gold');
      setTimeout(()=>doRoll(p.isBot),700);
    } else if(p._mg){
      p._mg=false;showMG(pi,dbl);
    }
  } else if(c.t==='community'){
    const cd=COMMUNITY[Math.floor(Math.random()*COMMUNITY.length)];
    const result=cd.fx(p,G.players,G.cells);
    showEventPop('🏦','공동체기금','community',cd.txt,cd.desc||'',result,cd.col,'rgba(16,172,132,.25)',()=>ckBk(pi),pi,dbl);
  } else if(c.t==='airport'){
    if(c.own<0){
      if(p.isBot&&p.cash>=1000){
        c.own=pi;p.cash-=1000;
        addLog(p.em+' ✈️ 공항 매입','good');
        drawBoard();renderPCards();endAct(pi,dbl);
      } else if(!p.isBot){
        showProp(pi,dbl,'airport',c);
      } else endAct(pi,dbl);
    } else if(c.own===pi){
      addLog(p.em+' 자신의 공항','sys');endAct(pi,dbl);
    } else {
      const ow=G.players[c.own];
      const fee=Math.floor(500*(c._airportMod||1));
      p.cash-=Math.min(fee,p.cash);ow.cash+=Math.min(fee,p.cash+Math.min(fee,p.cash));
      addLog(p.em+' ✈️ 공항 이용료 -₩'+fee+' → '+ow.em,'bad');
      toast('✈️ -₩'+fee,'bad');ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);
    }
  } else if(c.t==='prop'){
    if(c.own<0){
      if(p.isBot){
        const ratio=p.cash/c.price;
        if(ratio>1.8||(ratio>1.3&&mono(p.id,c.ctry))){buyProp(pi,p.pos);}
        endAct(pi,dbl);
      } else showProp(pi,dbl,'buy',c);
    } else if(c.own===pi){
      if(p.isBot)botBuild(pi,dbl);else showProp(pi,dbl,'build',c);
    } else {
      const ow=G.players[c.own];
      const ri=c.ho>0?5:(c.hs||0);
      let rent=c.rent[Math.min(ri,5)];
      // Modifiers
      if(c._rentMod)rent=Math.floor(rent*c._rentMod);
      if(G.ecoEvent&&G.ecoEvent.title==='글로벌 경제 호황')rent=Math.floor(rent*1.2);
      if(G.ecoEvent&&G.ecoEvent.title==='글로벌 금융위기')rent=Math.floor(rent*.8);
      if(mono(c.own,c.ctry))rent=Math.floor(rent*(ow.bk==='mono'?2.8:2));
      if(ow.bk==='rent')rent=Math.floor(rent*1.12);

      // Dodge bonus
      if(p.bk==='dodge'&&Math.random()<.1){
        addLog(p.em+' 🦊 임대료 회피!','purple');
        toast('🦊 임대료 회피!','purple');endAct(pi,dbl);return;
      }

      addLog(p.em+' → '+ow.em+' 임대료 ₩'+rent,'bad');
      toast('💸 임대료 -₩'+rent,'bad');
      G.gameStats.totalRent+=rent;

      // Bankruptcy check with asset liquidation
      if(p.cash<rent){
        let canPay=p.cash;
        G.cells.forEach(cell=>{
          if(cell.own===pi&&cell.t==='prop'&&canPay<rent){
            const sv=Math.floor(cell.price*(cell.ho?0.7:cell.hs>0?0.6:0.5));
            canPay+=sv;p.cash+=sv;cell.own=-1;cell.hs=0;cell.ho=0;
            addLog(p.em+' 긴급매각 '+cell.name+' +₩'+sv,'sys');
          }
        });
      }

      if(p.cash<rent){
        ow.cash+=p.cash;p.totalLost+=p.cash;
        addLog(p.em+' 💀 파산! 잔여자산 → '+ow.em,'bad');
        toast('💀 '+p.name+' 파산!','bad');
        p.cash=0;p.bkrt=true;
        G.cells.forEach(cell=>{if(cell.own===pi){cell.own=c.own;}});
        drawBoard();renderPCards();renderLegend();endAct(pi,dbl);return;
      }
      p.cash-=rent;ow.cash+=rent;
      p.totalLost+=rent;ow.totalEarned+=rent;
      ckBk(pi);drawBoard();renderPCards();renderLegend();endAct(pi,dbl);
    }
  }
}

function buyProp(pi,ci){
  const p=G.players[pi];const c=G.cells[ci];
  const disc=p.bk==='build'?.85:1;
  const costMod=G._buildCostMod||1;
  const pr=Math.floor(c.price*disc);
  if(p.cash<pr)return false;
  p.cash-=pr;p.totalLost+=pr;c.own=pi;
  addLog(p.em+' 🏠 '+c.name+' 매입 -₩'+pr,'good');
  toast('🏠 '+c.name+' 매입!','good');
  if(mono(pi,c.ctry)){
    toast('🌟 '+COUNTRIES[c.ctry].flag+' 독점!','gold');
    addLog('🌟 '+COUNTRIES[c.ctry].name+' 독점 달성!','gold');
    showAchievement('monopoly');
  }
  showAchievement('firstBuy');
  renderLegend();
  return true;
}

function botBuild(pi,dbl){
  const p=G.players[pi];
  G.cells.forEach(c=>{
    if(c.own!==pi||c.t!=='prop')return;
    const bc=Math.floor(c.price*.5*(p.bk==='build'?.85:1)*(G._buildCostMod||1));
    if(c.ho>=1)return;
    if((c.hs||0)>=4&&p.cash>=bc*2){
      c.hs=0;c.ho=1;p.cash-=bc*2;
      addLog(p.em+' 🏨 호텔 at '+c.name,'good');
      showAchievement('hotel');
    } else if((c.hs||0)<4&&p.cash>=bc&&p.cash>c.price*2){
      c.hs=(c.hs||0)+1;p.cash-=bc;
      addLog(p.em+' 🏠 집 '+c.hs+'채 at '+c.name,'good');
    }
  });
  endAct(pi,dbl);
}

// ── PROPERTY POPUP ──
function showProp(pi,dbl,type,c){
  const p=G.players[pi];
  const ctryName=c.ctry>=0?(COUNTRIES[c.ctry]?.flag||'')+' '+COUNTRIES[c.ctry]?.name:'';
  document.getElementById('pctry').textContent=ctryName;
  document.getElementById('ptitle').textContent=c.name||'';
  document.getElementById('ptitle').style.color=c.col||'var(--text)';

  let info='',btnLabel='',btnAction=null,canAfford=true;

  if(type==='buy'){
    const disc=p.bk==='build'?.85:1;const pr=Math.floor(c.price*disc);
    canAfford=p.cash>=pr;
    const rentRows=c.rent?c.rent.map((r,i)=>{
      const label=['기본','집1','집2','집3','집4','호텔'][i];
      const cur=(c.hs||0)===i||(i===5&&c.ho>0);
      return`<div class="rent-row${cur?' cur':''}"><span>${label}</span><span>₩${r}</span></div>`;
    }).join(''):'';
    info=`
      <div class="prow"><span class="prlbl">매입가</span><span class="prval">${disc<1?`<del style="color:var(--text2);font-size:.75rem;">₩${c.price}</del> `:''}₩${pr.toLocaleString()}</span></div>
      <div class="prow"><span class="prlbl">현재 잔고</span><span style="color:${canAfford?'var(--green)':'var(--red)'}">₩${p.cash.toLocaleString()}</span></div>
      ${c.rent?`<div class="rent-table"><div style="font-size:.72rem;color:var(--text2);margin-bottom:5px;font-family:Rajdhani;letter-spacing:2px;">RENT TABLE</div>${rentRows}</div>`:''}
      ${mono(pi,c.ctry)?'<div style="color:var(--gold);font-size:.78rem;text-align:center;padding:6px;background:rgba(255,215,0,.06);border-radius:8px;">⭐ 독점 시 임대료 2배!</div>':''}
    `;
    btnLabel='🏠 매입하기';
    btnAction=()=>{
      if(canAfford){buyProp(pi,p.pos);}else toast('💸 잔고 부족!','bad');
      closeProp();drawBoard();renderPCards();endAct(pi,dbl);
    };
  } else if(type==='build'){
    const bc=Math.floor(c.price*.5*(p.bk==='build'?.85:1)*(G._buildCostMod||1));
    canAfford=p.cash>=bc&&!c.ho;
    const nextLevel=c.ho?'최고 단계':(c.hs||0)>=4?'호텔':('집 '+(c.hs+1)+'채');
    info=`
      <div class="prow"><span class="prlbl">현재 건물</span><span>${'🏠'.repeat(c.hs||0)}${c.ho?'🏨':''}</span></div>
      <div class="prow"><span class="prlbl">다음 단계</span><span style="color:var(--cyan)">${nextLevel}</span></div>
      <div class="prow"><span class="prlbl">건설 비용</span><span class="prval">₩${bc.toLocaleString()}</span></div>
      <div class="prow"><span class="prlbl">현재 임대료</span><span style="color:var(--cyan)">₩${c.rent?c.rent[Math.min((c.hs||0)+(c.ho?5:0),5)]:0}</span></div>
      <div class="prow"><span class="prlbl">다음 임대료</span><span style="color:var(--green)">₩${c.rent?c.rent[Math.min((c.hs||0)+1+(c.ho?4:0),5)]:0}</span></div>
    `;
    btnLabel=(c.hs||0)>=4&&!c.ho?'🏨 호텔 건설':'🏠 집 건설';
    btnAction=()=>{
      if(c.ho){toast('이미 호텔!','');closeProp();endAct(pi,dbl);return;}
      const bc2=Math.floor(c.price*.5*(p.bk==='build'?.85:1)*(G._buildCostMod||1));
      if(p.cash<bc2){toast('💸 잔고 부족!','bad');closeProp();endAct(pi,dbl);return;}
      p.cash-=bc2;
      if((c.hs||0)>=4){c.hs=0;c.ho=1;addLog(p.em+' 🏨 호텔! '+c.name,'gold');showAchievement('hotel');}
      else{c.hs=(c.hs||0)+1;addLog(p.em+' 🏠 집 '+c.hs+'채 at '+c.name,'good');}
      closeProp();drawBoard();renderPCards();endAct(pi,dbl);
    };
  } else if(type==='airport'){
    canAfford=p.cash>=1000;
    info=`
      <div class="prow"><span class="prlbl">매입가</span><span class="prval">₩1,000</span></div>
      <div class="prow"><span class="prlbl">타인 이용료</span><span style="color:var(--cyan)">₩500/회</span></div>
      <div class="prow"><span class="prlbl">현재 잔고</span><span style="color:${canAfford?'var(--green)':'var(--red)'}">₩${p.cash.toLocaleString()}</span></div>
    `;
    btnLabel='✈️ 공항 매입';
    btnAction=()=>{
      if(p.cash>=1000){p.cash-=1000;c.own=pi;addLog(p.em+' ✈️ 공항 매입!','good');}
      else toast('💸 잔고 부족!','bad');
      closeProp();drawBoard();renderPCards();endAct(pi,dbl);
    };
  }

  document.getElementById('pinfo').innerHTML=info;
  const btns=document.getElementById('pbtns');
  btns.innerHTML=`
    <button class="pbtn buy" ${!canAfford?'disabled':''} id="popBuyBtn">${btnLabel}</button>
    <button class="pbtn pass">통과</button>
  `;
  if(btnAction)btns.querySelector('#popBuyBtn').onclick=btnAction;
  btns.querySelector('.pass').onclick=()=>{closeProp();endAct(pi,dbl);};
  document.getElementById('pp2').style.display='flex';
}
function closeProp(){document.getElementById('pp2').style.display='none';}

// ── EVENT POPUP ──
function showEventPop(icon,type,id,title,desc,effect,col,border,afterFx,pi,dbl){
  const box=document.getElementById('evBox');
  document.getElementById('evIcon').textContent=icon;
  document.getElementById('evType').textContent=type.toUpperCase();
  document.getElementById('evTitle').textContent=title;
  document.getElementById('evDesc').textContent=desc;
  const effEl=document.getElementById('evEffect');
  effEl.textContent=effect;
  effEl.style.color=col;effEl.style.background=border.replace('.4','.1').replace('.3','.08').replace('.25','.08');
  box.style.borderColor=border;
  box.style.boxShadow=`0 0 50px ${border.replace('.3','.12').replace('.4','.1')},0 20px 60px rgba(0,0,0,.7)`;
  const okBtn=document.getElementById('evOk');
  okBtn.style.background=col;okBtn.style.color='#000';
  okBtn.onclick=()=>{
    document.getElementById('evPop').style.display='none';
    if(afterFx)afterFx();
    drawBoard();renderPCards();renderLegend();endAct(pi,dbl);
  };
  document.getElementById('evPop').style.display='flex';
}

// ── MINIGAME ──
function showMG(pi,dbl){
  const mg=MG[Math.floor(Math.random()*MG.length)];
  document.getElementById('mgo').style.display='flex';
  document.getElementById('mgt').textContent='🎮 미니게임 찬스!';
  document.getElementById('mgd').textContent=`정답 → +₩${mg.reward} | 오답 → -₩200`;
  document.getElementById('mgq').textContent=mg.q;
  document.getElementById('mgReward').textContent='';

  let tl=12,answered=false;
  const circ=document.getElementById('mgTimerCirc');
  circ.style.stroke='var(--cyan)';
  circ.style.strokeDashoffset='0';
  document.getElementById('mgtime').textContent=tl;

  const iv=setInterval(()=>{
    tl--;
    document.getElementById('mgtime').textContent=tl;
    const pct=tl/12;
    circ.style.strokeDashoffset=CIRCUMFERENCE*(1-pct);
    if(tl<=3)circ.style.stroke='var(--red)';
    else if(tl<=6)circ.style.stroke='var(--orange)';
    if(tl<=0&&!answered){clearInterval(iv);answered=true;finMG(pi,dbl,false,mg.reward);}
  },1000);

  const opts=document.getElementById('mgopts');opts.innerHTML='';
  mg.o.forEach((o,i)=>{
    const b=document.createElement('button');b.className='mgopt';b.textContent=o;
    b.onclick=()=>{
      if(answered)return;answered=true;clearInterval(iv);
      const ok=i===mg.a;
      b.classList.add(ok?'ok':'no');
      if(!ok)opts.children[mg.a].classList.add('ok');
      const rewardEl=document.getElementById('mgReward');
      rewardEl.textContent=ok?'🎉 정답! +₩'+mg.reward:'💸 오답... -₩200';
      rewardEl.style.color=ok?'var(--green)':'var(--red)';
      rewardEl.style.background=ok?'rgba(0,255,136,.1)':'rgba(255,51,85,.1)';
      setTimeout(()=>finMG(pi,dbl,ok,mg.reward),1000);
    };
    opts.appendChild(b);
  });
}

function finMG(pi,dbl,ok,reward){
  const p=G.players[pi];
  document.getElementById('mgo').style.display='none';
  if(ok){
    p.cash+=reward;p.totalEarned+=reward;p._mgWins++;
    toast('🎉 정답! +₩'+reward,'good');addLog(p.em+' 미니게임 성공 +₩'+reward,'good');
    showAchievement('mgWin');
  } else {
    p.cash-=200;p.totalLost+=200;
    toast('💸 오답 -₩200','bad');addLog(p.em+' 미니게임 실패 -₩200','bad');
  }
  drawBoard();renderPCards();endAct(pi,dbl);
}

// ── MARKET / ASSET MANAGEMENT ──
function openMarket(){
  const p=G.players[0];
  document.getElementById('marketSub').textContent=`잔고: ₩${p.cash.toLocaleString()} | 순자산: ₩${nw(p).toLocaleString()}`;
  const list=document.getElementById('marketList');list.innerHTML='';
  const myProps=G.cells.filter(c=>c.own===0&&c.t==='prop');
  if(myProps.length===0){
    list.innerHTML='<div style="color:var(--text2);text-align:center;padding:20px;">보유 부동산 없음</div>';
  } else {
    myProps.forEach(c=>{
      const sv=Math.floor(c.price*(c.ho?0.7:c.hs>0?0.6:0.5));
      const row=document.createElement('div');row.className='market-row';
      row.innerHTML=`
        <div class="market-col" style="background:${c.col}"></div>
        <div>
          <div class="market-name">${COUNTRIES[c.ctry]?.flag||''} ${c.name}</div>
          <div class="market-info">${'🏠'.repeat(c.hs||0)}${c.ho?'🏨':''} 임대료 ₩${c.rent[Math.min((c.hs||0)+(c.ho?5:0),5)]}</div>
        </div>
        <div class="market-price">₩${c.price}</div>
        <button class="market-sell" data-ci="${c.idx}">₩${sv} 매각</button>
      `;
      row.querySelector('.market-sell').onclick=()=>{
        c.own=-1;p.cash+=sv;c.hs=0;c.ho=0;
        addLog(p.em+' 매각 '+c.name+' +₩'+sv,'sys');
        toast('💰 '+c.name+' 매각 +₩'+sv,'good');
        openMarket();drawBoard();renderPCards();renderLegend();
      };
      list.appendChild(row);
    });
  }
  document.getElementById('marketOv').style.display='flex';
}
function closeMarket(){document.getElementById('marketOv').style.display='none';}

// ── ECONOMIC EVENTS ──
function tryEcoEvent(){
  if(!G.eventsEnabled)return;
  if(G.ecoEvent){
    G.ecoTurns--;
    if(G.ecoTurns<=0){
      addLog('📰 '+G.ecoEvent.title+' 종료','sys');
      // Reset mods
      if(G.ecoEvent.title==='글로벌 경제 호황'||G.ecoEvent.title==='글로벌 금융위기'){
        G.cells.forEach(c=>{if(c.t==='prop')c._rentMod=1;});
      }
      if(G.ecoEvent.title==='자유무역 협정'){G.cells.forEach(c=>{if(c.t==='airport')c._airportMod=1;});}
      if(G.ecoEvent.title==='외국인 직접투자 급증')G._islandFree=false;
      if(G.ecoEvent.title==='중앙은행 금리 인상')G._buildCostMod=1;
      G.ecoEvent=null;
    }
    return;
  }

  // 15% chance per round start
  if(G.cur===0&&Math.random()<.15){
    const ev=ECO_EVENTS[Math.floor(Math.random()*ECO_EVENTS.length)];
    G.ecoEvent=ev;G.ecoTurns=ev.dur;
    ev.fx(G.cells,G.players,G);
    addLog('🌐 경제 이벤트: '+ev.title,'gold');
    showEcoBar(ev);
    drawBoard();renderPCards();renderLegend();
  }
}

function showEcoBar(ev){
  const existing=document.getElementById('mevBar');
  if(existing)existing.remove();
  const bar=document.createElement('div');bar.className='mev-bar';bar.id='mevBar';
  bar.innerHTML=`
    <div class="mev-icon">${ev.icon}</div>
    <div class="mev-content">
      <div class="mev-label">${ev.type.toUpperCase()} · ${ev.dur}턴 지속</div>
      <div class="mev-title">${ev.title}</div>
      <div class="mev-desc">${ev.desc}</div>
    </div>
    <button class="mev-close" onclick="document.getElementById('mevBar').remove()">확인</button>
  `;
  bar.style.borderTopColor=ev.border;
  document.body.appendChild(bar);
  setTimeout(()=>{if(bar.parentNode)bar.remove();},8000);
}

// ── ACHIEVEMENTS ──
function checkAchievements(){
  const p=G.players[0];
  ACHIEVEMENTS.forEach(ach=>{
    if(!unlockedAch.has(ach.id)&&ach.check(p,G)){
      unlockedAch.add(ach.id);showAchievement(ach.id);
    }
  });
}

function showAchievement(id){
  const ach=ACHIEVEMENTS.find(a=>a.id===id);
  if(!ach||unlockedAch.has(id+'shown'))return;
  unlockedAch.add(id+'shown');
  const el=document.createElement('div');el.className='ach-toast';
  el.style.borderColor='rgba(255,215,0,.4)';
  el.innerHTML=`
    <div class="ach-icon">${ach.icon}</div>
    <div class="ach-content">
      <div class="ach-label">🏆 업적 달성!</div>
      <div class="ach-name">${ach.name}</div>
      <div class="ach-desc">${ach.desc}</div>
    </div>
  `;
  document.body.appendChild(el);
  setTimeout(()=>el.remove(),4200);
}

// ── BANKRUPTCY ──
function ckBk(pi){
  const p=G.players[pi];
  if(p.cash<0){
    G.cells.forEach(c=>{
      if(c.own===pi&&c.t==='prop'&&p.cash<0){
        const sv=Math.floor(c.price*.5);p.cash+=sv;c.own=-1;c.hs=0;c.ho=0;
        addLog(p.em+' 긴급매각 +₩'+sv,'sys');
      }
    });
    if(p.cash<0){
      if(pi===0)p._survived++;
      p.bkrt=true;p.cash=0;
      addLog(p.em+' 💀 파산!','bad');
      toast('💀 '+p.name+' 파산!','bad');
      drawBoard();renderPCards();renderLegend();
      if(pi===0)showAchievement('survivor');
    }
  }
  // Check rich achievements
  if(pi===0){
    if(nw(p)>=10000)showAchievement('rich10k');
    if(nw(p)>=20000)showAchievement('rich20k');
    if(G.cells.filter(c=>c.own===0&&c.t==='prop').length>=5)showAchievement('landlord');
  }
}

function endAct(pi,dbl){
  renderPCards();renderLegend();
  const alive=G.players.filter(p=>!p.bkrt);
  if(alive.length<=1){endGame('파산 종료');return;}
  G.tot++;
  if(G.tot>=G.maxT){endGame('턴 초과');return;}
  tryEcoEvent();
  setTimeout(nextTurn,250);
}

function nextTurn(){
  G.cur=(G.cur+1)%G.players.length;
  while(G.players[G.cur].bkrt)G.cur=(G.cur+1)%G.players.length;
  if(G.cur===0)G.round++;
  renderPCards();startTurn();
}

// ============================================================
//  GAME END
// ============================================================
function endGame(reason){
  const rs=document.getElementById('rs');
  rs.style.display='flex';rs.style.flexDirection='column';
  rs.style.alignItems='center';rs.style.justifyContent='center';

  const sorted=[...G.players].sort((a,b)=>nw(b)-nw(a));
  const winner=sorted[0];

  document.getElementById('rtitle').textContent=winner.bkrt?'😱 전원 파산!':'🏆 게임 종료!';
  document.getElementById('rsub').textContent=reason+' · '+G.tot+'턴 · '+G.round+'라운드';

  const rc=document.getElementById('rcards');rc.innerHTML='';
  ['🥇','🥈','🥉','4️⃣'].forEach((m,i)=>{
    if(!sorted[i])return;
    const p=sorted[i];
    const change=nw(p)-p.initCash;
    const d=document.createElement('div');
    d.className='rcard'+(i===0?' win':'');
    d.style.setProperty('--delay',(i*.12+.1)+'s');
    d.innerHTML=`
      <div class="rrk">${m}${p.em}</div>
      <div class="rn">${p.name}${p.bkrt?' 💀':''}</div>
      <div class="rv">₩${nw(p).toLocaleString()}</div>
      <div class="rchange ${change>=0?'pos':'neg'}">${change>=0?'+':''}-₩${Math.abs(change).toLocaleString()}</div>
    `;
    rc.appendChild(d);
  });

  // Stats
  const st=document.getElementById('rstats');
  const youP=G.players[0];
  st.innerHTML=`
    <div class="rstat"><div class="rstat-v">${G.tot}</div><div class="rstat-l">총 턴</div></div>
    <div class="rstat"><div class="rstat-v">₩${G.gameStats.totalRent.toLocaleString()}</div><div class="rstat-l">총 임대료</div></div>
    <div class="rstat"><div class="rstat-v">${G.gameStats.doublesRolled}</div><div class="rstat-l">더블 횟수</div></div>
    <div class="rstat"><div class="rstat-v">₩${G.gameStats.totalTax.toLocaleString()}</div><div class="rstat-l">총 세금</div></div>
    <div class="rstat"><div class="rstat-v">${G.cells.filter(c=>c.own===0).length}</div><div class="rstat-l">보유 자산</div></div>
    <div class="rstat"><div class="rstat-v">${youP._mgWins}</div><div class="rstat-l">퀴즈 승리</div></div>
  `;

  try{window.parent.postMessage({type:'marble_result',score:nw(winner),wins:winner.id===0?1:0},'*');}catch(e){}
  if(!winner.bkrt)fireworks();
}

let _fwStats=false;
function showFinalStats(){
  if(_fwStats)return;_fwStats=true;
  const p=G.players[0];
  const earned=p.totalEarned,lost=p.totalLost;
  toast('총 수입: ₩'+earned.toLocaleString(),'good');
  setTimeout(()=>toast('총 지출: ₩'+lost.toLocaleString(),'bad'),400);
}

// ============================================================
//  FIREWORKS
// ============================================================
function fireworks(){
  const bg=document.getElementById('fw');
  const cols=['#ffd700','#ff3355','#4dabf7','#00ff88','#c084fc','#fb923c'];
  for(let f=0;f<12;f++){
    setTimeout(()=>{
      const x=5+Math.random()*90,y=3+Math.random()*65;
      const col=cols[Math.floor(Math.random()*cols.length)];
      for(let i=0;i<28;i++){
        const p=document.createElement('div');
        const ang=(i/28)*Math.PI*2;
        const dist=60+Math.random()*100;
        const dur=.5+Math.random()*.7;
        p.style.cssText=`position:absolute;left:${x}%;top:${y}%;width:6px;height:6px;border-radius:50%;background:${col};box-shadow:0 0 4px ${col};animation:fwp ${dur}s ease-out forwards;--dx:${Math.cos(ang)*dist}px;--dy:${Math.sin(ang)*dist}px;`;
        bg.appendChild(p);
        setTimeout(()=>p.remove(),(dur+.15)*1000);
      }
      // Trail
      const t=document.createElement('div');
      t.style.cssText=`position:absolute;left:${x}%;top:${y+5}%;font-size:1.2rem;animation:fwt 2s ease-out forwards;`;
      t.textContent=['🎊','✨','🌟','💫'][Math.floor(Math.random()*4)];
      bg.appendChild(t);setTimeout(()=>t.remove(),2100);
    },f*350);
  }
}

// ============================================================
//  UTILITIES
// ============================================================
function sl(ms){return new Promise(r=>setTimeout(r,ms));}

function addLog(txt,type){
  const b=document.getElementById('lbox');
  const d=document.createElement('div');d.className='le'+(type?' '+type:'');
  d.innerHTML=`<span class="le-turn">T${G.tot}</span><span>${txt}</span>`;
  b.insertBefore(d,b.firstChild);
  while(b.children.length>60)b.removeChild(b.lastChild);
}

function toast(txt,type){
  const w=document.getElementById('twrap');const d=document.createElement('div');
  const colors={good:'rgba(0,255,136,.3)',bad:'rgba(255,51,85,.3)',gold:'rgba(255,215,0,.3)',sys:'rgba(34,211,238,.3)',purple:'rgba(192,132,252,.3)'};
  d.className='toast';d.style.borderColor=colors[type]||'rgba(255,255,255,.08)';
  d.style.color=type==='good'?'var(--green)':type==='bad'?'var(--red2)':type==='gold'?'var(--gold)':type==='sys'?'var(--cyan)':type==='purple'?'var(--purple)':'var(--text)';
  d.textContent=txt;w.appendChild(d);setTimeout(()=>d.remove(),3200);
}

// ============================================================
//  CHARACTER SELECT UI
// ============================================================
let selChar=0,selT=30,selDiff='normal',eventsOn=true;

function renderChars(){
  const g=document.getElementById('cgrid');g.innerHTML='';
  CHARS.forEach((c,i)=>{
    const d=document.createElement('div');
    d.className='ccard'+(i===0?' sel':'');
    const statLabels=['투자','분석','독점','운'];
    const statBars=c.stats.map((v,si)=>{
      const statCols=['#ffd700','#4dabf7','#c084fc','#00ff88'];
      return`<div class="cstat-bar"><div class="fill" style="width:${v}%;background:${statCols[si]};"></div></div>`;
    }).join('');
    d.innerHTML=`
      <span class="em">${c.em}</span>
      <div class="cn" style="color:${c.col}">${c.name}</div>
      <div class="ct">${c.trait}</div>
      <div class="cstat">${statBars}</div>
      <div class="cb">⭐ ${c.bonus}</div>
    `;
    d.title=c.desc;
    d.onclick=()=>{
      document.querySelectorAll('.ccard').forEach(el=>el.classList.remove('sel'));
      d.classList.add('sel');selChar=i;
    };
    g.appendChild(d);
  });
}

// Turn buttons
document.querySelectorAll('[data-t]').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('[data-t]').forEach(x=>x.classList.remove('a'));b.classList.add('a');selT=parseInt(b.dataset.t);};
});

// Diff buttons
document.querySelectorAll('[data-d]').forEach(b=>{
  b.onclick=()=>{
    document.querySelectorAll('[data-d]').forEach(x=>{x.classList.remove('a-easy','a-normal','a-hard');});
    b.classList.add('a-'+b.dataset.d);
    selDiff=b.dataset.d;
  };
});

// Event toggle
document.getElementById('evtToggle').onclick=function(){
  eventsOn=!eventsOn;
  this.dataset.on=eventsOn?'1':'0';
  this.textContent=eventsOn?'🌐 경제 이벤트 ON':'🌐 경제 이벤트 OFF';
  this.classList.toggle('a',eventsOn);
};

// Start button
document.getElementById('sbtn').onclick=()=>{
  G.eventsEnabled=eventsOn;
  startGame(selChar,selT,selDiff);
};

// Game buttons
document.getElementById('rbtn').onclick=()=>{
  const p=G.players[G.cur];if(p&&!p.isBot&&!p.bkrt)doRoll(false);
};
document.getElementById('marketBtn').onclick=openMarket;
document.getElementById('moreBtn').onclick=()=>{
  toast('현재 순자산: ₩'+nw(G.players[0]).toLocaleString(),'gold');
};

// Canvas hover for cell info
cv.addEventListener('mousemove',e=>{
  const rect=cv.getBoundingClientRect();
  const scale=cv.width/rect.width;
  const mx=(e.clientX-rect.left)*scale;
  const my=(e.clientY-rect.top)*scale;
  for(let i=0;i<40;i++){
    const{x,y,w,h}=cellXY(i);
    if(mx>=x&&mx<x+w&&my>=y&&my<y+h){
      const c=G.cells[i];
      if(c.t==='prop'&&c.own>=0){
        cv.title=`${c.name} - ${G.players[c.own]?.name} 소유 | 임대료: ₩${c.rent[Math.min((c.hs||0)+(c.ho?5:0),5)]}`;
      } else cv.title=c.name;
      return;
    }
  }
});

// Init
renderChars();
initParticles();
</script>
</body>
</html>"""

def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import load_db, save_db, update_leaderboard
    from utils.config import USERS_FILE

    # 결과 처리는 app.py _save_game_result()에서 $set으로 원자적 처리됨

    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
    .block-container{padding:0 !important;max-width:100% !important;}iframe{border:none;}
    </style>
    """, unsafe_allow_html=True)

    # uid를 JS 전역변수로 주입
    _cur_uid = st.session_state.get('logged_in_user', '')
    if _cur_uid:
        _cv1.html('<script>window.parent._gr_uid="' + _cur_uid + '";</script>', height=0)

    listener_html = f"""
    <script>
    window.parent.addEventListener('message', function(e) {{
      if (e.data && e.data.type === 'marble_result') {{
        const url = new URL(window.parent.location.href);
        url.searchParams.set('marble_score', e.data.score);
        url.searchParams.set('marble_wins',  e.data.wins ?? 0);
        url.searchParams.set('_gr_uid', '{_cur_uid}');
        window.parent.location.href = url.toString();
      }}
    }});
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=960, scrolling=True)

if __name__ == "__main__":
    render()
