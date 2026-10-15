"""Group scan results: each distinct problem with the boards / sizes / text sizes where it occurs.
usage: python3 aggregate.py OUT.txt scan_0.json scan_1.json ..."""
import json, re, sys, collections
out, files = sys.argv[1], sys.argv[2:]
R = {}
for f in files:
    try: R.update(json.load(open(f)))
    except Exception as e: print('skip', f, e)
def norm(s):   # drop the measured numbers so the same problem groups together
    s = re.sub(r'(past-edge .*\]) "[^"]*" -?\d+\.\.\d+', r'\1', s)
    s = re.sub(r' \d+>\d+$', '', s); s = re.sub(r'by \d+px', 'by Npx', s); s = re.sub(r'tap<(\d+) \d+x\d+', r'tap<\1', s)
    s = re.sub(r'contrast [\d.]+', 'contrast', s); s = re.sub(r'tiny-text [\d.]+px', 'tiny-text', s); s = re.sub(r'sharp to [\d.]+x', 'soft', s)
    s = re.sub(r'long-line \d+cpl', 'long-line', s)
    return s
G = collections.defaultdict(list); N = collections.defaultdict(list); wide = []; errs = []; crash = []; cover = []
for k, v in R.items():
    if 'crash' in v: crash.append(k); continue
    b, sz, t = k.split('|')
    if v['docW'] > v['W']: wide.append(k + ' docW=%d' % v['docW'])
    if v.get('errors'): errs.append(k + ' ' + str(v['errors'][:2]))
    fx = v.get('fixed') or {}
    if fx.get('cover', 0) > 30: cover.append('%s cover %d%% %s' % (k, fx['cover'], fx.get('list')))
    for i in v['issues']: G[norm(i)].append((b, sz, t, i))
    for i in v['notes']: N[norm(i)].append((b, sz, t, i))
with open(out, 'w') as o:
    o.write('runs %d · page wider than screen %d · JS errors %d · crashed %d\n' % (len(R), len(wide), len(errs), len(crash)))
    for x in wide[:60]: o.write('WIDE ' + x + '\n')
    for x in errs[:20]: o.write('ERR ' + x + '\n')
    for x in crash[:20]: o.write('CRASH ' + x + '\n')
    for x in cover[:40]: o.write('COVER ' + x + '\n')
    o.write('\n== ISSUES (%d distinct)\n' % len(G))
    for key, occ in sorted(G.items(), key=lambda kv: (kv[0].split(' ')[0], -len(kv[1]))):
        sizes = sorted(set(s for _, s, _, _ in occ), key=lambda s: int(s.split('x')[0])); boards = sorted(set(b for b, _, _, _ in occ)); ts = sorted(set(t for _, _, t, _ in occ))
        o.write('%3d  %s\n      boards %s · sizes %s · text %s · e.g. %s\n' % (len(occ), key, ','.join(boards), ' '.join(sizes[:14]) + (' …' if len(sizes) > 14 else ''), '/'.join(ts), occ[0][3][-60:]))
    o.write('\n== NOTES (%d distinct)\n' % len(N))
    for key, occ in sorted(N.items(), key=lambda kv: (kv[0].split(' ')[0], -len(kv[1]))):
        sizes = sorted(set(s for _, s, _, _ in occ), key=lambda s: int(s.split('x')[0])); boards = sorted(set(b for b, _, _, _ in occ))
        o.write('%3d  %s  [%s] %s\n' % (len(occ), key, ','.join(boards)[:120], ' '.join(sizes[:10])))
print(open(out).read()[:200])
