"""相関図の会社ごとに、Yahoo!ニュースの検索で最近(90日以内)のニュースを探して、見出し・リンク・日付・配信元だけを yahoo_cos.json に保存する。
相関図ページの会社の概要と、「AIに聞く」の根拠に使う。本文は保存しない。Claude不要。
形: {会社名: [[日付, 見出し, URL, 配信元], ...(新しい順に最大5件)]}
使い方: python -I fetch_yahoo_cos.py"""
import datetime as dt, json, os, re, sys, time
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import fetch_yahoo as Y
from adds import apply_adds
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)
OUT = os.path.join(S, 'yahoo_cos.json')
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
TS = os.path.join(S, 'yahoo_cos_ts.json')
ts = json.load(open(TS, encoding='utf-8')) if os.path.exists(TS) else {}
names.sort(key=lambda n: ts.get(n, ''))      # 長く調べていない会社から順に
done = 0
for nm in names:
    if done >= limit:
        break
    page = Y.fetch(nm)
    done += 1
    ts[nm] = dt.date.today().isoformat()
    key = re.sub(r'\s*[\(（].*?[\)）]', '', nm).strip().lower()
    rows = []
    seen = set()
    for r in Y.parse(page):
        if r['d'] < cut or r['u'] in seen:
            continue
        if key and key not in r['t'].lower():
            continue
        seen.add(r['u'])
        media = re.sub(r'^Yahoo!ニュース\((.*)\)$', r'\1', r['s'])
        rows.append([r['d'], r['t'], r['u'], media])
    rows.sort(key=lambda x: x[0], reverse=True)
    if rows:
        old[nm] = rows[:3]
    else:
        old.pop(nm, None)
    if done % 25 == 0:
        json.dump(old, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(ts, open(TS, 'w', encoding='utf-8'))
        print('進み', done, '/', len(names), '会社数', len(old), flush=True)
    time.sleep(1.2)
json.dump(old, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(ts, open(TS, 'w', encoding='utf-8'))
print('Yahoo!ニュース(会社別):', len(old), '社 /', len(names), '社を調べた', flush=True)
