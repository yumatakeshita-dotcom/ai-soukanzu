from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Johnson & Johnson ----------------
deep('JNJ', 'Johnson & Johnson', 1886, NOTE + 'タルク(ベビーパウダー)訴訟の件は、報道に基づく範囲です。', [
  P('rwjohnson', 'ロバート・ウッド・ジョンソン', 'Robert Wood Johnson I', 1886, '1886年に兄弟とニュージャージー州で創業。', '共同創業者', 1910, 1),
  P('jwjohnson', 'ジェームズ・ウッド・ジョンソン', 'James Wood Johnson', 1886, '共同創業者(兄)。', '共同創業者', 1932, 1),
  P('rwj2', 'ロバート・ウッド・ジョンソン2世', 'Robert Wood Johnson II', 1932, '1932〜1963年に社長。会社の理念「我が信条」を築きました。', '元社長', 1963),
  P('burke', 'ジェームズ・バーク', 'James Burke', 1976, '1976〜1989年にCEO。1982年のタイレノール事件の対応で知られます。', '元CEO', 1989),
  P('weldon', 'ウィリアム・ウェルドン', 'William Weldon', 2002, '2002〜2012年にCEO。', '元CEO', 2012),
  P('gorsky', 'アレックス・ゴルスキー', 'Alex Gorsky', 1988, '2012〜2022年にCEO。Appleの取締役も務める。', '元CEO', 2022),
  P('duato', 'ホアキン・デュアト', 'Joaquin Duato', 1989, '2022年1月からCEO(会長も)。', '会長兼CEO'),
  P('wolk', 'ジョセフ・ウォーク', 'Joseph Wolk', 2012, 'CFO。', 'CFO'),
  O('janssen', 'Janssen Pharmaceutica', 1961, '1961年に買収(ベルギー)。', '買収(1961年)'),
  O('actelion', 'Actelion', 2017, '2017年に約300億ドルで買収。', '買収(2017年)'),
  O('abiomed', 'Abiomed', 2022, '2022年に約166億ドルで買収。', '買収(2022年)'),
  O('shockwave', 'Shockwave Medical', 2024, '2024年に約131億ドルで買収。', '買収(2024年)'),
  O('kenvue', 'Kenvue', 2023, '2023年に消費者向け事業を分離・上場。', '分離(2023年)'),
 ] + holders([('BlackRock', '6.6', M), ('Vanguard', '6.5', M), ('State Street', '5.6', M)]),
 [('rwjohnson', 'jwjohnson', 'link', '兄弟で創業'), ('rwjohnson', 'rwj2', 'link', '親族'), ('burke', 'weldon', 'link'), ('weldon', 'gorsky', 'link', '後任'), ('gorsky', 'duato', 'link', '後任', 2022), ('co', 'janssen', 'owns'), ('co', 'actelion', 'owns'), ('co', 'abiomed', 'owns'), ('co', 'shockwave', 'owns'), ('co', 'kenvue', 'owns', '分離')],
 '1886年に創業したヘルスケアの会社。2022年からホアキン・デュアトがCEOを務めています。')

# ---------------- T-Mobile US ----------------
deep('TMUS', 'T-Mobile US', 2013, NOTE, [
  P('legere', 'ジョン・レジェール', 'John Legere', 2012, '2012〜2020年にCEO。', '元CEO', 2020),
  P('sievert', 'マイク・シーバート', 'Mike Sievert', 2012, '2020〜2025年にCEO。現在は副会長。', '副会長'),
  P('gopalan', 'スリニ・ゴパラン', 'Srini Gopalan', 2025, '2025年11月からCEO(英語版Wikipedia)。', 'CEO'),
  P('hottges', 'ティモテウス・ヘットゲス', 'Timotheus Hottges', 2013, '会長。ドイツテレコムのCEO。', '会長'),
  P('son', '孫正義', 'Masayoshi Son', 2020, 'Sprint合併後、T-Mobileの取締役を務めました(ソフトバンクグループ)。', '元取締役', 2021),
  O('dt', 'Deutsche Telekom', 2013, '約54.3%を持つ支配株主(MarketScreener)。', '支配株主(約54.3%)', 'i'),
  O('metropcs', 'MetroPCS', 2013, '2013年に合併して現在の形に。', '合併(2013年)'),
  O('sprint', 'Sprint', 2020, '2020年に約260億ドルで合併。', '合併(2020年)'),
  O('uscellular', 'UScellularの事業', 2025, '2025年に約44億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('softbank', 'ソフトバンクグループ', 2020, 'Sprintの親会社で、合併後にT-Mobile株を持ちました。', '元関係者'),
 ] + holders([('Invesco', '3.0', M), ('Vanguard', '2.7', M), ('BlackRock', '2.7', M)]),
 [('legere', 'sievert', 'link', '後任', 2020), ('sievert', 'gopalan', 'link', '後任', 2025), ('dt', 'hottges', 'link', '会長'), ('son', 'sprint', 'link', 'Sprintの親会社'), ('co', 'metropcs', 'owns'), ('co', 'sprint', 'owns'), ('co', 'uscellular', 'owns'), ('son', 'softbank', 'link', '創業者')],
 'ドイツテレコムが約54%を持つ米国の携帯通信会社。2025年11月からスリニ・ゴパランがCEOを務めています。')

# ---------------- Danaher ----------------
deep('DHR', 'Danaher', 1969, NOTE, [
  P('srales', 'スティーブン・レイルズ', 'Steven Rales', 1969, '創業者の1人。会長。約4.9%を保有(MarketScreener)。', '創業者 / 会長', None, 1),
  P('mrales', 'ミッチェル・レイルズ', 'Mitchell Rales', 1969, '創業者の1人。執行委員会の会長。', '創業者 / 執行委員会会長', None, 1),
  P('culp', 'ラリー・カルプ', 'Larry Culp', 1990, '2001〜2014年にCEO。のちGEのCEO。', '元CEO', 2014),
  P('joyce', 'トム・ジョイス', 'Tom Joyce', 1990, '2014〜2020年にCEO。', '元CEO', 2020),
  P('blair', 'ライナー・ブレア', 'Rainer Blair', 2005, '2020年9月からCEO。', '社長兼CEO'),
  O('pall', 'Pall', 2015, '2015年に約138億ドルで買収。', '買収(2015年)'),
  O('cepheid', 'Cepheid', 2016, '2016年に約40億ドルで買収。', '買収(2016年)'),
  O('fortive', 'Fortive', 2016, '2016年に分離。', '分離(2016年)'),
  O('gebio', 'GEバイオファーマ事業', 2020, '2020年に約214億ドルで買収。', '買収(2020年)'),
  O('abcam', 'Abcam', 2023, '2023年に約57億ドルで買収。', '買収(2023年)'),
  O('veralto', 'Veralto', 2023, '2023年に水質・製品識別事業を分離。', '分離(2023年)'),
 ] + holders([('Vanguard', '5.9', M), ('BlackRock', '5.4', M), ('Fidelity', '4.2', M)]),
 [('srales', 'mrales', 'link', '兄弟で創業'), ('srales', 'culp', 'link', 'CEOを任せる', 2001), ('culp', 'joyce', 'link', '後任'), ('joyce', 'blair', 'link', '後任', 2020), ('co', 'pall', 'owns'), ('co', 'cepheid', 'owns'), ('co', 'gebio', 'owns'), ('co', 'abcam', 'owns'), ('co', 'fortive', 'owns', '分離'), ('co', 'veralto', 'owns', '分離')],
 '1969年にレイルズ兄弟が創業したライフサイエンス・診断の会社。2020年からライナー・ブレアがCEOを務めています。')

# ---------------- American Tower ----------------
deep('AMT', 'American Tower', 1995, NOTE, [
  P('dodge', 'スティーブン・ドッジ', 'Steven Dodge', 1995, '創業者。American Radio Systemsから分離して設立。', '創業者', 2004, 1),
  P('taiclet', 'ジェームズ・テイクレット', 'James Taiclet', 2004, '2004〜2020年にCEO。のちLockheed MartinのCEO。', '元CEO', 2020),
  P('bartlett', 'トム・バートレット', 'Tom Bartlett', 2007, '2020〜2023年にCEO。', '元CEO', 2023),
  P('vondran', 'スティーブン・ヴォンドラン', 'Steven Vondran', 2014, '2024年からCEO兼社長(英語版Wikipedia)。', 'CEO兼社長'),
  P('smith', 'ロッド・スミス', 'Rod Smith', 2015, 'CFO。', 'CFO'),
  O('ars', 'American Radio Systems', 1995, '1995年に分離元となったラジオ会社。', '分離元(1995年)'),
  O('verizontowers', 'Verizonのタワー', 2015, '2015年に約51億ドルで買収。', '買収(2015年)'),
  O('telxius', 'Telxius', 2021, '2021年に約94億ドルで買収。', '買収(2021年)'),
  O('coresite', 'CoreSite', 2021, '2021年に約101億ドルで買収。', '買収(2021年)'),
  O('lockheed', 'Lockheed Martin', 2020, 'テイクレット氏が移ったCEO職。', '関連'),
 ] + holders([('BlackRock', '7.6', M), ('Vanguard', '6.5', M), ('Vanguard Portfolio Mgmt', '6.0', M)]),
 [('ars', 'dodge', 'link', '分離を主導'), ('dodge', 'taiclet', 'link', '後任', 2004), ('taiclet', 'bartlett', 'link', '後任', 2020), ('bartlett', 'vondran', 'link', '後任', 2024), ('taiclet', 'lockheed', 'moved', 'CEOに就任'), ('co', 'verizontowers', 'owns'), ('co', 'telxius', 'owns'), ('co', 'coresite', 'owns')],
 '1995年に設立された通信タワーのREIT。2024年からスティーブン・ヴォンドランがCEOを務めています。')

# ---------------- EOG Resources ----------------
deep('EOG', 'EOG Resources', 1985, NOTE + 'Encinoの買収(2025年)は報道に基づきます。', [
  P('papa', 'マーク・パパ', 'Mark Papa', 1999, '1999〜2013年にCEO。', '元CEO', 2013),
  P('thomas', 'ビル・トーマス', 'Bill Thomas', 1989, '2014〜2021年にCEO。', '元CEO', 2021),
  P('yacob', 'エズラ・ヤコブ', 'Ezra Yacob', 2004, '2021年10月からCEO。', 'CEO'),
  P('janssen', 'アン・ジャンセン', 'Ann Janssen', 2000, 'CFO。', 'CFO'),
  O('enron', 'Enron', 1985, 'Enron Oil & Gasとして1985年に設立され、1999年にEnronから分離。', '分離元(1999年)'),
  O('yates', 'Yates Petroleum', 2016, '2016年に約25億ドルで買収。', '買収(2016年)'),
  O('encino', 'Encino Acquisition Partners', 2025, '2025年に約56億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Capital Group', '10.6', M), ('BlackRock', '7.0', M), ('Vanguard', '6.6', M)]),
 [('enron', 'papa', 'link', '分離を主導'), ('papa', 'thomas', 'link', '後任'), ('thomas', 'yacob', 'link', '後任', 2021), ('co', 'enron', 'owns', '分離'), ('co', 'yates', 'owns'), ('co', 'encino', 'owns')],
 '1985年にEnronの石油・ガス部門として設立され、1999年に独立したシェールの会社。2021年からエズラ・ヤコブがCEOを務めています。')

# ---------------- Moody's ----------------
deep('MCO', "Moody's", 1909, NOTE, [
  P('moody', 'ジョン・ムーディー', 'John Moody', 1909, '1909年に創業(鉄道債の格付け)。', '創業者', 1958, 1),
  P('mcdaniel', 'レイ・マクダニエル', 'Ray McDaniel', 1987, '2005〜2020年にCEO。', '元CEO', 2020),
  P('fauber', 'ロブ・ファウバー', 'Rob Fauber', 2008, '2021年1月からCEO。', 'CEO'),
  P('forlenza', 'ヴィンセント・フォルレンザ', 'Vincent Forlenza', 2016, '会長。', '会長'),
  O('db', 'Dun & Bradstreet', 1962, '1962年に買収。2000年に分離。', '親会社(1962〜2000年)'),
  O('berkshire', 'Berkshire Hathaway', 2000, '2000年から保有。約14.2%を持つ最大の株主(MarketScreener)。', '最大の株主(約14.2%)', 'i'),
  O('bvd', 'Bureau van Dijk', 2017, '2017年に約33億ドルで買収。', '買収(2017年)'),
  O('rms', 'Risk Management Solutions', 2021, '2021年に約20億ドルで買収。', '買収(2021年)'),
  O('doj', '米司法省との和解', 2017, '2017年に金融危機前の格付けで約8.6億ドルの和解。', '和解(2017年)'),
 ] + holders([('Vanguard', '5.6', M), ('BlackRock', '5.2', M), ('State Street', '4.1', M)]),
 [('moody', 'mcdaniel', 'link', '源流を継ぐ'), ('mcdaniel', 'fauber', 'link', '後任', 2021), ('db', 'moody', 'link', '親会社'), ('co', 'db', 'owns', '分離'), ('co', 'bvd', 'owns'), ('co', 'rms', 'owns'), ('co', 'doj', 'link', '和解')],
 '1909年にジョン・ムーディーが創業した信用格付けの会社。2021年からロブ・ファウバーがCEOを務め、バークシャーが約14%を持っています。')

# ---------------- Ecolab ----------------
deep('ECL', 'Ecolab', 1923, NOTE, [
  P('osborn', 'メリット・オズボーン', 'Merritt Osborn', 1923, '1923年にセントポールでEconomics Laboratoryを創業。', '創業者', 1950, 1),
  P('baker', 'ダグ・ベーカー', 'Doug Baker', 1989, '2004〜2020年にCEO。', '元CEO', 2020),
  P('beck', 'クリストフ・ベック', 'Christophe Beck', 2004, '2021年1月からCEO(会長も)。', '会長兼CEO'),
  O('cascade', 'Cascade Investment', 2026, 'ビル・ゲイツ氏の資産管理会社。約10.4%を持つ最大の株主(MarketScreener)。', '最大の株主(約10.4%)', 'i'),
  O('henkel', 'Henkel', 1991, '1991年に欧州の合弁会社を設立(のち統合)。', '合弁(1991年)'),
  O('nalco', 'Nalco', 2011, '2011年に約54億ドルで買収。', '買収(2011年)'),
  O('purolite', 'Purolite', 2021, '2021年に約37億ドルで買収。', '買収(2021年)'),
 ] + holders([('Vanguard', '5.9', M), ('BlackRock', '5.4', M), ('JPMorgan Asset Mgmt', '5.2', M)]),
 [('osborn', 'baker', 'link', '源流を継ぐ'), ('baker', 'beck', 'link', '後任', 2021), ('co', 'henkel', 'link', '合弁'), ('co', 'nalco', 'owns'), ('co', 'purolite', 'owns')],
 '1923年に創業した水処理・衛生の会社。2021年からクリストフ・ベックがCEOを務め、ゲイツ氏のCascadeが約10%の最大の株主です。')

# ---------------- KKR ----------------
deep('KKR', 'KKR', 1976, NOTE, [
  P('kohlberg', 'ジェローム・コールバーグ', 'Jerome Kohlberg', 1976, '共同創業者。1987年に去りました。', '共同創業者', 1987, 1),
  P('kravis', 'ヘンリー・クラビス', 'Henry Kravis', 1976, '共同創業者。共同執行会長。約9.0%を保有(MarketScreener)。', '共同創業者 / 共同会長', None, 1),
  P('roberts', 'ジョージ・ロバーツ', 'George Roberts', 1976, '共同創業者。共同執行会長。約9.3%を保有(MarketScreener)。', '共同創業者 / 共同会長', None, 1),
  P('bae', 'ジョセフ・ベイ', 'Joseph Bae', 1996, '共同CEO(2021年から)。', '共同CEO'),
  P('nuttall', 'スコット・ヌタル', 'Scott Nuttall', 1996, '共同CEO(2021年から)。', '共同CEO'),
  O('rjr', 'RJR Nabisco', 1989, '1989年に約250億ドルでLBO。「野蛮な来訪者」で知られる。', 'LBO(1989年)'),
  O('toysrus', "Toys 'R' Us", 2005, '2005年にBain、Vornadoとともに買収。', 'LBO(2005年)'),
  O('txu', 'TXU(Energy Future Holdings)', 2007, '2007年に約450億ドルでLBO。のち破綻。', 'LBO(2007年)'),
  O('amphenol', 'Amphenol', 1997, '1997年に買収(のち再上場)。', 'LBO(1997年)'),
  O('globalatlantic', 'Global Atlantic', 2021, '2021年に約47億ドルで残りを取得(保険)。', '買収(2021年)'),
 ] + holders([('Vanguard', '5.0', M), ('Capital Group', '4.1', M), ('State Street', '3.3', M)]),
 [('kohlberg', 'kravis', 'link', '共同創業'), ('kravis', 'roberts', 'link', '従兄弟で共同創業'), ('kravis', 'bae', 'link', '共同CEOを任せる', 2021), ('co', 'rjr', 'owns'), ('co', 'toysrus', 'owns'), ('co', 'txu', 'owns'), ('co', 'amphenol', 'owns'), ('co', 'globalatlantic', 'owns')],
 '1976年にコールバーグ氏、クラビス氏、ロバーツ氏が創業した投資会社。2021年からベイ氏とヌタル氏が共同CEOを務めています。')

# ---------------- Agnico Eagle ----------------
deep('AEM', 'Agnico Eagle Mines', 1957, NOTE + '歴代の経営者以外の情報は少なく、確認できた範囲だけを載せています。', [
  P('boyd', 'ショーン・ボイド', 'Sean Boyd', 1996, '1998〜2023年にCEO。現在は会長。', '会長'),
  P('aljoundi', 'アンマー・アル＝ジョンディ', 'Ammar Al-Joundi', 2023, '2024年2月からCEO。', 'CEO'),
  O('agnico', 'Agnico', 1972, '1972年にEagleと合併して誕生。', '合併(1972年)'),
  O('kirkland', 'Kirkland Lake Gold', 2022, '2022年に約106億ドルで合併。', '合併(2022年)'),
  O('yamana', 'Yamana Goldの鉱山', 2023, '2023年にPan American Silverとともに約48億ドルで取得。', '買収(2023年)'),
 ] + holders([('Van Eck', '3.9', M), ('Capital Group', '3.9', M), ('Royal Trust Corporation of Canada', '3.1', M)]),
 [('boyd', 'aljoundi', 'link', '後任', 2024), ('co', 'agnico', 'owns'), ('co', 'kirkland', 'owns'), ('co', 'yamana', 'owns')],
 'カナダの金鉱山会社。2024年からアンマー・アル＝ジョンディがCEOを務め、ショーン・ボイドが会長です。')

# ---------------- Enterprise Products Partners ----------------
deep('EPD', 'Enterprise Products Partners', 1968, NOTE + '歴代の経営者以外の情報は少なく、確認できた範囲だけを載せています。', [
  P('duncan', 'ダン・ダンカン', 'Dan Duncan', 1968, 'EPCOの創業者。富豪としても知られ、2010年に亡くなりました。', '創業者', 2010, 1),
  P('fowler', 'ランドール・ファウラー', 'Randall Fowler', 2000, '共同CEO。', '共同CEO'),
  P('teague', 'A・J・ティーグ', 'A. J. Teague', 2000, '共同CEO。', '共同CEO'),
  P('rwilliams', 'ランダ・ウィリアムズ', 'Randa Williams', 2010, 'ダン・ダンカンの娘。約1.1%を保有(MarketScreener)。', '創業家の株主'),
  O('epco', 'EPCO', 1968, 'ダンカン家の持株会社。約31.5%を持つ最大の株主(MarketScreener)。', '最大の株主(約31.5%)', 'i'),
  O('teppco', 'TEPPCO', 2009, '2009年に約33億ドルで統合。', '統合(2009年)'),
  O('oiltanking', 'Oiltanking Partners', 2014, '2014年に約60億ドルで統合。', '統合(2014年)'),
 ] + holders([('ALPS Advisors', '2.0', M), ('Invesco', '1.2', M)]),
 [('duncan', 'fowler', 'link', '経営を託す'), ('duncan', 'rwilliams', 'link', '親子'), ('duncan', 'epco', 'link', '創業'), ('co', 'teppco', 'owns'), ('co', 'oiltanking', 'owns')],
 'ダン・ダンカンが創業したパイプライン・天然ガス液の会社。創業家のEPCOが約31.5%を持っています。')
