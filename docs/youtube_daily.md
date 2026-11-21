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

## 日本語・アジアの情報源を追加(2026/11/21)
- ポッドキャスト16番組を `inbox/podcast_feeds.txt` に追加(計35)。日本のVC・スタートアップ(VIVA VC、XTech Ventures、スタートアップ投資TV、令和スタートアップ、Startup Now、川邊の会食、Off Topic、海外スタートアップレポート)、経済ニュース(日経ビジネス、NewsPicks)、アジア(SEA of Startups、Forbes India、韓国の스타인・와우레터、The New Playbook)。Apple Podcastsを国別(jp・kr・tw・cn・in・id・sg)に検索して選んだ。過去120日分(323本)を `pod_daily.py --days 120` で記録
- `media_digest.py` の会社名リストに日本・アジアの名前を足した(手がかり用。足すだけ)
- 確かめて足せたもの: movus technologies のシリーズB(出資1件、PR TIMESの会社リリースで確認)
- **まだ見られないもの(環境の許可に無いホスト)**:
  - ポッドキャスト: api.robotstart.jp(10分でわかるスタートアップ・資金調達ニュース)、hiromaeda.com(前田ヒロ)、www.radionikkei.jp(耳でわかるビジネステック)、rss.listen.style(Catalyst)、feed.pod.co(BRAVE Southeast Asia Tech)、feed.firstory.me(創創燒 TVCA ほか台湾)、feeds.captivate.fm(Prime Venture Partners)
  - 決算資料(IR): www.jpx.co.jp、www.release.tdnet.info、disclosure2.edinet-fsa.go.jp、api.edinet-fsa.go.jp、www.hkexnews.hk、dart.fss.or.kr、mops.twse.com.tw、www.bseindia.com、www.sgx.com、group.softbank
  - 記事: techinasia.com、e27.co、startup-db.com、entrackr.com
  - 許可済みで使えるもの: prtimes.jp、thebridge.jp、dealstreetasia.com、kr-asia.com、inc42.com、nikkei.com
