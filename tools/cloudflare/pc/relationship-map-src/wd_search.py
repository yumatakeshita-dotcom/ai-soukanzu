import urllib.request, urllib.parse, json, time
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
names = {
 'zaremba': 'Wojciech Zaremba', 'chen': 'Mark Chen', 'kwon': 'Jason Kwon', 'glaese': 'Amelia Glaese', 'schulman': 'John Schulman',
 'daniela': 'Daniela Amodei', 'leike': 'Jan Leike', 'toner': 'Helen Toner', 'mccauley': 'Tasha McCauley', 'lightcap': 'Brad Lightcap',
 'weil': 'Kevin Weil', 'kalinowski': 'Caitlin Kalinowski', 'achiam': 'Joshua Achiam', 'dresser': 'Denise Dresser',
 'clark': 'Jack Clark', 'olah': 'Chris Olah', 'brown': 'Tom Brown', 'mccandlish': 'Sam McCandlish', 'mann': 'Ben Mann',
 'rao': 'Krishna Rao', 'patil': 'Rahul Patil', 'vora': 'Ami Vora', 'kingma': 'Durk Kingma', 'narasimhan': 'Vas Narasimhan', 'liddell': 'Chris Liddell'}
def get(u):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=20).read()
        except Exception as e:
            if '429' in str(e):
                time.sleep(6 * (i + 1))
            else:
                raise
    raise Exception('429')
for k, n in names.items():
    time.sleep(1.5)
    try:
        u = 'https://www.wikidata.org/w/api.php?action=wbsearchentities&language=en&format=json&limit=4&search=' + urllib.parse.quote(n)
        d = json.loads(get(u))
        print(k, '|', ' ;; '.join('%s: %s' % (x['id'], x.get('description', '')) for x in d.get('search', [])), flush=True)
    except Exception as e:
        print(k, 'ERR', e, flush=True)
