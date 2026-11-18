"""顔写真がまだ無い人物について、所属する会社の公式サイトのチーム紹介ページ(/team, /about, /leadership など)から探す。会社ごとに数ページだけ取り、
画像の alt(代替テキスト)に、その人の名前(姓・名の両方)が入っているものだけを採る。途中から再開できる。Claude不要。
出力: faces_web.json  {名前(英語): {i: data URI, s: 'company site', u: ページのURL}}   進み具合: faces_web_done.json
使い方: python -u fetch_faces_web.py"""
import base64, html, io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
UA = {'User-Agent': 'Mozilla/5.0 (compatible; relationship-map-research/1.0; personal use)', 'Accept': 'text/html,image/*;q=0.8,*/*;q=0.5'}
OUT = os.path.join(S, 'faces_web.json')
DONE = os.path.join(S, 'faces_web_done.json')
from adds import apply_adds
CO_ALL = {**__import__('newco_data').CO, **__import__('newco_data2').CO2, **__import__('newco_data3').CO3, **__import__('newco_data4').CO4, **__import__('newco_data5').CO5,
          **__import__('newco_data6').CO6, **__import__('newco_data7').CO7, **__import__('newco_data7b').CO7B, **__import__('newco_data8').CO8}
apply_adds(CO_ALL)
PATHS = ['/team', '/about', '/about-us', '/company', '/leadership', '/people', '/about/team', '/our-team', '/company/leadership', '/about/leadership', '/management', '/who-we-are']

have = set()
for f in os.listdir(S):
    if (f.startswith('outsiders') and f.endswith('.json')) or f == 'photos2.json':
        try:
            for k, v in json.load(open(os.path.join(S, f), encoding='utf-8')).items():
                if isinstance(v, dict) and v.get('img'):
                    have.add(k)
        except Exception:
            pass
for f in ('faces_cache.json',):
    p = os.path.join(S, f)
    if os.path.exists(p):
        for k, v in json.load(open(p, encoding='utf-8')).items():
            if v:
                have.add(k)
out = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
have |= set(out)
done = json.load(open(DONE, encoding='utf-8')) if os.path.exists(DONE) else {}


def get(u, raw=False, tries=2):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25)
            b = r.read(3_000_000)
            return b if raw else b.decode(r.headers.get_content_charset() or 'utf-8', errors='replace')
        except Exception as e:
            if '404' in str(e) or '403' in str(e) or '410' in str(e):
                return None
            time.sleep(2 * (i + 1))
    return None


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def shrink(b):
    try:
        im = Image.open(io.BytesIO(b)).convert('RGB')
        w, h = im.size
        if min(w, h) < 80 or not (0.6 <= w / h <= 1.6):
            return None
        s = min(w, h)
        top = 0 if h > w else (h - s) // 2
        im = im.crop(((w - s) // 2, top, (w - s) // 2 + s, top + s)).resize((96, 96), Image.LANCZOS)
        o = io.BytesIO()
        im.save(o, 'JPEG', quality=68, optimize=True)
        return 'data:image/jpeg;base64,' + base64.b64encode(o.getvalue()).decode()
    except Exception:
        return None


IMG = re.compile(r'<img\b[^>]*>', re.I | re.S)
ATTR = re.compile(r'([\w:-]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\')', re.S)


def imgs(page, base):
    res = []
    for tag in IMG.findall(page):
        a = {m.group(1).lower(): html.unescape(m.group(2) if m.group(2) is not None else m.group(3)) for m in ATTR.finditer(tag)}
        src = a.get('data-src') or a.get('data-lazy-src') or (a.get('srcset') or '').split(',')[0].strip().split(' ')[0] or a.get('src') or ''
        if not src or src.startswith('data:') or re.search(r'\.(svg|gif)(\?|$)', src, re.I):
            continue
        res.append((urllib.parse.urljoin(base, src), (a.get('alt') or '') + ' ' + (a.get('title') or '')))
    return res


want = {}      # 会社キー -> {web, people: {名前}}
for key, c in CO_ALL.items():
    center = c.get('center')
    web = (c.get('WEB') or {}).get(center) or ''
    if not web.startswith('http'):
        continue
    en = c.get('EN', {})
    ppl = {en[n['id']] for n in c['N'] if n.get('kind') == 'p' and en.get(n['id']) and en[n['id']] not in have}
    if ppl:
        want[key] = {'web': web.rstrip('/'), 'people': sorted(ppl)}
print('会社', len(want), '人物', sum(len(v['people']) for v in want.values()), flush=True)
n = 0
for key, v in want.items():
    if key in done:
        continue
    found = 0
    seen_pages = set()
    for path in PATHS:
        u = v['web'] + path
        page = get(u)
        time.sleep(0.8)
        if not page or len(page) < 2000 or u in seen_pages:
            continue
        seen_pages.add(u)
        im = imgs(page, u)
        for nm in v['people']:
            if nm in out:
                continue
            toks = [norm(t) for t in nm.split() if len(norm(t)) >= 2]
            if len(toks) < 2:
                continue
            for src, alt in im:
                al = norm(alt + ' ' + src.rsplit('/', 1)[-1])
                if all(t in al for t in (toks[0], toks[-1])):
                    b = get(src, raw=True)
                    time.sleep(0.5)
                    data = shrink(b) if b else None
                    if data:
                        out[nm] = {'i': data, 's': '公式サイト', 'u': u}
                        found += 1
                        print('○', nm, u, flush=True)
                        break
        if all(nm in out for nm in v['people']):
            break
    done[key] = found
    n += 1
    if n % 10 == 0:
        json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(done, open(DONE, 'w', encoding='utf-8'))
        print('進み', n, '/', len(want), '見つかった', len(out), flush=True)
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(done, open(DONE, 'w', encoding='utf-8'))
print('完了', len(out), flush=True)
