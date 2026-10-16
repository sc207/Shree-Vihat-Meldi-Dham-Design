"""ભગવાન શ્રી કરમશીબાપા — natural photo for the arch frames (replaces 27, which came smoothed / AI-looking).
Source: image 08 (genuine photograph, 1000×1497, white background) — no AI enlargement, no face retouching.
1. cut-out: IS-Net mask (tasks/deity-hd/scripts/cutout.py)
2. white balance of the HIGHLIGHTS only (whites were blue: median 195/203/252): gains fade in from mid-tones, skin unchanged
3. warm golden glow background matched to સુરેશબાપા's photo (34); figure 3:4, turban near the top, shoulders fading into the glow at the photo's cut edges
usage: python3 compose_karamshi.py CUT_RGBA.png OUT_BASENAME [scale] [top_frac]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
cut = Image.open(sys.argv[1]).convert('RGBA'); OUT = sys.argv[2]
S = float(sys.argv[3]) if len(sys.argv) > 3 else 1.32; TOP = float(sys.argv[4]) if len(sys.argv) > 4 else 0.085
W, H = 1500, 2000
rng = np.random.default_rng(11)
a = np.asarray(cut).astype(np.float32); rgb, al = a[..., :3], a[..., 3]
# 2. highlight white balance
lum = rgb.mean(2) / 255.0
w = np.clip((lum - 0.30) / 0.45, 0, 1); w = w * w * (3 - 2 * w)                       # from dark mid-tones to highlights
blue = np.clip((rgb[..., 2] - (rgb[..., 0] + rgb[..., 1]) / 2) / 25.0, 0, 1)           # only where blue dominates (the cloth's cast)
w = w * blue
src = np.array([195., 203., 252.]); dst = np.array([241., 234., 224.])
g = dst / src
rgb = rgb * (1 + w[..., None] * (g - 1))
rgb = np.clip(rgb, 0, 255)
# figure geometry in the source
ys, xs = np.where(al > 128); top_src = ys.min()
rows = (al[top_src + 120: top_src + 260] > 128); cols = np.where(rows.any(0))[0]; cx_src = (cols.min() + cols.max()) / 2   # turban centre
fig = Image.fromarray(np.dstack([rgb, al]).astype(np.uint8), 'RGBA')
fw, fh = int(fig.width * S), int(fig.height * S); fig = fig.resize((fw, fh), Image.LANCZOS)
ox = int(W / 2 - cx_src * S); oy = int(H * TOP - top_src * S)
# fade the figure where the source photo was cut (left, right, bottom edges)
fa = np.asarray(fig).astype(np.float32)[..., 3]
yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
F = 220.0
d = np.minimum(np.minimum(xx, fw - 1 - xx), fh - 1 - yy)       # distance to a cut edge (top is not a cut)
fade = np.clip(d / F, 0, 1); fade = fade * fade * (3 - 2 * fade)
fa = fa * fade
fig = Image.fromarray(np.dstack([np.asarray(fig)[..., :3], fa]).astype(np.uint8), 'RGBA')
# 3. background glow (colours sampled from 34)
y, x = np.mgrid[0:H, 0:W].astype(np.float32)
hx, hy = W / 2, H * (TOP + 0.13)
r = np.sqrt(((x - hx) / (W * 0.62)) ** 2 + ((y - hy) / (W * 0.62)) ** 2)
c0, c1, c2 = np.array([250., 214., 140.]), np.array([196., 143., 78.]), np.array([108., 66., 36.])
t = np.clip(r, 0, 1.6) / 1.6
bg = np.where(t[..., None] < 0.45, c0 + (c1 - c0) * (t[..., None] / 0.45), c1 + (c2 - c1) * ((t[..., None] - 0.45) / 0.55))
# bright halo behind the head (as in 34)
hr = np.sqrt(((x - hx) / (W * 0.34)) ** 2 + ((y - H * (TOP + 0.12)) / (W * 0.34)) ** 2)
halo = np.clip(1 - hr, 0, 1) ** 1.4
bg = bg + (np.array([253., 231., 168.]) - bg) * (halo * 0.85)[..., None]
haze = np.array([238., 219., 186.])
hz = np.clip((y / H - 0.50) / 0.45, 0, 1); hz = hz * hz * (3 - 2 * hz)                  # lower half → cream haze
side = np.clip(1 - np.abs(x - W / 2) / (W * 0.62), 0, 1) ** 0.6                          # strongest under the figure
bg = bg + (haze - bg) * (hz * (0.28 + 0.55 * side))[..., None]
bg += rng.normal(0, 1.2, bg.shape)
canvas = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).convert('RGBA')
canvas.alpha_composite(fig, (ox, oy)) if ox >= 0 and oy >= 0 else canvas.paste(fig, (ox, oy), fig)
out = canvas.convert('RGB')
out.save(OUT + '.png'); out.save(OUT + '.webp', quality=90, method=6)
print('scale', S, 'figure', fw, fh, 'at', ox, oy, '-> canvas', W, H)
