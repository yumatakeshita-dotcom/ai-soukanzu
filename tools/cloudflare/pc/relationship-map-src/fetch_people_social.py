"""人物(people.json の6,472人)のSNS・公式サイトを、Wikidataから集める。 X(P2002)・Instagram(P2003)・YouTubeチャンネルID(P2397)・公式サイト(P856)。
回数制限(1分に1回)に合わせて、400人ずつ。途中から再開できる。Claude不要。
出力: people_social.json  {Q番号: {x, ig, yt, web}}   進み具合: people_social_done.json
使い方: python -u fetch_people_social.py"""
import json, os, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
OUT = os.path.join(S, 'people_social.json')
DONE = os.path.join(S, 'people_social_done.json')
qs = [r[0] for r in json.load(open(os.path.join(S, 'web', 'people.json'), encoding='utf-8'))['rows']]
out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
done = set(json.load(open(DONE, encoding='utf-8'))) if os.path.exists(DONE) else set()
todo = [q for q in qs if q not in done]
print('人物', len(qs), '未処理', len(todo), flush=True)
for i in range(0, len(todo), 400):
    ch = todo[i:i + 400]
    sp = ('SELECT ?p ?x ?ig ?yt ?web WHERE { VALUES ?p {%s} OPTIONAL{?p wdt:P2002 ?x} OPTIONAL{?p wdt:P2003 ?ig} OPTIONAL{?p wdt:P2397 ?yt} OPTIONAL{?p wdt:P856 ?web} '
          'FILTER(BOUND(?x)||BOUND(?ig)||BOUND(?yt)||BOUND(?web)) }') % ' '.join('wd:' + q for q in ch)
    data = None
    for t in range(4):
        time.sleep(62)
        try:
            data = json.loads(urllib.request.urlopen(urllib.request.Request('https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(sp), headers=UA), timeout=120).read())
            break
        except Exception as e:
            print('待機', str(e)[:60], flush=True)
            time.sleep(40 * (t + 1))
    if data is None:
        continue
    for r in data['results']['bindings']:
        q = r['p']['value'].rsplit('/', 1)[-1]
        e = out.setdefault(q, {})
        for k in ('x', 'ig', 'yt', 'web'):
            if k in r and not e.get(k):
                e[k] = r[k]['value']
    done.update(ch)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    json.dump(sorted(done), open(DONE, 'w', encoding='utf-8'))
    print('進み', len(done), '/', len(qs), 'SNSあり', len(out), flush=True)
print('完了', len(out), flush=True)
