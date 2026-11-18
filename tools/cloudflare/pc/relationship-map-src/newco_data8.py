import re, json, os, unicodedata
from newco_data import mk, std
S = os.path.dirname(os.path.abspath(__file__))

# 日経「米国株 時価総額上位ランキング」(2026-11-02更新、10/30終値)の200社
EN = dict(x.split('=', 1) for x in """AAPL=Apple
NVDA=Nvidia
MSFT=Microsoft
AMZN=Amazon
GOOGL=Alphabet
TSLA=Tesla
AVGO=Broadcom
GOOG=Alphabet
META=Meta
LLY=Eli Lilly
SPCX=SpaceX
MU=Micron Technology
WMT=Walmart
JPM=JPMorgan Chase
AMD=AMD
XOM=ExxonMobil
BRK.B=Berkshire Hathaway
V=Visa
JNJ=Johnson & Johnson
MA=Mastercard
ABBV=AbbVie
CVX=Chevron
COST=Costco
PLTR=Palantir
BRK.A=Berkshire Hathaway
CSCO=Cisco
KO=Coca-Cola
ORCL=Oracle
PG=Procter & Gamble
MRK=Merck
UNH=UnitedHealth Group
BAC=Bank of America
INTC=Intel
HD=Home Depot
PM=Philip Morris International
GE=GE Aerospace
AMAT=Applied Materials
PANW=Palo Alto Networks
LRCX=Lam Research
AZN=AstraZeneca
MS=Morgan Stanley
CAT=Caterpillar
RY=Royal Bank of Canada
TXN=Texas Instruments
RTX=RTX
GS=Goldman Sachs
TMO=Thermo Fisher Scientific
CRWD=CrowdStrike
NFLX=Netflix
AMGN=Amgen
WFC=Wells Fargo
IBM=IBM
LIN=Linde
GEV=GE Vernova
AXP=American Express
ANET=Arista Networks
GILD=Gilead Sciences
TTE=TotalEnergies
TD=Toronto-Dominion Bank
KLAC=KLA
C=Citigroup
ADI=Analog Devices
APH=Amphenol
DIS=Walt Disney
SHOP=Shopify
CRM=Salesforce
PEP=PepsiCo
VZ=Verizon
COP=ConocoPhillips
ABT=Abbott Laboratories
MCD=McDonald's
DE=Deere
UNP=Union Pacific
BLK=BlackRock
QCOM=Qualcomm
NEE=NextEra Energy
PFE=Pfizer
MRVL=Marvell Technology
WELL=Welltower
SNDK=Sandisk
TMUS=T-Mobile US
DHR=Danaher
TJX=TJX
ACN=Accenture
SCHW=Charles Schwab
SCCO=Southern Copper
ISRG=Intuitive Surgical
STX=Seagate Technology
UBS=UBS Group
LMT=Lockheed Martin
T=AT&T
ETN=Eaton
VRTX=Vertex Pharmaceuticals
CB=Chubb
WDC=Western Digital
BA=Boeing
SPGI=S&P Global
PGR=Progressive
DELL=Dell Technologies
UBER=Uber
MO=Altria
BMY=Bristol Myers Squibb
MPC=Marathon Petroleum
MDT=Medtronic
COF=Capital One
SPOT=Spotify
PLD=Prologis
BMO=Bank of Montreal
SBUX=Starbucks
LOW=Lowe's
ADP=ADP
MCK=McKesson
CNQ=Canadian Natural Resources
BNS=Bank of Nova Scotia
CVS=CVS Health
PH=Parker Hannifin
ENB=Enbridge
SYK=Stryker
VLO=Valero Energy
BKNG=Booking Holdings
NEM=Newmont
PSX=Phillips 66
NOW=ServiceNow
CME=CME Group
SNOW=Snowflake
SO=Southern Company
GLW=Corning
CM=CIBC
MAR=Marriott International
GD=General Dynamics
EQIX=Equinix
FTNT=Fortinet
BNY=BNY
DUK=Duke Energy
HCA=HCA Healthcare
ADBE=Adobe
CSX=CSX
MRSH=Marsh McLennan
ICE=Intercontinental Exchange
REGN=Regeneron
PWR=Quanta Services
CEG=Constellation Energy
SU=Suncor Energy
WM=Waste Management
MNST=Monster Beverage
USB=U.S. Bancorp
EMR=Emerson Electric
INTU=Intuit
WMB=Williams Companies
ELV=Elevance Health
NET=Cloudflare
PNC=PNC Financial Services
JCI=Johnson Controls
MMM=3M
BX=Blackstone
CDNS=Cadence Design Systems
TT=Trane Technologies
FCX=Freeport-McMoRan
SNPS=Synopsys
VRT=Vertiv
MRNA=Moderna
BN=Brookfield
CTAS=Cintas
AMT=American Tower
EOG=EOG Resources
MCO=Moody's
ECL=Ecolab
KKR=KKR
AEM=Agnico Eagle Mines
EPD=Enterprise Products Partners
MELI=MercadoLibre
CMCSA=Comcast
MDLZ=Mondelez International
RCL=Royal Caribbean
MSI=Motorola Solutions
TRV=Travelers
UPS=UPS
SHW=Sherwin-Williams
HLT=Hilton
SLB=SLB
HWM=Howmet Aerospace
NOC=Northrop Grumman
ITW=Illinois Tool Works
CI=Cigna
DDOG=Datadog
CP=CPKC
BAM=Brookfield Asset Management
NSC=Norfolk Southern
LITE=Lumentum
CL=Colgate-Palmolive
KMI=Kinder Morgan
RSG=Republic Services
CNI=Canadian National Railway
MFC=Manulife
GM=General Motors
FDX=FedEx
DASH=DoorDash
HPE=Hewlett Packard Enterprise
ROST=Ross Stores
URI=United Rentals""".splitlines())

# すでに単独の図がある会社
EXIST = {'NVDA': 'nvidia', 'MSFT': 'msft', 'META': 'meta', 'UBER': 'uber', 'DASH': 'doordash'}
SAME = {'GOOG': 'GOOGL', 'BRK.A': 'BRK.B'}
def key_of(t):
    if t in EXIST:
        return EXIST[t]
    t = SAME.get(t, t)
    return 'us_' + ('BRK' if t == 'BRK.B' else t.replace('.', '_'))

def norm(n):
    n = re.sub(r' \(.*\)', '', n).strip()
    n = n.replace('Sir ', '').replace(', Jr.', '').replace(' Jr.', '').replace(' III', '')
    toks = [w for w in n.split() if not re.fullmatch(r'[A-Z]\.', w)]
    n = ' '.join(toks)
    return {'Gail Koziara Boudreaux': 'Gail Boudreaux'}.get(n, n)

KANA = {}
for l in open(S + r'\kana.txt', encoding='utf-8'):
    l = l.strip()
    if '=' in l:
        a, b = l.split('=', 1)
        KANA[norm(a)] = b

def role_jp(t):
    t0 = t.lower()
    t0 = re.sub(r'\(.*?\)', '', t0).strip()
    if re.search(r'former|retired|emeritus|retiring', t) and 'retiring as ceo' not in t0:
        pass
    if ' of ' in t0 or 'markets' in t0 or 'laboratories' in t0 or 'sector' in t0 or 'research' in t0:
        return '部門: ' + t
    parts = []
    exe = 'executive' in t0
    if 'co-chair' in t0 or 'co-executive chairman' in t0:
        parts.append('共同会長')
    elif 'vice chair' in t0:
        parts.append('副会長')
    elif 'chairman emeritus' in t0 or 'chairman emerita' in t0:
        parts.append('名誉会長')
    elif 'senior chairman' in t0:
        parts.append('名誉会長(シニア)')
    elif 'lead independent' in t0:
        parts.append('筆頭社外取締役')
    elif 'chair' in t0:
        parts.append('会長(執行)' if exe else '会長')
    if 'co-ceo' in t0:
        parts.append('共同CEO')
    elif re.search(r'\bceo\b|chief executive', t0):
        parts.append('CEO')
    if re.search(r'\bpresident\b', t0) and 'vice president' not in t0 and 'group president' not in t0:
        parts.append('社長')
    elif 'president' in t0:
        parts.append('プレジデント')
    for k, v in [('cfo', 'CFO'), ('coo', 'COO'), ('cto', 'CTO'), ('cso', 'CSO'), ('cio', 'CIO'), ('cmo', 'CMO'), ('cbo', 'CBO'), ('cpo', 'CPO'), ('cco', 'CCO'), ('chief architect', 'チーフアーキテクト')]:
        if re.search(r'\b%s\b' % k, t0) or k in t0.split() or (k == 'chief architect' and k in t0):
            parts.append(v)
    if 'director' in t0 and not parts:
        parts.append('取締役')
    if not parts:
        parts.append(t)
    # 「会長 社長 CEO」の順で、兼任は「兼」でつなぐ
    out = '兼'.join(dict.fromkeys(parts))
    # 先頭を、トップの段に入る言葉にする: CEO > 会長 > 社長
    if 'CEO' in out and not out.startswith(('CEO', '会長', '社長')):
        pass
    return out

def tier1_first(parts_str):
    return parts_str

def parse():
    people = {}
    for l in open(S + r'\us_people.txt', encoding='utf-8'):
        l = l.strip()
        if not l:
            continue
        t, r = l.split('|', 1)
        people[t] = [(norm(x.split(' — ')[0]), x.split(' — ', 1)[1].strip() if ' — ' in x else '') for x in r.split(';')]
    return people

ORGS = {
 'AMZN': [('anthropic', 'Anthropic', '出資・提携先。')],
 'GOOGL': [('anthropic', 'Anthropic', '出資先。'), ('deepmind', 'Google DeepMind', 'AI研究部門。'), ('waymo', 'Waymo', '自動運転の子会社。'), ('isomorphic', 'Isomorphic Labs', 'AI創薬の子会社。')],
 'SPCX': [('xai', 'xAI', '2026年2月にSpaceXが買収したと報じられています。')],
 'TSLA': [('spacex', 'SpaceX', 'マスクが率いる関連会社。'), ('xai', 'xAI', 'マスクが率いる関連会社。')],
 'ORCL': [('openai', 'OpenAI', 'スターゲートで提携。')],
 'AVGO': [('openai', 'OpenAI', '専用チップの提携先と報じられています。')],
 'AMD': [('openai', 'OpenAI', 'AIチップの提携先と報じられています。')],
 'CRM': [('slack', 'Slack', '2021年に買収した子会社。')],
}

CANON = [('Vanguard', 'Vanguard'), ('Blackrock', 'BlackRock'), ('BlackRock', 'BlackRock'), ('State Street', 'State Street'), ('STATE STREET', 'State Street'),
         ('SSgA', 'State Street'), ('FMR', 'Fidelity'), ('Fidelity', 'Fidelity'), ('Capital Research', 'Capital Group'), ('Capital World', 'Capital Group'),
         ('Capital Group', 'Capital Group'), ('Geode', 'Geode Capital'), ('Invesco', 'Invesco'), ('JPMorgan', 'JPMorgan Asset Mgmt'), ('JPMORGAN', 'JPMorgan Asset Mgmt'),
         ('Eaton Vance', 'Eaton Vance'), ('Wellington', 'Wellington'), ('T. Rowe', 'T. Rowe Price')]
def canon(h):
    h = h.strip()
    for k, v in CANON:
        if h.startswith(k):
            return v
    return h
HOLD = {}
for _l in open(S + r'\us_holders.txt', encoding='utf-8'):
    _l = _l.strip()
    if not _l:
        continue
    _t, _meta, _hs = _l.split('|', 2)
    _rows, _seen = [], set()
    for _x in _hs.split(';'):
        _n, _v = _x.rsplit('=', 1)
        _c = canon(_n)
        if _c in _seen:
            continue
        _seen.add(_c)
        _rows.append((_c, _v))
    HOLD[_t] = (_meta, _rows)

def build():
    people = parse()
    co = {}
    rank = []
    for l in open(S + r'\ranking.txt', encoding='utf-8'):
        r, jp, t, cap = l.strip().split('|')
        jp = unicodedata.normalize('NFKC', jp)
        key = key_of(t)
        rank.append({'r': int(r), 'jp': jp, 'en': EN.get(t, jp), 'tk': t, 'cap': int(cap), 'key': key, 'new': key.startswith('us_')})
        if not key.startswith('us_') or key in co:
            continue
        base = SAME.get(t, t)
        base = 'BRK' if base == 'BRK.B' else base
        rows = people.get(base)
        if rows is None:
            rows = []   # 新規ランクイン: 人物は未調査。会社だけの図にする
        N = [{'id': 'co', 'name': EN.get(t, jp), 'kind': 'c', 'from': 2026, 'desc': '日経の米国株時価総額ランキングの企業(ティッカー %s)。%s' % (t if t not in SAME else SAME[t], '')}]
        enmap = {}
        seen = set()
        for i, (name, title) in enumerate(rows):
            if name in seen or name not in KANA:
                if name not in KANA:
                    raise SystemExit('no kana ' + name)
                continue
            seen.add(name)
            pid = 'p%d' % i
            rj = role_jp(title)
            N.append({'id': pid, 'name': KANA[name], 'kind': 'p', 'from': 2026, 'desc': '%s(英語版Wikipediaの「Key people」。取得日 2026年11月2日)。' % (title or '役職の記載なし'), 'role': rj})
            enmap[pid] = name
        extra = ''
        for oid, oname, odesc in ORGS.get(base, []):
            N.append({'id': oid, 'name': oname, 'kind': 'o', 'from': 2026, 'desc': odesc, 'role': '関連'})
            extra += "E.push({a:'co',b:'%s',k:'link'});\n" % oid
        hold = HOLD.get(base)
        edges = "const E = [];\nN.forEach(n=>{ if(n.kind==='p') E.push({a:n.id,b:'co',k:'member'}); });\n"
        if hold:
            meta, hs = hold
            for hi, (h, pct) in enumerate(hs):
                nm = KANA.get(norm(h), h)
                src = 'Yahoo Finance(2026年6月30日時点)' if meta.startswith('INS') else 'MarketScreener(2026年11月)'
                N.append({'id': 'h%d' % hi, 'name': nm, 'kind': 'i', 'from': 2026, 'role': '株主(約%s%%)' % pct,
                          'desc': '上位株主の1つ(約%s%%)。出典: %s。' % (pct, src)})
                edges += "E.push({a:'h%d',b:'co',k:'invest',label:'%s%%'});\n" % (hi, pct)
            if meta.startswith('INS'):
                a, b = re.findall(r'[\d.]+', meta)[:2]
                N[0]['desc'] += '内部者(役員など)の保有は約%s%%、機関投資家は約%s%%(Yahoo Finance、2026年6月30日時点)。' % (a, b)
            else:
                N[0]['desc'] += '上位株主はMarketScreener(2026年11月)の表に基づきます。'
        co[key] = mk(N, edges + extra, enmap, {}, {}, {}, {}, {}, 'co')
    return co, rank

CO8, RANK = build()

# 深掘りした会社は、上の簡易版を置き換える
import newco_data9b
import newco_data9c
import newco_data9d
import newco_data9e
import newco_data9f
import newco_data9g
import newco_data9h
import newco_data9i
import newco_data9j
import newco_data9k
import newco_data9l
import newco_data9m
import newco_data9n
import newco_data9o
import newco_data9p
import newco_data9q
import newco_data9r
import newco_data9s
import newco_data9t
import newco_data9u
import newco_data9v
import newco_data9w
import newco_data9x
from newco_data9 import DEEP
for _t, _d in DEEP.items():
    _k = key_of(_t)
    CO8[_k] = _d['co']
    for _r in RANK:
        if _r['key'] == _k:
            _r['min'] = _d['min']
            _r['note'] = _d['note']

# 注目スタートアップ
import newco_data10
import newco_data11
import newco_data12
import newco_data13
import newco_data14
import newco_data15
import newco_data15b
import newco_data15c
import newco_data16
CO8.update(newco_data10.CO10)
STARTUPS = newco_data10.STARTUPS
# 日本の時価総額上位企業の図(日経の会社概要+Wikidataから自動作成)
import newco_jp
CO8.update(newco_jp.COJP)
JPCO = newco_jp.JPCO
# ユニコーン一覧の会社のうち、まだ図がない会社の図(創業者・CEO・株主)。既存の会社名と重ならないものだけ
import newco_uni
_nn = newco_uni.n2
_ex = set()
import newco_data as _m1, newco_data2 as _m2, newco_data3 as _m3, newco_data4 as _m4, newco_data5 as _m5, newco_data6 as _m6, newco_data7 as _m7, newco_data7b as _m7b
for _co in (_m1.CO, _m2.CO2, _m3.CO3, _m4.CO4, _m5.CO5, _m6.CO6, _m7.CO7, _m7b.CO7B, CO8):
    for _c in _co.values():
        for _n in _c['N']:
            if _n['id'] == _c['center']:
                _ex.add(_nn(_n['name']))
_ex |= {_nn(x) for x in ('OpenAI', 'Anthropic', 'xAI', 'Meta', 'Facebook', 'Google DeepMind', 'DeepMind', 'Mercari', 'Rakuten', 'Slack', 'Uber', 'DoorDash')}
_ex |= {_nn(r['name']) for r in STARTUPS} | {_nn(r['en']) for r in RANK}
COUNI, UNICO = newco_uni.build(_ex)
CO8.update(COUNI)
JPCO = JPCO + UNICO     # 日本企業とユニコーンの図は、タブには並べず、会社名のリンクとして使う
# VCの投資先・資金調達ニュースの会社(小さなスタートアップを含む)の図
import newco_vcco
_ex2 = set(_ex) | {_nn(r['name']) for r in JPCO}
COVC, VCCO = newco_vcco.build(_ex2)
CO8.update(COVC)
JPCO = JPCO + VCCO
# 大企業が買収した会社・子会社の図(人物・買収元つき)
import newco_acq
_ex3 = set(_ex2) | {_nn(r['name']) for r in VCCO}
COAQ, AQCO = newco_acq.build(_ex3)
CO8.update(COAQ)
JPCO = JPCO + AQCO
