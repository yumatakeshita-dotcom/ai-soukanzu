# プロ会員(有料化)の仕組み(2026/11/20追加)

「地図は無料、資料として持ち出す機能は有料」にするための土台。**この変更だけでは、公開サイトの動きは何も変わらない**(`site/pro/config.js` の `gate` が false のため)。

## 何を作ったか
| 場所 | 中身 |
|---|---|
| `site/pro/index.html` | 料金ページ。決済リンクが空のあいだは「先行案内に登録」、入ると決済ボタンに切り替わる。顔写真は使わない |
| `site/pro/config.js` | 設定(`gate` `checkoutUrl` 価格)。ここだけ直せば動きが変わる |
| `site/pro/gate.js` | `gate:true` のとき、確かな版・営業資料の印刷/保存/コピーをアクセスキーのある人だけにする。既存コードは触らない |
| `site/index.html` | `<script>` を2行足しただけ |
| `tools/cloudflare/relmap/worker.mjs` | `/api/pro/waitlist` `/api/pro/verify`。D1 が付いていなければ 503(ほかの機能に影響なし) |
| `tools/cloudflare/relmap/pro_schema.sql` | D1 `kigyo-pro` の表(先行案内・アクセスキーのハッシュ) |
| `tools/cloudflare/relmap/pro_issue.py` | アクセスキーを1つ作る(法人の請求書払いなど、最初の会員用) |

## 公開までの手順(持ち主の確認が要るものに ★)
1. ★ Stripe アカウントを作り、Payment Link を作る → `config.js` の `checkoutUrl` に入れる
2. ★ D1 `kigyo-pro` を作り、`pro_schema.sql` を流す(CREATE は d1_add.py が拒否するので、ダッシュボードか wrangler で1回だけ)
3. ★ `python3 tools/cloudflare/relmap/deploy_worker.py` で Worker を置き直す(D1 があれば自動で束ねる)
4. 料金ページ `/pro/` が見えること、先行案内が登録できることを確かめる
5. 決済から会員になるまでは最初は手作業: Stripe で入金を確認 → `pro_issue.py` でキー作成 → メールで渡す(Stripe の webhook での自動化は、購入が出てから)
6. 準備ができたら `config.js` の `gate` を true にして push

## 決めてあること・まだ弱いところ
- 価格は仮(個人 月980円 / 法人 月9,800円)。反応を見て変える
- **制限はブラウザ側の鍵**。詳しい人は回避できる。データ自体が公開情報なので、守るのは「手間なく出典つき資料にできること」。弱くても最初は十分で、買われてからサーバー側の生成に移す
- 回数制限(レート制限)は未実装。先行案内の連投が目立つなら Cloudflare 側の設定で止める
- 免責(投資・法務の助言ではない)は料金ページに書いてある
