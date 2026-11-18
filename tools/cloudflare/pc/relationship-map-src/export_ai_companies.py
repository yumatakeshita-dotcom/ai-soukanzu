"""AI企業の一覧を書き出す(GAFAMは相関図で見ているので除く)。
元データ: ユニコーン一覧(Wikipedia)・Y Combinator公式ディレクトリ・日本のスタートアップ(東証/VC)・相関図の会社。
出力: output/ai-companies.csv (Excelで開けるUTF-8 BOMつき)
使い方: python -I export_ai_companies.py"""
import csv, json, os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
OUT = os.path.join(S, '..', '..', '..', 'output', 'ai-companies.csv')
GAFAM = {'google', 'alphabet', 'apple', 'meta', 'meta platforms', 'facebook', 'amazon', 'microsoft'}


def norm(s):
    s = re.sub(r'株式会社|\(株\)|㈱|Inc\.?|Corp\.?|Co\.,?\s*Ltd\.?|Ltd\.?|LLC|Labs?|Technologies|Technology|Holdings?', '', s or '')
    return re.sub(r'[^0-9a-zぁ-ヶ一-龥]', '', s.lower())


# 相関図に載っている会社
mapped = {}
from adds import apply_adds
CO_ALL = {}
for m, n in (('newco_data', 'CO'), ('newco_data2', 'CO2'), ('newco_data3', 'CO3'), ('newco_data4', 'CO4'), ('newco_data5', 'CO5'), ('newco_data6', 'CO6'), ('newco_data7', 'CO7'),
             ('newco_data7b', 'CO7B'), ('newco_data7c', 'CO7C'), ('newco_data8', 'CO8')):
    CO_ALL.update(getattr(__import__(m), n))
apply_adds(CO_ALL)
for k, c in CO_ALL.items():
    ce = next((x for x in c['N'] if x['id'] == c.get('center')), None)
    if ce:
        mapped[norm(ce['name'])] = k
for r in __import__('newco_data8').STARTUPS:
    mapped[norm(r['name'])] = r['key']
for nm in ('OpenAI', 'Anthropic', 'xAI', 'Meta', 'Thinking Machines Lab', 'Safe Superintelligence', 'Google DeepMind', 'Microsoft', 'Mistral AI', 'Sakana AI', 'Nvidia', 'Perplexity',
           'Cohere', 'Scale AI', 'Databricks', 'Hugging Face', 'Cursor', 'Notion', 'Figma', 'Stripe', 'Canva', 'Slack', 'PKSHA Technology', 'Preferred Networks'):
    mapped[norm(nm)] = 'core'
rows = {}


def add(name, country, kind, val, since, status, desc, url, src):
    k = norm(name)
    if not k or k in GAFAM or norm(name) in {norm(x) for x in GAFAM}:
        return
    r = rows.setdefault(k, {'会社名': name, '国・地域': country, '種別': set(), '評価額(億ドル)': '', '設立/選抜': since, '状態': status, '概要': '', '公式サイト': '', '相関図': '', '出典': set()})
    r['種別'].add(kind)
    r['出典'].add(src)
    if val and not r['評価額(億ドル)']:
        r['評価額(億ドル)'] = val
    if desc and len(desc) > len(r['概要']):
        r['概要'] = desc
    if url and not r['公式サイト']:
        r['公式サイト'] = url
    if country and not r['国・地域']:
        r['国・地域'] = country
    if status and not r['状態']:
        r['状態'] = status


for u in json.load(open(os.path.join(S, 'unicorns.json'), encoding='utf-8')):
    if re.search(r'artificial intelligence|machine learning|\bAI\b', u.get('i') or '', re.I):
        add(u['n'], ', '.join(u.get('c') or []), 'ユニコーン', u.get('v') or '', u.get('d') or '', '', '', '', 'Wikipedia ユニコーン一覧')
n_yc = 0
for r in json.load(open(os.path.join(S, 'yc_all.json'), encoding='utf-8')):
    tags = set(r.get('tags') or [])
    if tags & {'AI', 'Generative AI', 'Machine Learning', 'Computer Vision', 'Natural Language Processing', 'AI Assistant', 'AIOps', 'Conversational AI'} or re.search(r'\bAI\b', r.get('one_liner') or ''):
        loc = (r.get('all_locations') or '').split(',')[-1].strip()
        add(r['name'], loc, 'Y Combinator', '', r.get('batch') or '', {'Active': '活動中', 'Inactive': '休止', 'Acquired': '買収された', 'Public': '上場'}.get(r.get('status'), ''),
            (r.get('one_liner') or '')[:160], r.get('website') or '', 'Y Combinator公式ディレクトリ')
        n_yc += 1
for r in json.load(open(os.path.join(S, 'jp_startups.json'), encoding='utf-8')):
    if re.search(r'AI|人工知能|ＡＩ', r['n']) or re.search(r'artificial', r.get('ind') or '', re.I):
        add(r['n'], '日本', '日本のスタートアップ', '', str(r.get('est') or ''), r.get('mkt') or '', (r.get('ind') or ''), r.get('url') or '', '東証・VC・ニュースの記録')
for k, r in rows.items():
    r['相関図'] = '○' if k in mapped else ''
    r['種別'] = ' / '.join(sorted(r['種別']))
    r['出典'] = ' / '.join(sorted(r['出典']))
lst = sorted(rows.values(), key=lambda r: (r['相関図'] == '', -(float(r['評価額(億ドル)']) if r['評価額(億ドル)'] not in ('', None) else 0), r['会社名'].lower()))
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(lst[0].keys()))
    w.writeheader()
    w.writerows(lst)
print('AI企業', len(lst), '社 / 相関図にある', sum(1 for r in lst if r['相関図']), '社 / YC', n_yc, '社 →', os.path.abspath(OUT))
