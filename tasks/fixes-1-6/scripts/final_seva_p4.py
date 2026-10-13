import asyncio, io, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageChops
from _common import FIX, clock_script, launch
LIST = """()=>[...document.querySelectorAll('*')].filter(e=>['sticky','fixed'].includes(getComputedStyle(e).position)).map(e=>{const r=e.getBoundingClientRect();return `${e.tagName.toLowerCase()}.${(e.className||'').toString().split(' ')[0]} ${getComputedStyle(e).position} display=${getComputedStyle(e).display} y=${Math.round(r.top)}`})"""
PSEUDO = "()=>{const cs=getComputedStyle(document.querySelector('.vx-page'),'::after');return cs.position+' '+cs.display+' top='+cs.top}"
DECOR = """()=>{const s=document.querySelector('.vx-seva').closest('section');const R=s.getBoundingClientRect();
  return [...s.querySelectorAll('*')].filter(e=>{const cs=getComputedStyle(e);return cs.position==='absolute'||e.tagName==='svg'&&e.getAttribute('aria-hidden')==='true'}).map(e=>{const r=e.getBoundingClientRect();return {el:e.tagName.toLowerCase()+'.'+((e.className&&e.className.baseVal!==undefined)?e.className.baseVal:e.className).toString().split(' ')[0], outside: r.left<R.left||r.right>R.right||r.top<R.top||r.bottom>R.bottom}}).filter(x=>x.outside)}"""
async def main():
    async with async_playwright() as p:
        b=await launch(p)
        for port,tag in ((8771,'v109'),(8786,'preview')):
            ctx=await b.new_context(viewport={'width':1440,'height':900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
            out=[]
            for y in (0,1500,2600):
                await pg.evaluate('window.scrollTo({top:%d,behavior:"instant"})'%y); await pg.wait_for_timeout(80)
                out.append((y, await pg.evaluate(LIST), await pg.evaluate(PSEUDO)))
            print(tag); [print('  scroll',y,'sticky/fixed:',l,'| page ::after bar:',ps) for y,l,ps in out]
            print('  decorative elements reaching outside the section (these are what overflow clips):', await pg.evaluate(DECOR))
            await ctx.close()
        # static full-page at several desktop widths, ignoring the help card box
        for W in (1024,1100,1280,1440):
            ims=[]
            for port in (8771,8786):
                ctx=await b.new_context(viewport={'width':W,'height':900},device_scale_factor=1); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
                await pg.add_style_tag(content=FIX+' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}'%(W,W)); await pg.wait_for_timeout(400)
                box=await pg.evaluate("(()=>{const r=document.querySelector('.vx-seva > aside > .vx-yagna:last-child').getBoundingClientRect();return [Math.floor(r.left),Math.floor(r.top+scrollY),Math.ceil(r.right),Math.ceil(r.bottom+scrollY)]})()")
                ims.append((Image.open(io.BytesIO(await pg.screenshot(full_page=True))).convert('RGB'),box)); await ctx.close()
            (a,box),(c,_)=ims
            d=ImageChops.difference(a,c); m=Image.new('L',a.size,255); m.paste(0,box); d2=Image.composite(d,Image.new('RGB',a.size),m)
            print(f'static page {W}px: identical outside the help card: {d2.getbbox() is None}; inside the card max diff {max(x[1] for x in d.crop(box).getextrema())}/255')
        await b.close()
asyncio.run(main())
