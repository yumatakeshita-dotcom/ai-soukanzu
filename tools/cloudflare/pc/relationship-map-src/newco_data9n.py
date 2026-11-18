from newco_data9 import deep, P, O
from newco_data9c import NOTE, holders, Y, M

# ---------------- CME Group ----------------
deep('CME', 'CME Group', 1898, NOTE + 'ダフィー氏の退任とフィッツパトリック氏のCEO就任(2027年3月)は、英語版Wikipediaの記載に基づきます。', [
  P('melamed', 'レオ・メラメド', 'Leo Melamed', 1966, '「金融先物の父」。シカゴ・マーカンタイル取引所の元会長。', '名誉会長', 2020),
  P('donohue', 'クレイグ・ドナヒュー', 'Craig Donohue', 1989, '2004〜2012年にCEO。', '元CEO', 2012),
  P('duffy', 'テレンス・ダフィー', 'Terrence Duffy', 1981, '2012年からCEO兼会長。2027年3月にCEOを退く予定。', '会長兼CEO'),
  P('fitzpatrick', 'リン・フィッツパトリック', 'Lynne Fitzpatrick', 2016, 'CFO。2027年3月にCEOへ就任予定。', 'CFO(次期CEO)'),
  O('chicagoproduce', 'Chicago Butter and Egg Board', 1898, '1898年に設立された源流(1919年にCMEへ)。', '源流(1898年)'),
  O('cbot', 'シカゴ商品取引所(CBOT)', 2007, '2007年に約119億ドルで合併。', '合併(2007年)'),
  O('nymex', 'NYMEX', 2008, '2008年に約94億ドルで買収。', '買収(2008年)'),
  O('nex', 'NEX Markets', 2018, '2018年に約55億ドルで買収(BrokerTec、EBS)。', '買収(2018年)'),
 ] + holders([('Vanguard', '6.6', M), ('BlackRock', '6.6', M), ('State Street', '4.5', M)]),
 [('melamed', 'donohue', 'link', '育てる'), ('donohue', 'duffy', 'link', '後任', 2012), ('duffy', 'fitzpatrick', 'link', 'CEO交代(予定)', 2027), ('chicagoproduce', 'melamed', 'link', '源流'), ('co', 'cbot', 'owns'), ('co', 'nymex', 'owns'), ('co', 'nex', 'owns')],
 '1898年のシカゴの取引所を源流とする、世界最大級のデリバティブ取引所。テレンス・ダフィーが2012年からCEOを務め、2027年3月にフィッツパトリックCFOが後任となる予定です。')

# ---------------- Snowflake ----------------
deep('SNOW', 'Snowflake', 2012, NOTE, [
  P('dageville', 'ブノワ・ダジュビル', 'Benoit Dageville', 2012, '共同創業者で社長。', '共同創業者 / 社長', None, 1),
  P('cruanes', 'ティエリー・クルアネス', 'Thierry Cruanes', 2012, '共同創業者でCTO。', '共同創業者 / CTO', None, 1),
  P('zukowski', 'マルチン・ズコフスキ', 'Marcin Zukowski', 2012, '共同創業者。', '共同創業者', 2019, 1),
  P('muglia', 'ボブ・ムグリア', 'Bob Muglia', 2014, '2014〜2019年にCEO。', '元CEO', 2019),
  P('slootman', 'フランク・スルートマン', 'Frank Slootman', 2019, '2019〜2024年にCEO。現在は会長。', '会長'),
  P('ramaswamy', 'スリダール・ラマスワミ', 'Sridhar Ramaswamy', 2023, '2024年2月からCEO。グーグルの元広告責任者で、検索のNeevaを創業。', 'CEO'),
  O('suttterhill', 'Sutter Hill Ventures', 2012, '創業期の出資者(マイク・スパイザー氏)。', '創業期の出資者', 'i'),
  O('berkshire', 'Berkshire Hathaway', 2020, '2020年のIPO時に出資。', 'IPO時の出資者', 'i'),
  O('salesforce', 'Salesforce', 2020, '2020年のIPO時に出資。', 'IPO時の出資者', 'i'),
  O('neeva', 'Neeva', 2023, '2023年に買収(検索)。', '買収(2023年)'),
  O('crunchy', 'Crunchy Data', 2025, '2025年に買収と報じられています。', '買収(2025年・報道)'),
  O('servicenow', 'ServiceNow', 2011, 'スルートマン氏の前職。', '前職'),
 ] + holders([('Capital Group', '4.5', M), ('Vanguard', '4.2', M)]),
 [('dageville', 'cruanes', 'link', '共同創業'), ('dageville', 'zukowski', 'link', '共同創業'), ('muglia', 'slootman', 'link', '後任', 2019), ('slootman', 'ramaswamy', 'link', '後任', 2024), ('slootman', 'servicenow', 'moved', '前職'), ('co', 'neeva', 'owns'), ('co', 'crunchy', 'owns')],
 '2012年にフランス出身のエンジニア2人らが創業したデータクラウドの会社。2020年に上場し、2024年からスリダール・ラマスワミがCEOを務めています。')
