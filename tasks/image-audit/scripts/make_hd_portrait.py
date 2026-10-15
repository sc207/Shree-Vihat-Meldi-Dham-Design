"""HD portrait = Real-ESRGAN x4plus result (x4) halved with Lanczos -> exactly 2x the original. Alpha (cut-outs): the original alpha enlarged 2x
with Lanczos. Saves PNG (master) + WebP q90 method 6. usage: python3 make_hd_portrait.py SRC.png X4PLUS.png OUT_BASENAME"""
import sys
import numpy as np
from PIL import Image
src = Image.open(sys.argv[1]); up = Image.open(sys.argv[2]).convert('RGB'); out = sys.argv[3]
W, H = src.size
rgb = up.resize((W * 2, H * 2), Image.LANCZOS)
if src.mode == 'RGBA':
    a = src.getchannel('A').resize((W * 2, H * 2), Image.LANCZOS)
    res = rgb.convert('RGBA'); res.putalpha(a)
else:
    res = rgb
res.save(out + '.png')
res.save(out + '.webp', quality=90, method=6, **({'exact': False} if res.mode == 'RGBA' else {}))
print(out, res.size, res.mode)
