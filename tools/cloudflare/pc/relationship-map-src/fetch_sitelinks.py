"""人物の有名度の指標: Wikidata の sitelinks(Wikipedia等の言語版の数)を people_fame.json に集める。対象は people_social.json の X のある人。
wbgetentities(50件ずつ・1秒あけ)。SPARQL とは別の窓口だが、重い収集とは同時に動かさない。"""
import json, os, time, urllib.request, urllib.parse
S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, 'people_fame.json')
fame = json.load(open(OUT, encoding='utf8')) if os.path.exists(OUT) else {}
soc = json.load(open(os.path.join(S, 'people_social.json'), encoding='utf8'))
qs = [q for q, v in soc.items() if v.get('x') and q not in fame]
print('対象', len(qs), flush=True)
for i in range(0, len(qs), 50):
    ch = qs[i:i + 50]
    url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode({'action': 'wbgetentities', 'ids': '|'.join(ch), 'props': 'sitelinks', 'format': 'json'})
    for t in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'kigyo-hito-tsunagari-fame/1.0 (personal research)'})
            d = json.load(urllib.request.urlopen(req, timeout=60))
            break
        except Exception as e:
            print('再試行', e, flush=True); time.sleep(10)
    else:
        continue
    for q, e in (d.get('entities') or {}).items():
        sl = e.get('sitelinks') or {}
        fame[q] = sum(1 for k in sl if k.endswith('wiki') and k not in ('commonswiki', 'specieswiki', 'metawiki', 'wikidatawiki'))
    json.dump(fame, open(OUT, 'w', encoding='utf8'), ensure_ascii=False)
    print(i + len(ch), flush=True)
    time.sleep(1.5)
print('完了', len(fame))
