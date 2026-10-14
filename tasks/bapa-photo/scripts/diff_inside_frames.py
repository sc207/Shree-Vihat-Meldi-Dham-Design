"""Full-page compare v109 vs working copy; count changed pixels OUTSIDE the new photo's frames (must be 0).
usage: python3 diff_inside_frames.py BASE_PORT NEW_PORT BLOBID"""
import asyncio, io, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
from _common import FIX, clock_script, launch
from playwright.async_api import async_playwright
BASE, NEW, BLOB = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
CASES = [('Main', 1440), ('Main', 390), ('HomeTablet', 834), ('HomeTabletL', 1180), ('HomePhoneL', 844), ('HomeMobile2', 390),
         ('History', 1440), ('HistoryMobile', 390), ('Gallery', 1440), ('GalleryMobile', 390)]
async def shot(br, port, board, W, rects=False):
    ctx = await br.new_context(viewport={'width': W, 'height': 900})
    await ctx.add_init_script(clock_script('2026-10-14T12:00:00+05:30'))
    pg = await ctx.new_page()
    await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (port, board)); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important} img{transition:none!important}' % (W, W))
    await pg.evaluate('''async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 30)); } scrollTo({top: 0, behavior: 'instant'}); }''')
    await pg.wait_for_timeout(800)
    png = await pg.screenshot(full_page=True)
    rs = await pg.evaluate('''(b) => [...document.querySelectorAll('img')].filter(i => i.src.includes(b)).map(i => { const r = i.closest('figure,.vm-arch').getBoundingClientRect(); return [r.left, r.top + scrollY, r.right, r.bottom + scrollY]; })''', BLOB) if rects else []
    await ctx.close()
    return np.asarray(Image.open(io.BytesIO(png)).convert('RGB'), dtype=np.int16), rs
async def main():
    bad = 0
    async with async_playwright() as p:
        br = await launch(p)
        for board, W in CASES:
            a, _ = await shot(br, BASE, board, W); b, rs = await shot(br, NEW, board, W, True); a2, _ = await shot(br, BASE, board, W)
            if a.shape != b.shape: print(board, W, 'SIZE DIFFERS', a.shape, b.shape); bad += 1; continue
            m = (np.abs(a - b).max(axis=2) > 8)
            # noise = what differs between two loads of the SAME base page (moving text band); excluded, with a 6 px margin
            noise = ndimage.binary_dilation(np.abs(a - a2).max(axis=2) > 8, iterations=6) if a2.shape == a.shape else np.zeros_like(m)
            m &= ~noise
            inside = np.zeros_like(m)
            for x0, y0, x1, y1 in rs:   # frame + 2 px for the anti-aliased edge
                inside[max(0, int(y0) - 2):int(y1) + 3, max(0, int(x0) - 2):int(x1) + 3] = True
            out = int((m & ~inside).sum())
            print('%-14s %5d  frames %d  changed px %7d  outside frames %d  (noise px masked %d)' % (board, W, len(rs), int(m.sum()), out, int(noise.sum())))
            if out:   # where are they?
                lab, n = ndimage.label(ndimage.binary_dilation(m & ~inside, iterations=4))
                print('      outside boxes:', ['x %d-%d y %d-%d' % (q[1].start, q[1].stop, q[0].start, q[0].stop) for q in ndimage.find_objects(lab)][:8])
            bad += out > 0
        await br.close()
    print('RESULT:', 'OK - all changes inside the photo frames' if not bad else 'CHECK %d case(s)' % bad)
asyncio.run(main())
