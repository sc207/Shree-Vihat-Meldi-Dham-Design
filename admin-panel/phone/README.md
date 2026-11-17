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
