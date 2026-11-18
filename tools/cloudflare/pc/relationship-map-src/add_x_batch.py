"""xh/*.json (Chromeで読んだ[アカウント,日付,抜粋,パス])を watch.sqlite に発信(X)として入れる。人物名は x_targets.json / people_social 由来のnameを使う"""
import datetime as dt, glob, hashlib, json, os, sqlite3
S = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
names = {x['h'].lower(): x['name'] for x in json.load(open(os.path.join(S, 'x_targets.json'), encoding='utf8'))}
try:
    _soc = json.load(open(os.path.join(S, 'people_social.json'), encoding='utf8'))
    _h = sqlite3.connect(os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite'))
    for q, v in _soc.items():
        if v.get('x') and v['x'].lower() not in names:
            r = _h.execute('select en,ja from person where q=?', (q.lstrip('Q'),)).fetchone()
            if r and (r[0] or r[1]): names[v['x'].lower()] = r[0] or r[1]
except Exception as e:
    print('人物名の補完に失敗', e)
db = sqlite3.connect(W); now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'); n = 0
for f in sorted(glob.glob(os.path.join(S, 'xh', '*.json'))):
    for h, d, tx, path in json.load(open(f, encoding='utf8')):
        if not tx.strip() or d < '2026-08-01': continue
        url = 'https://x.com' + path
        eid = hashlib.sha1((url + '|x').encode()).hexdigest()[:16]
        if db.execute('select 1 from events where id=?', (eid,)).fetchone(): continue
        who = names.get(h.lower(), h)
        db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)', (eid, d + ' 12:00:00', 'X(@%s)' % h, '%s: %s' % (who, tx[:110]), url, '発信(X)', 20, '', '', who, now)); n += 1
db.commit(); print('Xの投稿を足しました', n, '件')
