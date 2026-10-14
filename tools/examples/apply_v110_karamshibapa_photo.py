"""v110: owner's new photo of ભગવાન શ્રી કરમશીબાપા (blessing, half-length, 3:4, 1086x1448) replaces the close-up 07
everywhere the close-up was shown: home portrait pair + home photo strip (Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile2),
History chapter 3 portrait (History, HistoryMobile), Gallery banner trio (Gallery, GalleryMobile).
Only the image address changes; alt text, captions, classes and inline styles stay as they are.
usage: python3 tools/examples/apply_v110_karamshibapa_photo.py <project folder>"""
import sys, os
OLD = '/_blob/692526c97fb81800db3adb90c432cc9a'   # 07_portrait_karamshibapa_closeup-glow (stays in the asset store, now unused)
NEW = '/_blob/0719d6d6a37c83a09b9880ba4507c70f'   # 27_portrait_karamshibapa_blessing-glow
EXPECT = {'Main': 2, 'HomeTablet': 2, 'HomeTabletL': 2, 'HomePhoneL': 2, 'HomeMobile2': 2,
          'History': 1, 'HistoryMobile': 1, 'Gallery': 1, 'GalleryMobile': 1}
proj = sys.argv[1]
for name, n in EXPECT.items():
    p = os.path.join(proj, name + '.dc.html')
    s = open(p, encoding='utf-8').read()
    assert s.count(OLD) == n, (name, s.count(OLD), n)
    assert NEW not in s, name
    open(p, 'w', encoding='utf-8').write(s.replace(OLD, NEW))
    print('%-14s %d replaced' % (name, n))
# nothing else may still point at the old close-up
left = [f for f in os.listdir(proj) if f.endswith(('.html', '.css', '.json')) and OLD in open(os.path.join(proj, f), encoding='utf-8').read()]
assert not left, left
print('done; old close-up referenced nowhere')
