# Evidence: tapping ☰ before (v109 + stage 1: nothing happens) and after (stage 2: menu panel), at tablet / small-laptop / phone-landscape sizes.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
WF = '*{animation:none!important;transition:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
async def shot(b, port, board, W, H, big=False):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(200)
    await pg.click('.vm-menu-btn'); await pg.wait_for_timeout(250)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for board, W, H, name, big in (('Seva', 768, 1024, 'seva_768', False), ('Main', 1024, 768, 'main_1024', False), ('PranPratishtha', 1179, 820, 'festival_1179', False), ('HomePhoneL', 844, 390, 'homephonel_844', False), ('Darshan', 900, 1200, 'darshan_900_big', True)):
            a = await shot(b, 8781, board, W, H, big); c = await shot(b, 8782, board, W, H, big)
            o = Image.new('RGB', (W * 2 + 24, H + 40), 'white'); d = ImageDraw.Draw(o)
            d.text((6, 8), f'BEFORE · tap ☰ · {board} {W}x{H}' + (' · large text' if big else ''), font=FB, fill=(150, 20, 40)); d.text((W + 30, 8), 'AFTER · tap ☰ opens the menu', font=FB, fill=(20, 110, 60))
            o.paste(a, (0, 40)); o.paste(c, (W + 24, 40))
            if o.width > 1800: o = o.resize((1800, int(o.height * 1800 / o.width)), Image.LANCZOS)
            o.save(f'work/fix/evidence/item2/ba_{name}.jpg', quality=85); print(name, o.size, flush=True)
        await b.close()
asyncio.run(main())
