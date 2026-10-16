"""Photographic finish for a smoothed portrait, after the same HD step as સુરેશબાપા's photos (Real-ESRGAN x4plus, halved to exactly 2×).
Adds only what a camera photo has and the smoothed file lost — no new features:
  - clarity: gentle large-radius local contrast (brings out the wrinkles and folds that are already in the picture)
  - fine monochrome grain on skin and cloth (real sensor texture instead of the plastic look); the background glow keeps less grain
usage: python3 photo_finish.py SRC.png X4PLUS.png OUT_BASENAME [clarity] [grain]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
src = Image.open(sys.argv[1]).convert('RGB'); up = Image.open(sys.argv[2]).convert('RGB'); OUT = sys.argv[3]
CL = float(sys.argv[4]) if len(sys.argv) > 4 else 0.35; GR = float(sys.argv[5]) if len(sys.argv) > 5 else 3.0
W, H = src.size
hd = up.resize((W * 2, H * 2), Image.LANCZOS)
a = np.asarray(hd).astype(np.float32)
# clarity: unsharp mask with a large radius on luminance only
lum = a.mean(2)
blur = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32)
detail = lum - blur
mid = np.clip(1 - np.abs(lum - 128) / 128, 0, 1)                 # mid-tones (skin, folds) get it, pure whites and darks less
a = a + (CL * detail * mid)[..., None]
# grain: fine, monochrome, stronger where the picture has subject detail than on the smooth glow
rng = np.random.default_rng(5)
n = rng.normal(0, 1, (H * 2, W * 2)).astype(np.float32)
n = np.asarray(Image.fromarray(np.clip(n * 40 + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) - 128
n = n / (n.std() + 1e-6)
edge = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.FIND_EDGES).filter(ImageFilter.GaussianBlur(25))).astype(np.float32)
subj = np.clip(edge / 12.0, 0.35, 1.0)
a = a + (GR * n * subj)[..., None]
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
out.save(OUT + '.png'); out.save(OUT + '.webp', quality=90, method=6)
print(OUT, out.size)
