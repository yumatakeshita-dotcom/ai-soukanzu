"""米SEC EDGARのForm D(私募の届出)から、ファンドの「募集総額」と「これまでの販売額」を取る。公的な一次資料。
使い方: python -u edgar_formd.py "Thrive Capital Partners X" "Founders Fund Growth IV" ...  → edgar_formd.json
Form Dの金額は、ファンドが申告した数字で、最終クローズの額と一致するとは限らない(募集中は目標額、不明は Indefinite)。"""
import json, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
UA = {'User-Agent': 'relationship-map-research (personal use)'}


def get(u):
    for i in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('utf-8', 'replace')
        except Exception as e:
            time.sleep(3 * (i + 1))
    return ''


out = []
for name in sys.argv[1:]:
    j = json.loads(get('https://efts.sec.gov/LATEST/search-index?q=%s&forms=D' % urllib.parse.quote('"%s"' % name)) or '{}')
    time.sleep(0.4)
    for h in (j.get('hits', {}).get('hits', []))[:12]:
        s = h['_source']
        adsh, fn = h['_id'].split(':')
        cik = (s.get('ciks') or [''])[0].lstrip('0')
        url = 'https://www.sec.gov/Archives/edgar/data/%s/%s/%s' % (cik, adsh.replace('-', ''), fn)
        x = get(url)
        time.sleep(0.4)
        off = re.search(r'<totalOfferingAmount>([^<]*)</totalOfferingAmount>', x)
        sold = re.search(r'<totalAmountSold>([^<]*)</totalAmountSold>', x)
        inv = re.search(r'<totalNumberAlreadyInvested>([^<]*)</totalNumberAlreadyInvested>', x)
        out.append({'query': name, 'entity': (s.get('display_names') or [''])[0], 'filed': s.get('file_date'), 'offering': off.group(1) if off else '', 'sold': sold.group(1) if sold else '', 'investors': inv.group(1) if inv else '', 'url': url})
json.dump(out, open('edgar_formd.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out:
    print(o['filed'], '|', o['entity'][:70], '| offering', o['offering'], '| sold', o['sold'], '| investors', o['investors'])
