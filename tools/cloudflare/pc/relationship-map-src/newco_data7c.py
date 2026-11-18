from newco_data import mk, std, wp
from newco_data7 import eg

# Instagramの図(Metaの図で、関連組織「Instagram」をダブルクリックすると開く)
CO7C = {}
N = [
 {'id': 'instagram', 'name': 'Instagram', 'kind': 'c', 'from': 2010, 'desc': '写真・動画の共有SNS。2010年10月にケビン・シストロムとマイク・クリーガーが公開。2012年4月にFacebookが買収を発表し(報道では約10億ドル、現金と株式)、同年9月に完了しました。以後はMeta(旧Facebook)の傘下で、2018年に創業者2人が退任しました。FTC対Meta裁判(買収が競争を損なったかが争点)では、2025年11月に連邦地裁がMetaの勝訴と判断しました。'},
 {'id': 'systrom', 'name': 'ケビン・シストロム', 'kind': 'p', 'from': 2010, 'to': 2018, 'desc': '共同創業者でCEO。写真共有アプリ「Burbn」を作り直してInstagramにしました。2018年9月に退任を発表。のちクリーガーとニュースアプリ「Artifact」を作りました。退任の背景には、買収後のInstagramの人員・資源・独立性をめぐるザッカーバーグとの対立があったと報じられています(2025年のFTC裁判で本人が証言。Metaは否定)。', 'role': '共同創業者 / 元CEO', 'founder': 1},
 {'id': 'krieger', 'name': 'マイク・クリーガー', 'kind': 'p', 'from': 2010, 'to': 2018, 'desc': '共同創業者でCTO。2018年9月に退任。2024年にAnthropicのCPOとして入社し、のちAnthropic Labsを率いています。', 'role': '共同創業者 / 元CTO', 'founder': 1},
 {'id': 'mosseri', 'name': 'アダム・モセリ', 'kind': 'p', 'from': 2018, 'desc': '創業者2人の退任を受け、2018年10月にInstagramの責任者(Head of Instagram)に就任。2008年にFacebookへ入り、ニュースフィードの製品開発を率いた人物です。', 'role': 'Instagram責任者'},
 {'id': 'zuckerberg', 'name': 'マーク・ザッカーバーグ', 'kind': 'p', 'from': 2012, 'desc': 'Facebook(現Meta)の創業者でCEO。2012年にInstagramの買収を主導しました。', 'role': '買収元(Meta CEO)'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'i', 'from': 2012, 'desc': '親会社。2012年にFacebook社として買収し、2021年に社名をMetaに変更しました。', 'role': '親会社(2012年〜)'},
 {'id': 'baseline', 'name': 'Baseline Ventures', 'kind': 'i', 'from': 2010, 'desc': '2010年のシード(約50万ドル)の出資者として報じられています。', 'role': 'シード出資者'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2010, 'desc': '初期の出資者として報じられています(公式のポートフォリオにInstagramが載っています)。', 'role': '初期出資者'},
 {'id': 'benchmark', 'name': 'Benchmark', 'kind': 'i', 'from': 2011, 'desc': '2011年のシリーズA(約700万ドル)を主導したと報じられています。', 'role': 'シリーズA出資者'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2012, 'desc': '2012年4月の増資(約5,000万ドル、評価額約5億ドル)を主導したと報じられています(買収発表の直前)。', 'role': '2012年の増資の出資者'},
 {'id': 'greylock', 'name': 'Greylock', 'kind': 'i', 'from': 2012, 'desc': '2012年4月の増資の出資者として報じられています。', 'role': '2012年の増資の出資者'},
 {'id': 'thrive', 'name': 'Thrive Capital', 'kind': 'i', 'from': 2012, 'desc': '2012年4月の増資の出資者として報じられています。', 'role': '2012年の増資の出資者'},
 {'id': 'levine', 'name': 'マーン・レヴィン', 'kind': 'p', 'from': 2014, 'desc': 'Instagramの初代COO(2014年)。それ以前はFacebookのグローバル公共政策のVP(2010〜2014年)。2018年にFacebookへ戻り、2021年にチーフ・ビジネス・オフィサー、2023年2月に退任。', 'role': '初代COO(2014年〜)'},
 {'id': 'walmart', 'name': 'Walmart', 'kind': 'o', 'from': 2014, 'to': 2018, 'desc': 'シストロムが2014年から2018年まで、取締役を務めた会社(英語版Wikipediaの記載)。', 'role': 'シストロムが取締役(2014〜2018年)'},
 {'id': 'threads', 'name': 'Threads', 'kind': 'o', 'from': 2023, 'desc': '2023年7月に、Instagramのアカウントでつながる形で始まったテキスト中心のSNS(Meta)。', 'role': 'Instagramから生まれたサービス'},
 {'id': 'artifact', 'name': 'Artifact', 'kind': 'o', 'from': 2022, 'desc': 'シストロムとクリーガーが、Instagram退任後に作ったAIニュースアプリ(運営はNokto, Inc.、2022年3月設立、2023年1月31日公開)。2024年1月に終了を発表し、同年4月にYahooが買収を発表。ダブルクリックで図を開きます。', 'role': '創業者2人の次の会社'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2024, 'desc': 'クリーガーの移籍先(2024年にCPOとして入社)。', 'role': 'クリーガーの移籍先'},
]
E = (std('instagram') +
 "E.push({a:'meta',b:'instagram',k:'owns',label:'2012年に買収(約10億ドル)',since:2012});\n"
 "E.push({a:'zuckerberg',b:'instagram',k:'link',label:'買収を主導',since:2012});\n"
 "['baseline','a16z','benchmark','sequoia','greylock','thrive'].forEach(a=>E.push({a,b:'instagram',k:'invest2'}));\n"
 "E.push({a:'systrom',b:'krieger',k:'link',label:'共同創業'});\n"
 "E.push({a:'systrom',b:'zuckerberg',k:'conflict',label:'資源・独立性をめぐり対立(報道)',since:2017});\n"
 "E.push({a:'systrom',b:'artifact',k:'moved'});\nE.push({a:'krieger',b:'artifact',k:'moved'});\nE.push({a:'krieger',b:'anthropic',k:'moved'});\n"
 "E.push({a:'systrom',b:'mosseri',k:'link',label:'2018年に後任',since:2018});\n"
 "E.push({a:'systrom',b:'walmart',k:'link',label:'取締役(2014〜2018年)',since:2014});\n"
 "E.push({a:'instagram',b:'threads',k:'owns',label:'2023年に派生',since:2023});\n\n")
TC = ['出典: TechCrunch(2012年の増資)', 'https://techcrunch.com/2012/04/09/right-before-acquisition-instagram-closed-50m-at-a-500m-valuation-from-sequoia-thrive-greylock-and-benchmark']
WPI = ['出典: Wikipedia(Instagram)', 'https://en.wikipedia.org/wiki/Instagram']
TESTIMONY = [['出典: Engadget(2025年のFTC裁判での証言)', 'https://www.engadget.com/social-media/instagrams-former-ceo-testifies-zuckerberg-thought-the-app-was-a-threat-to-facebook-202112282.html'],
             ['出典: Irish Times(資源を絞ったという証言)', 'https://www.irishtimes.com/business/2025/04/23/instagrams-co-founder-testifies-metas-mark-zuckerberg-withheld-resources'],
             ['出典: Bloomberg Tax(成長を脅威とみていたという証言)', 'https://news.bloombergtax.com/ip-law/instagrams-systrom-claims-app-could-have-thrived-without-meta'],
             ['出典: SiliconANGLE(証言の報道)', 'https://siliconangle.com/2025/04/22/instagram-co-founder-supports-ftcs-case-landmark-meta-monopoly-trial']]
RULING = [['出典: TheWrap(2025年11月、Metaの勝訴)', 'https://www.thewrap.com/meta-wins-ftc-antitrust-case-whatsapp-instagram/'],
          ['出典: Broadband Breakfast(同上)', 'https://broadbandbreakfast.com/meta-prevails-in-historic-ftc-antitrust-case-wont-have-to-break-off-whatsapp-instagram/']]
LINKS = {
    'instagram': [WPI, ['出典: Fortune(2012年4月の買収報道)', 'https://fortune.com/2012/04/09/breaking-facebook-buying-instagram-for-1-billion/'], TC] + RULING,
    'systrom': [WPI] + TESTIMONY,
    'krieger': [WPI],
    'mosseri': [WPI],
    'levine': [['出典: Wikipedia(Marne Levine)', 'https://en.wikipedia.org/wiki/Marne_Levine'], ['公式Instagram', 'https://www.instagram.com/marnelevine/']],
    'zuckerberg': TESTIMONY + RULING,
    'meta': [['出典: Fortune(2012年4月の買収報道)', 'https://fortune.com/2012/04/09/breaking-facebook-buying-instagram-for-1-billion/']],
    'baseline': [WPI],
    'a16z': [WPI, ['出典: a16z公式のポートフォリオ', 'https://a16z.com/portfolio/']],
    'benchmark': [WPI, TC],
    'sequoia': [TC],
    'greylock': [TC],
    'thrive': [WPI, TC],
    'threads': [['出典: Wikipedia(Threads)', 'https://en.wikipedia.org/wiki/Threads_(social_network)']],
    'artifact': [['出典: Wikipedia(Artifact)', 'https://en.wikipedia.org/wiki/Artifact_(app)']],
    'walmart': [['出典: Wikipedia(Kevin Systrom)', 'https://en.wikipedia.org/wiki/Kevin_Systrom']],
    'anthropic': [['出典: Anthropic公式(Mike Kriegerの入社)', 'https://www.anthropic.com/news/mike-krieger-joins-anthropic']],
}
CO7C['instagram'] = mk(N, E,
 {'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger', 'mosseri': 'Adam Mosseri', 'zuckerberg': 'Mark Zuckerberg', 'levine': 'Marne Levine'},
 {'systrom': 'kevin', 'krieger': 'mikeyk', 'mosseri': 'mosseri', 'zuckerberg': 'zuck', 'instagram': 'instagram'},
 {'instagram': 'https://www.instagram.com'},
 wp(('instagram', 'Instagram'), ('systrom', 'Kevin_Systrom'), ('krieger', 'Mike_Krieger'), ('mosseri', 'Adam_Mosseri'), ('zuckerberg', 'Mark_Zuckerberg'), ('meta', 'Meta_Platforms'), ('threads', 'Threads_(social_network)'), ('artifact', 'Artifact_(app)')),
 {'systrom': [['2006', 'スタンフォード大学を卒業(経営科学・工学)'], ['〜', 'Googleでプロダクトマーケティングを約2年(Gmailなど)'], ['2010', 'BaselineとAndreessen Horowitzから50万ドルを得て、Instagramを共同創業(CEO)'], ['2012', '4月にFacebookが約10億ドルで買収'], ['2014', 'Walmartの取締役に(〜2018年)'], ['2018', '9月24日に退任を発表'], ['2020', 'Rt.liveを共同で公開'], ['2023', '1月31日にArtifactを公開'], ['2024', '1月に終了を発表、4月2日にYahooが買収を発表'], ['2025', '9月、Instagramの利用者が30億人に(本人は退任済み)']],
  'krieger': [['2010', 'Instagramを共同創業(CTO)'], ['2018', '9月に退任'], ['2020', 'Rt.liveをシストロムと公開'], ['2023', 'Artifactを公開(CTO)'], ['2024', '5月にAnthropicのCPOに'], ['2025', '7月にFigmaの取締役に(2026年4月に辞任)'], ['2026', '1月にAnthropic Labsに加わる']],
  'mosseri': [['2008', 'Facebookに入社'], ['2018', '10月にInstagram責任者に就任']]},
 LINKS, 'instagram')
