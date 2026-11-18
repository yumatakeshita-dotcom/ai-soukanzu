from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- TJX ----------------
deep('TJX', 'TJX', 1956, NOTE, [
  P('cammarata', 'バーナード・カマラータ', 'Bernard Cammarata', 1974, 'T.J.マックスを築いた経営者。', '元CEO', 2000),
  P('meyrowitz', 'キャロル・メイロウィッツ', 'Carol Meyrowitz', 1983, '2007〜2015年にCEO。現在は執行会長。', '会長(執行)'),
  P('herrman', 'アーニー・ヘルマン', 'Ernie Herrman', 1989, '2016年からCEO。', 'CEO'),
  P('klinger', 'ジョン・クリンガー', 'John Klinger', 2021, 'CFO。', 'CFO'),
  O('zayre', 'Zayre', 1956, 'T.J.マックスやマーシャルズを持っていた親会社。TJXは1989年に分離。', '分離元(1989年)'),
  O('marshalls', 'Marshalls', 1956, '1956年に創業。', '傘下'),
  O('tjmaxx', 'T.J. Maxx', 1977, '1977年に開業。', '傘下'),
  O('sierra', 'Sierra Trading Post', 2012, '2012年に買収。', '買収(2012年)'),
 ] + holders([('BlackRock', '7.3', M), ('Vanguard', '6.6', M), ('State Street', '4.5', M)]),
 [('cammarata', 'meyrowitz', 'link', '後任'), ('meyrowitz', 'herrman', 'link', '後任', 2016), ('co', 'marshalls', 'owns'), ('co', 'tjmaxx', 'owns'), ('co', 'sierra', 'owns'), ('zayre', 'tjmaxx', 'link', '開業')],
 'T.J.マックスやマーシャルズなどを運営するオフプライス小売の会社。2016年からアーニー・ヘルマンがCEOを務めています。')

# ---------------- Accenture ----------------
deep('ACN', 'Accenture', 1989, NOTE, [
  P('forehand', 'ジョー・フォアハンド', 'Joe Forehand', 1999, '独立後の2000〜2004年にCEO。', '元CEO', 2004),
  P('green', 'ウィリアム・グリーン', 'William Green', 1986, '2004〜2010年にCEO。', '元CEO', 2010),
  P('nanterme', 'ピエール・ナンテルム', 'Pierre Nanterme', 1983, '2011〜2019年にCEO。2019年に亡くなりました。', '元CEO', 2019),
  P('sweet', 'ジュリー・スウィート', 'Julie Sweet', 2010, '2019年9月からCEO(会長も)。', '会長兼CEO'),
  P('park', 'アンジー・パーク', 'Angie Park', 2023, 'CFO。', 'CFO'),
  O('andersen', 'Arthur Andersen', 1989, 'アンダーセン・コンサルティングとして1989年に独立した部門。2001年にAccentureへ改名。', '源流'),
  O('avanade', 'Avanade', 2000, '2000年にMicrosoftと設立した合弁会社。', '合弁(2000年)'),
  O('fjord', 'Fjord', 2013, '2013年に買収(デザイン)。', '買収(2013年)'),
  O('droga5', 'Droga5', 2019, '2019年に買収(広告)。', '買収(2019年)'),
 ] + holders([('BlackRock', '7.0', M), ('Vanguard', '6.6', M), ('State Street', '5.0', M)]),
 [('forehand', 'green', 'link', '後任'), ('green', 'nanterme', 'link', '後任'), ('nanterme', 'sweet', 'link', '後任', 2019), ('andersen', 'forehand', 'link', '独立を主導'), ('co', 'avanade', 'owns'), ('co', 'fjord', 'owns'), ('co', 'droga5', 'owns')],
 'アーサー・アンダーセンのコンサルティング部門が2001年にAccentureとして独立した会社。2019年からジュリー・スウィートがCEOを務めています。')

# ---------------- Charles Schwab ----------------
deep('SCHW', 'Charles Schwab', 1971, NOTE, [
  P('cschwab', 'チャールズ・シュワブ', 'Charles Schwab', 1971, '創業者。共同会長。約5.4%を保有(MarketScreener)。', '創業者 / 共同会長', None, 1),
  P('bettinger', 'ウォルト・ベッティンガー', 'Walt Bettinger', 1999, '2008〜2022年にCEO。', '元CEO', 2022),
  P('wurster', 'リック・ワースター', 'Rick Wurster', 2007, '2022年10月からCEO。', 'CEO'),
  O('tdameritrade', 'TD Ameritrade', 2020, '2020年に約260億ドルで買収。', '買収(2020年)'),
  O('usaa', 'USAAのブローカレッジ事業', 2020, '2020年に約18億ドルで買収。', '買収(2020年)'),
  O('dodge', 'Dodge & Cox', 2026, '約4.5%を持つ上位株主(MarketScreener)。', '株主(約4.5%)', 'i'),
  O('tdbank', 'TD Bank', 2020, 'TD Ameritradeの売却に伴い、Schwab株を持つ。', '大口の株主', 'i'),
 ] + holders([('Vanguard', '6.2', M), ('BlackRock', '5.8', M)]),
 [('cschwab', 'bettinger', 'link', 'CEOを託す'), ('bettinger', 'wurster', 'link', '後任', 2022), ('co', 'tdameritrade', 'owns'), ('co', 'usaa', 'owns')],
 '1971年にチャールズ・シュワブが創業した証券会社。2022年からリック・ワースターがCEOを務めています。')

# ---------------- Southern Copper ----------------
deep('SCCO', 'Southern Copper', 1952, NOTE + '歴代の経営者の情報は少なく、確認できた範囲だけを載せています。', [
  P('larrea', 'ヘルマン・ラレア', 'German Larrea', 1999, '親会社Grupo Mexicoの会長。1999年にAsarcoを通じて支配。', '親会社の会長'),
  P('rocha', 'オスカル・ゴンサレス・ロチャ', 'Oscar Gonzalez Rocha', 1990, 'CEO。', 'CEO'),
  O('grupomexico', 'Grupo México', 1999, 'メキシコの鉱山・鉄道会社。支配株主(約90%)。', '親会社(約90%)', 'i'),
  O('asarco', 'Asarco', 1999, '1999年にGrupo Mexicoが買収した米国の銅会社(Southern Copperの旧株主)。', '旧親会社'),
  O('cerroverde', 'Cerro Verde', 2005, 'ペルーの銅鉱山(約20%の持ち分)。', '出資先'),
 ] + holders([('Capital Group', '0.9', M), ('BlackRock', '0.8', M)]),
 [('larrea', 'grupomexico', 'link', '会長'), ('grupomexico', 'asarco', 'link', '1999年に買収'), ('co', 'cerroverde', 'invest2', '出資')],
 'ペルーとメキシコに鉱山を持つ銅の会社。Grupo Méxicoが約90%を持つ支配株主です。')

# ---------------- Intuitive Surgical ----------------
deep('ISRG', 'Intuitive Surgical', 1995, NOTE, [
  P('moll', 'フレデリック・モル', 'Frederic Moll', 1995, '共同創業者。', '共同創業者', 2003, 1),
  P('freund', 'ジョン・フロイント', 'John Freund', 1995, '共同創業者(初期の会長)。', '共同創業者', 2005, 1),
  P('younge', 'ロバート・ヤング', 'Robert Younge', 1995, '共同創業者。', '共同創業者', 1997, 1),
  P('lsmith', 'ロニー・スミス', 'Lonnie Smith', 1997, '1997〜2010年にCEO。', '元CEO', 2010),
  P('guthart', 'ゲイリー・ガサート', 'Gary Guthart', 1996, '2010〜2025年にCEO。現在は会長。', '会長'),
  P('rosa', 'デイブ・ローザ', 'Dave Rosa', 2000, '2025年からCEO。', 'CEO'),
  P('barratt', 'クレイグ・バラット', 'Craig Barratt', 2020, '取締役(英語版Wikipedia)。', '取締役'),
  O('sri', 'SRI International', 1995, '手術ロボットの技術の起点となった研究機関。', '技術の源流'),
  O('computermotion', 'Computer Motion', 2003, '2003年に合併(競合)。', '合併(2003年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.1', M), ('State Street', '4.5', M)]),
 [('moll', 'freund', 'link', '共同創業'), ('moll', 'younge', 'link', '共同創業'), ('sri', 'moll', 'link', '技術を移転'), ('lsmith', 'guthart', 'link', '後任', 2010), ('guthart', 'rosa', 'link', '後任', 2025), ('co', 'computermotion', 'owns')],
 '1995年に創業した手術支援ロボット「ダビンチ」の会社。2025年からデイブ・ローザがCEOを務めています。')

# ---------------- Seagate ----------------
deep('STX', 'Seagate Technology', 1979, NOTE, [
  P('shugart', 'アル・シュガート', 'Al Shugart', 1979, '共同創業者。1998年まで経営。', '共同創業者', 1998, 1),
  P('mitchell', 'トム・ミッチェル', 'Tom Mitchell', 1979, '共同創業者。', '共同創業者', 1982, 1),
  P('conner', 'フィニス・コナー', 'Finis Conner', 1979, '共同創業者。のちConner Peripheralsを創業。', '共同創業者', 1985, 1),
  P('luczo', 'スティーブ・ルッツォ', 'Steve Luczo', 1993, '2007〜2017年にCEO。', '元CEO', 2017),
  P('mosley', 'デイブ・モズリー', 'Dave Mosley', 1998, '2017年からCEO(会長も)。', '会長兼CEO'),
  P('romano', 'ジャンルカ・ロマーノ', 'Gianluca Romano', 2018, 'CFO。', 'CFO'),
  O('conner', 'Conner Peripherals', 1996, '1996年に合併。', '合併(1996年)'),
  O('maxtor', 'Maxtor', 2006, '2006年に約19億ドルで買収。', '買収(2006年)'),
  O('samsunghdd', 'サムスンのHDD事業', 2011, '2011年に約14億ドルで買収。', '買収(2011年)'),
  O('xyratex', 'Xyratex', 2014, '2014年に買収。', '買収(2014年)'),
 ] + holders([('Vanguard', '6.4', M), ('BlackRock', '4.7', M), ('State Street', '4.4', M)]),
 [('shugart', 'mitchell', 'link', '共同創業'), ('shugart', 'conner', 'link', '共同創業'), ('luczo', 'mosley', 'link', '後任', 2017), ('co', 'conner', 'owns'), ('co', 'maxtor', 'owns'), ('co', 'samsunghdd', 'owns'), ('co', 'xyratex', 'owns')],
 '1979年にアル・シュガートらが創業したハードディスクの会社。2017年からデイブ・モズリーがCEOを務めています。')

# ---------------- UBS ----------------
deep('UBS', 'UBS', 1862, NOTE, [
  P('grubel', 'オスワルト・グリューベル', 'Oswald Gruebel', 2009, '2009〜2011年にCEO。', '元CEO', 2011),
  P('weber', 'アクセル・ウェーバー', 'Axel Weber', 2012, '2012〜2022年に会長。', '元会長', 2022),
  P('ermotti', 'セルジオ・エルモッティ', 'Sergio Ermotti', 2011, '2011〜2020年と、2023年4月からCEO。', 'CEO'),
  P('hamers', 'ラルフ・ハマーズ', 'Ralph Hamers', 2020, '2020〜2022年にCEO。', '元CEO', 2022),
  P('kelleher', 'コルム・ケレハー', 'Colm Kelleher', 2022, '2022年から会長。モルガン・スタンレーの元社長。', '会長'),
  P('tuckner', 'トッド・タックナー', 'Todd Tuckner', 2022, 'CFO。', 'CFO'),
  O('sbc', 'Swiss Bank Corporation', 1998, '1998年にスイス・ユニオン銀行と合併(UBSの誕生)。', '合併(1998年)'),
  O('ubs1', 'Union Bank of Switzerland', 1998, '1998年にSBCと合併。', '合併(1998年)'),
  O('paine', 'PaineWebber', 2000, '2000年に約120億ドルで買収。', '買収(2000年)'),
  O('cs', 'Credit Suisse', 2023, '2023年3月に、スイス当局の主導で買収(約30億スイスフラン)。', '買収(2023年)'),
 ] + holders([('Norges Bank', '3.0', M), ('Vanguard', '3.0', M)]),
 [('weber', 'kelleher', 'link', '後任', 2022), ('hamers', 'ermotti', 'link', '後任', 2022), ('ermotti', 'hamers', 'link', '後任', 2020), ('co', 'sbc', 'owns'), ('co', 'ubs1', 'owns'), ('co', 'paine', 'owns'), ('co', 'cs', 'owns')],
 '1998年にスイスの2行が合併して誕生した銀行。2023年にクレディ・スイスを買収し、セルジオ・エルモッティがCEOを務めています。')

# ---------------- Lockheed Martin ----------------
deep('LMT', 'Lockheed Martin', 1995, NOTE, [
  P('augustine', 'ノーマン・オーガスティン', 'Norman Augustine', 1995, 'ロッキードとマーチン・マリエッタの合併(1995年)時のトップ。', '元CEO', 1997),
  P('coffman', 'ヴァンス・コフマン', 'Vance Coffman', 1997, '1997〜2004年にCEO。', '元CEO', 2004),
  P('stevens', 'ロバート・スティーブンス', 'Robert Stevens', 2004, '2004〜2012年にCEO。', '元CEO', 2012),
  P('hewson', 'マリリン・ヒューソン', 'Marillyn Hewson', 2013, '2013〜2020年にCEO。', '元CEO', 2020),
  P('taiclet', 'ジェームズ・テイクレット', 'James Taiclet', 2020, '2020年6月からCEO兼会長。', '会長兼CEO'),
  P('stjohn', 'フランク・セントジョン', 'Frank St. John', 1995, 'COO。', 'COO'),
  P('scott', 'エバン・スコット', 'Evan Scott', 2023, 'CFO。', 'CFO'),
  O('lockheed', 'Lockheed Corporation', 1995, '1995年にマーチン・マリエッタと合併。', '合併(1995年)'),
  O('martinmarietta', 'Martin Marietta', 1995, '1995年にロッキードと合併。', '合併(1995年)'),
  O('sikorsky', 'Sikorsky', 2015, '2015年に約90億ドルで買収。', '買収(2015年)'),
  O('aerojet', 'Aerojet Rocketdyne', 2022, '2022年に約44億ドルで買収を発表したが、米連邦取引委員会の反対で断念。', '買収断念(2022年)'),
 ] + holders([('State Street', '14.3', M), ('BlackRock', '7.0', M), ('Vanguard', '6.1', M)]),
 [('augustine', 'coffman', 'link', '後任'), ('coffman', 'stevens', 'link', '後任'), ('stevens', 'hewson', 'link', '後任'), ('hewson', 'taiclet', 'link', '後任', 2020), ('co', 'lockheed', 'owns'), ('co', 'martinmarietta', 'owns'), ('co', 'sikorsky', 'owns'), ('co', 'aerojet', 'link', '買収を断念')],
 '1995年にロッキードとマーチン・マリエッタが合併して誕生した防衛・航空の会社。2020年からジェームズ・テイクレットがCEOを務めています。')

# ---------------- AT&T ----------------
deep('T', 'AT&T', 1877, NOTE + 'LumenとEchoStarの買収(2025年)は報道に基づきます。', [
  P('bell', 'アレクサンダー・グラハム・ベル', 'Alexander Graham Bell', 1877, '電話の発明者。1877年にベル電話会社を設立。', '源流の創業者', 1880, 1),
  P('whitacre', 'エド・ウィテカー', 'Ed Whitacre', 1990, 'SBCのCEO。2005年にAT&Tを買収し、新生AT&Tの会長兼CEO。', '元会長兼CEO', 2007),
  P('stephenson', 'ランドール・スティーブンソン', 'Randall Stephenson', 1982, '2007〜2020年にCEO。', '元CEO', 2020),
  P('stankey', 'ジョン・スタンキー', 'John Stankey', 1985, '2020年7月からCEO(会長も)。', '会長兼CEO'),
  P('legg', 'ジェレミー・レッグ', 'Jeremy Legg', 2020, 'CTO(英語版Wikipedia)。', 'CTO'),
  P('mcelfresh', 'ジェフ・マケルフレッシュ', 'Jeff McElfresh', 2008, 'COO(英語版Wikipedia)。', 'COO'),
  P('desroches', 'パスカル・デロッシュ', 'Pascal Desroches', 2016, 'CFO。', 'CFO'),
  O('sbc', 'SBC Communications', 2005, '2005年にAT&Tを買収し、AT&Tの名を継いだ。', '買収側(2005年)'),
  O('bellsouth', 'BellSouth', 2006, '2006年に約860億ドルで買収。', '買収(2006年)'),
  O('directv', 'DirecTV', 2015, '2015年に約485億ドルで買収(のち分離)。', '買収(2015年)'),
  O('timewarner', 'Time Warner', 2018, '2018年に約850億ドルで買収。2022年にWarner Bros. Discoveryとして分離。', '買収(2018年)'),
  O('lumen', 'Lumenの光ファイバー事業', 2025, '2025年に約57.5億ドルで買収と報じられています。', '買収(2025年・報道)'),
  O('echostar', 'EchoStarの周波数', 2025, '2025年に約230億ドルで取得と報じられています。', '取得(2025年・報道)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.2', M), ('State Street', '4.9', M)]),
 [('bell', 'whitacre', 'link', '源流を継ぐ'), ('whitacre', 'stephenson', 'link', '後任'), ('stephenson', 'stankey', 'link', '後任', 2020), ('co', 'bellsouth', 'owns'), ('co', 'directv', 'owns'), ('co', 'timewarner', 'owns'), ('co', 'lumen', 'owns'), ('co', 'echostar', 'owns')],
 '1877年のベル電話会社を源流とする通信大手。2020年からジョン・スタンキーがCEOを務めています。')

# ---------------- Eaton ----------------
deep('ETN', 'Eaton', 1911, NOTE + 'Fibrebondの買収(2025年)は報道に基づきます。', [
  P('jeaton', 'ジョセフ・イートン', 'Joseph Eaton', 1911, '1911年にEaton Axleを創業。', '創業者', 1950, 1),
  P('cutler', 'アレクサンダー・カトラー', 'Alexander Cutler', 1992, '2000〜2016年にCEO。', '元CEO', 2016),
  P('arnold', 'クレイグ・アーノルド', 'Craig Arnold', 1992, '2016〜2023年にCEO。', '元CEO', 2024),
  P('ruiz', 'パウロ・ルイス', 'Paulo Ruiz', 1998, '2024年2月からCEO兼会長。', '会長兼CEO'),
  P('leonetti', 'オリビエ・レオネッティ', 'Olivier Leonetti', 2008, 'CFO。', 'CFO'),
  O('cooper', 'Cooper Industries', 2012, '2012年に約118億ドルで買収。アイルランドに本社を移す合併。', '買収(2012年)'),
  O('fibrebond', 'Fibrebond', 2025, '2025年に約14億ドルで買収と報じられています。', '買収(2025年・報道)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.8', M), ('State Street', '4.5', M)]),
 [('jeaton', 'cutler', 'link', '源流'), ('cutler', 'arnold', 'link', '後任', 2016), ('arnold', 'ruiz', 'link', '後任', 2024), ('co', 'cooper', 'owns'), ('co', 'fibrebond', 'owns')],
 '1911年にジョセフ・イートンが創業した電気設備・産業機器の会社。2024年からパウロ・ルイスがCEOを務めています。')
