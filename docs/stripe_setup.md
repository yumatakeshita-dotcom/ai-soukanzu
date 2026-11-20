# Stripe で課金する手順(2026/11/20追加)

方式は **Payment Link + webhook**。Stripe Connect(他人への分配)は要りません。
秘密の鍵は **コードにもチャットにも書かず**、Worker の「秘密設定」に入れます。公開用の `pk_test_` は Payment Link 方式では使いません。

> ⚠ このクラウドから Stripe のサイトを開けないため、公式ドキュメントは確認していません。以下は知識ベースで、**★が付いた点は実際に画面で確かめてください**。

## 全体の流れ
1. 買う人が Payment Link で支払う → 2. Stripe が webhook(`/api/stripe/webhook`)を呼ぶ → 3. Worker が署名を確かめ、アクセスキーのハッシュを D1 `pro_keys` に足す → 4. 購入後のページ `/pro/thanks.html` が、その人のブラウザにキーを表示・保存する

- キーは `PRO_KEY_SECRET` と購入ID(定期購入ID `sub_…`)から**計算で作る**ので、保存するのはハッシュだけ。webhook が2回届いても同じキーになり、二重に発行されない
- 解約(`customer.subscription.deleted`)・支払い失敗(`…updated` で past_due/unpaid)・全額返金(`charge.refunded`)・チャージバック(`charge.dispute.created`)で `status` が変わり、`active` 以外は使えなくなる。支払いが戻れば `active` に戻る
- メールアドレスは保存しない(Stripeの顧客IDだけ)

## 手順(★=持ち主の操作)
1. ★ Stripe(テストモード)で「商品」を2つ作る: 個人 月980円、法人 月9,800円(定期購入)。価格は仮。法人は 5,000円以上で自動的に法人プラン扱い(`worker.mjs` の `BUSINESS_MIN_AMOUNT`)
2. ★ 各商品で Payment Link を作る。「支払い後の動作」で「確認ページを表示しない/カスタムURLへ移動」を選び、`https://kigyo-relmap.yuma-takeshita.workers.dev/pro/thanks.html?session_id={CHECKOUT_SESSION_ID}` を入れる。
   ★ **Payment Link の移動先URLで `{CHECKOUT_SESSION_ID}` が使えるかは未確認**。使えない場合は、Checkout Session を作る小さなAPIに切り替える(その場合は私が足します)。それまでは、購入後に `pro_issue.py` で手作業発行でも動きます
3. ★ D1 に表を足す: `pro_schema.sql` のあとに `pro_stripe.sql` を流す(足すだけ。ALTER は1回だけ)
4. ★ Stripe の「開発者 → Webhook」で、送り先 `https://kigyo-relmap.yuma-takeshita.workers.dev/api/stripe/webhook`、イベントは次の7つを選ぶ:
   `checkout.session.completed` `checkout.session.async_payment_succeeded` `customer.subscription.updated` `customer.subscription.deleted` `charge.refunded` `charge.dispute.created`
   → 表示される署名の秘密(`whsec_…`)を控える
5. ★ Worker の秘密設定に3つ入れる(Cloudflare ダッシュボードの Worker → 設定 → 変数とシークレット。「シークレット」で):
   - `STRIPE_WEBHOOK_SECRET` = 上の `whsec_…`
   - `STRIPE_SECRET_KEY` = テスト用の `sk_test_…`(購入ページがStripeに「支払い済みか」を聞くため。できれば権限を絞った制限付きキー(Checkout Sessions の読み取りだけ)★)
   - `PRO_KEY_SECRET` = ランダムな長い文字列(例: `python3 -c "import secrets;print(secrets.token_urlsafe(48))"`)。**あとで変えると、すでに渡したキーが全部無効になる**
   `deploy_worker.py` は秘密設定を残したまま置き直す(`keep_bindings`)
6. ★ `python3 tools/cloudflare/relmap/deploy_worker.py` で Worker を置き直す
7. ★ `site/pro/config.js` の `checkoutUrl` に Payment Link(`https://buy.stripe.com/test_…`)を入れて push。個人・法人で分けるときは、料金ページのボタンを2つにする(私が直します)

## テストモードでの確認
1. 料金ページ `/pro/` の購入ボタン → Stripe のテスト決済(カード番号 `4242 4242 4242 4242`、期限は未来の日付、CVCは任意の3桁)
2. 支払い後に `thanks.html` にアクセスキーが出る。コピーしておく
3. D1 に行が1件増えている(`SELECT plan,status,note FROM pro_keys`)。キーそのものは入っていない
4. Stripe のダッシュボードで、webhook の「配信」が 200 になっている。「再送」しても行が増えない
5. `config.js` を `gate:true` にしたローカル(または別環境)で、確かな版の印刷が、キーなしだと止まり、キーありで通る
6. テストの定期購入を解約 → `status` が `canceled` になり、同じキーが使えなくなる
7. テスト決済を全額返金 → `status` が `refunded`
8. 本番に切り替えるときは、本番モードで 1〜2 の商品・Payment Link・Webhook・`sk_live_`/`whsec_` を作り直し、秘密設定を入れ替える(テストと本番は鍵も Webhook も別)

## わかっていないこと・弱いところ
- Payment Link の移動先に `{CHECKOUT_SESSION_ID}` が使えるか(★)
- 日本の消費税・インボイス表示(Stripe Tax の設定)は未検討。事業として始める前に税理士さんへ
- `/api/pro/claim` は、購入ページのURLを知っている人ならキーが見られる(session_id は推測できない長い文字列)。URLを共有しないよう案内する
- 返金は「全額」のときだけ無効にする。一部返金は何もしない
