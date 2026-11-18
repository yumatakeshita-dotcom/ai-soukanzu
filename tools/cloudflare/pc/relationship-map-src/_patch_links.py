p = 'build_hub2.py'
s = open(p, encoding='utf-8').read()
a = "mL = {'lecun': [['個人サイト', 'https://yann.lecun.com']], 'friedman': [['個人サイト', 'https://nat.org']]}"
assert a in s
add = """from newco_data7c import LINKS as _IL
mL = {'lecun': [['個人サイト', 'https://yann.lecun.com']], 'friedman': [['個人サイト', 'https://nat.org']],
      'instagram': _IL['instagram'], 'systrom': _IL['systrom'], 'krieger': _IL['krieger'], 'mosseri': _IL['mosseri'], 'zuckerberg': _IL['zuckerberg'],
      'whatsapp': [['出典: Wikipedia(WhatsApp)', 'https://en.wikipedia.org/wiki/WhatsApp']]}"""
s = s.replace(a, add, 1)
open(p, 'w', encoding='utf-8').write(s)
p = 'newco_data7c.py'
s = open(p, encoding='utf-8').read()
s = s.replace("2012年の増資(約5,000万ドル、評価額約5億ドル)の出資者として報じられています。", "2012年4月の増資(約5,000万ドル、評価額約5億ドル)を主導したと報じられています(買収発表の直前)。")
s = s.replace("2012年の増資の出資者として報じられています。'", "2012年4月の増資の出資者として報じられています。'")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
