import sys, json, urllib.request, urllib.parse, base64, time, os
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
sys.path.insert(0, S)
from personal_data6 import P6
from newco_data5 import CO5
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
JA = {'Naoki Aoyagi': '青柳直樹', 'Shintaro Yamada': '山田進太郎', 'Kenichiro Kawanabe': '川鍋一朗', 'Hiroshi Nakajima': '中島宏', 'Tomoko Namba': '南場智子',
      'Satoshi Yano': '矢野哲', 'Hideo Fujii': '藤井英雄', 'Shintaro Nakagawa': '中川晋太郎', 'Yulia Brovkina': 'ユリア・ブロヴキナ'}
old = {}
for f in ('outsiders.json', 'outsiders2.json', 'outsiders3.json', 'outsiders4.json', 'outsiders5.json'):
    p = os.path.join(S, f)
    if os.path.exists(p):
        old.update(json.load(open(p, encoding='utf-8')))
people0 = {p[0] for p in json.load(open(S + r'\people.json', encoding='utf-8'))}
allkeys = set(P6)
names = {}
for c in CO5.values():
    for en in c['EN'].values():
        if en not in people0 and en not in JA:
            names[en] = 1
for rows in P6.values():
    for g, rel, en, jp, desc in rows:
        if g != 'org' and en not in allkeys and en not in JA:
            names[en] = 1
en_list = [n for n in names if n not in old]
print(len(en_list), 'en to fetch;', len(JA), 'ja', flush=True)
def get(u, raw=False):
    for i in range(6):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read()
            return b if raw else json.loads(b)
        except Exception as e:
            if '429' in str(e):
                time.sleep(8 * (i + 1))
            else:
                raise
out = {}
def one(key, lang, q):
    time.sleep(2.5)
    u = ('https://%s.wikipedia.org/w/api.php?action=query&format=json&generator=search&gsrlimit=1&gsrsearch=%s&prop=pageimages|extracts&piprop=thumbnail&pithumbsize=120&exintro=1&explaintext=1&exchars=70'
         % (lang, urllib.parse.quote(q)))
    d = get(u)
    pg = list(d.get('query', {}).get('pages', {}).values())
    if not pg:
        print(key, '| no result', flush=True); return
    pg = pg[0]
    title = pg.get('title'); ex = (pg.get('extract') or '').replace('\n', ' '); th = pg.get('thumbnail', {}).get('source')
    img = None
    if th:
        time.sleep(2)
        b = get(th, raw=True)
        if b[:3] == b'\xff\xd8\xff' or b[:4] == b'\x89PNG':
            img = 'data:%s;base64,%s' % ('image/jpeg' if b[:2] == b'\xff\xd8' else 'image/png', base64.b64encode(b).decode())
    out[key] = {'title': title, 'desc': ex, 'img': img, 'wiki': 'https://%s.wikipedia.org/wiki/%s' % (lang, urllib.parse.quote((title or '').replace(' ', '_')))}
    print(key, '|', title, '|', ex, '|', bool(img), flush=True)
for k, q in JA.items():
    try: one(k, 'ja', q)
    except Exception as e: print(k, 'ERR', e, flush=True)
    json.dump(out, open(S + r'\outsiders6.json', 'w', encoding='utf-8'), ensure_ascii=False)
for k in en_list:
    try: one(k, 'en', k)
    except Exception as e: print(k, 'ERR', e, flush=True)
    json.dump(out, open(S + r'\outsiders6.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('done', flush=True)
