"""祐真さんがXでいいね・保存した投稿のアカウントを、相関図の「いいね・保存した人」の印に足す(足すだけ)。

使い方:
  python scripts/x_liked_add.py handle:種類:日付 [handle:種類:日付 ...]
    種類 = b(保存) / l(いいね) / bl(両方)。日付 = その人の投稿をいいね・保存した中で一番新しい投稿の日付(YYYY-MM-DD)
  例: python scripts/x_liked_add.py trq212:l:2026-11-25 tmiyatake1:bl:2026-11-26

site/index.html の /*XLIKED_START*/ 〜 /*XLIKED_END*/ の間にある XLIKED に足す。
すでにある人は書き換えない(日付・種類もそのまま)。印は相関図の人物カードの「X @名前」の横に出る。
"""
import json, re, sys, pathlib

P = pathlib.Path(__file__).resolve().parent.parent / 'site' / 'index.html'
KIND = {'b': '保存', 'l': 'いいね', 'bl': 'いいね・保存', 'lb': 'いいね・保存'}


def main(args):
    if not args or args[0] in ('-h', '--help'):
        print(__doc__); return
    t = P.read_text(encoding='utf-8')
    m = re.search(r'/\*XLIKED_START\*/\s*const XLIKED=(\{.*?\});\s*/\*XLIKED_END\*/', t, re.S)
    if not m:
        sys.exit('XLIKED の印が index.html に見つからない')
    d = json.loads(m.group(1))
    added = []
    for a in args:
        parts = a.split(':')
        if len(parts) != 3 or parts[1] not in KIND or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', parts[2]):
            print('形式が違うので飛ばす:', a); continue
        h = parts[0].lstrip('@').lower()
        if not re.fullmatch(r'[a-z0-9_]{1,15}', h):
            print('アカウント名が違うので飛ばす:', a); continue
        if h in d:
            continue
        d[h] = {'k': KIND[parts[1]], 'd': parts[2]}
        added.append(h)
    if not added:
        print('足すものはなかった'); return
    new = '/*XLIKED_START*/ const XLIKED=' + json.dumps(d, ensure_ascii=False, sort_keys=True) + '; /*XLIKED_END*/'
    t = t[:m.start()] + new + t[m.end():]
    P.write_text(t, encoding='utf-8')
    print('足した:', ' '.join(added))


if __name__ == '__main__':
    main(sys.argv[1:])
