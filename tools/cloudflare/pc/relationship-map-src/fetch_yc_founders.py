"""Y Combinatorの公式ディレクトリ(各社のページ)から、AI分野の会社の創業者(名前・肩書き)・設立年・場所・Twitterを集める。
元: yc_all.json(AIの印がある会社)。出力: yc_founders.json {slug: {...}}。途中経過を保存し、続きから再開できる。
礼儀: 3並列、1件ごとに少し待つ。公開ページを読むだけ(ログインしない)。
使い方: python -u fetch_yc_founders.py"""
import concurrent.futures as cf, html, json, os, re, sys, threading, time, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(S, 'yc_founders.json')
AI = {'AI', 'Generative AI', 'Machine Learning', 'Computer Vision', 'Natural Language Processing', 'AI Assistant', 'AIOps', 'Conversational AI'}
yc = [r for r in json.load(open(os.path.join(S, 'yc_all.json'), encoding='utf-8')) if (set(r.get('tags') or []) & AI) or re.search(r'\bAI\b', r.get('one_liner') or '')]
# 上位(注目の会社・活動中・新しいバッチ)から先に取る
order = {'Active': 0, 'Public': 0, 'Acquired': 1, 'Inactive': 2}
yc.sort(key=lambda r: (not r.get('top_company'), order.get(r.get('status'), 3), -(int(re.sub(r'\D', '', r.get('batch') or '0') or 0) if False else 0)))
done = json.load(open(F, encoding='utf-8')) if os.path.exists(F) else {}
lock = threading.Lock()


def one(r):
    s = r['slug']
    if s in done:
        return
    u = 'https://www.ycombinator.com/companies/' + s
    for i in range(3):
        try:
            h = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (research; personal use)'}), timeout=40).read().decode('utf-8', 'replace')
            m = re.search(r'data-page="([^"]+)"', h)
            if not m:
                break
            c = json.loads(html.unescape(m.group(1)))['props']['company']
            rec = {'name': c.get('name') or r['name'], 'batch': c.get('batch_name') or r.get('batch'), 'year': c.get('year_founded'), 'team': c.get('team_size'), 'loc': c.get('location'),
                   'one': (c.get('one_liner') or '')[:120], 'web': c.get('website'), 'tw': c.get('twitter_url'), 'status': r.get('status'),
                   'founders': [{'n': f.get('full_name'), 't': f.get('title')} for f in (c.get('founders') or []) if f.get('full_name')][:6]}
            with lock:
                done[s] = rec
            return
        except Exception as ex:
            time.sleep(3 * (i + 1))
    with lock:
        done[s] = {'name': r['name'], 'founders': [], 'err': 1}


t0 = time.time()
todo = [r for r in yc if r['slug'] not in done]
print('取得する会社', len(todo), '/ 全', len(yc), flush=True)
with cf.ThreadPoolExecutor(3) as ex:
    futs = []
    for k, r in enumerate(todo):
        futs.append(ex.submit(lambda rr=r: (one(rr), time.sleep(0.5))))
        if len(futs) >= 3:
            for f in futs:
                f.result()
            futs = []
            if (k + 1) % 60 < 3:
                with lock:
                    json.dump(done, open(F, 'w', encoding='utf-8'), ensure_ascii=False)
                print('取得済み', len(done), round(time.time() - t0), '秒', flush=True)
    for f in futs:
        f.result()
json.dump(done, open(F, 'w', encoding='utf-8'), ensure_ascii=False)
print('完了: ', len(done), '社 / 創業者あり', sum(1 for v in done.values() if v.get('founders')), flush=True)
