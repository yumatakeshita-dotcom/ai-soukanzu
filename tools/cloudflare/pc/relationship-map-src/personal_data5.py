F, FR, M, W, R, O = 'family', 'friend', 'mentor', 'work', 'rival', 'org'
P5 = {
'Jack Dorsey': [
 (W, '共同創業者', 'Evan Williams', 'エヴァン・ウィリアムズ', 'Twitterの共同創業者。のち、ウィリアムズが先にCEOを務めました。'),
 (W, '共同創業者', 'Biz Stone', 'ビズ・ストーン', 'Twitterの共同創業者。'),
 (W, '共同創業者', 'Noah Glass', 'ノア・グラス', 'Twitterの共同創業者の一人。'),
 (W, '後任', 'Dick Costolo', 'ディック・コストロ', '2008年にドーシーが退いた後、CEOに。'),
 (W, '後任', 'Parag Agrawal', 'パラグ・アグラワル', '2021年に後継のCEOに。'),
 (W, '買い手', 'Elon Musk', 'イーロン・マスク', '2022年にTwitterを買収。ドーシーは買収を支持する姿勢を示したと報じられています。'),
 (O, '共同創業', 'Block', 'Block(旧Square)', '2009年に共同創業。'),
 (O, '支援', 'Bluesky', 'Bluesky', '2019年に出資を始めた分散型SNS。'),
],
'Evan Williams': [
 (W, '共同創業者', 'Jack Dorsey', 'ジャック・ドーシー', 'Twitterの共同創業者。'),
 (W, '共同創業者', 'Biz Stone', 'ビズ・ストーン', 'Twitterの共同創業者。のち共にObviousを設立。'),
 (W, '共同創業者', 'Noah Glass', 'ノア・グラス', 'Odeo時代からの仲間。'),
 (O, '創業', 'Blogger', 'Blogger', 'ブログのサービス。Googleが買収しました。'),
 (O, '創業', 'Obvious', 'Obvious', '2011年に設立。Mediumなどを生みました。'),
 (O, '前身', 'Odeo', 'Odeo', 'Twitterの前身のポッドキャスト会社。'),
],
'Biz Stone': [
 (W, '共同創業者', 'Evan Williams', 'エヴァン・ウィリアムズ', 'Twitterの共同創業者。のち共にObviousを設立。'),
 (W, '共同創業者', 'Jack Dorsey', 'ジャック・ドーシー', 'Twitterの共同創業者。'),
 (O, '創業', 'Obvious', 'Obvious', '2011年に設立。'),
],
'Noah Glass': [
 (W, '共同創業者', 'Jack Dorsey', 'ジャック・ドーシー', 'Twitterの共同創業者。'),
 (W, '共同創業者', 'Evan Williams', 'エヴァン・ウィリアムズ', 'Odeo時代からの仲間。'),
 (O, '前身', 'Odeo', 'Odeo', 'Twitterの前身。'),
],
'Dick Costolo': [
 (W, '前任', 'Jack Dorsey', 'ジャック・ドーシー', '2010年にCEOを引き継ぎました。'),
 (W, '後任', 'Jack Dorsey', 'ジャック・ドーシー', '2015年にCEOへ復帰。'),
],
'Parag Agrawal': [
 (W, '前任のCEO', 'Jack Dorsey', 'ジャック・ドーシー', '2021年に後継指名。'),
 (R, '対立', 'Elon Musk', 'イーロン・マスク', '買収完了直後の2022年10月に解任。'),
 (W, '同時に解任', 'Vijaya Gadde', 'ビジャヤ・ガッデ', '買収完了後に共に解任と報じられています。'),
 (W, '同時に解任', 'Ned Segal', 'ネッド・シーガル', '買収完了後に共に解任と報じられています。'),
],
'Vijaya Gadde': [
 (W, '同時に解任', 'Parag Agrawal', 'パラグ・アグラワル', '2022年10月の買収完了後。'),
 (R, '対立', 'Elon Musk', 'イーロン・マスク', '買収完了後に解任と報じられています。'),
],
'Ned Segal': [
 (W, '同時に解任', 'Parag Agrawal', 'パラグ・アグラワル', '2022年10月の買収完了後。'),
],
'Alwaleed bin Talal': [
 (W, '買収に持ち越し', 'Elon Musk', 'イーロン・マスク', '2022年の買収後も、保有分を持ち越したと報じられています。'),
 (O, '所属', 'Kingdom Holding', 'キングダム・ホールディング', 'サウジの投資会社。'),
],
'Ivan Zhao': [
 (W, '共同創業者', 'Simon Last', 'サイモン・ラスト', 'Notionの共同創業者。'),
 (W, 'COO', 'Akshay Kothari', 'アクシェイ・コタリ', 'NotionのCOO。'),
 (W, '出資者', 'Naval Ravikant', 'ナヴァル・ラヴィカント', '初期の個人投資家の一人と報じられています。'),
 (O, '移住', 'Kyoto', '京都', 'ラストと共に移住し、製品を作り直しました。'),
 (O, '前職', 'Inkling', 'Inkling', '創業前に勤めた会社。'),
 (O, '学校', 'University of British Columbia', 'ブリティッシュコロンビア大学', '認知科学を学んだと伝えられます。'),
],
'Simon Last': [
 (W, '共同創業者', 'Ivan Zhao', 'イワン・ジャオ', 'NotionのCEO。'),
 (O, '移住', 'Kyoto', '京都', 'ジャオと共に移住し、製品を作り直しました。'),
],
'Akshay Kothari': [
 (W, '上司', 'Ivan Zhao', 'イワン・ジャオ', 'NotionのCEO。'),
 (O, '前職', 'LinkedIn', 'LinkedIn', 'Pulseの買収後に在籍。'),
 (O, '創業', 'Pulse', 'Pulse', 'ニュースアプリ。LinkedInに買収されました。'),
],
'Naval Ravikant': [
 (W, '出資先', 'Ivan Zhao', 'イワン・ジャオ', 'Notionの初期の個人投資家の一人と報じられています。'),
 (O, '共同創業', 'AngelList', 'AngelList', '投資のプラットフォーム。'),
],
'Dylan Field': [
 (M, '支援者', 'Peter Thiel', 'ピーター・ティール', 'ティール・フェローシップで創業を支えた人物。'),
 (W, '共同創業者', 'Evan Wallace', 'エヴァン・ウォレス', 'ブラウン大学の同級生。'),
 (W, 'CFO', 'Praveer Melwani', 'プラヴィール・メルワニ', 'Figmaの最高財務責任者。'),
 (R, '買収の相手', 'Adobe', 'Adobe', '2022年に約200億ドルでの買収を発表し、2023年に断念。'),
 (O, '学校', 'Brown University', 'ブラウン大学', '中退して創業。'),
 (O, '前職', 'LinkedIn', 'LinkedIn', 'インターンとして在籍と報じられています。'),
],
'Evan Wallace': [
 (W, '共同創業者', 'Dylan Field', 'ディラン・フィールド', 'FigmaのCEO。議決権を委任。'),
 (O, '学校', 'Brown University', 'ブラウン大学', 'フィールドの同級生。'),
],
'Praveer Melwani': [
 (W, '上司', 'Dylan Field', 'ディラン・フィールド', 'FigmaのCEO。'),
],
'Patrick Collison': [
 (F, '弟', 'John Collison', 'ジョン・コリソン', 'Stripeの共同創業者で社長。'),
 (W, '初期のエンジニア', 'Greg Brockman', 'グレッグ・ブロックマン', 'Stripeの元CTO。のちOpenAIを共同創業。'),
 (W, '初期の出資者', 'Peter Thiel', 'ピーター・ティール', 'Founders Fundを通じて出資。'),
 (W, '初期の出資者', 'Elon Musk', 'イーロン・マスク', '2011年の初期の個人投資家の一人と報じられています。'),
 (O, '学校', 'MIT', 'マサチューセッツ工科大学', '中退してStripeを創業。'),
 (O, '創業', 'Auctomatic', 'Auctomatic', '10代で創業して売却した会社。'),
],
'John Collison': [
 (F, '兄', 'Patrick Collison', 'パトリック・コリソン', 'StripeのCEO。'),
 (O, '学校', 'Harvard University', 'ハーバード大学', '中退してStripeを創業。'),
],
'Melanie Perkins': [
 (F, '夫', 'Cliff Obrecht', 'クリフ・オブレヒト', 'Canvaの共同創業者でCOO。'),
 (W, '共同創業者', 'Cameron Adams', 'キャメロン・アダムス', 'Canvaの共同創業者。'),
 (W, '助言者', 'Lars Rasmussen', 'ラース・ラスムセン', 'Google Mapsの共同創業者。創業初期に助言と出資と伝えられます。'),
 (W, '元エバンジェリスト', 'Guy Kawasaki', 'ガイ・カワサキ', '2014〜2018年にチーフ・エバンジェリスト。'),
 (O, '学校', 'University of Western Australia', '西オーストラリア大学', '在学中にFusion Booksを始めました。'),
 (O, '原点', 'Fusion Books', 'Fusion Books', '卒業アルバムを作る事業。'),
],
'Cliff Obrecht': [
 (F, '妻', 'Melanie Perkins', 'メラニー・パーキンス', 'CanvaのCEO。'),
 (W, '共同創業者', 'Cameron Adams', 'キャメロン・アダムス', 'Canvaの共同創業者。'),
],
'Cameron Adams': [
 (W, '共同創業者', 'Melanie Perkins', 'メラニー・パーキンス', 'CanvaのCEO。'),
 (W, '共同創業者', 'Cliff Obrecht', 'クリフ・オブレヒト', 'CanvaのCOO。'),
],
'Guy Kawasaki': [
 (W, '雇い主', 'Melanie Perkins', 'メラニー・パーキンス', 'Canvaのチーフ・エバンジェリストを務めました。'),
 (O, '前職', 'Apple', 'Apple', '元エバンジェリスト。'),
],
'Lars Rasmussen': [
 (W, '助言先', 'Melanie Perkins', 'メラニー・パーキンス', 'Canvaの創業初期に助言・出資と伝えられます。'),
 (W, '元同僚', 'Bret Taylor', 'ブレット・テイラー', 'Google Mapsを共に立ち上げました。'),
 (O, '共同創業', 'Google Maps', 'Google Maps', 'Where 2 Technologiesを共同創業し、Googleが買収。'),
],
'Michael Truell': [
 (W, '共同創業者', 'Sualeh Asif', 'スアレー・アシフ', 'Cursorの共同創業者。'),
 (W, '共同創業者', 'Aman Sanger', 'アマン・サンガー', 'Cursorの共同創業者。'),
 (W, '共同創業者', 'Arvid Lunnemark', 'アルビッド・ルンネマルク', '2025年に退社。'),
 (O, '学校', 'MIT', 'マサチューセッツ工科大学', '学部。'),
],
'Sualeh Asif': [
 (W, '共同創業者', 'Michael Truell', 'マイケル・トゥルエル', 'CursorのCEO。'),
 (O, '学校', 'MIT', 'マサチューセッツ工科大学', '学部。'),
],
'Aman Sanger': [
 (W, '共同創業者', 'Michael Truell', 'マイケル・トゥルエル', 'CursorのCEO。'),
 (O, '学校', 'MIT', 'マサチューセッツ工科大学', '学部。'),
],
'Arvid Lunnemark': [
 (W, '元共同創業者', 'Michael Truell', 'マイケル・トゥルエル', 'CursorのCEO。'),
 (O, '学校', 'MIT', 'マサチューセッツ工科大学', '学部。'),
 (O, '新会社', 'Integrous Research', 'Integrous Research', '2025年に立ち上げたAIの安全性の研究所。'),
],
'Stewart Butterfield': [
 (W, '共同創業者', 'Cal Henderson', 'カル・ヘンダーソン', 'SlackとFlickrを共に創業。'),
 (W, '買い手', 'Marc Benioff', 'マーク・ベニオフ', '2021年にSlackを買収。'),
 (O, '創業', 'Flickr', 'Flickr', '写真共有サービス。Yahooが買収。'),
],
'Cal Henderson': [
 (W, '共同創業者', 'Stewart Butterfield', 'スチュワート・バターフィールド', 'SlackとFlickrを共に創業。'),
 (O, '前職', 'Flickr', 'Flickr', '初期の開発者。'),
],
'Lidiane Jones': [
 (W, '後任のCEO', 'Denise Dresser', 'デニス・ドレッサー', 'Slackの次のCEO。'),
 (O, '移籍先', 'Bumble', 'Bumble', 'CEOに就任と報じられています。'),
],
'Rob Seaman': [
 (W, '前任の責任者', 'Denise Dresser', 'デニス・ドレッサー', '退任後に暫定で引き継いだと報じられています。'),
],
'Marc Benioff': [
 (W, '共同CEOだった', 'Bret Taylor', 'ブレット・テイラー', 'Salesforceの共同CEOとして共に経営。'),
 (W, '買収した', 'Stewart Butterfield', 'スチュワート・バターフィールド', '2021年にSlackを約277億ドルで買収。'),
 (W, '部下', 'Denise Dresser', 'デニス・ドレッサー', 'Slack CEOを経てOpenAIへ。'),
 (O, '創業', 'Salesforce', 'Salesforce', '共同創業者でCEO。'),
],
}
