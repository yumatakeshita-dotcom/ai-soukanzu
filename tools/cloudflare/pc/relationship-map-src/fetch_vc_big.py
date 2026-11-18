"""VCを大量に集め、各VCの投資先(の候補)をWikipediaの「リンク元」から集める。Claude不要。途中から再開できる(キャッシュ: vc_big_*.json)。
手順
  1) 英語版・日本語版Wikipediaの「ベンチャーキャピタル」カテゴリ(下位カテゴリも)から、VC・アクセラレーターの記事を集める
  2) Wikidataで『会社・組織』だけに絞り、公式サイト・本社の国(現在も存在する国)・短い説明を取る
  3) 各VCの記事へリンクしている記事(=記事の中でそのVCに触れている会社)を集め、Wikidataで『会社』だけに絞って、投資先の記録にする
出力: vc_big.json {キー: {en, jp, country, kind, desc, site, wiki:[言語,記事名], p:[[英語名, 日本語名, Q番号], ...]}}
使い方: python fetch_vc_big.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
EN, JA, WD = 'https://en.wikipedia.org/w/api.php', 'https://ja.wikipedia.org/w/api.php', 'https://www.wikidata.org/w/api.php'


def api(base, **p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(base + '?' + urllib.parse.urlencode(p), headers=UA), timeout=60).read())
        except Exception:
            time.sleep(2 * (i + 1))
    return {}


def ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


def sv(n, o):
    json.dump(o, open(os.path.join(S, n + '.tmp'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    os.replace(os.path.join(S, n + '.tmp'), os.path.join(S, n))


# ---------- 1) VCの記事を集める ----------
def crawl(base, seeds, depth):
    pages, seen, front = {}, set(), [(s, 0) for s in seeds]
    while front:
        cat, d = front.pop(0)
        if cat in seen:
            continue
        seen.add(cat)
        cont = {}
        while True:
            r = api(base, action='query', format='json', list='categorymembers', cmtitle=cat, cmlimit=500, cmtype='page|subcat', **cont)
            for m in r.get('query', {}).get('categorymembers', []):
                if m['ns'] == 14 and d < depth:
                    front.append((m['title'], d + 1))
                elif m['ns'] == 0:
                    pages[m['title']] = cat
            if 'continue' in r:
                cont = {'cmcontinue': r['continue']['cmcontinue']}
            else:
                break
            time.sleep(0.2)
        time.sleep(0.2)
    return pages


titles = ld('vc_big_titles.json', None)
if titles is None:
    en = crawl(EN, ['Category:Venture capital firms', 'Category:Corporate venture capital', 'Category:Startup accelerators', 'Category:Seed accelerators'], 3)
    ja = crawl(JA, ['Category:ベンチャーキャピタル', 'Category:日本のベンチャーキャピタル'], 2)
    titles = {'en': sorted(en), 'ja': sorted(ja)}
    sv('vc_big_titles.json', titles)
print('VCの記事 en', len(titles['en']), 'ja', len(titles['ja']), flush=True)

# ---------- 2) Wikidataで絞る ----------
def pageprops(base, tl):
    out = {}
    for i in range(0, len(tl), 50):
        ch = tl[i:i + 50]
        d = api(base, action='query', format='json', titles='|'.join(ch), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation|wikibase-shortdesc', formatversion=2)
        q = d.get('query', {})
        norm = {x['from']: x['to'] for x in q.get('normalized', [])}
        red = {x['from']: x['to'] for x in q.get('redirects', [])}
        pg = {p['title']: p for p in q.get('pages', [])}
        for t in ch:
            n = red.get(norm.get(t, t), norm.get(t, t))
            p = pg.get(n)
            if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
                out[t] = (n, p['pageprops']['wikibase_item'], p.get('pageprops', {}).get('wikibase-shortdesc', ''))
        time.sleep(0.25)
    return out


def entities(ids, props='claims|labels'):
    ents = {}
    ids = sorted(set(ids))
    for i in range(0, len(ids), 40):
        ents.update(api(WD, action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props=props, languages='ja|en').get('entities', {}))
        time.sleep(0.25)
    return ents


def cl(e, p):
    out = []
    for c in e.get('claims', {}).get(p, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, dict) and 'id' in v and not c.get('qualifiers', {}).get('P582'):
            out.append(v['id'])
    return out


def site(e):
    c = []
    for x in e.get('claims', {}).get('P856', []):
        v = x.get('mainsnak', {}).get('datavalue', {}).get('value')
        if isinstance(v, str) and v.startswith('http') and not x.get('qualifiers', {}).get('P582') and x.get('rank') != 'deprecated':
            pu = urllib.parse.urlparse(v)
            c.append((len([z for z in pu.path.split('/') if z]), 0 if pu.scheme == 'https' else 1, len(v), v))
    return min(c)[3] if c else ''


vcmeta = ld('vc_big_meta.json', None)
if vcmeta is None:
    vcmeta = {}
    for lang, base in (('en', EN), ('ja', JA)):
        pp = pageprops(base, titles[lang])
        qs = [v[1] for v in pp.values()]
        ents = entities(qs)
        # 国: 本社所在地(P159)→その国(P17)、無ければ本体の国。現在も存在する国(終了日の無い記述)だけ使う
        hq = {q: (cl(e, 'P159') or [None])[0] for q, e in ents.items()}
        direct = {q: (cl(e, 'P17') or cl(e, 'P495') or [None])[0] for q, e in ents.items()}
        pl = entities([x for x in list(hq.values()) + list(direct.values()) if x])
        cty = {}
        for q in ents:
            c = None
            if hq.get(q) in pl:
                c = (cl(pl[hq[q]], 'P17') or [None])[0]
            c = c or direct.get(q)
            cty[q] = c
        lab = entities([c for c in cty.values() if c], 'labels')
        for t, (n, q, sd) in pp.items():
            e = ents.get(q) or {}
            if 'Q5' in cl(e, 'P31'):       # 人は除く
                continue
            lb = e.get('labels', {})
            c = cty.get(q)
            cname = ''
            if c and c in lab:
                cname = lab[c].get('labels', {}).get('ja', {}).get('value') or lab[c].get('labels', {}).get('en', {}).get('value', '')
            vcmeta[lang + ':' + t] = {'lang': lang, 'title': n, 'q': q, 'en': lb.get('en', {}).get('value', '') or (n if lang == 'en' else ''), 'jp': lb.get('ja', {}).get('value', ''),
                                      'country': cname, 'desc': sd, 'site': site(e)}
        print(lang, '会社・組織', sum(1 for k in vcmeta if k.startswith(lang)), flush=True)
    sv('vc_big_meta.json', vcmeta)
print('VC', len(vcmeta), flush=True)

# ---------- 3) リンク元(= そのVCに触れている記事) ----------
bl = ld('vc_big_bl.json', {})
for key, m in vcmeta.items():
    if key in bl:
        continue
    base = EN if m['lang'] == 'en' else JA
    r = api(base, action='query', format='json', list='backlinks', bltitle=m['title'], blnamespace=0, bllimit=500, blredirect=1)
    out = []
    for x in r.get('query', {}).get('backlinks', []):
        out.append(x['title'])
        for y in x.get('redirlinks', []):
            out.append(y['title'])
    bl[key] = list(dict.fromkeys(out))[:500]
    if len(bl) % 100 == 0:
        sv('vc_big_bl.json', bl)
        print('リンク元', len(bl), '/', len(vcmeta), flush=True)
    time.sleep(0.2)
sv('vc_big_bl.json', bl)

# ---------- 4) リンク元のうち『会社』だけを残す ----------
vctitles = {m['title'] for m in vcmeta.values()}
cand = {'en': set(), 'ja': set()}
for key, tl in bl.items():
    lang = vcmeta[key]['lang']
    for t in tl:
        if t not in vctitles and not re.match(r'^(List of|Category|Template|Wikipedia|\d{4}\b|Portal|File|Help|Talk|一覧|.+の一覧)', t):
            cand[lang].add(t)
verdict = ld('vc_big_verdict.json', {})       # 'lang:title' -> [英語名, 日本語名, Q番号] または 0(会社ではない)
COMPANY = re.compile(r'company|business|enterprise|corporation|startup|brand|firm|subsidiary|software|retailer|manufacturer|bank|企業|会社', re.I)
NOTCO = re.compile(r'news|media|magazine|newspaper|publisher|publishing|television|broadcast|website|encyclopedia|university|college|school|government|agency|city|country|nonprofit|non-profit|charity|foundation|think tank|wire service|research institute|venture capital|investment|asset management|private equity|hedge fund|law firm|accelerator|consult|human|film|album|song|village|species|disambiguation|series|video game|novel|book|bank holding', re.I)
clcache = ld('vc_big_cls.json', {})
for lang, base in (('en', EN), ('ja', JA)):
    todo = sorted(t for t in cand[lang] if lang + ':' + t not in verdict)
    print(lang, '会社かどうか調べる', len(todo), flush=True)
    for i in range(0, len(todo), 50):
        ch = todo[i:i + 50]
        pp = pageprops(base, ch)
        ents = entities([v[1] for v in pp.values()])
        need = {c for e in ents.values() for c in cl(e, 'P31')} - set(clcache)
        for k, e in entities(need, 'labels').items():
            clcache[k] = e.get('labels', {}).get('en', {}).get('value', '')
        for t in ch:
            hit = pp.get(t)
            ok = 0
            if hit:
                e = ents.get(hit[1]) or {}
                labs = [clcache.get(c, '') for c in cl(e, 'P31')]
                if labs and not any(NOTCO.search(x) for x in labs) and any(COMPANY.search(x) for x in labs):
                    lb = e.get('labels', {})
                    ok = [lb.get('en', {}).get('value') or hit[0], lb.get('ja', {}).get('value', ''), hit[1]]
            verdict[lang + ':' + t] = ok
        if (i // 50) % 20 == 0:
            sv('vc_big_verdict.json', verdict)
            sv('vc_big_cls.json', clcache)
            print(lang, i, '/', len(todo), flush=True)
sv('vc_big_verdict.json', verdict)
sv('vc_big_cls.json', clcache)

out = {}
for key, m in vcmeta.items():
    lang = m['lang']
    ports, seen = [], set()
    for t in bl.get(key, []):
        v = verdict.get(lang + ':' + t)
        if v and v[2] not in seen:
            seen.add(v[2])
            ports.append(v)
    kid = 'wp_' + re.sub(r'[^a-z0-9]', '', (m['en'] or m['title']).lower())[:30]
    while kid in out:
        kid += 'x'
    out[kid] = {'en': m['en'] or m['title'], 'jp': m['jp'], 'country': m['country'], 'kind': 'VC・アクセラレーター', 'desc': m['desc'], 'site': m['site'], 'wiki': [lang, m['title']], 'q': m['q'], 'p': ports[:400]}
sv('vc_big.json', out)
print('VC', len(out), '/ 投資先の記録', sum(len(v['p']) for v in out.values()), '/ 投資先ありのVC', sum(1 for v in out.values() if v['p']))
