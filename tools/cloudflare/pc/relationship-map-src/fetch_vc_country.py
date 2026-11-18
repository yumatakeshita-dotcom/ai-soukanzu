"""各VC・投資家の『本拠地の国』を Wikidata(本社所在地→国、無ければ国)から調べる。Claude不要。
出力: vc_country.json {VCのキー: 国名(日本語)}  ※Wikidataで分からないものは空(画面には「国は未確認」と出す)"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
WD = 'https://www.wikidata.org/w/api.php'
WP = 'https://en.wikipedia.org/w/api.php'
JA = 'https://ja.wikipedia.org/w/api.php'


def api(base, **p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(base + '?' + urllib.parse.urlencode(p), headers=UA), timeout=60).read())
        except Exception:
            time.sleep(3 * (i + 1))
    return {}


vc = json.load(open(os.path.join(S, 'vc_inv.json'), encoding='utf-8'))
rows = [ln.rstrip('\n').split('|') for ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8') if ln.strip()]
qid = {k: v.get('q') for k, v in vc.items() if v.get('q')}
# 記事が取れなかったVCは、英語/日本語のタイトルからQ番号を探す
for r in rows:
    key, en, ja = r[0], (r + [''] * 5)[3], (r + [''] * 5)[4]
    if key in qid:
        continue
    for base, t in ((WP, en), (JA, ja)):
        if not t:
            continue
        d = api(base, action='query', format='json', titles=t, redirects=1, prop='pageprops', ppprop='wikibase_item', formatversion=2)
        p = (d.get('query', {}).get('pages') or [{}])[0]
        q = p.get('pageprops', {}).get('wikibase_item')
        if q and not p.get('missing'):
            qid[key] = q
            break
    time.sleep(0.3)
ents = {}
ids = sorted(set(qid.values()))
for i in range(0, len(ids), 40):
    ents.update(api(WD, action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims', languages='ja|en').get('entities', {}))
    time.sleep(0.5)


def cl(e, p):
    out = []
    for c in e.get('claims', {}).get(p, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'id' in v:
            out.append(v['id'])
    return out


hq = {k: (cl(ents.get(q, {}), 'P159') or [None])[0] for k, q in qid.items()}
direct = {k: (cl(ents.get(q, {}), 'P17') or cl(ents.get(q, {}), 'P495') or [None])[0] for k, q in qid.items()}
need = {x for x in list(hq.values()) + list(direct.values()) if x}
place = {}
ids = sorted(need)
for i in range(0, len(ids), 40):
    place.update(api(WD, action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims|labels', languages='ja|en').get('entities', {}))
    time.sleep(0.5)
# 本社所在地(都市)→ その都市の国
ctry = {}
for k, p in hq.items():
    if p and p in place:
        c = (cl(place[p], 'P17') or [None])[0]
        ctry[k] = c or (p if 'Q6256' in cl(place[p], 'P31') else None)
for k, c in direct.items():
    if not ctry.get(k) and c:
        ctry[k] = c
more = sorted({c for c in ctry.values() if c and c not in place})
for i in range(0, len(more), 40):
    place.update(api(WD, action='wbgetentities', format='json', ids='|'.join(more[i:i + 40]), props='labels', languages='ja|en').get('entities', {}))
    time.sleep(0.5)
SHORT = {'アメリカ合衆国': 'アメリカ', 'グレートブリテン及び北アイルランド連合王国': 'イギリス', '連合王国': 'イギリス', '大韓民国': '韓国', '中華人民共和国': '中国', 'アラブ首長国連邦': 'UAE'}
out = {}
for r in rows:
    k = r[0]
    c = ctry.get(k)
    lab = ''
    if c and c in place:
        lb = place[c].get('labels', {})
        lab = lb.get('ja', {}).get('value') or lb.get('en', {}).get('value', '')
    out[k] = SHORT.get(lab, lab)
json.dump(out, open(os.path.join(S, 'vc_country.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('国が分かった', sum(1 for v in out.values() if v), '/', len(out))
print('分からない:', [k for k, v in out.items() if not v])
print({k: v for k, v in list(out.items())[:70]})
