"""相関図にまだない会社のQ番号だけを返す(ai_wd_to_maps.py と同じ基準)。"""
import os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)


def norm(s):
    s = re.sub(r'株式会社|\(株\)|㈱|Inc\.?|Corp\.?|Co\.,?\s*Ltd\.?|Ltd\.?|LLC|Labs?|Technologies|Technology|Holdings?', '', s or '')
    return re.sub(r'[^0-9a-zぁ-ヶ一-龥]', '', s.lower())


def unmapped(cos):
    mapped = {'google', 'alphabet', 'apple', 'meta', 'metaplatforms', 'facebook', 'amazon', 'microsoft'}
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
    for n in ('OpenAI', 'Anthropic', 'xAI', 'Meta', 'Thinking Machines Lab', 'Safe Superintelligence', 'Google DeepMind', 'DeepMind', 'Microsoft', 'Mistral AI', 'Sakana AI', 'Nvidia', 'Perplexity', 'Cohere', 'Scale AI',
              'Databricks', 'Hugging Face', 'Cursor', 'Notion', 'Figma', 'Stripe', 'Canva', 'Slack', 'PKSHA Technology', 'Preferred Networks', 'Anduril', 'Instagram', 'WhatsApp'):
        mapped.add(norm(n))
    LONG = [m for m in mapped if len(m) >= 7]
    out = []
    for q, c in sorted(cos.items()):
        nm = (c.get('name') or '').strip()
        k = norm(nm)
        if not nm or re.fullmatch(r'Q\d+', nm) or len(k) < 2 or k in mapped or any(k.startswith(m) for m in LONG):
            continue
        out.append(q)
    return out
