# Items 1–6 — consolidated report (working copy, not committed, not published)

14 Oct 2026 · Final copy: `project/` here (= live v109 + items 1–6; checksums `project-SHA256SUMS.txt`). Per-item stylesheet patches in `patches/`,
page-file changes by `scripts/apply_item*.py`; rebuilding from v109 with them reproduces `project/` exactly (checked). Saved to the repo on the owner's
"commit and save it" (14 Oct 2026, 03:21 IST); **not published**.
Live design is still **v109 `1791922103-42cb`**. Nothing was published; Figma untouched.

## 1. Baseline verification

- Repository `sc207/Shree-Vihat-Meldi-Dham-Design`, branch `main`, HEAD `34cca8b` (the Seva-evidence commit made just after `668bb3a`,
  before this run), clean working tree, in sync with GitHub.
- Live design id `1791922103-42cb` = v109; `design/project` (28 files) and `design/assets` (26 images) checksums OK.
- Seva working copy = v109 + 3 rules at the end of `site.css` (identical to the saved diff `tasks/seva-fix/seva_on_v109.diff`).

## 2. Status of the six items

| Item | Status |
|---|---|
| 1 Seva desktop right column | Fixed and verified (Chromium) |
| 2 Tablet / small-laptop menu, 761–1179 px | Fixed and verified (Chromium) |
| 3 Seva form errors (+ confirmation out of view) | Fixed and verified (Chromium); screen-reader output not tested |
| 4 Phone menu ✕ and closing | Fixed and verified in a normal browser; behaviour inside the Claude Design canvas not verifiable (falls back to Home) |
| 5 Home buttons on very small phones | Fixed and verified (Chromium) |
| 6 Polish 6.1–6.5 | Fixed and verified (Chromium); optional C7, C8, C9 deliberately not changed (see 8) |

## 3. Root causes and fixes

1. **Seva column.** Form ~2,100 px, help column ~1,000 px, and the section's `overflow: hidden` stops a sticky card. Fix (≥1000 px only): column
   stretches, last card "સહાયની જરૂર છે?" sticky under the compact header, section `overflow: clip`. 3 CSS rules.
2. **Tablet menu.** Below 1180 px the design system hides the header links and shows ☰; on the 12 desktop/tablet boards ☰ was a `<button>` with no
   action or panel. Fix: ☰ opens the design system's own menu panel (`.vm-mnav`, as on the phone menu page) with the board's 8 header links (current
   page marked), brand, text-size button, WhatsApp and phone. `role="dialog"`, `aria-modal`, `aria-expanded`/`aria-controls` on ☰, ✕ is a button,
   Escape closes, Tab stays inside, focus to ✕ on open and back to ☰ on close; above the phone bottom bar (z-index 90); one centred column ≤720 px;
   hidden from 1180 px.
3. **Seva form.** Messages were already under each field, but on a failed submit nothing moved: focus stayed on the button, and on a phone the
   summary and most messages were ~3,000 px above. Fields had no `aria-invalid` and no link to their message. Fix: on failure, scroll to the first
   invalid control (form order) and focus it; `aria-invalid` + `aria-describedby` on name, mobile, town, consent. Found during testing: after a
   valid submit the confirmation (which replaces the form) was 750–2,800 px above the screen — the page now moves to it and focuses its heading.
   Typed values kept; no wording change.
4. **Phone menu.** ✕ was maroon on maroon (1.41:1): the general link colour `.vm-root a` outranked the design system's ivory. ✕ and the
   current-page mark were fixed to Home. Fix: ivory ✕ (14.3:1); ✕ and Escape go back to the page the visitor came from (Home when opened directly,
   via the existing link); current-page mark follows that page. Because the browser's own scroll restoration raced with the page drawing itself,
   the 9 phone pages now remember their scroll position when ☰ is tapped and restore it on return (10-minute limit).
5. **Home buttons.** Equal-width buttons (`flex: 1 1 0`, no wrapping, overflow hidden): "મહોત્સવ વિશે જાણો →" (148 px) did not fit 139–149 px.
   Fix (<375 px only): each button sizes to its label and shares the rest; never narrower than its label (wraps instead of clipping).
6. **Polish.** 6.1 day tiles share one row at 1000–1179 px (7 equal columns). 6.2 night cards: date above the names below 360 px (below 390 px in
   large text). 6.3 `scroll-margin-top` 96 / 64 px on `#calendar`, `#travel`, `#progress`, matching every other jump link. 6.4 footer column titles
   h4 → h2 and Seva side-card titles h3 → h2, with rules reproducing their exact look. 6.5 consent checkbox 22 → 24 px.

## 4. Pictures (before / after)

`pictures/`: 1_seva_1440, 1_seva_1024, 2_menu_768, 2_menu_1024, 2_menu_phone_landscape, 3_form_errors_390, 3_form_errors_1440,
3_form_success_390, 4_phone_menu_close, 5_home_buttons, 6_1_seva_days_1024, 6_2_names_320_large, 6_3_jump_link, 6_5_checkbox.

## 5. Files changed (final copy vs v109)

23 page files + `site.css` (7 appended, commented blocks + one item-3 block; no existing rule edited):
- Item 1: `site.css`.
- Item 2: Main, HomeTablet, HomeTabletL, HomePhoneL, NewTemple, PranPratishtha, Seva, Gallery, History, Contact, Darshan, NotFound (`.dc.html`), `site.css`.
- Item 3: Seva, SevaMobile, `site.css`.
- Item 4: MenuMobile + HomeMobile, ContactMobile, DarshanMobile, GalleryMobile, HistoryMobile, NewTempleMobile, NotFoundMobile, PranPratishthaMobile,
  SevaMobile (scroll memory), `site.css`.
- Item 5: `site.css`. Items 6.1, 6.2, 6.3, 6.5: `site.css`. Item 6.4: 21 page files (heading tags) + `site.css`.
- Unchanged: OfflineMobile, `canvas.json`, design-system `bundle.css` and `tokens.json`, images.

## 6. Tests performed (Chromium / Playwright) and results

- Item 1: 24 / 25–26 scroll positions at 1440 / 1024: no overlap, 64 px gap, stays in column, stops 96 px above the footer; empty-column
  positions 6–7 → 0 at 1024/1100/1280/1440 (re-run on the final copy: same).
- Item 2: 81 runs — 9 pages × 760, 761, 800, 900, 1024, 1100, 1179, 1180 + HomeTablet 834, HomeTabletL 1112/1180, HomePhoneL 844×390/932×430 + 4 large-text
  runs: open, covers screen, nothing on top, aria-expanded, focus to ✕, 8 correct links + current mark, no sideways overflow, Tab stays inside, focus
  ring, Escape closes + focus back, ✕ closes, reopen, link navigates; at 1180 ☰ hidden and header links shown. 0 problems (also on the final copy).
  With the menu closed all 24 boards pixel-identical to the previous stage.
- Item 3: 7 scenarios × 1440, 1024, 390, 320 + 390 large = 35 runs (empty, several missing, 9-digit mobile, only consent missing, no seva chosen,
  keyboard submit, valid): focus lands on the right control, on screen above the bottom bar, values kept, aria-invalid correct; valid → confirmation
  on screen. 35/35 (before: focus stayed on the button in all error cases; confirmation off screen on phones). Reduced motion: instant jump.
- Item 4: 320, 360, 390, 430, 844×390: ✕ contrast 14.32:1, 48×48 target, focus ring; direct open → Home marked, ✕ → Home; from Darshan scrolled to
  1,400 px → Darshan marked, ✕ → back to Darshan at 1,400 px; reopen + Escape → back; other link → that page. All pass (also on the final copy).
- Item 5: 320–390 px in 5 px steps around the threshold, normal + large: one row, label 14–24 px from the button edge, 52 px tall (before: −5 to 5 px).
- Item 6: names wrapped 0/9 at 320–700 px both sizes (before: up to 9/9); day tiles one row at 1000–1179, unchanged elsewhere; jump links land at
  96 / 64 px (New Temple 99 / 67); no heading-level skip on any of the 24 boards; heading change pixel-identical on all 24 boards (normal) and spot
  checks in large text; checkbox 24×24.
- Consolidated, final copy vs v109: check_layout 212 runs (22 content boards, all their widths, normal + large) — 0 new problems; pixel compare
  24 boards — 21 identical, differences only on Seva, SevaMobile, MenuMobile (expected); frame heights — 0 to change; wording — nothing changed or
  removed, the only additions are the tablet menu's existing labels.

## 7. Regressions found during the run and how they were resolved

- Item 4: the browser's own scroll restoration after "back" was inconsistent (same width sometimes top, sometimes kept) → explicit scroll memory.
- Item 5: 360 px was not clipped but cramped (5 px) → threshold raised from 360 to 375 px.
- Item 3: confirmation out of view after a valid submit (found by the test) → moves to the confirmation.
- Pixel noise on MenuMobile appeared once; same box when v109 is compared with itself → noise, not a regression.

## 8. Not changed / unresolved / unverified

- Not changed on purpose: C7 banner entrance 900 ms (taste, not a defect), C8 image width/height attributes (many images, layout risk, load shift
  already low), C9 empty right half on text-only banners (approved design). C1 larger gallery photos: needs the trust. D1 (whole temple in the first
  phone screen): owner's decision, outside items 1–6.
- Not verified: Safari / WebKit (sticky inside `overflow: clip` needs Safari 16+), Firefox, real phones and tablets, screen readers, and behaviour inside
  the Claude Design canvas (the canvas does not scroll boards; whether boards there create browser history for "back" is unknown — ✕ then goes Home).

## 9. Browser and device limits

All tests ran in Chromium (Playwright) with local fonts; no Safari, Firefox, physical devices or assistive technology.

## 10. Confirmation

Live design remains v109 `1791922103-42cb`. Nothing was published or deployed; Figma untouched. Saved to the repository on the owner's instruction;
publishing needs a separate permission. To publish later: copy `project/` to `work/project`, then follow NEXT_SESSION.md §8 step 5 with the changed files
(REPORT §5), one version per item if the owner wants them separate.
