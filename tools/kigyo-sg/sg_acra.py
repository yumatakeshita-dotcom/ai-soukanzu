# -*- coding: utf-8 -*-
"""
シンガポール(ACRA)の会社登記データを data.gov.sg から一括ダウンロードし、
「現存する会社」だけの1つのCSV(sg_companies.csv)にまとめる道具。

使い方(Windows / Mac どちらでも。Python 3.8 以上、追加のインストール不要):
    python sg_acra.py
出力:
    sg_raw/         … 元のCSV 27個(そのまま保存。消さない)
    sg_companies.csv … 現存する会社だけ、検索サイト用の列にそろえたもの
    sg_status.txt    … 状態(Live など)ごとの件数。取り込み前の確認用

データ元: Accounting and Corporate Regulatory Authority (ACRA), data.gov.sg
利用条件: Singapore Open Data Licence v1.0(出典の表示が必要)
"""
import csv, json, os, sys, time, urllib.request
from collections import Counter

COLLECTION = "https://api-production.data.gov.sg/v2/public/api/collections/2/metadata"
POLL = "https://api-open.data.gov.sg/v1/public/api/datasets/{}/poll-download"
INIT = "https://api-open.data.gov.sg/v1/public/api/datasets/{}/initiate-download"
UA = {"User-Agent": "kigyo-asiapac-importer/1.0"}
# 「現存する会社」とみなす状態。sg_status.txt を見て足し引きしてよい
LIVE = {"live", "live company", "registered"}

def get_json(url, method="GET"):
    req = urllib.request.Request(url, headers=UA, method=method)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def download(did, path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print("  既にあります:", path); return
    url = None
    for i in range(10):
        d = get_json(POLL.format(did)).get("data") or {}
        if d.get("url"):
            url = d["url"]; break
        try: get_json(INIT.format(did), "GET")
        except Exception: pass
        time.sleep(3)
    if not url:
        raise RuntimeError("ダウンロード先を取得できませんでした: " + did)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(path + ".part", "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)
    os.replace(path + ".part", path)

def clean(v):
    v = (v or "").strip()
    return "" if v.lower() == "na" else v

def address(r):
    unit = ""
    if clean(r.get("level_no")) or clean(r.get("unit_no")):
        unit = "#{}-{}".format(clean(r.get("level_no")), clean(r.get("unit_no")))
    parts = [clean(r.get("block")), clean(r.get("street_name")), unit,
             clean(r.get("building_name")), clean(r.get("other_address_line1")),
             clean(r.get("other_address_line2"))]
    s = " ".join(p for p in parts if p)
    pc = clean(r.get("postal_code"))
    return (s + (" Singapore " + pc if pc else "")).strip()

def main():
    os.makedirs("sg_raw", exist_ok=True)
    meta = get_json(COLLECTION)["data"]["collectionMetadata"]
    ids = meta["childDatasets"]
    print("データの最終更新:", meta.get("lastUpdatedAt"), " ファイル数:", len(ids))
    for n, did in enumerate(ids, 1):
        print("[{}/{}] {}".format(n, len(ids), did))
        download(did, os.path.join("sg_raw", did + ".csv"))

    status, kept, total, seen = Counter(), 0, 0, set()
    cols = ["id", "name", "name_en", "type", "status", "established",
            "address", "postal_code", "industry_code", "industry", "former_names",
            "official_url"]
    with open("sg_companies.csv", "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out); w.writerow(cols)
        for did in ids:
            with open(os.path.join("sg_raw", did + ".csv"), newline="", encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    total += 1
                    st = clean(r.get("entity_status_description"))
                    status[st] += 1
                    uen = clean(r.get("uen"))
                    if st.lower() not in LIVE or not uen or uen in seen:
                        continue
                    seen.add(uen)
                    former = [clean(r.get("former_entity_name%d" % i)) for i in range(1, 16)]
                    name = clean(r.get("entity_name"))
                    w.writerow([
                        uen, name, name,
                        clean(r.get("company_type_description")) or clean(r.get("entity_type_description")),
                        st, clean(r.get("registration_incorporation_date")),
                        address(r), clean(r.get("postal_code")),
                        clean(r.get("primary_ssic_code")), clean(r.get("primary_ssic_description")),
                        " / ".join(x for x in former if x),
                        "https://www.bizfile.gov.sg/",
                    ]); kept += 1
    with open("sg_status.txt", "w", encoding="utf-8") as f:
        f.write("全件: {}\n現存として残した件数: {}\n\n状態ごとの件数:\n".format(total, kept))
        for k, v in status.most_common():
            f.write("{}\t{}{}\n".format(v, k, "  ← 残す" if k.lower() in LIVE else ""))
    print("完了。全件 {} 件のうち、現存 {} 件を sg_companies.csv に書きました。".format(total, kept))
    print("状態ごとの件数は sg_status.txt を見てください。")

if __name__ == "__main__":
    main()
