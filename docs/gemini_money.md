# お金の流れ v5(Gemini版)のしくみ(2026/11/19)

目的: Claudeの使用量を減らす。「探す」はGemini、「確かめる」はプログラム、Claudeは合格分を確かめて取り込むだけ。

流れ: `scripts/gemini_money.py run` → Geminiが探す → プログラムが1件ずつ確かめる → `inbox/gemini/money/日付_pass.md`(合格・要確認・却下)→ Claudeは「合格」の節だけ読む → `emit` で `inbox/money/日付_gemini.json`。

確かめること(プログラム): 出典が開けるか / ページに会社名・金額があるか / ページの日付とGeminiの日付が7日以内で合うか / すでにある事実(inbox/・調査の新着・毎日の更新記録)と重複しないか / 種類・確かさの値が正しいか。クラウドから届かないサイトは、Geminiの「URLを開く」機能(Google側で開く)で代わりに確かめる(開けたかは取得結果で判断)。
無料枠: 1日の呼び出しに上限(既定12回、GEMINI_DAILY_LIMIT)。429(枠切れ)が出たらその日は止める(inbox/gemini/usage.json)。

試験(2026/11/19): Geminiの候補19件のうち合格0。多くは出典URLがGeminiの作り間違い(開けない)か、すでにある事実。誤った候補を通さない点は意図どおり。合格を増やすには、通信先の許可の追加が効く(別スレッドで対応中)。
定期タスクの指示文: プロジェクトの共有フォルダ money-research/money_v5_gemini_prompt.txt。v4 はオフにするだけで消さない。
