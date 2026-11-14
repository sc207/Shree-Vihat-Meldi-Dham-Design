# Admin panel — MASTER design v5 (14 Nov 2026)

> **ગુજરાતીમાં:** આ એડમિન પેનલની અંતિમ (માસ્ટર) ડિઝાઇન છે. `meldi-admin-master.html` બ્રાઉઝરમાં ખોલો: ઉપર "Master v5 decisions" વિભાગ, પછી ક્લિક થતો પ્રોટોટાઇપ (ડેસ્કટોપ, ફોન, ટૅબ્લેટ), દરેક સ્ક્રીનની ગેલેરી અને અંદર Claude Code માટેનું પૂરું build brief છે. આ ફાઇલ જૂની Phase C (`../README-FOR-CLAUDE-CODE.md`) કરતાં ઉપર છે.

## What this is

`meldi-admin-master.html` is one self-contained file:

- **Section 00 · Master v5 decisions** — the owner's decisions of 14 Nov 2026.
- **Live prototype** — every admin page working on sample data, on desktop, phone portrait and landscape, and tablet portrait and landscape (iOS and Android). The **States** button shows the shared loading, empty, error, no-permission, offline and session states.
- **Gallery** — every screen and every new form or sheet on all devices.
- **Embedded build brief** — `<script type="text/markdown" id="handoff-brief">`. **Section 0A** has the master decisions and overrides older sections.

It is built on the V4 redesign of 13 Nov (the `meldi-admin-redesign.html` that is also in the code repository under `docs/admin-ux-2026-11-14/`) and adds the owner's decisions.

## Which design wins

| Topic | Source of truth |
|---|---|
| Menu, features, rules, flows, data, tests | **This master file** (section 0A first) |
| Visual detail of screens that exist in both | Phase C in `../` (screenshots, HTML, `phc.css`), adapted to the master menu |
| ID card artwork and `.idc` CSS | Phase C `phc.css`, with the wordmark corrected to **મંગલારોહણ** |
| Public website | `../../design/` — not touched by admin work |

## Prompt for Claude Code

> Read `admin-panel/master/README.md`, then open `admin-panel/master/meldi-admin-master.html` and read the embedded build brief, section 0A first. In the code repository, first check branch `feature/admin-idcard-mangalarohan` and the 14 Nov docs (`ADMIN_REFERENCE_COVERAGE_2026-11-14.md`, `ADMIN_PROPOSALS_NEEDING_APPROVAL_2026-11-14.md`, `PADHRAMNI_WORKFLOW_AUDIT_2026-11-14.md`). For every item in section 0A.2, tell me whether it is already built, partly built or missing. Then build on a new branch, one part at a time, starting with: the real emblem, the મંગલારોહણ spelling on the ID card, the message-policy setting and the 5-tab phone bar. Keep routes, permissions and the public website unchanged unless section 0A says otherwise. Test every rule on staging with the WhatsApp sender in test mode; never use production data. Stop after each part and show me.

## Changes from V4 (summary)

Real emblem; 14-entry menu with પધરામણી and ભક્ત યાદી; 5 phone tabs; full Padhramni (list, week, detail, new request with review, schedule with clash warning, follow-up, complete, cancel, purposes, duplicate warning, devotee link); devotee list; live 8-state ID cards with card preview, A4 sheet, collection details and reprint; attendance (present / absent with reason / pending, QR, team table) and the A4 attendance sheet; WhatsApp message policy (recommended: only "નોંધણી મળી" → about 180 registrations a day); trust-declared invitation consent; WhatsApp, reports, invitations and settings tabs; filters, edit forms, add user, notifications, search; landscape badge fix; dashboard Padhramni card and both countdowns.

All names and numbers in the prototype are invented sample data.
