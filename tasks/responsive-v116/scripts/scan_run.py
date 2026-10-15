"""Run scan.js on many boards x device sizes x text sizes; write one JSON per shard.
usage (from the repository root): python3 tasks/responsive-v116/scripts/scan_run.py PORT SHARD NSHARDS OUT.json [--time ISO] [--only Board1,Board2]
Devices: phones portrait/landscape, small tablets, tablets portrait/landscape, laptops, desktops, wide screens."""
import asyncio, json, os, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch

PORT, SHARD, NSH, OUT = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
TIME = sys.argv[sys.argv.index('--time') + 1] if '--time' in sys.argv else '2026-10-16T12:00:00+05:30'
ONLY = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
JS = open(os.path.join(os.path.dirname(__file__), 'scan.js')).read()

PHONE = [(320, 568), (360, 780), (375, 667), (390, 844), (412, 915), (430, 932), (480, 854), (540, 720), (600, 960), (680, 1000), (760, 1024),
         (568, 320), (667, 375), (740, 360)]                                   # last three = phones turned sideways
WIDE = [(768, 1024), (800, 1280), (820, 1180), (834, 1194), (900, 1200), (1024, 768), (1024, 1366), (1080, 810), (1133, 744), (1180, 820),
        (1194, 834), (1280, 800), (1366, 768), (1440, 900), (1536, 864), (1680, 1050), (1920, 1080), (2560, 1440),
        (844, 390), (896, 414), (932, 430)]                                    # last three = big phones sideways (tablet layout)
DESK = ['Main', 'NewTemple', 'PranPratishtha', 'Seva', 'Gallery', 'History', 'Contact', 'Darshan', 'NotFound']
PH = ['HomeMobile', 'HomeMobile2', 'NewTempleMobile', 'PranPratishthaMobile', 'SevaMobile', 'GalleryMobile', 'HistoryMobile', 'ContactMobile',
      'DarshanMobile', 'NotFoundMobile', 'MenuMobile', 'OfflineMobile']
NATIVE = {'HomeTablet': [(768, 1024), (810, 1080), (834, 1194)], 'HomeTabletL': [(1133, 744), (1180, 820), (1366, 1024)], 'HomePhoneL': [(844, 390), (896, 414), (932, 430)]}

jobs = []
for b in DESK: jobs += [(b, w, h) for (w, h) in PHONE[:11] + WIDE]          # desktop files at every width (one responsive page)
for b in PH: jobs += [(b, w, h) for (w, h) in PHONE]
for b, dv in NATIVE.items(): jobs += [(b, w, h) for (w, h) in dv]
if ONLY: jobs = [j for j in jobs if j[0] in ONLY]
if '--sizes' in sys.argv:   # replace the size list, e.g. --sizes 568x320,667x375
    SZ = [tuple(map(int, x.split('x'))) for x in sys.argv[sys.argv.index('--sizes') + 1].split(',')]
    jobs = [(b, w, h) for b in sorted(set(j[0] for j in jobs), key=[j[0] for j in jobs].index) for (w, h) in SZ]
jobs = [j for i, j in enumerate(jobs) if i % NSH == SHARD]


async def one(br, board, W, H, big):
    ctx = await br.new_context(viewport={'width': W, 'height': H})
    await ctx.add_init_script(clock_script(TIME, frozen=True, big_text=big))
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, board)); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
    await pg.evaluate('''async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += innerHeight) { scrollTo({top: y, behavior: 'instant'}); await new Promise(r => setTimeout(r, 25)); } scrollTo({top: 0, behavior: 'instant'}); }''')
    await pg.wait_for_timeout(400)
    r = await pg.evaluate(JS)
    # fixed layers: share of the first screen they cover, and whether the bottom bar hides the end of the page
    r['fixed'] = await pg.evaluate('''() => { const H = innerHeight; let cover = 0, bar = null; const list = [];
      for (const e of document.querySelectorAll('.vm-root *')) { const s = getComputedStyle(e); if (s.position !== 'fixed' && s.position !== 'sticky') continue; if (s.display === 'none' || s.visibility === 'hidden') continue;
        const q = e.getBoundingClientRect(); if (q.height < 10 || q.width < innerWidth * 0.5 || q.height > H * 0.95) continue; if (e.parentElement.closest('[style*="position: fixed"],.vx-abar')) continue;
        cover += Math.max(0, Math.min(q.bottom, H) - Math.max(q.top, 0)); list.push((e.className || e.tagName).toString().split(' ')[0] + ':' + Math.round(q.height)); if ((s.position === 'fixed' || s.position === 'sticky') && q.bottom >= H - 40 && q.top > H * 0.5) bar = e; }
      let hidesEnd = null; if (bar) { scrollTo({top: document.documentElement.scrollHeight, behavior: 'instant'}); const top = bar.getBoundingClientRect().top;
        const f = [...document.querySelectorAll('footer *, .vm-footer *')].filter(x => x.textContent.trim() && x.children.length === 0 && getComputedStyle(x).display !== 'none'); const last = f[f.length - 1];
        if (last) { const lb = last.getBoundingClientRect().bottom; hidesEnd = lb > top + 1 ? Math.round(lb - top) : 0; } scrollTo({top: 0, behavior: 'instant'}); }
      return {cover: Math.round(cover / H * 100), list, hidesEnd}; }''')
    r['errors'] = errs
    await ctx.close()
    return r


async def main():
    res = {}
    async with async_playwright() as p:
        br = await launch(p)
        for k, (board, W, H) in enumerate(jobs):
            for big in (False, True):
                key = '%s|%dx%d|%s' % (board, W, H, 'big' if big else 'std')
                try: res[key] = await one(br, board, W, H, big)
                except Exception as e: res[key] = {'crash': str(e)[:200]}
            if k % 10 == 0: print(SHARD, k, '/', len(jobs), flush=True); json.dump(res, open(OUT, 'w'), ensure_ascii=False)
        await br.close()
    json.dump(res, open(OUT, 'w'), ensure_ascii=False)
    print('done', SHARD, len(res), flush=True)
asyncio.run(main())
