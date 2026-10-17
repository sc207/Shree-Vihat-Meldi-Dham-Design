# UI / UX / responsive check of v147 and fixes v149–v152 (16–17 Oct 2026)

**Owner:** "check now if any bug related to design, ux ui and responsiveness issue then fix it for all device like laptop, tablet, mobile".
The request handed the decision over (CLAUDE.md rule 3), so each fix was published as its own version. v148 in the artifact history is a
Design-type re-save (new type release) with no content change: every page read back byte-identical to v147.

## What was checked (Chromium, on live v147)

- **Device scan** `tasks/responsive-v116/scripts/scan_run.py` on every board at 34 sizes (phones 320–760, phones sideways, tablets 744–1366
  both ways, laptops 1024–1536, monitors 1680–2560), normal and large text: **930 renders**, plus 90 for desktop pages on sideways phones.
  Result: no sideways scrolling, no script errors, no fixed bar covering content, **no new problem** since v123 (the remaining "issues" are
  the known false alarms: date medallion font boxes, Darshan week strip, the festival day carousel). The soft-image notes of v123 are gone
  (v125–v128, v146–v147). Grouped results: `results/scan147_grouped.txt`, `results/scan147_landscape_grouped.txt`.
- **By eye:** full-page sheets of every page at 390 / 768 / 1024 / 1440 and the three home boards, first screens on laptops and monitors
  (1280 → 2560), close-ups of everything changed since v123.
- **New checks the scan does not do:**
  - `scripts/cap_contrast.py` — contrast of text written over photos (background measured under each caption line with the text hidden);
  - `scripts/narrow.py` — text squeezed into narrow columns (real line count per block) at 320, 768 and 1024 px.

## Found and fixed (one version each, CSS only)

| Version | Problem | Fix | Pictures |
|---|---|---|---|
| **v149** | Home "ફોટો ગેલેરી": the names on the five photos (white text) sat on a pale grey band — **1.9–2.8 : 1** on every Home board; on phones the two-line "ભગવાન શ્રી / કરમશીબાપા" sat on his white clothes | deeper band (same height on one-line names) + soft text shadow → **4.5–7.8 : 1** everywhere | [390](pictures/v149_home_photo_names_390.png) · [1440](pictures/v149_home_photo_names_1440.png) |
| **v150** | Home banner date box at 320 px: "૮ ફેબ્રુ., સોમવાર" ran over the right border (3 px) | below 340 px: dates 18 → 16 px, side padding 14 → 10 px | [320](pictures/v150_home_dates_320.png) |
| **v151** | New Temple "દર્શનનો માર્ગ" cards on small phones: text column **96 px** at 320 px — 6 lines of one or two words, "·" and "×" starting lines | ≤ 400 px: picture 120 → 88 px, card padding/gap 16 px → text column **152 px** (360: 192, 390: 222); "સ્થાપત્ય ચિત્ર" label still inside the picture; NewTempleMobile frame 11812 → 11659 | [320](pictures/v151_route_cards_320.png) |
| **v152** | New Temple "નિર્માણ સ્થળની તાજી તસવીરો" on tablets 761–999 px: the three small update cards kept the laptop thumbnail (148 px), leaving **75–130 px** for date and text | the phone's compact card (104 px thumbnail) → text **130–222 px**; laptops and phones unchanged | [768](pictures/v152_construction_list_768.png) |

Script: `tools/examples/apply_v149_v152_ux.py <project> <part 1..4>` (part 2 also corrects the comment label of part 1, which went live
saying "v148").

## Looked at and left as they are

- Stacked dates (day / month / weekday on separate lines) in the festival cards, the 2 × 2 stats on Home, Seva choice cards at 1024 px,
  the placeholder beside સુરેશબાપા's small portrait (History ch. 4): narrow by design and readable.
- The festival PDF button has an empty link — hidden on purpose until the trust supplies the PDF.

## Tests

- Each stage against the previous one: `check_layout.py` on the touched boards (28 + 22 + 22 + 22 runs, 0 new problems); `pixel_regress.py`
  on all 24 boards: v149 only the photo strip on the 5 Home boards; v150 and v152 nothing at the boards' own widths (their rules start
  below 340 px / between 761 and 999 px); v151 only NewTempleMobile (shorter). MenuMobile differs run to run on the same server (noise).
- Measurements before/after: caption contrast (all Home boards); date box overrun 3 → 0 px at 320, 0 at 340–390 (normal + large text);
  route cards 320–430 px (picture, text width, label inside); construction list 760–1024 px.
- Frames: NewTempleMobile 11812 → 11659 (`frame_heights.py`: 0 to change after); canvas "h" stays 8000.
- Re-scan of the touched boards on v152: see `results/scan152_grouped.txt`.
- Live read-back after v152: all changed files byte-identical; `design/project/` = v152.
