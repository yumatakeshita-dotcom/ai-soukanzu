#!/usr/bin/env python3
"""YouTubeを直近15本より深くさかのぼる(2026/11/21追加)。

RSSは最新15本しか返さない。そこで、各チャンネルの「アップロード一覧」(再生リスト UU+チャンネルID)の
公開ページを開いて、直近100本のタイトル・長さ・おおよその投稿時期を読む(ログイン不要の普通の公開ページ)。
説明文は取れない(動画ページはロボット確認で断られるため、ごまかす工夫はしない)。タイトルは「手がかり」で、
出典(記事・公式発表)で確かめてから inbox/moves・money に足す。

  python3 scripts/yt_deep.py                 # 全チャンネル
  python3 scripts/yt_deep.py --only UCxxxx   # 1チャンネルだけ
足すだけ。inbox/youtube/deep/日付.json に保存し、すでにある動画は deep/seen.txt に足す。
"""
import jst
import argparse, json, os, re, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, "inbox", "youtube_channels.txt")
OUT = os.path.join(ROOT, "inbox", "youtube", "deep")
SEEN = os.path.join(OUT, "seen.txt")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"}


def lines(p):
    if not os.path.exists(p):
        return []
    return [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]


def get(cid, waits=(30, 90)):
    url = "https://www.youtube.com/playlist?list=UU" + cid[2:]
    err = ""
    for i in range(len(waits) + 1):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.read().decode("utf-8", "replace"), ""
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"[:150]
            if i < len(waits):
                time.sleep(waits[i])
    return None, err


def parse(html):
    i = html.find("var ytInitialData = ")
    if i < 0:
        return []
    data, _ = json.JSONDecoder().raw_decode(html[i + 20:])
    items = []

    def walk(o):
        if isinstance(o, dict):
            if o.get("contentType") == "LOCKUP_CONTENT_TYPE_VIDEO":
                items.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(data)
    out = []
    for it in items:
        md = it["metadata"]["lockupMetadataViewModel"]
        texts = []

        def contents(o):
            if isinstance(o, dict):
                if isinstance(o.get("content"), str):
                    texts.append(o["content"])
                for v in o.values():
                    contents(v)
            elif isinstance(o, list):
                for v in o:
                    contents(v)
        contents(md.get("metadata", {}))
        age = next((t for t in texts if re.search(r"\bago\b|Streamed|Premiered", t)), "")
        dur = it.get("rendererContext", {}).get("accessibilityContext", {}).get("label", "")
        out.append({"id": it["contentId"], "title": md["title"]["content"], "age": age, "label": dur})
    return out


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    seen = {l.split("|")[0] for l in lines(SEEN)}
    today = jst.strftime("%Y-%m-%d")
    res, checked, new_ids = [], [], []
    for l in lines(CH):
        cid, name, kind = (l.split("|") + ["", ""])[:3]
        if only and cid != only:
            continue
        html, err = get(cid)
        if html is None:
            checked.append({"channel_id": cid, "name": name, "ok": False, "error": err})
            continue
        try:
            vs = parse(html)
        except Exception as e:  # noqa: BLE001
            checked.append({"channel_id": cid, "name": name, "ok": False, "error": f"parse: {e}"[:150]})
            continue
        n = 0
        for v in vs:
            if v["id"] in seen:
                continue
            v.update({"channel": name, "channel_id": cid, "kind": kind, "url": "https://www.youtube.com/watch?v=" + v["id"]})
            res.append(v); new_ids.append(v["id"]); n += 1
        checked.append({"channel_id": cid, "name": name, "ok": True, "listed": len(vs), "new": n})
        time.sleep(1.5)
    path = os.path.join(OUT, f"{today}.json"); k = 2
    while os.path.exists(path):
        path = os.path.join(OUT, f"{today}-{k}.json"); k += 1
    ok = sum(1 for c in checked if c["ok"])
    summary = f"YouTube深掘り: {ok}/{len(checked)}チャンネル、過去分の新しい動画{len(res)}本(各100本まで)"
    json.dump({"date": today, "summary": summary, "checked": checked, "videos": res}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(SEEN, "a", encoding="utf-8") as f:
        for i in new_ids:
            f.write(i + "|" + today + "\n")
    print(summary)
    for c in checked:
        if not c["ok"]:
            print("  見られなかった:", c["name"], c["error"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    main(ap.parse_args().only)
