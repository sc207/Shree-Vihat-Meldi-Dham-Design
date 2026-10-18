"""v178 (proposed): (1) festival night-programme day tiles on phones 401–760 px: 11 -> 12 px, short day names up to 560 px;
(2) New Temple card 04: keep "·" and the closing "॥" on the line of the word before them (no-break space).
usage: python3 tools/examples/apply_v178_nights_bhuvan.py <project dir>"""
import sys, os
P = sys.argv[1]
def edit(f, pairs):
    p = os.path.join(P, f); s = open(p, encoding='utf8').read()
    for old, new, n in pairs:
        assert s.count(old) == n, (f, old, s.count(old)); s = s.replace(old, new)
    open(p, 'w', encoding='utf8').write(s)
for f in ('NewTemple.dc.html', 'NewTempleMobile.dc.html'):
    edit(f, [('ભુવન ॥</h3>', 'ભુવન&nbsp;॥</h3>', 1), ('ભુવન ॥</b>', 'ભુવન&nbsp;॥</b>', 1), ('ધામનું ભવન · નિર્માણ પૂર્ણ', 'ધામનું ભવન&nbsp;· નિર્માણ પૂર્ણ', 1)])
css = os.path.join(P, 'site.css'); s = open(css, encoding='utf8').read()
assert 'v178' not in s
s = s.rstrip('\n') + '''

/* v178 — festival night programme, ડાયરો day tiles on phones (401–760 px): the full day names were 11 px and filled the tile.
   12 px everywhere; short names (મંગળ, બુધ …) up to 560 px, as already below 400 px. Wider screens unchanged. */
@media (max-width: 760px) {
  .vx-nfeat__days li { font-size: 12px; }
}
@media (min-width: 401px) and (max-width: 560px) {
  .vx-nfeat__days .vx-dl { display: none; }
  .vx-nfeat__days .vx-ds { display: inline; }
}
'''
open(css, 'w', encoding='utf8').write(s)
print('applied')
