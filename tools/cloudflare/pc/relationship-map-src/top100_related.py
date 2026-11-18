"""最重要の100人の「関係する人物」(配偶者・元配偶者・兄弟姉妹・共同創業者)を、Wikidataから集めて、その人たちのページも作れるようにする。
載せる基準: Wikidataに項目がある人(=公に記録がある人)だけ。親・子は載せない(私生活の保護)。関係の出典は Wikidata の記録。
出力: top100_related.json {Q: [{r: 相手のQ, rel: '配偶者'|'元配偶者'|'兄弟姉妹'|'共同創業者'}]}, top100_people_extra.json (相手の人物の情報: ja,en,desc,intro,w,t,img)
使い方: python -u top100_related.py"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
d = json.load(open(os.path.join(S, 'top100_data.json'), encoding='utf-8'))
qs = [e['q'] for e in d if e['q']]
top = set(qs)
def mk(chunk):
    return ('SELECT ?p ?r ?rel WHERE { VALUES ?p {%s} '
      '{ ?p p:P26 ?st. ?st ps:P26 ?r. OPTIONAL{?st pq:P582 ?end} BIND(IF(BOUND(?end),"元配偶者","配偶者") AS ?rel) } '
      'UNION { ?p wdt:P3373 ?r. BIND("兄弟姉妹" AS ?rel) } '
      
      '?r wdt:P31 wd:Q5 }') % ' '.join('wd:' + q for q in chunk)


def mkf(chunk):
    return ('SELECT ?p ?r ?rel WHERE { VALUES ?p {%s} ?c wdt:P112 ?p. ?c wdt:P112 ?r. FILTER(?r != ?p) BIND("共同創業者" AS ?rel) ?r wdt:P31 wd:Q5 }') % ' '.join('wd:' + q for q in chunk)


def get(u, accept=None, raw=False):
    h = dict(UA)
    if accept:
        h['Accept'] = accept
    for i in range(5):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=120).read()
            return b if raw else json.loads(b)
        except Exception as ex:
            print('ERR', str(ex)[:100], flush=True)
            time.sleep(70 if '429' in str(ex) else 5 * (i + 1))
    return None


rel = {}
HUM = {}
for i in range(0, len(qs), 40):
    j = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(qs[i:i + 40]), 'props': 'claims', 'languages': 'en'}))
    for q, en in ((j or {}).get('entities', {})).items():
        cl = en.get('claims', {})
        for st in cl.get('P26', []):
            v = (st.get('mainsnak', {}).get('datavalue') or {}).get('value')
            if isinstance(v, dict) and v.get('id'):
                ended = bool(st.get('qualifiers', {}).get('P582'))
                rel.setdefault(q, []).append({'r': v['id'], 'rel': '元配偶者' if ended else '配偶者'})
        for st in cl.get('P3373', []):
            v = (st.get('mainsnak', {}).get('datavalue') or {}).get('value')
            if isinstance(v, dict) and v.get('id'):
                rel.setdefault(q, []).append({'r': v['id'], 'rel': '兄弟姉妹'})
    time.sleep(1)
# 相手が人間(P31=Q5)かを確認
cand = sorted({x['r'] for v in rel.values() for x in v})
for i in range(0, len(cand), 40):
    j = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(cand[i:i + 40]), 'props': 'claims', 'languages': 'en'}))
    for q, en in ((j or {}).get('entities', {})).items():
        HUM[q] = any(((st.get('mainsnak', {}).get('datavalue') or {}).get('value') or {}).get('id') == 'Q5' for st in en.get('claims', {}).get('P31', []))
    time.sleep(1)
rel = {p: [x for x in v if HUM.get(x['r'])] for p, v in rel.items()}
rel = {p: v for p, v in rel.items() if v}
print('関係', sum(len(v) for v in rel.values()), '件 / 関係のある人', len(rel), flush=True)
# 共同創業者(SPARQL。混雑で失敗しやすいので、失敗した塊は飛ばす)
if '--no-cofounder' not in sys.argv:
    for i in range(0, len(qs), 20):
        r = None
        for _try in range(3):
            try:
                u = 'https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(mkf(qs[i:i + 20]))
                r = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read())
                break
            except Exception as ex:
                print('共同創業者: 再試行', i, _try, str(ex)[:50], flush=True)
                time.sleep(70)
        if r is None:
            print('共同創業者の取得を飛ばす', i, flush=True)
            continue
        for b in r.get('results', {}).get('bindings', []):
            p = b['p']['value'].rsplit('/', 1)[-1]
            rq = b['r']['value'].rsplit('/', 1)[-1]
            rel.setdefault(p, [])
            if not any(x['r'] == rq for x in rel[p]):
                rel[p].append({'r': rq, 'rel': '共同創業者'})
        time.sleep(62)
    print('共同創業者を足した後の関係', sum(len(v) for v in rel.values()), flush=True)
others = sorted({x['r'] for v in rel.values() for x in v} - top)
print('関係', sum(len(v) for v in rel.values()), '件 / 100人以外の相手', len(others), flush=True)
# 相手が多すぎる(会社の創業者が多数)人は、共同創業者を最大6人に絞る
for p, v in rel.items():
    cf = [x for x in v if x['rel'] == '共同創業者']
    if len(cf) > 6:
        keep = [x for x in cf if x['r'] in top][:6]
        for x in cf:
            if len(keep) >= 6:
                break
            if x not in keep:
                keep.append(x)
        rel[p] = [x for x in v if x['rel'] != '共同創業者'] + keep
others = sorted({x['r'] for v in rel.values() for x in v} - top)
json.dump(rel, open(os.path.join(S, 'top100_related.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('絞り込み後の相手(100人以外)', len(others), flush=True)

ents = {}
for i in range(0, len(others), 40):
    j = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(others[i:i + 40]), 'props': 'sitelinks|claims|labels|descriptions', 'sitefilter': 'jawiki|enwiki', 'languages': 'ja|en'}))
    ents.update((j or {}).get('entities', {}))
    time.sleep(1)


def clip(t, n=480):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 80 else cut.rstrip() + '…'


extra = {}
want = {'ja': [], 'en': []}
for q in others:
    en = ents.get(q, {})
    sl = en.get('sitelinks', {})
    lb = en.get('labels', {})
    e = {'q': q, 'en': (lb.get('en') or {}).get('value', ''), 'ja': (lb.get('ja') or {}).get('value', ''), 'desc': (en.get('descriptions', {}).get('ja') or en.get('descriptions', {}).get('en') or {}).get('value', '')}
    extra[q] = e
    if sl.get('jawiki'):
        want['ja'].append((e, sl['jawiki']['title']))
    elif sl.get('enwiki'):
        want['en'].append((e, sl['enwiki']['title']))
for lang, items in want.items():
    for i in range(0, len(items), 20):
        ch = items[i:i + 20]
        j = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'exlimit': 20, 'redirects': 1, 'formatversion': 2, 'titles': '|'.join(t for _, t in ch)}))
        qd = (j or {}).get('query', {})
        norm = {x['from']: x['to'] for x in qd.get('normalized', [])}
        red = {x['from']: x['to'] for x in qd.get('redirects', [])}
        pg = {p['title']: p for p in qd.get('pages', [])}
        for e, t in ch:
            tt = red.get(norm.get(t, t), norm.get(t, t))
            ex = (pg.get(tt) or {}).get('extract', '')
            if ex:
                e['intro'], e['w'], e['t'] = clip(ex), lang, tt
        time.sleep(1)
for q in others:
    e = extra[q]
    p18 = ents.get(q, {}).get('claims', {}).get('P18', [])
    fn = p18 and p18[0].get('mainsnak', {}).get('datavalue', {}).get('value')
    if not fn:
        continue
    j = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': 400, 'titles': 'File:' + fn, 'formatversion': 2}))
    time.sleep(0.8)
    try:
        ii = j['query']['pages'][0]['imageinfo'][0]
    except Exception:
        continue
    md = ii.get('extmetadata', {})
    lic = (md.get('LicenseShortName') or {}).get('value', '')
    if not lic:
        continue
    b = get(ii.get('thumburl') or ii.get('url'), raw=True)
    if not b:
        continue
    try:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        w, h = im.size
        s = min(w, h)
        top0 = 0 if h > w else (h - s) // 2
        im = im.crop(((w - s) // 2, top0, (w - s) // 2 + s, top0 + s)).resize((200, 200), Image.LANCZOS)
        im.save(os.path.join(SITE, 'public', 'img', 'q-%s.jpg' % q.lstrip('Q')), 'JPEG', quality=82, optimize=True)
    except Exception:
        continue
    e['img'] = {'lic': lic, 'artist': re.sub(r'<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()[:80], 'url': ii.get('descriptionurl') or ''}
    time.sleep(0.8)
json.dump(extra, open(os.path.join(S, 'top100_people_extra.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('完了: 相手', len(extra), '人 / 紹介文', sum(1 for e in extra.values() if e.get('intro')), '/ 写真', sum(1 for e in extra.values() if e.get('img')), flush=True)
