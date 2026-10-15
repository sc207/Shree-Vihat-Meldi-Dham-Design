"""v125: the four ધામ પરિવાર pictures (Vihat માઁ, Meldi માઁ, Lakhnechi માઁ, Goga Maharaj) replaced by HD versions composed the same way:
1200x1500 (4:5 = the arch frame), one warm-gold background with a soft light behind the head and a soft ground shadow, every figure the
same height on the same baseline, inside the arch top. Vihat/Meldi from the HD cut-outs 21/22 (same paintings as 03/04); Lakhnechi/Goga
from 05/06 enlarged x4 with Real-ESRGAN (x4plus) and cut out with IS-Net. Only image addresses change (History, Gallery + phone pages).
usage: python3 tools/examples/apply_v125_deity_hd.py <project folder>"""
import os, sys
MAP = {'/_blob/5db2fa3066346bbda071d80127890079': '/_blob/6a5dfa42bf4395ad0c91358b6d58b309',   # 03 -> 28 vihat
       '/_blob/67db8acad0ff4fc9a1690e90a08d539b': '/_blob/8c6bc0f2d3dd302001ff1f0156ef263c',   # 04 -> 29 meldi
       '/_blob/e31c2f7a518cb9d094489412d6c323c8': '/_blob/64fea5310ba43b3bb3862a6fbc35b15d',   # 05 -> 30 lakhnechi
       '/_blob/713e6519487a5ab4a26d821bbca861a8': '/_blob/707057297d216df873c2b29940cce2e3'}   # 06 -> 31 goga
EXPECT = {'History': [1, 1, 1, 1], 'HistoryMobile': [1, 1, 1, 1], 'Gallery': [2, 1, 1, 1], 'GalleryMobile': [2, 1, 1, 1]}
proj = sys.argv[1]
for name, counts in EXPECT.items():
    p = os.path.join(proj, name + '.dc.html'); s = open(p, encoding='utf-8').read()
    for (old, new), n in zip(MAP.items(), counts):
        assert s.count(old) == n, (name, old, s.count(old), n); assert new not in s
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s); print(name, 'ok')
left = [f for f in os.listdir(proj) if f.endswith('.dc.html') and any(o in open(os.path.join(proj, f), encoding='utf-8').read() for o in MAP)]
assert not left, left
print('old 03-06 referenced nowhere')
