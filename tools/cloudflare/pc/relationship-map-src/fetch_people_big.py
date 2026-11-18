"""Wikidataから、職業ごとに人物(英語版Wikipediaなど2言語以上に記事がある人)を大量に集める。回数制限(1分に1回)に合わせて進める。途中から再開できる。Claude不要。
出力: people_big.jsonl  1行1件 {q(Q番号の数字), en, ja, o(職業キー), sl(言語版の数)}   進み具合: people_big_done.json
使い方: python -u fetch_people_big.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'people_big.jsonl')
DONE = os.path.join(S, 'people_big_done.json')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
OCC = [('politician', 'Q82955'), ('footballer', 'Q937857'), ('actor', 'Q33999'), ('writer', 'Q36180'), ('painter', 'Q1028181'), ('singer', 'Q177220'),
       ('musician', 'Q639669'), ('film director', 'Q2526255'), ('researcher', 'Q1650915'), ('university teacher', 'Q1622272'), ('journalist', 'Q1930187'),
       ('lawyer', 'Q40348'), ('businessperson', 'Q43845'), ('basketball player', 'Q3665646'), ('baseball player', 'Q10871364'), ('ice hockey player', 'Q11774891'),
       ('cyclist', 'Q2309784'), ('composer', 'Q36834'), ('poet', 'Q49757'), ('physician', 'Q39631'), ('engineer', 'Q81096'), ('historian', 'Q201788'),
       ('mathematician', 'Q170790'), ('tennis player', 'Q10833314'), ('swimmer', 'Q10843402'), ('military officer', 'Q189290'), ('judge', 'Q16533'),
       ('television actor', 'Q10798782'), ('film actor', 'Q10800557'), ('stage actor', 'Q2259451'), ('screenwriter', 'Q28389'), ('novelist', 'Q6625963'),
       ('diplomat', 'Q193391'), ('economist', 'Q188094'), ('physicist', 'Q169470'), ('chemist', 'Q593644'), ('biologist', 'Q864503'), ('architect', 'Q42973'),
       ('photographer', 'Q33231'), ('sculptor', 'Q1281618'), ('Catholic priest', 'Q250867'), ('association football manager', 'Q628099'), ('athlete', 'Q2066131'),
       ('sprinter', 'Q11513337'), ('racing driver', 'Q378622'), ('boxer', 'Q11338576'), ('golfer', 'Q11303721'), ('rugby union player', 'Q13141064'),
       ('American football player', 'Q19204627'), ('cricketer', 'Q12299841'), ('voice actor', 'Q214917'), ('manga artist', 'Q191633'), ('idol', 'Q1114973'),
       ('television presenter', 'Q947873'), ('model', 'Q4610556'), ('entrepreneur', 'Q131524'), ('computer scientist', 'Q82594'), ('programmer', 'Q5482740'),
       ('philosopher', 'Q4964182'), ('theologian', 'Q1234713'), ('activist', 'Q15253558'), ('chess player', 'Q10873124'), ('DJ', 'Q130857'),
       ('rapper', 'Q2252262'), ('guitarist', 'Q855091'), ('pianist', 'Q486748'), ('conductor', 'Q158852'), ('opera singer', 'Q2865819')]
PAGE = 2000
MAXPAGES = 100
NL = chr(10)


def query(occ, off):
    return ('SELECT ?p ?l ?ja ?sl WHERE { ?p wdt:P31 wd:Q5; wdt:P106 wd:%s; wikibase:sitelinks ?sl. FILTER(?sl>=2) '
            '?p rdfs:label ?l FILTER(lang(?l)="en") OPTIONAL{?p rdfs:label ?ja FILTER(lang(?ja)="ja")} } LIMIT %d OFFSET %d') % (occ, PAGE, off)


def run(sparql):
    url = 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(sparql)
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=150).read())
        except Exception as e:
            msg = str(e)
            print('待機', msg[:60], flush=True)
            time.sleep(70 if '429' in msg else 20 * (i + 1))
    return None


done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}
for name, occ in OCC:
    off = done.get(occ, 0)
    if off < 0:
        continue
    while True:
        time.sleep(62)
        d = run(query(occ, off))
        if d is None:
            fails = done.get('fail:' + occ, 0) + 1
            done['fail:' + occ] = fails
            if fails >= 3:
                done[occ] = -1
            json.dump(done, open(DONE, 'w', encoding='utf-8'))
            break
        rows = d.get('results', {}).get('bindings', [])
        with open(OUT, 'a', encoding='utf-8') as f:
            for r in rows:
                q = r['p']['value'].rsplit('/Q', 1)[-1]
                e = {'q': int(q) if q.isdigit() else q, 'en': r['l']['value'], 'ja': r.get('ja', {}).get('value', ''), 'o': name, 'sl': int(float(r['sl']['value']))}
                f.write(json.dumps(e, ensure_ascii=False, separators=(',', ':')) + NL)
        print(name, 'offset', off, '→', len(rows), '人', flush=True)
        if len(rows) < PAGE * 0.5 or off + PAGE >= PAGE * MAXPAGES:
            done[occ] = -1
            json.dump(done, open(DONE, 'w', encoding='utf-8'))
            break
        off += PAGE
        done[occ] = off
        json.dump(done, open(DONE, 'w', encoding='utf-8'))
print('完了', flush=True)
