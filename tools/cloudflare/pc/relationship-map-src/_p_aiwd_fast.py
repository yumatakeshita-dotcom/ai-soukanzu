"""ai_wikidata.py の関係の取得を、「相関図にまだない会社」だけに絞る(すでにある会社を調べる時間を省く)。
取得済みの分は、st['relq'](問い合わせ済みの会社)に移して、続きから再開できるようにする。"""
import json, os, re, subprocess, sys, time
S = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(S, 'ai_wikidata.py')
s = open(p, encoding='utf-8').read()
old = s[s.index("# ② 関係"):]
new = '''# ② 関係(創業者 P112・出資者 P1951・CEO P169・親会社 P749)。相関図にまだない会社だけを調べる
sys.path.insert(0, S)
import ai_wd_filter
st.setdefault('relq', [])
if not st['relq']:
    allids = sorted(st['cos'])
    for k in st['done']:
        if k.startswith('rel:'):
            i0 = int(k[4:])
            st['relq'] += allids[i0:i0 + 60]
need = [q for q in ai_wd_filter.unmapped(st['cos']) if q not in set(st['relq'])]
print('これから調べる会社', len(need), '社(相関図にない会社だけ)', flush=True)
for i in range(0, len(need), 60):
    ch = need[i:i + 60]
    q = ('SELECT ?c ?p ?pLabel ?rel WHERE { VALUES ?c {%s} '
         '{ ?c wdt:P112 ?p. BIND("創業者" AS ?rel) } UNION { ?c wdt:P1951 ?p. BIND("出資者" AS ?rel) } UNION { ?c wdt:P169 ?p. BIND("CEO" AS ?rel) } UNION { ?c wdt:P749 ?p. BIND("親会社" AS ?rel) } '
         'SERVICE wikibase:label { bd:serviceParam wikibase:language "ja,en". } }') % ' '.join('wd:' + x for x in ch)
    rows = sparql(q)
    time.sleep(65)
    if rows is None:
        continue
    for b in rows:
        c = b['c']['value'].rsplit('/', 1)[-1]
        pp = b['p']['value'].rsplit('/', 1)[-1]
        lst = st['rel'].setdefault(c, [])
        r = {'p': pp, 'name': b['pLabel']['value'], 'rel': b['rel']['value']}
        if r not in lst:
            lst.append(r)
    st['relq'] += ch
    save()
    print('関係', i + len(ch), '/', len(need), flush=True)
print('完了: 会社', len(st['cos']), '社 / 関係のある会社', len(st['rel']), flush=True)
'''
s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
open(os.path.join(S, 'ai_wd_filter.py'), 'w', encoding='utf-8').write('''"""相関図にまだない会社のQ番号だけを返す(ai_wd_to_maps.py と同じ基準)。"""
import os, re, sys
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)


def norm(s):
    s = re.sub(r'株式会社|\\(株\\)|㈱|Inc\\.?|Corp\\.?|Co\\.,?\\s*Ltd\\.?|Ltd\\.?|LLC|Labs?|Technologies|Technology|Holdings?', '', s or '')
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
        if not nm or re.fullmatch(r'Q\\d+', nm) or len(k) < 2 or k in mapped or any(k.startswith(m) for m in LONG):
            continue
        out.append(q)
    return out
''')
print('ok')
