"""最重要の100人(top100_names.txt)について、Wikidataの識別番号を確定し、年表のもと(職歴・創業・学歴・受賞)と出典の有無を集める。
同姓同名の取り違えを避けるため、①人物であること ②名前が一致 ③説明が事業・技術・政治などの肩書き を満たすものだけを採る。決められないものは「要確認」に残す。
出力: top100_data.json  [{group,en,q,ja,desc,timeline:[{y,kind,label,ref}],status:{...}}]
使い方: python -u top100_build.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'top100_data.json')
ROLE_OK = re.compile(r'business|entrepreneur|investor|executive|founder|CEO|chief|engineer|computer|scientist|researcher|venture|technolog|software|programmer|developer|professor|economist|banker|financier|manager|director|president|chairman|philanthropist|inventor|politician|capitalist|angel|AI |artificial|internet|startup|industrialist|billionaire|chess|crypto', re.I)
SKIP = {'Hiroshi Yoshimura', 'Masahiro Sakane', 'Kiyoshi Tsuji'}      # 確信が持てない候補は外す


def api(**p):
    url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(p)
    for i in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(40 if '429' in str(e) else 4 * (i + 1))
    return {}


rows = {r[1].lower(): r for r in json.load(open(os.path.join(S, 'web', 'people.json'), encoding='utf-8'))['rows']}
names = []
seen = set()
for ln in open(os.path.join(S, 'top100_names.txt'), encoding='utf-8'):
    if ln.startswith('#') or '|' not in ln:
        continue
    g, n = ln.strip().split('|', 1)
    if n in SKIP or n.lower() in seen:
        continue
    seen.add(n.lower())
    names.append((g, n))
for g, n in [('投資家', 'Jack Dorsey'), ('大手テック', 'Reed Hastings'), ('大手テック', 'Evan Spiegel')]:
    if n.lower() not in seen:
        names.append((g, n))
        seen.add(n.lower())
out = []
for g, n in names:
    r = rows.get(n.lower())
    e = {'group': g, 'en': n, 'q': r[0] if r else '', 'ja': r[2] if r else '', 'desc': r[4] if r else '', 'how': '人物データと一致' if r else ''}
    if not e['q']:
        time.sleep(0.6)
        cands = [x['id'] for x in api(action='wbsearchentities', format='json', language='en', type='item', limit=8, search=n).get('search', [])]
        ents = api(action='wbgetentities', format='json', props='claims|labels|descriptions|aliases', languages='en|ja', ids='|'.join(cands)).get('entities', {}) if cands else {}
        nl = re.sub(r'[^a-z0-9]', '', n.lower())
        for q in cands:
            en = ents.get(q) or {}
            cl = en.get('claims', {})
            if not any((c.get('mainsnak', {}).get('datavalue', {}).get('value', {}) or {}).get('id') == 'Q5' for c in cl.get('P31', [])):
                continue
            labs = [en.get('labels', {}).get('en', {}).get('value', '')] + [a.get('value', '') for a in en.get('aliases', {}).get('en', [])]
            if not any(re.sub(r'[^a-z0-9]', '', l.lower()) == nl for l in labs if l):
                continue
            ds = en.get('descriptions', {}).get('en', {}).get('value', '')
            if not ROLE_OK.search(ds):
                continue
            e['q'] = q
            e['ja'] = en.get('labels', {}).get('ja', {}).get('value', '')
            e['desc'] = en.get('descriptions', {}).get('ja', {}).get('value', '') or ds
            e['how'] = 'Wikidata検索(名前一致・人物・肩書き)'
            break
    out.append(e)
print('対応づけ', sum(1 for e in out if e['q']), '/', len(out), '要確認', [e['en'] for e in out if not e['q']], flush=True)

# 年表のもと: 職歴(P108)・役職(P39)・創業(P112)・学歴(P69)・受賞(P166) と出典の有無
P = {'P108': '職歴', 'P39': '役職', 'P69': '学歴', 'P166': '受賞'}
labels = {}


def yr(snak):
    v = (snak or {}).get('datavalue', {}).get('value', {})
    m = re.match(r'^[+-]?(\d{4})', v.get('time', '')) if isinstance(v, dict) else None
    return int(m.group(1)) if m else None


qs = [e['q'] for e in out if e['q']]
claims = {}
for i in range(0, len(qs), 40):
    d = api(action='wbgetentities', format='json', props='claims', ids='|'.join(qs[i:i + 40]))
    for q, en in d.get('entities', {}).items():
        claims[q] = en.get('claims', {})
    time.sleep(1)
need = set()
for q, cl in claims.items():
    for p in P:
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if isinstance(v, dict) and v.get('id'):
                need.add(v['id'])
    for st in cl.get('P569', [])[:1]:
        pass
need = sorted(need)
for i in range(0, len(need), 50):
    d = api(action='wbgetentities', format='json', props='labels', languages='ja|en', ids='|'.join(need[i:i + 50]))
    for q, en in d.get('entities', {}).items():
        lb = en.get('labels', {})
        labels[q] = (lb.get('ja') or lb.get('en') or {}).get('value', q)
    time.sleep(1)
for e in out:
    q = e['q']
    cl = claims.get(q, {})
    tl = []
    for p, kind in P.items():
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if not (isinstance(v, dict) and v.get('id')):
                continue
            qual = st.get('qualifiers', {})
            y0 = yr((qual.get('P580') or [None])[0]) or yr((qual.get('P585') or [None])[0])
            y1 = yr((qual.get('P582') or [None])[0])
            tl.append({'y': y0, 'y2': y1, 'kind': kind, 'label': labels.get(v['id'], v['id']), 'ref': bool(st.get('references'))})
    for st in cl.get('P569', [])[:1]:
        tl.append({'y': yr(st.get('mainsnak')), 'y2': None, 'kind': '生年', 'label': '生まれる', 'ref': bool(st.get('references'))})
    tl.sort(key=lambda t: (t['y'] is None, t['y'] or 0))
    e['timeline'] = tl
    e['nref'] = sum(1 for t in tl if t['ref'])
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('年表あり', sum(1 for e in out if e.get('timeline')), '人 / 項目数', sum(len(e.get('timeline', [])) for e in out), '/ 出典つき', sum(e.get('nref', 0) for e in out), flush=True)
