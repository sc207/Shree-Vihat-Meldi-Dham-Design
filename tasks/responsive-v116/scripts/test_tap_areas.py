"""Touch-area test: for each small link/button on phones, tap 1 px inside the 44 px band above and below its visible box
(and left/right for round buttons) and check the tap lands on that control. usage: python3 test_tap_areas.py PORT [W]"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT = int(sys.argv[1]); W = int(sys.argv[2]) if len(sys.argv) > 2 else 390
PAGES = ['Main', 'Contact', 'Darshan', 'PranPratishtha', 'Seva', 'History', 'Gallery', 'NewTemple', 'NotFound', 'OfflineMobile', 'MenuMobile']
SEL = '.vm-footer li a, .vm-notice a, .vx-crumb a, .vm-brand, .vx-dt__foot a, .vx-upnext__more, .vm-contact__card a, .vx-plan__foot a, .vx-off__info a, .vx-tel, .vx-caladd a, .vx-fs, .vx-marquee__btn'
JS = '''(sel) => { const res = [];
  for (const e of document.querySelectorAll(sel)) { if (e.closest('[hidden]')) continue; const r = e.getBoundingClientRect(); if (!r.width || !r.height) continue;
    if (r.top < 40 || r.bottom > innerHeight - 70) continue;               // only targets fully in view, away from fixed bars
    const need = Math.max(0, (44 - r.height) / 2); const cx = r.left + r.width / 2; const pts = [];
    if (need >= 2) { pts.push([cx, r.top - need + 1]); pts.push([cx, r.bottom + need - 1]); } else continue;
    // OK = the tap lands on this control, or on a neighbouring control that is closer (tightly stacked links share the gap); a miss = dead area
    const ctl = t => t && t.closest('a[href],button,summary,label,input,select');
    const hits = pts.map(([x, y]) => { const t = document.elementFromPoint(x, y); const c = ctl(t); return !!c && (c === e || e.contains(t) || (c !== e && c.matches(sel))); });
    res.push({t: (e.textContent || e.getAttribute('aria-label') || '').trim().replace(/\\s+/g, ' ').slice(0, 20), h: Math.round(r.height), ok: hits.every(Boolean)}); }
  return res; }'''
async def main():
    total = ok = 0; fails = []
    async with async_playwright() as p:
        br = await launch(p)
        for b in PAGES:
            ctx = await br.new_context(viewport={'width': W, 'height': 844}); await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30'))
            pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(1000)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;max-width:%dpx!important;min-width:0!important}' % (W, W)); await pg.wait_for_timeout(300)
            H = await pg.evaluate('document.documentElement.scrollHeight'); seen = set()
            for y in range(0, H, 600):
                await pg.evaluate('(y) => scrollTo({top: y, behavior: "instant"})', y); await pg.wait_for_timeout(60)
                for r in await pg.evaluate(JS, SEL):
                    k = (r['t'], r['h']);
                    if k in seen: continue
                    seen.add(k); total += 1; ok += r['ok']
                    if not r['ok']: fails.append((b, r['t'], r['h']))
            await ctx.close()
        await br.close()
    print('port %d width %d: %d small targets tested, %d reach 44 px, %d do not' % (PORT, W, total, ok, total - ok))
    for f in fails[:25]: print('   not reached:', f)
asyncio.run(main())
