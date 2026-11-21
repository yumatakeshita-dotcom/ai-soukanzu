#!/usr/bin/env python3
"""毎日のポッドキャスト確認(2026/11/21追加)。inbox/podcast_feeds.txt の公開RSSを見て、新着エピソードを記録する。

YouTube確認(yt_daily.py)と同じ形。タイトル・説明文・公開日だけを使い、音声の文字起こしはしない。
  python3 scripts/pod_daily.py            # 直近7日 → inbox/podcasts/日付.json に足す
  python3 scripts/pod_daily.py --days 14
見られない番組(ホストが許可されていない・断られた)は理由つきで記録し、翌日また見る。足すだけ。
"""
import argparse, datetime, email.utils, html, json, os, re, time, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = os.path.join(ROOT, "inbox", "podcast_feeds.txt")
OUT = os.path.join(ROOT, "inbox", "podcasts")
SEEN = os.path.join(OUT, "seen.txt")
IT = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"


def lines(p):
    if not os.path.exists(p):
        return []
    return [l.rstrip("\n") for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]


def fetch(url, waits=(20, 60)):
    err = ""
    for i in range(len(waits) + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (podcast feed reader)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return ET.fromstring(r.read()), ""
        except Exception as e:  # noqa: BLE001
            err = f"{type(e).__name__}: {e}"[:120]
            if "403" in err:
                err = "接続を断られた(環境のネットワーク許可に " + url.split("/")[2] + " が無い)"
            if i < len(waits) and "403" not in err:
                time.sleep(waits[i])
            else:
                break
    return None, err


def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def main(days=7, quiet=False):
    seen = {l.split("|")[0] for l in lines(SEEN)}
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    today = time.strftime("%Y-%m-%d")
    checked, eps = [], []
    for l in lines(FEEDS):
        url, name, kind, lang = (l.split("|") + ["", "", "", ""])[:4]
        root, err = fetch(url)
        if root is None:
            checked.append({"name": name, "ok": False, "error": err})
            continue
        n = 0
        for it in root.iter("item"):
            guid = it.findtext("guid") or it.findtext("link") or it.findtext("title") or ""
            try:
                dt = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
            except Exception:  # noqa: BLE001
                continue
            if dt < cutoff or guid in seen:
                continue
            n += 1
            desc = clean(it.findtext("description") or it.findtext(IT + "summary") or "")[:800]
            eps.append({"id": guid, "show": name, "kind": kind, "lang": lang, "title": clean(it.findtext("title")),
                        "published": dt.strftime("%Y-%m-%d"), "url": it.findtext("link") or "", "description": desc})
        checked.append({"name": name, "ok": True, "new": n})
    os.makedirs(OUT, exist_ok=True)
    first = os.path.join(OUT, f"{today}.json")
    path, k = first, 2
    while os.path.exists(path):
        path = os.path.join(OUT, f"{today}-{k}.json"); k += 1
    ok = sum(1 for c in checked if c["ok"])
    summary = f"ポッドキャスト確認: {ok}/{len(checked)}番組、新着{len(eps)}本"
    if os.path.exists(first) and not eps:
        return summary + "(今日の記録は" + os.path.basename(first) + ")"
    bad = [c for c in checked if not c["ok"]]
    if bad:
        summary += "。見られなかった: " + "、".join(f"{c['name']}({c['error']})" for c in bad) + "。翌日また見ます"
    json.dump({"date": today, "days": days, "summary": summary, "checked": checked, "episodes": eps},
              open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(SEEN, "a", encoding="utf-8") as f:
        for e in eps:
            f.write(f"{e['id']}|{e['show']}|{e['published']}|{e['title'][:100]}\n")
    if not quiet:
        print(summary)
        for e in eps:
            print(f"- [{e['show']}] {e['published']} {e['title']}")
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=7)
    main(ap.parse_args().days)
