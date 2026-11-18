"""ウォッチ(watch.sqlite)で集めた出来事を、独自サイト(Cloudflare D1)に送る。まだ送っていないものだけ、予算の範囲で。古いもの(21日より前)は消す。
上限(1日の書き込み)に達したら、その時点で止めて報告する。
使い方: python sync_events.py [送る件数の上限(既定 3000)]"""
import os, sqlite3, subprocess, sys
SITE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
db = sqlite3.connect(W)
db.execute('CREATE TABLE IF NOT EXISTS events_sent (id TEXT PRIMARY KEY)')
rows = db.execute("SELECT e.id,e.ts,e.src,e.title,e.url,e.kind,e.score,e.num,e.company FROM events e WHERE e.id NOT IN (SELECT id FROM events_sent) AND e.kind<>'その他' AND (e.kind NOT IN ('決算・業績','株主還元・報酬') OR e.score>=50) AND e.ts >= datetime('now','-14 days','localtime') ORDER BY e.score DESC, e.ts DESC LIMIT ?", (LIMIT,)).fetchall()
q = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
lines = ["CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, ts TEXT, src TEXT, title TEXT, url TEXT, kind TEXT, score INTEGER, num TEXT, company TEXT);",
         "CREATE INDEX IF NOT EXISTS i_ev_ts ON events(ts);", "CREATE INDEX IF NOT EXISTS i_ev_num ON events(num, ts);",
         "DELETE FROM events WHERE ts < datetime('now','-21 days','localtime');"]
for r in rows:
    lines.append('INSERT OR IGNORE INTO events VALUES (%s,%s,%s,%s,%s,%s,%d,%s,%s);' % (q(r[0]), q(r[1]), q(r[2]), q(r[3]), q(r[4]), q(r[5]), int(r[6]), q(r[7]), q(r[8])))
if not rows:
    print('送る出来事はありません')
    sys.exit(0)
sql = os.path.join(SITE, 'events.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('送る出来事', len(rows), '件', flush=True)
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗。記録しません(上限に達した可能性があります)。', out[-500:])
    sys.exit(1)
db.executemany('INSERT OR IGNORE INTO events_sent VALUES (?)', [(r[0],) for r in rows])
db.commit()
print('完了', len(rows), '件を送りました')
