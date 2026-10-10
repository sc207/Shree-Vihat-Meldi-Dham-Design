import asyncio, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
        pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:8772/Seva.dc.html'); await pg.wait_for_timeout(1200)
        r = await pg.evaluate("""()=>{window.scrollTo(0,1500);const se=document.scrollingElement;
          const chain=[];for(let e=document.querySelector('.vx-seva');e;e=e.parentElement){const cs=getComputedStyle(e);chain.push(`${e.tagName}.${(e.className||'').toString().split(' ')[0]} h=${Math.round(e.getBoundingClientRect().height)} ov=${cs.overflow}/${cs.overflowY} pos=${cs.position}`)}
          return {scrollY: scrollY, seH: se.scrollHeight, inner: innerHeight, bodyH: document.body.scrollHeight, chain}}""")
        print(r['scrollY'], r['seH'], r['inner'], r['bodyH']); print('\n'.join(r['chain']))
        await b.close()
asyncio.run(main())
