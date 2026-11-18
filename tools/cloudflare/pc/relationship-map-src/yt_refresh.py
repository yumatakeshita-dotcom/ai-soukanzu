"""人物の出演動画(YouTube検索)を読む順番。対象は x_targets の人物(有名な人)+企業家・スタートアップ(x_queue_biz)。海外の人物も含む。
  python yt_refresh.py next [n]   … 読む人 n 人(既定9)と検索語。読んだ日が古い順(未確認が先)、有名度が高い順
  python yt_refresh.py mark 名前.. … 読んだ印
状態は yt_people_state.json。1人ごとに検索(sp=CAI%253D=アップロード日順)を1回、5秒あける。"""
import datetime as dt, json, os, sys, urllib.parse
S = os.path.dirname(os.path.abspath(__file__))
ST = os.path.join(S, 'yt_people_state.json')
state = json.load(open(ST, encoding='utf8')) if os.path.exists(ST) else {}
fame = json.load(open(os.path.join(S, 'people_fame.json'), encoding='utf8'))
soc = json.load(open(os.path.join(S, 'people_social.json'), encoding='utf8'))
names = []
tg = json.load(open(os.path.join(S, 'x_targets.json'), encoding='utf8'))
for x in tg: names.append((x['name'], 99))
for o in json.load(open(os.path.join(S, 'x_queue_biz.json'), encoding='utf8')): names.append((o['name'], o['fame']))
# 個人名のみ(企業アカウントは除く)。x_targets に混じる会社名は手で除く
skip = set('Thinking Machines Lab,Nvidia,Cisco,Safe Superintelligence,Google DeepMind,Microsoft,OpenAI,Anthropic,Mistral AI,Sakana AI,SoftBank Group,xAI,Scale AI,Databricks,Hugging Face,Uber,Waymo,Perplexity,Cohere,Figma,Stripe,Canva,Anysphere (Cursor),DoorDash,Notion,Slack,Mercari,Bluesky,X,cohere'.split(','))
seen = set(); rows = []
for n, f in names:
    if not n or n in skip or n in seen: continue
    seen.add(n); rows.append((n, f))
today = dt.date.today().isoformat()
cmd = sys.argv[1] if len(sys.argv) > 1 else 'next'
if cmd == 'mark':
    for n in sys.argv[2:]: state[n] = today
    json.dump(state, open(ST, 'w', encoding='utf8'), ensure_ascii=False); print('記録', len(sys.argv) - 2)
else:
    rows.sort(key=lambda r: (state.get(r[0], '0000'), -r[1]))
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 9
    for nm, f in rows[:n]:
        print(nm, '|', 'https://www.youtube.com/results?search_query=' + urllib.parse.quote_plus(nm + ' interview') + '&sp=CAI%253D')
    print('対象', len(rows), '人 / 読んだ', len(state), '人')
