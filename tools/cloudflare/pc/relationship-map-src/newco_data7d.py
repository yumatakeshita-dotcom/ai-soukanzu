from newco_data import mk, std, wp

# Meta・OpenAI・Anthropicなどの人物が、会社を離れて起こした会社(生き別れ・独立)の図。
# 事実は、英語版Wikipedia(2026年11月に取得)と、各項目に付けた出典に基づく。確認できなかったこと(出資者、金額など)は、書かずに「確認できていません」とする。
CO7D = {}
WP = lambda t, label=None: ['出典: Wikipedia(%s)' % (label or t.replace('_', ' ')), 'https://en.wikipedia.org/wiki/' + t]


def E_(*lines):
    return ''.join(lines)


STD = lambda c: std(c)

# ---------------- Artifact ----------------
N = [
 {'id': 'artifact', 'name': 'Artifact', 'kind': 'c', 'from': 2022, 'desc': '運営会社はNokto, Inc.(2022年3月3日にカリフォルニアで設立)。2023年1月31日に、シストロムとクリーガーが公開した、AIが記事を薦めるニュースアプリ(公開時の社員は7人)。2024年1月に終了を発表し(「継続して投資するほど、市場機会は大きくない」)、2024年4月にYahooが買収を発表。技術は2024年6月のYahoo!ニュースのアプリに使われました。出資者と買収額は、確認できていません。'},
 {'id': 'systrom', 'name': 'ケビン・シストロム', 'kind': 'p', 'from': 2022, 'desc': 'Instagramの共同創業者。Artifactの共同創業者でCEO。', 'role': '共同創業者 / CEO', 'founder': 1},
 {'id': 'krieger', 'name': 'マイク・クリーガー', 'kind': 'p', 'from': 2022, 'to': 2024, 'desc': 'Instagramの共同創業者。Artifactの共同創業者でCTO。2024年5月にAnthropicのCPOに就任。', 'role': '共同創業者 / CTO', 'founder': 1},
 {'id': 'instagram', 'name': 'Instagram', 'kind': 'o', 'from': 2010, 'desc': '2人が2010年に創業し、2012年にFacebookへ売却、2018年に退任した会社。ダブルクリックで図を開きます。', 'role': '2人の前の会社'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2012, 'desc': 'Instagramの親会社。2人は、Metaとの対立の末に2018年に退任したと報じられています(英語版Wikipediaの記載)。', 'role': '退任前の親会社'},
 {'id': 'yahoo', 'name': 'Yahoo', 'kind': 'i', 'from': 2024, 'desc': '2024年4月2日にArtifactの買収を発表。Artifactの技術を、刷新したYahoo!ニュースのアプリ(2024年6月)に使いました。', 'role': '買収(2024年4月)'},
 {'id': 'rtlive', 'name': 'Rt.live', 'kind': 'o', 'from': 2020, 'desc': '2020年4月に、クリーガーがシストロムと公開した、米国各州の新型コロナの広がりを示すサイト。', 'role': '2人が作ったサイト(2020年)'},
 {'id': 'anthropic', 'name': 'Anthropic', 'kind': 'o', 'from': 2024, 'desc': 'クリーガーの移籍先。2024年5月にCPOに就任と発表され、2026年1月にAnthropic Labsに加わりました。', 'role': 'クリーガーの移籍先'},
 {'id': 'figma', 'name': 'Figma', 'kind': 'o', 'from': 2025, 'desc': 'クリーガーは2025年7月に取締役に就き、2026年4月に辞任しました(辞任は、競合する製品を出すという報道と結び付けて報じられています)。', 'role': 'クリーガーが取締役(2025年7月〜2026年4月)'},
]
E = (STD('artifact') +
 "E.push({a:'yahoo',b:'artifact',k:'owns',label:'2024年4月に買収を発表',since:2024});\n"
 "E.push({a:'systrom',b:'krieger',k:'link',label:'共同創業'});\n"
 "E.push({a:'systrom',b:'instagram',k:'from'});E.push({a:'krieger',b:'instagram',k:'from'});\n"
 "E.push({a:'systrom',b:'meta',k:'conflict',label:'2018年に退任(対立が報じられた)',since:2018});\n"
 "E.push({a:'krieger',b:'anthropic',k:'moved'});\nE.push({a:'krieger',b:'figma',k:'link',label:'取締役(2025〜2026年)',since:2025});\n"
 "E.push({a:'systrom',b:'rtlive',k:'link',label:'公開(2020年)',since:2020});\n\n")
L = {'artifact': [WP('Artifact_(app)')], 'systrom': [WP('Kevin_Systrom')], 'krieger': [WP('Mike_Krieger'), ['出典: TechCrunch(2026年4月、Figma取締役の辞任)', 'https://techcrunch.com/']]}
L['krieger'] = [WP('Mike_Krieger')]
CO7D['artifact'] = mk(N, E, {'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger'}, {'systrom': 'kevin', 'krieger': 'mikeyk'}, {}, wp(('artifact', 'Artifact_(app)'), ('systrom', 'Kevin_Systrom'), ('krieger', 'Mike_Krieger'), ('yahoo', 'Yahoo!')),
 {'systrom': [['2010', 'Instagramを共同創業'], ['2012', 'Facebookが買収'], ['2014', 'Walmartの取締役(〜2018年)'], ['2018', '9月にInstagramを退任'], ['2020', 'Rt.liveを公開'], ['2023', '1月31日にArtifactを公開'], ['2024', '1月に終了を発表、4月にYahooが買収を発表']],
  'krieger': [['2010', 'Instagramを共同創業(CTO)'], ['2018', '9月に退任'], ['2023', 'Artifactを公開(CTO)'], ['2024', '5月にAnthropicのCPOに'], ['2025', '7月にFigmaの取締役に(2026年4月に辞任)'], ['2026', '1月にAnthropic Labsに加わる']]},
 L, 'artifact')

# ---------------- WhatsApp ----------------
N = [
 {'id': 'whatsapp', 'name': 'WhatsApp', 'kind': 'c', 'from': 2009, 'desc': 'ジャン・クームが2009年2月24日にカリフォルニアで法人化したメッセージアプリ(同年5月にApp Storeで公開)。2014年2月19日にFacebookが買収を発表(報道では約190億ドル。現金40億ドル、株式120億ドル、従業員向けの制限付き株式30億ドル)。'},
 {'id': 'koum', 'name': 'ジャン・クーム', 'kind': 'p', 'from': 2009, 'to': 2018, 'desc': '共同創業者でCEO。2018年4月に退任を発表。Facebookとの間で、プライバシー、広告、収益化をめぐる衝突があったと報じられています。', 'role': '共同創業者 / 元CEO', 'founder': 1},
 {'id': 'acton', 'name': 'ブライアン・アクトン', 'kind': 'p', 'from': 2009, 'to': 2017, 'desc': '共同創業者。2009年11月に正式に参加。2017年9月に退社し、のちSignal Foundationを共同で設立しました。', 'role': '共同創業者(2017年に退社)', 'founder': 1},
 {'id': 'daniels', 'name': 'クリス・ダニエルズ', 'kind': 'p', 'from': 2018, 'desc': 'クームの退任後の後任として、Facebookが指名しました。', 'role': 'WhatsApp責任者(クームの後任)'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'i', 'from': 2014, 'desc': '2014年にFacebook社として買収。', 'role': '親会社(2014年〜)'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2011, 'desc': '2011年4月に出資(金額は、資料により700万ドルと約800万ドルで食い違っています)。', 'role': '出資者(2011年)'},
 {'id': 'yahoo', 'name': 'Yahoo', 'kind': 'o', 'from': 2009, 'desc': '創業者の2人の元の勤め先。アクトンは、元同僚5人から25万ドルのシード資金を得て参加しました。', 'role': '創業者の出身元'},
 {'id': 'signal', 'name': 'Signal Foundation', 'kind': 'o', 'from': 2018, 'desc': 'アクトンが、マーリンスパイクとともに2018年に設立した非営利団体。ダブルクリックで図を開きます。', 'role': 'アクトンが設立'},
]
E = (STD('whatsapp') +
 "E.push({a:'koum',b:'acton',k:'link',label:'共同創業'});\n"
 "E.push({a:'meta',b:'whatsapp',k:'owns',label:'2014年に買収(約190億ドル)',since:2014});\n"
 "E.push({a:'koum',b:'yahoo',k:'from'});E.push({a:'acton',b:'yahoo',k:'from'});\n"
 "E.push({a:'acton',b:'signal',k:'moved'});\n"
 "E.push({a:'koum',b:'meta',k:'conflict',label:'プライバシー・広告・収益化をめぐり衝突(報道)',since:2018});\n"
 "E.push({a:'daniels',b:'koum',k:'link',label:'後任',since:2018});\n\n")
CO7D['whatsapp'] = mk(N, E, {'koum': 'Jan Koum', 'acton': 'Brian Acton', 'daniels': 'Chris Daniels'}, {'acton': 'brianacton', 'koum': 'jankoum'}, {'whatsapp': 'https://www.whatsapp.com'},
 wp(('whatsapp', 'WhatsApp'), ('koum', 'Jan_Koum'), ('acton', 'Brian_Acton'), ('meta', 'Meta_Platforms'), ('signal', 'Signal_Foundation')),
 {'koum': [['2009', 'WhatsApp Inc.を法人化(2月24日)'], ['2014', '2月にFacebookが買収を発表'], ['2018', '4月に退任を発表']],
  'acton': [['2009', '11月に共同創業者として正式に参加'], ['2017', '9月に退社'], ['2018', 'Signal Foundationを共同で設立']]},
 {'whatsapp': [WP('WhatsApp')], 'koum': [WP('Jan_Koum'), WP('WhatsApp', 'WhatsApp、2018年の退任')], 'acton': [WP('Brian_Acton')], 'signal': [WP('Signal_Foundation')]}, 'whatsapp')

# ---------------- Signal Foundation ----------------
N = [
 {'id': 'signal', 'name': 'Signal Foundation', 'kind': 'c', 'from': 2018, 'desc': '2018年に、モクシー・マーリンスパイクとブライアン・アクトンが設立した米国の非営利団体(設立の発表は2018年2月21日。資料により設立日は1月10日とも)。「オープンソースのプライバシー技術で、自由な表現と安全な世界規模の通信を守る」ことを目的に、Signalアプリを運営する子会社Signal Messenger LLCを持ちます。'},
 {'id': 'acton', 'name': 'ブライアン・アクトン', 'kind': 'p', 'from': 2018, 'desc': 'WhatsAppの共同創業者。財団の会長(Executive Chairman)で、子会社Signal MessengerのCEO。最初に5,000万ドルを貸し付け、2018年末には約1億500万ドルになりました(無担保・無利子、返済期限は2068年)。', 'role': '会長 / 共同創業者', 'founder': 1},
 {'id': 'marlinspike', 'name': 'モクシー・マーリンスパイク', 'kind': 'p', 'from': 2018, 'to': 2022, 'desc': '共同創設者。Signal Messengerの初代CEOで、2022年1月まで務めました。', 'role': '共同創設者 / 元CEO', 'founder': 1},
 {'id': 'whittaker', 'name': 'メレディス・ウィテカー', 'kind': 'p', 'from': 2022, 'desc': '2022年9月に新設された、財団の「理事長(President)」。', 'role': '理事長'},
 {'id': 'whatsapp', 'name': 'WhatsApp', 'kind': 'o', 'from': 2009, 'desc': 'アクトンが共同創業し、2017年に離れた会社(Metaの傘下)。ダブルクリックで図を開きます。', 'role': 'アクトンの前の会社'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2014, 'desc': 'WhatsAppの親会社。アクトンは2017年9月に、Facebook(当時)を離れました。', 'role': 'アクトンの前の勤め先'},
]
E = (STD('signal') + "E.push({a:'acton',b:'whatsapp',k:'from'});\nE.push({a:'acton',b:'marlinspike',k:'link',label:'共同設立'});\nE.push({a:'meta',b:'whatsapp',k:'owns'});\n\n")
CO7D['signal'] = mk(N, E, {'acton': 'Brian Acton', 'marlinspike': 'Moxie Marlinspike', 'whittaker': 'Meredith Whittaker'}, {}, {'signal': 'https://signal.org'},
 wp(('signal', 'Signal_Foundation'), ('acton', 'Brian_Acton'), ('marlinspike', 'Moxie_Marlinspike'), ('whittaker', 'Meredith_Whittaker')),
 {'acton': [['2009', 'WhatsAppの共同創業者に'], ['2017', '9月にFacebookを離れる'], ['2018', 'Signal Foundationを設立、5,000万ドルを貸し付け']]},
 {'signal': [WP('Signal_Foundation')], 'acton': [WP('Brian_Acton')], 'marlinspike': [WP('Moxie_Marlinspike')], 'whittaker': [WP('Meredith_Whittaker')]}, 'signal')

# ---------------- Oculus ----------------
N = [
 {'id': 'oculus', 'name': 'Oculus VR', 'kind': 'c', 'from': 2012, 'desc': 'パルマー・ラッキーが2012年4月に、Oculus Riftの資金募集(Kickstarter、約240万ドル)のために設立したVRの会社。2014年3月にFacebookが約20億ドルで買収(ザッカーバーグは裁判で30億ドルと証言し、金額は食い違っています)。'},
 {'id': 'luckey', 'name': 'パルマー・ラッキー', 'kind': 'p', 'from': 2012, 'to': 2017, 'desc': '創業者。2017年3月にFacebookを離れ、同年6月にAnduril Industriesを共同創業しました。退社の理由は当時公表されず、2016年の政治団体への寄付が理由と報じられています(Facebookは「政治的な考えが理由ではない」と否定)。', 'role': '創業者(2017年に退社)', 'founder': 1},
 {'id': 'iribe', 'name': 'ブレンダン・イリベ', 'kind': 'p', 'from': 2012, 'desc': '2012年8月に、Oculusの最初のCEOとして迎えられました。', 'role': 'CEO(2012年8月〜)'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'i', 'from': 2014, 'desc': '2014年3月にFacebook社として買収。', 'role': '親会社(2014年〜)'},
 {'id': 'zuckerberg', 'name': 'マーク・ザッカーバーグ', 'kind': 'p', 'from': 2014, 'desc': '買収を主導。2018年のWall Street Journalの報道は、ザッカーバーグら経営陣が、ラッキーに圧力をかけたと伝えました(Facebookは否定)。', 'role': '買収元(Meta CEO)'},
 {'id': 'anduril', 'name': 'Anduril Industries', 'kind': 'o', 'from': 2017, 'desc': 'ラッキーが2017年6月に、元Palantirの幹部3人(マット・グリム、トレー・スティーブンス、ブライアン・シュルフ)とOculusの元ハード責任者ジョセフ・チェンと共同創業した防衛技術の会社。', 'role': 'ラッキーの次の会社'},
]
E = (STD('oculus') + "E.push({a:'meta',b:'oculus',k:'owns',label:'2014年に買収(約20億ドル)',since:2014});\nE.push({a:'luckey',b:'anduril',k:'moved'});\n"
 "E.push({a:'luckey',b:'meta',k:'conflict',label:'2017年3月に退社(経緯をめぐり報道)',since:2017});\nE.push({a:'luckey',b:'iribe',k:'link',label:'CEOに迎えた'});\n\n")
CO7D['oculus'] = mk(N, E, {'luckey': 'Palmer Luckey', 'iribe': 'Brendan Iribe', 'zuckerberg': 'Mark Zuckerberg'}, {'luckey': 'PalmerLuckey', 'zuckerberg': 'zuck'}, {},
 wp(('oculus', 'Oculus_VR'), ('luckey', 'Palmer_Luckey'), ('iribe', 'Brendan_Iribe'), ('anduril', 'Anduril_Industries'), ('zuckerberg', 'Mark_Zuckerberg')),
 {'luckey': [['2012', '4月にOculus VRを設立'], ['2014', '3月にFacebookが買収'], ['2017', '3月にFacebookを離れ、6月にAndurilを共同創業']]},
 {'oculus': [WP('Oculus_VR')], 'luckey': [WP('Palmer_Luckey')], 'iribe': [WP('Brendan_Iribe')], 'anduril': [WP('Anduril_Industries')], 'zuckerberg': [WP('Palmer_Luckey', 'Palmer Luckey、退社の経緯')]}, 'oculus')

# ---------------- AMI Labs ----------------
N = [
 {'id': 'amilabs', 'name': 'AMI Labs', 'kind': 'c', 'from': 2025, 'desc': 'Advanced Machine Intelligence。ヤン・ルカンがMetaを離れて起こした会社(退社を2025年11月19日に確認、共同創業は2025年12月とされます)。文章の予測ではなく、物理世界の構造や動きを学ぶ「世界モデル」のAIを作ります。2026年3月に10.3億ドルを調達(調達前評価額35億ドル)と発表。所在地は確認できていません。'},
 {'id': 'lecun', 'name': 'ヤン・ルカン', 'kind': 'p', 'from': 2025, 'desc': 'Metaに10年在籍し、FAIRを創設。AMI Labsの共同創業者でExecutive Chair。チューリング賞受賞者。', 'role': 'Executive Chair / 共同創業者', 'founder': 1},
 {'id': 'lebrun', 'name': 'アレックス・ルブラン', 'kind': 'p', 'from': 2025, 'desc': 'AMI LabsのCEO。', 'role': 'CEO'},
 {'id': 'cathay', 'name': 'Cathay Innovation', 'kind': 'i', 'from': 2026, 'desc': '2026年3月の調達の共同主導に含まれる出資者の一社(主導した会社と参加しただけの会社の区別は、確認できていません)。', 'role': '出資者(2026年3月)'},
 {'id': 'greycroft', 'name': 'Greycroft', 'kind': 'i', 'from': 2026, 'desc': '同上。', 'role': '出資者(2026年3月)'},
 {'id': 'hiro', 'name': 'Hiro Capital', 'kind': 'i', 'from': 2026, 'desc': '同上。', 'role': '出資者(2026年3月)'},
 {'id': 'hv', 'name': 'HV Capital', 'kind': 'i', 'from': 2026, 'desc': '同上。', 'role': '出資者(2026年3月)'},
 {'id': 'bezos', 'name': 'Bezos Expeditions', 'kind': 'i', 'from': 2026, 'desc': 'ジェフ・ベゾスの投資会社。同上。', 'role': '出資者(2026年3月)'},
 {'id': 'meta', 'name': 'Meta', 'kind': 'o', 'from': 2015, 'desc': 'ルカンの前の勤め先。2013年にFAIRを創設。2025年11月に退社。', 'role': 'ルカンの前の勤め先'},
]
E = (STD('amilabs') + "E.push({a:'lecun',b:'meta',k:'from'});\nE.push({a:'lecun',b:'lebrun',k:'link',label:'会長とCEO'});\n\n")
CO7D['amilabs'] = mk(N, E, {'lecun': 'Yann LeCun', 'lebrun': 'Alex LeBrun'}, {'lecun': 'ylecun'}, {}, wp(('amilabs', 'Yann_LeCun'), ('lecun', 'Yann_LeCun'), ('meta', 'Meta_Platforms')),
 {'lecun': [['2013', 'MetaのFAIRを創設'], ['2018', 'チューリング賞を受賞'], ['2025', '11月に退社を確認、12月にAMI Labsを共同創業'], ['2026', '3月に10.3億ドルを調達']]},
 {'amilabs': [WP('Yann_LeCun', 'Yann LeCun、AMI Labs')], 'lecun': [WP('Yann_LeCun')]}, 'amilabs')

# ---------------- Eureka Labs ----------------
N = [
 {'id': 'eureka', 'name': 'Eureka Labs', 'kind': 'c', 'from': 2024, 'desc': 'アンドレイ・カルパシーが、2024年7月16日にXで発表した「AI+教育」の会社。最初の製品は、AIの講座「LLM101n」。出資者と調達額は、確認できていません。'},
 {'id': 'karpathy', 'name': 'アンドレイ・カルパシー', 'kind': 'p', 'from': 2024, 'desc': 'OpenAIの創業メンバー(2015〜2017年)。2017年6月にTeslaのAI責任者になり、2022年7月に退社を発表。2023年2月9日にOpenAIへ戻り、2024年2月13日に退社が確認されました。', 'role': '創業者', 'founder': 1},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2015, 'desc': 'カルパシーの前の勤め先(2015〜2017年、2023〜2024年)。', 'role': '前の勤め先'},
 {'id': 'tesla', 'name': 'Tesla', 'kind': 'o', 'from': 2017, 'desc': 'カルパシーが、2017年6月から2022年7月までAI責任者を務めた会社(イーロン・マスクの直属)。', 'role': '前の勤め先'},
]
E = (STD('eureka') + "E.push({a:'karpathy',b:'openai',k:'from'});\nE.push({a:'karpathy',b:'tesla',k:'from'});\n\n")
CO7D['eureka'] = mk(N, E, {'karpathy': 'Andrej Karpathy'}, {'karpathy': 'karpathy'}, {}, wp(('eureka', 'Andrej_Karpathy'), ('karpathy', 'Andrej_Karpathy'), ('openai', 'OpenAI'), ('tesla', 'Tesla,_Inc.')),
 {'karpathy': [['2015', 'OpenAIの創業メンバー'], ['2017', '6月にTeslaのAI責任者に'], ['2023', '2月にOpenAIへ戻る'], ['2024', '2月にOpenAIを退社、7月にEureka Labsを発表']]},
 {'eureka': [WP('Andrej_Karpathy', 'Andrej Karpathy、Eureka Labs')], 'karpathy': [WP('Andrej_Karpathy')]}, 'eureka')
