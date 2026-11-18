"""各社の子会社・買収した会社をWikidata(親会社 P749 / 所有者 P127)から集める。Claude不要。途中から再開できる。
出力: acq_wd.json  {図のキー: [[会社名, 年(不明は0), 種類, 終了年(0=現在), 英語名], ...]}
使い方: python fetch_acq_wd.py   (全社で30分前後。429が出たら自動で待つ)"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
OUT = os.path.join(S, 'acq_wd.json')
QF = os.path.join(S, 'acq_qid.json')
ALIAS = {'Alphabet': 'Alphabet Inc.', 'Meta': 'Meta Platforms', 'X (Twitter)': 'Twitter', 'ADP': 'Automatic Data Processing',
         'BNY': 'BNY Mellon', 'RTX': 'RTX Corporation', 'GE Aerospace': 'GE Aerospace', 'Walt Disney': 'The Walt Disney Company',
         'AMD': 'AMD', '楽天グループ': 'Rakuten', 'ソフトバンクグループ': 'SoftBank Group', 'LINEヤフー': 'LY Corporation',
         'メルカリ': 'Mercari', 'ソフトバンク': 'SoftBank Corp.', 'Slack': 'Slack Technologies', 'Nvidia': 'Nvidia',
         'Salesforce': 'Salesforce', 'Cursor (Anysphere)': 'Anysphere', 'Arm': 'Arm Holdings', 'PayPay': 'PayPay', 'Apple': 'Apple Inc.',
         'Microsoft': 'Microsoft', 'Amazon': 'Amazon (company)', 'Tesla': 'Tesla, Inc.', 'Visa': 'Visa Inc.', 'Boeing': 'Boeing',
         'Intel': 'Intel', 'Oracle': 'Oracle Corporation', 'Cisco': 'Cisco', 'Meta Platforms': 'Meta Platforms', 'Uber': 'Uber',
         'Stripe': 'Stripe, Inc.', 'Figma': 'Figma', 'Canva': 'Canva', 'Notion': 'Notion (productivity software)', 'OpenAI': 'OpenAI',
         'Anthropic': 'Anthropic', 'Databricks': 'Databricks', 'Waymo': 'Waymo', 'Scale AI': 'Scale AI', 'xAI': 'XAI (company)',
         'Perplexity': 'Perplexity AI', 'Cohere': 'Cohere', 'Hugging Face': 'Hugging Face', 'DoorDash': 'DoorDash', 'Discord': 'Discord',
         'Plaid': 'Plaid (company)', 'Klarna': 'Klarna', 'Revolut': 'Revolut', 'ByteDance': 'ByteDance', 'Epic Games': 'Epic Games',
         'Fanatics': 'Fanatics (company)', 'DJI': 'DJI', 'Celonis': 'Celonis', 'Anduril Industries': 'Anduril Industries',
         'Cerebras': 'Cerebras', 'CoreWeave': 'CoreWeave', 'Checkout.com': 'Checkout.com', 'SpaceX': 'SpaceX', 'Palantir': 'Palantir Technologies',
         'Walmart': 'Walmart', 'Chevron': 'Chevron Corporation', 'ExxonMobil': 'ExxonMobil', 'Costco': 'Costco', 'Visa ': 'Visa Inc.'}


def api(url):
    for i in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read())
        except Exception as e:
            if '429' in str(e):
                print('429: 65秒待ちます', flush=True)
                time.sleep(65)
            else:
                time.sleep(4 * (i + 1))
    return None


names = {}
for ln in open(os.path.join(S, 'acq_names.txt'), encoding='utf-8'):
    ln = ln.strip()
    if '=' in ln:
        k, n = ln.split('=', 1)
        names[k] = ALIAS.get(n, n)

# 1) 記事名 → Wikidata Q番号
qid = json.load(open(QF, encoding='utf-8')) if os.path.exists(QF) else {}
todo = [k for k in names if k not in qid]
for i in range(0, len(todo), 50):
    ch = todo[i:i + 50]
    tt = [names[k] for k in ch]
    d = api('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(
        {'action': 'query', 'format': 'json', 'titles': '|'.join(tt), 'redirects': 1, 'prop': 'pageprops', 'ppprop': 'wikibase_item', 'formatversion': 2}))
    q = (d or {}).get('query', {})
    norm = {x['from']: x['to'] for x in q.get('normalized', [])}
    red = {x['from']: x['to'] for x in q.get('redirects', [])}
    pages = {p['title']: p for p in q.get('pages', [])}
    for k in ch:
        t = norm.get(names[k], names[k])
        t = red.get(t, t)
        pg = pages.get(t)
        qid[k] = (pg or {}).get('pageprops', {}).get('wikibase_item', '') if pg else ''
    json.dump(qid, open(QF, 'w', encoding='utf-8'))
    time.sleep(1)
print('Q番号', sum(1 for v in qid.values() if v), '/', len(qid), flush=True)

# 2) 子会社(親会社・所有者がこの会社の組織)
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
yr = lambda s: int(s.lstrip('+')[:4]) if s and re.match(r'^[+-]?\d{4}', s) else 0
pend = [k for k, q in qid.items() if q and k not in res]
rev = {qid[k]: k for k in pend}
BATCH = 6
for i in range(0, len(pend), BATCH):
    ch = pend[i:i + BATCH]
    vals = ' '.join('wd:' + qid[k] for k in ch)
    sp = ('SELECT ?p ?s ?el ?jl ?inc ?a ?b ?tl WHERE { VALUES ?p { %s } { ?s p:P749 ?st . ?st ps:P749 ?p } UNION { ?s p:P127 ?st . ?st ps:P127 ?p } '
          'FILTER NOT EXISTS { ?s wdt:P31 wd:Q5 } OPTIONAL{?st pq:P580 ?a} OPTIONAL{?st pq:P582 ?b} OPTIONAL{?s wdt:P571 ?inc} '
          'OPTIONAL{?s rdfs:label ?el FILTER(lang(?el)="en")} OPTIONAL{?s rdfs:label ?jl FILTER(lang(?jl)="ja")} '
          'OPTIONAL{?s wdt:P31 ?t. ?t rdfs:label ?tl FILTER(lang(?tl)="en")} } LIMIT 30000') % vals
    d = api('https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(sp))
    if d is None:
        print(ch, '失敗(あとで再開)', flush=True)
        time.sleep(60)
        continue
    ms = {k: {} for k in ch}
    for b in d['results']['bindings']:
        g = lambda x: b.get(x, {}).get('value')
        k = rev.get(g('p').rsplit('/', 1)[-1])
        sid = g('s').rsplit('/', 1)[-1]
        name = g('jl') or g('el')
        if not k or not name or re.fullmatch(r'Q\d+', name):
            continue
        o = ms[k].setdefault(sid, {'n': name, 'en': g('el') or '', 'a': 0, 'e': 0, 'inc': 0, 't': []})
        if g('a'):
            o['a'] = yr(g('a'))
        if g('b'):
            o['e'] = yr(g('b'))
        if g('inc'):
            o['inc'] = yr(g('inc'))
        if g('tl') and g('tl') not in o['t']:
            o['t'].append(g('tl'))
    for k in ch:
        rows = [[o['n'], o['a'], (o['t'] or [''])[0], o['e'], o['en']] for o in ms[k].values()]
        rows.sort(key=lambda r: (r[1] or 9999, r[0]))
        res[k] = rows
        print(k, len(rows), flush=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    time.sleep(20)
print('完了 会社', len(res), '件数', sum(len(v) for v in res.values()))
