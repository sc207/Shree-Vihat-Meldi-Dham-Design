"""v147: owner 16 Oct 2026 — "it looks good. just now sharp that image as you can see if we zoom see blessing hand it does not looks in focus.
so do it as we did in suresh bapa." — then: "as like blessing hand also focus on face so it looks more better and also check if sharpness
required or not".
Image 38 → 39: the same photo, same HD step and finish, but (1) the blessing hand, rings and wrist brought into focus and the face lightly
focused (halo-free edge sharpening inside soft masks; tasks/karamshi-natural/scripts/make_38_sharp.py) and (2) saved at the full 2× like સુરેશબાપા's
34 (2172×2896, same 3:4 shape, so every frame shows it exactly as before). 14 places on 9 pages. Only the image address changes.
usage: python3 tools/examples/apply_v147_karamshibapa_hand_focus.py <project folder>"""
import glob, os, sys
OLD, NEW = '/_blob/12fd255804899d0ead71c2e9e83930e0', '/_blob/3cc36279d9180905d49a932af9ea9e1a'
PAGES = {'Gallery': 1, 'GalleryMobile': 1, 'History': 1, 'HistoryMobile': 1, 'HomeMobile2': 2, 'HomePhoneL': 2, 'HomeTablet': 2, 'HomeTabletL': 2, 'Main': 2}
for page, n in PAGES.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count(OLD) == n, (page, s.count(OLD), n); open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
assert not [f for f in glob.glob(os.path.join(sys.argv[1], '*.dc.html')) if OLD in open(f, encoding='utf-8').read()]
print('updated', len(PAGES), 'pages, 14 places')
