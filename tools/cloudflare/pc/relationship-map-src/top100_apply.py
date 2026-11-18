"""注目の100人と、その関係する人物の情報を、手元のデータベース(houjin.sqlite)に反映し、Cloudflare D1 には「差分だけ」送る。
  person(紹介・名前)・img(写真・ライセンス)・person_rel(関係)・person_timeline(年表)・top100(確認状況)・person_social(100人は、本人確認済みのSNSだけ)
使い方: python -u top100_apply.py [--push]     (--push を付けると、D1にも送る。書き込みは数千行)"""
import json, os, re, sqlite3, subprocess, sys, datetime as dt
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
HDB = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite')
WDB = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
today = dt.date.today().isoformat()
top = json.load(open(os.path.join(S, 'top100_data.json'), encoding='utf-8'))
rel = json.load(open(os.path.join(S, 'top100_related.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'top100_related.json')) else {}
extra = json.load(open(os.path.join(S, 'top100_people_extra.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'top100_people_extra.json')) else {}
quotes = json.load(open(os.path.join(S, 'people_quotes.json'), encoding='utf-8'))
verified = json.load(open(os.path.join(S, 'sns_verified.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'sns_verified.json')) else {}
feed = {}
w = sqlite3.connect(WDB)
for who, n in w.execute("select company,count(*) from events where kind in ('発信(X)','出演(YouTube)','発信(YouTube)') group by company"):
    feed[(who or '').lower()] = n
db = sqlite3.connect(HDB)
for t in ('person_rel', 'person_timeline', 'top100'):
    db.execute('DROP TABLE IF EXISTS ' + t)
db.execute('CREATE TABLE person_rel (q TEXT, rq TEXT, rel TEXT)')
db.execute('CREATE TABLE person_timeline (q TEXT, y INTEGER, y2 INTEGER, kind TEXT, label TEXT, ref INTEGER)')
db.execute('CREATE TABLE top100 (q TEXT PRIMARY KEY, grp TEXT, checked_at TEXT, photo INTEGER, intro INTEGER, timeline INTEGER, sns INTEGER, feed INTEGER, quotes INTEGER)')
touched_person, touched_img = [], []


def put_person(q, en, ja, desc, intro, wl, t):
    n = q.lstrip('Q')
    db.execute('INSERT OR REPLACE INTO person VALUES (?,?,?,?,?,?,?)', (n, en or '', ja or '', desc or '', (intro or '')[:600], wl or '', t or ''))
    touched_person.append(n)


def put_img(q, im):
    n = q.lstrip('Q')
    src = 'Wikimedia Commons(%s%s)' % (im['lic'], (' / ' + im['artist']) if im.get('artist') else '')
    db.execute('INSERT OR REPLACE INTO img VALUES (?,?,?,?)', ('q-' + n, 'jpg', src, im.get('url', '')))
    touched_img.append('q-' + n)


for e in top:
    q = e['q']
    if not q:
        continue
    n = q.lstrip('Q')
    put_person(q, e['en'], e['ja'], e.get('desc', ''), e.get('intro', ''), e.get('w', ''), e.get('t', ''))
    if e.get('img'):
        put_img(q, e['img'])
    tl = [t for t in e.get('timeline', []) if t['kind'] != '生年' or t['y']]
    for t in tl:
        db.execute('INSERT INTO person_timeline VALUES (?,?,?,?,?,?)', (n, t['y'], t.get('y2'), t['kind'], t['label'], 1 if t['ref'] else 0))
    for r in rel.get(q, []):
        db.execute('INSERT INTO person_rel VALUES (?,?,?)', (n, r['r'].lstrip('Q'), r['rel']))
    sv = verified.get(q, {})
    db.execute('DELETE FROM person_social WHERE q=?', (n,))
    if sv:
        db.execute('INSERT INTO person_social VALUES (?,?,?,?,?)', (n, sv.get('x', ''), sv.get('ig', ''), sv.get('yt', ''), sv.get('web', '')))
    img_ok = bool(e.get('img'))
    db.execute('INSERT OR REPLACE INTO top100 VALUES (?,?,?,?,?,?,?,?,?)', (n, e['group'], today, int(img_ok), int(bool(e.get('intro'))), int(len(tl) >= 3), int(bool(sv.get('x') or sv.get('ig') or sv.get('yt'))),
                                                                            int(feed.get((e['en'] or '').lower(), 0) + feed.get((e['ja'] or '').lower(), 0) > 0), int(q in quotes)))
for q, e in extra.items():
    put_person(q, e.get('en'), e.get('ja'), e.get('desc'), e.get('intro'), e.get('w'), e.get('t'))
    if e.get('img'):
        put_img(q, e['img'])
db.commit()
print('反映: 注目の100人', len(top), '/ 関係する人物', len(extra), '/ 関係', db.execute('select count(*) from person_rel').fetchone()[0], '件 / 年表', db.execute('select count(*) from person_timeline').fetchone()[0], '項目', flush=True)
if '--push' not in sys.argv:
    sys.exit(0)
q1 = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
lines = ['DROP TABLE IF EXISTS person_rel;', 'CREATE TABLE person_rel (q TEXT, rq TEXT, rel TEXT);', 'CREATE INDEX i_prel ON person_rel(q);',
         'DROP TABLE IF EXISTS person_timeline;', 'CREATE TABLE person_timeline (q TEXT, y INTEGER, y2 INTEGER, kind TEXT, label TEXT, ref INTEGER);', 'CREATE INDEX i_ptl ON person_timeline(q);',
         'DROP TABLE IF EXISTS top100;', 'CREATE TABLE top100 (q TEXT PRIMARY KEY, grp TEXT, checked_at TEXT, photo INTEGER, intro INTEGER, timeline INTEGER, sns INTEGER, feed INTEGER, quotes INTEGER);']
for r in db.execute('select q,rq,rel from person_rel'):
    lines.append('INSERT INTO person_rel VALUES (%s,%s,%s);' % tuple(q1(x) for x in r))
for r in db.execute('select q,y,y2,kind,label,ref from person_timeline'):
    lines.append('INSERT INTO person_timeline VALUES (%s,%s,%s,%s,%s,%d);' % (q1(r[0]), r[1] if r[1] is not None else 'NULL', r[2] if r[2] is not None else 'NULL', q1(r[3]), q1(r[4]), r[5]))
for r in db.execute('select q,grp,checked_at,photo,intro,timeline,sns,feed,quotes from top100'):
    lines.append('INSERT INTO top100 VALUES (%s,%s,%s,%d,%d,%d,%d,%d,%d);' % (q1(r[0]), q1(r[1]), q1(r[2]), *r[3:]))
for n in sorted(set(touched_person)):
    r = db.execute('select q,en,ja,d,intro,w,t from person where q=?', (n,)).fetchone()
    lines.append('INSERT OR REPLACE INTO person VALUES (%s);' % ','.join(q1(x) for x in r))
for k in sorted(set(touched_img)):
    r = db.execute('select key,ext,src,url from img where key=?', (k,)).fetchone()
    lines.append('INSERT OR REPLACE INTO img VALUES (%s);' % ','.join(q1(x) for x in r))
for e in top:
    if e['q']:
        n = e['q'].lstrip('Q')
        lines.append('DELETE FROM person_social WHERE q=%s;' % q1(n))
        r = db.execute('select q,x,ig,yt,web from person_social where q=?', (n,)).fetchone()
        if r:
            lines.append('INSERT INTO person_social VALUES (%s);' % ','.join(q1(x) for x in r))
sql = os.path.join(SITE, 'top100.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('D1に送る文', len(lines), flush=True)
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗(上限に達した可能性があります)。', out[-500:])
    sys.exit(1)
print('D1への反映が完了しました', flush=True)
