"""ai_wikidata.json(Wikidataから集めたAI分野の会社と、創業者・出資者・CEO・親会社)から、相関図にまだない会社を選び、
ai_wd_maps.json(newco_data10w.py が読み込んで、スタートアップの図にする)を作る。
選ぶ基準: ①名前がある(Q番号だけでない) ②創業者・出資者・CEO・親会社のどれかの記録がある ③相関図・GAFAMにない。記録の多い順に、最大 LIMIT 社。
使い方: python -I ai_wd_to_maps.py [LIMIT]"""
import json, os, re, sys, unicodedata
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300
GAFAM = {'google', 'alphabet', 'apple', 'meta', 'metaplatforms', 'facebook', 'amazon', 'microsoft'}


def norm(s):
    s = re.sub(r'株式会社|\(株\)|㈱|Inc\.?|Corp\.?|Co\.,?\s*Ltd\.?|Ltd\.?|LLC|Labs?|Technologies|Technology|Holdings?', '', s or '')
    return re.sub(r'[^0-9a-zぁ-ヶ一-龥]', '', s.lower())


mapped = set(GAFAM)
from adds import apply_adds
CO_ALL = {}
for m, n in (('newco_data', 'CO'), ('newco_data2', 'CO2'), ('newco_data3', 'CO3'), ('newco_data4', 'CO4'), ('newco_data5', 'CO5'), ('newco_data6', 'CO6'), ('newco_data7', 'CO7'),
             ('newco_data7b', 'CO7B'), ('newco_data7c', 'CO7C'), ('newco_data7d', 'CO7D'), ('newco_data7e', 'CO7E'), ('newco_data7f', 'CO7F'), ('newco_data8', 'CO8')):
    CO_ALL.update(getattr(__import__(m), n))
apply_adds(CO_ALL)
for k, c in CO_ALL.items():
    if k.startswith('stw_'):
        continue
    ce = next((x for x in c['N'] if x['id'] == c.get('center')), None)
    if ce:
        mapped.add(norm(ce['name']))
for r in __import__('newco_data8').STARTUPS:
    mapped.add(norm(r['name']))
for nm_ in ('OpenAI', 'Anthropic', 'xAI', 'Meta', 'Thinking Machines Lab', 'Safe Superintelligence', 'Google DeepMind', 'DeepMind', 'Microsoft', 'Mistral AI', 'Sakana AI', 'Nvidia', 'Perplexity', 'Cohere', 'Scale AI',
            'Databricks', 'Hugging Face', 'Cursor', 'Notion', 'Figma', 'Stripe', 'Canva', 'Slack', 'PKSHA Technology', 'Preferred Networks', 'Anduril', 'Instagram', 'WhatsApp'):
    mapped.add(norm(nm_))
LONG = [m for m in mapped if len(m) >= 7]
d = json.load(open(os.path.join(S, 'ai_wikidata.json'), encoding='utf-8'))
isq = lambda s: bool(re.fullmatch(r'Q\d+', s or ''))
cand = []
for q, c in d['cos'].items():
    nm = (c.get('name') or '').strip()
    if not nm or isq(nm) or norm(nm) in mapped or len(norm(nm)) < 2 or any(norm(nm).startswith(m) for m in LONG):
        continue
    rels = [r for r in d['rel'].get(q, []) if r.get('name') and not isq(r['name'])]
    if not rels:
        continue
    cand.append((len(rels), q, nm, c, rels))
cand.sort(key=lambda x: (-x[0], x[2]))
out = []
for n, q, nm, c, rels in cand[:LIMIT]:
    year = int(c['inc']) if (c.get('inc') or '').isdigit() else 2000
    items = {'p': [], 'i': [], 'o': []}
    seen = set()
    for r in rels:
        key = (r['p'], r['rel'])
        if key in seen:
            continue
        seen.add(key)
        if r['rel'] in ('創業者', 'CEO'):
            items['p'].append(r)
        elif r['rel'] == '出資者':
            items['i'].append(r)
        else:
            items['o'].append(r)
    out.append({'q': q, 'name': nm, 'year': year, 'web': c.get('web', ''), 'p': items['p'][:8], 'i': items['i'][:8], 'o': items['o'][:3]})
# ---- Y Combinatorの公式ディレクトリ(yc_founders.json)から ----
yp = os.path.join(S, 'yc_founders.json')
nyc = 0
if os.path.exists(yp):
    seen = {norm(x['name']) for x in out}
    ycid = {r['slug']: r.get('id') for r in json.load(open(os.path.join(S, 'yc_all.json'), encoding='utf-8'))}
    rows = []
    for slug, v in json.load(open(yp, encoding='utf-8')).items():
        nm = (v.get('name') or '').strip()
        k = norm(nm)
        if v.get('err') or not v.get('founders') or not nm or len(k) < 2 or k in mapped or k in seen or any(k.startswith(m) for m in LONG):
            continue
        rows.append((v.get('status') != 'Active' and v.get('status') != 'Public', nm, slug, v))
    rows.sort(key=lambda x: (x[0], x[1].lower()))
    for _, nm, slug, v in rows:
        seen.add(norm(nm))
        yr = v.get('year') if isinstance(v.get('year'), int) and v.get('year') > 1990 else 2000
        out.append({'q': 'Y%s' % ycid.get(slug, slug), 'name': nm, 'year': yr, 'web': v.get('web') or '',
                    'p': [{'p': 'y%d' % i, 'name': f['n'], 'rel': ('CEO' if 'CEO' in (f.get('t') or '') else '創業者'), 't': f.get('t') or ''} for i, f in enumerate(v['founders'])],
                    'i': [], 'o': [], 'yc': {'b': v.get('batch') or '', 'one': v.get('one') or '', 'loc': v.get('loc') or '', 'team': v.get('team'), 'st': v.get('status') or ''}})
        nyc += 1
CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
out = out[:CAP]
print('Y Combinatorから', nyc, '社 / 公開版に入れる', len(out), '社(上限 %d)' % CAP)
json.dump(out, open(os.path.join(S, 'ai_wd_maps.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('候補', len(cand), '社 → 図にする', len(out), '社 / 創業者・CEO', sum(len(x['p']) for x in out), '人 / 出資者', sum(len(x['i']) for x in out))
