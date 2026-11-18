"""注目の100人の、Wikidata番号(q)が本人のものか、見直す。
各人の「期待される所属・キーワード」を持っておき、紹介文・肩書き・年表のどれかに出てこない人を、疑わしいとして洗い出す。
使い方: python -I top100_audit.py"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(S, 'top100_data.json'), encoding='utf-8'))
K = {
 'Sam Altman': 'OpenAI|Y Combinator|オープンAI|Loopt', 'Greg Brockman': 'OpenAI|Stripe|オープンAI', 'Mira Murati': 'OpenAI|Thinking Machines|オープンAI', 'Ilya Sutskever': 'OpenAI|Google|Safe Superintelligence|トロント',
 'John Schulman': 'OpenAI|Anthropic|Thinking Machines|reinforcement', 'Jakub Pachocki': 'OpenAI|chief scientist|computer scientist', 'Mark Chen': 'OpenAI|artificial intelligence',
 'Sarah Friar': 'OpenAI|Nextdoor|Square|Goldman', 'Fidji Simo': 'OpenAI|Instacart|Facebook|Meta', 'Dario Amodei': 'Anthropic|OpenAI|アンソロピック', 'Daniela Amodei': 'Anthropic|OpenAI|Stripe',
 'Jared Kaplan': 'Anthropic|physicist|scientist|researcher', 'Jack Clark': 'Anthropic|OpenAI|journalist|ジャーナリスト', 'Mike Krieger': 'Instagram|Anthropic|Artifact', 'Jan Leike': 'Anthropic|OpenAI|DeepMind|safety',
 'Elon Musk': 'Tesla|SpaceX|xAI|テスラ', 'Demis Hassabis': 'DeepMind|ディープマインド|Isomorphic', 'Mustafa Suleyman': 'DeepMind|Inflection|Microsoft', 'Jeff Dean': 'Google|Alphabet',
 'Koray Kavukcuoglu': 'DeepMind|Google|researcher', 'Alexandr Wang': 'Scale|Meta|スケール', 'Yann LeCun': 'Meta|NYU|ニューヨーク|Facebook|チューリング|AMI', 'Arthur Mensch': 'Mistral|DeepMind|researcher',
 'Aravind Srinivas': 'Perplexity|OpenAI|パープレキシティ|AI', 'Aidan Gomez': 'Cohere|Google|researcher', 'Clement Delangue': 'Hugging|data|founder', 'Ali Ghodsi': 'Databricks|Berkeley|computer|scientist',
 'Andrej Karpathy': 'Tesla|OpenAI|Eureka|AI|スタンフォード', 'Liang Wenfeng': 'DeepSeek|深度求索|High-Flyer|幻方|梁文鋒', 'Sebastian Thrun': 'Google|Udacity|Stanford|Waymo|スタンフォード',
 'Sundar Pichai': 'Google|Alphabet|グーグル', 'Satya Nadella': 'Microsoft|マイクロソフト', 'Kevin Scott': 'Microsoft|LinkedIn|Chief Technology', 'Brad Smith': 'Microsoft|マイクロソフト',
 'Mark Zuckerberg': 'Meta|Facebook|フェイスブック', 'Tim Cook': 'Apple|アップル', 'Jeff Bezos': 'Amazon|アマゾン', 'Andy Jassy': 'Amazon|アマゾン', 'Jensen Huang': 'Nvidia|NVIDIA|エヌビディア|ジェンスン',
 'Lisa Su': 'AMD|Advanced Micro', 'Lip-Bu Tan': 'Intel|Cadence|インテル', 'Larry Ellison': 'Oracle|オラクル', 'Larry Page': 'Google|Alphabet|グーグル', 'Sergey Brin': 'Google|Alphabet|グーグル',
 'Bill Gates': 'Microsoft|マイクロソフト', 'Eric Schmidt': 'Google|Novell|グーグル|Sun', 'Palmer Luckey': 'Oculus|Anduril', 'Alex Karp': 'Palantir|パランティア', 'Marc Benioff': 'Salesforce|セールスフォース',
 'Michael Dell': 'Dell|デル', 'Bret Taylor': 'Sierra|Salesforce|OpenAI|Facebook|Google', 'Daniel Ek': 'Spotify|スポティファイ', 'Brian Chesky': 'Airbnb|エアビーアンドビー', 'Patrick Collison': 'Stripe|ストライプ',
 'John Collison': 'Stripe|ストライプ', 'Dylan Field': 'Figma|フィグマ', 'Ivan Zhao': 'Notion|ノーション', 'Travis Kalanick': 'Uber|ウーバー', 'Dara Khosrowshahi': 'Uber|Expedia|ウーバー', 'Jack Ma': 'Alibaba|アリババ|馬雲',
 'Marc Andreessen': 'Andreessen|Netscape|ネットスケープ|アンドリーセン', 'Ben Horowitz': 'Andreessen|Opsware|ホロウィッツ|Loudcloud', 'Peter Thiel': 'PayPal|Palantir|Facebook|ペイパル|ティール',
 'Reid Hoffman': 'LinkedIn|PayPal|リンクトイン|Greylock', 'Vinod Khosla': 'Sun Microsystems|Khosla|サン・マイクロシステムズ', 'Bill Gurley': 'Benchmark|venture', 'Paul Graham': 'Y Combinator|Viaweb|Lisp',
 'Jessica Livingston': 'Y Combinator', 'Garry Tan': 'Y Combinator|Posterous|Initialized|venture', 'Michael Moritz': 'Sequoia|セコイア', 'Mary Meeker': 'Kleiner|Morgan Stanley|Bond|analyst|venture',
 'Bill Ackman': 'Pershing|パーシング|hedge|ヘッジ', 'Warren Buffett': 'Berkshire|バークシャー', 'Daniel Gross': 'Safe Superintelligence|Y Combinator|Pioneer|AI|businessman|investor|実業家',
 'Nat Friedman': 'GitHub|ギットハブ|Xamarin', 'Masayoshi Son': 'ソフトバンク|SoftBank', 'Rajeev Misra': 'SoftBank|ソフトバンク|Deutsche|Vision Fund', 'Yuri Milner': 'DST|Mail.ru|Facebook',
 'Naval Ravikant': 'AngelList|Epinions|Vast|investor|entrepreneur', 'Mark Cuban': 'Dallas Mavericks|broadcast.com|Shark Tank|マーベリックス',
 'Hiroshi Mikitani': '楽天|Rakuten', 'Akio Toyoda': 'トヨタ|Toyota', 'Tadashi Yanai': 'ファーストリテイリング|ユニクロ|Fast Retailing|Uniqlo', 'Taizo Son': 'Mistletoe|孫泰蔵|ソフトバンク|ガンホー|Gungho|ミスルトウ',
 'Takafumi Horie': 'ライブドア|livedoor', 'Fumiaki Koizumi': 'メルカリ|Mercari', 'Shintaro Yamada': 'メルカリ|Mercari', 'Takeshi Idezawa': 'LINE|ライン', 'Ken Miyauchi': 'ソフトバンク|SoftBank',
 'Tomoko Namba': 'ディー・エヌ・エー|DeNA', 'Susumu Fujita': 'サイバーエージェント|CyberAgent', 'Daisuke Okanohara': 'Preferred|プリファード', 'Yutaka Matsuo': '東京大学|人工知能|AI',
 'Kentaro Kawabe': 'LINEヤフー|Yahoo|ヤフー|ZHD|Zホールディングス', 'Junichi Miyakawa': 'ソフトバンク|SoftBank', 'Takao Ozawa': 'ヤフー|Yahoo|楽天|クラウドワークス|ビズリーチ', 'Kenichiro Yoshida': 'ソニー|Sony',
 'Jack Dorsey': 'Twitter|Block|Square|ツイッター', 'Reed Hastings': 'Netflix|ネットフリックス', 'Evan Spiegel': 'Snap|スナップ',
}
bad, none = [], []
for e in d:
    en = e['en']
    kw = K.get(en)
    if not kw:
        none.append(en)
        continue
    if not e.get('q'):
        bad.append((en, '番号なし'))
        continue
    blob = ' '.join([e.get('desc') or '', e.get('intro') or '', ' '.join(t['label'] for t in e.get('timeline', []))])
    if not re.search(kw, blob, re.I):
        bad.append((en, e['q'], '肩書き: ' + (e.get('desc') or '-')[:40], '紹介: ' + (e.get('intro') or '-')[:50].replace('\n', ' ')))
print('期待の言葉を持たない人', none)
print('疑わしい(紹介文・肩書き・年表に、期待する会社名などが出てこない)', len(bad))
for b in bad:
    print(' -', *b)
