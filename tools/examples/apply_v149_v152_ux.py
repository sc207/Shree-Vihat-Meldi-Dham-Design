"""UI / UX / responsive fixes from the check of v147 (16 Oct 2026, owner: "check now if any bug related to design, ux ui and responsiveness
issue then fix it for all device like laptop, tablet, mobile"). One part = one published version: v149–v152 (v148 in the artifact
history is a Design-type re-save with no content change; part 1 was published with its comment still saying "v148", corrected in part 2). CSS only, appended to site.css as one
commented block per part; no wording, no other file.
usage: python3 tools/examples/apply_v149_v152_ux.py <project folder> <part 1..4>
  1 Home "ફોટો ગેલેરી" strip: names on the photos readable (white text sat on a pale grey band, 1.9–2.8 : 1)
  2 Home banner date box at 320 px: "૮ ફેબ્રુ., સોમવાર" ran over the right border
  3 New Temple "દર્શનનો માર્ગ" cards on small phones: text column 96 px wide at 320 px (6+ lines of 1–2 words)
  4 New Temple "નિર્માણ સ્થળની તાજી તસવીરો" on tablets (761–999 px): text beside each thumbnail squeezed to ~75 px"""
import os, sys
proj, part = sys.argv[1], int(sys.argv[2])
css_path = os.path.join(proj, 'site.css')


def append_css(block):
    s = open(css_path, encoding='utf-8').read()
    marker = block.strip().splitlines()[0]
    assert marker not in s, 'part already applied'
    open(css_path, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n\n' + block.strip('\n') + '\n')


BLOCKS = {
1: '''
/* v148 — Home "ફોટો ગેલેરી" strip: the names on the photos are readable on every board.
   Was: white 16 px text on a light gradient (0 → 72 % maroon over 32 px) — on the cream backgrounds and the white clothes of the Bapa photos
   the band looked grey and the text measured 1.9–2.8 : 1. Now a deeper band (same height on one-line names) and a soft text shadow. */
.vm-root .vx-strip figcaption { padding-top: 36px;
  background: linear-gradient(180deg, rgba(28,10,16,0) 0%, rgba(28,10,16,.74) 48%, rgba(28,10,16,.88) 100%);
  text-shadow: 0 1px 3px rgba(20,6,10,.6); }
''',
2: '''
/* v150 — Home banner date box on 320 px phones: "૮ ફેબ્રુ., સોમવાર" ran 2 px over the right border (the first column took its full
   one-line width). Below 340 px: slightly smaller dates and side padding; 340 px and wider unchanged. */
@media (max-width: 339px) {
  .vm-root .vx-home-hero .vm-datestrip > div { padding-left: 10px; padding-right: 10px; }
  .vm-root .vx-home-hero .vm-datestrip b { font-size: 16px; }
}
''',
3: '''
/* v151 — New Temple "દર્શનનો માર્ગ" cards on small phones: picture 120 → 88 px, card padding and gap 16 px, so the text beside it gets
   152 px instead of 96 px at 320 px (it broke into 6+ short lines, "·" and "×" starting lines). 401 px and wider unchanged. */
@media (max-width: 400px) {
  .vm-root .vx-area { grid-template-columns: 88px minmax(0, 1fr); gap: 16px; padding: 16px; }
}
''',
4: '''
/* v152 — New Temple "નિર્માણ સ્થળની તાજી તસવીરો" on tablets (761–999 px): the three small update cards used the laptop thumbnail
   (148 px), leaving ~75 px for the date and text. Same compact card as on phones (104 px thumbnail). Phones and laptops unchanged. */
@media (min-width: 761px) and (max-width: 999px) {
  .vm-root .vx-prog__list li { grid-template-columns: 104px minmax(0, 1fr); gap: 12px; padding: 10px; }
  .vm-root .vx-prog__list .vx-slot { min-height: 80px; }
}
''',
}
if part == 2:   # part 1 went live as v149 (v148 was a re-save) with its comment saying "v148": correct the label
    t = open(css_path, encoding='utf-8').read(); a = '/* v148 — Home "ફોટો ગેલેરી" strip'
    assert t.count(a) == 1; open(css_path, 'w', encoding='utf-8').write(t.replace(a, '/* v149 — Home "ફોટો ગેલેરી" strip'))
append_css(BLOCKS[part])
# frames (tools/frame_heights.py): part 3 makes the phone New Temple page shorter; canvas "h" stays 8000 (cap)
FR = {3: {'NewTempleMobile': (11812, 11659)}}
for page, (old, new) in FR.get(part, {}).items():
    p = os.path.join(proj, page + '.dc.html'); s = open(p, encoding='utf-8').read()
    for a, b in (('height: %dpx;' % old, 'height: %dpx;' % new), ('"height": %d' % old, '"height": %d' % new)):
        assert s.count(a) == 1, (page, a, s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
    print('frame', page, old, '->', new)
print('part', part, 'applied')
