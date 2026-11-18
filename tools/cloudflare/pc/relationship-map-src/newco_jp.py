"""日本の時価総額ランキング上位企業の図(自動作成)。元データ: jp_nikkei.json(日経の会社概要) と jp_cos.json(Wikidata)。
手作りの図がある会社は作らない。データが無ければ空。"""
import json, os, re
from newco_data import mk, std
from jp_manual import MANUAL, SRC_NOTE

S = os.path.dirname(os.path.abspath(__file__))
COJP = {}
JPCO = []
HAVE = {'9984', '4755', '9434', '4689', '4385'}   # ソフトバンクG・楽天G・ソフトバンク・LINEヤフー・メルカリは手作りの図がある


def _ld(n, d):
    f = os.path.join(S, n)
    return json.load(open(f, encoding='utf-8')) if os.path.exists(f) else d


ROLE = {'ceo': ('CEO・代表(Wikidata)', 'p'), 'chair': ('会長(Wikidata)', 'p'), 'founder': ('創業者(Wikidata)', 'p'),
        'board': ('取締役(Wikidata)', 'p'), 'owner': ('株主(個人・Wikidata)', 'i')}
NOTE = ('代表者は日経の会社概要(2026年11月5日取得)に基づきます。創業者・会長・CEO・取締役・株主は、Wikidataの記録(終了した就任・所有は除外、2026年11月取得)に基づき、'
        '記録のない人や最新の人事・株主構成は載っていない場合があります。時価総額は日経のランキング(2026年11月5日)です。顔写真がない人はイニシャル表示です。')


def _nm(s):
    return re.sub(r'[\s　]+', '', s or '')


def _build():
    nk, jc = _ld('jp_nikkei.json', {}), _ld('jp_cos.json', {})
    rank = {}
    fn = os.path.join(S, 'ranking_jp.txt')
    if os.path.exists(fn):
        for ln in open(fn, encoding='utf-8'):
            a = ln.rstrip('\n').split('|')
            if len(a) >= 6:
                rank[a[2]] = a
    for code, n in nk.items():
        if code in HAVE or code not in rank:
            continue
        r = rank[code]
        name = n['full'] or r[1]
        m = re.search(r'(\d{4})年', n.get('est', ''))
        est = int(m.group(1)) if m else 2026
        cap = int(r[4])
        capt = ('%.2f兆円' % (cap / 1e6)) if cap >= 1e6 else ('%d億円' % round(cap / 100))
        desc = '%s(証券コード %s、%s)。時価総額は約%s(日経のランキング%s位、%s)。' % (name, code, r[3], capt, r[0], r[5])
        bits = []
        if n.get('est'):
            bits.append('設立 ' + n['est'])
        if n.get('addr'):
            bits.append('本社 ' + n['addr'])
        if n.get('cap'):
            bits.append('資本金 ' + n['cap'])
        if n.get('emp'):
            bits.append('従業員 %s人' % n['emp'])
        if bits:
            desc += '、'.join(bits) + '(日経の会社概要)。'
        N = [{'id': 'co', 'name': name, 'kind': 'c', 'from': est, 'desc': desc}]
        EN, seen = {}, set()
        c = jc.get(code, {})
        i = 0
        order = {'founder': 0, 'ceo': 1, 'chair': 2, 'board': 3, 'owner': 4}
        for p in sorted(c.get('people', []), key=lambda x: order.get(x['role'], 9)):
            nm = p['ja'] or p['en']
            if not nm or _nm(nm) in seen:
                continue
            seen.add(_nm(nm))
            role, kind = ROLE[p['role']]
            i += 1
            d = {'id': 'p%d' % i, 'name': nm, 'kind': kind, 'from': p['from'] or est, 'desc': 'Wikidataの記録(2026年11月取得)。', 'role': role}
            if p['role'] == 'founder':
                d['founder'] = 1
                d['from'] = est
            N.append(d)
            if p['en']:
                EN[d['id']] = p['en']
        # 有価証券報告書の「役員の状況」(jp_officers.json): 同じ名前は役職を公式の記載で上書き、無ければ追加(最大22人。会長・社長・代表を先に)
        off = _ld('jp_officers.json', {}).get(code)
        if off and off.get('rows'):
            def _pri(r):
                t = r[0]
                return 0 if re.search(r'会長|社長|代表', t) else 1 if re.search(r'取締役|執行役', t) and '監査' not in t else 2
            asof = off.get('asof', '')
            od = '有価証券報告書の「役員の状況」(%s現在)に基づきます(kabutore.bizの転記を自動で読み取ったもので、表記が崩れている場合があります)。' % (asof or '提出日')
            for rl, nm in sorted(off['rows'], key=_pri)[:22]:
                hit = next((x for x in N if x['kind'] == 'p' and _nm(x['name']) == _nm(nm)), None)
                rl = re.sub(r'^（|）$', '', rl)[:40]
                if hit:
                    hit['role'], hit['desc'] = rl, od
                else:
                    i += 1
                    N.append({'id': 'p%d' % i, 'name': nm, 'kind': 'p', 'from': 2026, 'desc': od, 'role': rl})
                    seen.add(_nm(nm))
        # 検索で確認した役員(jp_manual.py)を重ねる: 同じ名前は役職と説明を上書き、無ければ追加
        for (mn, mrole, myr, mdesc, men) in MANUAL.get(code, []):
            hit = next((x for x in N if x['kind'] == 'p' and _nm(x['name']) == _nm(mn)), None)
            if hit:
                hit['role'], hit['desc'] = mrole, mdesc
                hit['from'] = myr or hit['from']
                if men and hit['id'] not in EN:
                    EN[hit['id']] = men
            else:
                i += 1
                d = {'id': 'p%d' % i, 'name': mn, 'kind': 'p', 'from': myr or 2026, 'desc': mdesc, 'role': mrole}
                if mrole.startswith('創業者') or '創業者' in mrole:
                    d['founder'] = 1
                N.append(d)
                seen.add(_nm(mn))
                if men:
                    EN['p%d' % i] = men
        hold = _ld('jp_holders.json', {}).get(code)
        rep = _nm(n.get('rep', ''))
        if rep:
            hit = next((x for x in N if x['kind'] == 'p' and _nm(x['name']) == rep), None)
            if hit:
                hit['role'] = '代表者・' + hit['role']
                hit['desc'] += ' 日経の会社概要でも代表者として載っています。'
            else:
                N.append({'id': 'rep', 'name': n['rep'], 'kind': 'p', 'from': 2026, 'desc': '日経の会社概要の「代表者氏名」(2026年11月5日取得)。役職は代表取締役などです。', 'role': '代表者(日経の会社概要)'})
                for x in N:      # Wikidataに別のCEOが載っている場合は、古い記録の可能性を明示する
                    if x['kind'] == 'p' and x['role'].startswith('CEO・代表'):
                        x['role'] = 'CEO(Wikidataの記録。日経の代表者と異なる)'
                        x['desc'] += ' 日経の会社概要の代表者(%s)と異なるため、Wikidataの記録が古い可能性があります。' % n['rep']
        holder_ids = {}
        if hold and hold.get('rows'):      # 大株主(IRBANK=EDINETの転記)があれば、Wikidataの所有者よりも新しいので置き換える
            for hn, rk, pct in hold['rows']:
                i += 1
                nm = re.sub(r'株式会社', '', hn).strip()
                N.append({'id': 'h%d' % rk, 'name': nm, 'kind': 'i', 'from': 2026,
                          'desc': '大株主の第%d位(持株比率 約%s%%、%s時点)。出典: IRBANK(EDINETの有価証券報告書・半期報告書の転記)。「信託口」は信託銀行の名義上の保有で、実質的な株主は年金基金・投資信託の運用先などです。' % (rk, pct, hold.get('period', '')),
                          'role': '大株主(約%s%%)' % pct})
                holder_ids['h%d' % rk] = '%s%%' % pct
            desc_hold = '大株主は、IRBANK(EDINETの有価証券報告書の転記)の%s時点の上位10社です。' % hold.get('period', '')
            N[0]['desc'] += desc_hold
        for o in c.get('orgs', []):
            nm = o['ja'] or o['en']
            if holder_ids and o['role'] == 'owner':
                continue
            if not nm or _nm(nm) in seen:
                continue
            seen.add(_nm(nm))
            i += 1
            N.append({'id': 'o%d' % i, 'name': nm, 'kind': 'i', 'from': est, 'desc': 'Wikidataの「%s」の記録(2026年11月取得)。' % ('親会社' if o['role'] == 'parent' else '所有者'), 'role': ('親会社(Wikidata)' if o['role'] == 'parent' else '株主(Wikidataの所有者の記録)')})
        key = 'jp_' + code
        if holder_ids:
            E = "const E = [];\nN.forEach(n=>{ if(n.kind==='p') E.push({a:n.id,b:'co',k:'member'}); if(n.kind==='i' && !/^h\\d+$/.test(n.id)) E.push({a:n.id,b:'co',k:'invest'}); });\n"
            for hid, lab in holder_ids.items():
                E += "E.push({a:'%s',b:'co',k:'invest',label:'%s'});\n" % (hid, lab)
        else:
            E = std('co')
        COJP[key] = mk(N, E, EN, {}, {'co': n['url']} if n.get('url') else {}, {}, {}, {}, 'co')
        JPCO.append({'key': key, 'name': name, 'min': est, 'note': NOTE + (SRC_NOTE if code in MANUAL else ''), 'code': code})


_build()
