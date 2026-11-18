import re
# ---- newco_data10w.py: 図のデータを、別ファイル(aw/NN.json)に書き出せるようにする ----
p = 'newco_data10w.py'
w = open(p, encoding='utf-8').read()
if 'AWDATA' not in w:
    w = w.replace("AIWD = []", "AWDATA = {}  # {key: {N,E,EN,center}}  別ファイル(aw/NN.json)に書き出す。ページには入れない\nAIWD = []", 1)
    old = "        AIWD.append(_m.STARTUPS.pop())   # タブの一覧からは外す\n"
    new = old + """        _cc = _m.CO10['stw_' + c['q']]
        _E = [{'a': n['id'], 'b': 'co', 'k': 'member'} for n in _cc['N'] if n.get('kind') == 'p'] + [{'a': n['id'], 'b': 'co', 'k': 'invest'} for n in _cc['N'] if n.get('kind') == 'i']
        for e_ in edges:
            _d = {'a': e_[0], 'b': e_[1], 'k': e_[2]}
            if len(e_) > 3 and e_[3]:
                _d['label'] = e_[3]
            _E.append(_d)
        AWDATA['stw_' + c['q']] = {'N': _cc['N'], 'E': _E, 'EN': _cc['EN'], 'center': 'co'}
"""
    assert old in w
    w = w.replace(old, new, 1)
    w += '''

def shard_of(k):
    h = 5381
    for ch in k:
        h = (((h * 33) & 0xFFFFFFFF) ^ ord(ch)) & 0xFFFFFFFF
    return h


def write_shards(outdir, per=40):
    """aw/NN.json に、図のデータを分けて書き出す。振り分けは、ページ側(awShardOf)と同じ計算。"""
    import math
    os.makedirs(outdir, exist_ok=True)
    for f in os.listdir(outdir):
        if f.endswith('.json'):
            os.remove(os.path.join(outdir, f))
    n = max(1, math.ceil(len(AWDATA) / per))
    parts = [dict() for _ in range(n)]
    for k, v in AWDATA.items():
        parts[shard_of(k) % n][k] = v
    total = 0
    for i, d in enumerate(parts):
        if d:
            s = json.dumps(d, ensure_ascii=False, separators=(',', ':'))
            open(os.path.join(outdir, '%d.json' % i), 'w', encoding='utf-8').write(s)
            total += len(s.encode('utf-8'))
    return n, total
'''
    open(p, 'w', encoding='utf-8').write(w)

# ---- build_hub2.py: stw_ はページに入れず、別ファイルへ ----
p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
if "k.startswith('stw_')" not in b:
    old = "    for k, c in CO_ALL.items()]) + '\\n};\\n'"
    assert old in b
    b = b.replace(old, "    for k, c in CO_ALL.items() if not k.startswith('stw_')]) + '\\n};\\n'", 1)
    old = "data += 'const AIWD=%s;' % dump(__import__('newco_data10w').AIWD) + chr(10)"
    assert old in b
    b = b.replace(old, old + "\n_awn, _awb = __import__('newco_data10w').write_shards(O + r'\\aw')\ndata += 'const AWN=%d;' % _awn + chr(10)\nprint('別ファイルに書き出した図', len(__import__('newco_data10w').AWDATA), '社 /', _awn, 'ファイル /', round(_awb / 1e6, 2), 'MB')", 1)
    open(p, 'w', encoding='utf-8').write(b)

# ---- hub_template.html: 読み込みの仕組み ----
p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
if '/*AWLAZY*/' not in t:
    i = t.index('/*AIWD*/')
    j = t.index('\n', i)
    code = ("/*AWLAZY*/const AWKEYS=new Set(AIWD.map(r=>r.key)),AWP={};function awShardOf(k){let h=5381;for(let i=0;i<k.length;i++)h=((h*33)^k.charCodeAt(i))>>>0;return h%AWN}"
            "function awNorm(d){d.PH={};d.WIKI={};d.X={};d.WEB={};d.CAREER={};d.LINKS={};d.N.forEach(n=>{if(JA[n.name])n.name=JA[n.name];const k=d.EN[n.id];if(!k)return;"
            "const w=GL.wiki[k]||(OUT[k]&&OUT[k].wiki);if(w)d.WIKI[n.id]=w;const p=GL.ph[k]||(OUT[k]&&OUT[k].img)||(PHX[k]&&PHX[k].i);if(p)d.PH[n.id]=p;"
            "if(GL.x[k])d.X[n.id]=GL.x[k];else if(XI[k])d.X[n.id]=XI[k].h;if(GL.links[k])d.LINKS[n.id]=GL.links[k]});return d}"
            "function awLoad(k){const s=awShardOf(k);return AWP[s]||(AWP[s]=fetch('aw/'+s+'.json').then(r=>{if(!r.ok)throw new Error('HTTP '+r.status);return r.json()}).then(o=>{Object.keys(o).forEach(kk=>{const raw=o[kk];DATA[kk]=()=>awNorm(JSON.parse(JSON.stringify(raw)))})}).catch(e=>{delete AWP[s];throw e}))}"
            "const _awBuild=build;build=function(key,drill){if(AWKEYS.has(key)&&!DATA[key]){awLoad(key).then(()=>_awBuild(key,drill)).catch(e=>{alert('図を読み込めませんでした: '+e.message)});return}return _awBuild(key,drill)};")
    t = t[:j + 1] + code + '\n' + t[j + 1:]
    open(p, 'w', encoding='utf-8').write(t)

# ---- _merge_insta.py: stw_は入れず、公開版の古いブロックは全部取り除く。AWN・読み込みの行を重ねる ----
p = '_merge_insta.py'
g = open(p, encoding='utf-8').read()
if 'AWLAZY' not in g:
    g = g.replace("KEYS += sorted({m.group(1) for x in b for m in [re.match(r'^(stw_[QY][A-Za-z0-9]+):\\(\\)=>\\{$', x)] if m})\n", "", 1)
    old = "for key in _live_stw:\n    if key not in KEYS:"
    assert old in g
    g = g.replace(old, "for key in _live_stw:\n    if True:", 1)
    old = "# 5. AIWD(Wikidataから作った図の一覧)と、その登録の1行"
    new = '''# 5a. AWN(別ファイルの数)と、図を別ファイルから読み込む仕組み
ls = out.split('\\n')
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
out = '\\n'.join(ls)
''' + old
    assert old in g
    g = g.replace(old, new, 1)
    open(p, 'w', encoding='utf-8').write(g)
print('ok')
