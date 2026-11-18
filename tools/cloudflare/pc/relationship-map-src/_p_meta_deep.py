import re
p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
lines = b.split('\n')


def setnode(nid, text):
    for i, x in enumerate(lines):
        if x.startswith(" {'id': '%s'," % nid):
            m = re.search(r"'role': '([^']*)'", x)
            role = m.group(1) if m else ''
            kind = re.search(r"'kind': '([a-z])'", x).group(1)
            frm = re.search(r"'from': (\d+)", x).group(1)
            to = re.search(r"'to': (\d+)", x)
            name = re.search(r"'name': '([^']*)'", x).group(1)
            extra = (", 'to': %s" % to.group(1)) if to else ''
            fnd = ", 'founder': 1" if "'founder': 1" in x else ''
            lines[i] = " {'id': '%s', 'name': '%s', 'kind': '%s', 'from': %s%s, 'desc': '%s', 'role': '%s'%s}," % (nid, name, kind, frm, extra, text.replace("'", "\\'"), role, fnd)
            return True
    raise SystemExit('node not found: ' + nid)


setnode('bosworth', '1982年生まれ。ハーバード大学を2004年に卒業(AIの授業のTAとしてザッカーバーグと出会いました)。Microsoftで約2年、Visioの開発に携わったのち、2006年にFacebookへ(最初の15人ほどのエンジニアの一人で、ニュースフィードの開発に参加)。グループ、メッセンジャー、ビデオ通話を率い、2012年にモバイル広告への転換を主導(2015年にはモバイル広告が収益の78%)。2017年8月にAR・VR担当のVPとなり(2020年にReality Labsへ改称)、2022年にCTO(ザッカーバーグが2021年に、シュレープファーの後任と発表)。2016年の社内メモ「The Ugly」(2018年にBuzzFeedが報道)で批判されました。2025年に米陸軍予備役の中佐に任官し、Detachment 201の助言役に。2026年には、AI戦略「AI for Work」も見るようになったとWSJが報じています。')
setnode('cox', '1982年生まれ。スタンフォード大学で、記号システム(人工知能専攻)を学び、大学院を中退して、2005年にFacebookへ(最初の15人ほどのエンジニアの一人で、ニュースフィードの開発に参加)。2014年にCPO(最高製品責任者)、2018年5月にFacebook、Instagram、WhatsApp、Messengerなどのアプリ全体を任されました。2019年3月、ザッカーバーグが暗号化メッセージ中心の方針を示したことを受け、退社を発表。2020年6月に、CPOとして復帰しました。')
setnode('wang', '1997年、米ニューメキシコ州ロスアラモス生まれ(両親は、ロスアラモス国立研究所の物理学者)。MITを中退し、2016年にルーシー・グオとScale AIを共同創業(2021年に評価額73億ドル、24歳で「自力で財を築いた億万長者」として最年少と紹介)。2025年6月、MetaがScale AIの49%を取得(約143億ドルの出資)し、ワンはMetaへ移ってChief AI Officer兼Meta Superintelligence Labsの責任者に(Scaleの CEOは退き、取締役には残りました)。コロナ禍では、サム・アルトマンと同居していたと紹介されています。')
setnode('friedman', '1999年にMITを卒業(コンピュータ科学・数学)。同年にミゲル・デ・イカザとXimianを共同創業し、2003年にNovellが買収。2011年にXamarinを共同創業してCEOとなり、2016年にMicrosoftが買収。2018年6月にMicrosoftがGitHubを75億ドルで買収すると発表し、同年10月にGitHubのCEOに就任、2021年11月に退任を発表しました。ダニエル・グロスとAI投資(C2 Investments)を行い、2025年6月にMetaへ移って、Meta Superintelligence Labsを、ワンとともに率います(製品担当)。')
setnode('kaplan', 'Metaのチーフ・グローバル・アフェアーズ・オフィサー(2025年1月2日に、ニック・クレッグの後任として発表)。ハーバード大学卒、米海兵隊の砲兵将校(1991〜1995年)、ハーバード法科大学院(1998年)を経て、ブッシュ政権で大統領補佐官・行政管理予算局の副局長・ホワイトハウス副首席補佐官(政策、2006〜2009年)を歴任。2011年5月にFacebookへ入り、2014年10月にマーン・レヴィンの後任としてグローバル公共政策のVPに。2018年にはカバノー氏の最高裁人事を支持したことが注目されました。ウィン・ウィリアムズの回顧録は、カプランについて職場での行為の主張をしていますが、Metaは、2017年の社内調査で問題なしと判断したとし、主張を誤解を招く根拠のないものだと反論しています(未確認の主張)。')
b = '\n'.join(lines)
# 経歴
k = "mC = {\n"
assert b.count(k) == 1
add = (" 'bosworth': [['2004', 'ハーバード大学を卒業。Microsoft(Visio)で約2年'], ['2006', 'Facebookに入社。ニュースフィードの開発に参加'], ['2012', 'モバイル広告への転換を主導'], ['2017', '8月、AR・VR担当のVPに(2020年にReality Labs)'], ['2022', 'CTOに'], ['2025', '米陸軍予備役の中佐に。Detachment 201の助言役'], ['2026', 'AI戦略(AI for Work)も担当と報じられる']],\n"
       " 'cox': [['2005', 'スタンフォード大学の大学院を中退し、Facebookへ。ニュースフィードの開発に参加'], ['2014', 'CPOに'], ['2018', '5月、各アプリ(Facebook・Instagram・WhatsApp・Messenger)を担当'], ['2019', '3月に退社を発表'], ['2020', '6月、CPOとして復帰']],\n"
       " 'kaplan': [['1991', '米海兵隊の砲兵将校(〜1995年)'], ['2001', 'ブッシュ政権の大統領補佐官(〜2003年)'], ['2006', 'ホワイトハウス副首席補佐官(政策、〜2009年)'], ['2011', 'Facebookに入社。米国の公共政策のVP'], ['2014', 'グローバル公共政策のVPに'], ['2025', '1月、チーフ・グローバル・アフェアーズ・オフィサーに']],\n"
       " 'friedman': [['1999', 'Ximianを共同創業(2003年にNovellが買収)'], ['2011', 'Xamarinを共同創業(CEO)'], ['2016', 'Microsoftが、Xamarinを買収'], ['2018', '10月、GitHubのCEOに'], ['2021', '11月に、GitHubのCEOを退任と発表'], ['2025', '6月、Meta Superintelligence Labsに参加']],\n")
b = b.replace(k, k + add, 1)
# 既存の wang の経歴行は新しいものを優先(同じキーが2つあると後ろが勝つので、元のキーを除く)
b = re.sub(r"\n 'wang': \[\['2016', 'Scale AIを創業'\].*?\],\n", "\n", b, count=1)
b = b.replace(" 'friedman': [['2018', 'GitHub CEO(〜2021)'], ['2025', 'MetaのMSLに参加と報道']],\n", "\n", 1)
k2 = " 'olivan': [['1977', 'スペインに生まれる']"
assert b.count(k2) == 1
b = b.replace(k2, " 'wang': [['1997', '米ニューメキシコ州ロスアラモスに生まれる'], ['2016', 'MITを中退し、Scale AIを共同創業'], ['2021', 'Scale AIの評価額が73億ドルに'], ['2025', '6月、MetaがScale AIの49%を取得。ワンはMetaへ移り、Chief AI Officerに']],\n" + k2, 1)
open(p, 'w', encoding='utf-8').write(b)
# 個人の相関図
p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
add = """'Andrew Bosworth': [
 (W, '大学時代に出会った上司', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', 'ハーバード大学で、AIの授業のTAをしていたときに知り合いました。'),
 (W, '前任のCTO', 'Mike Schroepfer', 'マイク・シュレープファー', '2022年に、CTOを引き継ぎました。'),
 (W, '同僚', 'Chris Cox', 'クリス・コックス', 'ともに、最初の15人ほどのエンジニアの一人(2005〜2006年)。'),
 (O, '最初の職場', 'Microsoft', 'Microsoft', 'Visioの開発者として、約2年。'),
 (O, '出身大学', 'Harvard University', 'ハーバード大学', '2004年に卒業。'),
 (O, '担当部門', 'Reality Labs', 'Reality Labs', '2017年からAR・VR担当、CTOとしても統括。'),
],
'Chris Cox': [
 (W, '上司(CEO)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2019年に退社し、2020年に復帰。'),
 (W, '同僚', 'Andrew Bosworth', 'アンドリュー・ボズワース', 'ともに、最初の15人ほどのエンジニアの一人。'),
 (W, '同僚', 'Javier Olivan', 'ハビエル・オリバン', 'MetaのCOO。'),
 (O, '出身大学', 'Stanford University', 'スタンフォード大学', '記号システム(人工知能専攻)。大学院を中退して、2005年にFacebookへ。'),
 (O, '担当', 'Instagram', 'Instagram', '2018年5月から、各アプリを担当。'),
],
'Joel Kaplan': [
 (W, '上司(CEO)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', 'Metaのチーフ・グローバル・アフェアーズ・オフィサー。'),
 (W, '前任', 'Nick Clegg', 'ニック・クレッグ', '2025年1月に、役職を引き継ぎました。'),
 (W, '前任', 'Marne Levine', 'マーン・レヴィン', '2014年に、グローバル公共政策のVPを引き継ぎました。'),
 (R, '主張・反論', 'Sarah Wynn-Williams', 'サラ・ウィン・ウィリアムズ', '元の部下。回顧録で職場での行為を主張。Metaは、2017年の社内調査で問題なしと説明し、反論しています(未確認の主張)。'),
 (O, '前の勤め先', 'White House', 'ホワイトハウス', '2006〜2009年に、副首席補佐官(政策)。ブッシュ政権。'),
 (O, '出身', 'U.S. Marine Corps', '米海兵隊', '1991〜1995年、砲兵将校。'),
],
'Alexandr Wang': [
 (W, '上司(CEO)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', '2025年6月、MetaのChief AI Officerに。'),
 (W, '共同率い', 'Nat Friedman', 'ナット・フリードマン', 'Meta Superintelligence Labsを共同で率います。'),
 (W, '共同創業者', 'Lucy Guo', 'ルーシー・グオ', '2016年に、Scale AIを共同創業。'),
 (F, '元ルームメイト', 'Sam Altman', 'サム・アルトマン', 'コロナ禍に、同居していたと紹介されています。'),
 (O, '出身', 'Scale AI', 'Scale AI', '2025年にMetaが49%を取得。取締役には残りました。'),
 (O, '中退した大学', 'MIT', 'MIT', '短期間在籍して、2016年に創業のため中退。'),
],
'Nat Friedman': [
 (W, '共同率い', 'Alexandr Wang', 'アレクサンドル・ワン', 'Meta Superintelligence Labsを共同で率います(製品担当)。'),
 (W, '共同創業者', 'Miguel de Icaza', 'ミゲル・デ・イカザ', 'XimianとXamarinを共同創業。'),
 (W, '共同投資', 'Daniel Gross', 'ダニエル・グロス', 'AIへの投資(C2 Investments)。'),
 (O, '率いた会社', 'GitHub', 'GitHub', '2018年10月から2021年に、CEO。Microsoftが2018年6月に75億ドルで買収を発表。'),
 (O, '売却した会社', 'Xamarin', 'Xamarin', '2011年に共同創業、2016年にMicrosoftが買収。'),
 (O, '出身大学', 'MIT', 'MIT', '1999年に卒業(コンピュータ科学・数学)。'),
],
"""
k = "'Javier Olivan': ["
assert s.count(k) == 1
s = s.replace(k, add + k, 1)
open(p, 'w', encoding='utf-8').write(s)
import ast
ast.parse(b)
ast.parse(s)
print('ok')
