# Probe: the devotional band (deity art + rotating mandala + section glow at 50% 60%): are mandala and glow centred on the art?
import asyncio, sys, json, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import clock_script, launch
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8771
ALPHA = json.load(open('work/fx/alpha.json'))
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 15)
JS = r'''(alpha) => { const sec = document.querySelector('.vm-devotional'); if (!sec) return null; sec.scrollIntoView({block: 'start', behavior: 'instant'});
  const R = e => e.getBoundingClientRect(); const s = R(sec);
  const imgs = [...sec.querySelectorAll('img')].filter(i => R(i).width > 30 && getComputedStyle(i).display !== 'none');
  let L = 1e9, T = 1e9, Rr = -1e9, B = -1e9;
  for (const i of imgs) { const r = R(i); const st = getComputedStyle(i); let x = r.left, y = r.top, w = r.width, h = r.height;
    if (st.objectFit === 'contain' && i.naturalWidth) { const k = Math.min(w / i.naturalWidth, h / i.naturalHeight); const cw = i.naturalWidth * k, ch = i.naturalHeight * k; x += (w - cw) / 2; y += (h - ch) / 2; w = cw; h = ch; }
    const a = alpha[(i.getAttribute('src') || '').split('/').pop()] || [0, 0, 1, 1];
    L = Math.min(L, x + a[0] * w); T = Math.min(T, y + a[1] * h); Rr = Math.max(Rr, x + a[2] * w); B = Math.max(B, y + a[3] * h); }
  const m = sec.querySelector('.vm-devotional__mandala'); const mr = m ? R(m) : null;
  const art = {cx: (L + Rr) / 2 - s.left, cy: (T + B) / 2 - s.top, w: Rr - L, h: B - T};
  return {sec: [Math.round(s.width), Math.round(s.height)], art, glow: {cx: s.width * .5, cy: s.height * .6}, mandala: mr ? {cx: mr.left + mr.width / 2 - s.left, cy: mr.top + mr.height / 2 - s.top, d: mr.width} : null, nimg: imgs.length, top: s.top}; }'''
async def main():
    async with async_playwright() as p:
        b = await launch(p); tiles = []
        for board, W, H in (('ContactMobile', 320, 568), ('ContactMobile', 390, 844), ('Contact', 768, 1024), ('Contact', 1024, 768), ('Contact', 1440, 900), ('Main', 1440, 900), ('HomeMobile2', 390, 844), ('PranPratishtha', 1920, 1080)):
            ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(900)
            await pg.add_style_tag(content='html{scroll-behavior:auto!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}' % (W, W)); await pg.wait_for_timeout(1200)
            r = await pg.evaluate(JS, ALPHA); await pg.wait_for_timeout(1500); r = await pg.evaluate(JS, ALPHA)
            a, g, m = r['art'], r['glow'], r['mandala']
            print(f"{board}@{W}: section {r['sec']}, art centre ({a['cx']:.0f},{a['cy']:.0f}) {a['w']:.0f}x{a['h']:.0f}; glow centre ({g['cx']:.0f},{g['cy']:.0f}) off by {g['cy']-a['cy']:+.0f}px; mandala centre ({m['cx']:.0f},{m['cy']:.0f}) d{m['d']:.0f} off by ({m['cx']-a['cx']:+.0f},{m['cy']-a['cy']:+.0f})px", flush=True)
            im = Image.open(io.BytesIO(await pg.screenshot(clip={'x': 0, 'y': max(0, r['top']), 'width': W, 'height': min(r['sec'][1], 1400)}))).convert('RGB')
            d = ImageDraw.Draw(im)
            for (x, y, c) in ((a['cx'], a['cy'], (60, 220, 90)), (g['cx'], g['cy'], (255, 200, 0)), (m['cx'], m['cy'], (80, 160, 255))):
                d.ellipse([x - 7, y - 7, x + 7, y + 7], outline=c, width=3)
            s = 420 / im.height; im = im.resize((int(im.width * s), 420)); t = Image.new('RGB', (max(im.width, 200), 446), 'white'); ImageDraw.Draw(t).text((2, 4), f'{board} {W}', font=FB, fill=(90, 20, 35)); t.paste(im, (0, 26)); tiles.append(t)
            await ctx.close()
        o = Image.new('RGB', (sum(t.width + 10 for t in tiles), 446), 'white'); x = 0
        for t in tiles: o.paste(t, (x, 0)); x += t.width + 10
        o.save('work/fx/diag_devotional.png'); print(o.size); await b.close()
asyncio.run(main())
