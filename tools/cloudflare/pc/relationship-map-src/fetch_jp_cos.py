"""日本の時価総額上位企業の『会社データ』を集める。Claude不要。途中から再開できる。
  1) 日経の会社概要ページ(誰でも読める部分): 正式社名・設立・代表者氏名・資本金・従業員数・本社
  2) Wikipedia(日本語)→Wikidata: 創業者・会長・CEO・取締役・所有者(株主)の記録(終了した就任は除く)
出力: jp_nikkei.json(日経の概要) / jp_cos.json(会社の図の元データ)
使い方: python fetch_jp_cos.py"""
import json, os, re, sys, time, urllib.parse, urllib.request

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'Mozilla/5.0 (personal use; internal relationship map)'}
WUA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}


def http(url, hdr, timeout=40):
    for i in range(4):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=timeout).read()
        except Exception as e:
            time.sleep(3 * (i + 1))
    return None


def ld(name, d):
    f = os.path.join(S, name)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


def sv(name, o):
    json.dump(o, open(os.path.join(S, name), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


# ---- 1) 日経の会社概要 ----
rank = [ln.rstrip('\n').split('|') for ln in open(os.path.join(S, 'ranking_jp.txt'), encoding='utf-8')]
nk = ld('jp_nikkei.json', {})
for r in rank:
    code = r[2]
    if code in nk and len(nk[code].get('cap', '')) <= 30:   # 資本金の読み取りを直したので、古い(長すぎる)記録だけ取り直す
        continue
    raw = http('https://www.nikkei.com/nkd/company/gaiyo/?scode=' + code, UA)
    if not raw:
        print(code, '取得失敗', flush=True)
        continue
    t = raw.decode('utf-8', 'replace')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    t = re.sub(r'<[^>]+>', '|', t)
    t = re.sub(r'[\s|]+', '|', t).replace('&nbsp;', ' ')

    def f(a, b):
        m = re.search(a + r'\|(.*?)\|' + b, t)
        return m.group(1) if m else ''
    jn = lambda s: (' ' if re.search(r'[A-Za-z]{3}', s) else '').join(s.split('|')).strip()
    nk[code] = {'full': re.sub(r'[（(]株[）)]|株式会社', '', f('正式社名', 'URL')).strip(), 'url': f('URL', '英文社名'), 'en': jn(f('英文社名', '相場欄名')),
                'est': f('設立年月日', '日経業種分類').split('|')[0], 'rep': jn(f('代表者氏名', '資本金')),
                'cap': (re.search(r'資本金\|([\d,]+\([^)]*\))', t) or [0, ''])[1], 'emp': (re.search(r'従業員数\|([\d,]+)', t) or [0, ''])[1],
                'addr': f('本社住所', '地図').replace('|', ' ')}
    sv('jp_nikkei.json', nk)
    print(code, nk[code]['full'], nk[code]['rep'], flush=True)
    time.sleep(1.5)
print('日経の概要', len(nk), flush=True)

# ---- 2) Wikipedia(日本語) → Wikidata ----
def wapi(base, **p):
    raw = http(base + '?' + urllib.parse.urlencode(p), WUA, 60)
    return json.loads(raw) if raw else {}


jc = ld('jp_cos.json', {})
todo = [r for r in rank if r[2] not in jc and r[2] in nk]
qid = {}
for i in range(0, len(todo), 15):     # 1回の問い合わせは50件まで(3候補×15社=45件)
    ch = todo[i:i + 15]
    names = {}
    for r in ch:
        names[r[2]] = [x for x in (nk[r[2]]['full'], r[1], nk[r[2]]['full'] + '株式会社') if x]
    tt = sorted({n for v in names.values() for n in v})
    d = wapi('https://ja.wikipedia.org/w/api.php', action='query', format='json', titles='|'.join(tt), redirects=1, prop='pageprops', ppprop='wikibase_item|disambiguation', formatversion=2)
    q = d.get('query', {})
    norm = {x['from']: x['to'] for x in q.get('normalized', [])}
    red = {x['from']: x['to'] for x in q.get('redirects', [])}
    pg = {p['title']: p for p in q.get('pages', [])}
    for code, cands in names.items():
        for c in cands:
            t = red.get(norm.get(c, c), norm.get(c, c))
            p = pg.get(t)
            if p and not p.get('missing') and 'disambiguation' not in p.get('pageprops', {}) and p.get('pageprops', {}).get('wikibase_item'):
                qid.setdefault(code, p['pageprops']['wikibase_item'])
                break
    time.sleep(1)
print('Q番号', len(qid), '/', len(todo), flush=True)

ents = {}
ids = sorted(set(qid.values()))
for i in range(0, len(ids), 40):
    d = wapi('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='claims|labels', languages='ja|en')
    ents.update(d.get('entities', {}))
    time.sleep(1)


def cids(e, prop):
    out = []
    for c in e.get('claims', {}).get(prop, []):
        v = c.get('mainsnak', {}).get('datavalue', {}).get('value')
        if not (isinstance(v, dict) and 'id' in v):
            continue
        q = c.get('qualifiers', {})
        end = q.get('P582', [{}])[0].get('datavalue', {}).get('value', {}).get('time') if q.get('P582') else None
        st = q.get('P580', [{}])[0].get('datavalue', {}).get('value', {}).get('time') if q.get('P580') else None
        if end:      # 終わった就任・所有は載せない
            continue
        out.append((v['id'], int(st[1:5]) if st and re.match(r'^[+-]\d{4}', st) else 0))
    return out


# 本人確認: 東証の証券コードが一致する(P414の資格 P249)ものだけ採用
okq = {}
for code, q in qid.items():
    e = ents.get(q) or {}
    codes = []
    for c in e.get('claims', {}).get('P414', []):
        for x in c.get('qualifiers', {}).get('P249', []):
            codes.append(str(x.get('datavalue', {}).get('value', '')))
    if code in codes:
        okq[code] = q
print('証券コードで本人確認できた', len(okq), '/', len(qid), flush=True)

PROPS = [('P169', 'ceo'), ('P488', 'chair'), ('P112', 'founder'), ('P3320', 'board'), ('P127', 'owner'), ('P749', 'parent')]
need = set()
rel = {}
for code, q in okq.items():
    e = ents[q]
    rel[code] = []
    for p, role in PROPS:
        for vid, yr in cids(e, p)[:12]:
            rel[code].append((vid, role, yr))
            need.add(vid)
lab = {}
ids = sorted(need)
for i in range(0, len(ids), 40):
    d = wapi('https://www.wikidata.org/w/api.php', action='wbgetentities', format='json', ids='|'.join(ids[i:i + 40]), props='labels|claims', languages='ja|en')
    for k, e in d.get('entities', {}).items():
        lb = e.get('labels', {})
        human = any(c.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id') == 'Q5' for c in e.get('claims', {}).get('P31', []))
        lab[k] = {'ja': lb.get('ja', {}).get('value', ''), 'en': lb.get('en', {}).get('value', ''), 'human': human}
    time.sleep(1)
for code, q in okq.items():
    seen, people, orgs = set(), [], []
    for vid, role, yr in rel[code]:
        L = lab.get(vid)
        if not L or vid in seen and role not in ('founder',):
            continue
        nm = L['ja'] or L['en']
        if not nm:
            continue
        if role in ('owner', 'parent') :
            if L['human']:
                people.append({'id': vid, 'ja': L['ja'], 'en': L['en'], 'role': 'owner', 'from': yr})
            else:
                orgs.append({'id': vid, 'ja': L['ja'], 'en': L['en'], 'role': role})
        elif L['human']:
            people.append({'id': vid, 'ja': L['ja'], 'en': L['en'], 'role': role, 'from': yr})
        seen.add(vid)
    jc[code] = {'qid': q, 'people': people, 'orgs': orgs}
sv('jp_cos.json', jc)
print('jp_cos.json', len(jc), '社 / 人物', sum(len(v['people']) for v in jc.values()), '/ 組織', sum(len(v['orgs']) for v in jc.values()))
