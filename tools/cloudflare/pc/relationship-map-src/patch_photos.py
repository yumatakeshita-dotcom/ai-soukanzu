import urllib.request, urllib.parse, json, base64, re, time
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
O = r'C:\Users\yumat\.claude\output'
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
photos = json.load(open(S + r'\photos2.json'))
fn = "Jack Clark, co-founder of Anthropic, giving a talk on AI at the Schwarzman Centre in Oxford.jpg"
b = urllib.request.urlopen(urllib.request.Request('https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(fn.replace(' ', '_')) + '?width=120', headers=UA), timeout=25).read()
assert b[:3] == b'\xff\xd8\xff'
photos['clark'] = {'img': 'data:image/jpeg;base64,' + base64.b64encode(b).decode()}
add = {k: photos[k]['img'] for k in ('narasimhan', 'liddell', 'clark')}
p = O + r'\anthropic-relationship-map.html'
h = open(p, encoding='utf-8').read()
m = re.search(r'const PH=(\{.*?\});\n', h, flags=re.S)
ph = json.loads(m.group(1))
ph.update(add)
h = h[:m.start(1)] + json.dumps(ph, ensure_ascii=False) + h[m.end(1):]
open(p, 'w', encoding='utf-8').write(h)
print(sorted(ph))
