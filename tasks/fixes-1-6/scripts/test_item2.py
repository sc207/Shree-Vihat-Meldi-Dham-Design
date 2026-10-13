# Item 2 tests: tablet/small-laptop menu on every desktop/tablet board at 760–1180 px (port given), normal + large text.
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT = int(sys.argv[1])
WF = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important} html{scroll-behavior:auto!important}'
PAGES = ['Main', 'NewTemple', 'PranPratishtha', 'Seva', 'Gallery', 'History', 'Contact', 'Darshan', 'NotFound']
CUR = {'Main': 'Main.dc.html', 'HomeTablet': 'Main.dc.html', 'HomeTabletL': 'Main.dc.html', 'HomePhoneL': 'Main.dc.html', 'NotFound': None}
STATE = '''() => { const p = document.querySelector('#vx-tnav'); const b = document.querySelector('.vm-menu-btn'); const nav = document.querySelector('.vm-header .vm-nav');
  const r = p.getBoundingClientRect(); const ps = getComputedStyle(p); const cx = innerWidth / 2, cy = innerHeight / 2; const top = document.elementFromPoint(cx, cy);
  const ae = document.activeElement;
  return {open: ps.display !== 'none', rect: [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)], vw: innerWidth, vh: innerHeight,
    onTop: !!(top && p.contains(top)), exp: b.getAttribute('aria-expanded'), btnVisible: getComputedStyle(b).display !== 'none', navVisible: nav ? getComputedStyle(nav).display !== 'none' : null,
    focus: ae === b ? 'menu-btn' : (p.contains(ae) ? (ae.className || ae.tagName) : (ae ? ae.tagName : null)),
    links: [...p.querySelectorAll('ol a')].map(a => [a.getAttribute('href'), a.getAttribute('aria-current')]),
    docOverflow: document.documentElement.scrollWidth > innerWidth + 1, panelOverflowX: p.scrollWidth > p.clientWidth + 1,
    lastLinkReachable: (() => { const l = [...p.querySelectorAll('ol a')].pop(); return l.getBoundingClientRect().bottom <= r.top + p.scrollHeight + 1; })() }; }'''
async def run(b, board, W, H, big=False):
    errs = []
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(200)
    res = {'board': board, 'W': W, 'big': big, 'problems': []}
    s0 = await pg.evaluate(STATE)
    if s0['open']: res['problems'].append('panel visible before opening')
    if W >= 1180:
        if s0['btnVisible'] or not s0['navVisible']: res['problems'].append('at >=1180 the ☰ should be hidden and header links shown')
        await ctx.close(); res['errors'] = errs; return res
    if not s0['btnVisible']: res['problems'].append('☰ not visible'); await ctx.close(); return res
    await pg.click('.vm-menu-btn'); await pg.wait_for_timeout(150)
    s1 = await pg.evaluate(STATE)
    if not s1['open']: res['problems'].append('did not open')
    if s1['rect'] != [0, 0, W, H]: res['problems'].append(f'panel rect {s1["rect"]} != viewport')
    if not s1['onTop']: res['problems'].append('something paints over the panel')
    if s1['exp'] != 'true': res['problems'].append('aria-expanded not true')
    if s1['focus'] != 'vm-mnav__close': res['problems'].append(f'focus after open: {s1["focus"]}')
    want = ['Main.dc.html', 'Darshan.dc.html', 'NewTemple.dc.html', 'PranPratishtha.dc.html', 'Seva.dc.html', 'Gallery.dc.html', 'History.dc.html', 'Contact.dc.html']
    if [l[0] for l in s1['links']] != want: res['problems'].append(f'links {s1["links"]}')
    cur = CUR.get(board, board + '.dc.html'); got = [l[0] for l in s1['links'] if l[1] == 'page']
    if got != ([cur] if cur else []): res['problems'].append(f'current page mark {got} (want {cur})')
    if s1['docOverflow'] or s1['panelOverflowX']: res['problems'].append('horizontal overflow')
    if not s1['lastLinkReachable']: res['problems'].append('last link not reachable')
    # Tab cycles inside the panel
    outside = 0
    for i in range(18):
        await pg.keyboard.press('Tab'); f = await pg.evaluate("() => !!document.activeElement.closest('#vx-tnav')")
        outside += 0 if f else 1
    await pg.keyboard.press('Shift+Tab'); f = await pg.evaluate("() => !!document.activeElement.closest('#vx-tnav')"); outside += 0 if f else 1
    if outside: res['problems'].append(f'Tab left the panel {outside}x')
    # focus ring visible on a link
    await pg.focus('#vx-tnav ol a'); ring = await pg.evaluate("() => { const s = getComputedStyle(document.activeElement); return s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 || s.boxShadow !== 'none'; }")
    if not ring: res['problems'].append('no visible focus ring on links')
    await pg.keyboard.press('Escape'); await pg.wait_for_timeout(120)
    s2 = await pg.evaluate(STATE)
    if s2['open'] or s2['exp'] != 'false': res['problems'].append('Escape did not close')
    if s2['focus'] != 'menu-btn': res['problems'].append(f'focus after Escape: {s2["focus"]}')
    await pg.click('.vm-menu-btn'); await pg.wait_for_timeout(120); await pg.click('#vx-tnav .vm-mnav__close'); await pg.wait_for_timeout(120)
    s3 = await pg.evaluate(STATE)
    if s3['open'] or s3['focus'] != 'menu-btn': res['problems'].append('✕ did not close / return focus')
    await pg.click('.vm-menu-btn'); await pg.wait_for_timeout(120)
    async with pg.expect_navigation():
        await pg.click('#vx-tnav ol a[href="Darshan.dc.html"]')
    if not pg.url.endswith('/Darshan.dc.html'): res['problems'].append(f'link went to {pg.url}')
    res['errors'] = errs; await ctx.close(); return res
async def main():
    out = []
    async with async_playwright() as p:
        b = await launch(p)
        for board in PAGES:
            for W, H in ((760, 1000), (761, 1000), (800, 1100), (900, 1200), (1024, 768), (1100, 800), (1179, 820), (1180, 820)):
                out.append(await run(b, board, W, H))
        for board, W, H in (('HomeTablet', 834, 1112), ('HomeTabletL', 1180, 820), ('HomeTabletL', 1112, 834), ('HomePhoneL', 844, 390), ('HomePhoneL', 932, 430)):
            out.append(await run(b, board, W, H))
        for board, W, H in (('Main', 1024, 768), ('Seva', 768, 1024), ('HomePhoneL', 844, 390), ('Darshan', 900, 1200)):
            out.append(await run(b, board, W, H, big=True))
        await b.close()
    bad = [r for r in out if r['problems'] or r.get('errors')]
    print(f'{len(out)} runs, {len(bad)} with problems')
    for r in bad: print(' ', r['board'], r['W'], 'big' if r['big'] else '', r['problems'], r.get('errors', [])[:2])
    json.dump(out, open('work/fix/evidence/item2/tests.json', 'w'), ensure_ascii=False, indent=1)
asyncio.run(main())
