"""Open gallery photos in the viewer at several screen sizes; check the panel is fully on screen and measure the photo.
usage: python3 test_viewer.py PORT OUTDIR [--shots]"""
import asyncio, json, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, OUT = int(sys.argv[1]), sys.argv[2]
CFG = [('Gallery', 1920, 1080), ('Gallery', 1440, 900), ('Gallery', 1280, 720), ('Gallery', 1024, 768), ('Gallery', 834, 1194), ('Gallery', 844, 390),
       ('GalleryMobile', 430, 932), ('GalleryMobile', 390, 844), ('GalleryMobile', 360, 780), ('GalleryMobile', 320, 568), ('GalleryMobile', 667, 375)]
async def main():
    res = []
    async with async_playwright() as p:
        br = await launch(p)
        for b, W, H in CFG:
            for big in (False, True):
                ctx = await br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2)
                await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True, big_text=big))
                pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content=FIX)
                n = await pg.locator('.vm-gallery figure button').count()
                for i in range(n):
                    await pg.evaluate('(i) => { const b = document.querySelectorAll(".vm-gallery figure button")[i]; b.scrollIntoView({block: "center", behavior: "instant"}); b.click(); }', i); await pg.wait_for_timeout(600)
                    r = await pg.evaluate('''() => { const bx = document.querySelector('.vx-lb__box').getBoundingClientRect(); const im = document.querySelector('.vx-lb__img img').getBoundingClientRect();
                        const cl = document.querySelector('.vx-lb__close').getBoundingClientRect(); const lb = document.querySelector('.vx-lb'); const img = document.querySelector('.vx-lb__img img');
                        return {box: [bx.left, bx.top, bx.right, bx.bottom].map(Math.round), img: [Math.round(im.width), Math.round(im.height)], nat: [img.naturalWidth, img.naturalHeight],
                                close: [Math.round(cl.top), Math.round(cl.bottom)], scroll: lb.scrollHeight > lb.clientHeight + 1, vw: innerWidth, vh: innerHeight}; }''')
                    vis = r['box'][1] >= 0 and r['box'][3] <= r['vh'] and r['box'][0] >= 0 and r['box'][2] <= r['vw']
                    closeVis = r['close'][0] >= 0 and r['close'][1] <= r['vh']
                    r.update(board=b, W=W, H=H, big=big, i=i, panel_on_screen=vis, close_on_screen=closeVis); res.append(r)
                    if '--shots' in sys.argv and not big and i in (1, n - 1): await pg.screenshot(path=f'{OUT}/vw_{b}_{W}x{H}_{i}.png')
                    await pg.evaluate('() => document.querySelector(".vx-lb__close").click()'); await pg.wait_for_timeout(150)
                await ctx.close()
                bad = [x for x in res if x['W'] == W and x['H'] == H and x['big'] == big and x['board'] == b and not (x['panel_on_screen'] and x['close_on_screen'])]
                print(b, W, H, 'big' if big else 'std', 'photos', n, 'panel off screen:', len(bad), 'photo size e.g.', res[-1]['img'], flush=True)
        await br.close()
    json.dump(res, open(f'{OUT}/viewer.json', 'w'), indent=0)
asyncio.run(main())
