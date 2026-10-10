# Audit Phase A — automated inventory of the live v106 design (served on 8771). Read-only.
import asyncio, json, os, sys, re
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import FIX, clock_script, launch

PORT = 8771
CHECK = open('tools/fullcheck.js').read()
PROJ = 'design/project'
FILES = set(f for f in os.listdir(PROJ) if f.endswith('.dc.html'))
PHONE_W = [320, 360, 390, 430, 540]
DESK_W = [768, 900, 1024, 1280, 1440, 1920]
GROUPS = [('Home', ['HomeMobile', 'HomeMobile2'], 'Main'), ('NewTemple', ['NewTempleMobile'], 'NewTemple'),
          ('PranPratishtha', ['PranPratishthaMobile'], 'PranPratishtha'), ('Seva', ['SevaMobile'], 'Seva'),
          ('Gallery', ['GalleryMobile'], 'Gallery'), ('History', ['HistoryMobile'], 'History'), ('Contact', ['ContactMobile'], 'Contact'),
          ('Darshan', ['DarshanMobile'], 'Darshan'), ('NotFound', ['NotFoundMobile'], 'NotFound'), ('Menu', ['MenuMobile'], None),
          ('Offline', ['OfflineMobile'], None)]
NATIVE = [('HomeTablet', 834), ('HomeTabletL', 1180), ('HomePhoneL', 844)]

PROBE = r"""(files) => {
 const vis = e => { const cs = getComputedStyle(e); if (cs.display==='none'||cs.visibility==='hidden'||+cs.opacity===0) return false; const r=e.getBoundingClientRect(); return r.width>0&&r.height>0; };
 const W = innerWidth, H = innerHeight, out = {};
 const lab = e => (e.tagName.toLowerCase() + (e.id?'#'+e.id:'') + (typeof e.className==='string'&&e.className.trim()?'.'+e.className.trim().split(/\s+/)[0]:'')) + ' "' + (e.innerText||e.getAttribute('aria-label')||e.getAttribute('alt')||'').trim().replace(/\s+/g,' ').slice(0,30) + '"';
 // headings
 const hs=[...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis).map(h=>[+h.tagName[1], h.innerText.trim().replace(/\s+/g,' ').slice(0,40)]);
 out.h1 = hs.filter(h=>h[0]===1).length; out.headSkips=[]; for(let i=1;i<hs.length;i++) if(hs[i][0]>hs[i-1][0]+1) out.headSkips.push(`h${hs[i-1][0]}→h${hs[i][0]} at "${hs[i][1]}"`);
 out.landmarks = {header: document.querySelectorAll('header').length, nav: document.querySelectorAll('nav').length, main: document.querySelectorAll('main,[role=main]').length, footer: document.querySelectorAll('footer').length};
 const firstLink = [...document.querySelectorAll('a,button')].find(vis) || document.querySelector('a');
 out.skipLink = !!document.querySelector('a[href^="#"]') && /જાઓ/.test((document.querySelector('a[href^="#"]')||{}).textContent||'');
 // images
 out.imgs=[]; for (const im of document.querySelectorAll('img')) { const r=im.getBoundingClientRect(); const v=vis(im);
   const rec={src:(im.getAttribute('src')||'').slice(-32), alt: im.hasAttribute('alt')? im.getAttribute('alt'): null, nat:[im.naturalWidth,im.naturalHeight], ren:[Math.round(r.width),Math.round(r.height)], lazy: im.loading==='lazy', inFirstView: v && r.top < H && r.bottom > 0, dims: im.hasAttribute('width')&&im.hasAttribute('height'), fit:getComputedStyle(im).objectFit, visible:v, complete: im.complete};
   out.imgs.push(rec); }
 // touch targets
 out.small=[]; for (const e of document.querySelectorAll('a[href],button,input,select,textarea,[role=button],label.vm-check,label.vm-choice')) { if(!vis(e)) continue; const r=e.getBoundingClientRect();
   const inlineText = e.tagName==='A' && getComputedStyle(e).display==='inline' && e.closest('p,li,dd,small');
   if (inlineText) continue; const m=Math.min(r.width,r.height); if (m<24) out.small.push(`${lab(e)} ${Math.round(r.width)}×${Math.round(r.height)}`); }
 // contrast
 const parse = c => { const m=c.match(/rgba?\(([^)]+)\)/); if(!m) return null; const p=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}; };
 const L = c => { const f=v=>{v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)}; return 0.2126*f(c.r)+0.7152*f(c.g)+0.0722*f(c.b); };
 const blend=(fg,bg)=>({r:fg.r*fg.a+bg.r*(1-fg.a),g:fg.g*fg.a+bg.g*(1-fg.a),b:fg.b*fg.a+bg.b*(1-fg.a),a:1});
 out.lowContrast=[]; out.contrastSkipped=0; const seen=new Set();
 for (const e of document.querySelectorAll('body *')) { if (e instanceof SVGElement) continue; const own=[...e.childNodes].some(n=>n.nodeType===3&&n.nodeValue.trim().length>1); if(!own||!vis(e)) continue;
   const cs=getComputedStyle(e); let fg=parse(cs.color); if(!fg) continue; let bg=null, complex=false;
   for (let p=e; p; p=p.parentElement) { const pc=getComputedStyle(p); if (pc.backgroundImage!=='none') { complex=true; break; } const b=parse(pc.backgroundColor); if (b && b.a>0) { bg = b.a<1 ? blend(b,{r:251,g:247,b:239,a:1}) : b; break; } }
   if (complex||!bg) { out.contrastSkipped++; continue; } fg = fg.a<1 ? blend(fg,bg) : fg;
   const l1=L(fg), l2=L(bg), ratio=(Math.max(l1,l2)+0.05)/(Math.min(l1,l2)+0.05); const fs=parseFloat(cs.fontSize), fw=+cs.fontWeight; const large= fs>=24 || (fs>=18.66 && fw>=700);
   const need = large?3:4.5; if (ratio < need) { const k=lab(e)+' '+ratio.toFixed(2); if(!seen.has(k)){seen.add(k); out.lowContrast.push(`${lab(e)} ${ratio.toFixed(2)}:1 (${fs}px${large?' large':''}) fg ${cs.color} bg rgb(${Math.round(bg.r)},${Math.round(bg.g)},${Math.round(bg.b)})`);} } }
 // links
 out.badLinks=[]; for (const a of document.querySelectorAll('a[href]')) { const h=a.getAttribute('href'); if(/^(https?:|tel:|mailto:|data:)/.test(h)) continue;
   const [file,hash]=h.split('#'); if (file && !files.includes(file)) out.badLinks.push(`${lab(a)} → ${h} (no such page)`); else if (!file && hash && !document.getElementById(hash)) out.badLinks.push(`${lab(a)} → #${hash} (no such id)`); }
 // header + hero
 const hero=document.querySelector('section.vm-hero'), header=document.querySelector('header.vm-header');
 if (hero) { const hr=hero.getBoundingClientRect(), he=header?header.getBoundingClientRect():null; const h1=hero.querySelector('h1'); const h1r=h1?h1.getBoundingClientRect():null;
   const cont=[...hero.querySelectorAll('h1,p,a.vm-btn,.vm-btn,time,small')].filter(vis).map(e=>e.getBoundingClientRect());
   const art=[...hero.querySelectorAll('img')].filter(vis).map(im=>{const r=im.getBoundingClientRect(); let clip={l:-1e9,t:-1e9,r:1e9,b:1e9}; for(let p=im.parentElement;p&&p!==document.body;p=p.parentElement){const pc=getComputedStyle(p); if(pc.overflow!=='visible'||pc.overflowX!=='visible'||pc.overflowY!=='visible'){const q=p.getBoundingClientRect(); clip={l:Math.max(clip.l,q.left),t:Math.max(clip.t,q.top),r:Math.min(clip.r,q.right),b:Math.min(clip.b,q.bottom)};}}
     const vw=Math.max(0,Math.min(r.right,clip.r,W)-Math.max(r.left,clip.l,0)), vh=Math.max(0,Math.min(r.bottom,clip.b)-Math.max(r.top,clip.t)); return {src:(im.getAttribute('src')||'').slice(-8), alt:im.getAttribute('alt'), shown: +(vw*vh/(r.width*r.height)).toFixed(3), w:Math.round(r.width), h:Math.round(r.height), fit:getComputedStyle(im).objectFit};});
   out.hero={heroH:Math.round(hr.height), heroTop:Math.round(hr.top), headerBottom: he?Math.round(he.bottom):null, h1Top: h1r?Math.round(h1r.top):null, h1Lines: h1r? Math.round(h1r.height/parseFloat(getComputedStyle(h1).lineHeight||40)) : null,
     contentBelowHero: cont.some(r=>r.bottom>hr.bottom+1), textUnderHeader: he? cont.some(r=>r.top<he.bottom-1 && r.bottom>he.top): false, firstViewportFits: hr.bottom<=H, art}; }
 // fonts and gujarati letter-spacing
 out.fonts={hind: document.fonts.check('16px "Hind Vadodara"','અ'), noto: document.fonts.check('16px "Noto Serif Gujarati"','અ')};
 out.gujLetterSpacing=[...document.querySelectorAll('body *')].filter(e=>{if(!vis(e))return false; const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.nodeValue).join(''); if(!/[઀-૿]/.test(t)) return false; const ls=getComputedStyle(e).letterSpacing; return ls!=='normal' && parseFloat(ls)>=1;}).map(e=>`${lab(e)} ${getComputedStyle(e).letterSpacing}`).slice(0,12);
 out.cls = (window.__cls||0);
 return out; }"""

INIT_CLS = "window.__cls=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__cls+=e.value}}).observe({type:'layout-shift',buffered:true})}catch(e){}"


async def render(b, board, W, big=False):
    ctx = await b.new_context(viewport={'width': W, 'height': 900 if W > 760 else 780})
    await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    await ctx.add_init_script(INIT_CLS)
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1500)
    cls = await pg.evaluate('window.__cls||0')
    await pg.add_style_tag(content=FIX + ' .vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important}' % (W, W))
    await pg.wait_for_timeout(350)
    full = await pg.evaluate(CHECK)
    probe = await pg.evaluate(PROBE, sorted(FILES))
    probe['clsLoad'] = round(cls, 4); probe['full'] = full['issues']; probe['docW'] = full['docW']; probe['errors'] = errs
    return ctx, pg, probe


async def focus_and_buttons(b, board, W):
    """keyboard focus visibility (first 30 tab stops) + buttons that change nothing when clicked"""
    ctx, pg, _ = await render(b, board, W)
    await pg.evaluate('window.scrollTo(0,0)')
    focus = []
    for i in range(30):
        await pg.keyboard.press('Tab'); await pg.wait_for_timeout(30)
        f = await pg.evaluate("""()=>{const e=document.activeElement; if(!e||e===document.body) return null; const cs=getComputedStyle(e); const r=e.getBoundingClientRect();
            const ring = (cs.outlineStyle!=='none' && parseFloat(cs.outlineWidth)>0) || (cs.boxShadow && cs.boxShadow!=='none');
            return {el:(e.tagName.toLowerCase()+' "'+(e.innerText||e.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,24)+'"'), ring, outline: cs.outlineStyle+' '+cs.outlineWidth, shadow: (cs.boxShadow||'').slice(0,40), onScreen: r.width>0&&r.height>0}}""")
        if f: focus.append(f)
    # dead buttons: click each visible button via JS, see whether anything changes
    n = await pg.evaluate("document.querySelectorAll('button').length")
    dead = []
    for i in range(n):
      try:
        r = await pg.evaluate("""(i)=>{const b=document.querySelectorAll('button')[i]; if(!b) return null; const cs=getComputedStyle(b); const r=b.getBoundingClientRect(); if(cs.display==='none'||cs.visibility==='hidden'||!r.width) return null;
            const snap=document.body.innerHTML; window.__snap=snap; window.__href=location.href; b.click(); return (b.innerText||b.getAttribute('aria-label')||'').trim().replace(/\\s+/g,' ').slice(0,30)}""", i)
        if r is None: continue
        await pg.wait_for_timeout(250)
        changed = await pg.evaluate("()=>document.body.innerHTML!==window.__snap || location.href!==window.__href")
        if not changed: dead.append(r)
      except Exception as e:
        dead.append(f'(button {i}: navigation or error — {str(e)[:40]})')
        await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1200)
    await ctx.close()
    return focus, dead


async def main():
    res = {}
    async with async_playwright() as p:
        b = await launch(p)
        jobs = []
        for g, phones, desk in GROUPS:
            for ph in phones:
                for W in PHONE_W: jobs.append((g, ph, W))
            if desk:
                for W in DESK_W: jobs.append((g, desk, W))
        for board, W in NATIVE: jobs.append(('Home', board, W))
        for g, board, W in jobs:
            for big in (False, True):
                if big and W not in (390, 1440, 320, 1024): continue
                ctx, pg, probe = await render(b, board, W, big)
                await ctx.close()
                res[f'{board}|{W}|{"big" if big else "std"}'] = probe
            print(g, board, W, flush=True)
        # focus + dead buttons at 1440 and 390
        fb = {}
        for g, phones, desk in GROUPS:
            for board, W in ([(desk, 1440)] if desk else []) + [(phones[0], 390)]:
                fb[f'{board}|{W}'] = await focus_and_buttons(b, board, W)
                print('focus/buttons', board, W, flush=True)
        # reduced motion: animations still running
        rm = {}
        for g, phones, desk in GROUPS:
            board = desk or phones[0]; W = 1440 if desk else 390
            for mode in ('no-preference', 'reduce'):
                ctx = await b.new_context(viewport={'width': W, 'height': 900}, reduced_motion=mode)
                await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
                pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:{PORT}/{board}.dc.html'); await pg.wait_for_timeout(1500)
                rm[f'{board}|{mode}'] = await pg.evaluate("""()=>{const out=[];for(const a of document.getAnimations()){const t=a.effect&&a.effect.target; const ti=a.effect.getComputedTiming(); out.push({el: t? (t.tagName.toLowerCase()+'.'+((t.className&&t.className.baseVal!==undefined)?t.className.baseVal:t.className||'').toString().split(' ')[0]):'?', name: a.animationName||a.transitionProperty||a.constructor.name, iterations: ti.iterations, duration: Math.round(ti.duration||0), state:a.playState, timeline: a.timeline && a.timeline.constructor ? a.timeline.constructor.name : ''})} return out}""")
                await ctx.close()
        await b.close()
    json.dump({'renders': res, 'focus_buttons': fb, 'motion': rm}, open('work/audit/phaseA.json', 'w'), ensure_ascii=False, indent=0)
    print('saved', len(res), 'renders')

asyncio.run(main())
