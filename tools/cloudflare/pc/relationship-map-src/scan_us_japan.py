"""米国の取引所(Nasdaq・NYSE・OTCなど)に上場している会社のうち、本社(事業所の住所)が日本のものを、SEC EDGAR の公開データ(submissions)から探す。
SECの規則(1秒に10回まで)を守って、0.2秒おきに取る。途中から再開できる。Claude不要。
出力: us_japan_scan.json  {CIK: {name, ticker, exchange, sic, sicDesc, city, website, state, fy}}  (本社が日本のものだけ) と、調べ済みの一覧 us_japan_done.json
使い方: python -u scan_us_japan.py"""
import json, os, sys, time, urllib.request
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
S = os.path.dirname(os.path.abspath(__file__))
UA = {'User-Agent': 'relationship-map-research/1.0 (personal use)', 'Accept': 'application/json'}
OUT = os.path.join(S, 'us_japan_scan.json')
DONE = os.path.join(S, 'us_japan_done2.json')
d = json.load(open(os.path.join(S, 'sec_tickers.json'), encoding='utf-8'))
rows = [r for r in d['data'] if r[3] in ('Nasdaq', 'NYSE', 'OTC', 'CBOE', 'TXSE', None)]
found = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
done = set(json.load(open(DONE, encoding='utf-8'))) if os.path.exists(DONE) else set()
n = 0
for cik, name, ticker, ex in rows:
    if cik in done:
        continue
    url = 'https://data.sec.gov/submissions/CIK%010d.json' % cik
    j = None
    for i in range(4):
        try:
            j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
            break
        except Exception as e:
            if '404' in str(e):
                break
            time.sleep(3 * (i + 1))
    if j:
        biz = (j.get('addresses') or {}).get('business') or {}
        mail = (j.get('addresses') or {}).get('mailing') or {}
        _txt = ' '.join(str(x) for a in (biz, mail) for x in a.values()).upper()
        _jp_city = any(c in _txt for c in ('TOKYO', 'OSAKA', 'NAGOYA', 'YOKOHAMA', 'FUKUOKA', 'KYOTO', 'KOBE', 'SAPPORO', 'SENDAI', 'HIROSHIMA', 'JAPAN', 'CHIYODA', 'MINATO-KU', 'SHIBUYA', 'SHINJUKU', 'CHUO-KU'))
        _phone = str(j.get('phone') or '').replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
        if biz.get('stateOrCountry') == 'M0' or mail.get('stateOrCountry') == 'M0' or _jp_city or _phone.startswith('81'):      # M0 = 日本
            found[str(cik)] = {'name': j.get('name') or name, 'ticker': ticker, 'exchange': ex, 'sic': j.get('sic'), 'sicDesc': j.get('sicDescription'), 'city': biz.get('city') or mail.get('city'),
                               'street': biz.get('street1') or '', 'website': j.get('website') or '', 'fy': j.get('fiscalYearEnd'), 'tickers': j.get('tickers'), 'exchanges': j.get('exchanges'), 'forms': (j.get('filings', {}).get('recent', {}).get('form') or [])[:5]}
            print('○', name, ticker, ex, biz.get('city'), flush=True)
    done.add(cik)
    n += 1
    if n % 200 == 0:
        json.dump(found, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
        json.dump(sorted(done), open(DONE, 'w', encoding='utf-8'))
        print('進み', len(done), '/', len(rows), '日本本社', len(found), flush=True)
    time.sleep(0.2)
json.dump(found, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(sorted(done), open(DONE, 'w', encoding='utf-8'))
print('完了', len(found), flush=True)
