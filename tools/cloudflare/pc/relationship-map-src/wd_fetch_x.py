import json, os, re, time, urllib.parse, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'people_wd_x.json')


def api(base, **params):
    url = base + '?' + urllib.parse.urlencode(params)
    for i in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read())
        except Exception as e:
            if '429' in str(e) or '503' in str(e):
                time.sleep(8 * (i + 1))
            else:
                time.sleep(2)
    return {}


WP = 'https://en.wikipedia.org/w/api.php'
WD = 'https://www.wikidata.org/w/api.php'
people = json.load(open(os.path.join(S, 'people_all_x.json'), encoding='utf-8'))
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
todo = [p for p in people if p['en'] not in res]
print('todo', len(todo), flush=True)

# 1) Wikipedia titles -> qid, shortdesc, disambiguation
def chunks(a, n):
    for i in range(0, len(a), n):
        yield a[i:i + n]

for ch in chunks(todo, 50):
    titles = [p['en'] for p in ch]
    d = api(WP, action='query', format='json', titles='|'.join(titles), redirects=1, prop='pageprops',
            ppprop='wikibase_item|disambiguation|wikibase-shortdesc', formatversion=2)
    q = d.get('query', {})
    norm = {}
    for x in q.get('normalized', []):
        norm[x['from']] = x['to']
    red = {}
    for x in q.get('redirects', []):
        red[x['from']] = x['to']
    pages = {pg['title']: pg for pg in q.get('pages', [])}
    for p in ch:
        t = norm.get(p['en'], p['en'])
        t = red.get(t, t)
        pg = pages.get(t)
        r = {'title': t}
        if pg and not pg.get('missing'):
            pp = pg.get('pageprops', {})
            r['q'] = pp.get('wikibase_item')
            r['desc'] = pp.get('wikibase-shortdesc', '')
            r['dis'] = 'disambiguation' in pp
        res[p['en']] = r
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    time.sleep(1)
print('step1 done', len(res), flush=True)

# 2) extracts for identity check
need = [(en, r) for en, r in res.items() if r.get('q') and not r.get('dis') and 'ex' not in r]
for ch in chunks(need, 20):
    d = api(WP, action='query', format='json', titles='|'.join(r['title'] for _, r in ch), prop='extracts',
            exintro=1, explaintext=1, exlimit='max', formatversion=2)
    ex = {pg['title']: pg.get('extract', '') for pg in d.get('query', {}).get('pages', [])}
    for en, r in ch:
        r['ex'] = ex.get(r['title'], '')[:1200]
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
    time.sleep(1)
print('step2 done', flush=True)

# 3) Wikidata entities
qs = [r['q'] for r in res.values() if r.get('q') and not r.get('dis') and 'wd' not in r]
ents = {}
for ch in chunks(sorted(set(qs)), 50):
    d = api(WD, action='wbgetentities', format='json', ids='|'.join(ch), props='claims|sitelinks|labels',
            languages='ja|en', sitefilter='jawiki|enwiki')
    ents.update(d.get('entities', {}))
    time.sleep(1)


def claim_ids(e, prop):
    out = []
    for c in e.get('claims', {}).get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'id' in v:
            out.append(v['id'])
    return out


def claim_time(e, prop):
    for c in e.get('claims', {}).get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'time' in v:
            return v['time'], v.get('precision')
    return None


labels_need = set()
for q, e in ents.items():
    for pr in ('P19', 'P27', 'P69', 'P106', 'P31'):
        labels_need.update(claim_ids(e, pr)[:6])
labels = {}
for ch in chunks(sorted(labels_need), 50):
    d = api(WD, action='wbgetentities', format='json', ids='|'.join(ch), props='labels|claims', languages='ja|en')
    for q, e in d.get('entities', {}).items():
        lb = e.get('labels', {})
        labels[q] = {'ja': lb.get('ja', {}).get('value'), 'en': lb.get('en', {}).get('value'),
                     'c': claim_ids(e, 'P17')[:1]}
    time.sleep(1)
# country labels for birthplaces
cn = set()
for v in labels.values():
    cn.update(v['c'])
cn -= set(labels)
for ch in chunks(sorted(cn), 50):
    d = api(WD, action='wbgetentities', format='json', ids='|'.join(ch), props='labels', languages='ja|en')
    for q, e in d.get('entities', {}).items():
        lb = e.get('labels', {})
        labels[q] = {'ja': lb.get('ja', {}).get('value'), 'en': lb.get('en', {}).get('value'), 'c': []}
    time.sleep(1)


def lab(q):
    v = labels.get(q) or {}
    return v.get('ja') or v.get('en')


for en, r in res.items():
    q = r.get('q')
    if not q or r.get('dis') or q not in ents:
        r['wd'] = 1
        continue
    e = ents[q]
    r['human'] = 'Q5' in claim_ids(e, 'P31')
    dob = claim_time(e, 'P569')
    dod = claim_time(e, 'P570')
    r['dob'] = list(dob) if dob else None
    r['dod'] = list(dod) if dod else None
    pob = claim_ids(e, 'P19')
    if pob:
        pl = pob[0]
        cty = (labels.get(pl) or {}).get('c') or []
        r['pob'] = [lab(pl), lab(cty[0]) if cty else None]
    r['cit'] = [lab(x) for x in claim_ids(e, 'P27')[:3] if lab(x)]
    r['edu'] = [lab(x) for x in claim_ids(e, 'P69')[:5] if lab(x)]
    r['occ'] = [lab(x) for x in claim_ids(e, 'P106')[:5] if lab(x)]
    sl = e.get('sitelinks', {})
    r['jaw'] = sl.get('jawiki', {}).get('title')
    r['enw'] = sl.get('enwiki', {}).get('title')
    r['jal'] = e.get('labels', {}).get('ja', {}).get('value')
    r['wd'] = 1
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('done', len(res), flush=True)
