#!/usr/bin/env python3
"""Layout check: runs tools/fullcheck.js on chosen boards at chosen widths, normal and large (અ+) text,
on a baseline server and an edited server, and reports only NEW problems.

usage: python3 tools/check_layout.py --base 8771 --new 8772 --boards NewTemple,NewTempleMobile \
                                     [--widths auto] [--time 2026-10-10T12:30:00+05:30]

--widths auto (default): desktop boards 1440,1280,1100,1024,900,834,768 · phone boards 430,390,360,320 ·
                         tablet/landscape home boards at their own width. Or give a list: --widths 1440,390
fullcheck.js flags: page wider than the screen (docW), elements past the edge, clipped text (x/y),
distorted images, button labels breaking inside the button, a year split from its month.
Exit code 1 when any run has a new problem.
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from _common import FIX, clock_script, launch

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = open(os.path.join(HERE, 'fullcheck.js')).read()
NATIVE = {'HomeTablet': 834, 'HomeTabletL': 1180, 'HomePhoneL': 844, 'MenuMobile': 390, 'OfflineMobile': 390}


def widths_for(board, arg):
    if arg != 'auto':
        return [int(w) for w in arg.split(',')]
    if board in NATIVE:
        return [NATIVE[board]]
    if board.endswith(('Mobile', 'Mobile2')):
        return [430, 390, 360, 320]
    return [1440, 1280, 1100, 1024, 900, 834, 768]


async def run(b, port, board, W, t, big):
    ctx = await b.new_context(viewport={'width': W, 'height': 900})
    await ctx.add_init_script(clock_script(t, frozen=True, big_text=big))
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(f'http://127.0.0.1:{port}/{board}.dc.html'); await pg.wait_for_timeout(1100)
    await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
    await pg.wait_for_timeout(350)
    r = await pg.evaluate(CHECK); r['errors'] = errs; await ctx.close(); return r


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--base', type=int, required=True); ap.add_argument('--new', type=int, required=True)
    ap.add_argument('--boards', required=True); ap.add_argument('--widths', default='auto'); ap.add_argument('--time', default='2026-10-10T12:30:00+05:30')
    A = ap.parse_args(); bad = 0; n = 0
    async with async_playwright() as p:
        b = await launch(p)
        for board in A.boards.split(','):
            for W in widths_for(board, A.widths):
                cells = []
                for big in (False, True):
                    base = await run(b, A.base, board, W, A.time, big); new = await run(b, A.new, board, W, A.time, big)
                    added = sorted(set(new['issues']) - set(base['issues']))
                    wide = new['docW'] > W
                    n += 1; bad += bool(added or wide or new['errors'])
                    cells.append(f"{'large' if big else 'normal'}: {'OK' if not (added or wide or new['errors']) else 'NEW ' + str(added) + (' page wider than screen' if wide else '') + (' JS errors ' + str(new['errors']) if new['errors'] else '')}")
                print(f'{board:22} {W:>5}  ' + '  |  '.join(cells), flush=True)
        await b.close()
    print(f'{n} runs, {bad} with new problems'); sys.exit(1 if bad else 0)

asyncio.run(main())
