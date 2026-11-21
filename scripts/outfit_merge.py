# -*- coding: utf-8 -*-
"""inbox/outfit/*.json の「合格」だけを site/data/outfit_auto.js(OUTFIT_AUTO)にまとめる(2026/11/21)。
inbox/ の記録は消さないので、毎回作り直しても足すだけと同じ(人・出典URLが同じものは1件)。
画像は入れない(出典ページへのリンクと文章だけ)。使い方: python3 scripts/outfit_merge.py
"""
import glob, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CF = {'公式': 'o', '本人': 's', '本人の発言': 's', '報道': 'r'}
seen, people = set(), {}
for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', 'outfit', '2*.json'))):
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('判定') != '合格':
            continue
        key = (r['人物'], r['出典URL'])
        if key in seen:
            continue
        seen.add(key)
        p = people.setdefault(r['人物'], {'n': r['人物'], 'en': r.get('英語名', ''), 'co': r.get('会社', ''), 'looks': []})
        p['looks'].append({'d': r.get('日付', ''), 'scene': r.get('場面', ''), 'w': r.get('装い', ''),
                           'brands': [{'b': b.get('名前'), 'what': b.get('もの', ''), 'rel': b.get('関係', '着用')} for b in r.get('ブランド') or []],
                           'cf': CF.get(r.get('確かさ'), 'r'), 'src': [r.get('出典名') or '出典', r['出典URL']], 'note': r.get('備考', '')})
out = '// 装いとブランドの自動追加分(scripts/outfit_merge.py が inbox/outfit/ の合格分から作る。手で直さない)\nconst OUTFIT_AUTO=' + json.dumps(list(people.values()), ensure_ascii=False) + ';\n'
open(os.path.join(ROOT, 'site', 'data', 'outfit_auto.js'), 'w', encoding='utf-8').write(out)
print(f'{len(people)}人 / {sum(len(p["looks"]) for p in people.values())}件')
