"""シンガポールの検索用ファイル(build_sg.mjs の出力)を D1「kigyo-sg」に足す。足すだけ(INSERT OR IGNORE)。
使い方:
  python3 load_d1.py sg                       # 最初の版(2026-11-18)と同じ、そのままの形で入れる
  python3 load_d1.py sg2 --ver 2026-11-18b    # 新しい版として、/2026-11-18b/... に圧縮して入れ、全部入ったら版の表に足して切り替える
途中で止まっても、もう一度動かせば続きから入る。前の版は消さない(サイトは版の表のいちばん新しいものを使う)。
"""
import json, os, sys, time, gzip, base64, urllib.request
from concurrent.futures import ThreadPoolExecutor
DB = "https://api.cloudflare.com/client/v4/accounts/b7b515e722cbecf8000c746711d00a41/d1/database/b1b4af48-9eac-402d-be0e-2b91cc6d01f2/query"
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "x")  # 環境のネットワーク設定でトークンが自動で付くときは x のままでよい

def q(sql, params=None):
    body = json.dumps({"sql": sql, "params": params or []}).encode()
    for t in range(5):
        try:
            r = urllib.request.urlopen(urllib.request.Request(DB, body, {"Content-Type": "application/json", "Authorization": "Bearer " + TOKEN}), timeout=180)
            return json.loads(r.read())["result"][0]["results"]
        except urllib.error.HTTPError as e:
            print(e.code, e.read()[:300], flush=True)
            if e.code < 500 and e.code != 429: raise
        except Exception as e:
            print("retry", e, flush=True)
        time.sleep(3 * (t + 1))
    raise SystemExit("failed")

src = sys.argv[1]
ver = sys.argv[sys.argv.index("--ver") + 1] if "--ver" in sys.argv else ""
pre = f"/{ver}" if ver else ""
q("CREATE TABLE IF NOT EXISTS f (path TEXT PRIMARY KEY, data TEXT NOT NULL) WITHOUT ROWID")
q("CREATE TABLE IF NOT EXISTS ver (v TEXT PRIMARY KEY, z INTEGER NOT NULL, total INTEGER, at TEXT)")
have = {r["path"] for r in q("SELECT path FROM f WHERE path LIKE ?", [pre + "/%"])}
files = sorted(f"/{d}/{fn}" for d in ("c", "n") for fn in os.listdir(os.path.join(src, d)))

def enc(p):
    t = open(src + p, "rb").read()
    return base64.b64encode(gzip.compress(t, 9)).decode() if ver else t.decode()

def put(p):
    q("INSERT OR IGNORE INTO f (path, data) VALUES (?, ?)", [pre + p, enc(p)])

todo = [p for p in files if pre + p not in have]
with ThreadPoolExecutor(8) as ex:
    for i, _ in enumerate(ex.map(put, todo), 1):
        if i % 100 == 0: print(i, flush=True)
got = {r["path"] for r in q("SELECT path FROM f WHERE path LIKE ?", [pre + "/%"])}
miss = [p for p in files if pre + p not in got]
print("added", len(todo), "missing", len(miss))
if miss: raise SystemExit("まだ入っていないものがあるので、切り替えない")
if ver:
    total = json.load(open(src + "/c/meta.json"))["total"]
    q("INSERT OR IGNORE INTO ver (v, z, total, at) VALUES (?, 1, ?, datetime('now'))", [ver, total])
    print("switched to", ver, total)
