"""Open every gallery photo in the viewer (lightbox) and measure how big it is drawn. usage: python3 measure_lightbox.py PORT OUTDIR"""
import asyncio, json, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, OUT = int(sys.argv[1]), sys.argv[2]
async def main():
    res = []
    async with async_playwright() as p:
        br = await launch(p)
        for board, W, H, dpr in (('Gallery', 1440, 900, 2), ('GalleryMobile', 390, 844, 3)):
            ctx = await br.new_context(viewport={'width': W, 'height': H})
            await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True))
            pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, board)); await pg.wait_for_timeout(1000)
            await pg.add_style_tag(content=FIX)
            n = await pg.locator('.vm-gallery figure button').count()
            for i in range(n):
                b = pg.locator('.vm-gallery figure button').nth(i); cap = await b.get_attribute('aria-label')
                await b.scroll_into_view_if_needed(); await b.click(); await pg.wait_for_timeout(500)
                r = await pg.evaluate('''() => { const im = document.querySelector('.vx-lb__img img'); if (!im) return null; const q = im.getBoundingClientRect();
                    return {src: im.src.split('/_blob/')[1], nw: im.naturalWidth, nh: im.naturalHeight, w: Math.round(q.width), h: Math.round(q.height)}; }''')
                if r:
                    r.update(board=board, cap=cap, sharp=round(r['nw'] / (r['w'] * dpr), 2)); res.append(r); print(r, flush=True)
                    if i < 12: await pg.locator('.vx-lb__box').screenshot(path=f'{OUT}/lb_{board}_{i:02d}.png')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
                if await pg.locator('.vx-lb__close').count() and await pg.locator('.vx-lb__close').first.is_visible(): await pg.locator('.vx-lb__close').first.click(); await pg.wait_for_timeout(200)
            await ctx.close()
        await br.close()
    json.dump(res, open(f'{OUT}/lightbox.json', 'w'), ensure_ascii=False, indent=0)
asyncio.run(main())
