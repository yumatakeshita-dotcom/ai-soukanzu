#!/usr/bin/env python3
"""本人のXで確かめた移籍に「本人」の印を付ける道具(2026/11/20追加)。

引き抜き(moves)の調査が inbox/moves/ に残した候補のうち、出典に本人のXの投稿(x.com/名前/status/番号)か
プロフィール(x.com/名前)が入っているものを、X公式の埋め込みサービスで実際に開いて確かめる。
確かめられたら、相関図の「人の動き」の線に本人の印(s)で出典を足す行を作る。

確かめること:
  投稿: 投稿者のURLの名前が出典のURLと同じ / 投稿者の表示名が候補の英語名と合う / 本文と日付が取れる
  プロフィール: 見つかる / 表示名が候補の英語名と合う / 自己紹介に移籍先の会社名が入っている
  (どちらも、候補の confidence が「本人の発言」か「公式」のものだけ。報道の記事の出典は対象外)

使い方:
  python3 scripts/moves_x_apply.py            # 確かめて、足す行を表示するだけ(何も書き換えない)
  python3 scripts/moves_x_apply.py --apply    # site/index.html に足す(足すだけ。既存の行は消さない・直さない)
  python3 scripts/moves_x_apply.py --since 2026-11-15   # このファイル日付以降の inbox/moves/ だけ見る

足す場所(site/index.html の目印の間):
  /*XV_DS_START*/ ... /*XV_DS_END*/    出典 DS の行(キーは v_苗字)
  /*XV_PPL_START*/ ... /*XV_PPL_END*/  VERIFY_PPL の行 [人の名前, 移籍先, 出典キー, ひとこと, 確かめた日]
すでに DS か VERIFY_PPL にある人(名前が同じ)は飛ばす。確かめられなかった候補は、理由つきで表示するだけで足さない。
"""
import argparse
import glob
import json
import os
import re
import sys
import time
import jst

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from x_check import post, profile  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "site", "index.html")
STATUS = re.compile(r"https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/status/(\d{5,25})")
PROFILE = re.compile(r"^https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/?$")
OK_CONF = ("本人の発言", "公式")


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def name_match(display, en):
    """表示名と英語名が合うか(苗字・名前のどれかが含まれる、順番や記号は無視)。"""
    d = norm(display)
    parts = [norm(p) for p in re.split(r"\s+", en or "") if len(norm(p)) >= 3]
    return bool(d) and any(p in d for p in parts)


def company(to):
    t = re.split(r"[(（]", to or "")[0].strip()
    return t


def slug(en):
    p = [norm(x) for x in re.split(r"\s+", en or "") if norm(x)]
    return "v_" + (p[-1] if p else "x")


def load_candidates(since):
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, "inbox", "moves", "*.json"))):
        base = os.path.basename(f)
        if since and base[:10] < since:
            continue
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for it in d.get("items") or []:
            if isinstance(it, dict) and it.get("confidence") in OK_CONF:
                out.append((base, it))
    return out


def existing(txt):
    ppl = re.findall(r"^\s*\['([^']+)',", txt[txt.index("const VERIFY_PPL=["):], re.M)
    keys = set(re.findall(r"^\s*(v_[a-z0-9]+):\[", txt, re.M))
    return set(ppl), keys


def check(it):
    """候補1件を確かめる。戻り値: (種類, 出典URL, 出典の説明, エラー理由)。"""
    en = it.get("name_en", "")
    cands = []
    for s in it.get("src") or []:
        url = s[1] if len(s) > 1 else ""
        m = STATUS.match(url)
        if m:
            cands.append(("post", f"https://x.com/{m.group(1)}/status/{m.group(2)}", m.group(1)))
    for s in it.get("src") or []:
        url = s[1] if len(s) > 1 else ""
        m = PROFILE.match(url)
        if m:
            cands.append(("profile", f"https://x.com/{m.group(1)}", m.group(1)))
    if not cands:
        return None
    why = []
    for kind, url, handle in cands:
        if kind == "post":
            p = post(url)
            if p.get("error"):
                why.append(f"投稿を開けない({url})")
                continue
            au = (p.get("author_url") or "").rstrip("/").rsplit("/", 1)[-1].lower()
            if au != handle.lower():
                why.append(f"投稿者が違う({au})")
                continue
            if not name_match(p.get("author"), en):
                why.append(f"表示名が合わない({p.get('author')})")
                continue
            if not p.get("text"):
                why.append("本文が取れない")
                continue
            return ("post", url, p.get("date", ""), "")
        else:
            p = profile(handle)
            if p.get("error") or not p.get("found"):
                why.append(f"プロフィールが見つからない(@{handle})")
                continue
            if not name_match(p.get("name"), en):
                why.append(f"表示名が合わない({p.get('name')})")
                continue
            comp = norm(company(it.get("to", "")))
            if not comp or comp not in norm(p.get("bio", "")):
                why.append(f"自己紹介に移籍先が無い({p.get('bio', '')[:40]})")
                continue
            return ("profile", url, "", "")
    return ("fail", "", "", " / ".join(why))


def insert(txt, marker, lines):
    end = f"/*{marker}_END*/"
    if end not in txt:
        raise SystemExit(f"目印 {end} が site/index.html に見つかりません")
    return txt.replace(end, "".join(l + "\n" for l in lines) + " " + end, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--since", default="")
    ap.add_argument("--ignore-existing", action="store_true", help="試験用: すでにある人も対象にする")
    a = ap.parse_args()
    txt = open(INDEX, encoding="utf-8").read()
    have_ppl, have_keys = existing(txt)
    today = jst.strftime("%Y/%m/%d")
    ds_lines, ppl_lines, seen = [], [], set()
    for base, it in load_candidates(a.since):
        nm = it.get("name_ja") or it.get("name_en") or ""
        if not nm or nm in seen:
            continue
        if not a.ignore_existing and nm in have_ppl:
            continue
        r = check(it)
        if r is None:
            continue
        seen.add(nm)
        kind, url, date, err = r
        if kind == "fail":
            print(f"× {nm}({base}): 確かめられず - {err}")
            continue
        key, n = slug(it.get("name_en", "")), 2
        while key in have_keys:
            key = f"{slug(it.get('name_en', ''))}{n}"
            n += 1
        have_keys.add(key)
        to = company(it.get("to", ""))
        if not to or to in ("退任", "(退任)"):
            print(f"- {nm}: 移籍先が無いので飛ばしました")
            continue
        d = (it.get("date") or "").replace("-", "/")
        if kind == "post":
            ds = f"{nm}本人のX({d}、{to}に関する投稿。{today}にXで確認)"
            note = "本人のXの投稿で確認"
        else:
            ds = f"{nm}本人のXのプロフィール({today}確認、自己紹介に{to})"
            note = "本人のXのプロフィールで確認"
        ds_lines.append(f" {key}:['{ds}','{url}','s'],")
        ppl_lines.append(f" ['{nm}','{to}','{key}','{note}','{today}'],")
        print(f"○ {nm} → {to}: {kind} {url} {date}")
    if not ds_lines:
        print("足すものはありません")
        return 0
    if not a.apply:
        print("\n--- DS ---\n" + "\n".join(ds_lines) + "\n--- VERIFY_PPL ---\n" + "\n".join(ppl_lines))
        print("\n(表示だけ。足すには --apply)")
        return 0
    txt = insert(txt, "XV_DS", ds_lines)
    txt = insert(txt, "XV_PPL", ppl_lines)
    open(INDEX, "w", encoding="utf-8").write(txt)
    print(f"site/index.html に {len(ds_lines)} 件足しました")
    return 0


if __name__ == "__main__":
    sys.exit(main())
