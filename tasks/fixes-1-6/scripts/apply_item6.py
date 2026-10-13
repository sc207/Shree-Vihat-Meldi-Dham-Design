# Item 6 — polish, in five separately revertible parts. Usage: apply_item6.py <project> <part 1..5>
import sys, os, glob
root, part = sys.argv[1], int(sys.argv[2])
def add_css(block, marker):
    p = os.path.join(root, 'site.css'); s = open(p, encoding='utf-8').read(); assert marker not in s, marker
    open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n\n' + block.strip('\n') + '\n')
if part == 1:
    add_css('''
/* ════════ Seva day tiles, 1000–1179 px: the 7 festival days stay on one row (item 6.1) ════════
   Beside the help column the form is 491–557 px wide; seven 76 px tiles + gaps need 580 px, so "૮ સોમવાર" (or two days) wrapped alone.
   Here the tiles share the row equally (≥ 65 px each; their text needs ≤ 48 px). Other widths unchanged. */
@media (min-width: 1000px) and (max-width: 1179px) {
  .vm-root .vx-days { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 6px; }
  .vm-root .vx-day { min-width: 0; padding: 8px 2px; }
}''', 'item 6.1')
elif part == 2:
    add_css('''
/* ════════ Festival night cards on small phones: artist names stay whole (item 6.2) ════════
   The phone card puts the date in a 92 px column beside the names; below 360 px (below 390 px with large text) that left about 70–110 px
   for a name, so "ગોપાલ / સાધુ" broke word by word. There the date sits above the names, as on desktop. */
@media (max-width: 359px) {
  .vm-root .vx-night { grid-template-columns: minmax(0, 1fr); gap: 12px; }
  .vm-root .vx-night__d { flex-direction: row; align-items: center; gap: 10px; }
  .vm-root .vx-night__who, .vm-root .vx-night__tba { padding: 12px 0 0; border-left: 0; border-top: 1px solid rgba(226,194,122,.22); }
}
@media (max-width: 389px) {
  .vm-root.is-big .vx-night { grid-template-columns: minmax(0, 1fr); gap: 12px; }
  .vm-root.is-big .vx-night__d { flex-direction: row; align-items: center; gap: 10px; }
  .vm-root.is-big .vx-night__who, .vm-root.is-big .vx-night__tba { padding: 12px 0 0; border-left: 0; border-top: 1px solid rgba(226,194,122,.22); }
}''', 'item 6.2')
elif part == 3:
    add_css('''
/* ════════ Jump links land with breathing room (item 6.3) ════════
   "પંચાંગ", "યાત્રા માર્ગદર્શન" (Darshan) and "નિર્માણ પ્રગતિ" (New Temple) are targets without top padding, so their heading landed at the
   very top edge; every other jump link lands its heading 96 px (desktop) / 64 px (phone) down, the section padding. Same offset here. */
.vm-root #calendar, .vm-root #travel, .vm-root #progress { scroll-margin-top: 96px; }
@media (max-width: 760px) { .vm-root #calendar, .vm-root #travel, .vm-root #progress { scroll-margin-top: 64px; } }''', 'item 6.3')
elif part == 4:
    n = 0
    for f in sorted(glob.glob(os.path.join(root, '*.dc.html'))):
        s = open(f, encoding='utf-8').read(); o = s
        for t in ('પૃષ્ઠો', 'મહોત્સવ', 'સંપર્ક'):
            a = f'<h4>{t}</h4>'
            if a in s: assert s.count(a) == 1, (f, t); s = s.replace(a, f'<h2>{t}</h2>')
        for a, b in (('<h3>નોંધણી પછી શું?</h3>', '<h2>નોંધણી પછી શું?</h2>'), ('<h3 style="font-size: 24px;">યજ્ઞ નોંધણી</h3>', '<h2 style="font-size: 24px;">યજ્ઞ નોંધણી</h2>')):
            if a in s: assert s.count(a) == 1, (f, a); s = s.replace(a, b)
        assert '<h4>' not in s, f
        if s != o: open(f, 'w', encoding='utf-8').write(s); n += 1
    print('heading tags changed in', n, 'files')
    add_css('''
/* ════════ Heading levels without a skip (item 6.4) ════════
   Footer column titles were h4 right after the page's h2 sections, and the Seva side cards were h3 right after the page h1, so the page
   outline skipped a level for screen-reader users. They are now h2; these rules give them exactly the look they had as h4 / h3. */
.vm-footer h2 { margin: 0 0 var(--space-md); font-family: var(--font-body); font-size: 14px; font-weight: 600; line-height: 1.75; letter-spacing: normal; color: var(--gold-soft); }
.vm-root .vm-footer h2 { font-size: 16px; }
.vx-steps h2 { margin: 0; font-family: var(--font-display); font-size: 22px; font-weight: 600; line-height: 1.6; color: var(--heading); }
.vx-yagna h2 { margin: 0; font-family: var(--font-display); font-size: 28px; font-weight: 600; line-height: 1.3; color: var(--heading); }''', 'item 6.4')
elif part == 5:
    add_css('''
/* ════════ Seva consent checkbox 24 px (item 6.5) ════════
   22 × 22 px was below the 24 × 24 px minimum target size (WCAG 2.2); its label was already clickable. Same alignment with the text. */
.vm-root .vm-check input { width: 24px; height: 24px; margin-top: 1px; }''', 'item 6.5')
print('item 6 part', part, 'applied')
