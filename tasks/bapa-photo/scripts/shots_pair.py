"""Before/after pictures of whole sections that hold the portrait (home pair + strip, History ch.3, Gallery banner).
usage: python3 shots_pair.py BASE_PORT NEW_PORT OUTDIR"""
import asyncio, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
from _common import FIX, clock_script, launch
from playwright.async_api import async_playwright
BASE, NEW, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
SHOTS = [('Main', 1440, '.vx-duo'), ('Main', 390, '.vx-duo'), ('HomeTablet', 834, '.vx-duo'), ('Main', 1440, '.vx-strip'),
         ('HomeMobile2', 390, '.vx-strip'), ('History', 1440, '#ch3'), ('HistoryMobile', 390, '#ch3'), ('Gallery', 1440, '.vm-hero'),
         ('GalleryMobile', 390, '.vm-hero')]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        br = await launch(p)
        for board, W, sel in SHOTS:
            for tag, port in (('before', BASE), ('after', NEW)):
                ctx = await br.new_context(viewport={'width': W, 'height': 900}, device_scale_factor=2 if W <= 430 else 1)
                await ctx.add_init_script(clock_script('2026-10-14T12:00:00+05:30'))
                pg = await ctx.new_page()
                await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (port, board)); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
                el = pg.locator(sel).first
                await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(900)
                await el.screenshot(path='%s/%s_%d_%s_%s.png' % (OUT, board, W, sel.strip('.#'), tag))
                await ctx.close()
        await br.close()
asyncio.run(main())
