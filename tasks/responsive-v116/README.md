# Responsive / UI-UX check of v116 and fixes v118–v123 (15–16 Oct 2026)

Owner's request: "check design if you found any responsiveness issue in any device screen or any design, ux ui related issues fix it
and make website design easy to go for coding part".

## What was checked (Chromium)
- `scripts/scan_run.py` + `scripts/scan.js`: every content board on 34 device sizes — phones 320–760 portrait, phones sideways
  568×320 … 932×430, tablets 744–1366 both ways, laptops 1024–1536, monitors 1680–2560 — normal and large text: **930 renders**
  (+90 for desktop pages on sideways phones). Checks: sideways scrolling, elements past the edge, clipped text, text spilling out of
  its box, text-on-text overlap, distorted images, image sharpness on 2× screens, text below 12 px, contrast on solid grounds,
  touch-target size, fixed bars covering content, long lines. Grouped results: `results/scan_v116_grouped.txt`,
  `results/scan_v116_landscape_grouped.txt`; after the fixes: `results/scan_final_grouped.txt`.
- By eye: full-page sheets of every page at 390 / 768 / 1024 / 1440 (`scripts/shots_full.py`), first screens on sideways phones,
  laptops and wide monitors (`scripts/first_screens.py`), close-ups (`scripts/viewport_shot.py`).
- Result for v116: no sideways scrolling and no script errors anywhere. Six real problems, below. Not problems (checked): the date
  medallion and Darshan week strip "overlaps" (font boxes), the festival day carousel (scrolls on purpose), closed FAQ answers.

## Found and fixed (one version each; v117 in the history is a Design-type re-save without content change)
| Version | Problem | Fix | Files |
|---|---|---|---|
| v118 | Phone Home: leftover WhatsApp "જોડાઓ" button pinned over the દર્શન section (recorded as removed earlier) | removed | HomeMobile |
| v119 | History index at 320 px: "આધ્યાત્મિક" ran into "માતાજી અને ધામ પરિવાર" | label under the title below 375 px | site.css |
| v120 | Phones sideways 568–640 px: "મહોત્સવ વિશે જાણો →" cut; darshan time ran out of its card | buttons size to label and wrap; times wrap (balanced) | site.css |
| v121 | Festival chart on phones: "રામ કથા", "રમેલ" at 11 px | 13 px | site.css |
| v122 | WhatsApp band at 1000–1279 px: heading broke word by word / orphan "જોડાઓ" | smaller badge, tighter gaps; balanced heading lines | site.css, HomeTabletL frame 8192→8104 |
| v123 | Phones/touch screens: 156 small targets 25–40 px tall | invisible ::after touch areas ≥ 44 px, no visual change | site.css |

## Verification of the final copy (= live v123)
Device scan 930 renders: every targeted problem gone, nothing new (one count-up animation false alarm checked by eye). Pixel compare
of 24 boards with v116: differences only at the removed button (HomeMobile), the chart labels (PranPratishthaMobile) and the shorter
band (HomeTabletL). Touch areas: `scripts/test_tap_areas.py` — 156/156 targets reach 44 px at 390 and 320 px (v116: 0/156).
Frames: 0 to change after the HomeTabletL update. Wording: only the removed button label "જોડાઓ". Live read-back: 28/28 files identical.
First attempt at v123 (padding + negative margin) shortened phone footers by 70 px — caught by the pixel compare and rebuilt with ::after.

Pictures: `pictures/found_*.jpg` (problems as found) and `pictures/v118_…jpg` … `v122_…jpg` (before/after per version; v123 has no visual change).
Script: `tools/examples/apply_v118_v123_responsive.py <project> <part 1..6>`.

Coding hand-off produced in the same task: [DEVELOPER_HANDOFF.md](../../DEVELOPER_HANDOFF.md), `handoff/assets.json`, `tools/export_assets.py`.
