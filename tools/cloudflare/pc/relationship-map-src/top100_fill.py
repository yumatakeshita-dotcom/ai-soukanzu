"""注目の100人の、足りない写真・紹介文を、Wikipediaの記事(Wikidata番号が一致するもの)から補う。
Wikidataに記事へのリンクがなくても、名前の検索で見つかり、記事のWikidata番号が同じなら、同一人物として扱う。
写真は、Wikimedia Commonsのライセンスと作者を確認できたものだけ。top100_data.json を更新する。
使い方: python -u top100_fill.py"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
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


def get(u, raw=False):
    for i in range(4):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            return b if raw else json.loads(b)
        except Exception as ex:
            time.sleep(20 if '429' in str(ex) else 3 * (i + 1))
    return None


def clip(t, n=520):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 80 else cut.rstrip() + '…'


filled = {'photo': 0, 'intro': 0}
for e in d:
    if not e.get('q') or (e.get('img') and e.get('intro')):
        continue
    q = e['q']
    found = None
    for lang, name in (('ja', e.get('ja')), ('en', e.get('en'))):
        if not name:
            continue
        r = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': name, 'srlimit': 5, 'formatversion': 2}))
        time.sleep(0.5)
        titles = [x['title'] for x in ((r or {}).get('query', {}).get('search', []))]
        if not titles:
            continue
        r = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'pageprops|extracts|pageimages', 'ppprop': 'wikibase_item', 'exintro': 1, 'explaintext': 1, 'exlimit': 5,
                                                                                      'piprop': 'name', 'redirects': 1, 'titles': '|'.join(titles), 'formatversion': 2}))
        time.sleep(0.5)
        for pg in ((r or {}).get('query', {}).get('pages', [])):
            if (pg.get('pageprops') or {}).get('wikibase_item') == q:
                found = (lang, pg)
                break
        if found:
            break
    if not found:
        print('見つからず(Wikidata番号が一致する記事なし):', e.get('en') or e.get('ja'), flush=True)
        continue
    lang, pg = found
    if not e.get('intro') and pg.get('extract'):
        e['intro'], e['w'], e['t'] = clip(pg['extract']), lang, pg['title']
        filled['intro'] += 1
    if not e.get('img') and pg.get('pageimage'):
        fn = pg['pageimage']
        r = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': 400, 'titles': 'File:' + fn, 'formatversion': 2}))
        time.sleep(0.8)
        try:
            ii = r['query']['pages'][0]['imageinfo'][0]
            md = ii.get('extmetadata', {})
            lic = (md.get('LicenseShortName') or {}).get('value', '')
            if lic and 'fair' not in lic.lower() and 'non-free' not in lic.lower():
                b = get(ii.get('thumburl') or ii.get('url'), raw=True)
                im = Image.open(io.BytesIO(b)).convert('RGB')
                w, h = im.size
                s = min(w, h)
                top = 0 if h > w else (h - s) // 2
                im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((200, 200), Image.LANCZOS)
                im.save(os.path.join(SITE, 'public', 'img', 'q-%s.jpg' % q.lstrip('Q')), 'JPEG', quality=82, optimize=True)
                e['img'] = {'lic': lic, 'artist': re.sub(r'<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()[:80], 'url': ii.get('descriptionurl') or ''}
                filled['photo'] += 1
        except Exception as ex:
            print('写真を取れず', e.get('en'), str(ex)[:60], flush=True)
    print('補った:', e.get('en') or e.get('ja'), '→', lang, pg['title'], flush=True)
json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False)
print('完了 写真', filled['photo'], '/ 紹介文', filled['intro'], flush=True)
