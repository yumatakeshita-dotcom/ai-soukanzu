"""相関図の公開版を Cloudflare の静的サイトへ置く(Claude不要・トークン0)。
claude.ai の Artifact は使わない(2026-11-17 に切り替え)。

手順:
  1) python -I refresh.py --no-fetch   … output\\relationship-maps.html を作る
  2) python -I publish_static.py       … そのページと、ページが読む補助ファイルを docs\\rooms\\relationship-map-static\\public に集める
  3) cd docs\\rooms\\relationship-map-site と npx wrangler deploy -c ..\\relationship-map-static\\wrangler.toml
     (または 公開.bat を実行する)

このスクリプトは、公開フォルダの中身を作り直す(前回のファイルは消す)。
注意: 元の output フォルダは読むだけで、書き換えない。
"""
import os, shutil, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(SRC, '..', '..', '..', 'output'))
PUB = os.path.normpath(os.path.join(SRC, '..', 'relationship-map-static', 'public'))

PAGE = os.path.join(OUT, 'relationship-maps.html')
# ページが fetch() で読む補助ファイル(output の中にある)。ファイル名は build/hub_template の fetch() と一致させる
FILES = ['bulk.json', 'people.json', 'faces.json', 'faces_wp_0.json', 'faces_wp_1.json', 'faces_wp_2.json', 'x_info.json']
DIRS = ['aw', 'pb']          # 会社の図の遅延読み込み(aw/NN.json)、人物検索(pb/NNN.json)

if not os.path.exists(PAGE):
    sys.exit('失敗: output\\relationship-maps.html がありません。先に refresh.py を実行してください。')
size_mb = os.path.getsize(PAGE) / 1e6
if size_mb > 24:
    sys.exit('失敗: ページが %.1fMB。Cloudflareの1ファイル上限(25MiB)に近いので、確認が必要です。' % size_mb)

os.makedirs(PUB, exist_ok=True)
shutil.copyfile(PAGE, os.path.join(PUB, 'index.html'))
missing = []
for f in FILES:
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        shutil.copyfile(p, os.path.join(PUB, f))
    else:
        missing.append(f)
for d in DIRS:
    src, dst = os.path.join(OUT, d), os.path.join(PUB, d)
    if os.path.isdir(src):
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        missing.append(d + '/')

n = sum(len(fs) for _, _, fs in os.walk(PUB))
print('OK: 公開フォルダを作りました', PUB, '(ファイル %d 個、ページ %.1fMB)' % (n, size_mb))
if missing:
    print('注意: 見つからなかったもの(ページの該当機能は空になります): ' + ', '.join(missing))
