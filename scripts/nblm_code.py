# NotebookLM用の書き出し(コード一式): 大きなデータを省略したコードを、ファイルごとの見出し付きMarkdownにする。2026/11/19追加
# 使い方: python3 scripts/nblm_code.py 出力先フォルダ  (先に npm install。秘密の鍵・メール・PCのユーザー名・IDは伏せる。読むだけでサイトは変えない)
# 共有フォルダ notebooklm-code/ のファイル名は、出力の「0N_A_」を「0N_コード_」に変えたもの
import ast, os, re, subprocess, sys, json, datetime
SP=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(SP); OUT=sys.argv[1]
os.makedirs(OUT, exist_ok=True)
LIMIT=700_000
def sh(*a): return subprocess.run(a,capture_output=True,text=True).stdout
def strip_js(path_or_text, is_text=False):
    p=path_or_text
    if is_text:
        p='/tmp/_nblm_tmp.js'; open(p,'w').write(path_or_text)
    r=subprocess.run(['node',os.path.join(SP,'nblm_strip.js'),p],capture_output=True,text=True)
    return r.stdout if r.returncode==0 else None
def strip_py(src):
    try: t=ast.parse(src)
    except Exception: return src
    lines=src.splitlines(keepends=True); offs=[0]
    for l in lines: offs.append(offs[-1]+len(l))
    reps=[]
    def walk(n):
        if isinstance(n,(ast.List,ast.Dict,ast.Tuple,ast.Set,ast.Constant)) and hasattr(n,'end_lineno'):
            s=offs[n.lineno-1]+n.col_offset; e=offs[n.end_lineno-1]+n.end_col_offset
            if e-s>300 and (not isinstance(n,ast.Constant) or isinstance(n.value,str)):
                # docstringや説明の文字列は残す(1500字まで)
                if isinstance(n,ast.Constant) and e-s<1500: return
                cnt=len(n.elts) if hasattr(n,'elts') else len(n.keys) if isinstance(n,ast.Dict) else 0
                head=src[s:s+80].replace('\n',' ')
                reps.append((s,e,f"None  # データ省略: {cnt}件・{e-s}文字。先頭: {head}…")); return
        for c in ast.iter_child_nodes(n): walk(c)
    walk(t)
    for s,e,r in sorted(reps,reverse=True): src=src[:s]+r+src[e:]
    return src
def clean(t):
    t=re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', lambda m: m.group(0) if m.group(0).endswith(('.png','.jpg','.js','.json')) else '<メール省略>', t)
    t=t.replace('C:\\Users\\yumat','C:\\Users\\<ユーザー>').replace('C:/Users/yumat','C:/Users/<ユーザー>').replace('C:\\\\Users\\\\yumat','C:\\\\Users\\\\<ユーザー>')
    t=re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}','<ID省略>',t)
    return t
LANG={'.py':'python','.js':'javascript','.mjs':'javascript','.html':'html','.css':'css','.md':'markdown','.json':'json','.toml':'toml','.sh':'bash','.bat':'bat','.txt':'text'}
def block(rel, text, note=''):
    ext=os.path.splitext(rel)[1]; fence='````' if '```' in text else '```'
    return f"\n\n## ファイル: `{rel}`\n" + (f"\n> {note}\n" if note else '') + f"\n{fence}{LANG.get(ext,'text')}\n{text.rstrip()}\n{fence}\n"
def read(rel): return open(os.path.join(R,rel),encoding='utf-8',errors='replace').read()

parts={}  # name -> list of (rel, md)
def add(part, rel, text, note=''): parts.setdefault(part,[]).append((rel, block(rel, clean(text), note)))

# A. 説明書(CLAUDE.md・docs など)
for rel in ['CLAUDE.md','README.md']+sorted('docs/'+f for f in os.listdir(R+'/docs') if f.endswith('.md'))+['docs/photo_rights/README.md','newsletter/README.md','tools/cloudflare/README.md','tools/cloudflare/AUTOMATION.md','tools/cloudflare/pc/D1_SCHEMA.md','tools/cloudflare/pc/LARGE_FILES.txt','tools/cloudflare/pc/relationship-map-site/README.md','inbox/x_accounts.txt','package.json']:
    if os.path.exists(os.path.join(R,rel)): add('A_説明書と設定', rel, read(rel))
# B. 本体の相関図 site/index.html
html=read('site/index.html'); i=html.index('<script>\n',html.index('data/exectl.js')); j=html.rindex('</script>')
head_part=html[:i]; js=html[i+len('<script>\n'):j]; tail=html[j:]
sjs=strip_js(js,True)
add('B_本体の相関図', 'site/index.html (前半: 画面の部品と見た目)', head_part, '本体の相関図のHTMLとCSS。scriptの読み込み順もここでわかる。')
note='本体の相関図のプログラム。大きなデータ(会社・人・線の一覧)は「データ省略」と書いて中身を抜いた。会社ごとに同じ形で並ぶ図の作り方は、形ごとに1つだけ残した(省略した会社名はコメントにある)。'
add('B_本体の相関図', 'site/index.html (後半: プログラム)', sjs+'\n'+tail, note)
# C. site/data のプログラム部分・実験ページ・週のまとめ
for f in sorted(os.listdir(R+'/site/data')):
    s=strip_js(R+'/site/data/'+f)
    if s is None: continue
    add('C_データ読み込みと実験ページ', 'site/data/'+f, s, 'データの中身は省略。形(どんな項目を持つか)とプログラムだけを残した。')
for f in sorted(os.listdir(R+'/src/lab')):
    if f.endswith('.json'):
        s=strip_js('('+read('src/lab/'+f)+')',True); add('C_データ読み込みと実験ページ','src/lab/'+f,(s or '')[1:-1] if s else '(省略)','JSONのデータは省略。形だけ。'); continue
    t=read('src/lab/'+f)
    if f.endswith('.html'):
        t=re.sub(r'(<script>)(.*?)(</script>)', lambda m: m.group(1)+(strip_js(m.group(2),True) or m.group(2))+m.group(3), t, flags=re.S)
    add('C_データ読み込みと実験ページ','src/lab/'+f,t)
add('C_データ読み込みと実験ページ','site/lab/index.html',read('site/lab/index.html'))
# D. 道具(scripts と tools)
def tool_files():
    for base in ['scripts','tools']:
        for d,_,fs in os.walk(R+'/'+base):
            if '__pycache__' in d or 'node_modules' in d: continue
            for f in sorted(fs):
                rel=os.path.relpath(os.path.join(d,f),R)
                if f.endswith(('.sql','.pyc','package-lock.json')) or f=='gnews_map.json': continue
                if rel.endswith(('.md',)) or rel in [x for x,_ in parts.get('A_説明書と設定',[])]: continue
                yield rel
for rel in sorted(tool_files()):
    t=read(rel); ext=os.path.splitext(rel)[1]
    if ext=='.py': t=strip_py(t)
    elif ext in ('.js','.mjs'): t=strip_js(os.path.join(R,rel)) or t
    elif ext=='.json' and len(t)>2000: t=(strip_js('('+t+')',True) or '(省略)')
    part='D_道具_毎日の更新と確認' if rel.startswith('scripts') or rel.startswith('tools/cloudflare/relmap') or rel.count('/')<=2 else 'E_道具_PC側の作業用(古いものを含む)'
    if len(t)>60000: t=t[:60000]+'\n…(長いので以下省略)'
    add(part, rel, t)

# 書き出し(上限を超えたら分ける)
today=datetime.date.today().isoformat(); commit=sh('git','-C',R,'log','-1','--format=%h %ad','--date=short').strip()
written=[]
for pi,(name,items) in enumerate(sorted(parts.items())):
    chunks=[[]]; size=0
    for rel,md in items:
        b=len(md.encode())
        if size+b>LIMIT and chunks[-1]: chunks.append([]); size=0
        chunks[-1].append((rel,md)); size+=b
    for ci,ch in enumerate(chunks):
        fn=f"{pi+1:02d}_{name}"+(f"_その{ci+1}" if len(chunks)>1 else '')+'.md'
        hdr=f"# AI企業の相関図のコード: {name.split('_',1)[1]}"+(f"(その{ci+1})" if len(chunks)>1 else '')+f"\n\n{today}時点(リポジトリ yumatakeshita-dotcom/ai-soukanzu の main、{commit})。秘密の鍵・トークン・メールアドレスは含めていない。大きなデータの中身は省略している(データそのものは別の書き出し「notebooklm/」の30ファイルにある)。\n\n### このファイルに入っているもの\n"+''.join(f"- `{r}`\n" for r,_ in ch)
        open(os.path.join(OUT,fn),'w',encoding='utf-8').write(hdr+''.join(m for _,m in ch))
        written.append((fn,os.path.getsize(os.path.join(OUT,fn)),[r for r,_ in ch]))
for w in written: print(w[0],w[1],len(w[2]))
