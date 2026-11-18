#!/usr/bin/env python3
"""Cloudflare D1 に「足すだけ」でデータを入れる道具(標準ライブラリだけで動く)。

なぜ: 以前、同期のときに人物が消えたことがある。この道具は
  - SELECT / PRAGMA / INSERT OR IGNORE 以外の SQL を受け付けない(DELETE・UPDATE・DROP・REPLACE は拒否)
  - 入れる前と後で行数を数え、1行でも減っていたら止めて知らせる
ので、既存のデータを消したり書き換えたりできない。

鍵(トークン)について:
  - 環境変数 CLOUDFLARE_API_TOKEN があればそれを使う
  - なければ、クラウド環境の「ネットワークのシークレット」(api.cloudflare.com 宛てに
    Authorization ヘッダーを付ける設定)に任せる。鍵はリポジトリに書かない
  - アカウントID は CLOUDFLARE_ACCOUNT_ID、なければ自動で探す

使い方:
  python3 tools/cloudflare/d1_add.py whoami                 # 見えるアカウントと D1 の一覧
  python3 tools/cloudflare/d1_add.py tables  <DB名>          # 表の一覧と行数
  python3 tools/cloudflare/d1_add.py select  <DB名> "<SELECT文>"
  python3 tools/cloudflare/d1_add.py add     <DB名> <表名> <ファイル.csv|.json> [--dry-run]
      CSV は1行目が列名。JSON は [{列:値,...}, ...]。
      表にない列は無視する。主キー・UNIQUE が同じ行はそのまま残す(上書きしない)。
      主キーのない表(person_role など)では、同じ中身の行がすでにあれば足さない。
"""
import csv, json, os, re, sys, time, urllib.request, urllib.error

API = "https://api.cloudflare.com/client/v4"
BATCH_ROWS = 200          # 1回に送る行数
MAX_PARAMS = 90           # D1 の1文あたりのパラメータ上限(100)より少し下

SAFE = re.compile(r"^\s*(SELECT|PRAGMA|INSERT\s+OR\s+IGNORE\s+INTO|WITH)\b", re.I)
DANGER = re.compile(r"\b(DELETE|UPDATE|DROP|REPLACE|ALTER|TRUNCATE|CREATE|ATTACH|DETACH|VACUUM)\b", re.I)


def die(msg):
    print("止めました: " + msg, file=sys.stderr)
    sys.exit(1)


def call(method, path, body=None):
    headers = {"Content-Type": "application/json", "User-Agent": "d1-add-only/1"}
    tok = os.environ.get("CLOUDFLARE_API_TOKEN")
    if tok:
        headers["Authorization"] = "Bearer " + tok
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(4):
        req = urllib.request.Request(API + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r)
        except urllib.error.HTTPError as e:
            txt = e.read().decode("utf-8", "replace")
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 ** attempt * 3)
                continue
            die(f"Cloudflare が {e.code} を返しました: {txt[:500]}")
        if not out.get("success"):
            die("Cloudflare がエラーを返しました: " + json.dumps(out.get("errors"), ensure_ascii=False))
        return out
    die("何度試しても届きませんでした")


def account_id():
    a = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
    if a:
        return a
    res = call("GET", "/accounts")["result"]
    if len(res) != 1:
        die("アカウントが %d 個見えます。CLOUDFLARE_ACCOUNT_ID を設定してください: %s"
            % (len(res), [(x["id"], x["name"]) for x in res]))
    return res[0]["id"]


def databases(acc):
    return call("GET", f"/accounts/{acc}/d1/database?per_page=100")["result"]


def db_id(acc, name):
    for d in databases(acc):
        if d["name"] == name or d["uuid"] == name:
            return d["uuid"]
    die(f"D1 のデータベース「{name}」が見つかりません")


def query(acc, db, sql, params=None):
    if not SAFE.match(sql):
        die("この道具は SELECT / PRAGMA / INSERT OR IGNORE しか送りません: " + sql[:80])
    head = sql.split("VALUES")[0] if sql.lstrip().upper().startswith("INSERT") else sql
    if DANGER.search(head):
        die("消す・書き換える命令が入っているので送りません: " + sql[:80])
    body = {"sql": sql}
    if params:
        body["params"] = params
    return call("POST", f"/accounts/{acc}/d1/database/{db}/query", body)["result"]


def rows(res):
    return res[0]["results"] if res else []


def count(acc, db, table):
    return rows(query(acc, db, f'SELECT COUNT(*) AS n FROM "{table}"'))[0]["n"]


def columns(acc, db, table):
    cols = [r["name"] for r in rows(query(acc, db, f'PRAGMA table_info("{table}")'))]
    if not cols:
        die(f"表「{table}」がありません(この道具は表を作りません)")
    return cols


def has_key(acc, db, table):
    if any(r.get("pk") for r in rows(query(acc, db, f'PRAGMA table_info("{table}")'))):
        return True
    return any(r.get("unique") for r in rows(query(acc, db, f'PRAGMA index_list("{table}")')))


def load(path):
    if path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            data = [data]
        return data
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def add(acc, db, table, path, dry):
    cols_db = columns(acc, db, table)
    data = load(path)
    if not data:
        print("入れる行がありません")
        return
    cols = [c for c in data[0].keys() if c in cols_db]
    skipped = [c for c in data[0].keys() if c not in cols_db]
    if not cols:
        die("ファイルの列名が表の列と1つも合いません。表の列: " + ", ".join(cols_db))
    if skipped:
        print("表にない列は使いません: " + ", ".join(skipped))
    before = count(acc, db, table)
    print(f"{table}: 入れる前 {before:,} 行 / ファイル {len(data):,} 行")
    if dry:
        print("(試しなので送りません)")
        return
    if not has_key(acc, db, table):
        # 主キーがないと INSERT OR IGNORE でも重複するので、1行ずつ同じ行があるか確かめる
        keep = []
        for r in data:
            vals = [None if r.get(c) == "" else r.get(c) for c in cols]
            where = " AND ".join(f'"{c}" IS ?' for c in cols)
            if not rows(query(acc, db, f'SELECT 1 FROM "{table}" WHERE {where} LIMIT 1', vals)):
                keep.append(r)
        print(f"主キーのない表なので、すでにある {len(data) - len(keep):,} 行は足しません")
        data = keep
        if not data:
            print("足す行はありません")
            return
    per = max(1, min(BATCH_ROWS, MAX_PARAMS // len(cols)))
    collist = ",".join(f'"{c}"' for c in cols)
    one = "(" + ",".join("?" * len(cols)) + ")"
    sent = 0
    for i in range(0, len(data), per):
        chunk = data[i:i + per]
        params = []
        for r in chunk:
            for c in cols:
                v = r.get(c)
                params.append(None if v == "" else v)
        sql = f'INSERT OR IGNORE INTO "{table}" ({collist}) VALUES ' + ",".join([one] * len(chunk))
        query(acc, db, sql, params)
        sent += len(chunk)
        if (i // per) % 50 == 0:
            now = count(acc, db, table)
            if now < before:
                die(f"行数が減りました({before:,} → {now:,})。すぐ持ち主に知らせてください")
            print(f"  {sent:,} / {len(data):,} 送信、今 {now:,} 行")
    after = count(acc, db, table)
    if after < before:
        die(f"行数が減りました({before:,} → {after:,})。すぐ持ち主に知らせてください")
    print(f"完了: {before:,} → {after:,} 行(+{after - before:,})")


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return
    cmd = a[0]
    acc = account_id()
    if cmd == "whoami":
        print("アカウント:", acc)
        for d in databases(acc):
            print(f"  D1 {d['name']}  {d['uuid']}  {d.get('file_size', 0) / 1e6:.1f}MB")
    elif cmd == "tables" and len(a) >= 2:
        db = db_id(acc, a[1])
        for t in rows(query(acc, db, "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE '\\_%' ESCAPE '\\' AND name NOT LIKE 'sqlite_%'")):
            print(f"  {t['name']}: {count(acc, db, t['name']):,} 行")
    elif cmd == "select" and len(a) >= 3:
        db = db_id(acc, a[1])
        print(json.dumps(rows(query(acc, db, a[2])), ensure_ascii=False, indent=1))
    elif cmd == "add" and len(a) >= 4:
        add(acc, db_id(acc, a[1]), a[2], a[3], "--dry-run" in a)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
