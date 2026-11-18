# シンガポールの会社(ACRA)

出典: Accounting and Corporate Regulatory Authority (ACRA), data.gov.sg / Singapore Open Data Licence v1.0

## 作り直す手順(クラウドでできる)
1. `python3 sg_acra.py` で ACRA のデータを取り、現存する会社だけの `sg_companies.csv` を作る(プロジェクトのファイル `kigyo-sg/` にもある)
2. `node --max-old-space-size=6000 build_sg.mjs sg_companies.csv sg` で、サイトと同じ形のファイルを `sg/` に作る
3. `python3 load_d1.py`(`sg/` があるフォルダで)で、D1「kigyo-sg」の表 `f` に入れる
   - 足すだけ(INSERT OR IGNORE)。途中で止まっても、もう一度動かせば続きから入る
   - 毎月の更新で中身を新しくするときは、新しい表を作ってから切り替える(今の表は消さない)

## 版と毎月の更新(2026-11-18 追加)
- D1「kigyo-sg」の表 `ver` に版の一覧がある。サイトは `ver` のいちばん新しい版(`/版の名前/c/...` など、圧縮して入っている)を読む。`ver` が空なら最初の版(そのままの形)を読む
- 版 `2026-11-18b` から、旧社名でも検索できる(旧社名 約10万件)
- 毎月20日の定期タスクが `bash tools/kigyo-sg/monthly.sh` を実行して、新しい版を足す
  - 件数が前の版より1割以上減ったとき、データベースが400MBを超えたときは、切り替えずに止まる
  - 前の版は消さない。無料プランでは1つのデータベースが500MBまでなので、古い版を消すかどうかは持ち主に聞く
