# -*- coding: utf-8 -*-
"""品質チェックの「問題」を、取り込みで自動の保留にするための共通の判定(2026/11/21追加)。

- 判定だけをする小さな部品。inbox/ のファイルは読むだけで、書き換えも削除もしない
- 保留 = サイトに取り込まない(finds.js・相関図・幹部の年表に足さない)。元のファイルは inbox/ にそのまま残る
- 保留の理由: 出典(src)が無い/URLが不正、日付の書式が読めない(月だけ・年だけの日付は可)、日付が未来(明日より先)
- 次の日に判定し直すので、未来の日付だったものは日付が来れば自動で取り込まれる(直したファイルも同じ)
- 品質チェック係(quality_check.py)の「問題」と同じ決まり。merge_inbox.py・finds_map.py・exectl_auto.py が使う
"""
import datetime, os, re

JST = datetime.timezone(datetime.timedelta(hours=9))


def today_jst():
    return datetime.datetime.now(JST).date()


def parse_date(s):
    """YYYY-MM-DD(先頭10文字)。YYYY-MM と YYYY は「月だけ・年だけ」の日付として、その月・年の1日で読む。それ以外は None"""
    s = str(s).strip()
    try:
        if re.match(r'^\d{4}-\d{2}-\d{2}', s):
            return datetime.date.fromisoformat(s[:10])
        m = re.match(r'^(\d{4})(?:-(\d{2}))?$', s)
        if m:
            return datetime.date(int(m.group(1)), int(m.group(2) or 1), 1)
    except ValueError:
        return None
    return None


def has_src(it):
    for s in it.get('src') or []:
        if isinstance(s, (list, tuple)) and len(s) >= 2 and str(s[1]).startswith('http'):
            return True
        if isinstance(s, str) and s.startswith('http'):
            return True
    return False


def hold_reason(it, today=None):
    """保留にする理由(日本語の短い文)。問題がなければ None"""
    today = today or today_jst()
    if not has_src(it):
        return '出典(src)が無い、またはURLが http で始まらない'
    raw = it.get('date')
    if raw not in (None, ''):
        d = parse_date(raw)
        if d is None:
            return f'日付の書式が読めない(YYYY-MM-DD・YYYY-MM・YYYY のどれか): {raw}'
        if d > today + datetime.timedelta(days=1):
            return f'日付が先(未来): {d}'
    return None
