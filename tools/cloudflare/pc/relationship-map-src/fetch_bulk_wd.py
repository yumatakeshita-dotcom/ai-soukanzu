"""Wikidataから、国ごとの会社(英語名・設立年)を大量に集める。Wikidataの回数制限(1分に1回)に合わせてゆっくり進める。途中から再開できる。Claude不要。
出力: wd_bulk.jsonl  1行1件 {q, en, ja, c(国), inc(設立年), ind, web}   進み具合: wd_bulk_done.json
使い方: python -u fetch_bulk_wd.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'wd_bulk.jsonl')
DONE = os.path.join(S, 'wd_bulk_done.json')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
COUNTRIES = [('United States', 'Q30'), ('Japan', 'Q17'), ('United Kingdom', 'Q145'), ('Germany', 'Q183'), ('France', 'Q142'), ('India', 'Q668'), ('China', 'Q148'), ('Canada', 'Q16'),
 ('Australia', 'Q408'), ('Italy', 'Q38'), ('Spain', 'Q29'), ('South Korea', 'Q884'), ('Brazil', 'Q155'), ('Netherlands', 'Q55'), ('Sweden', 'Q34'), ('Switzerland', 'Q39'),
 ('Russia', 'Q159'), ('Mexico', 'Q96'), ('Indonesia', 'Q252'), ('Turkey', 'Q43'), ('Singapore', 'Q334'), ('Israel', 'Q801'), ('South Africa', 'Q258'), ('Nigeria', 'Q1033'),
 ('Kenya', 'Q114'), ('Egypt', 'Q79'), ('United Arab Emirates', 'Q878'), ('Saudi Arabia', 'Q851'), ('Taiwan', 'Q865'), ('Hong Kong', 'Q8646'), ('Thailand', 'Q869'), ('Vietnam', 'Q881'),
 ('Malaysia', 'Q833'), ('Philippines', 'Q928'), ('Poland', 'Q36'), ('Norway', 'Q20'), ('Denmark', 'Q35'), ('Finland', 'Q33'), ('Ireland', 'Q27'), ('Austria', 'Q40'), ('Belgium', 'Q31'),
 ('Portugal', 'Q45'), ('Greece', 'Q41'), ('Czech Republic', 'Q213'), ('New Zealand', 'Q664'), ('Argentina', 'Q414'), ('Chile', 'Q298'), ('Colombia', 'Q739'), ('Pakistan', 'Q843'),
 ('Bangladesh', 'Q902'), ('Ukraine', 'Q212'), ('Romania', 'Q218'), ('Hungary', 'Q28'), ('Ghana', 'Q117'), ('Tanzania', 'Q924'), ('Ethiopia', 'Q115'), ('Morocco', 'Q1028'),
 ('Algeria', 'Q262'), ('Tunisia', 'Q948'), ('Uganda', 'Q1036'), ('Rwanda', 'Q1037'), ('Sri Lanka', 'Q854'), ('Iran', 'Q794'), ('Kazakhstan', 'Q232'), ('Peru', 'Q419'),
 ('Luxembourg', 'Q32'), ('Cyprus', 'Q229'), ('Qatar', 'Q846'), ('Kuwait', 'Q817'), ('Jordan', 'Q810'), ('Senegal', 'Q1041'), ('Ivory Coast', 'Q1008'), ('Cameroon', 'Q1009')]
CLASSES = ['Q4830453', 'Q783794', 'Q891723', 'Q6881511']      # business / company / public company / enterprise
PAGE = 5000
MAXPAGES = 8      # まず各国・各種類で40,000件まで(広く浅く)。足りなければ上げて再実行
NL = chr(10)


def query(cq, off, cls):
    return ('SELECT ?c ?l ?inc WHERE { ?c wdt:P31 wd:%s; wdt:P17 wd:%s. ?c rdfs:label ?l FILTER(lang(?l)="en") OPTIONAL{?c wdt:P571 ?inc} } LIMIT %d OFFSET %d') % (cls, cq, PAGE, off)


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


done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}
for cls in CLASSES:
    for name, cq in COUNTRIES:
        key = cls + ':' + cq
        off = done.get(key, 0)
        if off < 0:
            continue
        while True:
            time.sleep(65)      # 回数制限(1分に1回)
            d = run(query(cq, off, cls))
            if d is None:
                break
            rows = d.get('results', {}).get('bindings', [])
            by = {}
            for r in rows:
                qid = r['c']['value'].rsplit('/', 1)[-1]
                e = by.setdefault(qid, {'q': qid, 'en': r['l']['value'], 'ja': '', 'c': name, 'inc': 0, 'ind': '', 'web': ''})
                if 'inc' in r:
                    m = re.match(r'^[+-]?(\d{4})', r['inc']['value'])
                    if m and not e['inc']:
                        e['inc'] = int(m.group(1))
            with open(OUT, 'a', encoding='utf-8') as f:
                for e in by.values():
                    f.write(json.dumps(e, ensure_ascii=False, separators=(',', ':')) + NL)
            print(cls, name, 'offset', off, '→', len(by), '社', flush=True)
            if len(rows) < PAGE * 0.5 or off + PAGE >= PAGE * MAXPAGES:
                done[key] = -1
                json.dump(done, open(DONE, 'w', encoding='utf-8'))
                break
            off += PAGE
            done[key] = off
            json.dump(done, open(DONE, 'w', encoding='utf-8'))
print('完了', flush=True)
