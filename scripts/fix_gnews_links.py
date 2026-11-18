"""Googleニュースの転送リンク(news.google.com/rss/articles/...)を元の記事のURLに置き換える。

使い方:
  1. node scripts/resolve_gnews.js <URL一覧.txt> <結果.jsonl>   # ブラウザで開いて転送先を記録する
  2. python3 scripts/fix_gnews_links.py <結果.jsonl>            # 下のファイルのリンクを置き換える

- 転送先がわかったものだけ置き換える。わからなかったものは今のリンクのまま残す(消さない)
- わかった対応は scripts/gnews_map.json に足していく(次回の更新でも使える)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = os.path.join(ROOT, "scripts", "gnews_map.json")
TARGETS = ["site/gnews.json", "site/index.html"] + [
    "site/data/" + f for f in sorted(os.listdir(os.path.join(ROOT, "site/data"))) if f.endswith(".js")]
GN = re.compile(r'https://news\.google\.com/rss/articles/[A-Za-z0-9_-]+(?:\?oc=5)?')
BAD = re.compile(r'["\\<>\s]')

def ok(u):
    return (u and u.startswith(("https://", "http://")) and not BAD.search(u)
            and "google.com" not in u.split("/")[2] and len(u) < 2000)

def main():
    m = json.load(open(MAP)) if os.path.exists(MAP) else {}
    for p in sys.argv[1:]:
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            if ok(o.get("to")):
                m[o["from"]] = o["to"]
    json.dump(m, open(MAP, "w"), ensure_ascii=False, indent=0, sort_keys=True)
    total = left = 0
    for t in TARGETS:
        f = os.path.join(ROOT, t)
        if not os.path.exists(f):
            continue
        s = open(f, encoding="utf-8").read()
        n = [0]
        def rep(mo):
            u = mo.group(0)
            to = m.get(u) or m.get(u + "?oc=5") or m.get(u.replace("?oc=5", ""))
            if to:
                n[0] += 1
                return to
            return u
        s2 = GN.sub(rep, s)
        rest = len(GN.findall(s2))
        if n[0]:
            open(f, "w", encoding="utf-8").write(s2)
        total += n[0]; left += rest
        if n[0] or rest:
            print(f"{t}: 置き換え {n[0]} 件 / 残り {rest} 件")
    print(f"合計: 置き換え {total} 件 / 元のURLがわからず残したもの {left} 件 / 対応表 {len(m)} 件")

if __name__ == "__main__":
    main()
