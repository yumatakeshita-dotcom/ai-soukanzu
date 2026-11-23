# -*- coding: utf-8 -*-
"""調査タスクの結果(inbox/*/*.json)から、相関図に足す「つながり」(FINDLINKS)を作る。

merge_inbox.py から呼ばれ、site/data/finds.js の2行目に const FINDLINKS=[...] として書く。
どの会社の図に付けるか(名前→図)は、サイトが開いたときに会社の一覧と照らして決める(index.html の applyFinds)。
inbox/ は足すだけなので、毎回ぜんぶ作り直しても、前にあったつながりは消えない。

1件の形:
  {k:'move', p:[名前, 英語名], fr:元の所属, to:行き先, r:役職, ...}  引き抜き・移籍
  {k:'inv',  i:[出資者...], to:出資先, ...}                          出資(LP→ファンドも含む)
  {k:'acq',  fr:買った会社, to:買われた会社, ...}                    買収
  {k:'deal', fr:会社, to:取引先, ...}                                取引・提携
  共通: y=年, lb=短い説明, d=説明文, s=[[出典名,URL]...], c=確かさ, f=元のファイル
"""
import json, os, re, glob
import quality_hold

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _s(x):
    return x.strip() if isinstance(x, str) else ''


def _src(lst):
    out = []
    for s in lst or []:
        if isinstance(s, (list, tuple)) and len(s) >= 2 and str(s[1]).startswith('http'):
            out.append([str(s[0])[:80], str(s[1])])
        elif isinstance(s, str) and s.startswith('http'):
            out.append([s[:80], s])
    return out[:3]


def _year(it, d):
    m = re.match(r'(\d{4})', str(it.get('date') or d.get('date') or ''))
    return int(m.group(1)) if m else None


def _noparen(x):
    return re.sub(r'[((][^))]*[))]', '', _s(x)).strip()


def split_names(x):
    """「A・B(共同リード)、C ほか」→ [A, B, C]"""
    x = _noparen(x)
    x = re.sub(r'(ほか|など|他)\s*$', '', x)
    out = []
    for p in re.split(r'[、,，。]|・(?=[A-Za-z0-9])|(?<=[A-Za-z0-9.])・', x):
        p = re.sub(r'^(and|&)\s+|^(個人で|事業会社として|事業会社の)', '', p.strip()).strip()
        p = re.sub(r'\s*(ほか|など)$', '', p)
        if p and len(p) <= 60 and not re.search(r'非公表|未公表|不明', p):
            out.append(p)
    return out


def _unknown(x):
    return (not _s(x)) or bool(re.search(r'未定|未発表|未公表|非公表|退任|療養|休養|社外|不明', _s(x)))


def short_amount(x):
    x = _s(x)
    x = re.split(r'[((]', x)[0].strip()
    return x[:16]


def build():
    out, seen = [], set()

    def add(rec, it, d, f, src=None):
        s = _src(src if src is not None else it.get('src'))
        if not s:
            return
        rec.update({'y': _year(it, d), 's': s, 'c': _s(it.get('confidence')), 'f': os.path.relpath(f, ROOT).replace(os.sep, '/')})
        if rec.get('d'):
            rec['d'] = rec['d'][:300]
        key = json.dumps({k: v for k, v in rec.items() if k in ('k', 'p', 'fr', 'to', 'i')}, ensure_ascii=False, sort_keys=True)
        if key in seen:
            return
        seen.add(key)
        out.append(rec)

    for kind in ['moves', 'money', 'vc', 'deep']:
        for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', kind, '*.json'))):
            try:
                d = json.load(open(f, encoding='utf-8'))
            except Exception:
                continue
            for it in d.get('items') or []:
                if not isinstance(it, dict) or quality_hold.hold_reason(it):
                    continue  # 品質チェックの「問題」は保留(取り込まない)
                note = _s(it.get('note'))
                date = _s(it.get('date'))[:10]
                if kind == 'moves':
                    ja, en = _s(it.get('name_ja')), _s(it.get('name_en'))
                    if not (ja or en):
                        continue
                    fr, to, role = _s(it.get('from')), _s(it.get('to')), _s(it.get('role'))
                    desc = f"{fr} → {to}" + (f"({role})" if role else '') + (f"、{date}" if date else '') + '。' + note
                    add({'k': 'move', 'p': [ja or en, en], 'fr': fr, 'to': '' if _unknown(to) else to, 'r': role[:40], 'lb': _noparen(role)[:20], 'd': desc}, it, d, f)
                elif kind == 'money':
                    mk = _s(it.get('kind'))
                    fr, to = _s(it.get('from')), _s(it.get('to'))
                    amt = short_amount(it.get('amount'))
                    desc = f"{_noparen(fr)} → {to}({mk}" + (f" {_s(it.get('amount'))}" if it.get('amount') else '') + ')' + (f"、{date}" if date else '') + '。' + note
                    if mk == '買収':
                        add({'k': 'acq', 'fr': _noparen(fr), 'to': _noparen(to), 'lb': ('買収 ' + amt).strip(), 'd': desc}, it, d, f)
                    elif mk in ('出資', '支援', '投資'):
                        inv = split_names(fr)
                        for t in (split_names(to) if inv else []):
                            add({'k': 'inv', 'i': inv, 'to': t, 'lb': amt or mk, 'd': desc}, it, d, f)
                    # 共同創業などの人どうしの関係は、図には足さない(調査の新着には出る)
                elif kind == 'vc':
                    gp, fund, lp, st = _s(it.get('gp')), _s(it.get('fund')), _s(it.get('lp')), _s(it.get('startup'))
                    size = short_amount(it.get('size'))
                    if st:
                        desc = f"{_noparen(gp)} → {st}" + (f"({_s(it.get('size'))})" if it.get('size') else '') + (f"、{date}" if date else '') + '。' + note
                        add({'k': 'inv', 'i': split_names(gp), 'to': _noparen(st), 'lb': size, 'd': desc}, it, d, f)
                        if lp and split_names(lp):
                            add({'k': 'inv', 'i': split_names(lp), 'to': _noparen(st), 'lb': '', 'd': desc}, it, d, f)
                    elif fund:
                        fname = _noparen(fund) or fund
                        desc = f"{_noparen(gp)} のファンド「{fund}」" + (f"({_s(it.get('size'))})" if it.get('size') else '') + (f"、LP: {lp}" if lp else '') + (f"、{date}" if date else '') + '。' + note
                        if gp:
                            add({'k': 'inv', 'i': split_names(gp)[:1], 'to': fname, 'lb': ('運営 ' + size).strip(), 'd': desc, 'fund': 1}, it, d, f)
                        if lp and split_names(lp):
                            add({'k': 'inv', 'i': split_names(lp), 'to': fname, 'lb': 'LP', 'd': desc, 'fund': 1}, it, d, f)
                elif kind == 'deep':
                    co = _s(it.get('company_en')) or _s(it.get('company_ja'))
                    if not co:
                        continue
                    what = _s(it.get('what'))
                    for p in it.get('people') or []:
                        if not isinstance(p, dict) or not _s(p.get('name')):
                            continue
                        nm = _s(p['name'])
                        m = re.match(r'^(.*?)[((]([^))]*)[))]\s*$', nm)
                        en, ja = (m.group(1).strip(), m.group(2).strip()) if m else (nm, nm)
                        if re.search(r'[A-Za-z]', ja) and not re.search(r'[A-Za-z]', en):
                            en, ja = ja, en
                        role, prev = _s(p.get('role')), _s(p.get('prev'))
                        desc = f"{co}({what})の{role}。" + (f"前は {prev}。" if prev else '')
                        add({'k': 'move', 'p': [ja or en, en], 'fr': _noparen(prev), 'to': co, 'r': role[:40], 'lb': _noparen(role)[:20], 'd': desc}, it, d, f, p.get('src') or it.get('src'))
                    for p in it.get('investors') or []:
                        if not isinstance(p, dict) or not _s(p.get('name')):
                            continue
                        amt = short_amount(p.get('amount'))
                        desc = f"{_noparen(p['name'])} → {co}(" + ' '.join(x for x in [_s(p.get('round')), _s(p.get('amount'))] if x) + ')。'
                        add({'k': 'inv', 'i': split_names(p['name']), 'to': co, 'lb': amt, 'd': desc}, it, d, f, p.get('src') or it.get('src'))
                    for p in it.get('partners') or []:
                        if not isinstance(p, dict) or not _s(p.get('name')):
                            continue
                        what2 = _s(p.get('what')) or _s(p.get('note')) or _s(p.get('kind'))
                        desc = f"{co} と {_s(p['name'])} の取引・提携" + (f"({what2})" if what2 else '') + '。'
                        add({'k': 'deal', 'fr': co, 'to': _noparen(p['name']), 'lb': what2[:16] or '取引', 'd': desc}, it, d, f, p.get('src') or it.get('src'))
    return [r for r in out if r.get('k') != 'inv' or r.get('i')]


def js_line():
    return 'const FINDLINKS=' + json.dumps(build(), ensure_ascii=False, separators=(',', ':')) + ';\n'


if __name__ == '__main__':
    L = build()
    from collections import Counter
    print(len(L), Counter(r['k'] for r in L))
    for r in L:
        print(json.dumps({k: r[k] for k in r if k in ('k', 'p', 'fr', 'to', 'i', 'lb')}, ensure_ascii=False))
