"""Real-ESRGAN x4 without PyTorch: read the official .pth weights (zip + pickle) with a tiny unpickler, build the same network as an
ONNX graph (SRVGGNetCompact for realesr-general-x4v3, RRDBNet for RealESRGAN_x4plus / _anime_6B) and run it with onnxruntime, in tiles.
usage: python3 sr_onnx.py MODEL.pth IN.png OUT.png [--tile 160] [--pad 16]
Output = 4x the input, RGB (alpha, if any, is upscaled separately with Lanczos)."""
import io, pickle, sys, zipfile
import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper
import onnxruntime as ort
from PIL import Image


def load_pth(path):
    z = zipfile.ZipFile(path); root = z.namelist()[0].split('/')[0]
    DT = {'FloatStorage': np.float32, 'HalfStorage': np.float16, 'DoubleStorage': np.float64, 'LongStorage': np.int64}

    def rebuild(storage, offset, size, stride, *a):
        dt, key = storage
        buf = np.frombuffer(z.read(f'{root}/data/{key}'), dtype=dt)
        n = int(np.prod(size)) if len(size) else 1
        arr = buf[offset:offset + n] if all(True for _ in [0]) else buf
        if len(size) and tuple(stride) != tuple(int(np.prod(size[i + 1:])) for i in range(len(size))):
            arr = np.lib.stride_tricks.as_strided(buf[offset:], shape=size, strides=[s * buf.itemsize for s in stride])
        return np.array(arr, dtype=np.float32).reshape(size)

    class U(pickle.Unpickler):
        def find_class(self, mod, name):
            if mod == 'torch._utils' and name == '_rebuild_tensor_v2': return rebuild
            if mod == 'torch' and name.endswith('Storage'): return name
            if mod == 'collections' and name == 'OrderedDict':
                import collections; return collections.OrderedDict
            if mod == 'torch._utils' and name == '_rebuild_parameter': return lambda d, *a: d
            return super().find_class(mod, name)

        def persistent_load(self, pid):
            _, stype, key, loc, numel = pid
            return (DT[stype if isinstance(stype, str) else stype.__name__], key)
    sd = U(io.BytesIO(z.read(f'{root}/data.pkl'))).load()
    for k in ('params_ema', 'params'):
        if k in sd: return sd[k]
    return sd


class G:
    def __init__(self): self.nodes, self.inits, self.n = [], [], 0
    def name(self, p): self.n += 1; return f'{p}{self.n}'
    def const(self, arr, p='c'):
        nm = self.name(p); self.inits.append(numpy_helper.from_array(np.asarray(arr, dtype=np.float32), nm)); return nm
    def op(self, t, ins, **kw):
        o = self.name(t); self.nodes.append(helper.make_node(t, ins, [o], **kw)); return o
    def conv(self, x, sd, k):
        return self.op('Conv', [x, self.const(sd[k + '.weight']), self.const(sd[k + '.bias'])], pads=[1, 1, 1, 1], kernel_shape=[3, 3])
    def lrelu(self, x): return self.op('LeakyRelu', [x], alpha=0.2)


def build(sd):
    g = G()
    if any(k.startswith('body.0.') for k in sd) and 'conv_first.weight' not in sd:      # SRVGGNetCompact
        idx = sorted({int(k.split('.')[1]) for k in sd if k.startswith('body.')})
        x = 'input'
        for i in idx:
            w = sd[f'body.{i}.weight']
            if w.ndim == 4: x = g.op('Conv', [x, g.const(w), g.const(sd[f'body.{i}.bias'])], pads=[1, 1, 1, 1], kernel_shape=[3, 3])
            else: x = g.op('PRelu', [x, g.const(w.reshape(-1, 1, 1))])
        up = g.op('DepthToSpace', [x], blocksize=4, mode='CRD')
        base = g.op('Resize', ['input', '', g.const([1, 1, 4, 4])], mode='nearest')
        out = g.op('Add', [up, base])
    else:                                                                                   # RRDBNet
        nb = len({k.split('.')[1] for k in sd if k.startswith('body.')})
        feat = g.conv('input', sd, 'conv_first'); x = feat
        for b in range(nb):
            inp = x
            for r in (1, 2, 3):
                p = f'body.{b}.rdb{r}'; xs = [x]
                for c in range(1, 5):
                    cat = xs[0] if len(xs) == 1 else g.op('Concat', xs, axis=1)
                    xs.append(g.lrelu(g.conv(cat, sd, f'{p}.conv{c}')))
                x5 = g.conv(g.op('Concat', xs, axis=1), sd, f'{p}.conv5')
                x = g.op('Add', [g.op('Mul', [x5, g.const(0.2)]), x])
            x = g.op('Add', [g.op('Mul', [x, g.const(0.2)]), inp])
        feat = g.op('Add', [feat, g.conv(x, sd, 'conv_body')])
        for u in ('conv_up1', 'conv_up2'):
            feat = g.lrelu(g.conv(g.op('Resize', [feat, '', g.const([1, 1, 2, 2])], mode='nearest'), sd, u))
        out = g.conv(g.lrelu(g.conv(feat, sd, 'conv_hr')), sd, 'conv_last')
    gr = helper.make_graph(g.nodes, 'sr', [helper.make_tensor_value_info('input', TensorProto.FLOAT, [1, 3, None, None])],
                           [helper.make_tensor_value_info(out, TensorProto.FLOAT, [1, 3, None, None])], g.inits)
    m = helper.make_model(gr, opset_imports=[helper.make_opsetid('', 17)]); m.ir_version = 8
    return m


def run(model_path, img, tile=160, pad=16):
    m = build(load_pth(model_path))
    so = ort.SessionOptions(); so.intra_op_num_threads = 2
    s = ort.InferenceSession(m.SerializeToString(), so, providers=['CPUExecutionProvider'])
    a = np.asarray(img.convert('RGB'), dtype=np.float32) / 255.0
    H, W, _ = a.shape; out = np.zeros((H * 4, W * 4, 3), np.float32)
    for y0 in range(0, H, tile):
        for x0 in range(0, W, tile):
            y1, x1 = min(H, y0 + tile), min(W, x0 + tile)
            ya, xa, yb, xb = max(0, y0 - pad), max(0, x0 - pad), min(H, y1 + pad), min(W, x1 + pad)
            t = a[ya:yb, xa:xb].transpose(2, 0, 1)[None]
            r = s.run(None, {'input': t})[0][0].transpose(1, 2, 0)
            out[y0 * 4:y1 * 4, x0 * 4:x1 * 4] = r[(y0 - ya) * 4:(y0 - ya) * 4 + (y1 - y0) * 4, (x0 - xa) * 4:(x0 - xa) * 4 + (x1 - x0) * 4]
    return Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8))


if __name__ == '__main__':
    mp, ip, op = sys.argv[1:4]
    tile = int(sys.argv[sys.argv.index('--tile') + 1]) if '--tile' in sys.argv else 160
    im = Image.open(ip); res = run(mp, im, tile=tile)
    if im.mode == 'RGBA':
        res = res.convert('RGBA'); res.putalpha(im.getchannel('A').resize(res.size, Image.LANCZOS))
    res.save(op); print(op, res.size)
