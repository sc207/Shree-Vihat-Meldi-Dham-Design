"""v146: owner 16 Oct 2026 — "karamshi bapa image actually looks like ai generated … same hd and humanize image set for karamshibapa image.
if have same image in other pages also fix over there" (then chose option B: keep the blessing photo, HD).
Image 27 (owner's photo of 14 Oct, as supplied) → 38: the same photo through the same HD step as સુરેશબાપા's photos (Real-ESRGAN x4plus,
halved to 2×) plus a photographic finish (gentle clarity, fine grain) — tasks/karamshi-natural/scripts/photo_finish.py; saved at 1.5×
(1629×2172, same 3:4 shape, so every frame shows it exactly as before). 14 places on 9 pages. Only the image address changes.
(Option C — his genuine photo 08 on the same glow — was prepared and shown but not chosen: tasks/karamshi-natural/.)
usage: python3 tools/examples/apply_v146_karamshibapa_hd.py <project folder>"""
import glob, os, sys
OLD, NEW = '/_blob/0719d6d6a37c83a09b9880ba4507c70f', '/_blob/12fd255804899d0ead71c2e9e83930e0'
PAGES = {'Gallery': 1, 'GalleryMobile': 1, 'History': 1, 'HistoryMobile': 1, 'HomeMobile2': 2, 'HomePhoneL': 2, 'HomeTablet': 2, 'HomeTabletL': 2, 'Main': 2}
for page, n in PAGES.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count(OLD) == n, (page, s.count(OLD), n); open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
assert not [f for f in glob.glob(os.path.join(sys.argv[1], '*.dc.html')) if OLD in open(f, encoding='utf-8').read()]
print('updated', len(PAGES), 'pages, 14 places')
