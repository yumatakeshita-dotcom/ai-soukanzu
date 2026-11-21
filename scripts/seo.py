"""各ページの <head> に title・description・OGP を入れ、sitemap.xml と robots.txt を作る。
使い方: python3 scripts/seo.py          … 書き込む(何度動かしても同じ結果。印の間だけ置き換える)
        python3 scripts/seo.py --check  … 足りないページがあれば終了コード1(書き込まない)
設定は scripts/seo_config.json(公開URLはそこ1か所)。
本体 index.html は毎朝の更新で中身が変わるが、<head> の印(SEO:START〜SEO:END)は触られない。
万一消えたら、このスクリプトをもう一度動かせば戻る。build-lab と weekly.py の最後にも自動で動く。
"""
import json, os, re, sys
from html import escape
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SITE = os.path.join(ROOT, 'site')
CFG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seo_config.json'), encoding='utf-8'))
BASE = CFG['base_url'].rstrip('/')
S, E = '<!--SEO:START-->', '<!--SEO:END-->'
BLOCK_RE = re.compile(re.escape(S) + r'.*?' + re.escape(E), re.S)

def block(p):
    url = BASE + p['url']; img = BASE + '/' + CFG['image']
    t, d = escape(p['title'], True), escape(p['description'], True)
    return '\n'.join([S,
      '<meta name="description" content="%s">' % d,
      '<link rel="canonical" href="%s">' % url,
      '<meta property="og:type" content="website">',
      '<meta property="og:site_name" content="%s">' % escape(CFG['site_name'], True),
      '<meta property="og:locale" content="ja_JP">',
      '<meta property="og:title" content="%s">' % t,
      '<meta property="og:description" content="%s">' % d,
      '<meta property="og:url" content="%s">' % url,
      '<meta property="og:image" content="%s">' % img,
      '<meta property="og:image:width" content="1200">',
      '<meta property="og:image:height" content="630">',
      '<meta name="twitter:card" content="summary_large_image">',
      '<meta name="twitter:title" content="%s">' % t,
      '<meta name="twitter:description" content="%s">' % d,
      '<meta name="twitter:image" content="%s">' % img,
      E]) + '\n'

def inject(path, p):
    s = open(path, encoding='utf-8').read()
    b = block(p)
    if S in s:
        n = BLOCK_RE.sub(lambda m: b.rstrip('\n'), s, count=1)
    else:
        i = s.find('</head>')   # 最初の </head> = 本物のページの頭
        if i < 0:               # 週のまとめは <head> のない断片。先頭の <title> の直後(まだ頭の中)に入れる
            i = s.find('</title>')
            if i < 0: return None
            i += len('</title>\n') if s[i+8:i+9] == '\n' else len('</title>')
        n = s[:i] + b + s[i:]
    if n != s: open(path, 'w', encoding='utf-8').write(n)
    return n != s

def main(check=False):
    bad = 0
    for rel, p in CFG['pages'].items():
        path = os.path.join(SITE, rel)
        if not os.path.exists(path): print('なし:', rel); continue
        s = open(path, encoding='utf-8').read()
        ok = S in s and block(p).rstrip('\n') in s
        if check:
            if not ok: print('NG  未設定または古い:', rel); bad += 1
            continue
        r = inject(path, p); print(('追加/更新: ' if r else '変更なし: ') + rel)
    if check: return bad
    urls = [BASE + p['url'] for p in CFG['pages'].values() if p.get('sitemap', True)]
    open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(
      '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      ''.join('  <url><loc>%s</loc></url>\n' % escape(u) for u in urls) + '</urlset>\n')
    open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % BASE)
    print('書き出し: sitemap.xml robots.txt')
    return 0

if __name__ == '__main__':
    sys.exit(1 if main('--check' in sys.argv) else 0)
