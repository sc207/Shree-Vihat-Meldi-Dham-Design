# Item 3 tests: Seva form errors at desktop and phone sizes. Port given; prints, per scenario, where focus went and whether it is on screen.
import asyncio, sys, json
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
PORT = int(sys.argv[1]); TAG = sys.argv[2] if len(sys.argv) > 2 else ''
WF = '.vx-page,.vm-root{width:%dpx!important;min-width:0!important;max-width:%dpx!important;height:auto!important;min-height:0!important}'
STATE = '''() => { const a = document.activeElement; const r = a.getBoundingClientRect(); const bar = document.querySelector('.vx-abar'); let bottom = innerHeight;
  if (bar && getComputedStyle(bar).display !== 'none') bottom = Math.min(bottom, bar.getBoundingClientRect().top);
  const inv = ['f-name', 'f-mob', 'f-city', 'f-agree'].map(id => { const e = document.getElementById(id); if (!e) return null; const d = e.getAttribute('aria-describedby'); const m = d && document.getElementById(d);
    return [id, e.getAttribute('aria-invalid'), m ? m.textContent.trim().slice(0, 22) : null]; });
  return {focus: a.id || (a.name ? 'seva:' + a.name : '') || a.className || a.tagName, onScreen: r.top >= 0 && r.bottom <= bottom + 1, top: Math.round(r.top), bottomLimit: Math.round(bottom),
    summary: !!document.querySelector('.vm-form .vm-alert[role=alert]'), errors: document.querySelectorAll('.vm-form .vm-field__error').length, inv,
    nameVal: (document.getElementById('f-name') || {}).value, mobVal: (document.getElementById('f-mob') || {}).value,
    success: (() => { const s = document.querySelector('.vx-success'); if (!s) return null; const q = s.getBoundingClientRect(); return {top: Math.round(q.top), visible: q.top < innerHeight && q.bottom > 0}; })()}; }'''
async def scenario(b, W, H, name, steps, big=False):
    ctx = await b.new_context(viewport={'width': W, 'height': H}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30', big_text=big))
    pg = await ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    await pg.goto(f'http://127.0.0.1:{PORT}/{"Seva" if W > 760 else "SevaMobile"}.dc.html'); await pg.wait_for_timeout(1000)
    await pg.add_style_tag(content=WF % (W, W)); await pg.wait_for_timeout(200)
    for st in steps:
        kind, arg = st
        if kind == 'fill': await pg.fill(arg[0], arg[1])
        elif kind == 'click': await pg.click(arg)
        elif kind == 'submit':
            btn = pg.locator('button', has_text='નોંધણી પૂર્ણ કરો').last; await btn.scroll_into_view_if_needed(); await btn.click(); await pg.wait_for_timeout(700)
        elif kind == 'submit-key':
            btn = pg.locator('button', has_text='નોંધણી પૂર્ણ કરો').last; await btn.scroll_into_view_if_needed(); await btn.focus(); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(700)
    s = await pg.evaluate(STATE); s['scenario'] = name; s['W'] = W; s['big'] = big; s['errs'] = errs
    if name.startswith('empty') and W in (390, 1440) and not big:
        await pg.screenshot(path=f'work/fix/evidence/item3/{TAG}_{name}_{W}.png')
    await ctx.close(); return s
SC = [
 ('empty', [('submit', None)], '#f-name'),
 ('name-only', [('fill', ('#f-name', 'રમેશભાઈ પટેલ')), ('submit', None)], '#f-mob'),
 ('mobile-9-digits', [('fill', ('#f-name', 'રમેશભાઈ પટેલ')), ('fill', ('#f-mob', '98765 4321')), ('fill', ('#f-city', 'સાણંદ')), ('submit', None)], '#f-mob'),
 ('only-consent-missing', [('fill', ('#f-name', 'રમેશભાઈ પટેલ')), ('fill', ('#f-mob', '98765 43210')), ('fill', ('#f-city', 'સાણંદ')), ('submit', None)], '#f-agree'),
 ('no-seva-chosen', [('fill', ('#f-name', 'રમેશભાઈ પટેલ')), ('fill', ('#f-mob', '98765 43210')), ('fill', ('#f-city', 'સાણંદ')), ('click', '.vm-choice:has(input:checked)'), ('click', '#f-agree, .vm-check input'), ('submit', None)], 'seva'),
 ('keyboard-submit-empty', [('submit-key', None)], '#f-name'),
 ('valid', [('fill', ('#f-name', 'રમેશભાઈ પટેલ')), ('fill', ('#f-mob', '98765 43210')), ('fill', ('#f-city', 'સાણંદ')), ('click', '#f-agree, .vm-check input'), ('submit', None)], 'success'),
]
async def main():
    out = []
    async with async_playwright() as p:
        b = await launch(p)
        for W, H, big in ((1440, 900, False), (1024, 768, False), (390, 844, False), (320, 568, False), (390, 844, True)):
            for name, steps, want in SC:
                s = await scenario(b, W, H, name, steps, big); s['want'] = want; out.append(s)
                ok = (s['success'] and s['success']['visible']) if want == 'success' else ((s['focus'] == want.lstrip('#') or (want == 'seva' and s['focus'].startswith('seva'))) and s['onScreen'])
                s['ok'] = bool(ok)
                print(f"{TAG:6s} {W}x{H}{' big' if big else ''} {name:22s} focus={s['focus']!s:12.12s} onScreen={s['onScreen']!s:5s} summary={s['summary']!s:5s} errors={s['errors']} name='{s['nameVal']}' inv={[x[1] for x in s['inv'] if x]} success={s['success']} {'OK' if ok else 'FAIL'} {s['errs'][:1]}", flush=True)
        await b.close()
    json.dump(out, open(f'work/fix/evidence/item3/tests_{TAG}.json', 'w'), ensure_ascii=False, indent=1)
asyncio.run(main())
