import sys, json, urllib.request, urllib.parse, base64, re, time
sys.path.insert(0, r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src')
from personal_data import P
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
main = set(P.keys())
names = {}
for k, rows in P.items():
    for g, rel, en, jp, desc in rows:
        if g != 'org' and en not in main:
            names[en] = jp
print(len(names), 'outsiders', flush=True)
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
for en in names:
    time.sleep(2.5)
    try:
        u = ('https://en.wikipedia.org/w/api.php?action=query&format=json&generator=search&gsrlimit=1&gsrsearch=' + urllib.parse.quote(en)
             + '&prop=pageimages|description&piprop=thumbnail&pithumbsize=120')
        d = get(u)
        pg = list(d.get('query', {}).get('pages', {}).values())
        if not pg:
            print(en, '| no result', flush=True); continue
        pg = pg[0]
        title = pg.get('title'); desc = pg.get('description'); th = pg.get('thumbnail', {}).get('source')
        img = None
        if th:
            time.sleep(2)
            b = get(th, raw=True)
            if b[:3] == b'\xff\xd8\xff' or b[:4] == b'\x89PNG':
                img = 'data:%s;base64,%s' % ('image/jpeg' if b[:2] == b'\xff\xd8' else 'image/png', base64.b64encode(b).decode())
        out[en] = {'title': title, 'desc': desc, 'img': img, 'wiki': 'https://en.wikipedia.org/wiki/' + urllib.parse.quote((title or '').replace(' ', '_'))}
        print(en, '|', title, '|', desc, '|', bool(img), flush=True)
    except Exception as e:
        print(en, '| ERR', e, flush=True)
    json.dump(out, open(S + r'\outsiders.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('done', flush=True)
