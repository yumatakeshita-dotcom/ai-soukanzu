"""日本のスタートアップの資金調達を、PR TIMESの発表から集め、出資者つきで jp_funding.json に出す。
  題名に「調達・出資・増資・引受」を含む発表だけを対象にし、本文・題名から出資者の名前を取り出す(出資者が取れない発表は載せない)。
  取れた名前は、発表のページが出典。見出し・金額・出資者の名前のみで、本文の転載はしない。
使い方: python -u fetch_jp_funding.py [ページ数(既定4)]   ※再実行すると、取得済みの発表は読み直さない(jp_funding_cache.json)"""
import html, json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 4
KW = ['資金調達を実施', '資金調達 シリーズA', '資金調達 シリーズB', '資金調達 シリーズC', '資金調達 シード', '資金調達 プレシリーズA', '第三者割当増資 引受先', 'リード投資家 調達', '出資を受け', 'から出資 スタートアップ', '億円 調達 VC', 'エクイティ調達', 'CVC 出資 スタートアップ', 'ベンチャーキャピタル 出資 実施']
CACHE = os.path.join(S, 'jp_funding_cache.json')
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}


def g(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('utf-8', 'replace')
        except Exception:
            time.sleep(2 * (i + 1))
    return ''


items = {}
for kw in KW:
    for pg in range(1, PAGES + 1):
        h = g('https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=%s&search_pattern=1&pagenum=%d' % (urllib.parse.quote(kw), pg))
        for m in re.finditer(r'href="(/main/html/rd/p/[0-9.]+\.html)"[^>]*>(.*?)</a>', h, flags=re.S):
            t = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
            d = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', t)
            t = re.sub(r'\d{4}年\d{1,2}月\d{1,2}日.*$', '', t).strip()
            if re.search(r'調達|出資|増資|引受', t) and not re.search(r'調査|アンケート|私募債|借入|ウェビナー|セミナー|キャンペーン|採用|登壇|開催|新株予約権|社債|ローン|融資|助成金|補助金', t) and m.group(1) not in items:
                items[m.group(1)] = (t, '%04d-%02d-%02d' % tuple(map(int, d.groups())) if d else '')
        time.sleep(0.7)
print('対象の発表', len(items), flush=True)
BAD = re.compile(r'^(?:既存|新規|個人|事業会社|金融機関|その他|他|各社|複数|主要|国内外|海外|国内|機関投資家|エンジェル|同社|当社|自社|ほか|など|等)|投資家$|株主$|[0-9]+回|ラウンド|調達|総額|累計|億円|万円|[（(]|[）)]|：|:')


ORG = re.compile(r'キャピタル|ベンチャー|ファンド|VC|CVC|Ventures?|Capital|Partners|Fund|Investment|Holdings|銀行|証券|信金|信用金庫|保険|ホールディングス|グループ|インベスト|パートナーズ|投資|機構|財団|商事|ソフトバンク|三菱|三井|住友|KDDI|NTT|JIC|DBJ|UTEC|Coral|ANRI|ミドリ|サイバーエージェント|株式会社|有限責任|Inc|Ltd|Corp', re.I)
BAD2 = re.compile(r'提供する|販売を行う|運用を行う|母体の|である|が運用|のうち|^キャピタル$|^インベストメンツ$|計[0-9]+|代表|取締役|CEO|CTO|CFO|社長|氏$|^[0-9０-９]+名|以下|既発表|既存|対し|ともに|とともに|運営する|リード|その他|一部|各社|ほか|同ファンド|および|[0-9]+社$')


def names(s):
    s = re.sub(r'[「」『』【】\[\]]', '', s)
    s = re.split(r'(?:を引受先|を割当先|が引受先|を引き受け|を引受け|による|からの|から|を含む|など|等)', s)[0] if re.search(r'を引受先|を割当先|が引受先|を引き受け|を引受け|による|からの|から|を含む|など|等', s) else s
    out = []
    for p in re.split(r'[、,，・／/&＆]|および|及び|ならびに|並びに', s):
        p = re.sub(r'\s+', ' ', p).strip(' 　')
        p = re.sub(r'^(?:リード投資家|リード|引受先|投資家|出資者|既存投資家|新規投資家)\s*', '', p)
        p = re.sub(r'^株式会社\s*|\s*株式会社$|\s*(?:\(|（).*$', '', p).strip()
        if 2 <= len(p) <= 30 and not BAD.search(p) and not BAD2.search(p) and ORG.search(p) and re.search(r'[A-Za-zぁ-んァ-ヶ一-龥]', p):
            out.append(p)
    return out


def parse(t, body):
    inv = []
    for line in body.split('\n'):
        line = line.strip()
        m = re.match(r'^(?:[■●◆・\-\s]*)?(?:リード投資家|リードインベスター|引受先|割当先|投資家|出資者|参加投資家|新規投資家|既存投資家|共同投資家|投資家一覧|調達先)\s*[：:]\s*(.+)$', line)
        if m and len(line) < 400:
            inv += names(m.group(1))
    for m in re.finditer(r'([^。\n、]{2,100}(?:[、・][^。\n、]{2,40}){0,8})(?:を引受先|を割当先|が引受先|を引き受け)', body[:20000]):
        inv += names(m.group(1))
    m = re.search(r'(?:、|が、?|は、?|，)([^、。]{2,60}?)(?:等|など)?から(?:の)?(?:総額|約)?[0-9０-９,.，億万円]+', t)
    if m:
        inv += names(m.group(1))
    m = re.search(r'〜\s*([^〜]+?)(?:…|$)', t)
    seen, out = set(), []
    for n in inv:
        if n not in seen:
            seen.add(n); out.append(n)
    return out[:10]


rows, tot = [], 0
for u, (t, d) in items.items():
    if u not in cache:
        p = g('https://prtimes.jp' + u)
        txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', p, flags=re.S)
        txt = re.sub(r'<br\s*/?>|</p>|</li>|</tr>|</div>|</h\d>|</td>', '\n', txt)
        txt = html.unescape(re.sub(r'<[^>]+>', '', txt))
        txt = re.sub(r'[ \t　]+', ' ', txt)
        cache[u] = txt[:30000]
        time.sleep(0.6)
        tot += 1
        if tot % 20 == 0:
            json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
            print('読み込み', tot, flush=True)
    inv = parse(t, cache[u])
    cn = re.match(r'^([^、,「」\s]{1,30}?)(?:、|が|は|，|\s-\s|―)', t)
    comp = cn.group(1) if cn else ''
    comp = re.sub(r'^.*?(?:を提供する|を開発する|を運営する|を展開する|の|で)(?=[A-Za-z0-9ぁ-んァ-ヶ一-龥]{2,}$)','',comp) if len(comp) > 12 else comp
    comp = re.sub(r'株式会社$','',comp)
    am = re.search(r'(?:総額|約)?([0-9,.，]+(?:億|万)?(?:[0-9,]+万)?円)', t)
    rd = re.search(r'(プレシリーズ[A-Z]|シリーズ[A-Z]|シード|プレA|エクイティ)', t)
    if comp and inv:
        for i in inv:
            if i != comp and comp not in i and i not in comp:
                rows.append({'src': i, 'dst': comp, 'label': rd.group(1) if rd else '', 'amount': am.group(1) if am else '', 'd': d, 'url': 'https://prtimes.jp' + u, 'media': 'PR TIMES', 'note': t[:160]})
json.dump(cache, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(rows, open(os.path.join(S, 'jp_funding.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('出資者つき', len({r['url'] for r in rows}), '件 / 線', len(rows), flush=True)
