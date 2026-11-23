#!/usr/bin/env python3
"""過去の動画・ポッドキャストの手がかりを、少しずつ確かめるための未確認リスト(2026/11/21追加)。

inbox/youtube/ と inbox/podcasts/ の全期間から、移籍・出資の強い言葉と会社名があるものを拾い、
inbox/backlog/queue.json に「足すだけ」で記録する。状態は todo / done(入れた) / checked(確かめたが入れない) / unverified(確かめられない・理由つき)。
  python3 scripts/media_backlog.py sync            # 新しい手がかりをリストに足す(既存の状態は変えない)
  python3 scripts/media_backlog.py prune           # すでにある todo のうち外れの条件に当てはまるものを checked に(消さない)
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


JOIN = md.JOINROLE  # 「joins ... as」の形だけ。出演の意味の joins は数えない(2026/11/21)
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


GENERIC_WORDS = {"buy", "leave", "left", "join"}  # 普通の動詞の原形だけ。「buys」「leaves」などの取引の形とは分ける


def noise_reason(title, words, newnames):
    """リストの段階で除く外れ(2026/11/22追加)。理由を返す。当てはまらなければ None。
    確かめて外れた残りの29件の理由(直近20件は別ルール、既出9件)を集計して決めた。"""
    ws = set(words)
    if re.search(r"exodus|shake-?up|depart|exits?\b|quit|poach|hires?\b|resign|steps? down|ousted|fired", title, re.I):
        return None  # 人の動きを思わせる題名は残す
    # 普通の動詞は説明文にあるだけ(題名にない)なら外れ。題名にあるもの(「Join OpenAI」など)は残す
    if ws and ws <= GENERIC_WORDS and not any(re.search(r"\b" + w + r"\b", title, re.I) for w in ws) and not md.join_move(title):
        return "普通の動詞(buy・leave・left・join)が説明文にあるだけで、題名に移籍・出資の言葉なし"
    if (title.startswith("20VC:") or title.count(" | ") >= 2) and " | " in title and not newnames:
        return "複数の話題のまとめ回で、題名の名前はすべて相関図にすでにある(新しい名前なし)"
    return None


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
            strong = sorted({m.group(0).lower() for m in STRONG.finditer(text)} | ({"joins(役職)"} if md.join_move(v["title"], v.get("description", "")) else set()))
            cos = sorted({m.group(0) for m in md.CO.finditer(text)})
            if not strong or not (set(cos) - WEAK_ONLY_CO):
                continue
            i = vid(v.get("url", ""), v["title"])
            if i in q["items"]:
                continue
            if noise_reason(v["title"], strong, new_names(v["title"])):
                continue  # 外れのもとは足さない(2026/11/22)
            q["items"][i] = {"id": i, "published": v["published"], "source": v.get("channel") or v.get("show"), "title": v["title"],
                             "url": v.get("url", ""), "words": strong[:6], "companies": cos[:6],
                             "desc": re.sub(r"\s+", " ", v.get("description", ""))[:400], "status": "todo", "note": "",
                             "newnames": new_names(v["title"])}
            new += 1
    save(q); print(f"新しく足した手がかり: {new}件(合計{len(q['items'])})")


def prune():
    """すでにリストにある todo のうち、外れの条件に当てはまるものを checked にして理由を書く(消さない)。"""
    q = load(); n = 0
    for x in q["items"].values():
        if x["status"] != "todo":
            continue
        r = noise_reason(x["title"], x["words"], x.get("newnames", new_names(x["title"])))
        if r:
            x["status"] = "checked"; x["note"] = "自動で除外(" + r + "。2026/11/22の絞り込み)"; n += 1
    save(q); print(f"外れとして checked にした: {n}件")


def todo(n):
    its = [x for x in load()["items"].values() if x["status"] == "todo"]
    # 相関図にまだ無い名前が題名にあるものは少しだけ先に(ゲスト名なども拾うので、ごく軽い加点)
    its.sort(key=lambda x: (-len(x["words"]) - len(x["companies"]) - (1 if x.get("newnames") else 0), x["published"]), reverse=False)
    return its[:n]


# 画面の部品(ホームと調査エージェント一覧が同じものを呼ぶ)。色はCSS変数だけ使う
PROG_FN = r"""function backlogBox(){
  const h=typeof BACKLOG_PROG!=='undefined'?BACKLOG_PROG:[];if(!h.length)return '';
  const e=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const L=h[h.length-1],P=h.length>1?h[h.length-2]:null,tot=L.todo+L.done+L.checked+L.unverified;
  const U=typeof BACKLOG_UNV!=='undefined'?BACKLOG_UNV:[];
  const md=d=>d.slice(5).replace('-','/');
  const dt=P?`${md(P.d)}→${md(L.d)}で確かめ済みが ${(L.done+L.checked+L.unverified)-(P.done+P.checked+P.unverified)} 件増えた(入れた +${L.done-P.done}・入れなかった +${L.checked-P.checked}・確かめられず +${L.unverified-P.unverified})`:'';
  const rows=h.slice(-7).reverse().map(r=>{const t=r.todo+r.done+r.checked+r.unverified;return `<tr><td>${md(r.d)}</td><td style="text-align:right">${r.todo}</td><td style="width:45%"><div style="background:var(--line);border-radius:4px;height:8px"><div style="background:var(--accent,var(--active,#4a5dd0));width:${t?Math.round(100*(t-r.todo)/t):0}%;height:8px;border-radius:4px"></div></div></td><td style="text-align:right">${r.done}</td></tr>`}).join('');
  return `<div style="border:1px solid var(--line);border-radius:12px;padding:14px 16px;background:var(--surface);overflow-wrap:anywhere"><b>確かめ係の進み具合</b>
  <p style="margin:6px 0;font-size:14px">過去の動画・番組の手がかり ${tot}件のうち、まだ確かめていないのは <b>${L.todo}件</b>(${e(md(L.d))} 時点)。毎日10:07に10件ほどずつ確かめています。</p>
  ${dt?`<p style="margin:0 0 8px;font-size:13px;color:var(--muted)">${e(dt)}</p>`:''}
  <div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:13px"><tr style="color:var(--muted)"><th style="text-align:left;font-weight:600">日付</th><th style="text-align:right;font-weight:600">残り</th><th style="font-weight:600">確かめ済みの割合</th><th style="text-align:right;font-weight:600">入れた累計</th></tr>${rows}</table></div>
  <details style="margin-top:8px;font-size:13px"><summary style="cursor:pointer">確かめられなかったもの(${U.length}件)</summary>${U.length?`<ul style="margin:6px 0 0;padding-left:1.2em">${U.map(x=>`<li>${e(x.d)} ${e(x.s)}「${x.u&&/^https?:/.test(x.u)?`<a href="${e(x.u)}" target="_blank" rel="noopener">${e(x.t)}</a>`:e(x.t)}」: ${e(x.n||'理由の記録なし')}</li>`).join('')}</ul>`:'<p style="margin:6px 0 0;color:var(--muted)">いまはありません。確かめられなかったものは、理由つきでここに並びます。</p>'}</details>
  <p style="margin:8px 0 0;font-size:12px;color:var(--muted)">「入れなかった」は、確かめて相関図に足さなかったもの(動きではない・すでにある・外れ)です。記録は inbox/backlog/history.json。</p></div>`;
}
"""

HIST = os.path.join(ROOT, "inbox", "backlog", "history.json")
PROG_JS = os.path.join(ROOT, "site", "data", "backlog.js")


def record_history(c, day=None, items=()):
    """日ごとの件数を inbox/backlog/history.json に足す(同じ日は置き換え。前の日は消さない)。
    画面(ホーム・調査エージェント一覧)用に site/data/backlog.js も書き出す(2026/11/22追加)。"""
    day = day or datetime.date.today().isoformat()
    h = json.load(open(HIST, encoding="utf-8")) if os.path.exists(HIST) else []
    row = {"d": day, **{k: c.get(k, 0) for k in ("todo", "done", "checked", "unverified")}}
    h = [r for r in h if r["d"] != day] + [row]
    h.sort(key=lambda r: r["d"])
    json.dump(h, open(HIST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    unv = [{"d": x["published"], "s": x["source"], "t": x["title"][:80], "n": x.get("note", ""), "u": x.get("url", "")}
           for x in sorted(items, key=lambda x: x["published"], reverse=True) if x["status"] == "unverified"]
    os.makedirs(os.path.dirname(PROG_JS), exist_ok=True)
    with open(PROG_JS, "w", encoding="utf-8") as f:
        f.write("/* 確かめ係(過去の動画・番組の手がかり)の進み具合。scripts/media_backlog.py status が書く。手で直さない */\n"
                "const BACKLOG_PROG=" + json.dumps(h, ensure_ascii=False, separators=(",", ":")) + ";\n"
                "const BACKLOG_UNV=" + json.dumps(unv, ensure_ascii=False, separators=(",", ":")) + ";\n" + PROG_FN)


def status():
    q = load(); c = {}
    for x in q["items"].values():
        c[x["status"]] = c.get(x["status"], 0) + 1
    record_history(c, items=q["items"].values())
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
    s.add_parser("sync"); s.add_parser("prune"); n = s.add_parser("next"); n.add_argument("-n", type=int, default=8); s.add_parser("status")
    m = s.add_parser("mark"); m.add_argument("id"); m.add_argument("state", choices=["done", "checked", "unverified", "todo"]); m.add_argument("note", nargs="?", default="")
    a = ap.parse_args()
    if a.cmd == "sync": sync()
    elif a.cmd == "prune": prune()
    elif a.cmd == "next":
        for x in todo(a.n): print(json.dumps(x, ensure_ascii=False))
    elif a.cmd == "mark":
        q = load(); q["items"][a.id]["status"] = a.state; q["items"][a.id]["note"] = a.note; save(q)
    else: status()

