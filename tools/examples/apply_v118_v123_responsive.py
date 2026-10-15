"""Responsive / UX fixes found in the device scan of v116 (15–16 Oct 2026). One part = one published version
(v117 in the artifact history is a re-save by the Design type with no content change, so the fixes are v118–v123).
usage: python3 tools/examples/apply_v118_v123_responsive.py <project folder> <part 1..6>
  1 (v118) phone Home: remove the leftover WhatsApp "જોડાઓ" button that sat over the દર્શન section (HomeMobile only)
  2 (v119) History chapter index below 375 px: the grey label goes under the title instead of running into it
  3 (v120) phone turned sideways: Home banner buttons never cut; darshan card times wrap inside the card
  4 (v121) festival overview chart on phones: night labels 11 px -> 13 px
  5 (v122) WhatsApp band on small laptops (1000–1279 px): text column no longer squeezed; heading lines balanced everywhere;
           HomeTabletL frame 8192 -> 8104
  6 (v123) phones and touch screens: touch areas of small links and buttons at least 44 px, no visual change
Exact-string edits, each asserted; CSS is appended at the end of site.css as one commented block per part."""
import os, re, sys
proj, part = sys.argv[1], int(sys.argv[2])
css_path = os.path.join(proj, 'site.css')


def append_css(block):
    s = open(css_path, encoding='utf-8').read()
    marker = block.strip().splitlines()[0]
    assert marker not in s, 'part already applied'
    open(css_path, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n\n' + block.strip('\n') + '\n')


if part == 1:
    p = os.path.join(proj, 'HomeMobile.dc.html')
    s = open(p, encoding='utf-8').read()
    m = re.findall(r'<a class="vm-wa-fab vx-fab"[^>]*>.*?</a>', s, flags=re.S)
    assert len(m) == 1 and 'જોડાઓ' in m[0], len(m)
    s = s.replace(m[0], '', 1)
    open(p, 'w', encoding='utf-8').write(s)
    others = [f for f in os.listdir(proj) if f.endswith('.dc.html') and 'vm-wa-fab' in open(os.path.join(proj, f), encoding='utf-8').read()]
    assert not others, others

elif part == 2:
    append_css('''
/* ════════ History chapter index on very small phones (v119) ════════
   Below 375 px the grey label sat beside the chapter title and ran into it ("આધ્યાત્મિક" × "માતાજી અને ધામ પરિવાર" at 320 px).
   The label now sits under the title; 375 px and wider unchanged. */
@media (max-width: 374px) {
  .vm-root .vx-toc a { grid-template-columns: 40px minmax(0, 1fr); row-gap: 2px; }
  .vm-root .vx-toc small { grid-column: 2; }
}''')

elif part == 3:
    append_css('''
/* ════════ Phone turned sideways: Home banner buttons and darshan card (v120) ════════
   568–640 px wide: "મહોત્સવ વિશે જાણો →" was cut (equal-width buttons, no wrapping) and "સવારે ૬:૦૦ – રાત્રે ૧૦:૦૦" ran out of the
   darshan card (no wrapping in a narrow column). Buttons now size to their label and wrap to a second row when needed; card times may wrap (balanced lines). */
@media (orientation: landscape) and (max-height: 500px) {
  .vm-root .vx-home-hero .vm-btn-row { flex-wrap: wrap; }
  .vm-root .vx-home-hero .vm-btn-row .vm-btn { flex: 1 1 auto; min-width: max-content; }
  .vm-root .vx-dgrid .vx-dt__item { padding: 16px 18px; column-gap: 12px; }
  .vm-root .vx-dgrid .vx-dt__item b { white-space: normal; flex-wrap: wrap; text-wrap: balance; }
}''')

elif part == 4:
    append_css('''
/* ════════ Festival overview chart on phones: readable night labels (v121) ════════
   "રામ કથા" and "રમેલ" pills were 11 px. Now 13 px; on the narrowest phones the label may take two lines inside the pill. */
@media (max-width: 760px) {
  .vm-root .vx-week__nt span { font-size: 13px; line-height: 1.15; }
}''')

elif part == 5:
    append_css('''
/* ════════ WhatsApp band on small laptops 1000–1279 px (v122) ════════
   Four columns (badge · text · QR · button) left the text 210–330 px wide: the heading broke word by word at 1024 px and left
   "જોડાઓ" alone at 1180 px. At these widths the round badge is smaller and the gaps tighter; heading lines are balanced at all widths. */
.vm-root .vm-wa__copy h3 { text-wrap: balance; }
@media (min-width: 1000px) and (max-width: 1279px) {
  .vm-root .vx-wa { gap: 32px; padding-left: 40px; padding-right: 40px; }
  .vm-root .vx-wa .vm-wa__glyph { width: 64px; height: 64px; }
  .vm-root .vx-wa .vm-wa__glyph svg { width: 34px; height: 34px; }
  .vm-root .vx-wa .vm-wa__copy h3 { font-size: 28px; }
}''')

    # the 1180 px tablet board gets shorter (band 88 px lower): frame = natural height + 3 (tools/frame_heights.py); canvas h stays 8000 (cap)
    p = os.path.join(proj, 'HomeTabletL.dc.html')
    t = open(p, encoding='utf-8').read()
    for a, b in (('style="width: 1180px; height: 8192px;"', 'style="width: 1180px; height: 8104px;"'),
                 ('"$preview": {"width": 1180, "height": 8192}', '"$preview": {"width": 1180, "height": 8104}')):
        assert t.count(a) == 1, a
        t = t.replace(a, b)
    open(p, 'w', encoding='utf-8').write(t)

elif part == 6:
    append_css('''
/* ════════ Phones and touch screens: touch areas of at least 44 px, no visual change (v123) ════════
   Small links and buttons were 25–40 px tall (footer links, festival strip link, breadcrumb, calendar chips, text-size button, ...).
   Each gets an invisible ::after touch area around it (the element becomes position: relative); nothing moves or changes colour.
   Insets are measured from the padding box, so framed controls (1 px border) get 1 px more. Stacked footer links are 40 px apart:
   the space between two links goes to the nearer one (no dead gap). */
@media (max-width: 760px), (pointer: coarse) {
  .vm-root .vm-footer li a, .vm-root .vm-notice a, .vm-root .vx-crumb a, .vm-root .vm-brand, .vm-root .vx-dt__foot a, .vm-root .vx-upnext__more,
  .vm-root .vm-contact__card a, .vm-root .vx-plan__foot a, .vm-root .vx-off__info a, .vm-root .vx-tel, .vm-root .vx-caladd a, .vm-root .vx-fs { position: relative; }
  .vm-root .vm-footer li a::after, .vm-root .vm-notice a::after, .vm-root .vx-crumb a::after, .vm-root .vm-brand::after, .vm-root .vx-dt__foot a::after,
  .vm-root .vx-upnext__more::after, .vm-root .vm-contact__card a::after, .vm-root .vx-plan__foot a::after, .vm-root .vx-off__info a::after,
  .vm-root .vx-tel::after, .vm-root .vx-caladd a::after, .vm-root .vx-fs::after, .vm-root .vx-marquee__btn::after { content: ""; position: absolute; }
  .vm-root .vm-footer li a::after { inset: -4px 0; }
  .vm-root .vm-notice a::after, .vm-root .vm-contact__card a::after { inset: -10px 0; }
  .vm-root .vx-crumb a::after, .vm-root .vx-dt__foot a::after { inset: -8px 0; }
  .vm-root .vx-upnext__more::after { inset: -9px 0; }
  .vm-root .vx-plan__foot a::after { inset: -7px 0; }
  .vm-root .vx-off__info a::after { inset: -6px 0; }
  .vm-root .vx-caladd a::after { inset: -6px 0; }
  .vm-root .vm-brand::after { inset: -2px; }
  .vm-root .vx-fs::after { inset: -3px; }
  .vm-root .vx-tel::after { inset: -1px 0; }
  .vm-root .vx-marquee__btn::after { inset: -5px; border-radius: 50%; }
}''')
else:
    raise SystemExit('part 1..6')
print('part', part, 'applied to', proj)
