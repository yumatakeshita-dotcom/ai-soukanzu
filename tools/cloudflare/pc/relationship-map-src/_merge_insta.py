"""公開中の最新版(他のセッションが足した内容を含む)に、こちらで足した分(Instagram・独立した会社の図・Metaの人物・出典リンク)だけを重ねる。何度実行しても同じ結果になる。
使い方: python -I _merge_insta.py <公開中の最新版のファイル>   → output\\relationship-maps.html を、重ねた結果で上書きする
(上書き前に、手元のビルド結果は .mine-instagram.bak に残す)"""
import re, shutil, sys
LIVE = sys.argv[1]
MINE = r'C:\Users\yumat\.claude\output\relationship-maps.html'
shutil.copy(MINE, MINE + '.mine-instagram.bak')
a = open(LIVE, encoding='utf-8').read().split('\n')
b = open(MINE, encoding='utf-8').read().split('\n')
KEYS = ['instagram', 'artifact', 'whatsapp', 'signal', 'oculus', 'amilabs', 'eureka', 'periodic', 'mirendil', 'humans', 'covariant', 'appliedcompute', 'carelesspeople', 'adept']




def find(lines, pred, what):
    ix = [i for i, x in enumerate(lines) if pred(x)]
    assert len(ix) == 1, (what, len(ix))
    return ix[0]


# 1. Metaの図(N・EN・つながり・WIKI・LINKS・X)
isN = lambda x: x.startswith('const N = [{"id": "meta", "name": "Meta"')
isEN = lambda x: x.startswith('const EN={"zuckerberg": "Mark Zuckerberg"')
a[find(a, isN, 'N')] = b[find(b, isN, 'N')]
a[find(a, isEN, 'EN')] = b[find(b, isEN, 'EN')]
for pre in ('const WIKI={', 'const LINKS=', 'const X={', 'const CAREER='):
    ia_ = find(a, isN, 'N')
    ib_ = find(b, isN, 'N')
    ka = next(k for k in range(ia_, ia_ + 12) if a[k].startswith(pre))
    kb = next(k for k in range(ib_, ib_ + 12) if b[k].startswith(pre))
    a[ka] = b[kb]
anch = lambda x: x.startswith("E.push({a:'meta',b:'scale',k:'invest2'")
NEWE = ("a:'levine'", "b:'carelesspeople'", "a:'wynn'", "b:'instagram'", "b:'whatsapp'", "b:'oculus'", "b:'signal'", "b:'anduril'", "a:'systrom',b:'zuckerberg'", "a:'koum',b:'meta'", "a:'luckey',b:'meta'", "a:'olivan',b:'sandberg'")
mine_pat = lambda x: x.startswith('E.push(') and any(t in x for t in NEWE)


def near(lines, n0):
    return min(i for i, x in enumerate(lines) if anch(x) and i > n0)


ib = near(b, find(b, isN, 'N'))
mine_e = [x for x in b[ib - 25:ib] if mine_pat(x)]
assert 14 <= len(mine_e) <= 26, len(mine_e)
ia = near(a, find(a, isN, 'N'))
for k in range(ia - 1, ia - 30, -1):
    if mine_pat(a[k]):
        del a[k]
        ia -= 1
ia = near(a, find(a, isN, 'N'))
a[ia:ia] = mine_e


# 2. 各社のデータ(DATA)
def block_range(lines, key):
    s = find(lines, lambda x: x == key + ':()=>{', key)
    e = s
    while not lines[e].startswith('return {N,PH,WIKI,EN,X,WEB,CAREER,LINKS,E,center:"'):
        e += 1
    e += 1
    assert lines[e].strip() in ('}', '},'), lines[e]
    return s, e + 1


# 公開版にある、Wikidata由来の古い図(今回の選び直しで外れたもの)を取り除く
_live_stw = [m.group(1) for x in a for m in [re.match(r'^(stw_[QY][A-Za-z0-9]+):\(\)=>\{$', x)] if m]
for key in _live_stw:
    if True:
        s_, e_ = block_range(a, key)
        del a[s_:e_]
for key in KEYS:
    s, e = block_range(b, key)
    block = list(b[s:e])
    if not block[-1].endswith(','):
        block[-1] += ','
    if any(x == key + ':()=>{' for x in a):
        s2, e2 = block_range(a, key)
        a[s2:e2] = block
    else:
        ip = find(a, lambda x: x == 'us_AAPL:()=>{', 'anchor')
        a[ip:ip] = block
# 2b. OpenAI・Anthropicの図の追加分(LEGACY)
isL = lambda x: x.startswith('const LEGACY=')
a[find(a, isL, 'L')] = b[find(b, isL, 'L')]
# 2c. Google DeepMind・Microsoft・Nvidiaの、主要人物の説明と経歴(公開版の他の追加分を残すため、該当する人物だけを差し替える)
import json as _json, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from adds_deep import DEEP


def _jline(lines, s, e, prefix):
    k = next(i for i in range(s, e) if lines[i].startswith(prefix))
    return k, _json.loads(lines[k][len(prefix):].rstrip().rstrip(';'))


for key in [k for k in DEEP if k != 'xai']:
    ids = list(DEEP[k]['patch']) if False else list(DEEP[key]['patch'])
    sa, ea = block_range(a, key)
    sb, eb = block_range(b, key)
    ka, na = _jline(a, sa, ea, 'const N = ')
    kb, nb = _jline(b, sb, eb, 'const N = ')
    mine = {n['id']: n for n in nb}
    for n in na:
        if n['id'] in ids and n['id'] in mine:
            n['desc'] = mine[n['id']]['desc']
    a[ka] = 'const N = ' + _json.dumps(na, ensure_ascii=False) + ';'
    kca, ca = _jline(a, sa, ea, 'const CAREER=')
    kcb, cb = _jline(b, sb, eb, 'const CAREER=')
    for i_ in ids:
        if i_ in cb:
            ca[i_] = cb[i_]
    a[kca] = 'const CAREER=' + _json.dumps(ca, ensure_ascii=False) + ';'
# 3. 人物の相関図(PERSONAL)
isP = lambda x: x.startswith('const PERSONAL=')
a[find(a, isP, 'P')] = b[find(b, isP, 'P')]
# 4. 会社の一覧(COMPANIES)と別名(ALIAS)
out = '\n'.join(a)
for key in [k for k in KEYS if not k.startswith('stw_')]:
    ent = [x for x in b if x.startswith('  %s:{name:' % key)]
    assert len(ent) == 1, key
    ls = out.split('\n')
    ex = [i for i, x in enumerate(ls) if x.startswith('  %s:{name:' % key)]
    if ex:
        ls[ex[0]] = ent[0]
        out = '\n'.join(ls)
    else:
        assert out.count("  melcoin:{name:'メルコイン'") == 1
        out = out.replace("  melcoin:{name:'メルコイン'", ent[0] + "\n  melcoin:{name:'メルコイン'", 1)
alias_b = [x for x in b if x.startswith('const ALIAS={')]
assert len(alias_b) == 1
ps = out.find("const ALIAS={")
assert ps >= 0
# 公開版のALIAS行を、こちらの行で、先頭のキーだけ足す(他のセッションが足した別名は残す)
ls = out.split('\n')
ii = find(ls, lambda x: x.startswith('const ALIAS={'), 'alias')
ADD = "adept:'adept',carelesspeople:'carelesspeople',periodic:'periodic',mirendil:'mirendil',humans:'humans',covariant:'covariant',appliedcompute:'appliedcompute',artifact:'artifact',whatsapp:'whatsapp',signal:'signal',oculus:'oculus',ami:'amilabs',amilabs:'amilabs',eureka:'eureka',instagram:'instagram',"
if not ls[ii].startswith('const ALIAS={' + ADD):
    for k in ('instagram:\'instagram\',',):
        ls[ii] = ls[ii].replace(k, '', 1)
    ls[ii] = ls[ii].replace('const ALIAS={', 'const ALIAS={' + ADD, 1)
out = '\n'.join(ls)
# 5a. AWN(別ファイルの数)と、図を別ファイルから読み込む仕組み
ls = out.split('\n')
for pre in ('const AWN=', '/*AWLAZY*/'):
    for i_, x in enumerate(ls):
        if x.startswith(pre):
            del ls[i_]
            break
aw_b = [x for x in b if x.startswith('const AWN=')]
lz_b = [x for x in b if x.startswith('/*AWLAZY*/')]
if aw_b and lz_b:
    j_ = find(ls, lambda x: x.startswith('const AIWD='), 'AIWD const')
    ls.insert(j_ + 1, aw_b[0])
    k_ = find(ls, lambda x: x.startswith('/*AIWD*/'), 'AIWD reg')
    ls.insert(k_ + 1, lz_b[0])
out = '\n'.join(ls)
# 5-. OpenAIなどの図の追加分(LEGACY)に、経歴(career)も使う
_k = "  Object.assign(d.EN,L.en||{});"
if _k in out and "Object.assign(d.CAREER,L.career" not in out:
    out = out.replace(_k, _k + "Object.assign(d.CAREER,L.career||{});", 1)
# 5. AIWD(Wikidataから作った図の一覧)と、その登録の1行
ls = out.split('\n')
ib_ = [x for x in b if x.startswith('const AIWD=')]
rb_ = [x for x in b if x.startswith('/*AIWD*/')]
if ib_ and rb_:
    for i_, x in enumerate(ls):
        if x.startswith('const AIWD='):
            del ls[i_]
            break
    j_ = find(ls, lambda x: x.startswith('const STARTUPS='), 'STARTUPS')
    ls.insert(j_ + 1, ib_[0])
    for i_, x in enumerate(ls):
        if x.startswith('/*AIWD*/'):
            del ls[i_]
            break
    k_ = find(ls, lambda x: x.startswith('STARTUPS.forEach(s=>{const i=s.key.slice(3)'), 'STARTUPS.forEach alias')
    ls.insert(k_ + 1, rb_[0])
out = '\n'.join(ls)
# 6. ユニコーン上位の手作りの図(st_…)。公開版にまだない図を足し、同じ会社の自動作成の図(un_…)を外す
a = out.split('\n')
try:
    from newco_uni import n2 as _n2
    _kS, _sa = _jline(a, 0, len(a), 'const STARTUPS=')
    _kSb, _sb = _jline(b, 0, len(b), 'const STARTUPS=')
    _have = {r['key'] for r in _sa}
    _new = [r for r in _sb if r['key'] not in _have and r['key'].startswith('st_') and not r['key'].startswith('stw_')]
    for r in _new:
        sb_, eb_ = block_range(b, r['key'])
        blk = list(b[sb_:eb_])
        if not blk[-1].endswith(','):
            blk[-1] += ','
        ip = find(a, lambda x: x == 'us_AAPL:()=>{', 'anchor')
        a[ip:ip] = blk
    _sa.extend(_new)
    _kS, _ = _jline(a, 0, len(a), 'const STARTUPS=')
    a[_kS] = 'const STARTUPS=' + _json.dumps(_sa, ensure_ascii=False) + ';'
    # 同じ会社の自動作成の図を外す
    _names = {_n2(r['name']) for r in _new}
    _kJ, _jp = _jline(a, 0, len(a), 'const JPCO=')
    _drop = [r['key'] for r in _jp if r['key'].startswith('un_') and _n2(r['name']) in _names]
    _jp = [r for r in _jp if r['key'] not in _drop]
    a[_kJ] = 'const JPCO=' + _json.dumps(_jp, ensure_ascii=False) + ';'
    for k_ in _drop:
        if any(x == k_ + ':()=>{' for x in a):
            s_, e_ = block_range(a, k_)
            del a[s_:e_]
    print('st追加', len(_new), 'un外す', len(_drop))
except StopIteration:
    print('STARTUPS/JPCOの行が見つからず、6は飛ばしました')
out = '\n'.join(a)
open(MINE, 'w', encoding='utf-8').write(out)
print('merged', len(out), 'ALIAS', out.count('const ALIAS={' + ADD))
