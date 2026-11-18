"""people.json の人物(Wikidata由来)の顔写真を、Wikidataの画像(P18, Wikimedia Commons)から集める。途中から再開できる。Claude不要。
出力: faces_wp.json  {Q番号: data URI(96px JPEG)}   進み具合: faces_wp_done.json
使い方: python -u fetch_faces_wp.py"""
import base64, io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/sparql-results+json'}
OUT = os.path.join(S, 'faces_wp.json')
DONE = os.path.join(S, 'faces_wp_done.json')
qs = [r[0] for r in json.load(open(os.path.join(S, 'web', 'people.json'), encoding='utf-8'))['rows']]
out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
done = set(json.load(open(DONE, encoding='utf-8'))) if os.path.exists(DONE) else set()


def get(u, accept=None, tries=4):
    for i in range(tries):
        try:
            h = dict(UA)
            if accept:
                h['Accept'] = accept
            return urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=60).read()
        except Exception as e:
            m = str(e)
            if '404' in m:
                return None
            time.sleep(25 if '429' in m else 5 * (i + 1))
    return None


def shrink(b):
    try:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        w, h = im.size
        s = min(w, h)
        top = 0 if h > w else (h - s) // 2
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((96, 96), Image.LANCZOS)
        o = io.BytesIO()
        im.save(o, 'JPEG', quality=62, optimize=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()
    except Exception:
        return None


todo = [q for q in qs if q not in done]
print('人物', len(qs), '未処理', len(todo), flush=True)
for i in range(0, len(todo), 300):
    ch = todo[i:i + 300]
    sp = 'SELECT ?p ?img WHERE { VALUES ?p {%s} ?p wdt:P18 ?img }' % ' '.join('wd:' + q for q in ch)
    time.sleep(62)
    b = get('https://query.wikidata.org/sparql?format=json&query=' + urllib.parse.quote(sp), 'application/sparql-results+json')
    if not b:
        print('失敗', i, flush=True)
        continue
    rows = json.loads(b)['results']['bindings']
    seen = {}
    for r in rows:
        q = r['p']['value'].rsplit('/', 1)[-1]
        seen.setdefault(q, r['img']['value'])
    # 画像の場所(サムネイルのURL)を50件まとめて聞き、本体は upload.wikimedia.org から取る(1枚ずつ Commons に聞くと回数制限に当たる)
    items = [(q, urllib.parse.unquote(u.rsplit('/', 1)[-1])) for q, u in seen.items() if q not in out]
    for j in range(0, len(items), 50):
        part = items[j:j + 50]
        titles = '|'.join('File:' + fn.replace('_', ' ') for _, fn in part)
        api = ('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=url&iiurlwidth=160&titles=' + urllib.parse.quote(titles))
        ab = get(api)
        if not ab:
            continue
        pages = json.loads(ab).get('query', {}).get('pages', {})
        norm = {x['from']: x['to'] for x in json.loads(ab).get('query', {}).get('normalized', [])}
        thumb = {}
        for pg in pages.values():
            ii = (pg.get('imageinfo') or [{}])[0]
            if ii.get('thumburl') or ii.get('url'):
                thumb[pg.get('title', '')] = ii.get('thumburl') or ii.get('url')
        for q, fn in part:
            t = 'File:' + fn.replace('_', ' ')
            tu = thumb.get(norm.get(t, t))
            if not tu:
                continue
            bb = get(tu)
            time.sleep(0.3)
            d = shrink(bb) if bb else None
            if d:
                out[q] = d
        json.dump(out, open(OUT, 'w', encoding='utf-8'), separators=(',', ':'))
    done.update(ch)
    json.dump(out, open(OUT, 'w', encoding='utf-8'), separators=(',', ':'))
    json.dump(sorted(done), open(DONE, 'w', encoding='utf-8'))
    print('進み', min(i + 300, len(todo)), '/', len(todo), '写真', len(out), flush=True)
print('完了', len(out), flush=True)
