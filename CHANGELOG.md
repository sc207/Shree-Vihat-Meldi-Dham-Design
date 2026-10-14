# CHANGELOG.md

Published versions of the website design artifact `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`.
Each entry: version · version id · files · reason · tests run (with their actual results). All dates 10 Oct 2026 unless noted.
History before v97 (the original build, 30 Sep – 9 Oct 2026) lives in the artifact's version history and is not reconstructed here.

Standard verification after every publish below: the changed files were read back from the live artifact and compared byte-for-byte with what was sent (all matched).

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
