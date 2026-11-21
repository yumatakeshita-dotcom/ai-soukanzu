# 毎日のYouTube確認(2026/11/21追加)

調査タスクが「YouTubeを見る」を飛ばさないように、道具で必ず通す形にした。

- 見るチャンネルの一覧: `inbox/youtube_channels.txt`(ID|名前|種類|確かめ方。足すだけ)。公式RSSのチャンネル名と一致したものだけ入れている(21件)
- `python3 scripts/yt_daily.py`: 全チャンネルの公式RSSを見て、直近7日の新着(説明文つき)を `inbox/youtube/日付.json` に足す。断られたら30秒・90秒待ってやり直し、それでも見られないチャンネルは理由つきで記録(翌日また見る)。見た動画は `inbox/youtube/seen.txt` に足す
- `python3 scripts/yt_fetch.py --retry-queue` を呼ぶと、この確認も一緒に動く(引き抜き・お金の流れの調査は元から呼んでいるので、プロンプトを変えなくても毎回通る)。止めるときだけ `--no-daily`
- 最後に「YouTube確認: ○/○チャンネル、新着○本」の1行が出る。調査の notes と報告にそのまま書く
- `scripts/watchdog.py` が毎朝 `inbox/youtube/` に今日のファイルがあるか確かめる
- 字幕はクラウドからロボット確認で断られやすいので、RSSの説明文と報道を使う(断られ方をごまかす工夫はしない)

## ポッドキャスト・手がかりのまとめ・Gemini(2026/11/21追加)
- Spotifyには公開RSSがないので、同じ番組の公開RSS(Apple Podcastsの検索で配信元を調べたもの)を使う。一覧は `inbox/podcast_feeds.txt`(20番組。日本語は今のところ Rebuild だけ)
- `python3 scripts/pod_daily.py`: 新着エピソードのタイトル・説明文・日付を `inbox/podcasts/日付.json` に足す(音声の文字起こしはしない)。見られない番組は理由つきで記録して翌日また見る
- `python3 scripts/media_digest.py`: 動画・番組の新着から、移籍・出資などの言葉と会社名があるものを `inbox/media/日付.md` にまとめる。**手がかりなので、出典を開いて確かめてから** inbox/moves・money に足す
- `yt_fetch.py --retry-queue` で上の3つが一緒に動く
- Geminiの調査(`gemini_research.py`)は、最新の手がかりのタイトルをプロンプトに添える(探すのはGemini、事実は検索で別の出典を確かめる)
- 配信元ホストが環境の許可に無いと見られない(2026/11/21に5つを許可して、20番組すべて見られた。以前は 20VC・All-In・Dwarkesh・Latent Space・Odd Lots・Rebuild は2026/11/21時点で未許可。許可すれば自動で見られる): rss.libsyn.com, apple.dwarkesh-podcast.workers.dev, podcast.latent.space, www.omnycontent.com, feeds.rebuild.fm
- 日本語のYouTubeは NewsPicks・ReHacQ・PIVOT・テレ東BIZ・日経・ソフトバンクグループを足した(計27)

## 過去の動画をさかのぼる(2026/11/21追加)
- 公式RSSは直近15本までなので、`python3 scripts/yt_backfill.py [--leads]` がチャンネルの「アップロード一覧」の公開ページから各チャンネル最新100本(動画ID・題名・おおよその古さ)を読み、`inbox/youtube/backfill/日付.json` に足す(足すだけ。取った動画は飛ばす)。2026/11/21の試運転で30/30チャンネル・2,885本。説明文は取らない(題名と会社名が手がかり。確かめは別の出典で)
- `--leads` を付けると、移籍・出資の言葉と会社名がある題名だけ表示する
