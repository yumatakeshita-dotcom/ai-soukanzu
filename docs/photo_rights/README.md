# 顔写真の権利の確認(2026年11月18日)

サイトにある顔写真 **2,019枚** を1枚ずつ、どこから来た写真か・どんなライセンスかを確かめました。
一覧の全部は `photo_licenses.csv`(Excelで開けます)と `photo_licenses.json` にあります。

## 結果のまとめ

| 判定 | 枚数 | どうするか |
|---|---|---|
| OK(パブリックドメイン・CC0 など) | 748 | そのまま使える |
| クレジットが必要(CC BY / CC BY-SA など) | 1,236 | クレジット一覧のページ `site/credits.html` を作り、写真の近くからリンクした(対応ずみ) |
| 要注意(権利がはっきりしない) | 33 | 11/18 に対応ずみ: 8人を差し替え、1人は問題なし、24人はイニシャル表示に(下の一覧) |
| すでに表示を止めている | 2 | 何もしない |

- 写真の置き場所は6か所: `index.html` の初期4社(29枚)、`data/out.js`(120枚)、`faces.json`(427枚)、`faces_wp_0〜2.json`(1,443枚)
- 「自由に使えないことがはっきりした写真」(Wikipedia の「非自由」扱いの画像)は、0枚でした
- 確かめ方: `faces.json` は記録してあった Commons のファイル、`faces_wp` は Wikidata の画像(P18)、`index.html` と `out.js` は Wikipedia 記事の画像を、Wikimedia Commons の記載(ライセンス・作者)で調べた。
  **写真そのものの見た目の照合は、Wikimedia の回数制限で途中までしかできていない。** ただ、前から記録してあった撮影者の名前(53枚分)は、今回調べた作者とほぼ全部一致したので、取り違えは少ないと考えている

## 要注意だった33枚 → 2026年11月18日に対応ずみ
持ち主の判断(「使える写真に差し替える」)で、次のようにした。元の画像は消さず、`replaced_20261118.json` に残してある。

### 自由に使える写真に差し替えた: 8人
- サイト内にすでにあった Commons の写真に: Mira Murati, Ilya Sutskever, Reid Hoffman, Alexandr Wang, Elon Musk(元は X のアイコン)
- 新しく Commons で見つけた写真に: Aravind Srinivas(CC BY 2.0、TechCrunch)、Clément Delangue(CC BY 3.0、SiliconANGLE theCUBE)、Tony West(パブリックドメイン、米司法省の公式写真)

### もともと問題なかった: 1人
- **Vas Narasimhan**(Anthropic の図): 見た目を照らすと、Commons の世界経済フォーラム2025の写真(CC BY 3.0)と同じだった。クレジット一覧に入れた
  - ただし Wikipedia のリンクが別人(スターバックスの Laxman Narasimhan)を指している。写真ではなくリンクの間違いなので、別に直す必要がある

### イニシャル表示にした: 24人
Wikidata・Commons に自由に使える写真が見つからなかった人。写真の代わりに名前の頭文字の丸が出る。
- X のアイコンだった13人: John Schulman, Soumith Chintala, Koray Kavukcuoglu, Oriol Vinyals, Kevin Scott, David Ha, Reynold Xin, Julien Chaumond, Thomas Wolf, Ivan Zhao, Michael Truell, Naoki Aoyagi(青柳直樹), Andy Konwinski
- 会社の公式サイトの写真だった10人: 伊藤 博樹・高橋 健太(Boost Capital)、Ivan Zhang(Cohere)、Andrew Macdonald・Jill Hazelbaker(Uber)、Max Jaderberg(Isomorphic Labs)、出木場 久征・Katrina Lake・峰岸 真澄・Rony Kahan(リクルート)
- **Jack Clark**(Anthropic の図): 写真が人物ではなく講堂の画像だった

あとで Commons に自由な写真が載ったら、差し替えられる(新しい写真はこの一覧にも足す)。

## そのほか気づいたこと
- **表示を止めたはずの4人の写真が、一部の画面で出ている**: Greg Brockman, Dario Amodei, Mark Zuckerberg, Sergey Brin。止める仕組みが名前で探しているのに、Wikidata の人物ページの写真は番号(Q〜)で入っているため。ただし今の写真は CC BY / CC BY-SA で、クレジットを付ければ使える(今回のクレジット一覧に入っている)。止めた理由の写真(Getty Images などの表記があったもの)とは別の写真
- **「肖像権」の注意書きがある写真が186枚**: Commons で「写っている人の許可なく広告などに使わないこと」と注意されているもの。相関図で人物を紹介するのは問題ないが、有料化するときに広告・宣伝に顔写真を使うなら注意
- 商標の注意(カーネル・サンダース、近藤麻理恵)や、歴史上の人物の写真(ナチス時代の人物など)も Wikidata の人物ページに少しある。権利の問題ではないが、気になるなら外せる

## 作り直し方
`python3 scripts/make_photo_credits.py` で `site/credits.html` を作り直せる(元データは `photo_licenses.json`)。
新しい写真を足したときは、Commons のライセンスと作者を確かめてこの一覧にも足す。
