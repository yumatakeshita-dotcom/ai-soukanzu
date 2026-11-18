"""お金の流れに足すデータ(出典つき)。出力: money_extra.json (money_apply.py が取り込む)
 ① AIマネーの循環(公開ページの図のデータ。出典は、図のページに載せたリンク)
 ② Y Combinator の出資先(YC公式の企業一覧)。 ※YCの一覧に載っている=YCの出資先(YCは通常、標準契約で出資する)
使い方: python -u money_extra.py"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
S = os.path.dirname(os.path.abspath(__file__))
N = {'nvidia': 'Nvidia', 'softbank': 'ソフトバンク', 'openai': 'OpenAI', 'google': 'Google', 'meta': 'Meta', 'oracle': 'Oracle', 'amazon': 'Amazon', 'coreweave': 'CoreWeave', 'anthropic': 'Anthropic', 'amd': 'AMD', 'msft': 'Microsoft'}
SRC = 'https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/'
F = [
 ['nvidia', 'openai', 'i', '出資 $30B', 30], ['openai', 'oracle', 'p', 'クラウド 約$300B', 300], ['oracle', 'nvidia', 'p', 'GPUを購入', 0],
 ['msft', 'openai', 'i', '出資 約$13B', 13], ['openai', 'msft', 'p', 'Azure $250B', 250], ['msft', 'nvidia', 'p', 'GPUを購入', 0],
 ['softbank', 'openai', 'i', '出資 $30B', 30], ['amazon', 'openai', 'i', '出資 最大$50B', 50], ['openai', 'amazon', 'p', 'AWS $38B', 38],
 ['openai', 'coreweave', 'p', '$22.4B', 22.4], ['nvidia', 'coreweave', 'i', '出資(株主)', 0], ['coreweave', 'nvidia', 'p', 'GPUを購入', 0],
 ['openai', 'amd', 'p', 'GPU 6GW', 0], ['amd', 'openai', 'w', 'AMD株 最大10%', 0],
 ['amazon', 'anthropic', 'i', '出資 累計$33B', 33], ['anthropic', 'amazon', 'p', 'AWS $100B+', 100],
 ['google', 'anthropic', 'i', '出資', 0], ['anthropic', 'google', 'p', 'TPU 約3.5GW', 0],
 ['msft', 'anthropic', 'i', '出資 最大$5B', 5], ['nvidia', 'anthropic', 'i', '出資 最大$10B', 10], ['anthropic', 'msft', 'p', 'Azure $30B', 30],
 ['meta', 'coreweave', 'p', '$35B', 35], ['meta', 'nvidia', 'p', 'GPU 数百万基', 0], ['meta', 'amd', 'p', 'GPU 6GW', 0], ['amd', 'meta', 'w', 'AMD株 最大10%', 0]]
KIND = {'i': '出資', 'p': '支払い', 'w': '株の権利'}
OUT = []
for a, b, k, lab, v in F:
    OUT.append({'src': N[a], 'dst': N[b], 'kind': KIND[k], 'label': lab, 'amount': '', 'year': '2026', 'note': 'AIマネーの循環(2026年11月13日時点。金額は契約の上限や報道ベースを含む)', 'url': 'https://claude.ai/artifact/FzzqJz3KhB1fptjKvFvWZu', 'media': '相関図(出典は図のページ)', 'd': '2026-11-13'})
yc = json.load(open(os.path.join(S, 'yc_startups.json'), encoding='utf-8'))
fnd = json.load(open(os.path.join(S, 'yc_founders.json'), encoding='utf-8'))
slug_by_name = {v.get('name'): k for k, v in fnd.items()}
def yr(batch):
    m = re.match(r'([WSFX])(\d{2})', batch or '')
    return str(2000 + int(m.group(2))) if m else ''
n = 0
for r in yc:
    name, site, ctry, batch, one, sector, status = (r + [''] * 7)[:7]
    if not name:
        continue
    sl = slug_by_name.get(name)
    OUT.append({'src': 'Y Combinator', 'dst': name, 'kind': '出資(YC)', 'label': 'YC ' + (batch or ''), 'amount': '', 'year': yr(batch), 'note': (one or '')[:120], 'url': ('https://www.ycombinator.com/companies/' + sl) if sl else 'https://www.ycombinator.com/companies?query=' + re.sub(r'\s+', '%20', name), 'media': 'Y Combinator', 'd': ''})
    n += 1
json.dump(OUT, open(os.path.join(S, 'money_extra.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('AIマネー', len(F), '/ YC', n)
