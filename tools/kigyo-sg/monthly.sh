#!/bin/bash
# シンガポールの会社を、毎月新しい版にする(足すだけ。前の版は消さない)。
# 使い方: bash tools/kigyo-sg/monthly.sh   (リポジトリの一番上のフォルダで)
set -euo pipefail
REPO=$(pwd); W=${WORK:-/tmp/kigyo-sg-work}; V=$(TZ=Asia/Tokyo date +%F)
mkdir -p "$W" && cd "$W"
python3 "$REPO/tools/kigyo-sg/sg_acra.py"
N=$(($(wc -l < sg_companies.csv) - 1))
PREV=$(python3 -I - <<'PY'
import json,urllib.request
DB="https://api.cloudflare.com/client/v4/accounts/b7b515e722cbecf8000c746711d00a41/d1/database/b1b4af48-9eac-402d-be0e-2b91cc6d01f2/query"
r=json.loads(urllib.request.urlopen(urllib.request.Request(DB,json.dumps({"sql":"SELECT coalesce((SELECT total FROM ver ORDER BY v DESC LIMIT 1),624977) t, (SELECT sum(length(data)) FROM f) s"}).encode(),{"Content-Type":"application/json","Authorization":"Bearer x"})).read())
x=r["result"][0]["results"][0]; print(x["t"], x["s"])
PY
)
read PT SIZE <<< "$PREV"
echo "今回 $N 社 / 前の版 $PT 社 / データベースの中身 $SIZE バイト"
# 件数が前の版より1割以上減ったら、取り込みの失敗かもしれないので切り替えない
if [ "$N" -lt $((PT * 9 / 10)) ]; then echo "件数が大きく減ったので止めます"; exit 2; fi
# 無料プランの上限(1つのデータベースで500MB)に近づいたら止める。古い版を消すかは持ち主が決める
if [ "$SIZE" -gt 400000000 ]; then echo "データベースが400MBを超えたので止めます"; exit 3; fi
rm -rf sgv && node --max-old-space-size=6000 "$REPO/tools/kigyo-sg/build_sg.mjs" sg_companies.csv sgv
python3 -u "$REPO/tools/kigyo-sg/load_d1.py" sgv --ver "$V"
cp sg_status.txt "$REPO/tools/kigyo-sg/last_status.txt" 2>/dev/null || true
echo "完了: 版 $V($N 社)"
