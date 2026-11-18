import json, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
def get(u):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(15 * (i + 1))
    return {}
for name, ctx in (('山田進太郎', 'メルカリ'), ('川邊健太郎', 'LINEヤフー'), ('松尾豊', '東京大学 人工知能'), ('小泉文明', 'メルカリ'), ('小澤隆生', 'ヤフー')):
    r = get('https://ja.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'list': 'search', 'srsearch': name + ' ' + ctx, 'srlimit': 4, 'formatversion': 2}))
    ts = [x['title'] for x in r.get('query', {}).get('search', [])]
    if not ts:
        print(name, 'なし'); continue
    r2 = get('https://ja.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'pageprops|extracts', 'ppprop': 'wikibase_item', 'exintro': 1, 'explaintext': 1, 'exlimit': 4, 'redirects': 1, 'titles': '|'.join(ts), 'formatversion': 2}))
    for pg in r2.get('query', {}).get('pages', []):
        print(name, '|', pg['title'], '|', (pg.get('pageprops') or {}).get('wikibase_item'), '|', (pg.get('extract') or '')[:70].replace('\n', ' '))
    time.sleep(1)
