"""大企業が買収した会社・子会社の図(自動作成)。
元データ: acq_cos.json(fetch_acq_cos.py。Wikidata: 創業者・CEO・会長・所有者・親会社)と acq_names.txt(買収元の表示名)。
作る条件: 人物か出資者・親会社の記録が1つ以上あり、既存の図にない会社。買収元の会社も、図の中で『親会社・買収元』として載せる。"""
import json, os, re

from newco_data import mk, std
from newco_uni import n2

S = os.path.dirname(os.path.abspath(__file__))
MAXMAPS = 1800
NOTE = ('この会社は、大企業が買収した会社・子会社の一覧(英語版Wikipediaの「買収の一覧」とWikidataの「子会社・所有」)から自動で作った図です(2026年11月)。'
        '創業者・CEO・会長・株主はWikidataの記録に基づき、記録のない人は載っていません。買収の金額・時期は一覧にあるものだけで、人物の名前は記録の言語のままです。')
ROLE = {'founder': ('創業者', 'p'), 'ceo': ('CEO(Wikidata)', 'p'), 'chair': ('会長(Wikidata)', 'p'), 'owner': ('株主(個人・Wikidata)', 'i')}


def _n(s):
    return re.sub(r'[^a-z0-9ぁ-んァ-ヶ一-龥]', '', (s or '').lower())


# 手で調べた図: 大企業の買収先のうち、Wikidataに人物の記録が少ない最近の案件(出どころは各説明に記載)
def _manual():
    SRCN = '英語版Wikipedia「Manus (AI agent)」、CNBC(2026-10-08)、Bloombergの報道(2026年)'
    N = [
     {'id': 'co', 'name': 'Manus AI', 'kind': 'c', 'from': 2022, 'desc': 'AIエージェント「Manus」を開発する企業(運営はシンガポールのButterfly Effect Pte.)。2025年12月にMetaが買収を発表(報道では約20億ドル)したが、中国当局が2026年4月に阻止し、6月にMetaが関係解消を発表。8月に独立企業として続けると発表し、10月に5億ドル超を調達(%s)。' % SRCN},
     {'id': 'xiao', 'name': 'Xiao Hong(肖弘)', 'kind': 'p', 'from': 2022, 'desc': '2022年にButterfly Effectを設立した創業者。', 'role': '創業者', 'founder': 1},
     {'id': 'ji', 'name': 'Ji Yichao(通称Peak)', 'kind': 'p', 'from': 2022, 'desc': 'Manusの共同創業者でチーフサイエンティスト。1992年生まれで、2012年にPeak Labsを設立。', 'role': '共同創業者 / チーフサイエンティスト', 'founder': 1},
     {'id': 'zhang', 'name': 'Zhang Tao', 'kind': 'p', 'from': 2022, 'desc': '創業チームに加わり、プロダクトディレクターを務めた(Bloombergは3人目の創業者と報道)。', 'role': 'プロダクトディレクター', 'founder': 1},
     {'id': 'chetan', 'name': 'Chetan Puttagunta', 'kind': 'p', 'from': 2025, 'desc': 'BenchmarkのGeneral Partner。2025年4月の出資の際に取締役会に加わった。', 'role': '取締役(Benchmark)'},
     {'id': 'zhenfund', 'name': 'ZhenFund(真格基金)', 'kind': 'i', 'from': 2023, 'desc': '2023年のシードラウンドを主導。', 'role': 'シード主導'},
     {'id': 'hsg', 'name': 'HSG(旧Sequoia China、紅杉中国)', 'kind': 'i', 'from': 2024, 'desc': '2024年11月のシリーズAに参加。', 'role': 'シリーズA参加'},
     {'id': 'tencent', 'name': 'Tencent', 'kind': 'i', 'from': 2024, 'desc': '2024年11月のシリーズAに参加。2026年10月の調達でも既存株主として追加出資。', 'role': '出資'},
     {'id': 'benchmark', 'name': 'Benchmark', 'kind': 'i', 'from': 2025, 'desc': '2025年4月のシリーズB(約7,500万ドル、企業価値は約5億ドルとされる)を主導。', 'role': 'シリーズB主導'},
     {'id': 'wang', 'name': 'Wang Huiwen(王慧文)', 'kind': 'i', 'from': 2025, 'desc': 'Meituan共同創業者。2025年4月のシリーズBに個人として参加。', 'role': '出資(個人)'},
     {'id': 'ofc', 'name': 'Old Friendship Capital', 'kind': 'i', 'from': 2025, 'desc': '2025年4月のシリーズBに参加。', 'role': '出資'},
     {'id': 'boyu', 'name': 'Boyu Capital', 'kind': 'i', 'from': 2026, 'desc': '2026年10月の5億ドル超の調達を主導(CNBC)。', 'role': '2026年調達を主導'},
     {'id': 'idg', 'name': 'IDG Capital', 'kind': 'i', 'from': 2026, 'desc': '2026年10月の5億ドル超の調達を主導(CNBC)。', 'role': '2026年調達を主導'},
     {'id': 'meta', 'name': 'Meta', 'kind': 'i', 'from': 2025, 'to': 2026, 'desc': '2025年12月に買収を発表(報道では約20億ドル)。中国の国家発展改革委員会が2026年4月27日に阻止し、2026年6月15日にMetaが関係解消を発表しました。', 'role': '買収を発表→撤回'},
    ]
    EN = {'xiao': 'Xiao Hong', 'ji': 'Ji Yichao', 'zhang': 'Zhang Tao', 'chetan': 'Chetan Puttagunta', 'wang': 'Wang Huiwen'}
    return mk(N, std('co'), EN, {}, {}, {}, {}, {}, 'co')


def build(existing):
    f = os.path.join(S, 'acq_cos.json')
    ac = json.load(open(f, encoding='utf-8')) if os.path.exists(f) else {}
    names = {}
    for ln in open(os.path.join(S, 'acq_names.txt'), encoding='utf-8'):
        if '=' in ln:
            k, v = ln.rstrip('\n').split('=', 1)
            names[k] = v
    co0, lst0 = {}, []
    if n2('Manus AI') not in existing:
        co0['aq_manus'] = _manual()
        lst0.append({'key': 'aq_manus', 'name': 'Manus AI', 'min': 2022, 'note': '人物・出資者は英語版Wikipediaと報道(CNBC、Bloomberg)に基づく手作業の図です。出資の金額・時期は報道ベースで、評価額は非公表です。'})
    import newco_acqtop
    for _k, (_mp, _note) in newco_acqtop.maps().items():
        _nm = _mp['N'][0]['name']
        if n2(_nm) and n2(_nm) in existing:      # 日本語だけの名前はn2が空になるので、存在確認の対象にしない
            continue
        co0[_k] = _mp
        lst0.append({'key': _k, 'name': _nm, 'min': _mp['N'][0]['from'], 'note': _note})
    cand = []
    for q, c in ac.items():
        nm = c.get('ja') or c.get('en') or c.get('name')
        if not nm or n2(c.get('en') or nm) in existing or n2(nm) in existing:
            continue
        if not c['people']:      # 人物の記録がない会社は、図を作らない(親会社だけの図は情報が薄い)
            continue
        cand.append((q, c, nm))
    cand.sort(key=lambda t: (-len(t[1]['people']), -len(t[1]['parents'])))
    co, lst, used, seen_names = dict(co0), list(lst0), set(co0), {n2('Manus AI')} | {n2(x['name']) for x in lst0}
    for q, c, nm in cand[:MAXMAPS * 2]:
        if len(lst) >= MAXMAPS:
            break
        x = n2(c.get('en') or nm)
        if x in seen_names:
            continue
        seen_names.add(x)
        ys = [p['y'] for p in c['parents'] if p.get('y')]
        year = min(ys) if ys else 2010
        par = [names[p['k']] for p in c['parents'] if p['k'] in names]
        par = list(dict.fromkeys(par))
        desc = '%s(%s)。' % (nm, ('、'.join(par[:3]) + 'に買収された会社・子会社') if par else '大企業の買収先・子会社')
        if ys:
            desc += '買収・取得の記録は%d年。' % year
        N = [{'id': 'co', 'name': nm, 'kind': 'c', 'from': year, 'desc': desc}]
        EN, seen, i = {}, {_n(nm)}, 0
        order = {'founder': 0, 'ceo': 1, 'chair': 2, 'owner': 3}
        for p in sorted(c['people'], key=lambda x: order.get(x['role'], 9)):
            pn = p.get('ja') or p.get('en')
            if not pn or _n(pn) in seen:
                continue
            seen.add(_n(pn))
            role, kind = ROLE[p['role']]
            i += 1
            d = {'id': 'p%d' % i, 'name': pn, 'kind': kind, 'from': p.get('from') or year, 'desc': 'Wikidataの記録(2026年11月取得)。', 'role': role}
            if p['role'] == 'founder':
                d['founder'] = 1
                d['from'] = year
            N.append(d)
            if p.get('en'):
                EN['p%d' % i] = p['en']
        for pn in par[:4]:
            if _n(pn) in seen:
                continue
            seen.add(_n(pn))
            i += 1
            N.append({'id': 'a%d' % i, 'name': pn, 'kind': 'i', 'from': year, 'desc': '買収元・親会社(英語版Wikipediaの買収一覧、またはWikidataの子会社の記録)。', 'role': '親会社・買収元'})
        for o in c['orgs']:
            on = o.get('ja') or o.get('en')
            if not on or _n(on) in seen:
                continue
            seen.add(_n(on))
            i += 1
            N.append({'id': 'o%d' % i, 'name': on, 'kind': 'i', 'from': year, 'desc': 'Wikidataの「%s」の記録(2026年11月取得)。' % ('親会社' if o['role'] == 'parent' else '所有者'), 'role': '親会社・株主(Wikidata)'})
        if len(N) < 3:
            continue
        key = 'aq_' + (_n(c.get('en') or nm)[:22] or 'x')
        while key in used:
            key += 'x'
        used.add(key)
        co[key] = mk(N, std('co'), EN, {}, {}, {}, {}, {}, 'co')
        lst.append({'key': key, 'name': nm, 'min': year, 'note': NOTE})
    return co, lst
