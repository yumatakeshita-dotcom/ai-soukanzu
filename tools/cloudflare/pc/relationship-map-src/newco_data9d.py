from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Mastercard ----------------
deep('MA', 'Mastercard', 1966, NOTE, [
  P('selander', 'ロバート・セランダー', 'Robert Selander', 1997, '1997〜2010年にCEO。2006年のIPOを率いました。', '元CEO', 2010),
  P('banga', 'アジェイ・バンガ', 'Ajay Banga', 2009, '2010〜2020年にCEO。のち世界銀行総裁(2023年から)。', '元CEO', 2021),
  P('miebach', 'マイケル・ミーバック', 'Michael Miebach', 2010, '2021年からCEO。', 'CEO'),
  P('janow', 'メリット・ジャナウ', 'Merit Janow', 2014, '会長。', '会長'),
  P('mehra', 'サチン・メーラ', 'Sachin Mehra', 2010, 'CFO。', 'CFO'),
  O('foundation', 'Mastercard Foundation', 2006, '2006年のIPOで株式を受け取った財団。約6.6%を持つ上位株主(Yahoo Finance)。', '上位株主(約6.6%)', 'i'),
  O('vocalink', 'Vocalink', 2017, '2017年に約7億ポンドで買収。', '買収(2017年)'),
  O('nets', 'Nets', 2019, '2019年に約28.5億ユーロで買収。', '買収(2019年)'),
  O('ethoca', 'Ethoca', 2019, '2019年に買収。', '買収(2019年)'),
  O('finicity', 'Finicity', 2020, '2020年に約8.25億ドルで買収。', '買収(2020年)'),
  O('recorded', 'Recorded Future', 2024, '2024年に約26.5億ドルで買収(サイバー脅威情報)。', '買収(2024年)'),
 ] + holders([('BlackRock', '7.6', Y), ('Vanguard', '6.0', Y), ('State Street', '4.3', Y)]),
 [('selander', 'banga', 'link', '後任'), ('banga', 'miebach', 'link', '後任', 2021), ('co', 'foundation', 'link', '株式を保有'), ('co', 'vocalink', 'owns'), ('co', 'nets', 'owns'), ('co', 'ethoca', 'owns'), ('co', 'finicity', 'owns'), ('co', 'recorded', 'owns')],
 '1966年のMaster Chargeを源流とする決済ネットワーク。2021年からマイケル・ミーバックがCEOを務めています。')

# ---------------- AbbVie ----------------
deep('ABBV', 'AbbVie', 2013, NOTE, [
  P('gonzalez', 'リチャード・ゴンザレス', 'Richard Gonzalez', 2013, 'アボットから分離独立した2013年から、2024年6月までCEO。', '元CEO', 2024),
  P('michael', 'ロバート・マイケル', 'Robert Michael', 2013, '2024年7月からCEO(のち会長も)。', '会長兼CEO'),
  P('reents', 'スコット・レエンツ', 'Scott Reents', 2013, 'CFO。', 'CFO'),
  O('abbott', 'Abbott Laboratories', 2013, '2013年に研究開発型の医薬品部門を分離。', '親会社(分離元)'),
  O('pharmacyclics', 'Pharmacyclics', 2015, '2015年に約210億ドルで買収。', '買収(2015年)'),
  O('stemcentrx', 'Stemcentrx', 2016, '2016年に約58億ドルで買収。', '買収(2016年)'),
  O('allergan', 'Allergan', 2020, '2020年に約630億ドルで買収。', '買収(2020年)'),
  O('immunogen', 'ImmunoGen', 2024, '2024年に約101億ドルで買収。', '買収(2024年)'),
  O('cerevel', 'Cerevel Therapeutics', 2024, '2024年に約87億ドルで買収。', '買収(2024年)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.5', M), ('State Street', '4.7', M)]),
 [('abbott', 'gonzalez', 'link', '分離を率いる'), ('gonzalez', 'michael', 'link', '後任', 2024), ('co', 'pharmacyclics', 'owns'), ('co', 'stemcentrx', 'owns'), ('co', 'allergan', 'owns'), ('co', 'immunogen', 'owns'), ('co', 'cerevel', 'owns')],
 '2013年にアボットから分離した製薬会社。2024年7月からロバート・マイケルがCEOを務めています。')

# ---------------- Chevron ----------------
deep('CVX', 'Chevron', 1879, NOTE, [
  P('oreilly', 'デビッド・オライリー', "Dave O'Reilly", 2000, '2000〜2009年にCEO。テキサコとの合併(2001年)を主導。', '元CEO', 2009),
  P('watson', 'ジョン・ワトソン', 'John Watson', 1980, '2010〜2017年にCEO。', '元CEO', 2017),
  P('wirth', 'マイク・ワース', 'Mike Wirth', 1982, '2018年からCEO兼会長。', '会長兼CEO'),
  P('bonner', 'エイメア・ボナー', 'Eimear Bonner', 2020, 'CFO。', 'CFO'),
  O('berkshire', 'Berkshire Hathaway', 2020, '約4.3%を持つ上位株主(MarketScreener、2026年11月)。', '株主(約4.3%)', 'i'),
  O('texaco', 'Texaco', 2001, '2001年に約450億ドルで合併。', '合併(2001年)'),
  O('unocal', 'Unocal', 2005, '2005年に約180億ドルで買収。', '買収(2005年)'),
  O('noble', 'Noble Energy', 2020, '2020年に約50億ドルで買収。', '買収(2020年)'),
  O('hess', 'Hess', 2025, '2025年に約530億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('State Street', '7.5', M), ('Vanguard', '6.2', M), ('BlackRock', '6.1', M)]),
 [('oreilly', 'watson', 'link', '後任'), ('watson', 'wirth', 'link', '後任', 2018), ('co', 'texaco', 'owns'), ('co', 'unocal', 'owns'), ('co', 'noble', 'owns'), ('co', 'hess', 'owns')],
 '1879年創業のStandard Oil of Californiaを源流とする石油大手。2018年からマイク・ワースがCEOを務めています。')

# ---------------- Costco ----------------
deep('COST', 'Costco', 1976, NOTE, [
  P('solprice', 'ソル・プライス', 'Sol Price', 1976, 'Price Club(1976年)を創業。Costcoとの合併(1993年)の源流。', '創業者(Price Club)', 1994, 1),
  P('sinegal', 'ジム・シネガル', 'Jim Sinegal', 1983, '1983年にCostcoを共同創業し、2011年までCEO。', '共同創業者 / 元CEO', 2011, 1),
  P('brotman', 'ジェフリー・ブロットマン', 'Jeffrey Brotman', 1983, '共同創業者。会長を務め、2017年に亡くなりました。', '共同創業者 / 元会長', 2017, 1),
  P('jelinek', 'クレイグ・ジェリネク', 'Craig Jelinek', 1984, '2012〜2023年にCEO。', '元CEO', 2024),
  P('vachris', 'ロン・ヴァクリス', 'Ron Vachris', 1983, '2024年1月からCEO。', 'CEO'),
  P('james', 'ハミルトン・ジェームズ', 'Hamilton James', 1998, '会長。', '会長'),
  P('millerchip', 'ゲイリー・ミラーチップ', 'Gary Millerchip', 2024, 'CFO。', 'CFO'),
  O('priceclub', 'Price Club', 1993, '1993年に合併(PriceCostco)。', '合併(1993年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.8', M), ('State Street', '4.1', M)]),
 [('sinegal', 'brotman', 'link', '共同創業'), ('solprice', 'sinegal', 'link', '師'), ('sinegal', 'jelinek', 'link', '後任', 2012), ('jelinek', 'vachris', 'link', '後任', 2024), ('co', 'priceclub', 'owns'), ('solprice', 'priceclub', 'link', '創業')],
 '1983年に創業した会員制の小売。1993年にPrice Clubと合併し、2024年1月からロン・ヴァクリスがCEOを務めています。')

# ---------------- Palantir ----------------
deep('PLTR', 'Palantir', 2003, NOTE, [
  P('thiel', 'ピーター・ティール', 'Peter Thiel', 2003, '共同創業者。会長。', '共同創業者 / 会長', None, 1),
  P('karp', 'アレックス・カープ', 'Alex Karp', 2003, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('cohen', 'スティーブン・コーエン', 'Stephen Cohen', 2003, '共同創業者で社長。', '共同創業者 / 社長', None, 1),
  P('lonsdale', 'ジョー・ロンズデール', 'Joe Lonsdale', 2003, '共同創業者。のち投資家(8VC)。', '共同創業者', 2005, 1),
  P('gettings', 'ネイサン・ゲッティングス', 'Nathan Gettings', 2003, '共同創業者。', '共同創業者', 2006, 1),
  P('sankar', 'シャム・サンカー', 'Shyam Sankar', 2006, 'CTO。', 'CTO'),
  P('glazer', 'デビッド・グレイザー', 'David Glazer', 2018, 'CFO。', 'CFO'),
  O('intelq', 'In-Q-Tel', 2005, '米中央情報局(CIA)系のベンチャー。初期の出資者として知られます。', '初期の出資者', 'i'),
  O('foundersfund', 'Founders Fund', 2004, '初期の出資者(ティールのファンド)。', '初期の出資者', 'i'),
 ] + holders([('BlackRock', '8.7', Y), ('Vanguard', '6.7', Y), ('State Street', '4.8', Y)]),
 [('thiel', 'karp', 'link', '共同創業'), ('thiel', 'cohen', 'link', '共同創業'), ('thiel', 'lonsdale', 'link', '共同創業'), ('intelq', 'thiel', 'link', '初期の資金')],
 '2003年にピーター・ティールらが創業したデータ分析の会社。アレックス・カープがCEOを務めています。')

# ---------------- Cisco ----------------
deep('CSCO', 'Cisco', 1984, NOTE, [
  P('bosack', 'レン・ボサック', 'Leonard Bosack', 1984, '共同創業者。', '共同創業者', 1990, 1),
  P('lerner', 'サンディ・ラーナー', 'Sandy Lerner', 1984, '共同創業者。', '共同創業者', 1990, 1),
  P('valentine', 'ドン・バレンタイン', 'Don Valentine', 1987, 'セコイア・キャピタルの創業者。1987年に出資。', '初期の出資者', 2019),
  P('morgridge', 'ジョン・モーリッジ', 'John Morgridge', 1988, '1988〜1995年にCEO。', '元CEO', 1995),
  P('chambers', 'ジョン・チェンバース', 'John Chambers', 1991, '1995〜2015年にCEO。', '元CEO', 2015),
  P('robbins', 'チャック・ロビンス', 'Chuck Robbins', 1997, '2015年からCEO(会長も)。', '会長兼CEO'),
  P('herren', 'スコット・ヘレン', 'Scott Herren', 2022, 'CFO。', 'CFO'),
  O('sequoia', 'Sequoia Capital', 1987, '1987年に出資。', '初期の出資者', 'i'),
  O('linksys', 'Linksys', 2003, '2003年に約5億ドルで買収(のち売却)。', '買収(2003年)'),
  O('scientific', 'Scientific-Atlanta', 2005, '2005年に約69億ドルで買収。', '買収(2005年)'),
  O('webex', 'WebEx', 2007, '2007年に約32億ドルで買収。', '買収(2007年)'),
  O('meraki', 'Meraki', 2012, '2012年に約12億ドルで買収。', '買収(2012年)'),
  O('appd', 'AppDynamics', 2017, '2017年に約37億ドルで買収。', '買収(2017年)'),
  O('duo', 'Duo Security', 2018, '2018年に約23.5億ドルで買収。', '買収(2018年)'),
  O('splunk', 'Splunk', 2024, '2024年に約280億ドルで買収。', '買収(2024年)'),
 ] + holders([('BlackRock', '9.1', Y), ('Vanguard', '6.2', Y), ('State Street', '5.0', Y)]),
 [('bosack', 'lerner', 'link', '共同創業(夫婦)'), ('valentine', 'bosack', 'link', '出資'), ('morgridge', 'chambers', 'link', '後任'), ('chambers', 'robbins', 'link', '後任', 2015), ('co', 'linksys', 'owns'), ('co', 'scientific', 'owns'), ('co', 'webex', 'owns'), ('co', 'meraki', 'owns'), ('co', 'appd', 'owns'), ('co', 'duo', 'owns'), ('co', 'splunk', 'owns'), ('valentine', 'sequoia', 'link', '創業')],
 '1984年にスタンフォード大学の2人が創業したネットワーク機器の会社。2015年からチャック・ロビンスがCEOを務めています。')

# ---------------- Coca-Cola ----------------
deep('KO', 'Coca-Cola', 1886, NOTE, [
  P('pemberton', 'ジョン・ペンバートン', 'John Pemberton', 1886, '1886年にコカ・コーラを考案した薬剤師。', '創業者', 1888, 1),
  P('candler', 'エイサ・キャンドラー', 'Asa Candler', 1888, '1888年に権利を買い取り、会社を築きました。', '元社長', 1916),
  P('woodruff', 'ロバート・ウッドラフ', 'Robert Woodruff', 1923, '1923〜1955年に社長。', '元社長', 1955),
  P('goizueta', 'ロベルト・ゴイズエタ', 'Roberto Goizueta', 1981, '1981〜1997年にCEO。', '元CEO', 1997),
  P('isdell', 'ニール・アイズデル', 'Neville Isdell', 2004, '2004〜2008年にCEO。', '元CEO', 2008),
  P('kent', 'ムーター・ケント', 'Muhtar Kent', 2008, '2008〜2017年にCEO。', '元CEO', 2017),
  P('quincey', 'ジェームズ・クインシー', 'James Quincey', 1996, '2017〜2026年にCEO。以後は執行会長。', '会長(執行)'),
  P('braun', 'エンリケ・ブラウン', 'Henrique Braun', 1996, '現CEO(英語版Wikipedia)。', 'CEO'),
  P('murphy', 'ジョン・マーフィー', 'John Murphy', 2003, '社長兼CFO。', '社長兼CFO'),
  O('berkshire', 'Berkshire Hathaway', 1988, '1988年から保有。約9.3%を持つ上位株主(Yahoo Finance)。', '株主(約9.3%)', 'i'),
  O('minutemaid', 'Minute Maid', 1960, '1960年に買収。', '買収(1960年)'),
  O('costa', 'Costa Coffee', 2018, '2018年に約39億ポンドで買収。', '買収(2018年)'),
  O('fairlife', 'fairlife', 2020, '2020年に買収。', '買収(2020年)'),
  O('bodyarmor', 'BodyArmor', 2021, '2021年に約56億ドルで買収。', '買収(2021年)'),
  O('monster', 'Monster Beverage', 2015, '約20%を保有(2015年の提携)。', '出資先'),
 ] + holders([('BlackRock', '7.5', Y), ('Vanguard', '5.6', Y)]),
 [('pemberton', 'candler', 'link', '権利を売却'), ('candler', 'woodruff', 'link', '後任'), ('goizueta', 'isdell', 'link'), ('isdell', 'kent', 'link', '後任'), ('kent', 'quincey', 'link', '後任', 2017), ('quincey', 'braun', 'link', 'CEO交代', 2026), ('co', 'minutemaid', 'owns'), ('co', 'costa', 'owns'), ('co', 'fairlife', 'owns'), ('co', 'bodyarmor', 'owns'), ('co', 'monster', 'invest2', '出資')],
 '1886年に誕生した飲料会社。2026年からヘンリケ・ブラウンがCEOを務め、バークシャーが約9.3%を持っています。')

# ---------------- Oracle ----------------
deep('ORCL', 'Oracle', 1977, NOTE + 'エリソン氏の持ち分は、Yahoo Financeのインサイダー合計が約38.4%です。', [
  P('ellison', 'ラリー・エリソン', 'Larry Ellison', 1977, '共同創業者。CEOを2014年まで務め、以後は会長兼CTO。', '共同創業者 / 会長兼CTO', None, 1),
  P('miner', 'ボブ・マイナー', 'Bob Miner', 1977, '共同創業者。2003年に亡くなりました。', '共同創業者', 2003, 1),
  P('oates', 'エド・オーツ', 'Ed Oates', 1977, '共同創業者。', '共同創業者', 1996, 1),
  P('catz', 'サフラ・キャッツ', 'Safra Catz', 1999, '2014〜2025年に共同CEO。以後は副会長。', '副会長'),
  P('hurd', 'マーク・ハード', 'Mark Hurd', 2010, '2010〜2018年に共同社長(のち共同CEO)。2019年に亡くなりました。', '元共同CEO', 2019),
  P('magouyrk', 'クレイ・マグワーク', 'Clay Magouyrk', 2014, '共同CEO(2025年から)。', '共同CEO'),
  P('sicilia', 'マイク・シシリア', 'Mike Sicilia', 2005, '共同CEO(2025年から)。', '共同CEO'),
  O('peoplesoft', 'PeopleSoft', 2005, '2005年に約103億ドルで買収。', '買収(2005年)'),
  O('netsuite', 'NetSuite', 2016, '2016年に約93億ドルで買収。', '買収(2016年)'),
  O('sun', 'Sun Microsystems', 2010, '2010年に約74億ドルで買収。', '買収(2010年)'),
  O('cerner', 'Cerner', 2022, '2022年に約283億ドルで買収(医療IT)。', '買収(2022年)'),
  O('openai', 'OpenAI', 2025, 'スターゲートで提携(報道)。', '提携'),
 ] + holders([('BlackRock', '4.8', M), ('Vanguard', '3.7', M), ('State Street', '2.6', M)]),
 [('ellison', 'miner', 'link', '共同創業'), ('ellison', 'oates', 'link', '共同創業'), ('ellison', 'catz', 'link', '共同CEO'), ('hurd', 'catz', 'link', '共同CEO'), ('catz', 'magouyrk', 'link', '後任', 2025), ('co', 'peoplesoft', 'owns'), ('co', 'netsuite', 'owns'), ('co', 'sun', 'owns'), ('co', 'cerner', 'owns'), ('co', 'openai', 'link')],
 '1977年にラリー・エリソンらが創業したデータベースの会社。2025年からクレイ・マグワークとマイク・シシリアが共同CEOを務めています。')

# ---------------- Procter & Gamble ----------------
deep('PG', 'Procter & Gamble', 1837, NOTE, [
  P('procter', 'ウィリアム・プロクター', 'William Procter', 1837, '1837年に共同創業(ろうそく職人)。', '共同創業者', 1884, 1),
  P('gamble', 'ジェームズ・ギャンブル', 'James Gamble', 1837, '1837年に共同創業(石けん職人)。', '共同創業者', 1891, 1),
  P('lafley', 'A・G・ラフリー', 'A. G. Lafley', 2000, '2000〜2009年と2013〜2015年にCEO。', '元CEO', 2015),
  P('mcdonald', 'ボブ・マクドナルド', 'Bob McDonald', 2009, '2009〜2013年にCEO。', '元CEO', 2013),
  P('taylor', 'デビッド・テイラー', 'David Taylor', 2015, '2015〜2021年にCEO。', '元CEO', 2021),
  P('moeller', 'ジョン・モエラー', 'Jon Moeller', 2021, '2021〜2025年にCEO。', '元CEO', 2026),
  P('jejurikar', 'シャイレシュ・ジェジュリカー', 'Shailesh Jejurikar', 2026, '2026年からCEO兼会長(英語版Wikipedia)。', 'CEO兼会長'),
  O('clairol', 'Clairol', 2001, '2001年に買収。', '買収(2001年)'),
  O('wella', 'Wella', 2003, '2003年に買収(のち売却)。', '買収(2003年)'),
  O('gillette', 'Gillette', 2005, '2005年に約570億ドルで買収。', '買収(2005年)'),
  O('duracell', 'Duracell', 2014, '2014年にバークシャーへ譲渡する契約を結びました(2016年完了)。', '譲渡(2016年)'),
 ] + holders([('BlackRock', '8.2', Y), ('Vanguard', '6.6', Y), ('State Street', '4.4', Y)]),
 [('procter', 'gamble', 'link', '共同創業'), ('lafley', 'mcdonald', 'link', '後任'), ('mcdonald', 'lafley', 'link', '復帰'), ('lafley', 'taylor', 'link', '後任'), ('taylor', 'moeller', 'link', '後任', 2021), ('moeller', 'jejurikar', 'link', '後任', 2026), ('co', 'clairol', 'owns'), ('co', 'wella', 'owns'), ('co', 'gillette', 'owns'), ('co', 'duracell', 'owns')],
 '1837年にプロクターとギャンブルが創業した日用品の会社。2026年からシャイレシュ・ジェジュリカーがCEOを務めています。')

# ---------------- Merck ----------------
deep('MRK', 'Merck', 1891, NOTE, [
  P('gmerck', 'ジョージ・メルク', 'George Merck', 1891, '1891年に米国法人を設立(ドイツのメルク家)。', '創設者', 1950, 1),
  P('gilmartin', 'レイ・ギルマーティン', 'Ray Gilmartin', 1994, '1994〜2005年にCEO。', '元CEO', 2005),
  P('clark', 'リチャード・クラーク', 'Richard Clark', 2005, '2005〜2010年にCEO。', '元CEO', 2010),
  P('frazier', 'ケン・フレイジャー', 'Ken Frazier', 2011, '2011〜2021年にCEO。', '元CEO', 2021),
  P('davis', 'ロバート・デイビス', 'Robert Davis', 2021, '2021年からCEO兼会長。', '会長兼CEO'),
  P('litchfield', 'キャロライン・リッチフィールド', 'Caroline Litchfield', 2021, 'CFO。', 'CFO'),
  P('li', 'ディーン・リー', 'Dean Li', 2013, 'メルク研究所の社長。', '研究所社長'),
  O('scheringplough', 'Schering-Plough', 2009, '2009年に約410億ドルで買収。', '買収(2009年)'),
  O('organon', 'Organon', 2021, '2021年に女性の健康などの事業を分離。', '分離(2021年)'),
  O('acceleron', 'Acceleron', 2021, '2021年に約115億ドルで買収。', '買収(2021年)'),
  O('prometheus', 'Prometheus Biosciences', 2023, '2023年に約108億ドルで買収。', '買収(2023年)'),
  O('verona', 'Verona Pharma', 2025, '2025年に約100億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '9.2', Y), ('Vanguard', '6.5', Y), ('State Street', '4.9', Y)]),
 [('clark', 'frazier', 'link', '後任'), ('frazier', 'davis', 'link', '後任', 2021), ('gilmartin', 'clark', 'link', '後任'), ('co', 'scheringplough', 'owns'), ('co', 'organon', 'owns'), ('co', 'acceleron', 'owns'), ('co', 'prometheus', 'owns'), ('co', 'verona', 'owns')],
 '1891年に米国法人が設立された製薬会社。2021年からロバート・デイビスがCEOを務めています。')
