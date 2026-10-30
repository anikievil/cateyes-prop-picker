# 把生好的道具圖收進 img/：下載 → 縮到 800px → 存成 img/<id>.jpg，最後產一張總表方便檢查。
# 用法：python 收圖.py 清單.txt [總表.jpg]
#   清單.txt 每行「<道具id> <result_url>」（result_url 從 jobs_wait 結果抄下來）
# 需要 Pillow：沒有就 python3 -m venv <暫存>/venv && <暫存>/venv/bin/pip install Pillow
import sys, io, pathlib, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

here = pathlib.Path(__file__).parent
rows = [l.split() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
sheet = sys.argv[2] if len(sys.argv) > 2 else str(here / '收圖總表.jpg')

def get(row):
    pid, url = row
    try:
        im = Image.open(io.BytesIO(urllib.request.urlopen(url, timeout=60).read())).convert('RGB')
        im.thumbnail((800, 800)); im.save(here / 'img' / f'{pid}.jpg', quality=86)
    except Exception as e:
        return pid, str(e)[:60]

bad = [r for r in ThreadPoolExecutor(8).map(get, rows) if r]
ok = [pid for pid, _ in rows if pid not in {b[0] for b in bad}]
# 總表：每格 100px，12 格一排，給人眼檢查有沒有畫錯（布料變袋子、碟子多了食物、出現文字）
cols = 12; c = Image.new('RGB', (cols * 100, ((len(ok) - 1) // cols + 1) * 100 or 100), 'white')
for k, pid in enumerate(ok):
    c.paste(Image.open(here / 'img' / f'{pid}.jpg').resize((100, 100)), ((k % cols) * 100, (k // cols) * 100))
c.save(sheet, quality=90)
print(f'成功 {len(ok)} 張，失敗 {len(bad)}：{bad}\n總表：{sheet}')
