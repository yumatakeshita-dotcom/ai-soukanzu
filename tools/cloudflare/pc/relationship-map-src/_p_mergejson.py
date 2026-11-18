import ast
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
if 'adds_deep' not in g:
    old = "# 3. 人物の相関図(PERSONAL)"
    new = """# 2c. Google DeepMind・Microsoft・Nvidiaの、主要人物の説明と経歴(公開版の他の追加分を残すため、該当する人物だけを差し替える)
import json as _json, os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from adds_deep import DEEP


def _jline(lines, s, e, prefix):
    k = next(i for i in range(s, e) if lines[i].startswith(prefix))
    return k, _json.loads(lines[k][len(prefix):].rstrip().rstrip(';'))


for key in ('gdm', 'msft', 'nvidia'):
    ids = list(DEEP[key]['patch'])
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
""" + old
    assert old in g
    g = g.replace(old, new, 1)
    ast.parse(g)
    open(p, 'w', encoding='utf-8').write(g)
print('ok')
