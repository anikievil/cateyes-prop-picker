# 把 props.js 的每件道具轉成「灰底商品照」生圖提示詞，輸出 生圖清單.json（id → 提示詞），給批次生圖用。
# 用法：python3 生圖清單.py [只產還沒有圖的]
# 生好的圖存成 img/<id>.jpg，網頁就會自動顯示。
import json, re, sys, pathlib, subprocess

here = pathlib.Path(__file__).parent
js = (here / 'props.js').read_text(encoding='utf-8')
props = json.loads(subprocess.run(['node', '-e', js + ';console.log(JSON.stringify(PROPS))'],
                                  capture_output=True, text=True, check=True).stdout)

def prompt(p):
    if p['cat'] in ('桌面', '後景'):  # 材質類：拍滿版平面材質，不是單一物件
        return f"{p['name']}的材質特寫照片，平面填滿整個畫面，柔和均勻光線，{p['style']}風格，無文字、無物件、無人物。"
    return (f"{p['name']}，{p['style']}風格道具，單一物件置中，商品攝影，淺灰色無縫背景（#E9E6E1），"
            f"柔和頂光、底部有淡淡接觸陰影，約 30 度俯角，物件完整入鏡、四周留白，無文字、無 logo、無人物。")

only_missing = len(sys.argv) > 1
out = {p['id']: prompt(p) for p in props if not (only_missing and (here / 'img' / f"{p['id']}.jpg").exists())}
(here / '生圖清單.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(out), '件')
