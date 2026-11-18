import urllib.request,re,sys,html,json,urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (personal use; internal relationship map)'}
def g(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read().decode('utf-8','replace')
    except Exception as e: return ''
# 題名に「調達」「出資」「増資」を含む発表のみ。検索の見出しを拾う
seen={}
for kw in ['資金調達を実施','シリーズA 調達','シリーズB 調達','第三者割当増資 引受先','億円 調達 リード投資家']:
    for pg in (1,2):
        h=g('https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=%s&search_pattern=1&pagenum=%d'%(urllib.parse.quote(kw),pg))
        for m in re.finditer(r'href="(/main/html/rd/p/[0-9.]+\.html)"[^>]*>(.*?)</a>',h,flags=re.S):
            t=html.unescape(re.sub(r'<[^>]+>','',m.group(2))).strip()
            if re.search(r'調達|出資|増資|引受',t) and m.group(1) not in seen: seen[m.group(1)]=t
print(len(seen))
for k,v in list(seen.items())[:25]: print(k,v[:80])
