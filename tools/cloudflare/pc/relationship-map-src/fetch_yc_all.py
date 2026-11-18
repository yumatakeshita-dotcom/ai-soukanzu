"""Y Combinator の出身スタートアップ全社(約6,400社)の一覧を、公開データ(yc-oss の API、YC公式ディレクトリの写し)から取る。Claude不要。
出力: yc_startups.json  [[会社名, HP, 国, バッチ(例 W21), 一言(日本語化はしない・60字まで), 業種, 状態(A=事業中/Q=買収/P=上場/I=終了)], ...]
使い方: python fetch_yc_all.py"""
import json, os, re, sys, urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
raw = urllib.request.urlopen(urllib.request.Request('https://yc-oss.github.io/api/companies/all.json', headers={'User-Agent': 'relationship-map-research/1.0 (personal use)'}), timeout=120).read()
d = json.loads(raw)
SEASON = {'Winter': 'W', 'Summer': 'S', 'Spring': 'X', 'Fall': 'F'}
ST = {'Active': 'A', 'Acquired': 'Q', 'Public': 'P', 'Inactive': 'I'}
out = []
for x in d:
    name = (x.get('name') or '').strip()
    if not name:
        continue
    loc = (x.get('all_locations') or '').split(';')[0].strip()
    ctry = loc.split(',')[-1].strip() if loc else ''
    m = re.match(r'^(Winter|Summer|Spring|Fall)\s+(\d{4})', x.get('batch') or '')
    batch = SEASON[m.group(1)] + m.group(2)[2:] if m else ''
    site = (x.get('website') or '').strip().rstrip('/')
    out.append([name, site, ctry, batch, (x.get('one_liner') or '').strip()[:60], (x.get('industry') or '').strip(), ST.get(x.get('status') or '', 'A')])
json.dump(out, open(os.path.join(S, 'yc_startups.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('YC', len(out), '社 / HPあり', sum(1 for r in out if r[1]), '/ 国の種類', len({r[2] for r in out}), '/ サイズ', os.path.getsize(os.path.join(S, 'yc_startups.json')) // 1024, 'KB')
