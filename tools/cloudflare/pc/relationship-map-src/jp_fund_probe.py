import urllib.request,re,sys,html,json
sys.stdout.reconfigure(encoding='utf-8')
UA={'User-Agent':'Mozilla/5.0 (personal use; internal relationship map)'}
def g(u):
    try: return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30).read().decode('utf-8','replace')
    except Exception as e: return ''
h=g('https://prtimes.jp/main/action.php?run=html&page=searchkey&search_word=%E8%B3%87%E9%87%91%E8%AA%BF%E9%81%94&search_pattern=1')
links=list(dict.fromkeys(re.findall(r'href="(/main/html/rd/p/[0-9.]+\.html)"',h)))
n=0
for l in links[:14]:
    p=g('https://prtimes.jp'+l)
    m=re.search(r'<title>([^<]*)',p); title=html.unescape(m.group(1)) if m else ''
    txt=re.sub(r'<script.*?</script>|<style.*?</style>','',p,flags=re.S); txt=re.sub(r'<br\s*/?>|</p>|</li>|</tr>|</div>|</h\d>','\n',txt); txt=html.unescape(re.sub(r'<[^>]+>','',txt))
    hits=[x.strip()[:140] for x in txt.split('\n') if re.search(r'引受先|投資家|出資者|リード|VC|ベンチャーキャピタル|キャピタル',x) and len(x.strip())<160][:4]
    print('##',title[:70],l); [print('   ',x) for x in hits]
