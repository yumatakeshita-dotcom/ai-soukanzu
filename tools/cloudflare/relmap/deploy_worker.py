#!/usr/bin/env python3
"""kigyo-relmap の Worker(worker.mjs)を Cloudflare に置く。標準ライブラリだけで動く。

Worker は GitHub の main の site/ をそのまま配るので、ファイルを上げる必要はない。
(wrangler のファイル上げは、クラウド環境の鍵の付け方と相性が悪く 401 になるため、この形にした)
鍵はクラウド環境の Network secret が api.cloudflare.com に付ける。
使い方: python3 tools/cloudflare/relmap/deploy_worker.py [--dry-run]
"""
import json, os, sys, urllib.request, urllib.error, uuid

API = "https://api.cloudflare.com/client/v4"
NAME = "kigyo-relmap"
HERE = os.path.dirname(os.path.abspath(__file__))


def call(method, path, data=None, ctype=None):
    h = {"User-Agent": "relmap-deploy/1"}
    if os.environ.get("CLOUDFLARE_API_TOKEN") and os.environ["CLOUDFLARE_API_TOKEN"] != "placeholder":
        h["Authorization"] = "Bearer " + os.environ["CLOUDFLARE_API_TOKEN"]
    if ctype:
        h["Content-Type"] = ctype
    req = urllib.request.Request(API + path, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"止めました: Cloudflare が {e.code} を返しました: {e.read().decode('utf-8', 'replace')[:500]}")


def main():
    acc = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if not acc:
        res = call("GET", "/accounts")["result"]
        if len(res) != 1:
            sys.exit("止めました: アカウントが1つに決まりません。CLOUDFLARE_ACCOUNT_ID を設定してください")
        acc = res[0]["id"]
    code = open(os.path.join(HERE, "worker.mjs"), "rb").read()
    # keep_bindings: 画面やAPIで設定した秘密(Stripeの鍵など)を、置き直しても消さない
    meta = {"main_module": "worker.mjs", "compatibility_date": "2026-11-01", "keep_bindings": ["secret_text"]}
    # プロ会員用の D1「kigyo-pro」があれば束ねる(なければこれまでどおり束ねない。作るのは持ち主の確認のあと)
    dbs = call("GET", f"/accounts/{acc}/d1/database?name=kigyo-pro").get("result") or []
    dbs = [d for d in dbs if d.get("name") == "kigyo-pro"]
    if dbs:
        meta["bindings"] = [{"type": "d1", "name": "DB", "id": dbs[0]["uuid"]}]
        print("D1 kigyo-pro を DB として束ねます")
    else:
        print("D1 kigyo-pro はまだありません(プロ会員のAPIは 503 を返します。ほかの機能には影響しません)")
    if "--dry-run" in sys.argv:
        print(f"(試し) {NAME} に worker.mjs({len(code):,} バイト)を置きます。送りません")
        return
    b = uuid.uuid4().hex
    body = (
        f'--{b}\r\nContent-Disposition: form-data; name="metadata"; filename="metadata.json"\r\n'
        f'Content-Type: application/json\r\n\r\n{json.dumps(meta)}\r\n'
        f'--{b}\r\nContent-Disposition: form-data; name="worker.mjs"; filename="worker.mjs"\r\n'
        f'Content-Type: application/javascript+module\r\n\r\n'
    ).encode() + code + f"\r\n--{b}--\r\n".encode()
    out = call("PUT", f"/accounts/{acc}/workers/scripts/{NAME}", body, f"multipart/form-data; boundary={b}")
    if not out.get("success"):
        sys.exit("止めました: " + json.dumps(out.get("errors"), ensure_ascii=False))
    # workers.dev のアドレスで見られるようにしておく(すでに有効なら何も変わらない)
    call("POST", f"/accounts/{acc}/workers/scripts/{NAME}/subdomain",
         json.dumps({"enabled": True}).encode(), "application/json")
    print(f"OK: {NAME} を置きました → https://{NAME}.yuma-takeshita.workers.dev/")


if __name__ == "__main__":
    main()
