import urllib.request,urllib.parse,json,sys,time
sys.stdout.reconfigure(encoding='utf-8')
H={'User-Agent':'relationship-map-research/1.0 (personal use)'}
def g(p):
    for i in range(4):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request('https://www.wikidata.org/w/api.php?'+urllib.parse.urlencode(p),headers=H),timeout=60).read())
        except Exception as e: time.sleep(20 if '429' in str(e) else 3)
for n in ['Sequoia Capital','Andreessen Horowitz','Founders Fund','Accel','Kleiner Perkins','Benchmark','Greylock Partners','Lightspeed Venture Partners','General Catalyst','Insight Partners','Thrive Capital','SoftBank Vision Fund']:
    r=g({'action':'wbsearchentities','search':n,'language':'en','type':'item','limit':1,'format':'json'})
    it=(r or {}).get('search',[])
    if not it: print(n,'none'); continue
    q=it[0]['id']
    e=g({'action':'wbgetentities','ids':q,'props':'claims|labels','format':'json'})['entities'][q]
    print(n,q,it[0].get('description','')[:40],'P1830:',len(e['claims'].get('P1830',[])),'P355:',len(e['claims'].get('P355',[])))
    time.sleep(1)
