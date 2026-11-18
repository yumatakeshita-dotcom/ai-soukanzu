# 手で追加するVC(Wikipediaに記事がない・薄い日本のVCなど)。投資先は、記事・公式発表で確認できたものだけ。
# 形: (キー, 英語名, 日本語名, 国, 種類, 説明, [投資先, ...])   投資先は、日本語の資金調達ニュースから毎日追加されます(fetch_sources.py の KNOWN_VC)。
EXTRA = [
 ('boost', 'Boost Capital', 'ブーストキャピタル', '日本', 'VC', '2024年設立の日本のVC。代表は小澤隆生氏。日本のITスタートアップに少額〜最大10億円を出資し、1号ファンド(LINEヤフーなどが出資)を運用。M&Aやバイアウトも手がける。ロンドンの「Boost Capital Partners」とは別の会社です。',
  ['ミライフグループ']),
 ('chibadojo', 'Chiba Dojo Fund', '千葉道場ファンド', '日本', 'VC', 'エンジェル投資家の千葉功太郎氏が率いる起業家コミュニティ「千葉道場」から生まれたVC。2019年に最初のファンドを組成し、2022年に3号ファンドを発表。',
  ['スペースマーケット', 'emole', 'ウェルスナビ', 'SmartNews', 'Kaminashi', 'Prossell Holdings', 'Treportal', 'ユートニック']),
 ('dronefund', 'Drone Fund', 'ドローンファンド', '日本', 'VC', '千葉功太郎氏と大前創希氏が運営する、ドローン・空飛ぶクルマなどエアモビリティ分野のVC。', []),
 ('genesia', 'Genesia Ventures', 'ジェネシア・ベンチャーズ', '日本', 'VC', '日本・インドネシア・ベトナム・インドに拠点を置く独立系のVC。', []),
 ('cacapital', 'CyberAgent Capital', 'サイバーエージェント・キャピタル', '日本', 'CVC', 'サイバーエージェントグループのVC。', []),
 ('realtech', 'Real Tech Fund', 'リアルテックファンド', '日本', 'VC', '大学・研究機関発の技術(リアルテック)を事業にするスタートアップに投資する日本のVC。', []),
 ('skyland', 'Skyland Ventures', 'スカイランドベンチャーズ', '日本', 'VC', '日本のシード・アーリー期のVC。', []),
 ('spiralcap', 'Spiral Capital', 'スパイラル・キャピタル', '日本', 'VC', '日本のVC。', []),
 ('xtech', 'XTech Ventures', 'エックステック・ベンチャーズ', '日本', 'VC', '日本のアーリー期のVC。', []),
 ('fenox', 'Fenox Venture Capital', 'フェノックス・ベンチャー・キャピタル', '日本', 'VC', '日本とアジアのスタートアップに投資するVC。', []),
 ('mtgv', 'MTG Ventures', 'MTGベンチャーズ', '日本', 'CVC', 'MTGグループのVC。', []),
 ('gumiv', 'gumi Ventures', 'gumiベンチャーズ', '日本', 'CVC', 'gumiグループのVC。', []),
 ('kuic', 'Kyoto University Innovation Capital', '京都大学イノベーションキャピタル', '日本', 'VC', '京都大学発のスタートアップに投資する大学系のVC。', []),
 ('miraicf', 'Mirai Creation Fund', 'ミライクリエーションファンド', '日本', 'VC', '日本のスタートアップに投資するVC。', []),
]
