"""Compare 2x versions of a portrait: Lanczos (plain enlargement) vs the two upscalers (x4 then halved), on a face crop at 1:1,
plus a faithfulness number: shrink each 2x result back to the original size and compare with the original (PSNR, higher = closer).
usage: python3 portrait_compare.py NAME x0 y0 x1 y1   (crop box in original pixels; files work/portraits/NAME_{src,gen,x4plus}.png)"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
n = sys.argv[1]; box = tuple(int(v) for v in sys.argv[2:6])
src = Image.open(f'work/portraits/{n}_src.png'); W, H = src.size; rgb = src.convert('RGB')
cands = {'Lanczos 2x (plain)': rgb.resize((W * 2, H * 2), Image.LANCZOS)}
for k, lab in (('gen', 'general-x4v3 → 2x'), ('x4plus', 'x4plus → 2x')):
    im = Image.open(f'work/portraits/{n}_{k}.png').convert('RGB'); cands[lab] = im.resize((W * 2, H * 2), Image.LANCZOS)
a = np.asarray(rgb, np.float32)
if src.mode == 'RGBA': m = np.asarray(src.getchannel('A')) > 200
else: m = np.ones(a.shape[:2], bool)
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
crops = []
for lab, im in cands.items():
    back = np.asarray(im.resize((W, H), Image.LANCZOS), np.float32)
    mse = ((back - a) ** 2)[m].mean(); psnr = 10 * np.log10(255 ** 2 / mse)
    c = im.crop(tuple(v * 2 for v in box)); crops.append((f'{lab}  PSNR {psnr:.1f} dB', c)); print(n, lab, 'PSNR %.1f' % psnr)
cw, ch = crops[0][1].size
s = Image.new('RGB', (cw * len(crops) + 20 * (len(crops) + 1), ch + 50), 'white'); d = ImageDraw.Draw(s)
for i, (lab, c) in enumerate(crops): x = 20 + i * (cw + 20); s.paste(c, (x, 40)); d.text((x, 10), lab, fill='black', font=F)
s.save(f'work/portraits/{n}_compare.png'); print(s.size)
