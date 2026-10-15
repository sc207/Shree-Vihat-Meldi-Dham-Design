# CHANGELOG.md

Published versions of the website design artifact `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`.
Each entry: version · version id · files · reason · tests run (with their actual results). All dates 10 Oct 2026 unless noted.
History before v97 (the original build, 30 Sep – 9 Oct 2026) lives in the artifact's version history and is not reconstructed here.

Standard verification after every publish below: the changed files were read back from the live artifact and compared byte-for-byte with what was sent (all matched).

_v118–v123 come from the owner's request of 15 Oct 2026 ("check design if you found any responsiveness issue in any device screen or any design,
ux ui related issues fix it and make website design easy to go for coding part"). Device scan, findings and verification: [tasks/responsive-v116/README.md](tasks/responsive-v116/README.md).
Script: `tools/examples/apply_v118_v123_responsive.py <project> <part>`. Coding hand-off written in the same task: [DEVELOPER_HANDOFF.md](DEVELOPER_HANDOFF.md)._

## v123 · `1792090563-62eb` — touch areas of at least 44 px on phones and touch screens (16 Oct 2026)

- **Files:** `site.css` (one block, `@media (max-width: 760px), (pointer: coarse)`).
- **Why:** 156 small links and buttons were 25–40 px tall on phones (footer links, festival-strip link, breadcrumb, calendar chips, અ+ button,
  strip pause button, contact links …); WCAG minimum met (24 px) but below the 44–48 px phones recommend.
- **Change:** each gets an invisible `::after` touch area (element `position: relative`), nothing moves or changes colour. A first attempt
  with padding + negative margin shortened phone footers by 70 px (footer links have a fixed height) — caught by the pixel compare, rebuilt.
- **Tests:** `tasks/responsive-v116/scripts/test_tap_areas.py` 156/156 targets reach 44 px at 390 and 320 px (v116: 0/156; stacked footer links
  40 px apart share the gap, no dead area); pixel compare: all boards identical to v122.

## v122 · `1792090553-d712` — WhatsApp band on small laptops (16 Oct 2026)

- **Files:** `site.css`, `HomeTabletL.dc.html` (frame 8192 → 8104; canvas h stays 8000).
- **Why:** at 1000–1279 px the four columns (badge · text · QR · button) left the text 210–330 px wide: heading "WhatsApp ચેનલમાં જોડાઓ"
  broke word by word at 1024 px and left "જોડાઓ" alone at 1180 px.
- **Change:** at 1000–1279 px badge 88 → 64 px, gaps 64 → 32 px, side padding 40 px, heading 28 px; `text-wrap: balance` on the band heading everywhere.
- **Tests:** heading on one line at 1024 / 1180; 1280+ and ≤ 999 unchanged; frames 0 to change after the HomeTabletL update.

## v121 · `1792090543-73a4` — festival chart labels readable on phones (16 Oct 2026)

- **Files:** `site.css`. **Why:** "રામ કથા" and "રમેલ" pills in the overview chart were 11 px. **Change:** 13 px (two lines inside the pill on the
  narrowest phones). **Tests:** fits at 320–760 px, both text sizes; desktop unchanged.

## v120 · `1792090533-1e4c` — phones turned sideways: Home buttons and darshan card (16 Oct 2026)

- **Files:** `site.css` (landscape `max-height: 500px` block). **Why:** at 568–640 px wide "મહોત્સવ વિશે જાણો →" was cut (equal-width buttons,
  no wrapping) and "સવારે ૬:૦૦ – રાત્રે ૧૦:૦૦" ran out of the darshan card (568 px). Seen on Main and HomeMobile.
- **Change:** buttons size to their label and wrap to a second row when needed; card times may wrap (balanced lines), card padding 16/18 px.
- **Tests:** 568×320, 640×360, 667×375, 740×360, 812×375: no clipping or spill; portrait unchanged.

## v119 · `1792090520-491b` — History chapter index on very small phones (16 Oct 2026)

- **Files:** `site.css`. **Why:** at 320 px "આધ્યાત્મિક પરંપરા" ran into its label "માતાજી અને ધામ પરિવાર" (title column squeezed by the label).
- **Change:** below 375 px the grey label sits under the title. **Tests:** 320/360 both text sizes; 375+ unchanged.

## v118 · `1792090496-e0cb` — leftover WhatsApp button removed from the phone Home page (16 Oct 2026)

- **Files:** `HomeMobile.dc.html`. **Why:** a green "જોડાઓ" WhatsApp button was pinned at 812 px on the phone Home board, over the top of the
  "દર્શન" section (and over the darshan card on sideways phones); the earlier review recorded it as removed ("bottom bar and band cover it"),
  and no other page or the desktop Home has it.
- **Change:** the button removed (its unused CSS `.vx-fab` stays, harmless). **Tests:** wording diff shows only that label gone.

## v117 · `1792089084-a7b0` — re-save, no content change (15–16 Oct 2026)

- The Design type updated itself (its own files changed); all 28 project files byte-identical to v116. Counted because the artifact numbers it.

_v111–v116 were published one after another on the owner's instruction "one version per fix". Built on v110 from the saved batch `tasks/fixes-1-6/` (patches + scripts); each stage byte-identical to the stage tested on v109 plus the v110 photo swap. Details, pictures and test logs: `tasks/fixes-1-6/REPORT.md`._

## v116 · `1791970043-58bb` — polish 6.1–6.5 (14 Oct 2026)

- **Files:** 21 page files (all except HomeMobile, MenuMobile, OfflineMobile) + `site.css`. Script `tasks/fixes-1-6/scripts/apply_item6.py <proj> 1…5`.
- **Change:** 6.1 Seva festival day tiles share one row of 7 equal columns at 1000–1179 px (were 5+2 / 6+1; audit C2). 6.2 festival night cards put the date above
  the artist names below 360 px (below 390 px in large text) — names no longer wrap word by word (C3). 6.3 `scroll-margin-top` 96 / 64 px on `#calendar`, `#travel`,
  `#progress`, so jump links no longer land with the heading under the top edge (C4). 6.4 footer column titles h4 → h2 (21 files) and Seva side-card titles h3 → h2,
  with rules that keep the exact previous look — no heading-level skips (C5). 6.5 Seva consent checkbox 22 → 24 px (C6).
- **Tests:** names wrapped 0/9 at 320–700 px both sizes; day tiles one row at 1000–1179, unchanged elsewhere; jump links land at 96 / 64 px; no heading skip on 24
  boards, heading change pixel-identical; checkbox 24×24. Whole batch on v110: pixel_regress — only Seva, SevaMobile, MenuMobile differ from v110; frames 0 to change.

## v115 · `1791970022-cc11` — Home buttons on very small phones (14 Oct 2026)

- **Files:** `site.css` (one rule, < 375 px). **Root cause:** equal-width buttons (`flex: 1 1 0`, no wrap, `overflow: hidden`), so "મહોત્સવ વિશે જાણો →" (148 px)
  was clipped at 320–340 px (audit B4). **Change:** below 375 px each phone home-banner button sizes to its label and shares the rest; never narrower than its label.
- **Tests:** 320–390 px in 5 px steps, normal + large text: one row, label 14–24 px from the button edge, 52 px tall — all OK (re-run on the final copy on v110).

## v114 · `1791970009-dcf8` — phone menu ✕ visible, closing returns to the page (14 Oct 2026)

- **Files:** MenuMobile + HomeMobile, ContactMobile, DarshanMobile, GalleryMobile, HistoryMobile, NewTempleMobile, NotFoundMobile, PranPratishthaMobile,
  SevaMobile (`.dc.html`) + `site.css`.
- **Root cause (audit B3):** ✕ was maroon on maroon (1.41:1) because `.vm-root a` outranked the design system's ivory; ✕ always opened Home and Home was always
  marked current. **Change:** ivory ✕ (14.3:1); ✕ and Escape go back to the page the visitor came from (Home when the menu was opened directly — the existing link
  stays as fallback); the current-page mark follows that page; the 9 phone pages remember their scroll position when ☰ is tapped and restore it on return (10 min).
- **Tests:** 320, 360, 390, 430, 844×390: contrast 14.32:1, 48×48 target, focus ring; direct open → Home marked, ✕ → Home; from Darshan at 1,400 px → Darshan marked,
  ✕ → back at 1,400 px; Escape → back; other link → that page. All pass on the final copy on v110. Inside the Claude Design canvas ✕ falls back to Home.

## v113 · `1791969994-902a` — Seva form errors brought into view (14 Oct 2026)

- **Files:** Seva, SevaMobile (`.dc.html`) + `site.css`.
- **Root cause (audit B2):** a failed submit showed the messages but did not move: focus stayed on the button and on phones the messages were ~3,000 px above;
  fields had no `aria-invalid` / link to their message. After a valid submit the confirmation (which replaces the form) was also off screen.
  **Change:** on failure the page scrolls to the first invalid control (form order) and focuses it; `aria-invalid` + `aria-describedby` on name, mobile, town,
  consent; on success it scrolls to the confirmation and focuses its heading. Typed values kept; no wording change.
- **Tests:** 7 scenarios × 1440, 1024, 390, 320 + 390 large = 35/35 pass on the final copy on v110 (focus on the right control, on screen above the bottom bar,
  values kept, aria-invalid correct; valid → confirmation on screen). Reduced motion: instant jump. Screen-reader output not tested.

## v112 · `1791969980-ab75` — working header menu on tablets and small laptops (14 Oct 2026)

- **Files:** Main, HomeTablet, HomeTabletL, HomePhoneL, NewTemple, PranPratishtha, Seva, Gallery, History, Contact, Darshan, NotFound (`.dc.html`) + `site.css`.
- **Root cause (audit A1, P1):** below 1180 px the design system hides the header links and shows ☰; on these 12 boards ☰ was a `<button>` with no action.
  **Change:** ☰ opens the design system's own menu panel (`.vm-mnav`, id `vx-tnav`, as on the phone menu page) with the board's 8 links (current page marked), brand,
  text-size button, WhatsApp and phone; `role="dialog"`, `aria-modal`, `aria-expanded`/`aria-controls` on ☰; ✕ button, Escape closes, Tab stays inside, focus to ✕
  on open and back to ☰ on close; above the phone bottom bar (z-index 90); one centred column ≤ 720 px; hidden from 1180 px.
- **Tests:** 81 runs (9 pages × 760–1180 px + tablet/landscape boards + large text) — 0 problems on the final copy on v110. With the menu closed all boards look as before.

## v111 · `1791969961-3b92` — Seva desktop help column (14 Oct 2026)

- **Files:** `site.css` (3 rules, ≥ 1000 px). **Root cause (audit B1):** form ~2,100 px, help column ~1,000 px, and the section's `overflow: hidden` stops a sticky card,
  so the right side was empty beside section ૩. **Change:** the column runs the full height of the form; the "સહાયની જરૂર છે?" card stays in view under the compact
  header; section `overflow: clip`. Single column below 1000 px unchanged.
- **Tests:** 24–26 scroll positions at 1440 / 1024: no overlap, stays in its column, stops 96 px above the footer; empty-column positions 6–7 → 0 at 1024–1440.

## v110 · `1791960914-1d1c` — new photo of ભગવાન શ્રી કરમશીબાપા (14 Oct 2026)

- **Files:** Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile2, History, HistoryMobile, Gallery, GalleryMobile (`.dc.html`) — the image address only.
  New image asset **27** `27_portrait_karamshibapa_blessing-glow` = `/_blob/0719d6d6a37c83a09b9880ba4507c70f` (1086×1448 WebP q92, 138,656 bytes, from the owner's
  photo `tasks/bapa-photo/originals/karamshibapa_blessing_bust_owner-2026-10-14.png`). Script: `tools/examples/apply_v110_karamshibapa_photo.py`.
- **Why:** owner's phone screenshot of the "૦૧ · મુખ્ય પૃષ્ઠ" board: the close-up 07 (1100×985, landscape, 50 KB) in the tall 3:4 arch showed only its middle —
  face filling the frame, turban cut, soft when enlarged. Owner sent two new photos and asked to use the one that fits, in good quality.
- **Change:** the owner's half-length blessing photo (exactly 3:4, so it shows whole) replaces 07 in all 14 places: Home portrait pair (`.vx-duo`) and photo strip
  (`.vx-strip`) on the 5 home boards, History chapter 3 portrait (`.vm-profile`, desktop + phone), Gallery banner trio (`.vx-trio`, desktop + phone).
  Alt text, captions, classes, inline styles and `site.css` unchanged. 07 stays in the asset store (rollback) but is referenced nowhere.
  The owner's seated full-length photo (`…_seated_owner-2026-10-14.png`) is kept in `tasks/bapa-photo/originals/`, not used (face too small in the small arches).
  No AI enlargement: the photo's own resolution is sharp at ≥ 2.47× on every frame (≥ 2.73× on phones), and enlargement could alter the face.
- **Tests:** frame boxes identical before/after (30 frame × size cases, `tasks/bapa-photo/scripts/measure_frames.py`); check_layout 72 runs (9 boards, all widths,
  both text sizes) 0 new problems; frames unchanged; wording identical; pixel_regress: the 15 other boards identical (MenuMobile = known noise); on the 9 changed boards
  every changed pixel lies inside a photo frame once the home ribbon's motion noise is masked (`diff_inside_frames.py`). The items 1–6 batch (unpublished) rebuilds
  cleanly on v110: result = saved batch + this image swap, identical. Pictures: `tasks/bapa-photo/pictures/`.

## v109 · `1791922103-42cb` — banner light stays behind Mataji / the temple (14 Oct 2026)

- **Files:** `site.css` only (one keyframes line changed, one commented block appended). Script: `tools/examples/apply_v109_banner_light.py`.
- **Root causes:** (1) the banner's gold light was painted at a fixed spot of the whole banner (`bundle.css` `.vm-hero`: radial-gradient at 72 % 42 %), which is
  behind the picture only while the picture sits on the right (desktop); in tablet portrait, phones and phone landscape the picture moves below the text and
  the light stayed beside the title (owner's screenshot, Festival 768×1024). (2) The breathing animation `vx-halo` set `transform: scale()`, which replaced
  the halo's own `translateX(-42%)`, so while animating the halo sat up to half its width to the right of the picture.
- **Change:** on banners with a picture (Home ×5 boards, New Temple, Festival, Gallery, desktop + phone) the light is drawn by `.vm-hero__art::before`
  inside the picture's own box (same colour and strength, about the same size on desktop); the halo is centred in the picture box with `translate`,
  and the breathing uses the separate `scale` property. Banners without a picture are unchanged.
- **Tests:** halo centre vs. visible artwork at 17 sizes × 7 boards + 3 tablet/landscape boards, animation running and reduced motion, and after
  portrait↔landscape resize: offset ≤ 2 % across / ≤ 8 % down (before: up to 92 % / 71 %). Before/after at the owner's 12 sizes (Home, New Temple,
  Festival, Gallery). check_layout 94 runs, 0 new problems; frames unchanged; pixel check: 12 boards without a picture banner identical, the other 12
  differ only inside the banner; the light and halo never catch taps. Pictures: `tasks/visual-effects/v109/`.

## v108 · `1791920313-6e1c` — new chakra everywhere (14 Oct 2026)

- **Files:** Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile, NewTemple, NewTempleMobile, PranPratishtha, PranPratishthaMobile (`.dc.html`).
- **Change:** the old chakra drawing (simple oval-petal mandala) was still used in two ornaments: `svg.vm-mandala` in the dark "નવું મંદિર" band of
  all 5 home boards, and `svg.vm-cta__orn` in the maroon call-to-action card of New Temple and Festival (desktop + phone). Both now draw the new lotus
  mandala already used by the banners (`vm-hero__mandala`), the closing devotional band (`vm-devotional__mandala`) and the photo slots. Only the drawing
  inside each `<svg>` changed; size, position, colour and opacity are as before. Script: `tools/examples/apply_v108_new_chakra.py`.
- **Why:** owner spotted the old chakra on the phone home page and asked for every old pattern to be replaced on all pages.
- **Tests:** all 24 boards now carry only the new drawing (hash check); desktop and phone carry the same pattern section by section; check_layout 72 runs
  (9 boards, 320–1440 px, both text sizes) 0 new problems; frames unchanged; wording identical; pixel check: the 15 other boards identical, and on the 9
  changed boards every changed pixel lies inside the ornaments (with pseudo-element animations frozen). Pictures: `tasks/visual-effects/v108/`.

## v107 · `1791918685-cd89` — re-save, no content change (13 Oct 2026)

- All 28 project files byte-identical to v106 (only the Design type's own files changed). Counted because the artifact numbers it.

## v106 · `1791624520-9b52` — "નવા મંદિરનો સંકલ્પ" text from the trust

- **Files:** NewTemple, NewTempleMobile, Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile, History, HistoryMobile (`.dc.html`), `site.css` (appended), `canvas.json`.
- **Change:** New Temple section `vis-t`: placeholder replaced by the trust's 3 paragraphs; eyebrow "સંકલ્પ" → "મંદિરની સંકલ્પના અને હેતુ";
  text column wider on desktop (≥1100: 7fr/5fr), text above image at 768–1099, facts row kept in one line on tablets (`.vx-prose`, `.vx-sk`).
  Home "નવું મંદિર" section: 2-sentence teaser from paragraph 1. History ch. 6: the સંકલ્પ sentence completes the lead line.
  Text edits to the trust's copy (reported to the owner): સનંદ→સાણંદ, ભગવાન કરમશી બાપા→ભગવાન શ્રી કરમશીબાપા, તેમના→તેઓશ્રીના, સમૂહિક→સામૂહિક;
  the trust's subtitle "શ્રી વિહત મેલડી ધામ – મંદિરની સંકલ્પના અને હેતુ" used as the eyebrow without its "શ્રી વિહત મેલડી ધામ –" prefix;
  closing "જય શ્રી વિહત મેલડી માતાજી!" not added (pages already end with the jaykaar). Frames: NewTemple 8647, NewTempleMobile 11846, Main 8090,
  HomeTablet 10804, HomeTabletL 8192, HomePhoneL 9092, HomeMobile 5249, History 8129, HistoryMobile 10511. Canvas to-do note updated.
- **Why:** owner supplied the content and delegated placement.
- **Tests:** 72 layout runs (9 boards × widths 320–1440 × normal/large text) — 0 new problems. All other boards pixel-identical; changed boards identical above
  and below the changed section (home differences only inside the moving text ribbon, which also differs between two loads of the same version).
  Frames fit at the 5 daily times. Text diff vs v105 = exactly the 3 placeholders + 1 eyebrow.

## v105 · `1791622143-5d00` — "આજે" marker on પૂનમ days and in Indian time

- **Files:** Darshan, DarshanMobile.
- **Change:** on a પૂનમ date (from the page's `EV` list) "આજે" moves to the પૂનમ tile; the weekday is taken from the Indian date (UTC+5:30), as the calendar already did.
- **Why:** a પૂનમ on an ordinary weekday read as "no ગાદી today"; overseas visitors saw their local day.
- **Tests:** 85 cases (17 moments around Indian/overseas midnights and પૂનમ dates × 5 visitor timezones) on desktop and phone pages — all correct and in step with
  the calendar's "ચાલુ છે"; 64 layout runs (4 dates × 8 widths × 2 text sizes) — 0 new problems, heights identical; ordinary days in India pixel-identical to v104.

## v104 · `1791621046-995a` — Darshan timetable

- **Files:** Darshan, DarshanMobile, `site.css` (appended `.vx-tt--day`, `.vx-tt__week`), `canvas.json` (Darshan h 5718→5030, DarshanMobile 7347→7090).
- **Change:** 8 identical day rows → row 1 "દરરોજ · સોમવારથી રવિવાર" (one timeline: darshan bar, two aarti marks, ભોજનશાળા) + row 2
  "માતાજીની ગાદી · રવિવાર · મંગળવાર · પૂનમ" (8 day tiles, ગાદી days highlighted, today marked). Tablet: labels above rows, no sideways scroll. Phone: 4×2 tiles.
- **Why:** hours are the same every day, so the chart repeated one row 8 times; tablet chart was cut off.
- **Tests:** 13 widths × 2 text sizes — 0 new problems; today marker correct on all 7 days; wording check (all text already in v103); other boards pixel-identical;
  content below the timetable identical (196–200 elements); frames fit at all daily times. Chart 1,018→330 px (desktop), 504→247 px (phone).

## v103 · `1791617581-c8ff` — invitation note

- **Files:** PranPratishtha, PranPratishthaMobile. **Change:** "મહોત્સવનું નિમંત્રણ અને પત્રિકા સગાં-સ્નેહીઓને મોકલો" → "મહોત્સવનું નિમંત્રણ સગાં-સ્નેહીઓને મોકલો".
- **Why:** the PDF does not exist yet. **Tests:** 16 runs, 0 problems; heights unchanged.

## v102 · `1791617270-e652` — festival PDF button hidden

- **Files:** `site.css` (block "Festival PDF button hidden": `.vm-root .vx-patrika { display: none !important; }` with restore instructions), PranPratishthaMobile frame 13888→13824.
- **Why:** no PDF yet. **Tests:** 16 runs, 0 problems.

## v101 · `1791617104-8b44` — home page becomes a festival summary

- **Files:** Main, HomeMobile, HomeTablet, HomeTabletL, HomePhoneL, `site.css` (`.vx-sumacts`), `canvas.json` (HomeMobile 6906→5083).
- **Change:** large festival section removed from home (stays on the festival page); event cards keep date/name/time/place; actions "સંપૂર્ણ કાર્યક્રમ",
  "સેવા નોંધણી કરો", "WhatsApp પર નિમંત્રણ મોકલો"; events section ivory on home. Owner's choices: night strip kept, PDF button removed from home,
  "નવું મંદિર" and "એક નજરે" kept separate.
- **Tests:** 30 runs, 0 problems; 24 frames fit. Page heights −1,175 to −1,823 px per home board.

## v100 · `1791592628-54e6` — compact ivory WhatsApp band on phones

- **Files:** `site.css` (phone rule: 48 px padding for sections holding only the WA band), PranPratishthaMobile 14000→13888, HistoryMobile 10523→10411.
- **Tests:** 104 runs, 0 problems; 24 frames fit; 27 spec pictures unchanged (max diff 1/255 noise).

## v99 · `1791590131-fe8b` — page endings and Seva shift cards

- **Based on:** `1791588058-863e` (v98, an editor re-save of v97 with identical content — checked byte-for-byte).
- **Change:** WhatsApp band added to New Temple (+phone, standard) and History (+phone, festival ivory variant); Contact: WA band moved below the FAQ +
  devotional band; Darshan: devotional band; `site.css`: `.vx-shift` padding 12 px at 761–1099 px (shift-card titles no longer wrap at 1024).
- **Tests:** 174 runs, 0 new problems; 24/24 frames fit; 27 spec pictures identical to v97.

## v97 · `1791587967-2aa6` — Gate A preview fixes applied to the website

- **Based on:** the owner's save `1791587156-17be` (04:35 IST).
- **Change (24 files):** festival strip on compact pages and short phone strip text; title non-breaking spaces; 9 Feb shown as સમાપન; WhatsApp dark variant removed;
  portrait and flag crop fixes; phone festival banner with one temple image (1,053→770 px); year never split from its month (NBSP); Karamshibapa portrait restored on
  the home heritage arch; phone button/heading rules (nowrap labels, wrapping rows, `text-wrap: balance`, CTA padding).
- **Tests:** 12 phone pages × 4 widths (320/360/390/430) — 0 issues; desktop 78 runs — 0 new issues; 27 spec pictures pixel-identical to the reviewed preview; frames = content + 3 px.
