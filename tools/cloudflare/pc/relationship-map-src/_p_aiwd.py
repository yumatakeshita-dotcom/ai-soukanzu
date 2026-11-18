# Wikidataから作る図は、タブ(STARTUPS)に出さず、検索で開ける副の図(COMPANIESのsub:1)にする
p = 'newco_data10w.py'
s = open(p, encoding='utf-8').read()
s = s.replace("def load(st):\n", "AIWD = []   # [{key,name,min,note}]  タブには出さず、検索で開く\n\n\ndef load(st):\n    import newco_data10 as _m\n", 1)
s = s.replace("        st('stw_' + c['q'], c['name'], c['year'], NOTE_W, items, edges, desc)\n",
              "        st('stw_' + c['q'], c['name'], c['year'], NOTE_W, items, edges, desc)\n        AIWD.append(_m.STARTUPS.pop())   # タブの一覧からは外す\n", 1)
open(p, 'w', encoding='utf-8').write(s)

p = 'build_hub2.py'
b = open(p, encoding='utf-8').read()
k = "data += 'const STARTUPS=%s;' % dump(__import__('newco_data8').STARTUPS) + chr(10)"
assert b.count(k) == 1
b = b.replace(k, k + "\ndata += 'const AIWD=%s;' % dump(__import__('newco_data10w').AIWD) + chr(10)", 1)
open(p, 'w', encoding='utf-8').write(b)

p = 'hub_template.html'
t = open(p, encoding='utf-8').read()
k = "STARTUPS.forEach(r=>{COMPANIES[r.key]={name:r.name,min:r.min,note:r.note}});"
assert t.count(k) == 1
t = t.replace(k, k + "\n/*AIWD*/AIWD.forEach(r=>{COMPANIES[r.key]={name:r.name,min:r.min,sub:1,note:r.note};ALIAS[r.key.slice(4)]=r.key});", 1)
open(p, 'w', encoding='utf-8').write(t)
print('ok')
