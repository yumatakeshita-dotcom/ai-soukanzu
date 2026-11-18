"""アジア・オセアニアの会社(環境変数 AP_SRCS の sqlite; 台湾・オーストラリア)を、サイトの静的ファイルに分けて書き出す。
  public/c/<番号>.json  … 国コード+登記番号のハッシュで決まるファイル。会社ページ用 [[国,番号,名称,種別,市,郵便番号,設立日,業種], ...]
  public/n/<番号>.json  … 名前の核(核の頭2〜6文字)から決まるファイル。名前検索用 [[国,番号,名称,市], ...]
  public/n/hot.json, public/c/meta.json
名前の核(core)・ハッシュ(FNV-1a)の規則は asiapac の app.mjs と同じにすること。
使い方: python -I build_asiapac_shards.py <出力するサイトのフォルダ>"""
import collections, json, math, os, re, sqlite3, sys, time, unicodedata
site = sys.argv[1]
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
ROWS_C, ROWS_N, LIMIT, MAXL = 3000, 1500, 6000, 6
LEG = {'ltd', 'limited', 'plc', 'llp', 'llc', 'inc', 'lp', 'cic', 'sas', 'sarl', 'sa', 'sasu', 'eurl', 'sci', 'snc', 'as', 'asa', 'ans', 'da', 'ba', 'oy', 'oyj', 'ab', 'gmbh', 'ag', 'kg', 'ug', 'bv', 'nv', 'ou', 'tu', 'uu', 'mu', 'fie', 'co', 'company', 'the', 'pty', 'nl'}


def core(name):
    s = unicodedata.normalize('NFKD', name or '')
    s = ''.join(c for c in s if not unicodedata.category(c).startswith('M')).lower()
    toks = re.sub(r'[^\w]+|_', ' ', s).split()
    while True:
        if len(toks) > 1 and toks[-1] in LEG:
            toks.pop()
        elif len(toks) > 1 and toks[0] in LEG:
            toks.pop(0)
        elif len(toks) > 3 and toks[0] in ('trustee', 'trustees') and toks[1] in ('for', 'of'):
            del toks[:2]
        else:
            break
    return ''.join(toks)


def fnv(key):
    h = 2166136261
    b = key.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | (b[i + 1] << 8))) * 16777619) & 0xFFFFFFFF
    return h


for d in ('c', 'n'):
    os.makedirs(os.path.join(site, 'public', d), exist_ok=True)
t0 = time.time()
srcs = os.environ['AP_SRCS'].split(';')
scratch = os.path.join(D, 'asiapac_scratch.sqlite')
if os.path.exists(scratch):
    os.replace(scratch, scratch + '.old-' + time.strftime('%H%M%S'))
sc = sqlite3.connect(scratch)
sc.execute('PRAGMA journal_mode=OFF')
sc.execute('PRAGMA synchronous=OFF')
sc.execute('CREATE TABLE a (cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT, core TEXT)')
total = 0
bycc = collections.Counter()
for p in srcs:
    if not os.path.exists(p):
        continue
    db = sqlite3.connect('file:' + p.replace(chr(92), '/') + '?mode=ro', uri=True)
    batch = []
    for r in db.execute('SELECT cc,id,name,kind,city,post,since,sic FROM wcorp'):
        c = core(r[2])
        if not r[2] or not r[1]:
            continue
        batch.append(r + (c,))
        bycc[r[0]] += 1
        total += 1
        if len(batch) >= 100000:
            sc.executemany('INSERT INTO a VALUES (?,?,?,?,?,?,?,?,?)', batch)
            batch = []
    if batch:
        sc.executemany('INSERT INTO a VALUES (?,?,?,?,?,?,?,?,?)', batch)
    sc.commit()
    db.close()
print('読み込み', total, '社', dict(bycc), round(time.time() - t0), '秒', flush=True)
ND = math.ceil(total / ROWS_C)
NB = math.ceil(total / ROWS_N)
# ① 会社ページ用: 国+番号のハッシュで ND 個に分ける
sc.execute('CREATE TABLE s (b INTEGER, cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT)')
batch = []
for r in sc.execute('SELECT cc,id,name,kind,city,post,since,sic FROM a'):
    batch.append((fnv(r[0] + ':' + r[1]) % ND,) + r)
    if len(batch) >= 100000:
        sc.executemany('INSERT INTO s VALUES (?,?,?,?,?,?,?,?,?)', batch)
        batch = []
if batch:
    sc.executemany('INSERT INTO s VALUES (?,?,?,?,?,?,?,?,?)', batch)
sc.execute('CREATE INDEX i_s ON s(b)')
sc.commit()
nfile = 0
for b in range(ND):
    rows = sc.execute('SELECT cc,id,name,kind,city,post,since,sic FROM s WHERE b=?', (b,)).fetchall()
    if rows:
        with open(os.path.join(site, 'public', 'c', '%d.json' % b), 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
        nfile += 1
json.dump({'total': total, 'by': dict(bycc), 'nd': ND, 'nb': NB, 'built': time.strftime('%Y-%m-%d')}, open(os.path.join(site, 'public', 'c', 'meta.json'), 'w'))
print('会社ページ用', nfile, 'ファイル(ND=%d)' % ND, round(time.time() - t0), '秒', flush=True)
# ② 名前検索用: 件数が多すぎる先頭は、文字数を伸ばして分ける(SQLiteで数える)
hot = {}
cur = sc.execute('SELECT substr(core,1,2) p, count(*) n FROM a WHERE length(core)>=2 GROUP BY p HAVING n>?', (LIMIT,))
hot[2] = {r[0] for r in cur}
for L in range(3, MAXL + 1):
    prev = hot[L - 1]
    if not prev:
        hot[L] = set()
        continue
    ph = ','.join('?' * len(prev))
    cur = sc.execute('SELECT substr(core,1,%d) p, count(*) n FROM a WHERE length(core)>=%d AND substr(core,1,%d) IN (%s) GROUP BY p HAVING n>?' % (L, L, L - 1, ph), tuple(prev) + (LIMIT,))
    hot[L] = {r[0] for r in cur}
print('長く分ける先頭', {L: len(v) for L, v in hot.items()}, round(time.time() - t0), '秒', flush=True)
sc.execute('CREATE TABLE x (b INTEGER, cc TEXT, id TEXT, name TEXT, city TEXT)')
batch = []
for cc, id_, name, city, c in sc.execute('SELECT cc,id,name,city,core FROM a WHERE length(core)>=2'):
    L = 2
    while L < MAXL and c[:L] in hot[L] and len(c) > L:
        L += 1
    batch.append((fnv(c[:L]) % NB, cc, id_, name, city))
    if len(batch) >= 100000:
        sc.executemany('INSERT INTO x VALUES (?,?,?,?,?)', batch)
        batch = []
if batch:
    sc.executemany('INSERT INTO x VALUES (?,?,?,?,?)', batch)
sc.execute('CREATE INDEX i_x ON x(b)')
sc.commit()
nidx = 0
big = 0
for b in range(NB):
    rows = sc.execute('SELECT cc,id,name,city FROM x WHERE b=?', (b,)).fetchall()
    if rows:
        with open(os.path.join(site, 'public', 'n', '%d.json' % b), 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
        nidx += 1
        big = max(big, len(rows))
json.dump({str(L): sorted(v) for L, v in hot.items() if v}, open(os.path.join(site, 'public', 'n', 'hot.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
size = sum(os.path.getsize(os.path.join(site, 'public', d, f)) for d in ('c', 'n') for f in os.listdir(os.path.join(site, 'public', d)))
print('名前検索用', nidx, 'ファイル(NB=%d, 最大 %d 行)' % (NB, big), '/ ファイル数', nfile + nidx + 2, '/ 合計', round(size / 1e6), 'MB', round(time.time() - t0), '秒', flush=True)
