# -*- coding: utf-8 -*-
"""毎朝の移籍の調査(inbox/moves/*.json)から、幹部の動きを「幹部の年表」に自動で足す。

- 書き出し先: site/data/finds.js の3行目(const EXECTL_AUTO={openai:[...],anthropic:[...]})。
  finds.js は毎朝9:13の定期タスクが commit して共有リンクに公開するので、別のファイルにしない
  (merge_inbox.py が finds.js を書くときに js_line() を3行目に入れる。このファイルを単独で動かしたときは3行目だけを書き換える)
- 手で書いた年表(site/data/exectl.js)は読むだけ。書き換えない
- 手で書いた年表にもう同じ人・同じ種類(入社/退社)があるもの、同じ人の前後1か月の行があるものは足さない(手の方を優先)
- 出典(src)の無いもの、confidence が「うわさ」のものは足さない
- 幹部らしい役職(CEO・VP・責任者・取締役など)のものだけ足す。研究者・技術スタッフだけのものは足さない
- inbox/ は足すだけなので、毎回作り直しても前に足したものは消えない
使い方: python3 scripts/exectl_auto.py   (自動で足した件数を表示する)
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site', 'data', 'finds.js')
MANUAL = os.path.join(ROOT, 'site', 'data', 'exectl.js')
# 年表の会社: キー -> 名前(inbox の from/to にこの名前が入っていれば対象)
COMPANIES = {'openai': 'OpenAI', 'anthropic': 'Anthropic', 'nvidia': 'Nvidia'}  # 2026/11/19 Nvidiaを追加
EXEC = re.compile(r'CEO|CTO|CFO|COO|CRO|CPO|CMO|CCO|CIO|CSO|Chief|最高|責任者|VP|副社長|社長|会長|取締役|役員|幹部|'
                  r'[Hh]ead|Director|ディレクター|部門長|統括|共同創業|創業者|顧問|General Manager|代表|Managing|President|'
                  r'リーダー|リード')
CF = {'公式': 'o', '開示': 'f', '本人の発言': 's', '本人': 's', '報道': 'r', '推定': 'e'}


def norm(x):
    return re.sub(r'[\s　・,、.()()]+', '', str(x or '')).lower()


def manual_keys():
    """手で書いた年表の (会社, 英語名, 種類)。英語名が「A / B」のときは両方"""
    keys = set()
    if not os.path.exists(MANUAL):
        return keys
    s = open(MANUAL, encoding='utf-8').read()
    cur = None
    for line in s.splitlines():
        m = re.match(r'^(\w+):\{\s*$', line)
        if m and m.group(1) in COMPANIES:
            cur = m.group(1)
        m = re.search(r"\{d:'([^']*)',t:'(\w+)',p:'[^']*',en:'([^']*)'", line)
        if cur and m:
            for en in m.group(3).split('/'):
                if en.strip():
                    keys.add((cur, norm(en), m.group(2)))
                    keys.add((cur, norm(en), 'd' + m.group(1)[:7]))
    return keys


def has(name, text):
    return name.lower() in str(text or '').lower()


def build():
    keys = manual_keys()
    out = {k: [] for k in COMPANIES}
    seen = set()
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', 'moves', '*.json'))):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for it in d.get('items', []) if isinstance(d, dict) else []:
            src = [s for s in (it.get('src') or []) if isinstance(s, list) and len(s) >= 2 and str(s[1]).startswith('http')]
            if not src or it.get('confidence') == 'うわさ':
                continue
            en = it.get('name_en') or ''
            ja = it.get('name_ja') or en
            if not en and not ja:
                continue
            fr, to, role = it.get('from') or '', it.get('to') or '', it.get('role') or ''
            for key, name in COMPANIES.items():
                hf, ht = has(name, fr), has(name, to)
                if not (hf or ht):
                    continue
                t = 'role' if (hf and ht) else ('in' if ht else 'out')
                # 幹部らしいか: 入社・役割の変更は新しい役職、退社は元の役職(from に書かれる)で見る
                if not EXEC.search(role + ' ' + (fr if t == 'out' else '')):
                    continue
                k = (key, norm(en or ja), t)
                if k in keys or k in seen:
                    continue
                # 手で書いた年表に、同じ人の前後1か月の行があれば足さない(入社・退社の書き分けが違っても同じ出来事とみなす)
                dd = it.get('date') or d.get('date') or ''
                if re.match(r'^\d{4}-\d{2}', dd):
                    y, mo = int(dd[:4]), int(dd[5:7])
                    near = [f'{y + (mo + x - 1) // 12:04d}-{(mo + x - 1) % 12 + 1:02d}' for x in (-1, 0, 1)]
                    if any((key, norm(en or ja), 'd' + n) in keys for n in near):
                        continue
                seen.add(k)
                e = {'d': it.get('date') or d.get('date') or '', 't': t, 'p': ja, 'en': en if en != ja else '',
                     'role': role if t != 'out' else (re.sub(r'^.*?[((]', '', fr).rstrip('))') if '(' in fr or '(' in fr else role),
                     'note': it.get('note') or '', 'cf': CF.get(it.get('confidence') or '報道', 'r'), 'src': src[:3],
                     'auto': os.path.basename(f)}
                if t == 'in':
                    e['from'] = fr
                elif t == 'out':
                    e['to'] = to
                if not re.match(r'^\d{4}-\d{2}', e['d']):
                    continue
                out[key].append(e)
    for k in out:
        out[k].sort(key=lambda e: (e['d'], e['en'] or e['p']))
    return out


def js_line(out=None):
    """finds.js の3行目。手で直さない"""
    out = build() if out is None else out
    return ('const EXECTL_AUTO=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) +
            ';// 幹部の年表に自動で足したもの(scripts/exectl_auto.py が inbox/moves/ から毎回作る。手で直さない)\n')


def report(out):
    n = sum(len(v) for v in out.values())
    print('幹部の年表(自動): ' + '、'.join(f'{COMPANIES[k]} {len(v)}件' for k, v in out.items()) + f'(合計{n}件)')
    return n


def main():
    """単独で動かしたとき: finds.js の EXECTL_AUTO の行だけを書き換える(ほかの行はそのまま)"""
    out = build()
    lines = open(OUT, encoding='utf-8').read().splitlines(True)
    keep = [l for l in lines if not l.startswith('const EXECTL_AUTO=')]
    if keep and not keep[-1].endswith('\n'):
        keep[-1] += '\n'
    open(OUT, 'w', encoding='utf-8').write(''.join(keep) + js_line(out))
    return report(out)


if __name__ == '__main__':
    main()
