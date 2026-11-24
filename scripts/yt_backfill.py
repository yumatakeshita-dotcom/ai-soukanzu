#!/usr/bin/env python3
"""YouTubeチャンネルの過去の動画(各チャンネル最新100本)を取って inbox/youtube/backfill/日付.json に足す(2026/11/21追加)。

公式RSSは直近15本までなので、チャンネルの「アップロード一覧」ページ(公開ページ)から、動画ID・題名・おおよその古さを読む。
説明文は取らない(題名と会社名から手がかりを作り、確かめは別の出典で)。足すだけ。すでに取った動画は飛ばす。
  python3 scripts/yt_backfill.py [--leads]    --leads: 移籍・出資の言葉+会社名がある題名だけ表示
"""
import jst
import argparse, json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
OUT = os.path.join(ROOT, "inbox", "youtube", "backfill")
CH = os.path.join(ROOT, "inbox", "youtube_channels.txt")


def page(cid):
    url = "https://www.youtube.com/playlist?list=UU" + cid[2:]
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})
    for wait in (0, 20, 60):
        time.sleep(wait)
        try:
            return urllib.request.urlopen(req, timeout=40).read().decode("utf-8", "ignore"), ""
        except Exception as e:  # noqa: BLE001
            err = str(e)[:80]
    return None, err


def parse(t):
    m = re.search(r"ytInitialData\s*=\s*(\{.*?\});\s*</script>", t, re.S)
    d = json.loads(m.group(1)); out = []

    def walk(o):
        if isinstance(o, dict):
            if "lockupViewModel" in o:
                l = o["lockupViewModel"]; s = json.dumps(l, ensure_ascii=False)
                title = l.get("metadata", {}).get("lockupMetadataViewModel", {}).get("title", {}).get("content")
                age = re.findall(r'"content": "([^"]*(?:ago|前)[^"]*)"', s)
                if l.get("contentId") and title:
                    out.append({"id": l["contentId"], "title": title, "age": age[0] if age else ""})
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(d)
    return out


def main(leads_only=False, quiet=False):
    os.makedirs(OUT, exist_ok=True)
    seen = set()
    for f in os.listdir(OUT):
        if f.endswith(".json"):
            seen |= {v["id"] for v in json.load(open(os.path.join(OUT, f), encoding="utf-8"))["videos"]}
    new, checked = [], []
    for l in open(CH, encoding="utf-8"):
        if l.startswith("#") or "|" not in l:
            continue
        cid, name = l.split("|")[:2]
        t, err = page(cid)
        if t is None:
            checked.append({"name": name, "ok": False, "error": err}); continue
        try:
            vs = parse(t)
        except Exception as e:  # noqa: BLE001
            checked.append({"name": name, "ok": False, "error": "読めない:" + str(e)[:60]}); continue
        n = 0
        for v in vs:
            if v["id"] not in seen:
                v.update(channel=name, url="https://www.youtube.com/watch?v=" + v["id"]); new.append(v); n += 1
        checked.append({"name": name, "ok": True, "new": n})
    ok = sum(c["ok"] for c in checked)
    summary = f"過去動画の取得: {ok}/{len(checked)}チャンネル、新しく{len(new)}本"
    if new:
        json.dump({"date": jst.strftime("%Y-%m-%d"), "summary": summary, "checked": checked, "videos": new},
                  open(os.path.join(OUT, jst.strftime("%Y-%m-%d-%H%M") + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    bad = [c for c in checked if not c["ok"]]
    if not quiet:
        print(summary)
        for c in bad:
            print("  見られなかった:", c["name"], c["error"])
    if quiet:
        return summary + ("。見られなかった: " + "、".join(c["name"] for c in bad) if bad else "")
    if leads_only:
        import media_digest as m
        for v in new:
            if m.KW.search(v["title"]) and m.CO.search(v["title"]):
                print(f"- [{v['channel']}] ({v['age']}) {v['title'][:120]} {v['url']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--leads", action="store_true")
    main(ap.parse_args().leads)
