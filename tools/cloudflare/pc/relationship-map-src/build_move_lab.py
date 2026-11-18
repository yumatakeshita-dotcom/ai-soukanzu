"""AI人材の移籍マップ(相関図ラボ④)を作り直す。
 材料: move_lab_template.html(元のページ・最初の71件入り)、moves_auto.json(build_moves.py が相関図から拾った移籍)、moves_extra.json(手で足す、出典つきの移籍 [{p,en,a,b,y,src}])
 出力: move_lab.html(単体で動く)。円は、移籍の多い上位 TOP 社だけ。一覧には、すべての移籍を出す。
使い方: python build_move_lab.py"""
import json, os, re, sys, datetime as dt
S = os.path.dirname(os.path.abspath(__file__))
TOP = 34
tpl = open(os.path.join(S, 'move_lab_template.html'), encoding='utf-8').read()
FL = json.loads(re.search(r'const FL=(\[.*?\]);\n', tpl, re.S).group(1))
for f in FL:
    f.setdefault('src', '相関図(出身・移籍先)')
auto = json.load(open(os.path.join(S, 'moves_auto.json'), encoding='utf-8'))
extra = json.load(open(os.path.join(S, 'moves_extra.json'), encoding='utf-8')) if os.path.exists(os.path.join(S, 'moves_extra.json')) else []
BAD_ORG = re.compile(r'大学|University|^MIT$|^UC|カレッジ|Ministry|省$|Careless|^松尾|^榛葉|^ティム|^ルー・')
SKIP_SRC = re.compile(r'^(us_|st_|jpx_|vc_|aq_|su_)')
def ok(m):
    return not SKIP_SRC.match(m.get('src', '')) and not BAD_ORG.search(m['a']) and not BAD_ORG.search(m['b'])
seen = {(f['p'], f['a'], f['b']) for f in FL}
seenpb = {(f['p'], f['b']) for f in FL}
added = 0
for m in auto:
    if not ok(m):
        continue
    k = (m['p'], m['a'], m['b'])
    if k in seen or (m['p'], m['b']) in seenpb:
        continue
    FL.append({'p': m['p'], 'en': m.get('en') or '', 'a': m['a'], 'b': m['b'], 'y': m['y'], 'src': '相関図(出身・移籍先)'})
    seen.add(k); seenpb.add((m['p'], m['b'])); added += 1
for m in extra:
    k = (m['p'], m['a'], m['b'])
    if k in seen:
        continue
    FL.append({'p': m['p'], 'en': m.get('en', ''), 'a': m['a'], 'b': m['b'], 'y': m.get('y') or 2026, 'src': m.get('src', ''), 'url': m.get('url', '')})
    seen.add(k); added += 1
ys = [f['y'] for f in FL if f.get('y')]
ymin, ymax = min(ys), max(ys)
html = tpl
html = re.sub(r'const FL=\[.*?\];\n', lambda _: 'const FL=' + json.dumps(FL, ensure_ascii=False, separators=(',', ':')) + ';\n', html, count=1, flags=re.S)
# 円は上位 TOP 社だけ
html = html.replace("const SORTED=Object.keys(tot).sort((a,b)=>tot[b]-tot[a]);\nconst ORGS=[];for(let i=0;i<Math.ceil(SORTED.length/2);i++){ORGS.push(SORTED[i]);const j=SORTED.length-1-i;if(j>i)ORGS.push(SORTED[j])}",
 "const SORTED=Object.keys(tot).sort((a,b)=>tot[b]-tot[a]).slice(0,%d);\nconst ORGS=[];for(let i=0;i<Math.ceil(SORTED.length/2);i++){ORGS.push(SORTED[i]);const j=SORTED.length-1-i;if(j>i)ORGS.push(SORTED[j])}" % TOP)
html = html.replace("const pairs={};FL.forEach(f=>{const k=f.a+'>'+f.b;(pairs[k]=pairs[k]||[]).push(f)});", "const pairs={};FL.forEach(f=>{if(!P[f.a]||!P[f.b])return;const k=f.a+'>'+f.b;(pairs[k]=pairs[k]||[]).push(f)});")
html = html.replace("const RANK=o=>SORTED.indexOf(o);", "const RANK=o=>SORTED.indexOf(o);\nconst RANKALL=o=>RANK(o);")
old = "<b style=\"color:${colOf(f.a)}\">${esc(f.a)}</b> → <b>${esc(f.b)}</b></span></span></li>`"
assert old in html
html = html.replace(old, "<b style=\"color:${colOf(f.a)}\">${esc(f.a)}</b> → <b>${esc(f.b)}</b>${f.url?` <a href=\"${esc(f.url)}\" target=\"_blank\" rel=\"noopener\" style=\"font-size:11.5px\">出典 ↗</a>`:''}</span></span></li>`")
html = html.replace('min="2015" max="2026" value="2026"', 'min="%d" max="%d" value="%d"' % (ymin, ymax, ymax))
html = html.replace("let year=2026,", "let year=%d,"%ymax)
html = html.replace("year=2015;$('y').value=year;draw()", "year=%d;$('y').value=year;draw()"%ymin)
html = html.replace("if(year>=2026){clearInterval", "if(year>=%d){clearInterval"%ymax)
html = html.replace('<span class="yr" id="yl">2026</span>', '<span class="yr" id="yl">%d</span>'%ymax)
import rank_patch
html = rank_patch.apply(html)
today = dt.date.today().strftime('%Y年%-m月%-d日') if os.name != 'nt' else dt.date.today().strftime('%Y年%m月%d日').replace('年0', '年').replace('月0', '月')
html = re.sub(r'<div>データ: .*?</div>', '<div>データ: 本体の「AI企業の相関図」に記録した「出身」「移籍先」のつながりを機械的に拾い、%d件にしました(%s時点)。相関図に載っている人だけなので、実際の移籍の一部です。年は、移った先に入った年(わかる場合)で、わからない場合は新しい年として扱っています。円には、移籍の多い上位%d社だけを描き、一覧にはすべての移籍を出します。Google BrainはGoogle DeepMindにまとめています。出典は、各人物のページ(本体の相関図)をご覧ください。</div>' % (len(FL), today, TOP), html, count=1, flags=re.S)
html = html.replace('(71件、2026年11月13日時点)', '')
open(os.path.join(S, 'move_lab.html'), 'w', encoding='utf-8').write(html)
print('件数', len(FL), '追加', added, '年', ymin, ymax, '円の会社', min(TOP, len({f['a'] for f in FL} | {f['b'] for f in FL})))
