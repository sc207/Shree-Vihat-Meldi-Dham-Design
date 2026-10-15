#!/usr/bin/env python3
"""Developer hand-off: image manifest + export with readable names.
Reads the image inventory table in DESIGN_SYSTEM.md (original names, blob ids), scans the design pages for where each image is
used and with which alt text, writes handoff/assets.json, and (with --export DIR) copies design/assets/<blob>.<ext> to
DIR/<original name>.<ext>.
usage (repo root): python3 tools/export_assets.py [--export work/export/images]"""
import glob, json, os, re, shutil, sys
from PIL import Image
inv = re.findall(r'^\| (\d\d) \| `([^`]+)` \| `([0-9a-f]{32})` \| (\d+)×(\d+) \| ([^|]+)\|', open('DESIGN_SYSTEM.md', encoding='utf-8').read(), re.M)
pages = {os.path.basename(f)[:-8]: open(f, encoding='utf-8').read() for f in glob.glob('design/project/*.dc.html')}
files = {f.split('.')[0]: f for f in os.listdir('design/assets') if not f.endswith('.txt')}
out = []
for no, name, bid, w, h, used in inv:
    f = files[bid]; path = os.path.join('design/assets', f); im = Image.open(path)
    assert (im.width, im.height) == (int(w), int(h)), (name, im.size)
    where = sorted(b for b, s in pages.items() if '/_blob/' + bid in s)
    alts = set()
    for s in pages.values():
        for m in re.finditer(r'<img[^>]*src="/_blob/%s"[^>]*>' % bid, s):
            a = re.search(r'alt="([^"]*)"', m.group(0)); alts.add(a.group(1) if a else '(no alt)')
    out.append({'no': int(no), 'name': name + os.path.splitext(f)[1], 'blob': bid, 'design_url': '/_blob/' + bid, 'width': int(w), 'height': int(h),
                'bytes': os.path.getsize(path), 'type': Image.MIME.get(im.format), 'used_on_boards': where,
                'alt_texts': sorted(alts) if alts else (['(no <img> tag: listed in the page logic, e.g. the gallery data, with its caption)'] if where else []),
                'note': used.strip()})
os.makedirs('handoff', exist_ok=True)
json.dump({'source': 'design/assets (copy of the Claude Design artifact image store); pages refer to /_blob/<blob>',
           'decorative_if_alt_empty': 'alt="" means decorative (or the text beside it names the picture)', 'images': out},
          open('handoff/assets.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('handoff/assets.json:', len(out), 'images,', sum(1 for x in out if x['used_on_boards']), 'used on the site')
if '--export' in sys.argv:
    d = sys.argv[sys.argv.index('--export') + 1]; os.makedirs(d, exist_ok=True)
    for x in out: shutil.copyfile(os.path.join('design/assets', files[x['blob']]), os.path.join(d, x['name']))
    print('exported to', d)
