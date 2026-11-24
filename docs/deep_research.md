# 投稿の深掘りリサーチ(段階式)の手順(2026/11/24 作成)

「人物を並べただけで深さがない」という指摘を受けて、note記事1本ごとに、調べる→カードにする→つなぐ→穴を埋める→書く→照らす、の6段で作る方式にした。
**書いてよいのは事実カードにあることだけ。** カードにない話は書かない(書くなら★を付ける)。

道具: `scripts/deep_post.py`(サイト・inbox は変えない。足すだけ)
置き場: `posts/research/<日付>_<テーマ>/`(消さない。直すときは新しい行に足す)

| ファイル | 中身 | だれが作る |
|---|---|---|
| plan.md | 問い・登場する人と会社・調べる資料の一覧 | Claude(init がひな形) |
| people.json | 人の英語名と日本語の書き方 | Claude |
| sources/ ・ sources.jsonl | 読んだ資料の本文と、読めた/読めなかったの記録 | `fetch` `addsrc` |
| facts.jsonl | 事実カード(1行1枚) | Claude |
| timeline.md | 年表・人ごとの欄の埋まり方・共通の相手 | `timeline`(手で直さない) |
| questions.md | 分からない点(自動)+手で足した問い | `gaps` + Claude |
| note.md | 本文(カードだけが材料) | Claude |
| verify.md | 本文の数字・日付・名前のうちカードに無いもの | `verify` |
| glossary.txt | 事実ではない一般の言葉(会社名の書き方・数えた数) | Claude |
| stats.md | 前の下書きとの情報量のくらべ | `stats` |

## 6つの段
**A テーマ** `python3 scripts/deep_post.py init 2026-12-01_xai-founders "テーマ"`
- その日のジャンル(`post_draft.py genre`)と候補(`post_draft.py pick`)から1つ選ぶ。相関図(index.html を grep)に、その人・会社の線が2本以上あるものを選ぶ
- plan.md に「この記事で答える問い」を3つまで書く

**B 一次資料** 人ごとに、次の順で読む(読めたものだけカードにする)
1. 本人: `python3 scripts/x_check.py @名前`(自己紹介=いまの勤め先が分かることが多い)、投稿は `deep_post.py fetch <名前> https://x.com/…/status/…`
2. 論文: Hugging Faceの論文目録 `https://huggingface.co/api/papers/<arXiv番号>`・`/api/papers/search?q=名前`(arXiv本体はこの環境から開けないが、著者と日付はここで確かめられる。出典には arxiv.org/abs/番号 を書く)。**共著者の一覧が、人と人の線のいちばんの手がかり**
3. 開示: SEC(`scripts/sec_watch.py`)、TDnet・HKEX(`scripts/ir_watch.py`)
4. 動画・音声: 講演やポッドキャストの字幕(`scripts/yt_fetch.py`、PCなら `docs/yt_pc.md`)
5. 公式: 会社のブログ・採用ページ・Wikipedia(会社と人のページ。Wikipediaは「報道」扱い)
6. 報道: `deep_post.py fetch` で本文を読む。読めないサイトは WebSearch の要約だけ(カードの read を「検索結果」にする)
- Gemini を使うときは1日18回の上限の中で、答えの出典URLは必ず `fetch` で本文を開いて確かめる(作り話のURLが多い)
- 事実カードの形(1行):
  `{"id":"F001","date":"2025-08-13","who":["Igor Babuschkin"],"org":["xAI"],"cat":"退社","fact":"日本語で1文","quote":"原文の短い引用(任意)","src":"URL","src_name":"媒体(日付)","cf":"公式|開示|本人|報道|推定","read":"本文|検索結果|本人投稿"}`
  - cat: 学歴・前職・研究・入社・役割・発言・退社・行き先・資金・会社・その他
  - org はその人の所属だけ(共著の相手の会社は入れない)。1枚に2人いて所属が違うときは `"org_by":{"人":["会社"]}`
  - 食い違いは `"conflict":"何が"` を書く(gaps が問いにする)
- `python3 scripts/deep_post.py lint <名前>` で形を確かめる

**C 年表と線** `python3 scripts/deep_post.py timeline <名前>` → timeline.md
- 「共通の相手」(2人以上が同じ会社・大学にいた)と、論文の共著が、記事の芯になる

**D 穴** `python3 scripts/deep_post.py gaps <名前>` → questions.md
- 人ごとに「前職・入社・役割・退社・行き先」が無い/報道1本だけ/検索結果だけ、を一覧にする。上から埋める(B に戻る)。埋まらないものは本文の「まだ分かっていないこと」に書く

**E 執筆** note.md に書く(2,000〜4,000字+表)。型: ①導入 ②前の線(論文・前職) ③抜けた順/起きた順 ④行き先と次の会社 ⑤お金の線 ⑥読み取れること(筆者の読み取りと明記) ⑦まだ分かっていないこと ⑧出典(`<!--SOURCES-->` の下)

**F 照合** `python3 scripts/deep_post.py verify <名前>` → verify.md
- 本文の日付・数字・英字とカタカナの名前のうち、カードに無いものを出す。0件にする(直すか、カードを足すか、★を付ける)。12/1の回では「ほかの7人」(正しくは8人)の誤りを2か所見つけた

**まとめ** `python3 scripts/deep_post.py stats <名前> --old 前の下書き.md` と `domains`(読めなかったサイト=許可リストの候補)

## 毎晩の自動下書き(20:30の定期タスク)での分け方
1回で全部やらない。**投稿日の3日前から**、1テーマを3回に分けて進める。
- 1回目(投稿の3日前): A・B(資料を読んでカード30枚以上)
- 2回目(2日前): C・D → B に戻って穴を埋める(カード50枚以上を目安)
- 3回目(前日): E・F → `posts/drafts/日付.md`(X用)と note.md を仕上げる
どの段まで進んだかは plan.md の先頭の「進み具合」に1行で書く。

## 12/1の回でのくらべ(2026/11/24)
前の下書き(v3)は報道6本で本文3,600字。段階式では事実カード69枚(一次資料=論文・本人のX・公式が24枚)、出典URL35本・9サイト、本文約5,700字(表を含む)。v3に無かった線: 論文の共著(ウー×セゲディ、ヤン×バブシュキン、ポーレン×バブシュキン)、コシック氏がいまRiver AIにいる(本人の自己紹介)、Nvidiaが xAI と River AI の両方に出資。

## この環境から読めなかったサイト(2026/11/24、許可リストの候補)
`python3 scripts/deep_post.py domains` で最新が出る。論文・記録の系統は特に効く:
arxiv.org, export.arxiv.org, api.openalex.org, api.semanticscholar.org, dblp.org, openreview.net, scholar.archive.org, www.courtlistener.com, patents.google.com, web.archive.org, www.businessinsider.com, www.fastcompany.com, www.inc.com, www.nbcnews.com, the-decoder.com, www.hpcwire.com, gizmodo.com, futurism.com, www.eweek.com, www.datacenterdynamics.com, www.sherwood.news, www.theguardian.com, www.cs.toronto.edu
(x.ai・bloomberg.com・reuters.com・cnbc.com は応答はあるが断られる)
