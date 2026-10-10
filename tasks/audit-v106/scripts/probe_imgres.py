# Probe: image sharpness after all lazy images have loaded. scale = how much the browser enlarges the photo at 1x; x2 = on a 2x (retina/phone) screen.
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
BOARDS = [('Main', 1440), ('NewTemple', 1440), ('PranPratishtha', 1440), ('Gallery', 1440), ('History', 1440), ('Contact', 1440), ('Darshan', 1440), ('Seva', 1440),
          ('HomeMobile', 390), ('NewTempleMobile', 390), ('PranPratishthaMobile', 390), ('GalleryMobile', 390), ('HistoryMobile', 390), ('DarshanMobile', 390), ('ContactMobile', 390)]
JS = '''() => [...document.querySelectorAll('img')].filter(i => { const r = i.getBoundingClientRect(); const s = getComputedStyle(i); return r.width > 40 && s.visibility !== 'hidden' && s.display !== 'none'; }).map(i => {
  const r = i.getBoundingClientRect(), fit = getComputedStyle(i).objectFit, nw = i.naturalWidth, nh = i.naturalHeight;
  const sc = fit === 'cover' ? Math.max(r.width / nw, r.height / nh) : fit === 'contain' ? Math.min(r.width / nw, r.height / nh) : r.width / nw;
  return {src: i.getAttribute('src').slice(-32), alt: (i.alt || '').slice(0, 40), nat: [nw, nh], ren: [Math.round(r.width), Math.round(r.height)], fit, scale: +sc.toFixed(2)}; })'''
async def main():
    out = {}
    async with async_playwright() as p:
        b = await launch(p)
        for board, W in BOARDS:
            ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1200)
            await pg.add_style_tag(content='.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W))
            h = await pg.evaluate('document.documentElement.scrollHeight')
            for y in range(0, h, 500):
                await pg.evaluate(f'window.scrollTo({{top:{y},behavior:"instant"}})'); await pg.wait_for_timeout(60)
            await pg.wait_for_timeout(1000)
            rows = await pg.evaluate(JS)
            bad = [r for r in rows if r['nat'][0] and r['scale'] * 2 > 1.25]
            out[f'{board}@{W}'] = bad
            print(board, W, 'imgs', len(rows), 'soft-on-2x:', [(r['src'][:8], r['alt'][:24], r['nat'], r['ren'], r['scale']) for r in bad], flush=True)
            await ctx.close()
        await b.close()
    json.dump(out, open('work/audit/imgres.json', 'w'), ensure_ascii=False, indent=1)
asyncio.run(main())
