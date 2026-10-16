"""Gallery viewer behaviour (v131): focus to ✕ on open, Tab stays inside, Escape closes and returns focus to the photo, click on the dark
area closes, click on the photo does not, ✕ closes; page does not jump. usage: python3 test_viewer_keys.py PORT"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT = int(sys.argv[1])
async def main():
    fails = 0; total = 0
    async with async_playwright() as p:
        br = await launch(p)
        for b, W, H in (('Gallery', 1440, 900), ('Gallery', 1024, 768), ('GalleryMobile', 390, 844), ('GalleryMobile', 320, 568)):
            ctx = await br.new_context(viewport={'width': W, 'height': H})
            await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True))
            pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
            await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(1000); await pg.add_style_tag(content=FIX)
            btns = pg.locator('.vm-gallery figure button'); n = await btns.count()
            async def st():
                return await pg.evaluate('''() => ({open: !!document.querySelector('.vx-lb'), act: (document.activeElement.className || '') + '|' + (document.activeElement.getAttribute('aria-label') || ''), y: Math.round(scrollY)})''')
            for i in (0, n // 2, n - 1):
                await pg.evaluate('(i) => document.querySelectorAll(".vm-gallery figure button")[i].scrollIntoView({block: "center", behavior: "instant"})', i)
                await pg.wait_for_timeout(200); lab = await btns.nth(i).get_attribute('aria-label')
                res = {}
                await btns.nth(i).click(force=True); await pg.wait_for_timeout(250); s = await st(); y0 = s['y']
                res['click opens, ✕ focused'] = s['open'] and s['act'].startswith('vx-lb__close')
                await pg.keyboard.press('Tab'); await pg.keyboard.press('Shift+Tab'); await pg.keyboard.press('Tab'); await pg.wait_for_timeout(80); s = await st()
                res['Tab stays on ✕'] = s['open'] and s['act'].startswith('vx-lb__close')
                await pg.keyboard.press('Escape'); await pg.wait_for_timeout(250); s = await st()
                res['Escape closes, focus back on photo'] = (not s['open']) and s['act'].endswith(lab) and abs(s['y'] - y0) <= 1
                await pg.keyboard.press('Enter'); await pg.wait_for_timeout(250); s = await st()
                res['Enter on photo opens'] = s['open'] and s['act'].startswith('vx-lb__close')
                await pg.mouse.click(6, H // 2); await pg.wait_for_timeout(250); s = await st()
                res['click on dark area closes'] = not s['open']
                await btns.nth(i).click(force=True); await pg.wait_for_timeout(250)
                bb = await pg.locator('.vx-lb__img img').bounding_box(); await pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); await pg.wait_for_timeout(200); s = await st()
                res['click on photo keeps it open'] = s['open']
                await pg.locator('.vx-lb__close').click(); await pg.wait_for_timeout(250); s = await st()
                res['✕ closes, focus back, no jump'] = (not s['open']) and s['act'].endswith(lab) and abs(s['y'] - y0) <= 1
                for k, v in res.items():
                    total += 1
                    if not v: fails += 1; print('FAIL', b, W, i, k)
            print(b, W, H, 'photos tested 3', 'js errors', len(errs), errs[:1], flush=True)
            await ctx.close()
        await br.close()
    print('checks', total, 'failed', fails)
asyncio.run(main())
