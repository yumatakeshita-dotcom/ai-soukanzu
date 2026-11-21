"""ニュージーランドの会社(Companies Office の月ごとの一括データ)から、現存する会社だけの一覧を作る。
使い方: python3 -I nz_prepare.py <解凍したフォルダ> nz_companies.csv
出力の列はシンガポールと同じ(tools/kigyo-sg/build_sg.mjs でそのまま使える)。
使う元ファイル: companies_core_data.csv / companies_registered_office_address.csv / companies_business_industry_classification.csv
役員・株主のファイル(個人の名前)は使わない。
"""
import csv, sys, os, collections
src, out = sys.argv[1], sys.argv[2]
csv.field_size_limit(10**8)
def rows(name):
    p = os.path.join(src, name)
    if not os.path.exists(p):
        print("見つからない:", name); return
    with open(p, newline="", encoding="utf-8-sig", errors="replace") as f:
        yield from csv.DictReader(f)

status = collections.Counter()
core = {}
for r in rows("companies_core_data.csv"):
    st = (r.get("ENTITY_STATUS") or "").strip()
    status[st] += 1
    if st.lower() != "registered" or (r.get("REMOVAL_DATE") or "").strip():
        continue
    core[r["NZBN"].strip()] = r

addr = {}
for r in rows("companies_registered_office_address.csv"):
    k = r["NZBN"].strip()
    if k not in core: continue
    # いちばん新しい住所を使う
    if k in addr and (addr[k].get("START_DATE") or "") >= (r.get("START_DATE") or ""): continue
    addr[k] = r

bic = {}
for r in rows("companies_business_industry_classification.csv"):
    k = r["NZBN"].strip()
    if k not in core: continue
    if k in bic and (bic[k].get("START_DATE") or "") >= (r.get("START_DATE") or ""): continue
    bic[k] = r

with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id","name","name_en","type","status","established","address","postal_code","industry_code","industry","former_names","official_url"])
    for k, r in core.items():
        a = addr.get(k, {})
        lines = [a.get(f"REGISTERED_OFFICE_ADDRESS_{i}", "").strip() for i in range(1, 5)]
        country = (a.get("REGISTERED_OFFICE_ADDRESS_COUNTRY") or "").strip()
        address = ", ".join([x for x in lines if x] + ([country] if country and country.upper() not in ("NZ", "NEW ZEALAND") else []))
        b = bic.get(k, {})
        w.writerow([k, r["ENTITY_NAME"].strip(), r["ENTITY_NAME"].strip(), r.get("ENTITY_TYPE","").strip(), r.get("ENTITY_STATUS","").strip(),
                    (r.get("REGISTRATION_DATE") or "").strip()[:10], address, (a.get("REGISTERED_OFFICE_ADDRESS_POSTCODE") or "").strip(),
                    (b.get("INDUSTRY_CLASSIFICATION_CODE") or "").strip(), (b.get("INDUSTRY_CLASSIFICATION_DESCRIPTION") or "").strip(), "",
                    f"https://www.nzbn.govt.nz/mynzbn/nzbndetails/{k}/"])

with open(os.path.splitext(out)[0] + "_status.txt", "w", encoding="utf-8") as f:
    f.write(f"全件: {sum(status.values())}\n現存として残した件数: {len(core)}\n住所あり: {len(addr)} / 業種あり: {len(bic)}\n\n状態ごとの件数:\n")
    for s, n in status.most_common(): f.write(f"{n}\t{s}\n")
print("現存:", len(core), "住所:", len(addr), "業種:", len(bic))
