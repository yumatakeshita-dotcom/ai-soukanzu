# 顔写真のクレジット一覧のページ(site/credits.html)を作る。
# もとのデータ: docs/photo_rights/photo_licenses.json(2026/11/18 に Wikimedia Commons から権利情報を集めたもの)
# 使い方: python3 scripts/make_photo_credits.py  (docs/photo_rights/photo_licenses.csv も作り直す)
import json, html, os, csv
R = os.path.join(os.path.dirname(__file__), '..')
rows = json.load(open(os.path.join(R, 'docs/photo_rights/photo_licenses.json'), encoding='utf-8'))
e = lambda s: html.escape(str(s or ''), quote=True)
seen, items = set(), []
for x in sorted(rows, key=lambda x: x['name'].lower()):
    if x['cat'] not in ('ok', 'credit') or not x['src']:
        continue
    k = (x['name'], x['src'])
    if k in seen:
        continue
    seen.add(k)
    nm = e(x['name']) + (f'({e(x["ja"])})' if x['ja'] else '')
    lic = f'<a href="{e(x["licurl"])}" rel="noopener license" target="_blank">{e(x["lic"])}</a>' if x['licurl'] else e(x['lic'])
    by = f'撮影・作者: {e(x["artist"])} / ' if x['artist'] else ''
    items.append(f'<li data-s="{e((x["name"]+" "+x["ja"]).lower())}"><b>{nm}</b><span>{by}{lic} / <a href="{e(x["src"])}" rel="noopener" target="_blank">元の画像</a></span></li>')
n_credit = sum(1 for x in rows if x['cat'] == 'credit')
page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>顔写真のクレジット</title>
<style>
:root{{--bg:#f2f4f6;--surface:#fff;--fg:#161b22;--muted:#5d6875;--line:#d5dbe1;--active:#0d8a79;color-scheme:light}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--active:#2fc2ab;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--active:#2fc2ab;color-scheme:dark}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.7 "Noto Sans JP",system-ui,-apple-system,"Hiragino Sans","Yu Gothic",sans-serif}}
main{{max-width:880px;margin:0 auto;padding:20px 16px 48px}}
h1{{font-size:20px;margin:0 0 8px}} p{{margin:6px 0}} .muted{{color:var(--muted);font-size:13px}}
a{{color:var(--active);overflow-wrap:anywhere}}
input{{width:100%;font:inherit;padding:8px 10px;margin:12px 0;border:1px solid var(--line);border-radius:8px;background:var(--surface);color:var(--fg)}}
ul{{list-style:none;margin:0;padding:0}}
li{{background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 12px;margin:6px 0;overflow-wrap:anywhere}}
li span{{display:block;color:var(--muted);font-size:12.5px}}
</style></head><body><main>
<p><a href="index.html">← 相関図に戻る</a></p>
<h1>顔写真のクレジット</h1>
<p>このサイトの顔写真は、Wikimedia Commons(Wikipedia・Wikidata で使われている画像)から、自由に使えるライセンスのものを選んで使っています。表示のために小さくし、顔の部分で切り抜いています(改変)。</p>
<p class="muted">CC BY / CC BY-SA などのライセンスの写真({n_credit}枚)は、撮影者・作者とライセンスをここに示します。パブリックドメインや CC0 の写真も、出どころがわかるよう一緒に載せています。作者名は Commons の記載をそのまま写しています。誤りや削除のご希望があればお知らせください。</p>
<p class="muted">一覧は2026年11月18日に Wikimedia Commons の記載から作りました。全{len(items)}件。</p>
<input id="q" type="search" placeholder="名前で絞り込む" aria-label="名前で絞り込む">
<ul id="list">
{chr(10).join(items)}
</ul>
</main>
<script>
const q=document.getElementById('q'),L=[...document.querySelectorAll('#list li')];
q.addEventListener('input',()=>{{const v=q.value.trim().toLowerCase();L.forEach(li=>li.hidden=v&&!li.dataset.s.includes(v))}});
</script>
</body></html>
'''
open(os.path.join(R, 'site/credits.html'), 'w', encoding='utf-8').write(page)
print('site/credits.html', len(items), '件')

# 一覧表(Excelで開ける)も作り直す
CAT = {'ok': 'OK(表記なしで使える)', 'credit': 'クレジットが必要', 'risk': '要注意', 'hidden': '表示を止めている', 'initials': 'イニシャル表示に変えた'}
ORDER = ['risk', 'initials', 'credit', 'ok', 'hidden']
with open(os.path.join(R, 'docs/photo_rights/photo_licenses.csv'), 'w', newline='', encoding='utf-8-sig') as fo:
    w = csv.writer(fo)
    w.writerow(['判定', '置き場所', 'キー', '名前(英)', '名前(日)', '手がかり', 'ライセンス', '作者', '元の画像', 'ライセンスのURL', '利用の制限', '候補の画像の数', 'メモ'])
    for x in sorted(rows, key=lambda x: (ORDER.index(x['cat']), x['set'], x['name'])):
        w.writerow([CAT[x['cat']], x['set'], x['key'], x['name'], x['ja'], x['origsrc'], x['lic'], x['artist'], x['src'], x['licurl'], x['restr'], x['nfiles'], x['why']])
print('docs/photo_rights/photo_licenses.csv', len(rows), '行')
