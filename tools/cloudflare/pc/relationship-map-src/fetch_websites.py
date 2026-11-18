"""各社の公式サイト(HP)のURLを、Wikidataの『公式ウェブサイト(P856)』から集める。Claude不要。途中から再開できる。
対象: 図のある会社・VC・VCの投資先・ニュースに出た会社・図に載っている出資者や関連組織。
手順: ①すでにQ番号が分かる会社(jp_cos/uni_cos/acq_qid/vc_inv)は直接 ②それ以外は英語/日本語Wikipediaの記事名からQ番号を探し、会社・組織かどうかを確認
出力: websites.json {'k': {図のキー: URL}, 'n': {正規化した名前: URL}}   ※URLが見つからない会社は載せない(画面側で「公式サイトを検索」を出す)"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'websites.json')
EN, JA, WD = 'https://en.wikipedia.org/w/api.php', 'https://ja.wikipedia.org/w/api.php', 'https://www.wikidata.org/w/api.php'


def api(base, **p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(base + '?' + urllib.parse.urlencode(p), headers=UA), timeout=60).read())
        except Exception:
            time.sleep(3 * (i + 1))
    return {}


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


def nz(s):
    s = re.sub(r'\b(inc|corp|co|ltd|llc|ai|labs|technologies|holdings)\b\.?', '', str(s or ''), flags=re.I)
    return re.sub(r'[\s・･·.\-_,]', '', s.lower())


import newco_data8 as D
res = {'k': {}, 'n': {}}      # 毎回作り直す(選び方を直したときに古いURLが残らないように)
names = {}          # 表示名 -> 優先度
keys = {}           # 図のキー -> 中心の会社名
for r in D.RANK:
    names[r['en']] = 9
for k, c in D.CO8.items():
    ctr = next((n for n in c['N'] if n['id'] == c['center']), None)
    if ctr:
        keys[k] = ctr['name']
        names[ctr['name']] = 9
    for n in c['N']:
        if n['kind'] in ('i', 'o') and n['id'] != c['center'] and not re.search(r'株主', n.get('role', '')):
            names[n['name']] = max(names.get(n['name'], 0), 3)
for r in D.JPCO:
    keys[r['key']] = r['name']
    names[r['name']] = 9
for k, v in ld('vc_inv.json', {}).items():
    for nm in (v['en'], v['jp']):
        if nm:
            names[nm] = 8
    for p in v.get('p', []):
        names[p[0]] = max(names.get(p[0], 0), 2)
        if p[1]:
            names[p[1]] = max(names.get(p[1], 0), 2)
try:
    from vc_official import OFFICIAL
    for k, (_u, ns) in OFFICIAL.items():
        for nm in [x.strip() for x in ns.split(', ') if x.strip()]:
            names[nm] = max(names.get(nm, 0), 2)
except ImportError:
    pass
for h in ld('funding_news.json', []):
    if h.get('cn'):
        names[h['cn']] = max(names.get(h['cn'], 0), 2)
for u in ld('unicorns.json', []):
    names[u['n']] = max(names.get(u['n'], 0), 7)
for r in ld('jp_startups.json', []):      # 日本のスタートアップ(未上場)。上場企業は日経のHPを使う
    if not r.get('code') and not r.get('url'):
        names[r['n']] = max(names.get(r['n'], 0), 6)
print('名前', len(names), '図', len(keys), flush=True)

# --- 既知のQ番号 ---
known = {}
for k, q in ld('acq_qid.json', {}).items():
    if q:
        known['k:' + k] = q
for code, v in ld('jp_cos.json', {}).items():
    if v.get('qid'):
        known['k:jp_' + code] = v['qid']
for nm, v in ld('uni_cos.json', {}).items():
    if v.get('qid'):
        known['n:' + nz(nm)] = v['qid']
for kid, v in ld('vc_big.json', {}).items():      # VCの投資先: Q番号が分かっているので、名前の検索なしで公式サイトを引く
    if v.get('q'):
        known['n:' + nz(v['en'])] = v['q']
    for p in v.get('p', [])[:120]:
        if p[2] and len(known) < 30000:
            known['n:' + nz(p[0])] = p[2]
for k, v in ld('vc_inv.json', {}).items():
    if v.get('q'):
        known['n:' + nz(v['en'])] = v['q']
        if v.get('jp'):
            known['n:' + nz(v['jp'])] = v['q']

# --- 名前→Q番号(Wikipediaの記事名) ---
todo = [nm for nm in names if nz(nm) and nz(nm) not in res['n'] and 'n:' + nz(nm) not in known and len(nm) >= 2]
todo.sort(key=lambda x: -names[x])
todo = todo[:7000]
print('記事名で調べる', len(todo), flush=True)
found = {}
for lang, base in (('ja', JA), ('en', EN)):
    pool = [t for t in todo if (re.search(r'[ぁ-んァ-ヶ一-龥]', t) if lang == 'ja' else not re.search(r'[ぁ-んァ-ヶ一-龥]', t))]
    for i in range(0, len(pool), 50):
        ch = pool[i:i + 50]
        d = api(base, action='query', format='json', titles='|'.join(ch), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation', formatversion=2)
        q = d.get('query', {})
        norm = {x['from']: x['to'] for x in q.get('normalized', [])}
        red = {x['from']: x['to'] for x in q.get('redirects', [])}
        pg = {p['title']: p for p in q.get('pages', [])}
        for t in ch:
            n = red.get(norm.get(t, t), norm.get(t, t))
            p = pg.get(n)
            if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
                found[t] = p['pageprops']['wikibase_item']
        time.sleep(0.4)
    print(lang, '記事あり', len(found), flush=True)

# --- Q番号 → 公式サイト(P856)・会社かどうか ---
want = {}      # Q番号 -> [(種別, キー)]
for kk, q in known.items():
    want.setdefault(q, []).append(tuple(kk.split(':', 1)))
for t, q in found.items():
    want.setdefault(q, []).append(('n', nz(t)))
ents = {}
ids = sorted(want)
for i in range(0, len(ids), 40):
    ents.update(api(WD, action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims', languages='en').get('entities', {}))
    time.sleep(0.4)
cls = set()
for e in ents.values():
    for c in e.get('claims', {}).get('P31', []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value', {})
        if isinstance(v, dict) and 'id' in v:
            cls.add(v['id'])
cl = {}
cls = sorted(cls)
for i in range(0, len(cls), 50):
    for k, e in api(WD, action='wbgetentities', format='json', ids='|'.join(cls[i:i + 50]), props='labels', languages='en').get('entities', {}).items():
        cl[k] = e.get('labels', {}).get('en', {}).get('value', '')
    time.sleep(0.4)
ORG = re.compile(r'company|business|enterprise|corporation|startup|brand|firm|subsidiary|software|retailer|manufacturer|bank|organization|organisation|fund|investment|capital|group|conglomerate|institution|service|platform|website|企業|会社', re.I)
BAD = re.compile(r'human|film|album|song|single|person|village|city|country|species|disambiguation|television series|video game|novel|book', re.I)


def site(e):
    """複数のURLがあるときは、国別・言語別のページ(/at/ など)ではなく、いちばん浅い(トップに近い)URLを選ぶ"""
    cands = []
    for c in e.get('claims', {}).get('P856', []):
        if c.get('rank') == 'deprecated':
            continue
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, str) and v.startswith('http'):
            if c.get('qualifiers', {}).get('P582'):        # 終了した(古い)サイトは使わない
                continue
            pu = urllib.parse.urlparse(v)
            depth = len([x for x in pu.path.split('/') if x])
            cands.append((depth, 0 if c.get('rank') == 'preferred' else 1, 0 if pu.scheme == 'https' else 1, len(v), v))
    return min(cands)[4] if cands else ''


def is_org(e, loose):
    labs = [cl.get(c.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id'), '') for c in e.get('claims', {}).get('P31', [])]
    if any(BAD.search(x) for x in labs):
        return False
    return loose or any(ORG.search(x) for x in labs)


n_added = 0
for q, targets in want.items():
    e = ents.get(q) or {}
    url = site(e)
    if not url:
        continue
    for kind, key in targets:
        loose = (kind == 'k')            # 図のキーは確実な対応なので、種別の確認を緩める
        if not is_org(e, loose or q in known.values()):
            continue
        res[kind][key] = url
        n_added += 1
# 図のキー: 中心の会社名 → 名前の対応から引く
for k, nm in keys.items():
    if k not in res['k'] and nz(nm) in res['n']:
        res['k'][k] = res['n'][nz(nm)]
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('公式サイトが見つかった: 名前', len(res['n']), '/ 図のキー', len(res['k']), '/ 図の総数', len(keys))
