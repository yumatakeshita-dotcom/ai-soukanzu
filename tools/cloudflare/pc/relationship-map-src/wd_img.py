import urllib.request, urllib.parse, json, time, base64
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
ids = {'zaremba': 'Q27733815', 'chen': 'Q126287485', 'schulman': 'Q103236782', 'daniela': 'Q119721378', 'leike': 'Q123130693',
       'toner': 'Q123475976', 'kalinowski': 'Q27449525', 'achiam': 'Q126287494', 'clark': 'Q135111322', 'olah': 'Q50358648',
       'mccandlish': 'Q105285886', 'kingma': 'Q29022624', 'narasimhan': 'Q115735786', 'liddell': 'Q5107236'}
def get(u):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read()
        except Exception as e:
            if '429' in str(e):
                time.sleep(6 * (i + 1))
            else:
                raise
    raise Exception('429')
out = {}
for k, q in ids.items():
    time.sleep(2)
    try:
        d = json.loads(get('https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&props=claims|labels|descriptions&languages=en&ids=' + q))
        e = d['entities'][q]
        label = e['labels'].get('en', {}).get('value')
        p18 = e['claims'].get('P18')
        if not p18:
            print(k, label, 'no P18', flush=True)
            continue
        fn = p18[0]['mainsnak']['datavalue']['value']
        time.sleep(2)
        b = get('https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(fn.replace(' ', '_')) + '?width=120')
        if b[:3] == b'\xff\xd8\xff' or b[:4] == b'\x89PNG':
            out[k] = {'img': 'data:%s;base64,%s' % ('image/jpeg' if b[:2] == b'\xff\xd8' else 'image/png', base64.b64encode(b).decode()), 'file': fn, 'label': label}
            print(k, label, fn, len(b), flush=True)
        else:
            print(k, label, fn, 'not image', flush=True)
    except Exception as ex:
        print(k, 'ERR', ex, flush=True)
json.dump(out, open(S + r'\photos2.json', 'w'))
