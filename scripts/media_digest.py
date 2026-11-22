#!/usr/bin/env python3
"""動画・ポッドキャストの新着から、移籍・出資・買収・取引の「手がかり」を毎朝まとめる(2026/11/21追加)。

inbox/youtube/ と inbox/podcasts/ の直近の記録を読み、タイトル・説明文に動きを表す言葉と会社名があるものを
inbox/media/日付.md と 日付.json に足す。これは候補の手がかりで、相関図には自動で入らない。
確かめる人(Claude)が、出典を開いて名前・日付・数字を確かめてから inbox/moves・money に足す。
  python3 scripts/media_digest.py [--days 3]
"""
import argparse, datetime, glob, json, os, re, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 「○○ joins the show」(出演・参加)は移籍ではないので、joins/joined は「joins ... as/to lead」の形のときだけ数える(2026/11/21。過去の確かめで外れの9割が出演の意味だった)
KW = re.compile(r"\b(hires?|hired|poach\w*|leaves?|left|steps? down|resign\w*|appoint\w*|named ceo|"
                r"raises?|raised|funding|valuation|invest\w*|acquir\w*|acquisition|buys?|bought|ipo|deal|partnership|"
                r"compute|data ?center|series [a-f])\b|移籍|入社|退社|退任|就任|引き抜き|出資|調達|買収|提携|上場", re.I)
CO = re.compile(r"\b(?:OpenAI|Anthropic|xAI|SpaceX|Nvidia|NVIDIA|Jensen|Meta|Google|DeepMind|Microsoft|Apple|Amazon|AWS|Mistral|"
                r"Perplexity|Cursor|Anysphere|Thinking Machines|Safe Superintelligence|SSI|TSMC|Samsung|SK hynix|SoftBank|"
                r"ソフトバンク|Sakana|Preferred Networks|Replit|Scale AI|Databricks|Stripe|Intel|AMD|Broadcom|Oracle|CoreWeave|"
                r"a16z|Sequoia|Thrive|Founders Fund|Altman|Amodei|Musk|Zuckerberg|Hassabis|"
                r"Rakuten|Toyota|Sony|NTT|KDDI|Moonshot|DeepSeek|Alibaba|Tencent|ByteDance|Baidu|Naver|Kakao|Upstage|Rebellions|"
                r"Grab|GoTo|Sea Limited|Reliance|Infosys|Sarvam|Temasek|GIC|Peak XV|Antler|East Ventures|"
                r"楽天|トヨタ|ソニー|サイバーエージェント|LINEヤフー|ヤフー|メルカリ|オープンAI|アンソロピック|エヌビディア|エヌヴィディア|"
                r"サカナ|Preferred|PFN|ELYZA|ソフトバンク|孫正義|ファーストライト|XTech|グロービス|ジャフコ|JAFCO)\b|"
                r"楽天|トヨタ|ソニー|サイバーエージェント|LINEヤフー|メルカリ|オープンAI|アンソロピック|エヌビディア|ソフトバンク|孫正義", re.I)
_COP = CO.pattern.split("(?:", 1)[1].rsplit(")", 1)[0]
JOINROLE = re.compile(r"\b(?:joins?|joined)\b[^.\n]{0,60}\b(?:as|to lead|to head|to run|to build)\b", re.I)
# 会社名が直接続く形は、題名にあるときだけ数える(説明文の「joins a16z パートナー...」は出演の意味が多い)
JOINCO = re.compile(r"\b(?:joins?|joined)\s+(?:the\s+)?(?:" + _COP + r")\b(?!\s+(?:to discuss|to talk|to break|for|on|in)\b)", re.I)


def join_move(title, desc=""):
    return bool(JOINROLE.search(title + " " + desc) or JOINCO.search(title))


class _JM:  # 以前の名前(JOINMOVE.search)との互換
    @staticmethod
    def search(text):
        return JOINROLE.search(text) or JOINCO.search(text.split("  ")[0][:160])


JOINMOVE = _JM()


def main(days=3):
    cutoff = (datetime.date.today() - datetime.timedelta(days=days)).isoformat()
    leads, scanned = [], 0
    for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "youtube", "2*.json")) +
                    glob.glob(os.path.join(ROOT, "inbox", "podcasts", "2*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for v in d.get("videos", []) + d.get("episodes", []):
            if v["published"] < cutoff:
                continue
            scanned += 1
            text = v["title"] + " " + v.get("description", "")
            kws, cos = sorted({m.group(0).lower() for m in KW.finditer(text)} | ({"joins(役職)"} if join_move(v["title"], v.get("description", "")) else set())), sorted({m.group(0) for m in CO.finditer(text)})
            if kws and cos:
                leads.append({"source": v.get("channel") or v.get("show"), "type": "動画" if "channel" in v else "ポッドキャスト",
                              "published": v["published"], "title": v["title"], "url": v.get("url", ""),
                              "words": kws[:6], "companies": cos[:6]})
    leads.sort(key=lambda x: x["published"], reverse=True)
    out = os.path.join(ROOT, "inbox", "media"); os.makedirs(out, exist_ok=True)
    today = time.strftime("%Y-%m-%d"); base = os.path.join(out, today); k = 2
    if os.path.exists(base + ".json"):
        old = json.load(open(base + ".json", encoding="utf-8")).get("leads", [])
        if [l["url"] + l["title"] for l in old] == [l["url"] + l["title"] for l in leads]:
            return f"動画・番組の手がかり: {len(leads)}本(今日の記録と同じ)"
    while os.path.exists(base + ".json"):
        base = os.path.join(out, f"{today}-{k}"); k += 1
    summary = f"動画・番組の手がかり: 新着{scanned}本のうち{len(leads)}本に移籍・出資などの言葉と会社名"
    json.dump({"date": today, "days": days, "summary": summary, "leads": leads}, open(base + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(f"# 動画・番組の手がかり {today}\n\n{summary}\n\n手がかりです。確かめる前は相関図に入れません。\n\n| 日付 | 種類 | 番組・チャンネル | タイトル | 言葉 | 会社 |\n|---|---|---|---|---|---|\n")
        for l in leads:
            f.write(f"| {l['published']} | {l['type']} | {l['source']} | [{l['title'].replace('|','/')}]({l['url']}) | {', '.join(l['words'])} | {', '.join(l['companies'])} |\n")
    print(summary); print("記録:", os.path.relpath(base + ".md", ROOT))
    return summary


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--days", type=int, default=3)
    main(ap.parse_args().days)
