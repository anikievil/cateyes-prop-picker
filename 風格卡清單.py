# 風格牆用：每個風格組 3 套「桌面＋布料＋後景＋墊高＋容器×3＋餐具×2＋軟裝×2」，輸出 風格卡.json（id、各部件道具 id、提示詞）。
# 用法：python3 風格卡清單.py  → 風格卡.json；生好的卡存 img/card/<風格key>-<1~3>.jpg
import json, re, subprocess
NODE = r'''const fs=require("fs");const src=fs.readFileSync("props.js","utf8");
eval(src.replace(/^(const|let|var)\s+(STYLES|CATS|RAW|PROPS)\b/gm,"globalThis.$2").replace(/export\s+/g,""));
console.log(JSON.stringify({STYLES,PROPS}));'''
D = json.loads(subprocess.check_output(['node', '-e', NODE], text=True))
STYLES, PROPS = D['STYLES'], D['PROPS']
BY = {}
for p in PROPS: BY.setdefault((p['style'], p['cat']), []).append(p)
MOOD = {  # 一行講光線與色調，決定卡片氣氛
 'nordic':'極簡北歐、低飽和米白杏色，柔和窗光從左後方來','taiwan':'台式老屋懷舊、暖色午後光從木窗斜射，略帶復古色','korean':'韓系奶油色、柔霧白光、粉嫩低對比','blackgold':'暗調低調奢華，黑金墨綠三色，點光源從右後方低角度打來，金屬邊有亮邊、暗部不死黑',
 'wafu':'侘寂質感、深木色配靛藍，柔和側光從左方來','wenqing':'文青手作、生成色與淺木、柔和自然光帶一點暖','midautumn':'台灣中秋團圓感、暖黃月光調、低飽和','newyear':'台灣年節喜氣但收斂、暗紅配暖金、柔和暖光','hot':'乾淨百搭、淺灰白背景、柔和均勻光',
 'french':'法式復古、奶油白配淡金、午後斜陽','industrial':'工業風、深灰水泥與鐵件、硬一點的側光有明暗','xmas':'聖誕感靠深綠酒紅與黃銅、暖燭光氛圍、不加印花','valentine':'情人節、酒紅裸粉緞面、燭光柔焦','bubbletea':'台式茶飲店、明亮清爽、淺木與白、乾淨日光',
 'kissaten':'日系喫茶店、深木與暖黃燈、懷舊低飽和','tropical':'南洋島嶼、藤編與綠葉、明亮熱帶陽光','picnic':'春日野餐、草地綠意與格紋、明亮逆光','goose':'台灣小吃店的乾淨質樸感、低飽和、自然窗光從左後方來','rechao':'台式海產店、不鏽鋼與紅色點綴、明亮熱鬧',
 'izakaya':'日式居酒屋、深木與暖黃燈籠光、暗調','patisserie':'法式甜點店、白大理石與淡金、明亮柔光','onsen':'溫泉旅宿、檜木與石、靜謐暖光帶一點霧氣感','kbbq':'韓式餐桌、深色桌面與不鏽鋼、暖燈','diner':'美式漢堡店、紅白格與金屬、明亮硬光',
 'chachaanteng':'港式茶餐廳、磨石子與綠白磁磚、日光燈偏冷','italian':'義式小館、紅白格布與橄欖木、暖黃燭光','ramen':'日式食堂、深木吧檯與暖燈、暗調','pho':'越南小館、淺藍木與香草、明亮日光','brunch':'早午餐店、白磁磚與淺木、明亮晨光',
 'shaveice':'冰品店、淺色清爽、明亮柔光','teahouse':'中式茶館、深木與紫砂、安靜側光','steak':'牛排館、深色皮革與黑石、低調暖光','seaside':'海邊餐廳、白色刷舊木與藍、強烈海邊日光','mexican':'墨西哥餐館、赤陶與手織布、暖橘陽光',
 'thai':'溫暖柚木色配深綠與赭紅，暖色自然光從左後方斜射','bakery':'歐式鄉村廚房、白橡木與麵粉白、柔和晨光',
}
clean = lambda n: re.sub(r'（.*?）', '', n).strip()
def pick(st, cat, k, n=1):
    L = BY.get((st, cat), [])
    if not L: return []
    return [L[(k*3+i) % len(L)] for i in range(n)]
cards = []
for key, name in STYLES.items():
    for k in range(3):
        P = {c: pick(name, c, k, n) for c, n in [('桌面',1),('布料',1),('後景',1),('墊高',1),('容器',3),('餐具',2),('軟裝',2)]}
        g = lambda c, i=0: clean(P[c][i]['name']) if len(P[c]) > i else ''
        prompt = (f"{name}風格的餐桌情境展示照，直式 4:5，相機約 30 度俯角、中長焦。後景是{g('後景')}、微微失焦；桌面是{g('桌面')}；一條{g('布料')}斜鋪半張；"
                  f"左側一個{g('墊高')}當墊高，上面放一個空的{g('容器')}；前方中央一個空的{g('容器',1)}、旁邊一個空的{g('容器',2)}；{g('餐具')}和{g('餐具',1)}放在布巾旁；"
                  f"右後方{g('軟裝')}、{g('軟裝',1)}點綴。所有盤碗杯都是空的、沒有食物飲料。{MOOD.get(key,'低飽和、柔和自然光')}，影子柔和。"
                  f"商品陳列照、整潔有留白，無文字、無 logo、無人物。")
        cards.append({'id': f'{key}-{k+1}', 'style': key, 'name': name, 'parts': {c: [p['id'] for p in v] for c, v in P.items()}, 'prompt': prompt})
json.dump(cards, open('風格卡.json', 'w'), ensure_ascii=False, indent=0)
print(len(cards), '張卡 →', '風格卡.json')
