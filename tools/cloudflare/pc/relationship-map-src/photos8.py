import sys, json, urllib.request, urllib.parse, base64, time, os
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
sys.path.insert(0, S)
from adds import ADDS
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
JA = {'Fumiaki Koizumi': '小泉文明', 'Shunya Kimura': '木村俊也', 'Kikuka Hanazawa': '花沢菊香'}
old = {}
for f in os.listdir(S):
    if f.startswith('outsiders') and f.endswith('.json'):
        try:
            old.update(json.load(open(os.path.join(S, f), encoding='utf-8')))
        except Exception:
            pass
names = {'Fumiaki Koizumi': 1, 'Shunya Kimura': 1, 'Kikuka Hanazawa': 1, 'John Lagerling': 1}
ja = {k: v for k, v in JA.items() if k in names}
en_list = [n for n in names if n not in old and n not in JA]
print(len(en_list), 'en;', len(ja), 'ja', flush=True)
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
for k, q in ja.items():
    try: one(k, 'ja', q)
    except Exception as e: print(k, 'ERR', e, flush=True)
    json.dump(out, open(S + r'\outsiders8.json', 'w', encoding='utf-8'), ensure_ascii=False)
for k in en_list:
    try: one(k, 'en', k)
    except Exception as e: print(k, 'ERR', e, flush=True)
    json.dump(out, open(S + r'\outsiders8.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('done', flush=True)
