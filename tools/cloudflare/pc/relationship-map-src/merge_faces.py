"""faces(Wikidata/X)・faces_web(公式サイト)・faces_wp(人物ページ)を、公開用のフォルダにまとめて置く。"""
import json, os, shutil
S = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(S))), 'output')
a = {}
for f in ('faces_cache.json',):
    p = os.path.join(S, f)
    if os.path.exists(p):
        a.update({k: v for k, v in json.load(open(p, encoding='utf-8')).items() if v})
for fn in ('faces_x.json', 'faces_web.json'):
    p = os.path.join(S, fn)
    if os.path.exists(p):
        for k, v in json.load(open(p, encoding='utf-8')).items():
            a.setdefault(k, v)
for d in (os.path.join(S, 'web'), OUTD):
    json.dump(a, open(os.path.join(d, 'faces.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    shutil.copy(os.path.join(S, 'x_info.json'), os.path.join(d, 'x_info.json')) if os.path.exists(os.path.join(S, 'x_info.json')) else None
    if os.path.exists(os.path.join(S, 'faces_wp.json')):
        w = json.load(open(os.path.join(S, 'faces_wp.json')))
        ks = sorted(w)
        for j in range(3):      # 1ファイル16MBまでなので3つに分ける
            json.dump({k: w[k] for k in ks[j::3]}, open(os.path.join(d, 'faces_wp_%d.json' % j), 'w'), separators=(',', ':'))
print('faces', len(a), 'wp', len(json.load(open(os.path.join(S, 'faces_wp.json'))) if os.path.exists(os.path.join(S, 'faces_wp.json')) else {}))
