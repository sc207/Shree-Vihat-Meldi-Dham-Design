# Before/after sheet of the first screen (as visitors see it, animations running) at the brief's 11 screen sizes + phone landscape.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 14)
VIEWS = [(320, 568), (360, 800), (375, 812), (390, 844), (430, 932), (768, 1024), (1024, 768), (1280, 800), (1366, 768), (1440, 900), (1920, 1080), (844, 390)]
PAGES = {'Home': ('HomeMobile', 'Main'), 'NewTemple': ('NewTempleMobile', 'NewTemple'), 'PranPratishtha': ('PranPratishthaMobile', 'PranPratishtha'), 'Gallery': ('GalleryMobile', 'Gallery')}
WF = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
TH = 300
async def shot(b, port, board, W, H):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(2600)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close()
    return im.resize((int(im.width * TH / im.height), TH), Image.LANCZOS)
async def main():
    pages = sys.argv[1].split(',') if len(sys.argv) > 1 else list(PAGES)
    async with async_playwright() as p:
        b = await launch(p)
        for name in pages:
            phone, desk = PAGES[name]; cols = []
            for W, H in VIEWS:
                board = phone if W <= 760 else desk
                a = await shot(b, 8771, board, W, H); c = await shot(b, 8773, board, W, H)
                col = Image.new('RGB', (max(a.width, 120), 2 * TH + 3 * 22), 'white'); d = ImageDraw.Draw(col)
                d.text((2, 3), f'{W}x{H}', font=FB, fill=(90, 20, 35)); col.paste(a, (0, 22)); d.text((2, TH + 25), 'after', font=FB, fill=(20, 110, 60)); col.paste(c, (0, TH + 44))
                cols.append(col)
            o = Image.new('RGB', (sum(c.width + 8 for c in cols) + 70, cols[0].height), 'white'); d = ImageDraw.Draw(o)
            d.text((4, 30), 'v106', font=FB, fill=(90, 20, 35)); d.text((4, TH + 50), 'fix', font=FB, fill=(20, 110, 60)); x = 70
            for c in cols: o.paste(c, (x, 0)); x += c.width + 8
            o.save(f'work/fx/sheet_{name}.png', optimize=True); print(name, o.size, flush=True)
        await b.close()
asyncio.run(main())
