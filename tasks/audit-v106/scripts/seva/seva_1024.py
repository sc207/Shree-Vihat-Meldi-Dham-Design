import asyncio, io, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageChops
from _common import FIX, clock_script, launch
async def shot(b,port,W):
    ctx=await b.new_context(viewport={'width':W,'height':900},device_scale_factor=1); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
    await pg.add_style_tag(content=FIX+' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}'%(W,W)); await pg.wait_for_timeout(400)
    box=await pg.evaluate("(()=>{const r=document.querySelector('.vx-seva > aside > .vx-yagna:last-child').getBoundingClientRect();return [Math.floor(r.left),Math.floor(r.top+scrollY),Math.ceil(r.right),Math.ceil(r.bottom+scrollY)]})()")
    what=await pg.evaluate("(y)=>{const out=new Set();for(const x of [100,300,500,700,900]){const e=document.elementFromPoint(x,y-scrollY);if(e)out.add(e.tagName.toLowerCase()+'.'+(e.className||'').toString().split(' ')[0])}return [...out]}", 0)
    im=Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); await ctx.close(); return im,box
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        a,box=await shot(b,8771,1024); a2,_=await shot(b,8771,1024); c,_=await shot(b,8772,1024)
        for name,x,y in (('v106 vs v106',a,a2),('v106 vs preview',a,c)):
            d=ImageChops.difference(x,y); m=Image.new('L',x.size,255); m.paste(0,box); d2=Image.composite(d,Image.new('RGB',x.size),m)
            bb=d2.getbbox(); print(name,'outside-card diff box',bb,'max',max(v[1] for v in d2.getextrema()) if bb else 0)
        bb=ImageChops.composite(ImageChops.difference(a,c),Image.new('RGB',a.size),Image.new('L',a.size,255)).getbbox()
        await b.close()
asyncio.run(main())
