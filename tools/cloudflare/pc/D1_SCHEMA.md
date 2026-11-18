# D1 と海外の会社データの置き場所(2026-11-18 に読み取りだけで調査)

D1 の中身は一切変えていません(どの問い合わせも `changed_db: false`、書き込み 0 行)。

## 一番大事なこと: 台湾・オーストラリアは D1 に入っていない

- D1 は `houjin` の1つだけで、**国コードの列を持つ会社の表はありません**。`corp` は日本の法人番号の表です。
- 台湾(TW)・オーストラリア(AU)の会社は、Worker **`kigyo-asiapac`** の**静的ファイル**(Workers Assets)にあります。
  - フォルダ: `relationship-map-asiapac/public/`(このリポジトリには入れていません。`LARGE_FILES.txt` 参照)
  - `public/c/<番号>.json` … 会社ページ用。`[[国,番号,名称,種別,市,郵便番号,設立日,業種], ...]`。番号 = FNV-1a(`国:登記番号`) % nd
  - `public/n/<番号>.json` … 名前検索用。`[[国,番号,名称,市], ...]`。名前の核(法人格の語を除いて小文字化)の頭2〜6文字で決まる
  - `public/n/hot.json`、`public/c/meta.json`
  - 作る道具: `relationship-map-src/build_asiapac_shards.py`(環境変数 `AP_SRCS` に sqlite を `;` 区切りで渡す)
  - 検索の画面とハッシュ規則: `relationship-map-asiapac/src/app.mjs`(Python 側の `core()`・`fnv()` と同じ規則にすること)
- 元データ(PC の `~/.claude/data/`、表 `wcorp (cc, id, name, kind, city, post, since, sic)`、主キー `(cc, id)`)
  - AU: `world_au.sqlite`(601MB) ← `load_au.py`(ABN Bulk Extract、現存の法人・団体のみ、個人事業主を除く)
  - TW: `world_tw_final.sqlite`(86MB) ← `crawl_tw.py`(経済部 商工行政資料開放平台の API)
- 国ごとの行数(`public/c/meta.json`、2026-11-17 作成)

| 国コード | 行数 |
|---|---|
| AU | 4,760,277 |
| TW | 819,965 |
| 合計 | 5,580,242(nd=1861, nb=3721) |

→ シンガポール(SG)を足すなら、`wcorp` と同じ形の `world_sg.sqlite` を作り、`AP_SRCS` に足して `build_asiapac_shards.py` を回し、`kigyo-asiapac` に公開し直すのが今の作りに合います。D1 の1日の書き込み上限は関係しません(ファイル数・Assets の上限のほうが関係します)。

参考: ヨーロッパは同じ作りの Worker `kigyo-europe`(UK 5,596,581 / FR 8,987,767 / NO 1,176,614 / EE 371,828 / FI 462,433、計 16,595,223、2026-11-15 作成)。

## Worker の一覧(wrangler.toml)

| フォルダ | Worker 名 | D1 | 中身 |
|---|---|---|---|
| relationship-map-site | kigyo-hito-tsunagari | houjin (binding `DB`) | 日本の会社と人のつながり |
| relationship-map-asiapac | kigyo-asiapac | なし | 台湾・オーストラリアの会社(静的ファイル) |
| relationship-map-europe | kigyo-europe | なし | ヨーロッパの会社(静的ファイル) |
| relationship-map-static | kigyo-relmap | なし | 相関図の公開版(静的ファイル、publish_static.py が作る) |

## wrangler d1 list

| 名前 | uuid | 作成 | 表の数(表示) | 大きさ | 用途 |
|---|---|---|---|---|---|
| houjin | 20d760a8-8e71-4cef-bc4b-71631888785b | 2026-11-11 | 0(一覧の表示上。実際は下の28表) | 45,273,088 バイト | 日本の会社・人物・お金の流れ(kigyo-hito-tsunagari 用) |

## houjin の表と行数

| 表 | 行数 | 作り |
|---|---|---|
| company_alias | 6 | `slug TEXT, alias TEXT` |
| company_fact | 30 | `slug, sec, text, url, ord INTEGER` |
| corp | 66,963 | `num TEXT PRIMARY KEY, name, kind, pref, city, street, zip, en, kana, since, upd`(日本の法人番号) |
| edinet | 6,980 | `code, kind, listed, name, en, addr, industry, sec, num` |
| events | 4,836 | `id TEXT PRIMARY KEY, ts, src, title, url, kind, score INTEGER, num, company` |
| img | 2,118 | `key TEXT PRIMARY KEY, ext, src, url` |
| lp_commit | 50 | `lp, fund, total_m INTEGER, commit_m INTEGER, year INTEGER, url` |
| lp_fund | 69 | `lp, mgr, fund, vintage INTEGER, committed_usd INTEGER, asof, url` |
| lp_side | 7 | `lp, what, url` |
| mapco | 9,291 | `slug TEXT PRIMARY KEY, name, en, note, num, people INTEGER, acq INTEGER` |
| mapco_acq | 4,434 | `slug, year, target, amount, note` |
| mapco_news | 5,959 | `slug, d, title, url, media` |
| mapco_people | 10,864 | `slug, name, en, role, since, until, note, q` |
| money_flow | 30,864 | `src, dst, kind, label, year, amount, note, url, media, d` |
| person | 6,628 | `q TEXT PRIMARY KEY, en, ja, d, intro, w, t` |
| person_alias | 13 | `q, alias` |
| person_feed | 2,297 | `q, ts, src, title, url, kind` |
| person_quote | 2,455 | `q, w, t, text` |
| person_rel | 250 | `q, rq, rel` |
| person_role | 8,531 | `q, company, role` |
| person_social | 1,769 | `q TEXT PRIMARY KEY, x, ig, yt, web` |
| person_src | 25 | `q, label, url` |
| person_timeline | 752 | `q, y INTEGER, y2 INTEGER, kind, label, ref INTEGER` |
| rel_news | 1,371 | `num, d, title, url, media` |
| rel_people | 2,177 | `num, name, en, role, since, until, note` |
| reports | 0 | `id INTEGER PRIMARY KEY, ts, page, text` |
| top100 | 100 | `q TEXT PRIMARY KEY, grp, checked_at, photo, intro, timeline, sns, feed, quotes`(INTEGER) |
| vc_fund | 43 | `mgr, fund, size, usd_m REAL, whenx, status, lp, note, url, conf` |

ほかに Cloudflare の内部表 `_cf_KV` があります。

索引: i_calias(company_alias.alias), i_cfact(company_fact.slug), i_edinet_num(edinet.num), i_ev_num(events.num,ts), i_ev_ts(events.ts), i_mapco_a/n/p(mapco_acq/news/people.slug), i_mapco_name(mapco.name), i_mapco_num(mapco.num), i_mf_d/i_mf_s(money_flow.dst/src), i_name(corp.name), i_pref(corp.pref,city), i_palias, i_person_en, i_person_ja, i_person_role, i_pf(person_feed.q,ts), i_pq, i_prel, i_psrc, i_ptl, i_rel_news(num,d), i_rel_people(num), i_vc_u(vc_fund.usd_m)。

## このフォルダに入れたもの

- `relationship-map-src/` … PC の作業フォルダの .py / .sql / .js / .bat / .md、`moves_extra.json`、`ext_adds/`(取り込みや公開の道具。データの .json やログは入れていません)
- `relationship-map-site/`、`relationship-map-asiapac/`、`relationship-map-europe/`、`relationship-map-static/` … wrangler.toml、package.json、src/、site の .sql / .py
- 鍵の検査: トークン・パスワードらしき文字列は見つからず、置き換えは 0 件。`.env`、`.dev.vars`、`~/.wrangler`、`wrangler_login*.log` は入れていません。
