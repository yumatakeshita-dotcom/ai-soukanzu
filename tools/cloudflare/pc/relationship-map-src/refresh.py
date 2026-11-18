"""ワンコマンド更新: 日経のランキング取得 → ビルド → プロフィール埋め込み。Claude不要。
使い方: python refresh.py [--no-fetch]   (公開は Claude の Artifact で output\relationship-maps.html を同じURLへ)"""
import os, re, subprocess, sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')  # 予定実行(cp932のコンソール)でも文字化けで止まらないように
    except Exception:
        pass

S = os.path.dirname(os.path.abspath(__file__))
env = dict(os.environ, SKIP_UNREVIEWED='1', PYTHONIOENCODING='utf-8')

# 同時に2つ動くとデータファイルが壊れるので、実行中の目印(ロック)を作る。30分以上前の目印は古いものとして無視する
import time as _t
LOCK = os.path.join(S, 'refresh.lock')
if os.path.exists(LOCK) and _t.time() - os.path.getmtime(LOCK) < 1800 and '--ignore-lock' not in sys.argv:
    sys.exit('別の更新が実行中のため、今回はやめます(refresh.lock)。')
open(LOCK, 'w').write(str(os.getpid()))
import atexit
atexit.register(lambda: os.path.exists(LOCK) and os.remove(LOCK))


def run(*a):
    r = subprocess.run([sys.executable, *a], cwd=S, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print((r.stdout + r.stderr).strip()[-600:])
    if r.returncode:
        sys.exit(f'失敗: {a}')


if '--news-only' in sys.argv:      # 4時間ごとの軽い更新: ニュース・上場申請だけ取り直す
    run('-I', 'fetch_sources.py')
    run('-I', 'fetch_yahoo.py')      # Yahoo!ニュースの検索(資金調達・買収・提携)
elif '--no-fetch' not in sys.argv:
    run('-I', 'update_ranking.py')
    run('-I', 'update_ranking_jp.py')   # 日本企業 時価総額ランキング
if '--no-fetch' not in sys.argv and '--news-only' not in sys.argv:
    run('-I', 'parse_unicorns.py')    # 世界のユニコーン一覧(Wikipedia)を取り直す
    run('-I', 'fetch_acquisitions.py')  # 買収一覧(英語版Wikipediaの一覧ページ)。Wikidataの子会社は重いので fetch_acq_wd.py を別途
    run('-I', 'fetch_sources.py')    # 上場申請(SEC EDGAR)・資金調達ニュース・ユニコーンの新規判定
    run('-I', 'fetch_yahoo.py')
    run('-I', 'fetch_yahoo_cos.py', '400')      # 会社ごとのYahoo!ニュース(1,800社ほど。時間がかかる)
    run('-I', 'fetch_news_cos.py', '400')      # 会社ごとのニュース(Googleニュース経由。日経・ロイターなど)
run('build_hub2.py')
run('-I', 'inject_pauto.py')
out = r'C:\Users\yumat\.claude\output\relationship-maps.html'
s = open(out, encoding='utf-8').read()
s = re.sub(r'data:image/[a-z]+;base64,[A-Za-z0-9+/=]+', '', s)
os.makedirs(os.path.join(S, 'web'), exist_ok=True)
open(os.path.join(S, 'web', 'index.html'), 'w', encoding='utf-8').write('<meta charset="utf-8"><style>[hidden]{display:none!important}</style>' + s)
_mb = os.path.getsize(out) / 1e6
if _mb > 24:   # 公開先はCloudflareの静的サイト(1ファイル上限25MiB)。2026-11-17に、Claude Artifactの16MB上限から変更
    sys.exit('失敗: ページが %.1fMB と大きすぎます(Cloudflareの1ファイル上限25MiBに近い)。公開せずに、データを別ファイルに分ける対応が必要です。' % _mb)
print('OK: ビルド完了。', out, '%.1fMB' % _mb)
