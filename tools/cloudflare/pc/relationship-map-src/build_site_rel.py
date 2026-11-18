"""相関図のデータ(会社ごとの人物・ニュース)を、独自サイトのデータベース(houjin.sqlite)に、法人番号つきで入れる。
会社の対応づけは、日本語名の会社を EDINET の提出者(上場企業など)と名前で一致させたものだけ(取り違えを避けるため)。
使い方: python -I build_site_rel.py <sqliteのパス>"""
import json, os, re, sqlite3, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
from adds import apply_adds
dbp = sys.argv[1]
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)


def norm(s):
    s = re.sub(r'株式会社|\(株\)|（株）|㈱|Inc\.?|Corp\.?|Co\.,?\s*Ltd\.?|Ltd\.?|Holdings?', '', s or '')
    return re.sub(r'[\s　]', '', s).lower()


db = sqlite3.connect(dbp)
ed = {}
for name, num, listed in db.execute("select name, num, listed from edinet where num<>''"):
    ed.setdefault(norm(name), []).append((listed != '上場', num))      # 上場を優先
match = {}      # 相関図の会社名 -> 法人番号
for k, c in CO_ALL.items():
    n = next((x['name'] for x in c['N'] if x['id'] == c.get('center')), k)
    if re.search(r'[ぁ-ヶ一-龥]', n) and norm(n) in ed:
        match[n] = sorted(ed[norm(n)])[0][1]
for t in ('rel_news', 'rel_people'):
    db.execute('DROP TABLE IF EXISTS ' + t)
db.execute('CREATE TABLE rel_news (num TEXT, d TEXT, title TEXT, url TEXT, media TEXT)')
db.execute('CREATE TABLE rel_people (num TEXT, name TEXT, en TEXT, role TEXT, since TEXT, until TEXT, note TEXT)')
nn = np_ = 0
for fn in ('news_cos.json', 'yahoo_cos.json'):
    p = os.path.join(S, fn)
    if not os.path.exists(p):
        continue
    for name, rows in json.load(open(p, encoding='utf-8')).items():
        if name in match:
            seen = set()
            for d, t, u, m in rows:
                if u in seen:
                    continue
                seen.add(u)
                db.execute('INSERT INTO rel_news VALUES (?,?,?,?,?)', (match[name], d, t, u, m))
                nn += 1
for k, c in CO_ALL.items():
    n = next((x['name'] for x in c['N'] if x['id'] == c.get('center')), k)
    if n not in match:
        continue
    en = c.get('EN', {})
    for x in c['N']:
        if x.get('kind') != 'p':
            continue
        db.execute('INSERT INTO rel_people VALUES (?,?,?,?,?,?,?)', (match[n], x['name'], en.get(x['id'], ''), x.get('role', ''), str(x.get('from', '') or ''), str(x.get('to', '') or ''), (x.get('desc', '') or '')[:200]))
        np_ += 1
db.execute('CREATE INDEX i_rel_news ON rel_news(num, d)')
db.execute('CREATE INDEX i_rel_people ON rel_people(num)')
db.commit()
print('対応づけた会社', len(match), '/ ニュース', nn, '件 / 人物', np_, '件')
