#!/usr/bin/env python3
"""プロ会員のアクセスキーを1つ作る。標準ライブラリだけで動く。

使い方:
  python3 tools/cloudflare/relmap/pro_issue.py --plan business --note "A社(請求書払い)" [--days 365]

やること:
  1. ランダムなキーを作って、画面に1回だけ表示する(会員に渡す。あとからは取り出せない)
  2. キーのハッシュだけの行を pro_keys.json に書く
  3. 次の1行を実行すると、D1(kigyo-pro)に「足すだけ」で入る(上書き・削除はしない)
       python3 tools/cloudflare/d1_add.py add kigyo-pro pro_keys pro_keys.json
※ pro_keys.json はキーそのものを含まないが、リポジトリには入れない(.gitignore 済み)。
"""
import argparse, datetime, hashlib, json, secrets

ap = argparse.ArgumentParser()
ap.add_argument("--plan", choices=["personal", "business"], default="personal")
ap.add_argument("--note", default="", help="会員の目印。メールアドレスは書かない")
ap.add_argument("--days", type=int, default=0, help="有効な日数。0なら期限なし")
ap.add_argument("--out", default="pro_keys.json")
a = ap.parse_args()

key = secrets.token_urlsafe(24)  # 32文字(A-Z a-z 0-9 - _)
now = datetime.datetime.now(datetime.timezone.utc)
row = {
    "key_hash": hashlib.sha256(key.encode()).hexdigest(),
    "plan": a.plan,
    "status": "active",
    "expires_at": (now + datetime.timedelta(days=a.days)).isoformat() if a.days else None,
    "note": a.note,
    "created_at": now.isoformat(),
}
json.dump([row], open(a.out, "w"), ensure_ascii=False)
print("アクセスキー(会員に1回だけ渡す。この画面を閉じると見られません):")
print(key)
print(f"\n{a.out} に書きました。次を実行すると D1 に足されます:")
print(f"  python3 tools/cloudflare/d1_add.py add kigyo-pro pro_keys {a.out}")
