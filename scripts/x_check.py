#!/usr/bin/env python3
"""Xのアカウントや投稿を直接確かめる道具(2026/11/19追加)。

ログインなしで使える公開の方法だけを使う:
  - プロフィール: https://x.com/<名前> のページに入っている表示名と自己紹介
  - 投稿: X公式の埋め込みサービス(publish.x.com/oembed)で本文・投稿者・日付

使い方:
  python3 scripts/x_check.py @t_blom @AnthropicAI          # プロフィールを見る
  python3 scripts/x_check.py https://x.com/jack/status/20  # 投稿を見る

できないこと: ログインが要る検索やタイムラインの一覧は見られない。
投稿のURLがわからないときは、報道記事などでURLを探してから使う。
"""
import html
import json
import re
import sys
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; relmap-checker)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def profile(handle):
    handle = handle.lstrip("@")
    try:
        t = get(f"https://x.com/{handle}")
    except Exception as e:  # noqa: BLE001
        return {"handle": handle, "error": str(e)}
    title = re.search(r"<title>([^<]*)</title>", t)
    desc = re.search(r'og:description" content="([^"]*)', t)
    title = html.unescape(title.group(1)) if title else ""
    found = "Not Found" not in title
    return {
        "handle": handle,
        "url": f"https://x.com/{handle}",
        "found": found,
        "name": title.replace(" / X", ""),
        "bio": html.unescape(desc.group(1)) if desc else "",
    }


def post(url):
    q = urllib.parse.urlencode({"url": url, "omit_script": 1})
    try:
        d = json.loads(get(f"https://publish.x.com/oembed?{q}"))
    except Exception as e:  # noqa: BLE001
        return {"url": url, "error": str(e)}
    body = html.unescape(re.sub(r"<[^>]+>", " ", d.get("html", "")))
    body = re.sub(r"\s+", " ", body).strip()
    date = re.findall(r"([A-Z][a-z]+ \d{1,2}, \d{4})", body)
    return {
        "url": url,
        "author": d.get("author_name"),
        "author_url": d.get("author_url"),
        "date": date[-1] if date else "",
        "text": body,
    }


def main(args):
    if not args:
        print(__doc__)
        return 1
    out = [post(a) if "/status/" in a else profile(a) for a in args]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
