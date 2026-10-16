"""v131: gallery viewer (lightbox) behaviour, completing v126 — Gallery + GalleryMobile logic and the dialog element only.
- Escape closes it; a tap or click on the dark area around the panel closes it.
- When it opens, keyboard focus moves to ✕ (Tab stays inside the dialog); when it closes, focus returns to the photo that opened it.
Same pattern as the tablet menu (`navOpen` / `navClose` / `navKey`). No visual change.
usage: python3 tools/examples/apply_v131_viewer_keys.py <project folder>"""
import os, sys
METHODS = ("lbOpen(e, it) { this._lbBtn = e && e.currentTarget; this.setState({ lb: it }); const b = this._lbBtn; "
           "setTimeout(() => { const r = b && b.closest('.vm-root'); const c = r && r.querySelector('.vx-lb__close'); if (c) c.focus({ preventScroll: true }); }, 30); }\n"
           "lbClose() { this.setState({ lb: null }); const b = this._lbBtn; setTimeout(() => { if (b && b.isConnected) b.focus({ preventScroll: true }); }, 30); }\n"
           "lbKey(e) { if (e.key === 'Escape') { e.preventDefault(); this.lbClose(); return; } "
           "if (e.key === 'Tab') { e.preventDefault(); const c = e.currentTarget.querySelector('.vx-lb__close'); if (c) c.focus(); } }\n")
R = [
    ("constructor(props) { super(props); this.state = { cat: 'બધું', lb: null }; }",
     METHODS + "constructor(props) { super(props); this.state = { cat: 'બધું', lb: null }; }"),
    ("open: () => this.setState({ lb: it })", "open: (e) => this.lbOpen(e, it)"),
    ("lbClose: () => this.setState({ lb: null })",
     "lbClose: () => this.lbClose(), lbKey: (e) => this.lbKey(e), lbScrim: (e) => { if (e.target === e.currentTarget) this.lbClose(); }"),
    ('<div class="vx-lb" role="dialog" aria-modal="true" aria-label="{{lbCap}}">',
     '<div class="vx-lb" role="dialog" aria-modal="true" aria-label="{{lbCap}}" onKeyDown="{{lbKey}}" onClick="{{lbScrim}}">'),
]
for page in ('Gallery', 'GalleryMobile'):
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert 'lbOpen(e, it)' not in s, 'already applied'
    for a, b in R:
        assert s.count(a) == 1, (page, a[:50], s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s); print('updated', page)
