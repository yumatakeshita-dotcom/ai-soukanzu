#!/usr/bin/env python3
"""PCのブラウザで文字起こしを読む動画の「順番待ち」を作る(2026/11/23追加)。

クラウドからはYouTubeの字幕がロボット確認で断られるので、字幕はPC側で読む。
この道具は「どの動画をPCで読むか」を決めるだけ(YouTubeには接続しない)。

使い方:
  python3 scripts/yt_pc_queue.py [--max 8]   # 読む動画の一覧を表示し、inbox/youtube/pc_queue.json に書く
  python3 scripts/yt_pc_queue.py --list-done # すでに文字起こしを取った動画

選び方(上から):
  1. inbox/money/yt_retry.txt・inbox/moves/yt_retry.txt に残っている(クラウドで字幕が取れなかった)動画
  2. 過去動画の一覧(inbox/youtube/backfill・deep)と毎日の新着(inbox/youtube/日付.json)のうち、
     題名に 移籍・出資などの言葉 と 会社名 が両方ある動画
  すでに inbox/youtube/transcripts/ に抜粋がある動画は飛ばす。足すだけ。何度動かしても同じ。
"""
import argparse, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TR = os.path.join(ROOT, "inbox", "youtube", "transcripts")
OUT = os.path.join(ROOT, "inbox", "youtube", "pc_queue.json")


def done_ids():
    return {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(TR, "*.md"))}


def retry_ids():
    ids = []
    for k in ("money", "moves"):
        p = os.path.join(ROOT, "inbox", k, "yt_retry.txt")
        if os.path.exists(p):
            for ln in open(p, encoding="utf-8"):
                m = re.match(r"\s*([A-Za-z0-9_-]{11})\b", ln)
                if m:
                    ids.append(m.group(1))
    return ids


def all_videos():
    vs = {}
    for pat in ("backfill/*.json", "deep/*.json", "*.json"):
        for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "youtube", pat))):
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            for v in (d.get("videos") if isinstance(d, dict) else d) or []:
                if isinstance(v, dict) and v.get("id"):
                    vs.setdefault(v["id"], v)
    return vs


def build(maxn):
    import media_digest as m
    done = done_ids()
    vs = all_videos()
    out, seen = [], set()
    for vid in retry_ids():
        if vid not in done and vid not in seen:
            v = vs.get(vid, {"id": vid})
            out.append({"id": vid, "title": v.get("title", ""), "channel": v.get("channel", ""),
                        "url": f"https://www.youtube.com/watch?v={vid}", "why": "クラウドで字幕が取れなかった"})
            seen.add(vid)
    for vid, v in vs.items():
        t = v.get("title", "")
        if vid in done or vid in seen:
            continue
        if m.KW.search(t) and m.CO.search(t):
            out.append({"id": vid, "title": t, "channel": v.get("channel", ""),
                        "url": f"https://www.youtube.com/watch?v={vid}", "why": "題名に移籍・出資の言葉と会社名"})
            seen.add(vid)
    return out[:maxn], len(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--list-done", action="store_true")
    a = ap.parse_args()
    if a.list_done:
        print("\n".join(sorted(done_ids())) or "(まだなし)")
        sys.exit(0)
    q, total = build(a.max)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(q, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"PCで読む動画: {len(q)}本(候補は全部で{total}本)")
    for v in q:
        print(f"- {v['id']} [{v['channel']}] {v['title'][:100]} ({v['why']})\n  {v['url']}")
