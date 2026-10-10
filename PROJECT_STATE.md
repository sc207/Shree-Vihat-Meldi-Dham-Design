# PROJECT_STATE.md

_Last updated: 10 Oct 2026, ~15:30 IST (handover). Update this file only when the project state meaningfully changes._

## Versions

| | Version | Id | Verified |
|---|---|---|---|
| **Live (published) design** | **v106** | `1791624520-9b52` | 10 Oct 2026: 28/28 project files identical to `design/project/`; 26/26 images identical to `design/assets/` (artifact checksums) |
| Local working version | — | — | No unpublished work. Last working copy = v106. |
| Rollback | v105 | `1791622143-5d00` | Any earlier version is in the artifact's history (list in [CHANGELOG.md](CHANGELOG.md)). |
| Spec / review page | v15 | `1791622167-aaa6` | `https://claude.ai/artifact/XzsLf5Ef672Cwr1i9QDJNW` — records v97–v105 (v106 not yet added) |

Website artifact: `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa` (type Design, `https://claude.ai/artifact/QKN21svewxgyPb6SYRqWnd`).

## Git

- Repository: `https://github.com/sc207/Shree-Vihat-Meldi-Dham-Design`, branch `main`.
- At handover the remote was **empty**. The handover commit was made locally in the old session's workspace (`git log` shows it once pushed);
  pushing waits for the owner to link GitHub to Claude and say "push". If that workspace is gone before the push, the same content is in the
  handover ZIP the owner downloaded — unzip it and push/upload it.
- There was no earlier Git history: the project lived only in the Claude Design artifact and a temporary session workspace.

## Completed (10 Oct 2026)

| Version | What |
|---|---|
| v97 | Gate A preview fixes applied to the website (phone festival banner, page strips, year never split, Karamshibapa portrait restored, …) |
| v99–v100 | Every content page ends WhatsApp band → devotional band → footer; Seva shift cards; compact ivory WA band on phones |
| v101 | Home page reduced to a festival summary (−1,175 to −1,823 px per board) |
| v102–v103 | Festival "કાર્યક્રમ પત્રિકા (PDF)" button hidden until the PDF exists; invitation note without "અને પત્રિકા" |
| v104 | Darshan timetable: 8 identical day rows → one daily timeline + one ગાદી week strip; tablet no longer scrolls sideways |
| v105 | "આજે" follows the Indian date; on પૂનમ days it marks the પૂનમ tile |
| v106 | Trust text "નવા મંદિરનો સંકલ્પ" placed on New Temple (3 paragraphs), Home (2-sentence teaser), History ch. 6 (1 sentence) |

## Files changed in the latest work (v106)

`project/NewTemple.dc.html`, `NewTempleMobile.dc.html`, `Main.dc.html`, `HomeTablet.dc.html`, `HomeTabletL.dc.html`, `HomePhoneL.dc.html`,
`HomeMobile.dc.html`, `History.dc.html`, `HistoryMobile.dc.html`, `site.css` (appended block `.vx-prose` / `.vx-sk`), `canvas.json`
(HomeMobile h 5083 → 5249; to-do note no longer lists the સંકલ્પ text).

## Board frames (v106)

Root height = natural content height + 3 px at the tallest daily time; canvas `h` = min(frame, 8000).

| Board | Width | Frame (root height) | Canvas h |
|---|---|---|---|
| Main | 1440 | 8090 | 8000 |
| HomeTablet | 834 | 10804 | 8000 |
| HomeTabletL | 1180 | 8192 | 8000 |
| HomePhoneL | 844 | 9092 | 8000 |
| HomeMobile | 390 | 5249 | 5249 |
| HomeMobile2 | 390 | 5750 | 5750 |
| NewTemple | 1440 | 8647 | 8000 |
| NewTempleMobile | 390 | 11846 | 8000 |
| PranPratishtha | 1440 | 10190 | 8000 |
| PranPratishthaMobile | 390 | 13824 | 8000 |
| Seva | 1440 | 3314 | 3314 |
| SevaMobile | 390 | 6127 | 6127 |
| Gallery | 1440 | 7907 | 7907 |
| GalleryMobile | 390 | 10455 | 8000 |
| History | 1440 | 8129 | 8000 |
| HistoryMobile | 390 | 10511 | 8000 |
| Contact | 1440 | 4345 | 4345 |
| ContactMobile | 390 | 5402 | 5402 |
| Darshan | 1440 | 5030 | 5030 |
| DarshanMobile | 390 | 7090 | 7090 |
| NotFound | 1440 | 1668 | 1668 |
| NotFoundMobile | 390 | 2520 | 2520 |
| MenuMobile | 390 | 844 | 844 |
| OfflineMobile | 390 | 844 | 844 |

MenuMobile and OfflineMobile are phone-screen boards (fixed 844 px), not content-sized.
(`python3 tools/frame_heights.py --port <p> --project design/project` prints the exact current values.)

## Outstanding tasks

1. **Trust content** — 61 placeholders (end of [PAGE_CONTENT.md](PAGE_CONTENT.md)). Latest request (New Temple): સ્થપતિ name, સંકલ્પ વર્ષ,
   આયોજન detail, construction progress, expected completion; optional dated સંકલ્પ story for History ch. 6.
   Other open items from the canvas to-do note (`canvas.json` → notes.todo): ગેપ્પરા spelling confirmation, Facebook link (button hidden), ભાગવત કથાકાર name,
   યજ્ઞશાળા/ભોજનશાળા location, યજ્ઞ પૂર્ણાહુતિ time, ગાદી on 2 and 7 Feb during the festival, place of શ્રી લાખણેચી માઁ and શ્રી ગોગા મહારાજ in the
   ધામ family, પૂનમ dates and 8 Feb tithi (Acharya), ten નક્ષત્ર on the pillars, deity introductions and પ્રાગટ્ય story, લોક ડાયરો/રામ કથા times,
   artists of 5 Feb ડાયરો and 8 Feb રમેલ and the spelling of their names, artist photos (with permission), arrival/parking instructions,
   authoritative temple history and both Bapas' introductions, dated construction photos and real festival photos, the પત્રિકા PDF, dress code,
   the trust's registered name. (The note still says the PDF button is "તૈયાર છે"; it has been hidden since v102 — reword the note if the owner wants.)
2. **Seva desktop:** empty right column (design audit item, not started).
3. **Spec page:** add v106 to `https://claude.ai/artifact/XzsLf5Ef672Cwr1i9QDJNW` when convenient (optional; it currently ends at v105).
4. **Figma Gate A:** when the allowance returns — one read-only check first; if blocked, stop. Then run `figma/scripts/call1.js` … in order
   (see `figma/state.json` → `run_order`), after the owner drops the 26 original images (original filenames) onto the Components page.
   Then sync Figma with website changes v99–v106 (`figma/state.json` → `figma_sync_todo`; the scripts already contain the v97 Gate A design).
5. **Before the March 2027 પૂનમ:** extend the date lists — `const EV` (Darshan, Contact, NotFound + phone pages) and `const EVH` + `const POONAM`
   (Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile). Last પૂનમ listed: 20 Feb 2027; calendars end 15 Apr 2027. Dates need the Acharya's confirmation.

## Pending decisions (owner)

- Whether to add "જય શ્રી વિહત મેલડી માતાજી!" at the end of the સંકલ્પ section (left out in v106 because every page already ends with "॥ જય શ્રી વિહત મેલડી માઁ ॥").
- When the PDF exists: link the file in the button, delete the "Festival PDF button hidden" rule `.vm-root .vx-patrika { display: none !important; }`
  in site.css (its comment explains the restore), and put "અને પત્રિકા" back in the invitation note.

## Known issues / limitations

- **Canvas only:** boards are capped at 8000 px, so the bottoms of long boards are not visible in the canvas (the real pages are fine).
- **Canvas only:** frames are sized for ordinary days. In festival week (countdown/day cards) the Festival and Home phone boards can be up to ~150 px
  taller than their frame; the Darshan phone board can be ~8 px taller on dates when the calendar list wraps differently. Real pages have no fixed height.
- Contact and 404 pages compute a local weekday in their logic but never display it (harmless; left unchanged).
- Seva form: no save destination yet (front-end only).
- Figma: C3 navigation built but not visually verified; C4–C8 specified, not built.
