import asyncio, io, sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageChops, ImageDraw, ImageFont
from _common import FIX, clock_script, launch
INSTANT = 'window.scrollTo({top:%d,behavior:"instant"})'
MEASURE = """()=>{const q=s=>document.querySelector(s); const R=e=>e.getBoundingClientRect();
 const card=R(q('.vx-seva > aside > .vx-yagna:last-child')), form=R(q('.vx-seva form')), aside=R(q('.vx-seva > aside')), foot=R(q('.vm-footer'));
 const fields=[...document.querySelectorAll('.vx-seva form input, .vx-seva form textarea, .vx-seva form label, .vx-seva form button, .vx-seva form .vm-choices > *, .vx-seva form .vx-days > *, .vx-seva form .vx-shifts > *')].map(R);
 const hit=r=>!(r.right<=card.left||r.left>=card.right||r.bottom<=card.top||r.top>=card.bottom);
 return {overlapsField: fields.filter(r=>r.width&&hit(r)).length, overlapsForm: hit(form), gapToForm: Math.round(card.left-form.right),
         insideColumn: card.bottom<=aside.bottom+0.5 && card.top>=aside.top-0.5, clearOfFooter: card.bottom<=foot.top+0.5, cardTop: Math.round(card.top), cardBottom: Math.round(card.bottom), vh: innerHeight}}"""
async def main():
    F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
    async with async_playwright() as p:
        b=await launch(p)
        for W,H in ((1440,900),(1024,768)):
            sheet=[]
            for port,tag in ((8771,'v109 (live)'),(8772,'preview')):
                ctx=await b.new_context(viewport={'width':W,'height':H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg=await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{port}/Seva.dc.html'); await pg.wait_for_timeout(1200)
                await pg.add_style_tag(content='*{animation:none!important;transition:none!important} .vx-page,.vm-root{height:auto!important;min-height:0!important;width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W)); await pg.wait_for_timeout(300)
                g=await pg.evaluate("""()=>{const f=document.querySelectorAll('.vx-seva fieldset');const b=[...document.querySelectorAll('.vx-seva form button')].pop();const ft=document.querySelector('.vm-footer');
                    return {s3:f[2].getBoundingClientRect().top+scrollY, mid:f[2].getBoundingClientRect().top+scrollY+f[2].getBoundingClientRect().height/2, btn:b.getBoundingClientRect().top+scrollY, foot:ft.getBoundingClientRect().top+scrollY, formTop:document.querySelector('.vx-seva').getBoundingClientRect().top+scrollY, formBottom:document.querySelector('.vx-seva form').getBoundingClientRect().bottom+scrollY}}""")
                # every 100 px through the form: measure
                if port==8772:
                    bad=[]; n=0; y=int(g['formTop'])-150
                    while y < g['foot']:
                        await pg.evaluate(INSTANT % y); await pg.wait_for_timeout(40); m=await pg.evaluate(MEASURE); n+=1
                        if m['overlapsField'] or m['overlapsForm'] or not m['insideColumn'] or not m['clearOfFooter']: bad.append((y,m))
                    # sample report
                        y+=100
                    print(f'{W}x{H}: {n} scroll positions from above the form to the footer — problems: {len(bad)}; card–form gap {m["gapToForm"]} px', bad[:2])
                pics=[]
                for label,y in (('section 3 start',g['s3']-120),('middle of section 3',g['mid']-H/2),('submit button in view',g['btn']-H+120),('footer reached',g['foot']-H/2)):
                    await pg.evaluate(INSTANT % int(y)); await pg.wait_for_timeout(120)
                    im=Image.open(io.BytesIO(await pg.screenshot())).convert('RGB'); pics.append((label,im))
                sheet.append((tag,pics)); await ctx.close()
            # sheet: rows = positions, cols = v106 | preview
            sc=0.42; cw=int(W*sc); ch=int(H*sc); rows=len(sheet[0][1])
            o=Image.new('RGB',(cw*2+30, 40+rows*(ch+40)),'white'); d=ImageDraw.Draw(o)
            for ci,(tag,pics) in enumerate(sheet):
                d.text((ci*(cw+30)+4,8),f'{tag} · Seva {W}×{H}',font=F,fill=(90,20,35))
                for ri,(label,im) in enumerate(pics):
                    y0=40+ri*(ch+40); d.text((ci*(cw+30)+4,y0+4),label,font=F,fill=(80,80,80)); o.paste(im.resize((cw,ch),Image.LANCZOS),(ci*(cw+30),y0+32))
            o.save(f'work/shots/seva_sequence_{W}.png',optimize=True); print('saved',o.size)
        await b.close()
asyncio.run(main())
