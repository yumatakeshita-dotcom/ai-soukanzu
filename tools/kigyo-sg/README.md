# シンガポールの会社(ACRA)

出典: Accounting and Corporate Regulatory Authority (ACRA), data.gov.sg / Singapore Open Data Licence v1.0

## 作り直す手順(クラウドでできる)
1. `python3 sg_acra.py` で ACRA のデータを取り、現存する会社だけの `sg_companies.csv` を作る(プロジェクトのファイル `kigyo-sg/` にもある)
2. `node --max-old-space-size=6000 build_sg.mjs sg_companies.csv sg` で、サイトと同じ形のファイルを `sg/` に作る
3. `python3 load_d1.py`(`sg/` があるフォルダで)で、D1「kigyo-sg」の表 `f` に入れる
   - 足すだけ(INSERT OR IGNORE)。途中で止まっても、もう一度動かせば続きから入る
   - 毎月の更新で中身を新しくするときは、新しい表を作ってから切り替える(今の表は消さない)
