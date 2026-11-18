import urllib.request, urllib.parse, json, base64, re, time
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
titles = {
 'musk': 'Elon Musk', 'babuschkin': 'Igor Babuschkin', 'szegedy': 'Christian Szegedy', 'ba': 'Jimmy Ba', 'yaccarino': 'Linda Yaccarino',
 'yang': 'Greg Yang (mathematician)', 'wu': 'Yuhuai Wu', 'pohlen': 'Toby Pohlen', 'zuckerberg': 'Mark Zuckerberg', 'wang': 'Alexandr Wang',
 'friedman': 'Nat Friedman', 'zhao': 'Shengjia Zhao', 'lecun': 'Yann LeCun', 'gross': 'Daniel Gross (entrepreneur)', 'pang': 'Ruoming Pang',
 'bosworth': 'Andrew Bosworth', 'cox': 'Chris Cox (Meta)', 'pineau': 'Joelle Pineau', 'alwaleed': 'Al-Waleed bin Talal'}
def get(u):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25).read()
        except Exception as e:
            if '429' in str(e):
                time.sleep(6 * (i + 1))
            else:
                raise
res = {}
for k, t in titles.items():
    time.sleep(2.5)
    try:
        d = json.loads(get('https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(t.replace(' ', '_'))))
        th = d.get('thumbnail', {}).get('source')
        img = None
        if th:
            time.sleep(2)
            b = get(re.sub(r'/(\d+)px-', r'/120px-', th))
            if b[:3] == b'\xff\xd8\xff' or b[:4] == b'\x89PNG':
                img = 'data:%s;base64,%s' % ('image/jpeg' if b[:2] == b'\xff\xd8' else 'image/png', base64.b64encode(b).decode())
        res[k] = {'wiki': d.get('content_urls', {}).get('desktop', {}).get('page'), 'img': img, 'title': d.get('title'), 'desc': d.get('description')}
    except Exception as e:
        res[k] = {'err': str(e)}
    print(k, '|', res[k].get('title'), '|', res[k].get('desc'), '|', bool(res[k].get('img')), res[k].get('err', ''), flush=True)
json.dump(res, open(S + r'\xm.json', 'w'))
