"""VCの代表者・パートナーのうち、Wikidataで本人と特定できた人の、人物ページ用のデータ(紹介文・写真とライセンス・役職)を作る。
本人の特定は、Wikidataの検索結果の説明(職業・国籍)が合うものだけを手で選んでいる(曖昧な人は入れない)。
出力: houjin.sqlite の person / img / person_role、site/public/img/q-<番号>.jpg。--push で、差分だけを D1 に送る。
使い方: python -u gafam_people.py [--push]"""
import io, json, os, re, sqlite3, subprocess, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
DB = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite')
# Q番号: (会社の表示名, 役職)
PEOPLE = {
    'Q4723073': ('Sequoia Capital', 'パートナー(共同スチュワード)'), 'Q7357593': ('Sequoia Capital', 'パートナー'), 'Q5301728': ('Sequoia Capital', 'パートナー'),
    'Q6289985': ('Thrive Capital', '創業者'), 'Q6384918': ('Founders Fund', 'パートナー'), 'Q16885691': ('Founders Fund', 'パートナー'),
    'Q108939818': ('Lightspeed Venture Partners', 'パートナー'), 'Q120765821': ('General Catalyst', '幹部'), 'Q516550': ('General Catalyst', '幹部'),
    'Q50403002': ('Kleiner Perkins', 'パートナー'), 'Q1380459': ('Kleiner Perkins', 'パートナー'),
    'Q6174196': ('Andreessen Horowitz', 'ジェネラル・パートナー'), 'Q5106403': ('Andreessen Horowitz', 'ジェネラル・パートナー'), 'Q23808716': ('Andreessen Horowitz', 'ジェネラル・パートナー'),
    'Q20979231': ('Tiger Global', '創業者'), 'Q113893551': ('Tiger Global', 'パートナー'),
}


def get(u, raw=False):
    for i in range(5):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            return b if raw else json.loads(b)
        except Exception as ex:
            time.sleep(40 if '429' in str(ex) else 3 * (i + 1))
    return None


def clip(t, n=480):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 80 else cut.rstrip() + '…'


qs = list(PEOPLE)
ents = {}
for i in range(0, len(qs), 40):
    r = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'format': 'json', 'ids': '|'.join(qs[i:i + 40]), 'props': 'sitelinks|claims|labels|descriptions', 'sitefilter': 'jawiki|enwiki', 'languages': 'ja|en'}))
    ents.update((r or {}).get('entities', {}))
    time.sleep(1)
out = {}
for q in qs:
    en = ents.get(q, {})
    sl = en.get('sitelinks', {})
    lb = en.get('labels', {})
    out[q] = {'en': (lb.get('en') or {}).get('value', ''), 'ja': (lb.get('ja') or {}).get('value', ''),
              'd': (en.get('descriptions', {}).get('ja') or en.get('descriptions', {}).get('en') or {}).get('value', ''), 'w': '', 't': '', 'intro': ''}
    if sl.get('jawiki'):
        out[q]['w'], out[q]['t'] = 'ja', sl['jawiki']['title']
    elif sl.get('enwiki'):
        out[q]['w'], out[q]['t'] = 'en', sl['enwiki']['title']
for lang in ('ja', 'en'):
    items = [(q, e['t']) for q, e in out.items() if e['w'] == lang]
    for i in range(0, len(items), 20):
        ch = items[i:i + 20]
        r = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'exlimit': 20, 'redirects': 1, 'formatversion': 2, 'titles': '|'.join(t for _, t in ch)}))
        qd = (r or {}).get('query', {})
        norm = {x['from']: x['to'] for x in qd.get('normalized', [])}
        red = {x['from']: x['to'] for x in qd.get('redirects', [])}
        pg = {p['title']: p for p in qd.get('pages', [])}
        for q, t in ch:
            tt = red.get(norm.get(t, t), norm.get(t, t))
            out[q]['intro'] = clip((pg.get(tt) or {}).get('extract', ''))
            out[q]['t'] = tt
        time.sleep(1)
imgs = {}
for q in qs:
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
    artist = re.sub(r'<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()[:80]
    imgs[q] = ('Wikimedia Commons(%s%s)' % (lic, (' / ' + artist) if artist else ''), ii.get('descriptionurl') or '')
    time.sleep(0.8)
db = sqlite3.connect(DB)
for q, e in out.items():
    n = q.lstrip('Q')
    db.execute('INSERT OR REPLACE INTO person VALUES (?,?,?,?,?,?,?)', (n, e['en'], e['ja'], e['d'], e['intro'], e['w'], e['t']))
    db.execute('DELETE FROM person_role WHERE q=? AND company=?', (n, PEOPLE[q][0]))
    db.execute('INSERT INTO person_role VALUES (?,?,?)', (n, PEOPLE[q][0], PEOPLE[q][1]))
    if q in imgs:
        db.execute('INSERT OR REPLACE INTO img VALUES (?,?,?,?)', ('q-' + n, 'jpg', imgs[q][0], imgs[q][1]))
db.commit()
print('人物', len(out), '/ 紹介文', sum(1 for e in out.values() if e['intro']), '/ 写真', len(imgs), flush=True)
json.dump({q: {**e, 'co': PEOPLE[q][0], 'role': PEOPLE[q][1]} for q, e in out.items()}, open(os.path.join(S, 'vcpeople_people.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
if '--push' in sys.argv:
    q1 = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
    L = []
    for q in qs:
        n = q.lstrip('Q')
        r = db.execute('SELECT q,en,ja,d,intro,w,t FROM person WHERE q=?', (n,)).fetchone()
        L.append('INSERT OR REPLACE INTO person VALUES (%s);' % ','.join(q1(x) for x in r))
        L.append('DELETE FROM person_role WHERE q=%s AND company=%s;' % (q1(n), q1(PEOPLE[q][0])))
        L.append('INSERT INTO person_role VALUES (%s,%s,%s);' % (q1(n), q1(PEOPLE[q][0]), q1(PEOPLE[q][1])))
        im = db.execute('SELECT key,ext,src,url FROM img WHERE key=?', ('q-' + n,)).fetchone()
        if im:
            L.append('INSERT OR REPLACE INTO img VALUES (%s);' % ','.join(q1(x) for x in im))
    sql = os.path.join(SITE, 'vcpeople_people.sql')
    open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    o = (p.stdout or '') + (p.stderr or '')
    print('D1', 'OK' if p.returncode == 0 and 'ERROR' not in o else 'NG ' + o[-300:], flush=True)
