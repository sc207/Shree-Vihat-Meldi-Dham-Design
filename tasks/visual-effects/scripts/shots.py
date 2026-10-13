# Before (v106, 8771) / after (chakra copy, 8774) pictures of every place the old chakra was used.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
WF = '*{animation:none!important;transition:none!important} html{scroll-behavior:auto!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
CASES = [  # board, W, H, selector to bring into view, out name
  ('HomeMobile', 390, 844, '.vm-section--inverse:has(svg.vm-mandala)', 'home_390'),
  ('Main', 1440, 900, '.vm-section--inverse:has(svg.vm-mandala)', 'home_1440'),
  ('HomeTablet', 834, 1112, '.vm-section--inverse:has(svg.vm-mandala)', 'hometablet_834'),
  ('HomeTabletL', 1180, 820, '.vm-section--inverse:has(svg.vm-mandala)', 'hometabletl_1180'),
  ('HomePhoneL', 844, 390, '.vm-section--inverse:has(svg.vm-mandala)', 'homephonel_844'),
  ('NewTemple', 1440, 900, '.vm-cta', 'newtemple_cta_1440'),
  ('NewTempleMobile', 390, 844, '.vm-cta', 'newtemple_cta_390'),
  ('PranPratishtha', 1440, 900, '.vm-cta', 'festival_cta_1440'),
  ('PranPratishthaMobile', 390, 844, '.vm-cta', 'festival_cta_390'),
]
async def shot(b, port, board, W, H, sel):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(1100)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(250)
    await pg.evaluate("(s) => { const e = document.querySelector(s); const r = e.getBoundingClientRect(); window.scrollTo({top: scrollY + r.top - 40, behavior: 'instant'}); }", sel)
    await pg.wait_for_timeout(500)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for board, W, H, sel, name in CASES:
            a = await shot(b, 8771, board, W, H, sel); c = await shot(b, 8774, board, W, H, sel)
            o = Image.new('RGB', (a.width * 2 + 20, a.height + 34), 'white'); d = ImageDraw.Draw(o)
            d.text((4, 6), f'BEFORE v106 · {board} {W}x{H}', font=FB, fill=(150, 20, 40)); d.text((a.width + 24, 6), f'AFTER · new chakra', font=FB, fill=(20, 110, 60))
            o.paste(a, (0, 34)); o.paste(c, (a.width + 20, 34))
            if o.width > 1800: o = o.resize((1800, int(o.height * 1800 / o.width)), Image.LANCZOS)
            o.save(f'work/chakra/ba_{name}.png'); print(name, o.size, flush=True)
        await b.close()
asyncio.run(main())
