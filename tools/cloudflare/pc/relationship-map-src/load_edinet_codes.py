"""EDINETコードリスト(金融庁が公開しているCSV)を、法人番号のデータベースに edinet テーブルとして足す。使い方: python -I load_edinet_codes.py <zip> <sqlite>"""
import csv, io, sqlite3, sys, zipfile
zp, dbp = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(zp)
t = io.TextIOWrapper(z.open(z.infolist()[0].filename), encoding='cp932', errors='replace', newline='')
rd = csv.reader(t)
next(rd)
hdr = next(rd)
db = sqlite3.connect(dbp)
db.execute('DROP TABLE IF EXISTS edinet')
db.execute('CREATE TABLE edinet (code TEXT PRIMARY KEY, kind TEXT, listed TEXT, name TEXT, en TEXT, addr TEXT, industry TEXT, sec TEXT, num TEXT)')
n = 0
for r in rd:
    if len(r) < 13:
        continue
    db.execute('INSERT OR REPLACE INTO edinet VALUES (?,?,?,?,?,?,?,?,?)', (r[0], r[1], r[2], r[6], r[7], r[9], r[10], r[11], r[12]))
    n += 1
db.execute('CREATE INDEX IF NOT EXISTS i_edinet_num ON edinet(num)')
db.commit()
print('EDINET提出者', n)
print('うち上場', db.execute("select count(*) from edinet where listed='上場'").fetchone()[0])
print('法人番号あり', db.execute("select count(*) from edinet where num<>''").fetchone()[0])
print('法人番号が法人DBにある', db.execute('select count(*) from edinet e join corp c on c.num=e.num').fetchone()[0])
for k, c in db.execute('select kind,count(*) from edinet group by kind order by 2 desc limit 6'):
    print(k, c)
