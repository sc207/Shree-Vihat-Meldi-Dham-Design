# DEVELOPER_HANDOFF.md — building the real website from this design

_For the developers who will code શ્રી વિહત મેલડી ધામ's website. Written 16 Oct 2026 against design **v123** (`1792090563-62eb`)._
_Everything below was checked against the design files in [`design/project/`](design/project/) (an exact copy of the live design)._

**In one sentence:** build **one responsive page per route** from the desktop design files, keep the two stylesheets and the
page behaviour described here, replace the canvas-only bits listed in §4, and fill the `[square-bracket]` placeholders only with text
the trust supplies.

---

## 1. Where things are

| What | Where |
|---|---|
| Live design (source of truth) | Claude Design artifact `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa` (private to the owner) |
| Exact copy of the design | [`design/project/`](design/project/) (pages, `site.css`, design system, `canvas.json`), checksums in `design/SHA256SUMS.txt` |
| Images | [`design/assets/`](design/assets/) (named by asset id) · manifest with real names, sizes, use and alt text: [`handoff/assets.json`](handoff/assets.json) · export with real names: `python3 tools/export_assets.py --export <folder>` |
| Every text on every page | [`PAGE_CONTENT.md`](PAGE_CONTENT.md) (generated from the pages) — includes the 61 open `[placeholders]` |
| Colours, type, spacing, wording rules | [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) · tokens: `design/project/ds/vihatmeldimandir/tokens.json` |
| What changed when, and why | [`CHANGELOG.md`](CHANGELOG.md) |
| Test tools (reuse them on your build) | [`TESTING.md`](TESTING.md), `tools/`, `tasks/responsive-v116/scripts/` |

**See the design running locally** (Chromium-accurate, with real fonts):
```bash
npm install --prefix work @fontsource/noto-serif-gujarati @fontsource/hind-vadodara
# dc-runtime.js: Artifact read of artifact-type/dc-runtime.js from the design (see NEXT_SESSION.md §8)
python3 tools/serve.py --project design/project --assets design/assets --runtime <dc-runtime.js> --fonts work/node_modules/@fontsource --port 8771
# open http://127.0.0.1:8771/Main.dc.html — resize the window freely; each page is fully responsive
```

## 2. Pages and routes

Gujarati only (`<html lang="gu">`). Suggested routes — names are yours to choose; the design files are the templates.

| Route (suggested) | Build from | Page title / purpose | Phone file (reference only) |
|---|---|---|---|
| `/` | `Main.dc.html` | મુખ્ય પૃષ્ઠ — home, festival summary | `HomeMobile` + `HomeMobile2` (= Main split in two boards) |
| `/darshan` | `Darshan.dc.html` | દર્શન અને યાત્રા — timings, ગાદી days, calendar, travel | `DarshanMobile` |
| `/new-temple` | `NewTemple.dc.html` | નવું મંદિર — સંકલ્પ, architecture, progress | `NewTempleMobile` |
| `/pran-pratishtha` | `PranPratishtha.dc.html` | મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ, 2–8 Feb 2027 | `PranPratishthaMobile` |
| `/seva` | `Seva.dc.html` | સેવા નોંધણી — volunteer registration form | `SevaMobile` |
| `/gallery` | `Gallery.dc.html` | ગેલેરી અને સમાચાર — news + photos (filter, lightbox) | `GalleryMobile` |
| `/history` | `History.dc.html` | મંદિરનો ઇતિહાસ — 7 chapters | `HistoryMobile` |
| `/contact` | `Contact.dc.html` | સંપર્ક — contact, map link, FAQ | `ContactMobile` |
| 404 | `NotFound.dc.html` | પાનું મળ્યું નથી | `NotFoundMobile` |
| offline fallback | `OfflineMobile.dc.html` | shown by a service worker when there is no connection (optional) | — |

In-page anchors used by links: `#main` (skip link) · Home `#darshan` · Darshan `#hours` `#calendar` `#travel` · New Temple `#progress` ·
Festival `#schedule` `#rites` `#nights` · Gallery `#notices` `#photos` · History `#ch1`…`#ch7`. Keep these ids.

### One page per route — the phone files are the same page

Each `…Mobile` file is its desktop page at 390 px. Compared line by line, the **only** differences are:

1. **Festival strip text** (`.vm-notice`): desktop "મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ · તા. ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭", phone "પ્રાણ પ્રતિષ્ઠા મહોત્સવ · ૨–૮ ફેબ્રુ.".
   → put both texts in the markup and show the short one at ≤ 760 px.
2. **Menu button ☰**: desktop/tablet files open an in-page menu panel (`.vm-mnav.vx-tnav`); phone files link to a separate menu page
   (`MenuMobile`) because the design canvas cannot overlay a panel. → **use the in-page panel at every width below 1180 px**
   (it is fully built: dialog, focus kept inside, Escape closes, focus returns to ☰). `MenuMobile` is the visual reference for it on phones.
3. **Festival page banner** (`PranPratishtha` only): the phone file adds the temple picture `<img class="vx-hero-temple">` under the
   buttons (CSS already hides it from 761 px) and shortens one fact label to "પ્રાણ પ્રતિષ્ઠા". → include the image in the one template.

Home: `HomeTablet` (834), `HomeTabletL` (1180) and `HomePhoneL` (844 sideways) are `Main` at fixed widths (identical markup;
`HomePhoneL` adds the class `vx-land`, a canvas stand-in for the real sideways-phone media query — do not ship `vx-land`).

## 3. Styles

Two stylesheets, in this order, are the whole look. Ship both unchanged first; refactor only with visual regression tests (§9).

| File | What | Rule |
|---|---|---|
| `ds/vihatmeldimandir/components/bundle.css` | Design system: tokens as CSS variables (`--maroon`, `--space-lg`, …), components `vm-*` | never edit; override in site CSS |
| `site.css` (~1,650 lines) | Site layer: page components `vx-*` and overrides | built as **dated, commented blocks appended in order**; later blocks override earlier ones — keep the order |

Fonts (Google Fonts): Noto Serif Gujarati (display, 400–700) and Hind Vadodara (body, 400–700), `display=swap`. Self-hosting is fine.

**Breakpoints in use** (the important ones; all are `max-width`/`min-width` on the viewport):

| Range | Layout |
|---|---|
| ≤ 359 / 374 / 389 px | very small phones: stacking tweaks (night cards, home buttons, History index) |
| ≤ 760 px | **phone** layout, bottom action bar `.vx-abar` |
| 761–999 px | tablet portrait; banner pictures move below the text (art column hidden ≤ 999) |
| 1000–1179 px | small laptop; header links still in the ☰ panel |
| ≥ 1180 px | full header navigation (8 links) |
| ≥ 1280 / 1300 px | widest layouts (content max 1320 px, centred) |
| `(orientation: landscape) and (max-height: 500px)` | phones turned sideways: compact banner, no bottom bar |
| `(pointer: coarse)` | touch screens: 44 px touch areas (v123) |
| `(prefers-reduced-motion: reduce)` | every animation off |

Large-text mode: the **અ+** button toggles class `is-big` on `.vm-root` (zooms running text ×1.14) and stores `vx-fs` = `1`/`0` in
`localStorage`. Every component is checked in both sizes.

Scroll effects use CSS only: a gold reading-progress line (`animation-timeline: scroll(root)`) and section reveals (`view()`);
browsers without scroll timelines simply show everything.

## 4. Canvas-only things — remove or replace

| In the design files | In the real site |
|---|---|
| `<div class="vm-root vx-page …" style="width: 1440px; height: 8090px;">` | drop the inline width/height (board frame for the canvas) |
| `<x-dc>`, `<helmet>`, `<script src="./support.js">`, `data-props='{"$preview": …}'` | design-tool wrapper — remove; put `<helmet>` contents in `<head>` |
| `{{binding}}` attributes and text, `<sc-if value="{{…}}">` | template values / conditionals — implement with your framework (see §6 for what each does) |
| `class Component extends DCLogic { … }` | the page's behaviour, written for the design tool's React runtime — port to your code (§6) |
| `src="/_blob/<id>"` | the real image file — names in `handoff/assets.json` |
| `MenuMobile`, `HomeMobile2`, `HomeTablet*`, `HomePhoneL`, class `vx-land` | canvas boards only — see §2 |
| `canvas.json`, frame heights | canvas layout only |
| unused CSS for `.vm-wa-fab` / `.vx-fab` (floating WhatsApp button) | removed from the design in v118; ignore |

## 5. Images

39 files (22 used). Use `handoff/assets.json` for names, sizes, alt texts and where each appears; export them with real names:
`python3 tools/export_assets.py --export public/images`.

- Deity art and portraits sit in the arch frame (`.vm-arch`); cover-cropping rules (`object-position`) are in the pages — keep them.
- Images are single-size today. For production, generate responsive sizes (`srcset`, e.g. 480/960/1440 w) and keep `loading="lazy"`
  below the first screen; add `width`/`height` attributes to avoid layout shift.
- The four ધામ પરિવાર pictures (28–31, v125) are 1200×1500 and already fit the 4:5 arch frame exactly — no cropping needed.
- Three સુરેશબાપા photos were enlarged to exactly 2× in v127–v128 (32, 33, 34; faces checked against the originals). One photo is still a small
  original and looks soft in the photo viewer on high-resolution screens: કરમશીબાપા seated poster 784×1045 (09) — a larger original must come
  from the trust (AI enlargement changed his face, so it was not used).
- Empty `alt=""` = decorative, or the picture is named by the text beside it. Missing photos use the "photo coming soon" tile — never stock photos.

## 6. Behaviour to implement (the `DCLogic` class at the end of each page is the reference implementation)

**All dates and times are Indian Standard Time (UTC+5:30), whatever the visitor's own time zone** (the pages compute
`now + 330 min` and read UTC fields). Numbers are shown in Gujarati digits (૦–૯).

| Where | Behaviour |
|---|---|
| All pages | **અ+ text size** (above). **Menu panel** below 1180 px: `aria-expanded`/`aria-controls` on ☰, `role="dialog" aria-modal`, Tab kept inside, Escape and ✕ close, focus back to ☰. **Skip link** to `#main`. |
| Phone menu (if you keep a menu page) | ✕/Escape go back to the page the visitor came from (Home if opened directly); current page marked with `aria-current`; the page remembers its scroll position (`sessionStorage['vx-menu-y']`, 10 min). With the in-page panel none of this is needed. |
| Home | **Countdown** to 8 Feb 2027 12:39 IST (days; "આવતીકાલે…/આજે…" text on 7–8 Feb; done state after). **Darshan status**: open 06:00–22:00 ("હાલ દર્શન ખુલ્લાં છે" / "દર્શન સવારે ૬ વાગ્યે ખૂલશે"); **next aarti** badge (07:00, 19:00). **Next ગાદી**: Sunday, Tuesday and પૂનમ (`POONAM` list). **Upcoming holy days** from the `EVH` list. **Scrolling strip** with a pause button (`aria-pressed`). Stats count up when shown. |
| Festival | Countdown (days/hours/minutes); **day tabs** 2–8 Feb (the current festival day is preselected during the festival); **live "now / next"** from the `EVT` programme during the festival; add-to-calendar links (Google Calendar URL and an `.ics` data link). |
| Darshan | **Calendar** of the coming પાવન days from the `EV` list (Oct 2026 – Apr 2027) with "આજે" on the Indian date; ગાદી week strip with today marked. (Contact and 404 carry the same `EV` code but show nothing from it — leave it out.) |
| Seva | Form: name (required), mobile (exactly 10 digits), town (required), age, address, optional photo (`accept="image/*" capture="user"`, preview), seva choice (`SEVAS`), day choice (`DAYS` 2–8 Feb), time slot (`SLOTS`), consent (required). On a failed submit: error summary (`role="alert"`), message under each field, `aria-invalid` + `aria-describedby`, **scroll to and focus the first invalid field**; typed values kept. On success: show the confirmation and move focus to its heading. **There is no back end yet** — the trust must decide where registrations go (sheet, e-mail, database); show the thank-you only after the save succeeds. |
| Gallery | Filter chips (with counts) and a **lightbox** (open, caption, close with ✕/Escape). The design's viewer is `position: fixed`, centred, image area ≤ screen height − 176 px; phones full-width photo (v126). Since v131 the design has the full behaviour: focus to ✕ on open (Tab stays inside), Escape or a tap on the dark area closes, focus returns to the photo. |
| Offline page | "ફરી પ્રયાસ કરો" reloads. |

**Countdown refresh:** the design re-renders every second; once a minute is enough (only the seconds-free countdown and status change).

**Date lists to maintain** (`EV`, `EVH`, `POONAM`, `EVT` in the page logic): they end in April 2027 (last પૂનમ listed: 20 Feb 2027).
Move them to one data file in your build and extend them before March 2027 — dates need the Acharya's confirmation.

**Links:** WhatsApp channel `https://whatsapp.com/channel/0029Vb8yWK3DZ4LbUcJhBt3w` · WhatsApp chat `https://wa.me/919909552020` ·
phone `tel:+919909552020` · Instagram `jay_vihat_meldi_ma_dham_sanand` · map `https://share.google/pLcypqU4GO1Zr0I4z` · Facebook: button
hidden until the trust gives the page link. The festival PDF button (`.vx-patrika`) is hidden until the PDF exists — see the comment in `site.css`.

## 7. Accessibility already in the design — keep it

Skip link · landmarks (`header`, `main`, `footer`, `nav`) · one `h1` per page and no skipped heading levels · visible focus ring
(2 px, `--focus`) · menus as proper dialogs · form errors announced and focusable · `prefers-reduced-motion` honoured · large-text
mode · touch areas ≥ 44 px on phones and touch screens · colour pairs from the tokens meet WCAG AA · decorative graphics `aria-hidden`.

## 8. Content rules (from the trust — do not relax)

Gujarati only. Never invent content: every `[square-bracket]` text is a placeholder that stays until the trust supplies the real text
or photo (61 open — list at the end of `PAGE_CONTENT.md`). Keep the approved wording, names, spellings and date format
(`DESIGN_SYSTEM.md` → Gujarati wording). Key facts: festival 2–8 Feb 2027; prāṇa-pratiṣṭhā 8 Feb 2027, 12:39 IST; darshan daily 06:00–22:00.

## 9. Acceptance checks for the build

The design passes all of these (16 Oct 2026, Chromium); the coded site should too:

- No sideways scrolling and no clipped Gujarati at **320–2560 px**, phones sideways included, normal and large text.
- Same look as the design at 390, 768, 1024, 1440 px (pixel compare with `tools/pixel_regress.py`, or screenshots side by side).
- Touch areas ≥ 44 px on phones (`tasks/responsive-v116/scripts/test_tap_areas.py`), menu and form behaviour as in §6
  (`tasks/fixes-1-6/scripts/test_item2.py`, `test_item3.py`, `test_item4.py`).
- Reduced motion stops all animation; keyboard alone can reach and use everything.
- **Still to test (not possible here):** Safari/iPhone, Firefox, real Android and iOS devices, a screen reader (TalkBack / VoiceOver).

`tasks/responsive-v116/scripts/scan_run.py` runs the full device scan (34 sizes × 2 text sizes) against any URL served like the design;
point it at your build to compare.

## 10. Open items that belong to the build, not the design

Seva form back end and privacy notice · countdown refresh (once a minute) · responsive image sizes · `<meta name="description">`, social
preview image, favicon (the logo mark 16/17), `sitemap.xml` · optional service worker for the offline page · analytics (if the trust wants
it) · hosting and HTTPS · extending the date lists · real-device testing. Header: the design system offers a compact fixed header
(`.vm-header.is-scrolled`) but the design keeps the header in the banner (it scrolls away; phones have the bottom bar) — keep it that way
unless the trust asks.
