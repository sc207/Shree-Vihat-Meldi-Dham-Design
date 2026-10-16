# CHANGELOG.md

Published versions of the website design artifact `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa`.
Each entry: version · version id · files · reason · tests run (with their actual results). All dates 10 Oct 2026 unless noted.
History before v97 (the original build, 30 Sep – 9 Oct 2026) lives in the artifact's version history and is not reconstructed here.

Standard verification after every publish below: the changed files were read back from the live artifact and compared byte-for-byte with what was sent (all matched).

_v126 onward come from the owner's follow-up of 16 Oct 2026: "also check other images have this issue" (after v125). Image check of every
picture on every page, findings and pictures: [tasks/image-audit/README.md](tasks/image-audit/README.md)._

## v147 · `1792167781-b26d` — ભગવાન શ્રી કરમશીબાપા photo: blessing hand and face in focus (16 Oct 2026)

- **Owner:** "it looks good. just now sharp that image as you can see if we zoom see blessing hand it does not looks in focus. so do it as we did
  in suresh bapa." — then, while it was being made: "as like blessing hand also focus on face so it looks more better and also check if sharpness
  required or not".
- **What was found:** in 38 the hand was clearly softer than the face (focus ratio, fine ÷ medium detail: hand 0.35, fingers 0.32, face 0.56) — already
  so in the supplied photo; and 38 was saved at 1.5×, where સુરેશબાપા's 34 is at the full 2×. Turban (0.46) and clothes were checked at 1:1: crisp, left alone.
- **Change:** 38 → 39 (2172×2896 = exactly 2× like 34, same 3:4 shape, 448 KB WebP q90): same HD step and finish as 38, plus edge sharpening
  that cannot draw rims (every pixel stays inside its 9×9 neighbourhood's own range) — hand, rings and wrist at 0.9 / 1.3 (limited to skin and
  rings, so the gold background and white cloth beside the hand are untouched), face, eyes, moustache and ear-rings lightly at 0.4 / 0.9.
  After: hand 0.51, fingers 0.45, face 0.79, eyes 0.70. Colour unchanged (mean RGB within 0.5). Shrunk back to the original size: 32.5 dB.
  Same 14 places on 9 pages; `tasks/karamshi-natural/scripts/make_38_sharp.py`, `tools/examples/apply_v147_karamshibapa_hand_focus.py`.
- **Tests:** layout check on all 9 boards — 72 runs, 0 new problems; frames 0 to change; 9 live files read back byte-identical, asset checksum
  matches `design/assets/`. Picture: `tasks/karamshi-natural/pictures/v147_hand_face_zoom_before_after.png` (History on a phone, pinch-zoomed 2×).

## v146 · `1792165942-c158` — ભગવાન શ્રી કરમશીબાપા photo in HD (16 Oct 2026)

- **Owner:** "karamshi bapa image actually looks like ai generated … suresh bapa image how their skin tone and actual looks original. same hd and
  humanize image set for karamshibapa image. if have same image in other pages also fix over there"; then (screenshot of the blessing photo) "make it
  feels image and person skin real just like we have fixed the suresh bapa image".
- **What was found:** image 27 (owner's photo of 14 Oct) was used exactly as supplied (v110, no processing); its skin already carries a generated,
  smoothed texture. Three options were shown side by side (`tasks/karamshi-natural/pictures/options_A_B_C.png`): A keep, **B the blessing photo
  through the same HD step as સુરેશબાપા's**, C his genuine camera photo (08) on the same golden glow. The owner chose **B**.
- **Change:** 27 → 38 (1629×2172, same 3:4 shape): Real-ESRGAN x4plus halved to 2× + photographic finish (gentle clarity, fine grain), saved at 1.5×
  (`tasks/karamshi-natural/scripts/photo_finish.py`). 14 places on 9 pages (Home pair + strip on every Home board, History ch. 3, Gallery banner).
  Built on the live files of v145 (see below). Script `tools/examples/apply_v146_karamshibapa_hd.py`.
- **Tests:** layout check Main, HomeMobile2, History, HistoryMobile, Gallery, GalleryMobile — 66 runs, 0 new problems; frames unchanged; every frame
  ≥ 1.36× the pixels needed (3× phones); 15 live files read back byte-identical; asset checksum matches `design/assets/`.

## v139–v145 · last `1792164754-08ae` — editor saves, no visible change (16 Oct 2026, evening)

- Saved by the design editor while the owner had the canvas open. Compared with v138: 7 pages (ContactMobile, GalleryMobile, HistoryMobile, NewTemple,
  NewTempleMobile, PranPratishthaMobile, SevaMobile) now write the no-break spaces as `&nbsp;` instead of the U+00A0 character (same text, checked),
  and `canvas.json` ends with a newline. `design/project/` follows the live files; v146 was built on them.

_v133–v138 come from the owner's list of 16 Oct 2026, 19:40 IST (Home photos, new-temple introduction, "ટ્રસ્ટ દ્વારા", the દર્શનનો માર્ગ pictures,
the પ્રાણ પ્રતિષ્ઠા date, the Darshan travel cards; the tagline request is answered with options, not published). One version per item; the request
handed the decisions over. Before/after pictures: `tasks/owner-fixes-1016/pictures/`. Live files read back after v138: 25/25 byte-identical._

## v138 · `1792162446-ce3e` — દર્શનનો માર્ગ: pictures from the architectural render (16 Oct 2026)

- **Owner:** "[પ્રવેશથી ગર્ભગૃહ સુધી ભક્તનો અનુભવ …] is that any way that we can showcase the proper image even if it will be visualise".
- **Files:** `NewTemple`, `NewTempleMobile`, `site.css` (block); new images 35–37 (close-ups cut from the render 14, no AI). Script `apply_v138_route_images.py`.
- **Change:** the empty [ફોટો] boxes of ૦૧ ગર્ભગૃહ, ૦૨ મંડપ, ૦૩ પ્રવેશદ્વાર show the doorway with માતાજી, the pillared hall and the entrance steps
  and porch, each labelled "સ્થાપત્ય ચિત્ર" (so they are not taken for photographs). ૦૪ [અન્ય વિભાગ] stays a placeholder (not in the render).
- **Tests:** layout check NewTemple + phone 22 runs, 0 new problems; frames unchanged; images ≥ 1.0 of the pixels a 2× screen needs.

## v137 · `1792162441-23e8` — Home photo order: મંદિર, માતાજી, કરમશીબાપા, સુરેશબાપા (16 Oct 2026)

- **Owner:** "main page phto : mandir, mataji, karamshi bapa, suresh bapa".
- **Files:** `Main`, `HomeTablet`, `HomeTabletL`, `HomePhoneL`, `HomeMobile2`, `site.css` (block), `canvas.json`. Script `apply_v137_home_photo_order.py`.
- **Change:** order મંદિર · વિહત માઁ · મેલડી માઁ · કરમશીબાપા · સુરેશબાપા (was મંદિર · કરમશીબાપા · વિહત માઁ · સુરેશબાપા · મેલડી માઁ). Phones (≤ 760 px)
  showed only the first three tiles (સુરેશબાપા and મેલડી માઁ hidden; with the new order both Bapas would have been hidden) — now all five:
  temple full width, the two માતાજી, the two Bapas. HomeMobile2 frame 5750 → 5986 (canvas h too).
- **Tests:** layout check Main + HomeMobile2 22 runs, 0 new problems; frames 0 to change after the update.

## v136 · `1792162435-c602` — પ્રાણ પ્રતિષ્ઠા date written in full (16 Oct 2026)

- **Owner:** "પ્રાણ પ્રતિષ્ઠા page · પ્રાણ પ્રતિષ્ઠા · બપોરે ૧૨:૩૯ · ૮ ફેબ્રુ., સોમવાર full".
- **Files:** `PranPratishtha`, `PranPratishthaMobile`. **Change:** banner date strip "૮ ફેબ્રુ., સોમવાર" → "૮ ફેબ્રુઆરી, સોમવાર".
- **Not changed:** the same strip in the Home banner keeps "૮ ફેબ્રુ." — tested: the full form wraps both boxes onto two lines on sideways
  phones (HomePhoneL +28 px) and runs past the strip at 320 px. (The short form already overruns by 2 px at 320 px — noted, not changed.)
- **Tests:** fits on one line at 320 px (19 px spare) and desktop; layout check 22 runs, 0 new problems; frames unchanged.

## v135 · `1792162429-bdf2` — new-temple introduction: "મંદિરનો", no "દાન" (16 Oct 2026)

- **Owner:** "nava mandir no parichay : replace ટ્રસ્ટનો to Mandir no. remove દાન".
- **Files:** `NewTemple`, `NewTempleMobile`, `Main`, `HomeTablet`, `HomeTabletL`, `HomePhoneL`, `HomeMobile`. Script `apply_v135_intro_mandir.py`.
- **Change:** "… એ જ ટ્રસ્ટનો મુખ્ય હેતુ છે." → "… એ જ મંદિરનો મુખ્ય હેતુ છે." (all 7 boards); "ટ્રસ્ટનો વિશ્વાસ છે કે ભક્તોના સહયોગ, દાન અને નિઃસ્વાર્થ
  સેવાથી …" → "મંદિરનો વિશ્વાસ છે કે ભક્તોના સહયોગ અને નિઃસ્વાર્થ સેવાથી …" (New Temple). No "ટ્રસ્ટનો" left on the site.
- **Tests:** layout check 44 runs, 0 new problems; frames unchanged.

## v134 · `1792162423-7494` — "ટ્રસ્ટ દ્વારા" removed (16 Oct 2026)

- **Owner:** "ટ્રસ્ટ દ્વારા remove this word and check if we can set mandir and not require then dont add anything".
- **Files:** 12 pages (Contact, Gallery, History, NewTemple, PranPratishtha, Seva + phone pages). Script `apply_v134_remove_trust_by.py`.
- **Change:** all 15 texts: 13 placeholders lose " — ટ્રસ્ટ દ્વારા"; "ટ્રસ્ટ દ્વારા ફોટો મળ્યે ઉમેરાશે" → "ફોટો મળ્યે ઉમેરાશે"; "ટ્રસ્ટ દ્વારા ચકાસાયેલ
  લખાણ" → "ચકાસાયેલ લખાણ"; the one sentence that needs a subject: "મંદિર દ્વારા જાહેર થયેલ સત્તાવાર કાર્યક્રમ." Other trust mentions
  ("ટ્રસ્ટ તરફથી …", "[ટ્રસ્ટ કાર્યાલય…]", "ટ્રસ્ટને") were not part of the request and stay. Frames: GalleryMobile 10455 → 10403,
  NewTempleMobile 11846 → 11812 (placeholders now fit on fewer lines).
- **Tests:** layout check 12 boards, 132 runs, 0 new problems; frames 0 to change after the update; wording diff = exactly these 15 texts.

## v133 · `1792162413-08a8` — Darshan: gap between the travel cards and the map (16 Oct 2026)

- **Owner:** "the gap between રેલવે / બસ / માર્ગ / હવાઈ માર્ગ cards and the direction — no gap" (screenshot).
- **Files:** `site.css` (block: `.vx-dmap` margin-top 24 px — it had no spacing rule), `Darshan`, `DarshanMobile` (frames 5030 → 5054,
  7090 → 7114), `canvas.json` (h). Script `apply_v133_travel_gap.py`.
- **Tests:** layout check 22 runs, 0 new problems; frames 0 to change after the update.

## v132 · `1792156846-744e` — re-save, no content change (16 Oct 2026)

- Design-type update; 25 project files read and byte-identical to v131 (the other 3 unchanged in size). Counted because the artifact numbers it.

_v130–v131 come from the owner's message of 16 Oct 2026, 12:21 IST: "If you think we need to modify any fixes then do it and push it"._

## v131 · `1792133852-3202` — gallery viewer: Escape, tap outside, keyboard focus (16 Oct 2026)

- **Files:** `Gallery.dc.html`, `GalleryMobile.dc.html` — page logic and the dialog element only (script `tools/examples/apply_v131_viewer_keys.py <project>`).
- **Why:** completes v126. The viewer closed with ✕ only: Escape did nothing, tapping the dark area did nothing, and keyboard focus stayed on the
  photo behind the dialog (a keyboard or screen-reader user could not reach ✕ directly). The developer guide already promised Escape.
- **Change:** same pattern as the tablet menu — focus moves to ✕ when the viewer opens (Tab stays inside), Escape closes, a tap/click on the dark
  area around the panel closes (not on the photo or caption), and focus returns to the photo that opened it; the page does not move.
- **Tests:** `tasks/image-audit/scripts/test_viewer_keys.py` — 3 photos × 4 screen sizes (1440, 1024, 390, 320) × 7 checks: 84/84 pass, no script
  errors (v129: 64 of 84 fail). Layout check Gallery + phone 22 runs: 0 new problems; pixel compare with the viewer closed: identical; wording unchanged.

## v130 · `1792133845-2a4a` — canvas to-do note brought up to date (16 Oct 2026)

- **Files:** `canvas.json` only (`notes.todo`; script `tools/examples/apply_v130_todo_note.py <project>`). No page changes.
- **Change:** (1) the PDF line, approved on 10 Oct: `• કાર્યક્રમ પત્રિકાની PDF — "કાર્યક્રમ પત્રિકા (PDF)" બટન તૈયાર છે, લિંક મૂકવાની બાકી` →
  `• કાર્યક્રમ પત્રિકાની PDF (હાલ બટન છુપાવેલું છે)` (the button has been hidden since v102; same form as the Facebook line).
  (2) new line after the photo requests: `• પરમ પૂજ્ય ભગવાન શ્રી કરમશીબાપાના આસન પર બિરાજમાન ફોટાની મોટી મૂળ ફાઇલ (હાલનો ફોટો નાનો છે)` (image 09, see v127).
  (3) `maxH` 1377 → 1480 so the longer note is not cut (measured +101 px; nothing below the note on the canvas).
- **Tests:** JSON valid; everything else in `canvas.json` identical; read back byte-identical.

## v129 · `1792098632-85c8` — re-save, no content change (16 Oct 2026)

- Design-type update (its own `app.js` changed); all 28 project files byte-identical to v128 (checked 16 Oct, 12:20 IST). Counted because the artifact numbers it.

## v128 · `1792098080-6f1e` — સુરેશબાપા blessing photo in HD (16 Oct 2026)

- **Files:** `Main`, `HomeMobile2`, `HomeTablet`, `HomeTabletL`, `HomePhoneL`, `History`, `HistoryMobile`, `Gallery`, `GalleryMobile` (.dc.html) —
  image address only, 14 places (home boards use it twice: pair + strip). Script `tools/examples/apply_v128_blessing_hd.py <project>`.
- **Why:** the re-measure after v127 left image 10 (1100×1019; Home pair, History arch, Gallery) at 0.64 of the pixels a 3× phone needs
  (0.87–0.96 on 2× screens) — by the same rule as v127 it gets the same treatment.
- **Change:** 10 → 34 (2200×2038, exactly 2×; Real-ESRGAN x4plus halved). Face and raised hand compared at 1:1 with the original (eyes, tilak,
  ear-rings, rings and palm lines unchanged; shrunk back it matches the original at 38.9 dB).
- **Tests:** `check_layout.py` Main, HomeMobile2, History, HistoryMobile, Gallery, GalleryMobile — 66 runs, 0 new problems; frames (9 boards) 0 to change;
  wording unchanged; no page uses 10 any more; server checksum of 34 matches `design/assets/`.

## v127 · `1792096917-c470` — two સુરેશબાપા photos in HD (16 Oct 2026)

- **Files:** `Gallery.dc.html`, `GalleryMobile.dc.html`, `History.dc.html`, `HistoryMobile.dc.html` — image addresses only
  (script `tools/examples/apply_v127_portraits_hd.py <project>`). New images 32, 33 uploaded to the artifact's image store.
- **What was wrong:** the image check measured every picture at every screen size: two photos were drawn far larger than their pixels —
  13 smiling cut-out 470×501 (Gallery tile and viewer: 0.45–0.5 of the pixels a 2× screen needs) and 11 candid 585×882 (Gallery tile 0.77,
  viewer 0.65; small History portrait).
- **Change:** 13 → 32 (940×1002, transparent background kept) and 11 → 33 (1170×1764): exactly 2× — Real-ESRGAN x4plus, then halved with
  Lanczos (halving removes the model's invented fine detail). Faces compared at 1:1 with the originals (eyes, moustache, wrinkles, ring, beads
  unchanged; shrunk back they match the originals at 36.5 dB); realesr-general-x4v3 was rejected (smoothed the skin). Cut-out edges checked on
  light and dark grounds (no fringe).
- **Not changed:** 09 કરમશીબાપા seated poster (784×1045) — both upscalers drew new dark outlines on his face and neck, so it stays as supplied;
  a larger original is needed from the trust. 10 સુરેશબાપા blessing (1100×1019) and 14 temple render are adequate (≥ 0.82 on 2× screens,
  except the zoomed tablet crop of 14, left as is: AI sharpening could invent carving details).
- **Tests:** `check_layout.py` 4 boards, 44 runs: 0 new problems; frames: 0 to change; wording: no change; no page uses 11 or 13 any more;
  server checksums of 32/33 match `design/assets/`. Pictures: `tasks/image-audit/pictures/`.

## v126 · `1792095937-de85` — gallery viewer opens on screen and fits phones (16 Oct 2026)

- **Files:** `site.css` (one block at the end; script `tools/examples/apply_v126_gallery_viewer.py <project>`).
- **What was wrong:** the photo viewer (tap a Gallery photo) was `position: absolute` at the top of the page: a photo opened from lower down
  showed only the dark scrim — the photo was off-screen above (240 of 242 test openings had the panel partly or fully off screen).
  Its image area was a fixed 680 px (caption and ✕ below the edge of a 1440×900 laptop) and it had no phone rules: on a 390 px phone the
  photo was 214 px wide above ~450 px of empty panel.
- **Change:** fixed to the screen and centred (same as the phone menu `.vm-mnav`), z-index above the bottom bar; image area at most the screen
  height minus the panel; phones: 16 px margins, photo across the full panel width; phones sideways: compact panel.
- **Tests:** `tasks/image-audit/scripts/test_viewer.py` — 11 photos × 11 screen sizes (1920×1080 … 320×568, 844×390, 667×375) × normal/large text:
  panel and ✕ fully on screen 242/242 (v125: 2/242); phone photo 334 px wide at 390 (was 214). Pixel compare Gallery + GalleryMobile with
  the viewer closed: identical. Only these two pages have the viewer.

## v125 · `1792094175-7284` — the four ધામ પરિવાર pictures in HD, aligned (16 Oct 2026)

- **Owner's request:** "images not alligned and set properly. make sure those images should be HD and if not make it hd that looks good and does not
  seems downgrade image quality" (screenshot of the History chapter 2 row: Vihat માઁ, Meldi માઁ, Lakhnechi માઁ, Goga Maharaj).
- **Files:** `History.dc.html`, `HistoryMobile.dc.html`, `Gallery.dc.html`, `GalleryMobile.dc.html` — image addresses only
  (script `tools/examples/apply_v125_deity_hd.py <project>`). New images 28–31 (1200×1500 WebP) uploaded to the artifact's image store.
- **What was wrong:** 03/04 filled the arch and lost the animals' feet to cropping; 05/06 were small (380×534, 393×534 — blurry at 2× screens),
  sat lower and smaller on a dark ring background. Four different sizes, baselines and backgrounds in one row.
- **Change:** all four rebuilt the same way at 1200×1500 (= the 4:5 arch frame, so nothing is cropped): one warm-gold background with a soft light
  behind the head and a soft ground shadow; every figure 80 % of the height on the same baseline and inside the arch top. Vihat/Meldi from the
  HD cut-outs 21/22 (same paintings); Lakhnechi/Goga enlarged ×4 with Real-ESRGAN (x4plus, chosen after comparing three models) and cut out with IS-Net.
  Same pictures in the Gallery grid, its lightbox and the Gallery banner trio. Old 03–06 kept in the store for rollback.
- **Tests:** `check_layout.py` History/Gallery + phone, 44 runs (1440 → 320 px, normal + large text): 0 new problems; `frame_heights.py`: 0 to change;
  wording diff: none; no page still uses 03–06; before/after pictures in `tasks/deity-hd/pictures/`. Image checksums on the server match `design/assets/`.
- **Rollback:** publish v123's four files (`1792090563-62eb`; v124 has the same content).

## v124 · `1792093482-e8c1` — re-save, no content change (16 Oct 2026)

- Editor / Design-type re-save; all 28 project files byte-identical to v123. Counted because the artifact numbers it.

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
