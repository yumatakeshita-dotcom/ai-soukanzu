import json, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
Q = [('Susan Li', 'Meta chief financial officer'), ('Chris Cox', 'Meta chief product officer Facebook'), ('C. J. Mahoney', 'Meta chief legal officer'), ('John Arnold', 'billionaire Arnold Ventures Enron'),
     ('Charlie Songhurst', 'Microsoft strategy investor'), ('Brad Smith', 'Microsoft vice chair president'), ('Anat Ashkenazi', 'Alphabet CFO Eli Lilly'), ('Thomas Kurian', 'Google Cloud CEO Oracle'),
     ('Edith Cooper', 'Goldman Sachs Medley Amazon board'), ('Matt Garman', 'AWS CEO Amazon Web Services'), ('Doug Herrington', 'Amazon Worldwide Stores CEO'), ('Takeshi Numoto', 'Microsoft chief marketing officer'), ('Amy Coleman', 'Microsoft chief people officer')]
def g(u):
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read())
        except Exception as e: time.sleep(30 if '429' in str(e) else 3)
res = []
for name, ctx in Q:
    j = g('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': name + ' ' + ctx, 'gsrlimit': 3, 'prop': 'pageprops|extracts', 'ppprop': 'wikibase_item', 'exintro': 1, 'explaintext': 1, 'exchars': 160, 'formatversion': 2}))
    pages = sorted(((j or {}).get('query', {}).get('pages', [])), key=lambda p: p.get('index', 9))
    res.append({'name': name, 'cand': [(p['title'], p.get('pageprops', {}).get('wikibase_item', ''), (p.get('extract') or '')[:120].replace('\n', ' ')) for p in pages]})
    time.sleep(1)
json.dump(res, open('gafam_resolve2.json', 'w', encoding='utf-8'), ensure_ascii=False)
for r in res:
    print(r['name']); [print('   ', c) for c in r['cand']]
