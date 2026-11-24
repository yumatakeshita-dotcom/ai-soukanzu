#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""調べる順番の一覧(宿題リスト)。2026/11/20追加。足すだけ・消さない。

inbox/queue.json に「テーマ・理由・状態(未/調査済/保留)・最終調査日」を持つ。
- build  … 相関図のデータから「薄いところ」を探して、新しい項目を足す(すでにある項目は触らない)
- next   … 次に調べる1件を表示する
- run-next … 次の1件を Gemini で調べ、出典を確かめ、状態を「調査済」にする(毎朝のGemini調査 daily から呼ばれる)
- mark   … 状態を手で変える(例: mark ID 保留 --note 理由)
- status … 件数と先頭の数件

「薄いところ」の見つけ方(外のサービスは使わない。リポジトリの中のデータだけ):
  1. 人の動き(inbox/moves と src/lab/flows.json)に出てくる回数が1回以下の会社
  2. 地域ごとの会社リスト(中国・韓国・欧州・日本。SEED)のうち、人の動きがまだ0〜1件のもの
  3. いつも先頭にある「固定の課題」(出典の無い移籍を補強する、など)
同じ会社は1項目だけ(id は種類+会社名)。調査済みの項目は、COOLDOWN_DAYS 日たつまで選ばない(同じ調査を繰り返さない)。
Gemini の無料枠が切れた(429)ときは、状態を変えずに終わる(次の朝に同じ項目を取る)。
"""
import argparse, datetime, glob, json, os, re, sys, unicodedata
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, 'inbox', 'queue.json')
STATES = ('未', '調査済', '保留')
COOLDOWN_DAYS = {'固定': 30, '会社': 120, '重要': 45, '薄い人物': 60}   # 調査済みの項目が、また選ばれるまでの日数
JST = datetime.timezone(datetime.timedelta(hours=9))


def today():
    return datetime.datetime.now(JST).date().isoformat()


def norm(s):
    s = unicodedata.normalize('NFKC', str(s or '')).lower()
    return re.sub(r'[\s・,、.()「」\-_/&]+', '', s)


# ---------- 地域ごとの会社リスト(「まだ薄いところ」調査と同じ範囲に、日本を足した) ----------
SEED = {
    '中国': ['DeepSeek', 'Moonshot AI', 'Zhipu AI', 'Baichuan', 'StepFun', '01.AI', 'ByteDance', 'Baidu', 'iFlytek',
             'SenseTime', 'Unitree', 'Cambricon', 'Horizon Robotics', 'Alibaba Qwen', 'Tencent Hunyuan', 'Huawei Ascend'],
    '韓国': ['Naver', 'Kakao', 'LG AI Research', 'Upstage', 'Rebellions', 'FuriosaAI', 'Samsung Electronics',
             'SK hynix', 'KT', 'SK Telecom'],
    '欧州': ['Mistral AI', 'Aleph Alpha', 'Black Forest Labs', 'Helsing', 'Synthesia', 'ElevenLabs', 'Poolside',
             'H Company', 'DeepL', 'Wayve', 'Nscale', 'Stability AI', 'Hugging Face', 'Graphcore', 'Kyutai',
             'Isomorphic Labs', 'ASML'],
    '日本': ['Sakana AI', 'Preferred Networks', 'PKSHA Technology', 'ELYZA', 'Stockmark', 'SoftBank', 'NTT', 'Rapidus'],
    '中東・インド': ['G42', 'Mubadala', 'Humain', 'Sarvam AI', 'Krutrim', 'Reliance Jio'],
}

# ---------- 固定の課題(2026/11/20の集計から。数字は集計した日のもの。毎回数え直しはしない) ----------
FIXED = [
    ('standing-unsourced-moves', 1,
     '出典の付いていない人の移籍を、公式発表・本人の投稿・SEC書類・大手報道で確かめて出典を足す対象を探す(OpenAI・Anthropic・Meta・xAI の幹部の入社・退社)',
     '出典なしの移籍が143件あるため(2026/11/20の集計)'),
    ('standing-unsourced-invest', 2,
     '出典の付いていない出資の線(大型の資金調達・評価額)について、公式発表・開示書類・大手報道で確かめられる直近1年の案件を探す(AI企業・半導体企業・AIスタートアップ)',
     '出資の線6,193本のうち6,131本に出典がないため(2026/11/20の集計)'),
    ('standing-moves-beyond-top5', 3,
     '上位5社(OpenAI・xAI・Anthropic・Meta・SK hynix)以外のAI企業・半導体企業の、経営陣・主要研究者の入社・退社・就任(直近3か月)',
     '人の動きが上位5社に偏っているため(2026/11/20の集計)'),
]


def load():
    if os.path.exists(QUEUE):
        return json.load(open(QUEUE, encoding='utf-8'))
    return {'version': 1, 'note': '調べる順番の一覧。scripts/research_queue.py が足す。項目は消さない(状態を変えるだけ)', 'items': []}


def save(q):
    os.makedirs(os.path.dirname(QUEUE), exist_ok=True)
    json.dump(q, open(QUEUE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(QUEUE, 'a', encoding='utf-8').write('\n')


# ---------- 人の動きの数え方 ----------
def move_counts():
    """会社名(正規化)ごとに、人の動きに出てきた回数。inbox/moves の from/to と、相関図の書き出し flows.json の a/b。"""
    c, name = {}, {}

    def add(n):
        n = re.sub(r'[((].*', '', str(n or '')).strip()
        if not n or n in ('未定', '(退任)') or n.startswith('('):
            return
        k = norm(n)
        c[k] = c.get(k, 0) + 1
        name.setdefault(k, n)
    for f in glob.glob(os.path.join(ROOT, 'inbox', 'moves', '*.json')):
        try:
            for it in json.load(open(f, encoding='utf-8')).get('items', []):
                add(it.get('from')); add(it.get('to'))
        except (json.JSONDecodeError, OSError, AttributeError):
            pass
    fp = os.path.join(ROOT, 'src', 'lab', 'flows.json')
    if os.path.exists(fp):
        for it in json.load(open(fp, encoding='utf-8')):
            add(it.get('a')); add(it.get('b'))
    return c, name


def company_item(name, region, n_moves):
    return {
        'id': 'company-' + norm(name), 'kind': '会社', 'company': name, 'region': region,
        'theme': f'{name}の経営陣・主要研究者の入社・退社・就任と、主な出資・提携(直近1年。公式発表・本人の投稿・SEC書類など出典のあるもの)',
        'reason': f'人の動きが相関図の調査データに{n_moves}件しかない({region}の会社)',
        'priority': 20 + (0 if n_moves == 0 else 5),
        'status': '未', 'last_researched': None, 'attempts': 0, 'history': [], 'added': today(),
    }


RANK_TOP = 25   # 重要度ランキング(scripts/importance_rank.py)の上位から、この数まで会社の項目を足す


def rank_items(have):
    """重要度ランキングの上位の会社・投資家を、優先して調べる項目として足す(すでにある id は触らない。足すだけ)"""
    p = os.path.join(ROOT, 'inbox', 'ranking', 'latest.json')
    if not os.path.exists(p):
        return []
    out = []
    xs = [r for r in json.load(open(p, encoding='utf-8')).get('top', []) if r['kind'] in ('会社', '投資家')][:RANK_TOP]
    for r in xs:
        id_ = 'company-' + norm(r['name'])
        if id_ in have:
            continue
        out.append({
            'id': id_, 'kind': '重要', 'company': r['name'], 'region': '世界',
            'theme': f"{r['name']}の経営陣・主要研究者の入社・退社・就任と、主な出資・提携(直近1年。公式発表・本人の投稿・SEC書類など出典のあるもの)",
            'reason': f"重要度ランキング{r['rank']}位(つながり{r['links']}・直近の動き{r['recent']}・ニュース{r['news']})。よく見られそうな会社を先に確かめる",
            'priority': 10, 'rank': r['rank'], 'status': '未', 'last_researched': None, 'attempts': 0, 'history': [], 'added': today(),
        })
    return out


THIN_TOP = 10   # 経歴の薄い有名人物(scripts/person_thin.py)の上位から、この数まで足す


def thin_items(have):
    """経歴が薄い有名人物の上位を、優先して調べる項目として足す(2026/11/24追加。足すだけ)。
    inbox/people_thin/latest.json の「上位」(知名度の高い順。skip.json の人は外れている)を使う。"""
    p = os.path.join(ROOT, 'inbox', 'people_thin', 'latest.json')
    if not os.path.exists(p):
        return []
    out = []
    for i, r in enumerate(json.load(open(p, encoding='utf-8')).get('top', [])[:THIN_TOP], 1):
        nm = r.get('en') or r['name']
        id_ = 'person-' + norm(nm)
        if id_ in have:
            continue
        out.append({
            'id': id_, 'kind': '薄い人物', 'company': nm, 'region': '世界',
            'theme': f"{nm}の経歴(前職・入社時期・役割・主な実績)を、本人のX・公式ブログ・SEC書類・報道の本文など、開ける出典で確かめる。いま相関図には「{r.get('role','')}」程度しかない",
            'reason': f"経歴の薄い有名人物の{i}位(知名度{r['fame']}。{'、'.join(r.get('why', []))})",
            'priority': 11, 'rank': i, 'status': '未', 'last_researched': None, 'attempts': 0, 'history': [], 'added': today(),
        })
    return out


def build(dry=False, log=print):
    q = load()
    have = {it['id'] for it in q['items']}
    added = []
    for id_, pri, theme, reason in FIXED:
        if id_ not in have:
            added.append({'id': id_, 'kind': '固定', 'theme': theme, 'reason': reason, 'priority': pri, 'status': '未',
                          'last_researched': None, 'attempts': 0, 'history': [], 'added': today()})
    # 0. 重要度ランキングの上位(優先度10。固定の課題の次、薄いところ探しの前)
    for r in rank_items(have | {a['id'] for a in added}):
        added.append(r)
    # 0b. 経歴の薄い有名人物の上位(優先度11。重要度ランキングの次)
    for r in thin_items(have | {a['id'] for a in added}):
        added.append(r)
    counts, names = move_counts()
    # 1. 地域ごとの会社リストで、人の動きが0〜1件のもの
    seeded = set()
    for region, cos in SEED.items():
        for co in cos:
            k = norm(co)
            seeded.add(k)
            n = counts.get(k, 0)
            if n <= 1 and 'company-' + k not in have:
                added.append(company_item(co, region, n))
    # 2. 調査データに1回だけ出てくる会社(リストに無いもの)
    for k, n in counts.items():
        if n == 1 and k not in seeded and 'company-' + k not in have and len(k) >= 2:
            added.append(company_item(names[k], '世界', 1))
    seen_ids = set()
    added = [a for a in added if not (a['id'] in seen_ids or seen_ids.add(a['id']))]
    log(f'人の動きに出てくる会社 {len(counts)}社(1回だけ: {sum(1 for v in counts.values() if v == 1)}社)。新しく足す項目: {len(added)}件')
    if not dry:
        q['items'] += added
        q['built'] = today()
        save(q)
        log(f'保存: {os.path.relpath(QUEUE, ROOT)}(合計 {len(q["items"])}件)')
    else:
        for a in added[:15]:
            log(f'  [{a["priority"]}] {a["id"]}: {a["theme"][:50]}…')
    return added


# ---------- 次の1件 ----------
def eligible(it, now=None):
    now = datetime.date.fromisoformat(now or today())
    if it['status'] == '保留':
        return False
    if it['status'] == '未':
        return True
    last = it.get('last_researched')
    if not last:
        return True
    return (now - datetime.date.fromisoformat(last)).days >= COOLDOWN_DAYS.get(it['kind'], 120)


def pick(q):
    xs = [it for it in q['items'] if eligible(it)]
    # 未が先、そのあと優先度の小さい順、古く調べたものの順
    xs.sort(key=lambda it: (it['status'] != '未', it['priority'], it.get('rank', 999), it.get('last_researched') or '', it['id']))
    return xs[0] if xs else None


def mark(qid, status, file='', note='', count=None):
    q = load()
    for it in q['items']:
        if it['id'] == qid:
            it['status'] = status
            if status == '調査済':
                it['last_researched'] = today()
                it['attempts'] = it.get('attempts', 0) + 1
            it['history'].append({'date': today(), 'result': status, 'file': file, 'note': note, 'items': count})
            save(q)
            return True
    return False


def run_next(dry=False, log=print):
    q = load()
    if not q['items']:
        log('一覧が空です。先に build を実行します'); build(False, log); q = load()
    it = pick(q)
    if not it:
        log('いま調べる項目はありません(すべて調査済みで、まだ間が空いていません)'); return None
    log(f'今日の宿題: [{it["id"]}] {it["theme"]}')
    log(f'  理由: {it["reason"]}')
    if dry:
        log('  (ドライラン: 調べません)'); return it
    import gemini_research as gr
    if not gr.key():
        log('GEMINI_API_KEY が無いので調べません(状態は変えません)'); return it
    try:
        res = gr.research(it['theme'], 10, True, False, log, True, queue_on_quota=False)
    except gr.QuotaExhausted:
        log('今日は無料枠の上限です。状態は変えずに、次の朝に同じ項目を取ります'); return it
    except Exception as e:  # 混雑・通信など。状態は変えず記録だけ残す
        log(f'調べられませんでした: {str(e)[:150]}(状態は変えません)')
        q = load()
        for x in q['items']:
            if x['id'] == it['id']:
                x['history'].append({'date': today(), 'result': '失敗', 'file': '', 'note': str(e)[:150], 'items': None})
        save(q); return it
    saved = res.get('saved', '')
    n = len(res.get('items', []))
    if saved:
        try:
            import gemini_verify
            gemini_verify.run([os.path.join(ROOT, saved[:-3] + '.json')])
        except Exception as e:
            log(f'確かめでエラー: {str(e)[:150]}(調べた結果は保存済み。確かめは次の回に)')
    mark(it['id'], '調査済', saved, f'Geminiの候補{n}件', n)
    log(f'調査済みにしました({n}件。{saved})')
    return it


def status(log=print):
    q = load()
    c = {s: sum(1 for it in q['items'] if it['status'] == s) for s in STATES}
    log(f'合計 {len(q["items"])}件 / 未 {c["未"]} / 調査済 {c["調査済"]} / 保留 {c["保留"]}')
    xs = sorted([it for it in q['items'] if eligible(it)], key=lambda it: (it['status'] != '未', it['priority'], it.get('rank', 999), it['id']))
    for it in xs[:8]:
        log(f'  次の候補 [{it["priority"]}] {it["id"]} … {it["theme"][:60]}')
    return c


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest='cmd', required=True)
    b = sp.add_parser('build'); b.add_argument('--dry-run', action='store_true')
    sp.add_parser('next')
    r = sp.add_parser('run-next'); r.add_argument('--dry-run', action='store_true')
    m = sp.add_parser('mark'); m.add_argument('id'); m.add_argument('status', choices=STATES); m.add_argument('--note', default='')
    sp.add_parser('status')
    a = ap.parse_args()
    if a.cmd == 'build':
        build(a.dry_run)
    elif a.cmd == 'next':
        it = pick(load()); print(json.dumps(it, ensure_ascii=False, indent=1) if it else '調べる項目はありません')
    elif a.cmd == 'run-next':
        run_next(a.dry_run)
    elif a.cmd == 'mark':
        print('更新しました' if mark(a.id, a.status, note=a.note) else 'その id はありません')
    else:
        status()


if __name__ == '__main__':
    main()
