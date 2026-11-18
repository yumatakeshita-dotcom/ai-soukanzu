"""金額の『ドル』表記のあとに、日本円の換算を(約…円)で足す。換算レートは RATE の1か所だけで決める。
 対象: 『約36億ドル』『最大95億ドル』『80〜100億ドル』『3,500万ドル』『$12.93bn』『$915m』『$0.7 million』など。すでに円が続いているものは足さない。"""
import re

RATE = 158      # 1ドル=158円(2026年の日本語報道で使われていた換算レート。参考値)


def _fmt(yen):
    if yen >= 1e12:
        v = yen / 1e12
        return ('%.1f' % v).rstrip('0').rstrip('.') + '兆円' if v < 10 else '%d兆円' % round(v)
    if yen >= 1e8:
        v = yen / 1e8
        if v >= 100:
            n = int(round(v))
            d = len(str(n)) - 3
            if d > 0:
                n = int(round(n, -d))      # 有効数字3桁に丸める(5,688億円 → 5,690億円)
            return '{:,}億円'.format(n)
        return ('%.1f' % v).rstrip('0').rstrip('.') + '億円'
    return '{:,}万円'.format(int(round(yen / 1e4)))


_U = {'兆': 1e12, '億': 1e8, '万': 1e4}
_JP = re.compile(r'(?P<pre>約|最大|最低|およそ)?(?P<a>\d[\d,]*(?:\.\d+)?)(?:[〜~～](?P<b>\d[\d,]*(?:\.\d+)?))?(?P<u>兆|億|万)ドル(?P<suf>超|以上|規模|前後|台|程度)?')
_PL = re.compile(r'\$(?P<a>\d{1,3}(?:,\d{3})+)(?![\d,]*\s?(?:bn|billion|B|m|M|million))')
_EN = re.compile(r'\$(?P<a>\d[\d,]*(?:\.\d+)?)(?:&nbsp;|\s)?(?P<u>bn|billion|B|m|M|million)\b(?P<suf>\+)?')


def _num(x):
    return float(x.replace(',', ''))


def yenify(s):
    if not isinstance(s, str) or ('ドル' not in s and '$' not in s):
        return s

    def jp(m):
        rest = s[m.end():m.end() + 2]
        if rest.startswith('(約') or rest.startswith('（約') or rest.startswith('円'):
            return m.group(0)
        u = _U[m.group('u')]
        lo = _num(m.group('a')) * u * RATE
        txt = _fmt(lo)
        if m.group('b'):
            txt = _fmt(lo) .replace('円', '') + '〜' + _fmt(_num(m.group('b')) * u * RATE)
        return m.group(0) + '(約' + txt + ')'

    def en(m):
        rest = s[m.end():m.end() + 2]
        if rest.startswith('(約') or rest.startswith('（約'):
            return m.group(0)
        mult = 1e9 if m.group('u').lower() in ('bn', 'billion', 'b') else 1e6
        return m.group(0) + '(約' + _fmt(_num(m.group('a')) * mult * RATE) + ')'
    s2 = _JP.sub(jp, s)
    s3 = _EN.sub(en, s2)

    def pl(m):
        rest = s3[m.end():m.end() + 2]
        if rest.startswith('(約') or rest.startswith('（約'):
            return m.group(0)
        return m.group(0) + '(約' + _fmt(_num(m.group('a')) * RATE) + ')'
    return _PL.sub(pl, s3)


if __name__ == '__main__':
    for t in ['約36億ドル', '最大95億ドル(前払い91億ドル)', '80〜100億ドル(協議中)', '3,500万ドル', '$12.93bn', '$915m', '$0.7 million', '4億ドル超(株式)', '約2兆円', '約141〜142億ドル(約2兆円)', '1.45億ドルの融資', '$60bn']:
        print(t, '=>', yenify(t))
