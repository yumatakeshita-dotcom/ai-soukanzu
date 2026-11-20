#!/usr/bin/env python3
"""ニュースの見出しを集めて site/data/relnews.js の先頭に足す(足すだけ・URLが同じものは足さない)。
あわせて index.html の BUILT(データの時点)を今の日本時間に更新する。
使い方: python3 scripts/fetch_relnews.py [--dry]
"""
import json, re, sys, urllib.request, urllib.parse, html
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

JST = timezone(timedelta(hours=9))
GN = "https://news.google.com/rss/search?q=%s&hl=%s&gl=%s&ceid=%s"
FEEDS = [  # (url, 媒体名, r: j=日本 w=世界)
    ("https://prtimes.jp/index.rdf", "PR TIMES", "j"),
    ("https://thebridge.jp/feed", "THE BRIDGE", "j"),
    ("https://techcrunch.com/feed/", "TechCrunch", "w"),
]
for q in ["AI 資金調達 スタートアップ", "生成AI 買収 提携", "OpenAI OR Anthropic", "NVIDIA OR 半導体 投資",
          "AI 幹部 就任 退任 移籍", "データセンター 投資 AI"]:
    FEEDS.append((GN % (urllib.parse.quote(q + " when:2d"), "ja", "JP", "JP:ja"), "Google News", "j"))
for q in ["AI startup funding round", "OpenAI Anthropic xAI", "Nvidia AMD chips deal", "AI executive joins leaves"]:
    FEEDS.append((GN % (urllib.parse.quote(q + " when:2d"), "en-US", "US", "US:en"), "Google News", "w"))

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (relmap news fetch)"})
    return urllib.request.urlopen(req, timeout=30).read()

def parse(data, src, r):
    root = ET.fromstring(data)
    out = []
    for it in root.iter():
        tag = it.tag.split('}')[-1]
        if tag not in ("item", "entry"):
            continue
        def f(n):
            for c in it:
                if c.tag.split('}')[-1] == n:
                    return (c.text or "").strip() if n != "link" or c.text else (c.get("href") or "")
            return ""
        link, title = f("link"), html.unescape(f("title"))
        ds = f("pubDate") or f("date") or f("published") or f("updated")
        try:
            d = parsedate_to_datetime(ds)
        except Exception:
            try:
                d = datetime.fromisoformat(ds.replace("Z", "+00:00"))
            except Exception:
                continue
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        desc = re.sub(r"<[^>]+>", "", html.unescape(f("description") or f("summary")))
        desc = re.sub(r"\s+", " ", desc).strip()
        if src == "Google News":
            desc = ""
        if link and title:
            out.append({"u": link, "t": title, "d": d.astimezone(JST).strftime("%Y-%m-%d"), "s": src, "r": r,
                        "x": desc[:120] + ("..." if len(desc) > 120 else "")})
    return out

def main():
    dry = "--dry" in sys.argv
    p = "site/data/relnews.js"
    s = open(p, encoding="utf-8").read()
    i, j = s.index("["), s.rindex("]") + 1
    cur = json.loads(s[i:j])
    have = {x["u"] for x in cur}
    cutoff = (datetime.now(JST) - timedelta(days=4)).strftime("%Y-%m-%d")
    new = []
    for url, src, r in FEEDS:
        try:
            for x in parse(get(url), src, r):
                if x["u"] not in have and x["d"] >= cutoff:
                    have.add(x["u"]); new.append(x)
        except Exception as e:
            print("取れなかった:", src, url[:70], e)
    new.sort(key=lambda x: x["d"], reverse=True)
    print(f"新しい見出し {len(new)}件(いまの記録 {len(cur)}件)")
    if dry:
        return
    if new:
        merged = new + cur
        open(p, "w", encoding="utf-8").write(s[:i] + json.dumps(merged, ensure_ascii=False, separators=(",", ":")) + s[j:])
    now = datetime.now(JST).strftime("%Y-%m-%d %H:%M")
    ix = open("site/index.html", encoding="utf-8").read()
    ix2 = re.sub(r"const BUILT='[^']*';", f"const BUILT='{now}';", ix, count=1)
    open("site/index.html", "w", encoding="utf-8").write(ix2)
    print("データの時点:", now)

if __name__ == "__main__":
    main()
