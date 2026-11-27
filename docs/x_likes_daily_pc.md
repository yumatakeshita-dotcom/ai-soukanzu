# 祐真さんのXのいいね・保存(ブックマーク)を毎日読む(PCの定期タスク)

2026-11-26 追加。手作業で2回やった手順(11/26 2:13 と 17:51)を、毎日の定期タスクにしたもの。
やり方は `docs/x_daily_pc.md`(見る一覧の読み取り)に合わせている。

## 何をするか
毎晩21:15(日本時間)、祐真さんのPCのChrome(Xにログイン済み)で `x.com/i/bookmarks`(保存)と、同じ画面の「いいね」のタブを読む。前回の続き(下の「どこまで読んだか」)より新しい投稿だけを見て、AIの会社・人の動き・出資・買収に当たるものを、別の出典(本人の投稿・会社の発表・報道)で確かめてから `inbox/moves/日付-x-likes.json`・`inbox/money/日付-x-likes.json` に足す。ブランチをpushして下書きPRにする。マージは本人が「マージして」と言うまで待つ。

## 守ること
- 読むだけ。いいね・保存の解除、投稿、フォロー、リポスト、返信はしない
- データは消さず、足すだけ。確かめが通ったものだけ足す
- 画像の転載はしない(リンクと説明だけ)。画像に載った一覧(カオスマップなど)は、社名を読んで照らすのには使ってよい
- `python scripts/merge_inbox.py` は実行しない(取り込みは9:13の定期タスクの仕事)
- 個人情報を外部サービスに送らない

## 読み方のコツ(2026-11-26の実績から)
- `x.com/i/bookmarks` を開くと `x.com/i/history` に変わる。上のタブ「ブックマーク」「いいね」をJavaScriptで `[role="tab"]` を探してクリックして切り替える
- `article` を12〜20回スクロールして集める。投稿のID(`/status/数字`)、日付(`time` の `dateTime`)、投稿者、本文の冒頭だけを返す
- **出力に URL・`=`・`?`・`&` が入ると読み取りがブロックされる。** 本文の URL を消し、記号を取り除いてから返す。長い出力は途中で切れるので、10〜15件ずつに分けて返す
- 保存は「保存した順」に並ぶ。前回の一番上の投稿IDまで読めば、それより上が新しい分
- 本文が「さらに表示」で切れる投稿は、投稿のページ(`x.com/名前/status/番号`)を開いて読む
- 人の動きは本人のXのプロフィール(`[data-testid="UserDescription"]`)と本人の投稿で確かめる。本人の投稿で確かめたものは confidence を「本人の発言」にする
- 既にあるかは `git grep -i 名前 origin/main -- inbox site/data` で確かめる

## どこまで読んだか
タスクは終わるたびに、一番上の投稿のIDをここに1行足す(消さない)。
- 2026-11-26 保存: 2125528624359154002(easyjackson、11/25) / いいね: 2125501715852226774(0xjack0x、11/25)
- 2026-11-27 09:15 保存: 2125757521038323822(nayuengin、11/26) / いいね: 2125948792012784070(mylesBaiM、11/26)
- 2026-11-27 09:18 保存: 2125757521038323822(nayuengin、11/26) / いいね: 2125948792012784070(mylesBaiM、11/26)(定期の9:15の回。8:57の回のあと新しい分なし)
- 2026-11-27 15:15 保存: 2125757521038323822(nayuengin、11/26) / いいね: 2126159855371325890(k_matsumaru、11/27)(17:39に実行。保存の新しい分0件、いいね7件で足すものなし)
- 2026-11-27 21:15 保存: 2125757521038323822(nayuengin、11/26) / いいね: 2126159855371325890(k_matsumaru、11/27)(21:37に実行。保存・いいねとも新しい分0件)

## 2026-11-26 2回目の実績
- 保存87件・いいね38件を見て、新しい分は約10件
- 足した: Thariq Shihipar(Anthropic → OpenAI)、Anthony Morris(Anthropicを退社)、カオスマップ・AI 100から出資・買収18件
- 見送り: Cat Wu・Austin Lau(既にある)、Lindy・Rye(出典が食い違う・確かめられない)

## 1日3回動かす(2026-11-26 祐真さんの希望で変更)
9:15・15:15・21:15(日本時間)の3回動く。予定作業は「【毎晩】Xのいいね・保存からAIのつながりを拾う」(x-likes-daily)。頻度は `15 9,15,21 * * *`。
- 重ならないように、毎回「どこまで読んだか」の一番下の行(前の回の一番上の投稿ID)より新しい投稿だけを読む。新しい分が0件なら、目印の行だけ足して終わる
- ブランチは1日1本(`claude/x-likes-YYYYMMDD`)。その日の2回目・3回目は、origin にそのブランチがあれば取り込んで続きを足す(`git fetch origin claude/x-likes-YYYYMMDD` のあと checkout)。同じブランチに下書きPRがすでにあれば、新しいPRは作らない
- ファイル名に時刻を付ける: `inbox/moves/YYYY-MM-DD-x-likes-HHMM.json`、`inbox/money/YYYY-MM-DD-x-likes-HHMM.json`(HHMMは 0915・1515・2115)
- 目印の行には時刻も書く(例: `- 2026-11-27 09:15 保存: 番号 / いいね: 番号`)

## いいね・保存した人の印(2026-11-26追加)
相関図の人物カードの「X @名前」の横に「♡ いいね・保存した人」の印を出す。データは `site/index.html` の `/*XLIKED_START*/〜/*XLIKED_END*/`(`XLIKED`)。
- 足し方: `python scripts/x_liked_add.py アカウント:種類:日付 ...`(種類 b=保存 l=いいね bl=両方。足すだけで、すでにある人は書き換えない)
- 足すのは、AIに関係するアカウントだけ(相関図の人物のX、`inbox/x_accounts.txt` の見る一覧、相関図に足した手がかりの投稿者)。友人や関係のないアカウントは公開ページに出さないため足さない
- 相関図の人物のXアカウントは、index.html の会社ごとの `const X={...}` と `site/x_info.json` にある
- 2026-11-26: 保存約115件・いいね直近約760件(367アカウント)を照らし、15アカウントに印を付けた(相関図の人物ではイーロン・マスク、ミラ・ムラティ、青柳直樹など)

## 定期タスクの登録(2026-11-26時点で未登録)
Claudeから定期タスクを作ろうとしたが、自動モードの安全確認に断られた。祐真さんがPCのClaudeアプリで登録する。
1. Claudeアプリの「予定作業」(Scheduled)で新しい作業を作る
2. 名前: `【毎晩】Xのいいね・保存からAIのつながりを拾う`
3. 頻度: 毎日 21:15(`15 21 * * *`)
4. 本文: 下の四角の中をそのまま貼る

```text
あなたは祐真さんのPCで動く。祐真さんのXのいいね・保存(ブックマーク)の新しい分から、AIの会社・人の動き(移籍)・出資・買収を拾い、確かめてから相関図リポジトリ(GitHub: yumatakeshita-dotcom/ai-soukanzu)に足す。報告は平易な日本語で。

【守ること】
- Xは読むだけ。いいね・保存の解除、投稿、フォロー、リポスト、返信はしない
- データは消さず足すだけ。別の出典で確かめが通ったものだけ足す
- 画像は転載しない(リンクと説明だけ)
- python scripts/merge_inbox.py は実行しない
- PRはマージしない(本人が「マージして」と言うまで待つ)
- 個人情報を外部サービスに送らない

【手順】
1. git fetch origin のあと、origin/main から claude/x-likes-YYYYMMDD(今日の日付)のブランチを作る。CLAUDE.md、docs/x_likes_daily_pc.md、docs/x_daily_pc.md を先に読む。docs/x_likes_daily_pc.md の「どこまで読んだか」の一番下の行が前回の続きの目印。
2. ChromeのClaude拡張(mcp__claude-in-chrome__*。ToolSearchでまとめて読み込む)で x.com/i/bookmarks を開き、「読み方のコツ」どおりに保存を読む。続けて「いいね」のタブに切り替えて読む。目印より新しい分だけを見る。
3. AIの会社・人の動き・出資・買収に当たるものを選び、git grep -i 名前 origin/main -- inbox site/data で既にあれば足さない。
4. 人の動きは本人のXのプロフィールと投稿で、出資・買収は会社の発表か報道の本文で確かめる。移籍先が確かめられない退社は to を「(未発表)」にする。
5. 通ったものを inbox/moves/YYYY-MM-DD-x-likes.json と inbox/money/YYYY-MM-DD-x-likes.json に足す(形式は inbox/moves/2026-11-26-x-bookmarks-2.json と inbox/money/2026-11-26-x-bookmarks-3.json と同じ)。「どこまで読んだか」に今回の一番上の投稿IDを1行足す(0件でも足す)。
5b. 今回の新しい分の投稿者のうち、AIに関係するアカウント(相関図の人物のX・inbox/x_accounts.txt の見る一覧・足した手がかりの投稿者)を python scripts/x_liked_add.py アカウント:種類:日付 で「いいね・保存した人」の印に足す(足すだけ。友人など関係のないアカウントは足さない)。
6. commit(作者 Claude <noreply@anthropic.com>、末尾に Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>)、push。足したものがあれば、git credential fill のトークンで GitHub API に下書きPR(draft:true, base:main)を作り、yumatakeshita-dotcom を担当者にする。本文の先頭に次の2行、末尾に 🤖 Generated with [Claude Code](https://claude.com/claude-code):
<!-- claude-projects-attribution: {"github_login":"yumatakeshita-dotcom"} -->
_Requested by **祐真** · [project thread](https://claude.ai/code/project/chan_01TAs4swRT2S9aZ3shCp4iCo?thread=cmsg_01TAs4swRT2S9aZ3shCp4iCo5oXDveEkoiGsRWYVfRVwCP)_
7. 開いたタブを閉じる。
8. 報告: 見た件数、新しい分の件数、足した数と中身、見送った数と理由、PRのURL。最後に次の候補を2〜3個。
```
