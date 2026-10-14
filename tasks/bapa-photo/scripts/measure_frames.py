"""Measure every frame that shows a given image: rendered box, crop, and the source pixels needed at DPR 2 and 3.
usage: python3 measure_frames.py PORT BLOBID [OUTDIR]  (OUTDIR: save a close-up picture of each frame)"""
import asyncio, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools'))
from _common import FIX, clock_script, launch
from playwright.async_api import async_playwright
PORT, BLOB = int(sys.argv[1]), sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else None
CASES = [('Main', [390, 768, 1024, 1440, 1920]), ('HomeTablet', [834]), ('HomeTabletL', [1180]), ('HomePhoneL', [844]),
         ('HomeMobile2', [320, 390, 430]), ('History', [1024, 1440]), ('HistoryMobile', [320, 390, 430]),
         ('Gallery', [1024, 1440]), ('GalleryMobile', [390])]
JS = '''(b) => [...document.querySelectorAll('img')].filter(i => i.src.includes(b)).map(i => {
  const r = i.getBoundingClientRect(), cs = getComputedStyle(i), fig = i.closest('figure,.vm-arch,.vm-profile__media');
  return {x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height), fit: cs.objectFit, pos: cs.objectPosition,
          nw: i.naturalWidth, nh: i.naturalHeight, where: (i.closest('.vx-duo') ? 'duo' : i.closest('.vx-strip') ? 'strip' : i.closest('.vx-trio') ? 'trio' : i.closest('.vm-profile') ? 'profile' : 'other'),
          visible: r.width > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'}; })'''
async def main():
    res = []
    async with async_playwright() as p:
        br = await launch(p)
        for board, widths in CASES:
            for W in widths:
                ctx = await br.new_context(viewport={'width': W, 'height': 900})
                await ctx.add_init_script(clock_script('2026-10-14T12:00:00+05:30'))
                pg = await ctx.new_page()
                await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, board)); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
                await pg.evaluate('''async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 30)); } scrollTo({top: 0, behavior: 'instant'}); }''')
                await pg.wait_for_timeout(700)
                items = await pg.evaluate(JS, BLOB)
                for k, it in enumerate(items):
                    if not it['visible']: continue
                    # cover: scale = max(w/nw, h/nh); visible source region = w/scale × h/scale
                    s = max(it['w'] / it['nw'], it['h'] / it['nh']) if it['fit'] == 'cover' else min(it['w'] / it['nw'], it['h'] / it['nh'])
                    it.update(board=board, W=W, used_src='%dx%d' % (round(min(it['nw'], it['w'] / s)), round(min(it['nh'], it['h'] / s))),
                              css_scale=round(s, 2), sharp_dpr=round(1 / s, 2))
                    res.append(it)
                    if OUT:
                        os.makedirs(OUT, exist_ok=True)
                        pad = 30
                        await pg.evaluate('(y) => scrollTo({top: Math.max(0, y - 120), behavior: "instant"})', it['y']); await pg.wait_for_timeout(250)
                        top = await pg.evaluate('(b) => [...document.querySelectorAll("img")].filter(i => i.src.includes(b))[%d].getBoundingClientRect().top' % k, BLOB)
                        await pg.screenshot(path='%s/%s_%d_%s.png' % (OUT, board, W, it['where']),
                                            clip={'x': max(0, it['x'] - pad), 'y': max(0, top - pad), 'width': min(W - max(0, it['x'] - pad), it['w'] + 2 * pad),
                                                  'height': min(900 - max(0, top - pad), it['h'] + 2 * pad + 60)})
                await ctx.close()
        await br.close()
    for r in res:
        print('%-14s %5d %-8s box %4dx%-4d %-6s pos %-9s src %4dx%-4d uses %-9s scale %.2f  sharp up to DPR %.2f' % (
            r['board'], r['W'], r['where'], r['w'], r['h'], r['fit'], r['pos'], r['nw'], r['nh'], r['used_src'], r['css_scale'], r['sharp_dpr']))
    if OUT: json.dump(res, open(os.path.join(OUT, 'frames.json'), 'w'), indent=1)
asyncio.run(main())
