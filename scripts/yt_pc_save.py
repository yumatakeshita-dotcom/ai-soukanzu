#!/usr/bin/env python3
"""PCのブラウザで読んだ文字起こしから、手がかりの抜粋だけを inbox/youtube/transcripts/ に保存する(2026/11/23追加)。

使い方(PCのClaudeが、ブラウザで読んだ文字起こしを一時ファイルに書いてから):
  python3 scripts/yt_pc_save.py 動画ID --title "題名" --channel "チャンネル名" --date 2026-11-23 --file /tmp/x.txt
  (--file を省くと標準入力から読む。1行=1発言。先頭に「0:12 」のような時刻があってもよい)

保存するのは全文ではなく、移籍・出資などの言葉(media_digest.KW)がある行とその前後1行だけ(最大80行)。
全文は保存しない。抜粋は手がかりで、報道・公式で確かめてから inbox/money・moves に足す。
保存したら、クラウド側の再取得の順番待ち(yt_retry.txt)の同じ動画は yt_retry_done.txt に足す(足すだけ)。
"""
import argparse, datetime, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import media_digest as m

TR = os.path.join(ROOT, "inbox", "youtube", "transcripts")


def excerpt(lines, maxn=80):
    keep = set()
    for i, ln in enumerate(lines):
        if m.KW.search(ln) or m.CO.search(ln) and re.search(r"\$|億|million|billion", ln):
            keep.update({max(0, i - 1), i, min(len(lines) - 1, i + 1)})
    return [lines[i] for i in sorted(keep)][:maxn]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--title", default="")
    ap.add_argument("--channel", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--file", default="")
    a = ap.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", a.id):
        sys.exit("動画IDは11文字です")
    raw = open(a.file, encoding="utf-8").read() if a.file else sys.stdin.read()
    lines = [re.sub(r"\s+", " ", x).strip() for x in raw.splitlines() if x.strip()]
    ex = excerpt(lines)
    os.makedirs(TR, exist_ok=True)
    path = os.path.join(TR, a.id + ".md")
    if os.path.exists(path):
        sys.exit(f"すでにあります(上書きしません): {path}")
    head = (f"# {a.title or a.id}\n\n- 動画: https://www.youtube.com/watch?v={a.id}\n- チャンネル: {a.channel}\n"
            f"- 動画の日付: {a.date}\n- 取った日: {datetime.date.today()}(PCのブラウザの文字起こし。全{len(lines)}行から抜粋{len(ex)}行)\n"
            f"- 注意: 手がかり。報道・公式で確かめてから inbox に足す\n\n")
    open(path, "w", encoding="utf-8").write(head + "\n".join("- " + x for x in ex) + "\n")
    for k in ("money", "moves"):
        q = os.path.join(ROOT, "inbox", k, "yt_retry.txt")
        if os.path.exists(q) and a.id in open(q, encoding="utf-8").read():
            open(os.path.join(ROOT, "inbox", k, "yt_retry_done.txt"), "a", encoding="utf-8").write(a.id + "\n")
    print(f"保存: {path}(抜粋{len(ex)}行)")
