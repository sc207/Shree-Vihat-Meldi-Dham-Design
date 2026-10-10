# Probe: non-text contrast of icons inside links/buttons (SVG stroke/fill vs. the nearest solid background). Needs ≥ 3:1 (WCAG 1.4.11).
import asyncio, sys, re
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch, boards
JS = r'''() => { const out = [];
  const rgb = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(parseFloat); return v.length > 3 && v[3] === 0 ? null : v; };
  const L = c => { const f = v => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2]); };
  const CR = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  const blend = (fg, bg) => fg.length > 3 && fg[3] < 1 ? fg.slice(0, 3).map((v, i) => v * fg[3] + bg[i] * (1 - fg[3])) : fg;
  for (const svg of document.querySelectorAll('a svg, button svg')) {
    const host = svg.closest('a,button'); const s = getComputedStyle(host); if (s.display === 'none' || s.visibility === 'hidden') continue;
    const r = svg.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    if (svg.closest('[aria-hidden=true] a, .vm-sr')) continue;
    let p = svg.parentElement, bg = null; while (p) { const b = rgb(getComputedStyle(p).backgroundColor); if (b && (b.length < 4 || b[3] > 0.6)) { bg = b; break; } p = p.parentElement; }
    if (!bg) continue; if (getComputedStyle(document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2) || svg).backgroundImage !== 'none') continue;
    let worst = 99, col = '';
    for (const sh of svg.querySelectorAll('path,line,circle,rect,polyline,polygon')) { const cs = getComputedStyle(sh);
      for (const k of ['stroke', 'fill']) { const c = rgb(cs[k]); if (!c || cs[k] === 'none') continue; if (k === 'stroke' && parseFloat(cs.strokeWidth) === 0) continue;
        const v = CR(blend(c, bg), bg); if (v < worst) { worst = v; col = cs[k]; } } }
    if (worst < 3) out.push({host: host.tagName.toLowerCase() + '.' + [...host.classList].slice(0, 2).join('.'), label: (host.getAttribute('aria-label') || host.textContent.trim()).slice(0, 24), cr: +worst.toFixed(2), col, bg: 'rgb(' + bg.slice(0, 3).map(Math.round).join(',') + ')'});
  }
  return out; }'''
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for name, bw, fh in boards('design/project'):
            W = 390 if bw <= 760 else 1440
            if name in ('HomeTablet', 'HomeTabletL', 'HomePhoneL'): W = bw
            ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{name}.dc.html'); await pg.wait_for_timeout(1100)
            r = await pg.evaluate(JS)
            if r: print(name, W, r, flush=True)
            await ctx.close()
        await b.close()
asyncio.run(main())
