# EXAMPLE kept for reference: the exact script that produced this published version.
# Pattern: exact-string replacements, each asserted to occur once, applied to every page variant; new CSS appended to site.css;
# frame heights updated in the page root, data-props and canvas.json. Its default path points to the old session —
# ALWAYS pass your work folder WITH a trailing slash (paths are built as folder + file name):
#   python3 tools/examples/apply_v106_sankalp.py work/project/
# Only meaningful against the version it was written for (it asserts the old text is present, so it stops safely otherwise).
# v106: the trust's "નવા મંદિરનો સંકલ્પ" text (10 Oct 2026) placed in the design.
# Trust text used verbatim except: સનંદ→સાણંદ, ભગવાન કરમશી બાપા→ભગવાન શ્રી કરમશીબાપા (site-wide form),
# તેમના→તેઓશ્રીના (site's honorific for Bapa), સમૂહિક→સામૂહિક (spelling). Subtitle used as the section eyebrow.
import sys
P = sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/-home-claude/dd84a57e-267c-5f0e-ba89-c24b2694ae3a/scratchpad/apply_sk/project/'

S1 = 'શ્રી વિહત મેલડી ધામ, સાણંદની સંકલ્પના માતાજી પ્રત્યેની અતૂટ શ્રદ્ધા, ભક્તિ અને સેવાના પવિત્ર ભાવમાંથી સાકાર થઈ છે.'
S2 = 'પરમ પૂજ્ય ભગવાન શ્રી કરમશીબાપાના પાવન આશીર્વાદ અને તેઓશ્રીના આધ્યાત્મિક વારસાને વંદન કરીને, માતાજીના ભવ્ય મંદિરની સ્થાપનાનો સંકલ્પ લેવામાં આવ્યો છે.'
S3 = 'આ મંદિર માત્ર આસ્થાનું કેન્દ્ર જ નહીં, પરંતુ સંસ્કાર, સમર્પણ, એકતા અને સેવાભાવને પ્રોત્સાહન આપતું પવિત્ર ધામ બને, એ જ ટ્રસ્ટનો મુખ્ય હેતુ છે.'
P2 = ('નવા મંદિરના નિર્માણ પાછળનો મુખ્ય ઉદ્દેશ ભક્તોને માતાજીનાં દર્શન, પૂજા-અર્ચના, યજ્ઞ, ભાગવત સપ્તાહ અને વિવિધ ધાર્મિક ઉત્સવો દ્વારા આધ્યાત્મિક શાંતિ તથા ભક્તિનો અનુભવ કરાવવાનો છે. '
      'સાથે જ, નવી પેઢીને આપણી ધાર્મિક પરંપરાઓ, સંસ્કૃતિ અને સંસ્કારો સાથે જોડીને સમાજમાં એકતા, સહકાર અને પરસ્પર પ્રેમની ભાવનાને મજબૂત બનાવવાનો સંકલ્પ છે.')
P3 = ('શ્રી વિહત મેલડી ધામ ભવિષ્યમાં ભક્તો માટે શ્રદ્ધા, સેવા અને સામૂહિક આધ્યાત્મિક અનુભૂતિનું વિશેષ કેન્દ્ર બને, જ્યાં દરેક ભક્તને માતાજીના આશીર્વાદ સાથે આત્મિક શાંતિ અને સકારાત્મક પ્રેરણા મળે. '
      'ટ્રસ્ટનો વિશ્વાસ છે કે ભક્તોના સહયોગ, દાન અને નિઃસ્વાર્થ સેવાથી આ પવિત્ર સંકલ્પ સાકાર થશે અને ધામ આવનારી પેઢીઓ માટે પણ આસ્થા તથા સંસ્કૃતિનો અમૂલ્ય વારસો બની રહેશે.')

EDITS = {
    # New temple page: eyebrow + three paragraphs
    ('NewTemple.dc.html', 'NewTempleMobile.dc.html'): [
        ('<div class="vm-grid vm-grid--split" style="gap: 80px;"><div style="display: flex; flex-direction: column; gap: 24px;"><div class="vm-heading"><p class="vm-eyebrow">સંકલ્પ</p>',
         '<div class="vm-grid vm-grid--split vx-sk" style="gap: 80px;"><div style="display: flex; flex-direction: column; gap: 24px;"><div class="vm-heading"><p class="vm-eyebrow">સંકલ્પ</p>'),
        ('<p class="vm-eyebrow">સંકલ્પ</p>\n<h2 id="vis-t"', '<p class="vm-eyebrow">મંદિરની સંકલ્પના અને હેતુ</p>\n<h2 id="vis-t"'),
        ('<p class="vm-body">[નવા મંદિરની કલ્પના કેવી રીતે થઈ, તેનો હેતુ શું છે અને ભક્તો માટે તે શું નવું લાવશે — ટ્રસ્ટ દ્વારા ૨–૩ ફકરામાં]</p>',
         f'<div class="vx-prose"><p class="vm-body">{S1} {S2} {S3}</p><p class="vm-body">{P2}</p><p class="vm-body">{P3}</p></div>'),
    ],
    # Home: the 2–3 sentence introduction
    ('Main.dc.html', 'HomeTablet.dc.html', 'HomeTabletL.dc.html', 'HomePhoneL.dc.html', 'HomeMobile.dc.html'): [
        ('<p class="vm-lead">[નવા મંદિરના સંકલ્પનો ટૂંકો પરિચય — બે-ત્રણ વાક્યમાં, ટ્રસ્ટ દ્વારા]</p>', f'<p class="vm-lead">{S2} {S3}</p>'),
    ],
    # History, chapter 6: the સંકલ્પ sentence completes the existing line
    ('History.dc.html', 'HistoryMobile.dc.html'): [
        ('<p class="vm-lead">આસ્થા, પરંપરા અને ભવ્ય સ્થાપત્યનું મિલન — [નવા મંદિરના સંકલ્પની કથા, ટ્રસ્ટ દ્વારા]</p>', f'<p class="vm-lead">આસ્થા, પરંપરા અને ભવ્ય સ્થાપત્યનું મિલન — {S2}</p>'),
    ],
}
for files, reps in EDITS.items():
    for fn in files:
        s = open(P + fn, encoding='utf-8').read()
        for old, new in reps:
            if '\n' in old:   # markup is stored on one line; match with or without the line break
                old1 = old.replace('\n', '')
                assert s.count(old1) == 1, (fn, old1[:60]); s = s.replace(old1, new.replace('\n', ''))
            else:
                assert s.count(old) == 1, (fn, old[:60]); s = s.replace(old, new)
        open(P + fn, 'w', encoding='utf-8').write(s); print(fn, len(reps), 'edit(s)')

CSS = '''
/* ════════ New temple · સંકલ્પ: the trust's three paragraphs (v106) ════════ */
.vx-prose { display: flex; flex-direction: column; gap: 16px; }
.vx-prose .vm-body { margin: 0; }
/* the text is now the main content: wider text column on desktop, stacked (text, then image) below 1100 px */
@media (min-width: 1100px) { .vm-grid--split.vx-sk { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); } }
@media (min-width: 768px) and (max-width: 1099px) {
  .vm-grid--split.vx-sk { grid-template-columns: minmax(0, 1fr); gap: 48px !important; }
  .vx-sk > .vx-crop { max-width: 560px; }
  .vx-sk .vx-facts { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .vx-sk .vx-facts > div + div { padding-left: var(--space-lg); border-left: 1px solid var(--line); }
}
'''
c = open(P + 'site.css', encoding='utf-8').read()
assert '.vx-prose' not in c
open(P + 'site.css', 'w', encoding='utf-8').write(c.rstrip('\n') + '\n' + CSS)
print('site.css appended')

# Frame heights: natural content height + 3 px at the daily maximum (04:40, 06:30, 12:30, 19:30, 22:30 IST)
import json
ROOTS = {'NewTemple': (8366, 8647), 'NewTempleMobile': (11082, 11846), 'Main': (8037, 8090), 'HomeTablet': (10571, 10804), 'HomeTabletL': (8059, 8192),
         'HomePhoneL': (8892, 9092), 'HomeMobile': (5083, 5249), 'History': (8055, 8129), 'HistoryMobile': (10411, 10511)}
for name, (old, new) in ROOTS.items():
    fn = name + '.dc.html'; s = open(P + fn, encoding='utf-8').read()
    assert s.count(f'height: {old}px;') == 1 and s.count(f'"height": {old}') == 1, fn
    s = s.replace(f'height: {old}px;', f'height: {new}px;').replace(f'"height": {old}', f'"height": {new}')
    open(P + fn, 'w', encoding='utf-8').write(s)
c = open(P + 'canvas.json', encoding='utf-8').read(); d = json.loads(c)
for name, (old, new) in ROOTS.items():
    h = d['boards'][name + '.dc.html']['h']; want = min(new, 8000)
    if h != want:
        a = c.index(f'"{name}.dc.html": {{'); e = c.index('}', a); blk = c[a:e]; assert blk.count(f'"h": {h}') == 1
        c = c[:a] + blk.replace(f'"h": {h}', f'"h": {want}') + c[e:]; print('canvas', name, h, '->', want)
assert {k: v['h'] for k, v in json.loads(c)['boards'].items()} == {k: (min(ROOTS[k[:-8]][1], 8000) if k[:-8] in ROOTS else v['h']) for k, v in d['boards'].items()}
open(P + 'canvas.json', 'w', encoding='utf-8').write(c)
print('frames updated')

# canvas to-do note: the સંકલ્પ text has arrived; architect, sankalp year and completion time are still awaited
c = open(P + 'canvas.json', encoding='utf-8').read(); o = '• નવા મંદિરનો સંકલ્પ, સ્થપતિ, સંકલ્પ વર્ષ, પૂર્ણતાનો સમય'
if o in c: c = c.replace(o, '• નવા મંદિરના સ્થપતિ, સંકલ્પ વર્ષ, પૂર્ણતાનો સમય'); json.loads(c); open(P + 'canvas.json', 'w', encoding='utf-8').write(c)
