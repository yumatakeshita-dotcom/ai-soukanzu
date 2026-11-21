#!/usr/bin/env python3
"""企業検索サイト(kigyo-asiapac)と相関図サイト(kigyo-relmap)の見張り。読むだけ・足すだけ。
応答・国ごとの社数(減っていないか)・検索の見本を確かめ、inbox/watchdog/kigyo-日付.md に記録する。
問題があると終了コード1。"""
import re, sys, json, urllib.request, urllib.parse, datetime, os
B = "https://kigyo-asiapac.yuma-takeshita.workers.dev"
R = "https://kigyo-relmap.yuma-takeshita.workers.dev/"
# 下限(これより減ったら異常)。国を足したらここに足す
MIN = {"台湾": 819965, "オーストラリア": 4760277, "シンガポール": 624977}
SAMPLES = [("Telstra", "オーストラリア"), ("DBS Bank", "シンガポール"), ("台灣積體電路製造", "台湾")]

def get(url, t=30):
    req = urllib.request.Request(url, headers={"User-Agent": "kigyo-health/1.0"})
    with urllib.request.urlopen(req, timeout=t) as r:
        return r.status, r.read().decode("utf-8", "replace")

jst = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=9)
today = jst.strftime("%Y-%m-%d")
lines, problems = [], []
try:
    st, html = get(B + "/")
    lines.append(f"- 企業検索トップ: {st}")
    for k, lo in MIN.items():
        m = re.search(re.escape(k) + r"\s*([\d,]+)社", html)
        n = int(m.group(1).replace(",", "")) if m else None
        ok = n is not None and n >= lo
        lines.append(f"- {k}: {n if n is not None else '読めず'}社(下限 {lo:,})" + ("" if ok else " ★異常"))
        if not ok: problems.append(f"{k}の社数が下限を下回るか読めない({n})")
except Exception as e:
    problems.append(f"企業検索トップに接続できない: {e}"); lines.append(f"- 企業検索トップ: 失敗 {e}")
for q, k in SAMPLES:
    try:
        st, h = get(B + "/search?q=" + urllib.parse.quote(q))
        hit = ("/c/" in h) or ("company" in h.lower()) or (q.split()[0].lower() in h.lower())
        lines.append(f"- 検索「{q}」: {st}")
        if st != 200: problems.append(f"検索「{q}」が{st}")
    except Exception as e:
        problems.append(f"検索「{q}」に失敗: {e}"); lines.append(f"- 検索「{q}」: 失敗")
try:
    st, h = get(R)
    m = re.search(r"LAST_CHECK='([^']*)'", h)
    lc = m.group(1) if m else "?"
    lines.append(f"- 相関図サイト: {st} / 最終確認日 {lc}")
    if st != 200: problems.append(f"相関図サイトが{st}")
    elif lc != "?" and (jst.date() - datetime.date.fromisoformat(lc)).days > 2:
        problems.append(f"相関図サイトの最終確認日が古い({lc})")
except Exception as e:
    problems.append(f"相関図サイトに接続できない: {e}"); lines.append("- 相関図サイト: 失敗")
status = "問題あり" if problems else "すべて順調"
out = f"# 企業検索の見張り {today}\n\n**{status}**\n\n" + "\n".join(lines) + "\n"
if problems: out += "\n## 問題\n" + "\n".join("- " + p for p in problems) + "\n"
os.makedirs("inbox/watchdog", exist_ok=True)
open(f"inbox/watchdog/kigyo-{today}.md", "w", encoding="utf-8").write(out)
print(out); sys.exit(1 if problems else 0)
