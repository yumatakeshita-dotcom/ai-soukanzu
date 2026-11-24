#!/usr/bin/env python3
"""毎週の使用量の目安を inbox/usage/YYYY-MM-DD.md に保存する(足すだけ)。
正確な使用量(トークン数)はここからは取れないので、
「main への commit の件数」と「inbox/ に増えたファイル数」から、各定期タスクが何回動いたかの目安を出す。
使い方: python3 scripts/usage_report.py [--days 7]
"""
import jst
import subprocess, datetime, argparse, re, os, collections

# commit メッセージの先頭 → 定期タスク名 と モデル(docs/task_models.md と同じ)
TASKS = [
    ("毎日更新", "AI企業の相関図 毎日更新", "標準"),
    ("調査(moves)", "調査: 引き抜き", "標準"),
    ("調査(money)", "調査: お金の流れ", "標準"),
    ("調査(vc)", "調査: LP・VC資金", "標準"),
    ("調査(world)", "調査: 世界企業", "標準"),
    ("調査(deep)", "調査: 深堀り", "標準"),
    ("調査(薄いところ)", "調査: まだ薄いところ", "標準"),
    ("Xアカウント一覧に追加", "Xアカウント毎日10個", "標準(軽くできる)"),
    ("調査の新着を追加", "調査の新着をサイトに追加", "標準(軽くできる)"),
    ("ニュースのリンクを元記事に", "ニュースのリンク直し", "標準(軽くできる)"),
    ("数字の確かめ直し", "報道だけの数字を確かめ直す", "標準"),
    ("週のまとめ", "週のまとめ(月曜)", "標準"),
]

ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=7)
a = ap.parse_args()
since = (jst.today() - datetime.timedelta(days=a.days)).isoformat()
log = subprocess.run(["git", "log", "origin/main", f"--since={since}", "--pretty=%s"],
                     capture_output=True, text=True).stdout.splitlines()
cnt = collections.Counter()
for s in log:
    for key, name, _ in TASKS:
        if s.startswith(key):
            cnt[name] += 1
            break

out = [f"# 定期タスクの使用量の目安 ({since} 〜 {jst.today()})", "",
       "※ トークン数そのものは取れません。main への commit の件数(=その回に変更が出た回数)と、",
       "inbox/ に増えたファイル数からの目安です。変更が無かった回は数えられません。", "",
       "| 定期タスク | モデル | commit した回数 |", "|---|---|---|"]
for key, name, model in TASKS:
    out.append(f"| {name} | {model} | {cnt.get(name, 0)} |")

out += ["", "## inbox/ に増えたファイル(期間内の日付名)", "", "| 種類 | 件数 |", "|---|---|"]
for kind in ["moves", "money", "vc", "world", "deep", "verify", "disclosures", "usage"]:
    d = os.path.join("inbox", kind)
    n = 0
    if os.path.isdir(d):
        for f in os.listdir(d):
            m = re.match(r"(\d{4}-\d{2}-\d{2})", f)
            if m and m.group(1) >= since:
                n += 1
    out.append(f"| {kind} | {n} |")

out += ["", "## 目安の読み方", "",
        "- 週あたりの回数(予定): 引き抜き7・Xアカウント7・毎日更新7・調査の新着7・リンク直し7・公開7・D1追加7、お金2、他は週1。",
        "- 回数が予定より少ない = 途中で止まった回があるかもしれない。",
        "- 正確な使用量は claude.ai の設定 → 使用量 で確認する。"]

today = jst.today().isoformat()
os.makedirs("inbox/usage", exist_ok=True)
p = f"inbox/usage/{today}.md"
if os.path.exists(p):
    p = f"inbox/usage/{today}-2.md"
open(p, "w", encoding="utf-8").write("\n".join(out) + "\n")
print(p)
