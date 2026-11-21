# ラボの6ページを組み立てて site/lab/ に書き出す。
# 使い方: npm run build-lab (または src/lab で python build.py route.html ...)
# 各ページの /*BASE*/ に共通の色と書体(base.css)を、/*DATA:cards*/ などに同じフォルダのJSONを差し込む。
import sys,os
here=os.path.dirname(os.path.abspath(__file__))
out=os.path.join(here,'..','..','site','lab')
os.makedirs(out,exist_ok=True)
base=open(os.path.join(here,'base.css'),encoding='utf8').read()
HEAD='<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
for f in sys.argv[1:] or ['route.html','stop.html','money.html','moves.html','cards.html','sports.html']:
    s=open(os.path.join(here,f),encoding='utf8').read().replace('/*BASE*/',base)
    for data in ['cards','flows']:
        tag='/*DATA:%s*/'%data
        if tag in s: s=s.replace(tag,open(os.path.join(here,data+'.json'),encoding='utf8').read())
    open(os.path.join(out,f),'w',encoding='utf8').write(HEAD+s+'\n</body>\n</html>\n')
    print('書き出し:',f)

# 法的ページへのフッターリンクを入れ直す(scripts/legal.py。設定がOFFなら何も足さない)
import subprocess
subprocess.run([sys.executable,os.path.join(here,'..','..','scripts','legal.py')],check=False)
# 共有カード用の meta(title・OGP)を入れ直す。scripts/seo.py は何度動かしても同じ結果
import subprocess
subprocess.run([sys.executable,os.path.join(here,'..','..','scripts','seo.py')],check=False)
