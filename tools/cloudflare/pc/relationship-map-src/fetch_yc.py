"""Y Combinator の出身企業を、英語版Wikipediaの『List of Y Combinator companies』の表から集める。Claude不要。
出力: vc_yc.json (会社名の配列)"""
import json, os, re, sys, urllib.parse, urllib.request

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
S = os.path.dirname(os.path.abspath(__file__))
url = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'parse', 'format': 'json', 'page': 'List of Y Combinator startups', 'prop': 'wikitext', 'formatversion': 2, 'redirects': 1})
wt = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'relationship-map-research/1.0 (personal use)'}), timeout=60).read())['parse']['wikitext']
names, seen = [], set()
for ln in wt.split('\n'):      # 箇条書き「* [[会社名]]」の形
    m = re.match(r'^\*+\s*\[\[([^\]|#\n]+)(?:\|([^\]\n]+))?\]\]', ln)
    if m:
        nm = (m.group(2) or m.group(1)).strip()
        if nm and nm.lower() not in seen:
            seen.add(nm.lower())
            names.append(nm)
for tb in re.findall(r'\{\|.*?\n\|\}', wt, re.S):
    for row in re.split(r'\n\|-+[^\n]*', tb)[1:]:
        m = re.search(r'\[\[([^\]|#\n]+)(?:\|([^\]\n]+))?\]\]', row)
        if not m:
            m2 = re.search(r'\n\|\s*([^|\n\[\]{}<]{2,40})\s*(?:\n|\|\|)', row)
            nm = m2.group(1).strip() if m2 else ''
        else:
            nm = (m.group(2) or m.group(1)).strip()
        if nm and nm.lower() not in seen and not re.match(r'^(File|Category|\d{4}|Winter|Summer|W\d\d|S\d\d)', nm):
            seen.add(nm.lower())
            names.append(nm)
json.dump(names, open(os.path.join(S, 'vc_yc.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('YC', len(names), names[:12])
