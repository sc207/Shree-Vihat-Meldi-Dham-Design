"""v126: the gallery viewer (lightbox, Gallery + GalleryMobile) opens where the visitor is and fits the screen.
Before: `position: absolute` at the top of the page (a photo opened from lower down appeared off-screen: only the dark scrim was visible),
a fixed 680 px image area (caption and ✕ below the edge of a 900 px laptop screen), and no phone layout (photo 214 px wide above ~450 px of
empty panel on a 390 px phone). After: fixed to the screen and centred (like the phone menu, `.vm-mnav`), image area at most the screen
height minus the panel, phone: 16 px margins and the photo across the full panel width; phones turned sideways: compact.
site.css only (one block appended at the end). usage: python3 tools/examples/apply_v126_gallery_viewer.py <project folder>"""
import os, sys
BLOCK = '''
/* v126 — gallery viewer (lightbox): open where the visitor is (fixed to the screen, centred, like the phone menu), fit the screen height,
   phone layout with the photo across the full panel. Was: absolute at the top of the page, fixed 680 px image area, no phone rules. */
.vm-root .vx-lb { position: fixed; z-index: 95; align-items: center; overflow-y: auto; overscroll-behavior: contain; padding: 32px var(--space-2xl); }
.vm-root .vx-lb__img { height: min(680px, calc(100vh - 176px)); height: min(680px, calc(100dvh - 176px)); }
@media (max-width: 760px) {
  .vm-root .vx-lb { padding: 16px; }
  .vm-root .vx-lb__box { padding: 12px; gap: 12px; }
  .vm-root .vx-lb__img { height: auto; }
  .vm-root .vx-lb__img img { width: 100%; height: auto; max-height: calc(100vh - 150px); max-height: calc(100dvh - 150px); }
  .vm-root .vx-lb__bar b { font-size: 19px; }
}
@media (orientation: landscape) and (max-height: 500px) {
  .vm-root .vx-lb { padding: 12px var(--space-lg); }
  .vm-root .vx-lb__box { padding: 12px; gap: 8px; }
  .vm-root .vx-lb__img { height: calc(100vh - 104px); height: calc(100dvh - 104px); }
}
'''
p = os.path.join(sys.argv[1], 'site.css'); s = open(p, encoding='utf-8').read()
assert '/* v126 — gallery viewer' not in s, 'already applied'
assert s.count('.vx-lb { position: absolute; inset: 0; z-index: 30;') == 1, 'unexpected base rule'
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + BLOCK)
print('appended v126 block to', p)
