#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""新しい係が初めて動くとき、過去に inbox/ へ入れた候補から、その係の仕事に当たるものを拾って、その係の出力にも足す(2026/11/21追加)。

使い方:
  python3 scripts/agent_seed.py ID            # 拾って inbox/ に足す(IDは docs/agents.json の id。下の RULES にあるもの)
  python3 scripts/agent_seed.py ID --dry-run  # 件数と中身だけ見る
  python3 scripts/agent_seed.py --all         # RULES の全部

決まり:
  - 足すだけ。元のファイルは触らない。同じ係を2回動かしても、すでに拾ったものは足さない(inbox/agents/seeded_ID.txt に記録)
  - 出典(src)のある項目だけ。拾った項目には seed_agent と seed_from(元のファイル)を付ける
  - 出力は inbox/money か inbox/moves の 日付-seed-ID.json。サイトへは9:13の取り込み係が足す(同じ内容は merge_inbox.py が重複として省く)
  - 自分(seed)が作ったファイルは、次の拾いの元にしない
"""
import argparse, datetime, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JST = datetime.timezone(datetime.timedelta(hours=9))
JP = re.compile(r'[぀-ヿ一-鿿]')  # かな・漢字


def txt(it):
    return ' '.join(str(it.get(k, '')) for k in ('from', 'to', 'role', 'note', 'name_en', 'name_ja', 'quote'))


def jp_side(it):
    return bool(JP.search(str(it.get('from', '')) + str(it.get('to', ''))))


def src_host(it):
    return ' '.join(s[1] for s in it.get('src', []) if len(s) > 1)


def jp_ctx(it):
    """日本の話か: 出典が日本の発表・報道、または日本・株式会社と書いてある"""
    return bool(re.search(r'\.jp|nikkei|itmedia|initial|tdnet|jpx', src_host(it), re.I)) or bool(re.search(r'日本|国内|株式会社|東証|適時開示', txt(it)))


RULES = {
    # id: (読む種類, 出力の種類, 当たる条件)。広く拾いすぎないよう、日本の話であることを必ず確かめる
    'jp_funding': ('money', 'money', lambda it: it.get('kind') == '出資' and jp_ctx(it)),
    'jp_alliance': ('money', 'money', lambda it: jp_ctx(it) and bool(re.search(r'提携|導入|協業|連携', txt(it)))),
    'jp_hr': ('moves', 'moves', lambda it: jp_ctx(it) and bool(re.search(r'役員|取締役|執行役員|CxO|最高.{0,6}責任者|組織変更', txt(it)))),
    'datacenter': ('money', 'money', lambda it: bool(re.search(r'データセンター|電力|\bGW\b|\bMW\b|ギガワット|JASM|data ?cent|gigawatt', txt(it), re.I))),
    'hiring': ('moves', 'moves', lambda it: bool(re.search(r'採用|CHRO|最高人事責任者|head of people|chief people', txt(it), re.I))),
}


def key(it):
    return re.sub(r'\W+', '', (str(it.get('from') or it.get('name_en') or '') + str(it.get('to', '')) + src_host(it))).lower()


def run(aid, dry):
    read_kind, out_kind, rule = RULES[aid]
    seen_f = os.path.join(ROOT, 'inbox', 'agents', f'seeded_{aid}.txt')
    seen = set(open(seen_f, encoding='utf-8').read().split()) if os.path.exists(seen_f) else set()
    found, newkeys = [], []
    for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', read_kind, '*.json'))):
        if '-seed-' in os.path.basename(f):
            continue
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for it in d.get('items', []):
            if not it.get('src') or not rule(it):
                continue
            k = key(it)
            if not k or k in seen or k in newkeys:
                continue
            newkeys.append(k)
            x = dict(it)
            x['seed_agent'] = aid
            x['seed_from'] = os.path.relpath(f, ROOT)
            found.append(x)
    print(f'{aid}: 当たり {len(found)} 件')
    for x in found[:8]:
        print('  -', (x.get('from') or x.get('name_en')), '→', x.get('to'), '|', x['seed_from'])
    if dry or not found:
        return len(found)
    today = datetime.datetime.now(JST).date().isoformat()
    out = os.path.join(ROOT, 'inbox', out_kind, f'{today}-seed-{aid}.json')
    n = 2
    while os.path.exists(out):
        out = os.path.join(ROOT, 'inbox', out_kind, f'{today}-seed-{aid}-{n}.json')
        n += 1
    json.dump({'date': today, 'kind': out_kind, 'items': found,
               'notes': f'{aid}: 過去の inbox から拾った {len(found)} 件(初回の拾い。元のファイルは変えていない)'},
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.makedirs(os.path.dirname(seen_f), exist_ok=True)
    with open(seen_f, 'a', encoding='utf-8') as fh:
        fh.write('\n'.join(newkeys) + '\n')
    print('  保存:', os.path.relpath(out, ROOT))
    return len(found)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('id', nargs='?')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    ids = list(RULES) if a.all else [a.id]
    for i in ids:
        if i not in RULES:
            raise SystemExit(f'知らない係: {i}(使えるのは {list(RULES)})')
        run(i, a.dry_run)
