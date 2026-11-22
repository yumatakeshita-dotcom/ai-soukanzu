# YouTubeの字幕をPC側で取る手順(2026/11/23追加)

クラウドからはYouTubeの字幕がロボット確認で断られる(説明文と題名だけで調べている)。祐真さんのPCのブラウザ(ログイン不要)では、動画ページの「文字起こし」が読める。これを使って、手がかりを `inbox/` に置き、クラウドの調査が使える流れにする。

## 流れ
1. クラウド側(毎朝の調査): `python3 scripts/yt_pc_queue.py` が「PCで読む動画」を決める → `inbox/youtube/pc_queue.json`(題名に移籍・出資の言葉と会社名がある動画、字幕が取れず `yt_retry.txt` に残った動画)
2. PC側(定期タスク): 順番待ちの動画の文字起こしを読み、手がかりの抜粋を `inbox/youtube/transcripts/動画ID.md` に保存して、ブランチをpush
3. クラウド側: PRを下書きで作る(PCにはGitHubログインがないため)。マージは祐真さんの「マージして」待ち
4. 次の調査が `inbox/youtube/transcripts/` を読み、報道・公式で確かめられたものだけ `inbox/money/`・`inbox/moves/` に足す(抜粋だけでは足さない)

## 守ること
- 読むだけ。YouTubeにコメント・高評価・登録はしない。ログインしない
- 保存するのは全文ではなく、言葉で絞った抜粋(最大80行)。全文は保存しない
- データは消さず、足すだけ。すでにあるファイルは上書きしない(道具が止める)
- `python scripts/merge_inbox.py` は実行しない(取り込みは9:13の定期タスクの仕事)
- 断られ方をごまかす工夫はしない。文字起こしが出ない動画は飛ばして報告する

## PCでの読み方(ChromeのClaude拡張、または内蔵ブラウザ)
- 動画ページ(https://www.youtube.com/watch?v=ID)を開く → 概要欄の「…もっと見る」→「文字起こしを表示」
- 文字起こしは、ページ内の `transcript-segment-view-model` が1行ずつ(時刻と本文)。JavaScriptで全部の行の本文を返し、一時ファイルに1行=1発言で書く
- 出力にクッキーやURLのクエリが入ると読み取りがブロックされるので、本文と時刻だけを返す
- 保存: `python scripts/yt_pc_save.py ID --title "題名" --channel "チャンネル" --date 日付 --file 一時ファイル`

## PCの定期タスク(祐真さんがPCのClaudeアプリで登録する)
名前: `毎朝 YouTubeの文字起こしから手がかりを拾う` / 頻度: 毎日 8:50(`50 8 * * *`)。X用の `docs/x_daily_pc.md` の8:35のあと。

```text
あなたは祐真さんのPCで動く。相関図リポジトリ(GitHub: yumatakeshita-dotcom/ai-soukanzu)に、YouTubeの文字起こしから拾った手がかりの抜粋を足す。報告は平易な日本語で。

【守ること】
- YouTubeは読むだけ。ログイン・コメント・高評価・登録はしない
- データは消さず足すだけ。全文は保存せず、抜粋だけ
- python scripts/merge_inbox.py は実行しない(--help でも実際に動く)
- PRはマージしない(本人が「マージして」と言うまで待つ)
- 本人の名前やメールなど個人情報を外部サービスに送らない

【手順】
1. 一時フォルダに git clone https://github.com/yumatakeshita-dotcom/ai-soukanzu.git し、git checkout -b claude/yt-pc-YYYYMMDD(日付は今日)。CLAUDE.md と docs/yt_pc.md を先に読む。
2. python scripts/yt_pc_queue.py --max 6 を実行し、PCで読む動画の一覧を得る。0本なら報告して終わる。
3. 動画ごとに、ブラウザで動画ページを開き、概要欄から「文字起こしを表示」して全行を読み、一時ファイルに書く。出ない動画は飛ばす。
4. python scripts/yt_pc_save.py ID --title ... --channel ... --date ... --file 一時ファイル で抜粋を保存する。
5. 抜粋に移籍・出資の具体的な話があれば、WebSearchなど別の出典(報道・公式)で確かめる。確かめられたものだけ inbox/moves/YYYY-MM-DD-yt-pc.json・inbox/money/YYYY-MM-DD-yt-pc.json に足す(形式は inbox/moves/2026-11-21-pc-media.json と inbox/money/2026-11-21-pc-media.json と同じ。出典に動画のURLと時刻を書く)。すでに inbox/ や site/data/ にあるものは足さない。
6. git add inbox、commit(末尾に Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>)、git push -u origin ブランチ名。PRはクラウド側が作るので、pushだけでよい(作れるなら下書きで)。
7. 報告する: 読んだ動画の数、文字起こしが出なかった動画、足した手がかり(移籍・出資)、見送った数と理由、pushしたブランチ名。
```

## クラウド側(PRを作る)
PCがpushした `claude/yt-pc-*` ブランチは、クラウドのClaudeが下書きPRにする(祐真さんが「PC側のブランチをPRにして」と言えばよい)。毎朝の調査のプロンプトに `python3 scripts/yt_pc_queue.py` を足すと、順番待ちが毎日更新される(まだ足していない)。
