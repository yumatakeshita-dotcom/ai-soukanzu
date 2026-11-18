"""最重要の100人について、紹介文(Wikipedia)・写真とそのライセンス(Wikimedia Commons)・Wikidataに登録されたSNSを、出典つきで集めて top100_data.json に足す。
写真は 200px の正方形(顔が上寄りの縦長は上から切り出す)にして、サイトの public/img/q-<番号>.jpg に置く。ライセンス・作者・ファイルのページを記録する。
使い方: python -u top100_enrich.py"""
import base64, io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
F = os.path.join(S, 'top100_data.json')
d = json.load(open(F, encoding='utf-8'))
FIX = {'Aidan Gomez': 'Q110864219', 'Junichi Miyakawa': 'Q96713601'}
for e in d:
    if not e['q'] and e['en'] in FIX:
        e['q'] = FIX[e['en']]
        e['how'] = 'Wikidata検索(候補1件・肩書き確認)'


def get(u, raw=False):
    for i in range(5):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            return b if raw else json.loads(b)
        except Exception as ex:
            time.sleep(30 if '429' in str(ex) else 3 * (i + 1))
    return None


qs = [e['q'] for e in d if e['q']]
ents = {}
for i in range(0, len(qs), 40):
    r = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(qs[i:i + 40]), 'props': 'sitelinks|claims|labels|descriptions', 'sitefilter': 'jawiki|enwiki', 'languages': 'ja|en'}))
    ents.update((r or {}).get('entities', {}))
    time.sleep(1)


def clip(t, n=520):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 80 else cut.rstrip() + '…'


# 紹介文
want = {'ja': [], 'en': []}
for e in d:
    en = ents.get(e['q'], {})
    sl = en.get('sitelinks', {})
    e['ja'] = e.get('ja') or en.get('labels', {}).get('ja', {}).get('value', '')
    e['desc'] = en.get('descriptions', {}).get('ja', {}).get('value') or en.get('descriptions', {}).get('en', {}).get('value') or e.get('desc', '')
    if sl.get('jawiki'):
        want['ja'].append((e, sl['jawiki']['title']))
    elif sl.get('enwiki'):
        want['en'].append((e, sl['enwiki']['title']))
for lang, items in want.items():
    for i in range(0, len(items), 20):
        ch = items[i:i + 20]
        r = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'exlimit': 20, 'redirects': 1, 'formatversion': 2, 'titles': '|'.join(t for _, t in ch)}))
        qd = (r or {}).get('query', {})
        norm = {x['from']: x['to'] for x in qd.get('normalized', [])}
        red = {x['from']: x['to'] for x in qd.get('redirects', [])}
        pg = {p['title']: p for p in qd.get('pages', [])}
        for e, t in ch:
            tt = red.get(norm.get(t, t), norm.get(t, t))
            ex = (pg.get(tt) or {}).get('extract', '')
            if ex:
                e['intro'], e['w'], e['t'] = clip(ex), lang, tt
        time.sleep(1)
# 写真とライセンス
os.makedirs(os.path.join(SITE, 'public', 'img'), exist_ok=True)
for e in d:
    cl = ents.get(e['q'], {}).get('claims', {})
    p18 = cl.get('P18', [])
    sns = {}
    for k, p in (('x', 'P2002'), ('ig', 'P2003'), ('yt', 'P2397'), ('web', 'P856')):
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if isinstance(v, str) and v:
                sns[k] = v
                break
    e['sns_wd'] = sns
    if not p18:
        continue
    fn = p18[0].get('mainsnak', {}).get('datavalue', {}).get('value')
    if not fn:
        continue
    r = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': 400, 'titles': 'File:' + fn, 'formatversion': 2}))
    time.sleep(0.8)
    try:
        ii = r['query']['pages'][0]['imageinfo'][0]
    except Exception:
        continue
    md = ii.get('extmetadata', {})
    lic = (md.get('LicenseShortName') or {}).get('value', '')
    art = re.sub(r'<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()[:80]
    if not lic:
        continue
    b = get(ii.get('thumburl') or ii.get('url'), raw=True)
    if not b:
        continue
    try:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        w, h = im.size
        s = min(w, h)
        top = 0 if h > w else (h - s) // 2
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((200, 200), Image.LANCZOS)
        im.save(os.path.join(SITE, 'public', 'img', 'q-%s.jpg' % e['q'].lstrip('Q')), 'JPEG', quality=82, optimize=True)
    except Exception:
        continue
    e['img'] = {'lic': lic, 'artist': art, 'url': ii.get('descriptionurl') or ('https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(fn.replace(' ', '_')))}
    time.sleep(0.8)
json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False)
print('識別番号', sum(1 for e in d if e['q']), '/ 紹介文', sum(1 for e in d if e.get('intro')), '/ 写真(ライセンスつき)', sum(1 for e in d if e.get('img')), '/ WikidataのSNS', sum(1 for e in d if e.get('sns_wd')), flush=True)
