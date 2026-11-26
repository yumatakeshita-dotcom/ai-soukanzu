# 人物の経歴の薄さを埋める(2026/11/24追加)

きっかけ: 「Boris Chernyはすごく有名なのに、名前と肩書き1行しか入っていない」という指摘。同じように薄い人物を数えて、有名な順に埋める。

## 使う道具
- `python3 scripts/person_thin.py [--top 30] [--dump ファイル]` … 相関図の人物(約4,700人)を数え、薄い人を知名度の高い順に `inbox/people_thin/latest.json`・`latest.md`(と日付つき)に書く。読むだけ(サイトは変えない)。
  - 薄さ = 説明文の短さ・経歴(CAREER)の行数・出典の有無(3点以上)。深掘りプロフィール(`PROFILES`)がある人は外す。
  - 知名度 = 主要なAI・半導体の図に出る数×5 + その他の図×1.5 + つながりの線×0.7 + ニュース見出し(上限30)×2 + 肩書き(CEO・創業者など)3 + Wikidata2。
  - `inbox/people_thin/skip.json`(名前→理由・日付)に書いた人は次回から一覧から外れる(確かめられなかった人・同名の別人など。消さない)。
- `python3 scripts/person_fill.py [--dry-run]` … `inbox/people_thin/fills/*.json`(出典のページを開いて確かめた人だけ)を、本体(site/index.html)の各図の人物に足す。説明文は新しい文を先頭に、もとの文を後ろに残す。経歴は足りない行だけ足す。出典は `/*PF_DS_START*/〜/*PF_DS_END*/` の DS に足し、人物の `src` に付ける(確かさの印が付く)。何度動かしても同じ。

## 毎日の仕組み
`scripts/research_queue.py build` が、薄い人物の上位10人を宿題リストに足す(種類「薄い人物」、優先度11、重要度ランキングの次)。毎朝のGemini調査が先頭から1件ずつ調べ、確かめを通ったものが inbox に入る。Claude が出典のページを開いて確かめたら、`fills/日付-x.json` に書いて `person_fill.py` を動かす。

## 確かめ方の決まり
1. 本人のX・GitHub・公式ページ → 2. SEC書類・公式発表 → 3. 英語版Wikipedia・報道の本文。Geminiの答えは手がかりだけ。
2. 同名の別人に注意(Rahul Patil・Denise Dresser・Luke Metz は Wikipedia では別人だった)。
3. 英語版Wikipediaだけで確かめたものは、確かさの印を「報道」(`r`)にし、説明の末尾に出典と日付を書く。公式で確かめたら `fills` の `src` の3番目を `o`/`f`/`s` にして足し直す。
4. 争いのある話(告発・訴訟の主張など)は、本文で確かめられても足さない。

## 2026/11/24の結果
28人を足した: Jack Ma、Andy Konwinski、Rajeev Misra、Sebastian Thrun、Daniel Ek、Bill McDermott、Frank Slootman、Adam D'Angelo、Diane Greene、Dick Costolo、Lip-Bu Tan、Garrett Camp、Nick Frosst、Luke Metz(本人のX)、Dara Khosrowshahi、Dmitri Dolgov、Marcelo Claure、Moxie Marlinspike、Parag Agrawal、Wojciech Zaremba、Ashish Vaswani、Helen Toner、Ion Stoica、Matei Zaharia、John Collison、Luis von Ahn、Bret Johnsen、Jill Hazelbaker。
確かめられず `skip.json` に残した: Rahul Patil、Denise Dresser、Cal Henderson、Ruoming Pang。

## 2026/11/25の追加
- 本人のXの自己紹介で確かめ直した8人(Zaremba、Toner、D'Angelo、Camp、Khosrowshahi、Collison、Frosst、Zaharia)に「本人」の出典を足した(`python3 scripts/person_xsrc.py`。入力は `inbox/people_thin/xsrc/`。自己紹介が説明文の中心と合う人だけ。説明文の事実の出どころは Wikipedia のまま)
- 経歴を18人足した(合計46人): Biz Stone、Reynold Xin、Francis deSouza、Lidiane Jones、Lucy Guo、Cliff Obrecht、Tom Blomfield、Danny Rimer、John Krafcik、Mamoon Hamid、Ned Segal、Tekedra Mawakana、Aman Sanger、Denis Yarats、Kyle Kosic、Shona Brown、Indra Nooyi
- 顔写真: 27人のうち17人はすでに写真があった。足りない10人(Rajeev Misra、Bill McDermott、Diane Greene、Luke Metz、Moxie Marlinspike、Wojciech Zaremba、Ashish Vaswani、Helen Toner、Luis von Ahn、Bret Johnsen)は、**Wikimedia Commons(commons.wikimedia.org と upload.wikimedia.org)がこの環境の許可リストに無く、ライセンスの確認も画像の取得もできなかった**ので足していない。許可したあと `python3 scripts/person_photo.py "Helen Toner" ...` で足せる(自由なライセンスだけ・足すだけ・すでにある写真は触らない。そのあと `python3 scripts/make_photo_credits.py`。`site/faces.json` と `site/credits.html` を変えたら共有リンクにも公開)
