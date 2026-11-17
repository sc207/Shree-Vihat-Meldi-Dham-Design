# PROMPT for Claude Code — build the phone design A to Z

```
Phone redesign of the admin panel. Design source: design repo sc207/Shree-Vihat-Meldi-Dham-Design, branch admin-panel-design, folder admin-panel/phone/ (latest commit on that branch, "revision 4.0"): phone-design.html (103 screens, groups A–R, 18 phone rules at the end), plus phone-design-overview.jpg (all 98 portrait screens), phone-design-landscape.jpg (the 5 landscape screens), phone-design-before-after.jpg, registration-before-after.jpg, registration-day-stats.jpg and README.md. Read the whole HTML first, including the 18 rules at the end, and README.md, whose revision 3.0 to 4.0 entries say what changed and why.

Work on a new branch feature/phone-ux from the latest release code (include feature/whatsapp-templates-v2 if it is merged; otherwise from 87b0f23). Read CLAUDE.md, STATUS.md and docs/FINAL_REPORT.md first.

SCOPE
- Phones only: portrait up to 699 px wide, and landscape phones (height up to 500 px). Tablet (700 px and up, taller than 500 px) and laptop must not change: prove it with before/after screenshots at 834, 1194 and 1440 (pixel difference ~0).
- Layout and presentation only. No change to data, business rules, permissions, endpoints, migrations or flags. If a screen in the design needs data the API does not give, leave that part out and list it.
- Gujarati wording: use the panel's existing strings. Where the design shows a NEW string (sheet titles, reason chips such as «બીમાર», «ખોવાયું», short notes), do not ship it silently: collect every new string in docs/PHONE_NEW_WORDING.md for my approval, and until approved use the existing wording or control (for example keep the reason as a text field).

RULES TO APPLY ON EVERY PAGE (the design file lists 18; the first five, A-E, are the newest and matter most)
A. One stat card per page, 2x2, with a soft tinted icon square in each cell. Never four small boxes in a row.
B. Detail pages: no «label : value» table. Fact rows (icon + small label + large value), a one-line «what is left to do» strip at the top, four quick-action buttons (phone, WhatsApp, Maps, calendar) and a dotted timeline at the bottom.
C. Forms show three or four fields; the rest sits in folded sections whose heading says what is inside. One reason, one save.
D. One line under the page name saying what the page is for (main pages only).
E. A round «+» button bottom right on list pages (registrations, padhramni, devotees, seva, teams); then no «+» in the top bar.

The thirteen original rules follow in the file:
1. Top bar: temple logo on the left on main pages, back arrow on inner pages; page name in the bar with the small group label above it. No separate large page title, no subtitle sentence, no «અ+» in the bar on phones (move text size to «મારું ખાતું»).
2. Section tabs and filters: one line each; a long row scrolls sideways inside itself (the page never scrolls sideways). No chips wrapping into several lines.
3. The first list row is visible in the top half of the first screen; the header area is at most about 220 px.
4. Lists use compact rows (56–76 px): name, one or two short lines, status. Full detail opens as a full-screen page with the main action fixed at the bottom.
5. No page longer than about 3 screens: use collapsed sections with a one-line summary (dashboard, registration control, Control Centre, reports, settings, team page).
6. One shared day strip (2–8 Feb, seven boxes in one line) everywhere: registrations, attendance, planner, team, Control Centre days.
7. One dark primary button per screen, full width, 48 px, at the bottom; destructive actions red; other actions as a list.
8. Forms in one column, 46 px fields.
9. Confirmations and small forms as bottom sheets whose buttons are always visible, also with the keyboard open and in landscape.
10. The selection bar appears only after something is selected.
11. Long explanations move to a separate «સમજૂતી» page or sheet.
12. Landscape phone: left rail with icon and label; filters in the top bar; lists in 2 columns; detail and confirmation split left/right so the buttons are visible without scrolling.
13. Touch targets at least 44 px, text at least 12 px, status never by colour alone.

ORDER (one local commit per group, report after each batch of 3 groups)
shell and top bar with logo → «વધુ» menu → dashboard → registrations (list, filter sheet, select mode, detail, sheets) → registration control → Control Centre → attendance and QR → Padhramni → ID cards → teams and planner → seva list → WhatsApp and invitations → devotees → groups → reports → settings, users, audit, my account → login screens → states (loading, empty with logo, error, no permission, offline, session, toast) → landscape.

AFTER EACH GROUP
- Full npm test and the related browser scripts (update selectors where the markup changed, never weaken a check).
- Playwright screenshots at 390×844 and 844×390 next to the matching design screen; list remaining differences.
- At 390 and 844×390: no sideways page scroll, targets ≥ 44 px, axe 0, console errors 0. Page height at 390 for dashboard, registration list (first screen), Control Centre, reports: report the number.
- Check with roles sa, ad, rm, tc, vw that nothing appears without permission.
- Unchanged-tablet/laptop proof at 834, 1194, 1440.

FOUR THINGS THE OWNER ASKED FOR, BESIDES THE LAYOUT
1. «ઝડપી નજર» (quick view). Every row that carries a SEVA number gets one round eye button on the
   right. It opens a bottom sheet with the photo, name, SEVA number, village, mobile, status, the
   availability chips and the seva/team line, and two buttons: «પૂરી વિગત ખોલો» and «સ્વીકારો».
   The photo and the full mobile are private: show them only to a role that may see them, write the
   «who looked, when» audit row exactly as the existing «ખાનગી વિગત બતાવો» flow does, and keep the
   masked form for every other role. No new endpoint: use what the detail view already returns.
2. **Photos in the list, behind a switch.** The row avatar is the person's initial by default. A
   «ફોટો સાથે યાદી» switch (filter sheet, and on the attendance and ID-card screens) turns the
   avatars into the volunteer's photo. Rules: only a role that may already see private details;
   serve a small thumbnail, never the stored 800 px photo; write ONE audit row when the switch is
   turned on («ફોટો સાથે યાદી જોઈ»), not one per devotee; the switch is off again on the next visit.
   This is what makes a person identifiable at the gate, so it matters most on હાજરી and ઓળખકાર્ડ.
3. WhatsApp daily limit. Confirm — do not rebuild — that when the 200-message rolling 24 h budget is
   full, a registration message STAYS pending and goes out by itself when the window frees up
   (server/wa-outbox.js refuses the reservation, writes last_error and leaves state='pending';
   tests/wa-outbox.test.js "with a cap of 3 only 3 of 5 messages go out, the rest wait"). What is
   missing is only in the panel: the queue shows the raw English reason. Show «મર્યાદા ભરાઈ —
   સંદેશ કતારમાં રાહ જુએ છે» with the time the oldest unit leaves the 24 h window, and add the same
   line to the WhatsApp dashboard. Collect that wording in docs/PHONE_NEW_WORDING.md for approval.
4. **One shared list header, with the chosen day's counts.** The seven festival days (૨–૮ ફેબ્રુ.)
   are one component used by every list that is read per day — the registration list AND the photo
   list, not only the registration list as before. Under the chosen date sits a strip of five equal
   columns for that day: મળી / સ્વીકારી / નવી / સમીક્ષા / રદ, the figure large, the word under it,
   a coloured top edge as decoration only (the word always carries the meaning, rule 13). It must
   fit 390 px with no sideways scroll.
   Data: these are counts of that day's registrations by status. If the list endpoint does not
   already return them, do NOT add an endpoint — derive them from the rows the page already has
   and say so in the report, or list it as a data gap. Never a second round trip per day box.
   In the row, the second line is «SEVA-000018 · ગામ», not the dates: the day strip above already
   says which day is shown. The village truncates first and the SEVA number never does.

AT THE END
docs/PHONE_UX_REPORT.md: every design screen (A1…R5) with status done / partly / left out and why, the test results, the new-wording list, and a single file phone-after.html with all phone screenshots (same format as phone-review.html) so I can review. Short summary in simple Gujarati.
Local commits only. Push, production migration and deploy only after my separate «ha».
```
