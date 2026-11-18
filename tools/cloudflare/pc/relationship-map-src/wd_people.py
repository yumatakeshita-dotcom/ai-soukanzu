import urllib.request, urllib.parse, json, time
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
people = json.loads(open(S + r'\people.json', encoding='utf-8').read())
extra_q = {'Wojciech Zaremba': 'Q27733815', 'Mark Chen': 'Q126287485', 'John Schulman': 'Q103236782', 'Daniela Amodei': 'Q119721378', 'Jan Leike': 'Q123130693',
           'Helen Toner': 'Q123475976', 'Caitlin Kalinowski': 'Q27449525', 'Joshua Achiam': 'Q126287494', 'Jack Clark': 'Q135111322', 'Chris Olah': 'Q50358648',
           'Sam McCandlish': 'Q105285886', 'Durk Kingma': 'Q29022624', 'Vas Narasimhan': 'Q115735786', 'Chris Liddell': 'Q5107236'}
def get(u):
    for i in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
        except Exception as e:
            if '429' in str(e):
                time.sleep(6 * (i + 1))
            else:
                raise
# 1) wiki title -> qid
qid = dict(extra_q)
titles = {p[0]: urllib.parse.unquote(p[2]) for p in people if p[2]}
items = list(titles.items())
for i in range(0, len(items), 40):
    chunk = items[i:i + 40]
    u = 'https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1&prop=pageprops&ppprop=wikibase_item&titles=' + urllib.parse.quote('|'.join(t for _, t in chunk))
    d = get(u)
    tmap = {}
    for n in d.get('query', {}).get('normalized', []): tmap[n['to']] = n['from']
    rmap = {r['to']: r['from'] for r in d.get('query', {}).get('redirects', [])}
    for pg in d['query']['pages'].values():
        q = pg.get('pageprops', {}).get('wikibase_item')
        t = pg.get('title')
        src = rmap.get(t, t)
        src = tmap.get(src, src)
        for name, tt in chunk:
            if tt.replace('_', ' ') == src or tt == src or tt.replace('_', ' ') == t:
                if q: qid[name] = q
    time.sleep(2)
print('qids', len(qid), flush=True)
props = ['P26', 'P451', 'P22', 'P25', 'P3373', 'P1038', 'P184', 'P185', 'P1066', 'P802', 'P69']
data = {}
names = list(qid.items())
targets = set()
for i in range(0, len(names), 40):
    chunk = names[i:i + 40]
    d = get('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims&ids=' + '|'.join(q for _, q in chunk))
    for name, q in chunk:
        cl = d['entities'][q].get('claims', {})
        rec = {}
        for p in props:
            vals = []
            for c in cl.get(p, []):
                v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
                if isinstance(v, dict) and 'id' in v:
                    vals.append(v['id']); targets.add(v['id'])
            if vals: rec[p] = vals
        data[name] = {'q': q, 'claims': rec}
    time.sleep(2)
tl = list(targets)
labels = {}
for i in range(0, len(tl), 50):
    d = get('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=labels|descriptions&languages=en&ids=' + '|'.join(tl[i:i + 50]))
    for q, e in d['entities'].items():
        labels[q] = [e.get('labels', {}).get('en', {}).get('value'), e.get('descriptions', {}).get('en', {}).get('value')]
    time.sleep(2)
out = {}
for name, r in data.items():
    o = {}
    for p, vs in r['claims'].items():
        o[p] = [(labels.get(v, [v, ''])[0] or v) + ' (' + (labels.get(v, [v, ''])[1] or '') + ')' for v in vs]
    out[name] = o
json.dump(out, open(S + r'\wd_people.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for name, o in out.items():
    if any(p in o for p in ('P26', 'P451', 'P22', 'P25', 'P3373', 'P1038', 'P184', 'P185', 'P1066', 'P802')):
        print(name, {p: v for p, v in o.items() if p not in ('P69',)}, flush=True)
