# Probe: text that spills outside its own visible box (pill, button, card, chip) — the case found by eye on HomeMobile at 320 px,
# which the earlier clipping check missed because the box does not hide overflow. All boards, phone + tablet + desktop widths, normal + large text.
import asyncio, sys, json, re
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch, boards
SCREEN = {'MenuMobile', 'OfflineMobile'}
JS = r'''() => {
  const out = [];
  const boxed = e => { const s = getComputedStyle(e); return (s.backgroundColor !== 'rgba(0, 0, 0, 0)' && s.backgroundColor !== 'transparent') || parseFloat(s.borderLeftWidth) > 0 || parseFloat(s.borderTopWidth) > 0; };
  for (const e of document.querySelectorAll('body *')) {
    if (e.closest('.vm-sr,[aria-hidden=true],svg,.vx-marquee,script,style')) continue;
    const s = getComputedStyle(e); if (s.display === 'none' || s.visibility === 'hidden' || s.display === 'contents') continue;
    if (!boxed(e)) continue;
    const r = e.getBoundingClientRect(); if (r.width < 8 || r.height < 8) continue;
    // text nodes whose nearest boxed ancestor is e
    const tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let n, worst = 0, txt = '';
    while ((n = tw.nextNode())) {
      if (!n.textContent.trim()) continue;
      let p = n.parentElement, own = null; while (p && p !== e) { if (boxed(p)) { own = p; break; } p = p.parentElement; }
      if (own) continue;
      if (n.parentElement.closest('.vm-sr')) continue;
      const ps = getComputedStyle(n.parentElement); if (ps.visibility === 'hidden' || ps.display === 'none') continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const q of rg.getClientRects()) { if (q.width < 1) continue;
        const d = Math.max(r.left - q.left, q.right - r.right, r.top - q.top - 2, q.bottom - r.bottom - 2);
        if (d > worst) { worst = d; txt = n.textContent.trim().slice(0, 30); } }
    }
    if (worst > 1.5) out.push({el: e.tagName.toLowerCase() + '.' + [...e.classList].slice(0, 2).join('.'), text: txt, by: Math.round(worst), w: Math.round(r.width), top: Math.round(r.top + scrollY), clip: s.overflow});
  }
  return out;
}'''
async def main():
    res = {}
    async with async_playwright() as p:
        b = await launch(p)
        for name, bw, fh in boards('design/project'):
            if name in SCREEN: continue
            if bw <= 760: widths = [320, 360, 390, 430]
            elif name in ('HomeTablet', 'HomeTabletL', 'HomePhoneL'): widths = [bw]
            else: widths = [768, 900, 1024, 1280, 1440]
            for W in widths:
                for big in (False, True):
                    if big and W not in (320, 390, 768, 1024, 1440, 834, 844, 1180): continue
                    ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
                    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{name}.dc.html'); await pg.wait_for_timeout(1100)
                    await pg.add_style_tag(content='*{animation:none!important;transition:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W))
                    await pg.wait_for_timeout(250)
                    r = await pg.evaluate(JS)
                    key = f'{name}|{W}|{"big" if big else "std"}'; res[key] = r
                    if r: print(key, [(x['el'], x['text'], x['by'], x['top']) for x in r][:8], flush=True)
                    await ctx.close()
        await b.close()
    json.dump(res, open('work/audit/spill.json', 'w'), ensure_ascii=False, indent=1)
    print('runs', len(res), 'with spill', sum(1 for v in res.values() if v))
asyncio.run(main())
