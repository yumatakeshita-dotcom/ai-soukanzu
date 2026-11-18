import json, sys
sys.path.insert(0, r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src')
S =r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
O = r'C:\Users\yumat\.claude\output'
dump = lambda o: json.dumps(o, ensure_ascii=False)

def block(path):
    h = open(path, encoding='utf-8').read()
    d = h[h.index('const N = ['):h.index('const byId')]
    return '\n'.join(l for l in d.split('\n') if not l.startswith('const li=') and not l.startswith('const xs='))

def gen(N, edges, PH, WIKI, EN, X, WEB, CAREER, LINKS):
    return ("const N = %s;\nconst PH=%s;\nconst WIKI=%s;\nconst EN=%s;\nconst X=%s;\nconst WEB=%s;\nconst CAREER=%s;\nconst LINKS=%s;\n"
            % tuple(dump(o) for o in (N, PH, WIKI, EN, X, WEB, CAREER, LINKS))) + edges

def fn(name, center, body):
    return '%s:()=>{\n%s\nreturn {N,PH,WIKI,EN,X,WEB,CAREER,LINKS,E,center:"%s"};\n}' % (name, body, center)

xm = json.load(open(S + r'\xm.json'))
ph = lambda ks: {k: xm[k]['img'] for k in ks if xm.get(k, {}).get('img')}
wk = lambda ks: {k: xm[k]['wiki'] for k in ks if xm.get(k, {}).get('wiki')}

# ---------------- xAI ----------------
xN = [
 {'id': 'xai', 'name': 'xAI', 'kind': 'c', 'from': 2023, 'desc': '2023年7月にマスクが設立したAI企業。Grokを開発。2025年3月にX(旧Twitter)を統合し、2026年2月にSpaceXが全株式交換(評価額約2,500億ドル)で買収したと報じられています。'},
 {'id': 'musk', 'name': 'イーロン・マスク', 'kind': 'p', 'from': 2023, 'desc': 'xAIの創業者。SpaceXとTeslaのCEOでもあります。OpenAIの共同創業者でしたが、2018年に退任し、のちに営利化をめぐって提訴しました。', 'role': '創業者', 'founder': 1},
 {'id': 'babuschkin', 'name': 'イーゴリ・バブシュキン', 'kind': 'p', 'from': 2023, 'to': 2025, 'desc': '共同創業者。2025年8月に退社し、自身のベンチャーキャピタルを立ち上げたと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'kosic', 'name': 'カイル・コシック', 'kind': 'p', 'from': 2023, 'to': 2024, 'desc': '共同創業者。2024年半ばに退社し、OpenAIへ移ったと報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'szegedy', 'name': 'クリスチャン・セゲディ', 'kind': 'p', 'from': 2023, 'to': 2025, 'desc': '共同創業者。画像認識(Inception)やAdversarial Examplesの研究で知られます。2025年2月に退社。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'yang', 'name': 'グレッグ・ヤン', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者。2026年1月に健康上の理由で退社と報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'ba', 'name': 'ジミー・バー', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者。トロント大学の研究者でもあります。SpaceXとの統合後の2026年2月に退社と報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'wu', 'name': 'トニー・ウー', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者(ユーフアイ・ウー)。数学・推論の研究を担当。2026年2月に退社と報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'pohlen', 'name': 'トビー・ポーレン', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者。2026年2月27日に退社と報じられています。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'kroiss', 'name': 'マヌエル・クロイス', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者。2026年3月下旬に退社と報じられています(報道により食い違いあり)。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'nordeen', 'name': 'ロス・ノルディーン', 'kind': 'p', 'from': 2023, 'to': 2026, 'desc': '共同創業者。2026年3月下旬に退社と報じられています(報道により食い違いあり)。', 'role': '元共同創業者', 'founder': 1},
 {'id': 'zhang', 'name': 'グオドン・ジャン', 'kind': 'p', 'from': 2023, 'desc': '共同創業者の一人。2026年2月時点の報道では在籍とされていますが、その後の状況は確認できていません。', 'role': '共同創業者', 'founder': 1},
 {'id': 'dai', 'name': 'ジハン・ダイ', 'kind': 'p', 'from': 2023, 'desc': '共同創業者の一人。2026年2月時点の報道では在籍とされていますが、その後の状況は確認できていません。', 'role': '共同創業者', 'founder': 1},
 {'id': 'yaccarino', 'name': 'リンダ・ヤッカリーノ', 'kind': 'p', 'from': 2023, 'to': 2025, 'desc': 'X(旧Twitter)の元CEO。2025年7月に退任し、後任は置かれていないと報じられています。', 'role': '元X CEO'},
 {'id': 'valor', 'name': 'Valor Equity Partners', 'kind': 'i', 'from': 2024, 'desc': 'xAIの主要な出資者の一社。マスクの会社への出資で知られます。', 'role': '投資会社'},
 {'id': 'a16z', 'name': 'Andreessen Horowitz', 'kind': 'i', 'from': 2024, 'desc': '2024年の資金調達に参加したと報じられています。', 'role': 'VC'},
 {'id': 'sequoia', 'name': 'Sequoia Capital', 'kind': 'i', 'from': 2024, 'desc': '2024年の資金調達に参加したと報じられています。', 'role': 'VC'},
 {'id': 'fidelity', 'name': 'Fidelity', 'kind': 'i', 'from': 2024, 'desc': '2024年以降の資金調達に参加したと報じられています。', 'role': '資産運用会社'},
 {'id': 'qia', 'name': 'Qatar Investment Authority', 'kind': 'i', 'from': 2024, 'desc': 'カタールの政府系ファンド。xAIの資金調達に参加したと報じられています。', 'role': '政府系ファンド'},
 {'id': 'nvidia', 'name': 'Nvidia', 'kind': 'i', 'from': 2024, 'desc': 'GPU供給元であり出資者。2025年のシリーズE(約200億ドル)にも参加と報じられています。', 'role': '出資 + GPU供給'},
 {'id': 'cisco', 'name': 'Cisco', 'kind': 'i', 'from': 2025, 'desc': '2025年のシリーズEに戦略出資者として参加と報じられています。', 'role': '戦略出資者'},
 {'id': 'humain', 'name': 'Humain', 'kind': 'i', 'from': 2026, 'desc': 'サウジアラビアのAI企業。シリーズEに30億ドルを出資し、有力な少数株主になったと発表しました。', 'role': '30億ドル出資'},
 {'id': 'mgx', 'name': 'MGX', 'kind': 'i', 'from': 2026, 'desc': 'アブダビの投資会社。シリーズEの参加者として挙げる報道があります。', 'role': 'ファンド'},
 {'id': 'spacex', 'name': 'SpaceX', 'kind': 'o', 'from': 2026, 'desc': 'マスクが率いる宇宙企業。2026年2月にxAIを全株式交換で買収し、xAIは完全子会社になりました。', 'role': '親会社'},
 {'id': 'x', 'name': 'X(旧Twitter)', 'kind': 'o', 'from': 2025, 'desc': 'マスクが2022年に買収したSNS。2025年3月にxAIと統合されたと報じられています。', 'role': 'xAIが統合'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2023, 'desc': 'マスクが共同創業し、2018年に退いた会社。2024年にマスクが提訴。共同創業者のコシックの移籍先でもあります。', 'role': '対立・移籍先'},
 {'id': 'babuschkinv', 'name': 'Babuschkin Ventures', 'kind': 'o', 'from': 2025, 'desc': 'バブシュキンが退社後に立ち上げたベンチャーキャピタルと報じられています。', 'role': 'バブシュキンが設立'},
]
xE = ("const E = [];\n"
 "N.forEach(n=>{\n  if(n.kind==='p') E.push({a:n.id,b:'xai',k:'member'});\n  if(n.kind==='i') E.push({a:n.id,b:'xai',k:'invest'});\n});\n"
 "E.push({a:'spacex',b:'xai',k:'owns',label:'2026年2月に買収'});\n"
 "E.push({a:'xai',b:'x',k:'owns',label:'2025年3月に統合'});\n"
 "E.push({a:'musk',b:'spacex',k:'link'});\n"
 "E.push({a:'musk',b:'openai',k:'conflict',label:'提訴',since:2024});\n"
 "E.push({a:'kosic',b:'openai',k:'moved'});\n"
 "E.push({a:'babuschkin',b:'babuschkinv',k:'moved'});\n"
 "E.push({a:'yaccarino',b:'x',k:'link'});\n\n")
xEN = {'musk': 'Elon Musk', 'babuschkin': 'Igor Babuschkin', 'kosic': 'Kyle Kosic', 'szegedy': 'Christian Szegedy', 'yang': 'Greg Yang', 'ba': 'Jimmy Ba',
       'wu': 'Yuhuai (Tony) Wu', 'pohlen': 'Toby Pohlen', 'kroiss': 'Manuel Kroiss', 'nordeen': 'Ross Nordeen', 'zhang': 'Guodong Zhang', 'dai': 'Zihang Dai', 'yaccarino': 'Linda Yaccarino'}
xX = {'musk': 'elonmusk', 'babuschkin': 'ibab', 'szegedy': 'ChrSzegedy', 'yang': 'TheGregYang', 'ba': 'jimmybajimmyba', 'wu': 'Yuhu_ai_', 'yaccarino': 'lindayacc', 'xai': 'xai', 'nvidia': 'nvidia', 'openai': 'OpenAI'}
xW = wk(['musk', 'yaccarino'])
xW.update({'xai': 'https://en.wikipedia.org/wiki/XAI_(company)', 'spacex': 'https://en.wikipedia.org/wiki/SpaceX', 'x': 'https://en.wikipedia.org/wiki/Twitter',
           'openai': 'https://en.wikipedia.org/wiki/OpenAI', 'nvidia': 'https://en.wikipedia.org/wiki/Nvidia', 'cisco': 'https://en.wikipedia.org/wiki/Cisco',
           'a16z': 'https://en.wikipedia.org/wiki/Andreessen_Horowitz', 'sequoia': 'https://en.wikipedia.org/wiki/Sequoia_Capital', 'valor': 'https://en.wikipedia.org/wiki/Valor_Equity_Partners',
           'qia': 'https://en.wikipedia.org/wiki/Qatar_Investment_Authority', 'fidelity': 'https://en.wikipedia.org/wiki/Fidelity_Investments', 'mgx': 'https://en.wikipedia.org/wiki/MGX_Fund_Management'})
xWEB = {'xai': 'https://x.ai', 'spacex': 'https://www.spacex.com', 'openai': 'https://openai.com', 'nvidia': 'https://www.nvidia.com', 'cisco': 'https://www.cisco.com', 'a16z': 'https://a16z.com', 'sequoia': 'https://www.sequoiacap.com'}
xC = {
 'musk': [['2015', 'OpenAIを共同創業、共同議長'], ['2018', 'OpenAIの取締役を退任'], ['2023', '7月にxAIを設立'], ['2024', 'OpenAIを提訴'], ['2026', 'SpaceXがxAIを買収']],
 'babuschkin': [['〜', 'DeepMind、OpenAIの研究者'], ['2023', 'xAIを共同創業'], ['2025', '8月に退社、ベンチャーキャピタルを設立']],
 'kosic': [['〜', '元OpenAI、元DeepMind'], ['2023', 'xAIを共同創業'], ['2024', '半ばに退社しOpenAIへ']],
 'yaccarino': [['〜', '元NBCUniversalの広告部門責任者'], ['2023', 'X(旧Twitter)のCEOに就任'], ['2025', '7月に退任']],
}
xBlock = gen(xN, xE, ph(['musk', 'yaccarino']), xW, xEN, xX, xWEB, xC, {})

# ---------------- Meta ----------------
mN = [
 {'id': 'meta', 'name': 'Meta', 'kind': 'c', 'from': 2013, 'desc': 'Facebook、Instagram、WhatsAppなどを運営する企業。2013年にAI研究所FAIRを設立し、Llamaを公開。2025年6月にMeta Superintelligence Labs(MSL)を発足しました。'},
 {'id': 'zuckerberg', 'name': 'マーク・ザッカーバーグ', 'kind': 'p', 'from': 2013, 'desc': '創業者でCEO。クラスB株により議決権の過半を持つ支配株主です。2025年に巨額の報酬でAI人材を集め、MSLを立ち上げました。', 'role': 'CEO / 創業者', 'founder': 1},
 {'id': 'lecun', 'name': 'ヤン・ルカン', 'kind': 'p', 'from': 2013, 'to': 2025, 'desc': 'FAIRを創設し、チーフAIサイエンティストを務めました。2025年11月に退社してAMI Labsを設立。2026年1月にワンを「経験不足」と批判したと報じられています。', 'role': '元チーフAIサイエンティスト'},
 {'id': 'pineau', 'name': 'ジョエル・ピノー', 'kind': 'p', 'from': 2017, 'to': 2025, 'desc': 'FAIRの責任者。2025年5月に退任し、のちCohereに参加したと報じられています。', 'role': '元FAIR責任者'},
 {'id': 'bosworth', 'name': 'アンドリュー・ボズワース', 'kind': 'p', 'from': 2013, 'desc': '1982年生まれ。ハーバード大学を2004年に卒業(AIの授業のTAとしてザッカーバーグと出会いました)。Microsoftで約2年、Visioの開発に携わったのち、2006年にFacebookへ(最初の15人ほどのエンジニアの一人で、ニュースフィードの開発に参加)。グループ、メッセンジャー、ビデオ通話を率い、2012年にモバイル広告への転換を主導(2015年にはモバイル広告が収益の78%)。2017年8月にAR・VR担当のVPとなり(2020年にReality Labsへ改称)、2022年にCTO(ザッカーバーグが2021年に、シュレープファーの後任と発表)。2016年の社内メモ「The Ugly」(2018年にBuzzFeedが報道)で批判されました。2025年に米陸軍予備役の中佐に任官し、Detachment 201の助言役に。2026年には、AI戦略「AI for Work」も見るようになったとWSJが報じています。', 'role': 'CTO'},
 {'id': 'mosseri', 'name': 'アダム・モセリ', 'kind': 'p', 'from': 2018, 'desc': 'Instagramの責任者(Head of Instagram)。2008年にFacebookへプロダクトデザイナーとして入り、のちにニュースフィードの製品・開発を率いました。2018年、Instagramの創業者2人の退任を受けて責任者に就任。Threadsも事実上統括していると報じられています。以前はTokBoxの最初のデザイナー、2002年に学生時代にデザイン会社Blank Mosseriを創業。ニューヨーク出身で、NYUのGallatin校で学びました(Metaの経営陣のページ・報道)。', 'role': 'Instagram責任者'},
 {'id': 'cox', 'name': 'クリス・コックス', 'kind': 'p', 'from': 2013, 'desc': '1982年生まれ。スタンフォード大学で、記号システム(人工知能専攻)を学び、大学院を中退して、2005年にFacebookへ(最初の15人ほどのエンジニアの一人で、ニュースフィードの開発に参加)。2014年にCPO(最高製品責任者)、2018年5月にFacebook、Instagram、WhatsApp、Messengerなどのアプリ全体を任されました。2019年3月、ザッカーバーグが暗号化メッセージ中心の方針を示したことを受け、退社を発表。2020年6月に、CPOとして復帰しました。', 'role': 'CPO'},
 {'id': 'wang', 'name': 'アレクサンドル・ワン', 'kind': 'p', 'from': 2025, 'desc': '1997年、米ニューメキシコ州ロスアラモス生まれ(両親は、ロスアラモス国立研究所の物理学者)。MITを中退し、2016年にルーシー・グオとScale AIを共同創業(2021年に評価額73億ドル、24歳で「自力で財を築いた億万長者」として最年少と紹介)。2025年6月、MetaがScale AIの49%を取得(約143億ドルの出資)し、ワンはMetaへ移ってChief AI Officer兼Meta Superintelligence Labsの責任者に(Scaleの CEOは退き、取締役には残りました)。コロナ禍では、サム・アルトマンと同居していたと紹介されています。', 'role': 'Chief AI Officer'},
 {'id': 'friedman', 'name': 'ナット・フリードマン', 'kind': 'p', 'from': 2025, 'desc': '1999年にMITを卒業(コンピュータ科学・数学)。同年にミゲル・デ・イカザとXimianを共同創業し、2003年にNovellが買収。2011年にXamarinを共同創業してCEOとなり、2016年にMicrosoftが買収。2018年6月にMicrosoftがGitHubを75億ドルで買収すると発表し、同年10月にGitHubのCEOに就任、2021年11月に退任を発表しました。ダニエル・グロスとAI投資(C2 Investments)を行い、2025年6月にMetaへ移って、Meta Superintelligence Labsを、ワンとともに率います(製品担当)。', 'role': 'MSLの幹部'},
 {'id': 'zhao', 'name': 'シェンジア・ジャオ', 'kind': 'p', 'from': 2025, 'desc': '元OpenAIの研究者。MSLのチーフサイエンティストに就任と報じられています。', 'role': 'MSL チーフサイエンティスト'},
 {'id': 'gross', 'name': 'ダニエル・グロス', 'kind': 'p', 'from': 2025, 'desc': 'Safe Superintelligenceの共同創業者から、2025年にMetaへ移ったと報じられています。', 'role': 'MSLの幹部'},
 {'id': 'pang', 'name': 'ルオミン・パン', 'kind': 'p', 'from': 2025, 'desc': '元Appleの基盤モデル責任者。2025年に巨額の報酬でMetaへ移ったと報じられています。', 'role': 'MSLの研究者'},
 {'id': 'instagram', 'name': 'Instagram', 'kind': 'o', 'from': 2012, 'desc': '2012年にFacebookが買収した写真・動画SNS(報道では約10億ドル)。創業者のシストロムとクリーガーは2018年に退任しました。ダブルクリックで、Instagramの図を開きます。', 'role': '2012年に買収'},
 {'id': 'systrom', 'name': 'ケビン・シストロム', 'kind': 'p', 'from': 2012, 'to': 2018, 'desc': 'Instagramの共同創業者でCEO。買収後もInstagramを率い、2018年9月に退任しました。', 'role': '元Instagram CEO'},
 {'id': 'krieger', 'name': 'マイク・クリーガー', 'kind': 'p', 'from': 2012, 'to': 2018, 'desc': 'Instagramの共同創業者でCTO。2018年9月に退任し、2024年にAnthropicへ入社しました。', 'role': '元Instagram CTO'},
 {'id': 'whatsapp', 'name': 'WhatsApp', 'kind': 'o', 'from': 2014, 'desc': '2014年にFacebookが買収したメッセージアプリ(報道では約190億ドル)。', 'role': '2014年に買収'},
 {'id': 'koum', 'name': 'ジャン・クーム', 'kind': 'p', 'from': 2014, 'to': 2018, 'desc': 'WhatsAppの共同創業者でCEO。2018年4月に退任を発表。Facebookとの間で、プライバシー、広告、収益化をめぐる衝突があったと報じられています。', 'role': '元WhatsApp CEO'},
 {'id': 'acton', 'name': 'ブライアン・アクトン', 'kind': 'p', 'from': 2014, 'to': 2017, 'desc': 'WhatsAppの共同創業者。2017年9月に退社し、のちSignal Foundationを共同で設立しました。', 'role': '元WhatsApp共同創業者'},
 {'id': 'luckey', 'name': 'パルマー・ラッキー', 'kind': 'p', 'from': 2014, 'to': 2017, 'desc': 'Oculus VRの創業者。2017年3月にFacebookを離れ、同年6月にAnduril Industriesを共同創業しました。', 'role': '元Oculus創業者'},
 {'id': 'oculus', 'name': 'Oculus VR', 'kind': 'o', 'from': 2014, 'desc': '2014年にFacebookが買収したVRの会社(報道では約20億ドル)。ダブルクリックで図を開きます。', 'role': '2014年に買収'},
 {'id': 'signal', 'name': 'Signal Foundation', 'kind': 'o', 'from': 2018, 'desc': 'アクトンが2018年に共同で設立した非営利団体(Signalアプリを運営)。', 'role': 'アクトンが設立'},
 {'id': 'anduril', 'name': 'Anduril Industries', 'kind': 'o', 'from': 2017, 'desc': 'ラッキーが2017年に共同創業した防衛技術の会社。', 'role': 'ラッキーが設立'},
 {'id': 'olivan', 'name': 'ハビエル・オリバン', 'kind': 'p', 'from': 2013, 'desc': 'COO(最高執行責任者)。1977年スペイン生まれ。ナバラ大学(テクヌン)で工学を学び、Siemens、NTT Dataを経て、スタンフォードのMBA(2007年修了)へ。2007年10月にFacebookへ入り、国際的な成長の責任者に(上司はパリハピティヤ)。2011〜2018年に成長担当のVP(Internet.org、Facebook Liteを推進。WhatsApp、Onavoの買収に助言)、2018年に信頼と安全の担当、2018〜2022年に中核製品のVPを務めました。2022年にサンドバーグの後任としてCOOに就きました(就任時期は、報道が6月、Wikipediaが8月と食い違っています)。2025年1月の再編で、Reality Labsの事業運営も見るようになりました。外部ではEndeavor Globalの取締役、元Mercado Libreの取締役(6年)。ダブルクリックで、個人の相関図を開きます。', 'role': 'COO(2022年〜)'},
 {'id': 'sandberg', 'name': 'シェリル・サンドバーグ', 'kind': 'p', 'from': 2013, 'to': 2022, 'desc': '2008年から約14年間COOを務め、2022年に退任。後任はオリバンです。', 'role': '元COO'},
 {'id': 'wynn', 'name': 'サラ・ウィン・ウィリアムズ', 'kind': 'p', 'from': 2013, 'to': 2017, 'desc': 'ニュージーランド出身の弁護士・外交官。2011年にFacebookへ入り、グローバル公共政策のディレクターに。2017年に解雇され、2025年3月に回顧録『Careless People』を出版しました(Metaは反論し、仲裁で発言を制限)。', 'role': '元グローバル公共政策ディレクター / 著者'},
 {'id': 'kaplan', 'name': 'ジョエル・カプラン', 'kind': 'p', 'from': 2013, 'desc': 'Metaのチーフ・グローバル・アフェアーズ・オフィサー(2025年1月2日に、ニック・クレッグの後任として発表)。ハーバード大学卒、米海兵隊の砲兵将校(1991〜1995年)、ハーバード法科大学院(1998年)を経て、ブッシュ政権で大統領補佐官・行政管理予算局の副局長・ホワイトハウス副首席補佐官(政策、2006〜2009年)を歴任。2011年5月にFacebookへ入り、2014年10月にマーン・レヴィンの後任としてグローバル公共政策のVPに。2018年にはカバノー氏の最高裁人事を支持したことが注目されました。ウィン・ウィリアムズの回顧録は、カプランについて職場での行為の主張をしていますが、Metaは、2017年の社内調査で問題なしと判断したとし、主張を誤解を招く根拠のないものだと反論しています(未確認の主張)。', 'role': 'グローバル・アフェアーズ責任者'},
 {'id': 'carelesspeople', 'name': '『Careless People』', 'kind': 'o', 'from': 2025, 'desc': 'ウィン・ウィリアムズの回顧録(2025年3月11日)。Metaは「古い、すでに報じられた主張」「虚偽」と反論。ダブルクリックで、登場人物の図を開きます。', 'role': '元幹部の回顧録'},
 {'id': 'levine', 'name': 'マーン・レヴィン', 'kind': 'p', 'from': 2013, 'to': 2023, 'desc': '元チーフ・ビジネス・オフィサー。米財務省(1993〜2000年)、ハーバード大学のサマーズ学長の首席補佐官(2001〜2003年)、オバマ政権の国家経済会議の首席補佐官(2009〜2010年)を経て、2010年にFacebookへ。グローバル公共政策のVP(2010〜2014年)、2014年にInstagramの初代COO、2018年にFacebookへ戻ってグローバル・パートナーシップ等のVP、2021年6月にチーフ・ビジネス・オフィサーに就き、2023年2月に退任しました。サンドバーグが創設したLean Inの取締役も務めました。', 'role': '元チーフ・ビジネス・オフィサー(2021〜2023年)'},
 {'id': 'vanguard', 'name': 'Vanguard', 'kind': 'i', 'from': 2013, 'desc': 'Metaの大株主として一般に報じられる運用会社。', 'role': '機関投資家'},
 {'id': 'blackrock', 'name': 'BlackRock', 'kind': 'i', 'from': 2013, 'desc': 'Metaの大株主として一般に報じられる運用会社。', 'role': '機関投資家'},
 {'id': 'scale', 'name': 'Scale AI', 'kind': 'o', 'from': 2025, 'desc': 'AI向けデータ整備の企業。Metaが約143億ドルを出資し、創業者のワンがMetaへ移りました(約49%の取得と報じられています)。', 'role': 'Metaが出資'},
 {'id': 'ami', 'name': 'AMI Labs', 'kind': 'o', 'from': 2025, 'desc': 'ルカンが2025年末に設立したAI研究企業(Advanced Machine Intelligence)。', 'role': 'ルカンが設立'},
 {'id': 'cohere', 'name': 'Cohere', 'kind': 'o', 'from': 2019, 'desc': 'カナダのAI企業。ピノーの移籍先と報じられています。', 'role': 'ピノーの移籍先'},
 {'id': 'openai', 'name': 'OpenAI', 'kind': 'o', 'from': 2013, 'desc': 'MSLが2025年に引き抜いた研究者の出身元。ジャオもここから移りました。', 'role': '出身元'},
 {'id': 'ssi', 'name': 'Safe Superintelligence', 'kind': 'o', 'from': 2024, 'desc': 'スツケバーらが設立。グロスはここからMetaへ。', 'role': '出身元'},
 {'id': 'apple', 'name': 'Apple', 'kind': 'o', 'from': 2013, 'desc': 'パンの出身元。', 'role': '出身元'},
]
mE = ("const E = [];\n"
 "N.forEach(n=>{\n  if(n.kind==='p') E.push({a:n.id,b:'meta',k:'member'});\n  if(n.kind==='i') E.push({a:n.id,b:'meta',k:'invest'});\n});\n"
 "E.push({a:'meta',b:'instagram',k:'owns',label:'2012年に買収',since:2012});\nE.push({a:'meta',b:'whatsapp',k:'owns',label:'2014年に買収',since:2014});\nE.push({a:'systrom',b:'instagram',k:'from',label:'共同創業'});\nE.push({a:'krieger',b:'instagram',k:'from',label:'共同創業'});\nE.push({a:'mosseri',b:'instagram',k:'link',label:'責任者'});\nE.push({a:'zuckerberg',b:'instagram',k:'link',label:'買収を主導',since:2012});\nE.push({a:'systrom',b:'zuckerberg',k:'conflict',label:'資源・独立性をめぐり対立(報道)',since:2017});\nE.push({a:'olivan',b:'sandberg',k:'link',label:'2022年に後任',since:2022});\nE.push({a:'levine',b:'instagram',k:'from',label:'初代COO(2014年)'});\nE.push({a:'levine',b:'sandberg',k:'link',label:'Lean In取締役'});\nE.push({a:'wynn',b:'carelesspeople',k:'link',label:'著者'});\nE.push({a:'wynn',b:'kaplan',k:'conflict',label:'ハラスメントを報告したと主張',since:2017});\nE.push({a:'wynn',b:'meta',k:'conflict',label:'2017年に解雇、2025年に仲裁',since:2025});\nE.push({a:'koum',b:'whatsapp',k:'from',label:'共同創業'});\nE.push({a:'acton',b:'whatsapp',k:'from',label:'共同創業'});\nE.push({a:'luckey',b:'oculus',k:'from',label:'創業'});\nE.push({a:'meta',b:'oculus',k:'owns',label:'2014年に買収',since:2014});\nE.push({a:'acton',b:'signal',k:'moved'});\nE.push({a:'luckey',b:'anduril',k:'moved'});\nE.push({a:'koum',b:'meta',k:'conflict',label:'2018年に衝突(報道)',since:2018});\nE.push({a:'luckey',b:'meta',k:'conflict',label:'2017年に退社(経緯は報道)',since:2017});\n"
 "E.push({a:'meta',b:'scale',k:'invest2',label:'約143億ドル出資'});\n"
 "E.push({a:'wang',b:'scale',k:'from'});\n"
 "E.push({a:'zhao',b:'openai',k:'from'});\n"
 "E.push({a:'gross',b:'ssi',k:'from'});\n"
 "E.push({a:'pang',b:'apple',k:'from'});\n"
 "E.push({a:'lecun',b:'ami',k:'moved'});\n"
 "E.push({a:'pineau',b:'cohere',k:'moved'});\n"
 "E.push({a:'lecun',b:'wang',k:'conflict',label:'2026年1月に批判',since:2026});\n\n")
mEN = {'zuckerberg': 'Mark Zuckerberg', 'lecun': 'Yann LeCun', 'pineau': 'Joelle Pineau', 'bosworth': 'Andrew Bosworth', 'cox': 'Chris Cox', 'mosseri': 'Adam Mosseri', 'wang': 'Alexandr Wang',
       'systrom': 'Kevin Systrom', 'krieger': 'Mike Krieger', 'olivan': 'Javier Olivan', 'levine': 'Marne Levine', 'wynn': 'Sarah Wynn-Williams', 'kaplan': 'Joel Kaplan', 'sandberg': 'Sheryl Sandberg', 'koum': 'Jan Koum', 'acton': 'Brian Acton', 'luckey': 'Palmer Luckey', 'friedman': 'Nat Friedman', 'zhao': 'Shengjia Zhao', 'gross': 'Daniel Gross', 'pang': 'Ruoming Pang'}
mX = {'zuckerberg': 'zuck', 'lecun': 'ylecun', 'bosworth': 'boztank', 'wang': 'alexandr_wang', 'friedman': 'natfriedman', 'koum': 'jankoum', 'acton': 'brianacton', 'gross': 'danielgross', 'meta': 'AIatMeta', 'openai': 'OpenAI', 'nvidia': 'nvidia'}
mW = wk(['zuckerberg', 'wang', 'friedman', 'lecun', 'gross', 'bosworth', 'pineau'])
mW.update({'meta': 'https://en.wikipedia.org/wiki/Meta_Platforms', 'scale': 'https://en.wikipedia.org/wiki/Scale_AI', 'vanguard': 'https://en.wikipedia.org/wiki/Vanguard_Group',
           'blackrock': 'https://en.wikipedia.org/wiki/BlackRock', 'cohere': 'https://en.wikipedia.org/wiki/Cohere', 'openai': 'https://en.wikipedia.org/wiki/OpenAI',
           'ssi': 'https://en.wikipedia.org/wiki/Safe_Superintelligence_Inc.', 'apple': 'https://en.wikipedia.org/wiki/Apple_Inc.', 'ami': 'https://en.wikipedia.org/wiki/Yann_LeCun'})
mWEB = {'meta': 'https://ai.meta.com', 'scale': 'https://scale.com', 'cohere': 'https://cohere.com', 'openai': 'https://openai.com', 'ssi': 'https://ssi.inc', 'apple': 'https://www.apple.com'}
from newco_data7c import LINKS as _IL
mL = {'lecun': [['個人サイト', 'https://yann.lecun.com']], 'friedman': [['個人サイト', 'https://nat.org']],
      'instagram': _IL['instagram'], 'systrom': _IL['systrom'], 'krieger': _IL['krieger'], 'mosseri': _IL['mosseri'], 'zuckerberg': _IL['zuckerberg'],
      'whatsapp': [['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']],
      'wynn': [['出典: Wikipedia(Sarah Wynn-Williams)', 'https://en.wikipedia.org/wiki/Sarah_Wynn-Williams']],
      'kaplan': [['出典: Wikipedia(Joel Kaplan)', 'https://en.wikipedia.org/wiki/Joel_Kaplan']],
      'carelesspeople': [['出典: Wikipedia(Careless People)', 'https://en.wikipedia.org/wiki/Careless_People']],
      'levine': [['出典: Wikipedia(Marne Levine)', 'https://en.wikipedia.org/wiki/Marne_Levine'], ['公式Instagram(プロフィールが「元Meta CBO」と一致)', 'https://www.instagram.com/marnelevine/']],
      'olivan': [['出典: Wikipedia(Javier Oliván)', 'https://en.wikipedia.org/wiki/Javier_Olivan']],
      'sandberg': [['出典: Wikipedia(Sheryl Sandberg)', 'https://en.wikipedia.org/wiki/Sheryl_Sandberg']],
      'koum': [['出典: Wikipedia(Jan Koum)', 'https://en.wikipedia.org/wiki/Jan_Koum'], ['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']],
      'acton': [['出典: Wikipedia(Brian Acton)', 'https://en.wikipedia.org/wiki/Brian_Acton'], ['出典: Wikipedia(Signal Foundation)', 'https://en.wikipedia.org/wiki/Signal_Foundation']],
      'luckey': [['出典: Wikipedia(Palmer Luckey)', 'https://en.wikipedia.org/wiki/Palmer_Luckey']],
      'oculus': [['出典: Wikipedia(Oculus VR)', 'https://en.wikipedia.org/wiki/Oculus_VR']],
      'signal': [['出典: Wikipedia(Signal Foundation)', 'https://en.wikipedia.org/wiki/Signal_Foundation']],
      'anduril': [['出典: Wikipedia(Anduril Industries)', 'https://en.wikipedia.org/wiki/Anduril_Industries']]}
mC = {
 'bosworth': [['2004', 'ハーバード大学を卒業。Microsoft(Visio)で約2年'], ['2006', 'Facebookに入社。ニュースフィードの開発に参加'], ['2012', 'モバイル広告への転換を主導'], ['2017', '8月、AR・VR担当のVPに(2020年にReality Labs)'], ['2022', 'CTOに'], ['2025', '米陸軍予備役の中佐に。Detachment 201の助言役'], ['2026', 'AI戦略(AI for Work)も担当と報じられる']],
 'cox': [['2005', 'スタンフォード大学の大学院を中退し、Facebookへ。ニュースフィードの開発に参加'], ['2014', 'CPOに'], ['2018', '5月、各アプリ(Facebook・Instagram・WhatsApp・Messenger)を担当'], ['2019', '3月に退社を発表'], ['2020', '6月、CPOとして復帰']],
 'kaplan': [['1991', '米海兵隊の砲兵将校(〜1995年)'], ['2001', 'ブッシュ政権の大統領補佐官(〜2003年)'], ['2006', 'ホワイトハウス副首席補佐官(政策、〜2009年)'], ['2011', 'Facebookに入社。米国の公共政策のVP'], ['2014', 'グローバル公共政策のVPに'], ['2025', '1月、チーフ・グローバル・アフェアーズ・オフィサーに']],
 'friedman': [['1999', 'Ximianを共同創業(2003年にNovellが買収)'], ['2011', 'Xamarinを共同創業(CEO)'], ['2016', 'Microsoftが、Xamarinを買収'], ['2018', '10月、GitHubのCEOに'], ['2021', '11月に、GitHubのCEOを退任と発表'], ['2025', '6月、Meta Superintelligence Labsに参加']],
 'levine': [['1993', '米財務省に入る(〜2000年)'], ['2001', 'ハーバード大学のサマーズ学長の首席補佐官(〜2003年)'], ['2009', 'オバマ政権の国家経済会議の首席補佐官(〜2010年)'], ['2010', 'Facebookのグローバル公共政策VPに(〜2014年)'], ['2014', 'Instagramの初代COOに'], ['2018', 'Facebookに戻り、グローバル・パートナーシップ等のVPに'], ['2021', '6月、チーフ・ビジネス・オフィサーに'], ['2023', '2月に退任']],
 'wang': [['1997', '米ニューメキシコ州ロスアラモスに生まれる'], ['2016', 'MITを中退し、Scale AIを共同創業'], ['2021', 'Scale AIの評価額が73億ドルに'], ['2025', '6月、MetaがScale AIの49%を取得。ワンはMetaへ移り、Chief AI Officerに']],
 'olivan': [['1977', 'スペインに生まれる'], ['2002', 'ナバラ大学(テクヌン)を卒業'], ['2007', 'スタンフォードのMBAを修了し、10月にFacebookへ(国際的な成長の責任者)'], ['2011', '成長担当のVPに(〜2018年)'], ['2014', 'アスペン研究所のヘンリー・クラウン・フェロー'], ['2018', '信頼と安全の担当、のち中核製品のVP'], ['2022', 'サンドバーグの後任としてCOOに'], ['2025', '1月、Reality Labsの事業運営も担当']],
 'sandberg': [['2008', 'Facebookに入社しCOOに'], ['2022', 'COOを退任(約14年)']],
 'zuckerberg': [['2004', 'Facebookを創業'], ['2013', 'FAIR(AI研究所)を設立'], ['2021', '社名をMetaに変更'], ['2025', 'MSLを発足']],
 'lecun': [['2013', 'MetaのFAIRを創設'], ['2018', 'チューリング賞を受賞'], ['2025', '11月にMetaを退社しAMI Labsを設立']],

 'gross': [['〜', 'Y Combinatorの元パートナー'], ['2024', 'Safe Superintelligenceを共同創業'], ['2025', 'Metaに移籍と報道']],
 'pineau': [['〜', 'マギル大学の教授'], ['2017', 'MetaのFAIRに参加'], ['2025', '5月に退任']],
}
mBlock = gen(mN, mE, ph(['zuckerberg', 'wang', 'friedman', 'lecun', 'gross', 'bosworth', 'pineau']), mW, mEN, mX, mWEB, mC, mL)

import sys as _sys
_sys.path.insert(0, S)
from adds import ADDS, apply_adds, legacy_json, LEGACY_KEYS, LEGACY_EDGES
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5, **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data7c').CO7C, **__import__('newco_data7d').CO7D, **__import__('newco_data7e').CO7E, **__import__('newco_data7f').CO7F, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)
from ext_apply import apply_ext   # 外部AIが作った追加データ(ext_adds/*.json)。検査に失敗すると、ここでビルドを止める
apply_ext(CO_ALL, ADDS, LEGACY_EDGES)
data = 'const LEGACY=%s;\n' % dump(legacy_json())
data += 'const DATA={\n' + ',\n'.join([
    fn('openai', 'openai', block(O + r'\openai-relationship-map.html')),
    fn('anthropic', 'anthropic', block(O + r'\anthropic-relationship-map.html')),
    fn('xai', 'xai', xBlock),
    fn('meta', 'meta', mBlock)] + [
    fn(k, c['center'], gen(c['N'], c['edges'], {}, c['WIKI'], c['EN'], c['X'], c['WEB'], c['CAREER'], c['LINKS']))
    for k, c in CO_ALL.items() if not k.startswith('stw_')]) + '\n};\n'
data += 'const RANK=%s;' % dump(__import__('newco_data8').RANK) + chr(10)
data += 'const STARTUPS=%s;' % dump(__import__('newco_data8').STARTUPS) + chr(10)
data += 'const AIWD=%s;' % dump(__import__('newco_data10w').AIWD) + chr(10)
_awn, _awb = __import__('newco_data10w').write_shards(O + r'\aw')
data += 'const AWN=%d;' % _awn + chr(10)
print('別ファイルに書き出した図', len(__import__('newco_data10w').AWDATA), '社 /', _awn, 'ファイル /', round(_awb / 1e6, 2), 'MB')
data += 'const JPCO=%s;' % dump(__import__('newco_data8').JPCO) + chr(10)
import os, sys
sys.path.insert(0, S)
from personal_data import P
from personal_data2 import P2
from personal_data3 import P3
from newco_data import CO
from newco_data2 import CO2
from newco_data3 import CO3
from personal_data4 import P4
from personal_data5 import P5
from newco_data4 import CO4
from newco_data5 import CO5
from personal_data6 import P6
from newco_data6 import CO6
from newco_data7 import CO7
from newco_data7b import CO7B
from newco_data7c import CO7C
from newco_data7d import CO7D
from newco_data7e import CO7E
from newco_data7f import CO7F
from newco_data8 import CO8, RANK
from personal_data8 import P8
CO = {**CO, **CO2, **CO3, **CO4, **CO5, **CO6, **CO7, **CO7B, **CO7C, **CO7D, **CO7E, **CO7F, **CO8}
P = {**P, **P2, **P3, **P4, **P5, **P6, **P8}
# 個人の相関図の「学校・所属」: 学校と日本の組織は日本語、海外の会社は英語の名前にする
SCHOOLS = ['University', 'College', 'Institute', 'MIT', 'Caltech', 'IIT', 'School', 'École', 'Berkeley', 'Stanford', 'Harvard', 'Cambridge', 'Oxford', 'Toronto', 'Tokyo', 'Gatsby']
JPKEEP = {'Rakuten', 'Raksul', 'Yahoo Japan', 'YJ Capital', 'Z Venture Capital', 'Dream Incubator', 'Mercari', 'Ministry of Foreign Affairs',
          'Industrial Bank of Japan', 'Bizseek', 'CSET', 'Boost Consulting', 'White House', 'LINE', 'livedoor', 'PayPay', 'Waseda University', 'Keio University', 'Hitotsubashi University'}
def fix_org(rows):
    out = []
    for g, rel, en, jp, desc in rows:
        if g == 'org' and en not in JPKEEP and not any(w in en for w in SCHOOLS):
            jp = en
        out.append((g, rel, en, jp, desc))
    return out
# 追加した人物に、個別の関係データがない場合は、所属の1行だけを自動で作る
def _fallback():
    names = {'openai': 'OpenAI', 'anthropic': 'Anthropic', 'xai': 'xAI', 'meta': 'Meta'}
    comps = []
    for k, c in CO.items():
        center = next(n for n in c['N'] if n['id'] == c['center'])
        comps.append((center['name'], c['N'], c['EN']))
    for k in LEGACY_KEYS:
        a = ADDS[k]
        comps.append((names[k], a['nodes'], a['en']))
    for cname, nodes, en in comps:
        for n in nodes:
            e = en.get(n['id'])
            if not e or e in P:
                continue
            P[e] = [('org', '所属', cname, cname, '%s。%s年〜%s' % (n.get('role') or '', n['from'], ('%s年' % n['to']) if n.get('to') else '現在'))]
        # 同じ人が複数社にいる場合のため、2社目以降も追記
    for cname, nodes, en in comps:
        for n in nodes:
            e = en.get(n['id'])
            if e and e in P and P[e] and P[e][0][1] == '所属' and not any(r[2] == cname for r in P[e]):
                P[e].append(('org', '所属', cname, cname, '%s。%s年〜%s' % (n.get('role') or '', n['from'], ('%s年' % n['to']) if n.get('to') else '現在')))
_fallback()
P = {k: fix_org(v) for k, v in P.items()}
people =json.loads(open(S + r'\people.json', encoding='utf-8').read())
missing = [p[0] for p in people if p[0] not in P]
assert not missing, missing
need = {en for c in CO.values() for en in c['EN'].values()}
missing2 = sorted(need - set(P))
assert not missing2, missing2
def jl(name, default):
    return json.load(open(S + '\\' + name, encoding='utf-8')) if os.path.exists(S + '\\' + name) else default
DROP = set(jl('drop.json', [])) | set(jl('drop2.json', [])) | set(jl('drop3.json', [])) | set(jl('drop5.json', [])) | set(jl('drop6.json', [])) | set(jl('drop7.json', []))
raw = {**jl('outsiders.json', {}), **jl('outsiders2.json', {}), **jl('outsiders3.json', {}), **jl('outsiders5.json', {}), **jl('outsiders6.json', {})}
if not os.environ.get('SKIP_UNREVIEWED'):   # 確認前の写真(7, 8)は、確認が済むまで使わない設定
    raw.update(jl('outsiders7.json', {}))
    raw.update(jl('outsiders8.json', {}))
    raw.update(jl('outsiders9.json', {}))
# 日本語Wikipedia等で取り直した結果は、別の除外リスト(drop4)で判断する
raw4 = jl('outsiders4.json', {})
DROP4 = set(jl('drop4.json', []))
for k in list(raw4):
    DROP.discard(k)
    raw.pop(k, None)
    if k not in DROP4:
        raw[k] = raw4[k]
OUT = {}
for k, v in raw.items():
    if k in DROP or not v.get('title'):
        continue
    OUT[k] = {'img': v.get('img'), 'wiki': v.get('wiki')}
data += 'const PERSONAL=%s;\nconst OUT=%s;\n' % (dump(P), dump(OUT))
t = open(S + r'\hub_template.html', encoding='utf-8').read()
t = t.replace("Object.keys(COMPANIES).forEach(k=>{", "['openai','anthropic','xai','meta','tml','ssi','gdm','msft','mistral','sakana','softbank','nvidia'].forEach(k=>{")
assert '/*DATA*/' in t
open(O + r'\relationship-maps.html', 'w', encoding='utf-8').write(t.replace('/*DATA*/', data))
print(len(data))
