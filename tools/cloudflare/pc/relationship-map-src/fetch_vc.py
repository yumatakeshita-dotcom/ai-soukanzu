"""日本・世界のVC(ベンチャーキャピタル、企業のVC部門、ファンド)の『主な投資先』を、Wikipediaの記事の「投資先」の節から集める。Claude不要。
手順: vc_names.txt の各VCの記事 → 投資先の節のリンク → Wikidataで『会社・事業体』だけに絞る。
出力: vc_inv.json  {VCのキー: {en, jp, region, kind, desc, wiki, p:[[英語名, 日本語名, Q番号], ...]}}
使い方: python fetch_vc.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'vc_inv.json')


def api(base, **p):
    url = base + '?' + urllib.parse.urlencode(p)
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(3 * (i + 1))
    return {}


EN = 'https://en.wikipedia.org/w/api.php'
JA = 'https://ja.wikipedia.org/w/api.php'
WD = 'https://www.wikidata.org/w/api.php'
rows = [ln.rstrip('\n').split('|') for ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8') if ln.strip()]
HEAD = re.compile(r'portfolio|investments?|notable|companies|exits?|funded|backed|alumni|投資先|出資先|主な|実績|ポートフォリオ', re.I)
SKIP_HEAD = re.compile(r'references|external|see also|history|notes|脚注|外部リンク|関連項目|歴史|沿革', re.I)
LINK = re.compile(r'\[\[([^\]\|#\n]+)(?:#[^\]\|]*)?(?:\|[^\]\n]*)?\]\]')
BAD = re.compile(r'^(File|Image|Category|Template|Help|Wikipedia|List of|ファイル|カテゴリ|Template:|画像)', re.I)
COMPANY = re.compile(r'company|business|enterprise|corporation|startup|brand|firm|subsidiary|software|retailer|manufacturer|bank|企業|会社', re.I)
NOTCO = re.compile(r'news|media|magazine|newspaper|publisher|publishing|television|broadcast|website|encyclopedia|university|college|school|government|agency|city|country|nonprofit|non-profit|charity|foundation|think tank|wire service|research institute|venture capital|investment|asset management|private equity|hedge fund|law firm|accelerator|consult', re.I)


def page(base, title):
    d = api(base, action='parse', format='json', page=title, prop='wikitext', redirects=1, formatversion=2)
    return d.get('parse', {}).get('wikitext', '') if d else ''


def sections(wt):
    parts = re.split(r'\n(={2,4})\s*([^=\n]+?)\s*\1\s*\n', '\n' + wt)
    out = []
    for i in range(1, len(parts) - 2, 3):
        out.append((parts[i + 1], parts[i + 2]))
    return out


def shortdesc(base, title):
    d = api(base, action='query', format='json', titles=title, redirects=1, prop='pageprops', ppprop='wikibase-shortdesc|wikibase_item', formatversion=2)
    p = (d.get('query', {}).get('pages') or [{}])[0]
    return p.get('pageprops', {}).get('wikibase-shortdesc', ''), p.get('pageprops', {}).get('wikibase_item', '')


res = {}
allq = {}      # 投資先の英語タイトル -> Q番号
for r in rows:
    key, region, kind, en, ja, _x, jp = (r + [''] * 7)[:7]
    lang, title, base = 'en', en, EN
    wt = page(EN, en) if en else ''
    if not wt and ja:
        lang, title, base, wt = 'ja', ja, JA, page(JA, ja)
    if not wt:
        print(key, '記事なし', flush=True)
        continue
    links = []
    for h, body in sections(wt):
        if HEAD.search(h) and not SKIP_HEAD.search(h):
            links += LINK.findall(body)
    # 投資先の節のリンクが少ない場合は、参考文献などを除く全節のリンクから探す(会社かどうかはあとでWikidataで絞る)
    if len(links) < 3:      # 投資先の節がほぼ無い記事だけ、全体から探す(それ以外は節に絞って精度を保つ)
        for h, body in sections(wt):
            if not SKIP_HEAD.search(h):
                links += LINK.findall(body)
    # 見出しに合う節が無い場合は、本文の表(wikitable)の中のリンクを使う
    if not links:
        for tb in re.findall(r'\{\|.*?\n\|\}', wt, re.S):
            links += LINK.findall(tb)
    seen, titles = set(), []
    for t in links:
        t = t.strip()
        if not t or BAD.match(t) or t.lower() in seen or t == title:
            continue
        seen.add(t.lower())
        titles.append(t)
    sd, q = shortdesc(base, title)
    res[key] = {'en': en or title, 'jp': jp or ja or en, 'region': region, 'kind': kind, 'desc': sd, 'wiki': [lang, title], 'q': q, 'raw': titles[:400]}
    print(key, lang, len(titles), flush=True)
    time.sleep(0.4)

# --- 投資先の候補(リンク)を Wikidata で『会社・事業体』に絞る ---
def resolve(base, titles):
    out = {}
    for i in range(0, len(titles), 50):
        ch = titles[i:i + 50]
        d = api(base, action='query', format='json', titles='|'.join(ch), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation', formatversion=2)
        q = d.get('query', {})
        norm = {x['from']: x['to'] for x in q.get('normalized', [])}
        red = {x['from']: x['to'] for x in q.get('redirects', [])}
        pg = {p['title']: p for p in q.get('pages', [])}
        for t in ch:
            n = red.get(norm.get(t, t), norm.get(t, t))
            p = pg.get(n)
            if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
                out[t] = (n, p['pageprops']['wikibase_item'])
        time.sleep(0.4)
    return out


for lang, base in (('en', EN), ('ja', JA)):
    tl = sorted({t for v in res.values() if v['wiki'][0] == lang for t in v['raw']})
    allq[lang] = resolve(base, tl)
    print(lang, '投資先の候補', len(tl), '→ 記事あり', len(allq[lang]), flush=True)
qids = sorted({q for m in allq.values() for (_n, q) in m.values()})
ent = {}
for i in range(0, len(qids), 50):
    d = api(WD, action='wbgetentities', format='json', ids='|'.join(qids[i:i + 50]), props='claims|labels', languages='en|ja')
    ent.update(d.get('entities', {}))
    time.sleep(0.4)
cls = set()
for e in ent.values():
    for c in e.get('claims', {}).get('P31', []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value', {})
        if isinstance(v, dict) and 'id' in v:
            cls.add(v['id'])
cl = {}
cls = sorted(cls)
for i in range(0, len(cls), 50):
    d = api(WD, action='wbgetentities', format='json', ids='|'.join(cls[i:i + 50]), props='labels', languages='en')
    for k, e in d.get('entities', {}).items():
        cl[k] = e.get('labels', {}).get('en', {}).get('value', '')
    time.sleep(0.4)


def is_company(e):
    ok = False
    for c in e.get('claims', {}).get('P31', []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value', {})
        if not isinstance(v, dict):
            continue
        label = cl.get(v.get('id'), '')
        if NOTCO.search(label):      # 報道機関・大学・他のVCなどは、投資先の会社として載せない
            return False
        if COMPANY.search(label):
            ok = True
    return ok


tot = 0
for key, v in res.items():
    lang = v['wiki'][0]
    out, seen = [], set()
    for t in v['raw']:
        hit = allq[lang].get(t)
        if not hit:
            continue
        n, q = hit
        e = ent.get(q) or {}
        if q in seen or q == v.get('q') or not is_company(e) or re.match(r'^(startup|start-up|company|business|venture|unicorn|corporation)\b', (n or '').lower()):
            continue
        seen.add(q)
        lb = e.get('labels', {})
        out.append([lb.get('en', {}).get('value') or n, lb.get('ja', {}).get('value', ''), q])
    v['p'] = out[:300]
    del v['raw']
    tot += len(v['p'])
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('VC', len(res), '/ 投資先の合計', tot, '/ 投資先ありのVC', sum(1 for v in res.values() if v['p']))
