#!/usr/bin/env python3
"""毎日のYouTube確認(2026/11/21追加)。inbox/youtube_channels.txt の全チャンネルを、公式RSSで必ず見る。

使い方:
  python3 scripts/yt_daily.py                # 直近7日の新着を調べ、inbox/youtube/日付.json に足す
  python3 scripts/yt_daily.py --days 14      # さかのぼる日数

やること:
  - 全チャンネルのRSS(説明文つき・最新15本)を見る。断られたら30秒・90秒待ってやり直す
  - 見られなかったチャンネルは、理由つきで記録に残す(翌日また必ず見る)
  - すでに見た動画(inbox/youtube/seen.txt と inbox/money/seen_videos.txt)は出さない
  - 最後に「YouTube確認: ○/○チャンネル、新着○本」の1行を出す。調査の notes にそのまま書く
足すだけ。消さない。断られ方をごまかす工夫はしない(待ってやり直すだけ)。
"""
import argparse, datetime, json, os, sys, time, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "inbox", "youtube_channels.txt")
OUT = os.path.join(ROOT, "inbox", "youtube")
SEEN = os.path.join(OUT, "seen.txt")
SEEN_MONEY = os.path.join(ROOT, "inbox", "money", "seen_videos.txt")
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "m": "http://search.yahoo.com/mrss/"}


def lines(p):
    if not os.path.exists(p):
        return []
    return [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]


def fetch(cid, waits=(30, 90)):
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
    err = ""
    for i in range(len(waits) + 1):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return ET.fromstring(r.read()), ""
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"[:150]
            if i < len(waits):
                time.sleep(waits[i])
    return None, err


def main(days=7, quiet=False):
    seen = {l.split("|")[0] for l in lines(SEEN)} | {l.split("|")[0] for l in lines(SEEN_MONEY)}
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    today = time.strftime("%Y-%m-%d")
    checked, videos = [], []
    for l in lines(CH):
        p = (l.split("|") + ["", "", ""])[:3]
        cid, name, kind = p
        root, err = fetch(cid)
        if root is None:
            checked.append({"channel_id": cid, "name": name, "ok": False, "error": err})
            continue
        n = 0
        for e in root.findall("a:entry", NS):
            vid = e.findtext("yt:videoId", "", NS)
            pub = e.findtext("a:published", "", NS)
            try:
                dt = datetime.datetime.fromisoformat(pub)
            except ValueError:
                continue
            if dt < cutoff or vid in seen:
                continue
            n += 1
            videos.append({"id": vid, "channel": name, "channel_id": cid, "kind": kind,
                           "title": e.findtext("a:title", "", NS), "published": pub[:10],
                           "url": f"https://www.youtube.com/watch?v={vid}",
                           "description": (e.findtext("m:group/m:description", "", NS) or "")[:800]})
        checked.append({"channel_id": cid, "name": name, "ok": True, "new": n})
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{today}.json")
    first = path
    k = 2
    while os.path.exists(path):
        path = os.path.join(OUT, f"{today}-{k}.json"); k += 1
    ok = sum(1 for c in checked if c["ok"])
    if os.path.exists(first) and not videos and ok == len(checked):
        return f"YouTube確認: {ok}/{len(checked)}チャンネル、新着0本(今日の記録は{os.path.basename(first)})"
    summary = f"YouTube確認: {ok}/{len(checked)}チャンネル、新着{len(videos)}本"
    failed = [c for c in checked if not c["ok"]]
    if failed:
        summary += "。見られなかった: " + "、".join(f"{c['name']}({c['error']})" for c in failed) + "。翌日また見ます"
    json.dump({"date": today, "days": days, "summary": summary, "checked": checked, "videos": videos},
              open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(SEEN, "a", encoding="utf-8") as f:
        for v in videos:
            f.write(f"{v['id']}|{v['channel']}|{v['published']}|{v['title']}\n")
    try:  # 過去動画(各100本)も一緒に取る。失敗しても毎日の確認は止めない(2026/11/21追加)
        import yt_backfill
        bf = yt_backfill.main(quiet=True)
        summary += " / " + bf
    except Exception as e:  # noqa: BLE001
        summary += f" / 過去動画の取得は失敗({str(e)[:60]})"
    if not quiet:
        print(summary)
        print("記録:", os.path.relpath(path, ROOT))
        for v in videos:
            print(f"- [{v['channel']}] {v['published']} {v['title']} {v['url']}")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    main(ap.parse_args().days)
