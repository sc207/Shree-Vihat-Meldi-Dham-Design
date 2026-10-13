# Item 4 tests: phone menu ✕ visibility, target, focus ring, closing back to the page the visitor came from, Escape, reopen, other links.
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT = int(sys.argv[1]); TAG = sys.argv[2]
def L(c):
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0] / 255) + 0.7152 * f(c[1] / 255) + 0.0722 * f(c[2] / 255)
def cr(a, b): x, y = L(a), L(b); return (max(x, y) + .05) / (min(x, y) + .05)
async def main():
    out = []
    async with async_playwright() as p:
        b = await launch(p)
        for W, H in ((320, 568), (360, 800), (390, 844), (430, 932), (844, 390)):
            ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            r = {'W': W, 'H': H, 'problems': []}
            # 1) direct open: ✕ look, target, focus ring, default current mark
            await pg.goto(f'http://127.0.0.1:{PORT}/MenuMobile.dc.html'); await pg.wait_for_timeout(900)
            m = await pg.evaluate('''() => { const c = document.querySelector('.vm-mnav__close'); const s = getComputedStyle(c); const path = c.querySelector('path'); const r = c.getBoundingClientRect();
                let p = c, bg = null; while (p) { const v = getComputedStyle(p).backgroundColor; if (v !== 'rgba(0, 0, 0, 0)') { bg = v; break; } p = p.parentElement; }
                return {stroke: getComputedStyle(path).stroke, bg, w: Math.round(r.width), h: Math.round(r.height), label: c.getAttribute('aria-label'), cur: [...document.querySelectorAll('.vm-mnav ol a')].filter(a => a.getAttribute('aria-current') === 'page').map(a => a.getAttribute('href'))}; }''')
            nums = lambda s: [float(x) for x in s[s.index('(') + 1:s.index(')')].split(',')[:3]]
            r['contrast'] = round(cr(nums(m['stroke']), nums(m['bg'])), 2); r['target'] = [m['w'], m['h']]; r['curDirect'] = m['cur']
            if r['contrast'] < 3: r['problems'].append(f'✕ contrast {r["contrast"]}')
            if min(m['w'], m['h']) < 44: r['problems'].append('✕ target < 44 px')
            if m['cur'] != ['HomeMobile.dc.html']: r['problems'].append(f'direct-open current {m["cur"]}')
            await pg.focus('.vm-mnav__close'); ring = await pg.evaluate("() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0; }")
            if not ring: r['problems'].append('no focus ring on ✕')
            await pg.click('.vm-mnav__close'); await pg.wait_for_timeout(700)
            r['directClose'] = pg.url.split('/')[-1]
            if r['directClose'] != 'HomeMobile.dc.html': r['problems'].append(f'direct close went to {r["directClose"]}')
            # 2) from Darshan, scrolled down: open menu, check mark, ✕ → back to Darshan at the same place
            await pg.goto(f'http://127.0.0.1:{PORT}/DarshanMobile.dc.html'); await pg.wait_for_timeout(900)
            await pg.evaluate("window.scrollTo({top: 1400, behavior: 'instant'})"); await pg.wait_for_timeout(200); y0 = await pg.evaluate('scrollY')
            await pg.evaluate("document.querySelector('a.vm-menu-btn').click()"); await pg.wait_for_url('**/MenuMobile.dc.html'); await pg.wait_for_timeout(800)
            cur = await pg.evaluate("() => [...document.querySelectorAll('.vm-mnav ol a')].filter(a => a.getAttribute('aria-current') === 'page').map(a => a.getAttribute('href'))")
            if cur != ['DarshanMobile.dc.html']: r['problems'].append(f'from Darshan current {cur}')
            await pg.click('.vm-mnav__close'); await pg.wait_for_url('**/DarshanMobile.dc.html'); await pg.wait_for_timeout(900)
            y1 = await pg.evaluate('scrollY'); r['backScroll'] = [y0, y1]
            if abs(y1 - y0) > 40: r['problems'].append(f'scroll not kept {y0}->{y1}')
            # 3) reopen + Escape
            await pg.evaluate("document.querySelector('a.vm-menu-btn').click()"); await pg.wait_for_url('**/MenuMobile.dc.html'); await pg.wait_for_timeout(800)
            await pg.focus('.vm-mnav ol a'); await pg.keyboard.press('Escape'); await pg.wait_for_url('**/DarshanMobile.dc.html'); await pg.wait_for_timeout(600)
            # 4) reopen + choose another page
            await pg.evaluate("document.querySelector('a.vm-menu-btn').click()"); await pg.wait_for_url('**/MenuMobile.dc.html'); await pg.wait_for_timeout(800)
            await pg.click('.vm-mnav ol a[href="SevaMobile.dc.html"]'); await pg.wait_for_url('**/SevaMobile.dc.html'); await pg.wait_for_timeout(500)
            r['afterLink'] = pg.url.split('/')[-1]
            # 5) from Home part 2 (HomeMobile2) → Home marked
            await pg.goto(f'http://127.0.0.1:{PORT}/HomeMobile2.dc.html'); await pg.wait_for_timeout(700)
            has = await pg.evaluate("!!document.querySelector('a[href=\"MenuMobile.dc.html\"]')")
            r['errors'] = errs
            if errs: r['problems'].append('page errors')
            out.append(r); print(TAG, W, H, 'contrast', r['contrast'], 'target', r['target'], 'back scroll', r.get('backScroll'), 'problems', r['problems'], flush=True)
            if W == 390:
                await pg.goto(f'http://127.0.0.1:{PORT}/MenuMobile.dc.html'); await pg.wait_for_timeout(800)
                await pg.screenshot(path=f'work/fix/evidence/item4/{TAG}_menu_390.png', clip={'x': 0, 'y': 0, 'width': 390, 'height': 300})
            await ctx.close()
        await b.close()
    json.dump(out, open(f'work/fix/evidence/item4/tests_{TAG}.json', 'w'), indent=1)
asyncio.run(main())
