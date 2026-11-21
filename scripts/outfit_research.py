# -*- coding: utf-8 -*-
"""起業家・経営者の「公開の場での装い」と関係ブランドを、Geminiで探して機械で確かめる(2026/11/21)。
メニュー「装いとブランド」(site/data/outfit.js)に足す元データを、inbox/outfit/日付.json に作る。

守ること(ここで機械的に守らせる):
  - 画像は保存・転載しない。出典ページのリンクと、装いの文章だけ(画像のURLの欄は作らない)
  - 対象は企業家・経営者・公式に紹介されたスタッフ。公開の場(式典・発表・報道・本人や公式のSNS)の装いだけ。私生活・個人の特定の詮索はしない
  - ブランドは、出典ページの本文にそのブランド名が書いてあるものだけ残す(無ければブランド欄を空にして装いだけ残す)
  - 出典ページが開けて、本人の名前が書いてあるものだけ「合格」。開けないものは「保留」、名前が無いものは「除外」(inbox/outfit/ に理由を残すだけ)
  - Geminiが書いたURLは作り話が多いので、必ず自分で開いて確かめる

使い方:
  python3 scripts/outfit_research.py daily [--people 2]   # people.txt の次の2人を調べる(1人=Gemini 1回)
  python3 scripts/outfit_research.py person "小澤隆生" "Takao Ozawa" "Boost Capital"
  --dry-run  … どこにも書かない
"""
import argparse, datetime, json, os, re, sys, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gemini_research as G

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ODIR = os.path.join(ROOT, 'inbox', 'outfit')
PEOPLE = os.path.join(ODIR, 'people.txt')
DONE = os.path.join(ODIR, 'done.txt')


def prompt(ja, en, co):
    return f"""あなたは、起業家・経営者が公開の場でどんな装いをしているかを、出典つきで調べる担当です。今日は{G.jst_today():%Y年%m月%d日}です。
調べる人: {ja}({en}、{co})

Google検索で、この人が公開の場(式典・記者発表・講演・インタビュー記事・報道・本人や公式のSNS投稿)で着ていたものを、最大5件返してください。
守ること:
- 出典は、その装いが実際に書いてある記事・公式ページ・本人の投稿のURL(https)。見つからないものは入れない。うわさ・推測は入れない
- 画像そのものは扱わない。画像のURLは返さない。装いは文章で説明する
- ブランドは、本人・報道・ブランド公式が明記したものだけ。写真から見た目で当てたブランドは入れない。書いてなければブランドは空にする
- 私生活(家族・自宅・休日の私服など)は対象外。公開の場の装いだけ
- 見つからなければ items は空でよい。作らない

答えは次のJSONだけを ```json と ``` で囲んで返す:
{{"items":[{{"人物":"{ja}","場面":"式典・発表・インタビューなど","日付":"YYYY-MM-DD か YYYY-MM","装い":"着ているものを日本語で短く","ブランド":[{{"名前":"","もの":"ジャケット・時計など","関係":"着用/愛用/広告起用/提携/出資 など"}}],"出典URL":"","出典名":"媒体名","確かさ":"公式/報道/本人","備考":""}}]}}
"""


def norm(s):
    return G.norm(s)


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; ai-soukanzu-outfit)'})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=G._ctx()) as r:
            h = r.read(700000).decode('utf-8', 'ignore')
        return 'ok', norm(re.sub(r'<[^>]+>', ' ', h))
    except urllib.error.HTTPError as e:
        return f'HTTP {e.code}', ''
    except Exception as e:
        return 'open_ng:' + type(e).__name__, ''


def verify(item, ja, en):
    """合格・保留・除外と理由を返し、ブランドは本文に名前があるものだけ残す"""
    url = G.resolve_redirect(str(item.get('出典URL') or ''))
    item['出典URL'] = url
    if not url.startswith('https://'):
        return '除外', '出典URLが無い', item
    st, text = fetch(url)
    if st != 'ok':
        return ('除外', f'ページが無い({st})', item) if st in ('HTTP 404', 'HTTP 410') else ('保留', f'ページを開けない({st})', item)
    if not any(norm(n) in text for n in (ja, en) if n and len(norm(n)) >= 3):
        return '除外', '本文に本人の名前が無い', item
    kept, dropped = [], []
    for b in item.get('ブランド') or []:
        nm = str((b or {}).get('名前') or '').strip()
        (kept if nm and norm(nm) in text else dropped).append(b)
    item['ブランド'] = kept
    if dropped:
        item['外したブランド(本文に名前なし)'] = [d.get('名前') for d in dropped]
    return '合格', 'ページが開け、名前を確認' + (f'。ブランド{len(dropped)}件は本文に無く外した' if dropped else ''), item


def research_person(ja, en, co, dry=False, log=print):
    body = {'contents': [{'role': 'user', 'parts': [{'text': prompt(ja, en, co)}]}], 'tools': [{'google_search': {}}]}
    resp = G.gen(body)
    items = G.parse_items(G.resp_text(resp))
    out = []
    for it in items[:5]:
        s, why, it = verify(it, ja, en)
        it.update(人物=ja, 英語名=en, 会社=co, 判定=s, 理由=why)
        out.append(it)
        log(f'  [{s}] {ja}: {str(it.get("装い"))[:30]} - {why}')
    if not items:
        log(f'  {ja}: 見つからなかった')
    return out, [e for e in items], resp


def save(rows, dry=False):
    if dry or not rows:
        return None
    os.makedirs(ODIR, exist_ok=True)
    d = G.jst_today().isoformat()
    p = os.path.join(ODIR, f'{d}.json')
    n = 2
    while os.path.exists(p):
        p = os.path.join(ODIR, f'{d}-{n}.json'); n += 1
    json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return p


def people():
    done = set(open(DONE, encoding='utf-8').read().split('\n')) if os.path.exists(DONE) else set()
    rows = [l.strip().split('|') for l in open(PEOPLE, encoding='utf-8') if l.strip() and not l.startswith('#')]
    return [r for r in rows if len(r) >= 3 and r[0] not in done]


def run_daily(n=1, dry=False):
    """毎朝のGemini調査の最後から呼ばれる。次の n 人を調べて保存し、合格分を outfit_auto.js にまとめる"""
    rows, finished = [], []
    for ja, en, co in people()[:n]:
        try:
            out, _, _ = research_person(ja, en, co)
        except G.QuotaExhausted as e:
            print('装いの調査: 上限のため止めた:', e); break
        rows += out; finished.append(ja)
    path = save(rows, dry)
    if finished and not dry:
        open(DONE, 'a', encoding='utf-8').write('\n'.join(finished) + '\n')
    if path:
        import subprocess
        subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'outfit_merge.py')], check=False)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    d = sp.add_parser('daily'); d.add_argument('--people', type=int, default=2); d.add_argument('--dry-run', action='store_true')
    p = sp.add_parser('person'); p.add_argument('ja'); p.add_argument('en'); p.add_argument('co'); p.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    targets = people()[:a.people] if a.cmd == 'daily' else [[a.ja, a.en, a.co]]
    rows, finished = [], []
    for ja, en, co in targets:
        try:
            out, _, _ = research_person(ja, en, co)
        except G.QuotaExhausted as e:
            print('止まりました(上限):', e); break
        rows += out; finished.append(ja)
    path = save(rows, a.dry_run)
    if a.cmd == 'daily' and finished and not a.dry_run:
        open(DONE, 'a', encoding='utf-8').write('\n'.join(finished) + '\n')
    print('保存:', path or '(なし)', f'/ 合格{sum(r["判定"]=="合格" for r in rows)}件 保留{sum(r["判定"]=="保留" for r in rows)}件 除外{sum(r["判定"]=="除外" for r in rows)}件')


if __name__ == '__main__':
    main()
