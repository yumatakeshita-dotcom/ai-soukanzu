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
6. `python3 scripts/media_backlog.py status` で README を更新 → `python3 scripts/merge_inbox.py` → commit して main に push
7. 報告は「確かめた○件・入れた○件・確かめられなかった○件・残り○件」の1行
