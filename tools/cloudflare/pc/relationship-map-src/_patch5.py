p='hub_template.html';h=open(p,encoding='utf-8').read()
fn=open('_all_fn.js',encoding='utf-8').read()
a='<button type="button" data-h="world">世界の企業</button>'
assert a in h and 'data-h="all"' not in h
h=h.replace(a,a+'<button type="button" data-h="all">全企業リスト</button>',1)
a="world:()=>showWorld(),su:()=>showStartups(),jp:"
assert a in h;h=h.replace(a,"world:()=>showWorld(),all:()=>showAll(),su:()=>showStartups(),jp:",1)
a="world:()=>showWorld(),su:()=>showStartups()};"
assert a in h;h=h.replace(a,"world:()=>showWorld(),all:()=>showAll(),su:()=>showStartups()};",1)
a="/^世界の企業/.test(t)?'world':"
assert a in h;h=h.replace(a,a+"/^全企業リスト/.test(t)?'all':",1)
a="    ['world','世界の企業',"
assert a in h;h=h.replace(a,"    ['all','全企業リスト','米国・東証の上場企業と、Wikipediaに記事のある世界の会社(検索できます)'],\n"+a,1)
a="const worldState="
assert a in h;h=h.replace(a,fn+a,1)
open(p,'w',encoding='utf-8').write(h);print('ok')
