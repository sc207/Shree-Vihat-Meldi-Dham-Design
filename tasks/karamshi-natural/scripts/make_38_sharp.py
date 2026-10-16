"""Image 39 = 38 with the blessing hand (and, lightly, the face) in focus, exported at full 2× like સુરેશબાપા's 34.
  1. Real-ESRGAN x4plus output halved with Lanczos to exactly 2× the original (same HD step as 32–34 and 38)
  2. hand, rings and wrist only (soft mask limited to skin + rings, hand_focus.hand_mask): edge contrast restored with two unsharp radii (1.2 px creases,
     3 px outlines; amounts 0.9 / 1.3); every pixel stays within its 9×9 neighbourhood's own min/max (±1), so edges get steeper but no rims
     or halos appear (limiting the mask to skin removed a light rim round the thumb and fingertips). Result: hand detail 12.7 vs face 13.8 (Laplacian mean at 2×; 38: 4.1 vs 9.7), finger outline twice as steep (74 vs 36);
     1.2 / 1.6 looked crunchy on the palm, 0.7 / 1.1 a little soft
  2b. owner, after seeing the hand: "as like blessing hand also focus on face" — the face was already the sharpest part (HF/MF focus ratio
     eyes 0.56, face 0.63; hand 0.40 → 0.56 after step 2; turban 0.52 and checked by eye: crisp, left alone). Same method on a face mask
     (face, eyes, moustache, ears and ear-rings) at a light 0.4 / 0.9: eyes, brows and moustache crisper; 0.9 / 1.3 made the skin crackle harsh
  3. the same photographic finish as 38 (photo_finish.py: clarity 0.45 on mid-tones, fine monochrome grain, same seed); grain 2.6 because the
     file is no longer shrunk to 1.5× afterwards (38: 3.2, then ×0.75)
usage: python3 make_38_sharp.py SRC.png X4PLUS.png OUT_BASENAME [fine] [outline] [grain] [face_fine] [face_outline]"""
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter, minimum_filter, maximum_filter
sys.path.insert(0, __import__('os').path.dirname(__file__))
from hand_focus import hand_mask, face_mask

src = Image.open(sys.argv[1]).convert('RGB'); up = Image.open(sys.argv[2]).convert('RGB'); OUT = sys.argv[3]
FINE = float(sys.argv[4]) if len(sys.argv) > 4 else 0.9
OUTL = float(sys.argv[5]) if len(sys.argv) > 5 else 1.3
GR = float(sys.argv[6]) if len(sys.argv) > 6 else 2.6
FF = float(sys.argv[7]) if len(sys.argv) > 7 else 0.4
FO = float(sys.argv[8]) if len(sys.argv) > 8 else 0.9
CL = 0.45
W, H = src.size
hd = up.resize((W * 2, H * 2), Image.LANCZOS)
a = np.asarray(hd).astype(np.float32)

# 2. hand (and face) in focus
def focus(a, m, fine, outl):
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    d = fine * (lum - gaussian_filter(lum, 1.2)) + outl * (lum - gaussian_filter(lum, 3.0))
    new = np.clip(lum + d * m, minimum_filter(lum, 9) - 1, maximum_filter(lum, 9) + 1)
    return np.clip(a + (new - lum)[..., None], 0, 255)
a = focus(a, hand_mask(hd.size, rgb=a), FINE, OUTL)
if FF or FO:
    a = focus(a, face_mask(hd.size), FF, FO)

# 3. photographic finish (as photo_finish.py)
lum = a.mean(2)
blur = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32)
mid = np.clip(1 - np.abs(lum - 128) / 128, 0, 1)
a = a + (CL * (lum - blur) * mid)[..., None]
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
