# Item 2 — tablet & small-laptop menu (761–1179 px). The ☰ button on the 12 desktop/tablet boards had no action and no panel.
# It now opens the design system's own menu panel (.vm-mnav, fixed full-screen, already used by the phone menu page) with the
# same 8 links as the board's header nav (current page marked), the same brand, text-size button and footer as the phone menu.
# Panel: role=dialog + aria-modal, ✕ is a real button, Escape closes, Tab stays inside, focus goes to ✕ on open and back to ☰ on close.
# Hidden at ≥1180 px (the header links show there). Exact-string edits, each asserted.
import re, sys, os
root = sys.argv[1]
BOARDS = ['Main', 'HomeTablet', 'HomeTabletL', 'HomePhoneL', 'NewTemple', 'PranPratishtha', 'Seva', 'Gallery', 'History', 'Contact', 'Darshan', 'NotFound']
menu = open(os.path.join(root, 'MenuMobile.dc.html'), encoding='utf-8').read()
top = re.search(r'<div class="vm-mnav__top">(.*?)<a class="vm-mnav__close"', menu, re.S).group(1)
brand = re.search(r'(<a class="vm-brand" href=")HomeMobile\.dc\.html(".*?</a>)', top, re.S)
fsbtn = re.search(r'(<button class="vm-lang vx-fs vx-fs--dark".*?</button>)', top, re.S).group(1)
xsvg = re.search(r'<a class="vm-mnav__close"[^>]*>(<svg.*?</svg>)</a>', menu, re.S).group(1)
foot = re.search(r'(<div class="vm-mnav__foot">.*?</div></div>)</div>\n</div>\n</x-dc>', menu, re.S).group(1)
assert brand and fsbtn and xsvg and foot
BTN_OLD = '<button class="vm-menu-btn" type="button" aria-label="મેનુ ખોલો" aria-expanded="false">'
BTN_NEW = '<button class="vm-menu-btn" type="button" aria-label="મેનુ ખોલો" aria-controls="vx-tnav" aria-expanded="{{navExp}}" onClick="{{navOpenClick}}">'
RV_OLD = "renderVals() { const base = this._rv() || {}; const big = this.fsBig(); return Object.assign({}, base, { "
RV_NEW = ("navOpen(e) { this._navBtn = e && e.currentTarget; this.setState({ navOpen: true }); const b = this._navBtn; setTimeout(() => { const r = b && b.closest('.vm-root'); const c = r && r.querySelector('#vx-tnav .vm-mnav__close'); if (c) c.focus(); }, 30); }\n"
          "navClose() { this.setState({ navOpen: false }); const b = this._navBtn; setTimeout(() => { if (b && b.isConnected) b.focus(); }, 30); }\n"
          "navKey(e) { if (e.key === 'Escape') { e.preventDefault(); this.navClose(); return; } if (e.key !== 'Tab') return; const f = [...e.currentTarget.querySelectorAll('a[href], button:not([disabled])')].filter(x => x.getClientRects().length); if (!f.length) return; const a = f[0], z = f[f.length - 1]; if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }\n"
          "renderVals() { const base = this._rv() || {}; const big = this.fsBig(); const nav = !!(this.state && this.state.navOpen); return Object.assign({}, base, { navExp: nav ? 'true' : 'false', navHidden: !nav, navOpenClick: (e) => this.navOpen(e), navCloseClick: () => this.navClose(), navKey: (e) => this.navKey(e), ")
END = '</div>\n</x-dc>'
for b in BOARDS:
    p = os.path.join(root, b + '.dc.html'); s = open(p, encoding='utf-8').read()
    nav = re.search(r'<nav class="vm-nav" aria-label="મુખ્ય મેનુ"><ul>(.*?)</ul></nav>', s).group(1)
    items = re.findall(r'<li><a href="[^"]+"(?: aria-current="page")?>[^<]+</a></li>', nav); assert len(items) == 8, b
    panel = ('<div class="vm-mnav vx-tnav" id="vx-tnav" role="dialog" aria-modal="true" aria-label="મેનુ" hidden="{{navHidden}}" onKeyDown="{{navKey}}">'
             '<div class="vm-mnav__top">' + brand.group(1) + 'Main.dc.html' + brand.group(2) + fsbtn +
             '<button class="vm-mnav__close" type="button" aria-label="મેનુ બંધ કરો" onClick="{{navCloseClick}}">' + xsvg + '</button></div>'
             '<ol>' + ''.join(items) + '</ol>' + foot + '</div>')
    for old, new in ((BTN_OLD, BTN_NEW), (RV_OLD, RV_NEW)):
        assert s.count(old) == 1, (b, old[:40]); s = s.replace(old, new)
    assert s.count(END) == 1, b; s = s.replace(END, panel + END)
    open(p, 'w', encoding='utf-8').write(s)
css = '''

/* ════════ Tablet & small-laptop menu, 761–1179 px (item 2) ════════
   Below 1180 px the header shows ☰ instead of the page links. On the desktop/tablet boards ☰ had no action, so there was no way to the other
   pages from the header. ☰ now opens the design system's menu panel (.vm-mnav, as on the phone menu page) with the same 8 links.
   Above the phone bottom bar; content in one centred column on wide screens; hidden from 1180 px, where the header links show. */
.vm-root .vx-tnav { z-index: 90; overscroll-behavior: contain; }
.vm-root .vx-tnav > * { width: 100%; max-width: 720px; margin-inline: auto; }
@media (min-width: 1180px) { .vm-root .vx-tnav { display: none; } }
'''
p = os.path.join(root, 'site.css'); s = open(p, encoding='utf-8').read(); assert 'vx-tnav' not in s
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + css.lstrip('\n'))
print('item 2 applied to', len(BOARDS), 'boards + site.css')
