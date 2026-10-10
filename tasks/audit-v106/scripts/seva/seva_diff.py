import asyncio, io, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageChops
from _common import FIX, clock_script, launch
async def shot(b,port,name,W):
    ctx=await b.new_context(viewport={'width':W,'height':900},device_scale_factor=1); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
    pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/{name}.dc.html'); await pg.wait_for_timeout(1200); await pg.add_style_tag(content=FIX); await pg.wait_for_timeout(400)
    box=await pg.evaluate("(()=>{const e=document.querySelector('.vx-seva > aside > .vx-yagna:last-child');if(!e)return null;const r=e.getBoundingClientRect();return [r.left,r.top+scrollY,r.width,r.height]})()") if name=='Seva' else None
    im=Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'); await ctx.close(); return im,box
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        for name,W in (('Seva',1440),('NewTemple',1440)):
            (a,ba),(c,bc)=await shot(b,8771,name,W),await shot(b,8772,name,W)
            d=ImageChops.difference(a,c); bb=d.getbbox(); ext=max(x[1] for x in d.getextrema())
            print(name,'diff box',bb,'max channel diff',ext,'help card box before/after',ba,bc)
            if bb:
                x0,y0,x1,y1=bb; pad=20; crop=(max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),y1+pad)
                o=Image.new('RGB',((crop[2]-crop[0])*2+20,crop[3]-crop[1]),'white'); o.paste(a.crop(crop),(0,0)); o.paste(c.crop(crop),(crop[2]-crop[0]+20,0)); o.save(f'work/shots/diff_{name}.png')
        await b.close()
asyncio.run(main())
