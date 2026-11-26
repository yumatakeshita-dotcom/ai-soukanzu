#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""顔写真を足す(権利を確かめられたものだけ)。2026/11/25追加。足すだけ(すでにある写真は触らない)。

人物の英語名 → Wikidata(英語版Wikipediaのページ名から)の画像(P18) → Wikimedia Commons の記載(ライセンス・作者)を読み、
自由に使えるライセンス(パブリックドメイン・CC0・CC BY・CC BY-SA)の写真だけ、240pxの縮小版を site/faces.json に足し、
docs/photo_rights/photo_licenses.json に権利の記録を足す(あとで python3 scripts/make_photo_credits.py)。
ライセンスが読めない・NC/ND・非自由・画像が無いものは足さず、理由を表示する。画像は他の場所へ転載しない(このサイトの中だけ)。
使い方: python3 scripts/person_photo.py "Jack Ma" "Daniel Ek" ... [--wiki タイトル] [--dry-run]
  Wikipediaのページ名が英語名と違う人は 名前=ページ名 で書く(例: "Parker Harris=Parker_Harris_(businessman)")
Wikimedia は回数制限が厳しい(429)。間をあけて、curl で取る。
"""
import argparse, base64, json, os, re, subprocess, sys, time, urllib.parse, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FACES = os.path.join(ROOT, 'site', 'faces.json')
LIC = os.path.join(ROOT, 'docs', 'photo_rights', 'photo_licenses.json')
UA = 'ai-soukanzu-research/1.0 (personal research project)'
OK = re.compile(r'^(CC0|Public domain|PD|CC BY(-SA)? \d\.\d|CC BY(-SA)? \d\.\d \w+)$', re.I)


def get(url, binary=False, tries=6):
    for i in range(tries):
        r = subprocess.run(['curl', '-s', '-m', '40', '-A', UA, '-w', '\n%{http_code}', url], capture_output=True)
        body, _, code = r.stdout.rpartition(b'\n')
        if code.strip() == b'200':
            return body if binary else body.decode('utf-8', 'replace')
        time.sleep(8 * (i + 1) if code.strip() == b'429' else 3)
    return None


def j(url):
    t = get(url)
    return json.loads(t) if t else None


def strip(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s or '')).strip()


def find(en, title):
    w = j('https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&format=json&props=claims&titles=' + urllib.parse.quote(title))
    if not w:
        return None, '通信できず'
    ent = next(iter(w.get('entities', {}).values()), {})
    q = ent.get('id', '')
    cl = ent.get('claims', {}).get('P18')
    if not cl:
        return None, '画像(P18)なし'
    fn = cl[0]['mainsnak']['datavalue']['value']
    time.sleep(2)
    c = j('https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo&iiprop=extmetadata|url&iiurlwidth=240&titles=' + urllib.parse.quote('File:' + fn))
    if not c:
        return None, 'Commonsに通信できず'
    pg = next(iter(c['query']['pages'].values()))
    ii = (pg.get('imageinfo') or [{}])[0]
    m = ii.get('extmetadata', {})
    lic = strip(m.get('LicenseShortName', {}).get('value'))
    if m.get('NonFree', {}).get('value') in ('true', True) or m.get('Restrictions', {}).get('value'):
        return None, '非自由・使用制限あり(%s)' % m.get('Restrictions', {}).get('value')
    if not OK.match(lic):
        return None, 'ライセンスが範囲外・読めない(%s)' % lic
    return dict(q=q, file=fn, lic=lic, licurl=strip(m.get('LicenseUrl', {}).get('value')), artist=strip(m.get('Artist', {}).get('value'))[:160],
                src='https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(fn.replace(' ', '_'), safe='_(),'), thumb=ii.get('thumburl')), ''


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('names', nargs='+'); ap.add_argument('--dry-run', action='store_true'); a = ap.parse_args()
    faces = json.load(open(FACES, encoding='utf-8')); rows = json.load(open(LIC, encoding='utf-8'))
    today = time.strftime('%Y/%m/%d', time.gmtime(time.time() + 9 * 3600))
    for arg in a.names:
        en, _, title = arg.partition('=')
        title = (title or en).replace(' ', '_')
        if en in faces:
            print('%-22s すでに写真あり(触らない)' % en); continue
        info, why = find(en, title)
        if not info:
            print('%-22s 足さない: %s' % (en, why)); continue
        time.sleep(3)
        img = get(info['thumb'], binary=True) if info['thumb'] else None
        if not img or img[:2] != b'\xff\xd8':
            print('%-22s 足さない: 画像を取れない/JPEGでない' % en); continue
        print('%-22s 足す: %s / %s / 作者 %s' % (en, info['file'], info['lic'], info['artist'][:40]))
        if a.dry_run:
            continue
        faces[en] = {'i': 'data:image/jpeg;base64,' + base64.b64encode(img).decode(), 's': 'Wikimedia Commons', 'u': info['src'], 'q': info['q'],
                     'note': '%s 経歴の薄い人物に追加(Commonsの記載で %s を確認)' % (today, info['lic'])}
        rows.append({'set': 'faces.json', 'key': en, 'name': en, 'ja': '', 'q': info['q'], 'cat': 'ok' if re.match(r'(CC0|Public|PD)', info['lic'], re.I) else 'credit',
                     'lic': info['lic'], 'licurl': info['licurl'], 'artist': info['artist'], 'file': info['file'], 'src': info['src'], 'restr': '', 'nfiles': 1,
                     'why': today + ' 追加', 'origsrc': 'Wikimedia Commons(Wikidata P18)'})
        time.sleep(3)
    if not a.dry_run:
        json.dump(faces, open(FACES, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
        json.dump(rows, open(LIC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
