# Full-page pictures for the visual review, cut into screen-height pieces (several pieces side by side per picture for narrow widths).
import asyncio, sys, io, os, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
OUTD = sys.argv[2] if len(sys.argv) > 2 else 'work/review'
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
PAGES = [('Home', 'HomeMobile', 'Main'), ('NewTemple', 'NewTempleMobile', 'NewTemple'), ('PranPratishtha', 'PranPratishthaMobile', 'PranPratishtha'),
         ('Seva', 'SevaMobile', 'Seva'), ('Gallery', 'GalleryMobile', 'Gallery'), ('History', 'HistoryMobile', 'History'),
         ('Contact', 'ContactMobile', 'Contact'), ('Darshan', 'DarshanMobile', 'Darshan'), ('NotFound', 'NotFoundMobile', 'NotFound')]
EXTRA = [('Home', 'HomeMobile2', 390, 844), ('Menu', 'MenuMobile', 390, 844), ('Offline', 'OfflineMobile', 390, 844), ('Home', 'HomeTablet', 834, 1112), ('Home', 'HomeTabletL', 1180, 820), ('Home', 'HomePhoneL', 844, 390)]
VIEWS = [(390, 844, 3), (768, 1024, 2), (1024, 768, 1), (1440, 900, 1)]   # (width, height, pieces per picture)
WF = 'html{scroll-behavior:auto!important} *{animation:none!important;transition:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
async def capture(b, page, board, W, H, per, index):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(900)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(300)
    h = await pg.evaluate('document.documentElement.scrollHeight')
    for y in range(0, h, 600): await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(40)
    await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(700)
    im = Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); await ctx.close()
    pieces = [im.crop((0, y, W, min(y + H, im.height))) for y in range(0, im.height, H)]
    n = 0
    for i in range(0, len(pieces), per):
        grp = pieces[i:i + per]; o = Image.new('RGB', (per * W + (per - 1) * 16, H + 30), (255, 255, 255)); d = ImageDraw.Draw(o)
        for j, pc in enumerate(grp):
            x = j * (W + 16); o.paste(pc, (x, 30)); d.text((x + 4, 6), f'{board} {W}x{H} · y {(i + j) * H}–{(i + j) * H + pc.height}', font=FB, fill=(150, 20, 40))
        if o.width > 1600: o = o.resize((1600, int(o.height * 1600 / o.width)), Image.LANCZOS)
        n += 1; fn = f'{OUTD}/{page}/{board}_{W}_{n:02d}.jpg'; os.makedirs(os.path.dirname(fn), exist_ok=True); o.save(fn, quality=86)
        index.setdefault(page, []).append(fn)
    print(board, W, 'height', h, 'pictures', n, flush=True)
async def main():
    index = {}
    async with async_playwright() as p:
        b = await launch(p)
        for page, phone, desk in PAGES:
            for W, H, per in VIEWS: await capture(b, page, phone if W <= 760 else desk, W, H, per, index)
        for page, board, W, H in EXTRA: await capture(b, page, board, W, H, 3 if W < 500 else (2 if W < 900 and H > 600 else 1), index)
        await b.close()
    json.dump(index, open(f'{OUTD}/index.json', 'w'), indent=1)
asyncio.run(main())
