"""注目の100人のうち、Wikidataで別人を選んでいた人(肩書きが合わない)を、正しい項目に直して、年表・紹介文・写真・SNSを取り直す。
直す人: 山田進太郎(メルカリ創業者)→Q22120737、川邊健太郎(LINEヤフー)→Q11479322、松尾豊(東京大学・AI)→Q11529703。
根拠: 日本語版Wikipediaの記事の冒頭が、本人の肩書きと一致(山田: メルカリ創業者、川邊: メディアプロデューサー・実業家、松尾: 工学者)。
使い方: python -u top100_fix.py"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(os.path.dirname(S), 'relationship-map-site')
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
F = os.path.join(S, 'top100_data.json')
FIX = {'Shintaro Yamada': 'Q22120737', 'Kentaro Kawabe': 'Q11479322', 'Yutaka Matsuo': 'Q11529703'}
d = json.load(open(F, encoding='utf-8'))


def get(u, raw=False):
    for i in range(5):
        try:
            b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
            return b if raw else json.loads(b)
        except Exception as ex:
            time.sleep(40 if '429' in str(ex) else 4 * (i + 1))
    return None


def wd(**p):
    return get('https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(p)) or {}


def yr(snak):
    v = (snak or {}).get('datavalue', {}).get('value', {})
    m = re.match(r'^[+-]?(\d{4})', v.get('time', '')) if isinstance(v, dict) else None
    return int(m.group(1)) if m else None


def clip(t, n=520):
    t = re.sub(r'\s+', ' ', t or '').strip()
    if len(t) <= n:
        return t
    cut = t[:n]
    k = max(cut.rfind('。'), cut.rfind('. '))
    return cut[:k + 1] if k > 80 else cut.rstrip() + '…'


P = {'P108': '職歴', 'P39': '役職', 'P69': '学歴', 'P166': '受賞'}
for e in d:
    q = FIX.get(e.get('en'))
    if not q:
        continue
    en = wd(action='wbgetentities', format='json', ids=q, props='claims|labels|descriptions|sitelinks', languages='ja|en', sitefilter='jawiki|enwiki').get('entities', {}).get(q, {})
    cl = en.get('claims', {})
    e['q'] = q
    e['ja'] = en.get('labels', {}).get('ja', {}).get('value', '') or e.get('ja', '')
    e['desc'] = en.get('descriptions', {}).get('ja', {}).get('value') or en.get('descriptions', {}).get('en', {}).get('value') or ''
    e['how'] = '日本語版Wikipediaの記事で確認(別人の項目を直した)'
    for k in ('intro', 'w', 't', 'img'):
        e.pop(k, None)
    # 年表
    need = set()
    for p in P:
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if isinstance(v, dict) and v.get('id'):
                need.add(v['id'])
    labels = {}
    nl = sorted(need)
    for i in range(0, len(nl), 50):
        for qq, x in wd(action='wbgetentities', format='json', props='labels', languages='ja|en', ids='|'.join(nl[i:i + 50])).get('entities', {}).items():
            lb = x.get('labels', {})
            labels[qq] = (lb.get('ja') or lb.get('en') or {}).get('value', qq)
        time.sleep(1)
    tl = []
    for p, kind in P.items():
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if not (isinstance(v, dict) and v.get('id')):
                continue
            qual = st.get('qualifiers', {})
            tl.append({'y': yr((qual.get('P580') or [None])[0]) or yr((qual.get('P585') or [None])[0]), 'y2': yr((qual.get('P582') or [None])[0]), 'kind': kind, 'label': labels.get(v['id'], v['id']), 'ref': bool(st.get('references'))})
    for st in cl.get('P569', [])[:1]:
        tl.append({'y': yr(st.get('mainsnak')), 'y2': None, 'kind': '生年', 'label': '生まれる', 'ref': bool(st.get('references'))})
    tl.sort(key=lambda t: (t['y'] is None, t['y'] or 0))
    e['timeline'] = tl
    e['nref'] = sum(1 for t in tl if t['ref'])
    # SNS(Wikidataに登録されたもの)
    sns = {}
    for k, p in (('x', 'P2002'), ('ig', 'P2003'), ('yt', 'P2397'), ('web', 'P856')):
        for st in cl.get(p, []):
            v = (st.get('mainsnak', {}).get('datavalue', {}) or {}).get('value')
            if isinstance(v, str) and v:
                sns[k] = v
                break
    e['sns_wd'] = sns
    # 紹介文(Wikipedia)
    sl = en.get('sitelinks', {})
    lang = 'ja' if sl.get('jawiki') else ('en' if sl.get('enwiki') else None)
    if lang:
        title = sl[lang + 'wiki']['title']
        r = get('https://%s.wikipedia.org/w/api.php?' % lang + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'extracts', 'exintro': 1, 'explaintext': 1, 'redirects': 1, 'titles': title, 'formatversion': 2}))
        ex = ((r or {}).get('query', {}).get('pages') or [{}])[0].get('extract', '')
        if ex:
            e['intro'], e['w'], e['t'] = clip(ex), lang, title
    # 写真(Commons。ライセンスを確認できたものだけ)
    p18 = cl.get('P18', [])
    fn = p18 and p18[0].get('mainsnak', {}).get('datavalue', {}).get('value')
    if fn:
        r = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode({'action': 'query', 'format': 'json', 'prop': 'imageinfo', 'iiprop': 'url|extmetadata', 'iiurlwidth': 400, 'titles': 'File:' + fn, 'formatversion': 2}))
        try:
            ii = r['query']['pages'][0]['imageinfo'][0]
            md = ii.get('extmetadata', {})
            lic = (md.get('LicenseShortName') or {}).get('value', '')
            if lic:
                b = get(ii.get('thumburl') or ii.get('url'), raw=True)
                im = Image.open(io.BytesIO(b)).convert('RGB')
                w, h = im.size
                s = min(w, h)
                top = 0 if h > w else (h - s) // 2
                im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((200, 200), Image.LANCZOS)
                im.save(os.path.join(SITE, 'public', 'img', 'q-%s.jpg' % q.lstrip('Q')), 'JPEG', quality=82, optimize=True)
                e['img'] = {'lic': lic, 'artist': re.sub(r'<[^>]+>', '', (md.get('Artist') or {}).get('value', '')).strip()[:80], 'url': ii.get('descriptionurl') or ''}
        except Exception as ex:
            print('写真を取れず', str(ex)[:60])
    print('直した:', e['en'], e['ja'], q, '| 肩書き:', e['desc'], '| 年表', len(tl), '| 紹介', bool(e.get('intro')), '| 写真', bool(e.get('img')), '| SNS', sns, flush=True)
json.dump(d, open(F, 'w', encoding='utf-8'), ensure_ascii=False)
