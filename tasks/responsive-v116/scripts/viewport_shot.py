"""Screenshot of the real viewport (what the visitor sees) at a scroll position, with fixed/sticky elements as they behave.
usage: python3 viewport_shot.py PORT BOARD W H SCROLLY OUT.png [--big] [--time ISO] [--anim]"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, B, W, H, Y, OUT = int(sys.argv[1]), sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6]
TIME = sys.argv[sys.argv.index('--time') + 1] if '--time' in sys.argv else '2026-10-16T12:00:00+05:30'
async def main():
    async with async_playwright() as p:
        br = await launch(p)
        ctx = await br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2)
        await ctx.add_init_script(clock_script(TIME, frozen=True, big_text='--big' in sys.argv))
        pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, B)); await pg.wait_for_timeout(1200)
        css = ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W)
        await pg.add_style_tag(content=(css if '--anim' in sys.argv else FIX + css))
        y = await pg.evaluate('(y) => { let v; if (y === "end") v = document.documentElement.scrollHeight; else if (/^[#.\\[a-z]/i.test(y) && isNaN(+y)) { const [sel, off] = y.split("@"); const e = document.querySelector(sel); v = e ? e.getBoundingClientRect().top + scrollY - (+off || 0) : 0; } else v = +y; scrollTo({top: v, behavior: "instant"}); return scrollY; }', Y)
        await pg.wait_for_timeout(700)
        await pg.screenshot(path=OUT)
        print(B, W, H, 'scrollY', y)
        await br.close()
asyncio.run(main())
