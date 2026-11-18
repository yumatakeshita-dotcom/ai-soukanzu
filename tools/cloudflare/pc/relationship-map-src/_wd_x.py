import json, sys, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
def get(u):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
for name in ['Javier Olivan', 'Jan Koum', 'Brian Acton', 'Kevin Systrom', 'Behnam Neyshabur', 'Liam Fedus', 'Alex LeBrun', 'Sarah Wynn-Williams']:
    r = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbsearchentities', 'search': name, 'language': 'en', 'format': 'json', 'limit': 3}))
    for h in r.get('search', [])[:2]:
        q = h['id']
        e = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'ids': q, 'props': 'claims|descriptions', 'format': 'json'}))['entities'][q]
        cl = e.get('claims', {})
        x = [s['mainsnak']['datavalue']['value'] for s in cl.get('P2002', []) if 'datavalue' in s['mainsnak']]
        ig = [s['mainsnak']['datavalue']['value'] for s in cl.get('P2003', []) if 'datavalue' in s['mainsnak']]
        print(name, q, (e.get('descriptions', {}).get('en') or {}).get('value'), 'X:', x, 'IG:', ig)
