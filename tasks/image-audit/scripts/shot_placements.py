"""Screenshot every place an image is drawn (its frame), at 2x. usage: python3 shot_placements.py PORT OUTDIR BOARD:WIDTH:BLOB[,...]"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, OUT, SPEC = int(sys.argv[1]), sys.argv[2], sys.argv[3]
async def main():
    async with async_playwright() as p:
        br = await launch(p)
        for item in SPEC.split(','):
            b, W, blob = item.split(':'); W = int(W)
            ctx = await br.new_context(viewport={'width': W, 'height': 900 if W > 760 else 844}, device_scale_factor=2)
            await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True))
            pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(900)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important} .vx-abar{display:none!important}' % (W, W))
            await pg.evaluate('async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += innerHeight) { scrollTo({top: y, behavior: "instant"}); await new Promise(r => setTimeout(r, 40)); } }')
            ims = pg.locator('img[src$="%s"]' % blob); n = await ims.count(); k = 0
            for i in range(n):
                im = ims.nth(i)
                if not await im.is_visible(): continue
                fr = im.locator('xpath=ancestor::*[self::figure or contains(@class,"vm-arch") or contains(@class,"vx-crop") or contains(@class,"vm-update")][1]')
                tgt = fr if await fr.count() else im
                await tgt.scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
                await tgt.screenshot(path=f'{OUT}/pl_{b}_{W}_{blob[:6]}_{k}.png'); k += 1
            print(b, W, blob[:6], k, flush=True); await ctx.close()
        await br.close()
asyncio.run(main())
