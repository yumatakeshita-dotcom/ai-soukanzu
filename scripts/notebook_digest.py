# AI相関図の全体を、Gemini Notebookに送れる1つのMarkdownにまとめる。
# 使い方: node scripts/export_graph.js の後に  python3 scripts/notebook_digest.py
# 出力: notebook/ai-soukanzu-digest.md
import json, os, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
g = json.load(open(os.path.join(ROOT, 'src', 'lab', 'graph_raw.json'), encoding='utf-8'))
N, E = g['nodes'], g['edges']
KIND = {'deal': '取引', 'invest': '出資', 'invest2': '出資(2)', 'moved': '移籍',
        'conflict': '対立', 'from': '出身', 'link': 'つながり', 'uses': '利用',
        'govern': '支配', 'owns': '保有', 'member': '所属'}
MAX_LINES = 60  # 1社あたりの出力の上限

centers = [i for i, n in enumerate(N) if n['t'] == 'c']
adj = collections.defaultdict(list)
for e in E:
    adj[e[0]].append(e)
    adj[e[1]].append(e)

def name(i):
    return N[i]['n']

out = []
out.append('# AI企業の相関図 まとめ\n')
out.append('AI企業・半導体企業の人・出資・取引・移籍のつながりをまとめたものです。')
out.append(f'会社 {len(centers)} 件、人物 {sum(1 for n in N if n["t"]=="p")} 件、組織 {sum(1 for n in N if n["t"] in ("i","o"))} 件、'
           f'つながり {len(E)} 件を含みます。\n')

for c in sorted(centers, key=lambda i: -len(adj[i])):
    out.append(f'## {name(c)}\n')
    rows = sorted(adj[c], key=lambda e: (e[2] not in ('deal', 'moved', 'govern', 'conflict'), str(e[4])))
    count = 0
    for e in rows:
        if count >= MAX_LINES:
            out.append(f'- ほか {len(rows) - count} 件(省略)')
            break
        other = e[1] if e[0] == c else e[0]
        if other == c:
            continue
        kind = KIND.get(e[2], e[2] or '')
        label = e[3] or ''
        since = f'({e[4]})' if e[4] else ''
        detail = e[5] if e[2] == 'deal' and e[5] else ''
        line = f'- [{kind}] {name(other)} {since} {label}'.rstrip()
        if detail:
            line += f' — {detail}'
        out.append(line)
        count += 1
    out.append('')

os.makedirs(os.path.join(ROOT, 'notebook'), exist_ok=True)
path = os.path.join(ROOT, 'notebook', 'ai-soukanzu-digest.md')
open(path, 'w', encoding='utf-8').write('\n'.join(out))
print(path, 'bytes', os.path.getsize(path), 'lines', len(out))
