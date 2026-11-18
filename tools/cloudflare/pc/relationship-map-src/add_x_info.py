"""x_people.py の人物について、Xのプロフィール画像(unavatar.io経由)を96pxに縮めて faces_x.json に、アカウントと自己紹介を x_info.json に保存する。"""
import base64, io, json, os, sys, time, urllib.parse, urllib.request
from PIL import Image
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from x_people import XP
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
fx = json.load(open(os.path.join(S, 'faces_x.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'faces_x.json')) else {}
for nm, (h, b) in XP.items():
    if nm in fx:
        continue
    try:
        by = None
        for _ in range(6):
            try:
                by = urllib.request.urlopen(urllib.request.Request('https://unavatar.io/x/' + urllib.parse.quote(h) + '?fallback=false', headers=UA), timeout=30).read()
                break
            except Exception as e:
                if '429' not in str(e):
                    raise
                time.sleep(45)
        im = Image.open(io.BytesIO(by)).convert('RGB')
        w, hh = im.size
        s = min(w, hh)
        im = im.crop(((w - s) // 2, 0 if hh > w else (hh - s) // 2, (w - s) // 2 + s, (0 if hh > w else (hh - s) // 2) + s)).resize((96, 96), Image.LANCZOS)
        o = io.BytesIO()
        im.save(o, 'JPEG', quality=68, optimize=True)
        fx[nm] = {'i': 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode(), 's': 'X(@' + h + ')', 'u': 'https://x.com/' + h}
        print('○', nm)
    except Exception as e:
        print('×', nm, str(e)[:60])
    time.sleep(6)
json.dump(fx, open(os.path.join(S, 'faces_x.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump({nm: {'h': h, 'b': b} for nm, (h, b) in XP.items()}, open(os.path.join(S, 'x_info.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(len(XP), len(fx))
