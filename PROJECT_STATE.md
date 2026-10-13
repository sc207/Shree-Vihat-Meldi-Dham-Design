# PROJECT_STATE.md

_Last updated: 10 Oct 2026, evening IST (audit Phases A–C reported). Update this file only when the project state meaningfully changes._

## Versions

| | Version | Id | Verified |
|---|---|---|---|
| **Live (published) design** | **v109** | `1791922103-42cb` | 14 Oct 2026: banner gold light and halo drawn in the picture's own box (`site.css` only); read back byte-identical to `design/project/site.css`. Owner asked for the fix directly. |
| v108 | v108 | `1791920313-6e1c` | 14 Oct 2026: new chakra everywhere (9 boards). Rollback target for v109. |
| v107 (artifact's own count) | v106 content | `1791918685-cd89` | 13 Oct 2026: a re-save (Design type update / editor open), **no content change**. Rollback target for v108 (= v106 content). |
| v106 | v106 | `1791624520-9b52` | 10 Oct 2026: 28/28 project files identical to the snapshot of that day. |
| Visual-effects work | — | — | Owner's brief [tasks/visual-effects-audit.md](tasks/visual-effects-audit.md): glow fixed in v109, old chakra replaced in v108. Remaining sweep items: see Outstanding tasks. |
| Local working version | **Items 1–6 on v109 (unpublished)** | — | Saved 14 Oct in [tasks/fixes-1-6/](tasks/fixes-1-6/): final copy `project/`, per-item patches and scripts, report, pictures, test logs. Seva column, tablet menu, Seva form errors + confirmation, phone menu ✕/closing, Home buttons <375 px, polish 6.1–6.5. All checks pass in Chromium (REPORT.md). **Publishing needs the owner's separate approval.** |
| Older rollback | v107 / v106 content | `1791918685-cd89` | Any earlier version is in the artifact's history (list in [CHANGELOG.md](CHANGELOG.md)). Version numbers follow the artifact's own count from v107 on. |
| Spec / review page | v16 | `1791922379-dd2c` | `https://claude.ai/artifact/XzsLf5Ef672Cwr1i9QDJNW` — records v97–v109 (new section "Banner light & chakra"); source + new pictures in `tasks/spec-page/` |
| Audit report page | v2 | `1791922345-463b` | `https://claude.ai/artifact/FJjnL8j4NB95mK2tcSjQuU` — audit of v106 + status after v108/v109; source `tasks/audit-v106/audit-page.html` |

Website artifact: `https://claude.ai/artifact/HWR4J5u9qBPjri6oUg7nVa` (type Design, `https://claude.ai/artifact/QKN21svewxgyPb6SYRqWnd`).

## Git

- Repository: `https://github.com/sc207/Shree-Vihat-Meldi-Dham-Design`, branch `main`.
- The handover is on GitHub (`main` at `1abec84`, 10 Oct). Later commits are pushed only when the owner says so; check `git status -sb` for unpushed work.
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
2. **Seva desktop:** empty right column — fix prepared as v107 (see Versions), **awaiting approval**.
   **Design audit v106 (Phases A–C):** done, no changes made — report [tasks/audit-report-v106.md](tasks/audit-report-v106.md)
   (page: `https://claude.ai/artifact/FJjnL8j4NB95mK2tcSjQuU`). 0 P0, 1 P1 (A1 header menu 761–1179 px), 4 P2, 9 P3, 1 owner decision (D1 hero).
   Phase D waits for the owner's approval; proposed order v107 Seva → v108 A1 → v109 B3 → v110 B4 → v111 B2 → polish.
3. **Spec page:** up to date with v109 (14 Oct). Add each new version there after publishing.
4. **Figma Gate A:** when the allowance returns — one read-only check first; if blocked, stop. Then run `figma/scripts/call1.js` … in order
   (see `figma/state.json` → `run_order`), after the owner drops the 26 original images (original filenames) onto the Components page.
   Then sync Figma with website changes v99–v106 (`figma/state.json` → `figma_sync_todo`; the scripts already contain the v97 Gate A design).
5. **Before the March 2027 પૂનમ:** extend the date lists — `const EV` (Darshan, Contact, NotFound + phone pages) and `const EVH` + `const POONAM`
   (Main, HomeTablet, HomeTabletL, HomePhoneL, HomeMobile). Last પૂનમ listed: 20 Feb 2027; calendars end 15 Apr 2027. Dates need the Acharya's confirmation.

## Owner's decisions and task queue (10 Oct 2026, end of the handover session)

Decided:
- **No extra closing line in the સંકલ્પ section.** Do not add "જય શ્રી વિહત મેલડી માતાજી!" there; the page's site-wide closing line
  "॥ જય શ્રી વિહત મેલડી માઁ ॥" (devotional band) stays the only one. Nothing to change.
- **Correct the canvas to-do note about the PDF button** — approved. The line currently reads
  `• કાર્યક્રમ પત્રિકાની PDF — "કાર્યક્રમ પત્રિકા (PDF)" બટન તૈયાર છે, લિંક મૂકવાની બાકી` although the button has been hidden since v102.
  Reword it to say the button is hidden until the PDF arrives (change `project/canvas.json` → `notes.todo.text` only; no page changes).
  Show the new wording to the owner before publishing it as its own version.

Task queue, one small task at a time (owner's order):
1. **Seva page, desktop: fix the empty right column** — prepared (v107 preview), awaiting approval.
2. **Canvas to-do note:** the PDF line correction above.
3. **Complete design audit** — owner's brief in [tasks/full-design-audit.md](tasks/full-design-audit.md); phases A–C end in a report to the owner, fixes follow
   in small approved versions. Phases A–C done (report: [tasks/audit-report-v106.md](tasks/audit-report-v106.md)); waiting for the owner's answers and approval.
4. Trust content as it arrives (placeholders stay until then). **Never invent** temple history, construction dates, festival details or any
   other trust-approved information.

Standing note for later: when the PDF exists, link the file in the button, delete the "Festival PDF button hidden" rule
`.vm-root .vx-patrika { display: none !important; }` in site.css (its comment explains the restore), put "અને પત્રિકા" back in the invitation note,
and update the canvas to-do note again.

## Known issues / limitations

- **Canvas only:** boards are capped at 8000 px, so the bottoms of long boards are not visible in the canvas (the real pages are fine).
- **Canvas only:** frames are sized for ordinary days. In festival week (countdown/day cards) the Festival and Home phone boards can be up to ~150 px
  taller than their frame; the Darshan phone board can be ~8 px taller on dates when the calendar list wraps differently. Real pages have no fixed height.
- Contact and 404 pages compute a local weekday in their logic but never display it (harmless; left unchanged).
- Seva form: no save destination yet (front-end only).
- Audit findings A1, B2–B4, C1–C9 and decision D1 are open — see [tasks/audit-report-v106.md](tasks/audit-report-v106.md).
- Figma: C3 navigation built but not visually verified; C4–C8 specified, not built.
