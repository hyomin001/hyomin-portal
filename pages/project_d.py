import streamlit as st
import streamlit.components.v1 as components

GAME_HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=no">
<title>인베스트마블 ULTRA</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&family=Black+Han+Sans&family=Orbitron:wght@700;900&display=swap" rel="stylesheet">
<style>
:root{--bg:#05080f;--bg2:#080d1a;--bg3:#0d1525;--gold:#ffd700;--gold2:#ffb800;--green:#10d96e;--red:#ff4560;--blue:#4dabf7;--purple:#b26cf7;--cyan:#22d3ee;--orange:#ff8c42;--text:#e8f0ff;--text2:#7a8fb5;--border:rgba(255,255,255,0.08);--r:12px;}
*{box-sizing:border-box;margin:0;padding:0;}
html,body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;min-height:100vh;user-select:none;}
.bg{position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse 60% 40% at 20% 20%,rgba(75,0,130,.1) 0%,transparent 60%),radial-gradient(ellipse 50% 60% at 80% 80%,rgba(0,50,120,.1) 0%,transparent 60%);}
#fw{position:fixed;inset:0;pointer-events:none;z-index:490;overflow:hidden;}
@keyframes fw{to{transform:translate(var(--dx),var(--dy));opacity:0;}}

/* CHAR SELECT */
#cs{position:fixed;inset:0;z-index:200;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(5,8,15,.97);}
.cs-title{font-family:'Black Han Sans',sans-serif;font-size:clamp(1.8rem,4vw,3rem);background:linear-gradient(135deg,#ffd700,#ff8c00,#ff4d6d);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:3px;margin-bottom:4px;text-align:center;}
.cs-sub{color:var(--text2);font-size:.78rem;letter-spacing:4px;margin-bottom:24px;}
.cgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:0 16px;max-width:720px;width:100%;}
.ccard{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.1);border-radius:var(--r);padding:18px 10px;cursor:pointer;transition:all .2s;text-align:center;}
.ccard:hover,.ccard.sel{transform:translateY(-4px);border-color:var(--gold);box-shadow:0 0 24px rgba(255,215,0,.25);}
.ccard .em{font-size:2.4rem;display:block;margin-bottom:6px;}
.ccard .cn{font-weight:700;font-size:.9rem;}
.ccard .ct{font-size:.7rem;color:var(--text2);margin-top:3px;}
.ccard .cb{font-size:.68rem;color:var(--cyan);margin-top:5px;font-weight:700;}
.trow{display:flex;gap:10px;margin:18px 0;}
.tbtn{padding:9px 20px;border-radius:8px;border:2px solid rgba(255,255,255,.1);background:rgba(255,255,255,.04);color:var(--text2);cursor:pointer;font-size:.85rem;font-weight:700;transition:all .2s;}
.tbtn.a,.tbtn:hover{border-color:var(--cyan);color:var(--cyan);background:rgba(34,211,238,.08);}
.sbtn{margin-top:18px;padding:13px 48px;font-size:1rem;font-weight:900;font-family:'Black Han Sans',sans-serif;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#1a0a00;border:none;border-radius:40px;cursor:pointer;letter-spacing:2px;box-shadow:0 0 28px rgba(255,215,0,.4);transition:all .2s;}
.sbtn:hover{transform:scale(1.05);box-shadow:0 0 45px rgba(255,215,0,.6);}

/* GAME MAIN */
#gm{display:none;flex-direction:column;min-height:100vh;position:relative;z-index:1;}
.tbar{background:rgba(8,13,26,.95);border-bottom:1px solid rgba(255,255,255,.08);padding:9px 18px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;backdrop-filter:blur(10px);position:sticky;top:0;z-index:100;}
.tbar-ttl{font-family:'Black Han Sans',sans-serif;font-size:1rem;background:linear-gradient(135deg,var(--gold),var(--orange));-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.tdsp{background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);border-radius:8px;padding:4px 12px;font-size:.85rem;font-weight:700;color:var(--gold);}
.tdsp.urg{animation:urgP .8s infinite;}
@keyframes urgP{0%,100%{background:rgba(255,69,96,.15);}50%{background:rgba(255,69,96,.3);}}
.pills{display:flex;gap:7px;flex-wrap:wrap;}
.pill{padding:3px 9px;border-radius:20px;font-size:.73rem;font-weight:700;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);}

/* BOARD WRAP */
.bwrap{display:flex;gap:14px;padding:14px;align-items:flex-start;justify-content:center;flex-wrap:wrap;}
#bc{background:var(--bg2);border:2px solid rgba(255,255,255,.08);border-radius:14px;box-shadow:0 12px 48px rgba(0,0,0,.8);position:relative;flex-shrink:0;}
.spanel{width:270px;display:flex;flex-direction:column;gap:10px;flex-shrink:0;}

/* PLAYER CARDS */
.pc{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:13px;position:relative;}
.pc.act{border-color:var(--gold);box-shadow:0 0 18px rgba(255,215,0,.2);}
.pc.bk{opacity:.5;filter:grayscale(.6);}
.pch{display:flex;align-items:center;gap:9px;margin-bottom:9px;}
.pcav{font-size:1.5rem;}
.pcn{font-weight:700;font-size:.88rem;}
.pct{font-size:.68rem;color:var(--text2);}
.pcc{font-size:1.05rem;font-weight:900;color:var(--green);}
.pcnet{font-size:.73rem;color:var(--text2);}
.pbar{height:4px;background:rgba(255,255,255,.07);border-radius:2px;overflow:hidden;margin-top:5px;}
.pfill{height:100%;background:linear-gradient(90deg,var(--green),var(--cyan));border-radius:2px;transition:width .4s;}

/* LOG & DICE */
.lbox{background:rgba(255,255,255,.02);border:1px solid rgba(255,255,255,.06);border-radius:10px;padding:10px;max-height:190px;overflow-y:auto;font-size:.76rem;line-height:1.7;}
.le{padding:2px 0;border-bottom:1px solid rgba(255,255,255,.03);}
.le:last-child{border:none;}
.le.good{color:var(--green);}.le.bad{color:var(--red);}.le.sys{color:var(--cyan);}.le.gold{color:var(--gold);}
.darea{text-align:center;padding:14px;}
.ddisp{font-size:3.5rem;margin:8px 0;display:flex;justify-content:center;gap:14px;}
.die{width:62px;height:62px;background:linear-gradient(135deg,#1e2d50,#0d1830);border:2px solid rgba(255,255,255,.1);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:2rem;font-weight:900;}
.die.r{animation:dr .08s linear infinite;}
@keyframes dr{0%{transform:rotate(-8deg);}50%{transform:rotate(8deg);}100%{transform:rotate(-8deg);}}
.rbtn{padding:11px 28px;font-size:.95rem;font-weight:900;font-family:'Black Han Sans',sans-serif;background:linear-gradient(135deg,var(--purple),#6c63ff);color:#fff;border:none;border-radius:28px;cursor:pointer;letter-spacing:1px;transition:all .2s;margin-top:5px;}
.rbtn:hover:not(:disabled){transform:scale(1.05);box-shadow:0 0 26px rgba(178,108,247,.5);}
.rbtn:disabled{opacity:.4;cursor:not-allowed;transform:none;}

/* POPUP */
.pov{position:fixed;inset:0;background:rgba(0,0,0,.75);z-index:300;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(5px);}
.pbox{background:linear-gradient(160deg,#0d1830,#1a2545);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:26px;max-width:400px;width:90%;box-shadow:0 30px 80px rgba(0,0,0,.7);}
.ptitle{font-family:'Black Han Sans',sans-serif;font-size:1.3rem;margin-bottom:7px;}
.pctry{font-size:.72rem;color:var(--text2);margin-bottom:14px;letter-spacing:2px;}
.prow{display:flex;justify-content:space-between;margin-bottom:7px;font-size:.85rem;}
.prlbl{color:var(--text2);}.prval{font-weight:700;color:var(--gold);}
.pbtns{display:flex;gap:9px;margin-top:16px;}
.pbtn{flex:1;padding:11px;border-radius:9px;border:none;font-size:.88rem;font-weight:700;cursor:pointer;transition:all .2s;}
.pbtn.buy{background:linear-gradient(135deg,var(--green),#00a854);color:#001a0d;}
.pbtn.buy:hover{transform:scale(1.03);}
.pbtn.pass{background:rgba(255,255,255,.04);color:var(--text2);border:1px solid rgba(255,255,255,.08);}
.pbtn.pass:hover{border-color:var(--red);color:var(--red);}

/* MINIGAME */
#mgo{position:fixed;inset:0;z-index:400;background:rgba(0,0,0,.85);align-items:center;justify-content:center;backdrop-filter:blur(7px);}
.mgbox{background:linear-gradient(160deg,#0d1830,#1a2545);border:2px solid var(--cyan);border-radius:16px;padding:28px;max-width:460px;width:90%;text-align:center;box-shadow:0 0 55px rgba(34,211,238,.18);}
.mgtitle{font-family:'Black Han Sans',sans-serif;font-size:1.5rem;color:var(--cyan);margin-bottom:8px;}
.mgdesc{color:var(--text2);font-size:.85rem;margin-bottom:18px;}
.mgtimer{font-size:1.3rem;font-weight:900;color:var(--gold);margin-bottom:9px;}
.mgq{font-size:1rem;font-weight:700;margin-bottom:18px;line-height:1.6;}
.mgopts{display:grid;grid-template-columns:1fr 1fr;gap:9px;margin-bottom:14px;}
.mgopt{padding:11px;border-radius:9px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);color:var(--text);cursor:pointer;font-size:.88rem;transition:all .2s;}
.mgopt:hover{border-color:var(--cyan);background:rgba(34,211,238,.07);}
.mgopt.ok{border-color:var(--green);background:rgba(16,217,110,.12);color:var(--green);}
.mgopt.no{border-color:var(--red);background:rgba(255,69,96,.12);color:var(--red);}

/* RESULT */
#rs{position:fixed;inset:0;z-index:500;background:rgba(5,8,15,.97);align-items:center;justify-content:center;flex-direction:column;}
.rtitle{font-family:'Black Han Sans',sans-serif;font-size:clamp(2rem,6vw,3.5rem);background:linear-gradient(135deg,var(--gold),var(--orange));-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:14px;text-align:center;}
.rsub{color:var(--text2);font-size:.95rem;margin-bottom:28px;text-align:center;}
.rcards{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin-bottom:28px;}
.rcard{background:rgba(255,255,255,.04);border:2px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 22px;text-align:center;min-width:150px;}
.rcard.win{border-color:var(--gold);box-shadow:0 0 36px rgba(255,215,0,.25);}
.rrk{font-size:1.6rem;margin-bottom:5px;}.rn{font-weight:700;font-size:.95rem;margin-bottom:3px;}.rv{color:var(--gold);font-weight:900;font-size:1.05rem;}
.rrbtn{padding:13px 44px;font-size:.95rem;font-weight:900;background:linear-gradient(135deg,var(--gold),var(--gold2));color:#1a0a00;border:none;border-radius:38px;cursor:pointer;letter-spacing:2px;transition:all .2s;}
.rrbtn:hover{transform:scale(1.05);}

/* TOAST */
.twrap{position:fixed;top:75px;right:18px;z-index:600;display:flex;flex-direction:column;gap:7px;pointer-events:none;}
.toast{padding:9px 16px;border-radius:9px;font-size:.82rem;font-weight:700;background:rgba(13,21,37,.95);border:1px solid rgba(255,255,255,.08);animation:ti .3s,to .3s 2.7s forwards;max-width:260px;}
@keyframes ti{from{opacity:0;transform:translateX(28px);}to{opacity:1;transform:translateX(0);}}
@keyframes to{to{opacity:0;transform:translateX(28px);}}
::-webkit-scrollbar{width:3px;}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:2px;}
</style>
</head>
<body>
<div class="bg"></div>
<div id="fw"></div>

<!-- CHAR SELECT -->
<div id="cs">
  <div class="cs-title">🌍 인베스트 마블 ULTRA</div>
  <div class="cs-sub">INVEST MARBLE · SEASON 1</div>
  <div class="cgrid" id="cgrid"></div>
  <div style="margin-top:18px;color:var(--text2);font-size:.8rem;">⏱️ 최대 턴 설정</div>
  <div class="trow" id="trow">
    <button class="tbtn" data-t="20">20턴</button>
    <button class="tbtn a" data-t="30">30턴</button>
    <button class="tbtn" data-t="40">40턴</button>
    <button class="tbtn" data-t="50">50턴</button>
  </div>
  <button class="sbtn" id="sbtn">🎲 게임 시작</button>
</div>

<!-- GAME MAIN -->
<div id="gm">
  <div class="tbar">
    <span class="tbar-ttl">🌍 인베스트 마블 ULTRA</span>
    <div id="tdsp" class="tdsp">🕐 남은 턴: —</div>
    <div class="pills">
      <span class="pill" id="pr">라운드 0</span>
      <span class="pill" id="pp">대기 중</span>
    </div>
  </div>
  <div class="bwrap">
    <canvas id="bc" width="600" height="600"></canvas>
    <div class="spanel">
      <div id="pcards"></div>
      <div class="pc">
        <div class="darea">
          <div class="ddisp"><div class="die" id="d1">🎲</div><div class="die" id="d2">🎲</div></div>
          <button class="rbtn" id="rbtn" disabled>주사위 굴리기</button>
          <div id="dhint" style="color:var(--text2);font-size:.76rem;margin-top:5px;"></div>
        </div>
      </div>
      <div class="pc">
        <div style="font-weight:700;font-size:.83rem;margin-bottom:7px;">📋 게임 로그</div>
        <div class="lbox" id="lbox"></div>
      </div>
    </div>
  </div>
</div>

<!-- PROPERTY POPUP -->
<div class="pov" id="pp2" style="display:none;">
  <div class="pbox">
    <div class="pctry" id="pctry"></div>
    <div class="ptitle" id="ptitle"></div>
    <div id="pinfo"></div>
    <div class="pbtns" id="pbtns"></div>
  </div>
</div>

<!-- MINIGAME -->
<div id="mgo" style="display:none;">
  <div class="mgbox">
    <div class="mgtitle" id="mgt">🎮 미니게임</div>
    <div class="mgdesc" id="mgd"></div>
    <div class="mgtimer" id="mgtime"></div>
    <div class="mgq" id="mgq"></div>
    <div class="mgopts" id="mgopts"></div>
  </div>
</div>

<!-- RESULT -->
<div id="rs" style="display:none;">
  <div class="rtitle" id="rtitle">🏆 게임 종료!</div>
  <div class="rsub" id="rsub"></div>
  <div class="rcards" id="rcards"></div>
  <button class="rrbtn" onclick="location.reload()">🔄 다시하기</button>
</div>

<div class="twrap" id="twrap"></div>

<script>
const DF=['⚀','⚁','⚂','⚃','⚄','⚅'];
const S=600,CELL=S/11;

const CHARS=[
  {name:'이효민',em:'👑',col:'#ffd700',trait:'경제학과 수재',bonus:'건물 할인 15%',bk:'build'},
  {name:'봇 알파',em:'🤖',col:'#4dabf7',trait:'AI 투자 봇',bonus:'임대료 +10%',bk:'rent'},
  {name:'미스터 K',em:'🎩',col:'#b26cf7',trait:'연쇄 투자자',bonus:'독점 보너스',bk:'mono'},
  {name:'탐정 J',em:'🕵️',col:'#22d3ee',trait:'정보 수집가',bonus:'다시 굴리기',bk:'reroll'},
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

// 40 border cells
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

const CHANCE=[
  {txt:'📈 주식 대박! +₩500',fx:p=>{p.cash+=500;}},
  {txt:'🎁 경품 당첨! +₩1,000',fx:p=>{p.cash+=1000;}},
  {txt:'💰 투자수익 ₩200/인 수금',fx:(p,ps)=>{ps.forEach(o=>{if(o!==p&&o.cash>0){o.cash-=200;p.cash+=200;}});}},
  {txt:'🏛️ 정부보조금 +₩400',fx:p=>{p.cash+=400;}},
  {txt:'🎰 즉석복권! ₩300 or -₩100',fx:p=>{p.cash+=Math.random()<.6?300:-100;}},
  {txt:'💸 과태료 -₩300',fx:p=>{p.cash-=300;}},
  {txt:'🚀 출발로 GO! +₩200',fx:p=>{p.pos=0;p.cash+=200;}},
  {txt:'🔙 3칸 후진',fx:p=>{p.pos=(p.pos-3+40)%40;}},
  {txt:'🎲 한 번 더 굴리기!',fx:p=>{p._ex=true;}},
  {txt:'💼 미니게임 도전! 성공 +₩800',fx:p=>{p._mg=true;}},
  {txt:'🏦 건물당 +₩50 보너스',fx:(p,_,cells)=>{let b=0;cells.forEach(c=>{if(c.own===p.id)b+=50*((c.ho||0)+(c.ho||0)>0?4:(c.hs||0));});p.cash+=b;}},
  {txt:'✈️ 가장 가까운 공항으로',fx:(p,_,cells)=>{const a=[6,15,25,32];let n=a[0],md=99;a.forEach(i=>{const d=(i-p.pos+40)%40;if(d>0&&d<md){md=d;n=i;}});p.pos=n;}},
];

const COMMUNITY=[
  {txt:'🏥 병원비 -₩500',fx:p=>{p.cash-=500;}},
  {txt:'🎓 장학금 +₩600',fx:p=>{p.cash+=600;}},
  {txt:'🏠 임대료 ₩150/인 수금',fx:(p,ps)=>{ps.forEach(o=>{if(o!==p&&o.cash>0){o.cash-=150;p.cash+=150;}});}},
  {txt:'💸 수리비 집×₩80',fx:(p,_,cells)=>{let c=0;cells.forEach(cl=>{if(cl.own===p.id)c+=cl.hs*80+cl.ho*200;});p.cash-=c;}},
  {txt:'🎉 생일선물 +₩300',fx:p=>{p.cash+=300;}},
  {txt:'📉 주가폭락 -₩400',fx:p=>{p.cash-=400;}},
  {txt:'🏆 우수시민상 +₩800',fx:p=>{p.cash+=800;}},
  {txt:'🔧 수선비 -₩100',fx:p=>{p.cash-=100;}},
];

const MG=[
  {q:'한국의 수도는?',o:['서울','부산','인천','광주'],a:0},
  {q:'세계에서 인구가 가장 많은 나라는?',o:['중국','인도','미국','인도네시아'],a:1},
  {q:'가장 큰 대륙은?',o:['아시아','아프리카','유럽','남미'],a:0},
  {q:'비트코인 최초 발행 연도는?',o:['2005','2007','2009','2011'],a:2},
  {q:'GDP가 가장 높은 나라는?',o:['중국','미국','일본','독일'],a:1},
  {q:'달에 처음 착륙한 우주선은?',o:['아폴로 11','아폴로 13','아르테미스','보스토크'],a:0},
  {q:'지구에서 가장 긴 강은?',o:['아마존','나일','양쯔강','미시시피'],a:1},
  {q:'1+1은?',o:['1','2','3','4'],a:1},
];

// GAME STATE
let G={phase:'s',players:[],cur:0,round:1,maxT:30,tot:0,cells:[]};

function initCells(){G.cells=RAW_CELLS.map((c,i)=>({...c,idx:i,own:-1,hs:0,ho:0}));}

function startGame(ci,mt){
  initCells();G.maxT=mt;G.tot=0;G.round=1;G.cur=0;
  const pc=CHARS[ci];
  const bots=CHARS.filter((_,i)=>i!==ci).slice(0,3);
  G.players=[
    {id:0,name:pc.name,em:pc.em,col:pc.col,bk:pc.bk,isBot:false,cash:15000,pos:0,bkrt:false,jl:false,jt:0,_ex:false,_mg:false},
    ...bots.map((c,i)=>({id:i+1,name:c.name,em:c.em,col:c.col,bk:c.bk,isBot:true,cash:15000,pos:0,bkrt:false,jl:false,jt:0,_ex:false,_mg:false}))
  ];
  document.getElementById('cs').style.display='none';
  document.getElementById('gm').style.display='flex';
  document.getElementById('rs').style.display='none';
  document.getElementById('mgo').style.display='none';
  renderPCards();drawBoard();startTurn();
}

// CANVAS DRAWING
const cv=document.getElementById('bc');
const ctx=cv.getContext('2d');

function cellXY(i){
  if(i<=10) return{x:i*CELL,y:S-CELL,w:CELL,h:CELL};
  if(i<=20) return{x:S-CELL,y:S-CELL-(i-10)*CELL,w:CELL,h:CELL};
  if(i<=30) return{x:S-CELL-(i-20)*CELL,y:0,w:CELL,h:CELL};
  return{x:0,y:(i-30)*CELL,w:CELL,h:CELL};
}

function rr(x,y,w,h,r){ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.arcTo(x+w,y,x+w,y+r,r);ctx.lineTo(x+w,y+h-r);ctx.arcTo(x+w,y+h,x+w-r,y+h,r);ctx.lineTo(x+r,y+h);ctx.arcTo(x,y+h,x,y+h-r,r);ctx.lineTo(x,y+r);ctx.arcTo(x,y,x+r,y,r);ctx.closePath();}

function wt(text,x,y,mw,lh){
  const words=[...text];let l='';const ls=[];
  words.forEach(c=>{const t=l+c;if(ctx.measureText(t).width>mw&&l){ls.push(l);l=c;}else l=t;});
  if(l)ls.push(l);
  const sy=y-(ls.length-1)*lh/2;
  ls.forEach((s,i)=>ctx.fillText(s,x,sy+i*lh));
}

function drawBoard(trail=[],tcol='rgba(255,215,0,0.5)'){
  ctx.clearRect(0,0,S,S);
  // bg
  ctx.fillStyle='#080d1a';ctx.fillRect(0,0,S,S);
  // center
  const cx=CELL,cy=CELL,cw=S-CELL*2,ch=S-CELL*2;
  ctx.fillStyle='rgba(13,21,37,.8)';rr(ctx,cx,cy,cw,ch,10);ctx.fill();
  // center text
  ctx.textAlign='center';
  ctx.font=`bold ${CELL*.28}px "Black Han Sans"`;
  ctx.fillStyle='rgba(255,215,0,.18)';ctx.fillText('인베스트 마블',S/2,S/2-8);
  ctx.font=`${CELL*.15}px "Noto Sans KR"`;
  ctx.fillStyle='rgba(255,215,0,.12)';ctx.fillText('남은 턴: '+(G.maxT-G.tot),S/2,S/2+14);

  G.cells.forEach((c,i)=>{
    const{x,y,w,h}=cellXY(i);
    const isT=trail.includes(i);
    let bg='#0d1525';
    if(c.t==='go')bg='#003020';
    else if(c.t==='island')bg='#2a1800';
    else if(c.t==='golden')bg='#1a1500';
    else if(c.t==='taxhub'||c.t==='tax')bg='#1a0a0a';
    else if(c.t==='chance')bg='#1a1500';
    else if(c.t==='community')bg='#001a20';
    else if(c.t==='airport')bg='#001a2a';
    if(isT){ctx.shadowBlur=18;ctx.shadowColor=tcol;ctx.fillStyle=tcol.replace('.5','.2');rr(ctx,x+1,y+1,w-2,h-2,3);ctx.fill();ctx.shadowBlur=0;}
    ctx.fillStyle=bg;rr(ctx,x+1,y+1,w-2,h-2,3);ctx.fill();
    // border
    let bc='rgba(255,255,255,.05)';
    if(c.t==='prop'&&c.own>=0)bc=G.players[c.own]?.col||'#ffd700';
    ctx.strokeStyle=bc;ctx.lineWidth=1.3;rr(ctx,x+1,y+1,w-2,h-2,3);ctx.stroke();
    // color stripe
    if(c.t==='prop'&&c.col){ctx.fillStyle=c.col;ctx.fillRect(x+2,y+2,w-4,4);}
    // content
    const mx=x+w/2,my=y+h/2;ctx.textAlign='center';
    const fs=Math.max(8,CELL*.26);
    if(c.t==='go'){ctx.font=`bold ${CELL*.2}px "Noto Sans KR"`;ctx.fillStyle='#10d96e';ctx.fillText('출발',mx,my-3);ctx.font=`${CELL*.3}px sans-serif`;ctx.fillText('🚀',mx,my+CELL*.16);}
    else if(c.t==='island'){ctx.font=`${CELL*.3}px sans-serif`;ctx.fillText('🏝️',mx,my-2);ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ff8c42';ctx.fillText('무인도',mx,my+CELL*.22);}
    else if(c.t==='golden'){ctx.font=`${CELL*.28}px sans-serif`;ctx.fillText('✨',mx,my-2);ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ffd700';ctx.fillText('황금시대',mx,my+CELL*.2);}
    else if(c.t==='taxhub'){ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText('💼',mx,my-2);ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#ff4560';ctx.fillText('세금징수소',mx,my+CELL*.2);}
    else if(c.t==='chance'){ctx.font=`${CELL*.28}px sans-serif`;ctx.fillText('🎲',mx,my-2);ctx.font=`${CELL*.13}px "Noto Sans KR"`;ctx.fillStyle='#ffd700';ctx.fillText('찬스!',mx,my+CELL*.2);}
    else if(c.t==='community'){ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText('🏦',mx,my-2);ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#10ac84';ctx.fillText('공동체기금',mx,my+CELL*.2);}
    else if(c.t==='airport'){ctx.font=`${CELL*.26}px sans-serif`;ctx.fillText('✈️',mx,my-2);ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#22d3ee';ctx.fillText(c.name,mx,my+CELL*.2);}
    else if(c.t==='tax'){ctx.font=`${CELL*.24}px sans-serif`;ctx.fillText('💸',mx,my-3);ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='#ff4560';ctx.fillText(c.name,mx,my+CELL*.16);}
    else if(c.t==='prop'){
      ctx.font=`${CELL*.15}px "Noto Sans KR"`;ctx.fillStyle='rgba(255,255,255,.85)';
      wt(c.name,mx,my-3,w-5,CELL*.15);
      if(c.ho>0){ctx.font=`${CELL*.2}px sans-serif`;ctx.fillText('🏨',mx,my+CELL*.2);}
      else if(c.hs>0){ctx.font=`${CELL*.14}px sans-serif`;ctx.fillText('🏠'.repeat(Math.min(c.hs,4)),mx,my+CELL*.2);}
      ctx.font=`${CELL*.12}px "Noto Sans KR"`;ctx.fillStyle='rgba(255,215,0,.55)';ctx.fillText('₩'+c.price,mx,my+CELL*.35);
      if(c.own>=0){const oc=G.players[c.own]?.col||'#fff';ctx.fillStyle=oc;ctx.beginPath();ctx.arc(x+w-6,y+7,4,0,Math.PI*2);ctx.fill();}
    }
  });

  // players
  G.players.forEach(p=>{
    if(p.bkrt)return;
    const{x,y,w,h}=cellXY(p.pos);
    const ox=(p.id%2===0?-7:7);const oy=(p.id<2?-7:7);
    const px=x+w/2+ox,py=y+h/2+oy;
    ctx.shadowBlur=10;ctx.shadowColor=p.col;
    ctx.fillStyle=p.col;ctx.beginPath();ctx.arc(px,py,8,0,Math.PI*2);ctx.fill();
    ctx.shadowBlur=0;
    ctx.font='10px sans-serif';ctx.textAlign='center';ctx.fillText(p.em,px,py+3);
  });
}

// PLAYER CARDS
function renderPCards(){
  const c=document.getElementById('pcards');c.innerHTML='';
  const maxNW=Math.max(...G.players.map(nw),1);
  G.players.forEach((p,i)=>{
    const pnw=nw(p);const pct=Math.round(pnw/maxNW*100);
    const d=document.createElement('div');
    d.className='pc'+(i===G.cur?' act':'')+(p.bkrt?' bk':'');
    d.id='pc'+i;
    d.innerHTML=`<div class="pch"><span class="pcav">${p.em}</span><div><div class="pcn" style="color:${p.col}">${p.name}${p.isBot?'<span style="font-size:.62rem;color:var(--text2)"> BOT</span>':' <span style="font-size:.62rem;color:var(--cyan)">YOU</span>'}</div><div class="pct">${p.bkrt?'💀 파산':'📍 '+G.cells[p.pos]?.name}</div></div></div><div class="pcc">₩${p.cash.toLocaleString()}</div><div class="pcnet">순자산 ₩${pnw.toLocaleString()}</div><div class="pbar"><div class="pfill" style="width:${pct}%"></div></div>`;
    c.appendChild(d);
  });
}

function nw(p){let v=p.cash;G.cells.forEach(c=>{if(c.own===p.id&&c.t==='prop')v+=c.price*(1+(c.hs||0)*.5+(c.ho||0));});return v;}

function mono(pid,ctry){const cp=G.cells.filter(c=>c.t==='prop'&&c.ctry===ctry);return cp.length>0&&cp.every(c=>c.own===pid);}

// TURN
function startTurn(){
  const p=G.players[G.cur];
  if(p.bkrt){nextTurn();return;}
  const rem=G.maxT-G.tot;
  const td=document.getElementById('tdsp');
  td.textContent='🕐 남은 턴: '+rem;td.className='tdsp'+(rem<=5?' urg':'');
  document.getElementById('pr').textContent='라운드 '+G.round;
  document.getElementById('pp').textContent=p.em+' '+p.name+'의 턴';
  if(p.isBot){
    document.getElementById('rbtn').disabled=true;
    document.getElementById('dhint').textContent=p.em+' '+p.name+' 생각 중...';
    setTimeout(()=>doRoll(true),1000+Math.random()*700);
  } else {
    document.getElementById('rbtn').disabled=false;
    document.getElementById('dhint').textContent='▶ 주사위를 굴려 이동하세요';
  }
}

function doRoll(isBot){
  document.getElementById('rbtn').disabled=true;
  document.getElementById('dhint').textContent='🎲 굴리는 중...';
  const d1=document.getElementById('d1'),d2=document.getElementById('d2');
  d1.classList.add('r');d2.classList.add('r');
  let t=0;
  const iv=setInterval(()=>{
    d1.textContent=DF[Math.floor(Math.random()*6)];
    d2.textContent=DF[Math.floor(Math.random()*6)];
    t++;
    if(t>=14){
      clearInterval(iv);
      const v1=Math.floor(Math.random()*6)+1,v2=Math.floor(Math.random()*6)+1;
      d1.textContent=DF[v1-1];d2.textContent=DF[v2-1];
      d1.classList.remove('r');d2.classList.remove('r');
      const tot=v1+v2,dbl=v1===v2;
      if(dbl)toast('🎉 더블! '+v1+'+'+v2+'='+tot,'gold');
      else toast(G.players[G.cur].em+' '+v1+'+'+v2+'='+tot+'칸','');
      moveP(G.cur,tot,dbl);
    }
  },80);
}

async function moveP(pi,steps,dbl){
  const p=G.players[pi];const trail=[];
  for(let s=1;s<=steps;s++){
    p.pos=(p.pos+1)%40;trail.push(p.pos);
    if(p.pos===0){p.cash+=200;addLog(p.em+' 출발 통과! +₩200','good');toast('🚀 출발 통과 +₩200','good');}
    drawBoard([...trail],p.col+'88');renderPCards();
    await sl(115);
  }
  await sl(180);
  drawBoard();renderPCards();
  await land(pi,dbl);
}

async function land(pi,dbl){
  const p=G.players[pi];const c=G.cells[p.pos];
  addLog(p.em+' → '+c.name+'('+p.pos+')','');
  if(c.t==='go'){p.cash+=200;addLog('🚀 출발칸 추가 +₩200','good');toast('🚀 +₩200 보너스','good');endAct(pi,dbl);}
  else if(c.t==='island'){
    if(p.jl){p.jt=(p.jt||0)+1;if(p.jt>=3){p.jl=false;p.jt=0;addLog(p.em+' 탈출!','good');}else addLog(p.em+' 무인도 '+p.jt+'턴째...','bad');endAct(pi,false);}
    else{p.jl=true;p.jt=0;addLog(p.em+' 🏝️ 무인도 고립! 3턴','bad');toast('🏝️ 무인도 고립!','bad');endAct(pi,dbl);}
  }
  else if(c.t==='golden'){p.cash+=1000;addLog('✨황금시대 +₩1,000','gold');toast('✨ +₩1,000!','gold');endAct(pi,dbl);}
  else if(c.t==='taxhub'){const tx=Math.floor(p.cash*.1);p.cash-=tx;addLog('💼 세금 10% -₩'+tx,'bad');toast('💼 -₩'+tx,'bad');ckBk(pi);endAct(pi,dbl);}
  else if(c.t==='tax'){p.cash-=c.amt;addLog('💸 세금 -₩'+c.amt,'bad');toast('💸 -₩'+c.amt,'bad');ckBk(pi);endAct(pi,dbl);}
  else if(c.t==='chance'){
    const cd=CHANCE[Math.floor(Math.random()*CHANCE.length)];
    cd.fx(p,G.players,G.cells);addLog('🎲 찬스: '+cd.txt,'gold');toast('🎲 '+cd.txt,'gold');
    if(p._ex){p._ex=false;drawBoard();renderPCards();setTimeout(()=>doRoll(p.isBot),900);return;}
    if(p._mg){p._mg=false;showMG(pi,dbl);return;}
    ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);
  }
  else if(c.t==='community'){
    const cd=COMMUNITY[Math.floor(Math.random()*COMMUNITY.length)];
    cd.fx(p,G.players,G.cells);addLog('🏦 공동체: '+cd.txt,'sys');toast('🏦 '+cd.txt,'sys');
    ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);
  }
  else if(c.t==='airport'){
    if(c.own<0){
      if(p.isBot&&p.cash>=1000){c.own=pi;p.cash-=1000;addLog(p.em+' ✈️ 공항 매입','good');drawBoard();renderPCards();endAct(pi,dbl);}
      else if(!p.isBot)showPop(pi,dbl,'airport',c);
      else endAct(pi,dbl);
    } else if(c.own===pi){addLog(p.em+' 자신의 공항','');endAct(pi,dbl);}
    else{const ow=G.players[c.own];p.cash-=500;ow.cash+=500;addLog(p.em+' ✈️ 사용료 -₩500 → '+ow.em,'bad');toast('✈️ -₩500','bad');ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);}
  }
  else if(c.t==='prop'){
    if(c.own<0){
      if(p.isBot){if(p.cash>=c.price&&p.cash/c.price>2){buyP(pi,p.pos);}endAct(pi,dbl);}
      else showPop(pi,dbl,'buy',c);
    } else if(c.own===pi){
      if(p.isBot)botBld(pi,dbl);else showPop(pi,dbl,'build',c);
    } else {
      const ow=G.players[c.own];
      const ri=c.ho>0?5:(c.hs||0);
      let rent=c.rent[Math.min(ri,5)];
      if(mono(c.own,c.ctry))rent=Math.floor(rent*2);
      if(ow.bk==='rent')rent=Math.floor(rent*1.1);
      addLog(p.em+' → '+ow.em+' 임대료 ₩'+rent,'bad');toast('💸 임대료 -₩'+rent,'bad');
      // [모두의마블 규칙] 잔고 부족 시 재산 강제매각 후 지불, 그래도 부족하면 파산
      if(p.cash<rent){
        G.cells.forEach(cell=>{
          if(cell.own===pi&&cell.t==='prop'&&p.cash<rent){
            const sv=Math.floor(cell.price*.5);
            p.cash+=sv;cell.own=-1;cell.hs=0;cell.ho=0;
            addLog(p.em+' 긴급매각 '+cell.name+' +₩'+sv,'sys');
          }
        });
      }
      if(p.cash<rent){
        ow.cash+=p.cash;
        addLog(p.em+' 💀 파산! 남은 ₩'+p.cash+' → '+ow.em,'bad');
        toast(p.em+' '+p.name+' 파산! 💀','bad');
        p.cash=0;p.bkrt=true;
        G.cells.forEach(cell=>{if(cell.own===pi){cell.own=c.own;addLog(ow.em+' '+cell.name+' 몰수','sys');}});
        drawBoard();renderPCards();endAct(pi,dbl);return;
      }
      p.cash-=rent;ow.cash+=rent;
      ckBk(pi);drawBoard();renderPCards();endAct(pi,dbl);
    }
  }
}

function buyP(pi,ci){
  const p=G.players[pi];const c=G.cells[ci];
  const disc=p.bk==='build'?.85:1;const pr=Math.floor(c.price*disc);
  if(p.cash<pr)return false;
  p.cash-=pr;c.own=pi;
  addLog(p.em+' 🏠 '+c.name+' 매입 -₩'+pr,'good');toast('🏠 '+c.name+' 매입!','good');
  if(mono(pi,c.ctry)){toast('🌟 '+COUNTRIES[c.ctry].flag+' 독점!','gold');addLog('🌟 '+COUNTRIES[c.ctry].name+' 독점!','gold');}
  return true;
}

function botBld(pi,dbl){
  const p=G.players[pi];
  G.cells.forEach(c=>{
    if(c.own!==pi||c.t!=='prop')return;
    const bc=Math.floor(c.price*.5*(p.bk==='build'?.85:1));
    if(c.hs>=4&&c.ho<1&&p.cash>=bc*2){c.hs=0;c.ho=1;p.cash-=bc*2;addLog(p.em+' 🏨 호텔 at '+c.name,'good');}
    else if(c.hs<4&&p.cash>=bc&&p.cash>c.price*2.5){c.hs++;p.cash-=bc;addLog(p.em+' 🏠 집 at '+c.name,'good');}
  });
  endAct(pi,dbl);
}

function showPop(pi,dbl,type,c){
  const p=G.players[pi];
  document.getElementById('pctry').textContent=c.ctry>=0?(COUNTRIES[c.ctry]?.flag||'')+' '+COUNTRIES[c.ctry]?.name:'';
  document.getElementById('ptitle').textContent=c.name||'';
  document.getElementById('ptitle').style.color=c.col||'var(--text)';
  let info='',bl='매입',ba=null;
  if(type==='buy'){
    const disc=p.bk==='build'?.85:1;const pr=Math.floor(c.price*disc);
    info=`<div class="prow"><span class="prlbl">매입가</span><span class="prval">₩${pr.toLocaleString()}</span></div><div class="prow"><span class="prlbl">현재 잔고</span><span style="color:${p.cash>=pr?'var(--green)':'var(--red)'}">₩${p.cash.toLocaleString()}</span></div>${c.rent?`<div class="prow"><span class="prlbl">기본 임대료</span><span style="color:var(--text2)">₩${c.rent[0]}</span></div><div class="prow"><span class="prlbl">호텔 임대료</span><span style="color:var(--text2)">₩${c.rent[5]}</span></div>`:''}`;
    bl='🏠 매입하기';
    ba=()=>{if(p.cash>=pr)buyP(pi,p.pos);else toast('💸 잔고 부족!','bad');closePop();drawBoard();renderPCards();endAct(pi,dbl);};
  } else if(type==='build'){
    const bc=Math.floor(c.price*.5*(p.bk==='build'?.85:1));
    info=`<div class="prow"><span class="prlbl">현재 건물</span><span>${'🏠'.repeat(c.hs||0)}${c.ho?'🏨':''}</span></div><div class="prow"><span class="prlbl">건설 비용</span><span class="prval">₩${bc.toLocaleString()}</span></div><div class="prow"><span class="prlbl">현재 임대료</span><span style="color:var(--cyan)">₩${c.rent?c.rent[Math.min((c.hs||0)+(c.ho?5:0),5)]:0}</span></div>`;
    bl=(c.hs||0)>=4?'🏨 호텔 건설':'🏠 집 건설';
    ba=()=>{
      if(c.ho>=1){toast('이미 호텔!','');closePop();endAct(pi,dbl);return;}
      const bc2=Math.floor(c.price*.5*(p.bk==='build'?.85:1));
      if(p.cash<bc2){toast('💸 잔고 부족!','bad');closePop();endAct(pi,dbl);return;}
      p.cash-=bc2;
      if((c.hs||0)>=4){c.hs=0;c.ho=1;addLog(p.em+' 🏨 호텔 at '+c.name,'good');}
      else{c.hs=(c.hs||0)+1;addLog(p.em+' 🏠 집 at '+c.name,'good');}
      closePop();drawBoard();renderPCards();endAct(pi,dbl);
    };
  } else if(type==='airport'){
    info=`<div class="prow"><span class="prlbl">매입가</span><span class="prval">₩1,000</span></div><div class="prow"><span class="prlbl">타인 사용료</span><span style="color:var(--text2)">₩500/회</span></div>`;
    bl='✈️ 공항 매입';
    ba=()=>{if(p.cash>=1000){p.cash-=1000;c.own=pi;addLog(p.em+' ✈️ 공항 매입!','good');}else toast('💸 잔고 부족!','bad');closePop();drawBoard();renderPCards();endAct(pi,dbl);};
  }
  document.getElementById('pinfo').innerHTML=info;
  const btns=document.getElementById('pbtns');
  btns.innerHTML=`<button class="pbtn buy">${bl}</button><button class="pbtn pass">통과</button>`;
  btns.children[0].onclick=ba||null;
  btns.children[1].onclick=()=>{closePop();endAct(pi,dbl);};
  document.getElementById('pp2').style.display='flex';
}
function closePop(){document.getElementById('pp2').style.display='none';}

function showMG(pi,dbl){
  const mg=MG[Math.floor(Math.random()*MG.length)];
  document.getElementById('mgo').style.display='flex';
  document.getElementById('mgt').textContent='🎮 미니게임 찬스!';
  document.getElementById('mgd').textContent='정답 → +₩800 | 오답 → -₩200';
  document.getElementById('mgq').textContent=mg.q;
  let tl=10,ans=false;
  document.getElementById('mgtime').textContent='⏱️ '+tl+'s';
  const iv=setInterval(()=>{tl--;document.getElementById('mgtime').textContent='⏱️ '+tl+'s';if(tl<=0&&!ans){clearInterval(iv);ans=true;finMG(pi,dbl,false);}},1000);
  const opts=document.getElementById('mgopts');opts.innerHTML='';
  mg.o.forEach((o,i)=>{
    const b=document.createElement('button');b.className='mgopt';b.textContent=o;
    b.onclick=()=>{if(ans)return;ans=true;clearInterval(iv);const ok=i===mg.a;b.classList.add(ok?'ok':'no');if(!ok)opts.children[mg.a].classList.add('ok');setTimeout(()=>finMG(pi,dbl,ok),900);};
    opts.appendChild(b);
  });
}
function finMG(pi,dbl,ok){
  const p=G.players[pi];document.getElementById('mgo').style.display='none';
  if(ok){p.cash+=800;toast('🎉 정답! +₩800','good');addLog(p.em+' 미니게임 성공 +₩800','good');}
  else{p.cash-=200;toast('💸 오답 -₩200','bad');addLog(p.em+' 미니게임 실패 -₩200','bad');}
  drawBoard();renderPCards();endAct(pi,dbl);
}

function ckBk(pi){
  const p=G.players[pi];
  if(p.cash<0){
    G.cells.forEach(c=>{if(c.own===pi&&c.t==='prop'&&p.cash<0){const sv=Math.floor(c.price*.5);p.cash+=sv;c.own=-1;c.hs=0;c.ho=0;addLog(p.em+' 긴급매각 +₩'+sv,'sys');}});
    if(p.cash<0){p.bkrt=true;p.cash=0;addLog(p.em+' 💀 파산!','bad');toast(p.em+' '+p.name+' 파산!','bad');drawBoard();renderPCards();}
  }
}

function endAct(pi,dbl){
  renderPCards();
  const alive=G.players.filter(p=>!p.bkrt);
  if(alive.length===1){endGame('파산 결정');return;}
  G.tot++;
  if(G.tot>=G.maxT){endGame('턴 초과 종료');return;}
  setTimeout(()=>{nextTurn();},300);
}

function nextTurn(){
  G.cur=(G.cur+1)%G.players.length;
  while(G.players[G.cur].bkrt){G.cur=(G.cur+1)%G.players.length;}
  if(G.cur===0)G.round++;
  renderPCards();startTurn();
}

function endGame(reason){
  const rs=document.getElementById('rs');rs.style.display='flex';rs.style.flexDirection='column';rs.style.alignItems='center';rs.style.justifyContent='center';
  const sorted=[...G.players].sort((a,b)=>nw(b)-nw(a));
  document.getElementById('rtitle').textContent=sorted[0].bkrt?'😱 파산 종료':'🏆 게임 종료!';
  document.getElementById('rsub').textContent=reason+' — '+G.tot+'턴 경과';
  const rc=document.getElementById('rcards');rc.innerHTML='';
  ['🥇','🥈','🥉','4️⃣'].forEach((m,i)=>{
    if(!sorted[i])return;const p=sorted[i];
    const d=document.createElement('div');d.className='rcard'+(i===0?' win':'');
    d.innerHTML=`<div class="rrk">${m}${p.em}</div><div class="rn">${p.name}${p.bkrt?' 💀':''}</div><div class="rv">₩${nw(p).toLocaleString()}</div>`;
    rc.appendChild(d);
  });
  try{window.parent.postMessage({type:'marble_result',score:nw(sorted[0]),wins:sorted[0].id===0?1:0},'*');}catch(e){}
  if(!sorted[0].bkrt)fireworks();
}

function fireworks(){
  const bg=document.getElementById('fw');
  for(let f=0;f<8;f++){setTimeout(()=>{
    const x=10+Math.random()*80,y=5+Math.random()*60;
    const cols=['#ffd700','#ff4560','#4dabf7','#10d96e','#b26cf7'];
    const col=cols[Math.floor(Math.random()*cols.length)];
    for(let i=0;i<22;i++){const p=document.createElement('div');const ang=(i/22)*Math.PI*2,dist=50+Math.random()*90,dur=.6+Math.random()*.6;
      p.style.cssText=`position:absolute;left:${x}%;top:${y}%;width:5px;height:5px;border-radius:50%;background:${col};animation:fw ${dur}s ease-out forwards;--dx:${Math.cos(ang)*dist}px;--dy:${Math.sin(ang)*dist}px;`;
      bg.appendChild(p);setTimeout(()=>p.remove(),(dur+.1)*1000);}
  },f*400);}
}

function sl(ms){return new Promise(r=>setTimeout(r,ms));}

function addLog(txt,type){
  const b=document.getElementById('lbox');const d=document.createElement('div');
  d.className='le'+(type?' '+type:'');d.textContent=txt;
  b.insertBefore(d,b.firstChild);while(b.children.length>55)b.removeChild(b.lastChild);
}

function toast(txt,type){
  const w=document.getElementById('twrap');const d=document.createElement('div');d.className='toast';
  d.style.borderColor=type==='good'?'rgba(16,217,110,.4)':type==='bad'?'rgba(255,69,96,.4)':type==='gold'?'rgba(255,215,0,.4)':type==='sys'?'rgba(34,211,238,.4)':'rgba(255,255,255,.08)';
  d.textContent=txt;w.appendChild(d);setTimeout(()=>d.remove(),3200);
}

// CHAR SELECT UI
let selChar=0,selT=30;

function renderChars(){
  const g=document.getElementById('cgrid');g.innerHTML='';
  CHARS.forEach((c,i)=>{
    const d=document.createElement('div');d.className='ccard'+(i===0?' sel':'');
    d.innerHTML=`<span class="em">${c.em}</span><div class="cn" style="color:${c.col}">${c.name}</div><div class="ct">${c.trait}</div><div class="cb">⭐ ${c.bonus}</div>`;
    d.onclick=()=>{document.querySelectorAll('.ccard').forEach(el=>el.classList.remove('sel'));d.classList.add('sel');selChar=i;};
    g.appendChild(d);
  });
}

document.querySelectorAll('.tbtn').forEach(b=>{
  b.onclick=()=>{document.querySelectorAll('.tbtn').forEach(x=>x.classList.remove('a'));b.classList.add('a');selT=parseInt(b.dataset.t);};
});
document.getElementById('sbtn').onclick=()=>startGame(selChar,selT);
document.getElementById('rbtn').onclick=()=>{const p=G.players[G.cur];if(p&&!p.isBot&&!p.bkrt)doRoll(false);};

renderChars();
</script>
</body>
</html>"""

def render():
    import streamlit.components.v1 as _cv1
    from utils.core import sync_user_data
    from utils.database import load_db, save_db
    from utils.config import USERS_FILE

    qp = st.query_params
    if qp.get('marble_score'):
        try:
            uid = st.session_state.get('logged_in_user', '')
            m_score = int(qp.get('marble_score', 0))
            m_wins  = int(qp.get('marble_wins', 0))
            if uid and m_score > 0:
                _users = load_db(USERS_FILE, {})
                if uid in _users:
                    ms = _users[uid].setdefault('marble_stats', {
                        'wins': 0, 'losses': 0, 'games_played': 0, 'best_net_worth': 0
                    })
                    ms['games_played'] = ms.get('games_played', 0) + 1
                    ms['wins']         = ms.get('wins', 0) + m_wins
                    if m_score > ms.get('best_net_worth', 0):
                        ms['best_net_worth'] = m_score
                        st.toast(f"🏆 인베스트마블 최고 순자산 갱신! ₩{m_score:,}", icon="🌍")
                    _users[uid]['marble_stats'] = ms
                    save_db(USERS_FILE, _users)
                    st.session_state.marble_stats = ms
                    sync_user_data()
        except Exception:
            pass
        st.query_params.clear()
        st.rerun()

    st.markdown("""
    <style>
    #MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
    .block-container{padding:0 !important;max-width:100% !important;}iframe{border:none;}
    </style>
    """, unsafe_allow_html=True)

    listener_html = """
    <script>
    window.parent.addEventListener('message', function(e) {
      if (e.data && e.data.type === 'marble_result') {
        const url = new URL(window.parent.location.href);
        url.searchParams.set('marble_score', e.data.score);
        url.searchParams.set('marble_wins',  e.data.wins ?? 0);
        window.parent.location.href = url.toString();
      }
    });
    </script>
    """
    _cv1.html(listener_html, height=0)
    components.html(GAME_HTML, height=920, scrolling=True)

if __name__ == "__main__":
    render()
