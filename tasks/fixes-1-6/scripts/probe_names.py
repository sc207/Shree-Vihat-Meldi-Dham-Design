# How many festival artist names break onto more than one line, per width and text size.
import asyncio, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT=int(sys.argv[1]); TAG=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        for big in (False, True):
            row=[]
            for W in (320, 340, 360, 375, 390, 430, 540, 700):
                ctx=await b.new_context(viewport={'width':W,'height':800}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
                pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/PranPratishthaMobile.dc.html'); await pg.wait_for_timeout(900)
                await pg.add_style_tag(content='.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'%(W,W)); await pg.wait_for_timeout(200)
                r=await pg.evaluate('''() => { const out={wrapped:0, total:0, spill:0, names:[]}; for (const li of document.querySelectorAll('.vx-night__who li')) { const rg=document.createRange(); const t=[...li.childNodes].find(n=>n.nodeType===3 && n.textContent.trim()); if(!t) continue; rg.selectNodeContents(t); const lines=new Set([...rg.getClientRects()].map(q=>Math.round(q.top))).size; out.total++; if(lines>1){out.wrapped++; out.names.push(t.textContent.trim());}
                   const card=li.closest('.vx-night').getBoundingClientRect(); const q=rg.getBoundingClientRect(); if(q.right>card.right-1) out.spill++; } return out; }''')
                row.append(f"{W}:{r['wrapped']}/{r['total']}" + (f" spill{r['spill']}" if r['spill'] else '')); await ctx.close()
            print(TAG, 'large' if big else 'normal', ' '.join(row), flush=True)
        await b.close()
asyncio.run(main())
