"""相関図のデータを、独自サイト(Cloudflare D1)に同期する。変わった会社だけを送るので、無料枠(1日10万行の書き込み)を使いすぎない。
やること: ① build_mapco.py で相関図から表(mapco*)を作り直す → ② 会社ごとの内容の指紋(ハッシュ)を、前回送った分と比べる → ③ 新しい・変わった会社だけ、予算の範囲で送る。
使い方: python sync_site.py [書き込みの予算(行数。既定 50000)]
次回の実行で、送りきれなかった分が続きから送られる。"""
import hashlib, json, os, sqlite3, subprocess, sys
SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite').replace('\\', '/')
MAPSRC = os.path.join(os.path.expanduser('~'), '.claude', 'docs', 'rooms', 'relationship-map-src')
BUDGET = int(sys.argv[1]) if len(sys.argv) > 1 else 50000
PY = sys.executable

DDL = """CREATE TABLE IF NOT EXISTS mapco (slug TEXT PRIMARY KEY, name TEXT, en TEXT, note TEXT, num TEXT, people INTEGER, acq INTEGER);
CREATE TABLE IF NOT EXISTS mapco_people (slug TEXT, name TEXT, en TEXT, role TEXT, since TEXT, until TEXT, note TEXT, q TEXT);
CREATE TABLE IF NOT EXISTS mapco_news (slug TEXT, d TEXT, title TEXT, url TEXT, media TEXT);
CREATE TABLE IF NOT EXISTS mapco_acq (slug TEXT, year TEXT, target TEXT, amount TEXT, note TEXT);
CREATE INDEX IF NOT EXISTS i_mapco_name ON mapco(name);
CREATE INDEX IF NOT EXISTS i_mapco_num ON mapco(num);
CREATE INDEX IF NOT EXISTS i_mapco_p ON mapco_people(slug);
CREATE INDEX IF NOT EXISTS i_mapco_n ON mapco_news(slug, d);
CREATE INDEX IF NOT EXISTS i_mapco_a ON mapco_acq(slug);
"""


def q(v):
    return "'" + str('' if v is None else v).replace("'", "''") + "'"


def wrangler(sqlfile):
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sqlfile.replace('\\', '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    return p.returncode == 0 and 'ERROR' not in out, out


# ① 相関図から表を作り直す
r = subprocess.run([PY, '-I', 'build_mapco.py', SRC], cwd=MAPSRC, capture_output=True, text=True, encoding='utf-8', errors='replace')
if r.returncode:
    print('表の作成に失敗', (r.stdout + r.stderr)[-400:])
    sys.exit(1)
print((r.stdout or '').strip().splitlines()[-1] if r.stdout else '', flush=True)

db = sqlite3.connect(SRC)
db.execute('CREATE TABLE IF NOT EXISTS mapco_sent (slug TEXT PRIMARY KEY, hash TEXT)')
sent = dict(db.execute('SELECT slug, hash FROM mapco_sent').fetchall())

# ② 会社ごとの指紋
cos = {}
for row in db.execute('SELECT slug,name,en,note,num,people,acq FROM mapco'):
    cos[row[0]] = {'co': row, 'people': [], 'news': [], 'acq': []}
for row in db.execute('SELECT slug,name,en,role,since,until,note,q FROM mapco_people'):
    cos[row[0]]['people'].append(row)
for row in db.execute('SELECT slug,d,title,url,media FROM mapco_news'):
    cos[row[0]]['news'].append(row)
for row in db.execute('SELECT slug,year,target,amount,note FROM mapco_acq'):
    cos[row[0]]['acq'].append(row)
for s, d in cos.items():
    # 人物の番号(q)が空の人は、指紋に入れない(列を足しても、全社が「変わった」扱いにならないように)
    _pp = [tuple(r[:7]) if not r[7] else tuple(r) for r in d['people']]
    d['hash'] = hashlib.sha1(json.dumps([d['co'], _pp, d['news'], d['acq']], ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
todo = [s for s, d in cos.items() if sent.get(s) != d['hash']]
_first = [x for x in os.environ.get('SYNC_FIRST', '').split(',') if x]   # 先に送る会社(例: SYNC_FIRST=vc_instagram)
todo.sort(key=lambda s: (s not in _first, 0))
gone = [s for s in sent if s not in cos]
print('変わった会社', len(todo), '/ なくなった会社', len(gone), '/ 全', len(cos), flush=True)
if not todo and not gone:
    print('送るものはありません')
    sys.exit(0)

# ③ 予算の範囲で送る(1社あたりの書き込み ≒ 本体4行 + 人物・ニュース・買収が各3行 + 消す分)
if not sent:
    ok, out = wrangler(os.path.join(SITE, 'ddl.sql')) if open(os.path.join(SITE, 'ddl.sql'), 'w', encoding='utf-8').write(DDL) else (True, '')
    if not ok:
        print('表の作成に失敗', out[-400:])
        sys.exit(1)
lines, used, batch = [], 0, []
for s in todo:
    d = cos[s]
    cost = 8 + 6 * (len(d['people']) + len(d['news']) + len(d['acq']))
    if used + cost > BUDGET and batch:
        break
    used += cost
    batch.append(s)
    for t in ('mapco', 'mapco_people', 'mapco_news', 'mapco_acq'):
        lines.append('DELETE FROM %s WHERE slug=%s;' % (t, q(s)))
    c = d['co']
    lines.append('INSERT INTO mapco VALUES (%s);' % ','.join([q(c[0]), q(c[1]), q(c[2]), q(c[3]), q(c[4]), str(int(c[5])), str(int(c[6]))]))
    for r in d['people']:
        lines.append('INSERT INTO mapco_people VALUES (%s);' % ','.join(q(x) for x in r))
    for r in d['news']:
        lines.append('INSERT INTO mapco_news VALUES (%s);' % ','.join(q(x) for x in r))
    for r in d['acq']:
        lines.append('INSERT INTO mapco_acq VALUES (%s);' % ','.join(q(x) for x in r))
for s in gone:
    for t in ('mapco', 'mapco_people', 'mapco_news', 'mapco_acq'):
        lines.append('DELETE FROM %s WHERE slug=%s;' % (t, q(s)))
sqlp = os.path.join(SITE, 'sync.sql')
open(sqlp, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('今回送る会社', len(batch), '(書き込みの見積もり', used, '行)', flush=True)
ok, out = wrangler(sqlp)
if not ok:
    print('失敗。記録しません。', out[-600:])
    sys.exit(1)
db.executemany('INSERT OR REPLACE INTO mapco_sent VALUES (?,?)', [(s, cos[s]['hash']) for s in batch])
for s in gone:
    db.execute('DELETE FROM mapco_sent WHERE slug=?', (s,))
db.commit()
rest = len(todo) - len(batch)
print('完了。送った会社', len(batch), '/ 残り', rest, '社(次回の実行で続きから)')
