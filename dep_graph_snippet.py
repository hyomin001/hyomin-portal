# ==========================================================
# 효민 포털 — "시스템 공지 & 전체 아키텍처 구조 보기" expander 안에
# 그대로 붙여넣을 인터랙티브 의존성 그래프 스니펫
# 기존 app.py 의 다크 네온 테마 색상(--bg, --cyan, --text 등)을 그대로 사용
# ==========================================================

DEP_GRAPH_HTML = r"""
<div id="depgraph-root" style="background:#060a14;border:1px solid rgba(255,255,255,0.08);border-radius:14px;padding:18px;">
  <div style="color:#8899bb;font-size:0.85rem;margin-bottom:10px;">
    파일을 클릭하면 직접 연관된 파일이 강조됩니다. 다시 클릭하면 해제됩니다.
  </div>
  <div style="position:relative;width:100%;overflow:hidden;">
    <svg id="depsvg" width="100%" viewBox="0 0 680 1080" style="display:block;">
      <defs>
        <marker id="dg-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>
      <g id="dg-edgeLayer"></g>
      <g id="dg-nodeLayer"></g>
    </svg>
  </div>
  <div id="dg-infobox" style="margin-top:12px;font-size:0.85rem;color:#8899bb;min-height:20px;line-height:1.6;"></div>
  <div style="margin-top:14px;display:flex;gap:14px;flex-wrap:wrap;font-size:0.78rem;color:#8899bb;">
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#ff6b5b;margin-right:5px;"></span>진입점 (app.py)</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#c08fff;margin-right:5px;"></span>공유 핵심 (utils)</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#5dcaa5;margin-right:5px;"></span>일반 페이지</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#f2a623;margin-right:5px;"></span>미니게임 (games/sports)</span>
    <span><span style="display:inline-block;width:10px;height:10px;border-radius:3px;background:#888;margin-right:5px;"></span>독립 게임 (project_a~i)</span>
  </div>
</div>

<script>
(function() {
  const edges = [["app","pages.admin"],["app","utils.database"],["app","utils.core"],["app","utils.market_sync"],["app","pages"],["app","pages.games"],["app","pages.sports"],["app","utils.config"],["app","utils.css"],["pages.admin.panel","utils.core"],["pages.admin.panel","utils.database"],["pages.admin.panel","utils.config"],["pages.bank","utils.core"],["pages.bank","utils.database"],["pages.bank","utils.config"],["pages.clan","utils.core"],["pages.clan","utils.database"],["pages.clan","utils.config"],["pages.crypto","utils.core"],["pages.crypto","utils.database"],["pages.crypto","utils.config"],["pages.dm","utils.core"],["pages.dm","utils.database"],["pages.dm","utils.config"],["pages.games.blackjack","utils.database"],["pages.games.blackjack","utils.core"],["pages.games.forge","utils.core"],["pages.games.forge","utils.database"],["pages.games.forge","utils.config"],["pages.games.gacha","utils.database"],["pages.games.gacha","utils.core"],["pages.games.holdem","utils.core"],["pages.games.holdem","utils.database"],["pages.games.holdem","utils.config"],["pages.games.lotto","utils.database"],["pages.games.lotto","utils.core"],["pages.games.mine","utils.database"],["pages.games.mine","utils.core"],["pages.games.mine","utils.config"],["pages.games.quiz","utils.database"],["pages.games.quiz","utils.core"],["pages.games.slot","utils.core"],["pages.games.slot","utils.database"],["pages.games.slot","utils.config"],["pages.home","utils.database"],["pages.home","utils.core"],["pages.home","utils.config"],["pages.pet","utils.core"],["pages.pet","utils.database"],["pages.pet","utils.config"],["pages.profile","utils.core"],["pages.profile","utils.database"],["pages.profile","pages.pet"],["pages.profile","utils.config"],["pages.project_b","utils.database"],["pages.project_b","utils.config"],["pages.project_c","utils.core"],["pages.project_c","utils.database"],["pages.project_c","utils.config"],["pages.project_d","utils.database"],["pages.project_d","utils.config"],["pages.project_e","utils.core"],["pages.project_e","utils.database"],["pages.project_e","utils.config"],["pages.project_f","utils.database"],["pages.project_f","utils.config"],["pages.project_g","utils.database"],["pages.project_g","utils.config"],["pages.project_h","utils.database"],["pages.project_h","utils.config"],["pages.project_i","utils.database"],["pages.project_i","utils.config"],["pages.quest","utils.database"],["pages.quest","utils.core"],["pages.quest","utils.config"],["pages.ranking","utils.core"],["pages.ranking","utils.database"],["pages.ranking","utils.config"],["pages.real_estate","utils.database"],["pages.real_estate","utils.core"],["pages.real_estate","utils.config"],["pages.sports.garage","utils.database"],["pages.sports.garage","utils.core"],["pages.sports.garage","utils.config"],["pages.sports.penalty","utils.database"],["pages.sports.penalty","utils.core"],["pages.sports.racing","utils.core"],["pages.sports.racing","utils.database"],["pages.sports.racing","utils.config"],["pages.sports.soccer_sim","utils.database"],["pages.sports.soccer_sim","utils.core"],["pages.stock","utils.core"],["pages.stock","utils.database"],["pages.stock","utils.config"],["pages.title_shop","utils.config"],["pages.title_shop","utils.database"],["pages.title_shop","utils.core"],["pages.txlog","utils.core"],["pages.txlog","utils.database"],["pages.txlog","utils.config"],["pages.vip","utils.database"],["pages.vip","utils.core"],["pages.vip","utils.config"],["utils.core","utils.database"],["utils.core","utils.config"],["utils.database","utils.config"],["utils.market_sync","utils.database"],["utils.market_sync","utils.core"],["utils.market_sync","utils.config"]];

  const layout = {
    'app': [340, 40],
    'utils.config': [120, 130], 'utils.database': [280, 130], 'utils.core': [440, 130], 'utils.market_sync': [600, 130],
    'utils.css': [600, 40],
    'pages.home': [50, 240], 'pages.bank': [150, 240], 'pages.stock': [250, 240], 'pages.crypto': [350, 240],
    'pages.real_estate': [450, 240], 'pages.clan': [550, 240], 'pages.dm': [50, 290], 'pages.quest': [150, 290],
    'pages.ranking': [250, 290], 'pages.title_shop': [350, 290], 'pages.txlog': [450, 290], 'pages.vip': [550, 290],
    'pages.profile': [200, 340], 'pages.pet': [400, 340],
    'pages.admin.panel': [340, 400],
    'pages.games.slot': [50, 460], 'pages.games.blackjack': [150, 460], 'pages.games.holdem': [250, 460],
    'pages.games.mine': [350, 460], 'pages.games.lotto': [450, 460], 'pages.games.forge': [550, 460],
    'pages.games.gacha': [50, 510], 'pages.games.quiz': [150, 510],
    'pages.sports.soccer_sim': [300, 510], 'pages.sports.penalty': [400, 510],
    'pages.sports.racing': [500, 510], 'pages.sports.garage': [600, 510],
    'pages.project_a': [40, 600], 'pages.project_b': [130, 600], 'pages.project_c': [220, 600],
    'pages.project_d': [310, 600], 'pages.project_e': [400, 600], 'pages.project_f': [490, 600],
    'pages.project_g': [580, 600], 'pages.project_h': [130, 650], 'pages.project_i': [310, 650],
  };

  const labels = {
    'app':'app.py','utils.config':'config.py','utils.database':'database.py','utils.core':'core.py',
    'utils.market_sync':'market_sync.py','utils.css':'css.py',
    'pages.home':'home.py','pages.bank':'bank.py','pages.stock':'stock.py','pages.crypto':'crypto.py',
    'pages.real_estate':'real_estate.py','pages.clan':'clan.py','pages.dm':'dm.py','pages.quest':'quest.py',
    'pages.ranking':'ranking.py','pages.title_shop':'title_shop.py','pages.txlog':'txlog.py','pages.vip':'vip.py',
    'pages.profile':'profile.py','pages.pet':'pet.py','pages.admin.panel':'admin/panel.py',
    'pages.games.slot':'slot.py','pages.games.blackjack':'blackjack.py','pages.games.holdem':'holdem.py',
    'pages.games.mine':'mine.py','pages.games.lotto':'lotto.py','pages.games.forge':'forge.py',
    'pages.games.gacha':'gacha.py','pages.games.quiz':'quiz.py',
    'pages.sports.soccer_sim':'soccer_sim.py','pages.sports.penalty':'penalty.py',
    'pages.sports.racing':'racing.py','pages.sports.garage':'garage.py',
    'pages.project_a':'project_a.py','pages.project_b':'project_b.py','pages.project_c':'project_c.py',
    'pages.project_d':'project_d.py','pages.project_e':'project_e.py','pages.project_f':'project_f.py',
    'pages.project_g':'project_g.py','pages.project_h':'project_h.py','pages.project_i':'project_i.py',
  };

  const isUtil = m => m.startsWith('utils.');
  const isGame = m => m.startsWith('pages.games.') || m.startsWith('pages.sports.');
  const isProject = m => m.startsWith('pages.project_');
  const isApp = m => m === 'app';

  function colorFor(m) {
    if (isApp(m)) return { fill: 'rgba(255,107,91,0.12)', stroke: '#ff6b5b', text: '#ff8a7a' };
    if (isUtil(m)) return { fill: 'rgba(192,143,255,0.12)', stroke: '#c08fff', text: '#d2aeff' };
    if (isGame(m)) return { fill: 'rgba(242,166,35,0.12)', stroke: '#f2a623', text: '#ffc14d' };
    if (isProject(m)) return { fill: 'rgba(136,136,136,0.12)', stroke: '#888888', text: '#aaaaaa' };
    return { fill: 'rgba(93,202,165,0.12)', stroke: '#5dcaa5', text: '#7fdbb9' };
  }

  const allNodes = Object.keys(layout);
  const neighbors = {};
  allNodes.forEach(n => neighbors[n] = new Set());
  edges.forEach(([a,b]) => { if (neighbors[a] && neighbors[b]) { neighbors[a].add(b); neighbors[b].add(a); } });

  const svgns = 'http://www.w3.org/2000/svg';
  const edgeLayer = document.getElementById('dg-edgeLayer');
  const nodeLayer = document.getElementById('dg-nodeLayer');
  const infobox = document.getElementById('dg-infobox');
  let selected = null;

  function nodeSize(m) {
    const label = labels[m];
    const w = Math.max(64, label.length * 6.6 + 16);
    return [w, 28];
  }

  const edgeEls = [];
  edges.forEach(([a,b]) => {
    if (!layout[a] || !layout[b]) return;
    const [x1,y1] = layout[a], [x2,y2] = layout[b];
    const line = document.createElementNS(svgns,'line');
    line.setAttribute('x1', x1); line.setAttribute('y1', y1);
    line.setAttribute('x2', x2); line.setAttribute('y2', y2);
    line.setAttribute('stroke', 'rgba(255,255,255,0.12)');
    line.setAttribute('stroke-width', '0.7');
    edgeLayer.appendChild(line);
    edgeEls.push({a, b, el: line});
  });

  const nodeEls = {};
  allNodes.forEach(m => {
    const [x,y] = layout[m];
    const [w,h] = nodeSize(m);
    const c = colorFor(m);
    const g = document.createElementNS(svgns,'g');
    g.style.cursor = 'pointer';
    const rect = document.createElementNS(svgns,'rect');
    rect.setAttribute('x', x - w/2); rect.setAttribute('y', y - h/2);
    rect.setAttribute('width', w); rect.setAttribute('height', h);
    rect.setAttribute('rx', 7);
    rect.setAttribute('fill', c.fill);
    rect.setAttribute('stroke', c.stroke);
    rect.setAttribute('stroke-width', '1');
    const text = document.createElementNS(svgns,'text');
    text.setAttribute('x', x); text.setAttribute('y', y);
    text.setAttribute('text-anchor','middle'); text.setAttribute('dominant-baseline','central');
    text.setAttribute('font-size', '12');
    text.setAttribute('font-family', 'inherit');
    text.setAttribute('fill', c.text);
    text.textContent = labels[m];
    g.appendChild(rect); g.appendChild(text);
    g.addEventListener('click', () => selectNode(m));
    nodeLayer.appendChild(g);
    nodeEls[m] = { g, rect };
  });

  function resetStyles() {
    Object.values(nodeEls).forEach(({g}) => { g.style.opacity = '1'; });
    edgeEls.forEach(({el}) => {
      el.setAttribute('stroke', 'rgba(255,255,255,0.12)');
      el.setAttribute('stroke-width', '0.7');
      el.removeAttribute('marker-end');
      el.style.opacity = '1';
    });
  }

  function selectNode(m) {
    if (selected === m) { selected = null; resetStyles(); infobox.textContent = ''; return; }
    selected = m;
    resetStyles();
    const ns = neighbors[m];
    allNodes.forEach(n => { if (n !== m && !ns.has(n)) nodeEls[n].g.style.opacity = '0.22'; });
    edgeEls.forEach(({a, b, el}) => {
      if (a === m || b === m) {
        el.setAttribute('stroke', '#00d4ff');
        el.setAttribute('stroke-width', '1.8');
        el.setAttribute('marker-end', 'url(#dg-arrow)');
        el.style.opacity = '1';
      } else {
        el.style.opacity = '0.12';
      }
    });
    const downstream = edges.filter(([a,b]) => a === m).map(([,b]) => labels[b]);
    const upstream = edges.filter(([a,b]) => b === m).map(([a]) => labels[a]);
    const parts = [];
    if (downstream.length) parts.push('이 파일이 가져다 쓰는 것: ' + downstream.join(', '));
    if (upstream.length) parts.push('이 파일을 가져다 쓰는 것: ' + upstream.join(', '));
    infobox.innerHTML = '<b style="color:#00d4ff;">' + labels[m] + '</b> — ' + (parts.join(' / ') || '다른 모듈과 직접 연결 없음');
  }
})();
</script>
"""
