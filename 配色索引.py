#!/usr/bin/env python3
"""建置腳本：讀 img/<id>.jpg，去掉灰底，算每件道具的主色（最多 3 色＋佔比），輸出 colors.json。
格式 {id: [[r,g,b,佔比%],...]}。需要 Pillow（pip install Pillow）。用法：python3 配色索引.py"""
import json, os, sys
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, 'img')
BG_DIST = 34      # 和四角底色的距離小於這個就當背景
MIN_PX = 0.02     # 主體像素太少（整張幾乎都是底）時，退回用全圖


def dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2) ** .5


def analyze(path):
    im = Image.open(path).convert('RGB')
    im.thumbnail((96, 96))
    w, h = im.size
    px = im.load()
    k = max(2, w // 12)
    corners = []
    for cx, cy in ((0, 0), (w-k, 0), (0, h-k), (w-k, h-k)):
        pts = [px[x, y] for x in range(cx, cx+k) for y in range(cy, cy+k)]
        corners.append(tuple(sum(c[i] for c in pts)//len(pts) for i in range(3)))
    bg = tuple(sum(sorted(c[i] for c in corners)[1:3])//2 for i in range(3))   # 四角各色中間兩值平均
    data = list(im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata())
    fg = [p for p in data if dist(p, bg) > BG_DIST]
    if len(fg) < w*h*MIN_PX:
        fg = data
    small = Image.new('RGB', (len(fg), 1))
    small.putdata(fg)
    q = small.quantize(colors=8, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()
    counts = sorted(q.getcolors(), reverse=True)   # (count, index)
    tot = sum(c for c, _ in counts)
    out = []
    for c, i in counts:
        rgb = pal[i*3:i*3+3]
        # 太接近已有顏色就併入
        for o in out:
            if dist(o[:3], rgb) < 28:
                o[3] += c
                break
        else:
            out.append([*rgb, c])
    out.sort(key=lambda o: -o[3])
    out = out[:3]
    s = sum(o[3] for o in out)
    return [[o[0], o[1], o[2], round(o[3]*100/s)] for o in out]


def main():
    res = {}
    files = sorted(f for f in os.listdir(IMG) if f.lower().endswith('.jpg'))
    for f in files:
        res[f[:-4]] = analyze(os.path.join(IMG, f))
    with open(os.path.join(HERE, 'colors.json'), 'w') as fh:
        json.dump(res, fh, ensure_ascii=False, separators=(',', ':'))
    print('img 張數', len(files), 'colors.json 筆數', len(res),
          '大小 KB', round(os.path.getsize(os.path.join(HERE, 'colors.json'))/1024, 1))


if __name__ == '__main__':
    main()
