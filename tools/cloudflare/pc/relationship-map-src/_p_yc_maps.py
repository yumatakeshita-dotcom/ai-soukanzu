p = 'ai_wd_to_maps.py'
s = open(p, encoding='utf-8').read()
old = "json.dump(out, open(os.path.join(S, 'ai_wd_maps.json'), 'w', encoding='utf-8'), ensure_ascii=False)"
new = '''# ---- Y Combinatorの公式ディレクトリ(yc_founders.json)から ----
yp = os.path.join(S, 'yc_founders.json')
nyc = 0
if os.path.exists(yp):
    seen = {norm(x['name']) for x in out}
    ycid = {r['slug']: r.get('id') for r in json.load(open(os.path.join(S, 'yc_all.json'), encoding='utf-8'))}
    rows = []
    for slug, v in json.load(open(yp, encoding='utf-8')).items():
        nm = (v.get('name') or '').strip()
        k = norm(nm)
        if v.get('err') or not v.get('founders') or not nm or len(k) < 2 or k in mapped or k in seen or any(k.startswith(m) for m in LONG):
            continue
        rows.append((v.get('status') != 'Active' and v.get('status') != 'Public', nm, slug, v))
    rows.sort(key=lambda x: (x[0], x[1].lower()))
    for _, nm, slug, v in rows:
        seen.add(norm(nm))
        yr = v.get('year') if isinstance(v.get('year'), int) and v.get('year') > 1990 else 2000
        out.append({'q': 'Y%s' % ycid.get(slug, slug), 'name': nm, 'year': yr, 'web': v.get('web') or '',
                    'p': [{'p': 'y%d' % i, 'name': f['n'], 'rel': ('CEO' if 'CEO' in (f.get('t') or '') else '創業者'), 't': f.get('t') or ''} for i, f in enumerate(v['founders'])],
                    'i': [], 'o': [], 'yc': {'b': v.get('batch') or '', 'one': v.get('one') or '', 'loc': v.get('loc') or '', 'team': v.get('team'), 'st': v.get('status') or ''}})
        nyc += 1
print('Y Combinatorから', nyc, '社')
json.dump(out, open(os.path.join(S, 'ai_wd_maps.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))'''
assert old in s
s = s.replace(old, new, 1)
open(p, 'w', encoding='utf-8').write(s)

p = 'newco_data10w.py'
w = open(p, encoding='utf-8').read()
old = "        desc = '%s年ごろに設立された、AI分野の会社(Wikidataの分野の記録による)。' % c['year'] if c['year'] != 2000 else 'AI分野の会社(Wikidataの分野の記録による)。設立年は確認できていません。'\n"
new = """        desc = '%s年ごろに設立された、AI分野の会社(Wikidataの分野の記録による)。' % c['year'] if c['year'] != 2000 else 'AI分野の会社(Wikidataの分野の記録による)。設立年は確認できていません。'
        note = NOTE_W
        yc = c.get('yc')
        if yc:
            note = NOTE_Y
            desc = 'Y Combinator(%s)の、AI分野の会社。%s%s%s' % (yc['b'], (yc['one'] + '。') if yc['one'] else '', ('所在地: %s。' % yc['loc']) if yc['loc'] else '', ('チーム%s人。' % yc['team']) if yc.get('team') else '')
            items = []
            for r in c['p']:
                items.append(P('w' + r['p'], r['name'], en(r['name']), c['year'], 'Y Combinatorの公式ディレクトリに、%sと記載。' % (r.get('t') or '創業者'), (r.get('t') or '創業者'), None, 1))
            items.append(O('yc', 'Y Combinator', c['year'], 'Y Combinator(%s)のスタートアップ。' % yc['b'], 'アクセラレーター(%s)' % yc['b'], 'i'))
            edges = []
"""
assert old in w
w = w.replace(old, new, 1)
w = w.replace("        st('stw_' + c['q'], c['name'], c['year'], NOTE_W, items, edges, desc)", "        st('stw_' + c['q'], c['name'], c['year'], note, items, edges, desc)", 1)
w = w.replace("AIWD = []", "NOTE_Y = 'Y Combinatorの公式ディレクトリ(2026年11月取得)に基づきます。創業者・肩書き・所在地などは、各社のページの記載です。出資者や金額は載せていません。顔写真がない人はイニシャル表示です。'\nAIWD = []", 1)
open(p, 'w', encoding='utf-8').write(w)
g = open('_merge_insta.py', encoding='utf-8').read()
g = g.replace("stw_Q[0-9]+", "stw_[QY][A-Za-z0-9]+", 1)
open('_merge_insta.py', 'w', encoding='utf-8').write(g)
print('ok')
