# 把 props.js 的每件道具轉成「灰底商品照」生圖提示詞，輸出 生圖清單.json（id → 提示詞），給批次生圖用。
# 用法：python3 生圖清單.py [只產還沒有圖的]
# 生好的圖存成 img/<id>.jpg，網頁就會自動顯示。
import json, re, sys, pathlib, subprocess

here = pathlib.Path(__file__).parent
js = (here / 'props.js').read_text(encoding='utf-8')
props = json.loads(subprocess.run(['node', '-e', js + ';console.log(JSON.stringify(PROPS))'],
                                  capture_output=True, text=True, check=True).stdout)

# 質感底線（10-30 使用者要求「避免太 low 沒格調」）：節慶風格 AI 會自己加印花、蝴蝶結、亮片，變廉價
TASTE = '設計極簡、高級精品質感、真實材質（陶、木、亞麻、黃銅、玻璃），低飽和配色，不加節慶印花、蝴蝶結、亮片或卡通圖案，不廉價、不塑膠感'

# 節慶要台灣在地感（10-30 使用者：「一定要改成台灣用法跟文字，不要中國感覺」）
TW = '，台灣在地生活感，不要中國大陸風格的大紅大金、流蘇、元寶、中國結'

def prompt(p):
    return base(p).replace('風格道具，', '風格道具' + TW + '，', 1) if p['style'].startswith('節慶') else base(p)

def base(p):
    if p['cat'] in ('桌面', '後景'):  # 材質類：拍滿版平面材質，不是單一物件
        return f"{p['name']}的材質特寫照片，平面填滿整個畫面，柔和均勻光線，{p['style']}風格，{TASTE}，無文字、無物件、無人物。"
    if p['cat'] == '布料':  # 不寫清楚 AI 會畫成袋子、髮圈、燈籠（10-30 實測）
        return (f"一塊{p['name']}，自然摺疊平放，只有布料本身（不是袋子、不是包包、不是燈籠、不是衣服），{p['style']}風格道具，{TASTE}，"
                f"置中，商品攝影，淺灰色無縫背景（#E9E6E1），柔和頂光、淡淡接觸陰影，約 30 度俯角，無文字、無 logo、無人物、無食物。")
    if p['cat'] in ('容器', '墊高'):  # 節慶風格 AI 會自己放月餅（10-30 實測）
        return (f"空的{p['name']}，上面完全沒有任何東西，{p['style']}風格道具，{TASTE}，單一物件置中，商品攝影，淺灰色無縫背景（#E9E6E1），"
                f"柔和頂光、底部有淡淡接觸陰影，約 30 度俯角，物件完整入鏡、四周留白，無文字、無 logo、無人物，沒有任何食物或點心。")
    # 只有這件東西：野餐、手搖風格會畫成整個場景或一杯飲料（10-30 實測）
    return (f"{p['name']}，只有這一件東西本身，不是場景、不是飲料、旁邊沒有其他物件，{p['style']}風格道具，{TASTE}，單一物件置中，商品攝影，淺灰色無縫背景（#E9E6E1），"
            f"柔和頂光、底部有淡淡接觸陰影，約 30 度俯角，物件完整入鏡、四周留白，無文字、無 logo、無人物。")

only_missing = len(sys.argv) > 1
out = {p['id']: prompt(p) for p in props if not (only_missing and (here / 'img' / f"{p['id']}.jpg").exists())}
(here / '生圖清單.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(out), '件')
