"""各社が買収した会社・子会社(acq.json / acq_wd.json)ごとに、Wikidataの記録(創業者・CEO・会長・所有者・親会社)を集める。Claude不要。途中から再開できる。
  会社の特定: 英語版Wikipediaの記事名 → Wikidata番号。Wikidata由来の行は、その会社の『親会社/所有者』に買収元の番号が入っているものだけを採用(別の会社との取り違えを避ける)。
出力: acq_cos.json  {Wikidata番号: {name, en, parents:[{k, y, src}], people:[{id,ja,en,role,from}], orgs:[{id,ja,en,role}]}}
使い方: python fetch_acq_cos.py [上限(会社の数)]"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 6000
WKIND = re.compile(r'business|enterprise|company|organi[sz]ation|subsidiary|manufacturer|bank|publisher|developer|chain|venture|corporation|contractor|provider|division|studio|firm|group|maker|retailer|airline|operator|broadcaster|unit', re.I)
WNOT = re.compile(r'patent|railway|station|skyscraper|building|bridge|factory|plant|cable|stadium|card|account|database|website|series|trademark|channel|franchise|product', re.I)


def api(base, **p):
    url = base + '?' + urllib.parse.urlencode(p)
    for i in range(15):      # 429(回数制限)のときは長く待って、成功するまで繰り返す
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            print('待機', str(e)[:40], flush=True)
            time.sleep(4 * (i + 1) if '429' not in str(e) else 90)
    raise SystemExit('API失敗が続いたので止めます(再実行で続きから)')


names = {}
for ln in open(os.path.join(S, 'acq_names.txt'), encoding='utf-8'):
    if '=' in ln:
        k, v = ln.rstrip('\n').split('=', 1)
        names[k] = v
pq = json.load(open(os.path.join(S, 'acq_qid.json'), encoding='utf-8'))
cand = {}      # 英語の記事名(小文字) -> {title, name, parents:[...]}


def add(title, name, key, y, src):
    t = (title or '').strip()
    if not t or not re.match(r'^[\x20-\x7eÀ-ɏ]+$', t) or len(t) < 3:
        return
    c = cand.setdefault(t.lower(), {'title': t, 'name': name, 'parents': []})
    if not any(p['k'] == key for p in c['parents']):
        c['parents'].append({'k': key, 'y': y, 'src': src})


for k, rows in json.load(open(os.path.join(S, 'acq.json'), encoding='utf-8')).items():
    for r in rows:      # [名前, 年, 金額, 説明, 記事名]
        add(r[4] or r[0], r[0], k, r[1], 'w')
for k, rows in json.load(open(os.path.join(S, 'acq_wd.json'), encoding='utf-8')).items():
    for r in rows:      # [名前, 年, 種類, 終了年, 英語名]
        kind = r[2] or ''
        if not kind or WNOT.search(kind) or not WKIND.search(kind):
            continue
        add(r[4] or r[0], r[0], k, r[1], 'd')
OUT = os.path.join(S, 'acq_cos.json')
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
done_titles = {v.get('title', '').lower() for v in res.values()} | set(json.load(open(os.path.join(S, 'acq_cos_done.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'acq_cos_done.json')) else [])
todo = [c for t, c in cand.items() if t not in done_titles][:LIMIT]
print('候補', len(cand), '/ これから', len(todo), flush=True)
qid = {}
for i in range(0, len(todo), 40):
    ch = todo[i:i + 40]
    d = api('https://en.wikipedia.org/w/api.php', action='query', format='json', titles='|'.join(c['title'] for c in ch), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation', formatversion=2)
    q = d.get('query', {})
    nm = {x['from']: x['to'] for x in q.get('normalized', [])}
    rd = {x['from']: x['to'] for x in q.get('redirects', [])}
    pg = {p['title']: p for p in q.get('pages', [])}
    for c in ch:
        t = rd.get(nm.get(c['title'], c['title']), nm.get(c['title'], c['title']))
        p = pg.get(t)
        if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
            qid[c['title'].lower()] = p['pageprops']['wikibase_item']
    time.sleep(2.5)
    if i % 400 == 0:
        print('記事', i, '/', len(todo), flush=True)
print('Q番号', len(qid), flush=True)
ids = sorted(set(qid.values()))
ents = {}
for i in range(0, len(ids), 40):
    d = api('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims|labels', languages='en|ja')
    ents.update(d.get('entities', {}))
    time.sleep(2.5)
    if i % 400 == 0:
        print('Wikidata', i, '/', len(ids), flush=True)
PROPS = [('P112', 'founder'), ('P169', 'ceo'), ('P488', 'chair'), ('P127', 'owner'), ('P749', 'parent')]


def cids(e, prop):
    out = []
    for c in e.get('claims', {}).get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if not (isinstance(v, dict) and 'id' in v):
            continue
        q = c.get('qualifiers', {})
        if q.get('P582'):
            continue
        st = q.get('P580', [{}])[0].get('datavalue', {}).get('value', {}).get('time') if q.get('P580') else None
        out.append((v['id'], int(st[1:5]) if st and re.match(r'^[+-]\d{4}', st) else 0))
    return out


rel, need, keep = {}, set(), {}
for c in todo:
    q = qid.get(c['title'].lower())
    e = ents.get(q or '') or {}
    if not q or not e:
        continue
    links = {v for p in ('P749', 'P127') for v, _ in cids(e, p)}
    ok = any(p['src'] == 'w' for p in c['parents']) or any(pq.get(p['k']) in links for p in c['parents'])
    if not ok:
        continue
    keep[q] = c
    rel[q] = []
    for p, role in PROPS:
        for vid, yr in cids(e, p)[:8]:
            rel[q].append((vid, role, yr))
            need.add(vid)
lab = {}
ids = sorted(need)
for i in range(0, len(ids), 40):
    d = api('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='labels|claims', languages='ja|en')
    for k, e in d.get('entities', {}).items():
        lb = e.get('labels', {})
        human = any(c.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id') == 'Q5' for c in e.get('claims', {}).get('P31', []))
        lab[k] = {'ja': lb.get('ja', {}).get('value', ''), 'en': lb.get('en', {}).get('value', ''), 'human': human}
    time.sleep(2.5)
    if i % 400 == 0:
        print('ラベル', i, '/', len(ids), flush=True)
for q, c in keep.items():
    people, orgs, seen = [], [], set()
    for vid, role, yr in rel.get(q, []):
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
    e = ents.get(q, {})
    lb = e.get('labels', {})
    res[q] = {'title': c['title'], 'name': c['name'], 'en': lb.get('en', {}).get('value', c['title']), 'ja': lb.get('ja', {}).get('value', ''),
              'parents': c['parents'], 'people': people, 'orgs': orgs}
dn = sorted(done_titles | {c['title'].lower() for c in todo})
json.dump(dn, open(os.path.join(S, 'acq_cos_done.json'), 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('完了', len(res), '社 / 人物あり', sum(1 for v in res.values() if v['people']))
