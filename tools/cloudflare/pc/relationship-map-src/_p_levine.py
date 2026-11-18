BS = chr(92)
NL = BS + 'n'
# ---- Metaの図 ----
p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
node = " {'id': 'levine', 'name': 'マーン・レヴィン', 'kind': 'p', 'from': 2013, 'to': 2023, 'desc': '元チーフ・ビジネス・オフィサー。米財務省(1993〜2000年)、ハーバード大学のサマーズ学長の首席補佐官(2001〜2003年)、オバマ政権の国家経済会議の首席補佐官(2009〜2010年)を経て、2010年にFacebookへ。グローバル公共政策のVP(2010〜2014年)、2014年にInstagramの初代COO、2018年にFacebookへ戻ってグローバル・パートナーシップ等のVP、2021年6月にチーフ・ビジネス・オフィサーに就き、2023年2月に退任しました。サンドバーグが創設したLean Inの取締役も務めました。', 'role': '元チーフ・ビジネス・オフィサー(2021〜2023年)'},\n"
a = " {'id': 'vanguard', 'name': 'Vanguard'"
assert b.count(a) == 1
b = b.replace(a, node + a, 1)
anchor = "E.push({a:'olivan',b:'sandberg',k:'link',label:'2022年に後任',since:2022});" + NL
assert b.count(anchor) == 1
b = b.replace(anchor, anchor + "E.push({a:'levine',b:'instagram',k:'from',label:'初代COO(2014年)'});" + NL + "E.push({a:'levine',b:'sandberg',k:'link',label:'Lean In取締役'});" + NL, 1)
b = b.replace("'olivan': 'Javier Olivan',", "'olivan': 'Javier Olivan', 'levine': 'Marne Levine',", 1)
k2 = "      'olivan': [['出典: Wikipedia(Javier Oliván)'"
assert b.count(k2) == 1
b = b.replace(k2, "      'levine': [['出典: Wikipedia(Marne Levine)', 'https://en.wikipedia.org/wiki/Marne_Levine'], ['公式Instagram(プロフィールが「元Meta CBO」と一致)', 'https://www.instagram.com/marnelevine/']],\n" + k2, 1)
b = b.replace("'olivan': [['1977', 'スペインに生まれる']", "'levine': [['1993', '米財務省に入る(〜2000年)'], ['2001', 'ハーバード大学のサマーズ学長の首席補佐官(〜2003年)'], ['2009', 'オバマ政権の国家経済会議の首席補佐官(〜2010年)'], ['2010', 'Facebookのグローバル公共政策VPに(〜2014年)'], ['2014', 'Instagramの初代COOに'], ['2018', 'Facebookに戻り、グローバル・パートナーシップ等のVPに'], ['2021', '6月、チーフ・ビジネス・オフィサーに'], ['2023', '2月に退任']],\n 'olivan': [['1977', 'スペインに生まれる']", 1)
open(p, 'w', encoding='utf-8').write(b)
# ---- Instagramの図 ----
p = 'newco_data7c.py'
c = open(p, encoding='utf-8').read()
n = " {'id': 'levine', 'name': 'マーン・レヴィン', 'kind': 'p', 'from': 2014, 'desc': 'Instagramの初代COO(2014年)。それ以前はFacebookのグローバル公共政策のVP(2010〜2014年)。2018年にFacebookへ戻り、2021年にチーフ・ビジネス・オフィサー、2023年2月に退任。', 'role': '初代COO(2014年〜)'},\n"
k = " {'id': 'walmart', 'name': 'Walmart'"
assert c.count(k) == 1
c = c.replace(k, n + k, 1)
c = c.replace("'mosseri': 'Adam Mosseri', 'zuckerberg': 'Mark Zuckerberg'}", "'mosseri': 'Adam Mosseri', 'zuckerberg': 'Mark Zuckerberg', 'levine': 'Marne Levine'}", 1)
c = c.replace("    'mosseri': [WPI],", "    'mosseri': [WPI],\n    'levine': [['出典: Wikipedia(Marne Levine)', 'https://en.wikipedia.org/wiki/Marne_Levine'], ['公式Instagram', 'https://www.instagram.com/marnelevine/']],", 1)
open(p, 'w', encoding='utf-8').write(c)
# ---- 人物の相関図 ----
p = 'personal_data.py'
s = open(p, encoding='utf-8').read()
a = " (F, '妹', 'Donna Zuckerberg', 'ドナ・ザッカーバーグ', '古典学者。'),"
assert a in s
s = s.replace(a, a + "\n (F, '妹', 'Arielle Zuckerberg', 'アリエル・ザッカーバーグ', 'ベンチャーキャピタリスト(Long Journey Ventures)。Instagramのプロフィールに「Early-stage VC」と記載(@az)。'),", 1)
add = """'Marne Levine': [
 (W, '元の上司(CEO)', 'Mark Zuckerberg', 'マーク・ザッカーバーグ', 'Facebook(Meta)のチーフ・ビジネス・オフィサー(2021〜2023年)として、CEOの下で働きました。'),
 (W, '同僚・取締役仲間', 'Sheryl Sandberg', 'シェリル・サンドバーグ', 'サンドバーグが創設した非営利団体Lean Inの取締役を務めました。'),
 (W, '前の上司', 'Larry Summers', 'ラリー・サマーズ', 'ハーバード大学の学長だった2001〜2003年に、首席補佐官を務めました。'),
 (W, '2009年の上司', 'Barack Obama', 'バラク・オバマ', '2009〜2010年に、国家経済会議の首席補佐官・大統領特別補佐官(経済政策)を務めました。'),
 (O, '所属(2014年)', 'Instagram', 'Instagram', '初代COO。'),
 (O, '最初の勤め先', 'U.S. Department of the Treasury', '米財務省', '1993〜2000年に、アジア通貨危機などに取り組みました。'),
],
"""
k = "'Javier Olivan': ["
assert s.count(k) == 1
s = s.replace(k, add + k, 1)
open(p, 'w', encoding='utf-8').write(s)
print('ok')
