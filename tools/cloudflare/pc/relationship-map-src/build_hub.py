import re
S = r'C:\Users\yumat\.claude\docs\rooms\relationship-map-src'
O = r'C:\Users\yumat\.claude\output'

def block(path):
    h = open(path, encoding='utf-8').read()
    a = h.index('const N = [')
    b = h.index('const byId')
    d = h[a:b]
    d = '\n'.join(l for l in d.split('\n') if not l.startswith('const li=') and not l.startswith('const xs='))
    return d

def fn(name, center, body):
    return ('%s:()=>{\n%s\nreturn {N,PH,WIKI,EN,X,WEB,CAREER,LINKS,E,center:"%s"};\n}' % (name, body, center))

data = 'const DATA={\n' + fn('openai', 'openai', block(O + r'\openai-relationship-map.html')) + ',\n' \
     + fn('anthropic', 'anthropic', block(O + r'\anthropic-relationship-map.html')) + '\n};\n'
t = open(S + r'\hub_template.html', encoding='utf-8').read()
assert '/*DATA*/' in t
open(O + r'\relationship-maps.html', 'w', encoding='utf-8').write(t.replace('/*DATA*/', data))
print(len(data))
