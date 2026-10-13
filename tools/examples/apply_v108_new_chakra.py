# Replace the old chakra drawing (oval-petal mandala, md5 36da477b) with the new lotus mandala used by the banners,
# the closing devotional band and the photo slots. Only the drawing inside <svg> changes: each ornament keeps its class,
# inline size/position, colour and opacity. Exact-string replacement, asserted per file.
import re, sys, glob, hashlib, os
root = sys.argv[1] if len(sys.argv) > 1 else 'work/project'
OLD_CLASSES = ('vm-mandala', 'vm-cta__orn')
changed = []
for f in sorted(glob.glob(os.path.join(root, '*.dc.html'))):
    s = open(f, encoding='utf-8').read()
    new = re.search(r'<svg class="vm-hero__mandala"[^>]*>(.*?)</svg>', s, re.S)
    n = 0
    for cls in OLD_CLASSES:
        for m in list(re.finditer(r'(<svg class="%s"[^>]*>)(.*?)(</svg>)' % re.escape(cls), s, re.S)):
            body = m.group(2)
            assert hashlib.md5(body.encode()).hexdigest()[:8] == '36da477b', (f, cls, 'unexpected drawing')
            assert 'viewBox="-200 -200 400 400"' in m.group(1), (f, cls, 'viewBox differs')
            assert new is not None, (f, 'no new mandala in this file to copy from')
            assert s.count(m.group(0)) == 1, (f, cls, 'not unique')
            s = s.replace(m.group(0), m.group(1) + new.group(1) + m.group(3)); n += 1
    if n:
        open(f, 'w', encoding='utf-8').write(s); changed.append((os.path.basename(f), n))
print(changed)
assert sum(n for _, n in changed) == 9, 'expected 9 old chakras'
