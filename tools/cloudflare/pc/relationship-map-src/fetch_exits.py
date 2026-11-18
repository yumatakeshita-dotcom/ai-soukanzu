"""VCの投資先のうち、上場(IPO)・買収(M&A)した会社を、Wikidataの記録から見つける。Claude不要。
  IPO: 証券取引所(P414)に上場中(終了日なし)。上場日(P580)があれば年も。
  M&A: 親会社(P749)が記録されている(開始日 P580 があれば年も)。
出力: exits_wd.json  {正規化した名前: [区分('IPO'|'M&A'), 年, 詳細(取引所名 / 親会社名)]}
対象: vc_inv.json / vc_big.json の投資先(Q番号あり)。使い方: python fetch_exits.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
WD = 'https://www.wikidata.org/w/api.php'


def api(**p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(WD + '?' + urllib.parse.urlencode(p), headers=UA), timeout=60).read())
        except Exception:
            time.sleep(2 * (i + 1))
    return {}


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


nz = lambda s: re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', str(s or '').lower())
rows = {}      # qid -> {名前...}
for k, v in ld('vc_inv.json', {}).items():
    for p in v.get('p', []):
        if p[2]:
            rows.setdefault(p[2], set()).update(x for x in (p[0], p[1]) if x)
for k, v in ld('vc_big.json', {}).items():
    for p in v.get('p', []):
        if p[2]:
            rows.setdefault(p[2], set()).update(x for x in (p[0], p[1]) if x)
for nm, v in ld('uni_cos.json', {}).items():
    if v.get('qid'):
        rows.setdefault(v['qid'], set()).add(nm)
ids = sorted(rows)
print('調べるQ番号', len(ids), flush=True)
res = ld('exits_wd.json', {})
done = ld('exits_done.json', [])
doneset = set(done)
todo = [q for q in ids if q not in doneset]


def yr(t):
    m = re.match(r'^[+-]?(\d{4})', t or '')
    return int(m.group(1)) if m else 0


ent, labs = {}, {}
for i in range(0, len(todo), 40):
    ch = todo[i:i + 40]
    ents = api(action='wbgetentities', format='json', ids='|'.join(ch), props='claims|labels', languages='ja|en').get('entities', {})
    need = set()
    for q, e in ents.items():
        for p in ('P414', 'P749'):
            for c in e.get('claims', {}).get(p, []):
                v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
                if isinstance(v, dict) and 'id' in v:
                    need.add(v['id'])
    lb = {}
    need = sorted(need)
    for j in range(0, len(need), 40):
        for k, e in api(action='wbgetentities', format='json', ids='|'.join(need[j:j + 40]), props='labels', languages='ja|en').get('entities', {}).items():
            l = e.get('labels', {})
            lb[k] = l.get('ja', {}).get('value') or l.get('en', {}).get('value', '')
    for q, e in ents.items():
        out = None
        for c in e.get('claims', {}).get('P414', []):
            v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
            qu = c.get('qualifiers', {})
            if isinstance(v, dict) and 'id' in v and not qu.get('P582') and c.get('rank') != 'deprecated':
                y = 0
                if qu.get('P580'):
                    y = yr(qu['P580'][0].get('datavalue', {}).get('value', {}).get('time', ''))
                out = ['IPO', y, lb.get(v['id'], '')]
                break
        if not out:
            for c in e.get('claims', {}).get('P749', []):
                v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
                qu = c.get('qualifiers', {})
                if isinstance(v, dict) and 'id' in v and not qu.get('P582') and c.get('rank') != 'deprecated':
                    y = yr(qu['P580'][0].get('datavalue', {}).get('value', {}).get('time', '')) if qu.get('P580') else 0
                    out = ['M&A', y, lb.get(v['id'], '')]
                    break
        if out:
            for nm in rows.get(q, []):
                res.setdefault(nz(nm), out)
    done += ch
    if (i // 40) % 25 == 0:
        json.dump(res, open(os.path.join(S, 'exits_wd.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(done, open(os.path.join(S, 'exits_done.json'), 'w', encoding='utf-8'))
        print(i, '/', len(todo), 'エグジット', len(res), flush=True)
    time.sleep(0.2)
json.dump(res, open(os.path.join(S, 'exits_wd.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(done, open(os.path.join(S, 'exits_done.json'), 'w', encoding='utf-8'))
print('完了 エグジット', len(res), '(IPO', sum(1 for v in res.values() if v[0] == 'IPO'), '/ M&A', sum(1 for v in res.values() if v[0] == 'M&A'), ')')
