"""ユニコーン一覧の会社ごとに、Wikidataの記録(創業者・CEO・会長・所有者・親会社)を集める。Claude不要。途中から再開できる。
出力: uni_cos.json  {会社名: {qid, people:[{id,ja,en,role,from}], orgs:[{id,ja,en,role}]}}"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}


def api(base, **p):
    url = base + '?' + urllib.parse.urlencode(p)
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception:
            time.sleep(3 * (i + 1))
    return {}


OUT = os.path.join(S, 'uni_cos.json')
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
uni = json.load(open(os.path.join(S, 'unicorns.json'), encoding='utf-8'))
todo = [u for u in uni if u['n'] not in res]
print('対象', len(todo), flush=True)
qid = {}
for i in range(0, len(todo), 40):
    ch = todo[i:i + 40]
    tt = sorted({(u.get('w') or u['n']) for u in ch})
    d = api('https://en.wikipedia.org/w/api.php', action='query', format='json', titles='|'.join(tt), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation', formatversion=2)
    q = d.get('query', {})
    norm = {x['from']: x['to'] for x in q.get('normalized', [])}
    red = {x['from']: x['to'] for x in q.get('redirects', [])}
    pg = {p['title']: p for p in q.get('pages', [])}
    for u in ch:
        t0 = u.get('w') or u['n']
        t = red.get(norm.get(t0, t0), norm.get(t0, t0))
        p = pg.get(t)
        if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
            qid[u['n']] = p['pageprops']['wikibase_item']
    time.sleep(1)
print('Q番号', len(qid), flush=True)
ents = {}
ids = sorted(set(qid.values()))
for i in range(0, len(ids), 40):
    d = api('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims', languages='en')
    ents.update(d.get('entities', {}))
    time.sleep(1)
PROPS = [('P112', 'founder'), ('P169', 'ceo'), ('P488', 'chair'), ('P127', 'owner'), ('P749', 'parent')]


def cids(e, prop):
    out = []
    for c in e.get('claims', {}).get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if not (isinstance(v, dict) and 'id' in v):
            continue
        q = c.get('qualifiers', {})
        if q.get('P582'):      # 終わった就任・所有は載せない
            continue
        st = q.get('P580', [{}])[0].get('datavalue', {}).get('value', {}).get('time') if q.get('P580') else None
        out.append((v['id'], int(st[1:5]) if st and re.match(r'^[+-]\d{4}', st) else 0))
    return out


rel, need = {}, set()
for n, q in qid.items():
    e = ents.get(q) or {}
    rel[n] = []
    for p, role in PROPS:
        for vid, yr in cids(e, p)[:10]:
            rel[n].append((vid, role, yr))
            need.add(vid)
lab = {}
ids = sorted(need)
for i in range(0, len(ids), 40):
    d = api('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='labels|claims', languages='ja|en')
    for k, e in d.get('entities', {}).items():
        lb = e.get('labels', {})
        human = any(c.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id') == 'Q5' for c in e.get('claims', {}).get('P31', []))
        lab[k] = {'ja': lb.get('ja', {}).get('value', ''), 'en': lb.get('en', {}).get('value', ''), 'human': human}
    time.sleep(1)
for u in todo:
    n = u['n']
    people, orgs, seen = [], [], set()
    for vid, role, yr in rel.get(n, []):
        L = lab.get(vid)
        if not L or vid in seen:
            continue
        nm = L['en'] or L['ja']
        if not nm:
            continue
        seen.add(vid)
        if L['human'] and role != 'parent':
            people.append({'id': vid, 'ja': L['ja'], 'en': L['en'], 'role': role, 'from': yr})
        elif not L['human']:
            orgs.append({'id': vid, 'ja': L['ja'], 'en': L['en'], 'role': role})
    res[n] = {'qid': qid.get(n, ''), 'people': people, 'orgs': orgs}
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('完了', len(res), '社 / 人物あり', sum(1 for v in res.values() if v['people']), '/ 組織あり', sum(1 for v in res.values() if v['orgs']))
