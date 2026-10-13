# Item 4 — phone menu page (MenuMobile): visible ✕ and sensible closing.
# Before: ✕ was maroon on maroon (1.41:1) because the general link colour (.vm-root a) outranked the design system's ivory for .vm-mnav__close;
# ✕ always went to the Home page and "મુખ્ય પૃષ્ઠ" was always marked current, whichever page the visitor came from.
# Now: ✕ ivory (14:1); ✕ and Escape return to the page the visitor came from (browser back: same page, same scroll position) when they
# came from a page of this site, otherwise ✕ still goes Home (its link is kept as the fallback); the current-page mark follows the page
# they came from (Home when the menu is opened directly, as before). Links to other pages are unchanged. No wording change.
import sys, os
root = sys.argv[1]
p = os.path.join(root, 'MenuMobile.dc.html'); s = open(p, encoding='utf-8').read()
PAGES = ['HomeMobile', 'DarshanMobile', 'NewTempleMobile', 'PranPratishthaMobile', 'SevaMobile', 'GalleryMobile', 'HistoryMobile', 'ContactMobile']
R = [('role="dialog" aria-label="મેનુ">', 'role="dialog" aria-label="મેનુ" onKeyDown="{{menuKey}}">'),
     ('<a class="vm-mnav__close" href="HomeMobile.dc.html" aria-label="મેનુ બંધ કરો">', '<a class="vm-mnav__close" href="HomeMobile.dc.html" aria-label="મેનુ બંધ કરો" onClick="{{closeClick}}">'),
     ('<li><a href="HomeMobile.dc.html" aria-current="page">', '<li><a href="HomeMobile.dc.html" aria-current="{{ac0}}">')]
for i, pg in enumerate(PAGES[1:], 1): R.append((f'<li><a href="{pg}.dc.html">', f'<li><a href="{pg}.dc.html" aria-current="{{{{ac{i}}}}}">'))
R.append(('_rv() {\nreturn {};\n}', '''_rv() {
let from = null;
try { const r = document.referrer ? new URL(document.referrer) : null; if (r && r.origin === window.location.origin) from = r.pathname.split('/').pop(); } catch (e) {}
const pages = ['HomeMobile.dc.html', 'DarshanMobile.dc.html', 'NewTempleMobile.dc.html', 'PranPratishthaMobile.dc.html', 'SevaMobile.dc.html', 'GalleryMobile.dc.html', 'HistoryMobile.dc.html', 'ContactMobile.dc.html'];
const cur = from === null ? 0 : pages.indexOf(from === 'HomeMobile2.dc.html' ? 'HomeMobile.dc.html' : from);
const canBack = !!from && from !== 'MenuMobile.dc.html' && window.history.length > 1;
const out = {
closeClick: (e) => { if (canBack) { e.preventDefault(); window.history.back(); } },
menuKey: (e) => { if (e.key !== 'Escape') return; e.preventDefault(); if (canBack) window.history.back(); else window.location.href = 'HomeMobile.dc.html'; }
};
pages.forEach((pg, i) => { out['ac' + i] = i === cur ? 'page' : 'false'; });
return out;
}'''))
for old, new in R:
    assert s.count(old) == 1, old[:60]; s = s.replace(old, new)
open(p, 'w', encoding='utf-8').write(s)
css = '''

/* ════════ Phone menu: the ✕ is ivory again (item 4) ════════
   On the phone menu page ✕ is a link, so the general link colour (.vm-root a, maroon) outranked the design system's ivory → maroon on
   maroon, 1.41:1. Ivory gives 14:1. Closing behaviour: see MenuMobile logic. */
.vm-root .vm-mnav__close { color: var(--ivory); }
'''
p = os.path.join(root, 'site.css'); t = open(p, encoding='utf-8').read(); assert '.vm-root .vm-mnav__close {' not in t
open(p, 'w', encoding='utf-8').write(t.rstrip('\n') + '\n' + css.lstrip('\n'))
# The browser's own scroll restoration after "back" is unreliable here (it races with the page drawing itself), so the 9 phone pages
# that open the menu remember their scroll position when ☰ is tapped and put it back when the visitor returns with "back" (10-minute limit).
PHONE = ['HomeMobile', 'ContactMobile', 'DarshanMobile', 'GalleryMobile', 'HistoryMobile', 'NewTempleMobile', 'NotFoundMobile', 'PranPratishthaMobile', 'SevaMobile']
LINK_OLD = '<a class="vm-menu-btn" href="MenuMobile.dc.html" aria-label="મેનુ ખોલો">'
LINK_NEW = '<a class="vm-menu-btn" href="MenuMobile.dc.html" aria-label="મેનુ ખોલો" onClick="{{menuGo}}">'
RV_OLD = "renderVals() { const base = this._rv() || {}; const big = this.fsBig(); return Object.assign({}, base, { "
RV_NEW = ("menuBack() { if (this._menuBackDone) return; this._menuBackDone = true; try { const v = JSON.parse(window.sessionStorage.getItem('vx-menu-y') || 'null'); const nav = window.performance.getEntriesByType('navigation')[0]; "
          "if (v && v.p === window.location.pathname && nav && nav.type === 'back_forward' && Date.now() - v.t < 600000) { window.sessionStorage.removeItem('vx-menu-y'); const go = () => { if (Math.abs(window.scrollY - v.y) > 2) window.scrollTo({ top: v.y, behavior: 'instant' }); }; setTimeout(go, 60); setTimeout(go, 400); } } catch (e) {} }\n"
          "renderVals() { this.menuBack(); const base = this._rv() || {}; const big = this.fsBig(); return Object.assign({}, base, { menuGo: () => { try { window.sessionStorage.setItem('vx-menu-y', JSON.stringify({ p: window.location.pathname, y: Math.round(window.scrollY), t: Date.now() })); } catch (e) {} }, ")
for b in PHONE:
    q = os.path.join(root, b + '.dc.html'); t = open(q, encoding='utf-8').read()
    for old, new in ((LINK_OLD, LINK_NEW), (RV_OLD, RV_NEW)):
        assert t.count(old) == 1, (b, old[:40]); t = t.replace(old, new)
    open(q, 'w', encoding='utf-8').write(t)
print('item 4 applied to MenuMobile + 9 phone pages + site.css')
