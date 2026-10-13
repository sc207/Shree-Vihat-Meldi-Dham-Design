import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 17)
WF = '*{animation:none!important;transition:none!important} html{scroll-behavior:auto!important}'
async def run(b, port, W, H, valid):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{"Seva" if W > 760 else "SevaMobile"}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF)
    if valid:
        await pg.fill('#f-name', 'રમેશભાઈ પટેલ'); await pg.fill('#f-mob', '98765 43210'); await pg.fill('#f-city', 'સાણંદ'); await pg.click('#f-agree, .vm-check input')
    else:
        await pg.fill('#f-name', 'રમેશભાઈ પટેલ')
    btn = pg.locator('button', has_text='નોંધણી પૂર્ણ કરો').last; await btn.scroll_into_view_if_needed(); await btn.click(); await pg.wait_for_timeout(800)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close(); return im
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for W, H, valid, name, lab in ((390, 844, False, 'missing_fields_390', 'mobile + town missing, submit'), (390, 844, True, 'valid_390', 'all filled, submit'),
                                       (1440, 900, False, 'missing_fields_1440', 'mobile + town missing, submit')):
            a = await run(b, 8782, W, H, valid); c = await run(b, 8783, W, H, valid)
            o = Image.new('RGB', (W * 2 + 24, H + 64), 'white'); d = ImageDraw.Draw(o)
            d.text((6, 6), (f'SevaMobile {W}x{H}' if W < 760 else f'Seva {W}x{H}') + ' · ' + lab, font=FB, fill=(60, 60, 60)); d.text((6, 32), 'BEFORE', font=FB, fill=(150, 20, 40)); d.text((W + 30, 32), 'AFTER', font=FB, fill=(20, 110, 60))
            o.paste(a, (0, 64)); o.paste(c, (W + 24, 64))
            if o.width > 1800: o = o.resize((1800, int(o.height * 1800 / o.width)), Image.LANCZOS)
            o.save(f'work/fix/evidence/item3/ba_{name}.jpg', quality=85); print(name, o.size, flush=True)
        await b.close()
asyncio.run(main())
