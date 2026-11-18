#!/usr/bin/env python3
"""開示ウォッチ(2026/11/18追加)

米国の開示書類(SEC EDGAR)から、相関図に関係する会社の新しい提出書類を集めて
inbox/disclosures/YYYY-MM-DD.json に保存する。足すだけで、前の記録は消さない。
SpaceX の決算発表(8-K の添付 EX-99.1)からは、AI部門(SI部門)の売上などの数字も拾う。

使い方:
  SEC_UA="名前 連絡先メール" python3 scripts/sec_watch.py          # 新しいものだけ
  SEC_UA="..." python3 scripts/sec_watch.py --days 120              # さかのぼる日数(はじめの1回など)
SEC は「名前とメール」を入れた User-Agent を求める。値は環境変数 SEC_UA か
inbox/disclosures/ua.txt(1行)に書く(リポジトリには個人のメールを書かないこと)。
"""
import json, os, re, sys, time, datetime, urllib.request, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'inbox', 'disclosures')
SEEN = os.path.join(OUT, 'seen.txt')

# [CIK, 図のキー(なければ空), 表示名]
COMPANIES = [
    ('1181412', 'xai', 'SpaceX(xAI・X・Cursorを含む)'),
    ('1318605', '', 'Tesla'),
    ('1045810', 'nvidia', 'Nvidia'),
    ('789019', 'msft', 'Microsoft'),
    ('1341439', '', 'Oracle'),
    ('1769628', '', 'CoreWeave'),
    ('1652044', 'gdm', 'Alphabet(Google)'),
    ('1018724', '', 'Amazon'),
    ('1326801', 'meta', 'Meta'),
]
FORMS = {'8-K', '10-Q', '10-K', 'S-1', 'S-1/A', '424B4', '6-K', '20-F', 'SC 13D', 'SC 13D/A'}
ITEMS = {'1.01': '大事な契約', '2.01': '買収・売却の完了', '2.02': '決算', '5.02': '役員の交代',
         '7.01': '公表資料', '8.01': 'その他の出来事', '3.02': '株の発行', '5.03': '定款の変更'}


def ua():
    v = os.environ.get('SEC_UA', '').strip()
    p = os.path.join(OUT, 'ua.txt')
    if not v and os.path.exists(p):
        v = open(p, encoding='utf-8').read().strip()
    if not v or '@' not in v:
        sys.exit('SEC_UA(名前とメール)がありません。scripts/sec_watch.py の説明を見てください')
    return v


def get(url, U):
    req = urllib.request.Request(url, headers={'User-Agent': U, 'Accept-Encoding': 'identity'})
    for i in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode('utf-8', 'replace')
        except Exception as e:  # noqa
            if i == 2:
                raise
            time.sleep(2 + i * 3)


def text_of(h):
    h = re.sub(r'(?is)<(script|style).*?</\1>', ' ', h)
    h = re.sub(r'(?s)<[^>]+>', ' ', h)
    return re.sub(r'\s+', ' ', html.unescape(h))


def spacex_numbers(t):
    """SpaceX の決算発表から AI(SI)部門の数字を拾う。見つからなければ空"""
    pats = {
        '会社全体の売上': r'Delivered revenue of \$([\d.,]+ (?:billion|million))',
        'SI部門の売上': r'SI revenues were \$([\d.,]+ (?:billion|million))',
        'SI部門の営業利益': r'SI income from operations was \$([\d.,]+ (?:billion|million))',
        'SI部門の調整後EBITDA': r'SI Adjusted EBITDA was \$([\d.,]+ (?:billion|million))',
        '計算拠点の規模': r'nameplate compute to ([\d.]+ ?GW)',
    }
    out = {}
    for k, p in pats.items():
        m = re.search(p, t)
        if m:
            out[k] = m.group(1)
    return out


def main():
    days = 30
    if '--days' in sys.argv:
        days = int(sys.argv[sys.argv.index('--days') + 1])
    U = ua()
    os.makedirs(OUT, exist_ok=True)
    seen = set(open(SEEN, encoding='utf-8').read().split()) if os.path.exists(SEEN) else set()
    since = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    found = []
    for cik, key, name in COMPANIES:
        try:
            d = json.loads(get(f'https://data.sec.gov/submissions/CIK{int(cik):010d}.json', U))
        except Exception as e:
            print('読めませんでした', name, e)
            continue
        r = d['filings']['recent']
        for i in range(len(r['accessionNumber'])):
            acc, form, date = r['accessionNumber'][i], r['form'][i], r['filingDate'][i]
            if date < since or form not in FORMS or acc in seen:
                continue
            doc = r['primaryDocument'][i]
            base = f'https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace("-", "")}/'
            items = [x.strip() for x in (r.get('items', [''] * (i + 1))[i] or '').split(',') if x.strip()]
            rec = {'d': date, 'co': name, 'key': key, 'form': form, 'items': items,
                   'items_ja': [ITEMS.get(x, x) for x in items], 'url': base + doc, 'acc': acc,
                   'desc': r.get('primaryDocDescription', [''] * (i + 1))[i] or '', 'cf': '開示'}
            # SpaceX の決算(8-K 2.02)は添付の EX-99.1 から数字を拾う
            if cik == '1181412' and form == '8-K' and '2.02' in items:
                try:
                    idx = get(base, U)
                    ex = [h for h in re.findall(r'href="([^"]+\.htm)"', idx) if acc.replace('-', '') in h and doc not in h and not h.endswith('R1.htm')]
                    for h in ex[:3]:
                        t = text_of(get('https://www.sec.gov' + h if h.startswith('/') else h, U))
                        nums = spacex_numbers(t)
                        if nums:
                            rec['numbers'] = nums
                            rec['numbers_src'] = 'https://www.sec.gov' + h if h.startswith('/') else h
                            break
                except Exception as e:
                    rec['note'] = f'添付を読めませんでした: {e}'
            found.append(rec)
            time.sleep(0.2)
        time.sleep(0.3)
    found.sort(key=lambda x: x['d'], reverse=True)
    today = datetime.date.today().isoformat()
    if found:
        path = os.path.join(OUT, f'{today}.json')
        old = json.load(open(path, encoding='utf-8')) if os.path.exists(path) else []
        have = {x['acc'] for x in old}
        old += [x for x in found if x['acc'] not in have]
        json.dump(old, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        with open(SEEN, 'a', encoding='utf-8') as f:
            for x in found:
                f.write(x['acc'] + '\n')
    print(f'新しい提出書類: {len(found)}件')
    for x in found:
        line = f"{x['d']} {x['co']} {x['form']} {'・'.join(x['items_ja'])} {x['url']}"
        if x.get('numbers'):
            line += ' ' + json.dumps(x['numbers'], ensure_ascii=False)
        print(line)


if __name__ == '__main__':
    main()
