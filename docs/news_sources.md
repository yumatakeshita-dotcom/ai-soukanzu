# 報道サイトの読める・読めない一覧(2026/11/21確認)

クラウド環境は、環境設定の許可リストにあるサイトにしかつながらない。追加したあとは本文が読めるか試して、ここに足す。

## 本文が読めた(確認済み)
- 英語: techcrunch.com(記事・RSS)、news.crunchbase.com、www.theverge.com、arstechnica.com、siliconangle.com、www.semafor.com(短め)、www.prnewswire.com(RSSのみ確認)、inc42.com、www.dealstreetasia.com(一部は購読者限定)、www.business-standard.com
- 日本語: gigazine.net、www.itmedia.co.jp、news.mynavi.jp、ai.watch.impress.co.jp、www.zaikei.co.jp、thebridge.jp、prtimes.jp、note.com
- 見出しと冒頭のみ(本文は有料): www.nikkei.com、xtech.nikkei.com
- RSSは200(記事本文は未確認): toyokeizai.net、www.scmp.com

## 読めない(許可リストから外してよい)
venturebeat.com(429)、www.axios.com(403)、www.cnbc.com(403)、www.reuters.com(401)、www.businesswire.com(接続できない)、e27.co(403)、dealroom.co(429)、www.globenewswire.com(403)、xenospectrum.com(403)、fourweekmba.com(403)、www.techflowpost.com(403)

## 再確認待ち
forbesjapan.com、ledge.ai、kr-asia.com(トップは開く。RSSは404。記事の取得を次回試す)

## 有料壁のため追加しない
Bloomberg、FT、WSJ、The Information、Business Insider、Fortune、Nikkei Asia、NewsPicks、Tech in Asia

## 毎朝のニュース集めに足したもの
`scripts/fetch_relnews.py` の FEEDS に、Crunchbase News・The Verge(AI)・Ars Technica(AI)・SiliconANGLE のRSSを足した(2026/11/21)。続けて日本語の GIGAZINE・東洋経済オンラインのRSSも足した(同日)。

2026/11/22: GIGAZINE・東洋経済オンラインのRSSは、AI関連の見出しが東洋経済38件中3件・GIGAZINE11件中2件だけだったので、ニュース集めから外した(すでに入った見出しは残す)。
