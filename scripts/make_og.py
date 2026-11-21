"""共有カード用の画像 site/og.png(1200x630)を作る。サイトの色(相関図の変数と同じ)を使う。
使い方: python3 scripts/make_og.py   (Pillow が要る)"""
import os, math
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
W, H = 1200, 630
BG, SURF, FG, MUTED, LINE = '#11151a', '#1a2027', '#e8ecf0', '#97a3b0', '#2e3741'
ACTIVE, INVEST, DEAL, LEFT = '#2fc2ab', '#8394f5', '#e6b84a', '#f09a55'
def font(sz, bold=False):
    for p in ['/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
# 右側の相関図(飾り)
nodes = {'OpenAI': (860, 190, 26, FG), 'Nvidia': (1040, 330, 26, DEAL), 'Anthropic': (790, 380, 22, FG),
         'TSMC': (1010, 500, 22, ACTIVE), 'Microsoft': (680, 230, 18, INVEST), 'ASML': (880, 540, 16, MUTED),
         'Google': (1100, 160, 16, INVEST), 'Amazon': (650, 470, 16, LEFT)}
edges = [('OpenAI', 'Nvidia', INVEST), ('Nvidia', 'TSMC', DEAL), ('Anthropic', 'Amazon', INVEST), ('Microsoft', 'OpenAI', INVEST),
         ('OpenAI', 'Anthropic', LEFT), ('Nvidia', 'Anthropic', INVEST), ('TSMC', 'ASML', DEAL), ('Google', 'OpenAI', LEFT), ('Google', 'Nvidia', ACTIVE)]
nodes = {k: (int(740 + (x - 650) * 0.78), y, r, c) for k, (x, y, r, c) in nodes.items()}
for a, b, c in edges: d.line([nodes[a][:2], nodes[b][:2]], fill=c, width=4)
f = font(22)
for n, (x, y, r, c) in nodes.items():
    d.ellipse([x-r, y-r, x+r, y+r], fill=c, outline=BG, width=5)
    tw = d.textlength(n, font=f); d.text((x - tw/2, y + r + 8), n, font=f, fill=MUTED)
# 左側の文字
d.rectangle([0, 0, 12, H], fill=ACTIVE)
d.text((70, 150), 'AI企業の相関図', font=font(84), fill=FG)
d.text((74, 270), '人・出資・取引・移籍のつながりを出典つきで', font=font(30), fill=MUTED)
d.text((74, 325), 'OpenAI / Anthropic / NVIDIA / TSMC ほか', font=font(28), fill=MUTED)
for i, (c, t) in enumerate([(INVEST, '出資'), (DEAL, '取引'), (LEFT, '移籍'), (ACTIVE, '提携')]):
    x = 76 + i * 130
    d.ellipse([x, 440, x+22, 462], fill=c); d.text((x+32, 434), t, font=font(28), fill=FG)
d.text((74, 540), '毎朝更新', font=font(26), fill=ACTIVE)
im.save(os.path.join(ROOT, 'site', 'og.png'), optimize=True)
print('書き出し: site/og.png', os.path.getsize(os.path.join(ROOT, 'site', 'og.png')) // 1024, 'KB')
