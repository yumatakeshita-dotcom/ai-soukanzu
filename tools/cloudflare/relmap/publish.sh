#!/usr/bin/env bash
# site/ を kigyo-relmap に公開する(クラウドの定期タスク用)。
# 鍵はクラウド環境の Network secret(api.cloudflare.com の Authorization)が付ける。
# 使い方: bash tools/cloudflare/relmap/publish.sh [--dry-run]
set -euo pipefail
cd "$(dirname "$0")"
SITE=../../../site
# 公開前の確認: 必要なファイルがそろっているか(欠けたまま公開すると、そのファイルが公開側から消えるため)
for f in index.html bulk.json people.json faces.json x_info.json pb/meta.json aw/0.json; do
  [ -s "$SITE/$f" ] || { echo "止めました: $SITE/$f がありません"; exit 1; }
done
grep -q 'data/' "$SITE/index.html" || { echo "止めました: index.html が data/ を読み込んでいません"; exit 1; }
n=$(find "$SITE" -type f | wc -l)
[ "$n" -ge 150 ] || { echo "止めました: ファイルが $n 個しかありません"; exit 1; }
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-placeholder}"
if [ -z "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then
  CLOUDFLARE_ACCOUNT_ID=$(curl -sS https://api.cloudflare.com/client/v4/accounts | python3 -c 'import json,sys;r=json.load(sys.stdin)["result"];print(r[0]["id"] if len(r)==1 else "")')
  export CLOUDFLARE_ACCOUNT_ID
fi
[ -n "$CLOUDFLARE_ACCOUNT_ID" ] || { echo "止めました: Cloudflare のアカウントがわかりません"; exit 1; }
if [ "${1:-}" = "--dry-run" ]; then
  npx -y wrangler@4 deploy --dry-run
else
  npx -y wrangler@4 deploy
fi
echo "公開先: https://kigyo-relmap.yuma-takeshita.workers.dev/"
