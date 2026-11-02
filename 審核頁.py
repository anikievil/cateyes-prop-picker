# 本機點選審核頁（2026-11-02）：新生的道具圖一件一件點「保留／刪除／重生」、改名、每風格新增，按「複製結果」貼回對話。
# 用法：python3 審核頁.py 輸出.html [cat=食材] [styles=rechao,izakaya] [ids=清單.txt]   （條件可混用；沒給就全部）
# 只在本機開（file://），不進 git。
import json, subprocess, pathlib, sys
here = pathlib.Path(__file__).parent
js = (here / 'props.js').read_text(encoding='utf-8')
props = json.loads(subprocess.run(['node', '-e', js + ';console.log(JSON.stringify({P:PROPS,S:STYLES}))'], capture_output=True, text=True, check=True).stdout)
P, ST = props['P'], props['S']
out = pathlib.Path(sys.argv[1]); opt = dict(a.split('=', 1) for a in sys.argv[2:])
if 'cat' in opt: P = [p for p in P if p['cat'] == opt['cat']]
if 'styles' in opt: P = [p for p in P if p['id'].split('-')[0] in opt['styles'].split(',')]
if 'ids' in opt: keep = {l.split()[0] for l in open(opt['ids'], encoding='utf-8') if l.strip()}; P = [p for p in P if p['id'] in keep]
IMG = (here / 'img').resolve()
data = [{'id': p['id'], 'st': ST.get(p['id'].split('-')[0], p['id'].split('-')[0]), 'cat': p['cat'], 'name': p['name'], 'img': f'file://{IMG}/{p["id"]}.jpg'} for p in P]
page = '''<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>道具審核</title>
<style>body{margin:0;font-family:system-ui;background:#f4f2ee;color:#222}header{position:sticky;top:0;background:#1d1b19;color:#fff;padding:10px 16px;display:flex;gap:12px;align-items:center;z-index:5}
header button{margin-left:auto;background:#c9a46a;border:0;border-radius:999px;padding:8px 16px;font-weight:700;cursor:pointer}
h2{margin:20px 16px 6px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;padding:0 16px}
.c{background:#fff;border:1px solid #e3ded6;border-radius:10px;padding:8px}.c img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:6px}
.c .n{font-size:13px;margin:6px 0 4px}.c input{width:100%;box-sizing:border-box;font:inherit;font-size:13px;padding:4px 6px;border:1px solid #ddd;border-radius:6px;margin-bottom:6px}
.b{display:flex;gap:4px}.b button{flex:1;border:1px solid #ccc;background:#fff;border-radius:6px;padding:5px 0;font-size:13px;cursor:pointer}
.b button.on{background:#1d1b19;color:#fff;border-color:#1d1b19}.c.del{opacity:.45}.c.re{outline:2px solid #e9b44c}
#zoom{position:fixed;top:60px;right:16px;width:min(560px,45vw);aspect-ratio:1;background:#fff;border:1px solid #ccc;border-radius:12px;box-shadow:0 8px 30px rgba(0,0,0,.25);display:none;z-index:9;pointer-events:none;overflow:hidden}#zoom img{width:100%;height:100%;object-fit:contain}#zoom div{position:absolute;left:0;right:0;bottom:0;background:rgba(0,0,0,.6);color:#fff;font-size:13px;padding:6px 10px}
textarea{width:calc(100% - 32px);margin:8px 16px 20px;box-sizing:border-box;font:inherit;font-size:13px;padding:8px;border:1px solid #ddd;border-radius:8px;min-height:60px}</style>
<header><b>道具審核（__N__ 件）</b><span id="sum"></span><button id="cp">複製結果</button></header>
<p style="margin:10px 16px;font-size:13px;color:#666">每件點「保留／刪除／重生」，要改名直接在框裡打新品名（含尺寸），下一格寫修改內容（例：不要蛋和牛奶、顏色要深一點）；每個風格下方可打「新增」，一行一件：品名｜尺寸。答案自動存在這台電腦，填完按右上「複製結果」貼回對話。</p>
<div id="root"></div><div id="zoom"><img><div></div></div>
<script>
const D=__DATA__,KEY='review_'+__KEY__;let S={};try{S=JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){}};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function render(){const sts=[...new Set(D.map(d=>d.st))];document.getElementById('root').innerHTML=sts.map(st=>`<h2>${st}</h2><div class="grid">${D.filter(d=>d.st===st).map((d,i)=>{const v=S[d.id]||{};return `<div class="c ${v.a==='刪除'?'del':v.a==='重生'?'re':''}" data-id="${d.id}"><img src="${d.img}" loading="lazy"><div class="n">${String(i+1).padStart(2,'0')} ${esc(d.cat)}｜${esc(d.name)}</div><input data-f="t" placeholder="改名（品名｜尺寸）" value="${esc(v.t||'')}"><input data-f="m" placeholder="修改內容（要怎麼改／不要什麼）" value="${esc(v.m||'')}"><div class="b">${['保留','刪除','重生'].map(a=>`<button data-a="${a}" class="${(v.a||'保留')===a?'on':''}">${a}</button>`).join('')}</div></div>`}).join('')}</div><textarea data-add="${st}" placeholder="${st} 新增（一行一件：品名｜尺寸）">${esc(S['+'+st]||'')}</textarea>`).join('');sum()}
function sum(){const n=Object.values(S).filter(v=>v&&v.a==='刪除').length,r=Object.values(S).filter(v=>v&&v.a==='重生').length,c=Object.values(S).filter(v=>v&&v.t).length,m=Object.values(S).filter(v=>v&&v.m).length;document.getElementById('sum').textContent=`刪除 ${n}｜重生 ${r}｜改名 ${c}｜修改 ${m}`}
document.addEventListener('click',e=>{const b=e.target.closest('button[data-a]');if(!b)return;const id=b.closest('.c').dataset.id;S[id]=S[id]||{};S[id].a=b.dataset.a;save();render()});
document.addEventListener('input',e=>{if(e.target.dataset.add){S['+'+e.target.dataset.add]=e.target.value;save();return}const c=e.target.closest('.c');if(!c)return;S[c.dataset.id]=S[c.dataset.id]||{};S[c.dataset.id][e.target.dataset.f||'t']=e.target.value.trim();save();sum()});
document.getElementById('cp').onclick=e=>{const L=['【道具審核結果】'];D.forEach(d=>{const v=S[d.id]||{};if(v.a==='刪除')L.push(`${d.id} 刪除`);else if(v.a==='重生')L.push(`${d.id} 重生${v.t?'→'+v.t:''}${v.m?'｜修改：'+v.m:''}`);else if(v.t||v.m)L.push(`${d.id}${v.t?' 改名→'+v.t:''}${v.m?' 修改：'+v.m:''}`)});Object.keys(S).filter(k=>k[0]==='+'&&S[k].trim()).forEach(k=>L.push(`${k.slice(1)} 新增：`+S[k].trim().split('\\n').join('；')));const t=L.join('\\n');navigator.clipboard.writeText(t).then(()=>e.target.textContent='已複製 ✓ 貼回對話',()=>prompt('複製這段：',t))};
const Z=document.getElementById('zoom');document.addEventListener('mouseover',e=>{const c=e.target.closest('.c');if(!c||e.target.tagName!=='IMG')return;const d=D.find(x=>x.id===c.dataset.id);Z.querySelector('img').src=d.img;Z.querySelector('div').textContent=d.st+'｜'+d.cat+'｜'+d.name;Z.style.display='block';const r=c.getBoundingClientRect();Z.style.right=r.left>innerWidth/2?'auto':'16px';Z.style.left=r.left>innerWidth/2?'16px':'auto'});document.addEventListener('mouseout',e=>{if(e.target.tagName==='IMG'&&e.target.closest('.c'))Z.style.display='none'});
render();
</script>'''.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__N__', str(len(data))).replace('__KEY__', json.dumps(out.stem))
out.write_text(page, encoding='utf-8'); print('產生', out, len(data), '件（用 open 開）')
