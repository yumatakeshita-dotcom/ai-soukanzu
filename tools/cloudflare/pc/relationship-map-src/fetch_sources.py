"""上場申請(SEC EDGAR)と、資金調達・ユニコーンのニュース(見出しとリンクだけ)を集めて、履歴ファイルに積み上げる。Claude不要。
  sec_ipo.json     … S-1/F-1(上場申請)と424B4(公開価格が決まった最終目論見書)
  funding_news.json… TechCrunch / Crunchbase News / THE BRIDGE / PR TIMES の見出しから、資金調達とユニコーン候補
  unicorn_seen.json… ユニコーン一覧に初めて載った日(新規の印用)。unicorns.json に 'ns'(新規の日付)を足す
毎日の更新(refresh.py)から呼ばれる。見出し・リンク・日付・金額だけを保存し、記事本文は保存しない。"""
import datetime as dt, html, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
TODAY = dt.date.today()


def get(url, timeout=40):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
        except Exception as e:
            err = e
            time.sleep(3 * (i + 1))
    print('  取得失敗:', url[:70], str(err)[:60])
    return None


def load(name, default):
    f = os.path.join(S, name)
    if not os.path.exists(f):
        return default
    txt = open(f, encoding='utf-8').read()
    try:
        return json.loads(txt)
    except ValueError:
        # 書き込みが重なって壊れた場合は、読める記録だけ拾い直す(履歴をなるべく残す)
        if not isinstance(default, list):
            return default
        dec, out, i = json.JSONDecoder(), [], 0
        while True:
            i = txt.find('{"', i)
            if i < 0:
                break
            try:
                o, j = dec.raw_decode(txt, i)
                if isinstance(o, dict) and 'u' in o and 't' in o:
                    out.append(o)
                i = j
            except ValueError:
                i += 2
        print('  (壊れていた %s から %d件を復元)' % (name, len(out)))
        return out


def save(name, obj):
    tmp = os.path.join(S, name + '.tmp')       # いったん別ファイルに書いてから置き換える(途中で壊れないように)
    json.dump(obj, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    os.replace(tmp, os.path.join(S, name))


# ---------- SEC EDGAR ----------
def sec():
    hist = load('sec_ipo.json', [])
    seen = {h['a'] for h in hist}
    start = (TODAY - dt.timedelta(days=45)).isoformat()
    new = 0
    for forms, want in (('S-1,F-1', ('S-1', 'F-1')), ('424B4', ('424B4',))):
        for page in range(0, 4):
            q = urllib.parse.urlencode({'q': '""', 'forms': forms, 'dateRange': 'custom', 'startdt': start,
                                        'enddt': TODAY.isoformat(), 'from': page * 100})
            b = get('https://efts.sec.gov/LATEST/search-index?' + q)
            if not b:
                break
            try:
                hits = json.loads(b)['hits']['hits']
            except Exception:
                break
            for h in hits:
                s = h['_source']
                form = s.get('form') or (s.get('root_forms') or [''])[0]
                if form not in want:
                    continue
                acc, _, fn = h['_id'].partition(':')
                if acc in seen:
                    continue
                name = re.sub(r'\s*\(CIK.*$', '', (s.get('display_names') or [''])[0]).strip()
                tick = re.search(r'\(([A-Z]{1,5})\)', (s.get('display_names') or [''])[0])
                cik = str((s.get('ciks') or ['0'])[0]).lstrip('0')
                hist.append({'a': acc, 'f': form, 'd': s.get('file_date'), 'n': name, 't': tick.group(1) if tick else '',
                             'u': 'https://www.sec.gov/Archives/edgar/data/%s/%s/%s' % (cik, acc.replace('-', ''), fn)})
                seen.add(acc)
                new += 1
            if len(hits) < 100:
                break
            time.sleep(0.4)
    hist.sort(key=lambda h: h['d'], reverse=True)
    cut = (TODAY - dt.timedelta(days=400)).isoformat()
    hist = [h for h in hist if h['d'] >= cut][:3000]
    save('sec_ipo.json', hist)
    print(f'SEC: 新規{new}件 / 履歴{len(hist)}件')


# ---------- ニュース ----------
_GN = 'https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s'


def _gn(q, hl, gl, ceid):
    return _GN % (urllib.parse.quote(q), hl, gl, ceid)


# 小さな会社の資金調達まで拾うため、専門媒体のRSSと、Google Newsの検索(シード・シリーズA/B…)を加える。見出しと抜粋だけを使う
FEEDS = [('TechCrunch', 'https://techcrunch.com/category/startups/feed/', 'w'),
         ('Crunchbase News', 'https://news.crunchbase.com/feed/', 'w'),
         ('THE BRIDGE', 'https://thebridge.jp/feed', 'j'),
         ('PR TIMES', 'https://prtimes.jp/index.rdf', 'j'),
         ('EU-Startups', 'https://www.eu-startups.com/feed/', 'w'),
         ('Tech.eu', 'https://tech.eu/feed/', 'w'),
         ('Inc42', 'https://inc42.com/feed/', 'w'),
         ('Entrackr', 'https://entrackr.com/feed/', 'w'),
         ('e27', 'https://e27.co/feed/', 'w'),
         ('KrASIA', 'https://kr-asia.com/feed', 'w'),
         ('Tech Funding News', 'https://techfundingnews.com/feed/', 'w'),
         ('AlleyWatch', 'https://www.alleywatch.com/feed/', 'w'),
         ('FinSMEs', 'https://www.finsmes.com/feed', 'w'),
         ('Google News', _gn('startup raises seed round OR "pre-seed" when:7d', 'en-US', 'US', 'US:en'), 'w'),
         ('Google News', _gn('startup raises "Series A" when:7d', 'en-US', 'US', 'US:en'), 'w'),
         ('Google News', _gn('startup raises "Series B" OR "Series C" when:7d', 'en-US', 'US', 'US:en'), 'w'),
         ('Google News', _gn('startup funding round led by venture million when:7d', 'en-GB', 'GB', 'GB:en'), 'w'),
         ('Google News', _gn('startup raises funding India OR Singapore OR Indonesia when:7d', 'en-IN', 'IN', 'IN:en'), 'w'),
         ('Google News', _gn('スタートアップ 資金調達 シード OR プレシード when:7d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('スタートアップ 資金調達 シリーズA OR シリーズB OR シリーズC when:7d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('億円 資金調達 第三者割当増資 スタートアップ when:7d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('ベンチャー 調達 実施 万円 when:7d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Yahoo!ニュース', 'https://news.yahoo.co.jp/rss/topics/it.xml', 'j'),
         ('Yahoo!ニュース', 'https://news.yahoo.co.jp/rss/topics/business.xml', 'j'),
         ('Yahoo!ニュース', 'https://news.yahoo.co.jp/rss/categories/business.xml', 'j'),
         ('Google News', _gn('site:news.yahoo.co.jp 資金調達 シリーズ when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('site:news.yahoo.co.jp 億円 調達 スタートアップ when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('シリーズB 億円 調達 リード when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('シリーズC OR シリーズD 億円 調達 when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('ラウンド 資金調達 実施 億円 when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('自動運転 OR AI OR ロボット 資金調達 億円 when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('プレシリーズA OR シリーズA 数億円 調達 when:14d', 'ja', 'JP', 'JP:ja'), 'j'),
         ('Google News', _gn('startup 調達 newmo OR ニーリー OR ナレッジワーク when:30d', 'ja', 'JP', 'JP:ja'), 'j')]
ROUND_EN = re.compile(r'\b(pre-?seed|seed|series\s+[a-g]\+?|bridge round|growth round|angel round)\b', re.I)
ROUND_JP = re.compile(r'(プレシード|シード|シリーズ\s?[A-GＡ-Ｇ]|プレシリーズ[A-Z])')
FUND_EN = re.compile(r'^(?P<c>.{2,45}?)\s+(?:raises?|raised|secures?|lands?|closes?|nabs?|bags?|scores?|gets?|banks?|snags?|announces?|completes?|unveils?)\b(?P<rest>.*)$', re.I)
LEAD_EN = re.compile(r'\b(?:co-led by|led by|backed by|from|with participation from|investors? includ\w*)\s+(?P<v>[^.;|]+)', re.I)
FUND_JP = re.compile(r'^(?P<c>[^、。「」【】\s]{2,24}?)(?:が|は|、|,)')
INV_SUFFIX = re.compile(r'(Capital|Ventures?|Partners|Fund|Investments?|Equity|Holdings|Labs|Management|Group|Angels?|Syndicate)$')
JP_INV_PAT = re.compile(r'(?:リード(?:投資家|インベスター|VC)?(?:は|を|に|:|：)|引受先(?:は|として|:|：)|出資(?:者|先)?(?:は|:|：))\s*([^。\n]{2,60})')
KNOWN_VC = []
try:       # vc_names.txt の日本のVC・CVC名(日本語・英語)。見出しに出てきたら投資家として扱う
    for _ln in open(os.path.join(S, 'vc_names.txt'), encoding='utf-8'):
        _a = (_ln.rstrip('\n').split('|') + [''] * 7)[:7]
        if _a[1] == '日本':
            for _n in (_a[6], re.sub(r'\s*\(.*?\)', '', _a[3]), _a[4]):
                if _n and len(_n) >= 3 and _n not in KNOWN_VC and _n not in ('World Innovation Lab',):
                    KNOWN_VC.append(_n)
    KNOWN_VC += ['WiL', 'DCM', 'ANRI', 'UTEC', 'Coral Capital', 'ZVC', 'East Ventures', 'SBIインベストメント', 'ジャフコ', 'グロービス・キャピタル・パートナーズ']
    try:      # vc_extra.py の日本のVC(ブーストキャピタル・千葉道場ファンドなど)も、見出しに出てきたら投資家として扱う
        sys.path.insert(0, S)
        from vc_extra import EXTRA
        for _e in EXTRA:
            for _n in (_e[2], _e[1]):
                if _n and _n not in KNOWN_VC:
                    KNOWN_VC.append(_n)
    except ImportError:
        pass
except Exception:
    pass
BADCO = re.compile(r'^(how|why|what|when|where|the (?:best|top|most)|report|exclusive|breaking|these|this|here|we|our|your|new|top|\d+ )', re.I)


DESC_WORDS = r'startup|start-up|company|firm|unicorn|platform|maker|developer|provider|operator|marketplace|app|giant|fintech|healthtech|spacetech|edtech|cleantech|biotech|deeptech|proptech|insurtech|agritech|medtech|legaltech|foodtech|martech|regtech'
ALLOW_LC = {'of', 'and', 'the', 'for', 'de', 'la', 'du', 'von', 'van', 'del', 'di', 'da', '&', 'e', 'x'}


def clean_company(c):
    """『Indian spacetech startup Cosmoserve』→『Cosmoserve』のように説明語を外し、名前らしくないものは空にする"""
    c = c.strip(' ,:-–')
    m = re.match(r'^(?:[\w\-\'’.]+\s+){0,6}?(?:%s)s?\s+(?=\S)' % DESC_WORDS, c, re.I)
    if m:
        c = c[m.end():]
    c = re.sub(r'^(?:the\s+)?(?:\w+-based|\w+-born)\s+', '', c, flags=re.I)
    c = re.sub(r"^[A-Z][\w\-]*['’]s\s+", '', c)        # 「Oxford’s FluoRok」→「FluoRok」
    c = c.strip(' ,:-–')
    toks = c.split()
    if not c or len(toks) > 4 or len(c) > 40 or len(c) < 2:
        return ''
    if re.search(r'(?i)\b(founders?|ceo|says|talks|report|exclusive|startups?|company|firm|investors?|funds?|vcs?)\b', c):
        return ''
    for t in toks:
        if not (re.search(r'[A-Z0-9]', t) or t.lower() in ALLOW_LC or re.search(r'[^\x00-\x7f]', t)):
            return ''
    return c


def parse_funding(title, region, blob=''):
    """見出しから、会社名・ラウンド・投資家を見つける。見つからない項目は空。"""
    t = re.sub(r'^(?:exclusive|report|breaking|update|just in|scoop|funding|startup news)\s*[:|-]\s*', '', title.strip(), flags=re.I)
    cn, inv = '', []
    rd = ''
    if region == 'w' or t.isascii():
        m = FUND_EN.match(t)
        if m and not BADCO.match(m.group('c')) and re.match(r'^[A-Z0-9]', m.group('c')):
            cn = re.sub(r'\s*[,:]\s*$', '', m.group('c')).strip()
            rest = m.group('rest')
            mr = ROUND_EN.search(t)
            rd = mr.group(1).title().replace('Pre Seed', 'Pre-Seed') if mr else ''
            ml = LEAD_EN.search(rest)
            if ml:
                v = re.sub(r'\b(?:and|with)\s+(?:participation|others|existing)\b.*$', '', ml.group('v'))
                for p in re.split(r',\s*|\s+and\s+|\s*&\s*|\s+with\s+', v):
                    p = re.sub(r'\s*[-–|].*$', '', p).strip(' .')
                    if 3 <= len(p) <= 40 and re.match(r'^[A-Z0-9]', p) and not re.search(r'\d{3}|million|billion|funding|round|series|seed', p, re.I) and (INV_SUFFIX.search(p) or len(p.split()) <= 3):
                        inv.append(p)
    else:
        if re.search(r'資金調達|調達|出資|増資', t):
            # 「…を提供する○○がシードラウンドで…」「…の○○、シリーズAで…」のように、調達を表す語の直前の名前を取る
            mm = re.search(r'(?P<pre>.{2,70}?)(?:が|、|は)[^、。]{0,24}?(?:プレ)?(?:シード|シリーズ|資金調達|総額|累計|第三者|[\d０-９,\.]+(?:億|万)円)', t)
            if mm:
                pre = re.sub(r'^.*?(?:スタートアップ|ベンチャー)(?=[A-Za-z0-9ぁ-ヶ一-龥])', '', mm.group('pre'))
                nm = re.split(r'(?:を提供する|を開発する|を運営する|を展開する|を手がける|を動かす|を提供している|を展開している|を[^をがは、]{1,12}?(?:する|している|かす)|の|、|」|』)', pre)[-1]
                nm = re.sub(r'^(?:株式会社|\(株\))|(?:株式会社|\(株\))$', '', nm).strip(' ,。')
                _t = re.search(r'([A-Za-z0-9][A-Za-z0-9.&-]{1,24})$', nm)
                if _t and len(nm) > 10 and re.search(r'[ぁ-ヶ一-龥]', nm[:_t.start()]):
                    nm = _t.group(1)       # 「…をAIでつなぐBooost」→ Booost
                nm = re.sub(r',?\s*(?:Inc\.?|Corp\.?|Ltd\.?|LLC|Co\.,?\s*Ltd\.?)$', '', nm).strip(' ,')
                if 2 <= len(nm) <= 24 and not re.search(r'^[\d０-９]|資金|調達|スタートアップ|ベンチャー|日本|東京|東証|市場|上場|お知らせ', nm):
                    cn = nm
            if not cn:
                m = FUND_JP.match(re.sub(r'^[^、。]*」の', '', t) if '」の' in t.split('、')[0] else t)
                if m:
                    cn = m.group('c')
        if cn:
            mr = ROUND_JP.search(t)
            rd = mr.group(1) if mr else ''
            for kv in KNOWN_VC:        # 見出しにVC名が出ていれば、投資家として入れる(ANRI・グローバル・ブレインなど)
                if kv in t and kv not in inv:
                    inv.append(kv)
            mi = JP_INV_PAT.search(t + ' ' + blob)
            if mi:
                for p in re.split(r'[、,・/]|および|及び|と', mi.group(1)):
                    p = re.sub(r'(?:など|ほか|他).*$', '', p).strip(' 「」『』()（）')
                    if 2 <= len(p) <= 30 and re.search(r'キャピタル|ベンチャーズ?|ファンド|パートナーズ|Capital|Ventures|Partners|Fund|インベストメント', p):
                        inv.append(p)
    if cn and (region == 'w' or (cn.isascii() and t.isascii())):
        cn = clean_company(cn)
    return {'cn': cn[:40], 'rd': rd, 'inv': list(dict.fromkeys(inv))[:6]}
EN_KEY = re.compile(r'\b(raises?|raised|raising|funding|series [a-f]\b|valuation|valued|unicorn|ipo|files? for (?:an )?ipo)\b', re.I)
JP_KEY = re.compile(r'(資金調達|調達|ユニコーン|シリーズ[A-Za-z]|評価額|IPO|新規上場|上場承認)')
JP_NEED = re.compile(r'(資金調達|ユニコーン|シリーズ[A-Za-z]|評価額|IPO|新規上場|上場承認|調達を実施|調達を完了|調達しました)')
AMT_EN = re.compile(r'\$\s?([\d][\d,]*(?:\.\d+)?)\s?(billion|million|B|M)\b', re.I)
VAL_EN = re.compile(r'valu(?:ation|ed|es|ing)\s+(?:of |at |to |as much as |it at )?\$\s?([\d][\d,]*(?:\.\d+)?)\s?(billion|million|B|M)', re.I)
VAL_EN2 = re.compile(r'\$\s?([\d][\d,]*(?:\.\d+)?)\s?(billion|million|B|M)\s+(?:post-money |pre-money )?valuation', re.I)
AMT_JP = re.compile(r'([\d][\d,\.]*)\s?(億円|百万円|万円|億ドル|百万ドル)')


def parse_date(s):
    s = (s or '').strip()
    for fmt in ('%a, %d %b %Y %H:%M:%S %z', '%a, %d %b %Y %H:%M:%S %Z', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S.%f%z'):
        try:
            return dt.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    m = re.match(r'(\d{4}-\d{2}-\d{2})', s)
    return m.group(1) if m else TODAY.isoformat()


def usd_b(num, unit):
    v = float(num.replace(',', ''))
    return v if unit.lower() in ('billion', 'b') else v / 1000.0


def classify(title, region):
    """見出しから、金額の表記と『ユニコーン候補(評価額10億ドル以上 / 1,000億円以上 / ユニコーンの語)』を判定する"""
    amt, unicorn = '', False
    if region == 'w':
        m = AMT_EN.search(title)
        if m:
            u = m.group(2).lower()
            amt = '$%s %s' % (m.group(1), {'b': 'billion', 'm': 'million'}.get(u, u))
        v = VAL_EN.search(title) or VAL_EN2.search(title)
        if v and usd_b(v.group(1), v.group(2)) >= 1.0:
            unicorn = True
        if re.search(r'\bunicorn\b', title, re.I):
            unicorn = True
    else:
        m = AMT_JP.search(title)
        if m:
            amt = m.group(1) + m.group(2)
        if 'ユニコーン' in title:
            unicorn = True
        v = re.search(r'評価額[^\d]{0,12}([\d,]+)\s?億円', title)
        if v and float(v.group(1).replace(',', '')) >= 1000:
            unicorn = True
    return amt, unicorn


def news():
    hist = load('funding_news.json', [])
    for h in hist:   # 判定の仕様を直したら、過去の見出しも付け直す
        h['a'], h['c'] = classify(h['t'], h['r'])
        h.update(parse_funding(h['t'], h['r'], h.get('x', '')))
    seen = {h['u'] for h in hist}
    new = 0
    for src, url, region in FEEDS:
        b = get(url)
        if not b:
            continue
        try:
            root = ET.fromstring(b)
        except ET.ParseError:
            print('  解析失敗:', src)
            continue
        for it in root.iter():
            if not it.tag.endswith('item'):
                continue
            g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
            title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
            if not title or not link or link in seen:
                continue
            sname = src
            if src in ('Google News', 'Yahoo!ニュース'):        # 見出し末尾の『- 配信元』を外し、配信元の名前を出典にする
                m = re.search(r'\s[-–|]\s([^-–|]{2,40})$', title)
                if m:
                    sname, title = m.group(1).strip(), title[:m.start()]
            if region == 'w':
                if not EN_KEY.search(title):
                    continue
            else:
                if not JP_KEY.search(title) or not JP_NEED.search(title):
                    continue
                if src == 'PR TIMES' and not re.search(r'(資金調達|シリーズ|ユニコーン|評価額|上場)', title):
                    continue
            date = parse_date(g('pubDate') or g('date'))
            amt, unicorn = classify(title, region)
            ex = '' if src == 'Google News' else re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(g('description') or ''))).strip()[:200]
            row = {'u': link, 't': title[:160], 'd': date, 's': sname, 'r': region, 'a': amt, 'c': unicorn, 'x': ex}
            row.update(parse_funding(title, region, ex))
            hist.append(row)
            seen.add(link)
            new += 1
        time.sleep(1)
    hist.sort(key=lambda h: h['d'], reverse=True)
    cut = (TODAY - dt.timedelta(days=200)).isoformat()
    hist = [h for h in hist if h['d'] >= cut][:3000]
    save('funding_news.json', hist)
    print(f'ニュース: 新規{new}件 / 履歴{len(hist)}件 / ユニコーン候補{sum(1 for h in hist if h["c"])}件')


# ---------- 企業間の関係のニュース(提携・買収・出資など)。ページ内AIで関係を抽出するための素材 ----------
GN = 'https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s'
REL_FEEDS = [('Google News(日本)', GN % (urllib.parse.quote('提携 OR 買収 OR 出資 OR 協業 OR 共同開発 OR 子会社化 when:7d'), 'ja', 'JP', 'JP:ja'), 'j'),
             ('Google News(世界)', GN % (urllib.parse.quote('acquires OR acquisition OR partnership OR invests OR "joint venture" OR merger when:7d'), 'en-US', 'US', 'US:en'), 'w'),
             ('Google News(AI)', GN % (urllib.parse.quote('AI startup acquires OR partnership OR invests OR "strategic investment" when:7d'), 'en-US', 'US', 'US:en'), 'w'),
             ('PR TIMES', 'https://prtimes.jp/index.rdf', 'j'), ('THE BRIDGE', 'https://thebridge.jp/feed', 'j'),
             ('TechCrunch', 'https://techcrunch.com/feed/', 'w'), ('Crunchbase News', 'https://news.crunchbase.com/feed/', 'w')]
REL_JP = re.compile(r'(提携|買収|出資|協業|共同開発|共同研究|資本参加|子会社化|合併|経営統合|M&A|供給契約|供給を開始|連携|業務提携|資本提携)')
REL_EN = re.compile(r'\b(acquir\w*|acquisition|partner\w*|invest\w*|stake|merger|merges?|joint venture|collaborat\w*|supply deal|teams? up|buys?|bought|backs?)\b', re.I)


def relnews():
    """見出し・リンク・日付と、フィードが公開している冒頭の抜粋(240字まで)だけを保存する。本文は保存しない。"""
    hist = load('relation_news.json', [])
    seen = {h['u'] for h in hist}
    new = 0
    for src, url, region in REL_FEEDS:
        b = get(url)
        if not b:
            continue
        try:
            root = ET.fromstring(b)
        except ET.ParseError:
            print('  解析失敗:', src)
            continue
        n0 = new
        for it in root.iter():
            if not it.tag.endswith('item'):
                continue
            g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
            title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
            if not title or not link or link in seen:
                continue
            ex = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', html.unescape(g('description') or g('encoded') or ''))).strip()
            if src.startswith('Google News'):
                ex = ''     # Google Newsの抜粋は見出しの繰り返しなので保存しない
            blob = title + ' ' + ex
            if not (REL_JP.search(blob) if region == 'j' else REL_EN.search(blob)):
                continue
            hist.append({'u': link, 't': title[:160], 'd': parse_date(g('pubDate') or g('date')), 's': src.split('(')[0].strip(), 'r': region, 'x': ex[:240]})
            seen.add(link)
            new += 1
        print(f'  {src}: +{new - n0}')
        time.sleep(1)
    hist.sort(key=lambda h: h['d'], reverse=True)
    cut = (TODAY - dt.timedelta(days=30)).isoformat()
    hist = [h for h in hist if h['d'] >= cut][:700]
    save('relation_news.json', hist)
    print(f'関係ニュース: 新規{new}件 / 履歴{len(hist)}件')


# ---------- VCの投資ニュース(「○○がリード」の見出し)。vc_news.py が会社と投資家を取り出す素材 ----------
VC_FEEDS = [(GN % (urllib.parse.quote(q), hl, gl, ceid), r) for q, hl, gl, ceid, r in (
    ('raises "led by" Series A OR Series B OR seed when:3d', 'en-US', 'US', 'US:en', 'w'),
    ('"round led by" startup when:3d', 'en-US', 'US', 'US:en', 'w'),
    ('"led by" funding AI startup raises million when:3d', 'en-US', 'US', 'US:en', 'w'),
    ('資金調達 シリーズ リード 億円 when:3d', 'ja', 'JP', 'JP:ja', 'j'),
    ('スタートアップ 資金調達 ベンチャーキャピタル 引受先 when:3d', 'ja', 'JP', 'JP:ja', 'j'))]


def vcraw():
    hist = load('vc_news_raw.json', [])
    seen = {h['u'] for h in hist}
    new = 0
    for url, region in VC_FEEDS:
        b = get(url)
        if not b:
            continue
        try:
            root = ET.fromstring(b)
        except ET.ParseError:
            continue
        for it in root.iter():
            if not it.tag.endswith('item'):
                continue
            g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
            title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
            if not title or not link or link in seen:
                continue
            src = ''
            m = re.search(r'\s[-–|]\s([^-–|]{2,40})$', title)
            if m:
                src, title = m.group(1), title[:m.start()]
            hist.append({'u': link, 't': title[:200], 'd': parse_date(g('pubDate')), 's': src or 'Google News', 'r': region})
            seen.add(link)
            new += 1
        time.sleep(1)
    cut = (TODAY - dt.timedelta(days=90)).isoformat()
    hist = [h for h in hist if h['d'] >= cut][:2500]
    save('vc_news_raw.json', hist)
    print(f'VCニュースの素材: 新規{new}件 / 履歴{len(hist)}件')


# ---------- ユニコーン: 初めて載った日 ----------
def unicorn_seen():
    f = os.path.join(S, 'unicorns.json')
    if not os.path.exists(f):
        return
    uni = json.load(open(f, encoding='utf-8'))
    seen = load('unicorn_seen.json', None)
    first_run = seen is None
    seen = seen or {}
    added = []
    for u in uni:
        if u['n'] not in seen:
            seen[u['n']] = '' if first_run else TODAY.isoformat()   # 初回は『最初から載っていた』扱い(新規の印を付けない)
            if not first_run:
                added.append(u['n'])
        u['ns'] = seen[u['n']]
    save('unicorn_seen.json', seen)
    json.dump(uni, open(f, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('ユニコーン一覧: 新規に載った会社', added if added else 'なし')


if __name__ == '__main__':
    try:
        unicorn_seen()
    except Exception as e:
        print('ユニコーンの新規判定に失敗:', e)
    for fn in (sec, news, relnews, vcraw):
        try:
            fn()
        except Exception as e:
            print(fn.__name__, '失敗:', e)

