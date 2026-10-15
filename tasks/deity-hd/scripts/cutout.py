"""Cut a figure out of its background with IS-Net (isnet-general-use.onnx, as used by rembg) on onnxruntime.
usage: python3 cutout.py MODEL.onnx IN.png OUT_RGBA.png  -> RGBA with the soft mask as alpha; also writes OUT_mask.png"""
import sys
import numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
mp, ip, op = sys.argv[1:4]
im = Image.open(ip).convert('RGB')
x = np.asarray(im.resize((1024, 1024), Image.LANCZOS), dtype=np.float32) / 255.0
x = ((x - 0.5) / 1.0).transpose(2, 0, 1)[None]
s = ort.InferenceSession(mp, providers=['CPUExecutionProvider'])
pred = s.run(None, {s.get_inputs()[0].name: x})[0][0, 0]
pred = (pred - pred.min()) / (pred.max() - pred.min())
m = Image.fromarray((pred * 255).astype(np.uint8)).resize(im.size, Image.LANCZOS)
# make the mask decisive: faint leftovers (< 60) go, near-solid areas (> 180) become solid, a smooth step in between keeps soft edges
a = np.asarray(m, dtype=np.float32); t = np.clip((a - 60) / 120, 0, 1); a = t * t * (3 - 2 * t) * 255
m = Image.fromarray(a.astype(np.uint8))
m.save(op[:-4] + '_mask.png')
out = im.convert('RGBA'); out.putalpha(m); out.save(op); print(op, im.size)
