# Shri Vihat Meldi Dham — Admin Panel: final design handoff

> **ગુજરાતીમાં ટૂંકમાં:** આ ફોલ્ડર Claude Code ને આપો અને કહો: *"README-FOR-CLAUDE-CODE.md વાંચીને હાલની એડમિન પેનલને આ ડિઝાઇન મુજબ બનાવો. Route, પરવાનગી અને backend બદલશો નહીં."* બધી સ્ક્રીન જોવા માટે `index.html` ખોલો.

This folder is the **approved visual design** for the existing admin panel of shreevihatmeldidhamsanand.com (Phase C, "Menu C"). Use it to restyle and restructure the **existing** admin panel. It is a design reference, not a new product spec.


**Source of truth:** Claude Design canvas "શ્રી વિહત મેલડી ધામ — એડમિન પેનલ · સંપૂર્ણ ડિઝાઇન" — `https://claude.ai/artifact/LryATCfbrsGsyoKwr76pJ5` (copied from the Phase C canvas `https://claude.ai/artifact/URpVXVJtjKGwBACDK3jDuv`, version 1793904868-72ad, incl. the volunteer ID card). This folder is a snapshot of it (2026-11-06). The public website design in `../design/` is separate and must not be changed by admin work.

---

## 0. Hard rules (read first)

1. **Do not change behaviour.** Keep every existing route, API call, permission check, role, database field, validation rule and backend job exactly as it is in the codebase. This design changes *layout, navigation grouping, wording and visual style* only.
2. **Do not invent features.** Where the design shows something the codebase does not have, skip it and list it in your final report. Many boards carry the note **"ચકાસણી બાકી"** (= "to be verified against the current system"). Treat each one as: *implement only if the current code already supports it.*
3. **All data in the design is sample data.** Names, phone numbers, counts, dates and the "ઉદાહરણ" (example) badges are placeholders. Wire every value to the real data the current code already loads. Never ship the sample values.
4. **Drop design-only annotations.** Board titles such as "નોંધણી યાદી · ડેસ્કટોપ · 1440", the "ઉદાહરણ / ઉદાહરણ — સાચી માહિતી નથી" pills, the grey "(ઉદાહરણ ભૂલ)" notes and review captions are for reviewers. They are not part of the UI.
5. **નિયંત્રણ કેન્દ્ર (Control Centre) is not part of this release.** It is a future proposal and is intentionally absent from the menu.
6. **WhatsApp:** the design shows real sending as **off / not connected**. Do not enable sending or add new sending paths. Keep whatever the current code does, and keep its safeguards (super-admin only, server credentials required).
7. **Do not touch** the public website, production data, Render/Turso config or secrets as part of this work.

---

## 1. What is in this folder

| Path | What it is | How to use it |
|---|---|---|
| `index.html` | Gallery of every screen and state, grouped by page | Open in a browser to browse |
| `shots/*.jpg` | Screenshot of each board at its design size | Visual target |
| `html/*.html` | **Static rendered HTML** of each board (real DOM + classes) | Best source for markup structure and Gujarati copy |
| `assets/phc.css` | The complete admin stylesheet (tokens + all `p-*` / `ov-*` classes + media queries) | **Use as the base stylesheet.** Port it into the app |
| `assets/fonts.css`, `assets/fonts/` | Hind Vadodara + Noto Serif Gujarati (self-hosted woff2) | Or load the same two families from Google Fonts |
| `assets/emblem.png`, `emblem-small.png` | Temple emblem used in sidebar/login | Use the app's existing emblem asset if it already has one |
| `source/*.dc.html` | Editable design sources. `renderVals()` in each file shows the data shape each screen expects | Read when you need to know which fields a screen shows |
| `SCREENS.md` | Inventory of all 449 boards: file → size → title | Checklist |

File naming:
- `V-<Screen>-<size>` = a full page at one screen size.
- `I-<Screen>-<state>-<size>` = an interaction state: popup, drawer, filter sheet, confirm dialog, loading, empty, error, saved toast.
- `<Screen>` without prefix = the page component itself (`Regs`, `DashC`, ...). `Shell` = the app frame. `Ov*` = shared overlays. `St*` / `States` = shared loading/empty/error patterns.
- Sizes: `D1440` desktop · `L1366` laptop · `TL1024` tablet landscape · `TP834` tablet portrait · `M390` phone · `M320` small phone · `ML844` phone landscape 844×390 · `ML667` small phone landscape 667×375.

---

## 2. Design tokens (from `assets/phc.css` `:root`)

| Token | Value | Use |
|---|---|---|
| `--maroon` | `#741A32` | Primary buttons, links, active text |
| `--maroon-deep` | `#5C1227` | Hover |
| `--burgundy` | `#481022` | Sidebar, login background |
| `--gold` / `--gold-soft` / `--gold-ink` | `#B78A35` / `#E2C27A` / `#86621F` | Hairlines, accents; `gold-ink` for readable gold text on light |
| `--ivory` / `--cream` / `--raised` | `#FBF7EF` / `#F2E6D2` / `#FFFDF8` | Page, alt surface, cards |
| `--ink` / `--muted` | `#29272A` / `#675A51` | Text |
| `--line` / `--line-strong` | `#E4D6BE` / `#9C8A73` | Borders / control borders |
| `--focus` | `#B25E12` | 3px focus ring |
| `--success` / `--ok-bg` | `#1F5F5B` / `#E3F1EF` | "ચાલુ", "સમીક્ષા થઈ", "પહોંચ્યો" |
| `--danger` / `--danger-bg` | `#B03A1E` / `#FBE7E1` | "રદ", errors, destructive confirm |
| `--warn-ink` / `--warn-bg` | `#7A4A0E` / `#FBEFD6` | "બાકી", work-first cards |
| `--info-ink` / `--info-bg` | `#1F4E79` / `#E5EEF7` | "નવી", info |
| `--off-ink` / `--off-bg` | `#5A524C` / `#EFEAE3` | "બંધ", disabled |
| `--display` | Noto Serif Gujarati | Page titles, brand, big numbers |
| `--body` | Hind Vadodara | Everything else, 15px / 1.55 |

---

## 3. App shell and navigation ("Menu C")

The shell is in `source/Shell.dc.html` and is visible in every `V-*` board.

**Desktop sidebar (burgundy, 256px):** brand (emblem + "શ્રી વિહત મેલડી ધામ / એડમિન પેનલ"), then:

1. આજનું કામ → `#/dashboard`
2. નોંધણી → `#/registrations` (tabs: નોંધણી યાદી · ઓળખકાર્ડ `#/idcards` · નવી નોંધણી ચાલુ/બંધ `#/capacity/intake`)
3. પધરામણી → `#/padhramni`
4. રિપોર્ટ → `#/reports` (tabs: રિપોર્ટ · પેનલના આંકડા `#/analytics`)
5. સેટિંગ્સ → `#/settings` (tabs: સેટિંગ્સ · વેબસાઇટ સ્થિતિ `#/site` · યુઝર્સ `#/users` · કોણે શું કર્યું `#/audit`)
6. Group heading **મહોત્સવ તૈયારી**:
   - ટીમો અને હાજરી → `#/teams` (tabs: ટીમો · કોણ ક્યારે આવી શકે `#/availability` · દિવસ મુજબ સેવક જગ્યા `#/capacity/dates`)
   - ભક્તો → `#/devotees`
   - મહોત્સવ અને નિમંત્રણ → `#/programme` (tabs: કાર્યક્રમ · નિમંત્રણ યાદી `#/invitations` · WhatsApp મેસેજ `#/whatsapp` · મેસેજની સ્થિતિ `#/notifications`)
7. Footer: user name + role → મારું ખાતું `#/account`, and લૉગઆઉટ.

Top bar: global search (`#/search`), "અ+" larger-text toggle (keep the existing behaviour), notifications bell with count. The page title appears **once**, in the page header, with that page's single primary action on the right.

**All 20 routes and their permissions stay exactly as now.** Only the menu position changes. A section is shown only if the current role can already see it today.

### Responsive behaviour (already coded in `phc.css` media queries)

| Width / orientation | Shell |
|---|---|
| ≥ 1280 | Full sidebar 256px, icon + label + sub-label |
| 700–1279 | Compact 92px sidebar (icon + short label); split layouts stack to one column |
| < 1180 | Registration time column hidden |
| 700–999 | Day, ID and mobile columns hidden from tables; that info moves to a sub-line under the name |
| < 700 (phone portrait) | Sidebar hidden. Top bar with brand + search icon. **Bottom bar:** આજનું કામ · નોંધણી · પધરામણી · વધુ. "વધુ" opens the full section list (`OvMore`) |
| height ≤ 500 and width ≥ 600 (phone landscape) | 64px icon-only rail on the left, compact top bar, no bottom bar |
| < 360 | Brand text hidden in top bar |

`p-force-land` and `p-force-compact` in the design files are **design-canvas helpers only** (they force landscape/compact styles inside a fixed-size board). In the app, rely on the real media queries in `phc.css` and do not add these classes.

Wider screens (1920) and in-between sizes (1180, 768, 430, 360, 932×430) use the same CSS. Content is capped by the page container, so no separate layouts are needed. Check them during QA (section 7).

---

## 4. Screens (25) and where to find them

| # | Screen | Route | Page component | Key states (`I-*` / `V-*` files) |
|---|---|---|---|---|
| 1 | લૉગિન | login | `Login` | code (2FA), required, invalid, loading, expired, error, logout, keyboard; recovery, help, code-invalid |
| 2 | આજનું કામ | `#/dashboard` | `DashC` | bell panel, error |
| 3 | નોંધણી યાદી | `#/registrations` | `Regs` | filter by seva / day, sort, phone filter sheet, filtered, CSV, bulk done, error |
| 4 | નોંધણી વિગત | drawer from list | `RegDetail` | contact revealed, photo, more-menu, saving, done, reveal-fail, loading; confirm (`OvConfirm`) |
| 5 | ઓળખકાર્ડ | `#/idcards` | `IdCards` | preview (shows the real card front + back, see §4a), confirm approve, none selected, done. Card artwork: `IdCardDesign`, print sheet: `IdCardSheet` |
| 6 | નવી નોંધણી ચાલુ/બંધ | `#/capacity/intake` | `Intake` | override add / error, switch confirm, recount, saving, saved, save fail |
| 7 | પધરામણી | `#/padhramni` | `Padhramni` | week view, detail, purposes, status change, filter sheet |
| 8 | પધરામણીની નવી વિનંતી | from પધરામણી | `PadhramniNew` | review, devotee pick, add purpose, sending, saved, fail |
| 9 | રિપોર્ટ | `#/reports` | `Reports` | CSV, print |
| 10 | પેનલના આંકડા | `#/analytics` | `Analytics` | period picker |
| 11 | સેટિંગ્સ | `#/settings` | `Settings` | saving, saved, fail (field validation shown inline) |
| 12 | વેબસાઇટ સ્થિતિ | `#/site` | `Site` | — |
| 13 | યુઝર્સ અને ભૂમિકા | `#/users` | `Users` | add user, add error, roles tab, sessions, self-block (cannot deactivate own account) |
| 14 | કોણે શું કર્યું | `#/audit` | `Audit` | filter by admin, dates, phone filter sheet, empty |
| 15 | મારું ખાતું | `#/account` | `Account` | password error/done, recovery codes show/confirm |
| 16 | ટીમો | `#/teams` | `Teams` | add, add error, view team, date, empty |
| 17 | કોણ ક્યારે આવી શકે | `#/availability` | `Availability` | — |
| 18 | દિવસ મુજબ સેવક જગ્યા | `#/capacity/dates` | `CapacityDates` | saved, error |
| 19 | ભક્તો | `#/devotees` | `Devotees` | detail, archive, duplicate warning |
| 20 | ભક્ત ઉમેરો | form inside ભક્તો | `DevoteesForm` (= `Devotees` with `form`) | add error, saving, saved |
| 21 | મહોત્સવ કાર્યક્રમ | `#/programme` | `Programme` | — |
| 22 | નિમંત્રણ યાદી | `#/invitations` | `Invitations` | new campaign, new error, open campaign |
| 23 | WhatsApp મેસેજ | `#/whatsapp` | `Whatsapp` | limits, mode confirm, stop (emergency) confirm, real-sending disabled |
| 24 | મેસેજની સ્થિતિ | `#/notifications` | `Notifications` | empty |
| 25 | શોધ | `#/search` | `Search` | minimum-characters hint |

### 4a. Volunteer ID card (સ્વયંસેવક ઓળખકાર્ડ) — `shots/IdCardDesign.jpg`, `shots/IdCardSheet.jpg`

The ID card is a printable component. Its CSS is the `.idc*` block at the end of `assets/phc.css` (print units via `--mm`).

- **Size:** 54 × 86 mm portrait, 3 mm rounded corners, 3 mm bleed, 3 mm safe area, 8 mm free at the top for the lanyard slot. Paper: PVC card or 300 gsm, laminated.
- **Front:** "॥ જય શ્રી વિહત મેલડી માઁ ॥", emblem + "શ્રી વિહત મેલડી ધામ / સાણંદ · ગુજરાત", the gold "મંગળારોહણ" event wordmark, "મૂર્તિ પ્રાણ પ્રતિષ્ઠા મહોત્સવ · ૨ થી ૮ ફેબ્રુઆરી, ૨૦૨૭", arch-framed photo, "સ્વયંસેવક" role pill, name, સેવાનો દિવસ, then a bottom band with the seva name, the SEVA number and that volunteer's QR code.
- **Back:** same header, "પ્રાણ પ્રતિષ્ઠા · ૮ ફેબ્રુઆરી, સોમવાર · બપોરે ૧૨:૩૯", a placeholder line for card instructions (to be decided by the trust), and a QR to shreevihatmeldidhamsanand.com with the text "મંદિરની વેબસાઇટ જોવા સ્કેન કરો".
- **Band colour by seva** (`.idc--b1`…`.idc--b5`: maroon, teal, blue, saffron, grey). The seva name is always written on the band; colour is never the only signal.
- **QR codes:** front QR holds **only the SEVA number**, back QR holds the website URL. Scanning a card in the panel to open the record or mark attendance is a *proposal, not approved*. Do not build it.
- **Not printed on the card:** mobile number, address, age.
- **Missing photo:** the card shows "ફોટો બાકી", stays in "તૈયાર નથી" status and must not be printable.
- **Print sheet:** A4, 9 cards (3 × 3), dashed cut guides, `@page{size:A4;margin:0}`.
- **Fonts on card:** Noto Serif Gujarati for name/headings, Hind Vadodara for the rest; SEVA number in Latin digits, monospace.
- Seva department names, the back-side instructions and the QR scan test before printing are marked **ચકાસણી બાકી**. Use the real seva list from the code and keep the instruction line as a placeholder until the trust supplies it.

Shared patterns: loading skeleton (`StLoading`), empty (`StEmpty`), error with retry (`StError`), all collected on the page "28 · લોડિંગ, ખાલી અને ભૂલ" (`States`). Toast (`OvToast`), confirm dialog (`OvConfirm`), filter sheet (`OvFilter`), "વધુ" menu (`OvMore`).

Each screen has `V-` boards at all 8 sizes in `shots/` and `html/`. Interaction states are mostly at D1440, M390 and ML667. On other sizes they follow the same CSS.

---

## 5. Components and UI rules (see `shots/Components.jpg`, `ComponentsPhone.jpg`)

- **Buttons:** primary (one per page), secondary, plain, danger (only inside a confirm dialog), disabled. Min height 44px; a 40px small variant is allowed on desktop only.
- **Icon buttons** always have a Gujarati `aria-label`.
- **Status badges, each with a distinct shape as well as colour:** નવી · સમીક્ષા થઈ · રદ (registrations); ચાલુ · બંધ · બાકી · મોકલાયો નથી · પહોંચ્યો (other sections). "રદ સિવાયની" is a list filter, not a status, so it has no badge. For invitations keep "બંધ", never "પૂરી".
- **Tabs with counts, filter chips, sort select:** sort options are only the existing ones (નવી પહેલાં · જૂની પહેલાં · નામ મુજબ).
- **Dashboard:** work cards (count + what to do + one link; warm yellow = do first), KPI tiles, link cards. No new metrics, only numbers the current dashboard already has.
- **Privacy:** mobile numbers are masked in lists (`98XXXXXX21`). The full number and photo appear only after an explicit "બતાવો" action in the detail drawer, and that action is audit-logged (as the current system does). Keep the "આ ખાનગી વ્યવસ્થાપન ક્ષેત્ર છે. દરેક કાર્ય ઓડિટ ઇતિહાસમાં નોંધાય છે." notice on login.
- **Tables** become cards on phone (`p-tablebox`/`p-rtbox` rules). Wide tables scroll inside their box, never the page.
- **Forms:** one column on phone, sticky action bar at the bottom (`p-actbar`), inline field errors plus a summary line ("એક ખાનામાં ભૂલ છે — સુધાર્યા પછી જ સાચવી શકાય").
- **Language:** all UI text in Gujarati exactly as in `html/*.html`. Gujarati digits (૦–૯) for counts and dates; phone numbers stay in Latin digits. No emoji.
- **Accessibility:** real `<button>`, `<a>`, `<label>`; visible 3px focus ring; `aria-current` on the active menu item; overlays trap focus and close with Esc; ≥ 4.5:1 text contrast (the tokens already pass); text must not clip when "અ+" is on.

---

## 6. Suggested implementation order

1. Port `phc.css` (and fonts) into the app, scoped under `.p-root`, so the public website styles are untouched.
2. Build the shell (sidebar, top bar, bottom bar, "વધુ") with Menu C grouping, driven by the **existing** route list and permission checks.
3. Shared pieces: page header, tabs, chips, badges, cards, table/card list, toast, confirm, drawer, filter sheet, loading/empty/error.
4. Restyle screens in this order: Login → Dashboard → Registrations (+ detail drawer) → ID cards → Intake → Padhramni (+ new request) → Reports/Analytics → Settings/Site/Users/Audit/Account → Teams/Availability/Capacity → Devotees → Programme/Invitations/WhatsApp/Notifications → Search.
5. For each screen: match `shots/V-<Screen>-D1440.jpg` and `-M390.jpg`, then the `I-<Screen>-*` states that the current code actually has.

---

## 7. Acceptance checklist

- [ ] Every existing route opens, with the same permissions per role as before.
- [ ] No backend, database or API change in the diff (or each one is listed and justified).
- [ ] No sample data or "ઉદાહરણ" labels left in the UI.
- [ ] Screens match the shots at 1440, 1366, 1024, 834, 390, 320, 844×390 and 667×375. Also checked at 1920, 1280, 1180×820, 768, 430, 360 and 932×430: no horizontal page scroll, no overlapping controls, no clipped Gujarati.
- [ ] Phone: bottom bar + "વધુ" work; landscape phone shows the icon rail.
- [ ] Larger text ("અ+") works on every screen.
- [ ] Keyboard: every control reachable, focus visible, dialogs trap focus and close with Esc.
- [ ] Mobile numbers masked by default; reveal is logged.
- [ ] WhatsApp real sending unchanged (still off unless the existing code and config say otherwise).
- [ ] Final report lists every design element **not** implemented because the current system lacks it (especially items marked "ચકાસણી બાકી").
