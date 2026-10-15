"""Every <img> on every board at several screen widths: drawn size vs real pixels, fit and crop.
usage (repo root): python3 tasks/image-audit/scripts/measure_images.py PORT OUT.json
'need' = real pixels needed for a sharp picture at that size on a 2x screen (3x for phones); 'sharp' = real / need (< 1 = blown up)."""
import asyncio, json, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
PORT, OUT = int(sys.argv[1]), sys.argv[2]
DESK = ['Main', 'NewTemple', 'PranPratishtha', 'Seva', 'Gallery', 'History', 'Contact', 'Darshan', 'NotFound']
PH = ['HomeMobile', 'HomeMobile2', 'NewTempleMobile', 'PranPratishthaMobile', 'SevaMobile', 'GalleryMobile', 'HistoryMobile', 'ContactMobile',
      'DarshanMobile', 'NotFoundMobile', 'MenuMobile', 'OfflineMobile']
JOBS = [(b, w, 2) for b in DESK for w in (1920, 1440, 1180, 1024, 834, 768)] + [(b, w, 3) for b in PH for w in (430, 390, 360, 320)] \
     + [('HomeTablet', 834, 2), ('HomeTabletL', 1180, 2), ('HomePhoneL', 844, 3)]
JS = r'''() => { const out = [];
  for (const im of document.querySelectorAll('img')) {
    const r = im.getBoundingClientRect(); const s = getComputedStyle(im);
    if (r.width < 2 || r.height < 2 || s.display === 'none' || s.visibility === 'hidden') continue;
    let hidden = false; for (let e = im; e; e = e.parentElement) { const c = getComputedStyle(e); if (c.display === 'none' || c.visibility === 'hidden' || +c.opacity === 0) { hidden = true; break; } }
    const src = (im.getAttribute('src') || '').replace(/^.*\/_blob\//, '');
    const box = im.closest('figure,.vm-arch,.vx-crop,div') || im.parentElement; const br = box.getBoundingClientRect();
    out.push({src, nw: im.naturalWidth, nh: im.naturalHeight, w: Math.round(r.width), h: Math.round(r.height), fit: s.objectFit, pos: s.objectPosition,
              y: Math.round(r.top + scrollY), cls: (im.className || '') + ' < ' + (im.parentElement.className || im.parentElement.tagName), alt: im.alt, hidden,
              cw: Math.round(br.width), ch: Math.round(br.height), tr: s.transform});
  } return out; }'''
async def main():
    res = {}
    async with async_playwright() as p:
        br = await launch(p)
        for b, W, dpr in JOBS:
            ctx = await br.new_context(viewport={'width': W, 'height': 900 if W > 760 else 844})
            await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True))
            pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(900)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
            await pg.evaluate('async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += innerHeight) { scrollTo({top: y, behavior: "instant"}); await new Promise(r => setTimeout(r, 40)); } scrollTo({top: 0, behavior: "instant"}); }')
            await pg.wait_for_timeout(500)
            items = await pg.evaluate(JS)
            for it in items:
                if not it['nw']: it['sharp'] = None; continue
                if it['fit'] in ('cover',): sc = max(it['w'] / it['nw'], it['h'] / it['nh'])
                elif it['fit'] in ('contain', 'scale-down'): sc = min(it['w'] / it['nw'], it['h'] / it['nh'])
                else: sc = max(it['w'] / it['nw'], it['h'] / it['nh'])          # fill
                it['scale'] = round(sc, 3); it['sharp'] = round(1 / (sc * dpr), 2); it['dpr'] = dpr
                # share of the picture cut away by cover
                if it['fit'] == 'cover': it['crop_w'] = round(1 - it['w'] / (it['nw'] * sc), 2); it['crop_h'] = round(1 - it['h'] / (it['nh'] * sc), 2)
            res['%s|%d' % (b, W)] = items
            await ctx.close(); print(b, W, len(items), flush=True)
        await br.close()
    json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
asyncio.run(main())
