#!/usr/bin/env python3
"""Frame heights: each board's root element has a fixed height = natural content height + 3 px,
taken at the tallest of the five daily times (some cards change between day and night).

usage: python3 tools/frame_heights.py --port 8772 --project <edited-copy>/project [--boards Main,HomeMobile]

Prints, per board: current frame, natural heights at the five times, and the frame it should have.
MenuMobile and OfflineMobile are phone-SCREEN boards (fixed 844 px, the height of a phone screen), not content-sized:
they are skipped.
When the frame must change, update BOTH places in the page: the root style `height: NNNNpx;` and
data-props `"height": NNNN`, and in canvas.json the board's "h" = min(frame, 8000) (the canvas caps boards at 8000).
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright
sys.path.insert(0, os.path.dirname(__file__))
from _common import FIX, DAILY_TIMES, clock_script, launch, boards

SCREEN_BOARDS = {'MenuMobile', 'OfflineMobile'}


async def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--port', type=int, required=True); ap.add_argument('--project', required=True); ap.add_argument('--boards')
    A = ap.parse_args(); want = set(A.boards.split(',')) if A.boards else None; changes = 0
    async with async_playwright() as p:
        b = await launch(p)
        for name, W, frame in boards(A.project):
            if want and name not in want:
                continue
            if name in SCREEN_BOARDS:
                print(f"{name:22} width {W:>5}  frame {frame:>6}  phone-screen board — fixed height, skipped", flush=True); continue
            hs = []
            for t in DAILY_TIMES:
                ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script(t, frozen=False))
                pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{A.port}/{name}.dc.html'); await pg.wait_for_timeout(1100)
                await pg.add_style_tag(content=FIX); await pg.wait_for_timeout(250)
                hs.append(await pg.evaluate("Math.ceil(document.querySelector('.vx-page').getBoundingClientRect().height)")); await ctx.close()
            should = max(hs) + 3; changes += should != frame
            print(f"{name:22} width {W:>5}  frame {frame:>6}  natural {hs}  -> should be {should}{'' if should == frame else '   <-- CHANGE'}", flush=True)
        await b.close()
    print('frames to change:', changes)

asyncio.run(main())
