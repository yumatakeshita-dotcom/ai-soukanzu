"""人物ごとの「創業した会社・組織」をWikidata(P112=創設者)から集める。Claude不要。
出力: ventures_wd.json  {英語名: [[表示名, 設立年, 解散年, 種類(英語)], ...]}
対象: PAUTOに入る(本人確認済み/可能性あり)人物。使い方: python wd_ventures.py"""
import json, os, re, time, urllib.parse, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
OUT = os.path.join(S, 'ventures_wd.json')


def sparql(q):
    url = 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(q)
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read())
        except Exception as e:
            print('retry', i, str(e)[:80], flush=True)
            time.sleep(10 * (i + 1))
    return None


qid = {}
for fn in ('people_wd.json', 'people_wd_x.json', 'people_wd_u.json'):
    f = os.path.join(S, fn)
    if os.path.exists(f):
        for en, r in json.load(open(f, encoding='utf-8')).items():
            if r.get('q') and r.get('human') and not r.get('dis'):
                qid.setdefault(en, r['q'])
# PAUTO(確認済み)の人物だけに絞る
html = open(os.path.join(S, 'web', 'index.html'), encoding='utf-8').read()
m = re.search(r'const PAUTO=(\{.*?\});\n', html, re.S)
auto = set(json.loads(m.group(1)).keys()) if m else set(qid)
rev = {q: en for en, q in qid.items() if en in auto}
qs = sorted(rev)
print('persons', len(qs), flush=True)
res = {}
SKIP = {'human', 'film', 'television series', 'album', 'single', 'video game', 'book', 'musical group', 'band'}
pending = [qs[i:i + 40] for i in range(0, len(qs), 40)]
tries = 0
while pending and tries < 60:
  tries += 1
  ch = pending.pop(0)
  if True:
    i = 0
    q = ('SELECT ?p ?o ?jl ?el ?inc ?dis ?tl WHERE { VALUES ?p { ' + ' '.join('wd:' + x for x in ch) + ' } '
         '?o wdt:P112 ?p. OPTIONAL{?o wdt:P571 ?inc} OPTIONAL{?o wdt:P576 ?dis} '
         'OPTIONAL{?o rdfs:label ?jl FILTER(lang(?jl)="ja")} OPTIONAL{?o rdfs:label ?el FILTER(lang(?el)="en")} '
         'OPTIONAL{?o wdt:P31 ?t. ?t rdfs:label ?tl FILTER(lang(?tl)="en")} }')
    rsp = sparql(q)
    if rsp is None:
        pending.append(ch)
        time.sleep(65)
        continue
    for b in rsp['results']['bindings']:
        g = lambda k: b.get(k, {}).get('value')
        p = rev.get(g('p').rsplit('/', 1)[-1])
        oid = g('o').rsplit('/', 1)[-1]
        name = g('jl') or g('el')
        if not p or not name or re.fullmatch(r'Q\d+', name):
            continue
        d = res.setdefault(p, {}).setdefault(oid, {'n': name, 'en': g('el') or '', 'a': None, 'b': None, 't': []})
        y = lambda s: int(s[:4]) if s and re.match(r'^[+-]?\d{4}', s.lstrip('+')) else None
        if g('inc'):
            d['a'] = y(g('inc').lstrip('+'))
        if g('dis'):
            d['b'] = y(g('dis').lstrip('+'))
        if g('tl') and g('tl') not in d['t']:
            d['t'].append(g('tl'))
    print('ok batch; remaining', len(pending), flush=True)
    time.sleep(30)
out = {}
for p, d in res.items():
    rows = []
    for o in d.values():
        if any(t in SKIP for t in o['t']):
            continue
        rows.append([o['n'], o['a'], o['b'], (o['t'] or [''])[0], o['en']])
    rows.sort(key=lambda r: (r[1] or 9999))
    if rows:
        out[p] = rows
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('people with ventures', len(out), 'orgs', sum(len(v) for v in out.values()))
