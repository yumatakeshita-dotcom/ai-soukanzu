"""法的ページ(ひな形)を site/legal/ に作り、各ページのフッターにリンクを入れる。
使い方: python3 scripts/legal.py          … 書き込む(何度動かしても同じ結果。印の間だけ置き換える)
        python3 scripts/legal.py --check  … 状態を表示(書き込まない)
設定は scripts/legal_config.json。
  show_footer_links=false(初期値)のあいだは、フッターのリンクは入らない(入っていたら消す)。
  ページ自体は「ひな形・未確認」の帯つき・noindex で作る。公開リンクにするのは専門家の確認のあと。
フッターは各ページの最後の印(LEGAL:START〜LEGAL:END)の間だけ。毎朝の更新で index.html の中身が変わっても、
印は触られない。消えたら、このスクリプトをもう一度動かせば戻る。
"""
import json, os, re, sys, glob
from html import escape
D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(D, '..', 'site')
CFG = json.load(open(os.path.join(D, 'legal_config.json'), encoding='utf-8'))
F = CFG['fields']
S, E = '<!--LEGAL:START-->', '<!--LEGAL:END-->'
BLOCK_RE = re.compile(r'\n?' + re.escape(S) + r'.*?' + re.escape(E), re.S)

PAGES = [('terms', '利用規約'), ('privacy', 'プライバシーポリシー'), ('tokushoho', '特定商取引法に基づく表記'), ('contact', 'お問い合わせ・訂正/削除の受付')]

def v(key, hint=None):
    """設定にあれば値、なければ【要記入】の印"""
    x = (F.get(key) or '').strip()
    if x: return escape(x)
    return '<mark class="todo">【要記入: %s】</mark>' % escape(hint or key)

CSS = """:root{--bg:#f2f4f6;--surface:#fff;--fg:#161b22;--muted:#5d6875;--line:#d5dbe1;--active:#0d8a79;--conflict:#c93b3b;--warn-bg:#fff4d6;--warn-fg:#6b4a00;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--active:#2fc2ab;--conflict:#f07272;--warn-bg:#3a2f10;--warn-fg:#f0d98a;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#11151a;--surface:#1a2027;--fg:#e8ecf0;--muted:#97a3b0;--line:#2e3741;--active:#2fc2ab;--conflict:#f07272;--warn-bg:#3a2f10;--warn-fg:#f0d98a;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.8 "Noto Sans JP",system-ui,-apple-system,"Hiragino Sans","Yu Gothic",sans-serif}
main{max-width:760px;margin:0 auto;padding:16px max(16px,env(safe-area-inset-right)) 56px max(16px,env(safe-area-inset-left))}
h1{font-size:22px;margin:12px 0 4px} h2{font-size:17px;margin:28px 0 6px;padding-left:10px;border-left:4px solid var(--active)}
p,li{overflow-wrap:anywhere} a{color:var(--active)} .muted{color:var(--muted);font-size:13px}
.draft{background:var(--warn-bg);color:var(--warn-fg);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:8px 0 16px;font-size:14px}
mark.todo{background:var(--warn-bg);color:var(--warn-fg);padding:0 4px;border-radius:4px}
table{border-collapse:collapse;width:100%;background:var(--surface)} th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top;overflow-wrap:anywhere} th{width:11em;background:var(--bg)}
nav.l{display:flex;flex-wrap:wrap;gap:6px 16px;margin:20px 0 0;font-size:13px}"""

def head(title):
    return ('<!doctype html>\n<html lang="ja"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<meta name="robots" content="noindex">\n<title>%s | %s</title>\n<style>\n%s\n</style></head><body><main>\n'
      '<p class="muted"><a href="../index.html">← 相関図に戻る</a></p>\n') % (escape(title), escape(F['service_name']), CSS)

def draft_banner():
    return ('<div class="draft" role="note"><b>【ひな形・未確認】</b> これは公開前の下書きです。法的な確認(弁護士など専門家)はまだ受けていません。'
            '黄色の【要記入】の部分は、運営者が決めて書き入れます。確認が済むまで、この内容を正式な規約として扱わないでください。</div>\n')

def nav(cur):
    return '<nav class="l">' + ''.join('<a href="%s.html"%s>%s</a>' % (k, ' aria-current="page"' if k == cur else '', t) for k, t in PAGES) + '</nav>\n</main></body></html>\n'

def page(key, title, body):
    stamp = F.get('site_url') and ''  # 予約
    upd = CFG.get('last_updated') or '【要記入: 制定日・最終更新日】'
    return head(title) + '<h1>%s</h1>\n<p class="muted">制定日・最終更新日: %s</p>\n' % (escape(title), escape(upd) if CFG.get('last_updated') else '<mark class="todo">%s</mark>' % escape(upd)) + draft_banner() + body + nav(key)

def terms():
    sn = escape(F['service_name'])
    return f"""<p>この利用規約(以下「本規約」)は、{v('operator_name','運営者の名前(個人・会社名)')}(以下「運営者」)が提供する「{sn}」(以下「本サービス」)の利用条件を定めるものです。本サービスを使った方は、本規約に同意したものとみなします。</p>
<h2>第1条(本サービスの内容)</h2>
<p>本サービスは、AI企業・半導体企業などの人・出資・取引・移籍のつながりを、公開されている情報をもとに整理して見せるウェブサイトです。</p>
<h2>第2条(情報の性質・免責)</h2>
<ul>
<li>掲載する情報は、公式発表・開示書類・報道・本人の発言など、公開情報をもとにしています。各情報には出典と「確かさ」の印を付けますが、正確さ・最新性・完全性は保証しません。</li>
<li>金額は報道ベースや契約の上限を含みます。人物・会社の関係が、実際の現在の状況と違うことがあります。</li>
<li>本サービスの内容は、投資・法務・採用・取引などの助言ではありません。判断は、利用者ご自身が出典で確かめたうえで行ってください。</li>
<li>本サービスの利用で生じた損害について、運営者に故意または重大な過失がある場合を除き、責任を負いません。<mark class="todo">【要記入・専門家確認: 責任の範囲の書き方】</mark></li>
</ul>
<h2>第3条(禁止事項)</h2>
<ul>
<li>法令または公序良俗に反する行為</li>
<li>本サービスの運営を妨げる行為(過度なアクセス、不正アクセスなど)</li>
<li>アクセスキーの第三者への譲渡・共有・転売</li>
<li>本サービスに載る人物の情報を、その人への嫌がらせ・つきまとい・差別などに使うこと</li>
<li>運営者や第三者の権利を侵害する行為</li>
</ul>
<h2>第4条(権利・出典・写真)</h2>
<ul>
<li>本サービスのデザイン・文章・整理したデータの権利は運営者に属します。ただし、出典となる記事・書類・写真などの権利は、それぞれの権利者に属します。</li>
<li>顔写真は、ライセンスを確かめられたもの(主に Wikimedia Commons の自由に使える写真)だけを使い、作者とライセンスを「写真のクレジット」に示します。</li>
<li>本サービスの内容を資料として引用するときは、出典を明記してください。<mark class="todo">【要記入: 転載・営業資料への利用の条件(有料の機能の範囲を含む)】</mark></li>
</ul>
<h2>第5条(有料機能)</h2>
<p>有料の機能(プロ会員)を設ける場合、料金・支払い・解約などの条件は「特定商取引法に基づく表記」と料金ページに定めます。アクセスキーは本人だけが使い、第三者に渡してはいけません。<mark class="todo">【要記入: 有料機能を始める日、始めない場合はこの条を削除】</mark></p>
<h2>第6条(訂正・削除の申し出)</h2>
<p>掲載内容に誤りがある場合や、人物・会社の情報の訂正・削除を希望する場合は、「お問い合わせ・訂正/削除の受付」からお知らせください。確認のうえ、必要な訂正や削除を行います。</p>
<h2>第7条(サービスの変更・中断・終了)</h2>
<p>運営者は、事前の通知なく、本サービスの内容を変更・中断・終了することがあります。</p>
<h2>第8条(規約の変更)</h2>
<p>運営者は、必要に応じて本規約を変更できます。変更後の規約は、本サービス上に掲示した時から効力を持ちます。</p>
<h2>第9条(準拠法・裁判所)</h2>
<p>本規約は日本法に従います。争いが生じたときは、{v('jurisdiction','管轄の裁判所(例: ○○地方裁判所を第一審の専属的合意管轄とする)')}を管轄裁判所とします。</p>"""

def privacy():
    sn = escape(F['service_name'])
    return f"""<p>{v('operator_name','運営者の名前')}(以下「運営者」)は、「{sn}」(以下「本サービス」)での個人に関する情報の扱いを、次のとおり定めます。</p>
<p class="muted">この文書は、いま本サービスが実際にしていること(確かめた分)と、これから始める予定のこと(予定)を分けて書いてあります。公開前に、実際の動きと合っているか見直してください。</p>
<h2>1. 取得する情報</h2>
<ul>
<li><b>(いま)閲覧するだけの場合:</b> 本サービスは、閲覧者の名前・メールアドレスなどの入力を求めません。</li>
<li><b>(予定)先行案内・お問い合わせ:</b> 先行案内の登録やお問い合わせの際に、メールアドレスなど、ご自身で入力された情報を取得します。<mark class="todo">【要記入: 実際に取得する項目】</mark></li>
<li><b>(予定)有料機能:</b> 決済は Stripe, Inc.(決済代行)が行います。カード番号などの決済情報は Stripe が扱い、運営者のサーバーには保存しません。運営者は、決済の有無・メールアドレスなど、会員の確認に必要な情報を受け取ります。<mark class="todo">【要記入: Stripeから受け取る情報の範囲(Payment Linkの設定に合わせる)】</mark></li>
<li><b>(予定)アクセスキー:</b> 会員にはアクセスキー(合言葉)を発行します。運営者の側ではキーそのものではなく、確認用の変換値(ハッシュ)を保存する設計です。キーを紛失・漏えいしたときは、お問い合わせください。</li>
</ul>
<h2>2. 利用目的</h2>
<ul><li>本サービスの提供・改善、不具合の調査</li><li>お問い合わせへの対応、訂正・削除の対応</li><li>(予定)有料機能の提供、請求・会員確認、重要なお知らせの連絡</li><li>(予定)アクセス状況の把握(統計。個人を特定しない形)</li></ul>
<h2>3. 外部への送信・外部サービス</h2>
<ul>
<li><b>(いま)Google Fonts:</b> 文字の書体を表示するため、閲覧者のブラウザが Google Fonts(Google LLC)に接続します。このとき、閲覧者のIPアドレスなどが Google に送られます。</li>
<li><b>(いま)ニュース等のリンク:</b> 出典や記事へのリンクを押すと、リンク先のサイトに移ります。リンク先での情報の扱いは、各サイトの方針によります。</li>
<li><b>(予定)Cloudflare:</b> 本サービスは Cloudflare, Inc. のサービス(Workers・D1 など)で配信・運用します。配信の過程でアクセス記録(IPアドレス等)が扱われます。</li>
<li><b>(予定)Stripe:</b> 有料機能を始める場合、決済のため Stripe に接続します。</li>
<li><b>(予定)アクセス計測:</b> {v('analytics_tool','使うアクセス解析のサービス名、使わない場合は「使いません」。使う場合は、送られる情報と、拒否(オプトアウト)の方法を書く')}</li>
<li>上のほか、運営者が閲覧者の情報を第三者に売ることはありません。<mark class="todo">【要記入・専門家確認: 外部送信規律(電気通信事業法)の対象になるか、公表が必要な項目】</mark></li>
</ul>
<h2>4. Cookie・ブラウザの保存領域</h2>
<ul>
<li><b>(いま)</b> 本サービスは、広告用や追跡用の Cookie を使っていません。画面の表示設定(確かさの表示の切り替えなど)を覚えるため、閲覧者のブラウザ内の保存領域(localStorage)を使うことがあります。この情報は閲覧者のブラウザの中だけに残り、運営者には送られません。ブラウザの設定で消せます。</li>
<li><b>(予定)</b> アクセスキーの確認のために、キーをブラウザ内に保存することがあります。アクセス計測を始める場合は、そこで使う Cookie などをここに書き足します。</li>
</ul>
<h2>5. 掲載する人物情報の出典と顔写真</h2>
<ul>
<li>本サービスに載る人物の経歴・移籍・役職などは、公式発表、開示書類(SEC・EDINET など)、報道、本人の公開投稿といった<b>すでに公開されている情報</b>をもとにしています。各情報には出典のURLと「確かさ」の印を付けます。非公開の情報や、うわさは載せません。</li>
<li>顔写真は、ライセンスを確かめられたもの(主に Wikimedia Commons の自由に使える写真)だけを使い、作者とライセンスを「写真のクレジット」に示します。通信社など権利表記のある写真は使いません。</li>
<li>人物の公開情報の掲載について、訂正・削除を希望する方は、「お問い合わせ・訂正/削除の受付」から申し出られます。本人であること、または正当な理由を確かめたうえで、訂正・削除などの対応をします。</li>
</ul>
<h2>6. 第三者への提供</h2>
<p>法令に基づく場合などを除き、あらかじめ本人の同意を得ずに、個人情報を第三者に提供しません。ただし、利用目的の達成に必要な範囲で、上の外部サービス(Cloudflare・Stripe など)に取り扱いを任せることがあります。</p>
<h2>7. 開示・訂正・利用停止などの請求</h2>
<p>運営者が保有する個人情報について、開示・訂正・削除・利用停止を求めることができます。「お問い合わせ・訂正/削除の受付」からご連絡ください。</p>
<h2>8. 安全管理・保存期間</h2>
<p>個人情報は、漏えい・滅失を防ぐよう適切に管理します。<mark class="todo">【要記入: 保存期間(例: 先行案内のメールは配信を止めるまで)】</mark></p>
<h2>9. 事業者情報・窓口</h2>
<p>運営者: {v('operator_name','運営者の名前')}<br>窓口: {v('contact_email','連絡先メールアドレス')}</p>
<h2>10. 改定</h2>
<p>この方針は、必要に応じて改定し、本サービス上に掲示します。</p>"""

def tokushoho():
    return f"""<p class="muted">有料の機能を始める場合に必要な表記です。始めるまでは公開しないでください(フッターのリンクも出しません)。個人で運営する場合の住所・電話番号の扱い(請求があったら遅滞なく開示する運用が認められる場合があります)は、専門家に確認してください。</p>
<table>
<tr><th>販売事業者</th><td>{v('operator_name','個人の氏名または会社名')}</td></tr>
<tr><th>運営責任者</th><td>{v('representative','運営責任者の氏名')}</td></tr>
<tr><th>所在地</th><td>{v('address','住所。請求があれば遅滞なく開示する運用にする場合はその旨')}</td></tr>
<tr><th>電話番号</th><td>{v('phone','電話番号。請求があれば遅滞なく開示する運用にする場合はその旨')}</td></tr>
<tr><th>メールアドレス</th><td>{v('contact_email','連絡先メールアドレス')}</td></tr>
<tr><th>受付時間</th><td>{v('contact_hours','例: 平日10:00〜18:00(メールは24時間受付)')}</td></tr>
<tr><th>販売URL</th><td>{v('site_url','サイトのURL')}</td></tr>
<tr><th>販売価格</th><td>{v('price_text','料金(税込)。例: 個人 月額○円 / 法人 月額○円。料金ページの金額と合わせる')}</td></tr>
<tr><th>商品代金以外の必要料金</th><td>インターネット接続にかかる通信料は、お客様のご負担です。<mark class="todo">【要記入: そのほかの料金があれば】</mark></td></tr>
<tr><th>支払い方法</th><td>{v('payment_methods','例: クレジットカード(Stripe)。法人の請求書払いを受けるなら、その方法')}</td></tr>
<tr><th>支払い時期</th><td>{v('payment_timing','例: 申し込み時に初回、以降は毎月の更新日')}</td></tr>
<tr><th>引き渡し時期</th><td>{v('delivery_timing','例: お支払い確認後、アクセスキーをメールでお送りします(○営業日以内)')}</td></tr>
<tr><th>解約・キャンセル</th><td>{v('cancel_policy','解約の方法と、いつまでに手続きすれば次回の請求を止められるか')}</td></tr>
<tr><th>返金・返品</th><td>{v('refund_policy','デジタルな商品の性質上、提供後の返金に応じるか。応じる場合の条件')}</td></tr>
<tr><th>動作環境</th><td>最新のウェブブラウザ(スマートフォン・パソコン)。<mark class="todo">【要記入: 必要なら】</mark></td></tr>
</table>"""

def contact():
    return f"""<p>掲載内容の誤りの指摘、人物・会社の情報の訂正・削除の申し出、そのほかのお問い合わせは、下の窓口で受け付けます。</p>
<h2>窓口</h2>
<table>
<tr><th>運営者</th><td>{v('operator_name','運営者の名前')}</td></tr>
<tr><th>メール</th><td>{v('contact_email','連絡先メールアドレス(個人のアドレスを推測で書かない。専用のアドレスの用意をおすすめ)')}</td></tr>
<tr><th>受付時間・返信の目安</th><td>{v('contact_hours','例: 通常○営業日以内に返信')}</td></tr>
</table>
<h2>訂正・削除を申し出るとき</h2>
<p>次の内容を書いて、上のメールアドレスに送ってください。</p>
<ol>
<li>対象のページと、該当する会社名・人物名・線(つながり)(URLがあれば貼る)</li>
<li>何が誤りか、どう直してほしいか(または削除してほしいか)</li>
<li>根拠となる出典(公式発表・開示書類・本人の公開投稿などのURL)</li>
<li>申し出る方の立場(ご本人、会社の関係者、そのほか)と返信先</li>
</ol>
<p>確認のうえ、誤りが確かめられたものは訂正します。顔写真や人物情報の削除の申し出は、できるだけ早く確認します。<mark class="todo">【要記入: 対応の目安の日数】</mark> 返信のため、いただいた連絡先は、この件の対応のためだけに使います。</p>
<h2>顔写真の権利について</h2>
<p>写真の権利者の方で、掲載の取りやめを希望される場合も、上の窓口に写真が載っている人物名を添えてご連絡ください。</p>"""

BODIES = {'terms': terms, 'privacy': privacy, 'tokushoho': tokushoho, 'contact': contact}

def footer_block(depth):
    pre = '../' * depth
    links = ' · '.join('<a href="%slegal/%s.html" style="color:inherit">%s</a>' % (pre, k, t) for k, t in PAGES if k != 'tokushoho' or CFG.get('show_tokushoho', True))
    return (S + '\n<div class="legal-foot" style="max-width:1120px;margin:24px auto 0;padding:12px 16px 20px;font-size:12.5px;line-height:1.8;'
            'color:var(--muted,#5d6875);border-top:1px solid var(--line,#d5dbe1);text-align:center">' + links + '</div>\n' + E)

def target_pages():
    out = []
    for p in glob.glob(os.path.join(SITE, '**', '*.html'), recursive=True):
        rel = os.path.relpath(p, SITE).replace(os.sep, '/')
        if rel.startswith('legal/') or rel.startswith('pro/') or rel.startswith('aw/') or rel.startswith('data/'): continue
        out.append((p, rel))
    return sorted(out)

def apply(path, rel, on):
    s = open(path, encoding='utf-8').read()
    s2 = BLOCK_RE.sub('', s)  # 古い印を消してから
    if on:
        blk = footer_block(rel.count('/'))
        i = s2.rfind('</body>')
        s2 = s2[:i] + '\n' + blk + s2[i:] if i >= 0 else s2 + '\n' + blk   # 週のまとめは <body> のない断片 → 末尾に足す
    if s2 != s: open(path, 'w', encoding='utf-8').write(s2)
    return s2 != s

def main(check=False):
    on = bool(CFG.get('show_footer_links'))
    if check:
        print('フッターのリンク:', 'ON(公開リンク)' if on else 'OFF(ひな形のまま)')
        miss = sum(1 for k, _ in PAGES if not os.path.exists(os.path.join(SITE, 'legal', k + '.html')))
        n = sum(1 for p, _ in target_pages() if S in open(p, encoding='utf-8').read())
        print('法的ページ', len(PAGES) - miss, '/', len(PAGES), ' フッター印のあるページ', n, '/', len(target_pages()))
        return 1 if (miss or (on and n < len(target_pages())) or (not on and n)) else 0
    os.makedirs(os.path.join(SITE, 'legal'), exist_ok=True)
    for k, t in PAGES:
        open(os.path.join(SITE, 'legal', k + '.html'), 'w', encoding='utf-8').write(page(k, t, BODIES[k]()))
    ch = sum(apply(p, rel, on) for p, rel in target_pages())
    print('書き出し: site/legal/ の', len(PAGES), 'ページ。フッターのリンク:', 'ON' if on else 'OFF', '/ 変更したページ', ch)
    return 0

if __name__ == '__main__':
    sys.exit(main('--check' in sys.argv))
