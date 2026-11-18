import ast
p = 'adds.py'
a = open(p, encoding='utf-8').read()
PATCH = {
 'dario': {'desc': '1983年、サンフランシスコ生まれ。カリフォルニア工科大学からスタンフォード大学へ移り、2006年に物理学の学士、2011年にプリンストン大学で生物物理学・計算神経科学の博士号。2014年11月〜2015年10月にBaidu、2015年にGoogle Brain、2016年にOpenAIへ(AI安全のチームとスケーリング則のチームを率い、GPT-2、GPT-3、人間のフィードバックによる強化学習に貢献)。2020年に、ブロックマンやアルトマンとの対立の末、妹ダニエラらとOpenAIを離れ、2021年にAnthropicを共同創業しました。2023年11月に、OpenAIの取締役会から、アルトマンの後任と合併を打診されましたが、断りました。2024年10月にエッセイ「Machines of Loving Grace」、2026年1月に「The Adolescence of Technology」を発表。2026年2月、大量の国内監視や完全自律兵器へのClaudeの使用を禁じる契約条項を外すことを拒み、国防総省が「サプライチェーン上のリスク」と指定したと報じられ、3月26日に連邦地裁が一時差止めを命じました。'},
 'daniela': {'desc': '1987年、サンフランシスコ生まれ。UCサンタクルーズで英文学を学び、政治・国際保健の分野を経て、ペンシルベニア州選出の下院議員の広報を担当。2013年にStripeに初期の社員として入社し、2018年にOpenAIへ(GPT-2の開発期のチームを管理し、のち安全・政策担当VP)。兄ダリオらとOpenAIを離れ、Anthropicの共同創業者で社長に(離れた時期は、資料により2020年または2021年)。安全性とモデルの整合性のチームを率います。2023年9月に、ダリオとともにTimeの「AI分野で最も影響力のある100人」に選ばれました。'},
 'kaplan': {'desc': 'イリノイ数学科学アカデミーを2001年に卒業。スタンフォード大学で物理学・数学の学士、ハーバード大学で物理学の博士号(2009年、指導教官はニマ・アルカニ=ハメド)。SLACとスタンフォードでポスドクを経て、2012年からジョンズ・ホプキンス大学の物理学の教員(現在は准教授と記載)。2019年にOpenAIの研究者となり、2020年1月に「Scaling Laws for Neural Language Models」を共著、GPT-3の論文にも参加。Anthropicの共同創業者でチーフサイエンス・オフィサー。2024年10月に「Responsible Scaling Officer」に就くと発表されました。2025年12月のGuardianのインタビューで、AIに自分自身を改良させるかどうかを、2030年までに人類が決める必要があると述べました。'},
 'clark': {'desc': 'Anthropicの共同創業者(法人化は2021年1月26日)。肩書きは「共同創業者、公益担当責任者(Head of Public Benefit)、元・政策責任者」。2026年3月に発足した、AIを研究するシンクタンク「Anthropic Institute」を率います。元ジャーナリスト(Bloomberg、The Register)で、OpenAIの政策ディレクターを務めたのち、Anthropicへ。ニュースレター「Import AI」の発行者でもあります。'},
 'olah': {'desc': '1991〜92年ごろ、カナダ生まれ(Forbesによる)。トロントの大学で数学を1年学んで中退し、2012年にティール・フェローシップを得ました。2015年にGoogle Brainのインターン、のち研究者(DeepDreamなど、ニューラルネットの可視化に関与)。2017年3月に、機械学習の解説誌「Distill」を共同創刊。2018年にOpenAIの解釈可能性チームの責任者になり、2020年にOpenAIを離れ、Anthropicを共同創業。2024年5月には、モデルの内部の「特徴」を地図にする成果が報じられました。2025年にForbesが、Anthropicの持ち株で億万長者になったと報じています。'},
 'leike': {'desc': '1986または87年生まれ。フライブルク大学で学び、オーストラリア国立大学で機械学習の博士号(指導教官はマーカス・ハッター)。人類の未来研究所のポスドクを経てDeepMindでAI安全の実証研究に。2021年にOpenAIへ入り、2023年にスツケバーとともに「スーパーアラインメント」の共同責任者になりました。2024年5月に退社を表明し、安全の文化と手順が、華やかな製品の後回しになってきたと書き、経営陣への信頼を徐々に失ったと述べました。同月、Anthropicに参加しました(The Vergeの報道は5月28日)。'},
}
CAREER = {
 'dario': [['1983', 'サンフランシスコに生まれる'], ['2006', 'スタンフォード大学を卒業(物理学)'], ['2011', 'プリンストン大学で博士号'], ['2014', '11月、Baiduへ(〜2015年10月)'], ['2015', 'Google Brainへ'], ['2016', 'OpenAIへ(AI安全・スケーリング則を率いる)'], ['2020', 'OpenAIを離れる'], ['2021', 'Anthropicを共同創業'], ['2023', '11月、OpenAIの取締役会からの打診を断る'], ['2024', '10月、エッセイ「Machines of Loving Grace」'], ['2026', '1月にエッセイ。2月に国防総省と対立、3月に連邦地裁が一時差止め']],
 'daniela': [['2013', 'Stripeに入社'], ['2018', 'OpenAIへ(のち安全・政策担当VP)'], ['2021', 'Anthropicを共同創業(社長)'], ['2023', '9月、Time「AI分野の100人」に']],
 'kaplan': [['2009', 'ハーバード大学で博士号'], ['2012', 'ジョンズ・ホプキンス大学の物理学の教員に'], ['2019', 'OpenAIの研究者に'], ['2020', '1月、スケーリング則の論文を共著'], ['2021', 'Anthropicを共同創業(チーフサイエンス・オフィサー)'], ['2024', '10月、Responsible Scaling Officerに']],
 'clark': [['〜', 'ジャーナリスト(Bloomberg、The Register)を経て、OpenAIの政策ディレクターに'], ['2021', 'Anthropicを共同創業'], ['2026', '3月、Anthropic Instituteを率いる']],
 'olah': [['2012', 'ティール・フェローシップ'], ['2015', 'Google Brainに'], ['2017', '3月、Distillを共同創刊'], ['2018', 'OpenAIの解釈可能性チームの責任者に'], ['2020', 'OpenAIを離れる'], ['2021', 'Anthropicを共同創業'], ['2024', '5月、モデルの特徴を地図化する成果']],
 'leike': [['2021', 'OpenAIに入社'], ['2023', 'スーパーアラインメントの共同責任者に'], ['2024', '5月、OpenAIを退社し、Anthropicに参加']],
}
i = a.index(" 'anthropic': dict(")
j = a.index("\n 'xai': dict(", i)
blk = a[i:j]
if 'career=' not in blk:
    k = blk.rindex('edges=')
    pre = blk[:k]
    if 'patch=' in pre:
        # 既存のpatchに足す
        pk = pre.index('patch=')
        pe = pre.index('\n', pk)
        pre = pre[:pk] + pre[pk:pe].rstrip(',') + ',\n' + pre[pe:]
    blk2 = blk[:k] + ('patch=%r,\n  ' % PATCH if 'patch=' not in blk else '') + 'career=%r,\n  ' % CAREER + blk[k:]
    a = a[:i] + blk2 + a[j:]
ast.parse(a)
open(p, 'w', encoding='utf-8').write(a)
import importlib
import adds
importlib.reload(adds)
print(list(adds.ADDS['anthropic'].keys()), list(adds.ADDS['anthropic']['patch']), list(adds.ADDS['anthropic']['career']))
