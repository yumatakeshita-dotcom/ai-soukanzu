"""国税庁 法人番号の全件CSV(Shift_JIS)の zip から、現存する法人だけを SQLite に入れる。
使い方: python -I build_houjin_db.py <zipのパス> <出力するsqliteのパス>
列(0始まり): 1=法人番号 2=処理区分 6=名称 8=種別 9=都道府県 10=市区町村 11=丁目番地 15=郵便番号 18=閉鎖年月日 24=英語名 28=フリガナ 4=更新年月日 22=法人番号指定年月日
現存: 処理区分が 21(閉鎖)・81(抹消)・90(削除) でなく、閉鎖年月日が空のもの。"""
import csv, io, os, sqlite3, sys, zipfile
zp, dbp = sys.argv[1], sys.argv[2]
if os.path.exists(dbp):
    import time as _t
    os.replace(dbp, dbp + '.old-' + _t.strftime('%H%M%S'))
db = sqlite3.connect(dbp)
db.execute('PRAGMA journal_mode=OFF')
db.execute('PRAGMA synchronous=OFF')
db.execute('CREATE TABLE corp (num TEXT PRIMARY KEY, name TEXT, kind TEXT, pref TEXT, city TEXT, street TEXT, zip TEXT, en TEXT, kana TEXT, since TEXT, upd TEXT)')
z = zipfile.ZipFile(zp)
name = next(i.filename for i in z.infolist() if i.filename.endswith('.csv'))
t = io.TextIOWrapper(z.open(name), encoding='utf-8-sig', errors='replace', newline='')
rows, n, skip = [], 0, 0
BAD = {'21', '81', '90'}      # 閉鎖(21)・商号の登記の抹消(81)・削除(90)。71(吸収合併)は存続した側なので除外しない
for r in csv.reader(t):
    if len(r) < 29:
        continue
    n += 1
    if r[2] in BAD or r[18]:
        skip += 1
        continue
    rows.append((r[1], r[6], r[8], r[9], r[10], r[11], r[15], r[24], r[28], r[22], r[4]))
    if len(rows) >= 50000:
        db.executemany('INSERT OR REPLACE INTO corp VALUES (?,?,?,?,?,?,?,?,?,?,?)', rows)
        rows = []
    if n % 500000 == 0:
        print('読み込み', n, flush=True)
if rows:
    db.executemany('INSERT OR REPLACE INTO corp VALUES (?,?,?,?,?,?,?,?,?,?,?)', rows)
db.commit()
db.execute('CREATE INDEX i_kind ON corp(kind)')
db.execute('CREATE INDEX i_pref ON corp(pref, city)')
db.commit()
print('全件', n, '現存', n - skip, '閉鎖など', skip, flush=True)
for k, c in db.execute('SELECT kind, COUNT(*) FROM corp GROUP BY kind ORDER BY 2 DESC LIMIT 12'):
    print(k, c)
