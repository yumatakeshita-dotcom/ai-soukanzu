"""人物の名言を、Wikiquote(英語版・日本語版)から集める。人物の記事名は people_titles.json(Wikipediaの記事名)を使う。同じ名前のWikiquoteの記事があれば、箇条書きの名言を最大6つ取る。
名言の文章は Wikiquote(CC BY-SA 4.0)のもの。出典のページへのリンクと一緒に表示すること。途中から再開できる。Claude不要。
出力: people_quotes.json  {Q番号: {w: 'en'|'ja', t: 記事名, q: [名言, ...]}}   進み具合: people_quotes_done.json
使い方: python -u fetch_quotes.py"""
import json, os, re, sys, time, urllib.parse, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)'}
OUT = os.path.join(S, 'people_quotes.json')
DONE = os.path.join(S, 'people_quotes_done.json')
titles = json.load(open(os.path.join(S, 'people_titles.json'), encoding='utf-8'))
out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
done = set(json.load(open(DONE, encoding='utf-8'))) if os.path.exists(DONE) else set()


def api(lang, **p):
    url = 'https://%s.wikiquote.org/w/api.php?%s' % (lang, urllib.parse.urlencode(p))
    for i in range(6):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
        except Exception as e:
            time.sleep(60 if '429' in str(e) else 4 * (i + 1))
    return {}


def clean(t):
    t = re.sub(r'<ref[^>]*>.*?</ref>|<ref[^>]*/>|<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r'\1', t)
    t = re.sub(r"'''?|<[^>]+>", '', t)
    t = re.sub(r'\[https?://\S+ ([^\]]+)\]|\[https?://\S+\]', r'\1', t)
    return re.sub(r'\s+', ' ', t).strip(' "「」“”')


def quotes(wikitext):
    qs = []
    for ln in wikitext.split('\n'):
        if re.match(r'^\*(?!\*)\s', ln):      # 箇条書きの1段目=名言(2段目=出典)
            q = clean(ln[1:])
            if 20 <= len(q) <= 260 and not q.startswith(('See ', 'Main', 'http')):
                qs.append(q)
        if len(qs) >= 6:
            break
    return qs


todo = [(q, t) for q, t in titles.items() if q not in done]
print('人物', len(titles), '未処理', len(todo), flush=True)
for lang in ('en', 'ja'):
    key = 'en' if lang == 'en' else 'ja'
    want = [(q, t[key]) for q, t in todo if t.get(key) and q not in out]
    for i in range(0, len(want), 40):
        ch = want[i:i + 40]
        d = api(lang, action='query', format='json', prop='revisions', rvprop='content', rvslots='main', redirects=1, formatversion=2, titles='|'.join(t for _, t in ch))
        qd = d.get('query', {})
        norm = {x['from']: x['to'] for x in qd.get('normalized', [])}
        red = {x['from']: x['to'] for x in qd.get('redirects', [])}
        pages = {p['title']: p for p in qd.get('pages', []) if not p.get('missing')}
        for q, t in ch:
            tt = red.get(norm.get(t, t), norm.get(t, t))
            pg = pages.get(tt)
            if not pg:
                continue
            try:
                wt = pg['revisions'][0]['slots']['main']['content']
            except Exception:
                continue
            qs = quotes(wt)
            if qs and q not in out:
                out[q] = {'w': lang, 't': tt, 'q': qs}
        time.sleep(1.0)
        if (i // 40) % 10 == 0:
            json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
            print(lang, i, '/', len(want), '名言あり', len(out), flush=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(sorted(titles.keys()), open(DONE, 'w', encoding='utf-8'))
print('完了', len(out), flush=True)
