# Audit Phase A — pictures: first screen (header + hero) per page at 6 widths; full-page thumbnails; flagged components.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
PORT = 8771
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
PAGES = [('Home', 'HomeMobile', 'Main'), ('NewTemple', 'NewTempleMobile', 'NewTemple'), ('PranPratishtha', 'PranPratishthaMobile', 'PranPratishtha'),
         ('Seva', 'SevaMobile', 'Seva'), ('Gallery', 'GalleryMobile', 'Gallery'), ('History', 'HistoryMobile', 'History'),
         ('Contact', 'ContactMobile', 'Contact'), ('Darshan', 'DarshanMobile', 'Darshan'), ('NotFound', 'NotFoundMobile', 'NotFound')]
VIEWS = [(320, 640), (390, 844), (768, 1024), (1024, 768), (1440, 900), (1920, 1080)]
STYLE = '*{animation:none!important;transition:none!important}'


async def open_page(b, board, W, H):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1300)
    await pg.add_style_tag(content=STYLE + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W))
    await pg.wait_for_timeout(300)
    return ctx, pg


async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for name, phone, desk in PAGES:
            tiles = []
            for W, H in VIEWS:
                ctx, pg = await open_page(b, phone if W <= 760 else desk, W, H)
                im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close()
                tiles.append((f'{W}×{H}', im))
            # sheet: scale each to height 420
            th = 420; scaled = [(l, im.resize((int(im.width * th / im.height), th), Image.LANCZOS)) for l, im in tiles]
            Wt = sum(i.width for _, i in scaled) + 12 * (len(scaled) - 1); o = Image.new('RGB', (Wt, th + 30), 'white'); d = ImageDraw.Draw(o); x = 0
            for l, i in scaled:
                d.text((x + 2, 4), l, font=F, fill=(90, 20, 35)); o.paste(i, (x, 30)); x += i.width + 12
            o.save(f'work/audit/hero_{name}.png', optimize=True); print('hero sheet', name, o.size, flush=True)
            # full-page thumbnails at 390 and 1440
            for W, board in ((390, phone), (1440, desk)):
                ctx, pg = await open_page(b, board, W, 900)
                im = Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); await ctx.close()
                im.save(f'work/audit/full_{board}_{W}.png'); print('full', board, W, im.size, flush=True)
        await b.close()

asyncio.run(main())
