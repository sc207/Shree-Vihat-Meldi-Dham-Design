# Item 5 — Home banner buttons on very small phones (below 375 px).
# Before: the two phone banner buttons were forced to equal widths (flex: 1 1 0) with labels that never wrap; the button hides overflow,
# so at 320–340 px "મહોત્સવ વિશે જાણો →" (148 px) did not fit its 139–149 px button and its first letter was cut.
# Now, below 375 px only, each button takes its own label width plus padding and they share the leftover space (both still fit in one row
# at 320 px: 172 + 99 + 10 px gap); a button may never become narrower than its label, so on anything narrower the second one wraps
# to its own row instead of clipping. Same wording, font size, padding and height; 375 px and wider unchanged. site.css only.
import sys, os
root = sys.argv[1]
css = '''

/* ════════ Home banner buttons below 375 px: the label is never cut or cramped (item 5) ════════
   Equal-width buttons (flex: 1 1 0) left "મહોત્સવ વિશે જાણો →" 9–24 px wider than its button at 320–340 px, and the button hides overflow,
   so the first letter was cut (360–374 px: only 5–8 px from the edge). Below 375 px each button sizes to its label and they share
   the rest; never narrower than the label. */
@media (max-width: 374px) {
  .vm-root .vx-home-hero .vm-btn-row .vm-btn { flex: 1 1 auto; min-width: max-content; }
}
'''
p = os.path.join(root, 'site.css'); s = open(p, encoding='utf-8').read(); assert 'item 5' not in s
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + css.lstrip('\n'))
print('item 5 applied to site.css')
