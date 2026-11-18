"""日本の全法人(houjin.sqlite の corp)を、サイトの静的ファイルに分けて書き出す。データベースの書き込み上限を使わずに、数百万社を載せるための作り。
  public/c/<番号>.json  … 法人番号から決まるファイル(6,000個)。会社ページ用。 [[法人番号,名称,種別,都道府県,市区町村,丁目番地,郵便番号,英語名,フリガナ,指定日,更新日], ...]
  public/n/<番号>.json  … 名前の先頭(核となる名前の頭2〜6文字)から決まるファイル(最大8,000個)。名前検索用。 [[法人番号,名称,都道府県], ...]
  public/n/hot.json     … 件数が多すぎて、頭の文字を長くして分けた先頭の一覧
  public/c/meta.json    … 総数
名前の核を取り出す規則(core)とハッシュ(FNV-1a)は、サイト側(src/app.mjs)と同じにすること。
使い方: python -I build_static_shards.py <houjin.sqlite> <siteのフォルダ>"""
import collections, json, os, re, sqlite3, sys, time, unicodedata
dbp, site = sys.argv[1], sys.argv[2]
ND, NB, LIMIT, MAXL = 6000, 8000, 4000, 6
STRIP = ['株式会社', '有限会社', '合同会社', '合資会社', '合名会社', '一般社団法人', '公益社団法人', '一般財団法人', '公益財団法人', '特定非営利活動法人', '医療法人社団', '医療法人財団', '医療法人', '社会福祉法人', '学校法人', '宗教法人', '協同組合', '(株)', '(有)', '(合)']


def core(name):
    s = unicodedata.normalize('NFKC', name or '').lower().replace(' ', '')
    ch = True
    while ch:
        ch = False
        for t in STRIP:
            if s.startswith(t) and len(s) > len(t):
                s = s[len(t):]
                ch = True
            if s.endswith(t) and len(s) > len(t):
                s = s[:-len(t)]
                ch = True
    return s


def fnv(key):
    h = 2166136261
    b = key.encode('utf-16-le')
    for i in range(0, len(b), 2):
        h = ((h ^ (b[i] | (b[i + 1] << 8))) * 16777619) & 0xFFFFFFFF
    return h


for d in ('c', 'n'):
    os.makedirs(os.path.join(site, 'public', d), exist_ok=True)
t0 = time.time()
db = sqlite3.connect(dbp)
# ① 会社ページ用(法人番号 % 6000)。作業用の表に番号を付けて、1つずつ書き出す
scratch = os.path.join(os.path.dirname(dbp), 'shard_scratch.sqlite')
if os.path.exists(scratch):
    os.replace(scratch, scratch + '.old')
sc = sqlite3.connect(scratch)
sc.execute('PRAGMA journal_mode=OFF')
sc.execute('PRAGMA synchronous=OFF')
sc.execute('CREATE TABLE s (b INTEGER, num TEXT, name TEXT, kind TEXT, pref TEXT, city TEXT, street TEXT, zip TEXT, en TEXT, kana TEXT, since TEXT, upd TEXT)')
cur = db.execute('SELECT num,name,kind,pref,city,street,zip,en,kana,since,upd FROM corp')
batch = []
total = 0
names = []      # (core, num, name, pref)
for r in cur:
    batch.append((int(r[0]) % ND,) + r)
    c = core(r[1])
    if len(c) >= 2:
        names.append((c, r[0], r[1], r[3]))
    total += 1
    if len(batch) >= 100000:
        sc.executemany('INSERT INTO s VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', batch)
        batch = []
if batch:
    sc.executemany('INSERT INTO s VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', batch)
sc.execute('CREATE INDEX i_b ON s(b)')
sc.commit()
print('読み込み', total, '社', round(time.time() - t0), '秒', flush=True)
nfile = 0
for b in range(ND):
    rows = sc.execute('SELECT num,name,kind,pref,city,street,zip,en,kana,since,upd FROM s WHERE b=?', (b,)).fetchall()
    if rows:
        with open(os.path.join(site, 'public', 'c', '%d.json' % b), 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
        nfile += 1
json.dump({'total': total, 'nd': ND, 'nb': NB, 'built': time.strftime('%Y-%m-%d')}, open(os.path.join(site, 'public', 'c', 'meta.json'), 'w'))
print('会社ページ用', nfile, 'ファイル', round(time.time() - t0), '秒', flush=True)
sc.close()
# ② 名前検索用: 頭の文字が多すぎる先頭は、文字数を伸ばして分ける
hot = {}
prefix_len = {}
cnt = collections.Counter(c[:2] for c, *_ in names)
hot[2] = {p for p, n in cnt.items() if n > LIMIT}
for L in range(3, MAXL + 1):
    cnt = collections.Counter(c[:L] for c, *_ in names if c[:L - 1] in hot[L - 1] and len(c) >= L)
    hot[L] = {p for p, n in cnt.items() if n > LIMIT}
shards = collections.defaultdict(list)
for c, num, name, pref in names:
    L = 2
    while L < MAXL and c[:L] in hot[L] and len(c) > L:
        L += 1
    shards[fnv(c[:L]) % NB].append([num, name, pref])
nidx = 0
big = 0
for i, rows in shards.items():
    with open(os.path.join(site, 'public', 'n', '%d.json' % i), 'w', encoding='utf-8') as f:
        json.dump(rows, f, ensure_ascii=False, separators=(',', ':'))
    nidx += 1
    big = max(big, len(rows))
json.dump({str(L): sorted(v) for L, v in hot.items() if v}, open(os.path.join(site, 'public', 'n', 'hot.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('名前検索用', nidx, 'ファイル(最大', big, '行) / 長く分けた先頭', {L: len(v) for L, v in hot.items()}, round(time.time() - t0), '秒', flush=True)
size = sum(os.path.getsize(os.path.join(site, 'public', d, f)) for d in ('c', 'n') for f in os.listdir(os.path.join(site, 'public', d)))
print('ファイル数', nfile + nidx + 2, '/ 合計', round(size / 1e6), 'MB')
