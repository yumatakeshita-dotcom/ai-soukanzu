"""人物(person・person_role)と画像の一覧(img)を、独自サイト(Cloudflare D1)に入れ直す。中身が前回と同じなら何もしない。画像ファイルは wrangler deploy で一緒に載る。
使い方: python sync_people.py   (先に docs/rooms/relationship-map-src/build_site_assets.py で表と画像を作っておく)"""
import hashlib, os, sqlite3, subprocess, sys
SITE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite')
db = sqlite3.connect(SRC)
db.execute('CREATE TABLE IF NOT EXISTS people_sent (k TEXT PRIMARY KEY, hash TEXT)')
tables = {
    'img': ('CREATE TABLE img (key TEXT PRIMARY KEY, ext TEXT, src TEXT, url TEXT)', 'SELECT key,ext,src,url FROM img', ['CREATE INDEX IF NOT EXISTS i_img_key ON img(key)'] if False else []),
    'person': ('CREATE TABLE person (q TEXT PRIMARY KEY, en TEXT, ja TEXT, d TEXT, intro TEXT, w TEXT, t TEXT)', 'SELECT q,en,ja,d,intro,w,t FROM person', ['CREATE INDEX i_person_ja ON person(ja)', 'CREATE INDEX i_person_en ON person(en)']),
    'person_social': ('CREATE TABLE person_social (q TEXT PRIMARY KEY, x TEXT, ig TEXT, yt TEXT, web TEXT)', 'SELECT q,x,ig,yt,web FROM person_social', []),
    'person_quote': ('CREATE TABLE person_quote (q TEXT, w TEXT, t TEXT, text TEXT)', 'SELECT q,w,t,text FROM person_quote', ['CREATE INDEX i_pq ON person_quote(q)']),
    'person_feed': ('CREATE TABLE person_feed (q TEXT, ts TEXT, src TEXT, title TEXT, url TEXT, kind TEXT)', 'SELECT q,ts,src,title,url,kind FROM person_feed', ['CREATE INDEX i_pf ON person_feed(q, ts)']),
    'person_role': ('CREATE TABLE person_role (q TEXT, company TEXT, role TEXT)', 'SELECT q,company,role FROM person_role', ['CREATE INDEX i_person_role ON person_role(q)']),
}


def q(v):
    return "'" + str('' if v is None else v).replace("'", "''") + "'"


data = {}; hs = {}
for t, (ddl, sel, idx) in tables.items():
    rows = db.execute(sel).fetchall()
    data[t] = rows
    h = hashlib.sha1()
    for r in rows:
        h.update(repr(r).encode('utf-8'))
    hs[t] = h.hexdigest()
sent = dict(db.execute("SELECT k,hash FROM people_sent").fetchall())
# 表ごとに前回と比べ、変わった表だけ送る(書き込み行数の節約。旧方式の 'all' が残っていても全表は送らない)
changed = [t for t in tables if sent.get('t:' + t) != hs[t]]
# 安全装置: person・person_role・person_social・img を丸ごと入れ替えると、手元に無い追加人物(注目100人・GAFAM/VC・ゲスト等。D1にだけある)が消える。
# 追加人物を手元に戻したうえで、--all を付けたときだけ送る。付けないときは person_feed だけ送る。
if '--all' not in sys.argv:
    skipped = [t for t in changed if t != 'person_feed']
    if skipped:
        print('安全装置: 次の表は送りません(追加人物が消えるため。送るなら追加人物を手元に戻してから --all):', skipped)
    changed = [t for t in changed if t == 'person_feed']
if not changed:
    print('送るものはありません(人物・画像の一覧は前回と同じ)')
    sys.exit(0)
if 'all' in sent and not any(k.startswith('t:') for k in sent):
    changed = [t for t in changed if t == 'person_feed']
    for t in tables:
        if t not in changed:
            db.execute("INSERT OR REPLACE INTO people_sent VALUES (?,?)", ('t:' + t, hs[t]))
lines = []
for t in changed:
    ddl, sel, idx = tables[t]
    lines.append('DROP TABLE IF EXISTS %s;' % t)
    lines.append(ddl + ';')
    for r in data[t]:
        lines.append('INSERT INTO %s VALUES (%s);' % (t, ','.join(q(x) for x in r)))
    lines += [i + ';' for i in idx]
sql = os.path.join(SITE, 'people.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('送る表', changed, '行', sum(len(data[t]) for t in changed), flush=True)
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗。記録しません。', out[-600:])
    sys.exit(1)
for t in changed:
    db.execute("INSERT OR REPLACE INTO people_sent VALUES (?,?)", ('t:' + t, hs[t]))
db.commit()
print('完了')
