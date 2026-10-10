#!/usr/bin/env python3
"""Serve a copy of the design's project folder so the pages render in a normal browser (Playwright).

usage: python3 tools/serve.py --project design/project --assets design/assets \
                              --runtime <dc-runtime.js> [--fonts <node_modules/@fontsource>] --port 8771

  --project  folder with the *.dc.html pages, site.css, ds/… (a copy you edit, or design/project for the baseline)
  --assets   folder with the 26 images named <blob-id>.<ext>  (pages ask for /_blob/<blob-id>)
  --runtime  the Design type's runtime script; pages load it as ./support.js
             (get it once per session: Artifact read, url = the website artifact, path = "artifact-type/dc-runtime.js")
  --fonts    optional: @fontsource packages so Gujarati renders offline
             (npm install @fontsource/noto-serif-gujarati @fontsource/hind-vadodara). Without it the
             Google Fonts link in each page is blocked in the sandbox and Gujarati falls back to system fonts —
             fine for logic checks, NOT for layout or text-fit checks.
Run one server per version you want to compare (e.g. baseline on 8771, your edited copy on 8772).
"""
import argparse, glob, http.server, mimetypes, os

ap = argparse.ArgumentParser()
ap.add_argument('--project', required=True); ap.add_argument('--assets', required=True); ap.add_argument('--runtime', required=True)
ap.add_argument('--fonts'); ap.add_argument('--port', type=int, default=8771)
A = ap.parse_args()
PROJ, ASSETS, RUNTIME, FONTS = (os.path.abspath(p) if p else None for p in (A.project, A.assets, A.runtime, A.fonts))


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        p = self.path.split('?')[0]
        if p.startswith('/_blob/'):
            m = glob.glob(os.path.join(ASSETS, p[7:] + '.*')); f = m[0] if m else None
        elif p == '/support.js':
            f = RUNTIME
        elif p == '/fonts.css':
            css = ''
            if FONTS:
                for fam, pk in (('Noto Serif Gujarati', 'noto-serif-gujarati'), ('Hind Vadodara', 'hind-vadodara')):
                    for w in (400, 500, 600, 700):
                        for sub in ('gujarati', 'latin'):
                            rng = 'unicode-range:U+0A80-0AFF,U+0964-0965,U+200C-200D,U+20B9,U+25CC,U+A830-A839;' if sub == 'gujarati' else ''
                            css += '@font-face{font-family:"%s";font-weight:%d;src:url("/font/%s/files/%s-%s-%d-normal.woff2") format("woff2");%s}\n' % (fam, w, pk, pk, sub, w, rng)
            self.send_response(200); self.send_header('Content-Type', 'text/css'); self.end_headers(); self.wfile.write(css.encode()); return
        elif p.startswith('/font/') and FONTS:
            f = os.path.join(FONTS, p[6:])
        else:
            f = os.path.join(PROJ, p.lstrip('/'))
        if not f or not os.path.isfile(f):
            self.send_response(404); self.end_headers(); return
        d = open(f, 'rb').read()
        if f.endswith('.dc.html'):  # add the local font faces after the site stylesheet
            d = d.replace(b'<link rel="stylesheet" href="./site.css">', b'<link rel="stylesheet" href="./site.css"><link rel="stylesheet" href="/fonts.css">')
        self.send_response(200); self.send_header('Content-Type', mimetypes.guess_type(f)[0] or 'application/octet-stream'); self.end_headers(); self.wfile.write(d)


print(f'serving {PROJ} on http://127.0.0.1:{A.port}/  (e.g. /Main.dc.html)', flush=True)
http.server.ThreadingHTTPServer(('127.0.0.1', A.port), H).serve_forever()
