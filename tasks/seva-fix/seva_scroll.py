import asyncio, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for W,H in ((1440,900),(1280,800),(1100,800),(1024,768)):
            for port,tag in ((8771,'before'),(8772,'after')):
                ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
                await pg.add_style_tag(content='*{animation:none!important;transition:none!important} .vx-page,.vm-root{height:auto!important;min-height:0!important;width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W)); await pg.wait_for_timeout(300)
                geo = await pg.evaluate("""()=>{const f=document.querySelector('.vx-seva form').getBoundingClientRect(), a=document.querySelector('.vx-seva > aside').getBoundingClientRect();return {formTop:f.top+scrollY, formBottom:f.bottom+scrollY, asideBottom:a.bottom+scrollY}}""")
                rows=[]; empty=0; steps=0
                y=geo['formTop']-100
                while y < geo['formBottom']:
                    await pg.evaluate(f'window.scrollTo({{top:{y},behavior:"instant"}})'); await pg.wait_for_timeout(60)
                    r = await pg.evaluate("""()=>{const vh=innerHeight;const cards=[...document.querySelectorAll('.vx-seva > aside > *')].map(c=>c.getBoundingClientRect());
                       const vis=cards.map(c=>Math.max(0,Math.min(c.bottom,vh)-Math.max(c.top,0)));const help=cards[cards.length-1];
                       const f=document.querySelector('.vx-seva form').getBoundingClientRect(); const formVis=Math.max(0,Math.min(f.bottom,vh)-Math.max(f.top,0));
                       return {anyCard: vis.some(v=>v>40), helpVisible: vis[vis.length-1] >= help.height-1, helpTop: Math.round(help.top), formVis: Math.round(formVis)}}""")
                    if r['formVis']>200:
                        steps+=1; empty += not r['anyCard']
                    y+=150
                await pg.evaluate('window.scrollTo({top:document.body.scrollHeight,behavior:"instant"})'); await pg.wait_for_timeout(100)
                end = await pg.evaluate("""()=>{const h=document.querySelector('.vx-seva > aside > .vx-yagna:last-child').getBoundingClientRect(), a=document.querySelector('.vx-seva > aside').getBoundingClientRect(), ft=document.querySelector('.vm-footer').getBoundingClientRect();return {helpInsideColumn: h.bottom<=a.bottom+0.5, gapToFooter: Math.round(ft.top-h.bottom)}}""")
                print(f"{W}x{H} {tag:6}: scroll positions with the form in view: {steps} · with NO card on the right: {empty} · at page end: help card inside its column {end['helpInsideColumn']}, {end['gapToFooter']} px above the footer")
                if W==1440 and True:
                    # viewport picture with section ૩ in view
                    t = await pg.evaluate("document.querySelectorAll('.vx-seva fieldset')[2].getBoundingClientRect().top+scrollY")
                    await pg.evaluate(f'window.scrollTo({{top:{t-120},behavior:"instant"}})'); await pg.wait_for_timeout(150)
                    await pg.screenshot(path=f'work/shots/scroll_{tag}_{W}.png')
                await ctx.close()
        await b.close()
asyncio.run(main())
