from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Citigroup ----------------
deep('C', 'Citigroup', 1998, NOTE + '2008〜2010年の米国政府の出資は、広く知られた範囲で書いています。', [
  P('weill', 'サンディ・ワイル', 'Sandy Weill', 1986, 'トラベラーズ・グループを率い、1998年のシティコープとの合併を主導。', '元会長', 2006),
  P('reed', 'ジョン・リード', 'John Reed', 1984, 'シティコープのCEO。合併後は共同CEO。', '元共同CEO', 2000),
  P('prince', 'チャック・プリンス', 'Chuck Prince', 2003, '2003〜2007年にCEO。', '元CEO', 2007),
  P('pandit', 'ビクラム・パンディット', 'Vikram Pandit', 2007, '2007〜2012年にCEO。金融危機時の経営者。', '元CEO', 2012),
  P('corbat', 'マイケル・コーバット', 'Michael Corbat', 1983, '2012〜2021年にCEO。', '元CEO', 2021),
  P('fraser', 'ジェーン・フレーザー', 'Jane Fraser', 2004, '2021年からCEO、2022年から会長。大手米銀で初の女性CEO。', '会長兼CEO'),
  P('raghavan', 'ビスワス・ラガヴァン', 'Viswas Raghavan', 2021, '執行副会長。', '執行副会長'),
  P('mason', 'マーク・メイソン', 'Mark Mason', 2021, 'CFO。', 'CFO'),
  O('usgov', '米国政府', 2008, '2008年の金融危機で優先株などを引き受け、約2割の株主に(2010年に売却開始)。', '株主(2008〜2010年)', 'i'),
  O('alwaleed', 'アルワリード・ビン・タラール', 1991, 'サウジの王子。長く大口の個人株主として知られました。', '大口株主(1991年〜)', 'i'),
  O('travelers', 'Travelers Group', 1998, '1998年にシティコープと合併。', '合併(1998年)'),
  O('salomon', 'Salomon Smith Barney', 1997, '1997年にトラベラーズが統合。', '統合(1997年)'),
  O('banamex', 'Banamex', 2001, '2001年に買収(メキシコ)。2025年に一部を売却すると発表。', '買収(2001年)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.4', M), ('State Street', '4.6', M)]),
 [('weill', 'reed', 'link', '共同CEO', 1998), ('weill', 'prince', 'link', '後任'), ('prince', 'pandit', 'link', '後任', 2007), ('pandit', 'corbat', 'link', '後任'), ('corbat', 'fraser', 'link', '後任', 2021), ('co', 'travelers', 'owns'), ('co', 'salomon', 'owns'), ('co', 'banamex', 'owns')],
 '1998年にシティコープとトラベラーズが合併して誕生した銀行。2021年からジェーン・フレーザーがCEOを務めています。')

# ---------------- Analog Devices ----------------
deep('ADI', 'Analog Devices', 1965, NOTE, [
  P('stata', 'レイ・スタータ', 'Ray Stata', 1965, '共同創業者で、長く会長。', '共同創業者', 2012, 1),
  P('lorber', 'マシュー・ローバー', 'Matthew Lorber', 1965, '共同創業者。', '共同創業者', 1970, 1),
  P('fishman', 'ジェリー・フィッシュマン', 'Jerald Fishman', 1971, '1996〜2013年にCEO。2013年に亡くなりました。', '元CEO', 2013),
  P('roche', 'ビンセント・ロッシュ', 'Vincent Roche', 1988, '2013年からCEO(2022年から会長も)。', '会長兼CEO'),
  P('puccio', 'リチャード・プッチオ', 'Richard Puccio', 2019, 'CFO。', 'CFO'),
  O('hittite', 'Hittite Microwave', 2014, '2014年に約25億ドルで買収。', '買収(2014年)'),
  O('linear', 'Linear Technology', 2017, '2017年に約148億ドルで買収。', '買収(2017年)'),
  O('maxim', 'Maxim Integrated', 2021, '2021年に約210億ドルで買収。', '買収(2021年)'),
 ] + holders([('BlackRock', '7.0', M), ('Vanguard', '6.6', M), ('State Street', '4.9', M)]),
 [('stata', 'lorber', 'link', '共同創業'), ('stata', 'fishman', 'link', '経営を託す'), ('fishman', 'roche', 'link', '後任', 2013), ('co', 'hittite', 'owns'), ('co', 'linear', 'owns'), ('co', 'maxim', 'owns')],
 '1965年に創業したアナログ半導体の会社。2013年からビンセント・ロッシュがCEOを務めています。')

# ---------------- Amphenol ----------------
deep('APH', 'Amphenol', 1932, NOTE + 'CommScopeの事業とTrexonの買収(2025年)は、報道に基づきます。', [
  P('schmitt', 'アーサー・シュミット', 'Arthur Schmitt', 1932, 'American Phenolic(Amphenolの前身)の創業者。', '源流の創業者', 1950, 1),
  P('norwitt', 'アダム・ノーウィット', 'Adam Norwitt', 2005, '2009年からCEO(2016年から社長兼CEO)。', 'CEO兼社長'),
  P('lampo', 'クレイグ・ランポ', 'Craig Lampo', 2007, 'CFO。', 'CFO'),
  O('kkr', 'KKR', 1997, '1997年にAmphenolを買収して非公開化し、のち再上場。', '元の買い手(1997年)', 'i'),
  O('carlisle', 'Carlisle Interconnect Technologies', 2024, '2024年に約20億ドルで買収。', '買収(2024年)'),
  O('commscope', 'CommScopeの無線・DAS事業', 2025, '2025年に約105億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('trexon', 'Trexon', 2025, '2025年に約10億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '7.6', M), ('Vanguard', '6.5', M), ('Vanguard Portfolio Mgmt', '6.0', M)]),
 [('schmitt', 'norwitt', 'link', '源流を継ぐ'), ('co', 'carlisle', 'owns'), ('co', 'commscope', 'owns'), ('co', 'trexon', 'owns')],
 '1932年のAmerican Phenolicを源流とするコネクターの会社。2009年からアダム・ノーウィットがCEOを務めています。')

# ---------------- Disney ----------------
deep('DIS', 'Walt Disney', 1923, NOTE, [
  P('waltdisney', 'ウォルト・ディズニー', 'Walt Disney', 1923, '1923年に兄ロイと創業。1966年に亡くなりました。', '共同創業者', 1966, 1),
  P('roydisney', 'ロイ・O・ディズニー', 'Roy O. Disney', 1923, '共同創業者。ウォルトの兄。', '共同創業者', 1971, 1),
  P('eisner', 'マイケル・アイズナー', 'Michael Eisner', 1984, '1984〜2005年にCEO。', '元CEO', 2005),
  P('iger', 'ボブ・アイガー', 'Bob Iger', 1996, '2005〜2020年と2022〜2026年にCEO。', '元CEO', 2026),
  P('chapek', 'ボブ・チャペック', 'Bob Chapek', 1993, '2020〜2022年にCEO。', '元CEO', 2022),
  P('damaro', 'ジョシュ・ダマロ', "Josh D'Amaro", 1998, '2026年3月18日からCEO。テーマパーク部門を率いました。', 'CEO'),
  P('gorman', 'ジェームズ・ゴーマン', 'James Gorman', 2024, '会長(2025年から)。モルガン・スタンレーの元CEO。', '会長'),
  P('walden', 'ダナ・ウォルデン', 'Dana Walden', 2019, '最高クリエイティブ責任者(CCO)。', 'CCO'),
  P('johnston', 'ヒュー・ジョンストン', 'Hugh Johnston', 2023, 'CFO。', 'CFO'),
  O('abc', 'Capital Cities/ABC', 1995, '1995年に約190億ドルで買収。', '買収(1995年)'),
  O('pixar', 'Pixar', 2006, '2006年に約74億ドルで買収。', '買収(2006年)'),
  O('marvel', 'Marvel', 2009, '2009年に約40億ドルで買収。', '買収(2009年)'),
  O('lucasfilm', 'Lucasfilm', 2012, '2012年に約40.5億ドルで買収。', '買収(2012年)'),
  O('fox', '21st Century Fox', 2019, '2019年に約710億ドルで買収(一部)。', '買収(2019年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '5.7', M), ('State Street', '4.8', M)]),
 [('waltdisney', 'roydisney', 'link', '兄弟で創業'), ('eisner', 'iger', 'link', '後任', 2005), ('iger', 'chapek', 'link', '後任', 2020), ('chapek', 'iger', 'link', '復帰', 2022), ('iger', 'damaro', 'link', '後任', 2026), ('co', 'abc', 'owns'), ('co', 'pixar', 'owns'), ('co', 'marvel', 'owns'), ('co', 'lucasfilm', 'owns'), ('co', 'fox', 'owns')],
 '1923年にウォルトとロイのディズニー兄弟が創業した娯楽の会社。2026年3月からジョシュ・ダマロがCEOを務めています。')

# ---------------- Shopify ----------------
deep('SHOP', 'Shopify', 2006, NOTE, [
  P('lutke', 'トビアス・リュトケ', 'Tobias Lutke', 2006, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('weinand', 'ダニエル・ヴァイナンド', 'Daniel Weinand', 2006, '共同創業者。', '共同創業者', 2008, 1),
  P('lake', 'スコット・レイク', 'Scott Lake', 2006, '共同創業者。', '共同創業者', 2008, 1),
  P('finkelstein', 'ハーレー・フィンケルスタイン', 'Harley Finkelstein', 2010, '社長。', '社長'),
  P('hoffmeister', 'ジェフ・ホフマイスター', 'Jeff Hoffmeister', 2019, 'CFO。', 'CFO'),
  O('bessemer', 'Bessemer Venture Partners', 2010, '初期の出資者。', '初期の出資者', 'i'),
  O('firstmark', 'FirstMark Capital', 2010, '初期の出資者。', '初期の出資者', 'i'),
  O('oberlo', 'Oberlo', 2017, '2017年に買収。', '買収(2017年)'),
  O('sixriver', '6 River Systems', 2019, '2019年に約4.5億ドルで買収(2023年に売却)。', '買収(2019年)'),
  O('deliverr', 'Deliverr', 2022, '2022年に約21億ドルで買収(2023年にFlexportへ売却)。', '買収(2022年)'),
 ] + holders([('Capital Group', '4.5', M), ('Fidelity', '3.9', M), ('Invesco', '3.0', M)]),
 [('lutke', 'weinand', 'link', '共同創業'), ('lutke', 'lake', 'link', '共同創業'), ('lutke', 'finkelstein', 'link', '社長'), ('co', 'oberlo', 'owns'), ('co', 'sixriver', 'owns'), ('co', 'deliverr', 'owns')],
 '2006年にカナダ・オタワで創業したEC基盤の会社。トビアス・リュトケがCEOを務めています。')

# ---------------- Salesforce ----------------
deep('CRM', 'Salesforce', 1999, NOTE + '2025年の買収(Informatica)は報道ベースです。', [
  P('benioff', 'マーク・ベニオフ', 'Marc Benioff', 1999, '創業者。会長兼CEO。約2.7%を保有(MarketScreener)。', '創業者 / 会長兼CEO', None, 1),
  P('harris', 'パーカー・ハリス', 'Parker Harris', 1999, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('moellenhoff', 'デイブ・メレンホフ', 'Dave Moellenhoff', 1999, '共同創業者。', '共同創業者', 2005, 1),
  P('dominguez', 'フランク・ドミンゲス', 'Frank Dominguez', 1999, '共同創業者。', '共同創業者', 2005, 1),
  P('block', 'キース・ブロック', 'Keith Block', 2000, '2018〜2020年に共同CEO。', '元共同CEO', 2020),
  P('weaver', 'エイミー・ウィーバー', 'Amy Weaver', 2017, 'CFO(2017〜2025年)。', '元CFO', 2025),
  P('washington', 'ロビン・ワシントン', 'Robin Washington', 2025, '社長兼最高執行・財務責任者。Alphabetの取締役でもあります。', '社長兼COO・CFO'),
  O('ellison', 'ラリー・エリソン', 1999, '創業期に約200万ドルを出資したと知られます。', '初期の出資者', 'i'),
  O('mulesoft', 'MuleSoft', 2018, '2018年に約65億ドルで買収。', '買収(2018年)'),
  O('tableau', 'Tableau', 2019, '2019年に約157億ドルで買収。', '買収(2019年)'),
  O('slack', 'Slack', 2021, '2021年に約277億ドルで買収。', '買収(2021年)'),
  O('informatica', 'Informatica', 2025, '2025年に約80億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '6.5', M), ('Vanguard', '6.3', M), ('State Street', '5.5', M)]),
 [('benioff', 'harris', 'link', '共同創業'), ('benioff', 'moellenhoff', 'link', '共同創業'), ('benioff', 'dominguez', 'link', '共同創業'), ('ellison', 'benioff', 'link', '出資'), ('weaver', 'washington', 'link', 'CFO職を引き継ぐ', 2025), ('co', 'mulesoft', 'owns'), ('co', 'tableau', 'owns'), ('co', 'slack', 'owns'), ('co', 'informatica', 'owns')],
 '1999年にマーク・ベニオフらが創業したクラウドの会社。ベニオフ氏が会長兼CEOを務めています。')

# ---------------- PepsiCo ----------------
deep('PEP', 'PepsiCo', 1965, NOTE + 'エリオット(アクティビスト)の出資(2025年)は報道に基づきます。', [
  P('bradham', 'ケイレブ・ブラッドハム', 'Caleb Bradham', 1893, '1893年にペプシ(のちのペプシ・コーラ)を考案した薬剤師。', '源流の考案者', 1923, 1),
  P('kendall', 'ドナルド・ケンドール', 'Donald Kendall', 1963, 'ペプシコーラのCEO。1965年のフリトレーとの合併を主導。', '元CEO', 1986),
  P('lay', 'ハーマン・レイ', 'Herman Lay', 1932, 'フリトレーの経営者。', '元経営者', 1971),
  P('reinemund', 'スティーブ・ライネムンド', 'Steve Reinemund', 1984, '2001〜2006年にCEO。', '元CEO', 2006),
  P('nooyi', 'インドラ・ヌーイ', 'Indra Nooyi', 1994, '2006〜2018年にCEO。', '元CEO', 2019),
  P('laguarta', 'ラモン・ラガルタ', 'Ramon Laguarta', 1996, '2018年からCEO兼会長。', '会長兼CEO'),
  P('caulfield', 'ジェイミー・コールフィールド', 'Jamie Caulfield', 2008, 'CFO。', 'CFO'),
  O('elliott', 'Elliott Management', 2025, '2025年に約40億ドルの株式を取得したと報じられています。', '株主(2025年・報道)', 'i'),
  O('tropicana', 'Tropicana', 1998, '1998年に約33億ドルで買収(のち売却)。', '買収(1998年)'),
  O('quaker', 'Quaker Oats', 2001, '2001年に約134億ドルで買収。', '買収(2001年)'),
  O('sodastream', 'SodaStream', 2018, '2018年に約32億ドルで買収。', '買収(2018年)'),
  O('rockstar', 'Rockstar Energy', 2020, '2020年に約38.5億ドルで買収。', '買収(2020年)'),
  O('poppi', 'poppi', 2025, '2025年に約19.5億ドルで買収(報道)。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.5', M), ('State Street', '4.4', M)]),
 [('bradham', 'kendall', 'link', '源流'), ('kendall', 'lay', 'link', '1965年に合併'), ('reinemund', 'nooyi', 'link', '後任'), ('nooyi', 'laguarta', 'link', '後任', 2018), ('co', 'tropicana', 'owns'), ('co', 'quaker', 'owns'), ('co', 'sodastream', 'owns'), ('co', 'rockstar', 'owns'), ('co', 'poppi', 'owns')],
 '1965年にペプシコーラとフリトレーが合併して誕生した飲料・スナックの会社。2018年からラモン・ラガルタがCEOを務めています。')

# ---------------- Verizon ----------------
deep('VZ', 'Verizon', 2000, NOTE, [
  P('seidenberg', 'アイバン・セイデンバーグ', 'Ivan Seidenberg', 2000, '2000〜2011年にCEO。ベル・アトランティックとGTEの合併で誕生した時のトップ。', '元CEO', 2011),
  P('mcadam', 'ローウェル・マカダム', 'Lowell McAdam', 2012, '2012〜2018年にCEO。', '元CEO', 2018),
  P('vestberg', 'ハンス・ベストベリ', 'Hans Vestberg', 2018, '2018〜2025年にCEO。', '元CEO', 2025),
  P('schulman', 'ダン・シュルマン', 'Dan Schulman', 2025, '2025年10月からCEO。PayPalの元CEO。', 'CEO'),
  P('bertolini', 'マーク・バートリーニ', 'Mark Bertolini', 2025, '会長。', '会長'),
  P('skiadas', 'トニー・スキアダス', 'Tony Skiadas', 2024, 'CFO。', 'CFO'),
  O('bellatlantic', 'Bell Atlantic', 2000, '2000年にGTEと合併して誕生。', '合併(2000年)'),
  O('gte', 'GTE', 2000, '2000年にBell Atlanticと合併。', '合併(2000年)'),
  O('vodafone', 'Vodafone', 2014, 'Verizon Wirelessの45%を持っていたが、2014年に約1,300億ドルで売却。', '元の共同出資者'),
  O('alltel', 'Alltel', 2008, '2008年に約281億ドルで買収。', '買収(2008年)'),
  O('aol', 'AOL', 2015, '2015年に約44億ドルで買収(のち売却)。', '買収(2015年)'),
  O('frontier', 'Frontier Communications', 2024, '2024年に約200億ドルでの買収を発表。', '買収発表(2024年)'),
 ] + holders([('Vanguard', '6.4', M), ('BlackRock', '5.9', M), ('State Street', '4.4', M)]),
 [('seidenberg', 'mcadam', 'link', '後任'), ('mcadam', 'vestberg', 'link', '後任'), ('vestberg', 'schulman', 'link', '後任', 2025), ('co', 'bellatlantic', 'owns'), ('co', 'gte', 'owns'), ('co', 'alltel', 'owns'), ('co', 'aol', 'owns'), ('co', 'frontier', 'owns'), ('co', 'vodafone', 'link', '合弁を解消')],
 '2000年にベル・アトランティックとGTEが合併して誕生した通信大手。2025年10月からダン・シュルマンがCEOを務めています。')

# ---------------- ConocoPhillips ----------------
deep('COP', 'ConocoPhillips', 2002, NOTE + '2026年9月1日のCEO交代は、会社の発表(2026年8月6日)に基づきます。', [
  P('dunham', 'アーチー・ダナム', 'Archie Dunham', 2002, 'コノコのCEO。2002年の合併後に初代会長。', '元会長', 2004),
  P('mulva', 'ジム・マルバ', 'Jim Mulva', 2002, '2002〜2012年にCEO。', '元CEO', 2012),
  P('lance', 'ライアン・ランス', 'Ryan Lance', 2012, '2012年から2026年8月までCEO。2026年9月から執行会長。', '会長(執行)'),
  P('obrien', 'アンディ・オブライエン', "Andy O'Brien", 1997, '2026年9月1日からCEO(CFOから昇格)。', 'CEO'),
  P('haynes', 'コニー・ヘインズ・ウェルシュ', 'Konnie Haynes-Welsh', 2026, '2026年9月からCFO。', 'CFO'),
  O('conoco', 'Conoco', 2002, '2002年にPhillipsと合併。', '合併(2002年)'),
  O('phillips', 'Phillips Petroleum', 2002, '2002年にConocoと合併。', '合併(2002年)'),
  O('burlington', 'Burlington Resources', 2006, '2006年に約360億ドルで買収。', '買収(2006年)'),
  O('p66', 'Phillips 66', 2012, '2012年に精製・販売部門を分離。', '分離(2012年)'),
  O('concho', 'Concho Resources', 2021, '2021年に約97億ドルで買収。', '買収(2021年)'),
  O('marathonoil', 'Marathon Oil', 2024, '2024年に約225億ドルで買収。', '買収(2024年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.2', M), ('State Street', '5.5', M)]),
 [('dunham', 'mulva', 'link', '後任'), ('mulva', 'lance', 'link', '後任', 2012), ('lance', 'obrien', 'link', 'CEO交代', 2026), ('co', 'conoco', 'owns'), ('co', 'phillips', 'owns'), ('co', 'burlington', 'owns'), ('co', 'concho', 'owns'), ('co', 'marathonoil', 'owns'), ('co', 'p66', 'owns', '分離')],
 '2002年にコノコとフィリップスが合併して誕生した石油・ガスの会社。2026年9月にアンディ・オブライエンがCEOへ就任しました。')

# ---------------- Abbott ----------------
deep('ABT', 'Abbott Laboratories', 1888, NOTE + 'Exact Sciencesの買収(2025年)は報道に基づきます。', [
  P('wabbott', 'ウォレス・アボット', 'Wallace Abbott', 1888, '1888年にシカゴで創業した医師。', '創業者', 1921, 1),
  P('white', 'マイルズ・ホワイト', 'Miles White', 1984, '1998〜2020年にCEO。', '元CEO', 2020),
  P('ford', 'ロバート・フォード', 'Robert Ford', 1996, '2020年からCEO(会長も)。', '会長兼CEO'),
  P('boudreau', 'フィル・ブードロー', 'Phil Boudreau', 2002, 'CFO。', 'CFO'),
  O('abbvie', 'AbbVie', 2013, '2013年に医薬品部門を分離して設立。', '分離(2013年)'),
  O('stjude', 'St. Jude Medical', 2017, '2017年に約250億ドルで買収。', '買収(2017年)'),
  O('alere', 'Alere', 2017, '2017年に約53億ドルで買収。', '買収(2017年)'),
  O('exact', 'Exact Sciences', 2025, '2025年に約210億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.6', M), ('State Street', '4.7', M)]),
 [('wabbott', 'white', 'link', '源流'), ('white', 'ford', 'link', '後任', 2020), ('co', 'abbvie', 'owns', '分離'), ('co', 'stjude', 'owns'), ('co', 'alere', 'owns'), ('co', 'exact', 'owns')],
 '1888年に創業した医療機器・診断薬の会社。2013年に医薬品部門をAbbVieとして分離し、2020年からロバート・フォードがCEOを務めています。')
