"""Contrast of photo captions (white text over photos): background under each caption line measured with the text hidden.
usage: cap_contrast.py PORT OUT.json Board@W[,...]"""
import asyncio, sys, json, io
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image
import numpy as np
from _common import FIX, clock_script, launch
PORT, OUT, SPEC = int(sys.argv[1]), sys.argv[2], sys.argv[3]
def lin(c): c = c / 255; return np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def L(rgb): r, g, b = lin(rgb[..., 0]), lin(rgb[..., 1]), lin(rgb[..., 2]); return 0.2126 * r + 0.7152 * g + 0.0722 * b
async def main():
    res = []
    async with async_playwright() as p:
        br = await launch(p)
        for item in SPEC.split(','):
            b, W = item.split('@'); W = int(W)
            ctx = await br.new_context(viewport={'width': W, 'height': 900 if W > 760 else 844}, device_scale_factor=1)
            await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True))
            pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(1000)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important} .vx-abar,.vm-tabbar,[class*="tabbar"]{display:none!important}' % (W, W))
            await pg.evaluate('async () => { const h = document.documentElement.scrollHeight; for (let y = 0; y < h; y += innerHeight) { scrollTo({top: y, behavior: "instant"}); await new Promise(r => setTimeout(r, 40)); } scrollTo({top: 0, behavior: "instant"}); }')
            await pg.wait_for_timeout(400)
            caps = await pg.evaluate('''() => [...document.querySelectorAll('figure figcaption')].filter(c => { const f = c.closest('figure'); const i = f.querySelector('img'); if (!i) return false;
                 const s = getComputedStyle(c); const r = c.getBoundingClientRect(), q = i.getBoundingClientRect(); return s.position === 'absolute' && r.width > 0 && r.height > 0 && r.top >= q.top - 2 && r.bottom <= q.bottom + 2; })
               .map((c, k) => { c.setAttribute('data-cc', k); const rng = document.createRange(); rng.selectNodeContents(c); const rs = [...rng.getClientRects()].filter(x => x.width > 2);
                 const sy = scrollY; return {k, text: c.textContent.trim().slice(0, 40), color: getComputedStyle(c).color, shadow: getComputedStyle(c).textShadow, rects: rs.map(x => [x.left, x.top + sy, x.width, x.height])}; })''')
            await pg.add_style_tag(content='figcaption[data-cc]{color:transparent!important;text-shadow:none!important} figcaption[data-cc] *{color:transparent!important;text-shadow:none!important}')
            await pg.wait_for_timeout(200)
            png = await pg.screenshot(full_page=True); im = np.asarray(Image.open(io.BytesIO(png)).convert('RGB')).astype(np.float32)
            for c in caps:
                rgb = np.array([float(v) for v in c['color'][c['color'].index('(') + 1:-1].split(',')[:3]])
                Lt = float(L(rgb[None, None, :])[0, 0]); worst = 99
                for x, y, w, h in c['rects']:
                    x0, y0 = int(max(0, x)), int(max(0, y)); reg = im[y0:int(y + h), x0:int(x + w)]
                    if reg.size == 0: continue
                    Lb = np.percentile(L(reg), 90)                      # bright parts of the background behind the letters
                    cr = (max(Lt, Lb) + 0.05) / (min(Lt, Lb) + 0.05); worst = min(worst, cr)
                res.append({'board': b, 'W': W, 'text': c['text'], 'contrast90': round(float(worst), 2), 'shadow': c['shadow'] != 'none'})
            await ctx.close()
        await br.close()
    json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=0)
    for r in res: print('%-14s %5d  %5.2f %s  %s' % (r['board'], r['W'], r['contrast90'], 'sh' if r['shadow'] else '  ', r['text']))
asyncio.run(main())
