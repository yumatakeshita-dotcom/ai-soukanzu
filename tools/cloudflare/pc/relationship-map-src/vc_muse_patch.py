import re, json, io
p='vc_funds_curated.py'; s=open(p,encoding='utf-8').read()
# Thrive: 注記の数字の食い違いを直す
s=s.replace("「10億ドル超」「初期10億ドル、成長90億ドル」と確認","「100億ドル超(Exceeding $10 billion)」「初期10億ドル、成長90億ドル」と確認")
# Founders Fund: Form D(SEC原文)で金額確定
s=s.replace("SECのForm Dで、Founders Fund Growth IV, LPが2026年3月23日に提出されていることを確認(金額は未確認)。","SECのForm D(原文を確認)で、販売済み6,024,585,000ドル(GPの出資約束を含む)、投資家370、初回販売2026年3月6日。外部45億/内部15億ドルの内訳は報道のみで、公的資料では未確認。")
s=re.sub(r"(fund='Growth IV', size='60億ドル'.*?)conf='中'\)", r"\1conf='高')", s, count=1, flags=re.S)
# Bessemer: 本人発表で確認
s=s.replace("url='https://techcrunch.com/2026/09/23/vc-firm-bessemer-now-has-another-5-75b-to-invest-in-what-else-ai/', conf='中'","url='https://www.bvp.com/news/5-75-billion-to-back-the-founders-building-what-s-next', conf='高'")
s=s.replace("2026年9月23日に発表(法律事務所Kirklandの発表でも、57.5億ドルを確認)。","2026年9月23日の同社発表で、57.5億ドル(初期17.5億・成長40億、単一クローズ)を確認。ファンド名は発表に記載なし。")
s=s.replace("ほかは非公開。', note='2026年9月23日の同社発表","SJCERAがXIIIへ3,000万ドル、Century Fund IIIへ2,000万ドルを2026年6月に可決(同機関の議事資料、Muse調査・原典未確認)。ほかは非公開。', note='2026年9月23日の同社発表")
new=[
('Felicis','Felicis Fund X','9億ドル',900,'2025年6月10日','組成完了','非公開(LPは「組織の種類」のみ公表)','同社最大のファンド。前の第9号は8億2,500万ドル(2023年)。','https://www.felicis.com/blog/fund-x','高'),
('Accel','後期側(Leaders Fund V＋サイドカー)','50億ドル',5000,'2026年4月14日','組成完了','非公開','同社の公式発表で合計50億ドルを確認。内訳は記載なし。','https://www.accel.com/news/ourlatestfundearlyinsightandenduringpartnership','高'),
('Accel','早期側(4本立て)','35億ドル',3500,'2026年8月11日','組成完了','非公開','米国・欧州・イスラエル・インドの初期投資を支える4本。個別金額は発表になし。','https://www.accel.com/news/our-enduring-commitment-to-investing-at-the-earliest-stages','高'),
('Index Ventures','Index Ventures XII＋Growth VII','23億ドル',2300,'2024年7月10日','組成完了','非公開','ベンチャー8億ドル、成長15億ドル。','https://www.indexventures.com/perspectives/relationships-that-reshape-industries-index-launches-23bn-in-new-funds/','高'),
('Lux Capital','Lux Ventures IX','15億ドル',1500,'2026年1月7日','組成完了','非公開','同社の発表で15億ドル。運用総額70億ドル。(Muse調査: 産業革新投資機構JICが5,000万ドルを出資、JIC公式一覧が出典・未確認)','https://www.luxcapital.com/news/announcing-lux-ventures-ix','高'),
('Union Square Ventures','中心ファンド＋機会ファンド(2026年)','9億ドル',900,'2026年10月8日','組成完了','非公開','同社の発表で9億ドル。前回の中心ファンドは2.75億ドル。内訳は発表になし。','https://www.usv.com/writing/the-next-chapter-of-usv','高'),
('Menlo Ventures','Menlo Ventures XVII＋Menlo Inflection IV','30億ドル',3000,'2026年6月23日','組成完了','非公開','同社の発表で約30億ドル(同社最大)。XVIIはシード〜A、Inflection IVはB以降。個別金額は未公表。','https://menlovc.com/perspective/menlo-turns-50-and-announces-3b-in-fresh-capital-to-go-all-in-on-ai/','高'),
('Peak XV Partners','India Seed・India Venture・APACの3本','13億ドル',1300,'2026年2月20日','組成完了','非公開','同社の発表で新たに合計13億ドルの出資約束。個別金額は未記載。','https://www.peakxv.com/announcement/three-new-funds-for-exceptional-founders-in-india-apac-and-beyond','高'),
('Initialized Capital','Fund VI(中心＋機会)','7億ドル',700,'2021年12月14日','組成完了','非公開(機関・大学基金・財団という種類のみ)','中心5.3億・機会1.7億ドル。運用総額32億ドル超。','https://blog.initialized.com/2021/12/announcing-initialized-fund-vi/','高'),
]
add=''.join(" dict(mgr=%r, fund=%r, size=%r, usd_m=%r, when=%r, status=%r, lp=%r, note=%r, url=%r, conf=%r),\n"%n for n in new)
i=s.index('\n]\n',s.index('ROWS = ['))
s=s[:i+1]+add+s[i+1:]
open(p,'w',encoding='utf-8').write(s)
# WSIB Feeder 行: 原典で確認できないため外す(退避)
w=json.load(open('wsib_vc.json',encoding='utf-8'))
bad=[r for r in w if 'Group XIII - Feeder' in r['fund']]
json.dump(bad,open('wsib_vc_held.json','w',encoding='utf-8'),ensure_ascii=False)
json.dump([r for r in w if r not in bad],open('wsib_vc.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(bad))
