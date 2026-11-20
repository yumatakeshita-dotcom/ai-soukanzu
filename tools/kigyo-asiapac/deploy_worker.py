"""kigyo-asiapac の Worker(プログラム部分)だけを入れ替える。
今のファイル(台湾・オーストラリアのデータ)は keep_assets でそのまま残す。
使い方: python3 tools/kigyo-asiapac/deploy_worker.py   (トークンは環境のネットワーク設定から自動で付く)
元に戻すとき: python3 tools/kigyo-asiapac/deploy_worker.py --rollback <version_id>
"""
import json, sys, uuid, urllib.request, os
A = "b7b515e722cbecf8000c746711d00a41"
CF = f"https://api.cloudflare.com/client/v4/accounts/{A}/workers/scripts/kigyo-asiapac"
SGDB = "b1b4af48-9eac-402d-be0e-2b91cc6d01f2"  # D1「kigyo-sg」
H = {"Authorization": "Bearer " + os.environ.get("CLOUDFLARE_API_TOKEN", "x")}

def call(url, data=None, headers=None, method=None):
    r = urllib.request.Request(url, data=data, headers={**H, **(headers or {})}, method=method)
    try:
        return json.loads(urllib.request.urlopen(r, timeout=120).read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")

if len(sys.argv) > 2 and sys.argv[1] == "--rollback":
    body = json.dumps({"strategy": "percentage", "versions": [{"version_id": sys.argv[2], "percentage": 100}]}).encode()
    print(json.dumps(call(CF + "/deployments", body, {"Content-Type": "application/json"}, "POST"), ensure_ascii=False)[:500])
    sys.exit()

js = open(os.path.join(os.path.dirname(__file__), "worker.js"), "rb").read()
meta = {"main_module": "worker.js", "compatibility_date": "2026-11-01", "keep_assets": True,
        "bindings": [{"type": "assets", "name": "ASSETS"}, {"type": "d1", "name": "SGDB", "id": SGDB}]}
b = uuid.uuid4().hex
body = (f'--{b}\r\nContent-Disposition: form-data; name="metadata"\r\nContent-Type: application/json\r\n\r\n{json.dumps(meta)}\r\n'
        f'--{b}\r\nContent-Disposition: form-data; name="worker.js"; filename="worker.js"\r\nContent-Type: application/javascript+module\r\n\r\n').encode() + js + f'\r\n--{b}--\r\n'.encode()
r = call(CF, body, {"Content-Type": "multipart/form-data; boundary=" + b}, "PUT")
print(r.get("success"), r.get("errors"), (r.get("result") or {}).get("etag"))
