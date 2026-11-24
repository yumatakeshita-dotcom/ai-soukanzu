# 2026-12-02(水)お金の動き 下書き: 「買い手が、すでに取引先だった」

状態: **下書き(投稿はしていません)**。方針を「ニュースの要約」から「相関図の線をたどって初めて分かること」に改めて作り直しました(2026/11/24)。投稿前に出典ページを自分の目で開き、当日の朝に `git pull` して新しい情報があれば差し替えてください。
確かさ: 公式(Anthropicの発表3件。IPOの件は2026/11/24に本文を開いて確認、GoogleとMicrosoftの契約は相関図の記録)。画像は使いません。

## 材料(線をたどった結果)
- Anthropicは11/20のIPO完了と同時に、AMD・Broadcom・Google・Micron・Microsoft・NVIDIA・TSMC関連の7社へ新株を売る私募を実施(総額約260億ドル。1社ごとの金額は未開示)
- 相関図の「計算資源の取引」の線を重ねると、買い手のうちGoogleとMicrosoftは、すでにAnthropicと計算資源の契約でつながっていた
  - Google: TPU 約3.5GW(2026/4発表、Broadcomと)
  - Microsoft: Azureで300億ドル分(2025/11発表。MicrosoftとNVIDIAはAnthropicに出資も)
- つまり「お金を出す側」と「Anthropicが計算資源を買う先」が重なっている。ニュースの見出しだけでは見えない線

## X(本投稿)
<!--X1-->
【線をたどる】Anthropicの上場と同時の新株の売り先7社に、GoogleとMicrosoftが。この2社はすでに計算資源の契約先で、出資する側と売る側が重なっています。(公式発表)
https://www.anthropic.com/news/ipo-close
<!--/X-->

## X(返信・2つ目)
<!--X2-->
【契約の側】Googleとは2026年4月に約3.5GWのTPU、Microsoftとは2025年11月にAzure300億ドル分。7社それぞれの購入額は発表に書かれていません。(公式発表)
https://www.anthropic.com/news/google-broadcom-partnership-compute
<!--/X-->

## X(Premium向けの長文版・任意)
【線をたどる】Anthropicが11/20のIPOと同時に行った私募の買い手(AMD・Broadcom・Google・Micron・Microsoft・NVIDIA・TSMC関連の7社、総額約260億ドル)を、相関図の取引の線と重ねると:
・Google: すでにTPU約3.5GWの契約先(2026/4)
・Microsoft: すでにAzure300億ドル分の契約先(2025/11)
出資する側と、Anthropicが計算資源を買う側が重なっています。7社それぞれの金額は未開示なので「1社いくら」とは書きません。(公式発表)

## note(600〜1200字の骨子)
見出し: 「Anthropicに新株を買った7社は、すでに取引先だった ― 相関図で線を重ねる」
1. 何があったか(IPOの数字は公式発表のとおり。1株83ドル・計11.27億株・私募は約260億ドル)
2. 線を重ねる: 買い手7社 × Anthropicの計算資源の契約(Google TPU・Microsoft Azure ほか)。相関図の「共通のつながり」でAnthropicとGoogle/Microsoftを選ぶと線が出る
3. 読み方: 「出資する側が売り手でもある」関係。良い悪いの評価は書かない(事実の並べ方だけ)
4. 分かっていないこと: 7社それぞれの金額(未開示)。ほかの情報源の「1社100億ドル」は公式で確かめられていないので使わない
5. 出典の一覧: https://www.anthropic.com/news/ipo-close 、https://www.anthropic.com/news/google-broadcom-partnership-compute (2026/4/6)、https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships (2025/11/18)
末尾の定型文は docs/post_calendar_2026-12.md のとおり。

## 気をつけること
- 契約額は「上限・最大」のものがある。出典の言い方のとおり書く
- 株の売買をすすめる書き方(「買い」「上がる」)はしない
- GoogleとMicrosoftの契約ページ(上の2つ)は、相関図の記録を使っており、この環境から開けていない。投稿前に自分で開く

## 材料の元
- `inbox/money/2026-11-22-gemini.json`、index.html の `DEALS`(anthropic の行)
