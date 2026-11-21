#!/usr/bin/env python3
"""お金の流れの調査(inbox/money/)の出資のうち、公式・開示で出典のあるものを、出資の一覧の出典に足す道具(2026/11/21追加)。

対象: kind が「出資」で、confidence が「公式」か「開示」、src に URL があるもの。
出資する側(from)は「・」「、」「,」「/」で分け、「(リード)」などのかっこと「ほか」は外す。
足す先: site/data/investsrc.js の /*MONEY_SRC_START*/〜/*MONEY_SRC_END*/(行)と
        /*MONEY_DS_START*/〜/*MONEY_DS_END*/(出典)。足すだけ。すでにある行・キーは飛ばす。
名前が相関図の点と合わない行は、画面では何も起きない(壊れない)。

使い方:
  python3 scripts/invest_src_from_money.py          # 足す行を表示するだけ
  python3 scripts/invest_src_from_money.py --apply  # investsrc.js に足す
"""
import argparse
import glob
import hashlib
import json
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(ROOT, "site", "data", "investsrc.js")
OKCONF = {"公式": "o", "開示": "f"}


def clean(name):
    name = re.sub(r"[(（][^)）]*[)）]", "", name or "")
    name = re.sub(r"\s*(ほか|など|他)$", "", name.strip())
    return name.strip(" 　")


def investors(frm):
    out = []
    for p in re.split(r"[・、,/]", frm or ""):
        p = clean(p)
        if p and p not in ("ほか", "など") and len(p) <= 40 and p not in out:
            out.append(p)
    return out


def q(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    txt = open(FILE, encoding="utf-8").read()
    have = set(re.findall(r"\['([^']+)','([^']+)',\['(?:im_[0-9a-f]+)", txt))
    today = time.strftime("%Y/%m/%d")
    ds_lines, row_lines, seen = [], [], set()
    for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "money", "*.json"))):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for it in d.get("items") or [] if isinstance(d, dict) else []:
            cf = OKCONF.get(it.get("confidence"))
            if it.get("kind") != "出資" or not cf:
                continue
            src = [s for s in (it.get("src") or []) if len(s) > 1 and str(s[1]).startswith("http")]
            to = clean(it.get("to"))
            if not src or not to:
                continue
            key = "im_" + hashlib.md5(src[0][1].encode()).hexdigest()[:8]
            if f"{key}:[" not in txt and key not in seen:
                ds_lines.append(f" {key}:[{q(src[0][0])},{q(src[0][1])},'{cf}'],")
            seen.add(key)
            note = " ".join(x for x in [it.get("amount") or "", (it.get("date") or "").replace("-", "/")] if x).strip()
            for inv in investors(it.get("from")):
                if (inv, to) in have or (inv, to, key) in seen:
                    continue
                seen.add((inv, to, key))
                row_lines.append(f" [{q(inv)},{q(to)},['{key}'],{q(note[:60])},{q(today)}],")
    if not row_lines:
        print("足すものはありません")
        return 0
    print("\n".join(ds_lines + row_lines))
    if not a.apply:
        print(f"\n(表示だけ。足すには --apply)  行 {len(row_lines)} / 出典 {len(ds_lines)}")
        return 0
    txt = txt.replace("/*MONEY_DS_END*/", "".join(l + "\n" for l in ds_lines) + " /*MONEY_DS_END*/", 1)
    txt = txt.replace("/*MONEY_SRC_END*/", "".join(l + "\n" for l in row_lines) + " /*MONEY_SRC_END*/", 1)
    open(FILE, "w", encoding="utf-8").write(txt)
    print(f"site/data/investsrc.js に 行 {len(row_lines)} / 出典 {len(ds_lines)} を足しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
