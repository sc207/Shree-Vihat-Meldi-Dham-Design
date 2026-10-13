# Diagnostic only: ornaments made 5x stronger and pictures hidden, so the chakra drawing itself can be compared before/after.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
WF = '*{animation:none!important} html{scroll-behavior:auto!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important} svg.vm-mandala{opacity:.45!important} svg.vm-cta__orn{opacity:.6!important} .vm-section img{visibility:hidden}'
CASES = [('HomeMobile', 390, 844, '.vm-section--inverse:has(svg.vm-mandala)'), ('Main', 1440, 900, '.vm-section--inverse:has(svg.vm-mandala)'),
         ('NewTempleMobile', 390, 844, '.vm-cta'), ('PranPratishtha', 1440, 900, '.vm-cta')]
async def shot(b, port, board, W, H, sel):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(200)
    await pg.evaluate("(s) => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top - 20, behavior: 'instant'}); }", sel)
    await pg.wait_for_timeout(300); im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    rows = []
    async with async_playwright() as p:
        b = await launch(p)
        for board, W, H, sel in CASES:
            a = await shot(b, 8771, board, W, H, sel); c = await shot(b, 8774, board, W, H, sel)
            k = 420 / a.height; a = a.resize((int(a.width * k), 420)); c = c.resize((int(c.width * k), 420))
            r = Image.new('RGB', (a.width * 2 + 16, 446), 'white'); d = ImageDraw.Draw(r)
            d.text((2, 4), f'v106 {board} {W}', font=FB, fill=(150, 20, 40)); d.text((a.width + 18, 4), 'new chakra', font=FB, fill=(20, 110, 60))
            r.paste(a, (0, 26)); r.paste(c, (a.width + 16, 26)); rows.append(r)
        await b.close()
    o = Image.new('RGB', (max(r.width for r in rows), sum(r.height + 10 for r in rows)), 'white'); y = 0
    for r in rows: o.paste(r, (0, y)); y += r.height + 10
    o.save('work/chakra/diag_strong.png'); print(o.size)
asyncio.run(main())
