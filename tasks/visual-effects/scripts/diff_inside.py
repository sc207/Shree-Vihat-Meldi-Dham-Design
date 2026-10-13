# Every pixel that changed must lie inside the area where a chakra ornament is drawn (its box clipped to its section),
# apart from the known moving-ribbon noise on the home boards.
import asyncio, sys, io, os
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageChops, ImageDraw
from _common import FIX, clock_script, launch
INIT_EXTRA = 'performance.now=()=>0;Math.random=()=>0.5;'
BOARDS = [('Main', 1440), ('HomeTablet', 834), ('HomeTabletL', 1180), ('HomePhoneL', 844), ('HomeMobile', 390), ('NewTemple', 1440), ('NewTempleMobile', 390), ('PranPratishtha', 1440), ('PranPratishthaMobile', 390)]
JS = r'''() => { const out = [];
  for (const s of document.querySelectorAll('svg.vm-mandala, svg.vm-cta__orn')) { const r = s.getBoundingClientRect(); let p = s.parentElement, c = null;
    while (p) { const o = getComputedStyle(p).overflow; if (o !== 'visible') { c = p.getBoundingClientRect(); break; } p = p.parentElement; }
    const L = Math.max(r.left, c ? c.left : -1e9), T = Math.max(r.top, c ? c.top : -1e9), R = Math.min(r.right, c ? c.right : 1e9), B = Math.min(r.bottom, c ? c.bottom : 1e9);
    out.push(['orn', L, T + scrollY, R, B + scrollY]); }
  for (const s of document.querySelectorAll('.vx-marquee')) { const r = s.getBoundingClientRect(); out.push(['ribbon', r.left, r.top + scrollY, r.right, r.bottom + scrollY]); }
  return out; }'''
async def shot(b, port, name, W):
    ctx = await b.new_context(viewport={'width': W, 'height': 900}, device_scale_factor=1)
    await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', frozen=True)[:-4] + INIT_EXTRA + '})()')
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{name}.dc.html'); await pg.wait_for_timeout(1200)
    await pg.add_style_tag(content=FIX + ' *::before,*::after{animation:none!important;transition:none!important}'); await pg.wait_for_timeout(400)
    img = Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); boxes = await pg.evaluate(JS); await ctx.close(); return img, boxes
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for name, W in BOARDS:
            (a, _), (c, boxes) = await shot(b, int(sys.argv[1]), name, W), await shot(b, int(sys.argv[2]), name, W)
            diff = ImageChops.difference(a, c).convert('L').point(lambda v: 255 if v > 0 else 0)
            mask = Image.new('L', diff.size, 0); d = ImageDraw.Draw(mask)
            for kind, L, T, R, B in boxes: d.rectangle([L - 1, T - 1, R + 1, B + 1], fill=255)
            outside = ImageChops.multiply(diff, ImageChops.invert(mask))
            n_all = sum(1 for v in diff.getdata() if v); n_out = sum(1 for v in outside.getdata() if v)
            print(f'{name:22s} changed px {n_all:7d}  outside ornament/ribbon areas: {n_out}  {outside.getbbox() or ""}', flush=True)
        await b.close()
asyncio.run(main())
