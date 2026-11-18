"""独自サイト(Cloudflare D1)に、法人データを毎日少しずつ足す。無料枠(1日10万行の書き込み)に収まるよう、1回に BATCH 社まで。
順番: 熊本県 → 九州・沖縄 → 東京・大阪・愛知・福岡など大都市 → その他。どの会社を入れたかは、手元のデータベース(houjin.sqlite)の pushed 表に記録する。
使い方: python push_daily.py [社数]        (wrangler にログイン済みであること)"""
import os, sqlite3, subprocess, sys, time
SRC = 'C:/Users/yumat/.claude/data/houjin.sqlite'
SITE = os.path.dirname(os.path.abspath(__file__))
BATCH = int(sys.argv[1]) if len(sys.argv) > 1 else 20000      # 1社あたり約4行の書き込み(本体+主キー+索引2つ)。2万社で約8万行
ORDER = ['熊本県', '福岡県', '佐賀県', '長崎県', '大分県', '宮崎県', '鹿児島県', '沖縄県', '東京都', '大阪府', '愛知県', '神奈川県', '京都府', '兵庫県']
db = sqlite3.connect(SRC)
db.execute('CREATE TABLE IF NOT EXISTS pushed (num TEXT PRIMARY KEY)')
db.commit()
prefs = [r[0] for r in db.execute('select distinct pref from corp')]
order = ORDER + sorted(p for p in prefs if p not in ORDER)
rows = []
for pref in order:
    need = BATCH - len(rows)
    if need <= 0:
        break
    rows += db.execute('SELECT c.num,c.name,c.kind,c.pref,c.city,c.street,c.zip,c.en,c.kana,c.since,c.upd FROM corp c WHERE c.pref=? AND c.num NOT IN (SELECT num FROM pushed) ORDER BY c.num LIMIT ?', (pref, need)).fetchall()
if not rows:
    print('入れるものがありません(全件、入れ終わりました)')
    sys.exit(0)


def q(v):
    return "'" + str(v if v is not None else '').replace("'", "''") + "'"


sql = os.path.join(SITE, 'daily.sql')
with open(sql, 'w', encoding='utf-8') as f:
    for r in rows:
        f.write('INSERT OR IGNORE INTO corp VALUES (' + ','.join(q(x) for x in r) + ');\n')
print('今回入れる', len(rows), '社 (先頭:', rows[0][3], ')', flush=True)
t = time.time()
p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace('\\', '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
out = (p.stdout or '') + (p.stderr or '')
if p.returncode != 0 or 'ERROR' in out:
    print('失敗。記録しません。', out[-600:])
    sys.exit(1)
db.executemany('INSERT OR IGNORE INTO pushed VALUES (?)', [(r[0],) for r in rows])
db.commit()
print('完了', len(rows), '社', round(time.time() - t), '秒。累計', db.execute('select count(*) from pushed').fetchone()[0], '社(上場などの最初の分は別)')
