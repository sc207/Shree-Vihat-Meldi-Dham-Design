"""v138: owner 16 Oct 2026 — New Temple "દર્શનનો માર્ગ": "is that any way that we can showcase the proper image even if it will be visualise".
The three empty [ફોટો] boxes (૦૧ ગર્ભગૃહ, ૦૨ મંડપ, ૦૩ પ્રવેશદ્વાર) now show close-ups cut from the architectural render (14), each marked
"સ્થાપત્ય ચિત્ર" so no visitor takes it for a photograph: 35 doorway with માતાજી, 36 pillared hall, 37 entrance steps and porch.
Box ૦૪ ([અન્ય વિભાગ]) stays a placeholder — the render does not show it. NewTemple + NewTempleMobile + one site.css block.
usage: python3 tools/examples/apply_v138_route_images.py <project folder>"""
import os, sys
SLOT = ('<div class="vx-area__img"><div class="vx-slot"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 8h3l1.5-2.5h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z">'
        '</path><circle cx="12" cy="13" r="3.5"></circle></svg><span>[ફોટો]</span></div></div>')
IMG = ('<div class="vx-area__img vx-area__img--render"><img src="/_blob/%s" alt="%s — સ્થાપત્ય ચિત્ર" loading="lazy">'
       '<span class="vx-area__tag" aria-hidden="true">સ્થાપત્ય ચિત્ર</span></div>')
NEW = [IMG % ('c8cf833cc152ab8b5dc0b97f8865e332', 'ગર્ભગૃહ'), IMG % ('a6e4902a5aa10b4aa465188e5b48cdcd', 'મંડપ'), IMG % ('57821e4c0639457c075c918ecee6d7f4', 'પ્રવેશદ્વાર')]
for page in ('NewTemple', 'NewTempleMobile'):
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    sec = s.index('aria-labelledby="exp-t"'); end = s.index('</section>', sec)
    part = s[sec:end]; assert part.count(SLOT) == 4 and s.count(SLOT) == 4, (page, part.count(SLOT))
    for n in NEW: part = part.replace(SLOT, n, 1)        # first three cards, in order ૦૧ ૦૨ ૦૩
    assert part.count(SLOT) == 1
    s = s[:sec] + part + s[end:]; open(p, 'w', encoding='utf-8').write(s); print('updated', page)
BLOCK = '''
/* v138 — New Temple "દર્શનનો માર્ગ": close-ups from the architectural render fill the area boxes, marked "સ્થાપત્ય ચિત્ર". */
.vm-root .vx-area__img--render { position: relative; }
.vm-root .vx-area__img--render img { width: 100%; height: 100%; object-fit: cover; }
.vm-root .vx-area__tag { position: absolute; left: 8px; bottom: 8px; padding: 1px 8px; border-radius: var(--radius-pill); background: rgba(28,10,16,.74);
  color: var(--ivory); font-size: 13px; font-weight: 600; line-height: 1.7; white-space: nowrap; }
@media (max-width: 999px) { .vm-root .vx-area__tag { left: 5px; bottom: 5px; padding: 0 6px; line-height: 1.6; } }
'''
p = os.path.join(sys.argv[1], 'site.css'); s = open(p, encoding='utf-8').read()
assert '/* v138 — New Temple' not in s
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + BLOCK); print('appended v138 block')
