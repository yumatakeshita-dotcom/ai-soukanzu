#!/usr/bin/env bash
# kigyo-relmap の公開を確かめる(クラウドの定期タスク用)。
# 2026-11-18 から kigyo-relmap は GitHub の main の site/ をそのまま配る Worker になった。
# なので毎日ファイルを上げる必要はなく、Worker がなければ置き、公開側が main と同じかを確かめるだけ。
set -euo pipefail
cd "$(dirname "$0")"
URL=https://kigyo-relmap.yuma-takeshita.workers.dev
want=$(grep -o "LAST_CHECK='[0-9-]*'" ../../../site/index.html | head -1)
got=$(curl -s -m 60 "$URL/" | grep -o "LAST_CHECK='[0-9-]*'" | head -1 || true)
if [ "$got" != "$want" ] || [ "${1:-}" = "--force" ]; then
  python3 deploy_worker.py
  sleep 20
  got=$(curl -s -m 60 "$URL/?t=$(date +%s)" | grep -o "LAST_CHECK='[0-9-]*'" | head -1 || true)
fi
echo "main: $want / 公開側: $got"
for f in data/finds.js pb/meta.json bulk.json aw/0.json; do
  printf '%s ' "$f"; curl -s -o /dev/null -w '%{http_code}\n' -m 60 "$URL/$f"
done
[ "$got" = "$want" ] || { echo "注意: 公開側がまだ main と違います(GitHub側の5分ほどの遅れのことがあります)"; exit 1; }
