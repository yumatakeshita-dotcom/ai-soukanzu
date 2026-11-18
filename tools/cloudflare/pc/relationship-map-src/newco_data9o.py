from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Southern Company ----------------
deep('SO', 'Southern Company', 1945, NOTE, [
  P('fanning', 'トーマス・ファニング', 'Thomas Fanning', 1980, '2010〜2023年にCEO。ボーグル原発の拡張を率いました。', '元CEO', 2023),
  P('womack', 'クリス・ウォマック', 'Chris Womack', 1990, '2023年4月からCEO兼会長。', '会長兼CEO'),
  P('poroch', 'デビッド・ポロック', 'David Poroch', 2020, 'CFO。', 'CFO'),
  O('georgiapower', 'Georgia Power', 1945, '中核の電力子会社。', '子会社'),
  O('vogtle', 'ボーグル原子力発電所3・4号機', 2023, '2023年と2024年に営業運転を開始した新設の原発。', '事業'),
  O('agl', 'AGL Resources', 2016, '2016年に約80億ドルで買収(現Southern Company Gas)。', '買収(2016年)'),
  O('powersecure', 'PowerSecure', 2016, '2016年に買収。', '買収(2016年)'),
 ] + holders([('BlackRock', '7.0', M), ('Vanguard', '6.4', M), ('State Street', '5.6', M), ('Capital Group', '5.4', M)]),
 [('fanning', 'womack', 'link', '後任', 2023), ('co', 'georgiapower', 'owns'), ('co', 'agl', 'owns'), ('co', 'powersecure', 'owns'), ('georgiapower', 'vogtle', 'link', '運営')],
 '1945年に設立された米南東部の電力会社。2023年からクリス・ウォマックがCEOを務めています。')

# ---------------- Corning ----------------
deep('GLW', 'Corning', 1851, NOTE, [
  P('houghton1', 'アモリー・ホートン', 'Amory Houghton', 1851, '1851年にガラス会社を創業。', '創業者', 1882, 1),
  P('houghton2', 'ジェームズ・ホートン', 'James Houghton', 1983, '1983〜1996年と2002〜2005年にCEO。創業家出身。', '元CEO', 2005),
  P('weeks', 'ウェンデル・ウィークス', 'Wendell Weeks', 1989, '2005年からCEO兼会長。', '会長兼CEO'),
  P('steverson', 'ルイス・スティーバーソン', 'Lewis Steverson', 2013, '副会長(英語版Wikipedia)。', '副会長'),
  P('jobs', 'スティーブ・ジョブズ', 'Steve Jobs', 2006, 'Appleの共同創業者。2006年にiPhone用の強化ガラスを依頼し、Gorilla Glassが生まれました。', '顧客(Apple)', 2011),
  O('apple', 'Apple', 2007, 'iPhoneにGorilla Glassを供給。', '主要顧客'),
  O('samsung', 'Samsung', 2026, '約7.9%を持つ上位株主(Samsung Electronics、MarketScreener)。', '株主(約7.9%)', 'i'),
  O('dowcorning', 'Dow Corning', 1943, '1943年から折半出資していた合弁会社(2016年に持ち分を売却)。', '合弁(〜2016年)'),
 ] + holders([('BlackRock', '5.9', M), ('Vanguard', '5.9', M), ('State Street', '4.8', M)]),
 [('houghton1', 'houghton2', 'link', '創業家'), ('houghton2', 'weeks', 'link', '後任', 2005), ('jobs', 'weeks', 'link', 'Gorilla Glassを依頼', 2006), ('co', 'apple', 'link', '主要顧客'), ('co', 'dowcorning', 'invest2', '合弁')],
 '1851年に創業した特殊ガラス・光ファイバーの会社。2005年からウェンデル・ウィークスがCEOを務め、AppleのiPhone用のGorilla Glassを供給しています。')

# ---------------- CIBC ----------------
deep('CM', 'CIBC', 1961, NOTE + '歴代の経営者以外の情報は少なく、確認できた範囲だけを載せています。', [
  P('mccaughey', 'ジェリー・マッコーイ', 'Gerry McCaughey', 2005, '2005〜2014年にCEO。', '元CEO', 2014),
  P('dodig', 'ビクター・ドディグ', 'Victor Dodig', 2014, '2014〜2022年にCEO。', '元CEO', 2022),
  P('culham', 'ハリー・カルハム', 'Harry Culham', 2022, '2022年からCEO。', 'CEO'),
  P('stevenson', 'キャサリン・スティーブンソン', 'Katharine Stevenson', 2017, '取締役会長。', '会長'),
  O('commerce', 'Canadian Bank of Commerce', 1961, '1961年にImperial Bankと合併。', '合併(1961年)'),
  O('imperial', 'Imperial Bank of Canada', 1961, '1961年にCommerce銀行と合併。', '合併(1961年)'),
  O('privatebancorp', 'PrivateBancorp', 2017, '2017年に約49億ドルで買収(現CIBC Bank USA)。', '買収(2017年)'),
  O('royaltrust', 'Royal Trust Corporation of Canada', 2026, '約7.0%を持つ(MarketScreener)。RBCの信託子会社。', '株主(約7.0%)', 'i'),
 ] + holders([('BMO Bank NA', '4.6', M), ('Vanguard', '3.1', M)]),
 [('commerce', 'mccaughey', 'link', '源流を継ぐ'), ('mccaughey', 'dodig', 'link', '後任'), ('dodig', 'culham', 'link', '後任', 2022), ('co', 'commerce', 'owns'), ('co', 'imperial', 'owns'), ('co', 'privatebancorp', 'owns')],
 '1961年にカナダの2行が合併して誕生した銀行。2022年からハリー・カルハムがCEOを務めています。')

# ---------------- Marriott ----------------
deep('MAR', 'Marriott International', 1927, NOTE, [
  P('jwmarriott', 'J・ウィラード・マリオット', 'J. Willard Marriott', 1927, '1927年にワシントンDCでルートビア店を開いた創業者。', '創業者', 1985, 1),
  P('billmarriott', 'ビル・マリオット・ジュニア', 'Bill Marriott Jr.', 1964, '1972〜2012年にCEO。', '元CEO', 2012),
  P('sorenson', 'アーン・ソレンソン', 'Arne Sorenson', 1996, '2012〜2021年にCEO。2021年に亡くなりました。', '元CEO', 2021),
  P('capuano', 'アンソニー・カプアーノ', 'Anthony Capuano', 1995, '2021年からCEO。', 'CEO'),
  P('davidmarriott', 'デビッド・マリオット', 'David Marriott', 2000, '会長(英語版Wikipedia)。創業家。約4.1%を保有。', '会長'),
  P('johnmarriott', 'ジョン・マリオット', 'John Marriott', 1980, '創業家。約10.6%を保有(MarketScreener)。', '創業家の株主'),
  P('oberg', 'キャスリーン・オバーグ', 'Kathleen Oberg', 2021, 'CFO。', 'CFO'),
  O('ritz', 'The Ritz-Carlton', 1995, '1995年に過半を取得。', '買収(1995年)'),
  O('starwood', 'Starwood', 2016, '2016年に約136億ドルで買収。', '買収(2016年)'),
 ] + holders([('Vanguard', '5.4', M), ('BlackRock', '4.7', M)]),
 [('jwmarriott', 'billmarriott', 'link', '親子'), ('billmarriott', 'sorenson', 'link', '後任', 2012), ('sorenson', 'capuano', 'link', '後任', 2021), ('billmarriott', 'davidmarriott', 'link', '親族'), ('billmarriott', 'johnmarriott', 'link', '親族'), ('co', 'ritz', 'owns'), ('co', 'starwood', 'owns')],
 '1927年にルートビア店から始まったホテルの会社。創業家が約2割を持ち、2021年からアンソニー・カプアーノがCEOを務めています。')

# ---------------- General Dynamics ----------------
deep('GD', 'General Dynamics', 1899, NOTE + 'Longview Asset Managementは、クラウン家の投資会社として知られます。', [
  P('holland', 'ジョン・ホランド', 'John Holland', 1899, '近代的な潜水艦の設計者。Electric Boat(1899年)の源流。', '源流の設計者', 1914, 1),
  P('crown', 'ヘンリー・クラウン', 'Henry Crown', 1959, '1950年代に支配株主となった実業家。', '元大株主', 1990),
  P('chabraja', 'ニコラス・チャブラジャ', 'Nicholas Chabraja', 1993, '1997〜2009年にCEO。', '元CEO', 2009),
  P('jjohnson', 'ジェイ・ジョンソン', 'Jay Johnson', 2005, '2009〜2013年にCEO。', '元CEO', 2013),
  P('novakovic', 'フィービー・ノバコビッチ', 'Phebe Novakovic', 2001, '2013年からCEO兼会長。', '会長兼CEO'),
  P('deep', 'ダニー・ディープ', 'Danny Deep', 2000, '社長(英語版Wikipedia)。', '社長'),
  O('longview', 'Longview Asset Management', 2026, '約10%を持つ最大の株主(MarketScreener)。クラウン家の投資会社。', '最大の株主(約10%)', 'i'),
  O('bath', 'Bath Iron Works', 1995, '1995年に買収(造船)。', '買収(1995年)'),
  O('gulfstream', 'Gulfstream Aerospace', 1999, '1999年に約50億ドルで買収(ビジネスジェット)。', '買収(1999年)'),
  O('csra', 'CSRA', 2018, '2018年に約97億ドルで買収(ITサービス)。', '買収(2018年)'),
 ] + holders([('Vanguard', '6.2', M), ('BlackRock', '6.1', M), ('Newport Trust', '5.0', M)]),
 [('holland', 'crown', 'link', '会社を引き継ぐ'), ('crown', 'longview', 'link', '家族の投資会社'), ('chabraja', 'jjohnson', 'link', '後任'), ('jjohnson', 'novakovic', 'link', '後任', 2013), ('co', 'bath', 'owns'), ('co', 'gulfstream', 'owns'), ('co', 'csra', 'owns')],
 '1899年のElectric Boatを源流とする防衛の会社。2013年からフィービー・ノバコビッチがCEOを務めています。')

# ---------------- Equinix ----------------
deep('EQIX', 'Equinix', 1998, NOTE, [
  P('avery', 'アル・エイブリー', 'Al Avery', 1998, '共同創業者。', '共同創業者', 2002, 1),
  P('adelson', 'ジェイ・アデルソン', 'Jay Adelson', 1998, '共同創業者。のちDiggの創業者。', '共同創業者', 2005, 1),
  P('smith', 'スティーブ・スミス', 'Steve Smith', 2007, '2007〜2018年にCEO。', '元CEO', 2018),
  P('meyers', 'チャールズ・メイヤーズ', 'Charles Meyers', 2010, '2018〜2024年にCEO。', '元CEO', 2024),
  P('foxmartin', 'アデア・フォックス＝マーティン', 'Adaire Fox-Martin', 2024, '2024年6月からCEO兼社長。', 'CEO兼社長'),
  O('switchdata', 'Switch & Data', 2010, '2010年に約6.9億ドルで買収。', '買収(2010年)'),
  O('telecity', 'TelecityGroup', 2016, '2016年に約38億ドルで買収(欧州)。', '買収(2016年)'),
  O('verizondc', 'Verizonのデータセンター', 2017, '2017年に約36億ドルで買収。', '買収(2017年)'),
  O('mainone', 'MainOne', 2022, '2022年に買収(西アフリカ)。', '買収(2022年)'),
 ] + holders([('BlackRock', '8.6', M), ('Vanguard', '6.5', M), ('State Street', '6.1', M)]),
 [('avery', 'adelson', 'link', '共同創業'), ('smith', 'meyers', 'link', '後任', 2018), ('meyers', 'foxmartin', 'link', '後任', 2024), ('co', 'switchdata', 'owns'), ('co', 'telecity', 'owns'), ('co', 'verizondc', 'owns'), ('co', 'mainone', 'owns')],
 '1998年に創業したデータセンターの会社。2024年6月からアデア・フォックス＝マーティンがCEOを務めています。')

# ---------------- Fortinet ----------------
deep('FTNT', 'Fortinet', 2000, NOTE, [
  P('kenxie', 'ケン・シー', 'Ken Xie', 2000, '創業者でCEO兼会長。NetScreenの創業者でもあります。約7.9%を保有(MarketScreener)。', '創業者 / 会長兼CEO', None, 1),
  P('michaelxie', 'マイケル・シー', 'Michael Xie', 2000, '共同創業者でCTO。ケンの弟。約7.6%を保有(MarketScreener)。', '共同創業者 / CTO', None, 1),
  P('jensen', 'キース・ジェンセン', 'Keith Jensen', 2019, 'CFO(英語版Wikipedia)。', 'CFO'),
  O('netscreen', 'NetScreen', 1997, 'ケン・シー氏が先に創業した会社。2004年にJuniperが約40億ドルで買収。', 'シー氏の前の創業'),
  O('lacework', 'Lacework', 2024, '2024年に買収(クラウドセキュリティ)。', '買収(2024年)'),
  O('nextdlp', 'Next DLP', 2024, '2024年に買収。', '買収(2024年)'),
 ] + holders([('BlackRock', '6.4', M), ('Vanguard', '5.5', M), ('State Street', '4.0', M)]),
 [('kenxie', 'michaelxie', 'link', '共同創業(兄弟)'), ('kenxie', 'netscreen', 'link', '前に創業'), ('co', 'lacework', 'owns'), ('co', 'nextdlp', 'owns')],
 '2000年にシー兄弟が創業したネットワークセキュリティの会社。ケン・シーが会長兼CEOを務めています。')

# ---------------- BNY ----------------
deep('BNY', 'BNY', 1784, NOTE, [
  P('hamilton', 'アレクサンダー・ハミルトン', 'Alexander Hamilton', 1784, '1784年にBank of New Yorkを創設。のち初代米財務長官。', '創設者', 1804, 1),
  P('tmellon', 'トーマス・メロン', 'Thomas Mellon', 1869, '1869年にMellon Bankの前身を創業。', '源流の創業者', 1908, 1),
  P('kelly', 'ロバート・ケリー', 'Robert Kelly', 2007, '2007年の合併後、2011年までCEO。', '元CEO', 2011),
  P('hassell', 'ジェラルド・ハッセル', 'Gerald Hassell', 2011, '2011〜2017年にCEO。', '元CEO', 2017),
  P('scharf', 'チャールズ・シャーフ', 'Charles Scharf', 2017, '2017〜2019年にCEO。のちウェルズ・ファーゴCEO。', '元CEO', 2019),
  P('gibbons', 'トッド・ギボンズ', 'Todd Gibbons', 2019, '2019〜2022年にCEO。', '元CEO', 2022),
  P('vince', 'ロビン・ヴィンス', 'Robin Vince', 2022, '2022年7月からCEO。', 'CEO'),
  P('mcdonogh', 'ダーモット・マクドナー', 'Dermot McDonogh', 2022, 'CFO。', 'CFO'),
  O('bonny', 'Bank of New York', 1784, '1784年創業のBank of New York。', '源流(1784年)'),
  O('mellon', 'Mellon Financial', 2007, '2007年にBank of New Yorkと合併。', '合併(2007年)'),
 ] + holders([('Vanguard', '6.3', M), ('BlackRock', '5.8', M), ('State Street', '4.4', M)]),
 [('hamilton', 'bonny', 'link', '創設'), ('tmellon', 'mellon', 'link', '源流'), ('kelly', 'hassell', 'link', '後任'), ('hassell', 'scharf', 'link', '後任'), ('scharf', 'gibbons', 'link', '後任'), ('gibbons', 'vince', 'link', '後任', 2022), ('co', 'bonny', 'owns'), ('co', 'mellon', 'owns')],
 '1784年にアレクサンダー・ハミルトンが創設したBank of New Yorkと、Mellonが2007年に合併して誕生。2022年からロビン・ヴィンスがCEOを務めています。')
