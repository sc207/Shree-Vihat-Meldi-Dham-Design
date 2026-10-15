"""Per image: worst sharpness (real pixels / pixels needed on a 2x or 3x screen) and where; cover crops.
usage: python3 tasks/image-audit/scripts/summarise.py results/measure.json"""
import json, re, sys, collections
inv = {b: (int(n), name, f'{w}×{h}') for n, name, b, w, h, _ in re.findall(r'^\| (\d\d) \| `([^`]+)` \| `([0-9a-f]{32})` \| (\d+)×(\d+) \| ([^|]+)\|', open('DESIGN_SYSTEM.md').read(), re.M)}
d = json.load(open(sys.argv[1]))
per = collections.defaultdict(list)
for key, items in d.items():
    for it in items:
        if it.get('sharp') is None or it['hidden']: continue
        per[it['src']].append((it['sharp'], key, it['w'], it['h'], it['fit'], it['pos'], it.get('crop_w', 0), it.get('crop_h', 0), it['cls'][:60]))
for src, L in sorted(per.items(), key=lambda kv: min(x[0] for x in kv[1])):
    no, name, px = inv.get(src, (0, src, '?'))
    L.sort()
    worst = L[0]
    print(f'{no:02d} {name:45s} {px:10s} worst sharp {worst[0]:.2f} at {worst[1]} ({worst[2]}x{worst[3]} {worst[4]} {worst[5]})  placements {len(L)}')
    seen = set()
    for x in L:
        k = (x[1].split('|')[0], x[8])
        if k in seen or x[0] >= 1.0: continue
        seen.add(k); print(f'      {x[0]:.2f}  {x[1]:24s} {x[2]}x{x[3]} {x[4]} pos {x[5]} crop w{x[6]} h{x[7]}  [{x[8]}]')
