p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
old = "for key in KEYS:\n    s, e = block_range(b, key)"
assert old in g
new = """# 公開版にある、Wikidata由来の古い図(今回の選び直しで外れたもの)を取り除く
_live_stw = [m.group(1) for x in a for m in [re.match(r'^(stw_[QY][A-Za-z0-9]+):\(\)=>\{$', x)] if m]
for key in _live_stw:
    if key not in KEYS:
        s_, e_ = block_range(a, key)
        del a[s_:e_]
""" + old
g = g.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(g)
import ast; ast.parse(g); print('ok')
