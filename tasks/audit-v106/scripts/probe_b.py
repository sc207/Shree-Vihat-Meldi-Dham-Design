import asyncio, sys, io
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image
from _common import clock_script, launch
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        # 1) menu button behaviour at 390 and 1024
        for board,W in (('HomeMobile',390),('Seva',1024),('NewTempleMobile',390)):
            ctx=await b.new_context(viewport={'width':W,'height':800}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1200)
            if W>760: await pg.add_style_tag(content='.vx-page,.vm-root{width:%dpx!important;min-width:0!important}'%W); await pg.wait_for_timeout(300)
            info=await pg.evaluate("""()=>{const m=document.querySelector('.vm-menu-btn');if(!m)return 'no menu button';const cs=getComputedStyle(m);return {tag:m.tagName, visible: cs.display!=='none'&&m.getBoundingClientRect().width>0, expanded:m.getAttribute('aria-expanded'), parentLink: !!m.closest('a'), onclick: !!m.onclick}}""")
            url=pg.url
            try:
                await pg.click('.vm-menu-btn', timeout=3000); await pg.wait_for_timeout(500)
            except Exception as e: info['clickErr']=str(e)[:60]
            after=await pg.evaluate("()=>({url:location.href, expanded:(document.querySelector('.vm-menu-btn')||{}).getAttribute?document.querySelector('.vm-menu-btn').getAttribute('aria-expanded'):null, dialog: !!document.querySelector('.vm-mnav')})")
            print(board,W,info,'| after click:',after, '| navigated:', after['url']!=url)
            await ctx.close()
        # 2) close-ups of contrast flags
        targets=[('Main',1440,'.vx-live, .vm-hero [class*=count], .vm-hero .vx-cd','home_countdown'),('NewTemple',1440,'.vx-areas','nt_areas'),
                 ('PranPratishtha',1440,'.vx-pday.is-main, .vx-pday:nth-of-type(7)','pp_mainday'),('PranPratishtha',1440,'.vx-muhurat, [class*=muhurat]','pp_muhurat')]
        for board,W,sel,name in targets:
            ctx=await b.new_context(viewport={'width':W,'height':900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1300)
            await pg.add_style_tag(content='*{animation:none!important;transition:none!important}'); await pg.wait_for_timeout(300)
            loc=pg.locator(sel).first
            try:
                await loc.screenshot(path=f'work/audit/close_{name}.png'); print('shot',name)
            except Exception as e: print('no element for',name,sel,str(e)[:60])
            await ctx.close()
        await b.close()
asyncio.run(main())
