# Probe: animations whose keyframes set `transform` on an element that also has its own (non-animated) transform.
# The keyframes replace the element's transform, so e.g. a centring translate(-50%) is lost while the animation runs (or forever with fill: both).
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch, boards
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
JS = r'''() => { const out = [];
  const els = [...document.querySelectorAll('body *')];
  for (const e of els) { for (const pseudo of ['', '::before', '::after']) {
    const s = getComputedStyle(e, pseudo || null); if (s.animationName === 'none' || (pseudo && s.content === 'none')) continue;
    if (s.display === 'none') continue;
    out.push({e, pseudo, name: s.animationName, live: s.transform}); } }
  // remove animations and read the element's own transform
  const st = document.createElement('style'); st.textContent = '*, *::before, *::after { animation: none !important; }'; document.head.appendChild(st);
  const res = [];
  for (const o of out) { const s = getComputedStyle(o.e, o.pseudo || null); const base = s.transform;
    const r = o.e.getBoundingClientRect();
    if (base !== 'none' && !/^matrix\(1, 0, 0, 1, 0, 0\)$/.test(base)) res.push({sel: o.e.tagName.toLowerCase() + '.' + [...o.e.classList].slice(0, 3).join('.') + o.pseudo, anim: o.name, base, live: o.live, w: Math.round(r.width), vis: r.width > 0}); }
  st.remove(); return res; }'''
async def main():
    seen = {}
    async with async_playwright() as p:
        b = await launch(p)
        for name, bw, fh in boards('design/project'):
            for W in ((390,) if bw <= 760 else (1440, 1024, 768)):
                ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{name}.dc.html'); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content='.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W))
                await pg.wait_for_timeout(1500)
                for r in await pg.evaluate(JS):
                    k = (r['sel'], r['anim'], r['base'])
                    seen.setdefault(k, []).append(f'{name}@{W}' + ('' if r['vis'] else '(hidden)'))
                await ctx.close()
        await b.close()
    for (sel, anim, base), where in sorted(seen.items()):
        print(f'{sel:45s} anim={anim:22s} own transform={base}\n    on: {", ".join(where[:12])}{" …" if len(where) > 12 else ""}')
asyncio.run(main())
