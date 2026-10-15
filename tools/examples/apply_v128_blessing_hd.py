"""v128: સુરેશબાપા blessing photo (10, 1100x1019; Home pair + strip, History arch, Gallery) replaced by its HD version 34 (2200x2038, exactly 2x:
Real-ESRGAN x4plus halved; face and hand checked against the original). Only the image address changes, on 9 boards (14 places: home boards use it twice, pair + strip).
usage: python3 tools/examples/apply_v128_blessing_hd.py <project folder>"""
import os, sys
OLD, NEW = '/_blob/4e30bcd6319bfef6bce709ce0ef4afb1', '/_blob/f4d99b08a58c4d7320683cd72bbc67cc'
PAGES = {'Gallery': 1, 'GalleryMobile': 1, 'History': 1, 'HistoryMobile': 1, 'HomeMobile2': 2, 'HomePhoneL': 2, 'HomeTablet': 2, 'HomeTabletL': 2, 'Main': 2}
for page, n in PAGES.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    assert s.count(OLD) == n, (page, s.count(OLD), n); open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW)); print('updated', page)
