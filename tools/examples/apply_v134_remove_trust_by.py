"""v134: owner 16 Oct 2026 — "ટ્રસ્ટ દ્વારા remove this word and check if we can set mandir and not require then dont add anything".
All 15 texts with "ટ્રસ્ટ દ્વારા" (12 pages). Placeholders lose the " — ટ્રસ્ટ દ્વારા" ending; where a sentence needs a subject
("… દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ") it becomes "મંદિર દ્વારા"; elsewhere nothing is added.
Other trust mentions (ટ્રસ્ટ તરફથી …, [ટ્રસ્ટ કાર્યાલય…], ટ્રસ્ટને) are not part of this request and stay.
usage: python3 tools/examples/apply_v134_remove_trust_by.py <project folder>"""
import glob, os, sys
R = [
    ('[દર્શનનો સમય, પહેરવેશ, પાર્કિંગ અને અન્ય સૂચનાઓ — ટ્રસ્ટ દ્વારા]', '[દર્શનનો સમય, પહેરવેશ, પાર્કિંગ અને અન્ય સૂચનાઓ]', ['Contact', 'ContactMobile']),
    ('[સેવા નોંધણીની છેલ્લી તારીખ અને વિગત — ટ્રસ્ટ દ્વારા]', '[સેવા નોંધણીની છેલ્લી તારીખ અને વિગત]', ['Gallery', 'GalleryMobile']),
    ('[નવા મંદિરના નિર્માણની તાજી સ્થિતિ — ટ્રસ્ટ દ્વારા]', '[નવા મંદિરના નિર્માણની તાજી સ્થિતિ]', ['Gallery', 'GalleryMobile']),
    ('ટપકાંવાળી જગ્યાઓ વાસ્તવિક ફોટો માટે છે — ટ્રસ્ટ દ્વારા ફોટો મળ્યે ઉમેરાશે.', 'ટપકાંવાળી જગ્યાઓ વાસ્તવિક ફોટો માટે છે — ફોટો મળ્યે ઉમેરાશે.', ['Gallery', 'GalleryMobile']),
    ('[અહીં મંદિરનો અધિકૃત ઇતિહાસ ઉમેરવાનો છે — ટ્રસ્ટ દ્વારા ચકાસાયેલ લખાણ, ૩–૪ ફકરા]', '[અહીં મંદિરનો અધિકૃત ઇતિહાસ ઉમેરવાનો છે — ચકાસાયેલ લખાણ, ૩–૪ ફકરા]', ['History', 'HistoryMobile']),
    ('[ધામની પરંપરા મુજબ માતાજીનો પરિચય અને પ્રાગટ્યની કથા — ટ્રસ્ટ દ્વારા]', '[ધામની પરંપરા મુજબ માતાજીનો પરિચય અને પ્રાગટ્યની કથા]', ['History', 'HistoryMobile']),
    ('[નાના સ્થાનકથી તીર્થધામ સુધી — મંદિરના વિકાસના મુખ્ય પડાવ — ટ્રસ્ટ દ્વારા]', '[નાના સ્થાનકથી તીર્થધામ સુધી — મંદિરના વિકાસના મુખ્ય પડાવ]', ['History', 'HistoryMobile']),
    ('[કયાં નક્ષત્ર — ટ્રસ્ટ દ્વારા]', '[કયાં નક્ષત્ર]', ['NewTemple', 'NewTempleMobile']),
    ('[પ્રવેશથી ગર્ભગૃહ સુધી ભક્તનો અનુભવ — ટ્રસ્ટ દ્વારા]', '[પ્રવેશથી ગર્ભગૃહ સુધી ભક્તનો અનુભવ]', ['NewTemple', 'NewTempleMobile']),
    ('[યજ્ઞશાળા, પ્રસાદ ખંડ વગેરે — ટ્રસ્ટ દ્વારા]', '[યજ્ઞશાળા, પ્રસાદ ખંડ વગેરે]', ['NewTemple', 'NewTempleMobile']),
    ('ટ્રસ્ટ દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ.', 'મંદિર દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ.', ['PranPratishtha', 'PranPratishthaMobile']),
    ('[ભક્તો માટે આગમન, પાર્કિંગ અને ભીડ વ્યવસ્થાની સૂચના — ટ્રસ્ટ દ્વારા]', '[ભક્તો માટે આગમન, પાર્કિંગ અને ભીડ વ્યવસ્થાની સૂચના]', ['PranPratishtha', 'PranPratishthaMobile']),
    ('[સૂચના — ટ્રસ્ટ દ્વારા]', '[સૂચના]', ['PranPratishtha', 'PranPratishthaMobile']),
    ('[ઓળખપત્ર ક્યાંથી મેળવવું — ટ્રસ્ટ દ્વારા]', '[ઓળખપત્ર ક્યાંથી મેળવવું]', ['Seva', 'SevaMobile']),
    ('[ફોન કરવાનો સમય — ટ્રસ્ટ દ્વારા]', '[ફોન કરવાનો સમય]', ['Seva', 'SevaMobile']),
]
pages = sorted({p for _, _, ps in R for p in ps}); txt = {p: open(os.path.join(sys.argv[1], p + '.dc.html'), encoding='utf-8').read() for p in pages}
for old, new, ps in R:
    for p in ps:
        assert txt[p].count(old) == 1, (p, old, txt[p].count(old)); txt[p] = txt[p].replace(old, new)
for p in pages:
    open(os.path.join(sys.argv[1], p + '.dc.html'), 'w', encoding='utf-8').write(txt[p])
left = [os.path.basename(f) for f in glob.glob(os.path.join(sys.argv[1], '*.dc.html')) if 'ટ્રસ્ટ દ્વારા' in open(f, encoding='utf-8').read()]
assert not left, left
print('updated', len(pages), 'pages; "ટ્રસ્ટ દ્વારા" left nowhere')

# frames (frame_heights.py: shorter placeholders wrap onto fewer lines on phones); canvas "h" stays 8000 (cap)
FR = {'GalleryMobile': (10455, 10403), 'NewTempleMobile': (11846, 11812)}
for page, (old, new) in FR.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    for a, b in (('height: %dpx;' % old, 'height: %dpx;' % new), ('"height": %d' % old, '"height": %d' % new)):
        assert s.count(a) == 1, (page, a, s.count(a)); s = s.replace(a, b)
    open(p, 'w', encoding='utf-8').write(s)
print('frames updated', FR)
