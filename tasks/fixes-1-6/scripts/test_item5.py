import asyncio, sys, json
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT=int(sys.argv[1]); TAG=sys.argv[2]
async def main():
    out=[]
    async with async_playwright() as p:
        b=await launch(p)
        for big in (False, True):
            for W in (320, 325, 330, 335, 340, 345, 350, 355, 359, 360, 375, 390):
                ctx=await b.new_context(viewport={'width':W,'height':800}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
                pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/HomeMobile.dc.html'); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content='.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'%(W,W)); await pg.wait_for_timeout(200)
                r=await pg.evaluate('''() => { const bs=[...document.querySelectorAll('.vx-home-hero .vm-btn-row .vm-btn')]; return {btns: bs.map(b => { const rg=document.createRange(); rg.selectNodeContents(b); const t=rg.getBoundingClientRect(); const r=b.getBoundingClientRect();
                   return {room: Math.round(Math.min(t.left - r.left, r.right - t.right)), w: Math.round(r.width), h: Math.round(r.height), top: Math.round(r.top)}; }), overflow: document.documentElement.scrollWidth > innerWidth}; }''')
                rows=len(set(x['top'] for x in r['btns'])); ok = all(x['room'] >= 8 for x in r['btns']) and not r['overflow'] and all(x['h'] >= 44 for x in r['btns'])
                out.append({'W':W,'big':big,**r,'rows':rows,'ok':ok})
                print(TAG, 'big' if big else 'std', W, 'rows', rows, 'side room', [x['room'] for x in r['btns']], 'widths', [x['w'] for x in r['btns']], 'h', r['btns'][0]['h'], 'OK' if ok else 'CLIPPED/TIGHT', flush=True)
                await ctx.close()
        await b.close()
    json.dump(out, open(f'work/fix/evidence/item5/tests_{TAG}.json','w'), indent=1)
asyncio.run(main())
