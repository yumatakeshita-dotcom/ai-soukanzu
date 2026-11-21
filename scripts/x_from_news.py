#!/usr/bin/env python3
"""報道の記事から、記事に載っているXの投稿をたどって本人の投稿か確かめる道具(2026/11/19追加)。

Xの検索はログインが要るので使えない。代わりに:
  1. 記事のページを開き、本文に埋め込まれた・リンクされた x.com / twitter.com の投稿URLを拾う
  2. それぞれを X公式の埋め込みサービス(scripts/x_check.py と同じ publish.x.com/oembed)で開き、
     投稿者・日付・本文を確かめる
  3. --handles で inbox/x_accounts.txt の見るアカウントと照らし、一覧のアカウントの投稿に印を付ける

使い方:
  python3 scripts/x_from_news.py 記事URL [記事URL ...]
  python3 scripts/x_from_news.py --handles inbox/x_accounts.txt 記事URL
  python3 scripts/x_from_news.py --kind money 記事URL   # 一覧のうち「見る種類」に money があるものだけ照らす

結果は JSON: 記事ごとに見つかった投稿(url, author, author_url, date, text, watched)。
出典にするときは、投稿者が会社・本人の公式アカウントか(プロフィールは x_check.py @名前 で確かめる)を見てから
confidence を「本人の発言」(会社の公式アカウントなら「公式」)にする。記事は開けないこともある(ネットワークの許可外)。
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x_check import post  # noqa: E402

UA = "Mozilla/5.0 (compatible; relmap-checker)"
STATUS = re.compile(r"https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/status(?:es)?/(\d{5,25})")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def watched_handles(path, kind):
    hs = set()
    if not path or not os.path.exists(path):
        return hs
    for line in open(path, encoding="utf-8"):
        if not line.startswith("@"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if kind and (len(parts) < 2 or kind not in parts[1]):
            continue
        hs.add(parts[0].lstrip("@").lower())
    return hs


def links_in(page):
    page = html.unescape(page)
    seen, out = set(), []
    for m in STATUS.finditer(page):
        user, sid = m.group(1), m.group(2)
        if user.lower() in ("i", "intent", "share", "home"):
            continue
        if sid in seen:
            continue
        seen.add(sid)
        out.append(f"https://x.com/{user}/status/{sid}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("articles", nargs="+")
    ap.add_argument("--handles", default="")
    ap.add_argument("--kind", default="")
    ap.add_argument("--max", type=int, default=10, help="記事1本あたりに確かめる投稿の数")
    a = ap.parse_args()
    if a.kind and not a.handles:
        a.handles = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                 "inbox", "x_accounts.txt")
    watch = watched_handles(a.handles, a.kind)
    res = []
    for art in a.articles:
        r = {"article": art, "posts": []}
        try:
            links = links_in(get(art))
        except Exception as e:  # noqa: BLE001
            r["error"] = f"記事を開けませんでした: {e}"
            res.append(r)
            continue
        for u in links[: a.max]:
            p = post(u)
            au = (p.get("author_url") or "").rstrip("/").rsplit("/", 1)[-1].lower()
            p["watched"] = bool(au and au in watch)
            r["posts"].append(p)
        r["found"] = len(links)
        res.append(r)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
