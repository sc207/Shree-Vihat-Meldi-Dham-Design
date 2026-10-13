import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
WF = '*{animation:none!important;transition:none!important} html{scroll-behavior:auto!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
async def shot(b, port, board, W, H, prep, clip, big=False, dpr=1):
    ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=dpr); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(200)
    await pg.evaluate(prep); await pg.wait_for_timeout(300)
    im = Image.open(io.BytesIO(await pg.screenshot(clip=clip))).convert('RGB'); await ctx.close(); return im
def pair(a, c, title, out):
    o = Image.new('RGB', (a.width * 2 + 24, a.height + 64), 'white'); d = ImageDraw.Draw(o)
    d.text((6, 6), title, font=FB, fill=(60, 60, 60)); d.text((6, 34), 'BEFORE', font=FB, fill=(150, 20, 40)); d.text((a.width + 30, 34), 'AFTER', font=FB, fill=(20, 110, 60))
    o.paste(a, (0, 64)); o.paste(c, (a.width + 24, 64))
    if o.width > 1800: o = o.resize((1800, int(o.height * 1800 / o.width)), Image.LANCZOS)
    o.save(out, quality=86); print(out, o.size)
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        prep = "document.querySelector('.vx-days').scrollIntoView({block:'center',behavior:'instant'})"
        a = await shot(b, 8785, 'Seva', 1024, 768, prep, {'x': 0, 'y': 284, 'width': 1024, 'height': 200}); c = await shot(b, 8786, 'Seva', 1024, 768, prep, {'x': 0, 'y': 284, 'width': 1024, 'height': 200})
        pair(a, c, '6.1 · Seva 1024×768 · festival day tiles', 'work/fix/evidence/item6/ba_6_1_days_1024.jpg')
        prep = "document.querySelector('.vx-night').scrollIntoView({block:'start',behavior:'instant'})"
        a = await shot(b, 8785, 'PranPratishthaMobile', 320, 568, prep, {'x': 0, 'y': 0, 'width': 320, 'height': 500}, big=True, dpr=2); c = await shot(b, 8786, 'PranPratishthaMobile', 320, 568, prep, {'x': 0, 'y': 0, 'width': 320, 'height': 500}, big=True, dpr=2)
        pair(a, c, '6.2 · Festival phone 320 px · large text · night cards', 'work/fix/evidence/item6/ba_6_2_names_320_large.jpg')
        a = await shot(b, 8785, 'PranPratishthaMobile', 320, 568, prep, {'x': 0, 'y': 0, 'width': 320, 'height': 420}, dpr=2); c = await shot(b, 8786, 'PranPratishthaMobile', 320, 568, prep, {'x': 0, 'y': 0, 'width': 320, 'height': 420}, dpr=2)
        pair(a, c, '6.2 · Festival phone 320 px · normal text', 'work/fix/evidence/item6/ba_6_2_names_320.jpg')
        prep = "(()=>{window.scrollTo(0,0); location.hash=''; location.hash='#calendar';})()"
        a = await shot(b, 8785, 'Darshan', 1440, 900, prep, {'x': 0, 'y': 0, 'width': 1440, 'height': 300}); c = await shot(b, 8786, 'Darshan', 1440, 900, prep, {'x': 0, 'y': 0, 'width': 1440, 'height': 300})
        pair(a, c, '6.3 · Darshan 1440×900 · after the "પંચાંગ" jump link', 'work/fix/evidence/item6/ba_6_3_jump_1440.jpg')
        prep = "document.querySelector('.vm-check').scrollIntoView({block:'center',behavior:'instant'})"
        a = await shot(b, 8785, 'SevaMobile', 390, 844, prep, {'x': 0, 'y': 380, 'width': 390, 'height': 90}, dpr=3); c = await shot(b, 8786, 'SevaMobile', 390, 844, prep, {'x': 0, 'y': 380, 'width': 390, 'height': 90}, dpr=3)
        pair(a, c, '6.5 · Seva phone · consent checkbox 22 → 24 px (3x)', 'work/fix/evidence/item6/ba_6_5_checkbox.jpg')
        await b.close()
asyncio.run(main())
