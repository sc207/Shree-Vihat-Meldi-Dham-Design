"""v137: owner 16 Oct 2026 — Home photo gallery ("ફોટો ગેલેરી"): "mandir, mataji, karamshi bapa, suresh bapa".
Order was મંદિર · કરમશીબાપા · વિહત માઁ · સુરેશબાપા · મેલડી માઁ → now મંદિર · વિહત માઁ · મેલડી માઁ · કરમશીબાપા · સુરેશબાપા (all Home boards).
Phones (≤ 760 px) used to show only the first three tiles (temple + two) — with the new order that would hide both Bapas, and today it hides
સુરેશબાપા and મેલડી માઁ. Now phones show all five: the temple full width, then the two માતાજી side by side, then the two Bapas.
Pages: Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile2 (figure order only) + one site.css block (+ HomeMobile2 frame, canvas "h").
usage: python3 tools/examples/apply_v137_home_photo_order.py <project folder>"""
import json, os, re, sys
ORDER = ['નવું મંદિર — સ્થાપત્ય ચિત્ર', 'જય શ્રી વિહત માઁ', 'જય શ્રી મેલડી માઁ', 'ભગવાન શ્રી કરમશીબાપા', 'ભુવાજી શ્રી સુરેશબાપા']
OLD = ['નવું મંદિર — સ્થાપત્ય ચિત્ર', 'ભગવાન શ્રી કરમશીબાપા', 'જય શ્રી વિહત માઁ', 'ભુવાજી શ્રી સુરેશબાપા', 'જય શ્રી મેલડી માઁ']
for page in ('Main', 'HomeTablet', 'HomeTabletL', 'HomePhoneL', 'HomeMobile2'):
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count('<div class="vx-strip">') == 1
    i = s.index('<div class="vx-strip">') + len('<div class="vx-strip">'); j = s.index('</div>', i)
    figs = re.findall(r'<figure.*?</figure>', s[i:j]); assert ''.join(figs) == s[i:j], page
    alts = [re.search(r'alt="([^"]*)"', f).group(1) for f in figs]; assert alts == OLD, (page, alts)
    by = dict(zip(alts, figs)); s = s[:i] + ''.join(by[a] for a in ORDER) + s[j:]
    open(p, 'w', encoding='utf-8').write(s); print('reordered', page)
BLOCK = '''
/* v137 — Home "ફોટો ગેલેરી" on phones: show all five photos (temple full width, then the two માતાજી, then the two Bapas).
   Was: only the first three (the rest hidden by `.vx-strip figure:nth-child(n+4) { display: none; }`). */
@media (max-width: 760px) {
  .vm-root .vx-strip figure:nth-child(n+4) { display: block; }
}
'''
p = os.path.join(sys.argv[1], 'site.css'); s = open(p, encoding='utf-8').read()
assert '/* v137 — Home' not in s and s.count('.vx-strip figure:nth-child(n+4) { display: none; }') == 1
open(p, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + BLOCK); print('appended v137 block')

# frame: HomeMobile2 shows one more row of photos (+236 px) — root style, data-props, canvas.json "h"
old, new = 5750, 5986
p = os.path.join(sys.argv[1], 'HomeMobile2.dc.html'); s = open(p, encoding='utf-8').read()
for a, b in (('height: %dpx;' % old, 'height: %dpx;' % new), ('"height": %d' % old, '"height": %d' % new)):
    assert s.count(a) == 1, (a, s.count(a)); s = s.replace(a, b)
open(p, 'w', encoding='utf-8').write(s)
p = os.path.join(sys.argv[1], 'canvas.json'); s = open(p, encoding='utf-8').read()
a = '"HomeMobile2.dc.html": {\n      "h": %d,' % old
assert s.count(a) == 1; s = s.replace(a, '"HomeMobile2.dc.html": {\n      "h": %d,' % new); json.loads(s)
open(p, 'w', encoding='utf-8').write(s); print('HomeMobile2 frame', old, '->', new)
