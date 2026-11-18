import re, ast
# ---- adds.py: OpenAIの人物の説明(patch)と経歴(career) ----
p = 'adds.py'
a = open(p, encoding='utf-8').read()
PATCH = {
 'altman': '1985年シカゴ生まれ。2005年にスタンフォード大学を中退(2年在籍)し、同年にLooptを共同創業してCEOに(2012年3月にGreen Dotが4,340万ドルで買収)。2011年にY Combinatorのパートナー、2014年2月にポール・グレアムの後任で社長(2019年3月に退任)。2014年にはRedditのCEOを8日間務めました。2015年にOpenAIを共同創業し、2019年3月に専任CEOに。2023年11月17日に取締役会に解任され、同月21日までに復帰が決まりました(従業員約770人のうち700人超が、復帰を求める書簡に署名)。2024年2月にマスクに提訴され、2026年5月に陪審が、時効を理由にマスクの請求を退けました。Helion Energyの会長、Worldcoin(Tools for Humanity)の共同創業者でもあります。',
 'brockman': '1987年ノースダコタ州生まれ。ハーバード大学、のちMITに進み、2010年にMITを中退してStripeへ(2013年に初代CTO)。2015年5月にStripeを離れ、同年12月にOpenAIを共同創業(最初は自宅の居間で活動し、創業チームの採用を率いました)。2023年11月17日に、アルトマン解任に合わせて退社を表明し、数日後に復帰。2024年8〜11月は休職。2026年には、フィジー・シモの休職後、製品を含む役割を引き継ぎました。2019年11月に結婚(スツケバーが司式)。AI関連の政治団体などへの高額の寄付が報じられています(額・年の記載は資料で食い違っています)。',
 'pachocki': '1991年、ポーランドのグダニスク生まれ。ワルシャワ大学を出て、カーネギーメロン大学で博士号(指導教官はゲイリー・ミラー)。2012年にGoogle Code Jamで優勝し、ICPC世界大会では銀メダル。ハーバード大学とシモンズ研究所のポスドクを経て、2017年にOpenAIに入社。2021年に研究ディレクターとして、GPT-4とOpenAI Fiveの開発を率い、2024年5月に、スツケバーの退社後のチーフサイエンティストに(アルトマンは「世代を代表する頭脳の一人」と評しました)。',
 'friar': '1972年、北アイルランド生まれ。オックスフォード大学で冶金学・経済・経営を学び、スタンフォードでMBA。Arthur Andersen、McKinsey、Goldman Sachs(エクイティリサーチ)、Salesforceを経て、Squareの初代CFO(2012〜2018年)、Nextdoor CEO(2018〜2024年、2021年にSPACで上場)。2024年6月にOpenAIの初代CFOに就任(Reutersが同年6月10日に報道)。WalmartとConsenSysの取締役。2019年にOBE(大英帝国勲章)、2026年にTime100に選ばれました。',
 'simo': '1985年、フランス・セート生まれ。HEC Paris卒。eBay(2007〜2011年)を経て2011年にFacebookへ入り、約10年、Facebookアプリの責任者(VP)。2021年7月にInstacartのCEO(2023年9月の上場後は取締役会長)。2024年3月にOpenAIの取締役、2025年5月に、最初の「アプリケーション担当CEO」として発表され、同年8月に就任(のち「AGIデプロイメント担当CEO」に改称)。2026年1月にChatGPT Healthを主導。2026年7月にフルタイムを退き、非常勤のアドバイザーになったと報じられています。Shopifyの取締役、Metrodora Instituteの共同創業者。',
}
CAREER = {
 'altman': [['1985', 'シカゴに生まれる'], ['2005', 'スタンフォード大学を中退し、Looptを共同創業'], ['2012', '3月、Looptを、Green Dotが買収'], ['2014', 'Y Combinatorの社長に(〜2019年)'], ['2015', 'OpenAIを共同創業'], ['2019', '3月、専任のCEOに'], ['2023', '11月17日に解任、21日までに復帰が決まる'], ['2024', '2月、マスクが提訴'], ['2026', '5月、陪審がマスクの請求を、時効を理由に退ける']],
 'brockman': [['1987', 'ノースダコタ州に生まれる'], ['2010', 'MITを中退し、Stripeへ(2013年に初代CTO)'], ['2015', '5月にStripeを離れ、12月にOpenAIを共同創業'], ['2019', '11月に結婚(スツケバーが司式)'], ['2023', '11月17日に退社を表明、数日後に復帰'], ['2024', '8〜11月、休職'], ['2026', 'シモの休職後、製品を含む役割を引き継ぐ']],
 'pachocki': [['1991', 'ポーランドのグダニスクに生まれる'], ['2012', 'Google Code Jamで優勝'], ['2017', 'OpenAIに入社'], ['2021', '研究ディレクターに(GPT-4、OpenAI Five)'], ['2024', '5月、チーフサイエンティストに']],
 'friar': [['2012', 'Squareの初代CFOに(〜2018年)'], ['2018', 'Nextdoor CEOに(〜2024年)'], ['2021', 'NextdoorがSPACで上場'], ['2024', '6月、OpenAIの初代CFOに']],
 'simo': [['2007', 'eBayに入社(〜2011年)'], ['2011', 'Facebookに入社'], ['2021', '7月、InstacartのCEOに'], ['2024', '3月、OpenAIの取締役に'], ['2025', '8月、アプリケーション担当CEOに就任'], ['2026', '1月にChatGPT Healthを主導。7月にフルタイムを退くと報じられる']],
}
i = a.index(" 'openai': dict(")
j = a.index("\n 'anthropic': dict(", i)
blk = a[i:j]
if "patch=" not in blk and 'career=' not in blk:
    k = blk.rindex('edges=')
    blk2 = blk[:k] + 'patch=%r,\n  career=%r,\n  ' % (PATCH, CAREER) + blk[k:]
    a = a[:i] + blk2 + a[j:]
old = "out[k] = {'nodes': a['nodes'], 'en': a['en'], 'patch': a.get('patch', {}), 'edges': LEGACY_EDGES[k]}"
assert old in a
a = a.replace(old, "out[k] = {'nodes': a['nodes'], 'en': a['en'], 'patch': a.get('patch', {}), 'career': a.get('career', {}), 'edges': LEGACY_EDGES[k]}", 1)
ast.parse(a)
open(p, 'w', encoding='utf-8').write(a)
# ---- hub_template.html: LEGACYの経歴を使う ----
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
old = "  Object.assign(d.EN,L.en||{});"
assert t.count(old) == 1
t = t.replace(old, old + "Object.assign(d.CAREER,L.career||{});", 1)
open(p, 'w', encoding='utf-8').write(t)
# ---- _merge_insta.py: 公開版のapplyLegacyにも、同じ1行を足す ----
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
if 'L.career' not in g:
    old = "out = '\\n'.join(ls)\n# 5. AIWD"
    new = """out = '\\n'.join(ls)
# 5-. OpenAIなどの図の追加分(LEGACY)に、経歴(career)も使う
_k = "  Object.assign(d.EN,L.en||{});"
if _k in out and "L.career" not in out:
    out = out.replace(_k, _k + "Object.assign(d.CAREER,L.career||{});", 1)
# 5. AIWD"""
    assert old in g
    g = g.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(g)
    ast.parse(g)
print('ok')
