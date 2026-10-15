"""Compose the four ધામ પરિવાર pictures the same way: 1200x1500 (4:5, the arch frame's shape), one warm-gold background,
a soft light behind the head, a soft ground shadow, every figure the same height on the same baseline, kept inside the arch top.
usage: python3 compose.py OUTDIR  (inputs: HD cut-outs, see SRC)"""
import os, sys
import numpy as np
from PIL import Image, ImageFilter

W, H = 1200, 1500
BASE = 0.952           # figure baseline (fraction of height)
SRC = {  # name: (RGBA cut-out, figure height fraction to aim for (capped by the arch), horizontal centre offset)
    'vihat': 'design/assets/95787e5469dde0e0ecebc09bef4a4a4a.webp',     # 21 HD cut-out, same painting as 03
    'meldi': 'design/assets/a6fe6bdb26e6dded27110709664aea5a.webp',     # 22 HD cut-out, same painting as 04
    'lakhnechi': 'tasks/deity-hd/cutouts/lakh_cut.webp',                # 05 x4 Real-ESRGAN (x4plus) + IS-Net cut-out (lossless copy)
    'goga': 'tasks/deity-hd/cutouts/goga_cut.webp',                     # 06 x4 Real-ESRGAN (x4plus) + IS-Net cut-out (lossless copy)
}
rng = np.random.default_rng(7)


def hexrgb(h): return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32)


def background(head_y):
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    top, mid, bot = hexrgb('#b9793d'), hexrgb('#ad6633'), hexrgb('#8e4c24')
    t = y / (H - 1)
    base = np.where(t[..., None] < 0.55, top + (mid - top) * (t[..., None] / 0.55), mid + (bot - mid) * ((t[..., None] - 0.55) / 0.45))
    # soft light behind the head
    cx, cy = W / 2, head_y
    r = np.sqrt(((x - cx) / (W * 0.55)) ** 2 + ((y - cy) / (W * 0.55)) ** 2)
    glow = np.clip(1 - r, 0, 1) ** 1.6
    light = hexrgb('#f6cf8a')
    img = base + (light - base) * glow[..., None] * 0.95
    # gentle vignette towards the corners
    v = np.sqrt(((x - W / 2) / (W * 0.75)) ** 2 + ((y - H * 0.45) / (H * 0.75)) ** 2)
    img *= (1 - 0.28 * np.clip(v - 0.35, 0, 1) ** 1.5)[..., None]
    img += rng.normal(0, 1.1, img.shape)          # dither so the gradient never bands
    return np.clip(img, 0, 255)


def arch_ok(alpha, ox, oy):
    """True when every opaque pixel lies inside the arch (semicircle top of radius W/2) with a 2 % margin."""
    ys, xs = np.where(alpha > 40)
    X, Y = xs + ox, ys + oy
    R = W / 2 * 0.98
    top = Y < W / 2
    inside = np.ones_like(X, bool)
    inside[top] = (X[top] - W / 2) ** 2 + (Y[top] - W / 2) ** 2 <= R ** 2
    side = (X >= W * 0.02) & (X <= W * 0.98)
    return bool(inside.all() and side.all())


def place(name, path, height_frac):
    im = Image.open(path).convert('RGBA'); a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 128); x0, y0, x1, y1 = xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    fig = im.crop((x0, y0, x1, y1)); fw, fh = fig.size
    hf = height_frac
    while True:
        th = int(H * hf); tw = int(fw * th / fh)
        small = fig.resize((tw, th), Image.LANCZOS)
        ox, oy = (W - tw) // 2, int(H * BASE) - th
        if arch_ok(np.asarray(small)[..., 3], ox, oy): return small, ox, oy, hf
        hf -= 0.005


def compose(outdir, target=0.80):
    os.makedirs(outdir, exist_ok=True)
    # one common figure height for all four: the largest that fits every figure inside the arch
    fits = {n: place(n, p, target)[3] for n, p in SRC.items()}
    common = min(fits.values()); print('arch-limited heights', {k: round(v, 3) for k, v in fits.items()}, '-> common', round(common, 3))
    for n, p in SRC.items():
        small, ox, oy, hf = place(n, p, common)
        head_y = oy + small.height * 0.16
        bg = background(head_y)
        canvas = Image.fromarray(bg.astype(np.uint8)).convert('RGBA')
        # ground shadow: soft dark ellipse under the base
        sh = Image.new('L', (W, H), 0); sa = np.zeros((H, W), np.float32)
        yy, xx = np.mgrid[0:H, 0:W]; cx, cy = W / 2, oy + small.height - 6
        e = ((xx - cx) / (small.width * 0.46)) ** 2 + ((yy - cy) / 26) ** 2
        sa = np.clip(1 - e, 0, 1) * 150
        sh = Image.fromarray(sa.astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))
        dark = Image.new('RGBA', (W, H), (60, 26, 10, 0)); dark.putalpha(sh)
        canvas.alpha_composite(dark)
        canvas.alpha_composite(small, (ox, oy))
        out = canvas.convert('RGB')
        out.save(os.path.join(outdir, f'{n}.png'))
        print(n, 'figure', small.size, 'at', (ox, oy), 'head glow y', int(head_y))


if __name__ == '__main__':
    compose(sys.argv[1] if len(sys.argv) > 1 else 'work/deity/hd')
