"""台湾の会社(経済部 商工行政資料開放平台「公司登記關鍵字查詢」API)を world_tw_names.sqlite に取り込む。
会社名に含まれる漢字1文字ごとに「Company_Name like 字 and Company_Status eq 01(核准設立)」を全ページ取得し、統一編号で重複を除く。
取れた会社名から新しい文字を見つけて続ける。1文字で50万件を超えるもの(公・司・有・限…)は上限(skip最大50万)で取り切れないので capped として記録。
出典: 経済部商業発展署(政府資料開放授權條款 第1版)。再実行すると done 表の続きから。
使い方: python -I -X utf8 crawl_tw.py"""
import json, os, sqlite3, time, urllib.parse, urllib.request
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
URL = 'https://data.gcis.nat.gov.tw/od/data/api/6BBA2268-1367-4B42-9CCA-BC17499EBE8C?'
DELAY = float(os.environ.get('TW_DELAY', '0.3'))


def get(ch, skip):
    u = URL + urllib.parse.urlencode({'$format': 'json', '$top': 1000, '$skip': skip, '$filter': 'Company_Name like %s and Company_Status eq 01' % ch})
    for t in range(8):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'kigyo-research-crawler'}), timeout=120).read().decode('utf-8')
            if r.startswith('['):
                return json.loads(r)
            if not r.strip():
                return []
        except Exception:
            pass
        time.sleep(5 * (t + 1))
    raise RuntimeError('失敗 ' + ch)


def roc(d):
    d = (d or '').strip()
    return '%04d-%s-%s' % (int(d[:-4]) + 1911, d[-4:-2], d[-2:]) if len(d) >= 6 and d.isdigit() else ''


db = sqlite3.connect(os.path.join(D, 'world_tw_names.sqlite'))
db.execute('PRAGMA journal_mode=WAL')
db.execute('CREATE TABLE IF NOT EXISTS wcorp (cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT, PRIMARY KEY (cc, id))')
db.execute('CREATE TABLE IF NOT EXISTS done (ch TEXT PRIMARY KEY, rows INTEGER, capped INTEGER)')
done = {r[0] for r in db.execute('SELECT ch FROM done')}
seen = set(done)
queue = []


def cjk(c):
    return '一' <= c <= '鿿'


def enqueue(name):
    for c in name:
        if cjk(c) and c not in seen:
            seen.add(c)
            queue.append(c)


# 既存の会社名から文字を拾う(再開時)
for (nm,) in db.execute('SELECT name FROM wcorp'):
    enqueue(nm)
if not queue and not done:
    for c in '台臺中華大新東西南北山海':
        seen.add(c)
        queue.append(c)
queue = [c for c in queue if c not in done]
t0 = time.time()
k = 0
while queue:
    ch = queue.pop(0)
    sk, n, capped = 0, 0, 0
    while True:
        rows = get(ch, sk)
        out = []
        for r in rows:
            i = r.get('Business_Accounting_NO')
            if not i:
                continue
            nm = r.get('Company_Name', '')
            enqueue(nm)
            loc = r.get('Company_Location') or ''
            out.append(('TW', i, nm, '', loc[:8], '', roc(r.get('Company_Setup_Date')), ''))
        db.executemany('INSERT OR IGNORE INTO wcorp VALUES (?,?,?,?,?,?,?,?)', out)
        n += len(rows)
        if len(rows) < 1000:
            break
        sk += 1000
        if sk > 500000:
            capped = 1
            break
        time.sleep(DELAY)
    db.execute('INSERT OR REPLACE INTO done VALUES (?,?,?)', (ch, n, capped))
    db.commit()
    k += 1
    if k % 10 == 0 or capped:
        c = db.execute('SELECT count(*) FROM wcorp').fetchone()[0]
        print(k, ch, '行', n, '待ち', len(queue), '会社(重複除く)', c, round(time.time() - t0), '秒', 'CAPPED' if capped else '', flush=True)
    time.sleep(DELAY)
print('完了', db.execute('SELECT count(*) FROM wcorp').fetchone()[0], flush=True)
