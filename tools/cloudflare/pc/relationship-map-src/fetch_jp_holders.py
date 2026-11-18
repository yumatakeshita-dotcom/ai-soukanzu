"""日本の主要企業の大株主(上位10)を IRBANK(EDINETの有価証券報告書・半期報告書の転記)から集める。Claude不要。
出力: jp_holders.json  {証券コード: {'period':'2026/03','rows':[[株主名,順位,持株比率%],...]}}
使い方: python fetch_jp_holders.py [コード ...]   (省略時は ranking_jp.txt の上位25社)"""
import json, os, re, sys, time, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
OUT = os.path.join(S, 'jp_holders.json')
res = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
codes = sys.argv[1:] or [ln.split('|')[2] for ln in open(os.path.join(S, 'ranking_jp.txt'), encoding='utf-8')][:25]
for code in codes:
    try:
        t = urllib.request.urlopen(urllib.request.Request('https://irbank.net/%s/holder' % code, headers=UA), timeout=40).read().decode('utf-8', 'replace')
    except Exception as e:
        print(code, '失敗', str(e)[:60], flush=True)
        continue
    m = re.search(r'<table class="bs">.*?</table>', t, re.S)
    if not m:
        print(code, '表なし', flush=True)
        continue
    tb = m.group(0)
    per = re.search(r'<th>大株主</th><th[^>]*>([\d/]+)</th>', tb)
    rows = []
    for tr in re.findall(r'<tr><td[^>]*><a [^>]*>([^<]+)</a></td><td[^>]*>(.*?)</td>', tb, re.S):
        name, cell = tr
        r = re.match(r'\s*(\d+)<span', cell)
        p = re.search(r'([\d.]+)%', cell)
        if r and p:
            rows.append([re.sub(r'\s+', ' ', name).strip(), int(r.group(1)), float(p.group(1))])
    rows.sort(key=lambda x: x[1])
    title = re.search(r'<title>([^<]*)', t)
    res[code] = {'period': per.group(1) if per else '', 'rows': rows[:10], 'title': title.group(1) if title else ''}
    print(code, res[code]['period'], len(rows), rows[:2], flush=True)
    json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    time.sleep(1.5)
