p='hub_template.html';h=open(p,encoding='utf-8').read()
fn=open('_wp_fn.js',encoding='utf-8').read()
# 1) insert functions before qGo definition (after qSearch)
a="function qGo(it){"
assert a in h and 'showWPerson' not in h
h=h.replace(a,fn+a,1)
# 2) search: concat wpItems
a=".concat(vcItems(),newsCoItems())"
assert a in h;h=h.replace(a,".concat(vcItems(),newsCoItems(),wpItems())",1)
# 3) labels
a="u:'ユニコーン',n:'ニュース',v:'VC',s:'スタートアップ'}"
assert a in h;h=h.replace(a,"u:'ユニコーン',n:'ニュース',v:'VC',s:'スタートアップ',q:'人物',w:'人物'}",1)
# 4) qGo
a="  if(it.t==='p'){showProfile(it.en);return}"
assert a in h;h=h.replace(a,a+"\n  if(it.t==='w'){showWPerson(it);return}",1)
# 5) buildIndex: people without EN -> t:'q' (人物)
a="      SIDX.push({t:n.kind==='i'?'i':'o',key:k,id:n.id,name:n.name,en,sub:C.name+(n.role?' / '+n.role:''),s:norm(n.name+' '+en+' '+n.id)});"
assert a in h
h=h.replace(a,"      SIDX.push({t:n.kind==='p'?'q':n.kind==='i'?'i':'o',key:k,id:n.id,name:n.name,en,sub:C.name+(n.role?' / '+n.role:''),s:norm(n.name+' '+en+' '+n.id)});",1)
# 6) kick off the people load at startup (after SIDX decl area): call at the end of qEl listeners
a="qEl.addEventListener('input',qSearch);"
assert a in h;h=h.replace(a,"wpLoad();\n"+a,1)
open(p,'w',encoding='utf-8').write(h);print('ok')
