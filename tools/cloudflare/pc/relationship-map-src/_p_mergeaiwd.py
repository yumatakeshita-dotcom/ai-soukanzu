import re
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
a = "def find(lines, pred, what):"
add = "KEYS += sorted({m.group(1) for x in b for m in [re.match(r'^(stw_Q\d+):\(\)=>\{$', x)] if m})\n\n\n"
assert 'stw_Q' not in g
g = g.replace("import shutil, sys\n", "import re, shutil, sys\n", 1)
g = g.replace(a, add + a, 1)
# COMPANIESの一覧: stw_はAIWD配列から作られるので、個別の行は要らない
g = g.replace("for key in KEYS:\n    ent = [x for x in b if x.startswith('  %s:{name:' % key)]", "for key in [k for k in KEYS if not k.startswith('stw_')]:\n    ent = [x for x in b if x.startswith('  %s:{name:' % key)]", 1)
tail = "open(MINE, 'w', encoding='utf-8').write(out)"
extra = '''# 5. AIWD(Wikidataから作った図の一覧)と、その登録の1行
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
    k_ = find(ls, lambda x: x.startswith('STARTUPS.forEach(r=>{COMPANIES[r.key]='), 'STARTUPS.forEach')
    ls.insert(k_ + 1, rb_[0])
out = '\n'.join(ls)
'''
g = g.replace(tail, extra + tail, 1)
open(p, 'w', encoding='utf-8').write(g)
print('ok')
