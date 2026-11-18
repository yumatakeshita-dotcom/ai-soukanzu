"""取得済みの、ノルウェー(Brønnøysund)・エストニア(e-Business Register)・フィンランド(PRH)の会社登記データから、現存する会社だけを world_more.sqlite に入れる。
(英国とフランスは world.sqlite。ロックを避けるため、別のファイルにする)  出典: NLOD(ノルウェー)・CC BY(エストニア)・PRH Open Data(フィンランド)
使い方: python -I load_world_more.py no|ee|fi"""
import csv, gzip, io, json, os, sqlite3, sys, zipfile
which = sys.argv[1]
D = os.path.join(os.path.expanduser('~'), '.claude', 'data')
RAW = os.path.join(D, 'world_raw')
db = sqlite3.connect(os.environ.get('WORLD_MORE_DB') or os.path.join(D, 'world_more.sqlite'))
db.execute('PRAGMA journal_mode=OFF')
db.execute('PRAGMA synchronous=OFF')
db.execute('CREATE TABLE IF NOT EXISTS wcorp (cc TEXT, id TEXT, name TEXT, kind TEXT, city TEXT, post TEXT, since TEXT, sic TEXT, PRIMARY KEY (cc, id))')
db.execute('DELETE FROM wcorp WHERE cc=?', (which.upper(),))
rows, keep, n = [], 0, 0


def flush():
    global rows, keep
    if rows:
        db.executemany('INSERT OR REPLACE INTO wcorp VALUES (?,?,?,?,?,?,?,?)', rows)
        keep += len(rows)
        rows = []


if which == 'no':
    rd = csv.DictReader(gzip.open(os.path.join(RAW, 'no_enheter.csv.gz'), 'rt', encoding='utf-8', newline=''))
    for r in rd:
        n += 1
        if r.get('konkurs', '').lower() == 'true' or r.get('underTvangsavviklingEllerTvangsopplosning', '').lower() == 'true' or r.get('slettedato'):
            continue
        rows.append(('NO', r['organisasjonsnummer'], r['navn'], r.get('organisasjonsform.beskrivelse', ''), r.get('forretningsadresse.poststed') or r.get('postadresse.poststed') or '',
                     r.get('forretningsadresse.postnummer') or r.get('postadresse.postnummer') or '', r.get('stiftelsesdato') or r.get('registreringsdatoenhetsregisteret') or '', r.get('naeringskode1.beskrivelse', '')[:80]))
        if len(rows) >= 50000:
            flush()
elif which == 'ee':
    z = zipfile.ZipFile(os.path.join(RAW, 'ee_basic.zip'))
    t = io.TextIOWrapper(z.open(z.infolist()[0].filename), encoding='utf-8-sig', newline='')
    for r in csv.DictReader(t, delimiter=';'):
        n += 1
        if r.get('ettevotja_staatus') != 'R':
            continue
        d = r.get('ettevotja_esmakande_kpv', '')
        since = '%s-%s-%s' % (d[6:10], d[3:5], d[0:2]) if len(d) == 10 else d
        rows.append(('EE', r['ariregistri_kood'], r['nimi'], r.get('ettevotja_oiguslik_vorm', ''), r.get('asukoha_ehak_tekstina', ''), r.get('indeks_ettevotja_aadressis', ''), since, ''))
        if len(rows) >= 50000:
            flush()
else:
    z = zipfile.ZipFile(os.path.join(RAW, 'fi_all.zip'))
    f = io.TextIOWrapper(z.open(z.infolist()[0].filename), encoding='utf-8', newline='')
    dec = json.JSONDecoder()
    buf = ''
    pos = 0
    started = False
    eof = False
    SKIP = ' ' + chr(13) + chr(10) + chr(9) + ','
    while True:
        if len(buf) - pos < 4_000_000 and not eof:
            chunk = f.read(32_000_000)
            if not chunk:
                eof = True
            buf = buf[pos:] + chunk
            pos = 0
        while pos < len(buf) and buf[pos] in SKIP:
            pos += 1
        if not started:
            if pos < len(buf) and buf[pos] == '[':
                pos += 1
                started = True
                continue
            if eof:
                break
            continue
        if pos >= len(buf) or buf[pos] == ']':
            if eof or pos < len(buf):
                break
            continue
        try:
            o, end = dec.raw_decode(buf, pos)
        except json.JSONDecodeError:
            if eof:
                break
            chunk = f.read(32_000_000)
            if not chunk:
                eof = True
            buf = buf[pos:] + chunk
            pos = 0
            continue
        pos = end
        n += 1
        reg = [e for e in (o.get('registeredEntries') or []) if str(e.get('type')) == '1']
        if not reg or any(e.get('endDate') for e in reg[-1:]):      # 現存(登録が終了していない)ものだけ
            continue
        names = [x for x in (o.get('names') or []) if not x.get('endDate')] or (o.get('names') or [])
        if not names:
            continue
        ad = next((a for a in (o.get('addresses') or []) if a.get('type') == 1), (o.get('addresses') or [{}])[0] if o.get('addresses') else {})
        city = next((p.get('city') for p in (ad.get('postOffices') or []) if str(p.get('languageCode')) == '1'), '') or ''
        form = next((d.get('description') for d in ((o.get('companyForms') or [{}])[0].get('descriptions') or []) if str(d.get('languageCode')) == '3'), '') or ''
        sic = next((d.get('description') for d in ((o.get('mainBusinessLine') or {}).get('descriptions') or []) if str(d.get('languageCode')) == '3'), '') or ''
        rows.append(('FI', (o.get('businessId') or {}).get('value', ''), names[0].get('name', ''), form, city, ad.get('postCode') or '', (o.get('businessId') or {}).get('registrationDate') or '', sic[:80]))
        if len(rows) >= 50000:
            flush()
            if n % 500000 < 50000:
                print('読み込み', n, flush=True)
flush()
db.commit()
print('完了', which.upper(), '全', n, '現存', keep, flush=True)
