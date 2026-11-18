"""外部AI(ChatGPT・Gemini等)が作った追加データを、相関図に取り込む。Claude不要・トークン0。

置き場所: ext_adds/<会社キー>.json  (名前が _ で始まるファイルは見本なので無視する)
  例: ext_adds/openai.json → 会社キー openai の図に人物・出資者・関連組織を足す

使い方:
  python -I ext_apply.py          … 全ファイルを検査して結果を表示(ビルドはしない)
  build_hub2.py が apply_ext(CO_ALL) を呼ぶので、refresh.py で自動的に入る。
検査で1つでもエラーがあれば、ビルドを止める(壊れたデータを公開しないため)。

ルール(指示書 docs/rooms/relationship-map.md の「守ること」に従う):
- 出典(src)と確度(conf)は必須。確度は「確認済み」「報道」「未確認」のいずれか。
- 子ども・連絡先・確認できない噂は入れない。
- 同じ id が既にある人物は追加しない(警告を出す)。
"""
import json, os, sys

S = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(S, 'ext_adds')
KINDS = {'p', 'i', 'o'}                       # 人物・出資者・関連組織
CONFS = {'確認済み', '報道', '未確認'}
EDGE_K = {'member', 'invest', 'invest2', 'moved', 'from', 'govern', 'owns', 'link', 'conflict', 'deal', 'family', 'friend', 'mentor', 'work', 'rival', 'org'}
LEGACY_KEYS = ('openai', 'anthropic', 'xai', 'meta')  # 手作りの図。adds.py の ADDS・LEGACY_EDGES に足す形で扱う


def _load():
    """(会社キー, ファイル名, 中身) の一覧と、エラー一覧を返す"""
    items, errs = [], []
    if not os.path.isdir(DIR):
        return items, errs
    for fn in sorted(os.listdir(DIR)):
        if not fn.endswith('.json') or fn.startswith('_'):
            continue
        path = os.path.join(DIR, fn)
        try:
            d = json.load(open(path, encoding='utf-8'))
        except Exception as e:
            errs.append(f'{fn}: JSONとして読めません({e})')
            continue
        items.append((fn, d))
    return items, errs


def check(d, fn, known_ids=None):
    """1ファイルを検査し、エラーの文字列リストを返す"""
    e = []
    key = d.get('company')
    if not key or not isinstance(key, str):
        e.append('company(会社キー)がありません')
    ids = set()
    for i, n in enumerate(d.get('nodes', [])):
        tag = f'nodes[{i}]'
        nid = n.get('id')
        if not nid or not isinstance(nid, str) or not nid.replace('_', '').isalnum():
            e.append(f'{tag}: id は英数字とアンダースコアだけの英語のidにしてください')
        elif nid in ids:
            e.append(f'{tag}: id={nid} が重複しています')
        ids.add(nid)
        if n.get('kind') not in KINDS:
            e.append(f'{tag}({nid}): kind は p・i・o のどれかです')
        if not n.get('name'):
            e.append(f'{tag}({nid}): name(日本語名)がありません')
        if not isinstance(n.get('from'), int):
            e.append(f'{tag}({nid}): from(開始年)は数字です')
        if not n.get('desc'):
            e.append(f'{tag}({nid}): desc(説明)がありません')
        if not n.get('src'):
            e.append(f'{tag}({nid}): src(出典)がありません')
        if n.get('conf') not in CONFS:
            e.append(f'{tag}({nid}): conf は 確認済み・報道・未確認 のどれかです')
    for j, ed in enumerate(d.get('edges', [])):
        if ed.get('k') not in EDGE_K:
            e.append(f'edges[{j}]: k={ed.get("k")} は使えない種類です')
        if known_ids is not None:   # 実際のビルド時だけ、線の両端が図にあるかを見る
            for side in ('a', 'b'):
                v = ed.get(side)
                if v not in ids and v not in known_ids:
                    e.append(f'edges[{j}]: {side}={v} が図にありません(新しい人は nodes に入れる)')
    return e


def _legacy_known(key, ADDS):
    return {n['id'] for n in ADDS[key].get('nodes', [])} | {key}


def apply_ext(CO, ADDS=None, LEGACY_EDGES=None):
    """CO(会社キー→データ)に外部データを足す。build_hub2.py から呼ばれる。
    openai/anthropic/xai/meta(手作りの図)は、ADDS の nodes・en と LEGACY_EDGES に足す"""
    ADDS = ADDS or {}
    LEGACY_EDGES = LEGACY_EDGES if LEGACY_EDGES is not None else {}
    items, errs = _load()
    for fn, d in items:
        key = d.get('company')
        if key in LEGACY_KEYS:
            known = _legacy_known(key, ADDS) if key in ADDS else {key}
        elif key in CO:
            known = {n['id'] for n in CO[key]['N']} | {key}
        else:
            known = {key}
        errs += [f'{fn}: {m}' for m in check(d, fn, known_ids=known)]
    if errs:
        sys.exit('外部AIのデータに誤りがあるため、ビルドを止めました:\n  ' + '\n  '.join(errs))
    for fn, d in items:
        key = d['company']
        if key in LEGACY_KEYS:
            a = ADDS.setdefault(key, dict(nodes=[], en={}, edges=''))
            c = dict(N=a['nodes'], EN=a['en'], edges=None)
            LEGACY_EDGES.setdefault(key, [])
            have = {n['id'] for n in a['nodes']}
        elif key in CO:
            c = CO[key]
            have = {n['id'] for n in c['N']}
        else:
            print(f'[ext] {fn}: 会社キー {key} がないためスキップ', file=sys.stderr)
            continue
        added = 0
        for n in d.get('nodes', []):
            if n['id'] in have:
                print(f'[ext] {fn}: id={n["id"]} は既にあるため追加しない', file=sys.stderr)
                continue
            node = {'id': n['id'], 'name': n['name'], 'kind': n['kind'], 'from': n['from'],
                    'desc': f'{n["desc"]}（出典: {n["src"]}・{n["conf"]}）', 'role': n.get('role', '')}
            if n.get('to'):
                node['to'] = n['to']
            if n.get('founder'):
                node['founder'] = 1
            c['N'].append(node)
            have.add(n['id'])
            added += 1
        c['EN'].update(d.get('en', {}))
        if key in LEGACY_KEYS:
            for ed in d.get('edges', []):
                x = {'a': ed['a'], 'b': ed['b'], 'k': ed['k']}
                if ed.get('label'):
                    x['label'] = ed['label']
                LEGACY_EDGES[key].append(x)
            print(f'[ext] {fn}: {key} に {added} 件追加', file=sys.stderr)
            continue
        js = ''
        for ed in d.get('edges', []):
            parts = [f"a:{json.dumps(ed['a'], ensure_ascii=False)}", f"b:{json.dumps(ed['b'], ensure_ascii=False)}", f"k:{json.dumps(ed['k'])}"]
            if ed.get('label'):
                parts.append(f"label:{json.dumps(ed['label'], ensure_ascii=False)}")
            js += 'E.push({' + ','.join(parts) + '});\n'
        if js:
            c['edges'] = c['edges'].rstrip('\n') + '\n' + js
        print(f'[ext] {fn}: {key} に {added} 件追加', file=sys.stderr)
    return CO


if __name__ == '__main__':
    for _s in (sys.stdout, sys.stderr):
        try:
            _s.reconfigure(encoding='utf-8', errors='replace')   # cp932のコンソールでも文字化けしないように
        except Exception:
            pass
    items, errs = _load()
    if errs:
        print('\n'.join(errs))
    total = 0
    for fn, d in items:
        e = check(d, fn)
        total += len(d.get('nodes', []))
        print(('NG  ' if e else 'OK  ') + fn + f'  人物・組織 {len(d.get("nodes", []))} 件' + (f'  / エラー {len(e)} 件' if e else ''))
        for m in e:
            print('      ' + m)
    if not items:
        print('ext_adds/ にファイルがありません(_テンプレート.json を参考に作ってください)。')
    sys.exit(1 if errs or any(check(d, fn) for fn, d in items) else 0)
