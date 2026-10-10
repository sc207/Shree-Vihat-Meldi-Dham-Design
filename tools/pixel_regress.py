#!/usr/bin/env python3
"""Regression: full-page screenshot of every board at its own width on two servers (baseline vs edited),
clock frozen at the same moment, and report which boards are pixel-identical.

usage: python3 tools/pixel_regress.py --base 8771 --new 8772 --project design/project [--time 2026-10-10T12:30:00+05:30]

Boards you did NOT touch must be IDENTICAL. Known noise (not a regression): the home boards' moving text ribbon
(.vx-marquee) and the darshan photo area can differ by a few pixels even between two loads of the SAME version —
confirm by running the same version on both ports. For boards you changed, a difference is expected; check it by eye.
"""
import argparse, asyncio, io, os, sys
from playwright.async_api import async_playwright
from PIL import Image, ImageChops
sys.path.insert(0, os.path.dirname(__file__))
from _common import FIX, clock_script, launch, boards

INIT_EXTRA = 'performance.now=()=>0;Math.random=()=>0.5;'


async def shot(b, port, name, W, t):
    ctx = await b.new_context(viewport={'width': W, 'height': 900}, device_scale_factor=1)
    await ctx.add_init_script(clock_script(t, frozen=True)[:-4] + INIT_EXTRA + '})()')
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{name}.dc.html'); await pg.wait_for_timeout(1200)
    await pg.add_style_tag(content=FIX); await pg.wait_for_timeout(400)
    img = Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); await ctx.close(); return img


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', type=int, required=True); ap.add_argument('--new', type=int, required=True)
    ap.add_argument('--project', required=True); ap.add_argument('--time', default='2026-10-10T12:30:00+05:30'); ap.add_argument('--boards')
    A = ap.parse_args(); want = set(A.boards.split(',')) if A.boards else None
    async with async_playwright() as p:
        b = await launch(p)
        for name, W, _ in boards(A.project):
            if want and name not in want:
                continue
            a = await shot(b, A.base, name, W, A.time); c = await shot(b, A.new, name, W, A.time)
            if a.size != c.size:
                print(f'{name:22} {W:>5}  DIFFERENT height {a.size[1]} -> {c.size[1]}', flush=True)
            else:
                bb = ImageChops.difference(a, c).getbbox()
                print(f'{name:22} {W:>5}  {"identical" if bb is None else "DIFFERENT in box " + str(bb)}', flush=True)
        await b.close()

asyncio.run(main())
