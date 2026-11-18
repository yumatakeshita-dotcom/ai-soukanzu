"""people.json の人物(Wikidata)ごとに、短い紹介(Wikidataの説明・Wikipediaの冒頭の文)を集める。Claude不要。途中から再開できる。
  1) Wikidata(wbgetentities, 50件ずつ): 日本語版・英語版Wikipediaの記事名と、短い説明
  2) Wikipedia(action=query&prop=extracts, 20件ずつ): 冒頭の文(日本語版があれば日本語、なければ英語)。長さは最大300文字
出力: people_intro.json  {Q番号: {d: 説明, x: 冒頭の文, w: 'ja'|'en', t: 記事名}}
使い方: python -u fetch_people_intro.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'people_intro.json')
TITLES = os.path.join(S, 'people_titles.json')


def api(base, **p):
    url = base + '?' + urllib.parse.urlencode(p)
    for i in range(8):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            msg = str(e)
            time.sleep(70 if '429' in msg else 5 * (i + 1))
    return {}


def clip(t, n=300):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 60 else cut.rstrip() + '…'


ids = []
seen = set()
for ln in open(os.path.join(S, 'people_wd.jsonl'), encoding='utf-8'):
    try:
        q = json.loads(ln)['p']
    except Exception:
        continue
    if q not in seen:
        seen.add(q)
        ids.append(q)
print('人物', len(ids), flush=True)
titles = json.load(open(TITLES, encoding='utf-8')) if os.path.exists(TITLES) else {}
todo = [q for q in ids if q not in titles]
for i in range(0, len(todo), 50):
    ch = todo[i:i + 50]
    d = api('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ch), props='sitelinks|descriptions', sitefilter='jawiki|enwiki', languages='ja|en')
    for q, e in d.get('entities', {}).items():
        sl = e.get('sitelinks', {})
        ds = e.get('descriptions', {})
        titles[q] = {'ja': sl.get('jawiki', {}).get('title', ''), 'en': sl.get('enwiki', {}).get('title', ''), 'd': ds.get('ja', {}).get('value') or ds.get('en', {}).get('value', '')}
    time.sleep(1)
    if (i // 50) % 10 == 0:
        json.dump(titles, open(TITLES, 'w', encoding='utf-8'), ensure_ascii=False)
        print('記事名', i, '/', len(todo), flush=True)
json.dump(titles, open(TITLES, 'w', encoding='utf-8'), ensure_ascii=False)
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
for w, base in (('ja', 'https://ja.wikipedia.org/w/api.php'), ('en', 'https://en.wikipedia.org/w/api.php')):
    want = [(q, t[w]) for q, t in titles.items() if t[w] and q not in res and (w == 'ja' or not t['ja'])]
    print(w, '本文', len(want), flush=True)
    for i in range(0, len(want), 20):
        ch = want[i:i + 20]
        d = api(base, action='query', format='json', prop='extracts', exintro=1, explaintext=1, exlimit=20, redirects=1, titles='|'.join(t for _, t in ch), formatversion=2)
        qd = d.get('query', {})
        norm = {x['from']: x['to'] for x in qd.get('normalized', [])}
        red = {x['from']: x['to'] for x in qd.get('redirects', [])}
        pg = {p['title']: p for p in qd.get('pages', [])}
        for q, t in ch:
            tt = red.get(norm.get(t, t), norm.get(t, t))
            ex = (pg.get(tt) or {}).get('extract', '')
            if ex:
                res[q] = {'d': titles[q]['d'], 'x': clip(ex), 'w': w, 't': tt}
        time.sleep(1.2)
        if (i // 20) % 10 == 0:
            json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
            print(w, i, '/', len(want), flush=True)
for q, t in titles.items():      # 記事が無い人は、説明だけ
    if q not in res and t['d']:
        res[q] = {'d': t['d'], 'x': '', 'w': '', 't': ''}
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('完了', len(res), flush=True)
