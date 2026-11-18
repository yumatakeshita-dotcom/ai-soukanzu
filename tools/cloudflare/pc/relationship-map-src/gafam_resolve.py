"""gafam_names.txt の人物を、Wikidataの検索(wbsearchentities)で、人間(Q5)かつ説明に会社名か役職が合う候補だけにする。曖昧なものは決めずに出力する。"""
import json, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
def get(u):
    for i in range(5):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
        except Exception as e: time.sleep(20 if '429' in str(e) else 3)
out = []
for line in open('gafam_names.txt', encoding='utf-8'):
    co, name, role = line.strip().split('|')
    j = get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbsearchentities', 'search': name, 'language': 'en', 'type': 'item', 'limit': 6, 'format': 'json'}))
    c = [(x['id'], x.get('description', '')) for x in (j or {}).get('search', [])]
    out.append({'co': co, 'name': name, 'role': role, 'cand': c}); time.sleep(1)
json.dump(out, open('gafam_resolve.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out: print(o['co'], o['name'], o['cand'][:3])
