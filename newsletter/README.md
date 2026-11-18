# 週のまとめ(ニュースレター)

毎週月曜の朝に、前の週(月〜日)の「AIのお金と人の動き」をまとめる。

- 作り方: `python3 scripts/weekly.py`(発行日=今日。前の月曜〜日曜をまとめる)
- 冒頭の「今週のポイント」: `newsletter/lead/発行日.md` に箇条書き3つで書く。無ければ件数から自動で作る
- できるもの
  - `newsletter/issues/発行日.json` その号のデータ(号ごとに1つ。消さない)
  - `newsletter/発行日.md` メールやnoteにそのまま貼れる文章
  - `site/weekly/index.html` ニュースレターのページ(最新号+過去の号)
- 公開先: https://claude.ai/artifact/WnWyUzjmrSVHcxVgzKWPCM (相関図の共有リンクとは別のページ)
- 定期タスク「週のまとめ 毎週月曜」(日本時間 月曜 9:37。月曜の調査と9:13のサイト反映のあと)が、作る → push → 公開 → プロジェクトに報告 までやる

## 集める範囲
- 大きなニュース: `site/index.html` の UPDATES(毎日の更新記録)のうち、期間内の日付のもの
- お金の流れ・人の動き・ファンドとVC: `inbox/money` `inbox/moves` `inbox/vc` のうち、出来事の日付が期間内のもの
- 注目の会社: その週に `inbox/deep` に入った会社
- 調査で見つかった過去の動き: その週の調査で見つかったが、出来事が期間より前のもの(多いときは12件まで載せる)
- 世界企業(`inbox/world`)は登記データの話なので載せない

## 配る方法(まだ決めていない。外部のサービスには登録していない)
`docs/newsletter_options.md` を参照。
