// 選物籃：三頁共用。內容＝localStorage 'propPick'.props（跟完整版的多選是同一份）
(function () {
  const KEY = 'propPick', SCENE = /桌面|布料|後景/, MAX = 7;
  const byId = {}; PROPS.forEach(p => byId[p.id] = p);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const read = () => { try { const o = JSON.parse(localStorage.getItem(KEY)); return o && typeof o === 'object' ? o : {}; } catch (e) { return {}; } };
  const write = o => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} };
  const fire = src => window.dispatchEvent(new CustomEvent('basket', { detail: { src: src || 'basket' } }));
  const B = window.Basket = {
    list() { const o = read(); return Array.isArray(o.props) ? o.props.filter(id => byId[id]) : []; },
    count() { return B.list().length; },
    propCount() { return B.list().filter(id => !SCENE.test(byId[id].cat)).length; },
    has(id) { return B.list().includes(id); },
    add(id) { if (!byId[id]) return; const o = read(), l = Array.isArray(o.props) ? o.props : []; if (!l.includes(id)) { o.props = [...l, id]; write(o); } fire(); },
    addMany(ids) { const o = read(), l = Array.isArray(o.props) ? o.props.slice() : []; ids.forEach(id => { if (byId[id] && !l.includes(id)) l.push(id); }); o.props = l; write(o); fire(); },
    remove(id) { const o = read(); o.props = (Array.isArray(o.props) ? o.props : []).filter(x => x !== id); write(o); fire(); },
    clear() { const o = read(); o.props = []; write(o); fire(); },
    refresh() { fire('save'); }   // 頁面自己存檔後呼叫，只通知籃子重畫
  };
  const css = `
#bk-fab{position:fixed;right:14px;bottom:84px;z-index:900;width:54px;height:54px;border-radius:50%;border:0;background:#1d1b19;color:#fff;box-shadow:0 4px 14px #0004;cursor:pointer;display:flex;align-items:center;justify-content:center;padding:0}
#bk-fab svg{width:26px;height:26px}
#bk-fab .n{position:absolute;top:-4px;right:-4px;min-width:22px;height:22px;border-radius:11px;background:#c9a46a;color:#1d1b19;font:700 12px/22px system-ui;text-align:center;padding:0 5px}
#bk-fab.over .n{background:#d33;color:#fff}
#bk-fab.bump{animation:bkb .5s}
@keyframes bkb{0%{transform:scale(1)}30%{transform:scale(1.35)}60%{transform:scale(.92)}100%{transform:scale(1)}}
.bk-mask{position:fixed;inset:0;background:#0006;z-index:950;display:none}.bk-mask.show{display:block}
.bk-dr{position:fixed;z-index:960;background:#fff;color:#1d1b19;display:none;flex-direction:column;left:0;right:0;bottom:0;height:80vh;border-radius:16px 16px 0 0;box-shadow:0 -6px 24px #0004;font-family:"Noto Sans TC","PingFang TC",system-ui,sans-serif}
.bk-dr.show{display:flex}
#bk-all{height:90vh;z-index:970}
@media(min-width:760px){.bk-dr{left:auto;top:0;height:100vh;width:420px;border-radius:0}#bk-all{height:100vh}}
.bk-hd{display:flex;align-items:center;gap:8px;padding:12px 14px;border-bottom:1px solid #e3ded6;flex-wrap:wrap}
.bk-hd b{font-size:16px}.bk-hd .warn{flex-basis:100%;color:#d33;font-size:12.5px;font-weight:600}
.bk-hd .sp{flex:1}
.bk-hd.over b{color:#d33}
.bk-x{border:0;background:none;font-size:22px;cursor:pointer;line-height:1;padding:4px 8px;color:inherit}
.bk-bd{flex:1;overflow-y:auto;overflow-x:hidden;padding:8px 14px}
.bk-row{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #f0ece6}
.bk-row img{width:52px;height:52px;object-fit:cover;border-radius:8px;background:#eee;flex:none}
.bk-row .t{flex:1;min-width:0}.bk-row .t b{display:block;font-size:14px}.bk-row .t small{color:#8a847b;font-size:12px}
.bk-row button{border:0;background:#f3efe9;border-radius:50%;width:32px;height:32px;cursor:pointer;font-size:15px;flex:none}
.bk-empty{color:#8a847b;text-align:center;padding:30px 0;font-size:14px}
.bk-ft{display:flex;gap:8px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));border-top:1px solid #e3ded6}
.bk-ft button,.bk-add{font:inherit;font-size:14px;border-radius:10px;border:1px solid #e3ded6;background:#fff;padding:10px 14px;cursor:pointer;color:inherit}
.bk-ft .pri{flex:1;background:#1d1b19;color:#fff;border-color:#1d1b19}
.bk-add{width:100%;margin:8px 0;border-style:dashed}
.bk-q{display:flex;flex-direction:column;gap:8px;padding:10px 14px;border-bottom:1px solid #e3ded6}
.bk-q input,.bk-q select{font:inherit;font-size:15px;padding:9px 10px;border:1px solid #e3ded6;border-radius:8px;width:100%;box-sizing:border-box}
.bk-cats{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none}.bk-cats::-webkit-scrollbar{display:none}
.bk-cats button{flex:none;border:1px solid #e3ded6;background:#fff;border-radius:999px;padding:6px 12px;font:inherit;font-size:13px;cursor:pointer}
.bk-cats button.on{background:#1d1b19;color:#fff;border-color:#1d1b19}
.bk-g{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
@media(min-width:760px){.bk-g{grid-template-columns:repeat(4,minmax(0,1fr))}}
.bk-c{position:relative;border:1px solid #e3ded6;border-radius:10px;overflow:hidden;background:#fff;cursor:pointer;padding:0;font:inherit;text-align:left;color:inherit}
.bk-c img{width:100%;aspect-ratio:1;object-fit:cover;display:block;background:#eee}
.bk-c span{display:block;font-size:12px;padding:4px 6px;line-height:1.3;min-height:32px}
.bk-c.on{border-color:#c9a46a;box-shadow:0 0 0 2px #c9a46a}
.bk-c.on::after{content:"✓";position:absolute;top:4px;right:4px;width:24px;height:24px;border-radius:50%;background:#c9a46a;color:#1d1b19;font-weight:700;text-align:center;line-height:24px}
`;
  const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  const mk = (tag, id, cls, html) => { const e = document.createElement(tag); if (id) e.id = id; if (cls) e.className = cls; if (html != null) e.innerHTML = html; document.body.appendChild(e); return e; };
  const fab = mk('button', 'bk-fab', '', '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 4h2.5l2.2 10.2a1.5 1.5 0 0 0 1.5 1.2h8.2a1.5 1.5 0 0 0 1.5-1.1L20.5 8H6.2"/><circle cx="9.5" cy="19.5" r="1.4"/><circle cx="17" cy="19.5" r="1.4"/></svg><span class="n">0</span>');
  fab.setAttribute('aria-label', '選物籃');
  const mask = mk('div', 'bk-mask', 'bk-mask'), dr = mk('div', 'bk-dr', 'bk-dr'), allDr = mk('div', 'bk-all', 'bk-dr');
  dr.innerHTML = `<div class="bk-hd" id="bk-hd"><b id="bk-t">0 件</b><span class="sp"></span><button class="bk-x" id="bk-close" aria-label="關閉">✕</button><span class="warn" id="bk-w" hidden>版面最多放 7 件道具，排版時只取前 7 件</span></div>
<div class="bk-bd"><div id="bk-rows"></div><button class="bk-add" id="bk-more">＋ 加道具</button></div>
<div class="bk-ft"><button id="bk-clear">清空</button><button class="pri" id="bk-go">去排版</button></div>`;
  allDr.innerHTML = `<div class="bk-hd"><b>全庫道具</b><span class="sp"></span><button class="bk-x" id="bk-aclose" aria-label="完成">完成</button></div>
<div class="bk-q"><input id="bk-s" type="search" placeholder="搜尋道具名稱"><div class="bk-cats" id="bk-cats"></div><select id="bk-st"><option value="">風格：全部</option></select></div>
<div class="bk-bd"><div class="bk-g" id="bk-g"></div></div>`;
  const $ = id => document.getElementById(id);
  const cats = ['全部', '容器', '餐具', '軟裝', '墊高', '桌面', '布料', '後景', '食材'];
  let aCat = '全部', aQ = '', aSt = '';
  $('bk-cats').innerHTML = cats.map(c => `<button data-c="${c}" class="${c === aCat ? 'on' : ''}">${c}</button>`).join('');
  [...new Set(PROPS.map(p => p.style))].forEach(s => { const o = document.createElement('option'); o.value = o.textContent = s; $('bk-st').appendChild(o); });
  const thumbImg = id => `<img loading="lazy" alt="" src="img/${id}.jpg" onerror="this.style.visibility='hidden'">`;
  function paintFab() {
    const n = B.count(), over = B.propCount() > MAX;
    fab.querySelector('.n').textContent = n; fab.classList.toggle('over', over);
  }
  function paintDr() {
    const l = B.list(), over = B.propCount() > MAX;
    $('bk-t').textContent = l.length + ' 件'; $('bk-hd').classList.toggle('over', over); $('bk-w').hidden = !over;
    $('bk-rows').innerHTML = l.length ? l.map(id => { const p = byId[id]; return `<div class="bk-row">${thumbImg(id)}<div class="t"><b>${esc(p.name)}</b><small>${esc(p.cat)}｜${esc(p.style)}</small></div><button data-rm="${id}" aria-label="移除 ${esc(p.name)}">✕</button></div>`; }).join('') : '<div class="bk-empty">籃子是空的，按下面「＋ 加道具」挑幾件。</div>';
  }
  function paintAll() {
    const q = aQ.trim(), l = PROPS.filter(p => (aCat === '全部' || p.cat === aCat) && (!aSt || p.style === aSt) && (!q || p.name.includes(q)));
    const sel = new Set(B.list());
    $('bk-g').innerHTML = l.map(p => `<button class="bk-c ${sel.has(p.id) ? 'on' : ''}" data-id="${p.id}">${thumbImg(p.id)}<span>${esc(p.name)}</span></button>`).join('') || '<div class="bk-empty" style="grid-column:1/-1">沒有符合的道具</div>';
  }
  let prevN = B.count();
  window.addEventListener('basket', e => {
    const n = B.count(); paintFab(); paintDr(); if (allDr.classList.contains('show')) { const y = allDr.querySelector('.bk-bd').scrollTop; paintAll(); allDr.querySelector('.bk-bd').scrollTop = y; }
    if (n > prevN) { fab.classList.remove('bump'); void fab.offsetWidth; fab.classList.add('bump'); }
    prevN = n;
  });
  window.addEventListener('storage', e => { if (e.key === KEY) fire('storage'); });
  const open = () => { paintDr(); mask.classList.add('show'); dr.classList.add('show'); };
  const closeAll = () => { dr.classList.remove('show'); allDr.classList.remove('show'); mask.classList.remove('show'); };
  fab.onclick = open; mask.onclick = closeAll; $('bk-close').onclick = closeAll;
  $('bk-more').onclick = () => { paintAll(); allDr.classList.add('show'); };
  $('bk-aclose').onclick = () => allDr.classList.remove('show');
  $('bk-rows').onclick = e => { const b = e.target.closest('[data-rm]'); if (b) B.remove(b.dataset.rm); };
  $('bk-g').onclick = e => { const b = e.target.closest('.bk-c'); if (!b) return; B.has(b.dataset.id) ? B.remove(b.dataset.id) : B.add(b.dataset.id); };
  $('bk-s').oninput = e => { aQ = e.target.value; paintAll(); };
  $('bk-cats').onclick = e => { const b = e.target.closest('button'); if (!b) return; aCat = b.dataset.c; [...$('bk-cats').children].forEach(x => x.classList.toggle('on', x === b)); paintAll(); };
  $('bk-st').onchange = e => { aSt = e.target.value; paintAll(); };
  $('bk-clear').onclick = () => { if (B.count() && confirm('確定清空籃子裡的 ' + B.count() + ' 件？')) B.clear(); };
  $('bk-go').onclick = () => { location.href = '快速.html'; };
  document.addEventListener('keydown', e => { if (e.key === 'Escape') { if (allDr.classList.contains('show')) allDr.classList.remove('show'); else closeAll(); } });
  paintFab();
})();
