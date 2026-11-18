"""move_lab.html を、公開ページ(relationship-maps.html)の MOVELAB に埋め込む。使い方: python embed_move_lab.py <公開ページのファイル>"""
import json, re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8', newline='').read()
lab = open(__file__.replace('embed_move_lab.py', 'move_lab.html'), encoding='utf-8').read()
lab = re.sub(r'\s*<div class="back">.*?</div>', '', lab, count=1, flags=re.S)
tail = '</script>\n\n</body></html>'
assert tail in lab
lab = lab.replace(tail, '''
function _h(){try{parent.postMessage({moneyH:document.documentElement.scrollHeight},'*')}catch(e){}}
addEventListener('load',_h);addEventListener('resize',_h);new MutationObserver(_h).observe(document.body,{childList:true,subtree:true});setTimeout(_h,400);
</script>

</body></html>''')
lit = json.dumps(lab, ensure_ascii=False).replace('</', '<\/')
nl = '\r\n' if '\r\n' in s else '\n'
a = s.index('const MOVELAB=')
b = s.index(';' + nl + 'function showMove(){', a)
s = s[:a] + 'const MOVELAB=' + lit + s[b:]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok', len(s))
