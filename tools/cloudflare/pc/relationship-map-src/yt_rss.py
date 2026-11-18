"""番組チャンネルのRSS(最新15本)から、人物がゲストで出た回を拾い、watch.sqlite の events に '出演(YouTube)' で入れる(無料・APIキー不要・RSSのみ)。
題名に人物の英語名(7文字以上)が完全一致し、かつ『Name: …』『Name on …』『… with Name』『A in conversation with B』『… | Name』の形(ゲスト回)だけ。特集・解説・ニュースの回は入れない。半年以内のみ。
使い方: python -X utf8 -I yt_rss.py [--dry]   (入れたあとは build_site_assets → sync_people → sync_events)"""
import datetime as dt, hashlib, html, json, os, re, sqlite3, sys, time, urllib.request
S = os.path.dirname(os.path.abspath(__file__)); H = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'en-US,en;q=0.9', 'Cookie': 'CONSENT=YES+1'}
CH = ['@20VC', '@allin', '@DwarkeshPatel', '@NoPriorsPodcast', '@sequoiacapital', '@a16z', '@AcquiredFM', '@LennysPodcast', '@lexfridman', '@latentspacepod', '@Stripe', '@CheekyPint', '@ycombinator', '@GoogleDeepMind', '@Anthropic-ai', '@OpenAI', '@NVIDIA', '@TheDiaryOfACEO']
names = {}
d = sqlite3.connect('file:' + os.path.expanduser('~/.claude/data/houjin.sqlite').replace(chr(92), '/') + '?mode=ro', uri=True, timeout=60)
for (en,) in d.execute("select en from person where en<>'' and length(en)>=7"): names[en.lower()] = en
for f in ('top100_data.json', 'top100_people_extra.json'):
    p = os.path.join(S, f)
    if os.path.exists(p):
        j = json.load(open(p, encoding='utf-8'))
        for e in (j if isinstance(j, list) else j.values()):
            if e.get('en') and len(e['en']) >= 7: names[e['en'].lower()] = e['en']
HOST = {'@Stripe': ['john collison'], '@CheekyPint': ['john collison'], '@DwarkeshPatel': ['dwarkesh patel'], '@lexfridman': ['lex fridman'], '@allin': ['jason calacanis', 'chamath palihapitiya', 'david friedberg'], '@20VC': ['harry stebbings']}  # 司会者はゲストではない
cut = (dt.date.today() - dt.timedelta(days=180)).isoformat()
def guest(t, k):
    k = re.escape(k)
    return bool(re.search(r'^' + k + r'\b\s*(:|-|–|—|\||on\b|says\b|explains\b|talks\b)', t, re.I) or re.search(r'\b(with|ft\.?|feat\.?|featuring)\s+' + k + r'\b', t, re.I) or re.search(r'[|:\-–—]\s*' + k + r'\s*$', t, re.I) or re.search(r'^.{3,60}\bin conversation with\s+' + k, t, re.I) or re.search(r'^' + k + r'.{0,10}(interview|conversation)', t, re.I))
W = sqlite3.connect(os.path.expanduser('~/.claude/data/watch.sqlite'), timeout=60); now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'); add = 0
for h in CH:
    try:
        pg = urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/' + h, headers=H), timeout=40).read().decode('utf-8', 'replace')
        m = re.search(r'"channelId":"(UC[\w-]{20,})"', pg) or re.search(r'channel_id=(UC[\w-]{20,})', pg)
        if not m: print(h, 'idなし'); continue
        feed = urllib.request.urlopen(urllib.request.Request('https://www.youtube.com/feeds/videos.xml?channel_id=' + m.group(1), headers=H), timeout=40).read().decode('utf-8', 'replace')
        ents = re.findall(r'<entry>.*?<yt:videoId>([^<]+)</yt:videoId>.*?<title>([^<]*)</title>.*?<published>([^<]*)</published>', feed, flags=re.S)
        n = 0
        for v, t, dd in ents:
            t = html.unescape(t)
            if dd[:10] < cut: continue
            for k, en in names.items():
                if k in HOST.get(h, []): continue
                if re.search(r'\b' + re.escape(k) + r'\b', t.lower()) and guest(t, en):
                    url = 'https://www.youtube.com/watch?v=' + v
                    eid = hashlib.sha1((url + '|' + en).encode()).hexdigest()[:16]
                    print(('[dry] ' if '--dry' in sys.argv else '') + h, dd[:10], en, '|', t[:70])
                    if '--dry' not in sys.argv and not W.execute('select 1 from events where id=? or (url=? and company=?)', (eid, url, en)).fetchone():
                        W.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)', (eid, dd[:10] + ' 12:00:00', 'YouTube(%s)' % h.lstrip('@')[:30], '%s: %s' % (en, t[:110]), url, '出演(YouTube)', 20, '', '', en, now)); add += 1; n += 1
        time.sleep(5)
    except Exception as e:
        print(h, 'エラー', str(e)[:60]); time.sleep(5)
W.commit(); print('追加', add, '件')
