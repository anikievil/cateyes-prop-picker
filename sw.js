// 離線快取：頁面與資料「先上網、失敗才用快取」（有網路時永遠拿到最新版）；道具圖「先用快取」（看過就能離線看）
// 改了 index.html／props.js 不用動這裡；只有 SHELL 清單變了才要改 VER
const VER = 'v2', SHELL = 'shell-' + VER, IMG = 'img-v1';
const FILES = ['./', 'index.html', 'props.js', 'manifest.json', 'icon-180.png', 'icon-192.png', 'icon-512.png', 'icon-512-maskable.png', 'favicon-32.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(SHELL).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('shell-') && k !== SHELL).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const u = new URL(e.request.url); if (e.request.method !== 'GET' || u.origin !== location.origin) return;
  if (u.pathname.includes('/img/')) {   // 道具圖：快取優先
    e.respondWith(caches.open(IMG).then(c => c.match(e.request).then(hit => hit || fetch(e.request).then(r => { if (r.ok) c.put(e.request, r.clone()); return r; }))));
    return;
  }
  e.respondWith(fetch(e.request).then(r => { if (r.ok) caches.open(SHELL).then(c => c.put(e.request, r.clone())); return r; })   // 頁面：網路優先
    .catch(() => caches.match(e.request, { ignoreSearch: true }).then(hit => hit || caches.match('index.html'))));
});
// 「下載全部道具圖」：頁面把圖片清單傳過來，逐張存進快取並回報進度
self.addEventListener('message', e => {
  if (!e.data || e.data.type !== 'cacheAll') return;
  const list = e.data.urls, src = e.source; let done = 0, fail = 0;
  caches.open(IMG).then(async c => {
    for (const url of list) {
      try { if (!(await c.match(url))) { const r = await fetch(url); if (r.ok) await c.put(url, r); else fail++; } } catch (err) { fail++; }
      if (++done % 20 === 0 || done === list.length) src.postMessage({ type: 'cacheProgress', done, total: list.length, fail });
    }
  });
});
