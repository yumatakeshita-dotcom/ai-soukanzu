"""yh/*.json (Chromeで読んだYouTube検索結果 [人物名,タイトル,/watch?v=..,チャンネル,'再生数 / N 日前'])を 出演(YouTube) として watch.sqlite に入れる。半年以内のみ"""
import datetime as dt, glob, hashlib, json, os, re, sqlite3
S = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(os.path.expanduser('~'), '.claude', 'data', 'watch.sqlite')
def ago(m):
    g = re.search(r'(\d+)\s*(秒|分|時間|日|週間|か月|年)前', m)
    if not g: return None
    n = int(g.group(1)); u = g.group(2)
    days = {'秒': 0, '分': 0, '時間': 0, '日': 1, '週間': 7, 'か月': 30, '年': 365}[u] * n
    return dt.date.today() - dt.timedelta(days=days)
db = sqlite3.connect(W); now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'); n = 0
for f in sorted(glob.glob(os.path.join(S, 'yh', '*.json'))):
    for who, title, href, ch, meta in json.load(open(f, encoding='utf8')):
        d = ago(meta)
        if not d or (dt.date.today() - d).days > 190: continue
        url = 'https://www.youtube.com' + href
        eid = hashlib.sha1((url + '|' + who).encode()).hexdigest()[:16]
        if db.execute('select 1 from events where id=? or (url=? and company=?)', (eid, url, who)).fetchone(): continue
        db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)', (eid, d.isoformat() + ' 12:00:00', 'YouTube(%s)' % ch[:30], '%s: %s' % (who, title[:110]), url, '出演(YouTube)', 20, '', '', who, now)); n += 1
db.commit(); print('YouTubeの出演を足しました', n, '件')
