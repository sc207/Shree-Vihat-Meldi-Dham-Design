# Design audit report — v106 (Phases A–C)

_10 Oct 2026. Baseline: live design v106 `1791624520-9b52`, all 24 boards. Brief: [full-design-audit.md](full-design-audit.md).
Viewable page with the same content: `https://claude.ai/artifact/FJjnL8j4NB95mK2tcSjQuU` (private to the owner)._

**No changes were made to the website during the audit.** Phase D (fixes) waits for the owner's approval; each fix will be its own previewed version.

### Status since the audit (14 Oct 2026, live v109 `1791922103-42cb`)

- **Fixed, owner's later requests (not in the findings below):** v108 old chakra replaced by the lotus chakra on all boards; v109 banner gold light and
  halo stay behind the picture at every screen size (owner's screenshot, Festival 768×1024). See [CHANGELOG.md](../CHANGELOG.md) and `tasks/visual-effects/`.
- **D1 answered in part:** the owner's screenshot showed the detached glow (fixed in v109), not cropped text.
- **Still open:** A1, B1 (Seva fix prepared, awaiting approval; it takes the next free version number, not v107), B2, B3, B4, C1–C9.
  Version numbers now follow the artifact's own count, so the plan's v107–v112 numbers below become the next free numbers.

| Priority | Count | Items |
|---|---|---|
| P0 critical | 0 | — |
| P1 high | 1 | A1 |
| P2 medium | 4 | B1 (fix prepared as v107), B2, B3, B4 |
| P3 polish | 9 | C1–C9 |
| Owner decision | 1 | D1 |

Pictures: [audit-v106/img/](audit-v106/img/). Scripts that produced the findings: [audit-v106/scripts/](audit-v106/scripts/)
(run from the repository root against `tools/serve.py` on port 8771). Pending Seva patch: [audit-v106/seva_v107_pending.diff](audit-v106/seva_v107_pending.diff).

## P1

### A1 · No header navigation between 761 and 1179 px — confirmed

- **Boards:** Main, HomeTablet (834), HomePhoneL (844), HomeTabletL (below 1180), NewTemple, PranPratishtha, Seva, Gallery, History, Contact, Darshan,
  NotFound (12 desktop/tablet files). Phone boards not affected.
- **What happens:** below 1180 px the 8 page links are hidden and a ☰ button shows; clicking it does nothing (clicked in Chromium: no menu, no navigation).
  iPads, laptops at 1024–1152 px and phone landscape lose header navigation. Footer links and in-page buttons still work.
- **Root cause:** `ds/vihatmeldimandir/components/bundle.css` lines 151–156 hide `.vm-nav` and show `.vm-menu-btn` below 1180 px. Phone boards:
  `<a class="vm-menu-btn" href="MenuMobile.dc.html">`. Desktop/tablet boards: `<button class="vm-menu-btn" type="button" aria-expanded="false">` with no
  handler and no panel.
- **Proposed fix (recommended):** a real drop-down panel under the header with the same 8 desktop links, toggled by the existing button, Esc closes,
  `aria-expanded` kept in step; styles reused from the phone menu. (Linking to MenuMobile would send tablet visitors to phone pages — not recommended.)
- **Picture:** `01_menu_button.jpg` (Main 1024×768, HomeTablet 834, Darshan 900, Main 1180 for comparison).

## P2

### B1 · Seva desktop: help column ends halfway beside the form — fix prepared (v107)

- **Boards:** Seva ≥ 1000 px. Right column empty for 6–7 scroll positions at 1024–1440 px.
- **Root cause:** column only as tall as its cards; the section's `overflow: hidden` prevents a sticky card.
- **Status:** 3 CSS rules appended to `site.css` (pending diff linked above), verified (no overlap with fields/submit, stops 96 px above the footer, 1024/1100/1280/1440,
  single column below 1000 px unchanged). **Awaiting approval.** Picture: `09_seva_column_1440.jpg`.

### B2 · Seva form: error messages appear out of view after a failed submit — confirmed

- **Boards:** Seva, SevaMobile.
- **What happens:** an empty submit shows the summary “કેટલીક વિગતો બાકી છે” and messages under name, mobile and town — all at the top of the form, more than
  3,000 px above the button on a 390 px phone. The page does not scroll, focus stays on the button; only the consent message beside the button is visible.
- **Root cause:** the form script adds `.is-invalid` and fills the `role=alert` region but does not scroll or move focus; fields lack `aria-invalid` and
  `aria-describedby`.
- **Proposed fix:** on a failed submit, scroll to and focus the summary (or the first invalid field); add `aria-invalid` / `aria-describedby`. No wording change.
  The success message already works. Picture: `08_seva_empty_submit_390.jpg`.

### B3 · Phone menu screen: close icon almost invisible; close always goes Home — confirmed

- **Board:** MenuMobile.
- **What happens:** ✕ is maroon on maroon, 1.41:1 (icons need ≥ 3:1; only its ring at 3.34:1 shows). Close always opens HomeMobile, and “મુખ્ય પૃષ્ઠ”
  is always marked current, whichever page the visitor came from.
- **Root cause:** `.vm-root a { color: var(--accent) }` (0,1,1) outranks `.vm-mnav__close { color: var(--ivory) }` (0,1,0) because the control is an `<a>` here;
  the shared static board hard-codes `href="HomeMobile.dc.html"` and `aria-current` on Home.
- **Proposed fix:** scoped rule `.vm-root .vm-mnav__close { color: var(--ivory); }` (14.3:1). Close returns to the previous page with Home as fallback, and the
  fixed current marker is dropped or set from that page — **owner to choose**. Picture: `03_menu_close.jpg`.

### B4 · Home hero button cut on 320–340 px phones — confirmed

- **Board:** HomeMobile ≤ ~340 px, normal and large text.
- **What happens:** “મહોત્સવ વિશે જાણો →” is wider than its button; the first letter is cut at the left. Fits at 360 px with little room.
- **Root cause:** `site.css` line 619 gives both phone home-hero buttons `flex: 1 1 0` + `white-space: nowrap`; `.vm-btn` has `overflow: hidden`, so its
  automatic minimum width is 0 and it shrinks below the label. The inner-page heroes have the guard `min-width: max-content` (line 1321); the home hero does not.
- **Proposed fix:** same guard on the phone home-hero buttons, so they stack when they do not fit; no change at ≥ 360 px. Picture: `02_home_button_320.jpg`.

## P3

| ID | Finding | Boards | Root cause → proposal |
|---|---|---|---|
| C1 | Four gallery photos are small originals: લાખણેચી માઁ 380×534, ગોગા મહારાજ 393×534, સુરેશબાપા cut-out 470×501 (enlarged 1.1× even at 1×), સુરેશબાપા portrait 585×882 | Gallery, GalleryMobile | Source files → larger originals from the trust; no design change |
| C2 | The 7 festival day tiles wrap 5+2 (1000 px) or 6+1 (1024–1100 px), leaving “૮ સોમવાર” alone | Seva 1000–1179 px | Fixed-width tiles in the narrowed form column → 7 equal columns at these widths. Picture `05` |
| C3 | Artist names wrap word by word at 320 px with large text; “માયાભાઈ આહીર” runs 4 px past its column | PranPratishthaMobile | Two-column night card too narrow → date above names at ≤ 360 px with large text. Picture `06` |
| C4 | Jump links land with the heading touching the top edge (“પંચાંગ”, “યાત્રા માર્ગદર્શન”, “નિર્માણ પ્રગતિ”); other 42 links fine | Darshan(+Mobile), NewTemple(+Mobile) | No `scroll-margin-top` on these targets → add it. Picture `07` |
| C5 | Heading levels skip: footer “પૃષ્ઠો” h2→h4 (19 boards); Seva “નોંધણી પછી શું?” h1→h3 | 19 boards; Seva(+Mobile) | Tag levels → change tags, classes unchanged |
| C6 | Consent checkbox 22×22 px (WCAG 2.2: 24×24); label is clickable so the tap area is larger | Seva(+Mobile) | Optional: 24 px |
| C7 | Hero entrance `vx-rise` 900 ms (brief: 350–650 ms); off under reduced motion | all heroes | Optional: 600 ms |
| C8 | Images without width/height (93 board×image cases); load shift ≤ 0.073 (lab) | deity art, gallery | Optional: add attributes |
| C9 | Text-only banners leave the right half empty at 1440/1920 | Contact, Darshan, Seva, NotFound | Approved design — note only |

## D1 · Header/hero (brief §3) — owner decision

- Not reproduced: 9 pages × 6 sizes (54 first screens: 320×640, 390×844, 768×1024, 1024×768, 1440×900, 1920×1080) plus ~100 hero measurements on 4 pages —
  no heading, date or button text cropped or under the header. Art fully visible in the first screen on every desktop size from 1024×768; tablets portrait
  (768–834) show 55–100%.
- Phones: the temple sits below the buttons. Home 36% visible at 360×640, ~45% at 390×664 (emulated iPhone with Safari bars), 90–100% at ≥ 360×780.
  Festival page 0–12% on short screens, 100% at 390×844. Pictures `04`, `04b`, `11`.
- **Questions:** which page and screen size showed cropped text? Should the whole temple fit in the first phone screen (tightening the hero on short phones,
  never shrinking text)?

## Checked and correct

- No sideways scrolling and no clipped Gujarati in 159 renders (phone files 320/360/390/430/540; desktop files 768/900/1024/1280/1440/1920; tablet boards at
  their widths; large text at 320/390/1024/1440). Box-spill scan (138 runs) found only B4 and C3 (plus closed FAQ answers and the festival day carousel,
  hidden on purpose).
- Contrast flags on dark sections are false alarms (close-ups `10`).
- “Dead” buttons in the click test (“બધું”, “આખો દિવસ”, “૨ મંગળ”) are already-selected options.
- A blank gallery tile in a full-page capture was lazy loading; it loads on scroll.
- Focus ring visible on the first 30 Tab stops (fewer on short pages) on 20 pages; skip link on all content pages.
- Reduced motion stops every animation (11 pages tested). 48 jump links on 16 pages reach their targets; none under a fixed bar.
- Seva form: error summary, field messages and success message appear. Load-time layout shift ≤ 0.073 everywhere (lab).

## Not verified

Chromium only (no Firefox, Safari/WebKit, real devices) · no Core Web Vitals (no hosted site, no field data) · no screen reader · hover and real touch not
exercised · phone heights with browser bars are emulated · fonts loaded from a local copy (Google Fonts on the live site not checked) · boards tested as pages
in a local server with the design runtime, not on the Claude Design canvas.

## Proposed fix plan (one version each; preview → approval → publish → verify; v106 stays the rollback)

| Version | Fix | Files |
|---|---|---|
| v107 | B1 Seva help column (prepared) | `site.css` |
| v108 | A1 working header menu 761–1179 px | 12 desktop/tablet boards + `site.css` |
| v109 | B3 phone menu close icon + close behaviour | MenuMobile + `site.css` |
| v110 | B4 home hero buttons ≤ 340 px | `site.css` |
| v111 | B2 Seva form errors into view | Seva, SevaMobile |
| v112+ | C2–C5 (C6–C8 if wanted), single or grouped as the owner prefers | `site.css`, heading tags |
| — | C1 larger photos (trust); D1 after the owner's answer | — |
