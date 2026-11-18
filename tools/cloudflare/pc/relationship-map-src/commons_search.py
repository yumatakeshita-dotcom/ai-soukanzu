import urllib.request, urllib.parse, json, time
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
q = {'zaremba': 'Wojciech Zaremba', 'chen': 'Mark Chen OpenAI', 'schulman': 'John Schulman', 'daniela': 'Daniela Amodei', 'leike': 'Jan Leike',
     'toner': 'Helen Toner', 'kalinowski': 'Caitlin Kalinowski', 'achiam': 'Joshua Achiam', 'clark': 'Jack Clark Anthropic', 'olah': 'Chris Olah',
     'mccandlish': 'Sam McCandlish', 'kingma': 'Durk Kingma', 'lightcap': 'Brad Lightcap', 'weil': 'Kevin Weil', 'kwon': 'Jason Kwon OpenAI',
     'mccauley': 'Tasha McCauley', 'rao': 'Krishna Rao Anthropic', 'patil': 'Rahul Patil Anthropic', 'vora': 'Ami Vora', 'brown': 'Tom Brown Anthropic', 'mann': 'Ben Mann Anthropic'}
def get(u):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read()
        except Exception as e:
            if '429' in str(e):
                time.sleep(6 * (i + 1))
            else:
                raise
for k, s in q.items():
    time.sleep(2)
    try:
        d = json.loads(get('https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srlimit=4&format=json&srsearch=' + urllib.parse.quote(s)))
        print(k, '|', ' ;; '.join(x['title'] for x in d['query']['search']), flush=True)
    except Exception as e:
        print(k, 'ERR', e, flush=True)
