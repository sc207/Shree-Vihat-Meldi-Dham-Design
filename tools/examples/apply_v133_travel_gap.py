"""v133: Darshan page — space between the four travel cards (રેલવે, બસ, માર્ગ, હવાઈ માર્ગ) and the map card below them.
The map wrapper `.vx-dmap` had no spacing rule, so the map touched the cards (desktop and phone). site.css block only (+ board frame heights
if frame_heights.py asks). usage: python3 tools/examples/apply_v133_travel_gap.py <project folder>"""
import os, sys
BLOCK = '''
/* v133 — Darshan "ધામ સુધી કેવી રીતે પહોંચશો": gap between the travel cards and the map (the map touched the cards). */
.vm-root .vx-dmap { margin-top: var(--space-lg); }
'''
p = os.path.join(sys.argv[1], 'site.css'); s = open(p, encoding='utf-8').read()
assert '/* v133 — Darshan' not in s and s.count('.vx-trv { display: grid;') == 1
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + BLOCK); print('appended v133 block')

# frames (frame_heights.py: natural +24 px) — root style height, data-props height, canvas.json "h"
import json, re
FR = {'Darshan': (5030, 5054), 'DarshanMobile': (7090, 7114)}
for page, (old, new) in FR.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    for a, b in (('height: %dpx;' % old, 'height: %dpx;' % new), ('"height": %d' % old, '"height": %d' % new)):
        assert s.count(a) == 1, (page, a, s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
p = os.path.join(sys.argv[1], 'canvas.json'); s = open(p, encoding='utf-8').read()
for page, (old, new) in FR.items():
    a = '"%s.dc.html": {\n      "h": %d,' % (page, old)
    assert s.count(a) == 1, (page, s.count(a)); s = s.replace(a, '"%s.dc.html": {\n      "h": %d,' % (page, new))
json.loads(s); open(p, 'w', encoding='utf-8').write(s); print('frames updated', FR)
