from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- 3M ----------------
deep('MMM', '3M', 1902, NOTE, [
  P('bryan', 'ヘンリー・ブライアン', 'Henry Bryan', 1902, '1902年にミネソタ州で3Mを共同創業した5人の1人。', '共同創業者', 1905, 1),
  P('cable', 'ハーモン・ケーブル', 'Hermon Cable', 1902, '共同創業者の1人。', '共同創業者', 1905, 1),
  P('mcknight', 'ウィリアム・マクナイト', 'William McKnight', 1907, '1907年に入社。長く社長・会長を務め、会社を大きくしました。', '元社長・会長', 1966),
  P('mcnerney', 'ジム・マクナーニー', 'Jim McNerney', 2001, '2001〜2005年にCEO。のちボーイングのCEO。', '元CEO', 2005),
  P('buckley', 'ジョージ・バックリー', 'George Buckley', 2005, '2005〜2012年にCEO。', '元CEO', 2012),
  P('thulin', 'インゲ・トゥリン', 'Inge Thulin', 1979, '2012〜2018年にCEO。', '元CEO', 2018),
  P('roman', 'マイク・ローマン', 'Mike Roman', 1988, '2018〜2024年にCEO。', '元CEO', 2024),
  P('brown', 'ビル・ブラウン', 'Bill Brown', 2024, '2024年5月からCEO兼会長。元ハリス/L3ハリスのCEO。', '会長兼CEO'),
  P('maheshwari', 'アヌラグ・マヘシュワリ', 'Anurag Maheshwari', 2024, 'CFO。', 'CFO'),
  O('scott', 'Scott Safety', 2017, '2017年に約20億ドルで買収。', '買収(2017年)'),
  O('acelity', 'Acelity', 2019, '2019年に約67億ドルで買収(のちSolventumへ)。', '買収(2019年)'),
  O('solventum', 'Solventum', 2024, '2024年4月にヘルスケア事業を分離。', '分離(2024年)'),
  O('pfas', 'PFAS・耳栓の訴訟', 2023, '2023年にPFAS(水質汚染)で約103億ドル、耳栓で約60億ドルの和解に合意と報じられています。', '和解(2023年)'),
 ] + holders([('JPMorgan Asset Mgmt', '7.6', M), ('BlackRock', '6.9', M), ('Vanguard', '6.6', M)]),
 [('bryan', 'cable', 'link', '共同創業'), ('mcknight', 'bryan', 'link', '会社を引き継ぐ'), ('mcnerney', 'buckley', 'link', '後任'), ('buckley', 'thulin', 'link', '後任'), ('thulin', 'roman', 'link', '後任'), ('roman', 'brown', 'link', '後任', 2024), ('co', 'scott', 'owns'), ('co', 'acelity', 'owns'), ('co', 'solventum', 'owns', '分離'), ('co', 'pfas', 'link', '和解')],
 '1902年にミネソタ州で創業した素材・製品の会社。2024年5月からビル・ブラウンがCEOを務めています。')

# ---------------- Blackstone ----------------
deep('BX', 'Blackstone', 1985, NOTE, [
  P('peterson', 'ピート・ピーターソン', 'Pete Peterson', 1985, '共同創業者。元米商務長官。2018年に亡くなりました。', '共同創業者', 2018, 1),
  P('schwarzman', 'スティーブン・シュワルツマン', 'Stephen Schwarzman', 1985, '共同創業者。会長兼CEO。', '共同創業者 / 会長兼CEO', None, 1),
  P('gray', 'ジョナサン・グレイ', 'Jonathan Gray', 1992, '社長兼COO。不動産事業を率いました。', '社長兼COO'),
  P('chae', 'マイケル・チェイ', 'Michael Chae', 2007, 'CFO。', 'CFO'),
  O('lehman', 'Lehman Brothers', 1985, 'ピーターソン氏の前職。共同創業の源流。', '前職の会社'),
  O('cic', '中国投資有限責任公司', 2007, '2007年のIPOで約30億ドルを出資。', '出資者(2007年)', 'i'),
  O('hilton', 'Hilton', 2007, '2007年に約260億ドルのLBOで買収(のち上場)。', '買収(2007年)'),
  O('blackrock', 'BlackRock', 1988, '1988年にブラックストーン内の債券部門として始まり、のち独立。', '源流の事業'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '5.5', M), ('Eaton Vance', '4.6', M)]),
 [('peterson', 'schwarzman', 'link', '共同創業'), ('schwarzman', 'gray', 'link', '後継候補'), ('peterson', 'lehman', 'moved', '前職'), ('co', 'hilton', 'owns'), ('co', 'blackrock', 'owns', '源流')],
 '1985年にピーターソン氏とシュワルツマン氏が創業した投資会社。スティーブン・シュワルツマンが会長兼CEOを務めています。')

# ---------------- Cadence ----------------
deep('CDNS', 'Cadence Design Systems', 1988, NOTE, [
  P('costello', 'ジョー・コステロ', 'Joe Costello', 1988, '1988〜1997年にCEO。SDA SystemsとECADの合併後の初代CEO。', '元CEO', 1997),
  P('bingham', 'レイ・ビンガム', 'Ray Bingham', 2005, '2005〜2008年にCEO。', '元CEO', 2008),
  P('tan', 'リップブー・タン', 'Lip-Bu Tan', 2008, '2009〜2021年にCEO。のちIntelのCEO(2025年)。', '元CEO', 2021),
  P('devgan', 'アニルド・デヴガン', 'Anirudh Devgan', 2012, '2021年12月からCEO(社長も)。', '社長兼CEO'),
  P('wall', 'ジョン・ウォール', 'John Wall', 2016, 'CFO。', 'CFO'),
  O('sda', 'SDA Systems', 1988, '1988年にECADと合併して誕生。', '合併(1988年)'),
  O('ecad', 'ECAD', 1988, '1988年にSDA Systemsと合併。', '合併(1988年)'),
  O('denali', 'Denali Software', 2010, '2010年に約3億ドルで買収。', '買収(2010年)'),
  O('tensilica', 'Tensilica', 2013, '2013年に約3.8億ドルで買収。', '買収(2013年)'),
  O('beta', 'BETA CAE', 2024, '2024年に約12.4億ドルで買収。', '買収(2024年)'),
  O('intel', 'Intel', 2025, 'タン氏がCEOを務める会社(2025年〜)。', '関連'),
 ] + holders([('BlackRock', '6.9', M), ('Vanguard', '6.5', M), ('State Street', '4.7', M)]),
 [('costello', 'bingham', 'link'), ('bingham', 'tan', 'link', '後任', 2009), ('tan', 'devgan', 'link', '後任', 2021), ('tan', 'intel', 'moved', 'CEOに就任'), ('co', 'sda', 'owns'), ('co', 'ecad', 'owns'), ('co', 'denali', 'owns'), ('co', 'tensilica', 'owns'), ('co', 'beta', 'owns')],
 '1988年にSDA SystemsとECADが合併して誕生した半導体設計ソフトの会社。2021年12月からアニルド・デヴガンがCEOを務めています。')

# ---------------- Trane Technologies ----------------
deep('TT', 'Trane Technologies', 1871, NOTE, [
  P('jtrane', 'ジェームズ・トレーン', 'James Trane', 1913, '1913年にTrane(ウィスコンシン州)を創業。', 'Trane創業者', 1936, 1),
  P('rtrane', 'レウベン・トレーン', 'Reuben Trane', 1913, 'Trane創業者の息子で、技術者。', 'Trane共同創業者', 1954, 1),
  P('lamach', 'マイケル・ラマック', 'Michael Lamach', 1996, '2010〜2021年にCEO。', '元CEO', 2021),
  P('regnery', 'デイブ・レグナリー', 'Dave Regnery', 1995, '2021年からCEO(会長も)。', '会長兼CEO'),
  P('kuehn', 'クリス・キューン', 'Chris Kuehn', 2021, 'CFO。', 'CFO'),
  O('ingersoll', 'Ingersoll Rand', 1871, '1871年と1905年の会社が源流。2020年にTrane Technologiesへ社名変更。', '前身'),
  O('american', 'American Standard', 2008, '2008年にTraneの親会社だった空調事業を、約100億ドルでIngersoll Randが買収。', '買収(2008年)'),
  O('gardner', 'Gardner Denver', 2020, '2020年に産業事業を分離して統合(Ingersoll Rand Inc.)。', '分離(2020年)'),
 ] + holders([('BlackRock', '6.7', M), ('Vanguard', '6.6', M), ('JPMorgan Asset Mgmt', '5.7', M)]),
 [('jtrane', 'rtrane', 'link', '親子'), ('lamach', 'regnery', 'link', '後任', 2021), ('ingersoll', 'lamach', 'link', '前身'), ('co', 'ingersoll', 'owns'), ('co', 'american', 'owns'), ('co', 'gardner', 'owns', '分離')],
 'Ingersoll Randが2020年にTrane Technologiesへ社名変更した、空調の会社。2021年からデイブ・レグナリーがCEOを務めています。')

# ---------------- Freeport-McMoRan ----------------
deep('FCX', 'Freeport-McMoRan', 1912, NOTE + 'グラスベルグ鉱山の事故(2025年9月)は報道に基づきます。', [
  P('jmoffett', 'ジム・ボブ・モフェット', 'Jim Bob Moffett', 1969, 'McMoRanの共同創業者。長くFreeportを率いました。', '元会長', 2003),
  P('adkerson', 'リチャード・アドカーソン', 'Richard Adkerson', 1989, '2003〜2024年にCEO。現在は会長。', '会長'),
  P('quirk', 'キャスリーン・クワーク', 'Kathleen Quirk', 2003, '2024年からCEO。', 'CEO'),
  O('freeportsulphur', 'Freeport Sulphur', 1912, '1912年に設立された源流の会社。', '源流(1912年)'),
  O('phelps', 'Phelps Dodge', 2007, '2007年に約259億ドルで買収。', '買収(2007年)'),
  O('plains', 'Plains Exploration & Production', 2013, '2013年に約69億ドルで買収(のち売却)。', '買収(2013年)'),
  O('mindid', 'MIND ID(インドネシア政府)', 2018, '2018年にグラスベルグ鉱山の事業会社の過半(51%)を取得。', '大株主(事業会社)', 'i'),
  O('grasberg', 'グラスベルグ鉱山', 1988, 'インドネシアの世界最大級の銅・金鉱山。', '事業'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.1', M), ('Fisher Asset Mgmt', '4.7', M)]),
 [('jmoffett', 'adkerson', 'link', '後任'), ('adkerson', 'quirk', 'link', '後任', 2024), ('co', 'phelps', 'owns'), ('co', 'plains', 'owns'), ('co', 'grasberg', 'owns'), ('mindid', 'grasberg', 'invest2', '過半を取得')],
 '1912年のFreeport Sulphurを源流とする銅・金の鉱山会社。2024年からキャスリーン・クワークがCEOを務めています。')

# ---------------- Synopsys ----------------
deep('SNPS', 'Synopsys', 1986, NOTE, [
  P('degeus', 'アート・デ・ゲウス', 'Aart de Geus', 1986, '共同創業者。2024年までCEO。現在は会長。', '共同創業者 / 会長', None, 1),
  P('gregory', 'デビッド・グレゴリー', 'David Gregory', 1986, '共同創業者。', '共同創業者', 1990, 1),
  P('ghazi', 'サシーン・ガジ', 'Sassine Ghazi', 2012, '2024年からCEO(社長も)。', '社長兼CEO'),
  P('glaser', 'シェラ・グレイザー', 'Shelagh Glaser', 2024, 'CFO。', 'CFO'),
  O('ge', 'GE', 1986, '創業者がGEの研究所の出身。', '源流'),
  O('magma', 'Magma Design Automation', 2012, '2012年に約5.2億ドルで買収。', '買収(2012年)'),
  O('coverity', 'Coverity', 2014, '2014年に約3.75億ドルで買収。', '買収(2014年)'),
  O('blackduck', 'Black Duck', 2017, '2017年に約5.5億ドルで買収。', '買収(2017年)'),
  O('ansys', 'Ansys', 2025, '2025年に約350億ドルで買収。', '買収(2025年)'),
 ] + holders([('Vanguard', '6.5', M), ('BlackRock', '6.1', M), ('State Street', '4.7', M)]),
 [('degeus', 'gregory', 'link', '共同創業'), ('degeus', 'ghazi', 'link', '後任', 2024), ('ge', 'degeus', 'link', '源流'), ('co', 'magma', 'owns'), ('co', 'coverity', 'owns'), ('co', 'blackduck', 'owns'), ('co', 'ansys', 'owns')],
 '1986年にアート・デ・ゲウスらが創業した半導体設計ソフトの会社。2024年からサシーン・ガジがCEOを務めています。')
