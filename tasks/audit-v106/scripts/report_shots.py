# Audit report pictures (v106 baseline, port 8771). Each picture is labelled with board, viewport and text size; red boxes mark the issue.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
PORT = 8771
OUT = 'work/audit/report/'
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
RED = (214, 32, 32)
WIDTH_FIX = '*{animation:none!important;transition:none!important} html{scroll-behavior:auto!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'

async def render(b, board, W, H, dpr=1, big=False, prep=None, boxes=(), clip=None):
    """Open board at W×H; optional prep(pg); boxes = CSS selectors (first match) to outline; clip = (x, y, w, h) in CSS px of the viewport."""
    ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=dpr)
    await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1300)
    await pg.add_style_tag(content=WIDTH_FIX % (W, W)); await pg.wait_for_timeout(300)
    if prep: await prep(pg); await pg.wait_for_timeout(400)
    rects = []
    for sel in boxes:
        r = await pg.evaluate('(s) => { const e = document.querySelector(s); if (!e) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; }', sel)
        if r: rects.append(r)
    im = Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); await ctx.close()
    d = ImageDraw.Draw(im)
    for l, t, r_, bt in rects:
        d.rectangle([l * dpr - 4 * dpr, t * dpr - 4 * dpr, r_ * dpr + 4 * dpr, bt * dpr + 4 * dpr], outline=RED, width=3 * dpr)
    if clip:
        x, y, w, h = clip; im = im.crop((x * dpr, y * dpr, (x + w) * dpr, (y + h) * dpr))
    return im

def label(im, text, width=None):
    if width and im.width != width: im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    o = Image.new('RGB', (im.width, im.height + 34), (255, 255, 255)); ImageDraw.Draw(o).text((6, 6), text, font=FB, fill=(90, 20, 35)); o.paste(im, (0, 34)); return o

def stack(ims, horizontal=False, gap=16):
    if horizontal:
        o = Image.new('RGB', (sum(i.width for i in ims) + gap * (len(ims) - 1), max(i.height for i in ims)), 'white'); x = 0
        for i in ims: o.paste(i, (x, 0)); x += i.width + gap
    else:
        o = Image.new('RGB', (max(i.width for i in ims), sum(i.height for i in ims) + gap * (len(ims) - 1)), 'white'); y = 0
        for i in ims: o.paste(i, (0, y)); y += i.height + gap
    return o

def save(im, name):
    im.save(OUT + name, optimize=True); print(name, im.size, flush=True)

async def main():
    async with async_playwright() as p:
        b = await launch(p)
        # 1 — P1 header menu button without action (desktop/tablet pages, 761–1179 px)
        a = await render(b, 'Main', 1024, 768, boxes=['.vm-menu-btn'], clip=(0, 0, 1024, 120))
        c = await render(b, 'HomeTablet', 834, 1112, boxes=['.vm-menu-btn'], clip=(0, 0, 834, 120))
        e = await render(b, 'Darshan', 900, 900, boxes=['.vm-menu-btn'], clip=(0, 0, 900, 120))
        f = await render(b, 'Main', 1180, 800, boxes=['.vm-nav'], clip=(0, 0, 1180, 120))
        save(stack([label(a, 'Main · 1024×768 · menu button (red) does nothing; no page links in the header'),
                    label(c, 'HomeTablet · 834 px (tablet board) · same button, same result'),
                    label(e, 'Darshan · 900 px (every inner desktop page between 761 and 1179 px)'),
                    label(f, 'For comparison: Main · 1180 px · the page links appear only from 1180 px')]), '01_menu_button.png')
        # 2 — P2 home hero: first button label clipped at 320 px
        prep = lambda pg: pg.evaluate("document.querySelector('.vx-home-hero .vm-btn-row').scrollIntoView({block:'center',behavior:'instant'})")
        a = await render(b, 'HomeMobile', 320, 568, dpr=2, prep=prep, boxes=['.vx-home-hero .vm-btn'], clip=(0, 234, 320, 100))
        c = await render(b, 'HomeMobile', 360, 640, dpr=2, prep=prep, clip=(0, 270, 360, 100))
        save(stack([label(a, 'HomeMobile · 320×568 · first button: first letter cut at the left edge (red)', 720),
                    label(c, 'HomeMobile · 360×640 · fits, with little side room', 720)]), '02_home_button_320.png')
        # 3 — P2 phone menu screen: close always goes to the home page; "મુખ્ય પૃષ્ઠ" always marked as current
        a = await render(b, 'MenuMobile', 390, 844, boxes=['.vm-mnav__close', '.vm-mnav a[aria-current="page"], a[aria-current="page"]'], clip=(0, 0, 390, 300), dpr=2)
        save(label(a, 'MenuMobile · 390×844 · close goes to Home; Home always current', 780), '03_menu_close.png')
        # 4 — first screen on phones: how much of the temple shows above the bottom bar
        tiles = []
        for W, H in ((360, 640), (390, 664), (360, 780), (390, 844)):
            im = await render(b, 'HomeMobile', W, H)
            tiles.append(label(im, f'{W}×{H}'))
        save(stack(tiles, horizontal=True), '04_home_first_screen_phones.png')
        tiles = []
        for W, H in ((390, 664), (390, 844)):
            im = await render(b, 'PranPratishthaMobile', W, H)
            tiles.append(label(im, f'{W}×{H}'))
        save(stack(tiles, horizontal=True), '04b_festival_first_screen_phones.png')
        # 5 — P3 Seva desktop 1024: the 8th day tile sits alone on a second row
        prep = lambda pg: pg.evaluate("[...document.querySelectorAll('button,label')].find(e => /સોમવાર/.test(e.textContent) && e.getBoundingClientRect().width < 200).scrollIntoView({block:'center',behavior:'instant'})")
        a = await render(b, 'Seva', 1024, 768, prep=prep, clip=(0, 205, 1024, 300))
        save(label(a, 'Seva · 1024×768 · the 8th day tile (8 Feb, Monday) wraps onto its own row'), '05_seva_days_1024.png')
        # 6 — P3 festival night artists at 320 px with large text
        prep = lambda pg: pg.evaluate("document.querySelector('.vx-night__who').scrollIntoView({block:'center',behavior:'instant'})")
        a = await render(b, 'PranPratishthaMobile', 320, 568, dpr=2, big=True, prep=prep, boxes=['.vx-night__who'])
        save(label(a, 'PranPratishthaMobile · 320×568 · large text · names wrap', 640), '06_night_names_320_big.png')
        # 7 — P3 in-page jump lands with the heading touching the top edge
        async def jump(pg):
            await pg.evaluate("location.hash = '#calendar'")
        a = await render(b, 'Darshan', 1440, 900, prep=jump, clip=(0, 0, 1440, 260))
        save(label(a, 'Darshan · 1440×900 · after the calendar jump link: heading flush with the top edge'), '07_darshan_jump.png')
        await b.close()
asyncio.run(main())
