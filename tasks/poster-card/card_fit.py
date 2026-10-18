import asyncio,sys
sys.path.insert(0,'tools')
from playwright.async_api import async_playwright
from PIL import Image, ImageDraw, ImageFont
from _common import FIX, clock_script, launch
P=sys.argv[1]
FIND='''()=>{for(const h of document.querySelectorAll('h3')){if(!/મહોત્સવની તૈયારી/.test(h.textContent))continue;let c=h;for(let k=0;k<6&&c&&!c.querySelector('img');k++)c=c.parentElement;if(c&&c.querySelector('img').offsetParent)return c;}}'''
async def m():
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22); tiles=[]
  async with async_playwright() as p:
    b=await launch(p)
    for board,W,lab in (('Main',1440,'Home · laptop 1440'),('Main',1024,'Home · 1024 (3:2 box)'),('HomeTablet',834,'Home · tablet 834'),('HomeMobile2',390,'Home · phone 390'),('HomeMobile2',320,'Home · phone 320'),('Gallery',768,'Gallery · tablet 768')):
      c=await b.new_context(viewport={'width':W,'height':900},device_scale_factor=2); await c.add_init_script(clock_script('2026-10-18T16:50:00+05:30',frozen=True))
      pg=await c.new_page(); await pg.goto(f'http://127.0.0.1:8774/{board}.dc.html'); await pg.wait_for_timeout(900)
      await pg.add_style_tag(content=FIX+' .vx-abar{display:none!important} .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}'%(W,W))
      card=await pg.evaluate_handle(FIND)
      await card.evaluate('c=>{const i=c.querySelector("img");i.src="/_blob/aaaa00000000000000000000000c4a3a";i.removeAttribute("loading")}'); await pg.wait_for_timeout(700)
      f=f'{P}/c2_{board}_{W}.png'; await card.as_element().screenshot(path=f); tiles.append((lab,Image.open(f).convert('RGB'))); await c.close()
    await b.close()
  g=24; cols=3; rows=[tiles[:3],tiles[3:]]
  W=sum(i.width for _,i in rows[0])+g*4; H=sum(max(i.height for _,i in r)+60 for r in rows)+g
  S=Image.new('RGB',(max(W,sum(i.width for _,i in rows[1])+g*4),H),(245,240,232)); d=ImageDraw.Draw(S); y=g
  for r in rows:
    x=g
    for lab,im in r: d.text((x,y),lab,fill=(60,30,40),font=font); S.paste(im,(x,y+34)); x+=im.width+g
    y+=max(i.height for _,i in r)+60
  if S.width>2400: S=S.resize((2400,round(S.height*2400/S.width)))
  S.save(f'{P}/card_fit_4x3.png'); print(S.size)
asyncio.run(m())
