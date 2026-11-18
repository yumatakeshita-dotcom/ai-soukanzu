"""Wikidataから、会社の創業者(P112)・CEO(P169)・会長(P488)になっている人物(英語版などに多く記事がある有名人)を集める。回数制限(1分に1回)に合わせて進める。途中から再開できる。Claude不要。
出力: people_wd.jsonl  1行1件 {p(Q番号), en, ja, c(会社名), role, sl(言語版の数)}   進み具合: people_wd_done2.json
使い方: python -u fetch_people_wd.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'people_wd.jsonl')
DONE = os.path.join(S, 'people_wd_done3.json')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
ROLES = [('P488', 'chair', 4), ('P3320', 'board', 4), ('P169', 'ceo', 4)]      # (性質, 役割, 最大ページ数)
MIN_SL = 3          # 言語版の記事数がこれ以上の人物だけ(有名人に絞る)
PAGE = 5000
CLS = 'wd:Q4830453 wd:Q783794 wd:Q891723 wd:Q6881511 wd:Q1589009'


def query(prop, off):
    return ('SELECT ?p ?pl ?pja ?cl ?sl WHERE { VALUES ?cls {%s} ?c wdt:P31 ?cls; wdt:%s ?p. ?p wdt:P31 wd:Q5; wikibase:sitelinks ?sl. FILTER(?sl>=%d) '
            '?p rdfs:label ?pl FILTER(lang(?pl)="en") ?c rdfs:label ?cl FILTER(lang(?cl)="en") OPTIONAL{?p rdfs:label ?pja FILTER(lang(?pja)="ja")} } LIMIT %d OFFSET %d') % (CLS, prop, MIN_SL, PAGE, off)


def run(sparql):
    url = 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(sparql)
    for i in range(8):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120).read())
        except Exception as e:
            msg = str(e)
            print('待機', msg[:60], flush=True)
            time.sleep(70 if '429' in msg else 30 * (i + 1))
    return None


NL = chr(10)
done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}
for prop, role, maxpages in ROLES:
    off = done.get(prop, 0)
    while off >= 0:
        time.sleep(65)
        d = run(query(prop, off))
        if d is None:
            break
        rows = d.get('results', {}).get('bindings', [])
        with open(OUT, 'a', encoding='utf-8') as f:
            for r in rows:
                e = {'p': r['p']['value'].rsplit('/', 1)[-1], 'en': r['pl']['value'], 'ja': r.get('pja', {}).get('value', ''), 'c': r['cl']['value'], 'role': role, 'sl': int(float(r['sl']['value']))}
                f.write(json.dumps(e, ensure_ascii=False, separators=(',', ':')) + NL)
        print(role, 'offset', off, '→', len(rows), '件', flush=True)
        if len(rows) < PAGE * 0.5 or off + PAGE >= PAGE * maxpages:
            done[prop] = -1
            json.dump(done, open(DONE, 'w', encoding='utf-8'))
            break
        off += PAGE
        done[prop] = off
        json.dump(done, open(DONE, 'w', encoding='utf-8'))
print('完了', flush=True)
