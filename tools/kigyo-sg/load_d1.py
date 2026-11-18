import json,os,sys,urllib.request,time
DB="https://api.cloudflare.com/client/v4/accounts/b7b515e722cbecf8000c746711d00a41/d1/database/b1b4af48-9eac-402d-be0e-2b91cc6d01f2/query"
def q(sql,params=None):
    body=json.dumps({"sql":sql,"params":params or []}).encode()
    for t in range(4):
        try:
            r=urllib.request.urlopen(urllib.request.Request(DB,body,{"Content-Type":"application/json","Authorization":"Bearer x"}),timeout=120)
            return json.loads(r.read())
        except urllib.error.HTTPError as e:
            x=e.read(); print(e.code,x[:300]); 
            if e.code<500: raise
        except Exception as e: print('retry',e)
        time.sleep(3*(t+1))
    raise SystemExit('failed')
q("CREATE TABLE IF NOT EXISTS f (path TEXT PRIMARY KEY, data TEXT NOT NULL) WITHOUT ROWID")
have={r['path'] for r in q("SELECT path FROM f")['result'][0]['results']}
files=[]
for d in ('c','n'):
    for fn in os.listdir('sg/'+d): files.append(f'/{d}/{fn}')
files.sort(key=lambda p:(p.endswith('meta.json'),p))  # meta.json を最後に
from concurrent.futures import ThreadPoolExecutor
def put(p):
    q("INSERT OR IGNORE INTO f (path,data) VALUES (?,?)",[p,open('sg'+p).read()])
todo=[p for p in files if p not in have and not p.endswith('meta.json')]
with ThreadPoolExecutor(8) as ex:
    for i,_ in enumerate(ex.map(put,todo),1):
        if i%100==0: print(i,flush=True)
# 件数の情報(meta.json)は、ほかが全部入ってから最後に入れる(途中の状態でサイトに出ないように)
if '/c/meta.json' not in have: put('/c/meta.json')
n=len(todo)
c=q("SELECT count(*) c, sum(length(data)) s FROM f")['result'][0]['results'][0]
print('added',n,'now',c)
