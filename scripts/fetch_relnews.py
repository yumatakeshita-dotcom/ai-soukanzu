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
    # 2026/11/21 追加: 許可リストに足して本文が読めると確かめた報道サイト
    ("https://news.crunchbase.com/feed/", "Crunchbase News", "w"),
    ("https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "The Verge", "w"),
    ("https://arstechnica.com/ai/feed/", "Ars Technica", "w"),
    ("https://siliconangle.com/feed/", "SiliconANGLE", "w"),
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

KW = re.compile(r"AI|人工知能|生成|OpenAI|Anthropic|Claude|ChatGPT|Gemini|NVIDIA|エヌビディア|半導体|GPU|チップ|データセンター|TSMC|ソフトバンク|xAI|Meta|Microsoft|Google|スタートアップ|資金調達|買収|出資|LLM|robot|ロボット|chip|startup|funding|acquir|raises", re.I)


def gemini_pick(items):
    """新しい見出しのうち、AI・半導体・資金調達・企業の人事や買収に関係するものをGeminiに選んでもらう。
    失敗したら None(キーワードの判定にもどる)。2026/11/20追加"""
    try:
        sys.path.insert(0, __import__("os").path.dirname(__file__))
        import gemini_research as g
        if not g.key():
            return None
        keep = set()
        for b in range(0, len(items), 80):
            chunk = items[b:b + 80]
            lines = "\n".join(f"{i}: {x['t']}" for i, x in enumerate(chunk))
            prompt = ("次の見出しのうち、AI企業・半導体・AI向けの計算資源やデータセンター・スタートアップの資金調達や買収・"
                      "AI関連企業の幹部の人事に関係するものの番号だけを選び、JSONの数字の配列だけを返してください(例: [0,3,5])。\n" + lines)
            r = g.gen({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0}})
            m = re.search(r"\[[\d,\s]*\]", g.resp_text(r))
            if not m:
                return None
            keep |= {b + i for i in json.loads(m.group(0)) if 0 <= i < len(chunk)}
        return keep
    except Exception as e:
        print("Geminiの選別は使えなかった(キーワードで代わりに選ぶ):", str(e)[:120])
        return None


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
    picked = gemini_pick(new) if new else None
    for k, x in enumerate(new):
        x["a"] = 1 if (k in picked if picked is not None else bool(KW.search(x["t"]))) else 0
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
