#!/usr/bin/env python3
"""人物の経歴の回(土曜)や、人を主役にした投稿の材料を、相関図のデータから探す道具。読むだけ(サイトも inbox も変えない)。

使い方:
  node scripts/export_graph.js                 # 先に1回。src/lab/graph_raw.json ができる(会社の図の全部を1枚にしたもの。gitには入れない)
  python3 scripts/career_finder.py hoppers     # 渡り歩きが多い人(会社の数が多い順)
  python3 scripts/career_finder.py diaspora 会社名   # その会社の出身で、ほかにどこへ散ったか(例: OpenAI)
  python3 scripts/career_finder.py bridges     # 人の線とお金の線が同じ2社に重なっている組(意外なつながり)
  python3 scripts/career_finder.py person 名前  # 1人の経歴(年表・つながり・出典の手がかり)。日本語名でも英語名でも
  python3 scripts/career_finder.py between "Elon Musk" "Sam Altman"  # 2者(人・会社)のあいだの線と、共通の相手(★いちばん使う)
  python3 scripts/career_finder.py conflicts   # 対立・訴訟の2者と、もともと共通していた相手
  python3 scripts/career_finder.py coinvest    # 対立する2社の両方に出資している人・会社
  python3 scripts/career_finder.py chains [会社]  # 出資の連鎖
  python3 scripts/career_finder.py ties "Elon Musk"  # 中心人物と二重三重につながる人
  python3 scripts/career_finder.py pick 日付    # 土曜の経歴の回の候補を、上の3つから混ぜて10人ほど出す
  どれも --out ファイル.md で書き出せる(inbox/careers/ に置く場合は足すだけ)

見方の注意:
  ・「出身」「移籍先」の線(from / moved)は、相関図の会社の図ごとの線を合わせたもの。向き(どちらからどちらへ)は
    出典を開いて確かめてから書く。年がわかるのは、人物カードの役割(r)に年があるものだけ。
  ・材料は「手がかり」。投稿に使うときは、本人のX・公式・開示で経歴を確かめる(docs/post_calendar_2026-12.md の0章)。
"""
import sys, os, re, json, glob, argparse, collections, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'src', 'lab', 'graph_raw.json')
SCHOOL = re.compile(r'(大学|University|Univ\.|College|Institute of Technology|MIT$|Stanford|Oxford|Cambridge|学院|高校|School)', re.I)
PERSON_LINK = ('member', 'from', 'moved')      # 人と会社をつなぐ線
AI_ORGS = ['openai', 'anthropic', 'xai', 'meta', 'google deepmind', 'google', 'microsoft', 'nvidia', 'thinking machines lab', 'safe superintelligence',
           'cursor (anysphere)', 'mistral ai', 'scale ai', 'character.ai', 'perplexity', 'apple', 'amazon', 'tesla', 'spacex']   # pick で「AI会社を2社以上渡り歩いた人」を選ぶ目印
PASSIVE = re.compile(r'(blackrock|vanguard|state street|fidelity|信託|カストディ|norges|jp ?morgan|capital group)', re.I)   # 株を持つだけの大株主(意外性がないので外す)
MONEY_LINK = ('invest', 'invest2', 'deal')     # お金の線


def load():
    if not os.path.exists(RAW):
        sys.exit('src/lab/graph_raw.json がありません。先に `node scripts/export_graph.js` を実行してください(初回は npm install と npx playwright install chromium)。')
    g = json.load(open(RAW, encoding='utf-8'))
    N, E = g['nodes'], g['edges']
    orgs = {}                                   # 人の番号 -> {会社の番号: set(根拠)}
    for a, b, k, lab, since, d in E:
        if k not in PERSON_LINK:
            continue
        for p, o in ((a, b), (b, a)):
            if N[p]['t'] == 'p' and N[o]['t'] != 'p' and not SCHOOL.search(N[o]['n']):
                orgs.setdefault(p, {}).setdefault(o, set()).add(k)
    names = {}                                  # 会社名(小文字)-> 番号
    for i, n in enumerate(N):
        if n['t'] != 'p':
            names.setdefault(n['n'].lower(), i)
    # 人物カードの役割(会社名・役割・開始年・終了年)も会社の組に足す
    roles = {}
    for i, n in enumerate(N):
        if n['t'] == 'p' and n.get('r'):
            roles[i] = n['r']
            for co, role, y0, y1 in n['r']:
                j = names.get(str(co).lower())
                if j is not None and not SCHOOL.search(N[j]['n']):
                    orgs.setdefault(i, {}).setdefault(j, set()).add('role')
    return N, E, orgs, roles, names


def en_name(n):
    return n['k'][2:] if n['k'].startswith('p:') else ''


def label(n):
    e = en_name(n)
    return f"{n['n']}({e})" if e and e != n['n'] else n['n']


def person_orgs(N, orgs, i):
    return sorted(N[o]['n'] for o in orgs.get(i, {}))


def money_pairs(E):
    m = collections.Counter()
    for a, b, k, lab, since, d in E:
        if k in MONEY_LINK and a != b:
            m[(min(a, b), max(a, b))] += 1
    return m


def pair_people(orgs):
    """2社をまたぐ人の一覧(人の線で2社が重なる組)"""
    pp = collections.defaultdict(set)
    for p, od in orgs.items():
        ks = sorted(od)
        if len(ks) > 8:                          # 組み合わせが爆発するので、会社が多すぎる人は主な8社だけ
            ks = ks[:8]
        for x in range(len(ks)):
            for y in range(x + 1, len(ks)):
                pp[(ks[x], ks[y])].add(p)
    return pp


def cmd_hoppers(a, N, E, orgs, roles, names):
    rows = [(len(od), p) for p, od in orgs.items() if N[p]['t'] == 'p' and len(od) >= a.min]
    rows.sort(key=lambda r: (-r[0], N[r[1]]['n']))
    out = [f'# 渡り歩きが多い人(会社{a.min}社以上、{len(rows)}人。上位{a.top}人)', '']
    for n, p in rows[:a.top]:
        out.append(f"- **{label(N[p])}** … {n}社: " + '、'.join(person_orgs(N, orgs, p)[:10]))
    return out


def cmd_diaspora(a, N, E, orgs, roles, names):
    q = a.arg.lower()
    hit = [i for k, i in names.items() if k == q] or [i for k, i in names.items() if q in k]
    if not hit:
        return [f'「{a.arg}」という会社は相関図に見つかりません。']
    target = set(hit)
    alumni = []
    for p, od in orgs.items():
        if not (set(od) & target):
            continue
        kinds = set().union(*[od[o] for o in od if o in target])
        former = 'from' in kinds
        for co, role, y0, y1 in roles.get(p, []):
            if names.get(str(co).lower()) in target and (y1 or str(role).startswith('元')):
                former = True
        if former:
            alumni.append(p)
    out = [f'# {a.arg} の出身者と、ほかに加わった会社({len(alumni)}人)', '']
    dest = collections.Counter()
    for p in alumni:
        for o in orgs[p]:
            if o not in target:
                dest[N[o]['n']] += 1
    out.append('よく出てくる会社: ' + '、'.join(f'{k}({v})' for k, v in dest.most_common(12)))
    out.append('')
    for p in sorted(alumni, key=lambda p: -len(orgs[p])):
        others = [N[o]['n'] for o in orgs[p] if o not in target]
        out.append(f"- **{label(N[p])}** → " + ('、'.join(others[:8]) or '(ほかの会社の記録なし)'))
    return out


def cmd_bridges(a, N, E, orgs, roles, names):
    pp = pair_people(orgs)
    mp = money_pairs(E)
    rows = []
    for pair, people in pp.items():
        if pair in mp and len(people) <= a.max_people:
            rows.append((len(people), -mp[pair], pair, people))
    rows.sort()
    out = [f'# 人の線とお金の線が重なっている2社(人が{a.max_people}人以下・{len(rows)}組)', '',
           '「お金でつながる2社を、1人の人も結んでいる」組。人の数が少ないほど意外性がある。', '']
    for n, m, pair, people in rows[:a.top]:
        x, y = N[pair[0]]['n'], N[pair[1]]['n']
        out.append(f"- **{x} ⇄ {y}** … 人{n}人({'、'.join(label(N[p]) for p in sorted(people))[:80]})・お金の線{-m}本")
    return out


def find_person(N, q):
    ql = q.lower()
    ex = [i for i, n in enumerate(N) if n['t'] == 'p' and (n['n'].lower() == ql or en_name(n).lower() == ql)]
    return ex or [i for i, n in enumerate(N) if n['t'] == 'p' and (ql in n['n'].lower() or ql in en_name(n).lower())]


def hints(en, ja):
    """inbox/moves・deep の中の、その人の出典の手がかり"""
    out = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', '*', '20*.json'))):
        if os.path.basename(os.path.dirname(f)) not in ('moves', 'deep'):
            continue
        try:
            d = json.load(open(f, encoding='utf-8'))
        except (ValueError, OSError):
            continue
        for it in d.get('items', []) if isinstance(d, dict) else []:
            if not isinstance(it, dict):
                continue
            if (en and it.get('name_en', '').lower() == en.lower()) or (ja and it.get('name_ja') == ja):
                src = it.get('src') or []
                out.append(f"  - {os.path.relpath(f, ROOT)}: {it.get('from', '')} → {it.get('to', '')} ({it.get('date', '')}・{it.get('confidence', '')}) "
                           + ' / '.join(s[1] for s in src[:2] if isinstance(s, (list, tuple)) and len(s) > 1))
    return out


def card(N, E, orgs, roles, p):
    n = N[p]
    out = [f'## {label(n)}', '']
    rs = roles.get(p, [])
    if rs:
        out.append('年表(人物カードの役割。年は相関図の記録で、投稿前に本人・公式で確かめる):')
        for co, role, y0, y1 in sorted(rs, key=lambda r: (r[2] if isinstance(r[2], int) else 9999)):
            out.append(f"  - {y0 or '?'}〜{y1 or ''} {co} / {role}")
    od = orgs.get(p, {})
    if od:
        out.append('つながる会社: ' + '、'.join(f"{N[o]['n']}({'/'.join(sorted(k))})" for o, k in od.items()))
    others = collections.Counter()
    for a, b, k, lab, since, d in E:
        if k in ('conflict', 'link', 'member') and (a == p or b == p):
            o = b if a == p else a
            others[(N[o]['n'], k, lab)] += 1
    ppl = [x for x in others if x[1] in ('conflict', 'link')]
    if ppl:
        out.append('ほかの線: ' + '、'.join(f"{x[0]}[{x[1]}{':' + x[2] if x[2] else ''}]" for x in ppl[:8]))
    h = hints(en_name(n), n['n'])
    out.append('出典の手がかり(inbox):' + ('' if h else ' なし。本人のX・GitHub・公式ページを `python3 scripts/x_check.py @名前` などで探す'))
    out += h
    out.append('')
    return out


def cmd_person(a, N, E, orgs, roles, names):
    ps = find_person(N, a.arg)
    if not ps:
        return [f'「{a.arg}」という人物は見つかりません。']
    out = []
    for p in ps[:5]:
        out += card(N, E, orgs, roles, p)
    return out


def cmd_pick(a, N, E, orgs, roles, names):
    out = [f'# {a.arg} の経歴の回の候補(手がかり。確かめてから使う)', '']
    ai = {names[k] for k in AI_ORGS if k in names}
    ho = sorted(((len(set(od) & ai), p) for p, od in orgs.items() if len(od) >= 3 and len(set(od) & ai) >= 2 and N[p]['t'] == 'p'), reverse=True)
    pp = pair_people(orgs); mp = money_pairs(E)
    br = sorted((len(ps), pair) for pair, ps in pp.items() if pair in mp and len(ps) <= 2)
    chosen, seen = [], set()
    for n, p in ho[:6]:
        chosen.append(('渡り歩き', p)); seen.add(p)
    for n, pair in br[:30]:
        for p in sorted(pp[pair]):
            if p not in seen and len(orgs[p]) >= 2:
                chosen.append((f"お金と人の二重の線({N[pair[0]]['n']}⇄{N[pair[1]]['n']})", p)); seen.add(p); break
        if len(chosen) >= 10:
            break
    for why, p in chosen[:10]:
        out.append(f'### 切り口: {why}')
        out += card(N, E, orgs, roles, p)
    return out


KIND_JA = {'member': '所属', 'from': '出身', 'moved': '移籍', 'link': 'つながり', 'invest': '出資', 'invest2': '出資', 'deal': '取引',
           'owns': '保有', 'conflict': '対立・訴訟', 'govern': '統治', 'uses': '利用', 'fun': 'おもしろ'}


def adjacency(N, E):
    adj = collections.defaultdict(list)
    for a, b, k, lab, since, d in E:
        if a == b:
            continue
        adj[a].append((b, k, lab, since, '→'))
        adj[b].append((a, k, lab, since, '←'))
    return adj


def edge_txt(N, a, o, k, lab, since, arrow):
    j = KIND_JA.get(k, k)
    return f"{N[a]['n']} {arrow} {N[o]['n']}〔{j}{(':' + lab) if lab else ''}{('・' + str(since)) if since else ''}〕"


def one(N, q):
    r = find_person(N, q)
    if r:
        return r[0]
    ql = q.lower()
    ex = [i for i, n in enumerate(N) if n['n'].lower() == ql or en_name(n).lower() == ql] or [i for i, n in enumerate(N) if ql in n['n'].lower()]
    return ex[0] if ex else None


def cmd_between(a, N, E, orgs, roles, names):
    """2者(人でも会社でも)のあいだの線を、直接+1つ間に挟んだ線(共通の相手)+2つ挟んだ線まで全部出す"""
    if not a.arg2:
        sys.exit('between は2つ名前が要ります: between "Elon Musk" "Sam Altman"')
    x, y = one(N, a.arg), one(N, a.arg2)
    if x is None or y is None:
        return ['名前が相関図に見つかりません: ' + (a.arg if x is None else a.arg2)]
    adj = adjacency(N, E)
    out = [f"# {N[x]['n']} と {N[y]['n']} のあいだの線", '', '## 直接の線']
    d = [edge_txt(N, x, o, k, lab, since, ar) for o, k, lab, since, ar in adj[x] if o == y]
    out += ['- ' + t for t in d] or ['- なし']
    out += ['', '## 共通の相手(1人・1社をはさんでつながる)。2者が別の線で同じ相手につながっている']
    nx = {}
    for o, k, lab, since, ar in adj[x]:
        nx.setdefault(o, []).append((k, lab, since, ar))
    ny = {}
    for o, k, lab, since, ar in adj[y]:
        ny.setdefault(o, []).append((k, lab, since, ar))
    com = [o for o in nx if o in ny and o not in (x, y)]
    com.sort(key=lambda o: (N[o]['t'] != 'p', N[o]['n']))
    for o in com[:a.top]:
        out.append(f"- **{N[o]['n']}**({ {'p': '人', 'c': '会社', 'o': '会社', 'i': '投資家'}.get(N[o]['t'], '') }): "
                   + '/'.join(f"{N[x]['n']}の{KIND_JA.get(k, k)}{':' + lab if lab else ''}" for k, lab, s2, ar in nx[o][:2]) + ' ・ '
                   + '/'.join(f"{N[y]['n']}の{KIND_JA.get(k, k)}{':' + lab if lab else ''}" for k, lab, s2, ar in ny[o][:2]))
    if not com:
        out.append('- なし')
    out += ['', '## 2つ挟んだ線(人の線・出資の線だけ。長いほど「推測」の度合いが高い)']
    n2 = 0
    for o1, l1 in nx.items():
        if o1 in (x, y):
            continue
        for o2, k2, lab2, s2, ar2 in adj[o1]:
            if o2 in ny and o2 not in (x, y, o1) and n2 < a.top and N[o1]['t'] in 'pi' + 'c':
                out.append(f"- {N[x]['n']} — {N[o1]['n']} — {N[o2]['n']} — {N[y]['n']}  ({KIND_JA.get(l1[0][0], l1[0][0])}→{KIND_JA.get(k2, k2)}→{KIND_JA.get(ny[o2][0][0], ny[o2][0][0])})")
                n2 += 1
    out += ['', '※ 線の向きと意味は出典で確かめる。共通の相手がいるだけでは「関係がある」とは言えない(偶然・大企業どうしの一般的なつながりもある)。']
    return out


def cmd_conflicts(a, N, E, orgs, roles, names):
    """対立・訴訟・決裂の線がある2者について、対立の前に共通していたもの(共通の相手)を並べる"""
    adj = adjacency(N, E)
    rows = []
    for x, y, k, lab, since, d in E:
        if k != 'conflict':
            continue
        sx = {o for o, k2, *_ in adj[x] if k2 != 'conflict' and o != y and not PASSIVE.search(N[o]['n'])}
        sy = {o for o, k2, *_ in adj[y] if k2 != 'conflict' and o != x and not PASSIVE.search(N[o]['n'])}
        com = sx & sy
        rows.append((-len(com), N[x]['n'], N[y]['n'], lab, sorted(N[o]['n'] for o in com)))
    rows.sort()
    out = [f'# 対立・訴訟の線と、その2者の共通の相手({len(rows)}組)', '',
           '「いま敵対している2者が、もとは同じ会社・同じ投資家・同じ人につながっていた」ものを探す材料。理由は出典で確かめる。', '']
    for n, xa, ya, lab, com in rows[:a.top]:
        out.append(f"- **{xa} ⇄ {ya}**〔{lab}〕共通{-n}: " + ('、'.join(com[:10]) or 'なし'))
    return out


def cmd_coinvest(a, N, E, orgs, roles, names):
    """出資の線で、同じ出資者が競合・対立する2社の両方に出している組(=意外な共通の出資者)"""
    inv = collections.defaultdict(set)
    for x, y, k, lab, since, d in E:
        if k in ('invest', 'invest2'):
            inv[x].add(y)
    rival = set()
    for x, y, k, *_ in E:
        if k == 'conflict' and N[x]['t'] != 'p' and N[y]['t'] != 'p':
            rival.add((min(x, y), max(x, y)))
    rows = []
    for (x, y) in rival:
        both = [i for i, t in inv.items() if x in t and y in t and not PASSIVE.search(N[i]['n'])]
        if both:
            rows.append((-len(both), N[x]['n'], N[y]['n'], sorted(N[i]['n'] for i in both)))
    rows.sort()
    out = ['# 対立する2社の両方に出資している人・会社', '']
    for n, xa, ya, both in rows[:a.top]:
        out.append(f"- **{xa} ⇄ {ya}** の両方に出資: " + '、'.join(both[:8]))
    return out or ['該当なし']


def cmd_chains(a, N, E, orgs, roles, names):
    """出資の連鎖: A→B(出資)かつ B→C(出資・取引)で、AとCも別の線でつながっているものなどを、人物つきで出す"""
    inv = collections.defaultdict(set)
    for x, y, k, *_ in E:
        if k in ('invest', 'invest2'):
            inv[x].add(y)
    q = one(N, a.arg) if a.arg else None
    out = ['# 出資の連鎖(出資を受けた先が、さらに別の会社に出資している)', '']
    n = 0
    for x in ([q] if q is not None else list(inv)):
        for y in inv.get(x, ()):
            for z in inv.get(y, ()):
                if z != x and z not in inv.get(x, ()) and n < a.top and N[x]['t'] != 'p':
                    out.append(f"- {N[x]['n']} → {N[y]['n']} → {N[z]['n']}")
                    n += 1
    return out


def cmd_ties(a, N, E, orgs, roles, names):
    """中心人物(例: Elon Musk)と、二重三重につながる人: 直接の線+同じ会社に所属した数+共通の相手の数で並べる"""
    c = one(N, a.arg)
    if c is None:
        return ['人物が見つかりません: ' + a.arg]
    adj = adjacency(N, E)
    direct = collections.defaultdict(list)
    for o, k, lab, since, ar in adj[c]:
        if N[o]['t'] == 'p':
            direct[o].append(f"{KIND_JA.get(k, k)}{':' + lab if lab else ''}")
    mine = set(orgs.get(c, {}))
    nb = {o for o, *_ in adj[c] if not PASSIVE.search(N[o]['n'])}
    rows = []
    for p in range(len(N)):
        if p == c or N[p]['t'] != 'p':
            continue
        shared = mine & set(orgs.get(p, {}))
        com = {o for o, *_ in adj[p] if o in nb and o != c} - shared
        score = 3 * len(direct.get(p, [])) + 2 * len(shared) + len(com)
        if len(direct.get(p, [])) + len(shared) >= 1 and score >= 3:
            rows.append((-score, p, direct.get(p, []), sorted(N[o]['n'] for o in shared), sorted(N[o]['n'] for o in com)))
    rows.sort()
    out = [f"# {N[c]['n']} と二重三重につながる人(直接×3+同じ会社×2+共通の相手×1。上位{a.top})", '']
    for sc, p, d, sh, com in rows[:a.top]:
        out.append(f"- **{label(N[p])}** {-sc}点 … 直接:{'、'.join(d) or 'なし'} / 同じ会社:{'、'.join(sh) or 'なし'} / 共通の相手:{'、'.join(com[:6]) or 'なし'}")
    return out


def main():
    ap = argparse.ArgumentParser(description='人物の経歴の回の材料を探す(読むだけ)')
    ap.add_argument('cmd', choices=['hoppers', 'diaspora', 'bridges', 'person', 'pick', 'between', 'conflicts', 'coinvest', 'chains', 'ties'])
    ap.add_argument('arg', nargs='?', default='')
    ap.add_argument('arg2', nargs='?', default='')
    ap.add_argument('--min', type=int, default=4)
    ap.add_argument('--top', type=int, default=30)
    ap.add_argument('--max-people', type=int, default=2)
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.cmd in ('diaspora', 'person', 'ties') and not a.arg:
        sys.exit('会社名(または人物名)を付けてください')
    if a.cmd == 'pick' and not a.arg:
        a.arg = datetime.date.today().isoformat()
    N, E, orgs, roles, names = load()
    f = {'hoppers': cmd_hoppers, 'diaspora': cmd_diaspora, 'bridges': cmd_bridges, 'person': cmd_person, 'pick': cmd_pick, 'between': cmd_between, 'conflicts': cmd_conflicts, 'coinvest': cmd_coinvest, 'chains': cmd_chains, 'ties': cmd_ties}[a.cmd]
    text = '\n'.join(f(a, N, E, orgs, roles, names))
    if a.out:
        if os.path.exists(a.out):
            sys.exit(f'{a.out} はすでにあります(上書きしません)')
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, 'w', encoding='utf-8').write(text + '\n')
        print('書き出しました:', a.out)
    else:
        print(text)


if __name__ == '__main__':
    main()
