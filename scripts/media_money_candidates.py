#!/usr/bin/env python3
"""番組・動画の説明文から「出資の候補」の文だけを拾い、確かめる順番の一覧を作る(2026/11/21追加)。

inbox/podcasts/ と inbox/youtube/ の説明文を読み、「○○が△ドル調達」「シリーズB」「led by」などの具体的な文を探す。
すでに inbox/money/ にある会社(to)は飛ばす。結果は inbox/media/candidates-日付.md に書くだけ。
相関図には入れない。確かめる人が出典の記事を開いて、日付・金額・リードを確かめてから inbox/money に足す。
  python3 scripts/media_money_candidates.py [--days 30]
"""
import argparse, datetime, glob, json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r"(raised|raises|secures?d?|closes?d?)\s+(about\s+|over\s+|more than\s+)?(US)?[\$¥₹S]?\$?\s?[\d.,]+\s?(million|billion|M|B|mn|bn|crore)?"
                 r"|series\s+[a-e]\b.{0,80}(led|round)|led by [A-Z]|シリーズ[A-E][^。]{0,40}(調達|ラウンド|クローズ)|[\d.,]+(億円?|万ドル|億ドル)を?調達|領投", re.I)


def known_targets():
    s = set()
    for f in glob.glob(os.path.join(ROOT, "inbox", "money", "*.json")):
        try:
            for it in json.load(open(f, encoding="utf-8")).get("items", []):
                s.add(re.sub(r"\W", "", str(it.get("to", "")).lower()))
        except Exception:
            pass
    return s


def main(days=30):
    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    known, out, seen = known_targets(), [], set()
    for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "podcasts", "2*.json")) +
                    glob.glob(os.path.join(ROOT, "inbox", "youtube", "2*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for v in d.get("videos", []) + d.get("episodes", []):
            key = v["title"]
            if v["published"] < cutoff or key in seen:
                continue
            seen.add(key)
            text = re.sub(r"\s+", " ", v.get("description", ""))
            for s in re.split(r"(?<=[.。!?])\s*", text):
                if PAT.search(s) and 20 < len(s) < 400:
                    if any(k and k in re.sub(r"\W", "", s.lower()) for k in known if len(k) > 3):
                        break
                    out.append({"date": v["published"], "show": v.get("show") or v.get("channel"),
                                "title": v["title"], "url": v.get("url", ""), "sentence": s})
                    break
    out.sort(key=lambda x: x["date"], reverse=True)
    today = time.strftime("%Y-%m-%d")
    path = os.path.join(ROOT, "inbox", "media", f"candidates-{today}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# 出資の候補(説明文から) {today}\n\n確かめる前の手がかりです。相関図には入れません。{len(out)}件\n\n")
        for o in out:
            f.write(f"- {o['date']} {o['show']} / {o['title'][:70]}\n  - {o['sentence']}\n  - {o['url']}\n")
    print(f"出資の候補{len(out)}件 →", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=30)
    main(ap.parse_args().days)
