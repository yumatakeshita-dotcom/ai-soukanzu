"""独自サイト用に、①人物の顔写真を画像ファイル(site/public/img)に書き出し、②人物の表(person・person_role・img)を houjin.sqlite に作る。
画像の名前: 相関図の人物 → m-<英語名の英数字とハイフン>.jpg、Wikidata由来の人物 → q-<Q番号の数字>.jpg
使い方: python -I build_site_assets.py <houjin.sqlite> <サイトのフォルダ>"""
import base64, json, os, re, sqlite3, sys
S = os.path.dirname(os.path.abspath(__file__))
dbp, site = sys.argv[1], sys.argv[2]
imgdir = os.path.join(site, 'public', 'img')
os.makedirs(imgdir, exist_ok=True)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')[:60]


def save(key, data_uri):
    m = re.match(r'data:image/(jpeg|png|webp);base64,(.+)$', data_uri or '', flags=re.S)
    if not m:
        return False
    raw = base64.b64decode(m.group(2))
    ext = 'jpg' if m.group(1) == 'jpeg' else m.group(1)
    for old in ('jpg', 'png', 'webp'):
        pth = os.path.join(imgdir, key + '.' + old)
        if old != ext and os.path.exists(pth):
            os.replace(pth, pth + '.bak') if False else None
    open(os.path.join(imgdir, key + '.' + ext), 'wb').write(raw)
    return ext


db = sqlite3.connect(dbp)
for t in ('person', 'person_role', 'img'):
    db.execute('DROP TABLE IF EXISTS ' + t)
db.execute('CREATE TABLE img (key TEXT PRIMARY KEY, ext TEXT, src TEXT, url TEXT)')
imgs = {}
# 1) 相関図の人物(Wikipedia以外: X・Commons・公式サイト)
for en, v in json.load(open(os.path.join(S, 'web', 'faces.json'), encoding='utf-8')).items():
    k = 'm-' + slug(en)
    ext = save(k, v.get('i'))
    if ext:
        imgs[k] = (ext, v.get('s', ''), v.get('u', ''))
# 2) 相関図の人物(Wikipediaの記事の写真。以前に集めたもの)
op = os.path.join(S, 'out_photos.json')
if os.path.exists(op):
    for en, v in json.load(open(op, encoding='utf-8')).items():
        k = 'm-' + slug(en)
        if k in imgs:
            continue
        ext = save(k, v.get('img'))
        if ext:
            imgs[k] = (ext, 'Wikipedia', v.get('wiki', ''))
# 3) Wikidata由来の人物(Wikimedia Commons)
wp = {}
for i in range(3):
    p = os.path.join(S, 'web', 'faces_wp_%d.json' % i)
    if os.path.exists(p):
        wp.update(json.load(open(p)))
for q, uri in wp.items():
    k = 'q-' + q.lstrip('Q')
    ext = save(k, uri)
    if ext:
        imgs[k] = (ext, 'Wikimedia Commons', 'https://www.wikidata.org/wiki/' + q)
db.executemany('INSERT INTO img VALUES (?,?,?,?)', [(k, *v) for k, v in imgs.items()])
# 4) 人物(Wikidata由来 6,472人)
db.execute('CREATE TABLE person (q TEXT PRIMARY KEY, en TEXT, ja TEXT, d TEXT, intro TEXT, w TEXT, t TEXT)')
db.execute('CREATE TABLE person_role (q TEXT, company TEXT, role TEXT)')
rows = json.load(open(os.path.join(S, 'web', 'people.json'), encoding='utf-8'))['rows']
for q, en, ja, cos, d, x, w, t in rows:
    db.execute('INSERT OR REPLACE INTO person VALUES (?,?,?,?,?,?,?)', (q.lstrip('Q'), en, ja, d, (x or '')[:400], w, t))
    for c, role in cos[:8]:
        db.execute('INSERT INTO person_role VALUES (?,?,?)', (q.lstrip('Q'), c, role))
db.execute('CREATE INDEX i_person_ja ON person(ja)')
db.execute('CREATE INDEX i_person_en ON person(en)')
db.execute('CREATE INDEX i_person_role ON person_role(q)')
# 5) 人物のSNS・名言・最近の発信
for t in ('person_social', 'person_quote', 'person_feed'):
    db.execute('DROP TABLE IF EXISTS ' + t)
db.execute('CREATE TABLE person_social (q TEXT PRIMARY KEY, x TEXT, ig TEXT, yt TEXT, web TEXT)')
db.execute('CREATE TABLE person_quote (q TEXT, w TEXT, t TEXT, text TEXT)')
db.execute('CREATE TABLE person_feed (q TEXT, ts TEXT, src TEXT, title TEXT, url TEXT, kind TEXT)')
sp = os.path.join(S, 'people_social.json')
if os.path.exists(sp):
    for q, v in json.load(open(sp, encoding='utf-8')).items():
        db.execute('INSERT OR REPLACE INTO person_social VALUES (?,?,?,?,?)', (q.lstrip('Q'), v.get('x', ''), v.get('ig', ''), v.get('yt', ''), v.get('web', '')))
qp = os.path.join(S, 'people_quotes.json')
if os.path.exists(qp):
    for q, v in json.load(open(qp, encoding='utf-8')).items():
        for text in v['q'][:6]:
            db.execute('INSERT INTO person_quote VALUES (?,?,?,?)', (q.lstrip('Q'), v['w'], v['t'], text))
name2q = {}
_norm = lambda n: re.sub(r'(?<![a-z])[a-z]\.\s*', '', (n or '').lower()).strip()
for q, en, ja, cos, d, x, w, t in rows:
    for nm in (en, ja):
        if nm:
            name2q.setdefault(nm.lower(), q.lstrip('Q')); name2q.setdefault(_norm(nm), q.lstrip('Q'))
# 注目の100人(top100_data.json)とその関係人物は web/people.json に無いことがあるので、名前と本人確認済みXのアカウント名でも結びつける
known = {q.lstrip('Q') for q, *_ in rows}
for _f in ('top100_data.json', 'top100_people_extra.json'):
    _p = os.path.join(S, _f)
    if os.path.exists(_p):
        _d = json.load(open(_p, encoding='utf-8'))
        for e in (_d if isinstance(_d, list) else _d.values()):
            if e.get('q'):
                known.add(e['q'].lstrip('Q'))
                for nm in (e.get('en'), e.get('ja')):
                    if nm:
                        name2q.setdefault(nm.lower(), e['q'].lstrip('Q')); name2q.setdefault(_norm(nm), e['q'].lstrip('Q'))
handle2q = {}
_sp = os.path.join(S, 'people_social.json')
if os.path.exists(_sp):
    for q, v in json.load(open(_sp, encoding='utf-8')).items():
        if v.get('x') and q.lstrip('Q') in known:
            handle2q[v['x'].lower()] = q.lstrip('Q')
_sv = os.path.join(S, 'sns_verified.json')
if os.path.exists(_sv):
    for q, v in json.load(open(_sv, encoding='utf-8')).items():
        if v.get('x'):
            handle2q[v['x'].lower()] = q.lstrip('Q')
wdb = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
nf = 0
if os.path.exists(wdb):
    w = sqlite3.connect(wdb)
    for ts, src, title, url, kind, who in w.execute("select ts,src,title,url,kind,company from events where kind in ('発信(X)','出演(YouTube)','発信(YouTube)') order by ts desc"):
        _m = re.match(r'X\(@(.+)\)', src or '')
        q = (_m and handle2q.get(_m.group(1).lower())) or name2q.get((who or '').lower()) or name2q.get(_norm(who))
        if q:
            db.execute('INSERT INTO person_feed VALUES (?,?,?,?,?,?)', (q, ts, src, title.split(': ', 1)[-1], url, kind))
            nf += 1
db.execute('CREATE INDEX i_pq ON person_quote(q)')
db.execute('CREATE INDEX i_pf ON person_feed(q, ts)')
print('SNS', db.execute('select count(*) from person_social').fetchone()[0], '人 / 名言', db.execute('select count(*) from person_quote').fetchone()[0], '件 / 発信', nf, '件')
db.commit()
n = sum(os.path.getsize(os.path.join(imgdir, f)) for f in os.listdir(imgdir))
print('画像', len(imgs), '枚', round(n / 1e6, 1), 'MB / 人物', len(rows), '人 / 人物の関わり', db.execute('select count(*) from person_role').fetchone()[0], '件')
