"""Cramped text: text blocks narrower than MINW px that wrap to 4+ lines (or a single word per line). usage: narrow.py PORT W MINW Board,Board"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, W, MINW, BOARDS = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4].split(',')
JS = '''(MINW) => { const out = []; const seen = new Set();
 for (const e of document.querySelectorAll('.vm-root p, .vm-root li, .vm-root h2, .vm-root h3, .vm-root h4, .vm-root dd, .vm-root figcaption, .vm-root b, .vm-root span, .vm-root a')) {
   if (e.closest('[aria-hidden="true"],.vx-marquee,.vm-mnav,[hidden]')) continue;
   const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || s.display === 'inline') continue;
   const txt = e.innerText.trim(); if (txt.length < 12) continue;
   const r = e.getBoundingClientRect(); if (r.width === 0) continue;
   const rg = document.createRange(); rg.selectNodeContents(e); const tops = new Set([...rg.getClientRects()].filter(q => q.width > 1).map(q => Math.round(q.top / 4))); const lines = tops.size;
   if (e.querySelector('p,li,div,h2,h3,h4,figcaption')) continue;
   const words = txt.split(/\\s+/).length;
   if ((r.width < MINW && lines >= 4) || (lines >= 3 && words <= lines + 1 && words >= 3)) {
     const sec = e.closest('section,[id]'); const k = (sec && (sec.id || sec.className.split(' ')[0])) + '|' + txt.slice(0, 30); if (seen.has(k)) continue; seen.add(k);
     out.push([Math.round(r.width), lines, words, (sec && (sec.id || sec.className.split(' ')[0])) || '', e.tagName + '.' + (e.className || '').toString().split(' ')[0], txt.replace(/\\n/g, ' / ').slice(0, 70)]); }
 } return out; }'''
async def main():
    async with async_playwright() as p:
        br = await launch(p)
        for b in BOARDS:
            for big in (False, True):
                ctx = await br.new_context(viewport={'width': W, 'height': 844})
                await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True, big_text=big))
                pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
                for r in await pg.evaluate(JS, MINW): print('%-20s %-3s w=%-4d lines=%-2d words=%-3d %-22s %-26s %s' % (b, 'big' if big else 'std', r[0], r[1], r[2], r[3][:22], r[4][:26], r[5]))
                await ctx.close()
        await br.close()
asyncio.run(main())
