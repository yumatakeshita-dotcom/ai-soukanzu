from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- Morgan Stanley ----------------
deep('MS', 'Morgan Stanley', 1935, NOTE, [
  P('hmorgan', 'ヘンリー・モルガン', 'Henry Morgan', 1935, 'J.P.モルガンの孫。1935年にハロルド・スタンレーらと創業。', '共同創業者', 1950, 1),
  P('hstanley', 'ハロルド・スタンレー', 'Harold Stanley', 1935, '共同創業者。初代社長。', '共同創業者', 1955, 1),
  P('purcell', 'フィリップ・パーセル', 'Philip Purcell', 1997, '1997〜2005年にCEO。Dean Witterとの合併(1997年)を主導。', '元CEO', 2005),
  P('mack', 'ジョン・マック', 'John Mack', 1972, '2005〜2010年にCEO。', '元CEO', 2010),
  P('gorman', 'ジェームズ・ゴーマン', 'James Gorman', 2006, '2010〜2023年にCEO、のち会長(現在は名誉会長)。', '名誉会長', None),
  P('pick', 'テッド・ピック', 'Ted Pick', 1996, '2024年1月からCEO、のち会長。', '会長兼CEO'),
  P('saperstein', 'アンディ・サパースタイン', 'Andy Saperstein', 2009, '共同社長。', '共同社長'),
  P('simkowitz', 'ダン・シムコウィッツ', 'Dan Simkowitz', 1999, '共同社長。', '共同社長'),
  P('yeshaya', 'シャロン・イェシャヤ', 'Sharon Yeshaya', 2013, 'CFO。', 'CFO'),
  O('mufg', '三菱UFJフィナンシャル・グループ', 2008, '2008年に約90億ドルを出資。約23.9%を持つ最大の株主(MarketScreener、2026年11月)。', '最大の株主(約23.9%)', 'i'),
  O('cic', '中国投資有限責任公司', 2007, '2007年に約50億ドルを出資(転換証券)。', '出資者(2007年)', 'i'),
  O('dw', 'Dean Witter', 1997, '1997年に合併。', '合併(1997年)'),
  O('smithbarney', 'Smith Barney', 2009, '2009年にシティと合弁を設立し、のち取得。', '取得(2009〜2013年)'),
  O('etrade', 'E*Trade', 2020, '2020年に約130億ドルで買収。', '買収(2020年)'),
  O('eatonvance', 'Eaton Vance', 2021, '2021年に約70億ドルで買収。', '買収(2021年)'),
 ] + holders([('State Street', '6.3', M), ('Vanguard', '4.9', M), ('BlackRock', '4.7', M)]),
 [('hmorgan', 'hstanley', 'link', '共同創業'), ('purcell', 'mack', 'link', '後任'), ('mack', 'gorman', 'link', '後任'), ('gorman', 'pick', 'link', '後任', 2024), ('co', 'dw', 'owns'), ('co', 'smithbarney', 'owns'), ('co', 'etrade', 'owns'), ('co', 'eatonvance', 'owns')],
 '1935年にJ.P.モルガンから分かれて創業した投資銀行。2024年からテッド・ピックがCEOを務め、三菱UFJが約24%を持っています。')

# ---------------- Caterpillar ----------------
deep('CAT', 'Caterpillar', 1925, NOTE, [
  P('holt', 'ベンジャミン・ホルト', 'Benjamin Holt', 1925, 'ホルト社の創業者。キャタピラー型トラクターの発明者。', '源流の創業者', 1925, 1),
  P('best', 'C・L・ベスト', 'C. L. Best', 1925, 'ベスト社の創業者。1925年にホルト社と合併。', '源流の創業者', 1951, 1),
  P('fites', 'ドナルド・フィッツ', 'Donald Fites', 1990, '1990〜1999年にCEO。', '元CEO', 1999),
  P('barton', 'グレン・バートン', 'Glen Barton', 1999, '1999〜2004年にCEO。', '元CEO', 2004),
  P('owens', 'ジム・オーエンス', 'Jim Owens', 2004, '2004〜2010年にCEO。', '元CEO', 2010),
  P('oberhelman', 'ダグ・オーバーヘルマン', 'Doug Oberhelman', 2010, '2010〜2017年にCEO。', '元CEO', 2017),
  P('umpleby', 'ジム・アンプルビー', 'Jim Umpleby', 2017, '2017〜2024年にCEO。', '元CEO', 2025),
  P('creed', 'ジョー・クリード', 'Joe Creed', 2025, '2025年1月からCEO(会長も)。', '会長兼CEO'),
  P('bonfield', 'アンドリュー・ボンフィールド', 'Andrew Bonfield', 2023, 'CFO。', 'CFO'),
  O('solar', 'Solar Turbines', 1981, '1981年に買収。', '買収(1981年)'),
  O('perkins', 'Perkins Engines', 1998, '1998年に買収。', '買収(1998年)'),
  O('progress', 'Progress Rail', 2006, '2006年に買収(鉄道)。', '買収(2006年)'),
  O('bucyrus', 'Bucyrus International', 2011, '2011年に約88億ドルで買収(鉱山機械)。', '買収(2011年)'),
  O('statefarm', 'State Farm', 2026, '約3.2%を持つ上位株主(MarketScreener、2026年11月)。', '株主(約3.2%)', 'i'),
 ] + holders([('State Street', '7.5', M), ('Vanguard', '6.5', M), ('BlackRock', '6.5', M)]),
 [('holt', 'best', 'conflict', '競合から合併へ'), ('fites', 'barton', 'link', '後任'), ('barton', 'owens', 'link', '後任'), ('owens', 'oberhelman', 'link', '後任'), ('oberhelman', 'umpleby', 'link', '後任'), ('umpleby', 'creed', 'link', '後任', 2025), ('co', 'solar', 'owns'), ('co', 'perkins', 'owns'), ('co', 'progress', 'owns'), ('co', 'bucyrus', 'owns')],
 '1925年にホルト社とベスト社が合併して誕生した建設・鉱山機械の会社。2025年からジョー・クリードがCEOを務めています。')

# ---------------- Royal Bank of Canada ----------------
deep('RY', 'Royal Bank of Canada', 1864, NOTE + 'Royal Trust Corporation of Canadaは、RBCの信託子会社です。', [
  P('cleghorn', 'ジョン・クレグホーン', 'John Cleghorn', 1995, '1995〜2001年にCEO。', '元CEO', 2001),
  P('nixon', 'ゴード・ニクソン', 'Gord Nixon', 2001, '2001〜2014年にCEO。', '元CEO', 2014),
  P('mckay', 'デビッド・マッケイ', 'David McKay', 1983, '2014年からCEO。', 'CEO'),
  P('ahn', 'ナディーン・アン', 'Nadine Ahn', 2010, 'CFO。', 'CFO'),
  O('merchants', 'Merchants Bank of Halifax', 1864, '1864年に創業(のちのRBC)。', '源流(1864年)'),
  O('centura', 'Centura Banks', 2001, '2001年に買収(米国)。', '買収(2001年)'),
  O('citynational', 'City National Bank', 2015, '2015年に約54億ドルで買収。', '買収(2015年)'),
  O('hsbcca', 'HSBC Bank Canada', 2024, '2024年に約135億カナダドルで買収。', '買収(2024年)'),
  O('royaltrust', 'Royal Trust Corporation of Canada', 2026, 'RBCの信託子会社。約5.1%を持つ(Yahoo Finance・MarketScreener)。', '子会社・株主(約5.1%)', 'i'),
 ] + holders([('Vanguard', '5.1', M), ('BMO Bank NA', '4.1', M)]),
 [('merchants', 'cleghorn', 'link', '源流を継ぐ'), ('cleghorn', 'nixon', 'link', '後任'), ('nixon', 'mckay', 'link', '後任', 2014), ('co', 'centura', 'owns'), ('co', 'citynational', 'owns'), ('co', 'hsbcca', 'owns')],
 '1864年にハリファックスで創業したカナダ最大級の銀行。2014年からデビッド・マッケイがCEOを務めています。')

# ---------------- Texas Instruments ----------------
deep('TXN', 'Texas Instruments', 1930, NOTE, [
  P('karcher', 'J・クラレンス・カーチャー', 'J. Clarence Karcher', 1930, '1930年にGeophysical Service(TIの源流)を共同創業。', '源流の共同創業者', 1941, 1),
  P('kilby', 'ジャック・キルビー', 'Jack Kilby', 1958, '1958年に集積回路を発明。2000年にノーベル物理学賞。', '元エンジニア', 1983),
  P('haggerty', 'パット・ハガティ', 'Pat Haggerty', 1951, '半導体事業への転換を主導。', '元経営者', 1981),
  P('engibous', 'トム・エンジボウス', 'Tom Engibous', 1996, '1996〜2004年にCEO。', '元CEO', 2004),
  P('templeton', 'リッチ・テンプルトン', 'Rich Templeton', 2004, '2004〜2018年にCEO。', '元CEO', 2018),
  P('crutcher', 'ブライアン・クラッチャー', 'Brian Crutcher', 2018, '2018〜2023年にCEO。', '元CEO', 2023),
  P('ilan', 'ハビブ・イラン', 'Haviv Ilan', 2000, '2023年からCEO(2024年から会長も)。', '会長兼CEO'),
  P('lizardi', 'ラファエル・リザルディ', 'Rafael Lizardi', 2008, 'CFO。', 'CFO'),
  O('burrbrown', 'Burr-Brown', 2000, '2000年に約76億ドルで買収。', '買収(2000年)'),
  O('national', 'National Semiconductor', 2011, '2011年に約65億ドルで買収。', '買収(2011年)'),
 ] + holders([('Vanguard', '6.0', M), ('BlackRock', '5.7', M), ('State Street', '4.5', M)]),
 [('karcher', 'haggerty', 'link', '会社を引き継ぐ'), ('haggerty', 'kilby', 'link', '集積回路を支援'), ('engibous', 'templeton', 'link', '後任'), ('templeton', 'crutcher', 'link', '後任'), ('crutcher', 'ilan', 'link', '後任', 2023), ('co', 'burrbrown', 'owns'), ('co', 'national', 'owns')],
 '1930年のGeophysical Serviceを源流とする半導体の会社。1958年にジャック・キルビーが集積回路を発明し、2023年からハビブ・イランがCEOを務めています。')

# ---------------- RTX ----------------
deep('RTX', 'RTX', 1922, NOTE, [
  P('marshall', 'ローレンス・マーシャル', 'Laurence Marshall', 1922, 'レイセオン(1922年創業)の共同創業者。', '源流の共同創業者', 1950, 1),
  P('bush', 'ヴァネヴァー・ブッシュ', 'Vannevar Bush', 1922, 'レイセオンの共同創業者。のち米国の科学行政を率いました。', '源流の共同創業者', 1940, 1),
  P('kennedy', 'トム・ケネディ', 'Tom Kennedy', 2014, 'レイセオンのCEO(2014〜2020年)。RTXの執行会長。', '元CEO', 2021),
  P('hayes', 'グレッグ・ヘイズ', 'Greg Hayes', 2014, 'UTCのCEO(2014〜2020年)、RTXのCEO(2020〜2023年)。', '元CEO', 2023),
  P('calio', 'クリス・カリオ', 'Chris Calio', 1998, '2023年からCEO(2025年から会長も)。', '会長兼CEO'),
  P('mitchill', 'ニール・ミッチル', 'Neil Mitchill', 2011, 'CFO。', 'CFO'),
  O('goodrich', 'Goodrich', 2012, '2012年に約184億ドルで買収(UTC)。', '買収(2012年)'),
  O('rockwell', 'Rockwell Collins', 2018, '2018年に約300億ドルで買収(UTC)。', '買収(2018年)'),
  O('otis', 'Otis', 2020, '2020年にUTCから分離。', '分離(2020年)'),
  O('carrier', 'Carrier', 2020, '2020年にUTCから分離。', '分離(2020年)'),
 ] + holders([('State Street', '7.1', M), ('BlackRock', '6.9', M), ('Vanguard', '6.5', M)]),
 [('marshall', 'bush', 'link', '共同創業'), ('kennedy', 'hayes', 'link', '合併を主導', 2020), ('hayes', 'calio', 'link', '後任', 2023), ('co', 'goodrich', 'owns'), ('co', 'rockwell', 'owns'), ('co', 'otis', 'owns'), ('co', 'carrier', 'owns')],
 '2020年にレイセオン(1922年創業)とユナイテッド・テクノロジーズが合併して誕生。2023年からクリス・カリオがCEOを務めています。')

# ---------------- Goldman Sachs ----------------
deep('GS', 'Goldman Sachs', 1869, NOTE, [
  P('goldman', 'マーカス・ゴールドマン', 'Marcus Goldman', 1869, '1869年に創業。', '創業者', 1885, 1),
  P('sachs', 'サミュエル・サックス', 'Samuel Sachs', 1882, 'ゴールドマンの娘婿で、のち経営者。', '元経営者', 1928),
  P('weinberg', 'シドニー・ワインバーグ', 'Sidney Weinberg', 1907, '1930〜1969年に実質的な経営者。', '元経営者', 1969),
  P('paulson', 'ハンク・ポールソン', 'Hank Paulson', 1974, '1999〜2006年にCEO。のち米財務長官。', '元CEO', 2006),
  P('blankfein', 'ロイド・ブランクファイン', 'Lloyd Blankfein', 1982, '2006〜2018年にCEO。', '元CEO', 2018),
  P('solomon', 'デビッド・ソロモン', 'David Solomon', 1999, '2018年からCEO兼会長。DJ名義でも知られます。', '会長兼CEO'),
  P('waldron', 'ジョン・ウォルドロン', 'John Waldron', 1997, '社長兼COO。', '社長兼COO'),
  P('coleman', 'デニス・コールマン', 'Denis Coleman', 1994, 'CFO。', 'CFO'),
  O('berkshire', 'Berkshire Hathaway', 2008, '2008年に50億ドルを出資(優先株)。', '出資者(2008年)', 'i'),
  O('ayco', 'Ayco', 2003, '2003年に買収。', '買収(2003年)'),
  O('greensky', 'GreenSky', 2022, '2022年に約22億ドルで買収。', '買収(2022年)'),
 ] + holders([('State Street', '6.5', M), ('Vanguard', '6.3', M), ('BlackRock', '6.3', M)]),
 [('goldman', 'sachs', 'link', '娘婿'), ('sachs', 'weinberg', 'link'), ('paulson', 'blankfein', 'link', '後任'), ('blankfein', 'solomon', 'link', '後任', 2018), ('co', 'ayco', 'owns'), ('co', 'greensky', 'owns')],
 '1869年にマーカス・ゴールドマンが創業した投資銀行。2018年からデビッド・ソロモンがCEOを務めています。')

# ---------------- Thermo Fisher ----------------
deep('TMO', 'Thermo Fisher Scientific', 1956, NOTE, [
  P('hatsopoulos', 'ジョージ・ハツォプロス', 'George Hatsopoulos', 1956, 'Thermo Electron(1956年創業)の創業者。', '源流の創業者', 2001, 1),
  P('casper', 'マーク・キャスパー', 'Marc Casper', 2001, '2009年からCEO(会長も)。', '会長兼CEO'),
  P('pettiti', 'ジャンルカ・ペッティッティ', 'Gianluca Pettiti', 2007, '社長兼COO。', '社長兼COO'),
  P('williamson', 'スティーブン・ウィリアムソン', 'Stephen Williamson', 2010, 'CFO。', 'CFO'),
  O('fisher', 'Fisher Scientific', 2006, '2006年に合併(Thermo Electron×Fisher)。', '合併(2006年)'),
  O('lifetech', 'Life Technologies', 2014, '2014年に約136億ドルで買収。', '買収(2014年)'),
  O('patheon', 'Patheon', 2017, '2017年に約72億ドルで買収。', '買収(2017年)'),
  O('ppd', 'PPD', 2021, '2021年に約174億ドルで買収。', '買収(2021年)'),
  O('olink', 'Olink', 2024, '2024年に約31億ドルで買収。', '買収(2024年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '5.8', M), ('State Street', '4.6', M)]),
 [('hatsopoulos', 'casper', 'link', '会社を引き継ぐ'), ('co', 'fisher', 'owns'), ('co', 'lifetech', 'owns'), ('co', 'patheon', 'owns'), ('co', 'ppd', 'owns'), ('co', 'olink', 'owns')],
 '1956年のThermo Electronを源流に、2006年にFisher Scientificと合併して誕生。2009年からマーク・キャスパーがCEOを務めています。')

# ---------------- CrowdStrike ----------------
deep('CRWD', 'CrowdStrike', 2011, NOTE + '2024年7月19日の大規模障害は、同社の更新ファイルの不具合が原因と広く報じられました。', [
  P('kurtz', 'ジョージ・カーツ', 'George Kurtz', 2011, '共同創業者でCEO。', '共同創業者 / CEO', None, 1),
  P('alperovitch', 'ドミトリ・アルペロビッチ', 'Dmitri Alperovitch', 2011, '共同創業者でCTO。2020年に退社。', '共同創業者', 2020, 1),
  P('marston', 'グレッグ・マーストン', 'Gregg Marston', 2011, '共同創業者でCFO。', '共同創業者', 2014, 1),
  P('sentonas', 'マイケル・センタナス', 'Michael Sentonas', 2012, '社長。', '社長'),
  P('podbere', 'バート・ポドベア', 'Burt Podbere', 2020, 'CFO。', 'CFO'),
  O('accel', 'Accel', 2013, '初期の出資者。', '初期の出資者', 'i'),
  O('warburg', 'Warburg Pincus', 2014, '初期の出資者。', '初期の出資者', 'i'),
  O('capitalg', 'CapitalG', 2015, 'グーグル系ファンド。2015年に出資。', '出資者(2015年)', 'i'),
  O('humio', 'Humio', 2021, '2021年に約4億ドルで買収(ログ分析)。', '買収(2021年)'),
 ] + holders([('BlackRock', '6.4', M), ('Vanguard', '6.3', M), ('State Street', '4.5', M)]),
 [('kurtz', 'alperovitch', 'link', '共同創業'), ('kurtz', 'marston', 'link', '共同創業'), ('co', 'humio', 'owns')],
 '2011年にジョージ・カーツらが創業したエンドポイントセキュリティの会社。2019年に上場しました。')

# ---------------- Netflix ----------------
deep('NFLX', 'Netflix', 1997, NOTE, [
  P('hastings', 'リード・ヘイスティングス', 'Reed Hastings', 1997, '共同創業者。2023年までCEO、以後は執行会長。', '共同創業者 / 会長(執行)', None, 1),
  P('randolph', 'マーク・ランドルフ', 'Marc Randolph', 1997, '共同創業者で初代CEO。', '共同創業者', 2002, 1),
  P('sarandos', 'テッド・サランドス', 'Ted Sarandos', 2000, '共同CEO。コンテンツ責任者から昇格(2020年〜)。', '共同CEO'),
  P('peters', 'グレッグ・ピーターズ', 'Greg Peters', 2008, '共同CEO(2023年から)。', '共同CEO'),
  P('neumann', 'スペンサー・ニューマン', 'Spencer Neumann', 2019, 'CFO。', 'CFO'),
  P('verdu', 'マイク・ヴェルドゥ', 'Mike Verdu', 2022, 'ゲーム担当の副社長。', 'ゲーム担当副社長'),
  O('millar', 'Millarworld', 2017, '2017年に買収(コミック)。', '買収(2017年)'),
  O('dahl', 'Roald Dahl Story Company', 2021, '2021年に買収。', '買収(2021年)'),
  O('scanline', 'Scanline VFX', 2021, '2021年に買収。', '買収(2021年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.2', M), ('State Street', '4.3', M)]),
 [('hastings', 'randolph', 'link', '共同創業'), ('hastings', 'sarandos', 'link', '共同CEO'), ('hastings', 'peters', 'link', 'CEOを譲る', 2023), ('co', 'millar', 'owns'), ('co', 'dahl', 'owns'), ('co', 'scanline', 'owns')],
 '1997年にDVDレンタルで創業した動画配信の会社。2023年からテッド・サランドスとグレッグ・ピーターズが共同CEOを務めています。')

# ---------------- Amgen ----------------
deep('AMGN', 'Amgen', 1980, NOTE, [
  P('binder', 'ゴードン・バインダー', 'Gordon Binder', 1988, '1988〜2000年にCEO。', '元CEO', 2000),
  P('sharer', 'ケビン・シェアラー', 'Kevin Sharer', 1992, '2000〜2012年にCEO。', '元CEO', 2012),
  P('bradway', 'ロバート・ブラッドウェイ', 'Robert Bradway', 2006, '2012年からCEO(会長も)。', '会長兼CEO'),
  P('bradner', 'ジェイ・ブラドナー', 'Jay Bradner', 2019, '研究開発の責任者。', '研究開発責任者'),
  P('griffith', 'ピーター・グリフィス', 'Peter Griffith', 2023, 'CFO。', 'CFO'),
  O('immunex', 'Immunex', 2002, '2002年に約160億ドルで買収。', '買収(2002年)'),
  O('onyx', 'Onyx Pharmaceuticals', 2013, '2013年に約104億ドルで買収。', '買収(2013年)'),
  O('horizon', 'Horizon Therapeutics', 2023, '2023年に約278億ドルで買収。', '買収(2023年)'),
  O('beigene', 'BeiGene', 2020, '2020年に約27億ドルで約20%を取得(のち縮小)。', '出資(2020年)'),
 ] + holders([('BlackRock', '6.8', M), ('Vanguard', '6.5', M), ('State Street', '5.7', M)]),
 [('binder', 'sharer', 'link', '後任'), ('sharer', 'bradway', 'link', '後任', 2012), ('co', 'immunex', 'owns'), ('co', 'onyx', 'owns'), ('co', 'horizon', 'owns'), ('co', 'beigene', 'invest2', '出資')],
 '1980年創業のバイオ医薬の会社。2012年からロバート・ブラッドウェイがCEOを務めています。')
