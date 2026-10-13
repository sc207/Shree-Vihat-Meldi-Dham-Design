# Glow fix on a copy of v106: (1) halo keyframes no longer replace the halo's centring transform; (2) on banners with a picture,
# the gold light and the halo are drawn in the picture's own box. Exact-string edits, each asserted once.
import sys
p = sys.argv[1] if len(sys.argv) > 1 else 'work/glow/project/site.css'
s = open(p, encoding='utf-8').read()
old = '@keyframes vx-halo { from { opacity: .72; transform: scale(.96); } to { opacity: 1; transform: scale(1.04); } }'
new = ('/* breathing uses the separate `scale` property, so it no longer replaces the halo\'s own centring transform (glow fix) */\n'
       '@keyframes vx-halo { from { opacity: .72; scale: .96; } to { opacity: 1; scale: 1.04; } }')
assert s.count(old) == 1; s = s.replace(old, new)
block = '''

/* ════════ Banner light stays behind the picture at every screen size (glow fix) ════════
   Before: the banner's gold light was painted at a fixed spot of the whole banner (72 % across, 42 % down). That spot is behind the
   picture only while the picture sits on the right (desktop). When the picture moves below the text (tablet portrait, phones, phone
   landscape) the light stayed beside the title. The breathing halo inside the picture box was also pushed to the right while it
   animated (fixed in @keyframes vx-halo above).
   Now, on banners with a picture (Home, New Temple, Festival, Gallery) the light and the halo are drawn in the picture's own box,
   so they move and scale with the picture. Same colour, strength and desktop size; banners without a picture are unchanged. */
.vm-root .vm-hero:has(> .vm-hero__grid > .vm-hero__art img) {
  background: radial-gradient(ellipse 120% 90% at 50% 110%, #5a1428 0%, rgba(90,20,40,0) 60%), linear-gradient(180deg, #2a0913 0%, var(--burgundy) 55%, #3b0c1b 100%);
}
.vm-root .vm-hero__art:has(img)::before {
  content: ""; position: absolute; z-index: -1; left: 50%; top: 31%;
  height: 140%; aspect-ratio: 1.8; max-width: 165%;
  translate: -50% -50%; border-radius: 50%; pointer-events: none;
  background: radial-gradient(closest-side, rgba(226,194,122,.34), rgba(226,194,122,0));
}
.vm-root .vm-hero__halo { top: 50%; transform: none; translate: -50% -50%; pointer-events: none; }
'''
s = s.rstrip('\n') + block
open(p, 'w', encoding='utf-8').write(s)
print('applied to', p)
