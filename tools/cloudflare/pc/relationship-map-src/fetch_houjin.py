"""国税庁 法人番号公表サイトから、全件データ(CSV・Unicode)のzipを取得する。保存先は引数。使い方: python -I fetch_houjin.py 保存先フォルダ ファイル番号"""
import http.cookiejar, os, re, sys, urllib.parse, urllib.request
dest, fno = sys.argv[1], sys.argv[2]
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA = {'User-Agent': 'Mozilla/5.0 (compatible; relationship-map-research/1.0; personal use)'}
u = 'https://www.houjin-bangou.nta.go.jp/download/zenken/index.html'
page = op.open(urllib.request.Request(u, headers=UA), timeout=60).read().decode('utf-8', 'replace')
tok = re.search(r'name="(jp\.go\.nta[^"]*token)" value="([^"]*)"', page)
data = urllib.parse.urlencode({tok.group(1): tok.group(2), 'event': 'download', 'selDlFileNo': fno}).encode()
r = op.open(urllib.request.Request(u, data=data, headers=UA), timeout=600)
cd = r.headers.get('Content-Disposition', '')
name = re.search(r'filename="?([^";]+)', cd)
name = name.group(1) if name else 'zenken_%s.zip' % fno
path = os.path.join(dest, os.path.basename(name))
n = 0
with open(path, 'wb') as f:
    while True:
        b = r.read(1 << 20)
        if not b:
            break
        f.write(b)
        n += len(b)
print(path, n, r.headers.get('Content-Type'), cd)
