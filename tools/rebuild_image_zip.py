#!/usr/bin/env python3
"""Rebuild the owner's 26-image ZIP with the ORIGINAL file names (<NN_name>__<blob-id>.<ext>) from design/assets/.
The Figma image script (figma/scripts/call5.js) matches dropped images by these names and pixel sizes.

usage: python3 tools/rebuild_image_zip.py design/assets figma/scripts/body5_images.js out.zip
"""
import json, os, re, sys, zipfile
assets, body5, out = sys.argv[1:4]
inv = json.loads(re.search(r'const INV = (\[.*?\]);', open(body5, encoding='utf-8').read(), re.S).group(1))
files = {f.split('.')[0]: f for f in os.listdir(assets)}
with zipfile.ZipFile(out, 'w', zipfile.ZIP_STORED) as z:
    for no, base, w, h in inv:
        bid = base.split('__')[1]; f = files[bid]
        z.write(os.path.join(assets, f), f'vihat-meldi-dham-images/{base}{os.path.splitext(f)[1]}')
print(out, len(inv), 'images')
