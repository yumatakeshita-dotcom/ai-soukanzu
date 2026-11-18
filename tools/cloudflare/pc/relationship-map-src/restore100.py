"""公開側(D1)の person / img / person_social に、注目の100人と関係する人物を戻す(手元のデータベースは使わず、JSONだけから作る)。
理由: build_site_assets.py → sync_people.py が、手元の person 表(Wikidataの6,472人)で D1 を丸ごと入れ替え、あとから足した人物が消えたため(2026-11-17)。
入力: top100_data.json / top100_people_extra.json / sns_verified.json  出力: restore100.sql を作り、--push で D1 に送る(INSERT OR REPLACE のみ。他の行は消さない)
使い方: python -u -X utf8 -I restore100.py [--push]"""
import json, os, subprocess, sys
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
top = json.load(open(os.path.join(S, 'top100_data.json'), encoding='utf-8'))
extra = json.load(open(os.path.join(S, 'top100_people_extra.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'top100_people_extra.json')) else {}
ver = json.load(open(os.path.join(S, 'sns_verified.json'), encoding='utf-8'))
q1 = lambda v: "'" + str('' if v is None else v).replace("'", "''") + "'"
L = []
n_p = n_i = n_s = 0


def person(q, en, ja, desc, intro, w, t):
    global n_p
    L.append('INSERT OR REPLACE INTO person VALUES (%s,%s,%s,%s,%s,%s,%s);' % tuple(q1(x) for x in (q.lstrip('Q'), en, ja, desc, (intro or '')[:600], w, t)))
    n_p += 1


def img(q, im):
    global n_i
    src = 'Wikimedia Commons(%s%s)' % (im['lic'], (' / ' + im['artist']) if im.get('artist') else '')
    L.append('INSERT OR REPLACE INTO img VALUES (%s,%s,%s,%s);' % tuple(q1(x) for x in ('q-' + q.lstrip('Q'), 'jpg', src, im.get('url', ''))))
    n_i += 1


for e in top:
    if not e.get('q'):
        continue
    person(e['q'], e.get('en'), e.get('ja'), e.get('desc'), e.get('intro'), e.get('w'), e.get('t'))
    if e.get('img'):
        img(e['q'], e['img'])
    sv = ver.get(e['q'])
    if sv:
        n = e['q'].lstrip('Q')
        L.append('DELETE FROM person_social WHERE q=%s;' % q1(n))
        L.append('INSERT INTO person_social VALUES (%s,%s,%s,%s,%s);' % tuple(q1(x) for x in (n, sv.get('x', ''), sv.get('ig', ''), sv.get('yt', ''), sv.get('web', ''))))
        n_s += 1
for q, e in extra.items():
    person(q, e.get('en'), e.get('ja'), e.get('desc'), e.get('intro'), e.get('w'), e.get('t'))
    if e.get('img'):
        img(q, e['img'])
sql = os.path.join(SITE, 'restore100.sql')
open(sql, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('人物', n_p, '/ 写真', n_i, '/ SNS', n_s, '/ 文', len(L), flush=True)
if '--push' in sys.argv:
    p = subprocess.run('npx wrangler d1 execute houjin --remote --yes --file="' + sql.replace(chr(92), '/') + '"', cwd=SITE, shell=True, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (p.stdout or '') + (p.stderr or '')
    if p.returncode != 0 or 'ERROR' in out:
        print('失敗', out[-400:])
        sys.exit(1)
    print('D1へ反映しました', flush=True)
