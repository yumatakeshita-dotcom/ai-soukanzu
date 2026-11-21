# -*- coding: utf-8 -*-
"""週のまとめ(ニュースレター)を作る。

1週間分の「調査タスクの候補(inbox/)」と「相関図の更新記録(site/index.html の UPDATES)」を集めて、
次の3つを作る。
  newsletter/issues/YYYY-MM-DD.json   その号のデータ(号ごとに1つ。前の号は消さない)
  newsletter/YYYY-MM-DD.md            その号の文章(メールやnoteに貼れる形)
  site/weekly/index.html              ニュースレターのページ(最新号+過去の号の一覧)

使い方:
  python3 scripts/weekly.py                      今日(日本時間)を発行日にして、前の月曜〜日曜をまとめる
  python3 scripts/weekly.py --date 2026-11-23    発行日を指定
  python3 scripts/weekly.py --start 2026-11-11 --end 2026-11-18   期間を指定
  python3 scripts/weekly.py --render-only        号のデータは作らず、ページと .md だけ作り直す

冒頭の「今週のポイント」は newsletter/lead/YYYY-MM-DD.md(発行日)に書いておくと使われる。
無ければ件数から短い文を自動で作る。
足すだけ: inbox/ や index.html は読むだけで書き換えない。
"""
import argparse, datetime, glob, html, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import merge_inbox as mi  # 題名・説明文・重複判定を「調査の新着」とそろえる
import finds_map

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NL = os.path.join(ROOT, 'newsletter')
ISSUES = os.path.join(NL, 'issues')
LEAD = os.path.join(NL, 'lead')
PAGE = os.path.join(ROOT, 'site', 'weekly', 'index.html')
MAP_URL = 'https://claude.ai/artifact/FzzqJz3KhB1fptjKvFvWZu'
WEEKLY_URL = 'https://claude.ai/artifact/WnWyUzjmrSVHcxVgzKWPCM'  # このページ(site/weekly/index.html)の共有リンク
JST = datetime.timezone(datetime.timedelta(hours=9))

SECTIONS = [
    ('updates', '大きなニュース', '相関図の毎日の更新で記録した、主要企業の動き'),
    ('money', 'お金の流れ', '出資・買収・共同創業'),
    ('moves', '人の動き', '引き抜き・移籍・退任'),
    ('vc', 'ファンドとVC', '新しいファンドと、そこにお金を出した人(LP)'),
    ('deep', '注目の会社', '今週くわしく調べた会社'),
]
WEEKDAY = '月火水木金土日'


def d2s(d):
    return d.strftime('%Y-%m-%d')


def s2d(s):
    return datetime.date.fromisoformat(s)


def jdate(s):
    try:
        d = s2d(s)
        return f'{d.month}月{d.day}日({WEEKDAY[d.weekday()]})'
    except Exception:
        return s or ''


def load_updates():
    """index.html の UPDATES(毎日の更新記録)を読む。書き換えはしない"""
    src = open(os.path.join(ROOT, 'site', 'index.html'), encoding='utf-8').read()
    m = re.search(r'/\* UPDATES_START \*/(.*?)/\* UPDATES_END \*/', src, re.S)
    if not m:
        return []
    js = m.group(1) + '\nprocess.stdout.write(JSON.stringify(UPDATES));'
    try:
        out = subprocess.run(['node', '-e', js], capture_output=True, text=True, check=True).stdout
        return json.loads(out)
    except Exception as e:
        print('UPDATES を読めなかった(とばす):', e, file=sys.stderr)
        return []


def collect(start, end):
    """期間内の項目を集める。
    main: 出来事の日付が期間内のもの
    found: 期間内の調査で見つかったが、出来事の日付が期間より前のもの(過去の動き)"""
    sec = {k: [] for k, _, _ in SECTIONS}
    found = []
    keys = set()
    files_in_week = set()
    for u in load_updates():
        d = str(u.get('d') or '')[:10]
        if start <= d <= end:
            s = u.get('src') or []
            sec['updates'].append({'d': d, 't': u.get('t', ''), 'x': '', 'c': '',
                                   'src': [[s[0], s[1]]] if len(s) >= 2 else [], 'co': u.get('co') or []})
    for kind in ['money', 'moves', 'vc', 'deep']:
        for f in sorted(glob.glob(os.path.join(ROOT, 'inbox', kind, '*.json'))):
            try:
                data = json.load(open(f, encoding='utf-8'))
            except Exception as e:
                print('読めないファイル(とばす):', f, e, file=sys.stderr)
                continue
            fdate = str(data.get('date') or os.path.basename(f)[:10])[:10]
            in_week_file = start <= fdate <= end
            if in_week_file:
                files_in_week.add(os.path.relpath(f, ROOT).replace(os.sep, '/'))
            for it in data.get('items') or []:
                if not isinstance(it, dict) or not mi.src_list(it):
                    continue
                k = mi.key_of(kind, it)
                if k in keys:
                    continue
                d = str(it.get('date') or '')[:10]
                row = {'d': d or fdate, 't': mi.title_of(kind, it), 'x': mi.detail_of(kind, it)[:300],
                       'c': it.get('confidence') or '', 'src': mi.src_list(it)[:2], 'k': kind}
                if it.get('quote'):
                    row['q'] = str(it['quote'])[:200]
                if kind == 'money':
                    row['kind'] = it.get('kind') or ''
                if kind == 'deep':
                    if in_week_file:
                        keys.add(k)
                        sec['deep'].append(row)
                    continue
                if start <= d <= end:
                    keys.add(k)
                    sec[kind].append(row)
                elif in_week_file and d and d < start:
                    keys.add(k)
                    found.append(row)
    for k in sec:
        sec[k].sort(key=lambda r: (r['d'], r.get('c') == '公式'), reverse=True)
    found.sort(key=lambda r: r['d'], reverse=True)
    edges = [r for r in finds_map.build() if r.get('f') in files_in_week]
    return sec, found, edges


def auto_lead(sec, found):
    n = {k: len(v) for k, v in sec.items()}
    buy = sum(1 for r in sec['money'] if r.get('kind') == '買収')
    inv = sum(1 for r in sec['money'] if r.get('kind') == '出資')
    lines = []
    if sec['updates']:
        lines.append('今週いちばん大きな動き: ' + sec['updates'][0]['t'])
    lines.append(f'出資 {inv}件・買収 {buy}件、人の動き {n["moves"]}件、新しいファンド {n["vc"]}件を記録しました。')
    if found:
        lines.append(f'調査で、これまで抜けていた過去の動きも {len(found)}件見つかりました。')
    return '\n'.join('- ' + l for l in lines)


def build_issue(date, start, end):
    sec, found, edges = collect(start, end)
    lead_path = os.path.join(LEAD, date + '.md')
    lead = open(lead_path, encoding='utf-8').read().strip() if os.path.exists(lead_path) else auto_lead(sec, found)
    nums = sorted(os.path.basename(p)[:10] for p in glob.glob(os.path.join(ISSUES, '*.json')))
    no = (nums.index(date) + 1) if date in nums else len(nums) + 1
    from collections import Counter
    return {
        'no': no, 'date': date, 'start': start, 'end': end, 'lead': lead,
        'sections': sec, 'found': found,
        'counts': {k: len(v) for k, v in sec.items()} | {'found': len(found), 'edges': len(edges)},
        'edge_kinds': dict(Counter(r['k'] for r in edges)),
        'made': datetime.datetime.now(JST).strftime('%Y-%m-%d %H:%M'),
    }


# ---------- 文章(Markdown) ----------

def md_item(r):
    conf = f'〔{r["c"]}〕' if r.get('c') else ''
    s = f'- **{r["t"]}** {conf}({jdate(r["d"])})'
    if r.get('x'):
        s += f'\n  {r["x"]}'
    if r.get('q'):
        s += f'\n  > {r["q"]}'
    if r.get('src'):
        s += '\n  出典: ' + ' / '.join(f'[{a}]({b})' for a, b in r['src'])
    return s


def to_md(iss):
    out = [f'# 今週のAIのお金と人の動き 第{iss["no"]}号',
           f'{jdate(iss["start"])}〜{jdate(iss["end"])} / 発行 {jdate(iss["date"])}', '',
           '## 今週のポイント', iss['lead'], '']
    for k, name, desc in SECTIONS:
        rows = iss['sections'][k]
        if not rows:
            continue
        out += [f'## {name}({len(rows)}件)', f'_{desc}_', ''] + [md_item(r) for r in rows] + ['']
    if iss['found']:
        out += [f'## 調査で見つかった過去の動き({len(iss["found"])}件)',
                '_今週の調査で見つかった、これまで相関図に無かった動き_', '']
        out += [md_item(r) for r in iss['found'][:12]]
        if len(iss['found']) > 12:
            out.append(f'- ほか {len(iss["found"]) - 12}件は相関図の「調査の新着」で見られます')
        out.append('')
    out += ['---',
            '〔公式〕は会社の発表、〔報道〕は報道ベースです。金額は報道ベースや契約の上限のことがあり、そのときは本文に書いています。',
            f'相関図: {MAP_URL}', f'過去の号: {WEEKLY_URL}', '']
    return '\n'.join(out)


# ---------- ページ(HTML) ----------

def e(x):
    return html.escape(str(x or ''), quote=True)


def html_item(r):
    conf = ''
    if r.get('c'):
        cls = 'off' if r['c'] == '公式' else 'rep'
        conf = f'<span class="conf {cls}">{e(r["c"])}</span>'
    src = ''.join(f'<a href="{e(b)}" target="_blank" rel="noopener">{e(a)}</a>' for a, b in r.get('src') or [])
    q = f'<blockquote>{e(r["q"])}</blockquote>' if r.get('q') else ''
    x = f'<p class="x">{e(r["x"])}</p>' if r.get('x') else ''
    return (f'<li><div class="meta"><time datetime="{e(r["d"])}">{e(jdate(r["d"]))}</time>{conf}</div>'
            f'<p class="t">{e(r["t"])}</p>{x}{q}<div class="src">{src}</div></li>')


def lead_html(lead):
    lines = [l.strip() for l in lead.splitlines() if l.strip()]
    if all(l.startswith(('- ', '・')) for l in lines):
        return '<ul class="lead">' + ''.join(f'<li>{e(l[2:] if l.startswith("- ") else l[1:])}</li>' for l in lines) + '</ul>'
    return ''.join(f'<p class="lead">{e(l)}</p>' for l in lines)


def issue_html(iss, open_=True):
    c = iss['counts']
    tiles = [('お金の流れ', c['money'], 'money'), ('人の動き', c['moves'], 'moves'),
             ('ファンド', c['vc'], 'vc'), ('過去の動き', c['found'], 'found')]
    tile_html = ''.join(f'<div class="tile {k}"><b>{n}</b><span>{e(lbl)}</span></div>' for lbl, n, k in tiles)
    body = [f'<div class="tiles">{tile_html}</div>', '<h3>今週のポイント</h3>', lead_html(iss['lead'])]
    for k, name, desc in SECTIONS:
        rows = iss['sections'][k]
        if rows:
            body.append(f'<section class="sec {k}"><h3>{e(name)}<small>{len(rows)}件</small></h3>'
                        f'<p class="desc">{e(desc)}</p><ul class="items">{"".join(html_item(r) for r in rows)}</ul></section>')
    if iss['found']:
        rows = iss['found'][:12]
        more = f'<p class="desc">ほか {len(iss["found"]) - 12}件は相関図の「調査の新着」にあります。</p>' if len(iss['found']) > 12 else ''
        body.append(f'<section class="sec found"><h3>調査で見つかった過去の動き<small>{len(iss["found"])}件</small></h3>'
                    f'<p class="desc">今週の調査で見つかった、これまで相関図に無かった動き</p>'
                    f'<ul class="items">{"".join(html_item(r) for r in rows)}</ul>{more}</section>')
    head = (f'<span class="no">第{iss["no"]}号</span>'
            f'<span class="range">{e(jdate(iss["start"]))}〜{e(jdate(iss["end"]))}</span>')
    md = e(to_md(iss))
    tools = (f'<div class="tools"><button type="button" class="copy" data-target="md-{e(iss["date"])}">'
             f'メールやnoteに貼る文章をコピー</button><span class="copied" role="status"></span></div>'
             f'<textarea id="md-{e(iss["date"])}" class="md" readonly aria-label="貼り付け用の文章">{md}</textarea>')
    inner = ''.join(body) + tools
    if open_:
        return f'<article class="issue" id="i{e(iss["date"])}"><header class="ih">{head}</header>{inner}</article>'
    return (f'<details class="issue past" id="i{e(iss["date"])}"><summary>{head}'
            f'<span class="sum">お金 {c["money"]}・人 {c["moves"]}・ファンド {c["vc"]}</span></summary>{inner}</details>')


CSS = '''
/* Layout: 1列の読みもの。号の頭に件数の札、その下に種類ごとの一覧。色は相関図本体と同じ変数 */
:root{
  --bg:#f2f4f6; --surface:#ffffff; --fg:#161b22; --muted:#5d6875; --line:#d5dbe1;
  --active:#0d8a79; --left:#d9772b; --invest:#4a5dd0; --pink:#b8397a; --deal:#8f6500; --org:#6a7684;
  --font-body:"Noto Sans JP",system-ui,-apple-system,"Hiragino Sans","Yu Gothic",sans-serif;
  --font-mono:"IBM Plex Mono",ui-monospace,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#11151a; --surface:#1a2027; --fg:#e8ecf0; --muted:#97a3b0; --line:#2e3741;
  --active:#2fc2ab; --left:#f09a55; --invest:#8394f5; --pink:#f08cbc; --deal:#e6b84a; --org:#97a3b0; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#11151a; --surface:#1a2027; --fg:#e8ecf0; --muted:#97a3b0; --line:#2e3741;
  --active:#2fc2ab; --left:#f09a55; --invest:#8394f5; --pink:#f08cbc; --deal:#e6b84a; --org:#97a3b0; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--font-body);font-size:15px;line-height:1.7;margin:0;
  padding-block:28px 56px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:720px;margin:0 auto;display:flex;flex-direction:column;gap:28px}
.mast{display:flex;flex-direction:column;gap:6px;border-bottom:2px solid var(--fg);padding-bottom:16px}
.mast .eyebrow{font-family:var(--font-mono);font-size:12px;letter-spacing:.08em;color:var(--muted)}
.mast h1{margin:0;font-size:clamp(24px,6vw,34px);line-height:1.3;text-wrap:balance}
.mast p{margin:0;color:var(--muted);font-size:14px}
.mast a{color:var(--active)}
.issue{display:flex;flex-direction:column;gap:14px;min-width:0}
.ih,.issue summary{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px}
.no{font-weight:700;font-size:20px}
.range{font-family:var(--font-mono);font-size:13px;color:var(--muted)}
.tiles{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.tile{background:var(--surface);border:1px solid var(--line);border-top:3px solid var(--c,var(--org));border-radius:4px;padding:8px 10px;display:flex;flex-direction:column}
.tile b{font-family:var(--font-mono);font-size:24px;font-variant-numeric:tabular-nums;line-height:1.2}
.tile span{font-size:12px;color:var(--muted)}
.money{--c:var(--invest)} .moves{--c:var(--left)} .vc{--c:var(--active)} .deep{--c:var(--pink)} .updates{--c:var(--deal)} .found{--c:var(--org)}
h3{margin:12px 0 0;font-size:17px;display:flex;align-items:baseline;gap:8px}
h3 small{font-family:var(--font-mono);font-size:12px;color:var(--muted);font-weight:400}
.sec h3::before{content:"";width:10px;height:10px;border-radius:2px;background:var(--c);flex:none;align-self:center}
.desc{margin:0;color:var(--muted);font-size:13px}
.lead{margin:0;padding-left:1.2em} .lead li{margin:2px 0} p.lead{padding-left:0}
.items{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-direction:column}
.items li{padding:12px 0;border-top:1px solid var(--line);min-width:0}
.meta{display:flex;gap:8px;align-items:center;font-family:var(--font-mono);font-size:12px;color:var(--muted)}
.conf{font-family:var(--font-body);font-size:11px;padding:0 6px;border-radius:3px;border:1px solid currentColor}
.conf.off{color:var(--active)} .conf.rep{color:var(--deal)}
.t{margin:2px 0 0;font-weight:500;overflow-wrap:anywhere}
.x{margin:2px 0 0;font-size:13.5px;color:var(--muted);overflow-wrap:anywhere}
blockquote{margin:6px 0 0;padding-left:10px;border-left:2px solid var(--line);font-size:13.5px}
.src{display:flex;flex-wrap:wrap;gap:2px 12px;font-size:12px;margin-top:4px}
.src a{color:var(--active);overflow-wrap:anywhere}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:8px}
button{font:inherit;font-size:13px;background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:4px;padding:6px 12px;cursor:pointer}
button:hover{border-color:var(--active)} button:focus-visible,summary:focus-visible{outline:2px solid var(--active);outline-offset:2px}
.copied{font-size:12px;color:var(--active)}
.md{width:100%;height:9em;font-family:var(--font-mono);font-size:12px;background:var(--surface);color:var(--fg);border:1px solid var(--line);border-radius:4px;padding:8px}
.past{border-top:1px solid var(--line);padding-top:10px}
.past summary{cursor:pointer;list-style:none} .past summary::-webkit-details-marker{display:none}
.past summary .no{font-size:16px} .past .sum{font-size:12px;color:var(--muted)}
.past[open]{gap:14px;display:flex;flex-direction:column}
h2{font-size:14px;margin:0;color:var(--muted);letter-spacing:.06em}
footer{font-size:12.5px;color:var(--muted);border-top:1px solid var(--line);padding-top:14px}
footer a{color:var(--active)}
@media (max-width:480px){.tiles{grid-template-columns:repeat(2,minmax(0,1fr))}}
'''

JS = '''
document.querySelectorAll('button.copy').forEach(function(b){
  b.addEventListener('click',function(){
    var ta=document.getElementById(b.dataset.target), msg=b.parentNode.querySelector('.copied');
    function sel(){ta.focus();ta.select();msg.textContent='選択しました。コピーしてください';}
    try{navigator.clipboard.writeText(ta.value).then(function(){msg.textContent='コピーしました';},sel);}catch(err){sel();}
  });
});
'''


def render_page(issues):
    issues = sorted(issues, key=lambda i: i['date'], reverse=True)
    latest, past = issues[0], issues[1:]
    past_html = ''
    if past:
        past_html = '<section class="backs"><h2>過去の号</h2>' + ''.join(issue_html(i, False) for i in past) + '</section>'
    return f'''<title>AIのお金と人の動き</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+JP:wght@400;500;700&display=swap">
<style>{CSS}</style>
<div class="wrap">
<header class="mast">
<span class="eyebrow">WEEKLY · 毎週月曜</span>
<h1>今週のAIのお金と人の動き</h1>
<p>AI企業・半導体企業の出資、買収、引き抜きを1週間分まとめています。すべてに出典があります。もとのデータは<a href="{MAP_URL}" target="_blank" rel="noopener">AI企業の相関図</a>。</p>
</header>
{issue_html(latest)}
{past_html}
<footer>〔公式〕は会社の発表、〔報道〕は報道ベースです。金額は報道ベースや契約の上限のことがあり、そのときは本文に書いています。最終更新 {e(latest["made"])}(日本時間)</footer>
</div>
<script>{JS}</script>
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--date')
    ap.add_argument('--start')
    ap.add_argument('--end')
    ap.add_argument('--render-only', action='store_true')
    a = ap.parse_args()
    os.makedirs(ISSUES, exist_ok=True)
    if not a.render_only:
        date = a.date or datetime.datetime.now(JST).strftime('%Y-%m-%d')
        dd = s2d(date)
        last_sun = dd - datetime.timedelta(days=dd.weekday() + 1)
        start = a.start or d2s(last_sun - datetime.timedelta(days=6))
        end = a.end or d2s(last_sun)
        iss = build_issue(date, start, end)
        json.dump(iss, open(os.path.join(ISSUES, date + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'第{iss["no"]}号 {start}〜{end}: ' + ', '.join(f'{k} {v}' for k, v in iss['counts'].items()))
    issues = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(ISSUES, '*.json')))]
    if not issues:
        print('号がまだない')
        return
    for iss in issues:
        open(os.path.join(NL, iss['date'] + '.md'), 'w', encoding='utf-8').write(to_md(iss))
    os.makedirs(os.path.dirname(PAGE), exist_ok=True)
    open(PAGE, 'w', encoding='utf-8').write(render_page(issues))
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'seo.py')], check=False)  # 共有カード用の meta を入れ直す
    print('作ったもの:', os.path.relpath(PAGE, ROOT), f'newsletter/ に .md {len(issues)}号分')
    # 法的ページへのフッターリンクを入れ直す(設定がOFFなら何も足さない)
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'legal.py')], check=False)


if __name__ == '__main__':
    main()
