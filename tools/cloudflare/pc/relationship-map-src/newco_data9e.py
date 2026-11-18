from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- UnitedHealth ----------------
deep('UNH', 'UnitedHealth Group', 1977, NOTE, [
  P('burke', 'リチャード・バーク', 'Richard Burke', 1977, 'UnitedHealthcareの創業者。', '創業者', 1989, 1),
  P('mcguire', 'ウィリアム・マクガイア', 'William McGuire', 1991, '1991〜2006年にCEO。ストックオプション問題で退任。', '元CEO', 2006),
  P('hemsley', 'スティーブン・ヘムズリー', 'Stephen Hemsley', 1997, '2006〜2017年にCEO。2025年5月にCEOへ復帰し、会長兼CEO。', '会長兼CEO'),
  P('wichmann', 'デイブ・ウィックマン', 'Dave Wichmann', 1998, '2017〜2021年にCEO。', '元CEO', 2021),
  P('witty', 'アンドリュー・ウィティ', 'Andrew Witty', 2021, '2021〜2025年にCEO。', '元CEO', 2025),
  P('deveydt', 'ウェイン・デベイト', 'Wayne DeVeydt', 2025, 'CFO。', 'CFO'),
  P('noel', 'ティム・ノエル', 'Tim Noel', 2000, 'UnitedHealthcareのCEO。', '部門CEO'),
  O('pacificare', 'PacifiCare', 2005, '2005年に約81億ドルで買収。', '買収(2005年)'),
  O('sierra', 'Sierra Health', 2008, '2008年に約26億ドルで買収。', '買収(2008年)'),
  O('lhc', 'LHC Group', 2023, '2023年に約54億ドルで買収。', '買収(2023年)'),
  O('change', 'Change Healthcare', 2022, '2022年に約130億ドルで買収。', '買収(2022年)'),
  O('amedisys', 'Amedisys', 2025, '2025年に約33億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.3', M), ('State Street', '5.1', M)]),
 [('burke', 'mcguire', 'link', '後任'), ('mcguire', 'hemsley', 'link', '後任', 2006), ('hemsley', 'wichmann', 'link', '後任', 2017), ('wichmann', 'witty', 'link', '後任', 2021), ('witty', 'hemsley', 'link', 'CEOに復帰', 2025), ('co', 'pacificare', 'owns'), ('co', 'sierra', 'owns'), ('co', 'lhc', 'owns'), ('co', 'change', 'owns'), ('co', 'amedisys', 'owns')],
 '1977年創業の医療保険の会社。2025年5月にスティーブン・ヘムズリーがCEOに復帰しました。')

# ---------------- Bank of America ----------------
deep('BAC', 'Bank of America', 1904, NOTE, [
  P('giannini', 'アマデオ・ジャンニーニ', 'Amadeo Giannini', 1904, '1904年にBank of Italy(のちBank of America)を創業。', '創業者', 1949, 1),
  P('mccoll', 'ヒュー・マッコール', 'Hugh McColl', 1983, 'NationsBankのCEO。1998年の合併を主導。', '元CEO', 2001),
  P('lewis', 'ケン・ルイス', 'Ken Lewis', 2001, '2001〜2009年にCEO。', '元CEO', 2009),
  P('moynihan', 'ブライアン・モイニハン', 'Brian Moynihan', 2004, '2010年からCEO、2014年から会長。', '会長兼CEO'),
  P('thompson', 'ブルース・トンプソン', 'Bruce Thompson', 2010, '副会長(英語版Wikipedia)。', '副会長'),
  P('borthwick', 'アラステア・ボースウィック', 'Alastair Borthwick', 2021, 'CFO。', 'CFO'),
  O('berkshire', 'Berkshire Hathaway', 2011, '2011年に50億ドルを出資。約6.9%を持つ上位株主(MarketScreener、2026年11月)。', '株主(約6.9%)', 'i'),
  O('nationsbank', 'NationsBank', 1998, '1998年に合併。', '合併(1998年)'),
  O('fleet', 'FleetBoston', 2004, '2004年に約470億ドルで買収。', '買収(2004年)'),
  O('mbna', 'MBNA', 2005, '2005年に約350億ドルで買収。', '買収(2005年)'),
  O('countrywide', 'Countrywide', 2008, '2008年に約40億ドルで買収。', '買収(2008年)'),
  O('merrill', 'Merrill Lynch', 2008, '2008年に約500億ドルで買収。', '買収(2008年)'),
 ] + holders([('Vanguard', '6.0', M), ('State Street', '4.3', M), ('Vanguard Portfolio Mgmt', '2.5', M)]),
 [('giannini', 'mccoll', 'link', '源流を継ぐ'), ('mccoll', 'lewis', 'link', '後任'), ('lewis', 'moynihan', 'link', '後任', 2010), ('mccoll', 'nationsbank', 'moved'), ('co', 'nationsbank', 'owns'), ('co', 'fleet', 'owns'), ('co', 'mbna', 'owns'), ('co', 'countrywide', 'owns'), ('co', 'merrill', 'owns')],
 '1904年のBank of Italyを源流とする銀行。2010年からブライアン・モイニハンがCEOを務めています。')

# ---------------- Intel ----------------
deep('INTC', 'Intel', 1968, NOTE + '米国政府、ソフトバンク、エヌビディアの出資(2025年)は報道に基づきます。', [
  P('noyce', 'ロバート・ノイス', 'Robert Noyce', 1968, '共同創業者。集積回路の発明者の1人。', '共同創業者', 1990, 1),
  P('moore', 'ゴードン・ムーア', 'Gordon Moore', 1968, '共同創業者。「ムーアの法則」で知られます。', '共同創業者', 2006, 1),
  P('grove', 'アンディ・グローブ', 'Andy Grove', 1968, '1987〜1998年にCEO。', '元CEO', 1998),
  P('barrett', 'クレイグ・バレット', 'Craig Barrett', 1974, '1998〜2005年にCEO。', '元CEO', 2005),
  P('otellini', 'ポール・オッテリーニ', 'Paul Otellini', 1974, '2005〜2013年にCEO。', '元CEO', 2013),
  P('krzanich', 'ブライアン・クルザニッチ', 'Brian Krzanich', 1982, '2013〜2018年にCEO。', '元CEO', 2018),
  P('swan', 'ボブ・スワン', 'Bob Swan', 2016, '2019〜2021年にCEO。', '元CEO', 2021),
  P('gelsinger', 'パット・ゲルシンガー', 'Pat Gelsinger', 1979, '2021〜2024年12月にCEO。', '元CEO', 2025),
  P('tan', 'リップブー・タン', 'Lip-Bu Tan', 2025, '2025年3月からCEO。', 'CEO'),
  P('yeary', 'フランク・イアリー', 'Frank Yeary', 2009, '会長。', '会長'),
  P('zinsner', 'デビッド・ジンスナー', 'David Zinsner', 2022, 'CFO。', 'CFO'),
  O('mcafee', 'McAfee', 2010, '2010年に約77億ドルで買収(のち売却)。', '買収(2010年)'),
  O('altera', 'Altera', 2015, '2015年に約167億ドルで買収。', '買収(2015年)'),
  O('mobileye', 'Mobileye', 2017, '2017年に約153億ドルで買収(のち上場)。', '買収(2017年)'),
  O('habana', 'Habana Labs', 2019, '2019年に約20億ドルで買収。', '買収(2019年)'),
  O('usgov', '米国政府', 2025, '2025年8月に約10%の株式を取得と報じられています。', '株主(2025年・報道)', 'i'),
  O('softbank', 'ソフトバンクグループ', 2025, '2025年8月に20億ドルを出資と報じられています。', '出資者(2025年・報道)', 'i'),
  O('nvidia', 'Nvidia', 2025, '2025年に50億ドルを出資と報じられ、約4.3%を持つ(Yahoo Finance)。', '株主(約4.3%)', 'i'),
 ] + holders([('BlackRock', '8.5', Y), ('Vanguard', '5.7', Y)]),
 [('noyce', 'moore', 'link', '共同創業'), ('moore', 'grove', 'link'), ('grove', 'barrett', 'link', '後任'), ('barrett', 'otellini', 'link', '後任'), ('otellini', 'krzanich', 'link', '後任'), ('krzanich', 'swan', 'link', '後任'), ('swan', 'gelsinger', 'link', '後任', 2021), ('gelsinger', 'tan', 'link', '後任', 2025),
  ('co', 'mcafee', 'owns'), ('co', 'altera', 'owns'), ('co', 'mobileye', 'owns'), ('co', 'habana', 'owns')],
 '1968年にノイスとムーアが創業した半導体の会社。2025年3月からリップブー・タンがCEOを務め、2025年に米国政府などの出資を受けました。')

# ---------------- Home Depot ----------------
deep('HD', 'Home Depot', 1978, NOTE, [
  P('marcus', 'バーニー・マーカス', 'Bernie Marcus', 1978, '共同創業者。', '共同創業者', 1997, 1),
  P('blank', 'アーサー・ブランク', 'Arthur Blank', 1978, '共同創業者。のちNFLのアトランタ・ファルコンズのオーナー。', '共同創業者', 2001, 1),
  P('langone', 'ケン・ランゴーン', 'Ken Langone', 1978, '初期の出資者で共同創業者の1人。', '初期の出資者', 2020, 1),
  P('nardelli', 'ボブ・ナルデリ', 'Bob Nardelli', 2000, '2000〜2007年にCEO。', '元CEO', 2007),
  P('blake', 'フランク・ブレイク', 'Frank Blake', 2002, '2007〜2014年にCEO。', '元CEO', 2014),
  P('menear', 'クレイグ・メニア', 'Craig Menear', 1997, '2014〜2022年にCEO。', '元CEO', 2022),
  P('decker', 'テッド・デッカー', 'Ted Decker', 2000, '2022年からCEO(会長も)。', '会長兼CEO'),
  P('mcphail', 'リチャード・マクフェイル', 'Richard McPhail', 2019, 'CFO。', 'CFO'),
  O('hdsupply', 'HD Supply', 2020, '2020年に約87億ドルで買収。', '買収(2020年)'),
  O('srs', 'SRS Distribution', 2024, '2024年に約182億ドルで買収。', '買収(2024年)'),
  O('gms', 'GMS', 2025, '2025年に約55億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.2', M), ('State Street', '4.7', M)]),
 [('marcus', 'blank', 'link', '共同創業'), ('langone', 'marcus', 'link', '出資'), ('nardelli', 'blake', 'link', '後任'), ('blake', 'menear', 'link', '後任'), ('menear', 'decker', 'link', '後任', 2022), ('co', 'hdsupply', 'owns'), ('co', 'srs', 'owns'), ('co', 'gms', 'owns')],
 '1978年に創業した住宅リフォーム小売の会社。2022年からテッド・デッカーがCEOを務めています。')

# ---------------- Philip Morris International ----------------
deep('PM', 'Philip Morris International', 2008, NOTE, [
  P('camilleri', 'ルイ・カミレリ', 'Louis Camilleri', 2008, '2008年の分離から2013年までCEO。', '元CEO', 2013),
  P('calantzopoulos', 'アンドレ・カランゾポロス', 'Andre Calantzopoulos', 2008, '2013〜2020年にCEO。現在は会長。', '会長'),
  P('olczak', 'ヤツェク・オルチャク', 'Jacek Olczak', 2008, '2021年からCEO。', 'CEO'),
  P('babeau', 'エマニュエル・バボー', 'Emmanuel Babeau', 2021, 'CFO。', 'CFO'),
  O('altria', 'Altria', 2008, '2008年に分離した元の親会社。', '親会社(分離元)'),
  O('vectura', 'Vectura', 2021, '2021年に約12億ポンドで買収(吸入薬)。', '買収(2021年)'),
  O('swedish', 'Swedish Match', 2022, '2022年に約160億ドルで買収。', '買収(2022年)'),
 ] + holders([('Capital Group', '8.5', M), ('Vanguard', '6.5', M), ('BlackRock', '5.9', M)]),
 [('altria', 'camilleri', 'link', '分離を率いる'), ('camilleri', 'calantzopoulos', 'link', '後任'), ('calantzopoulos', 'olczak', 'link', '後任', 2021), ('co', 'vectura', 'owns'), ('co', 'swedish', 'owns')],
 '2008年にAltriaから分離したたばこの会社。2021年からヤツェク・オルチャクがCEOを務めています。')

# ---------------- GE Aerospace ----------------
deep('GE', 'GE Aerospace', 1892, NOTE + 'GE Vernovaは2024年に、GE HealthCareは2023年に分離しました。', [
  P('edison', 'トーマス・エジソン', 'Thomas Edison', 1892, 'Edison General Electricの創業者。1892年の合併でGEが誕生。', '源流の創業者', 1892, 1),
  P('coffin', 'チャールズ・コフィン', 'Charles Coffin', 1892, 'GEの初代社長(1892年〜)。', '初代社長', 1913),
  P('welch', 'ジャック・ウェルチ', 'Jack Welch', 1960, '1981〜2001年にCEO。', '元CEO', 2001),
  P('immelt', 'ジェフ・イメルト', 'Jeff Immelt', 1982, '2001〜2017年にCEO。', '元CEO', 2017),
  P('flannery', 'ジョン・フラナリー', 'John Flannery', 1987, '2017〜2018年にCEO。', '元CEO', 2018),
  P('culp', 'ラリー・カルプ', 'Larry Culp', 2018, '2018年からCEO。', '会長兼CEO'),
  P('ghai', 'ラフル・ガイ', 'Rahul Ghai', 2022, 'CFO。', 'CFO'),
  O('tci', 'TCI Fund Management', 2026, '約4.6%を持つ上位株主(MarketScreener、2026年11月)。', '株主(約4.6%)', 'i'),
  O('vernova', 'GE Vernova', 2024, '2024年4月にエネルギー事業を分離。', '分離(2024年)'),
  O('healthcare', 'GE HealthCare', 2023, '2023年1月に医療機器事業を分離。', '分離(2023年)'),
  O('nbc', 'NBCUniversal', 1986, '1986年にRCA(NBC)を買収(のちComcastへ売却)。', '買収(1986年)'),
  O('alstom', 'アルストムの電力事業', 2015, '2015年に約95億ドルで買収。', '買収(2015年)'),
 ] + holders([('BlackRock', '6.6', M), ('Vanguard', '6.6', M), ('Fidelity', '4.7', M)]),
 [('edison', 'coffin', 'link', '合併で誕生'), ('welch', 'immelt', 'link', '後任'), ('immelt', 'flannery', 'link', '後任'), ('flannery', 'culp', 'link', '後任', 2018), ('co', 'vernova', 'owns'), ('co', 'healthcare', 'owns'), ('co', 'nbc', 'owns'), ('co', 'alstom', 'owns')],
 '1892年にエジソン系の会社などが合併して誕生。2024年に分割を終え、現在は航空エンジンのGE Aerospaceとして、ラリー・カルプがCEOを務めています。')

# ---------------- Applied Materials ----------------
deep('AMAT', 'Applied Materials', 1967, NOTE, [
  P('mcneilly', 'マイケル・マクニーリー', 'Michael McNeilly', 1967, '1967年の創業者。', '創業者', 1976, 1),
  P('morgan', 'ジム・モーガン', 'Jim Morgan', 1976, '1976〜2003年にCEO。', '元CEO', 2003),
  P('splinter', 'マイク・スプリンター', 'Mike Splinter', 2003, '2003〜2013年にCEO。', '元CEO', 2013),
  P('dickerson', 'ゲイリー・ディッカーソン', 'Gary Dickerson', 2013, '2013年からCEO。', 'CEO'),
  P('iannotti', 'トーマス・イアノッティ', 'Thomas Iannotti', 2018, '会長。', '会長'),
  P('hill', 'ブライス・ヒル', 'Brice Hill', 2022, 'CFO。', 'CFO'),
  O('semitool', 'Semitool', 2009, '2009年に買収。', '買収(2009年)'),
  O('varian', 'Varian Semiconductor', 2011, '2011年に約49億ドルで買収。', '買収(2011年)'),
  O('tel', '東京エレクトロン', 2013, '2013年に経営統合を発表したが、規制当局の承認が得られず2015年に断念。', '統合断念'),
  O('kokusai', '国際電気', 2021, '2021年に約22億ドルで買収を発表したが、中国当局の承認が得られず断念。', '買収断念(2021年)'),
 ] + holders([('BlackRock', '7.5', M), ('Vanguard', '6.5', M), ('State Street', '4.8', M)]),
 [('mcneilly', 'morgan', 'link', '後任'), ('morgan', 'splinter', 'link', '後任'), ('splinter', 'dickerson', 'link', '後任', 2013), ('co', 'semitool', 'owns'), ('co', 'varian', 'owns'), ('co', 'tel', 'link', '統合を断念'), ('co', 'kokusai', 'link', '買収を断念')],
 '1967年創業の半導体製造装置の会社。2013年からゲイリー・ディッカーソンがCEOを務めています。')

# ---------------- Palo Alto Networks ----------------
deep('PANW', 'Palo Alto Networks', 2005, NOTE, [
  P('zuk', 'ニア・ズク', 'Nir Zuk', 2005, '創業者でCTO。', '創業者', None, 1),
  P('mclaughlin', 'マーク・マクラフリン', 'Mark McLaughlin', 2011, '2011〜2018年にCEO。のち会長。', '元CEO', 2018),
  P('arora', 'ニケシュ・アローラ', 'Nikesh Arora', 2018, '2018年6月からCEO兼会長。グーグルやソフトバンクの元幹部。', '会長兼CEO'),
  O('demisto', 'Demisto', 2019, '2019年に約5.6億ドルで買収。', '買収(2019年)'),
  O('talon', 'Talon Cyber Security', 2023, '2023年に買収。', '買収(2023年)'),
  O('cyberark', 'CyberArk', 2025, '2025年に約250億ドルで買収すると発表(報道)。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.5', M), ('State Street', '4.5', M)]),
 [('zuk', 'mclaughlin', 'link', '経営を託す'), ('mclaughlin', 'arora', 'link', '後任', 2018), ('co', 'demisto', 'owns'), ('co', 'talon', 'owns'), ('co', 'cyberark', 'owns')],
 '2005年にニア・ズクが創業したセキュリティの会社。2018年からニケシュ・アローラがCEOを務めています。')

# ---------------- Lam Research ----------------
deep('LRCX', 'Lam Research', 1980, NOTE, [
  P('dlam', 'デビッド・ラム', 'David Lam', 1980, '1980年の創業者。', '創業者', 1985, 1),
  P('bagley', 'ジェームズ・バグレー', 'James Bagley', 1997, '1997〜2005年にCEO。', '元CEO', 2005),
  P('newberry', 'スティーブ・ニューベリー', 'Steve Newberry', 2005, '2005〜2012年にCEO。', '元CEO', 2012),
  P('anstice', 'マーティン・アンスティス', 'Martin Anstice', 2012, '2012〜2018年にCEO。', '元CEO', 2018),
  P('archer', 'ティム・アーチャー', 'Tim Archer', 2012, '2018年からCEO。', 'CEO'),
  P('talwalkar', 'アビ・タルワルカー', 'Abhi Talwalkar', 2011, '会長。', '会長'),
  O('novellus', 'Novellus Systems', 2012, '2012年に約33億ドルで買収。', '買収(2012年)'),
  O('coventor', 'Coventor', 2017, '2017年に買収。', '買収(2017年)'),
 ] + holders([('BlackRock', '10.6', Y), ('Vanguard', '6.5', Y), ('State Street', '4.9', Y)]),
 [('dlam', 'bagley', 'link', '経営を引き継ぐ'), ('bagley', 'newberry', 'link', '後任'), ('newberry', 'anstice', 'link', '後任'), ('anstice', 'archer', 'link', '後任', 2018), ('co', 'novellus', 'owns'), ('co', 'coventor', 'owns')],
 '1980年にデビッド・ラムが創業した半導体製造装置の会社。2018年からティム・アーチャーがCEOを務めています。')

# ---------------- AstraZeneca ----------------
deep('AZN', 'AstraZeneca', 1999, NOTE, [
  P('barnevik', 'ペール・バーネビック', 'Percy Barnevik', 1999, '1999年の合併時の会長。', '元会長', 2004),
  P('mckillop', 'トム・マッキロップ', 'Tom McKillop', 1999, '1999〜2005年にCEO。', '元CEO', 2005),
  P('brennan', 'デビッド・ブレナン', 'David Brennan', 2006, '2006〜2012年にCEO。', '元CEO', 2012),
  P('soriot', 'パスカル・ソリオ', 'Pascal Soriot', 2012, '2012年からCEO。', 'CEO'),
  P('johansson', 'レイフ・ヨハンソン', 'Leif Johansson', 2012, '2012〜2018年に会長。', '元会長', 2018),
  P('demare', 'ミシェル・デマレ', 'Michel Demare', 2018, '会長。', '会長'),
  P('sarin', 'アラダナ・サリン', 'Aradhana Sarin', 2021, 'CFO。', 'CFO'),
  O('investor', 'Investor AB', 1999, 'ウォレンバーグ家系の投資会社。約3.3%を持つ上位株主(MarketScreener、2026年11月)。', '上位株主(約3.3%)', 'i'),
  O('astra', 'Astra AB', 1999, '1999年に合併(スウェーデン)。', '合併(1999年)'),
  O('zeneca', 'Zeneca Group', 1999, '1999年に合併(英国)。', '合併(1999年)'),
  O('medimmune', 'MedImmune', 2007, '2007年に約152億ドルで買収。', '買収(2007年)'),
  O('pfizer', 'Pfizer', 2014, '2014年にファイザーが約1,060億ドルで買収を提案したが、拒否。', '買収提案(2014年)'),
  O('alexion', 'Alexion', 2021, '2021年に約390億ドルで買収。', '買収(2021年)'),
 ] + holders([('Vanguard', '2.9', M), ('Capital Group', '2.2', M), ('Norges Bank', '2.2', M)]),
 [('barnevik', 'mckillop', 'link', '会長とCEO'), ('mckillop', 'brennan', 'link', '後任'), ('brennan', 'soriot', 'link', '後任', 2012), ('johansson', 'demare', 'link', '後任', 2018), ('co', 'astra', 'owns'), ('co', 'zeneca', 'owns'), ('co', 'medimmune', 'owns'), ('co', 'alexion', 'owns'), ('soriot', 'pfizer', 'conflict', '買収提案を拒否', 2014)],
 '1999年にスウェーデンのAstraと英国のZenecaが合併して誕生した製薬会社。2012年からパスカル・ソリオがCEOを務めています。')
