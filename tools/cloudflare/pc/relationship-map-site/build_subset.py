"""独自サイトの最初の公開版に使う、小さなデータベースを作る(EDINET提出者に結び付いた法人 + 相関図の人物・ニュース)。D1に入れるSQLも出す。
使い方: python -I build_subset.py <houjin.sqlite> <出力フォルダ>"""
import os, sqlite3, sys
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
p = os.path.join(out, 'subset.sqlite')
if os.path.exists(p):
    os.remove(p)
db = sqlite3.connect(p)
db.execute('ATTACH DATABASE ? AS s', (src,))
db.execute('CREATE TABLE corp (num TEXT PRIMARY KEY, name TEXT, kind TEXT, pref TEXT, city TEXT, street TEXT, zip TEXT, en TEXT, kana TEXT, since TEXT, upd TEXT)')
db.execute("INSERT INTO corp SELECT c.* FROM s.corp c WHERE c.num IN (SELECT num FROM s.edinet WHERE num<>'')")
db.execute("CREATE TABLE edinet AS SELECT * FROM s.edinet WHERE num IN (SELECT num FROM corp)")
db.execute('CREATE TABLE rel_news AS SELECT * FROM s.rel_news')
db.execute('CREATE TABLE rel_people AS SELECT * FROM s.rel_people')
db.commit()
db.execute('DETACH DATABASE s')
db.execute('CREATE INDEX i_name ON corp(name)')
db.execute('CREATE INDEX i_pref ON corp(pref, city)')
db.execute('CREATE INDEX i_edinet_num ON edinet(num)')
db.execute('CREATE INDEX i_rel_news ON rel_news(num, d)')
db.execute('CREATE INDEX i_rel_people ON rel_people(num)')
db.commit()
for t in ('corp', 'edinet', 'rel_news', 'rel_people'):
    print(t, db.execute('select count(*) from ' + t).fetchone()[0])
with open(os.path.join(out, 'subset.sql'), 'w', encoding='utf-8') as f:
    for line in db.iterdump():
        f.write(line + '\n')
print('sql', os.path.getsize(os.path.join(out, 'subset.sql')) // 1000, 'KB')
