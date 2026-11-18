// 幹部の入れ替わり年表(メニュー「幹部の年表」)。2026年11月19日に追加。
// データ(EXECTL)と画面(showExecTl)がこのファイルに入っている。会社を足すときは EXECTL に同じ形で足す。
// 1件 = {d:'日付(YYYY-MM-DD か YYYY-MM)', t:'in'入社 / 'out'退社 / 'role'役割の変更 / 'co'会社の出来事, p:'人の名前', en:'英語名', role:'役職', from/to:'どこから・どこへ', note:'ひとこと', cf:'o'公式 / 'f'開示 / 's'本人 / 'r'報道 / 'e'推定, src:[[出典名,URL],...]}
// 守ること: 出典のURLを必ず付ける。うわさは入れない。報道だけのものは cf:'r'。既存の行は消さず、直すときは note に「(○年○月○日に直した)」と書き添える。
const EXECTL={
openai:{
 name:'OpenAI',
 ipo:{d:'2026-06-08',label:'上場の準備書類(S-1)を米SECに非公開で提出'},
 asof:'2026-11-19',
 note:'OpenAIの経営陣・幹部の入社・退社・役割の変更を、2023年11月の解任騒動から並べました。公式=OpenAIの発表、本人=本人の投稿・寄稿、報道=報道だけで確かめたもの。報道だけのものは日付が数日ずれることがあります。研究者は、幹部級か、話題になった人だけを入れています。',
 now:[
  ['CEO','サム・アルトマン','共同創業者'],
  ['社長','グレッグ・ブロックマン','共同創業者。2026年は計算資源・売上・渉外の責任者が直属になったと報道'],
  ['CFO','サラ・フライアー','2024年6月から。上場準備を担当'],
  ['チーフサイエンティスト','ヤクブ・パチョツキ','2024年5月から'],
  ['研究の責任者(Chief Research Officer)','マーク・チェン','2025年3月から'],
  ['売上の責任者(CRO)','ダリ・ラジッチ','2026年8月、Wizから'],
  ['世界営業VP','ブライアン・マッカーシー','2026年9月、SpaceX(旧Cursor)から'],
  ['欧州・中東・アフリカ営業VP','イスマイル・エルマス','2026年10月、Cursorから(ミュンヘン)'],
  ['渉外の責任者','ジル・ヘイゼルベイカー','2026年12月着任予定、Uberから'],
  ['人事の責任者','アルビンド・KC','2026年2月、Robloxから'],
  ['計算資源インフラ','ウダイ・ルッダラジュ','2026年10月、カッティの後任'],
  ['研究・安全VP','メリア・グレイズ','2026年7月の再編で安全も統括']
 ],
 ev:[
  {d:'2023-11-17',t:'co',p:'サム・アルトマン',en:'Sam Altman',role:'CEO',note:'取締役会がアルトマンの解任を発表。CTOのミラ・ムラティが暫定CEOに。社長のブロックマンも辞任を表明',cf:'o',src:[['OpenAI公式(2023/11/17)','https://openai.com/index/openai-announces-leadership-transition/']]},
  {d:'2023-11-29',t:'co',p:'サム・アルトマン',en:'Sam Altman',role:'CEO',note:'アルトマンがCEOに、ムラティがCTOに戻る。新しい取締役会はブレット・テイラー(議長)、ラリー・サマーズ、アダム・ダンジェロ。解任に関わったトナー、マコーリーらは退任',cf:'o',src:[['OpenAI公式(2023/11/29)','https://openai.com/index/sam-altman-returns-as-ceo-openai-has-a-new-initial-board/']]},
  {d:'2024-03-08',t:'role',p:'サム・アルトマン',en:'Sam Altman',role:'取締役に復帰',note:'外部の法律事務所の調査が終わり、アルトマンが取締役に復帰。フィジー・シモら3人が新しい取締役に',cf:'o',src:[['OpenAI公式(2024/3/8)','https://openai.com/index/review-completed-altman-brockman-to-continue-to-lead-openai/']]},
  {d:'2024-05-14',t:'out',p:'イリヤ・スツケバー',en:'Ilya Sutskever',role:'共同創業者・チーフサイエンティスト',to:'Safe Superintelligence(のちに設立)',note:'退社。後任のチーフサイエンティストはヤクブ・パチョツキ',cf:'o',src:[['OpenAI公式(2024/5/14)','https://openai.com/index/jakub-pachocki-announced-as-chief-scientist/']]},
  {d:'2024-05-14',t:'role',p:'ヤクブ・パチョツキ',en:'Jakub Pachocki',role:'チーフサイエンティストに',note:'研究ディレクターから昇格',cf:'o',src:[['OpenAI公式(2024/5/14)','https://openai.com/index/jakub-pachocki-announced-as-chief-scientist/']]},
  {d:'2024-05-15',t:'out',p:'ヤン・ライケ',en:'Jan Leike',role:'安全チーム(スーパーアラインメント)の共同責任者',to:'Anthropic(5月28日に発表)',note:'「安全より製品が優先されてきた」と本人がXに書いて退社',cf:'s',src:[['本人のX(@janleike)','https://x.com/janleike'],['CIO(2024/5)','https://www.cio.com/article/2130038/ex-open-ai-researcher-jan-leike-joins-anthropic-amid-ai-safety-concerns.html']]},
  {d:'2024-06-10',t:'in',p:'サラ・フライアー',en:'Sarah Friar',role:'CFO(最高財務責任者)',from:'Nextdoor(CEO)',note:'初代CFO。のちに上場準備を担当',cf:'o',src:[['OpenAI公式(2024/6/10)','https://openai.com/index/openai-welcomes-cfo-cpo/']]},
  {d:'2024-06-10',t:'in',p:'ケビン・ワイル',en:'Kevin Weil',role:'CPO(最高製品責任者)',from:'Planet',note:'',cf:'o',src:[['OpenAI公式(2024/6/10)','https://openai.com/index/openai-welcomes-cfo-cpo/']]},
  {d:'2024-08-05',t:'out',p:'ジョン・シュルマン',en:'John Schulman',role:'共同創業者',to:'Anthropic(2025年2月にThinking Machines Labへ)',note:'同じ週に社長のブロックマンが年末までの休職を発表(11月に復帰)',cf:'r',src:[['TechCrunch(2024/8/5)','https://techcrunch.com/2024/08/05/openai-co-founder-leaves-for-anthropic'],['The Decoder','https://the-decoder.com/john-schulman-openai-co-founder-and-key-chatgpt-developer-leaves-for-anthropic/']]},
  {d:'2024-09-25',t:'out',p:'ミラ・ムラティ',en:'Mira Murati',role:'CTO',to:'Thinking Machines Lab(2025年に設立)',note:'同じ日に研究の責任者ボブ・マグルー、研究VPバレット・ゾフも退社',cf:'r',src:[['Axios(2024/9/25)','https://www.axios.com/2024/09/25/openai-mira-murati-leaving'],['The Register(2024/9/26)','https://www.theregister.com/2024/09/26/openai_execs_leave']]},
  {d:'2025-03-24',t:'role',p:'ブラッド・ライトキャップ / マーク・チェン',en:'Brad Lightcap / Mark Chen',role:'COOの役割を拡大 / 研究の責任者に',note:'アルトマンが研究と製品に集中するための体制変更。ライトキャップが事業と日々の運営、チェンが研究の責任者(Chief Research Officer)に',cf:'o',src:[['OpenAI公式(2025/3/24)','https://openai.com/index/leadership-updates-march-2025'],['Bloomberg(2025/3/24)','https://www.bloomberg.com/news/articles/2025-03-24/openai-expands-coo-s-role-as-altman-focuses-more-on-products']]},
  {d:'2025-05-08',t:'in',p:'フィジー・シモ',en:'Fidji Simo',role:'アプリケーション部門のCEO',from:'Instacart(CEO)',note:'8月に就任。のちに「AGIデプロイメント担当CEO」と呼ばれ、社内の2番手とみられた',cf:'r',src:[['Fortune(2025/5/8)','https://fortune.com/2025/05/08/openai-hires-instacart-ceo-fidji-simo-for-major-leadership-role/']]},
  {d:'2025-06',t:'out',p:'研究者の大量移籍',en:'',role:'推論モデルなどの研究者',to:'Meta(Superintelligence Labs)',note:'トラピット・バンサル、ジェイソン・ウェイ、ヒョンウォン・チョンらがMetaへ(6〜7月)',cf:'r',src:[['TechCrunch(2025/6/26)','https://techcrunch.com/2025/06/26/meta-hires-key-openai-researcher-to-work-on-ai-reasoning-models']]},
  {d:'2025-11',t:'in',p:'サチン・カッティ',en:'Sachin Katti',role:'計算資源インフラの責任者',from:'Intel(CTO)',note:'',cf:'r',src:[['TrendForce(2025/11/11)','https://www.trendforce.com/news/2025/11/11/news-intel-cto-and-ai-chief-departs-for-openai-ceo-lip-bu-tan-steps-in-to-lead-ai-push/']]},
  {d:'2025-12-09',t:'in',p:'デニス・ドレッサー',en:'Denise Dresser',role:'CRO(売上の責任者)',from:'Slack(CEO)',note:'初代CRO。企業向けの営業とカスタマーサクセスを統括',cf:'r',src:[['Bloomberg Law(2025/12/9)','https://news.bloomberglaw.com/tech-and-telecom-law/openai-hires-slack-ceo-denise-dresser-as-chief-revenue-officer']]},
  {d:'2025-12-15',t:'in',p:'アルバート・リー',en:'Albert Lee',role:'企業開発(M&A)担当VP',from:'Google',note:'Googleに約15年在籍',cf:'r',src:[['Yahoo Finance(Reuters、2025/12/15)','https://finance.yahoo.com/news/openai-hires-veteran-google-executive-184017915.html']]},
  {d:'2026-01-14',t:'in',p:'バレット・ゾフ',en:'Barret Zoph',role:'研究の幹部(シモの直属)',from:'Thinking Machines Lab(CTO)',note:'ルーク・メッツ、サム・ショーンホルツとともに復帰。シモがXで発表',cf:'r',src:[['TechCrunch(2026/1/14)','https://techcrunch.com/2026/01/14/mira-muratis-startup-thinking-machines-lab-is-losing-two-of-its-co-founders-to-openai']]},
  {d:'2026-02-24',t:'in',p:'アルビンド・KC',en:'Arvind KC',role:'人事の責任者(Chief People Officer)',from:'Roblox',note:'',cf:'r',src:[['Bloomberg(2026/2/24)','https://www.bloomberg.com/news/articles/2026-02-24/openai-hires-former-roblox-executive-as-chief-people-officer']]},
  {d:'2026-03-05',t:'out',p:'マックス・シュワルツァー',en:'Max Schwarzer',role:'研究VP',to:'Anthropic',note:'',cf:'r',src:[['Storyboard18(2026/3/5)','https://www.storyboard18.com/trending/openai-vp-joins-anthropic-says-people-he-trusts-most-and-respects-moved-there-91303.htm']]},
  {d:'2026-03-07',t:'out',p:'ケイトリン・カリノウスキ',en:'Caitlin Kalinowski',role:'ロボティクス・ハードウェアの責任者',to:'(未発表)',note:'米国防総省との契約に反対して辞任と本人が表明',cf:'r',src:[['NPR(2026/3/8)','https://www.npr.org/2026/03/08/nx-s1-5741779/openai-resigns-ai-pentagon-guardrails-military'],['Fortune(2026/3/7)','https://fortune.com/2026/03/07/openai-robotics-leader-caitlin-kalinowski-resignation-pentagon-surveillance-autonomous-weapons-anthropic/']]},
  {d:'2026-04-11',t:'out',p:'ピーター・ホシェレほか2人',en:'Peter Hoeschele',role:'Stargate(計算資源)部門の幹部',to:'Meta(参画予定と報道)',note:'シェイメズ・ヘマニ、アヌジ・サハランも',cf:'r',src:[['Bloomberg Law(2026/4/11)','https://news.bloomberglaw.com/california-brief/former-openai-stargate-leaders-plan-to-join-meta-platforms']]},
  {d:'2026-04-17',t:'out',p:'ケビン・ワイル',en:'Kevin Weil',role:'OpenAI for Science の責任者(元CPO)',to:'(自分の会社)',note:'同じ日にSoraの責任者ビル・ピーブルズも退社。「本業以外」を減らす流れと報道',cf:'r',src:[['TechCrunch(2026/4/17)','https://techcrunch.com/2026/04/17/kevin-weil-and-bill-peebles-exit-openai-as-company-continues-to-shed-side-quests/']]},
  {d:'2026-04-17',t:'out',p:'ケイト・ラウチ',en:'Kate Rouch',role:'CMO(最高マーケティング責任者)',to:'(療養)',note:'がんの治療に専念するためと報道',cf:'r',src:[['The Next Web(2026/4/18)','https://thenextweb.com/news/openai-departures-kevin-weil-sora-peebles-enterprise-pivot']]},
  {d:'2026-06-08',t:'co',p:'上場の準備',en:'',role:'',note:'OpenAIがS-1(上場の届け出書類の下書き)を米SECに非公開で出したと公表。「時期はまだ決めていない」とも。約1週間前にAnthropicも提出',cf:'r',src:[['TechRepublic(2026/6)','https://www.techrepublic.com/article/news-openai-confidential-sec-ipo-filing/'],['ABC7(AP、2026/6)','https://abc7ny.com/post/openai-files-confidential-sec-paperwork-ipo-opening-door-wall-street-debut/19259780/']]},
  {d:'2026-06-18',t:'in',p:'ノーム・シェイザー',en:'Noam Shazeer',role:'研究の幹部',from:'Google DeepMind(Gemini共同責任者)',note:'Transformer論文の著者の1人',cf:'r',src:[['Fast Company(2026/6/18)','https://www.fastcompany.com/91562193/google-ai-leader-noam-shazeer-leaves-company-for-openai']]},
  {d:'2026-06-26',t:'in',p:'ポール・ミード',en:'Paul Meade',role:'ハードウェア部門',from:'Apple',note:'Appleからハードウェア人材の引き抜きが続く',cf:'r',src:[['AppleInsider(2026/6/26)','https://appleinsider.com/articles/26/06/26/openai-has-poached-another-apple-executive-for-its-hardware-division']]},
  {d:'2026-07-07',t:'out',p:'ジョシュア・アキアム',en:'Joshua Achiam',role:'チーフフューチャリスト(元ミッション・アラインメント責任者)',to:'(社外で安全なAIの仕事を続ける)',note:'約9年在籍。WIREDが報道。2月にミッション・アラインメントのチームが解散していた',cf:'r',src:[['Placera(WIREDを引用、2026/7/8)','https://www.placera.se/telegram/wired-openai-profilen-joshua-achiam-lamnar-bolaget-20260708']]},
  {d:'2026-07-09',t:'out',p:'フィジー・シモ',en:'Fidji Simo',role:'AGIデプロイメント担当CEO(社内の2番手)',to:'(非常勤のアドバイザー)',note:'4月から病気で休職し、フルタイムを退くと発表。製品などの役割はブロックマンが引き継ぐ',cf:'r',src:[['TechCrunch(2026/7/9)','https://techcrunch.com/2026/07/09/fidji-simo-steps-down-from-openais-no-2-role/']]},
  {d:'2026-07-10',t:'out',p:'ヨハネス・ハイデッケ',en:'Johannes Heidecke',role:'安全システムの責任者',to:'(未発表)',note:'研究と安全のチームを1つにする再編のあと。メリア・グレイズが研究・安全VPに、サーチ・ジェインが暫定の責任者に',cf:'r',src:[['The Next Web(2026/7)','https://thenextweb.com/news/openai-heidecke-safety-head-leaving-research-merger'],['ThePrint(WIREDを引用)','https://theprint.in/world/openai-safety-chief-johannes-heidecke-to-leave-firm-after-reshuffle-wired-report/2983693/']]},
  {d:'2026-07-30',t:'in',p:'リリアン・ウェン',en:'Lilian Weng',role:'研究チームの責任者',from:'Thinking Machines Lab(共同創業者)',note:'2024年11月に退社していたが復帰',cf:'r',src:[['Dataconomy(TechCrunchを引用、2026/7/30)','https://dataconomy.com/2026/07/30/lilian-weng-rejoins-openai-lead-ai-research-team/']]},
  {d:'2026-08-11',t:'out',p:'ブラッド・ライトキャップ',en:'Brad Lightcap',role:'元COO(2022〜2026年4月)、特別プロジェクト担当',to:'(起業予定)',note:'約8年在籍。4月にCOOから特別プロジェクトに移っていた',cf:'r',src:[['Axios(2026/8/11)','https://axios.com/2026/08/11/openai-executive-brad-lightcap-is-leaving'],['TechCrunch(2026/8/11)','https://techcrunch.com/2026/08/11/brad-lightcap-openais-longtime-coo-is-leaving-to-start-something-new/']]},
  {d:'2026-08-13',t:'out',p:'デニス・ドレッサー',en:'Denise Dresser',role:'CRO(売上の責任者)',to:'(未発表)',note:'1年足らずで退任。ライトキャップの2日後',cf:'r',src:[['Axios(2026/8/13)','https://axios.com/2026/08/13/openai-denise-dresser-replace-chief-revenue-officer']]},
  {d:'2026-08-13',t:'in',p:'ダリ・ラジッチ',en:'Dali Rajic',role:'CRO(売上の責任者)',from:'Wiz(社長兼COO)',note:'ドレッサーの後任。営業の組織を作り直すと報道',cf:'r',src:[['Bloomberg(2026/8/13)','https://www.bloomberg.com/news/articles/2026-08-13/openai-hires-new-chief-revenue-officer-after-less-than-a-year'],['The Next Web','https://thenextweb.com/news/openai-denise-dresser-exit-dali-rajic-cro']]},
  {d:'2026-08-21',t:'out',p:'ケイリン・ヴォス',en:'Kaylin Voss',role:'米州の営業VP',to:'Salesforce(復帰)',note:'約5か月で退任。前の上司ドレッサーの退任の約1週間後',cf:'r',src:[['The Next Web(2026/8/24)','https://thenextweb.com/news/openai-kaylin-voss-resigns-salesforce-rajic-sales']]},
  {d:'2026-08-24',t:'out',p:'ルーク・メッツ',en:'Luke Metz',role:'研究者',to:'Meta(Superintelligence Labs)',note:'1月に戻ってから約7か月',cf:'r',src:[['The Next Web(2026/8)','https://thenextweb.com/news/luke-metz-meta-superintelligence-labs-openai']]},
  {d:'2026-08-25',t:'out',p:'クリス・マローン',en:'Chris Malone',role:'データセンターの責任者',to:'(未発表)',note:'報道の数え方で、2026年に退いた幹部は14人に',cf:'r',src:[['CNBC(2026/8/25)','https://www.cnbc.com/2026/08/25/openais-head-of-data-centers-chris-malone-is-out-in-latest-exec-exit.html'],['TechCrunch(2026/8/25)','https://techcrunch.com/2026/08/25/openai-loses-a-top-data-center-exec-as-stream-of-high-profile-departures-continues/']]},
  {d:'2026-08-26',t:'out',p:'バレット・ゾフ',en:'Barret Zoph',role:'研究の幹部',to:'Google DeepMind(研究VP)',note:'1月に戻ってから約7か月',cf:'r',src:[['Quartz(2026/8)','https://qz.com/barret-zoph-google-deepmind-research-vp-thinking-machines-082726']]},
  {d:'2026-09-18',t:'in',p:'ブライアン・マッカーシー',en:'Brian McCarthy',role:'世界営業VP(新設)',from:'SpaceX(旧Cursor)',note:'',cf:'r',src:[['The Next Web(2026/9/18)','https://thenextweb.com/news/openai-brian-mccarthy-worldwide-sales-spacex-cursor']]},
  {d:'2026-10-03',t:'out',p:'デビッド・ロビンソン',en:'David Robinson',role:'安全報告書づくりを率いた研究者',to:'(社外で活動)',note:'The Atlanticに「文化が壊れている」と寄稿して退社',cf:'s',src:[['TechCrunch(2026/10/3)','https://techcrunch.com/2026/10/03/openai-safety-employee-resigns-claiming-the-companys-culture-is-broken/']]},
  {d:'2026-10-08',t:'in',p:'イスマイル・エルマス',en:'Ismail Elmas',role:'欧州・中東・アフリカの営業VP(ミュンヘン)',from:'Cursor',note:'OpenAIが独Handelsblattに認めた',cf:'r',src:[['The Next Web(2026/10/8)','https://thenextweb.com/news/openai-ismail-elmas-emea-sales-spacex-cursor']]},
  {d:'2026-10-14',t:'out',p:'サチン・カッティ',en:'Sachin Katti',role:'計算資源インフラの責任者',to:'(顧問。新しく何かを作ると表明)',note:'約1年で退任。後任はウダイ・ルッダラジュ(ブロックマン直属)',cf:'r',src:[['Analytics India Magazine(2026/10)','https://analyticsindiamag.com/ai-news/sachin-katti-to-leave-openai-after-leading-major-compute-expansion']]},
  {d:'2026-11-03',t:'in',p:'ジル・ヘイゼルベイカー',en:'Jill Hazelbaker',role:'渉外の責任者(Chief Corporate Affairs Officer)',from:'Uber',note:'広報・政府対応を統括。ブロックマン直属で12月初めに着任と報道。上場準備の一環とみられる',cf:'r',src:[['Axios(2026/11/3)','https://axios.com/2026/11/03/jill-hazelbaker-openai-uber']]},
  {d:'2026-11-03',t:'in',p:'ダン・ドリスコル',en:'Dan Driscoll',role:'国家安全保障の上級顧問',from:'米陸軍(元陸軍長官)',note:'',cf:'r',src:[['CNBC(2026/11/3)','https://www.cnbc.com/2026/11/03/openai-hires-dan-driscoll-national-security.html']]}
 ],
 points:[
  '売上・営業の上の人が2026年にほぼ入れ替わりました(CRO ドレッサー → ラジッチ、米州VPヴォス退任、世界営業VPマッカーシーと欧州VPエルマスが新任)。以前の担当者とのつながりは、今は使えないことがあります。',
  '社長のブロックマンに、計算資源・売上・渉外の責任者が集まっていると報じられています。大きな提携の話は、ブロックマンの周りの人が窓口になりやすいとみられます(報道ベースの見立て)。',
  '上場の準備書類を出した2026年6月8日のあとも、幹部の退任が続いています。上場の時期は「まだ決めていない」と会社は言っています。'
 ]
}
};

let exTlKey='openai',exTlType='all',exTlYear='all';
function exTlYearOf(e){return e.d.slice(0,4)}
function exTlFmt(d){const [y,m,dd]=d.split('-');return y+'年'+(+m)+'月'+(dd?(+dd)+'日':'')}
const EXTL_T={in:['入社','var(--active)'],out:['退社','var(--conflict)'],role:['役割の変更','var(--invest)'],co:['会社の出来事','var(--deal)']};
function exTlText(D,list){
  const L=[`${D.name} 幹部の入れ替わり年表(${exTlFmt(D.asof)}時点)`,''];
  if(D.ipo)L.push(`上場の準備: ${exTlFmt(D.ipo.d)} ${D.ipo.label}`,'');
  L.push('【今の主な顔ぶれ(報道ベース)】');D.now.forEach(r=>L.push(`・${r[0]}: ${r[1]}(${r[2]})`));L.push('');
  L.push('【営業で使えるポイント】');D.points.forEach(p=>L.push('・'+p));L.push('');
  L.push('【年表】');
  list.forEach(e=>{const cf=(typeof CFL!=='undefined'&&CFL[e.cf])?CFL[e.cf].t:e.cf;
    L.push(`${exTlFmt(e.d)} [${EXTL_T[e.t][0]}・${cf}] ${e.p}${e.role?'('+e.role+')':''}${e.from?' ← '+e.from:''}${e.to?' → '+e.to:''}${e.note?' / '+e.note:''}`);
    e.src.forEach(s=>L.push(`    出典: ${s[0]} ${s[1]}`))});
  L.push('','公式=会社の発表、本人=本人の投稿・寄稿、報道=報道だけで確かめたもの。AI企業の相関図より。');
  return L.join('\n');
}
function showExecTl(key){
  if(key&&EXECTL[key])exTlKey=key;
  stop();leavePerson();ctrail=[];
  MAINEL.hidden=true;controls.hidden=true;trailbar.hidden=true;document.getElementById('subbar').hidden=true;RANKEL.hidden=true;PROFEL.hidden=true;UNIEL.hidden=true;FEEDEL.hidden=false;
  document.querySelectorAll('#tabs button').forEach(b=>b.setAttribute('aria-pressed','false'));
  const D=EXECTL[exTlKey];
  document.getElementById('title').textContent='幹部の年表('+D.name+')';document.title='幹部の年表 '+D.name;
  document.getElementById('note').textContent='';
  exTlRender();
}
function exTlRender(){
  const D=EXECTL[exTlKey],esc=kkEsc;
  const all=D.ev.slice().sort((a,b)=>a.d<b.d?-1:a.d>b.d?1:0);
  const years=[...new Set(all.map(exTlYearOf))];
  const list=all.filter(e=>(exTlType==='all'||e.t===exTlType)&&(exTlYear==='all'||exTlYearOf(e)===exTlYear));
  const y26=all.filter(e=>exTlYearOf(e)==='2026');
  const out26=y26.filter(e=>e.t==='out').length,in26=y26.filter(e=>e.t==='in').length;
  const afterIpo=D.ipo?all.filter(e=>e.t==='out'&&e.d>D.ipo.d).length:0;
  const ok=all.filter(e=>e.cf==='o'||e.cf==='f'||e.cf==='s').length;
  let ipoShown=false;let lastY='';
  const rows=[];
  list.forEach(e=>{
    const y=exTlYearOf(e);if(y!==lastY){rows.push(`<li class="xt-y">${y}年</li>`);lastY=y}
    if(D.ipo&&!ipoShown&&e.d>D.ipo.d){ipoShown=true;rows.push(`<li class="xt-ipo">ここから上場の準備書類を出したあと(${exTlFmt(D.ipo.d)})</li>`)}
    const T=EXTL_T[e.t];
    rows.push(`<li class="xt-e" style="--c:${T[1]}"><div class="xt-d">${exTlFmt(e.d)}</div><div class="xt-b">
      <div class="xt-h"><span class="xt-t">${T[0]}</span>${typeof cfBadge==='function'?cfBadge(e.cf):''}<b>${esc(e.p)}</b>${e.en?` <small>${esc(e.en)}</small>`:''}</div>
      ${e.role?`<div class="xt-r">${esc(e.role)}</div>`:''}
      ${e.from?`<div class="xt-m">前は: ${esc(e.from)}</div>`:''}${e.to?`<div class="xt-m">次は: ${esc(e.to)}</div>`:''}
      ${e.note?`<div class="xt-n">${esc(e.note)}</div>`:''}
      <div class="xt-s">${e.src.map(s=>`<a href="${esc(s[1])}" target="_blank" rel="noopener">${esc(s[0])}</a>`).join(' ・ ')}</div></div></li>`);
  });
  if(D.ipo&&!ipoShown&&exTlType==='all'&&exTlYear==='all')rows.push(`<li class="xt-ipo">上場の準備書類を出した日: ${exTlFmt(D.ipo.d)}</li>`);
  FEEDEL.innerHTML=`<style>
  .xt-wrap{max-width:900px}
  .xt-lead{font-size:13px;color:var(--muted);margin:0 0 10px;max-width:70ch}
  .xt-top{display:flex;flex-wrap:wrap;gap:10px;margin:4px 0 12px}
  .xt-top div{border:1px solid var(--line);border-radius:10px;padding:8px 12px;background:var(--surface);min-width:0}
  .xt-top b{display:block;font-size:26px;line-height:1.15;font-variant-numeric:tabular-nums}.xt-top small{color:var(--muted);font-size:12px}
  .xt-top .o b{color:var(--conflict)}.xt-top .i b{color:var(--active)}
  .xt-bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:0 0 10px;font-size:13px}
  .xt-bar button{font:inherit;font-size:13px;padding:5px 10px;border-radius:6px;border:1px solid var(--line);background:var(--surface);color:var(--fg);cursor:pointer}
  .xt-bar button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
  .xt-box{border:1px solid var(--line);border-radius:10px;background:var(--surface);padding:10px 14px;margin:0 0 12px}
  .xt-box h3{font-size:14px;margin:0 0 6px}
  .xt-box ul{margin:0;padding-left:1.2em;font-size:13px;line-height:1.6}
  .xt-now{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px;font-size:13px}
  .xt-now div{min-width:0;overflow-wrap:anywhere}.xt-now small{color:var(--muted);display:block}
  .xt{list-style:none;margin:0;padding:0}
  .xt-y{font-weight:700;font-size:16px;margin:14px 0 6px}
  .xt-ipo{margin:10px 0;padding:6px 10px;border:2px dashed var(--deal);border-radius:8px;color:var(--fg);font-size:13px;font-weight:700}
  .xt-e{display:grid;grid-template-columns:96px minmax(0,1fr);gap:10px;padding:8px 0;border-top:1px solid var(--line)}
  .xt-d{font-size:12px;color:var(--muted);font-variant-numeric:tabular-nums}
  .xt-b{border-left:4px solid var(--c);padding-left:10px;min-width:0;overflow-wrap:anywhere}
  .xt-h{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center}.xt-h small{color:var(--muted)}
  .xt-t{font-size:11px;font-weight:700;color:var(--c);border:1px solid var(--c);border-radius:4px;padding:0 4px}
  .xt-r{font-size:13px;margin-top:2px}.xt-m{font-size:12px;color:var(--muted)}.xt-n{font-size:13px;margin-top:3px}
  .xt-s{font-size:12px;margin-top:3px}.xt-s a{color:var(--invest)}
  @media (max-width:520px){.xt-e{grid-template-columns:minmax(0,1fr);gap:2px}}
  </style>
  <div class="xt-wrap">
  <p class="xt-lead">${esc(D.note)}</p>
  <div class="xt-top"><div class="o"><b>${out26}件</b><small>2026年に退いた幹部など</small></div><div class="i"><b>${in26}件</b><small>2026年に入った幹部など</small></div>${D.ipo?`<div><b>${afterIpo}件</b><small>上場の準備書類のあとの退任</small></div>`:''}<div><b>${ok} / ${all.length}</b><small>公式・本人で確かめた件数</small></div></div>
  <div class="xt-box"><h3>営業で使えるポイント</h3><ul>${D.points.map(p=>`<li>${esc(p)}</li>`).join('')}</ul></div>
  <details class="xt-box"><summary><b>今の主な顔ぶれ(${exTlFmt(D.asof)}時点、報道ベース)</b></summary><div class="xt-now" style="margin-top:8px">${D.now.map(r=>`<div><small>${esc(r[0])}</small>${esc(r[1])}<small>${esc(r[2])}</small></div>`).join('')}</div></details>
  <div class="xt-bar" role="group" aria-label="種類で絞り込む"><span class="meta">種類</span>${[['all','すべて'],['out','退社'],['in','入社'],['role','役割の変更'],['co','会社の出来事']].map(([v,t])=>`<button type="button" data-t="${v}" aria-pressed="${exTlType===v}">${t}</button>`).join('')}</div>
  <div class="xt-bar" role="group" aria-label="年で絞り込む"><span class="meta">年</span>${[['all','すべて'],...years.map(y=>[y,y+'年'])].map(([v,t])=>`<button type="button" data-y="${v}" aria-pressed="${exTlYear===v}">${t}</button>`).join('')}</div>
  <div class="xt-bar"><button type="button" id="xtcopy">テキストをコピー</button><button type="button" id="xtsave">.txtで保存</button><span class="meta" id="xtmsg" aria-live="polite"></span></div>
  <ol class="xt">${rows.join('')||'<li class="meta">当てはまるものがありません</li>'}</ol>
  </div>`;
  FEEDEL.querySelectorAll('.xt-bar button[data-t]').forEach(b=>b.addEventListener('click',()=>{exTlType=b.dataset.t;exTlRender()}));
  FEEDEL.querySelectorAll('.xt-bar button[data-y]').forEach(b=>b.addEventListener('click',()=>{exTlYear=b.dataset.y;exTlRender()}));
  const msg=t=>{const m=document.getElementById('xtmsg');if(m)m.textContent=t};
  document.getElementById('xtcopy').addEventListener('click',()=>{const t=exTlText(D,list);
    (navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(t):Promise.reject()).then(()=>msg('コピーしました')).catch(()=>msg('コピーできませんでした'))});
  document.getElementById('xtsave').addEventListener('click',()=>{const t=exTlText(D,list);
    if(typeof saveTextFile==='function')saveTextFile(D.name+'_幹部の年表.txt',t,msg)});
}
