# TESTING.md

There is no build step: the pages are static `.dc.html` files rendered by the Claude Design runtime. Testing = rendering the pages in headless Chromium
(Playwright) and measuring them. All tools are in `tools/` and take their paths as arguments.

## One-time setup in a fresh session

Run from the repository root. `work/` and `base/` are git-ignored scratch folders.

```bash
pip install playwright pillow --break-system-packages                                        # usually already installed
npm install --prefix work @fontsource/noto-serif-gujarati @fontsource/hind-vadodara          # Gujarati fonts (Google Fonts is blocked in the sandbox)
mkdir -p work && cp -r design/project work/project                                           # FULL working copy (when live = design/ version)
```

Fetch the Design runtime once (Artifact tool): `action: read`, `url: https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`,
`path: "artifact-type/dc-runtime.js"` (default out folder) → use the saved path it prints as `--runtime`.
Images are in `design/assets/` (if one is ever missing: `Artifact read` with `path` = the 32-character blob id saves `<id>.<ext>`).

**Without the fonts, layout and text-fit results are not valid** (Gujarati falls back to another font with different widths).

## Serve baseline and edited copy

```bash
RT=<runtime path>; F=work/node_modules/@fontsource
python3 tools/serve.py --project design/project --assets design/assets --runtime $RT --fonts $F --port 8771 &   # baseline (base/project if live is newer)
python3 tools/serve.py --project work/project   --assets design/assets --runtime $RT --fonts $F --port 8772 &   # your edited copy
```

Pages: `http://127.0.0.1:8771/<Board>.dc.html`. The working copy must be complete (all 28 files), or the server returns 404 for missing CSS/pages.
Servers stop when the session's container restarts — just start them again.

## Focused checks (run these for every change)

| Check | Command | Pass when |
|---|---|---|
| Layout, both text sizes | `python3 tools/check_layout.py --base 8771 --new 8772 --boards <Touched,Boards>` | "0 with new problems" (exit 0) |
| Frame heights | `python3 tools/frame_heights.py --port 8772 --project work/project --boards <Touched,Boards>` | "frames to change: 0" — otherwise update root `height`, `data-props` height and `canvas.json` h (= min(frame, 8000)). MenuMobile/OfflineMobile are phone-screen boards (844) and are skipped. |
| Regression (only if `site.css` changed) | `python3 tools/pixel_regress.py --base 8771 --new 8772 --project work/project [--boards A,B]` | untouched boards "identical" |
| Wording | `python3 tools/gen_page_content.py design/project /tmp/before.md && python3 tools/gen_page_content.py work/project /tmp/after.md && diff /tmp/before.md /tmp/after.md` | only the intended strings changed |
| Snapshot integrity | `(cd design/project && sha256sum -c --quiet ../SHA256SUMS.txt) && (cd design/assets && sha256sum -c --quiet SHA256SUMS.txt)` | no output, exit 0 |

What `tools/fullcheck.js` flags: page wider than the viewport, elements past the screen edge (outside scroll areas), clipped text horizontally/vertically,
distorted images, button labels breaking inside the button, a ૨૦૨૭ year split from its month. It compares edited vs baseline, so pre-existing items are not reported as new.

Viewports used by `check_layout.py --widths auto`: desktop boards 1440 · 1280 · 1100 · 1024 · 900 · 834 · 768; phone boards 430 · 390 · 360 · 320;
tablet/landscape home boards at their own width (834 · 1180 · 844). Each in normal and large (અ+) text.

Time-dependent content (countdown, darshan open/closed card, calendar "ચાલુ છે", "આજે" marker): pages read the clock. Use `clock_script(iso, frozen=True)` from
`tools/_common.py` as an init script; frame heights use the five daily times in `DAILY_TIMES` (04:40, 06:30, 12:30, 19:30, 22:30 IST).

## Before/after pictures for the owner

Screenshot just the changed section on both servers (Playwright `locator(<section selector>).screenshot()`), at desktop 1440, tablet 834 and phone 390/320,
hide the phone action bar (`.vx-abar{display:none}`) so it does not cover content, and put them side by side with Pillow. Send with SendUserFile.

## Known limitations of the checks

- The home boards' moving text ribbon (`.vx-marquee`) and the darshan photo area can differ by a few pixels between two loads of the **same** version.
  Treat a difference there as noise only after confirming it with the same version on both ports.
- Canvas boards are capped at 8000 px; frames are sized for ordinary days (festival-week states can be taller — canvas only).
- These are render checks in Chromium only; no Safari/Firefox, no real devices, no screen-reader run.
- Figma is not checked here (Gate A needs Figma screenshots; see `figma/state.json`).

## Last verified results

10 Oct 2026, design v106:


- Handover check: all 28 project files of live v106 byte-identical to `design/project/` (`design/SHA256SUMS.txt`); 26 images match the artifact's asset checksums
  (`design/assets/SHA256SUMS.txt`); `tools/rebuild_image_zip.py` rebuilds the owner's original 26-image ZIP byte-for-byte.
- Tools validated on the v106 snapshot: `frame_heights.py` (Darshan, HomeMobile, NewTemple, Seva: 0 changes; MenuMobile/OfflineMobile skipped), `check_layout.py` (Darshan 1440/390, NewTempleMobile 1440/390:
  8 runs, 0 problems), `pixel_regress.py` (4 boards identical); all Python tools and the 15 Figma scripts parse.
- Per-version results: see [CHANGELOG.md](CHANGELOG.md). Most recent full regression: v106 (all 24 boards).
