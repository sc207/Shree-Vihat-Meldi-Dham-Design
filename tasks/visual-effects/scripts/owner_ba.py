# Before/after of the owner's screenshot views (PranPratishtha 768x1024 and 1024x768) plus Home phone 390x844, animations running.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
WF = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
async def shot(b, port, board, W, H):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(3000)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for board, W, H, name in (('PranPratishtha', 768, 1024, 'pp_768'), ('PranPratishtha', 1024, 768, 'pp_1024'), ('HomeMobile', 390, 844, 'home_390'), ('Main', 1440, 900, 'home_1440')):
            a = await shot(b, 8771, board, W, H); c = await shot(b, 8775, board, W, H)
            o = Image.new('RGB', (W * 2 + 24, H + 40), 'white'); d = ImageDraw.Draw(o)
            d.text((6, 8), f'BEFORE · {board} {W}x{H}', font=FB, fill=(150, 20, 40)); d.text((W + 30, 8), 'AFTER · light behind Mataji', font=FB, fill=(20, 110, 60))
            o.paste(a, (0, 40)); o.paste(c, (W + 24, 40))
            if o.width > 1800: o = o.resize((1800, int(o.height * 1800 / o.width)), Image.LANCZOS)
            o.save(f'work/glow2/ba_{name}.jpg', quality=86); print(name, o.size, flush=True)
        await b.close()
asyncio.run(main())
