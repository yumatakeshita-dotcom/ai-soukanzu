from newco_data import mk, std, wp

CO6 = {}

N = [
 {'id': 'mercari', 'name': 'Mercari', 'kind': 'c', 'from': 2013, 'desc': '2013年に設立されたフリマアプリの会社。2018年に東証マザーズに上場し、2023年に指名委員会等設置会社へ移行しました。創業者の山田進太郎の持株比率は約21.5%(2025年12月期)。米国事業は2026年6月期に黒字転換と報じられています。'},
 {'id': 'yamada', 'name': '山田進太郎', 'kind': 'p', 'from': 2013, 'desc': '創業者で代表執行役CEO。持株比率は約21.5%で筆頭株主(2025年12月期)。2018年6月期は約27.5%でした。', 'role': '創業者 / 代表執行役CEO', 'founder': 1},
 {'id': 'koizumi', 'name': '小泉文明', 'kind': 'p', 'from': 2014, 'desc': '代表執行役。創業初期に参画した幹部で、長く社長兼COOとして山田氏を支えました。', 'role': '代表執行役'},
 {'id': 'kimura', 'name': '木村俊也', 'kind': 'p', 'from': 2016, 'desc': 'CTO。2026年6月1日から、CHRO(最高人事責任者)とCAIO(最高AI責任者)も兼ねると報じられています。', 'role': 'CTO / CHRO / CAIO'},
 {'id': 'aoyagi', 'name': '青柳直樹', 'kind': 'p', 'from': 2016, 'to': 2024, 'desc': '元メルペイの経営者。2024年1月にnewmoを設立しました。', 'role': '元メルペイ経営者'},
 {'id': 'hanazawa', 'name': '花沢菊香', 'kind': 'p', 'from': 2024, 'desc': '社外取締役(2024年6月期に就任)。', 'role': '社外取締役'},
 {'id': 'lagerling', 'name': 'ジョン・ラガリング', 'kind': 'p', 'from': 2017, 'desc': '2017年に、Facebookの経営チームから、米国戦略を率いるために迎えられたと報じられました(現在の役職は確認できていません)。', 'role': '米国戦略(2017年)'},
 {'id': 'suadd', 'name': 'suadd', 'kind': 'i', 'from': 2018, 'desc': '約6.3%を持つ株主(2025年12月期)。2018年6月期にも約4.9%を持つ大株主でした。', 'role': '大株主'},
 {'id': 'eastv', 'name': 'East Ventures', 'kind': 'i', 'from': 2018, 'desc': '2018年6月期の大株主に、イーストベンチャーズ投資事業有限責任組合が挙がっています。', 'role': '初期のVC'},
 {'id': 'globis', 'name': 'Globis Capital Partners', 'kind': 'i', 'from': 2018, 'desc': '2018年6月期の大株主に、グロービス4号ファンドが挙がっています。', 'role': '初期のVC'},
 {'id': 'merpay', 'name': 'メルペイ', 'kind': 'o', 'from': 2018, 'desc': 'スマホ決済・金融の子会社。青柳氏が経営者として率いました。', 'role': '子会社(決済・金融)'},
 {'id': 'melcoin', 'name': 'メルコイン', 'kind': 'o', 'from': 2022, 'desc': '暗号資産事業の子会社。2026年6月期の第3四半期の収益は約13.6億円で、前年同期とほぼ横ばいと報じられています。', 'role': '子会社(暗号資産)'},
 {'id': 'souzo', 'name': 'ソウゾウ', 'kind': 'o', 'from': 2021, 'desc': 'メルカリShopsを運営していた子会社。事業開発の機能を除く部門は、会社分割でメルカリが承継すると決定されました。', 'role': '子会社'},
 {'id': 'shops', 'name': 'メルカリShops', 'kind': 'o', 'from': 2021, 'desc': '2021年10月に開始した、事業者向け(BtoC)の出品の仕組み。', 'role': 'サービス'},
 {'id': 'mercariUS', 'name': 'Mercari US', 'kind': 'o', 'from': 2014, 'desc': '米国事業。2026年6月期に黒字転換と報じられています。2026年6月には、米国の買い手向けに日本のメルカリの専用アプリを始めたと報じられています。', 'role': '海外の事業'},
 {'id': 'mercariUK', 'name': 'Mercari Europe', 'kind': 'o', 'from': 2016, 'desc': '英国の子会社。事業として確立できず、清算を決めたと報じられています(古い情報)。', 'role': '清算した子会社'},
 {'id': 'merlogi', 'name': 'メルロジ', 'kind': 'o', 'from': 2020, 'desc': '物流の完全子会社。2023年1月1日にメルカリへ吸収合併されました。', 'role': '吸収合併した子会社'},
 {'id': 'michael', 'name': 'マイケル', 'kind': 'o', 'from': 2018, 'desc': '2018年10月にメルカリの完全子会社になった会社。', 'role': '子会社'},
 {'id': 'antlers', 'name': '鹿島アントラーズ', 'kind': 'o', 'from': 2019, 'desc': 'Jリーグの鹿島アントラーズ。メルカリが2019年に筆頭株主になった球団として知られます(連結に含まれると見られますが、持ち分は確認できていません)。', 'role': 'グループの球団'},
 {'id': 'newmo', 'name': 'newmo', 'kind': 'o', 'from': 2024, 'desc': '青柳氏が2024年に設立。メルカリは、2024年2月のシードに出資したと報じられています。', 'role': '出資先'},
]
E = (std('mercari') +
 "['merpay','melcoin','souzo','mercariUS','mercariUK','merlogi','michael','antlers'].forEach(b=>E.push({a:'mercari',b,k:'owns'}));\n"
 "E.push({a:'souzo',b:'shops',k:'link',label:'運営'});\nE.push({a:'merlogi',b:'mercari',k:'owns',label:'2023年に吸収合併',since:2023});\n"
 "E.push({a:'aoyagi',b:'merpay',k:'link',label:'率いた'});\nE.push({a:'aoyagi',b:'newmo',k:'moved'});\nE.push({a:'mercari',b:'newmo',k:'invest2',label:'シードに出資',since:2024});\n"
 "E.push({a:'koizumi',b:'yamada',k:'link',label:'経営を支える'});\n\n")
CO6['mercari'] = mk(N, E,
 {'yamada': 'Shintaro Yamada', 'koizumi': 'Fumiaki Koizumi', 'kimura': 'Shunya Kimura', 'aoyagi': 'Naoki Aoyagi', 'hanazawa': 'Kikuka Hanazawa', 'lagerling': 'John Lagerling'},
 {'mercari': 'mercari_app'}, {'mercari': 'https://about.mercari.com'},
 wp(('mercari', 'Mercari'), ('antlers', 'Kashima_Antlers')),
 {'yamada': [['2001', 'ウノウを設立(のちZyngaに売却)'], ['2013', 'メルカリを創業'], ['2018', '東証マザーズに上場'], ['2023', '指名委員会等設置会社へ移行']]}, {}, 'mercari')
