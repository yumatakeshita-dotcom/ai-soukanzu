import json, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
def get(u):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(20 * (i + 1))
    return {}
for name in ['computer vision', 'natural language processing', 'deep learning', 'generative artificial intelligence', 'robotics', 'speech recognition', 'chatbot', 'autonomous car', 'data science', 'large language model', 'machine vision', 'computer science', 'software industry']:
    r = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbsearchentities', 'search': name, 'language': 'en', 'format': 'json', 'limit': 2}))
    print(name, [(h['id'], h.get('description', '')[:40]) for h in r.get('search', [])])
    time.sleep(2)
