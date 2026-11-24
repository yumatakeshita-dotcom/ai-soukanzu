# 引き継ぎメモ（HANDOFF）

このファイルは、Claude Code と Muse の間で作業を引き継ぐためのメモです。
作業の終わりに更新し、始めに最初に読みます。詳しい仕組みは CLAUDE.md、移行の経緯は docs/migration_memo.md。

## いま何を作っているか
- 目的：AI企業・半導体企業の人・出資・取引・移籍のつながりを見せるWebサイト(site/index.html + 実験ページ site/lab/)
- 完成のイメージ：毎朝の調査が自動でデータを足し、確かさ(公式・開示・本人・報道)の印つきで見られる。ビジネス化の案は docs/business_notes.md

## どこまで終わったか(2026/11/24時点)
- 本体の相関図、確かさの一覧、人材の流れ、出資の一覧、幹部の年表、おもしろ情報、装いとブランド、調査エージェント一覧が稼働
- 毎朝の定期タスク(引き抜き・お金・Gemini・日本の3係・採用・品質チェック・見張り役など)が inbox/ に足し、main に push
- 11/24: 動画・音声の記録が「なし」と出た原因は日付のずれ(7:29はUTCだと前日→ファイル名が11/23になる)。日本時間にそろえる修正はPR #122でマージ済み
- 11/24: Muse側のリサーチを再開・拡張(お金の流れ・深掘り・引き抜き・世界の企業抽出・LP・VC資金・人物言葉の6部屋)。成果物は受け渡し置き場(Claude側 inbox)に順次入る。VC資金は再開後に裏付け2巡目と新規ファンドのバッチ18まで進み、候補は約245件。検索の手がかりにポッドキャストとXも追加(未確認の手がかりとして分離して保存、確定は公式・開示・報道の裏付けがあるものだけ)

- 11/24(PR #125〜127の上に積んだ分): TDnetの提携は、表題が長くても本文の「提携先の概要」から相手を読めるようにした(試験 scripts/test_tdnet_body.py、34件で誤り0)。HKEXは scripts/hkex_scan.py を新設し、全社ぶんの出資・買収・提携を本文で確かめたものだけ inbox/money/日付-hkex.json に自動で足す(ir_watch.py の最後に自動で動く。試験 scripts/test_hkex_scan.py)。詳しくは docs/ir_watch.md

## 次にやること（優先順）
1. 【マージ済み 2026-11-24】日付ずれ修正PR #122(Museレビュー済み→ユーザーの指示でマージ、merge commit c50082a)。残る確認: 翌朝、見張り役の「動画・音声係」が緑になるか。注意点: scripts/__pycache__ の .pyc が混ざっている(実害なし、.gitignore検討)
2. 未マージの古い下書きPR(#57 Stripe課金、#42 お金の流れv5、#10 有料サービス案)の扱いを決める
3. 【対応済み】日付ずれの他スクリプト点検: yt_deep.py, yt_fetch.py, media_money_candidates.py, yt_backfill.py は全てPR #122に含まれて切り替え済みだった

4. 【PR出し済み 2026-11-24】日本の提携係にTDnet(`tdnet_scan.py --kind alliance`)と、調査エージェント一覧に再確認待ち件数。PR #125(TDnet人事)の上に積んでいる

- 11/24(PR #127、#126の上に積んだ): `tdnet_scan.py` に `--kind invest`(相関図にない会社の出資・買収)を追加。alliance と invest は、条件がそろったものを `inbox/money/日付-tdnet.json` に自動で足す(条件は docs/ir_watch.md)

4. 【11/24 PR #125〜#129の上に積んだ分】TDnet提携を本文の定義(「以下「○○」といいます」)からも読む(tdnet_scan.py)/香港の覚書(MOU)が後日の発表で実行・完了・失効したかを確かめる(scripts/mou_followup.py、目録 inbox/ir/mou_followup.json)。#125→#129は未マージ。順にマージが必要

## 決めたこと・約束ごと
- データは足すだけで消さない。ファイルの削除・上書きは確認する
- 作業前に git pull。アーティファクトは直接直さない(正本はこのリポジトリ)
- PRは下書きで出す。マージはユーザーが「マージして」と言ったときだけ
- 返事は平易な日本語。終わったら次の候補を2〜3個

## 注意点・ハマりどころ
- index.html は約5.4MB。全体を読まず目印で探す
- site/data/ のファイルを足す・変えたら共有リンクのアーティファクトにも公開
- 毎朝の更新でSEO・法的ページの印が消えたら `python3 scripts/seo.py` / `scripts/legal.py`
- inbox/watchdog/ の記録で、毎朝の係が動いたか分かる

## 変更したファイル（直近）
- scripts/tdnet_scan.py, docs/ir_watch.md, docs/agents.json(+作り直した agents.md・site/agents/index.html), HANDOFF.md

## 最終更新
- 日時：2026-11-24
- 更新した側：Claude(スレッド)
