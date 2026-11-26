#!/usr/bin/env python3
"""主要AI企業の「薄さ」一覧を作る(読むだけ・サイトは変えない)。
使い方: node scripts/depth_score.js && python3 scripts/depth_rank.py
inbox/depth/raw.json(相関図の線・人物の数)から inbox/depth/latest.json と latest.md を作る。
薄さ=100に近いほど情報が少ない。同じ日に何度動かしても同じ。"""
import json,os,datetime
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEYS="openai anthropic xai meta tml ssi gdm msft mistral sakana nvidia pfn perplexity cohere scale databricks hf cursor amilabs st_cognition st_lovable st_harvey st_elevenlabs st_figure st_cerebras st_groq st_replit st_runway st_midjourney st_characterai st_bfl st_reflection st_moonshot st_zhipu st_deepseek st_coreweave st_glean st_sierra st_pi st_skild st_together st_poolside st_lambda st_bytedance aq_manus alibaba minimax".split()
DIMS=[('資金',['invest','invest2'],8),('幹部',['member'],10),('移籍',['from','moved'],8),('提携',['deal','uses','link'],6),('子会社',['owns'],3)]
raw={x['key']:x for x in json.load(open(os.path.join(ROOT,'inbox/depth/raw.json')))}
rows=[]
for k in KEYS:
    x=raw.get(k)
    if not x: continue
    tot=0;vals={}
    for n,ks,full in DIMS:
        v=x['people'] if n=='幹部' else sum(x['kinds'].get(a,0) for a in ks)
        vals[n]=v;tot+=min(1,v/full)
    rows.append((round(100*(1-tot/len(DIMS))),x['name'],k,vals))
rows.sort(key=lambda t:-t[0])
today=datetime.date.today().isoformat()
json.dump([{'thin':a,'name':b,'key':c,'dims':d} for a,b,c,d in rows],open(os.path.join(ROOT,'inbox/depth/latest.json'),'w'),ensure_ascii=False,indent=1)
L=[f'# 主要AI企業の「薄さ」一覧({today})','','薄さ=100に近いほど情報が少ない。目安: '+'・'.join(f'{n}{f}' for n,_,f in DIMS)+'。','','| 薄さ | 会社 | '+' | '.join(n for n,_,_ in DIMS)+' |','|---|---|'+'---|'*len(DIMS)]
for a,b,c,d in rows: L.append(f'| {a} | {b} | '+' | '.join(str(d[n]) for n,_,_ in DIMS)+' |')
open(os.path.join(ROOT,'inbox/depth/latest.md'),'w').write('\n'.join(L)+'\n')
print(len(rows),'社',today)
