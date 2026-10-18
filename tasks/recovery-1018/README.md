# Recovery check and GitHub sync — 18 Oct 2026

The owner moved to a second Claude account after the first one stopped while publishing v177. This session opened the
**original** design artifact through a share with edit rights (not a copy), checked it read-only, and then — on the owner's request
"check if something pending then fix and commit and push" — brought this repository up to the live design.
**Nothing on the website artifact, the spec page or Figma was changed.**

## What was found

| Check | Result |
|---|---|
| Live design | `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`, version id `1792315235-dd28` (saved 18 Oct 2026, 14:50 IST), 28 project files, 56 images |
| v177 | **Present.** "ધામની ભોજનશાળા બારેમાસ અવિરત" on the festival page (venue, programme band, notice), Contact FAQ and Darshan card, desktop and phone; festival meal times gone. The spec page (`1792315277-f9e1`, 14:51 IST) records v177 as published. |
| v153–v176 | Present — content of each spot-checked in the live files (YouTube link, history chapters, સંકલ્પ ૨૦૨૪, photos, ૨૭ નક્ષત્ર, ઊજવીએ, news, calendar to 13 Dec 2027, labels, timeline, stuti, night programme, venue rows). |
| Images | Every `/_blob/` id used by the pages exists in the asset store; 19 stored images are no longer used (replaced originals, kept for rollback). |
| GitHub before this sync | `main` at `6b4cfef` = v152 (17 Oct). 25 of 28 project files and 15 used images differed from live; docs stopped at v152. Nothing existed only on GitHub. |
| Layout | Live v177 vs v152 with `tools/check_layout.py`, all 24 boards, every width in `--widths auto`, normal + large text, clock 18 Oct 2026 16:30 IST: **216 runs, 0 new problems, no script errors** — [layout-check-v177-vs-v152.txt](layout-check-v177-vs-v152.txt). |
| Not verifiable | Exact v176 → v177 file diff (earlier versions' files cannot be read from here); which numeric version each intermediate id belongs to — only v177's id is known. |

## What this sync changed in the repository

- `design/project/` = live v177, byte-for-byte (all 28 files compared); `design/SHA256SUMS.txt` regenerated.
- `design/assets/`: 17 images added (15 used by the pages, 2 uploaded on 17 Oct but unused) → 56, every hash equal to the live asset store; `SHA256SUMS.txt` regenerated.
- `tasks/spec-page/`: page source = live spec page `1792315277-f9e1`, plus its 59 pictures that were missing here.
- `PAGE_CONTENT.md` regenerated for v177 (0 bracket placeholders).
- CHANGELOG, PROJECT_STATE, NEXT_SESSION, CLAUDE.md, DESIGN_SYSTEM, DEVELOPER_HANDOFF and TESTING brought up to v177, including the
  owner's v170/v173 decision on unknown details ("વિગત ટૂંક સમયમાં" or left out, instead of `[brackets]`).

## How it was checked

Fonts came from the fontsource GitHub repository (npm and font CDNs are blocked in this sandbox), served by `tools/serve.py` with the
live `dc-runtime.js`. Baseline = the v152 snapshot on port 8771, live v177 on 8772. Chromium only — Safari/iPhone, real devices and
screen readers remain untested, as before.
