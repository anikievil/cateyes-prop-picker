// 配色工具：index.html（丟參考圖選物）和 風格範例.html（搭配範例）共用。純計算，不上傳任何東西。
// 顏色資料來自 colors.json（配色索引.py 建置）：{id: [[r,g,b,佔比%],...]}
const PC = (() => {
  const lin = v => ((v /= 255) <= .04045 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4));
  const f = t => (t > .008856 ? Math.cbrt(t) : 7.787 * t + 16 / 116);
  function lab(r, g, b) {
    r = lin(r); g = lin(g); b = lin(b);
    const x = f((r * .4124 + g * .3576 + b * .1805) / .95047), y = f(r * .2126 + g * .7152 + b * .0722), z = f((r * .0193 + g * .1192 + b * .9505) / 1.08883);
    return [116 * y - 16, 500 * (x - y), 200 * (y - z)];
  }
  const d = (a, b) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2]);
  const hex = (r, g, b) => '#' + [r, g, b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const chroma = l => Math.hypot(l[1], l[2]);
  const hue = l => (Math.atan2(l[2], l[1]) * 180 / Math.PI + 360) % 360;
  const hueDiff = (a, b) => { const x = Math.abs(hue(a) - hue(b)); return x > 180 ? 360 - x : x; };

  // 簡單 k-means（固定起點，同一張圖每次結果一樣）。pixels：[[r,g,b],...]
  function kmeans(pixels, k = 5, iters = 12) {
    const P = pixels.map(p => ({ rgb: p, lab: lab(p[0], p[1], p[2]) }));
    const mean = [0, 1, 2].map(i => P.reduce((s, p) => s + p.lab[i], 0) / P.length);
    let cs = [P.reduce((b, p) => (d(p.lab, mean) < d(b.lab, mean) ? p : b)).lab];
    while (cs.length < k) {   // 最遠點優先挑起點
      let best = null, bd = -1;
      for (const p of P) { const m = Math.min(...cs.map(c => d(p.lab, c))); if (m > bd) { bd = m; best = p; } }
      cs.push(best.lab);
    }
    let asg = new Array(P.length).fill(0);
    for (let it = 0; it < iters; it++) {
      P.forEach((p, i) => { let bi = 0, bd = 1e9; cs.forEach((c, j) => { const x = d(p.lab, c); if (x < bd) { bd = x; bi = j; } }); asg[i] = bi; });
      cs = cs.map((c, j) => { const m = P.filter((_, i) => asg[i] === j); return m.length ? [0, 1, 2].map(t => m.reduce((s, p) => s + p.lab[t], 0) / m.length) : c; });
    }
    return cs.map((c, j) => {
      const m = P.filter((_, i) => asg[i] === j);
      if (!m.length) return null;
      const rgb = [0, 1, 2].map(t => Math.round(m.reduce((s, p) => s + p.rgb[t], 0) / m.length));
      return { lab: c, rgb, hex: hex(...rgb), w: m.length / P.length };
    }).filter(Boolean).sort((a, b) => b.w - a.w);
  }

  let COL = {};
  const load = () => fetch('colors.json').then(r => r.json()).then(j => { COL = {}; for (const id in j) COL[id] = j[id].map(([r, g, b, w]) => ({ rgb: [r, g, b], lab: lab(r, g, b), hex: hex(r, g, b), w: w / 100 })); return COL; });
  const pal = id => COL[id] || [];
  const main = id => pal(id)[0];

  // 道具色盤和參考色盤的距離（越小越搭）：雙向加權最近色距離
  function dist(a, b) {
    if (!a.length || !b.length) return 1e3;
    const one = (x, y) => x.reduce((s, c) => s + c.w * Math.min(...y.map(o => d(c.lab, o.lab))), 0) / x.reduce((s, c) => s + c.w, 0);
    return (one(a, b) + one(b, a)) / 2;
  }
  return { lab, d, hex, chroma, hue, hueDiff, kmeans, load, pal, main, dist };
})();
