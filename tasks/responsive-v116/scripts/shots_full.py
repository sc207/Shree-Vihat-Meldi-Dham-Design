"""Full-page screenshots for the by-eye review, then contact sheets (page cut into columns).
usage (repo root): python3 tasks/responsive-v116/scripts/shots_full.py PORT OUTDIR [--time ISO] [--big] [--only Board@W,...]"""
import asyncio, os, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image
from _common import FIX, clock_script, launch
PORT, OUT = int(sys.argv[1]), sys.argv[2]
TIME = sys.argv[sys.argv.index('--time') + 1] if '--time' in sys.argv else '2026-10-16T12:00:00+05:30'
BIG = '--big' in sys.argv
PAGES = ['Main', 'NewTemple', 'PranPratishtha', 'Seva', 'Gallery', 'History', 'Contact', 'Darshan', 'NotFound']
SETS = [(p + 'Mobile' if p != 'Main' else 'HomeMobile', 390, 844) for p in PAGES] + [('HomeMobile2', 390, 844)] + \
       [(p, w, h) for p in PAGES for (w, h) in ((768, 1024), (1024, 768), (1440, 900))] + \
       [('HomeTablet', 834, 1194), ('HomeTabletL', 1180, 820), ('HomePhoneL', 844, 390), ('MenuMobile', 390, 844), ('OfflineMobile', 390, 844)]
if '--only' in sys.argv:
    want = sys.argv[sys.argv.index('--only') + 1].split(',')
    SETS = [(b, int(w), 900 if int(w) > 760 else 844) for b, w in (x.split('@') for x in want)]


def sheet(path, W, out):
    im = Image.open(path).convert('RGB'); H = im.height
    sh = 1500 if W <= 760 else 1100                      # slice height
    cols = (H + sh - 1) // sh
    per_row = cols if W <= 760 else 3
    rows = (cols + per_row - 1) // per_row
    gap = 16
    S = Image.new('RGB', (per_row * (W + gap), rows * (sh + gap)), (90, 90, 90))
    for i in range(cols):
        part = im.crop((0, i * sh, W, min(H, (i + 1) * sh)))
        S.paste(part, ((i % per_row) * (W + gap), (i // per_row) * (sh + gap)))
    maxw = 2400
    if S.width > maxw: S = S.resize((maxw, round(S.height * maxw / S.width)), Image.LANCZOS)
    S.save(out, quality=82)


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        br = await launch(p)
        for board, W, H in SETS:
            ctx = await br.new_context(viewport={'width': W, 'height': H})
            await ctx.add_init_script(clock_script(TIME, frozen=True, big_text=BIG))
            pg = await ctx.new_page()
            await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, board)); await pg.wait_for_timeout(1000)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
            await pg.evaluate('''async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += innerHeight) { scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 40)); } scrollTo({top: 0, behavior: 'instant'}); }''')
            await pg.wait_for_timeout(600)
            f = '%s/%s_%d%s.png' % (OUT, board, W, '_big' if BIG else '')
            await pg.screenshot(path=f, full_page=True)
            sheet(f, W, f[:-4] + '_sheet.jpg')
            print(board, W, flush=True)
            await ctx.close()
        await br.close()
asyncio.run(main())
