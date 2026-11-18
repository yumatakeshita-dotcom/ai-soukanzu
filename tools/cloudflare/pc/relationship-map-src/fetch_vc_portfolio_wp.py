"""VCの出資先を、Wikipedia(英語版)の各VCの記事の『出資先・ポートフォリオ』の節から集める。
会社だけに絞る: リンク先のWikidata項目が、人間ではなく、設立日(P571)か業種(P452)を持つもの。出典は、そのVCのWikipedia記事(CC BY-SA)。
出力: money_wp.json    使い方: python -u fetch_vc_portfolio_wp.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
H = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
VCS = {'Sequoia Capital': 'Sequoia Capital', 'Andreessen Horowitz': 'Andreessen Horowitz', 'Founders Fund': 'Founders Fund', 'Accel': 'Accel (company)', 'Kleiner Perkins': 'Kleiner Perkins', 'Benchmark': 'Benchmark (venture capital firm)', 'Greylock': 'Greylock Partners', 'Lightspeed Venture Partners': 'Lightspeed Venture Partners', 'General Catalyst': 'General Catalyst', 'Insight Partners': 'Insight Partners', 'Thrive Capital': 'Thrive Capital', 'SoftBank Vision Fund': 'SoftBank Vision Fund', 'Index Ventures': 'Index Ventures', 'Khosla Ventures': 'Khosla Ventures', 'Tiger Global Management': 'Tiger Global Management', 'Coatue': 'Coatue Management', 'Union Square Ventures': 'Union Square Ventures', 'First Round Capital': 'First Round Capital', 'Bessemer Venture Partners': 'Bessemer Venture Partners', 'NEA': 'New Enterprise Associates', 'Techstars': 'Techstars', '500 Global': '500 Global', 'Lux Capital': 'Lux Capital', 'Menlo Ventures': 'Menlo Ventures', 'Redpoint Ventures': 'Redpoint Ventures', 'Battery Ventures': 'Battery Ventures', 'GV': 'GV (company)', 'Insight Venture Partners': 'Insight Partners'}


def api(p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request('https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(p), headers=H), timeout=60).read())
        except Exception as e:
            time.sleep(30 if '429' in str(e) else 3 * (i + 1))


def wd(p):
    for i in range(5):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(p), headers=H), timeout=60).read())
        except Exception as e:
            time.sleep(30 if '429' in str(e) else 3 * (i + 1))


rows = []
P31 = {}
for vc, title in VCS.items():
    r = api({'action': 'parse', 'page': title, 'prop': 'sections', 'redirects': 1, 'format': 'json', 'formatversion': 2})
    secs = (r or {}).get('parse', {}).get('sections', [])
    want = [s['index'] for s in secs if re.search(r'invest|portfolio|companies', s['line'], re.I)]
    links = []
    for idx in want[:3]:
        w = api({'action': 'parse', 'page': title, 'prop': 'links', 'section': idx, 'redirects': 1, 'format': 'json', 'formatversion': 2})
        links += [l['title'] for l in (w or {}).get('parse', {}).get('links', []) if l.get('ns') == 0 and l.get('exists')]
        time.sleep(0.5)
    links = list(dict.fromkeys(links))
    print(vc, 'セクション', len(want), 'リンク', len(links), flush=True)
    kept = []
    for i in range(0, len(links), 50):
        ch = links[i:i + 50]
        q = api({'action': 'query', 'prop': 'pageprops', 'ppprop': 'wikibase_item', 'titles': '|'.join(ch), 'redirects': 1, 'format': 'json', 'formatversion': 2})
        ids = {}
        for pg in (q or {}).get('query', {}).get('pages', []):
            qq = pg.get('pageprops', {}).get('wikibase_item')
            if qq:
                ids[qq] = pg['title']
        if ids:
            e = wd({'action': 'wbgetentities', 'ids': '|'.join(ids), 'props': 'claims', 'format': 'json'})
            for qq, en in ((e or {}).get('entities', {})).items():
                cl = en.get('claims', {})
                human = any(((s.get('mainsnak', {}).get('datavalue') or {}).get('value') or {}).get('id') == 'Q5' for s in cl.get('P31', []))
                if not human and (cl.get('P571') or cl.get('P452')) and ids.get(qq) and ids[qq] != title:
                    kept.append(ids[qq]); P31[ids[qq]] = [((x.get('mainsnak', {}).get('datavalue') or {}).get('value') or {}).get('id') for x in cl.get('P31', [])]
        time.sleep(1)
    for c in dict.fromkeys(kept):
        rows.append({'src': vc, 'dst': c, 'kind': '出資', 'label': 'Wikipediaの記載', 'year': '', 'amount': '', 'note': 'Wikipediaの「%s」の出資先の記載' % title, 'url': 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(title.replace(' ', '_')), 'media': 'Wikipedia(CC BY-SA)', 'd': '', 'p31': P31.get(c, [])})
    print('  会社に絞った出資先', len(set(kept)), flush=True)
json.dump(rows, open(os.path.join(S, 'money_wp.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('合計', len(rows))
