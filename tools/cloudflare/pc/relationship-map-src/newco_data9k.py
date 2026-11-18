from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Vertex ----------------
deep('VRTX', 'Vertex Pharmaceuticals', 1989, NOTE, [
  P('boger', 'ジョシュア・ボーガー', 'Joshua Boger', 1989, '創業者。1992〜2009年にCEO。', '創業者 / 元CEO', 2009, 1),
  P('emmens', 'マシュー・エメンス', 'Matthew Emmens', 2003, '2009〜2012年にCEO。', '元CEO', 2012),
  P('leiden', 'ジェフリー・ライデン', 'Jeffrey Leiden', 2012, '2012〜2020年にCEO。現在は会長。', '会長'),
  P('kewalramani', 'レシュマ・ケワルラマニ', 'Reshma Kewalramani', 2018, '2020年4月からCEO。大手バイオ医薬の初の女性CEOの1人。', 'CEO'),
  P('altshuler', 'デビッド・アルトシュラー', 'David Altshuler', 2015, '最高科学責任者(CSO)。', 'CSO'),
  P('wagner', 'チャールズ・ワグナー', 'Charles Wagner', 2016, 'CFO。', 'CFO'),
  O('semma', 'Semma Therapeutics', 2019, '2019年に約9.5億ドルで買収(糖尿病の細胞治療)。', '買収(2019年)'),
  O('viacyte', 'ViaCyte', 2022, '2022年に約3.2億ドルで買収。', '買収(2022年)'),
  O('alpine', 'Alpine Immune Sciences', 2024, '2024年に約49億ドルで買収。', '買収(2024年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.3', M), ('Capital Group', '5.4', M)]),
 [('boger', 'emmens', 'link', '後任'), ('emmens', 'leiden', 'link', '後任'), ('leiden', 'kewalramani', 'link', '後任', 2020), ('co', 'semma', 'owns'), ('co', 'viacyte', 'owns'), ('co', 'alpine', 'owns')],
 '1989年にジョシュア・ボーガーが創業した、のう胞性線維症の薬で知られる製薬会社。2020年からレシュマ・ケワルラマニがCEOを務めています。')

# ---------------- Chubb ----------------
deep('CB', 'Chubb', 1882, NOTE, [
  P('tchubb', 'トーマス・チャブ', 'Thomas Chubb', 1882, 'Chubb(1882年)の創業者。', '源流の創業者', 1900, 1),
  P('egreenberg', 'エバン・グリーンバーグ', 'Evan Greenberg', 2002, '2004年からACEのCEO。2016年のChubb買収後はChubbの会長兼CEO。', '会長兼CEO'),
  P('hgreenberg', 'ハンク・グリーンバーグ', 'Hank Greenberg', 1967, 'AIGの元CEO。エバンの父。', '関係者', 2005),
  O('acelimited', 'ACE Limited', 1985, '1985年に設立。2016年にChubb Corp.を買収し、社名をChubbに。', '前身'),
  O('chubbcorp', 'Chubb Corporation', 2016, '2016年に約283億ドルで買収。', '買収(2016年)'),
  O('cigna', 'Cignaのアジア事業', 2019, '2019年に買収。', '買収(2019年)'),
  O('huatai', 'Huatai Insurance', 2023, '2023年に過半を取得(中国)。', '買収(2023年)'),
  O('berkshire', 'Berkshire Hathaway', 2023, '約8.9%を持つ上位株主(MarketScreener、2026年11月)。', '株主(約8.9%)', 'i'),
 ] + holders([('Vanguard', '6.0', M), ('BlackRock', '5.7', M), ('State Street', '4.3', M)]),
 [('tchubb', 'egreenberg', 'link', '源流を継ぐ'), ('hgreenberg', 'egreenberg', 'link', '親子'), ('acelimited', 'egreenberg', 'link', 'CEO(2004年〜)'), ('co', 'chubbcorp', 'owns'), ('co', 'cigna', 'owns'), ('co', 'huatai', 'owns')],
 '1882年創業のChubbを、2016年にACEが買収して誕生した保険の会社。エバン・グリーンバーグが会長兼CEOを務め、バークシャーが約8.9%を持っています。')

# ---------------- Western Digital ----------------
deep('WDC', 'Western Digital', 1970, NOTE, [
  P('phillips', 'アルビン・フィリップス', 'Alvin Phillips', 1970, '創業者(General Digital)。', '創業者', 1976, 1),
  P('massengill', 'マット・マッセンギル', 'Matt Massengill', 2000, '2000〜2005年にCEO。', '元CEO', 2005),
  P('coyne', 'ジョン・コイン', 'John Coyne', 2005, '2005〜2013年にCEO。', '元CEO', 2013),
  P('milligan', 'スティーブ・ミリガン', 'Steve Milligan', 2013, '2013〜2020年にCEO。', '元CEO', 2020),
  P('goeckeler', 'デビッド・ゲッケラー', 'David Goeckeler', 2020, '2020〜2025年にCEO。のちSandiskのCEO。', '元CEO', 2025),
  P('tan', 'アービング・タン', 'Irving Tan', 2025, 'CEO(英語版Wikipedia)。', 'CEO'),
  O('hgst', 'HGST', 2012, '2012年に約43億ドルで買収。', '買収(2012年)'),
  O('fusion', 'Fusion-io', 2014, '2014年に買収。', '買収(2014年)'),
  O('sandisk', 'SanDisk', 2016, '2016年に約190億ドルで買収。2025年2月にフラッシュ事業を分離。', '買収(2016年)'),
 ] + holders([('Fidelity', '7.2', M), ('BlackRock', '6.7', M), ('Vanguard', '6.2', M)]),
 [('massengill', 'coyne', 'link', '後任'), ('coyne', 'milligan', 'link', '後任'), ('milligan', 'goeckeler', 'link', '後任', 2020), ('goeckeler', 'tan', 'link', '後任', 2025), ('co', 'hgst', 'owns'), ('co', 'fusion', 'owns'), ('co', 'sandisk', 'owns')],
 '1970年創業のストレージの会社。2025年にフラッシュ事業をSandiskとして分離し、アービング・タンがCEOを務めています。')

# ---------------- Boeing ----------------
deep('BA', 'Boeing', 1916, NOTE, [
  P('wboeing', 'ウィリアム・ボーイング', 'William Boeing', 1916, '1916年に創業。', '創業者', 1934, 1),
  P('condit', 'フィル・コンディット', 'Phil Condit', 1996, '1996〜2003年にCEO。マクドネル・ダグラスとの合併(1997年)を主導。', '元CEO', 2003),
  P('mcnerney', 'ジム・マクナーニー', 'Jim McNerney', 2005, '2005〜2015年にCEO。', '元CEO', 2015),
  P('muilenburg', 'デニス・ミューレンバーグ', 'Dennis Muilenburg', 1985, '2015〜2019年にCEO。737MAXの墜落事故(2018年、2019年)を受け退任。', '元CEO', 2019),
  P('calhoun', 'デビッド・カルホーン', 'David Calhoun', 2009, '2020〜2024年にCEO。', '元CEO', 2024),
  P('ortberg', 'ケリー・オートバーグ', 'Kelly Ortberg', 2024, '2024年8月からCEO。ロックウェル・コリンズの元CEO。', 'CEO'),
  P('mollenkopf', 'スティーブ・モレンコフ', 'Steve Mollenkopf', 2020, '会長(英語版Wikipedia)。クアルコムの元CEO。', '会長'),
  P('west', 'ブライアン・ウェスト', 'Brian West', 2021, 'CFO。', 'CFO'),
  O('mcdonnell', 'McDonnell Douglas', 1997, '1997年に約130億ドルで合併。', '合併(1997年)'),
  O('hughes', 'Hughesの宇宙事業', 2000, '2000年に買収。', '買収(2000年)'),
  O('jeppesen', 'Jeppesen', 2000, '2000年に買収。', '買収(2000年)'),
  O('aurora', 'Aurora Flight Sciences', 2017, '2017年に買収。', '買収(2017年)'),
  O('spirit', 'Spirit AeroSystems', 2025, '2024年に約47億ドルでの買収を発表(2025年に完了と報じられています)。', '買収(2025年・報道)'),
 ] + holders([('Fidelity', '8.4', M), ('BlackRock', '7.4', M), ('Vanguard', '6.5', M)]),
 [('wboeing', 'condit', 'link', '源流'), ('condit', 'mcnerney', 'link', '後任'), ('mcnerney', 'muilenburg', 'link', '後任'), ('muilenburg', 'calhoun', 'link', '後任'), ('calhoun', 'ortberg', 'link', '後任', 2024), ('co', 'mcdonnell', 'owns'), ('co', 'hughes', 'owns'), ('co', 'jeppesen', 'owns'), ('co', 'aurora', 'owns'), ('co', 'spirit', 'owns')],
 '1916年にウィリアム・ボーイングが創業した航空宇宙の会社。2024年8月からケリー・オートバーグがCEOを務めています。')

# ---------------- S&P Global ----------------
deep('SPGI', 'S&P Global', 1860, NOTE, [
  P('poor', 'ヘンリー・バーナム・プア', 'Henry Varnum Poor', 1860, '1860年にプア社を創業(鉄道の財務情報)。', '源流の創業者', 1905, 1),
  P('mcgrawiii', 'ハロルド・マグロウ3世', 'Harold McGraw III', 1980, '2000〜2013年にCEO。', '元CEO', 2013),
  P('peterson', 'ダグ・ピーターソン', 'Doug Peterson', 2011, '2013〜2024年にCEO。', '元CEO', 2024),
  P('cheung', 'マルティナ・チャン', 'Martina Cheung', 2010, '2024年11月からCEO。', 'CEO'),
  P('steenbergen', 'エワウト・ステーンベルヘン', 'Ewout Steenbergen', 2019, 'CFO。', 'CFO'),
  O('standard', 'Standard Statistics', 1906, '1906年設立。1941年にプア社と合併してS&Pに。', '源流(1906年)'),
  O('mcgrawhill', 'McGraw-Hill', 2016, '2016年にS&P Globalへ社名変更(教育事業は売却)。', '前身'),
  O('snl', 'SNL Financial', 2015, '2015年に約22億ドルで買収。', '買収(2015年)'),
  O('kensho', 'Kensho', 2018, '2018年に約5.5億ドルで買収(AI)。', '買収(2018年)'),
  O('ihs', 'IHS Markit', 2022, '2022年に約440億ドルで買収。', '買収(2022年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.9', M), ('State Street', '4.9', M), ('TCI Fund Management', '4.8', M)]),
 [('poor', 'mcgrawiii', 'link', '源流を継ぐ'), ('mcgrawiii', 'peterson', 'link', '後任'), ('peterson', 'cheung', 'link', '後任', 2024), ('standard', 'poor', 'link', '1941年に合併'), ('co', 'snl', 'owns'), ('co', 'kensho', 'owns'), ('co', 'ihs', 'owns'), ('co', 'mcgrawhill', 'owns')],
 '1860年のプア社などを源流とする信用格付け・市場データの会社。2024年11月からマルティナ・チャンがCEOを務めています。')

# ---------------- Progressive ----------------
deep('PGR', 'Progressive', 1937, NOTE, [
  P('jlewis', 'ジョセフ・ルイス', 'Joseph Lewis', 1937, '創業者の1人(クリーブランド)。', '創業者', 1965, 1),
  P('green', 'ジャック・グリーン', 'Jack Green', 1937, '創業者の1人。', '創業者', 1950, 1),
  P('plewis', 'ピーター・ルイス', 'Peter Lewis', 1965, '1965〜2000年にCEO。ジョセフ・ルイスの息子。', '元CEO', 2000),
  P('renwick', 'グレン・レンウィック', 'Glenn Renwick', 1986, '2001〜2016年にCEO。', '元CEO', 2016),
  P('griffith', 'トリシア・グリフィス', 'Tricia Griffith', 1998, '2016年からCEO。', 'CEO'),
  P('fitt', 'ローントン・フィット', 'Lawton Fitt', 2006, '会長。', '会長'),
  P('sauerland', 'ジョン・ソーランド', 'John Sauerland', 2017, 'CFO。', 'CFO'),
  O('asi', 'American Strategic Insurance', 2015, '2015年に約8.75億ドルで買収(住宅保険)。', '買収(2015年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.0', M), ('Capital Group', '4.6', M)]),
 [('jlewis', 'green', 'link', '共同創業'), ('jlewis', 'plewis', 'link', '親子'), ('plewis', 'renwick', 'link', '後任'), ('renwick', 'griffith', 'link', '後任', 2016), ('co', 'asi', 'owns')],
 '1937年にクリーブランドで創業した自動車保険の会社。2016年からトリシア・グリフィスがCEOを務めています。')

# ---------------- Dell ----------------
deep('DELL', 'Dell Technologies', 1984, NOTE, [
  P('mdell', 'マイケル・デル', 'Michael Dell', 1984, '創業者。会長兼CEO。約5.8%を保有(MarketScreener)。', '創業者 / 会長兼CEO', None, 1),
  P('rollins', 'ケビン・ロリンズ', 'Kevin Rollins', 1996, '2004〜2007年にCEO。', '元CEO', 2007),
  P('clarke', 'ジェフ・クラーク', 'Jeff Clarke', 2000, '副会長兼COO。', '副会長兼COO'),
  P('johnson', 'タイラー・ジョンソン', 'Tyler Johnson', 2024, 'CFO。', 'CFO'),
  P('durban', 'エゴン・ダーバン', 'Egon Durban', 2013, 'Silver Lakeの共同CEO。2013年の非公開化を主導し、取締役。', '取締役'),
  O('silverlake', 'Silver Lake', 2013, '2013年の約249億ドルの非公開化(LBO)でデル氏と組んだ投資会社。', '出資者(2013年)', 'i'),
  O('emc', 'EMC', 2016, '2016年に約670億ドルで買収。Dell Technologiesが誕生。', '買収(2016年)'),
  O('vmware', 'VMware', 2021, '2021年に分離(のちBroadcomが買収)。', '分離(2021年)'),
 ] + holders([('Vanguard', '5.8', M), ('BlackRock', '5.5', M), ('State Street', '4.2', M)]),
 [('mdell', 'rollins', 'link', 'CEOを任せる', 2004), ('rollins', 'mdell', 'link', 'CEOに復帰', 2007), ('silverlake', 'mdell', 'link', '共同で非公開化'), ('durban', 'silverlake', 'link', '共同CEO'), ('co', 'emc', 'owns'), ('co', 'vmware', 'owns', '分離')],
 '1984年にマイケル・デルが大学の寮で始めたPCの会社。2013年に非公開化し、2018年に再上場。マイケル・デルが会長兼CEOを務めています。')

# ---------------- Altria ----------------
deep('MO', 'Altria', 1985, NOTE, [
  P('camilleri', 'ルイ・カミレリ', 'Louis Camilleri', 1996, '2002〜2008年にCEO。', '元CEO', 2008),
  P('szymanczyk', 'マイケル・シマンジク', 'Michael Szymanczyk', 2008, '2008〜2012年にCEO。', '元CEO', 2012),
  P('barrington', 'マーティ・バリントン', 'Marty Barrington', 2013, '2013〜2019年にCEO。', '元CEO', 2019),
  P('willard', 'ハワード・ウィラード', 'Howard Willard', 2019, '2019〜2020年にCEO。JUUL投資の責任を問われ退任。', '元CEO', 2020),
  P('gifford', 'ビリー・ギフォード', 'Billy Gifford', 2020, '2020年からCEO(会長も)。', '会長兼CEO'),
  O('kraft', 'Kraft Foods', 2007, '2007年に分離。', '分離(2007年)'),
  O('pmi', 'Philip Morris International', 2008, '2008年に分離。', '分離(2008年)'),
  O('juul', 'JUUL', 2018, '2018年に約128億ドルで35%を取得。のち大幅に評価減。', '出資(2018年)'),
  O('njoy', 'NJOY', 2023, '2023年に約27.5億ドルで買収。', '買収(2023年)'),
  O('abi', 'Anheuser-Busch InBev', 2016, 'ABIの株式(約10%)を保有。', '出資先'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.3', M), ('State Street', '4.2', M)]),
 [('camilleri', 'szymanczyk', 'link', '後任'), ('szymanczyk', 'barrington', 'link', '後任'), ('barrington', 'willard', 'link', '後任'), ('willard', 'gifford', 'link', '後任', 2020), ('co', 'kraft', 'owns', '分離'), ('co', 'pmi', 'owns', '分離'), ('co', 'juul', 'invest2', '出資'), ('co', 'njoy', 'owns'), ('co', 'abi', 'invest2', '出資')],
 'フィリップ・モリスを源流とする米国のたばこの会社。2020年からビリー・ギフォードがCEOを務めています。')

# ---------------- Bristol Myers Squibb ----------------
deep('BMY', 'Bristol Myers Squibb', 1858, NOTE + '買収は英語版Wikipediaの記載に基づきます。', [
  P('squibb', 'エドワード・スクイブ', 'Edward Squibb', 1858, '1858年にSquibbを創業した医師。', '源流の創業者', 1900, 1),
  P('bristol', 'ウィリアム・ブリストル', 'William Bristol', 1887, '1887年にBristol-Myersを共同創業。', '源流の共同創業者', 1900, 1),
  P('myers', 'ジョン・マイヤーズ', 'John Myers', 1887, 'Bristol-Myersの共同創業者。', '源流の共同創業者', 1900, 1),
  P('dolan', 'ピーター・ドラン', 'Peter Dolan', 2001, '2001〜2006年にCEO。', '元CEO', 2006),
  P('cornelius', 'ジェームズ・コーネリアス', 'James Cornelius', 2006, '2006〜2010年にCEO。', '元CEO', 2010),
  P('andreotti', 'ランベルト・アンドレオッティ', 'Lamberto Andreotti', 2010, '2010〜2015年にCEO。', '元CEO', 2015),
  P('caforio', 'ジョバンニ・カフォリオ', 'Giovanni Caforio', 2015, '2015〜2023年にCEO。のち会長。', '元CEO', 2024),
  P('boerner', 'クリス・ボーナー', 'Chris Boerner', 2014, '2023年11月からCEO(のち会長も)。', '会長兼CEO'),
  P('elkins', 'デビッド・エルキンス', 'David Elkins', 2023, 'CFO。', 'CFO'),
  O('medarex', 'Medarex', 2009, '2009年に約24億ドルで買収。', '買収(2009年)'),
  O('celgene', 'Celgene', 2019, '2019年に約740億ドルで買収。', '買収(2019年)'),
  O('myokardia', 'MyoKardia', 2020, '2020年に約131億ドルで買収。', '買収(2020年)'),
  O('turning', 'Turning Point Therapeutics', 2022, '2022年に約41億ドルで買収。', '買収(2022年)'),
  O('mirati', 'Mirati Therapeutics', 2024, '2024年に約48億ドルで買収。', '買収(2024年)'),
  O('karuna', 'Karuna Therapeutics', 2024, '2024年に約140億ドルで買収。', '買収(2024年)'),
  O('rayze', 'RayzeBio', 2024, '2024年に約41億ドルで買収。', '買収(2024年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.3', M), ('State Street', '5.0', M)]),
 [('squibb', 'bristol', 'link', '1989年に合併'), ('bristol', 'myers', 'link', '共同創業'), ('dolan', 'cornelius', 'link', '後任'), ('cornelius', 'andreotti', 'link', '後任'), ('andreotti', 'caforio', 'link', '後任'), ('caforio', 'boerner', 'link', '後任', 2023), ('co', 'medarex', 'owns'), ('co', 'celgene', 'owns'), ('co', 'myokardia', 'owns'), ('co', 'turning', 'owns'), ('co', 'mirati', 'owns'), ('co', 'karuna', 'owns'), ('co', 'rayze', 'owns')],
 '1989年にBristol-MyersとSquibbが合併して誕生した製薬会社。2023年11月からクリス・ボーナーがCEOを務めています。')

# ---------------- Marathon Petroleum ----------------
deep('MPC', 'Marathon Petroleum', 2011, NOTE, [
  P('heminger', 'ゲイリー・ヘミンガー', 'Gary Heminger', 2011, '2011〜2020年にCEO。', '元CEO', 2020),
  P('hennigan', 'マイケル・ヘニガン', 'Michael Hennigan', 2020, '2020〜2024年にCEO。現在は会長。', '会長'),
  P('mannen', 'メアリーアン・マネン', 'Maryann Mannen', 2020, '2024年からCEO。', 'CEO'),
  P('quaid', 'ジョン・クエイド', 'John Quaid', 2016, 'CFO。', 'CFO'),
  O('marathonoil', 'Marathon Oil', 2011, '2011年に精製・販売部門を分離して発足。', '分離元(2011年)'),
  O('andeavor', 'Andeavor', 2018, '2018年に約230億ドルで買収。', '買収(2018年)'),
  O('speedway', 'Speedway', 2021, '2021年にセブン-イレブンに約210億ドルで売却。', '売却(2021年)'),
  O('mplx', 'MPLX', 2012, 'パイプライン事業の上場子会社。', '子会社'),
 ] + holders([('BlackRock', '7.3', M), ('Vanguard', '6.8', M), ('State Street', '6.6', M)]),
 [('heminger', 'hennigan', 'link', '後任'), ('hennigan', 'mannen', 'link', '後任'), ('marathonoil', 'heminger', 'link', '分離を主導'), ('co', 'andeavor', 'owns'), ('co', 'speedway', 'owns'), ('co', 'mplx', 'owns')],
 '2011年にマラソン・オイルから精製・販売部門を分離して誕生した石油精製の会社。メアリーアン・マネンがCEOを務めています。')
