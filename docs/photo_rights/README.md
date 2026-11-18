# 顔写真の権利の確認(2026年11月18日)

サイトにある顔写真 **2,019枚** を1枚ずつ、どこから来た写真か・どんなライセンスかを確かめました。
一覧の全部は `photo_licenses.csv`(Excelで開けます)と `photo_licenses.json` にあります。

## 結果のまとめ

| 判定 | 枚数 | どうするか |
|---|---|---|
| OK(パブリックドメイン・CC0 など) | 748 | そのまま使える |
| クレジットが必要(CC BY / CC BY-SA など) | 1,236 | クレジット一覧のページ `site/credits.html` を作り、写真の近くからリンクした(対応ずみ) |
| 要注意(権利がはっきりしない) | 33 | 下の一覧。消さずに残してある。差し替えは持ち主の判断を待つ |
| すでに表示を止めている | 2 | 何もしない |

- 写真の置き場所は6か所: `index.html` の初期4社(29枚)、`data/out.js`(120枚)、`faces.json`(427枚)、`faces_wp_0〜2.json`(1,443枚)
- 「自由に使えないことがはっきりした写真」(Wikipedia の「非自由」扱いの画像)は、0枚でした
- 確かめ方: `faces.json` は記録してあった Commons のファイル、`faces_wp` は Wikidata の画像(P18)、`index.html` と `out.js` は Wikipedia 記事の画像を、Wikimedia Commons の記載(ライセンス・作者)で調べた。
  **写真そのものの見た目の照合は、Wikimedia の回数制限で途中までしかできていない。** ただ、前から記録してあった撮影者の名前(53枚分)は、今回調べた作者とほぼ全部一致したので、取り違えは少ないと考えている

## 要注意の33枚

### X(旧Twitter)のプロフィール画像: 20枚
本人のXのアイコンを使っている。自由に使えるライセンスではないので、広く公開する前に差し替えたほうがよい。
Mira Murati, John Schulman, Soumith Chintala, Ilya Sutskever, Koray Kavukcuoglu, Oriol Vinyals, Kevin Scott, Reid Hoffman, David Ha, Aravind Srinivas, Alexandr Wang, Reynold Xin, Clément Delangue, Julien Chaumond, Thomas Wolf, Elon Musk, Ivan Zhao, Michael Truell, Naoki Aoyagi(青柳直樹), Andy Konwinski

- このうち **Mira Murati, Ilya Sutskever, Reid Hoffman, Alexandr Wang, Elon Musk の5人** は、自由に使える Commons の写真がすでにサイト内にある(多くの画面ではそちらが先に出る)。X の画像を使わないようにするだけで済む

### 会社の公式サイトの写真: 11枚
会社の紹介ページの写真。会社に著作権があり、許可なく使うと問題になりうる。
伊藤 博樹・高橋 健太(Boost Capital)、Ivan Zhang(Cohere)、Andrew Macdonald・Jill Hazelbaker・Tony West(Uber)、Max Jaderberg(Isomorphic Labs)、出木場 久征・Katrina Lake・峰岸 真澄・Rony Kahan(リクルート)

### 出どころがわからない: 2枚(本体 index.html の Anthropic の図)
- **Vas Narasimhan**: 写真の記録がない。しかも Wikipedia のリンクが別人(スターバックスの Laxman Narasimhan)を指しているので、**写真も別人の可能性がある**。確認が必要
- **Jack Clark**: 日本語版 Wikipedia の記事には写真がなく、出どころがわからない

### 差し替えの案(おすすめ順)
1. **イニシャル表示にする(おすすめ)**: 今も写真がない人はイニシャルの丸で出ている。いちばん早く、安全
2. Commons で自由なライセンスの写真を探して差し替える(5人はすでにある。ほかの人は見つかったものから)
3. 本人や会社に使用の許可をもらう(手間がかかる)

## そのほか気づいたこと
- **表示を止めたはずの4人の写真が、一部の画面で出ている**: Greg Brockman, Dario Amodei, Mark Zuckerberg, Sergey Brin。止める仕組みが名前で探しているのに、Wikidata の人物ページの写真は番号(Q〜)で入っているため。ただし今の写真は CC BY / CC BY-SA で、クレジットを付ければ使える(今回のクレジット一覧に入っている)。止めた理由の写真(Getty Images などの表記があったもの)とは別の写真
- **「肖像権」の注意書きがある写真が186枚**: Commons で「写っている人の許可なく広告などに使わないこと」と注意されているもの。相関図で人物を紹介するのは問題ないが、有料化するときに広告・宣伝に顔写真を使うなら注意
- 商標の注意(カーネル・サンダース、近藤麻理恵)や、歴史上の人物の写真(ナチス時代の人物など)も Wikidata の人物ページに少しある。権利の問題ではないが、気になるなら外せる

## 作り直し方
`python3 scripts/make_photo_credits.py` で `site/credits.html` を作り直せる(元データは `photo_licenses.json`)。
新しい写真を足したときは、Commons のライセンスと作者を確かめてこの一覧にも足す。
