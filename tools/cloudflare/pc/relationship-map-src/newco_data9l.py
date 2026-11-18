from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Medtronic ----------------
deep('MDT', 'Medtronic', 1949, NOTE, [
  P('bakken', 'アール・バッケン', 'Earl Bakken', 1949, '共同創業者。心臓ペースメーカーの先駆者。', '共同創業者', 1989, 1),
  P('hermundslie', 'パーマー・ハーマンズリー', 'Palmer Hermundslie', 1949, '共同創業者。', '共同創業者', 1976, 1),
  P('bgeorge', 'ビル・ジョージ', 'Bill George', 1991, '1991〜2001年にCEO。', '元CEO', 2001),
  P('collins', 'アート・コリンズ', 'Art Collins', 1992, '2001〜2007年にCEO。', '元CEO', 2007),
  P('hawkins', 'ビル・ホーキンス', 'Bill Hawkins', 2007, '2007〜2011年にCEO。', '元CEO', 2011),
  P('ishrak', 'オマー・イシュラク', 'Omar Ishrak', 2011, '2011〜2020年にCEO。', '元CEO', 2020),
  P('martha', 'ジェフ・マーサ', 'Geoff Martha', 2002, '2020年4月からCEO(会長も)。', '会長兼CEO'),
  P('parkhill', 'カレン・パークヒル', 'Karen Parkhill', 2019, 'CFO。', 'CFO'),
  O('sofamor', 'Sofamor Danek', 1999, '1999年に約36億ドルで買収。', '買収(1999年)'),
  O('kyphon', 'Kyphon', 2007, '2007年に約39億ドルで買収。', '買収(2007年)'),
  O('covidien', 'Covidien', 2015, '2015年に約499億ドルで買収。本社をアイルランドへ移す合併。', '買収(2015年)'),
  O('mazor', 'Mazor Robotics', 2018, '2018年に約16億ドルで買収。', '買収(2018年)'),
 ] + holders([('BlackRock', '6.6', M), ('Vanguard', '6.6', M), ('State Street', '5.0', M)]),
 [('bakken', 'hermundslie', 'link', '共同創業'), ('bgeorge', 'collins', 'link', '後任'), ('collins', 'hawkins', 'link', '後任'), ('hawkins', 'ishrak', 'link', '後任'), ('ishrak', 'martha', 'link', '後任', 2020), ('co', 'sofamor', 'owns'), ('co', 'kyphon', 'owns'), ('co', 'covidien', 'owns'), ('co', 'mazor', 'owns')],
 '1949年にミネアポリスで創業した医療機器の会社。2020年からジェフ・マーサがCEOを務めています。')

# ---------------- Capital One ----------------
deep('COF', 'Capital One', 1994, NOTE, [
  P('fairbank', 'リチャード・フェアバンク', 'Richard Fairbank', 1994, '共同創業者。創業から会長兼CEO。', '共同創業者 / 会長兼CEO', None, 1),
  P('morris', 'ナイジェル・モリス', 'Nigel Morris', 1994, '共同創業者。', '共同創業者', 2004, 1),
  P('young', 'アンドリュー・ヤング', 'Andrew Young', 2020, 'CFO。', 'CFO'),
  P('yajnik', 'サンジブ・ヤジニク', 'Sanjiv Yajnik', 2000, '金融サービス部門の社長。', '部門社長'),
  O('signet', 'Signet Bank', 1994, '1994年に分離して誕生した元の親会社(バージニア州)。', '分離元(1994年)'),
  O('hibernia', 'Hibernia', 2005, '2005年に約53億ドルで買収。', '買収(2005年)'),
  O('northfork', 'North Fork Bancorp', 2006, '2006年に約132億ドルで買収。', '買収(2006年)'),
  O('ingdirect', 'ING Direct USA', 2012, '2012年に約90億ドルで買収。', '買収(2012年)'),
  O('discover', 'Discover Financial Services', 2025, '2025年5月に約350億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.4', M), ('BlackRock', '5.5', M), ('State Street', '4.3', M)]),
 [('fairbank', 'morris', 'link', '共同創業'), ('signet', 'fairbank', 'link', '社内ベンチャー'), ('co', 'hibernia', 'owns'), ('co', 'northfork', 'owns'), ('co', 'ingdirect', 'owns'), ('co', 'discover', 'owns')],
 '1994年にリチャード・フェアバンクらが創業したクレジットカードの会社。フェアバンクが創業から会長兼CEOを務めています。')

# ---------------- Spotify ----------------
deep('SPOT', 'Spotify', 2006, NOTE, [
  P('ek', 'ダニエル・エク', 'Daniel Ek', 2006, '共同創業者。2025年までCEO。以後は執行会長。約5.8%を保有(MarketScreener)。', '共同創業者 / 会長(執行)', None, 1),
  P('lorentzon', 'マーティン・ローレンツォン', 'Martin Lorentzon', 2006, '共同創業者。約9.2%を保有(MarketScreener)。', '共同創業者', None, 1),
  P('norstrom', 'アレックス・ノルストローム', 'Alex Norstrom', 2012, '共同CEO(2026年1月から)。', '共同CEO'),
  P('soderstrom', 'グスタフ・ソダーストローム', 'Gustav Soderstrom', 2009, '共同CEO(2026年1月から)。', '共同CEO'),
  P('luiga', 'クリスチャン・ルイガ', 'Christian Luiga', 2024, 'CFO。', 'CFO'),
  O('tencent', 'Tencent', 2017, '2017年に株式を交換。約8.1%を持つ上位株主(MarketScreener)。', '株主(約8.1%)', 'i'),
  O('baillie', 'Baillie Gifford', 2026, '約3.9%を持つ上位株主(MarketScreener)。', '株主(約3.9%)', 'i'),
  O('echonest', 'The Echo Nest', 2014, '2014年に約1億ドルで買収。', '買収(2014年)'),
  O('gimlet', 'Gimlet Media', 2019, '2019年に約2.3億ドルで買収(ポッドキャスト)。', '買収(2019年)'),
  O('ringer', 'The Ringer', 2020, '2020年に約1.96億ドルで買収。', '買収(2020年)'),
  O('megaphone', 'Megaphone', 2020, '2020年に約2.35億ドルで買収。', '買収(2020年)'),
  O('findaway', 'Findaway', 2022, '2022年に買収(オーディオブック)。', '買収(2022年)'),
 ] + holders([('BlackRock', '3.9', M)]),
 [('ek', 'lorentzon', 'link', '共同創業'), ('ek', 'norstrom', 'link', '共同CEOを任せる', 2026), ('ek', 'soderstrom', 'link', '共同CEOを任せる', 2026), ('co', 'echonest', 'owns'), ('co', 'gimlet', 'owns'), ('co', 'ringer', 'owns'), ('co', 'megaphone', 'owns'), ('co', 'findaway', 'owns')],
 '2006年にスウェーデンでダニエル・エクらが創業した音楽配信の会社。2026年からノルストローム氏とソダーストローム氏が共同CEOを務めています。')

# ---------------- Prologis ----------------
deep('PLD', 'Prologis', 1983, NOTE, [
  P('moghadam', 'ハミド・モガダム', 'Hamid Moghadam', 1983, 'AMB Propertyの共同創業者。長くCEOを務め、現在は執行会長。', '会長(執行)'),
  P('letter', 'ダン・レッター', 'Dan Letter', 2011, '現CEO(英語版Wikipedia)。', 'CEO'),
  P('andrus', 'カーター・アンドラス', 'Carter Andrus', 2011, 'COO。', 'COO'),
  P('arndt', 'ティム・アーント', 'Tim Arndt', 2011, 'CFO。', 'CFO'),
  O('amb', 'AMB Property', 2011, '2011年にProLogisと合併して現在の形に。', '合併(2011年)'),
  O('liberty', 'Liberty Property Trust', 2020, '2020年に約126億ドルで買収。', '買収(2020年)'),
  O('duke', 'Duke Realty', 2022, '2022年に約260億ドルで買収。', '買収(2022年)'),
 ] + holders([('Vanguard', '13.6', M), ('BlackRock', '8.2', M), ('State Street', '5.9', M)]),
 [('moghadam', 'letter', 'link', 'CEOを譲る'), ('amb', 'moghadam', 'link', '共同創業'), ('co', 'amb', 'owns'), ('co', 'liberty', 'owns'), ('co', 'duke', 'owns')],
 '物流施設のREIT大手。ハミド・モガダムが共同創業したAMB PropertyとProLogisが2011年に合併して誕生しました。')

# ---------------- Bank of Montreal ----------------
deep('BMO', 'Bank of Montreal', 1817, NOTE, [
  P('comper', 'トニー・コンパー', 'Tony Comper', 1999, '1999〜2007年にCEO。', '元CEO', 2007),
  P('downe', 'ビル・ダウニー', 'Bill Downe', 2007, '2007〜2017年にCEO。', '元CEO', 2017),
  P('white', 'ダリル・ホワイト', 'Darryl White', 2017, '2017年11月からCEO。', 'CEO'),
  P('cope', 'ジョージ・コープ', 'George Cope', 2019, '会長。BCEの元CEO。', '会長'),
  O('montrealbank', 'Montreal Bank', 1817, '1817年に創業(カナダ最古の銀行)。', '源流(1817年)'),
  O('harris', 'Harris Bank', 1984, '1984年に買収(シカゴ)。', '買収(1984年)'),
  O('mi', 'Marshall & Ilsley', 2011, '2011年に約41億ドルで買収。', '買収(2011年)'),
  O('bankwest', 'Bank of the West', 2023, '2023年に約163億ドルでBNPパリバから買収。', '買収(2023年)'),
  O('royaltrust', 'Royal Trust Corporation of Canada', 2026, '約7.5%を持つ(MarketScreener)。RBCの信託子会社。', '株主(約7.5%)', 'i'),
 ] + holders([('BMO Bank NA', '3.8', M), ('Vanguard', '2.9', M)]),
 [('montrealbank', 'comper', 'link', '源流を継ぐ'), ('comper', 'downe', 'link', '後任'), ('downe', 'white', 'link', '後任', 2017), ('co', 'harris', 'owns'), ('co', 'mi', 'owns'), ('co', 'bankwest', 'owns')],
 '1817年に創業したカナダ最古の銀行。2017年からダリル・ホワイトがCEOを務めています。')

# ---------------- Starbucks ----------------
deep('SBUX', 'Starbucks', 1971, NOTE, [
  P('baldwin', 'ジェリー・ボールドウィン', 'Jerry Baldwin', 1971, '1971年にシアトルで共同創業。', '共同創業者', 1987, 1),
  P('siegl', 'ゼブ・シーゲル', 'Zev Siegl', 1971, '共同創業者。', '共同創業者', 1980, 1),
  P('bowker', 'ゴードン・バウカー', 'Gordon Bowker', 1971, '共同創業者。', '共同創業者', 1993, 1),
  P('schultz', 'ハワード・シュルツ', 'Howard Schultz', 1982, '1987年に買収し、1986〜2000年、2008〜2017年にCEO。名誉会長。', '名誉会長'),
  P('smith', 'オーリン・スミス', 'Orin Smith', 1990, '2000〜2005年にCEO。', '元CEO', 2005),
  P('donald', 'ジム・ドナルド', 'Jim Donald', 2002, '2005〜2008年にCEO。', '元CEO', 2008),
  P('johnson', 'ケビン・ジョンソン', 'Kevin Johnson', 2009, '2017〜2022年にCEO。', '元CEO', 2022),
  P('narasimhan', 'ラクシュマン・ナラシンハン', 'Laxman Narasimhan', 2022, '2022〜2024年にCEO。', '元CEO', 2024),
  P('niccol', 'ブライアン・ニコル', 'Brian Niccol', 2024, '2024年9月からCEO兼会長。チポトレの元CEO。', '会長兼CEO'),
  P('ruggeri', 'レイチェル・ルジェリ', 'Rachel Ruggeri', 2018, 'CFO。', 'CFO'),
  O('teavana', 'Teavana', 2012, '2012年に約6.2億ドルで買収。', '買収(2012年)'),
  O('laboulange', 'La Boulange', 2012, '2012年に買収(のち閉鎖)。', '買収(2012年)'),
  O('chipotle', 'Chipotle', 2024, 'ニコル氏の前職。', '前職'),
 ] + holders([('Capital Group', '9.6', M), ('Vanguard', '6.5', M), ('BlackRock', '5.6', M)]),
 [('baldwin', 'siegl', 'link', '共同創業'), ('baldwin', 'bowker', 'link', '共同創業'), ('schultz', 'baldwin', 'link', '1987年に買収', 1987), ('smith', 'donald', 'link', '後任'), ('johnson', 'narasimhan', 'link', '後任'), ('narasimhan', 'niccol', 'link', '後任', 2024), ('niccol', 'chipotle', 'moved', '前職'), ('co', 'teavana', 'owns'), ('co', 'laboulange', 'owns')],
 '1971年にシアトルで3人が創業したコーヒーチェーン。2024年9月からブライアン・ニコルがCEOを務めています。')

# ---------------- Lowe's ----------------
deep('LOW', "Lowe's", 1921, NOTE + 'FBMとArtisanの買収(2025年)は報道に基づきます。', [
  P('llowe', 'ルーシャス・スミス・ロウ', 'Lucius Smith Lowe', 1921, '1921年にノースカロライナ州で創業。', '創業者', 1940, 1),
  P('tillman', 'ロバート・ティルマン', 'Robert Tillman', 1996, '1996〜2011年にCEO。', '元CEO', 2011),
  P('niblock', 'ロバート・ニブロック', 'Robert Niblock', 2005, '2005〜2018年にCEO。', '元CEO', 2018),
  P('ellison', 'マービン・エリソン', 'Marvin Ellison', 2018, '2018年7月からCEO兼会長。', '会長兼CEO'),
  P('sink', 'ブランドン・シンク', 'Brandon Sink', 2018, 'CFO。', 'CFO'),
  O('maintenance', 'Maintenance Supply Headquarters', 2017, '2017年に約5億ドルで買収。', '買収(2017年)'),
  O('fbm', 'Foundation Building Materials', 2025, '2025年に約88億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('artisan', 'Artisan Design Group', 2025, '2025年に約13億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('homedepot', 'Home Depot', 1978, '最大の競合。', '競合'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.4', M), ('State Street', '5.1', M)]),
 [('llowe', 'tillman', 'link', '源流'), ('tillman', 'niblock', 'link', '後任'), ('niblock', 'ellison', 'link', '後任', 2018), ('co', 'maintenance', 'owns'), ('co', 'fbm', 'owns'), ('co', 'artisan', 'owns'), ('co', 'homedepot', 'conflict', '競合')],
 '1921年にノースカロライナ州で創業した住宅リフォーム小売の会社。2018年からマービン・エリソンがCEOを務めています。')

# ---------------- ADP ----------------
deep('ADP', 'ADP', 1949, NOTE, [
  P('taub', 'ヘンリー・タウブ', 'Henry Taub', 1949, '1949年にAutomatic Payrollsを創業。', '創業者', 1998, 1),
  P('rodriguez', 'カルロス・ロドリゲス', 'Carlos Rodriguez', 1999, '2011〜2022年にCEO。', '元CEO', 2022),
  P('black', 'マリア・ブラック', 'Maria Black', 2022, '2022年11月からCEO。', 'CEO'),
  P('hadley', 'ピーター・ハドリー', 'Peter Hadley', 2021, 'CFO。', 'CFO'),
  P('ackman', 'ビル・アックマン', 'Bill Ackman', 2017, 'Pershing Squareを率いる投資家。2017年に取締役の座を求めて争い、敗れました。', 'アクティビスト'),
  O('celergo', 'Celergo', 2017, '2017年に買収。', '買収(2017年)'),
  O('workmarket', 'WorkMarket', 2018, '2018年に買収。', '買収(2018年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.5', M), ('State Street', '5.2', M)]),
 [('taub', 'rodriguez', 'link', '源流'), ('rodriguez', 'black', 'link', '後任', 2022), ('ackman', 'co', 'conflict', '取締役の座を求めて争う', 2017), ('co', 'celergo', 'owns'), ('co', 'workmarket', 'owns')],
 '1949年にヘンリー・タウブが創業した給与計算・人事の会社。2022年からマリア・ブラックがCEOを務めています。')

# ---------------- McKesson ----------------
deep('MCK', 'McKesson', 1833, NOTE, [
  P('mckesson', 'ジョン・マッケソン', 'John McKesson', 1833, '1833年にニューヨークで創業。', '創業者', 1850, 1),
  P('olcott', 'チャールズ・オルコット', 'Charles Olcott', 1833, '共同創業者。', '共同創業者', 1850, 1),
  P('hammergren', 'ジョン・ハマーグレン', 'John Hammergren', 1996, '1999〜2019年にCEO。', '元CEO', 2019),
  P('tyler', 'ブライアン・タイラー', 'Brian Tyler', 2018, '2019年4月からCEO。', 'CEO'),
  P('knauss', 'ドナルド・クナウス', 'Donald Knauss', 2013, '会長。', '会長'),
  O('celesio', 'Celesio', 2014, '2014年に約83億ドルで買収(ドイツ)。', '買収(2014年)'),
  O('rexall', 'Rexall Health', 2017, '2017年に買収(カナダ)。', '買収(2017年)'),
  O('opioid', 'オピオイド訴訟', 2022, '2022年にオピオイド問題で約74億ドルの和解に合意と報じられています。', '和解(2022年)'),
 ] + holders([('BlackRock', '6.9', M), ('Vanguard', '6.7', M), ('State Street', '4.9', M)]),
 [('mckesson', 'olcott', 'link', '共同創業'), ('hammergren', 'tyler', 'link', '後任', 2019), ('co', 'celesio', 'owns'), ('co', 'rexall', 'owns'), ('co', 'opioid', 'link', '和解')],
 '1833年創業の医薬品卸の会社。2019年からブライアン・タイラーがCEOを務めています。')

# ---------------- Canadian Natural Resources ----------------
deep('CNQ', 'Canadian Natural Resources', 1973, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('edwards', 'マーレー・エドワーズ', 'Murray Edwards', 1989, '会長。', '会長'),
  P('stauth', 'スコット・ストース', 'Scott Stauth', 2000, '社長(英語版Wikipedia)。', '社長'),
  O('albian', 'Albian Sands', 2017, '2017年にシェルの持ち分などを約85億カナダドルで取得。', '買収(2017年)'),
  O('devon', 'Devonのカナダ事業', 2019, '2019年に約28億ドルで取得。', '買収(2019年)'),
  O('capital', 'Capital Group', 2026, '約10.7%を持つ上位株主(MarketScreener)。', '株主(約10.7%)', 'i'),
 ] + holders([('Royal Trust Corporation of Canada', '6.7', M)]),
 [('edwards', 'stauth', 'link', '経営陣'), ('co', 'albian', 'owns'), ('co', 'devon', 'owns')],
 'カナダ最大級の石油・ガスの会社。マーレー・エドワーズが会長を務めています。')
