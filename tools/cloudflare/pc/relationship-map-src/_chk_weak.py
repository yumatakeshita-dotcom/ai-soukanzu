import json, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
def api(**p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(p), headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(30 if '429' in str(e) else 4 * (i + 1))
    return {}
d = json.load(open('top100_data.json', encoding='utf-8'))
W = ['Mark Chen', 'Koray Kavukcuoglu', 'Jared Kaplan', 'Aidan Gomez', 'Clement Delangue', 'Daniel Gross', 'Naval Ravikant', 'Bill Gurley', 'Jakub Pachocki', 'Jack Clark', 'Jan Leike', 'Garry Tan', 'Mary Meeker', 'Dylan Field', 'Alexandr Wang', 'Arthur Mensch', 'Kevin Scott', 'Ivan Zhao', 'Aravind Srinivas', 'Daniela Amodei', 'John Schulman']
qs = {e['en']: e['q'] for e in d if e['en'] in W}
ents = api(action='wbgetentities', format='json', ids='|'.join(qs.values()), props='claims|descriptions|sitelinks', languages='en').get('entities', {})
lab = {}
need = set()
for q, e in ents.items():
    for p in ('P108', 'P463', 'P69'):
        for st in e.get('claims', {}).get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if isinstance(v, dict) and v.get('id'):
                need.add(v['id'])
need = sorted(need)
for i in range(0, len(need), 50):
    for k, x in api(action='wbgetentities', format='json', ids='|'.join(need[i:i + 50]), props='labels', languages='en').get('entities', {}).items():
        lab[k] = x.get('labels', {}).get('en', {}).get('value', k)
for n, q in qs.items():
    e = ents.get(q, {})
    cl = e.get('claims', {})
    def labs(p):
        return [lab.get((s.get('mainsnak', {}).get('datavalue', {}) or {}).get('value', {}).get('id'), '?') for s in cl.get(p, [])][:5]
    by = [re.match(r'^[+-]?(\d{4})', s['mainsnak']['datavalue']['value']['time']).group(1) for s in cl.get('P569', []) if 'datavalue' in s['mainsnak']][:1]
    print(n, q, '|', (e.get('descriptions', {}).get('en') or {}).get('value'), '| 生', by, '| 勤務', labs('P108'), '| 所属', labs('P463'), '| 学', labs('P69'), '| 記事', list(e.get('sitelinks', {}).keys())[:3])
