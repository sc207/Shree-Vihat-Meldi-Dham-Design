# Admin panel — phone design A to Z (17 Nov 2026)

`phone-design.html` is the phone layout for every page, form, sheet and state of the admin panel: 101 screens (96 portrait 390×844, 5 landscape 844×390), groups A–R, with the 13 phone rules at the end. Open it in a browser; on a phone it shows one screen per row.

Why: the built panel (release v11) kept the old page structure on phones, so pages were 4–8 screens long, filter chips wrapped into 3–5 lines and the first row appeared at the bottom of the first screen. This design keeps the v11 colours, fonts, logo and wording and changes only the phone arrangement. Tablet and laptop stay as in the v11 canvas.

- Data, rules, permissions and wording do not change.
- New wording in sheets and chips (for example reasons on chips) needs the owner's approval before it goes into the panel.
- `phone-design-overview.jpg` and `phone-design-landscape.jpg`: all screens at a glance.

Status: design proposal, shown to the owner. Not yet in the Claude Design canvas.

## Revision 2 (17 Nov 2026, after owner feedback "still hard, not professional")
- Calmer look: white cards on a light neutral background, larger text (16 px base, 20 px page titles), one line of detail per row, 52 px buttons and fields, lighter segmented controls.
- Day strip: weekday above the date with the caption "મહોત્સવનો દિવસ · ફેબ્રુઆરી ૨૦૨૭"; counts removed from the boxes (they were unclear).
- Dashboard: only the festival card, "આજે કરવાનું" and four quick actions; charts live in Reports.
- "વિગત સુધારો" is a short menu: photo, name and contact, seva days and time. Photo change by an admin is NEW (needs owner approval and a server change).

## Revision 3 (17 Nov 2026) — after reviewing svmds.onrender.com on a phone
The owner asked to look at the other temple panel (SVMDS) on a phone and fix what our design lacked.
Six patterns were taken from it, the rest of our design was kept:

1. **One stat card, 2×2** replaces every cramped four-across number row (dashboard, registrations,
   padhramni, attendance, capacity planner, invitations, reports). Each cell: soft tinted icon square,
   big number, label.
2. **Detail pages no longer show a raw "label : value" table.** Fact rows (icon + small label + large
   value), a "what is left to do" strip at the top, four quick-action buttons (phone, WhatsApp, Maps,
   calendar) and a dotted **timeline** at the bottom. Applied to registration detail, padhramni detail,
   devotee profile, message detail and the smaller sheets.
3. **Colour**: five soft tints (saffron, green, gold, blue, rose) for icon chips only; maroon stays the
   single strong colour.
4. **One line under the page name** saying what the page is for (main pages only, ~20 px).
5. **"વિગત સુધારો" is now one page** — photo inline with its two buttons, three folded sections
   (name and contact, seva days and time, **registration date and time**), one reason, one save.
   This answers the owner's request that the admin can edit the date and the photo.
6. **Padhramni request form** shows four fields (devotee, date, time, purpose); place/Maps and
   note/contact are folded, with a one-line summary next to each fold. Sort was added to the
   registration filter sheet; list pages get a round "+" button bottom right.

Checked: all 101 screens render with no overflow and no console errors (Playwright, 390×844 and
844×390). `phone-design-before-after.jpg` shows six screens before (v4) and now (v5).
`generate.py` is the script that produces the HTML.

Still open for the owner: new wording in the new strips and folds, and whether an admin may edit a
registration's date — both need approval before they go into the panel.

### Revision 3.1 — full audit pass (18 Nov 2026)
Every one of the 101 screens was measured in the browser, not just looked at:
- vertical overflow: none; sideways page scroll: none
- tab and filter strips now really scroll sideways (`overflow-x:auto`); before they were cut off by
  `overflow:hidden`, which contradicted rule 2
- all text on a screen is at least 12 px. Raised: the group label in the top bar, the bottom-bar labels,
  the weekday in the day strip, list second lines, quick-tile labels, summary lines, the calendar
  weekday header and the "નવું" tag. Exceptions on purpose: the red count badge (11 px), level badges
  (11.5 px) and the printed ID card, which is a 54x86 mm card and not a screen.
- touch targets: every tappable row, button, chip, tab and nav item is 40 px or more. The switch graphic
  is 30 px but sits inside a 70 px row that is tappable as a whole; status pills are not tappable.
- no script errors. The file loads its Gujarati fonts from Google Fonts, so it needs internet to look
  right; nothing else is fetched.

### Revision 3.2 — card preview shows both sides (18 Nov 2026)
The owner asked for the older behaviour back: the v11 design showed the ID card's front and back
together, and that read better than a front/back switch.
- «કાર્ડ પ્રિવ્યૂ» now shows both cards side by side, 170x271 each, labelled આગળ and પાછળ, with the
  back carrying the festival dates and the website QR. The આગળ/પાછળ segmented control is gone.
- The same pair shows behind the «કાર્ડ સોંપ્યું?» and «કાર્ડ ફરી છાપવું?» sheets, which used to sit
  on an empty screen.
- Bug found while doing it: the design system already uses `.back` for the round back-arrow button
  (display:grid, 44x44), so a card marked `.idcard.back` lost its flex column and its header and
  footer band shrank. The card class is now `.idcard.bk`. Worth knowing for the build: do not reuse
  `back` as a modifier.

### Revision 3.3 — the preview uses the real v11 card (18 Nov 2026)
The owner asked for the actual card from the repo, not a redrawn one. `admin-panel/master/id-card/
front-3x.png` and `back-3x.png` are scaled to 360 px wide (`card-front.jpg`, `card-back.jpg`, beside
`generate.py`) and embedded in the preview, so the screen shows the approved artwork: mandala, the
મંગલારોહણ wordmark, the arched photo frame, the gold volunteer pill, the maroon footer band with the
SEVA number and the QR, and on the back the festival dates and the website QR.
The card art names અંકિત શાહ / SEVA-000060, so the three card screens now name the same volunteer.
The file is 666 KB because of the two embedded pictures.

### Revision 3.4 — how a registration record is shown (18 Nov 2026)
After going through all ~73 screenshots in the Zoho People mobile guide (help.zoho.com, mobile app
guide), three of their patterns were taken for the registration screens. Their look was not copied:
the panel stays maroon and cream.
- **Key facts first.** Zoho opens a record with a small block of its decisive values (First In, Last
  Out, Overtime, Total). «નોંધણીની વિગત» now opens with the person card and a 2x2 block:
  ઉપલબ્ધતા ૨ દિવસ · સેવા ફાળવણી બાકી · WhatsApp સંદેશ ગયો · ઓળખકાર્ડ બાકી.
- **The four things you do with a person, as buttons**, not as list rows: ફોન · WhatsApp · ખાનગી ·
  ઓળખકાર્ડ. The long «label : value» table is gone; only ઉપલબ્ધતા stays as a fact row, because the
  chips show which days.
- **The row's own action inside the row.** Zoho puts ✓/✕ on an approval row. A registration whose
  status is «નવી» now carries a «સ્વીકારો» button in the row itself, in the list and on the dashboard.
Not copied: their empty cards that still take space ("No Birthdays today!"), three stacked rows of
navigation before the content starts, and the dark theme.

### Revision 3.5 — login, mandala, final check (18 Nov 2026)
- **Login rebuilt for the phone.** The maroon head runs edge to edge with a soft mandala behind the
  logo, the temple name, «એડમિન પેનલ · સાણંદ» and a gold line «મંગલારોહણ · ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭».
  The form sits in a white card that overlaps the head by 22 px, and the screen closes with
  «જય શ્રી વિહત મેલડી ધામ» in gold. All five login screens (sign in, code, wrong password,
  recovery code, lost password) use it.
- **Mandala, lightly.** One SVG (about 1 KB, drawn in `generate.py`, not a picture) is used three
  times: behind the login head (14% white), top right of the festival card on the dashboard (13%
  white) and behind every empty state (7% maroon). Never behind running text.
- **Final measured check of all 101 screens**: no overflow, no sideways scroll, every tappable row,
  button, chip and tab at least 40 px, on-screen text at least 12 px (count badges and the printed
  ID card excepted), no script errors.

### Revision 3.6 — the website's own mandala (18 Nov 2026)
The hand-drawn mandala was replaced with the real one the website and the ID card use:
`public/media/mandala.*.svg` from the website repo, copied here as `mandala.svg` (24 KB) and
embedded by `generate.py`. It is used as a CSS mask, so one copy serves all three places and each
can take its own colour: white at 17% behind the login head, white at 16% on the dashboard festival
card, maroon at 10% behind every empty state. Still never behind running text.

### Revision 3.7 — the login screen rebuilt again (18 Nov 2026)
The owner did not like the first attempt (a maroon strip over a mostly empty cream screen), so the
login is now one piece:
- the whole screen is a maroon gradient; the website's mandala sits behind the logo at 16% white and
  the new temple render (`14_temple_new-temple-render.webp`, reduced to a 640 px alpha mask,
  `temple-mask.png`) rises from the bottom edge at 15.5% white
- ॥ જય શ્રી વિહત મેલડી માઁ ॥ in gold above the logo, the temple name, «એડમિન પેનલ · સાણંદ», and
  «મંગલારોહણ · ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭» under a thin gold rule
- the form sits in a near-white card with a deep shadow, and «જય શ્રી વિહત મેલડી ધામ» closes the
  screen in gold
All five login screens use it. No overflow; the file is 770 KB with the two card pictures, the
mandala and the temple mask embedded.

### Revision 3.8 — «ઝડપી નજર», and the list row that finally fits (18 Nov 2026) — FINAL
- **One button per row shows the whole record.** Every row that carries a SEVA number has a round
  eye button on the right; it opens the «ઝડપી નજર» sheet: photo, name, SEVA number, village,
  mobile, status, availability chips, seva and team, and two buttons — «પૂરી વિગત ખોલો» and
  «સ્વીકારો». The sheet says in one line that the photo and the full mobile are private and that
  looking at them is written to the audit.
- **The row was rebuilt to make room for it**: the name now has the full width on its own line, and
  the SEVA number, the status pill and any time sit on the second line, the number truncating first.
  Before this the name was cut after about twelve letters.
- The inline «સ્વીકારો» button from revision 3.4 was removed: the quick view carries it now, and
  the row stayed readable.
- 102 screens (one new), all measured: no overflow, no sideways scroll, 40 px targets, 12 px text,
  no script errors.
