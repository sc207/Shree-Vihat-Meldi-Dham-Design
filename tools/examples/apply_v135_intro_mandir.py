"""v135: owner 16 Oct 2026 — "નવા મંદિરનો પરિચય: replace ટ્રસ્ટનો to મંદિરનો. remove દાન".
1. "… પવિત્ર ધામ બને, એ જ ટ્રસ્ટનો મુખ્ય હેતુ છે." → "… એ જ મંદિરનો મુખ્ય હેતુ છે." (new-temple introduction: NewTemple + all Home boards)
2. "ટ્રસ્ટનો વિશ્વાસ છે કે ભક્તોના સહયોગ, દાન અને નિઃસ્વાર્થ સેવાથી …" → "મંદિરનો વિશ્વાસ છે કે ભક્તોના સહયોગ અને નિઃસ્વાર્થ સેવાથી …" (NewTemple)
usage: python3 tools/examples/apply_v135_intro_mandir.py <project folder>"""
import glob, os, sys
A = ('એ જ ટ્રસ્ટનો મુખ્ય હેતુ છે.', 'એ જ મંદિરનો મુખ્ય હેતુ છે.')
B = ('ટ્રસ્ટનો વિશ્વાસ છે કે ભક્તોના સહયોગ, દાન અને નિઃસ્વાર્થ સેવાથી', 'મંદિરનો વિશ્વાસ છે કે ભક્તોના સહયોગ અને નિઃસ્વાર્થ સેવાથી')
EXPECT = {'Main': (1, 0), 'HomeTablet': (1, 0), 'HomeTabletL': (1, 0), 'HomePhoneL': (1, 0), 'HomeMobile': (1, 0), 'NewTemple': (1, 1), 'NewTempleMobile': (1, 1)}
for page, (na, nb) in EXPECT.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count(A[0]) == na and s.count(B[0]) == nb, (page, s.count(A[0]), s.count(B[0]))
    s = s.replace(*A).replace(*B); open(p, 'w', encoding='utf-8').write(s)
left = [os.path.basename(f) for f in glob.glob(os.path.join(sys.argv[1], '*.dc.html')) if 'ટ્રસ્ટનો' in open(f, encoding='utf-8').read()]
assert not left, left
print('updated', len(EXPECT), 'pages')
