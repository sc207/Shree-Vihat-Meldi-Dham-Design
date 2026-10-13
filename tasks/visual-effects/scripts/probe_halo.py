# Probe: where is the golden hero glow (.vm-hero__halo) relative to the artwork it should sit behind?
# Measures, for each board and viewport, the glow's centre against the visible figure (image box minus transparent padding),
# with animations running (what visitors see) and with reduced motion (no animation).
# Usage: python3 work/fx/probe_halo.py [port] [out.json]
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
OUT = sys.argv[2] if len(sys.argv) > 2 else 'work/fx/halo_8771.json'
ALPHA = json.load(open('work/fx/alpha.json'))
VIEWS = [(320, 568), (360, 800), (375, 812), (390, 844), (430, 932), (600, 900), (768, 1024), (900, 1200), (1024, 768), (1100, 800), (1180, 820),
         (1280, 800), (1366, 768), (1440, 900), (1920, 1080), (844, 390), (932, 430)]
PAGES = [('Main', 'HomeMobile'), ('NewTemple', 'NewTempleMobile'), ('PranPratishtha', 'PranPratishthaMobile')]
NATIVE = [('HomeTablet', 834, 1112), ('HomeTabletL', 1180, 820), ('HomePhoneL', 844, 390)]
WIDTH_FIX = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
JS = r'''(alpha) => {
  const hero = document.querySelector('.vm-hero'); const halo = hero && hero.querySelector('.vm-hero__halo'); if (!halo) return null;
  const imgs = [...hero.querySelectorAll('.vm-hero__art img')].filter(i => { const r = i.getBoundingClientRect(); const s = getComputedStyle(i); return r.width > 40 && s.display !== 'none' && s.visibility !== 'hidden' && i.offsetParent; });
  if (!imgs.length) return {noart: true};
  let L = 1e9, T = 1e9, R = -1e9, B = -1e9;
  for (const i of imgs) { const r = i.getBoundingClientRect(); const s = getComputedStyle(i); let x = r.left, y = r.top, w = r.width, h = r.height;
    if (s.objectFit === 'contain' && i.naturalWidth) { const k = Math.min(w / i.naturalWidth, h / i.naturalHeight); const cw = i.naturalWidth * k, ch = i.naturalHeight * k; x += (w - cw) / 2; y += (h - ch) / 2; w = cw; h = ch; }
    const id = (i.getAttribute('src') || '').split('/').pop(); const a = alpha[id] || [0, 0, 1, 1];
    L = Math.min(L, x + a[0] * w); T = Math.min(T, y + a[1] * h); R = Math.max(R, x + a[2] * w); B = Math.max(B, y + a[3] * h); }
  const hr = halo.getBoundingClientRect(); const hs = getComputedStyle(halo); const sy = scrollY;
  const art = {l: L, t: T + sy, r: R, b: B + sy, cx: (L + R) / 2, cy: (T + B) / 2 + sy, w: R - L, h: B - T};
  const glow = {cx: hr.left + hr.width / 2, cy: hr.top + hr.height / 2 + sy, d: hr.width};
  const heroR = hero.getBoundingClientRect();
  return {art, glow, dx: (glow.cx - art.cx) / art.h, dy: (glow.cy - art.cy) / art.h, inside: glow.cx >= L && glow.cx <= R && glow.cy - sy >= T && glow.cy - sy <= B,
          transform: hs.transform, anim: hs.animationName, heroW: heroR.width, heroH: heroR.height, n: imgs.length};
}'''

async def measure(b, board, W, H, motion, resize_from=None):
    ctx = await b.new_context(viewport={'width': (resize_from or (W, H))[0], 'height': (resize_from or (W, H))[1]}, reduced_motion=motion)
    await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(900)
    w0 = (resize_from or (W, H))[0]
    await pg.add_style_tag(content=WIDTH_FIX % (w0, w0))
    if resize_from:
        await pg.wait_for_timeout(400)
        await pg.evaluate('(t) => { for (const s of document.querySelectorAll("style")) if (s.textContent.startsWith(".vx-page,.vm-root{width:")) s.remove(); }', None)
        await pg.add_style_tag(content=WIDTH_FIX % (W, W)); await pg.set_viewport_size({'width': W, 'height': H})
    await pg.wait_for_timeout(2600)
    r = await pg.evaluate(JS, ALPHA); await ctx.close(); return r

async def main():
    res = {}
    async with async_playwright() as p:
        b = await launch(p)
        runs = []
        for desk, phone in PAGES:
            for W, H in VIEWS:
                runs.append((phone if W <= 760 else desk, W, H, None))
        for board, W, H in NATIVE: runs.append((board, W, H, None))
        runs.append(('PranPratishtha', 1024, 768, (768, 1024)))   # portrait → landscape without reload
        runs.append(('PranPratishtha', 768, 1024, (1024, 768)))   # landscape → portrait without reload
        for board, W, H, rf in runs:
            for motion in ('no-preference', 'reduce'):
                r = await measure(b, board, W, H, motion, rf)
                key = f'{board}|{W}x{H}|{motion}' + (f'|from{rf[0]}x{rf[1]}' if rf else '')
                res[key] = r
                if r and not r.get('noart'):
                    print(f'{key:55s} glow-art dx {r["dx"]:+.2f} dy {r["dy"]:+.2f} inside {r["inside"]!s:5s} glow d {r["glow"]["d"]:.0f} art {r["art"]["w"]:.0f}x{r["art"]["h"]:.0f}', flush=True)
                else:
                    print(key, r, flush=True)
        await b.close()
    json.dump(res, open(OUT, 'w'), indent=0)

asyncio.run(main())
