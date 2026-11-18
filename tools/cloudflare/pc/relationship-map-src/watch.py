"""ウォッチ(監視): 東証の適時開示(TDnet)・PR TIMES・Googleニュースから、会社の出来事(資金調達・買収・提携・役員の交代・不祥事・決算など)を拾い、
種類と重要度をつけて、相関図の会社(法人番号)に結び付けて watch.sqlite に貯める。同じ出来事は二重に入れない。
使い方: python -u watch.py once        … 1回だけ取る
        python -u watch.py loop [分]   … 指定した間隔(既定10分)で、ずっと取り続ける
出来事の表 events: id, ts(開示/掲載の日時), src, title, url, kind, score, code(証券コード), num(法人番号), company, added(取得した日時)"""
import datetime as dt, hashlib, html, os, re, sqlite3, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
UA = {'User-Agent': 'Mozilla/5.0 (compatible; relationship-map-research/1.0; personal use)'}
WDB = os.path.join(D, 'watch.sqlite')
HDB = os.path.join(D, 'houjin.sqlite')

# 種類の判定(上から順に最初に当たったもの)。(種類, 基本の重要度, 正規表現)
RULES = [
    ('不祥事・調査', 90, r'不正|不適切|調査委員会|第三者委員会|粉飾|改ざん|横領|逮捕|不倫|行政処分|課徴金|リコール|情報漏えい|情報漏洩|サイバー攻撃|不祥事|謝罪|scandal|probe|investigat|fraud|resign'),
    ('株主還元・報酬', 25, r'自己株式|株式報酬|株式インセンティブ|ストックオプション|配当|株主優待|株式分割|dividend|buyback'),
    ('買収・M&A', 85, r'公開買付|TOB|株式取得|子会社化|完全子会社|買収|合併|経営統合|事業譲渡|事業承継|吸収分割|株式交換|M&A|acquir|merger|takeover|buyout'),
    ('資金調達', 80, r'資金調達|第三者割当|シリーズ[A-Za-zＡ-Ｚ]|プレシリーズ|シードラウンド|新株予約権|増資|社債|調達を実施|raises|funding round|series [a-f]\b|seed round'),
    ('上場・IPO', 75, r'新規上場|上場承認|上場廃止|上場予定|IPO|ＩＰＯ|上場市場の変更|市場区分|files for ipo|listing'),
    ('人材移籍', 72, r'(OpenAI|Anthropic|Meta|DeepMind|Google|xAI|Nvidia|Microsoft|Amazon|Apple|Mistral|Tesla|SpaceX|Thinking Machines|SSI|Safe Superintelligence|Perplexity|Scale AI|ソフトバンク|サカナ|Sakana|PFN).{0,80}(joins?|joined|leaves?|left|leaving|depart|poach|hires?|hired|lures?|defect|移籍|引き抜|転職|参画|入社|退社|離脱)|(joins?|joined|leaves?|left|leaving|depart|poach|hires?|hired|lures?|defect|移籍|引き抜|転職|参画|入社|退社|離脱).{0,80}(OpenAI|Anthropic|Meta|DeepMind|xAI|Nvidia|Thinking Machines|Superintelligence)'),
    ('役員・人事', 70, r'代表取締役|社長|CEO|ＣＥＯ|会長|取締役の異動|役員人事|人事異動|就任|辞任|退任|解任|後任|appoint|steps down|names new'),
    ('提携', 60, r'業務提携|資本提携|資本業務提携|提携|協業|共同開発|共同出資|合弁|アライアンス|partnership|joint venture|collaborat'),
    ('決算・業績', 40, r'決算短信|業績予想|業績の修正|修正に関する|四半期報告|有価証券報告|決算|earnings|quarterly results'),
]
RX = [(k, s, re.compile(p, re.I)) for k, s, p in RULES]


def classify(title):
    for k, s, rx in RX:
        if rx.search(title or ''):
            return k, s
    return 'その他', 10


def get(url, timeout=40, tries=3):
    for i in range(tries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except Exception:
            time.sleep(2 * (i + 1))
    return None


def init():
    db = sqlite3.connect(WDB)
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, ts TEXT, src TEXT, title TEXT, url TEXT, kind TEXT, score INTEGER, code TEXT, num TEXT, company TEXT, added TEXT)')
    db.execute('CREATE INDEX IF NOT EXISTS i_ev_ts ON events(ts)')
    db.execute('CREATE INDEX IF NOT EXISTS i_ev_num ON events(num, ts)')
    db.commit()
    return db


def load_entities():
    """証券コード→法人番号、会社名の一覧(相関図・EDINET上場)を読み込む"""
    code2num, names = {}, {}
    try:
        h = sqlite3.connect('file:' + HDB.replace(chr(92), '/') + '?mode=ro', uri=True, timeout=20)
        for sec, num in h.execute("select sec, num from edinet where sec<>'' and num<>''"):
            code2num[sec] = num
        for name, num, people in h.execute('select name, num, people from mapco'):
            if len(name) >= 3:
                names[name] = (num, people)
        h.close()
    except Exception as e:
        print('(会社の一覧を読めませんでした)', str(e)[:60], flush=True)
    return code2num, names


def link_company(title, names):
    best = None
    for n, (num, people) in names.items():
        if n in title and (best is None or len(n) > len(best[0])):
            best = (n, num, people)
    return best


def fetch_tdnet(code2num, days=1):
    out = []
    today = dt.date.today()
    for k in range(days):
        d = today - dt.timedelta(days=k)
        ds = d.strftime('%Y%m%d')
        page = 1
        while page <= 40:
            b = get('https://www.release.tdnet.info/inbs/I_list_%03d_%s.html' % (page, ds))
            if not b:
                break
            t = b.decode('utf-8', 'replace')
            rows = re.findall(r'<tr>\s*<td[^>]*kjTime[^>]*>(.*?)</td>\s*<td[^>]*kjCode[^>]*>(.*?)</td>\s*<td[^>]*kjName[^>]*>(.*?)</td>\s*<td[^>]*kjTitle[^>]*>(.*?)</td>', t, flags=re.S)
            if not rows:
                break
            for tm, code, name, ti in rows:
                code = re.sub(r'<[^>]+>|\s|&nbsp;', '', code)
                name = html.unescape(re.sub(r'<[^>]+>', '', name)).strip()
                m = re.search(r'href="([^"]+\.pdf)"', ti)
                title = html.unescape(re.sub(r'<[^>]+>', '', ti)).strip()
                url = ('https://www.release.tdnet.info/inbs/' + m.group(1)) if m else 'https://www.release.tdnet.info/inbs/I_main_00.html'
                ts = '%s-%s-%s %s:00' % (ds[:4], ds[4:6], ds[6:], re.sub(r'<[^>]+>|\s', '', tm))
                out.append({'ts': ts, 'src': '適時開示(TDnet)', 'title': '%s %s' % (name, title), 'url': url, 'code': code, 'num': code2num.get(code, ''), 'company': name})
            if ('I_list_%03d_%s.html' % (page + 1, ds)) not in t:
                break
            page += 1
            time.sleep(0.6)
    return out


def fetch_rss(url, src, limit=200):
    b = get(url)
    out = []
    if not b:
        return out
    try:
        root = ET.fromstring(b)
    except ET.ParseError:
        return out
    for it in root.iter():
        if not it.tag.endswith('item'):
            continue
        g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
        title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
        if not title or not link:
            continue
        m = re.search(r'\s[-–|]\s([^-–|]{2,40})$', title) if src.startswith('Google') else None
        media = m.group(1).strip() if m else ''
        if m:
            title = title[:m.start()]
        raw = g('pubDate') or g('date')
        ts = ''
        for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%S%z'):
            try:
                ts = dt.datetime.strptime(raw.strip(), fmt).astimezone().strftime('%Y-%m-%d %H:%M:00')
                break
            except Exception:
                pass
        out.append({'ts': ts or dt.datetime.now().strftime('%Y-%m-%d %H:%M:00'), 'src': src + (('(' + media + ')') if media else ''), 'title': title, 'url': link, 'code': '', 'num': '', 'company': ''})
        if len(out) >= limit:
            break
    return out


def fetch_youtube():
    """youtube_channels.json にあるチャンネル(会社・人物)の新着動画を、YouTube公式のRSSで取る。(出演動画の検索は、別の仕組みが必要)"""
    path = os.path.join(S, 'youtube_channels.json')
    out = []
    if not os.path.exists(path):
        return out
    import json as _j
    chans = _j.load(open(path, encoding='utf-8'))
    stp = os.path.join(S, 'yt_state.json')
    off = _j.load(open(stp)).get('off', 0) if os.path.exists(stp) else 0
    batch = [chans[(off + i) % len(chans)] for i in range(min(20, len(chans)))]      # 1回あたり60チャンネルずつ、順番に(全部を約%d回で一巡)
    _j.dump({'off': (off + 20) % max(1, len(chans))}, open(stp, 'w'))
    for ch in batch:
        b = get('https://www.youtube.com/feeds/videos.xml?channel_id=' + ch['id'])
        if not b:
            continue
        t = b.decode('utf-8', 'replace')
        for e in re.findall(r'<entry>(.*?)</entry>', t, flags=re.S)[:8]:
            ti = html.unescape(re.search(r'<title>(.*?)</title>', e).group(1))
            pub = re.search(r'<published>(.*?)</published>', e).group(1)
            vid = re.search(r'<yt:videoId>(.*?)</yt:videoId>', e).group(1)
            out.append({'ts': pub[:10] + ' ' + pub[11:16] + ':00', 'src': 'YouTube', 'title': '%s: %s' % (ch['name'], ti), 'url': 'https://www.youtube.com/watch?v=' + vid, 'code': '', 'num': ch.get('num', ''), 'company': ch['name'], 'kind': '発信(YouTube)'})
        time.sleep(2.5)
    return out


GN = 'https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s'
QUERIES = [('資金調達 シリーズ OR 億円調達 when:1d', 'ja', 'JP', 'JP:ja'), ('買収 OR 子会社化 OR TOB OR 経営統合 when:1d', 'ja', 'JP', 'JP:ja'), ('社長交代 OR 代表取締役 異動 OR 辞任 when:1d', 'ja', 'JP', 'JP:ja'),
           ('不正 OR 不祥事 OR 調査委員会 OR 情報漏えい when:1d', 'ja', 'JP', 'JP:ja'), ('新規上場 OR IPO 承認 when:1d', 'ja', 'JP', 'JP:ja'),
           ('startup raises Series when:1d', 'en-US', 'US', 'US:en'), ('acquires OR acquisition OR merger announced when:1d', 'en-US', 'US', 'US:en'), ('CEO steps down OR appointed CEO when:1d', 'en-US', 'US', 'US:en'),
           ('IPO files OR prices when:1d', 'en-US', 'US', 'US:en'),
           ('(OpenAI OR Anthropic OR Meta OR DeepMind OR xAI OR Nvidia OR Microsoft) (joins OR leaves OR poached OR hires OR departs) researcher OR executive when:1d', 'en-US', 'US', 'US:en'),
           ('(OpenAI OR Anthropic OR Google OR Meta) 移籍 OR 引き抜き OR 退社 OR 転職 AI研究者 OR 幹部 when:1d', 'ja', 'JP', 'JP:ja')]


def collect(days=1):
    code2num, names = load_entities()
    evs = fetch_tdnet(code2num, days)
    evs += fetch_rss('https://prtimes.jp/index.rdf', 'PR TIMES')
    evs += fetch_youtube()
    for q, hl, gl, ce in QUERIES:
        evs += fetch_rss(GN % (urllib.parse.quote(q), hl, gl, ce), 'Googleニュース', 60)
        time.sleep(0.8)
    return evs, names


def store(evs, names):
    db = init()
    new = 0
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for e in evs:
        eid = hashlib.sha1((e['url'] + '|' + e['title']).encode('utf-8')).hexdigest()[:16]
        if db.execute('select 1 from events where id=?', (eid,)).fetchone():
            continue
        kind, score = classify(e['title'])
        if e.get('kind'):
            kind, score = e['kind'], 20
        if kind == '買収・M&A' and re.search(r'完全子会社間|連結子会社間|グループ内|簡易合併|簡易株式交換|当社の完全子会社を', e['title']):
            score = 35
        if kind == 'その他' and e['src'].startswith('適時開示'):
            continue      # 適時開示のうち、種類が判定できないものは貯めない(量が多いため)
        company, num = e['company'], e['num']
        lk = link_company(e['title'], names) if not num else None
        if lk:
            company, num = lk[0], lk[1]
            score += 10 if lk[2] else 0
        if e['code'] and num:
            score += 10      # 上場企業の適時開示
        db.execute('INSERT INTO events VALUES (?,?,?,?,?,?,?,?,?,?,?)', (eid, e['ts'], e['src'], e['title'][:200], e['url'], kind, min(score, 100), e['code'], num, company, now))
        new += 1
    db.commit()
    return new


def run_once(days=1):
    evs, names = collect(days)
    n = store(evs, names)
    db = init()
    tot = db.execute('select count(*) from events').fetchone()[0]
    print('%s 取得 %d件 / 新しい出来事 %d件 / 累計 %d件' % (dt.datetime.now().strftime('%m/%d %H:%M'), len(evs), n, tot), flush=True)
    return n


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'once'
    if mode == 'loop':
        mins = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        while True:
            try:
                run_once()
            except Exception as e:
                print('エラー(次の回に進みます):', str(e)[:100], flush=True)
            time.sleep(mins * 60)
    else:
        run_once(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
