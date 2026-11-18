# 人物のXの読み直し手順(毎日45人(約240人を約5〜6日で一巡)。定期タスク x-posts-daily-refresh が毎朝7時台に実行)

目的: 人物ページ・企業ページの「最近の発信」を新しく保つ。Xの利用規約と負荷を考え、**手作業のペース**(1アカウント6秒あけ、1バッチ9人まで)で行う。APIは使わない(無料の範囲)。

## 1回の流れ(約25分、27バッチ)
1. 対象を決める: `python x_refresh.py next 9`(最後に読んだ日が古い順・有名な順)。まず 'status' で全体を確認。
2. Claude in Chrome で、各アカウントを `https://x.com/<h>` を開き、6秒待って `eval(localStorage.hv)('<h>',2)`(ピン留め・リポストを除く最新2件)。localStorage の 'hv' が無ければ、同じ読み取りコードを入れ直す(add_x_batch.py と同じ形の [アカウント,日付,抜粋,パス])。
3. 結果を `xh/bNN.json` に書き、`python add_x_batch.py` で watch.sqlite に入れる(新しい投稿だけ。2026-08以降のみ・抜粋110字まで・本文が空のものは入れない)。
4. 読んだ人を印する: `python x_refresh.py mark <h1> <h2> ...`(0件・古い投稿だった人も)。
5. 数バッチごと、または最後に反映: `python -I build_site_assets.py houjin.sqlite <site>` → `python -I top100_apply.py`(--push は付けない。build で消える注目100人の人物を手元に戻す) → `cd ../relationship-map-site; python sync_people.py`(変わった表だけ送る。person_feed 約400行) → `python sync_events.py`。画像や表が変わらなければ `wrangler deploy` は不要(コードを変えたときだけ)。

## 注意
- 警告(ログインを求められる、アクセス制限、CAPTCHA)が出たら止めて報告。回避しない。
- 1バッチ10件を超えるとブラウザの応答が切れる。9件まで。
- 同名の別人のアカウント、収監中などで本人の投稿と確認できないものは入れない(x_checked.json に残す)。
- D1の無料枠: 書き込み1日10万行。通常の同期は約400行。人物表を作り直すとき(sync_people が person など)は約2万行/回なので、1日に何度もやらない。
- YouTube(出演)は別の手順: 検索 `results?search_query=<名前>&sp=CAI%253D` を `localStorage.hy` で読み、`yh/*.json` → `add_yt_batch.py`。月1回で足りる。
- 自動実行について: ブラウザ操作が要るため完全な無人化はしていない。定期実行にするなら、週1回「Xを読み直して」とだけ依頼するか、Claudeの定期タスクにする。

- 【重要】sync_people.py は、既定では person_feed だけ送る(安全装置)。person・person_role・person_social・img を丸ごと入れ替えると、D1にだけある追加人物(注目100人・GAFAM/VC・ゲスト)が消える。それらを送るのは、restore100.py・gafam_people.py などで追加人物を手元に戻したうえで --all を付けたときだけ。2026-11-17に一度、これで注目100人が消え、復旧した。
