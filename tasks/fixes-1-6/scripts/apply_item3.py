# Item 3 — Seva form: after a failed submit the visitor is taken to the first field with a problem.
# Before: errors were shown under each field and in a summary at the top of the form, but the page did not move and focus stayed on
# the button, so on a long form (phone: ~3,000 px) only the last message near the button was visible. Fields were not marked invalid
# for assistive technology and not linked to their message.
# Now: submit (unchanged rules) → on failure, the first invalid control (name, mobile, town, seva choice, time slot, consent — in form
# order) is scrolled to the middle of the screen and focused; name/mobile/town/consent get aria-invalid + aria-describedby → their
# message. Typed values are kept (state unchanged). After a successful registration the page moves to the confirmation (which replaces the
# form) and focuses its heading. No wording change. Seva + SevaMobile (identical form and logic) + 2 CSS rules.
import sys, os
root = sys.argv[1]
R = [
 ('<input class="vm-input" id="f-name" autocomplete="name" required="" placeholder="દા.ત. રમેશભાઈ પટેલ" onChange="{{setName}}">',
  '<input class="vm-input" id="f-name" autocomplete="name" required="" placeholder="દા.ત. રમેશભાઈ પટેલ" onChange="{{setName}}" aria-invalid="{{invName}}" aria-describedby="f-name-err">'),
 ('<sc-if value="{{errName}}" hint-placeholder-val="{{false}}"><span class="vm-field__error">',
  '<sc-if value="{{errName}}" hint-placeholder-val="{{false}}"><span class="vm-field__error" id="f-name-err">'),
 ('<input class="vm-input" id="f-mob" type="tel" inputmode="tel" autocomplete="tel" required="" placeholder="98XXX XXXXX" onChange="{{setMobile}}">',
  '<input class="vm-input" id="f-mob" type="tel" inputmode="tel" autocomplete="tel" required="" placeholder="98XXX XXXXX" onChange="{{setMobile}}" aria-invalid="{{invMob}}" aria-describedby="f-mob-err">'),
 ('<sc-if value="{{errMob}}" hint-placeholder-val="{{false}}"><span class="vm-field__error">',
  '<sc-if value="{{errMob}}" hint-placeholder-val="{{false}}"><span class="vm-field__error" id="f-mob-err">'),
 ('<input class="vm-input" id="f-city" autocomplete="address-level2" required="" onChange="{{setCity}}">',
  '<input class="vm-input" id="f-city" autocomplete="address-level2" required="" onChange="{{setCity}}" aria-invalid="{{invCity}}" aria-describedby="f-city-err">'),
 ('<sc-if value="{{errCity}}" hint-placeholder-val="{{false}}"><span class="vm-field__error">',
  '<sc-if value="{{errCity}}" hint-placeholder-val="{{false}}"><span class="vm-field__error" id="f-city-err">'),
 ('<input type="checkbox" required="" checked="{{agree}}" onChange="{{setAgree}}">',
  '<input type="checkbox" id="f-agree" required="" checked="{{agree}}" onChange="{{setAgree}}" aria-invalid="{{invAgree}}" aria-describedby="f-agree-err">'),
 ('<sc-if value="{{errAgree}}" hint-placeholder-val="{{false}}"><span class="vm-field__error">',
  '<sc-if value="{{errAgree}}" hint-placeholder-val="{{false}}"><span class="vm-field__error" id="f-agree-err">'),
 ('<p class="vm-eyebrow" style="margin: 8px 0 0;">॥ જય શ્રી વિહત મેલડી માઁ ॥</p><h2>આપની નોંધણી થઈ ગઈ છે</h2>', '<p class="vm-eyebrow" style="margin: 8px 0 0;">॥ જય શ્રી વિહત મેલડી માઁ ॥</p><h2 tabindex="-1">આપની નોંધણી થઈ ગઈ છે</h2>'),
 ('errName: errName, errMob: errMob, errCity: errCity, errSeva: errSeva, errAgree: errAgree, anyErr: anyErr,',
  "errName: errName, errMob: errMob, errCity: errCity, errSeva: errSeva, errAgree: errAgree, anyErr: anyErr,\n"
  "invName: errName ? 'true' : 'false', invMob: errMob ? 'true' : 'false', invCity: errCity ? 'true' : 'false', invAgree: errAgree ? 'true' : 'false',"),
 ("submit: () => {\nconst ok = s.name.trim().length >= 2 && digits.length === 10 && s.city.trim().length >= 2 && s.sevas.length > 0 && !!s.slot && s.agree;\nthis.setState(ok ? { done: true, tried: false } : { tried: true });\n},",
  "submit: (e) => {\nconst ok = s.name.trim().length >= 2 && digits.length === 10 && s.city.trim().length >= 2 && s.sevas.length > 0 && !!s.slot && s.agree;\nthis.setState(ok ? { done: true, tried: false } : { tried: true });\n"
  "const root = e && e.currentTarget && e.currentTarget.closest('.vm-root');\n"
  "if (ok && root) setTimeout(() => { const card = root.querySelector('.vx-success'); if (!card) return; card.scrollIntoView({ block: 'start' }); const h = card.querySelector('h2'); if (h) h.focus({ preventScroll: true }); }, 40);\n"
  "if (!ok) { const form = e && e.currentTarget && e.currentTarget.closest('form'); const first = [[s.name.trim().length < 2, '#f-name'], [digits.length !== 10, '#f-mob'], [s.city.trim().length < 2, '#f-city'], [s.sevas.length === 0, 'input[name=\"seva\"]'], [!s.slot, '.vx-shift'], [!s.agree, '#f-agree']].find((x) => x[0]);\n"
  "  if (form && first) setTimeout(() => { const el = form.querySelector(first[1]); if (!el) return; el.scrollIntoView({ block: 'center' }); el.focus({ preventScroll: true }); }, 40); }\n},"),
]
for b in ('Seva', 'SevaMobile'):
    p = os.path.join(root, b + '.dc.html'); s = open(p, encoding='utf-8').read()
    for old, new in R:
        assert s.count(old) == 1, (b, old[:60]); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s)
css = """

/* ════════ Seva form: the confirmation comes into view after a successful registration (item 3) ════════
   The confirmation replaces the long form, so the visitor was left far below it (phone: ~2,300 px). The page now moves to it and focuses
   its heading; this keeps a little space above it and gives the heading no focus ring (it is a destination, not a control). */
.vm-root .vx-success { scroll-margin-top: 24px; }
.vm-root .vx-success h2:focus { outline: none; }
"""
p = os.path.join(root, 'site.css'); s = open(p, encoding='utf-8').read(); assert '.vx-success { scroll-margin-top' not in s
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + css.lstrip('\n'))
print('item 3 applied to Seva, SevaMobile + site.css')
