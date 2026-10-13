# For every section of every board: background pattern (lattice data-URI / gradient) and ornaments it contains.
# Then compare each desktop board with its phone board section by section (matched by heading id).
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8774
PAIRS = [('Main', 'HomeMobile', 'HomeMobile2'), ('NewTemple', 'NewTempleMobile'), ('PranPratishtha', 'PranPratishthaMobile'), ('Seva', 'SevaMobile'),
         ('Gallery', 'GalleryMobile'), ('History', 'HistoryMobile'), ('Contact', 'ContactMobile'), ('Darshan', 'DarshanMobile'), ('NotFound', 'NotFoundMobile'),
         ('HomeTablet',), ('HomeTabletL',), ('HomePhoneL',)]
JS = r'''() => [...document.querySelectorAll('section, footer.vm-footer, .vm-cta, .vx-stats')].map(s => {
  const cs = getComputedStyle(s); const bg = cs.backgroundImage;
  const pat = bg === 'none' ? '-' : (bg.match(/stroke-opacity='?\.?(\d+)/) ? 'lattice' + (bg.includes('circle') ? '+dot' : '') : (bg.includes('gradient') ? 'gradient' : 'other'));
  const orn = [...s.querySelectorAll(':scope > svg, :scope > * > svg[class*=mandala], svg.vm-cta__orn, svg.vm-mandala, svg.vm-hero__mandala, svg.vm-devotional__mandala')].map(x => x.getAttribute('class')).filter((v, i, a) => v && a.indexOf(v) === i);
  const key = s.getAttribute('aria-labelledby') || s.id || [...s.classList].slice(0, 3).join('.');
  return {key, cls: [...s.classList].slice(0, 4).join('.'), pat, orn: orn.join(',')}; })'''
async def main():
    out = {}
    async with async_playwright() as p:
        b = await launch(p)
        for grp in PAIRS:
            for board in grp:
                W = 390 if 'Mobile' in board else {'HomeTablet': 834, 'HomeTabletL': 1180, 'HomePhoneL': 844}.get(board, 1440)
                ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(900)
                out[board] = await pg.evaluate(JS); await ctx.close()
        await b.close()
    json.dump(out, open('work/chakra/patterns.json', 'w'), ensure_ascii=False, indent=1)
    for grp in PAIRS:
        rows = {}
        for board in grp:
            for r in out[board]: rows.setdefault(r['key'], {})[board] = (r['pat'], r['orn'])
        print('\n==', ' / '.join(grp))
        for k, v in rows.items():
            vals = set(v.values()); flag = '  <-- differs' if len(grp) > 1 and len(vals) > 1 and not (grp[0] == 'Main' and len(v) == 1) else ''
            print(f'  {k[:38]:38s}', ' | '.join(f'{bd}:{p}/{o or "-"}' for bd, (p, o) in v.items()), flag)
asyncio.run(main())
