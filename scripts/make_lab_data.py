# export_graph.js / export_flows.js の結果から、ラボ用のデータを作る。
#  - site/lab/graph.json : ①つながり最短ルート用(表記ゆれをまとめ、信託銀行など「株を持つだけ」の組織に印)
#  - src/lab/cards.json  : ⑤トレカ用(AI関連の人物120人とレア度)
#  - src/lab/flows.json  : ④移籍マップ用(主要AI企業どうしの移籍)
# 使い方: node scripts/export_graph.js && node scripts/export_flows.js && python scripts/make_lab_data.py && npm run build-lab
import json,re,collections,os
R=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
g=json.load(open(os.path.join(R,'src/lab/graph_raw.json'),encoding='utf8'))
alias={'o:yコンビネータ':'o:ycombinator','o:yコンビネーター':'o:ycombinator','o:softbank':'o:ソフトバンクグループ','o:ソフトバンク':'o:ソフトバンクグループ','o:googlebrain':'o:googledeepmind','o:エヌビディア':'o:nvidia','o:オープンai':'o:openai','o:マイクロソフト':'o:microsoft','o:アマゾン':'o:amazon','o:メタ':'o:meta','o:アンソロピック':'o:anthropic','o:google':'o:alphabet','o:spacex旧xai':'o:spacex'}
newidx={};nodes=[];remap=[]
for n in g['nodes']:
    k=alias.get(n['k'],n['k'])
    if k not in newidx: newidx[k]=len(nodes);nodes.append({'n':n['n'],'t':n['t'],'k':k})
    remap.append(newidx[k])
passive=re.compile(r'(信託|カストディ|vanguard|blackrock|state ?street|jp ?morgan|chase bank|master ?trust|mellon|ssbtc|norway|持株会|自己株|ノルウェー|生命保険|custody|nominee|bnym|goldman sachs international|citibank|hsbc|morgan stanley & co|ステート|ジェーピー|バンク・オブ|ゴールドマン|シティバンク|モルガン|証券金融)',re.I)
seen=set();E=[]
for a,b,k,lab,since,d in g['edges']:
    A,B=remap[a],remap[b]
    if A==B or (A,B,k) in seen: continue
    seen.add((A,B,k));E.append([A,B,k,lab])
json.dump({'n':[[x['n'],x['t'],1 if passive.search(x['n']) else 0] for x in nodes],'e':E},open(os.path.join(R,'site/lab/graph.json'),'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
AI={'OpenAI','Anthropic','xAI','Meta','Google DeepMind','Microsoft','Thinking Machines Lab','Safe Superintelligence','Mistral AI','Nvidia','Apple','Amazon','Tesla','Perplexity','Cohere','Scale AI','Databricks','Hugging Face','Sakana AI','Preferred Networks','Cursor (Anysphere)','Anysphere (Cursor)','ソフトバンクグループ','Character.AI','Figure AI','Reflection AI','DeepSeek','Moonshot AI','Inflection AI','Alphabet','PKSHA Technology','Rakuten','LY Corporation','Arm','TSMC','ASML','SK hynix','Samsung','Stripe','Notion','Figma','Canva','Slack','Waymo','Mercari','メルカリ'}
deg=collections.Counter();inv=collections.Counter()
for a,b,k,*_ in g['edges']:
    deg[a]+=1;deg[b]+=1
    if k in('invest','invest2'): inv[a]+=1
cards=[]
for i,n in enumerate(g['nodes']):
    if n['t']!='p' or not n.get('r'): continue
    cos=sorted({r[0] for r in n['r']})
    if not set(cos)&AI: continue
    en=n['k'][2:] if n['k'].startswith('p:') else ''
    roles=[r for r in n['r'] if r[1]]
    cur=next((r for r in roles if not r[3]),roles[0] if roles else ['','','',''])
    founder=any('創業' in (r[1] or '') or 'founder' in (r[1] or '').lower() for r in n['r'])
    cards.append({'n':n['n'],'en':en if re.search('[A-Za-z]',en) else '','d':deg[i],'c':len(cos),'v':inv[i],'f':int(founder),'co':cos[:6],'role':(cur[0]+' '+(cur[1] or '')).strip()[:40]})
cards.sort(key=lambda c:-(c['d']+3*c['c']+2*c['v']+5*c['f']));cards=cards[:120]
for i,c in enumerate(cards):
    p=i/len(cards);c['rar']='SSR' if p<0.06 else 'SR' if p<0.22 else 'R' if p<0.55 else 'N'
json.dump(cards,open(os.path.join(R,'src/lab/cards.json'),'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
F=json.load(open(os.path.join(R,'src/lab/flows_raw.json'),encoding='utf8'))
M={'Google Brain':'Google DeepMind','Cursor (Anysphere)':'Cursor','Anysphere (Cursor)':'Cursor'}
ORG={'OpenAI','Anthropic','Meta','Google DeepMind','Microsoft','xAI','Thinking Machines Lab','Safe Superintelligence','Mistral AI','Cohere','Sakana AI','Inflection AI','Scale AI','Apple','Nvidia','Stripe','Reflection AI','Perplexity','Databricks','SpaceX','Tesla','Eureka Labs','AMI Labs','Groq','Holistic','Ineffable Intelligence','Discovery Loop','Sierra','Cursor'}
fl=[];s2=set()
for f in F:
    a=M.get(f['from'],f['from']);b=M.get(f['to'],f['to'])
    if a in ORG and b in ORG and a!=b and (f['p'],a,b) not in s2:
        s2.add((f['p'],a,b))
        try: y=int(str(f['y'])[:4])
        except: y=None
        fl.append({'p':f['p'],'en':f['en'] if re.search('[A-Za-z]',f['en']) else '','a':a,'b':b,'y':y})
json.dump(fl,open(os.path.join(R,'src/lab/flows.json'),'w',encoding='utf8'),ensure_ascii=False,separators=(',',':'))
print('graph',len(nodes),'nodes /',len(E),'edges; cards',len(cards),'; flows',len(fl))
