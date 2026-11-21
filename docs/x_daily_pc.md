# 毎朝のXの読み取り(PCの定期タスク)

2026-11-21 追加。

## 何をするか
祐真さんのPCのChrome(Xにログイン済み)で、`inbox/x_accounts.txt` のアカウントの直近の投稿を読み、移籍・出資の手がかりを拾う。報道などの別の出典で確かめられたものだけ `inbox/moves/` と `inbox/money/` に足し、ブランチをpushしてPRを作る。マージは本人が「マージして」と言うまで待つ。

## 守ること
- 読むだけ。投稿・いいね・フォロー・リポスト・返信はしない
- データは消さず、足すだけ
- 確かめが通っていない手がかりは足さない(足す場合は「協議中・未確定」と書く)
- `python scripts/merge_inbox.py` は実行しない(取り込みは9:13の定期タスクの仕事。`--help` でも実行される)

## 読み方のコツ
- ChromeのClaude拡張を使う。`x.com/アカウント` を開き、3〜4回スクロールして `article` を読む
- 日付は `time` タグの `dateTime`、投稿のURLは `time` を囲むリンクから取る
- 移籍・出資のことばだけに絞ると速い(join・hire・appoint・raise・funding・series・valuation・acquire、調達・出資・買収・就任)
- 出力にクッキーやURLのクエリが入ると読み取りがブロックされるので、投稿の本文と日付とURLだけを返す
- 約130アカウントを毎回全部は読まない。報道系・主要人物・日本のスタートアップ報道を毎回、VCなどは曜日で分けて回す
- 2026-11-21の実績: 約40アカウントを読み、移籍1件・出資3件が拾えた。VC公式は人事・出資の投稿が少なく、報道系と創業者本人が多い

## どのアカウントを読むか(2026-11-21 決定)
`inbox/x_accounts.txt`(約114件)を2つに分ける。アカウントが増えたら、毎日の分に入れない限り、下の表の「その他」に自動で回る(曜日は一覧の並び順を7で割った余り)。

**毎日読む(38件。報道系・主要人物・日本のスタートアップ報道)**
@sama @gdb @miramurati @alexandr_wang @AnthropicAI @OpenAI @xai @elonmusk @jackclarkSF @DarioAmodei @amir @aaronpholmes @ZeffMax @alexeheath @Kantrowitz @theinformation @business @eladgil @TechCrunch @Techmeme @Reuters @SakanaAILabs @nikkei_startup @thebridge_jp @a16z @sequoia @lightspeedvp @Kepple_jp @coral_capital @JapanVenture @WSJ @axios @semafor @NikkeiAsia @nikkei @Crunchbase @SiliconANGLE @geekwire

**曜日ごとに回す(その他76件。1日あたり約11件)**
| 曜日 | アカウント |
|---|---|
| 月 | @ecommartinez @garrytan @tech_eu @EricNewcomer @saranormous @ylecun @paulg @tdnet_jp @JETRO_info @IndexVentures @dwarkesh_sp |
| 火 | @tmiyatake1 @SemiAnalysis_ @HarryStebbings @Siftedeu @sarahcat21 @AndrewYNg @bhorowitz @startupnews_jp @UTEC_official @Accel @NFX |
| 水 | @qihang_zeng6688 @dylan522p @collision @ycombinator @bgurley @JeffDean @reidhoffman @japantimes @globalbrains_jp @founders_fund @hunterwalk |
| 木 | @USAnt_IDEA @pmarca @GoogleDeepMind @MistralAI @PreferredNet @mustafasuleyman @vkhosla @SoraNews24 @hardmaru @PitchBook @Jason |
| 金 | @ctgptlb @nvidia @demishassabis @AravSrinivas @JPStartups @satyanadella @sogyotecho @JapanTodayNews @drfeifei @naval @TurnerNovak |
| 土 | @bizlab09 @crunchbasenews @pushmeet @karpathy @chamath @sundarpichai @kabutan_jp @NHKWORLD_News @kleinerperkins @balajis @jasonlk |
| 日 | @SierraPlatform @thenextweb @james_riney @ilyasut @DavidSacks @patrickc @Nikkei_Business @e27co @GreylockVC @sarahguo |

曜日の分けかた: 一覧から「毎日読む」を除いた残りを、上から順に月・火・水・木・金・土・日・月…と1件ずつ割り当てる。一覧に足したアカウントは、種類(moves, money)に関わらずこの規則で割り当てる。

## 定期タスク(まだ作っていない。祐真さんがPCのClaudeアプリで登録する)
2026-11-21に、クラウド側のClaudeから予定作業の作成を試したが、自動モードの安全確認に断られて作れていない。アプリが閉じていたら、次に開いたときに動く。

### 登録のしかた
1. Claudeアプリの「予定作業」(Scheduled)を開き、新しい作業を作る
2. 名前: `毎朝 Xの見る一覧から移籍・出資の手がかりを拾う`
3. 頻度: 毎日 8:35(`35 8 * * *`)
4. 本文: 下の四角の中を、そのまま貼る

```text
あなたは祐真さんのPCで動く。相関図リポジトリ(GitHub: yumatakeshita-dotcom/ai-soukanzu)に、Xの見る一覧から拾った移籍・出資の手がかりを足す。報告は平易な日本語で。

【守ること】
- Xは読むだけ。投稿・いいね・フォロー・リポスト・返信はしない
- データは消さず足すだけ。確かめが通ったものだけ足す
- python scripts/merge_inbox.py は実行しない(--help でも実際に動く。取り込みは別の定期タスクの仕事)
- PRはマージしない(本人が「マージして」と言うまで待つ)
- 本人の名前やメールなど個人情報を外部サービスに送らない

【手順】
1. 一時フォルダに git clone https://github.com/yumatakeshita-dotcom/ai-soukanzu.git し、git checkout -b claude/x-timeline-YYYYMMDD(日付は今日)。CLAUDE.md と docs/x_daily_pc.md を先に読む。
2. docs/x_daily_pc.md の「どのアカウントを読むか」に従い、毎日の分と、今日の曜日の分を読む。
3. ChromeのClaude拡張(mcp__claude-in-chrome__*。ToolSearchでまとめて読み込む)で、tabs_context_mcp のあと新しいタブを作り、x.com/アカウント を開く。3〜4回スクロールして article を読み、日付(timeのdateTime)・投稿URL・本文冒頭だけを返すJavaScriptで、移籍・出資のことば(join, hire, appoint, leave, raise, funding, series, valuation, acquire, 調達, 出資, 買収, 就任)に当たる投稿だけ拾う。出力にクッキーやURLのクエリを含めない(ブロックされる)。終わったらタブを閉じる。
4. 手がかりごとに、WebSearchなど別の出典(報道・本人の投稿・公式発表)で確かめる。すでに inbox/ や site/data/ にあるもの(grepで確認)は足さない。確かめられないもの・出典が1件だけの協議中の話は足さない(足すなら note に「協議中・未確定」と明記)。
5. 通ったものを inbox/moves/YYYY-MM-DD-x-pc.json と inbox/money/YYYY-MM-DD-x-pc.json に足す。形式は inbox/moves/2026-11-21-x-pc.json と inbox/money/2026-11-21-x-pc.json と同じ。0件ならファイルは作らず報告だけ。
6. git add inbox、commit(末尾に Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>)、git push -u origin ブランチ名。下書きPRをGitHub APIで作る(gh は入っていない): git credential fill で得たトークンで POST https://api.github.com/repos/yumatakeshita-dotcom/ai-soukanzu/pulls (draft:true, base:main)。本文の先頭に次の2行、末尾に 🤖 Generated with [Claude Code](https://claude.com/claude-code) を入れる:
<!-- claude-projects-attribution: {"github_login":"yumatakeshita-dotcom"} -->
_Requested by **祐真** · [project thread](https://claude.ai/code/project/chan_01TAs4swRT2S9aZ3shCp4iCo?thread=cmsg_01TAs4swRT2S9aZ3shCp4iCo3v6Wp68JAGsDkxAHB95fjt)_
7. 報告する: 読んだ数、足した数(移籍・出資)、見送った数と理由、PRのURL、読めなかったアカウント。
```
