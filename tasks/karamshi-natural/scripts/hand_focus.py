"""Bring the blessing hand of 38 into the same focus as the face — no new features, only edge contrast that is already there.
Halo-free unsharp mask on luminance (each pixel clamped to its 9×9 neighbourhood's own min/max ±1, so edges get steeper without
bright/dark rims), two radii (1.2 px creases + 3 px finger outlines), applied inside a soft mask around the hand, rings and wrist, limited to skin and rings.
Tried and rejected: Richardson–Lucy deconvolution (dark rims round the fingers), x4plus on a pre-shrunk hand (smoother, lost creases).
usage: python3 hand_focus.py IN_2x.png OUT.png [fine_amount] [outline_amount]   (make_38_sharp.py does the whole 39 build)
Coordinates are in the 2× image (2172×2896) of the 1086×1448 original."""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy.ndimage import gaussian_filter, minimum_filter, maximum_filter

def hand_mask(size, feather=45, rgb=None):
    """Soft ellipses round the hand, rings and wrist. With rgb (the 2× picture as a float array) the mask is also limited to skin and the
    two rings, so the gold background and the white cloth beside the hand are never changed (without this a light rim appeared round the
    thumb and fingertips)."""
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    d.ellipse((200, 1170, 660, 1780), fill=255)          # fingers and rings
    d.ellipse((210, 1400, 810, 2140), fill=255)          # palm and thumb
    d.ellipse((250, 1850, 720, 2260), fill=255)          # wrist
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(feather))).astype(np.float32) / 255
    if rgb is None:
        return m
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    skin = np.clip((B - 92) / 16, 0, 1) * np.clip((R - B - 35) / 25, 0, 1) * np.clip((R - G - 25) / 20, 0, 1)
    skin = minimum_filter(maximum_filter(skin, 9), 9)    # closing: keep the darker palm creases inside the mask
    skin = gaussian_filter(skin, 1.0)
    r = Image.new('L', size, 0); d = ImageDraw.Draw(r)
    d.ellipse((230, 1595, 345, 1685), fill=255); d.ellipse((310, 1525, 425, 1620), fill=255)   # the two rings
    r = np.asarray(r.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255
    return m * np.maximum(skin, r)


def face_mask(size, feather=45):
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    d.ellipse((780, 780, 1540, 1640), fill=255)          # face, eyes, moustache, chin
    d.ellipse((690, 990, 860, 1210), fill=255)           # left ear and ear-ring
    d.ellipse((1390, 990, 1560, 1210), fill=255)         # right ear and ear-ring
    return np.asarray(m.filter(ImageFilter.GaussianBlur(feather))).astype(np.float32) / 255

def usm(lum, radius, amount):
    return amount * (lum - gaussian_filter(lum, radius))

def focus(a, mask, fine=0.9, mid=1.3):
    lum = (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]).astype(np.float32)
    d = usm(lum, 1.2, fine) + usm(lum, 3.0, mid)
    new = lum + d * mask
    lo, hi = minimum_filter(lum, 9), maximum_filter(lum, 9)
    new = np.clip(new, lo - 1, hi + 1)                    # no halos
    return np.clip(a + (new - lum)[..., None], 0, 255)

if __name__ == '__main__':
    im = Image.open(sys.argv[1]).convert('RGB')
    fine = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
    mid = float(sys.argv[4]) if len(sys.argv) > 4 else 1.3
    a = np.asarray(im).astype(np.float32)
    out = focus(a, hand_mask(im.size, rgb=a), fine, mid)
    Image.fromarray(out.astype(np.uint8)).save(sys.argv[2]); print(sys.argv[2], im.size)
