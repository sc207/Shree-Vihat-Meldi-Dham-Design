# Probe: Seva form — what happens on submit when empty, and when the required fields are filled.
import asyncio, sys
sys.path.insert(0, 'tools')
from playwright.async_api import async_playwright
from _common import clock_script, launch
async def main():
    async with async_playwright() as p:
        b = await launch(p)
        for board, W in (('Seva', 1440), ('SevaMobile', 390)):
            ctx = await b.new_context(viewport={'width': W, 'height': 900}); await ctx.add_init_script(clock_script('2026-10-10T12:30:00+05:30'))
            pg = await ctx.new_page(); await pg.goto(f'http://127.0.0.1:8771/{board}.dc.html'); await pg.wait_for_timeout(1200)
            info = await pg.evaluate('''() => { const f = document.querySelector('form'); if (!f) return 'no form';
               return {action: f.getAttribute('action'), novalidate: f.noValidate, required: [...f.querySelectorAll('[required]')].map(e => e.name || e.id || e.type), submit: [...f.querySelectorAll('button[type=submit],input[type=submit],button:not([type])')].map(b => b.textContent.trim().slice(0, 20)),
                       onsubmit: !!f.onsubmit, errs: document.querySelectorAll('[role=alert],[aria-live]').length}; }''')
            print(board, 'form:', info)
            body0 = await pg.evaluate('document.body.innerText.length')
            sub = pg.locator('a, button', has_text='નોંધણી પૂર્ણ કરો').last
            print('  submit element:', await sub.evaluate("e => e.outerHTML.slice(0, 220) + ' | in form: ' + !!e.closest('form')"))
            await sub.scroll_into_view_if_needed(); await sub.click(); await pg.wait_for_timeout(600)
            st = await pg.evaluate('''() => ({url: location.pathname, invalid: [...document.querySelectorAll(':invalid')].filter(e => e.tagName !== 'FORM').map(e => e.name || e.id).slice(0, 6), focused: document.activeElement && (document.activeElement.name || document.activeElement.id || document.activeElement.tagName), msg: (document.activeElement && document.activeElement.validationMessage) || '', alerts: [...document.querySelectorAll('[role=alert],[aria-live]')].map(e => e.innerText.trim().slice(0, 60))})''')
            print('  empty submit ->', st, 'text length', body0, '->', await pg.evaluate('document.body.innerText.length'))
            await ctx.close()
        await b.close()
asyncio.run(main())
