"""英語版Wikipediaの『List of unicorn startup companies』(wikitext)から、世界のユニコーン一覧を作る。
出力: unicorns.json(表示用) / people_all_u.json(創業者のWikidata取得用)。Claude不要。"""
import json, os, re, urllib.parse, urllib.request

S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}


def fetch():
    u = 'https://en.wikipedia.org/w/api.php?' + urllib.parse.urlencode(
        {'action': 'parse', 'page': 'List of unicorn startup companies', 'prop': 'wikitext', 'format': 'json', 'formatversion': 2})
    d = json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read())
    return d['parse']['wikitext']


def clean(s):
    s = re.sub(r'<ref[^>]*/>', '', s)
    s = re.sub(r'<ref[^>]*>.*?</ref>', '', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return s.strip()


def link_name(s):
    """[[Target|Shown]] -> (Shown, Target)"""
    m = re.match(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', s.strip())
    if m:
        return (m.group(2) or m.group(1)).strip(), m.group(1).strip()
    return re.sub(r"'''?|\[\[|\]\]", '', s).strip(), ''


def plain(s):
    s = re.sub(r'\[\[(?:[^\]|]+\|)?([^\]]+)\]\]', r'\1', s)
    return re.sub(r"'''?|\{\{[^}]*\}\}", '', s).strip()


def date_of(s):
    m = re.search(r'\{\{\s*[Ss]tart date\s*\|\s*(\d{4})(?:\|(\d{1,2}))?', s)
    if m:
        return '%s-%02d' % (m.group(1), int(m.group(2) or 1)) if m.group(2) else m.group(1)
    m = re.search(r'([A-Z][a-z]+)?\s*(\d{4})', plain(s))
    return m.group(2) if m else ''


def flags(s):
    return [x.strip() for x in re.findall(r'\{\{\s*[Ff]lag(?:icon)?\s*\|\s*([^}|]+)', s)] or ([plain(s)] if plain(s) else [])


def founders(s):
    out = []
    s = clean(s)
    for part in re.split(r',| and |;|<br>', s):
        part = part.strip()
        if not part:
            continue
        n, t = link_name(part)
        n = plain(n)
        if n and len(n) < 40 and '=' not in n and not n.lower().startswith(('see ', 'various', 'url', 'website')):
            out.append({'n': n, 't': t})
    return out


w = fetch()
open(os.path.join(S, 'unicorn_wikitext.txt'), 'w', encoding='utf-8').write(w)
a = w.index('==List==')
m = re.search(r'^==\s*Former unicorns\s*==', w, re.M)
b = m.start() if m else len(w)
body = w[a:b]
rows = re.split(r'\n\|-\s*\n', body[body.index('{|'):])[1:]
res = []
for r in rows:
    cells = re.split(r'\n\|(?!\|)', '\n' + r.strip().lstrip('|'))
    cells = [c.strip() for c in cells]
    if len(cells) < 5:
        continue
    while len(cells) < 6:
        cells.append('')
    cells = [clean(c) for c in cells]
    name, tgt = link_name(cells[0].split('<ref')[0])
    try:
        val = float(re.sub(r'[^\d.]', '', cells[1].split('{{')[0]) or 0)
    except ValueError:
        continue
    res.append({'n': plain(name), 'w': tgt, 'v': val, 'd': date_of(cells[2]), 'i': plain(cells[3]),
                'c': flags(cells[4]), 'f': founders(cells[5])})
res = [x for x in res if x['n'] and x['v'] > 0]
for i, x in enumerate(res, 1):
    x['r'] = i
json.dump(res, open(os.path.join(S, 'unicorns.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# 創業者(リンクのある人)をWikidata取得用に
seen, ppl = set(), []
for x in res:
    for f in x['f']:
        t = f['t'] or ''
        if not t or t in seen or ':' in t:
            continue
        seen.add(t)
        ppl.append({'en': t, 'jp': f['n'], 'k': {'p': 1}, 'wiki': '',
                    'co': [['u_' + x['n'], x['n'], '共同創業者', 0, 0, 'p']]})
json.dump(ppl, open(os.path.join(S, 'people_all_u.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('unicorns', len(res), 'founders with page', len(ppl), 'top', [(x['n'], x['v']) for x in res[:3]])
