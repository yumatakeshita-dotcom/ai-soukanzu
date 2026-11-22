# 過去の動画・番組の手がかりを少しずつ確かめる(2026/11/21追加)

過去の動画・ポッドキャストのタイトル・説明文から拾った「移籍・出資・買収の手がかり」のうち、まだ確かめていないものを毎日10件ほどずつ確かめる。

## ファイル
- 未確認リスト: `inbox/backlog/queue.json`(足すだけ。状態 todo / done / checked / unverified と理由)
- 進み具合と「確かめられなかったもの(理由つき)」: `inbox/backlog/README.md`
- 道具: `scripts/media_backlog.py`
  - `sync` 新しい手がかりを足す / `next -n 8` 次の候補 / `mark ID 状態 "理由"` / `status` 進み具合
- 直近3日分は毎日の `media_digest.py` が見るので、このリストには入れない

## 手順(1回あたり10件まで)
1. `git pull`、`python3 scripts/media_backlog.py sync`、`python3 scripts/media_backlog.py next -n 10`
2. 各候補の説明文から、**具体的な動き**(だれがどこへ移った・だれがいくら出資・どこがどこを買収)を取り出す。司会やゲストの紹介だけのものは `checked`(理由:動きではない)
3. 独立した情報源(公式発表・複数の報道)で、**名前・日付・金額**を WebSearch で確かめる。動画の説明文だけで入れない。名前の取り違えに注意
4. 通ったものだけ `inbox/money/日付-backlog.json`・`inbox/moves/日付-backlog.json` に**足すだけ**(形は `inbox/money/2026-11-21-backlog.json` と同じ。`via:"backlog"`、移籍は `backfill:true`)。すでに inbox か相関図にあるものは足さず `checked`(理由:すでにある)
5. 状態を `mark` で記録。入れたら `done`、確認できないものは `unverified` に理由つき(例:報道が1件だけ・日付が合わない・見つからない)。削除はしない
6. `python3 scripts/media_backlog.py status` で README と進み具合の記録(`inbox/backlog/history.json`、画面用の `site/data/backlog.js`)を更新 → `python3 scripts/merge_inbox.py` → commit して main に push
7. 報告は「確かめた○件・入れた○件・確かめられなかった○件・残り○件」の1行

## 過去動画の一覧も入れた(2026/11/21)
- `media_backlog.py sync` が `inbox/youtube/backfill/`(各チャンネル最新100本の題名。`scripts/yt_backfill.py`)も読む。説明文が無く古さだけなので、日付は「3mo ago」などからおおよそ作る(`approx_date`)
- 各手がかりに `newnames`(題名にある英字の固有名詞のうち、相関図のデータに1回も無いもの)を付け、`next` の並びで少しだけ先にする。ゲスト名なども拾うので、あくまで軽い加点

## 出演の意味の「joins」を除いた(2026/11/21)
- 確かめて外れた288件のうち259件(9割)は、「○○ joins the show / joins 司会者…」という出演の意味で、移籍ではなかった
- `media_digest.py` の `join_move()` が、「joins ... as / to lead」の形(説明文も見る)か、題名で「joins 会社名」と直接続く形(続きが to discuss・for・on などでないもの)のときだけ移籍の手がかりとして数える。`media_backlog.py` も同じ判定を使う
- すでにリストにあった未確認のうち、出演の意味だけだった34件は、状態を checked にして理由を書いた(消していない)。毎日の手がかりのまとめは51本→40本に減った

## 残りの外れ29件の理由を集計して、リストの段階で除いた(2026/11/22)
- 理由: 直近3日のもの20件(毎日の手がかりのまとめが見るので、過去分のリストでは見ない。すでに `RECENT_DAYS` で除外)、すでに相関図にあったもの9件(20VCなど複数の話題のまとめ回)
- 追加した条件(`media_backlog.py` の `noise_reason`): (1)buy・leave・left・join の原形が説明文にあるだけで題名にない(2)「20VC:」か「|」で区切った複数話題のまとめ回で、題名の名前がすべて相関図にすでにある。人の動きを思わせる題名(exodus・shakeup・quit・poach・hires など)は残す
- `python3 scripts/media_backlog.py prune` が、すでにある todo のうち当てはまるものを checked にして理由を書く(消さない)。60件を checked に(todo 413→353)。まちがいなら `mark ID todo` で戻せる
- `sync` も、当てはまるものは新しくリストに足さない

## 進み具合を画面に出した(2026/11/22)
- `status` を動かすたびに、その日の件数(todo/done/checked/unverified)を `inbox/backlog/history.json` に足し(同じ日は置き換え・前の日は消さない)、`site/data/backlog.js` を書き直す。11/21分は git の履歴から埋めた
- 「確かめられなかったもの」(unverified)の理由は、同じ欄の折りたたみに出る(`BACKLOG_UNV`)
- ホーム(「調査のようす」)と調査エージェント一覧の上に「確かめ係の進み具合」の欄が出る(残り○件・前の記録からの増減・直近7日の表)。部品は `backlog.js` の `backlogBox()`
- **`site/data/backlog.js` が変わったら共有リンクのアーティファクトにも公開する**(毎朝の自動更新は index.html しか公開しないため)。10:07のタスクは手順7のあとに公開まで行う
