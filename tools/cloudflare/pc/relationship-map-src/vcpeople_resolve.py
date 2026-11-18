"""VCの代表者・パートナーなど(VCとLPの表に出てくる会社の人たち)を、Wikipedia検索→Wikidataの項目で特定する候補を出す。
英語版Wikipediaで、「人名 + 会社名」で検索し、記事の冒頭に会社名が含まれるものだけを候補にする(同名の別人を避けるため)。
出力: vcpeople_resolve.json / 標準出力(人名・会社・Wikipedia記事名・Q・冒頭)"""
import json, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
PEOPLE = [
    ('Alfred Lin', 'Sequoia Capital', ['sequoia']), ('Pat Grady', 'Sequoia Capital', ['sequoia']), ('Roelof Botha', 'Sequoia Capital', ['sequoia']), ('Doug Leone', 'Sequoia Capital', ['sequoia']), ('Michael Moritz', 'Sequoia Capital', ['sequoia']),
    ('Joshua Kushner', 'Thrive Capital', ['thrive']), ('Keith Rabois', 'Founders Fund', ['founders fund', 'khosla']), ('Brian Singerman', 'Founders Fund', ['founders fund']), ('Napoleon Ta', 'Founders Fund', ['founders fund']),
    ('Ravi Mhatre', 'Lightspeed Venture Partners', ['lightspeed']), ('Jeremy Liew', 'Lightspeed Venture Partners', ['lightspeed']), ('Barry Eggers', 'Lightspeed Venture Partners', ['lightspeed']),
    ('Hemant Taneja', 'General Catalyst', ['general catalyst']), ('Kenneth Chenault', 'General Catalyst', ['general catalyst']),
    ('Mamoon Hamid', 'Kleiner Perkins', ['kleiner']), ('John Doerr', 'Kleiner Perkins', ['kleiner']),
    ('Saam Motamedi', 'Greylock', ['greylock']), ('David Cowan', 'Bessemer Venture Partners', ['bessemer']), ('Byron Deeter', 'Bessemer Venture Partners', ['bessemer']),
    ('Jeff Jordan', 'Andreessen Horowitz', ['andreessen']), ('Chris Dixon', 'Andreessen Horowitz', ['andreessen']), ('Martin Casado', 'Andreessen Horowitz', ['andreessen']),
    ('Chase Coleman', 'Tiger Global Management', ['tiger global']), ('Scott Shleifer', 'Tiger Global Management', ['tiger global']),
    ('Michael Mritunjay Dell', 'x', ['x']),
    ('Gen Isayama', 'World Innovation Lab', ['world innovation lab', 'wil']), ('Yasuhiko Yurimoto', 'Global Brain', ['global brain']),
    ('Yohei Sawayama', 'Coral Capital', ['coral']), ('James Riney', 'Coral Capital', ['coral']),
    ('Anri Samata', 'ANRI', ['anri']), ('Yusuke Murata', 'Incubate Fund', ['incubate']),
    ('Nicole Musicco', 'CalPERS', ['calpers', 'california public employees']), ('Marcie Frost', 'CalPERS', ['calpers', 'california public employees']),
    ('Rajeev Misra', 'SoftBank Vision Fund', ['softbank']), ('Ruth Porat', 'Alphabet', ['google', 'alphabet']),
]


def get(u):
    for i in range(4):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read())
        except Exception as e:
            time.sleep(30 if '429' in str(e) else 3)
    return {}


out = []
for name, firm, keys in PEOPLE:
    if firm == 'x':
        continue
    j = get('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'generator': 'search', 'gsrsearch': name + ' ' + firm, 'gsrlimit': 4, 'prop': 'pageprops|extracts', 'ppprop': 'wikibase_item', 'exintro': 1, 'explaintext': 1, 'exchars': 500, 'formatversion': 2}))
    pages = sorted((j.get('query', {}).get('pages', [])), key=lambda p: p.get('index', 9))
    cand = []
    last = name.split()[-1].lower()
    for p in pages:
        t = (p.get('title') or '')
        ex = (p.get('extract') or '').lower()
        if last in t.lower() and any(k in ex for k in keys):
            cand.append({'title': t, 'q': p.get('pageprops', {}).get('wikibase_item', ''), 'intro': (p.get('extract') or '')[:140].replace('\n', ' ')})
    out.append({'name': name, 'firm': firm, 'cand': cand})
    time.sleep(1)
json.dump(out, open('vcpeople_resolve.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for o in out:
    print(o['name'], '|', o['firm'], '|', [(c['title'], c['q']) for c in o['cand'][:2]])
