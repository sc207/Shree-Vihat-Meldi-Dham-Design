"""v127: two soft સુરેશબાપા photos replaced by HD versions (exactly 2x, Real-ESRGAN x4plus halved; faces checked against the originals).
13 smiling cut-out 470x501 -> 32 (940x1002, RGBA); 11 candid 585x882 -> 33 (1170x1764). Only image addresses change.
09 (કરમશીબાપા seated poster) deliberately NOT upscaled: the upscalers drew new outlines on his face - needs a better original from the trust.
usage: python3 tools/examples/apply_v127_portraits_hd.py <project folder>"""
import os, sys
MAP = {'/_blob/f784ff0d57da00d73030819bb850bb43': '/_blob/fc35afd1b74520e77020323b6e293a68',   # 13 -> 32 Sureshbapa smiling cut-out HD
       '/_blob/e1b6930a984c9f3a8eb9b9783ae97fe9': '/_blob/805bf02d7a1d405c2fc9caea541abbee'}   # 11 -> 33 Sureshbapa candid HD
EXPECT = {'Gallery': [1, 1], 'GalleryMobile': [1, 1], 'History': [0, 1], 'HistoryMobile': [0, 1]}
for page, counts in EXPECT.items():
    p = os.path.join(sys.argv[1], page + '.dc.html'); s = open(p, encoding='utf-8').read()
    for (old, new), n in zip(MAP.items(), counts):
        assert s.count(old) == n, (page, old, s.count(old), n); s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s); print('updated', page)
