"""相関図の会社ごとに、Googleニュース(日本経済新聞・ロイター・朝日・TechCrunch・THE BRIDGE・PR TIMESなど、多くのニュースサイトの見出しを集めたもの)で
最近(60日以内)のニュースを探して、見出し・リンク・日付・配信元だけを news_cos.json に保存する。Yahoo!ニュース(yahoo_cos.json)と合わせて、会社の概要と「AIに聞く」で使う。本文は保存しない。Claude不要。
形: {会社名: [[日付, 見出し, URL, 配信元], ...(新しい順に最大6件)]}
使い方: python -I fetch_news_cos.py [件数の上限]"""
import datetime as dt, html, json, os, re, sys, time, urllib.parse
import xml.etree.ElementTree as ET
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import fetch_sources as F
from adds import apply_adds
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)
OUT = os.path.join(S, 'news_cos.json')
names = ['OpenAI', 'Anthropic', 'xAI']
for key, c in CO_ALL.items():
    n = next((x['name'] for x in c['N'] if x['id'] == c.get('center')), '')
    if n:
        names.append(n)
try:      # 相関図の外から足した会社(東証の上場企業・スタートアップ・米国上場の日本企業)も調べる
    import sqlite3 as _sq
    _db = _sq.connect('file:' + os.path.join(os.path.expanduser('~'), '.claude', 'data', 'houjin.sqlite').replace(chr(92), '/') + '?mode=ro', uri=True)
    names += [r[0] for r in _db.execute("select name from mapco where slug like 'jpx_%' or slug like 'su_%' or slug like 'usjp_%'")]
except Exception:
    pass
names = list(dict.fromkeys(n.strip() for n in names if n and len(n.strip()) >= 2))
old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
cut = (dt.date.today() - dt.timedelta(days=45)).isoformat()
limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
TS = os.path.join(S, 'news_cos_ts.json')
ts = json.load(open(TS, encoding='utf-8')) if os.path.exists(TS) else {}
names.sort(key=lambda n: ts.get(n, ''))      # 長く調べていない会社から順に


def feed(q, hl, gl, ceid):
    b = F.get('https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s' % (urllib.parse.quote(q), hl, gl, ceid), timeout=30)
    rows = []
    if not b:
        return rows
    try:
        root = ET.fromstring(b)
    except ET.ParseError:
        return rows
    for it in root.iter():
        if not it.tag.endswith('item'):
            continue
        g = lambda t: next((c.text for c in it if c.tag.endswith(t) and c.text), '')
        title, link = html.unescape(g('title')).strip(), (g('link') or '').strip()
        m = re.search(r'\s[-–|]\s([^-–|]{2,40})$', title)
        media = ''
        if m:
            media, title = m.group(1).strip(), title[:m.start()]
        d = F.parse_date(g('pubDate'))
        if title and link:
            rows.append((d, title[:160], link, media))
    return rows


done = 0
for nm in names:
    if done >= limit:
        break
    key = re.sub(r'\s*[\(（].*?[\)）]', '', nm).strip().lower()
    ascii_name = nm.isascii()
    rows = []
    seen = set()
    for hl, gl, ceid in ((('ja', 'JP', 'JP:ja'), ('en-US', 'US', 'US:en')) if ascii_name else (('ja', 'JP', 'JP:ja'),)):
        q = '"%s" when:60d' % key if ascii_name else '%s when:60d' % nm
        for r in feed(q, hl, gl, ceid):
            if r[0] < cut or r[2] in seen or key not in r[1].lower():
                continue
            seen.add(r[2])
            rows.append(list(r))
        time.sleep(1.0)
        if len(rows) >= 4:
            break
    rows.sort(key=lambda x: x[0], reverse=True)
    if rows:
        old[nm] = rows[:4]
    elif nm in old and old[nm] and old[nm][0][0] < cut:
        del old[nm]
    done += 1
    ts[nm] = dt.date.today().isoformat()
    if done % 25 == 0:
        json.dump(old, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(ts, open(TS, 'w', encoding='utf-8'))
        print('進み', done, '/', len(names), '会社数', len(old), flush=True)
json.dump(old, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(ts, open(TS, 'w', encoding='utf-8'))
print('ニュース(会社別・Googleニュース):', len(old), '社 /', len(names), '社を調べた', flush=True)
