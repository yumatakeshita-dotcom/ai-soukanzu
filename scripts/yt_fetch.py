#!/usr/bin/env python3
"""YouTubeの動画の説明文と字幕を、断られたら時間をおいてやり直しながら取る道具(2026/11/19追加)。

お金の流れ・引き抜きの調査タスクで使う。

使い方:
  python3 scripts/yt_fetch.py ID [ID ...]            # 動画ごとに説明文と字幕を取る
  python3 scripts/yt_fetch.py --retry-queue          # 前回までに取れなかった動画をやり直す
  python3 scripts/yt_fetch.py --waits 60,180,600 ID  # 待つ秒数を変える(初期値 60,180,600)
  python3 scripts/yt_fetch.py --channel ID --title T ID  # 取れなかったときの記録用の情報
  python3 scripts/yt_fetch.py --kind moves ID        # 記録先を inbox/moves/ にする(初期値は money)

結果:
  - 画面に JSON(id, ok, description, transcript, tries, error, desc_source)を出す
  - 字幕のテキストは --out のフォルダ(初期値はスクラッチ用の /tmp/yt)に <ID>.txt で保存
  - 最後まで取れなかった動画は inbox/<種類>/yt_retry.txt に足す(足すだけ)。
    次の回は --retry-queue で先にやり直す。取れたら inbox/<種類>/yt_retry_done.txt に足す

やり方:
  1. yt-dlp の普通の取り方で説明文と英語の字幕を取る
  2. 混雑(429)やロボット確認で断られたら、--waits の秒数だけ待って同じ取り方でやり直す
  3. それでもだめなら、説明文だけはチャンネルの公式RSSから取る(最新15本まで)
  ※ 断られ方をごまかす工夫(取り方の切り替え・偽装)はしない。待ってやり直すだけ。
"""
import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "inbox", "money", "yt_retry.txt")
DONE = os.path.join(ROOT, "inbox", "money", "yt_retry_done.txt")
BUSY = ("429", "Too Many Requests", "not a bot", "Sign in to confirm", "sorry", "rate-limit")


def run_ytdlp(vid, out):
    url = f"https://www.youtube.com/watch?v={vid}"
    cmd = ["yt-dlp", "--skip-download", "--write-info-json", "--write-subs", "--write-auto-subs",
           "--sub-langs", "en.*,ja.*", "--sub-format", "json3", "--no-progress",
           "-o", os.path.join(out, "%(id)s"), url]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    return p.returncode, (p.stderr or "") + (p.stdout or "")


def json3_text(path):
    d = json.load(open(path, encoding="utf-8"))
    parts = []
    for ev in d.get("events", []):
        for s in ev.get("segs", []) or []:
            parts.append(s.get("utf8", ""))
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def rss_description(vid, channel_id):
    if not channel_id:
        return ""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            root = ET.fromstring(r.read())
    except Exception:  # noqa: BLE001
        return ""
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "media": "http://search.yahoo.com/mrss/"}
    for e in root.findall("a:entry", ns):
        if e.findtext("yt:videoId", "", ns) == vid:
            return e.findtext("media:group/media:description", "", ns)
    return ""


def fetch(vid, out, waits, channel_id=""):
    res = {"id": vid, "ok": False, "description": "", "transcript": "", "tries": 0,
           "error": "", "desc_source": ""}
    for i in range(len(waits) + 1):
        res["tries"] = i + 1
        code, log = run_ytdlp(vid, out)
        info = os.path.join(out, f"{vid}.info.json")
        if os.path.exists(info):
            d = json.load(open(info, encoding="utf-8"))
            res["description"] = d.get("description", "")
            res["desc_source"] = "yt-dlp"
            res["title"] = d.get("title", "")
            res["upload_date"] = d.get("upload_date", "")
            channel_id = channel_id or d.get("channel_id", "")
            subs = sorted(glob.glob(os.path.join(out, f"{vid}.*.json3")),
                          key=lambda p: (".en." not in p and ".en-" not in p, p))
            if subs:
                res["transcript"] = json3_text(subs[0])
                with open(os.path.join(out, f"{vid}.txt"), "w", encoding="utf-8") as f:
                    f.write(res["transcript"])
            res["ok"] = bool(res["transcript"])
            if res["ok"] or not any(b in log for b in BUSY):
                break  # 取れた、または字幕がもともと無い
        last = [l for l in log.splitlines() if "ERROR" in l]
        res["error"] = (last[-1] if last else log.strip()[-300:])[:300]
        if not any(b in log for b in BUSY) and code != 0 and "Unable to download" not in log:
            break  # 混雑以外の失敗(非公開など)は待っても同じ
        if i < len(waits):
            print(f"[{vid}] 断られました。{waits[i]}秒待ってやり直します({i + 1}/{len(waits)})",
                  file=sys.stderr)
            time.sleep(waits[i])
    if not res["description"]:
        res["description"] = rss_description(vid, channel_id)
        res["desc_source"] = "rss" if res["description"] else ""
    return res


def read_lines(path):
    if not os.path.exists(path):
        return []
    return [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]


def append(path, line):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as f:
        if new and path == QUEUE:
            f.write("# 字幕が取れなかった動画(yt_fetch.py が足す)。ID|チャンネルID|日付|タイトル|理由|記録した日\n")
        if new and path == DONE:
            f.write("# yt_retry.txt のうち、あとで取れた動画。ID|取れた日\n")
        f.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--retry-queue", action="store_true")
    ap.add_argument("--waits", default="60,180,600")
    ap.add_argument("--out", default="/tmp/yt")
    ap.add_argument("--channel", default="")
    ap.add_argument("--title", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--gap", type=int, default=10, help="動画の間に空ける秒数")
    ap.add_argument("--kind", default="money", help="記録先の inbox/ のフォルダ(money, moves など)")
    ap.add_argument("--no-daily", action="store_true", help="--retry-queue のときの毎日のチャンネル確認(yt_daily.py)を止める")
    ap.add_argument("--no-queue", action="store_true", help="取れなくても yt_retry.txt に足さない")
    a = ap.parse_args()
    global QUEUE, DONE
    QUEUE = os.path.join(ROOT, "inbox", a.kind, "yt_retry.txt")
    DONE = os.path.join(ROOT, "inbox", a.kind, "yt_retry_done.txt")
    waits = [int(x) for x in a.waits.split(",") if x.strip()]
    os.makedirs(a.out, exist_ok=True)
    today = time.strftime("%Y-%m-%d")

    if a.retry_queue and not a.no_daily:
        # 2026/11/21: 毎日のYouTube確認を必ず通す(登録済みチャンネルの新着を公式RSSで見る)。
        # 調査タスクは今までどおり --retry-queue を呼ぶだけで、ここで一緒に動く
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import yt_daily
        print("[yt_daily] " + yt_daily.main(quiet=True) + "(新着は inbox/youtube/ の今日のJSONを見る。"
              "調査の notes にこの1行を書く)", file=sys.stderr)
        # ポッドキャストも同じ回で確認し、動画・番組の新着から移籍・出資の手がかりをまとめる(2026/11/21追加)
        import pod_daily, media_digest
        print("[pod_daily] " + pod_daily.main(quiet=True), file=sys.stderr)
        print("[media_digest] " + media_digest.main() + "(inbox/media/ の今日の.mdを見て、出典を開いて確かめてから候補にする)", file=sys.stderr)

    jobs = [(v, a.channel, a.date, a.title) for v in a.ids]
    if a.retry_queue:
        done = {l.split("|")[0] for l in read_lines(DONE)}
        seen = set()
        for l in read_lines(QUEUE):
            p = (l.split("|") + [""] * 4)[:4]
            if p[0] not in done and p[0] not in seen:
                seen.add(p[0])
                jobs.append(tuple(p))
    queued = {l.split("|")[0] for l in read_lines(QUEUE)}

    out = []
    for n, (vid, ch, date, title) in enumerate(jobs):
        if n:
            time.sleep(a.gap)
        r = fetch(vid, a.out, waits, ch)
        out.append(r)
        if r["ok"] and vid in queued:
            append(DONE, f"{vid}|{today}")
        elif not r["ok"] and vid not in queued and not a.no_queue and r["error"]:
            append(QUEUE, f"{vid}|{ch}|{date or r.get('upload_date', '')}|{title or r.get('title', '')}|"
                          f"{r['error'][:80].replace('|', '/')}|{today}")
            queued.add(vid)
    for r in out:
        r["transcript_chars"] = len(r["transcript"])
        r["transcript"] = r["transcript"][:2000]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
