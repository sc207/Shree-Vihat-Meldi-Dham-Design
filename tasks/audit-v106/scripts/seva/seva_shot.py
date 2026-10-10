import asyncio, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch
port, tag = int(sys.argv[1]), sys.argv[2]
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for W in (1440, 1280, 1100, 1024):
            ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
            await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W)); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f'work/shots/{tag}_{W}.png', full_page=True)
            info = await pg.evaluate("""()=>{const s=document.querySelector('section.vx-grow');const out=[];
              const walk=(e,d)=>{if(d>5)return;for(const c of e.children){const r=c.getBoundingClientRect();if(r.height<4)continue;out.push(' '.repeat(d*2)+c.tagName.toLowerCase()+'.'+(typeof c.className==='string'?c.className.split(' ').slice(0,3).join('.'):'')+` x=${Math.round(r.left)} w=${Math.round(r.width)} y=${Math.round(r.top+scrollY)} h=${Math.round(r.height)}`);walk(c,d+1);}};
              walk(s,0);return out.slice(0,60).join('\\n');}""")
            if W == 1440: print(info)
            await ctx.close()
        await b.close()
asyncio.run(main())
