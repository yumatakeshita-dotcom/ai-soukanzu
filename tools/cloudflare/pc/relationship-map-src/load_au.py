"""オーストラリアの ABN Bulk Extract(data.gov.au, CC BY 3.0 AU)から、現存(ABN status=ACT)する法人・団体(個人事業主 IND を除く)を world_au.sqlite に入れる。
使い方: python -I -X utf8 load_au.py"""
import io, os, re, sqlite3, time, zipfile
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
RAW = os.path.join(D, 'world_raw', 'au')
db = sqlite3.connect(os.path.join(D, 'world_au.sqlite'))
db.execute('PRAGMA journal_mode=OFF')
db.execute('PRAGMA synchronous=OFF')
db.execute('CREATE TABLE IF NOT EXISTS wcorp (cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT, PRIMARY KEY (cc, id))')
db.execute('DELETE FROM wcorp')
R = re.compile(r'<ABR [^>]*>.*?</ABR>', re.S)
ABN = re.compile(r'<ABN status="(\w+)" ABNStatusFromDate="(\d+)">(\d+)</ABN>')
ET = re.compile(r'<EntityTypeInd>(\w+)</EntityTypeInd><EntityTypeText>([^<]*)</EntityTypeText>')
NM = re.compile(r'<MainEntity><NonIndividualName type="MN"><NonIndividualNameText>([^<]*)</NonIndividualNameText>')
ST = re.compile(r'<State>(\w*)</State><Postcode>(\w*)</Postcode>')
UN = re.compile(r'&(amp|lt|gt|quot|apos);')
M = {'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'"}
t0 = time.time()
n = keep = 0
rows = []
for zn in ('au1.zip', 'au2.zip'):
    z = zipfile.ZipFile(os.path.join(RAW, zn))
    for info in z.infolist():
        f = io.TextIOWrapper(z.open(info.filename), encoding='utf-8', newline='')
        buf = ''
        while True:
            chunk = f.read(64_000_000)
            if not chunk:
                break
            buf += chunk
            last = 0
            for m in R.finditer(buf):
                last = m.end()
                s = m.group(0)
                n += 1
                a = ABN.search(s)
                if not a or a.group(1) != 'ACT':
                    continue
                e = ET.search(s)
                if not e or e.group(1) == 'IND':
                    continue
                nm = NM.search(s)
                if not nm:
                    continue
                st = ST.search(s)
                d = a.group(2)
                rows.append(('AU', a.group(3), UN.sub(lambda x: M[x.group(1)], nm.group(1)), UN.sub(lambda x: M[x.group(1)], e.group(2)), st.group(1) if st else '', st.group(2) if st else '', '%s-%s-%s' % (d[:4], d[4:6], d[6:8]), ''))
                keep += 1
            buf = buf[last:]
            db.executemany('INSERT OR REPLACE INTO wcorp VALUES (?,?,?,?,?,?,?,?)', rows)
            rows = []
        db.commit()
        print(info.filename, '全', n, '現存(個人除く)', keep, round(time.time() - t0), '秒', flush=True)
db.commit()
print('完了', n, keep, flush=True)
