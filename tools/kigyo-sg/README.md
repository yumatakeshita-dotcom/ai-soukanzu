# シンガポールの会社を企業検索サイトに足す

2026年11月18日に作成。データ元は ACRA(シンガポールの会社登記の役所)が data.gov.sg で公開している「ACRA Information on Corporate Entities」。

## データについて
- 無料・申し込みなし。毎月更新(2026年11月16日更新を確認)
- 会社名の頭文字ごとに27個のCSV(A〜Z と その他)。1ファイルあたり数万件(例: 1つで58,192件)
- 解散・抹消した会社も入っているので、道具で「現存する会社」だけに絞る
- 利用条件: Singapore Open Data Licence v1.0。サイトに出典の表示が必要
  - 表示例: 「出典: Accounting and Corporate Regulatory Authority (ACRA), data.gov.sg / Singapore Open Data Licence v1.0」
- 公式の登記で見るリンク: 会社ごとの固定ページは無いため、BizFile の検索ページ(https://www.bizfile.gov.sg/)に飛ばす

## 手順(PCで)
1. このフォルダの `sg_acra.py` を、作業用のフォルダに置く
2. そのフォルダで `python sg_acra.py` を実行(数分〜十数分。27個をダウンロードする)
3. `sg_status.txt` を開き、「残す」の付いた状態(Live / Live Company / Registered)で合っているか確かめる
4. `sg_companies.csv` を、台湾・オーストラリアと同じやり方で D1 に**追加**する(国コードは `SG`)
   - 既存の台湾・オーストラリアのデータは消さない。足すだけ
5. サイトの国一覧と出典の欄に、シンガポールと上の出典表示を足す

## sg_companies.csv の列
| 列 | 中身 |
|---|---|
| id | UEN(シンガポールの会社番号) |
| name / name_en | 会社名(英語のみなので同じ値) |
| type | 会社の種類(例: Private Company Limited by Shares) |
| status | 状態(Live Company など) |
| established | 設立日・登録日 |
| address / postal_code | 住所・郵便番号 |
| industry_code / industry | 主な業種(SSIC コードと説明) |
| former_names | 旧社名(「 / 」区切り) |
| official_url | 公式の登記の検索ページ |

台湾・オーストラリアの取り込みで使っている列名と違うときは、ここの列名を合わせ直す。
