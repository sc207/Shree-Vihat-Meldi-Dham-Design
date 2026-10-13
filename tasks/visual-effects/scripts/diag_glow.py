# Diagnostic sheet: which glow is where? normal render vs. only the section-background glow vs. only the halo element.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
OUT = sys.argv[2] if len(sys.argv) > 2 else 'work/fx/diag_glow.png'
BOARD = sys.argv[3] if len(sys.argv) > 3 else 'PranPratishtha'
WF = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
BG_ONLY = '.vm-hero__halo{visibility:hidden!important}'
HALO_ONLY = '.vm-hero{background:radial-gradient(ellipse 120% 90% at 50% 110%, #5a1428 0%, rgba(90,20,40,0) 60%), linear-gradient(180deg, #2a0913 0%, var(--burgundy) 55%, #3b0c1b 100%)!important}'
async def shot(b, W, H, extra):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{BOARD}.dc.html'); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=WF % (W, W) + extra); await pg.wait_for_timeout(2600)   # animations keep running, as for a visitor
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    async with async_playwright() as p:
        b = await launch(p); rows = []
        for W, H in ((768, 1024), (1024, 768)):
            tiles = []
            for lab, ex in (('as visitors see it', ''), ('section background glow only', BG_ONLY), ('halo element only', HALO_ONLY)):
                im = await shot(b, W, H, ex); s = 360 / im.height; im = im.resize((int(im.width * s), 360), Image.LANCZOS)
                t = Image.new('RGB', (max(im.width, 250), 386), 'white'); ImageDraw.Draw(t).text((2, 4), f'{W}x{H} · {lab}', font=FB, fill=(90, 20, 35)); t.paste(im, (0, 26)); tiles.append(t)
            row = Image.new('RGB', (sum(t.width for t in tiles) + 24, 386), 'white'); x = 0
            for t in tiles: row.paste(t, (x, 0)); x += t.width + 12
            rows.append(row)
        o = Image.new('RGB', (max(r.width for r in rows), sum(r.height for r in rows) + 10), 'white'); y = 0
        for r in rows: o.paste(r, (0, y)); y += r.height + 10
        o.save(OUT); print(OUT, o.size); await b.close()
asyncio.run(main())
