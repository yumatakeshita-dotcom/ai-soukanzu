from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Kinder Morgan ----------------
deep('KMI', 'Kinder Morgan', 1997, NOTE, [
  P('kinder', 'リチャード・キンダー', 'Richard Kinder', 1997, '共同創業者。Enronの元社長。執行会長。約11.6%を保有(MarketScreener)。', '共同創業者 / 執行会長', None, 1),
  P('morgan', 'ビル・モーガン', 'Bill Morgan', 1997, '共同創業者。', '共同創業者', 2005, 1),
  P('dang', 'キム・ダン', 'Kim Dang', 2001, 'CEO。', 'CEO'),
  P('sanders', 'デックス・サンダース', 'Dax Sanders', 2012, '社長。', '社長'),
  P('michels', 'デビッド・ミシェルズ', 'David Michels', 2012, 'CFO。', 'CFO'),
  O('enron', 'Enron', 1997, 'キンダー氏が社長を務めた元の会社。', '前職の会社'),
  O('kn', 'KN Energy', 1999, '1999年に合併し、Kinder Morganに。', '合併(1999年)'),
  O('elpaso', 'El Paso', 2012, '2012年に約211億ドルで買収。', '買収(2012年)'),
 ] + holders([('BlackRock', '6.4', M), ('State Street', '5.9', M), ('Vanguard', '5.6', M)]),
 [('kinder', 'morgan', 'link', '共同創業'), ('kinder', 'enron', 'moved', '前職'), ('kinder', 'dang', 'link', 'CEOを任せる'), ('co', 'kn', 'owns'), ('co', 'elpaso', 'owns')],
 '1997年にリチャード・キンダー氏らが創業したパイプラインの会社。キム・ダンがCEOを務め、キンダー氏が約11.6%の筆頭株主です。')

# ---------------- Republic Services ----------------
deep('RSG', 'Republic Services', 1996, NOTE, [
  P('huizenga', 'ウェイン・ハイゼンガ', 'Wayne Huizenga', 1996, '創業者。Waste Management、Blockbuster、AutoNationも創業。', '創業者', 1998, 1),
  P('slager', 'ドン・スレイガー', 'Don Slager', 2008, '2011〜2023年にCEO。', '元CEO', 2023),
  P('vanderark', 'ジョン・ヴァンダー・アーク', 'Jon Vander Ark', 2011, '2023年からCEO兼社長。', 'CEO兼社長'),
  P('kadre', 'マヌエル・カドレ', 'Manuel Kadre', 2018, '会長。', '会長'),
  P('delghiaccio', 'ブライアン・デルギアッチョ', 'Brian DelGhiaccio', 2018, 'CFO。', 'CFO'),
  O('cascade', 'Cascade Investment', 2026, 'ビル・ゲイツ氏の資産管理会社。約38%を持つ最大の株主(MarketScreener)。', '最大の株主(約38.2%)', 'i'),
  O('allied', 'Allied Waste', 2008, '2008年に約61億ドルで買収・合併。', '買収(2008年)'),
  O('usecology', 'US Ecology', 2022, '2022年に約22億ドルで買収。', '買収(2022年)'),
  O('wm', 'Waste Management', 1998, '最大の競合。ハイゼンガ氏の別の創業会社。', '競合'),
 ] + holders([('BlackRock', '4.6', M), ('Vanguard', '4.3', M)]),
 [('huizenga', 'slager', 'link', '源流'), ('slager', 'vanderark', 'link', '後任', 2023), ('co', 'allied', 'owns'), ('co', 'usecology', 'owns'), ('co', 'wm', 'conflict', '競合'), ('huizenga', 'wm', 'link', '共同創業')],
 '1996年にウェイン・ハイゼンガ氏が創業した廃棄物処理の会社。2023年からジョン・ヴァンダー・アークがCEOを務め、ゲイツ氏のCascadeが約38%を持っています。')

# ---------------- Canadian National Railway ----------------
deep('CNI', 'Canadian National Railway', 1919, NOTE + 'TCIの株主提案(2022年)は報道に基づきます。', [
  P('harrison', 'ハンター・ハリソン', 'Hunter Harrison', 2003, '2003〜2009年にCEO。のちCP、CSXのCEO。', '元CEO', 2009),
  P('mongeau', 'クロード・モンジョー', 'Claude Mongeau', 1994, '2010〜2016年にCEO。', '元CEO', 2016),
  P('jobin', 'リュック・ジョバン', 'Luc Jobin', 2016, '2016〜2022年にCEO。', '元CEO', 2022),
  P('robinson', 'トレイシー・ロビンソン', 'Tracy Robinson', 2022, '2022年6月からCEO。', 'CEO'),
  P('bruder', 'ショーニーン・ブルーダー', 'Shauneen Bruder', 2014, '会長。', '会長'),
  O('gates', 'ゲイツ財団の信託', 2026, '約8.6%を持つ最大の株主(MarketScreener)。', '最大の株主(約8.6%)', 'i'),
  O('tci', 'TCI Fund Management', 2022, 'アクティビスト。2022年にCEO交代などを求めたと報じられています。', 'アクティビスト(2022年)', 'i'),
  O('ic', 'Illinois Central', 1998, '1998年に買収。', '買収(1998年)'),
  O('kcs', 'Kansas City Southern', 2021, '2021年に約336億ドルの買収を提案したが、CPが競り勝った。', '買収断念(2021年)'),
  O('cp', 'CPKC', 2021, '競合。KCSを買収した。', '競合'),
 ] + holders([('Royal Trust Corporation of Canada', '5.2', M), ('Fidelity', '3.2', M)]),
 [('harrison', 'mongeau', 'link', '後任', 2010), ('mongeau', 'jobin', 'link', '後任'), ('jobin', 'robinson', 'link', '後任', 2022), ('tci', 'jobin', 'conflict', '経営陣の刷新を要求', 2022), ('co', 'ic', 'owns'), ('co', 'kcs', 'link', '買収を断念'), ('co', 'cp', 'conflict', '競合')],
 '1919年に設立されたカナダの鉄道会社。2022年からトレイシー・ロビンソンがCEOを務め、ゲイツ財団の信託が約8.6%を持っています。')

# ---------------- Manulife ----------------
deep('MFC', 'Manulife', 1887, NOTE, [
  P('macdonald', 'ジョン・A・マクドナルド', 'John A. Macdonald', 1887, 'カナダ初代首相。1887年のManufacturers Life設立時の初代社長。', '初代社長', 1891, 1),
  P('guloien', 'ドナルド・グロイアン', 'Donald Guloien', 1990, '2009〜2017年にCEO。', '元CEO', 2017),
  P('gori', 'ロイ・ゴーリ', 'Roy Gori', 2017, '2017〜2025年にCEO。', '元CEO', 2025),
  P('witherington', 'フィル・ウィザリントン', 'Phil Witherington', 2014, '2025年5月からCEO。アジア事業の責任者から昇格。', 'CEO'),
  P('cassaday', 'ジョン・カッサバ', 'John Cassava', 2020, '会長(英語版Wikipedia)。', '会長'),
  O('hancock', 'John Hancock', 2004, '2004年に約110億ドルで買収。', '買収(2004年)'),
  O('royaltrust', 'Royal Trust Corporation of Canada', 2026, '約6.6%を持つ上位株主(MarketScreener)。RBCの信託子会社。', '株主(約6.6%)', 'i'),
 ] + holders([('BMO Bank NA', '3.2', M), ('Vanguard', '2.9', M)]),
 [('macdonald', 'guloien', 'link', '源流を継ぐ'), ('guloien', 'gori', 'link', '後任'), ('gori', 'witherington', 'link', '後任', 2025), ('co', 'hancock', 'owns')],
 '1887年に初代首相ジョン・A・マクドナルドを社長に設立された、カナダの保険大手。2025年5月からフィル・ウィザリントンがCEOを務めています。')

# ---------------- General Motors ----------------
deep('GM', 'General Motors', 1908, NOTE + 'GMの後継者の話(スターリング・アンダーソン氏など)は憶測の報道で、会社は否定しています。', [
  P('durant', 'ウィリアム・デュラント', 'William Durant', 1908, '1908年にGMを創業。', '創業者', 1920, 1),
  P('sloan', 'アルフレッド・スローン', 'Alfred Sloan', 1923, '1923〜1946年にCEO。近代的な経営を築きました。', '元CEO', 1946),
  P('wagoner', 'リック・ワゴナー', 'Rick Wagoner', 2000, '2000〜2009年にCEO。2009年の破綻で退任。', '元CEO', 2009),
  P('whitacre', 'エド・ウィテカー', 'Ed Whitacre', 2009, '2009〜2010年に会長兼CEO。AT&Tの元CEO。', '元会長', 2010),
  P('akerson', 'ダン・エイカーソン', 'Dan Akerson', 2010, '2010〜2014年にCEO。', '元CEO', 2014),
  P('barra', 'メアリー・バーラ', 'Mary Barra', 1980, '2014年からCEO(2016年から会長も)。', '会長兼CEO'),
  P('russo', 'パトリシア・ルッソ', 'Patricia Russo', 2016, '筆頭社外取締役。HPEの会長でもあります。', '筆頭社外取締役'),
  P('jacobson', 'ポール・ジェイコブソン', 'Paul Jacobson', 2017, 'CFO。', 'CFO'),
  O('usgov', '米国政府', 2009, '2009年の破綻手続きで約61%の株主に(2013年までに全株を売却)。', '株主(2009〜2013年)', 'i'),
  O('cruise', 'Cruise', 2016, '2016年に約10億ドルで買収(自動運転)。2024年12月に事業を終了。', '買収(2016年)'),
  O('att', 'AT&T', 2009, 'ウィテカー氏の前職。', '前職'),
 ] + holders([('Vanguard', '6.7', M), ('BlackRock', '6.3', M), ('State Street', '5.1', M)]),
 [('durant', 'sloan', 'link', '経営を引き継ぐ'), ('wagoner', 'whitacre', 'link', '後任', 2009), ('whitacre', 'akerson', 'link', '後任'), ('akerson', 'barra', 'link', '後任', 2014), ('whitacre', 'att', 'moved', '前職'), ('co', 'cruise', 'owns')],
 '1908年にウィリアム・デュラントが創業した自動車の会社。2014年からメアリー・バーラがCEOを務めています。')

# ---------------- FedEx ----------------
deep('FDX', 'FedEx', 1971, NOTE + 'FedEx Freightの分離(2026年6月予定)は報道に基づきます。', [
  P('fsmith', 'フレッド・スミス', 'Fred Smith', 1971, '創業者。Federal Expressを創業。2025年6月に亡くなりました。', '創業者', 2025, 1),
  P('subramaniam', 'ラジ・スブラマニアム', 'Raj Subramaniam', 1991, '2022年6月からCEO兼社長。', 'CEO兼社長'),
  P('martin', 'ブラッド・マーティン', 'Brad Martin', 2002, '執行会長(英語版Wikipedia)。', '会長(執行)'),
  P('dietrich', 'ジョン・ディートリッヒ', 'John Dietrich', 2019, 'CFO。', 'CFO'),
  O('estate', 'フレデリック・スミスの遺産', 2026, '約6.0%を持つ株主(MarketScreener)。', '株主(約6.0%)', 'i'),
  O('kinkos', "Kinko's", 2004, '2004年に約24億ドルで買収(FedEx Office)。', '買収(2004年)'),
  O('tnt', 'TNT Express', 2016, '2016年に約48億ユーロで買収。', '買収(2016年)'),
  O('freight', 'FedEx Freight', 2026, '2026年6月に分離する計画と報じられています。', '分離(予定)'),
 ] + holders([('BlackRock', '6.6', M), ('Vanguard', '6.0', M), ('State Street', '4.2', M)]),
 [('fsmith', 'subramaniam', 'link', '後継CEOを選ぶ', 2022), ('fsmith', 'estate', 'link', '遺産'), ('co', 'kinkos', 'owns'), ('co', 'tnt', 'owns'), ('co', 'freight', 'owns', '分離')],
 '1971年にフレッド・スミスが創業した物流の会社。2022年からラジ・スブラマニアムがCEOを務めています。')

# ---------------- Hewlett Packard Enterprise ----------------
deep('HPE', 'Hewlett Packard Enterprise', 1939, NOTE + 'Elliottの出資(2025年)は報道に基づきます。', [
  P('hewlett', 'ビル・ヒューレット', 'Bill Hewlett', 1939, '1939年にHPを共同創業。', '共同創業者', 1978, 1),
  P('packard', 'デイブ・パッカード', 'Dave Packard', 1939, '1939年にHPを共同創業。', '共同創業者', 1993, 1),
  P('whitman', 'メグ・ホイットマン', 'Meg Whitman', 2011, '2011〜2018年にHP、のちHPEのCEO。2015年の分割を主導。', '元CEO', 2018),
  P('neri', 'アントニオ・ネリ', 'Antonio Neri', 1995, '2018年2月からCEO。', 'CEO'),
  P('russo', 'パトリシア・ルッソ', 'Patricia Russo', 2015, '会長。GMの筆頭社外取締役でもあります。', '会長'),
  P('myers', 'マリー・マイヤーズ', 'Marie Myers', 2023, 'CFO。', 'CFO'),
  O('hp', 'Hewlett-Packard', 2015, '2015年にHP Inc.とHPEに分割。', '分割元(2015年)'),
  O('juniper', 'Juniper Networks', 2025, '2025年に約140億ドルで買収。', '買収(2025年)'),
  O('elliott', 'Elliott Management', 2025, '2025年に約15億ドルを出資し、取締役を求めたと報じられています。', '株主(2025年・報道)', 'i'),
 ] + holders([('Vanguard', '6.5', M), ('Vanguard Portfolio Mgmt', '5.5', M), ('State Street', '5.1', M)]),
 [('hewlett', 'packard', 'link', '共同創業'), ('whitman', 'neri', 'link', '後任', 2018), ('hp', 'whitman', 'link', '分割を主導'), ('co', 'hp', 'owns', '分割'), ('co', 'juniper', 'owns')],
 '2015年にHPから分離した企業向けIT機器の会社。2018年からアントニオ・ネリがCEOを務めています。')

# ---------------- Ross Stores ----------------
deep('ROST', 'Ross Stores', 1950, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('moldaw', 'スチュアート・モルダウ', 'Stuart Moldaw', 1982, '1982年に買収して再建した実業家。', '元会長', 1996),
  P('rentler', 'バーバラ・レントラー', 'Barbara Rentler', 1987, '2014〜2025年にCEO。', '元CEO', 2025),
  P('conroy', 'ジム・コンロイ', 'James Conroy', 2025, '2025年2月からCEO。', 'CEO'),
  P('bjorklund', 'ガナー・ビョークルンド', 'Gunnar Bjorklund', 1990, '執行会長。', '会長(執行)'),
  O('rossdress', 'Ross Dress for Less', 1982, 'オフプライスの小売店。', 'ブランド'),
 ] + holders([('BlackRock', '6.8', M), ('Vanguard', '6.6', M), ('State Street', '4.6', M)]),
 [('moldaw', 'rentler', 'link', '源流'), ('rentler', 'conroy', 'link', '後任', 2025), ('co', 'rossdress', 'owns')],
 'オフプライス小売のRoss Dress for Lessを運営する会社。2025年からジム・コンロイがCEOを務めています。')

# ---------------- United Rentals ----------------
deep('URI', 'United Rentals', 1997, NOTE, [
  P('jacobs', 'ブラッド・ジェイコブス', 'Brad Jacobs', 1997, '創業者。のちXPOなどを創業。', '創業者', 2007, 1),
  P('kneeland', 'マイケル・ニーランド', 'Michael Kneeland', 2008, '2008〜2019年にCEO。現在は会長。', '会長'),
  P('flannery', 'マシュー・フラナリー', 'Matthew Flannery', 1998, '2019年からCEO。', 'CEO'),
  P('grace', 'テッド・グレース', 'Ted Grace', 2013, 'CFO。', 'CFO'),
  O('rsc', 'RSC Holdings', 2012, '2012年に約42億ドルで買収。', '買収(2012年)'),
  O('neff', 'Neff', 2017, '2017年に約13億ドルで買収。', '買収(2017年)'),
  O('ahern', 'Ahern Rentals', 2022, '2022年に約20億ドルで買収。', '買収(2022年)'),
  O('xpo', 'XPO', 2011, 'ジェイコブス氏が後に創業した物流の会社。', '創業者の別会社'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.3', M), ('State Street', '4.8', M)]),
 [('jacobs', 'kneeland', 'link', '後任'), ('kneeland', 'flannery', 'link', '後任', 2019), ('jacobs', 'xpo', 'link', '創業'), ('co', 'rsc', 'owns'), ('co', 'neff', 'owns'), ('co', 'ahern', 'owns')],
 '1997年にブラッド・ジェイコブスが創業した建設機械レンタルの会社。2019年からマシュー・フラナリーがCEOを務めています。')
