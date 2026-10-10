# Probe: how much of the hero artwork (temple / deities) is visible in the first screen, above the phone action bar, on common screen sizes.
import asyncio, sys, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image
from _common import clock_script, launch
SIZES_PH = [(320, 568), (360, 640), (375, 667), (390, 664), (360, 780), (412, 800), (390, 844), (430, 932)]
SIZES_DT = [(768, 1024), (834, 1112), (1024, 768), (1280, 720)]
PAGES = [('HomeMobile', 'Main'), ('NewTempleMobile', 'NewTemple'), ('PranPratishthaMobile', 'PranPratishtha'), ('GalleryMobile', 'Gallery')]
JS = '''() => { const vh = innerHeight; let bar = vh; for (const e of document.querySelectorAll('body *')) { const s = getComputedStyle(e); if ((s.position === 'fixed' || s.position === 'sticky') && s.display !== 'none' && s.visibility !== 'hidden') { const r = e.getBoundingClientRect(); if (r.bottom >= vh - 1 && r.top > vh / 2 && r.width > innerWidth * 0.6) bar = Math.min(bar, r.top); } }
  const hero = document.querySelector('.vm-hero'); const imgs = [...hero.querySelectorAll('img')].filter(i => { const r = i.getBoundingClientRect(); return r.width > 80 && getComputedStyle(i).display !== 'none'; });
  const art = imgs.map(i => { const r = i.getBoundingClientRect(); const vis = Math.max(0, Math.min(r.bottom, bar) - Math.max(r.top, 0)); return {alt: (i.alt || '').slice(0, 18), top: Math.round(r.top), bottom: Math.round(r.bottom), visPct: Math.round(100 * vis / r.height)}; });
  const btn = [...hero.querySelectorAll('.vm-btn')].map(b => Math.round(b.getBoundingClientRect().bottom));
  const h1 = hero.querySelector('h1').getBoundingClientRect();
  return {bar: Math.round(bar), h1: [Math.round(h1.top), Math.round(h1.bottom)], btnBottom: btn.length ? Math.max(...btn) : null, art}; }'''
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for ph, dt in PAGES:
            for board, sizes in ((ph, SIZES_PH), (dt, SIZES_DT)):
                for W, H in sizes:
                    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1300)
                    await pg.add_style_tag(content='*{animation:none!important;transition:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W))
                    await pg.wait_for_timeout(300)
                    r = await pg.evaluate(JS)
                    print(f'{board:22s} {W}x{H}: h1 {r["h1"]} buttons end {r["btnBottom"]} bar {r["bar"]} art', [(a['alt'], a['top'], a['bottom'], str(a['visPct']) + '%') for a in r['art']], flush=True)
                    await ctx.close()
        await b.close()
asyncio.run(main())
