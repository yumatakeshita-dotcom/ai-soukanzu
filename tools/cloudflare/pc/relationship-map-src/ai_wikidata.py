"""Wikidataから、AI分野の会社を、創業者・出資者・CEO・設立年つきで集める。
分野(P452)が「人工知能」「機械学習」「生成AI」「コンピュータビジョン」「自然言語処理」などの会社。
Wikidataの制限(1分に1回程度)があるので、少しずつ・待ちながら取る。途中経過は ai_wikidata.json に毎回保存する(続きから再開できる)。
使い方: python -u ai_wikidata.py"""
import json, os, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(S, 'ai_wikidata.json')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
INDS = ['Q11660', 'Q2539', 'Q117246174', 'Q844240', 'Q30642', 'Q197536', 'Q115305900', 'Q1425977', 'Q189436', 'Q870780', 'Q170978', 'Q741490', 'Q2374463']   # 人工知能, 機械学習, 生成AI, コンピュータビジョン, 自然言語処理, 深層学習, 大規模言語モデル, マシンビジョン, 音声認識, チャットボット, ロボット工学, 自動運転車, データサイエンス
st = json.load(open(F, encoding='utf-8')) if os.path.exists(F) else {'cos': {}, 'rel': {}, 'done': []}


def sparql(q):
    for i in range(8):
        try:
            b = urllib.request.urlopen(urllib.request.Request('https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(q), headers=UA), timeout=180).read()
            return json.loads(b)['results']['bindings']
        except Exception as ex:
            print('ERR', str(ex)[:90], flush=True)
            time.sleep(75 if '429' in str(ex) else 20 * (i + 1))
    return None


def save():
    json.dump(st, open(F, 'w', encoding='utf-8'), ensure_ascii=False)


# ① 会社の一覧(分野ごと・ページごと)
for ind in INDS:
    off = 0
    while True:
        key = '%s:%d' % (ind, off)
        if key in st['done']:
            off += 2000
            continue
        q = ('SELECT ?c ?cLabel ?inc ?web ?ctry WHERE { ?c wdt:P452 wd:%s. ?c wdt:P31/wdt:P279* wd:Q4830453. OPTIONAL{?c wdt:P571 ?inc} OPTIONAL{?c wdt:P856 ?web} OPTIONAL{?c wdt:P17 ?ctry} '
             'SERVICE wikibase:label { bd:serviceParam wikibase:language "ja,en". } } LIMIT 2000 OFFSET %d') % (ind, off)
        rows = sparql(q)
        time.sleep(65)
        if rows is None:
            break
        for b in rows:
            c = b['c']['value'].rsplit('/', 1)[-1]
            e = st['cos'].setdefault(c, {'name': '', 'inc': '', 'web': '', 'ctry': ''})
            e['name'] = b['cLabel']['value']
            e['inc'] = (b.get('inc') or {}).get('value', '')[:4] or e['inc']
            e['web'] = (b.get('web') or {}).get('value', '') or e['web']
            e['ctry'] = (b.get('ctry') or {}).get('value', '').rsplit('/', 1)[-1] or e['ctry']
        st['done'].append(key)
        save()
        print(ind, off, len(rows), '→', len(st['cos']), '社', flush=True)
        if len(rows) < 2000:
            break
        off += 2000
# ② 関係(創業者 P112・出資者 P1951・CEO P169・親会社 P749)。相関図にまだない会社だけを調べる
sys.path.insert(0, S)
import ai_wd_filter
st.setdefault('relq', [])
if not st['relq']:
    allids = sorted(st['cos'])
    for k in st['done']:
        if k.startswith('rel:'):
            i0 = int(k[4:])
            st['relq'] += allids[i0:i0 + 60]
need = [q for q in ai_wd_filter.unmapped(st['cos']) if q not in set(st['relq'])]
print('これから調べる会社', len(need), '社(相関図にない会社だけ)', flush=True)
for i in range(0, len(need), 120):
    ch = need[i:i + 120]
    q = ('SELECT ?c ?p ?pLabel ?rel WHERE { VALUES ?c {%s} '
         '{ ?c wdt:P112 ?p. BIND("創業者" AS ?rel) } UNION { ?c wdt:P1951 ?p. BIND("出資者" AS ?rel) } UNION { ?c wdt:P169 ?p. BIND("CEO" AS ?rel) } UNION { ?c wdt:P749 ?p. BIND("親会社" AS ?rel) } '
         'SERVICE wikibase:label { bd:serviceParam wikibase:language "ja,en". } }') % ' '.join('wd:' + x for x in ch)
    rows = sparql(q)
    time.sleep(65)
    if rows is None:
        continue
    for b in rows:
        c = b['c']['value'].rsplit('/', 1)[-1]
        pp = b['p']['value'].rsplit('/', 1)[-1]
        lst = st['rel'].setdefault(c, [])
        r = {'p': pp, 'name': b['pLabel']['value'], 'rel': b['rel']['value']}
        if r not in lst:
            lst.append(r)
    st['relq'] += ch
    save()
    print('関係', i + len(ch), '/', len(need), flush=True)
print('完了: 会社', len(st['cos']), '社 / 関係のある会社', len(st['rel']), flush=True)
