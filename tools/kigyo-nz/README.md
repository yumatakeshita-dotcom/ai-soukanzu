# ニュージーランドの会社(Companies Office の一括データ)

2026-11-19 準備。持ち主が Companies Office に一括データの利用を申し込み、承認待ち(返事は3営業日以内)。

## 承認されたら
1. Box.com の共有フォルダから、いちばん新しい zip(CSV 19個)を取ってきて解凍する
2. `python3 -I tools/kigyo-nz/nz_prepare.py <解凍したフォルダ> nz_companies.csv`
   - 状態が Registered で、抹消日が空の会社だけを残す。役員・株主のファイル(個人名)は使わない
   - 件数は `nz_companies_status.txt` に出る
3. `CC=NZ SOURCE="NZ Companies Office bulk data" NB=600 ND=600 node --max-old-space-size=6000 tools/kigyo-sg/build_sg.mjs nz_companies.csv nz`
4. D1 に新しいデータベース「kigyo-nz」を作り、`D1_DB=<その番号> python3 tools/kigyo-sg/load_d1.py nz --ver <日付>` で入れる(足すだけ・圧縮)
5. `python3 tools/kigyo-asiapac/add_nz_patch.py` で worker.js にニュージーランドを足し、`deploy_worker.py` の bindings に `{"type":"d1","name":"NZDB","id":"<その番号>"}` を足して出す

## 出典の表示
「ニュージーランド Companies Office(Ministry of Business, Innovation and Employment)・Companies Office Bulk Data Access Agreement」。会社ごとのページから NZBN の公式ページへリンクする。
