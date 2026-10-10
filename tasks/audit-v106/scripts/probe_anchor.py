# Probe: in-page links (#...) — after jumping, is the target's heading hidden under a fixed/sticky bar at the top?
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PAGES = [('Main', 1440), ('History', 1440), ('PranPratishtha', 1440), ('Darshan', 1440), ('Contact', 1440), ('NewTemple', 1440), ('Seva', 1440), ('Gallery', 1440),
         ('HomeMobile', 390), ('HistoryMobile', 390), ('PranPratishthaMobile', 390), ('DarshanMobile', 390), ('ContactMobile', 390), ('NewTempleMobile', 390), ('SevaMobile', 390), ('GalleryMobile', 390)]
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for board, W in PAGES:
            ctx = await b.new_context(viewport={'width': W, 'height': 900 if W > 760 else 844}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1200)
            await pg.add_style_tag(content='html{scroll-behavior:auto!important} *{animation:none!important;transition:none!important}')
            hrefs = await pg.evaluate('''() => [...new Set([...document.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href')).filter(h => h.length > 1))]''')
            bad = []
            for h in hrefs:
                r = await pg.evaluate('''(h) => { const t = document.getElementById(decodeURIComponent(h.slice(1))); if (!t) return {missing: true};
                    t.scrollIntoView({block: 'start', behavior: 'instant'}); return null; }''', h)
                if r and r.get('missing'): bad.append((h, 'target missing')); continue
                # emulate the browser's own anchor jump instead of scrollIntoView (honours scroll-margin/padding)
                await pg.evaluate('window.scrollTo({top:0,behavior:"instant"})'); await pg.evaluate('(h) => { location.hash = ""; location.hash = h; }', h); await pg.wait_for_timeout(250)
                m = await pg.evaluate('''(h) => { const t = document.getElementById(decodeURIComponent(h.slice(1)));
                    const head = t.matches('h1,h2,h3') ? t : (t.querySelector('h1,h2,h3,.vm-eyebrow') || t); const hr = head.getBoundingClientRect();
                    let cover = 0; for (const e of document.querySelectorAll('body *')) { const s = getComputedStyle(e); if ((s.position === 'fixed' || s.position === 'sticky') && s.display !== 'none' && s.visibility !== 'hidden') { const r = e.getBoundingClientRect(); if (r.top <= 1 && r.height > 0 && r.height < 300 && r.width > innerWidth * 0.5) cover = Math.max(cover, r.bottom); } }
                    return {headTop: Math.round(hr.top), cover: Math.round(cover), text: head.textContent.trim().slice(0, 24), sm: getComputedStyle(t).scrollMarginTop}; }''', h)
                if m['headTop'] < m['cover'] + 4: bad.append((h, m))
            print(board, W, 'links', len(hrefs), 'hidden-under-bar:', bad, flush=True)
            await ctx.close()
        await b.close()
asyncio.run(main())
