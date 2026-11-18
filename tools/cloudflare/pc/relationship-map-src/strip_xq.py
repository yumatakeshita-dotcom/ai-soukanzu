"""相関図に足したXの発信リンク(add_x_links.pyが入れた行)を取り除く。使い方: python -I strip_xq.py [ページのファイル]"""
import sys
P = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\yumat\.claude\output\relationship-maps.html'
ls = open(P, encoding='utf-8').read().split('\n')
n = len(ls)
ls = [x for x in ls if not x.startswith('/*XQ*/')]
open(P, 'w', encoding='utf-8').write('\n'.join(ls))
print('取り除いた行', n - len(ls))
