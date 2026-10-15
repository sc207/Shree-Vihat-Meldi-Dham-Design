"""First screen (no scroll) of chosen boards at chosen device sizes, as one labelled sheet.
usage: python3 first_screens.py PORT OUT.jpg Board1,Board2 WxH,WxH [--big] [--scale 0.5]"""
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import FIX, clock_script, launch
PORT, OUT, BOARDS, SIZES = int(sys.argv[1]), sys.argv[2], sys.argv[3].split(','), [tuple(map(int, s.split('x'))) for s in sys.argv[4].split(',')]
SC = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
async def main():
    tiles = []
    async with async_playwright() as p:
        br = await launch(p)
        for b in BOARDS:
            for (W, H) in SIZES:
                ctx = await br.new_context(viewport={'width': W, 'height': H})
                await ctx.add_init_script(clock_script('2026-10-16T12:00:00+05:30', frozen=True, big_text='--big' in sys.argv))
                pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:%d/%s.dc.html' % (PORT, b)); await pg.wait_for_timeout(1100)
                await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W)); await pg.wait_for_timeout(500)
                f = '/tmp/_fs.png'; await pg.screenshot(path=f); im = Image.open(f).convert('RGB')
                im = im.resize((round(W * SC), round(H * SC))); t = Image.new('RGB', (im.width, im.height + 24), 'white'); t.paste(im, (0, 24))
                ImageDraw.Draw(t).text((4, 3), '%s %dx%d' % (b, W, H), fill=(0, 0, 0), font=F); tiles.append(t); await ctx.close()
        await br.close()
    maxw = 2400; rows = []; row = []; x = 0
    for t in tiles:
        if x + t.width > maxw and row: rows.append(row); row = []; x = 0
        row.append(t); x += t.width + 12
    rows.append(row)
    S = Image.new('RGB', (maxw, sum(max(t.height for t in r) + 12 for r in rows)), (110, 110, 110)); y = 0
    for r in rows:
        x = 0
        for t in r: S.paste(t, (x, y)); x += t.width + 12
        y += max(t.height for t in r) + 12
    S.save(OUT, quality=85); print(OUT, S.size)
asyncio.run(main())
