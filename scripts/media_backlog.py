#!/usr/bin/env python3
"""過去の動画・ポッドキャストの手がかりを、少しずつ確かめるための未確認リスト(2026/11/21追加)。

inbox/youtube/ と inbox/podcasts/ の全期間から、移籍・出資の強い言葉と会社名があるものを拾い、
inbox/backlog/queue.json に「足すだけ」で記録する。状態は todo / done(入れた) / checked(確かめたが入れない) / unverified(確かめられない・理由つき)。
  python3 scripts/media_backlog.py sync            # 新しい手がかりをリストに足す(既存の状態は変えない)
  python3 scripts/media_backlog.py next [-n 8]     # 次に確かめるもの(todo、強い順)
  python3 scripts/media_backlog.py mark ID 状態 "理由やメモ"
  python3 scripts/media_backlog.py status          # 進み具合(inbox/backlog/README.md も更新)
"""
import argparse, glob, hashlib, json, os, re, sys, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = os.path.join(ROOT, "inbox", "backlog", "queue.json")
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import media_digest as md

STRONG = re.compile(r"\b(hires?|hired|poach\w*|leaves?|left|steps? down|resign\w*|appoint\w*|named ceo|raises?|raised|"
                    r"funding|valuation|acquir\w*|acquisition|buys?|bought|series [a-f])\b|移籍|入社|退社|退任|就任|引き抜き|出資|調達|買収", re.I)
WEAK_ONLY_CO = {"Jensen", "Altman", "Amodei", "Musk", "Zuckerberg", "Hassabis"}


JOIN = re.compile(r"\b(?:joins?|joined)\s+(?:the\s+)?(?:" + md.CO.pattern.split("(?:",1)[1].rsplit(")",1)[0] + r")", re.I)
RECENT_DAYS = 3  # 直近は毎日の手がかりのまとめ(media_digest)が見るので、ここでは過去分だけ


def vid(url, title):
    return hashlib.sha1((url or title).encode()).hexdigest()[:10]


def load():
    return json.load(open(Q, encoding="utf-8")) if os.path.exists(Q) else {"items": {}}


def save(q):
    os.makedirs(os.path.dirname(Q), exist_ok=True)
    json.dump(q, open(Q, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)


AGE = re.compile(r"(\d+)\s*(h|d|w|mo|y)\b")
STOP = set("the and for with why how what who this that from into your you are was will new now all but not can has have its our out one two ceo ai vs inc llc interview episode podcast live show part week monday tuesday wednesday thursday friday saturday sunday january february march april may june july august september october november december".split())
_corpus = []


def approx_date(age):
    """YouTubeの『3mo ago』のようなおおよその古さから、おおよその日付(年月日)を作る(2026/11/21追加)。"""
    m = AGE.search(age or "")
    if not m:
        return datetime.date.today().isoformat()
    n, u = int(m.group(1)), m.group(2)
    days = {"h": 0, "d": n, "w": 7 * n, "mo": 30 * n, "y": 365 * n}[u]
    return (datetime.date.today() - datetime.timedelta(days=days)).isoformat()


def corpus():
    if not _corpus:
        t = ""
        for f in glob.glob(os.path.join(ROOT, "site", "data", "*.js")) + [os.path.join(ROOT, "site", "index.html")]:
            t += open(f, encoding="utf-8", errors="ignore").read().lower()
        _corpus.append(t)
    return _corpus[0]


def new_names(title):
    """題名の中の英字の固有名詞のうち、相関図のデータに1回も出てこないもの(新しい会社・人の可能性)。"""
    c = corpus()
    out = []
    for w in re.findall(r"\b[A-Z][A-Za-z0-9]{2,}\b", title):
        if w.lower() not in STOP and w.lower() not in c and w not in out:
            out.append(w)
    return out[:4]


def sync():
    q = load(); new = 0
    files = sorted(glob.glob(os.path.join(ROOT, "inbox", "youtube", "2*.json")) + glob.glob(os.path.join(ROOT, "inbox", "podcasts", "2*.json")) +
                   glob.glob(os.path.join(ROOT, "inbox", "youtube", "backfill", "2*.json")))
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        for v in d.get("videos", []) + d.get("episodes", []):
            if "published" not in v:  # 過去動画の一覧は古さだけ(説明文なし)
                v["published"] = approx_date(v.get("age"))
            text = v["title"] + " " + v.get("description", "")
            if v["published"] >= (datetime.date.today() - datetime.timedelta(days=RECENT_DAYS)).isoformat():
                continue
            strong = sorted({m.group(0).lower() for m in STRONG.finditer(text)} | {m.group(0).lower() for m in JOIN.finditer(text)})
            cos = sorted({m.group(0) for m in md.CO.finditer(text)})
            if not strong or not (set(cos) - WEAK_ONLY_CO):
                continue
            i = vid(v.get("url", ""), v["title"])
            if i in q["items"]:
                continue
            q["items"][i] = {"id": i, "published": v["published"], "source": v.get("channel") or v.get("show"), "title": v["title"],
                             "url": v.get("url", ""), "words": strong[:6], "companies": cos[:6],
                             "desc": re.sub(r"\s+", " ", v.get("description", ""))[:400], "status": "todo", "note": "",
                             "newnames": new_names(v["title"])}
            new += 1
    save(q); print(f"新しく足した手がかり: {new}件(合計{len(q['items'])})")


def todo(n):
    its = [x for x in load()["items"].values() if x["status"] == "todo"]
    # 相関図にまだ無い名前が題名にあるものは少しだけ先に(ゲスト名なども拾うので、ごく軽い加点)
    its.sort(key=lambda x: (-len(x["words"]) - len(x["companies"]) - (1 if x.get("newnames") else 0), x["published"]), reverse=False)
    return its[:n]


def status():
    q = load(); c = {}
    for x in q["items"].values():
        c[x["status"]] = c.get(x["status"], 0) + 1
    line = " / ".join(f"{k} {v}" for k, v in sorted(c.items()))
    print("未確認リスト:", line)
    with open(os.path.join(ROOT, "inbox", "backlog", "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# 過去の動画・番組の手がかり 確認の進み具合\n\n更新: {datetime.date.today()}\n\n{line}\n\n"
                "- todo=まだ確かめていない / done=確かめて inbox/moves・money に入れた / checked=確かめたが入れない / unverified=確かめられない(理由つき)\n"
                "- リスト: `inbox/backlog/queue.json`(足すだけ)。道具: `scripts/media_backlog.py`\n\n## 確かめられなかったもの(理由つき)\n\n")
        for x in sorted(q["items"].values(), key=lambda x: x["published"], reverse=True):
            if x["status"] == "unverified":
                f.write(f"- {x['published']} {x['source']}「{x['title'][:70]}」: {x['note']}\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); s = ap.add_subparsers(dest="cmd")
    s.add_parser("sync"); n = s.add_parser("next"); n.add_argument("-n", type=int, default=8); s.add_parser("status")
    m = s.add_parser("mark"); m.add_argument("id"); m.add_argument("state", choices=["done", "checked", "unverified", "todo"]); m.add_argument("note", nargs="?", default="")
    a = ap.parse_args()
    if a.cmd == "sync": sync()
    elif a.cmd == "next":
        for x in todo(a.n): print(json.dumps(x, ensure_ascii=False))
    elif a.cmd == "mark":
        q = load(); q["items"][a.id]["status"] = a.state; q["items"][a.id]["note"] = a.note; save(q)
    else: status()

