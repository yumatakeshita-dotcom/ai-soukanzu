"""相関図に載っている人物のうち、顔写真がまだ無い人の写真を、Wikipedia以外から集める。途中から再開できる。Claude不要。
  1) Xのアカウントが分かっている人 → Xのプロフィール画像(unavatar.io経由)
  2) Wikidataで同姓同名の別人を避けて見つけた人(人物であること・肩書の説明が事業/技術系であること・名前が一致すること) → Wikimedia Commonsの写真(P18)
どちらも 96px の小さな JPEG にして、faces.json に入れる。 {名前(英語): {i: data URI, s: 出どころ, u: 出どころのURL}}
使い方: python -u fetch_faces.py"""
import base64, io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
CACHE = os.path.join(S, 'faces_cache.json')
OUT = os.path.join(S, 'faces.json')
from adds import apply_adds
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)

have = set()
for f in os.listdir(S):
    if (f.startswith('outsiders') and f.endswith('.json')) or f == 'photos2.json':
        try:
            for k, v in json.load(open(os.path.join(S, f), encoding='utf-8')).items():
                if isinstance(v, dict) and v.get('img'):
                    have.add(k)
        except Exception:
            pass
people = {}      # 英語名 -> {x: アカウント, cos: [会社名...]}
for key, c in CO_ALL.items():
    en = c.get('EN', {})
    xs = c.get('X', {})
    center = next((n['name'] for n in c['N'] if n['id'] == c.get('center')), key)
    for n in c['N']:
        if n.get('kind') != 'p':
            continue
        nm = en.get(n['id'])
        if not nm or nm in have:
            continue
        e = people.setdefault(nm, {'x': '', 'cos': []})
        if xs.get(n['id']) and not e['x']:
            e['x'] = xs[n['id']]
        if center not in e['cos']:
            e['cos'].append(center)
print('写真を探す人物', len(people), '(X', sum(1 for p in people.values() if p['x']), ')', flush=True)
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}


def get(u, tries=4):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
        except Exception as e:
            msg = str(e)
            if '404' in msg:
                return None
            time.sleep(8 * (i + 1) if '429' in msg else 3 * (i + 1))
    return None


def shrink(b):
    try:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        w, h = im.size
        s = min(w, h)
        top = 0 if h > w else (h - s) // 2        # 縦長の写真は上(顔のある側)から切り出す
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((96, 96), Image.LANCZOS)
        o = io.BytesIO()
        im.save(o, 'JPEG', quality=68, optimize=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()
    except Exception:
        return None


ROLE_OK = re.compile(r'business|entrepreneur|investor|executive|founder|CEO|chief|engineer|computer|scientist|researcher|venture|technolog|software|programmer|developer|professor|economist|banker|financier|manager|director|president|chairman|philanthropist|inventor|mathematician|physicist|chemist|executive|capitalist|angel|AI |artificial|internet|e-?commerce|startup|film|manufactur|industrialist|politician', re.I)


def wd_search(name):
    u = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&language=en&type=item&limit=5&search=' + urllib.parse.quote(name)
    b = get(u)
    return [x['id'] for x in json.loads(b).get('search', [])] if b else []


def wd_entities(ids):
    u = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|labels|descriptions|aliases&languages=en&ids=' + '|'.join(ids)
    b = get(u)
    return json.loads(b).get('entities', {}) if b else {}


def pick(name, cands):
    ents = {}
    for i in range(0, len(cands), 50):
        ents.update(wd_entities(cands[i:i + 50]))
    nl = re.sub(r'[^a-z0-9]', '', name.lower())
    for q in cands:
        e = ents.get(q) or {}
        cl = e.get('claims', {})
        if not any((c.get('mainsnak', {}).get('datavalue', {}).get('value', {}) or {}).get('id') == 'Q5' for c in cl.get('P31', [])):
            continue
        labs = [e.get('labels', {}).get('en', {}).get('value', '')] + [a.get('value', '') for a in e.get('aliases', {}).get('en', [])]
        if not any(re.sub(r'[^a-z0-9]', '', l.lower()) == nl for l in labs if l):
            continue
        desc = e.get('descriptions', {}).get('en', {}).get('value', '')
        if not ROLE_OK.search(desc):
            continue
        p18 = cl.get('P18', [])
        if not p18:
            continue
        fn = p18[0].get('mainsnak', {}).get('datavalue', {}).get('value')
        if fn:
            return q, fn, desc
    return None


n = 0
for name, p in people.items():
    if name in cache:
        continue
    res = None
    if p['x']:
        b = get('https://unavatar.io/x/' + urllib.parse.quote(p['x']) + '?fallback=false', tries=2)
        if b and len(b) > 1500:
            img = shrink(b)
            if img:
                res = {'i': img, 's': 'X(@' + p['x'] + ')', 'u': 'https://x.com/' + p['x']}
        time.sleep(1)
    if not res:
        try:
            time.sleep(0.6)
            cands = wd_search(name)
            hit = pick(name, cands) if cands else None
            if hit:
                q, fn, desc = hit
                b = get('https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(fn.replace(' ', '_')) + '?width=160')
                img = shrink(b) if b else None
                if img:
                    res = {'i': img, 's': 'Wikimedia Commons', 'u': 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(fn.replace(' ', '_')), 'q': q}
        except Exception as e:
            print('ERR', name, str(e)[:60], flush=True)
    cache[name] = res
    n += 1
    if res:
        print('○', name, res['s'], flush=True)
    if n % 25 == 0:
        json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump({k: v for k, v in cache.items() if v}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        print('進み', n, '/', len(people), '見つかった', sum(1 for v in cache.values() if v), flush=True)
json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump({k: v for k, v in cache.items() if v}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('完了', sum(1 for v in cache.values() if v), '/', len(people), flush=True)
